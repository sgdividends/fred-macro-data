#!/usr/bin/env python3
"""Fetch the extra FRED series the crisis dashboard needs, in the same
date,value CSV format as fred_fetch.py. Needs FRED_API_KEY. Run from repo root."""
import os, sys
from pathlib import Path
import requests

API_KEY = os.environ.get("FRED_API_KEY")
URL = "https://api.stlouisfed.org/fred/series/observations"
OUT = Path("data/fred")

SERIES = {
    "BAA10Y": "baa10y", "BAMLEMHBHYCRPIOAS": "emhy_oas",
    "DRCCLACBS": "cc_delinq", "DRALACBS": "loan_delinq", "DRSFRMACBS": "mortgage_delinq",
    "TDSP": "debt_service", "DRTSCILM": "sloos_ci", "DRTSCLCC": "sloos_cc",
    "VIXCLS": "vix", "DEXJPUS": "usdjpy", "DTWEXBGS": "broad_dollar",
    "NCBEILQ027S": "nfc_equity_mktcap", "GDP": "gdp", "T10Y2Y": "curve_10y2y", "VXVCLS": "vix3m",
}

def fetch(sid):
    r = requests.get(URL, params={"series_id": sid, "api_key": API_KEY, "file_type": "json"}, timeout=60)
    r.raise_for_status()
    return [(o["date"], o["value"]) for o in r.json()["observations"] if o["value"] != "."]

FINRA_URL = "https://raw.githubusercontent.com/sgdividends/finra-margin-tracker/main/data/finra_margin/margin_debt_history.csv"

def fetch_finra():
    """Copy FINRA margin debt history (lives in the finra-margin-tracker repo) so the dashboard can read it."""
    r = requests.get(FINRA_URL, timeout=60)
    r.raise_for_status()
    dest = Path("data/finra_margin")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "margin_debt_history.csv").write_text(r.text)
    print(f"finra margin_debt_history.csv ({len(r.text.splitlines())} lines)")

MOVE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/%5EMOVE"

def fetch_move():
    """MOVE index is not on FRED. Yahoo's unofficial chart API carries it (values matched Investing.com's
    ICE BofAML MOVE on 28 Sep - 6 Oct 2026). May be rate-limited from CI; the dashboard falls back to data/manual/move_index.csv."""
    r = requests.get(MOVE_URL, params={"range": "10y", "interval": "1d"}, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    import datetime as dt
    rows = [(dt.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"), c) for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c is not None]
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    rows = [(d, c) for d, c in rows if d < today]  # drop today's partial, in-progress bar
    if len(rows) < 1000:
        raise RuntimeError(f"only {len(rows)} MOVE rows")
    (OUT / "move.csv").write_text("date,value\n" + "\n".join(f"{d},{round(v, 2)}" for d, v in rows) + "\n")
    print(f"move.csv ({len(rows)} rows)")

def main():
    if not API_KEY:
        sys.exit("FRED_API_KEY not set")
    OUT.mkdir(parents=True, exist_ok=True)
    failed = []
    for sid, name in SERIES.items():
        try:
            rows = fetch(sid)
            (OUT / f"{name}.csv").write_text("date,value\n" + "\n".join(f"{d},{v}" for d, v in rows) + "\n")
            print(f"{sid:20s} -> {name}.csv ({len(rows)} rows)")
        except Exception as e:
            failed.append(sid); print(f"{sid:20s} FAILED: {e}", file=sys.stderr)
    try:
        fetch_move()
    except Exception as e:
        print(f"MOVE fetch failed ({e}); dashboard will use data/manual/move_index.csv", file=sys.stderr)
    try:
        fetch_finra()
    except Exception as e:
        failed.append("finra"); print(f"finra FAILED: {e}", file=sys.stderr)
    if failed:
        print(f"{len(failed)} series failed: {failed}", file=sys.stderr)

if __name__ == "__main__":
    main()
