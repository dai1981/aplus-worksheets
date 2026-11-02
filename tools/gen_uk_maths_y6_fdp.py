# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Fractions, decimals and percentages
(National Curriculum in England, Year 6: Fractions (including decimals and percentages))
  python3 tools/gen_uk_maths_y6_fdp.py
A fraction is a division: 3/8 = 3 ÷ 8 = 0.375 (short division, "bus stop" layout, drawn from the real working).
Place value to three decimal places; simple fraction / decimal / percentage equivalences; comparing mixed forms.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
British English, pounds and pence, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
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


def short_div(a, b, places, hide=False):
    """Short division ('bus stop') of a ÷ b, written to `places` decimal places, drawn from the real working.
    Remainders are carried as small red digits. hide=True draws the answer digits after the point as boxes."""
    w = str(a)
    cells = list(w) + ["."] + ["0"] * places
    q, carry, rem = [], {}, 0
    for i, ch in enumerate(cells):
        if ch == ".":
            q.append(".")
            continue
        cur = rem * 10 + int(ch)
        q.append(str(cur // b))
        rem = cur % b
        nxt = i + 1 if i + 1 < len(cells) and cells[i + 1] != "." else i + 2
        if rem and nxt < len(cells):
            carry[nxt] = str(rem)
    assert rem == 0, (a, b)
    qs = "".join(q)
    assert F(Dm(qs)) == F(a, b), (qs, a, b)
    # drop leading zeros of the whole-number part except the last one
    lead = 0
    while lead < len(w) - 1 and q[lead] == "0":
        lead += 1
    CW, DW = 30, 14
    xs, x = [], 62
    for ch in cells:
        xs.append(x)
        x += DW if ch == "." else CW
    W = x + 10
    ytop, ybar, ydig = 34, 46, 78
    o = []
    for i, ch in enumerate(cells):
        cx = xs[i] + (DW if ch == "." else CW) / 2.0
        if ch == ".":
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ydig - 2, LINE))
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ytop - 2, LINE))
            continue
        o.append(text(cx + 3, ydig, ch, 26))
        if i in carry:
            o.append(text(xs[i] + 5, ydig - 14, carry[i], 15, col=RED))
        if i < lead:
            continue
        after = i > len(w)
        if hide and after:
            o.append("<rect x='%.1f' y='%d' width='20' height='24' fill='#fff' stroke='%s' stroke-width='1.8' rx='3'/>"
                     % (cx - 10, ytop - 22, LINE))
        else:
            o.append(text(cx + 3, ytop, q[i], 26))
    o.append("<line x1='54' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (ybar, W - 6, ybar, LINE))
    o.append("<path d='M 54 %d Q 62 %d 54 %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (ybar, ybar + 22, ybar + 44, LINE))
    o.append(text(30, ydig, str(b), 26))
    label = "short division of %s by %d" % ("".join(cells), b)
    return svg_wrap(W, ybar + 50, "".join(o), label)


def line_svg(parts, dot, labels, W=400):
    """Number line from 0 to 1 with `parts` equal spaces, red dot at tick `dot`. labels: {tick: text}."""
    L, R, Y = 26, W - 26, 30

    def X(i):
        return L + (R - L) * i / float(parts)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(parts + 1):
        big = i in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if big else 9), X(i), Y + (13 if big else 9), LINE, "2.5" if big else "1.8"))
    for i, t in labels.items():
        s.append(text(X(i), Y + 36, t, 17))
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from 0 to 1 split into %d equal parts" % parts)


