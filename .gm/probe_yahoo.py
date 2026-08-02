import sys

sys.path.insert(0, r"C:\dev\trad\eth-strategy-lab")
import fetch_data as f
import fetch_multi as m


def boom(*a, **k):
    raise RuntimeError("simulated 451 geo-block")


f.fetch_binance = boom
m.fetch_data.fetch_binance = boom

name, df = f.fetch_with_fallback()
print("eth fallback ->", name, len(df), "rows",
      df["date"].iloc[0].date(), "->", df["date"].iloc[-1].date())

status = m.fetch_basket()
for sym, s in status.items():
    print("basket", sym, s)

df2 = m.fetch_yahoo_btc()
print("extended btc -> yahoo", len(df2), "rows",
      df2["date"].iloc[0].date(), "->", df2["date"].iloc[-1].date())
