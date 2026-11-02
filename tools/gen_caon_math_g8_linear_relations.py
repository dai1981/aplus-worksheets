# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Linear relations (Ontario Curriculum 2020, Algebra C1.1, C1.2, C1.3)
  python3 tools/gen_caon_math_g8_linear_relations.py
Constant rate and initial value (including negative and decimal rates), linear growing and shrinking
patterns, the equation from a table of values (y = −2x + 10), graphs of linear relations (points and
lines, negative values, discrete and continuous), solving for unknown values, and word problems
(a cooling drink, a bike rental, a transit card, a draining pool, a falling temperature).
Wrong answers come from real mistakes: the sign of the rate in shrinking patterns, the first value used as
the initial value, the change in y used without dividing by the change in x, mixing up x and y, plotting
(y, x), undoing operations in the wrong order, dividing by the rate without the sign, and off-by-one jumps.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
BLUE = "#1f5f99"
INK = "#2b2b2b"
GRID = "#c9d6cd"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NB = " "


# ------------------------------------------------------------ numbers
def n(v):
    """Ontario/SI style: 4536, 12 000 (no-break space), decimals with a point, real minus sign."""
    v = Fr(v)
    neg = v < 0
    v = abs(v)
    for k in range(0, 5):
        t = v * 10 ** k
        if t.denominator == 1:
            w, r = divmod(t.numerator, 10 ** k)
            s = str(w)
            if len(s) >= 5:
                g = []
                while s:
                    g.insert(0, s[-3:])
                    s = s[:-3]
                s = NB.join(g)
            if k:
                s += "." + str(r).rjust(k, "0")
            return (MINUS if neg else "") + s
    raise ValueError(v)


def frac(v):
    """Whole numbers and terminating decimals as numbers; other fractions as a stacked fraction."""
    v = Fr(v)
    if v.denominator == 1:
        return n(v)
    return (MINUS if v < 0 else "") + ("<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>"
                                       % (abs(v.numerator), v.denominator))


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1 and v >= 0, v
    w, r = divmod(c.numerator, 100)
    return "$%s.%02d" % (n(w), r)


def dol(v):
    v = Fr(v)
    assert v.denominator == 1 and v >= 0
    return "$" + n(v)


def units(u):
    return lambda v: "%s%s%s" % (n(v), NB if u.startswith("°") else " ", u)


def plain(s):
    return re.sub(r"<[^>]+>", "", s).replace(NB, " ")


def lst(xs):
    return ", ".join(n(x) for x in xs)


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
    elif a.denominator == 1 or (a * 10000).denominator == 1 and a.denominator in (2, 4, 5, 10, 20, 25, 50, 100):
        s = n(a) + I(x)
    else:
        s = frac(a) + I(x)
    if b > 0:
        s += " + " + n(b)
    elif b < 0:
        s += " " + MINUS + " " + n(-b)
    return s


def eq(a, b, x="x", y="y"):
    return I(y) + " = " + rhs(a, b, x)


def lv(a, b, x):
    return Fr(a) * Fr(x) + Fr(b)


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


# ---- shape patterns
T = 14


def tile(x, y, col=CUBE):
    return "<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (
        x, y, T, T, col, GREEN)


def stick(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L * 2.5, dy / L * 2.5
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
            % (x1 + ux, y1 + uy, x2 - ux, y2 - uy, STICK))


SQ = 24


def squares(k):
    def draw(x, y):
        s = [stick(x + i * SQ, y, x + i * SQ, y + SQ) for i in range(k + 1)]
        for i in range(k):
            s.append(stick(x + i * SQ, y, x + (i + 1) * SQ, y))
            s.append(stick(x + i * SQ, y + SQ, x + (i + 1) * SQ, y + SQ))
        return "".join(s)
    return k * SQ, SQ, draw


def towers3(k):
    def draw(x, y):
        return "".join(tile(x + i * (T + 5), y + j * T) for i in range(k + 1) for j in range(3))
    return (k + 1) * T + k * 5, 3 * T, draw


def shrink2(k):
    """Two rows of tiles that lose one column each figure: 10, 8, 6, ..."""
    c = 6 - k

    def draw(x, y):
        return "".join(tile(x + i * T, y + j * T) for i in range(c) for j in range(2))
    return c * T, 2 * T, draw


PATTERNS = {
    "sq": (squares, lambda k: 3 * k + 1, "sticks"),
    "towers": (towers3, lambda k: 3 * k + 3, "cubes"),
    "shrink": (shrink2, lambda k: 12 - 2 * k, "tiles"),
}


def cnt(nm, k):
    return PATTERNS[nm][1](k)


def pattern_svg(nm, steps=(1, 2, 3), hide=None):
    drawer = PATTERNS[nm][0]
    parts = [drawer(k) for k in steps]
    m, gap, lab = 8, 26, 24
    hmax = max(max(h for _, h, _ in parts), 36)
    widths = [max(w, 62) for w, _, _ in parts]
    W = 2 * m + sum(widths) + gap * (len(parts) - 1)
    H = m + hmax + 8 + lab
    s, x = [], m
    for k, (w, h, draw), cw in zip(steps, parts, widths):
        if k == hide:
            bw, bh = 46, min(hmax, 46)
            bx, by = x + (cw - bw) / 2, m + hmax - bh
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
                     "stroke-dasharray='4 3'/>" % (bx, by, bw, bh, FILL, GREEN))
            s.append(text(bx + bw / 2, by + bh / 2 + 7, "?", 20, col=RED))
        else:
            s.append(draw(x + (cw - w) / 2, m + hmax - h))
        s.append(text(x + cw / 2, m + hmax + 8 + 16, "Figure %d" % k, 14))
        x += cw + gap
    return svg_wrap(W, H, "".join(s), "shape pattern %s" % nm)


# ---- graphs
def graph_svg(pts, xmax, ymax, ymin=0, ystep=1, ylab=2, xname="x", yname="y", tags=None, seg=None,
              xlab=1, label="graph of a linear relation"):
    """Graph drawn exactly to the grid. ymin may be negative: the x-axis is then drawn at y = 0 and the
    x labels sit under the grid. seg = (x1, y1, x2, y2) draws a solid line (continuous relation)."""
    tags = tags or {}
    assert ymin % ylab == 0 and ymin % ystep == 0
    XU = 32 if xmax <= 7 else (24 if xmax <= 10 else 20)
    PH = 210.0
    YU = PH / (ymax - ymin)
    ylabels = [(gy, n(gy)) for gy in range(ymin, ymax + 1, ylab)]
    LW = max(tw(t, 14) for _, t in ylabels)
    yn_long = len(yname) > 1
    L = (34 if yn_long else 24) + LW + 8
    Tm, R, B = 16, 18, 50
    X0 = L
    Y = lambda v: Tm + (ymax - Fr(v)) * Fr(YU)
    Yb = float(Y(ymin))
    W = L + xmax * XU + R
    H = Yb + B
    s = []
    for gy in range(ymin, ymax + 1, ystep):
        y = float(Y(gy))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + xmax * XU, y, GRID))
    for gy, t in ylabels:
        s.append(text(X0 - 7, float(Y(gy)) + 5, t, 14, "end", bold=False))
    for gx in range(0, xmax + 1):
        x = X0 + gx * XU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, Tm, x, Yb, GRID))
        if gx % xlab == 0:
            s.append(text(x, Yb + 19, n(gx), 14, bold=False))
    ya = float(Y(0))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, ya, X0 + xmax * XU, ya, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Tm, X0, Yb, INK))
    xn = SX(xname) if len(xname) == 1 else xname
    yn = SX(yname) if len(yname) == 1 else yname
    s.append(text(X0 + xmax * XU / 2, H - 8, xn, 15 if len(xname) > 1 else 17))
    if yn_long:
        cy = (Tm + Yb) / 2
        s.append(text(16, cy, yn, 15, extra=" transform='rotate(-90 16 %.1f)'" % cy))
    else:
        s.append(text(X0 - LW - 16, (Tm + Yb) / 2 + 6, yn, 17))
    if seg:
        x1, y1, x2, y2 = seg
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                 % (X0 + x1 * XU, float(Y(y1)), X0 + x2 * XU, float(Y(y2)), RED))
    for px, py in pts:
        assert 0 <= px <= xmax and ymin <= py <= ymax, (px, py)
        cx, cy = float(X0 + Fr(px) * XU), float(Y(py))
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
        if (px, py) in tags:
            s.append("<rect x='%.1f' y='%.1f' width='16' height='18' fill='#ffffff' opacity='0.85'/>" % (cx + 5, cy - 24))
            s.append(text(cx + 13, cy - 10, tags[(px, py)], 16, col=GREEN))
    return svg_wrap(W, H, "".join(s), label)


