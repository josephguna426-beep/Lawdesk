from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

styles = getSampleStyleSheet()
NOTE = "Application-generated summary. This is not an official or certified court order."


def _p(value, style="BodyText"):
    # escape user-supplied text so it cannot break the PDF markup
    text = escape(str(value)) if value not in (None, "") else "-"
    return Paragraph(text.replace("\n", "<br/>"), styles[style])


def _table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build_closure_pdf(case, closure, hearings, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm, title=f"Closure - {case.case_number}")
    s = [_p("Case Closure Summary", "Title"), _p(NOTE, "Italic"), Spacer(1, 6)]

    # 1. Case summary
    s += [_p("1. Case Summary", "Heading2")]
    s += [_table([
        [_p("Case number"), _p(case.case_number)],
        [_p("Title"), _p(case.title)],
        [_p("Type"), _p(case.case_type)],
        [_p("Court"), _p(case.court.name)],
        [_p("Filing date"), _p(case.filing_date)],
    ], [45 * mm, 125 * mm])]

    # 2. Client and parties
    s += [Spacer(1, 8), _p("2. Client and Parties", "Heading2")]
    rows = [[_p("Name"), _p("Role")]]
    rows += [[_p(c.full_name), _p("Client")] for c in case.clients.all()]
    rows += [[_p(cp.party.full_name), _p(cp.role or "Party")] for cp in case.caseparty_set.select_related("party")]
    s += [_table(rows, [100 * mm, 70 * mm])]

    # 3. Closure details
    s += [Spacer(1, 8), _p("3. Closure Details", "Heading2")]
    s += [_table([
        [_p("Outcome"), _p(closure.outcome)],
        [_p("Closure date"), _p(closure.closure_date)],
        [_p("Remarks"), _p(closure.remarks)],
        [_p("Final order reference"), _p(closure.final_order_reference)],
    ], [45 * mm, 125 * mm])]

    # 4. Judge comments and orders
    s += [Spacer(1, 8), _p("4. Judge Comments and Orders", "Heading2")]
    for h in hearings:
        if h.judge_comments or h.orders:
            s += [_p(f"Hearing {h.hearing_datetime:%d %b %Y %H:%M}", "Heading4"),
                  _p(f"Judge comments: {h.judge_comments or '-'}"),
                  _p(f"Orders: {h.orders or '-'}")]

    # 5. Complete hearing history
    s += [Spacer(1, 8), _p("5. Complete Hearing History", "Heading2")]
    rows = [[_p("Date/time"), _p("Status"), _p("Proceedings")]]
    rows += [[_p(f"{h.hearing_datetime:%d %b %Y %H:%M}"), _p(h.status), _p(h.proceedings)] for h in hearings]
    s += [_table(rows, [38 * mm, 28 * mm, 104 * mm])]

    doc.build(s)
