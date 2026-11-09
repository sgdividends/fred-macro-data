# Crisis dashboard - 2026-11-09 23:06 UTC

**State: ALERT: fragile and a trigger is turning**

Fragility (worst fragility block or valuation input) 2 | Trigger index (average) 0.25 (0 normal, 1 warn, 2 critical)

Fast trigger lines (any WARN or worse flags a trigger):

- St. Louis Fed stress index: -0.522 - ok
- Chicago Fed NFCI: -0.459 - ok
- VIX: 25.64 - WARN
- HY OAS 3m change (pp): 0.71 - ok
- SLOOS C&I net tightening, change vs prior quarter (pp): 1.7 - ok
- SLOOS credit card net tightening, change vs prior quarter (pp): -2.7 - ok
- VIX / VIX3M (>1.0 = inverted, acute stress): 1.042 - WARN
- MOVE index (rates vol): 92.77 - ok

Triggers hit: VIX (WARN); VIX / VIX3M (>1.0 = inverted, acute stress) (WARN)

| Block | Role | Score | n |
|---|---|---|---|
| Credit pricing | trigger | 0.14 | 7 |
| Household / consumer debt | fragility | 0.14 | 7 |
| Market leverage | fragility | 1.0 | 1 |
| Funding and liquidity | trigger | 0.0 | 2 |
| Growth and rates | trigger | 0.0 | 3 |
| Valuation, vol, global | mixed | 0.6 | 5 |
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
| Moody's Baa minus 10y (%) | 2026-11-06 | 1.56 | 1.56 | ok | 10.3 | 1986-01-02 |
| CCC OAS (%) | 2026-11-06 | 13.17 | 13.17 | WARN | 99.0* | 2023-08-01 |
| HY OAS (%) | 2026-11-06 | 3.42 | 3.42 | ok | 79.5* | 2023-07-24 |
| HY OAS 3m change (pp) | 2026-11-06 | 3.42 | 0.71 | ok | 79.5* | 2023-07-24 |
| IG OAS (%) | 2026-11-06 | 0.93 | 0.93 | ok | 68.8* | 2023-07-24 |
| SLOOS credit card net tightening, change vs prior quarter (pp) | 2026-10-01 | 4.0 | -2.7 | ok | 47.6 | 1996-01-01 |
| SLOOS C&I net tightening, change vs prior quarter (pp) | 2026-10-01 | 1.7 | 1.7 | ok | 53.1 | 1990-04-01 |
| Chicago Fed NFCI | 2026-10-30 | -0.459 | -0.459 | ok | 43.6 | 1971-01-08 |
| St. Louis Fed stress index | 2026-10-30 | -0.522 | -0.522 | ok | 26.0 | 1993-12-31 |
| 10y-3m spread (pp) | 2026-11-09 | 0.64 | 0.64 | ok | 27.0 | 1982-01-04 |
| Initial claims 4wk avg, 3m % change | 2026-10-31 | 194750.0 | -4.182 | ok | 1.5 | 1967-01-28 |
| Sahm rule indicator | 2026-10-01 | 0.0 | 0.0 | ok | 43.8 | 1959-12-01 |
| FINRA margin debt y/y (%) | 2026-09-01 | 1.48 | 31.4 | WARN | 82.6 | 1998-01-01 |
| Broad USD index 3m % change | 2026-11-06 | 121.88 | 1.982 | ok | 91.4 | 2006-01-02 |
| EM HY corporate OAS (%) | 2026-11-06 | 3.97 | 3.97 | ok | 75.8* | 2023-11-10 |
| Nonfinancial corp equity / GDP (%) - Buffett-style, percentile only | 2026-04-01 | 255.046 | 255.046 | CRIT | 100.0 | 1947-10-01 |
| USDJPY 3m % change (negative = yen carry unwind) | 2026-11-06 | 158.23 | -0.139 | ok | 70.8 | 1971-01-04 |
| VIX | 2026-11-06 | 25.64 | 25.64 | WARN | 84.5 | 1990-01-02 |
| MOVE index (rates vol) | 2026-11-06 | 92.77 | 92.77 | ok | 66.9* | 2016-11-10 |
| VIX3M (info, not scored) | 2026-11-06 | 24.6 | 24.6 | n/a | 75.1 | 2007-12-04 |
| VIX / VIX3M (>1.0 = inverted, acute stress) | 2026-11-06 | 1.042 | 1.042 | WARN | 95.4 | 2007-12-04 |

* percentile covers under 10 years of history (HY/IG/CCC/EM HY from 2023, subprime auto file): not a comparison with 2008 or 2020.

_Thresholds are judgment anchors, not backtested. This is a condition read, not a forecast or a timing signal._
