# -*- coding: utf-8 -*-
"""
British Columbia Grade 8 Math: Linear relations
(BC Mathematics Curriculum, Grade 8: Patterning — discrete linear relations, extended to larger numbers,
limited to integers)
  python3 tools/gen_cabc_math_g8_linear_relations.py
Tables of values (with negative x), equations from tables (y = 3x − 2), graphing relations with integers in
all four quadrants, interpreting graphs, and word problems in BC contexts (snowshoe rental, Whistler
temperature, a diver in Howe Sound, the Terry Fox Run, kayak rentals in Victoria, a rain barrel in Nanaimo).
Every rate, initial value and coordinate is an integer.
Wrong answers come from real mistakes: plotting (y, x), the wrong sign of the rate (a shrinking relation
given a positive rate), the value at x = 1 used as the initial value, the change in y used without dividing
by the change in x, swapping the rate and the initial value, adding before multiplying, reading 3x as 35,
dropping a minus sign, and off-by-one steps.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d6cd"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NB = " "
X = "<i>x</i>"
Y = "<i>y</i>"


# ------------------------------------------------------------ numbers
def n(v):
    """BC/SI style: 4536, 12 000 (no-break space), real minus sign. Integers only in this unit."""
    v = Fr(v)
    assert v.denominator == 1, v
    neg = v < 0
    s = str(abs(v.numerator))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return (MINUS if neg else "") + s


def dol(v):
    v = Fr(v)
    assert v.denominator == 1 and v >= 0
    return "$" + n(v)


def units(u):
    return lambda v: "%s%s%s" % (n(v), NB if u.startswith("°") else " ", u)


def plain(s):
    return re.sub(r"<[^>]+>", "", s).replace(NB, " ")


def pt(a, b):
    return "(%s, %s)" % (n(a), n(b))


def I(v):
    return "<i>%s</i>" % v


# ------------------------------------------------------------ equations y = ax + b
def rhs(a, b, x="x"):
    a, b = Fr(a), Fr(b)
    if a == 0:
        return n(b)
    if a == 1:
        s = I(x)
    elif a == -1:
        s = MINUS + I(x)
    else:
        s = n(a) + I(x)
    if b > 0:
        s += " + " + n(b)
    elif b < 0:
        s += " " + MINUS + " " + n(-b)
    return s


def eq(a, b, x="x", y="y"):
    return I(y) + " = " + rhs(a, b, x)


def lv(a, b, x):
    return Fr(a) * Fr(x) + Fr(b)


def slope(xs, ys):
    r = {(Fr(ys[i + 1]) - Fr(ys[i])) / (Fr(xs[i + 1]) - Fr(xs[i])) for i in range(len(xs) - 1)}
    assert len(r) == 1, (xs, ys)
    return r.pop()


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e):
    seen = {plain(correct)}
    pick = []
    for c in cands:
        if not c or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order (A, B, C, D)."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


def nmcq(q, ans, cands, e, fmt=n):
    """Numeric choices: no two equal in value."""
    ans = Fr(ans)
    vals, pick = {ans}, []
    for c in cands:
        c = Fr(c)
        if c in vals:
            continue
        vals.add(c)
        pick.append(fmt(c))
    assert len(pick) == 3, (q, ans, cands)
    return mcq(q, fmt(ans), pick, e)


def eqmcq(q, right, wrong, e, xs, ys, x="x", y="y"):
    """Equation choices (a, b) for y = ax + b. right fits every pair; each wrong misses at least one."""
    for k, v in zip(xs, ys):
        assert lv(right[0], right[1], k) == Fr(v), (right, k, v)
    seen = {(Fr(right[0]), Fr(right[1]))}
    for w in wrong:
        assert any(lv(w[0], w[1], k) != Fr(v) for k, v in zip(xs, ys)), (w, xs, ys)
        key = (Fr(w[0]), Fr(w[1]))
        assert key not in seen, w
        seen.add(key)
    assert len(wrong) == 3
    return mcq(q, eq(right[0], right[1], x, y), [eq(a, b, x, y) for a, b in wrong], e)


def ptmcq(q, right, wrong, e):
    assert len({right} | set(wrong)) == 4
    return mcq(q, pt(*right), [pt(*w) for w in wrong], e)


def balance(sets, rnd):
    """Move the answers of the free questions so every position is right 5 times in each set."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("_fix", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, bold=True, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def tw(s, fs):
    """Rough width of bold Arial text."""
    s = plain(s)
    return sum(0.36 if ch in " .,()" else (0.62 if ch.isdigit() else 0.66) for ch in s) * fs


def SX(s):
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<tspan font-style='italic'>\1</tspan>", s)


def tov_svg(top, bot, heads, label="table of values"):
    """Two-row table of values. '?' shows red. Numbers are formatted."""
    lab = lambda v: v if isinstance(v, str) else n(v)
    top, bot = [lab(v) for v in top], [lab(v) for v in bot]
    CW = max(46, int(max(tw(t, 16) for t in top + bot) + 16))
    RH = 32
    LW = int(max(tw(h, 14) for h in heads) + 18)
    W, H = LW + CW * len(top) + 4, RH * 2 + 4
    s = []
    for r, (hd, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 5, SX(hd) if len(hd) == 1 else hd, 14 if len(hd) > 1 else 17))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def tbl(top, bot, heads=("x", "y"), label="table of values"):
    return fig(tov_svg(top, bot, heads, label))


# ---- stick pattern (squares in a row)
SQ = 24


def stick(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L * 2.5, dy / L * 2.5
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
            % (x1 + ux, y1 + uy, x2 - ux, y2 - uy, STICK))


def squares(k):
    def draw(x, y):
        s = [stick(x + i * SQ, y, x + i * SQ, y + SQ) for i in range(k + 1)]
        for i in range(k):
            s.append(stick(x + i * SQ, y, x + (i + 1) * SQ, y))
            s.append(stick(x + i * SQ, y + SQ, x + (i + 1) * SQ, y + SQ))
        return "".join(s)
    return k * SQ, SQ, draw


def sticks(k):
    return 3 * k + 1


def pattern_svg(steps=(1, 2, 3)):
    parts = [squares(k) for k in steps]
    m, gap, lab = 8, 26, 24
    hmax = max(max(h for _, h, _ in parts), 36)
    widths = [max(w, 62) for w, _, _ in parts]
    W = 2 * m + sum(widths) + gap * (len(parts) - 1)
    H = m + hmax + 8 + lab
    s, x = [], m
    for k, (w, h, draw), cw in zip(steps, parts, widths):
        s.append(draw(x + (cw - w) / 2, m + hmax - h))
        s.append(text(x + cw / 2, m + hmax + 8 + 16, "Figure %d" % k, 14))
        x += cw + gap
    return svg_wrap(W, H, "".join(s), "shape pattern of squares made of sticks")


# ---- four-quadrant grid (square, exact; every axis number is written)
HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"


def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


class Grid:
    def __init__(self, R=6, u=27):
        self.R, self.u = R, u
        self.ox = 24 + R * u
        self.oy = 34 + R * u
        self.W = self.H = int(math.ceil(24 + 2 * R * u + 34))
        self.pts = []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name="", col=RED):
        assert x == int(x) and y == int(y) and abs(x) <= self.R and abs(y) <= self.R, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col))
        return self

    def _label_cell(self, x, y, used, others, boxes):
        for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            cx, cy = x + dx, y + dy
            if not (abs(cx) <= self.R and abs(cy) <= self.R):
                continue
            if {(x + dx, y), (x, y + dy), (x + dx, y + dy)} & others:
                continue
            cell = (min(x, cx), min(y, cy))
            if cell in used:
                continue
            c = self.P(x + dx / 2.0, y + dy / 2.0)
            box = (c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7)
            if any(overlap(box, b) for b in boxes):
                continue
            used.add(cell)
            return c, box
        raise AssertionError(("no room for label", x, y))

    def svg(self, label):
        u, ox, oy, R = self.u, self.ox, self.oy, self.R
        s = []
        lo, hi = -R * u, R * u
        for k in range(-R, R + 1):
            if k == 0:
                continue
            x = ox + k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, oy - hi, x, oy - lo, GRID))
            y = oy - k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ox + lo, y, ox + hi, y, GRID))
        x0, x1 = ox + lo - 14, ox + hi + 14
        y0, y1 = oy - hi - 14, oy - lo + 14
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 + 4, oy, x1 - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, y0 + 4, ox, y1 - 4, INK))
        for (ax, ay, dx, dy) in [(x1, oy, 1, 0), (x0, oy, -1, 0), (ox, y0, 0, -1), (ox, y1, 0, 1)]:
            bx, by = ax - dx * 9, ay - dy * 9
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (ax, ay, bx - dy * 4.5, by + dx * 4.5, bx + dy * 4.5, by - dx * 4.5, INK))
        s.append(text(x1 + 3, oy + 5, "x", 15, anchor="start", extra=" font-style='italic'"))
        s.append(text(ox + 12, y0 + 8, "y", 15, anchor="start", extra=" font-style='italic'"))
        assert x1 + 3 + 10 <= self.W and y0 - 4 >= 0
        boxes = []
        for k in range(-R, R + 1):
            if k == 0:
                continue
            t = n(k)
            w = len(t) * 14 * 0.58
            cx = ox + k * u
            boxes.append((cx - w / 2, oy + 5, cx + w / 2, oy + 15.5))
            s.append(text(cx, oy + 15.5, t, 14, bold=False, extra=HALO))
            cy = oy - k * u
            boxes.append((ox - 6 - w, cy - 5, ox - 6, cy + 5))
            s.append(text(ox - 6, cy + 5, t, 14, "end", bold=False, extra=HALO))
        allpts = {(p[0], p[1]) for p in self.pts}
        for x, y, name, col in self.pts:
            c = self.P(x, y)
            dot = (c[0] - 4.5, c[1] - 4.5, c[0] + 4.5, c[1] + 4.5)
            for b in boxes:
                assert not overlap(dot, b, 0), ("dot on a number", x, y)
        used = set()
        for x, y, name, col in self.pts:
            c = self.P(x, y)
            s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (c[0], c[1], col))
            if name:
                lc, box = self._label_cell(x, y, used, allpts - {(x, y)}, boxes)
                boxes.append(box)
                s.append(text(lc[0], lc[1] + 5.8, name, 16, col=GREEN, extra=HALO))
        return svg_wrap(self.W, self.H, "".join(s), label)


