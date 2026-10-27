"""08 Ex 1B: decompose the board's FY25 -> FY26 win-rate change into mix vs performance.

Population = the board's: every New Opportunity row marked Won or Lost, by Close FY
(9.4% -> 18.5%). Segments cover every row:
  1 Initial Deployment  (Closed Won / Closed Lost, not Duplicate)
  2 Expansion           (Closed Won / Closed Lost, not Duplicate)
  3 Order entries + admin (Stage = Ordered / Won or GTM Ops Review; always Won)
  4 Duplicate records   (Loss Reason = Duplicate; always Lost)

Shift-share with midpoint weights, so the two parts add to the total exactly:
  total change = sum_s (share26 - share25) * (avg_rate - avg_blended)   [mix: what is counted]
               + sum_s avg_share * (rate26 - rate25)       [performance]
A segment absent in FY25 has no FY25 rate; its FY25 rate is set to its FY26 rate,
so it contributes mix only. Writes outputs/08_ex1b_decomposition.csv.
"""
import numpy as np
import pandas as pd

from common import OUT, RT_NEW, load

pd.set_option("display.width", 250)

df = load()
b = df[df["Opportunity Record Type"].eq(RT_NEW) & df["Won/Lost"].isin(["Won", "Lost"])
       & df["Close FY"].isin([2025, 2026])].copy()
b["segment"] = np.select(
    [b["Loss Reason"].eq("Duplicate"),
     b["Stage"].isin(["Ordered / Won", "GTM Ops Review"]),
     b["Deal Type"].eq("Initial Deployment"),
     b["Deal Type"].eq("Expansion")],
    ["4 Duplicate records", "3 Order entries + admin", "1 Initial Deployment", "2 Expansion"],
    "5 Other")
assert not b["segment"].eq("5 Other").any(), "every board row must fall in a segment"

g = b.groupby(["segment", "Close FY"]).agg(rows=("Won/Lost", "size"), won=("Won/Lost", lambda s: int(s.eq("Won").sum())))
t = g.unstack("Close FY", fill_value=0)
t.columns = [f"{m} FY{fy - 2000}" for m, fy in t.columns]
for fy in ("FY25", "FY26"):
    t[f"share {fy}"] = t[f"rows {fy}"] / t[f"rows {fy}"].sum()
    t[f"win rate {fy}"] = t[f"won {fy}"] / t[f"rows {fy}"].replace(0, np.nan)
t["win rate FY25"] = t["win rate FY25"].fillna(t["win rate FY26"])  # absent in FY25: no rate change
avg_rate = (t["win rate FY25"] + t["win rate FY26"]) / 2
avg_share = (t["share FY25"] + t["share FY26"]) / 2
blended_avg = (t["won FY25"].sum() / t["rows FY25"].sum() + t["won FY26"].sum() / t["rows FY26"].sum()) / 2
# Measured against the average blended rate: shares sum to 1 both years, so the mix total is
# unchanged, but a segment gets credit for being above or below the blend (duplicates show up).
t["mix (pts)"] = 100 * (t["share FY26"] - t["share FY25"]) * (avg_rate - blended_avg)
t["performance (pts)"] = 100 * avg_share * (t["win rate FY26"] - t["win rate FY25"])
t["total (pts)"] = t["mix (pts)"] + t["performance (pts)"]

blended = {fy: 100 * t[f"won {fy}"].sum() / t[f"rows {fy}"].sum() for fy in ("FY25", "FY26")}
change = blended["FY26"] - blended["FY25"]
assert abs(t["total (pts)"].sum() - change) < 1e-9, "components must reconcile to the total"

show = t[["rows FY25", "won FY25", "share FY25", "win rate FY25", "rows FY26", "won FY26", "share FY26",
          "win rate FY26", "mix (pts)", "performance (pts)", "total (pts)"]]
show.loc["Total"] = [t["rows FY25"].sum(), t["won FY25"].sum(), 1, blended["FY25"] / 100,
                     t["rows FY26"].sum(), t["won FY26"].sum(), 1, blended["FY26"] / 100,
                     t["mix (pts)"].sum(), t["performance (pts)"].sum(), change]
show.round(4).to_csv(OUT / "08_ex1b_decomposition.csv")
print(show.round(3).to_string())
print(f"\nBlended: {blended['FY25']:.2f}% -> {blended['FY26']:.2f}% = {change:+.2f} pts"
      f" = mix {t['mix (pts)'].sum():+.2f} + performance {t['performance (pts)'].sum():+.2f}")
non_sales = t.loc[["3 Order entries + admin", "4 Duplicate records"], "total (pts)"].sum()
print(f"Of which non-sales records (segments 3-4, all mix): {non_sales:+.2f} pts;"
      f" sales motions (segments 1-2): {change - non_sales:+.2f} pts")
