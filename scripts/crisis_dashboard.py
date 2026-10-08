#!/usr/bin/env python3
"""Crisis dashboard. Reads CSVs already in the repo, scores each indicator
0 (normal) / 1 (warn) / 2 (critical) against config/crisis_indicators.json,
averages per block, splits blocks into FRAGILITY (slow-building) and TRIGGER
(fast-moving), and writes reports/crisis_dashboard.{md,json}.

Honest limits: thresholds are judgment anchors, not backtested. Missing data
is excluded from block averages, never scored as 0. Output is a condition
read, not a timing signal or a probability. Run from repo root."""
import json, sys
from pathlib import Path
import pandas as pd

CFG = json.loads(Path("config/crisis_indicators.json").read_text())

def load(path):
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    df.columns = [c.lower() for c in df.columns]
    if "date" not in df or "value" not in df:
        return None
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date", "value"]).sort_values("date")
    return df if len(df) else None

def value_at_or_before(df, date):
    sub = df[df["date"] <= date]
    return None if sub.empty else sub.iloc[-1]

def score(ind, series):
    mode = ind.get("mode", "level")
    last = series.iloc[-1]
    prior = value_at_or_before(series, last["date"] - pd.DateOffset(months=3))
    chg_abs = None if prior is None else last["value"] - prior["value"]
    chg_pct = None if prior is None or prior["value"] == 0 else (last["value"] / prior["value"] - 1) * 100
    x = last["value"] if mode == "level" else chg_pct
    st = None
    if x is not None and ind.get("warn") is not None:
        d = ind.get("dir", 1)
        w, c = ind["warn"], ind["crit"]
        st = 2 if x * d >= c * d else 1 if x * d >= w * d else 0
    # percentile of the latest level vs the indicator's own history
    pct = float((series["value"] <= last["value"]).mean() * 100)
    if st is None and ind.get("pctile_warn") is not None:
        st = 2 if pct >= ind["pctile_crit"] else 1 if pct >= ind["pctile_warn"] else 0
    trig = bool(ind.get("chg3m_trigger") is not None and chg_abs is not None and chg_abs >= ind["chg3m_trigger"])
    return {"id": ind["id"], "label": ind["label"], "block": ind["block"], "date": str(last["date"].date()),
            "value": round(float(last["value"]), 3), "read": None if x is None else round(float(x), 3),
            "chg_3m_abs": None if chg_abs is None else round(float(chg_abs), 3),
            "pctile_own_history": round(pct, 1), "history_start": str(series["date"].iloc[0].date()),
            "status": st, "chg3m_trigger_hit": trig, "note": ind.get("note", "")}

def finra_row():
    df = load_finra()
    if df is None:
        return None
    last = df.iloc[-1]
    yoy = float(last["debit_yoy_pct"])
    st = 2 if yoy >= 50 else 1 if yoy >= 30 else 0
    return {"id": "finra_margin_yoy", "label": "FINRA margin debt y/y (%)", "block": "leverage", "date": str(last["month"].date()),
            "value": round(float(last["debit_balances_musd"]) / 1e6, 3), "read": round(yoy, 1), "chg_3m_abs": None,
            "pctile_own_history": round(float((df["debit_yoy_pct"].dropna() <= yoy).mean() * 100), 1),
            "history_start": str(df["month"].iloc[0].date()), "status": st, "chg3m_trigger_hit": False,
            "note": "value = debit balances in $ trillion. 2000 and 2007 tops came at +60-80% y/y. The crash signal is hot growth followed by a 10%+ drop in 1-2 months."}

def load_finra():
    p = Path("data/finra_margin/margin_debt_history.csv")
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["month"]).sort_values("month")
    return df if df["debit_yoy_pct"].notna().any() else None

def buffett_row():
    a, b = load("data/fred/nfc_equity_mktcap.csv"), load("data/fred/gdp.csv")
    if a is None or b is None:
        return None
    m = pd.merge_asof(a.rename(columns={"value": "eq"}), b.rename(columns={"value": "gdp"}), on="date")
    m = m.dropna()
    m["value"] = m["eq"] / (m["gdp"] * 1000) * 100  # eq in $M, GDP in $B
    s = m[["date", "value"]]
    row = score({"id": "nfc_equity_to_gdp", "label": "Nonfinancial corp equity / GDP (%) - Buffett-style, percentile only",
                 "block": "valuation_vol_global", "mode": "level", "pctile_warn": 90, "pctile_crit": 98, "note": "Not the Wilshire-5000 Buffett ratio (nonfinancial corporate equities only). Scored on percentile of its own history; a long-run upward drift biases the percentile high, so treat as a valuation-stretch flag, not a precise level."}, s)
    return row

