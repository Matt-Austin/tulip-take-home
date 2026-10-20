# Tulip GTM Operations Take-Home — Matt Austin

Analysis for the Revenue Strategy & Data Analytics Lead take-home exercise.

## Contents
| Path | What |
|---|---|
| `GTM_Operations_Take_Home.pdf`, `GTM_Context_Data_Dictionary.pdf` | The brief and its appendix |
| `CLAUDE.md` | Working instructions and data rules used throughout. This is the AI setup. |
| `analysis/` | Reproducible Python scripts, one per step |
| `outputs/` | Numbers files (mirrored to Google Sheets), commentary, Ex 3 recommendation |
| `AI_LOG.md` | Tools used, key prompts, and where AI output was checked or overridden |
| `TIME_LOG.md` | Time spent vs the 3–4 hour budget |

## Reproduce
```bash
pip install -r requirements.txt
# place the dataset at data/GTMO_Take_Home_Dataset.xlsx (not committed)
python analysis/01_inventory.py
python analysis/02_ex1_winrate.py
python analysis/03_ex2_renewals.py
```

## Deliverables
- Numbers workbook (Google Sheets): _link_
- Ex 3 recommendation: _link_
