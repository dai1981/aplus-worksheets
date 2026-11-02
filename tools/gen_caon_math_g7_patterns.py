# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Linear growing patterns (Ontario Curriculum 2020, Algebra C1.1, C1.2, C1.3)
  python3 tools/gen_caon_math_g7_patterns.py
Constant rate and initial value, tables of values (extend, find missing terms, predict), the expression and
equation for the nth term (t = 3n + 2), graphs of linear patterns, solving for an unknown term number,
and word problems (taxi fares, saving for skates, canoe rentals, maple sap, Terry Fox Run pledges).
Wrong answers come from real mistakes: a rule from the first step only, mixing up the term number and the
term value, the first term used as the initial value, "add 3" written as n + 3, skipped term numbers,
plotting (value, term number), undoing operations in the wrong order, and off-by-one jumps.
Every answer is computed and checked in code (fractions.Fraction). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
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
NB = " "


# ------------------------------------------------------------ numbers
def n(v):
    """Ontario/SI style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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

def eqmcq(q, right, wrong, e, ns, vals, lhs="t", var="n"):
    """Equation choices 't = 3n + 2'. Checked like emcq on the right-hand sides."""
    for k, v in zip(ns, vals):
        assert ev(right, k) == Fr(v), (right, k, v)
    sig = lambda s: tuple(ev(s, k) for k in range(-3, 8))
    sigs = {sig(right)}
    for w in wrong:
        assert any(ev(w, k) != Fr(v) for k, v in zip(ns, vals)), (w, ns, vals)
        assert sig(w) not in sigs, w
        sigs.add(sig(w))
    f = lambda s: X(lhs + " = " + s)
    return mcq(q, f(right), [f(w) for w in wrong], e)


TV = ("Term number", "Term value")


def tt(ns, vals, heads=TV, label="table of values: term number and term value"):
    return tbl(ns, vals, heads, label)


N4 = [1, 2, 3, 4]


def units(u):
    return lambda v: "%s %s" % (n(v), u)


# ============================================================ set 1: constant rate and initial value
def set_rate():
    its = []
    its.append(nmcq(tt(N4, [5, 8, 11, 14]) + "What is the constant rate of this pattern?", 3, [5, 2, 1],
                    "The term value goes up by the same amount each time: 8 − 5 = 3 and 11 − 8 = 3. "
                    "The constant rate is <b>3</b>. 5 is the value of term 1, and 2 is the initial value."))
    its.append(nmcq(tt(N4, [5, 8, 11, 14]) + "What is the initial value of this pattern (the term value for term number 0)?",
                    2, [5, 3, 0],
                    "The pattern goes up by 3, so go back one step from term 1: 5 − 3 = <b>2</b>. "
                    "5 is the value of term 1, not term 0. 3 is the constant rate."))
    its.append(nmcq(tt(N4, [7, 11, 15, 19]) + "What is the initial value of this pattern?", 3, [7, 4, 11],
                    "The constant rate is 4. Going back from term 1 to term 0 subtracts 4: 7 − 4 = <b>3</b>. "
                    "7 is the first term, not the initial value. 4 is the constant rate."))
    its.append(nmcq(fig(pattern_svg("sq")) + "Each new figure adds the same number of sticks. What is the constant rate?",
                    3, [4, 1, 7],
                    "Count: 4, 7, 10 sticks. Each figure adds <b>3</b> sticks. "
                    "4 counts all the sticks of one square, but each new square shares a side with the one before."))
    its.append(nmcq(fig(pattern_svg("sq")) + "Imagine Figure 0. How many sticks would it have? (This is the initial value.)",
                    1, [4, 3, 0],
                    "Figure 1 has 4 sticks and each figure adds 3. Going back one figure: 4 − 3 = <b>1</b>. "
                    "4 is Figure 1. 0 guesses that Figure 0 must be empty."))
    its.append(mcq(tt(N4, [40, 36, 32, 28]) + "How does this pattern change?", "It goes down by 4 each term",
                   ["It goes up by 4 each term", "It goes down by 40 each term", "It goes down by 4 every 2 terms"],
                   "40 − 36 = 4, 36 − 32 = 4, 32 − 28 = 4. It is a shrinking pattern: <b>it goes down by 4 each term</b>."))
    its.append(nmcq(tt(N4, [40, 36, 32, 28]) + "What is the initial value of this pattern?", 44, [40, 36, 4],
                    "The pattern goes down by 4, so going back one step <b>adds</b> 4: 40 + 4 = <b>44</b>. "
                    "36 subtracts 4 again, but that is term 2. 40 is term 1."))
    its.append(mcq("A linear growing pattern has an initial value of 6 and a constant rate of 5. "
                   "What are the values of terms 1, 2 and 3?", "11, 16, 21", ["6, 11, 16", "5, 10, 15", "5, 11, 17"],
                   "The initial value is term 0. Term 1 = 6 + 5 = 11, then add 5 each time: <b>11, 16, 21</b>. "
                   "6, 11, 16 starts at term 0. 5, 10, 15 forgets the initial value."))
    its.append(mcq("For term numbers 1, 2, 3, 4, which list of term values has a constant rate?", "4, 9, 14, 19",
                   ["1, 4, 9, 16", "3, 6, 12, 24", "2, 5, 9, 14"],
                   "4, 9, 14, 19 goes up by 5 every time, so the rate is constant: <b>4, 9, 14, 19</b>. "
                   "1, 4, 9, 16 goes up by 3, 5, 7. 2, 5, 9, 14 goes up by 3, 4, 5. 3, 6, 12, 24 doubles."))
    its.append(mcq(tt(N4, [3, 5, 9, 15]) + "Hana says this pattern has a constant rate of 2, because 5 − 3 = 2. Is she right?",
                   "No, the steps are 2, 4, 6, so the rate is not constant",
                   ["Yes, the first step is 2", "No, the constant rate is 3", "No, the constant rate is 4"],
                   "Check every step, not only the first: 5 − 3 = 2, 9 − 5 = 4, 15 − 9 = 6. "
                   "<b>The steps change, so this pattern has no constant rate.</b> It is not linear."))
    its.append(nmcq(tt([2, 4, 6, 8], [11, 17, 23, 29]) + "What is the constant rate of this pattern (the change for each 1 term)?",
                    3, [6, 11, 5],
                    "The term numbers go up by 2 and the term values go up by 6. For each 1 term the value goes up by "
                    "6 ÷ 2 = <b>3</b>. 6 forgets that the term numbers skip. 5 is the initial value."))
    assert 13 - 2 * 4 == 5
    its.append(nmcq(tt([2, 5, 8, 11], [13, 25, 37, 49]) + "What is the initial value of this pattern?", 5, [13, 9, 1],
                    "The term numbers go up by 3 and the values go up by 12, so the constant rate is 12 ÷ 3 = 4. "
                    "Term 2 is 13, so go back 2 steps: 13 − 2 × 4 = <b>5</b>. 9 goes back only one step. "
                    "1 subtracts the jump of 12 in the table."))
    its.append(mcq("Pattern A has the rule %s. Pattern B has the rule %s. Which pattern grows faster?" % (X("4n + 10"), X("6n + 2")),
                   "Pattern B, because its constant rate is 6",
                   ["Pattern A, because its initial value is 10", "They grow at the same rate",
                    "Pattern A, because 10 is greater than 6"],
                   "How fast a pattern grows depends on the constant rate, the number multiplied by <i>n</i>. "
                   "B adds 6 each term and A adds 4, so <b>Pattern B grows faster</b>. "
                   "A has the greater initial value, but that only tells where it starts."))
    its.append(mcq("Pattern C: 3, 8, 13, 18, … Pattern D: 9, 11, 13, 15, … (both start at term 1). Which statement is true?",
                   "C has the greater constant rate, D has the greater initial value",
                   ["C has the greater constant rate and initial value", "D has the greater constant rate",
                    "They have the same constant rate"],
                   "C goes up by 5, so its initial value is 3 − 5 = −2. D goes up by 2, so its initial value is 9 − 2 = 7. "
                   "<b>C has the greater constant rate, D has the greater initial value.</b> Both reach 13 at term 3, "
                   "but that does not make their rates the same."))
    its.append(nmcq(tt(N4, [Fr(5, 2), Fr(13, 4), 4, Fr(19, 4)]) + "What is the constant rate of this pattern?",
                    Fr(3, 4), [Fr(1, 4), Fr(7, 4), Fr(5, 2)],
                    "3.25 − 2.5 = 0.75 and 4 − 3.25 = 0.75. The constant rate is <b>0.75</b>. "
                    "0.25 compares 3.25 with 3. 1.75 is the initial value."))
    its.append(nmcq(tt(N4, [-7, -4, -1, 2]) + "What is the initial value of this pattern?", -10, [-4, -7, 10],
                    "From −7 to −4 is +3, so the constant rate is 3. Going back one step: −7 − 3 = <b>−10</b>. "
                    "−4 adds 3, which goes forward to term 2. 10 drops the negative sign."))
    its.append(mcq(tt([0, 1, 2, 3], [20, 25, 30, 35], ("Minutes", "Depth (cm)"), "table of values minutes and depth") +
                   "Arjun fills a fish tank with a hose. What does the initial value, 20, tell you?",
                   "The tank had 20 cm of water before he started",
                   ["The water rises 20 cm each minute", "It takes 20 minutes to fill the tank", "The tank holds 20 L"],
                   "The initial value is the value at 0 minutes, before the hose adds any water. "
                   "<b>The tank already had 20 cm of water.</b> The constant rate is 5 cm per minute."))
    its.append(mcq("A climbing gym charges a $15 membership fee plus $8 for each visit. "
                   "For the total cost, what are the constant rate and the initial value?",
                   "Rate $8 per visit, initial value $15",
                   ["Rate $15 per visit, initial value $8", "Rate $23 per visit, initial value $0",
                    "Rate $8 per visit, initial value $23"],
                   "The cost goes up by $8 for every visit: that is the constant rate. The $15 fee is paid once, even "
                   "with 0 visits: that is the initial value. <b>Rate $8 per visit, initial value $15.</b>"))
    its.append(mcq("What are the constant rate and the initial value of the pattern %s?" % X("7n - 4"),
                   "Constant rate 7, initial value −4",
                   ["Constant rate −4, initial value 7", "Constant rate 7, initial value 3", "Constant rate 7, initial value 4"],
                   "The number multiplied by <i>n</i> is the constant rate: 7. When <i>n</i> = 0, 7 × 0 − 4 = −4, "
                   "so the initial value is −4. <b>Constant rate 7, initial value −4.</b> 3 is term 1, not term 0."))
    its.append(mcq("At the start of March Break there is 60 cm of snow on the ground. It melts 4 cm each day. "
                   "Which list shows the snow depth, in centimetres, after days 1, 2, 3 and 4?",
                   "56, 52, 48, 44", ["60, 56, 52, 48", "64, 68, 72, 76", "56, 48, 40, 32"],
                   "The initial value is 60 (day 0). Each day subtract 4: <b>56, 52, 48, 44</b>. "
                   "60, 56, 52, 48 starts at day 0. 64, 68, … adds snow instead of melting it."))
    assert len(its) == 20
    return {"title": "Constant rate and initial value", "items": its}


# ============================================================ set 2: tables of values
def set_tables():
    its = []
    v = [cnt("L", k) for k in range(1, 6)]
    its.append(nmcq(fig(pattern_svg("L")) + "The pattern continues. How many tiles will Figure 5 have?", v[4], [7, 10, 25],
                    "Count: 1, 3, 5. Each figure adds 2 tiles: Figure 4 has 7 and Figure 5 has <b>9</b>. "
                    "7 is Figure 4. 10 is 5 × 2 and forgets that Figure 1 has only 1 tile."))
    its.append(nmcq(tbl([1, 2, 3, 4, 5], [6, 11, "?", 21, 26], TV) + "What term value is missing from the table?", 16, [3, 12, 31],
                    "The values go up by 5: 11 + 5 = <b>16</b>. Check: 16 + 5 = 21. "
                    "3 is the term number, not the term value. 31 is the next term after 26."))
    its.append(nmcq(tt(N4, [4, 10, 16, 22]) + "The pattern continues. What is the value of term 6?", 34, [28, 40, 36],
                    "Add 6 each time: term 5 is 28 and term 6 is <b>34</b>. 28 is term 5. "
                    "40 makes 6 jumps from term 1, but from term 1 to term 6 there are only 5 jumps."))
    its.append(nmcq(tt([1, 2, 3, 6], [5, 9, 13, "?"]) + "The pattern continues in the same way. What is the missing term value?",
                    25, [17, 21, 29],
                    "The values go up by 4 each term. The term number jumps from 3 to 6, which is 3 terms: "
                    "13 + 3 × 4 = <b>25</b>. 17 adds 4 only once. 21 is term 5 and 29 is term 7."))
    v = [cnt("towers", k) for k in (1, 2, 3)]
    its.append(nmcq(fig(pattern_svg("towers", hide=2)) + "Figure 2 is hidden. The pattern grows at a constant rate. "
                    "How many cubes are in Figure 2?", v[1], [8, 18, 10],
                    "Figure 1 has 6 cubes and Figure 3 has 12. From Figure 1 to Figure 3 is 2 equal steps of 3: "
                    "6, <b>9</b>, 12. 18 adds Figures 1 and 3."))
    assert [7 + 6 * k for k in range(5)] == [7, 13, 19, 25, 31]
    its.append(nmcq(tbl([1, 2, 3, 4, 5], [7, 13, 19, 26, 31], TV) + "One term value in this table is wrong. Which one?",
                    26, [13, 19, 31],
                    "The pattern goes up by 6: 7, 13, 19, 25, 31. <b>26</b> should be 25."))
    its.append(nmcq(tt(N4, [50, 46, 42, 38]) + "The pattern continues. What is the value of term 7?", 26, [30, 22, 43],
                    "Subtract 4 each time: 38, 34, 30, <b>26</b>. 30 is term 6 and 22 is term 8. 43 subtracts 7, the term number."))
    vals = [3 * k + 4 for k in N4]
    its.append(mcq("Which list gives the term values of %s for term numbers 1, 2, 3 and 4?" % X("3n + 4"), lst(vals),
                   ["4, 7, 10, 13", "7, 11, 15, 19", "3, 6, 9, 12"],
                   "3 × 1 + 4 = 7, 3 × 2 + 4 = 10, 3 × 3 + 4 = 13, 3 × 4 + 4 = 16: <b>%s</b>. "
                   "4, 7, 10, 13 starts at term 0. 7, 11, 15, 19 mixes up the 3 and the 4." % lst(vals)))
    its.append(nmcq(tt([0, 1, 2, 3], ["?", 9, 14, 19]) + "What is the missing value for term number 0?", 4, [5, 0, 24],
                    "The values go up by 5, so go back one step from term 1: 9 − 5 = <b>4</b>. "
                    "This is the initial value. 0 thinks term 0 must have value 0. 5 is the constant rate."))
    assert 2 * 19 + 2 == 40
    its.append(mcq(fig(pattern_svg("tables")) + "The pattern continues. Which figure has 40 chairs?", "Figure 19",
                   ["Figure 40", "Figure 20", "Figure 21"],
                   "The rule is 2<i>n</i> + 2 (4, 6, 8 chairs). Solve 2<i>n</i> + 2 = 40: 40 − 2 = 38, 38 ÷ 2 = 19. "
                   "<b>Figure 19</b>. Figure 20 divides 40 by 2 and forgets the 2 end chairs. 40 is the number of chairs."))
    its.append(nmcq(tt(N4, [4, 7, 10, 13]) + "The pattern continues. What is the value of term 25?", 76, [79, 100, 75],
                    "The rule is 3<i>n</i> + 1, so term 25 is 3 × 25 + 1 = <b>76</b>. "
                    "79 adds 25 jumps to term 1, but there are only 24 jumps. 100 is 25 × 4."))
    its.append(nmcq(tt(N4, [Fr(6, 5), Fr(9, 5), "?", 3]) + "What term value is missing from the table?", Fr(12, 5),
                    [Fr(18, 5), 2, Fr(11, 5)],
                    "1.8 − 1.2 = 0.6, so add 0.6: 1.8 + 0.6 = <b>2.4</b>. Check: 2.4 + 0.6 = 3. "
                    "3.6 doubles 1.8, but the pattern adds, it does not multiply."))
    its.append(nmcq(tbl([1, 2, 3, 4, 5], [-8, -5, -2, "?", 4], TV) + "What term value is missing from the table?", 1, [-5, -1, 2],
                    "From −8 to −5 is +3, so the values go up by 3: −2 + 3 = <b>1</b>. Check: 1 + 3 = 4. "
                    "−5 subtracts 3 instead of adding."))
    its.append(nmcq(tt(N4, [2, 5, 10, 17]) + "Kai says the next term is 20 because the first step is +3. "
                    "The steps keep changing in the same way. What is term 5?", 26, [20, 24, 22],
                    "The steps are +3, +5, +7, so the next step is +9: 17 + 9 = <b>26</b>. "
                    "This pattern has no constant rate, so it is not linear. 20 uses the first step only. 24 repeats +7."))
    its.append(mcq(fig(pattern_svg("sq")) + "Maya predicts that Figure 10 has 40 sticks. Is she right?",
                   "No, it has 31: 3 × 10 + 1", ["Yes, 4 sticks for each of 10 squares", "No, it has 34: 4 + 3 × 10",
                                                  "No, it has 30: 3 × 10"],
                   "Each square after the first shares a stick, so the rule is 3<i>n</i> + 1. "
                   "3 × 10 + 1 = 31. <b>No, it has 31.</b> 34 makes 10 jumps from Figure 1 instead of 9."))
    assert 3 * 40 + 5 == 125
    its.append(nmcq(tt([10, 20, 30], [35, 65, 95]) + "The pattern continues. What is the value of term 40?", 125, [98, 105, 120],
                    "The term numbers go up by 10 and the values by 30, so each term adds 3. Term 40 is 10 terms after term 30: "
                    "95 + 30 = <b>125</b>. 98 adds 3 only once. 105 adds 10. 120 is 3 × 40 and forgets the + 5."))
    core = ["red", "blue", "blue", "green", "yellow"]
    assert core[(34 - 1) % 5] == "green"
    its.append(mcq("A bead bracelet repeats the colours red, blue, blue, green, yellow. What colour is the 34th bead?",
                   "green", ["yellow", "red", "blue"],
                   "The core has 5 beads. 34 = 6 × 5 + 4, so after 6 full cores, count 4 more beads: red, blue, blue, "
                   "<b>green</b>. Yellow is bead 30, the end of the 6th core."))
    its.append(nmcq(tt(N4, [72, "?", 58, 51]) + "What term value is missing from the table?", 65, [79, 44, 62],
                    "From 58 to 51 is −7, so the pattern goes down by 7: 72 − 7 = <b>65</b>. Check: 65 − 7 = 58. "
                    "79 goes up instead of down. 44 is the next term after 51."))
    its.append(nmcq(tt(N4, [Fr(3, 2), Fr(9, 4), 3, Fr(15, 4)]) + "The pattern continues. What is the value of term 8?",
                    Fr(27, 4), [Fr(15, 2), 6, Fr(9, 2)],
                    "The constant rate is 0.75. From term 1 to term 8 there are 7 jumps: 1.5 + 7 × 0.75 = 1.5 + 5.25 = <b>6.75</b>. "
                    "7.5 doubles term 4. 6 is 8 × 0.75 and forgets the initial value."))
    its.append(nmcq(tt(N4, [10, 7, 4, 1]) + "The pattern continues. What is the value of term 8?", -11, [-14, -8, 11],
                    "Subtract 3 each time: 1, −2, −5, −8, <b>−11</b>. −8 is term 7. "
                    "−14 makes 8 jumps from term 1. 11 drops the negative sign."))
    assert len(its) == 20
    return {"title": "Tables of values: extend and find missing terms", "items": its}


# ============================================================ set 3: expression for the nth term
def set_rule():
    its = []

    def from_table(vals, right, wrong, e, ns=N4):
        return emcq(tt(ns, vals) + "Which expression gives the term value for term number <i>n</i>?", right, wrong, e, ns, vals)

    its.append(from_table([4, 8, 12, 16], "4n", ["n + 4", "4n + 4", "n + 12"],
                          "Each term value is 4 times the term number: 4 × 1 = 4, 4 × 2 = 8. The expression is <b>%s</b>. "
                          "%s gives 5, 6, 7, 8." % (X("4n"), X("n + 4"))))
    its.append(from_table([5, 8, 11, 14], "3n + 2", ["n + 3", "3n + 5", "5n + 3"],
                          "The constant rate is 3, so start with %s. For term 1, 3 × 1 = 3, but the value is 5, so add 2: "
                          "<b>%s</b>. %s uses the first term as the initial value." % (X("3n"), X("3n + 2"), X("3n + 5"))))
    its.append(from_table([7, 11, 15, 19], "4n + 3", ["n + 4", "4n + 7", "7n + 4"],
                          "The constant rate is 4, so start with %s. 4 × 1 = 4 and the value is 7, so add 3: <b>%s</b>. "
                          "Check: 4 × 4 + 3 = 19." % (X("4n"), X("4n + 3"))))
    its.append(from_table([1, 6, 11, 16], "5n - 4", ["n + 5", "5n + 1", "5n - 1"],
                          "The constant rate is 5, so start with %s. 5 × 1 = 5 but the value is 1, so subtract 4: <b>%s</b>. "
                          "Check: 5 × 4 − 4 = 16." % (X("5n"), X("5n − 4"))))
    its.append(from_table([10, 12, 14, 16], "2n + 8", ["n + 2", "2n + 10", "10n + 2"],
                          "The constant rate is 2, so start with %s. 2 × 1 = 2 and the value is 10, so add 8: <b>%s</b>. "
                          "%s says “add 2 each time” but does not multiply <i>n</i>." % (X("2n"), X("2n + 8"), X("n + 2"))))
    sq = [cnt("sq", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("sq")) + "Which expression gives the number of sticks in Figure <i>n</i>?",
                    "3n + 1", ["4n", "3n + 4", "n + 3"],
                    "Count: 4, 7, 10. The constant rate is 3, so start with %s. 3 × 1 = 3 and Figure 1 has 4, so add 1: "
                    "<b>%s</b>. %s counts 4 sticks for every square, but squares share sticks." % (X("3n"), X("3n + 1"), X("4n")),
                    [1, 2, 3], sq))
    tb = [cnt("tables", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("tables")) + "Which expression gives the number of chairs around <i>n</i> tables in a row?",
                    "2n + 2", ["4n", "2n + 4", "n + 2"],
                    "Count: 4, 6, 8. Each table adds 2 chairs, so start with %s. 2 × 1 = 2 and 1 table has 4 chairs, "
                    "so add 2: <b>%s</b>. %s gives 8 chairs for 2 tables, but there are only 6." % (X("2n"), X("2n + 2"), X("4n")),
                    [1, 2, 3], tb))
    L = [cnt("L", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("L")) + "Which expression gives the number of tiles in Figure <i>n</i>?",
                    "2n - 1", ["n + 2", "2n + 1", "3n - 2"],
                    "Count: 1, 3, 5. The constant rate is 2, so start with %s. 2 × 1 = 2 and Figure 1 has 1, so subtract 1: "
                    "<b>%s</b>. %s works for Figure 1 only: 3 × 2 − 2 = 4, not 3." % (X("2n"), X("2n − 1"), X("3n − 2")),
                    [1, 2, 3], L))
    tw_ = [cnt("towers", k) for k in (1, 2, 3)]
    its.append(emcq(fig(pattern_svg("towers")) + "Which expression gives the number of cubes in Figure <i>n</i>?",
                    "3n + 3", ["n + 3", "3n + 6", "6n"],
                    "Count: 6, 9, 12. Each figure adds 3 cubes, so start with %s. 3 × 1 = 3 and Figure 1 has 6, so add 3: "
                    "<b>%s</b>. %s works for Figure 1 only: 6 × 2 = 12, not 9." % (X("3n"), X("3n + 3"), X("6n")),
                    [1, 2, 3], tw_))
    its.append(emcq("A linear growing pattern has a constant rate of 6 and an initial value of 5. "
                    "Which expression gives the nth term?", "6n + 5", ["5n + 6", "6n + 11", "n + 6"],
                    "The constant rate multiplies <i>n</i> and the initial value is added: <b>%s</b>. "
                    "Check term 0: 6 × 0 + 5 = 5. %s swaps the rate and the initial value." % (X("6n + 5"), X("5n + 6")),
                    [0, 1, 2, 3], [5, 11, 17, 23]))
    its.append(eqmcq(tt(N4, [9, 14, 19, 24]) + "Which equation gives the term value <i>t</i> for term number <i>n</i>?",
                     "5n + 4", ["n + 5", "5n + 9", "9n + 5"],
                     "The constant rate is 5, so start with 5<i>n</i>. 5 × 1 = 5 and term 1 is 9, so add 4: <b>%s</b>. "
                     "Check: 5 × 4 + 4 = 24." % X("t = 5n + 4"), N4, [9, 14, 19, 24]))
    its.append(from_table([6, 13, 20, 27], "7n + 6", ["7n - 1", "n + 7", "6n + 7"],
                          "This table starts at term 0, so 6 is the initial value. The constant rate is 7: <b>%s</b>. "
                          "%s would be right if the table started at term 1." % (X("7n + 6"), X("7n − 1")), ns=[0, 1, 2, 3]))
    its.append(from_table([45, 41, 37, 33], "49 - 4n", ["45 - 4n", "n - 4", "4n + 41"],
                          "The values go down by 4, so the expression subtracts %s. Going back to term 0: 45 + 4 = 49. "
                          "So it is <b>%s</b>. Check: 49 − 4 × 4 = 33. %s gives 41 for term 1."
                          % (X("4n"), X("49 − 4n"), X("45 − 4n"))))
    its.append(from_table([13, 23, 33, 43], "5n + 3", ["10n + 3", "10n - 7", "n + 10"],
                          "The term numbers go up by 2 and the values by 10, so the constant rate is 10 ÷ 2 = 5. "
                          "5 × 2 = 10 and term 2 is 13, so add 3: <b>%s</b>. %s forgets that the term numbers skip."
                          % (X("5n + 3"), X("10n + 3")), ns=[2, 4, 6, 8]))
    its.append(emcq("Figure 1 of a pattern has 8 dots. Each new figure has 5 more dots. "
                    "Which expression gives the number of dots in Figure <i>n</i>?",
                    "5n + 3", ["5n + 8", "8n + 5", "n + 5"],
                    "The constant rate is 5, so start with %s. 5 × 1 = 5 and Figure 1 has 8, so add 3: <b>%s</b>. "
                    "%s gives 13 dots in Figure 1." % (X("5n"), X("5n + 3"), X("5n + 8")), [1, 2, 3], [8, 13, 18]))
    its.append(mcq(fig(pattern_svg("sq")) + "The rule for the number of sticks is %s. What does the 1 tell you?" % X("3n + 1"),
                   "The initial value: Figure 0 would have 1 stick",
                   ["The constant rate", "The number of sticks in Figure 1", "The figure number"],
                   "The number added on its own is the value when <i>n</i> = 0: 3 × 0 + 1 = 1. "
                   "<b>It is the initial value.</b> The 3 is the constant rate, and Figure 1 has 4 sticks."))
    its.append(from_table([Fr(3, 2), 2, Fr(5, 2), 3], "0.5n + 1", ["n + 0.5", "0.5n + 1.5", "1.5n"],
                          "The constant rate is 0.5, so start with %s. 0.5 × 1 = 0.5 and term 1 is 1.5, so add 1: "
                          "<b>%s</b>. %s goes up by 1 each term, not 0.5." % (X("0.5n"), X("0.5n + 1"), X("n + 0.5"))))
    its.append(from_table([-1, 2, 5, 8], "3n - 4", ["n + 3", "3n - 1", "3n + 4"],
                          "The constant rate is 3, so start with %s. 3 × 1 = 3 and term 1 is −1. 3 − 4 = −1, so "
                          "<b>%s</b>. %s gives 2 for term 1." % (X("3n"), X("3n − 4"), X("3n − 1"))))
    its.append(emcq("Term 4 of a linear growing pattern is 22 and term 7 is 37. Which expression gives the nth term?",
                    "5n + 2", ["n + 18", "3n + 10", "6n - 2"],
                    "From term 4 to term 7 is 3 steps, and the value goes up 37 − 22 = 15. The constant rate is 15 ÷ 3 = 5. "
                    "5 × 4 = 20, and 22 − 20 = 2: <b>%s</b>. The other choices give 22 for term 4 but not 37 for term 7."
                    % X("5n + 2"), [4, 7], [22, 37]))
    its.append(emcq(tt(N4, [4, 10, 16, 22]) + "Owen says the rule is %s because 1 + 3 = 4. "
                    "Which expression is right for the whole table?" % X("n + 3"),
                    "6n - 2", ["n + 3", "4n", "6n + 4"],
                    "%s works for term 1 only: 2 + 3 = 5, not 10. The constant rate is 6, so start with %s. "
                    "6 × 1 = 6 and term 1 is 4, so subtract 2: <b>%s</b>." % (X("n + 3"), X("6n"), X("6n − 2")),
                    N4, [4, 10, 16, 22]))
    assert len(its) == 20
    return {"title": "Expressions and equations for the nth term", "items": its}


# ============================================================ set 4: graphs
def set_graphs():
    its = []
    TN, TVL = "Term number", "Term value"
    g1pts = [(k, 2 * k + 1) for k in range(1, 6)]
    g1 = graph_svg(g1pts, 6, 12, xname=TN, yname=TVL, tags={(3, 7): "P"},
                   label="graph of a linear pattern: points (1, 3) to (5, 11)")
    its.append(mcq(fig(g1) + "Point P shows one term of the pattern as (term number, term value). What are its coordinates?",
                   pt(3, 7), [pt(7, 3), pt(3, 6), pt(4, 7)],
                   "Go across first, then up. P is 3 across and 7 up, so it is <b>(3, 7)</b>. "
                   "(7, 3) gives the numbers in the wrong order: the term number comes first."))
    g1b = graph_svg(g1pts, 6, 12, xname=TN, yname=TVL, label="graph of a linear pattern: 5 points")
    its.append(nmcq(fig(g1b) + "What is the value of term 4?", 9, [4, 8, 11],
                    "Find 4 on the term number axis and go up to the point. Read across: <b>9</b>. "
                    "4 is the term number. 11 is term 5."))
    its.append(mcq(tt(N4, [4, 7, 10, 13]) + "Liam graphs this pattern. Which point should he plot for term 3?",
                   pt(3, 10), [pt(10, 3), pt(3, 13), pt(4, 10)],
                   "Each column is one point (term number, term value). Term 3 has value 10, so plot <b>(3, 10)</b>. "
                   "(10, 3) puts the term value first."))
    its.append(mcq(fig(g1b) + "The pattern continues. Which point comes next?", pt(6, 13), [pt(13, 6), pt(6, 12), pt(7, 13)],
                   "The next term number is 6. The values go up by 2, so 11 + 2 = 13. The point is <b>(6, 13)</b>. "
                   "(13, 6) swaps the numbers."))
    its.append(nmcq(fig(g1b) + "What is the constant rate of this pattern?", 2, [1, 3, 5],
                    "Each step right (one more term), the points go up 2: 3, 5, 7, 9, 11. The constant rate is <b>2</b>. "
                    "1 is the step in the term number. 3 is the value of term 1."))
    its.append(emcq(fig(g1b) + "Which expression gives the term value for term number <i>n</i>?", "2n + 1",
                    ["n + 2", "3n", "2n + 3"],
                    "The constant rate is 2, so start with %s. 2 × 1 = 2 and term 1 is 3, so add 1: <b>%s</b>. "
                    "%s works for term 1 only." % (X("2n"), X("2n + 1"), X("3n")), [1, 2, 3, 4, 5], [3, 5, 7, 9, 11]))
    GL = ["Graph A", "Graph B", "Graph C", "Graph D"]
    want = [(k, 3 * k - 1) for k in (1, 2, 3)]
    panels = [[(2, 1), (5, 2), (8, 3)], [(1, 2), (2, 4), (3, 6)], want, [(1, 2), (2, 3), (3, 4)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "A pattern has the term values 2, 5, 8 for terms 1, 2, 3. Which graph shows it?", GL, 2,
                         "The points are (1, 2), (2, 5), (3, 8): <b>Graph C</b>. Graph A plots (term value, term number). "
                         "Graph B goes up by 2 and Graph D goes up by 1, but this pattern goes up by 3."))
    want = [(k, k + 5) for k in (1, 2, 3)]
    panels = [[(1, 5), (2, 6), (3, 7)], want, [(6, 1), (7, 2), (8, 3)], [(1, 6), (2, 5), (3, 4)]]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for terms 1, 2 and 3?" % X("t = n + 5"), GL, 1,
                         "1 + 5 = 6, 2 + 5 = 7, 3 + 5 = 8. The points are (1, 6), (2, 7), (3, 8): <b>Graph B</b>. "
                         "Graph A adds 4. Graph C swaps the numbers. Graph D goes down, but %s grows." % X("n + 5")))
    want = [(k, 9 - 2 * k) for k in (1, 2, 3)]
    panels = [[(1, 7), (2, 6), (3, 5)], [(7, 1), (5, 2), (3, 3)], [(1, 2), (2, 4), (3, 6)], want]
    its.append(mcq_fixed(fig(panels_svg(panels, "four graphs A to D")) +
                         "Which graph shows %s for terms 1, 2 and 3?" % X("t = 9 - 2n"), GL, 3,
                         "9 − 2 = 7, 9 − 4 = 5, 9 − 6 = 3. The points are (1, 7), (2, 5), (3, 3): <b>Graph D</b>. "
                         "Graph A goes down by 1, not 2. Graph B swaps the numbers. Graph C grows instead of shrinking."))
    g4 = graph_svg([(k, 5 * k + 10) for k in range(0, 5)], 5, 35, ystep=5, ylab=5, xname=TN, yname=TVL,
                   label="graph of a linear pattern going up by 5")
    its.append(nmcq(fig(g4) + "What is the initial value of this pattern?", 10, [0, 5, 15],
                    "The initial value is the term value for term 0. The first point is on the vertical axis at 10, "
                    "so the initial value is <b>10</b>. Read the scale: each grid line is 5. 15 is term 1."))
    its.append(nmcq(fig(g4) + "What is the constant rate of this pattern?", 5, [10, 15, 1],
                    "Each step right, the points go up one grid line, and each grid line is 5. The constant rate is <b>5</b>. "
                    "10 is the initial value. 1 counts grid lines without reading the scale."))
    its.append(emcq(fig(g4) + "Which expression gives the term value for term number <i>n</i>?", "5n + 10",
                    ["10n + 5", "5n + 15", "n + 5"],
                    "The initial value is 10 and the constant rate is 5: <b>%s</b>. "
                    "%s uses term 1 as the initial value. %s swaps the rate and the initial value."
                    % (X("5n + 10"), X("5n + 15"), X("10n + 5")), [0, 1, 2, 3, 4], [10, 15, 20, 25, 30]))
    g2 = graph_svg([(k, 12 - 2 * k) for k in range(0, 6)], 6, 12, xname=TN, yname=TVL,
                   label="graph of a shrinking linear pattern")
    its.append(mcq(fig(g2) + "How does the term value change from one term to the next?", "It goes down by 2",
                   ["It goes up by 2", "It goes down by 1", "It goes down by 12"],
                   "The points are (0, 12), (1, 10), (2, 8). Each step right, the value drops 2: <b>it goes down by 2</b>. "
                   "This is a shrinking pattern."))
    its.append(emcq(fig(g2) + "Which expression gives the term value for term number <i>n</i>?", "12 - 2n",
                    ["2n + 12", "12 - n", "10 - 2n"],
                    "The initial value is 12 and the value goes down by 2 each term: <b>%s</b>. "
                    "%s uses term 1 as the start." % (X("12 − 2n"), X("10 − 2n")),
                    [0, 1, 2, 3, 4, 5], [12, 10, 8, 6, 4, 2]))
    sv = [cnt("sq", k) for k in range(1, 5)]
    g3 = graph_svg(list(zip(N4, sv)), 6, 16, ylab=4, xname="Figure number", yname="Number of sticks",
                   label="graph of figure number and number of sticks")
    its.append(mcq(fig(g3) + "This graph shows the stick pattern 4, 7, 10, 13. Why are the points not joined with a line?",
                   "Only whole figure numbers make sense",
                   ["The points are not in a straight line", "A line would go off the graph", "Graphs never join points"],
                   "You can build Figure 1 or Figure 2, but not Figure 1.5. <b>Only whole figure numbers make sense</b>, "
                   "so the points stay separate. They still line up, because the pattern is linear."))
    its.append(mcq(fig(g3) + "The pattern continues. Which point would be on this graph for Figure 10?", pt(10, 31),
                   [pt(31, 10), pt(10, 30), pt(10, 40)],
                   "The rule is %s. For Figure 10: 3 × 10 + 1 = 31, so the point is <b>(10, 31)</b>. "
                   "(31, 10) swaps the numbers. (10, 40) counts 4 sticks for every square." % X("3n + 1")))
    panels = [[(0, 1), (1, 2), (2, 3), (3, 4)], [(0, 5), (1, 6), (2, 7), (3, 8)],
              [(0, 0), (1, 2), (2, 4), (3, 6)], [(0, 1), (1, 4), (2, 7)]]
    pv = panels_svg(panels, "four graphs A to D of linear patterns")
    its.append(mcq_fixed(fig(pv) + "Which graph shows the pattern with the greatest constant rate?", GL, 3,
                         "The constant rate is how far the points go up for each step right. A and B go up 1, C goes up 2, "
                         "and D goes up 3. <b>Graph D</b> is the steepest. Graph B starts highest, but that is its initial value."))
    its.append(mcq_fixed(fig(pv) + "Which graph shows the pattern with the greatest initial value?", GL, 1,
                         "The initial value is where the pattern meets the vertical axis (term 0). Graph B starts at 5, "
                         "the highest: <b>Graph B</b>. Graph D grows fastest, but it starts at 1."))
    good = [(1, 1), (2, 5), (5, 17)]
    assert all(ev("4n - 3", a) == b for a, b in good) and ev("4n - 3", 3) == 9
    its.append(mcq("Which point is <b>not</b> on the graph of %s?" % X("t = 4n − 3"), pt(3, 10), [pt(a, b) for a, b in good],
                   "Test each point. For <i>n</i> = 3: 4 × 3 − 3 = 9, not 10, so <b>(3, 10)</b> is not on the graph. "
                   "(1, 1), (2, 5) and (5, 17) all work."))
    bad = [(1, 3), (2, 5), (3, 8), (4, 9)]
    assert [2 * a + 1 for a, _ in bad] == [3, 5, 7, 9]
    g6 = graph_svg(bad, 6, 12, xname=TN, yname=TVL, label="graph of four points, one plotted wrong")
    its.append(mcq(fig(g6) + "These points should follow %s. One point is plotted wrong. Which one?" % X("t = 2n + 1"),
                   pt(3, 8), [pt(1, 3), pt(2, 5), pt(4, 9)],
                   "For <i>n</i> = 3: 2 × 3 + 1 = 7. The point is at <b>(3, 8)</b>, one too high. The other points fit."))
    assert len(its) == 20
    return {"title": "Graph linear growing patterns", "items": its}


# ============================================================ set 5: solve for the term number, word problems
def set_words():
    its = []
    nn = lambda v: X("n") + " = " + n(v)
    its.append(nmcq("In the pattern %s, which term number has a term value of 47?" % X("3n + 2"), 15, [47, 22, 143],
                    "Solve 3<i>n</i> + 2 = 47. Undo + 2: 47 − 2 = 45. Undo × 3: 45 ÷ 3 = <b>15</b>. Check: 3 × 15 + 2 = 47. "
                    "47 is the term value, not the term number. 143 finds term 47 instead."))
    its.append(nmcq("Solve %s." % X("4n + 1 = 33"), 8, [Fr(17, 2), Fr(29, 4), 133],
                    "Undo + 1: 33 − 1 = 32. Undo × 4: 32 ÷ 4 = 8, so <b>%s</b>. 8.5 adds 1 instead of subtracting. "
                    "7.25 undoes in the wrong order: 33 ÷ 4 − 1. 133 puts 33 in for <i>n</i>." % nn(8), fmt=nn))
    its.append(nmcq("The rule of a pattern is %s. Which term number has a value of 58?" % X("t = 5n - 7"), 13,
                    [Fr(51, 5), 58, 283],
                    "Solve 5<i>n</i> − 7 = 58. Undo − 7: 58 + 7 = 65. Undo × 5: 65 ÷ 5 = <b>13</b>. "
                    "10.2 subtracts 7 instead of adding. 283 finds term 58."))
    assert 6 * 11 + 4 == 70 and 6 * 12 + 4 == 76
    its.append(mcq("Is 75 a term value of the pattern %s?" % X("6n + 4"),
                   "No, the term number would not be a whole number",
                   ["Yes, it is term 11", "Yes, it is term 12", "Yes, it is term 75"],
                   "Solve 6<i>n</i> + 4 = 75: 75 − 4 = 71, and 71 ÷ 6 is not a whole number. Term 11 is 70 and term 12 is 76, "
                   "so 75 is skipped. <b>No.</b>"))
    assert 90 - 6 * 11 == 24
    its.append(nmcq("The rule of a shrinking pattern is %s. Which term number has a value of 24?" % X("t = 90 - 6n"), 11,
                    [24, 66, 19],
                    "Solve 90 − 6<i>n</i> = 24. 90 − 24 = 66, so 6<i>n</i> = 66 and <i>n</i> = <b>11</b>. "
                    "Check: 90 − 66 = 24. 66 forgets to divide by 6. 19 adds 24 to 90 instead of subtracting."))
    assert 4 * 5 + 1 == 2 * 5 + 11 == 21
    its.append(nmcq("Pattern A is %s and pattern B is %s. For which term number do they have the same value?"
                    % (X("4n + 1"), X("2n + 11")), 5, [21, 10, 12],
                    "Make a table. Term 4: 17 and 19. Term 5: 4 × 5 + 1 = 21 and 2 × 5 + 11 = 21. "
                    "They match at term <b>5</b>. 21 is the value, not the term number. 10 is 11 − 1."))
    assert Fr(9, 2) + 2 * 8 == Fr(41, 2)
    its.append(nmcq("A taxi charges $4.50 to start plus $2 for each kilometre. How much does an 8 km ride cost?",
                    Fr(41, 2), [52, 16, 36],
                    "2 × 8 = 16. Then $16.00 + $4.50 = <b>$20.50</b>. $16.00 forgets the $4.50 start. "
                    "$52.00 adds first: (4.50 + 2) × 8. $36.00 charges $4.50 per kilometre.", money))
    assert Fr(9, 2) + 2 * 13 == Fr(61, 2)
    its.append(nmcq("The same taxi charges $4.50 to start plus $2 for each kilometre. A ride costs $30.50. How long was it?",
                    13, [Fr(61, 4), Fr(35, 2), 26],
                    "Take off the start: $30.50 − $4.50 = $26. Each kilometre is $2: 26 ÷ 2 = <b>13 km</b>. "
                    "15.25 km forgets the $4.50. 17.5 km adds the $4.50 instead of subtracting. 26 km forgets to divide by 2.",
                    units("km")))
    sv = [45, 60, 75, 90]
    its.append(eqmcq(tt([0, 1, 2, 3], sv, ("Weeks", "Savings ($)"), "table of values weeks and savings") +
                     "Olivia is saving for new hockey skates. Which equation gives her savings <i>s</i>, in dollars, "
                     "after <i>w</i> weeks?", "15w + 45", ["45w + 15", "15w", "60w"],
                     "The savings go up $15 each week: the constant rate. She had $45 at week 0: the initial value. "
                     "So <b>%s</b>. %s forgets the $45 she started with." % (X("s = 15w + 45"), X("s = 15w")),
                     [0, 1, 2, 3], sv, lhs="s"))
    assert 45 + 15 * 11 == 210
    its.append(nmcq("Olivia has $45 and saves $15 each week. The skates cost $210. After how many weeks can she buy them?",
                    11, [14, 17, 12],
                    "Solve 15<i>w</i> + 45 = 210. She still needs $210 − $45 = $165. 165 ÷ 15 = <b>11 weeks</b>. "
                    "14 weeks forgets the $45 she has. 17 weeks adds the $45 instead of subtracting.", units("weeks")))
    assert 30 * 5 + 20 == 170
    its.append(nmcq("A ski hill near Collingwood rents snowboards for $30 a day plus a $20 helmet fee paid once. "
                    "How much is a 5-day rental?", 170, [250, 150, 180],
                    "30 × 5 = 150. Then 150 + 20 = <b>$170</b>. $250 pays the helmet fee every day: (30 + 20) × 5. "
                    "$150 forgets the helmet fee.", dol))
    assert 20 * 5 == 40 + 12 * 5 == 100
    its.append(mcq("A canoe rental in Algonquin Park has two plans. Plan A: $20 per hour. Plan B: $40 plus $12 per hour. "
                   "For how many hours do both plans cost the same?", "5 hours", ["2 hours", "8 hours", "100 hours"],
                   "Make a table. Plan A: $20, $40, $60, $80, $100. Plan B: $52, $64, $76, $88, $100. "
                   "At <b>5 hours</b> both cost $100. 100 is the cost, not the hours. 8 is 20 − 12."))
    its.append(emcq("A sugar bush in Ontario has 150 L of maple sap in a tank and collects 40 L more each day. "
                    "Which expression gives the litres of sap after <i>d</i> days?", "40d + 150",
                    ["150d + 40", "190d", "40d"],
                    "The constant rate is 40 L per day and the initial value is 150 L: <b>%s</b>. "
                    "%s adds 150 L every day." % (X("40d + 150"), X("150d + 40")), [0, 1, 2], [150, 190, 230]))
    assert 150 + 40 * 15 == 750
    its.append(nmcq("The tank starts with 150 L of sap and collects 40 L each day. It is full at 750 L. "
                    "After how many days is it full?", 15, [Fr(75, 4), Fr(45, 2), 600],
                    "Solve 40<i>d</i> + 150 = 750. 750 − 150 = 600, and 600 ÷ 40 = <b>15 days</b>. "
                    "18.75 days forgets the 150 L already there. 22.5 days adds the 150 L.", units("days")))
    assert 10 + 3 * 8 == 34
    its.append(nmcq("For the Terry Fox Run, Chloe’s uncle pledges $10 plus $3 for each kilometre she runs. "
                    "Chloe runs 8 km. How much does he give?", 34, [104, 24, 21],
                    "3 × 8 = 24. Then 24 + 10 = <b>$34</b>. $104 adds first: (10 + 3) × 8. $24 forgets the $10.", dol))
    assert 12 + Fr(1, 4) * 60 == 27
    its.append(nmcq("An e-bike rental costs $12 plus $0.25 per minute. Ethan’s ride costs $27. How many minutes did he ride?",
                    60, [108, 156, 15],
                    "Solve 0.25<i>m</i> + 12 = 27. 27 − 12 = 15, and 15 ÷ 0.25 = <b>60 minutes</b>. "
                    "108 forgets the $12. 156 adds the $12. 15 forgets to divide by 0.25.", units("minutes")))
    cp = [(h, 10 * h + 15) for h in range(1, 5)]
    g = graph_svg(cp, 6, 60, ystep=5, ylab=10, xname="Hours", yname="Cost ($)", vals=True, ypre="$",
                  label="graph of canoe rental cost and hours")
    its.append(mcq(fig(g) + "The graph shows the cost of renting a canoe. What is the initial value, and what does it mean?",
                   "$15, a fee paid once", ["$25, the cost for 1 hour", "$10, the cost per hour", "$0, nothing to pay at the start"],
                   "The cost goes up $10 each hour. Going back from 1 hour: $25 − $10 = $15. "
                   "<b>$15 is a fee paid once</b>, before any hours. $10 is the constant rate."))
    its.append(nmcq(fig(g) + "The pattern continues. How much does a 7-hour rental cost?", 85, [70, 95, 175],
                    "Cost = 10 × 7 + 15 = <b>$85</b>. $70 forgets the $15 fee. $95 is 8 hours. $175 is 7 × $25.", dol))
    assert 120 - 8 * 5 == 30 + 10 * 5 == 80
    its.append(nmcq("Ava has $120 and spends $8 each week. Nathan has $30 and saves $10 each week. "
                    "After how many weeks will they have the same amount?", 5, [45, 9, 80],
                    "The gap is $120 − $30 = $90. Each week it shrinks by $8 + $10 = $18. 90 ÷ 18 = <b>5 weeks</b>. "
                    "Check: 120 − 40 = 80 and 30 + 50 = 80. 45 divides by 10 − 8, but Ava goes down while Nathan goes up.",
                    units("weeks")))
    assert 300 + 25 * 60 == 1800
    its.append(nmcq("A class books a bus for a field trip for $300, plus $25 per student for tickets. "
                    "The budget is $1800. How many students can go?", 60, [72, 84, 12],
                    "Solve 25<i>s</i> + 300 = 1800. 1800 − 300 = 1500, and 1500 ÷ 25 = <b>60 students</b>. "
                    "72 forgets the bus. 84 adds the bus cost instead of subtracting.", units("students")))
    assert len(its) == 20
    return {"title": "Solve for the term number and word problems", "items": its}


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
        "<p>A <b>linear growing pattern</b> changes by the same amount from one term to the next. "
        "That amount is the <b>constant rate</b>. The <b>initial value</b> is the term value for term number 0: "
        "go back one step from term 1.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>4, 7, 10 sticks. Each figure adds 3, so the constant rate is 3. "
        "Figure 0 would have 4 − 3 = 1 stick, so the initial value is 1.</figcaption></figure>"
        + table(["Term number (<i>n</i>)", "0", "1", "2", "3", "4"], [["Term value", "1", "4", "7", "10", "13"]]) +
        "<h2>The nth term</h2>"
        "<p>The constant rate multiplies <i>n</i>, and the initial value is added. "
        "As an equation: <i>t</i> = 3<i>n</i> + 1, where <i>t</i> is the term value.</p>"
        + ex("Write the rule", "Write the rule for 5, 8, 11, 14, … (term 1 is 5).",
             "The constant rate is 3, so start with 3<i>n</i>. Term 1: 3 × 1 = 3, but the value is 5, so add 2. "
             "Check term 4: 3 × 4 + 2 = 14.", X("t = 3n + 2"))
        + ex("Predict a term", "In the stick pattern, how many sticks are in Figure 20?",
             "Replace <i>n</i> with 20. Multiply first: 3 × 20 = 60. Then 60 + 1 = 61.", "61 sticks")
        + ex("Solve for the term number", "Which figure has 49 sticks?",
             "Solve 3<i>n</i> + 1 = 49. Undo + 1: 49 − 1 = 48. Undo × 3: 48 ÷ 3 = 16. Check: 3 × 16 + 1 = 49.", "Figure 16") +
        "<h2>Graph a linear pattern</h2>"
        "<p>Plot each term as a point (term number, term value): across first, then up. The points lie in a straight line. "
        "The initial value is where the pattern meets the vertical axis, and the constant rate is how far the points go up "
        "for each step right. There is no Figure 1.5, so the points are <b>not joined</b>.</p>"
        "<figure class='sn-fig'>" + graph_svg([(0, 1), (1, 4), (2, 7), (3, 10), (4, 13)], 5, 16, ylab=4,
                                               xname="Figure number", yname="Number of sticks", vals=True,
                                               label="graph of figure number and number of sticks") +
        "<figcaption>Start at the initial value 1, then go up 3 for each step right.</figcaption></figure>"
        + ex("Word problem", "A taxi charges $4.50 to start plus $2 for each kilometre. A ride costs $30.50. How far was it?",
             "The rule is 2<i>k</i> + 4.50. Solve 2<i>k</i> + 4.50 = 30.50: 30.50 − 4.50 = 26, and 26 ÷ 2 = 13.", "13 km") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Finding the rule from the first step only", "Check every step. 3, 5, 9, 15 has steps 2, 4, 6: no constant rate"],
            ["Using term 1 as the initial value: 3<i>n</i> + 5 for 5, 8, 11", "The initial value is term 0: 5 − 3 = 2, so 3<i>n</i> + 2"],
            ["Writing “add 3 each time” as <i>n</i> + 3", "The constant rate multiplies <i>n</i>: 3<i>n</i>"],
            ["Mixing up <i>n</i> and the term value", "<i>n</i> is the position. The rule gives the value at that position"],
            ["Forgetting skipped term numbers", "Divide the change in value by the change in term number"],
            ["Plotting (term value, term number)", "The term number goes across first, then the value goes up"],
        ])
    )


FAQ = [
    {"q": "What are linear growing patterns in Grade 7 math in Ontario?",
     "a": "They are patterns that change by the same amount each term. In the Ontario Grade 7 algebra strand, students describe them by their constant rate and initial value, write a rule such as 3n + 2, graph them and use the rule to find unknown terms."},
    {"q": "What is the difference between the constant rate and the initial value?",
     "a": "The constant rate is how much the pattern changes from one term to the next. The initial value is the term value for term number 0, the starting amount before any change."},
    {"q": "How do you find the nth term of a pattern like 5, 8, 11, 14?",
     "a": "The pattern goes up by 3, so write 3n. Then check term 1: 3 × 1 = 3, but the value is 5, so add 2. The nth term is 3n + 2."},
    {"q": "How do you find which term has a certain value?",
     "a": "Set the rule equal to the value and work backward. For 3n + 2 = 47, subtract 2 to get 45, then divide by 3 to get term number 15."},
]


def gen():
    rnd = random.Random(47812)
    sets = [set_rate(), set_tables(), set_rule(), set_graphs(), set_words()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "linear-growing-patterns",
        "sort": 12, "updated": UPDATED, "pdf_url": "",
        "title": "Linear Growing Patterns: Constant Rate, Initial Value and the nth Term",
        "seo_title": "Grade 7 Linear Growing Patterns Worksheets: Tables, Graphs and nth Term (Ontario Math, Free)",
        "short_title": "Linear growing patterns",
        "domain": "Algebra",
        "standard_code": "Grade 7: C1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating, growing, and shrinking patterns, and use algebraic representations of the pattern rules to solve for unknown values in linear growing patterns",
        "meta_desc": "Free Grade 7 math worksheets on linear growing patterns for the Ontario curriculum: constant rate and initial value, tables of values, rules like 3n + 2 for the nth term, graphs, solving for the term number, and taxi, savings and rental word problems. 100 questions with an answer key.",
        "key_big": "A linear growing pattern has a constant rate and an initial value: the rate multiplies n and the initial value is added.",
        "key_sub": "For 5, 8, 11, 14 the constant rate is 3 and the initial value (term 0) is 5 − 3 = 2, so the rule is t = 3n + 2. To find which term is 47, work backward: (47 − 2) ÷ 3 = 15.",
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
