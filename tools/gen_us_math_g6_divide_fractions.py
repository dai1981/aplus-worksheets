# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Divide Fractions by Fractions (6.NS.A.1)
  python tools/gen_us_math_g6_divide_fractions.py
Grade 6 goes past Grade 5 (unit fractions and whole numbers only):
  any fraction ÷ any fraction, "how many groups" models with partial groups,
  reciprocals and multiplying by the reciprocal, mixed numbers, word problems.
Every answer is computed with fractions.Fraction and checked with multiplication.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
G1 = "#4fae74"        # group color 1
G2 = "#a6dbb7"        # group color 2
PART = "#f3c9c4"      # partial group
LINE = "#2b2b2b"
GRAY = "#8a8178"
RED = "#d6453b"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PARTS = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 9: "ninths",
         10: "tenths", 12: "twelfths", 15: "fifteenths", 18: "eighteenths", 20: "twentieths", 24: "twenty-fourths"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def imp(v):
    """A Fraction as a whole number or a (possibly improper) fraction: 5/2, 3."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def show(v):
    """A positive Fraction in simplest form, mixed when greater than 1: 7/12, 1 1/6, 2."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%d %s" % (w, fr(r, v.denominator))


def neg(v):
    return MINUS + show(v)


def dv(a, b):
    return "%s ÷ %s" % (show(a), show(b))


def lcm(a, b):
    return a * b // gcd(a, b)


def pl(k, one, many):
    return one if k == 1 else many


def mcq(q, correct, cands, e):
    """correct / cands: (html, value) pairs or plain html; a candidate equal in value to the answer is skipped."""
    cv = None
    if isinstance(correct, tuple):
        correct, cv = correct
    seen = {correct}
    vals = {cv} if cv is not None else set()
    pick = []
    for c in cands:
        v = None
        if isinstance(c, tuple):
            c, v = c
        if not c or c in seen or (v is not None and v in vals):
            continue
        seen.add(c)
        if v is not None:
            vals.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (many small pieces) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def svg_num(x, y, v, fs=16, anchor="middle"):
    """A number drawn in SVG: whole, or stacked fraction, or mixed number. y = the middle line.
    Returns (svg, width)."""
    v = F(v)
    cw = fs * 0.6
    w, r = divmod(v.numerator, v.denominator)
    t = "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
    if r == 0:
        width = cw * len(str(w))
        cx = x if anchor == "middle" else x + width / 2
        return t % (cx, y + fs * 0.35, fs, LINE, w), width
    n, d = str(r), str(v.denominator)
    fw = cw * max(len(n), len(d)) + 4
    ww = (cw * len(str(w)) + 3) if w else 0
    width = ww + fw
    left = x - width / 2 if anchor == "middle" else x
    s = ""
    if w:
        s += t % (left + (ww - 3) / 2, y + fs * 0.35, fs, LINE, w)
    fx = left + ww + fw / 2
    s += t % (fx, y - 4, fs, LINE, n)
    s += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>" % (fx - fw / 2 + 1, y, fx + fw / 2 - 1, y, LINE)
    s += t % (fx, y + fs * 0.95 + 1, fs, LINE, d)
    return s, width


def groups_svg(a, b, PW=None):
    """Fraction bar: ceil(a) wholes cut into L pieces each (L = common denominator).
    The first a*L pieces are shaded in groups of b*L pieces (two greens); a partial group is pink.
    Brackets above number the full groups. Labels 0, 1, 2 ... under the whole lines."""
    L = lcm(a.denominator, b.denominator)
    k, m = int(a * L), int(b * L)
    nw = max(1, -(-a.numerator // a.denominator))
    total = nw * L
    if PW is None:
        PW = max(14, min(44, 380 // total))
    X0, T, BH = 14, 34, 34
    W = X0 * 2 + total * PW
    s = []
    full = k // m
    for i in range(total):
        if i < full * m:
            col = G1 if (i // m) % 2 == 0 else G2
        elif i < k:
            col = PART
        else:
            col = "#ffffff"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (X0 + i * PW, T, PW, BH, col, LINE))
    for j in range(nw + 1):
        x = X0 + j * L * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (x, T + BH + 26, LINE, j))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, total * PW, BH, LINE))
    # brackets over groups
    g = 0
    while g * m < k:
        x0 = X0 + g * m * PW + 2
        x1 = X0 + min(k, (g + 1) * m) * PW - 2
        isfull = (g + 1) * m <= k
        colr = LINE if isfull else RED
        s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, T - 4, T - 12, x1, T - 4, colr))
        if isfull:
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % ((x0 + x1) / 2.0, T - 16, LINE, g + 1))
        elif (g + 1) * m <= total:          # dashed: how long a full group would be
            xf = X0 + (g + 1) * m * PW - 2
            s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0, T - 16, T - 24, xf, T - 16, GRAY))
        g += 1
    label = "fraction bar: %s shaded in groups of %s, %d pieces in each whole" % (
        re.sub("<[^>]+>", "", show(a)), re.sub("<[^>]+>", "", show(b)), L)
    return svg_wrap(W, T + BH + 32, "".join(s), label.replace("  ", " "))


