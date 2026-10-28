"""Ex 3 presentation narrative (v2): recommendation-heavy, with slide citations.
Builds the Google Docs batchUpdate requests that replace the narrative doc's body in place.
Run: python outputs/ex3_presentation_narrative.py <end_index> > requests.json
"""
import json
import sys

# (style, text); style: T=title, H1, H2, P=body, E=evidence note (bold label), X=transition (italic label)
DOC = [
    ("T", "Presentation narrative: GTM Operations take-home"),
    ("P", "Speaker script for the 20-minute presenting slot, in the deck's current order. About 15½ minutes go on the recommendation. The win-rate and renewal sections are a fast back-up pass, because their numbers have already been used and cited by slide number during the recommendation. Planned run time is 19:00, leaving a minute of buffer."),
    ("P", "Run time: Opening 0:45. Recommendation 15:30. Win rate 1:20. Renewals 1:05. Close 0:20."),
    ("P", "Evidence lines are for you, not to read aloud. They name the back-up slide and figure so you can jump to it if the panel asks."),

    ("H1", "Opening (0:45)"),
    ("H2", "Slide 1. Title (0:20)"),
    ("P", "Thanks for the time. I'm going to give you one recommendation for FY28 and spend most of my time on it: what changes, who owns it, what it costs, and how we'd know in one quarter if I'm wrong. The win-rate and renewal analysis is behind it, and I'll point to it as we go."),
    ("H2", "Slide 2. Agenda (0:25)"),
    ("P", "The recommendation first. Then a quick pass through win rate and renewals, which is where the numbers come from. I'll cite those slides by number as I use them, so you can ask me to jump to any of them."),

    ("H1", "01. Recommendation (15:30)"),
    ("H2", "Slide 3. Section divider: The Recommendation (0:15)"),
    ("P", "Short version: stop funding outbound and put that capacity on the renewals we are about to lose."),

    ("H2", "Slide 4. The recommendation (2:30)"),
    ("P", "From November, move every at-risk renewal over $100K to a save pod: a senior AE plus the account's CSM. Fund it by stopping BDR outbound."),
    ("P", "The number I'd put in front of the board is 2.2 times. Our FY27 churn forecast is $3.5M in the medium case. All eleven net-new deals we won in FY26 brought in $1.6M of new ARR. On today's course we lose more than twice what new business added last year."),
    ("E", "Evidence: slide 20, FY27 churn $3.5M medium, range $2.5M to $4.8M. Slide 13, FY26 net-new 11 won, 124 lost, 8.1%."),
    ("P", "Three findings drive the call. First, new business isn't improving: net-new win rate is 8.1%, not the 19% in the board pack. Second, the outbound motion we fund for acquisition won none of its 75 closed net-new deals. Third, who owns a renewal matters: renewals on the renewal desk lost 44% of their ARR last year, AE-owned renewals lost 2%."),
    ("E", "Evidence: slide 13, board definition 9.4% to 18.5% vs net-new 7.0% to 8.1%. Slide 17, BDR 0 of 75 closed net-new deals. Slide 6, desk vs AE churn."),
    ("P", "I looked at the obvious alternative, which is to fix acquisition by shifting mix toward Enterprise. It's worth about $57K a year. The renewal side is worth more than seven times that: just holding FY27 churn at FY26's 16.2% keeps about $0.4M, more than a quarter of what net-new added."),
    ("E", "Evidence: slide 16, mix lever +0.3 pts, $57K a year, all-Enterprise ceiling 9.8%. Slide 19, FY26 ARR churn 16.2%."),
    ("X", "Transition: Let me take the three numbers in turn."),

    ("H2", "Slide 5. Why renewals (2:00)"),
    ("P", "Left to right. $3.5M is what we expect to lose in FY27, somewhere between $2.5M and $4.8M. $1.6M is everything FY26's net-new wins added, at an 8.1% win rate. And 0 of 75 is outbound's net-new record across two years."),
    ("P", "The comparison isn't renewals good, new business bad. It's where the next dollar of effort returns more this year. The renewal number is bigger, it's nearer, because most of it closes in Q4, and the accounts are already named. The acquisition motion we'd be protecting by not changing hasn't produced a net-new win."),
    ("E", "Evidence: slide 20, medium and range by quarter. Slide 13, 8.1% net-new. Slide 17, BDR 0 of 75 and ecosystem-sourced at 14%."),
    ("P", "If someone pushes on the 19%: the board definition counts order entries. 18 of the 36 FY26 wins are order entries and one is an admin record. Mix explains +10.1 points of the change and performance minus 1.1, so no sales motion improved."),
    ("E", "Evidence: slide 13 for the counts, slide 14 for the decomposition."),

    ("H2", "Slide 6. Who owns the renewal (2:15)"),
    ("P", "This is the finding that says what to change, not just where to look. In FY26 the renewal desk lost 44% of the ARR it owned. AE-owned renewals lost 2%."),
    ("P", "It holds when you compare like with like. Among renewals where the notes or calls flagged risk, the desk lost 62 of 75 and AEs lost 11 of 31. Among renewals of $50K or more, the desk lost 9 of 18 and AEs lost none of 37. So it isn't only that the desk carries the small accounts."),
    ("P", "The limit, stated up front: ownership is inferred from each owner's book, and the hardest accounts may be routed to the desk on purpose. If so, moving them won't help. That is Risk 1 on slide 11, and it has a tripwire that reads within a quarter."),
    ("E", "Evidence: owner roles from scripts 02 and 17 (desk = owners with 80%+ renewals in their book). Risk text definition matches slide 21's rule. FY26 overall churn for context: slide 19, 16.2% of ARR, 24.1% of logos."),

    ("H2", "Slide 7. Where the money is (1:45)"),
    ("P", "Seventeen open renewals over $100K have risk language in the CSM note or the Gong call. Together they hold $5.4M. Twelve of them close in Q4, carrying $4.4M, and the desk owns fourteen of the seventeen."),
    ("P", "The four largest are on screen, all in Q4 and all with the desk. Antares Metals alone is $1.9M at 34% utilization with a competitor in the notes. Seventeen is a list a VP can review by name every week, which is the point."),
    ("E", "Evidence: slide 20, Q4 carries $2.1M of the $3.5M medium forecast. Slide 21, the rule for when text overrides the structured fields. Full list: outputs/17_ex3_pod_accounts.csv."),

    ("H2", "Slide 8. Funding (1:30)"),
    ("P", "The plan needs no new hires. Six senior AEs from the 51-person AE team lead the seventeen pods, about three accounts each. Each account's existing CSM joins its pod. BDRs move off outbound and onto booking value reviews for pod accounts, so their time goes to accounts we already have."),
    ("P", "On budget, the BDR outbound program line, meaning tools, data and sequences, moves to renewals and pays for professional-services rescue work on pod accounts. The export doesn't carry those dollar amounts, so Finance confirms the size in week one. I'd rather say that than invent a number."),
    ("E", "Evidence: slide 17, BDR 0 of 75 is why that line is the one to move. Slide 16, the acquisition alternative is worth $57K a year."),

    ("H2", "Slide 9. Stop and start (1:45)"),
    ("P", "Three stops, each with an owner. BDR outbound stops from 1 November, owned by the VP of Marketing. Health stops being used in forecast calls this quarter, owned by the VP of Customer Success, because accounts marked At-Risk churned 0 of 36 last year. And the blended win rate comes out of the board pack at the next meeting, owned by the CRO, replaced by the net-new rate."),
    ("E", "Evidence: Health 0 of 36 is from the Ex 2F workings (script 16), not on a slide. Slide 21, Health never breaks a tie. Slide 13, the net-new rate that replaces the blended one."),
    ("P", "Two starts. Save pods on the seventeen renewals, live by 15 November, owned jointly by the VP of Sales and the VP of CS. And a weekly risk review of all 143 open renewals with risk language in the notes, $7.6M of ARR, owned by RevOps and paid for from the BDR program line."),
    ("E", "Evidence: slide 20, the forecast those 143 renewals feed. Slide 21, how text is read when it conflicts with the fields."),

    ("H2", "Slide 10. 90 days and one year (1:45)"),
    ("P", "The next 90 days are FY27 Q4. Pods live by 15 November, the budget moved, and a target of Q4 churn at or below $1.4M, which is our low case, against a medium forecast of $2.1M."),
    ("E", "Evidence: slide 20, Q4 low $1.4M, medium $2.1M, high $3.0M."),
    ("P", "Then a quarter at a time. FY28 Q1: desk renewals over $50K move to AE plus CSM coverage, and we turn on stage history and required loss reasons, which closes both data gaps. Q2: the same six AEs work the $1.8M pursuable expansion list, targeting $0.5M booked. Q3: a partner-sourced acquisition pilot from what's left of the BDR line, aiming at a 10% net-new win rate. Q4: FY28 ARR churn at or below 16%, against 18.4% forecast for FY27, and a decision on the desk model."),
    ("E", "Evidence: slide 17, the two data gaps Q1 closes. Slide 19, $2.5M expansion of which $1.8M pursuable. Slide 15, Enterprise 9.8% is the best segment today, so 10% is a stretch, not a given. Slide 20, 18.4% forecast."),

    ("H2", "Slide 11. Two ways this could be wrong (1:45)"),
    ("P", "Risk 1: ownership tracks risk rather than causing it. If the desk simply receives the accounts that were going to churn anyway, moving them to AEs won't change the outcome. Tripwire: pods retain under 40% of at-risk ARR by 31 January. For reference, last year the desk kept 17% of that ARR and AEs kept 65%. We'd see it in the weekly RevOps save report. If it trips, we revert the pods and keep the weekly triage."),
    ("P", "Risk 2: the notes overstate risk months ahead of the renewal. Tripwire: Q4 at-risk renewals lose under 15% of their ARR by 31 January, against a model range of 25% to 53%. That would mean the text signal is too noisy to staff against, and we scale the pods back."),
    ("E", "Evidence: slide 20, the weakest cell is Q4 risk text with healthy usage, a 25% rate on 20 FY26 records, which is exactly what Risk 2 tests. Slide 21, accounts where the text was wrong in each direction."),
    ("P", "Both read inside one quarter. That's why the plan starts in November rather than at the start of FY28."),
    ("X", "Transition: The next two sections are the evidence I've been citing. I'll move quickly; stop me on any slide."),

    ("H1", "02. Win rate (1:20, back-up pass)"),
    ("H2", "Slide 12. Section divider: Win rate (0:05)"),
    ("P", "Did new-business win rate double? No."),
    ("H2", "Slide 13. The board number vs net-new (0:15)"),
    ("P", "Board definition 9.4% to 18.5%; net-new clients 7.0% to 8.1%, 11 won and 124 lost. Supports slides 4 and 5."),
    ("H2", "Slide 14. Mix vs performance (0:15)"),
    ("P", "Mix +10.1 points, performance minus 1.1; order entries and admin records alone add 8.4. Supports slide 5."),
    ("H2", "Slide 15. Segments against plan (0:15)"),
    ("P", "Enterprise 9.8% vs 15% plan; Mid-Market 6.8% vs 35%; SME 8.2% vs 10%. Plan rates are comparison only. Supports the slide 10 target."),
    ("H2", "Slide 16. Sizing the mix lever (0:15)"),
    ("P", "Shifting 10 points of deals to Enterprise: 8.1% to 8.4%, $57K a year. Supports slides 4 and 8."),
    ("H2", "Slide 17. What the data can't tell us (0:15)"),
    ("P", "44 net-new deals open past close (6.1% if dead); 58% of losses say No Decision; BDR 0 of 75. Supports slides 5, 8 and 10."),

    ("H1", "03. Renewals (1:05, back-up pass)"),
    ("H2", "Slide 18. Section divider: Renewals (0:05)"),
    ("P", "Where the $3.5M comes from."),
    ("H2", "Slide 19. FY26 baseline (0:20)"),
    ("P", "FY26 lost 24.1% of logos and 16.2% of ARR. FY27 expansion sizes to $2.5M across 826 seats, $1.8M pursuable. Supports slides 4 and 10."),
    ("H2", "Slide 20. FY27 churn forecast (0:20)"),
    ("P", "$2.5M to $4.8M, medium $3.5M (18.4%); Q4 $2.1M. Weakest cell: Q4 risk text with healthy usage, 25% on 20 records. Supports slides 4, 5, 10 and 11."),
    ("H2", "Slide 21. When the notes and the fields disagree (0:20)"),
    ("P", "Hawkridge Co. (text says risk), Meridian Foods and Jasperton Mechanical (text says safe). Text decides risk, utilization sets the odds, Health never breaks a tie. Supports slides 7, 9 and 11."),

    ("H1", "Close (0:20)"),
    ("H2", "Slide 22. Appendix: Definitions and filters (0:20)"),
    ("P", "Every definition and filter is here and in the workbook, and every number reruns from the scripts. The ask again: stop BDR outbound, put six senior AEs and their CSMs on the seventeen renewals, and judge it on Q4 by 31 January. Happy to take questions."),
]

