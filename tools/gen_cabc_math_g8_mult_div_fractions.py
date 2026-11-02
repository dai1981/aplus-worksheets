# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Multiplying and Dividing Fractions (BC Mathematics Curriculum, Computational fluency:
operations with fractions, including order of operations)
  python3 tools/gen_cabc_math_g8_mult_div_fractions.py
Multiply fractions (area model, simplify before multiplying), multiply mixed numbers (change to improper
fractions first), divide by multiplying by the reciprocal (keep, change, flip only the divisor), the order of
operations (BEDMAS) with fractions, and word problems in BC contexts.
Answers are in simplest form (mixed numbers when greater than 1). Every answer is checked with
fractions.Fraction; no two choices are equal in value; every explanation ends with the correct choice.
Wrong answers are real student mistakes: flipping the wrong fraction (or both), multiplying without flipping,
adding across, cross-multiplying, multiplying the whole parts and the fraction parts separately, writing a
mixed number as (whole + numerator)/denominator, ignoring BEDMAS (working left to right, adding first).
Helpers are adapted from gen_caon_math_g7_mult_div_fractions.py (area model, fraction bar, mistakes).
BC style: Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
G1 = "#3f9a63"        # dark part / group colour 1
G2 = "#a6dbb7"        # group colour 2
LIGHT = "#d7ecdf"     # light part of an area model
DARKLINE = "#006633"
PART = "#f3c9c4"      # partial group
LINE = "#2b2b2b"
GRAY = "#8a8178"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
PL = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 9: "ninths",
      10: "tenths", 12: "twelfths", 15: "fifteenths", 20: "twentieths", 24: "twenty-fourths"}
