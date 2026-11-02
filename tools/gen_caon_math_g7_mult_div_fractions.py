# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Multiplying and Dividing Fractions (Ontario Mathematics Curriculum 2020, B2.8)
  python3 tools/gen_caon_math_g7_mult_div_fractions.py
Grade 7 multiplies and divides FRACTIONS BY FRACTIONS:
  fraction × fraction with area models, simplifying before multiplying, fraction ÷ fraction
  (how many fit, multiply by the reciprocal), mixed numbers, word problems.
Answers are in simplest form (mixed numbers when greater than 1).
Every answer is checked with fractions.Fraction; no two choices are equal in value.
Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
G1 = "#4fae74"        # group colour 1 / dark part
G2 = "#a6dbb7"        # group colour 2
LIGHT = "#d7ecdf"     # light part of an area model
DARKLINE = "#1f6b3e"
PART = "#f3c9c4"      # partial group
LINE = "#2b2b2b"
GRAY = "#8a8178"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
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
    """Plain-text form for SVG labels and plain fields: 3/4, 1 1/2."""
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
    return {"q": q, "c": ch, "a": 0, "e": e}


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
    s += "Keep %s, change ÷ to ×, and flip %s to %s. " % (imp(x), imp(y), imp(1 / y))
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
    """x × y: (value) list from real mistakes."""
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
        elif k == "div":                    # flipped one fraction (divided)
            out.append(x / y)
        elif k == "sameden":                # kept the denominator, as when adding
            if b == d:
                out.append(F(a * c, b))
        elif k == "parts":                  # multiplied the whole parts and the fraction parts
            (w1, f1), (w2, f2) = split(x), split(y)
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


# ============================================================ set 1: area models
def set_area():
    its = []
    # A) which multiplication does the model show
    for a1, b1, a2, b2 in [(3, 4, 1, 3), (2, 3, 1, 4), (4, 5, 2, 3), (1, 3, 3, 4), (3, 5, 3, 4)]:
        q = (fig(area_svg(a1, b1, a2, b2)) + "The square is 1 whole. The light columns are %s of the square. "
             "The dark part is a part of the light columns. Which multiplication does the dark part show?" % fr(a1, b1))
        right = "%s × %s" % (fr(a2, b2), fr(a1, b1))
        cands = [("%s × %s" % (fr(b2 - a2, b2), fr(a1, b1)), F(b2 - a2, b2) * F(a1, b1)),   # counted the rows that are not dark
                 ("%s + %s" % (fr(a2, b2), fr(a1, b1)), F(a2, b2) + F(a1, b1)),             # added
                 ("%s × %s" % (fr(a2, b2), fr(b1 - a1, b1)), F(a2, b2) * F(b1 - a1, b1))]   # counted the white columns
        e = ("The light part is %d of %d columns: %s of the square. The dark part is %d of the %d rows of the light part: "
             "%s of it. So the dark part is %s of %s, which is <b>%s</b> = %s." %
             (a1, b1, fr(a1, b1), a2, b2, fr(a2, b2), fr(a2, b2), fr(a1, b1), right, show(F(a1 * a2, b1 * b2))))
        its.append(mcq(q, (right, F(a2, b2) * F(a1, b1)), cands, e))
    # B) what fraction of the square is dark
    for a1, b1, a2, b2 in [(3, 4, 1, 2), (2, 3, 2, 5), (3, 5, 1, 2), (5, 6, 1, 2), (2, 3, 1, 3), (3, 4, 3, 5), (4, 5, 2, 3)]:
        n, d = a1 * a2, b1 * b2
        v = F(n, d)
        q = (fig(area_svg(a1, b1, a2, b2)) + "The model shows %s × %s. What fraction of the whole square is dark? "
             "Give the answer in simplest form." % (fr(a2, b2), fr(a1, b1)))
        cands = Ss([F(n, d - n), F(n, a1 * b2), F(a1 + a2, b1 + b2), F(a1, b1), F(a2, b2)])
        e = ("The square is cut into %d × %d = %d equal small rectangles. %d × %d = %d of them are dark. "
             "So %s × %s = %s" % (b1, b2, d, a1, a2, n, fr(a2, b2), fr(a1, b1), fr(n, d)))
        e += (" = <b>%s</b>." % show(v)) if gcd(n, d) > 1 else ". The answer is <b>%s</b>." % show(v)
        its.append(mcq(q, S(v), cands, e))
    # C) multiply without a model
    for (a, b), (c, d), order in [((1, 2), (3, 5), ["addfr", "cross", "add", "addden"]),
                                  ((2, 3), (4, 5), ["cross", "addfr", "addden", "add"]),
                                  ((3, 4), (1, 5), ["addfr", "addden", "cross", "add"]),
                                  ((1, 3), (2, 7), ["add", "addfr", "cross", "addden"]),
                                  ((5, 6), (1, 2), ["addfr", "cross", "addden", "add"]),
                                  ((3, 5), (2, 7), ["cross", "addfr", "add", "addden"]),
                                  ((2, 5), (3, 5), ["sameden", "addfr", "cross", "add"]),
                                  ((3, 8), (5, 7), ["addfr", "add", "cross", "addden"])]:
        x, y = F(a, b), F(c, d)
        q = "%s = <b>?</b>" % mul(x, y)
        its.append(mcq(q, S(x * y), Ss(mwr(x, y, order)), mul_e(x, y, cancel=False)))
    assert len(its) == 20, len(its)
    return {"title": "Fraction × fraction with area models", "items": its}