def panels_svg(groups, label):
    """Four small graphs A, B, C, D (x and y from 0 to 8) in one picture."""
    U, N = 13, 8
    PL, PT, PB, PR, GAP = 24, 26, 22, 10, 14
    PW = PL + U * N + PR
    W = 4 + 4 * PW + 3 * GAP
    H = PT + U * N + PB + 2
    s = []
    for i, pts in enumerate(groups):
        ox = 2 + i * (PW + GAP)
        X0, Y0 = ox + PL, PT + U * N
        s.append(text(ox + PL + U * N / 2, 18, "ABCD"[i], 17, col=GREEN))
        for g in range(N + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (X0 + g * U, PT, X0 + g * U, Y0, GRID))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (X0, Y0 - g * U, X0 + N * U, Y0 - g * U, GRID))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + N * U, Y0, INK))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X0, PT, X0, Y0, INK))
        for g in range(2, N + 1, 2):
            s.append(text(X0 + g * U, Y0 + 16, str(g), 14, bold=False))
            s.append(text(X0 - 4, Y0 - g * U + 5, str(g), 14, "end", bold=False))
        for px, py in pts:
            assert 0 <= px <= N and 0 <= py <= N
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X0 + px * U, Y0 - py * U, RED))
    return svg_wrap(W, H, "".join(s), label)


def slope(xs, ys):
    """Constant rate of a table, checked to be constant."""
    r = {(Fr(ys[i + 1]) - Fr(ys[i])) / (Fr(xs[i + 1]) - Fr(xs[i])) for i in range(len(xs) - 1)}
    assert len(r) == 1, (xs, ys)
    return r.pop()


GRAPHS = ["Graph A", "Graph B", "Graph C", "Graph D"]


# ============================================================ set 1: constant rate and initial value
def set_rate():
    its = []
    xs, ys = [0, 1, 2, 3, 4], [3, 7, 11, 15, 19]
    assert slope(xs, ys) == 4
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", 4, [3, 7, 1],
                    "Each time <i>x</i> goes up by 1, <i>y</i> goes up by the same amount: 7 − 3 = 4 and 11 − 7 = 4. "
                    "The constant rate is <b>4</b>. 3 is the initial value and 7 is the value when <i>x</i> = 1. 1 is the change in <i>x</i>, not in <i>y</i>."))
    xs, ys = [1, 2, 3, 4], [8, 13, 18, 23]
    assert slope(xs, ys) == 5
    its.append(nmcq(tbl(xs, ys) + "What is the initial value (the value of <i>y</i> when <i>x</i> = 0)?", 3, [8, 5, 13],
                    "The rate is 5. Go back one step from <i>x</i> = 1 to <i>x</i> = 0: 8 − 5 = <b>3</b>. "
                    "8 is the value when <i>x</i> = 1, not when <i>x</i> = 0, and 13 is the value when <i>x</i> = 2. 5 is the constant rate."))
    xs, ys = [0, 1, 2, 3, 4], [20, 17, 14, 11, 8]
    assert slope(xs, ys) == -3
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", -3, [3, 20, 17],
                    "17 − 20 = −3 and 14 − 17 = −3. The values go down, so the rate is negative: <b>−3</b>. "
                    "3 forgets the sign. In a shrinking pattern the rate is always negative. 20 is the initial value and 17 is the value when <i>x</i> = 1."))
    xs, ys = [1, 2, 3, 4], [26, 22, 18, 14]
    assert slope(xs, ys) == -4
    its.append(nmcq(tbl(xs, ys) + "What is the initial value of this linear relation?", 30, [26, 22, -4],
                    "The rate is −4. Going back one step from <i>x</i> = 1 does the opposite, so <b>add</b> 4: 26 + 4 = <b>30</b>. "
                    "22 subtracts 4 again, but that is the value for <i>x</i> = 2. 26 is the value for <i>x</i> = 1. −4 is the rate."))
    its.append(nmcq("What is the constant rate of %s?" % eq(5, -2), 5, [-2, 3, 8],
                    "In <i>y</i> = <i>a</i><i>x</i> + <i>b</i>, the number that multiplies <i>x</i> is the constant rate: <b>5</b>. "
                    "−2 is the initial value. 3 and 8 are the values of <i>y</i> when <i>x</i> = 1 and 2."))
    its.append(nmcq("What is the constant rate of %s?" % eq(-4, 9), -4, [4, 9, 5],
                    "The number that multiplies <i>x</i> is <b>−4</b>, so <i>y</i> goes down by 4 each time <i>x</i> goes up by 1. "
                    "4 drops the negative sign. 9 is the initial value. 5 is the value of <i>y</i> when <i>x</i> = 1."))
    its.append(nmcq("What is the initial value of %s?" % eq(-4, 9), 9, [-4, 5, 13],
                    "When <i>x</i> = 0, −4 × 0 = 0, so <i>y</i> = <b>9</b>. "
                    "−4 is the constant rate. 5 is the value of <i>y</i> when <i>x</i> = 1. 13 is 4 + 9, which treats the rate as +4."))
    its.append(nmcq("The relation <i>y</i> = 12 − 3<i>x</i> is written with the <i>x</i>-term last. What is its constant rate?",
                    -3, [3, 12, 9],
                    "12 − 3<i>x</i> is the same as −3<i>x</i> + 12. The rate is <b>−3</b>: each time <i>x</i> goes up by 1, "
                    "3 more is taken away. 3 forgets the minus sign in front of 3<i>x</i>. 12 is the initial value and 9 is the value when <i>x</i> = 1."))
    its.append(eqmcq("A linear relation has an initial value of 6 and a constant rate of −2. Which equation shows it?",
                     (-2, 6), [(6, -2), (2, 6), (-2, -6)],
                     "The rate multiplies <i>x</i> and the initial value is added: <b>%s</b>. "
                     "%s swaps the rate and the initial value. %s has a growing rate, but −2 means the values shrink."
                     % (eq(-2, 6), eq(6, -2), eq(2, 6)), [0, 1, 2], [6, 4, 2]))
    xs, ys = [0, 1, 2, 3], [2, Fr(11, 4), Fr(7, 2), Fr(17, 4)]
    assert slope(xs, ys) == Fr(3, 4)
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", Fr(3, 4), [2, Fr(9, 4), Fr(11, 4)],
                    "2.75 − 2 = 0.75 and 3.5 − 2.75 = 0.75. The rate is <b>0.75</b>. "
                    "2.25 is the total change from <i>x</i> = 0 to <i>x</i> = 3: divide it by 3 steps. 2 is the initial value and 2.75 is the value when <i>x</i> = 1."))
    xs, ys = [0, 1, 2, 3], [-6, -4, -2, 0]
    assert slope(xs, ys) == 2
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", 2, [-2, -6, -4],
                    "−4 − (−6) = −4 + 6 = 2. The values go up (−6, −4, −2, 0), so the rate is <b>2</b>. "
                    "−2 comes from seeing negative numbers and thinking the pattern shrinks. −6 is the initial value and −4 is the value when <i>x</i> = 1."))
    xs, ys = [0, 2, 4, 6], [5, 11, 17, 23]
    assert slope(xs, ys) == 3
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", 3, [6, 5, 2],
                    "<i>x</i> goes up by 2 each time and <i>y</i> goes up by 6. The rate is the change for each 1: "
                    "6 ÷ 2 = <b>3</b>. 6 forgets that <i>x</i> skips numbers. 5 is the initial value. 2 is the change in <i>x</i>."))
    xs, ys = [0, 3, 6, 9], [40, 31, 22, 13]
    assert slope(xs, ys) == -3
    its.append(nmcq(tbl(xs, ys) + "What is the constant rate of this linear relation?", -3, [-9, 3, 9],
                    "<i>x</i> goes up by 3 and <i>y</i> goes down by 9. The rate is −9 ÷ 3 = <b>−3</b>. "
                    "−9 forgets to divide by the change in <i>x</i>. 3 and 9 forget that the values go down."))
    its.append(mcq("For <i>x</i> = 0, 1, 2, 3, which list of <i>y</i>-values makes a linear relation?", "10, 7, 4, 1",
                   ["1, 2, 4, 8", "10, 8, 5, 1", "0, 1, 4, 9"],
                   "A linear relation changes by the same amount each step. 10, 7, 4, 1 goes down by 3 every time, so it is "
                   "<b>linear</b>. 10, 8, 5, 1 goes down by 2, 3, 4: the steps change. 1, 2, 4, 8 doubles."))
    its.append(mcq("Which equation shows a shrinking pattern?", eq(-2, 20),
                   [eq(2, -20), eq(2, 20), eq(Fr(1, 2), -3)],
                   "A pattern shrinks when the constant rate (the number times <i>x</i>) is negative: <b>%s</b>. "
                   "%s has a minus sign, but it is on the initial value. Its rate is +2, so it grows." % (eq(-2, 20), eq(2, -20))))
    its.append(mcq("In %s, what does the 8 tell you?" % eq(3, 8), "The value of <i>y</i> when <i>x</i> = 0",
                   ["<i>y</i> goes up by 8 each time", "The value of <i>y</i> when <i>x</i> = 1", "<i>x</i> goes up by 8 each time"],
                   "The number added on its own is the initial value: <b>the value of <i>y</i> when <i>x</i> = 0</b>. "
                   "The rate is 3, so <i>y</i> goes up by 3 each time. When <i>x</i> = 1, <i>y</i> = 11."))
    its.append(nmcq("For %s, how much does <i>y</i> change when <i>x</i> goes up by 2?" % eq(Fr(1, 2), 4), 1,
                    [Fr(1, 2), 2, 5],
                    "Each 1 that <i>x</i> goes up adds 0.5. For 2 steps: 2 × 0.5 = <b>1</b>. "
                    "0.5 is the change for one step only. 5 is the value of <i>y</i> when <i>x</i> = 2."))
    a, b = 3, 8
    assert lv(a, b, 2) == 14 and lv(a, b, 4) == 20
    its.append(nmcq("A linear relation has <i>y</i> = 14 when <i>x</i> = 2 and <i>y</i> = 20 when <i>x</i> = 4. "
                    "What is its initial value?", 8, [14, 11, 3],
                    "The rate is (20 − 14) ÷ (4 − 2) = 3. From <i>x</i> = 2 back to <i>x</i> = 0 is 2 steps: "
                    "14 − 2 × 3 = <b>8</b>. 11 goes back only one step. 14 is the value when <i>x</i> = 2, and 3 is the rate."))
    xs, ys = [1, 2, 3, 4], [-1, 3, 7, 11]
    assert slope(xs, ys) == 4
    its.append(nmcq(tbl(xs, ys) + "What is the initial value of this linear relation?", -5, [-1, 3, 5],
                    "The rate is 4. Go back one step from <i>x</i> = 1: −1 − 4 = <b>−5</b>. "
                    "3 adds 4 instead of subtracting. 5 loses the negative sign. −1 is the value for <i>x</i> = 1."))
    its.append(mcq("Relation P is %s. Relation Q is %s. Which statement is true?" % (eq(3, 10), eq(5, 2)),
                   "Q has the greater rate and P has the greater initial value",
                   ["P has the greater rate and Q has the greater initial value", "P has the greater rate and initial value",
                    "Q has the greater rate and initial value"],
                   "The rates are 3 and 5, so Q grows faster. The initial values are 10 and 2, so P starts higher. "
                   "<b>Q has the greater rate and P has the greater initial value.</b>"))
    return {"title": "Constant rate and initial value", "items": its}


