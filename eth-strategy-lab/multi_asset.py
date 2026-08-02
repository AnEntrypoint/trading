"""Cross-market confidence testing for the walk-forward SMA trend overlay.

For every asset in the Binance basket:
  (a) buy_hold, (b) the identical mechanical walk-forward SMA overlay
      (train 730d / test 182d / step 182d, pick best-Sharpe n from {50,100,200}),
      (c) rebalance_50_50_band.
Plus: extended BTC-USD history (Yahoo, 2014+), pooled OOS window stats across
assets, and an equal-weight portfolio comparison (overlay vs hold).

All strategy/backtest logic is imported from strategies.py / backtest.py.
Outputs: results/multi_asset_table.csv, results/pooled_window_stats.csv,
results/portfolio_ew.csv, results/walk_forward_btc_yahoo.csv.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from backtest import walk_forward_sma
from strategies import (
    daily_returns, engine_frame, load_data, metrics_from_frame,
    sig_buy_hold, simulate_rebalance_50_50,
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
RESULTS = BASE / "results"

BASKET = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT",
          "ADAUSDT", "DOGEUSDT", "SOLUSDT", "LINKUSDT", "TRXUSDT"]
BTC_YAHOO = DATA / "btc_usd_yahoo_daily.csv"

METRIC_ROUND = {"total_return_pct": 1, "CAGR_pct": 2, "ann_vol_pct": 1,
                "sharpe": 3, "sortino": 3, "max_drawdown_pct": 1,
                "calmar": 3, "fees_pct_initial": 2, "pct_days_invested": 1}


def analyze_asset(sym: str) -> dict:
    """Run hold + WF overlay + band on one asset; return everything needed."""
    df = load_data(DATA / f"{sym}_daily.csv")
    ret = daily_returns(df)
    hold_frame = engine_frame(sig_buy_hold(df), ret)
    band_frame = simulate_rebalance_50_50(ret, mode="band")
    wf, stitched, oos, counts = walk_forward_sma(df)

    span = slice(pd.Timestamp(wf["test_start"].iloc[0]),
                 pd.Timestamp(wf["test_end"].iloc[-1]))
    hold_m = metrics_from_frame(hold_frame.loc[span.start:span.stop])
    band_m = metrics_from_frame(band_frame.loc[span.start:span.stop])

                                                                          
    hold_windows = []
    for _, w in wf.iterrows():
        m = metrics_from_frame(
            hold_frame.loc[pd.Timestamp(w["test_start"]):
                           pd.Timestamp(w["test_end"])])
        hold_windows.append({"test_sharpe_hold": m["sharpe"],
                             "test_return_hold_pct": m["total_return_pct"]})
    wf = pd.concat([wf.reset_index(drop=True),
                    pd.DataFrame(hold_windows)], axis=1)
    wf.insert(0, "asset", sym)

    row = {
        "asset": sym,
        "oos_start": str(span.start.date()), "oos_end": str(span.stop.date()),
        "n_windows": len(wf),
        "overlay_sharpe": oos["sharpe"], "hold_sharpe": hold_m["sharpe"],
        "band_sharpe": band_m["sharpe"],
        "overlay_maxDD": oos["max_drawdown_pct"],
        "hold_maxDD": hold_m["max_drawdown_pct"],
        "band_maxDD": band_m["max_drawdown_pct"],
        "overlay_CAGR": oos["CAGR_pct"], "hold_CAGR": hold_m["CAGR_pct"],
        "band_CAGR": band_m["CAGR_pct"],
        "overlay_fees_pct": oos["fees_pct_initial"],
        "beats_hold_sharpe": oos["sharpe"] > hold_m["sharpe"],
        "beats_hold_maxDD": oos["max_drawdown_pct"] > hold_m["max_drawdown_pct"],
    }
    return {"row": row, "wf": wf, "stitched": stitched,
            "hold_frame": hold_frame, "span": span}


def pooled_stats(all_wf: pd.DataFrame) -> dict:
    ov = all_wf["test_sharpe"].astype(float)
    hd = all_wf["test_sharpe_hold"].astype(float)
    diff = ov - hd
    n = len(diff)
    t_stat = diff.mean() / (diff.std(ddof=1) / np.sqrt(n)) if n > 1 else np.nan
    return {
        "n_windows": n,
        "mean_window_sharpe_overlay": ov.mean(),
        "mean_window_sharpe_hold": hd.mean(),
        "mean_diff": diff.mean(),
        "pct_windows_positive_return":
            (all_wf["test_return_pct"].astype(float) > 0).mean() * 100,
        "pct_windows_overlay_beats_hold": (diff > 0).mean() * 100,
        "paired_t_stat": t_stat,
    }


def ew_portfolio(per_asset: dict[str, dict]) -> pd.DataFrame:
    """Daily-rebalanced equal-weight basket over the common OOS date range."""
    start = max(a["span"].start for a in per_asset.values())
    end = min(a["span"].stop for a in per_asset.values())
    ov_frames, hd_frames = [], []
    for a in per_asset.values():
        ov_frames.append(a["stitched"].loc[start:end])
        hd_frames.append(a["hold_frame"].loc[start:end])

    def combine(frames):
        return pd.DataFrame({
            "r": pd.concat(f["r"] for f in frames).groupby(level=0).mean(),
            "p": pd.concat(f["p"] for f in frames).groupby(level=0).mean(),
            "turnover": pd.concat(f["turnover"] for f in frames)
                              .groupby(level=0).mean(),
            "port_ret": pd.concat(f["port_ret"] for f in frames)
                               .groupby(level=0).mean(),
        }).sort_index()

    rows = {
        "ew_overlay": metrics_from_frame(combine(ov_frames)),
        "ew_hold": metrics_from_frame(combine(hd_frames)),
    }
    table = pd.DataFrame(rows).T.round(METRIC_ROUND)
    table.insert(0, "common_start", str(start.date()))
    table.insert(1, "common_end", str(end.date()))
    table.insert(2, "n_assets", len(per_asset))
    return table


def analyze_yahoo_btc() -> None:
    df = load_data(BTC_YAHOO)
    ret = daily_returns(df)
    print(f"\n=== EXTENDED BTC-USD (Yahoo) "
          f"{df.index[0].date()} -> {df.index[-1].date()}, {len(df)} rows ===")
    hold_full = metrics_from_frame(engine_frame(sig_buy_hold(df), ret))
    print("buy_hold, full 2014+ span:")
    print(pd.DataFrame({"btc_hold_full": hold_full}).T.round(
        METRIC_ROUND).to_string())

    wf, stitched, oos, counts = walk_forward_sma(df)
    wf.to_csv(RESULTS / "walk_forward_btc_yahoo.csv", index=False)
    span = slice(pd.Timestamp(wf["test_start"].iloc[0]),
                 pd.Timestamp(wf["test_end"].iloc[-1]))
    hold_oos = metrics_from_frame(
        engine_frame(sig_buy_hold(df), ret).loc[span.start:span.stop])
    comp = pd.DataFrame({"overlay_oos": oos, "hold_same_span": hold_oos}).T
    print(f"\nwalk-forward overlay vs hold, OOS span {span.start.date()} -> "
          f"{span.stop.date()} ({len(wf)} windows):")
    print(comp.round(METRIC_ROUND).to_string())
    print("n-selection counts:", {int(k): int(v) for k, v in counts.items()})
    print("per-window table saved -> results/walk_forward_btc_yahoo.csv")
    print(wf.to_string(index=False))


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    per_asset, all_wf = {}, []
    for sym in BASKET:
        path = DATA / f"{sym}_daily.csv"
        if not path.exists():
            print(f"{sym}: data file missing - skipped")
            continue
        per_asset[sym] = analyze_asset(sym)
        all_wf.append(per_asset[sym]["wf"])
        print(f"{sym}: done ({per_asset[sym]['row']['n_windows']} windows)")

    table = pd.DataFrame([a["row"] for a in per_asset.values()])
    table = table.round({"overlay_sharpe": 3, "hold_sharpe": 3, "band_sharpe": 3,
                         "overlay_maxDD": 1, "hold_maxDD": 1, "band_maxDD": 1,
                         "overlay_CAGR": 2, "hold_CAGR": 2, "band_CAGR": 2,
                         "overlay_fees_pct": 2})
    both = table["beats_hold_sharpe"] & table["beats_hold_maxDD"]
    print("\n=== PER-ASSET: WALK-FORWARD OVERLAY vs HOLD (same OOS span) ===")
    print(table.to_string(index=False))
    table.to_csv(RESULTS / "multi_asset_table.csv", index=False)
    n = len(table)
    print(f"\nHEADLINE: overlay beats hold on Sharpe in "
          f"{table['beats_hold_sharpe'].sum()}/{n} assets, on maxDD in "
          f"{table['beats_hold_maxDD'].sum()}/{n}, on BOTH in {both.sum()}/{n} "
          f"({both.mean() * 100:.0f}%)")

    wf_all = pd.concat(all_wf, ignore_index=True)
    wf_all.to_csv(RESULTS / "pooled_window_stats.csv", index=False)
    stats = pooled_stats(wf_all)
    print("\n=== POOLED OOS WINDOW STATS (all basket assets) ===")
    for k, v in stats.items():
        print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")
    print("  caveat: crypto assets are highly correlated -> windows are NOT")
    print("  independent; effective sample size << raw window count.")

    print("\n=== EQUAL-WEIGHT PORTFOLIO (overlay vs hold) ===")
    port = ew_portfolio(per_asset)
    print(port.to_string())
    port.to_csv(RESULTS / "portfolio_ew.csv")

    analyze_yahoo_btc()


if __name__ == "__main__":
    main()
