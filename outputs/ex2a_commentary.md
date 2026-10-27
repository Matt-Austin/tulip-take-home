# Exercise 2A: FY26 baseline

**FY26 logo churn: 25.1%** (77 of 307 accounts). **FY26 ARR churn: 16.2%** ($2.13M of $13.15M Renewal ARR up for renewal). Gross ARR retention is 83.8%. These are the calibration anchors for the FY27 forecast.

## Definitions

- **Cohort:** Subscription Renewal records with a close date in FY26 (Feb 2025 to Jan 2026): 367 records. 348 are closed (261 renewed, 87 churned) and 19 are still Open.
- **Logo:** an account. A logo churns when every one of its closed FY26 renewal records churned. Nine accounts renewed some subscriptions and lost others. They count as retained logos, and the $190K they lost is included in ARR churn.
- **ARR:** Renewal ARR, the annual amount up for renewal on each record. Total Booking is contract value. It often spans several years or includes the expansion uplift, so it is not an annual churn measure.
- **Open renewals:** excluded. All 19 are 90 to 335 days past their close date, so their outcome is unknown. One of them, Forsythe Beverages, is an open duplicate of a renewal already recorded as Won.

## Result and sensitivities

| Measure | Churned | Base | Rate |
|---|---|---|---|
| **Logo churn** (accounts fully churned) | 77 | 307 accounts | **25.1%** |
| **ARR churn** (Renewal ARR) | $2.13M | $13.15M | **16.2%** |
| Logo, if any churned record counts | 86 | 307 | 28.0% |
| Logo, counted by renewal record | 87 | 348 | 25.0% |
| ARR, if the 19 open renewals all churned | $2.37M | $13.40M | 17.7% |
| ARR, on Total Booking instead | $7.18M | $36.36M | 19.8% |

Every reasonable treatment lands logo churn at 25% to 28% and ARR churn at 16% to 18%.

## By quarter

| FY26 quarter | Records | Churned | Record churn | Renewal ARR | Churned ARR | ARR churn |
|---|---|---|---|---|---|---|
| Q1 (Feb to Apr 2025) | 65 | 17 | 26.2% | $1.87M | $0.77M | 40.8% |
| Q2 (May to Jul) | 89 | 10 | 11.2% | $2.51M | $0.22M | 8.8% |
| Q3 (Aug to Oct) | 102 | 44 | 43.1% | $3.46M | $0.68M | 19.7% |
| Q4 (Nov 2025 to Jan 2026) | 92 | 16 | 17.4% | $5.31M | $0.46M | 8.6% |

## What the baseline shows

- **Logo churn exceeds ARR churn by 9 points**, so churn falls more on small accounts than large ones. Churned records average $24K of Renewal ARR against $42K for renewed ones. Twenty of the 87 churned records are $1,096 or less, the partner long tail.
- **ARR churn is concentrated.** One account, Holloway Defense ($365K, Q1), is 17% of all FY26 churned ARR and is the reason Q1 shows 40.8%. The three largest churned accounts make up 31%. A few accounts will swing the FY27 number, so the forecast needs account-level review of its largest renewals, not just a rate.
- **Q3 lost 44 of 102 records**, the most in any quarter, but at 19.7% of ARR because they were smaller accounts.

---
Source: `analysis/11_ex2a_baseline.py` → `outputs/11_ex2a_baseline.csv`, `11_ex2a_by_quarter.csv`. Hygiene decisions: H15 (Renewal ARR), H21 (logo = account), H30 and open rows (excluded, sensitivity shown).
