# Exercise 1C: Segment mix model

**Bottom line:** Every size tier wins net-new deals at 6% to 10%. The planning assumptions overstate every tier, and Mid-Market by 28 points. Moving 10 points of mix toward the best tier, Enterprise, adds 0.3 points of win rate, about one extra win every two to three years. Segment mix is not a win-rate lever in this data.

## Population and tiers

Net-new clients, as defined in 1A: New Opportunity, Deal Type = Initial Deployment and New Logo flag = New, Closed Won or Closed Lost, duplicate losses excluded, by Close FY. Size tier comes from Company Size (Employees). SMB and SME are treated as one tier, the planning SME tier (under 500 employees). The SME label appears only on Sales-sourced rows, and 25 accounts carry both labels, so the two can't be told apart. The split is shown below so the assumption is visible.

## Measured win rate by tier vs planning assumption

| Tier | FY25 won / closed | FY25 | FY26 won / closed | FY26 | FY25+26 | Plan | FY26 gap to plan |
|---|---|---|---|---|---|---|---|
| SME (under 500) | 8 / 113 | 7.1% | 4 / 49 | 8.2% | 7.4% | 10% | −1.8 pts |
| *of which SMB label* | *8 / 101* | *7.9%* | *4 / 46* | *8.7%* | *8.2%* | | |
| *of which SME label* | *0 / 12* | *0.0%* | *0 / 3* | *0.0%* | *0.0%* | | |
| MM (500 to 5,000) | 3 / 54 | 5.6% | 3 / 44 | 6.8% | 6.1% | **35%** | **−28.2 pts** |
| ENT (over 5,000) | 3 / 32 | 9.4% | 4 / 41 | 9.8% | 9.6% | 15% | −5.2 pts |
| Unknown (blank size) | 0 / 2 | — | 0 / 1 | — | — | | |
| **Total net-new** | **14 / 201** | **7.0%** | **11 / 135** | **8.1%** | **7.4%** | | |

- **Every tier is below plan.** Mid-Market is the largest miss. The plan treats it as the best-converting tier at 35%; measured, it is the worst at 6.1% over the two years.
- **The tiers are not meaningfully different from each other.** Enterprise (7 of 73 won) against Mid-Market (6 of 98) gives p = 0.56. With 3 to 4 wins per tier per year, the ranking could reverse next year by chance.
- Applied to the FY26 mix, the planning rates imply a blended net-new win rate of 19.6%, close to the 19% in the board deck. The measured figure is 8.1%. A plan built on these assumptions will keep reading the board's number as normal.

## Mix shift of closed net-new deals

| Tier | FY25 share | FY26 share | Shift |
|---|---|---|---|
| SME | 56.2% | 36.3% | −19.9 pts |
| MM | 26.9% | 32.6% | +5.7 pts |
| ENT | 15.9% | 30.4% | **+14.4 pts** |
| Unknown | 1.0% | 0.7% | −0.3 pts |

A large shift toward Enterprise has already happened. Its share of closed net-new deals nearly doubled, yet the blended rate moved only from 7.0% to 8.1%.

## Mix model

Blended win rate = sum of (tier share × tier win rate), using FY26 measured shares and rates. Planning rates are shown for comparison only.

| Scenario | Blended win rate | Lift | Extra wins at FY26 volume (135 closed) |
|---|---|---|---|
| **Today:** FY26 mix, FY26 measured rates | **8.1%** | | |
| **Proposed:** move 10 pts of closed-deal mix from MM to ENT | **8.4%** | **+0.3 pts** | **0.4 per year** |
| Ceiling: every closed deal is Enterprise | 9.8% | +1.6 pts | 2.2 per year |
| *Plan view:* FY26 mix at planning rates | *19.6%* | | |
| *Plan view:* 10 pts from SME to MM at planning rates | *22.1%* | *+2.5 pts* | *3.4 per year* |

**The shift I'd propose:** 10 more points of closed net-new deals from Mid-Market, the lowest-converting tier, to Enterprise, the highest. That takes Enterprise from 30% to 40% of closed deals, on top of the 14-point move that has already happened. Going further means turning away most of the SME and MM pipeline.

## What this means for segment mix as a lever

The lever is small. A realistic shift adds 0.3 points, and even an impossible all-Enterprise mix adds only 1.6. The planning assumptions suggest a 2.5-point lever, eight times larger, and point it at the wrong tier. The measured gap between tiers is 3.5 points (9.6% vs 6.1%). The planning gap between MM and SME is 25 points.

The case for Enterprise, if there is one, rests on deal size, not win rate. Won Enterprise net-new deals carried $1.31M of New Committed ARR across FY25 and FY26 (7 deals, median $44.7K), against $0.42M for SME (12 deals, median $34.2K). Any reallocation should be justified on ARR per closed deal, not on conversion.

---
Source: `analysis/09_ex1c_segments.py` → `outputs/09_ex1c_tier_rates.csv`, `09_ex1c_mix.csv`, `09_ex1c_mix_model.csv`. Size-tier mapping: `analysis/02_size_labels.py` and hygiene log H10.
