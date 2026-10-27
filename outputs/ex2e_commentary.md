# Exercise 2E: Expansion sizing

**Using the fixed method exactly: 82 FY27 renewal records across 78 accounts, 826 additional seats, $2,508,467.85 of expansion ARR.**

## Method, as given

1. FY27 renewal records (Subscription Renewals, Close FY = 2027) with Utilization – 1 Month Ago greater than 1.0. All 82 qualifying records are included, whatever their stage: 58 open, 23 renewed, 1 churned.
2. Additional seats = Sold Licenses × (Utilization − 1), rounded up to whole seats.
3. Price per seat = that record's Renewal ARR ÷ its Sold Licenses.
4. Expansion ARR = additional seats × price per seat.

The rounding uses exact arithmetic. For one record, Sterling Holdings (10 seats at 1.10), the product is exactly 1 seat. Binary floating point computes it as 1.0000000000000009 and rounds up to 2, which gives 827 seats. The correct answer is 826.

## Result by fiscal quarter

| FY27 quarter | Records | Accounts | Additional seats | Expansion ARR |
|---|---|---|---|---|
| Q1 (Feb to Apr 2026) | 28 | 27 | 191 | $583,992 |
| Q2 (May to Jul) | 18 | 18 | 276 | $721,939 |
| Q3 (Aug to Oct) | 13 | 13 | 258 | $886,678 |
| Q4 (Nov 2026 to Jan 2027) | 23 | 23 | 101 | $315,860 |
| **FY27** | **82** | **78** | **826** | **$2,508,468** |

## What would make this number wrong in practice

- **Over-utilization is not purchase intent.** Utilization above 1.0 can mean shared logins or users the customer won't pay for. 42 of the 82 records have a single sold seat, and their 47 extra seats are only $90K.
- **It is concentrated.** Two records, Larkspur Dynamics ($824K) and Hawkridge ($489K), are 52% of the total.
- **Some of it may already be sold.** Larkspur Dynamics is named "Renewal and Expansion 2027", and its Total Booking is $1.77M above its Renewal ARR, so part of the expansion may already be priced into the renewal. Marigold Sciences and Thatcher & Co. show the same pattern.
- **Timing.** 23 records ($430K) have already renewed at their current seat count, so that expansion now needs a separate add-on sale before the next renewal.

## Accounts we would not pursue

| Account | Additional seats | Expansion ARR | Why not |
|---|---|---|---|
| Hawkridge Co., Ltd. | 205 | $489,194 | Usage plateaued, "the same deck won't work this year"; a second subscription is being phased out (see 2D) |
| Redwood Precision | 33 | $123,071 | Acquired by a company with a competing platform; CSM expects churn |
| Thornton Instruments | 31 | $109,169 | Consolidating its vendor stack; Tulip "on the watchlist" |
| Garrick Chemicals | 4 | $12,052 | Already churned in FY27 Q1 |
| Lochstone Components | 2 | $5,478 | Being phased out after an M&A |
| Kingsbrook Holdings | 1 | $3,013 | Financial distress; group picked another MES |
| Glenmoor Precision | 2 | $2,191 | Reviewing a competing solution |
| **Total not pursued** | **278** | **$744,168** | |

**Pursuable: 75 records, 548 seats, $1.76M of expansion ARR**, with Larkspur Dynamics, Marigold Sciences and Thatcher & Co. checked first for overlap with expansion already in their renewals. Seven accounts are excluded, but they hold 30% of the sized ARR.

---
Source: `analysis/15_ex2e_expansion.py` → `outputs/15_ex2e_summary.csv`, `15_ex2e_by_quarter.csv`, `15_ex2e_expansion_records.csv` (every record with its seats, price per seat and pursue flag).
