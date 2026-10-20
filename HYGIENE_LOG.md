# Hygiene & Open-Questions Log

A running list of data problems and open questions. Each entry records the issue, the evidence count, which exercise it touches, and what was decided. This is a working file, not a deliverable. Only issues that move a reported number reach the commentary.

**Status:** `OPEN` = not yet decided · `PROPOSED` = a treatment is suggested and waiting on Matt · `RESOLVED` = the treatment is settled and coded in `analysis/common.py` · `PARKED` = checked, but it doesn't change any number we report

Evidence comes from `analysis/01_inventory.py` and ad-hoc checks run on 2026-10-20. Rerun after any change.

## Population & outcome

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H01 | `Won/Lost` spans both lifecycles: renewed renewals read as Won | 316 renewal Won, 108 renewal Lost | Ex1 | RESOLVED | New business = Record Type `New Opportunity` only. Renewals never enter the win rate. |
| H02 | 18 New Opportunity rows sit at `Ordered / Won`. These look like order entries, not competitive deals. | All FY26, one owner, source Eco, Age 0, no ARR, "Unnamed Account". Half of FY26's 36 "wins". | Ex1A/B | PROPOSED | Exclude from the competitive win rate (Def1). Show them as the main driver of the reported jump. |
| H03 | `Closed Lost` with Loss Reason `Duplicate` is not a real loss | FY25 30, FY26 12 | Ex1A/B | PROPOSED | Exclude from the denominator (Def1). |
| H04 | 1 `GTM Ops Review` win (Coppermill, FY26, $23K, Age 242, Commit) | 1 row | Ex1A | OPEN | Looks real. Matt to decide whether to count it as Won. Moves FY26 by 1 win. |
| H05 | 51 New Opportunity rows have FY26 close dates but are still Open (mostly `1 Discovery`). Earliest open close date is Feb 2025. | 51 rows | Ex1A/D | OPEN | Excluded from closed counts. If they're really dead, FY26's denominator is understated. Show a sensitivity and name it in 1D. |
| H06 | Hardware (35) and Qualification (12) records carry Won/Lost | 34 `Ordered / Won`, 11 `Rejected` | Ex1 | RESOLVED | Excluded by record type. |
| H07 | Deal Type vs `New Logo vs. Existing` disagree | 28 Expansion marked New; 15 Initial Deployment marked Existing; 1 New Logo blank | Ex1A/C | OPEN | Default: trust Deal Type. Matt to confirm. |
| H08 | 1 Professional Services row closed in FY2021 (Close Date 2020-12-14, created 2022) | 1 row | Ex1 | RESOLVED | Outside FY25–FY26 and an invalid date order. Ignored. |
| H09 | 2 Won rows carry a Loss Reason (`Lost to Competitor`, `No Decision`) | 2 rows | Ex1 | PARKED | Outcome follows Stage. Loss Reason isn't used for won rows. |

## Segmentation

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H10 | `Company Size` has four labels (SMB/SME/MM/ENT) vs three planning tiers. No headcount is available to reconcile them. | Closed New Opportunity, FY25: SMB 111, SME 16; FY26: SMB 47, SME 12. SME is a minority label in every geo, year and vertical. **Backtest (`02_size_labels.py`):** (1) ARR per license doesn't separate any tier. Median is about $2.9K–3.3K/license for all four labels on both renewals and new business, so it can't tell SMB from SME. (2) 25 of 72 SME accounts are labelled SMB on another row. All 25 multi-label accounts are SMB/SME pairs, never any other combination, and Geo, Industry and Region match on all 25, so these aren't anonymization name collisions. (3) New business: SMB and SME look identical (median $27,390 ARR, 9 vs 8 licenses). (4) Renewals: SMB holds a long tail of 136 tiny subscriptions (≤$1,095.60, 1–2 seats, 129 partner-generated, all Eco, mostly EMEA/APAC). SME has none of these. With the tail removed, SMB is still smaller than SME (median 2 vs 12 licenses), but SME is n=41. A web lookup of company size isn't possible because account names are anonymized. Example: Garrick Foods, same owner, labelled SMB on a renewal closed 19 Mar 2025 (Excel row 796) and SME on one closed 7 May 2025 (row 1223). | Ex1C | RESOLVED (2026-10-20) | **Treatment:** SMB and SME are mapped to one planning tier, "SME" (<500 employees), in `common.py` (`SIZE_TIER` → `size_tier`): 666 SMB + 77 SME rows. The raw label stays in `Company Size (Employees)`, and segment outputs show the SMB / SME split under the SME tier. **Stated assumption:** SMB and SME are two labels for the same tier. **Explanation:** reps use the two labels interchangeably on the same customer. All 25 multi-label accounts are SMB/SME pairs (no other combination exists), with consistent Geo, Industry and Region (see `outputs/02_multi_label_accounts.csv`). The two look identical on new business, and ARR per license doesn't separate any tier. **Mechanism found:** the SME label appears only on Sales-sourced rows: 77/77 SME rows are Reporting Source = Sales, and 0 Sales-sourced rows are SMB. Every other source labels small accounts SMB. On the 25 multi-label accounts, all 26 SME rows are Sales-sourced and all 30 SMB rows are not. So the label tracks how the opportunity was sourced, not the size of the company. **Caveat to state:** SME-labelled renewals are larger than SMB ones (median 12 vs 2 licenses, n=41), partly because of SMB's 136-row partner long tail of ≤$1,096 subscriptions. |
| H11 | `Company Size` blank on closed New Opportunity rows rises from 2 (FY25) to 19 (FY26) | 21 rows | Ex1C | OPEN | Report as an "Unknown" segment so segment counts still sum to the total. Coded as `size_tier = "Unknown"` (28 rows in all), pending Matt's sign-off. |
| H12 | `FY26 Segment` is an industry vertical, not size | per dictionary | Ex1C | RESOLVED | Never used as a size cut. |

