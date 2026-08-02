"""Strategy signals, backtest engine, and performance metrics.

Conventions
-----------
- Daily-close data. A signal computed at the close of day t determines the
  position held from close(t) to close(t+1); the position series returned by
  the sig_* functions is indexed by the day whose close produced it, and the
  engine shifts it by one day. No lookahead.
- Taker fee FEE charged on traded notional at every position change /
  rebalance. Flat (cash) earns 0%.
- Portfolio return on day t:  p_t * r_t - FEE * |p_t - p_{t-1}|.
"""

import numpy as np
import pandas as pd

FEE = 0.001                                             
ANN = 365                                     
TRADING_DAYS = 365.25

TARGET_VOL = 0.60                                      
VOL_WINDOW = 30                                    
BAND_LOW, BAND_HIGH = 0.45, 0.55                        


def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").set_index("date")
    return df


def daily_returns(df: pd.DataFrame) -> pd.Series:
    """Close-to-close simple returns, indexed by the day the return is earned."""
    return df["close"].pct_change().dropna()


                                                                         
def sig_buy_hold(df: pd.DataFrame) -> pd.Series:
    return pd.Series(1.0, index=df.index, name="buy_hold")


def sig_sma_trend(df: pd.DataFrame, n: int) -> pd.Series:
    sma = df["close"].rolling(n, min_periods=n).mean()
    sig = (df["close"] > sma).astype(float)
    sig[sma.isna()] = 0.0                     
    return sig.rename(f"sma_trend_{n}")


def sig_vol_target_trend(df: pd.DataFrame, sma_n: int = 100,
                         vol_window: int = VOL_WINDOW,
                         target_vol: float = TARGET_VOL) -> pd.Series:
    trend = sig_sma_trend(df, sma_n)
    ret = df["close"].pct_change()
    ann_vol = ret.rolling(vol_window, min_periods=vol_window).std() * np.sqrt(ANN)
    size = (target_vol / ann_vol).clip(upper=1.0).fillna(0.0)
    size[ann_vol <= 0] = 0.0
    return (trend * size).rename("vol_target_trend")


                                                                        
def engine_frame(positions: pd.Series, returns: pd.Series,
                 fee: float = FEE, execution_lag: int = 1,
                 cash_yield_apr: float = 0.0,
                 asset_yield_apr: float = 0.0) -> pd.DataFrame:
    """Align positions (decided at close of day t-lag) with returns (day t).

    Returns a DataFrame indexed by return dates with columns:
    r (asset return), p (position held), turnover, port_ret (net of costs).
    fee is the total per-side execution cost on traded notional.
    Yields accrue daily: cash_yield_apr on the uninvested fraction,
    asset_yield_apr (e.g. staking) on the invested fraction.
    """
    p = positions.shift(execution_lag).reindex(returns.index)
    p = p.fillna(0.0)                                   
    turnover = p.diff().abs()
    turnover.iloc[0] = abs(p.iloc[0])                   
    cash_d = (1.0 + cash_yield_apr) ** (1.0 / ANN) - 1.0
    asset_d = (1.0 + asset_yield_apr) ** (1.0 / ANN) - 1.0
    port_ret = p * (returns + asset_d) + (1.0 - p) * cash_d - fee * turnover
    return pd.DataFrame({
        "r": returns, "p": p, "turnover": turnover, "port_ret": port_ret,
    })


