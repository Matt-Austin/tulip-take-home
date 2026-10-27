"""14 Ex 2D: the three named FY27 conflict accounts, with the fields behind each conclusion.

Selected (Matt, 2026-10-27) from candidates found with text_categories.py:
  Hawkridge Co., Ltd.   numbers look fine (utilization 2.89), text says downsell risk
  Meridian Foods        flagged by utilization (0.05), text says healthy and expanding
  Jasperton Mechanical  Health Critical, CSM note says the flag was stale; renewed
Writes outputs/14_ex2d_conflict_accounts.csv.
"""
from math import ceil

import pandas as pd

from common import OUT, load, renewals
from text_categories import add_text_signals

pd.set_option("display.width", 300)
pd.set_option("display.max_colwidth", 140)

ACCOUNTS = ["Hawkridge Co., Ltd.", "Meridian Foods", "Jasperton Mechanical"]
df = load()
r = add_text_signals(renewals(df))
x = r[r["Close FY"].eq(2027) & r["Account Name"].isin(ACCOUNTS)].copy()
# What the Ex 2E expansion method would size on utilization alone
over = x["Utilization - 1 Month Ago"] > 1
x["2E seats"] = [ceil(s * (u - 1)) if o else 0 for s, u, o in zip(x["Sold Licenses"], x["Utilization - 1 Month Ago"], over)]
x["2E expansion ARR"] = x["2E seats"] * x["Renewal ARR"] / x["Sold Licenses"]
cols = ["Account Name", "Opportunity Name", "Stage", "close_fq", "Renewal ARR", "Sold Licenses",
        "Utilization - 1 Month Ago", "Health", "text_signal", "text_cats", "note_stale_flag",
        "CSM Health Note", "Latest Gong Call Highlight", "2E seats", "2E expansion ARR"]
x = x[cols].sort_values(["Account Name", "Renewal ARR"], ascending=[True, False])
x.to_csv(OUT / "14_ex2d_conflict_accounts.csv", index=False)
print(x.round(2).to_string(index=False))
