"""Ex 3 presentation narrative (v3): nine-slide main deck built on the brief's four asks; evidence in A1-A9.
Builds the Google Docs batchUpdate requests that replace the narrative doc's body in place.
Two steps: "text <end_index>" replaces the body; "style <read_doc.json>" styles it from a fresh read.
"""
import json
import re
import sys

# (style, text); style: T=title, H1, H2, P=body, E=evidence note (bold label), X=transition (italic label)
DOC = [
    ("T", "Presentation narrative: GTM Operations take-home"),
    ("P", "Speaker script for the 20-minute presenting slot. The main deck is nine slides and answers the brief's four asks in order: the recommendation up top (slide 2), one number with its cut (slide 3), what stops and starts with functions, sequence and owners (slides 6 to 8), and two ways it could be wrong with tripwires (slide 9). Slides 4 and 5 say why this lever and where it lands. The Exercise 1 and 2 work sits in the appendix as A1 to A9 and is not presented; it is there for questions."),
    ("P", "Run time: 19:00 on slides 1 to 9, leaving a minute of buffer. Evidence lines are for you, not to read aloud: they name the appendix slide and figure to jump to if the panel asks."),

    ("H1", "Main deck (19:00)"),
    ("H2", "Slide 1. Title: Protect the renewal base (0:30)"),
    ("P", "Thanks for having me. One recommendation: protect the renewal base Tulip expands from, starting in November. The next eight slides are that recommendation: the number behind it, what stops and starts, who owns each piece, and how we'd know within a quarter if I'm wrong. The Exercise 1 and 2 work is in the appendix, and I'll point to it as I go."),

    ("H2", "Slide 2. The recommendation (3:00)"),
    ("P", "Starting 1 November, move every at-risk renewal over $100K, 17 accounts holding $5.4M, from the renewal desk to a save pod: a senior AE plus the account's CSM. Pay for it by stopping BDR outbound."),
    ("P", "Here is why that's the right call for a land-and-expand business. Tulip lands small in one team or site and grows by expanding into the next ones. That only works if the first renewal happens. A lost renewal costs more than its own ARR; it ends every expansion that account would have produced. So the renewal is where Tulip's growth is protected or lost."),
    ("P", "Last year the renewal desk lost 44% of the renewal ARR it owned. AE-owned renewals lost 2%. That's the number I'd put in front of the board, and the next slide shows exactly how I cut it."),
    ("P", "Meanwhile the motion we funded to land new logos isn't landing them: BDR outbound won none of its 75 closed net-new deals. Stopping it is how this gets paid for with no new headcount."),
    ("E", "Evidence: A5, BDR 0 of 75 closed net-new deals. A7, the FY27 forecast by quarter. Slide 5 for the 17 by name."),
    ("P", "If you stop listening after this slide: at-risk renewals over $100K move to AE plus CSM pods on 1 November, outbound stops, and we know by 31 January whether it worked."),

    ("H2", "Slide 3. The number: 44% (2:30)"),
    ("P", "The cut. Every FY26 renewal that closed Won or Lost, valued at Renewal ARR. I grouped owners by their book: an owner whose opportunities are 80% or more renewals counts as the renewal desk; everyone else is an AE. Renewals the desk owned lost 44% of their ARR. Renewals AEs owned lost 2%."),
    ("P", "It holds like for like. Among renewals where the CSM note or Gong call flagged risk, the desk lost 62 of 75 and AEs lost 11 of 31. Among renewals of $50K or more, the desk lost 9 of 18 and AEs lost none of 37. At the same size and the same risk signal, AE-owned accounts mostly stay."),
    ("P", "Why this number and not a bigger one: I could show $3.5M of forecast churn, but that's the medium case of a model. 44% is measured, a board member can repeat it, and it points at the one thing we'd change: who owns the renewal."),
    ("P", "What it doesn't prove is cause. The desk may simply be handed the accounts that were already leaving. That is Risk 1 on slide 9, and it has a tripwire."),
    ("E", "Evidence: owner roles from scripts 02 and 17 (no appendix slide). A6, FY26 churn overall: 16.2% of ARR, 24.1% of logos. A8, how risk language is read. A9, definitions."),

    ("H2", "Slide 4. Why this lever (2:30)"),
    ("P", "Three numbers on why the money goes to retention and not acquisition."),
    ("P", "$2.1M: renewal ARR churned in FY26. All eleven net-new wins added $1.6M. The base shrank faster than new business grew it."),
    ("P", "0 of 75: outbound's net-new record over two years. Ecosystem-sourced deals win 14% and marketing-sourced 7%, so the channel we're defunding is the weakest one."),
    ("P", "$57K: what the obvious alternative is worth. Shifting deal mix toward Enterprise, our best-converting segment, adds 0.3 points of win rate, about $57K of new ARR a year."),
    ("P", "One more signal for a land-and-expand business: the expansion win rate fell from 37% to 23%. Growth runs through the installed base, and the base is where the leakage is."),
    ("P", "If someone raises the board's 19%: that definition counts order entries. Net-new win rate is 8.1%, flat with FY25's 7.0%."),
    ("E", "Evidence: A6, $2.1M of $13.2M churned. A1, net-new 8.1% (11 won, 124 lost) vs board 18.5%. A5, BDR 0 of 75; ecosystem 14%; marketing 7%. A4, mix lever 8.1% to 8.4%, $57K, all-Enterprise ceiling 9.8%. A2, expansion 37% to 23%; mix +10.1 pts, performance minus 1.1."),

    ("H2", "Slide 5. Where it lands (1:45)"),
    ("P", "Seventeen open renewals over $100K have risk language in the CSM note or the Gong call. Together they hold $5.4M. Twelve close in Q4, carrying $4.4M, and the desk owns fourteen of the seventeen."),
    ("P", "The four largest are on screen, all in Q4 and all with the desk. Antares Metals alone is $1.9M at 34% utilization with a competitor in the notes. Seventeen is a list a VP can review by name every week, which is why I drew the line at $100K."),
    ("E", "Evidence: A7, Q4 carries $2.1M of the $3.5M medium forecast. A8, the rule when notes and fields disagree. Full list: outputs/17_ex3_pod_accounts.csv."),

    ("H2", "Slide 6. What stops, what starts (2:00)"),
    ("P", "Stops come first, because they free the money and the time. On 1 November BDR outbound stops; the VP of Marketing owns it. In Q4, Health comes out of forecast calls, owned by the VP of Customer Success: accounts marked At-Risk churned 0 of 36 last year. At the next board meeting the blended win rate comes out of the pack and the net-new rate replaces it; the CRO owns that."),
    ("P", "Then two starts. Save pods on the seventeen renewals, live by 15 November, owned jointly by the VP of Sales and the VP of CS. And a weekly risk review of all 143 open renewals with risk language, $7.6M of ARR, run by RevOps and paid for from the outbound line."),
    ("E", "Evidence: A5, BDR 0 of 75. A1, the net-new rate for the board pack. A8, how risk text is read. Health 0 of 36 is from the Ex 2F workings (script 16); no appendix slide."),

    ("H2", "Slide 7. Effect on each function (2:15)"),
    ("P", "Function by function. AEs: six senior AEs from the 51 lead the pods, about three accounts each. CSMs: each pod account's CSM joins its pod; the desk keeps renewals under $100K, so its load drops by fourteen accounts. SDRs: outbound stops, and they book value reviews for pod accounts instead."),
    ("P", "Marketing: the outbound program line, meaning tools, data and sequences, pays for professional-services rescue work on pod accounts. The export has no spend data, so Finance sizes the line in week one; I'd rather say that than invent a number."),
    ("P", "Partner channel: from FY28 Q1, ecosystem-sourced deals get the acquisition budget, because they win 14% against 7% for marketing and 0% for outbound. One caveat: the file doesn't define the Eco source, so I'm treating it as partner-sourced and would confirm that first."),
    ("P", "Pricing: no list change. Expansion seats are quoted at each account's current per-seat price, the same method that sized the $2.5M expansion opportunity."),
    ("E", "Evidence: A5, ecosystem 14%, marketing 7%, BDR 0%. A6, expansion $2.5M, 826 seats, $1.8M pursuable. Eco meaning is open item H31 in the hygiene log."),

    ("H2", "Slide 8. Sequence and owners (2:15)"),
    ("P", "The first 90 days are FY27 Q4. Pods live by 15 November, the budget moved, and a target of Q4 churn at or below $1.4M, our low case, against a medium forecast of $2.1M. Owners: VP Sales and VP CS."),
    ("P", "Then the year, a quarter at a time. FY28 Q1: if the Q4 tripwires hold, desk renewals over $50K move to AE plus CSM coverage, and the ecosystem channel takes the acquisition budget; owners VP CS and the partner lead. RevOps also turns on required loss reasons and stage history. Q2: the pods work the $1.8M pursuable expansion list and book $0.5M; VP Sales. Q3: ecosystem pipeline reviewed against a 10% net-new win rate; partner lead. Q4: FY28 ARR churn at or below 16%, against 18.4% forecast for FY27, and the CRO decides the future of the desk model."),
    ("E", "Evidence: A7, Q4 low $1.4M, medium $2.1M, high $3.0M; FY27 18.4%. A6, $1.8M pursuable. A3, Enterprise at 9.8% is the best segment today, so 10% is a stretch. A5, the two data gaps Q1 closes."),

    ("H2", "Slide 9. Where I could be wrong (2:00)"),
    ("P", "Risk 1: ownership tracks risk rather than causing it. If the desk is simply handed the accounts that were leaving anyway, moving them to AEs won't help. Tripwire: the pods retain under 40% of their at-risk ARR by 31 January. Last year the desk kept 17% of that ARR and AEs kept 65%, so under 40% means the pods look like the desk. We'd see it in the weekly RevOps save report. If it trips, we revert the pods and keep the weekly triage."),
    ("P", "Risk 2: the notes overstate risk months ahead. The test has to be outside the pods, because inside them a low loss would look like success. So I watch the 49 at-risk Q4 renewals under $100K that stay with the desk. The model expects them to lose 37% to 62% of their ARR. If they lose under 20% by 31 January, the text signal is too noisy to staff against, and we scale the pods back."),
    ("E", "Evidence: A7, the weakest forecast cell is Q4 risk text with healthy usage, a 25% rate on 20 FY26 records. A8, accounts where the text was wrong in each direction. Control-group range from script 17."),
    ("P", "Close (0:15): Stop outbound on 1 November, put six senior AEs and their CSMs on seventeen renewals from 15 November, and judge it on 31 January. Happy to take questions; the evidence is in A1 to A9."),

    ("H1", "Appendix: use if asked (not presented)"),
    ("H2", "Slide 10. Evidence divider"),
    ("P", "Only if you need to jump into the appendix: the Exercise 1 and 2 analysis behind each number."),
    ("H2", "A1. Net-new vs the board number"),
    ("P", "Board definition 9.4% to 18.5%; net-new clients 7.0% to 8.1%, 11 won and 124 lost. FY26 board wins: 18 order entries, 1 admin record, 6 expansions, 11 net-new. Backs slides 4 and 6."),
    ("H2", "A2. Mix vs performance"),
    ("P", "Of the +9.0 point change, mix explains +10.1 and performance minus 1.1. Expansion win rate 37% to 23%. Backs slide 4."),
    ("H2", "A3. Segments against plan"),
    ("P", "Enterprise 9.8% vs 15% plan; Mid-Market 6.8% vs 35%; SME 8.2% vs 10%. Plan rates are comparison only. Backs the slide 8 target."),
    ("H2", "A4. Sizing the mix lever"),
    ("P", "Shifting 10 points of closed deals to Enterprise: 8.1% to 8.4%, about $57K a year. Backs slide 4."),
    ("H2", "A5. What the data can't tell us"),
    ("P", "44 net-new deals open past close (6.1% if dead); 58% of losses say No Decision; BDR 0 of 75; ecosystem 14%. Backs slides 2, 4, 6 and 7."),
    ("H2", "A6. FY26 baseline and expansion"),
    ("P", "FY26 lost 24.1% of logos and 16.2% of ARR, $2.1M of $13.2M. FY27 expansion $2.5M across 826 seats, $1.8M pursuable. Backs slides 3, 4, 7 and 8."),
    ("H2", "A7. FY27 churn forecast"),
    ("P", "$2.5M to $4.8M, medium $3.5M (18.4%); Q4 medium $2.1M. Weakest cell: Q4 risk text with healthy usage, 25% on 20 records. Backs slides 5, 8 and 9."),
    ("H2", "A8. When notes and fields disagree"),
    ("P", "Hawkridge Co. (text says risk), Meridian Foods and Jasperton Mechanical (text says safe). Text decides risk, utilization sets the odds, Health never breaks a tie. Backs slides 5, 6 and 9."),
    ("H2", "A9. Definitions and filters"),
    ("P", "Every definition and filter, matching the workbook's Definitions tab."),
]

