# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Decimals and percentages
(National Curriculum in England, Year 5: Fractions (including decimals and percentages))
  python3 tools/gen_uk_maths_y5_decimals_percentages.py
Decimals as fractions and thousandths; compare and order up to three decimal places; round 2-place decimals
to the nearest whole number and to 1 decimal place (halfway rounds up); per cent as parts per hundred;
equivalents of 1/2, 1/4, 1/5, 2/5, 4/5 and denominators of 10, 25 and 50.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
British English, pounds and pence, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(£)?([\d,]*\.?\d+)(p|%)?( .+)?$")


def val(c):
    """Value of a choice (Fraction) with its unit; 20% is 1/5 with unit '' so 20% and 0.2 count as equal.
    None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(",", ""))
    if m.group(1):
        return (v, "£")
    if m.group(3) == "p":
        return (v / 100, "£")
    if m.group(3) == "%":
        v = v / 100
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False):
    """4 choices: correct first + 3 wrong. Positions are set by balance(). No two choices may have the same value
    (same_ok=True only for 'Which is NOT equal ...?' questions)."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
        assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def dec(v, places=None):
    """Exact decimal text of a Fraction with a terminating decimal (no trailing zeros unless places is given)."""
    v = F(v)
    d = Dm(v.numerator) / Dm(v.denominator)
    assert F(d) == v, v
    if places is not None:
        s = format(d.quantize(Dm(1).scaleb(-places)), "f")
        assert F(Dm(s)) == v
        return s
    return format(d.normalize(), "f")


def pct(v):
    return dec(F(v) * 100) + "%"


PLACE = {1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


def digit_place(num, k):
    """(digit, place) of the digit k (a character) in num text; k must appear exactly once."""
    assert num.count(k) == 1, (num, k)
    w, _, f = num.partition(".")
    if k in w:
        return len(w) - 1 - w.index(k)
    return -(f.index(k) + 1)


def place_value(num, k):
    p = digit_place(num, k)
    return F(int(k)) * F(10) ** p


# ------------------------------------------------------------ pictures
def grid_body(k, ox, oy, cell):
    """10 x 10 hundred square at (ox, oy) with k squares shaded: full columns first, then from the top of the next column."""
    assert 0 <= k <= 100
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox + c * cell, oy + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, LINE))
    return "".join(s)


def grid_svg(k, cell=18):
    pad = 4
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "hundred square with %d of 100 squares shaded" % k)


PV_ALL = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths"), (-3, "Thousandths")]


def chart_svg(rows, hi=None):
    """Place value chart: (Tens) | Ones | . | Tenths | Hundredths | Thousandths. hi: (row, place) drawn in red."""
    tens = any(len(r.partition(".")[0]) > 1 for r in rows)
    cols = PV_ALL if tens else PV_ALL[1:]
    CW, PW, HEAD, ROW = 108, 16, 30, 44
    x0, y0 = 6, 6
    W = 2 * x0 + len(cols) * CW + PW
    H = 2 * y0 + HEAD + ROW * len(rows)
    xs, x = {}, x0
    for p, _ in cols:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, W - 2 * x0, HEAD + ROW * len(rows), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, HEADFILL)]
    for p, name in cols:
        if p != cols[0][0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW * len(rows), GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, name, 14))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW * len(rows), GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    for r, s in enumerate(rows):
        yb = y0 + HEAD + ROW * r
        if r:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, yb, W - x0, yb, GREEN))
        w, _, f = s.partition(".")
        assert len(w) <= (2 if tens else 1) and len(f) <= 3, s
        digits = {}
        for j, ch in enumerate(w):
            digits[len(w) - 1 - j] = ch
        for j, ch in enumerate(f):
            digits[-(j + 1)] = ch
        for p, ch in digits.items():
            o.append(text(xs[p] + CW / 2.0, yb + 32, ch, 28, col=RED if hi == (r, p) else LINE, weight=800))
        if f:
            o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, yb + 31, LINE))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % " and ".join(rows))



def rnd_dp(x, places):
    """Round a decimal text half up (the way it is taught in English schools) and return the text with that many places."""
    q = Dm(1).scaleb(-places)
    return format(Dm(x).quantize(q, rounding=ROUND_HALF_UP), "f")


