"""11 Ex 2A: FY26 renewal-cohort baseline, logo churn and ARR churn.

Cohort = Subscription Renewals with Close FY = 2026 (renewal records start Feb 2025).
Decisions (Matt, 2026-10-27):
  H15  ARR basis = Renewal ARR (annual amount up for renewal), not Total Booking.
  H21  Logo = account. A logo churns when every one of its closed FY26 renewal records churned.
  H30  Rows still Open (19, all 90+ days past close) are excluded from the base; sensitivity shown.
       The one Open duplicate of a Won record (Forsythe Beverages) is excluded with them.
  H23/H24 rows close in FY27, so they don't touch this cohort.
Writes outputs/11_ex2a_baseline.csv and outputs/11_ex2a_by_quarter.csv.
"""
import pandas as pd

from common import OUT, load, renewals

pd.set_option("display.width", 250)

df = load()
cohort = renewals(df)[lambda r: r["Close FY"].eq(2026)]
closed = cohort[cohort["Won/Lost"].isin(["Won", "Lost"])]
open_ = cohort[cohort["Won/Lost"].eq("Open")]
lost = closed["Won/Lost"].eq("Lost")
print(f"FY26 cohort: {len(cohort)} records | closed {len(closed)} (won {int((~lost).sum())}, lost {int(lost.sum())}) | open {len(open_)}")

acct = closed.groupby("Account Name")["Won/Lost"].agg(lambda s: s.eq("Lost").mean())
logos, churned_logos, partial = len(acct), int(acct.eq(1).sum()), int(acct.between(0, 1, inclusive="neither").sum())
arr_base, arr_lost = closed["Renewal ARR"].sum(), closed.loc[lost, "Renewal ARR"].sum()

rows = [
    {"measure": "Logo churn (primary): accounts fully churned / accounts", "churned": churned_logos, "base": logos},
    {"measure": "ARR churn (primary): Renewal ARR churned / Renewal ARR up for renewal", "churned": arr_lost, "base": arr_base},
    {"measure": "Sensitivity, logo: account churns if any record churned", "churned": int(acct.gt(0).sum()), "base": logos},
    {"measure": "Sensitivity, logo: renewal records", "churned": int(lost.sum()), "base": len(closed)},
    {"measure": "Sensitivity, ARR: 19 open renewals counted as churned",
     "churned": arr_lost + open_["Renewal ARR"].sum(), "base": cohort["Renewal ARR"].sum()},
    {"measure": "Sensitivity, ARR: Total Booking instead of Renewal ARR",
     "churned": closed.loc[lost, "Total Booking"].sum(), "base": closed["Total Booking"].sum()},
]
out = pd.DataFrame(rows)
out["rate %"] = (100 * out["churned"] / out["base"]).round(1)
out.to_csv(OUT / "11_ex2a_baseline.csv", index=False)
print(out.to_string(index=False))
print(f"Partial-churn accounts (some records lost, some renewed): {partial};"
      f" their lost ARR is inside ARR churn: ${closed[lost & closed['Account Name'].isin(acct[acct.between(0, 1, inclusive='neither')].index)]['Renewal ARR'].sum():,.0f}")
print(f"Gross ARR retention: {100 * (1 - arr_lost / arr_base):.1f}%")

# By fiscal quarter of close (calibration anchor for the FY27 quarterly forecast)
q = closed.assign(lost_arr=closed["Renewal ARR"].where(lost, 0), is_lost=lost).groupby("close_fq").agg(
    records=("is_lost", "size"), churned_records=("is_lost", "sum"),
    renewal_arr=("Renewal ARR", "sum"), churned_arr=("lost_arr", "sum"))
q["record churn %"] = (100 * q["churned_records"] / q["records"]).round(1)
q["ARR churn %"] = (100 * q["churned_arr"] / q["renewal_arr"]).round(1)
q.index = [f"FY26 Q{i}" for i in q.index]
q.round(0).to_csv(OUT / "11_ex2a_by_quarter.csv")
print("\n" + q.round(1).to_string())
