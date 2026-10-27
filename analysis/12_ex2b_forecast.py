"""12 Ex 2B: FY27 churn ARR forecast, low / medium / high, by quarter.

Cohort = Subscription Renewals with Close FY = 2027, Renewal ARR basis (H15).
Already closed in FY27 (by the ~1 May 2026 snapshot): actual outcome.
  H24 Underwood Dynamics ($648K, GTM Ops Review, marked Won) = renewed.
  H23 Brightline Holdings ($29K, Deal Type mislabelled) = churned.
Still Open: churn probability = FY26 churn rate of its risk cell. Text stating explicit churn
  intent is its own cell; every other renewal falls in utilization below 0.33 (internal
  retention-risk threshold) x text risk (any other risk category in the CSM Health Note or
  Gong highlight, text_categories.py). Health is not used (H20).
  Open rows that duplicate a closed record for the same account within 60 days are dropped (H30).
Medium = cell point rates. Low / high = cell rates at the lower / upper end of a 90% Clopper-Pearson
interval on the FY26 counts. Writes outputs/12_ex2b_*.csv.
"""
from math import comb

import pandas as pd

from common import LOW_UTIL, OUT, load, renewals
from text_categories import add_text_signals

pd.set_option("display.width", 250)


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def clopper_pearson(k, n, conf=0.90):
    """Exact two-sided interval for a binomial proportion (bisection on the binomial CDF)."""
    a = (1 - conf) / 2

    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) < a)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) > a)
    return lower, upper


df = load()
r = add_text_signals(renewals(df))
r["low util"] = r["Utilization - 1 Month Ago"] < LOW_UTIL
r["text risk"] = r["text_signal"].eq("Risk")
r["cell"] = r["low util"].map({True: "Util <0.33", False: "Util >=0.33"}) + " / " + \
            r["text risk"].map({True: "text risk", False: "no text risk"})
# Customer says outright they are leaving: its own tier, whatever the utilization
r.loc[r["text_cats"].map(lambda c: "Explicit churn intent" in c), "cell"] = "Explicit churn intent"

# Calibration: FY26 churn rate by cell, with 90% interval
fy26 = r[r["Close FY"].eq(2026) & r["Won/Lost"].isin(["Won", "Lost"])]
cal = fy26.groupby("cell")["Won/Lost"].agg(records="size", churned=lambda s: int(s.eq("Lost").sum()))
cal["rate"] = cal["churned"] / cal["records"]
cal[["low", "high"]] = [clopper_pearson(k, n) for k, n in zip(cal["churned"], cal["records"])]
cal.round(4).to_csv(OUT / "12_ex2b_calibration.csv")
print("FY26 calibration by cell:\n" + cal.round(3).to_string())

# FY27 cohort
f = r[r["Close FY"].eq(2027)].copy()
closed = f[f["Won/Lost"].isin(["Won", "Lost"])]
open_ = f[f["Won/Lost"].eq("Open")]
dup = open_.apply(lambda x: ((closed["Account Name"] == x["Account Name"])
                             & ((closed["Close Date"] - x["Close Date"]).abs().dt.days <= 60)).any(), axis=1)
print(f"\nFY27 cohort {len(f)} records: closed {len(closed)}, open {len(open_)},"
      f" open duplicates of a closed record dropped: {int(dup.sum())} (${open_.loc[dup, 'Renewal ARR'].sum():,.0f})")
open_ = open_[~dup]
for case, col in [("low", "low"), ("medium", "rate"), ("high", "high")]:
    open_[f"p {case}"] = open_["cell"].map(cal[col])
    open_[f"churn ARR {case}"] = open_["Renewal ARR"] * open_[f"p {case}"]

actual = closed.assign(lost_arr=closed["Renewal ARR"].where(closed["Won/Lost"].eq("Lost"), 0))
q = pd.DataFrame({
    "closed ARR": closed.groupby("close_fq")["Renewal ARR"].sum(),
    "actual churned (closed)": actual.groupby("close_fq")["lost_arr"].sum(),
    "open ARR": open_.groupby("close_fq")["Renewal ARR"].sum(),
}).fillna(0)
q.insert(0, "renewal ARR due", q.pop("closed ARR") + q["open ARR"])
for case in ("low", "medium", "high"):
    q[f"{case} churn ARR"] = q["actual churned (closed)"] + open_.groupby("close_fq")[f"churn ARR {case}"].sum().reindex(q.index, fill_value=0)
q.index = [f"FY27 Q{i}" for i in q.index]
q.loc["FY27 total"] = q.sum()
for case in ("low", "medium", "high"):
    q[f"{case} churn %"] = 100 * q[f"{case} churn ARR"] / q["renewal ARR due"]
q.round(1).to_csv(OUT / "12_ex2b_quarterly.csv")
print("\n" + q.round(0).to_string())

# Check against FY26
fy26_arr = fy26.groupby("Won/Lost")["Renewal ARR"].sum()
print(f"\nFY26 actual ARR churn: {100 * fy26_arr['Lost'] / fy26_arr.sum():.1f}% | FY27 medium:"
      f" {q.loc['FY27 total', 'medium churn %']:.1f}% (low {q.loc['FY27 total', 'low churn %']:.1f}%,"
      f" high {q.loc['FY27 total', 'high churn %']:.1f}%)")
mix = pd.DataFrame({
    "FY26 share of renewal ARR %": 100 * fy26.groupby("cell")["Renewal ARR"].sum() / fy26["Renewal ARR"].sum(),
    "FY27 open share of open ARR %": 100 * open_.groupby("cell")["Renewal ARR"].sum() / open_["Renewal ARR"].sum(),
}).round(1)
mix.to_csv(OUT / "12_ex2b_mix_vs_fy26.csv")
print(mix.to_string())

# Swing list: largest open renewals carrying text risk
swing = open_[open_["text risk"]].sort_values("Renewal ARR", ascending=False).head(10)
swing = swing[["Account Name", "close_fq", "Renewal ARR", "Utilization - 1 Month Ago", "cell", "p medium",
               "churn ARR medium", "text_cats"]]
swing.to_csv(OUT / "12_ex2b_swing_accounts.csv", index=False)
print("\nLargest open renewals with text risk:\n" + swing.round(2).to_string(index=False))
print(f"Top 10 share of medium forecast churn ARR on open renewals: "
      f"{100 * swing['churn ARR medium'].sum() / open_['churn ARR medium'].sum():.0f}%")

# What changed vs FY26: the largest single account, and FY27's own mix at FY26 cell rates
top = swing.iloc[0]
due, med = q.loc["FY27 total", "renewal ARR due"], q.loc["FY27 total", "medium churn ARR"]
print(f"Medium excluding {top['Account Name']}: {100 * (med - top['churn ARR medium']) / (due - top['Renewal ARR']):.1f}%")
q1 = closed[closed["Won/Lost"].isin(["Won", "Lost"])].groupby("cell")["Won/Lost"].agg(
    records="size", churned=lambda s: int(s.eq("Lost").sum()))
print("FY27 renewals already closed, by cell (out-of-sample check):\n" + q1.to_string())
