"""Keyword categories for CSM Health Note and Latest Gong Call Highlight (Ex 2B-2D).

Renewal rows only (the text is meaningless on new-business rows, hygiene H19).
Each text is matched against every rule; a row can carry several categories.
Rules were written by reading every distinct phrase on renewal rows (176 notes, 160 highlights).
"""
import re

import pandas as pd

RISK = {
    "Champion loss": r"champion (was let go|gone)|lost the executive sponsor|exec sponsor left|sponsor who drove this|"
                     r"person who bought this is gone|champion left|moved internally|turned over|attrition has taken|"
                     r"two are gone|people who understood the value have moved on|renewal owner change|no one above me|"
                     r"nobody has picked it up|lacks organizational influence|out of political capital|don't control the money|"
                     r"not my decision|get to my boss|only one advocating|can't win it on my own|can't fight for it alone|"
                     r"isn't\. *$|it isn't\.|where the yes has to come from|without someone senior",
    "Budget pressure": r"budget approval is slow|pricing concerns|minimum license commitments|financial distress|survival mode|"
                       r"keeping the lights on|non-essential is frozen|surviving this budget cycle|line item is going to get questioned|"
                       r"cut tooling spend|take 20% out|cutting any saas|budget i'd renew this out of doesn't exist|"
                       r"can't promise the budget|reviewing all (saas spend|subscriptions)|auditing every subscription|"
                       r"make it through the cuts|roi in writing|documented return|savings written down|quantified i can hand|"
                       r"results i can point to|defend the spend|hard numbers|no new commitments|roi .{0,15}in writing",
    "Competitive displacement": r"competing (solution|platform)|different mes vendor|evaluating an alternative|pitch that overlaps|"
                                r"other vendors is claiming|\[competitor\]|platform they already own|didn't make the cut|"
                                r"mandated one platform|picked the incumbent|legacy vendor|their own platform|standardised elsewhere|"
                                r"different stack|existing tooling|consolidate vendor stack",
    # "new owner has" (not "new owner"): "New owner is non-technical" is a champion change, not M&A
    "M&A / ownership change": r"acquired|acquisition|acquiring|m&a|merger|new ownership|new owner has|parent company|transaction|"
                              r"deal closes|restructuring",
    "Adoption / value gap": r"pilot never went live|never really got it off the ground|never got past the first use case|pilot stalled|"
                            r"adoption pocketed|plateaued|unmet expectations|unresolved support tickets|never staffed|"
                            r"didn't put the resources|logins dropped|haven't logged in|nobody's touched it|seats aren't being used|"
                            r"reduce the license count|over-provisioned|right-size|smaller footprint|smaller version|trim the seats|"
                            r"come down on quantity|licenses we're not fully using|licenses versus active users|seat utilisation|"
                            r"seat count|look at our usage|attention it deserves|firefighting|no oxygen|slipped down the list|"
                            r"underwater|haven't driven this|strategic narrative weakened|same value pitch|new use case|"
                            r"same deck won't work|identical to last renewal|recall and the audit|view tulip as optional",
    "Customer business change": r"lost their major end-customer|layoffs|winding down|de-prioritized|rough year operationally",
    "Explicit churn intent": r"likely churn|expecting churn|won't be renewing|don't think we'll be renewing|can't justify another year|"
                             r"can't defend renewing|renewing would just repeat|being phased out|being migrated|folded into|"
                             r"going in a different direction|out of my hands|we don't get a vote|don't see tulip surviving|"
                             r"don't think this makes it through|don't think i win|recommending downsell or churn",
}
POSITIVE = (r"no issues|went well|budget approved|budget is locked|renewal looks straightforward|essentially a formality|"
            r"strong adoption|expansion likely|expanding into|multi-year|stable retention|no flags|renewal is a given|"
            r"not renewing isn't on the table|we're renewing|renewal is not a question|just need the paperwork|"
            r"send (it|the order form|us the paperwork)|good to go|all set|nothing chang|same as last year|no concerns|"
            r"on track|second site|other plants|sister sites|group standard|global template|reference architecture|"
            r"need (more seats|licenses)|another \d+ (seats|operators)|additional \d+ seats|licenses for another|"
            r"through it|settled down|less worried|internal politics|green light|approved|signed off")

# One-off CSM notes that say an earlier risk flag was stale or overstated (de-escalation)
STALE_FLAG = (r"assumed the worst|never in scope|inclined to discount|still bought in|resolved inside a week|"
              r"nothing about the deployment changed|no evaluation ever opened|does not touch it|historically these unstick|"
              r"adoption metrics never dipped|forwarded it to us unprompted|seasonal in prior years|still logging in daily|"
              r"renewal is probably fine|she is not going anywhere|acquirer runs no competing platform|stepped up cleanly")
# One-off CSM notes that are genuinely two-sided
UNCERTAIN = r"mixed signals|too early to call|hard to read|cannot guarantee the budget"

_risk = {k: re.compile(v, re.I) for k, v in RISK.items()}
_pos = re.compile(POSITIVE.replace("(", "(?:"), re.I)
_stale = re.compile(STALE_FLAG, re.I)
_unc = re.compile(UNCERTAIN, re.I)


def categorize(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return [k for k, rx in _risk.items() if rx.search(text)]


def add_text_signals(r: pd.DataFrame) -> pd.DataFrame:
    """Adds per-source categories and a combined text signal: 'Risk', 'Positive' or 'Neutral'.
    Also 'note_stale_flag' (CSM says an earlier flag was stale) and 'note_uncertain'."""
    r = r.copy()
    note = r["CSM Health Note"].fillna("")
    r["note_stale_flag"] = note.str.contains(_stale)
    r["note_uncertain"] = note.str.contains(_unc) & ~r["note_stale_flag"]
    # A note that says an earlier flag was stale is a de-escalation: its risk words don't count
    r["note_cats"] = [[] if stale else categorize(t) for stale, t in zip(r["note_stale_flag"], r["CSM Health Note"])]
    r["gong_cats"] = r["Latest Gong Call Highlight"].map(categorize)
    r["text_cats"] = [sorted(set(a) | set(b)) for a, b in zip(r["note_cats"], r["gong_cats"])]
    note_pos = r["CSM Health Note"].fillna("").str.contains(_pos)
    gong_pos = r["Latest Gong Call Highlight"].fillna("").str.contains(_pos)
    r["note_signal"] = ["Risk" if c else ("Positive" if p else "Neutral") for c, p in zip(r["note_cats"], note_pos)]
    r["gong_signal"] = ["Risk" if c else ("Positive" if p else "Neutral") for c, p in zip(r["gong_cats"], gong_pos)]
    r["text_signal"] = ["Risk" if c else ("Positive" if (a == "Positive" or b == "Positive") else "Neutral")
                        for c, a, b in zip(r["text_cats"], r["note_signal"], r["gong_signal"])]
    return r
