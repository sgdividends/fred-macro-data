#!/usr/bin/env python3
"""
walcl_regime_bands.py

Rebuilds SKILL.md Section 3a from source: the WALCL QE/QT/Pause classifier and
the regime-conditional threshold bands for NFCI, STLFSI4 and the 10Y-3M curve.

Run this instead of trusting the constants baked into SKILL.md whenever the
pipeline has materially extended, or whenever Section 3a needs to be
reconstructed. Nothing here depends on a FRED API key -- it reads the cached
CSVs straight from the public repo.

    python3 walcl_regime_bands.py

Classifier spec:
    26-week trailing cumulative pct change in WALCL
    >= +3%  -> QE
    <= -3%  -> QT
    else    -> Pause

The 3% magnitude gate suppresses base-effect false positives from short blips
(repo spikes, TGA swings, quarter-end effects). Do not remove it, and do not
shorten the 26-week window -- both changes reintroduce regime whipsaw.
"""

import io
import sys
import urllib.request

import pandas as pd

RAW = "https://raw.githubusercontent.com/sgdividends/fred-macro-data/main/data/fred"

FILES = {
    "walcl": "fed_balance_sheet.csv",
    "nfci": "chicago_fed_nfci.csv",
    "stlfsi": "stl_fed_stress_index.csv",
    "curve": "curve_10y3m.csv",
}

WINDOW = 26          # weeks
GATE = 3.0           # percent
QUANTILES = [10, 25, 50, 75, 90]


def load(name: str, fname: str) -> pd.DataFrame:
    """Fetch a cached FRED CSV and return a clean two-column frame."""
    url = f"{RAW}/{fname}"
    try:
        raw = urllib.request.urlopen(url, timeout=30).read().decode()
    except Exception as e:
        sys.exit(f"FAILED to fetch {url}: {e}")
    if raw.lstrip().startswith("404"):
        sys.exit(f"{fname} not found in repo -- has the pipeline run?")

    df = pd.read_csv(io.StringIO(raw), header=None, names=["date", name])
    # tolerate a header row and any stray non-date lines
    df = df[df["date"].astype(str).str.match(r"\d{4}-\d{2}-\d{2}")].copy()
    df["date"] = pd.to_datetime(df["date"])
    df[name] = pd.to_numeric(df[name], errors="coerce")
    return df.dropna().sort_values("date").reset_index(drop=True)


def classify(pct):
    if pd.isna(pct):
        return None
    if pct >= GATE:
        return "QE"
    if pct <= -GATE:
        return "QT"
    return "Pause"


def main():
    walcl = load("walcl", FILES["walcl"])
    walcl["chg"] = walcl["walcl"].pct_change(WINDOW) * 100
    walcl["regime"] = walcl["chg"].apply(classify)
    walcl = walcl.dropna(subset=["regime"]).reset_index(drop=True)

    cur_reg = walcl["regime"].iloc[-1]
    cur_chg = walcl["chg"].iloc[-1]
    cur_date = walcl["date"].iloc[-1].date()

    print("=" * 72)
    print(f"CURRENT REGIME: {cur_reg}   {WINDOW}w change {cur_chg:+.2f}%   as of {cur_date}")
    print("=" * 72)

    # contiguous episodes, for validating the classifier against known Fed history
    walcl["blk"] = (walcl["regime"] != walcl["regime"].shift()).cumsum()
    ep = walcl.groupby("blk").agg(
        regime=("regime", "first"),
        start=("date", "first"),
        end=("date", "last"),
        n=("date", "size"),
    )
    print(f"\nEpisodes >= 13 weeks (sanity check vs known Fed history):")
    for _, r in ep[ep["n"] >= 13].iterrows():
        print(f"  {r['regime']:5s} {r['start'].date()} -> {r['end'].date()}  ({r['n']}w)")

    regimes = walcl[["date", "regime"]]

    series = [
        ("nfci", "NFCI", "higher = tighter"),
        ("stlfsi", "STLFSI4", "higher = more stress"),
        ("curve", "10Y-3M curve", "higher = steeper"),
    ]

    bands = {}
    for key, label, direction in series:
        df = load(key, FILES[key])
        # attach each observation to the prevailing regime week
        m = pd.merge_asof(
            df.sort_values("date"),
            regimes.sort_values("date"),
            on="date",
            direction="backward",
            tolerance=pd.Timedelta("10D"),
        ).dropna(subset=["regime"])

        print(f"\n--- {label}  ({direction})")
        print(f"    n={len(m)}  {m['date'].min().date()} -> {m['date'].max().date()}")
        hdr = f"    {'regime':7s} {'n':>5s} {'mean':>8s} {'sd':>7s} " + " ".join(
            f"{'p'+str(q):>8s}" for q in QUANTILES
        )
        print(hdr)
        for r in ["QE", "Pause", "QT"]:
            s = m.loc[m["regime"] == r, key]
            if len(s) < 10:
                continue
            qv = [s.quantile(q / 100) for q in QUANTILES]
            print(
                f"    {r:7s} {len(s):5d} {s.mean():8.3f} {s.std():7.3f} "
                + " ".join(f"{v:8.3f}" for v in qv)
            )
            bands[(label, r)] = dict(zip(QUANTILES, qv))

        latest = df[key].iloc[-1]
        in_reg = m.loc[m["regime"] == cur_reg, key]
        pct = (in_reg < latest).mean() * 100
        print(f"    latest = {latest:.3f}  -> {pct:.1f}th percentile within current {cur_reg} regime")

    # derive the green/yellow/red cutoffs actually used in SKILL.md 3a
    print("\n" + "=" * 72)
    print("THRESHOLD BANDS  (stress indices: p50/p90 | curve: p50/p25, flattening = risk)")
    print("=" * 72)
    for label in ["NFCI", "STLFSI4"]:
        for r in ["QE", "Pause", "QT"]:
            b = bands.get((label, r))
            if not b:
                continue
            print(f"  {label:8s} {r:6s}  green < {b[50]:+.3f}   yellow {b[50]:+.3f}..{b[90]:+.3f}   red > {b[90]:+.3f}")
    for r in ["QE", "Pause", "QT"]:
        b = bands.get(("10Y-3M curve", r))
        if not b:
            continue
        print(f"  {'Curve':8s} {r:6s}  green > {b[50]:+.3f}   yellow {b[25]:+.3f}..{b[50]:+.3f}   red < {b[25]:+.3f}")

    print("""
CAVEATS (carried into SKILL.md 3a -- do not drop them when quoting these numbers):
  1. Regime membership is ENDOGENOUS. The Fed runs QE because conditions are
     stressed and QT because they are calm. QT showing the tightest, lowest-
     variance stress distributions is selection, not causation. These bands
     describe co-occurrence only.
  2. QT bands rest on ~3 episodes and are the weakest of the three.
  3. History starts 2003-06 (WALCL begins 2002-12, plus the 26w lookback).
     No dot-com, no 1990s. Roughly 1.5 cycles.
  4. All percentiles here are WITHIN-REGIME. Always state the basis when
     quoting them, since the unconditional figure can differ materially.
""")


if __name__ == "__main__":
    main()
