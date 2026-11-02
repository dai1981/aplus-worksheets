# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Ratio Tables, Double Number Lines and Graphs (6.RP.A.3a)
  python tools/gen_us_math_g6_ratio_tables.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above are written with commas.

Tables of equivalent ratios, missing values, double number lines, which table is equivalent,
plotting ratio pairs on the coordinate plane, and comparing two ratios with tables.
Every figure is drawn to the data: double number line ticks are spaced in proportion to the
values, grid points sit on grid intersections, labels never touch another point.
Wrong answers come from real mistakes: adding the same amount to both quantities instead of
multiplying, reading the wrong row, multiplying by one group too many or too few, switching x and y
when plotting, counting grid spaces instead of reading the scale, and comparing the first numbers
only instead of equivalent ratios.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ question helpers
def f(n):
    """Grade 6 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def pair(x, y):
    return "(%s, %s)" % (f(x), f(y))


def rat(a, b):
    return "%s : %s" % (f(a), f(b))


def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (point letters, table columns from left to right)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e, fmt=f):
    """Number answers: 3 distractors from real mistakes (positive, unique); positions are balanced later."""
    ch = []
    for c in cands:
        if c is not None and c > 0 and c != correct and c not in ch:
            ch.append(c)
    assert len(ch) >= 3, (q, correct, ch)
    return {"q": q, "c": [fmt(c) for c in ch[:3]] + [fmt(correct)], "a": 3, "e": e}


def unit(word, plural):
    return lambda v: "%s %s" % (f(v), word if v == 1 else plural)


def money(v):
    return "$" + f(v)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


class Pos:
    """Positions for picture answers, spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def cell(v):
    return f(v) if isinstance(v, int) else v


# ------------------------------------------------------------ ratio table
def ratio_table(top, bot, la, lb, label="ratio table"):
    """Two rows: la with values top, lb with values bot. A value can be '?'."""
    n = len(top)
    assert len(bot) == n
    LW = int(max(tw(la, 15, True), tw(lb, 15, True)) + 18)
    CW = int(max(46, max(tw(cell(c), 17, True) for c in top + bot) + 18))
    RH = 32
    s = []
    for r, (name, vals) in enumerate([(la, top), (lb, bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2.0, y + RH / 2.0 + 5.5, name, 15, bold=True))
        for i, v in enumerate(vals):
            x = 2 + LW + i * CW
            t = cell(v)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                     % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2.0, y + RH / 2.0 + 6, t, 17, bold=True, col=RED if t == "?" else INK))
    return svg_wrap(4 + LW + CW * n, 4 + RH * 2, "".join(s), label)


# ------------------------------------------------------------ double number line
def dnl(ticks, p, q, la, lb, hide=None, label="double number line"):
    """ticks: multipliers (0 first). Top value m*p, bottom value m*q. Tick x is in proportion to m.
    hide: (row 'A' or 'B', index) shown as a red ?."""
    assert ticks[0] == 0 and ticks == sorted(ticks)
    tops = [m * p for m in ticks]
    bots = [m * q for m in ticks]
    tt = [f(v) for v in tops]
    bb = [f(v) for v in bots]
    if hide:
        (tt if hide[0] == "A" else bb)[hide[1]] = "?"
    widest = max(tw(t, 16, True) for t in tt + bb)
    dmin = min(b - a for a, b in zip(ticks, ticks[1:]))
    U = max(330.0 / ticks[-1], (widest + 8) / dmin)
    LW = max(tw(la, 14, True), tw(lb, 14, True)) + 10
    x0 = LW + 18
    xe = x0 + ticks[-1] * U
    W = int(math.ceil(xe + widest / 2 + 22))
    yA, yB = 38, 82
    s = []
    for ly, name in [(yA, la), (yB, lb)]:
        s.append(text(4, ly + 5, name, 14, anchor="start", bold=True))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 6, ly, xe + 12, ly, INK))
        s.append("<polygon points='%.1f,%d %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (xe + 18, ly, xe + 10, ly - 4.5, xe + 10, ly + 4.5, INK))
    for m, a, b in zip(ticks, tt, bb):
        x = x0 + m * U
        for ly in (yA, yB):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 7, x, ly + 7, INK))
        s.append(text(x, yA - 13, a, 16, bold=True, col=RED if a == "?" else INK))
        s.append(text(x, yB + 26, b, 16, bold=True, col=RED if b == "?" else INK))
    return svg_wrap(W, 114, "".join(s), label)