def line_svg(a, b, spaces, dot, labels, W=400):
    """Number line from a to b thousandths with `spaces` equal spaces; red dot at `dot` thousandths (may sit between ticks).
    labels: thousandths values written under the line."""
    L, R, Y = 30, W - 30, 30
    assert (b - a) % spaces == 0 and a <= dot <= b
    step = (b - a) // spaces

    def X(v):
        return L + (R - L) * (v - a) / float(b - a)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
    for v in labels:
        assert (v - a) % step == 0
        s.append(text(X(v), Y + 36, dec(F(v, 1000)), 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from %s to %s split into %d equal spaces"
                    % (dec(F(a, 1000)), dec(F(b, 1000)), spaces))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


# ============================================================ set 1: decimals as fractions, thousandths
def set_fractions():
    its = []
    for d_, (n, dd), wrong, e in [
        ("0.3", (3, 10), [fr(3, 100), fr(1, 3), fr(3, 1000)],
         "0.3 has <b>one</b> decimal place, so the 3 is in the tenths place: 3 tenths = <b>%s</b>." % fr(3, 10)),
        ("0.71", (71, 100), [fr(7, 10), fr(71, 10), fr(71, 1000)],
         "0.71 has <b>two</b> decimal places, so the last digit is in the hundredths place: 71 hundredths = <b>%s</b>. "
         "%s would be 7.1." % (fr(71, 100), fr(71, 10))),
        ("0.09", (9, 100), [fr(9, 10), fr(9, 1000), fr(1, 9)],
         "Two decimal places means hundredths. The tenths digit is 0, so 0.09 = 9 hundredths = <b>%s</b>." % fr(9, 100)),
        ("0.007", (7, 1000), [fr(7, 100), fr(7, 10), fr(1, 7)],
         "0.007 has <b>three</b> decimal places, so the 7 is in the thousandths place: <b>%s</b>. "
         "%s would be 0.07." % (fr(7, 1000), fr(7, 100))),
        ("0.453", (453, 1000), [fr(453, 100), fr(453, 10), fr(3, 1000)],
         "Three decimal places means thousandths: 0.453 = 453 thousandths = <b>%s</b>. "
         "%s is only the last digit." % (fr(453, 1000), fr(3, 1000))),
    ]:
        assert F(Dm(d_)) == F(n, dd)
        its.append(mcq("Write <b>%s</b> as a fraction." % d_, fr(n, dd), wrong, e))
    for (n, dd), right, wrong, e in [
        ((29, 100), "0.29", ["2.9", "0.029", "29"],
         "29 hundredths: the last digit goes in the <b>second</b> place after the point. %s = <b>0.29</b>." % fr(29, 100)),
        ((7, 1000), "0.007", ["0.07", "0.7", "0.0007"],
         "7 thousandths: the 7 goes in the <b>third</b> place after the point. Write 0s in the tenths and hundredths places: "
         "<b>0.007</b>. 0.07 is 7 hundredths."),
        ((63, 1000), "0.063", ["0.63", "6.3", "0.0063"],
         "63 thousandths = 6 hundredths and 3 thousandths. The last digit must be in the third place: <b>0.063</b>. "
         "0.63 would be 63 hundredths."),
    ]:
        assert F(Dm(right)) == F(n, dd)
        its.append(mcq("Write %s as a decimal." % fr(n, dd), right, wrong, e))
    its.append(mcq(fig(chart_svg(["2.738"], hi=(0, -3))) + "What is the value of the red digit in 2.738?",
                   "8 thousandths", ["8 hundredths", "8 tenths", "8 ones"],
                   "The red 8 is the <b>third</b> digit after the decimal point, in the thousandths column. "
                   "Its value is <b>8 thousandths</b> = 0.008."))
    its.append(mcq(fig(chart_svg(["5.064"], hi=(0, -2))) + "What is the value of the red digit in 5.064?",
                   "6 hundredths", ["6 tenths", "6 thousandths", "6 ones"],
                   "The red 6 is the <b>second</b> digit after the decimal point, in the hundredths column. "
                   "Its value is <b>6 hundredths</b> = 0.06. The 0 holds the tenths place."))
    its.append(mcq("What is the value of the digit <b>4</b> in <b>3.124</b>?", "0.004", ["0.04", "0.4", "4"],
                   "Tenths, hundredths, thousandths: 3 . 1 2 <b>4</b>. The 4 is in the thousandths place, "
                   "so it is worth 4 thousandths = <b>0.004</b>."))
    its.append(mcq("Write <b>3 ones, 5 hundredths and 2 thousandths</b> as a decimal.", "3.052", ["3.52", "3.502", "3.0052"],
                   "There are 0 tenths, so write a 0 in the tenths place: 3 . 0 5 2 = <b>3.052</b>. "
                   "3.52 would have 5 tenths."))
    its.append(mcq("1 hundredth is split into 10 equal parts. What decimal is each part?", "0.001", ["0.01", "0.1", "0.0001"],
                   "A hundredth divided by 10 is a <b>thousandth</b>: %s = <b>0.001</b>. "
                   "1 whole = 10 tenths = 100 hundredths = 1,000 thousandths." % fr(1, 1000)))
    its.append(mcq("How many thousandths are there in <b>1 hundredth</b>?", "10", ["100", "1,000", "0.1"],
                   "1 hundredth = 0.01 = 0.010. That is <b>10</b> thousandths."))
    its.append(mcq("How many thousandths are there in <b>0.3</b>?", "300", ["3", "30", "3,000"],
                   "1 tenth = 100 thousandths, so 3 tenths = <b>300</b> thousandths. 0.3 = 0.300 = %s." % fr(300, 1000)))
    its.append(mcq("Which number is equal to <b>0.6</b>?", "0.600", ["0.06", "0.006", "6.00"],
                   "A 0 at the <b>end</b> of a decimal does not change its value: 0.6 = 0.60 = <b>0.600</b>. "
                   "0.06 and 0.006 have the 6 in a different place."))
    its.append(mcq("%s + %s + %s = ?" % (fr(6, 10), fr(4, 100), fr(9, 1000)), "0.649", ["0.946", "6.49", "0.0649"],
                   "6 tenths, 4 hundredths and 9 thousandths: 0 . 6 4 9 = <b>0.649</b>."))
    its.append(mcq("0.35 = %s = %s" % (fr(35, 100), fr("?", 1000)), "350", ["35", "3,500", "305"],
                   "Multiply the numerator and the denominator by 10: %s = %s. So the missing number is <b>350</b>. "
                   "0.35 = 0.350." % (fr(35, 100), fr(350, 1000))))
    its.append(mcq("Write <b>2.09</b> as a mixed number.", mixed(2, 9, 100), [mixed(2, 9, 10), fr(29, 100), mixed(2, 1, 9)],
                   "2 wholes, then 0.09 = 9 hundredths. So 2.09 = <b>%s</b>. %s would be 2.9." % (mixed(2, 9, 100), mixed(2, 9, 10))))
    its.append(mcq("What number is <b>1 thousandth more</b> than 4.209?", "4.21", ["4.219", "4.2010", "4.309"],
                   "9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. So 4.209 + 0.001 = 4.210 = <b>4.21</b>. "
                   "4.219 adds 1 hundredth, not 1 thousandth."))
    order = [0, 1, 2, 5, 3, 6, 4, 7, 8, 9, 10, 11, 15, 12, 13, 14, 16, 17, 18, 19]
    return {"title": "Decimals as fractions and thousandths", "items": reorder(its, order)}


# ============================================================ set 2: compare and order
def cmp_item(x, y, e):
    a, b = Dm(x), Dm(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare <b>%s</b> and <b>%s</b>." % (x, y), right, wrong, e, same_ok=True)


def order_q(q, nums, asc, wrongs, e):
    right = ", ".join(sorted(nums, key=Dm, reverse=not asc))
    ws = [", ".join(w) for w in wrongs]
    assert right not in ws and len(set(ws)) == 3
    for w in wrongs:
        assert sorted(w) == sorted(nums)
    return mcq(q, right, ws, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.5", "0.45", "0.5 = 0.50. Compare the tenths: 5 tenths &gt; 4 tenths. So <b>0.5 &gt; 0.45</b>. "
                        "More digits does not mean a bigger number."))
    its.append(cmp_item("0.38", "0.4", "0.4 = 0.40. Compare the tenths: 3 &lt; 4. So <b>0.38 &lt; 0.4</b>."))
    its.append(cmp_item("0.405", "0.45", "Write both with 3 places: 0.405 and 0.450. The tenths are the same. "
                        "Compare the hundredths: 0 &lt; 5. So <b>0.405 &lt; 0.45</b>."))
    its.append(cmp_item("2.07", "2.070", "A 0 at the end does not change the value. 2.07 = 2.070, so <b>2.07 = 2.070</b>."))
    its.append(cmp_item("0.009", "0.09", "0.09 = 0.090. Compare the hundredths: 0 &lt; 9. So <b>0.009 &lt; 0.09</b>. "
                        "9 thousandths is less than 9 hundredths."))
    its.append(cmp_item("3.125", "3.12", "3.12 = 3.120. Ones, tenths and hundredths are the same. Compare the thousandths: "
                        "5 &gt; 0. So <b>3.125 &gt; 3.12</b>."))
    its.append(cmp_item("1.9", "1.899", "1.9 = 1.900. The ones are the same. Compare the tenths: 9 &gt; 8. "
                        "So <b>1.9 &gt; 1.899</b>."))
    its.append(cmp_item("0.62", "0.602", "0.62 = 0.620. The tenths are the same. Compare the hundredths: 2 &gt; 0. "
                        "So <b>0.62 &gt; 0.602</b>."))
    its.append(mcq("Which number is the <b>greatest</b>?", "0.7", ["0.68", "0.699", "0.075"],
                   "Write them with 3 places: 0.700, 0.680, 0.699, 0.075. Compare the tenths first: only 0.7 has 7 tenths. "
                   "So <b>0.7</b> is the greatest."))
    its.append(mcq("Which number is the <b>smallest</b>?", "0.205", ["0.25", "0.3", "0.52"],
                   "Write them with 3 places: 0.205, 0.250, 0.300, 0.520. The smallest is <b>0.205</b>, "
                   "even though it has the most digits."))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.5, 0.45, 0.405</b>", ["0.5", "0.45", "0.405"], True,
                       [["0.5", "0.45", "0.405"], ["0.45", "0.405", "0.5"], ["0.405", "0.5", "0.45"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405. Compare 500, 450 and 405 thousandths. "
                       "So <b>0.405, 0.45, 0.5</b>."))
    its.append(order_q("Order from <b>greatest to smallest</b>:<br><b>3.2, 3.18, 3.205, 3.02</b>", ["3.2", "3.18", "3.205", "3.02"],
                       False, [["3.205", "3.18", "3.2", "3.02"], ["3.02", "3.18", "3.2", "3.205"], ["3.2", "3.205", "3.18", "3.02"]],
                       "Write them with 3 places: 3.200, 3.180, 3.205, 3.020. Greatest first: <b>3.205, 3.2, 3.18, 3.02</b>."))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.6, 0.06, 0.606, 0.066</b>", ["0.6", "0.06", "0.606", "0.066"],
                       True, [["0.06", "0.6", "0.066", "0.606"], ["0.6", "0.06", "0.066", "0.606"], ["0.066", "0.06", "0.606", "0.6"]],
                       "Write them with 3 places: 0.600, 0.060, 0.606, 0.066. Compare 600, 60, 606 and 66 thousandths. "
                       "So <b>0.06, 0.066, 0.6, 0.606</b>."))
    its.append(mcq("Which number is between <b>0.4</b> and <b>0.5</b>?", "0.408", ["0.048", "0.54", "0.399"],
                   "0.4 = 0.400 and 0.5 = 0.500. <b>0.408</b> is between them. 0.048 and 0.399 are less than 0.4, "
                   "and 0.54 is more than 0.5."))
    its.append(mcq("Which number is between <b>2.3</b> and <b>2.31</b>?", "2.305", ["2.35", "2.031", "2.315"],
                   "2.3 = 2.300 and 2.31 = 2.310. <b>2.305</b> is between 2.300 and 2.310. "
                   "2.35 and 2.315 are more than 2.31."))
    its.append(mcq(fig(line_svg(1200, 1300, 10, 1240, [1200, 1250, 1300])) + "What number is at the red dot?",
                   "1.24", ["1.204", "1.4", "1.34"],
                   "The line goes from 1.2 to 1.3 in 10 equal spaces, so each space is 1 hundredth. "
                   "Count 4 spaces on from 1.20: <b>1.24</b>."))
    its.append(mcq(fig(line_svg(320, 330, 10, 326, [320, 325, 330])) + "What number is at the red dot?",
                   "0.326", ["0.36", "0.306", "0.336"],
                   "The line goes from 0.32 to 0.33 in 10 equal spaces, so each space is 1 thousandth. "
                   "Count 6 spaces on from 0.320: <b>0.326</b>."))
    its.append(mcq("What number is <b>0.01 less</b> than 3.2?", "3.19", ["3.1", "3.199", "3.21"],
                   "3.2 = 3.20. Take away 1 hundredth: exchange 1 tenth for 10 hundredths. 3.20 − 0.01 = <b>3.19</b>. "
                   "3.199 is 0.001 less."))
    its.append(mcq("How many of these numbers are <b>greater than 0.6</b>?<br><b>0.59, 0.61, 0.596, 0.601</b>", "2",
                   ["1", "3", "4"],
                   "0.6 = 0.600. Compare: 0.590 &lt; 0.600, 0.610 &gt; 0.600, 0.596 &lt; 0.600, 0.601 &gt; 0.600. "
                   "So <b>2</b> numbers (0.61 and 0.601) are greater."))
    its.append(mcq("0.4□7 &lt; 0.45<br>What is the <b>greatest</b> digit that can go in the box?", "4", ["5", "9", "3"],
                   "0.45 = 0.450. With 4 in the box: 0.447 &lt; 0.450. With 5: 0.457 &gt; 0.450. So the greatest digit is <b>4</b>."))
    order = [0, 1, 3, 4, 2, 5, 6, 7, 8, 9, 13, 15, 10, 17, 11, 14, 16, 12, 18, 19]
    return {"title": "Compare and order decimals up to 3 places", "items": reorder(its, order)}


