# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 8 Math: Interest and Credit
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 8, Financial Literacy F1.4, with F1.1, F1.2-F1.3 and F1.6)
  python3 tools/gen_caon_math_g8_financial.py
Simple interest (I = Prt), compound interest year by year in a table (no formula), simple vs compound growth and
long-term planning (graph and spreadsheet tables), credit cards (interest on the unpaid balance, minimum payments,
fees and rewards, other ways to pay), and budgets and financial choices.
All money is worked with decimal.Decimal. Compound balances are rounded to the cent each year (half up); every
cent answer is also checked against rounding only at the end, so both methods give the same answer.
Every rate is stated plainly in the question (sample rates).
Wrong answers come from real mistakes: compounding on the original amount only (= simple interest), the rate as
a whole number (x 4 instead of x 0.04) or as 0.4, giving the interest instead of the balance, months as years,
interest on the whole balance instead of the unpaid part, and rounding weeks or months down.
Ontario style: 4-digit numbers without a separator; 5 or more digits with a no-break space. HTML attributes
use single quotes. Helpers are copied from gen_caon_math_g6_financial.py.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e3f1e7"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#1f5fa8"
GREY = "#8a8a8a"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
CENT = D("0.01")


# ------------------------------------------------------------ numbers and money
def grp(n):
    """Whole number in Ontario style: 4536, 10 000 (no-break space)."""
    s = str(int(n))
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def money(d):
    d = D(d).quantize(CENT)
    assert 0 <= d < 1000000, d
    ip, fp = format(d, "f").split(".")
    return "$" + grp(ip) + "." + fp


def dol(d):
    """Money in running text: $1000, $1102.50, $12 000."""
    d = D(d).quantize(CENT)
    return "$" + grp(int(d)) if d == int(d) else money(d)


def pc(r):
    """Percent text: 4 -> 4%, 2.5 -> 2.5%."""
    return format(D(str(r)).normalize(), "f") + "%"


def dec(r):
    """Rate as a decimal: 4 -> 0.04, 2.5 -> 0.025."""
    return format((D(str(r)) / 100).normalize(), "f")


def r2(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


def cents_ok(x):
    return (F(str(x)) * 100).denominator == 1


def si(p, r, t):
    """Simple interest I = Prt (r in percent, t in years)."""
    return D(p) * D(str(r)) / 100 * D(str(t))


def comp(p, r, n):
    """Year-by-year compound table, rounded to the cent each year: [(year, start, interest, end)]."""
    rows, b = [], D(p)
    for y in range(1, n + 1):
        i = r2(b * D(str(r)) / 100)
        rows.append((y, b, i, b + i))
        b = b + i
    return rows


def cbal(p, r, n, exact=True):
    """Compound balance after n years. With exact=True also checks rounding only at the end gives the same cents."""
    b = comp(p, r, n)[-1][3] if n else D(p)
    if exact:
        assert r2(D(p) * (1 + D(str(r)) / 100) ** n) == b, (p, r, n)
    return b


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mq(q, correct, wrongs, e):
    """Money question: wrong values equal to the answer, not positive, or not whole cents are skipped."""
    correct = D(correct)
    w = [money(x) for x in wrongs if x is not None and D(x) > 0 and cents_ok(x) and D(x) != correct]
    return mcq(q, money(correct), w, e)


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def txt(x, y, t, fs=15, anchor="middle", bold=False, col=INK):
    return "<text x='%g' y='%g' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>" % (
        x, y, fs, " font-weight='700'" if bold else "", col, anchor, t)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (tables, graphs, statements) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def grid_svg(title, head, rows, widths, label):
    """A table drawn in SVG. A cell written as '?' is shown in red as the missing value."""
    rh, fs = 26, 15
    W = sum(widths) + 4
    s = []
    y = 4
    if title:
        s.append(txt(W / 2, 19, title, 16, bold=True))
        y = 28
    top = y
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
    x = 2
    for h, w in zip(head, widths):
        s.append(txt(x + w / 2, y + 18, h, fs, bold=True, col="#ffffff"))
        x += w
    y += rh
    for i, r in enumerate(rows):
        if i % 2:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, FILL))
        x = 2
        for c, w in zip(r, widths):
            if c == "?":
                s.append(txt(x + w / 2, y + 18, "?", 17, bold=True, col=RED))
            else:
                s.append(txt(x + w / 2, y + 18, c, fs))
            x += w
        y += rh
    x = 2
    for w in widths[:-1]:
        x += w
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, top, x, y, EDGE))
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    return svg_wrap(W, y + 3, "".join(s), label)


def comp_table(p, r, n, blank=None, title=None):
    """Year-by-year compound interest table. blank = (row index, column index) shown as '?'."""
    rows = []
    for y, st, i, en in comp(p, r, n):
        rows.append([str(y), money(st), money(i), money(en)])
    if blank:
        rows[blank[0]][blank[1]] = "?"
    t = title or "%s at %s compound interest per year" % (dol(p), pc(r))
    label = "Table " + t + ". " + "; ".join("Year %s: start %s, interest %s, end %s" % tuple(r_) for r_ in rows)
    return grid_svg(t, ["Year", "Start of year", "Interest", "End of year"], rows, [56, 122, 100, 122], label)


def sheet_table(title, head, rows, label):
    """A spreadsheet-style table (a digital tool) with whole-dollar balances."""
    widths = [70] + [120] * (len(head) - 1)
    return grid_svg(title, head, rows, widths, "Table " + label)


def graph_svg(p, r, years, labels):
    """Simple (straight line) and compound (curve) growth of p at r% per year, years 0..years."""
    ymax = 5000
    L, T, PW, PH = 62, 12, 300, 170
    W, H = L + PW + 92, T + PH + 46
    X = lambda t: L + PW * t / years
    Y = lambda v: T + PH - PH * float(v) / ymax
    s = []
    for v in range(0, ymax + 1, 1000):
        s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#dddddd' stroke-width='1'/>" % (L, Y(v), L + PW, Y(v)))
        s.append(txt(L - 6, Y(v) + 5, "$" + str(v), 14, anchor="end"))
    for t in range(0, years + 1, 5):
        s.append(txt(X(t), T + PH + 20, str(t), 14))
    s.append(txt(L + PW / 2, T + PH + 40, "Years", 14, bold=True))
    s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='%s' stroke-width='2'/>" % (L, T + PH, L + PW, T + PH, INK))
    s.append("<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='%s' stroke-width='2'/>" % (L, T, L, T + PH, INK))
    simple = [(X(t), Y(D(p) + si(p, r, t))) for t in range(years + 1)]
    cmp_ = [(X(t), Y(cbal(p, r, t, exact=False))) for t in range(years + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % q for q in simple), BLUE))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % q for q in cmp_), RED))
    if labels:
        s.append(txt(simple[-1][0] + 6, simple[-1][1] + 5, "Simple", 14, anchor="start", bold=True, col=BLUE))
        s.append(txt(cmp_[-1][0] + 6, cmp_[-1][1] + 5, "Compound", 14, anchor="start", bold=True, col=RED))
    end_s, end_c = D(p) + si(p, r, years), cbal(p, r, years, exact=False)
    label = ("Graph of %s at %s per year over %d years: a straight line rises to about %s and a curve rises to about %s%s"
             % (dol(p), pc(r), years, dol(round(end_s)), dol(round(end_c)),
                " (straight line labelled Simple, curve labelled Compound)" if labels else ""))
    return svg_wrap(W, H, "".join(s), label)


def statement_svg(rows, title="Credit card statement"):
    """rows = [(label, text, bold)]; '?' is shown in red."""
    W, rh, fs = 330, 26, 15
    s = [txt(W / 2, 19, title, 16, bold=True)]
    y = 28
    top = y
    for i, (lab, val, bold) in enumerate(rows):
        if bold:
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, FILL))
        s.append(txt(12, y + 18, lab, fs, anchor="start", bold=bold))
        if val == "?":
            s.append(txt(W - 12, y + 18, "?", 17, anchor="end", bold=True, col=RED))
        else:
            s.append(txt(W - 12, y + 18, val, fs, anchor="end", bold=bold))
        y += rh
        s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 2, y, EDGE))
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    label = "Statement " + title + ": " + "; ".join("%s %s" % (a, b) for a, b, c in rows)
    return svg_wrap(W, y + 3, "".join(s), label)


