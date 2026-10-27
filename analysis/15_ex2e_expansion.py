"""15 Ex 2E: expansion sizing, using the brief's fixed method exactly.

1. FY27 renewal records (Subscription Renewals, Close FY = 2027) with Utilization - 1 Month Ago > 1.0
2. Additional seats = Sold Licenses x (Utilization - 1), rounded up to whole seats
3. Price per seat = that record's Renewal ARR / Sold Licenses
4. Expansion ARR = additional seats x price per seat
All qualifying records are included, whatever their stage. The ceiling uses exact decimal
arithmetic: in binary floating point 10 x (1.1 - 1) = 1.0000000000000009, which would round up
to 2 seats instead of 1 (one record, Sterling Holdings).
Then flags records we would not pursue (risk text, already churned; text_categories.py).
Writes outputs/15_ex2e_expansion_records.csv, 15_ex2e_by_quarter.csv, 15_ex2e_summary.csv.
"""
import math
from decimal import ROUND_CEILING, Decimal

import pandas as pd

from common import OUT, load, renewals
from text_categories import add_text_signals

pd.set_option("display.width", 250)


def extra_seats(sold: int, util: float) -> int:
    return int((Decimal(int(sold)) * (Decimal(repr(util)) - 1)).to_integral_value(ROUND_CEILING))


df = load()
r = add_text_signals(renewals(df))
x = r[r["Close FY"].eq(2027) & (r["Utilization - 1 Month Ago"] > 1.0)].copy()
x["additional seats"] = [extra_seats(s, u) for s, u in zip(x["Sold Licenses"], x["Utilization - 1 Month Ago"])]
x["price per seat"] = x["Renewal ARR"] / x["Sold Licenses"]
x["expansion ARR"] = x["additional seats"] * x["price per seat"]
float_seats = sum(math.ceil(s * (u - 1)) for s, u in zip(x["Sold Licenses"], x["Utilization - 1 Month Ago"]))

summary = pd.DataFrame([{
    "renewal records": len(x), "accounts": x["Account Name"].nunique(),
    "additional seats": int(x["additional seats"].sum()), "expansion ARR": round(x["expansion ARR"].sum(), 2),
    "seats if computed in binary floating point": float_seats,
}])
summary.to_csv(OUT / "15_ex2e_summary.csv", index=False)
print(summary.to_string(index=False))

q = x.groupby("close_fq").agg(records=("additional seats", "size"), accounts=("Account Name", "nunique"),
                              seats=("additional seats", "sum"), expansion_ARR=("expansion ARR", "sum"))
q.index = [f"FY27 Q{i}" for i in q.index]
q.loc["FY27 total"] = [len(x), x["Account Name"].nunique(), x["additional seats"].sum(), x["expansion ARR"].sum()]
q.round(2).to_csv(OUT / "15_ex2e_by_quarter.csv")
print("\n" + q.round(0).to_string())

# Records we would not pursue: already churned, or risk language in the CSM note / Gong highlight
x["pursue?"] = "Pursue"
x.loc[x["text_signal"].eq("Risk"), "pursue?"] = "Don't pursue: risk text"
x.loc[x["Won/Lost"].eq("Lost"), "pursue?"] = "Don't pursue: churned"
# Expansion that may already be priced into the renewal (name says expansion, Total Booking well above Renewal ARR)
named_exp = x["Opportunity Name"].str.contains("expan", case=False) | x["Deal Type"].eq("Expansion + Renewal")
x["check overlap"] = named_exp & (x["Total Booking"] > 1.5 * x["Renewal ARR"]) & x["pursue?"].eq("Pursue")
cols = ["Account Name", "Opportunity Name", "Deal Type", "Won/Lost", "close_fq", "Sold Licenses",
        "Utilization - 1 Month Ago", "additional seats", "price per seat", "expansion ARR", "Renewal ARR",
        "Total Booking", "text_signal", "text_cats", "pursue?", "check overlap"]
x.sort_values("expansion ARR", ascending=False)[cols].to_csv(OUT / "15_ex2e_expansion_records.csv", index=False)

p = x.groupby("pursue?").agg(records=("expansion ARR", "size"), seats=("additional seats", "sum"),
                             expansion_ARR=("expansion ARR", "sum"))
print("\n" + p.round(0).to_string())
print("\nNot pursued:\n" + x[x["pursue?"].ne("Pursue")].sort_values("expansion ARR", ascending=False)[
    ["Account Name", "Won/Lost", "close_fq", "additional seats", "expansion ARR", "text_cats"]].round(0).to_string(index=False))
print("\nPursue, but check for overlap with expansion already in the deal:\n" + x[x["check overlap"]][
    ["Account Name", "Opportunity Name", "additional seats", "expansion ARR", "Renewal ARR", "Total Booking"]].round(0).to_string(index=False))
top2 = x.nlargest(2, "expansion ARR")
print(f"\nTwo largest records: {', '.join(top2['Account Name'])} = "
      f"{100 * top2['expansion ARR'].sum() / x['expansion ARR'].sum():.0f}% of expansion ARR")
won = x[x["Won/Lost"].eq("Won")]
print(f"Already renewed at current seat count: {len(won)} records, ${won['expansion ARR'].sum():,.0f}")
one = x[x["Sold Licenses"].eq(1)]
print(f"Single-seat records: {len(one)}, {int(one['additional seats'].sum())} seats, ${one['expansion ARR'].sum():,.0f}")
