"""17 Ex 3: the figures the recommendation deck uses that are not already in scripts 07-16.

Writes outputs/17_ex3_numbers.csv.
"""
import contextlib
import io
import runpy
from pathlib import Path

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
    # Risk 1 tripwire baseline: share of at-risk Renewal ARR kept (ARR basis, not deal count)
    rows.append((f"FY26 risk-text Renewal ARR retained, {role}",
                 risk.loc[risk["Won/Lost"].eq("Won"), "Renewal ARR"].sum() / risk["Renewal ARR"].sum()))
    big = g[g["Renewal ARR"] >= 50000]
    rows.append((f"FY26 renewals >= $50K churned, {role}", f"{int(big['Won/Lost'].eq('Lost').sum())} of {len(big)}"))

# FY27 open at-risk book
f = add_text_signals(renewal_cohort(df, 2027))
o = f[f["Won/Lost"].eq("Open") & f["text_signal"].eq("Risk")].join(roles, on="Opportunity Owner")
big = o[o["Renewal ARR"] >= 100000]
rows += [("FY27 open renewals with risk text", len(o)), ("their Renewal ARR", o["Renewal ARR"].sum()),
         ("of which owned by the renewal desk", o.loc[o["role"].eq("Renewal desk"), "Renewal ARR"].sum()),
         ("at-risk renewals >= $100K", len(big)), ("their Renewal ARR", big["Renewal ARR"].sum()),
         ("of which owned by the renewal desk", int(big["role"].eq("Renewal desk").sum())),
         ("of which close in Q4", int(big["close_fq"].eq(4).sum())),
         ("their Renewal ARR", big.loc[big["close_fq"].eq(4), "Renewal ARR"].sum())]
big.sort_values("Renewal ARR", ascending=False)[
    ["Account Name", "close_fq", "Renewal ARR", "Utilization - 1 Month Ago", "role", "text_cats"]
].to_csv(OUT / "17_ex3_pod_accounts.csv", index=False)

# Risk 1 sizing: ARR kept on the desk-owned pod accounts if pods keep at-risk ARR at the AE rate, not the desk rate
desk_pod = big[big["role"].eq("Renewal desk")]
rate = {row[0].rsplit(", ", 1)[1]: row[1] for row in rows if row[0].startswith("FY26 risk-text Renewal ARR retained")}
lift = rate["AE (mixed source)"] - rate["Renewal desk"]
rows += [("Desk-owned pod accounts", len(desk_pod)), ("their Renewal ARR (desk-owned pods)", desk_pod["Renewal ARR"].sum()),
         ("ARR kept if pods retain at the AE rate, vs the desk rate", lift * desk_pod["Renewal ARR"].sum()),
         ("  of which closing in Q4", lift * desk_pod.loc[desk_pod["close_fq"].eq(4), "Renewal ARR"].sum())]

# Risk 2 control group: Q4 renewals with risk text that the pods don't cover (< $100K), at Ex2B cell rates
with contextlib.redirect_stdout(io.StringIO()):
    fc = runpy.run_path(str(Path(__file__).with_name("12_ex2b_forecast.py")))["open_"]
q4 = fc[fc["close_fq"].eq(4) & ~fc["cell"].str.contains("no text risk")]
for label, s in [("pods", q4[q4["Renewal ARR"] >= 100000]), ("control, not in pods", q4[q4["Renewal ARR"] < 100000])]:
    arr = s["Renewal ARR"].sum()
    rows += [(f"Q4 risk-text renewals, {label}", len(s)), (f"their Renewal ARR ({label})", arr)]
    rows += [(f"modelled ARR loss % {case} ({label})", 100 * (s[f"p {case}"] * s["Renewal ARR"]).sum() / arr)
             for case in ("low", "medium", "high")]

# What holding FY27 churn at the FY26 rate is worth
fy26_rate = 0.16159
due = q.loc["FY27 total", "renewal ARR due"]
rows.append(("ARR kept if FY27 churn held at FY26 rate", fy27_medium - fy26_rate * due))

out = pd.DataFrame(rows, columns=["figure", "value"])
out.to_csv(OUT / "17_ex3_numbers.csv", index=False)
print(out.to_string(index=False))
