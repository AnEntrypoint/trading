"""run_all.py - single command that reproduces the full research pipeline.

Runs each step with the current interpreter (the venv python when invoked
from the venv), stops and exits non-zero on the first failure, and writes
results/summary.json with per-step status, duration and key output files.

Usage: .venv/Scripts/python.exe run_all.py
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent

STEPS = [
    ("fetch_data.py", ["data/ethusdt_daily.csv", "data/fetch_meta.json"]),
    ("backtest.py", ["results/metrics_full.csv", "results/walk_forward.csv",
                     "results/walk_forward_oos_metrics.csv",
                     "results/holdout_tail.csv", "equity_curves.png"]),
    ("fetch_multi.py", ["data/btc_usd_yahoo_daily.csv",
                        "data/fetch_multi_meta.json"]),
    ("multi_asset.py", ["results/multi_asset_table.csv",
                        "results/pooled_window_stats.csv",
                        "results/portfolio_ew.csv",
                        "results/walk_forward_btc_yahoo.csv"]),
    ("risk_suite.py", ["results/slippage_sensitivity.csv",
                       "results/yield_scenarios.csv",
                       "results/risk_suite.csv", "results/pbo.csv",
                       "results/monte_carlo.csv", "results/kelly.csv",
                       "results/execution_timing.csv"]),
    ("signal_today.py", ["paper_ledger.csv"]),
]

TAIL_LINES = 12


def run_step(script):
    start = time.monotonic()
    proc = subprocess.run([sys.executable, str(BASE / script)],
                          capture_output=True, text=True, cwd=BASE)
    duration = time.monotonic() - start
    tail = (proc.stdout.strip().splitlines() or [""])[-TAIL_LINES:]
    return {"script": script, "status": "ok" if proc.returncode == 0
            else "failed", "exit_code": proc.returncode,
            "duration_s": round(duration, 2), "stdout_tail": tail,
            "stderr_tail": (proc.stderr.strip().splitlines()
                            or [""])[-TAIL_LINES:]}


def main() -> int:
    summary = {"generated_at_utc": datetime.now(timezone.utc).isoformat(
        timespec="seconds"), "python": sys.executable, "steps": []}
    for script, outputs in STEPS:
        print(f"[run_all] {script} ...", flush=True)
        record = run_step(script)
        record["outputs"] = {
            o: (BASE / o).stat().st_size if (BASE / o).exists() else None
            for o in outputs}
        summary["steps"].append(record)
        print(f"[run_all] {script}: {record['status']} "
              f"({record['duration_s']}s)", flush=True)
        if record["status"] != "ok":
            summary["overall"] = f"failed at {script}"
            (BASE / "results" / "summary.json").write_text(
                json.dumps(summary, indent=2))
            print(f"[run_all] FAILED at {script}; see results/summary.json")
            return 1
    summary["overall"] = "ok"
    (BASE / "results" / "summary.json").write_text(
        json.dumps(summary, indent=2))
    total = sum(s["duration_s"] for s in summary["steps"])
    print(f"[run_all] all {len(STEPS)} steps ok in {total:.1f}s; "
          f"summary -> results/summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
