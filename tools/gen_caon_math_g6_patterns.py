# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Patterns and Expressions (Ontario Mathematics Curriculum 2020, Grade 6: Algebra, C1 and C2.2)
  python3 tools/gen_ca_math_g6_patterns.py
Growing and shrinking patterns in lists, tables of values and tile or craft-stick figures, evaluating expressions
with whole numbers and decimal tenths, finding the pattern rule as an expression (3n + 2), term numbers and term
values, simple graphs of linear patterns, and word problems in Canadian contexts.
Wrong answers come from real student mistakes: using only the first difference, mixing up the term number and the
term value, reading 3n as 3 + n (or as 34 when n = 4), forgetting the constant, using the first term as the
constant (3n + 5 for 5, 8, 11 …), adding before multiplying, multiplying only the whole-number part of a decimal,
swapping the coordinates of a point, and counting n jumps instead of n − 1.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d6cd"
WOOD = "#c08a3e"
HEAD = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """Ontario style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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
                s = NBSP.join(g)
            if k:
                s += "." + str(r).rjust(k, "0")
            return (M if neg else "") + s
    raise ValueError(v)


def money(v, cents=True):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1, v
    if not cents:
        assert v.denominator == 1
        return "$" + n(v)
    w, r = divmod(c.numerator, 100)
    return "$%s.%02d" % (n(w), r)


def plain(s):
    return re.sub(r"<[^>]+>", "", s).replace(NBSP, " ")


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ expressions
def X(s):
    """Plain expression '3n + 2' -> HTML with the letter in italics and the real minus sign."""
    s = s.replace("-", M)
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<i>\1</i>", s)


def ev(s, v, var=None):
    """Value of the plain expression s when its letter is v (exact, with Fractions)."""
    t = s.replace(M, "-").replace("−", "-").replace("×", "*").replace("÷", "/")
    t = re.sub(r"(\d|\))\s*([a-z(])", r"\1*\2", t)
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Fr('%s')" % m.group(), t)
    env = {"Fr": Fr}
    letters = set(re.findall(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", s))
    for L in letters:
        env[L] = Fr(v)
    return eval(t, {"__builtins__": {}}, env)


def lin(a, b, var="n"):
    """Plain text of a·var + b: 3n + 2, 4n − 1, n + 5, 2.5n."""
    a, b = Fr(a), Fr(b)
    s = ("" if a == 1 else n(a)) + var
    if b > 0:
        s += " + " + n(b)
    elif b < 0:
        s += " − " + n(-b)
    return s


def SX(s):
    """Expression inside an SVG text: the letter in italics with a tspan."""
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<tspan font-style='italic'>\1</tspan>", s.replace("-", M))


def dec_lin(c, a, var="n"):
    """Plain text of c − a·var: 50 − 3n."""
    return "%s − %s%s" % (n(c), "" if Fr(a) == 1 else n(a), var)


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None, allow0=False):
    """correct and cands are numbers shown with disp, or HTML strings. Equal values and negatives are skipped."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pick = {plain(cs)}, {cv}, []
    for c in cands:
        if c is None:
            continue
        if disp is not None:
            c = Fr(c)
            if c < 0 or (c == 0 and not allow0) or c in vals:
                continue
            vals.add(c)
            c = disp(c)
        if plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def lstr(vals):
    return ", ".join(n(v) for v in vals)


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


S = 16


def sq(x, y, s=S, fill=FILL):
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x, y, s, s, fill, GREEN))


def shp_grid(k):
    """2 rows of k + 1 tiles: 2k + 2 tiles."""
    cols = k + 1
    s = [sq(1 + i * S, 1 + j * S) for i in range(cols) for j in range(2)]
    return cols * S + 2, 2 * S + 2, s, 2 * cols


def shp_L(k):
    """A corner tile with an arm of k tiles up and k tiles to the right: 2k + 1 tiles."""
    s = [sq(1, 1 + j * S) for j in range(k + 1)] + [sq(1 + i * S, 1 + k * S) for i in range(1, k + 1)]
    return (k + 1) * S + 2, (k + 1) * S + 2, s, 2 * k + 1


def shp_cross(k):
    """A centre tile with 4 arms of k tiles: 4k + 1 tiles."""
    C = 14
    s = []
    for i in range(2 * k + 1):
        s.append(sq(1 + i * C, 1 + k * C, C))
        if i != k:
            s.append(sq(1 + k * C, 1 + i * C, C))
    s.append(sq(1 + k * C, 1 + k * C, C, FILL2))
    return (2 * k + 1) * C + 2, (2 * k + 1) * C + 2, s, 4 * k + 1


def stick(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    t = 6.0 / L
    ax, ay, bx, by = x1 + dx * t, y1 + dy * t, x2 - dx * t, y2 - dy * t
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
            % (ax, ay, bx, by, WOOD))


L_ST = 32


def shp_sticks_sq(k):
    """A row of k squares made of craft sticks: 3k + 1 sticks."""
    s = []
    for i in range(k):
        s.append(stick(3 + i * L_ST, 3, 3 + (i + 1) * L_ST, 3))
        s.append(stick(3 + i * L_ST, L_ST + 3, 3 + (i + 1) * L_ST, L_ST + 3))
    for i in range(k + 1):
        s.append(stick(3 + i * L_ST, 3, 3 + i * L_ST, L_ST + 3))
    assert len(s) == 3 * k + 1
    return k * L_ST + 6, L_ST + 6, s, 3 * k + 1


def shp_house(k):
    """A row of k houses (a square with a triangle roof) sharing walls: 5k + 1 sticks."""
    L, h = L_ST, L_ST * 0.866
    s = []
    for i in range(k):
        x = 3 + i * L
        s.append(stick(x + L / 2, 3, x, 3 + h))
        s.append(stick(x + L / 2, 3, x + L, 3 + h))
        s.append(stick(x, 3 + h, x + L, 3 + h))
        s.append(stick(x, 3 + h + L, x + L, 3 + h + L))
    for i in range(k + 1):
        s.append(stick(3 + i * L, 3 + h, 3 + i * L, 3 + h + L))
    assert len(s) == 5 * k + 1
    return k * L + 6, h + L + 6, s, 5 * k + 1


