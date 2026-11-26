# Crisis dashboard - 2026-11-26 22:30 UTC

**State: ALERT: fragile and a trigger is turning**

Fragility (worst fragility block or valuation input) 2 | Trigger index (average) 0.32 (0 normal, 1 warn, 2 critical)

Fast trigger lines (any WARN or worse flags a trigger):

- St. Louis Fed stress index: -0.07 - ok
- Chicago Fed NFCI: -0.444 - ok
- VIX: 26.36 - WARN
- HY OAS 3m change (pp): 1.03 - WARN
- SLOOS C&I net tightening, change vs prior quarter (pp): 1.7 - ok
- SLOOS credit card net tightening, change vs prior quarter (pp): -2.7 - ok
- VIX / VIX3M (>1.0 = inverted, acute stress): 1.035 - WARN
- MOVE index (rates vol): 97.54 - ok

Triggers hit: VIX (WARN); HY OAS 3m change (pp) (WARN); VIX / VIX3M (>1.0 = inverted, acute stress) (WARN)

| Block | Role | Score | n |
|---|---|---|---|
| Credit pricing | trigger | 0.29 | 7 |
| Household / consumer debt | fragility | 0.14 | 7 |
| Market leverage | fragility | 0.0 | 1 |
| Funding and liquidity | trigger | 0.0 | 2 |
| Growth and rates | trigger | 0.0 | 3 |
| Valuation, vol, global | mixed | 0.8 | 5 |
| Volatility regime | trigger | 0.5 | 2 |

| Indicator | As of | Value | Read | Status | Pctile (own history) | History from |
|---|---|---|---|---|---|---|
| Credit card delinquency rate, banks (%) | 2026-04-01 | 2.85 | 2.85 | ok | 31.7 | 1991-01-01 |
| Household debt service ratio (%) | 2026-04-01 | 11.111 | 11.111 | ok | 22.1 | 2005-01-01 |
| All-loan delinquency rate, banks (%) | 2026-04-01 | 1.42 | 1.42 | ok | 8.4 | 1985-01-01 |
| Single-family mortgage delinquency, banks (%) | 2026-04-01 | 1.86 | 1.86 | ok | 20.4 | 1991-01-01 |
| SLOOS net % tightening, credit cards | 2026-10-01 | 4.0 | 4.0 | ok | 47.6 | 1996-01-01 |
| SLOOS net % tightening C&I, large/mid firms | 2026-10-01 | 1.7 | 1.7 | ok | 53.1 | 1990-04-01 |
| Fitch subprime auto ABS 60+ delinquency (%) | 2026-07-31 | 6.13 | 6.13 | WARN | 66.7* | 2026-01-31 |
| Moody's Baa minus 10y (%) | 2026-11-24 | 1.61 | 1.61 | ok | 13.7 | 1986-01-02 |
| CCC OAS (%) | 2026-11-24 | 14.05 | 14.05 | WARN | 100.0* | 2023-08-01 |
| HY OAS (%) | 2026-11-24 | 3.72 | 3.72 | ok | 85.7* | 2023-07-24 |
| HY OAS 3m change (pp) | 2026-11-24 | 3.72 | 1.03 | WARN | 85.7* | 2023-07-24 |
| IG OAS (%) | 2026-11-24 | 0.98 | 0.98 | ok | 77.7* | 2023-07-24 |
| SLOOS credit card net tightening, change vs prior quarter (pp) | 2026-10-01 | 4.0 | -2.7 | ok | 47.6 | 1996-01-01 |
| SLOOS C&I net tightening, change vs prior quarter (pp) | 2026-10-01 | 1.7 | 1.7 | ok | 53.1 | 1990-04-01 |
| Chicago Fed NFCI | 2026-11-20 | -0.444 | -0.444 | ok | 44.9 | 1971-01-08 |
| St. Louis Fed stress index | 2026-11-20 | -0.07 | -0.07 | ok | 61.2 | 1993-12-31 |
| 10y-3m spread (pp) | 2026-11-25 | 0.51 | 0.51 | ok | 23.2 | 1982-01-04 |
| Initial claims 4wk avg, 3m % change | 2026-11-21 | 196000.0 | -4.039 | ok | 1.8 | 1967-01-28 |
| Sahm rule indicator | 2026-10-01 | 0.0 | 0.0 | ok | 43.8 | 1959-12-01 |
| FINRA margin debt y/y (%) | 2026-10-01 | 1.448 | 22.4 | ok | 68.8 | 1998-01-01 |
| Broad USD index 3m % change | 2026-11-20 | 123.598 | 4.518 | WARN | 95.6 | 2006-01-02 |
| EM HY corporate OAS (%) | 2026-11-24 | 4.38 | 4.38 | ok | 88.5* | 2023-11-27 |
| Nonfinancial corp equity / GDP (%) - Buffett-style, percentile only | 2026-04-01 | 255.046 | 255.046 | CRIT | 100.0 | 1947-10-01 |
| USDJPY 3m % change (negative = yen carry unwind) | 2026-11-20 | 158.76 | -0.057 | ok | 71.0 | 1971-01-04 |
| VIX | 2026-11-24 | 26.36 | 26.36 | WARN | 86.3 | 1990-01-02 |
| MOVE index (rates vol) | 2026-11-25 | 97.54 | 97.54 | ok | 70.2* | 2016-11-28 |
| VIX3M (info, not scored) | 2026-11-24 | 25.47 | 25.47 | n/a | 78.3 | 2007-12-04 |
| VIX / VIX3M (>1.0 = inverted, acute stress) | 2026-11-24 | 1.035 | 1.035 | WARN | 94.6 | 2007-12-04 |

* percentile covers under 10 years of history (HY/IG/CCC/EM HY from 2023, subprime auto file): not a comparison with 2008 or 2020.

_Thresholds are judgment anchors, not backtested. This is a condition read, not a forecast or a timing signal._
