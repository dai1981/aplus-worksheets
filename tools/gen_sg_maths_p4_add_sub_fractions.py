# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Adding and Subtracting Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 4: Fractions)
  python3 tools/gen_sg_maths_p4_add_sub_fractions.py
Like denominators, related denominators (one a multiple of the other, up to 12), simplest form,
subtracting from a whole, and word problems with bar models and pizzas.
Every answer is in simplest form (a mixed number when it is more than 1); wrong choices come from
real mistakes and are never equal in value to the answer or to each other.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
FILL3 = "#8fb8e8"     # bar models
PIZZA = "#f6d58a"     # pizza not eaten
RED = "#c0392b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}
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


def F(n, d):
    return (0, n, d)


def val(x):
    w, n, d = x
    return Fraction(w) + Fraction(n, d)


def lcm(a, b):
    return a * b // math.gcd(a, b)


L_ = " ℓ"
M = " m"
KM = " km"
KG = " kg"
H = " h"


def withu(v, unit):
    return show(v) + (unit or "")


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
        return (size + 2) * 0.6 * len(lab)
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


def cross(cx, cy, r):
    return ("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))


# ------------------------------------------------------------ pictures
def bar_cells(x0, y0, W, Hh, d, k, col, sw=2.2):
    return "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='%.1f'/>"
                   % (x0 + i * W / d, y0, W / d, Hh, col if i < k else "#fff", LINE, sw) for i in range(d))


def dashes(x0, y0, W, Hh, d, L):
    """Dashed lines that cut a bar of d parts into L parts (only where there is no solid line yet)."""
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
    s = [bar_cells(x0, 6, W, Hh, d1, k1, FILL), dashes(x0, 6, W, Hh, d1, L),
         bar_cells(x0, 6 + Hh + 14, W, Hh, d2, k2, FILL2), dashes(x0, 6 + Hh + 14, W, Hh, d2, L)]
    s.append("<rect x='%d' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, W, Hh, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, 6 + Hh + 14, W, Hh, LINE))
    if labels:
        g1, g2 = math.gcd(k1, d1), math.gcd(k2, d2)
        s.append(sfr(26, 22, k1 // g1, d1 // g1, 15))
        s.append(sfr(26, 22 + Hh + 14, k2 // g2, d2 // g2, 15))
    return svg_wrap(x0 + W + 6, 2 * Hh + 26, "".join(s),
                    "two bars of the same size: %d of %d parts green and %d of %d parts yellow, dashed lines cut both into %d parts"
                    % (k1, d1, k2, d2, L))


def one_bar_svg(L, k1, k2, crossed=0, W=264, Hh=40):
    """One bar of L parts: k1 green then k2 yellow. crossed = how many of the last green parts get a red X."""
    s = []
    for i in range(L):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else "#fff")
        x = 6 + i * W / L
        s.append("<rect x='%.2f' y='6' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (x, W / L, Hh, col, LINE))
        if k1 - crossed <= i < k1:
            c = W / L
            r = min(c, Hh) / 2 - min(c, Hh) * 0.2
            s.append(cross(x + c / 2, 6 + Hh / 2, r))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, Hh, LINE))
    if crossed:
        lab = "bar of %d equal parts: %d shaded and the last %d of them crossed out" % (L, k1, crossed)
    else:
        lab = "bar of %d equal parts: %d green and %d yellow" % (L, k1, k2)
    return svg_wrap(W + 12, Hh + 12, "".join(s), lab)


def wholes_svg(d, k1, k2, W=264, Hh=40):
    """Two bars (two wholes) of d parts each. The first k1 parts are green, the next k2 yellow, filling bar 1 then bar 2."""
    s = []
    for b in range(2):
        y0 = 6 + b * (Hh + 14)
        for i in range(d):
            j = b * d + i
            col = FILL if j < k1 else (FILL2 if j < k1 + k2 else "#fff")
            s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                     % (6 + i * W / d, y0, W / d, Hh, col, LINE))
        s.append("<rect x='6' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (y0, W, Hh, LINE))
    return svg_wrap(W + 12, 2 * Hh + 26, "".join(s),
                    "two bars of %d equal parts each: %d parts green then %d parts yellow" % (d, k1, k2))


def pie_body(cx, cy, R, d, k1, k2=0, crossed=0, base="#fff"):
    """A circle cut into d equal slices from 12 o'clock, clockwise. First k1 slices green, next k2 yellow,
    the rest in base colour. The first `crossed` slices get a red X."""
    s = []
    for i in range(d):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else base)
        if d == 1:
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2.2'/>" % (cx, cy, R, col, LINE))
            continue
        a0 = -math.pi / 2 + 2 * math.pi * i / d
        a1 = a0 + 2 * math.pi / d
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%.1f %.1f 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                    cx + R * math.cos(a1), cy + R * math.sin(a1), col, LINE))
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    for i in range(crossed):
        am = -math.pi / 2 + 2 * math.pi * (i + 0.5) / d
        s.append(cross(cx + 0.62 * R * math.cos(am), cy + 0.62 * R * math.sin(am), min(6, 0.62 * R * math.sin(math.pi / d) * 0.6)))
    return "".join(s)


def pies_svg(pies, R=46, label="pizza"):
    """pies: list of (d, k1, k2, crossed, base). Drawn side by side."""
    s = []
    for j, (d, k1, k2, crossed, base) in enumerate(pies):
        s.append(pie_body(6 + R + j * (2 * R + 20), 6 + R, R, d, k1, k2, crossed, base))
    n = len(pies)
    lab = "%s: " % label + "; ".join("circle cut into %d equal slices, %d green, %d yellow, %d crossed out" % p[:4] for p in pies)
    return svg_wrap(12 + n * 2 * R + (n - 1) * 20, 12 + 2 * R, "".join(s), lab)


