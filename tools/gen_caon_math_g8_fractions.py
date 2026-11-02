# -*- coding: utf-8 -*-
"""
CA Grade 8 Math: Operations with Fractions (Ontario Mathematics Curriculum 2020, B2.5 and B2.6)
  python3 tools/gen_caon_math_g8_fractions.py
Grade 8 uses all four operations with fractions and mixed numbers:
  add and subtract with unlike denominators and mixed numbers, multiply fractions and mixed numbers,
  divide by multiplying by the reciprocal, mixed operations with BEDMAS, word problems.
Answers are in simplest form (mixed numbers when greater than 1).
Every answer is checked with fractions.Fraction; no two choices are equal in value.
Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
G1 = "#4fae74"
G2 = "#a6dbb7"
BLUE = "#7fb2e0"
LIGHT = "#d7ecdf"
DARKLINE = "#1f6b3e"
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def num(n):
    s = str(n)
    if len(s) <= 4:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NBSP.join(out)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return num(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (num(q), fr(r, v.denominator))


def imp(v):
    """A Fraction as an improper fraction (or a whole number)."""
    v = F(v)
    return num(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def frv(v):
    v = F(v)
    return fr(v.numerator, v.denominator)


class N:
    """An operand exactly as it is written: whole number, proper fraction or mixed number."""
    def __init__(self, w, n=0, d=1):
        self.w, self.n, self.d = w, n, d
        self.v = w + F(n, d)
        if n == 0:
            self.h = num(w)
        elif w == 0:
            self.h = fr(n, d)
        else:
            self.h = "%d %s" % (w, fr(n, d))
        self.f = F(n, d)

    @property
    def mixed(self):
        return self.w > 0 and self.n > 0


def P(n, d):
    return N(0, n, d)


def M(w, n, d):
    return N(w, n, d)


def W(w):
    return N(w)


def R(n, d, unit=""):
    """A fraction exactly as a student wrote it (not simplified), with its value."""
    return (fr(n, d) + (" " + unit if unit else ""), F(n, d))


def S(v, unit="", pre=""):
    v = F(v)
    return (pre + show(v) + (" " + unit if unit else ""), v)


def lcm(a, b):
    return a * b // math.gcd(a, b)


def cap(s):
    return s[0].upper() + s[1:]


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). A candidate equal in value to an earlier choice
    (or not positive) is skipped. Positions are set later by balance()."""
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
            continue
        ch.append(h)
        vals.append(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e}


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
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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
    return u


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def bar_row(x0, y0, Wd, H, d, k, col, start=0, col2=None, k2=0):
    s = []
    pw = Wd / float(d)
    for i in range(d):
        c = "#fff"
        if start <= i < start + k:
            c = col
        elif col2 and start + k <= i < start + k + k2:
            c = col2
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + i * pw, y0, pw, H, c, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x0, y0, Wd, H, LINE))
    return "".join(s)


def sum_bars_svg(d1, d2, Wd=288):
    """Bar in d1 parts with 1 shaded, bar in d2 parts with 1 shaded, and a bar in L parts showing both."""
    L = lcm(d1, d2)
    k1, k2 = L // d1, L // d2
    x0, H, gap = 58, 32, 12
    s = []
    rows = [("1/%d" % d1, bar_row(x0, 4, Wd, H, d1, 1, G1)),
            ("1/%d" % d2, bar_row(x0, 4 + H + gap, Wd, H, d2, 1, BLUE)),
            ("?", bar_row(x0, 4 + 2 * (H + gap), Wd, H, L, k1, G1, 0, BLUE, k2))]
    for i, (lab, b) in enumerate(rows):
        s.append(b)
        s.append(text(x0 - 10, 4 + i * (H + gap) + H / 2 + 6, lab, 16, anchor="end"))
    return svg_wrap(x0 + Wd + 4, 4 + 3 * H + 2 * gap + 4, "".join(s),
                    "three bars: one cut into %d parts with 1 shaded, one cut into %d parts with 1 shaded, "
                    "and one cut into %d parts with %d and %d shaded" % (d1, d2, L, k1, k2))


def area_svg(a1, b1, a2, b2, S=150):
    """Area model for a2/b2 × a1/b1 in a 1-by-1 square: a1 of b1 columns light, a2 of b2 rows of them dark."""
    p = 4
    cw, rh = S / float(b1), S / float(b2)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (p, p, S, S),
         "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (p, p, a1 * cw, S, LIGHT),
         "<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s'/>" % (p, p, a1 * cw, a2 * rh, G1)]
    for i in range(1, b1):
        x = p + i * cw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x, p, x, p + S, LINE))
    for j in range(1, b2):
        y = p + j * rh
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (p, y, p + S, y, LINE))
    s.append("<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='none' stroke='%s' stroke-width='3.5'/>"
             % (p, p, a1 * cw, a2 * rh, DARKLINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (p, p, S, S, LINE))
    return svg_wrap(S + 2 * p, S + 2 * p, "".join(s),
                    "area model: a square cut into %d columns and %d rows, %d columns light, %d by %d dark"
                    % (b1, b2, a1, a1, a2))


def groups_svg(n, d, k, a, PW=16):
    """n wholes, each cut into d pieces; the first k pieces are shaded in alternating groups of a,
    with a bracket over every group. Labels 0..n under the whole lines."""
    tot = n * d
    X0, T, BH = 14, 30, 34
    s = []
    for i in range(tot):
        col = "#fff" if i >= k else (G1 if (i // a) % 2 == 0 else G2)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                 % (X0 + i * PW, T, PW, BH, col, LINE))
    for j in range(n + 1):
        x = X0 + j * d * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append(text(x, T + BH + 26, str(j), 16))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, tot * PW, BH, LINE))
    for g in range(k // a):
        x0 = X0 + g * a * PW + 2
        x1 = X0 + (g + 1) * a * PW - 2
        s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, T - 4, T - 12, x1, T - 4, LINE))
        s.append(text((x0 + x1) / 2.0, T - 15, str(g + 1), 14))
    return svg_wrap(X0 * 2 + tot * PW, T + BH + 32, "".join(s),
                    "%d wholes, each cut into %d pieces, %d pieces shaded in groups of %d" % (n, d, k, a))


# ------------------------------------------------------------ explanations
def simp(n, d):
    """n/d, then = simplest form if that is different."""
    v = F(n, d)
    s = fr(n, d)
    if v.denominator != d or v.numerator != n:
        s += " = " + (frv(v) if v.denominator != 1 else str(v.numerator))
        if v.denominator != 1 and v > 1:
            s += " = " + show(v)
    elif v > 1:
        s += " = " + show(v)
    return s


def to_imp(x):
    """'2 1/3 = 7/3' for a mixed number; '4 = 4/1' for a whole number; nothing for a fraction."""
    if x.mixed:
        return "%s = %s" % (x.h, fr(x.v.numerator, x.v.denominator))
    return ""


def imp_h(x):
    if x.n == 0:
        return fr(x.w, 1)
    return fr(x.v.numerator, x.v.denominator)


