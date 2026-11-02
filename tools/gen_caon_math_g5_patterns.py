# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Patterns (Ontario Mathematics Curriculum 2020, Grade 5: Algebra, C1.2, C1.3 and C1.4)
  python3 tools/gen_caon_math_g5_patterns.py
Growing, shrinking and repeating patterns, tables of values, pattern rules in words (start at 5 and add 3 each time;
term number × 3 + 2), patterns with decimal tenths and hundredths (0.25, 0.5, 0.75), graphs of patterns and
predictions in Canadian word problems.
Wrong answers come from real student mistakes: using only the first step, mixing up the term number and the term
value, counting n jumps instead of n − 1, using the first term as the number added, swapping the start and the jump,
decimal regrouping slips (0.9 + 0.3 = 0.12, 0.75 + 0.25 = 0.100), and swapping the coordinates of a point.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
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
    """Ontario style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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



def graph_svg(pts, xmax=7, ymax=None, xl="Term number", yl="Term value", label="graph of a pattern"):
    """First-quadrant graph. Each point shows its value above it."""
    top = max(y for _, y in pts)
    if ymax is None:
        ymax = int(math.ceil((top + 3) / 4.0)) * 4
    if ymax > 32:
        ymax = int(math.ceil(ymax / 10.0)) * 10
    step = 2 if ymax <= 16 else (4 if ymax <= 32 else 10)
    lab = 2 * step if ymax <= 32 else step
    YU = 150.0 / ymax
    XU = 34
    L, T, R, B = 58, 22, 16, 50
    W = L + xmax * XU + R
    H = T + ymax * YU + B
    X0, Y0 = L, T + ymax * YU
    s = []
    for gy in range(0, ymax + 1, step):
        y = Y0 - gy * YU
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + xmax * XU, y, GRID))
        if gy % lab == 0:
            s.append(text(X0 - 7, y + 5, n(gy), 14, "end", False))
    for gx in range(0, xmax + 1):
        x = X0 + gx * XU
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, T, x, Y0, GRID))
        s.append(text(x, Y0 + 19, n(gx), 14, "middle", False))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + xmax * XU, Y0, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, T, X0, Y0, INK))
    s.append(text(X0 + xmax * XU / 2, H - 6, xl, 15))
    s.append(text(17, T + ymax * YU / 2, yl, 15, extra=" transform='rotate(-90 17 %.1f)'" % (T + ymax * YU / 2)))
    for px, py in pts:
        cx, cy = X0 + px * XU, Y0 - py * YU
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
        s.append("<rect x='%.1f' y='%.1f' width='24' height='17' fill='#fff' opacity='0.85'/>" % (cx - 12, cy - 24))
        s.append(text(cx, cy - 10, n(py), 14))
    return svg_wrap(W, H, "".join(s), label)


def pair(a, b):
    return "(%s, %s)" % (n(a), n(b))


def F(*xs):
    return [Fr(x) for x in xs]


def jumps_e(a, k, N, ans):
    sg = "+" if k > 0 else "−"
    return ("From term 1 to term %d there are %d jumps of %s: %s %s %d × %s = %s %s %s = %s." % (
        N, N - 1, n(abs(k)), n(a), sg, N - 1, n(abs(k)), n(a), sg, n((N - 1) * abs(k)), n(ans)))


# ============================================================ set 1: growing and shrinking patterns
def set_grow(rnd):
    its = []
    # A: growing by the same amount
    for s0, k, wrong in [(6, 4, [26, 21, 24]), (15, 8, [55, 46, 54]), (120, 25, [245, 210, 315]),
                         (12500, 2500, [25000, 21000, 32500])]:
        xs = [s0 + i * k for i in range(5)]
        assert wrong[0] == xs[3] + 2 * k
        q = "What is the next term?<br><b>%s, ?</b>" % lstr(xs[:4])
        e = "The pattern grows by %s each time (%s + %s = %s). Next: %s + %s = %s." % (
            n(k), n(xs[0]), n(k), n(xs[1]), n(xs[3]), n(k), n(xs[4]))
        its.append((0, mcq(q, xs[4], wrong, e, rnd, n)))
    # B: shrinking by the same amount
    for s0, k, wrong in [(90, 6, [60, 78, 74]), (150, 12, [90, 126, 104]), (1000, 125, [375, 750, 525]),
                         (75, 5, [50, 65, 45])]:
        xs = [s0 - i * k for i in range(5)]
        assert wrong[0] == xs[3] - 2 * k and wrong[1] == xs[3] + k
        q = "What is the next term?<br><b>%s, ?</b>" % lstr(xs[:4])
        e = "The pattern shrinks by %s each time (%s − %s = %s). Next: %s − %s = %s." % (
            n(k), n(xs[0]), n(k), n(xs[1]), n(xs[3]), n(k), n(xs[4]))
        its.append((1, mcq(q, xs[4], wrong, e, rnd, n)))
    # C: check every step, not only the first one
    rows = [
        ("3, 6, 12, 24", 48, [27, 36, 30],
         "The jumps are 3, 6, 12, so the pattern does not add the same amount. Each term is 2 times the one before: "
         "24 × 2 = 48. (Adding the first jump, 24 + 3 = 27, only works for the first step.)"),
        ("1, 2, 4, 7, 11", 16, [12, 15, 22],
         "The jumps are 1, 2, 3, 4, so the next jump is 5: 11 + 5 = 16. (Adding the first jump gives 12.)"),
        ("2, 6, 18, 54", 162, [58, 108, 126],
         "Each term is 3 times the one before: 54 × 3 = 162. (Adding the first jump, 54 + 4 = 58, only works for the first step.)"),
        ("640, 320, 160, 80", 40, [160, 20, 70],
         "Each term is half of the one before (divide by 2): 80 ÷ 2 = 40. (Subtracting 320 like the first step does not work after that.)"),
    ]
    for lst, ans, wrong, e in rows:
        q = "What is the next term?<br><b>%s, ?</b>" % lst
        its.append((2, mcq(q, ans, wrong, e, rnd, n)))
    # D: missing term in the middle
    rows = [((8, 6), 1, [12, 16, 10]), ((100, -8), 2, [86, 82, 16]), ((35, 15), 2, [60, 70, 30]),
            ((4500, 500), 3, [6500, 7000, 1000])]
    for (a, k), m, wrong in rows:
        xs = [a + i * k for i in range(5)]
        ans = xs[m]
        shown = [n(x) if i != m else "?" for i, x in enumerate(xs)]
        q = "What is the missing term?<br><b>%s</b>" % ", ".join(shown)
        if k > 0:
            e = "The pattern grows by %s each time. The missing term is %s + %s = %s. Check: %s + %s = %s." % (
                n(k), n(xs[m - 1]), n(k), n(ans), n(ans), n(k), n(xs[m + 1]))
        else:
            e = "The pattern shrinks by %s each time. The missing term is %s − %s = %s. Check: %s − %s = %s." % (
                n(-k), n(xs[m - 1]), n(-k), n(ans), n(ans), n(-k), n(xs[m + 1]))
        if m == 1:
            e += " (The jump from %s to %s is %s, but the missing term sits halfway between them.)" % (
                n(xs[0]), n(xs[2]), n(xs[2] - xs[0]))
        its.append((3, mcq(q, ans, wrong, e, rnd, n)))
    # E: tile and craft-stick figures
    for kind in ["sticks_sq", "L", "grid", "house"]:
        a, b, c = [count(kind, k) for k in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = c + k
        assert ans == count(kind, 4)
        q = fig(pattern_svg(kind)) + "The pattern continues. How many %ss will Figure 4 need?" % w
        e = "Count each figure: %d, %d, %d. Each figure adds %d %ss. Figure 4: %d + %d = %d." % (a, b, c, k, w, c, k, ans)
        its.append((4, mcq(q, ans, [c + 1, 4 * a, c + 2 * k, c + a], e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Growing and shrinking patterns", "items": [i for _, i in its]}


# ============================================================ set 2: tables of values
def set_tables(rnd):
    its = []
    # A: a missing value in a table
    for a, k, m in [(5, 3, 3), (6, 4, 4), (12, 5, 2), (60, -5, 3), (9, 7, 4)]:
        vals = [a + i * k for i in range(5)]
        ans = vals[m]
        q = fig(tbl([1, 2, 3, 4, 5], vals, missing=m)) + "What is the missing term value?"
        if k > 0:
            e = "The term value goes up by %d each time. %s + %d = %s." % (k, n(vals[m - 1]), k, n(ans))
        else:
            e = "The term value goes down by %d each time. %s − %d = %s." % (-k, n(vals[m - 1]), -k, n(ans))
        cands = [ans + 1, ans + k, (m + 1) * abs(k), ans - 1, ans + 2 * k]
        its.append((0, mcq(q, ans, cands, e, rnd, n)))
    # B: a far term
    for a, k, N in [(5, 3, 8), (6, 4, 10), (100, -6, 10), (90, -8, 8), (2, 5, 12)]:
        vals = [a + i * k for i in range(4)]
        ans = a + (N - 1) * k
        q = (fig(tbl([1, 2, 3, 4, N], vals + [ans], missing=4)) +
             "The pattern continues in the same way. What is the term value for term number %d?" % N)
        e = jumps_e(a, k, N, ans) + " (%s is the value for term 5, the next term in the list.)" % n(vals[3] + k)
        cands = [vals[3] + k, a + N * k]
        cands += [N * k, N * a, a + (N - 2) * k] if k > 0 else [a + (N - 2) * k, a - N]
        its.append((1, mcq(q, ans, cands, e, rnd, n)))
    # C: from a picture to a table
    for kind, N in [("sticks_sq", 6), ("grid", 7), ("L", 8), ("cross", 6)]:
        a, b, c = [count(kind, k) for k in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = count(kind, N)
        assert ans == a + (N - 1) * k
        q = (fig(pattern_svg(kind)) + "Make a table of values: figure number and number of %ss. "
             "How many %ss will Figure %d need?" % (w, w, N))
        e = ("The table starts %d, %d, %d and goes up by %d. From Figure 1 to Figure %d there are %d jumps: "
             "%d + %d × %d = %d." % (a, b, c, k, N, N - 1, a, N - 1, k, ans))
        its.append((2, mcq(q, ans, [N * a, c + k, a + N * k, N * k], e, rnd, n)))
    # D: which term number has this value?
    for a, k, V, wrong in [(4, 3, 40, [40, 12, 14]), (5, 5, 75, [75, 14, 16]), (50, -4, 14, [14, 9, 36])]:
        vals = [a + i * k for i in range(4)]
        N = Fr(V - a, k) + 1
        assert N.denominator == 1
        q = fig(tbl([1, 2, 3, 4], vals)) + "The pattern continues. Which term number has a term value of %s?" % n(V)
        if k > 0:
            e = ("Count the jumps: %s − %s = %s, and %s ÷ %d = %s jumps after term 1. So it is term %s. "
                 "(%s is the term value, not the term number.)" % (
                     n(V), n(a), n(V - a), n(V - a), k, n(N - 1), n(N), n(V)))
        else:
            e = ("Count the jumps down: %s − %s = %s, and %s ÷ %d = %s jumps after term 1. So it is term %s. "
                 "(%s is the term value, not the term number.)" % (
                     n(a), n(V), n(a - V), n(a - V), -k, n(N - 1), n(N), n(V)))
        its.append((3, mcq(q, N, wrong, e, rnd, n)))
    # E: which table matches a rule in words
    for start, k in [(7, 4), (20, 5), (50, -6)]:
        right = lstr([start + i * k for i in range(4)])
        if k > 0:
            rule = "Start at %d and add %d each time." % (start, k)
            wrong = [lstr([k + i * start for i in range(4)]), lstr([start + (i + 1) * k for i in range(4)]),
                     lstr([start + i * (k + 1) for i in range(4)])]
            e = "Start at %d and add %d: %s. (Swapping gives %s, which starts at %d and adds %d.)" % (
                start, k, right, wrong[0], k, start)
        else:
            rule = "Start at %d and subtract %d each time." % (start, -k)
            wrong = [lstr([start - i * k for i in range(4)]), lstr([start + (i + 1) * k for i in range(4)]),
                     lstr([start + i * (k + 1) for i in range(4)])]
            e = "Start at %d and subtract %d: %s. The first term is the start number, %d." % (start, -k, right, start)
        q = "Which list follows the pattern rule?<br><b>%s</b>" % rule
        its.append((4, mcq(q, right, wrong, e, rnd)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Tables of values", "items": [i for _, i in its]}


# ============================================================ set 3: pattern rules
def set_rules(rnd):
    its = []
    # A: describe the pattern in words (a wrong rule that fits only the first step)
    rows = [
        ("4, 8, 12, 16", "Start at 4 and add 4 each time.",
         ["Start at 4 and multiply by 2 each time.", "Start at 8 and add 4 each time.", "Start at 4 and add 8 each time."],
         "Each term is 4 more than the one before. “Multiply by 2” works for 4 → 8 but not for 8 → 12."),
        ("3, 9, 15, 21", "Start at 3 and add 6 each time.",
         ["Start at 3 and multiply by 3 each time.", "Start at 6 and add 3 each time.", "Start at 9 and add 6 each time."],
         "Each term is 6 more than the one before. “Multiply by 3” works for 3 → 9 but not for 9 → 15."),
        ("2, 4, 8, 16", "Start at 2 and multiply by 2 each time.",
         ["Start at 2 and add 2 each time.", "Start at 4 and multiply by 2 each time.", "Start at 2 and add 4 each time."],
         "Each term is 2 times the one before: 2 × 2 = 4, 4 × 2 = 8, 8 × 2 = 16. “Add 2” works only for the first step."),
        ("96, 48, 24, 12", "Start at 96 and divide by 2 each time.",
         ["Start at 96 and subtract 48 each time.", "Start at 96 and subtract 24 each time.", "Start at 48 and divide by 2 each time."],
         "Each term is half of the one before: 96 ÷ 2 = 48, 48 ÷ 2 = 24, 24 ÷ 2 = 12. “Subtract 48” works only for the first step."),
        ("100, 93, 86, 79", "Start at 100 and subtract 7 each time.",
         ["Start at 100 and add 7 each time.", "Start at 93 and subtract 7 each time.", "Start at 79 and subtract 7 each time."],
         "The first term is 100, and each term is 7 less than the one before: 100 − 7 = 93, 93 − 7 = 86."),
    ]
    for lst, good, bad, e in rows:
        q = "Which pattern rule describes this pattern?<br><b>%s, …</b>" % lst
        its.append((0, mcq(q, good, bad, e, rnd)))
    # B: a rule that uses the term number
    for a, b in [(3, 1), (4, 3), (2, 5), (5, -2), (10, 5)]:
        vals = [a * i + b for i in range(1, 5)]
        f = vals[0]

        def R(m, c):
            return "term number × %d" % m + ("" if c == 0 else (" + %d" % c if c > 0 else " − %d" % -c))
        good = R(a, b)
        bad = ["term number + %d" % (f - 1), R(f, 0), R(a, f)]
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which rule gives the term value from the term number?"
        e = ("The term value goes up by %d, so multiply the term number by %d. Term 1: 1 × %d = %d, and the value is %d, "
             "so %s. Check term 4: 4 × %d %s %d = %d. (A rule must work for every term, not only term 1.)" % (
                 a, a, a, a, f, ("add %d" % b) if b > 0 else ("subtract %d" % -b), a, "+" if b > 0 else "−", abs(b),
                 vals[3]))
        its.append((1, mcq(q, good, bad, e, rnd)))
    # C: make and justify a prediction: which number is in the pattern?
    for a, k, good, bad in [(4, 3, 46, [45, 47, 48]), (5, 4, 41, [40, 42, 44]), (2, 5, 52, [50, 55, 53]),
                            (6, 6, 84, [64, 86, 76])]:
        assert (good - a) % k == 0 and all((x - a) % k for x in bad)
        q = "The pattern %s, … continues. Which number will be in the pattern?" % lstr([a + i * k for i in range(4)])
        e = ("Every term is %d plus a number of jumps of %d. %d − %d = %d, and %d ÷ %d = %d jumps, so %d is term %d. "
             "For the other numbers, the difference from %d is not a multiple of %d." % (
                 a, k, good, a, good - a, good - a, k, (good - a) // k, good, (good - a) // k + 1, a, k))
        its.append((2, mcq(q, good, bad, e, rnd, n)))
    # D: repeating patterns
    q = ("Emma strings beads in a repeating pattern: <b>red, blue, green, yellow, red, blue, green, yellow, …</b> "
         "What colour is the 30th bead?")
    assert 30 % 4 == 2
    e = ("The core has 4 beads. 30 ÷ 4 = 7 R 2, so after 7 full cores the 30th bead is the 2nd bead of the core: blue.")
    its.append((3, mcq(q, "blue", ["red", "green", "yellow"], e, rnd)))
    q = ("Owen draws shapes in a repeating pattern: <b>circle, square, triangle, star, circle, square, …</b> "
         "What is the 43rd shape?")
    assert 43 % 4 == 3
    e = "The core has 4 shapes. 43 ÷ 4 = 10 R 3, so the 43rd shape is the 3rd shape of the core: triangle."
    its.append((3, mcq(q, "triangle", ["circle", "square", "star"], e, rnd)))
    q = ("A bracelet repeats <b>red, white, white, red, white, white, …</b> In which position is the 10th red bead?")
    assert 1 + 9 * 3 == 28
    e = ("The red beads are in positions 1, 4, 7, … (start at 1 and add 3). The 10th red bead is 9 jumps after the first: "
         "1 + 9 × 3 = 28. (10 × 3 = 30 counts one jump too many.)")
    its.append((3, mcq(q, "position 28", ["position 30", "position 27", "position 10"], e, rnd)))
    # E: use the rule to find a far term
    for s0, k, N, wrong in [(12, 5, 10, [62, 50, 17]), (8, 7, 20, [148, 140, 160]), (200, -15, 12, [20, 180, 185])]:
        ans = s0 + (N - 1) * k
        rule = ("Start at %d and add %d each time." % (s0, k)) if k > 0 else ("Start at %d and subtract %d each time." % (s0, -k))
        q = "Here is a pattern rule: <b>%s</b> What is the term value for term number %d?" % (rule, N)
        e = jumps_e(s0, k, N, ans) + " (Term 1 is the start number, so there are only %d jumps.)" % (N - 1)
        its.append((4, mcq(q, ans, wrong, e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Pattern rules and predictions", "items": [i for _, i in its]}


# ============================================================ set 4: decimal patterns
def set_decimals(rnd):
    its = []
    # A: next term with tenths and hundredths
    rows = [
        ("0.25, 0.5, 0.75", "0.25", 1, ["0.1", "1.25", "0.5"],
         "The pattern adds 0.25 each time. 0.75 + 0.25 = 1. (75 hundredths + 25 hundredths = 100 hundredths = 1 whole, not 0.100.)"),
        ("1.5, 2, 2.5, 3", "0.5", "3.5", ["4", "3.05", "4.5"],
         "The pattern adds 0.5 (five tenths) each time. 3 + 0.5 = 3.5. (3.05 adds 5 hundredths, not 5 tenths.)"),
        ("0.3, 0.6, 0.9", "0.3", "1.2", ["0.12", "1.5", "0.93"],
         "The pattern adds 0.3 each time. 0.9 + 0.3 = 1.2, because 9 tenths + 3 tenths = 12 tenths = 1 and 2 tenths. (0.12 is twelve hundredths.)"),
        ("2.45, 2.55, 2.65", "0.1", "2.75", ["2.66", "3.65", "2.85"],
         "The pattern adds 0.1 (one tenth) each time: the tenths digit goes up by 1. 2.65 + 0.1 = 2.75. (2.66 adds one hundredth.)"),
        ("6.3, 5.9, 5.5", "-0.4", "5.1", ["4.7", "5.4", "5.9"],
         "The pattern subtracts 0.4 each time. 5.5 − 0.4 = 5.1. (5.9 adds instead of subtracting.)"),
    ]
    for lst, k, ans, wrong, e in rows:
        xs = [Fr(x) for x in lst.split(", ")]
        assert all(xs[i + 1] - xs[i] == Fr(k) for i in range(len(xs) - 1)) and xs[-1] + Fr(k) == Fr(ans)
        q = "What is the next term?<br><b>%s, ?</b>" % lst
        its.append((0, mcq(q, Fr(ans), [Fr(w) for w in wrong], e, rnd, n)))
    # B: counting by 0.25, 0.5 and 0.75
    q = "Count by 0.75: <b>0.75, 1.5, 2.25, ?</b>"
    assert Fr("2.25") + Fr("0.75") == 3
    e = "2.25 + 0.75 = 3, because 25 hundredths + 75 hundredths = 100 hundredths = 1 whole. (2.1 comes from writing 2.100: the 100 hundredths are 1 whole, so they go to the ones.)"
    its.append((1, mcq(q, 3, F("3.75", "2.1", "3.25"), e, rnd, n)))
    q = "The pattern 0.5, 1, 1.5, 2, … continues. What is the 10th term?"
    assert Fr("0.5") * 10 == 5
    e = "Each term is the term number × 0.5 (half of the term number). Term 10: 10 × 0.5 = 5. (4.5 is term 9.)"
    its.append((1, mcq(q, 5, F("4.5", "5.5", "10"), e, rnd, n)))
    q = "The pattern 0.25, 0.5, 0.75, 1, … continues. What is the 8th term?"
    e = "Each term is the term number × 0.25 (a quarter). Term 8: 8 × 0.25 = 2. (1.25 is term 5, the next term in the list.)"
    its.append((1, mcq(q, 2, F("1.75", "2.25", "1.25"), e, rnd, n)))
    q = "What is the next term?<br><b>3, 2.75, 2.5, 2.25, ?</b>"
    e = "The pattern subtracts 0.25 each time. 2.25 − 0.25 = 2. (1.75 subtracts twice; 2.05 subtracts 0.2.)"
    its.append((1, mcq(q, 2, F("1.75", "2.5", "2.05"), e, rnd, n)))
    # C: tables of values with decimals
    rows = [
        ([1, 2, 3, 4], ["0.4", "0.8", "1.2", "1.6"], 2, ["0.12", "1.1", "1.4"],
         "The value goes up by 0.4 each time. 0.8 + 0.4 = 1.2. Check: 1.2 + 0.4 = 1.6. (0.12 is twelve hundredths.)"),
        ([1, 2, 3, 4], ["2.5", "5", "7.5", "10"], 3, ["12.5", "9.1", "10.5"],
         "The value goes up by 2.5 each time. 7.5 + 2.5 = 10, because 0.5 + 0.5 = 1 whole. (9.10 forgets to regroup the 10 tenths.)"),
        ([1, 2, 3, 4, 10], ["0.05", "0.1", "0.15", "0.2", "0.5"], 4, ["0.25", "0.55", "5"],
         "Each term is the term number × 0.05 (5 hundredths). Term 10: 10 × 0.05 = 0.5. (0.25 is term 5.)"),
        ([1, 2, 3, 4, 8], ["10", "9.5", "9", "8.5", "6.5"], 4, ["6", "8", "7"],
         "The value goes down by 0.5 each time. From term 1 to term 8 there are 7 jumps: 7 × 0.5 = 3.5, and 10 − 3.5 = 6.5. (6 uses 8 jumps.)"),
    ]
    for nums, vals, m, wrong, e in rows:
        vals = [Fr(v) for v in vals]
        d = vals[1] - vals[0]
        if nums[-1] == 4:
            assert all(vals[i + 1] - vals[i] == d for i in range(3))
        else:
            assert all(vals[i] == vals[0] + (nums[i] - 1) * d for i in range(5))
        q = fig(tbl(nums, vals, missing=m)) + (
            "What is the missing term value?" if nums[-1] == 4 else
            "The pattern continues in the same way. What is the term value for term number %d?" % nums[-1])
        its.append((2, mcq(q, vals[m], [Fr(w) for w in wrong], e, rnd, n)))
    # D: rules for decimal patterns
    rows = [
        ("0.5, 1.25, 2, 2.75", "Start at 0.5 and add 0.75 each time.",
         ["Start at 0.75 and add 0.5 each time.", "Start at 0.5 and add 0.25 each time.", "Start at 1.25 and add 0.75 each time."],
         "0.5 + 0.75 = 1.25, 1.25 + 0.75 = 2, 2 + 0.75 = 2.75. The first term, 0.5, is the start."),
        ("3.2, 3.4, 3.6, 3.8", "Start at 3.2 and add 0.2 each time.",
         ["Start at 3.2 and add 2 each time.", "Start at 3.2 and add 0.02 each time.", "Start at 3.4 and add 0.2 each time."],
         "The tenths digit goes up by 2 each time, so the pattern adds 0.2 (2 tenths): 3.2 + 0.2 = 3.4."),
        ("5, 4.75, 4.5, 4.25", "Start at 5 and subtract 0.25 each time.",
         ["Start at 5 and add 0.25 each time.", "Start at 5 and subtract 0.75 each time.", "Start at 4.75 and subtract 0.25 each time."],
         "5 − 0.25 = 4.75, 4.75 − 0.25 = 4.5, 4.5 − 0.25 = 4.25. The terms get smaller, so the rule subtracts."),
        ("0.25, 0.5, 1, 2", "Start at 0.25 and multiply by 2 each time.",
         ["Start at 0.25 and add 0.25 each time.", "Start at 0.5 and multiply by 2 each time.", "Start at 0.25 and add 0.5 each time."],
         "0.25 × 2 = 0.5, 0.5 × 2 = 1, 1 × 2 = 2. “Add 0.25” works only for the first step (0.5 + 0.25 = 0.75, not 1)."),
    ]
    for lst, good, bad, e in rows:
        q = "Which pattern rule describes this pattern?<br><b>%s, …</b>" % lst
        its.append((3, mcq(q, good, bad, e, rnd)))
    # E: whole numbers and decimals (multiply or divide by 10)
    q = "What is the next term?<br><b>0.03, 0.3, 3, 30, ?</b>"
    e = "Each term is 10 times the one before: the digits move one place to the left. 30 × 10 = 300. (33 adds 3.)"
    its.append((4, mcq(q, 300, F("33", "3000", "60"), e, rnd, n)))
    q = "What is the next term?<br><b>7000, 700, 70, 7, ?</b>"
    e = "Each term is the one before ÷ 10: the digits move one place to the right. 7 ÷ 10 = 0.7. (0.07 divides by 100.)"
    its.append((4, mcq(q, Fr("0.7"), F("0.07", "6", "70"), e, rnd, n)))
    q = "What is the next term?<br><b>4.97, 4.98, 4.99, ?</b>"
    e = "The pattern adds 0.01 each time. 4.99 + 0.01 = 5, because 99 hundredths + 1 hundredth = 1 whole. (4.1 comes from writing 4.100: the 100 hundredths are 1 whole, so they go to the ones.)"
    its.append((4, mcq(q, 5, F("4.1", "5.1", "4.9"), e, rnd, n)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Decimal patterns (0.25, 0.5, 0.75)", "items": [i for _, i in its]}


# ============================================================ set 5: graphs and predictions (word problems)
def set_words(rnd):
    its = []

    def add(q, ans, cands, e, disp=None):
        its.append(mcq(q, ans, cands, e, rnd, disp))

    unit = lambda u: (lambda v: n(v) + NBSP + u)
    dol = lambda v: money(v, False)
    # graphs
    g1 = graph_svg([(i, 4 * i + 4) for i in range(1, 5)], xl="Week", yl="Dollars saved",
                   label="graph of savings: 8, 12, 16, 20 dollars")
    assert 4 * 7 + 4 == 32
    add(fig(g1) + "The graph shows how much money Liam has saved after each week. The pattern continues. "
        "How much will he have after week 7?", 32, [24, 28, 56],
        "The points go up $4 each week: 8, 12, 16, 20, 24, 28, 32. After week 7 he has $32. (7 × 8 = 56 multiplies the first value.)",
        dol)
    assert 4 * 11 + 4 == 48
    add(fig(g1) + "Liam keeps saving in the same way. In which week will he have $48 saved?", "week 11",
        ["week 48", "week 12", "week 10"],
        "From $20 in week 4, he needs 48 − 20 = $28 more. 28 ÷ 4 = 7 more weeks: 4 + 7 = week 11. (48 is the number of dollars, not the week.)")
    g2 = graph_svg([(i, 3 * i - 1) for i in range(1, 5)], xl="Day", yl="Height (cm)",
                   label="graph of a plant’s height: 2, 5, 8, 11 cm")
    assert 3 * 8 - 1 == 23
    add(fig(g2) + "Zoe’s bean plant grows the same amount each day. How tall will it be on day 8?", 23, [14, 26, 16],
        "It grows 3 cm a day. From day 1 to day 8 there are 7 jumps: 2 + 7 × 3 = 23 cm. (14 cm is day 5, the next point.)",
        unit("cm"))
    add(fig(g2) + "Each point is (day, height). Which point will come next on the graph?", pair(5, 14),
        [pair(14, 5), pair(5, 13), pair(6, 14)],
        "The next day is day 5. The height goes up 3 cm: 11 + 3 = 14. The point is (5, 14). (In (14, 5) the numbers are swapped: the day comes first.)")
    g3 = graph_svg([(i, 33 - 3 * i) for i in range(1, 5)], xl="Day", yl="Snow (cm)",
                   label="graph of snow depth: 30, 27, 24, 21 cm")
    assert 33 - 3 * 7 == 12
    add(fig(g3) + "In March the snow in Nathan’s backyard melts by the same amount each day. "
        "On which day will the snow be 12 cm deep?", "day 7", ["day 12", "day 6", "day 8"],
        "The snow goes down 3 cm a day: 30, 27, 24, 21, 18, 15, 12. That is day 7. (12 is the depth, not the day.)")
    g4 = graph_svg([(i, 30 - 5 * i) for i in range(1, 5)], xl="Day", yl="Pages left",
                   label="graph of pages left: 25, 20, 15, 10")
    add(fig(g4) + "The graph shows the pages Ava has left to read in her book at the end of each day. "
        "Which pattern rule matches the graph?", "Start at 25 and subtract 5 each day.",
        ["Start at 25 and add 5 each day.", "Start at 30 and subtract 5 each day.", "Start at 25 and subtract 10 each day."],
        "The first point is 25, and each point is 5 lower: 25, 20, 15, 10. So start at 25 and subtract 5 each day.")
    # word problems
    assert 2 * 10 + 2 == 22
    add("Square tables are pushed together in a row for a class party. 1 table seats 4 students, 2 tables seat 6, "
        "and 3 tables seat 8. How many students can sit at 10 tables?", 22, [40, 20, 24],
        "Each new table adds 2 seats. From 1 table to 10 tables there are 9 jumps: 4 + 9 × 2 = 22. "
        "(10 × 4 = 40 counts seats lost where the tables touch.)", lambda v: "%d students" % v)
    assert 20 + 5 * 9 == 65
    add("Priya has $20 in her piggy bank. She saves $5 each week. How much will she have after 9 weeks?", 65, [45, 70, 60],
        "She adds 9 × $5 = $45 to her $20: 20 + 45 = $65. ($45 forgets the $20 she started with.)", dol)
    assert Fr("1.5") + 5 * Fr("0.5") == 4
    add("To train for the Terry Fox Run, Maya runs 1.5 km in week 1. Each week she runs 0.5 km more. How far does she run in week 6?",
        4, F("4.5", "3", "3.5"),
        "From week 1 to week 6 there are 5 jumps: 5 × 0.5 = 2.5 km. 1.5 + 2.5 = 4 km. (4.5 km uses 6 jumps.)", unit("km"))
    assert 20 - 6 * Fr("1.5") == 11
    add("A candle is 20 cm tall. It burns down 1.5 cm each hour. How tall is it after 6 hours?", 11, F("9", "29", "12.5"),
        "6 × 1.5 = 9 cm burns away. 20 − 9 = 11 cm. (9 cm is the part that burned.)", unit("cm"))
    assert Fr("0.25") * 12 == 3
    add("Ava puts a quarter (25¢) in a jar every day. How much money is in the jar after 12 days?", 3, F("2.75", "3.25", "300"),
        "Count by 0.25: 4 quarters make $1, so 12 quarters make $3.00. 12 × 0.25 = 3. ($300 forgets that 25¢ is $0.25.)", money)
    assert 9 - 4 * Fr("1.5") == 3
    add("On a winter afternoon it is 9" + NBSP + "°C at 3 p.m. The temperature falls 1.5" + NBSP +
        "°C each hour. What is the temperature at 7 p.m.?", 3, F("6", "15", "4.5"),
        "3 p.m. to 7 p.m. is 4 hours. 4 × 1.5 = 6 degrees. 9 − 6 = 3" + NBSP + "°C. (15" + NBSP + "°C adds instead of subtracting.)",
        unit("°C"))
    assert 12 + 9 * Fr("1.5") == Fr("25.5")
    add("One paper cup is 12 cm tall. Each extra cup on the stack adds 1.5 cm. How tall is a stack of 10 cups?",
        Fr("25.5"), F("27", "120", "15"),
        "The first cup is 12 cm. There are 9 extra cups: 9 × 1.5 = 13.5 cm. 12 + 13.5 = 25.5 cm. (27 cm counts 10 extra cups.)",
        unit("cm"))
    assert 3 * 10 + 1 == 31
    add("Lucas makes a row of squares with craft sticks: 4 sticks, 7 sticks, 10 sticks, … Which figure uses 31 sticks?",
        "Figure 10", ["Figure 31", "Figure 11", "Figure 9"],
        "The sticks go up by 3. 31 − 4 = 27, and 27 ÷ 3 = 9 jumps after Figure 1, so it is Figure 10. "
        "(31 is the number of sticks, not the figure number.)")
    assert 15 + 8 * 8 == 79
    add("Swimming lessons cost $15 to sign up plus $8 for each lesson. Hana pays $79 in total. How many lessons does she take?",
        "8 lessons", ["9 lessons", "64 lessons", "7 lessons"],
        "Take away the $15 first: 79 − 15 = 64. Then 64 ÷ 8 = 8 lessons. Check: 15 + 8 × 8 = $79. (64 is the cost of the lessons.)")
    assert 120 - 6 * 12 == 48
    add("Mei has 120 hockey cards. She gives away 6 cards each week. After how many weeks will she have 48 cards left?",
        "12 weeks", ["8 weeks", "20 weeks", "48 weeks"],
        "She gives away 120 − 48 = 72 cards. 72 ÷ 6 = 12 weeks. (48 ÷ 6 = 8 uses the cards left, not the cards given away.)")
    assert 40 + 6 * Fr("2.5") == 55
    add("A sap tank on a maple farm has 40 L of sap at 8 a.m. Sap drips in at 2.5 L each hour. How much sap is in the tank at 2 p.m.?",
        55, F("57.5", "15", "52.5"),
        "8 a.m. to 2 p.m. is 6 hours. 6 × 2.5 = 15 L. 40 + 15 = 55 L. (15 L forgets the 40 L already in the tank.)", unit("L"))
    assert 10 + 4 * Fr("2.5") == 20
    add("During a snowstorm, there is 10 cm of snow on the ground at noon. Snow piles up 2.5 cm each hour. "
        "How deep is the snow at 4 p.m.?", 20, F("22.5", "50", "12.5"),
        "Noon to 4 p.m. is 4 hours. 4 × 2.5 = 10 cm. 10 + 10 = 20 cm. ((10 + 2.5) × 4 = 50 adds the starting snow every hour.)",
        unit("cm"))
    assert 2 * 15 + 1 == 31
    add("Benjamin builds a row of triangles with toothpicks. 1 triangle uses 3, 2 triangles use 5 and 3 triangles use 7. "
        "How many toothpicks does he need for 15 triangles?", 31, [45, 29, 33],
        "Each new triangle adds 2 toothpicks. From 1 to 15 triangles there are 14 jumps: 3 + 14 × 2 = 31. "
        "(15 × 3 = 45 counts the shared sides twice.)", lambda v: "%d toothpicks" % v)
    assert 30 % 7 == 2
    add("Today is Monday. Days of the week repeat every 7 days. What day of the week will it be 30 days from today?",
        "Wednesday", ["Tuesday", "Thursday", "Monday"],
        "30 ÷ 7 = 4 R 2. After 4 full weeks (28 days) it is Monday again. 2 more days: Wednesday.")
    rnd.shuffle(its)
    return {"title": "Graphs of patterns and predictions", "items": its}


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
    g = graph_svg([(i, 3 * i + 1) for i in range(1, 5)], label="graph of a growing pattern: 4, 7, 10, 13")
    return (
        "<h2>Growing and shrinking patterns</h2>"
        "<p>A <b>growing</b> pattern gets bigger and a <b>shrinking</b> pattern gets smaller. Find the change from each term "
        "to the next. Check every step, not only the first one.</p>" +
        ex("Example 1", "95, 88, 81, 74, ?", "Each step subtracts 7. 74 − 7 = 67.", "67") +
        "<h2>Tables of values</h2>"
        "<p>Each number in a pattern is a <b>term</b>. Its place is the <b>term number</b> (1, 2, 3 …), and the number "
        "itself is the <b>term value</b>. A table of values shows both.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sticks_sq") +
        "<figcaption>4, 7, 10 craft sticks: each new square adds 3 sticks, because it shares a side.</figcaption></figure>"
        "<figure class='sn-fig'>" + t +
        "<figcaption>From term 1 to term 10 there are 9 jumps of 3: 4 + 9 × 3 = 31.</figcaption></figure>"
        "<h2>Pattern rules</h2>"
        "<p>A pattern rule can say how to get the next term (<b>start at 4 and add 3 each time</b>) or how to get a term "
        "from its term number (<b>term number × 3 + 1</b>). Both rules give 4, 7, 10, 13 …</p>" +
        ex("Example 2", "Which term number has a term value of 40 in 4, 7, 10, 13, …?",
           "40 − 4 = 36, and 36 ÷ 3 = 12 jumps after term 1. So it is term 13. Check: 13 × 3 + 1 = 40.", "term number 13") +
        "<h2>Decimal patterns</h2>"
        "<p>Count by 0.25, 0.5 or 0.75 like counting by quarters, halves or three-quarters. When the hundredths make "
        "100, they make 1 whole.</p>" +
        ex("Example 3", "0.25, 0.5, 0.75, ?", "0.75 + 0.25: 75 hundredths + 25 hundredths = 100 hundredths = 1.", "1") +
        "<h2>Graphs of patterns</h2>"
        "<p>Plot each term as a point (term number, term value). In a pattern that adds the same amount, the points lie "
        "in a straight line, so you can predict the next point.</p>"
        "<figure class='sn-fig'>" + g +
        "<figcaption>4, 7, 10, 13: each step right goes up 3. The next point is (5, 16).</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using only the first step: 3, 6, 12, 24 is “add 3”", "Check every step. 3, 6, 12, 24 doubles, so the next term is 48"],
            ["Mixing up the term number and the term value", "The term number is the place; the term value is the number in that place"],
            ["Term 10 = term 1 + 10 jumps", "From term 1 to term 10 there are 9 jumps"],
            ["0.9 + 0.3 = 0.12", "9 tenths + 3 tenths = 12 tenths = 1.2"],
            ["Swapping a point: (16, 5)", "Write the term number first: (5, 16)"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about patterns in the Ontario math curriculum?",
     "a": "In Grade 5 (Algebra, C1), students extend growing, shrinking and repeating patterns, find pattern rules, show patterns in tables of values and graphs, and make predictions. They also make patterns with decimal tenths and hundredths, such as 0.25, 0.5, 0.75."},
    {"q": "What is the difference between a term number and a term value?",
     "a": "The term number is the place in the pattern (1st, 2nd, 3rd …) and the term value is the number in that place. In 5, 8, 11, 14, term number 3 has a term value of 11."},
    {"q": "How do you find the 10th term of a pattern like 4, 7, 10, 13?",
     "a": "The pattern adds 3 each time, and from term 1 to term 10 there are 9 jumps. 4 + 9 × 3 = 31, so the 10th term is 31."},
    {"q": "How can I help my child with decimal patterns at home?",
     "a": "Count by quarters with money: 25¢, 50¢, 75¢, $1.00 is the same as 0.25, 0.5, 0.75, 1. Then try counting by 0.5 or 0.75 and talk about what happens when the hundredths reach 100."},
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
    rnd = random.Random(45811)
    sets = [set_grow(rnd), set_tables(rnd), set_rules(rnd), set_decimals(rnd), set_words(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "patterns", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Patterns: Pattern Rules, Tables of Values and Decimal Patterns",
        "seo_title": "Grade 5 Patterns Math Worksheets: Pattern Rules, Tables of Values and Graphs (Free, Answer Key)",
        "short_title": "Patterns",
        "domain": "Algebra",
        "standard_code": "Grade 5: C1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating, growing, and shrinking patterns",
        "meta_desc": "Free Grade 5 math worksheets on patterns for the Ontario curriculum: growing, shrinking and repeating patterns, tables of values, pattern rules, decimal patterns with 0.25, 0.5 and 0.75, and graphs for making predictions. 100 questions with an answer key.",
        "key_big": "From term 1 to term 10 there are 9 jumps. In 4, 7, 10, 13 …, term 10 is 4 + 9 × 3 = 31.",
        "key_sub": "The term number is the place; the term value is the number in that place. Check every step of a pattern, not only the first one. In decimal patterns, 100 hundredths make 1 whole: 0.75 + 0.25 = 1.",
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
