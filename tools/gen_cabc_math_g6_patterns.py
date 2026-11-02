# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Patterns, tables and graphs (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g6_patterns.py
Increasing and decreasing patterns, using expressions, tables, and graphs as functional relationships:
tables of values and input/output tables, expressions for patterns such as 2n + 3, graphing a pattern
in the first quadrant, decreasing patterns such as 30 − 4n, and word problems in BC contexts.
Wrong answers come from real mistakes: a rule that fits only the first step (or only the first pair),
plotting (y, x), "add 2 each time" written as n + 2, using the first value as the number added,
ignoring skipped inputs, counting n jumps instead of n − 1, reading 3n as 3 + n or as 38, doing the
operations in the wrong order, and going the wrong way in a decreasing pattern.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
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



def triangles(k):
    """A row of k triangles made of sticks (pointing up and down in turn): 2k + 1 sticks."""
    S = 28
    h = S * 0.866

    def draw(x, y):
        pts = []
        for i in range(k + 2):
            if i % 2 == 0:
                pts.append((x + (i // 2) * S, y + h))
            else:
                pts.append((x + (i // 2) * S + S / 2, y))
        s = [stick(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]) for i in range(k + 1)]
        bot = [p for i, p in enumerate(pts) if i % 2 == 0]
        top = [p for i, p in enumerate(pts) if i % 2 == 1]
        for row in (bot, top):
            for i in range(len(row) - 1):
                s.append(stick(row[i][0], row[i][1], row[i + 1][0], row[i + 1][1]))
        assert len(s) == 2 * k + 1
        return "".join(s)
    w = ((k + 1) // 2) * S + (S / 2 if (k + 1) % 2 else 0)
    return w, h, draw


PATTERNS["tri"] = (triangles, lambda k: 2 * k + 1, "sticks")
TN = ("Term number", "Term value")
IO = ("Input", "Output")
GX, GY = "Term number", "Term value"


def tv(top, bot, heads=TN, label="table of values"):
    return tbl(top, bot, heads, label)


def jumps_e(a1, k, N, ans, what="value"):
    sg = "+" if k > 0 else "−"
    return ("From term 1 to term %d there are %d jumps of %s: %s %s %d × %s = %s." % (
        N, N - 1, n(abs(k)), n(a1), sg, N - 1, n(abs(k)), n(ans)))


def rule_text(a, b):
    if a == 1:
        return "Add %s" % n(b)
    if b == 0:
        return "Multiply by %s" % n(a)
    return "Multiply by %s, then %s %s" % (n(a), "add" if b > 0 else "subtract", n(abs(b)))


# ============================================================ set 1: tables of values
def set_tables():
    its = []
    # A: shape patterns, two figures ahead
    for nm in ["sq", "L", "tables", "towers"]:
        c = [cnt(nm, k) for k in range(1, 6)]
        k = c[1] - c[0]
        ans = c[4]
        assert ans == c[0] + 4 * k
        q = fig(pattern_svg(nm)) + "The pattern continues. How many %s are in Figure 5?" % thing(nm)
        e = ("Count: %s. Each figure adds %d %s. Figure 4 has %d and Figure 5 has %d + %d = <b>%d</b>. "
             "(%d is Figure 4, only one step ahead. %d is 5 × %d, but each figure adds %d, not %d.)"
             % (lst(c[:3]), k, thing(nm), c[3], c[3], k, ans, c[3], 5 * c[0], c[0], k, c[0]))
        its.append(nmcq(q, ans, [c[3], 5 * c[0], 5 * k + c[0]], e))
    # B: missing value, consecutive term numbers
    rows = [([6, 11, 16, None, 26], 21, [20, 22, 31], "The value goes up by 5 each time: 16 + 5 = <b>21</b>. Check: 21 + 5 = 26."),
            ([2, 5, 8, 11, None], 14, [13, 15, 17], "The value goes up by 3 each time: 11 + 3 = <b>14</b>. (17 adds two jumps.)"),
            (["2.5", 4, "5.5", None, "8.5"], 7, [6, "6.5", 10],
             "The value goes up by 1.5 each time: 5.5 + 1.5 = <b>7</b>. Check: 7 + 1.5 = 8.5. (6.5 adds only 1.)"),
            ([7, 15, None, 31, 39], 23, [22, 24, 47], "The value goes up by 8 each time: 15 + 8 = <b>23</b>. Check: 23 + 8 = 31. "
             "(47 is the next value after 39, not the missing one.)")]
    for vals, ans, wrong, e in rows:
        full = [Fr(v) if v is not None else Fr(ans) for v in vals]
        d = full[1] - full[0]
        assert all(full[i + 1] - full[i] == d for i in range(4))
        bot = [Fr(v) if v is not None else "?" for v in vals]
        its.append(nmcq(tv([1, 2, 3, 4, 5], bot) + "What value is missing from the table?", ans, wrong, e))
    # C: far term from a table (n − 1 jumps)
    for a, b, N in [(3, 2, 10), (5, 1, 12), (4, 3, 20), (6, -2, 15)]:
        vals = [a * i + b for i in range(1, 5)]
        ans = a * N + b
        e = ("The value goes up by %d each time. From term 1 to term %d there are %d jumps: %d + %d × %d = <b>%s</b>. "
             "(%s is term 5, the next value only. %s makes %d jumps, one too many.)"
             % (a, N, N - 1, vals[0], N - 1, a, n(ans), n(vals[3] + a), n(vals[0] + N * a), N))
        its.append(nmcq(tv([1, 2, 3, 4], vals) + "The pattern continues. What is the term value for term number %d?" % N,
                        ans, [vals[3] + a, N * vals[0], vals[0] + N * a], e))
    # D: input/output tables with skipped inputs
    rows = [
        ([1, 2, 3, 5, 8], 4, 1, [25, 32, 29],
         "The inputs skip. From 1 to 2 the output goes up by 4, so the rule is multiply by 4, then add 1. "
         "4 × 8 + 1 = <b>33</b>. (25 adds 4 once, but the input jumped from 5 to 8.)"),
        ([1, 2, 4, 6, 10], 2, 5, [21, 19, 20],
         "From 1 to 2 the output goes up by 2, so the rule is multiply by 2, then add 5. 2 × 10 + 5 = <b>25</b>. "
         "(21 copies the last change, +4, but the input jumped by 4, not 2.)"),
        ([1, 3, 5, 7, 8], 3, 1, [28, 24, 23],
         "The input goes up by 2 and the output goes up by 6, so each 1 adds 3. Rule: multiply by 3, then add 1. "
         "3 × 8 + 1 = <b>25</b>. (28 adds 6 again, but the input only went up by 1.)"),
    ]
    for ins, a, b, wrong, e in rows:
        outs = [a * i + b for i in ins]
        its.append(nmcq(tv(ins, outs[:-1] + ["?"], IO, "input output table") + "What is the missing output?",
                        outs[-1], wrong, e))
    ins = [2, 4, 7, 9]
    outs = [3 * i - 1 for i in ins]
    its.append(nmcq(tv(ins, outs[:-1] + ["?"], IO, "input output table") +
                    "The rule is: multiply the input by 3, then subtract 1. What is the missing output?", outs[-1],
                    [24, 27, 11],
                    "Multiply first, then subtract: 3 × 9 = 27, and 27 − 1 = <b>26</b>. "
                    "(24 subtracts first: 3 × 8. 27 forgets to subtract 1.)"))
    # E: which rule fits every pair (not only the first)
    rows = [([1, 2, 3, 4], (3, 2), [(1, 4), (5, 0), (1, 3)]),
            ([2, 3, 4, 5], (2, 3), [(1, 5), (1, 2), (3, 1)]),
            ([1, 2, 3, 4], (5, -1), [(1, 3), (4, 0), (1, 5)]),
            ([3, 4, 5, 6], (3, 1), [(1, 7), (1, 3), (4, -2)])]
    for ins, (a, b), wrong in rows:
        outs = [a * i + b for i in ins]
        for wa, wb in wrong:
            assert any(wa * i + wb != o for i, o in zip(ins, outs))
        step = outs[1] - outs[0]
        first = [rule_text(wa, wb) for wa, wb in wrong if wa * ins[0] + wb == outs[0]]
        e = ("Test every pair: %s. <b>%s</b> works for all of them. %s %s how much the output grows each time, "
             "not the rule from input to output." % (
                 ", ".join("%s × %s %s %s = %s" % (n(a), n(i), "+" if b > 0 else "−", n(abs(b)), n(o)) for i, o in zip(ins, outs)),
                 rule_text(a, b),
                 ("“" + "” and “".join(first) + "” work for the first pair only.") if first else "",
                 "“Add %d” is" % step))
        assert (1, step) in wrong
        its.append(mcq(tv(ins, outs, IO, "input output table") + "Which rule works for every pair in the table?",
                       rule_text(a, b), [rule_text(wa, wb) for wa, wb in wrong], e))
    return {"title": "Tables of values", "items": its}


# ============================================================ set 2: expressions for patterns
def set_expressions():
    its = []
    N4 = [1, 2, 3, 4]
    # B first (easiest): evaluate
    rows = [("2n + 3", 8, [13, 31, 22], "2 + 8 + 3 = 13 reads 2<i>n</i> as 2 + <i>n</i>. 31 reads 2<i>n</i> as 28."),
            ("4n + 5", 6, [15, 51, 44], "4 + 6 + 5 = 15 reads 4<i>n</i> as 4 + <i>n</i>. 51 reads 4<i>n</i> as 46."),
            ("6n - 4", 7, [9, 63, 18], "6 + 7 − 4 = 9 reads 6<i>n</i> as 6 + <i>n</i>. 63 reads 6<i>n</i> as 67."),
            ("5n + 2", "1.2", ["8.2", "7.2", 16], "8.2 adds instead of multiplying. 7.2 multiplies only the 1 by 5 and just adds the 0.2.")]
    for s, v, wrong, why in rows:
        v = Fr(v)
        ans = ev(s, v)
        a, b = [Fr(x) for x in re.match(r"(\d+)n ([+-]) (\d+)", s).group(1, 3)]
        sg = "+" if "+" in s else "−"
        e = ("Replace <i>n</i> with %s. Multiply first: %s × %s = %s. Then %s %s %s = <b>%s</b>. (%s)" % (
            n(v), n(a), n(v), n(a * v), n(a * v), sg, n(b), n(ans), why))
        its.append(nmcq("What is the value of <b>%s</b> when <i>n</i> = %s?" % (X(s), n(v)), ans, wrong, e))
    # A: expression from a table
    rows = [(2, 3, ["n + 2", "2n + 5", "5n"]), (3, 1, ["n + 3", "3n + 4", "4n"]),
            (4, -1, ["n + 4", "4n + 3", "3n"]), (5, 2, ["n + 5", "5n + 7", "7n"])]
    for a, b, wrong in rows:
        vals = [a * i + b for i in N4]
        r = lin(a, b)
        e = ("The value goes up by %d each time, so start with %s. Term 1: %d × 1 = %d, but the value is %d, so %s: <b>%s</b>. "
             "Check term 4: %d × 4 %s %d = %d. (%s adds %d only once, not each time. %s uses the first value as the number added.)"
             % (a, X(lin(a, 0)), a, a, vals[0], ("add %d" % b) if b > 0 else ("subtract %d" % -b), X(r),
                a, "+" if b > 0 else "−", abs(b), vals[3], X(wrong[0]), a, X(wrong[1])))
        its.append(emcq(tv(N4, vals) + "Which expression gives the term value for term number <i>n</i>?", r, wrong, e, N4, vals))
    # D: which list matches the expression
    for a, b, wrong_lists in [(3, 2, None), (2, 5, None), (4, 3, None), (5, 1, None)]:
        s = lin(a, b)
        right = lst([a * i + b for i in N4])
        from0 = lst([a * i + b for i in range(0, 4)])
        swap = lst([b * i + a for i in N4])
        times = lst([(a + b) * i for i in N4])
        e = ("Replace <i>n</i> with 1, 2, 3 and 4: %d × 1 + %d = %d, %d × 2 + %d = %d, and so on: <b>%s</b>. "
             "(%s starts at <i>n</i> = 0. %s swaps the two numbers in the expression.)" % (
                 a, b, a + b, a, b, 2 * a + b, right, from0, swap))
        its.append(mcq("Which list shows the first four term values of <b>%s</b>? (The first term number is 1.)" % X(s),
                       right, [from0, swap, times], e))
    # C: expression from a shape pattern
    rows = [("tri", ["3n", "n + 2", "2n + 3"]), ("sq", ["4n", "n + 3", "3n + 4"]),
            ("L", ["3n - 2", "n + 2", "2n + 1"]), ("towers", ["6n", "n + 3", "3n + 6"])]
    for nm, wrong in rows:
        c = [cnt(nm, k) for k in range(1, 6)]
        a = c[1] - c[0]
        b = c[0] - a
        r = lin(a, b)
        e = ("Count: %s. Each figure adds %d, so start with %s. Figure 1: %d × 1 = %d, and it has %d, so %s: <b>%s</b>. "
             "Check Figure 3: %d × 3 %s %d = %d. (%s works for Figure 1 only.)" % (
                 lst(c[:3]), a, X(lin(a, 0)), a, a, c[0], ("add %d" % b) if b > 0 else ("subtract %d" % -b), X(r),
                 a, "+" if b > 0 else "−", abs(b), c[2], X(wrong[0])))
        assert ev(wrong[0], 1) == c[0]
        its.append(emcq(fig(pattern_svg(nm)) + "Which expression gives the number of %s in Figure <i>n</i>?" % thing(nm),
                        r, wrong, e, [1, 2, 3, 4, 5], c))
    # E: work backwards
    for a, b, V, wrong in [(4, 2, 42, [42, 11, 170]), (5, 5, 60, [60, 13, 12]), (2, 3, 31, [31, 17, 65])]:
        s = lin(a, b)
        N = Fr(V - b, a)
        assert N.denominator == 1 and ev(s, N) == V
        e = ("Work backwards. Undo + %d: %d − %d = %d. Undo × %d: %d ÷ %d = <b>%s</b>. Check: %d × %s + %d = %d. "
             "(%s adds %d instead of subtracting. %d is the term value, not the term number.)" % (
                 b, V, b, V - b, a, V - b, a, n(N), a, n(N), b, V, n(wrong[1]), b, V))
        assert Fr(V + b, a) == wrong[1]
        its.append(nmcq("The rule for a pattern is <b>%s</b>. Which term number has a term value of %d?" % (X(s), V),
                        N, wrong, e))
    good, bad = 31, [30, 32, 33]
    assert (good - 1) % 3 == 0 and all((x - 1) % 3 for x in bad)
    its.append(nmcq("Which number is a term value of the pattern <b>%s</b>?" % X("3n + 1"), good, bad,
                    "Undo the rule: 31 − 1 = 30, and 30 ÷ 3 = 10, a whole term number. Check: 3 × 10 + 1 = <b>31</b>. "
                    "For 30, 32 and 33, subtracting 1 does not give a multiple of 3."))
    order = [0, 1, 2, 3, 4, 5, 8, 9, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Expressions for patterns (2n + 3)", "items": [its[i] for i in order]}


# ============================================================ set 3: graph a pattern
ABCD = ["Graph A", "Graph B", "Graph C", "Graph D"]


def set_graphs():
    its = []
    p1 = [(i, 3 * i - 1) for i in range(1, 5)]
    g1t = graph_svg(p1, 6, 14, xname=GX, yname=GY, tags={(3, 8): "P"}, label="graph of a pattern with point P")
    its.append(mcq(fig(g1t) + "Each point is (term number, term value). What are the coordinates of point P?",
                   pt(3, 8), [pt(8, 3), pt(3, 7), pt(4, 8)],
                   "Go across first, then up. P is 3 across and 8 up, so it is <b>(3, 8)</b>. "
                   "(8, 3) gives the numbers in the wrong order: the term number comes first."))
    g1 = graph_svg(p1, 6, 14, xname=GX, yname=GY, label="graph of a pattern with 4 points")
    its.append(nmcq(fig(g1) + "What is the term value for term number 4?", 11, [4, 8, 14],
                    "Find 4 on the term number axis and go up to the point. Read across: <b>11</b>. "
                    "4 is the term number. 8 is the value for term number 3."))
    its.append(mcq("To plot the point (4, 9), start at (0, 0). How do you move?", "4 right, then 9 up",
                   ["9 right, then 4 up", "4 right, then 5 up", "3 right, then 9 up"],
                   "The first number tells how far across and the second tells how far up: <b>4 right, then 9 up</b>. "
                   "9 right, then 4 up plots (9, 4)."))
    its.append(mcq(tv([1, 2, 3, 4], [6, 8, 10, 12]) + "Mei graphs this table. Which point shows term number 3?",
                   pt(3, 10), [pt(10, 3), pt(3, 12), pt(4, 10)],
                   "Each column is one point (term number, term value). Under 3 is 10, so plot <b>(3, 10)</b>. "
                   "(10, 3) plots the numbers the wrong way around."))
    # A-D graphs (one answer in each position)
    want = [(1, 1), (2, 3), (3, 5)]
    pan = [[(1, 1), (3, 2), (5, 3)], want, [(1, 1), (2, 2), (3, 3)], [(1, 2), (2, 4), (3, 6)]]
    its.append(mcq_fixed(fig(panels_svg(pan, "four graphs A to D")) +
                         "A table has term numbers 1, 2, 3 and term values 1, 3, 5. Which graph shows it?", ABCD, 1,
                         "The points are (1, 1), (2, 3), (3, 5): <b>Graph B</b>. Graph A plots (term value, term number). "
                         "Graph C goes up by 1, not 2."))
    want = [(1, 4), (2, 6), (3, 8)]
    pan = [[(1, 4), (2, 5), (3, 6)], [(4, 1), (6, 2), (8, 3)], [(1, 2), (2, 4), (3, 6)], want]
    its.append(mcq_fixed(fig(panels_svg(pan, "four graphs A to D")) +
                         "Which graph shows %s for <i>n</i> = 1, 2, 3?" % X("2n + 2"), ABCD, 3,
                         "2 × 1 + 2 = 4, 2 × 2 + 2 = 6, 2 × 3 + 2 = 8. The points are (1, 4), (2, 6), (3, 8): <b>Graph D</b>. "
                         "Graph B plots (term value, term number). Graph C shows 2<i>n</i> without the + 2."))
    want = [(1, 5), (2, 6), (3, 7)]
    pan = [want, [(5, 1), (6, 2), (7, 3)], [(1, 4), (2, 5), (3, 6)], [(1, 7), (2, 6), (3, 5)]]
    its.append(mcq_fixed(fig(panels_svg(pan, "four graphs A to D")) +
                         "Which graph shows %s for <i>n</i> = 1, 2, 3?" % X("n + 4"), ABCD, 0,
                         "1 + 4 = 5, 2 + 4 = 6, 3 + 4 = 7. The points are (1, 5), (2, 6), (3, 7): <b>Graph A</b>. "
                         "Graph B swaps the numbers. Graph D goes down, but <i>n</i> + 4 goes up."))
    want = [(1, 2), (2, 5), (3, 8)]
    pan = [[(1, 3), (2, 5), (3, 7)], [(2, 1), (5, 2), (8, 3)], want, [(1, 2), (2, 4), (3, 6)]]
    its.append(mcq_fixed(fig(panels_svg(pan, "four graphs A to D")) +
                         "Which graph shows %s for <i>n</i> = 1, 2, 3?" % X("3n − 1"), ABCD, 2,
                         "3 × 1 − 1 = 2, 3 × 2 − 1 = 5, 3 × 3 − 1 = 8. The points are (1, 2), (2, 5), (3, 8): <b>Graph C</b>. "
                         "Graph B plots (term value, term number). Graph D goes up by 2, not 3."))
    # next point and far points
    p2 = [(i, 4 * i + 1) for i in range(1, 5)]
    g2 = graph_svg(p2, 6, 24, ylab=4, xname=GX, yname=GY, label="graph of a pattern going up by 4")
    its.append(mcq(fig(g2) + "The pattern continues. Which point comes next?", pt(5, 21), [pt(21, 5), pt(5, 20), pt(6, 21)],
                   "The next term number is 5. The values go up by 4: 17 + 4 = 21. The point is <b>(5, 21)</b>. "
                   "(21, 5) swaps the numbers: the term number comes first."))
    its.append(nmcq(fig(g2) + "The pattern continues. What is the term value for term number 8?", 33, [21, 32, 40],
                    "The values are 5, 9, 13, 17 and go up by 4. The rule is %s: 4 × 8 + 1 = <b>33</b>. "
                    "21 is term 5, the next point only. 40 is 8 × 5." % X("4n + 1")))
    p3 = [(i, 2 * i + 4) for i in range(1, 5)]
    assert ev("2n + 4", 10) == 24
    g3 = graph_svg(p3, 6, 14, xname=GX, yname=GY, label="graph of a pattern going up by 2")
    its.append(mcq(fig(g3) + "The rule for this pattern is %s. Which point would also be on the graph?" % X("2n + 4"),
                   pt(10, 24), [pt(24, 10), pt(10, 20), pt(10, 26)],
                   "For term number 10: 2 × 10 + 4 = 24, so the point is <b>(10, 24)</b>. "
                   "(10, 20) forgets the + 4. (24, 10) swaps the numbers."))
    p4 = [(i, 3 * i + 2) for i in range(1, 5)]
    g4 = graph_svg(p4, 6, 16, ylab=4, xname=GX, yname=GY, vals=True, label="graph of a pattern with values")
    its.append(emcq(fig(g4) + "Which expression gives the term value for term number <i>n</i>?", "3n + 2",
                    ["n + 3", "3n + 5", "5n"],
                    "The values are 5, 8, 11, 14. They go up by 3, so start with %s. 3 × 1 = 3 and the value is 5, "
                    "so add 2: <b>%s</b>. (%s uses the first value as the number added.)" % (X("3n"), X("3n + 2"), X("3n + 5")),
                    [1, 2, 3, 4], [5, 8, 11, 14]))
    # mistakes: (y, x) and a wrong point
    its.append(mcq(tv([1, 2, 3], [3, 5, 7]) + "Noah graphs this table. His points are (3, 1), (5, 2) and (7, 3). "
                   "What did he do wrong?", "He plotted (term value, term number)",
                   ["He used the wrong table", "He added 2 to each term number", "He should start at (3, 3)"],
                   "The points should be (1, 3), (2, 5), (3, 7). <b>He swapped the numbers.</b> "
                   "Go across for the term number first, then up for the term value."))
    bad = [(1, 4), (2, 6), (3, 9), (4, 10)]
    assert [2 * x + 2 for x, _ in bad] == [4, 6, 8, 10]
    g5 = graph_svg(bad, 6, 12, xname=GX, yname=GY, label="graph of four points, one plotted wrong")
    its.append(mcq(fig(g5) + "These points should follow %s. One point is plotted wrong. Which one?" % X("2n + 2"),
                   pt(3, 9), [pt(1, 4), pt(2, 6), pt(4, 10)],
                   "For term number 3: 2 × 3 + 2 = 8. The point is at <b>(3, 9)</b>, one too high. The other points fit."))
    good = [(1, 2), (2, 7), (4, 17)]
    assert all(ev("5n - 3", a) == b for a, b in good) and ev("5n - 3", 3) != 13
    its.append(mcq("Which point is <b>not</b> on the graph of %s?" % X("5n − 3"), pt(3, 13), [pt(a, b) for a, b in good],
                   "Test each point. For term number 3: 5 × 3 − 3 = 12, not 13, so <b>(3, 13)</b> is not on the graph. "
                   "(1, 2), (2, 7) and (4, 17) all work."))
    sw = [(4, 1), (6, 2), (8, 3)]
    g6 = graph_svg(sw, 8, 8, xname=GX, yname=GY, label="graph with swapped points")
    its.append(mcq(fig(g6) + "Kai wants to graph the pattern 4, 6, 8 (term numbers 1, 2, 3). This is his graph, but he "
                   "swapped the numbers. Where should the point for term number 2 be?", pt(2, 6),
                   [pt(6, 2), pt(2, 4), pt(3, 6)],
                   "Term number 2 has a term value of 6, so the point is <b>(2, 6)</b>: 2 across, 6 up. "
                   "Kai plotted (6, 2), with the term value first."))
    # scale and linear shape
    p5 = [(i, 5 * i + 10) for i in range(1, 5)]
    g7 = graph_svg(p5, 6, 35, ystep=5, ylab=5, xname=GX, yname=GY, label="graph of a pattern going up by 5")
    its.append(nmcq(fig(g7) + "How much does the term value go up for each new term?", 5, [10, 15, 1],
                    "The points are (1, 15), (2, 20), (3, 25), (4, 30). Each step right goes up <b>5</b>. "
                    "Read the scale: each grid line is 5, not 1. 15 is the first value."))
    its.append(emcq(fig(g7) + "Which expression gives the term value for term number <i>n</i>?", "5n + 10",
                    ["10n + 5", "5n + 15", "15n"],
                    "The values 15, 20, 25, 30 go up by 5, so start with %s. 5 × 1 = 5 and the value is 15, so add 10: <b>%s</b>. "
                    "(%s works for term 1 only.)" % (X("5n"), X("5n + 10"), X("15n")),
                    [1, 2, 3, 4], [15, 20, 25, 30]))
    its.append(mcq("The points of a pattern lie on a straight line going up. What does that tell you?",
                   "The value goes up by the same amount each time",
                   ["The value doubles each time", "The value goes down each time", "Every term value is the same"],
                   "Points in a straight line mean the pattern grows by <b>the same amount each time</b>, like 3, 5, 7, 9. "
                   "A doubling pattern like 1, 2, 4, 8 curves up more and more."))
    its.append(mcq("For term numbers 1, 2, 3, 4, which pattern makes points in a straight line?", "3, 6, 9, 12",
                   ["1, 2, 4, 8", "1, 4, 9, 16", "2, 3, 5, 8"],
                   "Check every step, not only the first. 3, 6, 9, 12 goes up by 3 each time, so its points line up: "
                   "<b>3, 6, 9, 12</b>. 1, 2, 4, 8 goes up by 1, then 2, then 4."))
    return {"title": "Graph a pattern", "items": its}


# ============================================================ set 4: decreasing patterns
def set_decreasing():
    its = []
    for s0, k, wrong_extra in [(50, 4, 35), (85, 5, 66), ("6.4", "0.3", "2.5"), (120, 15, 65)]:
        s0, k = Fr(s0), Fr(k)
        xs = [s0 - i * k for i in range(5)]
        if k.denominator != 1:
            note = "(2.5 subtracts 3 instead of 0.3.)"
        else:
            note = "(%s goes the wrong way: the pattern gets smaller.)" % n(xs[3] + k)
        e = "The pattern goes down by %s each time (%s − %s = %s). Next: %s − %s = <b>%s</b>. %s" % (
            n(k), n(xs[0]), n(k), n(xs[1]), n(xs[3]), n(k), n(xs[4]), note)
        its.append(nmcq("What is the next term?<br><b>%s, ?</b>" % lst(xs[:4]), xs[4],
                        [xs[3] - 2 * k, xs[3] + k, Fr(wrong_extra)], e))
    # missing value
    for s0, k, miss in [(40, 6, 2), (100, 12, 3), (75, 8, 4), ("4.8", "0.4", 2)]:
        s0, k = Fr(s0), Fr(k)
        xs = [s0 - i * k for i in range(5)]
        bot = [("?" if i == miss else x) for i, x in enumerate(xs)]
        prev = xs[miss - 1]
        e = "The value goes down by %s each time: %s − %s = <b>%s</b>." % (n(k), n(prev), n(k), n(xs[miss]))
        if miss < 4:
            e += " Check: %s − %s = %s." % (n(xs[miss]), n(k), n(xs[miss + 1]))
        cands = [prev + k, xs[miss] - k, xs[miss] + Fr(1, 10) if k.denominator != 1 else xs[miss] + 1]
        its.append(nmcq(tv([1, 2, 3, 4, 5], bot) + "What value is missing from the table?", xs[miss], cands, e))
    # expressions
    rows = [(30, 4, ["26 - 4n", "n - 4", "30 - n"]), (50, 7, ["43 - 7n", "7n + 43", "50 - n"]),
            (20, 3, ["17 - 3n", "n - 3", "3n + 17"]), (64, 9, ["55 - 9n", "9n - 64", "64 - n"])]
    for c0, a, wrong in rows:
        vals = [c0 - a * i for i in range(1, 5)]
        r = "%d - %dn" % (c0, a)
        e = ("The value goes down by %d each time, so the expression subtracts %s. Term 1 is %d, so start one jump higher: "
             "%d + %d = %d. The rule is <b>%s</b>. Check term 4: %d − %d × 4 = %d. (%s uses the first value as the start.)"
             % (a, X("%dn" % a), vals[0], vals[0], a, c0, X(r), c0, a, vals[3], X(wrong[0])))
        its.append(emcq(tv([1, 2, 3, 4], vals) + "Which expression gives the term value for term number <i>n</i>?",
                        r, wrong, e, [1, 2, 3, 4], vals))
    # graphs
    pd = [(i, 17 - 3 * i) for i in range(1, 5)]
    gd = graph_svg(pd, 6, 16, xname=GX, yname=GY, label="graph of a decreasing pattern")
    its.append(mcq(fig(gd) + "The pattern keeps going down in the same way. Which point comes next?", pt(5, 2),
                   [pt(2, 5), pt(5, 3), pt(6, 2)],
                   "The values are 14, 11, 8, 5. They go down by 3, so term 5 is 5 − 3 = 2. The point is <b>(5, 2)</b>. "
                   "(2, 5) swaps the numbers."))
    want = [(1, 7), (2, 5), (3, 3)]
    pan = [[(7, 1), (5, 2), (3, 3)], [(1, 3), (2, 5), (3, 7)], [(1, 7), (2, 6), (3, 5)], want]
    its.append(mcq_fixed(fig(panels_svg(pan, "four graphs A to D")) +
                         "Which graph shows the decreasing pattern 7, 5, 3 for term numbers 1, 2, 3?", ABCD, 3,
                         "The points are (1, 7), (2, 5), (3, 3): <b>Graph D</b>. Graph A plots (term value, term number). "
                         "Graph B goes up. Graph C goes down by 1, not 2."))
    pz = [(i, 20 - 4 * i) for i in range(1, 5)]
    gz = graph_svg(pz, 6, 16, ylab=4, xname=GX, yname=GY, label="graph of a pattern going down by 4")
    its.append(nmcq(fig(gz) + "The pattern keeps going down in the same way. Which term number has a term value of 0?",
                    5, [0, 4, 6],
                    "The values are 16, 12, 8, 4. Go down 4 more: term number <b>5</b> has 0. "
                    "0 is the term value, not the term number. Term 4 has 4."))
    pc = [(i, 18 - 2 * i) for i in range(1, 5)]
    gc = graph_svg(pc, 6, 16, ylab=4, xname=GX, yname=GY, label="graph of a pattern going down by 2")
    its.append(mcq(fig(gc) + "How does the term value change from one term to the next?", "It goes down by 2",
                   ["It goes up by 2", "It goes down by 16", "It goes down by 1"],
                   "The points are (1, 16), (2, 14), (3, 12), (4, 10). Each step right drops 2: <b>it goes down by 2</b>. "
                   "16 is the first value, not the change."))
    # harder
    assert ev("60 - 4n", 9) == 24
    its.append(nmcq("The rule for a pattern is <b>%s</b>. What is the term value for term number 9?" % X("60 − 4n"), 24,
                    [504, 47, 28],
                    "Multiply first: 4 × 9 = 36. Then 60 − 36 = <b>24</b>. "
                    "(504 works left to right: (60 − 4) × 9. 47 reads 4<i>n</i> as 4 + <i>n</i>. 28 is term 8.)"))
    xs = [90 - 6 * i for i in range(10)]
    its.append(nmcq("The pattern continues: <b>90, 84, 78, …</b><br>What is the term value for term number 10?", xs[9],
                    [30, 60, 42],
                    "It goes down by 6. From term 1 to term 10 there are 9 jumps: 9 × 6 = 54, and 90 − 54 = <b>36</b>. "
                    "(30 makes 10 jumps. 42 is term 9.)"))
    assert ev("49 - 4n", 9) == 13
    its.append(nmcq("The rule for a pattern is <b>%s</b>. Which term number has a term value of 13?" % X("49 − 4n"), 9,
                    [13, 36, 8],
                    "The amount taken away is 49 − 13 = 36. 36 ÷ 4 = <b>9</b>. Check: 49 − 4 × 9 = 13. "
                    "(36 forgets to divide by 4. 13 is the term value, not the term number.)"))
    xs = [100 - 7 * i for i in range(12)]
    first = next(x for x in xs if x < 50)
    assert first == 44
    its.append(nmcq("The pattern continues: <b>100, 93, 86, 79, …</b><br>What is the first term value that is less than 50?",
                    first, [51, 43, 49],
                    "Keep subtracting 7: 100, 93, 86, 79, 72, 65, 58, 51, <b>44</b>. "
                    "51 is still more than 50. 43 and 49 are not in the pattern."))
    order = [0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 13, 14, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Decreasing patterns", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words():
    its = []
    hrs = lambda v: "%s hours" % n(v)
    km = lambda v: "%s km" % n(v)
    # bike rental at Stanley Park: $12 + $6 per hour
    its.append(nmcq("A bike rental near Stanley Park costs $12 plus $6 for each hour. How much does a 4-hour rental cost?",
                    12 + 6 * 4, [72, 24, 30],
                    "Multiply first: 6 × 4 = 24. Then 24 + 12 = <b>$36</b>. "
                    "$72 adds first: (12 + 6) × 4. $24 forgets the $12.", dol))
    its.append(emcq("A bike rental costs $12 plus $6 for each hour. Which expression gives the cost, in dollars, for "
                    "<i>h</i> hours?", "6h + 12", ["12h + 6", "18h", "6h"],
                    "Each hour adds $6, so start with %s. The $12 is paid once: <b>%s</b>. "
                    "%s charges $12 for every hour." % (X("6h"), X("6h + 12"), X("12h + 6")), [1, 2, 3], [18, 24, 30]))
    assert 12 + 6 * 7 == 54
    its.append(nmcq("A bike rental costs $12 plus $6 for each hour. Mei’s family pays $54 for one bike. How many hours "
                    "did they rent it?", 7, [9, 3, 11],
                    "Take away the $12 first: 54 − 12 = 42. Then 42 ÷ 6 = <b>7 hours</b>. Check: 6 × 7 + 12 = 54. "
                    "(9 hours forgets the $12. 11 hours adds the $12 instead of subtracting.)", hrs))
    # snow melting at Whistler
    assert 120 - 8 * 6 == 72
    its.append(nmcq("In spring, the snow at a Whistler trail marker is 120 cm deep. It melts 8 cm each day. "
                    "How deep is the snow after 6 days?", 72, [48, 168, 80],
                    "8 × 6 = 48 cm melts. 120 − 48 = <b>72 cm</b>. (48 cm is the part that melted. "
                    "168 cm adds instead of subtracting. 80 cm is after 5 days.)", lambda v: "%s cm" % n(v)))
    its.append(emcq("The snow is 120 cm deep and melts 8 cm each day. Which expression gives the depth, in centimetres, "
                    "after <i>d</i> days?", "120 - 8d", ["8d - 120", "120 + 8d", "112d"],
                    "It starts at 120 and loses 8 each day, so subtract %s: <b>%s</b>. "
                    "%s makes the snow get deeper." % (X("8d"), X("120 − 8d"), X("120 + 8d")), [0, 1, 2], [120, 112, 104]))
    # Terry Fox Run training
    assert 2 + Fr(1, 2) * 8 == 6
    its.append(nmcq("To train for the Terry Fox Run, Ryan runs 2 km in week 1. Each week he runs 0.5 km more. "
                    "How far does he run in week 9?", 6, [Fr(13, 2), Fr(9, 2), 18],
                    "From week 1 to week 9 there are 8 jumps: 8 × 0.5 = 4 km. 2 + 4 = <b>6 km</b>. "
                    "(6.5 km makes 9 jumps. 4.5 km forgets the 2 km he started with.)", km))
    # Kai saves: table
    kv = [30 + 8 * w for w in range(1, 5)]
    its.append(nmcq(tv([1, 2, 3, 4], kv, ("Weeks", "Savings ($)"), "table of values savings") +
                    "Kai saves the same amount each week. The table shows his savings. How much will he have after 10 weeks?",
                    30 + 8 * 10, [70, 80, 380],
                    "His savings go up by $8 each week. Week 1 is $38, so he started with 38 − 8 = $30. "
                    "8 × 10 + 30 = <b>$110</b>. ($70 is week 5 only. $80 forgets the $30.)", dol))
    its.append(emcq(tv([1, 2, 3, 4], kv, ("Weeks", "Savings ($)"), "table of values savings") +
                    "Which expression gives Kai’s savings, in dollars, after <i>w</i> weeks?", "8w + 30",
                    ["30w + 8", "8w + 38", "38w"],
                    "Each week adds $8, so start with %s. 8 × 1 = 8, but week 1 shows $38, so add 30: <b>%s</b>. "
                    "(%s uses the first value as the number added.)" % (X("8w"), X("8w + 30"), X("8w + 38")),
                    [1, 2, 3, 4], kv))
    # hiking
    assert 300 + 150 * Fr(7, 2) == 825
    its.append(nmcq("Hana starts a hike at 300 m above sea level. She climbs 150 m each hour. How high is she after "
                    "3.5 hours?", 825, [1575, 525, 750],
                    "Multiply first: 150 × 3.5 = 525. Then 300 + 525 = <b>825 m</b>. "
                    "(1575 m adds first: (300 + 150) × 3.5. 525 m forgets the 300 m start.)", lambda v: "%s m" % n(v)))
    # picnic tables
    assert 2 * 14 + 2 == 30
    its.append(nmcq("At a school field day, square picnic tables are pushed together in a row. 1 table seats 4 students, "
                    "2 tables seat 6, and 3 tables seat 8. How many tables are needed to seat 30 students?", 14,
                    [15, 16, 8],
                    "Each table adds 2 seats, so the rule is %s. Work backwards: 30 − 2 = 28, and 28 ÷ 2 = <b>14 tables</b>. "
                    "Check: 2 × 14 + 2 = 30. (15 is 30 ÷ 2 and forgets the 2 end seats.)" % X("2n + 2"),
                    lambda v: "%s tables" % n(v)))
    # food bank cans
    assert 85 + 24 * 6 == 229
    its.append(nmcq("Ava’s class has collected 85 cans for the food bank. They collect 24 more cans each week. "
                    "How many cans will they have after 6 more weeks?", 229, [144, 654, 205],
                    "24 × 6 = 144 new cans. 85 + 144 = <b>229 cans</b>. "
                    "(144 forgets the 85 cans they had. 654 adds first: (85 + 24) × 6.)", lambda v: "%s cans" % n(v)))
    # tablet battery
    assert 100 - 8 * 8 == 36
    its.append(nmcq("Liam’s tablet is fully charged at 100%. It drops 8% each hour while he watches videos. "
                    "After how many hours is it at 36%?", 8, [Fr(9, 2), Fr(25, 2), 64],
                    "It needs to drop 100 − 36 = 64%. 64 ÷ 8 = <b>8 hours</b>. Check: 100 − 8 × 8 = 36. "
                    "(4.5 hours is 36 ÷ 8, but 36% is what is left, not what was used.)", hrs))
    # ski lessons graph
    sk = [(i, 20 + 25 * i) for i in range(1, 5)]
    gs = graph_svg(sk, 6, 140, ystep=10, ylab=20, xname="Number of lessons", yname="Cost ($)", vals=True, ypre="$",
                   label="graph of the cost of ski lessons")
    its.append(nmcq(fig(gs) + "The graph shows the cost of ski lessons at a mountain near Kamloops. "
                    "How much does each extra lesson add?", 25, [45, 20, 70],
                    "The cost goes $45, $70, $95, $120. Each lesson adds 70 − 45 = <b>$25</b>. "
                    "$45 is the cost of 1 lesson, which includes a $20 fee paid once.", dol))
    its.append(emcq(fig(gs) + "Which expression gives the cost, in dollars, of <i>n</i> ski lessons?", "25n + 20",
                    ["45n", "25n + 45", "20n + 25"],
                    "Each lesson adds $25, so start with %s. 25 × 1 = 25, but 1 lesson costs $45, so add 20: <b>%s</b>. "
                    "(%s works for 1 lesson only.)" % (X("25n"), X("25n + 20"), X("45n")), [1, 2, 3, 4], [45, 70, 95, 120]))
    # water jug graph
    wj = [(i, 20 - 2 * i) for i in range(1, 5)]
    gw = graph_svg(wj, 6, 20, ystep=2, ylab=4, xname="Games played", yname="Water left (L)", vals=True,
                   label="graph of water left in a jug")
    assert 20 - 2 * 10 == 0
    its.append(mcq(fig(gw) + "At a soccer tournament in Surrey, the team’s water jug loses the same amount each game. "
                   "The pattern continues. After which game is the jug empty?", "Game 10", ["Game 9", "Game 18", "Game 20"],
                   "The water goes 18, 16, 14, 12 L, so it drops 2 L each game. The jug started with 18 + 2 = 20 L. "
                   "20 ÷ 2 = 10, so it is empty after <b>Game 10</b>. (Game 9 still has 2 L. 18 is the litres after Game 1.)"))
    # snack bar on a ferry
    assert (240 - 90) // 15 == 10
    its.append(nmcq("The snack bar on a BC Ferries ship starts the day with 240 cinnamon buns. It sells 15 buns each hour. "
                    "After how many hours are 90 buns left?", 10, [6, 16, 150],
                    "It needs to sell 240 − 90 = 150 buns. 150 ÷ 15 = <b>10 hours</b>. Check: 240 − 15 × 10 = 90. "
                    "(6 hours is 90 ÷ 15, but 90 is the number left, not sold.)", hrs))
    # ferry distance
    assert 54 - 30 * Fr(3, 2) == 9
    its.append(nmcq("A ferry is 54 km from Nanaimo. It sails toward Nanaimo at 30 km each hour. How far from Nanaimo is it "
                    "after 1.5 hours?", 9, [45, 99, 24],
                    "30 × 1.5 = 45 km sailed. 54 − 45 = <b>9 km</b> left. "
                    "(45 km is how far it sailed. 99 km adds instead of subtracting. 24 km is after 1 hour only.)", km))
    # cherries
    assert Fr(9, 2) * 3 + 2 == Fr(31, 2)
    its.append(nmcq("At a fruit stand in the Okanagan, cherries cost $4.50 for each kilogram plus $2 for a basket. "
                    "How much do 3 kg of cherries in one basket cost?", Fr(31, 2), [Fr(39, 2), Fr(27, 2), 11],
                    "4.50 × 3 = 13.50. Then $13.50 + $2.00 = <b>$15.50</b>. "
                    "($19.50 pays for a basket with every kilogram. $13.50 forgets the basket.)", money))
    # two patterns
    assert 60 - 5 * 3 == 15 + 10 * 3
    its.append(nmcq("Zara has $60 and spends $5 each week. Nadia has $15 and saves $10 each week. "
                    "After how many weeks will they have the same amount?", 3, [9, Fr(9, 2), 45],
                    "Make a table. Zara: $55, $50, $45. Nadia: $25, $35, $45. After <b>3 weeks</b> both have $45. "
                    "(45 is the amount, not the number of weeks.)", lambda v: "%s weeks" % n(v)))
    # hockey camp
    assert 60 + 30 * 7 == 270
    its.append(nmcq("A hockey camp in Prince George costs $60 to register plus $30 for each day. Simran’s family pays $270. "
                    "How many days is she at camp?", 7, [9, 11, 8],
                    "Take away the $60 first: 270 − 60 = 210. Then 210 ÷ 30 = <b>7 days</b>. Check: 30 × 7 + 60 = 270. "
                    "(9 days forgets the $60. 11 days adds the $60 instead of subtracting.)", lambda v: "%s days" % n(v)))
    order = [0, 1, 3, 4, 5, 6, 7, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Pattern word problems", "items": [its[i] for i in order]}


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
        "<h2>Patterns are functional relationships</h2>"
        "<p>In a pattern, each <b>term number</b> (input) gives exactly one <b>term value</b> (output). "
        "An <b>increasing</b> pattern goes up by the same amount each time. A <b>decreasing</b> pattern goes down. "
        "You can show a pattern three ways: a <b>table</b>, an <b>expression</b> and a <b>graph</b>.</p>"
        "<figure class='sn-fig'>" + pattern_svg("tri") +
        "<figcaption>3, 5, 7 sticks: each new triangle adds 2 sticks, because it shares a side.</figcaption></figure>"
        + table(["Term number (<i>n</i>)", "1", "2", "3", "4"], [["Number of sticks", "3", "5", "7", "9"]]) +
        "<h2>Write an expression</h2>"
        "<p>The amount the value goes up each time is the number in front of <i>n</i>. Then check term 1 and fix the start.</p>"
        + ex("Expression for 3, 5, 7, 9", "Write an expression for the number of sticks in Figure <i>n</i>.",
             "The value goes up by 2, so start with 2<i>n</i>. For Figure 1, 2 × 1 = 2, but there are 3 sticks. Add 1.",
             X("2n + 1"))
        + ex("Use the expression", "How many sticks are in Figure 15?",
             "Replace <i>n</i> with 15. Multiply first: 2 × 15 = 30. Then 30 + 1 = 31.", "31 sticks") +
        "<h2>Graph the pattern</h2>"
        "<p>Each column of the table is a point (term number, term value). Go <b>across</b> for the term number first, "
        "then <b>up</b> for the term value. The points of an increasing pattern line up and go up to the right.</p>"
        "<figure class='sn-fig'>" + graph_svg([(1, 3), (2, 5), (3, 7), (4, 9)], 5, 12, ylab=2, xname=GX, yname=GY,
                                               vals=True, label="graph of the pattern 3, 5, 7, 9") +
        "<figcaption>The points (1, 3), (2, 5), (3, 7), (4, 9). Each step right goes up 2.</figcaption></figure>"
        "<h2>Decreasing patterns</h2>"
        "<p>When the value goes down by the same amount, subtract that amount times <i>n</i> from a starting number.</p>"
        + ex("Decreasing pattern", "Find an expression for 26, 22, 18, 14, …",
             "It goes down by 4, so the expression has − 4<i>n</i>. Term 1 is 26, so start one jump higher: 26 + 4 = 30. "
             "Check term 4: 30 − 4 × 4 = 14.", X("30 − 4n"))
        + "<figure class='sn-fig'>" + graph_svg([(1, 26), (2, 22), (3, 18), (4, 14)], 5, 28, ystep=2, ylab=4, xname=GX,
                                                 yname=GY, vals=True, label="graph of the pattern 26, 22, 18, 14") +
        "<figcaption>The points of a decreasing pattern go down to the right: 4 down for each step right.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using only the first step: “1 → 5, so add 4”", "Test the rule on every pair in the table"],
            ["Writing “add 2 each time” as <i>n</i> + 2", "The change multiplies <i>n</i>: 2<i>n</i>, then fix the start"],
            ["Using the first value as the number added: 2<i>n</i> + 3 for 3, 5, 7", "Compare 2 × 1 with 3: add 1, so 2<i>n</i> + 1"],
            ["Plotting (term value, term number)", "Across for the term number first, then up for the term value"],
            ["Term 10 = term 1 + 10 jumps", "From term 1 to term 10 there are 9 jumps"],
            ["Adding in a decreasing pattern", "Check the direction: 50, 46, 42 goes down, so subtract"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about patterns in BC math?",
     "a": "In the BC curriculum, Grade 6 students study increasing and decreasing patterns as functional relationships. They show them with tables of values, expressions like 2n + 3 and graphs in the first quadrant."},
    {"q": "What is an input/output table?",
     "a": "It is a table where each input goes through the same rule to make an output. For the rule multiply by 2, then add 3, the input 4 gives the output 11."},
    {"q": "How do you graph a pattern from a table of values?",
     "a": "Make each column a point (term number, term value), go across first, then up. For 5, 7, 9 the points are (1, 5), (2, 7) and (3, 9)."},
    {"q": "How do you write an expression for a decreasing pattern?",
     "a": "Find how much it goes down each time and subtract that times n from a starting number one jump above term 1. For 26, 22, 18, 14 the expression is 30 − 4n."},
]


def gen():
    rnd = random.Random(56809)
    sets = [set_tables(), set_expressions(), set_graphs(), set_decreasing(), set_words()]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"]
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            assert it["q"] not in allk, it["q"]
            allk.add(it["q"])
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "patterns-tables-and-graphs",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Patterns, Tables and Graphs: Increasing and Decreasing Patterns",
        "seo_title": "Grade 6 Patterns Worksheets: Tables of Values, Expressions and Graphs (BC Math, Free)",
        "short_title": "Patterns, tables and graphs",
        "domain": "Patterning",
        "standard_code": "Grade 6: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Increasing and decreasing patterns, using expressions, tables, and graphs as functional relationships",
        "meta_desc": "Free Grade 6 math worksheets on increasing and decreasing patterns: complete tables of values and input/output tables, write expressions like 2n + 3, graph patterns in the first quadrant, and solve BC word problems. 100 questions with an answer key, matched to the BC curriculum.",
        "key_big": "A pattern that changes by the same amount each time has an expression like 2n + 3, and its points line up on a graph.",
        "key_sub": "The change is the number in front of n. Check term 1 to fix the start: 5, 7, 9, 11 is 2n + 3, and 26, 22, 18 is 30 − 4n. Test the rule on every pair, and plot (term number, term value): across first, then up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(graph|four graphs|shape pattern|table of values|input output table)")


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
