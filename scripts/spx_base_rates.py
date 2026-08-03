#!/usr/bin/env python3
"""
spx_base_rates.py

Computes the correction / crash base rates that Section 4 of macro-regime-read
depends on, from actual S&P 500 history instead of assumption.

WHY THIS EXISTS
    The base rates in config/regime_factor_weights.json were carried as
    "approximate" and had never been derived. Sensitivity testing (2026-08-03,
    scripts/regime_score.py) showed they move the final probability roughly 3x
    more than any factor weight. They were the weakest empirical link in the
    framework. This script closes that gap the same way scripts/
    walcl_regime_bands.py closed Section 3a.

DEFINITIONS -- these match SKILL.md exactly and are mutually exclusive
    From each date t, look forward N months and take the deepest close-to-close
    decline measured FROM t:

        decline(t) = min(price over (t, t+N]) / price(t) - 1

        Crash       : decline <= -20%
        Correction  : -20% < decline <= -10%
        Neither     : decline > -10%

    This is the "if I am invested today, what can happen from here" framing,
    which is what the framework actually uses. It deliberately avoids defining
    discrete drawdown "episodes", which would require arbitrary peak/trough
    rules and would double-count overlapping windows.

    Note the two buckets are mutually exclusive by construction, which is what
    the Section 5 severity ratio crash/(correction+crash) assumes.

OVERLAPPING WINDOWS
    Consecutive observations share almost all of their forward window, so the
    point estimate is unbiased but naive standard errors are far too small.
    Confidence intervals here use a MOVING BLOCK BOOTSTRAP with block length
    equal to the horizon, which preserves that dependence. An effective sample
    size (non-overlapping windows) is reported alongside the raw n.

DATA
    Primary  : daily ^GSPC via yfinance. Requires network access to Yahoo.
               Works in GitHub Actions and on a normal machine.
    Fallback : Shiller monthly series from GitHub.
               *** Shiller's price column is a MONTHLY AVERAGE of daily closes.
               It smooths away intra-month extremes and therefore UNDERSTATES
               drawdown frequency. Fallback results are a LOWER BOUND. ***

USAGE
    pip install yfinance pandas numpy
    python3 spx_base_rates.py                 # daily if available, else monthly
    python3 spx_base_rates.py --force-monthly
"""

import argparse
import io
import sys
import urllib.request

import numpy as np
import pandas as pd

SHILLER_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv"

HORIZONS = {"3mo": 3, "6mo": 6, "12mo": 12, "18mo": 18}
TRADING_DAYS_PER_MONTH = 21

CORRECTION_THRESHOLD = -0.10
CRASH_THRESHOLD = -0.20

# sample-period splits. pre-war volatility is a different world; report both so
# the choice of sample is visible rather than buried.
PERIODS = [
    ("full", None),
    ("post-1928", "1928-01-01"),
    ("post-1950", "1950-01-01"),
    ("post-1980", "1980-01-01"),
]

N_BOOT = 1000
SEED = 42


# ---------------------------------------------------------------- data loading
def load_daily():
    """Daily ^GSPC closes via yfinance. Returns None if unavailable."""
    try:
        import yfinance as yf
    except ImportError:
        print("[data] yfinance not installed -> falling back to monthly", file=sys.stderr)
        return None
    try:
        df = yf.download("^GSPC", start="1927-01-01", progress=False, auto_adjust=False)
        if df is None or df.empty:
            print("[data] yfinance returned nothing -> falling back", file=sys.stderr)
            return None
        s = df["Close"]
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        s = s.dropna()
        s.index = pd.to_datetime(s.index)
        return s.sort_index()
    except Exception as e:
        print(f"[data] yfinance failed ({e}) -> falling back to monthly", file=sys.stderr)
        return None


def load_monthly():
    """Shiller monthly series. NOTE: monthly AVERAGE of daily closes."""
    raw = urllib.request.urlopen(SHILLER_URL, timeout=30).read().decode()
    df = pd.read_csv(io.StringIO(raw))
    df = df[["Date", "SP500"]].copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["SP500"] = pd.to_numeric(df["SP500"], errors="coerce")
    df = df.dropna().sort_values("Date")
    return pd.Series(df["SP500"].values, index=df["Date"], name="SP500")


# ------------------------------------------------------------------ statistics
def classify_forward(prices: pd.Series, periods_ahead: int) -> pd.Series:
    """
    For each t, deepest decline from price(t) over the next `periods_ahead`
    observations. Returns a Series of {'crash','correction','neither'}.
    """
    vals = prices.values.astype(float)
    n = len(vals)
    out = np.full(n, np.nan)

    # reverse rolling min over the forward window, excluding t itself
    rev = pd.Series(vals[::-1])
    fwd_min = rev.rolling(window=periods_ahead, min_periods=periods_ahead).min().values[::-1]
    # fwd_min[i] currently covers [i-periods+1 .. i] reversed == [i .. i+periods-1]
    # shift by one so the window is (t, t+periods]
    fwd_min = np.concatenate([fwd_min[1:], [np.nan]])

    valid = ~np.isnan(fwd_min)
    out[valid] = fwd_min[valid] / vals[valid] - 1.0

    lab = pd.Series(index=prices.index, dtype=object)
    lab[:] = None
    d = pd.Series(out, index=prices.index)
    lab[d <= CRASH_THRESHOLD] = "crash"
    lab[(d > CRASH_THRESHOLD) & (d <= CORRECTION_THRESHOLD)] = "correction"
    lab[d > CORRECTION_THRESHOLD] = "neither"
    return lab.dropna()