SG = {2: "half", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 8: "eighth", 9: "ninth",
      10: "tenth", 12: "twelfth", 15: "fifteenth", 20: "twentieth", 24: "twenty-fourth"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(v):
    """A positive Fraction in simplest form, mixed when greater than 1: 7/12, 1 1/6, 2."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%d %s" % (w, fr(r, v.denominator))


def imp(v):
    """Whole number or (possibly improper) fraction."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def plain(h):
    return re.sub(r"<span class='fr'><span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span></span>",
                  r"\1/\2", h)


def tx(v):
    """Plain-text form for SVG labels: 3/4, 1 1/2."""
    return re.sub("<[^>]+>", "", plain(show(v)))


def lcm(a, b):
    return a * b // gcd(a, b)


def pl(k, one, many):
    return one if k == 1 else many


def cap(s):
    return s[0].upper() + s[1:]


def mul(x, y):
    return "%s × %s" % (show(x), show(y))


def dv(x, y):
    return "%s ÷ %s" % (show(x), show(y))


def qty(v, one, many=None):
    many = one if many is None else many
    return "%s %s" % (show(v), one if F(v) <= 1 else many)


def mcq(q, correct, cands, e):
    """correct / cands: (html, value). value None = not a number. A candidate equal in value to an
    earlier choice (or not positive) is skipped. Positions are set later by balance()."""
    ch, vals = [correct[0]], ({correct[1]} if correct[1] is not None else set())
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
            continue
        ch.append(h)
        if v is not None:
            vals.add(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e, "_num": correct[1] is not None}


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


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
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
    """Tag wide pictures (fraction bars) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


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
        s.append(text(x, T + BH + 26, str(j), 16))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, total * PW, BH, LINE))
    g = 0
    while g * m < k:
        x0 = X0 + g * m * PW + 2
        x1 = X0 + min(k, (g + 1) * m) * PW - 2
        isfull = (g + 1) * m <= k
        colr = LINE if isfull else RED
        s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, T - 4, T - 12, x1, T - 4, colr))
        if isfull:
            s.append(text((x0 + x1) / 2.0, T - 16, str(g + 1), 15))
        elif (g + 1) * m <= total:          # dashed: how long a full group would be
            xf = X0 + (g + 1) * m * PW - 2
            s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0, T - 16, T - 24, xf, T - 16, GRAY))
        g += 1
    label = "fraction bar: %s shaded in groups of %s, %d pieces in each whole" % (tx(a), tx(b), L)
    return svg_wrap(W, T + BH + 32, "".join(s), label)


# ------------------------------------------------------------ explanations
def conv(v):
    """Sentence that rewrites a whole or mixed number as a fraction (or '')."""
    v = F(v)
    if v.denominator == 1:
        return "Write %d as %s. " % (v.numerator, fr(v.numerator, 1))
    if v > 1:
        return "Write %s as %s. " % (show(v), fr(v.numerator, v.denominator))
    return ""


def chain(x, y, cancel, unit=""):
    """x × y with x, y as fractions (improper allowed). Returns the working ending in <b>answer</b>."""
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    s = ""
    steps = []
    if cancel:
        g1, g2 = gcd(a, d), gcd(c, b)
        for g, p, q in ((g1, a, d), (g2, c, b)):
            if g > 1:
                steps.append(("the %ds cancel" % p) if p == q else ("divide %d and %d by %d" % (p, q, g)))
        a, d = a // g1, d // g1
        c, b = c // g2, b // g2
    n, m = a * c, b * d
    v = F(n, m)
    if steps:
        s += "Simplify first: " + ", and ".join(steps) + ". "
        s += "Now %s × %s = " % (imp(F(a, b)), imp(F(c, d)))
        parts = [imp(v)]
    else:
        s += "%s × %s = %s = " % (fr(a, b), fr(c, d), fr("%d × %d" % (a, c), "%d × %d" % (b, d)))
        parts = [fr(n, m)] if m != 1 else [str(n)]
        if m != 1 and gcd(n, m) > 1:
            parts.append(imp(v))
    if v.denominator != 1 and v > 1:
        parts.append(show(v))
    last = parts[-1] + (" " + unit if unit else "")
    s += "".join(p + " = " for p in parts[:-1]) + "<b>%s</b>." % last
    return s


def mul_e(x, y, cancel=True, unit="", lead="", convert=True):
    x, y = F(x), F(y)
    s = lead + ((conv(x) + conv(y)) if convert else "")
    if not cancel:
        s += "Multiply the numerators and multiply the denominators: "
    return s + chain(x, y, cancel, unit)


def div_e(x, y, unit="", lead="", check=True):
    x, y = F(x), F(y)
    q = x / y
    s = lead + conv(x) + conv(y)
    s += "Keep %s, change ÷ to ×, and flip only the divisor %s to %s. " % (imp(x), imp(y), imp(1 / y))
    s += chain(x, 1 / y, True, unit)
    if check:
        s += " Check: %s × %s = %s." % (show(q), show(y), show(x))
    return s


def e_groups(a, b):
    """How many groups of b fit in a, explained with pieces of a common denominator."""
    q = a / b
    L = lcm(a.denominator, b.denominator)
    k, m = int(a * L), int(b * L)
    nm, one = PL[L], SG[L]
    eq = []
    for v, c in ((a, k), (b, m)):
        if not (v.denominator == L and v < 1):
            eq.append("%s = %s" % (show(v), fr(c, L)))
    s = "Use %s%s. " % (nm, (": " + " and ".join(eq)) if eq else "")
    s += "Each group is %d %s. " % (m, pl(m, one, nm))
    full, r = divmod(k, m)
    if r == 0:
        s += "%d %s make %d ÷ %d = %d %s. " % (k, nm, k, m, full, pl(full, "group", "groups"))
    else:
        s += ("%d %s make %d full %s, with %d %s left over. %s %s of a group. "
              % (k, nm, full, pl(full, "group", "groups"), r, pl(r, one, nm),
                 ("That 1 " + one + " is") if r == 1 else ("Those %d %s are" % (r, nm)), fr(r, m)))
    s += "So %s = <b>%s</b>. Check: %s × %s = %s." % (dv(a, b), show(q), show(q), show(b), show(a))
    return s


# ------------------------------------------------------------ typical wrong answers
def split(v):
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    return w, F(r, v.denominator)


def badimp(v):
    """Mixed number converted the wrong way: w n/d -> (w + n)/d."""
    v = F(v)
    w, f = split(v)
    if w == 0 or f == 0:
        return v
    return F(w + f.numerator, f.denominator)


def mwr(x, y, order):
    """x × y: values from real mistakes."""
    x, y = F(x), F(y)
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    out = []
    for k in order:
        if k == "addfr":                    # added across: (a + c)/(b + d)
            out.append(F(a + c, b + d))
        elif k == "cross":                  # cross-multiplied: (a × d)/(b × c)
            out.append(F(a * d, b * c))
        elif k == "add":                    # added the fractions
            out.append(x + y)
        elif k == "addden":                 # multiplied the numerators, added the denominators
            out.append(F(a * c, b + d))
        elif k == "sameden":                # kept the denominator, as when adding
            if b == d:
                out.append(F(a * c, b))
        elif k == "parts":                  # multiplied the whole parts and the fraction parts
            (w1, f1), (w2, f2) = split(x), split(y)
            if w1 or w2:
                out.append(w1 * w2 + f1 * f2)
        elif k == "badimp":
            out.append(badimp(x) * badimp(y))
        else:
            raise ValueError(k)
    return out


def dwr(x, y, order):
    """x ÷ y: values from real mistakes."""
    x, y = F(x), F(y)
    q = x / y
    out = []
    for k in order:
        if k == "nf":                       # multiplied without flipping
            out.append(x * y)
        elif k == "first":                  # flipped the first fraction instead
            out.append(y / x)
        elif k == "both":                   # flipped both
            out.append(1 / (x * y))
        elif k == "parts":                  # divided the whole parts and the fraction parts
            (w1, f1), (w2, f2) = split(x), split(y)
            if w1 and w2 and f1 and f2:
                out.append(F(w1, w2) + f1 / f2)
        elif k == "fracflip":               # flipped only the fraction part of the divisor
            w2, f2 = split(y)
            if w2 and f2:
                out.append(x * (w2 + 1 / f2))
        elif k == "badimp":
            out.append(badimp(x) / badimp(y))
        elif k == "leftover":               # leftover pieces written as part of a whole
            L = lcm(x.denominator, y.denominator)
            kk, m = int(x * L), int(y * L)
            if q.denominator != 1 and kk > m:
                out.append(kk // m + F(kk % m, L))
        elif k == "drop":                   # dropped the leftover
            if q.denominator != 1 and q > 1:
                out.append(F(math.floor(q)))
        elif k == "addfr":
            out.append(F(x.numerator + y.numerator, x.denominator + y.denominator))
        else:
            raise ValueError(k)
    return out


def S(v):
    return (show(v), F(v))


def Ss(vals):
    return [S(v) for v in vals if F(v) > 0]


def Q(vals, one, many=None):
    return [(qty(v, one, many), F(v)) for v in vals if F(v) > 0]


def ask(expr, v):
    """'expr = ?' plus a hint when the answer is a mixed number."""
    q = "%s = <b>?</b>" % expr
    v = F(v)
    if v > 1 and v.denominator != 1:
        q += "<br>Give the answer as a mixed number."
    return q


# ============================================================ set 1: multiply fractions
def set_multiply(P):
    its = []
    # A) area model: what fraction of the square is dark
    for a1, b1, a2, b2 in [(3, 5, 2, 3), (3, 4, 1, 2), (4, 5, 3, 4)]:
        n, d = a1 * a2, b1 * b2
        v = F(n, d)
        q = (fig(area_svg(a1, b1, a2, b2)) + "The model shows %s × %s. What fraction of the whole square is dark? "
             "Give the answer in simplest form." % (fr(a2, b2), fr(a1, b1)))
        cands = Ss([F(n, d - n), F(a1 + a2, b1 + b2), F(n, a1 * b2), F(a1, b1), F(a2, b2)])
        e = ("The square is cut into %d × %d = %d equal small rectangles, and %d × %d = %d of them are dark. "
             "So %s × %s = %s" % (b1, b2, d, a1, a2, n, fr(a2, b2), fr(a1, b1), fr(n, d)))
        e = e[:-len(fr(n, d))] + ("%s = <b>%s</b>." % (fr(n, d), show(v)) if gcd(n, d) > 1 else "<b>%s</b>." % show(v))
        its.append(mcq(q, S(v), cands, e))
    # B) area model: which multiplication
    a1, b1, a2, b2 = 3, 4, 2, 3
    q = (fig(area_svg(a1, b1, a2, b2)) + "The square is 1 whole. The light columns are %s of the square, and the dark "
         "part is a part of the light columns. Which multiplication does the dark part show?" % fr(a1, b1))
    right = "%s × %s" % (fr(a2, b2), fr(a1, b1))
    cands = [("%s × %s" % (fr(b2 - a2, b2), fr(a1, b1)), F(b2 - a2, b2) * F(a1, b1)),
             ("%s + %s" % (fr(a2, b2), fr(a1, b1)), F(a2, b2) + F(a1, b1)),
             ("%s × %s" % (fr(a2, b2), fr(b1 - a1, b1)), F(a2, b2) * F(b1 - a1, b1))]
    e = ("The light part is %d of %d columns: %s of the square. The dark part is %d of the %d rows of the light part. "
         "So the dark part is %s of %s: <b>%s</b> = %s = %s." %
         (a1, b1, fr(a1, b1), a2, b2, fr(a2, b2), fr(a1, b1), right, fr(6, 12), fr(1, 2)))
    its.append(mcq(q, (right, F(a2, b2) * F(a1, b1)), cands, e))
    # C) multiply across
    for (a, b), (c, d), order in [((1, 3), (2, 5), ["addfr", "cross", "add", "addden"]),
                                  ((3, 4), (3, 5), ["cross", "addfr", "addden", "add"]),
                                  ((2, 7), (3, 4), ["addfr", "addden", "cross", "add"]),
                                  ((5, 8), (1, 3), ["add", "addfr", "cross", "addden"]),
                                  ((4, 5), (2, 3), ["addfr", "cross", "addden", "add"]),
                                  ((1, 6), (3, 7), ["cross", "addfr", "add", "addden"]),
                                  ((2, 9), (4, 5), ["addden", "addfr", "cross", "add"]),
                                  ((3, 8), (3, 8), ["sameden", "addfr", "cross", "add"])]:
        x, y = F(a, b), F(c, d)
        q = ask("%s × %s" % (fr(a, b), fr(c, d)), x * y)
        its.append(mcq(q, S(x * y), Ss(mwr(x, y, order)), mul_e(x, y, cancel=False)))
    # D) simplify before multiplying
    orders = [["addfr", "cross", "add", "addden"], ["cross", "addfr", "addden", "add"],
              ["addfr", "add", "cross", "addden"], ["cross", "add", "addfr", "addden"]]
    for i, ((a, b), (c, d)) in enumerate([((5, 8), (4, 15)), ((9, 14), (7, 12)), ((6, 25), (10, 9)),
                                          ((8, 21), (14, 9))]):
        x, y = F(a, b), F(c, d)
        q = ask("%s × %s" % (fr(a, b), fr(c, d)), x * y)
        its.append(mcq(q, S(x * y), Ss(mwr(x, y, orders[i])), mul_e(x, y, convert=False)))
    # E) simplifying two numerators
    nm, he, his = P.next()
    q = ("%s wants to simplify %s × %s before multiplying, so %s divides 6 and 14 by 2. What is wrong?"
         % (nm, fr(6, 35), fr(14, 9), he))
    its.append(mcq(q, ("6 and 14 are both numerators. Pair a numerator with a denominator.", None),
                   [("Nothing. Any two numbers that share a factor can be divided.", None),
                    ("%s should divide 6 and 14 by 7." % cap(he), None),
                    ("You can never simplify before multiplying.", None)],
                   "Dividing two numerators changes the value. Pair each numerator with a denominator: 6 and 9 share 3, "
                   "and 14 and 35 share 7. Then %s × %s = %s. <b>6 and 14 are both numerators</b>, so %s cannot divide "
                   "them both." % (fr(2, 5), fr(2, 3), fr(4, 15), he)))
    # F) whole number × fraction
    its.append(mcq(ask("6 × %s" % fr(2, 3), 4), S(4),
                   [(fr(12, 18), F(2, 3)), S(9), S(F(20, 3))],
                   "Write 6 as %s. %s × %s = %s = <b>4</b>. Multiply only the numerator by 6. "
                   "(%s is wrong: it multiplies the denominator too.)"
                   % (fr(6, 1), fr(6, 1), fr(2, 3), fr(12, 3), fr(12, 18))))
    its.append(mcq(ask("10 × %s" % fr(3, 4), F(15, 2)), S(F(15, 2)),
                   [(fr(30, 40), F(3, 4)), S(F(40, 3)), S(F(43, 4))],
                   "Write 10 as %s. %s × %s = %s = %s = <b>%s</b>. Check: %s of 10 is a bit less than 10."
                   % (fr(10, 1), fr(10, 1), fr(3, 4), fr(30, 4), fr(15, 2), show(F(15, 2)), fr(3, 4))))
    # G) reasoning
    q = "Without calculating, which product is <b>greater</b> than %s?" % fr(3, 5)
    its.append(mcq(q, ("%s × %s" % (fr(3, 5), fr(5, 4)), None),
                   [("%s × %s" % (fr(3, 5), fr(4, 5)), None), ("%s × %s" % (fr(3, 5), fr(1, 2)), None),
                    ("%s × 1" % fr(3, 5), None)],
                   "Multiplying by a number greater than 1 makes the answer greater. %s is greater than 1, so "
                   "<b>%s × %s</b> is greater than %s. %s × 1 = %s, and %s and %s are less than 1."
                   % (fr(5, 4), fr(3, 5), fr(5, 4), fr(3, 5), fr(3, 5), fr(3, 5), fr(4, 5), fr(1, 2))))
    assert len(its) == 20, len(its)
    return {"title": "Multiply fractions", "items": its}


# ============================================================ set 2: multiply mixed numbers
def set_mixed(P):
    its = []
    # A) mixed number -> improper fraction
    for w, n, d in [(2, 3, 4), (3, 2, 5)]:
        v = F(w * d + n, d)
        q = "Write %d %s as an improper fraction." % (w, fr(n, d))
        its.append(mcq(q, (fr(w * d + n, d), v),
                       [(fr(w + n, d), F(w + n, d)), (fr(w * n, d), F(w * n, d)), (fr(w * d, d), F(w))],
                       "%d wholes are %d × %d = %d %s. Add the %d %s: %d + %d = %d. So %d %s = <b>%s</b>."
                       % (w, w, d, w * d, PL[d], n, PL[d] if n > 1 else SG[d], w * d, n, w * d + n, w, fr(n, d),
                          fr(w * d + n, d))))
    # B) multiply with mixed numbers
    mo = ["parts", "badimp", "add", "cross", "addfr"]
    for x, y in [(F(5, 2), F(2, 5)), (F(7, 3), F(3, 4)), (F(9, 4), F(2, 3)), (F(11, 4), F(8, 11)),
                 (F(3, 2), F(5, 3)), (F(7, 4), F(6, 5)), (F(10, 3), F(9, 5)), (F(5, 4), F(7, 3)),
                 (F(8, 3), F(15, 4)), (F(13, 5), F(5, 6)), (F(9, 2), F(7, 6)), (F(11, 6), F(9, 4))]:
        v = x * y
        its.append(mcq(ask(mul(x, y), v), S(v), Ss(mwr(x, y, mo)), mul_e(x, y)))
    # C) whole number × mixed number
    its.append(mcq(ask("3 × 2 %s" % fr(1, 4), F(27, 4)), S(F(27, 4)),
                   [S(F(25, 4)), S(F(15, 4)), S(F(21, 4))],
                   "Write 2 %s as %s. 3 × %s = %s = <b>6 %s</b>. (6 %s multiplies only the 2 by 3, "
                   "not the %s.)" % (fr(1, 4), fr(9, 4), fr(9, 4), fr(27, 4), fr(3, 4), fr(1, 4), fr(1, 4))))
    its.append(mcq(ask("4 × 1 %s" % fr(2, 3), F(20, 3)), S(F(20, 3)),
                   [S(F(14, 3)), S(F(17, 3)), S(4)],
                   "Write 1 %s as %s. 4 × %s = %s = <b>6 %s</b>. Check: 4 × 1 = 4 and 4 × %s = %s = 2 %s, "
                   "and 4 + 2 %s = 6 %s." % (fr(2, 3), fr(5, 3), fr(5, 3), fr(20, 3), fr(2, 3), fr(2, 3), fr(8, 3),
                                              fr(2, 3), fr(2, 3), fr(2, 3))))
    # D) estimate
    q = "Which is the best estimate for %s?" % mul(F(31, 8), F(19, 9))
    its.append(mcq(q, ("about 8", None), [("about 6", None), ("about 12", None), ("about 2", None)],
                   "Round each mixed number to the nearest whole number: %s is close to 4 and %s is close to 2. "
                   "4 × 2 = 8, so the product is <b>about 8</b>. (3 × 2 = 6 ignores the %s.)"
                   % (show(F(31, 8)), show(F(19, 9)), fr(7, 8))))
    # E) error analysis
    nm, he, his = P.next()
    q = ("%s says %s = 6 %s, because 2 × 3 = 6 and %s × %s = %s. What is wrong?"
         % (nm, mul(F(5, 2), F(10, 3)), fr(1, 6), fr(1, 2), fr(1, 3), fr(1, 6)))
    its.append(mcq(q, ("%s multiplied the whole parts and the fraction parts separately." % cap(he), None),
                   [("%s forgot to simplify %s." % (cap(he), fr(1, 6)), None),
                    ("%s should have flipped 3 %s." % (cap(he), fr(1, 3)), None),
                    ("Nothing. The answer is correct.", None)],
                   "A mixed number is a sum, so its parts cannot be multiplied separately. Change to improper fractions: "
                   "%s × %s = %s = %s = 8 %s. <b>%s multiplied the whole parts and the fraction parts separately</b>."
                   % (fr(5, 2), fr(10, 3), fr(50, 6), fr(25, 3), fr(1, 3), nm)))
    # F) missing factor
    q = "1 %s × <b>?</b> = 2" % fr(1, 2)
    its.append(mcq(q, S(F(4, 3)), Ss([F(3), F(1, 2), F(3, 4)]),
                   "Divide: 2 ÷ 1 %s = 2 ÷ %s = 2 × %s = %s = <b>1 %s</b>. Check: %s × %s = %s = 2."
                   % (fr(1, 2), fr(3, 2), fr(2, 3), fr(4, 3), fr(1, 3), fr(3, 2), fr(4, 3), fr(12, 6))))
    # G) reasoning
    q = "Without calculating, which product is <b>greater</b> than 2 %s?" % fr(1, 2)
    its.append(mcq(q, ("2 %s × 1 %s" % (fr(1, 2), fr(1, 5)), None),
                   [("2 %s × %s" % (fr(1, 2), fr(4, 5)), None), ("2 %s × %s" % (fr(1, 2), fr(1, 2)), None),
                    ("2 %s × 1" % fr(1, 2), None)],
                   "Multiplying by a number greater than 1 makes the answer greater. 1 %s is greater than 1, so "
                   "<b>2 %s × 1 %s</b> is greater than 2 %s. (It equals %s × %s = 3.)"
                   % (fr(1, 5), fr(1, 2), fr(1, 5), fr(1, 2), fr(5, 2), fr(6, 5))))
    assert len(its) == 20, len(its)
    return {"title": "Multiply mixed numbers", "items": its}


# ============================================================ set 3: divide by the reciprocal
def set_divide(P):
    its = []
    # A) reciprocals
    q = "What is the reciprocal of %s?" % fr(4, 7)
    its.append(mcq(q, (fr(7, 4), None), [(fr(4, 7), None), ("−" + fr(4, 7), None), (fr(3, 7), None)],
                   "Flip the fraction: the reciprocal of %s is <b>%s</b>. Check: %s × %s = %s = 1. "
                   "(−%s is the opposite, not the reciprocal.)" % (fr(4, 7), fr(7, 4), fr(4, 7), fr(7, 4), fr(28, 28),
                                                                  fr(4, 7))))
    q = "What is the reciprocal of 2 %s?" % fr(1, 3)
    its.append(mcq(q, (fr(3, 7), None), [(fr(7, 3), None), ("5", None), (fr(1, 2), None)],
                   "First write 2 %s as an improper fraction: %s. Then flip it: <b>%s</b>. Check: %s × %s = 1. "
                   "Do not flip only the %s." % (fr(1, 3), fr(7, 3), fr(3, 7), fr(7, 3), fr(3, 7), fr(1, 3))))
    # B) fraction bars: how many fit
    for a, b in [(F(3, 4), F(3, 8)), (F(2, 3), F(1, 4)), (F(5, 4), F(1, 2))]:
        q = (fig(groups_svg(a, b)) + "The bar shows %s. How many groups of %s fit in %s? %s = <b>?</b>"
             % (show(a), show(b), show(a), dv(a, b)))
        its.append(mcq(q, S(a / b), Ss(dwr(a, b, ["nf", "leftover", "first", "drop", "both"])), e_groups(a, b)))
    # C) which multiplication (flip the right fraction)
    for (a, b, c, d) in [(3, 5, 2, 7), (4, 9, 5, 6)]:
        q = "Which multiplication has the same answer as %s ÷ %s?" % (fr(a, b), fr(c, d))
        right = "%s × %s" % (fr(a, b), fr(d, c))
        cands = [("%s × %s" % (fr(b, a), fr(c, d)), F(b, a) * F(c, d)),
                 ("%s × %s" % (fr(b, a), fr(d, c)), F(b, a) * F(d, c)),
                 ("%s × %s" % (fr(a, b), fr(c, d)), F(a, b) * F(c, d))]
        e = ("Keep the first fraction, change ÷ to ×, and flip only the second fraction, the one you divide by: "
             "<b>%s</b>. Do not flip %s." % (right, fr(a, b)))
        its.append(mcq(q, (right, F(a, b) * F(d, c)), cands, e))
    # D) fraction ÷ fraction
    for a, b in [(F(2, 3), F(1, 6)), (F(3, 5), F(9, 10)), (F(5, 8), F(3, 4)), (F(7, 10), F(2, 5)),
                 (F(8, 9), F(4, 15)), (F(3, 7), F(6, 7)), (F(5, 6), F(5, 9))]:
        v = a / b
        its.append(mcq(ask(dv(a, b), v), S(v), Ss(dwr(a, b, ["first", "nf", "both", "addfr", "leftover"])),
                       div_e(a, b)))
    # E) mixed numbers
    do = ["first", "nf", "parts", "fracflip", "badimp", "leftover", "drop", "both"]
    for x, y in [(F(15, 4), F(5, 6)), (F(10, 3), F(5, 4)), (F(9, 2), F(3, 2)), (F(16, 5), F(8, 3))]:
        v = x / y
        its.append(mcq(ask(dv(x, y), v), S(v), Ss(dwr(x, y, do)), div_e(x, y)))
    # F) whole number ÷ fraction
    its.append(mcq(ask("6 ÷ %s" % fr(3, 4), 8), S(8), Ss([F(9, 2), F(1, 8), F(2)]),
                   "Keep 6, change ÷ to ×, and flip %s to %s. 6 × %s = %s = <b>8</b>. Check: 8 × %s = %s = 6. "
                   "(%s ÷ 6 = %s flips the wrong number.)"
                   % (fr(3, 4), fr(4, 3), fr(4, 3), fr(24, 3), fr(3, 4), fr(24, 4), fr(3, 4), fr(1, 8))))
    # G) error analysis: flipped the wrong fraction
    nm, he, his = P.next()
    q = ("%s writes %s = %s × %s = %s. What mistake did %s make?"
         % (nm, dv(F(3, 4), F(3, 8)), fr(4, 3), fr(3, 8), fr(1, 2), he))
    its.append(mcq(q, ("%s flipped %s instead of %s." % (cap(he), fr(3, 4), fr(3, 8)), None),
                   [("%s multiplied without flipping." % cap(he), None),
                    ("%s flipped both fractions." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "%s flipped the first fraction. Flip only the divisor: %s × %s = %s = 2. Check: 2 × %s = %s = %s. "
                   "So <b>%s flipped %s instead of %s</b>." % (nm, fr(3, 4), fr(8, 3), fr(24, 12), fr(3, 8), fr(6, 8),
                                                             fr(3, 4), he, fr(3, 4), fr(3, 8))))
    assert len(its) == 20, len(its)
    return {"title": "Divide by multiplying by the reciprocal", "items": its}


# ============================================================ set 4: order of operations
def set_bedmas(P):
    its = []

    def item(expr, correct, wrongs, e):
        its.append(mcq(ask(expr, correct), S(correct), Ss(wrongs), e))

    h, t, q4 = F(1, 2), F(1, 3), F(1, 4)
    # 1
    item("%s + %s × %s" % (fr(1, 3), fr(1, 2), fr(4, 5)), t + h * F(4, 5),
         [(t + h) * F(4, 5), t + h / F(4, 5), F(5, 10) * F(4, 5)],
         "Multiply first: %s × %s = %s = %s. Then %s + %s = %s + %s = <b>%s</b>."
         % (fr(1, 2), fr(4, 5), fr(4, 10), fr(2, 5), fr(1, 3), fr(2, 5), fr(5, 15), fr(6, 15), fr(11, 15)))
    # 2
    item("%s − %s ÷ 3" % (fr(3, 4), fr(1, 2)), F(3, 4) - h / 3,
         [(F(3, 4) - h) / 3, (F(3, 4) - h) * 3, F(3, 4) - h],
         "Divide first: %s ÷ 3 = %s × %s = %s. Then %s − %s = %s − %s = <b>%s</b>."
         % (fr(1, 2), fr(1, 2), fr(1, 3), fr(1, 6), fr(3, 4), fr(1, 6), fr(9, 12), fr(2, 12), fr(7, 12)))
    # 3
    item("(%s − %s) × %s" % (fr(5, 6), fr(1, 3), fr(4, 9)), (F(5, 6) - t) * F(4, 9),
         [F(5, 6) - t * F(4, 9), (F(5, 6) - t) / F(4, 9), F(5, 6) * F(4, 9) + t],
         "Brackets first: %s − %s = %s − %s = %s = %s. Then %s × %s = %s = <b>%s</b>."
         % (fr(5, 6), fr(1, 3), fr(5, 6), fr(2, 6), fr(3, 6), fr(1, 2), fr(1, 2), fr(4, 9), fr(4, 18), fr(2, 9)))
    # 4 left to right
    item("%s ÷ %s × %s" % (fr(2, 3), fr(4, 9), fr(1, 2)), F(2, 3) / F(4, 9) * h,
         [F(2, 3) / (F(4, 9) * h), F(2, 3) * F(4, 9) * h, F(3, 2) * F(4, 9) * h],
         "÷ and × have the same rank, so work from left to right. %s ÷ %s = %s × %s = %s = %s. "
         "Then %s × %s = <b>%s</b>." % (fr(2, 3), fr(4, 9), fr(2, 3), fr(9, 4), fr(18, 12), fr(3, 2), fr(3, 2),
                                        fr(1, 2), fr(3, 4)))
    # 5 exponent
    item("(%s)² + %s" % (fr(2, 3), fr(1, 9)), F(2, 3) ** 2 + F(1, 9),
         [F(4, 3) + F(1, 9), F(2, 3) + F(1, 9), (F(2, 3) + F(1, 9)) ** 2],
         "Exponent first: (%s)² = %s × %s = %s. Then %s + %s = <b>%s</b>. (Squaring is not × 2.)"
         % (fr(2, 3), fr(2, 3), fr(2, 3), fr(4, 9), fr(4, 9), fr(1, 9), fr(5, 9)))
    # 6
    item("3 − 1 %s × %s" % (fr(1, 2), fr(4, 3)), 3 - F(3, 2) * F(4, 3),
         [(3 - F(3, 2)) * F(4, 3), 3 - F(3, 2) / F(4, 3), 3 - (1 + h * F(4, 3))],
         "Multiply first: 1 %s × %s = %s × %s = %s = 2. Then 3 − 2 = <b>1</b>."
         % (fr(1, 2), fr(4, 3), fr(3, 2), fr(4, 3), fr(12, 6)))
    # 7
    item("1 %s × (%s + %s)" % (fr(3, 4), fr(1, 2), fr(1, 3)), F(7, 4) * (h + t),
         [F(7, 4) * h + t, F(7, 4) / (h + t), 1 + F(3, 4) * (h + t)],
         "Brackets first: %s + %s = %s + %s = %s. Then 1 %s × %s = %s × %s = %s = <b>1 %s</b>."
         % (fr(1, 2), fr(1, 3), fr(3, 6), fr(2, 6), fr(5, 6), fr(3, 4), fr(5, 6), fr(7, 4), fr(5, 6), fr(35, 24),
            fr(11, 24)))
    # 8
    item("%s ÷ (%s + %s)" % (fr(5, 6), fr(1, 4), fr(1, 3)), F(5, 6) / (q4 + t),
         [F(5, 6) / q4 + t, F(5, 6) * (q4 + t), (q4 + t) / F(5, 6)],
         "Brackets first: %s + %s = %s + %s = %s. Then %s ÷ %s = %s × %s = %s = <b>1 %s</b>."
         % (fr(1, 4), fr(1, 3), fr(3, 12), fr(4, 12), fr(7, 12), fr(5, 6), fr(7, 12), fr(5, 6), fr(12, 7),
            fr(10, 7), fr(3, 7)))
    # 9
    item("(%s)² ÷ %s" % (fr(3, 5), fr(9, 10)), F(3, 5) ** 2 / F(9, 10),
         [F(6, 5) / F(9, 10), F(3, 5) ** 2 * F(9, 10), F(9, 10) / F(3, 5) ** 2],
         "Exponent first: (%s)² = %s. Then %s ÷ %s = %s × %s = %s = <b>%s</b>."
         % (fr(3, 5), fr(9, 25), fr(9, 25), fr(9, 10), fr(9, 25), fr(10, 9), fr(10, 25), fr(2, 5)))
    # 10 left to right
    item("%s − %s + %s" % (fr(7, 8), fr(1, 4), fr(1, 2)), F(7, 8) - q4 + h,
         [F(7, 8) - (q4 + h), F(7, 8) + q4 + h, F(7, 8) - q4],
         "+ and − have the same rank, so work from left to right. %s − %s = %s − %s = %s. "
         "Then %s + %s = %s + %s = %s = <b>1 %s</b>."
         % (fr(7, 8), fr(1, 4), fr(7, 8), fr(2, 8), fr(5, 8), fr(5, 8), fr(1, 2), fr(5, 8), fr(4, 8), fr(9, 8),
            fr(1, 8)))
    # 11
    item("4 %s − 2 %s × 1 %s" % (fr(1, 2), fr(1, 4), fr(1, 3)), F(9, 2) - F(9, 4) * F(4, 3),
         [(F(9, 2) - F(9, 4)) * F(4, 3), F(9, 2) - (2 + q4 * t), F(9, 2) - F(9, 4) / F(4, 3)],
         "Multiply first: 2 %s × 1 %s = %s × %s. The 4s cancel, and 9 and 3 share 3, so the product is 3. "
         "Then 4 %s − 3 = <b>1 %s</b>." % (fr(1, 4), fr(1, 3), fr(9, 4), fr(4, 3), fr(1, 2), fr(1, 2)))
    # 12
    item("%s × %s + %s ÷ %s" % (fr(2, 3), fr(3, 8), fr(3, 4), fr(1, 2)), F(2, 3) * F(3, 8) + F(3, 4) / h,
         [F(2, 3) * F(3, 8) + F(3, 4) * h, (F(2, 3) * F(3, 8) + F(3, 4)) / h, F(2, 3) * F(3, 8) + h / F(3, 4)],
         "Multiply and divide first: %s × %s = %s = %s, and %s ÷ %s = %s × 2 = %s. "
         "Then %s + %s = %s = <b>1 %s</b>."
         % (fr(2, 3), fr(3, 8), fr(6, 24), fr(1, 4), fr(3, 4), fr(1, 2), fr(3, 4), fr(6, 4), fr(1, 4), fr(6, 4),
            fr(7, 4), fr(3, 4)))
    # 13
    item("(1 − %s) × (1 + %s)" % (fr(3, 8), fr(1, 5)), (1 - F(3, 8)) * (1 + F(1, 5)),
         [(1 - F(3, 8)) + (1 + F(1, 5)), 1 - F(3, 8) * 1 + F(1, 5), (1 - F(3, 8)) / (1 + F(1, 5))],
         "Brackets first: 1 − %s = %s and 1 + %s = %s. Then %s × %s = %s = <b>%s</b>."
         % (fr(3, 8), fr(5, 8), fr(1, 5), fr(6, 5), fr(5, 8), fr(6, 5), fr(30, 40), fr(3, 4)))
    # 14
    item("%s ÷ (%s − %s)" % (fr(2, 3), fr(1, 2), fr(1, 6)), F(2, 3) / (h - F(1, 6)),
         [F(2, 3) / h - F(1, 6), F(2, 3) * (h - F(1, 6)), (h - F(1, 6)) / F(2, 3)],
         "Brackets first: %s − %s = %s − %s = %s = %s. Then %s ÷ %s = %s × 3 = <b>2</b>."
         % (fr(1, 2), fr(1, 6), fr(3, 6), fr(1, 6), fr(2, 6), fr(1, 3), fr(2, 3), fr(1, 3), fr(2, 3)))
    # 15
    item("%s ÷ %s − %s" % (fr(5, 9), fr(5, 6), fr(1, 3)), F(5, 9) / F(5, 6) - t,
         [F(5, 6) / F(5, 9) - t, F(5, 9) * F(5, 6) - t, F(5, 9) / (F(5, 6) - t)],
         "Divide first: %s ÷ %s = %s × %s. The 5s cancel: %s = %s. Then %s − %s = <b>%s</b>."
         % (fr(5, 9), fr(5, 6), fr(5, 9), fr(6, 5), fr(6, 9), fr(2, 3), fr(2, 3), fr(1, 3), fr(1, 3)))
    # 16
    item("%s + %s ÷ %s" % (fr(1, 2), fr(2, 5), fr(4, 5)), h + F(2, 5) / F(4, 5),
         [(h + F(2, 5)) / F(4, 5), h + F(2, 5) * F(4, 5), h + F(4, 5) / F(2, 5)],
         "Divide first: %s ÷ %s = %s × %s = %s = %s. Then %s + %s = <b>1</b>."
         % (fr(2, 5), fr(4, 5), fr(2, 5), fr(5, 4), fr(10, 20), fr(1, 2), fr(1, 2), fr(1, 2)))
    # 17
    item("2 %s ÷ %s − 1 %s" % (fr(1, 2), fr(5, 6), fr(1, 3)), F(5, 2) / F(5, 6) - F(4, 3),
         [F(5, 2) * F(5, 6) - F(4, 3), F(5, 2) / F(5, 6) + F(4, 3), F(3, 2) / F(5, 6) - F(2, 3)],
         "Divide first: 2 %s ÷ %s = %s × %s = %s = 3. Then 3 − 1 %s = <b>1 %s</b>."
         % (fr(1, 2), fr(5, 6), fr(5, 2), fr(6, 5), fr(30, 10), fr(1, 3), fr(2, 3)))
    # 18 substitution
    a, b = F(5, 6), F(2, 3)
    its.append(mcq("Evaluate 4<i>a</i> − <i>b</i> when <i>a</i> = %s and <i>b</i> = %s." % (fr(5, 6), fr(2, 3)),
                   S(4 * a - b), Ss([4 + a - b, 4 * (a - b), F(20, 24) - b]),
                   "4<i>a</i> means 4 × <i>a</i>: 4 × %s = %s = %s. Then %s − %s = %s = <b>2 %s</b>. "
                   "(4<i>a</i> is not 4 %s.)" % (fr(5, 6), fr(20, 6), fr(10, 3), fr(10, 3), fr(2, 3), fr(8, 3),
                                               fr(2, 3), fr(5, 6))))
    # 19 substitution
    x = F(3, 4)
    its.append(mcq("Evaluate <i>x</i>² + <i>x</i> when <i>x</i> = %s." % fr(3, 4),
                   S(x ** 2 + x), Ss([2 * x + x, F(9, 4) + x, F(6, 8) + x]),
                   "<i>x</i>² = (%s)² = %s. Then %s + %s = %s + %s = %s = <b>1 %s</b>. "
                   "(<i>x</i>² means <i>x</i> × <i>x</i>, not 2 × <i>x</i>.)"
                   % (fr(3, 4), fr(9, 16), fr(9, 16), fr(3, 4), fr(9, 16), fr(12, 16), fr(21, 16), fr(5, 16))))
    # 20 error analysis
    nm, he, his = P.next()
    q = "%s says %s − %s × 2 = 1. What did %s do wrong?" % (nm, fr(3, 4), fr(1, 4), he)
    its.append(mcq(q, ("%s subtracted before multiplying." % cap(he), None),
                   [("%s multiplied 2 by both 1 and 4." % cap(he), None),
                    ("%s forgot to simplify." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "(%s − %s) × 2 = %s × 2 = 1, so %s subtracted first. BEDMAS says multiply first: "
                   "%s × 2 = %s, then %s − %s = %s. <b>%s subtracted before multiplying</b>."
                   % (fr(3, 4), fr(1, 4), fr(1, 2), nm, fr(1, 4), fr(1, 2), fr(3, 4), fr(1, 2), fr(1, 4), cap(he))))
    assert len(its) == 20, len(its)
    return {"title": "Order of operations with fractions", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    MO = ["parts", "add", "addfr", "cross", "badimp", "addden"]
    DO = ["nf", "first", "leftover", "parts", "fracflip", "badimp", "drop", "both"]

    def wm(q, x, y, one, many=None, lead=""):
        x, y = F(x), F(y)
        v = x * y
        its.append(mcq(q, (qty(v, one, many), v), Q(mwr(x, y, MO) + [x / y], one, many),
                       mul_e(x, y, unit=(one if v <= 1 else (many or one)), lead=lead)))

    def wd(q, x, y, one, many=None, lead=""):
        x, y = F(x), F(y)
        v = x / y
        its.append(mcq(q, (qty(v, one, many), v), Q(dwr(x, y, DO), one, many),
                       div_e(x, y, unit=(one if v <= 1 else (many or one)), lead=lead)))

    # 1 Nanaimo bars
    nm, he, his = P.next()
    wm("A pan of Nanaimo bars needs %s cup of butter. %s makes %s of the recipe. How much butter does %s need?"
       % (fr(3, 4), nm, fr(1, 2), he), F(1, 2), F(3, 4), "cup", "cups",
       "%s of %s means %s × %s. " % (fr(1, 2), fr(3, 4), fr(1, 2), fr(3, 4)))
    # 2 pancakes
    nm, he, his = P.next()
    wm("One batch of pancakes needs %s cup of milk. %s makes 2 %s batches for a ski trip breakfast. "
       "How much milk does %s need?" % (fr(2, 3), nm, fr(1, 2), he), F(5, 2), F(2, 3), "cup", "cups",
       "2 %s batches of %s cup: multiply. " % (fr(1, 2), fr(2, 3)))
    # 3 seawall
    nm, he, his = P.next()
    wm("%s’s walk along the Stanley Park seawall is 4 %s km long. %s has walked %s of it. How far has %s walked?"
       % (nm, fr(1, 2), cap(he), fr(2, 3), he), F(2, 3), F(9, 2), "km", None,
       "%s of 4 %s km means %s × 4 %s. " % (fr(2, 3), fr(1, 2), fr(2, 3), fr(1, 2)))
    # 4 hiking rate
    nm, he, his = P.next()
    wd("On a trail near Squamish, %s hikes 3 %s km in 1 %s h. At this rate, how far does %s hike in 1 h?"
       % (nm, fr(3, 4), fr(1, 4), he), F(15, 4), F(5, 4), "km", None, "Divide the distance by the time. ")
    # 5 Terry Fox Run banners
    nm, he, his = P.next()
    wd("%s has 2 %s m of fabric to make banners for the school’s Terry Fox Run. Each banner needs %s m. "
       "How many banners can %s make?" % (nm, fr(1, 4), fr(3, 4), he), F(9, 4), F(3, 4), "banner", "banners",
       "How many %s m pieces fit in 2 %s m? Divide. " % (fr(3, 4), fr(1, 4)))
    # 6 salmon
    wd("A family buys 1 %s kg of fresh salmon in Steveston. They cut it into portions of %s kg. "
       "How many portions do they get?" % (fr(1, 2), fr(3, 16)), F(3, 2), F(3, 16), "portion", "portions",
       "How many %s kg portions fit in 1 %s kg? Divide. " % (fr(3, 16), fr(1, 2)))
    # 7 cedar board
    nm, he, his = P.next()
    wd("%s is building a planter box. A cedar board is 2 %s m long, and %s cuts it into pieces that are each %s m long. "
       "How many pieces does %s get?" % (nm, fr(2, 3), he, fr(2, 3), he), F(8, 3), F(2, 3), "piece", "pieces",
       "How many %s m pieces fit in 2 %s m? Divide. " % (fr(2, 3), fr(2, 3)))
    # 8 garden bed area
    wm("A rectangular garden bed is 2 %s m long and 1 %s m wide. What is its area?" % (fr(1, 2), fr(3, 5)),
       F(5, 2), F(8, 5), "m²", None, "Area = length × width. ")
    # 9 ferry
    nm, he, his = P.next()
    wm("A BC Ferries trip from Tsawwassen to Swartz Bay takes about 1 %s h. %s reads for %s of the trip. "
       "For how long does %s read?" % (fr(1, 2), nm, fr(2, 3), he), F(2, 3), F(3, 2), "h", None,
       "%s of 1 %s h means %s × 1 %s. " % (fr(2, 3), fr(1, 2), fr(2, 3), fr(1, 2)))
    # 10 juice
    wd("A jug holds 1 %s L of apple juice from the Okanagan. Each cup holds %s L. How many cups can be filled?"
       % (fr(3, 4), fr(1, 4)), F(7, 4), F(1, 4), "cup", "cups",
       "How many %s L cups fit in 1 %s L? Divide. " % (fr(1, 4), fr(3, 4)))
    # 11 paint
    nm, he, his = P.next()
    wd("%s uses %s of a can of stain to stain %s of a fence. How much stain does %s need for the whole fence?"
       % (nm, fr(2, 3), fr(4, 5), he), F(2, 3), F(4, 5), "of a can", "cans",
       "Stain for the whole fence = stain used ÷ fraction of the fence stained. ")
    # 12 field trip
    wm("%s of the Grade 8 students go on a field trip to Victoria. %s of those students visit the Royal BC Museum. "
       "What fraction of the Grade 8 students visit the museum?" % (fr(3, 5), fr(2, 3)), F(2, 3), F(3, 5),
       "of the students", None, "%s of %s means %s × %s. " % (fr(2, 3), fr(3, 5), fr(2, 3), fr(3, 5)))
    # 13 rain
    x, y = F(9, 2), F(6)
    its.append(mcq("In Vancouver, 4 %s cm of rain fell over 6 days, the same amount each day. "
                   "How much rain fell each day?" % fr(1, 2),
                   (qty(x / y, "cm"), x / y), Q([x * y, y / x, F(4, 6) + F(1, 2), F(1, 2) / 6], "cm"),
                   "Share 4 %s cm equally over 6 days: 4 %s ÷ 6. Write 4 %s as %s and flip 6 to %s. "
                   "%s × %s = %s = <b>%s cm</b>. Check: 6 × %s = %s = 4 %s."
                   % (fr(1, 2), fr(1, 2), fr(1, 2), fr(9, 2), fr(1, 6), fr(9, 2), fr(1, 6), fr(9, 12), fr(3, 4),
                      fr(3, 4), fr(18, 4), fr(1, 2))))
    # 14 full batches
    nm, he, his = P.next()
    x, y = F(7, 2), F(3, 4)
    q = ("%s has 3 %s cups of flour. One batch of oatmeal cookies needs %s cup. How many <b>full</b> batches "
         "can %s make?" % (nm, fr(1, 2), fr(3, 4), he))
    its.append(mcq(q, ("4 batches", F(4)),
                   [("5 batches", F(5)), ("%s batches" % show(x / y), x / y), ("%s batches" % show(x * y), x * y)],
                   div_e(x, y) + " Only full batches count, so %s can make <b>4 batches</b>." % he))
    # 15 which expression
    q = ("A rope is 4 %s m long. It is cut into pieces that are each %s m long. Which expression gives the number of "
         "pieces?" % (fr(1, 2), fr(3, 8)))
    its.append(mcq(q, ("4 %s ÷ %s" % (fr(1, 2), fr(3, 8)), None),
                   [("4 %s × %s" % (fr(1, 2), fr(3, 8)), None), ("%s ÷ 4 %s" % (fr(3, 8), fr(1, 2)), None),
                    ("4 %s − %s" % (fr(1, 2), fr(3, 8)), None)],
                   "The question asks how many %s m pieces fit in 4 %s m, so divide by %s: <b>4 %s ÷ %s</b> = "
                   "%s × %s = 12 pieces." % (fr(3, 8), fr(1, 2), fr(3, 8), fr(1, 2), fr(3, 8), fr(9, 2), fr(8, 3))))
    # 16 reverse: whole route
    nm, he, his = P.next()
    wd("%s has paddled a canoe 2 %s km. That is %s of the route around a lake. How long is the whole route?"
       % (nm, fr(1, 4), fr(3, 4)), F(9, 4), F(3, 4), "km", None,
       "%s of the route is 2 %s km, so the whole route is 2 %s ÷ %s. " % (fr(3, 4), fr(1, 4), fr(1, 4), fr(3, 4)))
    # 17 two steps with BEDMAS: rope left
    nm, he, his = P.next()
    its.append(mcq("%s has 5 m of rope. %s cuts 3 pieces that are each 1 %s m long. How much rope is left?"
                   % (nm, cap(he), fr(1, 4)),
                   (qty(F(5, 4), "m"), F(5, 4)),
                   Q([(5 - 3) * F(5, 4), 5 - F(13, 4), 3 * F(5, 4)], "m"),
                   "Rope left = 5 − 3 × 1 %s. Multiply first: 3 × 1 %s = 3 × %s = %s = 3 %s m. "
                   "Then 5 − 3 %s = <b>1 %s m</b>." % (fr(1, 4), fr(1, 4), fr(5, 4), fr(15, 4), fr(3, 4), fr(3, 4),
                                                      fr(1, 4))))
    # 18 recipe scaling (two steps)
    nm, he, his = P.next()
    its.append(mcq("A recipe for 24 muffins uses 2 %s cups of flour. %s wants to make 16 muffins. "
                   "How much flour does %s need?" % (fr(1, 4), nm, he),
                   (qty(F(3, 2), "cup", "cups"), F(3, 2)),
                   Q([F(9, 4) * F(3, 2), F(9, 4) - F(1, 3), F(2) * F(2, 3) + F(1, 4)], "cup", "cups"),
                   "16 muffins is %s = %s of the recipe. %s × 2 %s = %s × %s. The 3s cancel, and 2 and 4 share 2: "
                   "%s = <b>1 %s cups</b>."
                   % (fr(16, 24), fr(2, 3), fr(2, 3), fr(1, 4), fr(2, 3), fr(9, 4), fr(3, 2), fr(1, 2))))
    # 19 pizzas
    x, y = F(12), F(3, 8)
    its.append(mcq("A school orders 12 pizzas for a Grade 8 year-end party. Each student eats %s of a pizza. "
                   "How many students can be served?" % fr(3, 8),
                   ("32 students", F(32)),
                   [("%s students" % show(x * y), x * y), ("4 students", F(4)), ("96 students", F(96))],
                   "How many %s fit in 12? Divide: 12 ÷ %s = 12 × %s = %s = <b>32 students</b>. "
                   "Check: 32 × %s = %s = 12." % (fr(3, 8), fr(3, 8), fr(8, 3), fr(96, 3), fr(3, 8), fr(96, 8))))
    # 20 savings (two steps)
    nm, he, his = P.next()
    its.append(mcq("%s spends %s of %s savings on a skateboard. Then %s spends %s of the rest on a helmet. "
                   "What fraction of %s savings does %s spend on the helmet?" % (nm, fr(2, 5), his, he, fr(1, 2), his, he),
                   (qty(F(3, 10), "of the savings"), F(3, 10)),
                   Q([F(1, 2) * F(2, 5), F(2, 5) + F(1, 2), F(1, 2)], "of the savings"),
                   "The rest is 1 − %s = %s of the savings. %s of %s is %s × %s = <b>%s of the savings</b>."
                   % (fr(2, 5), fr(3, 5), fr(1, 2), fr(3, 5), fr(1, 2), fr(3, 5), fr(3, 10))))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, trails and BC trips", "items": its}


# ============================================================ lesson
def body_html():
    area_fig = ("<figure class='sn-fig'>" + area_svg(3, 4, 2, 3) +
                "<figcaption>" + mul(F(2, 3), F(3, 4)) + ": the light columns are " + fr(3, 4) + " of the square. "
                "The dark part is " + fr(2, 3) + " of them: 6 of 12 small rectangles, so " + fr(6, 12) + " = "
                + fr(1, 2) + ".</figcaption></figure>")
    bar_fig = ("<figure class='sn-fig'>" + groups_svg(F(5, 6), F(1, 3), PW=36) +
               "<figcaption>" + dv(F(5, 6), F(1, 3)) + ": " + fr(1, 3) + " = " + fr(2, 6) + ". 2 full groups fit, and the "
               "1 sixth left over is half a group, so the answer is 2 " + fr(1, 2) + ".</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p><b>× a fraction means “of”.</b> " + mul(F(2, 3), F(3, 4)) + " means " + fr(2, 3) + " of " + fr(3, 4) + ". "
        "<b>÷ a fraction asks “how many fit?”</b> " + dv(F(5, 6), F(1, 3)) + " asks how many thirds fit in "
        + fr(5, 6) + ".</p>"
        "<h2>Multiply fractions</h2>"
        "<p>Multiply the numerators. Multiply the denominators. Then simplify. "
        "The area model shows why: the square is cut into 3 × 4 = 12 small rectangles.</p>"
        + area_fig
        + ex("Example 1", mul(F(5, 8), F(4, 15)) + " = ?",
             "Simplify first. 5 and 15 share 5: they become 1 and 3. 4 and 8 share 4: they become 1 and 2. "
             "Now " + mul(F(1, 2), F(1, 3)) + " = " + fr(1, 6) + ".", fr(1, 6))
        + "<p>Change mixed numbers to improper fractions first.</p>"
        + ex("Example 2", "2 " + fr(1, 2) + " × 1 " + fr(1, 5) + " = ?",
             "Write 2 " + fr(1, 2) + " as " + fr(5, 2) + " and 1 " + fr(1, 5) + " as " + fr(6, 5) + ". "
             + fr(5, 2) + " × " + fr(6, 5) + " = " + fr(30, 10) + " = 3.", "3")
        + "<h2>Divide fractions</h2>"
        "<p>Count how many groups fit, or use the rule: <b>keep</b> the first fraction, <b>change</b> ÷ to ×, "
        "and <b>flip</b> the second fraction (use its reciprocal). Flip only the number you divide by.</p>"
        + bar_fig
        + ex("Example 3", "3 " + fr(3, 4) + " ÷ " + fr(5, 6) + " = ?",
             "Write 3 " + fr(3, 4) + " as " + fr(15, 4) + ". Keep " + fr(15, 4) + ", flip " + fr(5, 6) + " to "
             + fr(6, 5) + ": " + fr(15, 4) + " × " + fr(6, 5) + " = " + fr(90, 20) + " = 4 " + fr(1, 2)
             + ". Check: 4 " + fr(1, 2) + " × " + fr(5, 6) + " = " + fr(9, 2) + " × " + fr(5, 6) + " = " + fr(45, 12)
             + " = 3 " + fr(3, 4) + ".", "4 " + fr(1, 2))
        + "<h2>Order of operations (BEDMAS)</h2>"
        "<p>Fractions follow the same order as whole numbers: brackets, exponents, then × and ÷ from left to right, "
        "then + and − from left to right.</p>"
        + ex("Example 4", fr(1, 3) + " + " + fr(1, 2) + " × " + fr(4, 5) + " = ?",
             "Multiply first: " + mul(F(1, 2), F(4, 5)) + " = " + fr(2, 5) + ". Then " + fr(1, 3) + " + " + fr(2, 5)
             + " = " + fr(5, 15) + " + " + fr(6, 15) + " = " + fr(11, 15) + ".", fr(11, 15))
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [dv(F(3, 4), F(3, 8)) + " = " + fr(4, 3) + " × " + fr(3, 8) + " (flipping the wrong fraction)",
             "Keep the first fraction. Flip only the divisor: " + fr(3, 4) + " × " + fr(8, 3) + " = 2."],
            [mul(F(2, 3), F(4, 5)) + " = " + fr(6, 8) + " (adding across)",
             "Multiply across: " + fr("2 × 4", "3 × 5") + " = " + fr(8, 15) + "."],
            ["2 " + fr(1, 2) + " × 3 " + fr(1, 3) + " = 6 " + fr(1, 6)
             + " (multiplying the whole parts and the fraction parts separately)",
             "Change to improper fractions first: " + fr(5, 2) + " × " + fr(10, 3) + " = " + fr(25, 3) + " = 8 "
             + fr(1, 3) + "."],
            [fr(1, 3) + " + " + fr(1, 2) + " × " + fr(4, 5) + " = " + fr(5, 6) + " × " + fr(4, 5)
             + " (adding first)", "Multiply before you add: the answer is " + fr(11, 15) + "."],
        ])
    )


FAQ = [
    {"q": "How do you multiply fractions and mixed numbers in Grade 8?",
     "a": "Change any mixed numbers to improper fractions, multiply the numerators, multiply the denominators, then simplify. For example, 2 1/2 × 1 1/5 = 5/2 × 6/5 = 30/10 = 3."},
    {"q": "When you divide fractions, which fraction do you flip?",
     "a": "Flip only the second fraction, the one you divide by. Keep the first fraction, change ÷ to ×, and multiply by the reciprocal: 3/4 ÷ 3/8 = 3/4 × 8/3 = 2."},
    {"q": "Does BEDMAS work with fractions?",
     "a": "Yes. Do brackets, then exponents, then × and ÷ from left to right, then + and − from left to right. For example, 1/3 + 1/2 × 4/5 = 1/3 + 2/5 = 11/15."},
    {"q": "When do BC students learn to multiply and divide fractions?",
     "a": "In Grade 8. The BC Grade 8 math curriculum lists operations with fractions, including multiplication, division and order of operations, under Computational fluency. In Grade 9 these operations are extended to rational numbers, including negative fractions."},
]


def gen():
    rnd = random.Random(58805)
    P = People(rnd)
    sets = [set_multiply(P), set_mixed(P), set_divide(P), set_bedmas(P), set_words(P)]
    # every explanation shows the correct numeric choice
    for s in sets:
        for it in s["items"]:
            if it.pop("_num"):
                assert ("<b>%s</b>" % it["c"][0]) in it["e"] or ("<b>%s." % it["c"][0]) in it["e"], (it["q"], it["e"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "multiplying-and-dividing-fractions",
        "sort": 5, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Multiplying and Dividing Fractions",
        "seo_title": "Grade 8 Multiplying and Dividing Fractions Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Multiplying and Dividing Fractions",
        "domain": "Computational fluency",
        "standard_code": "Grade 8: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Operations with fractions (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 8 math worksheets on multiplying and dividing fractions, matched to the BC curriculum: "
                     "area models, simplifying first, mixed numbers, dividing by the reciprocal, order of operations "
                     "(BEDMAS) and word problems. 100 questions with an answer key.",
        "key_big": "To multiply fractions, multiply the numerators and the denominators. To divide, flip only the "
                   "fraction you divide by and multiply.",
        "key_sub": "3/4 ÷ 3/8 = 3/4 × 8/3 = 2, not 4/3 × 3/8. Change mixed numbers to improper fractions first, "
                   "and follow BEDMAS: × and ÷ before + and −.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "fraction bar")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
