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
