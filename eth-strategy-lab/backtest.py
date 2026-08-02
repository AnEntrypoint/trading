"""Run full-period backtests and walk-forward validation; print metric tables.

Outputs:
  results/metrics_full.csv   - full-period metrics for every strategy
  results/walk_forward.csv   - per-window walk-forward detail (SMA family)
  equity_curves.png          - log-scale equity curves (if matplotlib present)
"""

from pathlib import Path

import numpy as np
import pandas as pd

from strategies import (
    FEE, daily_returns, engine_frame, equity_curve, load_data,
    metrics_from_frame, sig_buy_hold, sig_sma_trend, sig_vol_target_trend,
    simulate_rebalance_50_50,
)

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "data" / "ethusdt_daily.csv"
RESULTS = BASE / "results"

SMA_GRID = [50, 100, 200]
TRAIN, TEST, STEP = 730, 182, 182


def build_frames(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    ret = daily_returns(df)
    frames = {}
    frames["buy_hold"] = engine_frame(sig_buy_hold(df), ret)
    for n in SMA_GRID:
        frames[f"sma_trend_{n}"] = engine_frame(sig_sma_trend(df, n), ret)
    frames["vol_target_trend"] = engine_frame(sig_vol_target_trend(df), ret)
    frames["rebalance_50_50_daily"] = simulate_rebalance_50_50(ret, mode="daily")
    frames["rebalance_50_50_band"] = simulate_rebalance_50_50(ret, mode="band")
    return frames


def full_period_table(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = {name: metrics_from_frame(f) for name, f in frames.items()}
    table = pd.DataFrame(rows).T
    return table.round({
        "total_return_pct": 1, "CAGR_pct": 2, "ann_vol_pct": 1,
        "sharpe": 3, "sortino": 3, "max_drawdown_pct": 1, "calmar": 3,
        "fees_pct_initial": 2, "pct_days_invested": 1,
    })


def walk_forward_sma(df: pd.DataFrame, fee: float = FEE,
                     cash_yield_apr: float = 0.0, asset_yield_apr: float = 0.0,
                     returns: pd.Series | None = None,
                     execution_lag: int = 1):
    """Rolling train 730d / test 182d / step 182d over the SMA family.

    Optional overrides let risk_suite reuse the identical mechanical rule
    under different cost/yield/timing assumptions.
    """
    ret = daily_returns(df) if returns is None else returns.dropna()
    frames = {n: engine_frame(sig_sma_trend(df, n), ret, fee=fee,
                              execution_lag=execution_lag,
                              cash_yield_apr=cash_yield_apr,
                              asset_yield_apr=asset_yield_apr)
              for n in SMA_GRID}
    n_days = len(ret)
    windows = []
    stitched = []
    start = 0
    while start + TRAIN < n_days:
        tr = slice(start, start + TRAIN)
                                                                            
        te = slice(start + TRAIN, min(start + TRAIN + TEST, n_days))
        train_sharpes = {
            n: metrics_from_frame(frames[n].iloc[tr])["sharpe"] for n in SMA_GRID
        }
        best_n = max(train_sharpes, key=train_sharpes.get)
        test_frame = frames[best_n].iloc[te]
        test_metrics = metrics_from_frame(test_frame)
        windows.append({
            "train_start": ret.index[tr.start].date(),
            "train_end": ret.index[tr.stop - 1].date(),
            "test_start": ret.index[te.start].date(),
            "test_end": ret.index[te.stop - 1].date(),
            "sharpe_50": round(train_sharpes[50], 3),
            "sharpe_100": round(train_sharpes[100], 3),
            "sharpe_200": round(train_sharpes[200], 3),
            "selected_n": best_n,
            "test_sharpe": round(test_metrics["sharpe"], 3),
            "test_return_pct": round(test_metrics["total_return_pct"], 1),
        })
        stitched.append(test_frame)
        start += STEP

    wf = pd.DataFrame(windows)
    stitched_frame = pd.concat(stitched)
    oos_metrics = metrics_from_frame(stitched_frame)
    selection_counts = wf["selected_n"].value_counts().reindex(SMA_GRID, fill_value=0)
    return wf, stitched_frame, oos_metrics, selection_counts


def holdout_tail(frames: dict[str, pd.DataFrame],
                 tail_start: pd.Timestamp) -> pd.DataFrame:
    """Frozen-strategy snapshot over the final holdout tail (no re-selection).

    Positions come from the full-history frames, so each strategy enters the
    tail holding whatever its signal said at the prior close (continuity
    preserved, no restart artifact).
    """
    names = ["buy_hold", "sma_trend_50", "sma_trend_100", "sma_trend_200",
             "vol_target_trend", "rebalance_50_50_band"]
    rows = {name: metrics_from_frame(frames[name].loc[tail_start:])
            for name in names}
    return pd.DataFrame(rows).T.round({
        "total_return_pct": 1, "CAGR_pct": 2, "ann_vol_pct": 1,
        "sharpe": 3, "sortino": 3, "max_drawdown_pct": 1, "calmar": 3,
        "fees_pct_initial": 2, "pct_days_invested": 1,
    })


def save_plot(frames: dict[str, pd.DataFrame], table: pd.DataFrame,
              stitched_frame: pd.DataFrame) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available - skipping equity_curves.png")
        return
    best_sma = max(
        (n for n in SMA_GRID),
        key=lambda n: table.loc[f"sma_trend_{n}", "sharpe"],
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    for name, label in [
        ("buy_hold", "Buy & Hold"),
        (f"sma_trend_{best_sma}", f"SMA trend ({best_sma})"),
        ("vol_target_trend", "Vol-target trend"),
        ("rebalance_50_50_band", "Rebalance 50/50 (band)"),
    ]:
        ax.plot(equity_curve(frames[name]), label=label)
    ax.plot(equity_curve(stitched_frame), label="SMA walk-forward OOS",
            linestyle="--")
    ax.set_yscale("log")
    ax.set_title("ETH/USD daily strategies - equity curves (log scale, net of 0.1% fees)")
    ax.set_ylabel("Growth of $1")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = BASE / "equity_curves.png"
    fig.savefig(out, dpi=120)
    print(f"saved -> {out}")


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    df = load_data(CSV_PATH)
    print(f"data: {len(df)} daily rows, {df.index[0].date()} -> {df.index[-1].date()}")
    print(f"fee: {FEE * 100:.1f}% taker on traded notional\n")

    frames = build_frames(df)
    table = full_period_table(frames)
    print("=== FULL-PERIOD METRICS ===")
    print(table.to_string())
    table.to_csv(RESULTS / "metrics_full.csv")

    print("\n=== WALK-FORWARD (SMA family, train 730d / test 182d / step 182d) ===")
    wf, stitched_frame, oos, counts = walk_forward_sma(df)
    print(wf.to_string(index=False))
    wf.to_csv(RESULTS / "walk_forward.csv", index=False)

    oos_table = pd.DataFrame({"sma_walkforward_oos": oos}).T.round({
        "total_return_pct": 1, "CAGR_pct": 2, "ann_vol_pct": 1,
        "sharpe": 3, "sortino": 3, "max_drawdown_pct": 1, "calmar": 3,
        "fees_pct_initial": 2, "pct_days_invested": 1,
    })
    print("\n=== STITCHED OUT-OF-SAMPLE EQUITY (walk-forward) ===")
    print(oos_table.to_string())
    oos_table.to_csv(RESULTS / "walk_forward_oos_metrics.csv")
    print("\nn-selection counts across windows:")
    for n, c in counts.items():
        print(f"  sma_trend_{n}: {c}")

    tail_start = pd.Timestamp(wf["test_start"].iloc[-1])
    print(f"\n=== FINAL HOLDOUT TAIL ({tail_start.date()} -> "
          f"{df.index[-1].date()}, frozen strategies) ===")
    holdout = holdout_tail(frames, tail_start)
    print(holdout.to_string())
    holdout.to_csv(RESULTS / "holdout_tail.csv")

    save_plot(frames, table, stitched_frame)


if __name__ == "__main__":
    main()
