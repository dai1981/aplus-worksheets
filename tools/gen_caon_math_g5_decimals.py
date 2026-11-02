# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 5 Math: Decimals to Hundredths
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 5, Number, B1.5, B1.6 and B2.3)
  python3 tools/gen_caon_math_g5_decimals.py
Hundred grids, place value charts and number lines are drawn from whole numbers of hundredths (47 = 0.47).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Canadian English, dollars and cents with the cent sign (no pennies), metric units,
Ontario/SI number style (4536, 12 500 with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
NB = " "
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fb5"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def D(h):
    """Decimal text for h hundredths without trailing zeros: 30 -> '0.3', 27 -> '0.27', 100 -> '1'."""
    s = format((Dm(h) / 100).normalize(), "f")
    assert F(Dm(s)) == F(h, 100)
    return s


def V(s):
    return F(Dm(s.replace(NB, "")))


def r1(s):
    """Round a decimal string to the nearest tenth (half up), always with 1 decimal place."""
    return str(Dm(s).quantize(Dm("0.1"), rounding=ROUND_HALF_UP))


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢)?( .+)?$")


def val(c):
    """(value, unit) of a choice: '$0.45' and '45¢' are both 0.45 dollars. None for choices that are not one number."""
    c = c.replace(NB, "")
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), (m.group(3) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2))
    if m.group(1):
        return (v, "$")
    if m.group(3):
        return (v / 100, "$")
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (0.3 vs 0.30)."""
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


def fixed(q, choices, a, e):
    """Choices are picture labels (A, B, C, D): keep this order; the answer position is fixed."""
    assert len(set(choices)) == 4
    return {"q": q, "c": list(choices), "a": a, "e": e, "fix": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each).
    Items with fixed label order keep their position; the others fill the rest."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.get("fix"):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


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


def tw(t):
    return "1 tenth" if t == 1 else "%d tenths" % t


def hw(h):
    return "1 hundredth" if h == 1 else "%d hundredths" % h


# ------------------------------------------------------------ pictures
def grid_body(k, ox, oy, cell):
    """10 x 10 hundred grid at (ox, oy) with k squares shaded: full columns first, then down the next column."""
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
    return svg_wrap(w, w, grid_body(k, pad, pad, cell), "hundred grid with %s shaded" % squ(k))


def grids_svg(k, cell=14, gap=18):
    """k hundredths on as many hundred grids as needed, side by side (full grids first)."""
    n = (k + 99) // 100
    side = 10 * cell
    body = "".join(grid_body(min(100, k - 100 * i), 4 + i * (side + gap), 4, cell) for i in range(n))
    return svg_wrap(8 + n * side + (n - 1) * gap, side + 8, body,
                    "%d hundred grids with %s shaded in all" % (n, squ(k)))


def line_svg(a, b, spaces, labels=None, dots=(), W=420):
    """Number line from a to b hundredths with `spaces` equal spaces.
    labels: hundredths values written under the line (default both ends; must sit on a tick).
    dots: (value, letter or None). A dot may sit between ticks. Letters are written above their dot."""
    labels = labels if labels is not None else [a, b]
    lettered = any(l for _, l in dots)
    L, R = 30, W - 30
    Y = 46 if lettered else 30
    assert (b - a) % spaces == 0
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
        s.append(text(X(v), Y + 36, D(v), 17))
    xs = []
    for v, l in dots:
        assert a <= v <= b
        xs.append(X(v))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(v), Y, BLUE if l else RED))
        if l:
            s.append(text(X(v), Y - 20, l, 18))
    xs.sort()
    assert all(q - p >= 20 for p, q in zip(xs, xs[1:])), (a, b, dots)
    lab = "number line from %s to %s split into %d equal spaces" % (D(a), D(b), spaces)
    if lettered:
        lab += " with points %s" % ", ".join(l for _, l in dots)
    return svg_wrap(W, Y + 46, "".join(s), lab)


PV = [(2, "Hundreds"), (1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths")]


def chart_svg(rows, hi=None):
    """Place value chart: (Hundreds) | (Tens) | Ones | . | Tenths | Hundredths. hi: (row, place) drawn in red."""
    wl = max(len(r.partition(".")[0]) for r in rows)
    cols = PV[3 - wl:]
    CW, PW, HEAD, ROW = 100, 16, 30, 44
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
        assert len(f) <= 2, s
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


def grids_abcd_svg(ks, cell=8, gap=26):
    """Four hundred grids labelled A-D (k squares shaded in each)."""
    o = []
    side = 10 * cell
    for i, k in enumerate(ks):
        ox = 6 + i * (side + gap)
        o.append(text(ox + side / 2.0, 20, "ABCD"[i], 18))
        o.append(grid_body(k, ox, 28, cell))
    return svg_wrap(12 + 4 * side + 3 * gap, 28 + side + 6, "".join(o), "four hundred grids labelled A, B, C and D")


# ============================================================ set 1: hundredths with hundred grids
def grid_e(k):
    t, h = k // 10, k % 10
    if t == 0:
        return ("Each small square is 1 hundredth. %s shaded and there is no full column, so there are 0 tenths. "
                "%s = %s = <b>%s</b>. Write a 0 in the tenths place." % (
                    "1 square is" if k == 1 else "%d squares are" % k, hw(k), fr(k, 100), D(k)))
    if h == 0:
        return ("Each full column is 1 tenth. %d full columns are shaded: %s = %s = <b>%s</b> (or 0.%d0). "
                "0.0%d would be only %d small squares." % (t, tw(t), fr(t, 10), D(k), t, t, t))
    return ("Each full column is 1 tenth and each small square is 1 hundredth. <b>%d full %s</b> and <b>%s</b> are shaded: "
            "%s and %s = %s = <b>%s</b>." % (t, "column" if t == 1 else "columns", squ(h), tw(t), hw(h), fr(k, 100), D(k)))


def set_hundredths():
    its = []
    for k, wrong in [(34, ["3.4", "0.43", "34"]), (70, ["0.07", "7", "0.3"]), (9, ["0.9", "9", "0.91"]),
                     (85, ["8.5", "0.58", "0.15"])]:
        e = grid_e(k)
        if k in (9, 85):
            e += " %s is the part that is <b>not</b> shaded." % D(100 - k)
        if k == 70:
            e += " 0.3 is the part that is not shaded."
        its.append(mcq(fig(grid_svg(k)) + "The whole grid is 1. What decimal is shaded?", D(k), wrong, e))
    its.append(mcq(fig(grids_svg(136)) + "Each grid is 1 whole. What decimal is shaded?", "1.36", ["0.36", "13.6", "136"],
                   "One full grid is shaded: that is 1 whole. The second grid has 3 full columns and 6 squares: 36 hundredths. "
                   "1 and %s = <b>1.36</b>. 0.36 forgets the whole grid." % fr(36, 100)))
    its.append(mcq(fig(grids_svg(205)) + "Each grid is 1 whole. What decimal is shaded?", "2.05", ["2.5", "20.5", "0.25"],
                   "Two full grids are shaded: 2 wholes. The third grid has only 5 squares: 5 hundredths. "
                   "There are 0 tenths, so write a 0 in the tenths place: <b>2.05</b>. 2.5 would be 2 and 5 tenths (50 squares)."))
    its.append(mcq("1 whole is split into 100 equal parts. What decimal is each part?", "0.01", ["0.1", "1", "100"],
                   "Each part is %s of the whole, one <b>hundredth</b>: <b>0.01</b>. "
                   "0.1 is one tenth: 1 whole split into 10 parts." % fr(1, 100)))
    its.append(mcq("How many hundredths make <b>1 tenth</b>?", "10", ["100", "1", "0.1"],
                   "On a hundred grid, 1 column is 1 tenth and it has 10 small squares. So <b>10</b> hundredths = 1 tenth."))
    its.append(mcq("Write %s as a decimal." % fr(27, 100), "0.27", ["2.7", "27.1", "0.027"],
                   "%s is 27 hundredths: 2 tenths and 7 hundredths. The tenths digit is 2 and the hundredths digit is 7: <b>0.27</b>."
                   % fr(27, 100)))
    its.append(mcq("Write %s as a decimal." % fr(6, 100), "0.06", ["0.6", "6", "0.006"],
                   "%s is 6 hundredths. Hundredths need <b>two places</b> after the point, so write a 0 in the tenths place: "
                   "<b>0.06</b>. (0.6 would be 6 tenths.)" % fr(6, 100)))
    its.append(mcq("Write 3 %s as a decimal." % fr(45, 100), "3.45", ["3.045", "0.345", "34.5"],
                   "3 wholes, then the decimal point, then 45 hundredths (4 tenths and 5 hundredths): <b>3.45</b>."))
    its.append(mcq("Which fraction is equal to <b>0.08</b>?", fr(8, 100), [fr(8, 10), fr(1, 8), fr(100, 8)],
                   "0.08 has two digits after the point, so it means hundredths. The tenths digit is 0: "
                   "0.08 = 8 hundredths = <b>%s</b>. (%s is 0.8.)" % (fr(8, 100), fr(8, 10))))
    its.append(mcq("0.4 is the same as how many hundredths?", fr(40, 100), [fr(4, 100), fr(40, 10), fr(1, 4)],
                   "0.4 = 4 tenths. Each tenth is 10 hundredths, so 4 tenths = 40 hundredths = <b>%s</b>. "
                   "%s is only 0.04." % (fr(40, 100), fr(4, 100))))
    its.append(fixed(fig(grids_abcd_svg([4, 40, 14, 44])) + "Which hundred grid shows <b>0.04</b>?", ["A", "B", "C", "D"], 0,
                     "0.04 is 4 hundredths: only 4 small squares, with no full column. That is grid <b>A</b>. "
                     "B shows 0.4, C shows 0.14 and D shows 0.44."))
    its.append(mcq(fig(line_svg(30, 40, 10, dots=[(36, None)])) + "What decimal is at the red dot?", "0.36",
                   ["0.306", "0.6", "0.46"],
                   "From 0.3 to 0.4 there are <b>10 equal spaces</b>, so each space is 1 hundredth (0.01). "
                   "The dot is 6 spaces after 0.30: <b>0.36</b>."))
    its.append(mcq(fig(line_svg(100, 200, 10, dots=[(145, None)])) + "What decimal is at the red dot?", "1.45",
                   ["1.4", "1.5", "1.405"],
                   "Each space from 1 to 2 is 0.1. The dot is halfway between 1.4 and 1.5. "
                   "Halfway between 1.40 and 1.50 is <b>1.45</b>."))
    its.append(mcq("Count on in hundredths. What comes next?<br><b>2.97, 2.98, 2.99, ?</b>", "3.00", ["2.100", "2.910", "2.9"],
                   "2.99 + 0.01: 9 hundredths and 1 more make 10 hundredths, which is 1 more tenth. "
                   "Then 10 tenths make 1 more whole. So the next number is <b>3.00</b> (the same as 3). "
                   "There is no such step as 2.100."))
    its.append(mcq(fig(grid_svg(25)) + "%s of this grid is shaded. Which decimal is equal to %s?" % (fr(1, 4), fr(1, 4)),
                   "0.25", ["0.4", "0.14", "1.4"],
                   "%s of 100 squares is 25 squares. 25 squares = 25 hundredths = <b>0.25</b>. "
                   "0.4 just copies the 4 from the fraction." % fr(1, 4)))
    assert F(1, 4) == V("0.25")
    its.append(mcq("Which decimal is equal to %s?" % fr(2, 5), "0.4", ["0.25", "2.5", "0.04"],
                   "Make tenths: %s = %s (multiply the top and bottom by 2). 4 tenths = <b>0.4</b>. "
                   "0.25 just writes the 2 and the 5 after the point." % (fr(2, 5), fr(4, 10))))
    assert F(2, 5) == V("0.4")
    its.append(mcq("Priya colours 38 squares of a hundred grid blue and 27 squares green. "
                   "What decimal of the grid is <b>not</b> coloured?", "0.35", ["0.65", "0.45", "3.5"],
                   "38 + 27 = 65 squares are coloured. 100 − 65 = 35 squares are not coloured: <b>0.35</b>. "
                   "0.65 is the coloured part."))
    assert 1 - V("0.38") - V("0.27") == V("0.35")
    assert len(its) == 20, len(its)
    return {"title": "Hundredths with hundred grids", "items": its}


# ============================================================ set 2: place value
NAMES = {2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths"}


def set_place_value():
    its = []
    for s, place, wrong in [("4.36", -1, ["3 ones", "3 hundredths", "3 tens"]),
                            ("27.58", -2, ["8 tenths", "8 ones", "8 tens"]),
                            ("152.07", -2, ["7 tenths", "7 ones", "7 tens"]),
                            ("608.9", 2, ["6 tens", "6 ones", "6 tenths"])]:
        w, _, f = s.partition(".")
        dg = w[len(w) - 1 - place] if place >= 0 else f[-place - 1]
        right = "%s %s" % (dg, NAMES[place])
        pos = {2: "three places before the decimal point", -1: "in the <b>first</b> place after the decimal point",
               -2: "in the <b>second</b> place after the decimal point"}[place]
        e = "The red %s is %s, in the %s column. Its value is <b>%s</b>" % (dg, pos, NAMES[place], right)
        e += {2: " = %s00." % dg, -1: " = 0.%s." % dg, -2: " = 0.0%s." % dg}[place]
        if s == "152.07":
            e += " The 0 holds the tenths place."
        its.append(mcq(fig(chart_svg([s], hi=(0, place))) + "What is the value of the red digit in %s?" % s,
                       right, wrong, e, same_ok=True))
    for dg, s, place, right, wrong in [("5", "3.45", -2, "0.05", ["0.5", "5", "50"]),
                                       ("8", "18.6", 0, "8", ["0.8", "80", "0.08"]),
                                       ("9", "240.9", -1, "0.9", ["9", "0.09", "90"]),
                                       ("4", "431.25", 2, "400", ["4", "40", "0.4"])]:
        w, _, f = s.partition(".")
        where = {2: "the hundreds place (third place before the point)", 0: "the ones place, just before the point",
                 -1: "the tenths place, the first place after the point",
                 -2: "the hundredths place, the second place after the point"}[place]
        assert (w[len(w) - 1 - place] if place >= 0 else f[-place - 1]) == dg
        assert Dm(right) == Dm(dg) * Dm(10) ** place
        e = "In %s the %s is in %s. It is worth <b>%s</b>." % (s, dg, where, right)
        its.append(mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (dg, s), right, wrong, e))
    for s, place, right, wrong in [("58.17", "tenths", "1", ["7", "8", "5"]), ("906.34", "hundredths", "4", ["3", "6", "0"])]:
        w, _, f = s.partition(".")
        e = ("Read the places from the decimal point: tenths is the first digit after the point and hundredths is the second. "
             "In %s, the tenths digit is %s and the hundredths digit is %s. The answer is <b>%s</b>." % (s, f[0], f[1], right))
        its.append(mcq("In <b>%s</b>, which digit is in the <b>%s</b> place?" % (s, place), right, wrong, e))
    its.append(mcq("30 + 6 + 0.2 + 0.05 = ?", "36.25", ["3.625", "36.52", "362.5"],
                   "3 tens, 6 ones, 2 tenths and 5 hundredths: 3 6 . 2 5 = <b>36.25</b>."))
    assert 30 + 6 + V("0.2") + V("0.05") == V("36.25")
    its.append(mcq("7 + 0.09 = ?", "7.09", ["7.9", "0.79", "70.9"],
                   "There are no tenths, so write a 0 in the tenths place: 7 . 0 9 = <b>7.09</b>. "
                   "7.9 would be 7 ones and 9 tenths."))
    its.append(mcq("Which shows <b>46.83</b> in expanded form?", "40 + 6 + 0.8 + 0.03",
                   ["4 + 6 + 8 + 3", "40 + 6 + 0.08 + 0.3", "4 + 0.6 + 0.08 + 0.003"],
                   "4 tens, 6 ones, 8 tenths and 3 hundredths: <b>40 + 6 + 0.8 + 0.03</b>.", same_ok=True))
    assert 40 + 6 + V("0.8") + V("0.03") == V("46.83")
    its.append(mcq("Which decimal is <b>5 tens, 2 ones and 4 hundredths</b>?", "52.04", ["52.4", "5.24", "50.24"],
                   "5 tens and 2 ones make 52. There are 0 tenths, so write a 0 before the 4 hundredths: <b>52.04</b>."))
    its.append(mcq("Write <b>nine and twelve hundredths</b> as a decimal.", "9.12", ["9.012", "90.12", "0.912"],
                   "“Nine” is the whole number. “And” is the decimal point. Twelve hundredths = 0.12. "
                   "So the number is <b>9.12</b>."))
    its.append(mcq("How do you read <b>3.07</b>?", "three and seven hundredths",
                   ["three and seven tenths", "thirty-seven hundredths", "three hundred seven"],
                   "3 is the whole number. Say “and” for the decimal point. The 7 is in the hundredths place (0.07), "
                   "so read it as <b>three and seven hundredths</b>.", same_ok=True))
    its.append(mcq("How many hundredths are there in <b>0.8</b>?", "80", ["8", "800", "0.08"],
                   "1 tenth = 10 hundredths, so 8 tenths = <b>80</b> hundredths. 0.8 = 0.80."))
    its.append(mcq("How many tenths are there in <b>4.6</b>?", "46", ["6", "4", "460"],
                   "1 whole = 10 tenths, so 4 wholes = 40 tenths. 40 + 6 = <b>46</b> tenths. "
                   "(6 is only the digit in the tenths place.)"))
    its.append(mcq("0.58 = 4 tenths and ? hundredths", "18", ["8", "58", "1.8"],
                   "Take 1 of the 5 tenths and rename it as 10 hundredths: 10 + 8 = 18. "
                   "So 0.58 = 4 tenths and <b>18</b> hundredths (0.4 + 0.18 = 0.58)."))
    assert V("0.4") + V("0.18") == V("0.58")
    its.append(mcq("How many hundredths are there in <b>1.24</b>?", "124", ["24", "12.4", "1240"],
                   "1 whole = 100 hundredths. 100 + 24 = <b>124</b> hundredths. So 1.24 = %s." % fr(124, 100)))
    assert V("1.24") == F(124, 100)
    assert len(its) == 20, len(its)
    return {"title": "Place value: hundreds to hundredths", "items": its}


# ============================================================ set 3: compare and order
def cmp_item(x, y, e):
    a, b = V(x), V(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare the decimals.", right, wrong, e, same_ok=True)


def order_q(nums, how, right, wrong, e):
    vs = sorted((V(x) for x in nums), reverse=how.startswith("greatest"))
    assert [V(x) for x in right.split(", ")] == vs, right
    for w in wrong:
        assert sorted(w.split(", ")) == sorted(nums)
    return mcq("Order from <b>%s</b>: <b>%s</b>" % (how, ", ".join(nums)), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.62", "0.6", "0.6 = 0.60. Both have 6 tenths. Compare the hundredths: 2 &gt; 0. So <b>0.62 &gt; 0.6</b>."))
    its.append(cmp_item("0.5", "0.45", "Write 0.5 as 0.50 so both have hundredths. 50 hundredths &gt; 45 hundredths, "
                        "so <b>0.5 &gt; 0.45</b>. Do not compare 5 with 45: the 5 in 0.5 is 5 <b>tenths</b>."))
    its.append(cmp_item("3.08", "3.8", "Both have 3 ones. Compare the tenths: 3.08 has 0 tenths and 3.8 has 8 tenths. "
                        "So <b>3.08 &lt; 3.8</b>."))
    its.append(cmp_item("12.4", "9.87", "Compare the whole numbers first: 12 &gt; 9. So <b>12.4 &gt; 9.87</b>, "
                        "even though 9.87 has more digits."))
    its.append(cmp_item("7.30", "7.3", "A 0 at the <b>end</b> of a decimal does not change its value: 3 tenths = 30 hundredths. "
                        "So <b>7.30 = 7.3</b>."))
    its.append(cmp_item("0.09", "0.1", "Compare the tenths: 0.09 has 0 tenths and 0.1 has 1 tenth. "
                        "So <b>0.09 &lt; 0.1</b>, even though 9 &gt; 1."))
    its.append(mcq("Which number is <b>greater than 0.7</b>?", "0.71", ["0.69", "0.07", "0.65"],
                   "0.7 = 0.70. 0.71 is 71 hundredths, which is more than 70 hundredths. So <b>0.71</b> &gt; 0.7. "
                   "0.69 and 0.65 have only 6 tenths, and 0.07 has 0 tenths."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.8", ["0.79", "0.08", "0.75"],
                   "All have 0 ones. Compare the tenths: 8, 7, 0 and 7. <b>0.8</b> has the most tenths, "
                   "so it is the greatest, even though 0.79 has more digits."))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.38", ["0.4", "0.83", "0.5"],
                   "Compare the tenths: 0.38 has 3 tenths and the others have 4, 8 and 5. So <b>0.38</b> is the smallest."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "10.1", ["9.99", "10.09", "1.11"],
                   "9.99 and 1.11 are less than 10. Compare 10.1 and 10.09: 1 tenth &gt; 0 tenths. So <b>10.1</b> is the greatest."))
    its.append(mcq("Which number is <b>between 2.3 and 2.4</b>?", "2.35", ["2.53", "2.04", "3.25"],
                   "2.3 = 2.30 and 2.4 = 2.40. <b>2.35</b> is 2 and 35 hundredths, between 30 and 40 hundredths."))
    its.append(mcq("Which statement is <b>true</b>?", "0.4 &gt; 0.38",
                   ["0.4 &lt; 0.38", "0.15 &gt; 0.2", "0.06 &gt; 0.6"],
                   "0.4 = 0.40, and 40 hundredths &gt; 38 hundredths. So <b>0.4 &gt; 0.38</b> is true.", same_ok=True))
    its.append(mcq("Which decimal is <b>equal to 0.6</b>?", "0.60", ["0.06", "6.0", "0.16"],
                   "0.6 = 6 tenths = 60 hundredths = <b>0.60</b>. A 0 at the end does not change the value. "
                   "0.06 is only 6 hundredths."))
    its.append(fixed(fig(line_svg(0, 100, 10, labels=[0, 50, 100], dots=[(25, "A"), (45, "B"), (52, "C"), (80, "D")], W=500)) +
                     "Which letter shows <b>0.52</b>?", ["A", "B", "C", "D"], 2,
                     "Each space is 0.1. 0.52 is just after 0.5 (2 hundredths more). That is point <b>C</b>. "
                     "B is 0.45, just before 0.5, and A is 0.25 (the digits of 0.52 swapped)."))
    its.append(mcq("Which decimal is <b>less than 0.3</b>?", "0.29", ["0.31", "0.4", "0.33"],
                   "0.3 = 0.30. 0.29 is 29 hundredths, less than 30 hundredths. So <b>0.29</b> &lt; 0.3."))
    its.append(order_q(["0.5", "0.45", "0.4"], "smallest to greatest", "0.4, 0.45, 0.5",
                       ["0.4, 0.5, 0.45", "0.5, 0.45, 0.4", "0.45, 0.4, 0.5"],
                       "Write them with hundredths: 0.50, 0.45, 0.40. 40 &lt; 45 &lt; 50, so the order is <b>0.4, 0.45, 0.5</b>. "
                       "0.45 is not the biggest just because it has more digits."))
    its.append(order_q(["3.2", "3.02", "3.12"], "smallest to greatest", "3.02, 3.12, 3.2",
                       ["3.2, 3.12, 3.02", "3.02, 3.2, 3.12", "3.2, 3.02, 3.12"],
                       "All have 3 ones. Write them with hundredths: 3.20, 3.02, 3.12. 2 &lt; 12 &lt; 20 hundredths, so "
                       "<b>3.02, 3.12, 3.2</b>."))
    its.append(order_q(["1.9", "1.09", "1.19", "0.99"], "greatest to smallest", "1.9, 1.19, 1.09, 0.99",
                       ["1.19, 1.09, 1.9, 0.99", "0.99, 1.09, 1.19, 1.9", "1.9, 1.09, 1.19, 0.99"],
                       "0.99 is less than 1, so it is the smallest. Write the others with hundredths: 1.90, 1.09, 1.19. "
                       "Greatest first: <b>1.9, 1.19, 1.09, 0.99</b>. Careful: the question asks for greatest first."))
    its.append(order_q(["5.6", "5.06", "6.5", "5.65"], "smallest to greatest", "5.06, 5.6, 5.65, 6.5",
                       ["5.6, 5.65, 5.06, 6.5", "6.5, 5.65, 5.6, 5.06", "5.06, 5.65, 5.6, 6.5"],
                       "6.5 has 6 ones, so it is the greatest. The others have 5 ones: 5.06, 5.60, 5.65. "
                       "6 &lt; 60 &lt; 65 hundredths, so the order is <b>5.06, 5.6, 5.65, 6.5</b>."))
    its.append(mcq("Which digit can go in the box to make this true?<br><b>0.4□ &lt; 0.43</b>", "2", ["3", "5", "9"],
                   "Both numbers have 4 tenths, so compare the hundredths. The hundredths digit must be less than 3: "
                   "0.42 &lt; 0.43. So <b>2</b> works. With 3 the numbers are equal, and 5 or 9 make it greater."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 14, 11, 10, 9, 13, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare and order decimals", "items": its}


# ============================================================ set 4: round to the nearest tenth
def round_e(x):
    """Explanation for rounding the decimal string x (hundredths) to the nearest tenth."""
    lo = Dm(x).quantize(Dm("0.1"), rounding="ROUND_FLOOR")
    hi = lo + Dm("0.1")
    r = Dm(r1(x))
    h = int(x.partition(".")[2][1])
    s = ("%s is between %s and %s. Look at the hundredths digit: %d. %s, so round %s to <b>%s</b>."
         % (x, lo, hi, h, "5 or more" if h >= 5 else "4 or less", "up" if r > lo else "down", r))
    if r > lo and str(lo)[-1] == "9":
        s += " The tenths digit is 9, so 1 more tenth makes 10 tenths: that is 1 more whole."
    return s


def round_line(x):
    """Number line from the tenth below x to the tenth above, with hundredths ticks and a red dot at x."""
    h = int(Dm(x) * 100)
    lo = h // 10 * 10
    return fig(line_svg(lo, lo + 10, 10, labels=[lo, lo + 5, lo + 10], dots=[(h, None)]))


def rq(x, wrong, extra="", stem=None, fig_=False, unit=""):
    right = r1(x) + unit
    assert len(x.partition(".")[2]) == 2
    q = (round_line(x) if fig_ else "") + (stem or "Round <b>%s</b> to the nearest tenth." % x)
    return mcq(q, right, [w + unit for w in wrong], round_e(x) + extra)


def set_round():
    its = []
    its.append(rq("2.47", ["2.4", "3", "2"], " The dot is closer to 2.5 than to 2.4.", fig_=True,
                  stem="Round the number at the red dot (2.47) to the nearest tenth."))
    its.append(rq("6.13", ["6.2", "6", "7"], " The dot is closer to 6.1.", fig_=True,
                  stem="Round the number at the red dot (6.13) to the nearest tenth."))
    its.append(rq("0.85", ["0.8", "1", "0.85"], " 0.85 is exactly halfway. When the hundredths digit is 5, round up. 0.85 is not rounded yet: a number of tenths has only one decimal place.",
                  fig_=True, stem="Round the number at the red dot (0.85) to the nearest tenth."))
    its.append(rq("3.96", ["3.9", "3.10", "3"], " The answer 4.0 shows it is rounded to tenths. "
                  "3.10 is wrong: 10 tenths are not written in one place.", fig_=True,
                  stem="Round the number at the red dot (3.96) to the nearest tenth."))
    its.append(rq("5.32", ["5.4", "5", "6"], " 5.4 rounds the wrong way, and 5 rounds to the nearest whole number."))
    its.append(rq("8.75", ["8.7", "9", "8"], " 9 rounds to the nearest whole number instead of the nearest tenth."))
    its.append(rq("0.64", ["0.7", "1", "0"], " 0.7 rounds the wrong way. 0 and 1 are whole numbers, not tenths."))
    its.append(rq("12.08", ["12.0", "12.8", "13"], " 12.0 just drops the 8. 12.8 moves the 8 into the tenths place."))
    its.append(rq("1.98", ["1.9", "1.10", "1"], " The answer is written 2.0 to show tenths. 1.9 just drops the 8."))
    its.append(rq("26.45", ["26.4", "27", "26"], " 26.4 drops the 5, but a 5 rounds up."))
    its.append(mcq("Round <b>3.6</b> to the nearest tenth.", "3.6", ["4", "3.7", "3.5"],
                   "3.6 has only tenths. It is already a number of tenths, so it stays <b>3.6</b>. "
                   "Rounding to the nearest whole number would give 4."))
    its.append(mcq("Which number rounds to <b>4.3</b> when you round to the nearest tenth?", "4.26", ["4.36", "4.21", "4.35"],
                   "Numbers from 4.25 up to 4.34 round to 4.3. 4.26 rounds up to <b>4.3</b>. "
                   "4.21 rounds down to 4.2, and 4.35 and 4.36 round up to 4.4."))
    assert r1("4.26") == "4.3" and r1("4.36") == "4.4" and r1("4.21") == "4.2" and r1("4.35") == "4.4"
    its.append(mcq("Which number does <b>not</b> round to 0.8 when you round to the nearest tenth?", "0.86",
                   ["0.79", "0.81", "0.75"],
                   "0.75 and 0.79 round up to 0.8, and 0.81 rounds down to 0.8. "
                   "<b>0.86</b> has 6 hundredths, so it rounds up to 0.9."))
    assert [r1(x) for x in ("0.79", "0.81", "0.75", "0.86")] == ["0.8", "0.8", "0.8", "0.9"]
    its.append(mcq("To round <b>7.48</b> to the nearest tenth, which digit do you look at?", "the 8 (hundredths)",
                   ["the 4 (tenths)", "the 7 (ones)", "all of the digits"],
                   "To round to the nearest tenth, look one place to the right of the tenths: the hundredths digit. "
                   "It is <b>8</b>, so 7.48 rounds up to 7.5.", same_ok=True))
    assert r1("7.48") == "7.5"
    its.append(mcq("What is the <b>smallest</b> number with two decimal places that rounds to 2.6?", "2.55",
                   ["2.51", "2.59", "2.65"],
                   "Numbers from 2.55 up to 2.64 round to 2.6. The smallest one is <b>2.55</b>. "
                   "2.51 rounds to 2.5, and 2.65 rounds to 2.7. 2.59 rounds to 2.6, but it is not the smallest."))
    assert r1("2.55") == "2.6" and r1("2.54") == "2.5" and r1("2.65") == "2.7"
    its.append(rq("3.46", ["3.4", "3", "4"], " Answer: about 3.5 km.", unit=" km",
                  stem="At the Terry Fox Run, Noah runs 3.46 km. How far is that to the nearest tenth of a kilometre?"))
    its.append(rq("6.83", ["6.9", "7", "6"], " Answer: about 6.8 kg.", unit=" kg",
                  stem="A pumpkin at the fall fair has a mass of 6.83 kg. What is its mass to the nearest tenth of a kilogram?"))
    its.append(rq("12.95", ["12.9", "12.10", "12"], " Answer: 13.0 cm. 12.10 cm is wrong: 10 tenths make 1 whole.", unit=" cm",
                  stem="On a snow day in Ottawa, 12.95 cm of snow falls. What is this to the nearest tenth of a centimetre?"))
    its.append(rq("41.37", ["41.3", "41", "42"], " Answer: 41.4 seconds.", unit=" seconds",
                  stem="At a swim meet, Owen swims 50 m in 41.37 seconds. What is his time to the nearest tenth of a second?"))
    its.append(mcq("A notebook at the school store costs $3.84. What is the price to the nearest tenth of a dollar (the nearest 10¢)?",
                   "$3.80", ["$3.90", "$4.00", "$3.00"],
                   "A tenth of a dollar is 10¢. $3.84 is between $3.80 and $3.90. The hundredths digit is 4: "
                   "4 or less, so round down to <b>$3.80</b>. $4.00 rounds to the nearest dollar."))
    assert r1("3.84") == "3.8"
    assert len(its) == 20, len(its)
    return {"title": "Round decimals to the nearest tenth", "items": its}


# ============================================================ set 5: × 0.1 and × 0.01, word problems
def mul_e(n, m, res):
    if m == "0.1":
        return ("× 0.1 is the same as ÷ 10: take 1 tenth of the number. Each digit moves <b>one</b> place to the right. "
                "%s × 0.1 = %s ÷ 10 = <b>%s</b>." % (n, n, res))
    return ("× 0.01 is the same as ÷ 100: take 1 hundredth of the number. Each digit moves <b>two</b> places to the right. "
            "%s × 0.01 = %s ÷ 100 = <b>%s</b>." % (n, n, res))


def mq(n, m, wrong, extra=""):
    res = Dm(n) * Dm(m)
    res = format(res.normalize(), "f")
    assert V(res) == F(n) * V(m)
    return mcq("%s × %s = ?" % (n, m), res, wrong, mul_e(n, m, res) + extra)


def set_problems():
    its = []
    its.append(mq("7", "0.1", ["70", "0.07", "7.1"], " 70 is 7 × 10: multiplying by 0.1 makes the number smaller."))
    its.append(mq("45", "0.1", ["450", "0.45", "45.1"], " 0.45 moves the digits two places: that is 45 × 0.01."))
    its.append(mq("8", "0.01", ["0.8", "800", "8.01"], " 0.8 moves the digit only one place: that is 8 × 0.1."))
    its.append(mq("36", "0.01", ["3.6", "3600", "36.01"], " 3.6 is 36 × 0.1, not 36 × 0.01."))
    its.append(mq("250", "0.1", ["2500", "2.5", "250.1"], ""))
    its.append(mq("125", "0.01", ["12.5", "12" + NB + "500", "0.125"], ""))
    its.append(mcq("Which gives the same answer as <b>63 × 0.1</b>?", "63 ÷ 10", ["63 × 10", "63 ÷ 100", "63 × 100"],
                   "0.1 is 1 tenth, so 63 × 0.1 means 1 tenth of 63. That is <b>63 ÷ 10</b> = 6.3.", same_ok=True))
    its.append(mcq("64 ÷ 100 = ?", "0.64", ["6.4", "6400", "0.064"],
                   "÷ 100 is the same as × 0.01. Each digit moves <b>two</b> places to the right: 64 ÷ 100 = <b>0.64</b>. "
                   "6.4 is 64 ÷ 10."))
    assert Dm(64) / 100 == Dm("0.64")
    its.append(mcq("? × 0.1 = 3.8", "38", ["380", "0.38", "3800"],
                   "× 0.1 moves each digit one place to the right. Go back: move the digits of 3.8 one place to the left. "
                   "<b>38</b> × 0.1 = 3.8."))
    assert 38 * V("0.1") == V("3.8")
    its.append(mcq("Liam says 30 × 0.1 = 300 because multiplying always makes a number bigger. What is 30 × 0.1?",
                   "3", ["300", "0.3", "30.1"],
                   "Multiplying by a number less than 1 makes a number <b>smaller</b>. 30 × 0.1 = 30 ÷ 10 = <b>3</b>. "
                   "300 is 30 × 10."))
    assert 30 * V("0.1") == 3
    # word problems
    its.append(mcq("A dime is worth $0.10. Maya has 46 dimes. How much money does she have?", "$4.60",
                   ["$46", "$0.46", "$460"],
                   "46 × $0.10 = 46 × 0.1 = 4.6. So she has <b>$4.60</b>. (10 dimes make $1, so 40 dimes make $4.)"))
    assert 46 * V("0.1") == V("4.60")
    its.append(mcq("1 cm = 0.01 m. A canoe paddle is 152 cm long. How long is it in metres?", "1.52 m",
                   ["15.2 m", "0.152 m", "152 m"],
                   "152 × 0.01 = 152 ÷ 100 = 1.52. The paddle is <b>1.52 m</b> long. 15.2 m would be longer than a canoe."))
    assert 152 * V("0.01") == V("1.52")
    its.append(mcq("1 mm = 0.1 cm. A ladybug is 7 mm long. How long is it in centimetres?", "0.7 cm",
                   ["70 cm", "0.07 cm", "7 cm"],
                   "7 × 0.1 = 7 ÷ 10 = 0.7. The ladybug is <b>0.7 cm</b> long, less than 1 cm."))
    its.append(mcq("1¢ = $0.01. Arjun saved 385¢ in his piggy bank. How many dollars is that?", "$3.85",
                   ["$38.50", "$0.385", "$385"],
                   "385 × 0.01 = 385 ÷ 100 = 3.85. So 385¢ = <b>$3.85</b>. (100¢ = $1, so 300¢ = $3.)"))
    assert 385 * V("0.01") == V("3.85")
    its.append(mcq("There are 240 students at Maple Grove School. 0.1 of them take the bus. How many students take the bus?",
                   "24 students", ["2400 students", "2.4 students", "240 students"],
                   "0.1 of 240 means 240 × 0.1 = 240 ÷ 10 = <b>24 students</b>."))
    assert 240 * V("0.1") == 24
    its.append(mcq("A box of 100 maple leaf cookies has a mass of 1250 g. All the cookies have the same mass. "
                   "What is the mass of one cookie?", "12.5 g", ["125 g", "1.25 g", "0.125 g"],
                   "Share 1250 g among 100 cookies: 1250 ÷ 100 = 1250 × 0.01 = <b>12.5 g</b>. "
                   "125 g is 1250 ÷ 10."))
    assert Dm(1250) / 100 == Dm("12.5")
    its.append(mcq("10 friends share the cost of a $65 pizza party equally. How much does each friend pay?", "$6.50",
                   ["$0.65", "$650", "$6.05"],
                   "65 ÷ 10 = 65 × 0.1 = 6.5. Each friend pays <b>$6.50</b>. "
                   "$6.05 is wrong: 6.5 has 5 tenths, which is 50¢."))
    assert Dm(65) / 10 == Dm("6.50")
    its.append(mcq("Kai’s canoe trip is 18 km long. He has paddled 0.1 of the trip. How far has he paddled?", "1.8 km",
                   ["180 km", "0.18 km", "17.9 km"],
                   "0.1 of 18 km = 18 × 0.1 = 18 ÷ 10 = <b>1.8 km</b>. 17.9 km subtracts 0.1 instead of multiplying."))
    assert 18 * V("0.1") == V("1.8")
    its.append(mcq("Zoe’s class collects 900 cans for the food drive. 0.01 of the cans are soup. How many cans of soup are there?",
                   "9 cans", ["90 cans", "0.9 cans", "9000 cans"],
                   "0.01 of 900 means 900 × 0.01 = 900 ÷ 100 = <b>9 cans</b>. 90 cans is 900 × 0.1."))
    assert 900 * V("0.01") == 9
    its.append(mcq("Jayden has 48 dimes. Leah has 480¢ in nickels. Who has more money?", "They have the same amount",
                   ["Jayden", "Leah", "You can’t tell"],
                   "Jayden: 48 × $0.10 = 48 × 0.1 = $4.80. Leah: 480¢ = 480 × 0.01 = $4.80. "
                   "<b>They have the same amount</b>.", same_ok=True))
    assert 48 * V("0.1") == 480 * V("0.01")
    assert len(its) == 20, len(its)
    return {"title": "× 0.1, × 0.01, ÷ 10 and ÷ 100 with word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_grid = grids_svg(136, cell=16)
    f_chart = chart_svg(["46.83"])
    f_cmp = svg_wrap(452, 222, "".join([
        grid_body(50, 6, 6, 18), text(96, 214, "0.5 = 0.50", 18),
        grid_body(45, 266, 6, 18), text(356, 214, "0.45", 18),
    ]), "two hundred grids: 50 squares shaded for 0.5 and 45 squares shaded for 0.45")
    f_round = line_svg(240, 250, 10, labels=[240, 245, 250], dots=[(247, None)])
    return (
        "<h2>Tenths and hundredths</h2>"
        "<p>Split 1 whole into <b>100 equal parts</b>. Each part is one <b>hundredth</b>: " + fr(1, 100) + " = 0.01. "
        "One column of 10 parts is one <b>tenth</b>: " + fr(1, 10) + " = 0.1. "
        "Tenths go in the <b>first place</b> after the decimal point, and hundredths go in the <b>second place</b>.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>Each grid is 1 whole. 1 full grid and 36 squares are shaded: 1 and " + fr(36, 100) + " = 1.36."
        "</figcaption></figure>"
        "<h2>Place value</h2>"
        "<p>Each place is worth 10 times the place to its right. Use a 0 to hold an empty place: " + fr(7, 100) + " = 0.07.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>46.83 = 4 tens, 6 ones, 8 tenths and 3 hundredths = 40 + 6 + 0.8 + 0.03.</figcaption></figure>"
        + ex("Example 1", "Write " + fr(8, 100) + " as a decimal.",
             "8 hundredths. There are 0 tenths, so put a 0 in the tenths place.", "0.08")
        + "<h2>Comparing and ordering</h2>"
        "<p>Compare the whole numbers first, then the tenths, then the hundredths. "
        "It helps to give both numbers the same number of places: 0.5 = 0.50.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.5 = 50 hundredths and 0.45 = 45 hundredths. So 0.5 &gt; 0.45, even though 45 is more than 5."
        "</figcaption></figure>"
        + ex("Example 2", "Order 0.5, 0.45 and 0.4 from smallest to greatest.",
             "Write them with hundredths: 0.50, 0.45, 0.40.", "0.4, 0.45, 0.5")
        + "<h2>Rounding to the nearest tenth</h2>"
        "<p>Find the two tenths the number is between. Look at the <b>hundredths</b> digit: "
        "5 or more rounds up, 4 or less rounds down.</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>2.47 is between 2.4 and 2.5. The hundredths digit is 7, so 2.47 rounds up to 2.5.</figcaption></figure>"
        + ex("Example 3", "Round 3.96 to the nearest tenth.",
             "3.96 is between 3.9 and 4.0. The hundredths digit is 6, so round up. 10 tenths make 1 whole.", "4.0")
        + "<h2>Multiplying by 0.1 and 0.01</h2>"
        "<p>× 0.1 is the same as ÷ 10: each digit moves <b>one</b> place to the right. "
        "× 0.01 is the same as ÷ 100: each digit moves <b>two</b> places to the right. "
        "Multiplying by 0.1 or 0.01 makes a number smaller.</p>"
        + table(["Number", "× 0.1 (÷ 10)", "× 0.01 (÷ 100)"], [
            ["45", "4.5", "0.45"], ["250", "25", "2.5"], ["8", "0.8", "0.08"]])
        + ex("Example 4", "A dime is $0.10. How much are 46 dimes worth?",
             "46 × 0.1 = 46 ÷ 10 = 4.6.", "$4.60")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because 45 &gt; 5", "Use the same places: 0.45 &lt; 0.50"],
            ["Writing " + fr(7, 100) + " as 0.7", "Hundredths need two places: 0.07"],
            ["Rounding 2.47 to 2.4 by dropping the 7", "Look at the hundredths digit: 7 rounds up to 2.5"],
            ["Rounding to the wrong place: 8.75 → 9", "Nearest tenth keeps one decimal place: 8.8"],
            ["45 × 0.1 = 450", "× 0.1 makes it smaller: 45 × 0.1 = 4.5"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about decimals in Ontario?",
     "a": "In the Ontario Grade 5 math curriculum, students read, represent, compare and order decimals to hundredths, round decimals to the nearest tenth, and multiply whole numbers by 0.1 and 0.01 using mental math."},
    {"q": "How do you round a decimal to the nearest tenth?",
     "a": "Find the two tenths the number is between and look at the hundredths digit. If it is 5 or more, round up; if it is 4 or less, round down, so 2.47 rounds to 2.5 and 6.13 rounds to 6.1."},
    {"q": "Why is 0.5 bigger than 0.45?",
     "a": "The 5 in 0.5 means 5 tenths, which is 50 hundredths. 0.45 is only 45 hundredths, so 0.5 is bigger even though it has fewer digits."},
    {"q": "How do you multiply by 0.1 and 0.01 in your head?",
     "a": "Multiplying by 0.1 is the same as dividing by 10, so each digit moves one place to the right: 45 × 0.1 = 4.5. Multiplying by 0.01 is the same as dividing by 100: 45 × 0.01 = 0.45."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (12 500) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        s["title"] = nbsp(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines, place value charts, hundred grids)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45807)
    sets = [set_hundredths(), set_place_value(), set_compare(), set_round(), set_problems()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "decimals-to-hundredths", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals to Hundredths: Compare, Order, Round and Multiply by 0.1",
        "seo_title": "Grade 5 Decimals to Hundredths Worksheets: Compare, Round, × 0.1 and × 0.01 (Free, Answer Key)",
        "short_title": "Decimals to hundredths",
        "domain": "Number",
        "standard_code": "Grade 5: B1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compare, and order decimal numbers up to hundredths, in various contexts",
        "meta_desc": "Free Grade 5 math worksheets on decimals to hundredths for the Ontario curriculum: hundred grids, place value, comparing and ordering decimals, rounding to the nearest tenth, and multiplying by 0.1 and 0.01. 100 questions with an answer key.",
        "key_big": "Tenths are the first place after the decimal point; hundredths are the second. 0.5 = 0.50 > 0.45.",
        "key_sub": "To round to the nearest tenth, look at the hundredths digit: 5 or more rounds up (2.47 → 2.5). × 0.1 is ÷ 10 and × 0.01 is ÷ 100, so 45 × 0.1 = 4.5 and 45 × 0.01 = 0.45.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "(number line|place value chart|hundred grid|[0-9] hundred grids|four hundred grids)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