def block_bootstrap_ci(labels: pd.Series, target: str, block: int, n_boot=N_BOOT, seed=SEED):
    """Moving-block bootstrap CI for the proportion of `target`, respecting overlap."""
    rng = np.random.default_rng(seed)
    arr = (labels.values == target).astype(float)
    n = len(arr)
    if n < block * 2:
        return (np.nan, np.nan)
    n_blocks = int(np.ceil(n / block))
    max_start = n - block
    props = np.empty(n_boot)
    for b in range(n_boot):
        starts = rng.integers(0, max_start + 1, size=n_blocks)
        samp = np.concatenate([arr[s:s + block] for s in starts])[:n]
        props[b] = samp.mean()
    return (float(np.percentile(props, 2.5)), float(np.percentile(props, 97.5)))


def run(prices: pd.Series, freq: str, label: str):
    per_month = TRADING_DAYS_PER_MONTH if freq == "daily" else 1

    print("\n" + "=" * 82)
    print(f"SAMPLE: {label}   n={len(prices)} {freq} obs   "
          f"{prices.index.min().date()} -> {prices.index.max().date()}")
    print("=" * 82)
    print(f"  {'horizon':8s} {'n':>7s} {'eff_n':>6s} {'correction':>12s} {'95% CI':>16s} "
          f"{'crash':>8s} {'95% CI':>16s} {'severity':>9s}")

    results = {}
    for hname, months in HORIZONS.items():
        ahead = months * per_month
        lab = classify_forward(prices, ahead)
        if len(lab) < ahead * 2:
            print(f"  {hname:8s}  insufficient history")
            continue
        p_corr = (lab == "correction").mean()
        p_crash = (lab == "crash").mean()
        ci_c = block_bootstrap_ci(lab, "correction", ahead)
        ci_k = block_bootstrap_ci(lab, "crash", ahead)
        sev = p_crash / (p_corr + p_crash) if (p_corr + p_crash) > 0 else float("nan")
        eff_n = len(lab) // ahead
        print(f"  {hname:8s} {len(lab):7d} {eff_n:6d} "
              f"{p_corr*100:11.1f}% [{ci_c[0]*100:5.1f},{ci_c[1]*100:5.1f}] "
              f"{p_crash*100:7.1f}% [{ci_k[0]*100:5.1f},{ci_k[1]*100:5.1f}] "
              f"{sev*100:8.1f}%")
        results[hname] = {"correction": p_corr, "crash": p_crash}
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force-monthly", action="store_true")
    args = ap.parse_args()

    prices, freq = (None, None)
    if not args.force_monthly:
        prices = load_daily()
        freq = "daily"
    if prices is None:
        prices = load_monthly()
        freq = "monthly"

    print("=" * 82)
    print(f"SPX BASE RATES   source={freq}")
    print("=" * 82)
    if freq == "monthly":
        print("""
*** WARNING -- MONTHLY FALLBACK IN USE ***
Shiller's price column is a MONTHLY AVERAGE of daily closes, not a month-end
close. Averaging smooths away intra-month extremes, so every number below
UNDERSTATES the true drawdown frequency. Treat these as a LOWER BOUND, not as
the base rates to publish. Re-run with daily ^GSPC (yfinance, works in GitHub
Actions) for figures fit to write into the config.
""")

    all_res = {}
    for name, start in PERIODS:
        p = prices if start is None else prices[prices.index >= start]
        if len(p) < 400:
            continue
        all_res[name] = run(p, freq, name)

    print("\n" + "=" * 82)
    print("CONFIG COMPARISON  --  current assumed values vs computed")
    print("=" * 82)
    assumed = {
        "correction": {"3mo": 0.10, "6mo": 0.18, "12mo": 0.30, "18mo": 0.36},
        "crash": {"3mo": 0.03, "6mo": 0.06, "12mo": 0.12, "18mo": 0.17},
    }
    ref = all_res.get("post-1950") or next(iter(all_res.values()))
    print(f"  reference sample: post-1950\n")
    print(f"  {'horizon':8s} {'kind':11s} {'assumed':>9s} {'computed':>10s} {'delta':>9s}")
    for kind in ("correction", "crash"):
        for h in HORIZONS:
            if h not in ref:
                continue
            a, c = assumed[kind][h], ref[h][kind]
            print(f"  {h:8s} {kind:11s} {a*100:8.1f}% {c*100:9.1f}% {(c-a)*100:+8.1f}pp")

    print("""
NEXT STEP
    Do NOT paste these into config/regime_factor_weights.json straight from a
    monthly run. Run with daily data, decide the sample period deliberately
    (post-1950 is the usual compromise: enough history to be stable, recent
    enough to reflect a modern market structure), then update the config and
    re-run scripts/regime_score.py to see how much the framework output moves.
""")


if __name__ == "__main__":
    main()
