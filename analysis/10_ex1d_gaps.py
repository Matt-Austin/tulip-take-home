"""10 Ex 1D: evidence for the two things the file can't tell us about net-new win rate.

Gap 1: whether FY26 is a finished, comparable number (stale open pipeline, no stage history).
Gap 2: why deals are won or lost (loss reasons, sourcing, no activity or attribution data).
Population = net-new clients (Ex 1A primary). Snapshot date ~1 May 2026 (hygiene log H14).
Writes outputs/10_ex1d_loss_reasons.csv and outputs/10_ex1d_source_outcomes.csv.
"""
import pandas as pd

from common import OUT, is_net_new_deal, load, net_new

pd.set_option("display.width", 250)
SNAPSHOT = pd.Timestamp("2026-05-01")

df = load()
net_new_any = is_net_new_deal(df)
nn = net_new(df)
nn = nn[nn["Close FY"].isin([2025, 2026])]

# Gap 1: FY26 net-new deals still Open although their close date has passed
stale = df[net_new_any & df["Won/Lost"].eq("Open") & df["Close FY"].eq(2026)]
days_past = (SNAPSHOT - stale["Close Date"]).dt.days
print(f"FY26 net-new still Open: {len(stale)} | stages {stale['Stage'].value_counts().to_dict()}"
      f" | probability {stale['Probability (%)'].value_counts().to_dict()}"
      f" | days past close date: min {days_past.min()}, median {days_past.median():.0f}")
w26 = int(nn[nn["Close FY"].eq(2026)]["Won/Lost"].eq("Won").sum())
c26 = int(nn["Close FY"].eq(2026).sum())
print(f"FY26 net-new win rate: as closed {w26}/{c26} = {100 * w26 / c26:.1f}%;"
      f" stale counted as lost {w26}/{c26 + len(stale)} = {100 * w26 / (c26 + len(stale)):.1f}%")
print(f"Wins per year: {nn[nn['Won/Lost'].eq('Won')].groupby('Close FY').size().to_dict()}")

# Gap 2: loss reasons on closed-lost net-new deals
lost = nn[nn["Won/Lost"].eq("Lost")]
lr = lost["Loss Reason"].fillna("(blank)").value_counts().rename("lost deals").to_frame()
lr["share %"] = (100 * lr["lost deals"] / len(lost)).round(1)
lr.to_csv(OUT / "10_ex1d_loss_reasons.csv")
print(f"\nNet-new loss reasons ({len(lost)} lost deals, FY25+26):\n" + lr.to_string())

# Outcomes by Reporting Source: a pattern the file can show but not explain
src = pd.crosstab(nn["Reporting Source"], nn["Won/Lost"])
src["closed"] = src.sum(axis=1)
src["win %"] = (100 * src["Won"] / src["closed"]).round(1)
src.to_csv(OUT / "10_ex1d_source_outcomes.csv")
print("\nNet-new outcomes by Reporting Source (FY25+26):\n" + src.to_string())