# ============================================================ set 3: rounding
def round_q(x, places, right, wrong, e, stem=None):
    assert rnd_dp(x, places) == right, (x, places, right)
    q = stem or ("Round <b>%s</b> to %s." % (x, "the nearest whole number" if places == 0 else "1 decimal place"))
    return mcq(q, right, wrong, e)


def set_round():
    its = []
    its.append(round_q("4.38", 0, "4", ["5", "4.4", "4.3"],
                       "To round to the nearest whole number, look at the <b>tenths</b> digit: 3. 4 or less rounds down. "
                       "4.38 is between 4 and 5, nearer to <b>4</b>."))
    its.append(round_q("7.62", 0, "8", ["7", "7.6", "7.7"],
                       "Look at the tenths digit: 6. 5 or more rounds up. 7.62 is between 7 and 8, nearer to <b>8</b>."))
    its.append(round_q("0.83", 0, "1", ["0", "0.8", "0.9"],
                       "Look at the tenths digit: 8. 5 or more rounds up. 0.83 is between 0 and 1, nearer to <b>1</b>."))
    its.append(round_q("9.51", 0, "10", ["9", "9.5", "9.6"],
                       "Look at the tenths digit: 5. 5 or more rounds up. 9.51 is between 9 and 10, so it rounds to <b>10</b>."))
    its.append(round_q("12.49", 0, "12", ["13", "12.5", "12.4"],
                       "Look <b>only</b> at the tenths digit: 4. 4 or less rounds down, so 12.49 rounds to <b>12</b>. "
                       "Do not round twice (12.49 → 12.5 → 13): 12.49 is less than halfway (12.5)."))
    its.append(round_q("6.72", 1, "6.7", ["6.8", "7", "6.2"],
                       "To round to 1 decimal place, look at the <b>hundredths</b> digit: 2. 4 or less rounds down. "
                       "6.72 is between 6.7 and 6.8, nearer to <b>6.7</b>."))
    its.append(round_q("0.64", 1, "0.6", ["0.7", "1", "0.5"],
                       "Look at the hundredths digit: 4. 4 or less rounds down. 0.64 is between 0.6 and 0.7, nearer to <b>0.6</b>."))
    its.append(round_q("3.45", 1, "3.5", ["3.4", "3", "4"],
                       "Look at the hundredths digit: 5. 5 or more rounds <b>up</b>. 3.45 is exactly halfway between 3.4 and 3.5, "
                       "and halfway rounds up: <b>3.5</b>."))
    its.append(round_q("2.08", 1, "2.1", ["2", "2.8", "3"],
                       "2.08 is between 2.0 and 2.1. Look at the hundredths digit: 8. 5 or more rounds up, so the 0 tenths "
                       "become 1 tenth: <b>2.1</b>."))
    its.append(round_q("14.35", 1, "14.4", ["14.3", "14", "15"],
                       "Look at the hundredths digit: 5. 5 or more rounds up. 14.35 is halfway between 14.3 and 14.4, "
                       "so it rounds up to <b>14.4</b>."))
    its.append(round_q("5.96", 1, "6.0", ["5.9", "5.10", "5.0"],
                       "Look at the hundredths digit: 6, so round up. 9 tenths + 1 tenth = 10 tenths = 1 whole. "
                       "So 5.96 rounds to <b>6.0</b>. Keep the 0 to show it is rounded to 1 decimal place."))
    its.append(round_q("2.45", 0, "2", ["3", "2.5", "2.4"],
                       "Look <b>only</b> at the tenths digit: 4. 4 or less rounds down, so 2.45 rounds to <b>2</b>. "
                       "Rounding twice (2.45 → 2.5 → 3) is a common mistake."))
    its.append(round_q("3.47", 1, "3.5", ["3.4", "3", "3.45"],
                       "The dot is between 3.4 and 3.5. It is past the halfway mark (3.45), so it is nearer to <b>3.5</b>. "
                       "The hundredths digit is 7: 5 or more rounds up.",
                       stem=fig(line_svg(3400, 3500, 10, 3470, [3400, 3450, 3500])) +
                       "The red dot shows 3.47. Round 3.47 to 1 decimal place."))
    its.append(round_q("8.36", 0, "8", ["9", "8.4", "8.5"],
                       "The dot is between 8 and 9. It is before the halfway mark (8.5), so it is nearer to <b>8</b>. "
                       "The tenths digit is 3: 4 or less rounds down.",
                       stem=fig(line_svg(8000, 9000, 10, 8360, [8000, 8500, 9000])) +
                       "The red dot shows 8.36. Round 8.36 to the nearest whole number."))
    for x in ["4.26", "4.36", "4.23", "4.35"]:
        assert (rnd_dp(x, 1) == "4.3") == (x == "4.26")
    its.append(mcq("Which number rounds to <b>4.3</b> to 1 decimal place?", "4.26", ["4.36", "4.23", "4.35"],
                   "Look at the hundredths digit. 4.26 rounds up to <b>4.3</b>. 4.36 rounds to 4.4, 4.23 rounds to 4.2, "
                   "and 4.35 is halfway, so it rounds up to 4.4."))
    for x in ["6.52", "7.5", "7.61", "6.49"]:
        assert (rnd_dp(x, 0) == "7") == (x == "6.52")
    its.append(mcq("Which number rounds to <b>7</b> to the nearest whole number?", "6.52", ["7.5", "7.61", "6.49"],
                   "6.52 has 5 tenths, so it rounds up to <b>7</b>. 7.5 and 7.61 round up to 8. 6.49 has 4 tenths, so it rounds down to 6."))
    its.append(mcq("What is the <b>smallest</b> number with 2 decimal places that rounds to <b>5.4</b>?", "5.35",
                   ["5.3", "5.36", "5.45"],
                   "Numbers from 5.35 up to 5.44 round to 5.4. The smallest is <b>5.35</b>, because halfway rounds up. "
                   "5.45 rounds up to 5.5."))
    assert rnd_dp("5.35", 1) == "5.4" and rnd_dp("5.34", 1) == "5.3" and rnd_dp("5.45", 1) == "5.5"
    its.append(mcq("What is the <b>greatest</b> number with 2 decimal places that rounds to <b>2</b> to the nearest whole number?",
                   "2.49", ["2.5", "2.4", "2.99"],
                   "Numbers up to 2.49 round down to 2. <b>2.49</b> is the greatest. 2.5 is halfway, so it rounds up to 3."))
    assert rnd_dp("2.49", 0) == "2" and rnd_dp("2.50", 0) == "3"
    for x in ["5.76", "5.74", "5.86", "6.8"]:
        assert (rnd_dp(x, 0) == "6" and rnd_dp(x, 1) == "5.8") == (x == "5.76")
    its.append(mcq("A number rounds to <b>6</b> to the nearest whole number and to <b>5.8</b> to 1 decimal place. "
                   "Which number could it be?", "5.76", ["5.74", "5.86", "6.8"],
                   "5.76 rounds to 5.8 (6 hundredths: round up) and to 6 (7 tenths: round up). So <b>5.76</b>. "
                   "5.74 rounds to 5.7, 5.86 rounds to 5.9, and 6.8 rounds to 7."))
    assert rnd_dp("4.65", 0) == "5" and rnd_dp("4.65", 1) == "4.7"
    its.append(mcq("Round <b>4.65</b> to the nearest whole number and to 1 decimal place.", "5 and 4.7",
                   ["4 and 4.6", "5 and 4.6", "4 and 4.7"],
                   "Nearest whole number: the tenths digit is 6, so round up to 5. 1 decimal place: the hundredths digit is 5, "
                   "so round up to 4.7. Answer: <b>5 and 4.7</b>.", same_ok=True))
    order = [0, 1, 2, 3, 13, 5, 6, 8, 12, 4, 7, 9, 11, 10, 14, 15, 16, 17, 18, 19]
    return {"title": "Round decimals to the nearest whole number and to 1 decimal place", "items": reorder(its, order)}