def qgraph(pts, label, names=None):
    G = Grid(6)
    for i, (x, y) in enumerate(pts):
        G.point(x, y, names[i] if names else "")
    return fig(G.svg(label))


def rel_pts(a, b, xs):
    return [(x, int(lv(a, b, x))) for x in xs]


def panels_svg(groups, label="four graphs A to D"):
    """Four small four-quadrant graphs A, B, C, D (x and y from −4 to 4) in one picture."""
    U, R = 12, 4
    S = 2 * R * U
    PL, PT, PB, PR, GAP = 26, 24, 22, 8, 16
    PW = PL + S + PR
    W = 4 + 4 * PW + 3 * GAP
    H = PT + S + PB + 2
    s = []
    for i, pts in enumerate(groups):
        ox = 2 + i * (PW + GAP)
        X0 = ox + PL
        cx, cy = X0 + R * U, PT + R * U
        s.append(text(cx, 17, "ABCD"[i], 17, col=GREEN))
        for g in range(-R, R + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cx + g * U, PT, cx + g * U, PT + S, GRID))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (X0, cy + g * U, X0 + S, cy + g * U, GRID))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X0, cy, X0 + S, cy, INK))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (cx, PT, cx, PT + S, INK))
        for g in (-R, R):
            s.append(text(cx + g * U, PT + S + 17, n(g), 14, bold=False))
            s.append(text(X0 - 5, cy - g * U + 5, n(g), 14, "end", bold=False))
        for px, py in pts:
            assert abs(px) <= R and abs(py) <= R, (px, py)
            s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx + px * U, cy - py * U, RED))
    return svg_wrap(W, H, "".join(s), label)


GRAPHS = ["Graph A", "Graph B", "Graph C", "Graph D"]


def panels_q(groups, ai, a, b, xs, q, e):
    assert groups[ai] == rel_pts(a, b, xs), (groups[ai], a, b)
    return mcq_fixed(fig(panels_svg(groups)) + q, GRAPHS, ai, e)


# ============================================================ set 1: tables of values
def set_tables():
    its = []

    def sub(a, b, x, ans, wrong, e):
        assert lv(a, b, x) == ans, (a, b, x)
        return nmcq("For %s, what is %s when %s = %s?" % (eq(a, b), Y, X, n(x)), ans, wrong, e)

    its.append(sub(2, 1, 4, 9, [8, 10, 7],
                   "Multiply first, then add: 2 × 4 + 1 = 8 + 1 = <b>9</b>. 8 forgets the + 1. "
                   "10 adds first: (4 + 1) × 2. 7 is the value for %s = 3." % X))
    its.append(sub(3, -2, 5, 13, [17, 15, 33],
                   "3%s means 3 × %s: 3 × 5 − 2 = 15 − 2 = <b>13</b>. 17 adds the 2 instead of subtracting. "
                   "15 forgets the − 2. 33 reads 3%s as the number 35: 35 − 2." % (X, X, X)))
    its.append(sub(2, 3, -4, -5, [11, 5, -11],
                   "2 × (−4) = −8, and −8 + 3 = <b>−5</b>. 11 uses 4 instead of −4: 8 + 3. "
                   "5 drops the minus sign of the answer. −11 subtracts 3 instead of adding."))
    its.append(sub(-3, 1, 2, -5, [7, 5, -7],
                   "−3 × 2 = −6, and −6 + 1 = <b>−5</b>. 7 forgets the sign of the rate: 3 × 2 + 1. "
                   "5 drops the minus sign of the answer. −7 subtracts 1 instead of adding."))
    its.append(sub(-2, -1, -3, 5, [-7, 7, -5],
                   "−2 × (−3) = +6, because a negative times a negative is positive. Then 6 − 1 = <b>5</b>. "
                   "−7 makes −2 × (−3) negative. 7 adds 1 instead of subtracting. −5 drops the sign."))
    xs, ys = [-2, -1, 0, 1, 2], ["?", -4, -1, 2, 5]
    assert all(lv(3, -1, x) == y for x, y in zip(xs[1:], ys[1:])) and lv(3, -1, -2) == -7
    its.append(nmcq(tbl(xs, ys) + "The table is for %s. What is the missing value?" % eq(3, -1), -7, [5, -5, -6],
                    "3 × (−2) − 1 = −6 − 1 = <b>−7</b>. Check: the values go up by 3, and −7 + 3 = −4. "
                    "5 uses 2 instead of −2. −5 adds 1 instead of subtracting. −6 forgets the − 1."))
    xs, ys = [0, 1, 2, 3, 4], [4, 7, 10, 13, 16]
    assert slope(xs, ys) == 3
    its.append(nmcq(tbl(xs, ys) + "By how much does %s change each time %s goes up by 1?" % (Y, X), 3, [4, 7, 1],
                    "7 − 4 = 3, 10 − 7 = 3, 13 − 10 = 3. The constant rate is <b>3</b>. "
                    "4 is the value when %s = 0. 7 is the value when %s = 1. 1 is the change in %s, not in %s." % (X, X, X, Y)))
    xs, ys = [0, 1, 2, 3, 4], [9, 7, 5, 3, 1]
    assert slope(xs, ys) == -2
    its.append(nmcq(tbl(xs, ys) + "By how much does %s change each time %s goes up by 1?" % (Y, X), -2, [2, 9, 7],
                    "7 − 9 = −2. The values go down, so the change is negative: <b>−2</b>. "
                    "2 forgets the sign: a relation that goes down has a negative rate. 9 is the value when %s = 0." % X))
    xs, ys = [-2, -1, 0, 1, 2], [-8, -5, -2, 1, 4]
    assert slope(xs, ys) == 3
    its.append(nmcq(tbl(xs, ys) + "What is the initial value (the value of %s when %s = 0)?" % (Y, X), -2, [2, 1, -5],
                    "Find the column where %s = 0. There %s = <b>−2</b>. 2 drops the minus sign. "
                    "1 is the value when %s = 1, and −5 is the value when %s = −1." % (X, Y, X, X)))
    lists = {(a, b): ", ".join(n(lv(a, b, x)) for x in (-1, 0, 1, 2)) for a, b in [(2, -3), (-2, -3), (2, 3), (-2, 3)]}
    assert lists[(2, -3)] == "−5, −3, −1, 1"
    its.append(mcq("For %s = −1, 0, 1, 2, which list of %s-values matches %s?" % (X, Y, eq(2, -3)), lists[(2, -3)],
                   [lists[(-2, -3)], lists[(2, 3)], lists[(-2, 3)]],
                   "2 × (−1) − 3 = −5, then −3, −1, 1. The values go up by 2. The list is <b>−5, −3, −1, 1</b>. "
                   "−1, −3, −5, −7 goes down, as if the rate were −2. 1, 3, 5, 7 adds 3 instead of subtracting. 5, 3, 1, −1 has both mistakes."))
    xs, ys = [-1, 0, 1, 2, 3], [6, 2, -2, -5, -10]
    assert [lv(-4, 2, x) for x in xs] == [6, 2, -2, -6, -10]
    its.append(nmcq(tbl(xs, ys) + "The table should follow %s. One value is wrong. Which one?" % eq(-4, 2), -5, [6, -2, -10],
                    "The values should go down by 4: 6, 2, −2, −6, −10. For %s = 2: −4 × 2 + 2 = −6, so <b>−5</b> is wrong." % X))
    xs, ys = [-1, 0, 1, 2, 3], [8, 3, -2, "?", -12]
    assert lv(-5, 3, 2) == -7 and all(lv(-5, 3, x) == y for x, y in zip(xs, ys) if y != "?")
    its.append(nmcq(tbl(xs, ys) + "The table is for %s. What is the missing value?" % eq(-5, 3), -7, [13, 7, -13],
                    "−5 × 2 + 3 = −10 + 3 = <b>−7</b>. Check: the values go down by 5, and −2 − 5 = −7. "
                    "13 treats −5 × 2 as +10. 7 drops the minus sign. −13 subtracts 3 instead of adding."))
    xs, ys = [0, 2, 4, 6], [1, 7, 13, 19]
    assert slope(xs, ys) == 3
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate (the change in %s for each 1 that %s goes up)?" % (Y, X), 3, [6, 1, 2],
                    "%s goes up by 2 each time and %s goes up by 6. For each 1: 6 ÷ 2 = <b>3</b>. "
                    "6 forgets that %s skips numbers. 1 is the initial value. 2 is the change in %s." % (X, Y, X, X)))
    xs, ys = [-3, -1, 1, 3], [10, 6, 2, -2]
    assert slope(xs, ys) == -2
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate (the change in %s for each 1 that %s goes up)?" % (Y, X), -2, [-4, 2, 4],
                    "%s goes up by 2 and %s goes down by 4. The rate is −4 ÷ 2 = <b>−2</b>. "
                    "−4 forgets to divide by the change in %s. 2 and 4 forget that the values go down." % (X, Y, X)))
    xs, ys = [1, 2, 3, 4], [4, 1, -2, -5]
    assert slope(xs, ys) == -3
    its.append(nmcq(tbl(xs, ys) + "What is the initial value (the value of %s when %s = 0)?" % (Y, X), 7, [4, 1, -3],
                    "The rate is −3. Going back one step from %s = 1 does the opposite, so <b>add</b> 3: 4 + 3 = <b>7</b>. "
                    "4 is the value when %s = 1. 1 subtracts 3 again, but that is the value for %s = 2. −3 is the rate." % (X, X, X)))
    xs, ys = [0, 1, 2, 3], [-9, -5, -1, 3]
    assert slope(xs, ys) == 4 and lv(4, -9, 10) == 31
    its.append(nmcq(tbl(xs, ys) + "The relation continues. What is %s when %s = 10?" % (Y, X), 31, [40, 49, 27],
                    "The rule is %s. For %s = 10: 4 × 10 − 9 = 40 − 9 = <b>31</b>. "
                    "40 forgets the initial value −9. 49 adds 9 instead of subtracting. 27 is the value for %s = 9." % (eq(4, -9), X, X)))
    assert lv(3, -4, 7) == 17
    its.append(nmcq("For %s, which value of %s gives %s = 17?" % (eq(3, -4), X, Y), 7, [21, 47, 6],
                    "Undo − 4: 17 + 4 = 21. Undo × 3: 21 ÷ 3 = <b>7</b>. Check: 3 × 7 − 4 = 17. "
                    "21 stops before dividing. 47 puts 17 in for %s instead of %s. 6 gives 14." % (X, Y)))
    its.append(sub(-2, 5, -6, 17, [-7, 7, -17],
                   "−2 × (−6) = +12, and 12 + 5 = <b>17</b>. −7 makes −2 × (−6) negative: −12 + 5. "
                   "7 subtracts 5: 12 − 5. −17 drops the sign of the answer."))
    assert lv(2, 3, 2) == lv(3, 1, 2) == 7
    its.append(nmcq("For which value of %s do %s and %s give the same %s?" % (X, eq(2, 3), eq(3, 1), Y), 2, [7, 4, 1],
                    "Make a table. %s = 1: 5 and 4. %s = 2: 7 and 7. They match at %s = <b>2</b>. "
                    "7 is the value of %s, not %s. 4 adds 3 + 1. At %s = 1 the values are 5 and 4." % (X, X, X, Y, X, X)))
    xs, ys = [-4, -2, 0, 2], [11, 5, -1, -7]
    assert slope(xs, ys) == -3 and lv(-3, -1, 5) == -16
    its.append(nmcq(tbl(xs, ys) + "The relation continues. What is %s when %s = 5?" % (Y, X), -16, [14, -13, -19],
                    "%s goes up by 2 and %s goes down by 6, so the rate is −3. The initial value is −1. "
                    "−3 × 5 − 1 = −15 − 1 = <b>−16</b>. 14 uses a rate of +3. −13 is the value for %s = 4 and −19 is for %s = 6." % (X, Y, X, X)))
    return {"title": "Tables of values", "items": its}