SHAPES = {"grid": shp_grid, "L": shp_L, "cross": shp_cross, "sticks_sq": shp_sticks_sq, "house": shp_house}


def thing(kind):
    return "craft stick" if kind in ("sticks_sq", "house") else "tile"


def count(kind, k):
    return SHAPES[kind](k)[3]


def pattern_svg(kind, figs=(1, 2, 3)):
    parts = [SHAPES[kind](k) for k in figs]
    LBW, gap, pad = 70, 22, 6
    hmax = max(p[1] for p in parts)
    x = pad
    out = []
    for k, (w, h, s, c) in zip(figs, parts):
        col = max(w, LBW)
        out.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (x + (col - w) / 2, pad + hmax - h, "".join(s)))
        out.append(text(x + col / 2, pad + hmax + 21, "Figure %d" % k, 15))
        x += col + gap
    W = x - gap + pad
    H = pad + hmax + 28
    return svg_wrap(W, H, "".join(out), "growing pattern of %ss: figures %s" % (thing(kind), ", ".join(map(str, figs))))


def table_svg(top, bot, heads=("Term number", "Term value"), label="table of values: term number and term value"):
    CW, LW, RH = 54, 124, 32
    k = len(top)
    W, H = LW + CW * k + 4, RH * 2 + 4
    s = []
    for r, (name, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 5, name, 15))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def tbl(nums, vals, missing=None):
    """Table of values with term numbers nums and values vals; the value at index missing is '?'."""
    top = [n(x) for x in nums]
    bot = ["?" if i == missing else n(v) for i, v in enumerate(vals)]
    return table_svg(top, bot)


def graph_svg(pts, xmax=7, ymax=None, label="graph of a linear pattern"):
    """First-quadrant graph: term number across, term value up. Each point shows its value above it."""
    top = max(y for _, y in pts)
    if ymax is None:
        ymax = int(math.ceil((top + 3) / 4.0)) * 4
    XU, YU = 34, 9
    L, T, R, B = 56, 12, 16, 50
    W = L + xmax * XU + R
    H = T + ymax * YU + B
    X0, Y0 = L, T + ymax * YU
    s = []
    for gy in range(0, ymax + 1, 2):
        y = Y0 - gy * YU
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + xmax * XU, y, GRID))
        if gy % 4 == 0:
            s.append(text(X0 - 7, y + 5, n(gy), 14, "end", False))
    for gx in range(0, xmax + 1):
        x = X0 + gx * XU
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, T, x, Y0, GRID))
        s.append(text(x, Y0 + 19, n(gx), 14, "middle", False))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + xmax * XU, Y0, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, T, X0, Y0, INK))
    s.append(text(X0 + xmax * XU / 2, H - 6, "Term number", 15))
    s.append(text(17, T + ymax * YU / 2, "Term value", 15, extra=" transform='rotate(-90 17 %.1f)'" % (T + ymax * YU / 2)))
    for px, py in pts:
        cx, cy = X0 + px * XU, Y0 - py * YU
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
        s.append("<rect x='%.1f' y='%.1f' width='24' height='17' fill='#fff' opacity='0.85'/>" % (cx - 12, cy - 24))
        s.append(text(cx, cy - 10, n(py), 14))
    return svg_wrap(W, H, "".join(s), label)


def ordinal_pair(a, b):
    return "(%s, %s)" % (n(a), n(b))


