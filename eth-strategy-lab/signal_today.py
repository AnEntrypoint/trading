"""Paper-trading scaffold: compute today's signals and log them.

- Loads the local history (data/ethusdt_daily.csv) and tops it up with the
  latest completed daily candles from the same source that fetched it
  (recorded in data/fetch_meta.json).
- Computes the current signal for sma_trend(100), vol_target_trend, and
  rebalance_50_50(band).
- Appends one row per date to paper_ledger.csv (idempotent: re-running on
  the same day does not create a duplicate).

Signals are computed at the latest COMPLETED daily close and apply to the
next day. This is a zero-capital research log - no orders are placed.
"""

import json
from pathlib import Path

import pandas as pd

import fetch_data
from strategies import (
    BAND_HIGH, BAND_LOW, TARGET_VOL, VOL_WINDOW, daily_returns,
    sig_sma_trend, sig_vol_target_trend, simulate_rebalance_50_50,
)

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "data" / "ethusdt_daily.csv"
META_PATH = BASE / "data" / "fetch_meta.json"
LEDGER_PATH = BASE / "paper_ledger.csv"


def load_history() -> tuple[pd.DataFrame, str]:
    meta = json.loads(META_PATH.read_text())
    source = meta["source"]
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
                                                                   
    fetch_fn = dict(fetch_data.SOURCES)[source]
    try:
        recent = fetch_fn(limit_days=400)
        df = (pd.concat([df, recent])
              .drop_duplicates(subset="date", keep="last")
              .sort_values("date").reset_index(drop=True))
        print(f"topped up history from {source}: latest completed close "
              f"{df['date'].iloc[-1].date()}")
    except Exception as exc:                                                
        print(f"warning: live top-up from {source} failed ({exc}); "
              f"using local CSV ending {df['date'].iloc[-1].date()}")
    return df.set_index("date"), source


def compute_signals(df: pd.DataFrame) -> dict:
    close = df["close"]
    last_date = df.index[-1]
    last_close = float(close.iloc[-1])

                       
    sma100 = close.rolling(100, min_periods=100).mean()
    sma100_val = float(sma100.iloc[-1])
    trend_long = bool(sig_sma_trend(df, 100).iloc[-1] > 0)

                                                       
    vt = sig_vol_target_trend(df)
    vt_size = float(vt.iloc[-1])
    ann_vol = float(close.pct_change().rolling(VOL_WINDOW).std().iloc[-1]
                    * (365 ** 0.5))
    raw_size = min(1.0, TARGET_VOL / ann_vol) if ann_vol > 0 else 0.0

                                                                       
    ret = daily_returns(df)
    sim = simulate_rebalance_50_50(ret, mode="band")
    band_weight = float(sim["p"].iloc[-1])
    band_trigger = not (BAND_LOW <= band_weight <= BAND_HIGH)

    return {
        "date": last_date,
        "close": last_close,
        "sma100": sma100_val,
        "sma100_signal": "LONG" if trend_long else "FLAT",
        "ann_vol_30d": ann_vol,
        "vol_target_raw_size": raw_size,
        "vol_target_size": vt_size,
        "band_eth_weight": band_weight,
        "band_trigger": band_trigger,
    }


def print_dashboard(s: dict) -> None:
    print("\n================ TODAY'S DASHBOARD ================")
    print(f"signal date (last completed close): {s['date'].date()}")
    print(f"ETH close:                          {s['close']:,.2f}")
    print("---------------------------------------------------")
    print(f"sma_trend(100):   {s['sma100_signal']}"
          f"   (close {s['close']:,.2f} vs SMA100 {s['sma100']:,.2f})")
    print(f"vol_target_trend: size {s['vol_target_size']:.2f}"
          f"   (30d ann. vol {s['ann_vol_30d'] * 100:.1f}%,"
          f" target {TARGET_VOL * 100:.0f}% -> raw size"
          f" {s['vol_target_raw_size']:.2f}, trend-gated)")
    print(f"rebalance 50/50 (band): ETH weight {s['band_eth_weight'] * 100:.1f}%"
          f"  band [{BAND_LOW * 100:.0f}-{BAND_HIGH * 100:.0f}%]"
          f"  -> rebalance {'TRIGGERED' if s['band_trigger'] else 'not triggered'}")
    print("===================================================")
    print("Signals apply from this close to the next day's close.")


def update_ledger(s: dict) -> None:
    row = {
        "date": str(s["date"].date()),
        "close": round(s["close"], 2),
        "sma100_signal": s["sma100_signal"],
        "vol_target_size": round(s["vol_target_size"], 4),
        "band_eth_weight": round(s["band_eth_weight"], 4),
        "band_rebalance_trigger": "YES" if s["band_trigger"] else "NO",
    }
    if LEDGER_PATH.exists():
        ledger = pd.read_csv(LEDGER_PATH, dtype={"date": str})
        if row["date"] in set(ledger["date"]):
            print(f"ledger: row for {row['date']} already exists - not duplicating")
            return
        ledger = pd.concat([ledger, pd.DataFrame([row])], ignore_index=True)
    else:
        ledger = pd.DataFrame([row])
    ledger.to_csv(LEDGER_PATH, index=False)
    print(f"ledger: appended {row['date']} -> {LEDGER_PATH}")


def main() -> None:
    df, _source = load_history()
    signals = compute_signals(df)
    print_dashboard(signals)
    update_ledger(signals)


if __name__ == "__main__":
    main()
