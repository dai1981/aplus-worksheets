# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Adding and Subtracting Mixed Numbers
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 5: Fractions)
  python3 tools/gen_sg_maths_p5_mixed_numbers.py
Like and unlike denominators, renaming 1 whole, answers in simplest form, and word problems
with bar models. Every answer is in simplest form; wrong choices come from real mistakes
and are also in simplest form. A wrong choice is never equal in value to the right answer or
to another choice. Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
FILL3 = "#8fb8e8"     # bar models
RED = "#c0392b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 12: "twelfths", 15: "fifteenths", 20: "twentieths", 24: "twenty-fourths"}
SIMPLE = "<br>Give your answer in its simplest form."


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mx(w, n, d):
    """Whole part w and fraction n/d written as given."""
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def show(v):
    """A positive Fraction in simplest form: '7/12', '1 1/6', '2'."""
    w, r = divmod(v.numerator, v.denominator)
    return mx(w, r, v.denominator)


def val(x):
    w, n, d = x
    return Fraction(w) + Fraction(n, d)


def tup(v):
    w, r = divmod(v.numerator, v.denominator)
    return (w, r, v.denominator)


def lcm(a, b):
    return a * b // math.gcd(a, b)


M = " m"
L_ = " ℓ"
H = " h"
KG = " kg"
KM = " km"


def withu(v, unit):
    return show(v) + (unit or "")


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ helpers
class Spots:
    """Where the right answer goes: A-D used equally often, in a shuffled order."""
    def __init__(self):
        self.left = []

    def next(self, rnd):
        if not self.left:
            self.left = [0, 1, 2, 3]
            rnd.shuffle(self.left)
        return self.left.pop()


SPOTS = Spots()


def mcq(q, correct, cands, e, rnd, unit=None):
    """correct is a Fraction (shown in simplest form, with unit) or a string.
    cands are Fractions or strings. A Fraction equal to the answer, another choice, zero or less is skipped."""
    if isinstance(correct, Fraction):
        cv, cs = correct, withu(correct, unit)
    else:
        cv, cs = None, correct
    seen, vals, pick = {cs}, set(), []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, Fraction):
            if c <= 0 or c == cv or c in vals:
                continue
            vals.add(c)
            c = withu(c, unit)
        if c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    rnd.shuffle(pick)
    pos = SPOTS.next(rnd)
    ch = pick[:pos] + [cs] + pick[pos:]
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their parts stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ SVG text
def txt(x, y, s, size=15, anchor="middle", weight="700", color=LINE):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, color, anchor, s))


def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return (txt(x, y, a, size, color=color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            % (x - w / 2, y + 5, x + w / 2, y + 5, color) + txt(x, y + size + 5, b, size, color=color))


def lab_w(lab, unit, size=15):
    """Width of a label drawn by lab_svg. lab is (w, n, d) or a string."""
    if isinstance(lab, str):
        return size * 0.62 * len(lab)
    w, n, d = lab
    t = 0
    if w:
        t += size * 0.62 * len(str(w)) + 3
    if n:
        t += size * 0.62 * max(len(str(n)), len(str(d))) + 4
    if unit:
        t += size * 0.55 * len(unit) + 3
    return t


def lab_svg(cx, yc, lab, unit, size=15):
    """Mixed number with unit (or a string such as '?') centred at cx; yc is the middle line."""
    if isinstance(lab, str):
        return txt(cx, yc + size * 0.36, lab, size + 2)
    w, n, d = lab
    x = cx - lab_w(lab, unit, size) / 2
    s = []
    if w:
        ww = size * 0.62 * len(str(w))
        s.append(txt(x, yc + size * 0.36, w, size, anchor="start"))
        x += ww + 3
    if n:
        fw = size * 0.62 * max(len(str(n)), len(str(d))) + 4
        s.append(sfr(x + fw / 2, yc - 5, n, d, size))
        x += fw
    if unit:
        s.append(txt(x + 4, yc + size * 0.36, unit.strip(), size, anchor="start", weight="400"))
    return "".join(s)


def brace(x0, x1, y, up=True):
    """Curly brace from x0 to x1 at height y. up=True: the point is above."""
    m = (x0 + x1) / 2
    k = -8 if up else 8
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f "
            "Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
            % (x0, y, x0, y + k, x0 + 8, y + k, m - 6, y + k, m, y + k, m, y + 2 * k,
               m, y + k, m + 6, y + k, x1 - 8, y + k, x1, y + k, x1, y, LINE))


# ------------------------------------------------------------ pictures
def bar_cells(x0, y0, W, Hh, d, k, col, sw=2.0):
    return "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                   % (x0 + i * W / d, y0, W / d, Hh, col if i < k else "#fff", LINE, sw) for i in range(d))


def dashes(x0, y0, W, Hh, d, L):
    s = []
    for i in range(1, L):
        if (i * d) % L == 0:
            continue
        x = x0 + W * i / L
        s.append("<line x1='%.2f' y1='%.1f' x2='%.2f' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>"
                 % (x, y0 + 2, x, y0 + Hh - 2, LINE))
    return "".join(s)


