# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 7 Math: Proportional reasoning
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 7, Number, B2.10)
  python3 tools/gen_caon_math_g7_proportional.py
Proportional or not (tables, graphs through the origin, y = kx, situations); unit rates and the constant
of proportionality; equivalent ratios and proportions; solving proportions (3/5 = x/20); word problems
(recipes, speed, best buys, map scales).
Wrong answers come from real mistakes, above all additive instead of multiplicative thinking
(3/5 = x/20 gives 18), a straight line that misses (0, 0) called proportional, reversed rates,
multiplying instead of dividing, and unit mix-ups on map scales.
Every answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
NBSP = " "
FILL = "#4fae74"
LIGHT = "#eef6f0"
LINE = "#2b2b2b"
GRID = "#c9d6cd"
RED = "#d6453b"
BLUE = "#2f6fc0"
GREEN = "#006633"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
X = "<i>x</i>"
Y = "<i>y</i>"
CANT = "You can’t tell"


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 50000 -> '50 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def money(x):
    """$45, $25.50, 75¢ under $1."""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
    if c % 100:
        return "$%s.%02d" % (num(c // 100), c % 100)
    return "$" + num(c // 100)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def R(*t):
    return ":".join(num(x) if not isinstance(x, str) else x for x in t)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
RAT = re.compile(r"^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = RAT.match(c)
    if m:
        return (F(m.group(1)) / F(m.group(2)), "ratio")
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(NBSP, ""))
    if (m.group(1) or m.group(3) == "¢") and m.group(4):
        return None
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        return None if m.group(4) else (v, "%")
    return (v, (m.group(4) or "").strip())


def mcq(q, right, wrong, e, value=None, same_ok=False, fix=None):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value (unless same_ok).
    value: the exact answer, checked against the correct choice.
    fix: for picture labels (A, B, C, D) — the choices stay in this order and the answer is at index fix."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
    if not same_ok:
        known = [v for v in (val(x) for x in ch) if v is not None]
        assert len(set(known)) == len(known), (q, ch)
    if fix is not None:
        order = sorted(ch, key=plain)
        assert order[fix] == right, (q, order, fix)
        return {"q": q, "c": order, "a": fix, "e": e, "fix": True}
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each).
    Items with fixed A–D choices keep their place; the others fill the remaining slots."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fix", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


# ------------------------------------------------------------ svg helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700, italic=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, " font-style='italic'" if italic else "", col, anchor, t))


def tw(t, fs):
    """Rough width of bold Arial text."""
    return len(plain(t)) * fs * 0.62


def cell(v):
    return v if isinstance(v, str) else num(v)


def tov_svg(heads, top, bot, label="table of values"):
    """Two-row table. heads: row headings; top, bot: the cells ('?' in red)."""
    fs = 16
    top, bot = [cell(v) for v in top], [cell(v) for v in bot]
    hw = max(tw(h, fs) for h in heads) + 20
    cw = max([44] + [tw(c, fs) + 20 for c in top + bot])
    rh = 34
    n = len(top)
    W, H = 4 + hw + n * cw + 4, 4 + 2 * rh + 4
    s = ["<rect x='4' y='4' width='%.1f' height='%d' fill='%s'/>" % (hw, 2 * rh, LIGHT)]
    for j, (hd, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 4 + j * rh
        s.append(text(4 + hw / 2, y + rh / 2 + 5.5, hd, fs, italic=len(hd) == 1))
        for i, c in enumerate(row):
            s.append(text(4 + hw + i * cw + cw / 2, y + rh / 2 + 5.5, c, fs, col=RED if c == "?" else LINE))
    for j in range(3):
        s.append("<line x1='4' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (4 + j * rh, 4 + hw + n * cw, 4 + j * rh, LINE))
    for i in range(n + 1):
        x = 4 + hw + i * cw
        s.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, x, 4 + 2 * rh, LINE))
    s.append("<line x1='4' y1='4' x2='4' y2='%d' stroke='%s' stroke-width='2'/>" % (4 + 2 * rh, LINE))
    return svg_wrap(W, H, "".join(s), label)


def tables4_svg(groups, label="four tables of values"):
    """Four small x–y tables labelled A, B, C, D in one picture. groups: [(xs, ys)] * 4."""
    fs, rh, hw, cw, gap = 15, 28, 24, 34, 16
    n = len(groups[0][0])
    TW = hw + n * cw
    W = 4 + 4 * TW + 3 * gap + 4
    H = 26 + 2 * rh + 4
    s = []
    for g, (xs, ys) in enumerate(groups):
        ox, oy = 4 + g * (TW + gap), 26
        s.append(text(ox + TW / 2, 19, "ABCD"[g], 17, col=GREEN))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox, oy, hw, 2 * rh, LIGHT))
        for j, (hd, row) in enumerate([("x", xs), ("y", ys)]):
            y = oy + j * rh
            s.append(text(ox + hw / 2, y + rh / 2 + 5, hd, fs, italic=True))
            for i, v in enumerate(row):
                s.append(text(ox + hw + i * cw + cw / 2, y + rh / 2 + 5, cell(v), fs))
        for j in range(3):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (ox, oy + j * rh, ox + TW, oy + j * rh, LINE))
        for i in range(n + 1):
            x = ox + hw + i * cw
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, oy, x, oy + 2 * rh, LINE))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (ox, oy, ox, oy + 2 * rh, LINE))
    return svg_wrap(W, H, "".join(s), label)


def graph_svg(pts, xmax, ymax, ystep=1, ylab=2, xname="x", yname="y", label="graph", line=True):
    """First-quadrant graph, drawn exactly to the grid: points (red) joined by a line."""
    XU = 30
    PH = 180.0
    YU = PH / ymax
    ylabels = [(g, num(g)) for g in range(0, ymax + 1, ylab)]
    LW = max(tw(t, 14) for _, t in ylabels)
    long_y = len(yname) > 1
    L = (30 if long_y else 24) + LW + 8
    T, Rm, B = 14, 16, 46
    X0, Y0 = L, T + PH
    W = L + xmax * XU + Rm
    H = T + PH + B
    s = []
    for g in range(0, ymax + 1, ystep):
        y = Y0 - g * YU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + xmax * XU, y, GRID))
    for g, t in ylabels:
        s.append(text(X0 - 7, Y0 - g * YU + 5, t, 14, "end", weight=400))
    for g in range(0, xmax + 1):
        x = X0 + g * XU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, T, x, Y0, GRID))
        s.append(text(x, Y0 + 19, num(g), 14, weight=400))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + xmax * XU, Y0, LINE))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, T, X0, Y0, LINE))
    s.append(text(X0 + xmax * XU / 2, H - 6, xname, 15, italic=len(xname) == 1))
    if long_y:
        cy = T + PH / 2
        s.append("<text x='16' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle' "
                 "transform='rotate(-90 16 %.1f)'>%s</text>" % (cy, LINE, cy, yname))
    else:
        s.append(text(X0 - LW - 18, T + PH / 2 + 6, yname, 17, italic=True))
    xy = []
    for px, py in pts:
        assert 0 <= px <= xmax and 0 <= py <= ymax, (px, py)
        xy.append((X0 + float(F(px) * XU), Y0 - float(F(py) * F(YU))))
    if line and len(xy) > 1:
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (" ".join("%.1f,%.1f" % p for p in xy), BLUE))
    for cx, cy in xy:
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
    return svg_wrap(W, H, "".join(s), label)


def panels_svg(groups, label="four graphs"):
    """Four small graphs A, B, C, D (x and y from 0 to 8) in one picture; points joined by a line."""
    U, N = 13, 8
    PL, PT, PB, PR, GAP = 22, 26, 22, 10, 14
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
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + N * U, Y0, LINE))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X0, PT, X0, Y0, LINE))
        s.append(text(X0 - 4, Y0 + 16, "0", 14, "end", weight=400))
        for g in (4, 8):
            s.append(text(X0 + g * U, Y0 + 16, str(g), 14, weight=400))
            s.append(text(X0 - 4, Y0 - g * U + 5, str(g), 14, "end", weight=400))
        xy = []
        for px, py in pts:
            assert 0 <= px <= N and 0 <= py <= N
            xy.append((X0 + float(F(px) * U), Y0 - float(F(py) * U)))
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.2'/>"
                 % (" ".join("%.1f,%.1f" % p for p in xy), BLUE))
        for cx, cy in xy:
            s.append("<circle cx='%.1f' cy='%.1f' r='3.6' fill='%s'/>" % (cx, cy, RED))
    return svg_wrap(W, H, "".join(s), label)