def budget_svg(title, money_in, money_out):
    """A monthly budget: rows of (label, amount) under Money in and Money out."""
    W, rh, fs = 300, 25, 15
    s = [txt(W / 2, 19, title, 16, bold=True)]
    y = 28
    rows = [("Money in", None, "h")] + [(a, b, "r") for a, b in money_in] + [("Money out", None, "h")] + [(a, b, "r") for a, b in money_out]
    top = y
    for lab, amt, kind in rows:
        if kind == "h":
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
            s.append(txt(12, y + 18, lab, fs, anchor="start", bold=True, col="#ffffff"))
        else:
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
            s.append(txt(12, y + 18, lab, fs, anchor="start"))
            s.append(txt(W - 12, y + 18, money(amt), fs, anchor="end"))
        y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    label = "Budget %s. Money in: %s. Money out: %s" % (
        title, ", ".join("%s %s" % (a, money(b)) for a, b in money_in), ", ".join("%s %s" % (a, money(b)) for a, b in money_out))
    return svg_wrap(W, y + 3, "".join(s), label)


# ============================================================ set 1: simple interest
def si_item(q, p, r, t, e_extra="", balance_=False, t_text=None, wr=None):
    """Simple interest (or the balance) with the usual wrong answers."""
    i = si(p, r, t)
    ans = D(p) + i if balance_ else i
    tt = t_text or str(D(str(t)).normalize())
    e = "I = Prt = %s × %s × %s = %s." % (dol(p), dec(r), tt, dol(i))
    if balance_:
        e = e[:-1] + ". Balance: %s + %s = <b>%s</b>." % (dol(p), dol(i), dol(ans))
    else:
        e = e.replace("= %s." % dol(i), "= <b>%s</b>." % dol(i))
    if e_extra:
        e += " " + e_extra
    whole = si(p, r, t) * 100                              # rate as a whole number
    tenth = si(p, r, t) * 10                               # 4% as 0.4
    one = si(p, r, 1)                                      # only one year
    if wr is None:
        if balance_:
            wr = [i, D(p) + one, D(p) + whole, D(p) + tenth]
        else:
            wr = [whole, D(p) + i, one, tenth]
    return mq(q, ans, wr, e)


def set_simple(P):
    its = []
    its.append(mcq("What is interest?", "Money paid for using someone else’s money",
                   ["The money you first put in", "A tax added to a purchase", "A fee for opening an account"],
                   "Interest is <b>money paid for the use of money</b>. A bank pays you interest on savings, and you pay "
                   "interest when you borrow."))
    its.append(mcq("In the simple interest formula I = Prt, what does P stand for?", "The principal (starting amount)",
                   ["The interest rate", "The time in years", "The total at the end"],
                   "I is the interest, <b>P is the principal</b> (the amount saved or borrowed), r is the yearly rate as a "
                   "decimal, and t is the time in years."))
    its.append(mcq("To use I = Prt, how do you write a rate of 4% per year?", "0.04", ["4", "0.4", "0.004"],
                   "Percent means “out of 100”. 4% = 4 ÷ 100 = <b>0.04</b>. Using 4 makes the interest 100 times too big."))
    its.append(mcq("How do you write a rate of 2.5% per year as a decimal?", "0.025", ["0.25", "2.5", "0.0025"],
                   "Divide by 100: 2.5% = 2.5 ÷ 100 = <b>0.025</b>. (0.25 is 25%.)"))
    its.append(si_item("What is the simple interest on $500 at 4% per year for 1 year?", 500, 4, 1,
                       "($2000 uses 4 instead of 0.04; $520 is the balance, not the interest.)"))
    its.append(si_item("What is the simple interest on $800 at 3% per year for 2 years?", 800, 3, 2,
                       "($24 is only 1 year of interest.)"))
    its.append(si_item("What is the simple interest on $1200 at 2.5% per year for 3 years?", 1200, D("2.5"), 3,
                       "($900 uses 0.25 instead of 0.025; $9000 uses 2.5; $30 is only 1 year.)",
                       wr=[D(900), D(9000), D(30)]))
    n, he, his, him = P.next()
    its.append(si_item("%s saves $600 in an account that pays 5%% simple interest per year. What is the balance after 4 years?" % n,
                       600, 5, 4, "($120 is only the interest; $630 is the balance after 1 year.)", balance_=True))
    its.append(si_item("What is the simple interest on $2000 at 1.5% per year for 2 years?", 2000, D("1.5"), 2,
                       "($30 is only 1 year of interest.)"))
    assert si(1000, 3, 1) == 30
    its.append(mq("$1000 is saved at 3% simple interest per year. How much interest is earned in the 5th year alone?",
                  D(30), [D(150), D(1150), D("33.77")],
                  "Simple interest is always found on the <b>original</b> $1000, so every year earns the same: "
                  "$1000 × 0.03 = <b>$30</b>. ($150 is the total for all 5 years; $33.77 would be compound interest.)"))
    its.append(si_item("What is the simple interest on $900 at 4% per year for 6 months?", 900, 4, D("0.5"),
                       "The time must be in years: 6 months = 6/12 = 0.5 years. ($216 uses 6 as the time; $36 is a full year; "
                       "$1800 uses 4 instead of 0.04.)", t_text="0.5", wr=[D(216), D(36), D(1800)]))
    assert si(1000, 2, D("1.5")) == 30
    its.append(mq("What is the simple interest on $1000 at 2% per year for 18 months?", D(30), [D(360), D(20), D(1030)],
                  "18 months = 18/12 = 1.5 years. I = $1000 × 0.02 × 1.5 = <b>$30</b>. "
                  "($360 uses 18 as the number of years; $20 is only 1 year.)"))
    assert si(400, D("3.5"), 1) == 14
    its.append(mcq("$400 earns $14 of simple interest in 1 year. What is the yearly interest rate?", "3.5%", ["14%", "35%", "0.035%"],
                   "r = I ÷ (Pt) = $14 ÷ $400 = 0.035. As a percent: 0.035 × 100 = <b>3.5%</b>. "
                   "(0.035% forgets to change the decimal back to a percent.)"))
    assert si(750, 4, 3) == 90 and si(750, 4, 1) == 30
    its.append(mcq("$750 earns 4% simple interest per year. How many years until it has earned $90 of interest?", "3 years",
                   ["22.5 years", "30 years", "4 years"],
                   "Interest each year: $750 × 0.04 = $30. $90 ÷ $30 = <b>3 years</b>. "
                   "(22.5 comes from $90 ÷ 4; 30 is the dollars of interest per year, not the time.)"))
    assert si(1000, 3, 2) == 60
    its.append(mq("How much must be saved at 3% simple interest per year to earn $60 of interest in 2 years?", D(1000),
                  [D(2000), D(10), D("3.60")],
                  "I = Prt, so P = I ÷ (rt) = $60 ÷ (0.03 × 2) = $60 ÷ 0.06 = <b>$1000</b>. Check: $1000 × 0.03 × 2 = $60. "
                  "($2000 forgets the 2 years; $3.60 multiplies instead of dividing.)"))
    assert si(500, 3, 4) == 60 and si(800, 2, 2) == 32
    its.append(mcq("Which earns more simple interest: $500 at 3% per year for 4 years, or $800 at 2% per year for 2 years?",
                   "$500 at 3% for 4 years", ["$800 at 2% for 2 years", "They earn the same", "You cannot compare them"],
                   "$500 × 0.03 × 4 = $60. $800 × 0.02 × 2 = $32. <b>$500 at 3% for 4 years</b> earns more, even though the "
                   "principal is smaller: the rate and the time matter too."))
    n, he, his, him = P.next()
    assert si(6000, 7, 3) == 1260
    its.append(mq("%s’s family borrows $6000 for a new furnace at 7%% simple interest per year. They pay it all back after 3 years. "
                  "How much do they pay back in total?" % n,
                  D(7260), [D(1260), D(6420), D(19260)],
                  "I = $6000 × 0.07 × 3 = $1260. Total: $6000 + $1260 = <b>$7260</b>. "
                  "($6420 is only 1 year; $19 260 multiplies $6000 × 1.07 × 3.)"))
    assert si(3600, 5, 1) / 12 == 15
    its.append(mq("A GIC pays 5% simple interest per year on $3600. If the yearly interest is shared equally over 12 months, "
                  "how much interest is that each month?",
                  D(15), [D(180), D(1800), D(300)],
                  "Yearly interest: $3600 × 0.05 = $180. Each month: $180 ÷ 12 = <b>$15</b>. "
                  "($180 is the interest for the whole year; $300 is $3600 ÷ 12; $1800 uses 0.5 instead of 0.05.)"))
    assert si(1000, 5, 20) == 1000
    its.append(mcq("$1000 is saved at 5% simple interest per year. After how many years has the interest earned reached $1000?",
                   "20 years", ["2 years", "50 years", "200 years"],
                   "Each year earns $1000 × 0.05 = $50. $1000 ÷ $50 = <b>20 years</b>. "
                   "(2 years uses 0.5 instead of 0.05; 200 years comes from $1000 ÷ 5.)"))
    assert si(500, 4, 3) == 60 and si(500, 4, 6) == 120 and si(500, 8, 6) == 240 and si(1000, 2, 3) == 60 and si(500, 6, 3) == 90
    its.append(mcq("$500 at 4% simple interest per year for 3 years earns $60. Which of these earns $120?",
                   "$500 at 4% for 6 years", ["$500 at 8% for 6 years", "$1000 at 2% for 3 years", "$500 at 6% for 3 years"],
                   "Doubling the time doubles simple interest: $500 × 0.04 × 6 = <b>$120</b>. "
                   "Doubling both the rate and the time makes it 4 times as much ($240). $1000 at 2% for 3 years earns $60, "
                   "and $500 at 6% for 3 years earns $90."))
    assert len(its) == 20
    return {"title": "Simple interest: I = Prt", "items": its}


