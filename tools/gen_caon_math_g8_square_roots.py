# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Square Roots and Real Numbers (Ontario Mathematics Curriculum 2020, Grade 8: B1.3,
with B1.2 rational and irrational numbers and B2.2 perfect squares)
  python3 tools/gen_caon_math_g8_square_roots.py
Perfect squares and their square roots (whole numbers, decimals, fractions), estimating square roots between two
whole numbers and to one decimal place, rational and irrational numbers, ordering real numbers (√10, π, 3.2), and
word problems in Ontario contexts (square fields, gardens, backyard rinks, quilts, assembly chairs).
Wrong answers come from real student mistakes: halving (√50 ≈ 25), dividing by 4 (perimeter thinking), giving the
perfect square instead of its root, rooting only the numerator, √0.49 = 0.07, √a + √b = √(a + b),
“π = 3.14 so π is rational”, “every square root is irrational”, “repeating decimals are irrational”,
√20 ≈ 4.4 (20 − 16 = 4), choosing the wrong neighbour, and truncating instead of rounding.
Every answer is checked with math.isqrt, math.sqrt and fractions.Fraction. Helpers are adapted from
gen_caon_math_g7_integers.py and gen_au_maths_y6_primes_squares.py.
Canadian English, real minus sign −, HTML attributes in single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import isqrt, sqrt, pi

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
LIGHT = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = "\u00a0"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer, Ontario style: 4 digits with no separator, 5+ with a no-break space. Real minus sign."""
    assert isinstance(v, int), v
    a = abs(v)
    s = str(a) if a < 10000 else "{:,}".format(a).replace(",", NBSP)
    return (M if v < 0 else "") + s


def d(v):
    """A number given as int, Fraction (terminating) or str: shortest exact decimal, minus sign −."""
    if isinstance(v, str):
        return v.replace("-", M)
    v = F(v)
    if v.denominator == 1:
        return n(int(v))
    neg = v < 0
    v = abs(v)
    whole = int(v)
    frac = v - whole
    digits = ""
    for _ in range(8):
        frac *= 10
        digits += str(int(frac))
        frac -= int(frac)
        if frac == 0:
            break
    assert frac == 0, v
    return (M if neg else "") + n(whole) + "." + digits


def r1(x):
    """Round a float to one decimal place (half up) and return a Fraction."""
    return F(int(math.floor(x * 10 + 0.5)), 10)


def r1s(x):
    """One decimal place as text, keeping a trailing .0."""
    v = r1(x)
    s = d(v)
    return s if "." in s else s + ".0"


def rt(x):
    return "√" + (x if isinstance(x, str) else d(x))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def rtfr(a, b):
    return "√" + fr(a, b)


def bar(s):
    """Digits under a repeat bar."""
    return "<span style='text-decoration:overline;text-decoration-thickness:0.09em'>%s</span>" % s


def sq(u):
    return u + "<sup>2</sup>"


def unit(v, u):
    return d(v) + NBSP + u


def area(v, u):
    return d(v) + NBSP + sq(u)


def approx(x, k=3):
    """x to k decimal places as text (for explanations), real minus sign."""
    return (("%." + str(k) + "f") % x).replace("-", M)


def show(name, x):
    """“name ≈ 3.162”, or “name = 2.25” when the value is exact."""
    if abs(x * 1000 - round(x * 1000)) < 1e-9:
        return "%s = %s" % (name, d(F(round(x * 1000), 1000)))
    return "%s ≈ %s" % (name, approx(x))


def plural(k, w):
    return "%d %s" % (k, w if k == 1 else w + "s")


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, fixed=None):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped. fixed: the answer index of a picture question
    whose choices must stay A, B, C, D (then cands is the full list of 4 and correct is its index)."""
    if fixed is not None:
        assert len(cands) == 4 and len({plain(c) for c in cands}) == 4
        return {"q": q, "c": list(cands), "a": fixed, "e": e, "fixed": True}
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {plain(cs)}, ({cv} if cv is not None else set()), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if not s or plain(s) in seen:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(plain(s))
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    return {"q": q, "c": [cs] + pick, "a": 0, "e": e}


def mcq_v(q, v, cands, e, fmt=d):
    """Numeric answer (int or Fraction); cands are values (None skipped)."""
    return mcq(q, (fmt(v), F(v)), [(fmt(c), F(c)) for c in cands if c is not None], e)


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Picture questions with fixed A–D choices keep their answer position."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    bd = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, bd)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (number lines, rows of squares) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def square_svg(label, u):
    """A square with its area written inside and “?” on the bottom side."""
    S, o = 96, 10
    W = S + 2 * o
    H = S + o + 26
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (o, o, S, S, LIGHT, GREEN),
         text(o + S / 2, o + S / 2 - 2, "Area", 14),
         text(o + S / 2, o + S / 2 + 18, label + " " + u + "²", 15, bold=True),
         text(o + S / 2, o + S + 21, "?", 16, bold=True, col=RED)]
    return svg_wrap(W, H, "".join(s), "square with an area of %s square %s and an unknown side length"
                    % (label, {"cm": "centimetres", "m": "metres"}[u]))


def squares_row_svg():
    """Lesson: squares with areas 49, 50 and 64; sides 7, √50 and 8."""
    k = 12     # pixels per unit of side length
    gap, o = 34, 8
    sides = [(49, "7"), (50, "√50"), (64, "8")]
    H = int(o + 8 * k + 50)
    s, x = [], o
    for a, lab in sides:
        L = sqrt(a) * k
        y0 = o + 8 * k - L
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y0, L, L, LIGHT if a != 50 else "#fdecea", GREEN if a != 50 else RED))
        s.append(text(x + L / 2, y0 + L / 2 + 5, "%d" % a, 15, bold=True))
        s.append(text(x + L / 2, o + 8 * k + 20, "side " + lab, 14, col=GREEN if a != 50 else RED, bold=(a == 50)))
        x += L + gap
    W = int(x - gap + o)
    return svg_wrap(W, H, "".join(s), "squares with areas 49, 50 and 64 and sides 7, √50 and 8")


