# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Decimals - tenths and hundredths (Australian Curriculum v9.0, AC9M4N01)
  python3 tools/gen_au_maths_y4_decimals.py
Tenth strips, hundred squares, place value charts and number lines are drawn from whole numbers of hundredths (47 = 0.47).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Australian English, dollars and cents (5c is the smallest coin), metric units.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
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
    return F(Dm(s))


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(c)?( .+)?$")


def val(c):
    """(value, unit) of a choice: '$0.45' and '45c' are both 0.45 dollars. None for choices that are not one number."""
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
    """10 x 10 hundred square at (ox, oy) with k squares shaded: full columns first, then down the next column."""
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


def strip_body(k, ox, oy, W=300, H=40):
    s = []
    for i in range(10):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (ox + i * W // 10, oy, W // 10, H, FILL if i < k else "#fff", LINE))
    return "".join(s)


def strips_svg(t, W=300, H=40, gap=12):
    """Tenth strips: each strip is 1 whole split into 10 equal parts; t tenths shaded in total (full strips first)."""
    n = max(1, (t + 9) // 10)
    body = "".join(strip_body(min(10, t - 10 * i), 6, 6 + i * (H + gap), W, H) for i in range(n))
    return svg_wrap(W + 12, n * H + (n - 1) * gap + 12, body,
                    "tenth strip%s split into 10 equal parts with %d parts shaded" % ("s" if n > 1 else "", t))


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


PV = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths")]


def chart_svg(rows, hi=None):
    """Place value chart: (Tens) | Ones | . | Tenths | Hundredths. hi: (row, place) drawn in red."""
    tens = any(len(r.partition(".")[0]) > 1 for r in rows)
    cols = PV if tens else PV[1:]
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
        assert len(w) <= (2 if tens else 1) and len(f) <= 2, s
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
    # tenth strips
    for k, wrong in [(3, ["0.03", "3.10", "0.7"]), (7, ["0.07", "7.10", "0.3"])]:
        e = ("The strip is 1 whole split into 10 equal parts, so each part is 1 tenth. %d parts are shaded: "
             "%s = <b>%s</b>. Tenths go in the <b>first</b> place after the decimal point (not %s)."
             % (k, fr(k, 10), D(k * 10), "0.0%d" % k))
        its.append(mcq(fig(strips_svg(k)) + "Each strip is 1 whole. What decimal is shaded?", D(k * 10), wrong, e))
    its.append(mcq(fig(strips_svg(14)) + "Each strip is 1 whole. What decimal is shaded?", "1.4", ["0.14", "14", "1.04"],
                   "One whole strip is shaded (1) and 4 tenths of the second strip: 1 and %s = <b>1.4</b>. "
                   "0.14 would be only 14 hundredths." % fr(4, 10)))
    # hundred squares
    for k, wrong in [(40, ["0.04", "4", "0.6"]), (27, ["2.7", "27", "0.73"]), (58, ["5.8", "0.85", "58"]),
                     (6, ["0.6", "6", "0.94"]), (91, ["9.1", "0.19", "91"]), (3, ["0.3", "3", "0.97"])]:
        t, h = k // 10, k % 10
        if t == 0:
            e = ("Each small square is 1 hundredth. %s shaded and there is no full column, so there are 0 tenths. "
                 "%s = %s = <b>%s</b>. Write a 0 in the tenths place." % (
                     "1 square is" if k == 1 else "%d squares are" % k, hw(k), fr(k, 100), D(k)))
        elif h == 0:
            e = ("Each full column is 1 tenth. %d full columns are shaded: %s = %s = <b>%s</b> (or 0.%d0). "
                 "0.0%d would be only %d small squares." % (t, tw(t), fr(t, 10), D(k), t, t, t))
        else:
            e = ("Each full column is 1 tenth and each small square is 1 hundredth. <b>%d full %s</b> and <b>%s</b> are shaded: "
                 "%s and %s = %s = <b>%s</b>." % (t, "column" if t == 1 else "columns", squ(h), tw(t), hw(h), fr(k, 100), D(k)))
        its.append(mcq(fig(grid_svg(k)) + "The whole square is 1. What decimal is shaded?", D(k), wrong, e))
    # fraction -> decimal
    for n, d, wrong in [(3, 10, ["0.03", "3.10", "3.0"]), (9, 10, ["0.09", "9.10", "0.1"]),
                        (27, 100, ["2.7", "27.100", "0.027"]), (8, 100, ["0.8", "8.100", "8.0"]),
                        (50, 100, ["0.05", "5", "50"])]:
        right = D(n * 100 // d)
        assert V(right) == F(n, d)
        if d == 10:
            e = "%s is %s. Tenths go in the <b>first</b> place after the decimal point: <b>%s</b>." % (fr(n, d), tw(n), right)
        elif n < 10:
            e = ("%s is %s. Hundredths need <b>two places</b> after the point, so write a 0 in the tenths place: <b>%s</b>. "
                 "(0.%d would be %s.)" % (fr(n, d), hw(n), right, n, tw(n)))
        elif n % 10 == 0:
            e = ("%s is %d hundredths, which is the same as %s: <b>%s</b> (or 0.50). "
                 "0.05 would be only 5 hundredths." % (fr(n, d), n, tw(n // 10), right))
        else:
            e = ("%s is %d hundredths: %s and %s. The tenths digit is %d and the hundredths digit is %d: <b>%s</b>."
                 % (fr(n, d), n, tw(n // 10), hw(n % 10), n // 10, n % 10, right))
        its.append(mcq("Write %s as a decimal." % fr(n, d), right, wrong, e))
    # decimal -> fraction
    its.append(mcq("Which fraction is equal to <b>0.3</b>?", fr(3, 10), [fr(1, 3), fr(3, 100), fr(30, 10)],
                   "0.3 has one digit after the point, so it means tenths: 3 tenths = <b>%s</b>. "
                   "It is <b>not</b> %s: 0.3 is 3 out of 10 equal parts, not 1 out of 3." % (fr(3, 10), fr(1, 3))))
    its.append(mcq("Which fraction is equal to <b>0.07</b>?", fr(7, 100), [fr(7, 10), fr(1, 7), fr(7, 1000)],
                   "0.07 has two digits after the point, so it means hundredths. The tenths digit is 0: "
                   "0.07 = 7 hundredths = <b>%s</b>. (%s is 0.7.)" % (fr(7, 100), fr(7, 10))))
    its.append(mcq("Which fraction is equal to <b>0.45</b>?", fr(45, 100), [fr(45, 10), fr(4, 5), fr(1, 45)],
                   "Two digits after the point means hundredths: 0.45 = 45 hundredths = <b>%s</b>." % fr(45, 100)))
    # words
    its.append(mcq("Which decimal is <b>6 tenths and 2 hundredths</b>?", "0.62", ["6.2", "0.26", "62"],
                   "Tenths go in the first place after the point and hundredths in the second: <b>0.62</b>."))
    its.append(mcq("Which decimal is <b>3 ones and 4 hundredths</b>?", "3.04", ["3.4", "0.34", "34"],
                   "3 ones, then the point. There are 0 tenths, so write a 0 before the 4 hundredths: <b>3.04</b>. "
                   "(3.4 would be 3 ones and 4 tenths.)"))
    its.append(mcq("1 whole is split into 100 equal parts. What decimal is each part?", "0.01", ["0.1", "1", "100"],
                   "Each part is %s of the whole, one <b>hundredth</b>: <b>0.01</b>. "
                   "0.1 is one tenth: 1 whole split into 10 parts." % fr(1, 100)))
    order = [0, 1, 3, 4, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Tenths and hundredths: pictures and fractions", "items": its}


# ============================================================ set 2: place value
def set_place_value():
    its = []
    for s, place, wrong in [("4.37", -1, ["3 ones", "3 hundredths", "3 tens"]),
                            ("2.58", -2, ["8 tenths", "8 ones", "8 tens"]),
                            ("6.09", -2, ["9 tenths", "9 ones", "9 tens"]),
                            ("15.6", 0, ["5 tens", "5 tenths", "5 hundredths"])]:
        w, _, f = s.partition(".")
        dg = w[-1] if place == 0 else f[-place - 1]
        name = {0: "ones", -1: "tenths", -2: "hundredths"}[place]
        pos = {0: "just before the decimal point", -1: "in the <b>first</b> place after the decimal point",
               -2: "in the <b>second</b> place after the decimal point"}[place]
        right = "%s %s" % (dg, name)
        e = "The red %s is %s, in the %s column. Its value is <b>%s</b>" % (dg, pos, name, right)
        e += {0: ".", -1: " = 0.%s." % dg, -2: " = 0.0%s." % dg}[place]
        if s == "6.09":
            e += " The 0 holds the tenths place."
        its.append(mcq(fig(chart_svg([s], hi=(0, place))) + "What is the value of the red digit in %s?" % s,
                       right, wrong, e, same_ok=True))
    for dg, s, right, wrong in [("7", "3.72", "0.7", ["7", "0.07", "70"]), ("4", "8.14", "0.04", ["0.4", "4", "40"]),
                                ("6", "6.25", "6", ["0.6", "0.06", "60"]), ("9", "12.9", "0.9", ["9", "0.09", "90"])]:
        w, _, f = s.partition(".")
        if dg in w:
            where = "before the decimal point, in the ones place"
        elif f[0] == dg:
            where = "in the first place after the point, the tenths place"
        else:
            where = "in the second place after the point, the hundredths place"
        e = "In %s the %s is %s. It is worth <b>%s</b>." % (s, dg, where, right)
        its.append(mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (dg, s), right, wrong, e))
    for s, place, right, wrong in [("19.25", "tenths", "2", ["5", "9", "1"]), ("47.36", "hundredths", "6", ["3", "7", "4"]),
                                   ("30.48", "ones", "0", ["3", "4", "8"])]:
        w, _, f = s.partition(".")
        e = ("%s: tens %s, ones %s, then the point, tenths %s, hundredths %s. The %s digit is <b>%s</b>."
             % (s, w[0], w[1], f[0], f[1], place, right))
        its.append(mcq("In <b>%s</b>, which digit is in the <b>%s</b> place?" % (s, place), right, wrong, e))
    its.append(mcq("4 + 0.6 + 0.03 = ?", "4.63", ["4.36", "46.3", "0.463"],
                   "4 ones, 6 tenths and 3 hundredths: 4 . 6 3 = <b>4.63</b>."))
    its.append(mcq("2 + 0.08 = ?", "2.08", ["2.8", "0.28", "20.8"],
                   "There are no tenths, so write a 0 in the tenths place: 2 . 0 8 = <b>2.08</b>. "
                   "2.8 would be 2 ones and 8 tenths."))
    its.append(mcq("Which shows <b>5.29</b> in expanded form?", "5 + 0.2 + 0.09",
                   ["5 + 2 + 9", "5 + 0.02 + 0.9", "5 + 0.2 + 0.9"],
                   "5 ones, 2 tenths and 9 hundredths: <b>5 + 0.2 + 0.09</b>.", same_ok=True))
    its.append(mcq("Which decimal is <b>3 tens, 1 one and 6 hundredths</b>?", "31.06", ["31.6", "3.16", "30.16"],
                   "3 tens and 1 one make 31. There are 0 tenths, so write a 0 before the 6 hundredths: <b>31.06</b>."))
    its.append(mcq("How many hundredths are there in <b>0.6</b>?", "60", ["6", "600", "0.06"],
                   "1 tenth = 10 hundredths, so 6 tenths = <b>60</b> hundredths. 0.6 = 0.60."))
    its.append(mcq("How many hundredths are there in <b>0.35</b>?", "35", ["5", "3", "350"],
                   "0.35 = 3 tenths and 5 hundredths. 3 tenths = 30 hundredths, and 30 + 5 = <b>35</b> hundredths. "
                   "So 0.35 = %s." % fr(35, 100)))
    its.append(mcq("How many tenths are there in <b>2.4</b>?", "24", ["4", "2", "240"],
                   "1 whole = 10 tenths, so 2 wholes = 20 tenths. 20 + 4 = <b>24</b> tenths. "
                   "(4 is only the digit in the tenths place.)"))
    its.append(mcq("0.73 = 7 tenths and ? hundredths", "3", ["73", "30", "0.3"],
                   "0.73 = 0.7 + 0.03. So 0.73 = 7 tenths and <b>3</b> hundredths."))
    its.append(mcq("0.73 = 6 tenths and ? hundredths", "13", ["3", "1.3", "23"],
                   "Take 1 of the 7 tenths and rename it as 10 hundredths: 10 + 3 = 13. "
                   "So 0.73 = 6 tenths and <b>13</b> hundredths (0.6 + 0.13 = 0.73)."))
    assert V("0.6") + V("0.13") == V("0.73")
    assert len(its) == 20, len(its)
    return {"title": "Place value: ones, tenths and hundredths", "items": its}


# ============================================================ set 3: compare and order
def cmp_item(x, y, e):
    a, b = V(x), V(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare the decimals.", right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.3", "0.7", "Both have 0 ones. Compare the tenths: 3 tenths &lt; 7 tenths. So <b>0.3 &lt; 0.7</b>."))
    its.append(cmp_item("1.4", "0.9", "Compare the ones first: 1.4 has 1 one and 0.9 has 0 ones. So <b>1.4 &gt; 0.9</b>, "
                        "even though 9 &gt; 4."))
    its.append(cmp_item("0.62", "0.26", "Compare the tenths first: 6 tenths &gt; 2 tenths. So <b>0.62 &gt; 0.26</b>."))
    its.append(cmp_item("0.08", "0.8", "0.8 = 0.80. Compare the tenths: 0.08 has 0 tenths and 0.80 has 8 tenths. "
                        "So <b>0.08 &lt; 0.8</b>."))
    its.append(cmp_item("0.5", "0.45", "Write 0.5 as 0.50 so both have hundredths. 50 hundredths &gt; 45 hundredths, "
                        "so <b>0.5 &gt; 0.45</b>. Do not compare 5 with 45: the 5 in 0.5 is 5 <b>tenths</b>."))
    its.append(cmp_item("0.39", "0.4", "Compare the tenths first: 3 tenths &lt; 4 tenths. So <b>0.39 &lt; 0.4</b>. "
                        "(0.4 = 0.40, and 39 &lt; 40.)"))
    its.append(cmp_item("2.07", "2.7", "Both have 2 ones. Compare the tenths: 2.07 has 0 tenths and 2.7 has 7 tenths. "
                        "So <b>2.07 &lt; 2.7</b>."))
    its.append(cmp_item("3.5", "3.50", "A 0 at the <b>end</b> of a decimal does not change its value: 5 tenths = 50 hundredths. "
                        "So <b>3.5 = 3.50</b>."))
    its.append(mcq("Which number is <b>greater than 0.5</b>?", "0.61", ["0.49", "0.45", "0.05"],
                   "0.5 has 5 tenths. 0.61 has 6 tenths, so <b>0.61</b> &gt; 0.5. "
                   "0.49 and 0.45 have only 4 tenths, and 0.05 has 0 tenths."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.6", ["0.48", "0.09", "0.5"],
                   "All have 0 ones. Compare the tenths: 6, 4, 0 and 5. <b>0.6</b> has the most tenths, "
                   "so it is the greatest, even though 0.48 has more digits."))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.25", ["0.3", "0.4", "0.33"],
                   "Compare the tenths: 0.25 has 2 tenths, the others have 3 or 4. So <b>0.25</b> is the smallest."))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.07", ["0.7", "0.17", "0.71"],
                   "0.07 has 0 tenths. All the others have at least 1 tenth. So <b>0.07</b> is the smallest."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "1.2", ["0.95", "1.09", "0.99"],
                   "0.95 and 0.99 have 0 ones, so they are less than 1. Compare 1.2 and 1.09: 2 tenths &gt; 0 tenths. "
                   "So <b>1.2</b> is the greatest."))
    its.append(mcq("Which number is <b>between 0.4 and 0.5</b>?", "0.45", ["0.54", "0.04", "4.5"],
                   "0.4 = 0.40 and 0.5 = 0.50. <b>0.45</b> is 45 hundredths, which is between 40 and 50 hundredths."))
    its.append(mcq("Which statement is <b>true</b>?", "0.6 &gt; 0.59",
                   ["0.6 &lt; 0.59", "0.3 &gt; 0.31", "0.08 &gt; 0.8"],
                   "0.6 = 0.60, and 60 hundredths &gt; 59 hundredths. So <b>0.6 &gt; 0.59</b> is true.", same_ok=True))
    its.append(mcq("Which decimal is <b>equal to 0.4</b>?", "0.40", ["0.04", "4.0", "0.14"],
                   "0.4 = 4 tenths = 40 hundredths = <b>0.40</b>. A 0 at the end does not change the value. "
                   "0.04 is only 4 hundredths."))
    for nums, right, wrong, how, e in [
        (["0.6", "0.35", "0.4"], "0.35, 0.4, 0.6", ["0.4, 0.6, 0.35", "0.6, 0.4, 0.35", "0.35, 0.6, 0.4"], "smallest to greatest",
         "Compare the tenths: 0.35 has 3, 0.4 has 4 and 0.6 has 6. So the order is <b>0.35, 0.4, 0.6</b>. "
         "0.35 is not the biggest just because 35 is a bigger number than 4 or 6."),
        (["1.2", "0.8", "1.05"], "0.8, 1.05, 1.2", ["0.8, 1.2, 1.05", "1.2, 1.05, 0.8", "1.05, 0.8, 1.2"], "smallest to greatest",
         "0.8 has 0 ones, so it is the smallest. 1.05 has 0 tenths and 1.2 has 2 tenths, so 1.05 &lt; 1.2. "
         "Order: <b>0.8, 1.05, 1.2</b>."),
        (["0.7", "0.75", "0.57"], "0.75, 0.7, 0.57", ["0.7, 0.75, 0.57", "0.57, 0.7, 0.75", "0.75, 0.57, 0.7"], "greatest to smallest",
         "Write them with hundredths: 0.70, 0.75, 0.57. Greatest to smallest: 75, 70, 57 hundredths, so "
         "<b>0.75, 0.7, 0.57</b>. Careful: the question asks for greatest first."),
        (["2.3", "2.03", "2.33"], "2.03, 2.3, 2.33", ["2.3, 2.03, 2.33", "2.3, 2.33, 2.03", "2.33, 2.3, 2.03"], "smallest to greatest",
         "All have 2 ones. Write them with hundredths: 2.30, 2.03, 2.33. 3 &lt; 30 &lt; 33 hundredths, so "
         "<b>2.03, 2.3, 2.33</b>."),
    ]:
        vs = sorted((V(x) for x in nums), reverse=how.startswith("greatest"))
        assert [V(x) for x in right.split(", ")] == vs, right
        its.append(mcq("Order from <b>%s</b>: <b>%s</b>" % (how, ", ".join(nums)), right, wrong, e, same_ok=True))
    order = [0, 1, 2, 3, 9, 10, 11, 15, 4, 5, 6, 7, 8, 12, 13, 14, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare and order decimals", "items": its}


# ============================================================ set 4: number lines
def dot_q(a, b, spaces, dot, wrong, e, labels=None, stem="What decimal is at the red dot?"):
    return mcq(fig(line_svg(a, b, spaces, labels, [(dot, None)])) + stem, D(dot), wrong, e)


def set_number_line():
    its = []
    its.append(dot_q(0, 100, 10, 30, ["0.03", "3", "0.7"],
                     "The line from 0 to 1 has <b>10 equal spaces</b>, so each space is 1 tenth (0.1). "
                     "The dot is 3 spaces after 0: <b>0.3</b>."))
    its.append(dot_q(0, 100, 10, 80, ["0.08", "8", "0.2"],
                     "Each of the 10 spaces is 0.1. The dot is 8 spaces after 0: <b>0.8</b>. "
                     "(0.2 counts the 2 spaces back from 1, the wrong end.)"))
    its.append(dot_q(0, 100, 10, 60, ["0.06", "0.4", "0.65"],
                     "Each space is 0.1. The dot is 1 space after 0.5: <b>0.6</b>. "
                     "(0.4 counts the spaces from the 1 end.)", labels=[0, 50, 100]))
    its.append(dot_q(100, 200, 10, 140, ["0.4", "1.04", "14"],
                     "The line goes from 1 to 2 in 10 equal spaces, so each space is 0.1. "
                     "The dot is 4 spaces after 1: 1 + 0.4 = <b>1.4</b>."))
    its.append(dot_q(200, 300, 10, 290, ["2.09", "2.1", "0.9"],
                     "Each space is 0.1. The dot is 9 spaces after 2: <b>2.9</b>. "
                     "(2.1 counts 1 space from the wrong end.)"))
    its.append(dot_q(0, 100, 5, 40, ["0.2", "0.02", "0.6"],
                     "This line has only <b>5 equal spaces</b> from 0 to 1, so each space is 2 tenths (0.2). "
                     "The dot is 2 spaces after 0: 0.2 + 0.2 = <b>0.4</b>. 0.2 would be just 1 space."))
    its.append(dot_q(0, 200, 20, 130, ["1.03", "0.13", "1.7"],
                     "There are 10 spaces from 0 to 1, so each space is 0.1. The dot is 3 spaces after 1: <b>1.3</b>. "
                     "(1.7 is 3 spaces back from 2, counted in the wrong direction.)", labels=[0, 100, 200]))
    its.append(dot_q(0, 100, 10, 45, ["0.5", "0.4", "4.5"],
                     "Each space is 0.1. The dot is exactly <b>halfway</b> between 0.4 and 0.5. "
                     "Halfway between 40 and 50 hundredths is 45 hundredths: <b>0.45</b>.",
                     stem="The red dot is exactly halfway between two marks. What decimal is at the red dot?"))
    its.append(dot_q(0, 100, 10, 75, ["0.7", "0.8", "7.5"],
                     "The dot is exactly halfway between 0.7 (70 hundredths) and 0.8 (80 hundredths). "
                     "Halfway is 75 hundredths: <b>0.75</b>.",
                     stem="The red dot is exactly halfway between two marks. What decimal is at the red dot?"))
    # hundredths
    its.append(dot_q(30, 40, 10, 36, ["3.6", "0.06", "0.46"],
                     "From 0.3 to 0.4 is 1 tenth, split into <b>10 equal spaces</b>, so each space is 1 hundredth (0.01). "
                     "0.3 = 0.30. Count 6 spaces on: <b>0.36</b>."))
    its.append(dot_q(70, 80, 10, 72, ["7.2", "0.02", "0.78"],
                     "Each space is 0.01. 0.7 = 0.70. The dot is 2 spaces on: <b>0.72</b>. "
                     "(0.78 counts 2 spaces back from 0.8, the wrong end.)"))
    its.append(dot_q(0, 10, 10, 4, ["0.4", "4", "0.06"],
                     "From 0 to 0.1 there are 10 equal spaces, so each space is 0.01. The dot is 4 spaces after 0: <b>0.04</b>. "
                     "0.4 would be far to the right of 0.1."))
    its.append(dot_q(90, 100, 10, 97, ["9.7", "0.07", "0.93"],
                     "Each space is 0.01. 0.9 = 0.90. Count 7 spaces on: <b>0.97</b>. Only 3 more hundredths make 1."))
    its.append(dot_q(340, 350, 10, 347, ["3.7", "34.7", "3.43"],
                     "From 3.4 to 3.5 there are 10 equal spaces, so each space is 0.01. 3.4 = 3.40. "
                     "Count 7 spaces on: <b>3.47</b>."))
    # lettered points (A, B, C, D in order along the line)
    L1 = [(20, "A"), (45, "B"), (70, "C"), (90, "D")]
    its.append(fixed(fig(line_svg(0, 100, 10, None, L1)) + "Which letter shows <b>0.7</b>?", ["A", "B", "C", "D"], 2,
                     "Each space is 0.1. 0.7 is 7 spaces after 0, so it is point <b>C</b>. "
                     "A is 0.2, B is 0.45 and D is 0.9."))
    L2 = [(5, "A"), (50, "B"), (65, "C"), (95, "D")]
    its.append(fixed(fig(line_svg(0, 100, 10, None, L2)) + "Which letter shows <b>0.05</b>?", ["A", "B", "C", "D"], 0,
                     "0.05 is 5 hundredths, which is only half of the first space (0.1). So it is point <b>A</b>. "
                     "B is 0.5 (5 tenths), not 0.05."))
    L3 = [(110, "A"), (125, "B"), (150, "C"), (175, "D")]
    its.append(fixed(fig(line_svg(100, 200, 10, None, L3)) + "Which letter shows <b>1.25</b>?", ["A", "B", "C", "D"], 1,
                     "Each space is 0.1. 1.25 is halfway between 1.2 and 1.3, so it is point <b>B</b>. "
                     "A is 1.1, C is 1.5 and D is 1.75."))
    # counting on
    its.append(mcq("Count on in tenths. What comes next?<br><b>0.7, 0.8, 0.9, ?</b>", "1", ["0.10", "0.91", "10"],
                   "0.9 + 0.1: 9 tenths and 1 more make 10 tenths, which is 1 whole. So the next number is <b>1</b> (or 1.0). "
                   "0.10 is only 1 tenth."))
    its.append(mcq("Count on in hundredths. What comes next?<br><b>0.27, 0.28, 0.29, ?</b>", "0.30", ["0.210", "0.20", "0.39"],
                   "0.29 + 0.01: 9 hundredths and 1 more make 10 hundredths, which is 1 more tenth. "
                   "So 2 tenths become 3 tenths: <b>0.30</b> (the same as 0.3). There is no such step as 0.210."))
    its.append(mcq("Start at 0.8 on a number line. Jump on <b>3 tenths</b>. Where do you land?", "1.1", ["0.11", "0.83", "0.5"],
                   "0.9, 1.0, 1.1. 10 tenths make 1 whole, so 0.8 + 0.3 = <b>1.1</b>. "
                   "0.83 jumps 3 hundredths, and 0.5 jumps back."))
    assert V("0.8") + V("0.3") == V("1.1")
    assert len(its) == 20, len(its)
    return {"title": "Decimals on a number line", "items": its}


# ============================================================ set 5: money and measurement
def set_problems():
    its = []
    its.append(mcq("How many cents is <b>$4.35</b>?", "435c", ["4350c", "4035c", "35c"],
                   "$1 = 100c, so $4 = 400c. 400c + 35c = <b>435c</b>."))
    its.append(mcq("A muesli bar costs 75c. How do you write 75c in dollars?", "$0.75", ["$75", "$7.50", "$0.57"],
                   "There are 100c in $1, so 75c = %s of a dollar = <b>$0.75</b>. ($7.50 is 750c.)" % fr(75, 100)))
    its.append(mcq("Which amount is the same as <b>50c</b>?", "$0.50", ["$0.05", "$50", "$5.00"],
                   "50c = 50 hundredths of a dollar = <b>$0.50</b> (half a dollar). $0.05 is only 5c."))
    its.append(mcq("In <b>$6.80</b>, what is the digit 8 worth?", "80c", ["8c", "$8", "$80"],
                   "The 8 is in the tenths place: 8 tenths of a dollar. %s of $1 = <b>80c</b>." % fr(8, 10)))
    its.append(mcq("Which price tag shows <b>12 dollars and 5 cents</b>?", "$12.05", ["$125", "$12.50", "$1205"],
                   "Cents are hundredths of a dollar. 5c = 5 hundredths, so write a 0 in the tenths place: <b>$12.05</b>. "
                   "$12.50 is 12 dollars and 50 cents."))
    its.append(mcq("At the school canteen, a pie costs $4.50 and a sausage roll costs $4.05. Which costs more?", "The pie",
                   ["The sausage roll", "They cost the same", "You can’t tell"],
                   "Both cost $4 and some cents. Compare the tenths: $4.50 has 5 tenths (50c) and $4.05 has 0 tenths (5c). "
                   "So <b>the pie</b> costs more.", same_ok=True))
    its.append(mcq("Which amount of money is the <b>greatest</b>?", "$1.50", ["$1.05", "95c", "$0.59"],
                   "95c and $0.59 are less than $1. Compare $1.50 and $1.05: 5 tenths &gt; 0 tenths. So <b>$1.50</b> is the greatest."))
    its.append(mcq("Isla has $2.40. Her mum gives her $1. How much money does she have now?", "$3.40",
                   ["$1.40", "$2.50", "$12.40"],
                   "Add $1 to the dollars: $2 + $1 = $3. The cents stay the same: <b>$3.40</b>. ($2.50 adds 10c, not $1, and $12.40 just writes the 1 in front.)"))
    its.append(mcq("Zara has a $2 coin, two 20c coins and a 5c coin. How much money is that?", "$2.45",
                   ["$2.25", "$47", "$2.54"],
                   "20c + 20c + 5c = 45c. Then $2 + 45c = <b>$2.45</b>. ($47 comes from adding 2 + 20 + 20 + 5, "
                   "but the $2 coin is 200c.)"))
    its.append(mcq("A ribbon is 1.25 m long. What does the <b>2</b> in 1.25 m mean?", "2 tenths of a metre",
                   ["2 metres", "2 hundredths of a metre", "2 centimetres"],
                   "The 2 is in the first place after the point, the tenths place. So it means <b>2 tenths of a metre</b> "
                   "(20 cm).", same_ok=True))
    its.append(mcq("A pencil is 0.15 m long. 1 cm is %s of a metre. How long is the pencil in centimetres?" % fr(1, 100),
                   "15 cm", ["1.5 cm", "150 cm", "51 cm"],
                   "0.15 m = 15 hundredths of a metre = %s m. Each hundredth of a metre is 1 cm, so the pencil is <b>15 cm</b>."
                   % fr(15, 100)))
    its.append(mcq("Ruby’s water bottle holds 0.75 L. Which fraction of a litre is that?", fr(75, 100) + " L",
                   [fr(7, 10) + " L", fr(75, 10) + " L", fr(57, 100) + " L"],
                   "0.75 has two digits after the point, so it is hundredths: 75 hundredths = <b>%s L</b> (750 mL)."
                   % fr(75, 100)))
    its.append(mcq("Jug A holds 2.5 L of water. Jug B holds 2.45 L. Which jug holds more?", "Jug A",
                   ["Jug B", "They hold the same", "You can’t tell"],
                   "Both hold 2 L and a bit more. 2.5 = 2.50. Compare 50 hundredths and 45 hundredths: "
                   "<b>Jug A</b> holds more. 45 is bigger than 5, but the 5 in 2.5 means 5 <b>tenths</b>.", same_ok=True))
    its.append(mcq("At the athletics carnival, Mia jumps 2.48 m and Jack jumps 2.8 m in the long jump. Who jumps further?",
                   "Jack", ["Mia", "They jump the same", "You can’t tell"],
                   "Both jumps are 2 whole metres. Compare the tenths: 2.8 has 8 tenths and 2.48 has 4 tenths. "
                   "So <b>Jack</b> jumps further.", same_ok=True))
    its.append(mcq("At the swimming carnival, Kai swims 25 m in 24.6 seconds and Leo swims it in 24.06 seconds. "
                   "Who is faster?", "Leo", ["Kai", "They are equally fast", "You can’t tell"],
                   "In a race, the <b>shorter</b> time is faster. 24.06 &lt; 24.6 because 0 tenths &lt; 6 tenths. "
                   "So <b>Leo</b> is faster.", same_ok=True))
    its.append(mcq("Three students measure their height: Chloe 1.3 m, Aarav 1.28 m and Grace 1.35 m. Who is the tallest?",
                   "Grace", ["Chloe", "Aarav", "They are the same height"],
                   "All are 1 m and a bit more. Write them with hundredths: 1.30, 1.28 and 1.35. "
                   "35 hundredths is the most, so <b>Grace</b> is the tallest.", same_ok=True))
    its.append(mcq("A puppy has a mass of 4.05 kg. Which is the same as 4.05 kg?", "4 kg and 5 hundredths of a kilogram",
                   ["4 kg and 5 tenths of a kilogram", "45 kg", "405 kg"],
                   "4.05: 4 ones, 0 tenths and 5 hundredths. So it is <b>4 kg and 5 hundredths of a kilogram</b>. "
                   "5 tenths would be 4.5 kg.", same_ok=True))
    its.append(mcq("A 1 L carton of juice is full. Sienna pours out 0.3 L. How much juice is left?", "0.7 L",
                   ["0.07 L", "1.3 L", "0.97 L"],
                   "1 L = 10 tenths of a litre. 10 tenths − 3 tenths = 7 tenths = <b>0.7 L</b>. "
                   "0.97 L would take away only 3 hundredths."))
    assert 1 - V("0.3") == V("0.7")
    its.append(mcq("Lachlan’s ribbon is 1.25 m long. He cuts off 0.1 m. How long is the ribbon now?", "1.15 m",
                   ["1.24 m", "1.35 m", "0.25 m"],
                   "0.1 m is 1 tenth of a metre. Take 1 from the tenths digit: 2 tenths − 1 tenth = 1 tenth. "
                   "1.25 − 0.1 = <b>1.15 m</b>. 1.24 m takes away only 1 hundredth."))
    assert V("1.25") - V("0.1") == V("1.15")
    its.append(mcq("Matilda has $5. She buys a drink for $2.70. How much change does she get?", "$2.30",
                   ["$3.30", "$3.70", "$7.70"],
                   "$2.70 + 30c = $3, and $3 + $2 = $5. So the change is $2 + 30c = <b>$2.30</b>. "
                   "Check: $2.70 + $2.30 = $5.00."))
    assert V("5") - V("2.70") == V("2.30")
    order = [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement problems", "items": its}


# ============================================================ lesson
def body_html():
    f_strip = strips_svg(3)
    f_grid = grid_svg(27, cell=22)
    f_chart = chart_svg(["4.37"])
    f_cmp = svg_wrap(452, 222, "".join([
        grid_body(50, 6, 6, 18), text(96, 214, "0.5 = 0.50", 18),
        grid_body(45, 266, 6, 18), text(356, 214, "0.45", 18),
    ]), "two hundred squares: 50 squares shaded for 0.5 and 45 squares shaded for 0.45")
    f_line = line_svg(0, 100, 10, [0, 50, 100], [(30, None)])
    return (
        "<h2>Tenths</h2>"
        "<p>Split 1 whole into <b>10 equal parts</b>. Each part is one <b>tenth</b>: " + fr(1, 10) + " = 0.1. "
        "Tenths go in the <b>first place</b> after the decimal point.</p>"
        "<figure class='sn-fig'>" + f_strip +
        "<figcaption>The strip is 1 whole. 3 of the 10 parts are shaded: " + fr(3, 10) + " = 0.3.</figcaption></figure>"
        "<h2>Hundredths</h2>"
        "<p>Split 1 whole into <b>100 equal parts</b>. Each part is one <b>hundredth</b>: " + fr(1, 100) + " = 0.01. "
        "Hundredths go in the <b>second place</b> after the decimal point. 10 hundredths make 1 tenth.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>The whole square is 1. 2 full columns (2 tenths) and 7 more squares (7 hundredths) are shaded: "
        + fr(27, 100) + " = 0.27.</figcaption></figure>"
        "<h2>Place value</h2>"
        "<p>Each digit has a place: ones, then the decimal point, then tenths and hundredths. "
        "Use a 0 to hold an empty place: " + fr(7, 100) + " = 0.07.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>4.37 = 4 ones, 3 tenths and 7 hundredths = 4 + 0.3 + 0.07.</figcaption></figure>"
        + ex("Example 1", "Write " + fr(8, 100) + " as a decimal.",
             "8 hundredths. There are 0 tenths, so put a 0 in the tenths place.", "0.08")
        + "<h2>Comparing decimals</h2>"
        "<p>Compare the ones first, then the tenths, then the hundredths. "
        "It helps to give both numbers the same number of places: 0.5 = 0.50.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.5 = 50 hundredths and 0.45 = 45 hundredths. So 0.5 &gt; 0.45, even though 45 is more than 5."
        "</figcaption></figure>"
        + ex("Example 2", "Order 0.6, 0.35 and 0.4 from smallest to greatest.",
             "Compare the tenths: 3, 4 and 6.", "0.35, 0.4, 0.6")
        + "<h2>Decimals on a number line</h2>"
        "<p>Count the spaces between 0 and 1. With 10 equal spaces, each space is 0.1. "
        "Between 0.3 and 0.4, 10 more spaces would each be 0.01.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>The dot is 3 spaces after 0, so it shows 0.3.</figcaption></figure>"
        "<h2>Money and measurement</h2>"
        "<p>Cents are hundredths of a dollar: $4.35 = 4 dollars and 35 cents = 435c. "
        "Centimetres are hundredths of a metre: 1.25 m = 1 m 25 cm. 2.5 L is 2 and a half litres.</p>"
        + ex("Example 3", "Which costs more: $3.50 or $3.05?",
             "Compare the tenths: 5 tenths (50c) and 0 tenths (5c).", "$3.50")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because 45 &gt; 5", "Use the same places: 0.45 &lt; 0.50"],
            ["Writing 7 tenths as 0.07", "Tenths use the first place: 0.7"],
            ["Writing " + fr(7, 100) + " as 0.7", "Hundredths need two places: 0.07"],
            ["Reading 0.3 as " + fr(1, 3), "0.3 is 3 tenths: " + fr(3, 10)],
            ["Counting 0.28, 0.29, 0.210", "10 hundredths make 1 tenth: 0.29, 0.30"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about decimals in the Australian Curriculum?",
     "a": "In Year 4 (AC9M4N01) students extend place value to tenths and hundredths. They read and write decimals such as 0.3 and 0.27, connect them to fractions like 3/10 and 27/100, and compare decimals in money and measurement."},
    {"q": "How do you explain tenths and hundredths to a child?",
     "a": "Use a strip split into 10 equal parts for tenths and a hundred square for hundredths. Each part of the strip is 0.1 and each small square is 0.01, so 27 shaded squares show 0.27."},
    {"q": "Why is 0.5 bigger than 0.45?",
     "a": "The 5 in 0.5 means 5 tenths, which is 50 hundredths. 0.45 is only 45 hundredths, so 0.5 is bigger even though it has fewer digits."},
    {"q": "Is 0.3 the same as 1/3?",
     "a": "No. 0.3 means 3 tenths, which is 3/10. One third is a little more than 0.3, because 1/3 is 0.333... and never ends."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines, tenth strips, place value charts, hundred squares)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4802)
    sets = [set_tenths_hundredths(), set_place_value(), set_compare(), set_number_line(), set_problems()]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "decimals-tenths-and-hundredths", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals: Tenths and Hundredths",
        "seo_title": "Year 4 Decimals Worksheets: Tenths and Hundredths, Place Value and Comparing (Free, Answer Key)",
        "short_title": "Tenths and hundredths",
        "domain": "Number",
        "standard_code": "AC9M4N01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise and extend the application of place value to tenths and hundredths and use the conventions to name and write decimal numbers",
        "meta_desc": "Free Year 4 decimals worksheets for the Australian Curriculum (AC9M4N01): tenths and hundredths on strips and hundred squares, 3/10 = 0.3, place value, comparing and ordering decimals, number lines, and money and measurement. 100 maths questions with an answer key.",
        "key_big": "Tenths are the first place after the decimal point; hundredths are the second. 3/10 = 0.3 and 27/100 = 0.27.",
        "key_sub": "Compare by place value, not by length: 0.5 = 0.50 > 0.45. Use a 0 to hold an empty place: 7/100 = 0.07, and 0.3 is 3/10, not 1/3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|tenth strip|place value chart|hundred square)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
