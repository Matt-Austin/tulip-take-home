# Exercise 2: Renewals, churn and expansion

**FY27 churn ARR is likely to land near $3.5M (18.4%), slightly worse than FY26's 16.2%, with most of the risk in Q4 and one account, Antares Metals, able to move the total by up to $0.4M on its own.** The CSM notes and Gong calls decide which renewals are at risk; the structured fields only set the odds.

## A. FY26 baseline

Renewal records closing in FY26: 348 closed, 19 still open and excluded. **Logo churn 24.1%** (74 of 307 accounts lost every renewal and hold none in FY27). **ARR churn 16.2%** ($2.13M of $13.15M Renewal ARR). Renewal ARR is the basis because Total Booking includes multi-year terms and expansion uplift. Every reasonable treatment gives 24% to 28% logo churn and 16% to 18% ARR churn. Churn falls on smaller accounts, and it is concentrated: Holloway Defense ($365K) is 17% of FY26 churned ARR.

## B. FY27 forecast

| | Q1 | Q2 | Q3 | Q4 | **FY27** |
|---|---|---|---|---|---|
| Renewal ARR due | $5.25M | $2.46M | $4.47M | $6.79M | $18.97M |
| **Medium** | $0.49M | $0.41M | $0.48M | $2.11M | **$3.49M (18.4%)** |
| Low / high | $0.48–0.51M | $0.27–0.63M | $0.36–0.69M | $1.40–3.02M | $2.50–4.84M (13.2–25.5%) |

**Medium** = Q1 actuals plus each open renewal at the FY26 churn rate of its risk cell: explicit churn intent in the text 98%; other risk language with utilization below 0.33, 53%; other risk language with healthy utilization, 25%; no risk language, 0% (0 of 219 in FY26). Low and high use each cell's 90% range. **Check against FY26:** more of the FY27 book carries risk language (52% of open ARR against 33%), but less of it is explicit intent (5% against 11%), so the rate lands near FY26. **Weakest point:** Q4 renewals with risk language but healthy utilization. That cell is 32% of open ARR, rests on 20 FY26 records, and holds Antares Metals ($1.9M).

## C. Using the text

Seven risk categories from the CSM note and Gong highlight, with renewal accounts and FY26 churn: explicit churn intent (86 accounts, 98%), M&A (67, 83%), competitive displacement (93, 81%), customer business change (35, 80%), adoption or value gap (149, 69%), budget pressure (112, 55%), champion loss (105, 52%). **Conflict rule:** (1) text decides whether a renewal is at risk; (2) explicit intent is decisive, otherwise low utilization doubles the odds; (3) a CSM note saying a flag was stale overrides it (16 of 16 renewed); (4) if the note and the call disagree, risk wins; (5) Health is never the tiebreaker.

## D. Conflict accounts

- **Hawkridge Co., Ltd. ($258K, Q2).** Utilization 2.89 says expand (the 2E method sizes it at $489K), but the CSM reports a plateau and "risk flat-to-down renewal", and a second subscription is being phased out. *Treat as downsell risk; don't pitch seats.*
- **Meridian Foods ($53K, Q3).** Utilization 0.05 flags severe risk, but adoption is "trending up" and three APAC sites want in. *The usage reading is wrong; treat as a safe renewal with expansion potential.*
- **Jasperton Mechanical ($7K renewed, $4K open).** Health reads Critical on both subscriptions. The note shows the first flag was stale (it renewed in Q1); the second lost its end-customer contract. *Plan the second as churn.*

## E. Expansion sizing (fixed method)

**82 FY27 renewal records, 78 accounts, 826 additional seats, $2,508,467.85**: Q1 $584K, Q2 $722K, Q3 $887K, Q4 $316K. Exact arithmetic used: floating point gives 827 seats. It overstates in practice: over-utilization may be shared logins, 52% of the total is two accounts, and Larkspur Dynamics ($824K) may already include expansion in its renewal. **Not pursued: $744K** across 7 accounts with risk language or churn (Hawkridge, Redwood Precision, Thornton Instruments and four smaller), leaving **$1.76M** to pursue.

## F. The field we wouldn't trust

**Health.** FY26 renewals marked At-Risk churned **0 of 36**; Critical churned 94% and Healthy 2%. A middle grade that never churns means Critical is set after the decision, not before. 88 open FY27 renewals are marked At-Risk today. Runner-up: Probability, with 231 of 235 open renewals at 75% regardless of risk.

---
Workings: `outputs/workings/ex2a` to `ex2f`; scripts `analysis/11` to `16` and `analysis/text_categories.py`.
