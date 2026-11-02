# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Number patterns (Australian Curriculum v9.0, AC9M2A01)
  python3 tools/gen_au_maths_y2_patterns.py
Count on and back by 2s, 3s, 5s, 10s and 100s (number tracks and number lines), patterns on a
hundreds chart, find the rule (+5, −10) and the missing numbers, growing and shrinking shape
patterns (tiles, matchsticks, dots, cubes), and word problems in Australian settings.
Wrong answers come from real mistakes: counting on 1 instead of the step, counting back when the
pattern goes up, skipping a number (one step too many), using the first number as the rule
(3, 8, 13 -> +3), moving across a row instead of down a column on the hundreds chart, and giving
the step number instead of the amount.
Every answer is computed and checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
MINUS = "−"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def nums_mcq(q, ans, cands, e, fmt=str):
    """Number answer: drop distractors that equal the answer or are not 0..999."""
    ok = [v for v in cands if v != ans and 0 <= v <= 999]
    assert 0 <= ans <= 999
    return mcq(q, fmt(ans), [fmt(v) for v in ok], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
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
        return dict(n=p[0], he=p[1], He=p[1].capitalize(), his=p[2])


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def seq(start, step, n):
    return [start + step * k for k in range(n)]


def rule(d):
    return ("+%d" % d) if d > 0 else (MINUS + "%d" % -d)


def is_pattern(xs):
    d = xs[1] - xs[0]
    return d != 0 and all(xs[i + 1] - xs[i] == d for i in range(len(xs) - 1))


# ------------------------------------------------------------ number track and number line
TW, TH = 52, 36


def track_svg(nums):
    """Number track: a row of boxes. None shows a red ? in a shaded box."""
    m = 4
    W, H = 2 * m + len(nums) * TW, 2 * m + TH
    s = []
    for i, v in enumerate(nums):
        x = m + i * TW
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, TW, TH, FILL if v is None else "#ffffff", GREEN))
        s.append(text(x + TW / 2, m + 24, "?" if v is None else str(v), 17, col=RED if v is None else INK))
    return svg_wrap(W, H, "".join(s), "number track")


def track(nums, i):
    """Pattern with the number at position i hidden."""
    return fig(track_svg([None if k == i else v for k, v in enumerate(nums)]))


def jw(j):
    return 80 if abs(j) >= 100 else (74 if abs(j) >= 10 else 58)


def nline_svg(start, jumps, ticks=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    jl = [rule(j) for j in jumps]
    m, ry, ly = 30, 22, 48
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 6, jl[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line starting at %d with jumps of %s" % (
        start, ", ".join(jl).replace(MINUS, "minus ")))


# ------------------------------------------------------------ hundreds chart
RW, RH = 34, 28


def chart_rows_svg(first, nrows, shaded):
    """Full rows of a hundreds chart starting at `first` (1, 101, 341 ...). Shaded cells are green."""
    assert (first - 1) % 10 == 0
    m = 4
    W, H = 2 * m + 10 * RW, 2 * m + nrows * RH
    s = []
    for r in range(nrows):
        for c in range(10):
            v = first + 10 * r + c
            x, y = m + c * RW, m + r * RH
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                     % (x, y, RW, RH, CUBE if v in shaded else "#ffffff", GREEN))
            s.append(text(x + RW / 2, y + 19, str(v), 14))
    return svg_wrap(W, H, "".join(s), "hundreds chart rows")


CW, CH = 50, 34