def addsub_e(x, y, op, unit=""):
    u = " " + unit if unit else ""
    v = x.v + y.v if op == "+" else x.v - y.v
    L = lcm(x.d, y.d)
    if not x.mixed and not y.mixed and x.w == 0 and y.w == 0:
        a, b = x.n * L // x.d, y.n * L // y.d
        s = "Use the common denominator %d: " % L
        s += "%s = %s and %s = %s. " % (x.h, fr(a, L), y.h, fr(b, L)) if x.d != L and y.d != L else ""
        if x.d == L or y.d == L:
            if x.d != L:
                s += "%s = %s. " % (x.h, fr(a, L))
            if y.d != L:
                s += "%s = %s. " % (y.h, fr(b, L))
        r = a + b if op == "+" else a - b
        s += "%s %s %s = %s." % (fr(a, L), op, fr(b, L), simp(r, L))
        return s + " The answer is <b>%s%s</b>." % (show(v), u)
    if op == "+":
        a, b = x.n * L // x.d, y.n * L // y.d
        s = "Add the whole numbers: %d + %d = %d. " % (x.w, y.w, x.w + y.w)
        s += "Add the fractions with denominator %d: %s + %s = %s. " % (L, fr(a, L), fr(b, L), simp(a + b, L))
        if F(a + b, L) >= 1:
            s += "%d + %s = " % (x.w + y.w, show(F(a + b, L)))
        else:
            s += "So the sum is "
        return s + "<b>%s%s</b>." % (show(v), u)
    # subtraction with mixed numbers: change to improper fractions with the common denominator
    A, B = x.v * L, y.v * L
    s = "Change to improper fractions with denominator %d: %s = %s and %s = %s. " % (
        L, x.h, fr(int(A), L), y.h, fr(int(B), L))
    s += "%s − %s = %s." % (fr(int(A), L), fr(int(B), L), simp(int(A - B), L))
    return s + " The answer is <b>%s%s</b>." % (show(v), u)


def mul_e(x, y, unit="", lead=""):
    u = " " + unit if unit else ""
    v = x.v * y.v
    s = lead
    conv = [c for c in (to_imp(x), to_imp(y)) if c]
    if conv:
        s += "Change mixed numbers to improper fractions first: %s. " % ", ".join(conv)
    a, b = imp_h(x), imp_h(y)
    xn, xd = (x.v.numerator, x.v.denominator)
    yn, yd = (y.v.numerator, y.v.denominator)
    s += "%s × %s = %s = %s." % (a, b, fr("%d × %d" % (xn, yn), "%d × %d" % (xd, yd)), simp(xn * yn, xd * yd))
    return s + " The answer is <b>%s%s</b>." % (show(v), u)


def div_e(x, y, unit="", lead="", tail=""):
    u = " " + unit if unit else ""
    v = x.v / y.v
    s = lead
    conv = [c for c in (to_imp(x), to_imp(y)) if c]
    if conv:
        s += "Change mixed numbers to improper fractions first: %s. " % ", ".join(conv)
    yn, yd = y.v.numerator, y.v.denominator
    xn, xd = x.v.numerator, x.v.denominator
    s += "Multiply by the reciprocal of %s: %s × %s = %s." % (
        imp_h(y) if y.w == 0 or y.mixed else y.h, imp_h(x), fr(yd, yn), simp(xn * yd, xd * yn))
    s += " The answer is <b>%s%s</b>." % (show(v), u)
    return s + tail


# ------------------------------------------------------------ real mistakes
def as_wrongs(x, y, op, order, unit=""):
    out = []
    sg = 1 if op == "+" else -1
    L = lcm(x.d, y.d)
    both_proper = x.w == 0 and y.w == 0
    for k in order:
        v = None
        if k == "dens":                      # added (subtracted) the numerators and the denominators
            dd = x.d + y.d if op == "+" else x.d - y.d
            nn = x.n + sg * y.n
            if dd > 0 and nn > 0 and nn != dd:
                if both_proper:
                    out.append(R(nn, dd, unit)); continue
                v = x.w + sg * y.w + F(nn, dd)
        elif k == "numer":                   # common denominator, numerators not renamed
            nn = x.n + sg * y.n
            if nn > 0:
                if both_proper:
                    out.append(R(nn, L, unit)); continue
                v = x.w + sg * y.w + F(nn, L)
        elif k == "muld":                    # multiplied the denominators, added the numerators
            nn = x.n + sg * y.n
            if nn > 0:
                if both_proper:
                    out.append(R(nn, x.d * y.d, unit)); continue
                v = x.w + sg * y.w + F(nn, x.d * y.d)
        elif k == "one":                     # renamed only the first fraction
            nn = x.n * L // x.d + sg * y.n
            if nn > 0 and y.d != L:
                if both_proper:
                    out.append(R(nn, L, unit)); continue
                v = x.w + sg * y.w + F(nn, L)
        elif k == "op":                      # used the other operation
            v = x.v - y.v if op == "+" else x.v + y.v
        elif k == "nocarry":                 # forgot to carry the whole from the fraction part
            v = x.v + y.v - 1
        elif k == "flip":                    # subtracted the smaller fraction from the larger
            v = (x.w - y.w) + abs(x.f - y.f)
        elif k == "noborrow":                # regrouped the fraction but did not take 1 from the whole number
            v = x.v - y.v + 1
        elif k == "mult":
            v = x.v * y.v
        else:
            raise ValueError(k)
        if v is not None:
            out.append(S(v, unit))
    return out


def mul_wrongs(x, y, order, unit=""):
    out = []
    for k in order:
        if k == "sep":                       # multiplied whole parts and fraction parts separately
            v = x.w * y.w + x.f * y.f
        elif k == "whole":                   # multiplied only the whole part of the mixed number
            v = x.v * y.w + y.f if y.mixed else x.w * y.v + x.f
        elif k == "add":
            v = x.v + y.v
        elif k == "div":                     # cross-multiplied (that is division)
            v = x.v / y.v
        elif k == "keep":                    # common denominator, then multiplied the numerators only
            L = lcm(x.v.denominator, y.v.denominator)
            v = F((x.v * L) * (y.v * L), L)
        elif k == "addd":                    # multiplied numerators, added denominators
            out.append(R(x.v.numerator * y.v.numerator, x.v.denominator + y.v.denominator, unit)); continue
        else:
            raise ValueError(k)
        out.append(S(v, unit))
    return out


def div_wrongs(x, y, order, unit=""):
    out = []
    for k in order:
        if k == "noflip":                    # multiplied without flipping
            v = x.v * y.v
        elif k == "first":                   # flipped the first number instead
            v = y.v / x.v
        elif k == "both":                    # flipped both numbers
            v = 1 / (x.v * y.v)
        elif k == "sep":                     # divided whole parts and fraction parts separately
            if not (x.mixed and y.mixed):
                continue
            v = F(x.w, y.w) + x.f / y.f
        elif k == "fracflip":                # flipped only the fraction part of the mixed divisor
            if not y.mixed:
                continue
            v = x.v * 1 / (y.w + F(y.d, y.n))
        else:
            raise ValueError(k)
        out.append(S(v, unit))
    return out


SIMPLE = "<br>Give your answer in simplest form."


