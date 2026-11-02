# -*- coding: utf-8 -*-
"""
British Columbia Grade 2 Math: Repeating and increasing patterns (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g2_patterns.py
Repeating patterns and their core, translating patterns into letters and actions, increasing shape
patterns, increasing number patterns to 100 (+2, +5, +10) on number tracks, number lines and a
hundreds chart, missing elements, and real-life patterns and predictions in BC settings.
Wrong answers come from real mistakes: a wrong core (too short or too long), using only the first
step of a pattern, using the first number as the rule, counting on 1 instead of the step, going the
wrong way, changing the wrong digit, and mixing up the figure number and the number of objects.
Every answer is computed and checked in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
COLOURS = {"red": "#d64535", "blue": "#3b7dd8", "yellow": "#f2c230", "green": "#4caf50"}
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Sofia", "Emma", "Leah", "Zara", "Nadia", "Hana"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


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
    ok = [v for v in cands if v != ans and 0 <= v <= 999]
    assert 0 <= ans <= 999
    assert len(ok) == 3, (q, ans, cands)
    return mcq(q, fmt(ans), [fmt(v) for v in ok], e)


def balance(sets, rnd):
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def seq(start, step, n):
    return [start + step * k for k in range(n)]


def jump(d):
    return ("+%d" % d) if d > 0 else (MINUS + "%d" % -d)


def rule_text(start, d):
    if d > 0:
        return "Start at %d and add %d each time" % (start, d)
    return "Start at %d and subtract %d each time" % (start, -d)


def is_pattern(xs):
    d = xs[1] - xs[0]
    return d != 0 and all(xs[i + 1] - xs[i] == d for i in range(len(xs) - 1))


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


# ------------------------------------------------------------ repeating patterns (shapes, arrows, words)
def rep(core, n):
    return [core[i % len(core)] for i in range(n)]


def name(tok, mode):
    """'red circle' -> 'circle' (shape), 'red' (colour) or 'red circle' (both). 'arrow up' -> 'up'. 'w:clap' -> 'clap'."""
    if tok.startswith("w:"):
        return tok[2:]
    a, b = tok.split(" ")
    if a == "arrow":
        return b
    return {"shape": b, "colour": a, "both": tok}[mode]


def names(toks, mode):
    return ", ".join(name(t, mode) for t in toks)


def shape(kind, col, cx, cy, c):
    f = COLOURS[col]
    st = "stroke='%s' stroke-width='1.6' stroke-linejoin='round'" % INK
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' %s/>" % (cx, cy, 0.37 * c, f, st)
    if kind == "square":
        a = 0.66 * c
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' %s/>" % (cx - a / 2, cy - a / 2, a, a, f, st)
    if kind == "triangle":
        h, b = 0.68 * c, 0.8 * c
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' %s/>"
                % (cx, cy - h / 2, cx + b / 2, cy + h / 2, cx - b / 2, cy + h / 2, f, st))
    if kind == "star":
        pts = []
        for k in range(10):
            rr = 0.46 * c if k % 2 == 0 else 0.2 * c
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + 0.05 * c + rr * math.sin(a)))
        return "<polygon points='%s' fill='%s' %s/>" % (" ".join(pts), f, st)
    raise ValueError(kind)


def arrow(d, cx, cy, c):
    L = 0.36 * c
    pts = [(0, -L), (0.55 * L, -0.1 * L), (0.2 * L, -0.1 * L), (0.2 * L, L), (-0.2 * L, L), (-0.2 * L, -0.1 * L),
           (-0.55 * L, -0.1 * L)]
    a = math.radians({"up": 0, "right": 90, "down": 180, "left": 270}[d])
    p = ["%.1f,%.1f" % (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1' stroke-linejoin='round'/>" % (" ".join(p), GREEN, GREEN)


def row_svg(tokens, label="repeating pattern", numbered=False):
    """A row of tokens. '?' is a dashed box with a red ?. numbered: position numbers under the row."""
    words = any(t.startswith("w:") for t in tokens)
    c = 38
    w = 64 if words else c
    gap, m = 4, 4
    n = len(tokens)
    W = 2 * m + n * w + (n - 1) * gap
    H = 2 * m + c + (22 if numbered else 0)
    s = []
    for i, t in enumerate(tokens):
        x, y = m + i * (w + gap), m
        cx, cy = x + w / 2, y + c / 2
        if t == "?":
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
                     "stroke-dasharray='4 3'/>" % (x + 1, y + 1, w - 2, c - 2, FILL, GREEN))
            s.append(text(cx, cy + 7, "?", 20, col=RED))
        elif t.startswith("w:"):
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
                     % (x + 1, y + 1, w - 2, c - 2, GREEN))
            s.append(text(cx, cy + 5, t[2:], 15))
        else:
            a, b = t.split(" ")
            s.append(arrow(b, cx, cy, c) if a == "arrow" else shape(b, a, cx, cy, c))
        if numbered:
            s.append(text(cx, m + c + 18, str(i + 1), 14))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ number track, number line, table of values
TW, TH = 52, 36


def track_svg(nums):
    m = 4
    W, H = 2 * m + len(nums) * TW, 2 * m + TH
    s = []
    for i, v in enumerate(nums):
        x = m + i * TW
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, TW, TH, FILL if v is None else "#ffffff", GREEN))
        s.append(text(x + TW / 2, m + 24, "?" if v is None else str(v), 17, col=RED if v is None else INK))
    return svg_wrap(W, H, "".join(s), "number track")


def track(nums, hide=()):
    return fig(track_svg([None if k in hide else v for k, v in enumerate(nums)]))


def jw(j):
    return 80 if abs(j) >= 100 else (74 if abs(j) >= 10 else 58)


def nline_svg(start, jumps, ticks=None):
    if ticks is None:
        ticks = [str(start)] + [None] * (len(jumps) - 1) + ["?"]
    jl = [jump(j) for j in jumps]
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


def tov_svg(top, bot, heads):
    """Table of values: two rows. '?' shows red."""
    CW, RH = 46, 32
    LW = int(max(len(h) for h in heads) * 8.6 + 18)
    n = len(top)
    W, H = LW + CW * n + 4, RH * 2 + 4
    s = []
    for r, (hd, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 5, hd, 14))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, str(v), 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "table of values")


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
    def draw(x, y):
        s = [tile(x, y + i * T) for i in range(k)]
        s += [tile(x + i * T, y + (k - 1) * T) for i in range(1, k)]
        return "".join(s)
    return k * T, k * T, draw


TS, TRH = 26, 22.5


def triangles(k):
    def draw(x, y):
        pts = [(x + i * TS / 2, y + (TRH if i % 2 == 0 else 0)) for i in range(k + 2)]
        s = [stick(*pts[i], *pts[i + 1]) for i in range(k + 1)]
        for j in range(k):
            s.append(stick(*pts[j], *pts[j + 2]))
        return "".join(s)
    return (k + 1) * TS / 2, TRH, draw


SQ = 24


def squares(k):
    def draw(x, y):
        s = [stick(x + i * SQ, y, x + i * SQ, y + SQ) for i in range(k + 1)]
        for i in range(k):
            s.append(stick(x + i * SQ, y, x + (i + 1) * SQ, y))
            s.append(stick(x + i * SQ, y + SQ, x + (i + 1) * SQ, y + SQ))
        return "".join(s)
    return k * SQ, SQ, draw


def dot_rows(k):
    def draw(x, y):
        return "".join("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x + 7 + c * 14, y + 7 + r * 14, GREEN)
                       for r in range(k) for c in range(5))
    return 5 * 14, k * 14, draw


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


def stairs(k):
    """Staircase: columns of 1, 2, ... k tiles = 1, 3, 6, 10 (adds one more each time)."""
    def draw(x, y):
        return "".join(tile(x + i * T, y + (k - 1 - j) * T) for i in range(k) for j in range(i + 1))
    return k * T, k * T, draw


PATTERNS = {
    "L": (L_shape, lambda k: 2 * k - 1, "tiles"),
    "tri": (triangles, lambda k: 2 * k + 1, "sticks"),
    "sq": (squares, lambda k: 3 * k + 1, "sticks"),
    "dots": (dot_rows, lambda k: 5 * k, "dots"),
    "towers": (towers3, lambda k: 3 * k + 3, "cubes"),
    "tables": (tables, lambda k: 2 * k + 2, "chairs"),
    "stairs": (stairs, lambda k: k * (k + 1) // 2, "tiles"),
}


def cnt(nm, k):
    return PATTERNS[nm][1](k)


def thing(nm):
    return PATTERNS[nm][2]


def pattern_svg(nm, steps=(1, 2, 3), hide=None):
    """Figures side by side, bottoms lined up, 'Figure k' under each. hide = figure drawn as a ? box."""
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
    return svg_wrap(int(round(W)), int(round(H)), "".join(s), "shape pattern %s" % nm)



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




# ------------------------------------------------------------ Grade 2 extras
def col(k):
    """A tower of k + 1 cubes: 2, 3, 4 ..."""
    def draw(x, y):
        return "".join(tile(x, y + j * T) for j in range(k + 1))
    return T, (k + 1) * T, draw


def pairs(k):
    """2 rows of k tiles: 2, 4, 6 ..."""
    def draw(x, y):
        return "".join(tile(x + i * T, y + r * T) for r in range(2) for i in range(k))
    return k * T, 2 * T, draw


PATTERNS["col"] = (col, lambda k: k + 1, "cubes")
PATTERNS["pairs"] = (pairs, lambda k: 2 * k, "tiles")


def coins_svg(n, kind):
    """Canadian coins in rows of 5: nickel 5¢, dime 10¢, toonie $2."""
    if kind == "nickel":
        r, fill, edge, lab, fs = 20, "#dfe3e7", "#7a828a", "5¢", 14
    elif kind == "dime":
        r, fill, edge, lab, fs = 22, "#dfe3e7", "#7a828a", "10¢", 14
    else:
        r, fill, edge, lab, fs = 22, "#dfe3e7", "#7a828a", "$2", 15
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
        if kind == "toonie":
            s.append("<circle cx='%d' cy='%d' r='%d' fill='#e8c25a' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 7, "#9a7a1c"))
        else:
            s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 4, edge))
        s.append(text(cx, cy + 5, lab, fs))
    return svg_wrap(W, H, "".join(s), "%d coins" % n)


def add_text(start, d):
    if d > 0:
        return "Start at %d. Add %d each time." % (start, d)
    return "Start at %d. Take away %d each time." % (start, -d)


def each(d):
    return ("add %d each time" % d) if d > 0 else ("take away %d each time" % -d)


# ============================================================ set 1: repeating patterns and the core
AB = ["blue circle", "blue square"]
ABB = ["red circle", "blue circle", "blue circle"]
ABC = ["green triangle", "green circle", "green square"]
AABB = ["yellow star", "yellow star", "red star", "red star"]
AAB = ["blue square", "blue square", "red triangle"]
ARR = ["arrow up", "arrow right", "arrow down", "arrow left"]
SOUNDS = ["w:clap", "w:stomp", "w:stomp"]


def next_rep(core, shown, mode, cands, extra="", lead="The pattern repeats. What comes next?"):
    toks = rep(core, shown)
    a = rep(core, shown + 1)[-1]
    e = "The core is <b>%s</b>. It repeats again and again. So next comes <b>%s</b>.%s" % (
        names(core, mode), name(a, mode), extra)
    return mcq(fig(row_svg(toks + ["?"])) + lead, name(a, mode), cands, e)


def set_repeating():
    q1 = next_rep(AB, 7, "shape", ["circle", "triangle", "star"], " A circle is always followed by a square.")
    q2 = next_rep(ABB, 8, "colour", ["red", "yellow", "green"], " After red come two blues. Then red again.")
    q3 = next_rep(ABC, 7, "shape", ["triangle", "square", "star"])
    q4 = next_rep(ARR, 6, "shape", ["up", "left", "right"], " The arrow turns a quarter turn each time, like a clock.")
    q5 = next_rep(SOUNDS, 7, "shape", ["clap", "snap", "jump"],
                  " There are two stomps in each core, not one.", "Kai makes a sound pattern. What comes next?")
    q6 = next_rep(AAB, 8, "both", ["blue square", "red square", "blue triangle"],
                  " Both the shape and the colour change. It is a red triangle.")

    def core_q(core, shown, mode, cands, extra):
        return mcq(fig(row_svg(rep(core, shown))) + "What is the core of this pattern?", names(core, mode), cands,
                   "The core is the part that repeats. Here it is <b>%s</b>. Then it starts again.%s"
                   % (names(core, mode), extra))

    q7 = core_q(AB, 8, "shape", ["circle", "circle, square, circle", "circle, circle, square"],
                " “circle, square, circle” is too long. It goes into the next core.")
    q8 = core_q(ABB, 9, "colour", ["red, blue", "red, blue, blue, red", "blue, blue"],
                " “red, blue” is too short. After red come two blues.")
    q9 = core_q(ABC, 9, "shape", ["triangle, circle", "circle, square", "triangle, circle, square, triangle"],
                " Check by saying it: triangle, circle, square, triangle, circle, square.")
    q10 = mcq(fig(row_svg(rep(ABB, 6))) + "Which letters show the same pattern?", "A B B A B B",
              ["A B A B A B", "A A B A A B", "A B C A B C"],
              "Red is A. Blue is B. Red, blue, blue is A, B, B. So the pattern is <b>A B B A B B</b>.")
    q11 = mcq(fig(row_svg(rep(AABB, 8))) + "Which letters show the same pattern?", "A A B B A A B B",
              ["A B A B A B A B", "A A B A A B A A", "A B B A A B B A"],
              "Yellow is A. Red is B. Two yellow, two red: A, A, B, B. So it is <b>A A B B A A B B</b>.")
    q12 = mcq("Owen moves in a pattern: hop, hop, turn, hop, hop, turn. Which letters show the same pattern?",
              "A A B A A B", ["A B A B A B", "A B B A B B", "A A B B A A"],
              "Hop is A. Turn is B. Hop, hop, turn is A, A, B. So it is <b>A A B A A B</b>.")
    q13 = mcq("Which pattern has the core A, B, B?", "A B B A B B A B B",
              ["A B A B A B A B", "A A B A A B A A B", "A B B B A B B B"],
              "The core is one A and two Bs. Say it again and again: <b>A B B A B B A B B</b>.")
    q14 = nums_mcq(fig(row_svg(rep(AABB, 8))) + "How many shapes are in the core of this pattern?", 4, [2, 8, 3],
                   "The core is yellow, yellow, red, red. That is <b>4</b> shapes. 2 is the number of colours, not shapes.")
    nx = rep(AAB, 8)[6:]
    assert nx == ["blue square", "blue square"]
    q15 = mcq(fig(row_svg(rep(AAB, 6) + ["?", "?"])) + "The pattern repeats. What are the next two shapes?",
              "blue square, blue square",
              ["blue square, red triangle", "red triangle, blue square", "red triangle, red triangle"],
              "The core is blue square, blue square, red triangle. The row ends with a red triangle. "
              "So the core starts again: <b>blue square, blue square</b>.")
    nums = rep([1, 2, 2], 9)
    q16 = mcq(track(nums + [None]) + "The pattern repeats. What number comes next?", "1", ["2", "3", "0"],
              "The core is 1, 2, 2. The row ends with 2, 2. So next comes <b>1</b>. 3 counts on, but this is a repeating pattern.")
    q17 = mcq("Which of these is NOT a repeating pattern?", "A B A A B B B A",
              ["A B A B A B A B", "A A B A A B A A B", "A B C A B C A B C"],
              "The others repeat the same core each time. <b>A B A A B B B A</b> has no part that repeats.")
    bad = rep(ABB, 9)
    bad[4] = "red circle"
    assert rep(ABB, 9)[4] == "blue circle"
    q18 = mcq(fig(row_svg(bad, numbered=True)) + "Jasleen makes a pattern: red, blue, blue. "
              "She makes one mistake. Which circle is wrong?", "circle 5", ["circle 4", "circle 7", "circle 6"],
              "Red goes at 1, 4 and 7. Circles 5 and 6 should be blue. <b>Circle 5</b> is red, so it is the mistake.")
    q19 = nums_mcq("Simran makes a pattern with the core square, circle, circle. She makes the core 3 times. "
                   "How many circles does she use?", 6, [3, 2, 9],
                   "Each core has 2 circles. 3 cores: 2 + 2 + 2 = <b>6</b> circles. 3 counts only 1 circle in each core.")
    q20 = mcq("Hana makes a pattern with blocks: red, red, blue. She wants to show the same pattern with sounds. "
              "Which one works?", "clap, clap, snap", ["clap, snap, snap", "clap, snap", "clap, clap, clap"],
              "Red, red, blue is A, A, B. Clap, clap, snap is also A, A, B. So <b>clap, clap, snap</b> works.")
    out = [q1, q2, q3, q7, q10, q16, q8, q4, q5, q14, q11, q9, q6, q12, q13, q19, q15, q17, q18, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Repeating patterns and the core", "items": out}


# ============================================================ set 2: growing shape patterns
def set_growing():
    def d_of(nm):
        return cnt(nm, 2) - cnt(nm, 1)

    def next_q(nm, cands, extra=""):
        th = thing(nm)
        a, last, d = cnt(nm, 4), cnt(nm, 3), d_of(nm)
        e = "Count each figure: %s. Each figure has %d %s %s. %d %s %d = <b>%d</b> %s.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", th[:-1] if abs(d) == 1 else th,
            last, "+" if d > 0 else MINUS, abs(d), a, th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure 4?" % th, a, cands, e)

    def far_q(nm, k, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, j) for j in range(1, k + 1)]
        e = "Keep adding %d: %s. Figure %d has <b>%d</b> %s.%s" % (d_of(nm), lst(vals), k, vals[-1], th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure %d?" % (th, k),
                        vals[-1], cands, e)

    def which_q(nm, n, extra=""):
        th = thing(nm)
        vals = [cnt(nm, k) for k in range(1, 12)]
        k = vals.index(n) + 1
        e = "Keep going: %s. Figure <b>%d</b> has %d %s. %d is the number of %s, not the figure number.%s" % (
            lst(vals[:k]), k, n, th, n, th, extra)
        return mcq(fig(pattern_svg(nm)) + "The pattern keeps going. Which figure has %d %s?" % (n, th),
                   "Figure %d" % k, ["Figure %d" % n, "Figure %d" % (k + 1), "Figure %d" % (k - 1)], e)

    def rule_q(nm, cands, extra=""):
        d, s0 = d_of(nm), cnt(nm, 1)
        e = "Figure 1 has %d %s. Count each figure: %s. The rule is <b>start at %d and %s</b>.%s" % (
            s0, thing(nm)[:-1] if s0 == 1 else thing(nm), lst([cnt(nm, k) for k in (1, 2, 3)]), s0, each(d), extra)
        return mcq(fig(pattern_svg(nm)) + "What is the pattern rule for the number of %s?" % thing(nm),
                   add_text(s0, d), [add_text(a, b) for a, b in cands], e)

    q1 = next_q("col", [4, 6, 8], " 4 is Figure 3 again. 6 adds 2, not 1.")
    q2 = next_q("pairs", [7, 10, 6], " 7 counts on 1, not 2.")
    q3 = next_q("L", [6, 9, 5], " 6 counts on 1, not 2.")
    q4 = next_q("dots", [16, 25, 15], " 16 counts on 1, not 5.")
    q5 = next_q("tri", [8, 4, 11], " Count the sticks, not the triangles.")
    q6 = next_q("towers", [13, 18, 14], " Each new tower has 3 cubes.")
    q7 = far_q("dots", 5, [21, 20, 5], " 20 is Figure 4. 21 counts on 1, not 5.")
    q8 = next_q("tables", [9, 12, 16], " 16 gives each table 4 chairs. But no chairs fit where the tables touch.")
    q9 = nums_mcq(fig(pattern_svg("sq")) + "How many sticks are added each time?", 3, [4, 1, 10],
                  "Count: 4, 7, 10. 4 + 3 = 7 and 7 + 3 = 10. <b>3</b> sticks are added each time. "
                  "4 is how many sticks Figure 1 has. It is not the jump.")
    q10 = mcq(fig(pattern_svg("dots")) + "What kind of pattern is this?", "increasing pattern",
              ["decreasing pattern", "repeating pattern", "not a pattern"],
              "Count: 5, 10, 15. Each figure has more dots. It is an <b>increasing pattern</b>.")
    q11 = which_q("towers", 15)
    q12 = which_q("dots", 30)
    q13 = which_q("pairs", 12)
    q14 = which_q("L", 9)
    st = [cnt("stairs", k) for k in range(1, 5)]
    assert st == [1, 3, 6, 10]
    q15 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 4?", 10,
                   [8, 9, 12],
                   "Count: 1, 3, 6. The jumps are +2, then +3. Each jump is 1 more, so the next jump is +4. "
                   "6 + 4 = <b>10</b>. 8 uses only the first step (+2).")
    q16 = far_q("col", 5, [5, 7, 10], " 5 is the figure number. Each tower has 1 more cube than its figure number.")
    q17 = far_q("tri", 5, [9, 13, 15], " 15 counts 3 sticks for each triangle. But the triangles share sticks.")
    q18 = far_q("sq", 6, [16, 24, 22], " 24 counts 4 sticks for each square. But the squares share sticks.")
    q19 = rule_q("L", [(1, 1), (2, 2), (1, 3)])
    q20 = rule_q("sq", [(4, 4), (3, 3), (1, 3)], " 4 is how many sticks Figure 1 has. It is not the jump.")
    out = [q1, q2, q3, q10, q4, q11, q5, q7, q6, q9, q8, q12, q13, q16, q19, q14, q17, q15, q20, q18]
    assert len({id(x) for x in out}) == 20
    return {"title": "Increasing shape patterns", "items": out}


# ============================================================ set 3: number patterns to 100
def set_numbers():
    def nxt(nums, cands, extra=""):
        assert is_pattern(nums) and max(nums) <= 100
        d = nums[1] - nums[0]
        a = nums[-1] + d
        e = "Each number is %d %s. %d %s %d = <b>%d</b>.%s" % (
            abs(d), "more" if d > 0 else "less", nums[-1], "+" if d > 0 else MINUS, abs(d), a, extra)
        return nums_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)

    q1 = nxt([10, 12, 14, 16], [17, 20, 16], " 17 is only 1 more.")
    q2 = nxt([20, 25, 30, 35], [36, 45, 35], " 36 is only 1 more.")
    q3 = nxt([14, 24, 34], [35, 54, 45], " The ones digit stays 4. Only the tens digit goes up.")
    q4 = nxt([50, 60, 70], [71, 60, 90], " 71 is only 1 more. 90 jumps 20, not 10.")
    q5 = nxt([36, 38, 40], [41, 44, 39], " 41 is only 1 more.")
    q6 = nxt([55, 60, 65], [66, 75, 60], " Counting by 5s, the numbers end in 5 or 0.")
    q7 = nxt([23, 33, 43], [44, 63, 45], " With +10, the ones digit stays 3. 44 changes the ones digit.")
    q8 = nxt([68, 70, 72], [73, 82, 72], " 73 is only 1 more. 82 adds 10, not 2.")

    def rq(nums, wrong, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        e = "%d %s %d = %d. Every jump is the same. The rule is <b>%s</b>.%s" % (
            nums[0], "+" if d > 0 else MINUS, abs(d), nums[1], each(d), extra)
        return mcq(track(nums) + "What is the pattern rule?", each(d), [each(w) for w in wrong], e)

    q9 = rq([35, 40, 45, 50], [10, -5, 1], " The numbers go up, so the rule adds.")
    q10 = rq([3, 8, 13, 18], [3, 1, -5], " 3 is the first number, not the jump.")
    q11 = rq([62, 72, 82, 92], [-10, 1, 20], " The numbers go up, so the rule adds.")
    q12 = rq([41, 43, 45, 47], [1, 4, -2], " The numbers are odd. Counting by 2s from an odd number gives odd numbers.")

    def line(start, d, n, cands):
        a = start + d * n
        pts = seq(start + d, d, n)
        q = fig(nline_svg(start, [d] * n)) + "Start at %d. Make the jumps. Where do you land?" % start
        return nums_mcq(q, a, cands, "Each jump is %s. Count %s by %ds from %d: %s. You land on <b>%d</b>." % (
            jump(d), "on" if d > 0 else "back", abs(d), start, lst(pts), a))

    q13 = line(30, 5, 4, [34, 55, 45])
    q14 = line(65, 10, 3, [68, 85, 75])

    def shade(first, nrows, start, d, n, cands, how):
        sh = seq(start, d, n)
        a = sh[-1] + d
        assert a < first + 10 * nrows
        q = (fig(chart_rows_svg(first, nrows, set(sh))) +
             "The shaded squares count by %ds. What is the next shaded number?" % d)
        return nums_mcq(q, a, cands, "%d + %d = <b>%d</b>. %s" % (sh[-1], d, a, how))

    q15 = shade(1, 2, 2, 2, 6, [13, 16, 22], "Shade every second square.")
    q16 = shade(1, 5, 4, 10, 3, [35, 44, 25], "By 10s, go straight down one row. The ones digit stays 4.")

    def piece(tl, rows, cols, tgt, hide, cands):
        r, c = tgt
        a = tl + 10 * r + c
        vis = lambda rr, cc: 0 <= rr < rows and 0 <= cc < cols and (rr, cc) not in hide and (rr, cc) != tgt
        if vis(r - 1, c):
            ref = a - 10
            e = "The number just above is 10 less. So the ? is 10 more than %d. %d + 10 = <b>%d</b>." % (ref, ref, a)
        else:
            assert vis(r + 1, c)
            ref = a + 10
            e = "The number just below is 10 more. So the ? is 10 less than %d. %d − 10 = <b>%d</b>." % (ref, ref, a)
        q = fig(piece_svg(tl, rows, cols, tgt, hide)) + "This is part of a hundreds chart. What number goes in the box with the ?"
        return nums_mcq(q, a, cands, e)

    q17 = piece(23, 3, 3, (2, 1), set(), [35, 54, 45])
    q18 = piece(56, 3, 4, (0, 2), {(2, 0)}, [48, 59, 78])
    q19 = nums_mcq("Ryan counts by 5s from 0: 0, 5, 10, 15 … Which number will he say?", 45, [42, 51, 48],
                   "Counting by 5s from 0, every number ends in 5 or 0. Only <b>45</b> ends that way.")
    q20 = nums_mcq("Nadia counts by 10s from 6: 6, 16, 26 … Which number will she say?", 56, [60, 65, 50],
                   "Counting by 10s from 6, every number ends in 6. Only <b>56</b> ends in 6. "
                   "60 and 50 are what you say counting by 10s from 0.")
    out = [q1, q2, q5, q4, q9, q3, q6, q13, q11, q15, q7, q10, q17, q8, q16, q12, q14, q18, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Increasing number patterns to 100", "items": out}


# ============================================================ set 4: missing elements
def set_missing():
    def gap_rep(core, n, i, mode, cands):
        toks = rep(core, n)
        a = toks[i]
        toks[i] = "?"
        e = "The core is <b>%s</b>. Say the pattern from the start: %s. The missing one is <b>%s</b>." % (
            names(core, mode), names(rep(core, i + 1), mode), name(a, mode))
        return mcq(fig(row_svg(toks)) + "What is missing from this pattern?", name(a, mode), cands, e)

    q1 = gap_rep(AB, 8, 4, "shape", ["square", "triangle", "star"])
    q2 = gap_rep(ABB, 9, 5, "colour", ["red", "yellow", "green"])
    q3 = gap_rep(ABC, 9, 7, "shape", ["triangle", "square", "star"])
    q4 = gap_rep(AAB, 9, 2, "both", ["blue square", "red square", "blue triangle"])
    q5 = gap_rep(ARR, 8, 5, "shape", ["up", "down", "left"])

    def miss(nums, i, cands, extra=""):
        assert is_pattern(nums) and max(nums) <= 100
        d = nums[1] - nums[0]
        a = nums[i]
        if i == 0:
            e = "The rule is %s. Go back one step from %d: %d %s %d = <b>%d</b>." % (
                each(d), nums[1], nums[1], MINUS if d > 0 else "+", abs(d), a)
        else:
            e = "The rule is %s. %d %s %d = <b>%d</b>." % (each(d), nums[i - 1], "+" if d > 0 else MINUS, abs(d), a)
            if i < len(nums) - 1:
                e += " Check: %d %s %d = %d." % (a, "+" if d > 0 else MINUS, abs(d), nums[i + 1])
        return nums_mcq(track(nums, (i,)) + "What number is missing?", a, cands, e + extra)

    q6 = miss([30, 40, 50, 60, 70], 2, [41, 60, 45])
    q7 = miss([15, 20, 25, 30], 2, [21, 30, 35])
    q8 = miss([12, 14, 16, 18], 0, [13, 20, 15], " The first number is 2 less than 14.")
    q9 = miss([60, 70, 80, 90], 1, [61, 80, 75])
    q10 = miss([46, 48, 50, 52], 2, [49, 51, 54])
    q11 = miss([65, 70, 75, 80, 85], 3, [76, 85, 90])
    q12 = miss([28, 38, 48, 58], 2, [39, 58, 49])

    def two(nums, i, j, wrong):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = "%d, %d" % (nums[i], nums[j])
        e = "The rule is %s. Fill in each box: %s. The missing numbers are <b>%s</b>." % (each(d), lst(nums), a)
        return mcq(track(nums, (i, j)) + "Which two numbers are missing, in order?", a, wrong, e)

    q13 = two([10, 15, 20, 25, 30], 1, 3, ["11, 21", "25, 15", "20, 30"])
    q14 = two([22, 24, 26, 28, 30], 1, 3, ["23, 27", "28, 24", "26, 30"])
    lv = [cnt("L", k) for k in (1, 2, 3)]
    q15 = nums_mcq(fig(pattern_svg("L", hide=2)) + "Figure 2 is hidden. How many tiles are in Figure 2?", lv[1],
                   [4, 2, 6],
                   "Figure 1 has 1 tile. Figure 3 has 5 tiles. The pattern goes up by the same amount each time: "
                   "1, <b>3</b>, 5. The rule is add 2.")
    pv = [cnt("pairs", k) for k in (1, 2, 3, 4)]
    q16 = nums_mcq(fig(pattern_svg("pairs", (1, 2, 3, 4), hide=3)) + "Figure 3 is hidden. How many tiles are in Figure 3?",
                   pv[2], [5, 8, 3],
                   "Count: 2, 4, ?, 8. Each figure has 2 more tiles. 4 + 2 = <b>6</b>. Check: 6 + 2 = 8. "
                   "3 is the figure number.")
    sv = [cnt("sq", k) for k in (1, 2, 3, 4)]
    q17 = nums_mcq(fig(pattern_svg("sq", (2, 3, 4))) + "Figure 1 is not shown. How many sticks are in Figure 1?", sv[0],
                   [3, 1, 7],
                   "Count: Figure 2 has 7, Figure 3 has 10, Figure 4 has 13. Each figure adds 3 sticks. "
                   "Go back one step: 7 − 3 = <b>4</b>.")
    q18 = nums_mcq(track([20, 30, 40, 45, 60]) + "One number in this pattern is wrong. Which one?", 45, [30, 40, 60],
                   "The rule is add 10: 20, 30, 40, 50, 60. <b>45</b> should be 50.")
    q19 = nums_mcq("Liam counts by 5s: 35, 40, 45, 49, 55. One number is a mistake. What should it be?", 50,
                   [46, 59, 45],
                   "Counting by 5s: 35, 40, 45, <b>50</b>, 55. 45 + 5 = 50, not 49.")
    q20 = nums_mcq(track([1, 3, 6, None, 15]) + "What number is missing?", 10, [8, 9, 12],
                   "The jumps are +2, +3, then +4, then +5. 6 + 4 = <b>10</b>. Check: 10 + 5 = 15. "
                   "8 uses only the first step (+2).")
    out = [q1, q6, q2, q7, q3, q9, q8, q5, q10, q4, q15, q11, q13, q12, q16, q14, q18, q17, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Find the missing elements", "items": out}


# ============================================================ set 5: real-life patterns and predictions
def set_real(P):
    def nth(core, shown, n, mode, cands, lead, thingname):
        a = rep(core, n)[-1]
        L = len(core)
        pos = [k for k in range(1, n + 1) if (k - 1) % L == (n - 1) % L]
        assert all(rep(core, k)[-1] == a for k in pos)
        if mode == "colour":
            where = "%s %ss are at %s." % (name(a, mode).capitalize(), thingname, lst(pos))
            ans = name(a, mode)
        else:
            where = "%ss are at %s." % (name(a, mode).capitalize(), lst(pos))
            ans = "a " + name(a, mode)
        e = ("The core has %d %ss. Keep the pattern going and count. %s So the %s %s is <b>%s</b>."
             % (L, thingname, where, ordn(n), thingname, ans))
        return mcq(fig(row_svg(rep(core, shown))) + lead, name(a, mode), cands, e)

    d = P.next()
    q1 = nth(ABB, 6, 10, "colour", ["blue", "yellow", "green"],
             "{n} strings beads in this pattern. {He} keeps going. What colour is the 10th bead?".format(**d), "bead")
    d = P.next()
    q2 = nth(AB, 6, 11, "shape", ["square", "triangle", "star"],
             "{n} lays out blocks in this pattern. {He} keeps going. What shape is the 11th block?".format(**d), "block")
    q3 = nth(AABB, 8, 10, "colour", ["red", "blue", "green"],
             "A classroom banner has stars in this pattern. What colour is the 10th star?", "star")

    def story(t, ans, cands, e, pic="", unit=None):
        dd = P.next()
        return nums_mcq(pic + t.format(**dd), ans, cands, e.format(**dd), unit or str)

    cents = lambda v: "%d¢" % v
    dol = lambda v: "$%d" % v
    q4 = story("{n} counts nickels by 5s. How much money is this?", 30, [6, 25, 35],
               "Count by 5s: 5, 10, 15, 20, 25, <b>30¢</b>. 6¢ counts the coins, not the cents.",
               fig(coins_svg(6, "nickel")), cents)
    q5 = story("{n} counts dimes by 10s. How much money is this?", 70, [7, 60, 80],
               "Count by 10s: 10, 20, 30, 40, 50, 60, <b>70¢</b>. 7¢ counts the coins, not the cents.",
               fig(coins_svg(7, "dime")), cents)
    q6 = story("{n} counts toonies by 2s. A toonie is $2. How much money is this?", 10, [5, 7, 12],
               "Count by 2s: 2, 4, 6, 8, <b>$10</b>. $5 counts the coins, not the dollars.",
               fig(coins_svg(5, "toonie")), dol)
    q7 = story("A pair of mitts has 2 mitts. How many mitts are in 8 pairs?", 16, [8, 10, 18],
               "Count by 2s 8 times: 2, 4, 6, 8, 10, 12, 14, <b>16</b>. 8 is the number of pairs.")
    q8 = story("{n} has 10 loonies in {his} piggy bank. {He} adds 5 loonies each week. "
               "How many loonies are there after 4 weeks?", 30, [20, 25, 35],
               "Start at 10 and add 5 each week: 15, 20, 25, <b>30</b>. 20 forgets the 10 loonies {he} started with.")
    q9 = story("{n} skates at the rink in Kamloops. {He} skates 2 laps on Monday, 4 laps on Tuesday and 6 laps on Wednesday. "
               "The pattern keeps going. How many laps does {he} skate on Friday?", 10, [8, 7, 12],
               "Add 2 each day: Thursday 8, Friday <b>10</b>. 8 is Thursday.")
    q10 = story("A sunflower is 20 cm tall. It grows 10 cm each week. How tall is it after 3 weeks?", 50,
                [30, 23, 40],
                "Add 10 each week: 30, 40, <b>50 cm</b>. 30 is only 1 week. 23 adds 1 each week, not 10.",
                unit=lambda v: "%d cm" % v)
    q11 = mcq("{n} has gym class every Tuesday. The first three are on November 3, November 10 and November 17. "
              "When is the next one?".format(**P.next()),
              "November 24", ["November 18", "November 22", "November 27"],
              "There are 7 days in a week. Add 7 each time: 3, 10, 17, <b>24</b>. November 18 is only the next day. "
              "November 27 adds 10, not 7.")
    q12 = story("{n} gets 10 stickers each day. How many stickers does {he} have after 5 days?", 50, [15, 40, 60],
                "Count by 10s 5 times: 10, 20, 30, 40, <b>50</b>. 15 adds 10 and 5.")
    q13 = story("The class library in Surrey has 20 books. Each week, students bring 5 more books. "
                "How many books are there after 4 weeks?", 40, [24, 35, 9],
                "Add 5 each week: 25, 30, 35, <b>40</b>. 35 is after 3 weeks. 24 adds 1 each week. 9 adds 4 and 5.")
    q14 = story("{n} plants tulips in this pattern: red, red, yellow, red, red, yellow … {He} plants 12 tulips. "
                "How many are yellow?", 4, [8, 3, 6],
                "The core red, red, yellow has 3 tulips. 12 tulips make 4 cores: 3, 6, 9, 12. "
                "Each core has 1 yellow, so <b>4</b> are yellow. 8 is the number of red tulips.")
    d = P.next()
    q15 = mcq("{n} counts by 10s from 0. {He} says, “I will say 75.” Is {he} right?".format(**d),
              "No. {He} says numbers that end in 0.".format(**d),
              ["Yes. 75 is less than 100.", "Yes. 75 has a 7 in it.", "No. {He} stops at 50.".format(**d)],
              "Counting by 10s from 0: 10, 20, 30 … 70, 80. Every number ends in 0. "
              "75 ends in 5, so <b>{he} is not right</b>.".format(**d))
    q16 = story("Each canoe on the lake has 2 paddles. How many paddles are in 9 canoes?", 18, [11, 9, 20],
                "Count by 2s 9 times: 2, 4, 6, 8, 10, 12, 14, 16, <b>18</b>. 11 adds 9 and 2.")
    q17 = story("{n} builds towers. Tower 1 has 3 blocks. Tower 2 has 5 blocks. Tower 3 has 7 blocks. "
                "How many blocks are in Tower 6?", 13, [11, 18, 9],
                "Add 2 each time: 3, 5, 7, 9, 11, <b>13</b>. 18 uses 3 as the jump, but 3 is only Tower 1. 11 is Tower 5.")
    q18 = story("7 students each hold up one hand. Count the fingers by 5s. How many fingers are there?", 35,
                [12, 30, 40],
                "Count by 5s 7 times: 5, 10, 15, 20, 25, 30, <b>35</b>. 12 adds 7 and 5.")
    quilt = ["yellow square", "green square", "green square"]
    assert sum(1 for t in rep(quilt, 15) if t == "green square") == 10
    q19 = story("A quilt has a row of squares in this pattern. The row has 15 squares. How many are green?", 10,
                [5, 8, 12],
                "The core is yellow, green, green. 15 squares make 5 cores: 3, 6, 9, 12, 15. "
                "Each core has 2 green, so 2, 4, 6, 8, <b>10</b>. 5 counts only 1 green in each core.",
                fig(row_svg(rep(quilt, 6))))
    q20 = story("A Grade 2 class collects money for the Terry Fox Run. They have $15 after week 1, $25 after week 2 "
                "and $35 after week 3. The pattern keeps going. How much do they have after week 5?", 55,
                [45, 40, 75],
                "Add $10 each week: $15, $25, $35, $45, <b>$55</b>. $45 is week 4. "
                "$75 adds $15 each week, but $15 is only where they started.", unit=dol)
    assert 10 + 5 * 4 == 30 and 20 + 30 == 50 and 20 + 5 * 4 == 40 and 3 + 2 * 5 == 13 and 15 + 10 * 4 == 55
    out = [q4, q1, q7, q5, q2, q12, q6, q9, q3, q18, q8, q10, q16, q13, q11, q14, q19, q15, q17, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Real-life patterns and predictions", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Repeating patterns and the core</h2>"
        "<p>A <b>repeating pattern</b> has a part that repeats again and again. That part is the <b>core</b>. "
        "Find the core, then say the pattern out loud to check it.</p>"
        "<figure class='sn-fig'>" + row_svg(rep(ABB, 9)) +
        "<figcaption>The core is red, blue, blue. In letters it is A, B, B.</figcaption></figure>"
        "<p>You can show the same pattern in a new way. Red, blue, blue can be clap, snap, snap or A, B, B.</p>"
        "<h2>Increasing shape patterns</h2>"
        "<p>An <b>increasing pattern</b> gets bigger each time. "
        "Count each figure. Then find how many are added each time.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>4, 7, 10 sticks. The rule is start at 4 and add 3 each time.</figcaption></figure>"
        "<h2>Increasing number patterns to 100</h2>"
        "<p>Find the jump from one number to the next. Check that the same jump works every time.</p>"
        "<figure class='sn-fig'>" + nline_svg(30, [5, 5, 5], ticks=["30", "35", "40", "45"]) +
        "<figcaption>30, 35, 40, 45. The rule is start at 30 and add 5 each time.</figcaption></figure>"
        + ex("Next number", "14, 24, 34, ☐",
             "The jump is +10. Only the tens digit goes up. 34 + 10 = 44.", "44")
        + ex("Missing number", "60, ☐, 80, 90",
             "The rule is add 10. 60 + 10 = 70. Check: 70 + 10 = 80.", "70")
        + ex("Predict", "Beads go red, blue, blue, red, blue, blue … What colour is the 10th bead?",
             "Red is at 1, 4, 7 and 10.", "red") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Wrong core: red, blue, blue has the core “red, blue”", "Say it again and again to check: red, blue, blue"],
            ["Using only the first step: 1, 3, 6 is “add 2”", "Check every jump: +2, +3, so the next jump is +4"],
            ["Using the first number as the rule: 4, 7, 10 is “add 4”", "Find the jump: start at 4 and add 3 each time"],
            ["Counting on 1: 20, 25, 30, 31", "Use the same jump each time: 20, 25, 30, 35"],
            ["Mixing up the figure number and the number of objects", "Figure 3 is the 3rd picture. Count what is in it"],
        ])
    )


FAQ = [
    {"q": "What patterns do Grade 2 students learn in BC math?",
     "a": "In the BC curriculum (Patterning), Grade 2 students make, describe and extend repeating patterns and increasing patterns. They find the core, find missing parts and make number patterns to 100 by 2s, 5s and 10s."},
    {"q": "What is the core of a repeating pattern?",
     "a": "The core is the part of the pattern that repeats. In red, blue, blue, red, blue, blue, the core is red, blue, blue."},
    {"q": "What is an increasing pattern?",
     "a": "An increasing pattern gets bigger by the same amount each time, like 4, 7, 10, 13. The rule is “start at 4 and add 3 each time.”"},
    {"q": "How can I practise patterns with my child at home?",
     "a": "Make patterns with beads, blocks or claps, and count coins by 2s, 5s and 10s with toonies, nickels and dimes. Ask what comes next and how they know."},
]


def gen():
    rnd = random.Random(52807)
    P = People(rnd)
    sets = [set_repeating(), set_growing(), set_numbers(), set_missing(), set_real(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in allk, it["q"]
            allk.add(it["q"])
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "repeating-and-increasing-patterns",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Repeating and Increasing Patterns: Core, Shape Patterns and Number Patterns to 100",
        "seo_title": "Grade 2 Repeating and Increasing Patterns Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Repeating and increasing patterns",
        "domain": "Patterning",
        "standard_code": "Grade 2: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Repeating and increasing patterns",
        "meta_desc": "Free Grade 2 math worksheets on repeating and increasing patterns: find the core, extend increasing shape patterns, count by 2s, 5s and 10s to 100, fill in missing parts and make predictions. 100 questions with an answer key, matched to the BC curriculum.",
        "key_big": "Find what repeats or what changes each time.",
        "key_sub": "In a repeating pattern, find the core: the part that repeats. In an increasing pattern, find the jump and check it every time: 4, 7, 10 is “start at 4 and add 3 each time.”",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(repeating pattern|number track|number line|shape pattern|hundreds chart rows)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