class NL:
    """Number line from lo to hi (integers) with a labelled tick at every integer.
    Points: (value, name above, colour); names that would touch are lifted to a second row."""

    def __init__(self, lo, hi, g=56, step=1, fmt=None):
        self.lo, self.hi, self.g, self.step = lo, hi, g, step
        self.fmt = fmt or (lambda v: d(v))
        self.pad = 26
        self.W = int(2 * self.pad + (hi - lo) / step * g)
        self.pts = []

    def X(self, v):
        return self.pad + (v - self.lo) / self.step * self.g

    def point(self, v, name, col=GREEN):
        assert self.lo <= v <= self.hi, (v, self.lo, self.hi)
        self.pts.append((v, name, col))
        return self

    def svg(self, label):
        rows, last = [], {}
        for v, nm, col in sorted(self.pts):
            x = self.X(v)
            w = len(plain(nm)) * 9 + 8
            row = 0
            while row in last and last[row] > x - w / 2:
                row += 1
            last[row] = x + w / 2
            rows.append((v, nm, col, row))
        top = 18 * (1 + max(r for *_, r in rows)) if rows else 0
        Y = 16 + top
        H = Y + 34
        s = []
        x0, x1 = self.pad - 16, self.W - self.pad + 16
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, Y, x1, Y, INK))
        s.append("<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (x0 - 2, Y, x1 + 2, Y, INK))
        k = 0
        while True:
            v = F(self.lo) + k * F(self.step)
            if v > self.hi:
                break
            x = self.X(v)
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 7, x, Y + 7, INK))
            s.append(text(x, Y + 25, self.fmt(v), 14))
            k += 1
        for v, nm, col, row in rows:
            x = self.X(v)
            s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (x, Y, col))
            s.append(text(x, Y - 11 - 18 * row, nm, 15, bold=True, col=col))
        return svg_wrap(self.W, H, "".join(s), label)


# ============================================================ set 1: perfect squares and square roots
def set_perfect(rnd, P):
    its = []
    # A: square roots of perfect squares (7)
    for N in [49, 81, 121, 144, 225, 400, 900]:
        r = isqrt(N)
        assert r * r == N
        e = "%d × %d = %d, so √%d = <b>%d</b>. Do not halve: %d ÷ 2 = %s, and %s × %s is not %d." % (
            r, r, N, N, r, N, d(F(N, 2)), d(F(N, 2)), d(F(N, 2)), N)
        its.append(mcq_v("What is √%d?" % N, r, [F(N, 2), r + 1, r - 1, N], e))
    # B: squaring (2)
    for k in [13, 16]:
        e = "%d<sup>2</sup> means %d × %d = <b>%d</b>, not %d × 2 = %d." % (k, k, k, k * k, k, 2 * k)
        its.append(mcq_v("What is %d<sup>2</sup>?" % k, k * k, [2 * k, (k - 1) ** 2, (k + 1) ** 2], e))
    # C: which is (not) a perfect square (3)
    e = ("196 = 14 × 14, so 196 is a <b>perfect square</b>. 160, 140 and 200 are not: 12<sup>2</sup> = 144, "
         "13<sup>2</sup> = 169, 14<sup>2</sup> = 196 and 15<sup>2</sup> = 225. A number ending in 0 is not always a square.")
    assert isqrt(196) ** 2 == 196 and all(isqrt(x) ** 2 != x for x in (160, 140, 200))
    its.append(mcq("Which number is a perfect square?", "196", ["160", "140", "200"], e))
    e = ("225 = 15 × 15, so 225 is a <b>perfect square</b>. 125 = 5 × 5 × 5 is a cube, not a square. "
         "250 and 150 are between perfect squares.")
    assert isqrt(225) ** 2 == 225 and all(isqrt(x) ** 2 != x for x in (125, 250, 150))
    its.append(mcq("Which number is a perfect square?", "225", ["125", "250", "150"], e))
    e = ("36 = 6<sup>2</sup>, 64 = 8<sup>2</sup> and 100 = 10<sup>2</sup>. 9<sup>2</sup> = 81 and 10<sup>2</sup> = 100, "
         "so <b>90</b> is not a perfect square, even though 9 is a perfect square.")
    assert isqrt(90) ** 2 != 90
    its.append(mcq("Which number is <b>not</b> a perfect square?", "90", ["36", "64", "100"], e))
    # D: decimals and fractions (5)
    for N, r in [(F(49, 100), F(7, 10)), (F(9, 100), F(3, 10)), (F(144, 100), F(12, 10))]:
        assert r * r == N
        e = "%s × %s = %s, so %s = <b>%s</b>. Check: %s × %s = %s, not %s." % (
            d(r), d(r), d(N), rt(N), d(r), d(r / 10), d(r / 10), d(r * r / 100), d(N))
        its.append(mcq_v("What is %s?" % rt(N), r, [r / 10, N / 2, r * 10], e))
    for a, b in [(9, 16), (25, 36)]:
        ra, rb = isqrt(a), isqrt(b)
        e = "Take the square root of the top and the bottom: √%d = %d and √%d = %d, so %s = <b>%s</b>." % (
            a, ra, b, rb, rtfr(a, b), fr(ra, rb)) + " Check: %s × %s = %s." % (fr(ra, rb), fr(ra, rb), fr(a, b))
        its.append(mcq("What is %s?" % rtfr(a, b), fr(ra, rb), [fr(ra, b), fr(a, rb), fr(a, 2 * b)], e))
    # E: square with a given area (2)
    for A, u, wr in [(64, "cm", [16, 32, 4]), (169, "m", [F(169, 4), F(169, 2), 12])]:
        r = isqrt(A)
        e = ("The area of a square is side × side. %d × %d = %d, so each side is √%d = <b>%d" % (r, r, A, A, r) + NBSP + u +
             "</b>. Dividing by 4 (%s) gives the side from the <i>perimeter</i>, not the area." % d(F(A, 4)))
        its.append(mcq_v(fig(square_svg(str(A), u)) + "The area of this square is %s. How long is each side?" % area(A, u),
                         r, wr, e, fmt=lambda v, u=u: unit(v, u)))
    # F: √a + √b is not √(a + b) (1)
    e = ("Find each root first: √36 = 6 and √64 = 8, so √36 + √64 = 6 + 8 = <b>14</b>. "
         "You cannot add under the root sign: √(36 + 64) = √100 = 10 is a different number.")
    its.append(mcq_v("What is √36 + √64?", 14, [10, 100, 50], e))
    assert len(its) == 20
    return {"title": "Perfect squares and square roots", "items": its}


