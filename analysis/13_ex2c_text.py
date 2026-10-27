"""13 Ex 2C: text categories with renewal account counts, and text vs structured conflicts.

Renewal records only. Categories from text_categories.py (CSM Health Note + Gong highlight).
An account is in a category if any of its renewal records in that cohort carries it.
Writes outputs/13_ex2c_categories.csv and outputs/13_ex2c_conflicts.csv.
"""
import pandas as pd

from common import load, OUT, renewals
from text_categories import RISK, add_text_signals

pd.set_option("display.width", 250)

df = load()
r = add_text_signals(renewals(df))
r["low util"] = r["Utilization - 1 Month Ago"] < 0.33
r["churned"] = r["Won/Lost"].eq("Lost")
fy26 = r[r["Close FY"].eq(2026) & r["Won/Lost"].isin(["Won", "Lost"])]
fy27 = r[r["Close FY"].eq(2027)]

labels = list(RISK) + ["Any risk category", "CSM says earlier flag was stale", "CSM note two-sided", "No risk language"]


def members(x: pd.DataFrame, label: str) -> pd.Series:
    if label in RISK:
        return x["text_cats"].map(lambda c: label in c)
    return {"Any risk category": x["text_signal"].eq("Risk"),
            "CSM says earlier flag was stale": x["note_stale_flag"],
            "CSM note two-sided": x["note_uncertain"],
            "No risk language": x["text_signal"].ne("Risk")}[label]


rows = []
for label in labels:
    m26, m27, mall = members(fy26, label), members(fy27, label), members(r, label)
    rows.append({
        "category": label,
        "renewal accounts (all)": r.loc[mall, "Account Name"].nunique(),
        "FY26 accounts": fy26.loc[m26, "Account Name"].nunique(),
        "FY27 accounts": fy27.loc[m27, "Account Name"].nunique(),
        "FY27 open Renewal ARR": fy27.loc[m27 & fy27["Won/Lost"].eq("Open"), "Renewal ARR"].sum(),
        "FY26 records": int(m26.sum()),
        "FY26 churn %": round(100 * fy26.loc[m26, "churned"].mean(), 1) if m26.any() else None,
    })
cats = pd.DataFrame(rows)
cats.to_csv(OUT / "13_ex2c_categories.csv", index=False)
print(f"Renewal accounts: all {r['Account Name'].nunique()}, FY26 closed {fy26['Account Name'].nunique()}, FY27 {fy27['Account Name'].nunique()}")
print(cats.round(0).to_string(index=False))
multi = fy27[fy27["text_signal"].eq("Risk")]["text_cats"].map(len)
print(f"FY27 risk records carrying 2+ categories: {int((multi >= 2).sum())} of {len(multi)}")

# Conflicts between text and structured fields, FY26 closed outcomes and FY27 open book
def conflict(x):
    return pd.Series({
        "Text risk, utilization fine (>=0.33)": x["text_signal"].eq("Risk") & ~x["low util"],
        "Low utilization (<0.33), no text risk": ~x["text_signal"].eq("Risk") & x["low util"],
        "Health Healthy, text risk": x["Health"].eq("Healthy") & x["text_signal"].eq("Risk"),
        "Health Critical or At-Risk, no text risk": x["Health"].isin(["Critical", "At-Risk"]) & ~x["text_signal"].eq("Risk"),
        "Stage 1 At Risk, no text risk": x["Stage"].eq("1 At Risk") & ~x["text_signal"].eq("Risk"),
        "CSM says earlier flag was stale": x["note_stale_flag"],
        "Note risk, Gong positive": x["note_signal"].eq("Risk") & x["gong_signal"].eq("Positive"),
        "Gong risk, note not risk": x["gong_signal"].eq("Risk") & ~x["note_signal"].eq("Risk"),
    })


out = []
for name, mask in conflict(r).items():
    m = pd.Series(mask, index=r.index)
    c26, o27 = m & r.index.isin(fy26.index), m & r["Close FY"].eq(2027) & r["Won/Lost"].eq("Open")
    out.append({"conflict": name, "FY26 records": int(c26.sum()),
                "FY26 churned": int(r.loc[c26, "churned"].sum()),
                "FY26 churn %": round(100 * r.loc[c26, "churned"].mean(), 1) if c26.any() else None,
                "FY27 open records": int(o27.sum()), "FY27 open Renewal ARR": round(r.loc[o27, "Renewal ARR"].sum())})
conf = pd.DataFrame(out)
conf.to_csv(OUT / "13_ex2c_conflicts.csv", index=False)
print("\n" + conf.to_string(index=False))
