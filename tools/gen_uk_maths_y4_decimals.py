# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Decimals (National Curriculum in England, Year 4: Fractions (including decimals))
  python3 tools/gen_uk_maths_y4_decimals.py
Hundred squares and number lines are drawn from whole numbers of hundredths (47 = 0.47).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
British English, pounds and pence, metric units. HTML attributes use single quotes (no backslashes in the JSON).
When dividing by 10 and 100 the lesson says the DIGITS move (the way it is taught in English schools).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LINE = "#2b2b2b"
THIN = "#8a8a8a"      # lines between small squares
RED = "#d6453b"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def D(h, places=None):
    """Decimal text for h hundredths. places: 1 or 2 (default: 1 if h is whole tenths, else 2)."""
    if places is None:
        places = 1 if h % 10 == 0 else 2
    if places == 1:
        assert h % 10 == 0, h
        return "%d.%d" % (h // 100, (h % 100) // 10)
    return "%d.%02d" % (h // 100, h % 100)


def N(x):
    """Exact decimal text without extra zeros: Dm('6.0') -> '6'."""
    s = format(Dm(x).normalize(), "f")
    return s


FRX = re.compile(r"^(?:(\d+) and )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(£)?([\d,]*\.?\d+)(p)?( .+)?$")


def val(c):
    """(value, unit) of a choice: '£0.45' and '45p' are both 0.45 pounds; fractions are read from the spans.
    None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), m.group(4) or "")
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(",", ""))
    if m.group(1):
        return (v, "£")
    if m.group(3):
        return (v / 100, "£")
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong. Positions are set by balance(). Choices must differ in value too (0.3 vs 0.30)."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
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


def squ(n):
    return "1 square" if n == 1 else "%d squares" % n


def tenths_words(t):
    return "1 tenth" if t == 1 else "%d tenths" % t


def hund_words(h):
    return "1 hundredth" if h == 1 else "%d hundredths" % h


def rnd_whole(x):
    return Dm(x).quantize(Dm(1), rounding=ROUND_HALF_UP)


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
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "hundred square with %s shaded" % squ(k))


def bar_svg(k, W=300, H=44):
    """Tenths bar: 10 equal parts, first k shaded."""
    s = []
    for i in range(10):
        s.append("<rect x='%d' y='6' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (6 + i * W // 10, W // 10, H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 12, H + 12, "".join(s), "tenths bar split into 10 equal parts with %d shaded" % k)


def line_svg(a, b, spaces, dot=None, labels=None, W=380):
    """Number line from a to b hundredths with `spaces` equal spaces and a red dot at `dot` (hundredths).
    labels: hundredths values written under the line (default: both ends)."""
    L, R, Y = 26, W - 26, 30
    assert (b - a) % spaces == 0
    step = (b - a) // spaces

    def X(v):
        return L + (R - L) * (v - a) / float(b - a)
    labels = labels if labels is not None else [a, b]
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
    for v in labels:
        assert (v - a) % step == 0
        txt = str(v // 100) if v % 100 == 0 else D(v)
        s.append(text(X(v), Y + 36, txt, 17))
    if dot is not None:
        assert (dot - a) % step == 0 and a <= dot <= b
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from %s to %s split into %d equal spaces" % (D(a), D(b), spaces))


PV_COLS = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths")]


def chart_svg(rows, row_labels=None, hi=None):
    """Place value chart: Tens | Ones | . | Tenths | Hundredths. rows: numbers as text ('34', '3.4', '0.34').
    row_labels: text in a column on the left. hi: (row, place) to colour red."""
    CW, PW, HEAD, ROW = 88, 16, 30, 44
    LW = 78 if row_labels else 0
    x0, y0 = 6, 6
    W = 2 * x0 + LW + 4 * CW + PW
    H = 2 * y0 + HEAD + ROW * len(rows)
    xs, x = {}, x0 + LW
    for p, _ in PV_COLS:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, W - 2 * x0 - LW, HEAD + ROW * len(rows), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, W - 2 * x0 - LW, HEAD, HEADFILL)]
    for p, name in PV_COLS:
        if p != 1:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW * len(rows), GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, name, 14))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW * len(rows), GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0 + LW, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    for r, s in enumerate(rows):
        yb = y0 + HEAD + ROW * r
        if r:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + LW, yb, W - x0, yb, GREEN))
        if row_labels:
            o.append(text(x0 + LW - 8, yb + 29, row_labels[r], 16, anchor="end"))
        w, _, f = s.partition(".")
        assert len(w) <= 2 and len(f) <= 2, s
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


# ============================================================ set 1: tenths and hundredths
def set_tenths_hundredths():
    its = []
    for k, wrong in [(37, ["3.7", "37", "0.63"]), (8, ["0.8", "8", "0.92"]), (52, ["5.2", "52", "0.48"]),
                     (70, ["0.07", "7", "0.3"]), (19, ["1.9", "0.91", "19"]), (4, ["0.4", "4", "0.96"])]:
        t, h = k // 10, k % 10
        if t == 0:
            e = ("The hundred square has 100 equal squares, so each square is 1 hundredth. %s shaded and there is no full column, "
                 "so there are 0 tenths. %s = %s = <b>%s</b>. Write the 0 in the tenths place."
                 % ("1 square is" if k == 1 else "%d squares are" % k, hund_words(k), fr(k, 100), D(k)))
        elif h == 0:
            e = ("Each full column is 1 tenth. %d full columns are shaded: %s = %s = <b>%s</b> (or 0.70). "
                 "0.07 would be only 7 small squares." % (t, tenths_words(t), fr(t, 10), D(k)))
        else:
            e = ("Each full column is 1 tenth and each small square is 1 hundredth. <b>%d full %s</b> and <b>%s</b> are shaded: "
                 "%s and %s = %s = <b>%s</b>." % (t, "column" if t == 1 else "columns", squ(h), tenths_words(t), hund_words(h),
                                                  fr(k, 100), D(k)))
        its.append(mcq(fig(grid_svg(k)) + "The whole square is 1. What decimal is shaded?", D(k), wrong, e))

    for k, wrong in [(3, ["0.03", "3.10", "0.7"]), (8, ["0.08", "8.10", "0.2"])]:
        e = ("The bar has 10 equal parts, so each part is 1 tenth. %d parts are shaded: %s = <b>%s</b>. "
             "One digit after the decimal point means tenths." % (k, fr(k, 10), D(k * 10)))
        its.append(mcq(fig(bar_svg(k)) + "The whole bar is 1. What decimal is shaded?", D(k * 10), wrong, e))

    for n, d, wrong in [(3, 10, ["0.03", "3.10", "3.0"]), (23, 100, ["2.3", "23.100", "0.023"]),
                        (7, 100, ["0.7", "7.100", "7.0"]), (9, 10, ["0.09", "9.10", "0.1"]),
                        (60, 100, ["0.06", "6", "60"])]:
        right = D(n * 100 // d)
        if d == 10:
            e = "%s is %s. Tenths are the <b>first</b> place after the decimal point: <b>%s</b>." % (fr(n, d), tenths_words(n), right)
        elif n < 10:
            e = ("%s is %s. Hundredths need <b>two places</b> after the point, so write a 0 in the tenths place: <b>%s</b>. "
                 "(0.%d would be %d tenths.)" % (fr(n, d), hund_words(n), right, n, n))
        elif n % 10 == 0:
            e = ("%s is %d hundredths, which is the same as %s: <b>%s</b> (or 0.60). "
                 "0.06 would be only 6 hundredths." % (fr(n, d), n, tenths_words(n // 10), right))
        else:
            e = ("%s is %d hundredths: %s and %s. So the tenths digit is %d and the hundredths digit is %d: <b>%s</b>."
                 % (fr(n, d), n, tenths_words(n // 10), hund_words(n % 10), n // 10, n % 10, right))
        assert F(Dm(right)) == F(n, d)
        its.append(mcq("Write %s as a decimal." % fr(n, d), right, wrong, e))

    its.append(mcq("Which fraction is equal to <b>0.4</b>?", fr(4, 10), [fr(4, 100), fr(1, 4), fr(1, 40)],
                   "0.4 has one digit after the point, so it means tenths: 4 tenths = <b>%s</b>. "
                   "It is not %s: that is 0.25." % (fr(4, 10), fr(1, 4))))
    its.append(mcq("Which fraction is equal to <b>0.09</b>?", fr(9, 100), [fr(9, 10), fr(91, 100), fr(1, 9)],
                   "0.09 has two digits after the point, so it means hundredths. The tenths digit is 0: "
                   "0.09 = 9 hundredths = <b>%s</b>." % fr(9, 100)))

    its.append(mcq("Which decimal is <b>4 tenths and 5 hundredths</b>?", "0.45", ["4.5", "0.54", "45"],
                   "Tenths go in the first place after the point and hundredths in the second: <b>0.45</b>."))
    its.append(mcq("Which decimal is <b>2 ones and 3 hundredths</b>?", "2.03", ["2.3", "23", "0.23"],
                   "2 ones, then the point. There are 0 tenths, so write a 0 before the 3 hundredths: <b>2.03</b>. "
                   "(2.3 would be 3 tenths.)"))

    its.append(mcq("1 whole is divided into 100 equal parts. What decimal is each part?", "0.01", ["0.1", "1", "100"],
                   "Each part is %s of the whole, one <b>hundredth</b>: <b>0.01</b>. "
                   "0.1 is one tenth, which you get by dividing 1 into 10 parts." % fr(1, 100)))
    its.append(mcq("1 tenth is divided into 10 equal parts. What decimal is each part?", "0.01", ["0.1", "1", "0.001"],
                   "There are 10 tenths in 1 whole, and each tenth splits into 10 parts. That makes 10 × 10 = 100 parts in the whole, "
                   "so each part is one <b>hundredth</b>: <b>0.01</b>."))
    its.append(mcq("How many hundredths are there in <b>0.4</b>?", "40", ["4", "400", "60"],
                   "1 tenth = 10 hundredths, so 4 tenths = <b>40</b> hundredths. 0.4 = 0.40. "
                   "(4 is the number of tenths, not hundredths.)"))
    assert len(its) == 20, len(its)
    return {"title": "Tenths and hundredths", "items": its}


# ============================================================ set 2: quarters, halves, counting in hundredths
def set_equivalents():
    its = []
    for (n, d), right, wrong, e in [
        ((1, 2), "0.5", ["0.2", "1.2", "0.12"],
         "%s = %s, because 5 is half of 10. So %s = <b>0.5</b>. Do not just write the 1 and the 2 as digits." % (fr(1, 2), fr(5, 10), fr(1, 2))),
        ((1, 4), "0.25", ["0.4", "1.4", "0.14"],
         "%s of 100 is 25, so %s = %s = <b>0.25</b>. 0.4 is a common mistake: it uses the 4 from the bottom of the fraction." % (fr(1, 4), fr(1, 4), fr(25, 100))),
        ((3, 4), "0.75", ["0.34", "3.4", "0.43"],
         "%s = 25 hundredths, so %s = 3 × 25 = 75 hundredths = <b>0.75</b>." % (fr(1, 4), fr(3, 4))),
    ]:
        assert F(Dm(right)) == F(n, d)
        its.append(mcq("Write %s as a decimal." % fr(n, d), right, wrong, e))
    for dec, (n, d), wrong, e in [
        ("0.25", (1, 4), [fr(2, 5), fr(1, 25), fr(25, 10)],
         "0.25 = %s. 25 is a quarter of 100, so 0.25 = <b>%s</b>." % (fr(25, 100), fr(1, 4))),
        ("0.5", (1, 2), [fr(1, 5), fr(5, 100), fr(5, 1)],
         "0.5 = %s = 50 hundredths, which is half of 100. So 0.5 = <b>%s</b>. (%s is 0.2.)" % (fr(5, 10), fr(1, 2), fr(1, 5))),
        ("0.75", (3, 4), [fr(7, 5), fr(1, 75), fr(75, 10)],
         "0.75 = %s. 75 is three quarters of 100, so 0.75 = <b>%s</b>." % (fr(75, 100), fr(3, 4))),
    ]:
        assert F(Dm(dec)) == F(n, d)
        its.append(mcq("Which fraction is equal to <b>%s</b>?" % dec, fr(n, d), wrong, e))
    its.append(mcq(fig(grid_svg(25)) + "What fraction of the hundred square is shaded?", fr(1, 4),
                   [fr(1, 25), fr(3, 4), fr(2, 5)],
                   "25 of the 100 squares are shaded: %s = 0.25. 4 lots of 25 make 100, so this is <b>%s</b>."
                   % (fr(25, 100), fr(1, 4))))
    its.append(mcq(fig(grid_svg(75)) + "What fraction of the hundred square is shaded?", fr(3, 4),
                   [fr(1, 4), fr(7, 5), fr(1, 75)],
                   "75 of the 100 squares are shaded: %s = 0.75. Only 25 squares are white (%s), so the shaded part is <b>%s</b>."
                   % (fr(75, 100), fr(1, 4), fr(3, 4))))

    its.append(mcq("Count up in hundredths. What comes next?<br><b>0.37, 0.38, 0.39, ?</b>", "0.40",
                   ["0.310", "0.30", "0.50"],
                   "0.39 + 0.01: 9 hundredths and 1 more make 10 hundredths, which is 1 more tenth. "
                   "So 3 tenths become 4 tenths: <b>0.40</b> (the same as 0.4). There is no such step as 0.310."))
    its.append(mcq("Count down in hundredths. What comes next?<br><b>0.72, 0.71, 0.70, ?</b>", "0.69",
                   ["0.60", "0.79", "0.80"],
                   "0.70 − 0.01: there are no hundredths left, so exchange 1 tenth for 10 hundredths. "
                   "7 tenths become 6 tenths and 9 hundredths: <b>0.69</b>."))
    its.append(mcq("Count up in hundredths. What comes next?<br><b>1.97, 1.98, 1.99, ?</b>", "2.00",
                   ["1.100", "1.90", "2.10"],
                   "1.99 + 0.01: 99 hundredths and 1 more make 100 hundredths, which is 1 whole. "
                   "So 1.99 + 0.01 = <b>2.00</b> (the same as 2)."))
    its.append(mcq("Count up in tenths. What comes next?<br><b>0.7, 0.8, 0.9, ?</b>", "1.0",
                   ["0.10", "0.91", "10"],
                   "0.9 + 0.1: 9 tenths and 1 more make 10 tenths, which is 1 whole. So the next number is <b>1.0</b> (or 1). "
                   "0.10 is only 1 tenth."))
    its.append(mcq("What is the missing number?<br><b>0.46, 0.47, ?, 0.49</b>", "0.48", ["0.57", "0.58", "0.408"],
                   "The numbers go up by 1 hundredth each time: 0.47 + 0.01 = <b>0.48</b>. Check: 0.48 + 0.01 = 0.49."))
    its.append(mcq("Start at 0.58. Count on <b>3 hundredths</b>. Where do you land?", "0.61", ["0.511", "0.88", "0.51"],
                   "0.59, 0.60, 0.61. After 0.59, 10 hundredths make a new tenth, so 0.59 + 0.01 = 0.60. You land on <b>0.61</b>. "
                   "(0.88 adds 3 tenths, not 3 hundredths.)"))

    for a, v in [(30, 36), (80, 83)]:
        k = v - a
        e = ("The line goes from %s to %s, which is 1 tenth. It has <b>10 equal spaces</b>, so each space is 1 hundredth. "
             "%s = %s. Count %d spaces on: <b>%s</b>." % (D(a), D(a + 10), D(a, 1), D(a, 2), k, D(v)))
        wrong = ["0.0%d" % k, "%d.%d" % (v // 10, v % 10), D(v + 1)]
        its.append(mcq(fig(line_svg(a, a + 10, 10, dot=v)) + "What decimal is at the red dot?", D(v), wrong, e))
    its.append(mcq(fig(line_svg(0, 100, 4, dot=75)) + "The line from 0 to 1 is split into 4 equal parts. What decimal is at the red dot?",
                   "0.75", ["0.3", "0.34", "0.25"],
                   "4 equal parts means each part is %s = 0.25. The dot is 3 parts along: %s = <b>0.75</b>."
                   % (fr(1, 4), fr(3, 4))))
    its.append(mcq(fig(line_svg(0, 100, 4, dot=25)) + "The line from 0 to 1 is split into 4 equal parts. What decimal is at the red dot?",
                   "0.25", ["0.1", "0.4", "0.14"],
                   "4 equal parts means each part is %s. The dot is 1 part along: %s = <b>0.25</b>. "
                   "It is not 0.1: the line has 4 parts, not 10." % (fr(1, 4), fr(1, 4))))

    its.append(mcq("Write 2 and %s as a decimal." % fr(3, 4), "2.75", ["2.34", "2.3", "3.4"],
                   "2 ones, then %s = 0.75. So 2 and %s = <b>2.75</b>." % (fr(3, 4), fr(3, 4))))
    its.append(mcq("Write 1 and %s as a decimal." % fr(1, 4), "1.25", ["1.4", "1.14", "1.5"],
                   "1 one, then %s = 0.25. So 1 and %s = <b>1.25</b>. (1.5 would be 1 and a half.)" % (fr(1, 4), fr(1, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Halves, quarters and counting in hundredths", "items": its}


# ============================================================ set 3: divide by 10 and 100
def div_e(n, by):
    ans = Dm(n) / by
    places = 1 if by == 10 else 2
    e = ("Dividing by %d makes the number %d times smaller. Each digit moves <b>%s to the right</b>: %d ÷ %d = <b>%s</b>."
         % (by, by, "1 place" if places == 1 else "2 places", n, by, N(ans)))
    if ans < 1:
        e += " Write a 0 in the ones place%s." % (" (and in the tenths place)" if ans < Dm("0.1") else "")
    return ans, e


def set_divide():
    its = []
    for n, by, wrong in [(7, 10, ["0.07", "70", "7.10"]), (3, 10, ["0.03", "30", "0.3"]), (4, 100, ["0.4", "400", "0.004"]),
                         (8, 100, ["0.8", "800", "0.008"])]:
        ans, e = div_e(n, by)
        wrong = [w for w in wrong if Dm(w) != ans]
        if len(wrong) == 2:
            wrong.append("3.10")
        its.append(mcq("%d ÷ %d = ?" % (n, by), N(ans), wrong, e))
    for n in [34, 56, 82, 60]:
        ans, e = div_e(n, 10)
        wrong = [N(Dm(n) / 100), N(Dm(n) * 10), "%d.%d" % (n % 10, n // 10)] if n % 10 else ["0.6", "600", "0.06"]
        if n % 10 == 0:
            e += " The ones digit 0 moves to the tenths place, so 6.0 is just 6."
        its.append(mcq("%d ÷ 10 = ?" % n, N(ans), wrong, e))
    for n in [27, 75, 20, 61]:
        ans, e = div_e(n, 100)
        if n % 10:
            wrong = [N(Dm(n) / 10), "0.0%d" % n, "%s" % "{:,}".format(n * 100)]
        else:
            wrong = ["2", "0.02", "2,000"]
            e += " 0.20 is the same as 0.2."
        its.append(mcq("%d ÷ 100 = ?" % n, N(ans), wrong, e))

    for n, by, place, wrong in [(47, 10, -1, ["7 ones", "7 hundredths", "7 tens"]),
                                (58, 100, -2, ["8 tenths", "8 ones", "8 tens"]),
                                (36, 10, 0, ["3 tens", "3 tenths", "3 hundredths"]),
                                (90, 100, -1, ["9 hundredths", "9 ones", "9 tens"])]:
        ans = Dm(n) / by
        s = N(ans)
        dg = str(n)[0] if place in (0,) or n in (90,) else str(n)[1]
        if n == 58:
            dg = "8"
        if n == 47:
            dg = "7"
        name = {0: "ones", -1: "tenths", -2: "hundredths"}[place]
        right = "%s %s" % (dg, name)
        # the digit really is in that place
        w, _, f = s.partition(".")
        got = w[-1] if place == 0 else f[-place - 1]
        assert got == dg, (n, s, dg)
        row = s
        e = ("%d ÷ %d = %s. The digits moved %s to the right, so the %s is now in the <b>%s</b> place. Its value is <b>%s</b>."
             % (n, by, s, "1 place" if by == 10 else "2 places", dg, name, right))
        its.append(mcq(fig(chart_svg([row], hi=(0, place))) + "The chart shows %d ÷ %d = %s. What is the value of the red digit?"
                       % (n, by, s), right, wrong, e))

    its.append(mcq("? ÷ 10 = 0.6", "6", ["60", "0.06", "600"],
                   "Use the inverse: 0.6 × 10 = <b>6</b>. Check: 6 ÷ 10 = 0.6. (60 ÷ 10 is 6, not 0.6.)"))
    its.append(mcq("? ÷ 100 = 0.45", "45", ["4.5", "450", "4,500"],
                   "Use the inverse: 0.45 × 100 = <b>45</b>. Check: 45 ÷ 100 = 0.45. (4.5 is 45 ÷ 10.)"))
    its.append(mcq("Which calculation has the answer <b>0.38</b>?", "38 ÷ 100", ["38 ÷ 10", "38 × 10", "8 ÷ 100"],
                   "0.38 is 38 hundredths. Dividing 38 by 100 moves both digits 2 places to the right: <b>38 ÷ 100</b> = 0.38. "
                   "38 ÷ 10 is 3.8."))
    its.append(mcq("8 ÷ 10 ÷ 10 = ?", "0.08", ["0.8", "0.008", "80"],
                   "8 ÷ 10 = 0.8. Then 0.8 ÷ 10 = <b>0.08</b>. Dividing by 10 twice is the same as dividing by 100."))
    assert len(its) == 20, len(its)
    return {"title": "Divide by 10 and 100", "items": its}


# ============================================================ set 4: compare and round
def cmp_item(x, y, kind):
    a, b = Dm(x), Dm(y)
    assert len(x.split(".")[1]) == len(y.split(".")[1])
    sign = "&lt;" if a < b else "&gt;"
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    if kind == "ones":
        e = "Compare the ones first: %s has %s and %s has %s, so <b>%s %s %s</b>." % (
            x, x.split(".")[0] + " ones", y, y.split(".")[0] + " ones", x, sign, y)
    elif kind == "tenths":
        tx, ty = x.split(".")[1][0], y.split(".")[1][0]
        e = ("The ones are the same, so compare the <b>tenths</b>: %s and %s. So <b>%s %s %s</b>."
             % (tenths_words(int(tx)), tenths_words(int(ty)), x, sign, y))
        if len(x.split(".")[1]) == 2:
            e += " The tenths decide it, not the last digit."
    else:  # hundredths
        e = ("The ones and tenths are the same, so compare the hundredths: %s and %s. So <b>%s %s %s</b>."
             % (x[-1], y[-1], x, sign, y))
    return mcq("Compare the decimals.", right, wrong, e)


def round_item(x, P):
    r = rnd_whole(x)
    w, _, t = x.partition(".")
    lo, hi = int(w), int(w) + 1
    other = lo if int(r) == hi else hi
    wrong = [str(other), t, "%d.%s" % (int(w) + 1, t)]
    wrong = [c for c in wrong if Dm(c) != r]
    if len(wrong) < 3:
        wrong.append(str(int(r) + 1))
    e = ("%s is between %d and %d. Look at the tenths digit: <b>%s</b>. %s, so %s rounds to <b>%s</b>."
         % (x, lo, hi, t, "5 or more rounds up" if int(t) >= 5 else "4 or less rounds down", x, r))
    if t == "5":
        e += " 4.5 is exactly halfway: halfway always rounds <b>up</b>." if x == "4.5" else " Halfway always rounds <b>up</b>."
    return mcq("Round <b>%s</b> to the nearest whole number." % x, str(r), wrong[:3], e)


def set_compare_round(P):
    its = []
    for x, y, kind in [("0.45", "0.54", "tenths"), ("3.7", "3.2", "tenths"), ("0.08", "0.80", "tenths"),
                       ("2.63", "2.36", "tenths"), ("5.1", "4.9", "ones"), ("0.71", "0.17", "tenths"), ("6.48", "6.43", "hundredths")]:
        its.append(cmp_item(x, y, kind))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.83", ["0.38", "0.80", "0.08"],
                   "All have 0 ones. Compare the tenths: 0.83 and 0.80 both have 8 tenths. Then the hundredths: 3 &gt; 0. "
                   "So <b>0.83</b> is the greatest."))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "2.4", ["4.2", "2.9", "3.1"],
                   "Compare the ones first: 2.4 and 2.9 have 2 ones. Then the tenths: 4 &lt; 9. So <b>2.4</b> is the smallest."))
    its.append(mcq("Order from <b>smallest to greatest</b>.", "0.05, 0.35, 0.53",
                   ["0.35, 0.53, 0.05", "0.53, 0.35, 0.05", "0.05, 0.53, 0.35"],
                   "Compare the tenths: 0.05 has 0, 0.35 has 3 and 0.53 has 5. So the order is <b>0.05, 0.35, 0.53</b>."))

    for x in ["4.6", "4.5", "7.2", "12.8", "0.7", "9.5", "6.1"]:
        its.append(round_item(x, P))
    its.append(mcq(fig(line_svg(200, 300, 10, dot=230, labels=[200, 250, 300])) +
                   "The red dot shows 2.3. What is 2.3 rounded to the nearest whole number?", "2", ["3", "2.5", "23"],
                   "The dot is between 2 and 3. It is before the halfway mark (2.5), so it is nearer to <b>2</b>."))
    its.append(mcq(fig(line_svg(1500, 1600, 10, dot=1570, labels=[1500, 1550, 1600])) +
                   "The red dot shows 15.7. What is 15.7 rounded to the nearest whole number?", "16", ["15", "15.5", "17"],
                   "The dot is between 15 and 16. It is past the halfway mark (15.5), so it is nearer to <b>16</b>. "
                   "The tenths digit is 7, and 5 or more rounds up."))
    its.append(mcq("Which number rounds to <b>6</b> to the nearest whole number?", "5.7", ["5.4", "6.5", "6.7"],
                   "5.7 has 7 tenths, so it rounds up to <b>6</b>. 5.4 rounds down to 5. 6.5 and 6.7 round up to 7."))
    assert len(its) == 20, len(its)
    return {"title": "Compare and round decimals", "items": its}


# ============================================================ set 5: money and measures
def set_problems(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("A pencil costs 45p. How do you write 45p in pounds?", "£0.45", ["£45", "£4.50", "£0.54"],
                   "There are 100p in £1, so 1p = £0.01. 45p = %s of £1 = <b>£0.45</b>. (£4.50 is 450p.)" % fr(45, 100)))
    its.append(mcq("A comic costs £3.70. How many pence is that?", "370p", ["37p", "3,700p", "307p"],
                   "£3 = 300p and 70p more: 300p + 70p = <b>370p</b>. The 7 is 7 tenths of a pound, which is 70p."))
    n, he, his = P.next()
    its.append(mcq("%s has £2.45. %s gran gives %s £1. How much money does %s have now?" % (n, cap(his), "her" if he == "she" else "him", he),
                   "£3.45", ["£2.46", "£2.55", "£12.45"],
                   "Add £1 to the pounds: £2 + £1 = £3. The pence stay the same: <b>£3.45</b>. (£2.46 adds 1p, not £1.)"))
    n, he, his = P.next()
    its.append(mcq("%s has £5.60. %s spends £2.30 on a book. How much money does %s have left?" % (n, cap(he), he),
                   "£3.30", ["£7.90", "£3.03", "£3.20"],
                   "Subtract pounds from pounds and pence from pence: £5 − £2 = £3 and 60p − 30p = 30p. "
                   "So %s has <b>£3.30</b> left." % n))
    n, he, his = P.next()
    its.append(mcq("%s has a ribbon 1.25 m long and another ribbon 0.5 m long. How long are they altogether?" % n,
                   "1.75 m", ["1.30 m", "6.25 m", "0.75 m"],
                   "0.5 m = 0.50 m. Add tenths to tenths and hundredths to hundredths: 1.25 + 0.50 = <b>1.75 m</b>. "
                   "(1.30 m comes from adding the 5 to the hundredths.)"))
    n, he, his = P.next()
    its.append(mcq("%s runs 100 m in 15.7 seconds. What is %s time to the nearest second?" % (n, his),
                   "16 seconds", ["15 seconds", "17 seconds", "15.8 seconds"],
                   "15.7 is between 15 and 16. The tenths digit is 7, so round up: <b>16 seconds</b>."))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("In the long jump, %s jumps 2.48 m and %s jumps 2.84 m. Who jumps further?" % (a, b), b,
                   [a, "They jump the same", "You can’t tell"],
                   "Both jumps are 2 whole metres. Compare the tenths: 2.84 has 8 tenths and 2.48 has 4 tenths. "
                   "So <b>%s</b> jumps further." % b))
    its.append(mcq("A melon has a mass of 2.6 kg. What is its mass to the nearest kilogram?", "3 kg",
                   ["2 kg", "6 kg", "2.5 kg"],
                   "2.6 is between 2 and 3. The tenths digit is 6, so round up: <b>3 kg</b>."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a 1 m stick in half. How long is each piece in metres?" % n, "0.5 m",
                   ["0.2 m", "1.2 m", "0.12 m"],
                   "Half of 1 m is %s m = %s m = <b>0.5 m</b> (50 cm)." % (fr(1, 2), fr(5, 10))))
    its.append(mcq("A jug holds %s of a litre of milk. Write this as a decimal." % fr(1, 4), "0.25 litres",
                   ["0.4 litres", "1.4 litres", "0.14 litres"],
                   "%s = %s = 0.25. So the jug holds <b>0.25 litres</b> (250 ml)." % (fr(1, 4), fr(25, 100))))
    its.append(mcq("How much is %s of £1?" % fr(3, 4), "75p", ["34p", "£3.40", "25p"],
                   "£1 = 100p. %s of 100p is 25p, so %s of 100p is 3 × 25p = <b>75p</b> (£0.75). "
                   "25p is only %s." % (fr(1, 4), fr(3, 4), fr(1, 4))))
    n, he, his = P.next()
    its.append(mcq("%s’s pencil is 14 cm long. 1 cm is %s of a metre. How long is the pencil in metres?" % (n, fr(1, 100)),
                   "0.14 m", ["1.4 m", "140 m", "0.41 m"],
                   "14 cm = %s m. To change cm to m, divide by 100: 14 ÷ 100 = <b>0.14 m</b>. (1.4 m would be 140 cm.)"
                   % fr(14, 100)))
    its.append(mcq("£7 is shared equally between 10 children. How much does each child get?", "70p",
                   ["7p", "£70", "£7.10"],
                   "£7 ÷ 10 = £0.70. The 7 moves 1 place to the right, into the tenths place. £0.70 = <b>70p</b>. "
                   "(7p would be £7 ÷ 100.)"))
    its.append(mcq("A rope 3 m long is cut into 10 equal pieces. How long is each piece?", "0.3 m",
                   ["0.03 m", "30 m", "3.10 m"],
                   "3 ÷ 10 = <b>0.3 m</b> (30 cm). Dividing by 10 moves the 3 one place to the right, into the tenths place."))
    its.append(mcq("A ball costs £3.45 and a kite costs £3.54. Which is cheaper?", "The ball",
                   ["The kite", "They cost the same", "You can’t tell"],
                   "Both cost £3 and some pence. Compare the tenths: 4 tenths (40p) is less than 5 tenths (50p). "
                   "£3.45 &lt; £3.54, so <b>the ball</b> is cheaper."))
    n, he, his = P.next()
    its.append(mcq("A sunflower is 0.98 m tall. It grows 0.02 m more. How tall is it now?", "1.00 m",
                   ["0.100 m", "1.18 m", "0.99 m"],
                   "Count on 2 hundredths: 0.99, 1.00. 100 hundredths make 1 whole, so the sunflower is <b>1.00 m</b> (1 m) tall."))
    n, he, his = P.next()
    its.append(mcq("%s’s school bag has a mass of 3.5 kg. What is that to the nearest kilogram?" % n, "4 kg",
                   ["3 kg", "5 kg", "3.5 kg"],
                   "3.5 is exactly halfway between 3 and 4. Halfway rounds <b>up</b>, so the answer is <b>4 kg</b>."))
    its.append(mcq("A water bottle holds 0.75 litres. Which fraction of a litre is that?", fr(3, 4) + " of a litre",
                   [fr(1, 4) + " of a litre", fr(7, 5) + " of a litre", fr(75, 10) + " of a litre"],
                   "0.75 = %s. 75 is three quarters of 100, so the bottle holds <b>%s of a litre</b> (750 ml)." % (fr(75, 100), fr(3, 4))))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("On sports day, %s runs the race in 12.4 seconds and %s runs it in 12.9 seconds. Who is faster?" % (a, b),
                   a, [b, "They are equally fast", "You can’t tell"],
                   "In a race, the <b>shorter</b> time is faster. 12.4 &lt; 12.9, because 4 tenths &lt; 9 tenths. "
                   "So <b>%s</b> is faster." % a))
    n, he, his = P.next()
    its.append(mcq("%s has a £1 coin, a 50p coin, a 20p coin and a 5p coin. How much money is that?" % n, "£1.75",
                   ["£76", "£1.57", "£1.70"],
                   "50p + 20p + 5p = 75p. Then £1 + 75p = <b>£1.75</b>. (£76 comes from adding 1 + 50 + 20 + 5, "
                   "but the £1 coin is 100p, not 1p.)"))
    assert len(its) == 20, len(its)
    return {"title": "Money and measure problems", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grid_svg(37, cell=22)
    f_same = svg_wrap(400, 222, "".join([
        "".join("<rect x='%d' y='%d' width='18' height='180' fill='%s' stroke='%s' stroke-width='2'/>"
                % (6 + i * 18, 6, FILL if i < 3 else "#fff", LINE) for i in range(10)),
        text(96, 214, "3 tenths", 18),
        grid_body(30, 214, 6, 18),
        text(304, 214, "30 hundredths", 18),
    ]), "a tenths bar with 3 parts shaded and a hundred square with 30 squares shaded: the same amount")
    f_quarters = line_svg(0, 100, 4, labels=[0, 25, 50, 75, 100])
    f_chart = chart_svg(["34", "3.4", "0.34"], row_labels=["34", "÷ 10", "÷ 100"])
    f_round = line_svg(400, 500, 10, dot=460, labels=[400, 450, 500])
    return (
        "<h2>Tenths and hundredths</h2>"
        "<p>Divide 1 whole into <b>10 equal parts</b>: each part is one <b>tenth</b>, " + fr(1, 10) + " = 0.1. "
        "Divide it into <b>100 equal parts</b>: each part is one <b>hundredth</b>, " + fr(1, 100) + " = 0.01. "
        "Dividing one tenth by 10 also gives one hundredth.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>The whole square is 1. 3 full columns (3 tenths) and 7 more squares (7 hundredths) are shaded: "
        + fr(37, 100) + " = 0.37.</figcaption></figure>"
        "<p>The first place after the decimal point is <b>tenths</b>. The second place is <b>hundredths</b>. "
        "Use a 0 to hold an empty place: " + fr(7, 100) + " = 0.07, not 0.7.</p>"
        "<figure class='sn-fig'>" + f_same +
        "<figcaption>" + fr(3, 10) + " = " + fr(30, 100) + ", so 0.3 = 0.30. A 0 at the end does not change the value.</figcaption></figure>"
        "<h2>Halves and quarters as decimals</h2>"
        + table(["Fraction", "Hundredths", "Decimal"], [
            [fr(1, 4), fr(25, 100), "0.25"],
            [fr(1, 2), fr(50, 100), "0.5"],
            [fr(3, 4), fr(75, 100), "0.75"],
        ]) +
        "<figure class='sn-fig'>" + f_quarters +
        "<figcaption>Split 0 to 1 into 4 equal parts. Each part is " + fr(1, 4) + " = 0.25.</figcaption></figure>"
        + ex("Count in hundredths", "Count on from 0.37 in hundredths.",
             "0.37, 0.38, 0.39, then 10 hundredths make 1 tenth, so the next number is 0.40.",
             "0.38, 0.39, 0.40, 0.41")
        + "<h2>Dividing by 10 and 100</h2>"
        "<p>Dividing by 10 moves every digit <b>1 place to the right</b>. Dividing by 100 moves every digit "
        "<b>2 places to the right</b>. The decimal point stays where it is.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>34 ÷ 10 = 3.4 (3 ones and 4 tenths). 34 ÷ 100 = 0.34 (3 tenths and 4 hundredths).</figcaption></figure>"
        + ex("Example", "7 ÷ 100", "The 7 moves 2 places to the right, into the hundredths place. Put 0 in the ones and tenths places.", "0.07")
        + "<h2>Comparing and rounding</h2>"
        "<p>To compare decimals, look at the ones first, then the tenths, then the hundredths. "
        "0.45 &lt; 0.54, because 4 tenths &lt; 5 tenths.</p>"
        "<p>To round to the nearest whole number, look at the tenths digit. <b>5 or more</b>: round up. "
        "<b>4 or less</b>: round down.</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>4.6 is past the halfway mark (4.5), so it is nearer to 5. 4.6 rounds to 5.</figcaption></figure>"
        + ex("Example", "Round 4.5 to the nearest whole number.",
             "4.5 is exactly halfway between 4 and 5. Halfway always rounds up.", "5")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing " + fr(3, 10) + " as 0.03", "Tenths use one place: 0.3"],
            ["Writing " + fr(1, 4) + " as 0.4 or 1.4", fr(1, 4) + " = " + fr(25, 100) + " = 0.25"],
            ["34 ÷ 100 = 3.4", "÷ 100 moves digits 2 places: 0.34"],
            ["Counting 0.38, 0.39, 0.310", "10 hundredths make 1 tenth: 0.39, 0.40"],
            ["0.45 &gt; 0.54 because 5 &gt; 4 at the end", "Compare the tenths first: 4 &lt; 5, so 0.45 &lt; 0.54"],
            ["Rounding 4.5 down to 4", "Halfway rounds up: 5"],
        ])
    )


FAQ = [
    {"q": "What decimals do children learn in Year 4?",
     "a": "In Year 4 children learn tenths and hundredths: they write decimals like 0.3 and 0.37, learn that 1/4 = 0.25, 1/2 = 0.5 and 3/4 = 0.75, divide one- and two-digit numbers by 10 and 100, compare decimals and round numbers like 4.6 to the nearest whole number."},
    {"q": "How do you explain hundredths to a child?",
     "a": "Use a hundred square as 1 whole: each small square is one hundredth (0.01) and each column of 10 squares is one tenth (0.1). 37 shaded squares show 37 hundredths, which is 0.37."},
    {"q": "What happens when you divide a number by 10 or 100?",
     "a": "Dividing by 10 moves every digit one place to the right, and dividing by 100 moves every digit two places to the right. So 34 ÷ 10 = 3.4 and 34 ÷ 100 = 0.34."},
    {"q": "How do you round a decimal to the nearest whole number?",
     "a": "Look at the tenths digit. If it is 5 or more, round up; if it is 4 or less, round down. So 4.6 rounds to 5, 4.5 rounds to 5 and 4.3 rounds to 4."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred squares, number lines, place value charts) so labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4409)
    P = People(rnd)
    sets = [set_tenths_hundredths(), set_equivalents(), set_divide(), set_compare_round(P), set_problems(P)]
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
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "decimals", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals: Tenths and Hundredths",
        "seo_title": "Year 4 Decimals Worksheets: Tenths and Hundredths, Dividing by 10 and 100, Comparing and Rounding",
        "short_title": "Decimals",
        "domain": "Fractions (including decimals)",
        "standard_code": "Year 4: Fractions (including decimals)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count up and down in hundredths; recognise that hundredths arise when dividing an object by one hundred and dividing tenths by ten; recognise and write decimal equivalents of any number of tenths or hundredths; recognise and write decimal equivalents to 1/4, 1/2, 3/4; find the effect of dividing a one- or two-digit number by 10 and 100, identifying the value of the digits in the answer as ones, tenths and hundredths; round decimals with one decimal place to the nearest whole number; compare numbers with the same number of decimal places up to two decimal places.",
        "meta_desc": "Free Year 4 decimals worksheets for the National Curriculum: tenths and hundredths on a hundred square, 1/4 = 0.25, counting in hundredths, dividing by 10 and 100, comparing and rounding decimals, and money and measure problems. 100 maths questions with an answer key.",
        "key_big": "Tenths are the first place after the decimal point; hundredths are the second. 3/10 = 0.3 and 37/100 = 0.37.",
        "key_sub": "1/4 = 0.25, 1/2 = 0.5, 3/4 = 0.75. Dividing by 10 moves the digits 1 place right, by 100 two places: 34 ÷ 100 = 0.34. Round with the tenths digit: 4.5 rounds up to 5.",
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