# ============================================================ set 2: estimating square roots
def between(N):
    a = isqrt(N)
    assert a * a < N < (a + 1) ** 2
    return a


def set_estimate(rnd, P):
    its = []
    # A: between which two whole numbers (8)
    for N in [50, 30, 20, 75, 90, 110, 130, 200]:
        a = between(N)
        h = N // 2
        e = ("Find the perfect squares on each side: %d<sup>2</sup> = %d and %d<sup>2</sup> = %d. %d is between them, "
             "so √%d is between <b>%d and %d</b>. (√%d is about %s.)" % (a, a * a, a + 1, (a + 1) ** 2, N, N, a, a + 1, N, approx(sqrt(N), 2)))
        its.append(mcq("√%d is between which two whole numbers?" % N, "%d and %d" % (a, a + 1),
                       ["%d and %d" % (h, h + 1), "%d and %d" % (a - 1, a), "%d and %d" % (a + 1, a + 2)], e))
    # B: number line with points A–D (4); choices stay A, B, C, D
    plans = [(40, 4, 9, [F(4), F(56, 10), F(63, 10), F(77, 10)]),
             (80, 5, 10, [F(64, 10), F(8), F(85, 10), F(89, 10)]),
             (10, 0, 6, [F(1), F(32, 10), F(38, 10), F(5)]),
             (55, 4, 9, [F(55, 10), F(66, 10), F(74, 10), F(84, 10)])]
    for N, lo, hi, pts in plans:
        a = between(N)
        right = min(range(4), key=lambda i: abs(float(pts[i]) - sqrt(N)))
        assert abs(float(pts[right]) - sqrt(N)) < 0.06
        assert sorted(pts) == pts
        nl = NL(lo, hi)
        for i, v in enumerate(pts):
            nl.point(v, "ABCD"[i], GREEN)
        svg = nl.svg("number line from %d to %d with points A, B, C and D" % (lo, hi))
        near = a if sqrt(N) - a < 0.5 else a + 1
        e = ("%d<sup>2</sup> = %d and %d<sup>2</sup> = %d, so √%d is between %d and %d. %d is closer to %d, so √%d is closer to %d. "
             "√%d ≈ %s, so the answer is <b>point %s</b>." % (a, a * a, a + 1, (a + 1) ** 2, N, a, a + 1, N,
                                                             near * near, N, near, N, approx(sqrt(N), 2), "ABCD"[right]))
        its.append(mcq(fig(svg) + "Which point is closest to √%d on the number line?" % N, None, ["A", "B", "C", "D"], e, fixed=right))
    # C: closest whole number (4)
    for N in [60, 28, 84, 140]:
        a = between(N)
        near = a if sqrt(N) - a < 0.5 else a + 1
        other = a + 1 if near == a else a
        e = ("%d<sup>2</sup> = %d and %d<sup>2</sup> = %d. %d is closer to %d, so √%d is closest to <b>%d</b>. "
             "(√%d ≈ %s.) The answer is a root, not the perfect square %d." % (a, a * a, a + 1, (a + 1) ** 2, N, near * near, N, near,
                                                                           N, approx(sqrt(N), 2), near * near))
        its.append(mcq_v("Which whole number is √%d closest to?" % N, near, [other, near * near, F(N, 2)], e))
    # D: to one decimal place (4)
    for N, wrong in [(50, [F(25), F(75, 10), F(79, 10)]), (22, [F(11), F(46, 10), F(43, 10)]),
                     (45, [F(45, 2), F(69, 10), F(63, 10)]), (88, [F(44), F(97, 10), F(96, 10)])]:
        a = between(N)
        v = r1(sqrt(N))
        assert v not in wrong
        assert (v - F(1, 10)) ** 2 < N < (v + F(1, 10)) ** 2
        e = ("%d<sup>2</sup> = %d and %d<sup>2</sup> = %d, so √%d is between %d and %d. √%d ≈ %s, so to one decimal place "
             "√%d ≈ <b>%s</b>. Check: %s<sup>2</sup> = %s, close to %d." % (a, a * a, a + 1, (a + 1) ** 2, N, a, a + 1, N,
                                                                         approx(sqrt(N), 3), N, d(v), d(v), d(v * v), N))
        its.append(mcq_v("Estimate √%d to one decimal place." % N, v, wrong, e))
    assert len(its) == 20
    return {"title": "Estimating square roots", "items": its}


