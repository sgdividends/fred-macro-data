#!/usr/bin/env python3
"""
regime_score.py

Executes the Section 3b factor-grouping arithmetic for macro-regime-read.
Reads weights and base rates from config/regime_factor_weights.json, takes the
seven factor scores as input, and emits:

    1. the multi-horizon correction / crash probability table
    2. severity ratios
    3. a per-factor contribution decomposition of the composite S
    4. a weight-sensitivity analysis

Purpose. The composite arithmetic was previously done by hand, three times in
one session. Hand arithmetic across 7 factors x 4 horizons is error-prone and
unauditable. This makes it reproducible and shows the working.

IMPORTANT -- what this does NOT do. The weights in the config are judgment, not
fitted parameters. Nothing here validates them. The sensitivity block exists so
you can see whether the output is even sensitive to the weights: if perturbing
them barely moves the answer, arguing about the exact values is wasted effort,
and the real uncertainty lives in the base rates and the row scoring instead.

Usage:
    python3 regime_score.py                    # runs with SCORES below
    python3 regime_score.py --config path.json

Edit SCORES to the current read's factor averages before running.
"""

import argparse
import io
import json
import sys
import urllib.request

CONFIG_URL = (
    "https://raw.githubusercontent.com/sgdividends/fred-macro-data/"
    "main/config/regime_factor_weights.json"
)

# ---------------------------------------------------------------------------
# Factor scores for the current read. Range -1 (all Bullish) to +2 (all
# Critical). Average the row scores WITHIN each factor; exclude genuine data
# gaps from the average rather than scoring them 0.
#
# Values below are the 2026-08-03 read.
# ---------------------------------------------------------------------------
SCORES = {
    "positioning_vol":     -0.17,   # breadth/concentration constructive; VVIX, USDJPY offset
    "credit_risk_pricing": -0.40,   # 4 rows Bullish; CCC-BB quality spread Critical
    "liquidity_funding":   -0.20,   # NFCI/STLFSI4/CP-Tbill green; ON RRP drained Critical
    "rates_duration":       1.00,   # all 4 rows Caution: MOVE, curve, real yields, duration ETFs
    "growth_labor":        -0.50,   # Sahm/UNRATE/claims clean; refi wall Caution
    "leverage":             1.20,   # FINRA +70.7% and Z.1 HF +44.3% both Critical
    "valuation":            2.00,   # ERP negative; single-row factor, fragile
}


def load_config(path_or_url):
    if path_or_url.startswith("http"):
        raw = urllib.request.urlopen(path_or_url, timeout=30).read().decode()
    else:
        raw = open(path_or_url).read()
    cfg = json.loads(raw)

    # validate weight columns sum to 1.00
    fw = {k: v for k, v in cfg["factor_weights"].items() if not k.startswith("_")}
    for h in cfg["horizons"]:
        tot = sum(fw[f][h] for f in fw)
        if abs(tot - 1.0) > 1e-9:
            sys.exit(f"CONFIG ERROR: {h} weights sum to {tot:.4f}, expected 1.00")
    return cfg, fw


def composite(scores, fw, horizon):
    return sum(scores[f] * fw[f][horizon] for f in fw)