def scale_bar_svg(cm, km, parts):
    """Map scale bar: `parts` alternating blocks; the whole bar is `cm` cm on the map and stands for `km` km."""
    PX = 60  # drawing units per centimetre (the bar is a picture, not to real size)
    Lx = 16
    bw = cm * PX
    s = []
    seg = bw / float(parts)
    for i in range(parts):
        s.append("<rect x='%.1f' y='30' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (Lx + i * seg, seg, LINE if i % 2 == 0 else "#ffffff", LINE))
    for i in range(parts + 1):
        s.append(text(Lx + i * seg, 22, num(F(km * i, parts)), 14, weight=400))
    s.append(text(Lx + bw + 10, 42, "km", 15, "start"))
    s.append("<line x1='%d' y1='58' x2='%d' y2='58' stroke='%s' stroke-width='1.6'/>" % (Lx, Lx + bw, BLUE))
    for x in (Lx, Lx + bw):
        s.append("<line x1='%d' y1='52' x2='%d' y2='64' stroke='%s' stroke-width='1.6'/>" % (x, x, BLUE))
    s.append(text(Lx + bw / 2, 80, "%s cm on the map" % num(cm), 14, col=BLUE))
    W = Lx + bw + 10 + tw("km", 15) + 6
    return svg_wrap(W, 88, "".join(s), "map scale bar: %s cm stands for %s km" % (num(cm), num(km)))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def is_prop(xs, ys):
    """True when every (x, y) has the same y ÷ x and (0, 0) fits."""
    ks = set()
    for x, y in zip(xs, ys):
        if x == 0:
            if y != 0:
                return False
            continue
        ks.add(F(y) / F(x))
    return len(ks) == 1


def tbl(xs, ys, heads=("x", "y"), label="table of values"):
    return fig(tov_svg(heads, xs, ys, label))


def solve(a, b, c=None, d=None):
    """a/b = c/d with exactly one None; returns the missing value."""
    a, b = (None if a is None else F(a)), (None if b is None else F(b))
    c, d = (None if c is None else F(c)), (None if d is None else F(d))
    if a is None:
        return b * c / d
    if b is None:
        return a * d / c
    if c is None:
        return a * d / b
    return b * c / a


# ============================================================ set 1: proportional or not
def set_decide(P):
    its = []
    YES_K = lambda k: "Yes: %s ÷ %s is always %s" % (Y, X, k)
    xs, ys = [1, 2, 3, 4], [4, 8, 12, 16]
    assert is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), YES_K(4),
                   ["No: %s ÷ %s changes" % (Y, X), "No: the table does not start at 0", "Yes: %s − %s is always 3" % (Y, X)],
                   "4 ÷ 1 = 4, 8 ÷ 2 = 4, 12 ÷ 3 = 4, 16 ÷ 4 = 4. The ratio is the same every time, so <b>yes</b>: %s = 4%s. "
                   "%s − %s is 3, 6, 9, 12, so it is not always 3. A table does not need a 0 column." % (Y, X, Y, X)))
    xs, ys = [1, 2, 3, 4], [5, 7, 9, 11]
    assert not is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), "No: %s ÷ %s is not always the same" % (Y, X),
                   ["Yes: %s goes up by 2 each time" % Y, "Yes: %s ÷ %s is always 5" % (Y, X), "Yes: %s ÷ %s is always 2" % (Y, X)],
                   "5 ÷ 1 = 5 but 7 ÷ 2 = 3.5, so the ratio changes: <b>not proportional</b>. Going up by the same amount "
                   "is not enough (that is adding, not multiplying). If you go back one step, %s = 0 gives %s = 3, not 0." % (X, Y)))
    xs, ys = [2, 4, 6, 8], [3, 6, 9, 12]
    assert is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), YES_K("1.5"),
                   ["No: %s ÷ %s is not a whole number" % (Y, X), "Yes: %s is always 1 more than %s" % (Y, X),
                    "No: %s goes up by 3 but %s goes up by 2" % (Y, X)],
                   "3 ÷ 2 = 6 ÷ 4 = 9 ÷ 6 = 12 ÷ 8 = 1.5. <b>Yes</b>: %s = 1.5%s. The constant does not have to be a whole "
                   "number. 6 is 2 more than 4, so “1 more” is true only in the first column." % (Y, X)))
    xs, ys = [1, 2, 3, 4], [10, 20, 30, 45]
    assert not is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), "No: 45 ÷ 4 is not 10",
                   [YES_K(10), "Yes: %s always goes up" % Y, "No: %s goes up by 10 each time" % Y],
                   "10 ÷ 1, 20 ÷ 2 and 30 ÷ 3 are all 10, but 45 ÷ 4 = 11.25. Check <b>every</b> column: "
                   "<b>not proportional</b>. For 4 the value would have to be 40."))
    T = [([1, 2, 3], [3, 5, 7]), ([1, 2, 3], [4, 8, 12]), ([2, 4, 6], [3, 5, 7]), ([1, 2, 3], [2, 4, 7])]
    assert [is_prop(*t) for t in T] == [False, True, False, False]
    its.append(mcq(fig(tables4_svg(T)) + "Which table shows a proportional relationship?", "Table B",
                   ["Table A", "Table C", "Table D"],
                   "In Table B, 4 ÷ 1 = 8 ÷ 2 = 12 ÷ 3 = 4, so <b>Table B</b>. Table A goes up by 2 each time, "
                   "but 3 ÷ 1 = 3 and 5 ÷ 2 = 2.5. Table D starts like doubling, but 7 is not 2 × 3.", fix=1))
    G = [[(0, 0), (2, 4), (4, 6), (6, 7)], [(0, 0), (2, 2), (4, 4), (6, 6), (8, 8)],
         [(0, 2), (2, 4), (4, 6), (6, 8)], [(0, 0), (2, 1), (4, 3), (6, 6)]]
    its.append(mcq(fig(panels_svg(G)) + "Which graph shows a proportional relationship?", "Graph B",
                   ["Graph A", "Graph C", "Graph D"],
                   "A proportional graph is a <b>straight line through (0, 0)</b>. <b>Graph B</b> is. "
                   "Graph C is straight but starts at (0, 2). Graphs A and D start at (0, 0) but bend, "
                   "so %s ÷ %s changes." % (Y, X), fix=1))
    pts = [(0, 2), (1, 4), (2, 6), (3, 8), (4, 10)]
    its.append(mcq(fig(graph_svg(pts, 5, 12, 1, 2, label="graph of a straight line that starts at (0, 2)")) +
                   "Is %s proportional to %s?" % (Y, X), "No: the line does not pass through (0, 0)",
                   ["Yes: the points are on a straight line", "Yes: %s goes up by 2 each time" % Y,
                    "No: the points are not on a straight line"],
                   "When %s = 0, %s = 2, not 0. So %s ÷ %s changes (4 ÷ 1 = 4, 6 ÷ 2 = 3): <b>not proportional</b>. "
                   "A straight line is not enough; it must also go through (0, 0)." % (X, Y, Y, X)))
    pts = [(0, 0), (2, 5), (4, 10), (6, 15)]
    its.append(mcq(fig(graph_svg(pts, 6, 16, 1, 2, label="graph of a straight line through (0, 0)")) +
                   "Is %s proportional to %s?" % (Y, X), "Yes: a straight line through (0, 0)",
                   ["No: %s ÷ %s is not a whole number" % (Y, X), "No: the points are not on a straight line",
                    "No: the graph must start at (1, 1)"],
                   "The points lie on a straight line that starts at (0, 0), so <b>yes</b>. 5 ÷ 2 = 10 ÷ 4 = 15 ÷ 6 = 2.5, "
                   "and a constant like 2.5 is fine."))
    its.append(mcq("Which situation is proportional?", "Apples cost $3 per kilogram.",
                   ["A taxi charges $4 plus $2 per kilometre.", "A gym charges $50 to join plus $20 a month.",
                    "A plant is 5 cm tall and grows 2 cm a week."],
                   "0 kg of apples costs $0, and 2 kg costs exactly twice as much as 1 kg: <b>proportional</b>. "
                   "The other three have a starting amount ($4, $50, 5 cm), so the total for 0 is not 0."))
    its.append(mcq("Which situation is <b>not</b> proportional?", "Bowling costs $5 for shoes plus $4 per game.",
                   ["Gas costs $1.50 per litre.", "A car drives at a steady 90 km/h.",
                    "Each bag of milk holds 1.33 L."],
                   "Bowling 0 games still costs $5 for shoes, and 2 games ($13) is not twice 1 game ($9): "
                   "<b>not proportional</b>. In the other three, double one amount and the other doubles too."))
    its.append(mcq("Arjun is 12 years old and his sister Leah is 6. Is Arjun’s age proportional to Leah’s age as they grow up?",
                   "No: the difference stays 6, so the ratio changes",
                   ["Yes: he will always be twice her age", "Yes: their ages both go up by 1 each year",
                    "No: Arjun is older"],
                   "Now 12:6 = 2:1. In 6 years they are 18 and 12, which is 3:2, not 2:1. The ages keep the same "
                   "<b>difference</b> (adding), not the same <b>ratio</b>, so they are <b>not proportional</b>."))
    xs, ys = [0, 1, 2, 3], [0, 7, 14, 21]
    assert is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), "Yes: %s = 7%s in every column" % (Y, X),
                   ["No: 0 ÷ 0 cannot be found", "No: %s goes up by 7, not by 1" % Y, "Yes: %s goes up by 1 each time" % X],
                   "7 × 0 = 0, 7 × 1 = 7, 7 × 2 = 14, 7 × 3 = 21. Every column fits %s = 7%s, and (0, 0) is in the "
                   "table: <b>yes</b>. %s going up by 1 says nothing about proportion." % (Y, X, X)))
    xs, ys = [0, 1, 2, 3], [3, 5, 7, 9]
    assert not is_prop(xs, ys)
    its.append(mcq(tbl(xs, ys) + "Is %s proportional to %s?" % (Y, X), "No: when %s is 0, %s is 3" % (X, Y),
                   ["Yes: %s goes up by 2 each time" % Y, "Yes: %s ÷ %s is always 5" % (Y, X),
                    "Yes: %s and %s are whole numbers" % (X, Y)],
                   "A proportional relationship has %s = 0 when %s = 0. Here %s = 3 at the start, so it is "
                   "<b>not proportional</b>. Going up by 2 each time makes a straight line, but not one through (0, 0)."
                   % (Y, X, Y)))
    T = [([2, 3, 5], [6, 9, 15]), ([4, 6, 8], [2, 3, 4]), ([1, 3, 4], [3, 5, 6]), ([3, 6, 9], [5, 10, 15])]
    assert [is_prop(*t) for t in T] == [True, True, False, True]
    its.append(mcq(fig(tables4_svg(T)) + "Which table is <b>not</b> proportional?", "Table C",
                   ["Table A", "Table B", "Table D"],
                   "Table C: 3 ÷ 1 = 3 but 5 ÷ 3 is less than 2. Each %s is 2 <b>more</b> than %s (adding), so <b>Table C</b> "
                   "is not proportional. A: %s = 3%s. B: %s = 0.5%s. D: %s ÷ %s is always %s." % (Y, X, Y, X, Y, X, Y, X, fr(5, 3)),
                   fix=2))
    xs, ys = [2, 3, 5], [8, 12, "?"]
    its.append(mcq(tbl(xs, ys) + "%s is proportional to %s. What number is missing?" % (Y.capitalize(), X), "20",
                   ["16", "14", "17"],
                   "%s ÷ %s = 8 ÷ 2 = 4, so %s = 4%s. When %s = 5, %s = 4 × 5 = <b>20</b>. 16 adds 4 again, "
                   "and 14 adds 2 because %s went up by 2: both use adding instead of multiplying." % (Y, X, Y, X, X, Y, X),
                   value=20))
    assert solve(8, 2, None, 5) == 20
    its.append(mcq("%s is proportional to %s. When %s = 6, %s = 18. What is %s when %s = 10?" % (Y, X, X, Y, Y, X), "30",
                   ["22", "60", "24"],
                   "%s ÷ %s = 18 ÷ 6 = 3, so %s = 3%s. When %s = 10: 3 × 10 = <b>30</b>. 22 adds 4 because %s went up by 4. "
                   "60 multiplies 6 × 10." % (Y, X, Y, X, X, X), value=30))
    assert solve(18, 6, None, 10) == 30
    its.append(mcq("Which equation shows a proportional relationship?", "%s = 4%s" % (Y, X),
                   ["%s = %s + 4" % (Y, X), "%s = 4%s + 1" % (Y, X), "%s = 4 − %s" % (Y, X)],
                   "A proportional relationship has the form %s = <i>k</i>%s: <b>%s = 4%s</b>. With + 1 or + 4, "
                   "%s is not 0 when %s = 0." % (Y, X, Y, X, Y, X)))
    its.append(mcq("A proportional relationship passes through (2, 6). Which point is also on its graph?", "(5, 15)",
                   ["(5, 9)", "(3, 7)", "(6, 2)"],
                   "6 ÷ 2 = 3, so %s = 3%s. For %s = 5: 3 × 5 = 15, so <b>(5, 15)</b>. (5, 9) adds 3 to both "
                   "coordinates, and (6, 2) switches them." % (Y, X, X)))
    G = [[(0, 1), (2, 3), (4, 5), (6, 7)], [(0, 0), (2, 1), (4, 4), (5, 7)],
         [(0, 8), (2, 6), (4, 4), (6, 2), (8, 0)], [(0, 0), (2, 3), (4, 6)]]
    its.append(mcq(fig(panels_svg(G)) + "In which graph is %s proportional to %s?" % (Y, X), "Graph D",
                   ["Graph A", "Graph B", "Graph C"],
                   "<b>Graph D</b> is a straight line through (0, 0): 3 ÷ 2 = 6 ÷ 4 = 1.5. Graph A is straight but starts "
                   "at (0, 1). Graph B bends. Graph C goes down and starts at (0, 8).", fix=3))
    a, _, _ = P.next()
    b, _, bh = P.next()
    its.append(mcq("%s earns $15 an hour. %s earns $40 a week plus $10 an hour. Whose pay is proportional to the hours worked?"
                   % (a, b), "%s’s only" % a, ["%s’s only" % b, "Both", "Neither"],
                   "%s: 0 hours pays $0, and 2 hours ($30) is twice 1 hour ($15): proportional. %s gets $40 even for "
                   "0 hours, so %s pay is not. The answer is <b>%s’s only</b>." % (a, b, bh, a)))
    assert len(its) == 20, len(its)
    return {"title": "Proportional or not? Tables, graphs and situations", "items": its}