# ============================================================ set 2: equations from tables
def set_equations():
    its = []
    Q = "Which equation matches the table?"

    def ft(xs, ys, right, wrong, e):
        return eqmcq(tbl(xs, ys) + Q, right, wrong, e, xs, ys)

    its.append(ft([0, 1, 2, 3], [-2, 1, 4, 7], (3, -2), [(-2, 3), (3, 2), (3, 1)],
                  "%s goes up by 3, so the rate is 3. When %s = 0, %s = −2. The equation is <b>%s</b>. "
                  "%s swaps the rate and the initial value. %s drops the minus sign. %s uses the value for %s = 1."
                  % (Y, X, Y, eq(3, -2), eq(-2, 3), eq(3, 2), eq(3, 1), X)))
    its.append(ft([0, 1, 2, 3], [5, 3, 1, -1], (-2, 5), [(2, 5), (-2, 3), (5, -2)],
                  "%s goes down by 2, so the rate is −2. When %s = 0, %s = 5: <b>%s</b>. "
                  "%s forgets that a relation going down has a negative rate. %s uses the value for %s = 1."
                  % (Y, X, Y, eq(-2, 5), eq(2, 5), eq(-2, 3), X)))
    its.append(ft([1, 2, 3, 4], [2, 6, 10, 14], (4, -2), [(4, 2), (-2, 4), (4, 6)],
                  "The rate is 4. Go back one step to %s = 0: 2 − 4 = −2. The equation is <b>%s</b>. "
                  "%s uses the value for %s = 1 as the initial value. %s adds 4 when going back instead of subtracting."
                  % (X, eq(4, -2), eq(4, 2), X, eq(4, 6))))
    its.append(ft([1, 2, 3, 4], [1, -3, -7, -11], (-4, 5), [(-4, 1), (4, -3), (-4, -3)],
                  "The rate is −4. Going back one step does the opposite, so add 4: 1 + 4 = 5. The equation is <b>%s</b>. "
                  "%s uses the value for %s = 1. %s fits %s = 1 but goes up. %s subtracts 4 when going back."
                  % (eq(-4, 5), eq(-4, 1), X, eq(4, -3), X, eq(-4, -3))))
    its.append(ft([-2, -1, 0, 1], [-7, -4, -1, 2], (3, -1), [(3, -7), (-3, -1), (3, 1)],
                  "The values go up by 3, so the rate is 3. In the column %s = 0, %s = −1: <b>%s</b>. "
                  "%s uses the first column, but it is %s = −2, not 0. %s sees negative numbers and makes the rate negative."
                  % (X, Y, eq(3, -1), eq(3, -7), X, eq(-3, -1))))
    its.append(ft([-1, 0, 1, 2], [7, 3, -1, -5], (-4, 3), [(4, 3), (-4, 7), (-4, -1)],
                  "The values go down by 4, so the rate is −4. When %s = 0, %s = 3: <b>%s</b>. "
                  "%s has the wrong sign of the rate. %s uses the first column (%s = −1). %s uses the value for %s = 1."
                  % (X, Y, eq(-4, 3), eq(4, 3), eq(-4, 7), X, eq(-4, -1), X)))
    its.append(ft([0, 2, 4, 6], [-3, 1, 5, 9], (2, -3), [(4, -3), (2, 3), (-3, 2)],
                  "%s goes up by 2 and %s goes up by 4, so the rate is 4 ÷ 2 = 2. The initial value is −3: <b>%s</b>. "
                  "%s forgets that %s skips numbers. %s drops the minus sign. %s swaps the rate and the initial value." % (X, Y, eq(2, -3), eq(4, -3), X, eq(2, 3), eq(-3, 2))))
    its.append(ft([0, 3, 6, 9], [8, 2, -4, -10], (-2, 8), [(-6, 8), (2, 8), (-3, 8)],
                  "%s goes up by 3 and %s goes down by 6, so the rate is −6 ÷ 3 = −2. The initial value is 8: <b>%s</b>. "
                  "%s does not divide by 3. %s has the wrong sign. %s uses the change in %s as the rate."
                  % (X, Y, eq(-2, 8), eq(-6, 8), eq(2, 8), eq(-3, 8), X)))
    its.append(ft([-3, -2, -1, 0], [-11, -8, -5, -2], (3, -2), [(3, -11), (-3, -2), (-2, 3)],
                  "−8 − (−11) = 3, so the values go up by 3. The last column is %s = 0, where %s = −2: <b>%s</b>. "
                  "%s uses the first column. %s sees negative numbers and makes the rate negative."
                  % (X, Y, eq(3, -2), eq(3, -11), eq(-3, -2))))
    its.append(eqmcq("A linear relation has a constant rate of −5. When %s = 0, %s = −3. Which equation shows it?" % (X, Y),
                     (-5, -3), [(-3, -5), (5, -3), (-5, 3)],
                     "The rate multiplies %s and the initial value is added on its own: <b>%s</b>. "
                     "%s swaps the two numbers. %s has the wrong sign of the rate." % (X, eq(-5, -3), eq(-3, -5), eq(5, -3)),
                     [0, 1], [-3, -8]))
    its.append(eqmcq("A linear relation passes through (1, 4) and (3, 10). Which equation shows it?",
                     (3, 1), [(6, -2), (3, 4), (3, 7)],
                     "The rate is (10 − 4) ÷ (3 − 1) = 6 ÷ 2 = 3. Go back one step from (1, 4): 4 − 3 = 1. "
                     "The equation is <b>%s</b>. %s does not divide by the change in %s. %s uses the value for %s = 1 as the initial value."
                     % (eq(3, 1), eq(6, -2), X, eq(3, 4), X), [1, 3], [4, 10]))
    its.append(eqmcq("A linear relation passes through (−1, 9) and (2, 0). Which equation shows it?",
                     (-3, 6), [(3, 6), (-9, 0), (-3, 9)],
                     "The rate is (0 − 9) ÷ (2 − (−1)) = −9 ÷ 3 = −3. From %s = −1 to %s = 0 is one step: 9 − 3 = 6. "
                     "The equation is <b>%s</b>. %s has the wrong sign: the values go down. %s does not divide by 3. "
                     "%s uses 9 as the initial value, but 9 is the value when %s = −1."
                     % (X, X, eq(-3, 6), eq(3, 6), eq(-9, 0), eq(-3, 9), X), [-1, 2], [9, 0]))
    xs, ys = [0, 1, 2, 3], [4, 2, 0, -2]
    its.append(eqmcq(tbl(xs, ys) + "Owen writes %s for this table. What is the correct equation?" % eq(2, 4),
                     (-2, 4), [(2, 4), (-2, 2), (4, -2)],
                     "Owen’s equation gives 6 when %s = 1, but the table shows 2. The values go down by 2, so the rate is "
                     "negative: <b>%s</b>. When the values go down, the rate must be negative." % (X, eq(-2, 4)), xs, ys))
    v = [sticks(k) for k in (1, 2, 3)]
    its.append(eqmcq(fig(pattern_svg()) + "Which equation gives the number of sticks, %s, in Figure %s?" % (Y, X),
                     (3, 1), [(4, 0), (3, 4), (1, 3)],
                     "Count: 4, 7, 10. The rate is 3. Figure 0 would have 4 − 3 = 1 stick. The equation is <b>%s</b>. "
                     "%s counts 4 sticks for each square, but squares next to each other share a stick. "
                     "%s uses Figure 1 as the initial value." % (eq(3, 1), eq(4, 0), eq(3, 4)), [1, 2, 3], v))
    lists = {(a, b): ", ".join(n(lv(a, b, x)) for x in (-1, 0, 1, 2)) for a, b in [(-3, 2), (3, 2), (3, -2)]}
    l0 = ", ".join(n(lv(-3, 2, x)) for x in (0, 1, 2, 3))
    assert lists[(-3, 2)] == "5, 2, −1, −4"
    its.append(mcq("For %s = −1, 0, 1, 2, which list of values matches %s?" % (X, eq(-3, 2)), lists[(-3, 2)],
                   [lists[(3, 2)], lists[(3, -2)], l0],
                   "−3 × (−1) + 2 = 3 + 2 = 5, then 2, −1, −4. The list is <b>5, 2, −1, −4</b>. "
                   "−1, 2, 5, 8 goes up, as if the rate were +3. 2, −1, −4, −7 starts at %s = 0 instead of −1." % X))
    xs, ys = [-2, -1, 0, 1], [4, 4, 4, 4]
    its.append(mcq(tbl(xs, ys) + Q, "%s = 4" % Y, ["%s = 4%s" % (Y, X), "%s = %s + 4" % (Y, X), "%s = 4" % X],
                   "%s does not change, so the rate is 0 and %s is always 4: <b>%s = 4</b>. "
                   "%s = 4%s gives −8 when %s = −2. %s = %s + 4 goes up by 1. %s = 4 would need %s to stay 4, but here %s changes and %s stays 4."
                   % (Y, Y, Y, Y, X, X, Y, X, X, X, X, Y)))
    its.append(ft([0, 1, 2, 3], [-2, -3, -4, -5], (-1, -2), [(1, -2), (-2, -1), (-1, -3)],
                  "The values go down by 1, so the rate is −1. When %s = 0, %s = −2: <b>%s</b>. "
                  "%s goes up. %s swaps the rate and the initial value. %s uses the value for %s = 1."
                  % (X, Y, eq(-1, -2), eq(1, -2), eq(-2, -1), eq(-1, -3), X)))
    its.append(ft([2, 3, 4, 5], [-2, 3, 8, 13], (5, -12), [(5, -2), (5, -7), (-5, 8)],
                  "The rate is 5. %s = 2 is two steps from %s = 0, so take away 5 twice: −2 − 10 = −12. "
                  "The equation is <b>%s</b>. %s uses the first column as the initial value. %s goes back only one step. "
                  "%s fits %s = 2 but goes down." % (X, X, eq(5, -12), eq(5, -2), eq(5, -7), eq(-5, 8), X)))
    xs, ys = [1, 2, 3, 4], [4, 6, 8, 10]
    its.append(eqmcq(tbl(xs, ys) + "Jasleen looks only at %s = 2, %s = 6 and writes %s. Which equation fits the whole table?"
                     % (X, Y, eq(3, 0)), (2, 2), [(3, 0), (4, 0), (2, 4)],
                     "The values go up by 2, so the rate is 2. Go back from %s = 1: 4 − 2 = 2. The equation is <b>%s</b>. "
                     "%s fits only %s = 2, and %s fits only %s = 1. Always check every column. %s uses the value for %s = 1."
                     % (X, eq(2, 2), eq(3, 0), X, eq(4, 0), X, eq(2, 4), X), xs, ys))
    its.append(ft([-4, -1, 2, 5], [14, 8, 2, -4], (-2, 6), [(-6, 14), (2, 6), (-2, 2)],
                  "%s goes up by 3 and %s goes down by 6, so the rate is −6 ÷ 3 = −2. From %s = 2 back to 0 is two steps: "
                  "2 + 4 = 6. The equation is <b>%s</b>. %s does not divide by 3. %s has the wrong sign. "
                  "%s uses the value for %s = 2 as the initial value."
                  % (X, Y, X, eq(-2, 6), eq(-6, 14), eq(2, 6), eq(-2, 2), X)))
    return {"title": "Equations from tables", "items": its}