# ============================================================ set 2: simplify before multiplying
def set_simplify(P):
    its = []
    # A) the simplifying step
    q = "Simplify before you multiply: %s. Which is correct after simplifying?" % mul(F(4, 9), F(3, 8))
    its.append(mcq(q, ("%s × %s" % (fr(1, 3), fr(1, 2)), F(1, 6)),
                   [("%s × %s" % (fr(1, 3), fr(3, 2)), F(1, 2)), ("%s × %s" % (fr(1, 3), fr(1, 8)), F(1, 24)),
                    ("%s × %s" % (fr(4, 3), fr(1, 2)), F(2, 3))],
                   "Pair each numerator with a denominator. 4 and 8 share 4: they become 1 and 2. 3 and 9 share 3: they become "
                   "1 and 3. So %s × %s becomes <b>%s × %s</b> = %s. Each time, divide <b>both</b> numbers of the pair."
                   % (fr(4, 9), fr(3, 8), fr(1, 3), fr(1, 2), fr(1, 6))))
    nm, he, his = P.next()
    q = ("%s simplifies %s by dividing 6 and 9 by 3 before multiplying. What is wrong?" % (nm, mul(F(6, 7), F(9, 10))))
    its.append(mcq(q, ("6 and 9 are both numerators. Divide a numerator and a denominator.", None),
                   [("Nothing. You can divide any two numbers.", None),
                    ("%s should divide 6 and 9 by 9." % cap(he), None),
                    ("You can never simplify before multiplying.", None)],
                   "Dividing two numerators changes the value. Pair a numerator with a denominator: 6 and 10 share 2. "
                   "Then %s × %s = %s. <b>6 and 9 are both numerators</b>, so %s cannot divide them both."
                   % (fr(3, 7), fr(9, 5), fr(27, 35), he)))
    # B) calculate, simplifying first
    cases = [((4, 9), (3, 8)), ((5, 6), (3, 10)), ((2, 3), (9, 14)), ((7, 12), (4, 21)), ((3, 4), (8, 9)),
             ((6, 7), (14, 15)), ((9, 10), (5, 12)), ((8, 15), (5, 12)), ((10, 21), (7, 25)), ((12, 25), (15, 16)),
             ((4, 7), (21, 8)), ((9, 4), (8, 15)), ((5, 12), (6, 5)), ((15, 8), (4, 9))]
    orders = [["addfr", "cross", "add", "div"], ["cross", "addfr", "div", "add"], ["addfr", "div", "cross", "add"],
              ["div", "addfr", "add", "cross"]]
    for i, ((a, b), (c, d)) in enumerate(cases):
        x, y = F(a, b), F(c, d)
        v = x * y
        q = "%s = <b>?</b>" % ("%s × %s" % (fr(a, b), fr(c, d)))
        if v > 1:
            q += "<br>Give your answer as a mixed number."
        its.append(mcq(q, S(v), Ss(mwr(x, y, orders[i % 4] + ["addden"])), mul_e(x, y, convert=False)))
    # C) three fractions, a missing factor, an estimate
    x, y, z = F(2, 3), F(3, 4), F(4, 5)
    q = "%s × %s × %s = <b>?</b>" % (fr(2, 3), fr(3, 4), fr(4, 5))
    its.append(mcq(q, S(x * y * z), Ss([F(9, 12), x * y, x + y + z, F(2 * 3 * 4, 3 + 4 + 5)]),
                   "Simplify first: the 3s and the 4s cancel. %s = %s = <b>%s</b>."
                   % (fr("2 × 3 × 4", "3 × 4 × 5"), fr(24, 60), fr(2, 5))))
    x, y, z = F(5, 6), F(3, 10), F(4, 9)
    q = "%s × %s × %s = <b>?</b>" % (fr(5, 6), fr(3, 10), fr(4, 9))
    its.append(mcq(q, S(x * y * z), Ss([x * y, F(12, 25), F(5 + 3 + 4, 6 * 10 * 9), F(1, 6)]),
                   "Multiply all the numerators and all the denominators: %s = %s. Simplify: 60 ÷ 60 = 1 and 540 ÷ 60 = 9, "
                   "so the answer is <b>%s</b>." % (fr("5 × 3 × 4", "6 × 10 × 9"), fr(60, 540), fr(1, 9))))
    q = "%s × <b>?</b> = %s" % (fr(2, 3), fr(1, 2))
    its.append(mcq(q, S(F(3, 4)), Ss([F(1, 3), F(4, 3), F(1, 6), F(1, 4)]),
                   "Divide: %s ÷ %s = %s × %s = <b>%s</b>. Check: %s × %s = %s = %s."
                   % (fr(1, 2), fr(2, 3), fr(1, 2), fr(3, 2), fr(3, 4), fr(2, 3), fr(3, 4), fr(6, 12), fr(1, 2))))
    q = "Without calculating, which product is <b>less</b> than %s?" % fr(5, 6)
    its.append(mcq(q, (mul(F(5, 6), F(3, 4)), None),
                   [(mul(F(5, 6), F(4, 3)), None), (mul(F(5, 6), F(3, 2)), None), ("%s × 1" % fr(5, 6), None)],
                   "Multiplying by a fraction less than 1 gives less than you started with. %s is less than 1, so "
                   "<b>%s</b> is less than %s. %s × 1 = %s, and %s and %s are greater than 1."
                   % (fr(3, 4), mul(F(5, 6), F(3, 4)), fr(5, 6), fr(5, 6), fr(5, 6), fr(4, 3), fr(3, 2))))
    assert len(its) == 20, len(its)
    return {"title": "Simplify before you multiply", "items": its}


