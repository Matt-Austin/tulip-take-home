"""02 Ex 1A: new-business win rate, FY25 vs FY26, under each definition.

Win rate = won / (won + lost), closed deals only, by Close FY.
Primary = Def1 (nb_sales_led); comparison = Def0 (nb_board); sensitivity = Def2 (nb_land).
Writes outputs/02_ex1a_winrates.csv and outputs/02_ex1a_bridge.csv.
"""
import pandas as pd

from common import OUT, RT_NEW, load, nb_board, nb_land, nb_sales_led

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)

df = load()
FYS = (2025, 2026)


def rates(d: pd.DataFrame, name: str) -> list[dict]:
    rows = []
    for fy in FYS:
        x = d[d["Close FY"] == fy]
        won, closed = int(x["won"].sum()), len(x)
        rows.append({"definition": name, "Close FY": fy, "won": won, "lost": closed - won,
                     "closed": closed, "win_rate": won / closed})
    return rows


# 1. Win rate under each definition
defs = {"Def0 board": nb_board(df), "Def1 sales-led (PRIMARY)": nb_sales_led(df),
        "Def2 land only": nb_land(df)}
wr = pd.DataFrame([r for name, d in defs.items() for r in rates(d, name)])
wr.to_csv(OUT / "02_ex1a_winrates.csv", index=False)
print("== Ex 1A win rates ==")
print(wr.assign(win_rate=wr["win_rate"].map("{:.1%}".format)).to_string(index=False))
piv = wr.pivot(index="definition", columns="Close FY", values="win_rate")
piv["change_pp"] = (piv[2026] - piv[2025]) * 100
print("\nFY25 -> FY26 change (pp):")
print(piv.round(4).to_string())

# 2. Bridge Def0 -> Def1: which closed rows the primary definition drops, by reason
b0 = nb_board(df)
b0 = b0[b0["Close FY"].isin(FYS)]
keep = b0.index.isin(nb_sales_led(df).index)
dropped = b0[~keep].copy()
dropped["reason"] = "other"
dropped.loc[dropped["Stage"] == "Ordered / Won", "reason"] = "Ordered / Won admin entry"
dropped.loc[dropped["Stage"] == "GTM Ops Review", "reason"] = "GTM Ops Review"
dropped.loc[dropped["Loss Reason"] == "Duplicate", "reason"] = "Duplicate loss"
bridge = (dropped.groupby(["reason", "Close FY", "Won/Lost"]).size()
          .unstack(["Close FY", "Won/Lost"], fill_value=0))
bridge.to_csv(OUT / "02_ex1a_bridge.csv")
print("\n== Rows in Def0 but not Def1 ==")
print(bridge.to_string())
assert (dropped["reason"] != "other").all(), "unexplained Def0 -> Def1 difference"

# 3. Sensitivity: count the GTM Ops Review row (Coppermill, FY26) as a Def1 win
cop = df[(df["Opportunity Record Type"] == RT_NEW) & (df["Stage"] == "GTM Ops Review")]
d1 = wr[wr["definition"].str.startswith("Def1")].set_index("Close FY")
w, c = d1.loc[2026, "won"] + len(cop), d1.loc[2026, "closed"] + len(cop)
print(f"\nSensitivity: Def1 FY26 incl. GTM Ops Review win = {w}/{c} = {w / c:.1%}")
