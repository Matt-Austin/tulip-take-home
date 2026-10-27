# Exercise 1B: Decompose the change

**Bottom line:** The board's +9.0-point improvement is +10.1 points from what was counted and −1.1 points from performance. Cohorts did not convert better. Expansion converted worse, and records that are not sales outcomes account for more than the entire gain.

## Population and segments

The decomposition uses the board's own population: every New Opportunity row marked Won or Lost, by Close FY (25 / 265 = 9.43% in FY25, 36 / 195 = 18.46% in FY26, +9.03 points). Every row falls into one of four segments:

| Segment | What it is | FY25 rows (won) | FY26 rows (won) | FY25 share | FY26 share | FY25 win rate | FY26 win rate |
|---|---|---|---|---|---|---|---|
| Initial Deployment | First deployments, sales stages, not duplicates | 208 (15) | 138 (11) | 78.5% | 70.8% | 7.2% | 8.0% |
| Expansion | Expansions, sales stages, not duplicates | 27 (10) | 26 (6) | 10.2% | 13.3% | 37.0% | 23.1% |
| Order entries + admin | Stage = Ordered / Won (18) or GTM Ops Review (1). Recorded as won by definition | 0 | 19 (19) | 0.0% | 9.7% | — | 100% |
| Duplicate records | Loss Reason = Duplicate. Recorded as lost by definition | 30 (0) | 12 (0) | 11.3% | 6.2% | 0% | 0% |
| **Total** | | **265 (25)** | **195 (36)** | | | **9.43%** | **18.46%** |

The last two segments are not sales outcomes. Their win rates are fixed by how they were recorded, so any effect they have is purely about what is being counted.

## Method

Shift-share with midpoint weights, so the parts add to the total exactly with no residual:

- **Mix (what is being counted)** = (FY26 share − FY25 share) × (segment's average win rate − 13.95%)
- **Performance (cohorts converting better)** = segment's average share × (FY26 win rate − FY25 win rate)

13.95% is the average of the two blended rates. Measuring mix against it credits each segment for being above or below the blend and does not change the totals. Order entries did not exist in FY25, so they have no rate change and contribute through mix only.

## Result

| Segment | Mix (pts) | Performance (pts) | Total (pts) |
|---|---|---|---|
| Initial Deployment | +0.49 | +0.57 | +1.06 |
| Expansion | +0.51 | −1.64 | −1.13 |
| Order entries + admin | **+8.39** | 0.00 | +8.39 |
| Duplicate records | +0.72 | 0.00 | +0.72 |
| **Total** | **+10.10** | **−1.08** | **+9.03** |

**Arithmetic for the largest terms:**
- Order entries, mix: (9.7% − 0.0%) × (100% − 13.95%) = +8.39 pts
- Duplicates, mix: (6.2% − 11.3%) × (0% − 13.95%) = +0.72 pts
- Expansion, performance: 11.7% average share × (23.1% − 37.0%) = −1.64 pts
- Initial Deployment, performance: 74.6% average share × (8.0% − 7.2%) = +0.57 pts

**Check:** +10.10 + (−1.08) = +9.03 = 18.46% − 9.43%.

## What it means

- **What was counted: +10.1 points.** Nineteen order entries and admin records counted as FY26 wins add 8.4 points on their own. Fewer duplicates in the FY26 denominator add 0.7. Together, non-sales records account for +9.1 points, which is all of the reported improvement.
- **Genuine performance: −1.1 points.** Initial Deployment converted slightly better (+0.6), within normal variation. Expansion converted worse (37% to 23%, −1.6). Neither motion improved enough to explain any of the headline.
- **The two sales motions together: −0.1 points.** The CRM recorded the same sales performance in both years. The headline changed because of what was counted.

---
Source: `analysis/08_ex1b_decomposition.py` → `outputs/08_ex1b_decomposition.csv`. The script asserts that the segments cover every board row and that mix plus performance equals the total.
