# Exercise 2B: FY27 churn forecast

**FY27 in-year churn ARR: medium $4.6M (24.3% of $18.97M due), low $3.6M (19.0%), high $5.7M (30.3%).** That is materially worse than FY26's actual 16.2%. More of the FY27 book carries risk in the CSM notes and Gong calls than FY26 did, and the risk sits in Q4.

## What medium represents

Medium is the expected churn ARR if each open FY27 renewal churns at the rate FY26 renewals with the same risk profile actually churned. Renewals already closed by the snapshot (about 1 May 2026) are counted at their actual outcome. Every number is Renewal ARR (as in 2A).

**Risk profile = two signals, calibrated on FY26's 348 closed renewals:**

| Risk cell | FY26 records | FY26 churned | Churn rate (90% range) |
|---|---|---|---|
| Utilization below 0.33 and risk in the text | 102 | 74 | **72.5%** (64% to 80%) |
| Utilization 0.33 or above and risk in the text | 29 | 13 | **44.8%** (29% to 62%) |
| Utilization below 0.33, no risk in the text | 20 | 0 | 0% (0% to 14%) |
| Utilization 0.33 or above, no risk in the text | 197 | 0 | 0% (0% to 1.5%) |

- **Utilization** is Utilization – 1 Month Ago. 0.33 is Tulip's internal retention-risk threshold.
- **Text risk** means the CSM Health Note or the Gong highlight falls into at least one risk category (champion loss, budget pressure, competitive displacement, M&A, adoption or value gap, customer business change, explicit churn intent; see 2C).
- **The text decides the outcome; utilization sets the odds.** No FY26 renewal without risk text churned. Low utilization raises the churn rate of a risk-flagged renewal from 45% to 72%. The FY27 renewals already closed follow the same pattern: 21 of 29 with risk text churned, 0 of 48 without.
- **Health is not used.** It behaves like a record of the outcome, not a predictor (see 2F).
- **Low and high** use the bottom and top of each cell's 90% range, so the spread reflects how much FY26 history each rate rests on.

Two FY27 records were settled by decision. Underwood Dynamics ($648K, at the GTM Ops Review admin stage but marked Won) counts as renewed. Brightline Holdings ($29K, Deal Type mislabelled Initial Deployment) counts as churned. Three open records that duplicate a closed record for the same account were dropped ($11K).

## FY27 by quarter

| Quarter | Renewal ARR due | Already churned | Still open | Low | **Medium** | High |
|---|---|---|---|---|---|---|
| Q1 (Feb to Apr 2026) | $5.25M | $0.46M | $0.95M | $0.49M (9%) | **$0.50M (9%)** | $0.52M (10%) |
| Q2 (May to Jul) | $2.46M | — | $2.43M | $0.39M (16%) | **$0.55M (22%)** | $0.74M (30%) |
| Q3 (Aug to Oct) | $4.47M | — | $4.47M | $0.46M (10%) | **$0.58M (13%)** | $0.77M (17%) |
| Q4 (Nov 2026 to Jan 2027) | $6.79M | — | $6.79M | $2.27M (33%) | **$2.98M (44%)** | $3.71M (55%) |
| **FY27** | **$18.97M** | **$0.46M** | **$14.64M** | **$3.61M (19.0%)** | **$4.61M (24.3%)** | **$5.74M (30.3%)** |

## Check against FY26

| | FY26 actual | FY27 medium |
|---|---|---|
| ARR churn rate | 16.2% | 24.3% |
| Share of renewal ARR with risk text | 34% | 52% of open ARR |
| Share of renewal records with risk text | 38% | 51% to 62% by quarter |

The FY26 rates themselves have not changed. The FY27 book has more risk in it. The biggest single factor is Antares Metals: $1.9M due in Q4, utilization 0.34, with champion-loss and competitive-displacement language. It alone adds $0.85M to the medium case. Without it, medium is still 22.0%, so the increase is spread across the book. The ten largest risk-flagged open renewals carry 57% of forecast churn on open ARR, and seven of them close in Q4. They are the renewals to review account by account before trusting any rate.

## Where the model is weakest

**Q4, and the utilization-above-0.33-with-risk-text cell.** That cell holds 34% of open FY27 ARR, including Antares Metals. Its 45% churn rate rests on only 29 FY26 records, and its 90% range runs from 29% to 62%. Q4 renewals are also the furthest out from the snapshot. A note written 8 to 12 months before the renewal date is less likely to describe the final outcome than the notes on FY26's closed records, which may have been written close to the decision. If some of that early risk resolves, Q4 and the FY27 total land closer to the low case.

---
Source: `analysis/12_ex2b_forecast.py` (uses `analysis/text_categories.py`) → `outputs/12_ex2b_calibration.csv`, `12_ex2b_quarterly.csv`, `12_ex2b_mix_vs_fy26.csv`, `12_ex2b_swing_accounts.csv`.