# ============================================================ set 2: compound interest year by year
def set_compound(P):
    its = []
    its.append(mcq("What is compound interest?", "Interest earned on the principal and on earlier interest",
                   ["Interest that is the same every year", "Interest paid only at the very end", "A rate that goes up every year"],
                   "With compound interest, each year’s interest is added to the balance, and the next year’s interest is found on "
                   "<b>the new, bigger balance</b>. You earn interest on your interest."))
    b1, b2 = cbal(1000, 5, 1), cbal(1000, 5, 2)
    assert b1 == 1050 and b2 == D("1102.50")
    its.append(mq("$1000 is saved at 5% compound interest per year. What is the balance after 1 year?", b1,
                  [D(1500), D(50), D(1005)],
                  "Interest for year 1: $1000 × 0.05 = $50. Balance: $1000 + $50 = <b>$1050</b>. "
                  "($1500 uses 0.5 instead of 0.05.)"))
    its.append(mq("$1000 is saved at 5% compound interest per year. What is the balance after 2 years?", b2,
                  [D(1100), D(1050), D("102.50")],
                  "Year 1: $1000 + $50 = $1050. Year 2: interest on $1050 is $1050 × 0.05 = $52.50, so the balance is "
                  "$1050 + $52.50 = <b>$1102.50</b>. ($1100 finds the interest on the original $1000 again.)"))
    rows = comp(2000, 4, 2)
    assert rows[1][2] == D("83.20")
    its.append(mq(fig(comp_table(2000, 4, 2, blank=(1, 2))) + "The table shows $2000 saved at 4% compound interest per year. "
                  "What is the interest in year 2?",
                  rows[1][2], [D(80), rows[1][3], D("8.32")],
                  "Year 2 starts with $2080. Interest: $2080 × 0.04 = <b>$83.20</b>. "
                  "($80 uses the original $2000; $8.32 uses 0.004 instead of 0.04.)"))
    rows = comp(3000, 5, 3)
    assert rows[2][1] == D("3307.50")
    its.append(mq(fig(comp_table(3000, 5, 3, blank=(2, 1))) + "The table shows $3000 at 5% compound interest per year. "
                  "What goes in the missing cell?",
                  rows[2][1], [D(3000), D(3150), D(3300)],
                  "Each year starts with the balance at the end of the year before. Year 3 starts with <b>$3307.50</b>, "
                  "the end of year 2. ($3000 restarts from the original amount; $3300 is what simple interest would give.)"))
    b3 = cbal(1000, 10, 3)
    assert b3 == 1331
    its.append(mq("$1000 is saved at 10% compound interest per year. What is the balance after 3 years?", b3,
                  [D(1300), D(1210), D(331)],
                  "Year 1: $1000 + $100 = $1100. Year 2: $1100 + $110 = $1210. Year 3: $1210 + $121 = <b>$1331</b>. "
                  "($1300 adds $100 each year, which is simple interest.)"))
    its.append(mcq("At 3% compound interest per year, each year’s balance is the year before multiplied by what number?",
                   "1.03", ["0.03", "3", "1.3"],
                   "The new balance is 100% of the old balance plus 3% more: 103% = <b>1.03</b>. "
                   "Multiplying by 0.03 gives only the interest; 1.3 would be 30%."))
    its.append(mcq("Which calculation gives the balance after 2 years for $500 at 6% compound interest per year?",
                   "500 × 1.06 × 1.06", ["500 × 1.06 × 2", "500 + 500 × 0.06 × 2", "500 × 6 × 6"],
                   "Each year the balance is multiplied by 1.06, so two years is <b>500 × 1.06 × 1.06</b> = 561.80. "
                   "500 + 500 × 0.06 × 2 = 560 is simple interest; 500 × 1.06 × 2 doubles the money."))
    b = cbal(5000, 2, 2)
    assert b == 5202
    its.append(mq("$5000 is saved at 2% compound interest per year. What is the balance after 2 years?", b,
                  [D(5200), D(5100), D(202)],
                  "Year 1: $5000 × 0.02 = $100, so $5100. Year 2: $5100 × 0.02 = $102, so <b>$5202</b>. "
                  "($5200 uses $100 of interest both years.)"))
    rows = comp(2500, 4, 2)
    assert rows[1][2] == 104
    n, he, his, him = P.next()
    its.append(mq("%s puts $2500 in a savings account at 4%% compound interest per year. How much interest does %s earn in year 2?" % (n, he),
                  rows[1][2], [D(100), rows[1][3], D(1040)],
                  "Year 1: $2500 × 0.04 = $100, so the balance is $2600. Year 2: $2600 × 0.04 = <b>$104</b>. "
                  "($100 is year 1 again; $2704 is the balance, not the interest.)"))
    b = cbal(800, 5, 3)
    assert b == D("926.10")
    its.append(mq("$800 is saved at 5% compound interest per year. What is the balance after 3 years?", b,
                  [D(920), D(882), D("126.10")],
                  "Year 1: $800 + $40 = $840. Year 2: $840 + $42 = $882. Year 3: $882 + $44.10 = <b>$926.10</b>. "
                  "($920 is simple interest: $40 each year.)"))
    b = cbal(4000, 3, 2)
    assert b == D("4243.60")
    its.append(mq("$4000 is saved at 3% compound interest per year. What is the balance after 2 years?", b,
                  [D(4240), D(4120), D("243.60")],
                  "Year 1: $4000 × 0.03 = $120, so $4120. Year 2: $4120 × 0.03 = $123.60, so <b>$4243.60</b>. "
                  "($4240 uses $120 of interest both years.)"))
    b = cbal(5000, 2, 3)
    assert b == D("5306.04")
    its.append(mq(fig(comp_table(5000, 2, 3)) + "The table shows $5000 at 2% compound interest per year. "
                  "How much interest is earned in all over the 3 years?",
                  b - 5000, [D(300), b, D(102)],
                  "Total interest = final balance − principal = $5306.04 − $5000 = <b>$306.04</b>. "
                  "(Or add the interest column: $100 + $102 + $104.04.) $300 is what simple interest would give."))
    n, he, his, him = P.next()
    its.append(mcq("%s made a compound interest table for $1000 at 5%%. %s wrote $50 of interest in every row. What mistake did %s make?" % (n, cap(he), he),
                   "Finding interest on the original $1000 only",
                   ["Using 0.05 instead of 5", "Adding the interest to the balance", "Starting each year with the new balance"],
                   "$50 every year is simple interest. With compound interest each year’s interest is found on "
                   "<b>the new balance</b>, so year 2 earns $1050 × 0.05 = $52.50."))
    n, he, his, him = P.next()
    its.append(mcq("To find 4%% interest on $600, %s writes $600 × 4 = $2400. What should %s do instead?" % (n, he),
                   "Multiply $600 by 0.04", ["Multiply $600 by 0.4", "Add $4 to $600", "Divide $600 by 4"],
                   "4% = 0.04, so the interest is $600 × 0.04 = $24. Using 4 makes the interest 100 times too big, "
                   "and 0.4 is 40%. So <b>multiply by 0.04</b>."))
    its.append(mcq("In a spreadsheet, cell B2 holds the balance at the end of year 1. Which formula gives the balance at the end of "
                   "year 2 at 5% compound interest per year?", "=B2*1.05", ["=B2*0.05", "=B2+5", "=B2*5"],
                   "Multiplying by 1.05 keeps the balance and adds 5% of it. <b>=B2*1.05</b> can be filled down to make the next "
                   "years. (=B2*0.05 gives only the interest.)"))
    b = cbal(1000, 10, 4)
    assert b == D("1464.10")
    its.append(mq(fig(comp_table(1000, 10, 4, blank=(3, 3))) + "The table shows $1000 at 10% compound interest per year. "
                  "What is the balance at the end of year 4?",
                  b, [D(1400), D(1441), D("464.10")],
                  "Year 4 interest: $1331 × 0.10 = $133.10. End of year 4: $1331 + $133.10 = <b>$1464.10</b>. "
                  "($1400 is simple interest; $1441 adds only $110.)"))
    its.append(mcq("$1000 earns 5% compound interest per year: $50 in year 1 and $52.50 in year 2. Why is the interest bigger in year 2?",
                   "The year 1 interest earns interest too", ["The rate goes up in year 2", "The bank adds a bonus",
                                                               "Year 2 is longer than year 1"],
                   "The rate stays 5%, but year 2 starts with $1050, not $1000. The extra $2.50 is 5% of the $50 earned in year 1: "
                   "<b>the interest earns interest</b>."))
    b = cbal(10000, 3, 2)
    assert b == 10609
    its.append(mq("A family saves $10%s000 at 3%% compound interest per year. What is the balance after 2 years?" % NB, b,
                  [D(10600), D(10300), D(609)],
                  "Year 1: $10%s000 × 0.03 = $300, so $10%s300. Year 2: $10%s300 × 0.03 = $309, so <b>$10%s609</b>. "
                  "($10%s600 uses $300 both years.)" % (NB, NB, NB, NB, NB)))
    n, he, his, him = P.next()
    rows = comp(1500, 4, 3)
    b = cbal(1500, 4, 3)
    assert b == D("1687.30") and rows[2][3] == b
    its.append(mq("%s puts $1500 from a summer job into a 3-year GIC that pays 4%% compound interest per year. "
                  "What is the balance after 3 years, to the nearest cent?" % n,
                  b, [D(1680), D("1622.40"), D("187.30")],
                  "Year 1: $1500 + $60 = $1560. Year 2: $1560 + $62.40 = $1622.40. Year 3: $1622.40 × 0.04 = $64.896 → $64.90, "
                  "so <b>$1687.30</b>. ($1680 is simple interest.)"))
    assert len(its) == 20
    return {"title": "Compound interest year by year", "items": its}


