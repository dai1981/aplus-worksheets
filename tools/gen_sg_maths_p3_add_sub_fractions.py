# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Adding and Subtracting Fractions
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 3: Fractions)
  python3 tools/gen_sg_maths_p3_add_sub_fractions.py
Two related fractions within one whole (denominators up to 12): like fractions, related fractions with
fraction bars, simplest form, subtracting from 1, and word problems (cakes, water bottles, bar models).
Every answer is a fraction in simplest form that is not more than 1 (no mixed numbers in P3).
Wrong choices come from real mistakes and are never equal in value to the answer or to each other.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
FILL3 = "#8fb8e8"     # bar models
WATER = "#8fc6ee"     # water in a bottle
CAKE = "#f3d9b1"      # cake not eaten
RED = "#c0392b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
        10: "tenths", 11: "elevenths", 12: "twelfths"}
SIMPLE = "<br>Give your answer in its simplest form."


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(v):
    """A Fraction from 0 to 1 in simplest form: '7/12' or '1'."""
    assert 0 < v <= 1, v
    if v == 1:
        return "1"
    return fr(v.numerator, v.denominator)


def F(n, d):
    return (n, d)


def val(x):
    return Fraction(x[0], x[1])


def lcm(a, b):
    return a * b // math.gcd(a, b)


