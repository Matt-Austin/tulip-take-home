# Exercise 2C: Using the text

**Bottom line:** The text decides whether a renewal is at risk. No FY26 renewal without risk language in its CSM note or Gong highlight churned (0 of 217 records). Renewals with risk language churned 66% of the time. Structured fields set the odds within that, and where they conflict with the text, the text wins.

## Method

Renewal records only. The text on new-business rows is meaningless (hygiene H19). Both columns are templated phrases with small variations (176 distinct notes, 160 distinct Gong highlights). Every distinct phrase was read and the categories written as keyword rules (`analysis/text_categories.py`), so each assignment can be traced. A record can carry several categories: 136 of 172 risk-flagged FY27 records carry two or more. An account counts in a category if any of its renewal records in that year carries it.

## Categories and account counts

| Category | Example language | Renewal accounts (all) | FY26 accounts | FY27 accounts | FY27 open Renewal ARR | FY26 churn rate (records) |
|---|---|---|---|---|---|---|
| Explicit churn intent | "Likely churn", "I can't justify another year", "being phased out" | 86 | 54 | 33 | $0.76M | 98% |
| Customer business change | Lost a major end-customer contract, layoffs, program wound down | 35 | 15 | 20 | $0.95M | 80% |
| Competitive displacement | Reviewing a competitor, consolidating to another MES, "IT is pushing a platform they already own" | 93 | 43 | 52 | $3.48M | 79% |
| M&A / ownership change | Acquired by a company with a competing platform, merger freeze | 75 | 40 | 35 | $1.19M | 72% |
| Adoption / value gap | Pilot never went live, adoption stuck in one team, unused seats, "same value pitch" | 149 | 67 | 87 | $2.64M | 69% |
| Budget pressure | Procurement pushback, spend review, "show me ROI in writing" | 110 | 47 | 65 | $2.27M | 57% |
| Champion loss | Sponsor left or was let go, "I can't fight for it alone" | 106 | 47 | 59 | $3.61M | 51% |
| **Any risk category** | | **269** | **129** | **157** | **$7.59M** | **66%** |
| No risk language | "Renewal looks straightforward", expansion, budget locked | 284 | 193 | 150 | $7.06M | 0% |
| CSM says an earlier flag was stale | "Flagged Critical after a budget freeze rumour... never in scope" | 15 | 14 | 1 | — | 0% |
| CSM note genuinely two-sided | "Mixed signals", "too early to call" | 3 | 2 | 1 | — | 0% |

The base is 449 renewal accounts: 307 with a closed FY26 renewal and 284 with an FY27 renewal. Accounts appear in more than one row because records carry several categories and accounts span both years.

Explicit churn intent is almost a certainty (98%). Champion loss is the most recoverable (51%). Competitive displacement and champion loss together carry $7.1M of open FY27 ARR, almost half of the open book, because they include the largest accounts.

## Where text and structured fields disagree

| Conflict | FY26 records | FY26 churned | FY27 open records | FY27 open Renewal ARR |
|---|---|---|---|---|
| Text risk, utilization fine (0.33 or above) | 29 | 13 (45%) | 69 | $4.90M |
| Low utilization (below 0.33), no text risk | 20 | 0 (0%) | 4 | $0.12M |
| Health = Healthy, text risk | 24 | 5 (21%) | 25 | $1.06M |
| Health = Critical or At-Risk, no text risk | 16 | 0 (0%) | 0 | — |
| CSM note says an earlier flag was stale | 14 | 0 (0%) | 0 | — |
| CSM note risk, Gong highlight positive | 9 | 6 (67%) | 14 | $0.35M |

## The rule for resolving conflicts

1. **Text decides whether a renewal is at risk.** A risk category in either the CSM note or the Gong highlight makes the renewal at risk, whatever the structured fields say. Utilization looked fine on 13 of the FY26 churns, and Health read Healthy on 5.
2. **Utilization sets the odds within that.** For an at-risk renewal, utilization below 0.33 raises the churn rate from 45% to 72%. Low utilization without risk language is a prompt for the CSM to check, not a churn call: 0 of 20 churned.
3. **A CSM note that explicitly says an earlier flag was stale overrides the flag.** All 14 FY26 records with such a note renewed.
4. **When the note and the Gong highlight disagree, the risk wins.** Six of 9 FY26 records with a risk note and a positive call churned. The Gong highlight is one moment from one call; the note is the CSM's running view.
5. **Health is never the tiebreaker.** It is not used. Critical or At-Risk with no risk language churned 0 of 16, and Healthy with risk language churned 5 of 24 (see 2F).

**Caveat:** the FY26 notes on closed renewals may have been written close to the decision, which would make the text look more predictive than it is months ahead. FY27 renewals already closed show the same pattern (21 of 29 with risk text churned, 0 of 48 without), but those also closed near the snapshot. This is the main reason the Q4 forecast in 2B is the weakest part of the model.

---
Source: `analysis/13_ex2c_text.py` (categories in `analysis/text_categories.py`) → `outputs/13_ex2c_categories.csv`, `13_ex2c_conflicts.csv`.
