"""Shared loading, fiscal-calendar helpers and population definitions.

Every exercise imports populations from here so Ex 1-3 use identical filters.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "GTMO_Take_Home_Dataset.xlsx"
OUT = ROOT / "outputs"

# Record types
RT_NEW = "New Opportunity"
RT_RENEWAL = "Subscription Renewals"
RT_HARDWARE = "Hardware and Web Orders"
RT_QUAL = "Qualification Phase"

# Stages
NB_WON_STAGE = "Closed Won"
NB_LOST_STAGE = "Closed Lost"
ADMIN_STAGES = ["GTM Ops Review", "0 With Finance", "Rejected", "Ordered / Won"]

SIZE_ORDER = ["SMB", "SME", "MM", "ENT"]
# Planning tiers. SMB and SME are one tier (<500): reps use the two labels
# interchangeably on the same account (HYGIENE_LOG H10, outputs/02_multi_label_accounts.csv).
SIZE_TIER = {"SMB": "SME", "SME": "SME", "MM": "MM", "ENT": "ENT"}
TIER_ORDER = ["SME", "MM", "ENT", "Unknown"]
PLAN_WIN_RATE = {"SME": 0.10, "MM": 0.35, "ENT": 0.15}  # comparison only, never an input


def load() -> pd.DataFrame:
    """Read the export, strip header whitespace ('Won /Lost ' -> 'Won/Lost')."""
    df = pd.read_excel(DATA)
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"Won /Lost": "Won/Lost"})
    assert len(df) == 1458, f"expected 1,458 rows, got {len(df)}"
    # Derive the calendar from dates rather than trusting CRM labels (HYGIENE_LOG H13)
    df["close_fy"] = fiscal_year(df["Close Date"])
    df["close_fq"] = fiscal_quarter(df["Close Date"])
    assert (df["close_fy"] == df["Close FY"]).all(), "Close FY label disagrees with Close Date"
    assert (df["close_fy"].astype(str) + "Q" + df["close_fq"].astype(str)).eq(df["Close FYQ"]).all()
    # Raw label stays in 'Company Size (Employees)'; blanks become 'Unknown' (H10, H11)
    df["size_tier"] = df["Company Size (Employees)"].map(SIZE_TIER).fillna("Unknown")
    return df


def fiscal_year(d: pd.Series) -> pd.Series:
    """FY runs Feb 1 - Jan 31, named for the January it ends in."""
    return d.dt.year + (d.dt.month >= 2).astype(int)


def fiscal_quarter(d: pd.Series) -> pd.Series:
    """Q1 Feb-Apr, Q2 May-Jul, Q3 Aug-Oct, Q4 Nov-Jan."""
    return ((d.dt.month - 2) % 12) // 3 + 1


def check_calendar(df: pd.DataFrame) -> int:
    """Rows where Close FY disagrees with Close Date under the fiscal calendar."""
    return int((fiscal_year(df["Close Date"]) != df["Close FY"]).sum())


# ---------------------------------------------------------------------------
# New-business definitions (Ex 1A). Def1 (nb_sales_led) is the primary, carried
# through Ex 1-3 (decided 2026-10-21). Def0 is the as-reported comparison.
# Each returns closed rows only, with a boolean 'won' column.
# Treatments: H02 Ordered/Won and H04 GTM Ops Review excluded via Stage; H03 Duplicate
# losses excluded; H05 stale FY26 opens excluded (sensitivity in 03); H07 Deal Type used.
# ---------------------------------------------------------------------------

def _closed(df: pd.DataFrame) -> pd.DataFrame:
    out = df[df["Won/Lost"].isin(["Won", "Lost"])].copy()
    out["won"] = out["Won/Lost"].eq("Won")
    return out


def nb_board(df: pd.DataFrame) -> pd.DataFrame:
    """Def 0, the as-reported population: record type New Opportunity, any closed outcome."""
    return _closed(df[df["Opportunity Record Type"] == RT_NEW])


def nb_sales_led(df: pd.DataFrame) -> pd.DataFrame:
    """Def 1, all sales-led new business: New Opportunity, Initial Deployment + Expansion,
    closed through the real lifecycle stages only (Closed Won / Closed Lost),
    excluding losses flagged as Duplicate."""
    d = df[
        (df["Opportunity Record Type"] == RT_NEW)
        & df["Deal Type"].isin(["Initial Deployment", "Expansion"])
        & df["Stage"].isin([NB_WON_STAGE, NB_LOST_STAGE])
        & df["Loss Reason"].ne("Duplicate")
    ]
    return _closed(d)


def nb_land(df: pd.DataFrame) -> pd.DataFrame:
    """Def 2, new-logo land only: Def 1 restricted to Deal Type = Initial Deployment."""
    d = nb_sales_led(df)
    return d[d["Deal Type"] == "Initial Deployment"]


nb_primary = nb_sales_led


def renewals(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Opportunity Record Type"] == RT_RENEWAL]
