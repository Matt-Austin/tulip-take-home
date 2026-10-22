"""04 Board backtest: which definition reproduces the board's ~9% (FY25) -> ~19% (FY26)?

Tests candidate populations (record type, deal type, New Logo flag) x year basis
(Close FY vs Created FY). Win rate = Won / (Won + Lost) on the Won/Lost field.
Writes outputs/04_board_backtest.csv, ranked by distance from 9% and 19%.
"""
import pandas as pd

from common import OUT, RT_HARDWARE, RT_NEW, RT_QUAL, RT_RENEWAL, fiscal_year, load

pd.set_option("display.width", 250)

BOARD = {2025: 9.0, 2026: 19.0}  # "roughly 9 percent" / "roughly 19 percent"

df = load()
df["Created FY"] = fiscal_year(df["Created Date"])
rt, deal, logo = df["Opportunity Record Type"], df["Deal Type"], df["New Logo vs. Existing"]
new_opp = rt.eq(RT_NEW)

candidates = {
    "New Opportunity record type": new_opp,
    "New Opportunity + Hardware": rt.isin([RT_NEW, RT_HARDWARE]),
    "New Opportunity + Hardware + Qualification": rt.isin([RT_NEW, RT_HARDWARE, RT_QUAL]),
    "All non-renewal record types": rt.ne(RT_RENEWAL),
    "All record types incl. renewals": pd.Series(True, index=df.index),
    "New Opportunity, Initial Deployment": new_opp & deal.eq("Initial Deployment"),
    "New Opportunity, Expansion": new_opp & deal.eq("Expansion"),
    "Initial Deployment, any record type": deal.eq("Initial Deployment"),
    "New Logo = New, New Opportunity": new_opp & logo.eq("New"),
    "New Logo = New, any record type": logo.eq("New"),
}

rows = []
for name, mask in candidates.items():
    for basis in ["Close FY", "Created FY"]:
        r = {"population": name, "year basis": basis}
        for fy in (2025, 2026):
            x = df[mask & df["Won/Lost"].isin(["Won", "Lost"]) & df[basis].eq(fy)]
            won = int(x["Won/Lost"].eq("Won").sum())
            r[f"FY{fy - 2000} won"], r[f"FY{fy - 2000} lost"] = won, len(x) - won
            r[f"FY{fy - 2000} win %"] = round(100 * won / len(x), 1) if len(x) else None
        r["pts from board"] = round(abs(r["FY25 win %"] - BOARD[2025]) + abs(r["FY26 win %"] - BOARD[2026]), 1)
        rows.append(r)

out = pd.DataFrame(rows).sort_values("pts from board")
out.to_csv(OUT / "04_board_backtest.csv", index=False)
print(out.to_string(index=False))

# What drives the jump inside the matching population: FY26 wins by Stage
m = new_opp & df["Won/Lost"].isin(["Won", "Lost"])
print("\nMatching population, rows by Stage x Close FY:")
print(pd.crosstab(df.loc[m, "Stage"], df.loc[m, "Close FY"]).to_string())
real = m & df["Stage"].isin(["Closed Won", "Closed Lost"])
for fy in (2025, 2026):
    x = df[real & df["Close FY"].eq(fy)]
    won = int(x["Won/Lost"].eq("Won").sum())
    print(f"FY{fy - 2000} with admin-stage wins removed (Closed Won/Lost only): "
          f"{won}/{len(x)} = {100 * won / len(x):.1f}%")