def rect_svg(length, area, unit):
    """Rectangle with the length on top, the area inside and a ? on the left side."""
    W, H, X0, T = 210, 92, 40, 46
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#dff1e5' stroke='%s' stroke-width='3'/>" % (X0, T, W, H, LINE)]
    num, w = svg_num(0, 0, length)
    ut = " " + unit
    tot = w + 9.6 * len(ut)
    left = X0 + W / 2.0 - tot / 2
    num, w = svg_num(left, 20, length, anchor="start")
    s.append(num)
    s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s'>%s</text>" % (left + w + 4, 26, LINE, unit))
    s.append("<text x='%d' y='%d' font-size='16' fill='%s' text-anchor='middle'>Area =</text>" % (X0 + W / 2, T + 26, LINE))
    au = " sq " + unit
    num, w = svg_num(0, 0, area)
    tot = w + 9.0 * len(au)
    left = X0 + W / 2.0 - tot / 2
    num, w = svg_num(left, T + 58, area, anchor="start")
    s.append(num)
    s.append("<text x='%.1f' y='%d' font-size='16' fill='%s'>sq %s</text>" % (left + w + 5, T + 64, LINE, unit))
    s.append("<text x='%d' y='%d' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>?</text>" % (X0 - 16, T + H / 2 + 8, RED))
    lab = "rectangle with length %s %s and area %s square %s; the width is unknown" % (
        re.sub("<[^>]+>", "", show(length)), unit, re.sub("<[^>]+>", "", show(area)), unit)
    return svg_wrap(X0 + W + 8, T + H + 6, "".join(s), lab)


# ------------------------------------------------------------ explanations
def as_frac(v, name=None):
    """Sentence that rewrites a whole or mixed number as a fraction (or '')."""
    v = F(v)
    if v.denominator == 1:
        return "Write %d as %s. " % (v.numerator, fr(v.numerator, 1))
    if v > 1:
        return "Write %s as %s. " % (show(v), imp(v))
    return ""


def fstr(v):
    v = F(v)
    return fr(v.numerator, v.denominator)


def check(q, b, a):
    return "Check: %s × %s = %s." % (show(q), show(b), show(a))


def e_rule(a, b):
    q = a / b
    s = as_frac(a) + as_frac(b)
    rb = 1 / b
    n, d = a.numerator * rb.numerator, a.denominator * rb.denominator
    s += "Keep %s, change ÷ to ×, and flip %s to %s: %s × %s = %s" % (
        fstr(a), fstr(b), fstr(rb), fstr(a), fstr(rb), fr(n, d))
    if (n, d) != (q.numerator, q.denominator) or q.denominator == 1 or q > 1:
        s += " = <b>%s</b>. " % show(q)
    else:
        s += ". The answer is <b>%s</b>. " % show(q)
    return s + check(q, b, a)


def e_groups(a, b):
    q = a / b
    L = lcm(a.denominator, b.denominator)
    k, m = int(a * L), int(b * L)
    nm = PARTS[L]
    one = "half" if L == 2 else nm[:-1]
    eq = []
    for v, c in ((a, k), (b, m)):
        if not (v.denominator == L and v < 1):
            eq.append("%s = %s" % (show(v), fr(c, L)))
    s = "Use %s%s. " % (nm, (": " + " and ".join(eq)) if eq else "")
    s += "Each group is %d %s. " % (m, pl(m, one, nm))
    full, r = divmod(k, m)
    if r == 0:
        s += "%d %s make %d ÷ %d = %d %s. " % (k, nm, k, m, full, pl(full, "group", "groups"))
    elif full == 0:
        s += "There %s only %d %s, not enough for a full group. %s %s of a group. " % (
            pl(k, "is", "are"), k, pl(k, one, nm), pl(k, "It is", "They make"), fr(r, m))
    else:
        s += ("%d %s make %d full %s, with %d %s left over. %s %s of a group. "
              % (k, nm, full, pl(full, "group", "groups"), r, pl(r, one, nm),
                 "That 1 " + one + " is" if r == 1 else "Those %d %s are" % (r, nm), fr(r, m)))
    s += "So %s = <b>%s</b>. %s" % (dv(a, b), show(q), check(q, b, a))
    return s


