# Exercise 1: Win Rate

## A. Is the 9% → 19% real?

**No. New-business win rate was flat: 10.6% in FY25 and 10.4% in FY26.** The board's jump comes from what got counted, not from selling better.

**Definition (used from here through Ex 3):** a new-business deal is a *New Opportunity* record with Deal Type Initial Deployment or Expansion. It counts only if it closed through the sales lifecycle (`Closed Won` or `Closed Lost`). Losses coded `Duplicate` are excluded. Win rate = won ÷ (won + lost), by Close FY.

This is the right definition for this decision because the plan is to fund whatever drove the win rate. That only makes sense for deals a rep competed for. Renewals, hardware/web orders and qualification records are other record types and are out.

| Definition | FY25 won / closed | FY25 rate | FY26 won / closed | FY26 rate | Change |
|---|---|---|---|---|---|
| **Primary: sales-led new business** | 25 / 235 | **10.6%** | 17 / 164 | **10.4%** | **−0.3 pp** |
| As reported: every closed *New Opportunity* record | 25 / 265 | 9.4% | 36 / 195 | 18.5% | +9.0 pp |
| Sensitivity: new-logo land only (Initial Deployment) | 15 / 208 | 7.2% | 11 / 138 | 8.0% | +0.8 pp |

**Why the two definitions disagree.** The as-reported number reproduces the board's ~9% and ~19% exactly. It differs from the primary definition in 61 rows:
- **18 FY26 "wins" are `Ordered / Won` expansion entries.** One owner, source Eco, created and closed the same day, no ARR, all in Jul–Sep 2025. They are order-processing records, not competitive wins, and they are half of FY26's 36 reported wins.
- **42 losses coded `Duplicate`** (30 in FY25, 12 in FY26) are not lost deals.
- **1 `GTM Ops Review` win** (FY26) is excluded as an admin stage. Counting it moves FY26 to 10.9%, which doesn't change the conclusion.

**Which number the CRO should see:** 10.4% for FY26, flat on FY25. The definitions disagree on direction (+9.0 pp vs −0.3 pp), and only the primary definition measures competitive conversion. There is no FY26 improvement to put more money behind.

Every number traces to `analysis/02_ex1_winrate.py` → `outputs/02_ex1a_winrates.csv` and `02_ex1a_bridge.csv`.
