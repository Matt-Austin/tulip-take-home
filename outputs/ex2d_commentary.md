# Exercise 2D: Conflict accounts

Three FY27 renewal accounts where the CSM note and Gong highlight change the conclusion the structured fields would give.

## Looks fine on the numbers, and is not

**Hawkridge Co., Ltd.** ($258K Renewal ARR, FY27 Q2, open)
- **Conflict:** Utilization is 2.89 on 108 seats, so the numbers read as the account's best expansion opportunity: the Ex 2E method sizes it at 205 extra seats and $489K. Yet the CSM writes that it "hit utilization ceiling early last year, then plateaued... risk flat-to-down renewal", the customer says "The same deck won't work this year", and a second Hawkridge subscription ($38K, Q3) is being phased out after an M&A consolidation.
- **Conclusion:** Treat the $258K renewal as a downsell risk, not an expansion. It needs a new use case before renewal, and it comes off the expansion target list until it has one.

## Flagged as trouble, and the flag is wrong or stale

**Meridian Foods** ($53K Renewal ARR, FY27 Q3, open)
- **Conflict:** Utilization is 0.05 on 25 seats, far below the 0.33 retention-risk line, so the numbers mark it as one of the riskiest renewals in the book. Yet the CSM reports "Adoption metrics trending up. Multi-year renewal under discussion", and the customer says "Three sites in APAC are asking us how we did it."
- **Conclusion:** The utilization reading is wrong or out of date, so treat this as a safe renewal with multi-site expansion potential. Before relying on the usage number anywhere, check whether seats were just added or usage is being tracked under another account.

**Jasperton Mechanical** ($7K renewed in FY27 Q1; $4K still open in Q3)
- **Conflict:** Health reads Critical and utilization is 0.01 on both subscriptions. For the larger one, the CSM writes that it was "Marked At-Risk after two support escalations... both were resolved inside a week", and the customer says "We're renewing." For the smaller one, the customer "lost their major end-customer contract" and says "I haven't logged in in months."
- **Conclusion:** The text correctly separates the two subscriptions that the structured fields lump together. The larger one renewed in Q1, which confirms the Critical flag was stale. The smaller one should be planned as a churn or downsell to the floor.

---
Source: `analysis/14_ex2d_conflicts.py` → `outputs/14_ex2d_conflict_accounts.csv`. Candidates came from searching FY27 renewals for high utilization with risk text, and for low utilization, a Critical or At-Risk Health flag or an At Risk stage with no risk text (`analysis/text_categories.py`).