# ============================================================ set 1: place value to three decimal places
def set_place_value():
    its = []
    for num, k, wrong in [("4.073", "7", ["7 tenths", "7 thousandths", "7 ones"]),
                          ("2.508", "8", ["8 hundredths", "8 tenths", "8 ones"]),
                          ("13.264", "2", ["2 hundredths", "2 ones", "2 tens"]),
                          ("0.719", "9", ["9 hundredths", "9 tenths", "9 ones"])]:
        p = digit_place(num, k)
        right = "%s %s" % (k, PLACE[p])
        n = len(num.partition(".")[0])
        e = ("The red %s is in the <b>%s</b> column, the %s place after the decimal point. Its value is <b>%s</b> = %s."
             % (k, PLACE[p], ["first", "second", "third"][-p - 1], right, dec(place_value(num, k))))
        if p == -3:
            e += " Thousandths are the <b>third</b> place, not the second."
        its.append(mcq(fig(chart_svg([num], hi=(0, p))) + "What is the value of the red digit in %s?" % num,
                       right, wrong, e))

    for num, k in [("3.456", "6"), ("5.638", "3"), ("9.104", "4"), ("12.875", "8")]:
        v = place_value(num, k)
        p = digit_place(num, k)
        cands = [F(int(k)) * F(10) ** j for j in (-1, -2, -3, 0)]
        wrong = [dec(c) for c in cands if c != v][:3]
        e = ("In %s the %s is in the <b>%s</b> place (%s after the decimal point). So its value is %s %s = <b>%s</b>."
             % (num, k, PLACE[p], ["1st", "2nd", "3rd"][-p - 1], k, PLACE[p], dec(v)))
        its.append(mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (k, num), dec(v), wrong, e))

    its.append(mcq("Write <b>3 ones, 4 tenths and 6 thousandths</b> as a decimal.", "3.406", ["3.46", "3.0406", "3.604"],
                   "There are 0 hundredths, so write a 0 to hold the hundredths place: 3 . 4 0 6 = <b>3.406</b>. "
                   "3.46 would be 6 hundredths."))
    its.append(mcq("4 + 0.3 + 0.008 = ?", "4.308", ["4.38", "4.3008", "4.803"],
                   "4 ones, 3 tenths, 0 hundredths and 8 thousandths: <b>4.308</b>. The 0 holds the hundredths place."))
    its.append(mcq("Write %s as a decimal." % fr(7, 1000), "0.007", ["0.7", "0.07", "0.0007"],
                   "%s is 7 thousandths. Thousandths are the <b>third</b> place after the point, so write 0s in the tenths and "
                   "hundredths places: <b>0.007</b>." % fr(7, 1000)))
    its.append(mcq("Write %s as a decimal." % fr(45, 1000), "0.045", ["0.45", "4.5", "0.0045"],
                   "45 thousandths = 4 hundredths and 5 thousandths. The last digit must be in the third place: <b>0.045</b>. "
                   "0.45 would be 45 hundredths."))
    its.append(mcq("Which fraction is equal to <b>0.239</b>?", fr(239, 1000), [fr(239, 100), fr(239, 10), fr(23, 9)],
                   "0.239 has three decimal places, so the last digit is in the thousandths place: 239 thousandths = <b>%s</b>."
                   % fr(239, 1000)))
    its.append(mcq("6.254 = 6 + 0.2 + ? + 0.004", "0.05", ["5", "0.5", "0.005"],
                   "The 5 is in the hundredths place, so it is worth 5 hundredths = <b>0.05</b>. "
                   "Check: 6 + 0.2 + 0.05 + 0.004 = 6.254."))
    its.append(mcq("In which number is the digit 5 worth <b>5 thousandths</b>?", "2.305", ["2.053", "2.530", "5.023"],
                   "Thousandths are the third place after the decimal point. Only <b>2.305</b> has the 5 there. "
                   "In 2.053 the 5 is worth 5 hundredths."))
    its.append(mcq("How many thousandths are there in <b>0.1</b>?", "100", ["10", "1,000", "1"],
                   "1 tenth = 10 hundredths = <b>100</b> thousandths. 0.1 = 0.100."))
    its.append(mcq("What number is <b>1 thousandth more</b> than 2.399?", "2.4", ["2.3910", "2.409", "2.499"],
                   "9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. That makes 10 hundredths = 1 tenth. "
                   "So 2.399 + 0.001 = 2.400 = <b>2.4</b>. 2.409 adds 1 hundredth, not 1 thousandth."))
    its.append(mcq("Which number is equal to <b>2.07</b>?", "2.070", ["2.7", "2.007", "2.0007"],
                   "A 0 at the <b>end</b> of a decimal does not change its value: 2.07 = <b>2.070</b>. "
                   "A 0 in the middle does: 2.7 and 2.007 are different numbers."))
    its.append(mcq("Which digit is in the <b>thousandths</b> place in 5.162?", "2", ["6", "1", "5"],
                   "Tenths, hundredths, thousandths: 5 . 1 6 <b>2</b>. The third digit after the point is <b>2</b>. "
                   "6 is in the hundredths place."))
    its.append(mcq("47 ÷ 1,000 = ?", "0.047", ["0.47", "4.7", "0.0047"],
                   "Dividing by 1,000 moves every digit <b>3 places</b> to the right. The 7 lands in the thousandths place: "
                   "<b>0.047</b>. 0.47 is 47 ÷ 100."))
    assert len(its) == 20, len(its)
    return {"title": "Place value to three decimal places", "items": its}


