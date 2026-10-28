# AI Log

Tools: Claude (claude.ai project for setup, then Claude Code for analysis), Python/pandas, Google Sheets.

## Setup (2026-10-20, claude.ai)
- Read the job posting and assessed fit against the role requirements.
- Read the brief and data dictionary, and confirmed understanding of all three exercises and the panel format.
- Wrote the working instructions (now `CLAUDE.md`), which encode the fiscal calendar, the population rules, and every data trap the dictionary calls out.
- Decided where the work lives: a private GitHub repo for the method plus Google Drive for the deliverables. The dataset is kept out of version control.

## Sessions
<!-- One entry per session -->
### YYYY-MM-DD — Ex _ / step _
- Prompt (paraphrased):
- AI output:
- What I checked / changed:

### 2026-10-20 — Inventory / Ex 1A definitions (Claude Code)
- Prompt (paraphrased): read CLAUDE.md and both PDFs; build `common.py` + `01_inventory.py`; print row counts by Record Type × Deal Type × Stage × Won/Lost × Close FY, Company Size values, and renewal-only fields on non-renewal rows; propose new-business definitions with counts; no win rates yet.
- AI output: shared loader (strips the trailing space in `Won /Lost `), fiscal-calendar helpers (Close FY reconciles to Close Date on all 1,458 rows), three candidate new-business definitions, inventory CSVs. It flagged the 18 New Opportunity `Ordered / Won` rows (FY26 only, one owner, Eco, Age 0, no ARR) and 42 `Duplicate` losses.
- What I checked / changed: chose Def1 as primary and Def0 as the comparison. SMB+SME map to the SME tier, also shown split. Coppermill GTM Ops Review is excluded (sensitivity shown).

### 2026-10-20 — Ex 1A rates (Claude Code)
- Prompt (paraphrased): use Def1 as primary and Def0 as the comparison; map SMB+SME to the SME tier; compute the Ex1A rates.
- AI output: `02_ex1_winrate.py`. Def0 reproduces the board's 9.4% → 18.5%. Def1 gives 10.6% → 10.4% (−0.3 pp). The Def0→Def1 bridge is 18 Ordered/Won + 1 GTM Ops Review + 42 Duplicate losses, with an assertion that nothing else differs. Added `size_tier()` to common.py. Drafted the Ex1A commentary.
- What I checked / changed:

### 2026-10-21 — Owner teams + size-label explainer (Claude Code, Google connectors)
- Prompt (paraphrased): create a Google Sheet copy of the dataset with a Team column next to Opportunity Owner, built from the owner/source analysis; create a Google Doc explaining the teams and the SME vs SMB label.
- AI output: copied the existing converted sheet to "GTMO Take-Home Working Data". Added Data!B Team (VLOOKUP to Owner Teams). Owner Teams has per-owner COUNTIFS, the 80% thresholds as inputs, and a low-volume flag. Team Summary and Size Label Check are all live formulas, plus a Definitions tab. Created "GTMO Take-Home Working Notes" (Doc). Verified the sheet totals against pandas: teams 51/771, 14/330, 23/357; checks = 0; SME 77/77 Sales-sourced; 25 dual-label accounts.
- What I checked / changed: _(Matt to fill)_

### 2026-10-21 — Ex 1A win rate (Claude Code)
- Prompt (paraphrased): use Def1 (sales-led) as the primary new-business definition; compute FY25/FY26 win rates under Def0/Def1/Def2 with a reconciliation and sensitivities; put live formulas in the working Google Sheet.
- AI output: `analysis/03_ex1a_winrate.py`; Sheet tab "Ex1A Win Rate" (COUNTIFS on row-level flags Data!AS:AU), reconciled to Python on every cell. Def0 reproduces the board's 9.4% → 18.5%; Def1 is flat at 10.6% → 10.4%.
- What I checked / changed: chose Def1; took the recommended defaults on H04/H05/H07 (no preference). _(Matt to add anything else he verified.)_

