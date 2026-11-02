# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Exchange Rates and Interest (Ontario Curriculum 2020, Financial Literacy F1.1, F1.3, F1.5, F1.6)
  python3 tools/gen_caon_math_g7_financial.py
Converting Canadian dollars to other currencies and back, comparing prices in two currencies, simple interest
on savings and loans (I = Prt), budgets for longer-term goals, and choosing the better account, loan or card.
Every exchange rate is a clearly stated SAMPLE rate ("Suppose US$1 = C$1.35"); no current real rate is claimed.
All arithmetic uses fractions.Fraction; answers that are not whole cents are rounded half up to the cent.
Ontario style: 4-digit numbers without a separator, 5 or more digits with a no-break space, C$ / US$ / € / ¥.
Helpers follow gen_caon_math_g6_financial.py and gen_cabc_math_g7_financial_percentages.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
LIGHT = "#d9eadf"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers and money
def fr(x):
    return x if isinstance(x, F) else F(str(x))


def rd(x, dp=2):
    """Round a Fraction half up to dp decimal places; returns a Fraction."""
    x = fr(x)
    d = (D(x.numerator) / D(x.denominator)).quantize(D(1).scaleb(-dp), rounding=ROUND_HALF_UP)
    return F(str(d))


def num(x, dp=2):
    """Exact number text with dp decimals; 5+ digit whole parts grouped with a no-break space."""
    x = fr(x)
    assert (x * 10 ** dp).denominator == 1, (x, dp)
    assert x >= 0
    d = D(x.numerator) / D(x.denominator)
    s = format(d.quantize(D(1).scaleb(-dp)), "f")
    whole, _, dec = s.partition(".")
    if len(whole) >= 5:
        g = []
        while whole:
            g.insert(0, whole[-3:])
            whole = whole[:-3]
        whole = NB.join(g)
    return whole + ("." + dec if dec else "")


def C(x):
    return "C$" + num(x)


def U(x):
    return "US$" + num(x)


def E(x):
    return "€" + num(x)


def Y(x):
    return "¥" + num(x, 0)


def PES(x):
    return num(x, 0) + " pesos"


def M(x):
    return "$" + num(x)


def nz(x, pad=True):
    """Rate text such as 1.35, 1.50, 0.75, 110 (pad=False for times like 0.5)."""
    x = fr(x)
    s = format((D(x.numerator) / D(x.denominator)).normalize(), "f")
    return s if not pad or "." not in s or len(s.split(".")[1]) != 1 else s + "0"


def cents_ok(x, dp=2):
    return (fr(x) * 10 ** dp).denominator == 1


def cap(s):
    return s[0].upper() + s[1:]


def interest(p, r, t):
    """Simple interest I = Prt, r in percent. Kept to whole cents."""
    i = fr(p) * fr(r) / 100 * fr(t)
    assert cents_ok(i), (p, r, t)
    return i


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


