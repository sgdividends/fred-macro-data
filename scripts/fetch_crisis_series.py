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
    "NCBEILQ027S": "nfc_equity_mktcap", "GDP": "gdp", "T10Y2Y": "curve_10y2y",
}

def fetch(sid):
    r = requests.get(URL, params={"series_id": sid, "api_key": API_KEY, "file_type": "json"}, timeout=60)
    r.raise_for_status()
    return [(o["date"], o["value"]) for o in r.json()["observations"] if o["value"] != "."]

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
    if failed:
        print(f"{len(failed)} series failed: {failed}", file=sys.stderr)

if __name__ == "__main__":
    main()
