"""run_daily.py - daily paper-trading loop with drift check.

1. Refreshes data/ethusdt_daily.csv via fetch_data.py if the last completed
   candle is older than yesterday (UTC).
2. Runs signal_today.py (idempotent ledger append).
3. Drift check: independently recomputes the research engine's signals from
   the refreshed CSV and compares them with the ledger row written by
   signal_today.py. Exits non-zero on any mismatch.

Exit code 0 = logged and consistent. Exit 1 = failure or drift.
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

import signal_today
from strategies import load_data

BASE = Path(__file__).resolve().parent
CSV = BASE / "data" / "ethusdt_daily.csv"
LEDGER = BASE / "paper_ledger.csv"


def run(script):
    proc = subprocess.run([sys.executable, str(BASE / script)],
                          capture_output=True, text=True, cwd=BASE)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr.strip())
        print(f"run_daily: {script} failed with exit {proc.returncode}")
        sys.exit(1)


def refresh_if_stale():
    last = pd.read_csv(CSV, parse_dates=["date"])["date"].iloc[-1].date()
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    if last < yesterday:
        print(f"run_daily: data stale (last {last}, yesterday {yesterday}); "
              f"refreshing")
        run("fetch_data.py")
    else:
        print(f"run_daily: data current (last completed close {last})")


def drift_check():
    df = load_data(CSV)
    s = signal_today.compute_signals(df)
    date_str = str(s["date"].date())
    ledger = pd.read_csv(LEDGER, dtype={"date": str})
    row = ledger[ledger["date"] == date_str]
    if row.empty:
        print(f"run_daily: DRIFT - no ledger row for {date_str}")
        return False
    row = row.iloc[0]
    expected_trigger = "YES" if s["band_trigger"] else "NO"
    checks = [
        ("sma100_signal", row["sma100_signal"], s["sma100_signal"]),
        ("vol_target_size", round(float(row["vol_target_size"]), 4),
         round(s["vol_target_size"], 4)),
        ("band_rebalance_trigger", row["band_rebalance_trigger"],
         expected_trigger),
        ("close", round(float(row["close"]), 2), round(s["close"], 2)),
    ]
    ok = True
    for name, logged, recomputed in checks:
        if logged != recomputed:
            print(f"run_daily: DRIFT on {name}: ledger={logged} "
                  f"engine={recomputed}")
            ok = False
    if ok:
        print(f"run_daily: drift check ok for {date_str} "
              f"(signals match ledger)")
    return ok


def main():
    try:
        fd = os.open(BASE / ".run_daily.lock",
                     os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print("run_daily: another instance holds the lock; exiting")
        sys.exit(0)
    try:
        os.close(fd)
        refresh_if_stale()
        run("signal_today.py")
        if not drift_check():
            sys.exit(1)
        print("run_daily: done")
    finally:
        (BASE / ".run_daily.lock").unlink(missing_ok=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
