# Exercise 1: Win rate

**The board's win rate did not double. It counted order entries as wins.** Net-new client win rate was 7.0% in FY25 and 8.1% in FY26, flat within normal variation. The proposed spend would back a recording change, not a sales motion.

## A. Verify the claim

**Definition: net-new client deals.** A first-time sale to a company that is not yet a customer: New Opportunity, Deal Type = Initial Deployment and New Logo = New, closed as Closed Won or Closed Lost, duplicate records excluded, by Close FY. The plan is to fund what drove the improvement, and that money buys acquisition. Expansions, order entries and admin records are won through different motions at very different odds, so they can't tell us whether acquisition improved.

| Definition | FY25 won / lost | FY26 won / lost | Change |
|---|---|---|---|
| **Net-new clients (primary)** | 14 / 187 = **7.0%** | 11 / 124 = **8.1%** | +1.2 pts (p = 0.68) |
| Sales-led: net-new plus expansions | 25 / 210 = 10.6% | 17 / 147 = 10.4% | −0.3 pts |
| Board: every New Opportunity marked Won or Lost | 25 / 240 = 9.4% | 36 / 159 = 18.5% | +9.0 pts |

The board definition is the only one of 20 tested that reproduces the deck. Its 36 FY26 wins are 11 net-new wins, 6 expansions, 18 Ordered / Won order entries (one owner, created and closed the same day, no ARR) and 1 admin-stage record. The definitions disagree on direction, so the CRO should see net-new: it is the number the spend would move. If the 44 net-new deals still open past their FY26 close date are dead, FY26 is 6.1%.

## B. Decompose the change

Board population, four segments covering every row, midpoint shift-share:

| Segment | FY25 → FY26 win rate | Mix (pts) | Performance (pts) |
|---|---|---|---|
| Initial Deployment | 7.2% → 8.0% | +0.49 | +0.57 |
| Expansion | 37.0% → 23.1% | +0.51 | −1.64 |
| Order entries + admin (FY26 only) | — → 100% | +8.39 | 0 |
| Duplicate records | 0% → 0% | +0.72 | 0 |
| **Total: 9.43% → 18.46%** | | **+10.10** | **−1.08** = **+9.03** |

What was counted explains more than the whole gain. Genuine performance was slightly negative.

## C. Segment mix

| Net-new by size tier | FY25 | FY26 | Plan |
|---|---|---|---|
| SME (SMB + SME labels) | 8 / 113 = 7.1% | 4 / 49 = 8.2% | 10% |
| MM | 3 / 54 = 5.6% | 3 / 44 = 6.8% | **35%** |
| ENT | 3 / 32 = 9.4% | 4 / 41 = 9.8% | 15% |

SMB and SME are one tier: the SME label appears only on Sales-sourced rows, and 25 accounts carry both. Every tier misses plan, and MM misses by 28 points. The mix has already moved: Enterprise rose from 16% to 30% of closed deals while the blended rate moved 1 point. **Moving another 10 points of mix from MM to Enterprise lifts the blended rate from 8.1% to 8.4% (+0.3 pts, about 0.4 wins a year).** Even an all-Enterprise mix reaches only 9.8%. The planning assumptions imply a 2.5-point lever pointed at the wrong tier. Segment mix is not a win-rate lever. The Enterprise case is deal size: $1.31M of new ARR from 7 wins against $0.42M from 12 SME wins.

## D. What the data can't tell us

1. **Whether FY26 is final and comparable.** 44 FY26 net-new deals are still open, 90 or more days past close, mostly at Discovery. With no stage history we can't tell if demand fell, qualification tightened or dead deals were never closed out. *Needed:* opportunity stage and close-date history, last-activity dates, FY22 to FY24 closed deals for larger samples.
2. **Why deals are won or lost.** 58% of net-new losses are coded "No Decision" or "Change in priorities"; 6% name a competitor. BDR Outbound sourced 75 closed net-new deals and won none; Eco-sourced deals won 14%. *Needed:* campaign and partner-touch history, a required specific loss reason with competitor and stage-at-loss, and 15 to 20 win/loss interviews by source.

---
Workings: `outputs/workings/ex1a` to `ex1d`; scripts `analysis/04`, `05`, `07` to `10`; definitions in `analysis/common.py`.
