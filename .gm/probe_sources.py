import sys

sys.path.insert(0, r"C:\dev\trad\eth-strategy-lab")
import fetch_data as f

for name, fn in f.SOURCES:
    try:
        df = fn()
        print(name, "rows", len(df), "range", df["date"].iloc[0].date(),
              "->", df["date"].iloc[-1].date())
    except Exception as exc:
        print(name, "FAILED:", type(exc).__name__, str(exc)[:300])