# ============================================================ set 3: graph relations in four quadrants
def set_plot():
    its = []
    assert lv(2, -1, 3) == 5
    its.append(ptmcq("Which point is on the graph of %s?" % eq(2, -1), (3, 5), [(5, 3), (3, 7), (-3, 5)],
                     "For %s = 3: 2 × 3 − 1 = 5, so the point is <b>(3, 5)</b>. (5, 3) writes (%s, %s). "
                     "(3, 7) adds 1 instead of subtracting. For %s = −3 the value is −7, not 5." % (X, Y, X, X)))
    assert lv(-3, 2, -2) == 8
    its.append(ptmcq("Which point is on the graph of %s?" % eq(-3, 2), (-2, 8), [(8, -2), (-2, -4), (-2, -8)],
                     "For %s = −2: −3 × (−2) + 2 = 6 + 2 = 8. The point is <b>(−2, 8)</b>. (8, −2) writes (%s, %s). "
                     "(−2, −4) uses a rate of +3. (−2, −8) makes −3 × (−2) negative." % (X, Y, X)))
    assert lv(1, -4, 3) == -1
    its.append(ptmcq("Ethan graphs %s. Which point should he plot for %s = 3?" % (eq(1, -4), X), (3, -1),
                     [(-1, 3), (3, 1), (3, -4)],
                     "3 − 4 = −1, so he plots <b>(3, −1)</b>: right 3, then down 1. (−1, 3) plots (%s, %s). "
                     "(3, 1) drops the minus sign. (3, −4) uses the initial value instead of the value at %s = 3." % (Y, X, X)))
    g = rel_pts(2, 1, range(-2, 3))
    its.append(mcq(qgraph(g, "graph of y = 2x + 1 for x from −2 to 2") +
                   "The graph shows %s for %s = −2 to 2. In which quadrant is the point for %s = −2?" % (eq(2, 1), X, X),
                   "Quadrant III", ["Quadrant II", "Quadrant IV", "Quadrant I"],
                   "For %s = −2, %s = 2 × (−2) + 1 = −3. The point (−2, −3) is left and down: <b>Quadrant III</b>. "
                   "Quadrant II would need %s to be positive. The quadrants go counterclockwise from the top right: I, II, III, IV." % (X, Y, Y)))
    pts = [(-3, -1), (-2, 0), (-1, 1), (0, 2), (1, 3), (4, 2)]
    assert all(lv(1, 2, x) == y for x, y in pts[:5]) and lv(1, 2, 2) == 4
    its.append(mcq(qgraph(pts, "graph of six labelled points, one plotted as (y, x)", names=list("ABCDEF")) +
                   "Hana plots %s for %s = −3, −2, −1, 0, 1, 2. She plots one point as (%s, %s). Which point?" % (eq(1, 2), X, Y, X),
                   "Point F", ["Point E", "Point D", "Point A"],
                   "For %s = 2, %s = 4, so the point should be (2, 4). <b>Point F</b> is at (4, 2): across 4, up 2. "
                   "The other points fit: A (−3, −1), B (−2, 0), C (−1, 1), D (0, 2), E (1, 3)." % (X, Y)))
    xs = [-1, 0, 1, 2]
    its.append(panels_q([rel_pts(-1, -2, xs), rel_pts(1, -2, xs), [(y, x) for x, y in rel_pts(1, -2, xs)], rel_pts(1, 2, xs)],
                        1, 1, -2, xs, "Which graph shows %s for %s = −1, 0, 1, 2?" % (eq(1, -2), X),
                        "The points are (−1, −3), (0, −2), (1, −1), (2, 0): <b>Graph B</b>. Graph A goes down, as if the rate were −1. "
                        "Graph C plots (%s, %s). Graph D uses + 2 instead of − 2." % (Y, X)))
    xs = [-1, 0, 1]
    its.append(panels_q([rel_pts(2, 1, xs), [(y, x) for x, y in rel_pts(-2, 1, xs)], rel_pts(-2, -1, xs), rel_pts(-2, 1, xs)],
                        3, -2, 1, xs, "Which graph shows %s for %s = −1, 0, 1?" % (eq(-2, 1), X),
                        "−2 × (−1) + 1 = 3, then 1, then −1. The points are (−1, 3), (0, 1), (1, −1): <b>Graph D</b>. "
                        "Graph A goes up: it uses a rate of +2. Graph B plots (%s, %s). Graph C has −1 as the initial value." % (Y, X)))
    xs = [-2, -1, 0, 1]
    its.append(panels_q([rel_pts(-1, -1, xs), rel_pts(1, -1, xs), rel_pts(-1, 1, xs), rel_pts(2, 1, xs)],
                        0, -1, -1, xs, "Which graph shows a relation with a negative rate and an initial value of −1?",
                        "A negative rate goes down from left to right. The initial value is where the points cross the %s-axis. "
                        "<b>Graph A</b> goes down and passes through (0, −1). Graph B passes through (0, −1) but goes up. "
                        "Graph C goes down but passes through (0, 1)." % Y))
    g = rel_pts(-1, 1, range(-3, 4))
    its.append(eqmcq(qgraph(g, "graph of y = −x + 1 for x from −3 to 3") + "Which equation matches the graph?",
                     (-1, 1), [(1, 1), (-1, -1), (1, -1)],
                     "The points cross the %s-axis at (0, 1) and go down 1 for each step right: <b>%s</b>. "
                     "%s goes up from left to right. %s has the wrong initial value." % (Y, eq(-1, 1), eq(1, 1), eq(-1, -1)),
                     [x for x, _ in g], [y for _, y in g]))
    assert lv(-4, -3, -2) == 5 and lv(-4, -3, 2) != 5
    its.append(ptmcq("Which point is on the graph of %s?" % eq(-4, -3), (-2, 5), [(5, -2), (-2, -11), (2, 5)],
                     "For %s = −2: −4 × (−2) − 3 = 8 − 3 = 5. The point is <b>(−2, 5)</b>. (5, −2) writes (%s, %s). "
                     "(−2, −11) makes −4 × (−2) negative. For %s = 2 the value is −11, not 5." % (X, Y, X, X)))
    assert lv(2, -5, 6) == 7
    its.append(nmcq("The point (<i>k</i>, 7) is on the graph of %s. What is <i>k</i>?" % eq(2, -5), 6, [9, 1, 12],
                    "Solve 2%s − 5 = 7. Add 5: 2%s = 12. Divide by 2: %s = <b>6</b>. "
                    "9 puts 7 in for %s: 2 × 7 − 5. 1 subtracts 5 instead of adding. 12 forgets to divide." % (X, X, X, X)))
    assert lv(-2, 4, -3) == 10
    its.append(nmcq("The point (−3, <i>m</i>) is on the graph of %s. What is <i>m</i>?" % eq(-2, 4), 10, [-2, -10, 1],
                    "−2 × (−3) + 4 = 6 + 4 = <b>10</b>. −2 makes −2 × (−3) negative. −10 makes both parts negative. "
                    "1 forgets to multiply: −3 + 4."))
    its.append(mcq("For %s, in which quadrant are the points when %s is less than −5?" % (eq(1, 5), X),
                   "Quadrant III", ["Quadrant II", "Quadrant IV", "Quadrant I"],
                   "If %s is less than −5, then %s + 5 is less than 0. Both %s and %s are negative: <b>Quadrant III</b>. "
                   "For example, %s = −7 gives (−7, −2). Quadrant II only looks at %s." % (X, X, X, Y, X, X)))
    assert lv(-3, 0, 2) == -6 and lv(-3, 0, -2) == 6
    its.append(mcq("The graph of %s is plotted for %s = −3 to 3. Which quadrants do its points lie in?" % (eq(-3, 0), X),
                   "II and IV", ["I and III", "I and II", "III and IV"],
                   "When %s is positive, %s is negative: (2, −6) is in Quadrant IV. When %s is negative, %s is positive: "
                   "(−2, 6) is in Quadrant II. The answer is <b>II and IV</b>, plus the origin. "
                   "I and III would need a positive rate." % (X, Y, X, Y)))
    g = rel_pts(3, -2, range(-1, 3))
    its.append(nmcq(qgraph(g, "graph of y = 3x − 2 for x from −1 to 2") +
                    "Read the graph. What is %s when %s = −1?" % (Y, X), -5, [5, 1, -2],
                    "Find −1 on the %s-axis and go down to the point: it is 5 below the %s-axis, so %s = <b>−5</b>. "
                    "5 forgets the point is below the axis. 1 is the value when %s = 1. −2 is the value when %s = 0." % (X, X, Y, X, X)))
    g = rel_pts(-2, 3, range(0, 4))
    assert lv(-2, 3, 4) == -5
    its.append(ptmcq(qgraph(g, "graph of y = −2x + 3 for x from 0 to 3") +
                     "The pattern of points continues. Which point comes next?", (4, -5), [(-5, 4), (4, 5), (4, -4)],
                     "Each step right, the points go down 2: 3, 1, −1, −3, then <b>(4, −5)</b>. (−5, 4) writes (%s, %s). "
                     "(4, 5) goes up instead of down. (4, −4) goes down only 1." % (Y, X)))
    its.append(mcq("Mateo makes a table for %s with %s = −1, 0, 1, 2. He plots (−7, −1), (−4, 0), (−1, 1) and (2, 2). "
                   "What did he do wrong?" % (eq(3, -4), X),
                   "He plotted (%s, %s) instead of (%s, %s)" % (Y, X, X, Y),
                   ["He used the wrong rate", "He forgot the − 4", "Nothing: the points are correct"],
                   "The table gives (−1, −7), (0, −4), (1, −1), (2, 2). Mateo put %s first. "
                   "<b>He plotted (%s, %s)</b>. Go across for %s first, then up or down for %s." % (Y, Y, X, X, Y)))
    pts = [(-3, 2), (2, 5), (2, -3), (-2, -3)]
    assert [lv(-2, 1, x) == y for x, y in pts] == [False, False, True, False]
    its.append(mcq_fixed(qgraph(pts, "graph of four labelled points A, B, C, D", names=list("ABCD")) +
                         "Which point is on the graph of %s?" % eq(-2, 1), ["A", "B", "C", "D"], 2,
                         "For %s = 2: −2 × 2 + 1 = −3, so <b>C</b> (2, −3) is on the graph. A (−3, 2) is C with %s and %s swapped. "
                         "B (2, 5) uses a rate of +2. For D, %s = −2 gives 5, not −3." % (X, X, Y, X)))
    cand = [(0, -3), (5, 2), (-1, -4), (2, 1)]
    assert sum(lv(1, -3, x) == y for x, y in cand) == 3
    its.append(nmcq("How many of these points are on the graph of %s: (0, −3), (5, 2), (−1, −4), (2, 1)?" % eq(1, -3),
                    3, [4, 2, 1],
                    "Test each point: 0 − 3 = −3 yes, 5 − 3 = 2 yes, −1 − 3 = −4 yes, 2 − 3 = −1 not 1. "
                    "<b>3</b> points are on the graph. 4 forgets to test (2, 1). For %s = 2 the point would be (2, −1)." % X))
    assert 2 * -2 + 5 == 1
    its.append(nmcq("The graph of %s = 2%s + <i>b</i> passes through (−2, 1). What is <i>b</i>?" % (Y, X), 5, [-3, 1, 3],
                    "Put in the point: 1 = 2 × (−2) + <i>b</i>, so 1 = −4 + <i>b</i>. Add 4: <i>b</i> = <b>5</b>. "
                    "−3 adds −4 instead of undoing it. 1 is the value of %s, not the initial value. 3 adds the rate 2 to 1." % Y))
    return {"title": "Graph linear relations in four quadrants", "items": its}