# ============================================================ set 3: rational or irrational
def set_rational(rnd, P):
    its = []
    rep3 = "0." + bar("3")
    # A: rational or irrational, with the reason (8)
    A = [
        ("√49", ["Rational, because √49 = 7", "Irrational, because every square root is irrational",
                 "Irrational, because 49 is not a perfect square", "Rational, because √49 = 24.5"],
         "7 × 7 = 49, so √49 = 7, and 7 = " + fr(7, 1) + " is <b>rational</b>. The square root of a perfect square is rational."),
        ("√12", ["Irrational, because 12 is not a perfect square", "Rational, because 12 is a whole number",
                 "Rational, because √12 = 6", "Rational, because √12 = 3.46 exactly"],
         "9 &lt; 12 &lt; 16, so 12 is not a perfect square. Its root, 3.4641…, never ends and never repeats, so √12 is <b>irrational</b>."),
        ("π", ["Irrational, because its decimal never ends or repeats", "Rational, because π = 3.14",
               "Rational, because π = " + fr(22, 7), "Rational, because its decimal repeats"],
         "π = 3.14159265… never ends and never repeats, so π is <b>irrational</b>. 3.14 and " + fr(22, 7) + " are only close to π."),
        (rep3, ["Rational, because it equals " + fr(1, 3), "Irrational, because its decimal never ends",
                "Irrational, because 3 does not divide 10 evenly", "Rational, because it equals " + fr(3, 10)],
         "1 ÷ 3 = 0.333…, so " + rep3 + " = " + fr(1, 3) + ". A repeating decimal is <b>rational</b>. " + fr(3, 10) + " = 0.3 stops after one digit."),
        (M + "5", ["Rational, because " + M + "5 = " + fr(M + "5", 1), "Irrational, because it is negative",
                   "Irrational, because it is not written as a fraction", "Irrational, because " + M + "5 is not a whole number"],
         M + "5 = " + fr(M + "5", 1) + ", a quotient of two integers, so it is <b>rational</b>. Every integer is rational."),
        (fr(22, 7), ["Rational, because it is a fraction of two integers", "Irrational, because it equals π",
                     "Irrational, because 22 ÷ 7 does not divide evenly", "Rational, because it equals 3.14"],
         fr(22, 7) + " is 22 ÷ 7, a quotient of two integers, so it is <b>rational</b>. Its decimal 3.142857142857… repeats. It is close to π but not equal to it."),
        ("√0.25", ["Rational, because √0.25 = 0.5", "Irrational, because 0.25 is not a perfect square",
                   "Rational, because √0.25 = 0.125", "Irrational, because it is the root of a decimal"],
         "0.5 × 0.5 = 0.25, so √0.25 = 0.5 = " + fr(1, 2) + ", which is <b>rational</b>. Halving gives 0.125, but 0.125 × 0.125 = 0.015625."),
        ("0.1010010001…", ["Irrational, because the digits never end and never repeat", "Rational, because the decimal has a pattern",
                           "Rational, because it only uses the digits 0 and 1", "Rational, because it repeats 10"],
         "The number of 0s keeps growing (1, 2, 3, …), so no block of digits repeats. The decimal never ends and never repeats: it is <b>irrational</b>."),
    ]
    assert F(22, 7) != F(314, 100) and F(1, 2) ** 2 == F(25, 100) and isqrt(12) ** 2 != 12
    for x, ch, e in A:
        its.append(mcq("Is %s rational or irrational?" % x, ch[0], ch[1:], e))
    # B: which number is irrational (4)
    rep12 = "0." + bar("12")
    B = [
        (["√20", "√16", "0.25", fr(4, 5)],
         "16 is a perfect square (√16 = 4), but 20 is not. So <b>√20</b> = 4.472… is irrational. 0.25 and " + fr(4, 5) + " are rational."),
        (["π", "3.14", fr(22, 7), "√9"],
         "<b>π</b> = 3.14159… never ends and never repeats. 3.14 and " + fr(22, 7) + " are fractions close to π, and √9 = 3."),
        (["0.1211211121112…", rep12, "0.125", M + "12"],
         "In <b>0.1211211121112…</b> the number of 1s keeps growing, so no block repeats. " + rep12 + " repeats 12, so it is rational (" + fr(4, 33) + ")."),
        (["√50", "√0.04", rtfr(4, 9), M + "√64"],
         "√0.04 = 0.2, " + rtfr(4, 9) + " = " + fr(2, 3) + " and " + M + "√64 = " + M + "8 are rational. 50 is not a perfect square, so <b>√50</b> is irrational."),
    ]
    assert F(12, 99) == F(4, 33) and F(2, 10) ** 2 == F(4, 100) and isqrt(20) ** 2 != 20 and isqrt(50) ** 2 != 50
    for ch, e in B:
        its.append(mcq("Which number is irrational?", ch[0], ch[1:], e))
    # C: which number is rational (4)
    rep4 = "0." + bar("4")
    C = [
        (["√36", "√6", "π", "√30"],
         "6 × 6 = 36, so <b>√36</b> = 6 is rational. 6 and 30 are not perfect squares, and π is irrational."),
        ([rep4, "√2", "0.454554555…", "√40"],
         "<b>" + rep4 + "</b> = 0.444… repeats, so it is rational: it equals " + fr(4, 9) + ". The other decimals never end and never repeat."),
        ([fr(M + "7", 3), "√11", "2π", "√7"],
         "<b>" + fr(M + "7", 3) + "</b> is a quotient of two integers, so it is rational, even though it is negative. 2π, √11 and √7 are irrational."),
        (["√1.21", "√1.2", "√12", "√120"],
         "1.1 × 1.1 = 1.21, so <b>√1.21</b> = 1.1 is rational. 1.2, 12 and 120 are not perfect squares of rational numbers."),
    ]
    assert F(11, 10) ** 2 == F(121, 100) and F(4, 9) == F(4, 9)
    for ch, e in C:
        its.append(mcq("Which number is rational?", ch[0], ch[1:], e))
    # D: statements and number systems (4)
    its.append(mcq("Which statement is true?", "Every integer is a rational number.",
                   ["π is rational, because π = 3.14.", "Every square root is irrational.", "A repeating decimal is irrational."],
                   "Any integer can be written over 1, for example " + M + "4 = " + fr(M + "4", 1) + ", so <b>every integer is rational</b>. "
                   "π is irrational, √9 = 3 is rational, and repeating decimals are rational."))
    its.append(mcq("Which statement about √2 is true?", "Its decimal never ends and never repeats.",
                   ["√2 = 1.41 exactly.", "It is rational, because 2 is an integer.", "√2 = 1, because 2 ÷ 2 = 1."],
                   "1.41 × 1.41 = 1.9881, not 2, and no fraction squares to exactly 2. √2 = 1.41421356… <b>never ends and never repeats</b>, so it is irrational."))
    its.append(mcq("Which sets of numbers does " + M + "6 belong to?", "Integers and rational numbers",
                   ["Whole numbers and integers", "Irrational numbers only", "Whole numbers only"],
                   "Whole numbers are 0, 1, 2, 3, …, so " + M + "6 is not one. " + M + "6 is an <b>integer</b>, and every integer is a "
                   "<b>rational number</b> (" + fr(M + "6", 1) + ")."))
    assert F(1, 3) != F(3, 10) and F(1, 3) != F(33, 100)
    its.append(mcq("Which fraction is equal to " + rep3 + "?", fr(1, 3), [fr(3, 10), fr(33, 100), fr(3, 100)],
                   "1 ÷ 3 = 0.333… with the 3 repeating forever, so " + rep3 + " = <b>" + fr(1, 3) + "</b>. "
                   + fr(33, 100) + " = 0.33 stops after two digits."))
    assert len(its) == 20
    return {"title": "Rational or irrational?", "items": its}