# ============================================================ set 2: growing and shrinking patterns
def set_patterns():
    its = []
    v = [cnt("sq", k) for k in range(1, 7)]
    its.append(nmcq(fig(pattern_svg("sq")) + "The pattern continues. How many sticks are in Figure 5?", v[4], [20, 13, 19],
                    "Count: 4, 7, 10. Each figure adds 3 sticks: 10, 13, <b>16</b>. "
                    "20 is 5 × 4, but squares next to each other share a stick. 13 is Figure 4."))
    v = [cnt("shrink", k) for k in range(1, 6)]
    its.append(nmcq(fig(pattern_svg("shrink")) + "This pattern shrinks. How many tiles are in Figure 4?", v[3], [8, 5, 6],
                    "Count: 10, 8, 6. Each figure loses 2 tiles: 6 − 2 = <b>4</b>. "
                    "8 adds 2, but the pattern is shrinking. 5 takes away only 1. 6 is Figure 3."))
    assert cnt("shrink", 6) == 0
    its.append(mcq(fig(pattern_svg("shrink")) + "The pattern keeps shrinking. Which figure has 0 tiles?", "Figure 6",
                   ["Figure 5", "Figure 12", "Figure 10"],
                   "10, 8, 6, 4, 2, 0. <b>Figure 6</b> has no tiles. Check with the rule <i>y</i> = −2<i>x</i> + 12: "
                   "−2 × 6 + 12 = 0. Figure 5 still has 2 tiles. 12 is the initial value, not the figure number. 10 is the number of tiles in Figure 1."))
    xs, ys = [1, 2, 3, 4], [45, 41, 37, 33]
    a = slope(xs, ys)
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. What is <i>y</i> when <i>x</i> = 7?", lv(a, 49, 7), [25, 17, 45],
                    "<i>y</i> goes down by 4 each time: 33, 29, 25, <b>21</b>. "
                    "25 is the value for <i>x</i> = 6 and 17 is for <i>x</i> = 8. 45 adds 4 three times instead of subtracting."))
    xs, ys = [0, 1, 2, 3, 4, 5], [7, 4, 1, "?", -5, -8]
    its.append(nmcq(tbl(xs, ys) + "What value is missing from the table?", -2, [2, -1, 4],
                    "<i>y</i> goes down by 3 each time: 1 − 3 = <b>−2</b>. Check: −2 − 3 = −5. "
                    "2 forgets that 1 − 3 goes below zero. −1 takes away only 2. 4 is the value for <i>x</i> = 1."))
    v = [cnt("towers", k) for k in (1, 2, 3)]
    its.append(nmcq(fig(pattern_svg("towers", hide=2)) + "Figure 2 is hidden. How many cubes are in Figure 2?", v[1],
                    [18, 8, 12],
                    "Figure 1 has 6 cubes and Figure 3 has 12. The change is the same each time, so 12 − 6 = 6 is two steps "
                    "of 3: 6, <b>9</b>, 12. 18 adds Figures 1 and 3. 8 adds only 2. 12 is Figure 3."))
    xs, ys = [1, 2, 3, 4], [200, 185, 170, 155]
    a = slope(xs, ys)
    assert a == -15 and lv(a, 215, 10) == 65
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. What is <i>y</i> when <i>x</i> = 10?", 65, [50, 350, 80],
                    "The rate is −15. From <i>x</i> = 1 to <i>x</i> = 10 is 9 steps: 200 − 9 × 15 = 200 − 135 = <b>65</b>. "
                    "50 takes 10 steps. 80 is the value for <i>x</i> = 9. 350 adds 15 each time instead of subtracting."))
    xs, ys = [1, 2, 3, 4], [7, 12, 17, 22]
    assert slope(xs, ys) == 5 and lv(5, 2, 12) == 62
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. For which value of <i>x</i> is <i>y</i> = 62?", 12, [62, 13, 11],
                    "The rule is <i>y</i> = 5<i>x</i> + 2. Solve 5<i>x</i> + 2 = 62: 62 − 2 = 60 and 60 ÷ 5 = <b>12</b>. "
                    "62 is the value of <i>y</i>, not <i>x</i>. 13 and 11 are one step off."))
    xs, ys = [1, 2, 3, 4], [50, 46, 42, 38]
    assert slope(xs, ys) == -4 and lv(-4, 54, 11) == 10
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. For which value of <i>x</i> is <i>y</i> = 10?", 11, [10, 16, 12],
                    "The rule is <i>y</i> = −4<i>x</i> + 54. Solve −4<i>x</i> + 54 = 10: 54 − 10 = 44 and 44 ÷ 4 = <b>11</b>. "
                    "10 uses 50 as the initial value: (50 − 10) ÷ 4. 16 adds instead: (54 + 10) ÷ 4. 12 is one step too many."))
    bad = [18, 15, 12, 8, 6]
    assert [18 - 3 * k for k in range(5)][3] == 9
    its.append(nmcq(tbl([0, 1, 2, 3, 4], bad) + "One value in this shrinking pattern is wrong. Which one?", 8, [15, 12, 6],
                    "The values go down by 3: 18, 15, 12, 9, 6. <b>8</b> should be 9."))
    xs, ys = [0, 1, 2, 3, 4], [Fr(5, 2), Fr(7, 4), 1, "?", Fr(-1, 2)]
    its.append(nmcq(tbl(xs, ys) + "What value is missing from the table?", Fr(1, 4), [Fr(-1, 4), Fr(1, 2), Fr(-1, 2)],
                    "2.5 − 1.75 = 0.75, so <i>y</i> goes down by 0.75 each time: 1 − 0.75 = <b>0.25</b>. "
                    "Check: 0.25 − 0.75 = −0.5. 0.5 takes away only 0.5. −0.25 takes away 1.25 instead of 0.75. −0.5 is the value for <i>x</i> = 4."))
    a, b = Fr(1, 2), Fr(1, 4)
    its.append(nmcq("A pattern has <i>y</i>-values " + ", ".join(frac(lv(a, b, k)) for k in range(4)) +
                    " for <i>x</i> = 0, 1, 2, 3. What is <i>y</i> when <i>x</i> = 6?", lv(a, b, 6),
                    [lv(a, b, 5), lv(a, b, 7), 3],
                    "Each step adds <span class='fr'><span class='fn'>2</span><span class='fd'>4</span></span>. "
                    "From <i>x</i> = 3 to 6 is 3 more steps: "
                    "<span class='fr'><span class='fn'>7</span><span class='fd'>4</span></span> + "
                    "<span class='fr'><span class='fn'>6</span><span class='fd'>4</span></span> = <b>"
                    "<span class='fr'><span class='fn'>13</span><span class='fd'>4</span></span></b>. "
                    "3 is 6 × <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> and forgets the "
                    "initial value <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>. <span class='fr'><span class='fn'>11</span><span class='fd'>4</span></span> and <span class='fr'><span class='fn'>15</span><span class='fd'>4</span></span> are the values for <i>x</i> = 5 and 7.", frac))
    xs, ys = [1, 2, 3, 4], [-11, -8, -5, -2]
    assert slope(xs, ys) == 3 and lv(3, -14, 8) == 10
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. What is <i>y</i> when <i>x</i> = 8?", 10, [7, 13, -14],
                    "−8 − (−11) = 3, so the values go up by 3: −2, 1, 4, 7, <b>10</b>. "
                    "7 is the value for <i>x</i> = 7 and 13 is for <i>x</i> = 9. "
                    "−14 subtracts 3 each time, but the values are growing."))
    assert lv(-4, 30, 6) == 6
    its.append(nmcq("When <i>x</i> = 0, <i>y</i> = 30. Each time <i>x</i> goes up by 1, <i>y</i> goes down by 4. "
                    "What is <i>y</i> when <i>x</i> = 6?", 6, [54, 10, 2],
                    "The rule is <i>y</i> = −4<i>x</i> + 30. −4 × 6 + 30 = −24 + 30 = <b>6</b>. "
                    "54 adds 4 each time. 10 is the value for <i>x</i> = 5 and 2 is for <i>x</i> = 7."))
    assert cnt("sq", 15) == 46
    its.append(mcq(fig(pattern_svg("sq")) + "The pattern continues. Which figure has 46 sticks?", "Figure 15",
                   ["Figure 46", "Figure 14", "Figure 16"],
                   "The rule is <i>y</i> = 3<i>x</i> + 1. Solve 3<i>x</i> + 1 = 46: 46 − 1 = 45 and 45 ÷ 3 = 15. "
                   "<b>Figure 15</b>. Figure 14 comes from (46 − 4) ÷ 3 = 14: that counts the jumps after Figure 1, so add 1. Figure 16 is one too many. "
                   "46 is the number of sticks."))
    assert cnt("sq", 10) == 31 and cnt("sq", 20) == 61
    its.append(nmcq(fig(pattern_svg("sq")) + "Figure 10 has 31 sticks. Mei says Figure 20 must have 2 × 31 = 62 sticks. "
                    "How many sticks does Figure 20 really have?", 61, [62, 60, 64],
                    "Use the rule <i>y</i> = 3<i>x</i> + 1: 3 × 20 + 1 = <b>61</b>. Doubling also doubles the initial value 1, "
                    "so 62 is 1 too many. 60 forgets the + 1. 64 is Figure 21."))
    assert lv(-6, 50, 8) == 2 and lv(-6, 50, 9) == -4
    its.append(nmcq("The relation is %s. What is the first whole number <i>x</i> that makes <i>y</i> negative?" % eq(-6, 50), 9,
                    [8, 6, 50],
                    "When <i>x</i> = 8, <i>y</i> = −48 + 50 = 2, still positive. When <i>x</i> = 9, <i>y</i> = −54 + 50 = −4. "
                    "The answer is <b>9</b>. 8 is the last positive value. 6 is the rate and 50 is the initial value."))
    assert lv(4, 3, 6) == lv(-2, 39, 6) == 27
    its.append(nmcq("Pattern A is %s. Pattern B is %s. For which value of <i>x</i> do they have the same <i>y</i>?"
                    % (eq(4, 3), eq(-2, 39)), 6, [27, 18, 9],
                    "Set them equal: 4<i>x</i> + 3 = −2<i>x</i> + 39. Add 2<i>x</i>: 6<i>x</i> + 3 = 39. "
                    "So 6<i>x</i> = 36 and <i>x</i> = <b>6</b>. Check: both give 27. 27 is <i>y</i>. "
                    "18 subtracts the rates (4 − 2) instead of adding them, because B shrinks. 9 divides 36 by 4."))
    xs, ys = [1, 3, 5, 9], [20, 14, 8, "?"]
    assert slope([1, 3, 5], [20, 14, 8]) == -3 and lv(-3, 23, 9) == -4
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. What is the missing value?", -4, [2, -1, 4],
                    "<i>x</i> goes up by 2 and <i>y</i> goes down by 6, so the rate is −3. From <i>x</i> = 5 to 9 is 4 steps: "
                    "8 − 4 × 3 = <b>−4</b>. 2 takes only one jump of 6, but <i>x</i> jumps from 5 to 9. "
                    "−1 is the value for <i>x</i> = 8. 4 forgets that the answer is below zero."))
    xs, ys = [0, 1, 2, 3], [Fr(-6, 5), Fr(-2, 5), Fr(2, 5), Fr(6, 5)]
    assert slope(xs, ys) == Fr(4, 5) and lv(Fr(4, 5), Fr(-6, 5), 5) == Fr(14, 5)
    its.append(nmcq(tbl(xs, ys) + "The pattern continues. What is <i>y</i> when <i>x</i> = 5?", Fr(14, 5),
                    [2, Fr(18, 5), Fr(-26, 5)],
                    "−0.4 − (−1.2) = 0.8, so <i>y</i> goes up by 0.8: 1.2, 2, <b>2.8</b>. 2 is the value for <i>x</i> = 4 "
                    "and 3.6 is for <i>x</i> = 6. −5.2 subtracts 0.8 each time, but the values grow."))
    return {"title": "Growing and shrinking linear patterns", "items": its}


