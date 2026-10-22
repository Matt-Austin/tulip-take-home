"""06 Ex 1A: should Expansion + Renewal records with a seat increase count as expansion wins?

For each Expansion + Renewal row (renewal record type), find the latest earlier Won
record for the same account (renewal or New Opportunity) and compare Sold Licenses.
Then recompute the Expansion win rate (05 definition) with those rows added.
Writes outputs/06_ex1a_er_license_match.csv and outputs/06_ex1a_expansion_with_er.csv.
"""
import numpy as np
import pandas as pd

from common import OUT, RT_NEW, RT_RENEWAL, load, renewals

pd.set_option("display.width", 250)

df = load()
er = df[df["Opportunity Record Type"].eq(RT_RENEWAL) & df["Deal Type"].eq("Expansion + Renewal")].copy()
er["name says"] = np.where(er["Opportunity Name"].str.lower().str.contains("expan"), "expansion", "price increase")

prior_pool = df[df["Won/Lost"].eq("Won") & df["Opportunity Record Type"].isin([RT_RENEWAL, RT_NEW])]


def prior_record(r):
    p = prior_pool[prior_pool["Account Name"].eq(r["Account Name"])
                   & (prior_pool["Close Date"] < r["Close Date"]) & (prior_pool.index != r.name)]
    if p.empty:
        return pd.Series({"prior close": pd.NaT, "prior licenses": np.nan})
    p = p.sort_values("Close Date").iloc[-1]
    return pd.Series({"prior close": p["Close Date"], "prior licenses": p["Sold Licenses"]})


er = er.join(er.apply(prior_record, axis=1))
er["prior licenses"] = pd.to_numeric(er["prior licenses"], errors="coerce")  # NaT placeholders -> NaN
er["license change"] = np.select(
    [er["prior licenses"].isna(), er["Sold Licenses"] > er["prior licenses"], er["Sold Licenses"] < er["prior licenses"]],
    ["no earlier record", "up", "down"], "same")
subs = renewals(df).groupby(["Account Name", "Close FY"]).size()
er["multi-subscription account"] = [subs.get((a, f), 0) > 1 for a, f in zip(er["Account Name"], er["Close FY"])]
er[["Account Name", "Opportunity Name", "name says", "Close FY", "Won/Lost", "prior close", "prior licenses",
    "Sold Licenses", "license change", "multi-subscription account"]].to_csv(OUT / "06_ex1a_er_license_match.csv", index=False)

print("Expansion + Renewal rows by Close FY x license change (FY25 has none: renewal records start Feb 2025)")
print(pd.crosstab([er["Close FY"], er["name says"]], er["license change"], margins=True).to_string())
up = er[er["license change"].eq("up")]
print("\nLicense-up rows by outcome:")
print(pd.crosstab(up["Close FY"], up["Won/Lost"]).to_string())

expansion = (df["Opportunity Record Type"].eq(RT_NEW) & df["Stage"].isin(["Closed Won", "Closed Lost"])
             & df["Loss Reason"].ne("Duplicate") & df["Deal Type"].eq("Expansion")
             & df["New Logo vs. Existing"].eq("Existing"))
variants = {
    "Expansion (05 definition)": expansion,
    "+ Expansion + Renewal with licenses up": expansion | df.index.isin(up.index),
    "+ licenses up, single-subscription accounts only": expansion | df.index.isin(up[~up["multi-subscription account"]].index),
    "+ all Expansion + Renewal": expansion | df.index.isin(er.index),
}
rows = []
for name, mask in variants.items():
    r = {"population": name}
    for fy in (2025, 2026):
        x = df[mask & df["Won/Lost"].isin(["Won", "Lost"]) & df["Close FY"].eq(fy)]
        won = int(x["Won/Lost"].eq("Won").sum())
        r[f"FY{fy - 2000} won"], r[f"FY{fy - 2000} lost"] = won, len(x) - won
        r[f"FY{fy - 2000} win %"] = round(100 * won / len(x), 1)
    rows.append(r)
out = pd.DataFrame(rows)
out.to_csv(OUT / "06_ex1a_expansion_with_er.csv", index=False)
print("\n" + out.to_string(index=False))
