# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Add and Subtract Fractions with Unlike Denominators (5.NF.A.1-2)
  python tools/gen_us_math_g5_add_sub_fractions.py
Every answer is in simplest form (a fraction part less than 1 with no common factor).
Wrong choices come from real mistakes and are also written in simplest form, so the form
never gives the answer away. A wrong choice is never equal in value to the right answer.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # first fraction
FILL2 = "#f2b84b"     # second fraction
RED = "#c0392b"
LINE = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace", "Chloe", "Hana"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Max", "Theo"]
WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 9: "ninths", 10: "tenths",
        12: "twelfths", 15: "fifteenths", 20: "twentieths", 24: "twenty-fourths"}
SIMPLE = "<br>Write the answer in simplest form."


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frq(b):
    return fr("<b>?</b>", b)


def mx(w, n, d):
    """Whole part w and fraction n/d written as given: '3 15/12', '5/8', '2'."""
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


def lcm(a, b):
    return a * b // math.gcd(a, b)


def unit_for(v, units):
    if not units:
        return ""
    return " " + (units[0] if v <= 1 else units[1])


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


def mcq(q, correct, cands, e, rnd):
    """correct is a Fraction (shown in simplest form) or a string. cands are Fractions or strings.
    A Fraction candidate equal to the correct value, zero or negative is never used."""
    if isinstance(correct, Fraction):
        cv, cs = correct, show(correct)
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
            c = show(c)
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=16, color=LINE):
    """Stacked fraction drawn in SVG, centered at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 5, x + w / 2, y + 5, color, x, y + size + 5, size, color, b))


def bar_cells(x0, y0, W, H, d, k, col):
    return "".join("<rect x='%.2f' y='%.1f' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>"
                   % (x0 + i * W / d, y0, W / d, H, col if i < k else "#fff", LINE) for i in range(d))


def dashes(x0, y0, W, H, d, L):
    """Dashed lines that cut a bar of d parts into L parts (only where there is no solid line yet)."""
    s = []
    for i in range(1, L):
        if (i * d) % L == 0:
            continue
        x = x0 + W * i / L
        s.append("<line x1='%.2f' y1='%.1f' x2='%.2f' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>"
                 % (x, y0 + 2, x, y0 + H - 2, LINE))
    return "".join(s)


def two_bars_svg(d1, k1, d2, k2, L, W=264, H=40, labels=False):
    """Top bar: k1 of d1 parts (green). Bottom bar: k2 of d2 parts (yellow). Dashed lines cut both into L parts.
    With labels, the fractions are written to the left of the bars."""
    x0 = 58 if labels else 6
    s = [bar_cells(x0, 6, W, H, d1, k1, FILL), dashes(x0, 6, W, H, d1, L),
         bar_cells(x0, 6 + H + 14, W, H, d2, k2, FILL2), dashes(x0, 6 + H + 14, W, H, d2, L)]
    s.append("<rect x='%d' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, W, H, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (x0, 6 + H + 14, W, H, LINE))
    if labels:
        g1, g2 = math.gcd(k1, d1), math.gcd(k2, d2)
        s.append(sfr(26, 22, k1 // g1, d1 // g1, 15))
        s.append(sfr(26, 22 + H + 14, k2 // g2, d2 // g2, 15))
    return svg_wrap(x0 + W + 6, 2 * H + 26, "".join(s),
                    "two bars of the same size: %d of %d parts green and %d of %d parts yellow, dashed lines cut both into %d parts"
                    % (k1, d1, k2, d2, L))


def one_bar_svg(L, k1, k2, crossed=0, W=264, H=40):
    """One bar of L parts: k1 green then k2 yellow. crossed = how many of the last green parts get a red X."""
    s = []
    for i in range(L):
        col = FILL if i < k1 else (FILL2 if i < k1 + k2 else "#fff")
        x = 6 + i * W / L
        s.append("<rect x='%.2f' y='6' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (x, W / L, H, col, LINE))
        if k1 - crossed <= i < k1:
            c = W / L
            r = min(c, H) / 2 - min(c, H) * 0.2
            cx, cy = x + c / 2, 6 + H / 2
            s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, RED))
    s.append("<rect x='6' y='6' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (W, H, LINE))
    if crossed:
        lab = "bar of %d equal parts: %d shaded and the last %d of them crossed out" % (L, k1, crossed)
    else:
        lab = "bar of %d equal parts: %d green and %d yellow" % (L, k1, k2)
    return svg_wrap(W + 12, H + 12, "".join(s), lab)


def arc(x0, x1, y, h, col):
    cx, cy = (x0 + x1) / 2.0, y - 2 * h
    s = "<path d='M%.1f %d Q%.1f %.1f %.1f %d' fill='none' stroke='%s' stroke-width='2.6'/>" % (x0, y - 3, cx, cy, x1, y - 3, col)
    dx, dy = x1 - cx, (y - 3) - cy
    Ln = math.hypot(dx, dy)
    ux, uy = dx / Ln, dy / Ln
    px, py = -uy, ux
    a = (x1 - 11 * ux + 6 * px, y - 3 - 11 * uy + 6 * py)
    b = (x1 - 11 * ux - 6 * px, y - 3 - 11 * uy - 6 * py)
    s += "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1, y - 3, a[0], a[1], b[0], b[1], col)
    return s


def nl_jump_svg(L, start, end, W=380):
    """Number line 0..1 in L parts with a jump from start to end (in parts)."""
    lft, rgt, Y = 24, W - 24, 62

    def X(i):
        return lft + (rgt - lft) * float(i) / L
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (lft, Y, rgt, Y, LINE)]
    for i in range(L + 1):
        whole = i in (0, L)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if whole else 8), X(i), Y + (13 if whole else 8), LINE, "2.5" if whole else "1.6"))
    for v, i in ((0, 0), (1, L)):
        s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (X(i), Y + 36, LINE, v))
    s.append(arc(X(start), X(end), Y, min(26, 8 + 2.2 * abs(end - start)), RED))
    s.append("<circle cx='%.1f' cy='%d' r='5' fill='%s'/>" % (X(start), Y, LINE))
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to 1 in %d equal parts with a jump back" % L)


def bench_svg(points, W=420):
    """Number line 0..1 with the benchmarks 0, 1/2, 1 below and the given fractions marked above."""
    lft, rgt, Y = 24, W - 24, 70

    def X(v):
        return lft + (rgt - lft) * float(v)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (lft, Y, rgt, Y, LINE)]
    for v in (0, Fraction(1, 2), 1):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(v), Y - 13, X(v), Y + 13, LINE))
    s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>0</text>" % (X(0), Y + 36, LINE))
    s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>1</text>" % (X(1), Y + 36, LINE))
    s.append(sfr(X(Fraction(1, 2)), Y + 30, 1, 2, 15))
    for v in points:
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (X(v), Y, RED))
        s.append(sfr(X(v), 20, v.numerator, v.denominator, 15, RED))
    return svg_wrap(W, Y + 58, "".join(s), "number line from 0 to 1 with benchmarks 0, one half and 1")


# ------------------------------------------------------------ explanation and mistakes
def finish(W, N, L, units=None):
    """W wholes and N/L (N may be L or more). Rename, simplify, state the answer."""
    t = ""
    if N >= L:
        w2, r = divmod(N, L)
        t += "%s is more than 1: %s = %s. " % (fr(N, L), fr(N, L), mx(w2, r, L)) if r else "%s = %d. " % (fr(N, L), w2)
        if W:
            t += "%d + %s = %s. " % (W, mx(w2, r, L), mx(W + w2, r, L))
        W, N = W + w2, r
    g = math.gcd(N, L) if N else 1
    if N and g > 1:
        t += "Simplify: divide the top and bottom of %s by %d to get %s. " % (fr(N, L), g, fr(N // g, L // g))
    v = W + Fraction(N, L)
    return t + "The answer is <b>%s%s</b>." % (show(v), unit_for(v, units)), v


def common(d1, d2):
    L = lcm(d1, d2)
    if L == max(d1, d2):
        return "%d is a multiple of %d, so use %d as the common denominator. " % (max(d1, d2), min(d1, d2), L)
    return "The least common denominator of %d and %d is %d. " % (d1, d2, L)


def e_calc(x, y, op, units=None):
    """Step explanation for x op y. x, y = (whole, top, bottom)."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    t = common(d1, d2)
    rw = ["%s = %s" % (mx(w, n, d), mx(w, n * L // d, L)) for w, n, d in (x, y) if d != L]
    t += "Rewrite: " + " and ".join(rw) + ". "
    mixed = w1 or w2
    if op == "+":
        if not mixed:
            t += "Add the numerators: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            s, v = finish(0, a + b, L, units)
        else:
            t += "Add the fractions: %s + %s = %s. " % (fr(a, L), fr(b, L), fr(a + b, L))
            t += ("Add the whole numbers: %d + %d = %d. " % (w1, w2, w1 + w2)) if (w1 and w2) else "The whole number is %d. " % (w1 + w2)
            s, v = finish(w1 + w2, a + b, L, units)
        assert v == val(x) + val(y)
    else:
        if not mixed:
            t += "Subtract the numerators: %s − %s = %s. " % (fr(a, L), fr(b, L), fr(a - b, L))
            s, v = finish(0, a - b, L, units)
        elif a >= b:
            t += ("Subtract the fractions: %s − %s = %s. Subtract the whole numbers: %d − %d = %d. "
                  % (fr(a, L), fr(b, L), fr(a - b, L), w1, w2, w1 - w2))
            s, v = finish(w1 - w2, a - b, L, units)
        else:
            t += ("%s is less than %s, so rename 1 whole: %s = %s. Subtract the fractions: %s − %s = %s. "
                  "Subtract the whole numbers: %d − %d = %d. "
                  % (fr(a, L), fr(b, L), mx(w1, a, L), mx(w1 - 1, a + L, L), fr(a + L, L), fr(b, L), fr(a + L - b, L),
                     w1 - 1, w2, w1 - 1 - w2))
            s, v = finish(w1 - 1 - w2, a + L - b, L, units)
        assert v == val(x) - val(y)
    return t + s


def wrong(x, y, op):
    """Wrong answers from real mistakes, most common first."""
    (w1, n1, d1), (w2, n2, d2) = x, y
    L = lcm(d1, d2)
    a, b = n1 * L // d1, n2 * L // d2
    right = val(x) + val(y) if op == "+" else val(x) - val(y)
    c = []
    if op == "+":
        W = w1 + w2
        c.append(W + Fraction(n1 + n2, d1 + d2))                 # added tops and bottoms
        c.append(W + Fraction(n1 + n2, L))                       # changed the denominator but not the numerators
        c.append(W + Fraction(n1 + n2, d1 * d2))                 # multiplied the denominators, kept the numerators
        c.append(W + Fraction(a + n2, L) if d2 != L else W + Fraction(n1 + b, L))   # renamed only one fraction
        if a + b >= L:
            c.append(right - 1)                                  # forgot to carry the whole
        c.append(W + Fraction(n1 * n2, d1 * d2))                 # multiplied the tops and the bottoms
    else:
        W = w1 - w2
        if a >= b:
            if d1 != d2 and n1 > n2 and d1 > d2:
                c.append(W + Fraction(n1 - n2, d1 - d2))         # subtracted tops and bottoms
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)   # changed the denominator only
            c.append(W + Fraction(abs(n1 - n2), d1 * d2) if n1 != n2 else None)
            c.append(W + Fraction(a - n2, L) if d2 != L else W + Fraction(n1 - b, L))   # renamed only one fraction
            c.append(val(x) + val(y))                            # added instead
        else:
            c.append(W + Fraction(b - a, L))                     # took the smaller fraction from the bigger
            c.append(right + 1)                                  # renamed but did not lower the whole
            if W > 1:
                c.append(W - 1 + Fraction(b - a, L))
            if L != 10 and 10 + a - b > 0:
                c.append(W - 1 + Fraction(10 + a - b, L))        # renamed 1 whole as 10, like with whole numbers
            c.append(W + Fraction(abs(n1 - n2), L) if n1 != n2 else None)
    return c


def P0(n, d):
    return (0, n, d)


# ============================================================ set 1: common denominators
def pair(a, b, c, d):
    return "%s and %s" % (fr(a, b), fr(c, d))


def rename_choices(n1, d1, n2, d2, L):
    k1, k2 = L // d1, L // d2
    right = (n1 * k1, n2 * k2)
    cands = [(n1, n2),                                   # changed the denominator only
             (n1 * k2, n2 * k1),                         # multiplied by the wrong number
             (n1 + L - d1, n2 + L - d2),                 # added the same number to the top and bottom
             (n1 * k1, n2), (n1, n2 * k2)]               # renamed only one fraction
    return pair(right[0], L, right[1], L), [pair(p, L, q, L) for p, q in cands if (p, q) != right]


def e_rename(n1, d1, n2, d2, L):
    parts = []
    for n, d in ((n1, d1), (n2, d2)):
        k = L // d
        if k == 1:
            parts.append("%s already has the denominator %d" % (fr(n, d), L))
        else:
            parts.append("%d × %d = %d, so multiply the top and bottom of %s by %d: %s"
                         % (d, k, L, fr(n, d), k, fr(n * k, L)))
    return ". ".join(parts) + ". The answer is <b>%s</b>." % pair(n1 * L // d1, L, n2 * L // d2, L)


def set_common(rnd):
    SPOTS.left = []
    its = []
    # A: fraction bars with dashed lines
    for n1, d1, n2, d2 in [(1, 3, 1, 4), (1, 2, 2, 5), (3, 4, 1, 6), (2, 3, 1, 6), (1, 2, 3, 8)]:
        L = lcm(d1, d2)
        q = (fig(two_bars_svg(d1, n1, d2, n2, L)) +
             "The green part is %s and the yellow part is %s. The dashed lines cut both bars into %s. "
             "Which shows both fractions in %s?" % (fr(n1, d1), fr(n2, d2), WORD[L], WORD[L]))
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = "Count the small parts in each shaded piece. " + e_rename(n1, d1, n2, d2, L)
        its.append(mcq(q, r, c, e, rnd))
    # B: least common denominator
    for n1, d1, n2, d2 in [(3, 4, 1, 6), (1, 6, 3, 8), (2, 3, 1, 5), (1, 4, 3, 10), (5, 8, 7, 12)]:
        L = lcm(d1, d2)
        big, small = max(d1, d2), min(d1, d2)
        mb = ", ".join(str(big * i) for i in range(1, L // big + 1))
        ms = ", ".join(str(small * i) for i in range(1, L // small + 1))
        e = ("Multiples of %d: %s. Multiples of %d: %s. The first number in both lists is <b>%d</b>."
             % (big, mb, small, ms, L))
        if d1 * d2 != L:
            e += " %d × %d = %d is also a common denominator, but it is not the least." % (d1, d2, d1 * d2)
        cands = [d1 * d2 if d1 * d2 != L else None, d1 + d2, big, 2 * L]
        its.append(mcq("What is the least common denominator of %s and %s?" % (fr(n1, d1), fr(n2, d2)),
                       str(L), [str(x) for x in cands if x], e, rnd))
    # C: rename with a given denominator
    for n1, d1, n2, d2, L in [(2, 3, 3, 4, 12), (1, 2, 3, 5, 10), (3, 8, 1, 6, 24), (2, 5, 1, 3, 15), (1, 4, 5, 6, 24)]:
        r, c = rename_choices(n1, d1, n2, d2, L)
        e = e_rename(n1, d1, n2, d2, L)
        if L != lcm(d1, d2):
            e += " (%d also works, but any common denominator gives the right answer.)" % lcm(d1, d2)
        its.append(mcq("Rewrite %s and %s with the denominator %d." % (fr(n1, d1), fr(n2, d2), L), r, c, e, rnd))
    # D1: missing numerator
    for n, d, L in [(3, 4, 20), (5, 6, 18), (2, 5, 15)]:
        k = L // d
        e = "%d × %d = %d, so multiply the top by %d too: %d × %d = <b>%d</b>. So %s = %s." % (d, k, L, k, n, k, n * k, fr(n, d), fr(n * k, L))
        its.append(mcq("%s = %s" % (fr(n, d), frq(L)), str(n * k), [str(n), str(n + L - d), str(k), str(L - n * k)], e, rnd))
    # D2: which pair can be written with the denominator L
    for L, good, bads in [(12, ((1, 4), (5, 6)), [((1, 5), (1, 2)), ((3, 8), (1, 3)), ((2, 9), (1, 4))]),
                          (10, ((1, 2), (3, 5)), [((1, 4), (2, 5)), ((2, 3), (1, 2)), ((3, 8), (1, 5))])]:
        for p in bads:
            assert L % p[0][1] or L % p[1][1]
        assert L % good[0][1] == 0 and L % good[1][1] == 0
        e = ("%d must be a multiple of both denominators. %d × %d = %d and %d × %d = %d, so <b>%s</b> works. "
             "In the other pairs, %d is not a multiple of one of the denominators."
             % (L, good[0][1], L // good[0][1], L, good[1][1], L // good[1][1], L, pair(good[0][0], good[0][1], good[1][0], good[1][1]), L))
        its.append(mcq("Which pair of fractions can both be written as %s?" % WORD[L],
                       pair(good[0][0], good[0][1], good[1][0], good[1][1]),
                       [pair(a[0], a[1], b[0], b[1]) for a, b in bads], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find a common denominator", "items": its}


# ============================================================ set 2: add
def set_add(rnd, P):
    SPOTS.left = []
    its = []
    # F1: bar model
    for n1, d1, n2, d2 in [(1, 2, 1, 3), (1, 4, 3, 8), (2, 5, 1, 2), (1, 6, 2, 3)]:
        L = lcm(d1, d2)
        k1, k2 = n1 * L // d1, n2 * L // d2
        q = (fig(one_bar_svg(L, k1, k2)) +
             "The bar is cut into %s. Green shows %s and yellow shows %s. What is %s + %s?"
             % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + SIMPLE)
        x, y = P0(n1, d1), P0(n2, d2)
        its.append(mcq(q, val(x) + val(y), wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
    # F2: sums less than 1
    for n1, d1, n2, d2 in [(1, 6, 1, 3), (1, 4, 1, 12), (3, 10, 1, 5), (1, 6, 1, 2),
                           (2, 5, 1, 3), (3, 8, 1, 6), (1, 4, 2, 5), (2, 9, 1, 3)]:
        x, y = P0(n1, d1), P0(n2, d2)
        its.append(mcq("%s + %s = ?" % (fr(n1, d1), fr(n2, d2)) + SIMPLE, val(x) + val(y), wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
    # F3: sums more than 1
    for n1, d1, n2, d2 in [(3, 4, 2, 3), (5, 6, 3, 8), (4, 5, 1, 2), (7, 8, 3, 4), (5, 6, 5, 12)]:
        x, y = P0(n1, d1), P0(n2, d2)
        assert val(x) + val(y) > 1
        its.append(mcq("%s + %s = ?<br>Write the answer as a mixed number in simplest form." % (fr(n1, d1), fr(n2, d2)),
                       val(x) + val(y), wrong(x, y, "+"), e_calc(x, y, "+"), rnd))
    # F4: three addends
    e = ("Use 8 as the common denominator. Rewrite: %s = %s and %s = %s. Add the numerators: 4 + 2 + 1 = 7. "
         "The answer is <b>%s</b>." % (fr(1, 2), fr(4, 8), fr(1, 4), fr(2, 8), fr(7, 8)))
    assert Fraction(1, 2) + Fraction(1, 4) + Fraction(1, 8) == Fraction(7, 8)
    its.append(mcq("%s + %s + %s = ?" % (fr(1, 2), fr(1, 4), fr(1, 8)) + SIMPLE, Fraction(7, 8),
                   [Fraction(3, 14), Fraction(3, 8), Fraction(6, 8), Fraction(3, 64)], e, rnd))
    # F5: find the mistake
    n, he, his = P.next()
    q = "%s wrote %s + %s = %s. What mistake did %s make?" % (n, fr(1, 3), fr(1, 4), fr(2, 7), he)
    e = ("Thirds and fourths are different sizes, so you cannot just add the tops and bottoms. "
         "Rewrite them as twelfths: %s + %s = %s. %s is even less than %s, so it cannot be the sum."
         % (fr(4, 12), fr(3, 12), fr(7, 12), fr(2, 7), fr(1, 3)))
    its.append(mcq(q, "%s added the tops and the bottoms" % cap(he),
                   ["%s should have multiplied" % cap(he), "%s forgot to simplify" % cap(he), "There is no mistake"], e, rnd))
    # F6: missing addend
    e = ("Think: %s − %s. Rewrite %s = %s. Then %s − %s = %s = %s. Check: %s + %s = %s + %s = %s. The answer is <b>%s</b>."
         % (fr(5, 6), fr(1, 2), fr(1, 2), fr(3, 6), fr(5, 6), fr(3, 6), fr(2, 6), fr(1, 3),
            fr(1, 2), fr(1, 3), fr(3, 6), fr(2, 6), fr(5, 6), fr(1, 3)))
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    its.append(mcq("%s + <b>?</b> = %s" % (fr(1, 2), fr(5, 6)), Fraction(1, 3),
                   [Fraction(4, 6), Fraction(4, 4), Fraction(4, 3), Fraction(1, 6)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add fractions with unlike denominators", "items": its}


# ============================================================ set 3: subtract
def set_subtract(rnd, P):
    SPOTS.left = []
    its = []
    # G1: bar model with crossed parts
    for n1, d1, n2, d2 in [(3, 4, 1, 3), (5, 6, 1, 2), (7, 10, 1, 2), (3, 4, 1, 8)]:
        L = lcm(d1, d2)
        k1, k2 = n1 * L // d1, n2 * L // d2
        q = (fig(one_bar_svg(L, k1, 0, crossed=k2)) +
             "The bar is cut into %s. The shaded part is %s, and %s is crossed out. What is %s − %s?"
             % (WORD[L], fr(n1, d1), fr(n2, d2), fr(n1, d1), fr(n2, d2)) + SIMPLE)
        x, y = P0(n1, d1), P0(n2, d2)
        its.append(mcq(q, val(x) - val(y), wrong(x, y, "-"), e_calc(x, y, "-"), rnd))
    # G2: no picture
    for n1, d1, n2, d2 in [(5, 6, 1, 3), (7, 10, 1, 5), (3, 4, 1, 12), (5, 8, 1, 4), (2, 3, 1, 2),
                           (4, 5, 1, 2), (7, 8, 2, 3), (5, 6, 3, 4), (9, 10, 1, 4)]:
        x, y = P0(n1, d1), P0(n2, d2)
        its.append(mcq("%s − %s = ?" % (fr(n1, d1), fr(n2, d2)) + SIMPLE, val(x) - val(y), wrong(x, y, "-"), e_calc(x, y, "-"), rnd))
    # G3: number line
    q = (fig(nl_jump_svg(12, 10, 7)) +
         "The number line is cut into twelfths. The jump shows %s − %s. Where does it end?" % (fr(5, 6), fr(1, 4)) + SIMPLE)
    x, y = P0(5, 6), P0(1, 4)
    e = "The jump starts at %s = %s and goes back %s = %s, 3 spaces. " % (fr(5, 6), fr(10, 12), fr(1, 4), fr(3, 12)) + e_calc(x, y, "-")
    its.append(mcq(q, val(x) - val(y), wrong(x, y, "-"), e, rnd))
    # G4: missing numbers
    e = ("Think: %s + %s. Rewrite %s = %s and %s = %s. Then %s + %s = %s. Check: %s − %s = %s − %s = %s. The answer is <b>%s</b>."
         % (fr(1, 2), fr(1, 3), fr(1, 2), fr(3, 6), fr(1, 3), fr(2, 6), fr(3, 6), fr(2, 6), fr(5, 6),
            fr(5, 6), fr(1, 3), fr(5, 6), fr(2, 6), fr(3, 6), fr(5, 6)))
    assert Fraction(5, 6) - Fraction(1, 3) == Fraction(1, 2)
    its.append(mcq("<b>?</b> − %s = %s" % (fr(1, 3), fr(1, 2)), Fraction(5, 6),
                   [Fraction(1, 6), Fraction(2, 5), Fraction(1, 3)], e, rnd))
    e = ("Think: %s − %s. Rewrite %s = %s and %s = %s. Then %s − %s = %s. Check: %s − %s = %s − %s = %s. The answer is <b>%s</b>."
         % (fr(3, 4), fr(1, 6), fr(3, 4), fr(9, 12), fr(1, 6), fr(2, 12), fr(9, 12), fr(2, 12), fr(7, 12),
            fr(3, 4), fr(7, 12), fr(9, 12), fr(7, 12), fr(2, 12), fr(7, 12)))
    assert Fraction(3, 4) - Fraction(7, 12) == Fraction(1, 6)
    its.append(mcq("%s − <b>?</b> = %s" % (fr(3, 4), fr(1, 6)), Fraction(7, 12),
                   [Fraction(11, 12), Fraction(2, 3), Fraction(1, 2)], e, rnd))
    # G5: find the mistake
    n, he, his = P.next()
    q = "%s wrote %s − %s = %s. What mistake did %s make?" % (n, fr(5, 6), fr(1, 4), fr(4, 2), he)
    e = ("Sixths and fourths are different sizes. %s subtracted the tops and the bottoms. "
         "Use twelfths: %s − %s = %s. Also, %s = 2, which is more than %s, so it cannot be right."
         % (n, fr(10, 12), fr(3, 12), fr(7, 12), fr(4, 2), fr(5, 6)))
    its.append(mcq(q, "%s subtracted the denominators" % cap(he),
                   ["%s subtracted the numerators" % cap(he), "%s should have added" % cap(he), "There is no mistake"], e, rnd))
    # G6: how much more
    for n1, d1, n2, d2 in [(7, 8, 1, 2), (2, 3, 1, 4), (9, 10, 3, 5)]:
        x, y = P0(n1, d1), P0(n2, d2)
        e = "“How much more” means subtract. " + e_calc(x, y, "-")
        its.append(mcq("How much more is %s than %s?" % (fr(n1, d1), fr(n2, d2)) + SIMPLE,
                       val(x) - val(y), [val(x) + val(y)] + wrong(x, y, "-"), e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Subtract fractions with unlike denominators", "items": its}


# ============================================================ set 4: mixed numbers
def set_mixed(rnd):
    SPOTS.left = []
    its = []
    add_easy = [((2, 1, 3), (1, 1, 4)), ((1, 1, 2), (2, 1, 5)), ((3, 1, 6), (1, 1, 2)), ((2, 3, 8), (4, 1, 4)), ((1, 1, 6), (2, 3, 4))]
    add_carry = [((1, 2, 3), (2, 3, 4)), ((2, 5, 6), (1, 1, 2)), ((3, 4, 5), (1, 1, 2)), ((1, 7, 8), (2, 1, 4)), ((2, 3, 4), (3, 5, 6))]
    sub_easy = [((3, 3, 4), (1, 1, 3)), ((5, 5, 6), (2, 1, 2)), ((4, 7, 10), (1, 2, 5)), ((6, 2, 3), (4, 1, 6))]
    sub_borrow = [((3, 1, 4), (1, 2, 3)), ((4, 1, 3), (2, 1, 2)), ((5, 1, 6), (2, 3, 4)), ((6, 2, 5), (3, 1, 2)),
                  ((7, 1, 8), (4, 3, 4)), ((5, 1, 2), (2, 5, 6))]
    for grp, op in ((add_easy, "+"), (add_carry, "+"), (sub_easy, "-"), (sub_borrow, "-")):
        for x, y in grp:
            L = lcm(x[2], y[2])
            a, b = x[1] * L // x[2], y[1] * L // y[2]
            if grp is add_carry:
                assert a + b >= L
            if grp is add_easy:
                assert a + b < L
            if grp is sub_easy:
                assert a >= b
            if grp is sub_borrow:
                assert a < b
            r = val(x) + val(y) if op == "+" else val(x) - val(y)
            q = "%s %s %s = ?" % (mx(*x), "+" if op == "+" else "−", mx(*y)) + SIMPLE
            its.append(mcq(q, r, wrong(x, y, op), e_calc(x, y, op), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract mixed numbers", "items": its}


# ============================================================ set 5: word problems and estimating
def word(q, x, y, op, units, extra=None):
    e = e_calc(x, y, op, units)
    r = val(x) + val(y) if op == "+" else val(x) - val(y)
    c = wrong(x, y, op)
    if op == "-":
        c = [val(x) + val(y)] + c
    if extra:
        c = extra + c
    return q + SIMPLE, r, c, e


def amt(x, one, many):
    v = val(x)
    return "%s %s" % (mx(*x), one if v <= 1 else many)


def set_words(rnd, P):
    SPOTS.left = []
    LESS, MORE, EQ = "Less than 1", "More than 1", "Exactly 1"
    probs = []

    # estimation 1
    e = ("Use the benchmark %s. %s + %s = 1, and %s is less than %s, so the sum is <b>less than 1</b>. "
         "(The exact sum is %s.)" % (fr(1, 2), fr(1, 2), fr(1, 2), fr(2, 5), fr(1, 2), fr(9, 10)))
    assert Fraction(2, 5) + Fraction(1, 2) < 1
    probs.append(("Without finding the exact sum, is %s + %s more than 1 or less than 1?" % (fr(2, 5), fr(1, 2)),
                  LESS, [MORE, EQ, "Less than %s" % fr(1, 2)], e))
    # hike
    n, he, his = P.next()
    x, y = (0, 1, 2), (0, 3, 8)
    probs.append(word("%s hiked %s to the lake and then %s along the shore. How far did %s hike in all?"
                      % (n, amt(x, "mile", "miles"), amt(y, "mile", "miles"), he), x, y, "+", ("mile", "miles")))
    # recipe
    x, y = (0, 2, 3), (0, 1, 4)
    probs.append(word("A muffin recipe uses %s of flour and %s of sugar. How many cups of flour and sugar is that in all?"
                      % (amt(x, "cup", "cups"), amt(y, "cup", "cups")), x, y, "+", ("cup", "cups")))
    # estimation 2
    e = ("%s is more than %s, and %s is more than %s. Two numbers that are each more than %s add up to "
         "<b>more than 1</b>. (The exact sum is %s.)"
         % (fr(5, 8), fr(1, 2), fr(4, 7), fr(1, 2), fr(1, 2), show(Fraction(5, 8) + Fraction(4, 7))))
    assert Fraction(5, 8) + Fraction(4, 7) > 1
    probs.append(("Without finding the exact sum, is %s + %s more than 1 or less than 1?" % (fr(5, 8), fr(4, 7)),
                  MORE, [LESS, EQ, "Less than %s" % fr(1, 2)], e))
    # ribbon
    n, he, his = P.next()
    x, y = (0, 3, 4), (0, 1, 3)
    probs.append(word("%s had %s of ribbon. %s used %s to wrap a gift. How much ribbon is left?"
                      % (n, amt(x, "yard", "yards"), cap(he), amt(y, "yard", "yards")), x, y, "-", ("yard", "yards")))
    # rain
    x, y = (1, 1, 2), (0, 3, 4)
    probs.append(word("It rained %s on Monday and %s on Tuesday. How much rain fell on the two days in all?"
                      % (amt(x, "inch", "inches"), amt(y, "inch", "inches")), x, y, "+", ("inch", "inches")))
    # estimation 3: closest benchmark
    s = Fraction(3, 7) + Fraction(1, 8)
    assert abs(s - Fraction(1, 2)) < abs(s - 1) and abs(s - Fraction(1, 2)) < s
    e = ("%s is close to %s, and %s is close to 0. So %s + %s is about %s + 0 = <b>%s</b>. (The exact sum is %s.)"
         % (fr(3, 7), fr(1, 2), fr(1, 8), fr(3, 7), fr(1, 8), fr(1, 2), fr(1, 2), show(s)))
    probs.append(("Which benchmark is %s + %s closest to?" % (fr(3, 7), fr(1, 8)), fr(1, 2), ["0", "1", "1 " + fr(1, 2)], e))
    # paint: two steps
    n, he, his = P.next()
    e = ("First add what %s painted. Rewrite %s = %s and %s = %s: %s + %s = %s. The whole wall is %s. "
         "Left: %s − %s = <b>%s</b>." % (he, fr(1, 3), fr(2, 6), fr(1, 2), fr(3, 6), fr(2, 6), fr(3, 6), fr(5, 6),
                                          fr(6, 6), fr(6, 6), fr(5, 6), fr(1, 6)))
    assert 1 - Fraction(1, 3) - Fraction(1, 2) == Fraction(1, 6)
    probs.append(("%s painted %s of a wall in the morning and %s of it after lunch. What fraction of the wall is left to paint?"
                  % (n, fr(1, 3), fr(1, 2)) + SIMPLE, Fraction(1, 6),
                  [Fraction(5, 6), Fraction(3, 5), Fraction(2, 5), Fraction(2, 3)], e))
    # lemonade
    x, y = (2, 1, 2), (1, 2, 3)
    probs.append(word("A pitcher holds %s of lemonade. The class drinks %s. How much lemonade is left?"
                      % (amt(x, "liter", "liters"), amt(y, "liter", "liters")), x, y, "-", ("liter", "liters")))
    # estimation 4: is it reasonable
    n, he, his = P.next()
    e = ("%s alone is more than %s, so %s + %s must be more than %s. %s added the tops and the bottoms. "
         "The exact sum is %s + %s = %s." % (fr(3, 4), fr(4, 9), fr(3, 4), fr(1, 5), fr(3, 4), n, fr(15, 20), fr(4, 20), fr(19, 20)))
    assert Fraction(3, 4) + Fraction(1, 5) == Fraction(19, 20) and Fraction(4, 9) < Fraction(3, 4)
    probs.append(("%s added %s + %s and got %s. Is %s answer reasonable?" % (n, fr(3, 4), fr(1, 5), fr(4, 9), his),
                  "No. It is less than %s" % fr(3, 4),
                  ["Yes. It is close to %s" % fr(1, 2), "Yes. 3 + 1 = 4 and 4 + 5 = 9", "No. It must be more than 1"], e))
    # piano
    n, he, his = P.next()
    x, y = (0, 3, 4), (0, 2, 3)
    probs.append(word("%s practiced the piano for %s on Saturday and %s on Sunday. How long did %s practice in all?"
                      % (n, amt(x, "hour", "hours"), amt(y, "hour", "hours"), he), x, y, "+", ("hour", "hours")))
    # board
    n, he, his = P.next()
    x, y = (6, 1, 4), (2, 1, 2)
    probs.append(word("A board is %s long. %s cuts off a piece that is %s long. How long is the part that is left?"
                      % (amt(x, "foot", "feet"), n, amt(y, "foot", "feet")), x, y, "-", ("foot", "feet")))
    # estimation 5: about a whole number
    s = Fraction(11, 12) + Fraction(7, 8)
    assert abs(s - 2) < abs(s - 1) and abs(s - 2) < abs(s - 3)
    e = ("%s and %s are each close to 1. So the sum is about 1 + 1 = <b>2</b>. (The exact sum is %s.)"
         % (fr(11, 12), fr(7, 8), show(s)))
    probs.append(("About how much is %s + %s?" % (fr(11, 12), fr(7, 8)), "About 2",
                  ["About 1", "About 3", "About %s" % fr(1, 2)], e))
    # farther
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    x, y = (2, 3, 5), (1, 3, 4)
    q, r, c, e = word("%s ran %s. %s ran %s. How much farther did %s run than %s?"
                      % (n1, amt(x, "mile", "miles"), n2, amt(y, "mile", "miles"), n1, n2), x, y, "-", ("mile", "miles"))
    probs.append((q, r, c, "“How much farther” means subtract. " + e))
    # water bottle
    n, he, his = P.next()
    x, y = (0, 4, 5), (0, 1, 2)
    probs.append(word("%s's water bottle holds %s of water. %s drinks %s during soccer practice. How much water is left?"
                      % (n, amt(x, "liter", "liters"), cap(he), amt(y, "liter", "liters")), x, y, "-", ("liter", "liters")))
    # garden: two steps
    e = ("First add the parts that are used. Rewrite %s = %s and %s = %s: %s + %s = %s. The whole garden is %s. "
         "Left for flowers: %s − %s = <b>%s</b>." % (fr(1, 4), fr(5, 20), fr(2, 5), fr(8, 20), fr(5, 20), fr(8, 20), fr(13, 20),
                                                  fr(20, 20), fr(20, 20), fr(13, 20), fr(7, 20)))
    assert 1 - Fraction(1, 4) - Fraction(2, 5) == Fraction(7, 20)
    probs.append(("A garden is planted with tomatoes in %s of it and beans in %s of it. The rest is for flowers. "
                  "What fraction of the garden is for flowers?" % (fr(1, 4), fr(2, 5)) + SIMPLE, Fraction(7, 20),
                  [Fraction(13, 20), Fraction(2, 3), Fraction(3, 5), Fraction(3, 4)], e))
    # estimation 6: subtract mixed numbers
    s = Fraction(31, 6) - Fraction(23, 8)
    assert abs(s - 2) < abs(s - 3)
    e = ("5 %s is close to 5, and 2 %s is close to 3. So the difference is about 5 − 3 = <b>2</b>. (The exact difference is %s.)"
         % (fr(1, 6), fr(7, 8), show(s)))
    probs.append(("About how much is 5 %s − 2 %s?" % (fr(1, 6), fr(7, 8)), "About 2", ["About 3", "About 8", "About 1"], e))
    # trail mix
    n, he, his = P.next()
    x, y = (0, 3, 8), (0, 1, 3)
    probs.append(word("%s makes trail mix with %s of peanuts and %s of raisins. How much trail mix does %s make?"
                      % (n, amt(x, "pound", "pounds"), amt(y, "pound", "pounds"), he), x, y, "+", ("pound", "pounds")))
    # estimation 7: enough milk?
    n, he, his = P.next()
    e = ("%s is less than %s, so %s + %s is less than %s + %s = 1. "
         "<b>Yes</b>, 1 cup is enough. (%s needs %s.)" % (fr(3, 8), fr(1, 2), fr(1, 2), fr(3, 8),
                                                         fr(1, 2), fr(1, 2), cap(he), amt((0, 7, 8), "cup", "cups")))
    assert Fraction(1, 2) + Fraction(3, 8) <= 1
    probs.append(("%s has 1 cup of milk. %s needs %s for pancakes and %s for muffins. Does %s have enough milk?"
                  % (n, cap(he), amt((0, 1, 2), "cup", "cups"), amt((0, 3, 8), "cup", "cups"), he),
                  "Yes. The sum is less than 1", ["No. The sum is more than 1", "No. %s is more than %s" % (fr(3, 8), fr(1, 2)),
                                                 "Yes. It is exactly 1"], e))
    # reading goal: two steps
    n, he, his = P.next()
    e = ("First add the time %s read. Rewrite 1 %s = 1 %s and %s = %s: 1 %s + %s = 1 %s. "
         "Then subtract from 2. Rename 2 = 1 %s. 1 %s − 1 %s = <b>%s</b>."
         % (he, fr(1, 4), fr(3, 12), fr(1, 3), fr(4, 12), fr(3, 12), fr(4, 12), fr(7, 12),
            fr(12, 12), fr(12, 12), fr(7, 12), amt((0, 5, 12), "hour", "hours")))
    assert 2 - Fraction(5, 4) - Fraction(1, 3) == Fraction(5, 12)
    probs.append(("%s wants to read for 2 hours this weekend. %s read for %s on Saturday and %s on Sunday. "
                  "How much longer does %s need to read?" % (n, cap(he), amt((1, 1, 4), "hour", "hours"), amt((0, 1, 3), "hour", "hours"), he)
                  + SIMPLE, Fraction(5, 12),
                  [Fraction(19, 12), Fraction(17, 12), Fraction(5, 7), Fraction(3, 4)], e))

    assert len(probs) == 20, len(probs)
    its = [mcq(q, r, c, e, rnd) for q, r, c, e in probs]
    return {"title": "Word problems and estimating", "items": its}


# ============================================================ lesson
def body_html():
    f_bars = two_bars_svg(3, 1, 4, 1, 12, W=360, labels=True)
    f_sum = one_bar_svg(12, 4, 3, W=360)
    f_bench = bench_svg([Fraction(2, 5), Fraction(5, 8), Fraction(7, 8)])
    return (
        "<h2>Make the pieces the same size</h2>"
        "<p>You can only add or subtract pieces that are the <b>same size</b>. Thirds and fourths are different sizes, "
        "so first find a <b>common denominator</b>: a number both denominators divide into. "
        "Then rewrite each fraction as an equivalent fraction with that denominator.</p>"
        "<figure class='sn-fig'>" + f_bars +
        "<figcaption>The dashed lines cut both bars into twelfths. " + fr(1, 3) + " = " + fr(4, 12) + " and " +
        fr(1, 4) + " = " + fr(3, 12) + ".</figcaption></figure>"
        + ex("Example", fr(1, 3) + " + " + fr(1, 4) + " = ?",
             "Common denominator: 12. Rewrite: " + fr(1, 3) + " = " + fr(4, 12) + " and " + fr(1, 4) + " = " + fr(3, 12) +
             ". Add the numerators: 4 + 3 = 7.", fr(7, 12)) +
        "<figure class='sn-fig'>" + f_sum +
        "<figcaption>4 twelfths and 3 twelfths make " + fr(7, 12) + ", not " + fr(2, 7) + ".</figcaption></figure>"
        "<h2>Find a common denominator</h2>"
        "<p>Multiplying the two denominators always works. The <b>least common denominator</b> keeps the numbers small: "
        "list multiples of the bigger denominator until the smaller one divides it.</p>" +
        table(["Fractions", "Common denominator", "Rewrite"], [
            [fr(1, 3) + " and " + fr(1, 4), "12", fr(4, 12) + " and " + fr(3, 12)],
            [fr(1, 2) + " and " + fr(3, 8), "8", fr(4, 8) + " and " + fr(3, 8)],
            [fr(5, 6) + " and " + fr(3, 4), "12", fr(10, 12) + " and " + fr(9, 12)],
        ]) +
        "<h2>Add or subtract, then simplify</h2>"
        "<p>Write every answer in <b>simplest form</b>: the fraction part is less than 1, and its top and bottom "
        "have no common factor except 1.</p>"
        + ex("Example", fr(5, 6) + " + " + fr(3, 4) + " = ?",
             "Rewrite: " + fr(10, 12) + " + " + fr(9, 12) + " = " + fr(19, 12) + ". That is more than 1: " +
             fr(19, 12) + " = 1 " + fr(7, 12) + ".", "1 " + fr(7, 12))
        + ex("Example", fr(5, 6) + " − " + fr(1, 2) + " = ?",
             "Rewrite: " + fr(5, 6) + " − " + fr(3, 6) + " = " + fr(2, 6) + ". Divide the top and bottom by 2: " +
             fr(2, 6) + " = " + fr(1, 3) + ".", fr(1, 3)) +
        "<h2>Mixed numbers</h2>"
        "<p>Rewrite the fraction parts with a common denominator. Then work with the fractions and the whole numbers.</p>" +
        table(["Problem", "Rewrite", "Fractions", "Whole numbers", "Answer"], [
            ["2 " + fr(1, 3) + " + 1 " + fr(1, 4), "2 " + fr(4, 12) + " + 1 " + fr(3, 12), fr(7, 12), "2 + 1 = 3", "3 " + fr(7, 12)],
            ["1 " + fr(2, 3) + " + 2 " + fr(3, 4), "1 " + fr(8, 12) + " + 2 " + fr(9, 12), fr(17, 12) + " = 1 " + fr(5, 12), "1 + 2 + 1 = 4", "4 " + fr(5, 12)],
            ["3 " + fr(1, 4) + " − 1 " + fr(2, 3), "3 " + fr(3, 12) + " − 1 " + fr(8, 12), "rename: 2 " + fr(15, 12), "2 − 1 = 1", "1 " + fr(7, 12)],
        ]) +
        "<p>In the last row, " + fr(3, 12) + " is less than " + fr(8, 12) + ", so <b>rename 1 whole</b> as " + fr(12, 12) +
        ": 3 " + fr(3, 12) + " = 2 " + fr(15, 12) + ".</p>"
        + ex("Example", "3 " + fr(1, 4) + " − 1 " + fr(2, 3) + " = ?",
             "Rewrite: 3 " + fr(3, 12) + " − 1 " + fr(8, 12) + ". Rename: 3 " + fr(3, 12) + " = 2 " + fr(15, 12) +
             ". Fractions: " + fr(15, 12) + " − " + fr(8, 12) + " = " + fr(7, 12) + ". Whole numbers: 2 − 1 = 1.", "1 " + fr(7, 12)) +
        "<h2>Estimate with benchmarks</h2>"
        "<p>Compare each fraction with <b>0</b>, <b>" + fr(1, 2) + "</b> and <b>1</b>. Then check that your answer makes sense.</p>"
        "<figure class='sn-fig'>" + f_bench +
        "<figcaption>" + fr(2, 5) + " is a little less than " + fr(1, 2) + ". " + fr(5, 8) + " is a little more than " +
        fr(1, 2) + ". " + fr(7, 8) + " is close to 1.</figcaption></figure>"
        + ex("Example", "Is " + fr(2, 5) + " + " + fr(1, 2) + " more or less than 1?",
             fr(1, 2) + " + " + fr(1, 2) + " = 1, and " + fr(2, 5) + " is less than " + fr(1, 2) + ".", "less than 1 (it is " + fr(9, 10) + ")") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [fr(1, 3) + " + " + fr(1, 4) + " = " + fr(2, 7) + " (adding the tops and bottoms)", "Rewrite with a common denominator: " + fr(4, 12) + " + " + fr(3, 12) + " = " + fr(7, 12)],
            [fr(1, 3) + " + " + fr(1, 4) + " = " + fr(2, 12) + " (changing only the denominators)", "Multiply the top by the same number as the bottom"],
            [fr(5, 6) + " − " + fr(1, 2) + " = " + fr(2, 6) + ", and stopping there", "Simplify: " + fr(1, 3)],
            ["3 " + fr(1, 4) + " − 1 " + fr(2, 3) + " = 2 " + fr(5, 12) + " (taking " + fr(3, 12) + " from " + fr(8, 12) + ")", "Rename 1 whole: 2 " + fr(15, 12) + " − 1 " + fr(8, 12) + " = 1 " + fr(7, 12)],
            [fr(3, 4) + " + " + fr(1, 5) + " = " + fr(4, 9), "Check with benchmarks: the sum must be more than " + fr(3, 4)],
        ])
    )


FAQ = [
    {"q": "How do you add fractions with unlike denominators?",
     "a": "Find a common denominator, rewrite both fractions with it, then add the numerators. For 1/3 + 1/4, use 12: 4/12 + 3/12 = 7/12."},
    {"q": "How do you subtract mixed numbers with unlike denominators?",
     "a": "Rewrite the fraction parts with a common denominator. If the first fraction is smaller, rename 1 whole: 3 1/4 − 1 2/3 = 3 3/12 − 1 8/12 = 2 15/12 − 1 8/12 = 1 7/12."},
    {"q": "Do 5th graders have to write fractions in simplest form?",
     "a": "The Common Core standard does not require it, but most 5th grade programs and tests expect it. On this page every answer is in simplest form, such as 1/3 instead of 2/6."},
    {"q": "How do you estimate fraction sums with benchmark fractions?",
     "a": "Compare each fraction with 0, 1/2 and 1. For 2/5 + 1/2, 2/5 is less than 1/2, so the sum is less than 1."},
]


def gen_unit():
    rnd = random.Random(501)
    P = People(rnd)
    sets = [set_common(rnd), set_add(rnd, P), set_subtract(rnd, P), set_mixed(rnd), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "add-subtract-fractions-unlike", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Fractions with Unlike Denominators",
        "seo_title": "Grade 5 Adding and Subtracting Fractions with Unlike Denominators Worksheets: Common Denominators, Mixed Numbers and Word Problems",
        "short_title": "Add and Subtract Unlike Fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "5.NF.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NF/A/",
        "standard_text": "Add and subtract fractions with unlike denominators (including mixed numbers) by replacing given fractions with equivalent fractions in such a way as to produce an equivalent sum or difference of fractions with like denominators. Solve word problems involving addition and subtraction of fractions referring to the same whole, including cases of unlike denominators, e.g., by using visual fraction models or equations to represent the problem. Use benchmark fractions and number sense of fractions to estimate mentally and assess the reasonableness of answers.",
        "meta_desc": "Free Grade 5 worksheets on adding and subtracting fractions with unlike denominators: find a common denominator, add and subtract with fraction bars, mixed numbers with renaming, word problems and estimating with benchmarks. 100 practice questions with step-by-step answers.",
        "key_big": "Different denominators? Rewrite both fractions with a common denominator first, then add or subtract the numerators.",
        "key_sub": "1/3 + 1/4 = 4/12 + 3/12 = 7/12, not 2/7. Write the answer in simplest form, and check it with the benchmarks 0, 1/2 and 1.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "number line")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