def model_svg(segs, total, unit, W=300, name=None):
    """Part-whole bar model. segs: list of (value, label) where label is (w, n, d) or '?'.
    total: label for the whole bar, (w, n, d) or a string, shown with a brace above."""
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


def compare_svg(rows, diff, unit, W=230):
    """Comparison bar model. rows: [(name, value, label)] (two rows, the first is longer). The longer bar has its
    extra part marked with a dashed line and diff ('?') inside it. Each known value is written to the right of its bar."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    x0 = 14 + 8.6 * max(len(n1), len(n2))
    Hh = 40
    s = []
    right = x0 + W
    for j, (nm, v, lab) in enumerate(rows):
        y = 8 + j * (Hh + 16)
        w = W * v / v1
        s.append(txt(6, y + Hh / 2 + 5, nm, 15, anchor="start"))
        s.append("<rect x='%.2f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (x0, y, w, Hh, FILL3 if j == 0 else FILL2, LINE))
        if j == 0:
            ws = W * v2 / v1
            s.append("<line x1='%.2f' y1='%d' x2='%.2f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0 + ws, y, x0 + ws, y + Hh, LINE))
            assert lab_w(diff, unit) < W - ws - 4, (diff, W - ws)
            s.append(lab_svg(x0 + (ws + W) / 2, y + Hh / 2, diff, unit))
        s.append(lab_svg(x0 + w + 8 + lab_w(lab, unit) / 2, y + Hh / 2, lab, unit))
        right = max(right, x0 + w + 12 + lab_w(lab, unit))
    return svg_wrap(right + 6, 8 + 2 * Hh + 16 + 8, "".join(s), "bar model comparing two bars")


# ------------------------------------------------------------ explanation and mistakes
def finish(N, L, unit=None):
    """N/L (N may be L or more). Convert, simplify, state the answer."""
    t = ""
    W = 0
    if N >= L:
        w2, r = divmod(N, L)
        if r:
            t += "%s is more than 1: %s = %s. " % (fr(N, L), fr(N, L), mx(w2, r, L))
        else:
            t += "%s = %d. " % (fr(N, L), w2)
        W, N = w2, r
    g = math.gcd(N, L) if N else 1
    if N and g > 1:
        t += "Simplify: divide the numerator and denominator of %s by %d to get %s. " % (fr(N, L), g, fr(N // g, L // g))
    v = W + Fraction(N, L)
    return t + "The answer is <b>%s</b>." % withu(v, unit), v


def common(d1, d2):
    L = lcm(d1, d2)
    if d1 == d2:
        return "The denominators are the same, so the denominator stays %d. " % d1
    return "%d is a multiple of %d, so use %d as the common denominator. " % (L, min(d1, d2), L)


def e_calc(x, y, op, unit=None):
    """Step explanation for x op y (proper fractions, as (0, n, d))."""
    (_, n1, d1), (_, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    t = common(d1, d2)
    rw = ["%s = %s" % (fr(n, d), fr(n * L // d, L)) for _, n, d in (x, y) if d != L]
    if rw:
        k = L // min(d1, d2)
        t += "Multiply the numerator and denominator by %d: " % k + " and ".join(rw) + ". "
    if op == "+":
        t += "Add the numerators: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
        s, v = finish(a + b, L, unit)
        assert v == val(x) + val(y)
    else:
        t += "Subtract the numerators: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
        s, v = finish(a - b, L, unit)
        assert v == val(x) - val(y)
    return t + s


def wrong(x, y, op):
    """Wrong answers from real mistakes, most common first."""
    (_, n1, d1), (_, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    right = val(x) + val(y) if op == "+" else val(x) - val(y)
    N = a + b if op == "+" else a - b
    g = math.gcd(N % L, L) if N % L else 1
    c = []
    if op == "+":
        c.append(Fraction(n1 + n2, d1 + d2))                     # added the numerators and the denominators
        if d1 != d2:
            c.append(Fraction(n1 + n2, L))                       # changed the denominator but not the numerators
            c.append(Fraction(a + n2, L) if d2 != L else Fraction(n1 + b, L))   # changed only one fraction
        if g > 1 and N < L:
            c.append(Fraction(N // g, L))                        # divided only the numerator
        if N >= L:
            c.append(right - 1)                                  # left out the whole
            c.append(Fraction(N % L, L * 2) if N % L else None)
        c.append(Fraction(abs(a - b), L) if a != b else None)    # subtracted instead
        c.append(Fraction(N + 1, L))                             # miscounted the parts
        c.append(Fraction(N - 1, L) if N > 1 else None)
        c.append(right + 1)
    else:
        if d1 != d2 and n1 > n2 and d1 > d2:
            c.append(Fraction(n1 - n2, d1 - d2))                 # subtracted the numerators and the denominators
        if d1 != d2:
            c.append(Fraction(abs(n1 - n2), L) if n1 != n2 else None)   # changed the denominator but not the numerators
            c.append(Fraction(a - n2, L) if d2 != L else Fraction(n1 - b, L))   # changed only one fraction
        if g > 1:
            c.append(Fraction(N // g, L))                        # divided only the numerator
        c.append(Fraction(a + b, L))                             # added instead
        c.append(Fraction(N + 1, L))                             # miscounted the parts
        c.append(Fraction(N - 1, L) if N > 1 else None)
        c.append(Fraction(b, L))                                 # wrote the part taken away
    return c


def calc_q(x, y, op, prompt=SIMPLE):
    sym = "+" if op == "+" else "−"
    return "%s %s %s = ?" % (mx(*x), sym, mx(*y)) + prompt


def calc(x, y, op, rnd, prompt=SIMPLE, extra=None):
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    assert r > 0
    c = (extra or []) + wrong(x, y, op)
    return mcq(calc_q(x, y, op, prompt), r, c, e_calc(x, y, op), rnd)


def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


def rename_choices(n1, d1, n2, d2, L):
    k1, k2 = L // d1, L // d2
    right = (n1 * k1, n2 * k2)
    cands = [(n1, n2),                                   # changed the denominator only
             (n1 + L - d1, n2 + L - d2),                 # added the same number to the top and bottom
             (n1 * k1 + 1, n2 * k2), (n1 * k1, n2 + 1)]
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


def kind(x, y, op, like=None, simplify=None, over=None):
    """Checks that a question is of the kind the set says."""
    (_, n1, d1), (_, n2, d2) = x, y
    assert n1 < d1 <= 12 and n2 < d2 <= 12
    assert max(d1, d2) % min(d1, d2) == 0, (x, y)
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    N = a + b if op == "+" else a - b
    assert N > 0
    if like is not None:
        assert (d1 == d2) == like, (x, y)
    if over is not None:
        assert (N >= L) == over, (x, y)
    if simplify is not None:
        assert (N % L != 0 and math.gcd(N % L, L) > 1 or N % L == 0) == simplify, (x, y)


# ------------------------------------------------------------ subtract from a whole
def e_whole(W, n, d, unit=None):
    """Explanation for W − n/d."""
    if W == 1:
        t = "Write 1 as %s. Then %s − %s = %s. " % (fr(d, d), fr(d, d), fr(n, d), fr(d - n, d))
    else:
        t = ("Take 1 whole from %d and write it as %s: %d = %s. Then %s − %s = %s. "
             % (W, fr(d, d), W, mx(W - 1, d, d), mx(W - 1, d, d), fr(n, d), mx(W - 1, d - n, d)))
    g = math.gcd(d - n, d)
    if g > 1:
        t += "Simplify: %s = %s. " % (fr(d - n, d), fr((d - n) // g, d // g))
    v = W - Fraction(n, d)
    return t + "The answer is <b>%s</b>." % withu(v, unit), v


def wrong_whole(W, n, d):
    g = math.gcd(d - n, d)
    c = []
    if W == 1:
        c.append(Fraction(n, d))                         # wrote the part taken away
        if g > 1:
            c.append(Fraction((d - n) // g, d))          # divided only the numerator
        c.append(Fraction(n - 1, d) if n > 1 else None)  # took 1 from the numerator
        c.append(Fraction(d - n - 1, d) if d - n > 1 else None)   # miscounted
        c.append(Fraction(d - n + 1, d))
        c.append(Fraction(d - 1, d))
    else:
        c.append(W + Fraction(d - n, d))                 # did not take 1 from the wholes
        c.append(W - 1 + Fraction(n, d))                 # kept the fraction that was taken away
        c.append(Fraction(d - n, d))                     # forgot the whole number
        c.append(W - 1 + Fraction(d - n - 1, d) if d - n > 1 else None)
        c.append(W - 1 + Fraction(d - n + 1, d))
    return c


# ============================================================ set 1: like denominators
def set_like(rnd):
    SPOTS.left = []
    its = []
    # A: pictures
    q = (fig(one_bar_svg(7, 2, 3)) + "The bar is cut into 7 equal parts. The green parts show %s. The yellow parts show %s. "
         "What is %s + %s?" % (fr(2, 7), fr(3, 7), fr(2, 7), fr(3, 7)))
    e = "Count the shaded parts: 2 sevenths + 3 sevenths = 5 sevenths. The parts are still sevenths. The answer is <b>%s</b>." % fr(5, 7)
    its.append(mcq(q, Fraction(5, 7), [Fraction(5, 14), Fraction(6, 7), Fraction(1, 7), Fraction(4, 7)], e, rnd))
    q = (fig(pies_svg([(8, 3, 2, 0, "#fff")], label="circle")) + "The circle is cut into 8 equal parts. "
         "What fraction of the circle is shaded green or yellow?")
    e = "3 eighths are green and 2 eighths are yellow. %s + %s = <b>%s</b>." % (fr(3, 8), fr(2, 8), fr(5, 8))
    its.append(mcq(q, Fraction(5, 8), [Fraction(5, 16), Fraction(3, 8), Fraction(3, 4), Fraction(1, 4)], e, rnd))
    q = (fig(one_bar_svg(9, 7, 0, crossed=3)) + "The bar shows %s. Then %s is crossed out. What is %s − %s?"
         % (fr(7, 9), fr(3, 9), fr(7, 9), fr(3, 9)))
    e = "7 ninths take away 3 ninths leaves 4 ninths. Count the green parts with no X. The answer is <b>%s</b>." % fr(4, 9)
    its.append(mcq(q, Fraction(4, 9), [Fraction(10, 9), Fraction(5, 9), Fraction(7, 9), Fraction(1, 3)],
                   e, rnd))
    q = (fig(wholes_svg(5, 4, 3)) + "Each bar is 1 whole. The green parts show %s. The yellow parts show %s. "
         "What is %s + %s?" % (fr(4, 5), fr(3, 5), fr(4, 5), fr(3, 5)) + "<br>Give your answer as a mixed number.")
    e = ("4 fifths + 3 fifths = 7 fifths, so %s. 5 fifths fill the first bar and 2 fifths are in the second bar. "
         "%s = <b>1 %s</b>." % (fr(7, 5), fr(7, 5), fr(2, 5)))
    its.append(mcq(q, Fraction(7, 5), [Fraction(7, 10), Fraction(2, 5), 2 + Fraction(2, 5), Fraction(1, 5)], e, rnd))
    # B: add, no simplifying
    for x, y in [(F(2, 9), F(5, 9)), (F(4, 11), F(5, 11)), (F(3, 10), F(4, 10)), (F(1, 6), F(4, 6)),
                 (F(5, 7), F(4, 7)), (F(3, 5), F(4, 5)), (F(5, 8), F(6, 8)), (F(7, 12), F(6, 12))]:
        kind(x, y, "+", like=True, simplify=False)
        its.append(calc(x, y, "+", rnd))
    # C: subtract, no simplifying
    for x, y in [(F(8, 9), F(3, 9)), (F(6, 7), F(2, 7)), (F(9, 10), F(2, 10)), (F(11, 12), F(6, 12)),
                 (F(4, 5), F(1, 5)), (F(7, 8), F(4, 8))]:
        kind(x, y, "-", like=True, simplify=False)
        its.append(calc(x, y, "-", rnd))
    # D: missing number
    e = "Find the missing number by subtracting: %s − %s = %s. Check: %s + %s = %s. The answer is <b>%s</b>." % (
        fr(6, 7), fr(2, 7), fr(4, 7), fr(2, 7), fr(4, 7), fr(6, 7), fr(4, 7))
    its.append(mcq("%s + <b>?</b> = %s" % (fr(2, 7), fr(6, 7)), Fraction(4, 7),
                   [Fraction(8, 7), Fraction(5, 7), Fraction(3, 7), Fraction(2, 7)], e, rnd))
    # E: spot the mistake
    e = ("The parts are sevenths, so the denominator stays 7: 2 sevenths + 3 sevenths = 5 sevenths. "
         "%s + %s = <b>%s</b>. Ahmad added the denominators too, which gave fourteenths." % (fr(2, 7), fr(3, 7), fr(5, 7)))
    its.append(mcq("Ahmad wrote %s + %s = %s. What mistake did he make?" % (fr(2, 7), fr(3, 7), fr(5, 14)),
                   "He added the denominators",
                   ["He forgot to simplify", "He subtracted the numerators", "There is no mistake"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Like denominators", "items": its}


# ============================================================ set 2: related denominators
def set_related(rnd):
    SPOTS.left = []
    its = []
    # A: common denominator
    for x, y, op in [(F(1, 2), F(3, 8), "+"), (F(5, 6), F(1, 3), "-"), (F(2, 3), F(1, 9), "+")]:
        d1, d2 = x[2], y[2]
        big, small = max(d1, d2), min(d1, d2)
        e = ("%d is a multiple of %d (%d × %d = %d), so both fractions can be written in %s. "
             "The common denominator is <b>%d</b>." % (big, small, small, big // small, big, WORD[big], big))
        sym = "+" if op == "+" else "−"
        its.append(mcq("To work out %s %s %s, you need a common denominator. What is the common denominator?"
                       % (fr(x[1], d1), sym, fr(y[1], d2)), str(big),
                       [str(d1 * d2), str(d1 + d2), str(small)], e, rnd))
    # B: equivalent fraction
    for n, d, L, bad in [(1, 2, 8, ["1", "7", "2"]), (2, 3, 12, ["2", "11", "6"]), (3, 5, 10, ["3", "8", "5"])]:
        k = L // d
        e = ("%d × %d = %d, so the denominator was multiplied by %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (d, k, L, k, k, n, k, n * k, fr(n, d), fr(n * k, L)))
        its.append(mcq("%s = %s. What is the missing number?" % (fr(n, d), fr("<b>?</b>", L)), str(n * k), bad, e, rnd))
    # C: fraction bars
    for x, y in [(F(1, 2), F(3, 8)), (F(1, 3), F(5, 6))]:
        n1, d1, n2, d2 = x[1], x[2], y[1], y[2]
        L = lcm(d1, d2)
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "The bars show %s (green) and %s (yellow). The dashed lines cut both bars into %s. "
             "Which shows both fractions in %s?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
        its.append(mcq(q, r, c, e, rnd))
    # D: add
    for x, y in [(F(1, 2), F(3, 8)), (F(1, 4), F(3, 8)), (F(2, 5), F(3, 10)), (F(1, 3), F(2, 9)), (F(5, 12), F(1, 2))]:
        kind(x, y, "+", like=False, simplify=False, over=False)
        its.append(calc(x, y, "+", rnd))
    # E: subtract
    for x, y in [(F(5, 6), F(1, 3)), (F(7, 8), F(1, 4)), (F(7, 9), F(1, 3)), (F(3, 4), F(5, 12)), (F(9, 10), F(3, 5))]:
        kind(x, y, "-", like=False)
        its.append(calc(x, y, "-", rnd))
    # F: more than 1
    for x, y in [(F(3, 4), F(5, 8)), (F(5, 6), F(2, 3))]:
        kind(x, y, "+", like=False, over=True)
        its.append(calc(x, y, "+", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Related denominators", "items": its}


# ============================================================ set 3: simplest form
def set_simplest(rnd):
    SPOTS.left = []
    its = []
    # A: write in simplest form
    for n, d in [(6, 8), (4, 12), (8, 10)]:
        g = math.gcd(n, d)
        r = Fraction(n, d)
        e = ("%d and %d can both be divided by %d. %d ÷ %d = %d and %d ÷ %d = %d, so %s = <b>%s</b>."
             % (n, d, g, n, g, n // g, d, g, d // g, fr(n, d), show(r)))
        cands = [Fraction(n // g, d), Fraction(n, d // g), Fraction(n - 2, d - 2) if n > 2 else None, Fraction(n - 1, d - 1)]
        its.append(mcq("Write %s in its simplest form." % fr(n, d), r, cands, e, rnd))
    # B: like denominators, then simplify
    for x, y, op in [(F(1, 8), F(5, 8), "+"), (F(7, 10), F(3, 10), "-"), (F(5, 12), F(1, 12), "+"),
                     (F(2, 9), F(4, 9), "+"), (F(11, 12), F(2, 12), "-"), (F(2, 5), F(3, 5), "+")]:
        kind(x, y, op, like=True, simplify=True)
        its.append(calc(x, y, op, rnd))
    # C: related denominators, then simplify
    for x, y, op in [(F(1, 3), F(1, 6), "+"), (F(1, 4), F(5, 12), "+"), (F(1, 2), F(3, 10), "+"),
                     (F(1, 2), F(1, 10), "-"), (F(5, 6), F(1, 2), "-"), (F(11, 12), F(1, 4), "-")]:
        kind(x, y, op, like=False, simplify=True)
        its.append(calc(x, y, op, rnd))
    # D: more than 1, then simplify
    for x, y in [(F(7, 8), F(3, 8)), (F(5, 6), F(1, 2)), (F(9, 10), F(1, 2))]:
        kind(x, y, "+", over=True, simplify=True)
        its.append(calc(x, y, "+", rnd))
    # E: what to do next
    e = ("%s is not in its simplest form. 8 and 12 can both be divided by 4: %s = <b>%s</b>. "
         "%s is equal, but it can still be simplified." % (fr(8, 12), fr(8, 12), fr(2, 3), fr(4, 6)))
    its.append(mcq("Wei Ming worked out %s + %s and got %s. What should he do next?" % (fr(1, 4), fr(5, 12), fr(8, 12)),
                   "Write %s as %s" % (fr(8, 12), fr(2, 3)),
                   ["Nothing. The answer is finished", "Write %s as %s" % (fr(8, 12), fr(4, 6)),
                    "Write %s as %s" % (fr(8, 12), fr(8, 24))], e, rnd))
    assert Fraction(1, 2) + Fraction(3, 10) == Fraction(4, 5)
    e = ("%s = %s, and %s + %s = %s, so her working is right. But 8 and 10 can both be divided by 2, "
         "so the answer in simplest form is <b>%s</b>." % (fr(1, 2), fr(5, 10), fr(5, 10), fr(3, 10), fr(8, 10), fr(4, 5)))
    its.append(mcq("Nurul wrote %s + %s = %s. Is she right?" % (fr(1, 2), fr(3, 10), fr(8, 10)),
                   "Yes, but %s should be written as %s" % (fr(8, 10), fr(4, 5)),
                   ["No, the answer is %s" % fr(4, 12), "No, the answer is %s" % fr(4, 10),
                    "Yes, and %s is in simplest form" % fr(8, 10)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Answers in simplest form", "items": its}


# ============================================================ set 4: subtract from a whole
def set_whole(rnd):
    SPOTS.left = []
    its = []
    # A: pictures
    q = (fig(one_bar_svg(8, 8, 0, crossed=3)) + "The whole bar is 1. It is cut into 8 equal parts and 3 parts are crossed out. "
         "What is 1 − %s?" % fr(3, 8))
    e, v = e_whole(1, 3, 8)
    its.append(mcq(q, v, wrong_whole(1, 3, 8), "Count the parts with no X: 5 eighths. " + e, rnd))
    q = (fig(pies_svg([(6, 0, 0, 1, PIZZA)])) + "A pizza is cut into 6 equal slices. Siti eats 1 slice. "
         "What fraction of the pizza is left?")
    e, v = e_whole(1, 1, 6)
    its.append(mcq(q, v, [Fraction(1, 6), Fraction(4, 6), Fraction(1, 5), Fraction(6, 7)],
                   "1 whole pizza is %s. 1 slice is %s. " % (fr(6, 6), fr(1, 6)) + e, rnd))
    e = "1 whole cut into fifths has 5 fifths, so 1 = %s. The missing number is <b>5</b>." % fr(5, 5)
    its.append(mcq("1 = %s. What is the missing number?" % fr("<b>?</b>", 5), "5", ["1", "4", "10"], e, rnd))
    # B: 1 − a fraction
    for n, d in [(2, 5), (4, 7), (5, 9), (7, 12), (3, 10), (1, 4), (6, 11)]:
        e, v = e_whole(1, n, d)
        its.append(mcq("1 − %s = ?" % fr(n, d) + SIMPLE, v, wrong_whole(1, n, d), e, rnd))
    # C: 1 − a fraction, then simplify
    for n, d in [(2, 8), (4, 10), (6, 9)]:
        e, v = e_whole(1, n, d)
        assert math.gcd(d - n, d) > 1
        its.append(mcq("1 − %s = ?" % fr(n, d) + SIMPLE, v, wrong_whole(1, n, d), e, rnd))
    # D: 1 − two fractions
    for (n1, d1), (n2, d2) in [((1, 4), (3, 8)), ((1, 2), (1, 6)), ((1, 3), (2, 9))]:
        L = max(d1, d2)
        a, b = n1 * L // d1, n2 * L // d2
        v = 1 - Fraction(n1, d1) - Fraction(n2, d2)
        e = "Use %s: %s = %s. Write 1 as %s. %s − %s − %s = %s. " % (
            WORD[L], fr(n1, d1), fr(a, L), fr(L, L), fr(L, L), fr(a, L), fr(b, L), fr(L - a - b, L))
        g = math.gcd(L - a - b, L)
        if g > 1:
            e += "Simplify: %s = %s. " % (fr(L - a - b, L), show(v))
        e += "The answer is <b>%s</b>." % show(v)
        cands = [Fraction(a + b, L), 1 - Fraction(n1 + n2, L), 1 - Fraction(n1 + n2, d1 + d2),
                 Fraction(L - a - b + 1, L), Fraction(L - a - b - 1, L) if L - a - b > 1 else None]
        its.append(mcq("1 − %s − %s = ?" % (fr(n1, d1), fr(n2, d2)) + SIMPLE, v, cands, e, rnd))
    # E: 2 or 3 wholes
    for W, n, d in [(2, 3, 4), (3, 2, 5), (2, 5, 6)]:
        e, v = e_whole(W, n, d)
        its.append(mcq("%d − %s = ?" % (W, fr(n, d)) + SIMPLE, v, wrong_whole(W, n, d), e, rnd))
    # F: missing number
    e = "%s + ? = 1 means 1 − %s. Write 1 as %s: %s − %s = <b>%s</b>." % (
        fr(5, 8), fr(5, 8), fr(8, 8), fr(8, 8), fr(5, 8), fr(3, 8))
    its.append(mcq("%s + <b>?</b> = 1" % fr(5, 8), Fraction(3, 8),
                   [Fraction(5, 8), Fraction(4, 8), Fraction(2, 8), Fraction(1, 8)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Subtracting from a whole", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []

    def word(q, x, y, op, unit=None, extra=None, pre="", post="", figure=""):
        r = val(x) + val(y) if op == "+" else val(x) - val(y)
        c = (extra or []) + wrong(x, y, op)
        e = pre + e_calc(x, y, op, unit) + post
        its.append(mcq(figure + q + SIMPLE, r, c, e, rnd, unit))
        return r

    # 1 pizza eaten together
    word("Ali and Siti shared a pizza. Ali ate %s of the pizza (green) and Siti ate %s of it (yellow). "
         "What fraction of the pizza did they eat altogether?" % (fr(3, 8), fr(2, 8)), F(3, 8), F(2, 8), "+",
         figure=fig(pies_svg([(8, 3, 2, 0, PIZZA)])), pre="“Altogether” means add. ")
    # 2 pizza left
    e, v = e_whole(1, 5, 8)
    its.append(mcq(fig(pies_svg([(8, 0, 0, 5, PIZZA)])) +
                   "Mr Tan bought a pizza for his family. They ate %s of it. What fraction of the pizza was left?"
                   % fr(5, 8) + SIMPLE, v, wrong_whole(1, 5, 8), "The whole pizza is 1. Left = 1 − eaten. " + e, rnd))
    # 3 two pizzas, more than 1
    word("Mrs Lim ordered two pizzas of the same size for a class party. The students ate %s of the first pizza "
         "and %s of the second pizza. How many pizzas did they eat altogether?" % (fr(5, 6), fr(2, 3)),
         F(5, 6), F(2, 3), "+", figure=fig(pies_svg([(6, 5, 0, 0, PIZZA), (6, 0, 4, 0, PIZZA)])),
         post=" They ate 1 %s pizzas." % fr(1, 2))
    # 4 pizza, related, left
    v = 1 - Fraction(3, 8) - Fraction(1, 2)
    assert v == Fraction(1, 8)
    e = ("First add what they ate. Use eighths: %s + %s = %s + %s = %s. Then 1 − %s = %s − %s = <b>%s</b>."
         % (fr(3, 8), fr(1, 2), fr(3, 8), fr(4, 8), fr(7, 8), fr(7, 8), fr(8, 8), fr(7, 8), fr(1, 8)))
    its.append(mcq("Jun Jie ate %s of a pizza. His sister Hui Min ate %s of the same pizza. "
                   "What fraction of the pizza was left?" % (fr(3, 8), fr(1, 2)) + SIMPLE, v,
                   [Fraction(7, 8), Fraction(1, 2), Fraction(3, 5), Fraction(5, 8)], e, rnd))
    # 5 water bottle, drank altogether
    x, y = F(3, 10), F(1, 2)
    r = val(x) + val(y)
    word("Hafiz filled his water bottle. He drank %s of the water during recess and %s of it after his CCA. "
         "What fraction of the water did he drink altogether?" % (fr(3, 10), fr(1, 2)), x, y, "+",
         figure=fig(model_svg([(val(x), x), (val(y), y), (1 - r, "?")], "1 bottle", None)))
    # 6 water bottle left
    v = 1 - Fraction(3, 10) - Fraction(1, 2)
    e = ("She drank %s + %s = %s + %s = %s of the water. Left = 1 − %s = %s − %s = %s. "
         "Simplify: %s = <b>%s</b>." % (fr(3, 10), fr(1, 2), fr(3, 10), fr(5, 10), fr(8, 10), fr(8, 10), fr(10, 10),
                                        fr(8, 10), fr(2, 10), fr(2, 10), fr(1, 5)))
    its.append(mcq("Priya filled her water bottle. She drank %s of the water in the morning and %s of it at lunch. "
                   "What fraction of the water was left in the bottle?" % (fr(3, 10), fr(1, 2)) + SIMPLE, v,
                   [Fraction(4, 5), Fraction(3, 5), Fraction(2, 3), Fraction(1, 2)], e, rnd))
    # 7 water in litres
    e, v = e_whole(1, 2, 5, L_)
    its.append(mcq(fig(model_svg([(Fraction(2, 5), F(2, 5)), (Fraction(3, 5), "?")], (1, 0, 1), L_)) +
                   "Mei Ling had a bottle with 1 ℓ of water. She drank %s ℓ of it. How much water was left?" % fr(2, 5)
                   + SIMPLE, v, wrong_whole(1, 2, 5), "Left = 1 ℓ − %s ℓ. " % fr(2, 5) + e, rnd, L_))
    # 8 bottle 3/4 full, poured out
    word("A bottle was %s full of water. Ethan poured out %s of the bottle to water a plant. "
         "What fraction of the bottle is full now?" % (fr(3, 4), fr(1, 8)), F(3, 4), F(1, 8), "-")
    # 9 ribbon left
    x, y = F(5, 6), F(1, 3)
    r = val(x) - val(y)
    word("Siti had %s m of ribbon. She used %s m to wrap a present. How much ribbon did she have left?"
         % (fr(5, 6), fr(1, 3)), x, y, "-", M, pre="Left = total − used. ",
         figure=fig(model_svg([(val(y), y), (r, "?")], x, M)))
    # 10 run comparison
    x, y = F(7, 10), F(2, 5)
    word("On Sports Day, Ryan ran %s km and Chloe ran %s km. How much further did Ryan run than Chloe?"
         % (fr(7, 10), fr(2, 5)), x, y, "-", KM, pre="“How much further” means subtract. ",
         figure=fig(compare_svg([("Ryan", val(x), x), ("Chloe", val(y), y)], "?", KM)))
    # 11 bubble tea comparison
    x, y = F(7, 12), F(1, 4)
    word("Xin Yi and Zhi Hao each bought a cup of bubble tea of the same size. Xin Yi drank %s of her cup. "
         "Zhi Hao drank %s of his cup. How much more of a cup did Xin Yi drink than Zhi Hao?" % (fr(7, 12), fr(1, 4)),
         x, y, "-", pre="“How much more” means subtract. ",
         figure=fig(compare_svg([("Xin Yi", val(x), x), ("Zhi Hao", val(y), y)], "?", None)))
    # 12 flour total
    word("Mrs Ng used %s kg of flour to make kueh and %s kg of flour to make cookies. How much flour did she use altogether?"
         % (fr(3, 4), fr(1, 8)), F(3, 4), F(1, 8), "+", KG)
    # 13 students walk or bus
    word("In a class, %s of the students walk to school and %s of the students take the school bus. "
         "What fraction of the class walk or take the school bus?" % (fr(2, 5), fr(3, 10)), F(2, 5), F(3, 10), "+")
    # 14 money left
    v = 1 - Fraction(1, 4) - Fraction(3, 8)
    e = ("Model: the whole bar is all her money. She spent %s + %s = %s + %s = %s. "
         "Left = %s − %s = <b>%s</b>." % (fr(1, 4), fr(3, 8), fr(2, 8), fr(3, 8), fr(5, 8), fr(8, 8), fr(5, 8), fr(3, 8)))
    its.append(mcq(fig(model_svg([(Fraction(1, 4), F(1, 4)), (Fraction(3, 8), F(3, 8)), (v, "?")], "all her money", None)) +
                   "Mdm Wong spent %s of her money on groceries and %s of her money on a pair of shoes. "
                   "What fraction of her money did she have left?" % (fr(1, 4), fr(3, 8)) + SIMPLE, v,
                   [Fraction(5, 8), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)], e, rnd))
    # 15 garden plot
    v = 1 - Fraction(1, 2) - Fraction(1, 6)
    assert v == Fraction(1, 3)
    e = ("Use sixths: %s = %s. Chilli and kangkong take up %s + %s = %s of the plot. "
         "The rest is %s − %s = %s. Simplify: %s = <b>%s</b>." % (fr(1, 2), fr(3, 6), fr(3, 6), fr(1, 6), fr(4, 6),
                                                                fr(6, 6), fr(4, 6), fr(2, 6), fr(2, 6), fr(1, 3)))
    its.append(mcq(fig(model_svg([(Fraction(1, 2), F(1, 2)), (Fraction(1, 6), F(1, 6)), (v, "?")], "1 plot", None)) +
                   "Mr Rahman has a garden plot at his HDB block. He plants chilli on %s of the plot and kangkong on %s of it. "
                   "He plants bayam on the rest. What fraction of the plot has bayam?" % (fr(1, 2), fr(1, 6)) + SIMPLE, v,
                   [Fraction(2, 3), Fraction(3, 4), Fraction(1, 2), Fraction(1, 6)], e, rnd))
    # 16 walk to the library
    word("Kumar walked %s km from his HDB block to the MRT station. Then he walked %s km from the station to the library. "
         "How far did he walk altogether?" % (fr(1, 4), fr(5, 8)), F(1, 4), F(5, 8), "+", KM)
    # 17 two jugs, more than 1
    word("Jug A has %s ℓ of bandung. Jug B has %s ℓ of bandung. How much bandung is there altogether?"
         % (fr(3, 4), fr(5, 8)), F(3, 4), F(5, 8), "+", L_, post=" There is more than 1 ℓ.")
    # 18 at first
    x, y = F(1, 4), F(5, 12)
    word("Devi poured %s ℓ of water from a bottle into a cup. There was %s ℓ of water left in the bottle. "
         "How much water was in the bottle at first?" % (fr(1, 4), fr(5, 12)), x, y, "+", L_,
         pre="At first = poured out + left. ", extra=[val(y) - val(x)],
         figure=fig(model_svg([(val(x), x), (val(y), y)], "?", L_)))
    # 19 book read
    word("Arjun read %s of a storybook on Saturday and %s of it on Sunday. What fraction of the book did he read "
         "on the two days?" % (fr(2, 9), fr(1, 3)), F(2, 9), F(1, 3), "+")
    # 20 tank
    word("A fish tank was %s full of water. Mr Kumar let out some water to clean it. Then the tank was %s full. "
         "What fraction of the tank did he let out?" % (fr(11, 12), fr(1, 3)), F(11, 12), F(1, 3), "-",
         pre="Water let out = before − after. ")
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_like = one_bar_svg(7, 2, 3)
    f_bars = two_bars_svg(2, 1, 8, 3, 8, W=360, labels=True)
    f_over = wholes_svg(5, 4, 3)
    f_whole = one_bar_svg(8, 8, 0, crossed=3)
    f_model = model_svg([(Fraction(1, 3), F(1, 3)), (Fraction(1, 2), "?")], F(5, 6), M)
    return (
        "<h2>Like denominators: add or subtract the numerators</h2>"
        "<p>When the denominators are the same, the parts are the same size. Add or subtract the numerators. "
        "The denominator does not change.</p>"
        "<figure class='sn-fig'>" + f_like +
        "<figcaption>2 sevenths + 3 sevenths = 5 sevenths.</figcaption></figure>"
        + ex("Example", fr(2, 7) + " + " + fr(3, 7) + " = ?", "Add the numerators: 2 + 3 = 5. Keep the denominator 7.", fr(5, 7))
        + ex("Example", fr(8, 9) + " − " + fr(3, 9) + " = ?", "Subtract the numerators: 8 − 3 = 5. Keep the denominator 9.", fr(5, 9)) +
        "<h2>Related denominators: make the denominators the same</h2>"
        "<p>Halves and eighths are different sizes, so you cannot add them as they are. 8 is a multiple of 2, "
        "so change " + fr(1, 2) + " into eighths. Multiply the numerator and the denominator by the same number.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines cut the top bar into eighths: " + fr(1, 2) + " = " + fr(4, 8) + ".</figcaption></figure>"
        + ex("Example", fr(1, 2) + " + " + fr(3, 8) + " = ?",
             "2 × 4 = 8, so " + fr(1, 2) + " = " + fr(4, 8) + ". Then " + fr(4, 8) + " + " + fr(3, 8) + " = " + fr(7, 8) + ".", fr(7, 8))
        + ex("Example", fr(5, 6) + " − " + fr(1, 3) + " = ?",
             "3 × 2 = 6, so " + fr(1, 3) + " = " + fr(2, 6) + ". Then " + fr(5, 6) + " − " + fr(2, 6) + " = " + fr(3, 6) +
             " = " + fr(1, 2) + ".", fr(1, 2)) +
        "<h2>Answers greater than 1</h2>"
        "<p>If the answer is an improper fraction, write it as a mixed number.</p>"
        "<figure class='sn-fig'>" + f_over +
        "<figcaption>" + fr(4, 5) + " + " + fr(3, 5) + " = " + fr(7, 5) + ". 5 fifths make 1 whole, so " + fr(7, 5) +
        " = 1 " + fr(2, 5) + ".</figcaption></figure>" +
        "<h2>Give the answer in simplest form</h2>"
        "<p>Divide the numerator and the denominator by the same number until you cannot divide any more.</p>" +
        table(["Calculation", "Working", "Simplest form"], [
            [fr(1, 8) + " + " + fr(5, 8), fr(6, 8) + ", then divide 6 and 8 by 2", fr(3, 4)],
            [fr(1, 4) + " + " + fr(5, 12), fr(3, 12) + " + " + fr(5, 12) + " = " + fr(8, 12) + ", then divide 8 and 12 by 4", fr(2, 3)],
            [fr(7, 8) + " + " + fr(3, 8), fr(10, 8) + " = 1 " + fr(2, 8), "1 " + fr(1, 4)],
        ]) +
        "<h2>Subtracting from a whole</h2>"
        "<p>Write 1 whole as a fraction with the same denominator, such as 1 = " + fr(8, 8) + ".</p>"
        "<figure class='sn-fig'>" + f_whole +
        "<figcaption>1 − " + fr(3, 8) + " = " + fr(8, 8) + " − " + fr(3, 8) + " = " + fr(5, 8) + ".</figcaption></figure>" +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar for the whole amount. Mark the part you know and put “?” on the part you need to find. "
        "Then decide whether to add or subtract.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>Siti had " + fr(5, 6) + " m of ribbon and used " + fr(1, 3) + " m. Left = " + fr(5, 6) + " − " +
        fr(1, 3) + ".</figcaption></figure>"
        + ex("Example", "Siti had " + fr(5, 6) + " m of ribbon. She used " + fr(1, 3) + " m. How much ribbon was left?",
             fr(5, 6) + " − " + fr(2, 6) + " = " + fr(3, 6) + " = " + fr(1, 2) + ".", fr(1, 2) + " m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 14) + " (adding the denominators)",
             "Keep the denominator: " + fr(5, 7)],
            [fr(1, 2) + " + " + fr(3, 8) + " = " + fr(4, 8) + " (not making a common denominator)",
             "Change " + fr(1, 2) + " to " + fr(4, 8) + " first: " + fr(4, 8) + " + " + fr(3, 8) + " = " + fr(7, 8)],
            [fr(1, 8) + " + " + fr(5, 8) + " = " + fr(6, 8) + " (not simplifying)",
             "Divide by 2: " + fr(3, 4)],
            [fr(4, 5) + " + " + fr(3, 5) + " = " + fr(7, 5) + " (leaving an improper fraction)",
             "Write it as a mixed number: 1 " + fr(2, 5)],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 fractions for adding and subtracting?",
     "a": "In Primary 4, students add and subtract proper fractions with denominators up to 12, where one denominator is a multiple of the other. They give answers in simplest form and write answers greater than 1 as mixed numbers."},
    {"q": "How do I explain adding fractions with different denominators to my child?",
     "a": "Make the parts the same size first. For 1/2 + 3/8, change 1/2 into 4/8, then add: 4/8 + 3/8 = 7/8."},
    {"q": "What is the most common mistake when adding fractions?",
     "a": "Adding the denominators, as in 2/7 + 3/7 = 5/14. The parts are still sevenths, so the answer is 5/7."},
    {"q": "Is adding and subtracting fractions in the MOE syllabus for Primary 4?",
     "a": "Yes. It is part of Fractions in the Primary 4 Standard Mathematics syllabus (MOE 2021). In Primary 5, students go on to unlike denominators and mixed numbers."},
]


def gen_unit():
    rnd = random.Random(64808)
    sets = [set_like(rnd), set_related(rnd), set_simplest(rnd), set_whole(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "adding-and-subtracting-fractions", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Adding and Subtracting Fractions",
        "seo_title": "P4 Adding and Subtracting Fractions Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Adding and Subtracting Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting fractions with denominators not exceeding 12 (one denominator a multiple of the other)",
        "meta_desc": "Free P4 maths practice: add and subtract fractions with like and related denominators, simplest form and word problems. 100 questions with answers.",
        "key_big": "Make the denominators the same, then add or subtract only the numerators.",
        "key_sub": "1/2 + 3/8 = 4/8 + 3/8 = 7/8",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(two bars|bar of|bar model)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
