# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Patterns (Ontario Mathematics Curriculum 2020, C1.2-C1.4)
  python3 tools/gen_caon_math_g4_patterns.py
Repeating patterns (core, the nth element), growing and shrinking shape patterns with tables of
values and graphs, pattern rules for whole-number patterns to 10 000 (“start at 5 and add 3 each
time”), decimal tenth patterns (0.2, 0.4, 0.6), predictions, missing terms and real-life patterns in
Canadian settings.
Wrong answers come from real mistakes: using only the first step, mixing up the term (figure)
number and the value, one jump too many for a later term, multiplying the term number by the jump,
using the start as the jump, going the wrong way, changing the wrong digit, and writing 0.8 + 0.2
as 0.10. Every answer is computed and checked in code (Decimal for tenths). HTML attributes use
single quotes.
"""
import datetime, json, math, os, random, re
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d8cd"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NB = " "
COLOURS = {"red": "#d64535", "blue": "#3b7dd8", "yellow": "#f2c230", "green": "#4caf50"}
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ helpers
def f(n):
    """Ontario/SI style: 4 digits no separator, 5+ digits grouped with a no-break space."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return (MINUS if n < 0 else "") + s


def ds(x):
    """A decimal to tenths: 0.8, 1.0, 12.4."""
    return str(D(x).quantize(D("0.1")))


def lab(v):
    if v is None:
        return "?"
    if isinstance(v, str):
        return v
    if isinstance(v, D):
        return ds(v)
    return f(v)


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


def nums_mcq(q, ans, cands, e, fmt=f):
    ok = [v for v in cands if v != ans and 0 <= v <= 10000]
    assert 0 <= ans <= 10000
    assert len(ok) == 3 and len(set(ok)) == 3, (q, ans, cands)
    return mcq(q, fmt(ans), [fmt(v) for v in ok], e)


def dec_mcq(q, ans, cands, e, unit=""):
    """ans: Decimal. cands: strings, some written the wrong way on purpose (0.10). All values must differ."""
    vals = [D(ans)] + [D(c) for c in cands]
    assert len(set(vals)) == 4, (q, ans, cands)
    return mcq(q, ds(ans) + unit, [c + unit for c in cands], e)


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
    return ", ".join(lab(x) for x in xs)


def seq(start, step, n):
    return [start + step * k for k in range(n)]


def jump(d):
    return ("+" + lab(d)) if d > 0 else (MINUS + lab(-d))


def pm(d):
    return "+" if d > 0 else MINUS


def rule_text(start, d):
    if d > 0:
        return "Start at %s and add %s each time" % (lab(start), lab(d))
    return "Start at %s and subtract %s each time" % (lab(start), lab(-d))


def is_pattern(xs):
    d = xs[1] - xs[0]
    return d != 0 and all(xs[i + 1] - xs[i] == d for i in range(len(xs) - 1))


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def tw(s, fs):
    """Rough width of bold Arial text."""
    return sum(0.36 if ch in " .,:" + NB else (0.62 if ch.isdigit() else 0.68) for ch in s) * fs


# ------------------------------------------------------------ number track, number line, table of values, graph
def track_svg(vals):
    labels = [lab(v) for v in vals]
    cw = max(52, int(max(tw(t, 17) for t in labels) + 16))
    m, TH = 4, 36
    W, H = 2 * m + len(vals) * cw, 2 * m + TH
    s = []
    for i, t in enumerate(labels):
        x = m + i * cw
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, cw, TH, FILL if t == "?" else "#ffffff", GREEN))
        s.append(text(x + cw / 2, m + 24, t, 17, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number track")


def track(vals, hide=()):
    return fig(track_svg([None if k in hide else v for k, v in enumerate(vals)]))


def nline_svg(start, jumps, ticks=None):
    if ticks is None:
        ticks = [lab(start)] + [None] * (len(jumps) - 1) + ["?"]
    jl = [jump(j) for j in jumps]
    JW = 84
    m, ry, ly = 34, 22, 48
    W = 2 * m + JW * len(jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (JW if j > 0 else -JW))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 22, ly, W - m + 22, ly, INK)]
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
    return svg_wrap(W, H, "".join(s), "number line starting at %s with jumps of %s" % (
        lab(start), ", ".join(jl).replace(MINUS, "minus ")))


def tov_svg(top, bot, heads, label="table of values"):
    """Two-row table of values. '?' shows red."""
    top, bot = [lab(v) for v in top], [lab(v) for v in bot]
    CW = max(46, int(max(tw(t, 16) for t in top + bot) + 16))
    RH = 32
    LW = int(max(tw(h, 14) for h in heads) + 18)
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
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def graph_svg(vals, ystep, ylab, xmax=None, xlab="Figure number"):
    """Points (1, vals[0]), (2, vals[1]) ... on a grid. Every grid line is labelled."""
    xmax = xmax or len(vals)
    ymax = int(math.ceil(max(vals) / ystep)) * ystep
    if ymax == max(vals):
        ymax += ystep
    rows = ymax // ystep
    CW, RH = 40, 20
    L, T, R, B = 62, 10, 16, 50
    W, H = L + CW * xmax + R, T + RH * rows + B
    x0, y0 = L, T + RH * rows
    s = []
    for r in range(rows + 1):
        y = y0 - r * RH
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + CW * xmax, y, GRID))
        s.append(text(x0 - 6, y + 5, f(r * ystep), 14, anchor="end"))
    for c in range(1, xmax + 1):
        x = x0 + c * CW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, T, x, y0, GRID))
        s.append(text(x, y0 + 19, str(c), 14))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, T - 4, x0, y0, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + CW * xmax + 6, y0, INK))
    for i, v in enumerate(vals):
        s.append("<circle cx='%d' cy='%.1f' r='5.5' fill='%s'/>" % (x0 + (i + 1) * CW, y0 - v / ystep * RH, GREEN))
    s.append(text(x0 + CW * xmax / 2, H - 8, xlab, 14))
    yc = T + RH * rows / 2
    s.append("<text x='16' y='%.1f' font-size='14' font-weight='700' fill='%s' text-anchor='middle' "
             "transform='rotate(-90 16 %.1f)'>%s</text>" % (yc, INK, yc, ylab))
    return svg_wrap(W, H, "".join(s), "graph of a growing pattern")


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


def two_rows(k):
    n = 7 - k

    def draw(x, y):
        return "".join(tile(x + i * T, y + r * T) for r in range(2) for i in range(n))
    return n * T, 2 * T, draw


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
    "dec": (two_rows, lambda k: 14 - 2 * k, "tiles"),
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



# ============================================================ set 1: repeating patterns
AB = ["blue circle", "blue square"]
ABB = ["red circle", "blue circle", "blue circle"]
ABC = ["green triangle", "green circle", "green square"]
AABB = ["yellow star", "yellow star", "red star", "red star"]
ARR = ["arrow up", "arrow right", "arrow down", "arrow left"]
ABBC = ["red triangle", "blue circle", "blue circle", "yellow square"]
AABC = ["red star", "red star", "blue square", "yellow circle"]
WORDS = ["w:clap", "w:snap", "w:snap", "w:stomp"]


