# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Multiplying and Dividing with Fractions (Ontario Mathematics Curriculum 2020, Number B2)
  python3 tools/gen_ca_math_g6_mult_div_fractions.py
Grade 6 multiplies and divides WHOLE NUMBERS by PROPER FRACTIONS:
  whole number × fraction (bar models), fractions of quantities, whole number ÷ unit fraction (pictures),
  whole number ÷ proper fraction, word problems. No fraction × fraction or fraction ÷ fraction.
Every answer is checked with fractions.Fraction; no two choices are equal in value.
Canadian English, $ and ¢, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
G1 = "#4fae74"        # shaded / group colour 1
G2 = "#a6dbb7"        # group colour 2
LINE = "#2b2b2b"
RED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PARTS = {2: ("half", "halves"), 3: ("third", "thirds"), 4: ("fourth", "fourths"), 5: ("fifth", "fifths"),
         6: ("sixth", "sixths"), 7: ("seventh", "sevenths"), 8: ("eighth", "eighths"), 10: ("tenth", "tenths"),
         12: ("twelfth", "twelfths")}


# ------------------------------------------------------------ numbers
def num(n):
    """Ontario style: 4 digits plain, 5 or more digits grouped with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NBSP.join(out)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return num(q)
    if q == 0:
        return fr(r, v.denominator)
    return "%s %s" % (num(q), fr(r, v.denominator))


def R(n, d, unit=""):
    """A fraction exactly as a student wrote it (not simplified), with its value."""
    return (fr(n, d) + (" " + unit if unit else ""), F(n, d))


def S(v, unit="", pre=""):
    """A value in simplest form with an optional unit."""
    v = F(v)
    return (pre + show(v) + (" " + unit if unit else ""), v)


def parts(b, k=2):
    return PARTS[b][0] if k == 1 else PARTS[b][1]


def pl(k, one, many):
    return one if k == 1 else many


def cap(s):
    return s[0].upper() + s[1:]


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). A candidate equal in value to an earlier choice is skipped.
    Positions are set later by balance()."""
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
    """Tag wide pictures (rows of bars, number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def nf(n, a, b):
    return "%d × %s" % (n, fr(a, b))


def fn(a, b, n):
    return "%s × %d" % (fr(a, b), n)


def dv(n, a, b):
    return "%d ÷ %s" % (n, fr(a, b))


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tape_svg(q, a, b, part_labels=False, Wt=300):
    """A bar worth q split into b equal parts, a parts shaded; the total is marked above."""
    x0, y0, H = 6, 36, 36
    s = ["<line x1='%d' y1='16' x2='%d' y2='16' stroke='%s' stroke-width='2'/>" % (x0, x0 + Wt, LINE),
         "<line x1='%d' y1='8' x2='%d' y2='24' stroke='%s' stroke-width='2'/>" % (x0, x0, LINE),
         "<line x1='%d' y1='8' x2='%d' y2='24' stroke='%s' stroke-width='2'/>" % (x0 + Wt, x0 + Wt, LINE)]
    lab = num(q)
    lw = len(lab) * 18 * 0.6 + 12
    s.append("<rect x='%.1f' y='2' width='%.1f' height='26' fill='#fff'/>" % (x0 + Wt / 2 - lw / 2, lw))
    s.append(text(x0 + Wt / 2, 23, lab, 18))
    pw = Wt / float(b)
    for i in range(b):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * pw, y0, pw, H, G1 if i < a else "#fff", LINE))
        if part_labels:
            s.append(text(x0 + i * pw + pw / 2, y0 + 24, num(q // b), 16, "#fff" if i < a else LINE))
    return svg_wrap(Wt + 12, y0 + H + 6, "".join(s),
                    "bar model worth %d split into %d equal parts with %d shaded" % (q, b, a))


def copies_svg(n, a, b, BW=None):
    """n bars side by side, each 1 whole cut into b equal parts with a parts shaded (n × a/b)."""
    if BW is None:
        BW = max(48, min(84, (430 - (n - 1) * 12) // n))
    gap, x0, y0, H = 12, 6, 6, 40
    s = []
    for k in range(n):
        bx = x0 + k * (BW + gap)
        pw = BW / float(b)
        for i in range(b):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (bx + i * pw, y0, pw, H, G1 if i < a else "#fff", LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (bx, y0, BW, H, LINE))
    W = x0 * 2 + n * BW + (n - 1) * gap
    return svg_wrap(W, y0 + H + 6, "".join(s),
                    "row of %d bars, each 1 whole cut into %d equal parts with %d shaded" % (n, b, a))


def wholes_svg(n, b, a=1, numbered=False, PW=None):
    """n wholes in a row, each cut into b pieces. Pieces are coloured in groups of a (two greens).
    For a > 1 a bracket is drawn over every group. Labels 0..n under the thick whole lines."""
    k = n * b
    if PW is None:
        PW = max(16, min(40, 400 // k))
    X0, BH = 14, 36
    T = 30 if (a > 1 or numbered) else 8
    W = X0 * 2 + k * PW
    s = []
    for i in range(k):
        col = G1 if (i // a) % 2 == 0 else G2
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (X0 + i * PW, T, PW, BH, col, LINE))
    for j in range(n + 1):
        x = X0 + j * b * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append(text(x, T + BH + 26, str(j), 16))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, k * PW, BH, LINE))
    if a > 1 or numbered:
        for g in range(k // a):
            x0 = X0 + g * a * PW + 2
            x1 = X0 + (g + 1) * a * PW - 2
            s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x0, T - 4, T - 12, x1, T - 4, LINE))
            if numbered:
                s.append(text((x0 + x1) / 2.0, T - 15, str(g + 1), 14))
    if a > 1:
        lab = "%d wholes, each cut into %d equal pieces, marked in groups of %d pieces" % (n, b, a)
    else:
        lab = "%d %s, each cut into %d equal pieces" % (n, pl(n, "whole", "wholes"), b)
    return svg_wrap(W, T + BH + 32, "".join(s), lab)


def jumps_svg(n, b, W=440):
    """Number line 0..n with ticks every 1/b and n*b jumps of 1/b."""
    total = n * b
    L, Rr, Y = 18, W - 18, 46

    def X(i):
        return L + (Rr - L) * i / float(total)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, Rr, Y, LINE)]
    for i in range(total + 1):
        whole = (i % b == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if whole else 7), X(i), Y + (12 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append(text(X(i), Y + 34, str(i // b), 18))
    h = 26 if (Rr - L) / float(total) > 24 else 18
    for j in range(total):
        x0, x1 = X(j), X(j + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.2'/>"
                 % (x0 + 1, Y - 3, (x0 + x1) / 2, Y - 3 - h, x1 - 1, Y - 3, RED))
        s.append("<path d='M%.1f %d l-6 -8 l8 1 z' fill='%s'/>" % (x1 - 1, Y - 3, RED))
    return svg_wrap(W, Y + 42, "".join(s), "number line from 0 to %d with jumps of 1/%d" % (n, b))


# ------------------------------------------------------------ explanations
def of_e(a, b, q, pre="", unit=""):
    u = " " + unit if unit else ""
    p = q // b
    return ("Divide by the denominator: %s%s ÷ %d = %s%s%s in each part. Multiply by the numerator: "
            "%d × %s%s = %s%s%s. So %s of %s%s%s = <b>%s%s%s</b>."
            % (pre, num(q), b, pre, num(p), u, a, pre, num(p), pre, num(a * p), u,
               fr(a, b), pre, num(q), u, pre, num(a * p), u))


def of_wrongs(a, b, q, order, pre="", unit=""):
    u = " " + unit if unit else ""
    out = []
    order = list(order) + ["den"]
    for k in order:
        if k == "one":                          # stopped after dividing
            v = F(q, b)
        elif k == "unshaded":                   # found the other part
            v = F((b - a) * q, b)
        elif k == "times":                      # multiplied by the numerator only
            v = F(a * q)
        elif k == "swap":                       # divided by the numerator, multiplied by the denominator
            if q % a or a == 1:
                continue
            v = F(q // a * b)
        elif k == "den":                        # multiplied by the denominator
            v = F(q * b)
        else:
            raise ValueError(k)
        if v.denominator == 1:
            out.append(("%s%s%s" % (pre, num(v.numerator), u), v))
    return out


def nf_e(n, a, b, lead=""):
    v = F(n * a, b)
    s = lead + ("Multiply the whole number by the numerator and keep the denominator: %d × %d = %d, so the answer is %s."
                % (n, a, n * a, fr(n * a, b)))
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        s += " %d ÷ %d = %d, so it is <b>%s</b> %s." % (n * a, b, q, show(v), pl(q, "whole", "wholes"))
    else:
        g = math.gcd(n * a, b)
        if g > 1:
            s += " Simplify: %s = %s." % (fr(n * a, b), fr(v.numerator, v.denominator))
        s += " %d ÷ %d = %d remainder %d, so it is <b>%s</b>." % (v.numerator, v.denominator, q, r, show(v))
    return s


def nf_wrongs(n, a, b, order):
    """n × a/b: (html, value) from real mistakes."""
    out = []
    for k in order:
        if k == "both":                         # multiplied the numerator and the denominator
            out.append(R(n * a, n * b))
        elif k == "bottom":                     # multiplied the denominator
            out.append(R(a, n * b))
        elif k == "addtop":                     # added the whole number to the numerator
            out.append(R(n + a, b))
        elif k == "add":                        # added
            out.append(S(n + F(a, b)))
        elif k == "top":                        # forgot the denominator
            out.append(S(F(n * a)))
        else:
            raise ValueError(k)
    return out


def wu_e(n, b):
    if n == 1:
        s = "There are %d %s in 1 whole, so %s = <b>%d</b>." % (b, parts(b), dv(1, 1, b), b)
    else:
        s = ("Each whole has %d %s. %d wholes have %d × %d = %d %s, so %s = <b>%d</b>."
             % (b, parts(b), n, n, b, n * b, parts(b), dv(n, 1, b), n * b))
    return s + " Check: %d × %s = %s = %d." % (n * b, fr(1, b), fr(n * b, b), n)


def wu_wrongs(n, b, order):
    out = []
    for k in order:
        if k == "times":                        # multiplied by the fraction: “dividing makes smaller”
            out.append(R(n, b))
        elif k == "one":                        # counted the pieces in 1 whole only
            out.append(S(F(b)))
        elif k == "add":                        # added
            out.append(S(F(n + b)))
        elif k == "flip":                       # flipped the wrong number: 1/n × 1/b
            out.append(R(1, n * b))
        elif k == "div":                        # n ÷ b
            if n % b == 0:
                out.append(S(F(n, b)))
            else:
                out.append(S(F(n, b)))
        else:
            raise ValueError(k)
    return out


def wp_e(n, a, b, lead=""):
    """n ÷ a/b explained with pieces, then the rule."""
    k = n * b
    q = F(n) / F(a, b)
    one, many = PARTS[b]
    s = lead + "Each whole has %d %s, so %d wholes have %d × %d = %d %s. " % (b, many, n, n, b, k, many)
    s += "Each group is %s = %d %s. " % (fr(a, b), a, many)
    w, r = divmod(k, a)
    if r == 0:
        s += "%d ÷ %d = %d groups. " % (k, a, w)
    else:
        s += ("%d ÷ %d = %d remainder %d. The %d %s left over %s %s of a group. "
              % (k, a, w, r, r, pl(r, one, many), pl(r, "is", "are"), fr(r, a)))
    s += "Or flip only the divisor: %d × %s = %s. So %s = <b>%s</b>." % (n, fr(b, a), fr(n * b, a), dv(n, a, b), show(q))
    s += " Check: %s × %s = %d." % (show(q), fr(a, b), n)
    return s


def wp_wrongs(n, a, b, order):
    out = []
    for k in order:
        if k == "times":                        # multiplied by the fraction
            out.append(S(F(n * a, b)))
        elif k == "flip":                       # flipped the whole number instead: 1/n × a/b
            out.append(R(a, n * b))
        elif k == "denom":                      # multiplied by the denominator only
            out.append(S(F(n * b)))
        elif k == "numer":                      # divided by the numerator only
            out.append(S(F(n, a)))
        elif k == "drop":                       # dropped the leftover
            out.append(S(F(n * b // a)))
        elif k == "whole":                      # leftover written as part of a whole, not of a group
            w, r = divmod(n * b, a)
            if r:
                out.append(S(w + F(r, b)))
        elif k == "plus1":                      # rounded the groups up
            out.append(S(F(n * b // a + 1)))
        else:
            raise ValueError(k)
    return out


# ============================================================ set 1: whole number × fraction
def set_times():
    its = []
    # A) bar models: fraction of a whole number
    for a, b, q, order in [(2, 3, 12, ["one", "times", "unshaded", "swap"]),
                           (3, 4, 20, ["one", "unshaded", "times", "swap"]),
                           (2, 5, 30, ["times", "one", "unshaded", "swap"]),
                           (5, 6, 18, ["one", "unshaded", "times", "den"]),
                           (3, 8, 40, ["unshaded", "one", "times", "swap"]),
                           (4, 7, 21, ["one", "times", "unshaded", "den"])]:
        qq = (fig(tape_svg(q, a, b)) + "The whole bar is %d. The shaded part shows %s × %d. What is %s × %d?"
              % (q, fr(a, b), q, fr(a, b), q))
        e = "%s × %d means %s of %d. " % (fr(a, b), q, fr(a, b), q) + of_e(a, b, q)
        its.append(mcq(qq, S(F(a * q, b)), of_wrongs(a, b, q, order), e))
    # B) rows of bars: n × a/b
    for n, a, b, order in [(5, 3, 4, ["both", "bottom", "add", "top"]),
                           (4, 2, 3, ["addtop", "both", "add", "bottom"]),
                           (3, 4, 5, ["both", "add", "addtop", "bottom"]),
                           (6, 1, 4, ["bottom", "both", "add", "addtop"]),
                           (4, 3, 5, ["add", "both", "bottom", "addtop"])]:
        qq = (fig(copies_svg(n, a, b)) + "Each bar is 1 whole. The picture shows %s. "
              "How many wholes are shaded altogether?" % nf(n, a, b))
        lead = "Count the shaded parts: %d bars × %d shaded = %d %s. " % (n, a, n * a, parts(b, n * a))
        its.append(mcq(qq, S(F(n * a, b)), nf_wrongs(n, a, b, order), nf_e(n, a, b, lead)))
    # C) whole-number answers
    for form, n, a, b, order in [("nf", 4, 3, 4, ["both", "top", "add", "bottom"]),
                                 ("fn", 6, 2, 3, ["top", "both", "addtop", "add"]),
                                 ("nf", 10, 3, 5, ["both", "top", "bottom", "add"]),
                                 ("fn", 8, 3, 8, ["top", "both", "bottom", "add"]),
                                 ("nf", 12, 5, 6, ["top", "add", "both", "bottom"]),
                                 ("fn", 9, 2, 3, ["both", "top", "addtop", "add"])]:
        expr = nf(n, a, b) if form == "nf" else fn(a, b, n)
        qq = "%s = <b>?</b>" % expr
        its.append(mcq(qq, S(F(n * a, b)), nf_wrongs(n, a, b, order), nf_e(n, a, b)))
    # D) mixed-number answers
    for form, n, a, b, order in [("nf", 7, 2, 3, ["both", "addtop", "add", "top"]),
                                 ("fn", 3, 5, 6, ["add", "both", "bottom", "top"]),
                                 ("nf", 9, 3, 8, ["bottom", "both", "top", "add"])]:
        expr = nf(n, a, b) if form == "nf" else fn(a, b, n)
        qq = "%s = <b>?</b><br>Give your answer as a mixed number." % expr
        its.append(mcq(qq, S(F(n * a, b)), nf_wrongs(n, a, b, order), nf_e(n, a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Whole number × fraction with bar models", "items": its}


# ============================================================ set 2: fraction of a quantity
def set_quantity():
    its = []
    for a, b, q, pre, unit, order in [
            (3, 4, 24, "", "kg", ["one", "unshaded", "times", "swap"]),
            (2, 5, 35, "", "m", ["one", "times", "unshaded", "den"]),
            (3, 4, 20, "$", "", ["one", "unshaded", "times", "swap"]),
            (2, 3, 60, "", "min", ["one", "unshaded", "times", "swap"]),
            (5, 8, 64, "", "cm", ["one", "unshaded", "times", "swap"]),
            (7, 10, 50, "", "L", ["one", "unshaded", "times", "den"]),
            (3, 5, 2500, "", "m", ["one", "unshaded", "times", "swap"]),
            (5, 6, 42, "", "km", ["one", "unshaded", "times", "den"]),
            (4, 9, 54, "", "mL", ["one", "unshaded", "times", "swap"]),
            (2, 3, 4500, "", "g", ["one", "unshaded", "times", "swap"]),
            (3, 8, 96, "$", "", ["one", "unshaded", "times", "swap"]),
            (9, 10, 1000, "", "mL", ["one", "unshaded", "times", "den"]),
            (5, 12, 60, "", "min", ["one", "unshaded", "times", "swap"]),
            (3, 7, 140, "", "kg", ["one", "unshaded", "times", "den"])]:
        qq = "What is %s of %s%s%s?" % (fr(a, b), pre, num(q), " " + unit if unit else "")
        v = F(a * q, b)
        its.append(mcq(qq, S(v, unit, pre), of_wrongs(a, b, q, order, pre, unit), of_e(a, b, q, pre, unit)))
    # reverse: a/b of a number is p
    for a, b, p, extra in [(2, 5, 14, [("28", F(28)), ("7", F(7)), ("70", F(70)), ("5 " + fr(3, 5), F(28, 5))]),
                           (3, 4, 27, [("36", F(36)), ("9", F(9)), ("108", F(108)), ("20 " + fr(1, 4), F(81, 4))]),
                           (5, 6, 40, [("48", F(48)), ("8", F(8)), ("240", F(240)), ("33 " + fr(1, 3), F(100, 3))])]:
        whole = p * b // a
        qq = "%s of a number is %d. What is the number?" % (fr(a, b), p)
        e = ("%d parts are %d, so 1 part is %d ÷ %d = %d. The whole has %d parts: %d × %d = <b>%d</b>. "
             "Check: %s of %d = %d ÷ %d × %d = %d."
             % (a, p, p, a, p // a, b, p // a, b, whole, fr(a, b), whole, whole, b, a, p))
        its.append(mcq(qq, (str(whole), F(whole)), extra, e))
    # compare
    qq = "Which is greater: %s of 20 or %s of 24?" % (fr(3, 4), fr(2, 3))
    its.append(mcq(qq, ("%s of 24" % fr(2, 3), None),
                   [("%s of 20" % fr(3, 4), None), ("They are equal.", None), ("You can’t tell.", None)],
                   "%s of 20: 20 ÷ 4 = 5, 5 × 3 = 15. %s of 24: 24 ÷ 3 = 8, 8 × 2 = 16. 16 is greater than 15, "
                   "so <b>%s of 24</b> is greater." % (fr(3, 4), fr(2, 3), fr(2, 3))))
    # missing denominator
    qq = ("<span class='fr'><span class='fn'>3</span><span class='fd'><b>?</b></span></span> of 40 = 15. "
          "What is the missing denominator?")
    its.append(mcq(qq, ("8", F(8)), [("5", F(5)), ("25", F(25)), ("15", F(15))],
                   "15 is 3 parts, so 1 part is 15 ÷ 3 = 5. 40 ÷ 5 = 8, so 40 is split into 8 equal parts: "
                   "%s of 40 = 15. The missing denominator is <b>8</b>." % fr(3, 8)))
    # missing numerator
    qq = ("<span class='fr'><span class='fn'><b>?</b></span><span class='fd'>5</span></span> of 30 = 18. "
          "What is the missing numerator?")
    its.append(mcq(qq, ("3", F(3)), [("6", F(6)), ("2", F(2)), ("12", F(12))],
                   "30 ÷ 5 = 6, so each fifth of 30 is 6. 18 ÷ 6 = 3 parts, so %s of 30 = 18. "
                   "The missing numerator is <b>3</b>." % fr(3, 5)))
    assert len(its) == 20, len(its)
    return {"title": "Fraction of a quantity", "items": its}


# ============================================================ set 3: whole number ÷ unit fraction
def set_unit():
    its = []
    # A) bar pictures
    for n, b, order in [(3, 4, ["times", "one", "add", "flip"]), (2, 3, ["one", "times", "flip", "add"]),
                        (4, 2, ["times", "add", "flip", "one"]), (2, 5, ["flip", "times", "one", "add"]),
                        (3, 3, ["times", "one", "flip", "div"]), (2, 6, ["one", "times", "add", "flip"])]:
        qq = (fig(wholes_svg(n, b)) + "Each whole is cut into %s. How many %s are in %d? %s = <b>?</b>"
              % (parts(b), parts(b), n, dv(n, 1, b)))
        its.append(mcq(qq, S(F(n * b)), wu_wrongs(n, b, order), wu_e(n, b)))
    # B) number-line jumps
    for n, b, order in [(2, 4, ["times", "one", "flip", "add"]), (3, 2, ["one", "times", "add", "flip"]),
                        (3, 5, ["flip", "one", "times", "add"]), (4, 3, ["times", "add", "one", "flip"])]:
        qq = (fig(jumps_svg(n, b)) + "Each jump is %s. How many jumps from 0 to %d? %s = <b>?</b>"
              % (fr(1, b), n, dv(n, 1, b)))
        e = "Count the jumps: %d in each whole. " % b + wu_e(n, b)
        its.append(mcq(qq, S(F(n * b)), wu_wrongs(n, b, order), e))
    # C) calculate
    for n, b, order in [(5, 3, ["times", "one", "add", "flip"]), (8, 2, ["times", "flip", "one", "add"]),
                        (4, 6, ["times", "add", "flip", "one"]), (7, 4, ["flip", "times", "one", "add"]),
                        (9, 5, ["times", "one", "add", "flip"]), (10, 8, ["times", "flip", "add", "one"])]:
        qq = "%s = <b>?</b>" % dv(n, 1, b)
        its.append(mcq(qq, S(F(n * b)), wu_wrongs(n, b, order), wu_e(n, b)))
    # D) reasoning
    qq = "Which is the same as %s?" % dv(6, 1, 3)
    its.append(mcq(qq, ("6 × 3", None), [("6 × %s" % fr(1, 3), None), ("6 ÷ 3", None), ("%s × %s" % (fr(1, 6), fr(1, 3)), None)],
                   "%s asks how many thirds are in 6. Each whole has 3 thirds, so it is <b>6 × 3</b> = 18. "
                   "Flip only the divisor: %s becomes 3." % (dv(6, 1, 3), fr(1, 3))))
    qq = "Without calculating, which is true about %s?" % dv(4, 1, 2)
    its.append(mcq(qq, ("It is greater than 4.", None),
                   [("It is less than 4.", None), ("It is equal to 4.", None), ("It is less than 1.", None)],
                   "There are 2 halves in every whole, so there are more halves than wholes. %s = 8, which is "
                   "<b>greater than 4</b>. Dividing by a fraction less than 1 gives a bigger answer." % dv(4, 1, 2)))
    qq = "<b>?</b> ÷ %s = 30" % fr(1, 5)
    its.append(mcq(qq, ("6", F(6)), [("150", F(150)), ("25", F(25)), ("35", F(35))],
                   "Each whole has 5 fifths. How many wholes make 30 fifths? 30 ÷ 5 = <b>6</b>. "
                   "Check: %s = 6 × 5 = 30." % dv(6, 1, 5)))
    qq = "8 ÷ <b>?</b> = 24"
    its.append(mcq(qq, R(1, 3), [("3", F(3)), ("16", F(16)), R(1, 16)],
                   "24 ÷ 8 = 3, so each whole holds 3 equal pieces. The pieces are thirds: "
                   "%s = 8 × 3 = 24. The missing number is <b>%s</b>." % (dv(8, 1, 3), fr(1, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Whole number ÷ unit fraction with pictures", "items": its}


# ============================================================ set 4: whole number ÷ proper fraction
def set_proper(P):
    its = []
    # A) pictures with groups
    for n, a, b, order in [(4, 2, 3, ["times", "flip", "denom", "numer"]),
                           (4, 2, 5, ["times", "denom", "flip", "numer"]),
                           (3, 3, 4, ["flip", "times", "denom", "numer"]),
                           (2, 2, 3, ["times", "denom", "numer", "flip"]),
                           (3, 3, 5, ["times", "flip", "numer", "denom"]),
                           (4, 4, 5, ["denom", "times", "flip", "numer"])]:
        q = F(n) / F(a, b)
        qq = (fig(wholes_svg(n, b, a)) + "Each whole is cut into %s. Each bracket marks a group of %s. "
              "How many groups are in %d? %s = <b>?</b>" % (parts(b), fr(a, b), n, dv(n, a, b)))
        its.append(mcq(qq, S(q), wp_wrongs(n, a, b, order), wp_e(n, a, b, "Count the brackets. ")))
    # B) calculate, whole-number answers
    for n, a, b, order in [(8, 2, 3, ["times", "flip", "denom", "numer"]),
                           (10, 2, 5, ["times", "denom", "flip", "numer"]),
                           (9, 3, 5, ["flip", "times", "denom", "numer"]),
                           (12, 3, 4, ["times", "denom", "numer", "flip"]),
                           (15, 5, 6, ["times", "flip", "denom", "numer"]),
                           (14, 7, 8, ["denom", "times", "numer", "flip"]),
                           (6, 3, 7, ["times", "flip", "numer", "denom"]),
                           (20, 4, 5, ["times", "denom", "flip", "numer"])]:
        q = F(n) / F(a, b)
        qq = "%s = <b>?</b>" % dv(n, a, b)
        its.append(mcq(qq, S(q), wp_wrongs(n, a, b, order), wp_e(n, a, b)))
    # C) mixed-number answers
    for n, a, b, order in [(5, 2, 3, ["whole", "drop", "times", "flip"]),
                           (7, 3, 4, ["whole", "times", "drop", "flip"]),
                           (4, 3, 5, ["drop", "whole", "times", "flip"])]:
        q = F(n) / F(a, b)
        qq = "%s = <b>?</b><br>Give your answer as a mixed number." % dv(n, a, b)
        its.append(mcq(qq, S(q), wp_wrongs(n, a, b, order), wp_e(n, a, b)))
    # D) reasoning and mistakes
    qq = "Without calculating, which answer is greater than 12?"
    its.append(mcq(qq, (dv(12, 3, 4), None),
                   [("%s × 12" % fr(3, 4), None), ("%s of 12" % fr(3, 4), None), ("12 ÷ 4", None)],
                   "Multiplying by %s or taking %s of 12 gives less than 12, and 12 ÷ 4 = 3. Dividing by a fraction less "
                   "than 1 gives more: <b>%s</b> = 16." % (fr(3, 4), fr(3, 4), dv(12, 3, 4))))
    nm, he, his = P.next()
    qq = "%s says %s = 4. What did %s do?" % (nm, dv(6, 2, 3), he)
    its.append(mcq(qq, ("%s multiplied by %s instead of dividing." % (cap(he), fr(2, 3)), None),
                   [("%s flipped 6 instead of %s." % (cap(he), fr(2, 3)), None),
                    ("%s multiplied 6 by 3 only." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "6 × %s = 4, so %s multiplied. Dividing by a fraction less than 1 must give more than 6: "
                   "%s = 6 × %s = %s = <b>9</b>." % (fr(2, 3), nm, dv(6, 2, 3), fr(3, 2), fr(18, 2))))
    nm, he, his = P.next()
    qq = "%s says %s = %s. What did %s do?" % (nm, dv(4, 2, 5), fr(1, 10), he)
    its.append(mcq(qq, ("%s flipped 4 instead of %s." % (cap(he), fr(2, 5)), None),
                   [("%s multiplied by %s instead of dividing." % (cap(he), fr(2, 5)), None),
                    ("%s divided 4 by 5 only." % cap(he), None),
                    ("Nothing. The answer is correct.", None)],
                   "%s × %s = %s = %s, so %s flipped the wrong number. Keep 4 and flip only the divisor: "
                   "4 × %s = %s = <b>10</b>." % (fr(1, 4), fr(2, 5), fr(2, 20), fr(1, 10), nm, fr(5, 2), fr(20, 2))))
    assert len(its) == 20, len(its)
    return {"title": "Whole number ÷ proper fraction", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def add(qq, correct, cands, e):
        its.append(mcq(qq, correct, cands, e))

    # 1 servings
    add("A bag holds 3 cups of trail mix. One serving is %s cup. How many servings are in the bag?" % fr(1, 4),
        ("12 servings", F(12)),
        [(fr(3, 4) + " serving", F(3, 4)), ("4 servings", F(4)), ("7 servings", F(7))],
        "How many %s cups are in 3 cups? %s. " % (fr(1, 4), dv(3, 1, 4)) + wu_e(3, 4).replace("<b>12</b>", "<b>12</b> servings"))
    # 2 field trip
    add("There are 24 students in a Grade 6 class. %s of them go on the field trip to the science centre. "
        "How many students go?" % fr(2, 3),
        ("16 students", F(16)), of_wrongs(2, 3, 24, ["one", "unshaded", "times", "swap"], unit="students"),
        of_e(2, 3, 24, unit="students"))
    # 3 maple syrup bottles
    add("A sugar shack has 6 L of maple syrup. It fills bottles that each hold %s L. How many bottles can it fill?" % fr(3, 4),
        ("8 bottles", F(8)),
        [("4 %s bottles" % fr(1, 2), F(9, 2)), ("24 bottles", F(24)), ("2 bottles", F(2))],
        wp_e(6, 3, 4, "%s. " % dv(6, 3, 4)).replace("<b>8</b>", "<b>8</b> bottles"))
    # 4 skating practice
    nm, he, his = P.next()
    add("%s practises skating for %s h a day, 6 days a week. How many hours is that each week?" % (nm, fr(3, 4)),
        S(F(9, 2), "h"), [R(18, 24, "h"), S(F(18), "h"), S(F(27, 4), "h"), S(F(8), "h")],
        "6 × %s: " % fr(3, 4) + nf_e(6, 3, 4).replace("</b>.", " h</b>."))
    # 5 Terry Fox Run
    nm, he, his = P.next()
    add("The Terry Fox Run route at %s’s school is 5 km. %s has run %s of the route. How far has %s run?"
        % (nm, cap(he), fr(3, 5), he),
        ("3 km", F(3)), of_wrongs(3, 5, 5, ["unshaded", "times", "one"], unit="km"),
        of_e(3, 5, 5, unit="km"))
    # 6 toque sale
    nm, he, his = P.next()
    add("A toque costs $24. In a sale, %s pays %s of the price. How much does %s pay?" % (nm, fr(3, 4), he),
        ("$18", F(18)), of_wrongs(3, 4, 24, ["one", "unshaded", "times", "swap"], pre="$"),
        of_e(3, 4, 24, pre="$"))
    # 7 ribbon
    add("A 6 m roll of ribbon is cut into pieces that are each %s m long. How many pieces are there?" % fr(2, 3),
        ("9 pieces", F(9)), [("4 pieces", F(4)), ("18 pieces", F(18)), ("3 pieces", F(3))],
        wp_e(6, 2, 3, "%s. " % dv(6, 2, 3)).replace("<b>9</b>", "<b>9</b> pieces"))
    # 8 canoe trip
    add("A canoe trip is 12 km long. The group paddles %s of the route before lunch. How far do they paddle before lunch?"
        % fr(1, 3),
        ("4 km", F(4)), of_wrongs(1, 3, 12, ["unshaded", "den", "times"], unit="km"),
        of_e(1, 3, 12, unit="km"))
    # 9 pizza
    nm, he, his = P.next()
    add("%s orders 3 pizzas for a team party. Each player gets %s of a pizza. How many players can %s feed?"
        % (nm, fr(3, 8), he),
        ("8 players", F(8)),
        [("1 %s players" % fr(1, 8), F(9, 8)), ("24 players", F(24)), ("1 player", F(1))],
        wp_e(3, 3, 8, "%s. " % dv(3, 3, 8)).replace("<b>8</b>", "<b>8</b> players"))
    # 10 cookies
    add("One batch of maple cookies needs %s cup of flour. How much flour do 4 batches need?" % fr(2, 3),
        S(F(8, 3), "cups"), [R(8, 12, "cup"), S(F(8), "cups"), S(F(14, 3), "cups"), S(F(6), "cups")],
        "4 × %s: " % fr(2, 3) + nf_e(4, 2, 3).replace("</b>.", " cups</b>."))
    # 11 reading
    nm, he, his = P.next()
    add("%s reads for %s h every night. How many nights does it take %s to read for 5 h?" % (nm, fr(1, 4), him(he)),
        ("20 nights", F(20)),
        [("%s night" % fr(5, 4), F(5, 4)), ("4 nights", F(4)), ("9 nights", F(9))],
        "%s. " % dv(5, 1, 4) + wu_e(5, 4).replace("<b>20</b>", "<b>20</b> nights"))
    # 12 bake sale
    add("The Grade 6 bake sale has 45 muffins. %s of them are sold by recess. How many muffins are sold by recess?"
        % fr(3, 5),
        ("27 muffins", F(27)), of_wrongs(3, 5, 45, ["one", "unshaded", "times", "swap"], unit="muffins"),
        of_e(3, 5, 45, unit="muffins"))
    # 13 shelves at the cottage
    nm, he, his = P.next()
    add("At the cottage, %s cuts a 10 m board into shelves that are each %s m long. How many shelves does %s get?"
        % (nm, fr(5, 6), he),
        ("12 shelves", F(12)), [("8 shelves", F(8)), ("60 shelves", F(60)), ("2 shelves", F(2))],
        wp_e(10, 5, 6, "%s. " % dv(10, 5, 6)).replace("<b>12</b>", "<b>12</b> shelves"))
    # 14 water
    nm, he, his = P.next()
    add("%s drinks %s L of water at school each day. How much does %s drink in 5 school days?" % (nm, fr(3, 4), he),
        S(F(15, 4), "L"), [R(15, 20, "L"), S(F(15), "L"), S(F(23, 4), "L"), R(3, 20, "L")],
        "5 × %s: " % fr(3, 4) + nf_e(5, 3, 4).replace("</b>.", " L</b>."))
    # 15 hockey game
    nm, he, his = P.next()
    add("A hockey game has three 20-minute periods. %s is on the ice for %s of the game time. How many minutes is that?"
        % (nm, fr(2, 5)),
        ("24 min", F(24)), of_wrongs(2, 5, 60, ["one", "unshaded", "times", "swap"], unit="min"),
        "The game is 3 × 20 = 60 min. " + of_e(2, 5, 60, unit="min"))
    # 16 reverse: skates
    nm, he, his = P.next()
    add("%s has saved $30. That is %s of the cost of new skates. How much do the skates cost?" % (nm, fr(3, 5)),
        ("$50", F(50)), [("$18", F(18)), ("$10", F(10)), ("$20", F(20))],
        "3 parts are $30, so 1 part is $30 ÷ 3 = $10. The whole cost has 5 parts: 5 × $10 = <b>$50</b>. "
        "Check: %s of $50 = $50 ÷ 5 × 3 = $30." % fr(3, 5))
    # 17 which expression
    add("A 4 L jug of apple cider is poured into cups that each hold %s L. Which expression gives the number of cups?"
        % fr(1, 5),
        (dv(4, 1, 5), None),
        [(nf(4, 1, 5), None), ("%s ÷ 4" % fr(1, 5), None), ("5 ÷ 4", None)],
        "The question asks how many %s L cups fit in 4 L, so divide 4 by %s: <b>%s</b> = 4 × 5 = 20 cups."
        % (fr(1, 5), fr(1, 5), dv(4, 1, 5)))
    # 18 full batches (leftover)
    add("One batch of pancakes needs %s cup of milk. %s has 5 cups of milk. How many <b>full</b> batches can %s make?"
        % (fr(3, 4), "Hana", "she"),
        ("6 batches", F(6)),
        [("7 batches", F(7)), ("3 %s batches" % fr(3, 4), F(15, 4)), ("20 batches", F(20))],
        wp_e(5, 3, 4, "%s. " % dv(5, 3, 4)) + " Only whole batches count, so she can make <b>6 batches</b>.")
    # 19 walking
    nm, he, his = P.next()
    add("%s walks %s km to school and %s km home every day. How far does %s walk in 5 school days?"
        % (nm, fr(3, 4), fr(3, 4), he),
        S(F(15, 2), "km"), [S(F(15, 4), "km"), R(30, 40, "km"), S(F(10), "km"), S(F(35, 4), "km")],
        "Each day: 2 × %s = %s km. In 5 days: 10 × %s. " % (fr(3, 4), fr(6, 4), fr(3, 4))
        + nf_e(10, 3, 4).replace("</b>.", " km</b>."))
    # 20 snow fort
    nm, he, his = P.next()
    add("On a snow day, %s fills buckets of snow to build a fort. Each bucket holds %s of a wheelbarrow load. "
        "How many buckets fill 4 wheelbarrows?" % (nm, fr(2, 5)),
        ("10 buckets", F(10)), [("1 %s buckets" % fr(3, 5), F(8, 5)), ("20 buckets", F(20)), ("2 buckets", F(2))],
        wp_e(4, 2, 5, "%s. " % dv(4, 2, 5)).replace("<b>10</b>", "<b>10</b> buckets"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with fractions", "items": its}


def him(he):
    return "her" if he == "she" else "him"


# ============================================================ lesson
def body_html():
    tape_fig = ("<figure class='sn-fig'>" + tape_svg(12, 2, 3, part_labels=True) +
                "<figcaption>" + fr(2, 3) + " of 12: 12 ÷ 3 = 4 in each part, and 2 parts are 2 × 4 = 8.</figcaption></figure>")
    copies_fig = ("<figure class='sn-fig'>" + copies_svg(5, 3, 4) +
                  "<figcaption>" + nf(5, 3, 4) + ": 5 bars with 3 fourths shaded in each make 15 fourths = 3 "
                  + fr(3, 4) + ".</figcaption></figure>")
    unit_fig = ("<figure class='sn-fig'>" + wholes_svg(3, 4) +
                "<figcaption>" + dv(3, 1, 4) + ": each whole has 4 fourths, so 3 wholes have 12 fourths.</figcaption></figure>")
    group_fig = ("<figure class='sn-fig'>" + wholes_svg(6, 3, 2, numbered=True, PW=20) +
                 "<figcaption>" + dv(6, 2, 3) + ": 6 wholes have 18 thirds. Groups of 2 thirds: 18 ÷ 2 = 9 groups.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p><b>× a fraction means “of”.</b> " + fr(2, 3) + " × 12 means " + fr(2, 3) + " of 12. "
        "<b>÷ a fraction asks “how many of these fit?”</b> " + dv(3, 1, 4) + " asks how many fourths fit in 3. "
        "Multiplying by a proper fraction gives a smaller answer. Dividing by one gives a bigger answer.</p>"
        "<h2>Fraction of a whole number</h2>"
        "<p>Divide by the denominator, then multiply by the numerator.</p>"
        + tape_fig
        + ex("Example", "What is " + fr(3, 5) + " of 40 kg?",
             "40 ÷ 5 = 8 kg in each part. 3 × 8 = 24.", "24 kg")
        + "<h2>Whole number × fraction</h2>"
        "<p>Multiply the whole number by the numerator and keep the denominator. Then change it to a mixed number.</p>"
        + copies_fig
        + ex("Example", nf(7, 2, 3) + " = ?",
             "7 × 2 = 14, so the answer is " + fr(14, 3) + ". 14 ÷ 3 = 4 remainder 2.", "4 " + fr(2, 3))
        + "<h2>Whole number ÷ unit fraction</h2>"
        "<p>Count the pieces. Each whole has as many pieces as the denominator.</p>"
        + unit_fig
        + ex("Example", dv(5, 1, 3) + " = ?", "Each whole has 3 thirds. 5 × 3 = 15.", "15")
        + "<h2>Whole number ÷ proper fraction</h2>"
        "<p>Cut the wholes into pieces, then put the pieces into groups. "
        "Or use the rule: <b>keep the whole number, flip only the fraction you divide by, and multiply</b>.</p>"
        + group_fig
        + ex("Example", dv(6, 2, 3) + " = ?",
             "Flip " + fr(2, 3) + " to " + fr(3, 2) + ". 6 × " + fr(3, 2) + " = " + fr(18, 2) + " = 9. "
             "Check: 9 × " + fr(2, 3) + " = " + fr(18, 3) + " = 6.", "9")
        + table(["Question", "What it asks", "Answer"], [
            [fr(3, 4) + " of 20", "3 of the 4 equal parts of 20", "15"],
            [dv(2, 1, 5), "How many fifths are in 2?", "10"],
            [dv(8, 2, 3), "How many groups of " + fr(2, 3) + " are in 8?", "12"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [dv(3, 1, 4) + " = " + fr(3, 4) + " (thinking dividing always makes a number smaller)",
             "Dividing by a fraction less than 1 gives a bigger answer: there are 12 fourths in 3."],
            [dv(4, 2, 5) + " = " + fr(1, 4) + " × " + fr(2, 5) + " = " + fr(1, 10) + " (flipping the wrong number)",
             "Keep 4, flip only " + fr(2, 5) + ": 4 × " + fr(5, 2) + " = 10."],
            [nf(5, 3, 4) + " = " + fr(15, 20) + " (multiplying the denominator too)",
             "Only multiply the numerator: " + fr(15, 4) + " = 3 " + fr(3, 4) + "."],
            [dv(5, 2, 3) + " = 7 " + fr(1, 3) + " (leftover written as part of a whole)",
             "15 thirds make 7 groups of 2 and 1 third left. 1 third is " + fr(1, 2) + " of a group: 7 " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "How do you multiply a whole number by a fraction in Grade 6?",
     "a": "Multiply the whole number by the numerator and keep the denominator, then simplify. For example, 5 × 3/4 = 15/4 = 3 3/4, and 2/3 of 12 = 12 ÷ 3 × 2 = 8."},
    {"q": "How do you divide a whole number by a fraction?",
     "a": "Keep the whole number, flip only the fraction you divide by, and multiply. For example, 6 ÷ 2/3 = 6 × 3/2 = 9, and 3 ÷ 1/4 = 3 × 4 = 12."},
    {"q": "Why is the answer bigger when you divide by a fraction?",
     "a": "Dividing asks how many pieces fit. A piece smaller than 1 fits more times than 1 does, so 3 ÷ 1/4 = 12 is bigger than 3."},
    {"q": "Is multiplying and dividing with fractions on the Grade 6 EQAO math test?",
     "a": "The Grade 6 EQAO math assessment is based on the Ontario curriculum, and multiplying and dividing whole numbers by fractions is part of the Grade 6 Number strand. Practising fraction word problems like these is good preparation."},
]


def gen():
    rnd = random.Random(36807)
    P = People(rnd)
    sets = [set_times(), set_quantity(), set_unit(), set_proper(P), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "multiplying-and-dividing-with-fractions",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Multiplying and Dividing with Fractions",
        "seo_title": "Grade 6 Multiplying and Dividing with Fractions Worksheets: Fraction of a Number, Whole Number ÷ Fraction (Free, Answer Key, Ontario)",
        "short_title": "Multiplying and dividing with fractions",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide whole numbers by proper fractions, using appropriate tools and strategies",
        "meta_desc": "Free Grade 6 math worksheets on multiplying and dividing whole numbers by fractions for the Ontario curriculum: bar models, fractions of quantities, 3 ÷ 1/4 with pictures, 6 ÷ 2/3 and word problems. 100 questions with an answer key. Great EQAO practice.",
        "key_big": "× a fraction means “of”, so the answer gets smaller. ÷ a fraction asks how many pieces fit, so the answer gets bigger.",
        "key_sub": "2/3 of 12 = 12 ÷ 3 × 2 = 8. 3 ÷ 1/4 = 12, because each whole has 4 fourths. 6 ÷ 2/3 = 6 × 3/2 = 9: flip only the fraction you divide by.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(row of|number line|[0-9]+ wholes?,)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
