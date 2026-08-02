"""Fetch full daily ETH/USD(T) OHLCV history from free public APIs (no keys).

Fallback order:
  1. Binance public klines (api.binance.com, then api-gcp.binance.com)
  2. Kraken OHLC
  3. CoinGecko market_chart (prices only; OHLC synthesized from close)

Output: data/ethusdt_daily.csv  (columns: date,open,high,low,close,volume)
Meta:   data/fetch_meta.json    (which source worked, row count, date range)
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "ethusdt_daily.csv"
META_PATH = DATA_DIR / "fetch_meta.json"

START_DT = datetime(2017, 1, 1, tzinfo=timezone.utc)
TIMEOUT = 25
HEADERS = {"User-Agent": "Mozilla/5.0 (research; zero-capital academic use)"}


def _now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def _to_df(rows, source: str) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"], unit="ms").dt.normalize()
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.sort_values("date").drop_duplicates(subset="date", keep="last")
    df = df.dropna(subset=["close"])
                                                                              
    today = pd.Timestamp.now(tz="UTC").normalize().tz_localize(None)
    df = df[df["date"] < today]
    return df.reset_index(drop=True)


                                                                          
def fetch_binance(limit_days: int | None = None,
                  symbol: str = "ETHUSDT") -> pd.DataFrame:
    """Full daily klines for `symbol`. limit_days: only the last N days (signal_today)."""
    hosts = ["https://api.binance.com", "https://api-gcp.binance.com"]
    end_ms = _now_ms()
    start_ms = int(START_DT.timestamp() * 1000)
    if limit_days is not None:
        start_ms = max(start_ms, end_ms - limit_days * 86_400_000)

    last_err = None
    for host in hosts:
        rows = []
        cursor = start_ms
        try:
            while cursor < end_ms:
                resp = requests.get(
                    host + "/api/v3/klines",
                    params={
                        "symbol": symbol,
                        "interval": "1d",
                        "limit": 1000,
                        "startTime": cursor,
                        "endTime": end_ms,
                    },
                    timeout=TIMEOUT,
                )
                resp.raise_for_status()
                batch = resp.json()
                if not batch:
                    break
                for k in batch:
                    if k[6] >= end_ms:                                            
                        continue
                    rows.append((k[0], k[1], k[2], k[3], k[4], k[5]))
                cursor = batch[-1][6] + 1
                if len(batch) < 1000:
                    break
                time.sleep(0.2)
            if rows:
                return _to_df(rows, "binance")
        except Exception as exc:                                       
            last_err = exc
            print(f"  binance host {host} failed: {exc}")
    raise RuntimeError(f"Binance failed on all hosts: {last_err}")


def fetch_yahoo(limit_days: int | None = None,
                symbol: str = "ETH-USD",
                start_dt: datetime = START_DT) -> pd.DataFrame:
    """Unauthenticated Yahoo Finance chart API; geo-tolerant Binance fallback."""
    p1 = int(start_dt.timestamp())
    if limit_days is not None:
        p1 = max(p1, int(time.time()) - limit_days * 86_400)
    p2 = int(datetime.now(timezone.utc).timestamp())
    resp = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
        params={"period1": p1, "period2": p2, "interval": "1d"},
        headers=HEADERS, timeout=TIMEOUT,
    )
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    ts = result.get("timestamp") or []
    q = result["indicators"]["quote"][0]
    rows = [(t * 1000, o, h, l, c, v)
            for t, o, h, l, c, v in zip(ts, q["open"], q["high"], q["low"],
                                        q["close"], q["volume"])
            if c is not None]
    if not rows:
        raise RuntimeError("Yahoo returned no rows")
    return _to_df(rows, "yahoo")


                                                                          
def fetch_kraken(limit_days: int | None = None) -> pd.DataFrame:
    url = "https://api.kraken.com/0/public/OHLC"
    since = int(START_DT.timestamp())
    if limit_days is not None:
        since = max(since, int(time.time()) - limit_days * 86_400)

    rows = []
    now_s = int(time.time())
    while True:
        resp = requests.get(
            url,
            params={"pair": "ETHUSD", "interval": 1440, "since": since},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("error"):
            raise RuntimeError(f"Kraken API error: {payload['error']}")
        result = payload["result"]
        key = next(k for k in result if k != "last")
        batch = result[key]
        if not batch:
            break
        for c in batch:
            t = int(c[0])
            if t + 86_400 > now_s:                      
                continue
                                                                    
            rows.append((t * 1000, c[1], c[2], c[3], c[4], c[6]))
        new_last = int(result["last"])
        if new_last <= since or len(batch) < 2:
            break
        since = new_last
        if since + 86_400 >= now_s:
            break
        time.sleep(1.2)                                     
    if not rows:
        raise RuntimeError("Kraken returned no rows")
    return _to_df(rows, "kraken")


                                                                          
def fetch_coingecko(limit_days: int | None = None) -> pd.DataFrame:
    """Last resort: daily closes + volumes only; OHLC synthesized from close."""
    days = "max" if limit_days is None else str(limit_days)
    resp = requests.get(
        "https://api.coingecko.com/api/v3/coins/ethereum/market_chart",
        params={"vs_currency": "usd", "days": days, "interval": "daily"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    payload = resp.json()
    prices = payload.get("prices", [])
    vols = {int(v[0]): v[1] for v in payload.get("total_volumes", [])}
    if not prices:
        raise RuntimeError("CoinGecko returned no prices")
    rows = [(p[0], p[1], p[1], p[1], p[1], vols.get(int(p[0]), 0.0)) for p in prices]
    return _to_df(rows, "coingecko")


SOURCES = [
    ("binance", fetch_binance),
    ("yahoo", fetch_yahoo),
    ("kraken", fetch_kraken),
    ("coingecko", fetch_coingecko),
]


                                                                           
def validate(df: pd.DataFrame, source: str, min_rows: int = 2000) -> list[str]:
    problems = []
    if len(df) <= min_rows:
        problems.append(f"only {len(df)} rows (need >{min_rows})")
    if not df["date"].is_monotonic_increasing:
        problems.append("dates not monotonic increasing")
    if df["close"].isna().any():
        problems.append("NaNs in close")
    if df["date"].duplicated().any():
        problems.append("duplicate dates")
    if problems:
        print(f"  {source} failed validation: {'; '.join(problems)}")
    return problems


def fetch_with_fallback(limit_days: int | None = None, validate_full: bool = True):
    """Try each source in order; return (source_name, df)."""
    errors = []
    for name, fn in SOURCES:
        print(f"Trying {name} ...")
        try:
            df = fn(limit_days=limit_days)
            if validate_full and limit_days is None and validate(df, name):
                continue
            print(f"  {name}: {len(df)} rows, "
                  f"{df['date'].iloc[0].date()} -> {df['date'].iloc[-1].date()}")
            return name, df
        except Exception as exc:                
            errors.append(f"{name}: {exc}")
            print(f"  {name} failed: {exc}")
    raise RuntimeError("All data sources failed:\n" + "\n".join(errors))


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    source, df = fetch_with_fallback()
    df.to_csv(CSV_PATH, index=False)
    meta = {
        "source": source,
        "rows": int(len(df)),
        "start": str(df["date"].iloc[0].date()),
        "end": str(df["date"].iloc[-1].date()),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    META_PATH.write_text(json.dumps(meta, indent=2))
    print(f"\nSUCCESS source={source}")
    print(f"rows={meta['rows']}  range={meta['start']} -> {meta['end']}")
    print(f"saved -> {CSV_PATH}")


if __name__ == "__main__":
    main()