# ============================================================ set 2: unit rates
def set_rates(P):
    its = []
    its.append(mcq("A car travels 150 km in 2 hours at a steady speed. What is its speed?", "75 km/h",
                   ["300 km/h", "148 km/h", "152 km/h"],
                   "The unit rate is the distance in <b>1</b> hour: 150 ÷ 2 = <b>75 km/h</b>. 300 multiplies instead of "
                   "dividing, and 148 subtracts.", value=75))
    its.append(mcq("6 cans of juice cost $4.50. What is the cost of 1 can?", "75¢", ["$27", "$1.50", "45¢"],
                   "$4.50 ÷ 6 = 450¢ ÷ 6 = <b>75¢</b>. $27 multiplies, $1.50 divides by 3, "
                   "and 45¢ divides by 10.", value=F(3, 4)))
    its.append(mcq("3 kg of apples cost $7.20. What is the price per kilogram?", "$2.40", ["$21.60", "$4.20", "$10.20"],
                   "$7.20 ÷ 3 = <b>$2.40</b> per kilogram. Check: 3 × $2.40 = $7.20. $4.20 subtracts 3, and $10.20 adds 3.",
                   value=F(12, 5)))
    its.append(mcq(tbl([2, 4, 6], ["$30", "$60", "$90"], ("Hours", "Pay")) + "Hana is paid the same amount for every hour. "
                   "What is her unit rate?", "$15 per hour", ["$30 per hour", "$28 per hour", "$60 per hour"],
                   "Pay for 1 hour: $30 ÷ 2 = <b>$15 per hour</b>. Check: $60 ÷ 4 = $15 and $90 ÷ 6 = $15. "
                   "$30 is the pay for 2 hours, not 1."))
    its.append(mcq("A pump fills 2.4 L in 8 minutes. How many litres does it pump per minute?", "0.3 L",
                   ["3 L", "19.2 L", "5.6 L"],
                   "2.4 ÷ 8 = <b>0.3 L</b> per minute. Check: 8 × 0.3 = 2.4. 3 L puts the decimal point in the wrong place, "
                   "and 19.2 L multiplies.", value=F(3, 10)))
    its.append(mcq(tbl([4, 8, 12], [3, 6, 9]) + "%s is proportional to %s. What is the constant of proportionality "
                   "<i>k</i> in %s = <i>k</i>%s?" % (Y, X, Y, X), "0.75", [fr(4, 3), "3", "4"],
                   "<i>k</i> = %s ÷ %s = 3 ÷ 4 = <b>0.75</b>. Check: 0.75 × 8 = 6. %s divides the wrong way (%s ÷ %s), "
                   "and 3 is just the first %s value." % (Y, X, fr(4, 3), X, Y, Y), value=F(3, 4)))
    pts = [(0, 0), (2, 7), (4, 14), (6, 21)]
    its.append(mcq(fig(graph_svg(pts, 6, 22, 2, 4, label="graph of a straight line through (0, 0), (2, 7), (4, 14) and (6, 21)")) +
                   "The graph shows a proportional relationship. What is the constant of proportionality?",
                   "3.5", ["7", fr(2, 7), "2"],
                   "Use any point: 7 ÷ 2 = 14 ÷ 4 = 21 ÷ 6 = <b>3.5</b>. 7 is %s at (2, 7), not %s for 1. "
                   "%s divides %s by %s." % (Y, Y, fr(2, 7), X, Y), value=F(7, 2)))
    pts = [(0, 0), (3, 2), (6, 4), (9, 6)]
    its.append(mcq(fig(graph_svg(pts, 9, 7, 1, 1, label="graph of a straight line through (0, 0), (3, 2), (6, 4) and (9, 6)")) +
                   "The graph shows a proportional relationship. What is the constant of proportionality?",
                   fr(2, 3), [fr(3, 2), "2", "3"],
                   "<i>k</i> = %s ÷ %s = 2 ÷ 3 = <b>%s</b>. Check: %s × 9 = 6. %s is %s ÷ %s." % (Y, X, fr(2, 3), fr(2, 3), fr(3, 2), X, Y),
                   value=F(2, 3)))
    its.append(mcq("A Canada goose flies 135 km in 2.5 hours. What is its average speed?", "54 km/h",
                   ["337.5 km/h", "132.5 km/h", "67.5 km/h"],
                   "135 ÷ 2.5 = 1350 ÷ 25 = <b>54 km/h</b>. Check: 54 × 2.5 = 108 + 27 = 135. 67.5 divides by 2 and "
                   "forgets the half hour, and 337.5 multiplies.", value=54))
    assert F(135) / F(5, 2) == 54
    its.append(mcq("Gas costs $62.40 for 40 L. What is the price per litre?", "$1.56", ["$15.60", "$22.40", "$2496"],
                   "$62.40 ÷ 40 = <b>$1.56</b> per litre. Check: 40 × $1.56 = $62.40. $15.60 is 10 times too big, "
                   "and $22.40 subtracts 40.", value=F(156, 100)))
    its.append(mcq("Sofia runs 100 m in 16 seconds. What is her speed in metres per second?", "6.25 m/s",
                   ["84 m/s", "0.16 m/s", "1600 m/s"],
                   "100 ÷ 16 = <b>6.25 m/s</b>. Check: 16 × 6.25 = 100. 0.16 is 16 ÷ 100, the seconds for 1 metre, "
                   "not the metres in 1 second. 84 subtracts.", value=F(25, 4)))
    n, he, his = P.next()
    its.append(mcq("%s cycles 9 km in half an hour. What is %s speed in kilometres per hour?" % (n, his), "18 km/h",
                   ["4.5 km/h", "9.5 km/h", "8.5 km/h"],
                   "Half an hour is 0.5 h. 9 ÷ 0.5 = <b>18 km/h</b>: in a full hour %s goes twice as far. 4.5 multiplies by "
                   "0.5 instead of dividing." % he, value=18))
    its.append(mcq("Mei walks %s km in %s hour. How many kilometres per hour is that?" % (fr(1, 2), fr(1, 6)), "3",
                   [fr(1, 12), fr(1, 3), "6"],
                   "%s ÷ %s = %s × 6 = <b>3</b> km/h. In 6 sixths of an hour (1 hour) Mei walks 6 × %s = 3 km. "
                   "%s multiplies the fractions, and %s divides the wrong way." % (fr(1, 2), fr(1, 6), fr(1, 2), fr(1, 2), fr(1, 12), fr(1, 3)),
                   value=3))
    assert F(1, 2) / F(1, 6) == 3
    its.append(mcq("A recipe uses %s cup of sugar for 2 batches of cookies. How much sugar is that per batch?" % fr(3, 4),
                   fr(3, 8), [fr(3, 2), fr(8, 3), fr(5, 4)],
                   "%s ÷ 2 = <b>%s</b> cup. %s multiplies by 2, %s divides the wrong way, and %s adds %s + %s."
                   % (fr(3, 4), fr(3, 8), fr(3, 2), fr(8, 3), fr(5, 4), fr(3, 4), fr(1, 2)), value=F(3, 8)))
    its.append(mcq("%s is proportional to %s. When %s = 8, %s = 20. What is <i>k</i> in %s = <i>k</i>%s?" % (Y, X, X, Y, Y, X),
                   "2.5", ["0.4", "12", "160"],
                   "<i>k</i> = %s ÷ %s = 20 ÷ 8 = <b>2.5</b>. Check: 2.5 × 8 = 20. 0.4 is 8 ÷ 20, and 12 is the difference "
                   "20 − 8." % (Y, X), value=F(5, 2)))
    its.append(mcq("A 500 g bag of cheese costs $3.25. What is the price per 100 g?", "65¢",
                   ["$6.50", "$16.25", "6.5¢"],
                   "500 g = 5 × 100 g. $3.25 ÷ 5 = <b>65¢</b> per 100 g. $6.50 is the price per kilogram, "
                   "and $16.25 multiplies by 5.", value=F(65, 100)))
    its.append(mcq("A printer prints 48 pages in 3 minutes. How many seconds does it take to print 1 page?", "3.75 s",
                   ["16 s", "45 s", "144 s"],
                   "3 minutes = 180 s. 180 ÷ 48 = <b>3.75 s</b> per page. 16 is the number of pages per minute (the rate the "
                   "other way round), and 45 subtracts.", value=F(15, 4)))
    assert F(180, 48) == F(15, 4)
    its.append(mcq(tbl([2, 3, 5], ["$7", "?", "$17.50"], ("Mass (kg)", "Cost")) + "The cost is proportional to the mass. "
                   "What cost is missing?", "$10.50", ["$8", "$12.25", "$21"],
                   "Unit rate: $7 ÷ 2 = $3.50 per kilogram. 3 kg: 3 × $3.50 = <b>$10.50</b>. $8 adds $1 because the mass "
                   "goes up by 1, and $12.25 is halfway between $7 and $17.50, but 3 is not halfway between 2 and 5.",
                   value=F(21, 2)))
    a, _, ah = P.next()
    its.append(mcq("%s walks 3 km in 45 minutes at a steady pace. What is %s speed in kilometres per hour?" % (a, ah),
                   "4 km/h", ["15 km/h", "135 km/h", "42 km/h"],
                   "45 min = 0.75 h. 3 ÷ 0.75 = <b>4 km/h</b>. Or: 1 km every 15 minutes, so 4 km in 60 minutes. "
                   "15 is the minutes per kilometre, not km per hour.", value=4))
    its.append(mcq("Which unit rate is the greatest?", "84 km in 1.2 h", ["150 km in 2.5 h", "195 km in 3 h", "40 km in 0.8 h"],
                   "Speeds: 84 ÷ 1.2 = 70 km/h, 150 ÷ 2.5 = 60 km/h, 195 ÷ 3 = 65 km/h, 40 ÷ 0.8 = 50 km/h. "
                   "<b>84 km in 1.2 h</b> is the fastest, even though 195 km is the longest distance."))
    assert [F(84) / F(6, 5), F(150) / F(5, 2), F(195, 3), F(40) / F(4, 5)] == [70, 60, 65, 50]
    order = [1, 0, 2, 3, 4, 14, 5, 6, 7, 11, 8, 9, 10, 15, 16, 17, 12, 13, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Unit rates and the constant of proportionality", "items": its}


# ============================================================ set 3: equivalent ratios and proportions
def set_equiv(P):
    its = []
    its.append(mcq("Which ratio is equivalent to 3:4?", R(9, 12), [R(6, 7), R(4, 3), R(9, 4)],
                   "Multiply <b>both</b> terms by 3: 3 × 3 = 9 and 4 × 3 = 12, so <b>9:12</b>. 6:7 adds 3 to both terms, "
                   "and 9:4 multiplies only the first term."))
    its.append(mcq("Which ratio forms a proportion with 2:5?", R(8, 20), [R(5, 8), R(4, 7), R(6, 10)],
                   "2 × 4 = 8 and 5 × 4 = 20, so 2:5 = <b>8:20</b>. 5:8 adds 3 and 4:7 adds 2 to both terms. "
                   "6:10 multiplies the terms by different numbers."))
    its.append(mcq("Is 4:6 = 6:9 a proportion?", "Yes: both are equal to 2:3",
                   ["No: 6 − 4 is not 9 − 6", "No: 4 × 9 is not 6 × 6", "No: you can’t get 6 from 4 by multiplying"],
                   "4:6 = 2:3 (÷ 2) and 6:9 = 2:3 (÷ 3), so <b>yes</b>. Check: 4 × 9 = 36 and 6 × 6 = 36. "
                   "4 × 1.5 = 6, so you can multiply. Differences do not matter in a proportion."))
    its.append(mcq("Is 3:5 = 5:7 a proportion?", "No: 3 × 7 = 21 but 5 × 5 = 25",
                   ["Yes: both terms go up by 2", "Yes: both ratios are less than 1", "No: 7 is not a multiple of 5"],
                   "In a proportion the cross products are equal. 3 × 7 = 21 and 5 × 5 = 25, so <b>no</b>. "
                   "Adding 2 to both terms changes the ratio: 3:5 = 0.6 but 5:7 is about 0.71."))
    its.append(mcq("Which proportion is true?", fr(6, 8) + " = " + fr(9, 12),
                   [fr(6, 8) + " = " + fr(8, 10), fr(2, 3) + " = " + fr(3, 4), fr(4, 5) + " = " + fr(5, 6)],
                   "%s and %s both simplify to %s (cross products: 6 × 12 = 72 and 8 × 9 = 72). "
                   "The others add 1 or 2 to both terms, which never keeps a ratio the same." % (fr(6, 8), fr(9, 12), fr(3, 4))))
    assert F(6, 8) == F(9, 12) and F(6, 8) != F(8, 10)
    its.append(mcq(tbl([4, 6, 10], [6, 9, "?"], ("Blue", "Yellow"), "ratio table") +
                   "Blue and yellow paint are mixed in the same ratio. What number is missing?", "15", ["13", "12", "11"],
                   "4:6 = 2:3, so yellow = blue × 1.5. 10 × 1.5 = <b>15</b>. 13 adds 4 because blue went up by 4, "
                   "and 12 adds 3 like the last step.", value=15))
    assert solve(4, 6, 10, None) == 15
    its.append(mcq("Find the missing term: 5:? = 15:24", "8", ["14", "72", "3"],
                   "15 ÷ 3 = 5, so divide 24 by 3 too: <b>8</b>. 14 subtracts 10 from 24 (adding thinking), "
                   "and 72 multiplies 24 by 3.", value=8))
    its.append(mcq("Find the missing term: 7:? = 21:36", "12", ["22", "108", "50"],
                   "21 ÷ 3 = 7, so 36 ÷ 3 = <b>12</b>. 22 subtracts 14 from 36 because 21 − 14 = 7. "
                   "108 multiplies by 3 instead of dividing.", value=12))
    its.append(mcq("Find the missing term: 1.5:2 = ?:8", "6", ["7.5", "4", "12"],
                   "2 × 4 = 8, so 1.5 × 4 = <b>6</b>. 7.5 adds 6 to 1.5 because 8 − 2 = 6. 12 multiplies 8 × 1.5.",
                   value=6))
    its.append(mcq("Find the missing term: %s:%s = 2:?" % (fr(1, 2), fr(3, 4)), "3", ["4", fr(3, 2), "2.25"],
                   "%s × 4 = 2, so %s × 4 = <b>3</b>. %s multiplies %s by 2 instead of by 4, and 2.25 adds 1.5 like %s + 1.5 = 2."
                   % (fr(1, 2), fr(3, 4), fr(3, 2), fr(3, 4), fr(1, 2)), value=3))
    its.append(mcq("Which ratio is <b>not</b> equivalent to 12:18?", R(6, 12), [R(2, 3), R(4, 6), R(24, 36)],
                   "12:18 = 2:3. 4:6 and 24:36 also simplify to 2:3. <b>6:12</b> subtracts 6 from both terms "
                   "and equals 1:2, so it is not equivalent.", same_ok=True))
    its.append(mcq(tbl([2, 3, 7], [250, 375, "?"], ("Eggs", "Milk (mL)"), "ratio table") +
                   "A pancake recipe keeps eggs and milk in the same ratio. How much milk goes with 7 eggs?",
                   "875 mL", ["379 mL", "500 mL", "1750 mL"],
                   "Unit rate: 250 ÷ 2 = 125 mL per egg. 7 × 125 = <b>875 mL</b>. 379 adds 4 because the eggs went up by 4, "
                   "and 1750 multiplies 250 by 7.", value=875))
    its.append(mcq("Pasta for 4 people uses 300 g. Pasta for 6 people uses 450 g. Is this proportional?",
                   "Yes: 75 g per person both times",
                   ["No: 6 − 4 is not 450 − 300", "No: 450 is not a multiple of 300", "Yes: 50 g per person both times"],
                   "300 ÷ 4 = 75 and 450 ÷ 6 = 75, so the amount per person is the same: <b>yes</b>. "
                   "In a proportion you compare by dividing, not by subtracting."))
    its.append(mcq("Which value of %s makes 4:%s = 10:25 a proportion?" % (X, X), "10", ["19", "62.5", "1.6"],
                   "10:25 = 2:5 = 4:10, so %s = <b>10</b>. Cross products: 4 × 25 = 100 = 10 × 10. "
                   "19 subtracts 6 from 25, and 62.5 and 1.6 pair the wrong terms." % X, value=10))
    assert solve(4, None, 10, 25) == 10
    its.append(mcq("Which ratio is equivalent to 2.5:4?", R(5, 8), ["4.5:6", "4:2.5", "7.5:4"],
                   "Multiply both terms by 2: 2.5 × 2 = 5 and 4 × 2 = 8, so <b>5:8</b>. 4.5:6 adds 2 to both, "
                   "4:2.5 switches the order, and 7.5:4 multiplies only the first term."))
    its.append(mcq("Which fraction forms a proportion with %s?" % fr(6, 15), fr(10, 25), [fr(8, 17), fr(15, 6), fr(12, 15)],
                   "%s = %s and %s = %s, so they are equal: <b>%s</b>. %s adds 2 to both terms, and %s doubles only the "
                   "numerator." % (fr(6, 15), fr(2, 5), fr(10, 25), fr(2, 5), fr(10, 25), fr(8, 17), fr(12, 15)), value=F(2, 5)))
    its.append(mcq("A trail mix uses nuts, raisins and seeds in the ratio 2:3:1. Which ratio is equivalent?", "8:12:4",
                   ["4:5:3", "3:4:2", "6:9:1"],
                   "Multiply <b>all three</b> terms by 4: <b>8:12:4</b>. 4:5:3 adds 2 and 3:4:2 adds 1 to each term. "
                   "6:9:1 forgets to multiply the seeds."))
    its.append(mcq("Mix A is 3 cups of orange juice and 2 cups of water. Mix B is 4.5 cups of orange juice and 3 cups of water. "
                   "Do they taste the same?", "Yes: 4.5:3 = 3:2",
                   ["No: Mix B has more juice", "No: 4.5 − 3 is not 3 − 2", "Yes: both have 1 more cup of juice than water"],
                   "4.5:3 = 9:6 = 3:2, so the mixes are in the same ratio and taste the <b>same</b>. "
                   "Mix B has 1.5 more cups of juice than water, not 1 more, but that does not matter."))
    its.append(mcq("5:6 = 15:18 is a proportion. Which statement about it is true?", "5 × 18 = 6 × 15",
                   ["5 × 15 = 6 × 18", "5 + 18 = 6 + 15", "5 × 6 = 15 × 18"],
                   "In a proportion the cross products are equal: 5 × 18 = 90 and 6 × 15 = 90, so <b>5 × 18 = 6 × 15</b>. "
                   "5 × 15 = 75 and 6 × 18 = 108 are not equal."))
    its.append(mcq("Which pair of ratios forms a proportion?", "1.2:3 and 4:10",
                   ["1.2:3 and 3.2:5", "1.2:3 and 3:1.2", "1.2:3 and 2.4:3"],
                   "1.2 ÷ 3 = 0.4 and 4 ÷ 10 = 0.4, so <b>1.2:3 and 4:10</b> are equal. 3.2:5 adds 2 to both terms, "
                   "3:1.2 switches the order, and 2.4:3 doubles only the first term."))
    assert F(12, 10) / 3 == F(4, 10)
    order = [0, 1, 6, 7, 2, 3, 5, 11, 4, 18, 10, 12, 8, 14, 13, 9, 15, 16, 17, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Equivalent ratios and proportions", "items": its}


# ============================================================ set 4: solving proportions
def set_solve(P):
    its = []

    def eq(a, b, c, d):
        f = lambda v: X if v is None else num(v)
        return "Solve: %s = %s" % (fr(f(a), f(b)), fr(f(c), f(d)))

    def item(a, b, c, d, wrong, e):
        x = solve(a, b, c, d)
        its.append(mcq(eq(a, b, c, d), num(x), [num(w) for w in wrong], e, value=x))

    item(3, 5, None, 20, [18, 4, 60],
         "5 × 4 = 20, so multiply the top by 4 too: 3 × 4 = <b>12</b>. 18 adds 15 to the top because 20 − 5 = 15. "
         "Equivalent fractions come from multiplying, not adding.")
    item(2, 7, None, 28, [23, 4, 56],
         "7 × 4 = 28, so %s = 2 × 4 = <b>8</b>. 23 adds 21 because 28 − 7 = 21. 4 is only the scale factor." % X)
    item(4, 9, 12, None, [17, 3, 108],
         "4 × 3 = 12, so %s = 9 × 3 = <b>27</b>. 17 adds 8 because 12 − 4 = 8. 3 is the scale factor, not %s." % (X, X))
    item(5, 8, 20, None, [23, F(25, 2), 160],
         "5 × 4 = 20, so %s = 8 × 4 = <b>32</b>. 23 adds 15 to 8. 12.5 and 160 multiply the wrong terms. "
         "Cross products check: 5 × 32 = 160 = 8 × 20." % X)
    item(None, 6, 15, 18, [3, 45, 12],
         "%s = %s, so %s = <b>5</b>. Or cross-multiply: 18%s = 6 × 15 = 90, %s = 90 ÷ 18 = 5. "
         "3 subtracts 3 from 6 because 18 − 15 = 3." % (fr(15, 18), fr(5, 6), X, X, X))
    item(7, None, 21, 30, [16, 90, 3],
         "21 ÷ 3 = 7, so %s = 30 ÷ 3 = <b>10</b>. 16 subtracts 14 from 30 because 21 − 14 = 7. "
         "90 multiplies instead of dividing." % X)
    item(None, 15, 2, 3, [14, F(45, 2), 30],
         "3 × 5 = 15, so %s = 2 × 5 = <b>10</b>. 14 subtracts 1 from 15 because 3 − 2 = 1. 22.5 multiplies 15 by %s."
         % (X, fr(3, 2)))
    item(6, None, 15, 25, [16, F(125, 2), F(18, 5)],
         "%s = %s, so 6 = 3 × 2 gives %s = 5 × 2 = <b>10</b>. Cross products: 15%s = 6 × 25 = 150, %s = 10. "
         "16 subtracts 9 from 25 because 15 − 9 = 6." % (fr(15, 25), fr(3, 5), X, X, X))
    item(None, 12, 5, 8, [9, F(96, 5), 7],
         "Cross-multiply: 8%s = 12 × 5 = 60, so %s = 60 ÷ 8 = <b>7.5</b>. 9 subtracts 3 from 12 because 8 − 5 = 3, "
         "and 19.2 is 12 × 8 ÷ 5 (the wrong terms)." % (X, X))
    item(12, None, 16, 20, [16, F(48, 5), 8],
         "%s = %s = %s, so %s = <b>15</b>. Cross products: 16%s = 12 × 20 = 240, %s = 15. "
         "16 adds 4 to 12 because 20 − 16 = 4." % (fr(16, 20), fr(4, 5), fr(12, 15), X, X, X))
    item(3, 4, F(9, 2), None, [F(21, 4), F(27, 8), F(27, 2)],
         "3 × 1.5 = 4.5, so %s = 4 × 1.5 = <b>6</b>. 5.25 adds 1.5 to 4 (adding thinking). "
         "3.375 multiplies 4.5 × 3 ÷ 4, the wrong way round." % X)
    item(F(12, 5), None, 6, 10, [F(32, 5), F(36, 25), F(42, 5)],
         "Cross-multiply: 6%s = 2.4 × 10 = 24, so %s = 24 ÷ 6 = <b>4</b>. 6.4 adds 4 to 2.4 because 10 − 6 = 4, "
         "and 1.44 multiplies 2.4 × 6 ÷ 10." % (X, X))
    item(None, F(5, 2), 8, 5, [F(11, 2), F(8, 5), 16],
         "%s = 2.5 × 8 ÷ 5 = 20 ÷ 5 = <b>4</b>. 5.5 adds 3 to 2.5 because 8 − 5 = 3. "
         "1.6 is only 8 ÷ 5, and 16 divides by 2.5 instead of multiplying." % X)
    item(None, 14, F(7, 2), 7, [F(21, 2), 28, F(7, 4)],
         "14 = 7 × 2, so %s = 3.5 × 2 = <b>7</b>. 10.5 adds 7 to 3.5 because 14 − 7 = 7, "
         "and 28 is 14 × 7 ÷ 3.5." % X)
    item(F(4, 5), 2, None, 15, [F(69, 5), F(75, 2), 12],
         "2 × 7.5 = 15, so %s = 0.8 × 7.5 = <b>6</b>. Or: 0.8 ÷ 2 = 0.4, and 0.4 × 15 = 6. 13.8 adds 13 to 0.8, "
         "and 37.5 is 15 × 2 ÷ 0.8." % X)
    item(None, 4, 9, 6, [7, F(27, 2), F(3, 2)],
         "%s = %s, so %s = 1.5 × 4 = <b>6</b>. 7 adds 3 to 4 because 9 − 6 = 3. 13.5 is 9 × 6 ÷ 4." % (fr(9, 6), fr(3, 2), X))
    item(45, None, 9, 100, [136, F(81, 20), 5],
         "9 × 5 = 45, so %s = 100 × 5 = <b>500</b>. 136 adds 36 to 100 because 45 − 9 = 36. "
         "4.05 multiplies 45 × 9 ÷ 100." % X)
    item(5, None, F(25, 2), 30, [F(45, 2), 75, 6],
         "12.5 ÷ 2.5 = 5, so %s = 30 ÷ 2.5 = <b>12</b>. Cross products: 12.5%s = 5 × 30 = 150, %s = 12. "
         "22.5 subtracts 7.5 from 30, and 75 multiplies instead of dividing." % (X, X, X))
    its.append(mcq("Which step solves %s = %s?" % (fr(X, 8), fr(5, 2)), "%s = 8 × 5 ÷ 2" % X,
                   ["%s = 8 × 2 ÷ 5" % X, "%s = 8 + 5 − 2" % X, "%s = 5 × 2 ÷ 8" % X],
                   "Multiply both sides by 8: %s = 8 × %s = 8 × 5 ÷ 2 = 20. Check: %s = %s. "
                   "8 + 5 − 2 uses adding, which does not keep fractions equal." % (X, fr(5, 2), fr(20, 8), fr(5, 2))))
    assert solve(None, 8, 5, 2) == 20
    its.append(mcq("%s is proportional to %s. %s = 12 when %s = 16. What is %s when %s = 21?" % (Y, X, Y, X, X, Y), "28",
                   ["25", "15.75", "32"],
                   "%s ÷ %s = 16 ÷ 12 = %s. 21 × %s = <b>28</b>. Check: %s = %s. 25 adds 9 to 16 because 21 − 12 = 9, "
                   "and 15.75 uses the ratio upside down." % (X, Y, fr(4, 3), fr(4, 3), fr(12, 16), fr(21, 28)), value=28))
    assert solve(12, 16, 21, None) == 28 and F(21 * 12, 16) == F(63, 4)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 18, 9, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Solving proportions", "items": its}


# ============================================================ set 5: word problems
def set_problems(P):
    its = []
    its.append(mcq("A recipe uses 2 cups of flour for 8 pancakes. How much flour is needed for 20 pancakes?",
                   "5 cups", ["14 cups", "10 cups", "40 cups"],
                   "8 pancakes need 2 cups, so 4 pancakes need 1 cup. 20 ÷ 4 = <b>5 cups</b>. "
                   "14 adds 12 because there are 12 more pancakes.", value=5))
    its.append(mcq("A recipe uses 2 cups of rice and 3 cups of water. Noah cooks 5 cups of rice. How much water does he need?",
                   "7.5 cups", ["6 cups", "10 cups", "15 cups"],
                   "Water = rice × 1.5. 5 × 1.5 = <b>7.5 cups</b>. 6 cups keeps the water 1 cup more than the rice "
                   "(adding), but the ratio must stay 2:3.", value=F(15, 2)))
    its.append(mcq("Muffins for 12 people use 150 mL of maple syrup. How much syrup is needed for 30 people?",
                   "375 mL", ["168 mL", "4500 mL", "300 mL"],
                   "Unit rate: 150 ÷ 12 = 12.5 mL per person. 30 × 12.5 = <b>375 mL</b>. 168 adds 18 because there are "
                   "18 more people, and 300 just doubles.", value=375))
    its.append(mcq("A chili recipe for 6 people uses 450 g of beans. How much is needed for 4 people?",
                   "300 g", ["448 g", "675 g", "225 g"],
                   "450 ÷ 6 = 75 g per person. 4 × 75 = <b>300 g</b>. 448 subtracts 2 because there are 2 fewer people, "
                   "and 675 multiplies by %s instead of %s." % (fr(3, 2), fr(2, 3)), value=300))
    its.append(mcq("A car drives at 80 km/h. How far does it go in 3.5 hours?", "280 km", ["83.5 km", "240 km", "320 km"],
                   "Distance = speed × time: 80 × 3.5 = 240 + 40 = <b>280 km</b>. 240 km forgets the half hour, "
                   "and 83.5 adds 80 + 3.5.", value=280))
    its.append(mcq("A train travels 360 km in 4 hours. At the same speed, how far does it travel in 7 hours?",
                   "630 km", ["363 km", "2520 km", "720 km"],
                   "Unit rate: 360 ÷ 4 = 90 km/h. 7 × 90 = <b>630 km</b>. 363 adds 3 because 7 − 4 = 3, "
                   "and 2520 multiplies 360 × 7.", value=630))
    k, kh, _ = P.next()
    its.append(mcq("%s bikes at 18 km/h. How long does it take %s to bike 27 km?" % (k, "her" if kh == "she" else "him"),
                   "1 h 30 min", ["1 h 50 min", "9 h", "2 h"],
                   "Time = distance ÷ speed: 27 ÷ 18 = 1.5 h = <b>1 h 30 min</b>. 1 h 50 min reads 1.5 h as 1 h 50 min, "
                   "but 0.5 h is half of 60 minutes. 9 subtracts 18 from 27."))
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    its.append(mcq("At the rink, %s skates 1.2 km in 4 minutes. %s skates 2 km in 7 minutes. Who skates faster?" % (a, b),
                   a, [b, "They skate at the same speed", CANT],
                   "%s: 1.2 ÷ 4 = 0.3 km per minute. %s: 2 ÷ 7 is less than 0.3 (0.3 × 7 = 2.1 km). "
                   "So <b>%s</b> is faster, even though %s skates farther." % (a, b, a, b)))
    assert F(12, 10) / 4 > F(2, 7)
    its.append(mcq("Which is the better buy for yogurt?", "1 kg for $5.50",
                   ["650 g for $3.90", "They cost the same per 100 g", CANT],
                   "Price per 100 g: $3.90 ÷ 6.5 = 60¢ and $5.50 ÷ 10 = 55¢. <b>1 kg for $5.50</b> costs less per 100 g."))
    assert F(390, 65) == 6 and F(550, 100) == F(55, 10)
    its.append(mcq("Which is the better buy for granola bars?", "10 bars for $6.50",
                   ["6 bars for $4.20", "They cost the same per bar", CANT],
                   "Price per bar: $4.20 ÷ 6 = 70¢ and $6.50 ÷ 10 = 65¢. <b>10 bars for $6.50</b> is cheaper per bar."))
    its.append(mcq("Eggs come in 12 for $4.80 or 18 for $7.02. Which is the better buy?", "18 for $7.02",
                   ["12 for $4.80", "They cost the same per egg", CANT],
                   "Price per egg: $4.80 ÷ 12 = 40¢ and $7.02 ÷ 18 = 39¢. <b>18 for $7.02</b> costs 1¢ less per egg. "
                   "Paying more in total does not mean a worse buy."))
    assert F(702, 18) == 39
    its.append(mcq("Dog food comes in 3 bag sizes. Which is the best buy?", "5 kg for $21",
                   ["2 kg for $9", "8 kg for $35.20", "They cost the same per kilogram"],
                   "Price per kilogram: $9 ÷ 2 = $4.50, $21 ÷ 5 = $4.20, $35.20 ÷ 8 = $4.40. "
                   "<b>5 kg for $21</b> is the cheapest per kilogram, even though the biggest bag is 8 kg."))
    assert F(3520, 800) == F(44, 10)
    its.append(mcq("On a map of Ontario, 1 cm stands for 5 km. Two towns are 7.5 cm apart on the map. "
                   "How far apart are they really?", "37.5 km", ["12.5 km", "1.5 km", "375 km"],
                   "Each centimetre is 5 km: 7.5 × 5 = <b>37.5 km</b>. 12.5 adds 7.5 + 5, and 1.5 divides by 5.",
                   value=F(75, 2)))
    its.append(mcq("On a trail map, 1 cm stands for 2.5 km. A hike is 20 km long. How long is it on the map?",
                   "8 cm", ["50 cm", "17.5 cm", "22.5 cm"],
                   "Divide by the unit rate: 20 ÷ 2.5 = <b>8 cm</b>. Check: 8 × 2.5 = 20. 50 cm multiplies 20 × 2.5, "
                   "and 17.5 subtracts.", value=8))
    its.append(mcq(fig(scale_bar_svg(2, 15, 3)) + "On this map, a lake is 6 cm long. How long is the real lake?",
                   "45 km", ["19 km", "90 km", "7.5 km"],
                   "The scale bar shows 2 cm for 15 km. 6 cm = 3 × 2 cm, so the lake is 3 × 15 = <b>45 km</b>. "
                   "19 adds 4 because 6 − 2 = 4, and 90 multiplies 6 × 15 as if 1 cm were 15 km.", value=45))
    its.append(mcq("A map has the scale 1:50%s000. Two points are 2 cm apart on the map. How far apart are they really?" % NBSP,
                   "1 km", ["100 km", "10 km", "25 km"],
                   "1 cm on the map is 50%s000 cm in real life. 2 × 50%s000 = 100%s000 cm = 1000 m = <b>1 km</b>. "
                   "100 km treats 100%s000 cm as metres." % (NBSP, NBSP, NBSP, NBSP), value=1))
    assert 2 * 50000 == 100 * 1000
    its.append(mcq("A canoe rental costs $20 plus $10 per hour. Is the cost proportional to the number of hours?",
                   "No: 0 hours still costs $20",
                   ["Yes: the cost goes up by $10 every hour", "Yes: 2 hours cost twice as much as 1 hour",
                    "No: the price per hour changes"],
                   "1 hour costs $30 and 2 hours cost $40, which is not twice $30. Renting for 0 hours would still cost $20. "
                   "So the cost is <b>not proportional</b>, even though it goes up by the same amount each hour."))
    its.append(mcq("It takes about 40 L of maple sap to make 1 L of maple syrup. How much sap is needed for 250 mL of syrup?",
                   "10 L", ["160 L", "10%s000 L" % NBSP, "39.75 L"],
                   "250 mL = 0.25 L. 40 × 0.25 = <b>10 L</b> of sap. 160 L divides 40 by 0.25, "
                   "and 10%s000 L multiplies 40 × 250 without changing mL to litres." % NBSP, value=10))
    n, he, his = P.next()
    its.append(mcq("A hockey player scores 12 goals in the first 20 games. At this rate, how many goals will %s score in 65 games?" % he,
                   "39", ["57", "36", "65"],
                   "Unit rate: 12 ÷ 20 = 0.6 goals per game. 65 × 0.6 = <b>39</b>. 57 adds 45 because there are 45 more games, "
                   "and 36 is the goals for 60 games.", value=39))
    its.append(mcq("A car uses 6.5 L of gas per 100 km. Gas costs $1.60 per litre. What does the gas cost for a 400 km trip?",
                   "$41.60", ["$10.40", "$26", "$64"],
                   "400 km = 4 × 100 km, so 4 × 6.5 = 26 L. 26 × $1.60 = <b>$41.60</b>. $10.40 is the cost of only 100 km, "
                   "and $26 gives the litres as dollars.", value=F(416, 10)))
    assert F(26) * F(16, 10) == F(416, 10)
    order = [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 13, 16, 17, 10, 7, 14, 15, 18, 11, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Word problems: recipes, speed, best buys and maps", "items": its}


# ============================================================ lesson
def body_html():
    f_tab = tov_svg(("Tickets", "Cost ($)"), [1, 2, 3, 4], [12, 24, 36, 48])
    f_gr = graph_svg([(0, 0), (1, 3), (2, 6), (3, 9), (4, 12)], 4, 12, 1, 2,
                     label="graph of a straight line through (0, 0) with y = 3x")
    f_no = graph_svg([(0, 2), (1, 4), (2, 6), (3, 8), (4, 10)], 4, 12, 1, 2,
                     label="graph of a straight line that starts at (0, 2)")
    f_rt = tov_svg(("Flour (cups)", "Pancakes"), [2, 1, 5], [8, 4, 20], "ratio table")
    f_sc = scale_bar_svg(2, 15, 3)
    return (
        "<h2>What “proportional” means</h2>"
        "<p>Two quantities are <b>proportional</b> when one is always the same number times the other: "
        "%s = <i>k</i>%s. The number <i>k</i> is the <b>constant of proportionality</b>. It is also the <b>unit rate</b>, "
        "the amount for 1.</p>"
        "<p>Test a table: divide %s by %s in every column. If you always get the same number, it is proportional.</p>"
        "<figure class='sn-fig'>%s<figcaption>12 ÷ 1 = 24 ÷ 2 = 36 ÷ 3 = 48 ÷ 4 = 12. Cost = 12 × tickets, "
        "so the cost is proportional. The unit rate is $12 per ticket.</figcaption></figure>"
        "<h2>Proportional graphs</h2>"
        "<p>A proportional graph is a <b>straight line through (0, 0)</b>. Both parts matter.</p>"
        "<figure class='sn-fig'>%s<figcaption>Proportional: %s = 3%s. The line starts at (0, 0).</figcaption></figure>"
        "<figure class='sn-fig'>%s<figcaption>Not proportional: the line is straight, but it starts at (0, 2). "
        "4 ÷ 1 = 4 but 6 ÷ 2 = 3.</figcaption></figure>"
        "<h2>Solving a proportion</h2>"
        "<p>A <b>proportion</b> says two ratios are equal, like %s = %s. Three ways to find %s:</p>"
        "<ul><li><b>Scale factor:</b> 5 × 4 = 20, so 3 × 4 = 12.</li>"
        "<li><b>Unit rate:</b> 3 ÷ 5 = 0.6, and 0.6 × 20 = 12.</li>"
        "<li><b>Cross products:</b> 5%s = 3 × 20 = 60, so %s = 12.</li></ul>"
        "%s"
        "<figure class='sn-fig'>%s<figcaption>Ratio table: halve to get the unit rate (1 cup for 4 pancakes), "
        "then multiply by 5.</figcaption></figure>"
        "%s%s"
        "<figure class='sn-fig'>%s<figcaption>2 cm on the map stands for 15 km, so 6 cm stands for 3 × 15 = 45 km.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        "%s"
    ) % (Y, X, Y, X, f_tab, f_gr, Y, X, f_no, fr(3, 5), fr(X, 20), X, X, X,
         ex("Example 1", "Solve %s = %s." % (fr(3, 5), fr(X, 20)), "5 × 4 = 20, so multiply the top by 4 as well: 3 × 4.", "%s = 12" % X),
         f_rt,
         ex("Example 2: best buy", "Yogurt: 650 g for $3.90 or 1 kg for $5.50?",
            "Price per 100 g: $3.90 ÷ 6.5 = 60¢ and $5.50 ÷ 10 = 55¢.", "1 kg for $5.50"),
         ex("Example 3: speed", "A car drives 150 km in 2 h. How far does it go in 5 h?",
            "Unit rate: 150 ÷ 2 = 75 km/h. 5 × 75 = 375.", "375 km"),
         f_sc,
         table(["Mistake", "What to do instead"], [
             ["%s = %s gives %s = 18 (add 15 because 20 − 5 = 15)" % (fr(3, 5), fr(X, 20), X),
              "Multiply: 5 × 4 = 20, so 3 × 4 = 12"],
             ["“%s goes up by 2 each time, so it is proportional”" % Y, "Check that %s ÷ %s is always the same and that (0, 0) fits" % (Y, X)],
             ["A straight line that starts at (0, 2) is proportional", "It must also go through (0, 0)"],
             ["150 km in 2 h = 300 km/h", "Unit rate: divide. 150 ÷ 2 = 75 km/h"],
             ["The bigger package costs more, so it is the worse buy", "Compare the price for 1 unit (per kg, per 100 g, per bar)"],
         ]))


FAQ = [
    {"q": "What is proportional reasoning in Grade 7 math in Ontario?",
     "a": "In the Ontario Grade 7 math curriculum, students tell proportional situations from non-proportional ones and use ratios, unit rates and proportions to solve problems such as recipes, speed, best buys and map scales."},
    {"q": "How do you tell if a relationship is proportional?",
     "a": "In a table, y ÷ x is the same in every column. On a graph, the points lie on a straight line through (0, 0). As an equation, it has the form y = kx."},
    {"q": "How do you solve a proportion like 3/5 = x/20?",
     "a": "Find the scale factor: 5 × 4 = 20, so x = 3 × 4 = 12. You can also cross-multiply: 5x = 3 × 20 = 60, so x = 12."},
    {"q": "What is the most common mistake with proportions?",
     "a": "Adding instead of multiplying. For 3/5 = x/20, many students add 15 to get 18, but equal ratios come from multiplying both terms by the same number."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables of values, four-panel pictures, scale bars)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(47810)
    P = People(rnd)
    sets = [set_decide(P), set_rates(P), set_equiv(P), set_solve(P), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "proportional-reasoning", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Proportional Reasoning: Unit Rates, Proportions and Proportional Graphs",
        "seo_title": "Grade 7 Proportional Reasoning Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Proportional reasoning",
        "domain": "Number",
        "standard_code": "Grade 7: B2.10",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify proportional and non-proportional situations and apply proportional reasoning to solve problems",
        "meta_desc": "Free Grade 7 proportional reasoning worksheets for the Ontario curriculum: tell proportional from non-proportional tables and graphs, find unit rates, solve proportions like 3/5 = x/20, and solve recipe, speed, best-buy and map-scale problems. 100 math questions with an answer key.",
        "key_big": "Proportional means y = kx: y ÷ x is always the same, and the graph is a straight line through (0, 0).",
        "key_sub": "Equal ratios come from multiplying, not adding: 3/5 = x/20 gives x = 3 × 4 = 12, not 3 + 15 = 18.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(table of values|ratio table|four |map scale bar)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
