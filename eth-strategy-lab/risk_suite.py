"""risk_suite.py - deployment risk analysis for the walk-forward SMA overlay.

Implements, on the ETH stitched out-of-sample overlay and benchmarks:
  1. slippage sensitivity (+0.00/+0.05/+0.10/+0.20% per side on top of the
     0.1% fee) for all strategies and the overlay, with the overlay's
     break-even slippage vs buy-and-hold
  2. cash-yield scenarios for the flat leg and staking yield for buy_hold
  3. Deflated Sharpe Ratio (Bailey and Lopez de Prado)
  4. PBO overfitting probability via combinatorially symmetric CV (S=8)
  5. stationary-bootstrap Monte Carlo drawdowns and risk of ruin
  6. Kelly sizing (mean/variance, empirical, half/quarter, Vince optimal-f)
  7. execution-timing audit: fills at open[t+1] vs close-to-close

Outputs: results/slippage_sensitivity.csv, results/yield_scenarios.csv,
results/risk_suite.csv, results/pbo.csv, results/monte_carlo.csv,
results/kelly.csv, results/execution_timing.csv.
"""

import itertools
from math import e, log, sqrt
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

from backtest import walk_forward_sma
from strategies import (
    ANN, FEE, daily_returns, engine_frame, load_data, metrics_from_frame,
    sig_buy_hold, sig_sma_trend, sig_vol_target_trend,
    simulate_rebalance_50_50,
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
RESULTS = BASE / "results"

SLIPPAGES = [0.0, 0.0005, 0.001, 0.002]
CASH_YIELDS = [0.0, 0.02, 0.04, 0.08]
STAKING_YIELDS = [0.0, 0.035]
MC_PATHS = 10_000
MC_BLOCK = 20
MC_SEED = 42
ACCOUNT = 100.0
RUIN_LEVEL = 0.5
N_TRIALS = 7                                                                 

_norm = NormalDist()


def load_eth():
    df = load_data(DATA / "ethusdt_daily.csv")
    return df, daily_returns(df)


def overlay_stitched(df, **wf_kwargs):
    _, stitched, oos, _ = walk_forward_sma(df, **wf_kwargs)
    return stitched, oos


def oos_span(stitched):
    return stitched.index[0], stitched.index[-1]


def strategy_frames(df, ret, cost):
    return {
        "buy_hold": engine_frame(sig_buy_hold(df), ret, fee=cost),
        "sma_trend_50": engine_frame(sig_sma_trend(df, 50), ret, fee=cost),
        "sma_trend_100": engine_frame(sig_sma_trend(df, 100), ret, fee=cost),
        "sma_trend_200": engine_frame(sig_sma_trend(df, 200), ret, fee=cost),
        "vol_target_trend": engine_frame(sig_vol_target_trend(df), ret,
                                         fee=cost),
        "rebalance_50_50_band": simulate_rebalance_50_50(ret, mode="band",
                                                         fee=cost),
    }


def core_metrics(frame):
    m = metrics_from_frame(frame)
    return {"sharpe": m["sharpe"], "CAGR_pct": m["CAGR_pct"],
            "max_drawdown_pct": m["max_drawdown_pct"],
            "total_return_pct": m["total_return_pct"]}


                                                                         
def slippage_sensitivity(df, ret):
    rows = []
    overlay_sharpes, hold_sharpes = {}, {}
    for slip in SLIPPAGES:
        cost = FEE + slip
        frames = strategy_frames(df, ret, cost)
        stitched, _ = overlay_stitched(df, fee=cost)
        s0, s1 = oos_span(stitched)
        frames["walkforward_overlay"] = stitched
        hold_sharpes[slip] = metrics_from_frame(
            frames["buy_hold"].loc[s0:s1])["sharpe"]
        overlay_sharpes[slip] = metrics_from_frame(stitched)["sharpe"]
        for name, frame in frames.items():
            m = core_metrics(frame)
            rows.append({"slippage_pct": slip * 100, "cost_per_side_pct":
                         cost * 100, "strategy": name, **m})
    table = pd.DataFrame(rows).round(4)
    table.to_csv(RESULTS / "slippage_sensitivity.csv", index=False)
    print("=== row 1: slippage sensitivity (Sharpe / CAGR% / maxDD%) ===")
    pivot = table.pivot(index="strategy", columns="slippage_pct",
                        values="sharpe")
    print(pivot.round(3).to_string())

    def sharpe_gap(slip):
        st, _ = overlay_stitched(df, fee=FEE + slip)
        a, b = oos_span(st)
        ov = metrics_from_frame(st)["sharpe"]
        hd = metrics_from_frame(engine_frame(sig_buy_hold(df), ret,
                                             fee=FEE + slip).loc[a:b])["sharpe"]
        return ov - hd

    grid = np.arange(0.0, 0.0151, 0.001)
    gaps = [(s, sharpe_gap(s)) for s in grid]
    breakeven = None
    for (s0, g0), (s1, g1) in zip(gaps, gaps[1:]):
        if g0 == 0.0:
            breakeven = s0
            break
        if g0 * g1 < 0:
            breakeven = s0 - g0 * (s1 - s0) / (g1 - g0)
            break
    be_txt = (f"{breakeven * 100:.2f}%" if breakeven is not None
              else "> 1.50% (no crossing in grid)")
    print(f"overlay OOS Sharpe minus hold Sharpe, by slippage: "
          f"{[(f'{s * 100:.1f}%', round(g, 3)) for s, g in gaps]}")
    print(f"break-even slippage (overlay OOS Sharpe = hold Sharpe): {be_txt}")
    return table, breakeven


                                                                         
def yield_scenarios(df, ret):
    rows = []
    for cy in CASH_YIELDS:
        stitched, _ = overlay_stitched(df, cash_yield_apr=cy)
        m = core_metrics(stitched)
        rows.append({"strategy": "walkforward_overlay", "cash_apr_pct":
                     cy * 100, "staking_apr_pct": 0.0, **m})
        s0, s1 = oos_span(stitched)
        hold = engine_frame(sig_buy_hold(df), ret, cash_yield_apr=cy)
        mh = core_metrics(hold.loc[s0:s1])
        rows.append({"strategy": "buy_hold", "cash_apr_pct": cy * 100,
                     "staking_apr_pct": 0.0, **mh})
    for sy in STAKING_YIELDS:
        hold = engine_frame(sig_buy_hold(df), ret, asset_yield_apr=sy)
        m = core_metrics(hold)
        rows.append({"strategy": "buy_hold_staked", "cash_apr_pct": 0.0,
                     "staking_apr_pct": sy * 100, **m})
    table = pd.DataFrame(rows).round(4)
    table.to_csv(RESULTS / "yield_scenarios.csv", index=False)
    print("\n=== row 2: yield scenarios ===")
    print(table.to_string(index=False))
    return table


                                                                          
def deflated_sharpe(df, ret):
    stitched, oos = overlay_stitched(df)
    s0, s1 = oos_span(stitched)
    frames = strategy_frames(df, ret, FEE)
    frames["walkforward_overlay"] = stitched
    trial_sr = []
    for name in ["sma_trend_50", "sma_trend_100", "sma_trend_200",
                 "vol_target_trend", "rebalance_50_50_band",
                 "rebalance_50_50_daily", "walkforward_overlay"]:
        if name == "rebalance_50_50_daily":
            fr = simulate_rebalance_50_50(ret, mode="daily")
        else:
            fr = frames[name]
        r = fr["port_ret"].loc[s0:s1]
        trial_sr.append(r.mean() / r.std())
    trial_sr = np.array(trial_sr)
    v_sr = trial_sr.var(ddof=1)

    r = stitched["port_ret"]
    t = len(r)
    sr_daily = r.mean() / r.std()
    skew = r.skew()
    kurt = r.kurt() + 3.0                                                       
    gamma_em = 0.5772156649
    n = N_TRIALS
    sr_star = sqrt(v_sr) * ((1 - gamma_em) * _norm.inv_cdf(1 - 1 / n)
                            + gamma_em * _norm.inv_cdf(1 - 1 / (n * e)))
    denom = sqrt(1 - skew * sr_daily + (kurt - 1) / 4 * sr_daily ** 2)
    dsr = _norm.cdf((sr_daily - sr_star) * sqrt(t - 1) / denom)
    psr0 = _norm.cdf(sr_daily * sqrt(t - 1) / denom)

    out = pd.DataFrame([
        {"metric": "n_trials", "value": n,
         "note": "3 SMA + vol_target + 2 rebalance modes + WF overlay"},
        {"metric": "observed_oos_sharpe_ann", "value": round(
            sr_daily * sqrt(ANN), 4), "note": "stitched overlay"},
        {"metric": "benchmark_max_sharpe_ann", "value": round(
            sr_star * sqrt(ANN), 4), "note": "expected max SR under null"},
        {"metric": "dsr", "value": round(dsr, 4),
         "note": "Deflated Sharpe Ratio (probability)"},
        {"metric": "psr_vs_zero", "value": round(psr0, 4),
         "note": "raw probabilistic SR at benchmark 0"},
        {"metric": "sample_days", "value": t, "note": "OOS length"},
        {"metric": "skew", "value": round(skew, 4), "note": "OOS daily rets"},
        {"metric": "kurtosis_pearson", "value": round(kurt, 4),
         "note": "excess + 3"},
        {"metric": "trial_sr_variance", "value": round(v_sr, 8),
         "note": "daily SR variance across trials"},
    ])
    out.to_csv(RESULTS / "risk_suite.csv", index=False)
    print("\n=== row 3: Deflated Sharpe Ratio ===")
    print(out.to_string(index=False))
    return dsr


                                                                          
def pbo_overfitting(df, ret):
    configs = {
        "sma_50": engine_frame(sig_sma_trend(df, 50), ret)["port_ret"],
        "sma_100": engine_frame(sig_sma_trend(df, 100), ret)["port_ret"],
        "sma_200": engine_frame(sig_sma_trend(df, 200), ret)["port_ret"],
        "vol_target": engine_frame(sig_vol_target_trend(df), ret)["port_ret"],
        "rebal_daily": simulate_rebalance_50_50(ret, mode="daily")["port_ret"],
        "rebal_band": simulate_rebalance_50_50(ret, mode="band")["port_ret"],
    }
    rmat = pd.DataFrame(configs).dropna()
    values = rmat.to_numpy()
    names = list(rmat.columns)
    m = len(names)
    blocks = np.array_split(np.arange(len(rmat)), 8)

    def sharpes(idx):
        sub = values[idx]
        sd = sub.std(axis=0, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            sr = np.where(sd > 0, sub.mean(axis=0) / sd * sqrt(ANN), np.nan)
        return sr

    rows = []
    for combo in itertools.combinations(range(8), 4):
        tr_idx = np.concatenate([blocks[i] for i in combo])
        te_idx = np.concatenate([blocks[i] for i in range(8)
                                 if i not in combo])
        sr_is, sr_oos = sharpes(tr_idx), sharpes(te_idx)
        best = int(np.nanargmax(sr_is))
        order = np.argsort(-sr_oos, kind="stable")
        rank = int(np.where(order == best)[0][0]) + 1
        rel = rank / (m + 1)
        rows.append({"train_blocks": "-".join(str(i) for i in combo),
                     "is_best": names[best], "is_sharpe": sr_is[best],
                     "oos_sharpe": sr_oos[best], "oos_rank": rank,
                     "rel_rank": rel, "logit": log(rel / (1 - rel))})
    table = pd.DataFrame(rows).round(4)
    table.to_csv(RESULTS / "pbo.csv", index=False)
    pbo = float((table["rel_rank"] > 0.5).mean())
    print("\n=== row 4: PBO via CSCV (6 configs, S=8, 70 splits) ===")
    print(f"PBO = {pbo:.3f}  (fraction of splits where IS-best is below "
          f"median OOS)")
    print(f"logit: mean {table['logit'].mean():.3f}, median "
          f"{table['logit'].median():.3f}, p10 "
          f"{table['logit'].quantile(0.1):.3f}, p90 "
          f"{table['logit'].quantile(0.9):.3f}")
    print("IS-best counts:", table["is_best"].value_counts().to_dict())
    return pbo, table


                                                                         
def mc_paths_stats(rets, horizon, fraction, rng, n_paths=MC_PATHS,
                   mean_block=MC_BLOCK):
    t = len(rets)
    p_cont = 1.0 - 1.0 / mean_block
    idx = rng.integers(0, t, size=n_paths)
    equity = np.full(n_paths, ACCOUNT)
    peak = np.full(n_paths, ACCOUNT)
    maxdd = np.zeros(n_paths)
    for _ in range(horizon):
        equity = equity * np.maximum(1.0 + fraction * rets[idx], 1e-9)
        np.maximum(peak, equity, out=peak)
        np.minimum(maxdd, equity / peak - 1.0, out=maxdd)
        cont = rng.random(n_paths) < p_cont
        idx = np.where(cont, (idx + 1) % t, rng.integers(0, t, size=n_paths))
    terminal = equity
    dd = -maxdd
    return {"maxdd_p50": float(np.percentile(dd, 50)),
            "maxdd_p90": float(np.percentile(dd, 90)),
            "maxdd_p99": float(np.percentile(dd, 99)),
            "p_maxdd_gt50": float((dd > 0.50).mean()),
            "p_maxdd_gt80": float((dd > 0.80).mean()),
            "p_ruin": float((terminal < ACCOUNT * RUIN_LEVEL).mean()),
            "terminal_p50": float(np.percentile(terminal, 50))}


def monte_carlo(df, ret):
    stitched, _ = overlay_stitched(df)
    s0, s1 = oos_span(stitched)
    hold = engine_frame(sig_buy_hold(df), ret).loc[s0:s1]
    rng = np.random.default_rng(MC_SEED)
    rows = []
    for strat, r in [("overlay", stitched["port_ret"].to_numpy()),
                     ("buy_hold", hold["port_ret"].to_numpy())]:
        for horizon, hy in [(365, 1), (1095, 3)]:
            for frac in [0.25, 0.50, 1.00]:
                st = mc_paths_stats(r, horizon, frac, rng)
                rows.append({"strategy": strat, "horizon_years": hy,
                             "fraction": frac, **{k: round(v, 4)
                                                  for k, v in st.items()}})
    table = pd.DataFrame(rows)
    table.to_csv(RESULTS / "monte_carlo.csv", index=False)
    print("\n=== row 5: Monte Carlo (stationary bootstrap, 10k paths, "
          "block 20d, seed 42) ===")
    print(table.to_string(index=False))
    return table


                                                                           
def kelly_sizing(df, ret):
    stitched, _ = overlay_stitched(df)
    r = stitched["port_ret"].to_numpy()
    f_mv = r.mean() / r.var()

    grid = np.arange(0.0, 1.5001, 0.005)
    growth = np.array([
        np.log(1.0 + f * r).mean() if np.all(1.0 + f * r > 0) else -np.inf
        for f in grid])
    f_emp = float(grid[int(np.argmax(growth))])

    worst = abs(r.min())
    vgrid = np.arange(0.005, 1.0, 0.005)
    twr = np.array([np.prod(1.0 + f * r / worst) for f in vgrid])
    f_vince = float(vgrid[int(np.argmax(twr))])

    fractions = {
        "full_kelly_mean_var": min(f_mv, 1.5),
        "full_kelly_empirical": f_emp,
        "half_kelly_empirical": f_emp / 2,
        "quarter_kelly_empirical": f_emp / 4,
        "vince_optimal_f": f_vince,
    }
    rng = np.random.default_rng(MC_SEED + 1)
    rows = []
    for name, f in fractions.items():
        row = {"method": name, "fraction": round(f, 4)}
        for horizon, hy in [(365, "1y"), (1095, "3y")]:
            st = mc_paths_stats(r, horizon, min(f, 1.5), rng)
            row[f"mc_{hy}_maxdd_p50"] = round(st["maxdd_p50"], 4)
            row[f"mc_{hy}_maxdd_p99"] = round(st["maxdd_p99"], 4)
            row[f"mc_{hy}_ruin"] = round(st["p_ruin"], 4)
        rows.append(row)
    table = pd.DataFrame(rows)

    safe = table[(table["mc_3y_ruin"] <= 0.01)
                 & (table["mc_3y_maxdd_p99"] <= 0.60)]
    recommended = (safe["fraction"].max() if len(safe)
                   else table["fraction"].min())
    rec_row = {"method": "recommended_deployment", "fraction":
               round(float(recommended), 4)}
    table = pd.concat([table, pd.DataFrame([rec_row])], ignore_index=True)
    table.to_csv(RESULTS / "kelly.csv", index=False)
    print("\n=== row 6: Kelly sizing (stitched OOS overlay returns) ===")
    print(table.to_string(index=False))
    print(f"mean/var full Kelly: {f_mv:.3f}; empirical: {f_emp:.3f}; "
          f"Vince: {f_vince:.3f}; recommended for $100: {recommended:.2f}")
    return table, float(recommended)


                                                                       
def execution_timing(df, ret):
    open_ret = df["open"].pct_change()
    rows = []

    st_close, _ = overlay_stitched(df)
    st_open, _ = overlay_stitched(df, returns=open_ret, execution_lag=2)
    for label, frame in [("close_t+1", st_close), ("open_t+1", st_open)]:
        rows.append({"strategy": "walkforward_overlay", "fill": label,
                     **core_metrics(frame)})

    for label, rr, lag in [("close_t+1", ret, 1), ("open_t+1", open_ret, 2)]:
        fr = engine_frame(sig_sma_trend(df, 50), rr.dropna(),
                          execution_lag=lag)
        rows.append({"strategy": "sma_trend_50", "fill": label,
                     **core_metrics(fr)})

    table = pd.DataFrame(rows).round(4)
    for strat in table["strategy"].unique():
        sub = table[table["strategy"] == strat]
        base = sub[sub["fill"] == "close_t+1"].iloc[0]
        alt = sub[sub["fill"] == "open_t+1"].iloc[0]
        table.loc[table.index[(table["strategy"] == strat)
                              & (table["fill"] == "open_t+1")],
                  "sharpe_delta"] = round(alt["sharpe"] - base["sharpe"], 4)
        table.loc[table.index[(table["strategy"] == strat)
                              & (table["fill"] == "open_t+1")],
                  "cagr_delta_pct"] = round(alt["CAGR_pct"]
                                            - base["CAGR_pct"], 2)
    table.to_csv(RESULTS / "execution_timing.csv", index=False)
    print("\n=== row 7: execution timing audit (open t+1 fills vs close) ===")
    print(table.to_string(index=False))
    return table


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    df, ret = load_eth()
    print(f"ETH daily: {df.index[0].date()} -> {df.index[-1].date()}, "
          f"fee {FEE * 100:.1f}% per side base")

    _, breakeven = slippage_sensitivity(df, ret)
    yield_scenarios(df, ret)
    dsr = deflated_sharpe(df, ret)
    pbo, _ = pbo_overfitting(df, ret)
    monte_carlo(df, ret)
    _, recommended = kelly_sizing(df, ret)
    execution_timing(df, ret)

    extra = pd.DataFrame([
        {"metric": "slippage_breakeven_pct",
         "value": (round(breakeven * 100, 3) if breakeven is not None
                   else ">1.5"),
         "note": "overlay OOS Sharpe = hold Sharpe"},
        {"metric": "pbo", "value": round(pbo, 4),
         "note": "CSCV overfitting probability"},
        {"metric": "kelly_recommended_fraction", "value": recommended,
         "note": "deployment fraction of account"},
    ])
    risk_csv = RESULTS / "risk_suite.csv"
    base = pd.read_csv(risk_csv)
    pd.concat([base, extra], ignore_index=True).to_csv(risk_csv, index=False)

    print("\n=== CONSOLIDATED RISK SUITE SUMMARY ===")
    print(f"slippage break-even: {extra.iloc[0]['value']} per side")
    print(f"DSR: {dsr:.4f} | PBO: {pbo:.3f} | recommended fraction: "
          f"{recommended:.2f}")


if __name__ == "__main__":
    main()
