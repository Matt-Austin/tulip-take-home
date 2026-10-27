# Exercise 1A: Verify the claim

**Bottom line:** The board's win rate doubled because of what it counted, not because more customers bought. Counting net-new clients only, the win rate was 7.0% in FY25 and 8.1% in FY26. That is flat. The CRO should be shown the net-new number.

## 1. What counts as a new-business deal

A **net-new client deal**: a first-time sale to a company that is not already a Tulip customer.

- Opportunity Record Type = New Opportunity
- Deal Type = Initial Deployment **and** New Logo vs. Existing = New (both fields must agree)
- Closed through the sales stages: Closed Won or Closed Lost
- Losses marked Loss Reason = Duplicate excluded (a duplicate record is not a lost deal)
- Year = fiscal year of the Close Date (Feb to Jan)

**Why this is the right definition for this decision.** The plan is to put more money behind whatever drove the improvement. That money goes into acquisition: marketing, BDRs and AE capacity aimed at new logos. Expansions, hardware and web orders, and admin records are won through different motions, by different owners, at very different odds. Blending them in hides whether the acquisition engine improved, which is the thing the money would be buying. This is also the standard SaaS meaning of new-business win rate.

## 2. Won, lost and win rate under that definition

| | Won | Lost | Win rate |
|---|---|---|---|
| FY25 | 14 | 187 | **7.0%** |
| FY26 | 11 | 124 | **8.1%** |

+1.2 points on 201 and 135 closed deals. A change this size is within normal variation (Fisher exact test, p = 0.68).

If the 44 net-new deals that are still Open with an FY26 close date (mostly at 1 Discovery) are dead, FY26 falls to 6.1% (11 won / 168), below FY25.

## 3. Other definitions and what they produce

| Definition | FY25 | FY26 | Change |
|---|---|---|---|
| **Board, as reported:** every New Opportunity row marked Won or Lost | 25 / 240 = 9.4% | 36 / 159 = 18.5% | +9.0 pts |
| **Net-new clients** (primary) | 14 / 187 = 7.0% | 11 / 124 = 8.1% | +1.2 pts |
| **Sales-led new business:** net-new plus expansions at existing customers, same stage and duplicate rules | 25 / 210 = 10.6% | 17 / 147 = 10.4% | −0.3 pts |

The board definition is the only one of 20 tested combinations that reproduces the roughly 9% and 19% in the deck. It takes the CRM's Won/Lost field at face value. The board's 36 FY26 wins are made of:

| Board FY26 wins | Count |
|---|---|
| Net-new client wins | 11 |
| Expansions at existing customers | 6 |
| Ordered / Won order entries (one owner, created and closed the same day, no ARR) | 18 |
| GTM Ops Review (admin stage) | 1 |
| **Total** | **36** |

Its denominator also counts 42 duplicate records as losses (30 in FY25, 12 in FY26).

The sales-led definition is the broadest defensible reading of new business: every deal a rep competed for. It removes only records that are not sales outcomes, and on its own that turns the board's +9 points into a slight decline.

## 4. Which number the CRO should see

The definitions disagree on direction: the board's number rises 9 points, sales-led falls slightly, and net-new is flat. **Show the CRO the net-new win rate, 7.0% in FY25 and 8.1% in FY26.** It measures what the proposed spend would buy. The board's improvement comes almost entirely from 18 order entries recorded as wins in FY26, and funding "whatever drove it" would fund a recording change, not a sales motion. The rest of Exercise 1 uses the net-new definition. Expansion is reported separately: 40.0% in FY25 and 28.6% in FY26, on 25 and 21 closed deals, too few to call a trend.

*Not used:* counting by the year an opportunity was created gives 8.0% and 10.4%, but 130 of the FY26-created net-new deals are still open. That rate reflects the deals that closed fastest and cannot be read until the rest close.

---
Sources: `analysis/07_ex1a_definitions.py` (all win rates and the FY26 breakdown), `analysis/04_board_backtest.py` (20-combination backtest), `analysis/05_ex1a_newlogo_expansion.py` (p-value, expansion rate). Outputs in `outputs/07_*.csv`, `04_*.csv`, `05_*.csv`.
