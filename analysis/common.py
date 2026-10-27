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
# New-business definitions (Ex 1). PRIMARY = net_new (decided 2026-10-27).
# nb_board is the as-reported comparison; nb_sales_led and nb_land are alternatives.
# Each returns closed rows only, with a boolean 'won' column.
# Treatments: H02 Ordered / Won and H04 GTM Ops Review excluded via Stage; H03 Duplicate
# losses excluded; H05 stale opens excluded (sensitivity in 07 / 10); H07 Deal Type and the
# New Logo flag must agree.
# ---------------------------------------------------------------------------

SALES_STAGES = [NB_WON_STAGE, NB_LOST_STAGE]
LOW_UTIL = 0.33  # internal retention-risk threshold (data dictionary)


def is_net_new_deal(df: pd.DataFrame) -> pd.Series:
    """Row mask, any stage: a first-time sale to a company that isn't yet a customer."""
    return (df["Opportunity Record Type"].eq(RT_NEW) & df["Deal Type"].eq("Initial Deployment")
            & df["New Logo vs. Existing"].eq("New"))


def is_expansion_deal(df: pd.DataFrame) -> pd.Series:
    """Row mask, any stage: a sales-led expansion at an existing customer."""
    return (df["Opportunity Record Type"].eq(RT_NEW) & df["Deal Type"].eq("Expansion")
            & df["New Logo vs. Existing"].eq("Existing"))


def _sales_closed(df: pd.DataFrame) -> pd.Series:
    return df["Stage"].isin(SALES_STAGES) & df["Loss Reason"].ne("Duplicate")


def net_new(df: pd.DataFrame) -> pd.DataFrame:
    """PRIMARY (Ex 1-3): net-new client deals closed through the sales stages."""
    return _closed(df[is_net_new_deal(df) & _sales_closed(df)])


def expansion(df: pd.DataFrame) -> pd.DataFrame:
    """Expansion deals closed through the sales stages, reported beside net-new."""
    return _closed(df[is_expansion_deal(df) & _sales_closed(df)])

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


def renewals(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Opportunity Record Type"] == RT_RENEWAL]


def renewal_cohort(df: pd.DataFrame, fy: int) -> pd.DataFrame:
    """Ex 2 cohort: renewal records closing in fiscal year fy. ARR basis is Renewal ARR (H15)."""
    r = renewals(df)
    return r[r["Close FY"].eq(fy)]
