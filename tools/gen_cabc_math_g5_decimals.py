# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 5 Math: Decimals to Thousandths
(BC Mathematics Curriculum K-9, Grade 5 Content: "decimals to thousandths")
  python3 tools/gen_cabc_math_g5_decimals.py
Pictures are drawn from whole numbers of thousandths (247 = 0.247) or hundredths (hundred grids).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Canadian English, metric units, dollars and cents (no pennies),
BC/SI number style (4536, 12 500 with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
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


def T(v):
    """Decimal text for v thousandths without trailing zeros: 300 -> '0.3', 247 -> '0.247', 1000 -> '1'."""
    s = format((Dm(v) / 1000).normalize(), "f")
    assert F(Dm(s)) == F(v, 1000)
    return s


def V(s):
    return F(Dm(s.replace(NB, "")))


def rnd_to(s, places):
    """Round decimal string s (half up) to `places` decimal places; keeps the places (4.0, 12.10)."""
    q = Dm(1).scaleb(-places)
    return str(Dm(s).quantize(q, rounding=ROUND_HALF_UP))


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢)?( .+)?$")


def val(c):
    """(value, unit) of a choice. None for choices that are not one number."""
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
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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
    return svg_wrap(w, w, grid_body(k, pad, pad, cell),
                    "hundred grid with %s shaded" % ("1 square" if k == 1 else "%d squares" % k))


PV = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths"), (-3, "Thousandths")]


def chart_svg(s_, hi=None):
    """Place value chart: (Tens) | Ones | . | Tenths | Hundredths | Thousandths. hi = place drawn in red."""
    w, _, f = s_.partition(".")
    assert len(w) <= 2 and len(f) <= 3
    cols = PV if len(w) > 1 else PV[1:]
    CW, PW, HEAD, ROW = 104, 16, 30, 44
    x0, y0 = 6, 6
    W = 2 * x0 + len(cols) * CW + PW
    H = 2 * y0 + HEAD + ROW
    xs, x = {}, x0
    for p, _ in cols:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, W - 2 * x0, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, HEADFILL)]
    for p, name in cols:
        if p != cols[0][0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW, GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, name, 14))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW, GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    digits = {}
    for j, ch in enumerate(w):
        digits[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        digits[-(j + 1)] = ch
    for p, ch in digits.items():
        o.append(text(xs[p] + CW / 2.0, y0 + HEAD + 32, ch, 28, col=RED if hi == p else LINE, weight=800))
    if f:
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, y0 + HEAD + 31, LINE))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % s_)


def line_svg(a, b, spaces, labels=None, dots=(), W=440):
    """Number line from a to b thousandths with `spaces` equal spaces.
    labels: values (thousandths) written under the line, must sit on a tick.
    dots: (value, letter or None). Letters are written above their dot."""
    labels = labels if labels is not None else [a, b]
    lettered = any(l for _, l in dots)
    L, R = 34, W - 34
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
        s.append(text(X(v), Y + 36, T(v), 17))
    xs = []
    for v, l in dots:
        assert a <= v <= b
        xs.append(X(v))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(v), Y, BLUE if l else RED))
        if l:
            s.append(text(X(v), Y - 20, l, 18))
    xs.sort()
    assert all(q - p >= 20 for p, q in zip(xs, xs[1:])), (a, b, dots)
    # labels must not overlap: about 9 px per character at 17px
    lx = sorted((X(v), len(T(v))) for v in labels)
    for (x1, n1), (x2, n2) in zip(lx, lx[1:]):
        assert x2 - x1 > 5 * (n1 + n2) + 6, labels
    lab = "number line from %s to %s split into %d equal spaces" % (T(a), T(b), spaces)
    if lettered:
        lab += " with points %s" % ", ".join(l for _, l in dots)
    return svg_wrap(W, Y + 46, "".join(s), lab)