# ============================================================ set 2: fractions as division
def set_division():
    its = []
    its.append(mcq("Which calculation is the same as %s?" % fr(3, 8), "3 ÷ 8", ["8 ÷ 3", "3 × 8", "8 − 3"],
                   "A fraction is a division: the numerator is divided by the denominator. %s = <b>3 ÷ 8</b>." % fr(3, 8)))
    its.append(mcq("3 pizzas are shared equally between 4 children. How much pizza does each child get?",
                   fr(3, 4) + " of a pizza", [fr(4, 3) + " of a pizza", fr(1, 4) + " of a pizza", fr(1, 3) + " of a pizza"],
                   "3 shared between 4 is 3 ÷ 4 = <b>%s</b>. Each pizza gives every child %s, and there are 3 pizzas."
                   % (fr(3, 4), fr(1, 4))))
    its.append(mcq("Write %s as a decimal." % fr(1, 8), "0.125", ["0.18", "1.8", "0.12"],
                   "1 ÷ 8: write 1 as 1.000. 10 ÷ 8 = 1 r 2, 20 ÷ 8 = 2 r 4, 40 ÷ 8 = 5. So %s = <b>0.125</b>. "
                   "Do not just write the digits 1 and 8 after the point." % fr(1, 8)))
    its.append(mcq(fig(short_div(3, 8, 3, hide=True)) + "The short division shows 3 ÷ 8. What is %s as a decimal?" % fr(3, 8),
                   "0.375", ["0.38", "3.8", "0.83"],
                   "30 ÷ 8 = 3 r 6, 60 ÷ 8 = 7 r 4, 40 ÷ 8 = 5. So 3 ÷ 8 = <b>0.375</b>. "
                   "0.38 and 3.8 just use the digits of the fraction."))
    its.append(mcq(fig(short_div(5, 8, 3, hide=True)) + "The short division shows 5 ÷ 8. What is %s as a decimal?" % fr(5, 8),
                   "0.625", ["0.58", "5.8", "1.6"],
                   "50 ÷ 8 = 6 r 2, 20 ÷ 8 = 2 r 4, 40 ÷ 8 = 5. So 5 ÷ 8 = <b>0.625</b>. "
                   "1.6 is 8 ÷ 5: the division is the wrong way round."))
    its.append(mcq("Write %s as a decimal." % fr(7, 8), "0.875", ["0.78", "7.8", "0.87"],
                   "7 ÷ 8: 70 ÷ 8 = 8 r 6, 60 ÷ 8 = 7 r 4, 40 ÷ 8 = 5. So %s = <b>0.875</b>. "
                   "Keep dividing until there is no remainder: 0.87 stops too soon." % fr(7, 8)))
    its.append(mcq("Write %s as a decimal." % fr(1, 5), "0.2", ["0.5", "0.15", "5"],
                   "%s = %s, so %s = <b>0.2</b>. (Or 1 ÷ 5: 10 ÷ 5 = 2 tenths.) 5 is 5 ÷ 1, the wrong way round."
                   % (fr(1, 5), fr(2, 10), fr(1, 5))))
    its.append(mcq("Write %s as a decimal." % fr(3, 5), "0.6", ["0.35", "3.5", "0.53"],
                   "%s = %s (multiply the top and bottom by 2). So %s = <b>0.6</b>." % (fr(3, 5), fr(6, 10), fr(3, 5))))
    its.append(mcq("Write %s as a decimal." % fr(2, 25), "0.08", ["0.8", "0.225", "2.25"],
                   "25 × 4 = 100, so %s = %s = 8 hundredths = <b>0.08</b>. 0.8 would be 8 tenths."
                   % (fr(2, 25), fr(8, 100))))
    its.append(mcq("Write %s as a decimal." % fr(7, 20), "0.35", ["0.72", "0.7", "3.5"],
                   "20 × 5 = 100, so %s = %s = <b>0.35</b>. Multiply the numerator by 5 too, not just the denominator."
                   % (fr(7, 20), fr(35, 100))))
    its.append(mcq("Write %s as a decimal." % fr(9, 40), "0.225", ["0.94", "0.9", "2.25"],
                   "40 × 25 = 1,000, so %s = %s = <b>0.225</b>. (Or 9 ÷ 40: 9 ÷ 4 = 2.25, then ÷ 10 = 0.225.)"
                   % (fr(9, 40), fr(225, 1000))))
    its.append(mcq("Write %s as a decimal." % fr(6, 8), "0.75", ["0.68", "6.8", "0.86"],
                   "Simplify first: %s = %s. %s = %s = <b>0.75</b>." % (fr(6, 8), fr(3, 4), fr(3, 4), fr(75, 100))))
    its.append(mcq("Write %s as a decimal, rounded to 3 decimal places." % fr(1, 3), "0.333", ["0.13", "1.3", "3"],
                   "1 ÷ 3 = 0.3333… The 3s go on for ever. To 3 decimal places, %s = <b>0.333</b>. "
                   "3 is 3 ÷ 1, the wrong way round." % fr(1, 3)))
    its.append(mcq("Write %s as a decimal, rounded to 3 decimal places." % fr(2, 3), "0.667", ["0.666", "0.23", "1.5"],
                   "2 ÷ 3 = 0.6666… The 4th decimal place is 6, which is 5 or more, so round up: <b>0.667</b>. "
                   "0.666 cuts the digits off without rounding."))
    its.append(mcq("Write %s as a decimal." % fr(7, 4), "1.75", ["7.4", "1.3", "0.75"],
                   "7 ÷ 4 = 1 r 3. The remainder 3 still has to be divided by 4: %s = 0.75. So %s = <b>1.75</b>. "
                   "1.3 writes the remainder as a decimal digit." % (fr(3, 4), fr(7, 4))))
    its.append(mcq("13 ÷ 5 = ?", "2.6", ["2.3", "2.03", "13.5"],
                   "13 ÷ 5 = 2 r 3, and 3 ÷ 5 = %s = 0.6. So 13 ÷ 5 = 2 %s = <b>2.6</b>. "
                   "The remainder 3 is not 0.3." % (fr(3, 5), fr(3, 5))))
    its.append(mcq("Write %s as a decimal." % mixed(2, 3, 8), "2.375", ["2.38", "23.8", "2.83"],
                   "The 2 ones stay the same. %s = 3 ÷ 8 = 0.375. So %s = <b>2.375</b>." % (fr(3, 8), mixed(2, 3, 8))))
    its.append(mcq("Which fraction is equal to <b>0.125</b>?", fr(1, 8), [fr(125, 100), fr(1, 125), fr(12, 5)],
                   "0.125 = %s. Divide the top and bottom by 125: <b>%s</b>. %s would be 1.25."
                   % (fr(125, 1000), fr(1, 8), fr(125, 100))))
    its.append(mcq("Which fraction is equal to <b>4 ÷ 9</b>?", fr(4, 9), [fr(9, 4), fr(1, 36), fr(4, 36)],
                   "Divide 4 into 9 equal parts: each part is %s. So 4 ÷ 9 = <b>%s</b>. %s is 9 ÷ 4." % (fr(4, 9), fr(4, 9), fr(9, 4))))
    its.append(mcq("Which division has the answer <b>0.4</b>?", "2 ÷ 5", ["5 ÷ 2", "4 ÷ 100", "1 ÷ 4"],
                   "2 ÷ 5 = %s = %s = <b>0.4</b>. 5 ÷ 2 = 2.5, 4 ÷ 100 = 0.04 and 1 ÷ 4 = 0.25."
                   % (fr(2, 5), fr(4, 10))))
    # order: easy (what division means) -> harder
    order = [0, 1, 18, 6, 7, 2, 3, 4, 5, 11, 8, 9, 19, 14, 15, 16, 17, 10, 12, 13]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Fractions as division: 3/8 = 3 ÷ 8", "items": its}