def probabilities(cfg, fw, scores):
    out = {}
    lo = cfg["adjustment_rule"]["clamp_low"]
    hi = cfg["adjustment_rule"]["clamp_high"]
    for h in cfg["horizons"]:
        S = composite(scores, fw, h)
        adj = max(lo, min(hi, S)) * cfg["caps"][h]
        corr = cfg["base_rates"]["correction"][h] * (1 + adj)
        crash = cfg["base_rates"]["crash"][h] * (1 + adj)
        out[h] = {
            "S": S,
            "adj": adj,
            "correction": corr,
            "crash": crash,
            "severity": crash / (corr + crash),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=CONFIG_URL)
    args = ap.parse_args()

    cfg, fw = load_config(args.config)
    missing = set(fw) - set(SCORES)
    if missing:
        sys.exit(f"Missing factor scores for: {sorted(missing)}")

    res = probabilities(cfg, fw, SCORES)

    print("=" * 78)
    print(f"REGIME SCORE  --  config v{cfg['version']} ({cfg['updated']})")
    print("=" * 78)

    print("\nFACTOR SCORES")
    for f in sorted(fw, key=lambda x: -SCORES[x]):
        bar = "#" * int(abs(SCORES[f]) * 12)
        side = "risk+" if SCORES[f] > 0 else "risk-"
        print(f"  {f:22s} {SCORES[f]:+6.2f}  {side} {bar}")

    print("\nPROBABILITY TABLE")
    print(f"  {'horizon':8s} {'S':>7s} {'adj':>8s} {'correction':>12s} {'crash':>9s} {'severity':>10s}")
    for h in cfg["horizons"]:
        r = res[h]
        print(
            f"  {h:8s} {r['S']:+7.3f} {r['adj']*100:+7.1f}% "
            f"{r['correction']*100:11.1f}% {r['crash']*100:8.1f}% {r['severity']*100:9.1f}%"
        )

    print("\nCONTRIBUTION TO COMPOSITE S  (factor score x weight)")
    print(f"  {'factor':22s}" + "".join(f"{h:>10s}" for h in cfg["horizons"]))
    for f in fw:
        row = "".join(f"{SCORES[f]*fw[f][h]:+10.3f}" for h in cfg["horizons"])
        print(f"  {f:22s}{row}")
    print(f"  {'TOTAL':22s}" + "".join(f"{res[h]['S']:+10.3f}" for h in cfg["horizons"]))

    # ---- sensitivity -------------------------------------------------------
    print("\n" + "=" * 78)
    print("WEIGHT SENSITIVITY  --  does the answer actually depend on the weights?")
    print("=" * 78)
    print("Each factor's weight is shifted +/-0.05, others renormalised to keep the")
    print("column at 1.00. Reported: resulting swing in the 12mo crash probability.\n")

    base12 = res["12mo"]["crash"]
    print(f"  baseline 12mo crash = {base12*100:.2f}%\n")
    print(f"  {'factor perturbed':22s} {'w-0.05':>10s} {'w+0.05':>10s} {'swing':>9s}")
    worst = 0.0
    for f in fw:
        vals = []
        for delta in (-0.05, 0.05):
            w2 = {k: dict(v) for k, v in fw.items()}
            neww = w2[f]["12mo"] + delta
            if neww < 0:
                vals.append(None)
                continue
            w2[f]["12mo"] = neww
            others = [k for k in w2 if k != f]
            rem = 1.0 - neww
            osum = sum(fw[k]["12mo"] for k in others)
            for k in others:
                w2[k]["12mo"] = fw[k]["12mo"] / osum * rem
            S2 = composite(SCORES, w2, "12mo")
            adj2 = max(-1, min(1, S2)) * cfg["caps"]["12mo"]
            vals.append(cfg["base_rates"]["crash"]["12mo"] * (1 + adj2))
        lo = f"{vals[0]*100:9.2f}%" if vals[0] is not None else "      n/a"
        hi = f"{vals[1]*100:9.2f}%" if vals[1] is not None else "      n/a"
        pts = [v for v in vals if v is not None]
        swing = (max(pts) - min(pts)) * 100 if len(pts) > 1 else 0.0
        worst = max(worst, swing)
        print(f"  {f:22s} {lo} {hi} {swing:8.2f}pp")

    print(f"\n  Max swing from any single +/-0.05 weight change: {worst:.2f}pp")
    print(f"  For scale, the base rate itself is {cfg['base_rates']['crash']['12mo']*100:.0f}%.")
    print("""
  READ THIS. If the max swing is small relative to the base rate, the weights
  are NOT where the uncertainty lives -- the base rates and the row-level
  Bullish/Neutral/Caution/Critical scoring are. Arguing about a 0.05 weight
  shift is then noise. Spend the effort on (a) recomputing base rates from
  actual SPX drawdown history, and (b) tightening the row scoring rules.
""")


if __name__ == "__main__":
    main()