# ============================================================ set 1: tenths, hundredths, thousandths
NAMES = {1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


def digit_at(s, place):
    w, _, f = s.partition(".")
    return w[len(w) - 1 - place] if place >= 0 else f[-place - 1]


def set_places():
    its = []
    its.append(mcq(fig(grid_svg(70)) + "The whole grid is 1. What decimal is shaded?", "0.7", ["0.07", "7", "0.3"],
                   "Each full column is 1 tenth. 7 full columns are shaded: 7 tenths = %s = <b>0.7</b>. "
                   "0.07 would be only 7 small squares, and 0.3 is the part that is not shaded." % fr(7, 10)))
    its.append(mcq(fig(grid_svg(43)) + "The whole grid is 1. What decimal is shaded?", "0.43", ["4.3", "0.34", "0.043"],
                   "4 full columns (4 tenths) and 3 more squares (3 hundredths) are shaded: "
                   "43 hundredths = %s = <b>0.43</b>." % fr(43, 100)))
    its.append(mcq(fig(grid_svg(5)) + "The whole grid is 1. What decimal is shaded?", "0.05", ["0.5", "0.005", "5"],
                   "5 small squares are shaded and there is no full column, so there are 0 tenths. "
                   "5 hundredths = %s = <b>0.05</b>. Write a 0 in the tenths place." % fr(5, 100)))
    its.append(mcq("1 whole is split into <b>1000</b> equal parts. What decimal is each part?", "0.001",
                   ["0.01", "0.1", "1000"],
                   "Each part is %s of the whole, one <b>thousandth</b>: <b>0.001</b>. "
                   "0.01 is one hundredth (100 parts) and 0.1 is one tenth (10 parts)." % fr(1, 1000)))
    its.append(mcq("How many thousandths make <b>1 hundredth</b>?", "10", ["100", "1000", "0.1"],
                   "Split one hundredth into 10 equal parts and each part is 1 thousandth. "
                   "So <b>10</b> thousandths = 1 hundredth (0.010 = 0.01)."))
    its.append(mcq("How many thousandths make <b>1 tenth</b>?", "100", ["10", "1000", "1"],
                   "1 tenth = 10 hundredths, and each hundredth = 10 thousandths. 10 × 10 = <b>100</b> thousandths "
                   "(0.100 = 0.1). 1000 thousandths make 1 whole."))
    for s, place, wrong in [("2.635", -3, ["5 hundredths", "5 tenths", "5 ones"]),
                            ("0.482", -2, ["8 tenths", "8 thousandths", "8 ones"]),
                            ("14.307", -1, ["3 ones", "3 hundredths", "3 thousandths"]),
                            ("7.096", -3, ["6 hundredths", "6 tenths", "6 ones"])]:
        dg = digit_at(s, place)
        right = "%s %s" % (dg, NAMES[place])
        nth = {-1: "first", -2: "second", -3: "third"}[place]
        e = ("The red %s is in the <b>%s</b> place after the decimal point, in the %s column. Its value is <b>%s</b> = %s."
             % (dg, nth, NAMES[place], right, format((Dm(dg) * Dm(10) ** place).normalize(), "f")))
        if s == "14.307":
            e += " The 0 holds the hundredths place."
        if s == "7.096":
            e += " The 0 holds the tenths place."
        its.append(mcq(fig(chart_svg(s, hi=place)) + "What is the value of the red digit in %s?" % s,
                       right, wrong, e, same_ok=True))
    for dg, s, place, right, wrong in [("4", "3.024", -3, "0.004", ["0.04", "0.4", "4"]),
                                       ("9", "0.951", -1, "0.9", ["0.09", "0.009", "9"]),
                                       ("2", "25.168", 1, "20", ["2", "0.2", "200"])]:
        assert digit_at(s, place) == dg
        assert Dm(right) == Dm(dg) * Dm(10) ** place
        where = {1: "the tens place (two places before the point)", -1: "the tenths place, the first place after the point",
                 -3: "the thousandths place, the third place after the point"}[place]
        its.append(mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (dg, s), right, wrong,
                       "In %s the %s is in %s. It is worth <b>%s</b>." % (s, dg, where, right)))
    for s, place, right, wrong in [("6.583", "thousandths", "3", ["8", "5", "6"]),
                                   ("41.207", "hundredths", "0", ["7", "2", "1"])]:
        f = s.partition(".")[2]
        its.append(mcq("In <b>%s</b>, which digit is in the <b>%s</b> place?" % (s, place), right, wrong,
                       "Count places after the decimal point: tenths, hundredths, thousandths. "
                       "In %s the tenths digit is %s, the hundredths digit is %s and the thousandths digit is %s. "
                       "The answer is <b>%s</b>." % (s, f[0], f[1], f[2], right)))
    its.append(mcq(fig(line_svg(240, 250, 10, dots=[(247, None)])) + "What decimal is at the red dot?", "0.247",
                   ["0.27", "0.257", "0.2407"],
                   "From 0.24 to 0.25 there are <b>10 equal spaces</b>, so each space is 1 thousandth (0.001). "
                   "The dot is 7 spaces after 0.240: <b>0.247</b>."))
    its.append(mcq(fig(line_svg(1300, 1400, 10, dots=[(1380, None)])) + "What decimal is at the red dot?", "1.38",
                   ["1.308", "1.8", "1.48"],
                   "From 1.3 to 1.4 there are 10 equal spaces, so each space is 1 hundredth (0.01). "
                   "The dot is 8 spaces after 1.30: <b>1.38</b>. 1.308 would be very close to 1.3."))
    its.append(mcq("How many thousandths are there in <b>0.06</b>?", "60", ["6", "600", "0.6"],
                   "1 hundredth = 10 thousandths, so 6 hundredths = <b>60</b> thousandths. 0.06 = 0.060."))
    its.append(mcq("How many thousandths are there in <b>0.4</b>?", "400", ["4", "40", "4000"],
                   "1 tenth = 100 thousandths, so 4 tenths = <b>400</b> thousandths. 0.4 = 0.400."))
    its.append(mcq("Count on in thousandths. What comes next?<br><b>0.997, 0.998, 0.999, ?</b>", "1.000",
                   ["0.1000", "0.910", "0.9991"],
                   "0.999 + 0.001: 9 thousandths and 1 more make 10 thousandths = 1 hundredth. That makes 10 hundredths "
                   "= 1 tenth, and 10 tenths = 1 whole. So the next number is <b>1.000</b> (the same as 1). "
                   "There is no such step as 0.1000."))
    assert V("0.999") + V("0.001") == 1
    order = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 8, 9, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Tenths, hundredths and thousandths", "items": its}


