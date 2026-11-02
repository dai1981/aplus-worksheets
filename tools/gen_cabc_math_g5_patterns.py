# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Pattern rules (BC Mathematics Curriculum, Grade 5: Patterning)
  python3 tools/gen_cabc_math_g5_patterns.py
Rules for increasing and decreasing patterns with words (start at 4 and add 3 each time), tables of values,
symbols (□ × 3 + 1, where □ is the term number) and variables (3n + 1), and predicting terms in BC word problems.
Wrong answers come from real student mistakes: using only the first step, mixing up the term number and the term
value, counting n jumps instead of n − 1, reading 3n as the two-digit number 3n, adding before multiplying,
using the first term as the number added, and undoing a rule the wrong way.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English, SI number spacing.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
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
NBSP = "\u00a0"
M = "\u2212"


# ------------------------------------------------------------ numbers
def n(v):
    """BC style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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



BOX = "□"


def lin(a, b, v="n"):
    """Expression text: 3n + 1, 4n − 3, 54 − 4n (a < 0)."""
    if a < 0:
        return "%s %s %s%s" % (n(b), M, n(-a), v)
    return "%s%s" % (n(a), v) + ("" if b == 0 else (" + %s" % n(b) if b > 0 else " %s %s" % (M, n(-b))))


def boxr(a, b):
    """Symbol rule text: □ × 3 + 1."""
    return "%s × %s" % (BOX, n(a)) + ("" if b == 0 else (" + %s" % n(b) if b > 0 else " %s %s" % (M, n(-b))))


def addsub(b):
    return ("+ %s" % n(b)) if b > 0 else ("%s %s" % (M, n(-b)))


def finish(its, title, rnd):
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": title, "items": [i for _, i in its]}


# ============================================================ set 1: pattern rules in words
def set_words_rules(rnd):
    its = []
    # E (easiest): which list follows a rule in words
    for start, k in [(6, 4), (25, 5), (90, -8)]:
        right = lstr([start + i * k for i in range(4)])
        if k > 0:
            rule = "Start at %d and add %d each time." % (start, k)
            wrong = [lstr([k + i * start for i in range(4)]), lstr([start + (i + 1) * k for i in range(4)]),
                     lstr([start + i * (k + 1) for i in range(4)])]
            e = "Start at %d, then add %d: %s. (%s swaps the numbers: it starts at %d and adds %d.)" % (
                start, k, right, wrong[0], k, start)
        else:
            rule = "Start at %d and subtract %d each time." % (start, -k)
            wrong = [lstr([start - i * k for i in range(4)]), lstr([start + (i + 1) * k for i in range(4)]),
                     lstr([start + i * (k - 1) for i in range(4)])]
            e = ("Start at %d, then subtract %d: %s. The first term is the start number, %d. "
                 "(%s adds instead of subtracting.)" % (start, -k, right, start, wrong[0]))
        q = "Which list follows the pattern rule?<br><b>%s</b>" % rule
        its.append((0, mcq(q, right, wrong, e, rnd)))
    # A: which rule describes the pattern (a wrong rule fits only the first step)
    rows = [
        ("5, 10, 15, 20", "Start at 5 and add 5 each time.",
         ["Start at 5 and multiply by 2 each time.", "Start at 10 and add 5 each time.", "Start at 5 and add 10 each time."],
         "Each term is 5 more than the one before. “Multiply by 2” works for 5 → 10, but not for 10 → 15."),
        ("6, 18, 30, 42", "Start at 6 and add 12 each time.",
         ["Start at 6 and multiply by 3 each time.", "Start at 18 and add 12 each time.", "Start at 12 and add 6 each time."],
         "Each term is 12 more than the one before. “Multiply by 3” works for 6 → 18, but 18 × 3 is 54, not 30."),
        ("3, 6, 12, 24", "Start at 3 and multiply by 2 each time.",
         ["Start at 3 and add 3 each time.", "Start at 6 and multiply by 2 each time.", "Start at 3 and add 6 each time."],
         "Each term is 2 times the one before: 3 × 2 = 6, 6 × 2 = 12, 12 × 2 = 24. “Add 3” works only for the first step."),
        ("400, 200, 100, 50", "Start at 400 and divide by 2 each time.",
         ["Start at 400 and subtract 200 each time.", "Start at 200 and divide by 2 each time.", "Start at 400 and subtract 100 each time."],
         "Each term is half of the one before: 400 ÷ 2 = 200, 200 ÷ 2 = 100, 100 ÷ 2 = 50. “Subtract 200” works only for the first step."),
        ("250, 235, 220, 205", "Start at 250 and subtract 15 each time.",
         ["Start at 250 and add 15 each time.", "Start at 235 and subtract 15 each time.", "Start at 250 and subtract 25 each time."],
         "The terms get smaller, so the rule subtracts. 250 − 15 = 235, 235 − 15 = 220. The start is the first term, 250."),
    ]
    for lst, good, bad, e in rows:
        q = "Which pattern rule describes this pattern?<br><b>%s, …</b>" % lst
        its.append((1, mcq(q, good, bad, e, rnd)))
    # D: missing term in the middle
    rows = [((15, 7), 1, [14, 29, 23]), ((500, -25), 2, [425, 50, 445]), ((12000, 1500), 3, [16000, 3000, 19500])]
    for (a, k), m, wrong in rows:
        xs = [a + i * k for i in range(5)]
        ans = xs[m]
        shown = [n(x) if i != m else "?" for i, x in enumerate(xs)]
        q = "What is the missing term?<br><b>%s</b>" % ", ".join(shown)
        sg = "adds" if k > 0 else "subtracts"
        op = "+" if k > 0 else "−"
        e = "The rule %s %s each time. The missing term is %s %s %s = %s. Check: %s %s %s = %s." % (
            sg, n(abs(k)), n(xs[m - 1]), op, n(abs(k)), n(ans), n(ans), op, n(abs(k)), n(xs[m + 1]))
        e += " (The gap from %s to %s is 2 jumps, not 1.)" % (n(xs[m - 1]), n(xs[m + 1]))
        its.append((2, mcq(q, ans, wrong, e, rnd, n)))
    # B: use a rule in words to find a later term
    for a, k, N in [(8, 6, 6), (25, 9, 8), (300, -20, 7), (1200, 150, 10), (95, -7, 9)]:
        ans = a + (N - 1) * k
        if k > 0:
            rule = "starts at %s and adds %s each time" % (n(a), n(k))
        else:
            rule = "starts at %s and subtracts %s each time" % (n(a), n(-k))
        q = "A pattern %s. What is the %s term?" % (rule, {6: "6th", 7: "7th", 8: "8th", 9: "9th", 10: "10th"}[N])
        e = jumps_e(a, k, N, ans) + " (Using %d jumps gives the %s term instead.)" % (
            N, {6: "7th", 7: "8th", 8: "9th", 9: "10th", 10: "11th"}[N])
        cands = [a + N * k, a + (N - 2) * k, N * abs(k), N * a]
        its.append((3, mcq(q, ans, cands, e, rnd, n)))
    # C: check every step, not only the first one
    rows = [
        ("2, 4, 8, 16", 32, [18, 24, 20],
         "The jumps are 2, 4, 8, so the rule is not “add 2”. Each term is 2 times the one before: 16 × 2 = 32. "
         "(16 + 2 = 18 uses only the first step.)"),
        ("5, 15, 45, 135", 405, [145, 225, 270],
         "Each term is 3 times the one before: 135 × 3 = 405. (135 + 10 = 145 uses only the first step.)"),
        ("1, 3, 6, 10, 15", 21, [17, 20, 25],
         "The jumps are 2, 3, 4, 5, so the next jump is 6: 15 + 6 = 21. (15 + 2 = 17 uses only the first jump.)"),
        ("100, 99, 97, 94, 90", 85, [89, 86, 84],
         "The jumps down are 1, 2, 3, 4, so the next jump is 5: 90 − 5 = 85. (90 − 1 = 89 uses only the first jump; "
         "90 − 4 = 86 repeats the last jump.)"),
    ]
    for lst, ans, wrong, e in rows:
        q = "Check every step. What is the next term?<br><b>%s, ?</b>" % lst
        its.append((4, mcq(q, ans, wrong, e, rnd, n)))
    return finish(its, "Pattern rules in words", rnd)


# ============================================================ set 2: tables of values
def set_tables(rnd):
    its = []
    # A: a missing value in a table
    for a, k, m in [(7, 4, 3), (9, 6, 2), (15, 8, 4), (80, -6, 3), (11, 9, 1)]:
        vals = [a + i * k for i in range(5)]
        ans = vals[m]
        q = fig(tbl([1, 2, 3, 4, 5], vals, missing=m)) + "What is the missing term value?"
        if k > 0:
            e = "The term value goes up by %d each time. %s + %d = %s." % (k, n(vals[m - 1]), k, n(ans))
        else:
            e = "The term value goes down by %d each time. %s − %d = %s." % (-k, n(vals[m - 1]), -k, n(ans))
        if m + 1 < len(vals):
            e += " Check: %s %s %d = %s." % (n(ans), "+" if k > 0 else "−", abs(k), n(vals[m + 1]))
        cands = [ans + k, (m + 1) * abs(k), ans + 1, ans - 1, ans + 2 * k]
        its.append((0, mcq(q, ans, cands, e, rnd, n)))
    # E: the rule in words from a table (term number vs term value)
    for a, k in [(7, 4), (12, 5), (60, -8)]:
        vals = [a + i * k for i in range(4)]
        if k > 0:
            good = "Start at %d and add %d each time." % (a, k)
            bad = ["Start at 1 and add %d each time." % k, "Start at %d and add 1 each time." % a,
                   "Start at %d and add %d each time." % (k, a)]
            e = ("Read the term value row: %s. It starts at %d and goes up by %d. "
                 "(The term number row, 1, 2, 3, 4, only shows the place of each term.)" % (lstr(vals), a, k))
        else:
            good = "Start at %d and subtract %d each time." % (a, -k)
            bad = ["Start at %d and add %d each time." % (a, -k), "Start at %d and subtract 1 each time." % a,
                   "Start at %d and subtract %d each time." % (vals[1], -k)]
            e = ("Read the term value row: %s. It starts at %d and goes down by %d. "
                 "(The term number row goes up by 1, but that is only the place of each term.)" % (lstr(vals), a, -k))
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which pattern rule matches the table?"
        its.append((1, mcq(q, good, bad, e, rnd)))
    # B: a far term
    for a, k, N in [(6, 5, 10), (3, 4, 12), (120, -7, 10), (75, -6, 9), (9, 8, 15)]:
        vals = [a + i * k for i in range(4)]
        ans = a + (N - 1) * k
        q = (fig(tbl([1, 2, 3, 4, N], vals + [ans], missing=4)) +
             "The pattern continues in the same way. What is the term value for term number %d?" % N)
        e = jumps_e(a, k, N, ans) + " (%s is the term value for term 5, the next term.)" % n(vals[3] + k)
        cands = [a + N * k, vals[3] + k]
        cands += [N * k, N * a, a + (N - 2) * k] if k > 0 else [a + (N - 2) * k, a - N]
        its.append((2, mcq(q, ans, cands, e, rnd, n)))
    # C: from a picture to a table
    for kind, N in [("sticks_sq", 8), ("grid", 9), ("L", 10), ("house", 7)]:
        a, b, c = [count(kind, k) for k in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = count(kind, N)
        assert ans == a + (N - 1) * k
        q = (fig(pattern_svg(kind)) + "Make a table of values: figure number and number of %ss. "
             "How many %ss will Figure %d need?" % (w, w, N))
        e = ("The table starts %d, %d, %d and goes up by %d. From Figure 1 to Figure %d there are %d jumps: "
             "%d + %d × %d = %d." % (a, b, c, k, N, N - 1, a, N - 1, k, ans))
        its.append((3, mcq(q, ans, [N * a, a + N * k, c + k, N * k], e, rnd, n)))
    # D: which term number has this value?
    for a, k, V, wrong in [(6, 4, 46, [46, 10, 12]), (3, 5, 58, [58, 11, 13]), (90, -7, 6, [6, 12, 14])]:
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
        its.append((4, mcq(q, N, wrong, e, rnd, n)))
    return finish(its, "Tables of values", rnd)


# ============================================================ set 3: rules with symbols
def set_symbols(rnd):
    its = []
    # A: use a symbol rule
    for a, b, x in [(3, 1, 8), (4, 2, 6), (5, 3, 7), (6, -2, 9), (2, 9, 12)]:
        ans = a * x + b
        q = ("The pattern rule is <b>%s</b>, where %s is the term number. "
             "What is the term value for term number %d?" % (boxr(a, b), BOX, x))
        e = "Put %d in the box: %d × %d %s = %d %s = %d. Multiply first, then %s. (%s)" % (
            x, x, a, addsub(b), a * x, addsub(b), ans, "add" if b > 0 else "subtract",
            "Adding %d before multiplying gives %d." % (b, (x + b) * a) if b > 0 else
            "Subtracting %d before multiplying gives %d." % (-b, (x + b) * a))
        cands = [(x + b) * a, a * x, x * (a + b)]
        its.append((0, mcq(q, ans, cands, e, rnd, n)))
    # B: which symbol rule fits a table
    for a, b in [(3, 2), (4, 3), (2, 5), (5, -2), (6, 4)]:
        vals = [a * i + b for i in range(1, 5)]
        f = vals[0]
        good = boxr(a, b)
        bad = ["%s + %d" % (BOX, f - 1), boxr(f, 0), boxr(a, f)]
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which rule gives the term value? (%s is the term number.)" % BOX
        e = ("The term value goes up by %d, so the rule has %s × %d. Term 1: 1 × %d = %d, and the value is %d, "
             "so %s. Check term 4: 4 × %d %s = %d. (A rule must work for every term, not only term 1.)" % (
                 a, BOX, a, a, a, f, ("add %d" % b) if b > 0 else ("subtract %d" % -b), a, addsub(b), vals[3]))
        its.append((1, mcq(q, good, bad, e, rnd)))
    # D: from a picture to a symbol rule
    for kind in ["sticks_sq", "grid", "L", "house", "cross"]:
        a1, a2, a3 = [count(kind, k) for k in (1, 2, 3)]
        k = a2 - a1
        b = a1 - k
        assert all(count(kind, i) == k * i + b for i in range(1, 8))
        w = thing(kind)
        good = boxr(k, b)
        bad = ["%s + %d" % (BOX, k), boxr(a1, 0), boxr(k, a1)]
        q = fig(pattern_svg(kind)) + "Which rule gives the number of %ss in Figure %s?" % (w, BOX)
        e = ("The counts are %d, %d, %d: each figure adds %d %ss, so the rule has %s × %d. "
             "Figure 1: 1 × %d + %d = %d. Check Figure 3: 3 × %d + %d = %d." % (
                 a1, a2, a3, k, w, BOX, k, k, b, a1, k, b, a3))
        its.append((2, mcq(q, good, bad, e, rnd)))
    # C: work backwards to find the term number
    for a, b, V in [(2, 4, 30), (3, 3, 33), (5, 5, 60), (4, -4, 36), (10, 20, 150)]:
        N = Fr(V - b, a)
        assert N.denominator == 1
        cands = [V, Fr(V + b, a), Fr(V, a), V - b]
        cands = [c for c in cands if Fr(c).denominator == 1]
        q = ("The pattern rule is <b>%s</b>, where %s is the term number. "
             "Which term number has a term value of %s?" % (boxr(a, b), BOX, n(V)))
        if b > 0:
            e = "Work backwards. Undo + %d: %s − %d = %s. Undo × %d: %s ÷ %d = %s. Check: %s × %d + %d = %s." % (
                b, n(V), b, n(V - b), a, n(V - b), a, n(N), n(N), a, b, n(V))
        else:
            e = "Work backwards. Undo − %d: %s + %d = %s. Undo × %d: %s ÷ %d = %s. Check: %s × %d − %d = %s." % (
                -b, n(V), -b, n(V - b), a, n(V - b), a, n(N), n(N), a, -b, n(V))
        e += " (%s is the term value, not the term number.)" % n(V)
        its.append((3, mcq(q, N, cands, e, rnd, n)))
    return finish(its, "Rules with symbols (%s × 3 + 1)" % BOX, rnd)


# ============================================================ set 4: rules with variables
def set_variables(rnd):
    its = []
    # A: evaluate an expression
    for a, b, x in [(3, 1, 7), (4, -3, 9), (5, 2, 10), (2, 7, 8), (6, -4, 5)]:
        ans = a * x + b
        glued = int("%d%d" % (a, x)) + b
        q = "The rule for a pattern is <b>%s</b>, where n is the term number. What is the term value when n = %d?" % (
            lin(a, b), x)
        e = "%dn means %d × n. %d × %d = %d, then %d %s = %d. (%dn is not the number %d%d.)" % (
            a, a, a, x, a * x, a * x, addsub(b), ans, a, a, x)
        cands = [glued, a + x + b, a * (x + b)]
        its.append((0, mcq(q, ans, cands, e, rnd, n)))
    # D: which list matches the rule
    for a, b in [(2, 5), (3, 2), (5, 1), (10, 4)]:
        right = lstr([a * i + b for i in range(1, 5)])
        wrong = [lstr([b + a * i for i in range(4)]), lstr([a + i + b for i in range(1, 5)]),
                 lstr([a + b + b * i for i in range(4)])]
        q = "Which list shows the first four terms of the pattern <b>%s</b>? (n = 1, 2, 3, 4)" % lin(a, b)
        e = ("Put each term number in the rule. n = 1: %d × 1 + %d = %d. n = 2: %d × 2 + %d = %d. The terms go up by %d. "
             "(%s starts at n = 0; %s reads %dn as %d + n.)" % (
                 a, b, a + b, a, b, 2 * a + b, a, wrong[0], wrong[1], a, a))
        its.append((1, mcq(q, right, wrong, e, rnd)))
    right = lstr([30 - 3 * i for i in range(1, 5)])
    wrong = [lstr([30 - 3 * i for i in range(4)]), lstr([30 - 3 - i for i in range(1, 5)]),
             lstr([30 - i for i in range(1, 5)])]
    q = "Which list shows the first four terms of the pattern <b>%s</b>? (n = 1, 2, 3, 4)" % lin(-3, 30)
    e = ("n = 1: 30 − 3 × 1 = 27. n = 2: 30 − 3 × 2 = 24. The terms go down by 3: 27, 24, 21, 18. "
         "(30 is not a term, because n starts at 1.)")
    its.append((1, mcq(q, right, wrong, e, rnd)))
    # B: which expression fits a table
    for a, b in [(3, 4), (4, 1), (2, 6), (10, -5)]:
        vals = [a * i + b for i in range(1, 5)]
        f = vals[0]
        good = lin(a, b)
        bad = ["n + %d" % (f - 1), "%dn" % f, lin(a, f)]
        q = fig(tbl([1, 2, 3, 4], vals)) + "Which rule gives the term value? (n is the term number.)"
        e = ("The value goes up by %d, so the rule has %dn. For n = 1, %dn is %d and the value is %d, "
             "so %s %d: %s. Check n = 4: %d × 4 %s = %d. (A rule must work for every term.)" % (
                 a, a, a, a, f, "add" if b > 0 else "subtract", abs(b), good, a, addsub(b), vals[3]))
        its.append((2, mcq(q, good, bad, e, rnd)))
    vals = [54 - 4 * i for i in range(1, 5)]
    assert vals == [50, 46, 42, 38]
    q = fig(tbl([1, 2, 3, 4], vals)) + "Which rule gives the term value? (n is the term number.)"
    e = ("The value goes down by 4, so the rule subtracts 4n. For n = 1: 50 + 4 = 54, so the rule is 54 − 4n. "
         "Check n = 4: 54 − 16 = 38. (50 − 4n gives 46 for n = 1.)")
    its.append((2, mcq(q, lin(-4, 54), [lin(-4, 50), "51 − n", lin(4, 46)], e, rnd)))
    # C: find n
    for a, b, V in [(2, 6, 40), (3, 6, 51), (4, 8, 64), (7, -7, 63), (6, 12, 90)]:
        N = Fr(V - b, a)
        assert N.denominator == 1
        cands = [V, Fr(V + b, a), Fr(V, a), V - b]
        cands = [c for c in cands if Fr(c).denominator == 1]
        q = ("The rule for a pattern is <b>%s</b>, where n is the term number. "
             "Which term number has a term value of %s?" % (lin(a, b), n(V)))
        if b > 0:
            e = "Find n so that %dn + %d = %s. Undo + %d: %s − %d = %s. Undo × %d: %s ÷ %d = %s. So n = %s." % (
                a, b, n(V), b, n(V), b, n(V - b), a, n(V - b), a, n(N), n(N))
        else:
            e = "Find n so that %dn − %d = %s. Undo − %d: %s + %d = %s. Undo × %d: %s ÷ %d = %s. So n = %s." % (
                a, -b, n(V), -b, n(V), -b, n(V - b), a, n(V - b), a, n(N), n(N))
        e += " (%s is the term value, not the term number.)" % n(V)
        its.append((3, mcq(q, N, cands, e, rnd, n)))
    return finish(its, "Rules with variables (3n + 1)", rnd)


# ============================================================ set 5: predict terms (word problems)
def set_predict(rnd):
    its = []

    def add(q, ans, cands, e, disp=None):
        its.append((0, mcq(q, ans, cands, e, rnd, disp)))

    unit = lambda u: (lambda v: n(v) + NBSP + u)
    dol = lambda v: money(v, False)
    lab = lambda u: (lambda v: "%s %s" % (n(v), u))
    assert 2 + 6 * Fr("0.5") == 5
    add("To train for the Terry Fox Run, Simran runs 2 km in week 1. Each week she runs 0.5 km more. "
        "How far does she run in week 7?", 5, F("5.5", "3.5", "4.5"),
        "From week 1 to week 7 there are 6 jumps: 6 × 0.5 = 3 km. 2 + 3 = 5 km. (5.5 km uses 7 jumps.)", unit("km"))
    assert 4 + 11 * 2 == 26
    add("Square tables are pushed together in a row for a class party. 1 table seats 4 students, 2 tables seat 6, "
        "and 3 tables seat 8. How many students can sit at 12 tables?", 26, [48, 24, 28],
        "Each new table adds 2 seats. From 1 table to 12 tables there are 11 jumps: 4 + 11 × 2 = 26. "
        "(12 × 4 = 48 counts seats that are lost where the tables touch.)", lab("students"))
    assert 15 + 6 * 8 == 63
    add("Liam is saving for a lift ticket at Grouse Mountain. He has $15 and saves $6 each week. "
        "How much will he have after 8 weeks?", 63, [48, 69, 168],
        "He adds 8 × $6 = $48 to his $15: 15 + 48 = $63. ($48 forgets the $15 he started with.)", dol)
    assert 120 + 5 * 25 == 245
    add("Students count salmon swimming up a creek near Nanaimo. They count 120 on day 1, 145 on day 2 and 170 on day 3. "
        "If the pattern continues, how many will they count on day 6?", 245, [270, 150, 220],
        "The count goes up by 25 each day. From day 1 to day 6 there are 5 jumps: 120 + 5 × 25 = 245. "
        "(270 uses 6 jumps; 220 is day 5.)", lab("salmon"))
    assert 150 - 9 * 12 == 42
    add("Kai has 150 pages left in his book. He reads 12 pages each day. How many pages are left after 9 days?",
        42, [108, 30, 54],
        "He reads 9 × 12 = 108 pages. 150 − 108 = 42 pages left. (108 is the pages he read, not the pages left.)",
        lab("pages"))
    assert 8 * 5 + 12 == 52
    add("Bike rentals in Stanley Park cost $12 plus $8 for each hour. The rule is <b>8n + 12</b>, where n is the "
        "number of hours. How much do 5 hours cost?", 52, [100, 40, 60],
        "8 × 5 = 40, then 40 + 12 = $52. ((8 + 12) × 5 = $100 charges the $12 every hour.)", dol)
    assert 8 * 7 + 12 == 68
    add("The same bike rental costs $12 plus $8 for each hour (<b>8n + 12</b>). Nadia pays $68. "
        "How many hours does she rent the bike?", 7, [56, 10, 6],
        "Take away the $12 first: 68 − 12 = 56. Then 56 ÷ 8 = 7 hours. Check: 8 × 7 + 12 = 68. "
        "(56 is the cost of the hours, not the number of hours.)", lab("hours"))
    assert 14 + 6 * 3 == 32
    add("On a rainy day in Vancouver, a rain gauge has 14 mm of rain at 9 a.m. It rains 3 mm each hour. "
        "How much rain is in the gauge at 3 p.m.?", 32, [18, 35, 29],
        "9 a.m. to 3 p.m. is 6 hours. 6 × 3 = 18 mm. 14 + 18 = 32 mm. (35 mm counts 7 hours.)", unit("mm"))
    assert 3 + 4 * Fr("2.5") == 13
    add("On a hike near Kamloops, Owen walks 3 km in the first hour and 2.5 km in each hour after that. "
        "How far has he walked after 5 hours?", 13, F("15.5", "12.5", "10.5"),
        "After the first hour there are 4 more hours: 4 × 2.5 = 10 km. 3 + 10 = 13 km. "
        "(15.5 km adds 2.5 km for all 5 hours.)", unit("km"))
    assert 2 * 20 + 1 == 41
    add("Ava builds a row of triangles with toothpicks. 1 triangle uses 3, 2 triangles use 5 and 3 triangles use 7. "
        "How many toothpicks does she need for 20 triangles?", 41, [60, 40, 43],
        "Each new triangle adds 2 toothpicks (it shares a side). From 1 to 20 triangles there are 19 jumps: "
        "3 + 19 × 2 = 41. (20 × 3 = 60 counts the shared sides twice.)", lab("toothpicks"))
    assert 3 * 15 + 1 == 46
    add("Lucas makes a row of squares with craft sticks: 4 sticks, 7 sticks, 10 sticks, … The rule is <b>3n + 1</b>. "
        "Which figure uses 46 sticks?", "Figure 15", ["Figure 46", "Figure 14", "Figure 16"],
        "46 − 1 = 45, and 45 ÷ 3 = 15. So n = 15. Check: 3 × 15 + 1 = 46. (46 is the number of sticks, not the figure number.)")
    assert 150 - 10 * 8 == 70
    add("Mei has 150 hockey cards. She gives away 8 cards each week. After how many weeks will she have 70 cards left?",
        "10 weeks", ["70 weeks", "9 weeks", "11 weeks"],
        "She gives away 150 − 70 = 80 cards. 80 ÷ 8 = 10 weeks. Check: 150 − 10 × 8 = 70. (70 is the number of cards, not weeks.)")
    g = graph_svg([(i, 3 * i + 1) for i in range(1, 5)], xl="Day", yl="Height (cm)",
                  label="graph of a plant height: 4, 7, 10, 13 cm")
    assert 3 * 9 + 1 == 28
    add(fig(g) + "Zara’s bean plant grows the same amount each day. How tall will it be on day 9?", 28, [31, 27, 16],
        "It grows 3 cm a day. From day 1 to day 9 there are 8 jumps: 4 + 8 × 3 = 28 cm. "
        "(31 cm uses 9 jumps; 16 cm is day 5.)", unit("cm"))
    add(fig(g) + "Each point is (day, height). Which point will come next on the graph?", pair(5, 16),
        [pair(16, 5), pair(5, 14), pair(6, 16)],
        "The next day is day 5. The height goes up 3 cm: 13 + 3 = 16. The point is (5, 16). "
        "(In (16, 5) the numbers are swapped: the day comes first.)")
    assert 18 + 11 * 2 == 40
    add("In a school gym, chairs are set up for a concert. Row 1 has 18 chairs, and each row has 2 more chairs than the "
        "row before. How many chairs are in row 12?", 40, [42, 24, 216],
        "From row 1 to row 12 there are 11 jumps: 18 + 11 × 2 = 40 chairs. (42 uses 12 jumps.)", lab("chairs"))
    assert 3 * 6 + 5 == 23
    add("A wave pool charges $5 to get in plus $3 for each waterslide ride. The rule is <b>3n + 5</b>. "
        "How much does Ji-woo pay for 6 rides?", 23, [48, 41, 18],
        "3n means 3 × n: 3 × 6 = 18, then 18 + 5 = $23. ($41 reads 3n as 36; $48 adds before multiplying.)", dol)
    assert 180 - 15 * 9 == 45
    add("A rain barrel holds 180 L of water. Harjot uses 15 L each day to water his garden. "
        "The rule is <b>180 − 15 × %s</b>, where %s is the number of days. After how many days will 45 L be left?" % (BOX, BOX),
        "9 days", ["3 days", "45 days", "10 days"],
        "He uses 180 − 45 = 135 L. 135 ÷ 15 = 9 days. Check: 180 − 15 × 9 = 45. "
        "(45 ÷ 15 = 3 uses the water left, not the water used.)")
    assert 5 + 14 * 4 == 61
    add("Mateo plants cedar seedlings in rows. Row 1 has 5 seedlings, row 2 has 9 and row 3 has 13. "
        "Which row has 61 seedlings?", "row 15", ["row 61", "row 14", "row 16"],
        "The rows go up by 4. 61 − 5 = 56, and 56 ÷ 4 = 14 jumps after row 1, so it is row 15. "
        "(14 is the number of jumps, not the row number.)")
    assert 2 + 5 * 4 == 22
    add("A SkyTrain arrives at a station every 4 minutes. The first train arrives at 7:02 a.m. "
        "When does the 6th train arrive?", "7:22 a.m.", ["7:26 a.m.", "7:18 a.m.", "7:24 a.m."],
        "From the 1st train to the 6th train there are 5 jumps of 4 minutes: 5 × 4 = 20 minutes. "
        "7:02 + 20 minutes = 7:22 a.m. (7:26 a.m. uses 6 jumps.)")
    assert 24 - 8 * Fr("1.5") == 12
    add("A candle is 24 cm tall. It burns down 1.5 cm each hour. The rule is <b>24 − 1.5n</b>, where n is the number "
        "of hours. How tall is the candle after 8 hours?", 12, F("36", "13.5", "16"),
        "1.5 × 8 = 12 cm burns away. 24 − 12 = 12 cm. (36 cm adds instead of subtracting.)", unit("cm"))
    rnd.shuffle(its)
    return {"title": "Predict terms: word problems", "items": [i for _, i in its]}


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
    return (
        "<h2>Pattern rules in words</h2>"
        "<p>An <b>increasing</b> pattern gets bigger and a <b>decreasing</b> pattern gets smaller. A pattern rule in words "
        "tells where to start and what to do each time. Check the rule on every step, not only the first one.</p>" +
        ex("Example 1", "250, 235, 220, 205, …", "Each step subtracts 15, and the first term is 250.",
           "Start at 250 and subtract 15 each time.") +
        "<h2>Tables of values</h2>"
        "<p>Each number in a pattern is a <b>term</b>. Its place is the <b>term number</b> (1, 2, 3 …). The number "
        "itself is the <b>term value</b>. A table of values shows both.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sticks_sq") +
        "<figcaption>4, 7, 10 craft sticks: each new square adds 3 sticks, because it shares a side.</figcaption></figure>"
        "<figure class='sn-fig'>" + t +
        "<figcaption>From term 1 to term 10 there are 9 jumps of 3: 4 + 9 × 3 = 31.</figcaption></figure>"
        "<h2>Rules with symbols and variables</h2>"
        "<p>A rule can also give a term value straight from its term number. With a symbol, the box stands for the "
        "term number: <b>" + boxr(3, 1) + "</b>. With a variable, the letter n stands for the term number: "
        "<b>3n + 1</b>. 3n means 3 × n. Both rules give 4, 7, 10, 13 …</p>" +
        ex("Example 2", "Find term 10 with the rule 3n + 1.", "3 × 10 = 30, then 30 + 1 = 31.", "31") +
        ex("Example 3", "Which rule fits the table above?",
           "The values go up by 3, so the rule has 3n. For n = 1, 3n is 3, but the value is 4, so add 1. "
           "Check n = 4: 3 × 4 + 1 = 13.", "3n + 1") +
        "<h2>Predict terms</h2>"
        "<p>To predict a far term, use the rule. To find which term has a value, work backwards: undo the + 1, then "
        "undo the × 3.</p>" +
        ex("Example 4", "Which term number has a term value of 40 in 3n + 1?",
           "40 − 1 = 39, and 39 ÷ 3 = 13. Check: 3 × 13 + 1 = 40.", "term number 13") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using only the first step: 3, 6, 12, 24 is “add 3”", "Check every step. 3, 6, 12, 24 doubles, so the next term is 48"],
            ["Mixing up the term number and the term value", "The term number is the place; the term value is the number in that place"],
            ["Term 10 = term 1 + 10 jumps", "From term 1 to term 10 there are 9 jumps"],
            ["Reading 3n as 3 and n side by side (n = 7 gives 37)", "3n means 3 × n: 3 × 7 = 21"],
            ["Adding before multiplying in " + boxr(3, 1), "Multiply the term number by 3 first, then add 1"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about patterns in the BC math curriculum?",
     "a": "In Grade 5 Patterning, BC students describe rules for increasing and decreasing patterns with words, numbers, symbols and variables, such as “start at 4 and add 3”, □ × 3 + 1 or 3n + 1. They use tables of values to extend patterns and predict later terms."},
    {"q": "What does 3n + 1 mean in a pattern?",
     "a": "The letter n stands for the term number, and 3n means 3 × n. For term 5, the term value is 3 × 5 + 1 = 16."},
    {"q": "How do you find the 10th term of a pattern like 4, 7, 10, 13?",
     "a": "The pattern adds 3 each time, and from term 1 to term 10 there are 9 jumps. 4 + 9 × 3 = 31, so the 10th term is 31."},
    {"q": "What is the difference between a term number and a term value?",
     "a": "The term number is the place in the pattern (1st, 2nd, 3rd …) and the term value is the number in that place. In 5, 8, 11, 14, term number 3 has a term value of 11."},
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
    rnd = random.Random(55810)
    sets = [set_words_rules(rnd), set_tables(rnd), set_symbols(rnd), set_variables(rnd), set_predict(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "pattern-rules", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Pattern Rules: Words, Tables, Symbols and Variables",
        "seo_title": "Grade 5 Pattern Rules Math Worksheets: Tables of Values, Symbols and Variables (Free, Answer Key, BC Curriculum)",
        "short_title": "Pattern rules",
        "domain": "Patterning",
        "standard_code": "Grade 5: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Rules for increasing and decreasing patterns with words, numbers, symbols, and variables",
        "meta_desc": "Free Grade 5 math worksheets on pattern rules for the BC curriculum: describe increasing and decreasing patterns in words, use tables of values, write rules with symbols (□ × 3 + 1) and variables (3n + 1), and predict later terms. 100 questions with an answer key.",
        "key_big": "“Start at 4 and add 3”, □ × 3 + 1 and 3n + 1 are three ways to write the same rule: 4, 7, 10, 13 …",
        "key_sub": "n is the term number and 3n means 3 × n. Check a rule on every term, not only the first. From term 1 to term 10 there are 9 jumps.",
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