# ============================================================ set 4: interpret graphs
def set_interpret():
    its = []
    g1 = rel_pts(2, -3, range(-1, 5))
    G1 = qgraph(g1, "graph of y = 2x − 3 for x from −1 to 4")
    xs1, ys1 = [x for x, _ in g1], [y for _, y in g1]
    its.append(nmcq(G1 + "What is the initial value (the value of %s when %s = 0)?" % (Y, X), -3, [3, 2, -5],
                    "The initial value is where the points cross the %s-axis: (0, −3), so it is <b>−3</b>. "
                    "3 forgets the point is below the %s-axis. 2 is the rate. −5 is the value when %s = −1." % (Y, X, X)))
    its.append(nmcq(G1 + "By how much does %s change each time %s goes up by 1?" % (Y, X), 2, [-2, -3, 1],
                    "Each step right, the points go up 2: (0, −3), (1, −1), (2, 1). The rate is <b>2</b>. "
                    "−2 sees points below the %s-axis and makes the rate negative, but the points go up. "
                    "−3 is the initial value. 1 is the step in %s." % (X, X)))
    its.append(eqmcq(G1 + "Which equation matches the graph?", (2, -3), [(-3, 2), (2, 3), (-2, -3)],
                     "Rate 2, initial value −3: <b>%s</b>. %s swaps the rate and the initial value. "
                     "%s drops the minus sign. %s would go down from left to right." % (eq(2, -3), eq(-3, 2), eq(2, 3), eq(-2, -3)),
                     xs1, ys1))
    its.append(mcq(G1 + "How does %s change as %s goes up?" % (Y, X),
                   "It goes up 2 for each step right",
                   ["It goes down 2 for each step right", "It goes up 3 for each step right",
                    "It goes down, because some values are negative"],
                   "Read from left to right: −5, −3, −1, 1, 3, 5. <b>%s goes up 2 for each step right</b>. "
                   "Negative values do not mean the relation goes down: look at the direction, not the sign of the values." % Y))
    g2 = rel_pts(-3, 3, range(-1, 4))
    G2 = qgraph(g2, "graph of y = −3x + 3 for x from −1 to 3")
    its.append(nmcq(G2 + "What is the constant rate of this relation?", -3, [3, -6, 1],
                    "Each step right, the points go down 3: (0, 3), (1, 0), (2, −3). The rate is <b>−3</b>. "
                    "3 forgets that the points go down. −6 is the value when %s = 3. 1 is the step in %s." % (X, X)))
    its.append(nmcq(G2 + "For which value of %s is %s = 0?" % (X, Y), 1, [3, 0, -1],
                    "%s = 0 on the %s-axis. The point (1, 0) is there, so %s = <b>1</b>. "
                    "3 is the initial value. 0 is the value of %s, not %s. At %s = −1 the value is 6." % (Y, X, X, Y, X, X)))
    its.append(eqmcq(G2 + "Which equation matches the graph?", (-3, 3), [(3, 3), (3, -3), (-3, 6)],
                     "The points start at 3 on the %s-axis and go down 3 for each step right: <b>%s</b>. "
                     "%s goes up instead of down. %s swaps the numbers. %s uses the first point (%s = −1) as the initial value."
                     % (Y, eq(-3, 3), eq(3, 3), eq(3, -3), eq(-3, 6), X), [x for x, _ in g2], [y for _, y in g2]))
    assert lv(-3, 3, 6) == -15
    its.append(nmcq(G2 + "The relation continues in the same way. What is %s when %s = 6?" % (Y, X), -15, [21, -12, -18],
                    "The graph shows %s. For %s = 6: −3 × 6 + 3 = −18 + 3 = <b>−15</b>. "
                    "21 uses a rate of +3. −12 is the value for %s = 5. −18 forgets the initial value 3." % (eq(-3, 3), X, X)))
    its.append(mcq(G2 + "In which quadrant is the point for %s = 3?" % X, "Quadrant IV", ["Quadrant II", "Quadrant I", "Quadrant III"],
                   "For %s = 3 the point is (3, −6): right and down, <b>Quadrant IV</b>. "
                   "Quadrant II comes from reading it as (−6, 3)." % X))
    its.append(mcq("Relation P is %s. Relation Q is %s. Which statement is true?" % (eq(4, -1), eq(-4, -1)),
                   "Same initial value; P goes up and Q goes down",
                   ["Same rate; different initial values", "P and Q are the same relation",
                    "Different initial values; both go up"],
                   "Both cross the %s-axis at −1. P has rate 4, so it goes up. Q has rate −4, so it goes down. "
                   "<b>Same initial value; P goes up and Q goes down.</b> The sign of the rate changes the direction." % Y))
    g3 = rel_pts(-1, -2, range(-4, 4))
    G3 = qgraph(g3, "graph of y = −x − 2 for x from −4 to 3")
    its.append(ptmcq(G3 + "Where do the points cross the %s-axis?" % X, (-2, 0), [(0, -2), (2, 0), (0, 2)],
                     "On the %s-axis, %s = 0. The point (−2, 0) is there: <b>(−2, 0)</b>. "
                     "(0, −2) is where the points cross the %s-axis. (2, 0) drops the minus sign." % (X, Y, Y)))
    assert lv(-1, -2, -4) == 2
    its.append(nmcq(G3 + "What is %s when %s = −4?" % (Y, X), 2, [-6, 6, -2],
                    "Find −4 on the %s-axis and go up to the point: <b>2</b>. Check: −(−4) − 2 = 4 − 2 = 2. "
                    "−6 uses a rate of +1: −4 − 2. 6 adds 2 instead of subtracting. −2 is the initial value." % X))
    its.append(eqmcq(G3 + "Which equation matches the graph?", (-1, -2), [(1, -2), (-2, -1), (-1, 2)],
                     "The points cross the %s-axis at −2 and go down 1 for each step right: <b>%s</b>. "
                     "%s goes up. %s swaps the numbers. %s has the wrong initial value." % (Y, eq(-1, -2), eq(1, -2), eq(-2, -1), eq(-1, 2)),
                     [x for x, _ in g3], [y for _, y in g3]))
    its.append(mcq("Which relation is discrete (graphed as separate points, not joined with a line)?",
                   "The number of seats in %s rows of a theatre" % X,
                   ["The temperature over one day", "The water in a draining bathtub over time",
                    "The distance a ferry travels over time"],
                   "You can have 4 or 5 rows, but not 4.5 rows, so <b>seats and rows</b> is discrete. "
                   "Time can be any value, so the other three are continuous."))
    xs = [-2, -1, 0, 1]
    its.append(panels_q([rel_pts(1, 1, xs), rel_pts(-1, 2, range(-2, 3)), rel_pts(-1, -2, range(-2, 3)), rel_pts(1, -2, range(-2, 3))],
                        1, -1, 2, range(-2, 3), "Which graph has a negative rate and a positive initial value?",
                        "A negative rate goes down from left to right. A positive initial value crosses the %s-axis above 0. "
                        "<b>Graph B</b> goes down and passes through (0, 2). Graph C goes down but passes through (0, −2). "
                        "Graphs A and D go up." % Y))
    xs = list(range(-2, 3))
    its.append(panels_q([rel_pts(-2, 0, xs), [(y, x) for x, y in rel_pts(2, 0, xs)], rel_pts(1, 2, xs), rel_pts(2, 0, xs)],
                        3, 2, 0, xs, "Which graph shows %s?" % eq(2, 0),
                        "The points are (−2, −4), (−1, −2), (0, 0), (1, 2), (2, 4): <b>Graph D</b>. "
                        "Graph A goes down: it shows %s. Graph B plots (%s, %s). Graph C shows %s." % (eq(-2, 0), Y, X, eq(1, 2))))
    its.append(nmcq("On a graph, the points go down 4 squares for every 2 squares to the right. What is the constant rate?", -2,
                    [-4, 2, 4],
                    "The rate is the change in %s for each 1 that %s goes up: −4 ÷ 2 = <b>−2</b>. "
                    "−4 forgets to divide by 2. 2 and 4 forget that the points go down." % (Y, X)))
    its.append(mcq(G2 + "Owen says the rate is 3 because the points are 3 squares apart. What is the correct rate, and why?",
                   "−3, because %s goes down as %s goes up" % (Y, X),
                   ["3, because the points are 3 apart", "−3, because some points are below the %s-axis" % X,
                    "3, because the initial value is 3"],
                   "Read from left to right: 6, 3, 0, −3, −6. The values go down 3 each step, so the rate is <b>−3</b>. "
                   "The sign of the rate comes from the direction, not from where the points are."))
    assert lv(2, -3, 6) == 9
    its.append(ptmcq(G1 + "The relation continues. Which point is also on it?", (6, 9), [(9, 6), (6, 12), (5, 9)],
                     "For %s = 6: 2 × 6 − 3 = 9, so <b>(6, 9)</b>. (9, 6) writes (%s, %s). "
                     "(6, 12) forgets the − 3. For %s = 5 the value is 7, not 9." % (X, Y, X, X)))
    assert lv(1, 1, 2) == lv(-1, 5, 2) == 3
    its.append(ptmcq("At which point do the graphs of %s and %s meet?" % (eq(1, 1), eq(-1, 5)), (2, 3), [(3, 2), (1, 2), (0, 5)],
                     "Make a table. %s = 1: 2 and 4. %s = 2: 3 and 3. They meet at <b>(2, 3)</b>. "
                     "(3, 2) writes (%s, %s). (1, 2) is on %s only. (0, 5) is the initial value of %s." % (X, X, Y, X, eq(1, 1), eq(-1, 5))))
    return {"title": "Interpret graphs", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    assert 10 * 4 + 30 == 70
    its.append(eqmcq("A snowshoe rental at Mount Seymour costs $30 plus $10 for each hour. Which equation gives the cost, "
                     "<i>C</i>, in dollars, for <i>h</i> hours?", (10, 30), [(30, 10), (40, 0), (10, 0)],
                     "Each hour adds $10, so the rate is 10. The $30 is paid once, so it is the initial value: <b>%s</b>. "
                     "%s charges $30 every hour. %s adds the $30 to every hour. %s forgets the $30."
                     % (eq(10, 30, "h", "C"), eq(30, 10, "h", "C"), eq(40, 0, "h", "C"), eq(10, 0, "h", "C")),
                     [0, 1, 2], [30, 40, 50], x="h", y="C"))
    its.append(nmcq("A snowshoe rental costs $30 plus $10 for each hour. How much does it cost for 4 hours?", 70, [160, 40, 130],
                    "<i>C</i> = 10 × 4 + 30 = 40 + 30 = <b>$70</b>. $160 adds first: (30 + 10) × 4. "
                    "$40 forgets the $30. $130 swaps the numbers: 30 × 4 + 10.", dol))
    assert (90 - 30) / 10 == 6
    its.append(nmcq("A snowshoe rental costs $30 plus $10 for each hour. Simran has $90. For how many hours can she rent snowshoes?",
                    6, [9, 12, 60],
                    "Solve 10<i>h</i> + 30 = 90. Take off the $30: 90 − 30 = 60. Then 60 ÷ 10 = <b>6 hours</b>. "
                    "9 hours forgets the $30. 12 hours adds the $30. 60 is dollars, not hours.", units("hours")))
    assert -2 * 5 + 3 == -7
    its.append(nmcq("At 4:00 p.m. it is 3 °C on Whistler Mountain. The temperature falls 2 °C each hour. "
                    "What is the temperature at 9:00 p.m.?", -7, [13, 7, -5],
                    "From 4:00 to 9:00 is 5 hours. <i>T</i> = −2 × 5 + 3 = −10 + 3 = <b>−7 °C</b>. "
                    "13 °C adds instead of subtracting. 7 °C forgets the answer is below zero. −5 °C is after 4 hours.",
                    units("°C")))
    its.append(eqmcq("At 4:00 p.m. it is 3 °C on Whistler Mountain. The temperature falls 2 °C each hour. "
                     "Which equation gives the temperature, <i>T</i>, in °C, <i>h</i> hours after 4:00 p.m.?",
                     (-2, 3), [(2, 3), (3, -2), (-2, -3)],
                     "The start is 3 °C, so the initial value is 3. The temperature falls, so the rate is −2: <b>%s</b>. "
                     "%s makes it warmer each hour. %s swaps the rate and the initial value. %s starts below zero."
                     % (eq(-2, 3, "h", "T"), eq(2, 3, "h", "T"), eq(3, -2, "h", "T"), eq(-2, -3, "h", "T")),
                     [0, 1, 2], [3, 1, -1], x="h", y="T"))
    assert -2 * 6 + 3 == -9
    its.append(mcq("At 4:00 p.m. it is 3 °C on Whistler Mountain, and the temperature falls 2 °C each hour. "
                   "At what time is it −9 °C?", "10:00 p.m.", ["7:00 p.m.", "4:00 a.m.", "8:30 p.m."],
                   "It must fall from 3 °C to −9 °C, which is 12 degrees. 12 ÷ 2 = 6 hours after 4:00 p.m.: <b>10:00 p.m.</b> "
                   "7:00 p.m. uses 9 − 3 = 6 degrees, as if −9 were 9. 4:00 a.m. forgets to divide by 2. "
                   "8:30 p.m. uses only 9 ÷ 2."))
    assert -3 * 7 == -21
    its.append(nmcq("A diver in Howe Sound starts at the surface (0 m) and goes down 3 m each minute. Her depth is a negative "
                    "number of metres. What is her depth after 7 minutes?", -21, [21, -24, -10],
                    "<i>d</i> = −3<i>m</i>. For 7 minutes: −3 × 7 = <b>−21 m</b>. 21 m forgets that below the surface is negative. "
                    "−24 m is after 8 minutes. −10 m adds −3 and −7 instead of multiplying.", units("m")))
    assert 40 + 15 * 12 == 220
    its.append(nmcq("Arjun has $40. He saves $15 each week for a bike that costs $220. After how many weeks can he buy it?",
                    12, [180, 11, 13],
                    "Solve 15<i>w</i> + 40 = 220. He still needs 220 − 40 = $180, and 180 ÷ 15 = <b>12 weeks</b>. "
                    "180 is the money he still needs, not weeks. After 11 weeks he has $205. 13 weeks is one week more than needed.",
                    units("weeks")))
    assert 10 + 5 * 8 == 50
    its.append(nmcq("For the Terry Fox Run, Kai’s aunt pledges $10 plus $5 for each kilometre he runs. "
                    "How much does she give if Kai runs 8 km?", 50, [120, 40, 85],
                    "<i>P</i> = 5 × 8 + 10 = 40 + 10 = <b>$50</b>. $120 adds first: (10 + 5) × 8. "
                    "$40 forgets the $10. $85 swaps the numbers: 10 × 8 + 5.", dol))
    assert 10 + 5 * 9 == 55
    its.append(nmcq("For the Terry Fox Run, Kai’s aunt pledges $10 plus $5 for each kilometre. She gives $55. How far did Kai run?",
                    9, [11, 13, 45],
                    "Solve 5<i>k</i> + 10 = 55. 55 − 10 = 45, and 45 ÷ 5 = <b>9 km</b>. "
                    "11 km is 55 ÷ 5 and forgets the $10. 13 km adds the $10. 45 forgets to divide.", units("km")))
    assert 20 + 10 * 3 == 8 + 14 * 3 == 50
    its.append(nmcq("In Victoria, Shop A rents kayaks for $20 plus $10 for each hour. Shop B charges $8 plus $14 for each hour. "
                    "After how many hours do both shops cost the same?", 3, [12, 4, 50],
                    "Make a table or set them equal: 10<i>h</i> + 20 = 14<i>h</i> + 8. Then 12 = 4<i>h</i>, so <i>h</i> = <b>3</b>. "
                    "Both cost $50. 12 is the difference in start fees and 4 is the difference in hourly rates. 50 is the cost.",
                    units("hours")))
    assert 1200 - 15 * 20 == 900
    its.append(nmcq("Mei starts a hike near Kamloops at a height of 1200 m. On the way down she loses 15 m of height each minute. "
                    "What is her height after 20 minutes?", 900, [1500, 300, 885],
                    "<i>H</i> = −15 × 20 + 1200 = −300 + 1200 = <b>900 m</b>. 1500 m adds the 300 m, but she is going down. "
                    "300 m is how much height she lost. 885 m is after 21 minutes.", units("m")))
    assert 180 - 12 * 10 == 60
    its.append(nmcq("A rain barrel in Nanaimo holds 180 L. In a dry week, Liam uses 12 L each day for the garden. "
                    "After how many days are 60 L left?", 10, [5, 15, 20],
                    "Solve −12<i>d</i> + 180 = 60. He uses 180 − 60 = 120 L, and 120 ÷ 12 = <b>10 days</b>. "
                    "5 is 60 ÷ 12. 15 is when the barrel is empty. 20 adds 180 + 60.", units("days")))
    xs, ys = [0, 1, 2, 3], [6, 2, -2, -6]
    T = tbl(xs, ys, heads=("Hours", "Temperature (°C)"), label="table of values: hours and temperature")
    its.append(eqmcq(T + "A cold front reaches Prince George. The table shows the temperature after <i>h</i> hours. "
                     "Which equation gives the temperature, <i>T</i>?", (-4, 6), [(4, 6), (-4, 2), (6, -4)],
                     "The temperature falls 4 °C each hour, so the rate is −4. At 0 hours it is 6 °C: <b>%s</b>. "
                     "%s makes it warmer each hour. %s uses the temperature after 1 hour as the start. %s swaps the numbers."
                     % (eq(-4, 6, "h", "T"), eq(4, 6, "h", "T"), eq(-4, 2, "h", "T"), eq(6, -4, "h", "T")),
                     xs, ys, x="h", y="T"))
    assert -4 * 5 + 6 == -14
    its.append(nmcq(T + "The temperature keeps falling in the same way. What is it after 5 hours?", -14, [26, -10, 14],
                    "<i>T</i> = −4 × 5 + 6 = −20 + 6 = <b>−14 °C</b>. 26 °C uses a rate of +4. −10 °C is after 4 hours. "
                    "14 °C forgets the answer is below zero.", units("°C")))
    assert -30 + 3 * 6 == -12
    its.append(nmcq("Nadia is diving at −30 m. She swims up 3 m each minute. What is her depth after 6 minutes?", -12,
                    [-48, 12, -15],
                    "<i>d</i> = 3<i>m</i> − 30. For 6 minutes: 18 − 30 = <b>−12 m</b>. −48 m goes down instead of up. "
                    "12 m would be above the water. −15 m is after 5 minutes.", units("m")))
    assert -30 + 3 * 10 == 0
    its.append(nmcq("Nadia is diving at −30 m. She swims up 3 m each minute. After how many minutes does she reach the surface (0 m)?",
                    10, [30, 9, 11],
                    "Solve 3<i>m</i> − 30 = 0. She must rise 30 m, and 30 ÷ 3 = <b>10 minutes</b>. "
                    "30 is metres, not minutes. After 9 minutes she is still at −3 m. 11 minutes is one too many.",
                    units("minutes")))
    assert 2 * 15 + 10 == 40
    its.append(nmcq("A school theatre in Surrey has 12 seats in row 1, and each row has 2 more seats than the row before. "
                    "How many seats are in row 15?", 40, [42, 30, 38],
                    "The rule is <i>s</i> = 2<i>r</i> + 10 (row 0 would have 12 − 2 = 10). For row 15: 2 × 15 + 10 = <b>40</b>. "
                    "42 uses 12 as the initial value. 30 forgets the 10. 38 is row 14."))
    assert 2 * 20 + 10 == 50
    its.append(nmcq("A school theatre has 12 seats in row 1, and each row has 2 more seats than the row before. "
                    "Which row has 50 seats?", 20, [19, 25, 21],
                    "Solve 2<i>r</i> + 10 = 50. 50 − 10 = 40, and 40 ÷ 2 = <b>20</b>. "
                    "19 uses 12 as the initial value: (50 − 12) ÷ 2. 25 forgets the 10. 21 is one row too many.",
                    lambda v: "Row " + n(v)))
    assert 10 * 4 + 30 == 70 and 10 * 8 + 30 == 110
    its.append(mcq("A snowshoe rental costs <i>C</i> = 10<i>h</i> + 30 dollars. Ethan says 8 hours costs twice as much as 4 hours. "
                   "Is he right?", "No: 4 hours is $70 and 8 hours is $110",
                   ["Yes: 8 hours is $140", "Yes: the rate is the same", "No: 8 hours is $80"],
                   "4 hours: 10 × 4 + 30 = $70. 8 hours: 10 × 8 + 30 = $110, not 2 × 70 = $140. "
                   "<b>No</b>: the $30 is paid only once, so doubling the hours does not double the cost. $80 forgets the $30."))
    return {"title": "Linear relation word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    G = Grid(6)
    for x, y in rel_pts(3, -2, range(-1, 3)):
        G.point(x, y)
    return (
        "<h2>Tables of values</h2>"
        "<p>A <b>linear relation</b> changes by the same amount each time %s goes up by 1. "
        "That amount is the <b>constant rate</b>. The <b>initial value</b> is the value of %s when %s = 0. "
        "In %s = <i>a</i>%s + <i>b</i>, <i>a</i> is the rate and <i>b</i> is the initial value.</p>"
        "<p>To fill in a table, put each %s into the equation. Multiply first, then add or subtract. "
        "Take care with negative numbers: −2 × (−3) = +6.</p>" % (X, Y, X, Y, X, X)
        + table([X, "−1", "0", "1", "2"], [[Y, "−5", "−2", "1", "4"]]) +
        "<p>This table is for %s. The values go up by 3 each time.</p>" % eq(3, -2) +
        "<h2>Write the equation from a table</h2>"
        + ex("Equation for −5, −2, 1, 4", "Write an equation for the table above.",
             "Find the rate: −2 − (−5) = 3. Find the initial value: in the column %s = 0, %s = −2. "
             "Check %s = 2: 3 × 2 − 2 = 4." % (X, Y, X), eq(3, -2))
        + ex("A relation that goes down", "A table has (0, 5), (1, 3), (2, 1). Write the equation.",
             "The values go down by 2, so the rate is <b>negative</b>: −2. The initial value is 5.", eq(-2, 5))
        + ex("When x skips numbers", "A table has (0, −3), (2, 1), (4, 5). What is the rate?",
             "%s goes up by 2 and %s goes up by 4. Divide: 4 ÷ 2 = 2. The equation is %s." % (X, Y, eq(2, -3)), "2") +
        "<h2>Graph in four quadrants</h2>"
        "<p>Each column of the table is a point (%s, %s). Go <b>across</b> for %s first (right if positive, left if negative), "
        "then <b>up or down</b> for %s. The points lie in a straight line. "
        "When only whole numbers make sense, the relation is <b>discrete</b>: plot the points and do not join them.</p>" % (X, Y, X, Y)
        + "<figure class='sn-fig'>" + G.svg("graph of y = 3x − 2 for x from −1 to 2") +
        "<figcaption>The points (−1, −5), (0, −2), (1, 1), (2, 4) of %s. Each step right goes up 3.</figcaption></figure>" % eq(3, -2) +
        "<h2>Interpret a graph</h2>"
        "<p>The initial value is where the points cross the %s-axis. If the points go <b>up</b> from left to right, "
        "the rate is positive. If they go <b>down</b>, the rate is negative, even when the values are positive.</p>" % Y
        + ex("Snowshoe rental", "A rental costs $30 plus $10 for each hour. How long can you rent for $90?",
             "The equation is <i>C</i> = 10<i>h</i> + 30. Solve 10<i>h</i> + 30 = 90. Subtract 30: 10<i>h</i> = 60. "
             "Divide by 10: <i>h</i> = 6.", "6 hours") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Plotting (%s, %s): putting (−5, −1) for the point (−1, −5)" % (Y, X), "Across for %s first, then up or down for %s" % (X, Y)],
            ["Giving a relation that goes down a positive rate: %s for 5, 3, 1" % eq(2, 5),
             "Values go down, so the rate is negative: %s" % eq(-2, 5)],
            ["Thinking negative values mean the rate is negative", "Look at the direction: −5, −2, 1, 4 goes up, so the rate is +3"],
            ["Using the first column as the initial value when it is not %s = 0" % X, "Find %s when %s = 0, or go back step by step" % (Y, X)],
            ["Using the change in %s when %s skips numbers" % (Y, X), "Divide the change in %s by the change in %s" % (Y, X)],
            ["Making −2 × (−3) negative", "A negative times a negative is positive: +6"],
        ])
    )


