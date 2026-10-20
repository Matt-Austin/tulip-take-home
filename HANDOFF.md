# Handoff to Claude Code

## Status
- [x] Brief and data dictionary read; requirements captured in `CLAUDE.md`
- [x] Repo scaffolded
- [ ] Dataset placed at `data/GTMO_Take_Home_Dataset.xlsx`
- [ ] `git init` and private GitHub repo created
- [ ] Ex 1 / Ex 2 / Ex 3

## Suggested first prompt
> Read CLAUDE.md and both PDFs. Then build `analysis/common.py` and `analysis/01_inventory.py`: load the dataset and print row counts by Opportunity Record Type × Deal Type × Stage × Won/Lost × Close FY. Also print the distinct values of Company Size (Employees) and where Renewal ARR, Health and the text fields are populated on non-renewal rows. Don't compute any win rates yet. Propose the new-business definitions for Ex 1A with counts, and stop for my decision.
