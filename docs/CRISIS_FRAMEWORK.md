# Crisis framework (proposal, draft)

Goal: read credit and debt conditions against past crises (1929, 1987, 1997 Asia, 2000, 2007-08, 2020). It gives a condition read, not a timing call.

## Structure
Fragility (slow build: debt, leverage, valuation) versus Trigger (fast: spreads, funding, vol, growth). Alarm = high fragility AND a trigger turning. High fragility alone is late-cycle, not a crisis.

| Block | Role | Indicators | Historical anchors (approximate) |
|---|---|---|---|
| Credit pricing | trigger | HY/IG/CCC OAS, Baa-10y, EM HY | HY OAS: <3.5 complacent, 5-6 stress, >8 crisis (2008 ~20, 2020 ~11). +150bp in 3m flagged 2007, 2018, 2020 |
| Consumer debt | fragility | card/loan/mortgage delinquency, debt service ratio, SLOOS, Fitch subprime auto (manual file) | Card delinquency 2009-10 peak ~6.8%; net SLOOS tightening >20% preceded recessions |
| Leverage | fragility | FINRA margin debt y/y, hedge-fund prime-broker margin, CFTC lev-fund net | Margin debt +60-80% y/y at 2000 and 2007 tops; now +37% |
| Funding/liquidity | trigger | NFCI, STLFSI, ON RRP, SOFR vs EFFR | STLFSI ~5 in 2008 and 2020 |
| Growth/rates | trigger | 10y-3m, Sahm, claims | Sahm >= 0.5 = recession signal |
| Valuation/vol/global | mixed | VIX, USDJPY, broad USD, EM spreads, Buffett-style ratio | VIX >35 crisis; yen strength + dollar jumps mark carry unwinds |

## Known gaps (not yet automated)
CAPE and equity risk premium (needs a data source), VVIX/SKEW/MOVE (not on FRED), breadth (compute from stock-research-data), cross-currency basis, SRF usage, Treasury auction tails, China credit, a rebuilt SEC refi wall.

## Honest limits
- Thresholds are judgment anchors from historical ranges. They are not fitted or backtested.
- Only ~5-8 independent crises exist, so weights cannot be fitted tightly.
- HY OAS history here starts 2023-07 (FRED/ICE licence). Use Baa-10y for 2008/2020 comparisons.
- Subprime auto file is manual and from secondary sources. Fitch revised its series in July 2026.
- Next step: backtest block scores against forward 12-month drawdowns using the long series.
