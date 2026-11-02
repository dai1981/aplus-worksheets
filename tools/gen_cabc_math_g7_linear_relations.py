# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Linear relations (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g7_linear_relations.py
Discrete linear relations, using expressions, tables, and graphs: tables of values from patterns,
writing an expression such as 3n + 2, evaluating expressions (whole numbers, decimals, integers),
plotting and reading points of a linear relation, matching table, expression and graph, and
word problems (taxi fares, saving for a bike, rentals, rain barrels).
Wrong answers come from real mistakes: a rule from the first step only, mixing up n and the value,
plotting (y, x), using the first value as the constant, "add 3" written as n + 3, ignoring skipped
n values, 3n read as 30-something, doing the operations in the wrong order, and off-by-one jumps.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d6cd"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NB = "\u00a0"


# ------------------------------------------------------------ numbers
def n(v):
    """BC/SI style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1 and v >= 0, v
    w, r = divmod(c.numerator, 100)
    return "$%s.%02d" % (n(w), r)


def dol(v):
    """Whole dollars: $18."""
    v = Fr(v)
    assert v.denominator == 1 and v >= 0
    return "$" + n(v)


def plain(s):
    return re.sub(r"<[^>]+>", "", s).replace(NB, " ")


def lst(xs):
    return ", ".join(n(x) for x in xs)


def pt(a, b):
    return "(%s, %s)" % (n(a), n(b))


# ------------------------------------------------------------ expressions
def X(s):
    """Plain expression '3n + 2' -> HTML with the letter in italics and the real minus sign."""
    s = s.replace("-", MINUS)
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<i>\1</i>", s)


def ev(s, v):
    """Exact value of a one-letter expression s when the letter is v."""
    t = s.replace(MINUS, "-").replace("×", "*").replace("÷", "/")
    t = re.sub(r"(\d|\))\s*([a-z(])", r"\1*\2", t)
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Fr('%s')" % m.group(), t)
    env = {"Fr": Fr}
    for L in set(re.findall(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", s)):
        env[L] = Fr(v)
    return eval(t, {"__builtins__": {}}, env)


def lin(a, b, var="n"):
    """Plain text of a·var + b: 3n + 2, 4n − 1, n + 5, 0.5n + 1."""
    a, b = Fr(a), Fr(b)
    s = ("" if a == 1 else n(a)) + var
    if b > 0:
        s += " + " + n(b)
    elif b < 0:
        s += " − " + n(-b)
    return s


def SX(s):
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<tspan font-style='italic'>\1</tspan>", s.replace("-", MINUS))


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


def emcq(q, right, wrong, e, ns, vals):
    """Expression choices. right fits every (n, value); each wrong misses at least one; no two wrongs equal."""
    for k, v in zip(ns, vals):
        assert ev(right, k) == Fr(v), (right, k, v)
    sig = lambda s: tuple(ev(s, k) for k in range(-3, 8))
    sigs = {sig(right)}
    for w in wrong:
        assert any(ev(w, k) != Fr(v) for k, v in zip(ns, vals)), (w, ns, vals)
        assert sig(w) not in sigs, w
        sigs.add(sig(w))
    return mcq(q, X(right), [X(w) for w in wrong], e)


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


def tbl(top, bot, heads=("n", "Value"), label="table of values"):
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


def L_shape(k):
    def draw(x, y):
        s = [tile(x, y + i * T) for i in range(k)]
        s += [tile(x + i * T, y + (k - 1) * T) for i in range(1, k)]
        return "".join(s)
    return k * T, k * T, draw


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


def tables(k):
    S, r = 30, 7

    def draw(x, y):
        s = []
        x0, y0 = x + 2 * r + 4, y + 2 * r + 4
        for i in range(k):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x0 + i * S, y0, S, S, "#f3e3c3", STICK))
            for cy in (y0 - r - 3, y0 + S + r + 3):
                s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x0 + i * S + S / 2, cy, r, FILL, GREEN))
        for cx in (x0 - r - 3, x0 + k * S + r + 3):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, y0 + S / 2, r, FILL, GREEN))
        return "".join(s)
    return k * S + 2 * (2 * r + 4), S + 2 * (2 * r + 4), draw


PATTERNS = {
    "L": (L_shape, lambda k: 2 * k - 1, "tiles"),
    "sq": (squares, lambda k: 3 * k + 1, "sticks"),
    "towers": (towers3, lambda k: 3 * k + 3, "cubes"),
    "tables": (tables, lambda k: 2 * k + 2, "chairs"),
}


def cnt(nm, k):
    return PATTERNS[nm][1](k)


def thing(nm):
    return PATTERNS[nm][2]


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
def graph_svg(pts, xmax, ymax, ystep=1, ylab=2, xname="x", yname="y", tags=None, vals=False,
              ypre="", label="graph of a linear relation"):
    """First-quadrant graph of discrete points, drawn exactly to the grid.
    tags: {(x, y): 'P'} letters next to points. vals: show each y value above its point."""
    tags = tags or {}
    XU = 32 if xmax <= 7 else 26
    PH = 210.0
    YU = PH / ymax
    ylabels = [(gy, ypre + n(gy)) for gy in range(0, ymax + 1, ylab)]
    LW = max(tw(t, 14) for _, t in ylabels)
    yn_long = len(yname) > 1
    L = (34 if yn_long else 24) + LW + 8
    T, R, B = 24, 18, 50
    X0, Y0 = L, T + PH
    W = L + xmax * XU + R
    H = T + PH + B
    s = []
    for gy in range(0, ymax + 1, ystep):
        y = Y0 - gy * YU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + xmax * XU, y, GRID))
    for gy, t in ylabels:
        s.append(text(X0 - 7, Y0 - gy * YU + 5, t, 14, "end", bold=False))
    for gx in range(0, xmax + 1):
        x = X0 + gx * XU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, T, x, Y0, GRID))
        s.append(text(x, Y0 + 19, n(gx), 14, bold=False))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + xmax * XU, Y0, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, T, X0, Y0, INK))
    xn = SX(xname) if len(xname) == 1 else xname
    yn = SX(yname) if len(yname) == 1 else yname
    s.append(text(X0 + xmax * XU / 2, H - 8, xn, 15 if len(xname) > 1 else 17))
    if yn_long:
        cy = T + PH / 2
        s.append(text(16, cy, yn, 15, extra=" transform='rotate(-90 16 %.1f)'" % cy))
    else:
        s.append(text(X0 - LW - 16, T + PH / 2 + 6, yn, 17))
    for px, py in pts:
        assert 0 <= px <= xmax and 0 <= py <= ymax
        cx, cy = X0 + px * XU, Y0 - Fr(py) * Fr(YU)
        cx, cy = float(cx), float(cy)
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
        if vals:
            t = ypre + n(py)
            w = tw(t, 14) + 6
            assert cy - 24 >= 0
            lx = cx + w / 2 + 4 if px == 0 else cx
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='17' fill='#ffffff' opacity='0.85'/>" % (lx - w / 2, cy - 24, w))
            s.append(text(lx, cy - 10, t, 14))
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
            s.append("<circle cx='%d' cy='%d' r='4.5' fill='%s'/>" % (X0 + px * U, Y0 - py * U, RED))
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: tables of values from patterns
def set_tables():
    its = []
    HEAD = lambda nm: ("Figure number", "Number of " + thing(nm))

    # 1 next figure
    v = [cnt("sq", k) for k in range(1, 5)]
    its.append(nmcq(fig(pattern_svg("sq")) + "The pattern continues. How many sticks are in Figure 4?", v[3], [16, 14, 11],
                    "Count: 4, 7, 10. Each figure adds 3 sticks, so Figure 4 has 10 + 3 = <b>13</b>. "
                    "16 counts 4 sticks for every square, but squares next to each other share a stick."))
    v = [cnt("L", k) for k in range(1, 6)]
    its.append(nmcq(fig(pattern_svg("L")) + "The pattern continues. How many tiles are in Figure 4?", v[3], [16, 6, 9],
                    "Count: 1, 3, 5. Each figure adds 2 tiles, so Figure 4 has 5 + 2 = <b>7</b>. "
                    "6 adds 1 because the figure number goes up by 1. 9 is Figure 5."))
    # 3 missing value
    its.append(nmcq(tbl([1, 2, 3, 4, 5], [5, 9, 13, "?", 21]) + "What value is missing from the table?", 17, [4, 14, 25],
                    "The value goes up by 4 each time: 13 + 4 = <b>17</b>. Check: 17 + 4 = 21. "
                    "4 is the value of <i>n</i>, not the value in the table."))
    its.append(nmcq(tbl([1, 2, 3, 4], [6, 10, 14, 18]) + "The pattern continues. What is the value when <i>n</i> = 5?",
                    22, [19, 23, 5],
                    "The value goes up by 4 each time: 18 + 4 = <b>22</b>. "
                    "19 adds 1 (like <i>n</i>) instead of 4. 23 adds 5 because <i>n</i> is 5."))
    its.append(nmcq(tbl([1, 2, 3, 4], [30, 26, 22, 18]) + "The pattern continues. What is the value when <i>n</i> = 6?",
                    10, [14, 26, 12],
                    "The value goes down by 4 each time: 18, 14, <b>10</b>. 14 is the value for <i>n</i> = 5. "
                    "12 subtracts 6 because <i>n</i> is 6. 26 goes the wrong way."))
    its.append(nmcq(tbl([1, 2, 3, 4], [3, 8, 13, 18]) + "The pattern continues. What is the value when <i>n</i> = 6?",
                    28, [23, 26, 30],
                    "Add 5 each time: 18, 23, <b>28</b>. 26 doubles the value for <i>n</i> = 3, but this pattern does not "
                    "start at 0, so doubling does not work. 30 is 6 × 5 and forgets that 3 is 2 less than 5."))
    # 7 value at n = 0
    its.append(nmcq(tbl([1, 2, 3, 4], [7, 11, 15, 19]) + "The pattern works backward too. What is the value when <i>n</i> = 0?",
                    3, [7, 4, 11],
                    "The value goes up by 4, so going back one step subtracts 4: 7 − 4 = <b>3</b>. "
                    "4 is the jump, not the value. 7 is the value for <i>n</i> = 1."))
    # 8 which is linear
    its.append(mcq("For <i>n</i> = 1, 2, 3, 4, which list of values makes a linear relation?", "3, 7, 11, 15",
                   ["2, 5, 10, 17", "1, 2, 4, 8", "4, 6, 9, 13"],
                   "In a linear relation the value changes by the same amount every time. 3, 7, 11, 15 goes up by 4 each time, "
                   "so it is <b>linear</b>. 2, 5, 10, 17 goes up by 3, then 5, then 7: the first step alone is not enough."))
    # 9 first step only (not linear)
    its.append(nmcq(tbl([1, 2, 3, 4], [4, 7, 11, 16]) + "Kai says the next value is 19 because the first step is +3. "
                    "The jumps keep growing the same way. What is the next value?", 22, [19, 21, 20],
                    "Check every step, not only the first: +3, +4, +5. The next jump is +6, so 16 + 6 = <b>22</b>. "
                    "This pattern is not linear because the jumps change. 19 uses the first step only."))
    # 10 skipped n
    its.append(nmcq(tbl([1, 3, 5, 7], [5, 11, 17, 23]) + "How much does the value go up each time <i>n</i> goes up by 1?",
                    3, [6, 2, 5],
                    "Look at the top row: <i>n</i> goes up by 2 each time, and the value goes up by 6. "
                    "So for each 1, the value goes up by 6 ÷ 2 = <b>3</b>. 6 forgets that <i>n</i> skips numbers."))
    its.append(nmcq(tbl([2, 4, 6, 8], [9, 17, 25, 33]) + "What is the value when <i>n</i> = 5?", 21, [25, 13, 37],
                    "<i>n</i> goes up by 2 and the value goes up by 8, so each 1 adds 4. "
                    "<i>n</i> = 4 has 17, so <i>n</i> = 5 has 17 + 4 = <b>21</b>. 25 is the value for <i>n</i> = 6, and 13 is for <i>n</i> = 3."))
    # 12 find the error
    bad = [8, 13, 18, 24, 28]
    assert [8 + 5 * k for k in range(5)][3] == 23
    its.append(nmcq(tbl([1, 2, 3, 4, 5], bad) + "One value in this table is wrong. Which one?", 24, [13, 18, 28],
                    "The value goes up by 5: 8, 13, 18, 23, 28. <b>24</b> should be 23."))
    # 13 hidden figure
    v = [cnt("towers", k) for k in (1, 2, 3)]
    its.append(nmcq(fig(pattern_svg("towers", hide=2)) + "Figure 2 is hidden. How many cubes are in Figure 2?", v[1],
                    [8, 18, 10],
                    "Figure 1 has 6 cubes and Figure 3 has 12. The pattern grows by the same amount each time: "
                    "6, <b>9</b>, 12. 18 adds the two figures together."))
    # 14 which figure (n vs value)
    vals = [cnt("tables", k) for k in range(1, 12)]
    k = vals.index(22) + 1
    its.append(mcq(fig(pattern_svg("tables")) + "The pattern continues. Which figure has 22 chairs?", "Figure %d" % k,
                   ["Figure 22", "Figure %d" % (k + 1), "Figure %d" % (k - 1)],
                   "Add 2 chairs each time: %s. <b>Figure %d</b> has 22 chairs. "
                   "22 is the number of chairs, not the figure number." % (lst(vals[:k]), k)))
    # 15 figure 10
    v = [cnt("sq", k) for k in range(1, 11)]
    its.append(nmcq(fig(pattern_svg("sq")) + "The pattern continues. How many sticks are in Figure 10?", v[9],
                    [34, 40, 30],
                    "Start at 4 and add 3 each time. From Figure 1 to Figure 10 there are 9 jumps: 9 × 3 = 27. "
                    "4 + 27 = <b>31</b>. 34 makes 10 jumps. 40 is 10 × 4."))
    # 16 meaning of a column
    tv = [cnt("towers", k) for k in range(1, 6)]
    its.append(mcq(tbl([1, 2, 3, 4, 5], tv, HEAD("towers")) + "In this table, 15 is under 4. What does that mean?",
                   "Figure 4 has 15 cubes", ["Figure 15 has 4 cubes", "Each figure adds 15 cubes", "Each figure adds 4 cubes"],
                   "Read down the column. The figure number is on top and the number of cubes is below it. "
                   "So <b>Figure 4 has 15 cubes</b>."))
    # 17 table from a description
    its.append(mcq("Figure 1 of a pattern has 9 tiles. Each new figure has 4 more tiles. "
                   "Which list shows the number of tiles in Figures 1 to 4?", "9, 13, 17, 21",
                   ["13, 17, 21, 25", "4, 13, 22, 31", "4, 8, 12, 16"],
                   "Figure 1 has 9. Then add 4 each time: 9, 13, 17, 21. The answer is <b>9, 13, 17, 21</b>. "
                   "13, 17, … starts one jump too late. 4, 13, … mixes up the start and the jump."))
    # 18 decreasing: which n
    v = [50 - 4 * (k - 1) for k in range(1, 12)]
    k = v.index(22) + 1
    its.append(nmcq(tbl([1, 2, 3, 4], v[:4]) + "The pattern continues. For which value of <i>n</i> is the value 22?",
                    k, [22, 7, 9],
                    "Subtract 4 each time: %s. The value 22 is at <i>n</i> = <b>%d</b>. "
                    "22 is the value, not <i>n</i>." % (lst(v[:k]), k)))
    # 19 decimals
    v = [Fr(5, 2) + Fr(3, 2) * (k - 1) for k in range(1, 7)]
    its.append(nmcq(tbl([1, 2, 3, 4], v[:4]) + "The pattern continues. What is the value when <i>n</i> = 6?",
                    v[5], [Fr(17, 2), 11, 15],
                    "The value goes up by 1.5 each time: 7, 8.5, <b>10</b>. 8.5 is the value for <i>n</i> = 5. "
                    "11 doubles the value for <i>n</i> = 3, which only works when the pattern starts at 0."))
    # 20 integers
    v = [-5 + 3 * (k - 1) for k in range(1, 9)]
    assert v[6] == 13
    its.append(nmcq(tbl([1, 2, 3, 4], v[:4]) + "The pattern continues. What is the value when <i>n</i> = 7?",
                    v[6], [10, 16, -23],
                    "The value goes up by 3 each time: −5, −2, 1, 4, 7, 10, <b>13</b>. "
                    "10 is the value for <i>n</i> = 6 and 16 is for <i>n</i> = 8. "
                    "From −5 to −2 is +3, not −3, so the values go up."))
    order = [0, 1, 2, 3, 4, 12, 15, 6, 13, 7, 5, 16, 8, 14, 9, 17, 10, 18, 19, 11]
    assert sorted(order) == list(range(20))
    return {"title": "Tables of values from patterns", "items": [its[i] for i in order]}


# ============================================================ set 2: write an expression
def set_expressions():
    its = []
    N4 = [1, 2, 3, 4]

    def from_table(vals, right, wrong, e, ns=N4):
        return emcq(tbl(ns, vals) + "Which expression gives the value for any <i>n</i>?", right, wrong, e, ns, vals)

    its.append(from_table([3, 6, 9, 12], "3n", ["n + 3", "3n + 3", "n + 12"],
                          "Each value is 3 times <i>n</i>: 3 × 1 = 3, 3 × 2 = 6. The expression is <b>%s</b>. "
                          "%s gives 4, 5, 6, 7." % (X("3n"), X("n + 3"))))
    its.append(from_table([5, 8, 11, 14], "3n + 2", ["n + 3", "3n + 5", "5n + 3"],
                          "The value goes up by 3, so start with %s. When <i>n</i> = 1, 3 × 1 = 3, but the value is 5, "
                          "so add 2: <b>%s</b>. %s uses the first value as the number added." % (X("3n"), X("3n + 2"), X("3n + 5"))))
    its.append(from_table([6, 10, 14, 18], "4n + 2", ["n + 4", "4n + 6", "6n + 4"],
                          "The value goes up by 4, so start with %s. 4 × 1 = 4 and the value is 6, so add 2: <b>%s</b>. "
                          "Check: 4 × 3 + 2 = 14." % (X("4n"), X("4n + 2"))))
    its.append(from_table([3, 8, 13, 18], "5n - 2", ["n + 5", "5n + 3", "3n + 5"],
                          "The value goes up by 5, so start with %s. 5 × 1 = 5 but the value is 3, so subtract 2: <b>%s</b>. "
                          "Check: 5 × 4 − 2 = 18." % (X("5n"), X("5n − 2"))))
    its.append(from_table([9, 11, 13, 15], "2n + 7", ["n + 2", "2n + 9", "9n + 2"],
                          "The value goes up by 2, so start with %s. 2 × 1 = 2 and the value is 9, so add 7: <b>%s</b>. "
                          "%s writes “add 2 each time” but uses <i>n</i> only once." % (X("2n"), X("2n + 7"), X("n + 2"))))
    # shapes
    sq = [cnt("sq", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("sq")) + "Which expression gives the number of sticks in Figure <i>n</i>?",
                    "3n + 1", ["4n", "3n + 4", "n + 3"],
                    "Count: 4, 7, 10. Each figure adds 3 sticks, so start with %s. 3 × 1 = 3 and Figure 1 has 4, so add 1: "
                    "<b>%s</b>. %s counts 4 sticks for every square, but squares share sticks." % (X("3n"), X("3n + 1"), X("4n")),
                    [1, 2, 3], sq))
    tb = [cnt("tables", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("tables")) + "Which expression gives the number of chairs for <i>n</i> tables in a row?",
                    "2n + 2", ["4n", "2n + 4", "n + 2"],
                    "Count: 4, 6, 8. Each table adds 2 chairs, so start with %s. 2 × 1 = 2 and 1 table has 4 chairs, "
                    "so add 2: <b>%s</b>. %s gives 8 chairs for 2 tables, but there are only 6." % (X("2n"), X("2n + 2"), X("4n")),
                    [1, 2, 3], tb))
    L = [cnt("L", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("L")) + "Which expression gives the number of tiles in Figure <i>n</i>?",
                    "2n - 1", ["n + 2", "2n + 1", "3n - 2"],
                    "Count: 1, 3, 5. Each figure adds 2 tiles, so start with %s. 2 × 1 = 2 and Figure 1 has 1, so subtract 1: "
                    "<b>%s</b>. %s works for Figure 1 only: 3 × 2 − 2 = 4, not 3." % (X("2n"), X("2n − 1"), X("3n − 2")),
                    [1, 2, 3], L))
    tw_ = [cnt("towers", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("towers")) + "Which expression gives the number of cubes in Figure <i>n</i>?",
                    "3n + 3", ["n + 3", "3n + 6", "6n"],
                    "Count: 6, 9, 12. Each figure adds 3 cubes, so start with %s. 3 × 1 = 3 and Figure 1 has 6, so add 3: "
                    "<b>%s</b>. %s works for Figure 1 only: 6 × 2 = 12, not 9." % (X("3n"), X("3n + 3"), X("6n")),
                    [1, 2, 3], tw_))
    # n starts at 0
    its.append(from_table([7, 12, 17, 22], "5n + 7", ["5n + 2", "n + 5", "7n + 5"],
                          "The value goes up by 5, so start with %s. This table starts at <i>n</i> = 0, and 5 × 0 = 0, "
                          "so add the value at 0: <b>%s</b>. %s would be right if the table started at <i>n</i> = 1."
                          % (X("5n"), X("5n + 7"), X("5n + 2")), ns=[0, 1, 2, 3]))
    # decreasing
    its.append(from_table([37, 34, 31, 28], "40 - 3n", ["37 - 3n", "n - 3", "3n + 34"],
                          "The value goes down by 3, so the expression subtracts %s. When <i>n</i> = 1, the value is 37, "
                          "and 37 + 3 = 40, so it is <b>%s</b>. Check: 40 − 3 × 4 = 28. %s gives 34 when <i>n</i> = 1."
                          % (X("3n"), X("40 − 3n"), X("37 − 3n"))))
    # skipped n
    its.append(from_table([11, 21, 31, 41], "5n + 1", ["10n + 1", "10n - 9", "n + 10"],
                          "<i>n</i> goes up by 2 and the value goes up by 10, so each 1 adds 5. Start with %s. "
                          "5 × 2 = 10 and the value is 11, so add 1: <b>%s</b>. %s forgets that <i>n</i> skips numbers."
                          % (X("5n"), X("5n + 1"), X("10n + 1")), ns=[2, 4, 6, 8]))
    # from words
    its.append(emcq("Figure 1 of a pattern has 6 dots. Each new figure has 4 more dots. "
                    "Which expression gives the number of dots in Figure <i>n</i>?",
                    "4n + 2", ["4n + 6", "6n + 4", "n + 4"],
                    "Each figure adds 4, so start with %s. 4 × 1 = 4 and Figure 1 has 6, so add 2: <b>%s</b>. "
                    "%s gives 10 dots in Figure 1." % (X("4n"), X("4n + 2"), X("4n + 6")), [1, 2, 3], [6, 10, 14]))
    its.append(emcq("Figure 1 of Ryan’s pattern has 10 dots. Each new figure has 6 more dots. "
                    "Which expression gives the number of dots in Figure <i>n</i>?",
                    "6n + 4", ["6n + 10", "10n + 6", "n + 6"],
                    "Each figure adds 6, so start with %s. 6 × 1 = 6 and Figure 1 has 10, so add 4: <b>%s</b>. "
                    "%s mixes up the start and the jump." % (X("6n"), X("6n + 4"), X("10n + 6")), [1, 2, 3], [10, 16, 22]))
    # meaning of n and of the coefficient
    its.append(mcq(fig(pattern_svg("sq")) + "The number of sticks is %s. What does <i>n</i> stand for?" % X("3n + 1"),
                   "the figure number", ["the number of sticks", "the sticks added each time", "the sticks in Figure 1"],
                   "<i>n</i> is the input: <b>the figure number</b>. The whole expression %s is the number of sticks."
                   % X("3n + 1")))
    its.append(mcq(fig(pattern_svg("sq")) + "The number of sticks is %s. What does the 3 tell you?" % X("3n + 1"),
                   "Each figure adds 3 sticks", ["Figure 1 has 3 sticks", "There are 3 figures", "Figure 3 has 1 stick"],
                   "The number multiplied by <i>n</i> is the change from one figure to the next. "
                   "<b>Each figure adds 3 sticks</b>. Figure 1 has 3 × 1 + 1 = 4 sticks."))
    # two facts
    its.append(emcq("An expression gives 17 when <i>n</i> = 5 and 11 when <i>n</i> = 3. Which expression is it?",
                    "3n + 2", ["n + 12", "2n + 7", "4n - 3"],
                    "Test both pairs. 3 × 5 + 2 = 17 and 3 × 3 + 2 = 11, so <b>%s</b> works. "
                    "%s and %s give 17 for <i>n</i> = 5 but not 11 for <i>n</i> = 3: always check more than one pair."
                    % (X("3n + 2"), X("2n + 7"), X("4n − 3")), [5, 3], [17, 11]))
    # decimals
    its.append(from_table([Fr(3, 2), 2, Fr(5, 2), 3], "0.5n + 1", ["n + 0.5", "0.5n + 1.5", "1.5n"],
                          "The value goes up by 0.5, so start with %s. 0.5 × 1 = 0.5 and the value is 1.5, so add 1: "
                          "<b>%s</b>. %s goes up by 1 each time, not 0.5." % (X("0.5n"), X("0.5n + 1"), X("n + 0.5"))))
    # integers
    its.append(from_table([-1, 1, 3, 5], "2n - 3", ["n + 2", "2n - 1", "2n + 3"],
                          "The value goes up by 2, so start with %s. 2 × 1 = 2 and the value is −1. 2 − 3 = −1, so "
                          "<b>%s</b>. %s gives 1 when <i>n</i> = 1." % (X("2n"), X("2n − 3"), X("2n − 1"))))
    # first step only
    its.append(emcq(tbl(N4, [4, 9, 14, 19]) + "Jasleen says the expression is %s because 1 + 3 = 4. "
                    "Which expression is right for the whole table?" % X("n + 3"),
                    "5n - 1", ["n + 3", "4n", "5n + 4"],
                    "%s works for the first column only: 2 + 3 = 5, not 9. The value goes up by 5, so start with %s. "
                    "5 × 1 = 5 and the value is 4, so subtract 1: <b>%s</b>." % (X("n + 3"), X("5n"), X("5n − 1")),
                    N4, [4, 9, 14, 19]))
    order = [0, 1, 2, 5, 6, 14, 15, 4, 3, 8, 12, 7, 13, 9, 19, 17, 18, 10, 11, 16]
    assert sorted(order) == list(range(20))
    return {"title": "Write an expression for a pattern", "items": [its[i] for i in order]}


# ============================================================ set 3: evaluate expressions
def set_evaluate():
    its = []

    def evq(expr, v, cands, why):
        a = ev(expr, v)
        q = "What is the value of <b>%s</b> when <i>n</i> = %s?" % (X(expr), n(v))
        return nmcq(q, a, cands, why % {"a": n(a)})

    its.append(evq("3n + 2", 7, [39, 27, 12],
                   "Replace <i>n</i> with 7: 3 × 7 + 2 = 21 + 2 = <b>%(a)s</b>. "
                   "3<i>n</i> means 3 × <i>n</i>, not 37. Multiply before you add: 27 adds first, 3 × (7 + 2)."))
    its.append(evq("5n - 4", 6, [10, 52, 7],
                   "5 × 6 − 4 = 30 − 4 = <b>%(a)s</b>. 10 subtracts first: 5 × (6 − 4). 52 reads 5<i>n</i> as 56. 7 adds instead of multiplying: 5 + 6 − 4."))
    its.append(evq("2n + 9", 0, [11, 29, 2],
                   "2 × 0 + 9 = 0 + 9 = <b>%(a)s</b>. Any number times 0 is 0. 11 treats 2<i>n</i> as 2. 29 reads 2<i>n</i> as 20."))
    its.append(evq("4n + 3", 10, [52, 17, 40],
                   "4 × 10 + 3 = 40 + 3 = <b>%(a)s</b>. 52 adds first: 4 × (10 + 3). 40 forgets the + 3."))
    its.append(evq("6 + 2n", 4, [32, 12, 10],
                   "Multiply first: 2 × 4 = 8. Then 6 + 8 = <b>%(a)s</b>. 32 adds first: (6 + 2) × 4."))
    its.append(evq("3n - 8", 2, [2, 14, -14],
                   "3 × 2 − 8 = 6 − 8 = <b>%(a)s</b>. 8 is bigger than 6, so the answer is negative. "
                   "14 adds 8 instead of subtracting."))
    its.append(evq("10 - 3n", 5, [5, 35, 25],
                   "Multiply first: 3 × 5 = 15. Then 10 − 15 = <b>%(a)s</b>. 35 subtracts first: (10 − 3) × 5."))
    its.append(evq("4n + 3", Fr(5, 2), [Fr(23, 2), Fr(19, 2), 22],
                   "4 × 2.5 = 10. Then 10 + 3 = <b>%(a)s</b>. 11.5 multiplies only the 2: 4 × 2 + 0.5 + 3. "
                   "9.5 adds everything: 4 + 2.5 + 3."))
    its.append(evq("1.5n + 2", 6, [12, Fr(19, 2), 8],
                   "1.5 × 6 = 9. Then 9 + 2 = <b>%(a)s</b>. 12 adds first: 1.5 × (6 + 2). 8 forgets the 1.5."))
    its.append(evq("n ÷ 2 + 6", 10, [Fr(5, 4), 26, 16],
                   "Divide first: 10 ÷ 2 = 5. Then 5 + 6 = <b>%(a)s</b>. 1.25 adds first: 10 ÷ 8. 26 multiplies instead of dividing."))
    # table with skipped n
    a = ev("2n + 5", 5)
    its.append(nmcq(tbl([1, 2, 5, 8], [7, 9, "?", 21]) + "The table follows the rule %s. What is the missing value?" % X("2n + 5"),
                    a, [11, 20, 13],
                    "Use the rule on the <i>n</i> above the ?: 2 × 5 + 5 = <b>15</b>. "
                    "11 just adds 2 to 9, but <i>n</i> jumps from 2 to 5. 20 is 2 × (5 + 5). 13 is the value for <i>n</i> = 4."))
    # which table
    vals = [ev("4n - 3", k) for k in (1, 2, 3, 4)]
    its.append(mcq("Which list gives the values of %s for <i>n</i> = 1, 2, 3, 4?" % X("4n − 3"), lst(vals),
                   ["4, 8, 12, 16", "7, 11, 15, 19", lst([ev("4n - 3", k) for k in (0, 1, 2, 3)])],
                   "4 × 1 − 3 = 1, 4 × 2 − 3 = 5, 4 × 3 − 3 = 9, 4 × 4 − 3 = 13: <b>%s</b>. "
                   "4, 8, 12, 16 forgets the − 3. 7, 11, … adds 3 instead." % lst(vals)))
    vals = [ev("3n + 4", k) for k in (1, 2, 3, 4)]
    its.append(mcq("Which list gives the values of %s for <i>n</i> = 1, 2, 3, 4?" % X("3n + 4"), lst(vals),
                   [lst([ev("3n + 4", k) for k in (0, 1, 2, 3)]), "3, 7, 11, 15", "7, 11, 15, 19"],
                   "3 × 1 + 4 = 7, then add 3 each time: <b>%s</b>. 4, 7, 10, 13 starts at <i>n</i> = 0. "
                   "3, 7, 11, 15 mixes up the 3 and the 4." % lst(vals)))
    # solve
    assert ev("4n + 1", 9) == 37
    its.append(nmcq("For which value of <i>n</i> is %s equal to 37?" % X("4n + 1"), 9, [37, Fr(19, 2), Fr(33, 4)],
                    "Work backward. Undo + 1: 37 − 1 = 36. Undo × 4: 36 ÷ 4 = <b>9</b>. Check: 4 × 9 + 1 = 37. "
                    "37 is the value, not <i>n</i>. 9.5 adds 1 instead of subtracting."))
    assert ev("2n - 6", 18) == 30
    its.append(nmcq("For which value of <i>n</i> is %s equal to 30?" % X("2n − 6"), 18, [12, 30, 21],
                    "Work backward. Undo − 6: 30 + 6 = 36. Undo × 2: 36 ÷ 2 = <b>18</b>. Check: 2 × 18 − 6 = 30. "
                    "12 subtracts 6 instead of adding. 21 undoes in the wrong order: 30 ÷ 2 + 6."))
    its.append(nmcq("When <i>n</i> goes up by 1, how much does the value of %s go up?" % X("6n + 5"), 6, [5, 11, 1],
                    "Each extra 1 for <i>n</i> adds one more 6: 6 × 1 + 5 = 11, 6 × 2 + 5 = 17. "
                    "The value goes up by <b>6</b>. The + 5 stays the same."))
    its.append(mcq("Arjun finds %s when <i>n</i> = 4. He writes 34 + 2 = 36. What mistake did he make?" % X("3n + 2"),
                   "He wrote 3<i>n</i> as 34, not 3 × 4", ["He should add before he multiplies", "He should use <i>n</i> = 2",
                                                         "He made no mistake"],
                   "3<i>n</i> means 3 × <i>n</i>. 3 × 4 = 12, and 12 + 2 = 14. <b>He wrote 3<i>n</i> as 34.</b>"))
    its.append(evq("15 - 2n", 9, [3, 33, 117],
                   "Multiply first: 2 × 9 = 18. Then 15 − 18 = <b>%(a)s</b>. 3 forgets that the answer is negative. "
                   "117 subtracts first: (15 − 2) × 9."))
    its.append(evq("0.25n + 3", 12, [Fr(33, 10), Fr(61, 4), 39],
                   "0.25 × 12 = 3 (a quarter of 12). Then 3 + 3 = <b>%(a)s</b>. 3.3 puts the decimal point in the wrong place: "
                   "0.25 × 12 is 3, not 0.3. 15.25 adds everything."))
    assert ev("4n + 1", 4) == ev("2n + 9", 4) == 17
    assert all(ev("4n + 1", k) != ev("2n + 9", k) for k in range(0, 20) if k != 4)
    its.append(nmcq("For which value of <i>n</i> do %s and %s have the same value?" % (X("4n + 1"), X("2n + 9")),
                    4, [8, 2, 17],
                    "Try values. <i>n</i> = 3: 13 and 15. <i>n</i> = 4: 4 × 4 + 1 = 17 and 2 × 4 + 9 = 17. "
                    "They match at <i>n</i> = <b>4</b>. 17 is the value, not <i>n</i>. 8 is 9 − 1 and 2 is 4 − 2: compare the values, not the numbers in the expressions."))
    order = [0, 1, 2, 3, 4, 10, 15, 11, 12, 16, 5, 6, 7, 8, 9, 17, 18, 13, 14, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Evaluate expressions and complete tables", "items": [its[i] for i in order]}


# ============================================================ set 4: graphs
def set_graphs():
    its = []
    g1pts = [(x, 2 * x + 1) for x in range(1, 6)]
    g1 = graph_svg(g1pts, 6, 12, tags={(3, 7): "P"}, label="graph of a linear relation: points (1, 3) to (5, 11)")
    its.append(mcq(fig(g1) + "What are the coordinates of point P?", pt(3, 7), [pt(7, 3), pt(3, 6), pt(4, 7)],
                   "Go across first, then up. P is 3 across and 7 up, so it is <b>(3, 7)</b>. "
                   "(7, 3) gives the numbers in the wrong order: <i>x</i> comes first."))
    g1b = graph_svg(g1pts, 6, 12, label="graph of a linear relation: 5 points")
    its.append(nmcq(fig(g1b) + "What is the value of <i>y</i> when <i>x</i> = 4?", 9, [4, 8, 11],
                    "Find 4 on the <i>x</i>-axis and go up to the point. Read across: <i>y</i> = <b>9</b>. "
                    "4 is the value of <i>x</i>. 11 is the point for <i>x</i> = 5."))
    its.append(emcq(fig(g1b) + "Which expression gives <i>y</i> for any <i>x</i>?", "2x + 1", ["x + 2", "3x", "2x + 3"],
                    "The points are (1, 3), (2, 5), (3, 7). <i>y</i> goes up by 2, so start with %s. "
                    "2 × 1 = 2 and <i>y</i> is 3, so add 1: <b>%s</b>. %s works for (1, 3) only." % (X("2x"), X("2x + 1"), X("3x")),
                    [1, 2, 3, 4, 5], [3, 5, 7, 9, 11]))
    its.append(mcq(fig(g1b) + "The pattern continues. Which point comes next?", pt(6, 13), [pt(13, 6), pt(6, 12), pt(7, 13)],
                   "The next <i>x</i> is 6. <i>y</i> goes up by 2, so 11 + 2 = 13. The point is <b>(6, 13)</b>. "
                   "(13, 6) swaps the numbers: <i>x</i> comes first."))
    # plotting a table
    its.append(mcq(tbl([1, 2, 3, 4], [4, 7, 10, 13], ("x", "y")) + "Liam plots this table on a graph. Which point should he plot?",
                   pt(3, 10), [pt(10, 3), pt(3, 13), pt(4, 10)],
                   "Each column is one point (<i>x</i>, <i>y</i>). The column with 3 on top has 10 below, so plot <b>(3, 10)</b>. "
                   "(10, 3) plots (<i>y</i>, <i>x</i>)."))
    its.append(mcq("To plot the point (2, 7), start at (0, 0). How do you move?", "2 right, then 7 up",
                   ["7 right, then 2 up", "2 right, then 5 up", "1 right, then 7 up"],
                   "The first number tells how far across and the second tells how far up: <b>2 right, then 7 up</b>. "
                   "7 right, then 2 up plots (7, 2)."))
    # A-D graphs
    panels = [[(3, 1), (5, 2), (7, 3)], [(1, 3), (2, 5), (3, 7)], [(1, 3), (2, 4), (3, 5)], [(1, 2), (2, 4), (3, 6)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "A table of values has <i>x</i> = 1, 2, 3 and <i>y</i> = 3, 5, 7. Which graph shows these points?", ["Graph A", "Graph B", "Graph C", "Graph D"], 1,
                         "The points are (1, 3), (2, 5), (3, 7). <b>Graph B</b> shows them. Graph A plots (<i>y</i>, <i>x</i>). "
                         "Graph C adds 1 each time and Graph D is 2<i>x</i> without the + 1."))
    want = [(x, x + 4) for x in (1, 2, 3)]
    panels = [[(5, 1), (6, 2), (7, 3)], [(1, 4), (2, 5), (3, 6)], [(1, 7), (2, 6), (3, 5)], want]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for <i>x</i> = 1, 2, 3?" % X("y = x + 4"), ["Graph A", "Graph B", "Graph C", "Graph D"], 3,
                         "1 + 4 = 5, 2 + 4 = 6, 3 + 4 = 7. The points are (1, 5), (2, 6), (3, 7): <b>Graph D</b>. "
                         "Graph A plots (<i>y</i>, <i>x</i>). Graph B adds 3. Graph C goes down, but <i>x</i> + 4 goes up."))
    want = [(x, 8 - 2 * x) for x in (1, 2, 3)]
    panels = [[(1, 2), (2, 4), (3, 6)], [(6, 1), (4, 2), (2, 3)], want, [(1, 6), (2, 5), (3, 4)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for <i>x</i> = 1, 2, 3?" % X("y = 8 − 2x"), ["Graph A", "Graph B", "Graph C", "Graph D"], 2,
                         "8 − 2 = 6, 8 − 4 = 4, 8 − 6 = 2. The points are (1, 6), (2, 4), (3, 2): <b>Graph C</b>. "
                         "Graph B plots (<i>y</i>, <i>x</i>). Graph D goes down by 1, not 2."))
    # decreasing graph
    g2 = graph_svg([(x, 12 - 2 * x) for x in range(0, 6)], 6, 12, label="graph of a decreasing linear relation")
    its.append(mcq(fig(g2) + "How does <i>y</i> change each time <i>x</i> goes up by 1?", "<i>y</i> goes down by 2",
                   ["<i>y</i> goes up by 2", "<i>y</i> goes down by 1", "<i>y</i> goes down by 12"],
                   "The points are (0, 12), (1, 10), (2, 8). Each step right, <i>y</i> drops 2: <b><i>y</i> goes down by 2</b>."))
    its.append(emcq(fig(g2) + "Which expression gives <i>y</i> for any <i>x</i>?", "12 - 2x", ["2x + 12", "12 - x", "10 - 2x"],
                    "When <i>x</i> = 0, <i>y</i> = 12, and <i>y</i> goes down by 2 each time: <b>%s</b>. "
                    "%s uses the point for <i>x</i> = 1 as the start." % (X("12 − 2x"), X("10 − 2x")),
                    [0, 1, 2, 3, 4, 5], [12, 10, 8, 6, 4, 2]))
    # discrete
    sv = [cnt("sq", k) for k in range(1, 5)]
    g3 = graph_svg(list(zip([1, 2, 3, 4], sv)), 6, 16, ylab=4, xname="Figure number", yname="Number of sticks",
                   label="graph of figure number and number of sticks")
    its.append(mcq(fig(g3) + "Why are the points on this graph not joined with a line?",
                   "There is no Figure 1.5, only whole figures",
                   ["The points are not in a straight line", "A line would go off the graph", "Graphs never join points"],
                   "The relation is <b>discrete</b>: you can have Figure 1 or Figure 2 but no Figure 1.5. "
                   "The points do line up, but only whole figure numbers make sense."))
    v = [cnt("sq", k) for k in range(1, 11)]
    its.append(nmcq(fig(g3) + "The pattern continues. How many sticks are in Figure 7?", v[6], [19, 28, 25],
                    "The points go up by 3 sticks each figure: 4, 7, 10, 13, 16, 19, <b>22</b>. "
                    "19 is Figure 6. 28 is 7 × 4."))
    its.append(mcq(fig(g3) + "The pattern continues. Which point would be on this graph?", pt(10, 31),
                   [pt(31, 10), pt(10, 30), pt(10, 40)],
                   "The number of sticks is %s. For Figure 10: 3 × 10 + 1 = 31, so the point is <b>(10, 31)</b>. "
                   "The figure number comes first." % X("3n + 1")))
    good = [(1, 2), (2, 5), (5, 14)]
    assert all(ev("3x - 1", a) == b for a, b in good) and ev("3x - 1", 4) != 12
    its.append(mcq("Which point is <b>not</b> on the graph of %s?" % X("y = 3x − 1"), pt(4, 12), [pt(a, b) for a, b in good],
                   "Test each point. For <i>x</i> = 4: 3 × 4 − 1 = 11, not 12, so <b>(4, 12)</b> is not on the graph. "
                   "(1, 2), (2, 5) and (5, 14) all work."))
    g4 = graph_svg([(x, 5 * x + 10) for x in range(0, 5)], 5, 35, ystep=5, ylab=5,
                   label="graph of a linear relation going up by 5")
    its.append(nmcq(fig(g4) + "What is the value of <i>y</i> when <i>x</i> = 0?", 10, [0, 5, 15],
                    "The first point is on the <i>y</i>-axis at 10, so <i>y</i> = <b>10</b> when <i>x</i> = 0. "
                    "5 is how much <i>y</i> goes up each step. Read the scale: each line is 5."))
    its.append(emcq(fig(g4) + "Which expression gives <i>y</i> for any <i>x</i>?", "5x + 10", ["10x + 5", "5x + 15", "x + 5"],
                    "<i>y</i> starts at 10 when <i>x</i> = 0 and goes up by 5 each step: <b>%s</b>. "
                    "%s uses the point for <i>x</i> = 1 as the start." % (X("5x + 10"), X("5x + 15")),
                    [0, 1, 2, 3, 4], [10, 15, 20, 25, 30]))
    g5 = graph_svg([(x, 2 * x + 3) for x in range(0, 4)], 6, 12, label="graph of a linear relation with 4 points")
    its.append(mcq(fig(g5) + "Which list gives the <i>y</i>-values for <i>x</i> = 0, 1, 2, 3?", "3, 5, 7, 9",
                   ["5, 7, 9, 11", "2, 4, 6, 8", "3, 6, 9, 12"],
                   "Read each point: (0, 3), (1, 5), (2, 7), (3, 9). The list is <b>3, 5, 7, 9</b>. "
                   "5, 7, 9, 11 starts at <i>x</i> = 1."))
    its.append(mcq(tbl([1, 2, 3], [4, 6, 8], ("x", "y")) + "Zara plots this table. Her points are (4, 1), (6, 2) and (8, 3). "
                   "What did she do wrong?", "She plotted (<i>y</i>, <i>x</i>), not (<i>x</i>, <i>y</i>)",
                   ["She used the wrong table", "She added 2 to each <i>x</i>", "She should start at (0, 0)"],
                   "The points should be (1, 4), (2, 6), (3, 8). <b>She swapped the numbers.</b> "
                   "Always go across for <i>x</i> first, then up for <i>y</i>."))
    bad = [(1, 3), (2, 5), (3, 8), (4, 9)]
    assert [2 * x + 1 for x, _ in bad] == [3, 5, 7, 9]
    g6 = graph_svg(bad, 6, 12, label="graph of four points, one plotted wrong")
    its.append(mcq(fig(g6) + "These points should follow %s. One point is plotted wrong. Which one?" % X("y = 2x + 1"),
                   pt(3, 8), [pt(1, 3), pt(2, 5), pt(4, 9)],
                   "For <i>x</i> = 3: 2 × 3 + 1 = 7. The point is at <b>(3, 8)</b>, one too high. The other points fit."))
    order = [0, 1, 4, 5, 3, 2, 6, 9, 10, 7, 12, 13, 11, 8, 15, 16, 17, 14, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Plot and read graphs of linear relations", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words():
    its = []
    # taxi: $4 + $2 per km
    its.append(nmcq("A taxi in Vancouver charges $4 to start plus $2 for each kilometre. How much does a 7 km trip cost?",
                    4 + 2 * 7, [13, 42, 14],
                    "Cost = 2 × 7 + 4 = 14 + 4 = <b>$18</b>. $42 adds first: (4 + 2) × 7. $14 forgets the $4 to start.", dol))
    its.append(emcq("A taxi charges $4 to start plus $2 for each kilometre. Which expression gives the cost, in dollars, "
                    "for <i>k</i> kilometres?", "2k + 4", ["4k + 2", "2k", "k + 6"],
                    "Each kilometre adds $2, so start with %s. The $4 is paid once, so add it: <b>%s</b>. "
                    "%s charges $4 for every kilometre." % (X("2k"), X("2k + 4"), X("4k + 2")),
                    [1, 2, 3], [6, 8, 10]))
    its.append(mcq("A taxi charges $4 to start plus $2 for each kilometre. The trip costs $26. How far was the trip?",
                   "11 km", ["13 km", "15 km", "26 km"],
                   "Work backward. Take off the start: $26 − $4 = $22. Each km is $2: 22 ÷ 2 = <b>11 km</b>. "
                   "13 km forgets the $4. 15 km adds the $4 instead of subtracting."))
    assert Fr(7, 2) + Fr(5, 2) * 8 == Fr(47, 2)
    its.append(nmcq("A taxi in Victoria charges $3.50 to start plus $2.50 for each kilometre. How much does an 8 km trip cost?",
                    Fr(47, 2), [20, 48, 14],
                    "2.50 × 8 = 20. Then $20.00 + $3.50 = <b>$23.50</b>. $20.00 forgets the start. "
                    "$48.00 adds first: (3.50 + 2.50) × 8.", money))
    # bike savings: $40 + $20 per week
    its.append(nmcq(tbl([0, 1, 2, 3], [40, 60, 80, 100], ("Weeks", "Savings ($)"), "table of values savings") +
                    "Leah is saving for a new bike. The table shows her savings. How much will she have after 8 weeks?",
                    40 + 20 * 8, [160, 220, 480],
                    "She starts with $40 and adds $20 each week: 20 × 8 + 40 = 160 + 40 = <b>$200</b>. "
                    "$160 forgets the $40 she started with. $220 is after 9 weeks.", dol))
    its.append(emcq("Leah has $40. She saves $20 each week for a bike. Which expression gives her savings, in dollars, "
                    "after <i>w</i> weeks?", "20w + 40", ["40w + 20", "20w", "60w"],
                    "Each week adds $20, so start with %s. She already has $40, so add it once: <b>%s</b>. "
                    "%s adds $40 every week." % (X("20w"), X("20w + 40"), X("40w + 20")),
                    [0, 1, 2, 3], [40, 60, 80, 100]))
    assert 40 + 20 * 13 == 300
    its.append(nmcq("Leah has $40 and saves $20 each week. The bike costs $300. After how many weeks can she buy it?",
                    13, [15, 17, 14],
                    "She still needs $300 − $40 = $260. 260 ÷ 20 = <b>13 weeks</b>. Check: 20 × 13 + 40 = 300. "
                    "15 weeks forgets the $40 she has. 17 adds the $40 instead of subtracting.",
                    lambda v: "%s weeks" % n(v)))
    # Owen savings graph
    ow = [(w, 25 + 15 * w) for w in range(0, 6)]
    g = graph_svg(ow, 6, 120, ystep=10, ylab=20, xname="Weeks", yname="Savings ($)", vals=True, ypre="$",
                  label="graph of savings over 6 weeks")
    its.append(mcq(fig(g) + "Owen saves the same amount each week. What does the point (0, 25) tell you?",
                   "Owen had $25 before he started saving",
                   ["Owen saves $25 each week", "Owen saved for 25 weeks", "Owen has $0 after 25 weeks"],
                   "<i>x</i> = 0 means 0 weeks, before any saving. So <b>Owen had $25 to start</b>. "
                   "He saves $15 each week: 25, 40, 55."))
    its.append(nmcq(fig(g) + "How much does Owen save each week?", 15, [25, 40, 10],
                    "Each week the savings go up from $25 to $40 to $55: $40 − $25 = <b>$15</b>. "
                    "$25 is what he had at the start, not what he adds.", dol))
    # two plans
    assert 15 * 6 == 30 + 10 * 6
    its.append(mcq("A kayak rental in Victoria has two plans. Plan A: $15 per hour. Plan B: $30 plus $10 per hour. "
                   "For how many hours do both plans cost the same?", "6 hours", ["3 hours", "2 hours", "90 hours"],
                   "Make a table. Plan A: $15, $30, $45, $60, $75, $90. Plan B: $40, $50, $60, $70, $80, $90. "
                   "At <b>6 hours</b> both cost $90. 90 is the cost, not the hours."))
    its.append(nmcq("A snowboard rental at Whistler costs $25 per day plus $15 for a helmet (paid once). "
                    "How much does it cost for 4 days?", 25 * 4 + 15, [160, 100, 44],
                    "25 × 4 = 100. Then 100 + 15 = <b>$115</b>. $160 adds the helmet every day: (25 + 15) × 4. "
                    "$100 forgets the helmet.", dol))
    its.append(emcq("A swimming pool in Kelowna charges $12 for a card plus $3.50 for each visit. Which expression gives "
                    "the cost, in dollars, for <i>v</i> visits?", "3.5v + 12", ["12v + 3.5", "15.5v", "3.5v"],
                    "Each visit adds $3.50, so start with %s. The card is paid once: <b>%s</b>. "
                    "%s adds the card price every visit." % (X("3.5v"), X("3.5v + 12"), X("15.5v")),
                    [1, 2, 3], [Fr(31, 2), 19, Fr(45, 2)]))
    its.append(nmcq("A swimming pool charges $12 for a card plus $3.50 for each visit. How much do 10 visits cost?",
                    47, [155, 35, Fr(247, 2)],
                    "3.50 × 10 = 35. Then $35.00 + $12.00 = <b>$47.00</b>. $35.00 forgets the card. "
                    "$155.00 adds the card every visit.", money))
    # rain barrel
    its.append(emcq("A rain barrel in Surrey holds 180 L. Emma uses 12 L each day to water her garden. Which expression gives "
                    "the water left, in litres, after <i>d</i> days?", "180 - 12d", ["12d - 180", "180 + 12d", "168d"],
                    "Each day takes away 12 L, so subtract %s from 180: <b>%s</b>. "
                    "%s adds water, but the barrel is being used up." % (X("12d"), X("180 − 12d"), X("180 + 12d")),
                    [0, 1, 2], [180, 168, 156]))
    assert 180 - 12 * 15 == 0
    its.append(nmcq("A rain barrel holds 180 L. Emma uses 12 L each day. After how many days is it empty?", 15, [14, 12, 180],
                    "180 ÷ 12 = <b>15 days</b>. Check: 180 − 12 × 15 = 0. 12 is the litres used each day, not days. "
                    "After 14 days, 12 L is still left.", lambda v: "%s days" % n(v)))
    its.append(nmcq("For the Terry Fox Run, Simran’s aunt pledges $5 plus $2 for each kilometre Simran runs. "
                    "Simran runs 10 km. How much does her aunt give?", 5 + 2 * 10, [70, 20, 17],
                    "2 × 10 = 20. Then 20 + 5 = <b>$25</b>. $70 adds first: (5 + 2) × 10. $20 forgets the $5.", dol))
    its.append(emcq(tbl([Fr(1, 2), 1, Fr(3, 2), 2], [30, 60, 90, 120], ("Hours", "Distance (km)"), "table of values distance") +
                    "Ji-woo’s family drives on the Sea-to-Sky Highway at a steady speed. Which expression gives the distance, "
                    "in kilometres, after <i>h</i> hours?", "60h", ["h + 30", "30h", "60h + 30"],
                    "In 1 hour they go 60 km, so the distance is <b>%s</b>. Check: 60 × 1.5 = 90. "
                    "%s uses the change in the table, but the hours go up by 0.5, not 1." % (X("60h"), X("30h")),
                    [Fr(1, 2), 1, Fr(3, 2), 2], [30, 60, 90, 120]))
    assert 30 + 15 * 8 == 150
    its.append(nmcq("A cedar seedling is 30 cm tall. It grows 15 cm each year. After how many years will it be 150 cm tall?",
                    8, [10, 12, 9],
                    "It needs to grow 150 − 30 = 120 cm. 120 ÷ 15 = <b>8 years</b>. Check: 15 × 8 + 30 = 150. "
                    "10 years forgets the 30 cm it started with.", lambda v: "%s years" % n(v)))
    tx = [(k, 5 + 3 * k) for k in range(1, 5)]
    g = graph_svg(tx, 6, 20, ystep=1, ylab=4, xname="Distance (km)", yname="Cost ($)", vals=True, ypre="$",
                  label="graph of taxi cost and distance")
    its.append(nmcq(fig(g) + "The graph shows the cost of a taxi trip. The pattern continues. How much would a 10 km trip cost?",
                    35, [30, 38, 80],
                    "The cost goes up $3 each kilometre. At 1 km it is $8, so the start is $8 − $3 = $5. "
                    "Cost = 3 × 10 + 5 = <b>$35</b>. $30 forgets the $5 start. $38 is for 11 km.", dol))
    assert 90 - 6 * 5 == 20 + 8 * 5 == 60
    its.append(nmcq("Mateo has $90 and spends $6 each week on lunch. Sofia has $20 and saves $8 each week. "
                    "After how many weeks will they have the same amount?", 5, [35, 70, 6],
                    "Each week the gap of $70 shrinks by $6 + $8 = $14. 70 ÷ 14 = <b>5 weeks</b>. "
                    "Check: 90 − 30 = 60 and 20 + 40 = 60. 35 divides by 8 − 6, but Mateo goes down while Sofia goes up.",
                    lambda v: "%s weeks" % n(v)))
    order = [0, 1, 15, 4, 5, 10, 3, 8, 7, 2, 12, 11, 13, 14, 6, 17, 16, 18, 9, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Linear relation word problems", "items": [its[i] for i in order]}


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
        "<h2>What is a linear relation?</h2>"
        "<p>A <b>linear relation</b> changes by the same amount each time. You can show it three ways: "
        "a <b>table of values</b>, an <b>expression</b> and a <b>graph</b>. All three show the same pattern.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>Figure 1 has 4 sticks, Figure 2 has 7, Figure 3 has 10. Each figure adds 3.</figcaption></figure>"
        + table(["Figure number (<i>n</i>)", "1", "2", "3", "4"], [["Number of sticks", "4", "7", "10", "13"]]) +
        "<h2>Write an expression</h2>"
        "<p>The change each time is the number that multiplies <i>n</i>. Then fix the start: compare with Figure 1.</p>"
        + ex("Expression for 4, 7, 10, 13", "Write an expression for the number of sticks in Figure <i>n</i>.",
             "The value goes up by 3, so start with 3<i>n</i>. For Figure 1, 3 × 1 = 3, but there are 4 sticks. Add 1.",
             X("3n + 1"))
        + ex("Evaluate", "How many sticks are in Figure 20?",
             "Replace <i>n</i> with 20. Multiply first: 3 × 20 = 60. Then 60 + 1 = 61.", "61 sticks")
        + ex("Work backward", "Which figure has 49 sticks?",
             "Undo + 1: 49 − 1 = 48. Undo × 3: 48 ÷ 3 = 16. Check: 3 × 16 + 1 = 49.", "Figure 16") +
        "<h2>Graph a linear relation</h2>"
        "<p>Each column of the table is a point (<i>x</i>, <i>y</i>). Go <b>across</b> for <i>x</i> first, then <b>up</b> for <i>y</i>. "
        "The points line up in a straight line. For figures, there is no Figure 1.5, so the points are <b>not joined</b>: "
        "the relation is <b>discrete</b>.</p>"
        "<figure class='sn-fig'>" + graph_svg([(1, 4), (2, 7), (3, 10), (4, 13)], 5, 16, ylab=4,
                                               xname="Figure number", yname="Number of sticks", vals=True,
                                               label="graph of figure number and number of sticks") +
        "<figcaption>The points (1, 4), (2, 7), (3, 10), (4, 13). Each step right goes up 3.</figcaption></figure>"
        + ex("Taxi fare", "A taxi charges $4 to start plus $2 for each kilometre. Write an expression and find the cost of 9 km.",
             "Each km adds $2, so 2<i>k</i>. The $4 is paid once: 2<i>k</i> + 4. For 9 km: 2 × 9 + 4 = 22.", "$22") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing “add 3 each time” as <i>n</i> + 3", "The change multiplies <i>n</i>: 3<i>n</i>, then fix the start"],
            ["Using the first value as the number added: 3<i>n</i> + 4 for 4, 7, 10", "Compare 3 × 1 with 4: add 1, so 3<i>n</i> + 1"],
            ["Checking only the first column", "Test the expression on every column"],
            ["Mixing up <i>n</i> and the value", "<i>n</i> is the figure number. The expression gives the count"],
            ["Plotting (<i>y</i>, <i>x</i>)", "Across for <i>x</i> first, then up for <i>y</i>"],
            ["Reading 3<i>n</i> as 37 when <i>n</i> = 7", "3<i>n</i> means 3 × 7 = 21. Multiply before you add"],
        ])
    )


FAQ = [
    {"q": "What are linear relations in Grade 7 math in BC?",
     "a": "In the BC curriculum, Grade 7 students study discrete linear relations: patterns that change by the same amount each time. They show them with tables of values, expressions like 3n + 2 and graphs."},
    {"q": "How do you write an expression from a table of values?",
     "a": "Find how much the value changes each time n goes up by 1 and multiply n by that number. Then compare with the first value and add or subtract to fix the start: 5, 8, 11, 14 gives 3n + 2."},
    {"q": "What does discrete mean in a linear relation?",
     "a": "Discrete means only certain values make sense, such as whole figure numbers. On the graph the points are not joined with a line, because there is no Figure 1.5."},
    {"q": "Are linear relations on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy component is based on the BC curriculum, and patterning is part of Grade 7 math. Practice with tables, expressions and word problems like taxi fares is good preparation."},
]


def gen():
    rnd = random.Random(37809)
    sets = [set_tables(), set_expressions(), set_evaluate(), set_graphs(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "linear-relations",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Linear Relations: Tables, Expressions and Graphs",
        "seo_title": "Grade 7 Linear Relations Worksheets: Tables of Values, Expressions and Graphs (BC Math, Free)",
        "short_title": "Linear relations",
        "domain": "Patterning",
        "standard_code": "Grade 7: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Discrete linear relations, using expressions, tables, and graphs",
        "meta_desc": "Free Grade 7 math worksheets on discrete linear relations: build tables of values from patterns, write expressions like 3n + 2, evaluate them, plot and read graphs, and solve taxi fare and saving problems. 100 questions with an answer key, matched to the BC curriculum and good FSA practice.",
        "key_big": "A linear relation changes by the same amount each time, and that amount multiplies n.",
        "key_sub": "For 5, 8, 11, 14 the value goes up by 3, so start with 3n. When n = 1, 3n is 3 but the value is 5, so add 2: 3n + 2. To graph it, plot each pair (x, y): across first, then up.",
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