def two_bars_svg(d1, k1, d2, k2, L, W=264, Hh=40, labels=False):
    """Top bar: k1 of d1 parts (green). Bottom bar: k2 of d2 parts (yellow). Dashed lines cut both into L parts."""
    x0 = 58 if labels else 6
    s = [bar_cells(x0, 6, W, Hh, d1, k1, FILL, 2.2), dashes(x0, 6, W, Hh, d1, L),
         bar_cells(x0, 6 + Hh + 14, W, Hh, d2, k2, FILL2, 2.2), dashes(x0, 6 + Hh + 14, W, Hh, d2, L)]
    s.append("<rect x='%d' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, W, Hh, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, 6 + Hh + 14, W, Hh, LINE))
    if labels:
        g1, g2 = math.gcd(k1, d1), math.gcd(k2, d2)
        s.append(sfr(26, 22, k1 // g1, d1 // g1, 15))
        s.append(sfr(26, 22 + Hh + 14, k2 // g2, d2 // g2, 15))
    return svg_wrap(x0 + W + 6, 2 * Hh + 26, "".join(s),
                    "two bars of the same size: %d of %d parts green and %d of %d parts yellow, dashed lines cut both into %d parts"
                    % (k1, d1, k2, d2, L))


def mixed_rows_svg(rows, BW=62, Hh=26, gap=8):
    """Each row is a mixed number (w, n, d, colour): w full bars, then a bar with n of d parts shaded.
    A label with the mixed number is drawn at the left."""
    nb = max(r[0] + (1 if r[1] else 0) for r in rows)
    x0 = 60
    s = []
    for j, (w, n, d, col) in enumerate(rows):
        y = 6 + j * (Hh + 16)
        s.append(lab_svg(28, y + Hh / 2, (w, n, d), None, 15))
        for i in range(w + (1 if n else 0)):
            x = x0 + i * (BW + gap)
            s.append(bar_cells(x, y, BW, Hh, d, d if i < w else n, col, 1.6))
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.6'/>" % (x, y, BW, Hh, LINE))
    Wt = x0 + nb * (BW + gap) - gap + 6
    Ht = 6 + len(rows) * (Hh + 16) - 16 + 6
    lab = "bars for mixed numbers: " + "; ".join("%d wholes and %d of %d parts" % (w, n, d) for w, n, d, c in rows)
    return svg_wrap(Wt, Ht, "".join(s), lab)


def rename_svg(w, n, d, BW=56, Hh=28, gap=8):
    """w n/d drawn as (w-1) green wholes, then one whole and n/d in yellow inside a dashed box:
    this shows w n/d = (w-1) (d+n)/d."""
    x0 = 6
    s = []
    nb = w + 1
    y = 22
    for i in range(nb):
        x = x0 + i * (BW + gap)
        col = FILL if i < w - 1 else FILL2
        k = d if i < w else n
        s.append(bar_cells(x, y, BW, Hh, d, k, col, 1.6))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.6'/>" % (x, y, BW, Hh, LINE))
    bx = x0 + (w - 1) * (BW + gap) - 4
    bw = 2 * BW + gap + 8
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='6 4' rx='4'/>"
             % (bx, y - 6, bw, Hh + 12, RED))
    s.append(txt(x0 + ((w - 1) * (BW + gap) - gap) / 2, y + Hh + 26, "%d whole%s" % (w - 1, "" if w - 1 == 1 else "s"), 15))
    s.append(txt(bx + bw / 2, y + Hh + 26, "%d %s" % (d + n, WORD[d]), 15, color=RED))
    Wt = x0 + nb * (BW + gap) - gap + 10
    return svg_wrap(Wt, y + Hh + 34, "".join(s),
                    "bar of %d wholes and %d of %d parts, with the last whole and the part inside a dashed box" % (w, n, d))


def model_svg(segs, total, unit, W=300, name=None):
    """Part-whole bar model. segs: list of (value, label) where label is (w, n, d) or '?'.
    total: label for the whole bar, (w, n, d) or '?', shown with a brace above."""
    tv = sum(v for v, _ in segs)
    x0 = 6 if not name else 14 + 8.5 * len(name)
    s = []
    yb = 58
    Hh = 36
    s.append(lab_svg(x0 + W / 2, 16, total, unit))
    s.append(brace(x0, x0 + W, 50, up=True))
    x = x0
    cols = [FILL3, "#ffffff", "#d7e6f7"]
    for i, (v, lab) in enumerate(segs):
        w = W * v / tv
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x, yb, w, Hh, cols[i % 3], LINE))
        s.append(brace(x + 2, x + w - 2, yb + Hh + 6, up=False))
        s.append(lab_svg(x + w / 2, yb + Hh + 38, lab, unit))
        assert lab_w(lab, unit) < w + 6, (lab, w)
        x += w
    if name:
        s.append(txt(6, yb + Hh / 2 + 5, name, 15, anchor="start"))
    lab = "bar model: a whole bar split into %d parts" % len(segs)
    return svg_wrap(x0 + W + 8, yb + Hh + 62, "".join(s), lab)


def compare_svg(rows, diff, unit, W=230, total=None):
    """Comparison bar model. rows: [(name, value, label or None)] (two rows). The longer bar has its extra part
    marked with a dashed line and diff ((w, n, d) or '?') inside it. A known value of the longer bar is written
    to its right; the shorter bar's value is written inside it. total='?' adds a brace on the right."""
    (n1, v1, l1), (n2, v2, l2) = rows
    big = max(v1, v2)
    small = min(v1, v2)
    x0 = 14 + 8.6 * max(len(n1), len(n2))
    Hh = 40
    s = []
    right = x0 + W
    for j, (nm, v, lab) in enumerate(rows):
        y = 8 + j * (Hh + 16)
        w = W * v / big
        s.append(txt(6, y + Hh / 2 + 5, nm, 15, anchor="start"))
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x0, y, w, Hh, FILL3 if j == 0 else FILL2, LINE))
        ws = W * small / big
        if v == big:
            s.append("<line x1='%.2f' y1='%d' x2='%.2f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0 + ws, y, x0 + ws, y + Hh, LINE))
            assert lab_w(diff, unit) < W - ws - 4, (diff, W - ws)
            s.append(lab_svg(x0 + (ws + W) / 2, y + Hh / 2, diff, unit))
            if lab:
                s.append(lab_svg(x0 + W + 8 + lab_w(lab, unit) / 2, y + Hh / 2, lab, unit))
                right = max(right, x0 + W + 12 + lab_w(lab, unit))
        elif lab:
            s.append(lab_svg(x0 + w / 2, y + Hh / 2, lab, unit))
    Ht = 8 + 2 * Hh + 16 + 8
    if total:
        bx = right + 8
        y0, y1 = 8, 8 + 2 * Hh + 16
        m = (y0 + y1) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f "
                 "L%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                 % (bx, y0, bx + 8, y0, bx + 8, y0 + 8, bx + 8, m - 6, bx + 8, m, bx + 16, m,
                    bx + 8, m, bx + 8, m + 6, bx + 8, y1 - 8, bx + 8, y1, bx, y1, LINE))
        s.append(txt(bx + 30, m + 6, total, 17))
        right = bx + 42
    return svg_wrap(right + 6, Ht, "".join(s), "bar model comparing two bars")