STYLE = {"T": "TITLE", "H1": "HEADING_1", "H2": "HEADING_2", "P": "NORMAL_TEXT", "E": "NORMAL_TEXT", "X": "NORMAL_TEXT"}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def build(end_index):
    text = "".join(t + "\n" for _, t in DOC)
    reqs = []
    if end_index > 2:
        reqs.append({"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}})
    reqs.append({"insertText": {"location": {"index": 1}, "text": text}})
    total = 1 + u16(text)
    reqs.append({"updateParagraphStyle": {"range": {"startIndex": 1, "endIndex": total},
                 "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "fields": "namedStyleType"}})
    reqs.append({"updateTextStyle": {"range": {"startIndex": 1, "endIndex": total},
                 "textStyle": {"bold": False, "italic": False}, "fields": "bold,italic"}})
    pos = 1
    for style, t in DOC:
        n = u16(t)
        if style in ("T", "H1", "H2"):
            reqs.append({"updateParagraphStyle": {"range": {"startIndex": pos, "endIndex": pos + n + 1},
                         "paragraphStyle": {"namedStyleType": STYLE[style], "keepWithNext": True},
                         "fields": "namedStyleType,keepWithNext"}})
        elif style == "E":
            reqs.append({"updateTextStyle": {"range": {"startIndex": pos, "endIndex": pos + n},
                         "textStyle": {"italic": True}, "fields": "italic"}})
            reqs.append({"updateTextStyle": {"range": {"startIndex": pos, "endIndex": pos + u16("Evidence:")},
                         "textStyle": {"bold": True}, "fields": "bold"}})
        elif style == "X":
            reqs.append({"updateTextStyle": {"range": {"startIndex": pos, "endIndex": pos + u16("Transition:")},
                         "textStyle": {"italic": True}, "fields": "italic"}})
        pos += n + 1
    return reqs


if __name__ == "__main__":
    print(json.dumps(build(int(sys.argv[1])), ensure_ascii=False))