# ============================================================ set 4: per cent
def set_percent():
    its = []
    its.append(mcq(fig(grid_svg(37)) + "What percentage of the hundred square is shaded?", "37%", ["63%", "3.7%", "0.37%"],
                   "37 of the 100 squares are shaded. Per cent means <b>parts per hundred</b>, so it is <b>37%</b>. "
                   "63% is the white part."))
    its.append(mcq(fig(grid_svg(60)) + "What percentage of the hundred square is shaded?", "60%", ["6%", "40%", "0.6%"],
                   "6 full columns of 10 are shaded: 60 of the 100 squares = <b>60%</b>. 6% would be only 6 small squares."))
    its.append(mcq(fig(grid_svg(8)) + "What percentage of the hundred square is shaded?", "8%", ["80%", "92%", "0.8%"],
                   "8 of the 100 squares are shaded: <b>8%</b>. 80% would be 8 full columns."))
    its.append(mcq(fig(grid_svg(45)) + "What percentage of the hundred square is <b>not</b> shaded?", "55%",
                   ["45%", "65%", "5.5%"],
                   "45 squares are shaded, so 100 − 45 = 55 squares are white. 55 out of 100 = <b>55%</b>."))
    its.append(mcq(fig(grid_svg(25)) + "Which shows the shaded part as a fraction and as a percentage?",
                   "%s and 25%%" % fr(25, 100), ["%s and 25%%" % fr(25, 10), "%s and 25%%" % fr(1, 25), "%s and 75%%" % fr(25, 100)],
                   "25 of 100 squares: %s = <b>25%%</b>. The denominator is 100 because the square has 100 parts." % fr(25, 100),
                   same_ok=True))
    its.append(mcq("What does <b>per cent</b> mean?", "out of 100", ["out of 10", "out of 1,000", "out of 50"],
                   "“Per cent” means <b>out of 100</b> (parts per hundred). 23% means 23 parts out of 100."))
    its.append(mcq("Write <b>23%</b> as a fraction.", fr(23, 100), [fr(23, 10), fr(23, 1000), fr(1, 23)],
                   "Per cent means out of 100: 23%% = <b>%s</b>." % fr(23, 100)))
    its.append(mcq("Write <b>9%</b> as a fraction.", fr(9, 100), [fr(9, 10), fr(9, 1000), fr(1, 9)],
                   "9%% = 9 out of 100 = <b>%s</b>. %s would be 90%%." % (fr(9, 100), fr(9, 10))))
    its.append(mcq("Write %s as a percentage." % fr(71, 100), "71%", ["7.1%", "0.71%", "29%"],
                   "%s means 71 out of 100, so it is <b>71%%</b>." % fr(71, 100)))
    its.append(mcq("Write %s as a percentage." % fr(3, 10), "30%", ["3%", "0.3%", "70%"],
                   "Make the denominator 100: %s = %s = <b>30%%</b>. 3%% would be %s." % (fr(3, 10), fr(30, 100), fr(3, 100))))
    its.append(mcq("Write <b>45%</b> as a decimal.", "0.45", ["4.5", "0.045", "45"],
                   "45%% = %s = 45 hundredths = <b>0.45</b>." % fr(45, 100)))
    its.append(mcq("Write <b>6%</b> as a decimal.", "0.06", ["0.6", "6", "0.006"],
                   "6%% = %s = 6 hundredths. Hundredths are the second place after the point: <b>0.06</b>. 0.6 is 60%%."
                   % fr(6, 100)))
    its.append(mcq("Write <b>90%</b> as a decimal.", "0.9", ["0.09", "9", "0.009"],
                   "90%% = %s = %s = <b>0.9</b>. 0.09 is only 9%%." % (fr(90, 100), fr(9, 10))))
    its.append(mcq("Write <b>0.4</b> as a percentage.", "40%", ["4%", "0.4%", "400%"],
                   "0.4 = 4 tenths = 40 hundredths = %s = <b>40%%</b>. 4%% would be 0.04." % fr(40, 100)))
    its.append(mcq("Write <b>0.83</b> as a percentage.", "83%", ["8.3%", "0.83%", "830%"],
                   "0.83 = 83 hundredths = %s = <b>83%%</b>." % fr(83, 100)))
    its.append(mcq("Write <b>0.05</b> as a percentage.", "5%", ["50%", "0.5%", "0.05%"],
                   "0.05 = 5 hundredths = %s = <b>5%%</b>. 50%% would be 0.5." % fr(5, 100)))
    its.append(mcq("<b>100%</b> of something is …", "the whole amount", ["100 wholes", "one tenth of it", "one hundredth of it"],
                   "100%% = %s = 1. So 100%% is <b>the whole amount</b>. 1%% is one hundredth of it." % fr(100, 100)))
    its.append(mcq("64% of the pupils in a school have a pet. What percentage do <b>not</b> have a pet?", "36%",
                   ["46%", "64%", "0.36%"],
                   "All the pupils are 100%. 100% − 64% = <b>36%</b>. Check: 64 + 36 = 100."))
    its.append(mcq("Which of these is <b>not</b> equal to %s?" % fr(7, 10), "7%", ["0.7", "70%", fr(70, 100)],
                   "%s = %s = 0.7 = 70%%. <b>7%%</b> is %s, which is much smaller." % (fr(7, 10), fr(70, 100), fr(7, 100)),
                   same_ok=True))
    its.append(mcq("Which is the <b>greatest</b>?", "0.5", ["48%", "0.45", "5%"],
                   "Write them all as hundredths: 0.5 = 50%, 48%, 0.45 = 45%, 5%. The greatest is <b>0.5</b>."))
    order = [5, 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 12, 15, 16, 17, 18, 19]
    return {"title": "Per cent: parts per hundred, fractions and decimals", "items": reorder(its, order)}