# ------------------------------------------------------------ explanation and mistakes
def finish(W, N, L, unit=None):
    """W wholes and N/L (N may be L or more). Convert, simplify, state the answer."""
    t = ""
    if N >= L:
        w2, r = divmod(N, L)
        if r:
            t += "%s is an improper fraction: %s = %s. " % (fr(N, L), fr(N, L), mx(w2, r, L))
        else:
            t += "%s = %d. " % (fr(N, L), w2)
        if W:
            t += "%d + %s = %s. " % (W, mx(w2, r, L), mx(W + w2, r, L))
        W, N = W + w2, r
    g = math.gcd(N, L) if N else 1
    if N and g > 1:
        t += "Simplify: divide the numerator and denominator of %s by %d to get %s. " % (fr(N, L), g, fr(N // g, L // g))
    v = W + Fraction(N, L)
    return t + "The answer is <b>%s</b>." % withu(v, unit), v


def common(d1, d2):
    L = lcm(d1, d2)
    if d1 == d2:
        return "The denominators are the same. "
    if L == max(d1, d2):
        return "%d is a multiple of %d, so use %d as the common denominator. " % (max(d1, d2), min(d1, d2), L)
    return "The lowest common multiple of %d and %d is %d, so use %d as the common denominator. " % (d1, d2, L, L)


def e_calc(x, y, op, unit=None):
    """Step explanation for x op y. x, y = (whole, numerator, denominator)."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    t = common(d1, d2) if n1 else ""
    rw = ["%s = %s" % (mx(w, n, d), mx(w, n * L // d, L)) for w, n, d in (x, y) if d != L and n]
    if rw:
        t += ("Write the equivalent fraction: " if len(rw) == 1 else "Write equivalent fractions: ") + " and ".join(rw) + ". "
    mixed = w1 or w2
    if op == "+":
        if not mixed:
            t += "Add the numerators: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            s, v = finish(0, a + b, L, unit)
        else:
            t += "Add the fractions: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            t += ("Add the whole numbers: %d + %d = %d. " % (w1, w2, w1 + w2)) if (w1 and w2) else "The whole number is %d. " % (w1 + w2)
            s, v = finish(w1 + w2, a + b, L, unit)
        assert v == val(x) + val(y)
    else:
        if not mixed:
            t += "Subtract the numerators: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            s, v = finish(0, a - b, L, unit)
        elif n1 == 0:
            t += ("Rename 1 whole as %s: %d = %s. Subtract the fractions: %s − %s = %s. "
                  "Subtract the whole numbers: %d − %d = %d. "
                  % (fr(L, L), w1, mx(w1 - 1, L, L), fr(L, L), fr(b, L), fr(L - b, L), w1 - 1, w2, w1 - 1 - w2))
            s, v = finish(w1 - 1 - w2, L - b, L, unit)
        elif a >= b:
            t += "Subtract the fractions: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            t += ("Subtract the whole numbers: %d − %d = %d. " % (w1, w2, w1 - w2)) if w2 else "The whole number is %d. " % w1
            s, v = finish(w1 - w2, a - b, L, unit)
        else:
            t += ("%s is less than %s, so rename 1 whole as %s: %s = %s. Subtract the fractions: %s − %s = %s. "
                  % (fr(a, L), fr(b, L), fr(L, L), mx(w1, a, L), mx(w1 - 1, a + L, L), fr(a + L, L), fr(b, L), fr(a + L - b, L)))
            if w2:
                t += "Subtract the whole numbers: %d − %d = %d. " % (w1 - 1, w2, w1 - 1 - w2)
            elif w1 > 1:
                t += "The whole number is %d. " % (w1 - 1)
            s, v = finish(w1 - 1 - w2, a + L - b, L, unit)
        assert v == val(x) - val(y)
    return t + s


def wrong(x, y, op):
    """Wrong answers from real mistakes, most common first."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    right = val(x) + val(y) if op == "+" else val(x) - val(y)
    mixed = w1 or w2
    c = []
    if op == "+":
        W = w1 + w2
        c.append(W + Fraction(n1 + n2, d1 + d2))                 # added numerators and denominators
        if d1 != d2:
            c.append(W + Fraction(n1 + n2, L))                   # changed the denominator but not the numerators
        if a + b >= L:
            c.append(right - 1)                                  # did not add the whole from the improper fraction
        if mixed:
            c.append(Fraction((a + b) % L, L) if (a + b) % L else None)   # forgot the whole numbers
        if d1 != d2:
            c.append(W + Fraction(a + n2, L) if d2 != L else W + Fraction(n1 + b, L))   # changed only one fraction
            c.append(W + Fraction(n1 + n2, d1 * d2))             # multiplied the denominators, kept the numerators
        else:
            c.append(W + Fraction(abs(a - b), L) if a != b else None)   # subtracted the fractions
            c.append(right + 1)
        c.append(W + Fraction(n1 * n2, d1 * d2))                 # multiplied numerators and denominators
    else:
        W = w1 - w2
        if a >= b and n1:
            if d1 != d2 and n1 > n2 and d1 > d2:
                c.append(W + Fraction(n1 - n2, d1 - d2))         # subtracted numerators and denominators
            if d1 != d2:
                c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)   # changed the denominator only
                c.append(W + Fraction(a - n2, L) if d2 != L else W + Fraction(n1 - b, L))   # changed only one fraction
            else:
                c.append(W + Fraction(a + b, L))                 # subtracted the wholes but added the fractions
            if mixed:
                c.append(Fraction(a - b, L) if a != b else None)  # forgot the whole numbers
            c.append(val(x) + val(y))                            # added instead
            if d1 != d2 and n1 != n2:
                c.append(W + Fraction(abs(n1 - n2), abs(d1 - d2)))
            c.append(right + 1)
            c.append(right - 1)
        else:
            c.append(W + Fraction(b - a, L))                     # took the smaller fraction from the larger
            c.append(right + 1)                                  # renamed but did not take 1 from the wholes
            c.append(Fraction(a + L - b, L))                     # forgot the whole numbers
            if L != 10 and 10 + a - b > 0:
                c.append(W - 1 + Fraction(10 + a - b, L))        # renamed 1 whole as 10, like with whole numbers
            if W > 1:
                c.append(W - 1 + Fraction(b - a, L))
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)
            c.append(val(x) + val(y))
    return c


def calc_q(x, y, op, prompt=SIMPLE):
    sym = "+" if op == "+" else "−"
    return "%s %s %s = ?" % (mx(*x), sym, mx(*y)) + prompt


def calc(x, y, op, rnd, prompt=SIMPLE, extra=None):
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    c = wrong(x, y, op)
    if extra:
        c = extra + c
    return mcq(calc_q(x, y, op, prompt), r, c, e_calc(x, y, op), rnd)


def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


def rename_choices(n1, d1, n2, d2, L):
    k1, k2 = L // d1, L // d2
    right = (n1 * k1, n2 * k2)
    cands = [(n1, n2),                                   # changed the denominator only
             (n1 * k2, n2 * k1),                         # multiplied by the wrong number
             (n1 + L - d1, n2 + L - d2),                 # added the same number to the top and bottom
             (n1 * k1, n2), (n1, n2 * k2)]               # changed only one fraction
    return pair(right[0], L, right[1], L), [pair(p, L, q, L) for p, q in cands if (p, q) != right]


