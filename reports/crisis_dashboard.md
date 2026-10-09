# Crisis dashboard - 2026-10-09 18:56 UTC

**State: FRAGILE, no trigger yet (late-cycle risk, not a crisis)**

Fragility (worst fragility block or valuation input) 2 | Trigger index (average) 0.11 (0 normal, 1 warn, 2 critical)

Fast trigger lines (any WARN or worse flags a trigger):

- St. Louis Fed stress index: -0.468 - ok
- Chicago Fed NFCI: -0.494 - ok
- VIX: 15.41 - ok
- HY OAS 3m change (pp): 0.45 - ok
- SLOOS C&I net tightening, change vs prior quarter (pp): -8.1 - ok
- SLOOS credit card net tightening, change vs prior quarter (pp): 4.7 - ok
- VIX / VIX3M (>1.0 = inverted, acute stress): 0.852 - ok
- MOVE index (rates vol): 100.7 - ok

| Block | Role | Score | n |
|---|---|---|---|
| Credit pricing | trigger | 0.14 | 7 |
| Household / consumer debt | fragility | 0.14 | 7 |
| Market leverage | fragility | 1.0 | 1 |
| Funding and liquidity | trigger | 0.0 | 2 |
| Growth and rates | trigger | 0.0 | 3 |
| Valuation, vol, global | mixed | 0.4 | 5 |
| Volatility regime | trigger | 0.0 | 2 |

| Indicator | As of | Value | Read | Status | Pctile (own history) | History from |
|---|---|---|---|---|---|---|
| Credit card delinquency rate, banks (%) | 2026-04-01 | 2.85 | 2.85 | ok | 31.7 | 1991-01-01 |
| Household debt service ratio (%) | 2026-04-01 | 11.111 | 11.111 | ok | 22.1 | 2005-01-01 |
| All-loan delinquency rate, banks (%) | 2026-04-01 | 1.42 | 1.42 | ok | 8.4 | 1985-01-01 |
| Single-family mortgage delinquency, banks (%) | 2026-04-01 | 1.86 | 1.86 | ok | 20.4 | 1991-01-01 |
| SLOOS net % tightening, credit cards | 2026-07-01 | 6.7 | 6.7 | ok | 54.5 | 1996-01-01 |
| SLOOS net % tightening C&I, large/mid firms | 2026-07-01 | 0.0 | 0.0 | ok | 51.4 | 1990-04-01 |
| Fitch subprime auto ABS 60+ delinquency (%) | 2026-07-31 | 6.13 | 6.13 | WARN | 66.7* | 2026-01-31 |
| Moody's Baa minus 10y (%) | 2026-10-07 | 1.46 | 1.46 | ok | 3.1 | 1986-01-02 |
| CCC OAS (%) | 2026-10-08 | 12.52 | 12.52 | WARN | 100.0* | 2023-08-01 |
| HY OAS (%) | 2026-10-08 | 3.15 | 3.15 | ok | 59.4* | 2023-07-24 |
| HY OAS 3m change (pp) | 2026-10-08 | 3.15 | 0.45 | ok | 59.4* | 2023-07-24 |
| IG OAS (%) | 2026-10-08 | 0.82 | 0.82 | ok | 40.5* | 2023-07-24 |
| SLOOS credit card net tightening, change vs prior quarter (pp) | 2026-07-01 | 6.7 | 4.7 | ok | 54.5 | 1996-01-01 |
| SLOOS C&I net tightening, change vs prior quarter (pp) | 2026-07-01 | 0.0 | -8.1 | ok | 51.4 | 1990-04-01 |
| Chicago Fed NFCI | 2026-10-02 | -0.494 | -0.494 | ok | 39.8 | 1971-01-08 |
| St. Louis Fed stress index | 2026-10-02 | -0.468 | -0.468 | ok | 29.6 | 1993-12-31 |
| 10y-3m spread (pp) | 2026-10-08 | 0.99 | 0.99 | ok | 34.4 | 1982-01-04 |
| Initial claims 4wk avg, 3m % change | 2026-10-03 | 198000.0 | -11.011 | ok | 2.2 | 1967-01-28 |
| Sahm rule indicator | 2026-09-01 | 0.0 | 0.0 | ok | 43.7 | 1959-12-01 |
| FINRA margin debt y/y (%) | 2026-08-01 | 1.454 | 37.2 | WARN | 89.2 | 1998-01-01 |
| Broad USD index 3m % change | 2026-10-02 | 121.385 | 0.576 | ok | 90.0 | 2006-01-02 |
| EM HY corporate OAS (%) | 2026-10-08 | 3.34 | 3.34 | ok | 28.4* | 2023-10-10 |
| Nonfinancial corp equity / GDP (%) - Buffett-style, percentile only | 2026-04-01 | 255.046 | 255.046 | CRIT | 100.0 | 1947-10-01 |
| USDJPY 3m % change (negative = yen carry unwind) | 2026-10-02 | 157.81 | -1.92 | ok | 70.6 | 1971-01-04 |
| VIX | 2026-10-08 | 15.41 | 15.41 | ok | 34.6 | 1990-01-02 |
| MOVE index (rates vol) | 2026-10-08 | 100.7 | 100.7 | ok | 73.5* | 2016-10-12 |
| VIX3M (info, not scored) | 2026-10-08 | 18.08 | 18.08 | n/a | 37.5 | 2007-12-04 |
| VIX / VIX3M (>1.0 = inverted, acute stress) | 2026-10-08 | 0.852 | 0.852 | ok | 27.7 | 2007-12-04 |

* percentile covers under 10 years of history (HY/IG/CCC/EM HY from 2023, subprime auto file): not a comparison with 2008 or 2020.

_Thresholds are judgment anchors, not backtested. This is a condition read, not a forecast or a timing signal._