# ============================================================ set 2: read and write decimals
def set_read_write():
    its = []
    its.append(mcq("How do you read <b>0.6</b>?", "six tenths", ["six hundredths", "six thousandths", "sixty"],
                   "There is one digit after the point, so it means tenths: <b>six tenths</b>.", same_ok=True))
    its.append(mcq("How do you read <b>0.45</b>?", "forty-five hundredths",
                   ["forty-five tenths", "forty-five thousandths", "four and five tenths"],
                   "The last digit is in the hundredths place, so read the digits after the point as hundredths: "
                   "<b>forty-five hundredths</b>.", same_ok=True))
    its.append(mcq("How do you read <b>4.05</b>?", "four and five hundredths",
                   ["four and five tenths", "four hundred five", "forty-five hundredths"],
                   "4 is the whole number. Say “and” for the decimal point. The 5 is in the hundredths place, "
                   "so read it as <b>four and five hundredths</b>.", same_ok=True))
    its.append(mcq("How do you read <b>2.007</b>?", "two and seven thousandths",
                   ["two and seven hundredths", "two and seven tenths", "two thousand seven"],
                   "2 is the whole number and “and” is the decimal point. The 7 is in the <b>third</b> place after the point: "
                   "<b>two and seven thousandths</b>.", same_ok=True))
    its.append(mcq("How do you read <b>0.312</b>?", "three hundred twelve thousandths",
                   ["three hundred twelve hundredths", "three and twelve hundredths", "thirty-one and two tenths"],
                   "There are three digits after the point, so the last digit is in the thousandths place. "
                   "Read the digits as a whole number, then say the place: <b>three hundred twelve thousandths</b>.",
                   same_ok=True))
    its.append(mcq("Write <b>eight hundredths</b> as a decimal.", "0.08", ["0.8", "0.008", "8"],
                   "Hundredths need <b>two places</b> after the point. There are 0 tenths: <b>0.08</b>. "
                   "0.8 would be 8 tenths."))
    its.append(mcq("Write <b>twenty-three thousandths</b> as a decimal.", "0.023", ["0.23", "0.0023", "23"],
                   "Thousandths need <b>three places</b> after the point. 23 fills only two, so write a 0 in the tenths place: "
                   "<b>0.023</b>. 0.23 is twenty-three hundredths."))
    its.append(mcq("Write <b>five and nine tenths</b> as a decimal.", "5.9", ["5.09", "59", "0.59"],
                   "“Five” is the whole number, “and” is the decimal point, and nine tenths is one place after the point: "
                   "<b>5.9</b>."))
    its.append(mcq("Write <b>seven and three hundred eight thousandths</b> as a decimal.", "7.308",
                   ["7.38", "7.3008", "73.08"],
                   "7 is the whole number. Three hundred eight thousandths = 0.308 (three places after the point). "
                   "So the number is <b>7.308</b>."))
    its.append(mcq("Write <b>twelve and forty-six thousandths</b> as a decimal.", "12.046",
                   ["12.46", "12.0046", "1.246"],
                   "Forty-six thousandths needs three places: 0.046. So the number is <b>12.046</b>. "
                   "12.46 is twelve and forty-six hundredths."))
    its.append(mcq("Write <b>3 ones, 4 tenths, 0 hundredths and 9 thousandths</b> as a decimal.", "3.409",
                   ["3.49", "3.0409", "34.09"],
                   "Write one digit in each place: 3 . 4 0 9 = <b>3.409</b>. The 0 holds the hundredths place."))
    its.append(mcq("Write <b>2 tens, 6 hundredths and 5 thousandths</b> as a decimal.", "20.065",
                   ["20.65", "2.065", "26.5"],
                   "2 tens = 20. There are 0 ones and 0 tenths. Then 6 hundredths and 5 thousandths: <b>20.065</b>."))
    its.append(mcq("4 + 0.3 + 0.008 = ?", "4.308", ["4.38", "4.038", "4.3008"],
                   "4 ones, 3 tenths, 0 hundredths and 8 thousandths: 4 . 3 0 8 = <b>4.308</b>."))
    assert 4 + V("0.3") + V("0.008") == V("4.308")
    its.append(mcq("10 + 0.6 + 0.01 + 0.009 = ?", "10.619", ["1.619", "106.19", "10.6109"],
                   "1 ten, 0 ones, 6 tenths, 1 hundredth and 9 thousandths: <b>10.619</b>."))
    assert 10 + V("0.6") + V("0.01") + V("0.009") == V("10.619")
    its.append(mcq("Which shows <b>5.274</b> in expanded form?", "5 + 0.2 + 0.07 + 0.004",
                   ["5 + 0.2 + 0.7 + 0.4", "5 + 2 + 7 + 4", "5 + 0.002 + 0.07 + 0.4"],
                   "5 ones, 2 tenths, 7 hundredths and 4 thousandths: <b>5 + 0.2 + 0.07 + 0.004</b>.", same_ok=True))
    assert 5 + V("0.2") + V("0.07") + V("0.004") == V("5.274")
    its.append(mcq("Write <b>0.059</b> in words.", "fifty-nine thousandths",
                   ["fifty-nine hundredths", "five and nine thousandths", "fifty-nine tenths"],
                   "There are three places after the point, so it is thousandths. The digits make 59: "
                   "<b>fifty-nine thousandths</b>.", same_ok=True))
    its.append(mcq("Which decimal has a <b>7 in the thousandths place</b>?", "0.427", ["0.742", "0.472", "7.024"],
                   "The thousandths place is the <b>third</b> place after the point. In <b>0.427</b> it holds a 7. "
                   "In 0.742 the 7 is in the tenths, in 0.472 it is in the hundredths, and in 7.024 it is in the ones."))
    its.append(mcq("Simran writes “seven and twelve thousandths” as 7.12. What should she write?", "7.012",
                   ["7.0012", "70.12", "7.120"],
                   "7.12 is seven and twelve <b>hundredths</b>. Thousandths need three places after the point, "
                   "so write a 0 first: <b>7.012</b>."))
    its.append(mcq("A decimal has <b>3 ones, 15 hundredths and 2 thousandths</b>. What is the decimal?", "3.152",
                   ["3.1502", "3.0152", "31.52"],
                   "15 hundredths = 0.15 and 2 thousandths = 0.002. 3 + 0.15 + 0.002 = <b>3.152</b>."))
    assert 3 + V("0.15") + V("0.002") == V("3.152")
    its.append(mcq("Which number is <b>0.01 more</b> than 4.293?", "4.303", ["4.294", "4.393", "5.293"],
                   "0.01 is 1 hundredth. The hundredths digit is 9, and 9 + 1 = 10 hundredths = 1 more tenth. "
                   "So 4.293 + 0.01 = <b>4.303</b>. 4.294 adds 0.001 and 4.393 adds 0.1."))
    assert V("4.293") + V("0.01") == V("4.303")
    assert len(its) == 20, len(its)
    return {"title": "Read and write decimals", "items": its}


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
        assert w != right
    return mcq("Order from <b>%s</b>: <b>%s</b>" % (how, ", ".join(nums)), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.45", "0.5", "Write 0.5 as 0.50 so both have hundredths. 45 hundredths &lt; 50 hundredths, "
                        "so <b>0.45 &lt; 0.5</b>. Do not compare 45 with 5: the 5 in 0.5 is 5 <b>tenths</b>."))
    its.append(cmp_item("0.7", "0.700", "Zeros at the <b>end</b> of a decimal do not change its value: "
                        "7 tenths = 70 hundredths = 700 thousandths. So <b>0.7 = 0.700</b>."))
    its.append(cmp_item("2.305", "2.35", "Both have 2 ones and 3 tenths. Compare the hundredths: 0 &lt; 5. "
                        "So <b>2.305 &lt; 2.35</b>, even though 2.305 has more digits."))
    its.append(cmp_item("0.089", "0.1", "Compare the tenths: 0.089 has 0 tenths and 0.1 has 1 tenth. "
                        "So <b>0.089 &lt; 0.1</b>, even though 89 &gt; 1."))
    its.append(cmp_item("6.42", "6.402", "Write 6.42 as 6.420. Both have 6 ones and 4 tenths. Compare the hundredths: 2 &gt; 0. "
                        "So <b>6.42 &gt; 6.402</b>."))
    its.append(cmp_item("13.1", "9.999", "Compare the whole numbers first: 13 &gt; 9. So <b>13.1 &gt; 9.999</b>, "
                        "even though 9.999 has more digits."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.6", ["0.594", "0.599", "0.06"],
                   "Compare the tenths: 6, 5, 5 and 0. <b>0.6</b> has the most tenths, so it is the greatest, "
                   "even though 0.594 and 0.599 have more digits."))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.305", ["0.35", "0.351", "0.53"],
                   "0.53 has 5 tenths, so it is the greatest. The others have 3 tenths: compare the hundredths 0, 5 and 5. "
                   "<b>0.305</b> has 0 hundredths, so it is the smallest."))
    its.append(mcq("Which number is <b>greater than 0.25</b>?", "0.3", ["0.205", "0.025", "0.249"],
                   "0.25 = 0.250 and 0.3 = 0.300. 300 thousandths &gt; 250 thousandths, so <b>0.3</b> &gt; 0.25. "
                   "0.249 is 1 thousandth less than 0.25."))
    its.append(mcq("Which decimal is <b>equal to 0.4</b>?", "0.400", ["0.004", "0.04", "4.00"],
                   "0.4 = 4 tenths = 400 thousandths = <b>0.400</b>. Zeros at the end do not change the value. "
                   "0.04 and 0.004 move the 4 to a smaller place."))
    its.append(mcq("Which number is <b>between 1.25 and 1.26</b>?", "1.257", ["1.275", "1.205", "1.52"],
                   "1.25 = 1.250 and 1.26 = 1.260. <b>1.257</b> is 1 and 257 thousandths, between 250 and 260 thousandths."))
    its.append(fixed(fig(line_svg(300, 400, 10, labels=[300, 350, 400], dots=[(320, "A"), (355, "B"), (370, "C"), (395, "D")],
                              W=500)) +
                     "Which letter shows <b>0.355</b>?", ["A", "B", "C", "D"], 1,
                     "Each space is 0.01. 0.355 is halfway between 0.35 and 0.36. That is point <b>B</b>. "
                     "A is 0.32, C is 0.37 and D is 0.395."))
    its.append(mcq("Which statement is <b>true</b>?", "0.8 &gt; 0.79",
                   ["0.08 &gt; 0.8", "0.125 &gt; 0.2", "0.3 &lt; 0.296"],
                   "0.8 = 0.80, and 80 hundredths &gt; 79 hundredths. So <b>0.8 &gt; 0.79</b> is true.", same_ok=True))
    assert V("0.8") > V("0.79") and not V("0.08") > V("0.8") and not V("0.125") > V("0.2") and not V("0.3") < V("0.296")
    its.append(mcq("Hana says 0.125 &gt; 0.2 because 125 &gt; 2. Which is correct?", "0.125 &lt; 0.2",
                   ["0.125 &gt; 0.2", "0.125 = 0.2", "You can’t tell"],
                   "Compare the tenths first: 0.125 has 1 tenth and 0.2 has 2 tenths. So <b>0.125 &lt; 0.2</b>. "
                   "Or write 0.2 as 0.200: 125 &lt; 200 thousandths.", same_ok=True))
    its.append(order_q(["0.5", "0.45", "0.405"], "smallest to greatest", "0.405, 0.45, 0.5",
                       ["0.5, 0.45, 0.405", "0.45, 0.405, 0.5", "0.405, 0.5, 0.45"],
                       "Write them with thousandths: 0.500, 0.450, 0.405. 405 &lt; 450 &lt; 500, so the order is "
                       "<b>0.405, 0.45, 0.5</b>. The longest number is not the greatest."))
    its.append(order_q(["3.2", "3.02", "3.202", "3.022"], "smallest to greatest", "3.02, 3.022, 3.2, 3.202",
                       ["3.2, 3.02, 3.202, 3.022", "3.02, 3.2, 3.022, 3.202", "3.202, 3.2, 3.022, 3.02"],
                       "All have 3 ones. Write them with thousandths: 3.200, 3.020, 3.202, 3.022. "
                       "20 &lt; 22 &lt; 200 &lt; 202 thousandths, so <b>3.02, 3.022, 3.2, 3.202</b>."))
    its.append(order_q(["0.9", "0.09", "0.909", "0.099"], "greatest to smallest", "0.909, 0.9, 0.099, 0.09",
                       ["0.9, 0.909, 0.09, 0.099", "0.09, 0.099, 0.9, 0.909", "0.909, 0.099, 0.9, 0.09"],
                       "Write them with thousandths: 0.900, 0.090, 0.909, 0.099. Greatest first: 909, 900, 99, 90. "
                       "So <b>0.909, 0.9, 0.099, 0.09</b>."))
    its.append(mcq("Which digit can go in the box to make this true?<br><b>0.6□4 &gt; 0.67</b>", "8", ["6", "2", "0"],
                   "Write 0.67 as 0.670. Both numbers have 6 tenths, so compare the hundredths. "
                   "The box must be 7 or more: 0.684 &gt; 0.670. So <b>8</b> works. With 6, 0.664 &lt; 0.670."))
    assert V("0.684") > V("0.67") and V("0.664") < V("0.67")
    its.append(mcq("Use the digits 4, 0 and 7 once each to fill 0.□□□. What is the <b>greatest</b> decimal you can make?",
                   "0.740", ["0.704", "0.047", "0.470"],
                   "Put the greatest digit in the greatest place: 7 tenths, then 4 hundredths, then 0 thousandths. "
                   "The greatest decimal is <b>0.740</b>."))
    its.append(mcq("What is the <b>smallest</b> number with three decimal places that is greater than 2.39?", "2.391",
                   ["2.4", "2.389", "2.390"],
                   "2.39 = 2.390. The next thousandth after 2.390 is <b>2.391</b>. 2.390 is equal to 2.39, not greater, "
                   "and 2.389 is less."))
    assert V("2.391") > V("2.39") and V("2.390") == V("2.39")
    assert len(its) == 20, len(its)
    return {"title": "Compare and order decimals", "items": its}