# ============================================================ set 3: equation from a table
def set_equations():
    its = []
    Q = "Which equation matches the table?"

    def from_table(xs, ys, right, wrong, e):
        return eqmcq(tbl(xs, ys) + Q, right, wrong, e, xs, ys)

    its.append(from_table([0, 1, 2, 3], [4, 7, 10, 13], (3, 4), [(1, 3), (4, 3), (3, 7)],
                          "<i>y</i> goes up by 3, so the rate is 3. When <i>x</i> = 0, <i>y</i> = 4. The equation is <b>%s</b>. "
                          "%s swaps the rate and the initial value." % (eq(3, 4), eq(4, 3)) + " %s uses the value for <i>x</i> = 1, and %s uses only one column." % (eq(3, 7), eq(1, 3))))
    its.append(from_table([0, 1, 2, 3], [10, 8, 6, 4], (-2, 10), [(2, 10), (-2, 8), (10, -2)],
                          "<i>y</i> goes down by 2, so the rate is −2. When <i>x</i> = 0, <i>y</i> = 10. The equation is "
                          "<b>%s</b>. %s forgets that a shrinking pattern has a negative rate." % (eq(-2, 10), eq(2, 10))))
    its.append(from_table([1, 2, 3, 4], [5, 9, 13, 17], (4, 1), [(4, 5), (1, 4), (5, 4)],
                          "The rate is 4. Go back to <i>x</i> = 0: 5 − 4 = 1. The equation is <b>%s</b>. "
                          "%s uses the value for <i>x</i> = 1 as the initial value." % (eq(4, 1), eq(4, 5))))
    its.append(from_table([1, 2, 3, 4], [17, 14, 11, 8], (-3, 20), [(3, 14), (-3, 17), (20, -3)],
                          "The rate is −3. Going back to <i>x</i> = 0 adds 3: 17 + 3 = 20. The equation is <b>%s</b>. "
                          "%s uses 17 as the initial value. %s fits <i>x</i> = 1 but grows instead of shrinking."
                          % (eq(-3, 20), eq(-3, 17), eq(3, 14))))
    its.append(from_table([0, 1, 2, 3], [-5, -3, -1, 1], (2, -5), [(-2, -5), (2, 5), (-5, 2)],
                          "−3 − (−5) = 2, so the rate is 2. When <i>x</i> = 0, <i>y</i> = −5. The equation is <b>%s</b>. "
                          "%s sees negative numbers and makes the rate negative, but the values go up." % (eq(2, -5), eq(-2, -5))))
    its.append(from_table([0, 1, 2, 3], [6, 1, -4, -9], (-5, 6), [(5, 6), (-5, 1), (6, -5)],
                          "1 − 6 = −5, so the rate is −5. When <i>x</i> = 0, <i>y</i> = 6. The equation is <b>%s</b>. "
                          "%s uses the value for <i>x</i> = 1 as the initial value." % (eq(-5, 6), eq(-5, 1))))
    its.append(from_table([0, 2, 4, 6], [3, 11, 19, 27], (4, 3), [(8, 3), (1, 8), (4, 11)],
                          "<i>x</i> goes up by 2 and <i>y</i> goes up by 8, so the rate is 8 ÷ 2 = 4. When <i>x</i> = 0, "
                          "<i>y</i> = 3: <b>%s</b>. %s forgets that <i>x</i> skips numbers." % (eq(4, 3), eq(8, 3))))
    its.append(from_table([0, 5, 10, 15], [30, 20, 10, 0], (-2, 30), [(-10, 30), (2, 30), (-5, 30)],
                          "<i>x</i> goes up by 5 and <i>y</i> goes down by 10, so the rate is −10 ÷ 5 = −2. "
                          "The initial value is 30: <b>%s</b>. %s does not divide by 5. %s uses the change in <i>x</i> as the rate."
                          % (eq(-2, 30), eq(-10, 30), eq(-5, 30))))
    its.append(from_table([0, 1, 2, 3], [1, Fr(3, 2), 2, Fr(5, 2)], (Fr(1, 2), 1), [(1, Fr(1, 2)), (Fr(3, 2), 0), (Fr(1, 2), Fr(3, 2))],
                          "<i>y</i> goes up by 0.5, so the rate is 0.5. When <i>x</i> = 0, <i>y</i> = 1: <b>%s</b>. "
                          "%s swaps the rate and the initial value." % (eq(Fr(1, 2), 1), eq(1, Fr(1, 2)))))
    its.append(from_table([0, 1, 2, 3], [4, Fr(7, 2), 3, Fr(5, 2)], (Fr(-1, 2), 4), [(Fr(1, 2), 4), (4, Fr(-1, 2)), (Fr(-1, 2), Fr(7, 2))],
                          "<i>y</i> goes down by 0.5, so the rate is −0.5. When <i>x</i> = 0, <i>y</i> = 4: <b>%s</b>. "
                          "%s forgets the negative sign of a shrinking pattern." % (eq(Fr(-1, 2), 4), eq(Fr(1, 2), 4))))
    its.append(from_table([0, 3, 6, 9], [2, 3, 4, 5], (Fr(1, 3), 2), [(3, 2), (1, 2), (Fr(1, 3), 3)],
                          "<i>x</i> goes up by 3 and <i>y</i> goes up by 1, so the rate is "
                          "<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>. The initial value is 2: "
                          "<b>%s</b>. %s divides the wrong way: change in <i>x</i> ÷ change in <i>y</i>. "
                          "%s uses only the change in <i>y</i>." % (eq(Fr(1, 3), 2), eq(3, 2), eq(1, 2))))
    its.append(eqmcq("A linear relation has an initial value of −4 and a constant rate of 6. Which equation shows it?",
                     (6, -4), [(-4, 6), (6, 4), (-6, -4)],
                     "The rate multiplies <i>x</i> and the initial value is added: <b>%s</b>. "
                     "%s swaps the two numbers." % (eq(6, -4), eq(-4, 6)), [0, 1], [-4, 2]))
    its.append(eqmcq("A linear relation passes through (2, 11) and (5, 20). Which equation shows it?",
                     (3, 5), [(9, -7), (3, 11), (3, 2)],
                     "The rate is (20 − 11) ÷ (5 − 2) = 9 ÷ 3 = 3. Go back 2 steps from (2, 11): 11 − 6 = 5. "
                     "The equation is <b>%s</b>. %s uses 9 as the rate without dividing by 3. "
                     "%s uses 11 as the initial value, but 11 is the value when <i>x</i> = 2." % (eq(3, 5), eq(9, -7), eq(3, 11)),
                     [2, 5], [11, 20]))
    its.append(eqmcq("A linear relation passes through (1, 15) and (4, 3). Which equation shows it?",
                     (-4, 19), [(4, 11), (-4, 15), (-12, 27)],
                     "The rate is (3 − 15) ÷ (4 − 1) = −12 ÷ 3 = −4. Go back one step from (1, 15): 15 + 4 = 19. "
                     "The equation is <b>%s</b>. %s fits (1, 15) but has the wrong sign: the values go down. "
                     "%s does not divide by the change in <i>x</i>." % (eq(-4, 19), eq(4, 11), eq(-12, 27)),
                     [1, 4], [15, 3]))
    its.append(from_table([1, 2, 3, 4], [-7, -10, -13, -16], (-3, -4), [(3, -10), (-3, -7), (-7, -3)],
                          "The rate is −3. Go back to <i>x</i> = 0: −7 + 3 = −4. The equation is <b>%s</b>. "
                          "%s uses the value for <i>x</i> = 1 as the initial value." % (eq(-3, -4), eq(-3, -7))))
    its.append(mcq("For <i>x</i> = 0, 1, 2, 3, which list of values matches %s?" % eq(-2, 10), "10, 8, 6, 4",
                   ["10, 12, 14, 16", "8, 6, 4, 2", "−2, 8, 18, 28"],
                   "Substitute: −2 × 0 + 10 = 10, −2 × 1 + 10 = 8, then 6 and 4. The list is <b>10, 8, 6, 4</b>. "
                   "10, 12, 14, 16 adds 2 instead of subtracting. 8, 6, 4, 2 starts at <i>x</i> = 1. "
                   "−2, 8, 18, 28 mixes up the rate and the initial value."))
    its.append(from_table([0, 1, 2, 3], [Fr(5, 2), 1, Fr(-1, 2), -2], (Fr(-3, 2), Fr(5, 2)),
                          [(Fr(3, 2), Fr(5, 2)), (Fr(-3, 2), 1), (Fr(5, 2), Fr(-3, 2))],
                          "1 − 2.5 = −1.5, so the rate is −1.5. When <i>x</i> = 0, <i>y</i> = 2.5: <b>%s</b>. "
                          "%s forgets the negative sign. %s uses the value for <i>x</i> = 1 as the initial value."
                          % (eq(Fr(-3, 2), Fr(5, 2)), eq(Fr(3, 2), Fr(5, 2)), eq(Fr(-3, 2), 1))))
    xs, ys = [0, 1, 2, 3], [30, 26, 22, 18]
    its.append(eqmcq(tbl(xs, ys) + "Owen writes %s for this table. What is the correct equation?" % eq(4, 30),
                     (-4, 30), [(4, 30), (-4, 26), (30, -4)],
                     "Owen’s equation gives 34 when <i>x</i> = 1, but the table shows 26. The values go down by 4, so the rate "
                     "is −4: <b>%s</b>. In a shrinking pattern the rate must be negative." % eq(-4, 30), xs, ys))
    v = [cnt("shrink", k) for k in (1, 2, 3)]
    its.append(eqmcq(fig(pattern_svg("shrink")) + "Which equation gives the number of tiles, <i>y</i>, in Figure <i>x</i>?",
                     (-2, 12), [(-2, 10), (2, 8), (10, -2)],
                     "Count: 10, 8, 6. The rate is −2. Figure 0 would have 10 + 2 = 12 tiles. The equation is <b>%s</b>. "
                     "%s uses Figure 1 as the initial value. %s fits Figure 1 but grows." % (eq(-2, 12), eq(-2, 10), eq(2, 8)),
                     [1, 2, 3], v))
    v = [cnt("sq", k) for k in (1, 2, 3)]
    its.append(eqmcq(fig(pattern_svg("sq")) + "Which equation gives the number of sticks, <i>y</i>, in Figure <i>x</i>?",
                     (3, 1), [(4, 0), (3, 4), (1, 3)],
                     "Count: 4, 7, 10. The rate is 3. Figure 0 would have 4 − 3 = 1 stick. The equation is <b>%s</b>. "
                     "%s counts 4 sticks per square, but squares share sticks. %s uses Figure 1 as the initial value."
                     % (eq(3, 1), eq(4, 0), eq(3, 4)), [1, 2, 3], v))
    order = [0, 1, 2, 15, 3, 4, 5, 12, 6, 18, 19, 7, 8, 9, 14, 17, 10, 13, 16, 11]
    assert sorted(order) == list(range(20))
    return {"title": "Write the equation from a table", "items": [its[i] for i in order]}