# ============================================================ set 3: equivalences
def set_equivalents():
    its = []
    its.append(mcq(fig(grid_svg(20)) + "What percentage of the hundred square is shaded?", "20%", ["2%", "80%", "0.2%"],
                   "20 of the 100 squares are shaded. Per cent means <b>out of 100</b>, so it is <b>20%%</b>. "
                   "This is also %s = 0.2." % fr(1, 5)))
    its.append(mcq(fig(grid_svg(35)) + "Which shows the shaded part as a decimal and a percentage?",
                   "0.35 and 35%", ["3.5 and 35%", "0.35 and 3.5%", "0.65 and 65%"],
                   "35 of 100 squares: %s = <b>0.35</b> = <b>35%%</b>. 0.65 and 65%% describe the white part." % fr(35, 100)))
    its.append(mcq(fig(grid_svg(4)) + "What percentage of the hundred square is <b>not</b> shaded?", "96%",
                   ["4%", "6%", "0.96%"],
                   "4 squares are shaded, so 100 − 4 = 96 squares are white. 96 out of 100 = <b>96%</b>."))
    for (n, d), right, wrong, e in [
        ((1, 5), "20%", ["15%", "5%", "50%"],
         "%s = %s = 20%%. (1 ÷ 5 = 0.2.) 15%% just writes the digits 1 and 5." % (fr(1, 5), fr(20, 100))),
        ((3, 4), "75%", ["34%", "25%", "43%"],
         "%s = %s = 75%%. 25%% is only %s." % (fr(3, 4), fr(75, 100), fr(1, 4))),
        ((1, 4), "25%", ["14%", "4%", "40%"],
         "%s = %s = 25%%. 4%% and 40%% use the 4 from the denominator." % (fr(1, 4), fr(25, 100))),
        ((1, 10), "10%", ["1%", "0.1%", "100%"],
         "%s = %s = 10%%. 1%% is %s." % (fr(1, 10), fr(10, 100), fr(1, 100))),
        ((3, 20), "15%", ["32%", "3%", "60%"],
         "20 × 5 = 100, so %s = %s = 15%%. 60%% comes from 3 × 20." % (fr(3, 20), fr(15, 100))),
        ((9, 25), "36%", ["34%", "9.25%", "0.36%"],
         "25 × 4 = 100, so %s = %s = 36%%. 34%% adds 9 and 25." % (fr(9, 25), fr(36, 100))),
        ((1, 8), "12.5%", ["18%", "8%", "1.25%"],
         "%s = 1 ÷ 8 = 0.125. Multiply by 100: 0.125 × 100 = 12.5%%." % fr(1, 8)),
    ]:
        assert F(right.rstrip("%")) / 100 == F(n, d)
        e = e.replace(right, "<b>%s</b>" % right, 1) if right in e else e
        its.append(mcq("Write %s as a percentage." % fr(n, d), right, wrong, e))
    for d_, right, wrong, e in [
        ("0.4", "40%", ["4%", "0.4%", "400%"],
         "0.4 = 4 tenths = 40 hundredths = <b>40%</b>. To change a decimal to a percentage, multiply by 100: 0.4 × 100 = 40."),
        ("0.07", "7%", ["70%", "0.07%", "0.7%"],
         "0.07 = 7 hundredths = <b>7%</b>. 70% would be 0.7."),
        ("0.375", "37.5%", ["375%", "3.75%", "0.375%"],
         "Multiply by 100: the digits move 2 places to the left. 0.375 × 100 = 37.5, so 0.375 = <b>37.5%</b>."),
        ("1.2", "120%", ["12%", "1.2%", "0.12%"],
         "1.2 × 100 = 120, so 1.2 = <b>120%</b>. A number bigger than 1 is more than 100%."),
    ]:
        assert F(Dm(d_)) * 100 == F(right.rstrip("%"))
        its.append(mcq("Write <b>%s</b> as a percentage." % d_, right, wrong, e))
    for p_, right, wrong, e in [
        ("45%", "0.45", ["4.5", "0.045", "45"],
         "45% = 45 hundredths = <b>0.45</b>. Divide by 100: the digits move 2 places to the right."),
        ("8%", "0.08", ["0.8", "8", "0.008"],
         "8% = 8 hundredths. Hundredths are the second place after the point: <b>0.08</b>. 0.8 is 80%."),
    ]:
        its.append(mcq("Write <b>%s</b> as a decimal." % p_, right, wrong, e))
    its.append(mcq("Write %s as a decimal." % fr(2, 5), "0.4", ["0.25", "2.5", "0.2"],
                   "%s = %s = <b>0.4</b>. 0.25 just writes the digits, 2.5 is 5 ÷ 2, and 0.2 is only %s."
                   % (fr(2, 5), fr(4, 10), fr(1, 5))))
    its.append(mcq("Write <b>60%</b> as a fraction in its simplest form.", fr(3, 5), [fr(1, 6), fr(3, 50), fr(1, 60)],
                   "60%% = %s = %s. Divide the top and bottom by 2: <b>%s</b>. %s is 6%%."
                   % (fr(60, 100), fr(6, 10), fr(3, 5), fr(3, 50))))
    its.append(mcq("Write <b>5%</b> as a fraction in its simplest form.", fr(1, 20), [fr(1, 5), fr(5, 10), fr(1, 50)],
                   "5%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 20%%, not 5%%."
                   % (fr(5, 100), fr(1, 20), fr(1, 5))))
    its.append(mcq("Which of these is <b>not</b> equal to %s?" % fr(3, 4), "0.34", ["0.75", "75%", fr(6, 8)],
                   "%s = 0.75 = 75%% = %s. <b>0.34</b> just writes the digits 3 and 4, so it is not equal." % (fr(3, 4), fr(6, 8)),
                   same_ok=True))
    order = [0, 1, 3, 5, 4, 6, 10, 11, 14, 15, 16, 2, 19, 7, 8, 17, 18, 9, 12, 13]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Equivalent fractions, decimals and percentages", "items": its}


