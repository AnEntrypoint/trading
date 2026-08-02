# ETH/USD Daily Strategy Lab - Decision Report

> **Update (2026-08):** the walk-forward has since been extended through the
> final holdout tail (OOS now runs to 2026-08-01, 14 windows). See
> `evaluation.md` for the consolidated, most current evaluation - its verdict
> supersedes the one below where they differ.

Zero-capital research pipeline. No real money, no API keys, free public data only.
All results net of a 0.1% taker fee on traded notional, computed on daily closes
with next-day execution (no lookahead). Flat earns 0%.

## Data

- **Source used: Binance public klines** (`api.binance.com`, ETHUSDT, 1d). First-choice
  source succeeded; Kraken and CoinGecko fallbacks were not needed. (CoinGecko was
  later found to return HTTP 401 for unauthenticated `days=max` requests.)
- **Range: 2017-08-17 -> 2026-08-01** - 3,272 completed daily candles
  (today's still-forming candle is always excluded).
- Validation: monotonic dates, no duplicate dates, no NaN closes, >2000 rows. Passed.

## Full-period results (2017-08-17 -> 2026-08-01)

| strategy | total ret % | CAGR % | ann vol % | Sharpe | Sortino | maxDD % | Calmar | trades | fees % init | % days invested |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| buy_hold | 510.3 | 22.39 | 86.7 | 0.672 | 0.979 | -94.0 | 0.238 | 1 | 0.10 | 100.0 |
| sma_trend_50 | 4427.2 | 53.09 | 59.3 | 1.014 | 1.551 | -64.4 | 0.824 | 173 | 246.38 | 50.0 |
| sma_trend_100 | 1296.8 | 34.25 | 61.6 | 0.795 | 1.151 | -74.5 | 0.460 | 118 | 110.72 | 51.0 |
| sma_trend_200 | 832.9 | 28.33 | 57.8 | 0.729 | 1.052 | -73.7 | 0.385 | 54 | 23.13 | 47.3 |
| vol_target_trend | 1366.8 | 34.98 | 43.8 | 0.903 | 1.361 | -58.7 | 0.596 | 1303 | 118.88 | 51.0 |
| rebalance_50_50_daily | 477.9 | 21.65 | 43.3 | 0.666 | 0.969 | -72.1 | 0.300 | 3271 | 9.43 | 100.0 |
| rebalance_50_50_band | 541.9 | 23.08 | 43.4 | 0.692 | 1.014 | -71.2 | 0.324 | 122 | 2.73 | 100.0 |

(Equity curves: `equity_curves.png`. "fees % init" = cumulative fees paid as % of
initial capital; it grows with account equity, which is why the high-turnover
trend variants show triple-digit lifetime figures.)

## Walk-forward validation (SMA family)

Rolling train 730d / test 182d / step 182d; in each window the n in {50, 100, 200}
with the best **train** Sharpe is applied out of sample. 13 windows.

| train | test | Sharpe n=50 | n=100 | n=200 | picked | test Sharpe | test ret % |
|---|---|---:|---:|---:|---|---:|---:|
| 2017-08-18->2019-08-17 | 2019-08-18->2020-02-15 | 0.979 | 0.989 | -0.277 | 100 | 2.690 | 52.0 |
| 2018-02-16->2020-02-15 | 2020-02-16->2020-08-15 | 0.699 | 0.902 | 0.076 | 100 | 0.209 | -14.9 |
| 2018-08-17->2020-08-15 | 2020-08-16->2021-02-13 | 1.063 | 0.971 | 0.553 | 50 | 3.021 | 241.3 |
| 2019-02-15->2021-02-13 | 2021-02-14->2021-08-14 | 2.079 | 1.734 | 1.487 | 50 | 1.325 | 44.6 |
| 2019-08-16->2021-08-14 | 2021-08-15->2022-02-12 | 1.835 | 1.421 | 1.562 | 50 | -0.388 | -18.1 |
| 2020-02-14->2022-02-12 | 2022-02-13->2022-08-13 | 1.575 | 1.155 | 1.353 | 50 | 0.919 | 16.4 |
| 2020-08-14->2022-08-13 | 2022-08-14->2023-02-11 | 1.438 | 1.235 | 1.491 | 200 | 0.803 | 8.6 |
| 2021-02-12->2023-02-11 | 2023-02-12->2023-08-12 | 0.376 | 0.066 | 0.668 | 200 | 1.026 | 20.2 |
| 2021-08-13->2023-08-12 | 2023-08-13->2024-02-10 | -0.049 | -0.122 | 0.535 | 200 | 1.285 | 25.7 |
| 2022-02-11->2024-02-10 | 2024-02-11->2024-08-10 | 0.423 | 0.075 | 0.849 | 200 | 0.916 | 20.7 |
| 2022-08-12->2024-08-10 | 2024-08-11->2025-02-08 | 0.404 | 0.199 | 0.977 | 200 | 0.091 | -3.3 |
| 2023-02-10->2025-02-08 | 2025-02-09->2025-08-09 | 0.665 | 0.484 | 0.812 | 200 | 3.284 | 62.1 |
| 2023-08-11->2025-08-09 | 2025-08-10->2026-02-07 | 1.516 | 1.200 | 1.158 | 50 | -0.315 | -10.1 |

**n-selection counts:** n=50 picked 5x, n=100 picked 2x, n=200 picked 6x.
No single lookback dominates - the full-period "winner" (n=50) is not a stable
choice, which is exactly what the walk-forward is for.

**Stitched out-of-sample curve (2019-08-18 -> 2026-02-07), vs buy-and-hold over
the identical window:**

| strategy | total ret % | CAGR % | ann vol % | Sharpe | Sortino | maxDD % | Calmar | trades | fees % init | % days invested |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sma_walkforward_oos | 1597.9 | 54.86 | 58.4 | 1.052 | 1.530 | -64.4 | 0.852 | 77 | 46.37 | 53.8 |
| buy_hold (same window) | 1024.6 | 45.32 | 82.2 | 0.872 | 1.281 | -79.3 | 0.571 | 0 | 0.00 | 100.0 |

OOS Sharpe (1.052) sits between the per-window train Sharpes (avg ~ 1.0) and does
not wildly exceed the best full-period in-sample Sharpe (1.014) - no obvious
overfitting signature, though the sample is small.

## Fee-drag analysis (full period, net vs zero-fee)

| strategy | net CAGR % | gross CAGR % | CAGR drag | net Sharpe | gross Sharpe |
|---|---:|---:|---:|---:|---:|
| buy_hold | 22.39 | 22.40 | 0.01 | 0.672 | 0.672 |
| sma_trend_50 | 53.09 | 56.08 | 2.99 | 1.014 | 1.047 |
| sma_trend_100 | 34.25 | 36.02 | 1.77 | 0.795 | 0.816 |
| sma_trend_200 | 28.33 | 29.10 | 0.77 | 0.729 | 0.739 |
| vol_target_trend | 34.98 | 36.79 | 1.81 | 0.903 | 0.934 |
| rebalance_50_50_daily | 21.65 | 21.99 | 0.34 | 0.666 | 0.672 |
| rebalance_50_50_band | 23.08 | 23.18 | 0.10 | 0.692 | 0.694 |

- Fees are a real but not fatal drag on trend strategies (~0.8-3.0 CAGR points);
  the edge survives the 0.1% taker fee. It would **not** obviously survive much
  worse execution (slippage + spread on top of taker fees, especially for the
  173-trade SMA(50) variant).
- Band rebalancing does its job: 122 rebalances / 2.73% lifetime fees vs daily's
  3,271 / 9.43%, and ends with *higher* CAGR (23.08 vs 21.65). Rebalancing daily
  is pure fee leakage; the band captures the same premium cheaper.
- 50/50 rebalancing (either mode) has Sharpe ~ buy-and-hold (0.69 vs 0.67) at
  roughly half the volatility. It is de-risked holding plus a small rebalancing
  premium - not an alpha source.

## Verdict

**Does anything beat buy-and-hold risk-adjusted, out of sample, after fees?**
Yes, narrowly and honestly: the walk-forward SMA trend overlay beats same-window
buy-and-hold on Sharpe (1.05 vs 0.87), maxDD (-64% vs -79%), and CAGR (54.9% vs
45.3%), net of fees, with the parameter re-selected every window rather than
cherry-picked. `vol_target_trend` is the best full-period risk-adjusted variant
(Sharpe 0.903, maxDD -58.7%) but was not walk-forwarded - its two parameters
(60% target vol, 30d window) are a-priori canonical choices, not tuned here,
still that is one researcher-degree-of-freedom caveat.

**Would I deploy it with real money?** Cautiously, and not at full size:

- The trend edge is real but **concentrated**: most of it comes from sidestepping
  the 2018, 2021-22 and 2025-26 bear legs. In choppy regimes the strategy
  bleeds (several OOS windows are negative). If ETH's future has fewer clean
  multi-month trends, the edge shrinks.
- **-64% max drawdown, even for the trend overlay, is beyond most investors'
  tolerance.** The vol-target variant's -59% at ~44% vol is the more livable
  profile; raw buy-and-hold's -94% is a genuine portfolio-killer.
- Execution reality: 0.1% taker is the *best case*; slippage and spread widen
  it, and taxes on 100+ round trips can exceed fees. These were not modeled.
- Multiple-testing burden is low (3 lookbacks, a handful of canonical strategy
  specs - deflated-Sharpe-wise this is a mild search), but 13 OOS windows is a
  small sample and one asset in one market regime. Treat Sharpe ~ 1.0 as the
  optimistic end of the plausible range, not the expectation.

**Bottom line:** for a long-term ETH allocation, a trend-filtered or
vol-targeted overlay is defensible and beats naive holding on the evidence here;
fixed 50/50 band rebalancing is the low-effort alternative that halves risk at
no Sharpe cost. If forced to a single decision between "blind hold everything"
and "deploy the walk-forwarded trend overlay with real money," the data favors
the overlay - but sized so that a -60% drawdown is survivable, with realistic
execution costs re-checked before going live. For most people, plain holding
(ideally band-rebalanced to a fixed weight) remains the more robust decision.

## Limitations

- Single asset, single venue (Binance ETHUSDT ~ ETH/USD), 2017->2026 - includes
  two full crypto cycles; still one asset's history.
- Daily-close execution assumption ignores intraday fills; fees but not
  slippage/spread/taxes modeled; cash earns 0%.
- Walk-forward uses only 13 windows; n-selection instability (5/2/6) warns
  against trusting any fixed lookback.
- CoinGecko fallback currently requires an API key (HTTP 401); Binance and
  Kraken remain keyless.