def next_rep(core, shown, mode, cands, extra=""):
    toks = rep(core, shown)
    a = rep(core, shown + 1)[-1]
    e = "The core is <b>%s</b>. The last one shown is the %s element of a core, so next comes <b>%s</b>.%s" % (
        names(core, mode), ordn(shown % len(core) or len(core)), name(a, mode), extra)
    return mcq(fig(row_svg(toks + ["?"])) + "The pattern repeats. What comes next?", name(a, mode), cands, e)


def nth_rep(core, shown, n, mode, cands, ask):
    a = rep(core, n)[-1]
    L = len(core)
    k = (n - 1) % L + 1
    pos = [p for p in range(1, n + 1) if (p - 1) % L == k - 1]
    assert all(rep(core, p)[-1] == a for p in pos)
    pl = ("the %s ones" % name(a, mode)) if mode == "colour" else name(a, mode) + "s"
    e = ("The core has %d elements. %d = %d × %d + %d, so the %s element is the %s element of a core: <b>%s</b>. "
         "Check: %s are at %s." % (L, n, L, (n - k) // L, k, ordn(n), ordn(k), name(a, mode), pl, lst(pos)))
    if k == L:
        e = ("The core has %d elements. %d = %d × %d, so the %s element is the last element of a core: <b>%s</b>. "
             "Check: %s are at %s." % (L, n, L, n // L, ordn(n), name(a, mode), pl, lst(pos)))
    return mcq(fig(row_svg(rep(core, shown))) + ask, name(a, mode), cands, e)


def set_repeating():
    q1 = next_rep(ABBC, 9, "both", ["red triangle", "yellow square", "blue square"],
                  " After a red triangle come two blue circles.")
    q2 = next_rep(ARR, 7, "shape", ["up", "right", "down"], " Each arrow makes a quarter turn clockwise.")

    def core_q(core, shown, mode, cands, extra):
        return mcq(fig(row_svg(rep(core, shown))) + "What is the core of this pattern?", names(core, mode), cands,
                   "The core is the shortest part that repeats from the start. Here it is <b>%s</b>, and then it starts again.%s"
                   % (names(core, mode), extra))

    q3 = core_q(AABC, 8, "shape", ["star, square, circle", "star, star, square", "star, star, square, circle, star"],
                " There are two stars in each core, not one.")
    q4 = mcq(track(rep([2, 5, 5, 8], 8)) + "What is the core of this number pattern?", "2, 5, 5, 8",
             ["2, 5", "2, 5, 5", "5, 5, 8"],
             "The numbers go 2, 5, 5, 8, then 2 again. The core is <b>2, 5, 5, 8</b>. “2, 5” is too short: after 5 comes another 5.")
    q5 = mcq(fig(row_svg(rep(ABBC, 8))) + "Which letters show the same pattern?", "A B B C A B B C",
             ["A B C A B C A B", "A B B A B B A B", "A A B C A A B C"],
             "Red triangle is A, blue circle is B and yellow square is C. The core is A, B, B, C, so the pattern is "
             "<b>A B B C A B B C</b>.")
    q6 = nums_mcq(fig(row_svg(rep(AABC, 12))) + "How many elements are in the core of this pattern?", 4, [3, 12, 2],
                  "The core is star, star, square, circle. That is <b>4</b> elements. 3 counts the different shapes, "
                  "but the star is in the core twice.")
    q7 = mcq("Which pattern has the same core structure as red, red, blue, red, red, blue?", "2, 2, 7, 2, 2, 7",
             ["2, 7, 7, 2, 7, 7", "2, 7, 2, 7, 2, 7", "2, 2, 7, 7, 2, 2"],
             "Red, red, blue is A, A, B. The numbers 2, 2, 7 are also A, A, B. So the answer is <b>2, 2, 7, 2, 2, 7</b>.")
    q8 = mcq("Which of these is NOT a repeating pattern?", "A B B A B A A B",
             ["A B B A B B A B B", "A B C D A B C D", "A A B A A B A A B"],
             "The others repeat the same core each time. <b>A B B A B A A B</b> has no part that repeats the same way.")
    q9 = mcq(fig(row_svg(rep(ARR, 5))) + "The pattern repeats. Which way does the 15th arrow point?", "down",
             ["up", "right", "left"],
             "The core is up, right, down, left (4 arrows). 15 = 4 × 3 + 3, so the 15th arrow is the 3rd arrow of a core: "
             "<b>down</b>. Check: down arrows are at 3, 7, 11, 15.")
    q10 = nth_rep(ABC, 6, 12, "shape", ["triangle", "circle", "star"],
                  "The pattern keeps repeating. What shape is the 12th shape?")
    q11 = nth_rep(ABB, 6, 20, "colour", ["red", "yellow", "green"],
                  "The pattern keeps repeating. What colour is the 20th circle?")
    q12 = nth_rep(ABC, 6, 25, "shape", ["circle", "square", "star"],
                  "The pattern keeps repeating. What shape is the 25th shape?")
    q13 = nth_rep(AABB, 8, 22, "colour", ["red", "blue", "green"],
                  "The pattern keeps repeating. What colour is the 22nd star?")
    q14 = nums_mcq(track(rep([4, 1, 6], 6) + [None]) + "The pattern repeats. What is the 10th number?", 4, [1, 6, 10],
                   "The core is 4, 1, 6. 10 = 3 × 3 + 1, so the 10th number is the 1st number of a core: <b>4</b>. "
                   "10 is the position, not the number in that position.")
    nb = rep(WORDS, 6)
    q15 = mcq(fig(row_svg(nb + ["?", "?"])) + "Owen makes a sound pattern. What are the next two sounds?", "snap, stomp",
              ["stomp, clap", "clap, snap", "snap, snap"],
              "The core is <b>clap, snap, snap, stomp</b>. The row ends with clap, snap. Next come <b>snap, stomp</b>. "
              "There are two snaps in each core.")
    bad = rep(ABBC, 12)
    bad[6] = "yellow square"
    assert rep(ABBC, 12)[6] == "blue circle"
    q16 = mcq(fig(row_svg(bad, numbered=True)) + "This pattern has one mistake. Which shape is wrong?", "shape 7",
              ["shape 8", "shape 4", "shape 9"],
              "The core is red triangle, blue circle, blue circle, yellow square. Yellow squares go at 4, 8 and 12. "
              "<b>Shape 7</b> should be a blue circle.")
    q17 = nums_mcq(fig(row_svg(rep(ABBC, 9))) + "The pattern keeps repeating. What is the position of the next yellow square?",
                   12, [10, 13, 8],
                   "Yellow squares are the 4th element of each core. They are at 4, 8, <b>12</b>. "
                   "8 is the last yellow square shown.")
    q18 = nums_mcq("A pattern has the core red, blue, blue, yellow. It has 20 shapes. How many blue shapes are there?",
                   10, [5, 20, 8],
                   "20 ÷ 4 = 5 cores. Each core has 2 blue shapes. 5 × 2 = <b>10</b>. 5 counts only 1 blue in each core.")
    q19 = nums_mcq("Hana makes a bracelet with 30 beads. The core is red, red, white. How many white beads are there?",
                   10, [20, 15, 3],
                   "30 ÷ 3 = 10 cores. Each core has 1 white bead, so there are <b>10</b> white beads. 20 is the number of red beads.")
    q20 = mcq("A pattern has the core A, B, C, D, E. What is the 23rd letter?", "C", ["D", "B", "E"],
              "The core has 5 letters. 23 = 5 × 4 + 3, so the 23rd letter is the 3rd letter of a core: <b>C</b>. "
              "Check: C is at 3, 8, 13, 18, 23.")
    out = [q1, q2, q4, q3, q5, q6, q7, q8, q15, q16, q14, q10, q9, q11, q17, q12, q13, q18, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Repeating patterns", "items": out}


# ============================================================ set 2: growing patterns, tables of values and graphs
def HEADS(nm):
    return ["Figure number", "Number of " + thing(nm)]


def set_growing():
    def d_of(nm):
        return cnt(nm, 2) - cnt(nm, 1)

    def next_q(nm, cands, extra=""):
        th = thing(nm)
        a, last, d = cnt(nm, 4), cnt(nm, 3), d_of(nm)
        e = "Count each figure: %s. Each figure has %d more %s. %d + %d = <b>%d</b> %s in Figure 4.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), d, th, last, d, a, th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure 4?" % th, a, cands, e)

    def table_q(nm, shown, k, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, j) for j in range(1, k + 1)]
        d = d_of(nm)
        e = "The number of %s goes %s by %d each time. Keep going: %s. Figure %d has <b>%d</b> %s.%s" % (
            th, "up" if d > 0 else "down", abs(d), lst(vals[shown - 1:]), k, vals[-1], th, extra)
        return nums_mcq(fig(tov_svg(list(range(1, shown + 1)), vals[:shown], HEADS(nm))) +
                        "This table of values shows a pattern. How many %s are in Figure %d?" % (th, k),
                        vals[-1], cands, e)

    def which_q(nm, n, picture=True, extra=""):
        th = thing(nm)
        vals = [cnt(nm, k) for k in range(1, 20)]
        k = vals.index(n) + 1
        e = "Keep going: %s. Figure <b>%d</b> has %d %s. %d is the number of %s, not the figure number.%s" % (
            lst(vals[:k]), k, n, th, n, th, extra)
        pic = fig(pattern_svg(nm)) if picture else fig(tov_svg([1, 2, 3, 4], vals[:4], HEADS(nm)))
        return mcq(pic + "The pattern keeps going. Which figure has %d %s?" % (n, th),
                   "Figure %d" % k, ["Figure %d" % n, "Figure %d" % (k + 1), "Figure %d" % (k - 1)], e)

    q1 = next_q("sq", [16, 12, 11], " 16 counts 4 sticks for every square, but squares next to each other share a stick.")
    q2 = next_q("tables", [16, 12, 9], " 16 counts 4 chairs for every table, but no chairs fit where tables touch.")
    q3 = table_q("towers", 4, 7, [21, 27, 42], " 42 is 7 × 6, but only Figure 1 has 6 cubes.")
    q4 = table_q("sq", 4, 8, [28, 32, 22], " 28 is one jump too many. 32 is 8 × 4.")
    q5 = table_q("dec", 4, 5, [2, 5, 8], " This pattern is shrinking.")
    q6 = which_q("tables", 14)
    q7 = mcq(fig(tov_svg([1, 2, 3, 4, 5], [cnt("sq", k) for k in range(1, 6)], HEADS("sq"))) +
             "In this table, 16 is under 5. What does that mean?", "Figure 5 has 16 sticks",
             ["Figure 16 has 5 sticks", "Each figure adds 16 sticks", "Each figure adds 5 sticks"],
             "Read down the column: the figure number is on top and the number of sticks is below. "
             "So <b>Figure 5 has 16 sticks</b>.")
    tv = [cnt("tables", k) for k in range(1, 5)]
    q8 = nums_mcq(fig(graph_svg(tv, 2, "Chairs", xmax=5)) + "The graph shows the chairs in each figure of a pattern. "
                  "The pattern keeps going. How many chairs are in Figure 5?", 12, [11, 10, 14],
                  "Read the points: %s. Each point is 2 higher. 10 + 2 = <b>12</b> chairs. 10 is Figure 4." % lst(tv))
    cv = [cnt("towers", k) for k in range(1, 5)]
    q9 = mcq(fig(graph_svg(cv, 3, "Cubes")) + "The graph shows a growing pattern. What does the point above 3 show?",
             "Figure 3 has 12 cubes", ["Figure 12 has 3 cubes", "Figure 3 has 3 cubes", "Each figure adds 12 cubes"],
             "The figure number is along the bottom. The number of cubes is up the side. The point above 3 is at 12, so "
             "<b>Figure 3 has 12 cubes</b>.")
    dv = [cnt("dots", k) for k in range(1, 5)]
    q10 = nums_mcq(fig(graph_svg(dv, 5, "Dots")) + "The graph shows a growing pattern. How much does each point go up?",
                   5, [1, 10, 20],
                   "The points are at %s. Each one is <b>5</b> more. 1 counts one grid line, but each grid line is worth 5. 20 is the value of Figure 4." % lst(dv))
    lv = [cnt("L", k) for k in range(1, 5)]
    q11 = mcq(fig(graph_svg(lv, 1, "Tiles", xmax=6)) + "The pattern keeps going. Which figure has 9 tiles?", "Figure 5",
              ["Figure 9", "Figure 4", "Figure 6"],
              "The points go 1, 3, 5, 7. Each is 2 more, so the next point is 9. That is <b>Figure 5</b>. "
              "9 is the number of tiles, not the figure number.")
    tri = [cnt("tri", k) for k in range(1, 6)]
    q12 = nums_mcq(fig(tov_svg([1, 2, 3, 4, 5], [v if i != 3 else "?" for i, v in enumerate(tri)], HEADS("tri"))) +
                   "What number is missing from the table of values?", tri[3], [8, 10, 4],
                   "The number of sticks goes up by 2 each time: %s. The missing number is <b>%d</b>. "
                   "4 is the figure number, not the number of sticks." % (lst(tri), tri[3]))
    q13 = nums_mcq(fig(tov_svg([1, 2, "?", 4, 5], [cnt("tables", k) for k in range(1, 6)], HEADS("tables"))) +
                   "What figure number is missing from the table?", 3, [8, 6, 10],
                   "The figure numbers count 1, 2, 3, 4, 5. The missing figure number is <b>3</b>. "
                   "8 is the number of chairs in Figure 3.")
    q14 = mcq(fig(pattern_svg("towers")) + "What is the pattern rule for the number of cubes?",
              "Start at 6 and add 3 each time",
              ["Start at 3 and add 3 each time", "Start at 6 and add 6 each time", "Start at 3 and add 6 each time"],
              "Count: 6, 9, 12. Figure 1 has 6 cubes and each figure adds a tower of 3. "
              "The rule is <b>start at 6 and add 3 each time</b>. 6 is the start, not the jump.")
    q15 = mcq(fig(tov_svg([1, 2, 3, 4], tri[:4], HEADS("tri"))) + "What is the pattern rule for the number of sticks?",
              "Start at 3 and add 2 each time",
              ["Start at 3 and add 3 each time", "Start at 2 and add 3 each time", "Start at 1 and add 2 each time"],
              "The bottom row starts at 3. 3 + 2 = 5, 5 + 2 = 7, 7 + 2 = 9. The rule is <b>start at 3 and add 2 each time</b>.")
    q16 = mcq("Which table of values follows the rule “Start at 6 and add 4 each time”?",
              "6, 10, 14, 18", ["4, 10, 16, 22", "10, 14, 18, 22", "6, 24, 96, 384"],
              "Figure 1 has 6. Then add 4: 6, 10, 14, 18. The answer is <b>6, 10, 14, 18</b>. "
              "10, 14, 18, 22 adds 4 before the first figure.")
    st = [cnt("stairs", k) for k in range(1, 6)]
    q17 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 5?", st[4],
                   [14, 9, 25],
                   "Count: 1, 3, 6. The jumps are +2, then +3, so the next jumps are +4 and +5: 1, 3, 6, 10, <b>15</b>. "
                   "9 uses only the first step (+2) each time.")
    q18 = nums_mcq(fig(tov_svg([1, 2, 3, 4], tv, HEADS("tables"))) + "The pattern keeps going. How many chairs are in Figure 10?",
                   22, [40, 24, 20],
                   "Start at 4 and add 2 each time. From Figure 1 to Figure 10 there are 9 jumps: 9 × 2 = 18. "
                   "4 + 18 = <b>22</b>. 40 is 10 × 4, but only Figure 1 has 4 chairs.")
    q19 = nums_mcq(fig(pattern_svg("dots")) + "The pattern keeps going. How many dots are in Figure 12?", 60, [55, 65, 17],
                   "Each figure is a row of 5 more dots. Figure 12 has 12 rows: 12 × 5 = <b>60</b>. 55 is Figure 11.")
    q20 = which_q("sq", 31, picture=False)
    assert cnt("sq", 10) == 31 and cnt("tables", 10) == 22 and cnt("dots", 12) == 60 and cnt("tables", 6) == 14
    out = [q1, q2, q7, q3, q12, q13, q4, q5, q9, q10, q8, q14, q15, q6, q11, q16, q17, q18, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Growing patterns, tables of values and graphs", "items": out}


# ============================================================ set 3: pattern rules for number patterns to 10 000
def set_rules():
    def nxt(nums, cands, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = nums[-1] + d
        e = "Each number is %s %s. %s %s %s = <b>%s</b>.%s" % (
            f(abs(d)), "more" if d > 0 else "less", f(nums[-1]), pm(d), f(abs(d)), f(a), extra)
        return nums_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)

    def rq(nums, wrong, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        e = "%s %s %s = %s, and every jump is the same. The rule is <b>%s</b>.%s" % (
            f(nums[0]), pm(d), f(abs(d)), f(nums[1]), rule_text(nums[0], d).lower(), extra)
        return mcq(track(nums) + "What is the pattern rule?", rule_text(nums[0], d),
                   [rule_text(s, k) for s, k in wrong], e)

    q1 = rq([5, 8, 11, 14], [(5, 5), (3, 3), (8, 3)], " 5 is where the pattern starts. It is not the jump.")
    q2 = mcq("Which pattern follows the rule “Start at 5 and add 3 each time”?", "5, 8, 11, 14",
             ["3, 8, 13, 18", "8, 11, 14, 17", "5, 10, 15, 20"],
             "The first number is 5. Then add 3: 5 + 3 = 8, 8 + 3 = 11, 11 + 3 = 14. The answer is <b>5, 8, 11, 14</b>. "
             "8, 11, 14, 17 adds 3 before the first number.")
    q3 = nxt([3460, 3470, 3480, 3490], [3491, 4490, 3590], " 349 tens + 1 ten = 350 tens, so the answer is 3500.")
    q4 = nxt([1250, 1500, 1750], [1850, 1775, 2250], " Counting by 250s, the numbers end in 000, 250, 500 or 750.")
    q5 = nxt([8000, 7500, 7000], [6000, 7500, 6900], " The numbers get smaller, so keep subtracting 500.")
    q6 = rq([9400, 9300, 9200, 9100], [(9400, 100), (9400, -1000), (9400, -10)],
            " The numbers get smaller, so the rule subtracts. Only the hundreds digit changes.")
    q7 = rq([2025, 2050, 2075, 2100], [(2025, 2025), (25, 25), (2025, -25)], " 2025 is the start, not the jump.")
    q8 = nxt([4985, 4990, 4995], [4996, 5995, 5005], " 4996 adds only 1. 5995 changes the thousands digit.")
    q9 = nums_mcq(fig(nline_svg(2600, [200] * 4)) + "Start at 2600. Make the jumps. Where do you land?", 3400,
                  [3200, 3600, 2800],
                  "Count on by 200s 4 times: 2800, 3000, 3200, <b>3400</b>. 3200 makes only 3 jumps.")
    q10 = nums_mcq(fig(nline_svg(5000, [-250] * 3)) + "Start at 5000. Make the jumps. Where do you land?", 4250,
                   [5750, 4500, 4000],
                   "Count back by 250s 3 times: 4750, 4500, <b>4250</b>. 5750 goes the wrong way.")
    q11 = nums_mcq("The rule is “Start at 150 and subtract 15 each time.” What is the 4th number?", 105, [90, 195, 120],
                   "150, 135, 120, <b>105</b>. From the 1st number to the 4th there are only 3 jumps, so 90 is one jump too many.")
    q12 = nums_mcq("The rule is “Start at 1000 and add 1000 each time.” What is the 5th number?", 5000, [6000, 4000, 1005],
                   "1000, 2000, 3000, 4000, <b>5000</b>. 1005 adds 5 ones, not thousands.")
    q13 = nums_mcq("The rule is “Start at 2 and add 5 each time.” Which number will be in the pattern?", 1007,
                   [1005, 1010, 1003],
                   "The pattern goes 2, 7, 12, 17, 22 … Every number ends in 2 or 7. Only <b>1007</b> ends in 7.")
    assert (1007 - 2) % 5 == 0 and all((v - 2) % 5 for v in (1005, 1010, 1003))
    q14 = rq([6000, 5750, 5500, 5250], [(6000, 250), (6000, -25), (5250, 250)],
             " The numbers get smaller, so the rule subtracts.")
    q15 = nums_mcq(track([3, 4, 6, 9, 13, None]) + "What number comes next?", 18, [14, 17, 26],
                   "The jumps are +1, +2, +3, +4. Each jump is 1 more, so the next jump is +5. 13 + 5 = <b>18</b>. "
                   "14 uses only the first step (+1).")
    q16 = nums_mcq(track([2, 4, 8, 16, None]) + "Each number is double the one before. What number comes next?", 32,
                   [18, 24, 20],
                   "Double each time: 2 × 2 = 4, 4 × 2 = 8, 8 × 2 = 16, 16 × 2 = <b>32</b>. "
                   "18 uses only the first step (+2).")
    q17 = mcq(track([5, 8, 12, 15]) + "Ethan says the rule is “start at 5 and add 3 each time.” Is he right?",
              "No, 8 + 3 is 11, not 12",
              ["Yes, 5 + 3 = 8", "Yes, 12 + 3 = 15", "No, the rule is add 5"],
              "Check every jump, not just the first one: 5 + 3 = 8, but 8 + 3 = 11. "
              "So <b>he is not right</b>: 5, 8, 12, 15 does not follow one rule.")
    q18 = nums_mcq(track([1200, 1450, 1700, 1850, 2200]) + "One number in this pattern is wrong. Which one?", 1850,
                   [1450, 1700, 2200],
                   "The rule is +250: 1200, 1450, 1700, 1950, 2200. <b>1850</b> should be 1950.")
    q19 = nums_mcq("The rule is “Start at 3750 and add 50 each time.” Which number comes after 3950?", 4000,
                   [3955, 4050, 3960],
                   "3950 + 50 = <b>4000</b>. 395 tens + 5 tens = 400 tens. 4050 adds 100.")
    a6 = 10 + 4 * 5
    b6 = 30 + 2 * 5
    q20 = mcq("Pattern A: start at 10 and add 4 each time. Pattern B: start at 30 and add 2 each time. "
              "What are the 6th numbers of the two patterns?", "A: %d, B: %d" % (a6, b6),
              ["A: 34, B: 42", "A: 24, B: 12", "A: 30, B: 30"],
              "From the 1st number to the 6th there are 5 jumps. A: 10 + 5 × 4 = <b>30</b>. B: 30 + 5 × 2 = <b>40</b>. "
              "34 and 42 make 6 jumps, one too many.")
    assert (a6, b6) == (30, 40) and 10 + 6 * 4 == 34 and 30 + 6 * 2 == 42
    out = [q2, q1, q3, q5, q4, q8, q9, q10, q6, q7, q14, q11, q12, q19, q13, q18, q17, q15, q16, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Pattern rules for number patterns to 10 000", "items": out}


# ============================================================ set 4: decimal tenth patterns
def set_decimals():
    def dnxt(nums, cands, extra=""):
        nums = [D(x) for x in nums]
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = nums[-1] + d
        e = "Each number is %s %s. %s %s %s = <b>%s</b>.%s" % (
            ds(abs(d)), "more" if d > 0 else "less", ds(nums[-1]), pm(d), ds(abs(d)), ds(a), extra)
        return dec_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)

    q1 = dnxt(["0.4", "0.6", "0.8"], ["0.10", "0.9", "1.2"],
              " 8 tenths + 2 tenths = 10 tenths = 1 whole. 0.10 is only 1 tenth.")
    q2 = dnxt(["0.1", "0.2", "0.3", "0.4"], ["0.6", "1.4", "0.41"], " Count on by tenths. 0.41 adds 1 hundredth, not 1 tenth.")
    q3 = dnxt(["2.5", "3.0", "3.5"], ["3.6", "4.5", "5.0"], " Add 5 tenths, not 1 tenth and not 1 whole.")
    q4 = dnxt(["1.7", "1.8", "1.9"], ["1.10", "2.9", "1.20"],
              " 19 tenths + 1 tenth = 20 tenths = 2.0. 1.10 is less than 1.9.")
    q5 = dnxt(["3.6", "3.3", "3.0"], ["2.9", "3.9", "2.0"], " The numbers get smaller by 3 tenths.")
    q6 = dnxt(["4.6", "4.7", "4.8", "4.9"], ["4.10", "5.9", "4.0"], " After 4.9 comes 5.0, not 4.10.")
    vals = [D("0.2"), D("0.4"), D("0.6")]
    q7 = dec_mcq(fig(tenths_svg([2, 4, 6, None])) + "Each bar has 10 equal parts. What decimal comes next?",
                 D("0.8"), ["0.7", "8.0", "0.08"],
                 "The bars show 0.2, 0.4, 0.6. Each bar has 2 more tenths shaded. 0.6 + 0.2 = <b>0.8</b>. "
                 "8 tenths is 0.8, not 8.0.")
    assert vals[-1] + D("0.2") == D("0.8")
    q8 = mcq(track([D("0.5"), D("0.8"), D("1.1"), D("1.4")]) + "What is the pattern rule?", "Start at 0.5 and add 0.3 each time",
             ["Start at 0.5 and add 3 each time", "Start at 0.5 and add 0.5 each time", "Start at 0.3 and add 0.3 each time"],
             "0.5 + 0.3 = 0.8, 0.8 + 0.3 = 1.1, 1.1 + 0.3 = 1.4. The rule is <b>start at 0.5 and add 0.3 each time</b>. "
             "Add 3 tenths, not 3 wholes.")
    q9 = mcq(track([D("7.0"), D("6.5"), D("6.0"), D("5.5")]) + "What is the pattern rule?",
             "Start at 7.0 and subtract 0.5 each time",
             ["Start at 7.0 and add 0.5 each time", "Start at 7.0 and subtract 5 each time",
              "Start at 7.0 and subtract 0.1 each time"],
             "7.0 − 0.5 = 6.5, 6.5 − 0.5 = 6.0. The numbers get smaller, so the rule is "
             "<b>start at 7.0 and subtract 0.5 each time</b>.")
    q10 = mcq("Which pattern follows the rule “Start at 0.6 and add 0.2 each time”?", "0.6, 0.8, 1.0, 1.2",
              ["0.6, 0.8, 0.10, 0.12", "0.6, 2.6, 4.6, 6.6", "0.2, 0.8, 1.4, 2.0"],
              "0.6 + 0.2 = 0.8, 0.8 + 0.2 = 1.0, 1.0 + 0.2 = 1.2. The answer is <b>0.6, 0.8, 1.0, 1.2</b>. "
              "0.10 is not 0.8 + 0.2: 8 tenths + 2 tenths = 10 tenths = 1.0.")
    m = [D("1.2"), D("1.6"), D("2.0"), D("2.4")]
    assert is_pattern(m)
    q11 = dec_mcq(track(m, (2,)) + "What number is missing?", m[2], ["1.10", "1.8", "2.2"],
                  "The rule is +0.4. 1.6 + 0.4 = <b>2.0</b>. Check: 2.0 + 0.4 = 2.4. "
                  "16 tenths + 4 tenths = 20 tenths, so 1.10 is not right.")
    q12 = dec_mcq(fig(nline_svg(D("0.3"), [D("0.2")] * 3)) + "Start at 0.3. Make the jumps. Where do you land?", D("0.9"),
                  ["0.6", "1.1", "0.8"],
                  "Count on by 0.2 three times: 0.5, 0.7, <b>0.9</b>. 1.1 makes one jump too many.")
    q13 = dec_mcq(fig(nline_svg(D("2.0"), [D("-0.4")] * 3)) + "Start at 2.0. Make the jumps. Where do you land?", D("0.8"),
                  ["1.2", "3.2", "0.4"],
                  "Count back by 0.4 three times: 1.6, 1.2, <b>0.8</b>. 3.2 goes the wrong way.")
    q14 = dec_mcq(fig(tov_svg([1, 2, 3, 4], [D("1.5"), D("2.0"), D("2.5"), D("3.0")], ["Day", "Length (m)"])) +
                  "A vine grows the same length each day. The table shows its length. How long is it on day 6?",
                  D("4.0"), ["3.5", "6.0", "4.5"],
                  "The length goes up by 0.5 m each day: 1.5, 2.0, 2.5, 3.0, 3.5, <b>4.0 m</b>. 3.5 m is day 5. "
                  "6.0 is the day number, not the length.", unit=" m")
    q15 = dec_mcq("The rule is “Start at 0.3 and add 0.3 each time.” What is the 6th number?", D("1.8"),
                  ["2.1", "1.5", "0.18"],
                  "0.3, 0.6, 0.9, 1.2, 1.5, <b>1.8</b>. 6 × 3 tenths = 18 tenths = 1.8, not 0.18. "
                  "2.1 makes one jump too many.")
    q16 = mcq(track([D("0.4"), D("0.8"), D("1.2")]) + "The pattern keeps going. Which number will be in the pattern?",
              "2.0", ["1.8", "1.4", "2.2"],
              "Keep adding 0.4: 1.6, <b>2.0</b>, 2.4. 1.4, 1.8 and 2.2 are skipped.")
    p = [D("0.9"), D("1.2"), D("1.5"), D("1.8"), D("2.1")]
    assert is_pattern(p)
    q17 = mcq(track(p, (1, 3)) + "Which two numbers are missing, in order?", "1.2, 1.8",
              ["1.1, 1.7", "0.12, 0.18", "1.3, 1.9"],
              "From 0.9 to 1.5 is 6 tenths in 2 equal jumps, so each jump is 0.3. "
              "0.9 + 0.3 = <b>1.2</b> and 1.5 + 0.3 = <b>1.8</b>.")
    q18 = mcq(track(["2.2", "2.4", "2.6", "2.8", "2.10"]) + "The rule is add 0.2. Which number is a mistake?", "2.10",
              ["2.4", "2.6", "2.8"],
              "2.8 + 0.2 = 3.0 (28 tenths + 2 tenths = 30 tenths). So <b>2.10</b> is the mistake. "
              "It should be 3.0.")
    q19 = mcq(track([D("5.7"), D("5.8"), D("5.9"), None, None]) + "What are the next two numbers?", "6.0, 6.1",
              ["5.10, 5.11", "6.0, 7.0", "5.10, 6.0"],
              "Count on by tenths: 5.9 + 0.1 = 6.0, then 6.1. The answer is <b>6.0, 6.1</b>.")
    q20 = mcq(fig(tov_svg([1, 2, 3, 4], [D("0.3"), D("0.6"), D("0.9"), D("1.2")], ["Term number", "Value"])) +
              "The pattern keeps going. Which term has the value 2.4?", "term 8",
              ["term 24", "term 7", "term 9"],
              "Keep adding 0.3: 1.5, 1.8, 2.1, 2.4. Those are terms 5, 6, 7 and <b>8</b>. "
              "2.4 is the value, not the term number.")
    assert D("0.3") * 8 == D("2.4") and D("0.3") * 6 == D("1.8")
    out = [q2, q1, q7, q3, q4, q6, q5, q12, q8, q9, q10, q11, q13, q16, q19, q18, q15, q17, q14, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Decimal patterns with tenths", "items": out}


def tenths_svg(counts):
    """Bars of 10 parts with some parts shaded. None = a dashed ? box."""
    PW, PH, gap, m = 13, 22, 18, 4
    BW = PW * 10
    W = 2 * m + len(counts) * BW + (len(counts) - 1) * gap
    H = 2 * m + PH + 22
    s = []
    for i, c in enumerate(counts):
        x0 = m + i * (BW + gap)
        if c is None:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
                     "stroke-dasharray='4 3'/>" % (x0 + 30, m, BW - 60, PH, FILL, GREEN))
            s.append(text(x0 + BW / 2, m + PH - 4, "?", 20, col=RED))
            continue
        for k in range(10):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                     % (x0 + k * PW, m, PW, PH, CUBE if k < c else "#ffffff", GREEN))
        s.append(text(x0 + BW / 2, m + PH + 19, "0." + str(c), 15))
    return svg_wrap(W, H, "".join(s), "tenths bars")


# ============================================================ set 5: predictions, missing terms and word problems
def set_predict(P):
    def story(t, ans, cands, e, pic="", unit=None):
        d = P.next()
        return nums_mcq(pic + t.format(**d), ans, cands, e.format(**d), unit or f)

    q1 = nums_mcq(track([5, 8, 11, 14]) + "The rule is “start at 5 and add 3 each time.” What is the 10th number?",
                  32, [35, 30, 29],
                  "From the 1st to the 10th number there are 9 jumps. 9 × 3 = 27. 5 + 27 = <b>32</b>. "
                  "35 makes 10 jumps. 30 is 10 × 3, but the pattern starts at 5.")
    sv = [cnt("sq", k) for k in range(1, 5)]
    q2 = nums_mcq(fig(tov_svg([1, 2, 3, 4], sv, HEADS("sq"))) + "The pattern keeps going. How many sticks are in Figure 20?",
                  61, [64, 60, 80],
                  "Start at 4 and add 3 each time. From Figure 1 to Figure 20 there are 19 jumps: 19 × 3 = 57. "
                  "4 + 57 = <b>61</b>. 80 is 20 × 4, but only Figure 1 has 4 sticks.")
    assert seq(4, 3, 20)[19] == 61 and seq(5, 3, 10)[9] == 32
    q3 = nums_mcq(track([2300, None, 2700, 2900]) + "What number is missing?", 2500, [2400, 2600, 2350],
                  "From 2700 to 2900 is +200. 2300 + 200 = <b>2500</b>. Check: 2500 + 200 = 2700. "
                  "2400 adds only 100.")
    q4 = nums_mcq(track([None, 1475, 1500, 1525]) + "What number is missing?", 1450, [1550, 1400, 1465],
                  "The rule is +25. Go back one step from 1475: 1475 − 25 = <b>1450</b>. 1550 goes the wrong way.")
    q5 = story("A Grade 4 class collects money for the Terry Fox Run. They have $120 after week 1. "
               "They collect $45 more each week. How much do they have after week 6?",
               345, [390, 270, 300],
               "From week 1 to week 6 there are 5 jumps. 5 × $45 = $225. $120 + $225 = <b>$345</b>. "
               "$390 makes 6 jumps, one too many.", unit=lambda v: "$%d" % v)
    q6 = story("The school library has 2450 books. It gets 150 new books each month. "
               "After how many months will it have 3200 books?",
               5, [750, 6, 4],
               "Count by 150s from 2450: 2600, 2750, 2900, 3050, 3200. That is <b>5</b> months. "
               "750 is the number of new books, not the number of months.",
               unit=lambda v: "%s month%s" % (f(v), "" if v == 1 else "s"))
    q7 = story("A sugar shack needs 40 L of maple sap to make 1 L of maple syrup, 80 L for 2 L and 120 L for 3 L. "
               "How much syrup can it make from 360 L of sap?",
               9, [8, 10, 36],
               "The sap goes up by 40 L for each litre of syrup: 40, 80, 120 … 320, 360. 360 L of sap makes "
               "<b>9 L</b> of syrup. 36 L divides by 10, not 40.", unit=lambda v: "%d L" % v)
    assert 360 // 40 == 9
    q8 = mcq("{n} runs 1.5 km on day 1. {He} adds 0.5 km each day. How far does {he} run on day 6?".format(**P.next()),
             "4.0 km", ["4.5 km", "3.0 km", "3.5 km"],
             "Add 0.5 km each day: 1.5, 2.0, 2.5, 3.0, 3.5, <b>4.0 km</b>. 3.5 km is day 5. "
             "3.0 km is 6 × 0.5, but the pattern starts at 1.5.")
    assert D("1.5") + 5 * D("0.5") == D("4.0")
    q9 = story("After a snowstorm, the snow is 12 cm deep on day 1, 15 cm on day 2 and 18 cm on day 3. "
               "The pattern continues. How deep is the snow on day 8?",
               33, [36, 24, 30],
               "Start at 12 and add 3 each day. From day 1 to day 8 there are 7 jumps: 7 × 3 = 21. "
               "12 + 21 = <b>33 cm</b>. 24 is 8 × 3, but the snow started at 12 cm.", unit=lambda v: "%d cm" % v)
    q10 = story("The gym floor has a row of 40 tiles in the pattern blue, blue, white, blue, blue, white … "
                "How many white tiles are in the row?",
                13, [14, 27, 20],
                "White tiles are at 3, 6, 9 … 39. 39 = 3 × 13, so there are <b>13</b> white tiles. Tile 40 is blue. "
                "27 is the number of blue tiles. 14 counts one white tile too many.")
    assert len([k for k in range(1, 41) if k % 3 == 0]) == 13
    assert datetime.date(2026, 7, 1).weekday() == 2 and datetime.date(2026, 7, 25).weekday() == 5
    q11 = mcq("Canada Day, July 1, 2026, is a Wednesday. The days of the week repeat every 7 days. "
              "What day of the week is July 25, 2026?", "Saturday", ["Friday", "Sunday", "Wednesday"],
              "July 25 is 24 days after July 1. 24 = 7 × 3 + 3. Three weeks later is Wednesday again, then 3 more days: "
              "Thursday, Friday, <b>Saturday</b>.")
    q12 = mcq("A city bus leaves the stop every 15 minutes. The first bus leaves at 7:05 a.m. "
              "When does the 5th bus leave?", "8:05 a.m.", ["8:20 a.m.", "7:50 a.m.", "8:00 a.m."],
              "Add 15 minutes each time: 7:05, 7:20, 7:35, 7:50, <b>8:05 a.m.</b> From the 1st bus to the 5th there are "
              "4 jumps. 8:20 a.m. makes 5 jumps.")
    q13 = story("An ice rink tank holds 5000 L of water. It drains 250 L each minute. "
                "How much water is left after 8 minutes?",
                3000, [2750, 7000, 4750],
                "Subtract 250 L each minute. 8 × 250 = 2000. 5000 − 2000 = <b>3000 L</b>. "
                "7000 goes the wrong way. 4750 subtracts only once.", unit=lambda v: "%s L" % f(v))
    q14 = story("Tables are pushed together in a row. 1 table seats 4 people, 2 tables seat 6 and 3 tables seat 8. "
                "How many people can sit at 10 tables?",
                22, [40, 20, 24],
                "Start at 4 and add 2 for each table. From 1 table to 10 tables there are 9 jumps: 9 × 2 = 18. "
                "4 + 18 = <b>22</b>. 40 counts 4 people at every table.")
    q15 = mcq("{n} saves $15 in week 1 and $15 more each week. In which week will {he} have $180?".format(**P.next()),
              "week 12", ["week 180", "week 11", "week 13"],
              "Count by 15s: 15, 30, 45 … 165, 180. $180 ÷ $15 = 12. It is <b>week 12</b>. "
              "180 is the amount of money, not the week number.")
    assert 15 * 12 == 180
    d = P.next()
    q16 = mcq("{n} counts by 25s from 0. {He} predicts that {he} will say 1450. Is {he} right?".format(**d),
              "Yes, 1450 ends in 50",
              ["No, 1450 is too big", "No, 1450 ends in 0", "Yes, every number ends in 5"],
              "Counting by 25s from 0, every number ends in 00, 25, 50 or 75. 1450 ends in 50, so "
              "<b>{he} is right</b>: 1400, 1425, 1450.".format(**d))
    assert 1450 % 25 == 0
    q17 = mcq("{n} skates laps at the rink: 0.6 km on Monday, 0.9 km on Tuesday, ? on Wednesday, 1.5 km on Thursday. "
              "How far does {he} skate on Wednesday?".format(**P.next()),
              "1.2 km", ["1.1 km", "0.12 km", "1.3 km"],
              "The rule is add 0.3 km. 0.9 + 0.3 = <b>1.2 km</b>. Check: 1.2 + 0.3 = 1.5. "
              "9 tenths + 3 tenths = 12 tenths = 1.2, not 0.12.")
    q18 = story("A sunflower is 0.8 m tall. It grows 0.2 m each week. After how many weeks will it be 2.0 m tall?",
                6, [10, 5, 7],
                "Add 0.2 m each week: 1.0, 1.2, 1.4, 1.6, 1.8, 2.0. That is <b>6</b> weeks. "
                "10 is 2.0 ÷ 0.2, but the sunflower started at 0.8 m.",
                unit=lambda v: "%d weeks" % v)
    assert D("0.8") + 6 * D("0.2") == D("2.0")
    q19 = story("On a canoe trip, the table shows how far {n}’s family paddles. How far do they paddle in 7 hours?",
                42, [36, 48, 13],
                "Each hour adds 6 km: 6, 12, 18, 24, 30, 36, <b>42 km</b>. 13 adds 7 to 6 instead of 7 jumps of 6.",
                fig(tov_svg([1, 2, 3], [6, 12, 18], ["Hours", "Distance (km)"])), unit=lambda v: "%d km" % v)
    q20 = mcq("{n} builds a tile pattern. Figure 1 has 6 tiles. Each figure has 4 more tiles than the one before. "
              "Which figure has 50 tiles?".format(**P.next()),
              "Figure 12", ["Figure 50", "Figure 11", "Figure 13"],
              "50 − 6 = 44 more tiles. 44 ÷ 4 = 11 jumps. Figure 1 + 11 jumps = <b>Figure 12</b>. "
              "Check: 6 + 11 × 4 = 50.")
    assert 6 + 11 * 4 == 50
    out = [q1, q3, q4, q2, q8, q5, q9, q14, q12, q10, q11, q7, q6, q13, q15, q16, q17, q18, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Predictions, missing terms and word problems", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Repeating patterns</h2>"
        "<p>A <b>repeating pattern</b> has a <b>core</b>: the shortest part that repeats from the start. "
        "To find a later element, divide its position by the number of elements in the core.</p>"
        "<figure class='sn-fig'>" + row_svg(rep(ABBC, 8)) +
        "<figcaption>The core is red triangle, blue circle, blue circle, yellow square (4 elements). "
        "The 15th shape: 15 = 4 × 3 + 3, so it is the 3rd shape of a core, a blue circle.</figcaption></figure>"
        "<h2>Growing patterns, tables of values and graphs</h2>"
        "<p>Count each figure. Put the figure number (term number) in the top row and the count (value) below it. "
        "A graph shows the same pairs as points.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>Figure 1 has 4 sticks, Figure 2 has 7, Figure 3 has 10.</figcaption></figure>"
        + table(["Figure number", "1", "2", "3", "4"], [["Number of sticks", "4", "7", "10", "13"]]) +
        "<p>The <b>pattern rule</b> tells where to start and what to do each time: "
        "<b>start at 4 and add 3 each time</b>.</p>"
        "<figure class='sn-fig'>" + graph_svg([4, 6, 8, 10], 2, "Chairs", xmax=5) +
        "<figcaption>Tables in a row: Figure 1 has 4 chairs, and each figure adds 2. Each point is 2 higher.</figcaption></figure>"
        "<h2>Number patterns to 10 000 and decimal tenths</h2>"
        "<p>Find the jump between two numbers next to each other. Check that the same jump works every time.</p>"
        "<figure class='sn-fig'>" + nline_svg(D("0.2"), [D("0.2")] * 3, ticks=["0.2", "0.4", "0.6", "0.8"]) +
        "<figcaption>0.2, 0.4, 0.6, 0.8. The rule is start at 0.2 and add 0.2 each time. "
        "Next comes 1.0, because 10 tenths = 1 whole.</figcaption></figure>"
        + ex("Missing number", "1.2, 1.6, ☐, 2.4",
             "The rule is add 0.4. 1.6 + 0.4 = 2.0. Check: 2.0 + 0.4 = 2.4.", "2.0")
        + ex("Predict the 10th number", "Start at 5 and add 3 each time. What is the 10th number?",
             "From the 1st number to the 10th there are 9 jumps. 9 × 3 = 27. 5 + 27 = 32.", "32")
        + ex("Which figure?", "Figure 1 has 6 tiles. Each figure adds 4 tiles. Which figure has 50 tiles?",
             "50 − 6 = 44. 44 ÷ 4 = 11 jumps. 1 + 11 = 12.", "Figure 12") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using only the first step: 3, 4, 6, 9 is “add 1”", "Check every jump: +1, +2, +3, so the next jump is +4"],
            ["Mixing up the term number and the value", "The figure (term) number is on top. The value is below it"],
            ["Using the start as the jump: 5, 8, 11 is “add 5”", "Start at 5 and add 3 each time"],
            ["10 jumps for the 10th number", "From the 1st to the 10th number there are 9 jumps"],
            ["Writing 0.8 + 0.2 as 0.10", "8 tenths + 2 tenths = 10 tenths = 1.0"],
        ])
    )


FAQ = [
    {"q": "What patterns do Grade 4 students learn in the Ontario math curriculum?",
     "a": "In the Ontario curriculum (Algebra, C1), Grade 4 students extend repeating and growing patterns, show them in tables of values and graphs, find pattern rules and missing elements, make predictions, and create patterns with whole numbers and decimal tenths."},
    {"q": "How do you write a pattern rule in Grade 4?",
     "a": "Say where the pattern starts and what happens each time, for example “start at 5 and add 3 each time.” Check that the same jump works for every pair of numbers, not just the first two."},
    {"q": "How do you find the 10th term of a growing pattern?",
     "a": "Count the jumps: from the 1st term to the 10th there are 9 jumps. For “start at 5 and add 3 each time,” the 10th term is 5 + 9 × 3 = 32."},
    {"q": "What is a decimal pattern with tenths?",
     "a": "It is a pattern that grows or shrinks by tenths, such as 0.2, 0.4, 0.6, 0.8, 1.0. After 0.8 comes 1.0, not 0.10, because 10 tenths make 1 whole."},
]


def gen():
    rnd = random.Random(44809)
    P = People(rnd)
    sets = [set_repeating(), set_growing(), set_rules(), set_decimals(), set_predict(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["e"], it
            assert it["q"] not in allk, it["q"]
            allk.add(it["q"])
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "patterns",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Patterns: Pattern Rules, Tables of Values and Decimal Patterns",
        "seo_title": "Grade 4 Patterns Worksheets: Pattern Rules, Tables of Values and Decimal Tenths (Ontario Math)",
        "short_title": "Patterns",
        "domain": "Algebra",
        "standard_code": "Grade 4: C1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating and growing patterns",
        "meta_desc": "Free Grade 4 math worksheets on patterns: find the core and later elements of repeating patterns, extend growing patterns with tables of values and graphs, write pattern rules for numbers to 10 000 and decimal tenths, and predict missing terms. 100 questions with an answer key, matched to the Ontario curriculum.",
        "key_big": "A pattern rule tells where to start and what to do each time.",
        "key_sub": "Check that the jump works every time: 5, 8, 11, 14 is “start at 5 and add 3 each time.” For the 10th term, there are 9 jumps from the 1st. Keep the term number and the value apart, and remember that 10 tenths make 1.0.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(repeating pattern|number track|number line|shape pattern|table of values|graph of|tenths bars)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