# ============================================================ set 5: equivalents and problems
def set_problems(P):
    its = []
    for (n, d), right, wrong, e in [
        ((1, 2), "50%", ["12%", "2%", "20%"],
         "%s = %s = <b>50%%</b>. Do not just write the digits 1 and 2." % (fr(1, 2), fr(50, 100))),
        ((1, 5), "20%", ["15%", "5%", "50%"],
         "5 × 20 = 100, so %s = %s = <b>20%%</b>. 15%% writes the digits, and 50%% confuses %s with %s." % (fr(1, 5), fr(20, 100), fr(1, 5), fr(1, 2))),
        ((4, 5), "80%", ["45%", "40%", "20%"],
         "%s = 20%%, so %s = 4 × 20%% = <b>80%%</b>. 20%% is the part that is left." % (fr(1, 5), fr(4, 5))),
        ((3, 25), "12%", ["75%", "28%", "3%"],
         "25 × 4 = 100, so %s = %s = <b>12%%</b>. 75%% comes from 3 × 25." % (fr(3, 25), fr(12, 100))),
        ((13, 20), "65%", ["13%", "33%", "0.65%"],
         "20 × 5 = 100, so %s = %s = <b>65%%</b>. Multiply the numerator by 5 too." % (fr(13, 20), fr(65, 100))),
    ]:
        assert F(right.rstrip("%")) / 100 == F(n, d)
        its.append(mcq("Write %s as a percentage." % fr(n, d), right, wrong, e))
    for (n, d), right, wrong, e in [
        ((1, 4), "0.25", ["0.4", "0.14", "1.4"],
         "%s = %s = <b>0.25</b>. 0.4 uses the 4 from the denominator." % (fr(1, 4), fr(25, 100))),
        ((2, 5), "0.4", ["0.25", "2.5", "0.2"],
         "%s = %s = <b>0.4</b>. 0.2 is only %s." % (fr(2, 5), fr(4, 10), fr(1, 5))),
        ((7, 50), "0.14", ["0.07", "0.7", "0.057"],
         "50 × 2 = 100, so %s = %s = <b>0.14</b>. 0.07 forgets to double the numerator." % (fr(7, 50), fr(14, 100))),
    ]:
        assert F(Dm(right)) == F(n, d)
        its.append(mcq("Write %s as a decimal." % fr(n, d), right, wrong, e))
    n, he, his = P.next()
    its.append(mcq("%s scores 18 out of 25 in a spelling test. What percentage does %s score?" % (n, he), "72%",
                   ["18%", "7%", "43%"],
                   "25 × 4 = 100, so %s = %s = <b>72%%</b>. 7%% uses the 7 marks %s got wrong." % (fr(18, 25), fr(72, 100), he)))
    its.append(mcq("Which is greater: %s or 55%%?" % fr(3, 5), fr(3, 5), ["55%", "They are equal", "You can’t tell"],
                   "%s = %s = 60%%. 60%% &gt; 55%%, so <b>%s</b> is greater." % (fr(3, 5), fr(60, 100), fr(3, 5)), same_ok=True))
    its.append(mcq("Which is smaller: %s or 0.15?" % fr(1, 5), "0.15", [fr(1, 5), "They are equal", "You can’t tell"],
                   "%s = %s = 0.2 = 0.20. 0.15 &lt; 0.20, so <b>0.15</b> is smaller. %s is not 0.15." % (fr(1, 5), fr(2, 10), fr(1, 5)),
                   same_ok=True))
    its.append(mcq("A pencil costs 45p. What percentage of £1 is that?", "45%", ["4.5%", "0.45%", "55%"],
                   "£1 = 100p. 45p out of 100p = %s = <b>45%%</b>." % fr(45, 100)))
    its.append(mcq("40% of the pupils in a class are boys. What fraction of the class are girls?", fr(3, 5),
                   [fr(2, 5), fr(3, 50), fr(1, 60)],
                   "100%% − 40%% = 60%% are girls. 60%% = %s = <b>%s</b>. %s is the boys." % (fr(60, 100), fr(3, 5), fr(2, 5))))
    its.append(mcq("A jumper is %s off in one shop and 25%% off in another shop. Which shop takes off more?" % fr(1, 5),
                   "the 25% off shop", ["the %s off shop" % fr(1, 5), "They take off the same", "You can’t tell"],
                   "%s = 20%%, and 25%% &gt; 20%%. So <b>the 25%% off shop</b> takes off more." % fr(1, 5), same_ok=True))
    n, he, his = P.next()
    its.append(mcq("A jug holds 1 litre. %s pours 0.6 litres of water into it. What percentage of the jug is full?" % n,
                   "60%", ["6%", "40%", "0.6%"],
                   "0.6 = %s = %s = <b>60%%</b>. 40%% is the empty part." % (fr(6, 10), fr(60, 100))))
    a, _, ah = P.next()
    b, _, bh = P.next()
    its.append(mcq("%s has done 0.8 of %s homework. %s has done 75%% of %s homework. Who has done more?" % (a, ah, b, bh),
                   a, [b, "They have done the same", "You can’t tell"],
                   "0.8 = 80%%. 80%% &gt; 75%%, so <b>%s</b> has done more." % a, same_ok=True))
    its.append(mcq("There are 50 pupils in Year 5. 19 of them have school dinners. What percentage have school dinners?",
                   "38%", ["19%", "31%", "62%"],
                   "50 × 2 = 100, so %s = %s = <b>38%%</b>. 62%% is the pupils who do not have school dinners."
                   % (fr(19, 50), fr(38, 100))))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("In a maths test out of 25, %s scores 22. %s scores 90%%. Who has the higher score?" % (a, b),
                   b, [a, "They are the same", "You can’t tell"],
                   "%s = %s = 88%%. 90%% &gt; 88%%, so <b>%s</b> has the higher score." % (fr(22, 25), fr(88, 100), b),
                   same_ok=True))
    right = "0.55, 58%, " + fr(3, 5)
    its.append(mcq("Order from <b>smallest to greatest</b>:<br><b>%s, 0.55, 58%%</b>" % fr(3, 5), right,
                   [", ".join(w) for w in [[fr(3, 5), "0.55", "58%"], ["0.55", fr(3, 5), "58%"], ["58%", "0.55", fr(3, 5)]]],
                   "As hundredths: %s = 0.60, 0.55 and 58%% = 0.58. So <b>0.55, 58%%, %s</b>." % (fr(3, 5), fr(3, 5)),
                   same_ok=True))
    assert F(55, 100) < F(58, 100) < F(3, 5)
    n, he, his = P.next()
    its.append(mcq("%s’s tablet battery has 0.35 of a full charge left. What percentage is that?" % n, "35%", ["3.5%", "0.35%", "65%"],
                   "0.35 = 35 hundredths = %s = <b>35%%</b>. 65%% of the charge has been used." % fr(35, 100)))
    order = [0, 5, 1, 6, 2, 8, 3, 4, 7, 9, 11, 10, 19, 12, 13, 14, 15, 16, 17, 18]
    return {"title": "Equivalents and percentage problems", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg(["2.738"], hi=(0, -3))
    f_round = line_svg(3400, 3500, 10, 3470, [3400, 3450, 3500])
    f_grid = grid_svg(37, cell=22)
    return (
        "<h2>Decimals as fractions</h2>"
        "<p>The number of decimal places tells you the denominator. One place is <b>tenths</b>, two places are "
        "<b>hundredths</b>, three places are <b>thousandths</b>.</p>"
        + table(["Decimal", "Fraction", "Said as"], [
            ["0.7", fr(7, 10), "7 tenths"],
            ["0.71", fr(71, 100), "71 hundredths"],
            ["0.007", fr(7, 1000), "7 thousandths"],
            ["0.453", fr(453, 1000), "453 thousandths"],
        ]) +
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>In 2.738 the 8 is in the thousandths place, so it is worth 8 thousandths = 0.008. "
        "1 hundredth = 10 thousandths.</figcaption></figure>"
        "<h2>Comparing and ordering</h2>"
        "<p>Give the numbers the <b>same number of decimal places</b> by adding zeros at the end. Then compare the digits "
        "from the left: ones, tenths, hundredths, thousandths.</p>"
        + ex("Example", "Order 0.5, 0.45 and 0.405 from smallest to greatest.",
             "Write 0.500, 0.450 and 0.405. Compare 500, 450 and 405 thousandths.", "0.405, 0.45, 0.5")
        + "<h2>Rounding decimals</h2>"
        "<p>To the nearest <b>whole number</b>, look at the tenths digit. To <b>1 decimal place</b>, look at the hundredths digit. "
        "5 or more: round up. 4 or less: round down.</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>3.47 is past the halfway mark (3.45), so it rounds to 3.5 to 1 decimal place.</figcaption></figure>"
        + ex("Example", "Round 5.96 to 1 decimal place.",
             "The hundredths digit is 6, so round up. 9 tenths + 1 tenth = 10 tenths = 1 whole.", "6.0")
        + "<h2>Per cent</h2>"
        "<p>Per cent (%) means <b>parts per hundred</b>. 37% = " + fr(37, 100) + " = 0.37.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>37 of 100 squares are shaded: " + fr(37, 100) + " = 0.37 = 37%.</figcaption></figure>"
        "<p>To change a fraction into a percentage, make the denominator 100 first.</p>"
        + table(["Fraction", "Hundredths", "Decimal", "Percentage"], [
            [fr(1, 2), fr(50, 100), "0.5", "50%"],
            [fr(1, 4), fr(25, 100), "0.25", "25%"],
            [fr(1, 5), fr(20, 100), "0.2", "20%"],
            [fr(2, 5), fr(40, 100), "0.4", "40%"],
            [fr(4, 5), fr(80, 100), "0.8", "80%"],
            [fr(3, 10), fr(30, 100), "0.3", "30%"],
        ])
        + ex("Test score", "Freya scores 18 out of 25. What percentage is that?",
             "25 × 4 = 100, so multiply the top by 4 too: " + fr(18, 25) + " = " + fr(72, 100) + ".", "72%")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because it is longer", "Use the same places: 0.45 &lt; 0.50"],
            ["0.007 = " + fr(7, 100), "Three places means thousandths: " + fr(7, 1000)],
            ["Rounding 3.45 to 3.4", "Halfway rounds up: 3.5"],
            [fr(1, 5) + " = 15% or 0.5", fr(1, 5) + " = " + fr(20, 100) + " = 0.2 = 20%"],
            ["0.4 = 4%", "0.4 = 0.40 = 40%"],
        ])
    )


