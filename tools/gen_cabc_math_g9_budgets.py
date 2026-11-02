# -*- coding: utf-8 -*-
"""
BC Grade 9 Math: Budgets and Transactions (BC Mathematics Curriculum, Financial literacy: simple budgets and transactions)
  python3 tools/gen_cabc_math_g9_budgets.py
Income (hourly wage, gross and net pay), budgets (fixed and variable expenses), transactions with BC sales tax
(GST 5% + PST 7%), bank balances and fees, and saving goals. All money is worked with decimal.Decimal; each tax
is rounded to the cent (no price is used whose GST or PST ends in exactly half a cent). Canada has no pennies:
cash totals round to the nearest 5 cents, card and debit payments are exact. BC style: 4-digit numbers without a
separator, 5 or more digits with a no-break space, $ and the cent sign, the real minus sign.
Helpers are copied from gen_cabc_math_g7_financial_percentages.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
LIGHT = "#d9eadf"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
CENT = D("0.01")


# ------------------------------------------------------------ money
def group(ip):
    """Digits of a whole number: 4 digits plain, 5 or more grouped by threes with a no-break space."""
    if len(ip) < 5:
        return ip
    out = []
    while ip:
        out.insert(0, ip[-3:])
        ip = ip[:-3]
    return NB.join(out)


def money(d):
    d = D(d)
    assert abs(d) < 1000000, d
    s = format(abs(d).quantize(CENT), "f")
    ip, fp = s.split(".")
    return (MINUS if d < 0 else "") + "$" + group(ip) + "." + fp


def dol(n):
    """Whole dollars in running text: $48 000, $1200."""
    return "$" + group(str(int(n)))


def cents_ok(x):
    return (F(str(x)) * 100).denominator == 1


def rtax(p, rate):
    p = D(p)
    assert (p * 100 * rate) % 100 != 50, (p, rate)
    return (p * D(rate) / 100).quantize(CENT, rounding=ROUND_HALF_UP)


def gst(p):
    return rtax(p, 5)


def pst(p):
    return rtax(p, 7)


def both(p):
    t = gst(p) + pst(p)
    assert t == rtax(p, 12), p
    return t


def with_tax(p):
    return D(p) + both(p)


def pct(p, r):
    x = D(p) * D(r) / 100
    assert x == x.quantize(CENT), (p, r)
    return x


def sale(p, r):
    return D(p) - pct(p, r)


def cash(d):
    c = int(D(d) * 100)
    assert D(c) / 100 == D(d)
    return D((c + 2) // 5 * 5) / 100


def cap(s):
    return s[0].upper() + s[1:]


def ceil_div(a, b):
    q = F(str(D(a))) / F(str(D(b)))
    return -(-q.numerator // q.denominator)


def plural(n, w):
    return "%s %s%s" % (n, w, "" if n == 1 else "s")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
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
    correct = D(correct)
    w = [money(x) for x in wrongs if x is not None and cents_ok(x) and D(x) != correct]
    return mcq(q, money(correct), w, e)


def balance(sets, rnd):
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


def txt(x, y, t, fs=16, anchor="middle", bold=False, col=INK):
    return "<text x='%s' y='%s' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>" % (
        x, y, fs, " font-weight='700'" if bold else "", col, anchor, t)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    u["body_html"] = rx.sub("<svg data-pf='lg' ", u["body_html"])
    return u


# ------------------------------------------------------------ pictures
def stub_svg(rows, title="Pay stub"):
    """rows = [(label, value_text, kind)] kind: 'g' gross, 'd' deduction, 't' net (last)."""
    W, rh = 280, 24
    s = [txt(W // 2, 22, title, 17, bold=True)]
    y = 48
    for lab, val, kind in rows:
        if kind == "t":
            s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (y - 17, W - 10, y - 17, INK))
            y += 4
        bold = kind in ("g", "t")
        x0 = 14 if kind != "d" else 28
        s.append(txt(x0, y, lab, 16, "start", bold=bold))
        s.append(txt(W - 14, y, val, 16, "end", bold=bold, col=GREEN if val == "?" else INK))
        y += rh
    s.insert(0, "<rect x='2' y='2' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, y - 12, PAPER, EDGE))
    label = "Pay stub: " + ", ".join("%s %s" % (a, b) for a, b, k in rows)
    return svg_wrap(W, y - 8, "".join(s), label)


def receipt_svg(items, rows, title="Receipt"):
    W, rh = 280, 24
    s = [txt(W // 2, 22, title, 17, bold=True)]
    y = 48
    for name, p in items:
        s.append(txt(14, y, name, 16, "start"))
        s.append(txt(W - 14, y, money(p), 16, "end"))
        y += rh
    s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y - 14, W - 10, y - 14, GREY))
    y += 6
    for i, (lab, val) in enumerate(rows):
        last = i == len(rows) - 1
        s.append(txt(14, y, lab, 16, "start", bold=last))
        s.append(txt(W - 14, y, val, 16, "end", bold=last, col=GREEN if val == "?" else INK))
        y += rh
    s.insert(0, "<rect x='2' y='2' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, y - 12, PAPER, EDGE))
    label = "Receipt: " + ", ".join("%s %s" % (n, money(p)) for n, p in items) + "; " + ", ".join("%s %s" % r for r in rows)
    return svg_wrap(W, y - 8, "".join(s), label)


def budget_svg(title, rows, income=None):
    """Monthly budget table: rows = [(item, type_text, amount)]."""
    W, rh, fs = 320, 25, 16
    s = [txt(W // 2, 20, title, 17, bold=True)]
    y = 28
    top = y
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
    for x, t, a in ((12, "Expense", "start"), (186, "Type", "middle"), (W - 12, "Amount", "end")):
        s.append(txt(x, y + 18, t, fs, a, bold=True, col="#ffffff"))
    y += rh
    for item, typ, amt in rows:
        s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
        s.append(txt(12, y + 18, item, fs, "start"))
        s.append(txt(186, y + 18, typ, fs, "middle", col=GREEN if typ == "?" else INK))
        s.append(txt(W - 12, y + 18, money(amt), fs, "end"))
        y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    lab = "Budget %s: " % title + ", ".join("%s %s %s" % (a, b, money(c)) for a, b, c in rows)
    if income is not None:
        s.append(txt(12, y + 22, "Income", fs, "start", bold=True))
        s.append(txt(W - 12, y + 22, money(income), fs, "end", bold=True))
        y += 30
        lab += "; income " + money(income)
    return svg_wrap(W, y + 4, "".join(s), lab)


def register_svg(start, rows):
    """Account record. rows = [(description, withdrawal or None, deposit or None, balance text)]."""
    cols = [(10, "start", "Description"), (285, "end", "Withdrawal"), (375, "end", "Deposit"), (462, "end", "Balance")]
    W, rh, fs = 470, 26, 15
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, rh, GREEN)]
    for x, a, t in cols:
        s.append(txt(x, 20, t, fs, a, bold=True, col="#ffffff"))
    y = 2 + rh
    allrows = [("Starting balance", None, None, money(start))] + rows
    for desc, wd, dp, bal in allrows:
        s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
        s.append(txt(10, y + 18, desc, fs, "start"))
        if wd is not None:
            s.append(txt(285, y + 18, money(wd), fs, "end"))
        if dp is not None:
            s.append(txt(375, y + 18, money(dp), fs, "end"))
        s.append(txt(462, y + 18, bal, fs, "end", bold=bal == "?", col=GREEN if bal == "?" else INK))
        y += rh
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (W - 4, y - 2, EDGE))
    lab = "Account record: starting balance %s; " % money(start) + "; ".join(
        "%s%s%s, balance %s" % (d, ", withdrawal " + money(w) if w is not None else "", ", deposit " + money(p) if p is not None else "", b)
        for d, w, p, b in rows)
    return svg_wrap(W, y + 4, "".join(s), lab)


def goal_svg(saved, goal):
    """Savings goal bar: saved part shaded."""
    W, L, R = 420, 30, 390
    y0, h = 34, 34
    x = L + (R - L) * float(D(saved) / D(goal))
    s = [
        "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, y0, x - L, h, LIGHT),
        "<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (L, y0, R - L, h, GREEN),
        "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 6, x, y0 + h + 6, GREEN),
        txt(L, y0 - 10, "$0", 15), txt("%.1f" % x, y0 - 10, "Saved " + dol(saved), 15, bold=True, col=GREEN),
        txt(R, y0 - 10, "Goal " + dol(goal), 15, "end"),
        txt("%.1f" % ((x + R) / 2), y0 + h + 22, "Still needed: ?", 15, bold=True),
    ]
    return svg_wrap(W, y0 + h + 30, "".join(s), "Savings goal bar: saved %s of %s" % (dol(saved), dol(goal)))


# ============================================================ set 1: income and pay
def set_income(P):
    its = []
    n, he, his, him = P.next()
    its.append(mq("%s earns $18.00 an hour at a grocery store in Surrey. %s works 20 hours this week. What is %s gross pay?" % (n, cap(he), his),
                  D(360), [D(38), D(3600), D(342)],
                  "Gross pay = hourly wage × hours = $18.00 × 20 = <b>$360.00</b>. ($38.00 adds instead of multiplying; "
                  "$342.00 uses 19 hours.)"))
    its.append(mcq("What is <b>gross pay</b>?", "Pay before any deductions are taken off",
                   ["Pay after the deductions are taken off", "Only the money taken off for income tax", "Only the pay for overtime hours"],
                   "Gross pay is everything you earn <b>before</b> deductions. Net pay (take-home pay) is what is left <b>after</b> deductions."))
    its.append(mq("A pay stub shows gross pay of $600.00 and deductions of $90.00. What is the net pay?", D(510),
                  [D(690), D(90), D(600)],
                  "Net pay = gross pay − deductions = $600.00 − $90.00 = <b>$510.00</b>. ($690.00 adds the deductions; "
                  "$600.00 is the gross pay.)"))
    its.append(mcq("Which amounts are usually taken off a paycheque in Canada?", "Income tax, CPP and EI",
                   ["GST and PST", "Rent and groceries", "Bank fees and ATM fees"],
                   "Employers take off <b>income tax</b>, <b>CPP</b> (Canada Pension Plan) and <b>EI</b> (Employment Insurance). "
                   "GST and PST are sales taxes you pay when you buy things, not paycheque deductions."))
    n, he, his, him = P.next()
    its.append(mq("%s earns $17.50 an hour and works 24 hours. What is %s gross pay?" % (n, his), D(420),
                  [D("41.50"), D(408), D(4200)],
                  "$17.50 × 24 = $17 × 24 + $0.50 × 24 = $408 + $12 = <b>$420.00</b>. ($408.00 forgets the 50¢ part; "
                  "$41.50 adds.)"))
    n, he, his, him = P.next()
    assert D("7.5") * 18 == 135
    its.append(mq("%s works a shift of 7 hours 30 minutes at $18.00 an hour. How much does %s earn for the shift?" % (n, he), D(135),
                  [D("131.40"), D(126), D(144)],
                  "30 minutes is half an hour, so the shift is 7.5 hours (not 7.3). $18.00 × 7.5 = <b>$135.00</b>. "
                  "($131.40 uses 7.3 hours; $126.00 forgets the 30 minutes.)"))
    n, he, his, him = P.next()
    assert D("18.50") * 14 == 259
    its.append(mq("%s works 4 hours on Monday, 3.5 hours on Wednesday and 6.5 hours on Saturday at $18.50 an hour. What is %s gross pay?" % (n, his),
                  D(259), [D("240.50"), D(252), D("277.50")],
                  "Hours: 4 + 3.5 + 6.5 = 14 hours. Pay: $18.50 × 14 = <b>$259.00</b>. ($240.50 uses 13 hours; "
                  "$252.00 uses $18 an hour.)"))
    its.append(mq("Gross pay is $800.00. Deductions are 20% of gross pay. What is the net pay?", D(640),
                  [D(160), D(780), D(960)],
                  "Deductions: 20% of $800 = $160. Net pay: $800 − $160 = <b>$640.00</b>. ($160.00 is the deductions; "
                  "$780.00 subtracts 20 dollars, not 20%.)"))
    its.append(mq("In BC, overtime is usually paid at time and a half: 1.5 times the regular wage. What is the overtime rate for a $20.00 hourly wage?",
                  D(30), [D("21.50"), D(40), D("20.50")],
                  "Time and a half = 1.5 × $20.00 = <b>$30.00 an hour</b>. ($40.00 is double time; $21.50 adds $1.50.)"))
    n, he, his, him = P.next()
    its.append(mq("%s earns $20.00 an hour. One day %s works 10 hours: 8 regular hours and 2 overtime hours at time and a half. "
                  "What is %s pay for the day?" % (n, he, his), D(220), [D(200), D(300), D(240)],
                  "Regular: 8 × $20 = $160. Overtime: 2 × $30 = $60. Total: <b>$220.00</b>. ($200.00 forgets the overtime rate; "
                  "$300.00 pays all 10 hours at $30.)"))
    its.append(mq("A job pays a salary of %s a year. How much is that per month?" % dol(48000), D(4000),
                  [D(4800), D(2000), D(576000)],
                  "There are 12 months in a year. %s ÷ 12 = <b>$4000.00</b> a month. ($4800.00 divides by 10; "
                  "$2000.00 divides by 24, which is twice a month.)" % dol(48000)))
    its.append(mq("A worker earns %s a year and is paid every two weeks (26 pays a year). How much is each gross pay?" % dol(46800), D(1800),
                  [D(3900), D(900), D(1950)],
                  "%s ÷ 26 = <b>$1800.00</b>. ($3900.00 divides by 12, which is monthly; $900.00 divides by 52, which is weekly; "
                  "$1950.00 divides by 24, which is twice a month.)" % dol(46800)))
    its.append(mq("A job pays $20.00 an hour for 40 hours a week. What is the gross pay for 52 weeks?", D(41600),
                  [D(800), D(1040), D(3200)],
                  "One week: $20 × 40 = $800. One year: $800 × 52 = <b>$41" + NB + "600.00</b>. ($800.00 is one week; "
                  "$1040.00 forgets the 40 hours; $3200.00 is only 4 weeks.)"))
    n, he, his, him = P.next()
    assert D("0.16") * 1500 == 240
    its.append(mq("Tree planters in BC are often paid for each tree they plant. %s earns 16¢ a tree and plants 1500 trees in a day. "
                  "How much does %s earn?" % (n, he), D(240), [D(24), D(2400), D(1516)],
                  "16¢ = $0.16. $0.16 × 1500 = <b>$240.00</b>. ($24.00 and $2400.00 put the decimal point in the wrong place; "
                  "$1516.00 adds.)"))
    n, he, his, him = P.next()
    its.append(mq("%s sells bikes in Kelowna and earns 5%% commission on %s sales. %s sells %s of bikes this month. How much commission does %s earn?"
                  % (n, his, cap(he), dol(6000), he), D(300), [D(30), D(3000), D(1200)],
                  "5% = 0.05. $6000 × 0.05 = <b>$300.00</b>. Or: 10% is $600, so 5% is $300. ($3000.00 is 50%; "
                  "$1200.00 divides by 5.)"))
    assert D("17.50") * 30 == 525
    its.append(mcq("Job A pays $17.50 an hour for 30 hours a week. Job B pays $480 a week. Which job pays more each week, and by how much?",
                   "Job A, by $45", ["Job B, by $45", "Job B, by $462.50", "They pay the same"],
                   "Job A: $17.50 × 30 = $525. Job B: $480. $525 − $480 = $45, so <b>Job A pays $45 more</b>. "
                   "($462.50 subtracts the hourly wage from $480.)"))
    rows = [("Gross pay", "$1200.00", "g"), ("Income tax", "$118.20", "d"), ("CPP", "$63.39", "d"),
            ("EI", "$19.56", "d"), ("Net pay", "?", "t")]
    ded = D("118.20") + D("63.39") + D("19.56")
    assert ded == D("201.15")
    its.append(mq(fig(stub_svg(rows)) + "What is the net pay on this pay stub?", 1200 - ded,
                  [1200 + ded, 1200 - D("118.20"), ded],
                  "Add the deductions: $118.20 + $63.39 + $19.56 = $201.15. Net pay: $1200.00 − $201.15 = <b>$998.85</b>. "
                  "($1081.80 subtracts only the income tax; $1401.15 adds the deductions.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s gross pay is $600 and %s net pay is $510. What percent of %s gross pay was deducted?" % (n, his, his),
                   "15%", ["85%", "90%", "17.6%"],
                   "Deducted: $600 − $510 = $90. Compare with the <b>gross</b> pay: $90 ÷ $600 = 0.15 = <b>15%</b>. "
                   "(85% is the part kept; 17.6% divides by the net pay; 90% uses the dollars.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s earns $18.00 an hour. Last week %s gross pay was $378.00. How many hours did %s work?" % (n, his, he),
                   "21 hours", ["2.1 hours", "210 hours", "396 hours"],
                   "Hours = pay ÷ wage = $378 ÷ $18 = <b>21 hours</b>. Check: $18 × 21 = $378. "
                   "(2.1 and 210 put the decimal point in the wrong place; 396 adds.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s wage goes up from $18.00 to $18.90 an hour. What is the percent increase?" % n,
                   "5%", ["0.9%", "90%", "4.8%"],
                   "Increase: $18.90 − $18.00 = $0.90. Compare with the <b>old</b> wage: $0.90 ÷ $18.00 = 0.05 = <b>5%</b>. "
                   "(4.8% divides by the new wage; 0.9% uses the dollars.)"))
    assert len(its) == 20
    return {"title": "Income: wages, gross pay and net pay", "items": its}


# ============================================================ set 2: budgets
FV = ["Fixed: the amount is the same each month", "Variable: the amount changes from month to month"]


def set_budget(P):
    its = []
    its.append(mcq("Which of these is a <b>fixed</b> expense?", "Monthly rent", ["Groceries", "Movies and games", "Gas for the car"],
                   "A fixed expense is the same amount every month. <b>Rent</b> is set in the lease. Groceries, movies and gas "
                   "change with how much you buy or use, so they are variable."))
    its.append(mcq("Which of these is a <b>variable</b> expense?", "Groceries",
                   ["Monthly rent", "A $45-a-month phone plan", "A monthly car insurance payment"],
                   "<b>Groceries</b> change from month to month, so they are variable. Rent, a set phone plan and an insurance "
                   "payment are the same each month, so they are fixed."))
    its.append(mcq("A student buys a monthly transit pass for SkyTrain and buses. It costs the same every month. What type of expense is it?",
                   FV[0], [FV[1], "It is income, not an expense", "It is a deduction from pay"],
                   "The price of the pass is the same each month, so it is <b>fixed</b>, even if the student rides more in some months. "
                   "(Calling it variable mixes up how much you use it with how much you pay.)"))
    its.append(mcq("A family’s electricity bill is higher in winter and lower in summer. What type of expense is it?",
                   FV[1], [FV[0], "It is income, not an expense", "It is a deduction from pay"],
                   "The bill changes with how much power the family uses, so it is <b>variable</b>. "
                   "(Paying a bill every month does not make it fixed; the amount must stay the same.)"))
    n, he, his, him = P.next()
    rows = [("Rent", "Fixed", D(900)), ("Phone plan", "Fixed", D(45)), ("Transit pass", "Fixed", D(110)),
            ("Groceries", "Variable", D(320)), ("Entertainment", "Variable", D(80))]
    its.append(mq(fig(budget_svg("%s’s monthly budget" % n, rows)) + "What is the total of %s’s <b>fixed</b> expenses?" % n,
                  D(1055), [D(1455), D(400), D(1135)],
                  "Add only the fixed rows: $900 + $45 + $110 = <b>$1055.00</b>. ($1455.00 adds every row; $400.00 is the "
                  "variable total; $1135.00 counts Entertainment as fixed.)"))
    n, he, his, him = P.next()
    its.append(mq("%s’s variable expenses this month are food $260, clothes $75 and fun $90. %s fixed expenses are rent $850 and phone $50. "
                  "What is the total of %s <b>variable</b> expenses?" % (n, cap(his), his),
                  D(425), [D(900), D(1325), D(475)],
                  "Variable: $260 + $75 + $90 = <b>$425.00</b>. ($900.00 is the fixed total; $1325.00 adds everything; "
                  "$475.00 counts the phone as variable.)"))
    its.append(mcq("A monthly budget has income of $2400 and expenses of $2150. What is the result?",
                   "A surplus of $250", ["A deficit of $250", "A surplus of $4550", "A deficit of $2150"],
                   "Income − expenses = $2400 − $2150 = $250. Income is more than expenses, so it is a <b>surplus of $250</b>: "
                   "money left over to save."))
    its.append(mcq("A monthly budget has income of $1800 and expenses of $1950. What is the result?",
                   "A deficit of $150", ["A surplus of $150", "A deficit of $3750", "A surplus of $1950"],
                   "Income − expenses = $1800 − $1950 = −$150. Expenses are more than income, so it is a <b>deficit of $150</b>."))
    assert D(90) * 52 / 12 == 390
    its.append(mq("A family spends $90 a week on groceries. About how much is that per month? (Use 52 weeks in a year.)", D(390),
                  [D(360), D(1080), D(4680)],
                  "$90 × 52 = $4680 a year. $4680 ÷ 12 = <b>$390.00 a month</b>. ($360.00 uses 4 weeks a month, but most months "
                  "are a bit more than 4 weeks; $4680.00 is the whole year.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s monthly income is $3000 after deductions. Rent is $1050. What percent of %s income goes to rent?" % (n, his),
                   "35%", ["65%", "3.5%", "28.6%"],
                   "$1050 ÷ $3000 = 0.35 = <b>35%</b>. (65% is the rest of the income; 28.6% divides the wrong way round.)"))
    its.append(mq("One budget plan is 50/30/20: 50% for needs, 30% for wants and 20% for savings. With a monthly income of $2800, "
                  "how much goes to savings?", D(560), [D(1400), D(840), D(280)],
                  "20% of $2800: 10% is $280, so 20% is <b>$560.00</b>. ($1400.00 is the 50% for needs; $840.00 is the 30% for wants; "
                  "$280.00 is only 10%.)"))
    n, he, his, him = P.next()
    its.append(mq("%s spends $160 a month on entertainment. %s cuts it by 25%%. What is the new amount?" % (n, cap(he)), D(120),
                  [D(135), D(40), D(200)],
                  "25% of $160 = $40. New amount: $160 − $40 = <b>$120.00</b>. ($135.00 subtracts 25 dollars; $40.00 is the cut; "
                  "$200.00 adds 25%.)"))
    its.append(mq("Monthly income is $2200 and fixed expenses are $1400. What is the most the variable expenses can be without a deficit?",
                  D(800), [D(3600), D(1400), D(2200)],
                  "Money left after fixed expenses: $2200 − $1400 = <b>$800.00</b>. Variable expenses must stay at or below this. "
                  "($3600.00 adds.)"))
    its.append(mq("Car insurance costs $1440 a year. How much should a monthly budget set aside for it?", D(120),
                  [D(144), D(17280), D(360)],
                  "$1440 ÷ 12 months = <b>$120.00 a month</b>. ($144.00 divides by 10; $360.00 divides by 4; "
                  "$17" + NB + "280.00 multiplies by 12.)"))
    n, he, his, him = P.next()
    rows = [("Rent", "Fixed", D(700)), ("Internet", "Fixed", D(60)), ("Food", "?", D(350)), ("Bus pass", "Fixed", D(57))]
    its.append(mcq(fig(budget_svg("%s’s monthly budget" % n, rows)) + "Which word belongs in the empty Type box for Food?",
                   "Variable", ["Fixed", "Income", "Surplus"],
                   "The amount spent on food changes with what you buy, so food is <b>variable</b>. "
                   "Rent, internet and a bus pass are the same each month, so they are fixed."))
    n, he, his, him = P.next()
    its.append(mq("%s’s monthly income is $2000. Fixed expenses are $1200 and variable expenses are $650. %s wants to save $250 a month. "
                  "By how much must %s cut %s variable expenses?" % (n, cap(he), he, his), D(100),
                  [D(250), D(150), D(350)],
                  "Now: $2000 − $1200 − $650 = $150 left. To save $250, %s needs $250 − $150 = <b>$100.00</b> more. "
                  "(Fixed expenses like rent are hard to change, so the cut comes from variable expenses. "
                  "$250.00 forgets the $150 already left.)" % he))
    its.append(mcq("A family’s grocery spending goes up from $400 to $440 a month. What is the percent increase?",
                   "10%", ["40%", "9.1%", "110%"],
                   "Increase: $40. Compare with the <b>old</b> amount: $40 ÷ $400 = 0.1 = <b>10%</b>. "
                   "(9.1% divides by the new amount; 110% is the new amount as a percent of the old.)"))
    its.append(mq("A budget for a monthly income of $2500 uses 40% for rent, 25% for food and 15% for transportation. "
                  "The rest goes to savings. How much is saved?", D(500), [D(2000), D(375), D(200)],
                  "Rent, food and transportation: 40% + 25% + 15% = 80%. Savings: 100% − 80% = 20%. 20% of $2500 = <b>$500.00</b>. "
                  "($2000.00 is the 80% spent; $375.00 is 15%.)"))
    assert (D(640) * 52 / 12).quantize(CENT) == D("2773.33")
    its.append(mq("%s is paid $640 every week. About how much is that per month? (Use 52 weeks in a year.)" % P.next()[0],
                  D("2773.33"), [D(2560), D(7680), D(33280)],
                  "$640 × 52 = %s a year. %s ÷ 12 = <b>$2773.33</b> a month (rounded to the cent). "
                  "($2560.00 uses 4 weeks a month; $7680.00 multiplies by 12; %s is the whole year.)" % (dol(33280), dol(33280), money(33280))))
    n, he, his, him = P.next()
    left = 1000 - (55 + 110 + 35) - (240 + 180)
    assert left == 380
    its.append(mcq("%s earns $1000 a month. Fixed expenses: phone $55, transit pass $110, gym $35. Variable expenses: food $240, fun $180. "
                   "%s saves the rest. What percent of %s income does %s save?" % (n, cap(he), his, he),
                   "38%", ["62%", "80%", "58%"],
                   "Expenses: $55 + $110 + $35 + $240 + $180 = $620. Saved: $1000 − $620 = $380. $380 ÷ $1000 = <b>38%</b>. "
                   "(62% is the part spent; 80% forgets the variable expenses; 58% forgets the fixed expenses.)"))
    assert len(its) == 20
    return {"title": "Budgets: fixed and variable expenses", "items": its}


# ============================================================ set 3: transactions with GST and PST
def set_tax(P):
    its = []
    its.append(mq("A $30 adult phone case has 5% GST and 7% PST added. How much tax is that in total?", both(30),
                  [D(12), D("1.50"), D("33.60")],
                  "GST: $30 × 0.05 = $1.50. PST: $30 × 0.07 = $2.10. Total tax: <b>$3.60</b> (12% of $30). "
                  "($12.00 adds 12 dollars, not 12%; $1.50 is only the GST.)"))
    assert with_tax(45) == D("50.40")
    its.append(mq("An adult bike helmet costs $45 before tax. 5% GST and 7% PST are added. What is the total?", with_tax(45),
                  [D(57), D("47.25"), D("45.12")],
                  "Tax: 12% of $45 = $5.40. Total: $45 + $5.40 = <b>$50.40</b>. Or: $45 × 1.12. ($47.25 adds only the GST; "
                  "$57.00 adds $12.)"))
    n, he, his, him = P.next()
    assert with_tax(24) == D("26.88")
    its.append(mcq("%s has $25. A video game has a price tag of $24. 5%% GST and 7%% PST are added at the till. Can %s buy it?" % (n, he),
                   "No, the total is $26.88", ["Yes, and $1.00 is left over", "Yes, the total is $24.12", "No, the total is $36.00"],
                   "Tax: 12% of $24 = $2.88. Total: $24 + $2.88 = $26.88, which is more than $25. <b>No</b>. "
                   "(Forgetting the tax makes it look like $1 is left over.)"))
    items = [("Notebook", D("6.50")), ("Calculator", D("18.50"))]
    sub = D(25)
    assert gst(sub) == D("1.25") and pst(sub) == D("1.75")
    its.append(mq(fig(receipt_svg(items, [("Subtotal", money(sub)), ("GST 5%", "$1.25"), ("PST 7%", "$1.75"), ("Total", "?")]))
                  + "What is the total on this receipt?", D(28), [D(37), D("26.25"), D("26.75")],
                  "Subtotal + GST + PST = $25.00 + $1.25 + $1.75 = <b>$28.00</b>. ($26.25 forgets the PST; $26.75 forgets the GST; "
                  "$37.00 adds $12.)"))
    its.append(mq("A family’s restaurant meal in Nanaimo costs $36 before tax. Restaurant meals in BC have 5% GST but no PST. What is the total?",
                  36 + gst(36), [with_tax(36), D("1.80"), D("38.52")],
                  "GST only: $36 × 0.05 = $1.80. Total: $36 + $1.80 = <b>$37.80</b>. ($40.32 adds PST too, but restaurant meals "
                  "have no PST.)"))
    its.append(mq("A child’s winter jacket costs $45. Children’s clothing in BC has 5% GST but no PST. What is the total?",
                  45 + gst(45), [with_tax(45), D("2.25"), D("45.05")],
                  "GST only: $45 × 0.05 = $2.25. Total: <b>$47.25</b>. ($50.40 adds PST too; $45.05 adds 5¢ instead of 5%.)"))
    its.append(mcq("In Canada, which payment is rounded to the nearest 5¢?", "A cash payment",
                   ["A debit card payment", "A credit card payment", "Every payment"],
                   "Canada has no pennies, so only <b>cash</b> totals round to the nearest 5¢. Debit and credit payments are exact to the cent."))
    n, he, his, him = P.next()
    t = with_tax("11.99")
    assert t == D("13.43") and cash(t) == D("13.45")
    its.append(mq("%s buys an $11.99 phone charger. 5%% GST and 7%% PST make the total $13.43. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                  D("13.45"), [t, D("13.40"), D("13.50")],
                  "Cash rounds to the nearest 5¢. $13.43 is between $13.40 and $13.45 and closer to $13.45, so %s pays <b>$13.45</b>. "
                  "($13.43 is the exact debit amount; $13.40 rounds the wrong way.)" % he))
    t = with_tax("14.25")
    assert gst("14.25") == D("0.71") and pst("14.25") == D("1.00") and t == D("15.96") and cash(t) == D("15.95")
    its.append(mq("A $14.25 adult T-shirt has 5% GST and 7% PST added. You pay with a $20 bill. How much change do you get?",
                  D("4.05"), [D("4.04"), D("5.75"), D("4.10")],
                  "GST: $0.71. PST: $1.00. Total: $15.96. Cash rounds to $15.95. Change: $20.00 − $15.95 = <b>$4.05</b>. "
                  "($4.04 forgets the cash rounding; $5.75 forgets the tax.)"))
    assert with_tax(60) == D("67.20") and D(75) * D("0.92") == 69
    its.append(mq("Adult running shoes cost $75 and are 20% off. 5% GST and 7% PST are added to the sale price. What is the total?",
                  D("67.20"), [D(69), D(60), D(84)],
                  "Sale price: $75 − $15 = $60. Tax: 12% of $60 = $7.20. Total: <b>$67.20</b>. ($69.00 takes 20% off and adds 12% "
                  "in one step: $75 × 0.92; $60.00 forgets the tax; $84.00 forgets the discount.)"))
    assert with_tax(45) == D("50.40") and with_tax(55) - 10 == D("51.60")
    its.append(mq("A $55 item has a $10-off coupon. GST and PST (12%) are charged on the price after the coupon. What is the total?",
                  D("50.40"), [D("51.60"), D(45), D("49.40")],
                  "Coupon first: $55 − $10 = $45. Tax: 12% of $45 = $5.40. Total: <b>$50.40</b>. ($51.60 adds tax before the "
                  "coupon: $61.60 − $10; $45.00 forgets the tax.)"))
    assert with_tax("12.75") == D("14.28") and D("12.75") + gst("12.75") == D("13.39")
    its.append(mq("You buy 3 notebooks at $4.25 each. 5% GST and 7% PST are added. What is the total?", D("14.28"),
                  [D("12.75"), D("24.75"), D("13.39")],
                  "Subtotal: 3 × $4.25 = $12.75. Tax: 12% of $12.75 = $1.53. Total: <b>$14.28</b>. ($12.75 forgets the tax; "
                  "$13.39 adds only GST; $24.75 adds $12.)"))
    assert with_tax(80) == D("89.60") and (D("89.60") * D("0.88")).quantize(CENT) == D("78.85")
    its.append(mq("A receipt total is $89.60. It includes 5% GST and 7% PST. What was the price before tax?", D(80),
                  [D("78.85"), D("77.60"), D("100.35")],
                  "The total is 112% of the price. Price = $89.60 ÷ 1.12 = <b>$80.00</b>. Check: $80 × 1.12 = $89.60. "
                  "($78.85 takes 12% of the total, but the tax was 12% of the price; $77.60 subtracts $12.)"))
    assert with_tax(120) == D("134.40")
    its.append(mcq("Store A sells a jacket for $120 plus GST and PST (12%). Store B sells the same jacket for $132 with tax included. Which is cheaper?",
                   "Store B, by $2.40", ["Store A, by $12.00", "Store A, by $2.40", "They cost the same"],
                   "Store A: $120 × 1.12 = $134.40. Store B: $132.00. <b>Store B is cheaper by $2.40</b>. "
                   "(Store A by $12 forgets to add tax to Store A’s price.)"))
    t = 40 + gst(40) + with_tax(25)
    assert t == 70
    its.append(mq("You buy a pair of children’s shoes for $40 (5% GST only) and an adult shirt for $25 (5% GST and 7% PST). What is the total?",
                  t, [D("72.80"), D("68.25"), D(65)],
                  "Shoes: $40 + $2.00 = $42.00. Shirt: $25 + $3.00 = $28.00. Total: <b>$70.00</b>. ($72.80 adds 12% to both; "
                  "$68.25 adds only GST to both; $65.00 forgets the tax.)"))
    n, he, his, him = P.next()
    its.append(mq("%s returns a $30 adult item %s paid for with 5%% GST and 7%% PST. The store refunds the price and the tax. How much is the refund?" % (n, he),
                  with_tax(30), [D(30), D("26.40"), D(42)],
                  "The refund includes the tax that was paid: $30 + $3.60 = <b>$33.60</b>. ($30.00 forgets the tax; "
                  "$26.40 subtracts the tax.)"))
    t = with_tax("199.99")
    assert gst("199.99") == D("10.00") and pst("199.99") == D("14.00") and t == D("223.99")
    its.append(mq("A phone costs $199.99. 5% GST and 7% PST are added, each rounded to the cent. What is the total?", t,
                  [D("211.99"), D("209.99"), D("213.99")],
                  "GST: $199.99 × 0.05 = $9.9995 → $10.00. PST: $199.99 × 0.07 = $13.9993 → $14.00. Total: $199.99 + $24.00 = "
                  "<b>$223.99</b>. ($209.99 adds only GST; $213.99 adds only PST; $211.99 adds $12.)"))
    assert with_tax(30) == D("33.60") and with_tax(45) == D("50.40")
    its.append(mq("Adult T-shirts are $15 each with a deal: buy 2, get the third one free. You take 3 T-shirts. "
                  "5% GST and 7% PST are added. What is the total?", D("33.60"), [D("50.40"), D(30), D("31.50")],
                  "You pay for 2: $30. Tax: 12% of $30 = $3.60. Total: <b>$33.60</b>. ($50.40 pays for all 3; $30.00 forgets the tax; "
                  "$31.50 adds only GST.)"))
    n, he, his, him = P.next()
    t = with_tax(72)
    assert t == D("80.64") and cash(t) == D("80.65") and 100 - D(96) * D("0.87") == D("16.48")
    its.append(mq("%s buys a $96 adult hockey stick at 25%% off. 5%% GST and 7%% PST are added. %s pays with a $100 bill. How much change does %s get?" % (n, cap(he), he),
                  D("19.35"), [D("19.36"), D(28), D("16.48")],
                  "Sale price: $96 − $24 = $72. Tax: 12% of $72 = $8.64. Total: $80.64, which rounds to $80.65 for cash. "
                  "Change: $100.00 − $80.65 = <b>$19.35</b>. ($19.36 forgets the cash rounding; $28.00 forgets the tax; "
                  "$16.48 uses $96 × 0.87, which mixes the discount and tax into one step.)"))
    n, he, his, him = P.next()
    t = 18 + gst(18) + with_tax(20)
    assert t == D("41.30") and cash(t) == D("41.30")
    its.append(mq("At a store in Prince George, %s buys a child’s hoodie for $18 (5%% GST only) and an adult cap for $20 (5%% GST and 7%% PST). "
                  "%s pays with two $20 bills and a toonie. How much change does %s get?" % (n, cap(he), he),
                  D("0.70"), [D("4.00"), D("2.10"), D("0.85")],
                  "Hoodie: $18 + $0.90 = $18.90. Cap: $20 + $2.40 = $22.40. Total: $41.30 (already a multiple of 5¢). "
                  "Paid: $40 + $2 = $42. Change: $42.00 − $41.30 = <b>$0.70</b>. ($4.00 forgets the tax; $2.10 adds only GST to both; "
                  "$0.85 puts the PST on the hoodie instead of the cap.)"))
    assert 42 - 38 * D("1.05") == D("2.10") and 42 - cash(with_tax(18) + 20 + gst(20)) == D("0.85")
    assert len(its) == 20
    return {"title": "Transactions with GST and PST", "items": its}


# ============================================================ set 4: bank balances and fees
def set_bank(P):
    its = []
    its.append(mcq("Which transaction <b>increases</b> a bank account balance?", "A paycheque deposit",
                   ["A debit card purchase", "A monthly account fee", "An ATM withdrawal"],
                   "A <b>deposit</b> adds money to the account. Purchases, fees and withdrawals take money out."))
    its.append(mq("A bank account has $285.00. A deposit of $145.00 is made. What is the new balance?", D(430),
                  [D(140), D(320), D(420)],
                  "A deposit is added: $285 + $145 = <b>$430.00</b>. ($140.00 subtracts; $420.00 loses one carried 1 and $320.00 loses both.)"))
    its.append(mq("A bank account has $430.00. A withdrawal of $65.50 is made. What is the new balance?", D("364.50"),
                  [D("495.50"), D("375.50"), D("365.50")],
                  "A withdrawal is subtracted: $430.00 − $65.50 = <b>$364.50</b>. ($495.50 adds; $375.50 and $365.50 are "
                  "regrouping slips.)"))
    rows = [("Pay deposit", None, D(150), "$350.00"), ("Debit: jacket", D("75.25"), None, "$274.75"), ("ATM withdrawal", D(40), None, "?")]
    assert 200 + 150 - D("75.25") - 40 == D("234.75")
    its.append(mq(fig(register_svg(D(200), rows)) + "What is the balance after the ATM withdrawal?", D("234.75"),
                  [D("314.75"), D(310), D("465.25")],
                  "Start from the last balance and subtract: $274.75 − $40.00 = <b>$234.75</b>. ($314.75 adds the withdrawal; "
                  "$310.00 forgets the jacket; $465.25 adds every amount.)"))
    its.append(mq("A bank account has a fee of $4.95 a month. How much are the fees for a whole year?", 12 * D("4.95"),
                  [D("4.95"), 52 * D("4.95"), D("49.50")],
                  "12 months × $4.95 = <b>$59.40</b>. ($257.40 uses 52, the number of weeks; $49.50 uses 10.)"))
    its.append(mq("A bank plan includes 12 free transactions a month. Each extra transaction costs $1.25. "
                  "How much is charged for 17 transactions?", 5 * D("1.25"), [17 * D("1.25"), 12 * D("1.25"), 6 * D("1.25")],
                  "Extra transactions: 17 − 12 = 5. Fee: 5 × $1.25 = <b>$6.25</b>. ($21.25 charges all 17; $15.00 charges the 12 free "
                  "ones; $7.50 uses 6.)"))
    n, he, his, him = P.next()
    its.append(mq("%s takes $60 from another bank’s ATM. That ATM charges $3.50 and %s own bank charges $2.00. "
                  "By how much does %s balance go down?" % (n, his, his), D("65.50"), [D(60), D("63.50"), D(62)],
                  "$60.00 + $3.50 + $2.00 = <b>$65.50</b>. ($60.00 forgets both fees; $63.50 and $62.00 forget one fee.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s account has $40.00. %s makes a $65.00 debit purchase, and the account has overdraft protection. What is the new balance?" % (n, cap(he)),
                   MINUS + "$25.00", ["$25.00", "$105.00", MINUS + "$105.00"],
                   "$40 − $65 = −$25. The balance is <b>−$25.00</b>: %s owes the bank $25. (A positive $25.00 drops the sign; "
                   "$105.00 adds.)" % he))
    its.append(mcq("An account balance is " + MINUS + "$25.00. The bank charges a $5.00 overdraft fee. What is the new balance?",
                   MINUS + "$30.00", [MINUS + "$20.00", "$30.00", "$20.00"],
                   "A fee takes money away: −$25 − $5 = <b>−$30.00</b>. The account is now further below zero. "
                   "(−$20.00 adds the fee as if it were a deposit.)"))
    its.append(mcq("Plan A has no monthly fee but charges $1.00 for each transaction. Plan B costs $10.95 a month with unlimited transactions. "
                   "With 15 transactions a month, which plan is cheaper, and by how much?",
                   "Plan B, by $4.05", ["Plan A, by $4.05", "Plan A, by $10.95", "Plan B, by $15.00"],
                   "Plan A: 15 × $1.00 = $15.00. Plan B: $10.95. $15.00 − $10.95 = $4.05, so <b>Plan B is cheaper by $4.05</b>."))
    its.append(mcq("Plan A charges $1.00 for each transaction and has no monthly fee. Plan B costs $10.95 a month. "
                   "For how many transactions a month is Plan B cheaper?", "11 or more", ["10 or more", "12 or more", "15 or more"],
                   "10 transactions on Plan A cost $10.00, less than $10.95. 11 transactions cost $11.00, more than $10.95. "
                   "So Plan B is cheaper for <b>11 or more</b>."))
    n, he, his, him = P.next()
    its.append(mq("%s’s bank charges $1.50 for each e-transfer. %s sends $40 to a friend by e-transfer. How much leaves %s account?" % (n, cap(he), his),
                  D("41.50"), [D(40), D("38.50"), D("1.50")],
                  "The amount sent plus the fee: $40.00 + $1.50 = <b>$41.50</b>. ($38.50 subtracts the fee; $40.00 forgets it.)"))
    its.append(mq("A savings account pays 1.5% interest per year. How much simple interest does $2000 earn in 1 year?", D(30),
                  [D(300), D(3), D(2030)],
                  "1.5% = 0.015. $2000 × 0.015 = <b>$30.00</b>. ($300.00 uses 15%; $3.00 uses 0.15%; $2030.00 is the balance, not the interest.)"))
    n, he, his, him = P.next()
    its.append(mq("%s’s online banking shows a balance of $512.40. A debit purchase of $85.00 is still pending and has not been taken off yet. "
                  "How much money does %s really have to spend?" % (n, he), D("427.40"), [D("597.40"), D("512.40"), D("437.40")],
                  "The pending purchase will come out: $512.40 − $85.00 = <b>$427.40</b>. ($597.40 adds it; $512.40 ignores it.)"))
    its.append(mq("An account starts at $300.00 and ends at $245.00. During the month there was a deposit of $50.00, "
                  "a withdrawal of $80.00 and one more withdrawal. How much was the other withdrawal?", D(25),
                  [D(55), D(105), D(85)],
                  "$300 + $50 − $80 = $270. $270 − $245 = <b>$25.00</b>. Check: $300 + $50 − $80 − $25 = $245. "
                  "($55.00 is only the start minus the end; $105.00 forgets the $80 withdrawal; $85.00 swaps the deposit and the withdrawal.)"))
    n, he, his, him = P.next()
    v = 180 + 420 - 55 - D("3.95")
    assert v == D("541.05")
    its.append(mq("%s’s account starts the month at $180.00. %s pay of $420.00 is deposited, %s phone bill of $55.00 is paid, "
                  "and the bank charges a $3.95 monthly fee. What is the balance at the end of the month?" % (n, cap(his), his),
                  v, [v + 2 * D("3.95"), D(545), D("658.95")],
                  "$180.00 + $420.00 − $55.00 − $3.95 = <b>$541.05</b>. ($548.95 adds the fee; $545.00 forgets the fee; "
                  "$658.95 adds the phone bill.)"))
    n, he, his, him = P.next()
    assert 150 - with_tax(60) == D("82.80")
    its.append(mq("%s has $150.00 in %s account. %s buys a $60 adult jacket by debit, and 5%% GST and 7%% PST are added. What is the new balance?" % (n, his, cap(he)),
                  D("82.80"), [D(90), D("217.20"), D(87)],
                  "Total: $60 × 1.12 = $67.20. Balance: $150.00 − $67.20 = <b>$82.80</b>. Debit is exact, so there is no rounding. "
                  "($90.00 forgets the tax; $87.00 adds only GST.)"))
    n, he, his, him = P.next()
    its.append(mq("%s pays $3.95 a month for %s bank account. A student account has no monthly fee. How much would %s save in 2 years by switching?" % (n, his, he),
                  24 * D("3.95"), [12 * D("3.95"), 2 * D("3.95"), 104 * D("3.95")],
                  "2 years = 24 months. 24 × $3.95 = <b>$94.80</b>. ($47.40 is only 1 year; $7.90 is 2 months; "
                  "$410.80 uses 104 weeks.)"))
    rows = [("Deposit: birthday", None, D(75), "$195.40"), ("Debit: groceries", D("48.65"), None, "?"),
            ("Monthly fee", D("4.95"), None, "$141.80")]
    assert D("195.40") - 75 == D("120.40") and D("195.40") - D("48.65") == D("146.75") and D("146.75") - D("4.95") == D("141.80")
    its.append(mq(fig(register_svg(D("120.40"), rows)) + "What balance belongs in the empty box?", D("146.75"),
                  [D("244.05"), D("71.75"), D("141.80")],
                  "$195.40 − $48.65 = <b>$146.75</b>. Check the next row: $146.75 − $4.95 = $141.80. ($244.05 adds the purchase; "
                  "$71.75 starts from $120.40 and skips the deposit; $141.80 is the balance after the fee.)"))
    n, he, his, him = P.next()
    v = D("85.40") - 45 - D("12.60") + D("236.25") - D("4.95")
    assert v == D("259.10")
    its.append(mq("%s’s account has $85.40. This month %s pays a $45.00 phone bill, buys lunch for $12.60 by debit, gets a pay deposit of $236.25 "
                  "and is charged a $4.95 account fee. What is the balance at the end of the month?" % (n, he),
                  v, [v + D("4.95"), v + 2 * D("4.95"), v + 2 * D("12.60")],
                  "$85.40 − $45.00 − $12.60 + $236.25 − $4.95 = <b>$259.10</b>. ($264.05 forgets the fee; $269.00 adds the fee; "
                  "$284.30 adds the lunch instead of subtracting it.)"))
    assert len(its) == 20
    return {"title": "Bank balances and fees", "items": its}


# ============================================================ set 5: saving goals and word problems
def set_goals(P):
    its = []
    n, he, his, him = P.next()
    its.append(mq("%s saves $15 a week for 8 weeks. How much does %s save?" % (n, he), D(120), [D(23), D(135), D(105)],
                  "$15 × 8 = <b>$120.00</b>. ($23.00 adds; $135.00 is 9 weeks; $105.00 is 7 weeks.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s wants to save $180 and puts away $20 a week. How many weeks will it take?" % n,
                   "9 weeks", ["8 weeks", "10 weeks", "160 weeks"],
                   "$180 ÷ $20 = <b>9 weeks</b>. Check: 9 × $20 = $180. (160 subtracts instead of dividing.)"))
    n, he, his, him = P.next()
    its.append(mq(fig(goal_svg(260, 400)) + "%s is saving for a $400 used e-bike and has saved $260. How much more does %s need?" % (n, he),
                  D(140), [D(260), D(660), D(35)],
                  "Still needed = goal − saved = $400 − $260 = <b>$140.00</b>. ($660.00 adds; $260.00 is the amount saved; $35.00 is the percent still needed, 35%, not dollars.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s has saved $340 toward a $400 goal. What percent of the goal has %s reached?" % (n, he),
                   "85%", ["15%", "34%", "60%"],
                   "$340 ÷ $400 = 0.85 = <b>85%</b>. (15% is the part still needed; 34% uses the dollars; 60% subtracts 340 from 400.)"))
    t = with_tax(250)
    assert t == 280 and ceil_div(t, 30) == 10 and ceil_div(250, 30) == 9
    n, he, his, him = P.next()
    its.append(mcq("%s wants a $250 adult bike. 5%% GST and 7%% PST are added. %s saves $30 a week. How many weeks until %s can buy it?" % (n, cap(he), he),
                   "10 weeks", ["9 weeks", "8 weeks", "9.33 weeks"],
                   "Total: $250 × 1.12 = $280. $280 ÷ $30 = 9.33..., so after 9 weeks there is only $270. Round <b>up</b> to "
                   "<b>10 weeks</b>. (9 weeks forgets the tax or rounds down; 8 weeks forgets the tax and rounds down; "
                   "9.33 weeks does not round to whole weeks.)"))
    n, he, his, him = P.next()
    assert pct(360, 15) == 54 and 810 / 54 == 15
    its.append(mcq("%s earns $360 a week and saves 15%% of it. How many weeks will it take to save $810?" % n,
                   "15 weeks", ["3 weeks", "54 weeks", "2.25 weeks"],
                   "Saved each week: 15% of $360 = $54. $810 ÷ $54 = <b>15 weeks</b>. (2.25 weeks divides by the whole $360 pay; "
                   "54 is the dollars saved each week, not the weeks; 3 weeks uses $810 ÷ $270, the part not saved.)"))
    n, he, his, him = P.next()
    assert ceil_div(600 - 150, 45) == 10 and ceil_div(600, 45) == 14
    its.append(mcq("%s is saving for a $600 ski trip to Whistler. %s already has $150 and saves $45 a week. How many more weeks does %s need?" % (n, cap(he), he),
                   "10 weeks", ["14 weeks", "17 weeks", "9 weeks"],
                   "Still needed: $600 − $150 = $450. $450 ÷ $45 = <b>10 weeks</b>. (14 weeks forgets the $150 already saved; "
                   "17 weeks adds the $150.)"))
    assert ceil_div(750, 45) == 17
    its.append(mq("$1500 is put in a savings account at 2% simple interest per year. What is the balance after 3 years?", D(1590),
                  [D(90), D(1530), D(10500)],
                  "Interest: I = Prt = $1500 × 0.02 × 3 = $90. Balance: $1500 + $90 = <b>$1590.00</b>. "
                  "($90.00 is only the interest; $1530.00 is after 1 year; $10" + NB + "500.00 uses 2 instead of 0.02.)"))
    n, he, his, him = P.next()
    its.append(mcq("Option A: save $25 a week. Option B: save 10% of a $280 weekly pay. Which option saves more in 12 weeks, and by how much?",
                   "Option B, by $36", ["Option A, by $36", "Option B, by $3", "Option A, by $33"],
                   "A: $25 a week. B: 10% of $280 = $28 a week, which is $3 more each week. In 12 weeks: 12 × $3 = <b>$36 more with Option B</b>. "
                   "($3 is only one week.)"))
    assert 1850 * 3 == 5550
    its.append(mq("Many people keep an emergency fund of 3 months of expenses. A family spends $1850 a month. How much should the fund be?",
                  D(5550), [D(1850), D("616.67"), D(22200)],
                  "3 × $1850 = <b>$5550.00</b>. ($616.67 divides by 3; $22" + NB + "200.00 is 12 months.)"))
    n, he, his, him = P.next()
    assert pct(1250, 20) * 6 == 1500
    its.append(mq("“Pay yourself first” means saving before spending. %s saves 20%% of %s $1250 monthly net pay. How much does %s save in 6 months?" % (n, his, he),
                  D(1500), [D(250), D(7500), D(6000)],
                  "Each month: 20% of $1250 = $250. 6 months: 6 × $250 = <b>$1500.00</b>. ($250.00 is one month; "
                  "$7500.00 is all the pay for 6 months; $6000.00 is the part not saved.)"))
    n, he, his, him = P.next()
    assert 12 * 18 / 2 == 108 and ceil_div(650, 108) == 7
    its.append(mcq("%s works 12 hours a week at $18 an hour and saves half of %s pay. How many weeks until %s has $650 for a new laptop?" % (n, his, he),
                   "7 weeks", ["6 weeks", "4 weeks", "6.02 weeks"],
                   "Pay: 12 × $18 = $216. Saved: $108 a week. $650 ÷ $108 = 6.02, and 6 weeks give only $648. Round up: <b>7 weeks</b>. "
                   "(6 weeks rounds down; 6.02 weeks does not round to whole weeks; 4 weeks uses the whole pay: $650 ÷ $216 = 3.01 → 4.)"))
    assert 28 * 24 - 600 == 72
    its.append(mq("A $600 phone can be paid for now, or with a plan of $28 a month for 24 months. How much more does the plan cost in total?",
                  D(72), [D(672), D(28), D(576)],
                  "Plan: 24 × $28 = $672. Extra: $672 − $600 = <b>$72.00</b>. ($672.00 is the plan total; $576.00 subtracts $24.)"))
    n, he, his, him = P.next()
    its.append(mq("%s saves $75 every month. How much does %s save in a year?" % (n, he), D(900), [D(3900), D(300), D(750)],
                  "12 months × $75 = <b>$900.00</b>. ($3900.00 uses 52 weeks; $300.00 is 4 months; $750.00 is 10 months.)"))
    n, he, his, him = P.next()
    t = with_tax(sale(280, 25))
    assert t == D("235.20") and 520 - t == D("284.80")
    its.append(mq("%s has saved $520. %s buys adult snowboard boots that cost $280 at 25%% off, plus 5%% GST and 7%% PST, by debit. "
                  "How much of %s savings is left?" % (n, cap(he), his), D("284.80"),
                  [D(310), D("206.40"), D("276.40")],
                  "Sale price: $280 − $70 = $210. Tax: 12% of $210 = $25.20. Total: $235.20. Left: $520.00 − $235.20 = <b>$284.80</b>. "
                  "($310.00 forgets the tax; $206.40 forgets the discount; $276.40 uses $280 × 0.87, mixing the discount and tax into one step.)"))
    assert 520 - D(280) * D("0.87") == D("276.40")
    assert 520 - with_tax(280) == D("206.40")
    assert 185 - D(2400) / 24 == 85
    its.append(mq("A class of 24 students plans a field trip to Victoria on BC Ferries. The trip costs $185 for each student. "
                  "The class raised $2400 and shares it equally. How much does each student still pay?", D(85),
                  [D(100), D(2215), D(161)],
                  "Fundraising for each student: $2400 ÷ 24 = $100. Still to pay: $185 − $100 = <b>$85.00</b>. "
                  "($100.00 is the fundraising share; $161.00 subtracts 24.)"))
    n, he, his, him = P.next()
    wk = D("18.25") * 30
    net = wk - pct(wk, 10)
    assert wk == D("547.50") and net == D("492.75") and ceil_div(3000, net) == 7 and ceil_div(3000, wk) == 6
    its.append(mcq("%s has a summer job at $18.25 an hour for 30 hours a week. About 10%% of %s pay is taken off for deductions. "
                   "%s saves all of %s net pay. How many weeks until %s has $3000?" % (n, his, cap(he), his, he),
                   "7 weeks", ["6 weeks", "6.09 weeks", "5 weeks"],
                   "Gross: $18.25 × 30 = $547.50. Net: $547.50 − $54.75 = $492.75. $3000 ÷ $492.75 = 6.09, so 6 weeks give only "
                   "$2956.50. Round up: <b>7 weeks</b>. (6 weeks rounds down or uses the gross pay; 6.09 weeks does not round to whole weeks; "
                   "5 weeks divides by the gross pay and rounds down: $3000 ÷ $547.50 = 5.48.)"))
    n, he, his, him = P.next()
    assert ceil_div(520, 240 - 60 - 95) == 7 and ceil_div(520, 240 - 60) == 3 and ceil_div(520, 240 - 95) == 4
    its.append(mcq("%s earns $240 a week. %s fixed expenses (phone and transit) are $60 a week and %s variable expenses are about $95 a week. "
                   "%s saves the rest for a $520 trip. How many weeks will it take?" % (n, cap(his), his, cap(he)),
                   "7 weeks", ["6 weeks", "3 weeks", "4 weeks"],
                   "Saved each week: $240 − $60 − $95 = $85. $520 ÷ $85 = 6.1, and 6 weeks give only $510. Round up: <b>7 weeks</b>. "
                   "(6 weeks rounds down; 3 weeks forgets the variable expenses; 4 weeks forgets the fixed expenses.)"))
    a, b = P.next(), P.next()
    assert ceil_div(1200, 35 + 25) == 20
    its.append(mcq("%s and %s save together for a $1200 family gift. %s saves $35 a week and %s saves $25 a week. How many weeks will it take?"
                   % (a[0], b[0], a[0], b[0]), "20 weeks", ["35 weeks", "48 weeks", "60 weeks"],
                   "Together they save $35 + $25 = $60 a week. $1200 ÷ $60 = <b>20 weeks</b>. (35 weeks and 48 weeks use one person’s "
                   "savings only; 60 is the dollars saved each week.)"))
    assert ceil_div(1200, 35) == 35 and ceil_div(1200, 25) == 48
    n, he, his, him = P.next()
    s1, s2 = 1200 - 450 - 380, 1200 - 450 - 300
    assert s1 == 370 and s2 == 450 and ceil_div(2000, s1) == 6 and ceil_div(2000, s2) == 5
    its.append(mcq("%s’s monthly budget: income $1200, fixed expenses $450, variable expenses $380. %s saves the rest for a $2000 goal. "
                   "If %s cuts variable expenses by $80, how many months sooner does %s reach the goal?" % (n, cap(he), he, he),
                   "1 month sooner", ["2 months sooner", "No sooner", "0.96 months sooner"],
                   "Now: saves $1200 − $450 − $380 = $370 a month. $2000 ÷ $370 = 5.4, so 6 months. After the cut: saves $450 a month. "
                   "$2000 ÷ $450 = 4.4, so 5 months. <b>1 month sooner</b>. (Months must be whole, so round up each time; "
                   "0.96 subtracts the unrounded numbers.)"))
    assert len(its) == 20
    return {"title": "Saving goals and word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert with_tax(60) == D("67.20")
    return (
        "<h2>Income: gross pay and net pay</h2>"
        "<p>For an hourly job, <b>gross pay = hourly wage × hours</b>. Your employer then takes off deductions: income tax, "
        "CPP (Canada Pension Plan) and EI (Employment Insurance). What is left is your <b>net pay</b>, the money you take home.</p>"
        "<figure class='sn-fig'>" + stub_svg([("Gross pay", "$360.00", "g"), ("Income tax", "$21.60", "d"), ("CPP", "$17.40", "d"),
                                              ("EI", "$5.87", "d"), ("Net pay", "$315.13", "t")]) +
        "<figcaption>20 hours × $18.00 = $360.00 gross. Deductions: $21.60 + $17.40 + $5.87 = $44.87. "
        "Net pay: $360.00 − $44.87 = $315.13.</figcaption></figure>"
        "<p>Change minutes to hours before you multiply: 7 hours 30 minutes is 7.5 hours, not 7.3 hours.</p>"
        "<h2>Budgets: fixed and variable expenses</h2>"
        "<p>A budget compares money in (income) with money out (expenses). A <b>fixed</b> expense is the same each month, "
        "like rent or a phone plan. A <b>variable</b> expense changes, like food, gas or fun. "
        "Income − expenses gives a <b>surplus</b> (left over) or a <b>deficit</b> (short).</p>" +
        ex("Example", "Income is $1500 a month. Fixed expenses are $900. Variable expenses are $420. How much can be saved?",
           "Expenses: $900 + $420 = $1320. Surplus: $1500 − $1320 = $180.", "$180 a month") +
        "<h2>Transactions with GST and PST</h2>"
        "<p>Most things you buy in BC have <b>5% GST</b> and <b>7% PST</b> added, 12% in total. Children’s clothing and "
        "restaurant meals have GST only. Take any discount first, then add the tax. Cash totals round to the nearest 5¢; "
        "debit and credit are exact.</p>"
        "<figure class='sn-fig'>" + receipt_svg([("Headphones", D(60))], [("GST 5%", "$3.00"), ("PST 7%", "$4.20"), ("Total", "$67.20")]) +
        "<figcaption>$60 × 1.12 = $67.20. With cash you would pay $67.20 (already a multiple of 5¢).</figcaption></figure>"
        "<h2>Bank balances and fees</h2>"
        "<p>Deposits are added. Withdrawals, purchases and fees are subtracted. Keep a running balance, one row at a time. "
        "A balance below zero is written with a minus sign, like −$25.00.</p>"
        "<figure class='sn-fig'>" + register_svg(D(200), [("Pay deposit", None, D(150), "$350.00"),
                                                         ("Debit: shoes", D("67.20"), None, "$282.80"),
                                                         ("Monthly fee", D("3.95"), None, "$278.85")]) +
        "<figcaption>Each new balance = the balance above + deposit − withdrawal.</figcaption></figure>"
        "<h2>Saving goals</h2>"
        "<p>Weeks needed = amount still needed ÷ amount saved each week. If the answer is not a whole number, "
        "<b>round up</b>, because you cannot buy the item until the full amount is saved.</p>" +
        ex("Example", "A $250 bike has 12% tax. You save $30 a week. How many weeks?",
           "Total: $250 × 1.12 = $280. $280 ÷ $30 = 9.33..., so round up.", "10 weeks") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting to add GST and PST", "Multiply the price by 1.12 (or add 5% GST only for children’s clothing and restaurant meals)"],
            ["Calling a bill “fixed” because you pay it every month", "Fixed means the amount stays the same; a bill that changes is variable"],
            ["Mixing up gross and net pay", "Net pay = gross pay − deductions"],
            ["7 h 30 min = 7.3 hours", "30 minutes = 0.5 hour, so 7.5 hours"],
            ["Forgetting bank fees in a balance", "Subtract every fee, like a withdrawal"],
            ["Rounding the number of weeks down", "Round up so the full amount is saved"],
        ])
    )


FAQ = [
    {"q": "What is the difference between fixed and variable expenses?",
     "a": "A fixed expense costs the same each month, like rent, a phone plan or a transit pass. "
          "A variable expense changes from month to month, like groceries, gas, electricity or entertainment."},
    {"q": "What is the difference between gross pay and net pay?",
     "a": "Gross pay is what you earn before deductions, such as hourly wage × hours. "
          "Net pay is what you take home after income tax, CPP and EI are taken off."},
    {"q": "How do you add GST and PST to a price in BC?",
     "a": "Most items have 5% GST and 7% PST, so multiply the price by 1.12. A $50 item costs $50 × 1.12 = $56; "
          "children’s clothing and restaurant meals have only the 5% GST."},
    {"q": "What do Grade 9 students learn about financial literacy in BC?",
     "a": "The BC Mathematics 9 curriculum includes simple budgets and transactions. Students work out pay, "
          "build budgets with fixed and variable expenses, add sales tax, track bank balances and plan saving goals."},
]


def gen():
    rnd = random.Random(59809)
    P = People(rnd)
    sets = [set_income(P), set_budget(P), set_tax(P), set_bank(P), set_goals(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [x.replace(MINUS, "-").replace(NB, "") for x in it["c"]]
            if all(re.fullmatch(r"-?\$\d+\.\d\d", x) for x in vals):
                assert len({D(x.replace("$", "")) for x in vals}) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert "HST" not in x and "13%" not in x, x
                assert not re.search(r"\d,\d\d\d", x), x
                assert not re.search(r"\d{5}", re.sub(r"<[^>]+>", "", x)), x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "budgets-and-transactions", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Budgets and Transactions: Pay, Fixed and Variable Expenses, GST and PST, Bank Fees and Saving Goals",
        "seo_title": "Grade 9 Budgets and Transactions Worksheets: Net Pay, Budgets, GST + PST and Bank Fees (Free, Answer Key, BC Curriculum)",
        "short_title": "Budgets and transactions",
        "domain": "Financial literacy",
        "standard_code": "Grade 9: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Financial literacy – simple budgets and transactions",
        "meta_desc": "Free Grade 9 math worksheets on budgets and transactions for the BC curriculum: hourly wages, gross and net pay, "
                     "fixed and variable expenses, 5% GST and 7% PST, bank balances and fees, and saving goals. "
                     "100 questions with an answer key.",
        "key_big": "Income − expenses = what you can save. Add 12% tax (5% GST + 7% PST) to most prices before you plan.",
        "key_sub": "Net pay is gross pay minus deductions. Fixed expenses stay the same each month; variable expenses change. "
                   "Subtract every fee from a bank balance, and round the weeks to a saving goal up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Account record")
    mark_large(u, "Savings goal bar")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
