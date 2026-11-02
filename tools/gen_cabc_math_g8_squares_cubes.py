# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Squares, Cubes and Roots (BC Mathematics Curriculum, Grade 8: Number,
“perfect squares and cubes; square and cube roots”)
  python3 tools/gen_cabc_math_g8_squares_cubes.py
Perfect squares, square roots of perfect squares and estimating square roots such as √50, perfect cubes, cube roots
(including a few negative cubes and estimates), and word problems in BC contexts (area of a square, volume of a cube).
Wrong answers come from real student mistakes: √36 = 18 (halving), 2³ = 6 (multiplying by 3), n² = 2n, ∛27 = 9
(dividing by 3), mixing up √ and ∛, counting only one face or only the visible cubes of a cube, using the surface area
for the volume, dividing an area by 4 (perimeter thinking), √20 ≈ 4.4 (20 − 16 = 4), truncating instead of rounding,
dropping zeros (40³ = 6400) and “a negative number has no cube root”.
Every answer is checked with math.isqrt, integer cube roots and fractions.Fraction. Helpers are adapted from
gen_caon_math_g8_square_roots.py and gen_caon_math_g7_squares.py; all wording is rewritten for BC.
Canadian English, real minus sign −, HTML attributes in single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import isqrt, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
LIGHT = "#e6f2ea"
TOPF = "#f3f9f5"
SIDEF = "#c9e3d2"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer, BC style: 4 digits with no separator, 5+ with a no-break space. Real minus sign."""
    assert isinstance(v, int), v
    a = abs(v)
    s = str(a) if a < 10000 else "{:,}".format(a).replace(",", NBSP)
    return (M if v < 0 else "") + s


def d(v):
    """int or terminating Fraction: shortest exact decimal, minus sign −."""
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


def r1s(v):
    """One decimal place as text, keeping a trailing .0."""
    s = d(v)
    return s if "." in s else s + ".0"


def approx(x, k=3):
    return (("%." + str(k) + "f") % x).replace("-", M)


def icbrt(N):
    """Integer cube root of a perfect cube (negative allowed)."""
    a = abs(N)
    r = round(a ** (1 / 3))
    for c in (r - 1, r, r + 1):
        if c ** 3 == a:
            return c if N >= 0 else -c
    raise AssertionError(N)


def cbrt_floor(N):
    r = int(round(N ** (1 / 3)))
    while r ** 3 > N:
        r -= 1
    while (r + 1) ** 3 <= N:
        r += 1
    return r


def is_cube(N):
    return cbrt_floor(N) ** 3 == N


def is_sq(N):
    return isqrt(N) ** 2 == N


def sup(k):
    return "<sup>%d</sup>" % k


def unit(v, u):
    return d(v) + NBSP + u


def area(v, u):
    return d(v) + NBSP + u + sup(2)


def vol(v, u):
    return d(v) + NBSP + u + sup(3)


def plural(k, w, pl=None):
    return "%d %s" % (k, w if k == 1 else (pl or w + "s"))


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, fixed=None):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped. fixed: answer index of a picture question whose
    choices must stay A, B, C, D."""
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
    """Numeric answer (int or Fraction); cands are values. All 4 must be different values."""
    assert len(cands) == 3 and len({F(v)} | {F(c) for c in cands}) == 4, (q, v, cands)
    return mcq(q, (fmt(v), F(v)), [(fmt(c), F(c)) for c in cands], e)


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
    w, h = int(math.ceil(w)), int(math.ceil(h))
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
    """Tag wide pictures (number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def array_svg(k, cell=13):
    """A k × k square array of tiles."""
    o = 4
    W = H = k * cell + 2 * o
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (o + c * cell, o + r * cell, cell, cell, LIGHT, GREEN) for r in range(k) for c in range(k)]
    return svg_wrap(W, H, "".join(s), "square array of %d rows of %d tiles" % (k, k))


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


def cube_body(x0, y0, k, c, sw=1.4):
    """Oblique drawing of a cube built from k × k × k small cubes, cell c. Returns (svg parts, S, depth)."""
    S = k * c
    dd = 0.5 * S
    yf = y0 + dd
    s = []
    poly = lambda pts, fill: s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
                                      % (" ".join("%.1f,%.1f" % p for p in pts), fill, GREEN))
    ln = lambda a, b: s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f'/>"
                               % (a[0], a[1], b[0], b[1], GREEN, sw))
    poly([(x0, yf), (x0 + S, yf), (x0 + S, yf + S), (x0, yf + S)], LIGHT)
    poly([(x0, yf), (x0 + S, yf), (x0 + S + dd, y0), (x0 + dd, y0)], TOPF)
    poly([(x0 + S, yf), (x0 + S + dd, y0), (x0 + S + dd, y0 + S), (x0 + S, yf + S)], SIDEF)
    for i in range(1, k):
        t = i * c
        ln((x0 + t, yf), (x0 + t, yf + S))                           # front verticals
        ln((x0, yf + t), (x0 + S, yf + t))                           # front horizontals
        ln((x0 + t, yf), (x0 + t + dd, y0))                          # top: depth lines
        f = i / k
        ln((x0 + f * dd, yf - f * dd), (x0 + S + f * dd, yf - f * dd))  # top: width lines
        ln((x0 + S, yf + t), (x0 + S + dd, y0 + t))                  # right: depth lines
        ln((x0 + S + f * dd, yf - f * dd), (x0 + S + f * dd, yf - f * dd + S))  # right: verticals
    return s, S, dd


def small_cubes_svg(k):
    o = 6
    s, S, dd = cube_body(o, o, k, 22 if k <= 3 else 18)
    return svg_wrap(S + dd + 2 * o, S + dd + 2 * o, "".join(s), "large cube built from small cubes, %d along each edge" % k)


def cube_edge_svg(edge, u):
    """One cube with its edge length written under the front face."""
    o = 6
    s, S, dd = cube_body(o, o, 1, 84)
    s.append(text(o + S / 2, o + dd + S + 20, "%s %s" % (edge, u), 15, bold=True))
    return svg_wrap(S + dd + 2 * o, S + dd + o + 28, "".join(s), "cube with edges of %s %s" % (edge, u))


def cube_volume_svg(v, u):
    """One cube with its volume written on the front face and “?” on the bottom edge."""
    o = 6
    s, S, dd = cube_body(o, o, 1, 92)
    s.append(text(o + S / 2, o + dd + S / 2 - 2, "Volume", 14))
    s.append(text(o + S / 2, o + dd + S / 2 + 18, "%s %s³" % (n(v), u), 15, bold=True))
    s.append(text(o + S / 2, o + dd + S + 21, "?", 16, bold=True, col=RED))
    return svg_wrap(S + dd + 2 * o, S + dd + o + 28, "".join(s),
                    "cube with a volume of %s cubic %s and an unknown edge length" % (n(v), {"cm": "centimetres", "m": "metres"}[u]))


def squares_row_svg():
    """Lesson: squares with areas 49, 50 and 64; sides 7, √50 and 8."""
    k = 12
    gap, o = 34, 8
    sides = [(49, "7"), (50, "√50"), (64, "8")]
    H = int(o + 8 * k + 30)
    s, x = [], o
    for a, lab in sides:
        L = sqrt(a) * k
        y0 = o + 8 * k - L
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y0, L, L, LIGHT if a != 50 else "#fdecea", GREEN if a != 50 else RED))
        s.append(text(x + L / 2, y0 + L / 2 + 5, "%d" % a, 15, bold=True))
        s.append(text(x + L / 2, o + 8 * k + 20, "side " + lab, 14, col=GREEN if a != 50 else RED, bold=(a == 50)))
        x += L + gap
    return svg_wrap(x - gap + o, H, "".join(s), "squares with areas 49, 50 and 64 and sides 7, √50 and 8")


class NL:
    """Number line from lo to hi with a labelled tick at every integer. Points: (value, name above, colour)."""

    def __init__(self, lo, hi, g=56):
        self.lo, self.hi, self.g = lo, hi, g
        self.pad = 26
        self.W = int(2 * self.pad + (hi - lo) * g)
        self.pts = []

    def X(self, v):
        return self.pad + (v - self.lo) * self.g

    def point(self, v, name, col=GREEN):
        assert self.lo <= v <= self.hi
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
        for v in range(self.lo, self.hi + 1):
            x = self.X(v)
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 7, x, Y + 7, INK))
            s.append(text(x, Y + 25, n(v), 14))
        for v, nm, col, row in rows:
            x = self.X(float(v))
            s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (x, Y, col))
            s.append(text(x, Y - 11 - 18 * row, nm, 15, bold=True, col=col))
        return svg_wrap(self.W, H, "".join(s), label)


# ============================================================ set 1: perfect squares
def set_squares(rnd, P):
    its = []
    # A: squaring (5)
    for k in [9, 11, 12, 13, 15]:
        e = "%d%s means %d × %d = <b>%d</b>. It is not %d × 2 = %d." % (k, sup(2), k, k, k * k, k, 2 * k)
        its.append(mcq_v("What is %d%s?" % (k, sup(2)), k * k, [2 * k, (k - 1) ** 2, (k + 1) ** 2], e))
    # B: square arrays (2)
    for k in [6, 8]:
        border = 4 * k - 4
        e = ("The array has %d rows of %d tiles: %d × %d = %d%s = <b>%d</b> tiles. "
             "%d is only the rows plus the columns, and %d is only the tiles around the border." % (k, k, k, k, k, sup(2), k * k, 2 * k, border))
        its.append(mcq_v(fig(array_svg(k)) + "Which perfect square does this square array show?", k * k, [2 * k, border, (k + 1) ** 2], e))
    # C: which is / is not a perfect square (6)
    C = [(144, [124, 164, 140]), (196, [186, 160, 206]), (225, [125, 250, 205]), (400, [40, 200, 4000])]
    for right, wrong in C:
        r = isqrt(right)
        assert r * r == right and not any(is_sq(w) for w in wrong)
        e = "%d × %d = %d, so <b>%d</b> is a perfect square. " % (r, r, right, right)
        if right == 225:
            e += "125 = 5 × 5 × 5 is a perfect <i>cube</i>, not a square."
        elif right == 400:
            e += "40 and 4000 are not squares: a perfect square ending in 0 needs an even number of zeros (100, 400, 2500)."
        else:
            e += "%d%s = %d and %d%s = %d, so the other numbers fall between perfect squares." % (r - 1, sup(2), (r - 1) ** 2, r + 1, sup(2), (r + 1) ** 2)
        its.append(mcq("Which number is a perfect square?", n(right), [n(w) for w in wrong], e))
    for right, others in [(50, [49, 64, 36]), (200, [100, 121, 169])]:
        assert not is_sq(right) and all(is_sq(x) for x in others)
        a = isqrt(right)
        e = ("%s. %d%s = %d and %d%s = %d, so <b>%d</b> is between two perfect squares and is not one itself."
             % (", ".join("%d = %d%s" % (x, isqrt(x), sup(2)) for x in others), a, sup(2), a * a, a + 1, sup(2), (a + 1) ** 2, right))
        its.append(mcq("Which number is <b>not</b> a perfect square?", n(right), [n(x) for x in others], e))
    # D: other forms (7)
    its.append(mcq("Which is the same as 7%s?" % sup(2), "7 × 7", ["7 × 2", "7 + 7", "2 × 2 × 2 × 2 × 2 × 2 × 2"],
                   "The small 2 tells how many 7s to multiply: 7%s = <b>7 × 7</b> = 49. 7 × 2 and 7 + 7 both give 14." % sup(2)))
    for k, wr in [(20, [40, 4000, 200]), (30, [60, 90, 9000])]:
        e = ("%d%s = %d × %d = <b>%s</b>. Think %d × %d = %d, then add two zeros, one for each %d. %d is %d × 2."
             % (k, sup(2), k, k, n(k * k), k // 10, k // 10, (k // 10) ** 2, k, 2 * k, k))
        its.append(mcq_v("What is %d%s?" % (k, sup(2)), k * k, wr, e))
    its.append(mcq_v("What is the next perfect square: 1, 4, 9, 16, 25, …?", 36, [30, 34, 49],
                     "These are 1%s, 2%s, 3%s, 4%s and 5%s. The next one is 6%s = <b>36</b>. The gaps are 3, 5, 7, 9, so the next gap is 11."
                     % ((sup(2),) * 6)))
    assert [x for x in range(51, 100) if is_sq(x)] == [64, 81]
    its.append(mcq_v("How many perfect squares are between 50 and 100?", 2, [3, 1, 5],
                     "7%s = 49 is too small and 10%s = 100 is not <i>between</i> 50 and 100. Only 8%s = 64 and 9%s = 81 fit: <b>2</b> perfect squares."
                     % ((sup(2),) * 4)))
    its.append(mcq_v("A square array has 7 rows of 7 tiles. How many tiles must be added to make the next square array, 8 rows of 8 tiles?",
                     15, [1, 8, 64],
                     "8%s − 7%s = 64 − 49 = <b>15</b> tiles: one new row of 8 and one new column of 7. Adding only one row (8) leaves a rectangle."
                     % (sup(2), sup(2))))
    assert abs(90 - 81) < abs(100 - 90)
    its.append(mcq_v("Which perfect square is closest to 90?", 81, [100, 64, 45],
                     "9%s = 81 and 10%s = 100. 90 − 81 = 9 and 100 − 90 = 10, so <b>81</b> is closer, but only by 1." % (sup(2), sup(2))))
    assert len(its) == 20
    return {"title": "Perfect squares", "items": its}


# ============================================================ set 2: square roots
def set_sqrt(rnd, P):
    its = []
    # A: square roots of perfect squares (8)
    for N in [36, 64, 81, 121, 144, 169, 225, 400]:
        r = isqrt(N)
        assert r * r == N
        if N % 2 == 0:
            e = "%d × %d = %d, so √%d = <b>%d</b>. Do not halve: %d ÷ 2 = %d, and %d × %d = %s, not %d." % (
                r, r, N, N, r, N, N // 2, N // 2, N // 2, n((N // 2) ** 2), N)
            wr = [N // 2, r + 1, r - 1]
        else:
            e = "%d × %d = %d, so √%d = <b>%d</b>. Check by squaring: %d%s = %d." % (r, r, N, N, r, r, sup(2), N)
            wr = [F(N, 2), r + 1, r - 1]
        its.append(mcq_v("What is √%d?" % N, r, wr, e))
    # B: between which two whole numbers (5)
    for N in [50, 20, 30, 70, 110]:
        a = isqrt(N)
        assert a * a < N < (a + 1) ** 2
        h = N // 2
        e = ("Find the perfect squares on each side: %d%s = %d and %d%s = %d. %d is between them, so √%d is between "
             "<b>%d and %d</b> (√%d ≈ %s)." % (a, sup(2), a * a, a + 1, sup(2), (a + 1) ** 2, N, N, a, a + 1, N, approx(sqrt(N), 2)))
        its.append(mcq("√%d is between which two whole numbers?" % N, "%d and %d" % (a, a + 1),
                       ["%d and %d" % (h, h + 1), "%d and %d" % (a - 1, a), "%d and %d" % (a + 1, a + 2)], e))
    # C: number line with points A–D (3); choices stay A, B, C, D
    plans = [(50, 5, 9, [F(5), F(61, 10), F(71, 10), F(85, 10)]),
             (10, 0, 6, [F(1), F(32, 10), F(38, 10), F(5)]),
             (80, 5, 10, [F(64, 10), F(8), F(85, 10), F(89, 10)])]
    for N, lo, hi, pts in plans:
        a = isqrt(N)
        right = min(range(4), key=lambda i: abs(float(pts[i]) - sqrt(N)))
        assert abs(float(pts[right]) - sqrt(N)) < 0.06 and sorted(pts) == pts
        nl = NL(lo, hi)
        for i, v in enumerate(pts):
            nl.point(v, "ABCD"[i])
        svg = nl.svg("number line from %d to %d with points A, B, C and D" % (lo, hi))
        near = a if sqrt(N) - a < 0.5 else a + 1
        e = ("%d%s = %d and %d%s = %d, so √%d is between %d and %d. %d is closer to %d, so √%d is closer to %d. "
             "√%d ≈ %s, so the answer is <b>point %s</b>." % (a, sup(2), a * a, a + 1, sup(2), (a + 1) ** 2, N, a, a + 1, N,
                                                             near * near, N, near, N, approx(sqrt(N), 2), "ABCD"[right]))
        its.append(mcq(fig(svg) + "Which point is closest to √%d on the number line?" % N, None, ["A", "B", "C", "D"], e, fixed=right))
    # D: to one decimal place (3)
    big = lambda x: d(x) if x >= 10 else r1s(x)
    for N, wrong, note in [(50, [F(25), F(75, 10), F(7)], "Halving gives 25, but 25%s = 625." % sup(2)),
                           (20, [F(10), F(44, 10), F(4)], "4.4 comes from 20 − 16 = 4. That is not how roots work: 4.4%s = 19.36 and 4.5%s = 20.25." % (sup(2), sup(2))),
                           (90, [F(45), F(99, 10), F(94, 10)], "9.4 cuts off the digits instead of rounding: 9.48… rounds up to 9.5.")]:
        a = isqrt(N)
        v = r1(sqrt(N))
        assert v not in wrong and (v - F(1, 20)) ** 2 < N < (v + F(1, 20)) ** 2
        e = ("%d%s = %d and %d%s = %d, so √%d is between %d and %d. √%d ≈ %s, so to one decimal place √%d ≈ <b>%s</b>. "
             % (a, sup(2), a * a, a + 1, sup(2), (a + 1) ** 2, N, a, a + 1, N, approx(sqrt(N), 3), N, r1s(v)) + note)
        its.append(mcq_v("Estimate √%d to one decimal place." % N, v, wrong, e, fmt=big))
    # E: √a + √b (1)
    its.append(mcq_v("What is √36 + √64?", 14, [10, 100, 50],
                     "Find each root first: √36 = 6 and √64 = 8, so √36 + √64 = 6 + 8 = <b>14</b>. "
                     "You cannot add under the root sign: √(36 + 64) = √100 = 10 is a different number."))
    assert len(its) == 20
    return {"title": "Square roots and estimating", "items": its}


# ============================================================ set 3: perfect cubes
def set_cubes(rnd, P):
    its = []
    # A: cubing (6)
    for k in [2, 3, 4, 5, 6, 10]:
        e = "%d%s means %d × %d × %d = <b>%s</b>. It is not %d × 3 = %d." % (k, sup(3), k, k, k, n(k ** 3), k, 3 * k)
        wr = [3 * k, k * k, (k + 1) ** 3] if k != 3 else [9, 18, 64]
        its.append(mcq_v("What is %d%s?" % (k, sup(3)), k ** 3, wr, e))
    # B: large cube of small cubes (2)
    for k in [3, 4]:
        vis = k ** 3 - (k - 1) ** 3
        e = ("There are %d layers, and each layer has %d × %d = %d small cubes. %d × %d = %d%s = <b>%d</b>. "
             "%d counts only one face, and %d counts only the cubes you can see." % (k, k, k, k * k, k, k * k, k, sup(3), k ** 3, k * k, vis))
        its.append(mcq_v(fig(small_cubes_svg(k)) + "This large cube is built from small cubes. How many small cubes are in it?",
                         k ** 3, [k * k, vis, 6 * k * k], e))
    # C: which is / is not a perfect cube (5)
    C = [(125, [25, 75, 150]), (216, [36, 18, 100]), (1000, [100, 300, 30]), (343, [49, 21, 147])]
    for right, wrong in C:
        r = icbrt(right)
        assert not any(is_cube(w) for w in wrong)
        e = "%d × %d × %d = %s, so <b>%s</b> is a perfect cube. " % (r, r, r, n(right), n(right))
        why = []
        for w in wrong:
            if is_sq(w):
                why.append("%d = %d%s is a square, not a cube" % (w, isqrt(w), sup(2)))
            else:
                a = cbrt_floor(w)
                why.append("%d is between %d%s = %d and %d%s = %d" % (w, a, sup(3), a ** 3, a + 1, sup(3), (a + 1) ** 3))
        e += "; ".join(why) + "." 
        its.append(mcq("Which number is a perfect cube?", n(right), [n(w) for w in wrong], e))
    assert not is_cube(9) and all(is_cube(x) for x in (1, 8, 27))
    its.append(mcq("Which number is <b>not</b> a perfect cube?", "9", ["1", "8", "27"],
                   "1 = 1%s, 8 = 2%s and 27 = 3%s. <b>9</b> = 3%s is a perfect square, but 2%s = 8 and 3%s = 27, so 9 is not a cube."
                   % (sup(3), sup(3), sup(3), sup(2), sup(3), sup(3))))
    # D: others (7)
    assert is_sq(64) and is_cube(64) and not is_cube(16) and not is_sq(8) and not is_sq(27)
    its.append(mcq("Which number is both a perfect square and a perfect cube?", "64", ["16", "8", "27"],
                   "64 = 8 × 8 and 64 = 4 × 4 × 4, so <b>64</b> is both. 16 is only a square, and 8 and 27 are only cubes."))
    its.append(mcq("Which is the same as 4%s?" % sup(3), "4 × 4 × 4", ["4 × 3", "4 + 4 + 4", "3 × 3 × 3 × 3"],
                   "The small 3 tells how many 4s to multiply: 4%s = <b>4 × 4 × 4</b> = 64. 4 × 3 and 4 + 4 + 4 both give 12." % sup(3)))
    its.append(mcq(fig(cube_edge_svg(7, "cm")) + "What is the volume of this cube?", vol(343, "cm"),
                   [vol(49, "cm"), vol(21, "cm"), vol(294, "cm")],
                   "Volume of a cube = edge × edge × edge = 7 × 7 × 7 = <b>343" + NBSP + "cm" + sup(3) + "</b>. "
                   "49 is the area of one face, and 294 = 6 × 49 is the surface area."))
    its.append(mcq_v("What is the next perfect cube: 1, 8, 27, 64, …?", 125, [81, 100, 91],
                     "These are 1%s, 2%s, 3%s and 4%s. The next one is 5%s = <b>125</b>. 81 and 100 are perfect squares, not cubes."
                     % ((sup(3),) * 5)))
    its.append(mcq_v("What is 20%s?" % sup(3), 8000, [60, 800, 400],
                     "20%s = 20 × 20 × 20 = <b>8000</b>. Think 2%s = 8, then add three zeros (one for each 20)." % (sup(3), sup(3))))
    its.append(mcq("Which is greater: 2%s or 3%s?" % (sup(3), sup(2)), "3" + sup(2), ["2" + sup(3), "They are equal", "You cannot tell"],
                   "2%s = 2 × 2 × 2 = 8 and 3%s = 3 × 3 = 9. 9 &gt; 8, so <b>3%s</b> is greater." % (sup(3), sup(2), sup(2))))
    assert (-3) ** 3 == -27
    its.append(mcq_v("What is (%s3)%s?" % (M, sup(3)), -27, [27, -9, 9],
                     "(%s3) × (%s3) × (%s3): the first two give +9, then 9 × (%s3) = <b>%s27</b>. "
                     "Three negative factors give a negative answer." % (M, M, M, M, M)))
    assert len(its) == 20
    return {"title": "Perfect cubes", "items": its}


# ============================================================ set 4: cube roots
def set_cbrt(rnd, P):
    its = []
    # A: cube roots of perfect cubes (7)
    A = [(27, [9, 4, 2], "Dividing by 3 gives 9, but 9 × 9 × 9 = 729."),
         (64, [8, 32, 5], "8 is √64, the <i>square</i> root: 8 × 8 = 64, but 8 × 8 × 8 = 512."),
         (125, [25, 15, 6], "25 comes from 5 × 25 = 125, which uses only two factors."),
         (216, [72, 36, 7], "Dividing by 3 gives 72, but a cube root is not 216 ÷ 3."),
         (512, [256, 64, 9], "64 is 8%s, not the cube root." % sup(2)),
         (729, [243, 27, 8], "27 is √729, the <i>square</i> root: 27 × 27 = 729."),
         (1000, [100, 500, 9], "100 × 100 × 100 = 1" + NBSP + "000" + NBSP + "000, so 100 is too big.")]
    for N, wr, note in A:
        r = icbrt(N)
        assert r not in wr
        e = "%d × %d × %d = %d, so ∛%d = <b>%d</b>. %s" % (r, r, r, N, N, r, note)
        its.append(mcq_v("What is ∛%d?" % N, r, wr, e))
    # B: square root or cube root (2)
    its.append(mcq("Which statement is true?", "√64 = 8 and ∛64 = 4",
                   ["√64 = 4 and ∛64 = 8", "√64 = 32 and ∛64 = 21", "√64 and ∛64 are both 8"],
                   "8 × 8 = 64, so <b>√64 = 8</b>. 4 × 4 × 4 = 64, so <b>∛64 = 4</b>. A cube root uses three equal factors, so it is smaller here."))
    its.append(mcq_v("What is ∛27 + ∛216?", 9, [81, 243, 18],
                     "Find each root first: ∛27 = 3 and ∛216 = 6, so 3 + 6 = <b>9</b>. "
                     "243 adds the numbers under the roots, 81 divides each by 3 (9 + 72), and 18 multiplies 3 × 6."))
    # C: between which two whole numbers (5)
    for N in [50, 80, 20, 300, 600]:
        a = cbrt_floor(N)
        assert a ** 3 < N < (a + 1) ** 3
        s = isqrt(N)
        wrong = ["%d and %d" % (s, s + 1), "%d and %d" % (a - 1, a), "%d and %d" % (a + 1, a + 2)]
        e = ("Find the perfect cubes on each side: %d%s = %d and %d%s = %d. %d is between them, so ∛%d is between "
             "<b>%d and %d</b> (∛%d ≈ %s). %d and %d would be for √%d." % (a, sup(3), a ** 3, a + 1, sup(3), (a + 1) ** 3, N, N, a, a + 1,
                                                                        N, approx(N ** (1 / 3), 2), s, s + 1, N))
        assert s != a
        its.append(mcq("∛%d is between which two whole numbers?" % N, "%d and %d" % (a, a + 1), wrong, e))
    # D: negative cube roots (2)
    its.append(mcq("What is ∛(%s8)?" % M, M + "2", ["2", M + "4", "It has no cube root"],
                   "(%s2) × (%s2) × (%s2) = 4 × (%s2) = %s8, so ∛(%s8) = <b>%s2</b>. A negative number has a cube root, "
                   "because three negative factors give a negative product." % (M, M, M, M, M, M, M)))
    its.append(mcq_v("What is ∛(%s64)?" % M, -4, [4, -8, -32],
                     "(%s4) × (%s4) × (%s4) = 16 × (%s4) = %s64, so ∛(%s64) = <b>%s4</b>. %s8 comes from √64 = 8, the square root, "
                     "and %s32 is %s64 ÷ 2." % (M, M, M, M, M, M, M, M, M, M)))
    # E: cube with a given volume (1)
    its.append(mcq_v(fig(cube_volume_svg(216, "cm")) + "The volume of this cube is %s. How long is each edge?" % vol(216, "cm"),
                     6, [72, 36, 7],
                     "Edge × edge × edge = 216. 6 × 6 × 6 = 216, so each edge is ∛216 = <b>6" + NBSP + "cm</b>. "
                     "216 ÷ 6 = 36 shares the volume among the 6 faces, which does not give an edge.",
                     fmt=lambda v: unit(v, "cm")))
    # F: statements (2)
    its.append(mcq("Which statement is true?", "∛125 = 5, because 5 × 5 × 5 = 125",
                   ["∛125 = 25, because 5 × 25 = 125", "∛125 = 41, because 125 ÷ 3 ≈ 41",
                    "∛125 = 11, because 11 × 11 = 121"],
                   "A cube root is the number used <b>three</b> times as a factor. 5 × 5 × 5 = 125, so <b>∛125 = 5</b>."))
    assert is_cube(343) and not any(is_cube(x) for x in (300, 400, 81))
    its.append(mcq("Which number has a whole-number cube root?", "343", ["300", "400", "81"],
                   "7 × 7 × 7 = 343, so ∛343 = 7 and <b>343</b> is a perfect cube. 400 and 81 are perfect squares, not cubes, "
                   "and 300 is between 6%s = 216 and 7%s = 343." % (sup(3), sup(3))))
    # G: closest whole number (1)
    assert abs(30 - 27) < abs(64 - 30)
    its.append(mcq_v("Which whole number is ∛30 closest to?", 3, [10, 4, 5],
                     "3%s = 27 and 4%s = 64. 30 is much closer to 27, so ∛30 is closest to <b>3</b> (∛30 ≈ %s). "
                     "10 is 30 ÷ 3, and 5 is close to √30, the square root." % (sup(3), sup(3), approx(30 ** (1 / 3), 2))))
    assert len(its) == 20
    return {"title": "Cube roots", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    m_ = lambda v: unit(v, "m")
    cm_ = lambda v: unit(v, "cm")

    def mq(q, v, cands, e, fmt=d):
        its.append(mcq_v(q, v, cands, e, fmt=fmt))

    # 1 garden plot
    mq("A square plot in a Surrey community garden has an area of %s. How long is each side?" % area(64, "m"),
       8, [32, 16, 4096], "Side × side = 64. 8 × 8 = 64, so each side is √64 = <b>8" + NBSP + "m</b>. "
       "16 = 64 ÷ 4 would come from a perimeter, not an area.", fmt=m_)
    # 2 cabin floor to nearest tenth
    v = r1(sqrt(30))
    assert v == F(55, 10)
    mq("The floor of a square room in a Whistler cabin has an area of %s. How long is each side, to the nearest tenth of a metre?" % area(30, "m"),
       v, [15, F(75, 10), F(54, 10)], "√30 ≈ %s. The hundredths digit is 7, so round up: <b>5.5" % approx(sqrt(30)) + NBSP + "m</b>. "
       "Check: 5.5%s = 30.25, which is close to 30." % sup(2), fmt=lambda x: (d(x) if x >= 10 else r1s(x)) + NBSP + "m")
    # 3 poster
    mq("A square poster for the Terry Fox Run has an area of %s. How long is each side?" % area(3600, "cm"),
       60, [1800, 900, 6], "60 × 60 = 3600, so each side is √3600 = <b>60" + NBSP + "cm</b>. (6 × 6 = 36, not 3600.)", fmt=cm_)
    # 4 assembly chairs
    assert isqrt(169) == 13
    mq("For a school assembly in Burnaby, 169 chairs are set out in a square: the number of rows equals the number of chairs in each row. "
       "How many rows are there?", 13, [84, 42, 12], "Rows × chairs per row = 169, and they are equal. 13 × 13 = 169, so there are <b>13 rows</b>. "
       "Halving (84) or dividing by 4 (42) does not give a square root.", fmt=lambda x: plural(int(x), "row"))
    # 5 fence around paddock
    mq("A square horse paddock in the Okanagan has an area of %s. How much fencing goes all the way around it?" % area(900, "m"),
       120, [30, 225, 3600], "Each side is √900 = 30" + NBSP + "m. A square has 4 equal sides: 4 × 30 = <b>120" + NBSP + "m</b>. "
       "30" + NBSP + "m is only one side.", fmt=m_)
    # 6 sandbox border
    nm, he, his = P.next()
    assert 4 * sqrt(5) < 9
    its.append(mcq("%s builds a square sandbox with an area of %s. %s has 9" % (nm, area(5, "m"), he.capitalize()) + NBSP +
                   "m of cedar boards for the border. Is that enough?",
                   "Yes. %s needs about 8.9" % he.capitalize() + NBSP + "m.",
                   ["No. %s needs 20" % he.capitalize() + NBSP + "m.", "No. %s needs 10" % he.capitalize() + NBSP + "m.",
                    "Yes. %s needs 5" % he.capitalize() + NBSP + "m."],
                   "Each side is √5 ≈ 2.236" + NBSP + "m. The border is 4 × 2.236 ≈ 8.94" + NBSP + "m, which is less than 9" + NBSP +
                   "m. <b>Yes</b>, it is enough. (4 × 5 = 20 uses the area as the side.)"))
    # 7 cube box 1000 cm³
    mq("A cube-shaped box holds exactly 1 litre, which is %s. How long is each edge of the box?" % vol(1000, "cm"),
       10, [100, 500, F(316, 10)], "10 × 10 × 10 = 1000, so each edge is ∛1000 = <b>10" + NBSP + "cm</b>. "
       "31.6 is √1000, the square root, and 100 × 100 × 100 is far too big.", fmt=cm_)
    # 8 storage box 40 cm
    assert 40 ** 3 == 64000
    mq("A cube-shaped storage box for hockey gear has edges of 40" + NBSP + "cm. What is its volume?", 64000, [120, 1600, 6400],
       "40 × 40 × 40 = <b>64" + NBSP + "000" + NBSP + "cm" + sup(3) + "</b>. Think 4 × 4 × 4 = 64, then add three zeros. "
       "1600 is the area of one face.", fmt=lambda x: vol(x, "cm"))
    # 9 hatchery tank
    mq("A salmon hatchery near the Fraser River has a cube-shaped tank with edges of 2" + NBSP + "m. What is its volume?", 8, [6, 4, 24],
       "2 × 2 × 2 = <b>8" + NBSP + "m" + sup(3) + "</b>. 2 × 3 = 6 is a common mistake, and 24 = 6 × 4 is the surface area.",
       fmt=lambda x: vol(x, "m"))
    # 10 ice cube
    nm, he, his = P.next()
    mq("%s makes ice cubes that are 3" % nm + NBSP + "cm on each edge. What is the volume of one ice cube?", 27, [9, 54, 36],
       "3 × 3 × 3 = <b>27" + NBSP + "cm" + sup(3) + "</b>. 9 is the area of one face, 54 = 6 × 9 is the surface area, "
       "and 36 = 12 × 3 is the total length of the 12 edges.", fmt=lambda x: vol(x, "cm"))
    # 11 puzzle cube
    nm, he, his = P.next()
    mq("%s builds a large cube from small wooden cubes, with 5 small cubes along each edge. How many small cubes does %s use?" % (nm, he),
       125, [15, 25, 150], "5 layers of 5 × 5 = 25 cubes: 5 × 5 × 5 = <b>125 small cubes</b>. 25 is only one layer.",
       fmt=lambda x: n(int(x)) + " cubes")
    # 12 planter 125 000 cm³
    assert icbrt(125000) == 50
    mq("A cube-shaped wooden planter has a volume of %s. How long is each edge?" % vol(125000, "cm"), 50, [500, 5, 25],
       "50 × 50 × 50 = 125" + NBSP + "000, so each edge is <b>50" + NBSP + "cm</b>. ∛125 = 5, and each 0 in 50 gives three zeros "
       "in the volume. 500 × 500 × 500 = 125" + NBSP + "000" + NBSP + "000 is far too big.", fmt=cm_)
    # 13 doubling edge of a cube
    nm, he, his = P.next()
    assert 4 ** 3 // 2 ** 3 == 8
    mq("Cube A has edges of 2" + NBSP + "cm. Cube B has edges of 4" + NBSP + "cm. How many times greater is the volume of cube B?",
       8, [2, 4, 6], "Cube A: 2 × 2 × 2 = 8" + NBSP + "cm" + sup(3) + ". Cube B: 4 × 4 × 4 = 64" + NBSP + "cm" + sup(3) +
       ". 64 ÷ 8 = <b>8 times</b>. Doubling the edge doubles each of the 3 factors: 2 × 2 × 2 = 8.",
       fmt=lambda x: "%d times" % x)
    # 14 floor tiles
    mq("A square bathroom floor has an area of %s. It is covered with square tiles that are 0.5" % area(16, "m") + NBSP +
       "m on each side. How many tiles are in each row?", 8, [32, 4, 64],
       "Each side of the floor is √16 = 4" + NBSP + "m. 4 ÷ 0.5 = <b>8 tiles</b> in each row (and 64 tiles in all).",
       fmt=lambda x: plural(int(x), "tile"))
    # 15 orchard
    assert isqrt(256) == 16
    mq("An orchard in Kelowna plants 256 apple trees in a square: the number of rows equals the number of trees in each row. "
       "How many trees are in each row?", 16, [128, 64, 15],
       "16 × 16 = 256, so there are <b>16 trees</b> in each row. 128 = 256 ÷ 2 and 64 = 256 ÷ 4 are not square roots.",
       fmt=lambda x: plural(int(x), "tree"))
    # 16 doubling side of a square
    nm, he, his = P.next()
    mq("%s has a square garden bed with sides of 3" % nm + NBSP + "m. %s makes a new square bed with sides of 6" % he.capitalize() + NBSP +
       "m. How many times greater is the area of the new bed?", 4, [2, 8, 3],
       "Old bed: 3 × 3 = 9" + NBSP + "m" + sup(2) + ". New bed: 6 × 6 = 36" + NBSP + "m" + sup(2) + ". 36 ÷ 9 = <b>4 times</b>. "
       "Doubling the side doubles both factors: 2 × 2 = 4.", fmt=lambda x: "%d times" % x)
    # 17 rain cistern
    mq("A cube-shaped tank on Vancouver Island collects rainwater. Its volume is %s. How long is each edge?" % vol(8, "m"),
       2, [4, F(28, 10), 512], "2 × 2 × 2 = 8, so each edge is ∛8 = <b>2" + NBSP + "m</b>. 4 is 8 ÷ 2, and 2.8 is close to √8, the square root.",
       fmt=m_)
    # 18 snow block
    assert 30 ** 3 == 27000
    mq("A block of packed snow for a snow fort is a cube with edges of 30" + NBSP + "cm. What is its volume?", 27000, [90, 900, 2700],
       "30 × 30 × 30 = <b>27" + NBSP + "000" + NBSP + "cm" + sup(3) + "</b>. Think 3 × 3 × 3 = 27, then add three zeros. "
       "900 is the area of one face.", fmt=lambda x: vol(x, "cm"))
    # 19 estimate a cube edge
    assert 4 ** 3 < 90 < 5 ** 3 and 9 ** 2 < 90 < 10 ** 2
    its.append(mcq("A cube-shaped gift box has a volume of %s. Each edge is between which two lengths?" % vol(90, "cm"),
                   "4" + NBSP + "cm and 5" + NBSP + "cm",
                   ["9" + NBSP + "cm and 10" + NBSP + "cm", "30" + NBSP + "cm and 31" + NBSP + "cm", "3" + NBSP + "cm and 4" + NBSP + "cm"],
                   "4%s = 64 and 5%s = 125. 90 is between them, so each edge is between <b>4" % (sup(3), sup(3)) + NBSP + "cm and 5" + NBSP +
                   "cm</b> (∛90 ≈ %s" % approx(90 ** (1 / 3), 2) + NBSP + "cm). 9 and 10 would be for √90, the square root, and 30 is 90 ÷ 3."))
    # 20 claim 2³ = 6
    nm, he, his = P.next()
    its.append(mcq("%s says a cube with edges of 2" % nm + NBSP + "cm has a volume of 6" + NBSP + "cm" + sup(3) + ". Which statement is correct?",
                   "%s is wrong. The volume is 8" % nm + NBSP + "cm" + sup(3) + ".",
                   ["%s is right, because 2 × 3 = 6." % nm, "%s is wrong. The volume is 4" % nm + NBSP + "cm" + sup(3) + ".",
                    "%s is wrong. The volume is 24" % nm + NBSP + "cm" + sup(3) + "."],
                   "2%s means 2 × 2 × 2, not 2 × 3. The volume is <b>8" % sup(3) + NBSP + "cm" + sup(3) + "</b>. "
                   "4 is the area of one face and 24 is the surface area."))
    assert len(its) == 20
    return {"title": "Word problems: area of a square and volume of a cube", "items": its}


# ============================================================ lesson
def body_html():
    f_sq = squares_row_svg()
    f_cube = small_cubes_svg(3)
    return (
        "<h2>Perfect squares and square roots</h2>"
        "<p>A <b>perfect square</b> is a whole number times itself. 7 × 7 = 49, so 49 is a perfect square. "
        "We write 7" + sup(2) + " = 49 and say “7 squared”. It is the area of a square with sides of 7.</p>"
        "<p>The <b>square root</b> undoes squaring. √49 = 7, because 7" + sup(2) + " = 49.</p>" +
        table(["n", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
              [["n" + sup(2), "36", "49", "64", "81", "100", "121", "144", "169", "196", "225"]]) +
        "<h2>Estimating a square root</h2>"
        "<p>When a number is not a perfect square, find the perfect squares on each side of it. Its root is between their roots.</p>"
        "<figure class='sn-fig'>" + f_sq +
        "<figcaption>49 &lt; 50 &lt; 64, so 7 &lt; √50 &lt; 8. 50 is very close to 49, so √50 ≈ 7.1.</figcaption></figure>" +
        ex("Example 1", "Estimate √30 to one decimal place.",
           "5" + sup(2) + " = 25 and 6" + sup(2) + " = 36, so √30 is between 5 and 6, a little closer to 5. "
           "Try 5.4" + sup(2) + " = 29.16 and 5.5" + sup(2) + " = 30.25. 30 is closer to 30.25.", "√30 ≈ 5.5") +
        "<h2>Perfect cubes and cube roots</h2>"
        "<p>A <b>perfect cube</b> is a whole number used as a factor three times. 3 × 3 × 3 = 27, so 27 is a perfect cube. "
        "We write 3" + sup(3) + " = 27 and say “3 cubed”. It is the volume of a cube with edges of 3.</p>"
        "<figure class='sn-fig'>" + f_cube +
        "<figcaption>3 layers of 3 × 3 = 9 small cubes: 3" + sup(3) + " = 27.</figcaption></figure>"
        "<p>The <b>cube root</b> undoes cubing. ∛27 = 3, because 3" + sup(3) + " = 27.</p>" +
        table(["n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
              [["n" + sup(3), "1", "8", "27", "64", "125", "216", "343", "512", "729", "1000"]]) +
        ex("Example 2", "A cube-shaped box has a volume of 64" + NBSP + "cm" + sup(3) + ". How long is each edge?",
           "Edge × edge × edge = 64. 4 × 4 × 4 = 64, so the edge is ∛64.", "4" + NBSP + "cm") +
        ex("Example 3", "What is (" + M + "2)" + sup(3) + "?",
           "(" + M + "2) × (" + M + "2) = 4, then 4 × (" + M + "2) = " + M + "8. Three negative factors give a negative answer. "
           "So ∛(" + M + "8) = " + M + "2.", M + "8") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["√36 = 18", "Do not halve. 6 × 6 = 36, so √36 = 6"],
            ["2" + sup(3) + " = 6", "The 3 means three factors: 2 × 2 × 2 = 8"],
            ["9" + sup(2) + " = 18", "9" + sup(2) + " = 9 × 9 = 81"],
            ["∛27 = 9", "Do not divide by 3. 3 × 3 × 3 = 27, so ∛27 = 3"],
            ["√64 = 4", "That is ∛64. √64 = 8, because 8 × 8 = 64"],
            ["√50 ≈ 25", "7" + sup(2) + " = 49, so √50 ≈ 7.1"],
        ])
    )


FAQ = [
    {"q": "What is the difference between a square root and a cube root?",
     "a": "A square root uses two equal factors and a cube root uses three. √64 = 8 because 8 × 8 = 64, and ∛64 = 4 because 4 × 4 × 4 = 64."},
    {"q": "How do you estimate √50 without a calculator?",
     "a": "Find the perfect squares on each side: 7 × 7 = 49 and 8 × 8 = 64. So √50 is between 7 and 8 and very close to 7, about 7.1."},
    {"q": "What do Grade 8 students learn about squares and cubes in BC?",
     "a": "In the BC Grade 8 curriculum (Number), students work with perfect squares and cubes and with square and cube roots, and use them to find the side of a square or the edge of a cube."},
    {"q": "What are the perfect cubes from 1 to 1000?",
     "a": "1, 8, 27, 64, 125, 216, 343, 512, 729 and 1000. They are 1 × 1 × 1 up to 10 × 10 × 10."},
]


def gen():
    rnd = random.Random(58801)
    P = People(rnd)
    sets = [set_squares(rnd, P), set_sqrt(rnd, P), set_cubes(rnd, P), set_cbrt(rnd, P), set_words(rnd, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "squares-cubes-and-roots", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Squares, Cubes and Roots: Perfect Squares, Perfect Cubes, Square Roots and Cube Roots",
        "seo_title": "Grade 8 Math: Squares, Cubes, Square Roots and Cube Roots Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Squares, cubes and roots",
        "domain": "Number",
        "standard_code": "Grade 8: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Perfect squares and cubes; square and cube roots",
        "meta_desc": "Free Grade 8 math worksheets on squares, cubes and roots for the BC curriculum: perfect squares, square roots and estimating roots like √50, perfect cubes, cube roots, and word problems on the area of a square and the volume of a cube. 100 questions with an answer key.",
        "key_big": "A square root uses two equal factors; a cube root uses three. √36 = 6 (not 18) and 2³ = 8 (not 6).",
        "key_sub": "To estimate a square root, find the perfect squares on each side: 49 < 50 < 64, so √50 is between 7 and 8, about 7.1. The side of a square is the square root of its area; the edge of a cube is the cube root of its volume.",
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
