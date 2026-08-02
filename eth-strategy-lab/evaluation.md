# ETH/USD Strategy Lab - Consolidated Evaluation Report

Zero-capital research. All results net of 0.1% taker fee on traded notional,
daily-close signals with next-day execution (no lookahead), cash earns 0%.
Generated from the actual script outputs; raw tables in `results/*.csv`.

## (a) Data summary

- **Source:** Binance public klines (`api.binance.com`, ETHUSDT, interval 1d), no API key.
  First-choice source; Kraken/CoinGecko fallbacks not needed (CoinGecko now
  returns HTTP 401 without a demo key).
- **Range:** 2017-08-17 -> 2026-08-01 - **3,272 completed daily candles**
  (today's forming candle always excluded).
- **Validation:** monotonic dates, no duplicates, no NaN closes - passed.
- **Files:** `data/ethusdt_daily.csv`, `data/fetch_meta.json`;
  metrics in `results/metrics_full.csv`, `results/walk_forward.csv`,
  `results/walk_forward_oos_metrics.csv`, `results/holdout_tail.csv`;
  plot `equity_curves.png`; paper log `paper_ledger.csv`.

## (b) Full-period metrics (2017-08-17 -> 2026-08-01)

| strategy | total ret % | CAGR % | ann vol % | Sharpe | Sortino | maxDD % | Calmar | trades | fees % init | % days invested |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| buy_hold | 510.3 | 22.39 | 86.7 | 0.672 | 0.979 | -94.0 | 0.238 | 1 | 0.10 | 100.0 |
| sma_trend_50 | 4427.2 | 53.09 | 59.3 | 1.014 | 1.551 | -64.4 | 0.824 | 173 | 246.38 | 50.0 |
| sma_trend_100 | 1296.8 | 34.25 | 61.6 | 0.795 | 1.151 | -74.5 | 0.460 | 118 | 110.72 | 51.0 |
| sma_trend_200 | 832.9 | 28.33 | 57.8 | 0.729 | 1.052 | -73.7 | 0.385 | 54 | 23.13 | 47.3 |
| vol_target_trend | 1366.8 | 34.98 | 43.8 | 0.903 | 1.361 | -58.7 | 0.596 | 1303 | 118.88 | 51.0 |
| rebalance_50_50_daily | 477.9 | 21.65 | 43.3 | 0.666 | 0.969 | -72.1 | 0.300 | 3271 | 9.43 | 100.0 |
| rebalance_50_50_band | 541.9 | 23.08 | 43.4 | 0.692 | 1.014 | -71.2 | 0.324 | 122 | 2.73 | 100.0 |

## (c) Complete walk-forward history (train 730d / test 182d / step 182d)

Each window picks the n in {50, 100, 200} with best **train** Sharpe, applied out
of sample. The final window's test segment is the remaining tail (175 days).

| # | train | test | tr Sharpe 50 | 100 | 200 | picked | test Sharpe | test ret % |
|---|---|---|---:|---:|---:|---|---:|---:|
| 1 | 2017-08-18->2019-08-17 | 2019-08-18->2020-02-15 | 0.979 | 0.989 | -0.277 | 100 | 2.690 | 52.0 |
| 2 | 2018-02-16->2020-02-15 | 2020-02-16->2020-08-15 | 0.699 | 0.902 | 0.076 | 100 | 0.209 | -14.9 |
| 3 | 2018-08-17->2020-08-15 | 2020-08-16->2021-02-13 | 1.063 | 0.971 | 0.553 | 50 | 3.021 | 241.3 |
| 4 | 2019-02-15->2021-02-13 | 2021-02-14->2021-08-14 | 2.079 | 1.734 | 1.487 | 50 | 1.325 | 44.6 |
| 5 | 2019-08-16->2021-08-14 | 2021-08-15->2022-02-12 | 1.835 | 1.421 | 1.562 | 50 | -0.388 | -18.1 |
| 6 | 2020-02-14->2022-02-12 | 2022-02-13->2022-08-13 | 1.575 | 1.155 | 1.353 | 50 | 0.919 | 16.4 |
| 7 | 2020-08-14->2022-08-13 | 2022-08-14->2023-02-11 | 1.438 | 1.235 | 1.491 | 200 | 0.803 | 8.6 |
| 8 | 2021-02-12->2023-02-11 | 2023-02-12->2023-08-12 | 0.376 | 0.066 | 0.668 | 200 | 1.026 | 20.2 |
| 9 | 2021-08-13->2023-08-12 | 2023-08-13->2024-02-10 | -0.049 | -0.122 | 0.535 | 200 | 1.285 | 25.7 |
| 10 | 2022-02-11->2024-02-10 | 2024-02-11->2024-08-10 | 0.423 | 0.075 | 0.849 | 200 | 0.916 | 20.7 |
| 11 | 2022-08-12->2024-08-10 | 2024-08-11->2025-02-08 | 0.404 | 0.199 | 0.977 | 200 | 0.091 | -3.3 |
| 12 | 2023-02-10->2025-02-08 | 2025-02-09->2025-08-09 | 0.665 | 0.484 | 0.812 | 200 | 3.284 | 62.1 |
| 13 | 2023-08-11->2025-08-09 | 2025-08-10->2026-02-07 | 1.516 | 1.200 | 1.158 | 50 | -0.315 | -10.1 |
| 14 | 2024-02-09->2026-02-07 | 2026-02-08->2026-08-01 | 1.078 | 0.669 | 0.563 | 50 | 0.088 | -1.2 |

- **Windows:** 14 (13 full + final 175-day tail). **n-selection counts: 50 -> 6x, 100 -> 2x, 200 -> 6x.**
- **Stitched OOS curve, full span 2019-08-18 -> 2026-08-01** (net of fees):

| strategy | total ret % | CAGR % | ann vol % | Sharpe | Sortino | maxDD % | Calmar | trades | fees % init | % invested |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sma_walkforward_oos | 1576.9 | 50.00 | 57.1 | 1.007 | 1.466 | -64.4 | 0.777 | 82 | 54.44 | 53.2 |
| buy_hold (same span) | 894.1 | 39.13 | 80.7 | 0.819 | 1.203 | -79.3 | 0.493 | 0 | 0.00 | 100.0 |

## (d) Final holdout tail (2026-02-08 -> 2026-08-01, frozen strategies)

ETH fell from the ~$2,000s to $1,845 over this window (maxDD -35% for holding).
Frozen = no re-selection; positions enter the tail from the prior close's signal.

| strategy | total ret % | CAGR % | ann vol % | Sharpe | maxDD % | trades | % invested |
|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold | -11.6 | -22.81 | 54.9 | -0.197 | -35.2 | 0 | 100.0 |
| sma_trend_50 | -1.2 | -2.58 | 33.7 | 0.088 | -17.5 | 5 | 45.1 |
| sma_trend_100 | -13.9 | -27.04 | 14.6 | -2.073 | -14.1 | 6 | 18.3 |
| sma_trend_200 | 0.0 | 0.00 | 0.0 | n/a (flat all window) | 0.0 | 0 | 0.0 |
| vol_target_trend | -13.8 | -26.70 | 14.5 | -2.051 | -14.1 | 8 | 18.3 |
| rebalance_50_50_band | -4.9 | -9.92 | 27.2 | -0.242 | -18.7 | 3 | 100.0 |

**What the tail says, plainly:** the decline *rewarded* the walk-forward's
mechanical pick (n=50: -1.2% vs holding's -11.6%, near-zero Sharpe vs negative)
and fully rewarded the slowest lookback (n=200 sat out the entire drop). But it
*punished* the intermediate lookback: frozen SMA(100) - and with it
vol_target_trend, which shares the SMA(100) gate - was still long at the
breakdown and got whipsawed for -13.9%, *worse than buy-and-hold* over the
window. Trend following is not a monolithic edge; which lookback you happened to
freeze mattered more than the strategy family itself in this regime.

## (e) Current signals (last completed close 2026-08-01, ETH $1,844.94)

- **sma_trend(100): FLAT** - close 1,844.94 < SMA100 1,936.45
- **vol_target_trend: size 0.00** - 30d ann. vol 41.8% vs 60% target -> raw size
  1.00, but the trend gate is off
- **rebalance_50_50(band): ETH weight 49.8% - rebalance NOT triggered** (inside 45-55%)

Signals apply from this close to the next day's close; logged in `paper_ledger.csv`.

## (f) Final deployment verdict

**Unchanged in substance, tempered in confidence.** The extended, now-complete
out-of-sample evidence still favors the mechanical trend overlay over naive
holding: stitched OOS Sharpe 1.007 vs 0.819, maxDD -64.4% vs -79.3%, CAGR 50.0%
vs 39.1% - all net of fees, with the parameter re-picked every window. The final
holdout tail adds one more point in the overlay's favor: its rule-based pick
(n=50) lost -1.2% where holding lost -11.6%.

But the tail also demonstrates the caveats concretely:

- **Parameter fragility is real, not theoretical.** In the same 6-month window,
  n=50 lost -1.2%, n=100 lost -13.9% (worse than holding), n=200 lost nothing.
  Only the walk-forward's re-selection mechanism navigated this; any frozen
  choice was a coin flip between "saved" and "whipsawed."
- **vol_target_trend inherits the SMA(100) gate's weakness** - its elegant
  full-period stats (Sharpe 0.903, maxDD -58.7%) did not protect it in the tail
  (-13.8%). Its parameters were never walk-forwarded; treat its full-period
  numbers as in-sample.
- The absolute return of the stitched OOS strategy over the last two windows
  is negative (-10.1%, then -1.2%): in the most recent year the overlay's edge
  was *capital preservation*, not profit.
- Standing caveats remain: 14 windows is a small sample; fees but not
  slippage/spread/taxes modeled; one asset, one venue; -64% maxDD even for the
  overlay.

**Bottom line:** if deploying real money, the only version this evidence
supports is the *mechanical walk-forwarded* overlay (re-select n periodically,
never freeze it), sized so a -60% drawdown is survivable - and its current
signal is FLAT anyway. Fixed 50/50 band rebalancing remains the low-effort
alternative (half the risk, Sharpe ~ holding, trivial fees). Freezing any single
SMA lookback - including the full-period "winner" n=50 or the vol-target variant
- is not supported by the holdout evidence. For most people, hold (ideally
band-rebalanced) stays the more robust decision.

## (g) Risk-suite findings (risk_suite.py, all net of 0.1% fee)

**Slippage sensitivity** (results/slippage_sensitivity.csv): Sharpe falls
monotonically with extra per-side cost for every strategy. Overlay OOS Sharpe:
1.007 / 0.996 / 0.986 / 0.965 at +0.00/+0.05/+0.10/+0.20% per side; hold stays
0.819 (1 trade). Break-even extra slippage where overlay OOS Sharpe equals
hold's: **0.96% per side** - a wide margin over realistic execution costs.

**Yield scenarios** (results/yield_scenarios.csv): flat-leg cash yield lifts
the overlay (Sharpe 1.007 -> 1.023 / 1.039 / 1.070 and CAGR 50.0 -> 51.4 /
52.8 / 55.5 at 2/4/8% APR); no effect on hold (always invested). 3.5% staking
lifts full-period hold Sharpe 0.672 -> 0.712, CAGR 22.4% -> 26.7%.

**Deflated Sharpe** (results/risk_suite.csv): observed stitched OOS Sharpe
1.007 annualized vs benchmark expected-max-under-null 0.154, with 7 documented
trials (3 SMA lookbacks + vol_target + 2 rebalance modes + the walk-forward
overlay itself; buy_hold is the benchmark, not a trial), T=2541 days, skew
-1.09, Pearson kurtosis 32.4. **DSR = 0.985** (raw PSR vs zero 0.995; the
deflation haircut is small because the trial count is honestly low).

**PBO** (results/pbo.csv): CSCV over 6 configs (sma_50/100/200, vol_target,
rebal daily/band), S=8 blocks, 70 train/test splits: **PBO = 0.243** - in
24.3% of splits the in-sample best config lands below the OOS median. Logit
median -0.92, p10 -1.79, p90 +1.79; IS-best counts sma_50 42x, vol_target
22x, sma_200 6x. Moderate, not negligible, overfitting risk - consistent with
the "never freeze a lookback" rule.

**Monte Carlo** (results/monte_carlo.csv; stationary bootstrap, mean block
20d, 10,000 paths, seed 42, $100 account): overlay 3-year at 100% deployment:
p50/p90/p99 maxDD 54.7/76.3/89.7%, P(maxDD>50%) 59.3%, ruin 4.2%; at 37%
deployment: ruin about 0.1%, p99 maxDD about 52%. Hold 3-year at 100%: p99
maxDD 95.9%, P(maxDD>80%) 27.3%, ruin 12.0%. At matched fractions the
overlay's drawdown/ruin profile is strictly better than hold's.

**Kelly** (results/kelly.csv): full Kelly mean/variance 1.765, empirical
1.485 (3y ruin about 11% - rejected), half 0.743 (3y ruin 2.1%), quarter
0.371, Vince optimal-f 0.665. **Recommended deployment fraction 0.37** ($37
of a $100 account): largest fraction with 3y ruin <= 1% and p99 maxDD <= 60%.

**Execution-timing audit** (results/execution_timing.csv): fills at open t+1
instead of close-to-close move the overlay's Sharpe by -0.001 (CAGR -0.09pp)
and sma_50's by +0.002 (CAGR +0.21pp). The results do not depend on the
close-fill convention - no lookahead sensitivity.

## (h) Restated final deployment verdict

The risk suite mostly de-risks the earlier verdict rather than changing it.
The overlay's OOS edge survives realistic frictions (0.96% per-side break-even
slippage), is not a statistical artifact of heavy searching (DSR 0.985 at 7
honest trials; execution-timing delta about zero), and its overfitting risk
is moderate and managed by never freezing parameters (PBO 0.243). What the
suite adds is sizing discipline: the edge is drawdown insurance, and the
correct way to hold insurance is small - 0.37 of account equity (quarter
Kelly), because full Kelly carries about 11% three-year ruin and even 100%
deployment of the overlay carries 59% probability of a >50% drawdown within
3 years. So: deploy only the mechanical re-selecting overlay, at quarter
Kelly, only after the 4-8 week paper gate (discipline.md), with the
kill-switch armed. For capital beyond that fraction - or for anyone unwilling
to run the daily loop - plain holding, ideally band-rebalanced, remains the
more robust decision. None of this changes the standing caveats: single
asset class, correlated evidence, survivorship bias, no taxes modeled.
