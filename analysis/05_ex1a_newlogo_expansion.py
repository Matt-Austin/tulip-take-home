"""05 Ex 1A: New Logo win rate vs Expansion win rate, FY25 vs FY26.

New Logo  = New Opportunity, Deal Type = Initial Deployment AND New Logo flag = New.
Expansion = New Opportunity, Deal Type = Expansion AND New Logo flag = Existing.
Both: closed through Closed Won / Closed Lost only (excludes Ordered / Won and
GTM Ops Review, H02/H04), Duplicate losses excluded (H03), by Close FY.
Rows where Deal Type and the New Logo flag disagree (H07) are reported, not classified.
Expansion + Renewal (renewal record type) is excluded: its Won/Lost is a renewal
outcome, and 34 of those rows are price increases (H29).

Writes outputs/05_ex1a_newlogo_expansion.csv and outputs/05_ex1a_unclassified.csv.
"""
from math import comb

import pandas as pd

from common import OUT, RT_NEW, expansion, load, net_new, renewals

pd.set_option("display.width", 250)

df = load()
base = (
    df["Opportunity Record Type"].eq(RT_NEW)
    & df["Stage"].isin(["Closed Won", "Closed Lost"])
    & df["Loss Reason"].ne("Duplicate")
)
deal, flag = df["Deal Type"], df["New Logo vs. Existing"]
pops = {
    "Board (as reported): all New Opportunity Won/Lost": df["Opportunity Record Type"].eq(RT_NEW)
        & df["Won/Lost"].isin(["Won", "Lost"]),
    "New Logo: Initial Deployment + flag New": df.index.isin(net_new(df).index),
    "Expansion: Expansion + flag Existing": df.index.isin(expansion(df).index),
    "Sensitivity, New Logo on Deal Type only": base & deal.eq("Initial Deployment"),
    "Sensitivity, Expansion on Deal Type only": base & deal.eq("Expansion"),
    "Sensitivity, Expansion incl. 18 Ordered / Won rows": df["Opportunity Record Type"].eq(RT_NEW)
        & deal.eq("Expansion") & flag.eq("Existing")
        & df["Stage"].isin(["Closed Won", "Closed Lost", "Ordered / Won"]) & df["Loss Reason"].ne("Duplicate"),
}


def fisher_two_sided(w1, n1, w2, n2):
    """Exact test that two win rates are equal (hypergeometric, two-sided)."""
    k, n = w1 + w2, n1 + n2
    p = lambda a: comb(n1, a) * comb(n2, k - a) / comb(n, k)
    obs = p(w1)
    return sum(p(a) for a in range(max(0, k - n2), min(k, n1) + 1) if p(a) <= obs * (1 + 1e-9))


rows = []
for name, mask in pops.items():
    r = {"population": name}
    for fy in (2025, 2026):
        x = df[mask & df["Close FY"].eq(fy)]
        won = int(x["Won/Lost"].eq("Won").sum())
        r[f"FY{fy - 2000} won"], r[f"FY{fy - 2000} lost"] = won, len(x) - won
        r[f"FY{fy - 2000} win %"] = round(100 * won / len(x), 1)
    r["change (pts)"] = round(r["FY26 win %"] - r["FY25 win %"], 1)
    r["p (FY25 = FY26)"] = round(fisher_two_sided(r["FY25 won"], r["FY25 won"] + r["FY25 lost"],
                                                  r["FY26 won"], r["FY26 won"] + r["FY26 lost"]), 2)
    rows.append(r)
out = pd.DataFrame(rows)
out.to_csv(OUT / "05_ex1a_newlogo_expansion.csv", index=False)
print(out.to_string(index=False))

# Rows the two fields can't agree on (H07): reported, not classified
nb = base & deal.isin(["Initial Deployment", "Expansion"]) & df["Close FY"].isin([2025, 2026])
conflict = df[nb & ~((deal.eq("Initial Deployment") & flag.eq("New")) | (deal.eq("Expansion") & flag.eq("Existing")))]
conflict[["Account Name", "Opportunity Name", "Deal Type", "New Logo vs. Existing", "Close FY", "Won/Lost"]] \
    .to_csv(OUT / "05_ex1a_unclassified.csv", index=False)
print(f"\nUnclassified (Deal Type and New Logo flag disagree): {len(conflict)} rows")
print(pd.crosstab([conflict["Deal Type"], conflict["New Logo vs. Existing"].fillna("(blank)")],
                  [conflict["Close FY"], conflict["Won/Lost"]]).to_string())

# History check on New Logo rows: any earlier Won row for the same account?
nl = df[pops["New Logo: Initial Deployment + flag New"] & df["Close FY"].isin([2025, 2026])]
won = df[df["Won/Lost"].eq("Won")]
prior = nl.apply(lambda r: ((won["Account Name"] == r["Account Name"]) & (won["Close Date"] < r["Created Date"])).any(), axis=1)
ren = nl["Account Name"].isin(set(renewals(df)["Account Name"].dropna()))
print(f"\nNew Logo rows: {len(nl)} | with an earlier Won row for the account: {int(prior.sum())}"
      f" | won new logos that later appear as renewal accounts: {int((ren & nl['Won/Lost'].eq('Won')).sum())}"
      f" of {int(nl['Won/Lost'].eq('Won').sum())}")