# ============================================================ set 4: decimals and fractions
def set_fractions():
    its = []
    its.append(mcq("Write %s as a decimal." % fr(3, 10), "0.3", ["0.03", "3.10", "0.003"],
                   "%s is 3 tenths. Tenths are the first place after the point: <b>0.3</b>. "
                   "0.03 is 3 hundredths." % fr(3, 10)))
    its.append(mcq("Write %s as a decimal." % fr(3, 100), "0.03", ["0.3", "0.003", "3"],
                   "%s is 3 hundredths. Hundredths need two places, so write a 0 in the tenths place: <b>0.03</b>."
                   % fr(3, 100)))
    its.append(mcq("Write %s as a decimal." % fr(47, 1000), "0.047", ["0.47", "4.7", "0.0047"],
                   "%s is 47 thousandths. Thousandths need three places, so write a 0 in the tenths place: <b>0.047</b>."
                   % fr(47, 1000)))
    its.append(mcq("Which fraction is equal to <b>0.3</b>?", fr(3, 10), [fr(3, 100), fr(1, 3), fr(3, 1000)],
                   "0.3 has one digit after the point, so it means tenths: 0.3 = <b>%s</b>. "
                   "%s is 0.03, not 0.3." % (fr(3, 10), fr(3, 100))))
    its.append(mcq("Which fraction is equal to <b>0.09</b>?", fr(9, 100), [fr(9, 10), fr(1, 9), fr(9, 1000)],
                   "0.09 has two digits after the point, so it means hundredths: 9 hundredths = <b>%s</b>." % fr(9, 100)))
    its.append(mcq("Which fraction is equal to <b>0.125</b>?", fr(125, 1000), [fr(125, 100), fr(125, 10), fr(1, 125)],
                   "0.125 has three digits after the point, so it means thousandths: <b>%s</b>. "
                   "%s would be 1.25." % (fr(125, 1000), fr(125, 100))))
    its.append(mcq("0.6 is equal to how many hundredths?", fr(60, 100), [fr(6, 100), fr(6, 1000), fr(1, 6)],
                   "0.6 = 6 tenths. Each tenth is 10 hundredths, so 6 tenths = 60 hundredths = <b>%s</b>. "
                   "%s is only 0.06." % (fr(60, 100), fr(6, 100))))
    its.append(mcq("0.25 is equal to how many thousandths?", fr(250, 1000), [fr(25, 1000), fr(250, 100), fr(1, 25)],
                   "0.25 = 0.250. 25 hundredths = 250 thousandths = <b>%s</b>. %s is only 0.025."
                   % (fr(250, 1000), fr(25, 1000))))
    assert V("0.25") == F(250, 1000)
    its.append(mcq("Write 2 %s as a decimal." % fr(7, 10), "2.7", ["2.07", "0.27", "7.2"],
                   "2 wholes, the decimal point, then 7 tenths: <b>2.7</b>. 2.07 would be 2 and 7 hundredths."))
    its.append(mcq("Write 5 %s as a decimal." % fr(36, 1000), "5.036", ["5.36", "5.0036", "50.36"],
                   "5 wholes, then 36 thousandths. Thousandths need three places: 0.036. So the number is <b>5.036</b>."))
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 2), "0.5", ["1.2", "0.12", "0.2"],
                   "Make tenths: %s = %s (multiply the top and bottom by 5). 5 tenths = <b>0.5</b>. "
                   "1.2 just writes the digits 1 and 2." % (fr(1, 2), fr(5, 10))))
    assert F(1, 2) == V("0.5")
    its.append(mcq("Which decimal is equal to %s?" % fr(3, 4), "0.75", ["3.4", "0.34", "0.25"],
                   "Make hundredths: %s = %s (multiply the top and bottom by 25). 75 hundredths = <b>0.75</b>. "
                   "0.25 is the part that is left over (%s)." % (fr(3, 4), fr(75, 100), fr(1, 4))))
    assert F(3, 4) == V("0.75")
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 5), "0.2", ["1.5", "0.15", "0.5"],
                   "Make tenths: %s = %s (multiply the top and bottom by 2). 2 tenths = <b>0.2</b>. "
                   "0.15 just writes the 1 and the 5 after the point." % (fr(1, 5), fr(2, 10))))
    assert F(1, 5) == V("0.2")
    its.append(mcq(fig(grid_svg(40)) + "The whole grid is 1. Which is <b>not</b> equal to the shaded part?", "0.04",
                   ["0.4", fr(4, 10), fr(40, 100)],
                   "4 full columns are shaded: 4 tenths = 40 hundredths. So 0.4, %s and %s all match. "
                   "<b>0.04</b> is only 4 small squares." % (fr(4, 10), fr(40, 100)), same_ok=True))
    assert V("0.4") == F(4, 10) == F(40, 100) != V("0.04")
    its.append(mcq("Which decimal is equal to %s?" % fr(150, 1000), "0.15", ["1.5", "0.015", "0.51"],
                   "%s = 0.150. A 0 at the end can be dropped: 0.150 = <b>0.15</b>. "
                   "0.015 is %s." % (fr(150, 1000), fr(15, 1000))))
    assert F(150, 1000) == V("0.15")
    its.append(mcq("Which pair is <b>equal</b>?", "0.7 and " + fr(7, 10),
                   ["0.7 and " + fr(7, 100), "0.07 and " + fr(7, 10), "0.007 and " + fr(7, 100)],
                   "0.7 is 7 tenths, so <b>0.7 = %s</b>. 0.07 is %s and 0.007 is %s." % (fr(7, 10), fr(7, 100), fr(7, 1000)),
                   same_ok=True))
    its.append(mcq("Which fraction is <b>between 0.3 and 0.4</b>?", fr(35, 100), [fr(3, 4), fr(4, 100), fr(3, 100)],
                   "%s = 0.35, which is between 0.30 and 0.40. %s = 0.75, %s = 0.04 and %s = 0.03."
                   % (fr(35, 100), fr(3, 4), fr(4, 100), fr(3, 100))))
    assert V("0.3") < F(35, 100) < V("0.4")
    its.append(mcq("Compare %s and 0.65." % fr(3, 5), fr(3, 5) + " &lt; 0.65",
                   [fr(3, 5) + " &gt; 0.65", fr(3, 5) + " = 0.65", "You can’t tell"],
                   "Change %s to a decimal: %s = %s = 0.6. 0.6 = 0.60, and 60 hundredths &lt; 65 hundredths. "
                   "So <b>%s &lt; 0.65</b>." % (fr(3, 5), fr(3, 5), fr(6, 10), fr(3, 5)), same_ok=True))
    assert F(3, 5) < V("0.65")
    right = "0.45, " + fr(1, 2) + ", 0.6"
    its.append(mcq("Order from <b>smallest to greatest</b>: <b>0.6, %s, 0.45</b>" % fr(1, 2), right,
                   ["0.6, 0.45, " + fr(1, 2), fr(1, 2) + ", 0.45, 0.6", "0.45, 0.6, " + fr(1, 2)],
                   "Change %s to a decimal: 0.5. Now compare 0.60, 0.50 and 0.45: <b>0.45, %s, 0.6</b>. "
                   "%s is not the smallest just because 1 and 2 are small digits." % (fr(1, 2), fr(1, 2), fr(1, 2)),
                   same_ok=True))
    assert V("0.45") < F(1, 2) < V("0.6")
    its.append(mcq("Ji-woo says 0.3 = %s. What is correct?" % fr(3, 100), "0.3 is 3 tenths, so 0.3 = " + fr(3, 10),
                   ["0.3 = " + fr(3, 1000), "0.3 = " + fr(1, 3), "Ji-woo is right: 0.3 = " + fr(3, 100)],
                   "The 3 is in the first place after the point, the tenths place. So <b>0.3 = %s</b>. "
                   "%s is 0.03 (two places)." % (fr(3, 10), fr(3, 100)), same_ok=True))
    assert len(its) == 20, len(its)
    return {"title": "Decimals and fractions", "items": its}


