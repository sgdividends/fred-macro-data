#!/usr/bin/env python3
"""
fred_fetch.py
Pulls a fixed set of FRED series via the public API, caches each to its own
CSV under data/fred/, dedupes on date, and prints a latest-reading summary.
Requires env var FRED_API_KEY.
"""

import os
import sys
import datetime as dt
from pathlib import Path
import requests
import pandas as pd

API_KEY = os.environ.get("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
CACHE_DIR = Path("data/fred")

# series_id -> (short name, human label)
SERIES = {
    "BAMLH0A0HYM2": ("hy_oas", "ICE BofA High Yield OAS"),
    "BAMLC0A0CM":   ("ig_oas", "ICE BofA Investment Grade OAS"),
    "SAHMREALTIME": ("sahm_realtime", "Sahm Rule Recession Indicator"),
    "UNRATE":       ("unemployment_rate", "U.S. Unemployment Rate"),
    "NFCI":         ("chicago_fed_nfci", "Chicago Fed Financial Conditions Index"),
    "STLFSI4":      ("stl_fed_stress_index", "St. Louis Fed Financial Stress Index"),
    "T10Y3M":       ("curve_10y3m", "10Y-3M Treasury Spread"),
    "DGS10":        ("treasury_10y", "10-Year Treasury Yield"),
    "DGS2":         ("treasury_2y", "2-Year Treasury Yield"),
    "WRMFNS":       ("money_market_fund_assets", "Money Market Fund Assets"),
    "RRPONTSYD":    ("reverse_repo_volume", "Overnight Reverse Repo Volume"),
    "WALCL":        ("fed_balance_sheet", "Fed Total Assets (Balance Sheet)"),
    "M2SL": ("us_m2", "US M2 Money Stock"),
     "BAMLH0A3HYC":  "ccc_oas.csv",              
    "BAMLH0A1HYBB": "bb_oas.csv",               
    "IC4WSA":       "initial_claims_4wk.csv",   
    "ICSA":         "initial_claims.csv", 
       "DFII10": ("treasury_10y_real", "10-Year TIPS Real Yield"),
       "GFDEBTN": ("us_federal_debt", "Federal Debt: Total Public Debt"),
    "DFII30": ("treasury_30y_real", "30-Year TIPS Real Yield"),
    "BOGZ1FL624123035Q": ("hedge_fund_prime_broker_margin", "Hedge Funds: Prime Brokerage Margin Borrowing (Z.1)"),
    "BOGZ1FL663067003Q": ("broker_dealer_margin_receivables", "Broker-Dealer Margin Loan Receivables from Customers (Z.1)"),
"DGS30":  ("treasury_30y", "30-Year Treasury Yield"),
"DTB3":   ("tbill_3m", "3-Month T-Bill"),
    "DCPN3M": ("cp_3m_nonfin", "90-Day AA Nonfinancial Commercial Paper Rate"), 
    "EXPINF10YR": ("infl_exp_10y_cleveland", "Cleveland Fed 10-Yr Expected Inflation"),  # 1982+, primary
"MICH":       ("infl_exp_1y_michigan",   "U.Michigan 1-Yr Inflation Expectation"),   # 1978+, cross-check
"CPIAUCSL":   ("cpi",                    "CPI All Urban Consumers"),                 # 1947+, trailing proxy
}

def fetch_series(series_id: str) -> pd.DataFrame:
    if not API_KEY:
        raise RuntimeError("FRED_API_KEY environment variable is not set.")
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    obs = data.get("observations", [])
    if not obs:
        raise RuntimeError(f"No observations returned for {series_id}: {data}")

    df = pd.DataFrame(obs)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    # FRED encodes missing points as "."
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"]).sort_values("date").reset_index(drop=True)
    return df

def update_cache(df_new: pd.DataFrame, path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        df_old = pd.read_csv(path, parse_dates=["date"])
        merged = pd.concat([df_old, df_new]).drop_duplicates(
            subset="date", keep="last"
        ).sort_values("date")
    else:
        merged = df_new
    merged.to_csv(path, index=False)
    return merged

def main():
    print(f"[{dt.datetime.now()}] Fetching {len(SERIES)} FRED series...")
    failures = []
    for series_id, (short_name, label) in SERIES.items():
        try:
            df_new = fetch_series(series_id)
            path = CACHE_DIR / f"{short_name}.csv"
            merged = update_cache(df_new, path)
            latest = merged.iloc[-1]
            print(f"  {series_id:15s} ({label}): "
                  f"{latest['date'].strftime('%Y-%m-%d')} = {latest['value']} "
                  f"[{len(merged)} rows]")
        except Exception as e:
            failures.append((series_id, str(e)))
            print(f"  {series_id:15s} FAILED: {e}", file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} of {len(SERIES)} series failed.", file=sys.stderr)
        sys.exit(1)
    print("\nAll series updated successfully.")

if __name__ == "__main__":
    main()