### 2026-10-22 — Ex 1A board backtest (Claude Code)
- Prompt (paraphrased): backtest how the board's "~9% FY25 → ~19% FY26" new-business win rate was calculated.
- AI output: `analysis/04_board_backtest.py` → `outputs/04_board_backtest.csv`. Tested 10 candidate populations × 2 year bases (Close FY, Created FY). **The backtest found exactly one definition that reproduces the board's 9% to 19%: every New Opportunity row marked Won or Lost, by Close FY (9.4% to 18.5%; 25/240 FY25, 36/159 FY26).** The next-closest candidate is more than 9 points off in total. Inside that population, 19 of the 36 FY26 wins are admin stages (18 `Ordered / Won`, 1 `GTM Ops Review`). Remove those and FY26 is 17/176 = 9.7%.
- What I checked / changed: accepted. Left uncommitted working-tree changes (which undo fd4d271) untouched, by choice.

### 2026-10-27 — Ex 2A FY26 baseline (Claude Code)
- Prompt (paraphrased): compute FY26 logo and ARR churn from the renewal cohort; bring hygiene items H15, H21, H23, H24, H30 for decisions first.
- AI output: sized each item; H23 and H24 fall in FY27 and don't touch FY26. `analysis/11_ex2a_baseline.py`: logo churn 25.1% (77/307 accounts), ARR churn 16.2% ($2.13M / $13.15M Renewal ARR), with sensitivities and a quarterly split.
- What I decided: H15 Renewal ARR as the ARR basis; H21 logo = account, churned only if every FY26 record churned; open renewals excluded with a sensitivity (17.7% if all churn). HYGIENE_LOG.md not edited because it has uncommitted changes I asked to keep.

### 2026-10-27 — Ex 2B FY27 forecast (Claude Code)
- Prompt (paraphrased): FY27 low/medium/high churn ARR by quarter, checked against FY26; bring H23/H24 and method choices first.
- AI output: keyword text categorizer (`analysis/text_categories.py`, written from every distinct note and Gong phrase on renewals); `analysis/12_ex2b_forecast.py`. Medium $4.61M (24.3%), low $3.61M (19.0%), high $5.74M (30.3%) vs FY26 16.2%. Driver: 52% of open FY27 ARR has risk text vs 34% in FY26; Q4 at 44%; Antares Metals $1.9M is the largest swing.
- What I decided: medium = utilization (<0.33) x text-risk cells calibrated on FY26; low/high = 90% Clopper-Pearson range; Health excluded (H20); Underwood Dynamics counted renewed (H24); Brightline Holdings counted churned (H23).