FAQ = [
    {"q": "What are linear relations in Grade 8 math in BC?",
     "a": "In the BC Grade 8 curriculum, students work with discrete linear relations using integers and larger numbers. They make tables of values, write equations like y = 3x − 2, graph the points in all four quadrants and interpret the graphs."},
    {"q": "How do you write an equation from a table of values?",
     "a": "Find the constant rate: the change in y divided by the change in x. Then find the initial value, the value of y when x = 0. For −5, −2, 1, 4 at x = −1, 0, 1, 2, the rate is 3 and the initial value is −2, so y = 3x − 2."},
    {"q": "How do you graph a linear relation with negative numbers?",
     "a": "Make a table of values, then plot each pair (x, y): go left or right for x first, then up or down for y. A negative x goes left and a negative y goes down."},
    {"q": "What does a negative rate mean on a graph?",
     "a": "A negative rate means y goes down as x goes up, so the points fall from left to right. The sign of the rate comes from the direction of the points, not from whether the values are negative."},
]


def gen():
    rnd = random.Random(58808)
    sets = [set_tables(), set_equations(), set_plot(), set_interpret(), set_words()]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            assert it["q"] not in allk, it["q"]
            allk.add(it["q"])
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "linear-relations",
        "sort": 8, "updated": UPDATED, "pdf_url": "",
        "title": "Linear Relations: Tables, Equations and Graphs in Four Quadrants",
        "seo_title": "Grade 8 Linear Relations Worksheets: Tables, Equations and Graphs (BC Math, Free)",
        "short_title": "Linear relations",
        "domain": "Patterning",
        "standard_code": "Grade 8: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Discrete linear relations (extended to larger numbers, limited to integers)",
        "meta_desc": "Free Grade 8 math worksheets on discrete linear relations for the BC curriculum: tables of values with integers, equations like y = 3x − 2 from tables, graphing in all four quadrants, reading graphs, and word problems. 100 questions with an answer key.",
        "key_big": "In y = ax + b, the rate a is how much y changes each time x goes up by 1, and b is y when x = 0. If the values go down, the rate is negative.",
        "key_sub": "For −5, −2, 1, 4 at x = −1, 0, 1, 2, the values go up by 3 and y = −2 when x = 0, so y = 3x − 2. To graph it, plot (x, y): across for x first, then up or down for y.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(graph|four graphs|shape pattern|table of values)")


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