# Indicators in non-fragility blocks that still describe fragility (valuation stretch).
FRAGILITY_INPUTS = {"nfc_equity_to_gdp"}

def main():
    rows, gaps = [], []
    for ind in CFG["indicators"]:
        s = load(ind["file"])
        if s is None:
            gaps.append(ind["id"]); continue
        rows.append(score(ind, s))
    for extra in (finra_row(), buffett_row()):
        if extra:
            rows.append(extra)
    blocks = {}
    for k, b in CFG["blocks"].items():
        sts = [r["status"] for r in rows if r["block"] == k and r["status"] is not None]
        blocks[k] = {"label": b["label"], "role": b["role"], "n": len(sts),
                     "score": None if not sts else round(sum(sts) / len(sts), 2)}
    def worst(roles, flagged=True):
        """Fragility is slow-building and one stretched input matters, so use the worst block
        (and any indicator flagged as a fragility input), not an average that dilutes it."""
        v = [b["score"] for b in blocks.values() if b["role"] in roles and b["score"] is not None]
        if flagged:
            v += [r["status"] for r in rows if r["id"] in FRAGILITY_INPUTS and r["status"] is not None]
        return None if not v else round(max(v), 2)
    def avg(roles):
        v = [b["score"] for b in blocks.values() if b["role"] in roles and b["score"] is not None]
        return None if not v else round(sum(v) / len(v), 2)
    frag, trig = worst({"fragility"}), avg({"trigger", "mixed"})
    hits = [r["label"] for r in rows if r["chg3m_trigger_hit"]]
    rule = CFG["alert_rule"]
    empty = [k for k, b in blocks.items() if b["n"] == 0]
    if frag is None or trig is None:
        state = "INSUFFICIENT DATA"
    elif empty:
        state = "PARTIAL DATA (no scored indicators in: " + ", ".join(empty) + ") - do not read as calm"
    elif frag >= rule["fragility_high"] and (trig >= rule["trigger_on"] or hits):
        state = "ALERT: fragile and a trigger is turning"
    elif frag >= rule["fragility_high"]:
        state = "FRAGILE, no trigger yet (late-cycle risk, not a crisis)"
    elif trig >= rule["trigger_on"] or hits:
        state = "TRIGGER ACTIVE on low fragility (shock risk, usually contained)"
    else:
        state = "CALM"
    out = {"as_of": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC"), "state": state,
           "fragility_index": frag, "trigger_index": trig, "trigger_change_hits": hits,
           "blocks": blocks, "indicators": rows, "data_gaps": gaps, "empty_blocks": empty,
           "disclaimer": "Thresholds are judgment anchors, not backtested. This is a condition read, not a forecast or a timing signal."}
    Path("reports").mkdir(exist_ok=True)
    Path("reports/crisis_dashboard.json").write_text(json.dumps(out, indent=2))
    L = [f"# Crisis dashboard - {out['as_of']}", "", f"**State: {state}**", "",
         f"Fragility (worst fragility block or valuation input) {frag} | Trigger index (average) {trig} (0 normal, 1 warn, 2 critical)", ""]
    if hits:
        L += ["3-month jump triggers hit: " + "; ".join(hits), ""]
    L += ["| Block | Role | Score | n |", "|---|---|---|---|"]
    L += [f"| {b['label']} | {b['role']} | {b['score']} | {b['n']} |" for b in blocks.values()]
    L += ["", "| Indicator | As of | Value | Read | Status | Pctile (own history) | History from |", "|---|---|---|---|---|---|---|"]
    names = {0: "ok", 1: "WARN", 2: "CRIT", None: "n/a"}
    for r in sorted(rows, key=lambda r: (r["block"], r["id"])):
        L.append(f"| {r['label']} | {r['date']} | {r['value']} | {r['read']} | {names[r['status']]} | {r['pctile_own_history']} | {r['history_start']} |")
    if gaps:
        L += ["", "Missing data (excluded, not scored as normal): " + ", ".join(gaps)]
    L += ["", "_" + out["disclaimer"] + "_"]
    Path("reports/crisis_dashboard.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    sys.exit(main())