# ============================================================ set 4: ordering real numbers
def set_order(rnd, P):
    its = []

    def val(x):
        return x[1]

    # A: which is greater (6)
    pairs = [(("√10", sqrt(10)), ("3.2", 3.2)), (("√20", sqrt(20)), ("4.4", 4.4)), (("π", pi), ("√10", sqrt(10))),
             (("√50", sqrt(50)), ("7.1", 7.1)), (("√30", sqrt(30)), ("5.5", 5.5)), (("√65", sqrt(65)), ("8.1", 8.1))]
    for x, y in pairs:
        big, small = (x, y) if x[1] > y[1] else (y, x)
        assert abs(x[1] - y[1]) > 0.01

        if x[0] == "π":
            e = "π ≈ %s and √10 ≈ %s. So <b>√10</b> is greater, but only by about 0.02." % (approx(pi), approx(sqrt(10)))
            assert big[0] == "√10"
        else:
            sq_ = F(y[0]) ** 2
            N = int(x[0][1:])
            assert (sq_ > N) == (y[1] > x[1])
            e = ("Square the decimal: %s<sup>2</sup> = %s, and %s %s %d. So %s %s %s, and <b>%s</b> is greater. (%s ≈ %s.)"
                 % (y[0], d(sq_), d(sq_), "&gt;" if sq_ > N else "&lt;", N, y[0], "&gt;" if sq_ > N else "&lt;", x[0],
                    big[0], x[0], approx(x[1])))
        its.append(mcq("Which number is greater: %s or %s?" % (x[0], y[0]), big[0], [small[0], "They are equal", "You cannot compare them"], e))
    # B: order from least to greatest (6)
    lists = [[("√10", sqrt(10)), ("π", pi), ("3.2", 3.2)],
             [("√5", sqrt(5)), ("2.2", 2.2), (fr(9, 4), 2.25)],
             [("√2", sqrt(2)), ("1.4", 1.4), ("1.5", 1.5)],
             [("√40", sqrt(40)), ("6.3", 6.3), ("2π", 2 * pi)],
             [(M + "√9", -3.0), (M + "2.5", -2.5), (M + "√5", -sqrt(5))],
             [("√17", sqrt(17)), ("4.1", 4.1), (fr(17, 4), 4.25)]]
    for L in lists:
        o = sorted(L, key=val)
        assert all(o[i + 1][1] - o[i][1] > 0.005 for i in range(2))
        names = lambda seq: ", ".join(t[0] for t in seq)
        q = "Which list is in order from least to greatest: %s?" % names(L)
        right = names(o)
        wrong = [names(o[::-1]), names([o[1], o[0], o[2]]), names([o[0], o[2], o[1]])]
        e = "Write each as a decimal: " + ", ".join(
            show(t[0], t[1]) if not re.fullmatch(r"[0-9.−]+", t[0]) else t[0] for t in o) + \
            ". From least to greatest: <b>%s</b>." % right
        its.append(mcq(q, right, wrong, e))
    # C: between two whole numbers (3)
    for lo, right, wrong in [(5, 30, ["√5.5", "√11", "√40"]), (8, 70, ["√8.5", "√17", "√60"]), (3, 12, ["√3.5", "√7", "√20"])]:
        assert lo ** 2 < right < (lo + 1) ** 2
        for w in wrong:
            v = float(w[1:])
            assert not lo ** 2 < v < (lo + 1) ** 2
        e = ("%d<sup>2</sup> = %d and %d<sup>2</sup> = %d, so a square root between %d and %d must have a number between %d and %d "
             "under the root sign. Only <b>√%d</b> works (√%d ≈ %s)." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, lo, lo + 1, lo * lo,
                                                                          (lo + 1) ** 2, right, right, approx(sqrt(right), 2)))
        its.append(mcq("Which number is between %d and %d?" % (lo, lo + 1), "√%d" % right, wrong, e))
    # D: greatest / least (5)
    D = [("greatest", [("5.1", 5.1), ("√26", sqrt(26)), ("5.09", 5.09), ("5.01", 5.01)]),
         ("least", [("3.14", 3.14), ("π", pi), ("√10", sqrt(10)), (fr(22, 7), 22 / 7)]),
         ("greatest", [(M + "1.4", -1.4), (M + "√2", -sqrt(2)), (M + "1.5", -1.5), (M + "√3", -sqrt(3))]),
         ("least", [("√0.2", sqrt(0.2)), ("√0.5", sqrt(0.5)), ("0.5", 0.5), ("0.71", 0.71)]),
         ("greatest", [("√101", sqrt(101)), ("√99", sqrt(99)), ("9.9", 9.9), ("10", 10.0)])]
    for word, L in D:
        pick = max(L, key=val) if word == "greatest" else min(L, key=val)
        assert pick is L[0]
        vals = sorted(t[1] for t in L)
        assert all(vals[i + 1] - vals[i] > 0.0005 for i in range(3))
        e = "As decimals: " + ", ".join(
            show(t[0], t[1]) if not re.fullmatch(r"[0-9.−]+", t[0]) else t[0] for t in sorted(L, key=val)) + \
            ". The %s is <b>%s</b>." % (word, pick[0])
        if L[0][0] == "3.14":
            e += " π is a little more than 3.14, so 3.14 is not equal to π."
        if word == "greatest" and L[0][0].startswith(M):
            e += " For negative numbers, the one closest to 0 is the greatest."
        its.append(mcq("Which number is the %s: %s?" % (word, ", ".join(t[0] for t in sorted(L, key=lambda t: t[0]))),
                       pick[0], [t[0] for t in L[1:]], e))
    assert len(its) == 20
    return {"title": "Comparing and ordering real numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    m_ = lambda v: unit(v, "m")
    cm_ = lambda v: unit(v, "cm")

    def mq(q, v, cands, e, fmt=d):
        its.append(mcq_v(q, v, cands, e, fmt=fmt))

    # 1 soccer field
    assert isqrt(2500) == 50
    mq("A square soccer practice field in Mississauga has an area of %s. How long is each side?" % area(2500, "m"),
       50, [1250, 625, 250], "Side × side = 2500. 50 × 50 = 2500, so each side is √2500 = <b>50" + NBSP + "m</b>.", fmt=m_)
    # 2 garden between
    nm, he, his = P.next()
    assert 36 < 40 < 49
    its.append(mcq("%s plants a square vegetable garden with an area of %s. Each side is between which two lengths?" % (nm, area(40, "m")),
                   "6" + NBSP + "m and 7" + NBSP + "m", ["20" + NBSP + "m and 21" + NBSP + "m", "5" + NBSP + "m and 6" + NBSP + "m",
                                                          "7" + NBSP + "m and 8" + NBSP + "m"],
                   "6<sup>2</sup> = 36 and 7<sup>2</sup> = 49. 40 is between them, so each side is between <b>6" + NBSP + "m and 7" + NBSP +
                   "m</b> (√40 ≈ 6.32" + NBSP + "m)."))
    # 3 patio to nearest tenth
    v = r1(sqrt(30))
    assert v == F(55, 10)
    mq("A square patio at a cottage has an area of %s. How long is each side, to the nearest tenth of a metre?" % area(30, "m"),
       v, [15, F(75, 10), F(54, 10)], "√30 ≈ %s. The hundredths digit is 7, so round up: <b>5.5" % approx(sqrt(30)) + NBSP + "m</b>. "
       "Check: 5.5<sup>2</sup> = 30.25, which is close to 30.", fmt=m_)
    # 4 fence around a square field
    mq("A square horse paddock near Guelph has an area of %s. How much fencing goes around it?" % area(900, "m"),
       120, [30, 225, 3600], "Each side is √900 = 30" + NBSP + "m. A square has 4 equal sides: 4 × 30 = <b>120" + NBSP + "m</b>.", fmt=m_)
    # 5 assembly chairs
    assert isqrt(196) == 14
    mq("For a school assembly, 196 chairs are set out in a square: the number of rows equals the number of chairs in each row. "
       "How many rows are there?", 14, [98, 49, 13], "Rows × chairs per row = 196, and they are equal. 14 × 14 = 196, so there are <b>14 rows</b>.",
       fmt=lambda x: plural(int(x), "row"))
    # 6 quilt
    nm, he, his = P.next()
    mq("%s sews a square quilt from 64 small square patches. How many patches are in each row?" % nm,
       8, [32, 16, 7], "Patches per row × number of rows = 64, and the quilt is square. 8 × 8 = 64, so there are <b>8 patches</b> in each row.",
       fmt=lambda x: plural(int(x), "patch").replace("patchs", "patches"))
    # 7 canvas
    assert F(9, 10) ** 2 == F(81, 100)
    mq("An art class in Ottawa paints on a square canvas with an area of %s. How long is each side?" % area(F(81, 100), "m"),
       F(9, 10), [F(9, 100), F(81, 200), 9], "0.9 × 0.9 = 0.81, so each side is √0.81 = <b>0.9" + NBSP + "m</b>. "
       "(0.09 × 0.09 = 0.0081, which is too small.)", fmt=m_)
    # 8 backyard rink to the nearest metre
    nm, he, his = P.next()
    assert round(sqrt(150)) == 12
    mq("%s floods a square backyard rink with an area of %s. To the nearest metre, how long is each side?" % (nm, area(150, "m")),
       12, [75, 13, F(75, 2)], "12<sup>2</sup> = 144 and 13<sup>2</sup> = 169. 150 is much closer to 144, so the side is about "
       "<b>12" + NBSP + "m</b> (√150 ≈ %s" % approx(sqrt(150), 2) + NBSP + "m).", fmt=m_)
    # 9 tiles per row
    mq("A square bathroom floor has an area of %s. It is covered with square tiles that are 0.5" % area(16, "m") + NBSP +
       "m on each side. How many tiles are in each row?", 8, [32, 4, 64],
       "Each side of the floor is √16 = 4" + NBSP + "m. 4 ÷ 0.5 = <b>8 tiles</b> in each row (and 64 tiles in all).",
       fmt=lambda x: plural(int(x), "tile"))
    # 10 hectares
    assert isqrt(40000) == 200
    mq("A square farm field near Woodstock has an area of 4 hectares. One hectare is 10" + NBSP + "000" + NBSP + "m<sup>2</sup>. "
       "How long is each side of the field?", 200, [2, 20000, 10000],
       "4 hectares = 4 × 10" + NBSP + "000 = 40" + NBSP + "000" + NBSP + "m<sup>2</sup>. 200 × 200 = 40" + NBSP + "000, so each side is <b>200" +
       NBSP + "m</b>. √4 = 2 forgets to change hectares to square metres.", fmt=m_)
    # 11 falling ball
    assert F(196, 10) / F(49, 10) == 4
    mq("In science class, students learn that the time in seconds for a ball to fall <i>d</i> metres is about √(<i>d</i> ÷ 4.9). "
       "A ball is dropped from a balcony 19.6" + NBSP + "m high. About how long does it take to reach the ground?",
       2, [4, F(98, 10), F(44, 10)], "19.6 ÷ 4.9 = 4, and √4 = <b>2 seconds</b>. Do not stop at 4: you still need the square root.",
       fmt=lambda x: d(x) + " seconds")
    # 12 tablecloth
    assert sqrt(2) < 1.5
    nm, he, his = P.next()
    its.append(mcq("%s has a square tablecloth with an area of %s. Is it wide enough to cover a square table that is 1.5" % (nm, area(2, "m")) +
                   NBSP + "m wide?", "No. Each side is about 1.4" + NBSP + "m.",
                   ["Yes. Each side is 2" + NBSP + "m.", "Yes. Each side is 1.5" + NBSP + "m.", "No. Each side is 0.5" + NBSP + "m."],
                   "Each side is √2 ≈ 1.41" + NBSP + "m, and 1.41 &lt; 1.5. <b>No</b>, it is about 9" + NBSP + "cm too narrow. "
                   "√2 is not 2: 2 × 2 = 4."))
    # 13 poster
    mq("A square poster for the Terry Fox Run has an area of %s. How long is each side?" % area(3600, "cm"),
       60, [1800, 900, 6], "60 × 60 = 3600, so each side is √3600 = <b>60" + NBSP + "cm</b>. (6 × 6 = 36, not 3600.)", fmt=cm_)
    # 14 photo doubled
    nm, he, his = P.next()
    v = r1(sqrt(200))
    assert v == F(141, 10)
    mq("%s has a square photo with an area of %s. %s wants a square print with double the area, %s. "
       "To the nearest tenth of a centimetre, how long is each side of the new print?" % (nm, area(100, "cm"), he.capitalize(), area(200, "cm")),
       v, [20, 100, 50], "Each side is √200 ≈ %s" % approx(sqrt(200)) + NBSP + "cm ≈ <b>14.1" + NBSP + "cm</b>. "
       "Doubling the side to 20" + NBSP + "cm would make the area 400" + NBSP + "cm<sup>2</sup>, four times as big.", fmt=cm_)
    # 15 tent
    assert F(25, 10) ** 2 == F(625, 100)
    mq("A tent for a canoe trip in Algonquin Park has a square floor with an area of %s. How long is each side?" % area(F(625, 100), "m"),
       F(25, 10), [F(3125, 1000), 25, F(625, 100)], "2.5 × 2.5 = 6.25, so each side is √6.25 = <b>2.5" + NBSP + "m</b>.", fmt=m_)
    # 16 cottage lot
    assert 31 ** 2 < 1000 < 32 ** 2
    its.append(mcq("A square cottage lot has an area of 1000" + NBSP + "m<sup>2</sup>. Each side is between which two lengths?",
                   "31" + NBSP + "m and 32" + NBSP + "m", ["500" + NBSP + "m and 501" + NBSP + "m", "30" + NBSP + "m and 31" + NBSP + "m",
                                                          "100" + NBSP + "m and 101" + NBSP + "m"],
                   "31<sup>2</sup> = 961 and 32<sup>2</sup> = 1024. 1000 is between them, so each side is between <b>31" + NBSP +
                   "m and 32" + NBSP + "m</b> (√1000 ≈ 31.62" + NBSP + "m)."))
    # 17 √50 ≈ 25 claim
    nm, he, his = P.next()
    its.append(mcq("A square has an area of %s. %s says each side is 25" % (area(50, "cm"), nm) + NBSP + "cm. Which statement is correct?",
                   "%s is wrong. Each side is about 7.1" % nm + NBSP + "cm.",
                   ["%s is right, because 50 ÷ 2 = 25." % nm, "%s is wrong. Each side is 12.5" % nm + NBSP + "cm.",
                    "%s is wrong. Each side is about 7.5" % nm + NBSP + "cm."],
                   "25 × 25 = 625, not 50. 7<sup>2</sup> = 49, so √50 is just over 7: √50 ≈ 7.07 ≈ <b>7.1" + NBSP + "cm</b>. "
                   "12.5 is 50 ÷ 4, the side from a perimeter of 50" + NBSP + "cm."))
    # 18 sandbox border
    nm, he, his = P.next()
    assert 4 * sqrt(5) < 9
    its.append(mcq("%s builds a square sandbox with an area of %s. %s has 9" % (nm, area(5, "m"), he.capitalize()) + NBSP +
                   "m of wood for the border. Is that enough?",
                   "Yes. %s needs about 8.9" % he.capitalize() + NBSP + "m.",
                   ["No. %s needs 20" % he.capitalize() + NBSP + "m.", "No. %s needs 10" % he.capitalize() + NBSP + "m.",
                    "Yes. %s needs 5" % he.capitalize() + NBSP + "m."],
                   "Each side is √5 ≈ 2.236" + NBSP + "m. The border is 4 × 2.236 ≈ 8.94" + NBSP + "m, which is less than 9" + NBSP +
                   "m. <b>Yes</b>, it is enough. (4 × 5 = 20 uses the area as the side.)"))
    # 19 plywood
    assert F(17, 10) ** 2 == F(289, 100)
    mq("A square sheet of plywood for a snow fort roof has an area of %s. How long is each side?" % area(F(289, 100), "m"),
       F(17, 10), [F(289, 200), 17, F(17, 100)], "1.7 × 1.7 = 2.89, so each side is √2.89 = <b>1.7" + NBSP + "m</b>. "
       "Check the decimal place: 17 × 17 = 289, and 2.89 has two decimal places, so the root has one.", fmt=m_)
    # 20 two plots
    assert sqrt(50) < 7.2
    its.append(mcq("Plot A in a community garden is a square with an area of %s. Plot B is a square with sides of 7.2" % area(50, "m") +
                   NBSP + "m. Which plot has longer sides?",
                   "Plot B, because √50 ≈ 7.07" + NBSP + "m",
                   ["Plot A, because 50 is greater than 7.2", "Plot A, because √50 = 25" + NBSP + "m", "They have the same side length"],
                   "Plot A’s side is √50 ≈ 7.07" + NBSP + "m. 7.07 &lt; 7.2, so <b>Plot B</b> has longer sides. "
                   "Compare side with side, not area with side."))
    assert len(its) == 20
    return {"title": "Word problems: squares, sides and areas", "items": its}


# ============================================================ lesson
def body_html():
    f_sq = squares_row_svg()
    nl = NL(F(3), F(33, 10), g=90, step=F(1, 10), fmt=lambda v: d(v) if F(v).denominator != 1 else d(v) + ".0")
    nl.point(pi, "π").point(sqrt(10), "√10", RED).point(F(32, 10), "3.2")
    f_nl = nl.svg("number line from 3.0 to 3.3 with π, √10 and 3.2 marked")
    rep3 = "0." + bar("3")
    return (
        "<h2>Perfect squares and square roots</h2>"
        "<p>A <b>perfect square</b> is a whole number times itself: 7 × 7 = 49, so 49 is a perfect square. "
        "The <b>square root</b> undoes squaring. √49 = 7, because 7<sup>2</sup> = 49.</p>" +
        table(["n", "10", "11", "12", "13", "14", "15", "20", "30"],
              [["n<sup>2</sup>", "100", "121", "144", "169", "196", "225", "400", "900"]]) +
        "<p>Decimals and fractions can have exact roots too: √0.49 = 0.7 and √" + fr(9, 16) + " = " + fr(3, 4) + ".</p>"
        "<h2>Estimating a square root</h2>"
        "<p>Find the perfect squares on each side of the number. The root is between their roots.</p>"
        "<figure class='sn-fig'>" + f_sq +
        "<figcaption>49 &lt; 50 &lt; 64, so 7 &lt; √50 &lt; 8. 50 is very close to 49, so √50 ≈ 7.1.</figcaption></figure>" +
        ex("Example 1", "Estimate √30 to one decimal place.",
           "5<sup>2</sup> = 25 and 6<sup>2</sup> = 36, so √30 is between 5 and 6, a little closer to 5. "
           "Try 5.4<sup>2</sup> = 29.16 and 5.5<sup>2</sup> = 30.25. 30 is closer to 30.25.", "√30 ≈ 5.5") +
        "<h2>Rational and irrational numbers</h2>"
        "<p>A <b>rational number</b> can be written as a fraction of two integers. Its decimal stops (0.75) or repeats (" + rep3 + " = " + fr(1, 3) + "). "
        "An <b>irrational number</b> cannot be written as a fraction. Its decimal never ends and never repeats.</p>" +
        table(["Rational", "Irrational"], [
            [M + "5, 0.75, " + rep3 + ", " + fr(22, 7) + ", √49 = 7", "π, √2, √10, √50, 0.1010010001…"]]) +
        "<p>Together, the rational and irrational numbers make the <b>real numbers</b>. The square root of a whole number "
        "that is not a perfect square is always irrational.</p>"
        "<h2>Ordering real numbers</h2>"
        "<p>Change each number to a decimal, then compare.</p>"
        "<figure class='sn-fig'>" + f_nl +
        "<figcaption>π ≈ 3.142, √10 ≈ 3.162 and 3.2. From least to greatest: π, √10, 3.2.</figcaption></figure>" +
        ex("Example 2", "A square field has an area of 2500" + NBSP + "m<sup>2</sup>. How long is each side?",
           "Side × side = 2500. 50 × 50 = 2500.", "50" + NBSP + "m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["√50 ≈ 25", "Do not halve. 7<sup>2</sup> = 49, so √50 ≈ 7.1"],
            ["π is rational, because π = 3.14", "3.14 is only close to π. π never ends or repeats, so it is irrational"],
            ["Every square root is irrational", "√49 = 7 and √0.25 = 0.5 are rational"],
            ["√0.49 = 0.07", "0.07 × 0.07 = 0.0049. √0.49 = 0.7"],
            ["√36 + √64 = √100 = 10", "Find each root first: 6 + 8 = 14"],
        ])
    )


