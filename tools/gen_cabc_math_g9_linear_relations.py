# -*- coding: utf-8 -*-
"""
BC Mathematics 9: Linear relations and graphs (Patterning: two-variable linear relations, using graphing,
interpolation, and extrapolation)
  python3 tools/gen_cabc_math_g9_linear_relations.py
Tables of values to graphs, reading a linear graph, interpolation between points, extrapolation beyond the data,
and equations of relations in word problems (taxi fares, cooling soup and coffee, rentals, savings).
Wrong answers come from real mistakes: reading the wrong axis, plotting (y, x), taking the nearest data point
instead of interpolating, extrapolating the wrong way, forgetting the initial value, and dividing the wrong way.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
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
NB = "\u00a0"


# ------------------------------------------------------------ numbers
def n(v):
    """BC/SI style: 4536, 12 000 (no-break space), decimals with a point, real minus sign."""
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

def panels_svg(groups, label):
    """Four small graphs A, B, C, D (x and y from 0 to 8) in one picture."""
    U, N = 13, 8
    PL, PT, PB, PR, GAP = 27, 26, 22, 10, 14
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
            s.append(text(X0 - 7, Y0 - g * U + 5, str(g), 14, "end", bold=False))
        for px, py in pts:
            assert 0 <= px <= N and 0 <= py <= N
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X0 + px * U, Y0 - py * U, RED))
    return svg_wrap(W, H, "".join(s), label)


def slope(xs, ys):
    """Constant rate of a table, checked to be constant."""
    r = {(Fr(ys[i + 1]) - Fr(ys[i])) / (Fr(xs[i + 1]) - Fr(xs[i])) for i in range(len(xs) - 1)}
    assert len(r) == 1, (xs, ys)
    return r.pop()



def units(u):
    """Number + unit. '°C' and '%' attach with a no-break space / nothing; 1 hour, 1 minute (singular)."""
    def f(v):
        w = u
        if Fr(v) == 1 and u in ("hours", "minutes", "weeks", "days"):
            w = u[:-1]
        if u == "%":
            return n(v) + "%"
        return "%s%s%s" % (n(v), NB if u.startswith("°") else " ", w)
    return f


PCT = units("%")


def mon(v):
    """Money: $18.00 style."""
    return money(v)


# ------------------------------------------------------------ graph with any x step
def graph(pts, xmax, ymax, xstep=1, xlab=1, ymin=0, ystep=1, ylab=1, xname="x", yname="y",
          seg=None, dash=None, tags=None, label="graph of a linear relation"):
    """Grid drawn exactly to the data. x from 0 to xmax in steps of xstep (labels every xlab),
    y from ymin to ymax in steps of ystep (labels every ylab). seg / dash: lists of (x1, y1, x2, y2)."""
    xmax, xstep, xlab = Fr(xmax), Fr(xstep), Fr(xlab)
    ymin, ymax, ystep, ylab = Fr(ymin), Fr(ymax), Fr(ystep), Fr(ylab)
    nx = int(xmax / xstep)
    ny = int((ymax - ymin) / ystep)
    assert nx * xstep == xmax and ny * ystep == ymax - ymin
    assert (ymin / ylab).denominator == 1 and (ylab / ystep).denominator == 1 and (xlab / xstep).denominator == 1
    tags = tags or {}
    XU = 32 if nx <= 7 else (26 if nx <= 10 else 21)
    PH = Fr(210)
    ylabels = []
    k = ymin
    while k <= ymax:
        ylabels.append((k, n(k)))
        k += ylab
    LW = max(tw(t, 14) for _, t in ylabels)
    yn_long = len(yname) > 1
    L = (34 if yn_long else 24) + LW + 8
    Tm, R, B = 16, 22, 50
    X0 = L
    X = lambda v: float(X0 + Fr(v) / xstep * XU)
    Y = lambda v: float(Tm + (ymax - Fr(v)) * PH / (ymax - ymin))
    Yb = Y(ymin)
    W = L + nx * XU + R
    H = Yb + B
    s = []
    for j in range(ny + 1):
        y = Y(ymin + j * ystep)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X(xmax), y, GRID))
    for gy, t in ylabels:
        s.append(text(X0 - 7, Y(gy) + 5, t, 14, "end", bold=False))
    for i in range(nx + 1):
        gx = i * xstep
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X(gx), Tm, X(gx), Yb, GRID))
        if (gx / xlab).denominator == 1:
            s.append(text(X(gx), Yb + 19, n(gx), 14, bold=False))
    ya = Y(0) if ymin <= 0 <= ymax else Yb
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, ya, X(xmax), ya, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Tm, X0, Yb, INK))
    xn = SX(xname) if len(xname) == 1 else xname
    yn = SX(yname) if len(yname) == 1 else yname
    s.append(text(X0 + nx * XU / 2, H - 8, xn, 15 if len(xname) > 1 else 17))
    if yn_long:
        cy = (Tm + Yb) / 2
        s.append(text(16, cy, yn, 15, extra=" transform='rotate(-90 16 %.1f)'" % cy))
    else:
        s.append(text(X0 - LW - 16, (Tm + Yb) / 2 + 6, yn, 17))
    for x1, y1, x2, y2 in (seg or []):
        for v in ((x1, y1), (x2, y2)):
            assert 0 <= v[0] <= xmax and ymin <= v[1] <= ymax, v
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                 % (X(x1), Y(y1), X(x2), Y(y2), BLUE))
    for x1, y1, x2, y2 in (dash or []):
        for v in ((x1, y1), (x2, y2)):
            assert 0 <= v[0] <= xmax and ymin <= v[1] <= ymax, v
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                 % (X(x1), Y(y1), X(x2), Y(y2), BLUE))
    for px, py in pts:
        assert 0 <= px <= xmax and ymin <= py <= ymax, (px, py)
        cx, cy = X(px), Y(py)
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
        if (px, py) in tags:
            t = tags[(px, py)]
            w = tw(t, 15) + 6
            if cx - w - 6 < X0 + 4:
                bx, by = cx + 8, cy + 6
            else:
                bx, by = cx - w - 6, cy - 25
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='19' rx='3' fill='#ffffff' opacity='0.9'/>"
                     % (bx, by, w))
            s.append(text(bx + w / 2, by + 15, t, 15, col=GREEN))
    return svg_wrap(W, H, "".join(s), label)


GRAPHS = ["Graph A", "Graph B", "Graph C", "Graph D"]


# ============================================================ set 1: tables of values to graphs
def set_tables():
    its = []
    assert lv(2, 1, 3) == 7
    its.append(nmcq(tbl([0, 1, 2, 3], [1, 3, 5, "?"]) + "This table of values is for %s. What value is missing?" % eq(2, 1),
                    7, [6, 8, 4],
                    "Put <i>x</i> = 3 into the equation: 2 × 3 + 1 = <b>7</b>. "
                    "6 forgets the + 1. 8 adds before multiplying: 2 × (3 + 1). 4 adds 3 + 1 and forgets the 2."))
    assert lv(3, -2, 0) == -2
    its.append(nmcq(tbl([0, 1, 2, 3], ["?", 1, 4, 7]) + "This table of values is for %s. What value is missing?" % eq(3, -2),
                    -2, [2, 1, 3],
                    "When <i>x</i> = 0, 3 × 0 = 0, so <i>y</i> = 0 − 2 = <b>−2</b>. "
                    "2 drops the minus sign. 1 is the value for <i>x</i> = 1. 3 is the constant rate."))
    assert lv(-1, 4, -2) == 6
    its.append(nmcq(tbl([-2, -1, 0, 1, 2], ["?", 5, 4, 3, 2]) + "This table of values is for %s. What value is missing?" % eq(-1, 4),
                    6, [2, 5, -6],
                    "−(−2) = +2, so <i>y</i> = 2 + 4 = <b>6</b>. "
                    "2 treats −(−2) as −2. 5 is the value for <i>x</i> = −1. −6 makes the whole answer negative."))
    its.append(mcq(tbl([0, 1, 2, 3], [5, 8, 11, 14]) + "Which point do you plot for the column where <i>x</i> = 2?",
                   pt(2, 11), [pt(11, 2), pt(2, 8), pt(3, 11)],
                   "Each column gives one point (<i>x</i>, <i>y</i>). For <i>x</i> = 2, <i>y</i> = 11, so plot <b>(2, 11)</b>. "
                   "(11, 2) puts <i>y</i> first. (2, 8) takes <i>y</i> from the column before. (3, 11) uses the wrong <i>x</i>."))
    want = [(0, 1), (1, 3), (2, 5), (3, 7)]
    assert all(lv(2, 1, x) == y for x, y in want)
    panels = [[(0, 1), (1, 2), (2, 3), (3, 4)], want, [(1, 0), (3, 1), (5, 2), (7, 3)], [(0, 0), (1, 2), (2, 4), (3, 6)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows the table <i>x</i> = 0, 1, 2, 3 and <i>y</i> = 1, 3, 5, 7?", GRAPHS, 1,
                         "The points are (0, 1), (1, 3), (2, 5), (3, 7): <b>Graph B</b>. "
                         "Graph A goes up by 1, not 2. Graph C plots (<i>y</i>, <i>x</i>). Graph D starts at 0 instead of 1."))
    g = graph([(x, 3 * x + 2) for x in range(5)], 5, 14, ystep=1, ylab=2,
              label="graph of five points from (0, 2) to (4, 14)")
    its.append(mcq(fig(g) + "For <i>x</i> = 0, 1, 2, 3, 4, which <i>y</i>-values match the points on the graph?",
                   "2, 5, 8, 11, 14", ["0, 3, 6, 9, 12", "2, 4, 6, 8, 10", "1, 4, 7, 10, 13"],
                   "Read straight up from each <i>x</i> and across to the <i>y</i>-axis: <b>2, 5, 8, 11, 14</b>. "
                   "0, 3, 6, 9, 12 ignores that the first point is at 2. 2, 4, 6, 8, 10 copies the axis labels. "
                   "1, 4, 7, 10, 13 reads one grid line too low."))
    its.append(mcq("For <i>x</i> = 0, 1, 2, 3, which <i>y</i>-values give points on a straight line?",
                   "2, 5, 8, 11", ["2, 4, 8, 16", "1, 4, 9, 16", "2, 5, 9, 14"],
                   "Points are on a straight line when <i>y</i> changes by the same amount each step. "
                   "<b>2, 5, 8, 11</b> goes up 3 every time. 2, 5, 9, 14 goes up 3, 4, 5. 2, 4, 8, 16 doubles. "
                   "1, 4, 9, 16 goes up 3, 5, 7."))
    assert lv(2, 3, 4) == 11
    its.append(mcq("The points (0, 3), (1, 5) and (2, 7) lie on a line. Which point is also on this line?",
                   pt(4, 11), [pt(11, 4), pt(4, 9), pt(3, 8)],
                   "<i>y</i> goes up 2 for each 1 in <i>x</i>: (3, 9), then <b>(4, 11)</b>. "
                   "(11, 4) swaps <i>x</i> and <i>y</i>. (4, 9) is one step behind. (3, 8) adds only 1."))
    assert lv(-2, 1, -3) == 7
    its.append(nmcq("Make a table of values for %s. What is <i>y</i> when <i>x</i> = −3?" % eq(-2, 1), 7, [-5, 5, -7],
                    "−2 × (−3) = +6, and 6 + 1 = <b>7</b>. "
                    "−5 uses −2 × (−3) = −6. 5 subtracts 1 instead of adding. −7 makes both signs negative."))
    xs, ys = [0, 2, 4, 6], [1, 7, 13, 19]
    assert slope(xs, ys) == 3 and lv(3, 1, 8) == 25
    its.append(nmcq(tbl(xs, ys) + "The table continues in the same way. What is <i>y</i> when <i>x</i> = 8?", 25, [31, 20, 24],
                    "<i>x</i> goes up by 2 and <i>y</i> goes up by 6 each column. The next column is (8, 19 + 6) = <b>25</b>. "
                    "31 adds 6 for each 1 in <i>x</i>: 19 + 2 × 6. 20 adds 1. 24 is 3 × 8 and forgets the start of 1."))
    its.append(mcq("Which relation should be graphed as a solid line, not as separate points?",
                   "The temperature of soup over time",
                   ["The cost of <i>x</i> movie tickets", "The number of wheels on <i>x</i> bikes", "The number of chairs at <i>x</i> tables"],
                   "Time can take any value, like 2.5 minutes, so <b>the temperature of soup over time</b> is continuous: join the points. "
                   "You cannot buy 2.5 tickets or have 2.5 bikes or tables, so those graphs are separate points (discrete)."))
    its.append(mcq("A table of values for %s is graphed. Which describes the graph?" % eq(-3, 4),
                   "Goes down to the right and crosses the <i>y</i>-axis at 4",
                   ["Goes up to the right and crosses the <i>y</i>-axis at 4",
                    "Goes down to the right and crosses the <i>y</i>-axis at −3",
                    "Goes up to the right and crosses the <i>y</i>-axis at −3"],
                   "The rate −3 is negative, so <i>y</i> gets smaller as <i>x</i> grows: the line goes down. "
                   "When <i>x</i> = 0, <i>y</i> = 4. <b>Down to the right, through (0, 4).</b> −3 is the rate, not the start."))
    bad = [(0, 2), (1, 3), (2, 4), (5, 3), (4, 6)]
    assert [lv(1, 2, x) for x in range(5)] == [2, 3, 4, 5, 6]
    g = graph(bad, 6, 8, ystep=1, ylab=2, label="graph of five points, one plotted wrong")
    its.append(mcq(fig(g) + "These points should show %s for <i>x</i> = 0, 1, 2, 3, 4. Which point is plotted wrong?" % eq(1, 2),
                   pt(5, 3), [pt(1, 3), pt(2, 4), pt(4, 6)],
                   "For <i>x</i> = 3, <i>y</i> = 3 + 2 = 5, so the point should be (3, 5). It was plotted at <b>(5, 3)</b>: "
                   "<i>x</i> and <i>y</i> were swapped. The other three points fit the equation."))
    assert lv(Fr(1, 2), 1, 6) == 4
    its.append(nmcq("Make a table of values for %s. What is <i>y</i> when <i>x</i> = 6?" % eq(Fr(1, 2), 1), 4, [7, 13, Fr(7, 2)],
                    "0.5 × 6 = 3, and 3 + 1 = <b>4</b>. "
                    "7 adds 6 + 1 and forgets the 0.5. 13 doubles 6 instead of halving it. 3.5 is the value for <i>x</i> = 5."))
    assert lv(Fr(-1, 2), 3, 4) == 1
    its.append(nmcq("Make a table of values for %s. What is <i>y</i> when <i>x</i> = 4?" % eq(Fr(-1, 2), 3), 1, [5, -5, Fr(5, 2)],
                    "−0.5 × 4 = −2, and −2 + 3 = <b>1</b>. "
                    "5 uses +2 instead of −2. −5 computes −2 − 3. 2.5 is the value for <i>x</i> = 1."))
    good = "(−1, −5), (0, −1), (1, 3), (2, 7)"
    assert [lv(4, -1, x) for x in (-1, 0, 1, 2)] == [-5, -1, 3, 7]
    its.append(mcq("Which list of points comes from a table of values for %s?" % eq(4, -1), good,
                   ["(−1, 3), (0, −1), (1, 3), (2, 7)", "(−5, −1), (−1, 0), (3, 1), (7, 2)", "(−1, −3), (0, −1), (1, 3), (2, 7)"],
                   "4 × (−1) − 1 = −4 − 1 = −5, then −1, 3, 7: <b>%s</b>. The list with (−1, 3) uses 4 × (−1) = 4. "
                   "The list with (−5, −1) puts <i>y</i> first. (−1, −3) computes −4 + 1." % good))
    assert lv(2, -6, 0) == -6
    its.append(mcq("Where does the graph of %s cross the <i>y</i>-axis?" % eq(2, -6), pt(0, -6), [pt(0, 6), pt(-6, 0), pt(3, 0)],
                   "On the <i>y</i>-axis <i>x</i> = 0, and 2 × 0 − 6 = −6. The point is <b>(0, −6)</b>. "
                   "(0, 6) drops the sign. (−6, 0) puts the value on the wrong axis. (3, 0) is where it crosses the <i>x</i>-axis."))
    assert lv(2, -6, 3) == 0
    its.append(mcq("Where does the graph of %s cross the <i>x</i>-axis?" % eq(2, -6), pt(3, 0), [pt(0, -6), pt(-3, 0), pt(6, 0)],
                   "On the <i>x</i>-axis <i>y</i> = 0. Solve 2<i>x</i> − 6 = 0: 2<i>x</i> = 6, so <i>x</i> = 3. The point is <b>(3, 0)</b>. "
                   "(0, −6) is the <i>y</i>-axis crossing. (6, 0) forgets to divide by 2. (−3, 0) gets the sign wrong."))
    want = [(x, 8 - 2 * x) for x in range(5)]
    panels = [[(x, 2 * x) for x in range(5)], [(8 - 2 * x, x) for x in range(5)], want, [(x, 8 - x) for x in range(5)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for <i>x</i> = 0, 1, 2, 3, 4?" % eq(-2, 8), GRAPHS, 2,
                         "The points are (0, 8), (1, 6), (2, 4), (3, 2), (4, 0): <b>Graph C</b>. "
                         "Graph A goes up, but the rate −2 means down. Graph B plots (<i>y</i>, <i>x</i>). Graph D goes down by 1, not 2."))
    want = [(0, 2), (2, 3), (4, 4), (6, 5)]
    assert all(lv(Fr(1, 2), 2, x) == y for x, y in want)
    panels = [[(2, 0), (3, 2), (4, 4), (5, 6)], [(0, 2), (1, 3), (2, 4), (3, 5)], [(0, 2), (2, 4), (4, 6), (6, 8)], want]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows the table <i>x</i> = 0, 2, 4, 6 and <i>y</i> = 2, 3, 4, 5?", GRAPHS, 3,
                         "Plot each column: (0, 2), (2, 3), (4, 4), (6, 5): <b>Graph D</b>. Graph A plots (<i>y</i>, <i>x</i>). "
                         "Graph B puts the points at <i>x</i> = 0, 1, 2, 3 and ignores that <i>x</i> goes up by 2. "
                         "Graph C goes up 2 each column instead of 1."))
    return {"title": "Tables of values to graphs", "items": its}


# ============================================================ set 2: read a graph
def set_read():
    its = []
    g1 = graph([(x, 3 * x + 2) for x in range(7)], 6, 20, ystep=1, ylab=2, seg=[(0, 2, 6, 20)],
               label="graph of a line through (0, 2) and (6, 20)")
    its.append(nmcq(fig(g1) + "What is <i>y</i> when <i>x</i> = 4?", 14, [4, 12, 11],
                    "Find 4 on the <i>x</i>-axis, go up to the line, then across to the <i>y</i>-axis: <b>14</b>. "
                    "4 is the <i>x</i>-value, read from the wrong axis. 12 is 3 × 4 without the start of 2. 11 is the value for <i>x</i> = 3."))
    its.append(nmcq(fig(g1) + "For which value of <i>x</i> is <i>y</i> = 8?", 2, [8, 26, 6],
                    "Find 8 on the <i>y</i>-axis, go across to the line, then down: <i>x</i> = <b>2</b>. "
                    "8 is the <i>y</i>-value. 26 puts 8 in for <i>x</i>: 3 × 8 + 2. 6 is 8 − 2 without dividing by 3."))
    its.append(nmcq(fig(g1) + "What is the initial value of this relation (<i>y</i> when <i>x</i> = 0)?", 2, [0, 3, 5],
                    "The line meets the <i>y</i>-axis at <b>2</b>. 0 guesses that every line starts at the origin. "
                    "3 is the rate. 5 is the value for <i>x</i> = 1."))
    its.append(nmcq(fig(g1) + "By how much does <i>y</i> go up each time <i>x</i> goes up by 1?", 3, [2, 5, Fr(1, 3)],
                    "(0, 2), (1, 5), (2, 8): each step right, the line goes up <b>3</b>. 2 is the initial value. "
                    "5 is the value at <i>x</i> = 1, not the change. <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> "
                    "divides the change in <i>x</i> by the change in <i>y</i>.", frac))
    g2 = graph([(w, 4 + 2 * w) for w in range(9)], 8, 20, ystep=2, ylab=4, seg=[(0, 4, 8, 20)],
               xname="Time (weeks)", yname="Height (cm)", label="graph of a cedar seedling height over 8 weeks")
    its.append(nmcq(fig(g2) + "The graph shows the height of a cedar seedling. How tall is it after 6 weeks?", 16,
                    [6, 12, 14],
                    "Go up from 6 weeks to the line, then across: <b>16 cm</b>. "
                    "6 is read from the time axis. 12 cm is the growth only (6 × 2) without the 4 cm start. 14 cm is after 5 weeks.",
                    units("cm")))
    its.append(nmcq(fig(g2) + "After how many weeks is the seedling 10 cm tall?", 3, [10, 5, 24],
                    "Find 10 on the height axis, go across to the line, then down: <b>3 weeks</b>. "
                    "10 is the height, not the time. 5 weeks is 10 ÷ 2 and forgets the 4 cm start. 24 puts 10 in for the weeks.",
                    units("weeks")))
    its.append(nmcq(fig(g2) + "How much does the seedling grow each week?", 2, [4, 6, Fr(1, 2)],
                    "From 4 cm to 6 cm to 8 cm: it grows <b>2 cm</b> each week. 4 cm is the height at the start. "
                    "6 cm is the height after 1 week. 0.5 cm divides the weeks by the centimetres.", units("cm")))
    its.append(nmcq(fig(g2) + "Ji-woo reads the graph and says the seedling is 8 cm tall after 8 weeks. "
                    "What is the correct height after 8 weeks?", 20, [8, 16, 18],
                    "Go up from 8 weeks to the line and read the height axis: <b>20 cm</b>. "
                    "8 cm comes from reading the time axis instead of the height axis. 16 cm forgets the 4 cm start. 18 cm is after 7 weeks.",
                    units("cm")))
    g3 = graph([(h, 90 - 10 * h) for h in range(10)], 9, 100, ystep=10, ylab=20, seg=[(0, 90, 9, 0)],
               xname="Time (hours)", yname="Charge (%)", label="graph of a phone battery charge falling from 90 to 0")
    its.append(nmcq(fig(g3) + "The graph shows the charge on Mei’s phone battery. What is the charge after 4 hours?", 50,
                    [40, 4, 60],
                    "Go up from 4 hours to the line, then across: <b>50%</b>. 40% is how much charge was used. "
                    "4 is read from the time axis. 60% is after 3 hours.", PCT))
    its.append(nmcq(fig(g3) + "After how many hours is the charge 30%?", 6, [3, 12, 30],
                    "Find 30 on the charge axis, go across to the line, then down: <b>6 hours</b>. "
                    "3 hours is 30 ÷ 10 and forgets the start of 90%. 12 hours adds: (90 + 30) ÷ 10. 30 is the charge, not the time.",
                    units("hours")))
    its.append(nmcq(fig(g3) + "How much charge does the phone lose each hour?", 10, [90, 9, 80],
                    "90% to 80% to 70%: it loses <b>10%</b> each hour. 90% is the charge at the start. "
                    "9 is the number of hours until it is empty. 80% is the charge after 1 hour.", PCT))
    its.append(mcq(fig(g3) + "Is this a linear relation?", "Yes: the charge drops by the same amount each hour",
                   ["No: the line goes down", "Yes: the charge starts at 90%", "No: the line does not start at 0"],
                   "A relation is linear when it changes by the same amount for each step, so its graph is a straight line. "
                   "<b>Yes</b>: the charge drops 10% every hour. A line can go down and can start anywhere."))
    g4 = graph([(h, 6 - 2 * h) for h in range(9)], 8, 6, ymin=-10, ystep=1, ylab=2, seg=[(0, 6, 8, -10)],
               xname="Time (hours)", yname="Temperature (°C)", label="graph of temperature falling from 6 to −10 degrees")
    its.append(nmcq(fig(g4) + "The graph shows the temperature in Prince George after 8:00 p.m. "
                    "What is the temperature after 5 hours?", -4, [4, -2, 16],
                    "Go up from 5 hours to the line. The point is below the 0 line, at <b>−4 °C</b>. "
                    "4 °C forgets the point is below zero. −2 °C is after 4 hours. 16 °C adds 2 °C each hour instead of subtracting.",
                    units("°C")))
    its.append(mcq(fig(g4) + "At what time does the temperature reach 0 °C?", "11:00 p.m.",
                   ["8:00 p.m.", "2:00 a.m.", "10:00 p.m."],
                   "The line crosses 0 °C at 3 hours. 3 hours after 8:00 p.m. is <b>11:00 p.m.</b> "
                   "8:00 p.m. is the start, when it is 6 °C. 2:00 a.m. uses the 6 °C as a number of hours. 10:00 p.m. is 2 °C."))
    g5 = graph([(w, 30 + 15 * w) for w in range(9)], 8, 150, ystep=15, ylab=30, seg=[(0, 30, 8, 150)],
               xname="Time (weeks)", yname="Savings ($)", label="graph of Arjun savings growing from 30 to 150 dollars")
    its.append(nmcq(fig(g5) + "The graph shows Arjun’s savings for a new snowboard. How much has he saved after 4 weeks?",
                    90, [60, 75, 120],
                    "Go up from 4 weeks to the line, then across: <b>$90</b>. $60 is the money saved in 4 weeks (4 × 15) "
                    "without the $30 he had at the start. $75 is after 3 weeks. $120 multiplies 4 × 30.", dol))
    its.append(nmcq(fig(g5) + "How much does Arjun save each week?", 15, [30, 45, Fr(75, 4)],
                    "Each week the line goes up one grid line: $30, $45, $60. He saves <b>$15</b> a week. "
                    "$30 is what he had at the start. $45 is his total after 1 week. $18.75 is 150 ÷ 8 and forgets the $30 start.",
                    mon))
    its.append(nmcq(fig(g5) + "After how many weeks does Arjun have $120?", 6, [8, 10, 90],
                    "Find $120 on the savings axis, go across to the line, then down: <b>6 weeks</b>. "
                    "8 is 120 ÷ 15 and forgets the $30 start. 10 adds: (120 + 30) ÷ 15. 90 is the money saved, not the weeks.",
                    units("weeks")))
    its.append(mcq(fig(g5) + "The point (5, 105) is on the line. What does it mean?", "After 5 weeks, Arjun has $105",
                   ["After 105 weeks, Arjun has $5", "Arjun saves $105 each week", "Arjun saves $5 each week"],
                   "The first number is on the time axis and the second is on the savings axis: "
                   "<b>after 5 weeks, Arjun has $105</b>. Swapping them reads the wrong axis."))
    g6 = graph([(0, 0), (10, 2), (20, 4), (30, 6)], 30, 6, xstep=5, xlab=10, ystep=1, ylab=1, seg=[(0, 0, 30, 6)],
               xname="Time (minutes)", yname="Distance (km)", label="graph of Liam run, 6 km in 30 minutes")
    its.append(nmcq(fig(g6) + "The graph shows Liam’s run along the Stanley Park seawall. How far does he run each minute?",
                    Fr(1, 5), [5, 2, Fr(1, 2)],
                    "He runs 2 km in 10 minutes. 2 ÷ 10 = <b>0.2 km</b> each minute. "
                    "5 divides the wrong way: 10 ÷ 2 is minutes for each kilometre. 2 km is for 10 minutes, not 1. "
                    "0.5 km reads one small grid step on the time axis as 1 minute.", units("km")))
    its.append(nmcq(fig(g6) + "How many minutes does Liam take to run 5 km?", 25, [5, 1, 20],
                    "Find 5 km on the distance axis, go across to the line, then down: <b>25 minutes</b>. "
                    "5 is the distance. 1 multiplies 5 × 0.2. 20 minutes is the time for 4 km.", units("minutes")))
    return {"title": "Read a linear graph", "items": its}


# ============================================================ set 3: interpolate
def set_interp():
    its = []
    gi = graph([(0, 2), (2, 6), (4, 10), (6, 14)], 7, 16, ystep=1, ylab=2, seg=[(0, 2, 7, 16)],
               label="graph of a line through (0, 2), (2, 6), (4, 10) and (6, 14)")
    its.append(nmcq(fig(gi) + "Use the line to find <i>y</i> when <i>x</i> = 3.", 8, [6, 3, 10],
                    "<i>x</i> = 3 is halfway between the points at 2 and 4, so <i>y</i> is halfway between 6 and 10: <b>8</b>. "
                    "6 and 10 just take the nearest plotted point. 3 is the <i>x</i>-value."))
    its.append(nmcq(fig(gi) + "Use the line to find <i>x</i> when <i>y</i> = 12.", 5, [12, 4, 6],
                    "Find 12 on the <i>y</i>-axis, go across to the line and down: <b>5</b>, halfway between 4 and 6. "
                    "12 is the <i>y</i>-value. 4 and 6 stop at a plotted point instead of reading the line."))
    xs, ys = [0, 10, 20, 30], [50, 80, 110, 140]
    assert slope(xs, ys) == 3 and lv(3, 50, 15) == 95
    its.append(nmcq(tbl(xs, ys) + "The relation is linear. What is <i>y</i> when <i>x</i> = 15?", 95, [80, 45, 125],
                    "<i>y</i> goes up 30 for every 10 in <i>x</i>, so 3 for each 1. From <i>x</i> = 10 to 15: 80 + 5 × 3 = <b>95</b>. "
                    "80 is the nearest value in the table. 45 is 3 × 15 without the start of 50. 125 is the value for <i>x</i> = 25."))
    xs, ys = [2, 4, 6], [9, 15, 21]
    assert slope(xs, ys) == 3 and lv(3, 3, 5) == 18
    its.append(nmcq(tbl(xs, ys) + "The relation is linear. What is <i>y</i> when <i>x</i> = 5?", 18, [12, 15, 21],
                    "<i>y</i> goes up 6 for every 2 in <i>x</i>, so 3 for each 1. From <i>x</i> = 4: 15 + 3 = <b>18</b>. "
                    "12 subtracts 3, going the wrong way. 15 and 21 are the nearest values in the table."))
    its.append(nmcq("A line passes through (2, 7) and (6, 19). What is <i>y</i> at <i>x</i> = 4, halfway between?", 13,
                    [26, 12, 4],
                    "Halfway in <i>x</i> means halfway in <i>y</i>: (7 + 19) ÷ 2 = <b>13</b>. "
                    "26 adds 7 + 19 and forgets to halve. 12 is the change 19 − 7. 4 is the <i>x</i>-value."))
    xs, ys = [0, 4, 8], [90, 74, 58]
    assert slope(xs, ys) == -4 and lv(-4, 90, 6) == 66
    its.append(nmcq(tbl(xs, ys, ("Time (min)", "Temp. (°C)")) + "A cup of tea cools at a steady rate. "
                    "What is its temperature after 6 minutes?", 66, [82, 70, 62],
                    "It cools 16 °C in 4 minutes, so 4 °C each minute. 74 − 2 × 4 = <b>66 °C</b>. "
                    "82 °C adds 8 °C, going the wrong way for cooling tea. 70 °C is after 5 minutes. 62 °C is after 7 minutes.",
                    units("°C")))
    gh = graph([(0, 600), (1, 800), (2, 1000), (3, 1200)], Fr(7, 2), 1300, xstep=Fr(1, 2), xlab=1, ymin=500,
               ystep=100, ylab=100, seg=[(0, 600, 3, 1200)], xname="Time (hours)", yname="Elevation (m)",
               label="graph of a hiker elevation from 600 m to 1200 m in 3 hours")
    its.append(nmcq(fig(gh) + "A hiker near Whistler climbs at a steady rate. What is the elevation after 1.5 hours?",
                    900, [800, 1000, 300],
                    "1.5 hours is halfway between 1 and 2 hours, so the elevation is halfway between 800 m and 1000 m: <b>900 m</b>. "
                    "800 m and 1000 m take the nearest plotted point. 300 m is the climb (1.5 × 200) without the 600 m start.",
                    units("m")))
    its.append(nmcq(fig(gh) + "After how many hours is the hiker at 1100 m?", Fr(5, 2), [2, 3, Fr(11, 2)],
                    "1100 m is halfway between 1000 m (2 hours) and 1200 m (3 hours): <b>2.5 hours</b>. "
                    "2 and 3 hours take the nearest plotted point. 5.5 hours is 1100 ÷ 200 and forgets the 600 m start.",
                    units("hours")))
    assert Fr(25 - 40, 10) == Fr(-3, 2) and 40 + Fr(-3, 2) * 4 == 34
    its.append(nmcq("A linear relation passes through (10, 40) and (20, 25). What is <i>y</i> when <i>x</i> = 14?", 34,
                    [46, Fr(65, 2), 19],
                    "The rate is (25 − 40) ÷ (20 − 10) = −1.5. From <i>x</i> = 10: 40 − 4 × 1.5 = <b>34</b>. "
                    "46 adds 6, going the wrong way. 32.5 is halfway, but 14 is not halfway between 10 and 20. "
                    "19 takes 6 from 25, the wrong end."))
    its.append(mcq("A table shows a plant’s height every week from week 0 to week 10. Which question uses interpolation?",
                   "How tall was it in week 7.5?",
                   ["How tall will it be in week 15?", "How tall was it before week 0?", "When will it reach 2 m?"],
                   "Interpolation finds values <b>between</b> the data. Week 7.5 is between week 0 and week 10. "
                   "Week 15, before week 0, and a height past the data are extrapolation."))
    xs, ys = [0, 3, 6, 9, 12], [5, "?", 17, 23, 29]
    assert lv(2, 5, 3) == 11
    its.append(nmcq(tbl(xs, ys) + "The relation is linear. What value is missing?", 11, [8, 12, 14],
                    "<i>x</i> = 3 is halfway between 0 and 6, so <i>y</i> is halfway between 5 and 17: <b>11</b>. "
                    "8 adds the <i>x</i>-step 3 to 5. 12 is the change 17 − 5. 14 takes 3 from 17."))
    gr = graph([(0, 20), (4, 60)], 5, 70, xstep=Fr(1, 2), xlab=1, ystep=5, ylab=10, seg=[(0, 20, 5, 70)],
               xname="Time (hours)", yname="Water (L)", tags={(0, 20): "20 L", (4, 60): "60 L"},
               label="graph of water in a rain barrel from 20 L to 60 L in 4 hours")
    its.append(nmcq(fig(gr) + "Rain fills a barrel in Vancouver at a steady rate. How much water is in it after 2.5 hours?",
                    45, [40, 25, 50],
                    "It gains 40 L in 4 hours, so 10 L each hour. 20 + 2.5 × 10 = <b>45 L</b>. "
                    "40 L is after 2 hours. 25 L is 2.5 × 10 without the 20 L start. 50 L is after 3 hours.", units("L")))
    its.append(nmcq(fig(gr) + "After how many hours does the barrel hold 35 L?", Fr(3, 2), [Fr(7, 2), 2, 1],
                    "It must gain 35 − 20 = 15 L at 10 L each hour: 15 ÷ 10 = <b>1.5 hours</b>. "
                    "3.5 hours is 35 ÷ 10 and forgets the 20 L start. 1 and 2 hours round to a whole hour.", units("hours")))
    its.append(mcq("Why can you interpolate between two data points of a linear relation?",
                   "The values between them lie on the same straight line",
                   ["Every linear relation starts at 0", "Only whole numbers are allowed", "The line always goes up"],
                   "In a linear relation the rate is constant, so every value between two points lies on <b>the same straight line</b>. "
                   "Lines can start anywhere, can go down, and can use any <i>x</i> between the points."))
    assert Fr(1 - 9, 4) == -2 and lv(-2, 5, 1) == 3
    its.append(nmcq("A line passes through (−2, 9) and (2, 1). What is <i>y</i> when <i>x</i> = 1?", 3, [5, 7, -1],
                    "The rate is (1 − 9) ÷ (2 − (−2)) = −8 ÷ 4 = −2. From (2, 1), go back 1: 1 + 2 = <b>3</b>. "
                    "5 is the value at <i>x</i> = 0. 7 moves the wrong way from (−2, 9). −1 is the value for <i>x</i> = 3."))
    assert lv(Fr(1, 2), 3, 3) == Fr(9, 2)
    its.append(nmcq("A line passes through (0, 3) and (4, 5). What is <i>y</i> when <i>x</i> = 3?", Fr(9, 2), [9, 4, 5],
                    "The rate is (5 − 3) ÷ 4 = 0.5. 3 + 3 × 0.5 = <b>4.5</b>. "
                    "9 uses the rate 4 ÷ 2 = 2, divided the wrong way. 4 is the halfway value, but 3 is not halfway. 5 is the value at <i>x</i> = 4."))
    xs, ys = [0, 5, 10, 15], [200, 170, 140, 110]
    assert slope(xs, ys) == -6 and lv(-6, 200, 7) == 158
    its.append(nmcq(tbl(xs, ys) + "The relation is linear. For which value of <i>x</i> is <i>y</i> = 158?", 7, [2, 8, 6],
                    "<i>y</i> goes down 6 for each 1 in <i>x</i>. From 200 to 158 is 42: 42 ÷ 6 = <b>7</b>. "
                    "2 starts from 170 but forgets that 170 is at <i>x</i> = 5. 8 is how far back from <i>x</i> = 15, "
                    "not the <i>x</i>-value. 6 is one step short."))
    assert lv(-4, 78, 2) == 70 and lv(-4, 78, 6) == 54 and lv(-4, 78, 5) == 58
    its.append(nmcq("Soup is 70 °C after 2 minutes and 54 °C after 6 minutes. It cools at a steady rate. "
                    "What is its temperature after 5 minutes?", 58, [62, 82, 50],
                    "It cools 16 °C in 4 minutes, so 4 °C each minute. 70 − 3 × 4 = <b>58 °C</b>. "
                    "62 °C is the halfway value, after 4 minutes. 82 °C adds 12 °C, the wrong way for cooling soup. "
                    "50 °C goes from 54 °C the wrong way: back in time it should be warmer.", units("°C")))
    its.append(mcq("A graph shows the number of chairs, <i>y</i>, around <i>x</i> tables. Why should you not interpolate at <i>x</i> = 2.5?",
                   "You cannot have half a table",
                   ["The graph is not linear", "2.5 is too far from the data", "The rate is negative"],
                   "Tables come in whole numbers, so the relation is discrete. Interpolate only where the in-between values make sense. "
                   "<b>There is no half a table.</b>"))
    assert lv(3, 12, 1) == 15
    its.append(nmcq("In Kelowna it is 12 °C at 9:00 a.m. and 24 °C at 1:00 p.m. The temperature rises at a steady rate. "
                    "What is the temperature at 10:00 a.m.?", 15, [18, 13, 21],
                    "From 9:00 a.m. to 1:00 p.m. is 4 hours, so it rises 12 ÷ 4 = 3 °C each hour. 12 + 3 = <b>15 °C</b>. "
                    "18 °C is the halfway value, at 11:00 a.m. 13 °C adds 1 °C. 21 °C is at 12:00 p.m.", units("°C")))
    return {"title": "Interpolate between points", "items": its}


# ============================================================ set 4: extrapolate
def set_extrap():
    its = []
    xs, ys = [0, 1, 2, 3, 4], [3, 5, 7, 9, 11]
    assert slope(xs, ys) == 2 and lv(2, 3, 7) == 17
    its.append(nmcq(tbl(xs, ys) + "The relation continues in the same way. What is <i>y</i> when <i>x</i> = 7?", 17,
                    [14, 15, 19],
                    "<i>y</i> goes up 2 each step: 11, 13, 15, <b>17</b>. Or use <i>y</i> = 2<i>x</i> + 3: 2 × 7 + 3 = 17. "
                    "14 is 2 × 7 without the start of 3. 15 is the value for <i>x</i> = 6 and 19 is for <i>x</i> = 8."))
    assert lv(2, 3, -2) == -1
    its.append(nmcq(tbl(xs, ys) + "Extend the table to the left. What is <i>y</i> when <i>x</i> = −2?", -1, [7, 1, -4],
                    "Going left, <i>y</i> goes <b>down</b> 2 each step: 3, 1, <b>−1</b>. "
                    "7 adds 2 each step, going the wrong way. 1 is the value for <i>x</i> = −1. −4 is 2 × (−2) without the start of 3."))
    ge1 = graph([(x, 2 * x + 2) for x in range(5)], 6, 14, ystep=1, ylab=2,
                label="graph of five points from (0, 2) to (4, 10)")
    its.append(nmcq(fig(ge1) + "The pattern continues past the grid. What is <i>y</i> when <i>x</i> = 9?", 20, [18, 22, 10],
                    "The points go up 2 each step from 2, so <i>y</i> = 2<i>x</i> + 2. For <i>x</i> = 9: 2 × 9 + 2 = <b>20</b>. "
                    "18 forgets the start of 2. 22 is the value for <i>x</i> = 10. 10 is the last point on the grid."))
    xs, ys = [0, 1, 2, 3], [40, 35, 30, 25]
    assert slope(xs, ys) == -5 and lv(-5, 40, 8) == 0
    its.append(nmcq(tbl(xs, ys) + "The relation continues in the same way. What is <i>y</i> when <i>x</i> = 8?", 0,
                    [65, 5, -5],
                    "<i>y</i> goes down 5 each step: 40 − 8 × 5 = <b>0</b>. "
                    "65 adds 5 each step, going the wrong way. 5 is the value for <i>x</i> = 7 and −5 is for <i>x</i> = 9."))
    xs, ys = [2, 3, 4, 5], [14, 11, 8, 5]
    assert slope(xs, ys) == -3 and lv(-3, 20, 0) == 20
    its.append(nmcq(tbl(xs, ys) + "Extend the table back to <i>x</i> = 0. What is <i>y</i>?", 20, [8, 17, 23],
                    "Going back, the values go <b>up</b> 3 each step: 14, 17, <b>20</b>. "
                    "8 subtracts 3 twice, going the wrong way. 17 is the value for <i>x</i> = 1 and 23 is for <i>x</i> = −1."))
    its.append(mcq("A table shows a plant’s height every week from week 0 to week 10. Which question uses extrapolation?",
                   "How tall will it be in week 15?",
                   ["How tall was it in week 4?", "How tall was it in week 7.5?", "How tall was it in week 10?"],
                   "Extrapolation predicts values <b>beyond</b> the data. Week 15 is past week 10. "
                   "Weeks 4, 7.5 and 10 are inside the data."))
    assert lv(-3, 90, 10) == 60
    its.append(nmcq("Tea is 90 °C. Ava measures it for 5 minutes: 90, 87, 84, 81, 78, 75 °C. "
                    "If it keeps cooling at this rate, what is its temperature after 10 minutes?", 60, [120, 63, 30],
                    "It cools 3 °C each minute: 90 − 10 × 3 = <b>60 °C</b>. "
                    "120 °C adds, the wrong way for cooling tea. 63 °C is after 9 minutes. 30 °C is 10 × 3, the drop only.",
                    units("°C")))
    its.append(mcq("Tea at 90 °C cools 3 °C each minute for the first 5 minutes. A linear model predicts −30 °C after 40 minutes. "
                   "Why is this prediction wrong?",
                   "Tea stops cooling near room temperature",
                   ["Temperatures cannot be below 0 °C", "The rate should be positive", "The tea should be warmer than 90 °C"],
                   "Real tea cools to about room temperature and then stays there. Extrapolating far beyond the data can give "
                   "impossible answers. <b>The linear pattern only holds for a while.</b> Outdoor temperatures in BC can be below 0 °C."))
    ge2 = graph([(2, 7), (3, 9), (4, 11), (5, 13)], 6, 14, ystep=1, ylab=2,
                label="graph of four points from (2, 7) to (5, 13)")
    its.append(nmcq(fig(ge2) + "Extend the pattern back to <i>x</i> = 0. What is <i>y</i>?", 3, [11, 5, 7],
                    "Each step right adds 2, so each step left takes away 2: 7, 5, <b>3</b>. "
                    "11 adds 2 twice, going the wrong way. 5 is the value for <i>x</i> = 1. 7 is the first plotted point."))
    xs, ys = [1, 2, 3], [32, 28, 24]
    assert slope(xs, ys) == -4 and lv(-4, 36, 9) == 0
    its.append(nmcq(tbl(xs, ys, ("Day", "Snow (cm)")) + "Snow on a deck in Kamloops melts at a steady rate. "
                    "On which day will the snow be gone?", 9, [8, 6, 10],
                    "It melts 4 cm a day. On day 3 there is 24 cm left: 24 ÷ 4 = 6 more days, so day 3 + 6 = <b>day 9</b>. "
                    "8 is 32 ÷ 4 and forgets the table starts at day 1. 6 is the number of days after day 3. 10 is one day too many.",
                    lambda v: "Day " + n(v)))
    xs, ys = [3, 4, 5], [55, 70, 85]
    assert slope(xs, ys) == 15 and lv(15, 10, 10) == 160
    its.append(nmcq(tbl(xs, ys, ("Week", "Savings ($)")) + "Owen saves the same amount each week. "
                    "If he keeps saving, how much will he have after 10 weeks?", 160, [170, 145, 150],
                    "He saves $15 a week. From week 5 to week 10 is 5 weeks: 85 + 5 × 15 = <b>$160</b>. "
                    "$170 doubles the week 5 amount, but he started with money. $145 is week 9. $150 is 10 × 15 and forgets his start.",
                    dol))
    its.append(nmcq(tbl(xs, ys, ("Week", "Savings ($)")) + "How much did Owen have at the start (week 0)?", 10,
                    [100, 40, 0],
                    "Going back, take away $15 each week: 55 − 3 × 15 = <b>$10</b>. "
                    "$100 adds $45, going the wrong way. $40 goes back only one week. $0 assumes he started with nothing.", dol))
    xs, ys = [0, 1, 2, 3], [9, 6, 3, 0]
    assert slope(xs, ys) == -3 and lv(-3, 9, 5) == -6
    its.append(nmcq(tbl(xs, ys, ("Hours", "Temp. (°C)")) + "The temperature keeps falling at the same rate. "
                    "What is it after 5 hours?", -6, [6, -3, 24],
                    "It falls 3 °C each hour: 0, −3, <b>−6 °C</b>. "
                    "6 °C forgets the sign below zero. −3 °C is after 4 hours. 24 °C adds 3 °C each hour, the wrong way.",
                    units("°C")))
    ge4 = graph([(x, 4 - 2 * x) for x in range(5)], 5, 6, ymin=-6, ystep=1, ylab=2,
                label="graph of five points from (0, 4) to (4, −4)")
    assert lv(-2, 4, 6) == -8
    its.append(nmcq(fig(ge4) + "The pattern continues. For which value of <i>x</i> is <i>y</i> = −8?", 6, [-2, 4, 12],
                    "The points go down 2 each step from 4: <i>y</i> = −2<i>x</i> + 4. Solve −2<i>x</i> + 4 = −8: "
                    "−2<i>x</i> = −12, so <i>x</i> = <b>6</b>. −2 goes left, the wrong way: there <i>y</i> = 8. "
                    "4 is −8 ÷ (−2) and forgets the start of 4. 12 forgets to divide by 2."))
    its.append(mcq("Data for a linear relation goes from <i>x</i> = 0 to <i>x</i> = 10. Which prediction is most reliable?",
                   "<i>y</i> at <i>x</i> = 11", ["<i>y</i> at <i>x</i> = 50", "<i>y</i> at <i>x</i> = 100", "<i>y</i> at <i>x</i> = 1000"],
                   "The closer a prediction is to the data, the more you can trust it. <b><i>x</i> = 11</b> is just past the data. "
                   "Far beyond the data, the pattern may change."))
    assert lv(3, -2, 4) == 10 and lv(3, -2, 6) == 16 and lv(3, -2, 10) == 28
    its.append(nmcq("A line passes through (4, 10) and (6, 16). What is <i>y</i> when <i>x</i> = 10?", 28, [25, 22, 34],
                    "The rate is (16 − 10) ÷ (6 − 4) = 3. From (6, 16): 16 + 4 × 3 = <b>28</b>. "
                    "25 assumes the line goes through (0, 0): 10 × 2.5. 22 is the value for <i>x</i> = 8 and 34 is for <i>x</i> = 12."))
    its.append(nmcq("A line passes through (4, 10) and (6, 16). What is <i>y</i> when <i>x</i> = 0?", -2, [22, 4, 10],
                    "Going back, take away 3 for each step: 10 − 4 × 3 = <b>−2</b>. "
                    "22 adds 12, going the wrong way. 4 goes back only 2 steps. 10 is the value at <i>x</i> = 4."))
    assert lv(Fr(-3, 2), 30, 16) == 6
    its.append(nmcq("A candle is 30 cm tall. Chloe records its height for 4 hours: 30, 28.5, 27, 25.5, 24 cm. "
                    "If it keeps burning at this rate, after how many hours will it be 6 cm tall?", 16, [4, 20, 24],
                    "It burns 1.5 cm each hour. It must lose 30 − 6 = 24 cm: 24 ÷ 1.5 = <b>16 hours</b>. "
                    "4 hours is 6 ÷ 1.5. 20 hours is when it is all gone. 24 is the centimetres lost, not the hours.",
                    units("hours")))
    gc = graph([(0, 0), (1, 90), (2, 180), (3, 270)], 4, 360, ystep=30, ylab=90, seg=[(0, 0, 3, 270)],
               xname="Time (hours)", yname="Distance (km)", label="graph of distance driven, 270 km in 3 hours")
    its.append(nmcq(fig(gc) + "Mateo’s family drives on the Trans-Canada Highway at a steady speed. "
                    "If they keep this speed, how far will they go in 5 hours?", 450, [270, 360, 540],
                    "They drive 90 km each hour: 5 × 90 = <b>450 km</b>. "
                    "270 km is the last point on the graph. 360 km is after 4 hours. 540 km doubles the 3-hour distance, which is 6 hours.",
                    units("km")))
    assert lv(-3, 29, 1) == 26
    its.append(nmcq(tbl([3, 4, 5], [20, 17, 14]) + "Nadia extends the table back to <i>x</i> = 1 and gets <i>y</i> = 14. "
                    "What is the correct value?", 26, [14, 23, 17],
                    "Going forward, <i>y</i> goes down 3. Going <b>back</b>, it goes up 3: 20, 23, <b>26</b>. "
                    "Nadia subtracted 6, extrapolating the wrong way. 23 is the value for <i>x</i> = 2. 17 is in the table at <i>x</i> = 4."))
    return {"title": "Extrapolate beyond the data", "items": its}


# ============================================================ set 5: equations and word problems
def set_words():
    its = []
    C = lambda d: 2 * Fr(d) + 4
    its.append(eqmcq("A taxi charges $4.00 to start plus $2.00 for each kilometre. Which equation gives the cost, <i>C</i>, "
                     "in dollars, for <i>d</i> kilometres?", (2, 4), [(4, 2), (6, 0), (2, 0)],
                     "Each kilometre adds $2, so 2 multiplies <i>d</i>. The $4 is paid once: <b>%s</b>. "
                     "%s swaps the start fee and the rate. %s charges $6 for every kilometre. %s forgets the start fee."
                     % (eq(2, 4, "d", "C"), eq(4, 2, "d", "C"), eq(6, 0, "d", "C"), eq(2, 0, "d", "C")),
                     [0, 1, 2], [4, 6, 8], x="d", y="C"))
    assert C(7) == 18
    its.append(nmcq("A taxi costs <i>C</i> = 2<i>d</i> + 4 dollars for <i>d</i> km. How much is a 7 km ride?", 18, [42, 14, 30],
                    "<i>C</i> = 2 × 7 + 4 = 14 + 4 = <b>$18.00</b>. "
                    "$42.00 adds first: (2 + 4) × 7. $14.00 forgets the start fee. $30.00 swaps the numbers: 4 × 7 + 2.", mon))
    assert C(Fr(21, 2)) == 25
    its.append(nmcq("A taxi costs <i>C</i> = 2<i>d</i> + 4 dollars for <i>d</i> km. Kai pays $25.00. How long was the ride?",
                    Fr(21, 2), [Fr(25, 2), Fr(29, 2), 21],
                    "Solve 2<i>d</i> + 4 = 25. Subtract 4: 2<i>d</i> = 21. Divide by 2: <i>d</i> = <b>10.5 km</b>. "
                    "12.5 km is 25 ÷ 2 and forgets the start fee. 14.5 km adds the fee. 21 km forgets to divide.", units("km")))
    gt = graph([(d, C(d)) for d in range(0, 9, 2)], 8, 20, ystep=2, ylab=4, seg=[(0, 4, 8, 20)],
               xname="Distance (km)", yname="Cost ($)", label="graph of taxi cost, a line from (0, 4) to (8, 20)")
    its.append(mcq(fig(gt) + "The graph shows the taxi fare. What does the point where the line meets the cost axis show?",
                   "The $4.00 paid before the taxi moves",
                   ["The cost for each kilometre", "The cost of an 8 km ride", "The distance for $4.00"],
                   "At 0 km the cost is already $4. That is the start fee, <b>paid before the taxi moves</b>. "
                   "The cost for each kilometre is the rate, $2."))
    T = lambda m: 84 - 3 * Fr(m)
    its.append(eqmcq("Soup is 84 °C and cools 3 °C each minute. Which equation gives its temperature, <i>T</i>, in °C, "
                     "after <i>m</i> minutes?", (-3, 84), [(3, 84), (84, -3), (-3, 81)],
                     "The soup starts at 84 °C and loses 3 °C a minute, so the rate is −3: <b>%s</b>. "
                     "%s makes the soup get hotter. %s swaps the rate and the start. %s starts from the temperature after 1 minute."
                     % (eq(-3, 84, "m", "T"), eq(3, 84, "m", "T"), eq(84, -3, "m", "T"), eq(-3, 81, "m", "T")),
                     [0, 1, 2], [84, 81, 78], x="m", y="T"))
    assert T(6) == 66
    its.append(nmcq("Soup cools by the rule <i>T</i> = −3<i>m</i> + 84. What is its temperature after 6 minutes?", 66,
                    [102, 18, 69],
                    "<i>T</i> = −3 × 6 + 84 = −18 + 84 = <b>66 °C</b>. "
                    "102 °C adds the 18 degrees, but soup cools. 18 °C is the drop only. 69 °C is after 5 minutes.", units("°C")))
    assert T(8) == 60
    its.append(nmcq("Soup cools by the rule <i>T</i> = −3<i>m</i> + 84. After how many minutes is it 60 °C?", 8,
                    [20, 24, 48],
                    "Solve −3<i>m</i> + 84 = 60. It must cool 84 − 60 = 24 °C: 24 ÷ 3 = <b>8 minutes</b>. "
                    "20 is 60 ÷ 3 and forgets the start. 24 is degrees, not minutes. 48 adds: (84 + 60) ÷ 3.", units("minutes")))
    its.append(mcq("In the taxi rule <i>C</i> = 2.25<i>d</i> + 3.75, what does 2.25 mean?", "The cost for each kilometre",
                   ["The cost before the ride starts", "The total cost of the ride", "The number of kilometres"],
                   "2.25 multiplies the distance, so it is the rate: <b>$2.25 for each kilometre</b>. "
                   "$3.75 is the start fee, paid before the ride. The total depends on <i>d</i>."))
    xs, ys = [3, 7], [Fr(23, 2), Fr(43, 2)]
    its.append(eqmcq("A 3 km taxi ride costs $11.50 and a 7 km ride costs $21.50. The cost is linear. "
                     "Which equation gives the cost, <i>C</i>, for <i>d</i> km?", (Fr(5, 2), 4),
                     [(Fr(5, 2), 0), (4, Fr(5, 2)), (10, 4)],
                     "The rate is (21.50 − 11.50) ÷ (7 − 3) = 10 ÷ 4 = 2.5. Start fee: 11.50 − 3 × 2.5 = 4. <b>%s</b>. "
                     "%s forgets the start fee. %s swaps the rate and the fee. %s uses the $10 change without dividing by 4 km."
                     % (eq(Fr(5, 2), 4, "d", "C"), eq(Fr(5, 2), 0, "d", "C"), eq(4, Fr(5, 2), "d", "C"), eq(10, 4, "d", "C")),
                     xs, ys, x="d", y="C"))
    assert 2 * 4 + 4 == Fr(3, 2) * 4 + 6 == 12
    its.append(nmcq("Taxi A charges $4.00 plus $2.00 per km. Taxi B charges $6.00 plus $1.50 per km. "
                    "For what distance do they cost the same?", 4, [2, 12, Fr(1, 2)],
                    "Set them equal: 2<i>d</i> + 4 = 1.5<i>d</i> + 6. Then 0.5<i>d</i> = 2, so <i>d</i> = <b>4 km</b>. Both cost $12. "
                    "2 km is the difference in start fees. 12 is the cost. 0.5 is the difference in rates.", units("km")))
    assert 2 * 10 + 4 == 24 and Fr(3, 2) * 10 + 6 == 21
    its.append(mcq("Taxi A charges $4.00 plus $2.00 per km. Taxi B charges $6.00 plus $1.50 per km. "
                   "Which is cheaper for a 10 km ride?", "Taxi B, by $3.00",
                   ["Taxi A, by $3.00", "They cost the same", "Taxi B, by $0.50"],
                   "Taxi A: 2 × 10 + 4 = $24.00. Taxi B: 1.5 × 10 + 6 = $21.00. <b>Taxi B is cheaper by $3.00.</b> "
                   "They cost the same only at 4 km. $0.50 is the difference in rates for 1 km."))
    gco = graph([(0, 80), (2, 72), (4, 64), (6, 56)], 10, 90, ystep=10, ylab=10, seg=[(0, 80, 6, 56)],
                xname="Time (minutes)", yname="Temperature (°C)", label="graph of coffee cooling from 80 to 56 degrees in 6 minutes")
    its.append(eqmcq(fig(gco) + "Which equation matches the cooling coffee? (<i>T</i> is the temperature and <i>m</i> is minutes.)",
                     (-4, 80), [(4, 80), (-8, 80), (-4, 72)],
                     "It loses 8 °C every 2 minutes, so 4 °C each minute. It starts at 80 °C: <b>%s</b>. "
                     "%s gets hotter. %s uses the change for 2 minutes as the rate. %s starts at the second point."
                     % (eq(-4, 80, "m", "T"), eq(4, 80, "m", "T"), eq(-8, 80, "m", "T"), eq(-4, 72, "m", "T")),
                     [0, 2, 4, 6], [80, 72, 64, 56], x="m", y="T"))
    assert lv(-4, 80, 10) == 40
    its.append(nmcq(fig(gco) + "If the coffee keeps cooling at this rate, after how many minutes will it be 40 °C?", 10,
                    [5, 40, 12],
                    "Solve −4<i>m</i> + 80 = 40: it must cool 40 °C, and 40 ÷ 4 = <b>10 minutes</b>. "
                    "5 uses 8 °C per minute. 40 is read from the temperature axis. 12 goes one step of 2 minutes too far.",
                    units("minutes")))
    assert 10 * Fr(5, 2) + 15 == 40
    its.append(nmcq("Ryan rents a kayak in Nanaimo for $15.00 plus $10.00 an hour. How much does he pay for 2.5 hours?", 40,
                    [Fr(125, 2), 25, 45],
                    "<i>C</i> = 10 × 2.5 + 15 = 25 + 15 = <b>$40.00</b>. "
                    "$62.50 adds first: (15 + 10) × 2.5. $25.00 forgets the $15. $45.00 rounds up to 3 hours.", mon))
    assert 40 * 8 + 80 == 400
    its.append(nmcq("Simran’s class has $80 for the Terry Fox Run and raises $40 more each week. "
                    "After how many weeks will they have $400?", 8, [10, 12, 320],
                    "Solve 40<i>w</i> + 80 = 400. 400 − 80 = 320 and 320 ÷ 40 = <b>8 weeks</b>. "
                    "10 is 400 ÷ 40 and forgets the $80. 12 adds: (400 + 80) ÷ 40. 320 forgets to divide.", units("weeks")))
    its.append(nmcq("At 2:00 p.m. a pot of soup is 90 °C. At 2:10 p.m. it is 70 °C. It cools at a steady rate. "
                    "By how much does the temperature change each minute?", -2, [2, -20, Fr(-1, 2)],
                    "(70 − 90) ÷ 10 = −20 ÷ 10 = <b>−2 °C</b> each minute. "
                    "2 °C forgets that the soup is cooling. −20 °C is the change in 10 minutes. −0.5 divides the wrong way.",
                    units("°C")))
    assert Fr(23 - Fr(65, 4), 3) == Fr(9, 4) and Fr(65, 4) - 5 * Fr(9, 4) == 5
    its.append(nmcq("A 5 km taxi ride costs $16.25 and an 8 km ride costs $23.00. The cost is linear. What is the start fee?",
                    5, [Fr(55, 2), 14, Fr(27, 4)],
                    "The rate is (23.00 − 16.25) ÷ 3 = $2.25 per km. Go back 5 km from $16.25: 16.25 − 5 × 2.25 = <b>$5.00</b>. "
                    "$27.50 adds, extrapolating the wrong way. $14.00 goes back only 1 km. $6.75 is the change between the rides.", mon))
    assert 340 - 80 * 3 == 100
    its.append(nmcq("Zara is 340 km from home and drives toward home at 80 km/h. After how many hours is she 100 km from home?",
                    3, [Fr(5, 4), Fr(11, 2), Fr(17, 4)],
                    "Solve 340 − 80<i>t</i> = 100. She must drive 240 km: 240 ÷ 80 = <b>3 hours</b>. "
                    "1.25 hours is 100 ÷ 80. 5.5 hours adds: (340 + 100) ÷ 80. 4.25 hours is the whole trip home.", units("hours")))
    its.append(mcq("Which situation matches %s?" % eq(-5, 60),
                   "A tank holds 60 L and drains 5 L each minute",
                   ["A tank holds 60 L and fills 5 L each minute", "A tank holds 5 L and drains 60 L each minute",
                    "A tank holds 5 L and fills 60 L each minute"],
                   "60 is the initial value: the tank starts with 60 L. The rate −5 means it loses 5 L each minute. "
                   "<b>It holds 60 L and drains 5 L each minute.</b>"))
    assert C(10) + 3 == 27
    its.append(nmcq("A taxi charges $4.00 plus $2.00 per km. Chloe pays $27.00, which includes a $3.00 tip. How long was the ride?",
                    10, [Fr(23, 2), Fr(27, 2), 12],
                    "Take off the tip: 27 − 3 = $24. Solve 2<i>d</i> + 4 = 24: 2<i>d</i> = 20, so <i>d</i> = <b>10 km</b>. "
                    "11.5 km forgets the tip. 13.5 km is 27 ÷ 2. 12 km forgets the $4 start fee.", units("km")))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 10, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Equations and word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def lesson_graph():
    pts = [(0, 30), (2, 50), (4, 70)]
    assert all(10 * x + 30 == y for x, y in pts)
    return graph(pts + [(3, 60), (7, 100)], 8, 110, ystep=10, ylab=20, seg=[(0, 30, 4, 70)], dash=[(4, 70, 8, 110)],
                 xname="Time (hours)", yname="Water (L)", tags={(3, 60): "60", (7, 100): "100"},
                 label="graph of water in a tank: data from 0 to 4 hours, dashed extension to 8 hours")


def body_html():
    return (
        "<h2>From a table of values to a graph</h2>"
        "<p>A <b>linear relation</b> changes by the same amount for each step. Its graph is a straight line. "
        "To graph it, make a table of values, turn each column into a point (<i>x</i>, <i>y</i>), and plot it: "
        "across for <i>x</i> first, then up or down for <i>y</i>.</p>"
        + table(["<i>x</i>", "0", "1", "2", "3"], [["<i>y</i> = 2<i>x</i> + 1", "1", "3", "5", "7"]]) +
        "<p>Join the points with a line when every value in between makes sense, like time or distance (<b>continuous</b>). "
        "Leave them as separate points for things you count, like tickets or tables (<b>discrete</b>).</p>"
        "<h2>Read, interpolate and extrapolate</h2>"
        "<p>To read a graph, start on the axis you know, go to the line, then across or down to the other axis. "
        "<b>Interpolation</b> finds a value <b>between</b> data points. <b>Extrapolation</b> extends the line to predict "
        "a value <b>beyond</b> the data.</p>"
        "<figure class='sn-fig'>" + lesson_graph() +
        "<figcaption>Data for 0 to 4 hours (solid). Interpolate at 3 hours: 60 L. Extrapolate (dashed) to 7 hours: 100 L.</figcaption></figure>"
        + ex("Interpolate", "A tank has 30 L at 0 hours and 50 L at 2 hours. It fills at a steady rate. How much is in it at 3 hours?",
             "The rate is (50 − 30) ÷ 2 = 10 L each hour. From 2 hours: 50 + 10 = 60.", "60 L")
        + ex("Extrapolate", "The tank keeps filling at the same rate. When does it hold 100 L?",
             "The equation is <i>W</i> = 10<i>t</i> + 30. Solve 10<i>t</i> + 30 = 100: 10<i>t</i> = 70, so <i>t</i> = 7.", "7 hours")
        + ex("Taxi fare", "A taxi charges $4.00 plus $2.00 for each kilometre. What is the equation, and how much is a 7 km ride?",
             "The start fee is the initial value and the cost per kilometre is the rate: <i>C</i> = 2<i>d</i> + 4. "
             "For 7 km: 2 × 7 + 4 = 18.", "$18.00") +
        "<p>Predictions close to the data are the most reliable. Far beyond the data, the pattern may change: "
        "cooling soup stops at room temperature, it does not keep falling forever.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Reading the wrong axis: answering with the <i>x</i>-value", "Start on the axis you know and read the answer on the other axis"],
            ["Plotting (<i>y</i>, <i>x</i>)", "Go across for <i>x</i> first, then up or down for <i>y</i>"],
            ["Extrapolating the wrong way: subtracting when going back on a falling line",
             "Going back, do the opposite of the rate: a falling line gets higher to the left"],
            ["Taking the nearest data point instead of interpolating", "Use the rate to find the exact value between the points"],
            ["Using the change in <i>y</i> as the rate when <i>x</i> skips numbers", "Divide the change in <i>y</i> by the change in <i>x</i>"],
            ["Forgetting the initial value, like a taxi’s start fee", "Add the value at <i>x</i> = 0 after multiplying by the rate"],
        ])
    )


FAQ = [
    {"q": "What do Grade 9 students learn about linear relations in BC?",
     "a": "The BC Mathematics 9 curriculum covers two-variable linear relations: making tables of values, graphing them, reading the graphs, and using interpolation and extrapolation to find values between and beyond the data."},
    {"q": "What is the difference between interpolation and extrapolation?",
     "a": "Interpolation finds a value between known data points, such as 3 hours when you have data for 2 and 4 hours. Extrapolation extends the pattern to predict a value outside the data, such as 7 hours when the data stops at 4."},
    {"q": "Why can extrapolation be wrong?",
     "a": "Extrapolation assumes the pattern keeps going in the same way. Far from the data it may not: cooling soup stops at room temperature, so a linear prediction for a long time later can give an impossible answer."},
    {"q": "How do you write the equation of a linear relation from a word problem?",
     "a": "The amount that changes each step is the rate, which multiplies the variable, and the starting amount is the initial value. A taxi that charges $4.00 plus $2.00 per kilometre has C = 2d + 4."},
]


def gen():
    rnd = random.Random(59806)
    sets = [set_tables(), set_read(), set_interp(), set_extrap(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "linear-relations-and-graphs",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Linear Relations and Graphs: Interpolation and Extrapolation",
        "seo_title": "Grade 9 Linear Relations Worksheets: Graphing, Interpolation and Extrapolation (BC Math, Free)",
        "short_title": "Linear relations and graphs",
        "domain": "Patterning",
        "standard_code": "Grade 9: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Two-variable linear relations, using graphing, interpolation, and extrapolation",
        "meta_desc": "Free Grade 9 math worksheets on linear relations for the BC curriculum: tables of values to graphs, reading graphs, interpolation between points, extrapolation beyond the data, and equations for taxi fares and cooling soup. 100 questions with an answer key.",
        "key_big": "Interpolate to find a value between data points. Extrapolate to predict a value beyond them. Both follow the same straight line.",
        "key_sub": "A tank has 30 L at 0 hours and 50 L at 2 hours, so it gains 10 L each hour: W = 10t + 30. At 3 hours it holds 60 L (interpolation). It reaches 100 L at 7 hours (extrapolation).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(graph|four graphs|table of values)")


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
