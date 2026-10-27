"""09 Ex 1C: net-new win rate by size tier, vs planning assumptions, mix shift, mix model.

Population = net-new clients (Ex 1A primary): New Opportunity, Deal Type = Initial
Deployment and New Logo flag = New, Closed Won / Closed Lost, Duplicate losses excluded,
by Close FY. Size tier = size_tier from common.py (SMB + SME -> SME, H10; blank -> Unknown).
Planning assumptions are used for comparison only, never as inputs to the model.

Writes outputs/09_ex1c_tier_rates.csv, 09_ex1c_mix.csv, 09_ex1c_mix_model.csv.
"""
from math import comb

import pandas as pd

from common import OUT, PLAN_WIN_RATE, load, net_new

pd.set_option("display.width", 250)
TIERS = ["SME", "MM", "ENT", "Unknown"]

df = load()
nn = net_new(df)
nn = nn[nn["Close FY"].isin([2025, 2026])].copy()


def fisher_two_sided(w1, n1, w2, n2):
    k, n = w1 + w2, n1 + n2
    p = lambda a: comb(n1, a) * comb(n2, k - a) / comb(n, k)
    obs = p(w1)
    return sum(p(a) for a in range(max(0, k - n2), min(k, n1) + 1) if p(a) <= obs * (1 + 1e-9))


# 1. Win rate by tier and year, with the SMB / SME split under the SME tier
rows = []
for tier in TIERS:
    for label, mask in [(tier, nn["size_tier"].eq(tier))] + (
            [("  of which SMB label", nn["Company Size (Employees)"].eq("SMB")),
             ("  of which SME label", nn["Company Size (Employees)"].eq("SME"))] if tier == "SME" else []):
        r = {"tier": label}
        for fy in (2025, 2026):
            x = nn[mask & nn["Close FY"].eq(fy)]
            r[f"FY{fy - 2000} won"], r[f"FY{fy - 2000} closed"] = int(x["won"].sum()), len(x)
            r[f"FY{fy - 2000} win %"] = round(100 * x["won"].mean(), 1) if len(x) else None
        x = nn[mask]
        r["FY25+26 win %"] = round(100 * x["won"].mean(), 1)
        r["plan %"] = 100 * PLAN_WIN_RATE[tier] if label in PLAN_WIN_RATE else None
        r["FY26 gap to plan (pts)"] = round(r["FY26 win %"] - r["plan %"], 1) if r["plan %"] else None
        rows.append(r)
rates = pd.DataFrame(rows)
tot = {"tier": "Total net-new"}
for fy in (2025, 2026):
    x = nn[nn["Close FY"].eq(fy)]
    tot[f"FY{fy - 2000} won"], tot[f"FY{fy - 2000} closed"] = int(x["won"].sum()), len(x)
    tot[f"FY{fy - 2000} win %"] = round(100 * x["won"].mean(), 1)
tot["FY25+26 win %"] = round(100 * nn["won"].mean(), 1)
rates = pd.concat([rates, pd.DataFrame([tot])], ignore_index=True)
rates.to_csv(OUT / "09_ex1c_tier_rates.csv", index=False)
print(rates.to_string(index=False))

# Are the tiers different? Best vs worst tier, both years pooled
pooled = nn[nn["size_tier"].ne("Unknown")].groupby("size_tier")["won"].agg(["sum", "count"])
best, worst = pooled.eval("sum / count").idxmax(), pooled.eval("sum / count").idxmin()
p = fisher_two_sided(int(pooled.loc[best, "sum"]), int(pooled.loc[best, "count"]),
                     int(pooled.loc[worst, "sum"]), int(pooled.loc[worst, "count"]))
print(f"\nBest tier {best} vs worst {worst}, FY25+26 pooled: p = {p:.2f}")

# 2. Mix of closed net-new deals by tier
mix = pd.crosstab(nn["size_tier"], nn["Close FY"], normalize="columns").reindex(TIERS).fillna(0) * 100
mix.columns = ["FY25 share %", "FY26 share %"]
mix["shift (pts)"] = mix["FY26 share %"] - mix["FY25 share %"]
mix.round(1).to_csv(OUT / "09_ex1c_mix.csv")
print("\n" + mix.round(1).to_string())

# 3. Mix model on FY26 measured rates: blended = sum(share x rate)
r26 = nn[nn["Close FY"].eq(2026)].groupby("size_tier")["won"].mean().reindex(TIERS).fillna(0) * 100
s26 = mix["FY26 share %"] / 100
plan = pd.Series({t: 100 * PLAN_WIN_RATE.get(t, 0) for t in TIERS})
SHIFT = 10  # proposed: move 10 points of closed-deal mix from the lowest- to the highest-converting tier
lo, hi = r26.drop("Unknown").idxmin(), r26.drop("Unknown").idxmax()
proposed = s26.copy(); proposed[lo] -= SHIFT / 100; proposed[hi] += SHIFT / 100
all_hi = pd.Series(0.0, index=TIERS); all_hi[hi] = 1.0
plan_best = plan.drop("Unknown").idxmax()
plan_shift = s26.copy(); plan_shift[plan.drop("Unknown").idxmin()] -= SHIFT / 100; plan_shift[plan_best] += SHIFT / 100
scenarios = pd.DataFrame([
    {"scenario": "Today: FY26 mix x FY26 measured rates", "blended %": (s26 * r26).sum()},
    {"scenario": f"Proposed: +{SHIFT} pts of mix from {lo} to {hi}, measured rates", "blended %": (proposed * r26).sum()},
    {"scenario": f"Ceiling: 100% {hi}, measured rates", "blended %": (all_hi * r26).sum()},
    {"scenario": "Plan view: FY26 mix x planning rates", "blended %": (s26 * plan).sum()},
    {"scenario": f"Plan view: +{SHIFT} pts from {plan.drop('Unknown').idxmin()} to {plan_best}, planning rates", "blended %": (plan_shift * plan).sum()},
])
base_measured, base_plan = scenarios.loc[0, "blended %"], scenarios.loc[3, "blended %"]
scenarios["lift vs its base (pts)"] = [0, scenarios.loc[1, "blended %"] - base_measured,
                                      scenarios.loc[2, "blended %"] - base_measured, 0,
                                      scenarios.loc[4, "blended %"] - base_plan]
n26 = int(nn["Close FY"].eq(2026).sum())
scenarios["extra wins at FY26 volume"] = scenarios["lift vs its base (pts)"] / 100 * n26
scenarios.round(2).to_csv(OUT / "09_ex1c_mix_model.csv", index=False)
print(f"\nFY26 tier rates (%): {r26.round(1).to_dict()} | FY26 closed net-new deals: {n26}")
print(scenarios.round(2).to_string(index=False))

# ARR per won net-new deal by tier (context: what a win is worth)
arr = nn[nn["won"]].groupby("size_tier")["New Committed ARR"].agg(["count", "median", "sum"]).reindex(TIERS[:3])
print("\nWon net-new deals, New Committed ARR by tier (FY25+26):\n" + arr.round(0).to_string())