FAQ = [
    {"q": "What do children learn about decimals and percentages in Year 5?",
     "a": "In Year 5 children write decimals as fractions (0.71 = 71/100), learn thousandths, compare and order numbers with up to three decimal places, round decimals to the nearest whole number and to one decimal place, and learn that per cent means parts per hundred."},
    {"q": "How do you explain thousandths to a child?",
     "a": "Split 1 hundredth into 10 equal parts: each part is 1 thousandth, written 0.001. Thousandths are the third place after the decimal point, so 0.007 = 7/1000."},
    {"q": "How do you compare decimals with different numbers of digits?",
     "a": "Add zeros at the end so they have the same number of decimal places, then compare from the left. 0.5 = 0.500 and 0.45 = 0.450, so 0.5 is greater even though 0.45 has more digits."},
    {"q": "Which fraction, decimal and percentage facts should Year 5 know?",
     "a": "1/2 = 0.5 = 50%, 1/4 = 0.25 = 25%, 1/5 = 0.2 = 20%, 2/5 = 0.4 = 40% and 4/5 = 0.8 = 80%. For tenths, twentieths, twenty-fifths and fiftieths, make the denominator 100 to find the percentage."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred squares, number lines, place value charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(5512)
    P = People(rnd)
    sets = [set_fractions(), set_compare(), set_round(), set_percent(), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "decimals-and-percentages", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals and Percentages",
        "seo_title": "Year 5 Decimals and Percentages Worksheets: Thousandths, Rounding and Per Cent",
        "short_title": "Decimals and percentages",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 5: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Read and write decimal numbers as fractions [for example, 0.71 = 71/100]; recognise and use thousandths and relate them to tenths, hundredths and decimal equivalents; round decimals with two decimal places to the nearest whole number and to one decimal place; read, write, order and compare numbers with up to three decimal places; recognise the per cent symbol (%) and understand that per cent relates to ‘number of parts per hundred’, and write percentages as a fraction with denominator 100, and as a decimal; solve problems which require knowing percentage and decimal equivalents of 1/2, 1/4, 1/5, 2/5, 4/5 and those fractions with a denominator of a multiple of 10 or 25.",
        "meta_desc": "Free Year 5 decimals and percentages worksheets for the National Curriculum: decimals as fractions, thousandths, comparing and ordering up to three decimal places, rounding to the nearest whole number and 1 decimal place, and per cent as parts per hundred. 100 maths questions with an answer key.",
        "key_big": "Per cent means parts per hundred: 37% = 37/100 = 0.37. Three decimal places are thousandths: 0.007 = 7/1000.",
        "key_sub": "Compare decimals by giving them the same number of places: 0.5 = 0.500 > 0.45. Round with the next digit: 3.45 rounds up to 3.5. Know 1/2 = 50%, 1/4 = 25%, 1/5 = 20%, 2/5 = 40%, 4/5 = 80%.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred square|number line|place value chart)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
