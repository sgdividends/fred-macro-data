# Crisis dashboard - 2026-11-03 20:14 UTC

**State: FRAGILE, no trigger yet (late-cycle risk, not a crisis)**

Fragility (worst fragility block or valuation input) 2 | Trigger index (average) 0.11 (0 normal, 1 warn, 2 critical)

Fast trigger lines (any WARN or worse flags a trigger):

- St. Louis Fed stress index: -0.584 - ok
- Chicago Fed NFCI: -0.487 - ok
- VIX: 21.15 - ok
- HY OAS 3m change (pp): 0.58 - ok
- SLOOS C&I net tightening, change vs prior quarter (pp): 1.7 - ok
- SLOOS credit card net tightening, change vs prior quarter (pp): -2.7 - ok
- VIX / VIX3M (>1.0 = inverted, acute stress): 0.979 - ok
- MOVE index (rates vol): 100.36 - ok

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
| SLOOS net % tightening, credit cards | 2026-10-01 | 4.0 | 4.0 | ok | 47.6 | 1996-01-01 |
| SLOOS net % tightening C&I, large/mid firms | 2026-10-01 | 1.7 | 1.7 | ok | 53.1 | 1990-04-01 |
| Fitch subprime auto ABS 60+ delinquency (%) | 2026-07-31 | 6.13 | 6.13 | WARN | 66.7* | 2026-01-31 |
| Moody's Baa minus 10y (%) | 2026-10-30 | 1.53 | 1.53 | ok | 7.8 | 1986-01-02 |
| CCC OAS (%) | 2026-11-02 | 13.19 | 13.19 | WARN | 99.2* | 2023-08-01 |
| HY OAS (%) | 2026-11-02 | 3.43 | 3.43 | ok | 79.9* | 2023-07-24 |
| HY OAS 3m change (pp) | 2026-11-02 | 3.43 | 0.58 | ok | 79.9* | 2023-07-24 |
| IG OAS (%) | 2026-11-02 | 0.94 | 0.94 | ok | 70.4* | 2023-07-24 |
| SLOOS credit card net tightening, change vs prior quarter (pp) | 2026-10-01 | 4.0 | -2.7 | ok | 47.6 | 1996-01-01 |
| SLOOS C&I net tightening, change vs prior quarter (pp) | 2026-10-01 | 1.7 | 1.7 | ok | 53.1 | 1990-04-01 |
| Chicago Fed NFCI | 2026-10-23 | -0.487 | -0.487 | ok | 41.0 | 1971-01-08 |
| St. Louis Fed stress index | 2026-10-23 | -0.584 | -0.584 | ok | 22.8 | 1993-12-31 |
| 10y-3m spread (pp) | 2026-11-02 | 0.7 | 0.7 | ok | 28.3 | 1982-01-04 |
| Initial claims 4wk avg, 3m % change | 2026-10-24 | 196750.0 | -5.409 | ok | 2.0 | 1967-01-28 |
| Sahm rule indicator | 2026-09-01 | 0.0 | 0.0 | ok | 43.7 | 1959-12-01 |
| FINRA margin debt y/y (%) | 2026-09-01 | 1.48 | 31.4 | WARN | 82.6 | 1998-01-01 |
| Broad USD index 3m % change | 2026-10-30 | 121.666 | 1.663 | ok | 90.9 | 2006-01-02 |
| EM HY corporate OAS (%) | 2026-11-02 | 3.93 | 3.93 | ok | 73.0* | 2023-11-06 |
| Nonfinancial corp equity / GDP (%) - Buffett-style, percentile only | 2026-04-01 | 255.046 | 255.046 | CRIT | 100.0 | 1947-10-01 |
| USDJPY 3m % change (negative = yen carry unwind) | 2026-10-30 | 157.47 | -1.254 | ok | 70.3 | 1971-01-04 |
| VIX | 2026-11-02 | 21.15 | 21.15 | ok | 68.6 | 1990-01-02 |
| MOVE index (rates vol) | 2026-11-02 | 100.36 | 100.36 | ok | 72.8 | 2016-11-03 |
| VIX3M (info, not scored) | 2026-11-02 | 21.6 | 21.6 | n/a | 63.2 | 2007-12-04 |
| VIX / VIX3M (>1.0 = inverted, acute stress) | 2026-11-02 | 0.979 | 0.979 | ok | 85.4 | 2007-12-04 |

* percentile covers under 10 years of history (HY/IG/CCC/EM HY from 2023, subprime auto file): not a comparison with 2008 or 2020.

_Thresholds are judgment anchors, not backtested. This is a condition read, not a forecast or a timing signal._
