# Daily paper-trading loop

`run_daily.py` refreshes the data if stale, logs today's signals via
`signal_today.py`, then re-derives the same signals straight from the
research engine on the refreshed CSV and exits non-zero if they disagree
(drift check). Daily candles complete at 00:00 UTC, so schedule it a few
minutes after.

## Windows Task Scheduler (schtasks)

Run once from an elevated or normal prompt (paths as on this machine):

```
schtasks /Create /TN "eth-strategy-lab-daily" /SC DAILY /ST 00:15 /F /TR "\"C:\dev\trad\eth-strategy-lab\.venv\Scripts\python.exe\" C:\dev\trad\eth-strategy-lab\run_daily.py >> C:\dev\trad\eth-strategy-lab\logs\daily.log 2>&1"
```

Create the log directory first:

```
mkdir C:\dev\trad\eth-strategy-lab\logs
```

Notes: /ST 00:15 is local machine time; pick a local time that lands after
00:05 UTC (e.g. 01:15 local for UTC+1, 08:15 for UTC+8). Check with
`schtasks /Query /TN "eth-strategy-lab-daily" /V /FO LIST`, remove with
`schtasks /Delete /TN "eth-strategy-lab-daily" /F`.

## cron (Git Bash / WSL / Linux)

```
15 0 * * * cd /c/dev/trad/eth-strategy-lab && .venv/Scripts/python.exe run_daily.py >> logs/daily.log 2>&1
```

(On WSL/Linux use the Linux path form, e.g. /mnt/c/dev/trad/eth-strategy-lab,
and the venv's bin/python.)

## What to watch

- `paper_ledger.csv` gains at most one row per UTC day (idempotent).
- A non-zero exit means fetch failed, signal computation failed, or the
  drift check found signal_today.py disagreeing with the engine - treat
  any non-zero exit as a kill-switch event per discipline.md and
  investigate before trusting that day's row.