def e_rename(n1, d1, n2, d2, L):
    parts = []
    for n, d in ((n1, d1), (n2, d2)):
        k = L // d
        if k == 1:
            parts.append("%s already has the denominator %d" % (fr(n, d), L))
        else:
            parts.append("%d × %d = %d, so multiply the numerator and denominator of %s by %d: %s"
                         % (d, k, L, fr(n, d), k, fr(n * k, L)))
    return ". ".join(parts) + ". The answer is <b>%s</b>." % pair(n1 * L // d1, L, n2 * L // d2, L)


def check_kind(x, y, op, carry=None, rename=None, simplify=None, like=None):
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    assert r > 0
    if like is not None:
        assert (d1 == d2 or n1 == 0 or n2 == 0) == like, (x, y)
    if carry is not None:
        assert (a + b >= L) == carry, (x, y)
    if rename is not None:
        assert (a < b) == rename, (x, y)
    if simplify is not None:
        N = (a + b) % L if op == "+" else ((a - b) % L)
        assert (N != 0 and math.gcd(N, L) > 1 or (op == "+" and a + b >= L)) == simplify, (x, y)


# ============================================================ set 1: like denominators
def set_like(rnd):
    SPOTS.left = []
    its = []
    # A: pictures
    for x, y in [((1, 1, 5), (1, 2, 5)), ((2, 1, 8), (1, 5, 8))]:
        d = x[2]
        q = (fig(mixed_rows_svg([x + (FILL,), y + (FILL2,)])) +
             "The green bars show %s. The yellow bars show %s. What is %s + %s?"
             % (mx(*x), mx(*y), mx(*x), mx(*y)) + SIMPLE)
        e = ("Count the whole bars: %d + %d = %d. Count the shaded %s: %d + %d = %d, so %s. "
             % (x[0], y[0], x[0] + y[0], WORD[d], x[1], y[1], x[1] + y[1], fr(x[1] + y[1], d)))
        r = val(x) + val(y)
        g = math.gcd(x[1] + y[1], d)
        if g > 1:
            e += "Simplify: %s = %s. " % (fr(x[1] + y[1], d), fr((x[1] + y[1]) // g, d // g))
        e += "The answer is <b>%s</b>." % show(r)
        its.append(mcq(q, r, wrong(x, y, "+"), e, rnd))
    # B: add
    for x, y in [((2, 1, 7), (3, 4, 7)), ((4, 2, 9), (1, 5, 9)), ((3, 1, 6), (2, 1, 6)), ((1, 3, 10), (4, 3, 10)),
                 ((5, 3, 8), (2, 1, 8)), ((3, 0, 1), (2, 4, 9)), ((2, 3, 5), (3, 4, 5)), ((1, 5, 6), (3, 5, 6))]:
        if x[1] == 0:
            x = (x[0], 0, y[2])
            r = val(x) + val(y)
            e = "There is no fraction to add to %s. Add the whole numbers: %d + %d = %d. The answer is <b>%s</b>." % (
                fr(y[1], y[2]), x[0], y[0], x[0] + y[0], show(r))
            its.append(mcq(calc_q(x, y, "+"), r,
                           [Fraction(x[0]) + Fraction(y[1], y[2]), r + 1, Fraction(y[0]) + Fraction(y[1] + x[0], y[2])], e, rnd))
            continue
        check_kind(x, y, "+", like=True)
        its.append(calc(x, y, "+", rnd))
    # C: subtract
    for x, y in [((5, 6, 7), (2, 3, 7)), ((6, 7, 9), (4, 2, 9)), ((4, 5, 8), (1, 3, 8)), ((7, 9, 10), (3, 3, 10)),
                 ((3, 5, 6), (3, 1, 6)), ((8, 3, 5), (5, 1, 5)), ((9, 11, 12), (2, 5, 12)), ((6, 3, 4), (4, 0, 1))]:
        if y[1] == 0:
            y = (y[0], 0, x[2])
            r = val(x) - val(y)
            e = "Subtract the whole numbers: %d − %d = %d. The fraction %s stays the same. The answer is <b>%s</b>." % (
                x[0], y[0], x[0] - y[0], fr(x[1], x[2]), show(r))
            its.append(mcq(calc_q(x, y, "-"), r, [Fraction(x[0] - y[0]), val(x) + y[0], val(x) - y[0] + 1], e, rnd))
            continue
        check_kind(x, y, "-", like=True, rename=False)
        its.append(calc(x, y, "-", rnd))
    # D: missing number
    x, r = (2, 3, 8), (5, 7, 8)
    ans = val(r) - val(x)
    assert ans == Fraction(7, 2)
    e = ("Find the missing number by subtracting: %s − %s. Fractions: %s − %s = %s. Whole numbers: 5 − 2 = 3. "
         "%s = %s, so the answer is <b>%s</b>." % (mx(*r), mx(*x), fr(7, 8), fr(3, 8), fr(4, 8), mx(3, 4, 8), mx(3, 1, 2), mx(3, 1, 2)))
    its.append(mcq("%s + <b>?</b> = %s" % (mx(*x), mx(*r)) + SIMPLE, ans,
                   [val(r) + val(x), Fraction(1, 2), Fraction(13, 4), Fraction(9, 2)], e, rnd))
    # E: spot the mistake
    assert Fraction(7, 5) + Fraction(11, 5) == Fraction(18, 5)
    e = ("The parts are fifths, so the denominator stays 5: 2 fifths + 1 fifth = 3 fifths. "
         "1 %s + 2 %s = <b>3 %s</b>. Siti added the denominators too, which gave tenths." % (fr(2, 5), fr(1, 5), fr(3, 5)))
    its.append(mcq("Siti wrote 1 %s + 2 %s = 3 %s. What mistake did she make?" % (fr(2, 5), fr(1, 5), fr(3, 10)),
                   "She added the denominators",
                   ["She forgot to simplify", "She added the whole numbers", "There is no mistake"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Like denominators", "items": its}


# ============================================================ set 2: unlike denominators
def set_unlike(rnd):
    SPOTS.left = []
    its = []
    # A: lowest common denominator
    for x, y in [((2, 1, 4), (1, 1, 6)), ((3, 2, 3), (1, 1, 5)), ((1, 5, 6), (2, 3, 8))]:
        d1, d2 = x[2], y[2]
        L = lcm(d1, d2)
        big, small = max(d1, d2), min(d1, d2)
        mb = ", ".join(str(big * i) for i in range(1, L // big + 1))
        ms = ", ".join(str(small * i) for i in range(1, L // small + 1))
        e = ("Only the fractions need a common denominator. Multiples of %d: %s. Multiples of %d: %s. "
             "The first number in both lists is <b>%d</b>." % (big, mb, small, ms, L))
        if d1 * d2 != L:
            e += " %d × %d = %d also works, but it is not the lowest." % (d1, d2, d1 * d2)
        cands = [d1 * d2 if d1 * d2 != L else None, d1 + d2, big, 2 * L]
        its.append(mcq("To work out %s + %s, you need a common denominator. What is the lowest common denominator?"
                       % (mx(*x), mx(*y)), str(L), [str(v) for v in cands if v], e, rnd))
    # B: fraction bars
    for x, y in [((1, 2, 3), (2, 1, 4)), ((3, 1, 2), (1, 2, 5))]:
        n1, d1, n2, d2 = x[1], x[2], y[1], y[2]
        L = lcm(d1, d2)
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "To work out %s + %s, first write the fractions with a common denominator. The bars show %s (green) and %s (yellow). "
             "The dashed lines split both bars into %s. Which shows both fractions in %s?"
             % (mx(*x), mx(*y), fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
        its.append(mcq(q, r, c, e, rnd))
    # C: add
    for x, y in [((2, 1, 3), (1, 1, 4)), ((1, 1, 2), (3, 1, 5)), ((3, 1, 6), (1, 1, 2)), ((2, 3, 8), (4, 1, 4)),
                 ((1, 1, 6), (2, 3, 4)), ((4, 2, 5), (2, 1, 3)), ((3, 2, 9), (1, 1, 3)), ((5, 1, 4), (1, 3, 5))]:
        check_kind(x, y, "+", like=False, carry=False)
        its.append(calc(x, y, "+", rnd))
    # D: subtract
    for x, y in [((3, 3, 4), (1, 1, 3)), ((5, 5, 6), (2, 1, 2)), ((4, 7, 10), (1, 2, 5)), ((6, 2, 3), (4, 1, 6)),
                 ((7, 5, 8), (3, 1, 4)), ((4, 11, 12), (1, 3, 4)), ((8, 4, 5), (2, 1, 2))]:
        check_kind(x, y, "-", like=False, rename=False)
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Unlike denominators: use a common denominator", "items": its}


# ============================================================ set 3: renaming a whole
def set_rename(rnd):
    SPOTS.left = []
    its = []
    # A: rename with pictures
    for w, n, d, bad in [(4, 1, 5, ["1", "4", "11"]), (3, 1, 4, ["1", "3", "11"])]:
        q = (fig(rename_svg(w, n, d)) +
             "%s = %d %s. What is the missing number?" % (mx(w, n, d), w - 1, fr("<b>?</b>", d)))
        e = ("Rename 1 of the %d wholes as %s. Then there are %d wholes and %s + %s = %s. "
             "So %s = %s, and the missing number is <b>%d</b>."
             % (w, fr(d, d), w - 1, fr(d, d), fr(n, d), fr(d + n, d), mx(w, n, d), mx(w - 1, d + n, d), d + n))
        assert val((w, n, d)) == val((w - 1, d + n, d))
        its.append(mcq(q, str(d + n), bad, e, rnd))
    e = "Rename 1 whole as %s: 5 = 4 + 1 = 4 %s. The missing number is <b>7</b>." % (fr(7, 7), fr(7, 7))
    its.append(mcq("5 = 4 %s. What is the missing number?" % fr("<b>?</b>", 7), "7", ["1", "10", "6"], e, rnd))
    # B: like denominators, rename
    for x, y in [((4, 1, 5), (2, 3, 5)), ((5, 2, 7), (1, 5, 7)), ((6, 1, 4), (3, 3, 4)), ((3, 1, 8), (1, 5, 8)),
                 ((7, 2, 9), (4, 7, 9)), ((5, 3, 10), (2, 7, 10))]:
        check_kind(x, y, "-", like=True, rename=True)
        its.append(calc(x, y, "-", rnd))
    for x, y in [((5, 0, 4), (2, 3, 4)), ((4, 0, 6), (1, 5, 6))]:
        its.append(calc(x, y, "-", rnd))
    # C: unlike denominators, rename
    for x, y in [((3, 1, 4), (1, 2, 3)), ((4, 1, 3), (2, 1, 2)), ((5, 1, 6), (2, 3, 4)), ((6, 2, 5), (3, 1, 2)),
                 ((7, 1, 8), (4, 3, 4)), ((5, 1, 3), (1, 4, 9)), ((6, 1, 6), (2, 2, 3))]:
        check_kind(x, y, "-", like=False, rename=True)
        its.append(calc(x, y, "-", rnd))
    # D: spot the mistake
    assert Fraction(21, 5) - Fraction(13, 5) == Fraction(8, 5)
    e = ("%s is less than %s, so you cannot take %s away from %s. Rename 1 whole: 4 %s = 3 %s. "
         "3 %s − 2 %s = <b>1 %s</b>. Jun Jie took the smaller fraction from the larger one, which gave 2 %s."
         % (fr(1, 5), fr(3, 5), fr(3, 5), fr(1, 5), fr(1, 5), fr(6, 5), fr(6, 5), fr(3, 5), fr(3, 5), fr(2, 5)))
    its.append(mcq("Jun Jie wrote 4 %s − 2 %s = 2 %s. What mistake did he make?" % (fr(1, 5), fr(3, 5), fr(2, 5)),
                   "He took %s from %s instead of renaming" % (fr(1, 5), fr(3, 5)),
                   ["He added the fractions", "He forgot to simplify", "There is no mistake"], e, rnd))
    assert Fraction(25, 4) - Fraction(15, 4) == Fraction(5, 2)
    e = ("Rename 1 whole as %s: 6 %s = 5 %s. Now the first fraction is larger: 5 %s − 3 %s = 2 %s = 2 %s. "
         "The whole number goes down from 6 to 5 when you rename." % (fr(4, 4), fr(1, 4), fr(5, 4), fr(5, 4), fr(3, 4), fr(2, 4), fr(1, 2)))
    its.append(mcq("Which is the correct first step for 6 %s − 3 %s?" % (fr(1, 4), fr(3, 4)),
                   "5 %s − 3 %s" % (fr(5, 4), fr(3, 4)),
                   ["6 %s − 3 %s" % (fr(5, 4), fr(3, 4)), "5 %s − 3 %s" % (fr(11, 4), fr(3, 4)),
                    "5 %s − 3 %s" % (fr(1, 4), fr(3, 4))], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Renaming a whole", "items": its}


# ============================================================ set 4: answers in simplest form
def set_simplest(rnd):
    SPOTS.left = []
    its = []
    # A: write in simplest form
    for w, n, d, g in [(3, 6, 8, 2), (4, 10, 12, 2)]:
        r = Fraction(w) + Fraction(n, d)
        e = ("Only the fraction part changes. Divide the numerator and denominator of %s by %d: %s = %s. "
             "The whole number stays %d. The answer is <b>%s</b>." % (fr(n, d), g, fr(n, d), fr(n // g, d // g), w, show(r)))
        cands = [Fraction(w) + Fraction(n // g, d),          # divided only the numerator
                 Fraction(w // g) + Fraction(n // g, d // g),  # divided the whole number too
                 Fraction(w) + Fraction(n, d // g)]          # divided only the denominator
        its.append(mcq("Write %s in its simplest form." % mx(w, n, d), r, cands, e, rnd))
    e = ("%s is an improper fraction, so the answer is not finished. %s = 1 %s, and 3 + 1 %s = <b>4 %s</b>."
         % (fr(9, 6), fr(9, 6), fr(3, 6), fr(3, 6), fr(1, 2)))
    assert 3 + Fraction(9, 6) == Fraction(9, 2)
    its.append(mcq("Hui Min worked out 2 %s + 1 %s and got 3 %s. What should she do next?" % (fr(5, 6), fr(2, 3), fr(9, 6)),
                   "Write 3 %s as 4 %s" % (fr(9, 6), fr(1, 2)),
                   ["Nothing. The answer is finished", "Write 3 %s as 3 %s" % (fr(9, 6), fr(1, 2)),
                    "Write 3 %s as 3 %s" % (fr(9, 6), fr(2, 3))], e, rnd))
    # B: add, carry and simplify
    for x, y in [((2, 5, 6), (1, 2, 3)), ((2, 1, 3), (1, 3, 4)), ((3, 4, 5), (1, 1, 2)), ((1, 7, 8), (2, 1, 4)),
                 ((2, 3, 4), (3, 5, 6)), ((1, 5, 8), (2, 7, 8)), ((3, 3, 10), (2, 1, 5)), ((4, 5, 12), (1, 1, 4)),
                 ((2, 7, 9), (3, 2, 3))]:
        check_kind(x, y, "+")
        its.append(calc(x, y, "+", rnd))
    # C: subtract and simplify
    for x, y in [((5, 7, 12), (2, 1, 4)), ((6, 5, 6), (1, 1, 3)), ((4, 9, 10), (2, 2, 5)), ((3, 3, 4), (1, 1, 12)),
                 ((5, 1, 6), (1, 1, 2)), ((4, 1, 10), (1, 3, 5)), ((7, 1, 4), (2, 7, 12)), ((6, 1, 3), (3, 5, 6))]:
        check_kind(x, y, "-", simplify=True)
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Answers in simplest form", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []

    def amt(x, unit):
        return mx(*x) + unit

    def word(q, x, y, op, unit, extra=None, pre="", post="", figure=""):
        r = val(x) + val(y) if op == "+" else val(x) - val(y)
        c = (extra or []) + wrong(x, y, op)
        e = pre + e_calc(x, y, op, unit) + post
        its.append(mcq(figure + q + SIMPLE, r, c, e, rnd, unit))
        return r

    # 1 ribbon left
    x, y = (3, 1, 2), (1, 2, 3)
    r = val(x) - val(y)
    word("Siti had %s of ribbon. She used %s to wrap a present. How much ribbon did she have left?"
         % (amt(x, M), amt(y, M)), x, y, "-", M, pre="Left = total − used. ",
         figure=fig(model_svg([(val(y), y), (r, "?")], x, M)))
    # 2 ribbon total
    x, y = (2, 3, 4), (1, 5, 8)
    word("Ali has two pieces of ribbon. One is %s long and the other is %s long. What is their total length?"
         % (amt(x, M), amt(y, M)), x, y, "+", M,
         figure=fig(model_svg([(val(x), x), (val(y), y)], "?", M)))
    # 3 juice left
    x, y = (2, 1, 4), (1, 2, 3)
    r = val(x) - val(y)
    word("A jug had %s of orange juice. Ahmad poured %s of it into cups for his friends. How much orange juice was left in the jug?"
         % (amt(x, L_), amt(y, L_)), x, y, "-", L_,
         figure=fig(model_svg([(val(y), y), (r, "?")], x, L_)))
    # 4 juice total
    x, y = (1, 1, 2), (2, 3, 4)
    word("Mrs Lim bought %s of apple juice and %s of orange juice for a class party. How much juice did she buy altogether?"
         % (amt(x, L_), amt(y, L_)), x, y, "+", L_)
    # 5 hours total
    x, y = (1, 1, 3), (0, 3, 4)
    word("On Saturday, Wei Ming spent %s on his homework and %s reading a storybook. How much time did he spend altogether?"
         % (amt(x, H), amt(y, H)), x, y, "+", H, post=" (That is 2 h 5 min.)")
    assert val(x) + val(y) == 2 + Fraction(1, 12)
    # 6 hours left
    x, y = (4, 1, 2), (1, 3, 4)
    word("Kumar's family spent %s at East Coast Park. They cycled for %s. How much time did they spend on other activities?"
         % (amt(x, H), amt(y, H)), x, y, "-", H, post=" (That is 2 h 45 min.)")
    assert val(x) - val(y) == Fraction(11, 4)
    # 7 hours comparison
    x, y = (1, 1, 6), (0, 2, 3)
    assert val(x) - val(y) == Fraction(1, 2)
    word("Priya practised the piano for %s on Saturday and %s on Sunday. How much longer did she practise on Saturday than on Sunday?"
         % (amt(x, H), amt(y, H)), x, y, "-", H, pre="“How much longer” means subtract. ", post=" (That is 30 min.)",
         figure=fig(compare_svg([("Saturday", val(x), x), ("Sunday", val(y), y)], "?", H)))
    # 8 flour, whole minus mixed
    x, y = (3, 0, 8), (1, 3, 8)
    word("Mrs Ng had 3 kg of flour. She used %s to bake pineapple tarts for Chinese New Year. How much flour did she have left?"
         % amt(y, KG), x, y, "-", KG)
    # 9 cycling comparison
    x, y = (4, 2, 5), (2, 3, 4)
    assert val(x) - val(y) == 1 + Fraction(13, 20)
    word("Ryan cycled %s at East Coast Park. Chloe cycled %s. How much further did Ryan cycle than Chloe?"
         % (amt(x, KM), amt(y, KM)), x, y, "-", KM, pre="“How much further” means subtract. ",
         figure=fig(compare_svg([("Ryan", val(x), x), ("Chloe", val(y), y)], "?", KM)))
    # 10 two-step water
    a, b = Fraction(3, 4), Fraction(5, 6)
    r = 2 - a - b
    assert r == Fraction(5, 12)
    e = ("Model: the whole bar is 2 ℓ. First add what Hafiz drank. Use twelfths: %s + %s = %s + %s = %s = 1 %s ℓ. "
         "Then 2 − 1 %s: rename 1 whole as %s, so 2 = 1 %s. 1 %s − 1 %s = <b>%s ℓ</b>."
         % (fr(3, 4), fr(5, 6), fr(9, 12), fr(10, 12), fr(19, 12), fr(7, 12), fr(7, 12), fr(12, 12), fr(12, 12),
            fr(12, 12), fr(7, 12), fr(5, 12)))
    its.append(mcq(fig(model_svg([(a, (0, 3, 4)), (b, (0, 5, 6)), (r, "?")], (2, 0, 1), L_)) +
                   "Hafiz had a bottle with 2 ℓ of water. He drank %s in the morning and %s in the afternoon. "
                   "How much water was left?" % (fr(3, 4) + L_, fr(5, 6) + L_) + SIMPLE, r,
                   [a + b, 2 - Fraction(8, 10), Fraction(7, 12), 1 + Fraction(5, 12)], e, rnd, L_))
    # 11 two-step ribbon
    a, b = Fraction(3, 2), Fraction(7, 3)
    r = 5 - a - b
    assert r == Fraction(7, 6)
    e = ("Model: the whole bar is 5 m. First add the two pieces Farah cut. Use sixths: 1 %s + 2 %s = 3 %s m. "
         "Then 5 − 3 %s: rename 1 whole, 5 = 4 %s. 4 %s − 3 %s = <b>1 %s m</b>."
         % (fr(3, 6), fr(2, 6), fr(5, 6), fr(5, 6), fr(6, 6), fr(6, 6), fr(5, 6), fr(1, 6)))
    its.append(mcq(fig(model_svg([(a, (1, 1, 2)), (b, (2, 1, 3)), (r, "?")], (5, 0, 1), M)) +
                   "Farah had 5 m of ribbon. She cut off a piece of 1 %s m and another piece of 2 %s m. "
                   "How much ribbon did she have left?" % (fr(1, 2), fr(1, 3)) + SIMPLE, r,
                   [a + b, 2 + Fraction(1, 6), Fraction(1, 6), 1 + Fraction(3, 5)], e, rnd, M))
    # 12 two-step sugar
    s0, s1, s2 = Fraction(23, 10), Fraction(3, 2), Fraction(11, 5)
    r = s0 + s1 - s2
    assert r == Fraction(8, 5)
    e = ("First add: 2 %s + 1 %s = 2 %s + 1 %s = 3 %s = 3 %s kg. Then subtract what she used: 3 %s − 2 %s = 3 %s − 2 %s = 1 %s. "
         "Simplify: %s = %s. The answer is <b>1 %s kg</b>."
         % (fr(3, 10), fr(1, 2), fr(3, 10), fr(5, 10), fr(8, 10), fr(4, 5), fr(4, 5), fr(1, 5), fr(8, 10), fr(2, 10), fr(6, 10),
            fr(6, 10), fr(3, 5), fr(3, 5)))
    its.append(mcq("A tin had 2 %s kg of sugar. Mrs Lim added 1 %s kg more. Then she used 2 %s kg to make kaya. "
                   "How much sugar was left in the tin?" % (fr(3, 10), fr(1, 2), fr(1, 5)) + SIMPLE, r,
                   [s0 + s1, s0 - s2, s0 + s1 + s2, r + 1],
                   e, rnd, KG))
    # 13 two-step hours comparison
    x1, x2, z = Fraction(3, 2), Fraction(7, 4), Fraction(8, 3)
    xt = x1 + x2
    r = xt - z
    assert xt == Fraction(13, 4) and r == Fraction(7, 12)
    e = ("First find Xin Yi's total time. 1 %s + 1 %s = 1 %s + 1 %s = 2 %s = 3 %s h. "
         "Then compare: 3 %s − 2 %s = 3 %s − 2 %s. Rename 1 whole: 2 %s − 2 %s = <b>%s h</b>. (That is 35 min.)"
         % (fr(1, 2), fr(3, 4), fr(2, 4), fr(3, 4), fr(5, 4), fr(1, 4), fr(1, 4), fr(2, 3), fr(3, 12), fr(8, 12),
            fr(15, 12), fr(8, 12), fr(7, 12)))
    its.append(mcq("Xin Yi spent 1 %s h at the library on Monday and 1 %s h on Tuesday. Zhi Hao spent 2 %s h at the library "
                   "on the two days. How much longer did Xin Yi spend at the library than Zhi Hao?" % (fr(1, 2), fr(3, 4), fr(2, 3))
                   + SIMPLE, r, [1 + Fraction(5, 12), xt, xt + z, r + 1], e, rnd, H))
    # 14 two-step paint
    p0, p1, p2 = Fraction(13, 4), Fraction(3, 2), Fraction(3, 8)
    r = p0 - p1 - p2
    assert r == Fraction(11, 8)
    e = ("First add the paint Mr Rahman used. Use eighths: 1 %s + %s = 1 %s + %s = 1 %s ℓ. "
         "Then 3 %s − 1 %s = 3 %s − 1 %s. Rename 1 whole: 2 %s − 1 %s = <b>1 %s ℓ</b>."
         % (fr(1, 2), fr(3, 8), fr(4, 8), fr(3, 8), fr(7, 8), fr(1, 4), fr(7, 8), fr(2, 8), fr(7, 8), fr(10, 8), fr(7, 8), fr(3, 8)))
    its.append(mcq("A tin had 3 %s ℓ of paint. Mr Rahman used 1 %s ℓ to paint a door and %s ℓ to paint a gate. "
                   "How much paint was left in the tin?" % (fr(1, 4), fr(1, 2), fr(3, 8)) + SIMPLE, r,
                   [p1 + p2, p0 - p1, 2 + Fraction(5, 8), r + 1], e, rnd, L_))
    # 15 missing part
    x, y = (4, 3, 4), (2, 5, 6)
    r = val(x) - val(y)
    word("A piece of cloth %s long is cut into two pieces. One piece is %s long. How long is the other piece?"
         % (amt(x, M), amt(y, M)), x, y, "-", M, pre="The two pieces make the whole length, so subtract. ",
         figure=fig(model_svg([(val(y), y), (r, "?")], x, M)))
    # 16 at first
    x, y = (1, 2, 3), (2, 3, 4)
    r = val(x) + val(y)
    word("Devi had some ribbon. She used %s of it and had %s left. How much ribbon did she have at first?"
         % (amt(x, M), amt(y, M)), x, y, "+", M, pre="At first = used + left. ", extra=[val(y) - val(x)],
         figure=fig(model_svg([(val(x), x), (val(y), y)], "?", M)))
    # 17 durian and pineapple
    d0, k = Fraction(7, 4), Fraction(5, 8)
    pine = d0 - k
    r = d0 + pine
    assert pine == Fraction(9, 8) and r == Fraction(23, 8)
    e = ("First find the mass of the pineapple: 1 %s − %s = 1 %s − %s = 1 %s kg. "
         "Then add the two masses: 1 %s + 1 %s = <b>2 %s kg</b>."
         % (fr(3, 4), fr(5, 8), fr(6, 8), fr(5, 8), fr(1, 8), fr(6, 8), fr(1, 8), fr(7, 8)))
    its.append(mcq(fig(compare_svg([("Durian", d0, (1, 3, 4)), ("Pineapple", pine, None)], (0, 5, 8), KG, total="?")) +
                   "A durian has a mass of 1 %s kg. A pineapple is %s kg lighter than the durian. "
                   "What is the total mass of the two fruits?" % (fr(3, 4), fr(5, 8)) + SIMPLE, r,
                   [pine, d0 + d0 + k, d0 + k, r - 1], e, rnd, KG))
    # 18 jugs
    a0, k = Fraction(7, 3), Fraction(5, 4)
    b0 = a0 + k
    r = a0 + b0
    assert b0 == 3 + Fraction(7, 12) and r == 5 + Fraction(11, 12)
    e = ("First find the amount in Jug B: 2 %s + 1 %s = 2 %s + 1 %s = 3 %s ℓ. "
         "Then add both jugs: 2 %s + 3 %s = 2 %s + 3 %s = 5 %s ℓ. The answer is <b>5 %s ℓ</b>."
         % (fr(1, 3), fr(1, 4), fr(4, 12), fr(3, 12), fr(7, 12), fr(1, 3), fr(7, 12), fr(4, 12), fr(7, 12), fr(11, 12), fr(11, 12)))
    its.append(mcq(fig(compare_svg([("Jug B", b0, None), ("Jug A", a0, (2, 1, 3))], (1, 1, 4), L_, total="?")) +
                   "Jug A has 2 %s ℓ of bandung. Jug B has 1 %s ℓ more bandung than Jug A. "
                   "How much bandung is there in the two jugs altogether?" % (fr(1, 3), fr(1, 4)) + SIMPLE, r,
                   [b0, 2 * a0, 3 + Fraction(2, 7), r - 1], e, rnd, L_))
    # 19 three subjects
    t = [Fraction(3, 4), Fraction(4, 3), Fraction(1, 2)]
    r = sum(t)
    assert r == 2 + Fraction(7, 12)
    e = ("Use twelfths: %s + 1 %s + %s = %s + 1 %s + %s = 1 %s = 2 %s h. The answer is <b>2 %s h</b>. (That is 2 h 35 min.)"
         % (fr(3, 4), fr(1, 3), fr(1, 2), fr(9, 12), fr(4, 12), fr(6, 12), fr(19, 12), fr(7, 12), fr(7, 12)))
    its.append(mcq("Sarah spent %s h on Maths, 1 %s h on Science and %s h on English homework. How much time did she spend altogether?"
                   % (fr(3, 4), fr(1, 3), fr(1, 2)) + SIMPLE, r,
                   [1 + Fraction(5, 9), 1 + Fraction(7, 12), Fraction(7, 12), 3 + Fraction(7, 12)], e, rnd, H))
    # 20 MRT journey
    x, y = (0, 1, 3), (0, 3, 4)
    word("Jun Jie took a bus for %s and then the MRT for %s to get to Changi Airport. How long was his journey?"
         % (amt(x, H), amt(y, H)), x, y, "+", H, post=" (That is 1 h 5 min.)")
    assert val(x) + val(y) == 1 + Fraction(1, 12)
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_rows = mixed_rows_svg([(2, 1, 5, FILL), (1, 3, 5, FILL2)])
    f_bars = two_bars_svg(3, 1, 4, 1, 12, W=360, labels=True)
    f_ren = rename_svg(4, 1, 5)
    f_model = model_svg([(Fraction(5, 3), (1, 2, 3)), (Fraction(11, 6), "?")], (3, 1, 2), M)
    return (
        "<h2>Add the whole numbers and the fractions</h2>"
        "<p>A mixed number has a whole number part and a fraction part. When the denominators are the same, "
        "add the fractions, then add the whole numbers. The denominator does not change.</p>"
        "<figure class='sn-fig'>" + f_rows +
        "<figcaption>2 " + fr(1, 5) + " + 1 " + fr(3, 5) + ": 2 + 1 = 3 wholes, and 1 fifth + 3 fifths = 4 fifths.</figcaption></figure>"
        + ex("Example", "2 " + fr(1, 5) + " + 1 " + fr(3, 5) + " = ?",
             "Fractions: " + fr(1, 5) + " + " + fr(3, 5) + " = " + fr(4, 5) + ". Whole numbers: 2 + 1 = 3.", "3 " + fr(4, 5)) +
        "<h2>Unlike denominators: find a common denominator</h2>"
        "<p>Thirds and quarters are different sizes, so you cannot add them as they are. Find the <b>lowest common multiple</b> "
        "of the denominators and write <b>equivalent fractions</b>. The whole numbers stay the same.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines split both bars into twelfths. " + fr(1, 3) + " = " + fr(4, 12) + " and " +
        fr(1, 4) + " = " + fr(3, 12) + ".</figcaption></figure>"
        + ex("Example", "2 " + fr(1, 3) + " + 1 " + fr(1, 4) + " = ?",
             "Common denominator: 12. 2 " + fr(4, 12) + " + 1 " + fr(3, 12) + ". Fractions: " + fr(4, 12) + " + " + fr(3, 12) +
             " = " + fr(7, 12) + ". Whole numbers: 2 + 1 = 3.", "3 " + fr(7, 12)) +
        "<h2>Renaming 1 whole</h2>"
        "<p>In subtraction, the first fraction may be smaller than the second. Then <b>rename 1 whole</b> as a fraction, "
        "for example 1 = " + fr(5, 5) + ". The whole number goes down by 1.</p>"
        "<figure class='sn-fig'>" + f_ren +
        "<figcaption>4 " + fr(1, 5) + " = 3 " + fr(6, 5) + ". One whole and " + fr(1, 5) + " make 6 fifths.</figcaption></figure>"
        + ex("Example", "4 " + fr(1, 5) + " − 2 " + fr(3, 5) + " = ?",
             fr(1, 5) + " is less than " + fr(3, 5) + ", so rename: 4 " + fr(1, 5) + " = 3 " + fr(6, 5) + ". Fractions: " +
             fr(6, 5) + " − " + fr(3, 5) + " = " + fr(3, 5) + ". Whole numbers: 3 − 2 = 1.", "1 " + fr(3, 5))
        + ex("Example", "4 " + fr(1, 6) + " − 1 " + fr(3, 4) + " = ?",
             "Common denominator: 12. 4 " + fr(2, 12) + " − 1 " + fr(9, 12) + ". Rename: 3 " + fr(14, 12) + " − 1 " + fr(9, 12) +
             ". Fractions: " + fr(5, 12) + ". Whole numbers: 3 − 1 = 2.", "2 " + fr(5, 12)) +
        "<h2>Give the answer in simplest form</h2>"
        "<p>If the fraction part is an improper fraction, change it to a mixed number and add it to the whole number. "
        "Then simplify the fraction part.</p>" +
        table(["Calculation", "Working", "Simplest form"], [
            ["2 " + fr(5, 6) + " + 1 " + fr(2, 3), "2 " + fr(5, 6) + " + 1 " + fr(4, 6) + " = 3 " + fr(9, 6) + " = 4 " + fr(3, 6), "4 " + fr(1, 2)],
            ["5 " + fr(7, 12) + " − 2 " + fr(1, 4), "5 " + fr(7, 12) + " − 2 " + fr(3, 12) + " = 3 " + fr(4, 12), "3 " + fr(1, 3)],
            ["1 " + fr(5, 8) + " + 2 " + fr(7, 8), "3 " + fr(12, 8) + " = 4 " + fr(4, 8), "4 " + fr(1, 2)],
        ]) +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar for the whole amount and split it into parts. Mark the unknown part with “?”. "
        "Then decide whether to add or subtract.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>Siti had 3 " + fr(1, 2) + " m of ribbon and used 1 " + fr(2, 3) + " m. Left = 3 " + fr(1, 2) + " − 1 " +
        fr(2, 3) + ".</figcaption></figure>"
        + ex("Example", "Siti had 3 " + fr(1, 2) + " m of ribbon. She used 1 " + fr(2, 3) + " m. How much was left?",
             "3 " + fr(3, 6) + " − 1 " + fr(4, 6) + ". Rename: 2 " + fr(9, 6) + " − 1 " + fr(4, 6) + " = 1 " + fr(5, 6) + ".",
             "1 " + fr(5, 6) + " m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["1 " + fr(2, 5) + " + 2 " + fr(1, 5) + " = 3 " + fr(3, 10) + " (adding the numerators and the denominators)",
             "Keep the denominator: 3 " + fr(3, 5)],
            ["4 " + fr(1, 5) + " − 2 " + fr(3, 5) + " = 2 " + fr(2, 5) + " (taking the smaller fraction from the larger)",
             "Rename 1 whole: 3 " + fr(6, 5) + " − 2 " + fr(3, 5) + " = 1 " + fr(3, 5)],
            ["6 " + fr(1, 4) + " − 3 " + fr(3, 4) + " = 3 " + fr(1, 2) + " (renaming but keeping 6 wholes)",
             "After renaming there are 5 wholes: 5 " + fr(5, 4) + " − 3 " + fr(3, 4) + " = 2 " + fr(1, 2)],
            ["3 " + fr(9, 6) + " or 4 " + fr(3, 6) + " (not simplifying)",
             "Change the improper fraction and simplify: 4 " + fr(1, 2)],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 fractions for mixed numbers?",
     "a": "In Primary 5, students add and subtract mixed numbers, including fractions with unlike denominators. They find a common denominator, rename 1 whole when needed and give answers in simplest form."},
    {"q": "How do I explain renaming in mixed number subtraction to my child?",
     "a": "Show that 1 whole is the same as 5 fifths, so 4 1/5 = 3 6/5. Now there are enough fifths to take away 3/5: 3 6/5 − 2 3/5 = 1 3/5."},
    {"q": "What is the most common mistake when adding mixed numbers?",
     "a": "Adding the denominators, as in 1 2/5 + 2 1/5 = 3 3/10. The parts are still fifths, so the answer is 3 3/5."},
    {"q": "Is adding and subtracting mixed numbers in the MOE syllabus?",
     "a": "Yes. It is part of Fractions in the Primary 5 Standard Mathematics syllabus (MOE 2021). These skills are used again in Primary 6 and in PSLE word problems."},
]


def gen_unit():
    rnd = random.Random(65805)
    sets = [set_like(rnd), set_unlike(rnd), set_rename(rnd), set_simplest(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "adding-and-subtracting-mixed-numbers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Adding and Subtracting Mixed Numbers",
        "seo_title": "P5 Adding and Subtracting Mixed Numbers Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Adding and Subtracting Mixed Numbers",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting mixed numbers",
        "meta_desc": "Free P5 maths practice: add and subtract mixed numbers with like and unlike denominators, renaming and bar model word problems. 100 questions with answers.",
        "key_big": "Use a common denominator, add or subtract the fractions and the whole numbers, and rename 1 whole when the first fraction is too small.",
        "key_sub": "4 1/5 − 2 3/5 = 3 6/5 − 2 3/5 = 1 3/5",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(two bars|bars for|bar of|bar model)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