# ============================================================ set 3: simple vs compound, long-term planning
def set_compare(P):
    its = []
    g = graph_svg(1000, 8, 20, False)
    its.append(mcq(fig(g) + "The graph shows $1000 growing at 8% per year for 20 years, once with simple interest and once with "
                   "compound interest. Which line shows compound interest?",
                   "The curved line", ["The straight line", "Both lines", "You cannot tell"],
                   "Simple interest adds the same $80 every year, so it makes a <b>straight line</b>. Compound interest adds more each "
                   "year, so its graph <b>curves upward</b>. The curved line is compound interest."))
    g = graph_svg(1000, 8, 20, True)
    its.append(mcq(fig(g) + "Which statement about the graph is true?",
                   "The gap between the lines grows each year", ["The lines are the same after 20 years",
                                                                 "Simple interest grows faster", "The gap stays the same"],
                   "Both start at $1000. Each year compound interest earns a little more than the year before, so "
                   "<b>the gap gets wider and wider</b>. After 20 years compound is about $4661 and simple is $2600."))
    assert cbal(1000, 5, 2) - (1000 + si(1000, 5, 2)) == D("2.50")
    its.append(mq("$1000 is saved for 2 years at 5% per year. How much more is the balance with compound interest than with simple interest?",
                  D("2.50"), [D("102.50"), D(5), D(100)],
                  "Simple: $1000 + $50 + $50 = $1100. Compound: $1050 + $52.50 = $1102.50. Difference: <b>$2.50</b>, "
                  "which is the 5% interest on year 1’s $50."))
    assert cbal(2000, 10, 3) == 2662 and 2000 + si(2000, 10, 3) == 2600
    its.append(mq("$2000 is saved for 3 years at 10% per year. How much more is the balance with compound interest than with simple interest?",
                  D(62), [D(662), D(600), D(200)],
                  "Simple: $2000 + 3 × $200 = $2600. Compound: $2200, $2420, then <b>$2662</b>. Difference: $2662 − $2600 = <b>$62</b>."))
    its.append(mcq("$800 is saved at 4% per year. After exactly 1 year, how does compound interest compare with simple interest?",
                   "They give the same balance", ["Compound gives more", "Simple gives more", "Compound gives double"],
                   "In year 1 both find 4% of the same $800, so both give $832. <b>They are the same after 1 year</b>; "
                   "compound pulls ahead from year 2 on."))
    rows = []
    vals = {}
    for y in [0, 5, 10, 15, 20]:
        s_ = D(1000) + si(1000, 6, y)
        c_ = cbal(1000, 6, y, exact=False)
        vals[y] = (s_, c_)
        rows.append([str(y), dol(round(s_)), dol(round(c_))])
    sheet = sheet_table("$1000 at 6% per year", ["Year", "Simple", "Compound"], rows,
                        "$1000 at 6% per year. " + "; ".join("Year %s: simple %s, compound %s" % tuple(r) for r in rows))
    s20, c20 = round(vals[20][0]), round(vals[20][1])
    assert s20 == 2200 and c20 == 3207
    its.append(mq(fig(sheet) + "A spreadsheet shows $1000 growing at 6% per year (balances to the nearest dollar). "
                  "After 20 years, how much more is the compound balance than the simple balance?",
                  D(c20 - s20), [D(c20), D(2207), D(1200)],
                  "Compound: $3207. Simple: $2200. Difference: $3207 − $2200 = <b>$1007</b>."))
    s10, c10 = round(vals[10][0]), round(vals[10][1])
    assert (s10, c10) == (1600, 1791)
    its.append(mcq(fig(sheet) + "Use the spreadsheet. How much does the gap between the compound and simple balances grow from "
                   "year 10 to year 20?", "It grows from $191 to $1007",
                   ["It stays at $191", "It grows from $600 to $1200", "It grows from $791 to $2207"],
                   "Year 10: $1791 − $1600 = $191. Year 20: $3207 − $2200 = $1007. The gap is more than 5 times as big: "
                   "<b>it grows from $191 to $1007</b>. Over a long time, compound interest pulls far ahead."))
    assert cbal(1000, 6, 12, exact=False) >= 2000 > cbal(1000, 6, 11, exact=False)
    its.append(mcq("The Rule of 72 estimates how long money takes to double with compound interest: 72 ÷ the rate. "
                   "About how many years does it take to double at 6% per year?", "12 years", ["6 years", "66 years", "432 years"],
                   "72 ÷ 6 = <b>12 years</b>. Check: $1000 × 1.06 twelve times is about $2012. "
                   "(66 subtracts 72 − 6; 432 multiplies.)"))
    assert si(1000, 6, 17) >= 1000 > si(1000, 6, 16)
    its.append(mcq("$1000 is saved at 6% per year. Which doubles the money first?", "6% compound interest",
                   ["6% simple interest", "Both double at the same time", "Neither one ever doubles"],
                   "Simple interest adds $60 a year, so it needs about 17 years to add $1000. Compound interest doubles the money in "
                   "about 12 years. <b>Compound interest</b> doubles it first."))
    a2 = 5000 + si(5000, 4, 2)
    b2 = cbal(5000, D("3.5"), 2)
    assert a2 == 5400 and b2 == D("5356.13")
    its.append(mcq("Account A pays 4% simple interest per year. Account B pays 3.5% compound interest per year. "
                   "Which account gives more on $5000 after 2 years?", "Account A, by $43.87",
                   ["Account B, by $43.87", "Account A, by $400", "They give the same"],
                   "A: $5000 + 2 × $200 = $5400. B: $5000 × 1.035 = $5175, then $5175 × 1.035 = $5356.125 → $5356.13. "
                   "<b>Account A gives $43.87 more</b> over a short time."))
    a20 = 5000 + si(5000, 4, 20)
    b20 = cbal(5000, D("3.5"), 20, exact=False)
    assert a20 == 9000 and round(b20) == 9949
    its.append(mcq("Account A pays 4% simple interest per year. Account B pays 3.5% compound interest per year. "
                   "A spreadsheet shows that after 20 years $5000 grows to $9000 in A and about $9949 in B. What does this show?",
                   "Over a long time, compound can beat a higher simple rate",
                   ["A higher rate always gives more", "Simple interest is always better", "The two accounts are the same"],
                   "Over 2 years Account A is ahead, but over 20 years Account B is about $949 ahead. "
                   "<b>For long-term savings, compounding can matter more than a slightly higher simple rate.</b>"))
    assert cbal(500, 20, 2) == 720
    its.append(mq("A $500 debt grows at 20% compound interest per year, and no payments are made. How much is owed after 2 years?",
                  D(720), [D(700), D(600), D(220)],
                  "Year 1: $500 + $100 = $600. Year 2: $600 + $120 = <b>$720</b>. "
                  "($700 is simple interest.) Compound interest makes unpaid debt grow quickly."))
    its.append(mcq("Why is compound interest good for savers but bad for borrowers?",
                   "It grows any balance faster, saved or owed", ["Banks never charge it on loans",
                                                                  "It only applies to savings accounts", "It makes the rate lower over time"],
                   "Compound interest <b>grows the balance faster</b>, whether it is money you have saved or money you owe. "
                   "That helps savers and hurts borrowers who leave debt unpaid."))
    opts = [("5% simple interest", D(1000) + si(1000, 5, 10)), ("4% compound interest", cbal(1000, 4, 10, exact=False)),
            ("5% compound interest", cbal(1000, 5, 10, exact=False)), ("3% compound interest", cbal(1000, 3, 10, exact=False))]
    best = max(opts, key=lambda t: t[1])
    assert best[0] == "5% compound interest" and [round(v) for _, v in opts] == [1500, 1480, 1629, 1344]
    its.append(mcq("Which choice grows $1000 the most in 10 years?", best[0], [o for o, v in opts if o != best[0]],
                   "From a spreadsheet: 5% simple gives $1500, 4% compound about $1480, 3% compound about $1344, and "
                   "<b>5% compound</b> about $1629, the most."))
    n, he, his, him = P.next()
    its.append(mcq("%s says: “$1000 at 5%% compound interest for 3 years is $1000 + 3 × $50 = $1150.” What mistake did %s make?" % (n, he),
                   "Finding interest on the original amount only",
                   ["Writing 5% as 0.05", "Using too many years", "Adding the interest to the principal"],
                   "%s used simple interest. With compound interest the balance is $1050, $1102.50, then $1157.63 (to the nearest cent). "
                   "%s found <b>interest on the original amount only</b>." % (cap(he), cap(he))))
    n, he, his, him = P.next()
    assert cbal(2500, 4, 2) - (2500 + si(2500, 4, 2)) == 4
    its.append(mq("%s saves $2500 for 2 years at 4%% per year. How much more does %s earn with compound interest than with simple interest?" % (n, he),
                  D(4), [D(204), D(104), D(200)],
                  "Simple: 2 × $100 = $200 of interest. Compound: $100 + $104 = $204 of interest. Difference: <b>$4</b>."))
    rows = []
    vv = {}
    for y in [0, 10, 20, 30]:
        a = cbal(1000, 3, y, exact=False)
        b = cbal(1000, 6, y, exact=False)
        vv[y] = (round(a), round(b))
        rows.append([str(y), dol(round(a)), dol(round(b))])
    sheet2 = sheet_table("$1000 with compound interest", ["Year", "At 3%", "At 6%"], rows,
                         "$1000 with compound interest. " + "; ".join("Year %s: at 3%% %s, at 6%% %s" % tuple(r) for r in rows))
    a30, b30 = vv[30]
    assert (a30, b30) == (2427, 5743)
    its.append(mq(fig(sheet2) + "A spreadsheet shows $1000 with compound interest at 3% and at 6% per year (to the nearest dollar). "
                  "After 30 years, how much more is in the 6% account?",
                  D(b30 - a30), [D(b30), D(1427), D(4743)],
                  "$5743 − $2427 = <b>$3316</b>. The rate is only doubled, but the interest earned ($4743 compared with $1427) "
                  "is more than 3 times as much."))
    n, he, his, him = P.next()
    m, she2, her2, _ = P.next()
    a = cbal(1000, 5, 50, exact=False)
    b = cbal(1000, 5, 40, exact=False)
    assert a > b
    its.append(mcq("%s puts $1000 into savings at 5%% compound interest per year at age 15. %s puts in $1000 at the same rate at age 25. "
                   "Both leave it until age 65. Who has more?" % (n, m),
                   n, [m, "They have the same", "You cannot tell"],
                   "%s’s money grows for 50 years; %s’s grows for 40. A spreadsheet gives about %s and about %s. "
                   "<b>%s</b> has far more: starting early gives compound interest more time." % (n, m, dol(round(a)), dol(round(b)), n)))
    y20 = comp(1000, 6, 20)[-1]
    assert y20[1] == D("3025.60") and y20[2] == D("181.54")
    its.append(mq("$1000 is saved at 6%% compound interest per year. A spreadsheet shows a balance of %s at the start of year 20. "
                  "How much interest is earned in year 20, to the nearest cent?" % dol(y20[1]),
                  y20[2], [D(60), y20[3], D("1815.36")],
                  "$3025.60 × 0.06 = $181.536 → <b>$181.54</b>. That is about 3 times the $60 earned in year 1, at the same rate. "
                  "($60 uses the original $1000; $3207.14 is the balance, not the interest.)"))
    its.append(mcq("Which choice is the best long-term financial plan for saving?",
                   "Start early and leave the interest in", ["Wait to start until you earn more",
                                                             "Take the interest out each year", "Keep the money at home"],
                   "Compound interest needs the interest to stay in the account and needs time. <b>Starting early and leaving the "
                   "interest in</b> lets the interest earn interest for many years."))
    assert len(its) == 20
    return {"title": "Simple vs compound interest over time", "items": its}