# ------------------------------------------------------------ typical wrong answers
def wrongs(a, b):
    """a ÷ b: (html, value) pairs from real mistakes, most common first."""
    q = a / b
    out = []

    def add(v):
        v = F(v)
        if v > 0:
            out.append((show(v), v))
    add(a * b)                              # multiplied without flipping
    add(1 / q)                              # flipped the first fraction (gives the reciprocal)
    aw, af = divmod(a.numerator, a.denominator)
    if a.denominator > 1 and aw > 0:        # mixed number not converted
        add(aw + F(af, a.denominator) / b)
        add(F(aw + af, a.denominator) / b)  # wrong improper fraction: (w + n)/d
    bw, bf = divmod(b.numerator, b.denominator)
    if b.denominator > 1 and bw > 0:
        if aw > 0 and a.denominator > 1:   # divided whole parts and fraction parts
            add(F(aw, bw) + F(af, a.denominator) / F(bf, b.denominator))
        add(a * (bw + F(b.denominator, bf)))  # flipped only the fraction part of the divisor
    if a.denominator == 1:                  # wrote the whole number n as 1/n
        add(F(1, a.numerator) / b)
    if q.denominator != 1:                  # leftover pieces written as part of a whole
        L = lcm(a.denominator, b.denominator)
        k, m = int(a * L), int(b * L)
        if k > m:
            add(k // m + F(k % m, L))
            add(k // m)                     # dropped the leftover
    add(1 / b)                              # answered for 1 whole, forgot the first number
    add(1 / (a * b))                        # flipped both
    add(q + 1)
    return out


# ============================================================ set 1: how many groups (models)
def set_groups():
    its = []
    fig_items = [(F(3, 4), F(1, 8)), (F(2), F(2, 3)), (F(3, 4), F(3, 8)), (F(5, 6), F(1, 12)),
                 (F(2), F(2, 5)), (F(1, 2), F(1, 6)), (F(4, 3), F(2, 3)), (F(9, 10), F(3, 10)),
                 (F(1), F(2, 3)), (F(3, 4), F(1, 2)), (F(2, 3), F(3, 4)), (F(5, 6), F(1, 3))]
    for a, b in fig_items:
        q = a / b
        txt = ("The bar shows %s. How many groups of %s are in %s?<br>%s = <b>?</b>" % (show(a), show(b), show(a), dv(a, b)))
        if q.denominator != 1:
            txt = ("The bar shows %s. The pink part is not a full group. How many groups of %s are in %s?<br>%s = <b>?</b>"
                   % (show(a), show(b), show(a), dv(a, b)))
        L = lcm(a.denominator, b.denominator)
        nw = max(1, -(-a.numerator // a.denominator))
        w = wrongs(a, b)
        cands = w[:2] + [(str(int(a * L)), F(int(a * L))), (str(nw * L), F(nw * L))] + w[2:]
        its.append(mcq(fig(groups_svg(a, b)) + txt, (show(q), q), cands, e_groups(a, b)))
    for a, b in [(F(2, 3), F(1, 6)), (F(3, 5), F(1, 10)), (F(3, 2), F(1, 4)), (F(2, 3), F(2, 9)),
                 (F(7, 8), F(1, 4)), (F(1, 2), F(3, 4)), (F(4, 5), F(2, 5)), (F(5, 4), F(5, 8))]:
        q = a / b
        txt = "How many groups of %s are in %s?<br>%s = <b>?</b>" % (show(b), show(a), dv(a, b))
        L = lcm(a.denominator, b.denominator)
        w = wrongs(a, b)
        its.append(mcq(txt, (show(q), q), w[:2] + [(str(int(a * L)), F(int(a * L)))] + w[2:], e_groups(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "How many groups? Use a fraction bar", "items": its}


# ============================================================ set 2: reciprocals and the rule
def set_rule():
    its = []
    # reciprocals
    def recip(x, wr, why):
        r = 1 / x
        e = "%sFlip it: the reciprocal is <b>%s</b>. Check: %s × %s = 1. %s" % (
            as_frac(x), imp(r), imp(x), imp(r), why)
        its.append(mcq("What is the reciprocal of %s?" % show(x), (imp(r), r), wr, e.strip()))
    recip(F(3, 5), [(neg(F(3, 5)), F(-3, 5)), (show(F(3, 5)), F(3, 5)), (fr(1, 3), F(1, 3))],
          "The opposite %s is a different idea." % neg(F(3, 5)))
    recip(F(4), [(fr(4, 1), F(4)), (neg(F(4)), F(-4)), (fr(4, 4), F(1))],
          "")
    recip(F(1, 7), [(show(F(1, 7)), F(1, 7)), (neg(F(1, 7)), F(-1, 7)), (fr(7, 7), F(1))],
          "(%s = 7.)" % fr(7, 1))
    recip(F(5, 2), [(fr(5, 2), F(5, 2)), ("4", F(4)), (neg(F(5, 2)), F(-5, 2))],
          "Flipping only the %s part (to get 2 + 2 = 4) is a common mistake." % fr(1, 2))
    e = "A number times its reciprocal is 1. The reciprocal of %s is <b>%s</b>: %s × %s = %s = 1." % (
        fr(7, 9), fr(9, 7), fr(7, 9), fr(9, 7), fr(63, 63))
    its.append(mcq("%s × <b>?</b> = 1" % fr(7, 9), (fr(9, 7), F(9, 7)),
                   [(fr(2, 9), F(2, 9)), (show(F(7, 9)), F(7, 9)), (neg(F(7, 9)), F(-7, 9))],
                   e + " (%s is what you add to %s to make 1, not what you multiply by.)" % (fr(2, 9), fr(7, 9))))

    # rewrite as multiplication
    def rewrite(a, b):
        A, B = imp(a), imp(b)
        Ar, Br = imp(1 / a), imp(1 / b)
        right = "%s × %s" % (A, Br)
        wr = ["%s × %s" % (Ar, B), "%s × %s" % (A, B), "%s × %s" % (Ar, Br)]
        e = ("Keep the first number, change ÷ to ×, and flip only the second number (the divisor). "
             "%s ÷ %s = %s × %s = %s." % (A, B, A, Br, show(a / b)))
        its.append(mcq("Which is the same as %s ÷ %s?" % (A, B), right, wr, e))
    for a, b in [(F(5, 6), F(2, 3)), (F(3, 8), F(1, 4)), (F(4, 5), F(3, 10)), (F(1, 2), F(5, 6)), (F(4), F(2, 3)), (F(3, 4), F(6))]:
        rewrite(a, b)

    # check with multiplication
    def chk(a, b):
        q = a / b
        right = "%s × %s = %s" % (show(b), show(q), show(a))
        wr = ["%s × %s = %s" % (show(a), show(q), show(b)), "%s × %s = %s" % (show(a), show(b), show(q)),
              "%s ÷ %s = %s" % (show(q), show(b), show(a))]
        e = ("Division asks: what times %s gives %s? %s × %s = %s, so %s = %s is correct." % (
            show(b), show(a), show(b), show(q), show(a), dv(a, b), show(q)))
        its.append(mcq("Which equation shows that %s = %s is correct?" % (dv(a, b), show(q)), right, wr, e))
    for a, b in [(F(2, 3), F(3, 4)), (F(5, 6), F(1, 3)), (F(3, 5), F(9, 10)), (F(1, 2), F(3, 8))]:
        chk(a, b)

    # estimate: bigger or smaller
    def est(a, b):
        q = a / b
        A = show(a)
        if b < 1:
            right, why = "Greater than %s" % A, "You divide by a number less than 1, so the quotient is greater than %s (it is %s)." % (A, show(q))
        else:
            right, why = "Less than %s" % A, "You divide by a number greater than 1, so the quotient is less than %s (it is %s)." % (A, show(q))
        wr = ["Greater than %s" % A, "Less than %s" % A, "Equal to %s" % A, "Equal to 1"]
        its.append(mcq("Without computing, %s is ___." % dv(a, b), right, [w for w in wr if w != right], why))
    for a, b in [(F(5, 6), F(1, 3)), (F(3, 4), F(3, 2)), (F(2, 5), F(4, 5))]:
        est(a, b)
    opts = [(F(3, 5), F(1, 2)), (F(1, 2), F(3, 5)), (F(2, 5), F(1, 2)), (F(1, 3), F(3, 4))]
    e = ("A quotient is greater than 1 when the first number is greater than the second. %s is greater than %s, so "
         "%s = %s. The others are less than 1." % (fr(3, 5), fr(1, 2), dv(*opts[0]), show(opts[0][0] / opts[0][1])))
    its.append(mcq("Which quotient is greater than 1?", dv(*opts[0]), [dv(*o) for o in opts[1:]], e))
    opts = [(F(2, 3), F(5, 6)), (F(5, 6), F(2, 3)), (F(3, 4), F(1, 2)), (F(7, 8), F(3, 8))]
    e = ("A quotient is less than 1 when the first number is less than the second. %s is less than %s, so "
         "%s = %s. The others are greater than 1." % (fr(2, 3), fr(5, 6), dv(*opts[0]), show(opts[0][0] / opts[0][1])))
    its.append(mcq("Which quotient is less than 1?", dv(*opts[0]), [dv(*o) for o in opts[1:]], e))
    assert len(its) == 20, len(its)
    return {"title": "Reciprocals and the divide rule", "items": its}


# ============================================================ set 3: fraction ÷ fraction
def set_compute():
    its = []
    pairs = [(F(2, 5), F(1, 3)), (F(3, 8), F(3, 4)), (F(5, 6), F(5, 12)), (F(4, 9), F(2, 3)), (F(7, 10), F(1, 5)),
             (F(3, 4), F(5, 6)), (F(5, 8), F(1, 4)), (F(1, 6), F(2, 3)), (F(9, 10), F(3, 5)), (F(2, 7), F(1, 2)),
             (F(5, 12), F(1, 3)), (F(3, 5), F(4, 5)), (F(1, 4), F(5, 8)), (F(6, 7), F(3, 14)), (F(2, 3), F(5, 6)),
             (F(11, 12), F(1, 6)), (F(3, 10), F(2, 5)), (F(5, 9), F(1, 6))]
    for a, b in pairs:
        q = a / b
        its.append(mcq("%s = <b>?</b>" % dv(a, b), (show(q), q), wrongs(a, b), e_rule(a, b)))
    # missing divisor / dividend
    e = ("The missing number times %s must give %s. So divide: %s ÷ %s = %s × %s = %s = %s. The missing number is <b>%s</b>. Check: %s ÷ %s = %s × %s = %s = %s."
         % (show(F(3, 2)), fr(3, 4), fr(3, 4), fr(3, 2), fr(3, 4), fr(2, 3), fr(6, 12), fr(1, 2), fr(1, 2),
            fr(3, 4), fr(1, 2), fr(3, 4), fr(2, 1), fr(6, 4), show(F(3, 2))))
    its.append(mcq("%s ÷ <b>?</b> = %s" % (fr(3, 4), show(F(3, 2))), (fr(1, 2), F(1, 2)),
                   [(show(F(9, 8)), F(9, 8)), ("2", F(2)), (fr(3, 8), F(3, 8))], e))
    e = ("Multiply to undo the division: <b>?</b> = %s × %s = <b>%s</b>. Check: %s ÷ %s = %s × %s = %s = %s."
         % (fr(4, 3), fr(2, 5), fr(8, 15), fr(8, 15), fr(2, 5), fr(8, 15), fr(5, 2), fr(40, 30), show(F(4, 3))))
    its.append(mcq("<b>?</b> ÷ %s = %s" % (fr(2, 5), show(F(4, 3))), (fr(8, 15), F(8, 15)),
                   [(show(F(10, 3)), F(10, 3)), (show(F(6, 5)), F(6, 5)), (fr(15, 8), F(15, 8))], e))
    assert len(its) == 20, len(its)
    return {"title": "Divide fractions: simplest form", "items": its}


# ============================================================ set 4: mixed numbers and whole numbers
def set_mixed():
    its = []
    pairs = [(F(4), F(2, 3)), (F(3), F(3, 4)), (F(5), F(5, 6)), (F(6), F(4, 5)), (F(2), F(3, 8)),
             (F(4, 3), F(2)), (F(3, 4), F(6)), (F(4, 5), F(2)), (F(2, 3), F(4)),
             (F(5, 2), F(3, 4)), (F(3, 2), F(3, 8)), (F(15, 4), F(5, 8)), (F(9, 4), F(3, 4)), (F(8, 9), F(4, 3)),
             (F(9, 4), F(3, 2)), (F(10, 3), F(5, 3)), (F(7, 4), F(7, 3)), (F(5), F(5, 4)), (F(9, 2), F(3, 2)), (F(7, 2), F(7, 3))]
    for a, b in pairs:
        q = a / b
        its.append(mcq("%s = <b>?</b>" % dv(a, b), (show(q), q), wrongs(a, b), e_rule(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers and whole numbers", "items": its}


# ============================================================ set 5: word problems
def amount(one, many):
    def f(v):
        return "%s %s" % (show(v), one if v <= 1 else many)
    return f


def set_words(P):
    its = []

    def prob(q, a, b, unit, lead, e_extra=""):
        val = a / b
        cands = [(unit(v), v) for h, v in wrongs(a, b)]
        e = "%s: %s = %s × %s = <b>%s</b>. %s%s" % (lead, dv(a, b), imp(a), imp(1 / b), unit(val), check(val, b, a), e_extra)
        its.append(mcq(q, (unit(val), val), cands, e))

    lb = amount("pound", "pounds")
    cup = amount("cup", "cups")
    yd = amount("yard", "yards")
    ft = amount("foot", "feet")
    mi = amount("mile", "miles")
    gal = amount("gallon", "gallons")
    m_ = amount("meter", "meters")

    def count(word1, words):
        return amount(word1, words)

    # 1 sharing chocolate (standard)
    prob("3 friends share %s pound of chocolate equally. How much chocolate does each friend get?" % fr(1, 2),
         F(1, 2), F(3), lb, "Split %s pound into 3 equal parts" % fr(1, 2))
    # 2 yogurt servings (standard)
    def serving(v):
        return "%s of a serving" % show(v) if v < 1 else "%s %s" % (show(v), pl(v, "serving", "servings"))
    prob("One serving of yogurt is %s cup. How many servings are in %s cup of yogurt?" % (fr(3, 4), fr(2, 3)),
         F(2, 3), F(3, 4), serving, "Find how many %s-cup servings fit in %s cup" % (fr(3, 4), fr(2, 3)),
         " There is not enough for 1 full serving, so the answer is less than 1.")
    # 3, 4 rectangles with a figure
    q = (fig(rect_svg(F(3, 4), F(1, 2), "mi")) + "A rectangular strip of land is %s mile long. Its area is %s square mile. How wide is it?"
         % (fr(3, 4), fr(1, 2)))
    prob(q, F(1, 2), F(3, 4), mi, "Area = length × width, so width = area ÷ length")
    q = (fig(rect_svg(F(5, 2), F(15, 4), "yd")) + "A rectangular garden is %s yards long. Its area is %s square yards. How wide is it?"
         % (show(F(5, 2)), show(F(15, 4))))
    prob(q, F(15, 4), F(5, 2), yd, "Width = area ÷ length")
    # 5 ribbon
    nm, he, his = P.next()
    prob("%s has %s yards of ribbon. %s cuts it into pieces that are each %s yard long. How many pieces does %s get?"
         % (nm, show(F(21, 4)), cap(he), fr(3, 4), he), F(21, 4), F(3, 4), count("piece", "pieces"),
         "Find how many %s-yard pieces are in %s yards" % (fr(3, 4), show(F(21, 4))))
    # 6 trail mix
    nm, he, his = P.next()
    prob("%s has %s pounds of trail mix. %s puts %s pound in each bag. How many bags can %s fill?"
         % (nm, show(F(8, 3)), cap(he), fr(1, 3), he), F(8, 3), F(1, 3), count("bag", "bags"),
         "Find how many %s-pound bags are in %s pounds" % (fr(1, 3), show(F(8, 3))))
    # 7 flour
    nm, he, his = P.next()
    prob("%s has 6 cups of flour. One batch of muffins needs %s cup. How many batches can %s make?"
         % (nm, fr(3, 4), he), F(6), F(3, 4), count("batch", "batches"),
         "Find how many %s-cup amounts are in 6 cups" % fr(3, 4))
    # 8 juice glasses
    prob("A pitcher holds %s cups of juice. Each glass holds %s cup. How many glasses can be filled?"
         % (show(F(9, 2)), fr(3, 4)), F(9, 2), F(3, 4), count("glass", "glasses"),
         "Find how many %s-cup glasses are in %s cups" % (fr(3, 4), show(F(9, 2))))
    # 9 walking speed
    nm, he, his = P.next()
    mph = amount("mile per hour", "miles per hour")
    prob("%s walks %s mile in %s hour. At this speed, how far does %s walk in 1 hour?"
         % (nm, fr(3, 4), fr(1, 4), he), F(3, 4), F(1, 4), mph,
         "Divide the distance by the time")
    # 10 paint for a whole wall
    nm, he, his = P.next()
    prob("%s used %s gallon of paint to cover %s of a wall. How much paint does the whole wall need?"
         % (nm, fr(3, 8), fr(3, 4)), F(3, 8), F(3, 4), gal,
         "%s of the wall needs %s gallon. Find the amount for 1 whole wall" % (fr(3, 4), fr(3, 8)))
    # 11 shelves
    nm, he, his = P.next()
    prob("%s cuts a board %s feet long into shelves that are each %s feet long. How many shelves does %s get?"
         % (nm, show(F(15, 2)), show(F(5, 4)), he), F(15, 2), F(5, 4), count("shelf", "shelves"),
         "Find how many %s-foot shelves are in %s feet" % (show(F(5, 4)), show(F(15, 2))))
    # 12 study time
    nm, he, his = P.next()
    prob("%s has %s hours to study. Each practice quiz takes %s hour. How many quizzes can %s finish?"
         % (nm, show(F(5, 2)), fr(5, 6), he), F(5, 2), F(5, 6), count("quiz", "quizzes"),
         "Find how many %s-hour quizzes fit in %s hours" % (fr(5, 6), show(F(5, 2))))
    # 13 full portions (interpret the leftover)
    q = "A cook has 5 pounds of rice. Each portion uses %s pound. How many <b>full</b> portions can the cook make?" % fr(2, 3)
    e = ("5 ÷ %s = 5 × %s = %s = %s portions. Only whole portions count, so the cook can make <b>7</b> full portions "
         "(with %s pound left over)." % (fr(2, 3), fr(3, 2), fr(15, 2), show(F(15, 2)), fr(1, 3)))
    its.append(mcq(q, ("7", F(7)), [(show(F(15, 2)), F(15, 2)), ("8", F(8)), (show(F(10, 3)), F(10, 3))], e))
    # 14 laps
    nm, he, his = P.next()
    prob("A track is %s mile around. %s runs %s miles. How many laps does %s run?"
         % (fr(1, 2), nm, show(F(9, 4)), he), F(9, 4), F(1, 2), count("lap", "laps"),
         "Find how many %s-mile laps are in %s miles" % (fr(1, 2), show(F(9, 4))))
    # 15 lasagna sharing
    def ofpan(v):
        return "%s of the pan" % show(v)
    prob("%s of a pan of lasagna is left. 4 people share it equally. What fraction of the whole pan does each person get?"
         % fr(3, 5), F(3, 5), F(4), ofpan, "Split %s into 4 equal parts" % fr(3, 5))
    # 16 miles per gallon
    mpg = amount("mile per gallon", "miles per gallon")
    prob("A scooter uses %s gallon of gas to go 16 miles. How many miles can it go on 1 gallon?" % fr(2, 3),
         F(16), F(2, 3), mpg, "Divide the miles by the gallons")
    # 17 poster side
    prob("A poster has an area of %s square meter. It is %s meter wide. How long is it?" % (fr(5, 6), fr(2, 3)),
         F(5, 6), F(2, 3), m_, "Length = area ÷ width")
    # 18 which expression
    nm, he, his = P.next()
    q = "%s has 4 cups of soup. Each bowl holds %s cup. Which expression shows how many bowls %s can fill?" % (nm, fr(2, 3), he)
    e = "The question asks how many %s-cup bowls fit in 4 cups, so divide 4 by %s: 4 ÷ %s = 4 × %s = 6 bowls. Check: 6 × %s = 4." % (
        fr(2, 3), fr(2, 3), fr(2, 3), fr(3, 2), fr(2, 3))
    its.append(mcq(q, "4 ÷ %s" % fr(2, 3), ["%s ÷ 4" % fr(2, 3), "4 × %s" % fr(2, 3), "%s ÷ 4" % fr(3, 2)], e))
    # 19 which question
    q = "Which question can you answer with %s ÷ %s?" % (fr(3, 4), fr(1, 8))
    right = "How many %s-cup scoops are in %s cup?" % (fr(1, 8), fr(3, 4))
    wr = ["What is %s of %s cup?" % (fr(1, 8), fr(3, 4)),
          "How many %s-cup scoops are in %s cup?" % (fr(3, 4), fr(1, 8)),
          "How much is %s cup plus %s cup?" % (fr(3, 4), fr(1, 8))]
    e = ("%s ÷ %s asks how many eighths are in %s: %s = %s, so 6 scoops. “%s of %s” is multiplication, and the reversed "
         "question is %s ÷ %s." % (fr(3, 4), fr(1, 8), fr(3, 4), fr(3, 4), fr(6, 8), fr(1, 8), fr(3, 4), fr(1, 8), fr(3, 4)))
    its.append(mcq(q, right, wr, e))
    # 20 compare
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    q = ("%s pours 2 cups of milk into %s-cup glasses. %s pours %s cups of milk into %s-cup glasses. Who fills more glasses?"
         % (n1, fr(1, 3), n2, show(F(5, 2)), fr(1, 2)))
    e = ("%s: 2 ÷ %s = 6 glasses. %s: %s ÷ %s = %s × 2 = 5 glasses. 6 is more than 5, so <b>%s</b> fills more glasses. "
         "%s has less milk, but %s-cup glasses are smaller." % (n1, fr(1, 3), n2, show(F(5, 2)), fr(1, 2), fr(5, 2), n1, cap(h1), fr(1, 3)))
    its.append(mcq(q, n1, [n2, "They fill the same number.", "You can’t tell."], e))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    a, b = F(3, 4), F(1, 8)
    bar1 = ("<figure class='sn-fig'>" + groups_svg(a, b, PW=30) +
            "<figcaption>" + fr(3, 4) + " = " + fr(6, 8) + ". Each group is " + fr(1, 8) + ", and 6 groups fit, so "
            + dv(a, b) + " = 6.</figcaption></figure>")
    a2, b2 = F(2, 3), F(3, 4)
    bar2 = ("<figure class='sn-fig'>" + groups_svg(a2, b2, PW=30) +
            "<figcaption>In twelfths, " + fr(2, 3) + " = " + fr(8, 12) + " and " + fr(3, 4) + " = " + fr(9, 12)
            + ". A full group (dashed) needs 9 pieces, but there are only 8. So " + dv(a2, b2) + " = " + fr(8, 9)
            + " of a group.</figcaption></figure>")
    return (
        "<h2>The big idea: how many groups?</h2>"
        "<p>" + dv(a, b) + " asks: <b>how many groups of " + fr(1, 8) + " fit in " + fr(3, 4) + "?</b> "
        "Write both fractions with the same denominator and count.</p>"
        + bar1 +
        "<p>Sometimes only part of a group fits. Then the answer is a fraction or a mixed number.</p>"
        + bar2 +
        "<h2>The rule: multiply by the reciprocal</h2>"
        "<p>The <b>reciprocal</b> of a fraction is the fraction flipped: the reciprocal of " + fr(3, 4) + " is " + fr(4, 3)
        + ". A number times its reciprocal is 1.</p>"
        "<p>To divide, <b>keep</b> the first fraction, <b>change</b> ÷ to ×, and <b>flip</b> the second fraction. "
        "In general, " + fr(1, 1).replace(">1<", ">a<", 1).replace(">1<", ">b<", 1) + " ÷ "
        + fr(1, 1).replace(">1<", ">c<", 1).replace(">1<", ">d<", 1) + " = "
        + fr(1, 1).replace(">1<", ">ad<", 1).replace(">1<", ">bc<", 1) + ".</p>"
        + ex("Example 1", dv(a2, b2) + " = <b>?</b>",
             "Keep " + fr(2, 3) + ", change ÷ to ×, flip " + fr(3, 4) + ": " + fr(2, 3) + " × " + fr(4, 3) + " = " + fr(8, 9)
             + ". Check: " + fr(3, 4) + " × " + fr(8, 9) + " = " + fr(24, 36) + " = " + fr(2, 3) + ".", fr(8, 9))
        + ex("Example 2", dv(F(5, 2), F(3, 4)) + " = <b>?</b>",
             "Write " + show(F(5, 2)) + " as " + fr(5, 2) + ". Then " + fr(5, 2) + " × " + fr(4, 3) + " = " + fr(20, 6)
             + " = " + show(F(10, 3)) + ".", show(F(10, 3)))
        + ex("Example 3", "3 people share " + fr(1, 2) + " pound of chocolate equally. How much does each person get?",
             fr(1, 2) + " ÷ 3 = " + fr(1, 2) + " × " + fr(1, 3) + " = " + fr(1, 6) + ". Check: " + fr(1, 6) + " × 3 = " + fr(3, 6)
             + " = " + fr(1, 2) + ".", fr(1, 6) + " pound")
        + "<h2>Check with multiplication</h2>"
        "<p>Multiply the answer by the divisor. You should get the number you started with.</p>"
        + table(["Division", "Check"], [
            [dv(a2, b2) + " = " + fr(8, 9), fr(3, 4) + " × " + fr(8, 9) + " = " + fr(2, 3)],
            ["4 ÷ " + fr(2, 3) + " = 6", fr(2, 3) + " × 6 = 4"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(5, 6) + " ÷ " + fr(2, 3) + " = " + fr(6, 5) + " × " + fr(2, 3) + " (flipped the first fraction)",
             "Flip only the divisor: " + fr(5, 6) + " × " + fr(3, 2) + " = " + show(F(5, 4))],
            [fr(5, 6) + " ÷ " + fr(2, 3) + " = " + fr(10, 18) + " (multiplied without flipping)",
             "Flip the second fraction before you multiply."],
            [show(F(5, 2)) + " ÷ " + fr(3, 4) + " = 2 " + fr(2, 3) + " (divided only the fraction part)",
             "Change mixed numbers to fractions first: " + fr(5, 2) + " × " + fr(4, 3) + " = " + show(F(10, 3))],
            ["1 ÷ " + fr(2, 3) + " = 1 " + fr(1, 3) + " (leftover written as part of a whole)",
             "The leftover " + fr(1, 3) + " is half of a " + fr(2, 3) + " group, so the answer is " + show(F(3, 2))],
        ])
    )


FAQ = [
    {"q": "How do you divide a fraction by a fraction?",
     "a": "Keep the first fraction, change ÷ to ×, and flip the second fraction, then multiply. For example, 2/3 ÷ 3/4 = 2/3 × 4/3 = 8/9."},
    {"q": "Why do you flip the second fraction when dividing?",
     "a": "Dividing by a number is the same as multiplying by its reciprocal. You can check it: 3/4 × 8/9 = 2/3, so 2/3 ÷ 3/4 really is 8/9."},
    {"q": "How do you divide mixed numbers?",
     "a": "Change each mixed number to a fraction first, then multiply by the reciprocal of the divisor. 2 1/2 ÷ 3/4 = 5/2 × 4/3 = 10/3 = 3 1/3."},
    {"q": "What grade learns dividing fractions by fractions?",
     "a": "Grade 6, in Common Core standard 6.NS.A.1. In Grade 5, students divide only unit fractions by whole numbers and whole numbers by unit fractions."},
]


def gen():
    rnd = random.Random(605)
    P = People(rnd)
    sets = [set_groups(), set_rule(), set_compute(), set_mixed(), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "divide-fractions-by-fractions", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Divide Fractions by Fractions",
        "seo_title": "Grade 6 Dividing Fractions by Fractions Worksheets: Reciprocals, Keep-Change-Flip, Mixed Numbers and Word Problems",
        "short_title": "Divide fractions",
        "domain": "The Number System",
        "standard_code": "6.NS.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/A/1/",
        "standard_text": "Interpret and compute quotients of fractions, and solve word problems involving division of fractions by fractions, e.g., by using visual fraction models and equations to represent the problem. For example, create a story context for (2/3) ÷ (3/4) and use a visual fraction model to show the quotient; use the relationship between multiplication and division to explain that (2/3) ÷ (3/4) = 8/9 because 3/4 of 8/9 is 2/3. (In general, (a/b) ÷ (c/d) = ad/bc.) How much chocolate will each person get if 3 people share 1/2 lb of chocolate equally? How many 3/4-cup servings are in 2/3 of a cup of yogurt? How wide is a rectangular strip of land with length 3/4 mi and area 1/2 square mi?",
        "meta_desc": "Free Grade 6 worksheets on dividing fractions by fractions: use fraction bars to find how many groups fit, multiply by the reciprocal, divide mixed numbers and whole numbers, check with multiplication, and solve serving, sharing and area word problems. 100 practice questions with answers.",
        "key_big": "To divide by a fraction, multiply by its reciprocal: 2/3 ÷ 3/4 = 2/3 × 4/3 = 8/9.",
        "key_sub": "Keep the first fraction, change ÷ to ×, flip the second. Change mixed numbers to fractions first. Check: 3/4 × 8/9 = 2/3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "fraction bar")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
