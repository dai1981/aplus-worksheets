# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Multiplying Fractions (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p5_multiplying_fractions.py
Primary 5 multiplies a proper/improper fraction and a whole number, a proper fraction and a proper/improper
fraction, two improper fractions, and a mixed number and a whole number (no mixed number × mixed number).
Answers are in simplest form (mixed numbers when greater than 1). Every answer is checked with
fractions.Fraction; no two choices are equal in value; every explanation shows the correct choice in bold.
Wrong answers are real mistakes: multiplying the whole number into the denominator, multiplying the numerator
and the denominator, adding instead of multiplying, adding across, multiplying only the whole part of a mixed
number, (whole + numerator)/denominator, finding a fraction of the whole instead of the remainder.
Word problems use bar models with units (the model method). Helpers adapted from
gen_uk_maths_y5_multiply_fractions.py and gen_cabc_math_g8_mult_div_fractions.py.
Singapore style: British spelling, ℓ, $ and ¢, Singapore names and places. HTML attributes in single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
NBSP = " "
DARK = "#4fae74"      # shaded part
LIGHT = "#d7ecdf"     # light part of an area model
DARKLINE = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
PINK = "#f3c9c4"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
PL = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths",
      9: "ninths", 10: "tenths", 12: "twelfths"}


# ------------------------------------------------------------ helpers
def f(n):
    """Whole number in MOE style: 4536, 10 000 (no-break space)."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NBSP + s[-3:] + out
        s = s[:-3]
    return s + out


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    return "%s %s" % (f(w), fr(a, b))


def show(v):
    """A positive Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return f(q)
    if q == 0:
        return fr(r, v.denominator)
    return mixed(q, r, v.denominator)