# ============================================================ set 4: compare and order
def cmp_item(x, xv, y, yv, e):
    """x, y are HTML; xv, yv their values."""
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if xv < yv else gt if xv > yv else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare.", right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.35", F("0.35"), "0.305", F("0.305"),
                        "Write both with 3 decimal places: 0.350 and 0.305. Compare the hundredths: 5 &gt; 0. "
                        "So <b>0.35 &gt; 0.305</b>. More digits does not mean a bigger number."))
    its.append(cmp_item("0.7", F("0.7"), "0.65", F("0.65"),
                        "0.7 = 0.70. Compare the tenths: 7 tenths &gt; 6 tenths. So <b>0.7 &gt; 0.65</b>, even though 65 &gt; 7."))
    its.append(cmp_item("0.09", F("0.09"), "0.1", F("0.1"),
                        "0.1 = 0.10. Compare the tenths: 0 &lt; 1. So <b>0.09 &lt; 0.1</b>."))
    its.append(cmp_item(fr(3, 8), F(3, 8), "0.35", F("0.35"),
                        "Change the fraction to a decimal: %s = 3 ÷ 8 = 0.375. 0.375 &gt; 0.350, so <b>%s &gt; 0.35</b>."
                        % (fr(3, 8), fr(3, 8))))
    its.append(cmp_item("40%", F(2, 5), "0.04", F("0.04"),
                        "40% = 0.40. 0.40 &gt; 0.04, so <b>40% &gt; 0.04</b>. 0.04 is only 4%."))
    its.append(cmp_item(fr(1, 5), F(1, 5), "15%", F(15, 100),
                        "%s = 20%%. 20%% &gt; 15%%, so <b>%s &gt; 15%%</b>." % (fr(1, 5), fr(1, 5))))
    its.append(cmp_item("0.6", F("0.6"), fr(3, 5), F(3, 5),
                        "%s = %s = 0.6. So <b>0.6 = %s</b>." % (fr(3, 5), fr(6, 10), fr(3, 5))))
    its.append(cmp_item(fr(1, 8), F(1, 8), "0.2", F("0.2"),
                        "%s = 0.125 and 0.2 = 0.200. 0.125 &lt; 0.200, so <b>%s &lt; 0.2</b>. "
                        "8 is bigger than 2, but eighths are smaller parts." % (fr(1, 8), fr(1, 8))))
    its.append(cmp_item(fr(2, 3), F(2, 3), "0.66", F("0.66"),
                        "%s = 2 ÷ 3 = 0.666…, which is a little more than 0.66 = 0.660. So <b>%s &gt; 0.66</b>." % (fr(2, 3), fr(2, 3))))

    def order_q(q, vals, asc, wrongs, e):
        s = sorted(vals, key=lambda t: t[1], reverse=not asc)
        right = ", ".join(h for h, _ in s)
        return mcq(q, right, [", ".join(w) for w in wrongs], e, same_ok=True)

    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.35, %s, 37%%</b>" % fr(3, 8),
                       [("0.35", F("0.35")), (fr(3, 8), F(3, 8)), ("37%", F(37, 100))], True,
                       [[fr(3, 8), "0.35", "37%"], ["37%", "0.35", fr(3, 8)], ["0.35", fr(3, 8), "37%"]],
                       "Make them all decimals with 3 places: 0.350, %s = 0.375, 37%% = 0.370. "
                       "So the order is <b>0.35, 37%%, %s</b>." % (fr(3, 8), fr(3, 8))))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.5, 0.45, 0.405, 0.054</b>",
                       [("0.5", F("0.5")), ("0.45", F("0.45")), ("0.405", F("0.405")), ("0.054", F("0.054"))], True,
                       [["0.5", "0.45", "0.405", "0.054"], ["0.054", "0.45", "0.405", "0.5"], ["0.5", "0.054", "0.45", "0.405"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405, 0.054. Compare: 54 &lt; 405 &lt; 450 &lt; 500 thousandths. "
                       "So <b>0.054, 0.405, 0.45, 0.5</b>."))
    its.append(order_q("Order from <b>greatest to smallest</b>:<br><b>0.8, %s, 79%%</b>" % fr(3, 4),
                       [("0.8", F("0.8")), (fr(3, 4), F(3, 4)), ("79%", F(79, 100))], False,
                       [["79%", fr(3, 4), "0.8"], [fr(3, 4), "79%", "0.8"], ["79%", "0.8", fr(3, 4)]],
                       "As decimals: 0.8 = 0.80, %s = 0.75, 79%% = 0.79. Greatest first: <b>0.8, 79%%, %s</b>."
                       % (fr(3, 4), fr(3, 4))))
    its.append(order_q("Which list is in order, <b>smallest first</b>?",
                       [("0.6", F("0.6")), (fr(2, 3), F(2, 3)), ("70%", F(7, 10))], True,
                       [[fr(2, 3), "0.6", "70%"], ["70%", "0.6", fr(2, 3)], ["0.6", "70%", fr(2, 3)]],
                       "0.6 = 0.600, %s = 0.666… and 70%% = 0.700. So <b>0.6, %s, 70%%</b>." % (fr(2, 3), fr(2, 3))))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>1.2, 115%%, %s</b>" % mixed(1, 1, 4),
                       [("1.2", F("1.2")), ("115%", F(115, 100)), (mixed(1, 1, 4), F(5, 4))], True,
                       [["1.2", "115%", mixed(1, 1, 4)], [mixed(1, 1, 4), "1.2", "115%"], ["115%", mixed(1, 1, 4), "1.2"]],
                       "As decimals: 1.2 = 1.20, 115%% = 1.15, %s = 1.25. So <b>115%%, 1.2, %s</b>."
                       % (mixed(1, 1, 4), mixed(1, 1, 4))))

    its.append(mcq("Which is the <b>greatest</b>?", "0.45", [fr(2, 5), "42%", "0.405"],
                   "As decimals: 0.450, %s = 0.400, 42%% = 0.420, 0.405. The greatest is <b>0.45</b>." % fr(2, 5)))
    its.append(mcq("Which is the <b>smallest</b>?", "0.205", [fr(1, 4), "0.3", "22%"],
                   "As decimals: 0.205, %s = 0.250, 0.300, 22%% = 0.220. The smallest is <b>0.205</b>, "
                   "even though it has the most digits." % fr(1, 4)))
    its.append(mcq("Which number is between 0.3 and 0.4?", fr(3, 8), [fr(1, 4), "45%", "0.43"],
                   "%s = 0.375, which is between 0.3 and 0.4. %s = 0.25 and 45%% = 0.45 are not; 0.43 is more than 0.4."
                   % (fr(3, 8), fr(1, 4))))
    its.append(mcq("Which number is greater than %s but less than %s?" % (fr(1, 4), fr(1, 3)), "0.3",
                   ["0.2", "35%", "0.24"],
                   "%s = 0.25 and %s = 0.333… <b>0.3</b> is between them. 35%% = 0.35 is more than 0.333…"
                   % (fr(1, 4), fr(1, 3))))
    its.append(mcq(fig(line_svg(8, 3, {0: "0", 4: "0.5", 8: "1"})) +
                   "The line from 0 to 1 is split into 8 equal parts. What decimal is at the red dot?",
                   "0.375", ["0.3", "0.38", "0.83"],
                   "8 equal parts, so each part is %s. The dot is 3 parts along: %s = 3 ÷ 8 = <b>0.375</b>. "
                   "0.3 would be 3 tenths, but the line has 8 parts, not 10." % (fr(1, 8), fr(3, 8))))
    its.append(mcq(fig(line_svg(5, 4, {0: "0%", 5: "100%"})) +
                   "The line from 0% to 100% is split into 5 equal parts. What percentage is at the red dot?",
                   "80%", ["4%", "40%", "45%"],
                   "5 equal parts, so each part is %s = 20%%. The dot is 4 parts along: 4 × 20%% = <b>80%%</b>. "
                   "40%% counts each part as 10%%." % fr(1, 5)))
    # the question text "Compare." repeats with different choices, so make each stem name the numbers
    for it in its:
        if it["q"] == "Compare.":
            a, b = re.split(r" &lt; | &gt; | = ", it["c"][0])
            it["q"] = "Compare <b>%s</b> and <b>%s</b>." % (a, b)
    order = [0, 1, 2, 6, 3, 4, 5, 7, 8, 14, 15, 9, 10, 16, 18, 19, 11, 12, 17, 13]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare and order fractions, decimals and percentages", "items": its}