def simulate_rebalance_50_50(returns: pd.Series, mode: str = "band",
                             fee: float = FEE, cash_yield_apr: float = 0.0,
                             asset_yield_apr: float = 0.0) -> pd.DataFrame:
    """Exact simulation of a 50% ETH / 50% cash portfolio.

    The ETH weight drifts with price between rebalances.
    mode='daily': rebalance to 50/50 every day.
    mode='band' : rebalance only when the ETH weight leaves [0.45, 0.55].
    """
    dates = returns.index
    n = len(returns)
    port_ret = np.empty(n)
    weights = np.empty(n)
    turnovers = np.zeros(n)
    trades = np.zeros(n, dtype=bool)

    cash_d = (1.0 + cash_yield_apr) ** (1.0 / ANN) - 1.0
    asset_d = (1.0 + asset_yield_apr) ** (1.0 / ANN) - 1.0
    value = 1.0
    w = 0.5
                                               
    entry_fee = fee * 0.5
    value *= (1.0 - entry_fee)
    entry_turnover = 0.5

    for i, r in enumerate(returns.to_numpy()):
        growth = 1.0 + w * (r + asset_d) + (1.0 - w) * cash_d
        value_gross = value * growth
        w_drift = w * (1.0 + r + asset_d) / growth
        rebalance = (mode == "daily") or not (BAND_LOW <= w_drift <= BAND_HIGH)
        if rebalance:
            turnover = abs(w_drift - 0.5)
            value = value_gross - fee * turnover * value_gross
            turnovers[i] = turnover
            trades[i] = turnover > 1e-12
            w = 0.5
        else:
            value = value_gross
            w = w_drift
        weights[i] = w
        port_ret[i] = value                                                

    equity = pd.Series(port_ret, index=dates)
    ret_series = equity.pct_change()
    ret_series.iloc[0] = equity.iloc[0] / 1.0 - 1.0                                
    frame = pd.DataFrame({
        "r": returns, "p": pd.Series(weights, index=dates),
        "turnover": pd.Series(turnovers, index=dates),
        "port_ret": ret_series,
        "_trades": pd.Series(trades, index=dates),
        "_entry_fee": entry_fee,
        "_equity": equity,
    })
    return frame


                                                                         
def metrics_from_frame(frame: pd.DataFrame, fee: float = FEE,
                       initial: float = 1.0) -> dict:
    """Compute performance metrics from an engine/simulation frame slice."""
    port_ret = frame["port_ret"]
    if "_equity" in frame.columns:
                                                        
        equity = frame["_equity"] / frame["_equity"].iloc[0] * initial
        equity = pd.concat([pd.Series([initial], index=[frame.index[0]
                            - pd.Timedelta(days=1)]), equity])
    else:
        equity = pd.concat([
            pd.Series([initial], index=[frame.index[0] - pd.Timedelta(days=1)]),
            initial * (1.0 + port_ret).cumprod(),
        ])

    total_return = equity.iloc[-1] / initial - 1.0
    years = (frame.index[-1] - frame.index[0]).days / TRADING_DAYS
    cagr = (1.0 + total_return) ** (1.0 / years) - 1.0 if years > 0 else np.nan

    mu, sd = port_ret.mean(), port_ret.std()
    ann_vol = sd * np.sqrt(ANN)
    sharpe = mu / sd * np.sqrt(ANN) if sd > 0 else np.nan
    downside = port_ret.clip(upper=0.0)
    dd_dev = np.sqrt((downside**2).mean())
    sortino = mu / dd_dev * np.sqrt(ANN) if dd_dev > 0 else np.nan

    drawdown = equity / equity.cummax() - 1.0
    max_dd = drawdown.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan

                   
    equity_prev = equity.shift(1).reindex(frame.index).fillna(initial)
    fees_paid = (fee * frame["turnover"] * equity_prev).sum()
    if "_entry_fee" in frame.columns:
        fees_paid += frame["_entry_fee"].iloc[0] * initial
        n_trades = int(frame["_trades"].sum()) + 1                
    else:
        n_trades = int((frame["turnover"] > 1e-12).sum())
    pct_invested = float((frame["p"] > 0).mean() * 100.0)

    return {
        "total_return_pct": total_return * 100.0,
        "CAGR_pct": cagr * 100.0,
        "ann_vol_pct": ann_vol * 100.0,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown_pct": max_dd * 100.0,
        "calmar": calmar,
        "n_trades": n_trades,
        "fees_pct_initial": fees_paid / initial * 100.0,
        "pct_days_invested": pct_invested,
    }


def equity_curve(frame: pd.DataFrame, initial: float = 1.0) -> pd.Series:
    if "_equity" in frame.columns:
        return frame["_equity"] / frame["_equity"].iloc[0] * initial
    return initial * (1.0 + frame["port_ret"]).cumprod()