# ============================================================ set 4: credit cards, fees and rewards
def set_credit(P):
    its = []
    its.append(mcq("You pay the full credit card balance by the due date. How much interest do you pay on the new purchases?",
                   "None", ["2% of the balance", "The minimum payment", "One month of interest"],
                   "Credit cards in Canada give a grace period of at least 21 days for new purchases. If you "
                   "<b>pay the full balance by the due date</b>, no interest is charged."))
    its.append(mcq("What happens when you pay only the minimum payment on a credit card?",
                   "Interest is charged on the unpaid part", ["The rest of the bill is cancelled",
                                                              "No interest is charged", "The card company pays the rest"],
                   "The minimum payment only keeps the account in good standing. <b>Interest is charged on everything you do not pay</b>, "
                   "so the debt can last a long time."))
    its.append(mcq("A credit card charges 24% interest per year. About what rate is that per month?",
                   "2% per month", ["24% per month", "12% per month", "0.24% per month"],
                   "There are 12 months in a year: 24% ÷ 12 = <b>2% per month</b>."))
    n, he, his, him = P.next()
    assert D(400) * D("0.02") == 8
    its.append(mq("%s leaves $400 unpaid on a credit card that charges 2%% interest per month on the unpaid balance. "
                  "How much interest is added after 1 month?" % n,
                  D(8), [D(800), D(408), D(80)],
                  "$400 × 0.02 = <b>$8</b>. ($800 uses 2 instead of 0.02; $408 is the new balance; $80 uses 0.2.)"))
    n, he, his, him = P.next()
    assert (650 - 150) * D("0.02") == 10
    its.append(mq("%s’s credit card bill is $650. %s pays $150 by the due date. The card charges 2%% interest per month on the "
                  "unpaid balance. How much interest is added?" % (n, cap(he)),
                  D(10), [D(13), D(3), D(1000)],
                  "Unpaid balance: $650 − $150 = $500. Interest: $500 × 0.02 = <b>$10</b>. "
                  "($13 finds interest on the whole $650; $3 finds it on the $150 that was paid.)"))
    st = statement_svg([("New purchases", money(320), False), ("Balance", money(320), True),
                        ("Minimum payment", "?", True)])
    assert D(320) * D("0.03") == D("9.60")
    its.append(mq(fig(st) + "The minimum payment is $10 or 3% of the balance, whichever is more. What is the minimum payment on this statement?", D(10), [D("9.60"), D(96), D(320)],
                  "3% of $320 = $320 × 0.03 = $9.60. That is less than $10, so the minimum payment is <b>$10</b>."))
    assert D(850) * D("0.03") == D("25.50")
    its.append(mq("A card’s minimum payment is $10 or 3% of the balance, whichever is more. What is the minimum payment on a balance of $850?",
                  D("25.50"), [D(10), D(255), D("8.50")],
                  "3% of $850 = $850 × 0.03 = $25.50. That is more than $10, so the minimum is <b>$25.50</b>. "
                  "($255 uses 0.3; $8.50 is only 1%.)"))
    assert D(2400) * D("0.015") == 36
    its.append(mq("A credit card gives 1.5% cash back on purchases. A family spends $2400 on the card in a year. How much cash back do they get?",
                  D(36), [D(360), D(3600), D(24)],
                  "$2400 × 0.015 = <b>$36</b>. ($360 uses 0.15; $24 is only 1%.)"))
    assert D(120) / D("0.01") == 12000
    its.append(mq("A card has a $120 yearly fee and gives 1% cash back. How much must be spent in a year for the cash back to equal the fee?",
                  D(12000), [D(1200), D(120), D(121)],
                  "1%% of the spending must be $120. Spending = $120 ÷ 0.01 = <b>$12%s000</b>. Check: 1%% of $12%s000 = $120. "
                  "($1200 uses 0.1 instead of 0.01.)" % (NB, NB)))
    assert D(80) * D("0.025") == 2
    its.append(mq("A purchase on a US website is charged as $80.00 in Canadian dollars. The card adds a 2.5% foreign transaction fee. How much is the fee?",
                  D(2), [D(200), D("0.20"), D(82)],
                  "$80.00 × 0.025 = <b>$2.00</b>. ($200 uses 2.5 instead of 0.025; $82 is the total with the fee.)"))
    a = D(6000) * D("0.005")
    b = D(6000) * D("0.02") - 99
    assert a == 30 and b == 21
    its.append(mcq("Card A has no yearly fee and gives 0.5% cash back. Card B has a $99 yearly fee and gives 2% cash back. "
                   "A family spends $6000 a year on the card. Which card leaves them better off?",
                   "Card A, by $9", ["Card B, by $9", "Card B, by $90", "They are the same"],
                   "Card A: $6000 × 0.005 = $30. Card B: $6000 × 0.02 = $120, minus the $99 fee = $21. "
                   "<b>Card A is better by $9</b>. Big rewards do not always beat the fee."))
    n, he, his, him = P.next()
    m1 = D(500) + r2(D(500) * D("0.02"))
    m2 = m1 + r2(m1 * D("0.02"))
    assert m2 == D("520.20")
    its.append(mq("%s leaves $500 on a credit card that charges 2%% interest per month and makes no payments. "
                  "Interest is added each month. What is the balance after 2 months?" % n,
                  m2, [D(520), D(510), D("20.20")],
                  "Month 1: $500 × 0.02 = $10, so $510. Month 2: $510 × 0.02 = $10.20, so <b>$520.20</b>. "
                  "Credit card interest compounds: you pay interest on interest. ($520 uses $10 both months.)"))
    assert D(1000) * D("0.1999") == D("199.90")
    its.append(mq("A credit card charges 19.99% interest per year. About how much interest is charged on $1000 left unpaid for a year? "
                  "(Ignore the monthly compounding.)",
                  D("199.90"), [D(19990), D("19.99"), D("1199.90")],
                  "$1000 × 0.1999 = <b>$199.90</b>. That is almost $200 extra, about one fifth of the debt. ($19.99 uses 0.01999.)"))
    assert D(800) * D("0.015") == 12
    its.append(mq("A store credit card charges 1.5% interest per month on the unpaid balance. $800 is left unpaid. How much interest is added in 1 month?",
                  D(12), [D(1200), D(120), D(812)],
                  "$800 × 0.015 = <b>$12</b>. ($1200 uses 1.5; $120 uses 0.15; $812 is the new balance, not the interest.)"))
    its.append(mcq("Which way of paying takes money straight from your own bank account, so you are not borrowing?",
                   "Debit card", ["Credit card", "Buy now, pay later plan", "Store credit card"],
                   "A <b>debit card</b> uses money already in your bank account. Credit cards and pay-later plans are borrowed money "
                   "that you must pay back."))
    its.append(mcq("Which card can only spend the money that was loaded onto it ahead of time?",
                   "Prepaid card", ["Credit card", "Store credit card", "Line of credit"],
                   "A <b>prepaid card</b> is loaded with money first, so you cannot spend more than that or owe interest. "
                   "It lets you shop online without borrowing."))
    n, he, his, him = P.next()
    assert 4 * 45 == 180 and 180 + 2 * 10 == 200
    its.append(mq("A store offers a $180 jacket as 4 payments of $45 with no interest, but charges a $10 fee for each late payment. "
                  "%s is late with 2 payments. How much does the jacket cost in total?" % n,
                  D(200), [D(180), D(190), D(220)],
                  "Payments: 4 × $45 = $180. Late fees: 2 × $10 = $20. Total: $180 + $20 = <b>$200</b>."))
    its.append(mcq("Which habit helps a person build a good credit history?",
                   "Paying the full bill on time every month", ["Paying only some bills on time",
                                                                "Using as much of the limit as possible", "Opening many new cards"],
                   "Lenders look at how you have handled credit. <b>Paying the full bill on time</b> every month shows you are "
                   "reliable and also avoids interest."))
    assert D(1000) * D("0.01") == 10
    its.append(mq("A card gives 1 reward point for every $1 spent, and 100 points are worth $1. How much are the points worth after $1000 of purchases?",
                  D(10), [D(1000), D(100), D(1)],
                  "$1000 gives 1000 points. 1000 ÷ 100 = <b>$10</b>. That is the same as 1% back."))
    unpaid = D(450) - D(200)
    i = unpaid * D("0.02")
    new = unpaid + i + D(120)
    assert i == 5 and new == 375
    st = statement_svg([("Previous balance", money(450), False), ("Payment", MINUS + money(200), False),
                        ("Interest (2% of unpaid)", "?", False), ("New purchases", money(120), False), ("New balance", "?", True)])
    its.append(mq(fig(st) + "The card charges 2% interest per month on the unpaid part of the previous balance. What is the new balance?",
                  new, [D(370), D(379), D(775)],
                  "Unpaid: $450 − $200 = $250. Interest: $250 × 0.02 = $5. New balance: $250 + $5 + $120 = <b>$375</b>. "
                  "($370 forgets the interest; $379 finds interest on the whole $450.)"))
    assert len(its) == 20
    return {"title": "Credit cards: interest, fees and rewards", "items": its}