### 2026-10-27 — Review of Ex 1–2 and fixes (Claude Code)
- Prompt (paraphrased): re-run every component with everything learned; then apply all recommended corrections and improvements.
- AI output: logo churn 25.1% -> 24.1% (accounts with an FY27 renewal aren't churned); text-rule fixes (stale-flag notes override risk words; M&A and ROI phrasing); explicit-intent tier in 2B (FY27 medium 24.3% -> 18.4%); definitions centralised in common.py (Ex 1 outputs unchanged); one-page ex1/ex2 commentaries with detail in outputs/workings; Sheet tabs Ex1A, Ex1B, Ex1C, Ex2A, Ex2E, Ex2F live formulas and Ex2B values, all reconciled to Python.
- What I checked / changed: approved all recommendations. Time log to follow.

### 2026-10-27 — Ex 3 recommendation deck (Claude Code)
- Prompt (paraphrased): build Ex 3 in my Slides template: one recommendation, one board number, stops/starts with owners, 90-day and 1-year plan, two tripwires.
- AI output: proposed three options; I chose retention-first. Board number 2.2x (FY27 churn forecast $3.5M vs $1.6M new ARR from FY26 net-new wins). Supporting finding: FY26 desk-owned renewals lost 44% of ARR vs 2% for AE-owned (risk-text renewals: 62 of 75 vs 11 of 31). Filled all 18 template slides in a copy ("Tulip GTM Ops Exercise – Matt Austin"); template was view-only. Figures scripted in analysis/17_ex3_numbers.py.
- What I checked / changed: picked the recommendation, board number and deck format. Slide 6 chart to be inserted by hand from the Ex1B tab (connector can't link Sheets charts).

### 2026-10-27 — Ex 3 section brought to 8 slides (Claude Code)
- Prompt (paraphrased): the Ex 3 deliverable is 6–8 slides; add the four missing slides.
- AI output: four slides added after the agenda/section opener: why renewals (board number 2.2x with $3.5M vs $1.6M, BDR 0 of 75), who owns the renewal (desk 44% vs AE 2% ARR churn), where the money is (17 at-risk renewals of $100K+ = $5.4M; desk owns 14; 12 close in Q4 = $4.4M; top four listed), funding (no new hires; BDR program line moves to renewals). New figures scripted in analysis/17_ex3_numbers.py, account list in outputs/17_ex3_pod_accounts.csv.
- What I checked / changed: asked for the four slides; layout checked from rendered thumbnails (table notes shortened to one category so the callout no longer covers row four).

### 2026-10-28 — Tulip logo added to the deck (Claude Code)
- Prompt (paraphrased): add the Tulip logo (image supplied) to the deck in appropriate places.
- AI output: drew the mark from three native Slides shapes (a diamond plus two sheared rectangles, geometry measured from the supplied image) instead of uploading the image, so no Drive file or public link was needed. White on the six dark slides (large on the title, medium bottom-right on the three section dividers, small top-right on slides 2 and 8); navy (#0B1628) small top-right, aligned to the content margin, on the 16 light slides. Each mark is a group named `<slide>_logo`.
- What I checked / changed: asked for the logo; renders checked on the title, a divider, slide 2 and a light content slide.

### 2026-10-28 — Presentation narrative (Claude Code)
- Prompt (paraphrased): in a Google Doc, write a presentation narrative following the deck's new order (recommendation first).
- AI output: slide-by-slide speaker script for the 20-minute slot, with a time target per slide and transitions between sections; figures taken from the deck and the script outputs (09 segment rates, 12 quarterly forecast, 17 Ex 3 numbers). Google Doc "Tulip GTM Ops Exercise – Presentation Narrative" (id 13kEg7JdH0dvFavrXr9HNZ-WXGHL8cNZqlifNmmjuok8); source in outputs/ex3_presentation_narrative.html.
- What I checked / changed: asked for the narrative; to rehearse and adjust wording to my own voice.

### 2026-10-28 — Presentation narrative v2 (Claude Code)
- Prompt (paraphrased): rewrite the narrative to spend even more time on the recommendation, with speaker-note references (slide number and figure) to the data in the Win rate and Renewals sections.
- AI output: recommendation now 15:30 of a 19:00 plan (was 11:00); every recommendation slide has "Evidence:" notes citing back-up slides by number and figure; win-rate and renewal sections cut to a 2:25 back-up pass, each slide noting which recommendation slides it supports. Same Google Doc, replaced in place (same link). Source moved to outputs/ex3_presentation_narrative.py (builds the Docs requests); the v1 HTML was removed. One flagged citation: Health At-Risk 0 of 36 is not on any slide (Ex 2F workings).
- What I checked / changed: asked for the rewrite; to rehearse against the clock.

### 2026-10-28 — Ex 3 restructured around the brief's four asks (Claude Code)
- Prompt (paraphrased): fresh-eyes review of the deck and narrative against the Ex 3 brief (land-and-expand framing; recommendation up top; one number with its cut; stops/starts with functions, sequence and owners; two risks with tripwires). The deck should not be carved into the three exercises.
- AI output: review found (1) the 2.2x board number divides a model's medium case, which the brief rules out; (2) land-and-expand never named; (3) exercise-based sections pushed the recommendation to slide 4; (4) partner channel, pricing and per-quarter owners missing; (5) Risk 2 tripwire confounded by pod success. Changes: board number is now 44% (FY26 closed renewals, Renewal ARR basis, desk-owned vs AE-owned 2%); deck rebuilt in place as 9 main slides (title, recommendation, the number, why this lever, where it lands, stops/starts, effect on each function, sequence and owners, risks) plus an evidence divider and appendix A1-A9; agenda and exercise dividers deleted. Risk 2 now measured on a control group: 49 at-risk Q4 renewals under $100K, model loss 37%-62%, tripwire under 20% (script 17). Narrative v3 rewritten in place to match (19:00 on the main slides, evidence notes as bullets citing A1-A9).
- What I checked / changed: chose 44% as the board number and approved the restructure. My bullet formatting of evidence notes and "we funded" wording kept.

### 2026-10-28 — Slide 7 wording: BDR, value reviews (Claude Code)
- Prompt (paraphrased): use one term for the outbound team and define "value reviews" on slide 7.
- AI output: slide 7 now says BDR (matching the data's "BDR Outbound" and slide 6) and adds "Value review: AE + CSM meet the sponsor on value delivered, adoption gaps and the next team or site". Narrative doc and its source updated to match.
- What I checked / changed: asked for both edits after confirming BDRs keep their roles.