## Calendar & timing

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H13 | Fiscal labels vs dates | Close FY / Close FYQ / Fiscal Period match on 1,458/1,458. Created FYQ and Created Quarter are each off on 1 row (Tidewater Bioworks, 31 Oct 2023 labelled Q4). | All | RESOLVED | FY and quarter are derived from the dates in `common.py`, with an assert against the labels. |
| H14 | The export snapshot is about 1 May 2026 (start of FY27 Q2), so FY27 is mostly open | Latest Created 30 Apr 2026, latest closed outcome 1 May 2026. 224/287 FY27 plain renewals are at `2 Open Renewal`. | Ex2B | RESOLVED (framing) | Ex2 FY27 is a forecast on an open book, not a measurement. |

## Money fields

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H15 | On renewals, Renewal ARR and Total Booking disagree, and the gap is partly a labelling problem | Pure `Renewal`: 124/556 differ by >1% (94 Total Booking > Renewal ARR, 30 below). `Expansion + Renewal`: 135/143 have Total Booking > Renewal ARR, which fits Total Booking including the uplift. Named terms are 11–12 months (see H21), so multi-year contracts don't explain most of the gap. Naming vs Deal Type mismatches are in H29. | Ex2A/B/E | OPEN | **Default (unchanged):** Renewal ARR is the ARR basis. **Matt's plan to separate real expansion from noise:** (1) fix the labels via H29; (2) for accounts with an FY26 Won renewal and an FY27 renewal (151 accounts match by name), compare Sold Licenses year over year. A small increase may just be headcount growth in the same team, not an expansion into a new team or site. A decrease means checking `Utilization - 1 Month Ago` for a usage problem. (3) Read the CSM Health Note and Gong Highlight on those accounts to tell new-team expansion from growth or downsell. |
| H16 | Renewal ARR is filled on non-renewal rows | 61 New Opportunity rows (14 > 0), 5 hardware rows (all 0) | Ex1/Ex2 | RESOLVED | Ignored outside the renewal record type. |
| H17 | New Committed ARR is missing on many rows, including wins | 1,033/1,458 filled. 20 New Opportunity Won rows are null or 0 (18 are the H02 rows). | Ex1/Ex3 | OPEN | Only matters if we size the new-business ARR impact. Check before quoting any dollar figure. |
| H18 | `Weighted` = Probability × New Committed ARR exactly. **How the business uses it is unknown.** | 1,033/1,033 rows match exactly | Ex2 | OPEN | Matt's working assumption, not confirmed: it lets leadership see the most impactful opportunities at a glance. It's mechanically derived from an AE-set probability, so it adds no information beyond those two fields. Not used as a predictor. Usage could be a question for the panel. |