def piece_svg(tl, nrows, ncols, target, hide=()):
    """A piece of a hundreds chart. tl = top-left number. target (r, c) shows a red ?, hide = blank cells."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    m = 4
    W, H = 2 * m + ncols * CW, 2 * m + nrows * CH
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CW, m + r * CH
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CW, CH, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CW / 2, y + 23, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CW / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "hundreds chart piece")


# ------------------------------------------------------------ growing shape patterns
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
    """Tiles: a column of k and a row of k (sharing the corner) = 2k - 1."""
    def draw(x, y):
        s = [tile(x, y + i * T) for i in range(k)]
        s += [tile(x + i * T, y + (k - 1) * T) for i in range(1, k)]
        return "".join(s)
    return k * T, k * T, draw


TS = 26
TRH = 22.5


def triangles(k):
    """k matchstick triangles in a row (up, down, up ...) = 2k + 1 sticks."""
    def draw(x, y):
        pts = [(x + i * TS / 2, y + (TRH if i % 2 == 0 else 0)) for i in range(k + 2)]
        s = [stick(*pts[i], *pts[i + 1]) for i in range(k + 1)]
        for j in range(k):
            a, b = pts[j], pts[j + 2]
            s.append(stick(*a, *b))
        return "".join(s)
    return (k + 1) * TS / 2, TRH, draw


SQ = 24


def squares(k):
    """k matchstick squares in a row = 3k + 1 sticks."""
    def draw(x, y):
        s = [stick(x + i * SQ, y, x + i * SQ, y + SQ) for i in range(k + 1)]
        for i in range(k):
            s.append(stick(x + i * SQ, y, x + (i + 1) * SQ, y))
            s.append(stick(x + i * SQ, y + SQ, x + (i + 1) * SQ, y + SQ))
        return "".join(s)
    return k * SQ, SQ, draw


def dot_rows(k):
    """k rows of 5 dots = 5k."""
    def draw(x, y):
        return "".join("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x + 7 + c * 14, y + 7 + r * 14, GREEN)
                       for r in range(k) for c in range(5))
    return 5 * 14, k * 14, draw


def two_rows(k):
    """2 rows of (7 - k) tiles = 14 - 2k: 12, 10, 8 ..."""
    n = 7 - k

    def draw(x, y):
        return "".join(tile(x + i * T, y + r * T) for r in range(2) for i in range(n))
    return n * T, 2 * T, draw


def towers3(k):
    """(k + 1) towers of 3 cubes = 3k + 3."""
    def draw(x, y):
        return "".join(tile(x + i * (T + 5), y + j * T) for i in range(k + 1) for j in range(3))
    return (k + 1) * T + k * 5, 3 * T, draw


def tables(k):
    """k square tables in a row: 1 chair on each long side per table + 1 at each end = 2k + 2."""
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
    # name: (drawer, count(k), thing)
    "L": (L_shape, lambda k: 2 * k - 1, "tiles"),
    "tri": (triangles, lambda k: 2 * k + 1, "sticks"),
    "sq": (squares, lambda k: 3 * k + 1, "sticks"),
    "dots": (dot_rows, lambda k: 5 * k, "dots"),
    "dec": (two_rows, lambda k: 14 - 2 * k, "tiles"),
    "towers": (towers3, lambda k: 3 * k + 3, "cubes"),
    "tables": (tables, lambda k: 2 * k + 2, "chairs"),
}


def pattern_svg(name, steps=(1, 2, 3)):
    """The given steps side by side, bottoms lined up, with 'Step k' under each."""
    drawer = PATTERNS[name][0]
    parts = [drawer(k) for k in steps]
    m, gap, lab = 8, 30, 24
    widths = [max(w, 46) for w, _, _ in parts]
    hmax = max(h for _, h, _ in parts)
    W = 2 * m + sum(widths) + gap * (len(parts) - 1)
    H = m + hmax + 8 + lab
    s, x = [], m
    for k, (w, h, draw), cw in zip(steps, parts, widths):
        s.append(draw(x + (cw - w) / 2, m + hmax - h))
        s.append(text(x + cw / 2, m + hmax + 8 + 16, "Step %d" % k, 14))
        x += cw + gap
    return svg_wrap(int(round(W)), int(round(H)), "".join(s), "shape pattern %s" % name)


def coins_svg(n, kind):
    """Australian coins: $2 (gold, small) or 5c (silver)."""
    if kind == "$2":
        r, fill, edge, lab = 19, "#e8c25a", "#9a7a1c", "$2"
    else:
        r, fill, edge, lab = 18, "#dfe3e7", "#7a828a", "5c"
    per = 5
    rows = (n + per - 1) // per
    d, g, m = 2 * r, 8, 4
    W = 2 * m + min(n, per) * d + (min(n, per) - 1) * g
    H = 2 * m + rows * d + (rows - 1) * g
    s = []
    for i in range(n):
        cx = m + r + (i % per) * (d + g)
        cy = m + r + (i // per) * (d + g)
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge))
        s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 4, edge))
        s.append(text(cx, cy + 5, lab, 14))
    return svg_wrap(W, H, "".join(s), "%d coins" % n)


# ============================================================ set 1: count on and back
def set_counting():
    its = []

    def nxt(nums, cands, extra=""):
        d = nums[1] - nums[0]
        assert is_pattern(nums)
        a = nums[-1] + d
        word = "Count on in %ds." % d if d > 0 else "Count back in %ds." % -d
        e = "Each number is %d %s. %d %s %d = <b>%d</b>.%s" % (
            abs(d), "more" if d > 0 else "less", nums[-1], "+" if d > 0 else MINUS, abs(d), a, extra)
        return nums_mcq(fig(track_svg(nums + [None])) + word + " What number goes in the box with the ?",
                        a, cands, e)

    on2 = nxt([46, 48, 50, 52], [53, 56, 50], " 53 is only 1 more.")
    on5 = nxt([65, 70, 75], [76, 85, 70], " 76 is counting on 1, not 5.")
    on10 = nxt([27, 37, 47], [48, 67, 58], " The ones digit stays 7. Only the tens digit goes up.")
    on3 = nxt([12, 15, 18], [19, 24, 20], " 19 is only 1 more.")
    on100 = nxt([200, 300, 400], [401, 410, 600], " Only the hundreds digit goes up.")
    bk2 = nxt([60, 58, 56], [55, 58, 52], " 58 goes the wrong way.")
    bk10 = nxt([83, 73, 63], [62, 52, 73], " The ones digit stays 3.")
    bk5 = nxt([110, 105, 100], [99, 105, 90], " 99 is only 1 less.")
    bk3 = nxt([30, 27, 24], [23, 22, 27], " 23 is only 1 less.")
    bk100 = nxt([900, 800, 700], [690, 500, 800], " Only the hundreds digit goes down.")
    on2h = nxt([194, 196, 198], [199, 202, 196], " 199 is only 1 more.")
    on3b = nxt([41, 44, 47], [48, 53, 44], " 48 is only 1 more. 53 skips a number.")
    on5h = nxt([385, 390, 395], [396, 405, 390], " 396 is only 1 more.")
    on10h = nxt([470, 480, 490], [491, 510, 480], " 49 tens + 1 ten = 50 tens = 500.")
    on100b = nxt([135, 235, 335], [336, 345, 535], " Only the hundreds digit changes. The 3 and 5 stay.")
    bk10h = nxt([520, 510, 500], [499, 400, 510], " 499 is only 1 less.")
    bk100b = nxt([760, 660, 560], [550, 360, 660], " The tens and ones stay 60.")

    def line(start, d, n, cands):
        a = start + d * n
        pts = seq(start + d, d, n)
        q = fig(nline_svg(start, [d] * n)) + "Start at %d. Make the jumps. Where do you land?" % start
        return nums_mcq(q, a, cands, "Each jump is %s. Count %s in %ds from %d: %s. You land on <b>%d</b>." % (
            rule(d), "on" if d > 0 else "back", abs(d), start, lst(pts), a))

    l3 = line(0, 3, 5, [5, 12, 18])
    l5 = line(34, 5, 4, [38, 49, 59])
    l100 = line(250, 100, 3, [253, 450, 650])
    l10 = line(400, -10, 3, [397, 380, 360])
    out = [on2, on5, on10, bk2, on3, l3, bk10, on100, bk5, bk3,
           l5, bk100, on2h, on3b, l100, on5h, on10h, bk10h, l10, on100b]
    assert len({id(x) for x in out}) == 20
    return {"title": "Count on and back by 2s, 3s, 5s, 10s and 100s", "items": out}


# ============================================================ set 2: patterns on a hundreds chart
def set_chart():
    its = []

    def shade(first, nrows, start, d, n, cands, how):
        sh = seq(start, d, n)
        a = sh[-1] + d
        assert a < first + 10 * nrows
        q = (fig(chart_rows_svg(first, nrows, set(sh))) +
             "The shaded squares count on in %ds. Keep the pattern. What is the next shaded number?" % d)
        return nums_mcq(q, a, cands, "%d + %d = <b>%d</b>. %s" % (sh[-1], d, a, how))

    s2 = shade(1, 2, 2, 2, 6, [13, 22, 16], "Shade every second square.")
    s5 = shade(1, 3, 5, 5, 4, [21, 30, 26], "In 5s, the shaded squares end in 5 or 0.")
    s10 = shade(1, 5, 3, 10, 3, [24, 34, 43], "In 10s, go straight down one row. The ones digit stays 3.")
    s3 = shade(1, 2, 3, 3, 4, [13, 14, 18], "Count 3 squares on from 12: 13, 14, 15.")
    s5b = shade(101, 3, 105, 5, 4, [121, 130, 126], "In 5s, the shaded squares end in 5 or 0.")
    s10b = shade(341, 4, 346, 10, 2, [357, 376, 347], "In 10s, go straight down one row. The ones digit stays 6.")

    def piece(tl, rows, cols, tgt, hide, cands):
        r, c = tgt
        a = tl + 10 * r + c
        vis = lambda rr, cc: 0 <= rr < rows and 0 <= cc < cols and (rr, cc) not in hide and (rr, cc) != tgt
        if vis(r - 1, c):
            ref = a - 10
            e = "The number above is 10 less. So the ? is 10 more than %d. %d + 10 = <b>%d</b>." % (ref, ref, a)
        elif vis(r + 1, c):
            ref = a + 10
            e = "The number below is 10 more. So the ? is 10 less than %d. %d − 10 = <b>%d</b>." % (ref, ref, a)
        elif vis(r - 2, c):
            ref = a - 20
            e = "The ? is 2 rows below %d. Count on 10 twice: %d, <b>%d</b>." % (ref, ref + 10, a)
        else:
            assert vis(r + 2, c)
            ref = a + 20
            e = "The ? is 2 rows above %d. Count back 10 twice: %d, <b>%d</b>." % (ref, ref - 10, a)
        q = fig(piece_svg(tl, rows, cols, tgt, hide)) + "This is part of a hundreds chart. What number goes in the box with the ?"
        return nums_mcq(q, a, cands, e)

    p1 = piece(23, 3, 3, (2, 1), set(), [35, 45, 54])
    p2 = piece(156, 3, 4, (0, 2), {(2, 0)}, [167, 157, 148])
    p3 = piece(261, 3, 4, (0, 3), {(1, 0)}, [273, 265, 284])
    p4 = piece(35, 3, 3, (2, 0), {(1, 0)}, [45, 65, 56])
    p5 = piece(482, 3, 3, (2, 1), {(0, 0)}, [494, 502, 593])
    p6 = piece(708, 3, 3, (1, 2), {(0, 2)}, [721, 719, 710])
    p7 = piece(612, 3, 3, (0, 2), {(1, 2)}, [624, 604, 615])
    p8 = piece(87, 2, 3, (1, 1), set(), [89, 99, 78])
    ideas = [
        mcq("You count on in 10s from 7 on a hundreds chart. How do you move?", "down 1 row each time",
            ["right 1 square each time", "up 1 row each time", "right 2 squares each time"],
            "10 more is the square just below. 7, 17, 27, 37 go <b>down 1 row each time</b>."),
        mcq("You count back in 10s on a hundreds chart. How do you move?", "up 1 row each time",
            ["down 1 row each time", "left 1 square each time", "right 1 square each time"],
            "10 less is the square just above. 57, 47, 37 go <b>up 1 row each time</b>."),
        mcq("You count in 5s on a hundreds chart. Which columns get shaded?", "the columns of numbers ending in 5 and 0",
            ["only the column of numbers ending in 5", "every column",
             "the columns of numbers ending in 2 and 4"],
            "5, 10, 15, 20, 25 … end in 5 or 0. So <b>the columns of numbers ending in 5 and 0</b> are shaded."),
        nums_mcq("You count on in 2s from 2 on a hundreds chart. Which number is NOT shaded?", 35, [36, 48, 50],
                 "Counting in 2s from 2 gives even numbers: 2, 4, 6, 8 … 36, 48 and 50 are even. "
                 "<b>35</b> is odd, so it is not shaded."),
        nums_mcq("Start at 64 on a hundreds chart. Move down 3 rows. Where do you land?", 94, [67, 84, 74],
                 "Each row down is 10 more: 74, 84, <b>94</b>. 67 moves right, not down."),
        nums_mcq("Start at 158 on a hundreds chart. Move up 2 rows. Where do you land?", 138, [156, 148, 178],
                 "Each row up is 10 less: 148, <b>138</b>. 178 goes down, not up."),
    ]
    out = [s2, p1, ideas[0], s5, p8, s3, ideas[1], p2, s10, ideas[3],
           p4, s5b, ideas[2], p3, ideas[4], s10b, p6, ideas[5], p7, p5]
    assert len({id(x) for x in out}) == 20
    return {"title": "Patterns on a hundreds chart", "items": out}


# ============================================================ set 3: find the rule and the missing number
def set_rule_missing():
    def rq(nums, cands, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        q = fig(track_svg(nums)) + "What is the rule for this pattern?"
        e = "%d %s %d = %d, and each number is %d %s. The rule is <b>%s</b>.%s" % (
            nums[0], "+" if d > 0 else MINUS, abs(d), nums[1], abs(d), "more" if d > 0 else "less", rule(d), extra)
        return mcq(q, rule(d), [rule(c) for c in cands], e)

    r1 = rq([35, 40, 45, 50], [10, -5, 1], " The numbers go up, so it is not " + MINUS + "5.")
    r2 = rq([90, 80, 70, 60], [10, -1, -20], " The numbers go down, so the rule takes away.")
    r3 = rq([3, 8, 13, 18], [3, -5, 10], " 3 is the first number, not the rule. Look at the jump between numbers.")
    r4 = rq([4, 7, 10, 13], [4, 6, -3], " 4 is the first number, not the rule.")
    r5 = rq([150, 250, 350, 450], [10, -100, 200], " Only the hundreds digit goes up.")
    r6 = rq([64, 62, 60, 58], [2, -4, -1], " The numbers go down, so it is not +2.")
    r7 = rq([2, 12, 22, 32], [2, 20, -10], " 2 is the first number, not the rule.")
    r8 = rq([500, 495, 490, 485], [5, -10, -1])
    r10 = rq([800, 700, 600, 500], [100, -10, -200])

    def miss(nums, i, cands):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = nums[i]
        if i == 0:
            e = "The rule is %s. Go back one step from %d: %d %s %d = <b>%d</b>." % (
                rule(d), nums[1], nums[1], MINUS if d > 0 else "+", abs(d), a)
        else:
            e = "The rule is %s. %d %s %d = <b>%d</b>." % (rule(d), nums[i - 1], "+" if d > 0 else MINUS, abs(d), a)
            if i < len(nums) - 1:
                e += " Check: %d %s %d = %d." % (a, "+" if d > 0 else MINUS, abs(d), nums[i + 1])
        return nums_mcq(track(nums, i) + "What number is missing?", a, cands, e)

    m1 = miss([20, 25, 30, 35], 2, [26, 40, 34])
    m2 = miss([12, 14, 16, 18], 0, [13, 10, 20])
    m3 = miss([50, 40, 30, 20], 2, [39, 35, 10])
    m4 = miss([9, 12, 15, 18], 2, [13, 14, 16])
    m5 = miss([275, 280, 285, 290], 2, [281, 295, 286])
    m6 = miss([430, 530, 630, 730], 1, [440, 431, 830])
    m7 = miss([96, 98, 100, 102], 2, [99, 101, 104])
    m8 = miss([355, 345, 335, 325], 2, [344, 365, 330])
    m9 = miss([41, 44, 47, 50, 53], 3, [48, 49, 51])
    m10 = miss([990, 980, 970, 960], 2, [979, 870, 950])
    m11 = miss([700, 600, 500, 400], 0, [690, 600, 800])
    out = [r1, m1, r2, m2, r6, m4, r3, m3, r7, m7,
           r4, m5, r5, m6, r8, m8, m9, r10, m11, m10]
    assert len({id(x) for x in out}) == 20
    return {"title": "Find the rule and the missing number", "items": out}


# ============================================================ set 4: growing shape patterns
def set_shapes():
    def cnt(name, k):
        return PATTERNS[name][1](k)

    def d_of(name):
        return cnt(name, 2) - cnt(name, 1)

    def next_q(name, cands):
        thing = PATTERNS[name][2]
        a, last, d = cnt(name, 4), cnt(name, 3), d_of(name)
        e = "Count each step: %s. Each step has %d %s %s. %d %s %d = <b>%d</b> %s in Step 4." % (
            lst([cnt(name, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", thing,
            last, "+" if d > 0 else MINUS, abs(d), a, thing)
        return nums_mcq(fig(pattern_svg(name)) + "The pattern keeps going. How many %s are in Step 4?" % thing,
                        a, cands, e)

    def six_q(name, cands):
        thing = PATTERNS[name][2]
        vals = [cnt(name, k) for k in range(1, 7)]
        e = "Keep counting on %s: %s. Step 6 has <b>%d</b> %s." % (rule(d_of(name)), lst(vals), vals[-1], thing)
        return nums_mcq(fig(pattern_svg(name)) + "The pattern keeps going. How many %s are in Step 6?" % thing,
                        vals[-1], cands, e)

    def rule_q(name, cands, extra=""):
        thing = PATTERNS[name][2]
        d = d_of(name)
        e = "Count each step: %s. Each step has %d %s %s. The rule is <b>%s each step</b>.%s" % (
            lst([cnt(name, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", thing, rule(d), extra)
        return mcq(fig(pattern_svg(name)) + "What is the rule for the number of %s?" % thing,
                   rule(d) + " each step", [rule(c) + " each step" for c in cands], e)

    def which_q(name, n, cands):
        thing = PATTERNS[name][2]
        vals = [cnt(name, k) for k in range(1, 9)]
        k = vals.index(n) + 1
        e = "Keep counting on %s: %s. %d is the number for <b>Step %d</b>." % (
            rule(d_of(name)), lst(vals[:k]), n, k)
        return mcq(fig(pattern_svg(name)) + "The pattern keeps going. Which step has %d %s?" % (n, thing),
                   "Step %d" % k, ["Step %d" % c for c in cands], e)

    def first_q(name, cands):
        thing = PATTERNS[name][2]
        d = d_of(name)
        a = cnt(name, 1)
        e = "Each step has %d more %s. Count back one step from Step 2: %d − %d = <b>%d</b>." % (
            d, thing, cnt(name, 2), d, a)
        return nums_mcq(fig(pattern_svg(name, (2, 3, 4))) + "How many %s are in Step 1?" % thing, a, cands, e)

    def list_q(name, cands, extra):
        vals = [cnt(name, k) for k in (1, 2, 3, 4)]
        thing = PATTERNS[name][2]
        e = "Count the %s in each step: %s, and the next step has %d. The numbers are <b>%s</b>.%s" % (
            thing, lst(vals[:3]), vals[3], lst(vals), extra)
        return mcq(fig(pattern_svg(name)) + "Which number pattern matches the %s?" % thing, lst(vals), cands, e)

    out = [
        next_q("L", [6, 9, 3]),                                   # 1, 3, 5 -> 7
        next_q("dots", [16, 25, 10]),                             # 5, 10, 15 -> 20
        rule_q("L", [1, 3, -2], " Each new step adds 1 tile on top and 1 tile on the right."),
        next_q("tri", [8, 11, 5]),                                # 3, 5, 7 -> 9
        next_q("towers", [13, 18, 9]),                            # 6, 9, 12 -> 15
        rule_q("dots", [1, 10, -5], " Each step adds 1 row of 5 dots. That is 5 more dots, not 1."),
        next_q("dec", [10, 7, 4]),                                # 12, 10, 8 -> 6
        next_q("sq", [11, 16, 7]),                                # 4, 7, 10 -> 13
        list_q("tri", ["1, 2, 3, 4", "3, 6, 9, 12", "3, 4, 5, 6"], " Count the sticks, not the triangles."),
        rule_q("sq", [4, 1, -3], " 4 is the number in Step 1, not the rule. Each new square needs 3 more sticks."),
        rule_q("dec", [2, -1, -3], " The pattern gets smaller, so it is not +2. Each row loses 1 tile, so 2 tiles go."),
        first_q("towers", [9, 3, 7]),                             # steps 2-4: 9, 12, 15 -> 6
        six_q("L", [9, 13, 6, 12]),                               # 11
        list_q("dec", ["6, 5, 4, 3", "12, 14, 16, 18", "12, 11, 10, 9"], " The pattern gets smaller by 2 each step."),
        six_q("tri", [11, 15, 6, 12]),                            # 13
        first_q("sq", [7, 3, 1]),                                 # steps 2-4: 7, 10, 13 -> 4
        which_q("dots", 30, [5, 7, 10]),                          # Step 6
        six_q("towers", [18, 24, 6]),                             # 21
        which_q("tri", 13, [5, 7, 4]),                            # Step 6
        six_q("sq", [16, 22, 6, 18]),                             # 19
    ]
    assert len({id(x) for x in out}) == 20
    return {"title": "Growing shape patterns", "items": out}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def story(t, ans, cands, e, pic="", unit=None):
        d = P.next()
        fmt = unit or str
        its.append(nums_mcq(pic + t.format(**d), ans, cands, e.format(**d), fmt))

    cm = lambda v: "%d cm" % v
    L = lambda v: "%d L" % v
    dol = lambda v: "$%d" % v
    cents = lambda v: "%dc" % v

    story("Tables are pushed together for a class party. Look at the pattern. How many chairs fit around 5 tables?",
          12, [10, 14, 20],
          "1 table has 4 chairs, 2 tables have 6, 3 tables have 8. Each table adds 2 chairs: 8, 10, <b>12</b>. "
          "20 would be 4 chairs for every table, but there are no chairs where the tables join.",
          fig(pattern_svg("tables")))                                                             # 0
    story("{n} counts {his} $2 coins: $2, $4, $6 … How much money is there?", 16, [8, 14, 18],
          "Count on in 2s, one coin at a time: 2, 4, 6, 8, 10, 12, 14, 16. That is <b>$16</b>. "
          "8 is the number of coins.", fig(coins_svg(8, "$2")), dol)                                 # 1
    story("{n} counts {his} 5c coins in 5s. How much money is there?", 45, [9, 40, 50],
          "Count on in 5s: 5, 10, 15, 20, 25, 30, 35, 40, 45. That is <b>45c</b>.", fig(coins_svg(9, "5c")), cents)  # 2
    story("{n} reads 10 pages each night. After 1 night {he} has read 10 pages, after 2 nights 20 pages. "
          "How many pages after 7 nights?", 70, [17, 60, 80],
          "Count on in 10s 7 times: 10, 20, 30, 40, 50, 60, <b>70</b> pages.")                     # 3
    story("{n} has 600 points in a game. {He} loses 100 points each round. How many points are left after 3 rounds?",
          300, [597, 400, 900],
          "Count back in 100s 3 times: 500, 400, <b>300</b>. 900 counts on, but {he} loses points.")  # 4
    story("At the swimming carnival, each row has 5 seats. How many seats are in 8 rows?", 40, [13, 35, 45],
          "Count on in 5s 8 times: 5, 10, 15, 20, 25, 30, 35, <b>40</b> seats.")                     # 5
    story("{n}’s cricket team has 24 runs. They score 3 runs every over. How many runs after 4 more overs?",
          36, [28, 33, 39],
          "Count on in 3s 4 times: 27, 30, 33, <b>36</b> runs. Do not count 24, because that is the start.")  # 6
    story("{n}’s sunflower is 5 cm, then 8 cm, then 11 cm tall. It grows the same each week. How tall is it the next week?",
          14, [12, 17, 8],
          "5 + 3 = 8 and 8 + 3 = 11, so it grows 3 cm each week. 11 + 3 = <b>14 cm</b>.", unit=cm)  # 7
    story("The houses on one side of {n}’s street are numbered 2, 4, 6, 8 … What is the number of the 10th house?",
          20, [10, 18, 22],
          "Count on in 2s 10 times: 2, 4, 6, 8, 10, 12, 14, 16, 18, <b>20</b>. 10 is how many houses.")  # 8
    story("{n} plays hide-and-seek. {He} counts back in 5s from 50: 50, 45, 40 … What does {he} say after 20?",
          15, [19, 25, 10],
          "Counting back, each number is 5 less. 20 − 5 = <b>15</b>. 19 is only 1 less.",
          fig(track_svg([35, 30, 25, 20, None])))            # 9
    story("A school collects cans for a food drive. The total is 200 after week 1, 300 after week 2 and 400 after week 3. "
          "It keeps going. What is the total after week 6?", 700, [600, 800, 500],
          "Each week adds 100 cans: 500, 600, <b>700</b>. 600 is only week 5.")                       # 10
    story("A rainwater tank has 90 L, then 80 L, then 70 L. The same amount is used each day. "
          "How much is left after 3 more days?", 40, [67, 50, 100],
          "The tank loses 10 L each day. Count back in 10s 3 times: 60, 50, <b>40 L</b>.", unit=L)     # 11
    story("A toy kangaroo starts at 6 on a number line. It hops 5 each time: 6, 11, 16 … Where is it after 2 more hops?",
          26, [21, 31, 18],
          "Count on 5 two times from 16: 21, <b>26</b>. 18 adds 2, not 5.",
          fig(nline_svg(6, [5, 5, 5, 5], ticks=["6", "11", "16", None, "?"])))                          # 12
    story("{n} has 120 shells. {He} finds 10 more each day at the beach. How many shells after 5 days?",
          170, [125, 160, 180],
          "Count on in 10s 5 times: 130, 140, 150, 160, <b>170</b>. 125 adds 5, not 5 tens.")       # 13
    story("The school canteen has 80 icy poles. It sells 10 each day. How many are left after 4 days?",
          40, [76, 50, 120],
          "Count back in 10s 4 times: 70, 60, 50, <b>40</b>. 120 counts on, but the canteen sells them.")  # 14
    story("Page 1 of {n}’s sticker book has 4 stickers. Page 2 has 7 and page 3 has 10. How many are on page 5?",
          16, [13, 19, 12],
          "Each page has 3 more: 4, 7, 10, 13, <b>16</b>. 13 is page 4.")                           # 15
    story("At the athletics carnival, the runners’ numbers go 105, 110, 115 … What is the 6th number?",
          130, [125, 135, 120],
          "Count on in 5s: 105, 110, 115, 120, 125, <b>130</b>. That is 6 numbers.")                 # 16
    story("{n} has $20. {He} saves $5 each week. How much does {he} have after 4 more weeks?", 40, [24, 35, 45],
          "Count on in 5s 4 times: $25, $30, $35, <b>$40</b>. $24 adds 4, not 4 lots of $5.", unit=dol)  # 17
    story("{n} counts back in 3s from 30: 30, 27, 24 … What is the 5th number {he} says?", 18, [21, 15, 19],
          "Count back in 3s: 30, 27, 24, 21, <b>18</b>. 30 is the 1st number, so 18 is the 5th.")      # 18
    story("On a long drive, signs show how far it is to Brisbane: 900 km, 800 km, 700 km … "
          "They go down by 100 km each time. What does the 6th sign show?", 400, [500, 300, 890],
          "Count back in 100s: 900, 800, 700, 600, 500, <b>400 km</b>. That is 6 signs.",
          unit=lambda v: "%d km" % v)                                                               # 19
    k = its
    out = [k[0], k[2], k[1], k[3], k[5], k[8], k[9], k[7], k[4], k[14],
           k[11], k[6], k[13], k[12], k[16], k[15], k[17], k[18], k[10], k[19]]
    assert len({id(x) for x in out}) == 20
    return {"title": "Pattern word problems", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a number pattern?</h2>"
        "<p>A number pattern goes up or down by the <b>same amount</b> each time. "
        "That amount is the <b>rule</b>. In Year 2 you count on and back by 2s, 3s, 5s, 10s and 100s.</p>"
        + table(["Pattern", "Rule", "Goes"], [
            ["4, 6, 8, 10", "+2", "up"],
            ["12, 15, 18, 21", "+3", "up"],
            ["60, 55, 50, 45", MINUS + "5", "down"],
            ["83, 73, 63, 53", MINUS + "10", "down"],
            ["135, 235, 335, 435", "+100", "up"],
        ]) +
        "<h2>Find the rule</h2>"
        "<p>Look at two numbers next to each other. How much do you add or take away? "
        "Check that the same rule works for every jump.</p>"
        "<figure class='sn-fig'>" + nline_svg(3, [5, 5, 5], ticks=["3", "8", "13", "18"]) +
        "<figcaption>3, 8, 13, 18. Each jump is +5. The rule is +5, not +3.</figcaption></figure>"
        + ex("Missing number", "45, ☐, 55, 60",
             "The rule is +5 (55 to 60). 45 + 5 = 50. Check: 50 + 5 = 55.", "50") +
        "<h2>Patterns on a hundreds chart</h2>"
        "<p>On a hundreds chart, 1 more is one square to the right. "
        "<b>10 more</b> is one row <b>down</b>. 10 less is one row up.</p>"
        "<figure class='sn-fig'>" + chart_rows_svg(1, 3, set(seq(5, 5, 6))) +
        "<figcaption>Counting in 5s: 5, 10, 15, 20, 25, 30. The shaded squares end in 5 or 0.</figcaption></figure>"
        "<h2>Growing shape patterns</h2>"
        "<p>Shapes can make a pattern too. Count the shapes in each step. Find how many are added each time.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>4, 7, 10 sticks. Each new square needs 3 more sticks. Step 4 has 13 sticks.</figcaption></figure>"
        + ex("Shrinking pattern", "12, 10, 8, ☐",
             "Each step is 2 less. 8 − 2 = 6.", "6") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting on 1: 65, 70, 75, 76", "Add the rule every time: 75 + 5 = 80"],
            ["Using the first number as the rule: 3, 8, 13 is +3", "Find the jump between numbers: 8 − 3 = 5, so +5"],
            ["Counting back when it goes up: 35, 40, 45 is " + MINUS + "5", "The numbers get bigger, so the rule adds: +5"],
            ["Skipping a number: 46, 48, 50, 54", "Say every number in the pattern: 50, 52"],
            ["Changing the wrong digit: 27, 37, 47, 48", "In 10s the ones digit stays: 57"],
        ])
    )


FAQ = [
    {"q": "What number patterns do Year 2 students learn in Australia?",
     "a": "In the Australian Curriculum, Year 2 students make and describe patterns that go up or down by the same amount, such as counting by 2s, 3s, 5s, 10s and 100s, and find missing numbers in a pattern."},
    {"q": "How do you find the rule of a number pattern?",
     "a": "Look at two numbers next to each other and work out how much was added or taken away. For 3, 8, 13, 18 each number is 5 more, so the rule is +5."},
    {"q": "How do you find a missing number in a pattern?",
     "a": "Find the rule first, then use it on the number before the gap. For 45, ?, 55, 60 the rule is +5, so the missing number is 50."},
    {"q": "How does a hundreds chart help with patterns?",
     "a": "It shows patterns as shapes: counting in 10s goes straight down a column, and counting in 5s shades the columns ending in 5 and 0. This helps children see and check the rule."},
]


def gen():
    rnd = random.Random(2809)
    P = People(rnd)
    sets = [set_counting(), set_chart(), set_rule_missing(), set_shapes(), set_words(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 <= int(tok) <= 999, c
            k = it["q"]
            assert k not in allk, it["q"]
            allk.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "number-patterns",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Number Patterns: Count On and Back, Find the Rule",
        "seo_title": "Year 2 Number Patterns Worksheets: Skip Counting, Rules and Missing Numbers (Australian Curriculum)",
        "short_title": "Number patterns",
        "domain": "Algebra",
        "standard_code": "AC9M2A01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, describe and create additive patterns that increase or decrease by a constant amount, using numbers, shapes and objects, and identify missing elements in the pattern",
        "meta_desc": "Free Year 2 maths worksheets on number patterns: count on and back by 2s, 3s, 5s, 10s and 100s, find the rule (+5, −10), fill in missing numbers, spot patterns on a hundreds chart and continue growing shape patterns. 100 questions with an answer key, matched to the Australian Curriculum.",
        "key_big": "A number pattern goes up or down by the same amount each time. That amount is the rule.",
        "key_sub": "Find the jump between two numbers next to each other: 3, 8, 13, 18 has the rule +5. Use the rule to find the next or missing number: 45, ?, 55 is 50. If the numbers get smaller, the rule takes away: 90, 80, 70 is −10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number track|number line|hundreds chart rows|shape pattern|\\d+ coins)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
