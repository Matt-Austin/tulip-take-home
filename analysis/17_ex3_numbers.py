"""17 Ex 3: the figures the recommendation deck uses that are not already in scripts 07-16.

Writes outputs/17_ex3_numbers.csv.
"""
import pandas as pd

from common import OUT, load, net_new, renewal_cohort
from text_categories import add_text_signals

pd.set_option("display.width", 250)

df = load()
roles = pd.read_csv(OUT / "02_owner_roles.csv", index_col=0)["role"]
rows = []

# Board number: FY27 medium churn forecast vs new ARR from FY26 net-new wins
q = pd.read_csv(OUT / "12_ex2b_quarterly.csv", index_col=0)
fy27_medium = q.loc["FY27 total", "medium churn ARR"]
nn = net_new(df)
w26 = nn[nn["Close FY"].eq(2026) & nn["won"]]
nn_arr = w26["New Committed ARR"].sum()
rows += [("FY27 medium churn ARR", fy27_medium), ("FY26 net-new wins", len(w26)),
         ("FY26 net-new New Committed ARR", nn_arr), ("Board number: churn / net-new ARR", fy27_medium / nn_arr)]

# Ex 1C lever in ARR: extra wins a year x average new ARR per FY26 net-new win
mix = pd.read_csv(OUT / "09_ex1c_mix_model.csv")
extra_wins = mix.loc[mix["scenario"].str.startswith("Proposed"), "extra wins at FY26 volume"].iloc[0]
rows += [("Average new ARR per FY26 net-new win", nn_arr / len(w26)),
         ("Mix-shift lever, ARR a year", extra_wins * nn_arr / len(w26))]

# Owner team vs FY26 churn
r = renewal_cohort(df, 2026)
r = add_text_signals(r[r["Won/Lost"].isin(["Won", "Lost"])]).join(roles, on="Opportunity Owner")
for role, g in r.groupby("role"):
    lost = g["Won/Lost"].eq("Lost")
    rows.append((f"FY26 ARR churn, {role}", g.loc[lost, "Renewal ARR"].sum() / g["Renewal ARR"].sum()))
    risk = g[g["text_signal"].eq("Risk")]
    rows.append((f"FY26 risk-text renewals churned, {role}", f"{int(risk['Won/Lost'].eq('Lost').sum())} of {len(risk)}"))
    big = g[g["Renewal ARR"] >= 50000]
    rows.append((f"FY26 renewals >= $50K churned, {role}", f"{int(big['Won/Lost'].eq('Lost').sum())} of {len(big)}"))

# FY27 open at-risk book
f = add_text_signals(renewal_cohort(df, 2027))
o = f[f["Won/Lost"].eq("Open") & f["text_signal"].eq("Risk")].join(roles, on="Opportunity Owner")
big = o[o["Renewal ARR"] >= 100000]
rows += [("FY27 open renewals with risk text", len(o)), ("their Renewal ARR", o["Renewal ARR"].sum()),
         ("of which owned by the renewal desk", o.loc[o["role"].eq("Renewal desk"), "Renewal ARR"].sum()),
         ("at-risk renewals >= $100K", len(big)), ("their Renewal ARR", big["Renewal ARR"].sum())]

# What holding FY27 churn at the FY26 rate is worth
fy26_rate = 0.16159
due = q.loc["FY27 total", "renewal ARR due"]
rows.append(("ARR kept if FY27 churn held at FY26 rate", fy27_medium - fy26_rate * due))

out = pd.DataFrame(rows, columns=["figure", "value"])
out.to_csv(OUT / "17_ex3_numbers.csv", index=False)
print(out.to_string(index=False))
