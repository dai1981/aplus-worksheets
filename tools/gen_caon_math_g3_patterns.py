# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Patterns (Ontario Mathematics Curriculum 2020, C1.1-C1.4)
  python3 tools/gen_ca_math_g3_patterns.py
Repeating patterns and their core, growing and shrinking shape patterns with tables of values,
number patterns to 1000 (+25, −10, by 50s), pattern rules, missing elements, predicting the
10th term, and real-life patterns in Canadian settings.
Wrong answers come from real mistakes: a wrong core (stopping too soon or going one too far),
using only the first step of a pattern, mixing up the figure number and the number of objects,
counting one jump too many for the 10th term, going the wrong way, and changing the wrong digit.
Every answer is computed and checked in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
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
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


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


# ============================================================ set 1: repeating patterns and the core
AB = ["blue circle", "blue square"]
ABB = ["red circle", "blue circle", "blue circle"]
ABC = ["green triangle", "green circle", "green square"]
AABB = ["yellow star", "yellow star", "red star", "red star"]
ARR = ["arrow up", "arrow right", "arrow down", "arrow left"]
ABBC = ["red triangle", "blue circle", "blue circle", "yellow square"]
AAB = ["blue square", "blue square", "red triangle"]
WORDS = ["w:clap", "w:clap", "w:snap", "w:stomp"]


def next_rep(core, shown, mode, cands, extra=""):
    toks = rep(core, shown)
    a = rep(core, shown + 1)[-1]
    e = "The core is <b>%s</b>. It repeats again and again. The last one shown is the %s element of a core, so next comes <b>%s</b>.%s" % (
        names(core, mode), ordn(shown % len(core) or len(core)), name(a, mode), extra)
    return mcq(fig(row_svg(toks + ["?"])) + "The pattern repeats. What comes next?", name(a, mode), cands, e)


