# Cross-Market Confidence Testing - Walk-Forward SMA Trend Overlay

Question: does the **same mechanical overlay** that beat ETH buy-and-hold
(train 730d / test 182d / step 182d, pick best-train-Sharpe n from {50,100,200},
0.1% taker fee, next-day execution) generalize across many assets and more
history? Short answer: **it complicates the ETH-only story.** Details below;
all numbers from actual runs (`results/*.csv`).

## Data

- Binance basket, 10/10 symbols fetched (public klines, no key), validated
  (monotonic, no dupes, no NaN closes, completed candles only):

| symbol | rows | range |
|---|---:|---|
| BTCUSDT | 3272 | 2017-08-17 -> 2026-08-01 |
| ETHUSDT | 3272 | 2017-08-17 -> 2026-08-01 |
| BNBUSDT | 3191 | 2017-11-06 -> 2026-08-01 |
| XRPUSDT | 3012 | 2018-05-04 -> 2026-08-01 |
| LTCUSDT | 3154 | 2017-12-13 -> 2026-08-01 |
| ADAUSDT | 3029 | 2018-04-17 -> 2026-08-01 |
| DOGEUSDT | 2585 | 2019-07-05 -> 2026-08-01 |
| SOLUSDT | 2182 | 2020-08-11 -> 2026-08-01 |
| LINKUSDT | 2755 | 2019-01-16 -> 2026-08-01 |
| TRXUSDT | 2974 | 2018-06-11 -> 2026-08-01 |

- Extended BTC-USD: **Yahoo Finance chart API worked** (CryptoCompare fallback
  not needed) - 4,337 rows, **2014-09-17 -> 2026-08-01**, adding the 2014-15
  bear and 2015-17 bull to the training/early-test regimes.
  (`data/btc_usd_yahoo_daily.csv`)

## 1. Per-asset: walk-forward overlay vs hold (same OOS span per asset)

| asset | OOS span | windows | overlay Sharpe | hold Sharpe | band Sharpe | overlay maxDD | hold maxDD | band maxDD | overlay CAGR | hold CAGR | overlay fees % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTCUSDT | 2019-08->2026-08 | 14 | **1.048** | 0.739 | 0.741 | **-58.0** | -76.6 | -49.2 | **42.1** | 29.9 | 78.0 |
| ETHUSDT | 2019-08->2026-08 | 14 | **1.007** | 0.819 | 0.825 | **-64.4** | -79.3 | -51.7 | **50.0** | 39.1 | 54.4 |
| BNBUSDT | 2019-11->2026-08 | 14 | **1.213** | 1.001 | 1.000 | **-40.7** | -70.9 | -43.0 | **80.2** | 63.9 | 338.8 |
| XRPUSDT | 2020-05->2026-08 | 13 | 0.476 | **0.731** | 0.727 | -83.4 | **-83.2** | -51.4 | 7.7 | **28.7** | 14.3 |
| LTCUSDT | 2019-12->2026-08 | 14 | 0.244 | **0.441** | 0.421 | **-81.2** | -89.4 | -60.0 | -5.3 | **-0.1** | 14.5 |
| ADAUSDT | 2020-04->2026-08 | 13 | **0.785** | 0.735 | 0.740 | **-79.4** | -95.2 | -67.2 | **36.4** | 29.4 | 123.2 |
| DOGEUSDT | 2021-07->2026-08 | 11 | **0.316** | 0.176 | 0.192 | **-70.4** | -85.2 | -56.3 | **-0.1** | -22.2 | 8.1 |
| SOLUSDT | 2022-08->2026-08 | 8 | **0.762** | 0.598 | 0.621 | **-59.0** | -79.3 | -50.6 | **33.3** | 14.0 | 27.4 |
| LINKUSDT | 2021-01->2026-08 | 12 | -0.046 | **0.314** | 0.307 | -91.4 | **-90.2** | -57.5 | -20.6 | **-15.7** | 5.2 |
| TRXUSDT | 2020-06->2026-08 | 13 | 0.687 | **0.955** | 0.959 | -75.3 | **-69.5** | -40.0 | 30.7 | **61.0** | 33.9 |

**Headline: the overlay beats hold on Sharpe in 6/10 assets, on maxDD in 7/10,
on BOTH in 6/10 (60%).** Wins are concentrated in the large, liquid, strongly
trending assets (BTC, ETH, BNB, SOL, ADA; DOGE barely). Failures (XRP, LTC,
LINK, TRX) are mostly assets whose returns came in violent squeeze rallies that
a daily-close trend filter cannot capture - it exits after the crash and
re-enters after the recovery, repeatedly.

Note the band-rebalance column: band Sharpe ~ hold Sharpe in every asset (as
expected - it is de-risked holding, not alpha), with uniformly better maxDD.

## 2. Extended BTC history (Yahoo, 2014-09 -> 2026-08)

- **Buy & hold, full span:** +13,609%, CAGR 51.4%, vol 66.4%, **Sharpe 0.959**,
  maxDD -83.4%.
- **Walk-forward overlay, OOS 2016-09 -> 2026-08 (20 windows):** Sharpe **1.183**
  vs hold same-span **1.038**; CAGR 61.0% vs 60.0%; maxDD -79.4% vs -83.4%.
  n-selection counts: 50 -> 10x, 100 -> 5x, 200 -> 5x.
