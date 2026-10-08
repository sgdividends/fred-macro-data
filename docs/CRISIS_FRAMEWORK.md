# Crisis framework (proposal, draft)

Goal: read credit and debt conditions against past crises (1929, 1987, 1997 Asia, 2000, 2007-08, 2020). It gives a condition read, not a timing call.

## Structure
Fragility (slow build: debt, leverage, valuation) versus Trigger (fast: spreads, funding, vol, growth). Alarm = high fragility AND a trigger turning. High fragility alone is late-cycle, not a crisis.

| Block | Role | Indicators | Historical anchors (approximate) |
|---|---|---|---|
| Credit pricing | trigger | HY/IG/CCC OAS, Baa-10y, EM HY | HY OAS thresholds (<3.5 complacent, 5-6 stress, >8 crisis) are judgment anchors. HY 2008/2020 peaks and "+150bp in 3m flagged 2007, 2018, 2020" are UNVERIFIED here (repo HY history starts 2023-07). Verified long-history benchmark, Baa-10y spread: 2001-02 peak 3.90, 2008 peak 6.16 (4 Dec 2008), 2020 peak 4.31 (23 Mar 2020) |
| Consumer debt | fragility | card/loan/mortgage delinquency, debt service ratio, SLOOS, Fitch subprime auto (manual file) | Card delinquency 2009-10 peak ~6.8%; net SLOOS C&I tightening is a confirming signal, not a leading one: it read 50-60 in 2001, 32-84 through 2008 (but 0-19 during 2007, when the recession began) and 41-71 in 2020, and gave a false positive in 2022-23 (24-51, no recession) |
| Leverage | fragility | FINRA margin debt y/y, hedge-fund prime-broker margin, CFTC lev-fund net | Margin debt y/y peaked at 80.5% (2000), 62.6% (2007), 71.6% (2021); now +37% (percentile since 1998) |
| Funding/liquidity | trigger | NFCI, STLFSI, ON RRP, SOFR vs EFFR | STLFSI4 peaked at 9.66 (10 Oct 2008) and 5.62 (20 Mar 2020) |
| Growth/rates | trigger | 10y-3m, Sahm, claims | Sahm >= 0.5 = recession signal |
| Valuation/vol/global | mixed | VIX, USDJPY, broad USD, EM spreads, Buffett-style ratio | VIX >35 crisis; yen strength + dollar jumps mark carry unwinds |

## Known gaps (not yet automated)
CAPE and equity risk premium (needs a data source), VVIX/SKEW/MOVE (not on FRED), breadth (compute from stock-research-data), cross-currency basis, SRF usage, Treasury auction tails, China credit, a rebuilt SEC refi wall.

## Honest limits
- Thresholds are judgment anchors from historical ranges. They are not fitted or backtested.
- Only ~5-8 independent crises exist, so weights cannot be fitted tightly.
- HY OAS history here starts 2023-07 (FRED/ICE licence). Use Baa-10y for 2008/2020 comparisons.
- Subprime auto file is manual and from secondary sources. Fitch revised its whole history in July 2026, so the Jan 2026 6.90% record is unverified on the current series and likely pre-revision. Compare only values from the same vintage.
- Percentiles for HY/IG/CCC/EM HY (2023+) and the 3-row subprime file cover a short history and are marked with * in the dashboard. Do not read them as comparisons with 2008.
- Next step: backtest block scores against forward 12-month drawdowns using the long series.