def cq(q, correct, wrongs, e, f=M, dp=2):
    """Number question: values are numbers, f formats them. Wrong values that are not exact are rounded first."""
    correct = fr(correct)
    assert cents_ok(correct, dp), (q, correct)
    w = []
    for x in wrongs:
        if x is None:
            continue
        x = rd(x, dp)
        if x <= 0 or x == correct:
            continue
        w.append(f(x))
    return mcq(q, f(correct), w, e)


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
    """Tag wide pictures (number lines, account cards, budgets) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    u["body_html"] = rx.sub("<svg data-pf='lg' ", u["body_html"])
    return u


# ------------------------------------------------------------ pictures
BOARD = [("US dollar", "US$1", F("1.35")), ("Euro", "€1", F("1.50")), ("Japanese yen", "¥100", F("0.90"))]


def board_svg(rows=BOARD):
    """A sample exchange-rate board: each row is 1 unit of a currency and its value in C$."""
    W, rh = 330, 34
    s = ["<rect x='2' y='2' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, 44 + rh * len(rows) + 6, PAPER, EDGE),
         "<path d='M2 40 V10 a8 8 0 0 1 8 -8 H%d a8 8 0 0 1 8 8 V40 Z' fill='%s'/>" % (W - 10, GREEN),
         txt(W // 2, 28, "Sample exchange rates", 17, bold=True, col="#ffffff")]
    y = 44
    for i, (name, unit, rate) in enumerate(rows):
        if i:
            s.append("<line x1='12' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 12, y, EDGE))
        s.append(txt(16, y + 23, name, 16, "start"))
        s.append(txt(W - 16, y + 23, "%s = %s" % (unit, C(rate)), 16, "end", bold=True))
        y += rh
    label = "Sample exchange rates: " + "; ".join("%s = %s" % (u, C(r)) for n, u, r in rows)
    return svg_wrap(W, y + 8, "".join(s), label)


def dnl_svg(rate, n, unknown_at=None, top="C$", bottom="US$"):
    """Double number line: bottom US$0..n, top C$ = rate × each. The top label at unknown_at is '?'."""
    W, L, R = 440, 50, 420
    yt, yb = 40, 92
    step = (R - L) / n
    s = [txt(20, yt + 5, top, 15, bold=True, col=GREEN), txt(20, yb + 5, bottom, 15, bold=True),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L, yt, R + 8, yt, GREEN),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L, yb, R + 8, yb, INK)]
    for k in range(n + 1):
        x = L + k * step
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, yt - 7, x, yt + 7, GREEN))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, yb - 7, x, yb + 7, INK))
        tv = "?" if k == unknown_at else ("0" if k == 0 else num(rate * k))
        s.append(txt("%.1f" % x, yt - 13, tv, 15, bold=(k == unknown_at or k == 1), col=GREEN if k == unknown_at else INK))
        s.append(txt("%.1f" % x, yb + 24, str(k), 15, bold=(k == 1)))
    label = "Double number line: %s1 = %s%s, up to %s%d" % (bottom, top, num(rate), bottom, n)
    return svg_wrap(W, yb + 32, "".join(s), label)


def cards_svg(cards):
    """Account or card offers side by side: cards = [(name, [lines])]."""
    cw, gap = 214, 12
    nl = max(len(l) for n, l in cards)
    ch = 44 + 28 * nl + 8
    s = []
    for i, (name, lines) in enumerate(cards):
        x = 2 + i * (cw + gap)
        s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, cw, ch, PAPER, EDGE))
        s.append("<path d='M%d 36 V10 a8 8 0 0 1 8 -8 H%d a8 8 0 0 1 8 8 V36 Z' fill='%s'/>" % (x, x + cw - 8, GREEN))
        s.append(txt(x + cw // 2, 26, name, 17, bold=True, col="#ffffff"))
        for j, ln in enumerate(lines):
            s.append(txt(x + 12, 64 + 28 * j, ln, 16, "start"))
    W = 4 + len(cards) * cw + (len(cards) - 1) * gap
    label = "Offers: " + "; ".join("%s, %s" % (n, ", ".join(l)) for n, l in cards)
    return svg_wrap(W, ch + 4, "".join(s), label)


def budget_svg(title, money_in, money_out):
    """A monthly budget table: rows of (label, amount) under Money in and Money out. None prints '?'."""
    W, rh, fs = 300, 25, 16
    s = []
    y = 26
    s.append(txt(W // 2, y - 6, title, 17, bold=True))
    rows = [("Money in", None, "h")] + [(a, b, "r") for a, b in money_in] + [("Money out", None, "h")] + [(a, b, "r") for a, b in money_out]
    top = y
    for label, amt, kind in rows:
        if kind == "h":
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
            s.append(txt(12, y + 18, label, fs, "start", bold=True, col="#ffffff"))
        else:
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
            s.append(txt(12, y + 18, label, fs, "start"))
            s.append(txt(W - 12, y + 18, "?" if amt is None else M(amt), fs, "end", bold=amt is None, col=GREEN if amt is None else INK))
        y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    fmt = lambda b: "?" if b is None else M(b)
    label = "Budget %s. Money in: %s. Money out: %s" % (
        title, ", ".join("%s %s" % (a, fmt(b)) for a, b in money_in), ", ".join("%s %s" % (a, fmt(b)) for a, b in money_out))
    return svg_wrap(W, y + 4, "".join(s), label)


# ============================================================ set 1: C$ to another currency
def to_foreign_div(q, cad, rate, f, name, extra_e="", rounded=False):
    """Rate given as 1 foreign = C$rate: divide. Mistakes: multiply, take off the extra percent, add the rate."""
    cad, rate = fr(cad), fr(rate)
    exact = cad / rate
    ans = rd(exact) if rounded else exact
    e = ("Each %s costs C$%s, so divide: %s ÷ %s = " % (name, nz(rate), C(cad), nz(rate)))
    if rounded and ans != exact:
        e += "%s… ≈ <b>%s</b>." % (num(rd(exact, 3), 3), f(ans))
    else:
        e += "<b>%s</b>. Check: %s × %s = %s." % (f(ans), f(ans), nz(rate), C(ans * rate))
    if extra_e:
        e += " " + extra_e
    return cq(q, ans, [cad * rate, cad * (2 - rate), cad, cad + rate, cad / (rate * 10)], e, f)


def to_foreign_mul(q, cad, rate, f, name, dp=2, extra_e=""):
    """Rate given as C$1 = rate foreign: multiply. Mistakes: divide, add, place value."""
    cad, rate = fr(cad), fr(rate)
    ans = cad * rate
    e = "Each Canadian dollar is worth %s %s, so multiply: %s × %s = <b>%s</b>." % (nz(rate), name, C(cad), nz(rate), f(ans))
    if extra_e:
        e += " " + extra_e
    w = [cad / rate if cad / rate >= 10 else None, cad + rate, ans / 10, ans * 10 if ans * 10 < 10 ** 6 else None, cad * (1 - rate) if rate < 1 else None]
    return cq(q, ans, w, e, f, dp)


def set_cad_to_foreign(P):
    its = []
    its.append(mcq("Suppose 1 US dollar is worth 1.35 Canadian dollars (US$1 = C$1.35). Which is worth more?",
                   "1 US dollar", ["1 Canadian dollar", "They are worth the same", "You cannot tell"],
                   "You need C$1.35 to buy one US dollar, so <b>1 US dollar</b> is worth more than 1 Canadian dollar. "
                   "An exchange rate tells you how much of one currency equals one unit of another."))
    its.append(mcq("Suppose US$1 = C$1.35. To change Canadian dollars into US dollars, what should you do?",
                   "Divide by 1.35", ["Multiply by 1.35", "Subtract 1.35", "Subtract 35%"],
                   "Each US dollar costs C$1.35, so count how many groups of 1.35 fit into your Canadian dollars: "
                   "<b>divide by 1.35</b>. You get fewer US dollars than Canadian dollars."))
    its.append(to_foreign_div("Suppose US$1 = C$1.25. How many US dollars do you get for C$100?", 100, "1.25", U, "US dollar",
                              "(US$125.00 multiplies instead of dividing.)"))
    its.append(to_foreign_div("Suppose €1 = C$1.50. How many euros do you get for C$300?", 300, "1.50", E, "euro",
                              "(€450.00 multiplies instead of dividing.)"))
    its.append(to_foreign_div("Suppose US$1 = C$1.40. How many US dollars do you get for C$70?", 70, "1.40", U, "US dollar"))
    its.append(to_foreign_mul("Suppose C$1 = ¥110 (Japanese yen). How many yen do you get for C$50?", 50, 110, Y, "yen", 0,
                              "(¥160 adds instead of multiplying.)"))
    its.append(to_foreign_mul("Suppose C$1 = 13 Mexican pesos. How many pesos do you get for C$40?", 40, 13, PES, "pesos", 0))
    its.append(to_foreign_div("Suppose US$1 = C$1.35. How many US dollars do you get for C$270?", 270, "1.35", U, "US dollar",
                              "(US$175.50 takes 35% off, but dividing by 1.35 is not the same as subtracting 35%.)"))
    its.append(to_foreign_div("Suppose €1 = C$1.50. How many euros do you get for C$450?", 450, "1.50", E, "euro"))
    its.append(to_foreign_mul("Suppose C$1 = US$0.75. How many US dollars do you get for C$80?", 80, "0.75", U, "US dollars",
                              extra_e="This time the rate tells you what one Canadian dollar is worth, so you multiply. "
                                      "(US$106.67 divides instead.)"))
    its.append(to_foreign_mul("Suppose C$1 = €0.68. How many euros do you get for C$250?", 250, "0.68", E, "euros"))
    its.append(to_foreign_mul("Suppose C$1 = ¥110. How many yen do you get for C$125?", 125, 110, Y, "yen", 0))
    assert 340 / F("1.36") == 250
    its.append(to_foreign_div("Suppose US$1 = C$1.36. How many US dollars do you get for C$340?", 340, "1.36", U, "US dollar"))
    its.append(mcq("Suppose US$1 = C$1.38. About how many US dollars do you get for C$700?",
                   "About US$500", ["About US$1000", "About US$700", "About US$300"],
                   "Round the rate: 1.38 ≈ 1.4. C$700 ÷ 1.4 = US$500, so <b>about US$500</b>. "
                   "(About US$1000 multiplies by 1.4. You always get fewer US dollars than Canadian dollars at this rate.)"))
    its.append(to_foreign_div("Suppose US$1 = C$1.35. How many US dollars do you get for C$100? Round to the nearest cent.",
                              100, "1.35", U, "US dollar", "(US$65.00 takes off 35% instead of dividing.)", rounded=True))
    its.append(to_foreign_div("Suppose €1 = C$1.48. How many euros do you get for C$200? Round to the nearest cent.",
                              200, "1.48", E, "euro", rounded=True))
    its.append(mcq("Suppose US$1 = C$1.25. What is C$1 worth in US dollars?", U(F("0.80")),
                   [U(F("1.25")), U(F("0.75")), U(F("0.25"))],
                   "Divide: C$1 ÷ 1.25 = <b>US$0.80</b>. Check: US$0.80 × 1.25 = C$1.00. "
                   "(US$0.75 just takes 25¢ off; that is not the same as dividing by 1.25.)"))
    b = fig(board_svg())
    assert F(600) / F("1.50") == 400
    its.append(cq(b + "Use the sample exchange rates. How many euros do you get for C$600?", 400,
                  [900, 600 * F("1.35") ** -1, 600 - F("1.50")],
                  "The board shows €1 = C$1.50. C$600 ÷ 1.50 = <b>€400.00</b>. Check: 400 × C$1.50 = C$600. "
                  "(€900.00 multiplies; €444.44 uses the US dollar rate.)", E))
    assert F(90) / F("0.90") * 100 == 10000
    its.append(cq(b + "Use the sample exchange rates. How many yen do you get for C$90?", 10000,
                  [100, F(81), 1000],
                  "The board shows ¥100 = C$0.90. C$90 ÷ 0.90 = 100 groups of ¥100, and 100 × ¥100 = <b>¥10" + NB + "000</b>. "
                  "(¥100 forgets that each group is ¥100, not ¥1.)", Y, 0))
    n, he, his, him = P.next()
    assert (500 - 5) / F("1.25") == 396
    its.append(cq("Suppose US$1 = C$1.25. %s changes C$500 into US dollars for a trip to New York. The bank first takes a C$5 fee "
                  "from the C$500. How many US dollars does %s get?" % (n, he), 396,
                  [400, 395, F(495) * F("1.25")],
                  "After the fee: C$500 − C$5 = C$495. Convert: C$495 ÷ 1.25 = <b>US$396.00</b>. "
                  "(US$400.00 forgets the fee; US$395.00 takes the fee off in US dollars after converting.)", U))
    assert len(its) == 20
    return {"title": "Canadian dollars to other currencies", "items": its}


# ============================================================ set 2: another currency to C$
def to_cad_mul(q, amt, rate, f, name, extra_e="", rounded=False, figure=None):
    """Rate given as 1 foreign = C$rate: multiply. Mistakes: divide, add the rate, only the extra part."""
    amt, rate = fr(amt), fr(rate)
    exact = amt * rate
    ans = rd(exact) if rounded else exact
    if rounded and ans != exact:
        e = "Each %s is worth C$%s, so multiply: %s × %s = %s ≈ <b>%s</b>." % (name, nz(rate), f(amt), nz(rate), num(exact, 4), C(ans))
    else:
        e = "Each %s is worth C$%s, so multiply: %s × %s = <b>%s</b>." % (name, nz(rate), f(amt), nz(rate), C(ans))
    if extra_e:
        e += " " + extra_e
    if figure:
        q = fig(figure) + q
    return cq(q, ans, [amt / rate, amt + rate, amt * (rate - 1), exact / 10, amt], e, C)


def to_cad_div(q, amt, rate, f, name, dp_in=2, extra_e=""):
    """Rate given as C$1 = rate foreign: divide."""
    amt, rate = fr(amt), fr(rate)
    ans = amt / rate
    e = "C$1 buys %s %s, so divide: %s ÷ %s = <b>%s</b>. Check: %s × %s = %s." % (
        nz(rate), name, f(amt), nz(rate), C(ans), num(ans), nz(rate), f(ans * rate))
    if extra_e:
        e += " " + extra_e
    return cq(q, ans, [amt * rate if amt * rate < 10 ** 6 else None, amt / (rate * 10), amt / (rate / 10), amt - rate], e, C)


def set_foreign_to_cad(P):
    its = []
    its.append(to_cad_mul("The double number line shows US$1 = C$1.35. What is US$4 in Canadian dollars?", 4, "1.35", U, "US dollar",
                          figure=dnl_svg(F("1.35"), 4, unknown_at=4)))
    its.append(mcq("Suppose €1 = C$1.50. To change euros into Canadian dollars, what should you do?",
                   "Multiply by 1.50", ["Divide by 1.50", "Add 1.50", "Subtract 50%"],
                   "Each euro is worth C$1.50, so 2 euros are worth 2 × C$1.50. <b>Multiply by 1.50</b>. "
                   "You get more Canadian dollars than euros."))
    its.append(to_cad_mul("Suppose US$1 = C$1.35. What is US$10 in Canadian dollars?", 10, "1.35", U, "US dollar",
                          "(C$7.41 divides instead of multiplying.)"))
    its.append(to_cad_mul("Suppose €1 = C$1.50. What is €40 in Canadian dollars?", 40, "1.50", E, "euro"))
    its.append(to_cad_mul("Suppose US$1 = C$1.30. What is US$25 in Canadian dollars?", 25, "1.30", U, "US dollar"))
    its.append(to_cad_mul("Suppose US$1 = C$1.35. What is US$200 in Canadian dollars?", 200, "1.35", U, "US dollar",
                          "(C$70.00 is only the extra 35¢ on each dollar.)"))
    its.append(to_cad_mul("Suppose €1 = C$1.45. What is €80 in Canadian dollars?", 80, "1.45", E, "euro"))
    its.append(to_cad_div("Suppose C$1 = ¥110. What is ¥5500 in Canadian dollars?", 5500, 110, Y, "yen",
                          extra_e="(Multiplying would give a huge number of dollars, which cannot be right.)"))
    its.append(to_cad_div("Suppose C$1 = 13 Mexican pesos. What is 780 pesos in Canadian dollars?", 780, 13, PES, "pesos"))
    its.append(to_cad_div("Suppose C$1 = US$0.75. What is US$45 in Canadian dollars?", 45, "0.75", U, "US dollars",
                          extra_e="(C$33.75 multiplies, but the rate tells you what C$1 is worth, so divide.)"))
    its.append(to_cad_mul("Suppose US$1 = C$1.40. A pair of jeans costs US$35.50. What is that in Canadian dollars?", "35.50", "1.40", U, "US dollar"))
    b = board_svg()
    its.append(to_cad_mul("Use the sample exchange rates. A hotel room in Paris costs €120 a night. What is that in Canadian dollars?",
                          120, "1.50", E, "euro", figure=b))
    assert F(5000) / 100 * F("0.90") == 45
    its.append(cq(fig(b) + "Use the sample exchange rates. A train ticket in Japan costs ¥5000. What is that in Canadian dollars?", 45,
                  [4500, F("0.45"), F(5000) / F("0.90") / 100],
                  "The board shows ¥100 = C$0.90. ¥5000 is 50 groups of ¥100. 50 × C$0.90 = <b>C$45.00</b>. "
                  "(C$4500.00 multiplies 5000 × 0.90 and forgets that the rate is for ¥100.)", C))
    its.append(to_cad_mul("Suppose US$1 = C$1.37. A T-shirt costs US$19.99. What is that in Canadian dollars? Round to the nearest cent.",
                          "19.99", "1.37", U, "US dollar", "(C$14.59 divides instead of multiplying.)", rounded=True))
    its.append(to_cad_mul("Suppose €1 = C$1.48. What is €250 in Canadian dollars?", 250, "1.48", E, "euro"))
    its.append(mcq("Suppose US$1 = C$1.38. About how much is US$49.95 in Canadian dollars?",
                   "About C$70", ["About C$35", "About C$50", "About C$100"],
                   "Round: US$49.95 ≈ US$50 and 1.38 ≈ 1.4. 50 × 1.4 = 70, so <b>about C$70</b>. "
                   "(About C$35 divides; about C$50 forgets to convert.)"))
    n, he, his, him = P.next()
    its.append(mcq("Suppose US$1 = C$1.35. %s says US$80 is about C$59. Is %s right?" % (n, he),
                   "No, it is about C$108", ["Yes, C$59 is about right", "No, it is about C$81", "No, it is about C$135"],
                   "US dollars are worth more than Canadian dollars at this rate, so the C$ amount must be <b>more</b> than 80. "
                   "80 × 1.35 = 108, so <b>US$80 is about C$108</b>. %s divided instead of multiplying." % n))
    assert F(405) / 300 == F("1.35")
    its.append(mcq("A bank sells US$300 for C$405. What exchange rate did it use?",
                   "US$1 = C$1.35", ["US$1 = C$0.74", "US$1 = C$105", "US$1 = C$1.05"],
                   "Find the cost of US$1: C$405 ÷ 300 = 1.35, so <b>US$1 = C$1.35</b>. "
                   "(0.74 divides the other way; 105 is C$405 − 300.)"))
    n, he, his, him = P.next()
    assert (15 + 25) * F("1.50") == 60
    its.append(cq("Suppose €1 = C$1.50. On a trip to Paris, %s buys a souvenir for €15 and a T-shirt for €25. "
                  "What is the total in Canadian dollars?" % n, 60, [F(40) / F("1.50"), 40, F("41.50")],
                  "Total in euros: €15 + €25 = €40. Convert: 40 × 1.50 = <b>C$60.00</b>. "
                  "(C$26.67 divides; C$40.00 forgets to convert.)", C))
    n, he, his, him = P.next()
    assert 100 * F("1.30") == 130
    its.append(cq("A bank sells US dollars at US$1 = C$1.35 and buys them back at US$1 = C$1.30. After a trip, %s sells US$100 back "
                  "to the bank. How many Canadian dollars does %s get?" % (n, he), 130, [135, F(100) / F("1.30"), F("101.30")],
                  "When you sell US dollars back, the bank uses its <b>buying</b> rate: 100 × 1.30 = <b>C$130.00</b>. "
                  "(C$135.00 uses the selling rate. The difference between the two rates is how the bank earns money.)", C))
    assert len(its) == 20
    return {"title": "Other currencies to Canadian dollars", "items": its}


# ============================================================ set 3: comparing prices
def compare_item(q, cad_price, other_price, rate, fo, place, item, extra_e="", rate_txt=None, cad_other=None, home="Canada"):
    """Same item in Canada (C$) and elsewhere. rate = C$ per 1 unit of the other currency (yen: per ¥1)."""
    cad_price, other_price, rate = fr(cad_price), fr(other_price), fr(rate)
    oc = other_price * rate if cad_other is None else fr(cad_other)
    assert cents_ok(oc)
    diff = abs(oc - cad_price)
    conv = rate_txt or ("%s × %s = %s" % (fo(other_price), nz(rate), C(oc)))
    e = "Convert to the same currency: %s. Compare with %s. " % (conv, C(cad_price))
    if diff == 0:
        ans = "They cost the same"
        e += "<b>They cost the same.</b>"
    elif oc < cad_price:
        ans = "%s, by %s" % (place, C(diff))
        e += "<b>%s is cheaper, by %s − %s = %s</b>." % (place, C(cad_price), C(oc), C(diff))
    else:
        ans = "%s, by %s" % (home, C(diff))
        e += "<b>%s is cheaper" % home + ", by %s − %s = %s</b>." % (C(oc), C(cad_price), C(diff))
    if extra_e:
        e += " " + extra_e
    raw = abs(other_price - cad_price)
    wr = []
    if diff:
        wrong_place = place if ans.startswith(home) else home
        wr.append("%s, by %s" % (wrong_place, C(raw)) if raw else "%s, by %s" % (wrong_place, C(diff)))
        wr.append("%s, by %s" % (wrong_place, C(diff)))
        wr.append("They cost the same")
        wr.append("%s, by %s" % (ans.split(",")[0], C(raw)) if raw and raw != diff else None)
    else:
        wr += ["%s, by %s" % (home, C(raw)), "%s, by %s" % (place, C(raw)), "%s, by %s" % (place, C(cad_price * F(1, 10)))]
    return mcq(q, ans, wr, e)


def set_compare(P):
    its = []
    its.append(compare_item("Suppose US$1 = C$1.35. A book costs US$20 in the US and C$25 in Canada. Where is it cheaper, and by how much?",
                            25, 20, "1.35", U, "The US", "book",
                            "(Comparing 20 with 25 directly mixes two currencies.)"))
    its.append(compare_item("Suppose US$1 = C$1.35. A hoodie costs US$40 in the US and C$56 in Canada. Where is it cheaper, and by how much?",
                            56, 40, "1.35", U, "The US", "hoodie"))
    its.append(compare_item("Suppose €1 = C$1.50. Sneakers cost €80 in Paris and C$115 in Toronto. Where are they cheaper, and by how much?",
                            115, 80, "1.50", E, "Paris", "sneakers", home="Toronto"))
    its.append(compare_item("Suppose US$1 = C$1.25. A video game costs US$60 in the US and C$75 in Canada. Where is it cheaper, and by how much?",
                            75, 60, "1.25", U, "The US", "game", "Different numbers can still be the same price in different currencies."))
    its.append(compare_item("Suppose C$1 = ¥110. Headphones cost ¥8800 in Tokyo and C$85 in Vancouver. Where are they cheaper, and by how much?",
                            85, 8800, F(1, 110), Y, "Tokyo", "headphones",
                            "(Here you divide, because the rate tells you what C$1 buys.)", home="Vancouver",
                            rate_txt="¥8800 ÷ 110 = C$80.00"))
    its.append(compare_item("Suppose US$1 = C$1.40. A bottle of maple syrup costs US$15 in a US store and C$20 in Canada. "
                            "Where is it cheaper, and by how much?", 20, 15, "1.40", U, "The US", "syrup"))
    its.append(compare_item("Suppose US$1 = C$1.35. A pair of earbuds costs US$24 online in the US and C$32.40 in Canada. "
                            "Where are they cheaper, and by how much?", "32.40", 24, "1.35", U, "The US", "earbuds"))
    its.append(compare_item("Suppose US$1 = C$1.35. A 1 kg bag of coffee costs US$12 in the US and C$17 in Canada. "
                            "Where is it cheaper, and by how much?", 17, 12, "1.35", U, "The US", "coffee"))
    assert 115 * F("1.35") == F("155.25") and 95 * F("1.50") == F("142.50")
    its.append(mcq(fig(board_svg()) + "Use the sample exchange rates. The same jacket costs C$150 in Canada, US$115 in the US and €95 in France. "
                   "Where is it cheapest?", "€95 in France", ["C$150 in Canada", "US$115 in the US", "They cost the same"],
                   "Convert both to C$: US$115 × 1.35 = C$155.25; €95 × 1.50 = C$142.50. "
                   "<b>€95 in France</b> is the cheapest. (The smallest number is not always the lowest price.)"))
    its.append(mcq("Which sample exchange rate gives you the most US dollars for C$100?",
                   "US$1 = C$1.32", ["US$1 = C$1.35", "US$1 = C$1.38", "US$1 = C$1.40"],
                   "You divide by the rate, so the <b>smallest</b> rate gives the most US dollars. C$100 ÷ 1.32 ≈ US$75.76, "
                   "but C$100 ÷ 1.40 ≈ US$71.43. <b>US$1 = C$1.32</b> is best."))
    assert 50 * F("1.25") == F("62.50") and 50 * F("1.40") == 70
    its.append(mcq("The sample exchange rate changes from US$1 = C$1.25 to US$1 = C$1.40. "
                   "What happens to the cost of a US$50 hotel night in Canadian dollars?",
                   "It rises from C$62.50 to C$70", ["It falls from C$70 to C$62.50", "It stays at C$50", "It rises by C$0.15"],
                   "Before: 50 × 1.25 = C$62.50. After: 50 × 1.40 = C$70.00. Each US dollar now costs more, so "
                   "<b>the room costs more in Canadian dollars</b>. (C$0.15 is the change for just US$1.)"))
    n, he, his, him = P.next()
    assert 200 * F("1.40") == 280 and 200 * F("1.50") == 300
    its.append(cq("%s’s family needs €200 for a trip. Suppose €1 = C$1.40 in May and €1 = C$1.50 in June. "
                  "How much more does the €200 cost in June than in May?" % n, 20, [F("0.10"), 280, 300],
                  "May: 200 × 1.40 = C$280. June: 200 × 1.50 = C$300. Difference: C$300 − C$280 = <b>C$20.00</b>. "
                  "(C$0.10 is the change in the rate for only €1.)", C))
    its.append(compare_item("Suppose €1 = C$1.45. A soccer jersey costs €70 in Spain and C$100 in Canada. Where is it cheaper, and by how much?",
                            100, 70, "1.45", E, "Spain", "jersey"))
    its.append(compare_item("Suppose US$1 = C$1.30. A laptop costs US$800 in the US and C$1000 in Canada. Where is it cheaper, and by how much?",
                            1000, 800, "1.30", U, "The US", "laptop"))
    n, he, his, him = P.next()
    assert (30 + 10) * F("1.35") == 54
    its.append(mcq("Suppose US$1 = C$1.35. A US website sells a game for US$30 plus US$10 shipping. A Canadian store sells it for C$50. "
                   "Which is cheaper, and by how much?",
                   "Canada, by C$4.00", ["The US, by C$9.50", "The US, by C$10.00", "Canada, by C$10.00"],
                   "US total: US$30 + US$10 = US$40. 40 × 1.35 = C$54. <b>Canada is cheaper, by C$54 − C$50 = C$4.00</b>. "
                   "(The US, by C$9.50 forgets the shipping: 30 × 1.35 = C$40.50.)"))
    assert 10 * F("1.50") == 15 and 11 * F("1.35") == F("14.85")
    its.append(mcq("Suppose €1 = C$1.50 and US$1 = C$1.35. Which is worth more: €10 or US$11?",
                   "€10, by C$0.15", ["US$11, by C$0.15", "US$11, by C$1.00", "They are worth the same"],
                   "Change both to C$: €10 × 1.50 = C$15.00; US$11 × 1.35 = C$14.85. <b>€10 is worth C$0.15 more</b>. "
                   "(US$11 looks bigger only because 11 &gt; 10.)"))
    its.append(compare_item("Suppose C$1 = ¥110. A bowl of ramen costs ¥1100 in Tokyo and C$14 in Vancouver. Where is it cheaper, and by how much?",
                            14, 1100, F(1, 110), Y, "Tokyo", "ramen", home="Vancouver", rate_txt="¥1100 ÷ 110 = C$10.00"))
    n, he, his, him = P.next()
    assert 90 * F("1.35") + 15 == F("136.50")
    its.append(mcq("Suppose US$1 = C$1.35. %s finds skates for US$90 on a US website, plus C$15 shipping to Canada. "
                   "A store in Winnipeg sells them for C$135. Which is cheaper, and by how much?" % n,
                   "Winnipeg, by C$1.50", ["The website, by C$13.50", "The website, by C$45.00", "They cost the same"],
                   "Website: 90 × 1.35 = C$121.50, plus C$15 = C$136.50. <b>Winnipeg is cheaper, by C$1.50</b>. "
                   "(The website, by C$13.50 forgets the shipping.)"))
    assert 400 * F("1.25") == 500 and F(600 - 500, 500) == F(1, 5)
    its.append(mcq("Suppose US$1 = C$1.25. A bike costs US$400 in the US and C$600 in Canada. "
                   "The Canadian price is what percent more than the US price?",
                   "20%", ["50%", "25%", "17%"],
                   "US price in C$: 400 × 1.25 = C$500. Difference: C$600 − C$500 = C$100. 100 ÷ 500 = 0.2 = <b>20%</b>. "
                   "(50% compares 600 with 400 without converting; 17% divides by 600 instead of the US price.)"))
    its.append(mcq("Why can you not compare US$20 and C$25 just by looking at the numbers?",
                   "The units are worth different amounts", ["Prices in the US include tax", "US dollars have no cents",
                                                             "Bigger numbers always cost more"],
                   "A US dollar and a Canadian dollar are <b>worth different amounts</b>, like comparing metres and centimetres. "
                   "Convert both prices into the same currency first."))
    assert len(its) == 20
    return {"title": "Comparing prices in two currencies", "items": its}


# ============================================================ set 4: simple interest
def si_item(q, p, r, t, balance=False, extra_e="", w_first=()):
    """Simple interest (or the balance) on p at r% for t years. Mistake list: rate as a whole number, 1 year only, etc."""
    p, r, t = fr(p), fr(r), fr(t)
    i = interest(p, r, t)
    rd_txt = nz(r / 100)
    tt = nz(t, False)
    e = "I = Prt = %s × %s × %s = %s." % (M(p), rd_txt, tt, M(i))
    if balance:
        ans = p + i
        e = e[:-1] + ". Total: %s + %s = <b>%s</b>." % (M(p), M(i), M(ans))
        w = [i, p + p * r * t, p + interest(p, r, 1) if t != 1 else None, p + i * 10, p + i / 10]
    else:
        ans = i
        e = e.replace(M(i) + ".", "<b>" + M(i) + "</b>.")
        w = [p * r * t, interest(p, r, 1) if t != 1 else None, p + i, i * 10, i / 10]
    if extra_e:
        e += " " + extra_e
    return cq(q, ans, list(w_first) + w, e, M)


def set_interest(P):
    its = []
    its.append(mcq("What is interest?", "Money paid for using someone else’s money",
                   ["A fee for opening a bank account", "The tax added to a price", "The money you start with"],
                   "When you save, the bank uses your money and <b>pays you interest</b>. When you borrow, "
                   "<b>you pay interest</b> for using the lender’s money."))
    its.append(mcq("In the simple interest formula I = Prt, what does r stand for?", "The yearly interest rate, as a decimal",
                   ["The time in years", "The money at the start", "The total at the end"],
                   "I is the interest, P is the principal (the money at the start), <b>r is the yearly rate written as a decimal</b> "
                   "(3% = 0.03), and t is the time in years."))
    its.append(mcq("To use a 3% interest rate in I = Prt, what number do you use for r?", "0.03", ["3", "0.3", "0.003"],
                   "Percent means out of 100: 3% = 3 ÷ 100 = <b>0.03</b>. Using 3 would make the interest 100 times too big."))
    its.append(si_item("What is the simple interest on $500 at 2% per year for 1 year?", 500, 2, 1,
                       extra_e="($1000.00 uses 2 instead of 0.02.)"))
    its.append(si_item("What is the simple interest on $800 at 3% per year for 2 years?", 800, 3, 2,
                       extra_e="($24.00 is only 1 year.)"))
    n, he, his, him = P.next()
    its.append(si_item("%s saves $1200 in an account that pays 2.5%% simple interest per year. How much is in the account after 1 year?" % n,
                       1200, "2.5", 1, balance=True, extra_e="($30.00 is only the interest. 2.5% = 0.025, not 0.25.)"))
    n, he, his, him = P.next()
    its.append(si_item("%s borrows $600 at 8%% simple interest per year. How much must %s pay back after 1 year?" % (n, he),
                       600, 8, 1, balance=True, extra_e="When you borrow, you pay back the loan plus the interest."))
    its.append(si_item("What is the simple interest on a $1500 loan at 6% per year for 2 years?", 1500, 6, 2))
    its.append(si_item("What is the simple interest on $2000 at 4% per year for 6 months?", 2000, 4, F(1, 2),
                       extra_e="6 months is half a year, so t = 0.5. ($480.00 uses t = 6; $80.00 is a full year.)", w_first=[480]))
    assert interest(400, 3, 1) == 12
    its.append(mcq("$400 earns $12 of simple interest in 1 year. What is the yearly interest rate?", "3%", ["12%", "33%", "0.03%"],
                   "r = I ÷ (P × t) = 12 ÷ 400 = 0.03 = <b>3%</b>. (12% uses the dollars as the percent; 33% divides 400 by 12.)"))
    assert interest(900, 2, 3) == 54
    its.append(mcq("$900 earns 2% simple interest per year. How many years will it take to earn $54 of interest?", "3 years",
                   ["27 years", "18 years", "6 years"],
                   "Interest each year: $900 × 0.02 = $18. $54 ÷ $18 = <b>3 years</b>. "
                   "(27 divides $54 by 2; 18 is the interest for one year, not the time.)"))
    assert interest(1000, 2, 3) == 60 and interest(1500, 1, 3) == 45
    its.append(mcq("Which earns more simple interest in 3 years: $1000 at 2% per year, or $1500 at 1% per year?",
                   "$1000 at 2%, by $15", ["$1500 at 1%, by $15", "$1500 at 1%, by $500", "They earn the same"],
                   "$1000 × 0.02 × 3 = $60. $1500 × 0.01 × 3 = $45. <b>$1000 at 2% earns $15 more</b>. "
                   "A higher rate can beat a bigger principal."))
    assert interest(500, 3, 2) == interest(500, 2, 3) == 30
    its.append(mcq("$500 is saved for a few years. Which earns more simple interest: 3% for 2 years, or 2% for 3 years?",
                   "They earn the same", ["3% for 2 years", "2% for 3 years", "You cannot tell"],
                   "3% for 2 years: $500 × 0.03 × 2 = $30. 2% for 3 years: $500 × 0.02 × 3 = $30. <b>They earn the same</b>, "
                   "because 0.03 × 2 = 0.02 × 3."))
    its.append(mcq("How does a higher interest rate affect savers and borrowers?",
                   "Savings grow faster; loans cost more", ["Savings grow slower; loans cost less", "Both pay less",
                                                            "It does not change anything"],
                   "A higher rate means more interest. For a saver, the bank pays more, so <b>savings grow faster</b>. "
                   "For a borrower, <b>a loan costs more</b> to pay back."))
    its.append(mcq("A bank pays 2% interest on savings and charges 7% interest on loans. Why are the rates different?",
                   "The bank earns money from the gap", ["Savings are riskier than loans", "Savers pay the bank to save",
                                                         "Loans are always paid back early"],
                   "The bank lends out money that people save. It pays savers 2% and charges borrowers 7%, so "
                   "<b>it earns money from the difference</b>."))
    n, he, his, him = P.next()
    i = interest(500, F("19.99"), 1)
    assert i == F("99.95")
    its.append(cq("%s’s credit card charges 19.99%% interest per year. %s leaves a $500 balance unpaid for 1 year. "
                  "Using simple interest, how much interest is that?" % (n, cap(he)), i, [500 * F("19.99"), 500 + i, F("10.00")],
                  "19.99% = 0.1999. I = $500 × 0.1999 × 1 = <b>$99.95</b>, almost $100. "
                  "(Real cards add interest even faster, so paying the full bill on time is the best plan.)", M))
    its.append(si_item("A family borrows $3000 at 5% simple interest per year for 4 years. How much do they pay back in total?",
                       3000, 5, 4, balance=True))
    n, he, his, him = P.next()
    tot = 1200 + interest(1200, 5, 1)
    assert tot == 1260 and tot / 12 == 105
    its.append(cq("%s borrows $1200 for a laptop at 5%% simple interest for 1 year. %s pays it back in 12 equal monthly payments. "
                  "How much is each payment?" % (n, cap(he)), 105, [100, 5, F(1260)],
                  "Interest: $1200 × 0.05 × 1 = $60. Total: $1200 + $60 = $1260. Each month: $1260 ÷ 12 = <b>$105.00</b>. "
                  "($100.00 forgets the interest.)", M))
    assert interest(700, 3, 1) == 21 and interest(700, 3, 4) == 84
    its.append(cq("$700 at 3% simple interest earns $21 each year. How much interest does it earn in 4 years?", 84,
                  [784, 25, F("5.25")],
                  "Simple interest is the same every year. 4 × $21 = <b>$84.00</b>. "
                  "($784.00 is the balance, not the interest; $25.00 adds 4 instead of multiplying.)", M))
    assert interest(1500, 4, 1) == 60
    its.append(cq("How much must you save at 4% simple interest per year to earn $60 in 1 year?", 1500,
                  [240, 15, 150],
                  "I = Prt, so $60 = P × 0.04 × 1. P = $60 ÷ 0.04 = <b>$1500.00</b>. Check: $1500 × 0.04 = $60. "
                  "($240.00 multiplies by 4; $15.00 divides by 4 instead of 0.04.)", M))
    assert len(its) == 20
    return {"title": "Simple interest on savings and loans", "items": its}


# ============================================================ set 5: budgets, goals and choosing
def months(n):
    return "%d month%s" % (n, "" if n == 1 else "s")


def ceil(x):
    x = fr(x)
    return -(-x.numerator // x.denominator)


def set_words(P):
    its = []
    its.append(mcq("Which is a long-term financial goal for a Grade 7 student?",
                   "Saving for college or university", ["Buying lunch tomorrow", "A movie this weekend", "A snack after school"],
                   "A long-term goal takes many months or years of saving. <b>Saving for college or university</b> is long-term; "
                   "the others are short-term spending."))
    n, he, his, him = P.next()
    assert F(1200 - 300, 10) == 90
    its.append(cq("%s wants C$1200 for a school trip in 10 months. %s already has C$300 saved. How much must %s save each month?"
                  % (n, cap(he), he), 90, [120, 150, 900],
                  "Still needed: C$1200 − C$300 = C$900. Each month: C$900 ÷ 10 = <b>C$90.00</b>. "
                  "(C$120.00 forgets the C$300 already saved.)", C))
    n, he, his, him = P.next()
    bi = [("Part-time job", F(240)), ("Allowance", F(80))]
    bo = [("Phone plan", F(45)), ("Transit pass", F(60)), ("Fun", F(55)), ("Savings", None)]
    sv = sum(b for a, b in bi) - sum(b for a, b in bo if b is not None)
    assert sv == 160
    budget = fig(budget_svg("%s’s monthly budget" % n, bi, bo))
    its.append(cq(budget + "%s’s budget is balanced. How much does %s save each month?" % (n, he), sv, [320, 80, 215],
                  "Money in: $240 + $80 = $320. Spending: $45 + $60 + $55 = $160. Savings: $320 − $160 = <b>$160.00</b>. "
                  "($320.00 is all the money in; $80.00 forgets the allowance.)", M))
    assert F(960) / 160 == 6
    its.append(mcq(budget + "%s wants a $960 bike. Using this budget, how many months will it take to save for it?" % n,
                   months(6), [months(3), months(12), months(4)],
                   "%s saves $320 − $160 = $160 each month. $960 ÷ $160 = <b>6 months</b>. "
                   "(3 months divides by all the money in, $320; 4 months divides by the job pay only.)" % cap(he)))
    acc = fig(cards_svg([("Account A", ["Interest: 2.5% a year", "Fee: $3 a month"]),
                         ("Account B", ["Interest: 1% a year", "Fee: none"])]))
    a1, b1 = interest(1000, F("2.5"), 1) - 36, interest(1000, 1, 1)
    assert a1 == -11 and b1 == 10
    its.append(mcq(acc + "You keep $1000 in a savings account for 1 year. Which account leaves you with more money?",
                   "Account B, by $21", ["Account A, by $15", "Account B, by $10", "They are the same"],
                   "Account A: interest $1000 × 0.025 = $25, fees 12 × $3 = $36, so you lose $11. "
                   "Account B: interest $1000 × 0.01 = $10, no fees. $10 − (−$11) = $21, so <b>Account B, by $21</b>. "
                   "(Account A, by $15 forgets the monthly fees.)"))
    a2, b2 = interest(5000, F("2.5"), 1) - 36, interest(5000, 1, 1)
    assert a2 == 89 and b2 == 50
    its.append(mcq(acc + "You keep $5000 in a savings account for 1 year. Which account leaves you with more money?",
                   "Account A, by $39", ["Account B, by $39", "Account A, by $75", "They are the same"],
                   "Account A: $5000 × 0.025 = $125 interest, minus $36 in fees = $89. Account B: $5000 × 0.01 = $50. "
                   "$89 − $50 = $39, so <b>Account A, by $39</b>. With more money saved, the higher rate beats the fee. "
                   "(Account A, by $75 forgets the fees.)"))
    cards = fig(cards_svg([("Card A", ["Interest: 19.99% a year", "Annual fee: none"]),
                           ("Card B", ["Interest: 12.99% a year", "Annual fee: $40"])]))
    ca, cb = 1000 * F("0.1999"), 1000 * F("0.1299") + 40
    assert ca == F("199.90") and cb == F("169.90")
    its.append(mcq(cards + "Suppose you carry a $1000 balance on a credit card for a whole year. Using simple interest, "
                   "which card costs less?", "Card B, by $30", ["Card A, by $30", "Card B, by $70", "They cost the same"],
                   "Card A: $1000 × 0.1999 = $199.90. Card B: $1000 × 0.1299 = $129.90, plus the $40 fee = $169.90. "
                   "$199.90 − $169.90 = $30, so <b>Card B, by $30</b>. (Card B, by $70 forgets the fee.)"))
    its.append(mcq(cards + "Jayden always pays his credit card bill in full by the due date, so he never pays interest. Which card is better for him?",
                   "Card A, because it has no fee", ["Card B, because its rate is lower", "Card B, because it has a fee",
                                                    "They cost the same"],
                   "If the bill is always paid in full, no interest is charged, so the rate does not matter. "
                   "<b>Card A</b> has no annual fee, so it costs Jayden $0. Card B costs $40 a year."))
    assert interest(2000, 6, 2) == 240 and interest(2000, 5, 3) == 300
    its.append(mcq("A family borrows $2000 for a canoe. Loan A is 6% simple interest for 2 years. Loan B is 5% simple interest for 3 years. "
                   "Which loan costs less interest?", "Loan A, by $60", ["Loan B, by $60", "Loan B, by $100", "They cost the same"],
                   "Loan A: $2000 × 0.06 × 2 = $240. Loan B: $2000 × 0.05 × 3 = $300. <b>Loan A costs $60 less</b>. "
                   "A lower rate does not always mean less interest; the time matters too."))
    n, he, his, him = P.next()
    assert interest(600, 10, 1) == 60
    its.append(mcq("A phone costs $600. %s can save $50 a month for 12 months and then buy it, or borrow $600 now at 10%% simple interest "
                   "and pay it back in 1 year. How much more does borrowing cost?" % n,
                   "$60 more", ["$6000 more", "$50 more", "Nothing more"],
                   "Interest on the loan: $600 × 0.10 × 1 = <b>$60</b>. Saving first costs exactly $600. "
                   "Borrowing gets the phone sooner but costs $60 more. ($6000 uses 10 instead of 0.10.)"))
    n, he, his, him = P.next()
    usd = F(400)
    need = usd * F("1.35")
    assert need == 540 and ceil((need - 300) / 40) == 6
    its.append(mcq("Suppose US$1 = C$1.35. %s wants US$400 of spending money for a trip to Florida. %s has C$300 saved and saves C$40 a week. "
                   "How many more weeks until %s has enough?" % (n, cap(he), he),
                   "6 weeks", ["3 weeks", "14 weeks", "2 weeks"],
                   "US$400 × 1.35 = C$540. Still needed: C$540 − C$300 = C$240. C$240 ÷ C$40 = <b>6 weeks</b>. "
                   "(3 weeks forgets to convert the US dollars; 14 weeks forgets the C$300 already saved.)"))
    n, he, his, him = P.next()
    tot = 2000 + interest(2000, 3, 2)
    assert tot == 2120
    its.append(mcq("%s puts $2000 in a savings account at 3%% simple interest per year. After 2 years, will %s have enough for a $2100 trip?"
                   % (n, he), "Yes, with $20 to spare", ["No, $40 short", "No, $100 short", "Yes, with $120 to spare"],
                   "Interest: $2000 × 0.03 × 2 = $120. Balance: $2120. $2120 − $2100 = $20, so <b>yes, with $20 to spare</b>. "
                   "(No, $40 short uses only 1 year of interest.)"))
    assert 300 * F("1.50") == 450 and F(450) / 9 == 50
    its.append(cq("Lucas’s family is going to France next summer. Lucas wants €300 of spending money. "
                  "Suppose €1 = C$1.50. He saves the C$ amount over 9 months. How much is that each month?",
                  50, [F(300) / 9, F(200) / 9, 450],
                  "€300 × 1.50 = C$450. C$450 ÷ 9 = <b>C$50.00</b> a month. "
                  "(C$33.33 forgets to convert the euros; C$22.22 divides by 1.50.)", C))
    assert 2400 * F(1, 100) == 24
    its.append(cq("A credit card gives 1% cash back. Zoe’s family spends $2400 on the card in a year and pays the bill in full each month. "
                  "How much cash back do they get?", 24, [240, F("2.40"), 2400],
                  "1% = 0.01. $2400 × 0.01 = <b>$24.00</b>. ($240.00 is 10%.)", M))
    n, he, his, him = P.next()
    assert interest(1500, 2, 3) == 90
    its.append(cq("%s has $1500 from summer jobs. It could sit in a drawer, or go in a savings account at 2%% simple interest per year. "
                  "How much more will %s have after 3 years with the account?" % (n, he), 90, [30, 9000, 1590],
                  "Interest: $1500 × 0.02 × 3 = <b>$90.00</b>. Money in a drawer earns nothing. "
                  "($30.00 is only 1 year; $1590.00 is the whole balance.)", M))
    n, he, his, him = P.next()
    end = 800 + interest(800, F("1.5"), 1) - 24
    assert end == 788
    its.append(cq("%s keeps $800 in an account that pays 1.5%% simple interest per year but charges a $2 fee each month. "
                  "How much is in the account after 1 year?" % n, end, [812, 810, 776],
                  "Interest: $800 × 0.015 = $12. Fees: 12 × $2 = $24. $800 + $12 − $24 = <b>$788.00</b>. "
                  "($812.00 forgets the fees; $810.00 takes only one $2 fee.)", M))
    n, he, his, him = P.next()
    assert 300 * F(1, 5) == 60 and F(900) / 60 == 15
    its.append(mcq("%s earns $300 a month and saves 20%% of it. How many months will it take to save $900?" % n,
                   months(15), [months(3), months(45), months(5)],
                   "20% of $300: $300 × 0.20 = $60 a month. $900 ÷ $60 = <b>15 months</b>. "
                   "(3 months saves all $300 each month; 45 uses $20 instead of 20%.)"))
    assert interest(400, 15, 1) == 60
    its.append(cq("A store offers to let a family pay for a $400 bike over 1 year at 15% simple interest. A grandparent offers to lend "
                  "the $400 with no interest. How much does the family save by borrowing from the grandparent?",
                  60, [6000, 460, 15],
                  "Store interest: $400 × 0.15 × 1 = $60. The grandparent charges $0, so they save <b>$60.00</b>. "
                  "($460.00 is the total paid to the store; $6000.00 uses 15 instead of 0.15.)", M))
    n, he, his, him = P.next()
    assert 350 * F("1.36") == 476 and F(476) / 4 == 119
    its.append(cq("Suppose US$1 = C$1.36. A summer hockey camp in Michigan costs US$350. %s’s family pays the C$ amount in 4 equal "
                  "monthly payments. How much is each payment?" % n, 119, [F("87.50"), F(350) / F("1.36") / 4, 476],
                  "US$350 × 1.36 = C$476. C$476 ÷ 4 = <b>C$119.00</b>. "
                  "(C$87.50 forgets to convert; C$64.34 divides instead of multiplying.)", C))
    tot = 900 + interest(900, 6, 1)
    assert tot == 954 and tot / 12 == F("79.50")
    its.append(cq("Leah borrows $900 for a bike at 6% simple interest for 1 year and pays it back in 12 equal monthly payments. "
                  "How much is each payment?", F("79.50"), [75, F("4.50"), 954],
                  "Interest: $900 × 0.06 = $54. Total: $954. Each month: $954 ÷ 12 = <b>$79.50</b>. "
                  "($75.00 forgets the interest.)", M))
    assert len(its) == 20
    return {"title": "Budgets, goals and choosing accounts", "items": its}


# ============================================================ lesson
def body_html():
    assert 270 / F("1.35") == 200 and 40 * F("1.50") == 60 and interest(800, 3, 2) == 48
    return (
        "<h2>Exchange rates</h2>"
        "<p>An <b>exchange rate</b> tells you how much one currency is worth in another. C$ means Canadian dollars, "
        "US$ means US dollars, € means euros and ¥ means Japanese yen. Real rates change every day, so this page uses "
        "<b>sample rates</b>, such as US$1 = C$1.35.</p>"
        "<figure class='sn-fig'>" + dnl_svg(F("1.35"), 4) +
        "<figcaption>US$1 = C$1.35, so US$2 = C$2.70, US$3 = C$4.05 and US$4 = C$5.40.</figcaption></figure>"
        "<p>Read the rate as “1 foreign unit = some Canadian dollars”. Then:</p>" +
        table(["You have", "You want", "Do this (US$1 = C$1.35)"], [
            ["Foreign money", "Canadian dollars", "Multiply by the rate: US$40 × 1.35 = C$54"],
            ["Canadian dollars", "Foreign money", "Divide by the rate: C$270 ÷ 1.35 = US$200"],
        ]) +
        "<p>Check your answer. One US dollar is worth more than one Canadian dollar here, so the C$ number must be the bigger one.</p>" +
        ex("Example", "Suppose €1 = C$1.50. How many euros do you get for C$300?",
           "Each euro costs C$1.50. C$300 ÷ 1.50 = 200. Check: 200 × 1.50 = 300.", "€200") +
        ex("Example", "Suppose C$1 = ¥110. How many yen do you get for C$50?",
           "This rate tells you what C$1 buys, so multiply: 50 × 110 = 5500.", "¥5500") +
        "<h2>Comparing prices</h2>"
        "<p>To compare prices in two currencies, change one price into the other currency first. Then compare.</p>" +
        ex("Example", "Suppose US$1 = C$1.35. A hoodie costs US$40 in the US and C$56 in Canada. Where is it cheaper?",
           "US$40 × 1.35 = C$54. C$54 &lt; C$56.", "In the US, by C$2") +
        "<h2>Simple interest</h2>"
        "<p>Interest is the cost of using money. A bank pays you interest on savings. You pay interest when you borrow. "
        "Simple interest uses <b>I = Prt</b>: principal × yearly rate (as a decimal) × time in years.</p>" +
        ex("Example", "You save $800 at 3% simple interest per year for 2 years. How much interest do you earn?",
           "3% = 0.03. I = $800 × 0.03 × 2 = $48. The balance is $800 + $48 = $848.", "$48") +
        "<h2>Choosing an account, a loan or a card</h2>"
        "<p>Look at the whole cost, not just the rate: interest, monthly or annual fees and rewards. "
        "A low rate with a high fee can cost more. If you pay a credit card bill in full every month, the fee matters more than the rate. "
        "For a long-term goal, find what you still need and divide it by what you can save each month.</p>"
        "<figure class='sn-fig'>" + cards_svg([("Account A", ["Interest: 2.5% a year", "Fee: $3 a month"]),
                                                 ("Account B", ["Interest: 1% a year", "Fee: none"])]) +
        "<figcaption>With $1000 for a year, Account A earns $25 but charges $36 in fees. Account B earns $10 with no fees, so it is better.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Multiplying when you should divide (C$270 × 1.35)", "C$ to US$ with US$1 = C$1.35: divide, C$270 ÷ 1.35 = US$200"],
            ["Taking 35% off instead of dividing by 1.35", "Dividing by 1.35 is not the same as subtracting 35%"],
            ["Comparing US$20 with C$25 directly", "Convert to the same currency first"],
            ["Using the rate as a whole number (3 for 3%)", "Write the rate as a decimal: 3% = 0.03"],
            ["Using 6 for 6 months", "Time is in years: 6 months = 0.5"],
            ["Giving the interest as the balance", "Balance = principal + interest"],
            ["Choosing the account with the higher rate only", "Subtract the fees and compare what is left"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn in financial literacy in Ontario?",
     "a": "Grade 7 students compare exchange rates and convert between Canadian dollars and other currencies, plan budgets for longer-term goals, "
          "and learn how interest rates affect saving and borrowing. They also compare bank accounts, loans and credit cards."},
    {"q": "How do you convert Canadian dollars to US dollars?",
     "a": "If the rate is written as US$1 = C$1.35, divide the Canadian amount by 1.35: C$270 ÷ 1.35 = US$200. "
          "To go from US dollars to Canadian dollars, multiply by 1.35."},
    {"q": "How do you calculate simple interest in Grade 7?",
     "a": "Use I = Prt: principal × yearly rate as a decimal × time in years. For $800 at 3% for 2 years, I = 800 × 0.03 × 2 = $48."},
    {"q": "Are the exchange rates on these worksheets real?",
     "a": "No. Real exchange rates change every day, so every question gives a sample rate, such as US$1 = C$1.35. "
          "Students learn the method and can then use the rate posted by a bank on the day."},
]


def gen():
    rnd = random.Random(47820)
    P = People(rnd)
    sets = [set_cad_to_foreign(P), set_foreign_to_cad(P), set_compare(P), set_interest(P), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert not re.search(r"\d,\d{3}", re.sub(r"<[^>]+>", "", x)), x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "exchange-rates-and-interest", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Exchange Rates and Interest: Converting Currencies, Simple Interest and Budgets",
        "seo_title": "Grade 7 Exchange Rates and Simple Interest Worksheets (Free, Answer Key) | Ontario Math",
        "short_title": "Exchange Rates and Interest",
        "domain": "Financial Literacy",
        "standard_code": "Grade 7: F1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify and compare exchange rates, and convert foreign currencies to Canadian dollars and vice versa",
        "meta_desc": "Free Grade 7 math worksheets on exchange rates and interest for the Ontario curriculum: convert Canadian dollars to "
                     "US dollars, euros and yen and back, compare prices in two currencies, simple interest on savings and loans, "
                     "and budgets for longer-term goals. 100 questions with an answer key.",
        "key_big": "Foreign money to C$: multiply by the rate. C$ to foreign money: divide.",
        "key_sub": "With US$1 = C$1.35, US$40 × 1.35 = C$54 and C$270 ÷ 1.35 = US$200. Simple interest is I = Prt, "
                   "with the rate as a decimal (3% = 0.03) and the time in years.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Double number line")
    mark_large(u, "Offers: ")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