# ============================================================ set 5: budgets and choices
def set_budget(P):
    its = []
    its.append(mcq("In a monthly budget, which is a fixed expense?", "A $35 phone plan each month",
                   ["Snacks with friends", "Movie tickets", "Birthday gifts"],
                   "A fixed expense is <b>the same amount every month</b>, like a phone plan, rent or a bus pass. "
                   "The others change from month to month (variable expenses)."))
    n, he, his, him = P.next()
    assert D(240) * D("0.2") == 48
    its.append(mq("%s earns $240 a month babysitting. %s plan is to save 20%% first. How much does %s save each month?" % (n, cap(his), he),
                  D(48), [D(192), D(20), D(480)],
                  "20%% of $240 = $240 × 0.2 = <b>$48</b>. ($192 is the 80%% %s keeps to spend.)" % he))
    n, he, his, him = P.next()
    bi = [("Babysitting", D(200)), ("Allowance", D(120))]
    bo = [("Phone plan", D(35)), ("Bus pass", D(50)), ("Food out", D(60)), ("Clothes", D(45)), ("Savings", D(80))]
    left = sum(b for a, b in bi) - sum(b for a, b in bo)
    assert left == 50
    its.append(mq(fig(budget_svg("%s’s budget for October" % n, bi, bo)) + "How much of %s’s money is not planned for yet?" % n,
                  left, [D(130), D(270), D(10)],
                  "Money in: $200 + $120 = $320. Money out: $35 + $50 + $60 + $45 + $80 = $270 (savings is planned money too). "
                  "$320 − $270 = <b>$50</b>. ($130 forgets the savings.)"))
    n, he, his, him = P.next()
    assert -(-(900 - 300) // 75) == 8
    its.append(mcq("%s wants a $900 laptop. %s has $300 saved and saves $75 a month. How many more months until %s can buy it?" % (n, cap(he), he),
                   "8 months", ["12 months", "4 months", "11 months"],
                   "Still needed: $900 − $300 = $600. $600 ÷ $75 = <b>8 months</b>. (12 months forgets the $300 already saved.)"))
    n, he, his, him = P.next()
    assert 12 * 55 - 600 == 60
    its.append(mq("%s wants a $600 bike. Choice 1: save $100 a month and buy it in 6 months. Choice 2: buy it now with a store plan of "
                  "12 payments of $55. How much more does Choice 2 cost?" % n,
                  D(60), [D(660), D(55), D(45)],
                  "Choice 2: 12 × $55 = $660. Choice 1: $600. $660 − $600 = <b>$60</b> more. Buying now costs extra; waiting saves money. "
                  "($45 compares the monthly amounts, $100 − $55; $660 is the total, not the extra.)"))
    assert 3 * 2400 == 7200
    its.append(mq("A financial plan says a family should keep an emergency fund equal to 3 months of expenses. The family spends $2400 a month. "
                  "How big should the fund be?",
                  D(7200), [D(800), D(2400), D(7500)],
                  "3 × $2400 = <b>$7200</b>. ($800 divides by 3 instead of multiplying.)"))
    its.append(mcq("What does “pay yourself first” mean in a budget?",
                   "Put money into savings before spending", ["Buy what you want first", "Pay your friends back first",
                                                               "Spend your pay on the first day"],
                   "When money comes in, <b>move your savings amount first</b>, then plan spending with what is left. "
                   "Saving becomes a habit instead of whatever is left over."))
    n, he, his, him = P.next()
    assert 50 * 12 * 4 == 2400
    its.append(mq("%s saves $50 a month for college for 4 years. Without interest, how much will %s have?" % (n, he),
                  D(2400), [D(200), D(600), D(1200)],
                  "12 months × 4 years = 48 months. 48 × $50 = <b>$2400</b>. ($200 uses 4 months; $600 is only 1 year.)"))
    assert D(2000) * D("0.2") == 400
    its.append(mq("For an RESP, the Canada Education Savings Grant adds 20% of what is put in each year (up to $500 a year). "
                  "Parents put in $2000 this year. How much is the grant?",
                  D(400), [D(40), D(2400), D(500)],
                  "20% of $2000 = $2000 × 0.2 = <b>$400</b>. That is less than $500, so the full $400 is added. "
                  "($2400 is the total with the grant.)"))
    assert si(12000, 5, 3) == 1800
    its.append(mq("A family borrows $12%s000 for a used car at 5%% simple interest per year for 3 years. How much interest do they pay?" % NB,
                  D(1800), [D(600), D(13800), D(180000)],
                  "I = $12%s000 × 0.05 × 3 = <b>$1800</b>. ($600 is only 1 year; $13%s800 is the total paid back.)" % (NB, NB)))
    n, he, his, him = P.next()
    assert D(900) * D("1.2") == 1080
    its.append(mq("%s buys a $900 phone on a credit card that charges 20%% interest per year and pays nothing for a year. "
                  "About how much is owed after 1 year? (Ignore the monthly compounding.)" % n,
                  D(1080), [D(180), D(920), D(18900)],
                  "Interest: $900 × 0.2 = $180. Owed: $900 + $180 = <b>$1080</b>. Saving up first would have cost $180 less."))
    assert F(1800, 6000) == F(3, 10)
    its.append(mcq("A family earns $6000 a month. Rent is $1800 a month. What percent of the income goes to rent?",
                   "30%", ["18%", "3.3%", "60%"],
                   "$1800 ÷ $6000 = 0.3 = <b>30%</b>. (3.3% comes from 6000 ÷ 1800 = 3.33.)"))
    n, he, his, him = P.next()
    assert 380 + 90 - 450 == 20
    its.append(mcq("%s can play hockey for $450 this season, or ringette for $380 plus $90 for equipment. Which costs less, and by how much?" % n,
                   "Hockey, by $20", ["Ringette, by $70", "Ringette, by $20", "They cost the same"],
                   "Ringette: $380 + $90 = $470. Hockey: $450. $470 − $450 = $20, so <b>hockey costs $20 less</b>. "
                   "(Ringette by $70 forgets the equipment.)"))
    s_ = 2000 + si(2000, 4, 10)
    c_ = cbal(2000, 4, 10, exact=False)
    assert s_ == 2800 and round(c_) == 2960
    n, he, his, him = P.next()
    its.append(mq("%s’s grandparents put $2000 aside for %s at 4%% per year for 10 years. A spreadsheet shows $2800 with simple interest "
                  "and $2960 with compound interest (to the nearest dollar). How much more does compounding give?" % (n, him),
                  D(160), [D(960), D(800), D(2960)],
                  "$2960 − $2800 = <b>$160</b>. ($960 is all the compound interest; $800 is all the simple interest.)"))
    assert si(800, 3, D("0.25")) == 6
    its.append(mq("$800 sits in a savings account at 3% simple interest per year for the 3 months of summer. How much interest does it earn?",
                  D(6), [D(72), D(24), D(2)],
                  "3 months = 3/12 = 0.25 years. I = $800 × 0.03 × 0.25 = <b>$6</b>. ($72 uses 3 as the years; $24 is a full year.)"))
    n, he, his, him = P.next()
    assert 15 * 52 == 780
    its.append(mq("%s saves $15 every week for a year. How much does %s save?" % (n, he), D(780), [D(180), D(60), D(720)],
                  "A year has 52 weeks: 52 × $15 = <b>$780</b>. ($180 uses 12, the number of months; $720 uses 48 weeks.)"))
    n, he, his, him = P.next()
    earn = 17 * 20 * 8
    assert earn == 2720 and D(earn) * D("0.4") == 1088
    its.append(mq("%s works a summer job at $17 an hour, 20 hours a week, for 8 weeks. %s saves 40%% of the pay. How much does %s save?" % (n, cap(he), he),
                  D(1088), [D(2720), D(1632), D(136)],
                  "Pay: $17 × 20 × 8 = $2720. Savings: $2720 × 0.4 = <b>$1088</b>. ($1632 is the 60% spent; $136 is 40% of one week.)"))
    n, he, his, him = P.next()
    gain = D(1000) * D("0.2") - D(1000) * D("0.02")
    assert gain == 180
    its.append(mq("%s has $1000 in savings earning 2%% per year and owes $1000 on a credit card at 20%% per year. "
                  "If %s uses the savings to pay off the card, about how much better off is %s each year?" % (n, he, he),
                  gain, [D(200), D(20), D(220)],
                  "%s stops paying $1000 × 0.2 = $200 of interest, but gives up $1000 × 0.02 = $20 of interest earned. "
                  "$200 − $20 = <b>$180</b> better off each year. High-interest debt is usually the first thing to pay off." % cap(he)))
    its.append(mcq("Which is a need in a family budget for a Canadian winter?", "Winter boots that fit",
                   ["A new gaming console", "Concert tickets", "A second pair of skates"],
                   "A need is something you must have to be safe and healthy. <b>Winter boots that fit</b> keep feet warm and dry; "
                   "the others are wants."))
    n, he, his, him = P.next()
    b = cbal(3000, 2, 2)
    assert b == D("3121.20")
    its.append(mq("%s’s family saves $3000 for a canoe trip in 2 years in an account that pays 2%% compound interest per year. "
                  "How much will they have?" % n,
                  b, [D(3120), D(3060), D("121.20")],
                  "Year 1: $3000 × 0.02 = $60, so $3060. Year 2: $3060 × 0.02 = $61.20, so <b>$3121.20</b>. "
                  "($3120 finds interest on the original $3000 both years.)"))
    assert len(its) == 20
    return {"title": "Budgets and money choices", "items": its}


# ============================================================ lesson
def body_html():
    assert si(500, 3, 2) == 30 and cbal(1000, 5, 3, exact=False) == D("1157.63")
    return (
        "<h2>Simple interest: I = Prt</h2>"
        "<p>Interest is money paid for using money. A bank pays you interest on savings. You pay interest when you borrow. "
        "<b>Simple interest</b> is found on the principal only, so it is the same every year.</p>"
        "<p>I = Prt: P is the principal, r is the yearly rate <b>as a decimal</b> (3% = 0.03), and t is the time in years "
        "(6 months = 0.5 years).</p>" +
        ex("Example", "You save $500 at 3% simple interest per year for 2 years. What is the balance?",
           "I = $500 × 0.03 × 2 = $30. Balance: $500 + $30 = $530.", "$530") +
        "<h2>Compound interest: build a table</h2>"
        "<p>With <b>compound interest</b>, each year’s interest is added to the balance. Next year’s interest is found on the new, "
        "bigger balance, so you earn interest on interest. Make a table one year at a time (a spreadsheet can do this for you).</p>"
        "<figure class='sn-fig'>" + comp_table(1000, 5, 3) +
        "<figcaption>$1000 at 5% compound interest: $50, then $52.50, then $55.13 of interest (to the nearest cent). "
        "Simple interest would give only $1150.</figcaption></figure>" +
        ex("Example", "$1000 is saved at 5% compound interest per year. What is the balance after 2 years?",
           "Year 1: $1000 × 0.05 = $50, so $1050. Year 2: $1050 × 0.05 = $52.50, so $1102.50. "
           "In one step: $1000 × 1.05 × 1.05 = $1102.50.", "$1102.50") +
        "<h2>Simple vs compound over time</h2>"
        "<p>Simple interest grows in a straight line. Compound interest curves upward, and the gap gets wider every year. "
        "For long-term savings, <b>start early and leave the interest in</b>. For debt, the same growth works against you.</p>"
        "<figure class='sn-fig'>" + graph_svg(1000, 8, 20, True) +
        "<figcaption>$1000 at 8% per year: $2600 with simple interest and about $4661 with compound interest after 20 years.</figcaption></figure>"
        "<h2>Credit cards</h2>"
        "<p>A credit card is borrowed money. Pay the <b>full balance by the due date</b> and no interest is charged on new purchases. "
        "Leave part unpaid and interest is charged on it every month (often about 20% a year, close to 2% a month). "
        "Paying only the minimum keeps the debt growing. Watch for yearly fees, and check whether rewards really cover them.</p>" +
        ex("Example", "A bill is $650 and you pay $150. The card charges 2% interest per month on the unpaid balance. How much interest is added?",
           "Unpaid: $650 − $150 = $500. Interest: $500 × 0.02 = $10.", "$10") +
        "<h2>Budgets and financial plans</h2>"
        "<p>A budget lists money in and money out. Fixed expenses stay the same each month; variable expenses change. "
        "Pay yourself first: put savings aside before you spend. Compare choices by their total cost, including interest and fees.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using the rate as a whole number ($600 × 4)", "Change the percent to a decimal: 4% = 0.04"],
            ["Finding compound interest on the original amount every year", "Find each year’s interest on the new balance"],
            ["Giving the interest when the question asks for the balance", "Balance = principal + interest"],
            ["Using months as years (6 months as t = 6)", "Divide by 12: 6 months = 0.5 years"],
            ["Finding card interest on the whole bill", "Interest is charged only on the unpaid part"],
        ])
    )


