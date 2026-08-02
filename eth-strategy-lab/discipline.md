# Operating Discipline - ETH Walk-Forward Trend Overlay

Final operating rules for the eth-strategy-lab system. Every number below is
from the project's own computed outputs (results/*.csv, evaluation.md,
multi_asset_eval.md). ASCII only.

## (a) What the validated system is

- The system is the mechanical walk-forward SMA trend overlay: every 182
  days, re-select n from {50, 100, 200} by best trailing 730-day Sharpe,
  apply out of sample, 0.1% taker fee, next-day execution. Never a frozen
  lookback: in the 2026-02 -> 2026-08 holdout tail, frozen n=50 lost -1.2%,
  frozen n=100 lost -13.9% (worse than holding's -11.6%), frozen n=200 sat
  flat at 0.0%. Only re-selection navigated that.
- It is drawdown insurance with a negative premium in normal times, not a
  return machine. Pooled across 10 assets and 126 OOS windows: mean window
  Sharpe 0.217 (overlay) vs 0.492 (hold); the overlay wins only 32.5% of
  windows; paired t = -3.87. The edge is concentrated in a few bear-market
  avoidances.
- Cross-asset evidence: 6/10 assets beat hold on both Sharpe and maxDD;
  ETH is on the favorable side of that distribution. Extended BTC history
  (2014+, 20 windows) supports it: overlay Sharpe 1.183 vs hold 1.038.
- Portfolio level: equal-weight basket overlay maxDD -31.2% vs hold -62.9%
  at Sharpe 0.644 vs 0.596 (2022-08 -> 2026-08). The reliable benefit is
  drawdown reduction.
- ETH headline (stitched OOS 2019-08 -> 2026-08): Sharpe 1.007 vs hold
  0.819, maxDD -64.4% vs -79.3%, CAGR 50.0% vs 39.1%, net of fees.
- Statistical honesty checks: DSR 0.985 with 7 documented trials
  (benchmark max Sharpe under null 0.154 annualized); PBO 0.243 via CSCV
  (6 configs, S=8, 70 splits) - real but moderate overfitting risk; the
  execution-timing audit (open t+1 fills) moves overlay Sharpe by only
  -0.001 and sma_50 by +0.002, so results are not a close-fill artifact.
- Cost tolerance: break-even extra slippage is 0.96% per side - the edge
  survives realistic execution costs with a wide margin. Flat-leg yield
  helps if available: 4% APR on cash lifts overlay Sharpe 1.007 -> 1.039;
  3.5% staking lifts hold Sharpe 0.672 -> 0.712.

## (b) Named pre-deployment decisions (non-computable risks)

The operator must decide each of these explicitly, in writing, before any
capital is deployed. The backtest cannot answer them.

- DECISION-TAXES: the overlay trades about 82 times per 7 years on ETH
  (about 12 round trips/year). Decide how spot crypto gains are taxed in
  your jurisdiction per trade vs buy-and-hold's single unrealized gain, and
  whether post-tax the overlay's insurance premium is still worth paying.
  If your jurisdiction taxes every disposal at full income rates, the
  overlay's net edge may not survive even though gross Sharpe does.
- DECISION-CUSTODY: CEX earn/staking (up to 4-8% on the flat leg, 3.5%
  staking on the held leg per the yield scenarios) requires keeping coins
  and stablecoins on an exchange - counterparty risk (FTX precedent).
  Self-custody removes that risk but forfeits the yield and complicates
  same-day execution. Decide: full CEX, full self-custody, or split, and
  cap the CEX share you are willing to lose entirely.
- DECISION-STABLECOIN-DEPEG: the flat leg sits in USDT/USD stablecoins
  about 47% of days. A depeg turns the "safe" leg into the loss leg.
  Decide which stablecoin(s) the flat leg holds and the maximum share in
  any single issuer.
- DECISION-BEHAVIORAL-ADHERENCE: the overlay loses the average window
  (only 32.5-43.7% of pooled windows are wins/positive) and spends long
  stretches flat while price rises. Decide now, in writing, that you will
  not override signals during whipsaw boredom. Three consecutive
  discretionary overrides trigger the kill-switch below.

## (c) Position sizing rule (from results/kelly.csv)

- Full Kelly on stitched OOS overlay returns: mean/variance 1.765,
  empirical 1.485. Rejected: Monte Carlo at those fractions gives 3-year
  risk of ruin about 11% and p99 maxDD about 98%.
- Half Kelly 0.743: 3y ruin 2.1%, p99 maxDD 79.4% - only for operators who
  genuinely accept a 1-in-5 chance of a >63% drawdown (3y p50 is 42.9%).
- Vince optimal-f: 0.665. Quarter Kelly: 0.371.
- RULE: deploy at most 0.37 of account equity (quarter empirical Kelly,
  the largest fraction with MC 3-year ruin <= 1% and p99 maxDD <= 60%).
  On a $100 account: at most $37 deployed, $63 cash. Recompute the
  fraction from refreshed OOS returns after each 182-day window; never
  raise it because of a good quarter.
- Practical note: at $100 scale, exchange minimum order sizes and the
  0.1% fee on small tickets dominate; the paper gate (e) exists partly to
  measure whether live fills at this size track the model at all.

## (d) Kill-switch criteria (any one halts live trading)

1. run_daily.py exits non-zero (fetch failure or drift check mismatch) -
   halt until root-caused; the drift check compares signal_today.py output
   with an independent engine recomputation on the same refreshed data.
2. Measured live slippage per side persistently above 0.50% (about half
   the 0.96% break-even) over 10 consecutive trades - the modeled edge no
   longer covers execution.
3. Live paper/live cumulative return diverges from the engine's
   recomputation on identical data by more than 5 percentage points over
   any rolling 60 days - the model no longer describes reality.
4. Three consecutive discretionary signal overrides (violating
   DECISION-BEHAVIORAL-ADHERENCE) - halt and restart the paper gate.
5. Account drawdown exceeds the Monte Carlo 3-year p99 for the deployed
   fraction (60% at 0.37 fraction) - the scenario the sizing rule was
   built to cap has been exceeded; stop, do not "double down".

## (e) Paper-trading gate

- 4-8 weeks (28-56 consecutive UTC days) of run_daily.py logging, every
  day exit 0, zero drift incidents, before any real capital. The ledger
  (paper_ledger.csv) is the evidence.
- During the gate, record the actual quoted spread/slippage you would
  have paid on each signal change to feed kill-switch criterion 2.
- After a clean gate: start live at 0.25 fraction ($25 of $100), scale to
  the 0.37 rule only after 4 further clean weeks, and never above 0.37.
- Any kill-switch event during live trading returns the system to the
  paper gate for a full new 4-8 week cycle.
