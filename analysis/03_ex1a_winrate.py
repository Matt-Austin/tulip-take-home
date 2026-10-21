"""03 Ex 1A: new-business win rate, FY25 vs FY26, under each definition.

Def0 = as reported (all closed New Opportunity rows). Def1 = primary (sales-led).
Def2 = land only. Plus the Def0 -> Def1 bridge and two Def1 sensitivities (H04, H05).
Writes outputs/03_ex1a_winrate.csv and outputs/03_ex1a_bridge.csv.
"""
import pandas as pd

from common import OUT, RT_NEW, load, nb_board, nb_land, nb_sales_led

pd.set_option("display.width", 250)
FYS = (2025, 2026)

df = load()


def rates(d: pd.DataFrame, name: str, extra_won=None, extra_lost=None) -> dict:
    row = {"definition": name}
    for fy in FYS:
        x = d[d["Close FY"] == fy]
        won = int(x["won"].sum()) + (extra_won or {}).get(fy, 0)
        lost = int((~x["won"]).sum()) + (extra_lost or {}).get(fy, 0)
        row.update({f"FY{fy % 100} won": won, f"FY{fy % 100} lost": lost,
                    f"FY{fy % 100} win rate": won / (won + lost)})
    row["change (pts)"] = 100 * (row["FY26 win rate"] - row["FY25 win rate"])
    return row


new = df[df["Opportunity Record Type"] == RT_NEW]
in_scope_types = new["Deal Type"].isin(["Initial Deployment", "Expansion"])
coppermill = new[new["Stage"].eq("GTM Ops Review")].groupby("Close FY").size().to_dict()
stale_open = new[in_scope_types & new["Won/Lost"].eq("Open")].groupby("Close FY").size().to_dict()

table = pd.DataFrame([
    rates(nb_board(df), "Def0 as reported: all closed New Opportunity"),
    rates(nb_sales_led(df), "Def1 PRIMARY sales-led: ID + Expansion, Closed Won/Lost, excl Duplicate"),
    rates(nb_land(df), "Def2 land only: Def1, Initial Deployment"),
    rates(nb_sales_led(df), "Def1 sensitivity: + GTM Ops Review as Won (H04)", extra_won=coppermill),
    rates(nb_sales_led(df), "Def1 sensitivity: + still-Open past-due as Lost (H05)", extra_lost=stale_open),
])
table.to_csv(OUT / "03_ex1a_winrate.csv", index=False)
print(table.round(3).to_string(index=False))

# Bridge Def0 -> Def1: what each exclusion removes, by FY
b = nb_board(df)
steps = {
    "Ordered / Won (admin order entries, H02)": b["Stage"].eq("Ordered / Won"),
    "GTM Ops Review (H04)": b["Stage"].eq("GTM Ops Review"),
    "Duplicate losses (H03)": b["Loss Reason"].eq("Duplicate") & ~b["won"],
    "Professional Services deal type": b["Deal Type"].eq("Professional Services"),
}
rows = []
for label, mask in steps.items():
    for fy in FYS:
        x = b[mask & b["Close FY"].eq(fy)]
        rows.append({"step": label, "Close FY": fy, "won removed": int(x["won"].sum()), "lost removed": int((~x["won"]).sum())})
bridge = pd.DataFrame(rows)
bridge.to_csv(OUT / "03_ex1a_bridge.csv", index=False)
print("\nDef0 -> Def1 bridge")
print(bridge.to_string(index=False))
d0, d1 = nb_board(df), nb_sales_led(df)
assert len(d0[d0["Close FY"].isin(FYS)]) - bridge[["won removed", "lost removed"]].sum().sum() == len(d1[d1["Close FY"].isin(FYS)])