# ============================================================ set 5: rounding and word problems
def round_e(x, places):
    """Explanation for rounding decimal string x to `places` places (0 = whole number, 1 = tenth, 2 = hundredth)."""
    q = Dm(1).scaleb(-places)
    lo = Dm(x).quantize(q, rounding="ROUND_FLOOR")
    hi = lo + q
    r = Dm(rnd_to(x, places))
    nxt = {0: "tenths", 1: "hundredths", 2: "thousandths"}[places]
    f = x.partition(".")[2]
    d = int(f[places])
    s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s to <b>%s</b>."
         % (x, lo, hi, nxt, d, "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down", r))
    return s


def round_line(x):
    """Number line from the tenth below x to the tenth above (x in hundredths), red dot at x."""
    v = int(Dm(x) * 1000)
    lo = v // 100 * 100
    return fig(line_svg(lo, lo + 100, 10, labels=[lo, lo + 50, lo + 100], dots=[(v, None)]))


def rq(x, places, wrong, extra="", stem=None, fig_=False, unit="", right=None):
    right = (right or rnd_to(x, places)) + unit
    assert V(right.replace(unit, "")) == V(rnd_to(x, places))
    place = {0: "whole number", 1: "tenth", 2: "hundredth"}[places]
    q = (round_line(x) if fig_ else "") + (stem or "Round <b>%s</b> to the nearest %s." % (x, place))
    return mcq(q, right, [w + unit for w in wrong], round_e(x, places) + extra)