## Renewal-specific fields

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H19 | Health, CSM Note and Gong Highlight are filled on 100% of non-renewal rows | 758/758 | Ex2C | RESOLVED | Used only on renewal rows. |
| H20 | **We can't tell when Health was set relative to the outcome** | Churned: 100/108 Critical, 8 Healthy, 0 At-Risk. Renewed / Won: 268/316 Healthy. Open renewals are more mixed. The file has no Health history or last-modified date. | Ex2B/F | OPEN | The pattern suggests Health was set near the time of the final outcome, but that's unproven. **Don't rely on Health as a predictor** unless something later tells us when it was set. A comparison of Health on open FY27 rows against FY27 closes might help. Still the leading candidate for 2F. |
| H21 | The same account appears more than once in a renewal FY | 172 renewal rows across 77 account-FY groups. Of renewal names, 348/700 state a Mon YYYY–Mon YYYY term and **all are 11–12 months** (one-year contracts). 63 use a "YYYY - YYYY" style; 289 carry no term. FY26→FY27: 156 accounts appear in both years, 151 of them renewed in FY26. 5 FY27 accounts churned in FY26. | Ex2A logo churn, Ex2B | OPEN | **Matt's read:** an annual contract showing up in the next FY's renewals is expected, not a duplicate. Read the prior record's term before treating a repeat as meaningful. Within a single FY, the repeats fall into types: (a) separate subscriptions at the same account (e.g., Copperleaf Medical, 1 vs 5 seats, same term); (b) co-terming or short terms (e.g., Forsythe Microsystems, Oct 25–Oct 26 then Jan 26–Jan 27); (c) a Won and an Open record for the same term (see H30). **Next:** classify each repeat group by term and decide what a "logo" is before computing logo churn. The 5 FY26-churn / FY27-renewal accounts need a look: partial churn of one subscription? |
| H22 | Churn reason is filled on non-churn rows | 51 Renewed / Won and 7 Open rows carry an At Risk/Churn/Downsell Reason | Ex2C | OPEN | Probably at-risk or downsell history. Don't treat it as a churn label. |
| H23 | 1 renewal record has Deal Type `Initial Deployment` (Churned) | 1 row | Ex2A | OPEN | Probably a mis-typed renewal. Default: keep it in the renewal cohort. |
| H24 | 1 renewal sits at `GTM Ops Review` (Won) | 1 row | Ex2A | OPEN | Default: count as renewed. |
| H25 | 9 Churned rows have no churn reason; 8 Churned rows are Health = Healthy | 9 / 8 | Ex2C/D | OPEN | Candidate conflict accounts for 2D. |

## Other fields (checked; not yet relevant)

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H26 | `Generated by` vs `Partner of Record` disagree in both directions | 153 Tulip-generated with a partner set; 67 Partner-generated with no partner | Ex3 (if channel) | PARKED | Only matters if the recommendation touches the partner channel. |
| H27 | `Age` vs `Opp Age Recal` disagree | 293 rows differ by >1 day (291 New Opportunity). Age = Close − Created on 939 rows; Recal on 725. | — | PARKED | Not used. If cycle time is needed, compute Close − Created directly. |
| H28 | 21 rows with blank Account Name, all "Unnamed Account" opportunities | 21 (0 are renewals; 18 are the H02 rows) | Ex1 | OPEN | Held open (Matt, 2026-10-20). Appears not to affect Ex2 logo counts. |

## Renewal labelling (added 2026-10-20)

| ID | Issue | Evidence | Affects | Status | Treatment / resolution |
|---|---|---|---|---|---|
| H29 | Opportunity Name and Deal Type disagree on expansion | 34 rows named "Renewal Opportunity + Price Increase" are typed `Expansion + Renewal` with no "expansion" in the name: a price uplift labelled as expansion. 10 rows named "Renewal and Expansion" / "Renewal + Expansion" are typed plain `Renewal`. 3 price-increase rows are typed `Renewal`. | Ex2A/B/E, Ex3 | OPEN | A price increase isn't seat or team expansion. Proposed: reclassify by name into Renewal / Renewal + price increase / Renewal + expansion, and carry both labels. Decide before any expansion-vs-renewal ARR split. |
| H30 | A Won and an Open renewal record for the same account and term | e.g., Gallowstone Materials (Mar 2026–Mar 2027, Won 25 Mar plus Open 31 Mar); Forsythe Beverages (Won Jul 25 plus Open Aug 2025–Jul 2026) | Ex2A/B | OPEN | The Open twin is likely a stale duplicate that would double-count FY27 exposure. Count across all 77 repeat groups once H21 is classified. |
| H31 | Meaning of Reporting Source `Eco` isn't documented. It isn't a standard term for Customer Success, and Tulip's public partner pages don't use it as a program name. It most plausibly means "ecosystem". | Eco is 851/1,458 rows. It covers 527 of the 535 partner-generated rows, 526/556 plain renewals, and also 189 new-logo Initial Deployments (134 of those partner-generated). By owner (rule-based roles in `outputs/02_owner_roles.csv`): 23 renewal-desk owners (≥80% renewals, 329/357 rows Eco); 14 Eco/partner owners (≥80% Eco, 319/330 rows; e.g., Ursula Mwangi: 92 renewals + 45 Initial Deployments, 84% partner-generated); 51 AEs with mixed sources own all 89 BDR and 242 of 251 Marketing rows, plus most Expansion and Expansion + Renewal. | Ex1C/D, Ex2, Ex3 | OPEN | Working read (unconfirmed): Eco = business that came through the ecosystem (partners and the existing installed base), worked by renewal-desk and partner owners. It is not a CS team label. New logos are worked by AEs off BDR, Marketing and Sales sourcing. The split holds: no renewal-desk owner works new business (6 of 357 rows). Confirm the meaning if possible. |
