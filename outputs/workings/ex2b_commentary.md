# Exercise 2B: FY27 churn forecast

**FY27 in-year churn ARR: medium $3.49M (18.4% of $18.97M due), low $2.50M (13.2%), high $4.84M (25.5%).** That is 2.2 points above FY26's actual 16.2%. More of the FY27 book carries risk language in the CSM notes and Gong calls than FY26 did, and most of it sits in Q4.

## What medium represents

Medium is the expected churn ARR if each open FY27 renewal churns at the rate FY26 renewals with the same risk profile actually churned. Renewals already closed by the snapshot (about 1 May 2026) count at their actual outcome. Every figure is Renewal ARR (as in 2A).

**Risk profile = five cells, calibrated on FY26's 348 closed renewals:**

| Risk cell | FY26 records | FY26 churned | Churn rate (90% range) |
|---|---|---|---|
| Text states explicit churn intent ("Likely churn", "I can't justify another year") | 54 | 53 | **98.1%** (92% to 100%) |
| Other risk language, utilization below 0.33 | 55 | 29 | **52.7%** (41% to 64%) |
| Other risk language, utilization 0.33 or above | 20 | 5 | **25.0%** (10% to 46%) |
| No risk language, utilization below 0.33 | 21 | 0 | 0% (0% to 13%) |
| No risk language, utilization 0.33 or above | 198 | 0 | 0% (0% to 1.5%) |

- **Text risk** means the CSM Health Note or the Gong highlight falls into at least one risk category (2C). Explicit churn intent is its own cell because it describes a decision already made, not an early warning.
- **Utilization** is Utilization – 1 Month Ago. 0.33 is Tulip's internal retention-risk threshold.
- **The text decides whether a renewal is at risk; utilization sets the odds.** No FY26 renewal without risk language churned (0 of 219). For renewals with risk language short of explicit intent, low utilization doubles the churn rate (53% against 25%). FY27 renewals already closed follow the same pattern: 12 of 14 with explicit intent churned, 9 of 15 with other risk language, and 0 of 48 with none.
- **Health is not used.** It behaves like a record of the outcome, not a predictor (2F).
- **Low and high** use the bottom and top of each cell's 90% range, so the spread reflects how much FY26 history each rate rests on.

Two FY27 records were settled by decision. Underwood Dynamics ($648K, at the GTM Ops Review admin stage but marked Won) counts as renewed. Brightline Holdings ($29K, Deal Type mislabelled Initial Deployment) counts as churned. Three open records that duplicate a closed record for the same account were dropped ($11K).

## FY27 by quarter

| Quarter | Renewal ARR due | Already churned | Still open | Low | **Medium** | High |
|---|---|---|---|---|---|---|
| Q1 (Feb to Apr 2026) | $5.25M | $0.46M | $0.95M | $0.48M (9%) | **$0.49M (9%)** | $0.51M (10%) |
| Q2 (May to Jul) | $2.46M | — | $2.43M | $0.27M (11%) | **$0.41M (17%)** | $0.63M (25%) |
| Q3 (Aug to Oct) | $4.47M | — | $4.47M | $0.36M (8%) | **$0.48M (11%)** | $0.69M (15%) |
| Q4 (Nov 2026 to Jan 2027) | $6.79M | — | $6.79M | $1.40M (21%) | **$2.11M (31%)** | $3.02M (44%) |
| **FY27** | **$18.97M** | **$0.46M** | **$14.64M** | **$2.50M (13.2%)** | **$3.49M (18.4%)** | **$4.84M (25.5%)** |

## Check against FY26

| | FY26 | FY27 |
|---|---|---|
| ARR churn rate | 16.2% actual | 18.4% medium |
| Share of renewal ARR with any risk language | 33% | 52% of open ARR |
| Share with explicit churn intent | 11% | 5% of open ARR |

The FY27 medium is close to FY26 for two offsetting reasons. More of the FY27 book carries risk language (52% of open ARR against 33%), which pushes churn up. But less of it is explicit intent (5% against 11%), and explicit intent is where FY26's churn was concentrated. Most FY27 risk is early warning that historically converts at 25% to 53%, not a decision already made. The largest single exposure is Antares Metals: $1.9M due in Q4, utilization 0.34, with champion-loss and competitive-displacement language, and a pilot subscription that churned in FY26 ("IT is standardising the stack and we didn't make the cut"). It adds $0.47M to the medium case. Without it, medium is 17.7%. The ten largest risk-flagged open renewals carry 52% of forecast churn on open ARR, and seven close in Q4.

## Where the model is weakest

**Q4, and renewals with risk language but healthy utilization.** That cell holds 32% of open FY27 ARR, including Antares Metals, and its 25% rate rests on 20 FY26 records (90% range 10% to 46%). Q4 renewals are also furthest from the snapshot. A note written 8 to 12 months before the renewal date is less likely to describe the outcome than the notes on FY26's closed records, which may have been written close to the decision. Across that range Antares alone moves the FY27 total by $0.28M down to $0.39M up.

---
Source: `analysis/12_ex2b_forecast.py` (uses `analysis/text_categories.py`) → `outputs/12_ex2b_calibration.csv`, `12_ex2b_quarterly.csv`, `12_ex2b_mix_vs_fy26.csv`, `12_ex2b_swing_accounts.csv`.