def set_repeating():
    q1 = next_rep(AB, 7, "shape", ["circle", "triangle", "star"], " A circle is always followed by a square.")
    q2 = next_rep(ABB, 8, "colour", ["red", "yellow", "green"], " After red comes blue, blue. Only then red again.")
    q3 = next_rep(ABC, 7, "shape", ["triangle", "square", "star"])
    q6 = next_rep(ARR, 6, "shape", ["up", "left", "right"], " Each arrow makes a quarter turn clockwise.")
    q19 = next_rep(AABB, 9, "colour", ["red", "blue", "green"], " Two yellow, then two red. The pattern is not yellow, red, yellow, red.")

    def core_q(core, shown, mode, cands, extra):
        return mcq(fig(row_svg(rep(core, shown))) + "What is the core of this pattern?", names(core, mode), cands,
                   "The core is the shortest part that repeats from the start. Here it is <b>%s</b>, and then it starts again.%s"
                   % (names(core, mode), extra))

    q4 = core_q(AB, 8, "shape", ["circle, square, circle", "circle", "circle, circle, square"],
                " “circle, square, circle” is too long: it goes into the next core.")
    q5 = core_q(ABB, 9, "colour", ["red, blue", "red, blue, blue, red", "blue, blue"],
                " The core is not “red, blue”: after red, blue comes another blue, not red.")
    q7 = core_q(ABC, 9, "shape", ["triangle, circle", "triangle, circle, square, triangle", "circle, square"],
                " Check by repeating it: triangle, circle, square, triangle, circle, square.")
    wtoks = rep(WORDS, 6)
    q8 = mcq(fig(row_svg(wtoks + ["?"])) + "Kai makes a sound pattern. What comes next?", "snap",
             ["clap", "stomp", "jump"],
             "The core is <b>clap, clap, snap, stomp</b>. The last two shown are clap, clap, so next comes <b>snap</b>. "
             "There are two claps in each core, not one.")
    q9 = nums_mcq(fig(row_svg(rep(AABB, 12))) + "How many elements are in the core of this pattern?", 4, [2, 8, 12],
                  "The core is yellow, yellow, red, red. That is <b>4</b> elements. 2 is the number of colours, not elements.")
    q10 = mcq("Which pattern has the core A, B, B?", "A B B A B B A B B",
              ["A B A B A B A B", "A A B A A B A A B", "A B B B A B B B"],
              "The core A, B, B is one A and two Bs. Repeat it: <b>A B B A B B A B B</b>.")
    q11 = mcq(fig(row_svg(rep(ABB, 6))) + "Which letters show the same pattern?", "A B B A B B",
              ["A B A B A B", "A A B A A B", "A B C A B C"],
              "Red is A and blue is B. red, blue, blue is A, B, B. So the pattern is <b>A B B A B B</b>.")
    q12 = mcq(fig(row_svg(rep(ABBC, 6) + ["?", "?"])) + "The pattern repeats. What are the next two shapes?",
              "blue circle, yellow square",
              ["red triangle, blue circle", "yellow square, red triangle", "blue circle, blue circle"],
              "The core is red triangle, blue circle, blue circle, yellow square. The row ends with red triangle, blue circle. "
              "Next come <b>blue circle, yellow square</b>.")
    q13 = nums_mcq(fig(row_svg(rep(ABC, 12))) + "How many times does the core repeat in this row?", 4, [3, 12, 6],
                   "The core is triangle, circle, square (3 shapes). 12 shapes ÷ 3 = <b>4</b> times. "
                   "3 is the number of shapes in the core.")
    nums = rep([3, 1, 4], 9)
    q14 = mcq(track(nums) + "What is the core of this number pattern?", "3, 1, 4",
              ["3, 1", "3, 1, 4, 3", "1, 4"],
              "The numbers go 3, 1, 4, 3, 1, 4, 3, 1, 4. The core is <b>3, 1, 4</b>. “3, 1” is too short: after 1 comes 4.")
    q15 = mcq("Which of these is NOT a repeating pattern?", "A B A A B A B B",
              ["A B A B A B A B", "A A B A A B A A B", "A B C A B C A B C"],
              "The others repeat the same core each time. <b>A B A A B A B B</b> has no part that repeats the same way.")
    bad = rep(ABB, 9)
    bad[5] = "red circle"
    assert rep(ABB, 9)[5] == "blue circle"
    q16 = mcq(fig(row_svg(bad, numbered=True)) + "Maya makes a pattern with the core red, blue, blue. "
              "She makes one mistake. Which circle is wrong?", "circle 6", ["circle 4", "circle 7", "circle 5"],
              "Red circles go at 1, 4 and 7. Circles 5 and 6 should be blue. <b>Circle 6</b> is red, so it is the mistake.")
    q17 = nums_mcq("Zoe makes a pattern with the core square, circle, circle. She uses the core 3 times. "
                   "How many circles does she use?", 6, [3, 9, 2],
                   "Each core has 2 circles. 3 cores: 2 + 2 + 2 = <b>6</b> circles. 3 counts only 1 circle in each core.")
    q18 = next_rep(AAB, 8, "both", ["blue square", "red square", "blue triangle"],
                   " Both the shape and the colour change: it is a red triangle.")
    n7 = rep([7, 7, 3, 1], 9)
    q20 = mcq(track(n7) + "The pattern repeats. What are the next two numbers?", "7, 3", ["3, 1", "1, 7", "7, 7"],
              "The core is 7, 7, 3, 1. The row ends with one 7, so next come <b>7, 3</b>.")
    out = [q1, q2, q3, q6, q4, q8, q11, q5, q9, q18, q19, q7, q10, q13, q12, q14, q17, q15, q16, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Repeating patterns and the core", "items": out}


# ============================================================ set 2: growing shape patterns and tables of values
HEADS = lambda nm: ["Figure number", "Number of " + thing(nm)]


def set_growing():
    def d_of(nm):
        return cnt(nm, 2) - cnt(nm, 1)

    def next_q(nm, cands, extra=""):
        th = thing(nm)
        a, last, d = cnt(nm, 4), cnt(nm, 3), d_of(nm)
        e = "Count each figure: %s. Each figure has %d %s %s. %d %s %d = <b>%d</b> %s in Figure 4.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", th,
            last, "+" if d > 0 else MINUS, abs(d), a, th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure 4?" % th, a, cands, e)

    def rule_q(nm, cands, extra=""):
        d, s0 = d_of(nm), cnt(nm, 1)
        e = "Figure 1 has %d %s. Count each figure: %s. The pattern rule is <b>%s</b>.%s" % (
            s0, thing(nm)[:-1] if s0 == 1 else thing(nm), lst([cnt(nm, k) for k in (1, 2, 3)]), rule_text(s0, d).lower(), extra)
        return mcq(fig(pattern_svg(nm)) + "What is the pattern rule for the number of %s?" % thing(nm),
                   rule_text(s0, d), cands, e)

    def table_q(nm, shown, k, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, j) for j in range(1, k + 1)]
        d = d_of(nm)
        e = "The table goes up by %d each time. Keep going: %s. Figure %d has <b>%d</b> %s.%s" % (
            d, lst(vals[shown - 1:]), k, vals[-1], th, extra)
        return nums_mcq(fig(tov_svg(list(range(1, shown + 1)), vals[:shown], HEADS(nm))) +
                        "This table of values shows a growing pattern. How many %s are in Figure %d?" % (th, k),
                        vals[-1], cands, e)

    def which_q(nm, n, extra=""):
        th = thing(nm)
        vals = [cnt(nm, k) for k in range(1, 12)]
        k = vals.index(n) + 1
        e = "Keep going: %s. Figure <b>%d</b> has %d %s. %d is the number of %s, not the figure number.%s" % (
            lst(vals[:k]), k, n, th, n, th, extra)
        return mcq(fig(pattern_svg(nm)) + "The pattern keeps going. Which figure has %d %s?" % (n, th),
                   "Figure %d" % k, ["Figure %d" % n, "Figure %d" % (k + 1), "Figure %d" % (k - 1)], e)

    q1 = next_q("L", [8, 6, 9])
    q2 = next_q("dots", [16, 25, 18], " 16 counts on 1, not 5.")
    q3 = next_q("tri", [8, 11, 10], " Count the sticks, not the triangles.")
    q4 = next_q("towers", [13, 18, 16])
    q5 = next_q("dec", [10, 7, 4], " This pattern is shrinking.")
    q6 = next_q("tables", [9, 12, 16], " 16 counts 4 chairs for every table, but no chairs fit where tables touch.")
    st = [cnt("stairs", k) for k in range(1, 6)]
    q7 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 4?", st[3],
                  [8, 9, 12],
                  "Count: 1, 3, 6. The jumps are +2, then +3. Each jump is 1 more than the last, so the next jump is +4. "
                  "6 + 4 = <b>10</b>. 8 uses only the first step (+2).")
    q20 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 5?", st[4],
                   [14, 9, 16],
                   "The jumps are +2, +3, +4, +5: 1, 3, 6, 10, <b>15</b>. 14 adds +4 again, but each jump grows by 1. "
                   "9 uses only the first step (+2) each time.")
    q8 = rule_q("L", ["Start at 1 and add 1 each time", "Start at 2 and add 2 each time", "Start at 1 and add 3 each time"])
    q9 = rule_q("sq", ["Start at 4 and add 4 each time", "Start at 3 and add 4 each time", "Start at 1 and add 3 each time"],
                " 4 is how many sticks Figure 1 has. It is not the jump.")
    q10 = rule_q("dec", ["Start at 12 and add 2 each time", "Start at 12 and subtract 1 each time",
                         "Start at 8 and add 2 each time"], " The pattern gets smaller, so the rule subtracts.")
    q11 = rule_q("towers", ["Start at 3 and add 3 each time", "Start at 6 and add 6 each time",
                            "Start at 1 and add 3 each time"], " Each new tower has 3 cubes.")
    q12 = table_q("tri", 4, 6, [11, 15, 12], " 11 is Figure 5.")
    q13 = table_q("sq", 4, 5, [14, 17, 19])
    q14 = table_q("L", 4, 6, [9, 13, 12], " 12 is 6 × 2, but the pattern starts at 1.")
    q15 = which_q("sq", 13)
    q16 = which_q("dots", 30)
    q17 = which_q("tables", 14)
    tv = [cnt("towers", k) for k in (1, 2, 3, 4)]
    q18 = mcq(fig(tov_svg([1, 2, 3, 4], tv, HEADS("towers"))) + "In this table, what does the 4 in the top row tell you?",
              "the figure number", ["the number of cubes", "how many cubes are added", "the rule"],
              "The top row counts the figures: 1, 2, 3, 4. So 4 is <b>the figure number</b>. The bottom row is the number of cubes.")
    lv = [cnt("L", k) for k in (1, 2, 3, 4)]
    q19 = mcq(fig(tov_svg([1, 2, 3, 4], lv, HEADS("L"))) + "In this table, 7 is under 4. What does that mean?",
              "Figure 4 has 7 tiles", ["Figure 7 has 4 tiles", "Each figure adds 7 tiles", "Each figure adds 4 tiles"],
              "Read down the column: the figure number is on top and the number of tiles is below. So <b>Figure 4 has 7 tiles</b>.")
    out = [q1, q2, q3, q5, q4, q6, q8, q10, q9, q11, q12, q13, q14, q15, q16, q17, q18, q19, q7, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Growing shape patterns and tables of values", "items": out}


# ============================================================ set 3: number patterns to 1000 and the rule
def set_numbers():
    def nxt(nums, cands, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = nums[-1] + d
        e = "Each number is %d %s. %d %s %d = <b>%d</b>.%s" % (
            abs(d), "more" if d > 0 else "less", nums[-1], "+" if d > 0 else MINUS, abs(d), a, extra)
        return nums_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)

    q1 = nxt([240, 250, 260, 270], [271, 290, 370], " Only the tens digit goes up.")
    q2 = nxt([430, 420, 410], [409, 390, 420], " 409 is only 1 less.")
    q3 = nxt([350, 400, 450], [455, 550, 460], " Counting by 50s, the numbers end in 00 or 50.")
    q4 = nxt([100, 125, 150, 175], [176, 225, 180], " Counting by 25s, the numbers end in 00, 25, 50 or 75.")
    q5 = nxt([263, 363, 463], [464, 473, 663], " Only the hundreds digit goes up.")
    q6 = nxt([300, 275, 250], [230, 200, 275], " The numbers go down by 25 each time.")
    q7 = nxt([680, 685, 690, 695], [696, 705, 690], " 695 + 5 crosses the hundred to 700.")
    q8 = nxt([900, 850, 800], [700, 790, 850], " 700 skips a number.")
    q9 = nxt([375, 385, 395], [396, 495, 400], " 39 tens + 1 ten = 40 tens, so 395 + 10 = 405.")
    q19 = nxt([515, 510, 505], [504, 495, 405], " 504 is only 1 less.")

    def rq(nums, wrong, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        e = "%d %s %d = %d, and every jump is the same. The rule is <b>%s</b>.%s" % (
            nums[0], "+" if d > 0 else MINUS, abs(d), nums[1], rule_text(nums[0], d).lower(), extra)
        return mcq(track(nums) + "What is the pattern rule?", rule_text(nums[0], d),
                   [rule_text(s, k) for s, k in wrong], e)

    q10 = rq([50, 75, 100, 125], [(50, 50), (25, 25), (50, -25)], " 50 is the start, not the jump.")
    q11 = rq([615, 605, 595, 585], [(615, 10), (615, -100), (615, -20)], " The numbers get smaller, so the rule subtracts.")
    q12 = rq([150, 200, 250, 300], [(150, 150), (150, 5), (50, 50)])
    q13 = mcq(track([840, 815, 790, 765]) + "How does this pattern change?", "shrinking by 25 each time",
              ["growing by 25 each time", "shrinking by 15 each time", "shrinking by 20 each time"],
              "The numbers get smaller, so it is shrinking. 840 − 25 = 815, 815 − 25 = 790. It is <b>shrinking by 25 each time</b>.")
    g1 = [1, 2, 4, 7, 11]
    q14 = nums_mcq(track(g1 + [None]) + "What number comes next?", 16, [15, 12, 22],
                   "The jumps are +1, +2, +3, +4. Each jump is 1 more, so the next jump is +5. 11 + 5 = <b>16</b>. "
                   "12 uses only the first step (+1).")
    g2 = [10, 20, 40, 70]
    q15 = nums_mcq(track(g2 + [None]) + "What number comes next?", 110, [100, 80, 140],
                   "The jumps are +10, +20, +30. The next jump is +40. 70 + 40 = <b>110</b>. "
                   "80 uses only the first step (+10).")
    want = seq(40, 25, 4)
    q16 = mcq("Which pattern follows the rule “Start at 40 and add 25 each time”?", lst(want),
              ["25, 65, 105, 145", "40, 60, 80, 100", "40, 65, 90, 125"],
              "40 + 25 = 65, 65 + 25 = 90, 90 + 25 = 115. The pattern is <b>%s</b>. 90 + 25 is 115, not 125." % lst(want))
    q17 = nums_mcq(fig(nline_svg(175, [25] * 4)) + "Start at 175. Make the jumps. Where do you land?", 275,
                   [200, 300, 250], "Count on by 25s 4 times: 200, 225, 250, <b>275</b>.")
    q18 = nums_mcq(fig(nline_svg(600, [-50] * 3)) + "Start at 600. Make the jumps. Where do you land?", 450,
                   [550, 400, 750], "Count back by 50s 3 times: 550, 500, <b>450</b>. 750 goes the wrong way.")
    q20 = nums_mcq("Mei counts by 25s from 0: 0, 25, 50, 75, 100 … Which number will she say?", 350,
                   [340, 260, 415],
                   "Counting by 25s from 0, every number ends in 00, 25, 50 or 75. Only <b>350</b> ends that way.")
    out = [q1, q2, q3, q5, q4, q8, q6, q12, q10, q7, q9, q19, q11, q13, q17, q18, q14, q16, q15, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Number patterns to 1000 and the pattern rule", "items": out}


# ============================================================ set 4: missing elements
def set_missing():
    def gap_rep(core, n, i, mode, cands):
        toks = rep(core, n)
        a = toks[i]
        toks[i] = "?"
        e = "The core is <b>%s</b>. Say the pattern from the start: %s. The missing one is <b>%s</b>." % (
            names(core, mode), names(rep(core, i + 1), mode), name(a, mode))
        return mcq(fig(row_svg(toks)) + "What is missing from this repeating pattern?", name(a, mode), cands, e)

    q1 = gap_rep(AB, 8, 4, "shape", ["square", "triangle", "star"])
    q2 = gap_rep(ABB, 9, 5, "colour", ["red", "yellow", "green"])
    q3 = gap_rep(ABC, 9, 7, "shape", ["triangle", "square", "star"])
    q16 = gap_rep(ABBC, 8, 6, "both", ["red triangle", "yellow square", "blue square"])

    def miss(nums, i, cands, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = nums[i]
        if i == 0:
            e = "The rule is %s. Go back one step from %d: %d %s %d = <b>%d</b>." % (
                jump(d), nums[1], nums[1], MINUS if d > 0 else "+", abs(d), a)
        else:
            e = "The rule is %s. %d %s %d = <b>%d</b>." % (jump(d), nums[i - 1], "+" if d > 0 else MINUS, abs(d), a)
            if i < len(nums) - 1:
                e += " Check: %d %s %d = %d." % (a, "+" if d > 0 else MINUS, abs(d), nums[i + 1])
        return nums_mcq(track(nums, (i,)) + "What number is missing?", a, cands, e + extra)

    q4 = miss([30, 40, 50, 60, 70], 2, [41, 60, 45])
    q5 = miss([125, 150, 175, 200], 2, [160, 155, 225])
    q6 = miss([330, 340, 350, 360], 0, [370, 339, 320], " The first number is 10 less than 340.")
    q7 = miss([805, 795, 785, 775], 2, [784, 765, 885])
    q8 = miss([850, 900, 950, 1000], 2, [905, 910, 850])

    def two(nums, i, j, wrong):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        a = "%d, %d" % (nums[i], nums[j])
        e = "The rule is %s. Fill in each box: %s. The missing numbers are <b>%s</b>." % (jump(d), lst(nums), a)
        return mcq(track(nums, (i, j)) + "Which two numbers are missing, in order?", a, wrong, e)

    q9 = two([15, 20, 25, 30, 35], 2, 3, ["21, 22", "25, 35", "30, 25"])
    q10 = two([500, 475, 450, 425, 400], 1, 3, ["490, 440", "475, 435", "480, 430"])
    q20 = two([250, 275, 300, 325, 350], 0, 4, ["225, 375", "255, 345", "250, 330"])

    def tmiss(nm, i, cands, extra=""):
        vals = [cnt(nm, k) for k in range(1, 6)]
        a = vals[i]
        row = [v if k != i else "?" for k, v in enumerate(vals)]
        d = vals[1] - vals[0]
        e = "The number of %s goes up by %d each time: %s. The missing number is <b>%d</b>.%s" % (
            thing(nm), d, lst(vals), a, extra)
        return nums_mcq(fig(tov_svg([1, 2, 3, 4, 5], row, HEADS(nm))) + "What number is missing from the table of values?",
                        a, cands, e)

    q11 = tmiss("tri", 2, [6, 8, 10])
    q12 = tmiss("dots", 4, [21, 30, 6], " 6 is the next figure number, not the number of dots.")
    tw = [cnt("towers", k) for k in range(1, 5)]
    q13 = nums_mcq(fig(tov_svg([1, 2, "?", 4], tw, HEADS("towers"))) + "What figure number is missing from the table?",
                   3, [12, 4, 6],
                   "The figure numbers count 1, 2, 3, 4. So the missing figure number is <b>3</b>. 12 is the number of cubes in Figure 3.")
    lv = [cnt("L", k) for k in (1, 2, 3)]
    q14 = nums_mcq(fig(pattern_svg("L", hide=2)) + "Figure 2 is hidden. How many tiles are in Figure 2?", lv[1],
                   [4, 2, 6],
                   "Figure 1 has 1 tile and Figure 3 has 5 tiles. The pattern goes up by the same amount each time: "
                   "1, <b>3</b>, 5. The rule is add 2.")
    sv = [cnt("sq", k) for k in (1, 2, 3, 4)]
    q15 = nums_mcq(fig(pattern_svg("sq", (2, 3, 4))) + "How many sticks are in Figure 1?", sv[0], [3, 1, 10],
                   "Count: Figure 2 has 7, Figure 3 has 10, Figure 4 has 13. Each figure adds 3 sticks. "
                   "Go back one step: 7 − 3 = <b>4</b>.")
    bad = [120, 145, 170, 185, 220]
    q17 = nums_mcq(track(bad) + "One number in this pattern is wrong. Which one?", 185, [145, 170, 220],
                   "The rule is +25: 120, 145, 170, 195, 220. <b>185</b> should be 195.")
    q18 = nums_mcq("Liam counts by 50s: 150, 200, 250, 290, 350. One number is a mistake. What should it be?", 300,
                   [260, 400, 255],
                   "Counting by 50s: 150, 200, 250, <b>300</b>, 350. 250 + 50 = 300, not 290.")
    q19 = nums_mcq(track([2, 3, 5, None, 12]) + "What number is missing?", 8, [7, 6, 10],
                   "The jumps are +1, +2, then +3, then +4. 5 + 3 = <b>8</b>. Check: 8 + 4 = 12. "
                   "6 uses only the first step (+1).")
    out = [q1, q2, q4, q3, q6, q5, q11, q16, q7, q12, q14, q9, q8, q13, q10, q15, q17, q18, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Find the missing elements", "items": out}


# ============================================================ set 5: predict the 10th term and real-life patterns
def set_predict(P):
    its = []

    def nth_rep(core, shown, n, mode, cands, what):
        a = rep(core, n)[-1]
        L = len(core)
        pos = [k for k in range(1, n + 1) if (k - 1) % L == (n - 1) % L]
        assert all(rep(core, k)[-1] == a for k in pos)
        e = ("The core has %d elements. The %s element of every core is %s, at %s. So the %s is <b>%s</b>."
             % (L, ordn((n - 1) % L + 1), name(a, mode), lst(pos), ordn(n), name(a, mode)))
        return mcq(fig(row_svg(rep(core, shown))) + "The pattern keeps repeating. What %s is the %s %s?" % (
            "colour" if mode == "colour" else "shape", ordn(n), what), name(a, mode), cands, e)

    q1 = nth_rep(ABB, 6, 10, "colour", ["blue", "yellow", "green"], "circle")
    q2 = nth_rep(ABC, 6, 12, "shape", ["triangle", "circle", "star"], "shape")
    q3 = nth_rep(AABB, 8, 15, "colour", ["yellow", "blue", "green"], "star")

    p = seq(7, 3, 10)
    q4 = nums_mcq(track(p[:4] + [None]) + "The pattern rule is “Start at 7 and add 3 each time.” What is the 10th number?",
                  p[9], [37, 30, 31],
                  "From the 1st to the 10th number there are 9 jumps. 9 × 3 = 27. 7 + 27 = <b>34</b>. "
                  "37 makes 10 jumps, one too many.")
    p = seq(25, 25, 10)
    q5 = nums_mcq(track(p[:4] + [None]) + "The pattern keeps going. What is the 10th number?", p[9], [275, 225, 35],
                  "Count by 25s: %s. The 10th number is <b>%d</b>. 225 is only the 9th." % (lst(p), p[9]))
    sv = [cnt("sq", k) for k in range(1, 11)]
    q6 = nums_mcq(fig(pattern_svg("sq")) + "The pattern keeps going. How many sticks are in Figure 10?", sv[9],
                  [34, 30, 40],
                  "Start at 4 and add 3 each time. From Figure 1 to Figure 10 there are 9 jumps: 9 × 3 = 27. "
                  "4 + 27 = <b>31</b>. 40 is 10 × 4, but 4 is only Figure 1.")
    lv = [cnt("L", k) for k in range(1, 11)]
    q7 = nums_mcq(fig(pattern_svg("L")) + "The pattern keeps going. How many tiles are in Figure 10?", lv[9],
                  [21, 20, 10],
                  "Start at 1 and add 2 each time: %s. Figure 10 has <b>%d</b> tiles. 10 is the figure number." % (
                      lst(lv), lv[9]))

    def story(t, ans, cands, e, pic="", unit=None):
        d = P.next()
        return nums_mcq(pic + t.format(**d), ans, cands, e.format(**d), unit or str)

    dol = lambda v: "$%d" % v
    q8 = story("A Grade 3 class collects money for the Terry Fox Run. They have $40 after week 1, $65 after week 2 "
               "and $90 after week 3. The pattern continues. How much do they have after week 6?",
               165, [190, 150, 115],
               "The rule is add $25 each week: $40, $65, $90, $115, $140, <b>$165</b>. $150 is 6 × $25, "
               "but the class started at $40.", unit=dol)
    q9 = mcq("{n} has hockey practice every 7 days. The first three practices are on October 2, October 9 and "
             "October 16. What is the date of the 4th practice?".format(**P.next()),
             "October 23", ["October 24", "October 30", "October 17"],
             "Add 7 days each time: 2, 9, 16, <b>23</b>. October 30 is the 5th practice.")
    q10 = story("{n} has 5 loonies in {his} piggy bank. {He} adds 3 loonies each week. How many loonies are there after 4 weeks?",
                17, [12, 20, 8],
                "Start at 5 and add 3 each week: 8, 11, 14, <b>17</b>. 12 forgets the 5 loonies {he} started with.")
    q11 = story("At a hockey arena, row 1 has 20 seats. Each row has 4 more seats than the row before. How many seats are in row 6?",
                40, [44, 24, 36],
                "Start at 20 and add 4 each time: 20, 24, 28, 32, 36, <b>40</b>. 44 is row 7.")
    q12 = story("A sugar shack has 400 L of maple sap. It boils 50 L each hour. How much sap is left after 5 hours?",
                150, [200, 350, 450],
                "Start at 400 and subtract 50 each hour: 350, 300, 250, 200, <b>150 L</b>. 450 goes the wrong way.",
                unit=lambda v: "%d L" % v)
    q13 = story("{n} skates 2 laps at the rink on day 1, 4 laps on day 2 and 6 laps on day 3. "
                "The pattern continues. How many laps does {he} skate on day 10?",
                20, [18, 22, 12],
                "Start at 2 and add 2 each day. Day 10: 2 + 9 × 2 = <b>20</b> laps. 18 is day 9.")
    q14 = story("The table shows juice boxes in packs. How many juice boxes are in 10 packs?", 80, [40, 72, 88],
                "Each pack adds 8 juice boxes: 8, 16, 24, 32 … 72, <b>80</b>. 72 is 9 packs.",
                fig(tov_svg([1, 2, 3, 4], [8, 16, 24, 32], ["Packs", "Juice boxes"])))
    q15 = mcq("{n} builds a pattern. Figure 1 has 5 blocks. Each figure has 5 more blocks. "
              "Which figure has 45 blocks?".format(**P.next()),
              "Figure 9", ["Figure 45", "Figure 10", "Figure 8"],
              "Count by 5s: 5, 10, 15, 20, 25, 30, 35, 40, 45. That is <b>Figure 9</b>. 45 is the number of blocks, "
              "not the figure number.")
    d = P.next()
    q16 = mcq("{n} counts by 5s from 0. {He} says {his} prediction: “I will say 432.” Is {he} right?".format(**d),
              "No, counting by 5s gives numbers ending in 0 or 5",
              ["Yes, 432 is less than 1000", "Yes, 432 has a 3 in it", "No, {he} only counts to 100".format(**d)],
              "Counting by 5s from 0 gives 5, 10, 15, 20 … Every number ends in 0 or 5. "
              "432 ends in 2, so <b>{he} is not right</b>.".format(**d))
    q17 = story("The school library has 300 books. It gets 25 new books each month. "
                "After how many months will it have 400 books?",
                4, [100, 5, 3],
                "Count by 25s from 300: 325, 350, 375, 400. That is <b>4</b> months. 100 is how many new books, "
                "not the number of months.", unit=lambda v: "%d month%s" % (v, "" if v == 1 else "s"))
    q18 = story("{n} plants tulip bulbs in a pattern: red, red, yellow, red, red, yellow … {He} plants 18 bulbs. "
                "How many are yellow?", 6, [12, 9, 3],
                "The core red, red, yellow has 3 bulbs. 18 ÷ 3 = 6 cores. Each core has 1 yellow bulb, so <b>6</b> are yellow. "
                "12 is the number of red bulbs.")
    q19 = story("A beaver has 30 sticks in its dam after night 1. It adds 12 sticks each night. "
                "How many sticks are in the dam after night 10?",
                138, [150, 120, 126],
                "From night 1 to night 10 there are 9 jumps. 9 × 12 = 108. 30 + 108 = <b>138</b>. "
                "150 makes 10 jumps, one too many.")
    q20 = story("{n}’s book has 120 pages. {He} reads 15 pages each day. How many pages are left to read after 6 days?",
                30, [45, 90, 105],
                "Start at 120 and subtract 15 each day: 105, 90, 75, 60, 45, <b>30</b>. 90 is how many pages {he} has read.")
    assert seq(30, 12, 10)[9] == 138 and seq(40, 25, 6)[5] == 165 and seq(20, 4, 6)[5] == 40
    assert 400 - 50 * 5 == 150 and 120 - 15 * 6 == 30 and seq(5, 3, 5)[4] == 17
    out = [q1, q2, q4, q6, q3, q5, q7, q13, q11, q8, q10, q12, q14, q9, q18, q15, q17, q16, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Predict the 10th term and real-life patterns", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Repeating patterns and the core</h2>"
        "<p>A <b>repeating pattern</b> has a part that repeats again and again. That part is the <b>core</b>. "
        "The core is the shortest part that repeats from the start.</p>"
        "<figure class='sn-fig'>" + row_svg(rep(ABB, 9)) +
        "<figcaption>The core is red, blue, blue. In letters it is A, B, B.</figcaption></figure>"
        "<h2>Growing and shrinking patterns</h2>"
        "<p>A <b>growing pattern</b> gets bigger each time. A <b>shrinking pattern</b> gets smaller. "
        "Count each figure and put the numbers in a <b>table of values</b>.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>Figure 1 has 4 sticks, Figure 2 has 7, Figure 3 has 10.</figcaption></figure>"
        + table(["Figure number", "1", "2", "3", "4"], [["Number of sticks", "4", "7", "10", "13"]]) +
        "<p>The <b>pattern rule</b> tells where to start and what to do each time: "
        "<b>start at 4 and add 3 each time</b>.</p>"
        "<h2>Number patterns to 1000</h2>"
        "<p>Find the jump between two numbers next to each other. Check that the same jump works every time.</p>"
        "<figure class='sn-fig'>" + nline_svg(150, [25, 25, 25], ticks=["150", "175", "200", "225"]) +
        "<figcaption>150, 175, 200, 225. The rule is start at 150 and add 25 each time.</figcaption></figure>"
        + ex("Missing number", "805, 795, ☐, 775",
             "The rule is subtract 10. 795 − 10 = 785. Check: 785 − 10 = 775.", "785")
        + ex("Predict the 10th number", "Start at 7 and add 3 each time. What is the 10th number?",
             "From the 1st number to the 10th there are 9 jumps. 9 × 3 = 27. 7 + 27 = 34.", "34") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Wrong core: red, blue, blue has the core “red, blue”", "Check that the core repeats exactly: red, blue, blue"],
            ["Using only the first step: 1, 2, 4, 7 is “add 1”", "Check every jump: +1, +2, +3, so the next jump is +4"],
            ["Mixing up the figure number and the number of objects", "The figure number is on top of the table. The count is below it"],
            ["Using the first number as the rule: 4, 7, 10 is “add 4”", "Start at 4 and add 3 each time"],
            ["10 jumps for the 10th number", "From the 1st to the 10th number there are 9 jumps"],
        ])
    )


FAQ = [
    {"q": "What patterns do Grade 3 students learn in the Ontario math curriculum?",
     "a": "In the Ontario curriculum (Algebra, C1), Grade 3 students describe and extend repeating, growing and shrinking patterns, show them in tables of values, find pattern rules and missing elements, and make predictions with number patterns up to 1000."},
    {"q": "What is the core of a repeating pattern?",
     "a": "The core is the shortest part of the pattern that repeats from the start. In red, blue, blue, red, blue, blue, the core is red, blue, blue."},
    {"q": "How do you write a pattern rule in Grade 3?",
     "a": "Say where the pattern starts and what happens each time, for example “start at 4 and add 3 each time.” Check that the same jump works for every pair of numbers."},
    {"q": "Are patterns on the Grade 3 EQAO math assessment?",
     "a": "Yes. Patterning and algebra is part of the Ontario Grade 3 math curriculum, and the EQAO Grade 3 assessment is based on that curriculum, so practice with pattern rules, tables of values and missing elements helps."},
]


def gen():
    rnd = random.Random(33807)
    P = People(rnd)
    sets = [set_repeating(), set_growing(), set_numbers(), set_missing(), set_predict(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "patterns",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Patterns: Repeating, Growing and Number Patterns",
        "seo_title": "Grade 3 Patterns Worksheets: Pattern Rules, Tables of Values and Missing Elements (Ontario Math)",
        "short_title": "Patterns",
        "domain": "Algebra",
        "standard_code": "Grade 3: C1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine pattern rules and use them to extend patterns, make and justify predictions, and identify missing elements in repeating and growing patterns",
        "meta_desc": "Free Grade 3 math worksheets on patterns: find the core of repeating patterns, extend growing shape patterns with tables of values, write pattern rules for number patterns to 1000, fill in missing elements and predict the 10th term. 100 questions with an answer key, matched to the Ontario curriculum and good EQAO practice.",
        "key_big": "A pattern rule tells where to start and what to do each time.",
        "key_sub": "In a repeating pattern, find the core: the shortest part that repeats. In a growing or shrinking pattern, find the jump between terms: 4, 7, 10 is “start at 4 and add 3 each time.” For the 10th term, there are 9 jumps from the 1st.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(repeating pattern|number track|number line|shape pattern|table of values)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