# ============================================================ set 5: in context
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s scores 18 out of 20 in a spelling test. What percentage does %s score?" % (n, he),
                   "90%", ["18%", "10%", "9%"],
                   "%s = %s (multiply the top and bottom by 5) = <b>90%%</b>. 10%% is the part %s got wrong."
                   % (fr(18, 20), fr(90, 100), he)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("In a maths test, %s scores 21 out of 25 and %s scores 17 out of 20. Who has the higher percentage?" % (a, b),
                   b, [a, "They are the same", "You can’t tell"],
                   "%s = %s = 84%%. %s = %s = 85%%. 85%% &gt; 84%%, so <b>%s</b> does better, even with fewer marks."
                   % (fr(21, 25), fr(84, 100), fr(17, 20), fr(85, 100), b)))
    its.append(mcq("A shop sign says <b>25% off</b>. What fraction of the price is taken off?", fr(1, 4),
                   [fr(1, 25), fr(2, 5), fr(3, 4)],
                   "25%% = %s = <b>%s</b>. %s is what you still pay." % (fr(25, 100), fr(1, 4), fr(3, 4))))
    its.append(mcq("Shop A has %s off a coat. Shop B has 20%% off the same coat. Which shop takes off more?" % fr(1, 4),
                   "Shop A", ["Shop B", "They take off the same", "You can’t tell"],
                   "%s = 25%%, and 25%% &gt; 20%%. The coat is the same price to start with, so <b>Shop A</b> takes off more."
                   % fr(1, 4)))
    its.append(mcq("In a class, %s of the pupils walk to school. What percentage of the class walk?" % fr(3, 5),
                   "60%", ["35%", "30%", "3.5%"],
                   "%s = %s = <b>60%%</b>. 35%% just writes the digits 3 and 5." % (fr(3, 5), fr(60, 100))))
    its.append(mcq("0.7 of the pupils in Year 6 have school dinners. The rest have a packed lunch. "
                   "What percentage have a packed lunch?", "30%", ["70%", "3%", "0.3%"],
                   "0.7 = 70% have school dinners. The whole year group is 100%, so 100% − 70% = <b>30%</b> have a packed lunch."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a 3 m ribbon into 4 equal pieces. How long is each piece?" % n,
                   "0.75 m", ["1.33 m", "0.34 m", "0.25 m"],
                   "3 ÷ 4 = %s m = <b>0.75 m</b>. 1.33 m is 4 ÷ 3, the wrong way round. 0.25 m would be a 1 m ribbon."
                   % fr(3, 4)))
    its.append(mcq("5 pizzas are shared equally between 8 children. How much pizza does each child get, as a decimal?",
                   "0.625", ["0.58", "1.6", "0.85"],
                   "5 ÷ 8 = %s. 50 ÷ 8 = 6 r 2, 20 ÷ 8 = 2 r 4, 40 ÷ 8 = 5, so each child gets <b>0.625</b> of a pizza. "
                   "1.6 is 8 ÷ 5." % fr(5, 8)))
    n, he, his = P.next()
    its.append(mcq("%s’s tablet battery shows 45%%. What fraction of a full charge is that?" % n, fr(9, 20),
                   [fr(4, 5), fr(1, 45), fr(45, 1000)],
                   "45%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is 0.045 = 4.5%%."
                   % (fr(45, 100), fr(9, 20), fr(45, 1000))))
    its.append(mcq("A football team won 12 of its 16 matches. What percentage of its matches did it win?",
                   "75%", ["12%", "25%", "34%"],
                   "%s = %s (divide by 4) = <b>75%%</b>. 25%% is the matches it did not win." % (fr(12, 16), fr(3, 4))))
    its.append(mcq("A carton of fruit juice is %s apple juice and 40%% orange juice. Is there more apple or orange juice?" % fr(3, 8),
                   "Orange", ["Apple", "The same amount", "You can’t tell"],
                   "%s = 0.375 = 37.5%%. 40%% &gt; 37.5%%, so there is more <b>orange</b> juice." % fr(3, 8)))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("%s scores 33 out of 40 in a reading test. %s scores 82%%. Who has the higher score?" % (a, b),
                   a, [b, "They are the same", "You can’t tell"],
                   "%s = 33 ÷ 40 = 0.825 = 82.5%%. 82.5%% &gt; 82%%, so <b>%s</b> has the higher score."
                   % (fr(33, 40), a)))
    its.append(mcq("Four shops have a sale on the same trainers. Which sign gives the <b>biggest</b> discount?",
                   "35% off", [fr(1, 3) + " off", "30% off", fr(1, 4) + " off"],
                   "As percentages: %s = 33.3…%%, 30%%, %s = 25%%. 35%% is the biggest, so <b>35%% off</b>."
                   % (fr(1, 3), fr(1, 4))))
    its.append(mcq("There are 50 pupils in Year 6. 23 of them cycle to school. What percentage cycle?",
                   "46%", ["23%", "27%", "2.3%"],
                   "%s = %s (multiply the top and bottom by 2) = <b>46%%</b>. 27%% uses the 27 pupils who do not cycle."
                   % (fr(23, 50), fr(46, 100))))
    n, he, his = P.next()
    its.append(mcq("%s’s sunflower is 0.375 m tall. What fraction of a metre is that?" % n, fr(3, 8) + " m",
                   [fr(375, 100) + " m", fr(3, 75) + " m", fr(1, 375) + " m"],
                   "0.375 = %s. Divide the top and bottom by 125: <b>%s m</b>. %s m would be 3.75 m."
                   % (fr(375, 1000), fr(3, 8), fr(375, 100))))
    its.append(mcq("£2 is shared equally between 5 children. How much does each child get?", "40p",
                   ["£2.50", "25p", "4p"],
                   "£2 ÷ 5 = %s of £1 = %s = £0.40 = <b>40p</b>. £2.50 is 5 ÷ 2, the wrong way round."
                   % (fr(2, 5), fr(4, 10))))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("At PE, %s hits the target 7 times out of 8. %s hits it 85%% of the time. Who is more accurate?" % (a, b),
                   a, [b, "They are the same", "You can’t tell"],
                   "%s = 7 ÷ 8 = 0.875 = 87.5%%. 87.5%% &gt; 85%%, so <b>%s</b> is more accurate." % (fr(7, 8), a)))
    n, he, his = P.next()
    its.append(mcq("A bag holds 1 kg of flour. %s uses 0.4 kg to make bread. What percentage of the bag does %s use?" % (n, he),
                   "40%", ["4%", "0.4%", "60%"],
                   "0.4 kg out of 1 kg is 0.4 of the bag. 0.4 = %s = <b>40%%</b>. 60%% is what is left." % fr(40, 100)))
    n, he, his = P.next()
    its.append(mcq("A quiz has 20 questions. %s gets 0.85 of them right. How many questions does %s get right?" % (n, he),
                   "17", ["85", "8.5", "3"],
                   "0.85 = %s = %s. %s of 20 questions is <b>17</b> questions. 3 is the number %s gets wrong, and 8.5 is 0.85 × 10."
                   % (fr(85, 100), fr(17, 20), fr(17, 20), he)))
    its.append(mcq("A water bottle holds 1 litre. Jack drinks 0.35 litres. What fraction of the bottle is left?",
                   fr(13, 20), [fr(7, 20), fr(65, 10), fr(3, 5)],
                   "1 − 0.35 = 0.65 litres are left. 0.65 = %s = <b>%s</b> (divide by 5). %s is the part he drank."
                   % (fr(65, 100), fr(13, 20), fr(7, 20))))
    assert len(its) == 20, len(its)
    return {"title": "Fractions, decimals and percentages in context", "items": its}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg(["4.073"], hi=(0, -2))
    f_div = short_div(3, 8, 3)
    f_grid = grid_svg(20, cell=22)
    return (
        "<h2>Place value to three decimal places</h2>"
        "<p>After the decimal point come <b>tenths</b>, then <b>hundredths</b>, then <b>thousandths</b>. "
        "1 tenth = 10 hundredths = 100 thousandths. A 0 holds an empty place.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>In 4.073 the 7 is in the hundredths place, so it is worth 7 hundredths = 0.07. "
        "The 3 is worth 3 thousandths = 0.003.</figcaption></figure>"
        "<h2>A fraction is a division</h2>"
        "<p>" + fr(3, 8) + " means 3 ÷ 8. To change a fraction into a decimal, divide the numerator by the denominator. "
        "Write the number being divided with a decimal point and some zeros, then use short division.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>3 ÷ 8: 8 into 3 goes 0 times, remainder 3. 30 ÷ 8 = 3 r 6, 60 ÷ 8 = 7 r 4, 40 ÷ 8 = 5. "
        "So " + fr(3, 8) + " = 0.375.</figcaption></figure>"
        + ex("Quicker way", "Write " + fr(7, 20) + " as a decimal.",
             "Make the denominator 100: 20 × 5 = 100, so multiply the top by 5 too. " + fr(7, 20) + " = " + fr(35, 100) + ".",
             "0.35")
        + "<h2>Fractions, decimals and percentages</h2>"
        "<p>Per cent means <b>out of 100</b>. To change a decimal into a percentage, multiply by 100: 0.4 = 40%. "
        "To change a percentage into a decimal, divide by 100: 7% = 0.07.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>20 of 100 squares are shaded: " + fr(1, 5) + " = " + fr(20, 100) + " = 0.2 = 20%.</figcaption></figure>"
        + table(["Fraction", "Decimal", "Percentage"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 10), "0.1", "10%"],
            [fr(1, 8), "0.125", "12.5%"],
            [fr(1, 3), "0.333…", "33.3…%"],
        ])
        + "<h2>Comparing and ordering</h2>"
        "<p>Change everything into the same form first. Decimals with the <b>same number of places</b> are easiest to compare.</p>"
        + ex("Example", "Order 0.35, " + fr(3, 8) + " and 37% from smallest to greatest.",
             "0.35 = 0.350. " + fr(3, 8) + " = 0.375. 37% = 0.370. Compare 350, 370 and 375 thousandths.",
             "0.35, 37%, " + fr(3, 8))
        + ex("Who did better?", "Freya scored 21 out of 25. George scored 17 out of 20.",
             fr(21, 25) + " = " + fr(84, 100) + " = 84%. " + fr(17, 20) + " = " + fr(85, 100) + " = 85%.",
             "George, with the higher percentage")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(3, 8) + " = 0.38 or 3.8", "Divide: 3 ÷ 8 = 0.375"],
            [fr(1, 5) + " = 0.5 or 15%", fr(1, 5) + " = " + fr(2, 10) + " = 0.2 = 20%"],
            ["0.4 = 4%", "0.4 = 0.40 = 40%"],
            ["0.305 &gt; 0.35 because it has more digits", "Use 3 places: 0.305 &lt; 0.350"],
            ["The 7 in 4.007 is 7 hundredths", "The third place is thousandths: 0.007"],
            ["7 ÷ 4 = 1 r 3 = 1.3", "Divide the remainder too: " + fr(3, 4) + " = 0.75, so 1.75"],
        ])
    )