# ============================================================ set 3: fraction ÷ fraction
def set_divide(P):
    its = []
    # A) fraction bars: how many fit
    for a, b in [(F(3, 4), F(1, 8)), (F(2, 3), F(1, 6)), (F(4, 5), F(2, 5)), (F(5, 6), F(1, 3)), (F(7, 8), F(1, 4))]:
        q = (fig(groups_svg(a, b)) + "The bar shows %s. How many groups of %s fit in %s? %s = <b>?</b>"
             % (show(a), show(b), show(a), dv(a, b)))
        its.append(mcq(q, S(a / b), Ss(dwr(a, b, ["nf", "leftover", "first", "drop", "both"])), e_groups(a, b)))
    # B) reciprocals
    q = "What is the reciprocal of %s?" % fr(3, 5)
    its.append(mcq(q, (fr(5, 3), None), [(fr(3, 5), None), ("−" + fr(3, 5), None), (fr(2, 5), None)],
                   "Flip the fraction: the reciprocal of %s is <b>%s</b>. Check: %s × %s = %s = 1. "
                   "(−%s is the opposite, not the reciprocal.)" % (fr(3, 5), fr(5, 3), fr(3, 5), fr(5, 3), fr(15, 15), fr(3, 5))))
    q = "What is the reciprocal of %s?" % show(F(9, 4))
    its.append(mcq(q, (fr(4, 9), None), [(fr(9, 4), None), ("6", None), (fr(4, 3), None)],
                   "First write %s as a fraction: %s. Then flip it: <b>%s</b>. Check: %s × %s = 1."
                   % (show(F(9, 4)), fr(9, 4), fr(4, 9), fr(9, 4), fr(4, 9))))
    # C) rewrite as multiplication
    for (a, b, c, d) in [(2, 3, 4, 5), (5, 8, 1, 4)]:
        q = "Which multiplication has the same answer as %s ÷ %s?" % (fr(a, b), fr(c, d))
        right = "%s × %s" % (fr(a, b), fr(d, c))
        cands = [("%s × %s" % (fr(b, a), fr(c, d)), F(b, a) * F(c, d)),
                 ("%s × %s" % (fr(b, a), fr(d, c)), F(b, a) * F(d, c)),
                 ("%s × %s" % (fr(a, b), fr(c, d)), F(a, b) * F(c, d))]
        e = ("Keep the first fraction, change ÷ to ×, and flip only the second fraction: <b>%s</b>. "
             "Do not flip %s." % (right, fr(a, b)))
        its.append(mcq(q, (right, F(a, b) * F(d, c)), cands, e))
    # D) calculate
    for a, b in [(F(3, 4), F(1, 2)), (F(2, 5), F(3, 4)), (F(5, 6), F(2, 3)), (F(3, 8), F(3, 4)), (F(4, 7), F(2, 3)),
                 (F(9, 10), F(3, 4)), (F(1, 3), F(5, 6)), (F(5, 8), F(1, 6))]:
        v = a / b
        q = "%s = <b>?</b>" % dv(a, b)
        if v > 1:
            q += "<br>Give your answer as a mixed number."
        its.append(mcq(q, S(v), Ss(dwr(a, b, ["nf", "first", "both", "addfr", "leftover"])), div_e(a, b)))
    # E) reasoning
    q = "Without calculating, which quotient is <b>greater</b> than %s?" % fr(3, 4)
    its.append(mcq(q, (dv(F(3, 4), F(2, 3)), None),
                   [(dv(F(3, 4), F(3, 2)), None), (mul(F(3, 4), F(2, 3)), None), ("%s ÷ 1" % fr(3, 4), None)],
                   "Dividing by a fraction less than 1 gives a greater answer, because more than one group fits. "
                   "%s is less than 1, so <b>%s</b> = %s is greater than %s." % (fr(2, 3), dv(F(3, 4), F(2, 3)),
                                                                                 show(F(9, 8)), fr(3, 4))))
    nm, he, his = P.next()
    q = "%s says %s = %s. What mistake did %s make?" % (nm, dv(F(2, 3), F(4, 5)), fr(6, 5), he)
    its.append(mcq(q, ("%s flipped %s instead of %s." % (cap(he), fr(2, 3), fr(4, 5)), None),
                   [("%s multiplied without flipping." % cap(he), None),
                    ("%s flipped both fractions." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "%s × %s = %s = %s, so %s flipped the first fraction. Flip only the divisor: "
                   "%s × %s = %s = <b>%s</b>." % (fr(3, 2), fr(4, 5), fr(12, 10), fr(6, 5), nm, fr(2, 3), fr(5, 4),
                                                   fr(10, 12), fr(5, 6))))
    q = "%s ÷ <b>?</b> = 3" % fr(3, 4)
    its.append(mcq(q, S(F(1, 4)), Ss([F(4), F(9, 4), F(1, 3)]),
                   "3 groups fit in %s, so each group is %s ÷ 3 = %s × %s = <b>%s</b>. Check: %s ÷ %s = %s × 4 = 3."
                   % (fr(3, 4), fr(3, 4), fr(3, 4), fr(1, 3), fr(1, 4), fr(3, 4), fr(1, 4), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Fraction ÷ fraction and reciprocals", "items": its}


# ============================================================ set 4: mixed numbers
def set_mixed():
    its = []
    # A) mixed number -> fraction
    q = "Write %s as an improper fraction." % show(F(13, 5))
    its.append(mcq(q, (fr(13, 5), F(13, 5)), [(fr(5, 5), F(1)), (fr(11, 5), F(11, 5)), (fr(23, 5), F(23, 5))],
                   "2 wholes are 2 × 5 = 10 fifths. Add the 3 fifths: 10 + 3 = 13. So %s = <b>%s</b>."
                   % (show(F(13, 5)), fr(13, 5))))
    q = "Write %s as an improper fraction." % show(F(13, 4))
    its.append(mcq(q, (fr(13, 4), F(13, 4)), [(fr(4, 4), F(1)), (fr(7, 4), F(7, 4)), (fr(12, 4), F(3))],
                   "3 wholes are 3 × 4 = 12 fourths. Add the 1 fourth: 12 + 1 = 13. So %s = <b>%s</b>."
                   % (show(F(13, 4)), fr(13, 4))))
    # B) multiply
    mo = ["parts", "badimp", "add", "cross", "addfr"]
    for x, y in [(F(3, 2), F(8, 3)), (F(9, 4), F(4, 3)), (F(5, 3), F(3, 5)), (F(7, 3), F(3, 2)),
                 (F(5, 2), F(5, 4)), (F(10, 3), F(3, 2)), (F(7, 4), F(8, 7)), (F(4), F(11, 8))]:
        v = x * y
        q = "%s = <b>?</b>" % mul(x, y)
        its.append(mcq(q, S(v), Ss(mwr(x, y, mo)), mul_e(x, y)))
    # C) divide
    do = ["nf", "parts", "fracflip", "first", "badimp", "leftover", "drop", "both"]
    for x, y in [(F(5, 2), F(5, 4)), (F(15, 4), F(3, 2)), (F(4, 3), F(3, 4)), (F(9, 2), F(3, 4)),
                 (F(8, 3), F(8, 5)), (F(5, 6), F(5, 4)), (F(3), F(9, 8)), (F(21, 4), F(7, 4))]:
        v = x / y
        q = "%s = <b>?</b>" % dv(x, y)
        its.append(mcq(q, S(v), Ss(dwr(x, y, do)), div_e(x, y)))
    # D) estimate
    q = "Which is the best estimate for %s?" % mul(F(23, 8), F(41, 10))
    its.append(mcq(q, ("about 12", None), [("about 8", None), ("about 7", None), ("about 20", None)],
                   "Round each mixed number to the nearest whole number: %s is close to 3 and %s is close to 4. "
                   "3 × 4 = 12, so the product is <b>about 12</b>. (2 × 4 = 8 ignores the fraction parts.)"
                   % (show(F(23, 8)), show(F(41, 10)))))
    q = "Without calculating, which is true about %s?" % dv(F(7, 2), F(7, 4))
    its.append(mcq(q, ("It is less than %s." % show(F(7, 2)), None),
                   [("It is greater than %s." % show(F(7, 2)), None), ("It is equal to %s." % show(F(7, 2)), None),
                    ("It is less than 1.", None)],
                   "%s is greater than 1, so fewer than %s groups fit. The quotient is <b>less than %s</b>: "
                   "%s × %s = %s = 2." % (show(F(7, 4)), show(F(7, 2)), show(F(7, 2)), fr(7, 2), fr(4, 7), fr(28, 14))))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    MO = ["parts", "add", "addfr", "cross", "div", "badimp", "addden"]
    DO = ["nf", "first", "leftover", "parts", "fracflip", "badimp", "drop", "both"]

    def wm(q, x, y, one, many=None, lead=""):
        x, y = F(x), F(y)
        v = x * y
        its.append(mcq(q, (qty(v, one, many), v), Q(mwr(x, y, MO), one, many),
                       mul_e(x, y, unit=(one if v <= 1 else (many or one)), lead=lead)))

    def wd(q, x, y, one, many=None, lead="", tail=""):
        x, y = F(x), F(y)
        v = x / y
        its.append(mcq(q, (qty(v, one, many), v), Q(dwr(x, y, DO), one, many),
                       div_e(x, y, unit=(one if v <= 1 else (many or one)), lead=lead) + tail))

    # 1 half a recipe
    nm, he, his = P.next()
    wm("A recipe for butter tarts needs %s cup of maple syrup. %s makes %s of the recipe. How much maple syrup does %s need?"
       % (fr(3, 4), nm, fr(1, 2), he), F(1, 2), F(3, 4), "cup", "cups",
       "%s of %s means %s × %s. " % (fr(1, 2), fr(3, 4), fr(1, 2), fr(3, 4)))
    # 2 batches of pancakes
    nm, he, his = P.next()
    wm("One batch of pancakes needs %s cup of milk. %s makes %s batches for a sleepover. How much milk does %s need?"
       % (fr(2, 3), nm, show(F(5, 2)), he), F(5, 2), F(2, 3), "cup", "cups",
       "%s batches of %s cup: multiply. " % (show(F(5, 2)), fr(2, 3)))
    # 3 granola bars
    nm, he, his = P.next()
    wd("%s has %s cups of oats. One batch of granola bars needs %s cup. How many batches can %s make?"
       % (nm, show(F(15, 4)), fr(3, 4), he), F(15, 4), F(3, 4), "batch", "batches",
       "How many %s cups fit in %s cups? Divide. " % (fr(3, 4), show(F(15, 4))))
    # 4 banners
    nm, he, his = P.next()
    wd("%s has %s m of red fabric for Canada Day banners. Each banner needs %s m. How many banners can %s make?"
       % (nm, fr(5, 6), fr(5, 12), he), F(5, 6), F(5, 12), "banner", "banners",
       "How many %s m pieces fit in %s m? Divide. " % (fr(5, 12), fr(5, 6)))
    # 5 fabric strips
    wd("A strip of fabric is %s m long. It is cut into pieces that are each %s m long. How many pieces are there?"
       % (show(F(9, 4)), fr(3, 8)), F(9, 4), F(3, 8), "piece", "pieces",
       "How many %s m pieces fit in %s m? Divide. " % (fr(3, 8), show(F(9, 4))))
    # 6 fabric area
    wm("A rectangular piece of fabric for a quilt is %s m long and %s m wide. What is its area?"
       % (fr(3, 4), fr(2, 3)), F(3, 4), F(2, 3), "m²", None, "Area = length × width. ")
    # 7 trail
    nm, he, his = P.next()
    wm("A hiking trail in Algonquin Park is %s km long. %s’s group has hiked %s of the trail. How far has the group hiked?"
       % (show(F(9, 2)), nm, fr(2, 3)), F(2, 3), F(9, 2), "km", None,
       "%s of %s km means %s × %s. " % (fr(2, 3), show(F(9, 2)), fr(2, 3), show(F(9, 2))))
    # 8 hiking rate
    nm, he, his = P.next()
    wd("%s hikes %s km in %s h. At this rate, how far does %s hike in 1 h?" % (nm, show(F(9, 4)), fr(3, 4), he),
       F(9, 4), F(3, 4), "km", None, "Divide the distance by the time. ")
    # 9 benches
    wd("A trail is %s km long. There is a bench at the end of every %s km section. How many %s km sections are there?"
       % (show(F(5, 2)), fr(5, 8), fr(5, 8)), F(5, 2), F(5, 8), "section", "sections",
       "How many %s km sections fit in %s km? Divide. " % (fr(5, 8), show(F(5, 2))))
    # 10 portage
    nm, he, his = P.next()
    wm("On a canoe trip, a portage is %s km long. %s carries the canoe for %s of the portage. How far does %s carry it?"
       % (show(F(6, 5)), nm, fr(5, 6), he), F(5, 6), F(6, 5), "km", None,
       "%s of %s km means %s × %s. " % (fr(5, 6), show(F(6, 5)), fr(5, 6), show(F(6, 5))))
    # 11 pizza
    nm, he, his = P.next()
    wm("There is %s of a pizza left. %s eats %s of what is left. What fraction of the whole pizza does %s eat?"
       % (fr(3, 4), nm, fr(1, 3), he), F(1, 3), F(3, 4), "of the pizza", None,
       "%s of %s means %s × %s. " % (fr(1, 3), fr(3, 4), fr(1, 3), fr(3, 4)))
    # 12 apple cider
    wd("A jug holds %s L of apple cider. Each glass holds %s L. How many glasses can be filled?"
       % (fr(2, 3), fr(1, 6)), F(2, 3), F(1, 6), "glass", "glasses",
       "How many %s L glasses fit in %s L? Divide. " % (fr(1, 6), fr(2, 3)))
    # 13 paint
    nm, he, his = P.next()
    wd("%s uses %s of a can of paint to paint %s of a fence. How many cans does %s need to paint the whole fence?"
       % (nm, fr(1, 2), fr(3, 5), he), F(1, 2), F(3, 5), "can", "cans",
       "Paint for the whole fence = paint used ÷ fraction of the fence painted. ")
    # 14 garden
    wm("In a community garden plot, %s of the area is vegetables. %s of the vegetable area is tomatoes. "
       "What fraction of the plot is tomatoes?" % (fr(5, 8), fr(2, 5)), F(2, 5), F(5, 8), "of the plot", None,
       "%s of %s means %s × %s. " % (fr(2, 5), fr(5, 8), fr(2, 5), fr(5, 8)))
    # 15 field trip
    wm("%s of the Grade 7 students go on a field trip to Ottawa. %s of those students visit the Canadian Museum of Nature. "
       "What fraction of the Grade 7 students visit the museum?" % (fr(2, 3), fr(3, 4)), F(3, 4), F(2, 3),
       "of the students", None, "%s of %s means %s × %s. " % (fr(3, 4), fr(2, 3), fr(3, 4), fr(2, 3)))
    # 16 recipe scaling
    nm, he, his = P.next()
    wm("A recipe for 12 muffins uses %s cups of flour. %s makes %s times the recipe. How much flour does %s need?"
       % (show(F(4, 3)), nm, show(F(3, 2)), he), F(4, 3), F(3, 2), "cup", "cups",
       "%s times %s cups: multiply. " % (show(F(3, 2)), show(F(4, 3))))
    # 17 full batches (interpret the leftover)
    nm, he, his = P.next()
    x, y = F(5, 2), F(2, 3)
    q = ("%s has %s cups of flour. One batch of cookies needs %s cup. How many <b>full</b> batches can %s make?"
         % (nm, show(x), fr(2, 3), he))
    its.append(mcq(q, ("3 batches", F(3)),
                   [("4 batches", F(4)), ("%s batches" % show(x / y), x / y), ("%s batches" % show(x * y), x * y)],
                   div_e(x, y) + " Only full batches count, so %s can make <b>3 batches</b>." % he))
    # 18 which expression
    q = ("A trail is %s km long. A sign is placed at the end of every %s km. Which expression gives the number of "
         "%s km sections?" % (fr(5, 6), fr(1, 12), fr(1, 12)))
    its.append(mcq(q, (dv(F(5, 6), F(1, 12)), None),
                   [(mul(F(5, 6), F(1, 12)), None), (dv(F(1, 12), F(5, 6)), None), ("%s − %s" % (fr(5, 6), fr(1, 12)), None)],
                   "The question asks how many %s km sections fit in %s km, so divide %s by %s: <b>%s</b> = %s × 12 = "
                   "10 sections." % (fr(1, 12), fr(5, 6), fr(5, 6), fr(1, 12), dv(F(5, 6), F(1, 12)), fr(5, 6))))
    # 19 reverse: whole trail
    nm, he, his = P.next()
    wd("%s has biked %s km. That is %s of a trail. How long is the whole trail?" % (nm, show(F(3, 2)), fr(3, 5)),
       F(3, 2), F(3, 5), "km", None,
       "%s of the trail is %s km, so the whole trail is %s ÷ %s. " % (fr(3, 5), show(F(3, 2)), show(F(3, 2)), fr(3, 5)))
    # 20 piano
    nm, he, his = P.next()
    wm("%s practises piano for %s h. %s spends %s of the time on scales. How long does %s spend on scales?"
       % (nm, fr(3, 4), cap(he), fr(2, 3), he), F(2, 3), F(3, 4), "h", None,
       "%s of %s h means %s × %s. " % (fr(2, 3), fr(3, 4), fr(2, 3), fr(3, 4)))
    its[-1]["e"] += " That is 30 min."
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, fabric and trails", "items": its}


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
        "The area model shows why the denominators multiply: the square is cut into 3 × 4 = 12 small rectangles.</p>"
        + area_fig
        + ex("Example 1", mul(F(2, 5), F(3, 7)) + " = ?", fr("2 × 3", "5 × 7") + " = " + fr(6, 35) + ".", fr(6, 35))
        + "<h2>Simplify before you multiply</h2>"
        "<p>Divide a numerator and a denominator by the same number first. The numbers stay small.</p>"
        + ex("Example 2", mul(F(4, 9), F(3, 8)) + " = ?",
             "4 and 8 share 4: they become 1 and 2. 3 and 9 share 3: they become 1 and 3. "
             "Now " + mul(F(1, 3), F(1, 2)) + " = " + fr(1, 6) + ".", fr(1, 6))
        + "<h2>Divide fractions</h2>"
        "<p>Count how many groups fit, or use the rule: <b>keep</b> the first fraction, <b>change</b> ÷ to ×, "
        "and <b>flip</b> the second fraction (use its reciprocal).</p>"
        + bar_fig
        + ex("Example 3", dv(F(2, 3), F(4, 5)) + " = ?",
             "Keep " + fr(2, 3) + ", flip " + fr(4, 5) + " to " + fr(5, 4) + ": " + mul(F(2, 3), F(5, 4)) + " = "
             + fr(10, 12) + " = " + fr(5, 6) + ". Check: " + mul(F(5, 6), F(4, 5)) + " = " + fr(20, 30) + " = "
             + fr(2, 3) + ".", fr(5, 6))
        + "<h2>Mixed numbers</h2>"
        "<p>Change mixed numbers to improper fractions first. Then multiply or divide.</p>"
        + ex("Example 4", mul(F(3, 2), F(8, 3)) + " = ?",
             "Write " + show(F(3, 2)) + " as " + fr(3, 2) + " and " + show(F(8, 3)) + " as " + fr(8, 3) + ". "
             + fr(3, 2) + " × " + fr(8, 3) + " = " + fr(24, 6) + " = 4.", "4")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [mul(F(2, 3), F(4, 5)) + " = " + fr(6, 8) + " (adding across)",
             "Multiply across: " + fr("2 × 4", "3 × 5") + " = " + fr(8, 15) + "."],
            [dv(F(2, 3), F(4, 5)) + " = " + fr(3, 2) + " × " + fr(4, 5) + " (flipping the wrong fraction)",
             "Keep the first fraction. Flip only the divisor: " + mul(F(2, 3), F(5, 4)) + " = " + fr(5, 6) + "."],
            [mul(F(3, 2), F(8, 3)) + " = 2 + " + mul(F(1, 2), F(2, 3)) + " = 2 " + fr(1, 3)
             + " (multiplying whole parts and fraction parts separately)",
             "Change to improper fractions first: " + fr(3, 2) + " × " + fr(8, 3) + " = 4."],
            ["Simplifying two numerators, like 6 and 9 in " + mul(F(6, 7), F(9, 10)),
             "Always pair a numerator with a denominator: 6 and 10."],
        ])
    )


FAQ = [
    {"q": "How do you multiply fractions in Grade 7?",
     "a": "Multiply the numerators, multiply the denominators, then simplify. For example, 2/3 × 3/4 = 6/12 = 1/2. You can also simplify before you multiply by dividing a numerator and a denominator by the same number."},
    {"q": "How do you divide a fraction by a fraction?",
     "a": "Keep the first fraction, change ÷ to ×, and flip the second fraction, then multiply. For example, 2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12 = 5/6."},
    {"q": "How do you multiply and divide mixed numbers?",
     "a": "Change each mixed number to an improper fraction first. For example, 1 1/2 × 2 2/3 = 3/2 × 8/3 = 4, and 2 1/2 ÷ 1 1/4 = 5/2 × 4/5 = 2."},
    {"q": "When do Ontario students learn to multiply and divide fractions by fractions?",
     "a": "In Grade 7, in the Number strand of the 2020 Ontario math curriculum (expectation B2.8). In Grade 6, students multiply and divide whole numbers by proper fractions."},
]


def gen():
    rnd = random.Random(47808)
    P = People(rnd)
    sets = [set_area(), set_simplify(P), set_divide(P), set_mixed(), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "multiplying-and-dividing-fractions",
        "sort": 8, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Multiplying and Dividing Fractions",
        "seo_title": "Grade 7 Multiplying and Dividing Fractions Worksheets: Area Models, Reciprocals, Mixed Numbers (Free, Answer Key, Ontario)",
        "short_title": "Multiplying and dividing fractions",
        "domain": "Number",
        "standard_code": "Grade 7: B2.8",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide fractions by fractions, using tools in various contexts",
        "meta_desc": "Free Grade 7 math worksheets on multiplying and dividing fractions for the Ontario curriculum: area models, simplifying before you multiply, how many fit, multiplying by the reciprocal, mixed numbers and word problems. 100 questions with an answer key.",
        "key_big": "To multiply fractions, multiply the numerators and the denominators. To divide, multiply by the reciprocal of the second fraction.",
        "key_sub": "2/3 × 3/4 = 6/12 = 1/2. 2/3 ÷ 4/5 = 2/3 × 5/4 = 5/6: flip only the fraction you divide by. Change mixed numbers to improper fractions first.",
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
