# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Decimals (Australian Curriculum v9.0, AC9M5N01)
  python3 tools/gen_au_maths_y5_decimals.py
Place value to thousandths, decimals as fractions and mixed numerals, comparing and ordering decimals
(including numbers greater than one), decimals on a number line, and word problems.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Australian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
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


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)( .+)?$")


def val(c):
    """Value of a choice (Fraction) with its unit; None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    return (F(m.group(2)), "$" if m.group(1) else (m.group(3) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False):
    """4 choices: correct first + 3 wrong. No two choices may have the same value
    (same_ok=True only for questions whose choices are not plain numbers)."""
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


def dec(v):
    """Exact decimal text of a Fraction with a terminating decimal (no trailing zeros)."""
    v = F(v)
    d = Dm(v.numerator) / Dm(v.denominator)
    assert F(d) == v, v
    s = format(d.normalize(), "f")
    return s


def D(s):
    return F(Dm(s))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


# ------------------------------------------------------------ pictures
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


def line_svg(a, b, spaces, labels, dots=(), W=420):
    """Number line from a to b (in thousandths, integers) with `spaces` equal spaces.
    labels: thousandths values written under the line (must sit on a tick).
    dots: list of (value, letter or None). A dot may sit between ticks. Letters are written above the dot."""
    lettered = any(l for _, l in dots)
    L, R = 30, W - 30
    Y = 44 if lettered else 30
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
        s.append(text(X(v), Y + 36, dec(F(v, 1000)), 17))
    xs = []
    for v, l in dots:
        assert a <= v <= b
        xs.append(X(v))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(v), Y, RED if not l else BLUE))
        if l:
            s.append(text(X(v), Y - 18, l, 17))
    xs.sort()
    assert all(q - p >= 18 for p, q in zip(xs, xs[1:])), (a, b, dots)
    lab = "number line from %s to %s split into %d equal spaces" % (dec(F(a, 1000)), dec(F(b, 1000)), spaces)
    if lettered:
        lab += " with points %s" % ", ".join(l for _, l in dots)
    return svg_wrap(W, Y + 46, "".join(s), lab)


def dot_q(a, b, spaces, labels, dot, wrong, e, stem="What number is at the red dot?", unit=""):
    right = dec(F(dot, 1000)) + unit
    return mcq(fig(line_svg(a, b, spaces, labels, [(dot, None)])) + stem, right, [w + unit for w in wrong], e)


# ============================================================ set 1: place value to thousandths
def set_place_value():
    its = []
    its.append(mcq(fig(chart_svg(["3.407"], hi=(0, -3))) + "What is the value of the red digit in 3.407?",
                   "7 thousandths", ["7 hundredths", "7 tenths", "7 ones"],
                   "The red 7 is the <b>third</b> digit after the decimal point, in the thousandths column. "
                   "Its value is <b>7 thousandths</b> = 0.007. The 0 holds the hundredths place."))
    its.append(mcq(fig(chart_svg(["5.064"], hi=(0, -2))) + "What is the value of the red digit in 5.064?",
                   "6 hundredths", ["6 tenths", "6 thousandths", "6 ones"],
                   "The red 6 is the <b>second</b> digit after the decimal point, in the hundredths column. "
                   "Its value is <b>6 hundredths</b> = 0.06."))
    its.append(mcq(fig(chart_svg(["12.583"], hi=(0, -1))) + "What is the value of the red digit in 12.583?",
                   "5 tenths", ["5 hundredths", "5 ones", "5 tens"],
                   "The red 5 is the <b>first</b> digit after the decimal point, in the tenths column. "
                   "Its value is <b>5 tenths</b> = 0.5."))
    its.append(mcq("What is the value of the digit <b>9</b> in <b>6.192</b>?", "0.09", ["0.9", "0.009", "9"],
                   "6 . 1 <b>9</b> 2: the 9 is the second digit after the point, in the hundredths place. "
                   "It is worth 9 hundredths = <b>0.09</b>."))
    its.append(mcq("In which place is the digit <b>4</b> in <b>0.024</b>?", "thousandths",
                   ["hundredths", "tenths", "ones"],
                   "0 . 0 2 <b>4</b>: tenths, hundredths, thousandths. The 4 is in the <b>thousandths</b> place.",
                   same_ok=True))
    its.append(mcq("In <b>8.346</b>, which digit is in the <b>hundredths</b> place?", "4", ["3", "6", "8"],
                   "After the point the places are tenths (3), hundredths (4) and thousandths (6). "
                   "So the hundredths digit is <b>4</b>."))
    its.append(mcq("In <b>15.208</b>, which digit is in the <b>thousandths</b> place?", "8", ["0", "2", "5"],
                   "After the point: tenths 2, hundredths 0, thousandths 8. The thousandths digit is <b>8</b>."))
    its.append(mcq("Write <b>3 ones, 5 hundredths and 2 thousandths</b> as a decimal.", "3.052", ["3.52", "3.502", "3.0052"],
                   "There are 0 tenths, so write a 0 in the tenths place: 3 . 0 5 2 = <b>3.052</b>. "
                   "3.52 would have 5 tenths."))
    its.append(mcq("4 + 0.6 + 0.03 + 0.009 = ?", "4.639", ["4.936", "46.39", "4.0639"],
                   "4 ones, 6 tenths, 3 hundredths and 9 thousandths: 4 . 6 3 9 = <b>4.639</b>."))
    its.append(mcq("7 + 0.08 + 0.005 = ?", "7.085", ["7.85", "7.805", "7.0805"],
                   "There are no tenths, so the tenths digit is 0: 7 . 0 8 5 = <b>7.085</b>. "
                   "7.85 forgets the 0 that holds the tenths place."))
    its.append(mcq("Which shows <b>2.716</b> in expanded form?", "2 + 0.7 + 0.01 + 0.006",
                   ["2 + 0.7 + 0.1 + 0.06", "2 + 7 + 1 + 6", "2 + 0.07 + 0.001 + 0.6"],
                   "2 ones, 7 tenths, 1 hundredth and 6 thousandths: <b>2 + 0.7 + 0.01 + 0.006</b>.", same_ok=True))
    its.append(mcq("1 hundredth is split into 10 equal parts. What decimal is each part?", "0.001", ["0.01", "0.1", "0.0001"],
                   "A hundredth divided by 10 is a <b>thousandth</b>: %s = <b>0.001</b>. "
                   "1 whole = 10 tenths = 100 hundredths = 1000 thousandths." % fr(1, 1000)))
    its.append(mcq("How many thousandths are there in <b>1 hundredth</b>?", "10", ["100", "1000", "0.1"],
                   "1 hundredth = 0.01 = 0.010. That is <b>10</b> thousandths."))
    its.append(mcq("How many thousandths are there in <b>0.3</b>?", "300", ["3", "30", "3000"],
                   "1 tenth = 100 thousandths, so 3 tenths = <b>300</b> thousandths. 0.3 = 0.300."))
    its.append(mcq("Which number is equal to <b>0.6</b>?", "0.600", ["0.06", "0.006", "6.00"],
                   "A 0 at the <b>end</b> of a decimal does not change its value: 0.6 = 0.60 = <b>0.600</b>. "
                   "0.06 and 0.006 have the 6 in a different place."))
    its.append(mcq("In <b>5.55</b>, the 5 in the tenths place is worth how many times the 5 in the hundredths place?",
                   "10", ["100", "1000", "5"],
                   "Each place is worth <b>10 times</b> the place to its right. 0.5 = 10 × 0.05. So the answer is <b>10</b>."))
    its.append(mcq("What number is <b>0.001 more</b> than 4.209?", "4.21", ["4.219", "4.2010", "4.309"],
                   "9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. So 4.209 + 0.001 = 4.210 = <b>4.21</b>. "
                   "4.219 adds 1 hundredth, not 1 thousandth."))
    assert D("4.209") + D("0.001") == D("4.21")
    its.append(mcq("What number is <b>0.01 more</b> than 2.396?", "2.406", ["2.397", "2.496", "2.3106"],
                   "Add 1 hundredth: 9 hundredths + 1 hundredth = 10 hundredths = 1 tenth. "
                   "So 2.396 + 0.01 = <b>2.406</b>. 2.397 adds only 1 thousandth."))
    assert D("2.396") + D("0.01") == D("2.406")
    its.append(mcq("What number is <b>0.1 less</b> than 6.05?", "5.95", ["6.04", "6.15", "5.05"],
                   "Take away 1 tenth. 6.05 has 0 tenths, so regroup 1 one as 10 tenths: 6.05 − 0.1 = <b>5.95</b>. "
                   "6.04 takes away 1 hundredth."))
    assert D("6.05") - D("0.1") == D("5.95")
    its.append(mcq("Use each of the digits <b>3, 8, 1, 5</b> once to make the <b>greatest</b> number with "
                   "1 digit before the decimal point and 3 digits after it.", "8.531", ["8.513", "1.358", "5.831"],
                   "Put the largest digit in the ones place, then the next largest in the tenths, hundredths and thousandths: "
                   "<b>8.531</b>. 1.358 is the smallest number."))
    order = [0, 1, 2, 3, 5, 4, 6, 14, 7, 9, 8, 10, 11, 12, 13, 15, 16, 17, 18, 19]
    return {"title": "Place value to thousandths", "items": reorder(its, order)}


# ============================================================ set 2: decimals and fractions
def set_fractions():
    its = []
    for d_, (n, dd), wrong, e in [
        ("0.3", (3, 10), [fr(3, 100), fr(1, 3), fr(3, 1000)],
         "0.3 has <b>one</b> decimal place, so the 3 is in the tenths place: 3 tenths = <b>%s</b>." % fr(3, 10)),
        ("0.71", (71, 100), [fr(7, 10), fr(71, 10), fr(71, 1000)],
         "0.71 has <b>two</b> decimal places, so it is hundredths: 71 hundredths = <b>%s</b>. "
         "%s would be 7.1." % (fr(71, 100), fr(71, 10))),
        ("0.09", (9, 100), [fr(9, 10), fr(9, 1000), fr(1, 9)],
         "Two decimal places means hundredths. The tenths digit is 0, so 0.09 = 9 hundredths = <b>%s</b>." % fr(9, 100)),
        ("0.045", (45, 1000), [fr(45, 100), fr(45, 10), fr(5, 1000)],
         "0.045 has <b>three</b> decimal places, so it is thousandths: 45 thousandths = <b>%s</b>. "
         "%s would be 0.45." % (fr(45, 1000), fr(45, 100))),
        ("0.007", (7, 1000), [fr(7, 100), fr(7, 10), fr(1, 7)],
         "0.007 has three decimal places, so the 7 is in the thousandths place: <b>%s</b>. "
         "%s would be 0.07." % (fr(7, 1000), fr(7, 100))),
        ("0.453", (453, 1000), [fr(453, 100), fr(453, 10), fr(3, 1000)],
         "Three decimal places means thousandths: 0.453 = 453 thousandths = <b>%s</b>. "
         "%s is only the last digit." % (fr(453, 1000), fr(3, 1000))),
    ]:
        assert D(d_) == F(n, dd)
        its.append(mcq("Write <b>%s</b> as a fraction." % d_, fr(n, dd), wrong, e))
    for (n, dd), right, wrong, e in [
        ((29, 100), "0.29", ["2.9", "0.029", "29"],
         "29 hundredths: the last digit goes in the <b>second</b> place after the point. %s = <b>0.29</b>." % fr(29, 100)),
        ((7, 1000), "0.007", ["0.07", "0.7", "0.0007"],
         "7 thousandths: the 7 goes in the <b>third</b> place after the point. Write 0s in the tenths and hundredths places: "
         "<b>0.007</b>."),
        ((63, 1000), "0.063", ["0.63", "6.3", "0.0063"],
         "63 thousandths = 6 hundredths and 3 thousandths. The last digit must be in the third place: <b>0.063</b>. "
         "0.63 would be 63 hundredths."),
    ]:
        assert D(right) == F(n, dd)
        its.append(mcq("Write %s as a decimal." % fr(n, dd), right, wrong, e))
    its.append(mcq("Write <b>2.3</b> as a mixed numeral.", mixed(2, 3, 10), [mixed(2, 3, 100), fr(23, 100), mixed(3, 2, 10)],
                   "2 wholes, then 0.3 = 3 tenths. So 2.3 = <b>%s</b>. %s would be 2.03." % (mixed(2, 3, 10), mixed(2, 3, 100))))
    its.append(mcq("Write <b>2.09</b> as a mixed numeral.", mixed(2, 9, 100), [mixed(2, 9, 10), fr(29, 100), mixed(2, 9, 1000)],
                   "2 wholes, then 0.09 = 9 hundredths. So 2.09 = <b>%s</b>. %s would be 2.9." % (mixed(2, 9, 100), mixed(2, 9, 10))))
    its.append(mcq("Write <b>4.125</b> as a mixed numeral.", mixed(4, 125, 1000),
                   [mixed(4, 125, 100), mixed(4, 125, 10), fr(125, 1000)],
                   "4 wholes, then 0.125 has three decimal places = 125 thousandths. So 4.125 = <b>%s</b>. "
                   "Do not forget the 4 wholes." % mixed(4, 125, 1000)))
    for (w, n, dd), right, wrong, e in [
        ((3, 7, 10), "3.7", ["3.07", "37", "0.37"],
         "3 wholes and 7 tenths. Tenths are the first place after the point: <b>3.7</b>."),
        ((5, 6, 100), "5.06", ["5.6", "5.006", "56"],
         "5 wholes and 6 hundredths. The 6 must be in the <b>second</b> place, so write a 0 in the tenths place: <b>5.06</b>."),
        ((12, 48, 1000), "12.048", ["12.48", "12.0048", "1.248"],
         "12 wholes and 48 thousandths. The last digit must be in the <b>third</b> place: <b>12.048</b>. "
         "12.48 would be 12 and 48 hundredths."),
    ]:
        assert D(right) == w + F(n, dd)
        its.append(mcq("Write %s as a decimal." % mixed(w, n, dd), right, wrong, e))
    its.append(mcq("0.35 = %s = %s" % (fr(35, 100), fr("?", 1000)), "350", ["35", "3500", "305"],
                   "Multiply the numerator and the denominator by 10: %s = %s. So the missing number is <b>350</b>. "
                   "0.35 = 0.350." % (fr(35, 100), fr(350, 1000))))
    its.append(mcq("%s + %s + %s = ?" % (fr(6, 10), fr(4, 100), fr(9, 1000)), "0.649", ["0.946", "6.49", "0.0649"],
                   "6 tenths, 4 hundredths and 9 thousandths: 0 . 6 4 9 = <b>0.649</b>."))
    assert F(6, 10) + F(4, 100) + F(9, 1000) == D("0.649")
    its.append(mcq("Which of these is <b>not</b> equal to 0.5?", "0.05", [fr(5, 10), fr(50, 100), fr(500, 1000)],
                   "%s = %s = %s = 0.5. <b>0.05</b> is only 5 hundredths." % (fr(5, 10), fr(50, 100), fr(500, 1000)),
                   same_ok=True))
    its.append(mcq("How many hundredths are there in <b>3.06</b>?", "306", ["36", "360", "6"],
                   "3 wholes = 300 hundredths, and 0.06 = 6 hundredths. 300 + 6 = <b>306</b> hundredths. "
                   "So 3.06 = %s." % fr(306, 100)))
    assert D("3.06") == F(306, 100)
    its.append(mcq("Write <b>two and four hundred and five thousandths</b> as a decimal.", "2.405",
                   ["2.0405", "2405", "2.45"],
                   "2 wholes and 405 thousandths. Thousandths fill <b>three</b> places after the point: <b>2.405</b>. "
                   "2.45 leaves out the 0 in the hundredths place."))
    order = [0, 1, 2, 6, 7, 3, 4, 9, 12, 10, 13, 5, 8, 11, 14, 15, 16, 19, 17, 18]
    return {"title": "Decimals as fractions and mixed numerals", "items": reorder(its, order)}


# ============================================================ set 3: compare and order
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
    assert right in e
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
    its.append(cmp_item("0.98", "1.02", "Compare the ones first: 0 &lt; 1. So <b>0.98 &lt; 1.02</b>. "
                        "Any number less than 1 is smaller than any number greater than 1."))
    its.append(mcq("Which number is the <b>greatest</b>?", "0.7", ["0.68", "0.699", "0.075"],
                   "Write them with 3 places: 0.700, 0.680, 0.699, 0.075. Compare the tenths first: only 0.7 has 7 tenths. "
                   "So <b>0.7</b> is the greatest."))
    its.append(mcq("Which number is the <b>smallest</b>?", "0.205", ["0.25", "0.3", "0.52"],
                   "Write them with 3 places: 0.205, 0.250, 0.300, 0.520. The smallest is <b>0.205</b>, "
                   "even though it has the most digits."))
    its.append(mcq("Which number is the <b>greatest</b>?", "5.1", ["4.987", "5.09", "5.099"],
                   "Compare the ones first: 4.987 has only 4 ones. Then 5.100, 5.090, 5.099: 1 tenth beats 0 tenths. "
                   "So <b>5.1</b> is the greatest."))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.5, 0.45, 0.405</b>", ["0.5", "0.45", "0.405"], True,
                       [["0.5", "0.45", "0.405"], ["0.45", "0.405", "0.5"], ["0.405", "0.5", "0.45"]],
                       "Write them with 3 places: 0.500, 0.450, 0.405. Compare 500, 450 and 405 thousandths. "
                       "So <b>0.405, 0.45, 0.5</b>."))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>1.6, 1.06, 0.96, 1.059</b>",
                       ["1.6", "1.06", "0.96", "1.059"], True,
                       [["1.06", "1.059", "1.6", "0.96"], ["0.96", "1.6", "1.06", "1.059"], ["1.059", "1.06", "1.6", "0.96"]],
                       "0.96 has 0 ones, so it is the smallest. Then write the rest with 3 places: 1.600, 1.060, 1.059. "
                       "So <b>0.96, 1.059, 1.06, 1.6</b>."))
    its.append(order_q("Order from <b>greatest to smallest</b>:<br><b>3.2, 3.18, 3.205, 3.02</b>", ["3.2", "3.18", "3.205", "3.02"],
                       False, [["3.205", "3.18", "3.2", "3.02"], ["3.02", "3.18", "3.2", "3.205"], ["3.2", "3.205", "3.18", "3.02"]],
                       "Write them with 3 places: 3.200, 3.180, 3.205, 3.020. Greatest first: <b>3.205, 3.2, 3.18, 3.02</b>."))
    its.append(order_q("Order from <b>smallest to greatest</b>:<br><b>0.6, 0.06, 0.606, 0.066</b>", ["0.6", "0.06", "0.606", "0.066"],
                       True, [["0.06", "0.6", "0.066", "0.606"], ["0.6", "0.06", "0.066", "0.606"], ["0.066", "0.06", "0.606", "0.6"]],
                       "Write them with 3 places: 0.600, 0.060, 0.606, 0.066. Compare 600, 60, 606 and 66 thousandths. "
                       "So <b>0.06, 0.066, 0.6, 0.606</b>."))
    its.append(order_q("Order from <b>greatest to smallest</b>:<br><b>10.5, 9.75, 10.05, 10.495</b>",
                       ["10.5", "9.75", "10.05", "10.495"], False,
                       [["9.75", "10.495", "10.05", "10.5"], ["10.495", "10.05", "10.5", "9.75"], ["10.5", "10.05", "10.495", "9.75"]],
                       "9.75 is less than 10, so it is the smallest. Then 10.500, 10.495, 10.050. "
                       "Greatest first: <b>10.5, 10.495, 10.05, 9.75</b>."))
    its.append(mcq("Which number is between <b>0.4</b> and <b>0.5</b>?", "0.408", ["0.048", "0.54", "0.399"],
                   "0.4 = 0.400 and 0.5 = 0.500. <b>0.408</b> is between them. 0.048 and 0.399 are less than 0.4, "
                   "and 0.54 is more than 0.5."))
    its.append(mcq("Which number is between <b>2.3</b> and <b>2.31</b>?", "2.305", ["2.35", "2.031", "2.315"],
                   "2.3 = 2.300 and 2.31 = 2.310. <b>2.305</b> is between 2.300 and 2.310. "
                   "2.35 and 2.315 are more than 2.31."))
    assert sum(D(x) > D("0.6") for x in ["0.59", "0.61", "0.596", "0.601"]) == 2
    its.append(mcq("How many of these numbers are <b>greater than 0.6</b>?<br><b>0.59, 0.61, 0.596, 0.601</b>", "2",
                   ["1", "3", "4"],
                   "0.6 = 0.600. Compare: 0.590 &lt; 0.600, 0.610 &gt; 0.600, 0.596 &lt; 0.600, 0.601 &gt; 0.600. "
                   "So <b>2</b> numbers (0.61 and 0.601) are greater."))
    assert D("0.447") < D("0.45") < D("0.457")
    its.append(mcq("0.4□7 &lt; 0.45<br>What is the <b>greatest</b> digit that can go in the box?", "4", ["5", "9", "3"],
                   "0.45 = 0.450. With 4 in the box: 0.447 &lt; 0.450. With 5: 0.457 &gt; 0.450. So the greatest digit is <b>4</b>."))
    order = [0, 1, 3, 4, 7, 2, 5, 6, 8, 9, 11, 10, 16, 12, 13, 17, 14, 15, 18, 19]
    return {"title": "Compare and order decimals", "items": reorder(its, order)}


# ============================================================ set 4: number lines
def set_number_line():
    its = []
    # 0  read 0.7 on a tenths line
    its.append(dot_q(0, 1000, 10, [0, 500, 1000], 700, ["0.07", "7", "0.8"],
                     "The line goes from 0 to 1 in 10 equal spaces, so each space is 1 tenth (0.1). "
                     "The dot is 7 spaces from 0: <b>0.7</b>."))
    # 1  0 to 0.1 in hundredths
    its.append(dot_q(0, 100, 10, [0, 50, 100], 60, ["0.6", "0.006", "0.07"],
                     "The line goes from 0 to 0.1 in 10 equal spaces. 0.1 = 0.10, so each space is 1 hundredth (0.01). "
                     "6 spaces from 0: <b>0.06</b>."))
    # 2  0.3 to 0.4
    its.append(dot_q(300, 400, 10, [300, 400], 380, ["0.308", "0.8", "0.48"],
                     "From 0.3 to 0.4 there are 10 equal spaces, so each space is 1 hundredth. "
                     "Count 8 spaces on from 0.30: <b>0.38</b>."))
    # 3  2.1 to 2.2
    its.append(dot_q(2100, 2200, 10, [2100, 2150, 2200], 2140, ["2.104", "2.4", "2.24"],
                     "From 2.1 to 2.2 there are 10 equal spaces, so each space is 1 hundredth. "
                     "Count 4 spaces on from 2.10: <b>2.14</b>."))
    # 4  1 to 1.1
    its.append(dot_q(1000, 1100, 10, [1000, 1100], 1090, ["1.9", "1.009", "1.08"],
                     "From 1 to 1.1 there are 10 equal spaces, so each space is 1 hundredth. "
                     "9 spaces on from 1.00 is <b>1.09</b>. 1.9 would be much further along, near 2."))
    # 5  2.1 to 2.11 thousandths
    its.append(dot_q(2100, 2110, 10, [2100, 2105, 2110], 2107, ["2.17", "2.117", "2.103"],
                     "From 2.1 to 2.11 there are 10 equal spaces. 2.11 − 2.10 = 0.01, so each space is 1 thousandth. "
                     "Count 7 spaces on from 2.100: <b>2.107</b>."))
    # 6  0.45 to 0.46
    its.append(dot_q(450, 460, 10, [450, 460], 452, ["0.47", "0.472", "0.4502"],
                     "From 0.45 to 0.46 there are 10 equal spaces, so each space is 1 thousandth. "
                     "Count 2 spaces on from 0.450: <b>0.452</b>."))
    # 7  0 to 1 in 5 spaces
    its.append(dot_q(0, 1000, 5, [0, 1000], 600, ["0.3", "0.06", "0.5"],
                     "There are only <b>5</b> spaces from 0 to 1, so each space is 0.2 (1 ÷ 5). "
                     "The dot is 3 spaces along: 0.2, 0.4, <b>0.6</b>. 0.3 counts the spaces as tenths."))
    # 8  0.4 to 0.5 in 5 spaces
    its.append(dot_q(400, 500, 5, [400, 500], 440, ["0.42", "0.402", "0.45"],
                     "There are 5 spaces from 0.4 to 0.5, so each space is 0.1 ÷ 5 = 0.02. "
                     "The dot is 2 spaces along: 0.42, <b>0.44</b>. 0.42 counts each space as 0.01."))
    # 9  1 to 2 in 4 spaces
    its.append(dot_q(1000, 2000, 4, [1000, 2000], 1750, ["1.3", "1.7", "1.8"],
                     "There are 4 spaces from 1 to 2, so each space is 0.25 (a quarter). "
                     "The dot is 3 spaces along: 1.25, 1.5, <b>1.75</b>."))
    # 10 2.1 to 2.12 in 20 spaces
    its.append(dot_q(2100, 2120, 20, [2100, 2110, 2120], 2116, ["2.16", "2.106", "2.126"],
                     "From 2.11 to 2.12 there are 10 spaces, so each space is 1 thousandth. "
                     "The dot is 6 spaces past 2.11 (2.110): <b>2.116</b>."))
    # 11-13 size of each space
    for a, b, sp, labels, right, wrong, e in [
        (600, 700, 10, [600, 700], "0.01", ["0.1", "0.001", "1"],
         "0.7 − 0.6 = 0.1. Split 0.1 into 10 equal spaces: each space is <b>0.01</b> (1 hundredth)."),
        (4250, 4260, 10, [4250, 4260], "0.001", ["0.01", "0.1", "0.0001"],
         "4.26 − 4.25 = 0.01. Split 0.01 into 10 equal spaces: each space is <b>0.001</b> (1 thousandth)."),
        (0, 200, 4, [0, 200], "0.05", ["0.04", "0.02", "0.5"],
         "0.2 − 0 = 0.2 = 20 hundredths. There are <b>4</b> spaces, and 20 ÷ 4 = 5. Each space is <b>0.05</b>. "
         "0.02 assumes there are 10 spaces."),
    ]:
        assert D(right) * sp * 1000 == b - a
        its.append(mcq(fig(line_svg(a, b, sp, labels)) + "How much is each space on this number line worth?",
                       right, wrong, e))
    # 14-16 which point (labels in A, B, C, D order, answer position fixed)
    pts = [(305, "A"), (330, "B"), (350, "C"), (380, "D")]
    its.append(fixed(fig(line_svg(300, 400, 10, [300, 400], pts)) + "Which point shows <b>0.35</b>?",
                     ["A", "B", "C", "D"], 2,
                     "Each space is 0.01. 0.35 = 0.30 + 5 hundredths, so it is 5 spaces along: point <b>C</b>. "
                     "Point A is 0.305, halfway between 0.30 and 0.31."))
    pts = [(2070, "A"), (2300, "B"), (2700, "C"), (2900, "D")]
    its.append(fixed(fig(line_svg(2000, 3000, 10, [2000, 2500, 3000], pts)) + "Which point shows <b>2.07</b>?",
                     ["A", "B", "C", "D"], 0,
                     "Each space is 0.1. 2.07 is less than 2.1, so it sits <b>before</b> the first tick: point <b>A</b>. "
                     "Point C is 2.7."))
    pts = [(1508, "A"), (1530, "B"), (1580, "C"), (1590, "D")]
    its.append(fixed(fig(line_svg(1500, 1600, 10, [1500, 1600], pts)) + "Which point shows <b>1.508</b>?",
                     ["A", "B", "C", "D"], 0,
                     "Each space is 0.01. 1.508 = 1.50 + 8 thousandths. 8 thousandths is less than 1 hundredth, so the point "
                     "is <b>inside the first space</b>, close to 1.51: point <b>A</b>. Point C is 1.58."))
    # 17-19 halfway, closest
    its.append(mcq("What number is <b>halfway</b> between 0.3 and 0.4?", "0.35", ["0.305", "0.34", "0.7"],
                   "0.3 = 0.30 and 0.4 = 0.40. Halfway between 30 and 40 hundredths is 35 hundredths: <b>0.35</b>."))
    assert (D("0.3") + D("0.4")) / 2 == D("0.35")
    its.append(mcq("What number is <b>halfway</b> between 2.45 and 2.46?", "2.455", ["2.405", "2.4505", "2.55"],
                   "2.45 = 2.450 and 2.46 = 2.460. Halfway between 450 and 460 thousandths is 455: <b>2.455</b>."))
    assert (D("2.45") + D("2.46")) / 2 == D("2.455")
    cand = ["0.95", "0.9", "0.909", "0.59"]
    assert min(cand, key=lambda x: abs(1 - D(x))) == "0.95"
    its.append(mcq("On a number line, which number is <b>closest to 1</b>?", "0.95", ["0.9", "0.909", "0.59"],
                   "Find how far each is from 1: 0.05, 0.1, 0.091 and 0.41. The smallest gap is 0.05, so <b>0.95</b> is closest."))
    order = [0, 1, 2, 15, 3, 11, 7, 4, 14, 17, 9, 8, 13, 5, 12, 6, 16, 10, 18, 19]
    return {"title": "Decimals on a number line", "items": reorder(its, order)}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    # long jump
    jumps = [("Oliver", "3.05"), ("Kai", "3.5"), ("Leo", "3.15"), ("Noah", "3.4")]
    best = max(jumps, key=lambda t: D(t[1]))[0]
    assert best == "Kai"
    its.append(mcq("At the athletics carnival, the long jump results are: Oliver 3.05 m, Kai 3.5 m, Leo 3.15 m and "
                   "Noah 3.4 m. Who jumped the <b>furthest</b>?", "Kai", ["Oliver", "Leo", "Noah"],
                   "Write them with 2 places: 3.05, 3.50, 3.15, 3.40. The greatest is 3.50 m, so <b>Kai</b> jumped furthest.",
                   same_ok=True))
    its.append(mcq("Jack ran %s km. Write this distance as a decimal." % mixed(3, 7, 10), "3.7 km",
                   ["3.07 km", "37 km", "0.37 km"],
                   "3 whole kilometres and 7 tenths: <b>3.7 km</b>. 3.07 would be 3 and 7 hundredths."))
    its.append(mcq("Isla’s water bottle holds 0.75 L. Write this as a fraction of a litre.", fr(75, 100) + " L",
                   [fr(75, 10) + " L", fr(75, 1000) + " L", fr(7, 10) + " L"],
                   "0.75 has two decimal places, so it is hundredths: 0.75 L = <b>%s L</b>." % fr(75, 100)))
    its.append(mcq("Lachlan swam 50 m freestyle in 41.27 seconds. What is the value of the digit <b>7</b>?",
                   "7 hundredths of a second", ["7 tenths of a second", "7 seconds", "7 thousandths of a second"],
                   "41.2<b>7</b>: the 7 is the second digit after the point, so it is <b>7 hundredths of a second</b> (0.07 s).",
                   same_ok=True))
    rain = [("Monday", "15.4"), ("Tuesday", "9.8"), ("Wednesday", "15.2"), ("Thursday", "4.6")]
    its.append(mcq("The school rain gauge showed 15.4 mm on Monday, 9.8 mm on Tuesday, 15.2 mm on Wednesday and "
                   "4.6 mm on Thursday. Which day had the <b>most</b> rain?", "Monday", ["Tuesday", "Wednesday", "Thursday"],
                   "Compare the whole numbers first: 15 &gt; 9 &gt; 4. Then 15.4 &gt; 15.2 (4 tenths &gt; 2 tenths). "
                   "So <b>Monday</b> had the most rain.", same_ok=True))
    assert max(rain, key=lambda t: D(t[1]))[0] == "Monday"
    swim = [("Mia", "42.5"), ("Zara", "42.45"), ("Ruby", "42.54"), ("Matilda", "42.6")]
    assert min(swim, key=lambda t: D(t[1]))[0] == "Zara"
    its.append(mcq("At the swimming carnival, the 50 m backstroke times are: Mia 42.5 s, Zara 42.45 s, Ruby 42.54 s and "
                   "Matilda 42.6 s. The <b>fastest</b> time wins. Who won?", "Zara", ["Mia", "Ruby", "Matilda"],
                   "The fastest swimmer has the <b>smallest</b> time. Write them with 2 places: 42.50, 42.45, 42.54, 42.60. "
                   "The smallest is 42.45 s, so <b>Zara</b> won. 42.5 is not less than 42.45.", same_ok=True))
    its.append(mcq("Chloe swam 50 m in 40.5 seconds. Mei swam 50 m in 40.50 seconds. Who was faster?",
                   "They tied", ["Chloe", "Mei", "You can’t tell"],
                   "40.5 = 40.50, because a 0 at the end does not change the value. So <b>they tied</b>.", same_ok=True))
    its.append(mcq("Grace is 1.4 m tall. Her brother is 1.39 m tall. Who is taller?", "Grace",
                   ["her brother", "They are the same height", "You can’t tell"],
                   "1.4 = 1.40. Compare the tenths: 4 &gt; 3. So 1.40 m &gt; 1.39 m and <b>Grace</b> is taller.", same_ok=True))
    swim = [("Cooper", "39.9"), ("Ethan", "39.09"), ("William", "39.19"), ("Liam", "40.01")]
    srt = [n for n, _ in sorted(swim, key=lambda t: D(t[1]))]
    assert srt[1] == "William"
    its.append(mcq("In a 50 m freestyle race the times are: Cooper 39.9 s, Ethan 39.09 s, William 39.19 s and Liam 40.01 s. "
                   "Who came <b>second</b>?", "William", ["Cooper", "Ethan", "Liam"],
                   "Smallest time first: 39.09 (Ethan), 39.19 (William), 39.90 (Cooper), 40.01 (Liam). "
                   "So <b>William</b> came second.", same_ok=True))
    its.append(mcq("Cooper’s time was between 39.8 s and 39.9 s. Which time could it be?", "39.85 s",
                   ["39.09 s", "39.95 s", "39.79 s"],
                   "39.8 = 39.80 and 39.9 = 39.90. Only <b>39.85 s</b> is between them."))
    assert D("39.8") < D("39.85") < D("39.9")
    deli = [("ham", "0.4"), ("cheese", "0.375"), ("salami", "0.35"), ("olives", "0.25")]
    assert max(deli, key=lambda t: D(t[1]))[0] == "ham"
    its.append(mcq("Mum buys 0.375 kg of cheese, 0.4 kg of ham, 0.35 kg of salami and 0.25 kg of olives. "
                   "Which is the <b>heaviest</b>?", "the ham", ["the cheese", "the salami", "the olives"],
                   "Write them with 3 places: 0.375, 0.400, 0.350, 0.250. The greatest is 0.400 kg: <b>the ham</b>.",
                   same_ok=True))
    its.append(mcq("A builder has two boards. One is 1.205 m long and the other is 1.25 m long. Which board is longer?",
                   "the 1.25 m board", ["the 1.205 m board", "They are the same length", "You can’t tell"],
                   "1.25 = 1.250. Compare the hundredths: 5 &gt; 0. So 1.250 &gt; 1.205 and <b>the 1.25 m board</b> is longer.",
                   same_ok=True))
    its.append(order_q("The discus results at the athletics carnival are 12.08 m, 12.8 m and 12.18 m. "
                       "Order them from <b>greatest to smallest</b>.", ["12.08", "12.8", "12.18"], False,
                       [["12.18", "12.08", "12.8"], ["12.08", "12.18", "12.8"], ["12.8", "12.08", "12.18"]],
                       "Write them with 2 places: 12.08, 12.80, 12.18. Greatest first: <b>12.8, 12.18, 12.08</b>."))
    its.append(order_q("Four parcels have masses of 2.4 kg, 2.375 kg, 2.09 kg and 2.5 kg. "
                       "Order them from <b>lightest to heaviest</b>.", ["2.4", "2.375", "2.09", "2.5"], True,
                       [["2.4", "2.5", "2.09", "2.375"], ["2.09", "2.4", "2.5", "2.375"], ["2.5", "2.4", "2.375", "2.09"]],
                       "Write them with 3 places: 2.400, 2.375, 2.090, 2.500. Lightest first: <b>2.09, 2.375, 2.4, 2.5</b>."))
    its.append(mcq("The rain gauge showed 23.4 mm. Write this as a mixed numeral.", mixed(23, 4, 10) + " mm",
                   [mixed(23, 4, 100) + " mm", mixed(2, 34, 100) + " mm", mixed(23, 1, 4) + " mm"],
                   "23 whole millimetres and 4 tenths: 23.4 mm = <b>%s mm</b>." % mixed(23, 4, 10)))
    its.append(dot_q(1200, 1300, 10, [1200, 1300], 1270, ["1.207", "1.7", "1.37"],
                     "From 1.2 m to 1.3 m there are 10 equal spaces, so each space is 0.01 m. "
                     "Count 7 spaces on from 1.20: <b>1.27 m</b>.",
                     stem="Ava marks a measuring tape (in metres) with a red dot. What length does the dot show?", unit=" m"))
    its.append(mcq("Mei measures a screw. It is 0.045 m long. Write this as a fraction of a metre.", fr(45, 1000) + " m",
                   [fr(45, 100) + " m", fr(45, 10) + " m", fr(5, 1000) + " m"],
                   "0.045 has three decimal places, so it is thousandths: 0.045 m = <b>%s m</b> (45 mm). "
                   "%s m would be 0.45 m." % (fr(45, 1000), fr(45, 100))))
    its.append(mcq("The winning time in a race was 35.2 seconds. Which time is <b>1 tenth of a second slower</b>?",
                   "35.3 s", ["35.21 s", "36.2 s", "35.1 s"],
                   "A slower time is a greater number. 35.2 + 0.1 = <b>35.3 s</b>. 35.21 is only 1 hundredth more, "
                   "and 35.1 s would be faster."))
    rib = ["1.505", "1.455", "1.5", "1.05"]
    assert max(rib, key=D) == "1.505"
    its.append(mcq("Sienna cuts four pieces of ribbon: 1.5 m, 1.455 m, 1.05 m and 1.505 m. Which piece is the <b>longest</b>?",
                   "1.505 m", ["1.455 m", "1.5 m", "1.05 m"],
                   "Write them with 3 places: 1.500, 1.455, 1.050, 1.505. The greatest is <b>1.505 m</b>, "
                   "5 thousandths longer than 1.5 m."))
    its.append(mcq("A koala sleeps about 0.8 of a day. Write 0.8 as a fraction in tenths.", fr(8, 10),
                   [fr(8, 100), fr(1, 8), fr(8, 1000)],
                   "0.8 has one decimal place, so it is tenths: 0.8 = <b>%s</b>. Koalas sleep for most of the day." % fr(8, 10)))
    order = [1, 2, 4, 0, 7, 6, 3, 18, 10, 11, 5, 9, 14, 8, 12, 13, 15, 16, 17, 19]
    return {"title": "Decimal word problems", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg(["3.407"], hi=(0, -3))
    f_line = line_svg(2100, 2110, 10, [2100, 2105, 2110], [(2107, None)])
    return (
        "<h2>Place value to thousandths</h2>"
        "<p>Each place is worth <b>10 times</b> the place to its right. After the decimal point come "
        "<b>tenths</b>, <b>hundredths</b> and <b>thousandths</b>. 1 hundredth split into 10 equal parts makes 10 thousandths.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>In 3.407 the 7 is in the thousandths place, so it is worth 7 thousandths = 0.007. "
        "The 0 holds the hundredths place.</figcaption></figure>"
        "<h2>Decimals as fractions and mixed numerals</h2>"
        "<p>The number of decimal places tells you the denominator: one place is tenths, two places are hundredths, "
        "three places are thousandths. A number greater than one becomes a <b>mixed numeral</b>.</p>"
        + table(["Decimal", "Fraction", "Said as"], [
            ["0.7", fr(7, 10), "7 tenths"],
            ["0.71", fr(71, 100), "71 hundredths"],
            ["0.045", fr(45, 1000), "45 thousandths"],
            ["2.3", mixed(2, 3, 10), "2 and 3 tenths"],
            ["2.09", mixed(2, 9, 100), "2 and 9 hundredths"],
        ]) +
        "<h2>Comparing and ordering</h2>"
        "<p>Compare the <b>whole numbers</b> first. Then give the numbers the same number of decimal places by adding "
        "zeros at the end, and compare the digits from the left: tenths, hundredths, thousandths.</p>"
        + ex("Example 1", "Order 0.5, 0.45 and 0.405 from smallest to greatest.",
             "Write 0.500, 0.450 and 0.405. Compare 500, 450 and 405 thousandths.", "0.405, 0.45, 0.5")
        + ex("Example 2", "Order 1.6, 1.06, 0.96 and 1.059 from smallest to greatest.",
             "0.96 has 0 ones, so it is the smallest. Then 1.600, 1.060 and 1.059.", "0.96, 1.059, 1.06, 1.6")
        + "<h2>Decimals on a number line</h2>"
        "<p>First work out what <b>one space</b> is worth: the difference between two labels ÷ the number of spaces. "
        "Then count the spaces from a labelled number.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>From 2.1 to 2.11 there are 10 spaces, so each space is 0.001. The dot is 7 spaces past 2.1: "
        "2.107.</figcaption></figure>"
        + ex("Example 3", "A number line goes from 0.4 to 0.5 in 5 equal spaces. What is the second tick after 0.4?",
             "0.1 ÷ 5 = 0.02, so each space is 0.02. Two spaces: 0.42, 0.44.", "0.44")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.405 &gt; 0.5 because it is longer", "Use the same places: 0.405 &lt; 0.500"],
            ["0.045 = " + fr(45, 100), "Three places means thousandths: " + fr(45, 1000)],
            ["2.3 = " + mixed(2, 3, 100), "One place means tenths: 2.3 = " + mixed(2, 3, 10)],
            ["Every space on a number line is 0.1", "Work out each space first: 5 spaces from 0.4 to 0.5 are 0.02 each"],
            ["A smaller race time loses", "In a race, the smallest time is the fastest"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about decimals in the Australian Curriculum?",
     "a": "In Year 5 (AC9M5N01) students interpret, compare and order decimals with more than 2 decimal places, including numbers greater than one, using place value, and show them on a number line."},
    {"q": "How do you compare decimals with different numbers of decimal places?",
     "a": "Compare the whole numbers first, then add zeros at the end so the decimals have the same number of places and compare from the left. 0.5 = 0.500 and 0.45 = 0.450, so 0.5 is greater even though 0.45 has more digits."},
    {"q": "How do you write a decimal as a fraction or a mixed numeral?",
     "a": "Count the decimal places: one place is tenths, two are hundredths and three are thousandths. So 0.045 = 45/1000 and 2.3 = 2 3/10."},
    {"q": "How do you read decimals on a number line?",
     "a": "Find what one space is worth by dividing the gap between two labels by the number of spaces, then count on from a label. From 2.1 to 2.11 in 10 spaces, each space is 0.001."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines, place value charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(5801)
    sets = [set_place_value(), set_fractions(), set_compare(), set_number_line(), set_problems()]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "decimals", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimals: Thousandths, Comparing and Number Lines",
        "seo_title": "Year 5 Decimals Worksheets: Thousandths, Compare, Order and Number Lines (Free, Answer Key)",
        "short_title": "Decimals",
        "domain": "Number",
        "standard_code": "AC9M5N01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret, compare and order numbers with more than 2 decimal places, including numbers greater than one, using place value understanding; represent these on a number line",
        "meta_desc": "Free Year 5 decimals worksheets for the Australian Curriculum (AC9M5N01): place value to thousandths, decimals as fractions and mixed numerals, comparing and ordering decimals, and number lines. 100 maths questions with an answer key, good NAPLAN practice.",
        "key_big": "Compare decimals by place value, not by length: 0.5 = 0.500 > 0.45 > 0.405.",
        "key_sub": "Three decimal places are thousandths: 0.045 = 45/1000. On a number line, work out what one space is worth before you count.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|place value chart)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
