# Exercise 1D: What this data can't tell us

## 1. Whether FY26's net-new win rate is final, and comparable to FY25

**The gap.** 44 net-new deals with FY26 close dates are still Open. All of them are 90 or more days past their close date (median 152 days at the 1 May 2026 snapshot), and 43 sit at 1 Discovery with a 10% probability. If they are dead, FY26 is 6.1%, not 8.1%, and the trend reverses from slightly up to slightly down. The file can't say which, because it holds only each deal's current stage. It has no stage history, no last-activity date and no record of where a lost deal stopped. We can't tell whether FY26 closed fewer deals because demand fell, qualification tightened, or reps stopped closing out dead opportunities. Each of those changes the denominator, and with only 11 to 14 net-new wins a year, any change under about 5 points is indistinguishable from chance.

**Data to close it:**
- Salesforce opportunity field history: the date each deal entered each stage, and every close-date change.
- Last-activity date per opportunity, so stale deals can be identified and closed out under one rule applied to both years.
- Closed net-new opportunities for FY22 to FY24, so that a 1- or 2-point change can be told apart from noise.

## 2. Why net-new deals are won or lost, and therefore what the money should back

**The gap.** The board plan is to fund whatever drove the result. The file records outcomes but not causes. Of 311 net-new losses across FY25 and FY26, 58% are coded "No Decision / Non-Responsive" (39%) or "Change in priorities" (20%). Only 6% name a competitor and 8% name feature fit. There is no sales activity, campaign or partner-touch data. The file shows patterns it can't explain. BDR Outbound sourced 75 closed net-new deals and won none. Eco-sourced deals won 10 of 71 (14%), about twice the Marketing rate (11 of 151, 7%). We can't tell whether BDR leads are poorly qualified, handed off badly, or later recorded under another source. We also can't tell whether the Eco advantage comes from the partner relationship or from the kind of account partners bring.

**Data to close it:**
- Campaign and touch history on each opportunity: first touch, last touch, and which partner was involved and when.
- A required, specific loss reason on Closed Lost, with a competitor field, plus a stage-at-loss field so qualification failures can be separated from late losses.
- Fifteen to twenty structured win/loss interviews on FY26 net-new deals, split across BDR, Marketing and Eco sources.

---
Source: `analysis/10_ex1d_gaps.py` → `outputs/10_ex1d_loss_reasons.csv`, `10_ex1d_source_outcomes.csv`. Net-new definition as in 1A.
