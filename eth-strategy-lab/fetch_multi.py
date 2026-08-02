"""Fetch multi-asset daily history for cross-market validation.

- Binance basket: 10 USDT pairs -> data/{SYMBOL}_daily.csv
- Extended BTC-USD history (2014-09+) from Yahoo Finance's unauthenticated
  chart API -> data/btc_usd_yahoo_daily.csv
  (fallback: CryptoCompare histoday, free, no key)

Same zero-cost rules: no API keys, completed UTC daily candles only.
Listing dates differ (SOL ~2020-08, DOGE ~2019-07, ...) - shorter histories
simply yield fewer walk-forward windows downstream.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

import fetch_data
from fetch_data import DATA_DIR, TIMEOUT, _to_df, validate

BASKET = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT",
          "ADAUSDT", "DOGEUSDT", "SOLUSDT", "LINKUSDT", "TRXUSDT"]

BTC_YAHOO_PATH = DATA_DIR / "btc_usd_yahoo_daily.csv"
BTC_START = datetime(2014, 9, 17, tzinfo=timezone.utc)                       
MIN_ROWS = 1000                                                          

HEADERS = {"User-Agent": "Mozilla/5.0 (research; zero-capital academic use)"}


def fetch_basket() -> dict[str, str]:
    """Download the Binance basket. Returns {symbol: status}."""
    status = {}
    for sym in BASKET:
        try:
            df = fetch_data.fetch_binance(symbol=sym)
            problems = validate(df, sym, min_rows=MIN_ROWS)
            if problems:
                status[sym] = "FAILED validation: " + "; ".join(problems)
                continue
            out = DATA_DIR / f"{sym}_daily.csv"
            df.to_csv(out, index=False)
            status[sym] = (f"ok: {len(df)} rows, "
                           f"{df['date'].iloc[0].date()} -> {df['date'].iloc[-1].date()}")
            print(f"{sym}: {status[sym]}")
        except Exception as exc:                                       
            status[sym] = f"FAILED: {exc}"
            print(f"{sym}: {status[sym]}")
        time.sleep(0.3)
    return status


                                                                        
def fetch_yahoo_btc() -> pd.DataFrame:
    p1 = int(BTC_START.timestamp())
    p2 = int(datetime.now(timezone.utc).timestamp())
    resp = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD",
        params={"period1": p1, "period2": p2, "interval": "1d"},
        headers=HEADERS, timeout=TIMEOUT,
    )
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    ts = result["timestamp"]
    q = result["indicators"]["quote"][0]
    rows = [(t * 1000, o, h, l, c, v)
            for t, o, h, l, c, v in zip(ts, q["open"], q["high"], q["low"],
                                        q["close"], q["volume"])
            if c is not None]
    if not rows:
        raise RuntimeError("Yahoo returned no rows")
    return _to_df(rows, "yahoo")


def fetch_cryptocompare_btc() -> pd.DataFrame:
    """Fallback: paginate histoday backwards in 2000-day chunks."""
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    to_ts = int(datetime.now(timezone.utc).timestamp())
    start_ts = int(BTC_START.timestamp())
    rows = []
    while to_ts > start_ts:
        resp = requests.get(url, params={"fsym": "BTC", "tsym": "USD",
                                         "limit": 2000, "toTs": to_ts},
                            headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("Response") != "Success":
            raise RuntimeError(f"CryptoCompare error: {payload.get('Message')}")
        batch = payload["Data"]["Data"]
        if not batch:
            break
        for d in batch:
            if d["close"] and d["close"] > 0:
                rows.append((d["time"] * 1000, d["open"], d["high"],
                             d["low"], d["close"], d.get("volumefrom", 0.0)))
        earliest = batch[0]["time"]
        if earliest >= to_ts:
            break
        to_ts = earliest - 1
        time.sleep(0.5)
    if not rows:
        raise RuntimeError("CryptoCompare returned no rows")
    return _to_df(rows, "cryptocompare")


def fetch_extended_btc() -> str:
    for name, fn in [("yahoo", fetch_yahoo_btc),
                     ("cryptocompare", fetch_cryptocompare_btc)]:
        print(f"extended BTC: trying {name} ...")
        try:
            df = fn()
            problems = validate(df, name, min_rows=MIN_ROWS)
            if problems:
                continue
            df.to_csv(BTC_YAHOO_PATH, index=False)
            msg = (f"{name}: {len(df)} rows, {df['date'].iloc[0].date()} -> "
                   f"{df['date'].iloc[-1].date()} -> {BTC_YAHOO_PATH}")
            print(f"  {msg}")
            return msg
        except Exception as exc:                
            print(f"  {name} failed: {exc}")
    raise RuntimeError("extended BTC fetch failed on all sources")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    print("=== Binance basket ===")
    status = fetch_basket()
    ok = sum(1 for v in status.values() if v.startswith("ok"))
    print(f"\nbasket: {ok}/{len(BASKET)} symbols fetched")
    print("\n=== Extended BTC history (2014+) ===")
    btc_msg = fetch_extended_btc()
    (DATA_DIR / "fetch_multi_meta.json").write_text(json.dumps(
        {"basket": status, "extended_btc": btc_msg,
         "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        indent=2))


if __name__ == "__main__":
    main()