# ============================================================ set 1: add and subtract
def set_addsub():
    its = []

    def calc(x, y, op, order, extra=None, prompt=SIMPLE):
        v = x.v + y.v if op == "+" else x.v - y.v
        q = "%s %s %s = <b>?</b>%s" % (x.h, op if op == "+" else "−", y.h, prompt)
        e = addsub_e(x, y, op)
        its.append(mcq(q, S(v), as_wrongs(x, y, op, order + ["one", "muld", "op"]) + (extra or []), e))

    # picture
    q = (fig(sum_bars_svg(3, 4)) + "The bottom bar shows %s + %s in twelfths. What is %s + %s?"
         % (fr(1, 3), fr(1, 4), fr(1, 3), fr(1, 4)))
    its.append(mcq(q, R(7, 12), [R(2, 7), R(2, 12), R(1, 12), R(7, 24)],
                   "%s = %s (4 twelfths) and %s = %s (3 twelfths). Together: %s + %s = <b>%s</b>."
                   % (fr(1, 3), fr(4, 12), fr(1, 4), fr(3, 12), fr(4, 12), fr(3, 12), fr(7, 12))))
    # proper, unlike: add
    calc(P(3, 4), P(1, 6), "+", ["dens", "numer", "muld", "op"])
    calc(P(2, 5), P(1, 3), "+", ["dens", "muld", "op", "numer"])
    calc(P(5, 6), P(3, 8), "+", ["numer", "dens", "muld", "op"])
    calc(P(7, 10), P(1, 4), "+", ["dens", "numer", "op", "muld"])
    calc(P(2, 3), P(4, 9), "+", ["numer", "dens", "op", "muld"])
    # proper, unlike: subtract
    calc(P(5, 6), P(1, 4), "−", ["dens", "numer", "op", "muld"])
    calc(P(3, 4), P(2, 5), "−", ["numer", "dens", "muld", "op"])
    calc(P(7, 8), P(1, 6), "−", ["dens", "muld", "numer", "op"])
    calc(P(9, 10), P(3, 4), "−", ["numer", "one", "muld", "op"])
    # mixed: add
    calc(M(2, 1, 3), M(1, 1, 4), "+", ["dens", "numer", "op", "muld"])
    calc(M(3, 5, 6), M(2, 3, 4), "+", ["nocarry", "dens", "numer", "op"])
    calc(M(1, 2, 5), M(4, 1, 2), "+", ["dens", "numer", "muld", "op"])
    calc(M(5, 3, 8), M(2, 5, 6), "+", ["nocarry", "numer", "dens", "op"])
    # mixed: subtract
    calc(M(4, 3, 4), M(1, 1, 3), "−", ["dens", "numer", "op", "muld"])
    calc(M(5, 1, 4), M(2, 2, 3), "−", ["flip", "noborrow", "op", "numer"])
    calc(M(6, 1, 6), M(3, 3, 4), "−", ["noborrow", "flip", "op", "numer"])
    # whole number minus a mixed number
    x, y = W(3), M(1, 2, 5)
    its.append(mcq("3 − %s = <b>?</b>" % y.h, S(x.v - y.v),
                   [S(2 + F(2, 5)), S(F(8, 5) + 1), S(x.v + y.v), S(2 + F(3, 5))],
                   "Write 3 as 2 %s. Then 2 %s − 1 %s = <b>1 %s</b>."
                   % (fr(5, 5), fr(5, 5), fr(2, 5), fr(3, 5))))
    # missing number
    q = "%s − <b>?</b> = %s" % (fr(3, 4), fr(1, 6))
    its.append(mcq(q, R(7, 12), [S(F(11, 12)), R(2, 10), R(1, 12)],
                   "The missing number is %s − %s. With denominator 12: %s − %s = <b>%s</b>. "
                   "Check: %s − %s = %s − %s = %s = %s."
                   % (fr(3, 4), fr(1, 6), fr(9, 12), fr(2, 12), fr(7, 12),
                      fr(3, 4), fr(7, 12), fr(9, 12), fr(7, 12), fr(2, 12), fr(1, 6))))
    # error analysis
    its.append(mcq("A student writes %s + %s = %s. What is the mistake?" % (fr(2, 3), fr(1, 5), fr(3, 8)),
                   ("The student added the denominators.", None),
                   [("The student did not simplify.", None), ("The student subtracted the numerators.", None),
                    ("There is no mistake.", None)],
                   "Only the numerators are added, and only after the denominators are the same: "
                   "%s + %s = <b>%s</b>, not %s." % (fr(10, 15), fr(3, 15), fr(13, 15), fr(3, 8))))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract with unlike denominators and mixed numbers", "items": its}