FAQ = [
    {"q": "What is the difference between simple and compound interest?",
     "a": "Simple interest is found on the starting amount only, so it is the same every year. Compound interest is found on the "
          "new balance each year, so the interest also earns interest and the money grows faster."},
    {"q": "How do Grade 8 students calculate compound interest without a formula?",
     "a": "They build a table one year at a time: find the interest on the balance, add it, and use the new balance for the next year. "
          "A spreadsheet can fill in many years quickly, for example with =B2*1.05 at 5%."},
    {"q": "What do Grade 8 students learn in financial literacy in Ontario?",
     "a": "Grade 8 students compare methods of payment, build financial plans and budgets, find the growth of simple and compound "
          "interest, and learn how credit card interest, fees and rewards work."},
    {"q": "How is interest charged on a credit card?",
     "a": "If the full balance is paid by the due date, new purchases have no interest. Any unpaid balance is charged interest, "
          "often about 20% a year, and the interest compounds each month until it is paid off."},
]


def gen():
    rnd = random.Random(48819)
    P = People(rnd)
    sets = [set_simple(P), set_compound(P), set_compare(P), set_credit(P), set_budget(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"\$[\d ]+\.\d\d", x) for x in it["c"]):
                assert len({D(x[1:].replace(NB, "")) for x in it["c"]}) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert not re.search(r"\d,\d{3}", re.sub(r"<svg.*?</svg>", "", x)), x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "interest-and-credit", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Interest and Credit: Simple and Compound Interest, Credit Cards and Budgets",
        "seo_title": "Grade 8 Simple and Compound Interest Worksheets: Credit Cards and Budgets (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Interest and Credit",
        "domain": "Financial Literacy",
        "standard_code": "Grade 8: F1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine the growth of simple and compound interest at various rates using digital tools, and explain "
                         "the impact interest has on long-term financial planning",
        "meta_desc": "Free Grade 8 math worksheets on interest and credit for the Ontario curriculum: simple interest with I = Prt, "
                     "compound interest year by year in a table, simple vs compound growth over time, credit card interest, fees "
                     "and rewards, and budgets and money choices. 100 questions with an answer key.",
        "key_big": "Simple interest is found on the principal only; compound interest is found on the new balance each year.",
        "key_sub": "Write the rate as a decimal (4% = 0.04). $1000 at 5% compound grows to $1050, then $1102.50, because "
                   "the interest earns interest. On a credit card, interest is charged only on the part you do not pay by the due date.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Table ")
    mark_large(u, "Graph ")
    mark_large(u, "Budget ")
    mark_large(u, "Statement ")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