# ------------------------------------------------------------ missing value (tables and double number lines)
def missing(cols, row, j, ref, where):
    """cols: list of (top, bottom). The value at (row, j) is hidden. ref: a column used to find it.
    Returns answer, distractors, explanation."""
    A = [c[0] for c in cols]
    B = [c[1] for c in cols]
    H, K = (A, B) if row == "A" else (B, A)   # H: row with the hidden value, K: the other row
    ans = H[j]
    hr, kr = H[ref], K[ref]
    kj = K[j]
    F = Fraction(kj, kr)
    rowk = {"A": ("top", "bottom"), "B": ("bottom", "top")}[row]
    if F.denominator == 1:
        n = F.numerator
        e = ("In the %s %s, %s × %d = %s. Multiply the %s %s by the same number: %s × %d = %s."
             % (rowk[1], where, f(kr), n, f(kj), rowk[0], where, f(hr), n, f(ans)))
        near = [hr * (n + 1), hr * (n - 1)]
    elif F.numerator == 1:
        d = F.denominator
        e = ("In the %s %s, %s ÷ %d = %s. Divide the %s %s by the same number: %s ÷ %d = %s."
             % (rowk[1], where, f(kr), d, f(kj), rowk[0], where, f(hr), d, f(ans)))
        near = [hr - d, hr // (d - 1) if hr % (d - 1) == 0 else None, d]
    else:
        assert hr % kr == 0
        u = hr // kr
        e = ("First find the value that goes with 1: %s ÷ %s = %s. Then multiply: %s × %s = %s."
             % (f(hr), f(kr), f(u), f(kj), f(u), f(ans)))
        near = [hr * kj, u * (kj + 1), u * (kj - 1)]
    assert F * hr == ans
    add = hr + (kj - kr)
    cands = [add, kj] + near
    if add > 0 and add != ans:
        d_ = kj - kr
        r0 = (A[ref], B[ref])
        r1 = (r0[0] + d_, r0[1] + d_)
        e += " (%s %s %s both numbers of %s gives %s, but %s does not keep the same ratio.)" % (
            "Adding" if d_ > 0 else "Subtracting", f(abs(d_)), "to" if d_ > 0 else "from",
            rat(*r0), rat(*r1), "adding" if d_ > 0 else "subtracting")
    return ans, cands, e


# ------------------------------------------------------------ set 1: complete a ratio table
TABLES = [
    ("A fruit punch uses 1 cup of juice for every 3 cups of water.", "Juice (cups)", "Water (cups)", 1, 3, [1, 2, 3, 4, 5], "B", 3),
    ("A recipe uses 2 eggs for every 3 cups of flour.", "Flour (cups)", "Eggs", 3, 2, [1, 2, 3, 4], "B", 2),
    ("A shade of purple paint uses 2 cans of red for every 5 cans of blue.", "Red (cans)", "Blue (cans)", 2, 5, [1, 2, 3, 5, 6], "A", 3),
    ("A field trip needs 1 adult for every 8 students.", "Adults", "Students", 1, 8, [1, 2, 3, 4, 6], "B", 4),
    ("Kai bikes 12 miles every hour.", "Time (hours)", "Distance (miles)", 1, 12, [1, 2, 3, 5, 8], "B", 3),
    ("Movie tickets cost $7 each.", "Tickets", "Cost ($)", 1, 7, [1, 2, 4, 6, 10], "B", 4),
    ("A bracelet pattern uses 4 green beads for every 6 blue beads.", "Green beads", "Blue beads", 2, 3, [2, 4, 6, 8], "A", 3),
    ("A big batch of trail mix uses 20 cups of nuts and 16 cups of raisins.", "Nuts (cups)", "Raisins (cups)", 5, 4, [4, 1, 2, 3], "B", 1),
    ("A printer prints 30 pages every 2 minutes.", "Time (minutes)", "Pages", 1, 15, [2, 4, 6, 10], "B", 3),
    ("Every 3 lemons make 1 cup of lemon juice.", "Lemons", "Juice (cups)", 3, 1, [1, 2, 4, 5, 8], "A", 4),
    ("A car goes 150 miles on 5 gallons of gas.", "Gas (gallons)", "Distance (miles)", 1, 30, [5, 10, 15, 20], "B", 2),
    ("A store sells 4 cans of soup for $6.", "Cans", "Cost ($)", 2, 3, [2, 4, 6, 10], "B", 3),
    ("A choir has 5 sopranos for every 3 altos.", "Sopranos", "Altos", 5, 3, [1, 2, 3, 4, 6], "A", 4),
    ("A restaurant cooks 12 cups of rice in 18 cups of water.", "Rice (cups)", "Water (cups)", 2, 3, [6, 2, 4, 8], "A", 1),
]


def table_fig(cols, la, lb, hide=None, label="ratio table"):
    top = [c[0] for c in cols]
    bot = [c[1] for c in cols]
    if hide:
        (top if hide[0] == "A" else bot)[hide[1]] = "?"
    return fig(ratio_table(top, bot, la, lb, label))


def set_tables(rnd):
    its = []
    for intro, la, lb, p, q, ms, row, j in TABLES:
        cols = [(m * p, m * q) for m in ms]
        ans, cands, e = missing(cols, row, j, 0, "row")
        q_ = table_fig(cols, la, lb, (row, j)) + intro + " The table shows equivalent ratios. What number goes in the ? box?"
        its.append(mcq_num(q_, ans, cands, e))
    # which column could be added
    for la, lb, p, q, ms, k, add, third, why in [
        ("Red (cans)", "Blue (cans)", 2, 5, [1, 2, 3], 4, 6, "8 : 15",
         "2 × 4 = 8 and 5 × 4 = 20, so 8 : 20 is equivalent to 2 : 5. (8 : 11 adds 6 to both, 20 : 8 switches the rows, "
         "and 8 : 15 multiplies the bottom by 3 instead of 4.)"),
        ("Juice (cups)", "Water (cups)", 3, 4, [1, 2, 3], 5, 12, "15 : 24",
         "3 × 5 = 15 and 4 × 5 = 20, so 15 : 20 is equivalent to 3 : 4. (15 : 16 adds 12 to both, 20 : 15 switches the rows, "
         "and 15 : 24 multiplies the bottom by 6 instead of 5.)"),
    ]:
        cols = [(m * p, m * q) for m in ms]
        right = "%s : %s" % (k * p, k * q)
        wrong = ["%s : %s" % (p + add, q + add), "%s : %s" % (k * q, k * p), third]
        its.append(mcq(table_fig(cols, la, lb) + "Which pair of values (top : bottom) could be added as a new column of this ratio table?",
                       right, wrong, why, rnd))
    # what do you multiply by
    for la, lb, p, q, ms, jj in [("Hours", "Miles", 1, 6, [1, 2, 4, 7], 3), ("Boxes", "Pencils", 3, 24, [1, 2, 3, 5], 3)]:
        cols = [(m * p, m * q) for m in ms]
        n = ms[jj]
        right = "Multiply both by %d" % n
        wrong = ["Add %s to both" % f(cols[jj][0] - cols[0][0]), "Multiply only the top by %d" % n,
                 "Multiply both by %d" % (n - 1)]
        e = ("%s × %d = %s and %s × %d = %s. Equivalent ratios multiply both quantities by the same number. "
             "(Adding %s to both would give %s : %s.)" % (f(p), n, f(n * p), f(q), n, f(n * q),
                                                          f(cols[jj][0] - cols[0][0]), f(cols[jj][0]),
                                                          f(q + cols[jj][0] - cols[0][0])))
        its.append(mcq(table_fig(cols, la, lb) + "How do you get from the first column to the last column?",
                       right, wrong, e, rnd))
    # the value that goes with 1
    for intro, la, lb, a, b, ms in [
        ("Ella pays $12 for 4 notebooks.", "Notebooks", "Cost ($)", 4, 12, [4, 8, 1]),
        ("A runner covers 35 laps in 5 days.", "Days", "Laps", 5, 35, [5, 10, 1]),
    ]:
        u = b // a
        cols = [(m, m * u) for m in ms]
        ans = u
        e = ("To go from %d to 1 in the top row, divide by %d. Divide the bottom row by %d too: %s ÷ %d = %s. "
             "(Subtracting %d from both numbers of %s gives %s, but subtracting does not keep the same ratio.)"
             % (a, a, a, f(b), a, f(u), a - 1, rat(a, b), rat(1, b - a + 1)))
        its.append(mcq_num(table_fig(cols, la, lb, ("B", 2)) + intro + " What number goes in the ? box?",
                           ans, [b - (a - 1), a, b - u, b // 2], e))
    assert len(its) == 20, len(its)
    return {"title": "Complete a ratio table", "items": its}


# ------------------------------------------------------------ set 2: double number lines
LINES = [
    ("Mia runs 1 mile every 10 minutes.", "Miles", "Minutes", 1, 10, [0, 1, 2, 3, 4, 5], "B", 4, 1),
    ("A smoothie uses 2 bananas for every 1 cup of milk.", "Bananas", "Milk (cups)", 2, 1, [0, 1, 2, 3, 4, 5, 6], "A", 5, 1),
    ("3 packs of pens cost $4.", "Packs", "Cost ($)", 3, 4, [0, 1, 2, 3, 4, 5], "B", 4, 1),
    ("A train travels 60 miles every hour.", "Hours", "Miles", 1, 60, [0, 1, 2, 3, 4, 5], "B", 5, 1),
    ("A copier makes 20 copies every minute.", "Minutes", "Copies", 1, 20, [0, 1, 2, 3, 4, 6], "B", 5, 1),
    ("5 apples cost $2.", "Apples", "Cost ($)", 5, 2, [0, 1, 2, 3, 4], "A", 4, 1),
    ("Jon earns $15 every hour.", "Hours", "Pay ($)", 1, 15, [0, 1, 2, 4, 8], "B", 4, 1),
    ("A punch uses 2 cups of juice for every 5 cups of water.", "Juice (cups)", "Water (cups)", 2, 5, [0, 1, 2, 3, 4], "A", 3, 1),
    ("A tank fills with 4 liters of water every 3 minutes.", "Minutes", "Liters", 3, 4, [0, 1, 2, 3, 4, 5], "A", 5, 1),
    ("8 granola bars cost $12.", "Bars", "Cost ($)", 2, 3, [0, 1, 2, 4], "B", 1, 3),
    ("Sam types 180 words in 4 minutes.", "Minutes", "Words", 1, 45, [0, 1, 2, 4], "B", 1, 3),
    ("6 bottles of water weigh 9 pounds.", "Bottles", "Pounds", 2, 3, [0, 1, 2, 3], "B", 1, 3),
    ("Ben walks 6 miles in 2 hours.", "Hours", "Miles", 1, 3, [0, 2, 3, 4, 6], "B", 2, 1),
    ("4 pounds of grass seed cover 1,000 square feet.", "Seed (pounds)", "Area (sq ft)", 4, 1000, [0, 1, 2, 3, 5], "B", 4, 1),
]


def set_lines(rnd):
    its = []
    for intro, la, lb, p, q, ticks, row, j, ref in LINES:
        cols = [(m * p, m * q) for m in ticks]
        ans, cands, e = missing(cols, row, j, ref, "line")
        q_ = (fig(dnl(ticks, p, q, la, lb, (row, j))) + intro +
              " What number goes in place of the ? on the double number line?")
        its.append(mcq_num(q_, ans, cands, e))
    # extend the line
    for intro, la, lb, p, q, ticks, n in [
        ("A recipe uses 3 cups of flour for every 2 cups of sugar.", "Flour (cups)", "Sugar (cups)", 3, 2, [0, 1, 2, 3], 7),
        ("A bus travels 50 miles every 2 hours.", "Hours", "Miles", 2, 50, [0, 1, 2, 3, 4], 9),
    ]:
        top = n * p
        ans = n * q
        e = ("%s on the top line is %d groups of %d (%s ÷ %d = %d). The bottom line has %d groups of %d: %d × %d = %s."
             % (f(top), n, p, f(top), p, n, n, q, n, q, f(ans)))
        last = ticks[-1]
        add = last * q + (top - last * p)
        if add != ans:
            e += " (Adding %d to both lines gives %s.)" % (top - last * p, f(add))
        its.append(mcq_num(fig(dnl(ticks, p, q, la, lb)) + intro + " If the double number line kept going, what number would "
                           "line up with %s on the top line?" % f(top), ans, [add, (n + 1) * q, (n - 1) * q, top], e))
    its.append(mcq_num(fig(dnl([0, 1, 2, 3, 4], 3, 12, "Cups", "Servings")) + "A soup recipe makes 12 servings from 3 cups of beans. "
                       "How many servings come from 1 cup of beans?", 4, [10, 9, 36, 3],
                       "From 3 cups to 1 cup is ÷ 3. Divide the servings by 3 too: 12 ÷ 3 = 4 servings. "
                       "(Subtracting 2 from both lines gives 10, but subtracting does not keep the same ratio.)"))
    its.append(mcq("On every double number line, which number on the bottom line lines up with 0 on the top line?",
                   "0", ["1", "The first number of the ratio", "It depends on the ratio"],
                   "0 of one quantity goes with 0 of the other: 0 cups of juice need 0 cups of water. "
                   "Both lines start at 0.", rnd))
    its.append(mcq("Ana marked 2 and 5, then 4 and 7, then 6 and 9 on a double number line for the ratio 2 : 5. What mistake did she make?",
                   "She added 2 to both lines",
                   ["She switched the two lines", "She multiplied both lines by 2", "She made no mistake"],
                   "4 : 7 and 6 : 9 come from adding 2 each time. Equivalent ratios multiply both numbers: "
                   "2 : 5, 4 : 10, 6 : 15.", rnd))
    its.append(mcq("A double number line for a cookie recipe has 2 cups of oats lined up with 30 cookies. "
                   "Which pair also lines up on it?", "5 cups and 75 cookies",
                   ["5 cups and 33 cookies", "5 cups and 60 cookies", "30 cups and 2 cookies"],
                   "2 cups make 30 cookies, so 1 cup makes 15 cookies and 5 cups make 5 × 15 = 75 cookies. "
                   "(33 adds 3 to both numbers.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Double number lines", "items": its}


# ------------------------------------------------------------ set 3: equivalent or not
def set_equiv(rnd):
    its = []
    pos = Pos(rnd)
    for la, lb, p, q, ms, kind in [
        ("Flour (cups)", "Water (cups)", 2, 3, [1, 2, 3, 4, 5], "add"),
        ("Hours", "Miles", 1, 8, [1, 2, 3, 5, 6], "add"),
        ("Red (cans)", "White (cans)", 3, 5, [1, 2, 3, 4, 6], "plus"),
        ("Tickets", "Cost ($)", 1, 9, [1, 2, 3, 4, 5], "top"),
        ("Laps", "Minutes", 2, 7, [1, 2, 3, 4, 5], "add"),
        ("Cups of rice", "Servings", 1, 4, [2, 3, 4, 6, 10], "plus"),
        ("Boys", "Girls", 4, 5, [1, 2, 3, 4, 5], "add"),
        ("Pages", "Minutes", 3, 2, [1, 2, 3, 5, 10], "top"),
    ]:
        cols = [(m * p, m * q) for m in ms]
        w = pos.next() + 1
        a, b = cols[w]
        if kind == "add":
            nb = cols[0][1] + (a - cols[0][0])
            why = "%s adds %s to both numbers of %s instead of multiplying." % (rat(a, nb), f(a - cols[0][0]), rat(*cols[0]))
        elif kind == "plus":
            nb = b + q
            why = "%s multiplies the bottom by one group too many." % rat(a, nb)
        else:
            nb = cols[w - 1][1]
            why = "%s changed the top number but kept the bottom number from the column before." % rat(a, nb)
        assert nb != b and Fraction(a, nb) != Fraction(p, q)
        shown = list(cols)
        shown[w] = (a, nb)
        choices = [rat(*c) for c in shown[1:]]
        n = Fraction(a, cols[0][0])
        e = ("Compare each column with %s. %s should be %s, because %s × %s = %s and %s × %s = %s. %s"
             % (rat(*cols[0]), rat(a, nb), rat(a, b), f(cols[0][0]), n, f(a), f(cols[0][1]), n, f(b), why))
        its.append(mcq_fixed(table_fig(shown, la, lb) + "The first column is correct. Which other column (top : bottom) "
                             "is <b>not</b> equivalent to it?", choices, rat(a, nb), e))
    # which list is equivalent
    for p, q, ks in [(2, 3, [2, 4]), (3, 4, [2, 5]), (1, 6, [3, 4]), (5, 2, [2, 3]), (4, 7, [2, 3]), (3, 10, [2, 4])]:
        right = ", ".join(rat(k * p, k * q) for k in [1] + ks)
        add = ", ".join(rat(k * p, q + (k - 1) * p) for k in [1] + ks)
        swap = ", ".join([rat(p, q)] + [rat(k * q, k * p) for k in ks])
        mixed = ", ".join([rat(p, q), rat(ks[0] * p, ks[0] * q), rat(ks[1] * p, ks[0] * q + (ks[1] - ks[0]) * p)])
        e = ("Multiply both numbers of %s by the same number: × %d gives %s and × %d gives %s."
             % (rat(p, q), ks[0], rat(ks[0] * p, ks[0] * q), ks[1], rat(ks[1] * p, ks[1] * q)))
        its.append(mcq("Which list shows ratios that are all equivalent to %s?" % rat(p, q), right, [add, swap, mixed], e, rnd))
    # what mistake
    its.append(mcq(table_fig([(2, 5), (4, 7), (6, 9), (8, 11)], "Sugar (cups)", "Flour (cups)") +
                   "Leah made this table for the ratio 2 : 5. What mistake did she make?",
                   "She added 2 to both rows",
                   ["She multiplied both rows by 2", "She switched the rows", "She made no mistake"],
                   "Each column adds 2 to both numbers: 4 : 7, 6 : 9. Equivalent ratios multiply both numbers: "
                   "2 : 5, 4 : 10, 6 : 15, 8 : 20.", rnd))
    its.append(mcq(table_fig([(3, 4), (6, 4), (9, 4), (12, 4)], "Dogs", "Walkers") +
                   "Omar made this table for the ratio 3 : 4. What mistake did he make?",
                   "He multiplied only the top row",
                   ["He added 3 to both rows", "He switched the rows", "He made no mistake"],
                   "The top row is multiplied by 2, 3 and 4, but the bottom row stays 4. Multiply both rows: "
                   "3 : 4, 6 : 8, 9 : 12, 12 : 16.", rnd))
    its.append(mcq(table_fig([(1, 5), (2, 10), (3, 15), (5, 25)], "Hours", "Dollars") +
                   "Grace made this table for $5 every hour. Is her table correct?",
                   "Yes, each column is 1 : 5 times a number",
                   ["No, 5 hours should go with 20 dollars", "No, the columns must go up by 1", "No, the rows are switched"],
                   "1 × 2 = 2 and 5 × 2 = 10, 1 × 3 = 3 and 5 × 3 = 15, 1 × 5 = 5 and 5 × 5 = 25. All columns are equivalent. "
                   "A table can skip values like 4.", rnd))
    # yes or no
    its.append(mcq("Are the ratios 4 : 6 and 10 : 15 equivalent?", "Yes, both equal 2 : 3",
                   ["No, 10 − 4 is not 15 − 6", "No, 15 is not a multiple of 6", "Yes, both add 6"],
                   "Divide 4 : 6 by 2 to get 2 : 3. Divide 10 : 15 by 5 to get 2 : 3. Both simplify to 2 : 3, so they are equivalent.", rnd))
    its.append(mcq("Are the ratios 3 : 5 and 9 : 11 equivalent?", "No, 3 × 3 = 9 but 5 × 3 = 15",
                   ["Yes, both numbers go up by 6", "Yes, both are odd numbers", "No, 9 is bigger than 5"],
                   "3 × 3 = 9, so the second number must be 5 × 3 = 15, not 11. 9 : 11 adds 6 to both numbers, "
                   "and adding does not make an equivalent ratio.", rnd))
    its.append(mcq("Are the ratios 2 : 7 and 8 : 28 equivalent?", "Yes, both numbers are × 4",
                   ["No, 28 − 8 is not 7 − 2", "No, 8 is not a multiple of 7", "Yes, both add 6"],
                   "2 × 4 = 8 and 7 × 4 = 28. Both numbers are multiplied by the same number, so the ratios are equivalent. "
                   "The difference does not have to stay the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equivalent or not? Find the error", "items": its}


# ------------------------------------------------------------ coordinate grid (first quadrant)
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


class Grid:
    """First-quadrant grid from 0 to nx across and 0 to ny up. Grid space = u px.
    sx, sy: what one grid space counts by on each axis."""

    def __init__(self, nx, ny, u=22, sx=1, sy=1, xt=None, yt=None):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u, self.sx, self.sy = nx, ny, u, sx, sy
        self.xt, self.yt = xt, yt
        left = tw(ny * sy, 14) + 15 + (24 if yt else 0)
        top = 30
        self.ox, self.oy = left, top + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26 + (22 if xt else 0)))
        assert tw(nx * sx, 14) + 3 <= u, ("x numbers too wide", nx * sx, u)
        if xt:
            assert tw(xt, 14, True) < self.W
        if yt:
            assert tw(yt, 14, True) < ny * u + 20, yt
        self.pts, self.notes, self.lines = [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and 0 <= x <= self.nx and 0 <= y <= self.ny, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def data_point(self, xv, yv, name, col=GREEN, where=None):
        assert xv % self.sx == 0 and yv % self.sy == 0, (xv, yv)
        return self.point(xv // self.sx, yv // self.sy, name, col, where)

    def line(self, x1, y1, x2, y2):
        """A line between two grid positions (in grid spaces)."""
        self.lines.append((x1, y1, x2, y2))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not (0 <= cx <= self.nx and 0 <= cy <= self.ny):
                continue
            corners = {(x + dx, y), (x, y + dy), (x + dx, y + dy)}
            if corners & others:
                continue
            c_ = (min(x, cx), min(y, cy))
            if c_ in used:
                continue
            c = self.P(x + dx / 2.0, y + dy / 2.0)
            box = (c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7)
            if any(overlap(box, b) for b in boxes):
                continue
            used.add(c_)
            return c, box
        raise AssertionError(("no room for label", x, y))

    def render(self):
        u, ox, oy, nx, ny = self.u, self.ox, self.oy, self.nx, self.ny
        s = []
        for k in range(nx + 1):
            x = ox + k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, oy, x, oy - ny * u, GRID))
        for k in range(ny + 1):
            y = oy - k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ox, y, ox + nx * u, y, GRID))
        xe, ye = ox + nx * u + 12, oy - ny * u - 12
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, xe - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox, ye + 4, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (xe, oy, xe - 9, oy - 4.5, xe - 9, oy + 4.5, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (ox, ye, ox - 4.5, ye + 9, ox + 4.5, ye + 9, INK))
        s.append(text(xe + 4, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox, ye - 6, "y", 15, bold=True, extra=" font-style='italic'"))
        for k in range(1, nx + 1):
            s.append(text(ox + k * u, oy + 18, f(k * self.sx), 14))
        for k in range(1, ny + 1):
            s.append(text(ox - 9, oy - k * u + 5, f(k * self.sy), 14, anchor="end"))
        s.append(text(ox - 9, oy + 18, 0, 14, anchor="end"))
        if self.xt:
            s.append(text(ox + nx * u / 2.0, oy + 40, self.xt, 14, bold=True))
        if self.yt:
            my = oy - ny * u / 2.0
            s.append(text(13, my, self.yt, 14, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % my))
        for x1, y1, x2, y2 in self.lines:
            a, b = self.P(x1, y1), self.P(x2, y2)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (a[0], a[1], b[0], b[1], GREEN))
        boxes = []
        for gx, gy, t, anchor, col, fs in self.notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0 = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0, c[1] - fs * 0.4, x0 + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("notes overlap", t)
            boxes.append(box)
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col,
                          extra=" stroke='#ffffff' stroke-width='4' paint-order='stroke'"))
        allpts = {(p[0], p[1]) for p in self.pts}
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            dot = (c[0] - 4.5, c[1] - 4.5, c[0] + 4.5, c[1] + 4.5)
            for b in boxes:
                assert not overlap(dot, b), ("note on a point", x, y)
        used = set()
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (c[0], c[1], col))
            if name:
                lc, box = self._label_cell(x, y, used, allpts - {(x, y)}, boxes, where)
                boxes.append(box)
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True))
        return "".join(s)

    def svg(self, label="graph of ratio pairs"):
        return svg_wrap(self.W, self.H, self.render(), label)