STYLE = {"T": "TITLE", "H1": "HEADING_1", "H2": "HEADING_2", "P": "NORMAL_TEXT", "EL": "NORMAL_TEXT", "EI": "NORMAL_TEXT"}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def paragraphs():
    """Expand DOC into (style, text) paragraphs: an evidence note becomes a bold 'Evidence:' label plus one bullet per item."""
    for style, text in DOC:
        if style == "E":
            yield "EL", "Evidence:"
            for item in re.split(r"\.\s+(?=[A-Z])", text[len("Evidence: "):].rstrip(".")):
                yield "EI", item[0].upper() + item[1:] + "."
        else:
            yield style, text


def text_requests(end_index):
    """Step 1: replace the body text (guard with the doc's revisionId)."""
    text = "".join(t + "\n" for _, t in paragraphs())
    reqs = [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}}] if end_index > 2 else []
    reqs.append({"insertText": {"location": {"index": 1}, "text": text}})
    return reqs


def style_requests(doc_paras):
    """Step 2: style from the doc as read back. doc_paras = [(startIndex, endIndex, text)] for non-empty paragraphs."""
    spec = list(paragraphs())
    assert [t for _, _, t in doc_paras] == [t for _, t in spec], "doc text differs from spec"
    first, last = doc_paras[0][0], doc_paras[-1][1]
    reqs = [{"deleteParagraphBullets": {"range": {"startIndex": first, "endIndex": last}}},
            {"updateParagraphStyle": {"range": {"startIndex": first, "endIndex": last},
             "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "fields": "namedStyleType"}},
            {"updateTextStyle": {"range": {"startIndex": first, "endIndex": last - 1},
             "textStyle": {"bold": False, "italic": False}, "fields": "bold,italic"}}]
    bullets = []
    for (st, en, _), (style, _) in zip(doc_paras, spec):
        if style in ("T", "H1", "H2"):
            reqs.append({"updateParagraphStyle": {"range": {"startIndex": st, "endIndex": en},
                         "paragraphStyle": {"namedStyleType": STYLE[style], "keepWithNext": True},
                         "fields": "namedStyleType,keepWithNext"}})
        elif style == "EL":
            reqs.append({"updateTextStyle": {"range": {"startIndex": st, "endIndex": en - 1},
                         "textStyle": {"bold": True, "italic": True}, "fields": "bold,italic"}})
            reqs.append({"updateParagraphStyle": {"range": {"startIndex": st, "endIndex": en},
                         "paragraphStyle": {"keepWithNext": True}, "fields": "keepWithNext"}})
        elif style == "EI":
            reqs.append({"updateTextStyle": {"range": {"startIndex": st, "endIndex": en - 1},
                         "textStyle": {"italic": True}, "fields": "italic"}})
            if bullets and bullets[-1][1] == st:
                bullets[-1][1] = en
            else:
                bullets.append([st, en])
    reqs += [{"createParagraphBullets": {"range": {"startIndex": a, "endIndex": b}, "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
             for a, b in bullets]
    return reqs


if __name__ == "__main__":
    # python outputs/ex3_presentation_narrative.py text <end_index>
    # python outputs/ex3_presentation_narrative.py style <read_doc.json>
    if sys.argv[1] == "text":
        print(json.dumps(text_requests(int(sys.argv[2])), ensure_ascii=False))
    else:
        d = json.load(open(sys.argv[2]))["content"]
        paras = []
        for el in d["tabs"][0]["documentTab"]["body"]["content"]:
            if "paragraph" in el:
                t = "".join(r.get("textRun", {}).get("content", "") for r in el["paragraph"]["elements"]).rstrip("\n")
                if t:
                    paras.append((el["startIndex"], el["endIndex"], t))
        print(json.dumps(style_requests(paras), ensure_ascii=False))
