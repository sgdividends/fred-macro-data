#!/usr/bin/env python3
"""
regime_dating.py
Classifies the Fed's balance sheet (WALCL) history into QE / QT / Pause-Neutral
episodes using a 13-week rate-of-change threshold with a persistence filter to
suppress single-week noise (bill paydowns, coupon settlement, discount window
blips) from flipping the classification.

Reads from data/fred/fed_balance_sheet.csv (added to fred_fetch.py's SERIES
dict; populated daily by the existing FRED Series Daily Fetch workflow).
Expects the standard fred_fetch.py output columns: date, value.

Run from the repo root:
    python regime_dating.py
"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/fred/fed_balance_sheet.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

# 13-week (~1 quarter) rate of change
df["chg_13wk_pct"] = df["value"].pct_change(13) * 100

# Classification thresholds. WALCL is a weekly series with real week-to-week
# noise even inside a stable regime, so a single-week move doesn't flip the
# regime. 13wk window smooths that while staying short enough to catch
# genuine turns within ~1 quarter.
def classify(chg):
    if pd.isna(chg):
        return "Insufficient history"
    if chg > 1.5:
        return "QE"
    elif chg < -1.5:
        return "QT"
    else:
        return "Pause/Neutral"

df["regime"] = df["chg_13wk_pct"].apply(classify)

# Collapse into contiguous regime episodes (only flip on a persistent break;
# require the new regime to hold for at least 4 consecutive weeks to avoid
# whipsaw right at the +/-1.5% boundary)
df["regime_raw"] = df["regime"]
regimes = df["regime_raw"].tolist()
dates = df["date"].tolist()

confirmed = [regimes[0]]
for i in range(1, len(regimes)):
    if regimes[i] == confirmed[-1]:
        confirmed.append(confirmed[-1])
        continue
    # look ahead up to 4 weeks to see if this new state persists
    lookahead = regimes[i:i+4]
    if lookahead.count(regimes[i]) >= 3:  # majority of next 4 weeks agree
        confirmed.append(regimes[i])
    else:
        confirmed.append(confirmed[-1])  # treat as noise, keep prior regime

df["regime_confirmed"] = confirmed

# Build episode table
episodes = []
cur_regime = df["regime_confirmed"].iloc[0]
start_date = df["date"].iloc[0]
start_val = df["value"].iloc[0]
for i in range(1, len(df)):
    if df["regime_confirmed"].iloc[i] != cur_regime:
        end_date = df["date"].iloc[i-1]
        end_val = df["value"].iloc[i-1]
        episodes.append({
            "regime": cur_regime,
            "start": start_date.date(),
            "end": end_date.date(),
            "weeks": (end_date - start_date).days // 7,
            "start_bn": round(start_val/1000, 1),
            "end_bn": round(end_val/1000, 1),
            "pct_change": round((end_val-start_val)/start_val*100, 1)
        })
        cur_regime = df["regime_confirmed"].iloc[i]
        start_date = df["date"].iloc[i]
        start_val = df["value"].iloc[i]
# final episode
end_date = df["date"].iloc[-1]
end_val = df["value"].iloc[-1]
episodes.append({
    "regime": cur_regime,
    "start": start_date.date(),
    "end": end_date.date(),
    "weeks": (end_date - start_date).days // 7,
    "start_bn": round(start_val/1000, 1),
    "end_bn": round(end_val/1000, 1),
    "pct_change": round((end_val-start_val)/start_val*100, 1)
})

ep_df = pd.DataFrame(episodes)
ep_df.to_csv("regime_episodes.csv", index=False)
df.to_csv("walcl_with_regime.csv", index=False)

print("=== Regime episodes (only showing episodes >= 8 weeks to filter noise) ===")
big_eps = ep_df[ep_df["weeks"] >= 8]
print(big_eps.to_string(index=False))

print("\n=== ALL episodes, including short ones -- check these for false positives ===")
print("(e.g. a 'QE' episode with single-digit pct_change over a handful of weeks")
print(" is very likely a base-effect blip crossing the threshold, not real QE --")
print(" cross-check magnitude against the big episodes above before trusting a")
print(" short one.)")
print(ep_df.to_string(index=False))

print("\n=== Current regime ===")
print(df.iloc[-1][["date", "value", "chg_13wk_pct", "regime_confirmed"]])