# ------------------------------------------------------------ set 4: plot ratio pairs
LET = ["P", "Q", "R", "S"]


def set_graph(rnd):
    its = []
    pos = Pos(rnd)
    # A: read point P
    for xt, yt, p, q, sx, sy, nx, ny, t, nx_, ny_ in [
        ("Juice (cups)", "Water (cups)", 1, 3, 1, 3, 6, 6, 4, "cups of juice", "cups of water"),
        ("Time (hours)", "Distance (miles)", 1, 10, 1, 10, 6, 6, 3, "hours", "miles"),
        ("Tickets", "Cost ($)", 1, 4, 1, 4, 6, 6, 5, "tickets", "dollars"),
        ("Red (cans)", "Blue (cans)", 2, 3, 2, 3, 6, 6, 2, "cans of red", "cans of blue"),
        ("Apples (pounds)", "Cost ($)", 1, 2, 1, 2, 7, 7, 6, "pounds of apples", "dollars"),
    ]:
        G = Grid(nx, ny, sx=sx, sy=sy, xt=xt, yt=yt)
        for k in range(0, min(nx * sx // p, ny * sy // q) + 1):
            G.data_point(k * p, k * q, "P" if k == t else None)
        x, y = t * p, t * q
        cands = [pair(y, x), pair(x // sx, y // sy), pair(x, y - q), pair(x + p, y)]
        e = ("Go down from P to the x-axis: %s. Go across from P to the y-axis: %s. So P is %s: %s %s go with %s %s. "
             "Read the numbers on the axes, not the number of grid spaces." % (f(x), f(y), pair(x, y), f(x), nx_, f(y), ny_))
        its.append(mcq(fig(G.svg()) + "The graph shows equivalent ratios as ordered pairs (x, y). Which ordered pair does point P show?",
                       pair(x, y), cands, e, rnd))
    # B: which red point has the same ratio
    for p, q, shown, right, wrongs, why, xt, yt in [
        (1, 2, 3, (4, 8), [(8, 4), (4, 5), (4, 10)],
         "(8, 4) switches x and y, (4, 5) adds 3 to both numbers of (1, 2), and (4, 10) is not 4 × (1, 2).",
         "Juice (cups)", "Water (cups)"),
        (2, 3, 3, (6, 9), [(9, 6), (6, 7), (8, 9)],
         "(9, 6) switches x and y, (6, 7) adds 4 to both numbers of (2, 3), and (8, 9) multiplies only y by 3.",
         "Red (cans)", "Blue (cans)"),
        (1, 3, 2, (3, 9), [(9, 3), (3, 5), (3, 8)],
         "(9, 3) switches x and y, (3, 5) adds 2 to both numbers of (1, 3), and (3, 8) is one less than 3 × 3.",
         "Hours", "Miles"),
        (3, 2, 3, (9, 6), [(6, 9), (9, 8), (7, 6)],
         "(6, 9) switches x and y, (9, 8) adds 6 to both numbers of (3, 2), and (7, 6) is not 3 × (3, 2).",
         "Laps", "Minutes"),
    ]:
        G = Grid(10, 10, xt=xt, yt=yt)
        for k in range(shown):
            G.point(k * p, k * q, None)
        pp = pos.next()
        cand = list(wrongs)
        cand.insert(pp, right)
        for c in cand:
            assert Fraction(c[1], c[0]) != Fraction(q, p) or c == right
        for c, L in zip(cand, LET):
            G.point(c[0], c[1], L, RED)
        e = ("Point %s. The green points show the ratio %s. %s is %d × %s, so it is equivalent. "
             % (LET[pp], rat(p, q), pair(*right), right[0] // p, pair(p, q))) + why
        its.append(mcq_fixed(fig(G.svg()) + "The green points show equivalent ratios. Which red point shows "
                             "another equivalent ratio?", LET, LET[pp], e))
    # C: which point was plotted wrong
    for p, q, mk, xt, yt in [(1, 2, "swap", "Cups of rice", "Cups of water"), (2, 1, "add", "Pages", "Minutes"),
                             (1, 2, "add", "Packs", "Cost ($)")]:
        good = [(t * p, t * q) for t in range(1, 5)]
        pp = pos.next()
        pts = list(good)
        x, y = good[pp]
        if mk == "swap":
            pts[pp] = (y, x)
            why = "It is at %s, but the pair is %s: x and y are switched." % (pair(y, x), pair(x, y))
        elif pp == 0:
            pts[pp] = (x, y + q)
            why = ("It is at %s, but %s should be the ratio itself, %s. The point is one group too high."
                   % (pair(x, y + q), "the first point", pair(x, y)))
        else:
            pts[pp] = (x, q + (x - p))
            why = ("It is at %s. That adds %d to both numbers of %s. The correct point is %s."
                   % (pair(x, q + (x - p)), x - p, pair(p, q), pair(x, y)))
        nx = max(6, max(c[0] for c in pts) + 1)
        ny = max(6, max(c[1] for c in pts) + 1)
        G = Grid(nx, ny, xt=xt, yt=yt)
        G.point(0, 0, None)
        for c, L in zip(pts, LET):
            G.point(c[0], c[1], L)
        q_ = (fig(G.svg()) + "Points P, Q, R and S should show the ratio %s and equivalent ratios %s, %s and %s. "
              "Which point was plotted wrong?" % (rat(p, q), rat(2 * p, 2 * q), rat(3 * p, 3 * q), rat(4 * p, 4 * q)))
        its.append(mcq_fixed(q_, LET, LET[pp], "Point %s. " % LET[pp] + why))
    # D: read a value from the graph
    for intro, xt, yt, p, q, sx, sy, nx, ny, ask, unit_y in [
        ("how far a car goes over time.", "Time (hours)", "Distance (miles)", 1, 50, 1, 50, 6, 6,
         "How far does the car go in 4 hours?", unit("mile", "miles")),
        ("the cost of grapes by the pound.", "Grapes (pounds)", "Cost ($)", 1, 3, 1, 3, 6, 6,
         "How much do 5 pounds of grapes cost?", money),
        ("how many muffins a recipe makes from cups of flour.", "Flour (cups)", "Muffins", 2, 12, 2, 12, 5, 5,
         "How many muffins can you make with 8 cups of flour?", unit("muffin", "muffins")),
    ]:
        G = Grid(nx, ny, sx=sx, sy=sy, xt=xt, yt=yt)
        for k in range(0, nx * sx // p + 1):
            if k * q <= ny * sy:
                G.data_point(k * p, k * q, None)
        xv = int(re.search(r"(\d+) (hours|pounds|cups)", ask).group(1))
        ans = xv // p * q
        e = ("Find %d on the x-axis, go up to the point, then across to the y-axis: %s. Each grid space on the y-axis "
             "is %s, so count by %s." % (xv, f(ans), f(sy), f(sy)))
        its.append(mcq_num(fig(G.svg()) + "The graph shows " + intro + " " + ask, ans,
                           [xv // sx, ans + q, ans - q, xv * p + q], e, fmt=unit_y))
    # E: ideas about the graph
    its.append(mcq("Equivalent ratios such as 1 : 3, 2 : 6 and 3 : 9 are plotted as (x, y). What do you notice about the points?",
                   "They lie on a straight line through (0, 0)",
                   ["They make a curve", "They lie on a line through (0, 3)", "They go down to the right"],
                   "Each step goes right 1 and up 3, the same move every time, so the points line up. "
                   "0 : 0 is also equivalent, so the line goes through (0, 0).", rnd))
    its.append(mcq("Cups of juice and cups of water are plotted as (juice, water). What does the point (0, 0) mean?",
                   "0 cups of juice need 0 cups of water",
                   ["The recipe has no ratio", "The graph starts at 1", "Juice and water are equal"],
                   "(0, 0) means x = 0 and y = 0: no juice goes with no water. Every graph of equivalent ratios goes through it.", rnd))
    its.append(mcq("The points (2, 5), (4, 10) and (6, 15) are on a graph of equivalent ratios. How do you move from one point to the next?",
                   "Right 2, up 5", ["Right 5, up 2", "Right 2, up 2", "Right 1, up 5"],
                   "x grows by 2 (2, 4, 6) and y grows by 5 (5, 10, 15). So each move is right 2, up 5.", rnd))
    its.append(mcq("Hours worked and dollars earned are plotted as (hours, dollars). The points are (1, 12), (2, 24) and (3, 36). "
                   "Which point is also on the graph?", "(5, 60)", ["(60, 5)", "(5, 48)", "(4, 40)"],
                   "Each hour is worth $12, so 5 hours go with 5 × 12 = 60 dollars: (5, 60). (60, 5) switches x and y, "
                   "(5, 48) is only 4 × 12, and (4, 40) should be (4, 48).", rnd))
    its.append(mcq("A ratio table for 3 : 4 is plotted. Which point is <b>not</b> on the graph?",
                   "(6, 7)", ["(6, 8)", "(9, 12)", "(12, 16)"],
                   "(6, 8) = 2 × (3, 4), (9, 12) = 3 × (3, 4) and (12, 16) = 4 × (3, 4). (6, 7) adds 3 to both numbers, "
                   "so it is not equivalent.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Plot ratio pairs on the coordinate plane", "items": its}


# ------------------------------------------------------------ set 5: compare ratios and word problems
def common(a, b):
    return a * b // math.gcd(a, b)


def set_words(rnd):
    its = []
    # compare two ratios: (question, name A, (x, y), name B, (x, y), same-y compare, words)
    CH = ["Mix A", "Mix B", "They are the same", "You cannot tell"]
    for xa, ya, xb, yb in [(2, 3, 3, 5), (3, 4, 5, 8), (1, 2, 3, 6), (4, 5, 3, 4)]:
        w = common(ya, yb)
        ja, jb = xa * w // ya, xb * w // yb
        if ja > jb:
            right = "Mix A"
        elif jb > ja:
            right = "Mix B"
        else:
            right = "They are the same"
        def same(x, y, j):
            return "%s = %s" % (rat(x, y), rat(j, w)) if y != w else "%s already has %d cups of water" % (rat(x, y), w)
        e = ("Make the water the same in both tables: %d cups. Mix A: %s. Mix B: %s. "
             % (w, same(xa, ya, ja), same(xb, yb, jb)))
        if right == "They are the same":
            e += "Both have %d cups of juice for %d cups of water, so they taste the same. (Mix B is just a bigger batch.)" % (ja, w)
        else:
            e += "With the same water, %s has more juice, so it tastes stronger." % right
            other = "Mix B" if right == "Mix A" else "Mix A"
            if (xb if other == "Mix B" else xa) > (xa if other == "Mix B" else xb):
                e += " (%s uses more cups of juice, but also more water.)" % other
        tA = table_fig([(xa * k, ya * k) for k in range(1, max(w // ya, 3) + 1)][:5], "Juice (cups)", "Water (cups)", label="ratio table for Mix A")
        tB = table_fig([(xb * k, yb * k) for k in range(1, max(w // yb, 3) + 1)][:5], "Juice (cups)", "Water (cups)", label="ratio table for Mix B")
        q_ = ("<p>Mix A uses %s of juice for every %d cups of water. Mix B uses %d cups of juice for every %d cups of water.</p>"
              % ("1 cup" if xa == 1 else "%d cups" % xa, ya, xb, yb) +
              "Make a ratio table for each mix. Which mix tastes more strongly of juice?")
        its.append(mcq_fixed(q_, CH, right, e))
    # readers, speed, prices (text only)
    its.append(mcq("Mia reads 12 pages in 15 minutes. Jon reads 20 pages in 30 minutes. Who reads faster?",
                   "Mia", ["Jon", "They read at the same speed", "Jon, because 20 is more than 12"],
                   "Make the time the same: 30 minutes. Mia: 12 : 15 = 24 : 30. Jon: 20 : 30. In 30 minutes Mia reads 24 pages "
                   "and Jon reads 20, so Mia is faster.", rnd))
    its.append(mcq("Store A sells 3 pens for $2. Store B sells 5 pens for $3. Which is the better buy?",
                   "Store B", ["Store A", "They cost the same per pen", "Store A, because $2 is less than $3"],
                   "Make the number of pens the same: 15. Store A: 3 : 2 = 15 : 10, so $10. Store B: 5 : 3 = 15 : 9, so $9. "
                   "Store B is cheaper for the same pens.", rnd))
    its.append(mcq("Ruby runs 4 laps in 10 minutes. Eli runs 6 laps in 15 minutes. Who runs faster?",
                   "They run at the same speed", ["Ruby", "Eli", "Eli, because 6 laps is more"],
                   "Make the time the same: 30 minutes. Ruby: 4 : 10 = 12 : 30. Eli: 6 : 15 = 12 : 30. Both run 12 laps in "
                   "30 minutes, so their speeds are the same.", rnd))
    its.append(mcq("Car A goes 90 miles on 3 gallons of gas. Car B goes 140 miles on 5 gallons. Which car goes farther on the same gas?",
                   "Car A", ["Car B", "They go the same distance", "Car B, because 140 is more than 90"],
                   "Make the gas the same: 15 gallons. Car A: 90 : 3 = 450 : 15. Car B: 140 : 5 = 420 : 15. "
                   "Car A goes 450 miles and Car B goes 420 miles.", rnd))
    # missing value word problems
    W = [
        ("A recipe uses 3 cups of flour for every 2 cups of sugar. How much flour goes with 8 cups of sugar?",
         12, [9, 8, 15], "8 ÷ 2 = 4, so multiply both by 4: 3 × 4 = 12 cups of flour. (Adding 6 to both gives 9, "
         "but adding does not keep the ratio.)", unit("cup", "cups")),
        ("A field trip needs 1 adult for every 6 students. How many adults are needed for 42 students?",
         7, [37, 252, 8], "42 ÷ 6 = 7, so there are 7 groups of 6 students and 1 × 7 = 7 adults. "
         "(42 × 6 = 252 multiplies when you need to divide.)", unit("adult", "adults")),
        ("Lily earns $45 for 3 hours of babysitting. At the same rate, how much does she earn for 7 hours?",
         105, [49, 135, 90], "First find 1 hour: $45 ÷ 3 = $15. Then 7 × $15 = $105. (Adding 4 to $45 gives $49.)", money),
        ("Noah's printer prints 18 pages in 3 minutes. How many pages does it print in 10 minutes?",
         60, [25, 54, 180], "1 minute: 18 ÷ 3 = 6 pages. 10 minutes: 10 × 6 = 60 pages. "
         "(Adding 7 to both gives 25 pages.)", unit("page", "pages")),
        ("A paint mix uses 2 cans of yellow for every 5 cans of blue. Sofia uses 20 cans of blue. How many cans of yellow does she need?",
         8, [17, 50, 10], "20 ÷ 5 = 4, so multiply both by 4: 2 × 4 = 8 cans of yellow. "
         "(50 multiplies the wrong number: it reads the other row.)", unit("can", "cans")),
        ("A school orders 4 boxes of markers for every 3 classrooms. How many boxes does it need for 24 classrooms?",
         32, [25, 18, 28], "24 ÷ 3 = 8, so multiply both by 8: 4 × 8 = 32 boxes. "
         "(Adding 21 to both gives 25 boxes. 18 switches the two quantities.)", unit("box", "boxes")),
        ("A runner keeps the same pace and covers 5 kilometers in 25 minutes. How long does she take for 3 kilometers?",
         15, [23, 75, 10], "1 kilometer: 25 ÷ 5 = 5 minutes. 3 kilometers: 3 × 5 = 15 minutes. "
         "(Subtracting 2 from both gives 23, but subtracting does not keep the ratio.)", unit("minute", "minutes")),
        ("A concert hall has 2,000 seats in 40 equal rows. How many seats are in 15 rows?",
         750, [1975, 600, 800], "1 row: 2,000 ÷ 40 = 50 seats. 15 rows: 15 × 50 = 750 seats. "
         "(Subtracting 25 from both gives 1,975.)", unit("seat", "seats")),
        ("Owen mixes 1 scoop of plant food into every 4 liters of water. His watering can holds 12 liters. "
         "How many scoops does he use?", 3, [9, 48, 4], "12 ÷ 4 = 3, so he uses 1 × 3 = 3 scoops. "
         "(Adding 8 to both gives 9 scoops, and 48 multiplies instead of dividing.)", unit("scoop", "scoops")),
        ("In a club, the ratio of boys to girls is 3 : 5. There are 15 boys. How many girls are there?",
         25, [17, 9, 40], "15 ÷ 3 = 5, so multiply both by 5: 5 × 5 = 25 girls. "
         "(Adding 12 to both gives 17. 9 uses the ratio backward: 15 ÷ 5 × 3.)", unit("girl", "girls")),
        ("On a map, 2 inches stand for 25 miles. How many miles do 8 inches stand for?",
         100, [31, 200, 50], "8 ÷ 2 = 4, so multiply both by 4: 25 × 4 = 100 miles. "
         "(Adding 6 to both gives 31. 8 × 25 = 200 forgets that 25 miles goes with 2 inches, not 1 inch.)", unit("mile", "miles")),
        ("A bakery uses 6 eggs for every 4 cakes. How many eggs does it need for 10 cakes?",
         15, [12, 60, 18], "First find 2 cakes: 6 ÷ 2 = 3 eggs. 10 cakes is 5 groups of 2: 5 × 3 = 15 eggs. "
         "(Adding 6 to both gives 12.)", unit("egg", "eggs")),
    ]
    for q_, ans, wrong, e, fm in W:
        ch = []
        for c in wrong:
            if c != ans and c not in ch and c > 0:
                ch.append(c)
        assert len(ch) == 3, q_
        its.append({"q": q_, "c": [fm(c) for c in ch] + [fm(ans)], "a": 3, "e": e})
    assert len(its) == 20, len(its)
    return {"title": "Compare ratios and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    t1 = ratio_table([2, 4, 6, 8, 10], [3, 6, 9, 12, "?"], "Juice (cups)", "Water (cups)",
                     "ratio table for 2 cups of juice to 3 cups of water")
    line = dnl([0, 1, 2, 3, 4], 2, 3, "Juice (cups)", "Water (cups)", None,
               "double number line for 2 cups of juice to 3 cups of water")
    G = Grid(10, 10, xt="Juice (cups)", yt="Water (cups)")
    for k in range(4):
        G.point(2 * k, 3 * k, None)
    G.line(0, 0, 6, 9)
    G.note(6.3, 9, "(6, 9)", anchor="start")
    graph = G.svg("graph of the ratio pairs (0, 0), (2, 3), (4, 6), (6, 9)")
    return (
        "<h2>What is a ratio table?</h2>"
        "<p>A ratio table lists <b>equivalent ratios</b>. To make the next column, <b>multiply (or divide) both quantities "
        "by the same number</b>. Never add the same amount to both.</p>"
        "<figure class='sn-fig'>" + t1 +
        "<figcaption>A fruit punch uses 2 cups of juice for every 3 cups of water. Each column is 2 : 3 times a number.</figcaption></figure>" +
        ex("Example", "Find the ? in the table above.",
           "In the top row, 2 × 5 = 10. Multiply the bottom row by 5 too: 3 × 5 = 15.", "15 cups of water") +
        ex("Example", "6 cans of soup cost $9. How much do 2 cans cost?",
           "6 ÷ 3 = 2, so divide the cost by 3 too: $9 ÷ 3 = $3.", "$3") +
        "<h2>Double number lines</h2>"
        "<p>A double number line shows the same ratios on two lines. Values that line up go together. Both lines start at 0, "
        "and equal steps get equal spaces.</p>"
        "<figure class='sn-fig'>" + line + "<figcaption>2 cups of juice line up with 3 cups of water, 4 with 6, 6 with 9.</figcaption></figure>"
        "<h2>Plot the pairs on a graph</h2>"
        "<p>Write each column as an ordered pair (top, bottom) and plot it: go right by the first number and up by the second. "
        "Equivalent ratios always lie on a <b>straight line through (0, 0)</b>.</p>"
        "<figure class='sn-fig'>" + graph +
        "<figcaption>Each step goes right 2 and up 3. You can read new pairs from the line.</figcaption></figure>"
        "<h2>Compare two ratios</h2>"
        "<p>Make one quantity the same in both tables, then compare the other quantity.</p>" +
        ex("Example", "Mix A uses 2 cups of juice for 3 cups of water. Mix B uses 3 cups of juice for 5 cups of water. Which is stronger?",
           "Make the water 15 cups. Mix A: 2 : 3 = 10 : 15. Mix B: 3 : 5 = 9 : 15. Mix A has more juice for the same water.",
           "Mix A") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the same amount: 2 : 3, 4 : 5, 6 : 7", "Multiply both: 2 : 3, 4 : 6, 6 : 9"],
            ["Reading the wrong row", "Check which quantity the question asks for"],
            ["Switching x and y: plotting (3, 2) for 2 : 3", "First number across, second number up: (2, 3)"],
            ["Comparing only the first numbers: 3 cups is more than 2 cups", "Make one quantity the same, then compare"],
        ])
    )


FAQ = [
    {"q": "What does 6.RP.A.3a mean?",
     "a": "It is the Common Core Grade 6 standard for making tables of equivalent ratios, finding missing values, plotting the pairs on the coordinate plane and using tables to compare ratios."},
    {"q": "How do you find a missing value in a ratio table?",
     "a": "Find the number that one quantity was multiplied or divided by, then do the same to the other quantity. For 2 : 3 and 10 : ?, 2 × 5 = 10, so 3 × 5 = 15."},
    {"q": "Why can’t you add the same number to both parts of a ratio?",
     "a": "Adding changes how the two quantities compare. 2 : 3 and 4 : 5 are not equivalent, because 2 × 2 = 4 but 3 × 2 = 6, not 5."},
    {"q": "How do you compare two ratios with tables?",
     "a": "Extend both tables until one quantity is the same, then compare the other one. For 2 : 3 and 3 : 5, make the second number 15: 10 : 15 is more than 9 : 15."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Fixed-order choices stay as they are."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [max(0, 5 - c) for c in cnt]
        assert sum(need) == len(free), (s["title"], cnt, len(free))
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_ratio_tables():
    rnd = random.Random(603)
    sets = [set_tables(rnd), set_lines(rnd), set_equiv(rnd), set_graph(rnd), set_words(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "ratio-tables", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Ratio Tables: Equivalent Ratios, Double Number Lines and Graphs",
        "seo_title": "Grade 6 Ratio Tables Worksheets: Missing Values, Double Number Lines, Graphs and Comparing Ratios (6.RP.A.3a)",
        "short_title": "Ratio tables",
        "domain": "Ratios and Proportional Relationships",
        "standard_code": "6.RP.A.3a",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/RP/A/3/",
        "standard_text": "Make tables of equivalent ratios relating quantities with whole-number measurements, find missing values in the tables, and plot the pairs of values on the coordinate plane. Use tables to compare ratios.",
        "meta_desc": "Free Grade 6 ratio tables worksheets: find missing values in tables of equivalent ratios, use double number lines, spot errors, plot ratio pairs on the coordinate plane and compare ratios in word problems. 100 practice questions with an answer key.",
        "key_big": "In a ratio table, multiply or divide both quantities by the same number. 2 : 3 = 4 : 6 = 10 : 15.",
        "key_sub": "Never add the same amount to both (4 : 5 is not equivalent to 2 : 3). Plotted as (x, y), equivalent ratios lie on a straight line through (0, 0). To compare two ratios, make one quantity the same.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables, number lines and graphs) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            if it["q"].count("<svg") > 1:
                continue    # two tables in one question: keep them normal size so the page fits
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_ratio_tables()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(ratio table|double number line|graph of)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
