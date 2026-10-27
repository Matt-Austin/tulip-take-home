"""16 Ex 2F: the case against Health as a churn predictor (hygiene log H20).

Writes outputs/16_ex2f_health.csv.
"""
import pandas as pd

from common import OUT, load, renewals
from text_categories import add_text_signals

pd.set_option("display.width", 250)

df = load()
r = add_text_signals(renewals(df))
r["churned"] = r["Won/Lost"].eq("Lost")
fy26 = r[r["Close FY"].eq(2026) & r["Won/Lost"].isin(["Won", "Lost"])]

t = fy26.groupby("Health").agg(records=("churned", "size"), churned=("churned", "sum"))
t["churn %"] = (100 * t["churned"] / t["records"]).round(1)
t["records with risk text"] = fy26.groupby("Health")["text_signal"].apply(lambda s: int(s.eq("Risk").sum()))
t["churned without risk text"] = fy26.groupby("Health").apply(lambda g: int((g["churned"] & g["text_signal"].ne("Risk")).sum()))
t.to_csv(OUT / "16_ex2f_health.csv")
print("FY26 closed renewals by Health:\n" + t.to_string())

stale = fy26[fy26["note_stale_flag"]]
print(f"\nCSM notes saying the flag was stale: {len(stale)} records, Health {stale['Health'].value_counts().to_dict()},"
      f" churned {int(stale['churned'].sum())}")
risk = fy26[fy26["text_signal"].eq("Risk")]
print("Within risk-text renewals, churn by Health:", risk.groupby("Health")["churned"].agg(["sum", "size"]).to_dict("index"))
o = r[r["Close FY"].eq(2027) & r["Won/Lost"].eq("Open")]
print(f"FY27 open renewals by Health: {o['Health'].value_counts().to_dict()}")

# Runner-up: AE Probability / Forecast Category
print("\nFY26 closed, Forecast Category x outcome:\n" + pd.crosstab(fy26["Forecast Category"], fy26["Won/Lost"]).to_string())
open_renewal = o[o["Stage"].eq("2 Open Renewal")]
at75 = open_renewal["Probability (%)"].eq(75) & open_renewal["Forecast Category"].eq("Best Case")
risk_open = o[o["text_signal"].eq("Risk")]
print(f"FY27 at 2 Open Renewal: {int(at75.sum())} of {len(open_renewal)} at 75% Best Case;"
      f" open renewals with risk text: {len(risk_open)}, of which Best Case {int(risk_open['Forecast Category'].eq('Best Case').sum())}")
