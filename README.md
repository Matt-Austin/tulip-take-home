# Tulip GTM Operations Take-Home — Matt Austin

Analysis for the Revenue Strategy & Data Analytics Lead take-home. Every number in the commentary and the Exercise 3 deck reproduces from a script here, and most also recount live in the numbers workbook.

## Deliverables
| What | Where |
|---|---|
| Numbers workbook (Ex 1 and 2): start with the **Index** tab | [Google Sheet](https://docs.google.com/spreadsheets/d/1QMN-ye0lP8HNHmWVBBNg9bAO7SSHLm_QpOgmhTSz7qc/edit) |
| Ex 1 commentary (one page) | [`outputs/ex1_commentary.md`](outputs/ex1_commentary.md); detail in [`outputs/workings/`](outputs/workings/) |
| Ex 2 commentary (one page) | [`outputs/ex2_commentary.md`](outputs/ex2_commentary.md); detail in [`outputs/workings/`](outputs/workings/) |
| Ex 3 recommendation deck, with speaker notes | [Google Slides](https://docs.google.com/presentation/d/1omP4MTCa9DmfSe-9VNRYGUSPyyZmbxsNVHyvEXzY8iA/edit) |

## Reproduce
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# place the dataset (not committed) at data/GTMO_Take_Home_Dataset.xlsx
for f in analysis/[0-9]*.py; do python "$f"; done
```
Each script prints its key numbers and writes CSVs to `outputs/`. Run them in order: 02 writes the owner roles that 17 reads, and 17 reuses the 12 forecast.

## Scripts
| Script | Answers | Main output |
|---|---|---|
| `common.py` | Loading, fiscal calendar, size tiers, and every population definition (imported by all scripts) | — |
| `text_categories.py` | Keyword rules for the CSM note and Gong highlight risk categories | — |
| `01_inventory.py` | Row counts by record type, deal type, stage, outcome and year | `01_inventory_counts.csv` |
| `02_size_labels.py` | SMB vs SME label test; owner roles (renewal desk, ecosystem, AE) | `02_owner_roles.csv` |
| `04_board_backtest.py` | Which definition reproduces the board's ~9% to ~19% | `04_board_backtest.csv` |
| `05`, `06` | Ex 1A side checks: new logo vs expansion; expansion through renewals | `05_*`, `06_*` |
| `07_ex1a_definitions.py` | **Ex 1A** net-new win rate, second definition, board number | `07_ex1a_definitions.csv` |
| `08_ex1b_decomposition.py` | **Ex 1B** mix vs performance | `08_ex1b_decomposition.csv` |
| `09_ex1c_segments.py` | **Ex 1C** tier win rates vs plan, mix shift, mix lever | `09_ex1c_*.csv` |
| `10_ex1d_gaps.py` | **Ex 1D** sources, loss reasons, open deals | `10_ex1d_*.csv` |
| `11_ex2a_baseline.py` | **Ex 2A** FY26 logo and ARR churn | `11_ex2a_baseline.csv` |
| `12_ex2b_forecast.py` | **Ex 2B** FY27 churn low / medium / high by quarter | `12_ex2b_quarterly.csv` |
| `13_ex2c_text.py` | **Ex 2C** text categories and counts | `13_ex2c_categories.csv` |
| `14_ex2d_conflicts.py` | **Ex 2D** three conflict accounts | `14_ex2d_conflict_accounts.csv` |
| `15_ex2e_expansion.py` | **Ex 2E** expansion sizing, exact method | `15_ex2e_summary.csv` |
| `16_ex2f_health.py` | **Ex 2F** the field not to trust | `16_ex2f_health.csv` |
| `17_ex3_numbers.py` | **Ex 3** board number (44%), pod accounts, Risk 2 control group | `17_ex3_numbers.csv`, `17_ex3_pod_accounts.csv` |

There is no `03`; it was folded into 04 to 07.

## Process records
| File | What |
|---|---|
| `CLAUDE.md` | Working instructions and data rules given to the AI assistant (Claude Code) |
| `AI_LOG.md` | Each AI session: the prompt, what it produced, what I checked or overrode |
| `HYGIENE_LOG.md` | Data problems found, with the treatment applied to each |
| `TIME_LOG.md` | Time spent against the 3–4 hour budget |
| `outputs/ex3_presentation_narrative.py` | Source of the Ex 3 speaker notes and narrative doc |