def imp(v):
    v = F(v)
    return f(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def plain(h):
    h = re.sub(r"<span class='fr'><span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", h)
    return re.sub("<[^>]+>", "", h)


def R(n, d):
    """A fraction exactly as a student wrote it (not simplified), with its value."""
    return (fr(n, d), F(n, d))


def S(v):
    return (show(v), F(v))


def M(w, a, b):
    return (mixed(w, a, b), w + F(a, b))


def U(c, unit):
    """Add a unit after a (html, value) choice."""
    if not unit or c[1] is None:
        return c
    return ("%s %s" % (c[0], unit), c[1])


def mcq(q, correct, cands, e):
    """correct / cands: (html, value). value None = not a number. Candidates equal in value to an earlier
    choice (or not positive) are skipped. Positions are set later by balance()."""
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


def rot(order, i):
    i %= len(order)
    return order[i:] + order[:i]


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


def mul(x, y):
    return "%s × %s" % (x, y)


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(t, fs):
    return len(t) * fs * 0.6


def bar(x0, y0, BW, BH, b, k):
    return "".join("<rect x='%.1f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                   % (x0 + i * BW / float(b), y0, BW / float(b), BH, DARK if i < k else "#fff", LINE)
                   for i in range(b))


def groups_svg(n, a, b, BW=96, BH=34, GX=18, GY=14):
    """n bars (each 1 whole) cut into b parts, a parts of each shaded. Up to 3 bars per row."""
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    s = [bar(6 + (g % cols) * (BW + GX), 6 + (g // cols) * (BH + GY), BW, BH, b, a) for g in range(n)]
    W = cols * BW + (cols - 1) * GX + 12
    H = rows * BH + (rows - 1) * GY + 12
    return svg_wrap(W, H, "".join(s), "%d bars, each cut into %d equal parts with %d shaded" % (n, b, a))


def rows_svg(n, w, a, b, BW=64, BH=26, GX=10, GY=12):
    """n rows; each row shows the mixed number w a/b."""
    s = []
    for r in range(n):
        y0 = 6 + r * (BH + GY)
        for k in range(w + 1):
            s.append(bar(6 + k * (BW + GX), y0, BW, BH, b, b if k < w else a))
    W = (w + 1) * BW + w * GX + 12
    H = n * BH + (n - 1) * GY + 12
    return svg_wrap(W, H, "".join(s), "rows of bars: %d rows, each showing %d and %d/%d" % (n, w, a, b))


def area_svg(a1, b1, a2, b2, S_=150):
    """Area model for a2/b2 × a1/b1: a1 of b1 columns light, a2 of b2 rows of them dark."""
    p = 4
    cw, rh = S_ / float(b1), S_ / float(b2)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (p, p, S_, S_),
         "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (p, p, a1 * cw, S_, LIGHT),
         "<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s'/>" % (p, p, a1 * cw, a2 * rh, DARK)]
    for i in range(1, b1):
        x = p + i * cw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x, p, x, p + S_, LINE))
    for j in range(1, b2):
        y = p + j * rh
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (p, y, p + S_, y, LINE))
    s.append("<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='none' stroke='%s' stroke-width='3.5'/>"
             % (p, p, a1 * cw, a2 * rh, DARKLINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (p, p, S_, S_, LINE))
    return svg_wrap(S_ + 2 * p, S_ + 2 * p, "".join(s),
                    "area model: a square cut into %d columns and %d rows, %d columns light, %d by %d dark"
                    % (b1, b2, a1, a1, a2))


def model_svg(rows, BW=330, fs=15):
    """Bar model. rows: list of dicts with
         name   - label on the left ('' for none)
         x0     - start in units (default 0)
         cells  - list of (width in units, fill)
         top    - label for a bracket over the whole row (or None)
         above  - list of (first cell, last cell, label) brackets above
         below  - list of (first cell, last cell, label) brackets below
       All rows share one unit length, so equal amounts have equal lengths."""
    total = max(r.get("x0", 0) + sum(w for w, _ in r["cells"]) for r in rows)
    LW = max([tw(r["name"], fs) for r in rows] + [0])
    LW = LW + 10 if LW else 0
    u = BW / float(total)
    X0 = 6 + LW
    s = []
    y = 4
    lab_w = []

    def brack(x0, x1, yb, up, label):
        d = -8 if up else 8
        s.append("<path d='M%.1f %.1f V%.1f H%.1f V%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (x0 + 1, yb, yb + d, x1 - 1, yb, LINE))
        ty = yb + d - 6 if up else yb + d + fs + 2
        s.append(text((x0 + x1) / 2.0, ty, label, fs, RED if label == "?" else LINE))
        lab_w.append(((x0 + x1) / 2.0 - tw(label, fs) / 2, (x0 + x1) / 2.0 + tw(label, fs) / 2))

    BH = 30
    for r in rows:
        ab = list(r.get("above", []))
        tiers = (1 if r.get("top") is not None else 0) + (1 if ab else 0)
        TH = 8 + 6 + fs + 2
        y += tiers * TH if tiers else 2
        xs = [X0 + r.get("x0", 0) * u]
        for w, _ in r["cells"]:
            xs.append(xs[-1] + w * u)
        for i, (w, col) in enumerate(r["cells"]):
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (xs[i], y, w * u, BH, col, LINE))
        if r.get("top") is not None:
            brack(xs[0], xs[-1], y - 3 - (TH if ab else 0), True, r["top"])
        for i0, i1, lab in ab:
            brack(xs[i0], xs[i1 + 1], y - 3, True, lab)
        if r["name"]:
            s.append(text(6, y + BH / 2.0 + fs * 0.35, r["name"], fs, LINE, "start"))
        y += BH
        bl = r.get("below", [])
        for i0, i1, lab in bl:
            brack(xs[i0], xs[i1 + 1], y + 3, False, lab)
        y += (3 + 8 + fs + 6) if bl else 0
        y += 8
    W = X0 + BW + 6
    for a, b in lab_w:
        assert a >= 0 and b <= W, (a, b, W)
    return svg_wrap(W, y, "".join(s), "bar model")


def tape_svg(q, a, b, unit="", part_labels=False):
    """A bar worth q cut into b units, a units shaded."""
    cells = [(1, DARK if i < a else "#fff") for i in range(b)]
    below = [(0, a - 1, "?")] if not part_labels else []
    r = {"name": "", "cells": cells, "top": unit + f(q), "below": below}
    svg = model_svg([r], BW=300)
    if part_labels:
        each = q // b
        add = "".join(text(6 + (i + 0.5) * 300.0 / b, 0, f(each), 15, "#fff" if i < a else LINE) for i in range(b))
        # place the part labels in the middle of the bar (bar starts after the top bracket)
        ybar = 4 + 8 + 6 + 15 + 2
        add = add.replace("y='0.0'", "y='%.1f'" % (ybar + 15 + 5))
        svg = svg.replace("</g></svg>", add + "</g></svg>")
    return svg


# ------------------------------------------------------------ working
def chain_from(n, d, unit=""):
    """'n/d = ... = <b>simplest</b>' starting from n/d as written."""
    v = F(n, d)
    start = fr(n, d) if d != 1 else f(n)
    parts = []
    if d != 1:
        if v.denominator == 1:
            parts.append(f(v.numerator))
        else:
            if gcd(n, d) > 1:
                parts.append(fr(v.numerator, v.denominator))
            if v > 1:
                parts.append(show(v))
    u = (" " + unit) if unit else ""
    if not parts:
        return "<b>%s%s</b>" % (start, u)
    return start + "".join(" = " + p for p in parts[:-1]) + " = <b>%s%s</b>" % (parts[-1], u)


def fw_e(n, a, b, unit="", lead=""):
    """n × a/b (or a/b × n): multiply the numerator, keep the denominator."""
    return (lead + "Multiply the numerator by %d and keep the denominator: %s = %s = %s."
            % (n, mul(fr(a, b), n), fr("%d × %d" % (a, n), b), chain_from(a * n, b, unit)))


def fw_wrongs(n, a, b, order):
    """n × a/b: (html, value) from real mistakes."""
    v = F(n * a, b)
    out = []
    for k in order:
        if k == "bottom":                    # multiplied the whole number into the denominator
            out.append(R(a, n * b))
        elif k == "both":                    # multiplied the numerator and the denominator
            out.append(R(n * a, n * b))
        elif k == "add":                     # added instead of multiplying
            out.append(S(n + F(a, b)))
        elif k == "addtop":                  # added the whole number to the numerator
            out.append(S(F(n + a, b)))
        elif k == "one":                     # stopped at 1 unit
            out.append(S(F(n, b)))
        elif k == "rest":                    # found the unshaded part
            if a < b:
                out.append(S(F((b - a) * n, b)))
        elif k == "nodiv":                   # forgot to divide by the denominator
            out.append(S(n * a))
        elif k == "swap":                    # divided by the numerator, multiplied by the denominator
            out.append(S(F(n * b, a)))
        elif k == "up":                      # one whole too many when changing to a mixed number
            if v.denominator != 1:
                out.append(S(v + 1))
        elif k == "down":
            if v.denominator != 1 and v > 1:
                out.append(S(v - 1))
        else:
            raise ValueError(k)
    return out


def ff_chain(x, y, cancel, unit=""):
    """x × y, both fractions (improper allowed). Working that ends in <b>simplest</b>."""
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    steps = []
    if cancel:
        g1, g2 = gcd(a, d), gcd(c, b)
        for g, p, q in ((g1, a, d), (g2, c, b)):
            if g > 1:
                steps.append(("the %ds cancel" % p) if p == q else ("divide %d and %d by %d" % (p, q, g)))
        a, d = a // g1, d // g1
        c, b = c // g2, b // g2
    if steps:
        s = "Simplify first: " + ", and ".join(steps) + ". Now %s = %s." % (
            mul(imp(F(a, b)), imp(F(c, d))),
            chain_from(a * c, b * d, unit))
    else:
        s = "Multiply the numerators and multiply the denominators: %s = %s = %s." % (
            mul(fr(a, b), fr(c, d)), fr("%d × %d" % (a, c), "%d × %d" % (b, d)), chain_from(a * c, b * d, unit))
    return s


def ff_wrongs(x, y, order):
    x, y = F(x), F(y)
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    v = x * y
    out = []
    for k in order:
        if k == "addfr":                     # added across
            out.append(F(a + c, b + d))
        elif k == "cross":                   # cross-multiplied
            out.append(F(a * d, b * c))
        elif k == "add":                     # added the fractions
            out.append(x + y)
        elif k == "addden":                  # multiplied the numerators, added the denominators
            out.append(F(a * c, b + d))
        elif k == "sameden":                 # kept one denominator, as when adding
            out.append(F(a * c, b))
        elif k == "numnum":                  # divided two numerators by a common factor
            g = gcd(a, c)
            if g > 1:
                out.append(F((a // g) * (c // g), b * d))
        elif k == "up":
            if v.denominator != 1:
                out.append(v + 1)
        elif k == "drop":                    # dropped the fraction part
            if v > 1 and v.denominator != 1:
                out.append(F(v.numerator // v.denominator))
        else:
            raise ValueError(k)
    return [S(t) for t in out]


def mx_e(n, w, a, b, unit=""):
    N = w * b + a
    return ("Change %s to an improper fraction: %d × %d + %d = %d, so %s = %s. Then %s = %s = %s."
            % (mixed(w, a, b), w, b, a, N, mixed(w, a, b), fr(N, b), mul(fr(N, b), n), fr("%d × %d" % (N, n), b),
               chain_from(N * n, b, unit)))


def mx_wrongs(n, w, a, b, order):
    v = n * w + F(n * a, b)
    out = []
    for k in order:
        if k == "whole":                     # multiplied only the whole number part
            out.append(n * w + F(a, b))
        elif k == "frac":                    # multiplied only the fraction part
            out.append(w + F(n * a, b))
        elif k == "add":                     # added the whole number
            out.append(w + n + F(a, b))
        elif k == "lost":                    # forgot the whole made by the fraction part
            if n * a >= b and (n * a) % b:
                out.append(n * w + F(n * a % b, b))
        elif k == "badimp":                  # w a/b written as (w + a)/b
            out.append(F(w + a, b) * n)
        elif k == "up":
            out.append(v + 1)
        else:
            raise ValueError(k)
    return [S(t) for t in out]


def ask(expr, v, simp=True):
    q = "%s = <b>?</b>" % expr
    v = F(v)
    if v.denominator != 1 and v > 1:
        q += "<br>Give your answer as a mixed number in its simplest form."
    elif v.denominator != 1 and simp:
        q += "<br>Give your answer in its simplest form."
    return q


# ============================================================ set 1: fraction × whole number
def set_frac_whole(P):
    its = []
    # A) bar models: fraction of a whole number
    for i, (a, b, q) in enumerate([(3, 4, 12), (2, 3, 15), (4, 5, 20), (5, 6, 18), (3, 8, 24)]):
        p = q // b
        qq = fig(tape_svg(q, a, b)) + "The model shows %s. What is %s?" % (mul(fr(a, b), q), mul(fr(a, b), q))
        e = ("%s means %s of %d. %d units = %d, so 1 unit = %d ÷ %d = %d. %d units = %d × %d = <b>%d</b>."
             % (mul(fr(a, b), q), fr(a, b), q, b, q, q, b, p, a, a, p, a * p))
        order = rot(["one", "bottom", "nodiv", "add", "rest", "swap"], i)
        its.append(mcq(qq, S(a * p), fw_wrongs(q, a, b, order), e))
    # B) pictures: answers greater than 1
    for i, (n, a, b) in enumerate([(3, 2, 5), (4, 3, 4), (5, 2, 3)]):
        qq = (fig(groups_svg(n, a, b)) + "Each bar is 1 whole. There are %d bars with %s shaded in each. "
              "What is %s?" % (n, fr(a, b), mul(fr(a, b), n)))
        e = ("Count the shaded parts: %d × %d = %d %s. So %s = %s."
             % (n, a, n * a, PL[b], mul(fr(a, b), n), chain_from(n * a, b)))
        order = rot(["both", "add", "bottom", "addtop"], i)
        its.append(mcq(qq, S(F(n * a, b)), fw_wrongs(n, a, b, order), e))
    # C) calculate: proper fraction × whole number
    cases = [("fn", 3, 2, 7), ("nf", 5, 3, 8), ("fn", 20, 3, 10), ("fn", 6, 4, 9), ("nf", 18, 5, 6),
             ("fn", 8, 7, 12), ("nf", 9, 2, 3), ("fn", 10, 3, 4)]
    for i, (form, n, a, b) in enumerate(cases):
        expr = mul(fr(a, b), n) if form == "fn" else mul(n, fr(a, b))
        v = F(n * a, b)
        lead = "" if form == "fn" else "%s is the same as %s. " % (expr, mul(fr(a, b), n))
        order = rot(["bottom", "both", "add", "addtop", "up", "nodiv"], i)
        its.append(mcq(ask(expr, v), S(v), fw_wrongs(n, a, b, order), fw_e(n, a, b, lead=lead)))
    # D) improper fraction × whole number
    for i, (n, a, b) in enumerate([(3, 7, 4), (10, 9, 5), (4, 5, 3)]):
        v = F(n * a, b)
        order = rot(["bottom", "add", "both", "up", "down"], i)
        its.append(mcq(ask(mul(fr(a, b), n), v), S(v), fw_wrongs(n, a, b, order), fw_e(n, a, b)))
    # E) find the mistake
    nm, he, his = P.next()
    q = "%s says %s = %s. What mistake did %s make?" % (nm, mul(fr(3, 4), 12), fr(3, 48), he)
    its.append(mcq(q, (cap("%s multiplied the denominator by 12 instead of the numerator." % he), None),
                   [(cap("%s added 12 instead of multiplying." % he), None),
                    (cap("%s forgot to simplify the answer." % he), None),
                    ("There is no mistake.", None)],
                   "%s is smaller than %s, but 12 lots of %s must be more. Multiply the numerator: %s = %s = 9. "
                   "<b>%s multiplied the denominator by 12 instead of the numerator.</b>"
                   % (fr(3, 48), fr(3, 4), fr(3, 4), mul(fr(3, 4), 12), fr(36, 4), cap(he))))
    assert len(its) == 20, len(its)
    return {"title": "Fraction × whole number with models", "items": its}


# ============================================================ set 2: proper × proper (area models)
def set_proper(P):
    its = []
    # A) area models
    for i, (a1, b1, a2, b2) in enumerate([(3, 4, 2, 3), (3, 5, 1, 2), (2, 5, 3, 4), (1, 4, 2, 3)]):
        n, d = a1 * a2, b1 * b2
        v = F(n, d)
        q = (fig(area_svg(a1, b1, a2, b2)) + "The model shows %s of %s. What fraction of the whole square is "
             "dark green? Give your answer in its simplest form." % (fr(a2, b2), fr(a1, b1)))
        cands = [S(F(a1 + a2, b1 + b2)), S(F(n, a1 * b2)), S(F(a1, b1) + F(a2, b2)), S(F(n, d - n)), S(F(a1, b1))]
        e = ("The square is cut into %d × %d = %d equal parts, and %d × %d = %d of them are dark green. "
             "So %s = %s." % (b1, b2, d, a1, a2, n, mul(fr(a2, b2), fr(a1, b1)), chain_from(n, d)))
        its.append(mcq(q, S(v), rot(cands, i), e))
    # B) which multiplication
    a1, b1, a2, b2 = 2, 3, 3, 5
    q = (fig(area_svg(a1, b1, a2, b2)) + "The light green columns are %s of the square. Which multiplication "
         "does the dark green part show?" % fr(a1, b1))
    right = mul(fr(a2, b2), fr(a1, b1))
    cands = [(mul(fr(b2 - a2, b2), fr(a1, b1)), F(b2 - a2, b2) * F(a1, b1)),
             ("%s + %s" % (fr(a2, b2), fr(a1, b1)), F(a2, b2) + F(a1, b1)),
             (mul(fr(a2, b2), fr(b1 - a1, b1)), F(a2, b2) * F(b1 - a1, b1))]
    e = ("The dark green part is %d of the %d rows inside the light green columns, so it is %s of %s: <b>%s</b>."
         % (a2, b2, fr(a2, b2), fr(a1, b1), right))
    its.append(mcq(q, (right, F(a2, b2) * F(a1, b1)), cands, e))
    # C) multiply across
    for i, ((a, b), (c, d)) in enumerate([((1, 2), (1, 3)), ((2, 3), (1, 5)), ((3, 4), (1, 2)), ((2, 5), (3, 7)),
                                          ((3, 4), (3, 5)), ((5, 6), (1, 4)), ((2, 3), (4, 5)), ((3, 8), (3, 8)),
                                          ((4, 7), (2, 3))]):
        x, y = F(a, b), F(c, d)
        order = rot(["addfr", "cross", "add", "addden", "sameden"], i)
        its.append(mcq(ask(mul(fr(a, b), fr(c, d)), x * y), S(x * y), ff_wrongs(x, y, order), ff_chain(x, y, False)))
    # D) simplify the answer
    for i, ((a, b), (c, d)) in enumerate([((3, 5), (5, 9)), ((4, 5), (5, 8)), ((3, 4), (2, 9)), ((5, 6), (3, 10))]):
        x, y = F(a, b), F(c, d)
        order = rot(["addfr", "sameden", "cross", "add", "addden"], i)
        e = ("Multiply the numerators and multiply the denominators: %s = %s. Simplify: %s."
             % (mul(fr(a, b), fr(c, d)), fr(a * c, b * d), chain_from(a * c, b * d)))
        its.append(mcq(ask(mul(fr(a, b), fr(c, d)), x * y), S(x * y), ff_wrongs(x, y, order), e))
    # E) "of" and size
    x, y = F(3, 5), F(5, 6)
    its.append(mcq("Find %s of %s.<br>Give your answer in its simplest form." % (fr(3, 5), fr(5, 6)), S(x * y),
                   ff_wrongs(x, y, ["addfr", "cross", "add"]),
                   "“Of” means ×. %s = %s." % (mul(fr(3, 5), fr(5, 6)), chain_from(15, 30))))
    q = "%s = %s. Which sentence is true?" % (mul(fr(3, 4), fr(2, 3)), fr(1, 2))
    its.append(mcq(q, ("The answer is smaller than both fractions.", None),
                   [("The answer is greater than both fractions.", None),
                    ("The answer is between the two fractions.", None),
                    ("The answer is equal to one of the fractions.", None)],
                   "%s is less than %s and less than %s. Taking a part of a part gives a smaller amount, so "
                   "<b>the answer is smaller than both fractions.</b>" % (fr(1, 2), fr(3, 4), fr(2, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Proper fraction × proper fraction with area models", "items": its}


# ============================================================ set 3: improper fractions, simplify first
def set_improper(P):
    its = []
    # A) proper × improper
    for i, (x, y) in enumerate([(F(2, 3), F(9, 4)), (F(3, 5), F(10, 7)), (F(4, 7), F(7, 2)), (F(5, 6), F(9, 5)),
                                (F(3, 8), F(12, 5)), (F(5, 9), F(6, 5))]):
        order = rot(["addfr", "cross", "add", "sameden", "drop", "up"], i)
        its.append(mcq(ask(mul(fr(x.numerator, x.denominator), fr(y.numerator, y.denominator)), x * y), S(x * y),
                       ff_wrongs(x, y, order), ff_chain(x, y, True)))
    # B) improper × improper
    for i, (x, y) in enumerate([(F(3, 2), F(5, 4)), (F(7, 3), F(6, 5)), (F(9, 4), F(8, 3)), (F(5, 2), F(7, 5)),
                                (F(10, 3), F(9, 4)), (F(8, 5), F(15, 4)), (F(7, 6), F(9, 7)), (F(11, 4), F(6, 5)),
                                (F(12, 5), F(10, 9)), (F(4, 3), F(3, 4)), (F(9, 2), F(4, 3))]):
        order = rot(["addfr", "cross", "add", "drop", "up", "sameden"], i)
        its.append(mcq(ask(mul(fr(x.numerator, x.denominator), fr(y.numerator, y.denominator)), x * y), S(x * y),
                       ff_wrongs(x, y, order), ff_chain(x, y, True)))
    # C) which can be simplified first
    q = "Which multiplication can be simplified <b>before</b> multiplying?"
    its.append(mcq(q, (mul(fr(4, 9), fr(3, 5)), None),
                   [(mul(fr(2, 5), fr(3, 7)), None), (mul(fr(3, 4), fr(5, 7)), None), (mul(fr(5, 8), fr(3, 7)), None)],
                   "Look for a numerator and a denominator with a common factor. In %s, 3 and 9 share 3: "
                   "<b>%s</b> = %s = %s. The others have no such pair."
                   % (mul(fr(4, 9), fr(3, 5)), mul(fr(4, 9), fr(3, 5)), mul(fr(4, 3), fr(1, 5)), fr(4, 15))))
    # D) wrong cancelling
    nm, he, his = P.next()
    q = ("%s wants to simplify %s before multiplying, so %s divides 6 and 14 by 2. What is wrong?"
         % (nm, mul(fr(6, 35), fr(14, 9)), he))
    its.append(mcq(q, ("6 and 14 are both numerators. Pair a numerator with a denominator.", None),
                   [("Nothing is wrong. Any two numbers with a common factor can be divided.", None),
                    ("%s should divide 6 and 14 by 7." % cap(he), None),
                    ("You can never simplify before multiplying.", None)],
                   "Dividing two numerators changes the value. Pair a numerator with a denominator: 6 and 9 share 3, "
                   "and 14 and 35 share 7. Then %s = %s. <b>6 and 14 are both numerators. Pair a numerator with a "
                   "denominator.</b>" % (mul(fr(2, 5), fr(2, 3)), fr(4, 15))))
    # E) greater than
    q = "Without calculating, which product is <b>greater</b> than %s?" % fr(5, 4)
    its.append(mcq(q, (mul(fr(5, 4), fr(7, 6)), None),
                   [(mul(fr(5, 4), fr(6, 7)), None), (mul(fr(5, 4), fr(1, 2)), None), (mul(fr(5, 4), fr(3, 3)), None)],
                   "Multiplying by a number greater than 1 gives a greater answer. %s is greater than 1, so "
                   "<b>%s</b> is greater than %s. %s = 1, and %s and %s are less than 1."
                   % (fr(7, 6), mul(fr(5, 4), fr(7, 6)), fr(5, 4), fr(3, 3), fr(6, 7), fr(1, 2))))
    assert len(its) == 20, len(its)
    return {"title": "Improper fractions: simplify first, then multiply", "items": its}


# ============================================================ set 4: mixed number × whole number
def set_mixed(P):
    its = []
    # A) pictures
    for i, (n, w, a, b) in enumerate([(3, 2, 1, 4), (2, 1, 2, 5), (4, 1, 1, 3), (3, 2, 3, 4)]):
        q = (fig(rows_svg(n, w, a, b)) + "Each row shows %s. There are %d rows. What is %s?"
             % (mixed(w, a, b), n, mul(mixed(w, a, b), n)))
        e = ("Count the whole bars: %d × %d = %d. Count the shaded %s in the last column: %d × %d = %d. "
             % (n, w, n * w, PL[b], n, a, n * a)) + mx_e(n, w, a, b)
        its.append(mcq(q, S(n * w + F(n * a, b)), mx_wrongs(n, w, a, b, rot(["whole", "badimp", "add", "frac", "up"], i)), e))
    # B) improper fraction first
    for w, a, b in [(2, 3, 4), (3, 2, 5)]:
        N = w * b + a
        q = "To find %s, first write %s as an improper fraction. Which is it?" % (mul(mixed(w, a, b), 3), mixed(w, a, b))
        its.append(mcq(q, (fr(N, b), F(N, b)),
                       [(fr(w + a, b), F(w + a, b)), (fr(w * a, b), F(w * a, b)), (fr(w * b, b), F(w))],
                       "%d wholes are %d × %d = %d %s. Add %d more: %d + %d = %d. So %s = <b>%s</b>."
                       % (w, w, b, w * b, PL[b], a, w * b, a, N, mixed(w, a, b), fr(N, b))))
    # C) calculate
    cases = [(3, 1, 2, 7), (2, 3, 2, 5), (4, 2, 1, 5), (3, 4, 2, 7), (2, 5, 4, 9), (3, 3, 1, 4),
             (2, 4, 5, 8), (3, 1, 2, 5), (5, 1, 1, 2), (4, 2, 3, 4), (3, 3, 5, 6), (6, 1, 2, 3)]
    for i, (n, w, a, b) in enumerate(cases):
        v = n * w + F(n * a, b)
        expr = mul(mixed(w, a, b), n) if i % 2 == 0 else mul(n, mixed(w, a, b))
        lead = "" if i % 2 == 0 else "%s is the same as %s. " % (expr, mul(mixed(w, a, b), n))
        order = rot(["whole", "lost", "badimp", "add", "frac", "up"], i)
        q = ask(expr, v)
        if v.denominator == 1:
            q = "%s = <b>?</b>" % expr
        its.append(mcq(q, S(v), mx_wrongs(n, w, a, b, order), lead + mx_e(n, w, a, b)))
    # D) find the mistake
    nm, he, his = P.next()
    q = "%s says %s = %s. What mistake did %s make?" % (nm, mul(mixed(2, 3, 4), 3), mixed(6, 3, 4), he)
    its.append(mcq(q, (cap("%s multiplied only the whole number part by 3." % he), None),
                   [(cap("%s added 3 instead of multiplying." % he), None),
                    (cap("%s multiplied the denominator by 3." % he), None),
                    ("There is no mistake.", None)],
                   "Both parts must be multiplied: %s = %s = %s, not 6 %s. <b>%s multiplied only the whole "
                   "number part by 3.</b>" % (mul(fr(11, 4), 3), fr(33, 4), mixed(8, 1, 4), fr(3, 4), cap(he))))
    q = "Which is the same as %s?" % mul(mixed(1, 2, 3), 4)
    its.append(mcq(q, (mul(fr(5, 3), 4), F(20, 3)),
                   [(mul(fr(3, 3), 4), F(4)), ("1 × 4 + %s" % fr(2, 3), 4 + F(2, 3)), ("%s + 4" % mixed(1, 2, 3), 5 + F(2, 3))],
                   "%s = %s (1 × 3 + 2 = 5), so %s is the same as <b>%s</b> = %s = %s."
                   % (mixed(1, 2, 3), fr(5, 3), mul(mixed(1, 2, 3), 4), mul(fr(5, 3), 4), fr(20, 3), mixed(6, 2, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Mixed number × whole number", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def fw(q, n, a, b, unit, order):
        v = F(n * a, b)
        e = "Find %s. " % mul(n, fr(a, b)) + fw_e(n, a, b, unit)
        its.append(mcq(q, U(S(v), unit), [U(c, unit) for c in fw_wrongs(n, a, b, order)], e))

    def mx(q, n, w, a, b, unit, order):
        v = n * w + F(n * a, b)
        its.append(mcq(q, U(S(v), unit), [U(c, unit) for c in mx_wrongs(n, w, a, b, order)], mx_e(n, w, a, b, unit)))

    # 1-3 fraction × whole number
    fw("A bottle holds %s ℓ of soya bean milk. How much soya bean milk is there in 6 such bottles?" % fr(3, 4),
       6, 3, 4, "ℓ", ["add", "both", "bottom", "up"])
    nm, he, his = P.next()
    fw("%s uses %s m of ribbon for each gift. %s wraps 7 gifts. How much ribbon does %s use?"
       % (nm, fr(2, 5), cap(he), he), 7, 2, 5, "m", ["both", "add", "addtop", "up"])
    nm, he, his = P.next()
    fw("%s jogs %s km at East Coast Park every morning. How far does %s jog in 5 mornings?" % (nm, fr(7, 10), he),
       5, 7, 10, "km", ["add", "bottom", "both", "down"])
    # 4-6 mixed number × whole number
    mx("A bag of flour has a mass of %s kg. Mdm Wong buys 3 bags. What is the total mass of the flour?" % mixed(2, 1, 4),
       3, 2, 1, 4, "kg", ["whole", "badimp", "add", "up"])
    mx("A durian has a mass of %s kg. What is the total mass of 4 such durians?" % mixed(1, 3, 5),
       4, 1, 3, 5, "kg", ["whole", "lost", "badimp", "add"])
    mx("A tin holds %s ℓ of paint. Mr Rahman needs 6 tins to paint the walls of his HDB flat. "
       "How much paint is that?" % mixed(2, 3, 4), 6, 2, 3, 4, "ℓ", ["lost", "whole", "badimp", "add"])
    # 7-8 fraction of a quantity (models)
    q = (fig(model_svg([{"name": "", "cells": [(1, DARK if i < 3 else "#fff") for i in range(8)], "top": "40",
                         "below": [(0, 2, "?")]}])) +
         "There are 40 students in a Primary 5 class. %s of them join a sports CCA. How many students join a sports CCA?"
         % fr(3, 8))
    its.append(mcq(q, ("15 students", F(15)), [("5 students", F(5)), ("25 students", F(25)), ("120 students", F(120)),
                                               ("107 students", F(107))],
                   "8 units = 40, so 1 unit = 40 ÷ 8 = 5. 3 units = 3 × 5 = <b>15 students</b>."))
    nm, he, his = P.next()
    q = (fig(model_svg([{"name": "", "cells": [(1, DARK if i < 2 else "#fff") for i in range(5)], "top": "$60",
                         "below": [(0, 1, "spent"), (2, 4, "?")]}])) +
         "%s had $60. %s spent %s of it on a storybook. How much money did %s have left?" % (nm, cap(he), fr(2, 5), he))
    its.append(mcq(q, ("$36", F(36)), [("$24", F(24)), ("$12", F(12)), ("$150", F(150)), ("$58", F(58))],
                   "5 units = $60, so 1 unit = $60 ÷ 5 = $12. %s spent 2 units, so 3 units are left: "
                   "3 × $12 = <b>$36</b>." % cap(he)))
    # 9-11 fraction × fraction
    nm, he, his = P.next()
    x, y = F(2, 3), F(3, 4)
    its.append(mcq("%s had a ribbon %s m long. %s used %s of it to tie a bow. What length of ribbon did %s use?"
                   % (nm, fr(3, 4), cap(he), fr(2, 3), he), U(S(x * y), "m"),
                   [U(c, "m") for c in ff_wrongs(x, y, ["addfr", "add", "cross", "sameden"])],
                   "%s of %s m is %s. %s" % (fr(2, 3), fr(3, 4), mul(fr(2, 3), fr(3, 4)), ff_chain(x, y, True, "m"))))
    x, y = F(1, 2), F(4, 5)
    its.append(mcq("Mr Tan planted vegetables on %s of his garden. Chilli plants cover %s of the vegetable part. "
                   "What fraction of the whole garden is covered by chilli plants?<br>Give your answer in its simplest form."
                   % (fr(4, 5), fr(1, 2)), S(x * y), ff_wrongs(x, y, ["addfr", "add", "cross", "addden"]),
                   "%s of %s is %s. %s" % (fr(1, 2), fr(4, 5), mul(fr(1, 2), fr(4, 5)), ff_chain(x, y, False))))
    x, y = F(5, 4), F(6, 5)
    its.append(mcq("A rectangular mat is %s m long and %s m wide. What is its area?" % (fr(5, 4), fr(6, 5)),
                   U(S(x * y), "m²"), [U(c, "m²") for c in ff_wrongs(x, y, ["add", "addfr", "drop", "cross"])],
                   "Area = length × width = %s. %s" % (mul(fr(5, 4), fr(6, 5)), ff_chain(x, y, True, "m²"))))
    # 12 remainder: $200, 2/5 then 1/4 of the remainder
    nm, he, his = P.next()
    cells = [(4, DARK), (4, DARK)] + [(1, RED if i < 3 else "#fff") for i in range(12)]
    cells = [(w, PINK if c == RED else c) for w, c in cells]
    q = (fig(model_svg([{"name": "", "cells": cells, "top": "$200",
                         "below": [(0, 1, "bag"), (2, 4, "?"), (5, 13, "left")]}])) +
         "%s had $200. %s spent %s of it on a bag and %s of the remainder on a book. How much did %s spend on the book?"
         % (nm, cap(he), fr(2, 5), fr(1, 4), he))
    its.append(mcq(q, ("$30", F(30)), [("$50", F(50)), ("$80", F(80)), ("$90", F(90)), ("$110", F(110))],
                   "Cut the whole into 5 parts. The bag is 2 parts, and the remainder is 3 parts. Cut each part into 4 "
                   "units, so the whole is 20 units and the remainder is 12 units. %s of 12 units = 3 units. "
                   "20 units = $200, so 1 unit = $10. The book cost 3 × $10 = <b>$30</b>." % fr(1, 4)))
    # 13 two-row model: 360 students, 3/5 girls, 1/4 of girls
    girls = {"name": "Girls", "cells": [(3, PINK if i == 0 else DARK) for i in range(4)], "below": [(0, 0, "?")]}
    allp = {"name": "Students", "cells": [(4, DARK if i < 3 else "#fff") for i in range(5)], "top": "360",
            "below": [(0, 2, "girls")]}
    q = (fig(model_svg([allp, girls], BW=290)) +
         "There are 360 students in the hall. %s of them are girls. %s of the girls wear spectacles. "
         "How many girls wear spectacles?" % (fr(3, 5), fr(1, 4)))
    its.append(mcq(q, ("54 girls", F(54)), [("90 girls", F(90)), ("216 girls", F(216)),
                                            ("162 girls", F(162)), ("72 girls", F(72))],
                   "Girls: 5 units = 360, so 1 unit = 72 and 3 units = 216 girls. %s of 216 = 216 ÷ 4 = 54. "
                   "(Or %s of %s = %s, and %s of 360 = 54.) So <b>54 girls</b> wear spectacles."
                   % (fr(1, 4), fr(1, 4), fr(3, 5), fr(3, 20), fr(3, 20))))
    # 14 curry puffs: 120, 3/4 then 2/3 of the remainder, how many left
    cells = [(3, DARK)] * 3 + [(1, PINK), (1, PINK), (1, "#fff")]
    q = (fig(model_svg([{"name": "", "cells": cells, "top": "120",
                         "above": [(3, 4, "afternoon")], "below": [(0, 2, "morning"), (5, 5, "?")]}])) +
         "Mrs Ng made 120 curry puffs. She sold %s of them in the morning and %s of the remainder in the afternoon. "
         "How many curry puffs were left?" % (fr(3, 4), fr(2, 3)))
    its.append(mcq(q, ("10 curry puffs", F(10)), [("20 curry puffs", F(20)), ("30 curry puffs", F(30)),
                                                  ("40 curry puffs", F(40)), ("80 curry puffs", F(80))],
                   "The remainder is %s of 120 = 30. She sold %s of 30 = 20 in the afternoon, so 30 − 20 = 10 were left. "
                   "In units: 12 units = 120, 1 unit = 10, and 1 unit is left. <b>10 curry puffs</b> were left."
                   % (fr(1, 4), fr(2, 3))))
    # 15 durians: 72, 5/8 Saturday, 2/3 of remainder Sunday
    cells = [(1, DARK)] * 5 + [(1, PINK)] * 2 + [(1, "#fff")]
    q = (fig(model_svg([{"name": "", "cells": cells, "top": "72",
                         "below": [(0, 4, "Saturday"), (5, 6, "?")]}])) +
         "A fruit seller had 72 durians. He sold %s of them on Saturday and %s of the remainder on Sunday. "
         "How many durians did he sell on Sunday?" % (fr(5, 8), fr(2, 3)))
    its.append(mcq(q, ("18 durians", F(18)), [("48 durians", F(48)), ("27 durians", F(27)), ("45 durians", F(45)),
                                              ("9 durians", F(9))],
                   "The remainder is 3 of the 8 units. %s of 3 units = 2 units. 8 units = 72, so 1 unit = 9. "
                   "On Sunday he sold 2 × 9 = <b>18 durians</b>." % fr(2, 3)))
    # 16 time
    nm, he, his = P.next()
    x, y = F(1, 3), F(3, 4)
    its.append(mcq("%s spends %s h on homework every day. %s of that time is spent on maths. "
                   "How many minutes does %s spend on maths?" % (nm, fr(3, 4), fr(1, 3), he),
                   ("15 min", F(15)), [("20 min", F(20)), ("45 min", F(45)), ("30 min", F(30)), ("25 min", F(25))],
                   "%s = %s h. 1 h = 60 min, so %s h = 60 ÷ 4 = <b>15 min</b>."
                   % (mul(fr(1, 3), fr(3, 4)), fr(1, 4), fr(1, 4))))
    # 17 money: 2 3/4 m of cloth at $6 per metre
    its.append(mcq("A shop sells cloth at $6 per metre. Mrs Lim buys %s m of cloth. How much does she pay?" % mixed(2, 3, 4),
                   ("$16.50", F(33, 2)), [("$12.75", F(51, 4)), ("$12", F(12)), ("$18", F(18)), ("$15", F(15))],
                   "%s = %s = %s = %s. %s of $1 is 50¢, so she pays <b>$16.50</b>."
                   % (mul(mixed(2, 3, 4), 6), mul(fr(11, 4), 6), fr(66, 4), mixed(16, 1, 2), fr(1, 2))))
    # 18 mandarin oranges
    mx("Mr Kumar buys 4 boxes of mandarin oranges for Chinese New Year. Each box has a mass of %s kg. "
       "What is the total mass of the 4 boxes?" % mixed(4, 1, 2), 4, 4, 1, 2, "kg", ["whole", "badimp", "add", "up"])
    # 19 fraction of a fraction of a quantity
    its.append(mcq("There are 36 students in a class. %s of them went to the Singapore Zoo. %s of these students "
                   "watched the animal feeding show. How many students watched the show?" % (fr(2, 3), fr(3, 4)),
                   ("18 students", F(18)), [("24 students", F(24)), ("27 students", F(27)), ("6 students", F(6)),
                                            ("9 students", F(9))],
                   "%s of 36 = 36 ÷ 3 × 2 = 24 students went to the zoo. %s of 24 = 24 ÷ 4 × 3 = <b>18 students</b>. "
                   "(Or %s = %s, and %s of 36 = 18.)" % (fr(2, 3), fr(3, 4), mul(fr(3, 4), fr(2, 3)), fr(1, 2), fr(1, 2))))
    # 20 find the whole
    nm, he, his = P.next()
    cells = [(1, DARK), (1, PINK), (1, "#fff"), (1, "#fff")]
    q = (fig(model_svg([{"name": "", "cells": cells, "top": "?",
                         "below": [(0, 0, "brother"), (1, 1, "friends"), (2, 3, "30")]}])) +
         "%s gave %s of %s stickers to %s brother and %s of the remainder to %s friends. %s had 30 stickers left. "
         "How many stickers did %s have at first?" % (nm, fr(1, 4), his, his, fr(1, 3), his, cap(he), he))
    its.append(mcq(q, ("60 stickers", F(60)), [("72 stickers", F(72)), ("45 stickers", F(45)), ("40 stickers", F(40)),
                                               ("120 stickers", F(120))],
                   "The brother got 1 of 4 units, so the remainder is 3 units. %s of the remainder = 1 unit went to the "
                   "friends, so 2 units are left. 2 units = 30, so 1 unit = 15. At first: 4 × 15 = <b>60 stickers</b>. "
                   "(Do not find %s of the whole for the friends: that gives 72.)" % (fr(1, 3), fr(1, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    tape_fig = ("<figure class='sn-fig'>" + tape_svg(12, 3, 4, part_labels=True) +
                "<figcaption>" + mul(fr(3, 4), 12) + ": 4 units = 12, so 1 unit = 3, and 3 units = 9."
                "</figcaption></figure>")
    area_fig = ("<figure class='sn-fig'>" + area_svg(3, 4, 2, 3) +
                "<figcaption>" + fr(2, 3) + " of " + fr(3, 4) + ": 6 of the 12 equal parts are dark green, so "
                + mul(fr(2, 3), fr(3, 4)) + " = " + fr(6, 12) + " = " + fr(1, 2) + ".</figcaption></figure>")
    rows_fig = ("<figure class='sn-fig'>" + rows_svg(3, 2, 3, 4) +
                "<figcaption>3 rows of " + mixed(2, 3, 4) + ": 6 wholes and 9 quarters. 9 quarters = "
                + mixed(2, 1, 4) + ", so " + mul(mixed(2, 3, 4), 3) + " = " + mixed(8, 1, 4) + ".</figcaption></figure>")
    cells = [(4, DARK), (4, DARK)] + [(1, PINK if i < 3 else "#fff") for i in range(12)]
    model_fig = ("<figure class='sn-fig'>" + model_svg([{"name": "", "cells": cells, "top": "$200",
                                                         "below": [(0, 1, "bag"), (2, 4, "book"), (5, 13, "left")]}]) +
                 "<figcaption>" + fr(2, 5) + " on a bag, then " + fr(1, 4) + " of the remainder on a book: "
                 "20 units = $200, and the book is 3 units = $30.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>To multiply fractions, <b>multiply the numerators and multiply the denominators</b>. "
        "A whole number has no denominator to multiply: write 12 as " + fr(12, 1) + ", so only the numerator changes. "
        "Give answers in simplest form, and change improper fractions to mixed numbers.</p>"
        "<h2>Fraction × whole number</h2>"
        "<p>" + mul(fr(3, 4), 12) + " means " + fr(3, 4) + " of 12. Draw a model and use units.</p>"
        + tape_fig
        + ex("Example 1", mul(fr(2, 5), 3) + " = ?",
             "Multiply the numerator: 2 × 3 = 6, and keep the denominator 5. " + fr(6, 5) + " = " + mixed(1, 1, 5) + ".",
             mixed(1, 1, 5))
        + "<h2>Fraction × fraction</h2>"
        "<p>“Of” means ×. The area model shows " + fr(2, 3) + " of " + fr(3, 4) + ".</p>"
        + area_fig
        + ex("Example 2", mul(fr(9, 4), fr(8, 3)) + " = ?",
             "Simplify first: divide 9 and 3 by 3, and divide 8 and 4 by 4. Now 3 × 2 = 6. Always pair a numerator with a denominator.", "6")
        + "<h2>Mixed number × whole number</h2>"
        "<p>Change the mixed number to an improper fraction first. Then multiply.</p>"
        + rows_fig
        + ex("Example 3", mul(mixed(2, 3, 4), 3) + " = ?",
             mixed(2, 3, 4) + " = " + fr(11, 4) + " (2 × 4 + 3 = 11). " + mul(fr(11, 4), 3) + " = " + fr(33, 4)
             + " = " + mixed(8, 1, 4) + ".", mixed(8, 1, 4))
        + "<h2>Word problems: a fraction of the remainder</h2>"
        "<p>Draw the whole, then cut the remainder into equal units. Count the units, find 1 unit, then the answer.</p>"
        + model_fig
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [mul(fr(3, 4), 12) + " = " + fr(3, 48) + " (multiplying the whole number into the denominator)",
             "Multiply the numerator: " + fr(36, 4) + " = 9"],
            [mul(fr(2, 5), 3) + " = " + mixed(3, 2, 5) + " (adding instead of multiplying)",
             "3 lots of " + fr(2, 5) + " = " + fr(6, 5) + " = " + mixed(1, 1, 5)],
            [mul(fr(2, 3), fr(4, 5)) + " = " + fr(6, 8) + " (adding across)",
             "Multiply across: " + fr(8, 15)],
            [mul(mixed(2, 3, 4), 3) + " = " + mixed(6, 3, 4) + " (multiplying only the whole number part)",
             mul(fr(11, 4), 3) + " = " + mixed(8, 1, 4)],
            ["Finding " + fr(1, 4) + " of the whole instead of " + fr(1, 4) + " of the remainder",
             "Use the remainder as the new whole in the model"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 multiplying fractions?",
     "a": "Primary 5 students multiply a fraction by a whole number, a proper fraction by a proper or improper "
          "fraction, two improper fractions, and a mixed number by a whole number, without a calculator. "
          "They also solve word problems such as finding a fraction of a remainder."},
    {"q": "How do I explain multiplying fractions to my child?",
     "a": "Start with “of”: 2/3 × 3/4 means 2/3 of 3/4, and an area model shows 6 of 12 parts, which is 1/2. "
          "Then show the rule: multiply the numerators and multiply the denominators."},
    {"q": "What is the most common mistake?",
     "a": "Multiplying the whole number into the denominator, such as 3/4 × 12 = 3/48. The whole number multiplies "
          "only the numerator, so 3/4 × 12 = 36/4 = 9. Another is multiplying only the whole number part of a mixed number."},
    {"q": "Is multiplying fractions in the MOE syllabus for Primary 5?",
     "a": "Yes. It is part of Fractions in the MOE 2021 Primary Mathematics Syllabus for Primary 5. "
          "Fraction word problems like these also appear in Primary 6 and the PSLE."},
]


def gen():
    rnd = random.Random(65806)
    P = People(rnd)
    sets = [set_frac_whole(P), set_proper(P), set_improper(P), set_mixed(P), set_words(P)]
    for s in sets:
        for it in s["items"]:
            if it.pop("_num"):
                assert ("<b>%s</b>" % it["c"][0]) in it["e"], (it["q"], it["c"][0], it["e"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(plain(x) for x in it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "multiplying-fractions",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Multiplying Fractions",
        "seo_title": "P5 Multiplying Fractions Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplying fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplying a proper/improper fraction and a whole number, a proper fraction and a "
                         "proper/improper fraction, two improper fractions, and a mixed number and a whole number",
        "meta_desc": "Free P5 maths practice: multiply fractions by whole numbers, fractions and mixed numbers, "
                     "with area and bar models. 100 questions with answers (MOE syllabus).",
        "key_big": "Multiply the numerators and multiply the denominators. A whole number multiplies only the numerator.",
        "key_sub": "3/4 × 12 = 36/4 = 9, not 3/48. 2 3/4 × 3 = 11/4 × 3 = 33/4 = 8 1/4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(\\d+ bars|bar model|rows of bars)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