def set_round_problems():
    its = []
    its.append(rq("2.47", 1, ["2.4", "3", "2"], " The dot is closer to 2.5 than to 2.4.", fig_=True,
                  stem="Round the number at the red dot (2.47) to the nearest tenth."))
    its.append(rq("6.381", 2, ["6.39", "6.4", "6.3"], " 6.4 rounds to the nearest tenth instead of the nearest hundredth."))
    its.append(rq("4.65", 0, ["4", "4.7", "4.6"], " The nearest whole number has no decimal places, so 4.7 is not the answer."))
    its.append(rq("3.952", 1, ["3.9", "3.10", "3.95"], " The answer is written 4.0 to show tenths. "
                  "3.10 is wrong: 10 tenths make 1 whole."))
    its.append(rq("7.049", 1, ["7.1", "7.05", "7.4"], " Do not round the 9 first: "
                  "7.049 is closer to 7.0 than to 7.1."))
    its.append(mcq("Which number rounds to <b>5.3</b> when you round to the nearest tenth?", "5.348",
                   ["5.351", "5.249", "5.36"],
                   "Look at the hundredths digit. 5.348 has 4 hundredths, so it rounds down to <b>5.3</b> "
                   "(do not round the 8 first). 5.351 and 5.36 round up to 5.4, and 5.249 rounds to 5.2."))
    assert [rnd_to(x, 1) for x in ("5.348", "5.351", "5.249", "5.36")] == ["5.3", "5.4", "5.2", "5.4"]
    its.append(mcq("To round <b>8.274</b> to the nearest hundredth, which digit do you look at?", "the 4 (thousandths)",
                   ["the 7 (hundredths)", "the 2 (tenths)", "the 8 (ones)"],
                   "To round to the nearest hundredth, look one place to the right of the hundredths: the thousandths digit. "
                   "It is <b>4</b>, so 8.274 rounds down to 8.27.", same_ok=True))
    assert rnd_to("8.274", 2) == "8.27"
    its.append(rq("0.746", 2, ["0.74", "0.7", "0.8"], " Answer: about 0.75 kg.", unit=" kg",
                  stem="A bag of trail mix for a hike in Stanley Park has a mass of 0.746 kg. "
                       "What is its mass to the nearest hundredth of a kilogram?"))
    # word problems in BC contexts
    its.append(rq("4.386", 1, ["4.3", "4.39", "4"], " Answer: about 4.4 km. 4.39 km is rounded to the nearest hundredth.",
                  unit=" km",
                  stem="At the Terry Fox Run, Ava runs 4.386 km. How far is that to the nearest tenth of a kilometre?"))
    its.append(rq("3.752", 2, ["3.76", "3.8", "3.7"], " Answer: about 3.75 kg.", unit=" kg",
                  stem="A salmon caught on the Fraser River has a mass of 3.752 kg. "
                       "What is its mass to the nearest hundredth of a kilogram?"))
    its.append(rq("8.47", 0, ["9", "8.5", "8.4"], " Answer: about 8 cm. 9 cm comes from rounding twice "
                  "(8.47 → 8.5 → 9). Round only once, from the tenths digit.", unit=" cm",
                  stem="In one rainy week in Vancouver, 8.47 cm of rain falls. What is that to the nearest centimetre?"))
    its.append(rq("6.27", 1, ["6.2", "6", "7"], " Answer: about 6.3 g.", unit=" g",
                  stem="A loonie has a mass of 6.27 g. What is its mass to the nearest tenth of a gram?"))
    its.append(mcq("A bag of cherries at a fruit stand in the Okanagan costs $4.85. What is the price to the nearest dollar?",
                   "$5", ["$4", "$4.90", "$4.80"],
                   "$4.85 is between $4 and $5. Look at the tenths digit: 8. That is 5 or more, so round up to <b>$5</b>. "
                   "$4.90 rounds to the nearest 10¢, not the nearest dollar."))
    assert rnd_to("4.85", 0) == "5"
    its.append(mcq("At a track meet in Kamloops, Liam’s long jump is 2.45 m and Mateo’s is 2.405 m. Who jumped farther?",
                   "Liam", ["Mateo", "They jumped the same distance", "You can’t tell"],
                   "Write both with thousandths: 2.450 m and 2.405 m. 450 &gt; 405 thousandths, so <b>Liam</b> jumped farther. "
                   "2.405 has more digits, but that does not make it greater.", same_ok=True))
    assert V("2.45") > V("2.405")
    its.append(mcq("Three snowboarders race at Whistler. Kai finishes in 48.36 seconds, Owen in 48.4 seconds and "
                   "Zara in 48.305 seconds. Who is the fastest?", "Zara", ["Kai", "Owen", "They tie"],
                   "The fastest racer has the <b>least</b> time. Write the times with thousandths: 48.360, 48.400 and 48.305. "
                   "48.305 is the least, so <b>Zara</b> is the fastest.", same_ok=True))
    assert min(V("48.36"), V("48.4"), V("48.305")) == V("48.305")
    its.append(mcq("Three sockeye salmon have masses of 2.5 kg, 2.35 kg and 2.475 kg. "
                   "Order the masses from <b>lightest to heaviest</b>.", "2.35 kg, 2.475 kg, 2.5 kg",
                   ["2.5 kg, 2.35 kg, 2.475 kg", "2.475 kg, 2.35 kg, 2.5 kg", "2.5 kg, 2.475 kg, 2.35 kg"],
                   "Write them with thousandths: 2.500, 2.350 and 2.475. 350 &lt; 475 &lt; 500, so the order is "
                   "<b>2.35 kg, 2.475 kg, 2.5 kg</b>.", same_ok=True))
    assert V("2.35") < V("2.475") < V("2.5")
    its.append(mcq("On a hike up Grouse Mountain, Noah drinks 0.6 L of water and Chloe drinks 0.58 L. "
                   "Chloe says she drank more because 58 &gt; 6. Who drank more?", "Noah",
                   ["Chloe", "They drank the same amount", "You can’t tell"],
                   "0.6 L = 0.60 L. 60 hundredths &gt; 58 hundredths, so <b>Noah</b> drank more. "
                   "Compare place by place: 6 tenths &gt; 5 tenths.", same_ok=True))
    assert V("0.6") > V("0.58")
    its.append(mcq("Hana’s water bottle holds 0.75 L. What fraction of a litre is that?", fr(3, 4) + " L",
                   [fr(7, 5) + " L", fr(75, 1000) + " L", fr(1, 4) + " L"],
                   "0.75 = %s = <b>%s</b>. %s is 0.075, and %s is 0.25." % (fr(75, 100), fr(3, 4), fr(75, 1000), fr(1, 4))))
    assert V("0.75") == F(3, 4)
    its.append(mcq("A cedar seedling in a school garden in Nanaimo is 0.375 m tall. Which fraction of a metre is that?",
                   fr(375, 1000) + " m", [fr(375, 100) + " m", fr(375, 10) + " m", fr(3, 10) + " m"],
                   "0.375 has three places after the point, so it means thousandths: <b>%s m</b>. "
                   "%s m would be 3.75 m, taller than a door." % (fr(375, 1000), fr(375, 100))))
    assert V("0.375") == F(375, 1000)
    its.append(rq("2.396", 2, ["2.39", "2.310", "2.3"], " Answer: 2.40 m. 9 hundredths and 1 more make 10 hundredths, "
                  "which is 1 more tenth. 2.310 is wrong: 10 hundredths cannot go in one place.", unit=" m",
                  right="2.40",
                  stem="A tent pole for a camping trip on Vancouver Island is 2.396 m long. "
                       "What is its length to the nearest hundredth of a metre?"))
    assert len(its) == 20, len(its)
    return {"title": "Round decimals and word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg("2.635")
    f_cmp = svg_wrap(452, 222, "".join([
        grid_body(45, 6, 6, 18), text(96, 214, "0.45", 18),
        grid_body(50, 266, 6, 18), text(356, 214, "0.5 = 0.50", 18),
    ]), "two hundred grids: 45 squares shaded for 0.45 and 50 squares shaded for 0.5")
    f_line = line_svg(240, 250, 10, dots=[(247, None)])
    f_round = line_svg(2400, 2500, 10, labels=[2400, 2450, 2500], dots=[(2470, None)])
    return (
        "<h2>Tenths, hundredths and thousandths</h2>"
        "<p>Split 1 whole into 10 equal parts: each part is one <b>tenth</b> (0.1). "
        "Split it into 100 parts: each part is one <b>hundredth</b> (0.01). "
        "Split it into 1000 parts: each part is one <b>thousandth</b> (0.001). "
        "Each place is worth 10 times the place to its right.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>2.635 = 2 ones, 6 tenths, 3 hundredths and 5 thousandths = 2 + 0.6 + 0.03 + 0.005.</figcaption></figure>"
        "<p>Between two hundredths there are 10 thousandths. From 0.24 to 0.25, each small space is 0.001.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>The dot is 7 thousandths after 0.240, so it shows 0.247.</figcaption></figure>"
        "<h2>Reading and writing decimals</h2>"
        "<p>Say “and” for the decimal point. Then read the digits after the point and say the place of the "
        "<b>last</b> digit. Use a 0 to hold an empty place.</p>"
        + table(["Decimal", "In words", "Fraction"], [
            ["0.6", "six tenths", fr(6, 10)],
            ["0.45", "forty-five hundredths", fr(45, 100)],
            ["2.007", "two and seven thousandths", "2 " + fr(7, 1000)],
            ["0.312", "three hundred twelve thousandths", fr(312, 1000)]])
        + ex("Example 1", "Write twelve and forty-six thousandths as a decimal.",
             "Thousandths need three places after the point: 46 thousandths = 0.046.", "12.046")
        + "<h2>Comparing and ordering</h2>"
        "<p>Compare the whole numbers first, then the tenths, then the hundredths, then the thousandths. "
        "It helps to give the numbers the same number of places: 0.5 = 0.50 = 0.500.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.45 = 45 hundredths and 0.5 = 50 hundredths. So 0.45 &lt; 0.5, even though 45 is more than 5."
        "</figcaption></figure>"
        + ex("Example 2", "Order 0.5, 0.45 and 0.405 from smallest to greatest.",
             "Write them with thousandths: 0.500, 0.450, 0.405.", "0.405, 0.45, 0.5")
        + "<h2>Decimals and fractions</h2>"
        "<p>The number of places after the point tells you the denominator: one place is tenths, two places is hundredths, "
        "three places is thousandths. 0.3 = " + fr(3, 10) + ", 0.03 = " + fr(3, 100) + " and 0.003 = " + fr(3, 1000) + ". "
        "Some fractions are worth knowing by heart: " + fr(1, 2) + " = 0.5, " + fr(1, 4) + " = 0.25, "
        + fr(3, 4) + " = 0.75 and " + fr(1, 5) + " = 0.2.</p>"
        + ex("Example 3", "Write 0.125 as a fraction.",
             "There are three places after the point, so it is thousandths.", fr(125, 1000))
        + "<h2>Rounding decimals</h2>"
        "<p>Find the two numbers it is between. Look at the digit <b>one place to the right</b> of the place you are "
        "rounding to: 5 or more rounds up, 4 or less rounds down. Round only once.</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>2.47 is between 2.4 and 2.5. The hundredths digit is 7, so 2.47 rounds up to 2.5.</figcaption></figure>"
        + ex("Example 4", "Round 6.381 to the nearest hundredth.",
             "6.381 is between 6.38 and 6.39. The thousandths digit is 1, so round down.", "6.38")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because 45 &gt; 5", "Use the same places: 0.45 &lt; 0.50"],
            ["0.3 = " + fr(3, 100), "One place after the point is tenths: 0.3 = " + fr(3, 10)],
            ["Writing twenty-three thousandths as 0.23", "Thousandths need three places: 0.023"],
            ["Rounding 5.348 to 5.4 by rounding the 8 first", "Look only at the hundredths digit: 5.348 → 5.3"],
            ["Rounding 3.952 to 3.10", "10 tenths make 1 whole: 3.952 → 4.0"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about decimals in BC?",
     "a": "The BC Grade 5 math curriculum includes decimals to thousandths. Students read, write, compare and order decimals like 2.635, connect them to fractions such as 0.125 = 125/1000, and round decimals."},
    {"q": "How do you explain thousandths to a child?",
     "a": "Split a hundredth into 10 equal parts and each part is a thousandth, 0.001. On a number line from 0.24 to 0.25, the 10 small spaces are thousandths, so 7 spaces past 0.24 is 0.247."},
    {"q": "Why is 0.5 bigger than 0.45?",
     "a": "The 5 in 0.5 means 5 tenths, which is 50 hundredths. 0.45 is only 45 hundredths, so 0.5 is bigger even though it has fewer digits."},
    {"q": "Is 0.3 equal to 3/10 or 3/100?",
     "a": "0.3 = 3/10, because the 3 is in the first place after the decimal point, the tenths place. 3/100 is written 0.03."},
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
    """Tag pictures that must print larger (number lines, place value charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(55802)
    sets = [set_places(), set_read_write(), set_compare(), set_fractions(), set_round_problems()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "decimals-to-thousandths", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Decimals to Thousandths",
        "seo_title": "Grade 5 Decimals to Thousandths Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Decimals to thousandths",
        "domain": "Number",
        "standard_code": "Grade 5: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Decimals to thousandths",
        "meta_desc": "Free Grade 5 math worksheets on decimals to thousandths for the BC curriculum: place value charts, reading and writing decimals like 2.007, comparing and ordering, decimals and fractions such as 0.3 = 3/10, and rounding. 100 questions with an answer key.",
        "key_big": "Tenths, hundredths and thousandths are the first, second and third places after the decimal point. 0.3 = 3/10, 0.03 = 3/100 and 0.003 = 3/1000.",
        "key_sub": "Compare by place value, not by length: 0.45 < 0.50, so 0.45 < 0.5. To round, look one place to the right: 6.381 rounds to 6.38 and 2.47 rounds to 2.5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "(number line|place value chart)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
