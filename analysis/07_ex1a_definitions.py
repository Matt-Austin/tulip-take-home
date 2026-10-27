"""07 Ex 1A: every win-rate definition used in the Ex 1A commentary, in one table.

Win rate = Won / (Won + Lost). Year = Close FY unless stated. Writes
outputs/07_ex1a_definitions.csv and outputs/07_ex1a_board_fy26_wins.csv.
"""
import pandas as pd

from common import OUT, RT_NEW, fiscal_year, is_net_new_deal, load, nb_sales_led
from common import net_new as net_new_closed

pd.set_option("display.width", 250)

df = load()
df["Created FY"] = fiscal_year(df["Created Date"])
won, lost, open_ = (df["Won/Lost"].eq(v) for v in ("Won", "Lost", "Open"))
new_opp = df["Opportunity Record Type"].eq(RT_NEW)
net_new = df.index.isin(net_new_closed(df).index)
sales_led = df.index.isin(nb_sales_led(df).index)
stale = is_net_new_deal(df) & open_  # still Open with a close date in that FY

definitions = [
    ("Board (as reported): all New Opportunity Won/Lost", won & new_opp, lost & new_opp, "Close FY"),
    ("Net-new clients (primary)", won & net_new, lost & net_new, "Close FY"),
    ("Sales-led new business: net-new + expansions", won & sales_led, lost & sales_led, "Close FY"),
    ("Net-new, past-due Open counted as Lost", won & net_new, (lost & net_new) | stale, "Close FY"),
    ("Net-new by Created FY (cohort)", won & net_new, lost & net_new, "Created FY"),
]
rows = []
for name, w_mask, l_mask, basis in definitions:
    r, rate = {"definition": name, "year basis": basis}, {}
    for fy in (2025, 2026):
        w, l = int((w_mask & df[basis].eq(fy)).sum()), int((l_mask & df[basis].eq(fy)).sum())
        rate[fy] = 100 * w / (w + l)
        r[f"FY{fy - 2000} won"], r[f"FY{fy - 2000} lost"] = w, l
        r[f"FY{fy - 2000} win %"] = round(rate[fy], 1)
    r["change (pts)"] = round(rate[2026] - rate[2025], 1)  # from unrounded rates
    rows.append(r)
out = pd.DataFrame(rows)
out.to_csv(OUT / "07_ex1a_definitions.csv", index=False)
print(out.to_string(index=False))

# What the board's FY26 wins are made of
b = df[won & new_opp & df["Close FY"].eq(2026)]
parts = pd.Series({
    "Net-new client wins": int((b.index.isin(df[net_new].index)).sum()),
    "Expansions at existing customers": int((b["Stage"].eq("Closed Won") & b["Deal Type"].eq("Expansion")).sum()),
    "Ordered / Won order entries": int(b["Stage"].eq("Ordered / Won").sum()),
    "GTM Ops Review (admin stage)": int(b["Stage"].eq("GTM Ops Review").sum()),
})
parts["Other Closed Won"] = len(b) - parts.sum()
parts["Total board FY26 wins"] = len(b)
parts.to_csv(OUT / "07_ex1a_board_fy26_wins.csv", header=["rows"])
print("\n" + parts.to_string())
dups = df[new_opp & df["Loss Reason"].eq("Duplicate")].groupby("Close FY").size()
print(f"\nDuplicate losses in the board's denominator: {dups.to_dict()}")
print(f"Net-new deals still Open with an FY26 close date: {int((stale & df['Close FY'].eq(2026)).sum())}")
print(f"Net-new deals still Open, created in FY26: {int((stale & df['Created FY'].eq(2026)).sum())}")