- The pre-2017 regimes behave like the post-2017 ones: the 2016-17 bull windows
  are big overlay wins (test Sharpes 2.48, 2.53), the 2018 bear windows are
  small losses instead of catastrophes (-19.3%, -8.2% while hold lost far
  more), and choppy 2019-20 and 2025-26 windows are flat-to-negative. The
  pattern is regime-driven, not period-specific - mildly supportive.
- Caveat: cumulative fees 785% of initial over the decade (145 trades against a
  ~110x compounded equity) - the fee model matters more than ever on this span.

## 3. Pooled OOS window stats (126 windows, basket only)

| statistic | overlay | hold |
|---|---:|---:|
| mean per-window test Sharpe | **0.217** | **0.492** |
| % windows with positive return | 43.7% | - |
| % windows where overlay beats hold | 32.5% | - |
| paired t-stat (overlay - hold), 126 pairs | **-3.87** | - |

**This is the uncomfortable number.** Per 6-month window, the overlay
underperforms hold on average, significantly (t = -3.9). It wins only ~1/3 of
windows. Its long-run edge in 6/10 assets comes entirely from a *few*
high-impact windows - the 2018 and 2022 bear avoidances - which compound
decisively in the stitched equity curve and show up as maxDD reduction, while
the typical window is a slow bleed of whipsaw fees and missed rallies.
Honest interpretation: **the overlay is a drawdown-insurance mechanism with a
negative premium in normal times, not a consistent return enhancer.**

Correlation caveat, as required: these 126 windows are across 10 crypto assets
that are highly cross-correlated (same macro regimes, same calendar windows
overlap heavily). Windows are NOT independent; the effective sample size is far
smaller than 126 - plausibly closer to the number of distinct 6-month calendar
periods (~14) than to the raw count. The t-stat is reported for scale, not as a
literal 126-df test; the sign and rough magnitude are the takeaway, not the
p-value.

## 4. Equal-weight portfolio (common span 2022-08-12 -> 2026-08-01, 10 assets)

Daily-rebalanced equal-weight basket, overlay applied per-asset vs plain hold:

| portfolio | total ret % | CAGR % | ann vol % | Sharpe | Sortino | maxDD % | Calmar |
|---|---:|---:|---:|---:|---:|---:|---:|
| EW overlay | 89.9 | 17.53 | 34.2 | **0.644** | 0.914 | **-31.2** | 0.562 |
| EW hold | 102.0 | 19.38 | 57.9 | 0.596 | 0.854 | -62.9 | 0.308 |

At portfolio level the overlay's edge **survives and clarifies**: slightly
better Sharpe, slightly lower CAGR, and - the real prize - **half the maximum
drawdown (-31% vs -63%)** at ~60% of the volatility. Diversification smooths
the per-asset whipsaw noise that dominates individual coin results. This is the
strongest cross-asset evidence in the overlay's favor, and it is about risk
reduction, not return.

## 5. Confidence verdict - does cross-asset evidence strengthen, weaken, or
complicate the ETH-only conclusion?

**It complicates it, and on balance weakens the return claim while
strengthening the risk claim.**

- **Weakened:** "the overlay beats hold" is not a universal crypto truth. 60%
  of assets on Sharpe+maxDD; the average OOS window is significantly *worse*
  than hold; four assets (XRP, LTC, LINK, TRX) would have been better held.
  ETH was on the favorable side of the distribution - picking it was partly
  luck of asset choice. The edge is regime- and asset-specific, not mechanical.
- **Strengthened:** BTC with 12 years and two extra regimes still shows the
  overlay ahead OOS (Sharpe 1.18 vs 1.04), and the equal-weight portfolio shows
  the benefit that survives diversification is drawdown/vol reduction at
  comparable-or-better Sharpe. As **insurance**, the overlay works across
  assets; as **alpha**, it does not.
- **Is "deploy the overlay on ETH" now better or worse justified?** Slightly
  worse justified *as a return strategy* (ETH's clean result does not
  generalize to the average asset or the average window), but still justified
  *as a risk-management overlay on a large, trending, liquid asset* - BTC and
  ETH are precisely the asset class where it worked, and the portfolio-level
  evidence shows the drawdown benefit is real and diversifiable. The honest
  deployment statement narrows to: "expect long flat/choppy stretches of small
  losses and missed rallies in exchange for avoiding the -80% to -95% tails."

**Biases and caveats:**
- *Survivorship bias:* we only test coins that survived to 2026 on Binance.
  Delisted/dead 2017-era coins are absent; including them would likely hurt
  hold more than the overlay (dead coins trend to zero, and the overlay exits
  downtrends), so our basket probably *understates* the overlay's relative
  edge - but this is untestable here, so treat the 60% win rate as neither
  floor nor ceiling.
- *Correlation:* pooled windows are not independent; effective N ~ number of
  distinct calendar periods (~14-20), not 126. All pooled significance claims
  are soft.
- *Data heterogeneity:* Yahoo BTC-USD (aggregated exchange prices) vs Binance
  USDT pairs (stablecoin quote) - close but not identical series.
- *Model limits:* fees but no slippage/spread/taxes; daily-close execution;
  one strategy family with 3 parameters.

## Files

- `fetch_multi.py`, `multi_asset.py` (new); `fetch_data.py` (generalized:
  `symbol` param on `fetch_binance`, `min_rows` param on `validate`)
- `data/{10 symbols}_daily.csv`, `data/btc_usd_yahoo_daily.csv`,
  `data/fetch_multi_meta.json`
- `results/multi_asset_table.csv`, `results/pooled_window_stats.csv`,
  `results/portfolio_ew.csv`, `results/walk_forward_btc_yahoo.csv`