FAQ = [
    {"q": "What fractions, decimals and percentages do children learn in Year 6?",
     "a": "In Year 6 children find decimal equivalents of fractions by dividing (3/8 = 3 ÷ 8 = 0.375), read the value of each digit up to three decimal places, and use equivalences such as 1/5 = 0.2 = 20% and 3/4 = 0.75 = 75% to compare and solve problems."},
    {"q": "How do you change a fraction into a decimal?",
     "a": "Divide the numerator by the denominator, for example 3/8 = 3 ÷ 8 = 0.375 using short division. If the denominator goes into 10, 100 or 1,000, you can make an equivalent fraction instead: 7/20 = 35/100 = 0.35."},
    {"q": "How do you order fractions, decimals and percentages?",
     "a": "Change them all into decimals with the same number of decimal places, then compare. For 0.35, 3/8 and 37%: 0.350, 0.375 and 0.370, so the order is 0.35, 37%, 3/8."},
    {"q": "Are fractions, decimals and percentages in the Year 6 SATs?",
     "a": "Yes. The KS2 SATs arithmetic paper and both reasoning papers often include them, such as writing a fraction as a decimal, ordering mixed numbers in different forms and comparing test scores as percentages."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred squares, number lines, place value charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(6609)
    P = People(rnd)
    sets = [set_place_value(), set_division(), set_equivalents(), set_compare(), set_problems(P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "fractions-decimals-and-percentages", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Fractions, Decimals and Percentages",
        "seo_title": "Year 6 Fractions, Decimals and Percentages Worksheets: 3/8 = 0.375, Equivalents and Ordering",
        "short_title": "Fractions, decimals and percentages",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 6: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Associate a fraction with division and calculate decimal fraction equivalents [for example, 0.375] for a simple fraction [for example, 3/8]; identify the value of each digit in numbers given to three decimal places; recall and use equivalences between simple fractions, decimals and percentages, including in different contexts.",
        "meta_desc": "Free Year 6 fractions, decimals and percentages worksheets for the National Curriculum: place value to three decimal places, fractions as division (3/8 = 0.375), equivalents such as 1/5 = 0.2 = 20%, ordering mixed forms and SATs-style problems. 100 maths questions with an answer key.",
        "key_big": "A fraction is a division: 3/8 = 3 ÷ 8 = 0.375. Per cent means out of 100: 0.375 = 37.5%.",
        "key_sub": "Know the key facts: 1/2 = 0.5 = 50%, 1/4 = 0.25 = 25%, 1/5 = 0.2 = 20%, 1/8 = 0.125 = 12.5%. To compare, change everything into decimals with the same number of places.",
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