FAQ = [
    {"q": "How do you estimate a square root without a calculator?",
     "a": "Find the perfect squares on each side of the number. For √50: 7 × 7 = 49 and 8 × 8 = 64, so √50 is between 7 and 8 and very close to 7, about 7.1."},
    {"q": "Is π a rational or irrational number?",
     "a": "π is irrational. Its decimal 3.14159… never ends and never repeats. 3.14 and 22/7 are rational numbers that are only close to π."},
    {"q": "Which Ontario Grade 8 expectations cover square roots and real numbers?",
     "a": "In the Number strand of the 2020 Ontario math curriculum, B1.3 is about estimating and calculating square roots, B1.2 about rational and irrational numbers, and B2.2 about perfect squares and square roots."},
    {"q": "What are the perfect squares from 1 to 400?",
     "a": "1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361 and 400. They are 1 × 1 up to 20 × 20."},
]


def gen():
    rnd = random.Random(48802)
    P = People(rnd)
    sets = [set_perfect(rnd, P), set_estimate(rnd, P), set_rational(rnd, P), set_order(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "square-roots-and-real-numbers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Square Roots and Real Numbers",
        "seo_title": "Grade 8 Square Roots and Real Numbers Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Square roots and real numbers",
        "domain": "Number",
        "standard_code": "Grade 8: B1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Estimate and calculate square roots, in various contexts",
        "meta_desc": "Free Grade 8 math worksheets on square roots and real numbers for the Ontario curriculum: perfect squares, estimating square roots, rational and irrational numbers, ordering numbers like √10, π and 3.2, and word problems. 100 questions with an answer key.",
        "key_big": "√50 is between 7 and 8, because 7² = 49 and 8² = 64. It is about 7.1, not 25.",
        "key_sub": "The square root of a whole number that is not a perfect square is irrational. π is irrational too: 3.14 is only close to it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