L_ = " ℓ"
M = " m"
KM = " km"
KG = " kg"


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
    cands are Fractions or strings. A Fraction equal to the answer or another choice, zero or less,
    or more than 1 (a mixed number, not taught in P3) is skipped."""
    if isinstance(correct, Fraction):
        cv, cs = correct, withu(correct, unit)
    else:
        cv, cs = None, correct
    seen, vals, pick = {cs}, set(), []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, Fraction):
            if c <= 0 or c > 1 or c == cv or c in vals:
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
    """Width of a label drawn by lab_svg. lab is (n, d) or a string."""
    if isinstance(lab, str):
        return (size + 2) * 0.6 * len(lab)
    n, d = lab
    t = size * 0.62 * max(len(str(n)), len(str(d))) + 4
    if unit:
        t += size * 0.55 * len(unit) + 3
    return t


def lab_svg(cx, yc, lab, unit, size=15):
    """Fraction with unit (or a string such as '?') centred at cx; yc is the middle line."""
    if isinstance(lab, str):
        return txt(cx, yc + size * 0.36, lab, size + 2)
    n, d = lab
    x = cx - lab_w(lab, unit, size) / 2
    fw = size * 0.62 * max(len(str(n)), len(str(d))) + 4
    s = [sfr(x + fw / 2, yc - 5, n, d, size)]
    if unit:
        s.append(txt(x + fw + 4, yc + size * 0.36, unit.strip(), size, anchor="start", weight="400"))
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


def pie_body(cx, cy, R, d, k1, k2=0, crossed=0, base="#fff"):
    """A circle cut into d equal slices from 12 o'clock, clockwise. First k1 slices green, next k2 yellow,
    the rest in base colour. The first `crossed` slices get a red X."""
    s = []
    for i in range(d):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else base)
        a0 = -math.pi / 2 + 2 * math.pi * i / d
        a1 = a0 + 2 * math.pi / d
        s.append("<path d='M%.1f %.1f L%.2f %.2f A%.1f %.1f 0 0 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='2.2'/>"
                 % (cx, cy, cx + R * math.cos(a0), cy + R * math.sin(a0), R, R,
                    cx + R * math.cos(a1), cy + R * math.sin(a1), col, LINE))
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='%s' stroke-width='3'/>" % (cx, cy, R, LINE))
    for i in range(crossed):
        am = -math.pi / 2 + 2 * math.pi * (i + 0.5) / d
        rr = 0.66 * R
        s.append(cross(cx + rr * math.cos(am), cy + rr * math.sin(am), min(9, 0.55 * rr * math.sin(math.pi / d))))
    return "".join(s)


def pie_svg(d, k1=0, k2=0, crossed=0, base="#fff", R=46, label="circle"):
    lab = "%s cut into %d equal slices, %d green, %d yellow, %d crossed out" % (label, d, k1, k2, crossed)
    return svg_wrap(12 + 2 * R, 12 + 2 * R, pie_body(6 + R, 6 + R, R, d, k1, k2, crossed, base), lab)


def bottle_svg(d, k, crossed=0):
    """A bottle cut into d equal bands. The bottom k bands hold water; the top `crossed` of them get a red X."""
    bw, bh = 64, 120
    x0, y0 = 6, 34
    s = ["<rect x='%d' y='6' width='24' height='16' rx='2' fill='#fff' stroke='%s' stroke-width='2.2'/>" % (x0 + bw / 2 - 12, LINE),
         "<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2.2'/>"
         % (x0 + bw / 2 - 12, 22, x0 + bw / 2 - 12, 26, x0 + bw / 2 + 12, 26, x0 + bw / 2 + 12, 22, LINE),
         "<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2.2'/>"
         % (x0 + bw / 2 - 12, 26, x0, y0, x0 + bw, y0, x0 + bw / 2 + 12, 26, LINE)]
    h = bh / d
    for i in range(d):
        y = y0 + bh - (i + 1) * h
        s.append("<rect x='%d' y='%.2f' width='%d' height='%.2f' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x0, y, bw, h, WATER if i < k else "#fff", LINE))
        if k - crossed <= i < k:
            s.append(cross(x0 + bw / 2, y + h / 2, min(9, h / 2 - 2)))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, y0, bw, bh, LINE))
    lab = "bottle marked in %d equal parts: water in %d parts, %d of them crossed out" % (d, k, crossed)
    return svg_wrap(x0 + bw + 6, y0 + bh + 6, "".join(s), lab)


def model_svg(segs, total, unit, W=300):
    """Part-whole bar model. segs: list of (value, label) where label is (n, d) or '?'.
    total: label for the whole bar, (n, d) or a string, shown with a brace above."""
    tv = sum(v for v, _ in segs)
    x0 = 6
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
    """N/L with 0 < N <= L. Simplify and state the answer."""
    assert 0 < N <= L
    t = ""
    if N == L:
        t += "%s = 1 whole. " % fr(N, L)
    else:
        g = math.gcd(N, L)
        if g > 1:
            t += "Simplify: divide the numerator and denominator of %s by %d to get %s. " % (fr(N, L), g, fr(N // g, L // g))
    v = Fraction(N, L)
    return t + "The answer is <b>%s</b>." % withu(v, unit), v


def common(d1, d2):
    L = lcm(d1, d2)
    if d1 == d2:
        return "The denominators are the same, so the denominator stays %d. " % d1
    return "%d is a multiple of %d, so change both fractions into %s. " % (L, min(d1, d2), WORD[L])


def e_calc(x, y, op, unit=None):
    """Step explanation for x op y."""
    (n1, d1), (n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    t = common(d1, d2)
    rw = ["%s = %s" % (fr(n, d), fr(n * L // d, L)) for n, d in (x, y) if d != L]
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
    (n1, d1), (n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    N = a + b if op == "+" else a - b
    g = math.gcd(N, L)
    c = []
    if op == "+":
        c.append(Fraction(n1 + n2, d1 + d2))                     # added the numerators and the denominators
        if d1 != d2:
            c.append(Fraction(n1 + n2, L))                       # changed the denominator but not the numerators
            c.append(Fraction(a + n2, L) if d2 != L else Fraction(n1 + b, L))   # changed only one fraction
        if 1 < g < L:
            c.append(Fraction(N // g, L))                        # divided only the numerator
        c.append(Fraction(abs(a - b), L) if a != b else None)    # subtracted instead
        c.append(Fraction(N - 1, L) if N > 1 else None)          # miscounted the parts
        c.append(Fraction(N + 1, L))
        c.append(Fraction(N + 2, L))
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
        c.append(Fraction(N + 2, L))
        c.append(Fraction(a, L) if a < L else None)              # forgot to subtract
    return c


def calc_q(x, y, op, prompt=SIMPLE):
    sym = "+" if op == "+" else "−"
    return "%s %s %s = ?" % (fr(*x), sym, fr(*y)) + prompt


def calc(x, y, op, rnd, prompt=SIMPLE, extra=None, figure=""):
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    assert 0 < r <= 1
    c = (extra or []) + wrong(x, y, op)
    return mcq(figure + calc_q(x, y, op, prompt), r, c, e_calc(x, y, op), rnd)


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


def kind(x, y, op, like=None, simplify=None):
    """Checks that a question is of the kind the set says: two related fractions, answer within one whole."""
    (n1, d1), (n2, d2) = x, y
    assert 0 < n1 < d1 <= 12 and 0 < n2 < d2 <= 12
    assert max(d1, d2) % min(d1, d2) == 0, (x, y)
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    N = a + b if op == "+" else a - b
    assert 0 < N < L, (x, y)
    if like is not None:
        assert (d1 == d2) == like, (x, y)
    if simplify is not None:
        assert (math.gcd(N, L) > 1) == simplify, (x, y)


# ------------------------------------------------------------ subtract from 1
def e_whole(n, d, unit=None):
    """Explanation for 1 − n/d."""
    t = "Write 1 whole as %s. Then %s − %s = %s. " % (fr(d, d), fr(d, d), fr(n, d), fr(d - n, d))
    g = math.gcd(d - n, d)
    if g > 1:
        t += "Simplify: %s = %s. " % (fr(d - n, d), fr((d - n) // g, d // g))
    v = 1 - Fraction(n, d)
    return t + "The answer is <b>%s</b>." % withu(v, unit), v


def wrong_whole(n, d):
    g = math.gcd(d - n, d)
    c = [Fraction(n, d)]                                 # wrote the part taken away
    if g > 1:
        c.append(Fraction((d - n) // g, d))              # divided only the numerator
    c.append(Fraction(n - 1, d) if n > 1 else None)      # took 1 from the numerator
    c.append(Fraction(d - n - 1, d) if d - n > 1 else None)   # miscounted
    c.append(Fraction(d - n + 1, d))
    c.append(Fraction(d - 1, d))
    return c


# ============================================================ set 1: like fractions
def set_like(rnd):
    SPOTS.left = []
    its = []
    # A: pictures
    q = (fig(one_bar_svg(11, 2, 5)) + "The bar is cut into 11 equal parts. The green parts show %s. The yellow parts show %s. "
         "What is %s + %s?" % (fr(2, 11), fr(5, 11), fr(2, 11), fr(5, 11)))
    e = "Count the shaded parts: 2 elevenths + 5 elevenths = 7 elevenths. The parts are still elevenths. The answer is <b>%s</b>." % fr(7, 11)
    its.append(mcq(q, Fraction(7, 11), [Fraction(7, 22), Fraction(5, 11), Fraction(3, 11), Fraction(6, 11)], e, rnd))
    q = (fig(pie_svg(8, 2, 5)) + "The circle is cut into 8 equal parts. "
         "What fraction of the circle is green or yellow?")
    e = "2 eighths are green and 5 eighths are yellow. %s + %s = <b>%s</b>." % (fr(2, 8), fr(5, 8), fr(7, 8))
    its.append(mcq(q, Fraction(7, 8), [Fraction(7, 16), Fraction(5, 8), Fraction(3, 8), Fraction(1, 8)], e, rnd))
    q = (fig(one_bar_svg(7, 6, 0, crossed=2)) + "The bar shows %s. Then %s is crossed out. What is %s − %s?"
         % (fr(6, 7), fr(2, 7), fr(6, 7), fr(2, 7)))
    e = "6 sevenths take away 2 sevenths leaves 4 sevenths. Count the green parts with no X. The answer is <b>%s</b>." % fr(4, 7)
    its.append(mcq(q, Fraction(4, 7), [Fraction(2, 7), Fraction(6, 7), Fraction(3, 7), Fraction(5, 7)], e, rnd))
    q = (fig(pie_svg(5, 2, 2)) + "The circle is cut into 5 equal parts. What is %s + %s?" % (fr(2, 5), fr(2, 5)))
    e = "2 fifths + 2 fifths = 4 fifths. The answer is <b>%s</b>." % fr(4, 5)
    its.append(mcq(q, Fraction(4, 5), [Fraction(4, 10), Fraction(2, 5), Fraction(3, 5), Fraction(1, 5)], e, rnd))
    # B: add, no simplifying
    for x, y in [(F(1, 5), F(2, 5)), (F(3, 7), F(2, 7)), (F(2, 9), F(5, 9)), (F(5, 11), F(3, 11)),
                 (F(3, 10), F(4, 10)), (F(4, 12), F(3, 12)), (F(1, 8), F(6, 8))]:
        kind(x, y, "+", like=True, simplify=False)
        its.append(calc(x, y, "+", rnd))
    # C: subtract, no simplifying
    for x, y in [(F(7, 9), F(3, 9)), (F(5, 6), F(4, 6)), (F(9, 10), F(6, 10)), (F(11, 12), F(6, 12)),
                 (F(6, 7), F(4, 7)), (F(5, 8), F(2, 8))]:
        kind(x, y, "-", like=True, simplify=False)
        its.append(calc(x, y, "-", rnd))
    # D: makes 1 whole
    its.append(calc(F(3, 7), F(4, 7), "+", rnd, prompt=""))
    # E: missing number
    e = "Find the missing number by subtracting: %s − %s = %s. Check: %s + %s = %s. The answer is <b>%s</b>." % (
        fr(7, 9), fr(2, 9), fr(5, 9), fr(2, 9), fr(5, 9), fr(7, 9), fr(5, 9))
    its.append(mcq("%s + <b>?</b> = %s" % (fr(2, 9), fr(7, 9)), Fraction(5, 9),
                   [Fraction(1), Fraction(4, 9), Fraction(7, 9)], e, rnd))
    # F: spot the mistake
    e = ("The parts are fifths, so the denominator stays 5: 1 fifth + 3 fifths = 4 fifths. "
         "%s + %s = <b>%s</b>. Farah added the denominators too, which gave tenths." % (fr(1, 5), fr(3, 5), fr(4, 5)))
    its.append(mcq("Farah wrote %s + %s = %s. What mistake did she make?" % (fr(1, 5), fr(3, 5), fr(4, 10)),
                   "She added the denominators",
                   ["She forgot to simplify", "She subtracted the numerators", "There is no mistake"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Like fractions review", "items": its}


# ============================================================ set 2: related fractions
def set_related(rnd):
    SPOTS.left = []
    its = []
    # A: common denominator
    for x, y, op in [(F(1, 2), F(1, 4), "+"), (F(2, 3), F(1, 6), "-")]:
        d1, d2 = x[1], y[1]
        big, small = max(d1, d2), min(d1, d2)
        e = ("%d is a multiple of %d (%d × %d = %d), so both fractions can be written in %s. "
             "The common denominator is <b>%d</b>." % (big, small, small, big // small, big, WORD[big], big))
        sym = "+" if op == "+" else "−"
        cands = [str(d1 * d2), str(d1 + d2), str(small)]
        if d1 * d2 == big:
            cands = [str(d1 + d2), str(small), str(big * 2)]
        its.append(mcq("To work out %s %s %s, we need the same denominator. What denominator should we use?"
                       % (fr(x[0], d1), sym, fr(y[0], d2)), str(big), cands, e, rnd))
    # B: equivalent fraction
    for n, d, L, bad in [(1, 2, 6, ["1", "5", "2"]), (2, 5, 10, ["2", "7", "5"])]:
        k = L // d
        e = ("%d × %d = %d, so the denominator was multiplied by %d. Multiply the numerator by %d too: %d × %d = <b>%d</b>. "
             "So %s = %s." % (d, k, L, k, k, n, k, n * k, fr(n, d), fr(n * k, L)))
        its.append(mcq("%s = %s. What is the missing number?" % (fr(n, d), fr("<b>?</b>", L)), str(n * k), bad, e, rnd))
    # C: fraction bars, rename
    for x, y in [(F(1, 2), F(1, 8)), (F(2, 3), F(1, 6))]:
        n1, d1, n2, d2 = x[0], x[1], y[0], y[1]
        L = lcm(d1, d2)
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "The bars show %s (green) and %s (yellow). The dashed lines cut both bars into %s. "
             "Which shows both fractions in %s?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
        its.append(mcq(q, r, c, e, rnd))
    # D: add with fraction bars
    for x, y in [(F(1, 2), F(1, 4)), (F(1, 4), F(3, 8)), (F(1, 3), F(2, 9)), (F(1, 5), F(1, 10))]:
        kind(x, y, "+", like=False, simplify=False)
        L = lcm(x[1], y[1])
        f = fig(two_bars_svg(x[1], x[0], y[1], y[0], L))
        its.append(calc(x, y, "+", rnd, figure=f + "The bars show %s (green) and %s (yellow). " % (fr(*x), fr(*y))))
    # E: add
    for x, y in [(F(1, 2), F(3, 8)), (F(2, 5), F(3, 10)), (F(1, 3), F(1, 12)), (F(1, 6), F(5, 12))]:
        kind(x, y, "+", like=False, simplify=False)
        its.append(calc(x, y, "+", rnd))
    # F: subtract with fraction bars
    for x, y in [(F(3, 4), F(1, 8)), (F(1, 2), F(1, 8))]:
        kind(x, y, "-", like=False, simplify=False)
        L = lcm(x[1], y[1])
        f = fig(two_bars_svg(x[1], x[0], y[1], y[0], L))
        its.append(calc(x, y, "-", rnd, figure=f + "The bars show %s (green) and %s (yellow). " % (fr(*x), fr(*y))))
    # G: subtract
    for x, y in [(F(7, 9), F(1, 3)), (F(9, 10), F(3, 5)), (F(5, 6), F(2, 3)), (F(11, 12), F(1, 3))]:
        kind(x, y, "-", like=False, simplify=False)
        its.append(calc(x, y, "-", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Related fractions with fraction bars", "items": its}


# ============================================================ set 3: simplest form
def set_simplest(rnd):
    SPOTS.left = []
    its = []
    # A: write in simplest form
    # wrong: divided only the numerator, took 1 from the top and bottom, the unshaded part
    for n, d, bad in [(2, 4, [fr(1, 4), fr(1, 3), fr(3, 4)]),
                      (3, 9, [fr(1, 9), fr(2, 8), fr(6, 9)]),
                      (6, 8, [fr(3, 8), fr(5, 7), fr(2, 8)]),
                      (4, 10, [fr(2, 10), fr(3, 9), fr(6, 10)])]:
        g = math.gcd(n, d)
        r = Fraction(n, d)
        e = ("%d and %d can both be divided by %d. %d ÷ %d = %d and %d ÷ %d = %d, so %s = <b>%s</b>."
             % (n, d, g, n, g, n // g, d, g, d // g, fr(n, d), show(r)))
        its.append(mcq("Write %s in its simplest form." % fr(n, d), r, bad, e, rnd))
    # B: pictures
    for d, k in [(8, 6), (10, 4)]:
        r = Fraction(k, d)
        g = math.gcd(k, d)
        e = ("%d of the %d parts are shaded: %s. Divide the numerator and denominator by %d: %s = <b>%s</b>."
             % (k, d, fr(k, d), g, fr(k, d), show(r)))
        its.append(mcq(fig(one_bar_svg(d, k, 0)) + "What fraction of the bar is shaded? Give your answer in its simplest form.",
                       r, [fr(k // g, d), fr(d - k, d), fr(k - 1, d)], e, rnd))
    # C: like fractions, then simplify
    for x, y, op in [(F(1, 8), F(5, 8), "+"), (F(7, 10), F(3, 10), "-"), (F(5, 12), F(1, 12), "+"),
                     (F(2, 9), F(4, 9), "+"), (F(11, 12), F(2, 12), "-")]:
        kind(x, y, op, like=True, simplify=True)
        its.append(calc(x, y, op, rnd))
    # D: related fractions, then simplify
    for x, y, op in [(F(1, 3), F(1, 6), "+"), (F(2, 3), F(1, 6), "-"), (F(1, 4), F(5, 12), "+"),
                     (F(1, 2), F(3, 10), "+"), (F(9, 10), F(1, 2), "-"), (F(3, 4), F(5, 12), "-"), (F(1, 2), F(1, 6), "+")]:
        kind(x, y, op, like=False, simplify=True)
        its.append(calc(x, y, op, rnd))
    # E: what to do next
    assert Fraction(1, 4) + Fraction(1, 12) == Fraction(1, 3)
    e = ("%s is not in its simplest form. 4 and 12 can both be divided by 4: %s = <b>%s</b>. "
         "%s is equal, but it can still be simplified." % (fr(4, 12), fr(4, 12), fr(1, 3), fr(2, 6)))
    its.append(mcq("Wei Ming worked out %s + %s and got %s. What should he do next?" % (fr(1, 4), fr(1, 12), fr(4, 12)),
                   "Write %s as %s" % (fr(4, 12), fr(1, 3)),
                   ["Nothing. The answer is finished", "Write %s as %s" % (fr(4, 12), fr(2, 6)),
                    "Write %s as %s" % (fr(4, 12), fr(1, 12))], e, rnd))
    assert Fraction(1, 2) + Fraction(1, 10) == Fraction(3, 5)
    e = ("%s = %s, and %s + %s = %s, so her working is right. But 6 and 10 can both be divided by 2, "
         "so the answer in simplest form is <b>%s</b>." % (fr(1, 2), fr(5, 10), fr(5, 10), fr(1, 10), fr(6, 10), fr(3, 5)))
    its.append(mcq("Nurul wrote %s + %s = %s. Is she right?" % (fr(1, 2), fr(1, 10), fr(6, 10)),
                   "Yes, but %s should be written as %s" % (fr(6, 10), fr(3, 5)),
                   ["No, the answer is %s" % fr(2, 12), "No, the answer is %s" % fr(2, 10),
                    "Yes, and %s is in simplest form" % fr(6, 10)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Answers in simplest form", "items": its}


# ============================================================ set 4: subtract from 1
def set_whole(rnd):
    SPOTS.left = []
    its = []
    # A: pictures
    q = (fig(one_bar_svg(8, 8, 0, crossed=3)) + "The whole bar is 1. It is cut into 8 equal parts and 3 parts are crossed out. "
         "What is 1 − %s?" % fr(3, 8))
    e, v = e_whole(3, 8)
    its.append(mcq(q, v, wrong_whole(3, 8), "Count the parts with no X: 5 eighths. " + e, rnd))
    q = (fig(pie_svg(10, 0, 0, 3, CAKE, label="cake")) + "A cake is cut into 10 equal slices. Siti and her friends eat 3 slices. "
         "What fraction of the cake is left?")
    e, v = e_whole(3, 10)
    its.append(mcq(q, v, wrong_whole(3, 10),
                   "The whole cake is %s. 3 slices are %s. " % (fr(10, 10), fr(3, 10)) + e, rnd))
    e = "1 whole cut into ninths has 9 ninths, so 1 = %s. The missing number is <b>9</b>." % fr(9, 9)
    its.append(mcq("1 = %s. What is the missing number?" % fr("<b>?</b>", 9), "9", ["1", "8", "10"], e, rnd))
    # B: 1 − a fraction
    for n, d in [(3, 5), (2, 7), (4, 9), (5, 12), (7, 10), (5, 6), (5, 11)]:
        e, v = e_whole(n, d)
        its.append(mcq("1 − %s = ?" % fr(n, d) + SIMPLE, v, wrong_whole(n, d), e, rnd))
    # C: 1 − a fraction, then simplify
    for n, d in [(2, 6), (6, 10), (8, 12)]:
        e, v = e_whole(n, d)
        assert math.gcd(d - n, d) > 1
        its.append(mcq("1 − %s = ?" % fr(n, d) + SIMPLE, v, wrong_whole(n, d), e, rnd))
    # D: missing numbers
    e = "%s + ? = 1 means 1 − %s. Write 1 as %s: %s − %s = <b>%s</b>." % (
        fr(5, 8), fr(5, 8), fr(8, 8), fr(8, 8), fr(5, 8), fr(3, 8))
    its.append(mcq("%s + <b>?</b> = 1" % fr(5, 8), fr(3, 8), [fr(5, 8), fr(4, 8), fr(2, 8)], e, rnd))
    e = "? + %s = 1 means 1 − %s. Write 1 as %s: %s − %s = <b>%s</b>." % (
        fr(2, 7), fr(2, 7), fr(7, 7), fr(7, 7), fr(2, 7), fr(5, 7))
    its.append(mcq("<b>?</b> + %s = 1" % fr(2, 7), Fraction(5, 7),
                   [Fraction(2, 7), Fraction(4, 7), Fraction(6, 7), Fraction(1, 7)], e, rnd))
    e = ("1 − ? = %s. Write 1 as %s. %s − %s = %s, so the missing fraction is <b>%s</b>. "
         "Check: 1 − %s = %s." % (fr(1, 6), fr(6, 6), fr(6, 6), fr(1, 6), fr(5, 6), fr(5, 6), fr(5, 6), fr(1, 6)))
    its.append(mcq("1 − <b>?</b> = %s" % fr(1, 6), fr(5, 6), [fr(1, 6), fr(4, 6), fr(6, 7)], e, rnd))
    # E: pictures of things
    q = (fig(pie_svg(4, 0, 0, 1, CAKE, label="cake")) + "Mrs Lim cut a cake into 4 equal pieces. Her son ate 1 piece. "
         "What fraction of the cake was left?")
    e, v = e_whole(1, 4)
    its.append(mcq(q, v, [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)],
                   "1 piece is %s of the cake. " % fr(1, 4) + e, rnd))
    q = (fig(bottle_svg(6, 6, crossed=1)) + "The bottle was full of water. Raju drank %s of the water. "
         "What fraction of the bottle still has water?" % fr(1, 6))
    e, v = e_whole(1, 6)
    its.append(mcq(q, v, wrong_whole(1, 6), "A full bottle is 1. " + e, rnd))
    # F: ideas
    e = ("%s means 6 sixths, which is 1 whole. %s and %s are less than 1, and %s is a half. "
         "The answer is <b>%s</b>." % (fr(6, 6), fr(1, 6), fr(5, 6), fr(6, 12), fr(6, 6)))
    its.append(mcq("Which fraction is equal to 1?", fr(6, 6), [fr(1, 6), fr(5, 6), fr(6, 12)], e, rnd))
    e = ("1 whole is %s, not 1 part. %s − %s = %s. Kumar took 1 from the numerator 3 and got %s. "
         "The answer is <b>%s</b>." % (fr(8, 8), fr(8, 8), fr(3, 8), fr(5, 8), fr(2, 8), fr(5, 8)))
    its.append(mcq("Kumar wrote 1 − %s = %s. What is the correct answer?" % (fr(3, 8), fr(2, 8)), fr(5, 8),
                   [fr(2, 8), fr(3, 8), fr(4, 8)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Subtracting from 1", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    SPOTS.left = []
    its = []

    def word(q, x, y, op, unit=None, extra=None, pre="", post="", figure=""):
        r = val(x) + val(y) if op == "+" else val(x) - val(y)
        assert 0 < r <= 1
        c = (extra or []) + wrong(x, y, op)
        e = pre + e_calc(x, y, op, unit) + post
        its.append(mcq(figure + q + SIMPLE, r, c, e, rnd, unit))
        return r

    # 1 cake eaten together
    word("Ali and Siti shared a cake. Ali ate %s of the cake (green) and Siti ate %s of it (yellow). "
         "What fraction of the cake did they eat altogether?" % (fr(1, 8), fr(3, 8)), F(1, 8), F(3, 8), "+",
         figure=fig(pie_svg(8, 1, 3, 0, CAKE, label="cake")), pre="“Altogether” means add. ")
    # 2 cake left
    e, v = e_whole(5, 8)
    its.append(mcq(fig(pie_svg(8, 0, 0, 5, CAKE, label="cake")) +
                   "Mrs Ng baked a cake for Children’s Day. The children ate %s of it. What fraction of the cake was left?"
                   % fr(5, 8) + SIMPLE, v, wrong_whole(5, 8), "The whole cake is 1. Left = 1 − eaten. " + e, rnd))
    # 3 cake, related
    word("Chloe ate %s of a cake (green). Her brother Ryan ate %s of the same cake (yellow). "
         "What fraction of the cake did they eat altogether?" % (fr(1, 4), fr(1, 8)), F(1, 4), F(1, 8), "+",
         figure=fig(pie_svg(8, 2, 1, 0, CAKE, label="cake")),
         pre="The cake is cut into 8 equal slices, so %s is 2 slices. " % fr(1, 4))
    # 4 cake, two steps
    v = 1 - Fraction(1, 2) - Fraction(1, 4)
    assert v == Fraction(1, 4)
    e = ("First add what they ate. Use quarters: %s + %s = %s + %s = %s. Then 1 − %s = %s − %s = <b>%s</b>."
         % (fr(1, 2), fr(1, 4), fr(2, 4), fr(1, 4), fr(3, 4), fr(3, 4), fr(4, 4), fr(3, 4), fr(1, 4)))
    its.append(mcq("Mr Tan’s family ate %s of a kaya cake after dinner and %s of it the next morning. "
                   "What fraction of the cake was left?" % (fr(1, 2), fr(1, 4)) + SIMPLE, v,
                   [Fraction(3, 4), Fraction(1, 2), Fraction(2, 3), Fraction(1, 8)], e, rnd))
    # 5 water bottle, drank altogether
    x, y = F(3, 10), F(1, 2)
    r = val(x) + val(y)
    word("Hafiz filled his water bottle. He drank %s of the water during recess and %s of it after his CCA. "
         "What fraction of the water did he drink altogether?" % (fr(3, 10), fr(1, 2)), x, y, "+",
         figure=fig(model_svg([(val(x), x), (val(y), y), (1 - r, "?")], "1 bottle", None)))
    # 6 bottle 3/4 full, poured out
    word("A bottle was %s full of water. Ethan poured out %s of the bottle to water a plant. "
         "What fraction of the bottle is full now?" % (fr(3, 4), fr(1, 8)), F(3, 4), F(1, 8), "-",
         figure=fig(bottle_svg(8, 6, crossed=1)))
    # 7 water in litres
    e, v = e_whole(2, 5, L_)
    its.append(mcq(fig(model_svg([(Fraction(2, 5), F(2, 5)), (Fraction(3, 5), "?")], "1 ℓ", L_)) +
                   "Mei Ling had a bottle with 1 ℓ of water. She drank %s ℓ of it. How much water was left?" % fr(2, 5)
                   + SIMPLE, v, wrong_whole(2, 5), "Left = 1 ℓ − %s ℓ. " % fr(2, 5) + e, rnd, L_))
    # 8 water comparison
    x, y = F(5, 8), F(1, 4)
    word("Priya and Kavya each had a full bottle of water of the same size. Priya drank %s of her bottle. "
         "Kavya drank %s of her bottle. How much more of a bottle did Priya drink than Kavya?" % (fr(5, 8), fr(1, 4)),
         x, y, "-", pre="“How much more” means subtract. ", extra=[val(x) + val(y)],
         figure=fig(compare_svg([("Priya", val(x), x), ("Kavya", val(y), y)], "?", None)))
    # 9 ribbon left
    x, y = F(5, 6), F(1, 3)
    r = val(x) - val(y)
    word("Siti had %s m of ribbon. She used %s m to wrap a present. How much ribbon did she have left?"
         % (fr(5, 6), fr(1, 3)), x, y, "-", M, pre="Left = total − used. ",
         figure=fig(model_svg([(val(y), y), (r, "?")], x, M)))
    # 10 run comparison
    x, y = F(7, 10), F(2, 5)
    word("On Sports Day, Jun Jie ran %s km and Ahmad ran %s km. How much further did Jun Jie run than Ahmad?"
         % (fr(7, 10), fr(2, 5)), x, y, "-", KM, pre="“How much further” means subtract. ",
         figure=fig(compare_svg([("Jun Jie", val(x), x), ("Ahmad", val(y), y)], "?", KM)))
    # 11 bubble tea
    word("Xin Yi drank %s of a cup of bubble tea in the afternoon. She drank %s of the same cup in the evening. "
         "How much of the cup did she drink altogether?" % (fr(1, 2), fr(1, 6)), F(1, 2), F(1, 6), "+")
    # 12 sugar
    word("Mrs Ng used %s kg of sugar to make kaya and %s kg of sugar to make cookies. How much sugar did she use altogether?"
         % (fr(1, 4), fr(5, 8)), F(1, 4), F(5, 8), "+", KG)
    # 13 students walk or bus
    word("In a class, %s of the students walk to school and %s of the students take the school bus. "
         "What fraction of the class walk or take the school bus?" % (fr(2, 5), fr(3, 10)), F(2, 5), F(3, 10), "+")
    # 14 money left, two steps
    v = 1 - Fraction(3, 8) - Fraction(1, 4)
    e = ("Model: the whole bar is all his pocket money. He spent %s + %s = %s + %s = %s. "
         "Left = %s − %s = <b>%s</b>." % (fr(3, 8), fr(1, 4), fr(3, 8), fr(2, 8), fr(5, 8), fr(8, 8), fr(5, 8), fr(3, 8)))
    its.append(mcq(fig(model_svg([(Fraction(3, 8), F(3, 8)), (Fraction(1, 4), F(1, 4)), (v, "?")], "all his money", None)) +
                   "Ahmad spent %s of his pocket money on food at the canteen and %s of it on a storybook. "
                   "What fraction of his pocket money did he have left?" % (fr(3, 8), fr(1, 4)) + SIMPLE, v,
                   [Fraction(5, 8), Fraction(1, 2), Fraction(2, 3), Fraction(1, 4)], e, rnd))
    # 15 walk to the library
    word("Zhi Hao walked %s km from his HDB block to the bus stop. Then he walked %s km from the bus stop to the library. "
         "How far did he walk altogether?" % (fr(1, 5), fr(3, 10)), F(1, 5), F(3, 10), "+", KM)
    # 16 jug of bandung
    word("A jug had %s ℓ of bandung. Mdm Wong poured %s ℓ of it into cups. How much bandung was left in the jug?"
         % (fr(7, 8), fr(1, 2)), F(7, 8), F(1, 2), "-", L_, pre="Left = total − poured out. ")
    # 17 at first
    x, y = F(1, 4), F(5, 12)
    word("Devi poured %s ℓ of water from a bottle into a cup. There was %s ℓ of water left in the bottle. "
         "How much water was in the bottle at first?" % (fr(1, 4), fr(5, 12)), x, y, "+", L_,
         pre="At first = poured out + left. ", extra=[val(y) - val(x)],
         figure=fig(model_svg([(val(x), x), (val(y), y)], "?", L_)))
    # 18 book read
    word("Arjun read %s of a storybook on Saturday and %s of it on Sunday. What fraction of the book did he read "
         "on the two days?" % (fr(2, 9), fr(1, 3)), F(2, 9), F(1, 3), "+")
    # 19 book not read yet
    e, v = e_whole(5, 12)
    its.append(mcq("Hui Min has read %s of her library book. What fraction of the book has she not read yet?" % fr(5, 12)
                   + SIMPLE, v, wrong_whole(5, 12), "The whole book is 1. Not read = 1 − read. " + e, rnd))
    # 20 tank
    word("A fish tank was %s full of water. Mr Kumar let out some water to clean it. Then the tank was %s full. "
         "What fraction of the tank did he let out?" % (fr(11, 12), fr(1, 3)), F(11, 12), F(1, 3), "-",
         pre="Water let out = before − after. ")
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_like = one_bar_svg(7, 2, 3)
    f_bars = two_bars_svg(2, 1, 4, 1, 4, W=360, labels=True)
    f_sub = two_bars_svg(3, 2, 6, 1, 6, W=360, labels=True)
    f_whole = one_bar_svg(8, 8, 0, crossed=3)
    f_model = model_svg([(Fraction(1, 8), F(1, 8)), (Fraction(1, 2), F(1, 2)), (Fraction(3, 8), "?")], "1 cake", None)
    return (
        "<h2>Like fractions: add or subtract the numerators</h2>"
        "<p>When the denominators are the same, the parts are the same size. Add or subtract the numerators. "
        "The denominator does not change.</p>"
        "<figure class='sn-fig'>" + f_like +
        "<figcaption>2 sevenths + 3 sevenths = 5 sevenths.</figcaption></figure>"
        + ex("Example", fr(2, 7) + " + " + fr(3, 7) + " = ?", "Add the numerators: 2 + 3 = 5. Keep the denominator 7.", fr(5, 7))
        + ex("Example", fr(7, 9) + " − " + fr(3, 9) + " = ?", "Subtract the numerators: 7 − 3 = 4. Keep the denominator 9.", fr(4, 9)) +
        "<h2>Related fractions: make the denominators the same</h2>"
        "<p>Halves and quarters are different sizes, so you cannot add them as they are. 4 is a multiple of 2, "
        "so change " + fr(1, 2) + " into quarters. Multiply the numerator and the denominator by the same number.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed line cuts the top bar into quarters: " + fr(1, 2) + " = " + fr(2, 4) + ".</figcaption></figure>"
        + ex("Example", fr(1, 2) + " + " + fr(1, 4) + " = ?",
             "2 × 2 = 4, so " + fr(1, 2) + " = " + fr(2, 4) + ". Then " + fr(2, 4) + " + " + fr(1, 4) + " = " + fr(3, 4) + ".", fr(3, 4)) +
        "<figure class='sn-fig'>" + f_sub +
        "<figcaption>The dashed lines cut the top bar into sixths: " + fr(2, 3) + " = " + fr(4, 6) + ".</figcaption></figure>"
        + ex("Example", fr(2, 3) + " − " + fr(1, 6) + " = ?",
             "3 × 2 = 6, so " + fr(2, 3) + " = " + fr(4, 6) + ". Then " + fr(4, 6) + " − " + fr(1, 6) + " = " + fr(3, 6) +
             " = " + fr(1, 2) + ".", fr(1, 2)) +
        "<h2>Give the answer in simplest form</h2>"
        "<p>Divide the numerator and the denominator by the same number until you cannot divide any more.</p>" +
        table(["Calculation", "Working", "Simplest form"], [
            [fr(1, 8) + " + " + fr(5, 8), fr(6, 8) + " (6 and 8 ÷ 2)", fr(3, 4)],
            [fr(1, 3) + " + " + fr(1, 6), fr(2, 6) + " + " + fr(1, 6) + " = " + fr(3, 6) + " (3 and 6 ÷ 3)", fr(1, 2)],
            [fr(9, 10) + " − " + fr(1, 2), fr(9, 10) + " − " + fr(5, 10) + " = " + fr(4, 10) + " (4 and 10 ÷ 2)", fr(2, 5)],
        ]) +
        "<h2>Subtracting from 1</h2>"
        "<p>Write 1 whole as a fraction with the same denominator, such as 1 = " + fr(8, 8) + ".</p>"
        "<figure class='sn-fig'>" + f_whole +
        "<figcaption>1 − " + fr(3, 8) + " = " + fr(8, 8) + " − " + fr(3, 8) + " = " + fr(5, 8) + ".</figcaption></figure>" +
        "<h2>Word problems: draw a model</h2>"
        "<p>Draw a bar for the whole. Mark the parts you know and put “?” on the part you need to find. "
        "Then decide whether to add or subtract.</p>"
        "<figure class='sn-fig'>" + f_model +
        "<figcaption>Ali ate " + fr(1, 8) + " of a cake and Siti ate " + fr(1, 2) + " of it. The “?” is the part left.</figcaption></figure>"
        + ex("Example", "Ali ate " + fr(1, 8) + " of a cake. Siti ate " + fr(1, 2) + " of the cake. What fraction of the cake was left?",
             "Eaten: " + fr(1, 8) + " + " + fr(4, 8) + " = " + fr(5, 8) + ". Left: " + fr(8, 8) + " − " + fr(5, 8) + " = " + fr(3, 8) + ".",
             fr(3, 8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(2, 7) + " + " + fr(3, 7) + " = " + fr(5, 14) + " (adding the denominators)",
             "Keep the denominator: " + fr(5, 7)],
            [fr(1, 2) + " + " + fr(1, 4) + " = " + fr(2, 4) + " (not changing to the same denominator)",
             "Change " + fr(1, 2) + " to " + fr(2, 4) + " first: " + fr(2, 4) + " + " + fr(1, 4) + " = " + fr(3, 4)],
            [fr(1, 8) + " + " + fr(5, 8) + " = " + fr(6, 8) + " (answer not simplified)",
             "Divide by 2: " + fr(3, 4)],
            ["1 − " + fr(3, 8) + " = " + fr(2, 8) + " (taking 1 from the numerator)",
             "Write 1 as " + fr(8, 8) + ": " + fr(8, 8) + " − " + fr(3, 8) + " = " + fr(5, 8)],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 adding and subtracting fractions?",
     "a": "In Primary 3, students add and subtract two related fractions within one whole, with denominators up to 12, such as 1/2 + 1/4 or 2/3 − 1/6. They give the answer in simplest form."},
    {"q": "How do I explain adding fractions with different denominators to my child?",
     "a": "Make the parts the same size first. For 1/2 + 1/4, fold a paper strip to show that 1/2 = 2/4, then add: 2/4 + 1/4 = 3/4."},
    {"q": "What is the most common mistake when adding fractions?",
     "a": "Adding the denominators, as in 1/5 + 3/5 = 4/10. The parts are still fifths, so the answer is 4/5."},
    {"q": "Is adding and subtracting fractions in the MOE syllabus for Primary 3?",
     "a": "Yes. It is part of Fractions in the Primary 3 Standard Mathematics syllabus (MOE 2021). In Primary 4, students go on to answers greater than 1 and mixed numbers."},
]


def gen_unit():
    rnd = random.Random(63806)
    sets = [set_like(rnd), set_related(rnd), set_simplest(rnd), set_whole(rnd), set_words(rnd)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert it["q"].count("<svg") <= 1, it["q"]
    return {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "adding-and-subtracting-fractions", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Adding and Subtracting Fractions",
        "seo_title": "P3 Adding and Subtracting Fractions Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Adding and Subtracting Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting two related fractions within one whole (denominators not exceeding 12)",
        "meta_desc": "Free P3 maths practice: add and subtract like and related fractions within one whole, simplest form and word problems. 100 questions with answers.",
        "key_big": "Make the denominators the same, then add or subtract only the numerators.",
        "key_sub": "1/2 + 1/4 = 2/4 + 1/4 = 3/4",
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