# ============================================================ set 1: growing and shrinking patterns
def set_patterns(rnd):
    its = []
    # A: growing by a constant
    for s0, k in [(7, 4), (12, 6), ("3.5", "1.2"), (25, 15)]:
        s0, k = Fr(s0), Fr(k)
        xs = [s0 + i * k for i in range(5)]
        if k.denominator != 1:      # 7.1 + 1.2: two jumps, only the 1, only the 0.2, adding the first term
            cands = [xs[3] + 2 * k, xs[3] + int(k), xs[3] + (k - int(k)), xs[3] + s0]
        else:
            cands = [xs[3] + 2 * k, xs[3] + k + 1, xs[3] + k - 1, xs[3] + s0]
        q = "What is the next term?<br><b>%s, ?</b>" % lstr(xs[:4])
        e = "The pattern grows by %s each time (%s + %s = %s). Next: %s + %s = %s." % (
            n(k), n(xs[0]), n(k), n(xs[1]), n(xs[3]), n(k), n(xs[4]))
        its.append((0, mcq(q, xs[4], cands, e, rnd, n)))
    # B: shrinking by a constant
    for s0, k in [(95, 7), (200, 25), ("10.5", "0.8"), (60, 9)]:
        s0, k = Fr(s0), Fr(k)
        xs = [s0 - i * k for i in range(5)]
        if k.denominator != 1:      # 8.1 − 0.8: two jumps, wrong way, smaller digit from larger (8.7), only the 1
            assert xs[3] == Fr("8.1")
            cands = [xs[3] - 2 * k, xs[3] + k, Fr("8.7"), xs[3] - 1]
        else:
            cands = [xs[3] - 2 * k, xs[3] + k, xs[3] - k + 1, xs[3] - k - 1]
        q = "What is the next term?<br><b>%s, ?</b>" % lstr(xs[:4])
        e = "The pattern shrinks by %s each time (%s − %s = %s). Next: %s − %s = %s." % (
            n(k), n(xs[0]), n(k), n(xs[1]), n(xs[3]), n(k), n(xs[4]))
        its.append((1, mcq(q, xs[4], cands, e, rnd, n)))
    # C: check every step, not only the first difference
    q = "What is the next term?<br><b>3, 6, 12, 24, ?</b>"
    e = ("The differences are 3, 6, 12, so the pattern does not add the same amount. Each term is 2 times the one before: "
         "24 × 2 = 48. (Adding the first difference, 24 + 3 = 27, only works for the first step.)")
    its.append((2, mcq(q, 48, [27, 36, 30], e, rnd, n)))
    q = "What is the next term?<br><b>1, 2, 4, 7, 11, ?</b>"
    e = "The differences are 1, 2, 3, 4, so the next difference is 5: 11 + 5 = 16. (Adding the first difference gives 12.)"
    its.append((2, mcq(q, 16, [12, 15, 22], e, rnd, n)))
    q = "What is the next term?<br><b>1, 3, 6, 10, 15, ?</b>"
    e = "The differences are 2, 3, 4, 5, so the next difference is 6: 15 + 6 = 21. (Adding the first difference gives 17.)"
    its.append((2, mcq(q, 21, [17, 20, 30], e, rnd, n)))
    q = "What is the next term?<br><b>2, 5, 11, 23, ?</b>"
    e = ("The differences are 3, 6, 12. They double, so the next difference is 24: 23 + 24 = 47. "
         "(Rule: multiply by 2, then add 1. Adding the first difference gives 26.)")
    its.append((2, mcq(q, 47, [26, 35, 46], e, rnd, n)))
    # D: tables with a far term
    for a, k, N in [(5, 3, 8), (6, 4, 10), (100, -6, 10), (90, -8, 8)]:
        vals = [a + i * k for i in range(4)]
        ans = a + (N - 1) * k
        q = (fig(tbl([1, 2, 3, 4, N], vals + [ans], missing=4)) +
             "The pattern continues in the same way. What is the term value for term number %d?" % N)
        sg = "+" if k > 0 else "−"
        e = ("The term value %s by %d each time. From term 1 to term %d there are %d jumps: %s %s %d × %d = %s. "
             "(%s is the value for term 5, the next term in the list.)" % (
                 "goes up" if k > 0 else "goes down", abs(k), N, N - 1, n(a), sg, N - 1, abs(k), n(ans),
                 n(vals[3] + k)))
        cands = [vals[3] + k, a + N * k]
        if k > 0:
            cands += [2 * (a + (N // 2 - 1) * k), N * a, N * k]     # doubling term N/2 for term N
        else:
            cands += [a + (N - 2) * k, a - N]
        its.append((3, mcq(q, ans, cands, e, rnd, n)))
    # E: tile and craft-stick figures
    for kind in ["sticks_sq", "L", "cross", "house"]:
        a, b, c = [count(kind, k) for k in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = c + k
        assert ans == count(kind, 4)
        q = fig(pattern_svg(kind)) + "How many %ss will Figure 4 need?" % w
        e = "Count each figure: %d, %d, %d. Each figure adds %d %ss. Figure 4: %d + %d = %d." % (a, b, c, k, w, c, k, ans)
        its.append((4, mcq(q, ans, [c + 1, 4 * a, c + 2 * k, c + a], e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Growing and shrinking patterns", "items": [i for _, i in its]}


# ============================================================ set 2: evaluate expressions
def e_eval(expr, var, v, steps_):
    return "Replace %s with %s: %s." % (X(var), n(v), steps_)


def set_evaluate(rnd):
    its = []
    # A and B: a·var + b with whole numbers, then decimal tenths
    cases = [(3, 5, "n", 4), (6, -4, "x", 7), (2, 9, "k", 8), (5, -2, "m", 6), (7, 3, "t", 9),
             (4, -3, "n", "2.5"), (2, "1.5", "x", "3.4"), (5, 2, "k", "1.2"), (3, "-0.5", "m", "4.5"),
             (10, 4, "t", "0.7"), (6, -2, "n", "1.5")]
    for gi, (a, b, var, v) in enumerate(cases):
        a, b, v = Fr(a), Fr(b), Fr(v)
        s = lin(a, b, var)
        ans = ev(s, v)
        assert ans == a * v + b
        q = "Evaluate <b>%s</b> when %s = %s." % (X(s), X(var), n(v))
        sg = "+" if b > 0 else "−"
        e = ("Replace %s with %s and multiply first: %s × %s %s %s = %s %s %s = %s. %s means %s × %s, not %s + %s."
             % (X(var), n(v), n(a), n(v), sg, n(abs(b)), n(a * v), sg, n(abs(b)), n(ans),
                X(n(a) + var), n(a), X(var), n(a), X(var)))
        whole_part = Fr(int(v))
        cands = [a + v + b, a * v]
        if v.denominator != 1:
            slip = a * whole_part + (v - whole_part) + b      # 4 × 2.5 done as 4 × 2 + 0.5
            cands.insert(0, slip)
        concat = Fr(n(a) + n(v).replace(NBSP, "")) + b         # 3n read as 34 when n = 4
        cands.append(concat)
        cands += [a * (v + b), a * v - b if b > 0 else a * v + abs(b)]
        its.append((0 if v.denominator == 1 else 1, mcq(q, ans, cands, e, rnd, n)))
    # C: brackets, division and a number in front
    rows = [
        ("2(n + 3)", "n", "1.5", ["6", "6.5", "4.5"],
         "Work inside the brackets first: 1.5 + 3 = 4.5. Then 2 × 4.5 = 9. (2 × 1.5 + 3 = 6 forgets to double the 3.)"),
        ("n ÷ 2 + 7", "n", "9", ["1", "8", "11"],
         "Divide first, then add: 9 ÷ 2 = 4.5, and 4.5 + 7 = 11.5. (9 ÷ (2 + 7) = 1 adds first.)"),
        ("20 − 3n", "n", "4", ["68", "13", "16"],
         "Multiply first: 3 × 4 = 12. Then 20 − 12 = 8. (20 − 3 = 17, then 17 × 4 = 68 works left to right and is wrong.)"),
        ("4(n − 1)", "n", "3.5", ["13", "6.5", "14"],
         "Brackets first: 3.5 − 1 = 2.5. Then 4 × 2.5 = 10. (4 × 3.5 − 1 = 13 forgets the brackets.)"),
        ("5 + 2n", "n", "6.5", ["45.5", "13.5", "31.5"],
         "Multiply first: 2 × 6.5 = 13. Then 5 + 13 = 18. ((5 + 2) × 6.5 = 45.5 adds first.)"),
    ]
    for s, var, v, wrong, e in rows:
        ans = ev(s, Fr(v))
        q = "Evaluate <b>%s</b> when %s = %s." % (X(s), X(var), n(Fr(v)))
        its.append((2, mcq(q, ans, [Fr(w) for w in wrong], e, rnd, n)))
    # D: which expression has this value / missing value in a table
    for v, target, good, bad in [(4, 20, "6n − 4", ["4n + 6", "5n − 4", "n + 6"]),
                                 ("2.5", 12, "4n + 2", ["2n + 4", "5n − 2", "3n + 2"])]:
        v = Fr(v)
        assert ev(good, v) == target and all(ev(b, v) != target for b in bad)
        q = "Which expression has a value of %s when %s = %s?" % (n(target), X("n"), n(v))
        e = "Check each one: %s. Only %s gives %s." % (
            "; ".join("%s = %s" % (X(x), n(ev(x, v))) for x in [good] + bad), X(good), n(target))
        its.append((3, mcq(q, X(good), [X(b) for b in bad], e, rnd)))
    for a, b, nums, last in [(5, -1, [1, 2, 3], "4.5"), (3, 4, [1, 2, 3], "6.5")]:
        s = lin(a, b)
        last = Fr(last)
        vals = [ev(s, x) for x in nums]
        ans = ev(s, last)
        q = (fig(table_svg([n(x) for x in nums] + [n(last)], [n(x) for x in vals] + ["?"], (SX("n"), SX(s)),
                           "table of values for an expression")) +
             "The table shows values of <b>%s</b>. What is the missing value?" % X(s))
        e = "Replace %s with %s: %s × %s %s %s = %s." % (
            X("n"), n(last), n(a), n(last), "+" if b > 0 else "−", n(abs(b)), n(ans))
        cands = [vals[-1] + a, a * last, a * int(last) + (last - int(last)) + b, ev(s, last + 1)]
        its.append((3, mcq(q, ans, cands, e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate expressions with whole numbers and decimals", "items": [i for _, i in its]}


# ============================================================ set 3: find the rule as an expression
def rule_e(a, b, vals, what="term value"):
    sg = "+" if b > 0 else "−"
    s = lin(a, b)
    first = vals[0]
    return ("The %s goes up by %s each time, so the expression has %s. Term 1: %s × 1 = %s, but the value is %s, "
            "so %s: %s. Check term 4: %s × 4 %s %s = %s." % (
                what, n(a), X(lin(a, 0)), n(a), n(a), n(first),
                ("add " + n(b)) if b > 0 else ("subtract " + n(-b)), X(s),
                n(a), sg, n(abs(b)), n(vals[3])))


def set_rule(rnd):
    its = []
    # A: tables of values
    for a, b in [(3, 2), (4, 1), (5, -2), (2, 7), (6, 3), (7, -4)]:
        s = lin(a, b)
        vals = [a * i + b for i in range(1, 5)]
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which expression gives the term value for term number %s?" % X("n")
        e = rule_e(a, b, vals)
        cands = [X(lin(1, a)), X(lin(a, 0)), X(lin(vals[0], 0))]
        if b > 0:
            cands.insert(1, X(lin(b, a)))
        cands.append(X(lin(a, vals[0])))
        its.append((0, mcq(q, X(s), cands, e, rnd)))
    # B: lists of terms
    for a, b in [(4, 5), (8, -3), ("2.5", 1), (10, 5)]:
        a, b = Fr(a), Fr(b)
        s = lin(a, b)
        vals = [a * i + b for i in range(1, 5)]
        q = ("The first term of this pattern has term number 1.<br><b>%s, …</b><br>"
             "Which expression gives term %s?" % (lstr(vals), X("n")))
        e = rule_e(a, b, vals, "pattern")
        cands = [X(lin(a, vals[0])), X(lin(vals[0], 0)), X(lin(1, a)), X(lin(a, 0))]
        its.append((1, mcq(q, X(s), cands, e, rnd)))
    # C: figures
    for kind in ["sticks_sq", "grid", "cross", "house"]:
        a, b2, c = [count(kind, k) for k in (1, 2, 3)]
        k = b2 - a
        r = a - k
        w = thing(kind)
        s = lin(k, r)
        assert all(ev(s, i) == count(kind, i) for i in range(1, 6))
        q = fig(pattern_svg(kind)) + "Which expression gives the number of %ss in Figure %s?" % (w, X("n"))
        e = ("Count: %d, %d, %d. Each figure adds %d %ss, so the expression has %s. Figure 1: %d × 1 = %d, and it has %d, "
             "so add %d. Check Figure 3: %d × 3 + %d = %d." % (a, b2, c, k, w, X(lin(k, 0)), k, k, a, r, k, r, c))
        cands = [X(lin(a, 0)), X(lin(k, a)), X(lin(1, k)), X(lin(k, 0))]
        its.append((2, mcq(q, X(s), cands, e, rnd)))
    # D: shrinking patterns
    for c0, a in [(50, 3), (100, 8), (30, "2.5")]:
        c0, a = Fr(c0), Fr(a)
        s = dec_lin(c0, a)
        vals = [c0 - a * i for i in range(1, 5)]
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which expression gives the term value for term number %s?" % X("n")
        e = ("The value goes down by %s each time, so the expression subtracts %s. Term 1 is %s, so start at "
             "%s + %s = %s: %s. Check term 4: %s − %s × 4 = %s." % (
                 n(a), X(n(a) + "n"), n(vals[0]), n(vals[0]), n(a), n(c0), X(s), n(c0), n(a), n(vals[3])))
        cands = [X(dec_lin(vals[0], a)), X(lin(a, vals[0])), X(dec_lin(c0, 1)), X(lin(a, 0))]
        its.append((3, mcq(q, X(s), cands, e, rnd)))
    # E: which list of term values matches the expression
    for a, b in [(2, 5), (3, 4), (5, 1)]:
        s = lin(a, b)
        right = lstr([a * i + b for i in range(1, 5)])
        from0 = lstr([a * i + b for i in range(0, 4)])
        swap = lstr([b * i + a for i in range(1, 5)])
        times = lstr([(a + b) * i for i in range(1, 5)])
        q = "Which list shows the first four term values of <b>%s</b>? (The first term number is 1.)" % X(s)
        e = ("Replace %s with 1, 2, 3 and 4: %s × 1 + %d = %d, %s × 2 + %d = %d, and so on. "
             "Each value is %d more than the one before." % (X("n"), n(a), b, a + b, n(a), b, 2 * a + b, a))
        its.append((4, mcq(q, right, [from0, swap, times], e, rnd)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Find the pattern rule as an expression", "items": [i for _, i in its]}


# ============================================================ set 4: term numbers, term values and graphs
def set_terms(rnd):
    its = []
    # A: value from the rule
    for a, b, N in [(4, 3, 12), (6, -5, 20), ("2.5", 4, 10), (7, 9, 30)]:
        a, b = Fr(a), Fr(b)
        s = lin(a, b)
        ans = ev(s, N)
        q = "A pattern rule is <b>%s</b>, where %s is the term number. What is the term value for term number %d?" % (
            X(s), X("n"), N)
        e = "Replace %s with %d: %s × %d %s %s = %s. (%d is the term number; the term value is %s.)" % (
            X("n"), N, n(a), N, "+" if b > 0 else "−", n(abs(b)), n(ans), N, n(ans))
        its.append((0, mcq(q, ans, [a * N, a + N + b, a * (N + 1) + b, Fr(N)], e, rnd, n)))
    # B: value for a far term from a table
    for a, b, N in [(3, 4, 20), (5, -2, 25), (4, 6, 50), (9, 1, 15)]:
        vals = [a * i + b for i in range(1, 5)]
        ans = a * N + b
        q = (fig(tbl([1, 2, 3, 4], vals)) +
             "The pattern continues. What is the term value for term number %d?" % N)
        e = ("The value goes up by %d, so the rule is %s. Term %d: %d × %d %s %d = %s." % (
            a, X(lin(a, b)), N, a, N, "+" if b > 0 else "−", abs(b), n(ans)))
        its.append((1, mcq(q, ans, [vals[3] + a, N * vals[0], N * a, a * (N - 1) + b], e, rnd, n)))
    # C: term number from a value
    rows = [(3, 2, 44, ["44", "134", "15"]), (5, -4, 96, ["96", "476", "18.4"]),
            (4, 6, 70, ["70", "286", "19"]), ("2.5", 3, 28, ["28", "73", "12.4"])]
    for a, b, V, wrong in rows:
        a, b = Fr(a), Fr(b)
        s = lin(a, b)
        N = (V - b) / a
        assert N.denominator == 1 and ev(s, N) == V
        q = "A pattern rule is <b>%s</b>. Which term number has a term value of %s?" % (X(s), n(V))
        undo = "subtract %s" % n(b) if b > 0 else "add %s" % n(-b)
        e = ("Work backwards: %s, then divide by %s. %s %s %s = %s, and %s ÷ %s = %s. Check: %s × %s %s %s = %s. "
             "(%s is the term value, not the term number.)" % (
                 undo, n(a), n(V), "−" if b > 0 else "+", n(abs(b)), n(V - b), n(V - b), n(a), n(N),
                 n(a), n(N), "+" if b > 0 else "−", n(abs(b)), n(V), n(V)))
        for w in wrong:
            assert Fr(w) != N
        its.append((2, mcq(q, N, [Fr(w) for w in wrong], e, rnd, n)))
    # D: graphs
    g1 = graph_svg([(i, 2 * i + 3) for i in range(1, 5)], label="graph of a linear pattern: 5, 7, 9, 11")
    q = fig(g1) + "The graph shows a linear growing pattern. What is the term value for term number 6?"
    e = "The values go up by 2: 5, 7, 9, 11, 13, 15. Term 6 is 15. (13 is term 5, the next point.)"
    its.append((3, mcq(q, 15, [13, 30, 12], e, rnd, n)))
    q = fig(g1) + "Which expression gives the term value for term number %s?" % X("n")
    e = "The values go up by 2, so the expression has %s. Term 1: 2 × 1 = 2, and the value is 5, so add 3: %s." % (
        X("2n"), X("2n + 3"))
    its.append((3, mcq(q, X("2n + 3"), [X("2n + 5"), X("n + 2"), X("5n")], e, rnd)))
    g2 = graph_svg([(i, 3 * i + 1) for i in range(1, 5)], label="graph of a linear pattern: 4, 7, 10, 13")
    q = fig(g2) + "Each point is (term number, term value). Which point comes next?"
    e = ("The next term number is 5. The values go up by 3, so its value is 13 + 3 = 16. The point is (5, 16). "
         "(16, 5) has the numbers swapped: the term number comes first.")
    its.append((3, mcq(q, ordinal_pair(5, 16), [ordinal_pair(16, 5), ordinal_pair(5, 14), ordinal_pair(6, 16)], e, rnd)))
    g3 = graph_svg([(i, 20 - 3 * i) for i in range(1, 5)], label="graph of a linear shrinking pattern: 17, 14, 11, 8")
    q = fig(g3) + "The pattern keeps shrinking in the same way. Which term number has a term value of 2?"
    e = "The values go down by 3: 17, 14, 11, 8, 5, 2. The value 2 is term number 6. (2 is the term value, not the term number.)"
    its.append((3, mcq(q, 6, [2, 5, 7], e, rnd, n)))
    g4 = graph_svg([(i, 4 * i - 2) for i in range(1, 5)], label="graph of a linear pattern: 2, 6, 10, 14")
    assert ev("4n - 2", 10) == 38
    q = fig(g4) + "The pattern rule is %s. Which point would also be on this graph?" % X("4n − 2")
    e = "For term number 10: 4 × 10 − 2 = 38, so the point is (10, 38). The term number comes first."
    its.append((3, mcq(q, ordinal_pair(10, 38), [ordinal_pair(38, 10), ordinal_pair(10, 40), ordinal_pair(10, 42)], e, rnd)))
    # E: is this number a term of the pattern? (justify a prediction)
    for a, b, good, bad in [(4, 1, 45, [48, 46, 43]), (3, 2, 50, [51, 52, 49]), (5, -1, 64, [65, 66, 60])]:
        s = lin(a, b)
        N = Fr(good - b, a)
        assert N.denominator == 1
        for x in bad:
            assert Fr(x - b, a).denominator != 1
        q = "Which number is a term value in the pattern <b>%s</b>?" % X(s)
        e = ("Undo the rule: %s %s %d = %d, and %d ÷ %d = %s, a whole term number. Check: %d × %s %s %d = %d. "
             "For the other numbers, %s %d does not give a multiple of %d." % (
                 n(good), "−" if b > 0 else "+", abs(b), good - b, good - b, a, n(N), a, n(N),
                 "+" if b > 0 else "−", abs(b), good, "subtracting" if b > 0 else "adding", abs(b), a))
        its.append((4, mcq(q, good, bad, e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Term numbers, term values and graphs", "items": [i for _, i in its]}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []

    def add(q, ans, cands, e, disp=None):
        its.append(mcq(q, ans, cands, e, rnd, disp))

    def cad(v):
        return money(v)

    unit = lambda u: (lambda v: n(v) + NBSP + u)
    # values from a rule
    assert 2 * 12 + 2 == 26
    add("Square tables are pushed together in a row for a class party. 1 table seats 4 students, 2 tables seat 6, "
        "and 3 tables seat 8. How many students can sit at 12 tables?",
        26, [48, 24, 28],
        "Each table adds 2 seats, so the rule is 2" + X("n") + " + 2. 2 × 12 + 2 = 26. "
        "(12 × 4 = 48 counts the seats lost where tables touch.)", lambda v: "%d students" % v)
    assert 35 + 15 * 8 == 155
    add("Liam has $35 in his bank account. He saves $15 each week. How much will he have after 8 weeks?",
        155, [120, 400, 170],
        "The rule is 15" + X("w") + " + 35. 15 × 8 = 120, and 120 + 35 = 155, so $155. ($120 forgets the $35 he started with.)",
        lambda v: money(v, False))
    assert ev("8h + 25", Fr("3.5")) == 53
    add("A canoe rental at the provincial park costs $25 plus $8 for each hour. How much does a 3.5-hour rental cost?",
        53, [28, Fr("36.5"), Fr("115.5")],
        "The rule is 8" + X("h") + " + 25. Multiply first: 8 × 3.5 = 28. Then 28 + 25 = $53.00. "
        "((25 + 8) × 3.5 = $115.50 adds first.)", cad)
    assert Fr("1.5") + 7 * Fr("0.5") == 5
    add("To train for the Terry Fox Run, Maya runs 1.5 km in week 1. Each week she runs 0.5 km more. How far does she run in week 8?",
        5, [Fr("5.5"), Fr("4.5"), 12],
        "From week 1 to week 8 there are 7 jumps: 7 × 0.5 = 3.5 km. 1.5 + 3.5 = 5 km. (5.5 km adds 8 jumps.)", unit("km"))
    assert 30 - Fr("2.5") * 8 == 10
    add("A candle is 30 cm tall. It burns down 2.5 cm each hour. How tall is it after 8 hours?",
        10, [20, Fr("27.5"), Fr("7.5")],
        "The rule is 30 − 2.5" + X("h") + ". 2.5 × 8 = 20 cm burns away. 30 − 20 = 10 cm. (20 cm is the part that burned.)",
        unit("cm"))
    assert 300 + 12 * 28 == 636
    add("A field trip to the science centre costs $300 for the bus plus $12 for each student. What is the cost for 28 students?",
        636, [336, 8736, 340],
        "The rule is 12" + X("s") + " + 300. 12 × 28 = 336, and 336 + 300 = $636. ((300 + 12) × 28 = $8736 adds first.)",
        lambda v: money(v, False))
    assert 8 - Fr("1.5") * 4 == 2
    add("On a winter afternoon it is 8" + NBSP + "°C at 3 p.m. The temperature falls 1.5" + NBSP +
        "°C each hour. What is the temperature at 7 p.m.?",
        2, [14, Fr("6.5"), Fr("0.5")],
        "3 p.m. to 7 p.m. is 4 hours. 4 × 1.5 = 6 degrees. 8 − 6 = 2" + NBSP + "°C. (14" + NBSP + "°C adds instead of subtracting.)",
        unit("°C"))
    assert 74 + 6 * 10 == 134
    add("One stacking chair is 80 cm tall. Each extra chair on the stack adds 6 cm. How tall is a stack of 10 chairs?",
        134, [800, 140, 60],
        "From 1 chair to 10 chairs there are 9 extra chairs: 9 × 6 = 54 cm. 80 + 54 = 134 cm. "
        "(80 + 10 × 6 = 140 counts one chair too many.)", unit("cm"))
    assert 8 + Fr("14.5") * 6 == 95
    add("Pizza for a lunch fundraiser costs $14.50 a pizza plus an $8 delivery fee. How much do 6 pizzas cost?",
        95, [87, 135, Fr("28.5")],
        "The rule is 14.5" + X("p") + " + 8. 14.50 × 6 = 87, and 87 + 8 = $95.00. ((14.50 + 8) × 6 = $135 adds the fee to every pizza.)",
        cad)
    assert 12 - Fr("1.5") * 4 == 6
    add("On a canoe trip, Arjun is 12 km from the cottage. He paddles toward it at 1.5 km each hour. How far from the cottage is he after 4 hours?",
        6, [18, Fr("10.5"), Fr("7.5")],
        "The rule is 12 − 1.5" + X("h") + ". 1.5 × 4 = 6 km paddled. 12 − 6 = 6 km left. (18 km adds instead of subtracting.)",
        unit("km"))
    # term numbers from a value
    assert 3 * 20 + 1 == 61
    add("Lucas makes a row of squares with craft sticks: 4 sticks, 7 sticks, 10 sticks, … The rule is 3" + X("n") +
        " + 1. Which figure uses 61 sticks?",
        "Figure 20", ["Figure 61", "Figure 21", "Figure 184"],
        "Work backwards: 61 − 1 = 60, and 60 ÷ 3 = 20. Check: 3 × 20 + 1 = 61. (61 is the number of sticks, not the figure number.)")
    assert 20 + Fr("7.5") * 10 == 95
    add("A swimming pass costs $20 to join plus $7.50 for each lesson. Hana pays $95 in total. How many lessons does she take?",
        "10 lessons", ["12 lessons", "9 lessons", "75 lessons"],
        "Take away the $20 first: 95 − 20 = 75. Then 75 ÷ 7.50 = 10 lessons. Check: 20 + 10 × 7.50 = $95.00. (95 ÷ 7.50 forgets the $20 to join.)")
    assert 20 - Fr("0.5") * 24 == 8
    add("The ringette team’s water jug holds 20 L. Each player fills a 0.5 L bottle from it. After how many bottles are 8 L left?",
        "24 bottles", ["40 bottles", "16 bottles", "56 bottles"],
        "The rule is 20 − 0.5" + X("b") + ". 20 − 8 = 12 L is used. 12 ÷ 0.5 = 24 bottles. (40 bottles would empty the jug.)")
    assert 40 + Fr("12.5") * 8 == 140
    add("Mateo has $40. He saves $12.50 each week. After how many weeks will he have $140?",
        "8 weeks", ["11 weeks", "9 weeks", "14 weeks"],
        "He needs 140 − 40 = $100 more. 100 ÷ 12.50 = 8 weeks. Check: 40 + 8 × 12.50 = $140.00. (140 ÷ 12.50 forgets the $40 he already has.)")
    assert 3 * 16 + 1 == 49 and 3 * 17 + 1 == 52
    add("Chloe makes a row of craft-stick squares: 4, 7, 10, … sticks (3" + X("n") +
        " + 1). She has 50 sticks. What is the largest figure she can make?",
        "Figure 16", ["Figure 17", "Figure 12", "Figure 13"],
        "Figure 16 uses 3 × 16 + 1 = 49 sticks. Figure 17 needs 3 × 17 + 1 = 52, which is more than 50. So Figure 16.")
    # choose the expression
    add("A sap tank on a maple farm holds 40 L of sap at 8 a.m. Sap drips in at 2.5 L each hour. "
        "Which expression gives the amount of sap after " + X("h") + " hours?",
        X("40 + 2.5h"), [X("2.5 + 40h"), X("42.5h"), X("40 − 2.5h")],
        "Start with 40 L and add 2.5 L for every hour: 40 + 2.5" + X("h") + ". The 40 L is added only once.")
    add("Mei has 120 hockey cards. She gives away 6 cards each week. Which expression gives the number of cards left after "
        + X("w") + " weeks?",
        X("120 − 6w"), [X("6w − 120"), X("120 + 6w"), X("114w")],
        "She starts with 120 and loses 6 each week, so subtract 6" + X("w") + ": 120 − 6" + X("w") + ".")
    add("Ethan earns $15 for each driveway he shovels after a snowstorm. He paid $20 for a new shovel. "
        "Which expression gives his profit after " + X("d") + " driveways?",
        X("15d − 20"), [X("20 − 15d"), X("15d + 20"), X("5d")],
        "He earns 15" + X("d") + " dollars and the shovel cost $20, so his profit is 15" + X("d") + " − 20.")
    add("Benjamin builds a row of triangles with toothpicks. Figure 1 uses 3, Figure 2 uses 5 and Figure 3 uses 7. "
        "Which expression gives the toothpicks in Figure " + X("n") + "?",
        X("2n + 1"), [X("3n"), X("n + 2"), X("2n + 3")],
        "Each figure adds 2, so the expression has 2" + X("n") + ". Figure 1: 2 × 1 = 2, and it uses 3, so add 1: 2" + X("n") +
        " + 1. (2" + X("n") + " + 3 uses the first term, 3, as the number added.)")
    add("Leah’s sunflower is 4.5 cm tall on day 1 and grows 1.2 cm each day. Which expression gives its height on day " +
        X("d") + "?",
        X("1.2d + 3.3"), [X("1.2d + 4.5"), X("4.5d"), X("d + 1.2")],
        "Each day adds 1.2 cm, so the expression has 1.2" + X("d") + ". Day 1: 1.2 × 1 = 1.2, and the height is 4.5, "
        "so add 4.5 − 1.2 = 3.3. Check day 2: 1.2 × 2 + 3.3 = 5.7 cm.")
    assert ev("1.2d + 3.3", 1) == Fr("4.5") and ev("1.2d + 3.3", 2) == Fr("5.7")
    rnd.shuffle(its)
    return {"title": "Pattern and expression word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    t = tbl([1, 2, 3, 4, 10], [4, 7, 10, 13, 31])
    g = graph_svg([(i, 3 * i + 1) for i in range(1, 5)], label="graph of a linear pattern: 4, 7, 10, 13")
    return (
        "<h2>Term numbers and term values</h2>"
        "<p>Each number in a pattern is a <b>term</b>. Its place in the pattern is the <b>term number</b> (1, 2, 3 …), "
        "and the number itself is the <b>term value</b>. A <b>growing</b> pattern gets bigger and a <b>shrinking</b> "
        "pattern gets smaller.</p>" +
        ex("Example 1", "95, 88, 81, 74, ?", "The pattern shrinks by 7 each time. 74 − 7 = 67.", "67") +
        "<h2>Find the pattern rule</h2>"
        "<p>Put the pattern in a table of values. If the term value goes up by the same amount each time, the pattern is "
        "<b>linear</b>. The amount it goes up by is the number in front of " + X("n") + ".</p>"
        "<figure class='sn-fig'>" + pattern_svg("sticks_sq") +
        "<figcaption>4, 7, 10 craft sticks: each new square adds 3 sticks, because it shares a side.</figcaption></figure>"
        "<figure class='sn-fig'>" + t +
        "<figcaption>The value goes up by 3, so start with 3" + X("n") + ". Term 1: 3 × 1 = 3, but the value is 4, so add 1. "
        "The rule is 3" + X("n") + " + 1. Term 10: 3 × 10 + 1 = 31.</figcaption></figure>" +
        ex("Example 2", "Find the rule: 5, 8, 11, 14, …",
           "The terms go up by 3, so use 3" + X("n") + ". 3 × 1 = 3, and 5 − 3 = 2. Check term 4: 3 × 4 + 2 = 14.",
           X("3n + 2")) +
        "<h2>Evaluate an expression</h2>"
        "<p>To <b>evaluate</b> an expression, replace the letter with a number. 4" + X("n") + " means 4 × " + X("n") +
        ". Multiply before you add or subtract, unless there are brackets.</p>" +
        ex("Example 3", "Evaluate 4" + X("n") + " − 3 when " + X("n") + " = 2.5.",
           "4 × 2.5 = 10. Then 10 − 3 = 7.", "7") +
        "<h2>Work backwards to find the term number</h2>" +
        ex("Example 4", "The rule is 3" + X("n") + " + 2. Which term number has a value of 44?",
           "Undo the rule: 44 − 2 = 42, and 42 ÷ 3 = 14. Check: 3 × 14 + 2 = 44.", "term number 14") +
        "<h2>Graph a linear pattern</h2>"
        "<p>Plot each term as a point (term number, term value). The points of a linear pattern lie in a straight line.</p>"
        "<figure class='sn-fig'>" + g +
        "<figcaption>The pattern 3" + X("n") + " + 1: the points (1, 4), (2, 7), (3, 10), (4, 13) go up 3 for every step right. "
        "The next point is (5, 16).</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using only the first difference: 3, 6, 12, 24 is “add 3”", "Check every step. 3, 6, 12, 24 doubles: the next term is 48"],
            ["Mixing up the term number and the term value", "The term number is the position; the term value is the number in that position"],
            ["Reading 3" + X("n") + " as 3 + " + X("n"), "3" + X("n") + " means 3 × " + X("n") + ". When " + X("n") + " = 4, 3" + X("n") + " = 12"],
            ["Writing 3" + X("n") + " + 5 for 5, 8, 11, 14", "Check term 1: 3 × 1 + 5 = 8, not 5. The rule is 3" + X("n") + " + 2"],
            ["Term 10 = term 1 + 10 jumps", "From term 1 to term 10 there are 9 jumps"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about patterns in the Ontario math curriculum?",
     "a": "In Grade 6 (Algebra, C1), students extend growing and shrinking patterns, find the pattern rule, and write it as an algebraic expression such as 3n + 2 to find unknown term values and term numbers. They also show linear patterns in tables of values and graphs."},
    {"q": "What is the difference between a term number and a term value?",
     "a": "The term number is the position in the pattern (1st, 2nd, 3rd …) and the term value is the number in that position. In 5, 8, 11, 14, term number 3 has a term value of 11."},
    {"q": "How do you find the rule for a linear pattern like 5, 8, 11, 14?",
     "a": "Find how much the value goes up each time (3) and write 3n. Then check term 1: 3 × 1 = 3, and you need 5, so add 2. The rule is 3n + 2."},
    {"q": "Are patterns and expressions on the Grade 6 EQAO math test?",
     "a": "Yes. Grade 6 students write the EQAO math assessment in the spring, and it covers all strands of the Ontario curriculum, including algebra questions on patterns and expressions."},
]


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(36810)
    sets = [set_patterns(rnd), set_evaluate(rnd), set_rule(rnd), set_terms(rnd), set_words(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"]
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "patterns-and-expressions", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Patterns and Expressions: Pattern Rules, Term Values and Evaluating Expressions",
        "seo_title": "Grade 6 Patterns and Expressions Worksheets: Pattern Rules and Algebra (Free, Answer Key)",
        "short_title": "Patterns and Expressions",
        "domain": "Algebra",
        "standard_code": "Grade 6: Algebra, C1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating, growing, and shrinking patterns, and use algebraic representations of the pattern rules to solve for unknown values in linear growing patterns",
        "meta_desc": "Free Grade 6 math worksheets on patterns and expressions for the Ontario curriculum: growing and shrinking patterns, tables of values, pattern rules like 3n + 2, term numbers and term values, evaluating expressions with decimals, and simple graphs. 100 questions with an answer key, good EQAO practice.",
        "key_big": "In a linear pattern, the jump is the number in front of n. Check term 1 to find what to add: 5, 8, 11, 14 is 3n + 2.",
        "key_sub": "The term number is the position; the term value is the number there. 3n means 3 × n, so when n = 2.5, 3n = 7.5. Check every step, not only the first difference.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(growing pattern|table|graph)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