# ============================================================ set 2: multiply
def set_multiply(Pp):
    its = []

    def calc(x, y, order, prompt=SIMPLE, extra=None):
        q = "%s × %s = <b>?</b>%s" % (x.h, y.h, prompt)
        its.append(mcq(q, S(x.v * y.v), mul_wrongs(x, y, order) + (extra or []), mul_e(x, y)))

    # area models
    for a1, b1, a2, b2, order in [(3, 4, 2, 3, ["add", "addd", "div", "keep"]),
                                  (1, 2, 3, 5, ["add", "addd", "div", "keep"])]:
        x, y = P(a2, b2), P(a1, b1)
        q = (fig(area_svg(a1, b1, a2, b2)) + "The light part is %s of the square. The dark part is %s of the light part. "
             "What is %s × %s?" % (fr(a1, b1), fr(a2, b2), x.h, y.h))
        e = ("The square is cut into %d × %d = %d small rectangles, and %d × %d = %d of them are dark. "
             % (b1, b2, b1 * b2, a1, a2, a1 * a2)) + mul_e(x, y)
        its.append(mcq(q, S(x.v * y.v), mul_wrongs(x, y, order), e))
    # proper × proper (simplify)
    calc(P(4, 9), P(3, 8), ["add", "addd", "div"])
    calc(P(5, 6), P(3, 10), ["addd", "add", "div"])
    calc(P(7, 12), P(4, 7), ["add", "addd", "div"])
    calc(P(2, 5), P(5, 8), ["add", "addd", "div"])
    calc(P(5, 8), P(4, 15), ["addd", "add", "div"])
    # whole number and fraction / mixed number
    calc(W(6), M(1, 3, 4), ["whole", "add", "div", "addd"])
    calc(P(3, 4), M(2, 2, 3), ["whole", "add", "div", "keep"])
    calc(M(3, 1, 3), P(3, 5), ["whole", "add", "div", "keep"])
    calc(P(5, 6), W(9), ["addd", "add", "div", "keep"], extra=[R(45, 54)])
    calc(M(2, 3, 4), W(4), ["whole", "add", "div", "addd"])
    # mixed × mixed
    calc(M(1, 1, 2), M(2, 1, 3), ["sep", "add", "div", "keep"])
    calc(M(2, 1, 4), M(1, 1, 3), ["sep", "add", "div", "keep"])
    calc(M(3, 1, 3), M(1, 1, 5), ["sep", "add", "div", "keep"])
    calc(M(2, 2, 5), M(1, 7, 8), ["sep", "add", "div", "keep"])
    calc(M(1, 3, 4), M(2, 2, 7), ["sep", "add", "div", "keep"])
    # error analysis
    nm, he, his, him = Pp.next()
    q = "%s says 2 %s × 2 %s = 4 %s. What did %s do wrong?" % (nm, fr(1, 2), fr(1, 2), fr(1, 4), he)
    its.append(mcq(q, ("%s multiplied the whole numbers and the fractions separately." % cap(he), None),
                   [("%s added instead of multiplying." % cap(he), None),
                    ("%s did not simplify the answer." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "2 × 2 + %s × %s = 4 %s leaves out parts of the product. Change to improper fractions: "
                   "%s × %s = %s = <b>6 %s</b>." % (fr(1, 2), fr(1, 2), fr(1, 4), fr(5, 2), fr(5, 2), fr(25, 4), fr(1, 4))))
    # estimate
    q = "Which is the best estimate of 3 %s × 2 %s?" % (fr(7, 8), fr(1, 9))
    its.append(mcq(q, ("8", None), [("6", None), ("5", None), ("12", None)],
                   "3 %s is close to 4 and 2 %s is close to 2. 4 × 2 = <b>8</b>. "
                   "(The exact product is %s.)" % (fr(7, 8), fr(1, 9), show(F(31, 8) * F(19, 9)))))
    # reasoning
    q = "Without calculating, which product is <b>less</b> than %s?" % fr(5, 6)
    its.append(mcq(q, ("%s × %s" % (fr(5, 6), fr(2, 3)), None),
                   [("%s × 1 %s" % (fr(5, 6), fr(1, 3)), None), ("%s × %s" % (fr(5, 6), fr(3, 2)), None),
                    ("%s × 2" % fr(5, 6), None)],
                   "Multiplying by a number less than 1 makes the product smaller. Only %s is less than 1, so "
                   "<b>%s × %s</b> = %s is less than %s." % (fr(2, 3), fr(5, 6), fr(2, 3), fr(5, 9), fr(5, 6))))
    assert len(its) == 20, len(its)
    return {"title": "Multiply fractions and mixed numbers", "items": its}


# ============================================================ set 3: divide
def set_divide(Pp):
    its = []

    def calc(x, y, order, prompt=SIMPLE, extra=None):
        q = "%s ÷ %s = <b>?</b>%s" % (x.h, y.h, prompt)
        e = div_e(x, y, tail=" Check: %s × %s = %s." % (show(x.v / y.v), y.h, show(x.v)))
        its.append(mcq(q, S(x.v / y.v), div_wrongs(x, y, order) + (extra or []), e))

    # reciprocals
    its.append(mcq("What is the reciprocal of %s?" % fr(5, 8), R(8, 5),
                   [("−%s" % fr(5, 8), None), R(3, 8), R(5, 8)],
                   "The reciprocal swaps the numerator and the denominator: <b>%s</b>. Check: %s × %s = 1."
                   % (fr(8, 5), fr(5, 8), fr(8, 5))))
    its.append(mcq("What is the reciprocal of 1 %s?" % fr(3, 4), R(4, 7),
                   [("1 %s" % fr(4, 3), F(7, 3)), R(7, 4), R(4, 3)],
                   "Change to an improper fraction first: 1 %s = %s. Its reciprocal is <b>%s</b>. Check: %s × %s = 1."
                   % (fr(3, 4), fr(7, 4), fr(4, 7), fr(7, 4), fr(4, 7))))
    # picture
    q = (fig(groups_svg(3, 8, 18, 3)) + "The shaded part is 2 %s. Each bracket is %s. How many groups of %s are in 2 %s?"
         % (fr(1, 4), fr(3, 8), fr(3, 8), fr(1, 4)))
    x, y = M(2, 1, 4), P(3, 8)
    its.append(mcq(q, S(x.v / y.v), div_wrongs(x, y, ["noflip", "first", "both"]) + [S(F(18))],
                   "2 %s = %s, so 18 eighths are shaded. 18 ÷ 3 = 6 groups. " % (fr(1, 4), fr(18, 8))
                   + div_e(x, y)))
    # proper ÷ proper
    calc(P(3, 4), P(3, 8), ["noflip", "first", "both"], extra=[R(9, 32)])
    calc(P(2, 3), P(4, 9), ["noflip", "first", "both"])
    calc(P(5, 6), P(2, 3), ["noflip", "first", "both"])
    calc(P(3, 5), P(9, 10), ["noflip", "first", "both"])
    calc(P(7, 8), P(1, 4), ["noflip", "first", "both"])
    calc(P(8, 9), P(2, 3), ["noflip", "first", "both"])
    # with whole and mixed numbers
    calc(W(4), P(2, 3), ["noflip", "first", "both"])
    calc(M(2, 1, 2), W(5), ["noflip", "first", "both"], extra=[S(2 + F(1, 10))])
    calc(M(3, 3, 4), M(1, 1, 4), ["sep", "noflip", "fracflip", "first"])
    calc(M(3, 1, 3), M(1, 1, 4), ["sep", "noflip", "fracflip", "first"])
    calc(M(1, 7, 8), P(3, 4), ["noflip", "first", "both"])
    calc(W(6), M(1, 1, 2), ["fracflip", "noflip", "first", "both"])
    calc(M(2, 1, 4), M(2, 1, 2), ["sep", "noflip", "fracflip", "first"])
    # which is the same
    q = "Which is the same as %s ÷ %s?" % (fr(2, 5), fr(3, 4))
    its.append(mcq(q, ("%s × %s" % (fr(2, 5), fr(4, 3)), None),
                   [("%s × %s" % (fr(5, 2), fr(3, 4)), None), ("%s × %s" % (fr(2, 5), fr(3, 4)), None),
                    ("%s × %s" % (fr(5, 2), fr(4, 3)), None)],
                   "Keep the first fraction, change ÷ to ×, and flip the divisor: <b>%s × %s</b> = %s."
                   % (fr(2, 5), fr(4, 3), fr(8, 15))))
    # reasoning
    q = "Without calculating, which is true about %s ÷ %s?" % (fr(5, 6), fr(2, 3))
    its.append(mcq(q, ("It is greater than %s." % fr(5, 6), None),
                   [("It is less than %s." % fr(5, 6), None), ("It is equal to %s." % fr(5, 6), None),
                    ("It is less than %s." % fr(2, 3), None)],
                   "Dividing by a number less than 1 makes the answer larger. %s ÷ %s = %s = 1 %s, "
                   "which is <b>greater than %s</b>." % (fr(5, 6), fr(2, 3), fr(15, 12), fr(1, 4), fr(5, 6))))
    # error analysis
    nm, he, his, him = Pp.next()
    q = "%s says %s ÷ %s = %s. What did %s do wrong?" % (nm, fr(4, 5), fr(2, 3), fr(5, 6), he)
    its.append(mcq(q, ("%s flipped the first fraction instead of the second." % cap(he), None),
                   [("%s multiplied without flipping." % cap(he), None),
                    ("%s flipped both fractions." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "%s × %s = %s = %s, so %s flipped %s. Flip only the divisor: %s × %s = %s = <b>1 %s</b>."
                   % (fr(5, 4), fr(2, 3), fr(10, 12), fr(5, 6), nm, fr(4, 5), fr(4, 5), fr(3, 2), fr(12, 10), fr(1, 5))))
    # missing number
    q = "<b>?</b> ÷ %s = %s" % (fr(1, 2), fr(3, 4))
    its.append(mcq(q, R(3, 8), [S(F(3, 2)), R(1, 4), S(F(5, 4))],
                   "Undo the division by multiplying: %s × %s = <b>%s</b>. Check: %s ÷ %s = %s × 2 = %s = %s."
                   % (fr(3, 4), fr(1, 2), fr(3, 8), fr(3, 8), fr(1, 2), fr(3, 8), fr(6, 8), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Divide by multiplying by the reciprocal", "items": its}


# ============================================================ set 4: mixed operations (BEDMAS)
def set_bedmas(Pp):
    its = []

    def item(expr, correct, wrongs, e, prompt=SIMPLE):
        q = expr if prompt is None else "%s = <b>?</b>%s" % (expr, prompt)
        its.append(mcq(q, S(correct), [S(w) for w in wrongs], e))

    h, q, t, s6, t4 = F(1, 2), F(1, 4), F(2, 3), F(1, 6), F(3, 4)
    # 1
    item("%s + %s × %s" % (fr(1, 2), fr(1, 4), fr(2, 3)), h + q * t,
         [(h + q) * t, F(3, 14), h + q / t],
         "Multiply first: %s × %s = %s = %s. Then %s + %s = %s + %s = <b>%s</b>."
         % (fr(1, 4), fr(2, 3), fr(2, 12), fr(1, 6), fr(1, 2), fr(1, 6), fr(3, 6), fr(1, 6), fr(2, 3)))
    # 2
    item("%s − %s ÷ 2" % (fr(5, 6), fr(1, 3)), F(5, 6) - F(1, 3) / 2,
         [(F(5, 6) - F(1, 3)) / 2, F(5, 6) - F(2, 3), (F(5, 6) - F(1, 3)) * 2],
         "Divide first: %s ÷ 2 = %s × %s = %s. Then %s − %s = %s = <b>%s</b>."
         % (fr(1, 3), fr(1, 3), fr(1, 2), fr(1, 6), fr(5, 6), fr(1, 6), fr(4, 6), fr(2, 3)))
    # 3
    item("(%s + %s) × %s" % (fr(2, 3), fr(1, 6), fr(3, 5)), (t + s6) * F(3, 5),
         [t + s6 * F(3, 5), t * F(3, 5) + s6, (t + s6) / F(3, 5)],
         "Brackets first: %s + %s = %s + %s = %s. Then %s × %s = %s = <b>%s</b>."
         % (fr(2, 3), fr(1, 6), fr(4, 6), fr(1, 6), fr(5, 6), fr(5, 6), fr(3, 5), fr(15, 30), fr(1, 2)))
    # 4
    item("%s ÷ %s × %s" % (fr(3, 4), fr(1, 2), fr(1, 3)), t4 / h * F(1, 3),
         [t4 / (h * F(1, 3)), t4 * h * F(1, 3), h / t4 * F(1, 3)],
         "÷ and × have the same rank, so work from left to right. %s ÷ %s = %s × 2 = %s. "
         "Then %s × %s = %s = <b>%s</b>." % (fr(3, 4), fr(1, 2), fr(3, 4), fr(3, 2), fr(3, 2), fr(1, 3), fr(3, 6), fr(1, 2)))
    # 5 exponent
    item("(%s)² + %s" % (fr(1, 2), fr(3, 4)), h ** 2 + t4,
         [1 + t4, h + t4, (h + t4) ** 2],
         "Exponent first: (%s)² = %s × %s = %s. Then %s + %s = %s = <b>1</b>."
         % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 4), fr(1, 4), fr(3, 4), fr(4, 4)))
    # 6
    item("2 − %s × %s" % (fr(3, 4), fr(2, 3)), 2 - t4 * t,
         [(2 - t4) * t, 2 - t4 / t, 2 + t4 * t],
         "Multiply first: %s × %s = %s = %s. Then 2 − %s = <b>1 %s</b>."
         % (fr(3, 4), fr(2, 3), fr(6, 12), fr(1, 2), fr(1, 2), fr(1, 2)))
    # 7
    item("1 %s × (%s − %s)" % (fr(1, 2), fr(2, 3), fr(1, 4)), F(3, 2) * (t - q),
         [F(3, 2) * t - q, 1 + h * (t - q), F(3, 2) / (t - q)],
         "Brackets first: %s − %s = %s − %s = %s. Then %s × %s = %s = <b>%s</b>."
         % (fr(2, 3), fr(1, 4), fr(8, 12), fr(3, 12), fr(5, 12), fr(3, 2), fr(5, 12), fr(15, 24), fr(5, 8)))
    # 8
    item("%s ÷ (%s + %s)" % (fr(4, 5), fr(2, 5), fr(1, 2)), F(4, 5) / (F(2, 5) + h),
         [F(4, 5) / F(2, 5) + h, F(4, 5) * (F(2, 5) + h), (F(2, 5) + h) / F(4, 5)],
         "Brackets first: %s + %s = %s + %s = %s. Then %s ÷ %s = %s × %s = %s = <b>%s</b>."
         % (fr(2, 5), fr(1, 2), fr(4, 10), fr(5, 10), fr(9, 10), fr(4, 5), fr(9, 10), fr(4, 5), fr(10, 9),
            fr(40, 45), fr(8, 9)))
    # 9
    item("(%s)² ÷ %s" % (fr(3, 4), fr(3, 8)), t4 ** 2 / F(3, 8),
         [t4 * 2 / F(3, 8), t4 ** 2 * F(3, 8), F(9, 4) / F(3, 8)],
         "Exponent first: (%s)² = %s. Then %s ÷ %s = %s × %s = %s = <b>1 %s</b>."
         % (fr(3, 4), fr(9, 16), fr(9, 16), fr(3, 8), fr(9, 16), fr(8, 3), fr(72, 48), fr(1, 2)))
    # 10
    item("%s − %s + %s" % (fr(5, 6), fr(1, 3), fr(1, 4)), F(5, 6) - F(1, 3) + q,
         [F(5, 6) - (F(1, 3) + q), F(5, 6) + F(1, 3) + q, F(2, 6)],
         "+ and − have the same rank, so work from left to right. %s − %s = %s − %s = %s. "
         "Then %s + %s = %s + %s = <b>%s</b>."
         % (fr(5, 6), fr(1, 3), fr(5, 6), fr(2, 6), fr(3, 6), fr(1, 2), fr(1, 4), fr(2, 4), fr(1, 4), fr(3, 4)))
    # 11
    item("3 %s − 1 %s × 2" % (fr(1, 2), fr(1, 4)), F(7, 2) - F(5, 4) * 2,
         [(F(7, 2) - F(5, 4)) * 2, F(7, 2) - (2 + q), F(7, 2) - F(5, 4) / 2],
         "Multiply first: 1 %s × 2 = %s × 2 = %s = 2 %s. Then 3 %s − 2 %s = <b>1</b>."
         % (fr(1, 4), fr(5, 4), fr(10, 4), fr(1, 2), fr(1, 2), fr(1, 2)))
    # 12
    item("%s × %s + %s ÷ %s" % (fr(5, 6), fr(3, 5), fr(1, 2), fr(3, 4)), F(5, 6) * F(3, 5) + h / t4,
         [F(5, 6) * F(3, 5) + h * t4, (F(5, 6) * F(3, 5) + h) / t4, F(5, 6) * F(3, 5) + t4 / h],
         "Multiply and divide first: %s × %s = %s = %s, and %s ÷ %s = %s × %s = %s. "
         "Then %s + %s = %s + %s = %s = <b>1 %s</b>."
         % (fr(5, 6), fr(3, 5), fr(15, 30), fr(1, 2), fr(1, 2), fr(3, 4), fr(1, 2), fr(4, 3), fr(2, 3),
            fr(1, 2), fr(2, 3), fr(3, 6), fr(4, 6), fr(7, 6), fr(1, 6)))
    # 13
    item("(1 − %s) × (1 + %s)" % (fr(2, 5), fr(1, 3)), (1 - F(2, 5)) * (1 + F(1, 3)),
         [1 - F(2, 5) * 1 + F(1, 3), (1 - F(2, 5)) + (1 + F(1, 3)), (1 - F(2, 5)) * F(1, 3)],
         "Brackets first: 1 − %s = %s and 1 + %s = %s. Then %s × %s = %s = <b>%s</b>."
         % (fr(2, 5), fr(3, 5), fr(1, 3), fr(4, 3), fr(3, 5), fr(4, 3), fr(12, 15), fr(4, 5)))
    # 14
    item("%s − (%s − %s)" % (fr(7, 8), fr(1, 2), fr(1, 4)), F(7, 8) - (h - q),
         [F(7, 8) - h - q, F(7, 8) + (h - q), F(7, 8) - h],
         "Brackets first: %s − %s = %s. Then %s − %s = %s − %s = <b>%s</b>."
         % (fr(1, 2), fr(1, 4), fr(1, 4), fr(7, 8), fr(1, 4), fr(7, 8), fr(2, 8), fr(5, 8)))
    # 15
    item("%s ÷ %s − %s" % (fr(2, 3), fr(4, 9), fr(1, 2)), t / F(4, 9) - h,
         [F(4, 9) / t - h, t / F(4, 9) + h, t / F(4, 9)],
         "Divide first: %s ÷ %s = %s × %s = %s = %s. Then %s − %s = %s = <b>1</b>."
         % (fr(2, 3), fr(4, 9), fr(2, 3), fr(9, 4), fr(18, 12), fr(3, 2), fr(3, 2), fr(1, 2), fr(2, 2)))
    # 16
    item("%s + %s ÷ %s" % (fr(3, 4), fr(1, 4), fr(1, 2)), t4 + q / h,
         [(t4 + q) / h, t4 + q * h, F(5, 4) / h],
         "Divide first: %s ÷ %s = %s × 2 = %s. Then %s + %s = %s = <b>1 %s</b>."
         % (fr(1, 4), fr(1, 2), fr(1, 4), fr(1, 2), fr(3, 4), fr(2, 4), fr(5, 4), fr(1, 4)))
    # 17
    x, y = M(2, 1, 4), P(3, 4)
    item("2 %s ÷ %s − 1 %s" % (fr(1, 4), fr(3, 4), fr(1, 2)), x.v / y.v - F(3, 2),
         [x.v * y.v - F(3, 2), F(2) + F(1, 3) - F(3, 2), x.v / y.v + F(3, 2)],
         "Divide first: 2 %s ÷ %s = %s × %s = %s = 3. Then 3 − 1 %s = <b>1 %s</b>."
         % (fr(1, 4), fr(3, 4), fr(9, 4), fr(4, 3), fr(36, 12), fr(1, 2), fr(1, 2)))
    # 18 substitution
    item(("Evaluate 2<i>a</i> + <i>b</i> when <i>a</i> = %s and <i>b</i> = %s." + SIMPLE) % (fr(3, 4), fr(1, 6)),
         2 * t4 + s6, [2 + t4 + s6, 2 * (t4 + s6), t4 + s6, F(6, 4) + F(1, 4)],
         "2<i>a</i> means 2 × <i>a</i>: 2 × %s = %s = 1 %s. Then 1 %s + %s = 1 %s + %s = <b>1 %s</b>."
         % (fr(3, 4), fr(6, 4), fr(1, 2), fr(1, 2), fr(1, 6), fr(3, 6), fr(1, 6), fr(2, 3)), prompt=None)
    # 19 substitution
    item(("Evaluate <i>x</i>² − <i>x</i> when <i>x</i> = %s." + SIMPLE) % fr(3, 2),
         F(3, 2) ** 2 - F(3, 2), [F(3) - F(3, 2), F(9, 2) - F(3, 2), F(9, 4) + F(3, 2)],
         "<i>x</i>² = (%s)² = %s. Then %s − %s = %s − %s = <b>%s</b>."
         % (fr(3, 2), fr(9, 4), fr(9, 4), fr(3, 2), fr(9, 4), fr(6, 4), fr(3, 4)), prompt=None)
    # 20 error analysis
    nm, he, his, him = Pp.next()
    q = "%s says %s + %s × %s = %s. What did %s do wrong?" % (nm, fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2), he)
    its.append(mcq(q, ("%s added before multiplying." % cap(he), None),
                   [("%s multiplied the denominators." % cap(he), None),
                    ("%s forgot to simplify." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "(%s + %s) × %s = 1 × %s = %s, so %s added first. BEDMAS says multiply first: "
                   "%s × %s = %s, then %s + %s = <b>%s</b>."
                   % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2), nm, fr(1, 2), fr(1, 2), fr(1, 4),
                      fr(1, 2), fr(1, 4), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Mixed operations with BEDMAS", "items": its}


# ============================================================ set 5: word problems
def set_words(Pp):
    its = []

    def add(q, correct, cands, e):
        its.append(mcq(q, correct, cands, e))

    # 1 recipe: fraction × mixed
    x, y = P(2, 3), M(2, 1, 4)
    nm, he, his, him = Pp.next()
    add("A maple cookie recipe needs 2 %s cups of flour. %s makes %s of the recipe. How much flour does %s need?"
        % (fr(1, 4), nm, fr(2, 3), he),
        S(x.v * y.v, "cups"),
        [S(F(2, 3) * 2 + F(1, 4), "cups"), S(y.v / x.v, "cups"), S(y.v - x.v, "cups"), S(y.v + x.v, "cups")],
        mul_e(x, y, "cups", "Find %s of 2 %s: %s × 2 %s. " % (fr(2, 3), fr(1, 4), fr(2, 3), fr(1, 4))))
    # 2 area
    x, y = M(2, 1, 2), M(1, 1, 3)
    add("A rectangular garden bed is 2 %s m long and 1 %s m wide. What is its area?" % (fr(1, 2), fr(1, 3)),
        S(x.v * y.v, "m²"),
        [S(2 + F(1, 6), "m²"), S(2 * (x.v + y.v), "m²"), S(x.v + y.v, "m²"), S(F(5, 2) * F(4, 3) / 2, "m²")],
        mul_e(x, y, "m²", "Area = length × width. "))
    # 3 trail: subtraction with regrouping
    x, y = M(4, 1, 2), M(2, 2, 3)
    nm, he, his, him = Pp.next()
    add("A trail in Algonquin Park is 4 %s km long. %s has hiked 2 %s km. How much farther does %s have to go?"
        % (fr(1, 2), nm, fr(2, 3), he),
        S(x.v - y.v, "km"), as_wrongs(x, y, "−", ["flip", "noborrow", "op"], "km"),
        addsub_e(x, y, "−", "km"))
    # 4 practice sessions
    x, y = M(4, 1, 2), P(3, 4)
    add("A hockey team has 4 %s h of ice time this week. Each practice is %s h long. How many practices can the team have?"
        % (fr(1, 2), fr(3, 4)),
        ("6 practices", F(6)),
        [("3 %s practices" % fr(3, 8), F(27, 8)), (fr(1, 6) + " practice", F(1, 6)), ("4 practices", F(4)),
         ("18 practices", F(18))],
        div_e(x, y, lead="How many %s h practices fit in 4 %s h? 4 %s ÷ %s. " % (fr(3, 4), fr(1, 2), fr(1, 2), fr(3, 4)))
        .replace("<b>6</b>", "<b>6</b> practices"))
    # 5 ribbon
    x, y = M(5, 1, 4), P(7, 8)
    add("A 5 %s m roll of ribbon is cut into pieces that are each %s m long. How many pieces are there?" % (fr(1, 4), fr(7, 8)),
        ("6 pieces", F(6)),
        [("4 %s pieces" % fr(19, 32), F(147, 32)), (fr(1, 6) + " piece", F(1, 6)), ("5 pieces", F(5)),
         ("42 pieces", F(42))],
        div_e(x, y, lead="5 %s ÷ %s. " % (fr(1, 4), fr(7, 8))).replace("<b>6</b>", "<b>6</b> pieces"))
    # 6 canoe trip: add mixed
    x, y = M(3, 3, 4), M(4, 2, 3)
    add("On a canoe trip, a group paddles 3 %s km before lunch and 4 %s km after lunch. How far do they paddle in all?"
        % (fr(3, 4), fr(2, 3)),
        S(x.v + y.v, "km"), as_wrongs(x, y, "+", ["nocarry", "dens", "numer", "one"], "km"),
        addsub_e(x, y, "+", "km"))
    # 7 fraction of the rest
    nm, he, his, him = Pp.next()
    add("%s has $60. %s spends %s of it on a book. Then %s spends %s of the money that is left on a skating pass. "
        "How much money does %s have now?" % (nm, cap(he), fr(1, 4), he, fr(2, 3), he),
        ("$15", F(15)), [("$5", F(5)), ("$30", F(30)), ("$45", F(45))],
        "%s of $60 = $15, so $60 − $15 = $45 is left. %s of $45 = $30. $45 − $30 = <b>$15</b>. "
        "(%s of the money that is left, not %s of $60.)" % (fr(1, 4), fr(2, 3), fr(2, 3), fr(2, 3)))
    # 8 pizza shared
    x, y = P(2, 3), W(4)
    add("Four friends share %s of a pizza equally. What fraction of the whole pizza does each friend get?" % fr(2, 3),
        R(1, 6), [S(F(8, 3)), S(F(6)), R(1, 2), R(2, 7)],
        div_e(x, y, lead="%s ÷ 4. " % fr(2, 3)))
    # 9 fraction of a fraction
    add("In a school garden, %s of the area is vegetables. Tomatoes fill %s of the vegetable area. "
        "What fraction of the whole garden is tomatoes?" % (fr(3, 4), fr(2, 5)),
        R(3, 10), [S(F(3, 4) + F(2, 5)), S(F(3, 4) - F(2, 5)), S(F(3, 4) / F(2, 5)), R(5, 9)],
        mul_e(P(2, 5), P(3, 4), lead="%s of %s means %s × %s. " % (fr(2, 5), fr(3, 4), fr(2, 5), fr(3, 4))))
    # 10 snowfall: three mixed numbers
    add("It snowed 2 %s cm on Monday, 1 %s cm on Tuesday and 3 %s cm on Wednesday. How much snow fell in all?"
        % (fr(3, 4), fr(1, 2), fr(1, 3)),
        S(F(11, 4) + F(3, 2) + F(10, 3), "cm"),
        [S(6 + F(5, 9), "cm"), S(6 + F(5, 12), "cm"), S(F(11, 4) + F(3, 2) + F(10, 3) - 1, "cm"),
         S(6 + F(1, 2), "cm")],
        "Whole numbers: 2 + 1 + 3 = 6. Fractions with denominator 12: %s + %s + %s = %s = 1 %s. "
        "6 + 1 %s = <b>7 %s cm</b>." % (fr(9, 12), fr(6, 12), fr(4, 12), fr(19, 12), fr(7, 12), fr(7, 12), fr(7, 12)))
    # 11 maple syrup bottles
    x, y = M(12, 1, 2), P(5, 8)
    add("A sugar shack has 12 %s L of maple syrup. It fills bottles that each hold %s L. How many bottles can it fill?"
        % (fr(1, 2), fr(5, 8)),
        ("20 bottles", F(20)),
        [("7 %s bottles" % fr(13, 16), F(125, 16)), (fr(1, 20) + " bottle", F(1, 20)), ("100 bottles", F(100)),
         ("12 bottles", F(12))],
        div_e(x, y, lead="12 %s ÷ %s. " % (fr(1, 2), fr(5, 8))).replace("<b>20</b>", "<b>20</b> bottles"))
    # 12 speed
    nm, he, his, him = Pp.next()
    add("%s walks %s km in %s h. At this rate, how many kilometres does %s walk in 1 h?" % (nm, fr(3, 4), fr(1, 6), he),
        S(F(9, 2), "km"), [R(1, 8, "km"), S(F(2, 9), "km"), S(F(11, 12), "km"), S(F(7, 12), "km")],
        div_e(P(3, 4), P(1, 6), "km", "Distance ÷ time: %s ÷ %s. " % (fr(3, 4), fr(1, 6))))
    # 13 recipe scale up
    x, y = M(1, 2, 3), M(1, 1, 2)
    add("A pancake recipe for 4 people uses 1 %s cups of milk. How much milk is needed for 6 people?" % fr(2, 3),
        S(x.v * y.v, "cups"),
        [S(1 + F(1, 3), "cups"), S(x.v + y.v, "cups"), S(x.v + 2, "cups"), S(x.v / y.v, "cups")],
        "6 people is 6 ÷ 4 = 1 %s times as many. " % fr(1, 2) + mul_e(x, y, "cups"))
    # 14 board cut
    nm, he, his, him = Pp.next()
    add("At the cottage, %s cuts 3 pieces that are each %s m long from a board that is 2 %s m long. "
        "How much of the board is left?" % (nm, fr(5, 8), fr(2, 5)),
        S(F(12, 5) - 3 * F(5, 8), "m"),
        [S(F(12, 5) - F(5, 8), "m"), S(F(12, 5) - F(15, 24), "m"), S(1 + abs(F(2, 5) - F(7, 8)), "m"),
         S(F(12, 5) - F(15, 8) + 1, "m")],
        "The pieces use 3 × %s = %s = 1 %s m. Use denominator 40: 2 %s = %s and %s = %s. "
        "%s − %s = <b>%s m</b>." % (fr(5, 8), fr(15, 8), fr(7, 8), fr(2, 5), fr(96, 40), fr(15, 8), fr(75, 40),
                                    fr(96, 40), fr(75, 40), fr(21, 40)))
    # 15 painting: whole job time
    nm, he, his, him = Pp.next()
    x, y = M(1, 1, 2), P(2, 3)
    add("%s paints %s of a fence in 1 %s h. At the same rate, how long will the whole fence take?" % (nm, fr(2, 3), fr(1, 2)),
        S(x.v / y.v, "h"), [S(1, "h"), S(y.v / x.v, "h"), S(F(3), "h")],
        div_e(x, y, "h", "%s of the fence takes 1 %s h, so the whole fence takes 1 %s ÷ %s. " % (fr(2, 3), fr(1, 2), fr(1, 2), fr(2, 3)),
              " Check: %s of 2 %s h is 1 %s h." % (fr(2, 3), fr(1, 4), fr(1, 2))))
    # 16 trip remaining
    add("A family drives from Ottawa to Toronto, a trip of about 450 km. They have driven %s of the way. "
        "About how many kilometres are left?" % fr(3, 5),
        ("180 km", F(180)), [("270 km", F(270)), ("90 km", F(90)), ("750 km", F(750))],
        "%s of 450 km = 450 ÷ 5 × 3 = 270 km driven. 450 − 270 = <b>180 km</b> left "
        "(that is %s of the trip)." % (fr(3, 5), fr(2, 5)))
    # 17 mean
    add("Three students run 2 %s km, 3 %s km and 2 %s km in gym class. What is the mean distance?"
        % (fr(1, 2), fr(1, 4), fr(3, 4)),
        S(F(17, 6), "km"), [S(F(17, 2), "km"), S(F(17, 4), "km"), S(F(7, 3), "km"), S(F(8, 3) + F(1, 2), "km")],
        "Total: 2 %s + 3 %s + 2 %s = 8 %s km. Mean: 8 %s ÷ 3 = %s × %s = %s = <b>2 %s km</b>."
        % (fr(1, 2), fr(1, 4), fr(3, 4), fr(1, 2), fr(1, 2), fr(17, 2), fr(1, 3), fr(17, 6), fr(5, 6)))
    # 18 tiles along a wall
    x, y = M(2, 1, 4), P(3, 8)
    add("Square tiles are %s m wide. How many tiles fit in a row along a wall that is 2 %s m long?" % (fr(3, 8), fr(1, 4)),
        ("6 tiles", F(6)),
        [(fr(27, 32) + " tile", F(27, 32)), (fr(1, 6) + " tile", F(1, 6)), ("18 tiles", F(18)), ("8 tiles", F(8))],
        div_e(x, y, lead="2 %s ÷ %s. " % (fr(1, 4), fr(3, 8))).replace("<b>6</b>", "<b>6</b> tiles"))
    # 19 reverse: tank
    add("A water tank is %s full. It holds 45 L of water now. How many litres does it hold when it is full?" % fr(3, 4),
        ("60 L", F(60)), [("33 %s L" % fr(3, 4), F(135, 4)), ("15 L", F(15)), ("180 L", F(180))],
        "%s of the tank is 45 L, so the full tank is 45 ÷ %s = 45 × %s = <b>60 L</b>. Check: %s of 60 L = 45 L."
        % (fr(3, 4), fr(3, 4), fr(4, 3), fr(3, 4)))
    # 20 two-step: Terry Fox Run
    nm, he, his, him = Pp.next()
    add("The Terry Fox Run route is 5 km. %s walks %s of the route and runs the rest. How many kilometres does %s run?"
        % (nm, fr(2, 5), he),
        ("3 km", F(3)), [("2 km", F(2)), ("4 %s km" % fr(3, 5), F(23, 5)), ("12 %s km" % fr(1, 2), F(25, 2))],
        "%s walks %s × 5 = 2 km. The rest is 5 − 2 = <b>3 km</b>. (Or %s of 5 km = 3 km.)" % (nm, fr(2, 5), fr(3, 5)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with fractions", "items": its}


# ============================================================ lesson
def body_html():
    bars_fig = ("<figure class='sn-fig'>" + sum_bars_svg(3, 4) +
                "<figcaption>" + fr(1, 3) + " + " + fr(1, 4) + ": rename both in twelfths. 4 twelfths + 3 twelfths = "
                + fr(7, 12) + ".</figcaption></figure>")
    area_fig = ("<figure class='sn-fig'>" + area_svg(3, 4, 2, 3) +
                "<figcaption>" + fr(2, 3) + " × " + fr(3, 4) + ": 6 of the 12 small rectangles are dark, so the product is "
                + fr(6, 12) + " = " + fr(1, 2) + ".</figcaption></figure>")
    group_fig = ("<figure class='sn-fig'>" + groups_svg(3, 8, 18, 3) +
                 "<figcaption>2 " + fr(1, 4) + " ÷ " + fr(3, 8) + ": 2 " + fr(1, 4) + " = 18 eighths, and 18 eighths make "
                 "6 groups of 3 eighths.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p><b>Add and subtract</b> with a common denominator. <b>Multiply</b> straight across. "
        "<b>Divide</b> by multiplying by the reciprocal. Change mixed numbers to improper fractions before you "
        "multiply or divide. When there is more than one operation, follow <b>BEDMAS</b>.</p>"
        "<h2>Add and subtract</h2>"
        "<p>Rename the fractions with a common denominator. Then add or subtract the numerators only. "
        "The denominator tells the size of the pieces, so it stays the same.</p>"
        + bars_fig
        + ex("Example 1", "3 " + fr(5, 6) + " + 2 " + fr(3, 4) + " = ?",
             "Whole numbers: 3 + 2 = 5. Fractions: " + fr(10, 12) + " + " + fr(9, 12) + " = " + fr(19, 12)
             + " = 1 " + fr(7, 12) + ". 5 + 1 " + fr(7, 12) + " = 6 " + fr(7, 12) + ".", "6 " + fr(7, 12))
        + ex("Example 2", "5 " + fr(1, 4) + " − 2 " + fr(2, 3) + " = ?",
             fr(1, 4) + " is less than " + fr(2, 3) + ", so use improper fractions: " + fr(63, 12) + " − " + fr(32, 12)
             + " = " + fr(31, 12) + " = 2 " + fr(7, 12) + ".", "2 " + fr(7, 12))
        + "<h2>Multiply</h2>"
        "<p>Multiply the numerators and multiply the denominators. Simplify. "
        "Mixed numbers must become improper fractions first.</p>"
        + area_fig
        + ex("Example 3", "1 " + fr(1, 2) + " × 2 " + fr(1, 3) + " = ?",
             fr(3, 2) + " × " + fr(7, 3) + " = " + fr(21, 6) + " = 3 " + fr(1, 2) + ".", "3 " + fr(1, 2))
        + "<h2>Divide</h2>"
        "<p>Keep the first number, change ÷ to ×, and flip the divisor (use its reciprocal).</p>"
        + group_fig
        + ex("Example 4", "3 " + fr(3, 4) + " ÷ 1 " + fr(1, 4) + " = ?",
             fr(15, 4) + " ÷ " + fr(5, 4) + " = " + fr(15, 4) + " × " + fr(4, 5) + " = " + fr(60, 20) + " = 3. "
             "Check: 3 × 1 " + fr(1, 4) + " = 3 " + fr(3, 4) + ".", "3")
        + "<h2>More than one operation: BEDMAS</h2>"
        "<p>Brackets, Exponents, Division and Multiplication (left to right), Addition and Subtraction (left to right).</p>"
        + ex("Example 5", fr(1, 2) + " + " + fr(1, 4) + " × " + fr(2, 3) + " = ?",
             "Multiply first: " + fr(1, 4) + " × " + fr(2, 3) + " = " + fr(2, 12) + " = " + fr(1, 6) + ". Then "
             + fr(3, 6) + " + " + fr(1, 6) + " = " + fr(4, 6) + " = " + fr(2, 3) + ".", fr(2, 3))
        + table(["Operation", "Common denominator?", "Mixed numbers"], [
            ["+ and −", "Yes", "Add wholes and fractions, or use improper fractions"],
            ["×", "No", "Change to improper fractions first"],
            ["÷", "No", "Change to improper fractions, then multiply by the reciprocal"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(1, 3) + " + " + fr(1, 4) + " = " + fr(2, 7) + " (adding the denominators)",
             "Use a common denominator: " + fr(4, 12) + " + " + fr(3, 12) + " = " + fr(7, 12) + "."],
            ["1 " + fr(1, 2) + " × 2 " + fr(1, 3) + " = 2 " + fr(1, 6)
             + " (multiplying whole parts and fraction parts separately)",
             "Change to improper fractions first: " + fr(3, 2) + " × " + fr(7, 3) + " = 3 " + fr(1, 2) + "."],
            [fr(4, 5) + " ÷ " + fr(2, 3) + " = " + fr(5, 4) + " × " + fr(2, 3) + " (flipping the wrong fraction)",
             "Flip only the divisor: " + fr(4, 5) + " × " + fr(3, 2) + " = 1 " + fr(1, 5) + "."],
            ["5 " + fr(1, 4) + " − 2 " + fr(2, 3) + " = 3 " + fr(5, 12) + " (subtracting the smaller fraction from the larger)",
             "Regroup 1 whole, or use improper fractions: the answer is 2 " + fr(7, 12) + "."],
            [fr(1, 2) + " + " + fr(1, 2) + " × " + fr(1, 2) + " = " + fr(1, 2) + " (working left to right)",
             "Multiply first: " + fr(1, 2) + " + " + fr(1, 4) + " = " + fr(3, 4) + "."],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract fractions with different denominators?",
     "a": "Rename the fractions with a common denominator, then add or subtract the numerators only. For example, 1/3 + 1/4 = 4/12 + 3/12 = 7/12, not 2/7."},
    {"q": "How do you multiply mixed numbers in Grade 8?",
     "a": "Change each mixed number to an improper fraction, multiply the numerators and the denominators, then simplify. For example, 1 1/2 × 2 1/3 = 3/2 × 7/3 = 21/6 = 3 1/2."},
    {"q": "How do you divide a fraction by a fraction?",
     "a": "Keep the first fraction, change ÷ to ×, and flip the second fraction (use its reciprocal). For example, 3/4 ÷ 3/8 = 3/4 × 8/3 = 2."},
    {"q": "What order of operations do Ontario students use with fractions?",
     "a": "Ontario classrooms use BEDMAS: brackets, exponents, division and multiplication from left to right, then addition and subtraction from left to right. For example, 1/2 + 1/4 × 2/3 = 1/2 + 1/6 = 2/3."},
]


def gen():
    rnd = random.Random(48806)
    Pp = People(rnd)
    sets = [set_addsub(), set_multiply(Pp), set_divide(Pp), set_bedmas(Pp), set_words(Pp)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "operations-with-fractions",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Operations with Fractions",
        "seo_title": "Grade 8 Operations with Fractions Worksheets: Mixed Numbers, Multiplying, Dividing and BEDMAS (Free, Answer Key, Ontario)",
        "short_title": "Operations with fractions",
        "domain": "Number",
        "standard_code": "Grade 8: B2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide fractions by fractions, as well as by whole numbers and mixed numbers, in various contexts",
        "meta_desc": "Free Grade 8 math worksheets on operations with fractions for the Ontario curriculum: adding and subtracting with unlike denominators and mixed numbers, multiplying and dividing fractions and mixed numbers, BEDMAS and word problems. 100 questions with an answer key.",
        "key_big": "Add and subtract with a common denominator. Multiply straight across. To divide, multiply by the reciprocal. Change mixed numbers to improper fractions before you multiply or divide.",
        "key_sub": "1/3 + 1/4 = 4/12 + 3/12 = 7/12, not 2/7. 1 1/2 × 2 1/3 = 3/2 × 7/3 = 3 1/2, not 2 1/6. With more than one operation, follow BEDMAS.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(three bars|[0-9]+ wholes,)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
