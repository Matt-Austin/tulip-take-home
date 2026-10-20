"""01 Inventory: row counts and field-population checks before any total is reported.

Writes outputs/01_inventory_counts.csv and outputs/01_nb_definition_counts.csv.
No win rates are computed here.
"""
import pandas as pd

from common import (OUT, RT_RENEWAL, SIZE_ORDER, check_calendar, load,
                    nb_board, nb_land, nb_sales_led)

pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 50)

df = load()
print(f"Rows: {len(df)} | Close FY vs Close Date mismatches: {check_calendar(df)}")

# 1. Full inventory: Record Type x Deal Type x Stage x Won/Lost x Close FY
keys = ["Opportunity Record Type", "Deal Type", "Stage", "Won/Lost", "Close FY"]
inv = df.groupby(keys, dropna=False).size().rename("rows").reset_index()
inv.to_csv(OUT / "01_inventory_counts.csv", index=False)
print("\n== Rows by Record Type x Deal Type ==")
print(df.groupby(keys[:2]).size())
print("\n== Rows by Record Type x Stage x Won/Lost (columns = Close FY) ==")
print(pd.crosstab([df[k] for k in keys[:4]], df["Close FY"], margins=True))

# 2. Company Size labels
print("\n== Company Size (Employees) by Record Type ==")
print(pd.crosstab(df["Opportunity Record Type"], df["Company Size (Employees)"].fillna("(blank)"))
      .reindex(columns=SIZE_ORDER + ["(blank)"], fill_value=0))
print("\n== Company Size on closed New Opportunity rows, by Close FY ==")
nb = nb_board(df)
print(pd.crosstab(nb["Company Size (Employees)"].fillna("(blank)"), nb["Close FY"]))

# 3. Renewal-only fields populated on non-renewal rows
non = df[df["Opportunity Record Type"] != RT_RENEWAL]
print(f"\n== Renewal-type fields on {len(non)} non-renewal rows ==")
pop = pd.DataFrame({
    "Renewal ARR non-null": non.groupby("Opportunity Record Type")["Renewal ARR"].apply(lambda s: s.notna().sum()),
    "Renewal ARR > 0": non.groupby("Opportunity Record Type")["Renewal ARR"].apply(lambda s: (s > 0).sum()),
    "Health": non.groupby("Opportunity Record Type")["Health"].apply(lambda s: s.notna().sum()),
    "CSM Health Note": non.groupby("Opportunity Record Type")["CSM Health Note"].apply(lambda s: s.notna().sum()),
    "Gong Highlight": non.groupby("Opportunity Record Type")["Latest Gong Call Highlight"].apply(lambda s: s.notna().sum()),
    "rows": non.groupby("Opportunity Record Type").size(),
})
print(pop)
print("Non-renewal rows with Renewal ARR > 0:")
print(non.loc[non["Renewal ARR"] > 0, ["Opportunity Record Type", "Deal Type", "Stage", "Close FY",
                                        "New Committed ARR", "Renewal ARR", "Total Booking"]])

# 4. The 'Ordered / Won' rows inside New Opportunity
ow = df[(df["Opportunity Record Type"] == "New Opportunity") & (df["Stage"] == "Ordered / Won")]
print(f"\n== New Opportunity rows at 'Ordered / Won': {len(ow)} ==")
print("Close FY:", ow["Close FY"].value_counts().to_dict(),
      "| owners:", ow["Opportunity Owner"].value_counts().to_dict(),
      "| source:", ow["Reporting Source"].value_counts().to_dict(),
      "| Age=0:", int((ow["Age"] == 0).sum()),
      "| New Committed ARR populated:", int(ow["New Committed ARR"].notna().sum()))

# 5. Candidate new-business definitions: won / lost counts only
rows = []
for name, fn in [("Def0 board (all New Opportunity closed)", nb_board),
                 ("Def1 sales-led (ID+Exp, Closed Won/Lost, excl Duplicate)", nb_sales_led),
                 ("Def2 land only (Def1, Initial Deployment)", nb_land)]:
    d = fn(df)
    for fy in (2025, 2026):
        x = d[d["Close FY"] == fy]
        rows.append({"definition": name, "Close FY": fy,
                     "won": int(x["won"].sum()), "lost": int((~x["won"]).sum()), "closed": len(x)})
defs = pd.DataFrame(rows)
defs.to_csv(OUT / "01_nb_definition_counts.csv", index=False)
print("\n== Candidate new-business definitions (counts only) ==")
print(defs.to_string(index=False))