# ============================================================ set 4: graphs
def set_graphs():
    its = []
    gA = graph_svg([(x, 3 * x + 2) for x in range(0, 5)], 6, 16, ylab=4,
                   label="graph of a linear relation: points (0, 2) to (4, 14)")
    its.append(nmcq(fig(gA) + "What is the initial value of this relation?", 2, [3, 5, 0],
                    "The initial value is where the relation meets the <i>y</i>-axis (<i>x</i> = 0): <b>2</b>. "
                    "3 is how much <i>y</i> goes up each step. 5 is the value when <i>x</i> = 1. 0 guesses that every graph starts at 0."))
    its.append(nmcq(fig(gA) + "What is the constant rate of this relation?", 3, [2, 5, 1],
                    "Each step right, the points go up 3: (0, 2), (1, 5), (2, 8). The rate is <b>3</b>. "
                    "2 is the initial value. 5 is the first point after (0, 2), not the change. 1 is the step in <i>x</i>."))
    gB = graph_svg([(x, 10 - 2 * x) for x in range(0, 6)], 6, 10, ylab=2,
                   label="graph of a shrinking linear relation from (0, 10) to (5, 0)")
    its.append(eqmcq(fig(gB) + "Which equation matches the graph?", (-2, 10), [(2, 10), (-2, 8), (-1, 10)],
                     "The graph starts at 10 and goes down 2 for each step right. The equation is <b>%s</b>. "
                     "%s would go up from left to right. %s uses the point for <i>x</i> = 1 as the start."
                     % (eq(-2, 10), eq(2, 10), eq(-2, 8)), list(range(6)), [10 - 2 * x for x in range(6)]))
    its.append(nmcq(fig(gB) + "What is <i>y</i> when <i>x</i> = 4?", 2, [4, 8, 18],
                    "Find 4 on the <i>x</i>-axis and go up to the point, then read across: <b>2</b>. "
                    "4 is the value of <i>x</i>. 8 is the value when <i>x</i> = 1. 18 adds 2 for each step, but the graph goes down."))
    gC = graph_svg([(x, 2 * x - 4) for x in range(0, 5)], 6, 6, ymin=-6, ylab=2,
                   label="graph of a linear relation with negative values: points (0, −4) to (4, 4)")
    its.append(nmcq(fig(gC) + "What is the initial value of this relation?", -4, [4, 2, -2],
                    "At <i>x</i> = 0 the point is 4 below the <i>x</i>-axis: <b>−4</b>. 4 forgets the point is below zero. "
                    "2 is where the graph crosses the <i>x</i>-axis. −2 is the value when <i>x</i> = 1."))
    its.append(nmcq(fig(gC) + "For which value of <i>x</i> is <i>y</i> = 0?", 2, [-4, 0, 4],
                    "<i>y</i> = 0 on the <i>x</i>-axis. The point (2, 0) is there, so <i>x</i> = <b>2</b>. "
                    "Check: 2 × 2 − 4 = 0. −4 is the initial value. 0 is <i>y</i>, not <i>x</i>, and at <i>x</i> = 4 the value is 4."))
    panels = [[(0, 4), (1, 5), (2, 6), (3, 7)], [(7, 0), (6, 1), (5, 2), (4, 3)], [(0, 7), (1, 5), (2, 3), (3, 1)],
              [(0, 7), (1, 6), (2, 5), (3, 4)]]
    assert panels[3] == [(x, 7 - x) for x in range(4)]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for <i>x</i> = 0, 1, 2, 3?" % eq(-1, 7), GRAPHS, 3,
                         "The points are (0, 7), (1, 6), (2, 5), (3, 4): <b>Graph D</b>. Graph A goes up, but the rate is −1. "
                         "Graph B plots (<i>y</i>, <i>x</i>). Graph C goes down by 2 each step."))
    want = [(0, 1), (2, 4), (4, 7)]
    assert all(lv(Fr(3, 2), 1, x) == y for x, y in want)
    panels = [want, [(0, 0), (2, 3), (4, 6)], [(1, 0), (4, 2), (7, 4)], [(0, 1), (2, 3), (4, 5)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for <i>x</i> = 0, 2, 4?" % eq(Fr(3, 2), 1), GRAPHS, 0,
                         "1.5 × 0 + 1 = 1, 1.5 × 2 + 1 = 4, 1.5 × 4 + 1 = 7. The points are (0, 1), (2, 4), (4, 7): "
                         "<b>Graph A</b>. Graph B forgets the + 1. Graph C plots (<i>y</i>, <i>x</i>). Graph D goes up by 1 for each step."))
    panels = [[(0, 6), (1, 7), (2, 8)], [(0, 8), (1, 6), (2, 4)], [(0, 6), (1, 4), (2, 2)], [(0, 2), (1, 4), (2, 6)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows a shrinking pattern with an initial value of 6?", GRAPHS, 2,
                         "A shrinking pattern goes down from left to right, and the initial value is <i>y</i> at <i>x</i> = 0. "
                         "<b>Graph C</b> starts at 6 and goes down. Graph A starts at 6 but grows. "
                         "Graph B shrinks but starts at 8: it reaches 6 only at <i>x</i> = 1."))
    gD = graph_svg([(0, 24), (12, 0)], 12, 24, ystep=2, ylab=4, xlab=2, xname="Time (hours)", yname="Height (cm)",
                   seg=(0, 24, 12, 0), label="graph of candle height over time, a straight line from (0, 24) to (12, 0)")
    its.append(nmcq(fig(gD) + "The graph shows the height of a candle as it burns. How tall is it after 5 hours?",
                    14, [10, 19, 5],
                    "The candle starts at 24 cm and loses 2 cm each hour (24 cm in 12 hours). After 5 hours: "
                    "24 − 5 × 2 = <b>14 cm</b>. 10 cm is how much has burned. 19 cm takes away 1 cm per hour. 5 is the time, not the height.",
                    units("cm")))
    its.append(mcq(fig(gD) + "Why are the points of this graph joined with a line?",
                   "Time can be any value, such as 2.5 hours",
                   ["The candle gets taller over time", "Only whole hours make sense", "All linear graphs use a line"],
                   "The relation is <b>continuous</b>: the candle burns at every moment, so every time between 0 and 12 hours "
                   "makes sense. A pattern of figures is discrete: there is no Figure 2.5."))
    its.append(mcq("Which relation should be graphed as points that are <b>not</b> joined?",
                   "The number of chairs around <i>x</i> tables",
                   ["The height of a candle over time", "The water in a draining tank over time", "The distance a car drives over time"],
                   "You can have 3 or 4 tables, but not 3.5 tables, so <b>the chairs and tables</b> relation is discrete. "
                   "Time can be any value, so the other three are continuous and use a line."))
    gE = graph_svg([(x, Fr(x, 2) + 1) for x in range(0, 7)], 6, 5, ylab=1,
                   label="graph of a linear relation going up by one half")
    its.append(nmcq(fig(gE) + "What is the constant rate of this relation?", Fr(1, 2), [1, 2, Fr(3, 2)],
                    "The points go up 1 for every 2 steps right: 1 ÷ 2 = <b>0.5</b>. 1 is the initial value. "
                    "2 divides the wrong way. 1.5 is the value when <i>x</i> = 1."))
    gF = graph_svg([(x, 6 - 3 * x) for x in range(0, 5)], 6, 6, ymin=-6, ylab=2,
                   label="graph of a shrinking linear relation from (0, 6) to (4, −6)")
    its.append(nmcq(fig(gF) + "What is <i>y</i> when <i>x</i> = 4?", -6, [6, -3, -9],
                    "The point above 4 is below the <i>x</i>-axis at <b>−6</b>. Check: −3 × 4 + 6 = −6. "
                    "6 forgets the point is below zero. −3 is the value when <i>x</i> = 3 and −9 is for <i>x</i> = 5."))
    its.append(eqmcq(fig(gF) + "Which equation matches the graph?", (-3, 6), [(3, 6), (-3, 3), (6, -3)],
                     "The graph starts at 6 and goes down 3 for each step right: <b>%s</b>. "
                     "%s goes up instead of down. %s uses the value at <i>x</i> = 1 as the start."
                     % (eq(-3, 6), eq(3, 6), eq(-3, 3)), list(range(5)), [6 - 3 * x for x in range(5)]))
    good = [(1, 5), (3, 1), (4, -1)]
    assert all(lv(-2, 7, a) == b for a, b in good) and lv(-2, 7, 2) == 3
    its.append(mcq("Which point is <b>not</b> on the graph of %s?" % eq(-2, 7), pt(2, 4), [pt(a, b) for a, b in good],
                   "Test each point. For <i>x</i> = 2: −2 × 2 + 7 = 3, not 4, so <b>(2, 4)</b> is not on the graph. "
                   "(1, 5), (3, 1) and (4, −1) all work."))
    assert lv(4, -3, 6) == 21
    its.append(mcq("The graph of %s continues. Which point is on it?" % eq(4, -3), pt(6, 21), [pt(21, 6), pt(6, 24), pt(6, 27)],
                   "For <i>x</i> = 6: 4 × 6 − 3 = 21, so <b>(6, 21)</b> is on the graph. (21, 6) puts <i>y</i> first. "
                   "(6, 24) forgets the − 3, and (6, 27) adds 3 instead."))
    bad = [(0, 9), (1, 7), (2, 5), (3, 2), (4, 1)]
    assert [9 - 2 * x for x, _ in bad] == [9, 7, 5, 3, 1]
    gG = graph_svg(bad, 6, 10, ylab=2, label="graph of five points, one plotted wrong")
    its.append(mcq(fig(gG) + "These points should follow %s. One point is plotted wrong. Which one?" % eq(-2, 9),
                   pt(3, 2), [pt(1, 7), pt(2, 5), pt(4, 1)],
                   "For <i>x</i> = 3: −2 × 3 + 9 = 3. The point is at <b>(3, 2)</b>, one too low. The other points fit."))
    its.append(mcq("Two relations are %s and %s. Which statement is true?" % (eq(-4, 20), eq(-2, 20)),
                   "Both start at 20, and the first goes down faster",
                   ["Both start at 20, and the second goes down faster", "The first goes up faster", "They start at different values"],
                   "Both have the initial value 20. The first loses 4 each step and the second loses 2, so "
                   "<b>the first goes down faster</b>. −2 is greater than −4, but a rate of −2 is a slower drop."))
    assert lv(3, 2, 10) == 32
    its.append(nmcq(fig(gA) + "The relation continues in the same way. What is <i>y</i> when <i>x</i> = 10?", 32, [30, 35, 29],
                    "The graph shows <i>y</i> = 3<i>x</i> + 2. For <i>x</i> = 10: 3 × 10 + 2 = <b>32</b>. "
                    "30 forgets the initial value. 29 and 35 are the values for <i>x</i> = 9 and 11."))
    order = [0, 1, 3, 2, 4, 5, 6, 7, 8, 12, 9, 10, 11, 13, 14, 15, 16, 19, 17, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Graphs of linear relations", "items": [its[i] for i in order]}


# ============================================================ set 5: solve for unknowns and word problems
def set_words():
    its = []
    assert 3 * 9 + 6 == 33
    its.append(nmcq("Solve 3<i>x</i> + 6 = 33.", 9, [13, 27, 5],
                    "Undo + 6: 33 − 6 = 27. Undo × 3: 27 ÷ 3 = <b>9</b>. Check: 3 × 9 + 6 = 33. "
                    "13 adds 6 instead of subtracting. 27 stops before dividing. 5 undoes in the wrong order: 33 ÷ 3 − 6."))
    assert -2 * 3 + 10 == 4
    its.append(nmcq("Solve −2<i>x</i> + 10 = 4.", 3, [-3, 7, 6],
                    "Undo + 10: 4 − 10 = −6. Undo × (−2): −6 ÷ (−2) = <b>3</b>. Check: −2 × 3 + 10 = 4. "
                    "−3 divides by 2 instead of −2. 6 forgets to divide. 7 adds: (4 + 10) ÷ 2."))
    assert Fr(1, 2) * 14 - 3 == 4
    its.append(nmcq("Solve 0.5<i>x</i> − 3 = 4.", 14, [Fr(7, 2), 2, 7],
                    "Undo − 3: 4 + 3 = 7. Undo × 0.5: 7 ÷ 0.5 = <b>14</b>. Check: 0.5 × 14 − 3 = 4. "
                    "3.5 multiplies by 0.5 instead of dividing. 2 subtracts 3 instead of adding. 7 stops before dividing."))
    its.append(eqmcq("A cup of hot chocolate is 80 °C. For the first 10 minutes it cools by 2.5 °C each minute. "
                     "Which equation gives its temperature, <i>T</i>, after <i>m</i> minutes?",
                     (Fr(-5, 2), 80), [(Fr(5, 2), 80), (80, Fr(-5, 2)), (Fr(-5, 2), Fr(155, 2))],
                     "The drink starts at 80 °C, so the initial value is 80. It cools, so the rate is −2.5: <b>%s</b>. "
                     "%s makes the drink warmer each minute. %s swaps the rate and the initial value. %s uses the temperature after 1 minute as the start."
                     % (eq(Fr(-5, 2), 80, "m", "T"), eq(Fr(5, 2), 80, "m", "T"), eq(80, Fr(-5, 2), "m", "T"), eq(Fr(-5, 2), Fr(155, 2), "m", "T")),
                     [0, 1, 2], [80, Fr(155, 2), 75], x="m", y="T"))
    its.append(nmcq("Hot chocolate starts at 80 °C and cools by 2.5 °C each minute. What is its temperature after 6 minutes?",
                    65, [95, Fr(135, 2), 15],
                    "<i>T</i> = −2.5 × 6 + 80 = −15 + 80 = <b>65 °C</b>. 95 °C adds the 15 degrees, but the drink is cooling. "
                    "67.5 °C is after 5 minutes. 15 °C is how much it cooled.", units("°C")))
    its.append(nmcq("Hot chocolate starts at 80 °C and cools by 2.5 °C each minute. After how many minutes is it 60 °C?",
                    8, [24, 56, 20],
                    "Solve −2.5<i>m</i> + 80 = 60. It must cool 80 − 60 = 20 degrees. 20 ÷ 2.5 = <b>8 minutes</b>. "
                    "24 is 60 ÷ 2.5 and forgets the start. 20 is the number of degrees, not minutes. 56 adds 80 + 60.", units("minutes")))
    its.append(eqmcq("A bike rental in Muskoka costs $12 plus $8 for each hour. Which equation gives the cost, <i>C</i>, "
                     "in dollars, for <i>h</i> hours?", (8, 12), [(12, 8), (20, 0), (8, 0)],
                     "Each hour adds $8, so the rate is 8. The $12 is paid once, so it is the initial value: <b>%s</b>. "
                     "%s charges $12 every hour. %s adds the $12 to every hour, and %s forgets the $12." % (eq(8, 12, "h", "C"), eq(12, 8, "h", "C"),
                                                                             eq(20, 0, "h", "C"), eq(8, 0, "h", "C")),
                     [0, 1, 2], [12, 20, 28], x="h", y="C"))
    assert 8 * Fr(7, 2) + 12 == 40
    its.append(nmcq("A bike rental costs $12 plus $8 for each hour. How much does it cost for 3.5 hours?", 40, [70, 28, 50],
                    "<i>C</i> = 8 × 3.5 + 12 = 28 + 12 = <b>$40.00</b>. $28.00 forgets the $12. "
                    "$70.00 adds first: (12 + 8) × 3.5. $50.00 swaps the numbers: 12 × 3.5 + 8.", money))
    assert (60 - 12) / 8 == 6
    its.append(nmcq("A bike rental costs $12 plus $8 for each hour. Chloe has $60. For how many hours can she rent the bike?",
                    6, [Fr(15, 2), 9, 48],
                    "Solve 8<i>h</i> + 12 = 60. Take off the $12: 60 − 12 = 48. Then 48 ÷ 8 = <b>6 hours</b>. "
                    "7.5 hours forgets the $12. 9 hours adds the $12 instead of subtracting. 48 is dollars, not hours.", units("hours")))
    assert 12 + 8 * 4 == 20 + 6 * 4 == 44
    its.append(nmcq("Shop A rents bikes for $12 plus $8 per hour. Shop B charges $20 plus $6 per hour. "
                    "After how many hours do both shops cost the same?", 4, [8, 2, 44],
                    "Set them equal: 8<i>h</i> + 12 = 6<i>h</i> + 20. Subtract 6<i>h</i> and 12: 2<i>h</i> = 8, so <i>h</i> = <b>4</b>. "
                    "Both cost $44. 8 is the difference in start fees and 2 is the difference in rates. 44 is the cost.",
                    units("hours")))
    assert 90 - 6 * 10 == 30
    its.append(nmcq("A snowbank in Ottawa is 90 cm deep. In March it melts 6 cm each day. After how many days is it 30 cm deep?",
                    10, [5, 20, 15],
                    "Solve −6<i>d</i> + 90 = 30. It must melt 90 − 30 = 60 cm. 60 ÷ 6 = <b>10 days</b>. "
                    "5 is 30 ÷ 6. 20 adds 90 + 30. 15 is when the snow is all gone.", units("days")))
    assert 50 - Fr(13, 4) * 12 == 11
    its.append(nmcq("Maya puts $50 on a transit card. Each bus ride takes $3.25 off the card. How much is left after 12 rides?",
                    11, [89, Fr(57, 4), 39],
                    "Balance = −3.25 × 12 + 50 = −39 + 50 = <b>$11.00</b>. $89.00 adds the rides instead of subtracting. "
                    "$14.25 is after 11 rides. $39.00 is how much she spent.", money))
    its.append(eqmcq("Maya puts $50 on a transit card. Each bus ride costs $3.25. Which equation gives the balance, "
                     "<i>B</i>, in dollars, after <i>r</i> rides?",
                     (Fr(-13, 4), 50), [(Fr(13, 4), 50), (50, Fr(-13, 4)), (Fr(-13, 4), Fr(187, 4))],
                     "The card starts at $50 and each ride takes off $3.25, so the rate is −3.25: <b>%s</b>. "
                     "%s makes the card grow with every ride. %s uses the balance after 1 ride as the start."
                     % (eq(Fr(-13, 4), 50, "r", "B"), eq(Fr(13, 4), 50, "r", "B"), eq(Fr(-13, 4), Fr(187, 4), "r", "B")),
                     [0, 1, 2], [50, Fr(187, 4), Fr(87, 2)], x="r", y="B"))
    assert (96 - 24) / 12 == 6
    its.append(nmcq("A canoe outfitter near Algonquin Park charges a $24 fee plus $12 for each hour. Liam pays $96. "
                    "For how many hours did he rent the canoe?", 6, [8, 10, 72],
                    "Solve 12<i>h</i> + 24 = 96. Subtract the fee: 96 − 24 = 72. Then 72 ÷ 12 = <b>6 hours</b>. "
                    "8 is 96 ÷ 12 and forgets the fee. 10 adds the fee. 72 stops before dividing.", units("hours")))
    assert 12000 - 400 * 20 == 4000
    its.append(nmcq("A pool holds 12 000 L of water. It drains at 400 L each minute. After how many minutes are 4000 L left?",
                    20, [10, 40, 30],
                    "Solve −400<i>m</i> + 12 000 = 4000. It must lose 12 000 − 4000 = 8000 L. 8000 ÷ 400 = <b>20 minutes</b>. "
                    "10 is 4000 ÷ 400. 30 is when the pool is empty. 40 adds 12 000 + 4000.", units("minutes")))
    assert 4 - 2 * 5 == -6
    its.append(nmcq("At 6:00 p.m. in Winnipeg it is 4 °C. The temperature falls 2 °C each hour. What is the temperature at "
                    "11:00 p.m.?", -6, [14, 6, -4],
                    "From 6:00 to 11:00 is 5 hours. <i>T</i> = −2 × 5 + 4 = −10 + 4 = <b>−6 °C</b>. "
                    "14 °C adds instead of subtracting. 6 °C forgets the answer is below zero. −4 °C is after 4 hours.",
                    units("°C")))
    assert 4 - 2 * 7 == -10
    its.append(nmcq("It is 4 °C and the temperature falls 2 °C each hour. After how many hours is it −10 °C?", 7, [3, 5, 14],
                    "Solve −2<i>h</i> + 4 = −10. Subtract 4: −2<i>h</i> = −14. Divide by −2: <i>h</i> = <b>7 hours</b>. "
                    "3 uses 10 − 4, as if −10 were 10. 5 is 10 ÷ 2 and forgets the 4 °C start. 14 forgets to divide.",
                    units("hours")))
    assert 15 + 3 * 10 == 45
    its.append(nmcq("For the Terry Fox Run, Noah’s grandmother pledges $15 plus $3 for each kilometre he runs. "
                    "She gives $45. How far did Noah run?", 10, [15, 20, 30],
                    "Solve 3<i>k</i> + 15 = 45. 45 − 15 = 30, and 30 ÷ 3 = <b>10 km</b>. "
                    "15 km is 45 ÷ 3 and forgets the $15. 20 km adds the $15. 30 km forgets to divide.", units("km")))
    assert 80 - Fr(5, 2) * 8 == 70 - Fr(5, 4) * 8 == 60
    its.append(nmcq("Hot chocolate starts at 80 °C and cools 2.5 °C each minute. Tea starts at 70 °C and cools 1.25 °C each "
                    "minute. After how many minutes are they the same temperature?", 8, [4, 60, 10],
                    "Set them equal: −2.5<i>m</i> + 80 = −1.25<i>m</i> + 70. The hot chocolate catches up 1.25 °C each minute, "
                    "and the gap is 10 °C: 10 ÷ 1.25 = <b>8 minutes</b>. Both are 60 °C. 4 divides 10 by 2.5. "
                    "60 is the temperature. 10 is the gap in degrees.", units("minutes")))
    assert 8 * 2 + 12 == 28 and 8 * 4 + 12 == 44
    its.append(mcq("A bike rental costs <i>C</i> = 8<i>h</i> + 12 dollars. Ethan says 4 hours costs twice as much as 2 hours. "
                   "Is he right?", "No: 2 hours is $28 and 4 hours is $44",
                   ["Yes: 4 hours is $56", "Yes: both rates are $8", "No: 4 hours is $32"],
                   "2 hours: 8 × 2 + 12 = $28. 4 hours: 8 × 4 + 12 = $44, not 2 × 28 = $56. "
                   "<b>No</b>: the $12 is paid only once, so doubling the hours does not double the cost. $32 forgets the $12."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 9, 19, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Solve for unknowns and word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    return (
        "<h2>Constant rate and initial value</h2>"
        "<p>A <b>linear relation</b> changes by the same amount each time <i>x</i> goes up by 1. "
        "That amount is the <b>constant rate</b>. The <b>initial value</b> is the value of <i>y</i> when <i>x</i> = 0. "
        "In the equation <i>y</i> = <i>a</i><i>x</i> + <i>b</i>, <i>a</i> is the rate and <i>b</i> is the initial value.</p>"
        "<p>If the values go up, the pattern is <b>growing</b> and the rate is positive. "
        "If the values go down, the pattern is <b>shrinking</b> and the rate is <b>negative</b>.</p>"
        + table(["<i>x</i>", "0", "1", "2", "3", "4"], [["<i>y</i>", "10", "8", "6", "4", "2"]]) +
        "<h2>Write the equation from a table</h2>"
        + ex("Equation for 10, 8, 6, 4", "Write an equation for the table above.",
             "Find the rate: 8 − 10 = −2. The values go down, so the rate is negative. "
             "Find the initial value: when <i>x</i> = 0, <i>y</i> = 10. Check <i>x</i> = 3: −2 × 3 + 10 = 4.", eq(-2, 10))
        + ex("When x skips numbers", "The table has (0, 3), (2, 11), (4, 19). What is the rate?",
             "<i>x</i> goes up by 2 and <i>y</i> goes up by 8. Divide: 8 ÷ 2 = 4. The equation is <i>y</i> = 4<i>x</i> + 3.", "4") +
        "<h2>Graph a linear relation</h2>"
        "<p>Plot each pair (<i>x</i>, <i>y</i>): across first, then up or down. The points lie on a straight line. "
        "The graph meets the <i>y</i>-axis at the initial value. A growing relation goes up from left to right, "
        "and a shrinking one goes down. Join the points with a line only when every value between them makes sense "
        "(<b>continuous</b>, like time). For figures in a pattern, leave the points apart (<b>discrete</b>).</p>"
        "<figure class='sn-fig'>" + graph_svg([(x, 10 - 2 * x) for x in range(0, 6)], 6, 10, ylab=2,
                                               label="graph of y = −2x + 10") +
        "<figcaption>The graph of <i>y</i> = −2<i>x</i> + 10 starts at 10 and goes down 2 for each step right.</figcaption></figure>"
        "<h2>Solve for an unknown value</h2>"
        + ex("A cooling drink", "Hot chocolate is 80 °C and cools 2.5 °C each minute. When is it 60 °C?",
             "The equation is <i>T</i> = −2.5<i>m</i> + 80. Solve −2.5<i>m</i> + 80 = 60. Subtract 80: −2.5<i>m</i> = −20. "
             "Divide by −2.5: <i>m</i> = 8.", "8 minutes")
        + ex("A bike rental", "A bike costs $12 plus $8 for each hour. How long can you ride for $60?",
             "Solve 8<i>h</i> + 12 = 60. Subtract 12: 8<i>h</i> = 48. Divide by 8: <i>h</i> = 6.", "6 hours") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Giving a shrinking pattern a positive rate: <i>y</i> = 2<i>x</i> + 10 for 10, 8, 6", "Values go down, so the rate is negative: <i>y</i> = −2<i>x</i> + 10"],
            ["Using the value at <i>x</i> = 1 as the initial value", "The initial value is <i>y</i> when <i>x</i> = 0. Go back one step"],
            ["Using the change in <i>y</i> when <i>x</i> skips numbers", "Divide the change in <i>y</i> by the change in <i>x</i>"],
            ["Swapping the rate and the initial value", "The rate multiplies <i>x</i>. The initial value is added on its own"],
            ["Undoing in the wrong order when solving", "Undo the + or − first, then the × or ÷"],
            ["Plotting (<i>y</i>, <i>x</i>)", "Go across for <i>x</i> first, then up or down for <i>y</i>"],
        ])
    )


FAQ = [
    {"q": "What are linear relations in Grade 8 math in Ontario?",
     "a": "In the Ontario Grade 8 algebra strand, students study linear growing and shrinking patterns. They describe them with a constant rate and an initial value, show them in tables, graphs and equations like y = −2x + 10, and use the equations to solve for unknown values."},
    {"q": "How do you write an equation from a table of values?",
     "a": "Find the constant rate: the change in y divided by the change in x. Then find the initial value, the value of y when x = 0. For 10, 8, 6, 4 the rate is −2 and the initial value is 10, so y = −2x + 10."},
    {"q": "What is the difference between a growing and a shrinking linear pattern?",
     "a": "A growing pattern goes up by the same amount each time, so its rate is positive. A shrinking pattern goes down by the same amount each time, so its rate is negative and its graph goes down from left to right."},
    {"q": "How do you solve for an unknown value in a linear relation?",
     "a": "Set the equation equal to the known value and undo the operations in reverse order. For 8h + 12 = 60, subtract 12 to get 48, then divide by 8 to get h = 6."},
]


def gen():
    rnd = random.Random(48809)
    sets = [set_rate(), set_patterns(), set_equations(), set_graphs(), set_words()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "linear-relations",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Linear Relations: Growing and Shrinking Patterns, Equations and Graphs",
        "seo_title": "Grade 8 Linear Relations Worksheets: Tables, Equations and Graphs (Ontario Math, Free)",
        "short_title": "Linear relations",
        "domain": "Algebra",
        "standard_code": "Grade 8: C1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating, growing, and shrinking patterns, and use algebraic representations of the pattern rules to solve for unknown values in linear growing and shrinking patterns",
        "meta_desc": "Free Grade 8 math worksheets on linear relations for the Ontario curriculum: constant rate and initial value, growing and shrinking patterns, equations like y = −2x + 10 from tables, graphs, and solving for unknowns in cooling drink and bike rental problems. 100 questions with an answer key.",
        "key_big": "In y = ax + b, the constant rate a multiplies x and the initial value b is y when x = 0. A shrinking pattern has a negative rate.",
        "key_sub": "For 10, 8, 6, 4 the values go down by 2, so the rate is −2, and y = 10 when x = 0: y = −2x + 10. To find when y = 4, solve −2x + 10 = 4: subtract 10, then divide by −2 to get x = 3.",
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
