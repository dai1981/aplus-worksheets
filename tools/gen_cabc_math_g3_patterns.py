# -*- coding: utf-8 -*-
"""
British Columbia Grade 3 Math: Increasing and Decreasing Patterns (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g3_patterns.py
Increasing and decreasing number patterns to 1000, shape patterns with tables, pattern rules in
words and numbers, and predictions in BC settings.
Wrong answers come from real mistakes: using only the first step, extending the wrong way
(adding in a decreasing pattern), using the start as the jump, mixing up the figure number and
the number of objects, and counting one jump too many for a later term.
Every answer is computed and checked in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
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
    ok = [v for v in cands if v != ans and 0 <= v <= 1000]
    assert 0 <= ans <= 1000
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


def counters(k):
    """3 rows of counters that lose one column each time: 15, 12, 9, 6, 3."""
    n = 6 - k

    def draw(x, y):
        return "".join("<circle cx='%.1f' cy='%.1f' r='6' fill='#f0a640' stroke='%s' stroke-width='1.3'/>"
                       % (x + 8 + c * 16, y + 8 + r * 16, INK) for r in range(3) for c in range(n))
    return n * 16, 3 * 16, draw


PATTERNS = {
    "ctr": (counters, lambda k: 18 - 3 * k, "counters"),
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



# ------------------------------------------------------------ shared question makers
def nxt(nums, cands, extra=""):
    assert is_pattern(nums)
    d = nums[1] - nums[0]
    a = nums[-1] + d
    e = "Each number is %d %s than the one before. %d %s %d = <b>%d</b>.%s" % (
        abs(d), "more" if d > 0 else "less", nums[-1], "+" if d > 0 else MINUS, abs(d), a, extra)
    return nums_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)


def rq(nums, wrong, extra=""):
    assert is_pattern(nums)
    d = nums[1] - nums[0]
    e = "%d %s %d = %d, and every jump is the same. The rule is <b>%s</b>.%s" % (
        nums[0], "+" if d > 0 else MINUS, abs(d), nums[1], rule_text(nums[0], d).lower(), extra)
    return mcq(track(nums) + "What is the pattern rule?", rule_text(nums[0], d),
               [rule_text(s, k) for s, k in wrong], e)


def d_of(nm):
    return cnt(nm, 2) - cnt(nm, 1)


def HEADS(nm):
    return ["Figure number", "Number of " + thing(nm)]


# ============================================================ set 1: increasing patterns and rules
def set_increasing():
    q1 = nxt([12, 14, 16, 18], [19, 22, 28], " 19 adds only 1.")
    q2 = nxt([35, 40, 45, 50], [51, 60, 45], " Counting by 5s, the numbers end in 0 or 5. 45 goes the wrong way.")
    q3 = nxt([120, 130, 140, 150], [151, 250, 170], " Only the tens digit goes up.")
    q4 = nxt([200, 300, 400], [401, 410, 600], " Only the hundreds digit goes up.")
    q5 = nxt([64, 67, 70, 73], [74, 77, 70], " 70 goes the wrong way.")
    q6 = nxt([150, 175, 200, 225], [226, 275, 230], " Counting by 25s, the numbers end in 00, 25, 50 or 75.")
    q7 = nxt([485, 490, 495], [496, 505, 490], " 496 adds only 1. 490 goes the wrong way.")
    q8 = nxt([347, 357, 367], [368, 477, 387], " Only the tens digit changes.")
    q9 = nxt([612, 712, 812], [813, 822, 712], " 712 goes the wrong way.")
    q10 = nxt([650, 700, 750], [755, 850, 700], " Counting by 50s, the numbers end in 00 or 50.")
    q11 = rq([6, 10, 14, 18], [(6, 6), (4, 4), (6, -4)], " 6 is where the pattern starts, not the jump.")
    q12 = rq([25, 50, 75, 100], [(25, 50), (50, 25), (25, -25)], " The pattern gets bigger, so the rule adds.")
    q13 = rq([430, 440, 450, 460], [(430, 1), (430, 100), (440, 10)], " The tens digit goes up by 1, so the jump is 10.")
    q14 = rq([105, 110, 115, 120], [(105, 10), (5, 5), (105, -5)], " The pattern gets bigger, so the rule adds.")
    q15 = mcq("Which pattern follows the rule “Start at 14 and add 3 each time”?", "14, 17, 20, 23",
              ["14, 15, 16, 17", "17, 20, 23, 26", "14, 17, 20, 24"],
              "Start at 14. 14 + 3 = 17, 17 + 3 = 20, 20 + 3 = 23. The pattern is <b>14, 17, 20, 23</b>. "
              "The first number is 14, not 17.")
    q16 = nums_mcq(fig(nline_svg(240, [20] * 3)) + "Start at 240. Make the jumps. Where do you land?", 300,
                   [260, 180, 280], "Count on by 20s 3 times: 260, 280, <b>300</b>. 260 is only the first jump. "
                   "180 goes the wrong way.")
    q17 = mcq("Which is an increasing pattern?", "8, 12, 16, 20", ["20, 16, 12, 8", "8, 12, 8, 12", "8, 12, 9, 13"],
              "In an increasing pattern the numbers get bigger by the same amount each time. "
              "<b>8, 12, 16, 20</b> adds 4 each time. 20, 16, 12, 8 is decreasing.")
    q18 = nums_mcq(track([470, 480, 490, 500], (1,)) + "What number is missing?", 480, [471, 485, 460],
                   "The rule is +10. 470 + 10 = <b>480</b>. Check: 480 + 10 = 490.")
    q19 = mcq(track([318, 343, 368, 393]) + "How does this pattern change?", "It increases by 25 each time",
              ["It decreases by 25 each time", "It increases by 20 each time", "It increases by 35 each time"],
              "The numbers get bigger, so it increases. 318 + 25 = 343, 343 + 25 = 368. "
              "It <b>increases by 25 each time</b>.")
    assert seq(318, 25, 4) == [318, 343, 368, 393]
    p = seq(815, 30, 4)
    q20 = nums_mcq("A pattern starts at 815 and adds 30 each time. What is the 4th number?", p[3], [845, 935, 875],
                   "The numbers are %s. The 4th number is <b>%d</b>. From the 1st to the 4th number there are 3 jumps. "
                   "845 is only the first step." % (lst(p), p[3]))
    out = [q1, q2, q3, q4, q5, q17, q6, q11, q12, q16, q7, q8, q13, q18, q9, q14, q10, q15, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Increasing patterns and pattern rules", "items": out}


# ============================================================ set 2: decreasing patterns
def set_decreasing():
    q1 = nxt([20, 18, 16, 14], [16, 13, 10], " 16 goes the wrong way: the numbers get smaller.")
    q2 = nxt([50, 45, 40, 35], [40, 34, 25], " 40 goes the wrong way.")
    q3 = nxt([90, 80, 70, 60], [70, 59, 40])
    q4 = nxt([900, 800, 700], [800, 699, 690], " Only the hundreds digit goes down.")
    q5 = nxt([365, 355, 345], [355, 344, 245], " Only the tens digit goes down.")
    q6 = nxt([200, 175, 150, 125], [150, 124, 75], " Counting back by 25s, the numbers end in 00, 25, 50 or 75.")
    q7 = nxt([506, 504, 502], [504, 501, 498])
    q8 = nxt([430, 410, 390], [410, 380, 350], " 390 − 20: 39 tens − 2 tens = 37 tens.")
    q9 = nxt([1000, 950, 900], [950, 899, 800], " 950 goes the wrong way.")
    q10 = nxt([72, 69, 66, 63], [66, 62, 57])
    q11 = rq([80, 76, 72, 68], [(80, 4), (80, -8), (76, -4)], " The numbers get smaller, so the rule subtracts.")
    q12 = rq([600, 550, 500, 450], [(600, 50), (600, -5), (550, -50)], " The pattern starts at 600, not 550.")
    q13 = rq([245, 235, 225, 215], [(245, 10), (245, -100), (245, -1)], " The tens digit goes down by 1, so the jump is 10.")
    q14 = nums_mcq(fig(nline_svg(500, [-25] * 4)) + "Start at 500. Make the jumps back. Where do you land?", 400,
                   [475, 600, 425], "Count back by 25s 4 times: 475, 450, 425, <b>400</b>. 475 is only the first jump. "
                   "600 goes the wrong way.")
    q15 = mcq("Which is a decreasing pattern?", "45, 40, 35, 30", ["30, 35, 40, 45", "45, 40, 45, 40", "45, 50, 40, 35"],
              "In a decreasing pattern the numbers get smaller by the same amount each time. "
              "<b>45, 40, 35, 30</b> subtracts 5 each time. 30, 35, 40, 45 is increasing.")
    p = seq(96, -6, 4)
    q16 = nums_mcq("A pattern starts at 96 and subtracts 6 each time. What is the 4th number?", p[3], [90, 72, 114],
                   "The numbers are %s. The 4th number is <b>%d</b>. 90 is only the first step. 114 goes the wrong way."
                   % (lst(p), p[3]))
    q17 = mcq("Which pattern follows the rule “Start at 300 and subtract 20 each time”?", "300, 280, 260, 240",
              ["300, 320, 340, 360", "280, 260, 240, 220", "300, 298, 296, 294"],
              "Start at 300. 300 − 20 = 280, 280 − 20 = 260, 260 − 20 = 240. The pattern is <b>300, 280, 260, 240</b>. "
              "300, 320, 340, 360 adds instead of subtracts.")
    q18 = nums_mcq(track([750, 740, 730, 720], (0,)) + "What number is missing?", 750, [710, 741, 840],
                   "The rule is subtract 10. Go back one step from 740: 740 + 10 = <b>750</b>. "
                   "710 continues the pattern the wrong way: it is the next number, not the first.")
    q19 = mcq(track([184, 174, 164, 154]) + "How does this pattern change?", "It decreases by 10 each time",
              ["It increases by 10 each time", "It decreases by 1 each time", "It decreases by 100 each time"],
              "The numbers get smaller, so it decreases. 184 − 10 = 174, 174 − 10 = 164. It <b>decreases by 10 each time</b>.")
    p = seq(425, -25, 6)
    q20 = nums_mcq("A pattern starts at 425 and subtracts 25 each time. What is the 6th number?", p[5], [275, 400, 550],
                   "The numbers are %s. The 6th number is <b>%d</b>. There are 5 jumps, not 6. "
                   "275 makes 6 jumps, one too many." % (lst(p), p[5]))
    assert 425 + 125 == 550 and 425 - 150 == 275
    out = [q1, q2, q3, q15, q4, q10, q5, q11, q6, q14, q7, q13, q8, q18, q12, q9, q19, q17, q16, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Decreasing patterns", "items": out}


# ============================================================ set 3: shape patterns with tables
def set_shapes():
    def next_q(nm, cands, extra=""):
        th = thing(nm)
        a, last, d = cnt(nm, 4), cnt(nm, 3), d_of(nm)
        e = "Count each figure: %s. Each figure has %d %s %s. %d %s %d = <b>%d</b> %s in Figure 4.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", th,
            last, "+" if d > 0 else MINUS, abs(d), a, th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure 4?" % th, a, cands, e)

    def rule_q(nm, cands, extra=""):
        d, s0 = d_of(nm), cnt(nm, 1)
        e = "Count each figure: %s. Figure 1 has %d %s. The pattern rule is <b>%s</b>.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), s0, thing(nm)[:-1] if s0 == 1 else thing(nm),
            rule_text(s0, d).lower(), extra)
        return mcq(fig(pattern_svg(nm)) + "What is the pattern rule for the number of %s?" % thing(nm),
                   rule_text(s0, d), cands, e)

    def table_q(nm, shown, k, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, j) for j in range(1, k + 1)]
        d = d_of(nm)
        e = "The table goes %s by %d each time. Keep going: %s. Figure %d has <b>%d</b> %s.%s" % (
            "up" if d > 0 else "down", abs(d), lst(vals[shown - 1:]), k, vals[-1], th, extra)
        return nums_mcq(fig(tov_svg(list(range(1, shown + 1)), vals[:shown], HEADS(nm))) +
                        "This table shows a shape pattern. How many %s are in Figure %d?" % (th, k),
                        vals[-1], cands, e)

    def which_q(nm, n, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, k) for k in range(1, 7)]
        k = vals.index(n) + 1
        e = "Keep going: %s. Figure <b>%d</b> has %d %s.%s" % (lst(vals[:k]), k, n, th, extra)
        return mcq(fig(pattern_svg(nm)) + "The pattern keeps going. Which figure has %d %s?" % (n, th),
                   "Figure %d" % k, ["Figure %d" % c for c in cands], e)

    def tmiss(nm, i, cands, extra=""):
        vals = [cnt(nm, k) for k in range(1, 6)]
        a = vals[i]
        row = [v if k != i else "?" for k, v in enumerate(vals)]
        d = vals[1] - vals[0]
        e = "The number of %s goes %s by %d each time: %s. The missing number is <b>%d</b>.%s" % (
            thing(nm), "up" if d > 0 else "down", abs(d), lst(vals), a, extra)
        return nums_mcq(fig(tov_svg([1, 2, 3, 4, 5], row, HEADS(nm))) + "What number is missing from the table?",
                        a, cands, e)

    q1 = next_q("L", [8, 6, 9], " 6 adds only 1.")
    q2 = next_q("dots", [16, 25, 21], " Each new row has 5 dots, not 1.")
    q3 = next_q("tri", [8, 11, 4], " Count the sticks, not the triangles.")
    q4 = next_q("dec", [10, 7, 4], " The pattern is decreasing. 10 goes the wrong way.")
    q5 = next_q("ctr", [12, 8, 3], " Each figure loses one column of 3 counters. 12 goes the wrong way.")
    q6 = next_q("tables", [9, 12, 16], " No chairs fit where two tables touch.")
    q7 = next_q("towers", [13, 18, 16], " Each new tower has 3 cubes.")
    q8 = table_q("tri", 4, 6, [11, 15, 12], " 11 is Figure 5.")
    q9 = table_q("sq", 4, 5, [14, 17, 19], " 14 adds only 1.")
    cv = [cnt("ctr", k) for k in range(1, 6)]
    q10 = nums_mcq(fig(tov_svg([1, 2, 3, 4], cv[:4], HEADS("ctr"))) +
                   "This table shows a shape pattern. How many counters are in Figure 5?", cv[4], [9, 5, 7],
                   "The table goes down by 3 each time: %s. Figure 5 has <b>%d</b> counters. "
                   "9 goes the wrong way. 5 is the figure number." % (lst(cv), cv[4]))
    q11 = which_q("sq", 13, [13, 5, 3], " 13 is the number of sticks, not the figure number.")
    q12 = which_q("dots", 30, [30, 7, 5], " Count by 5s. 30 is the number of dots, not the figure number.")
    q13 = which_q("dec", 4, [4, 6, 2], " The pattern is decreasing, so the figures get smaller.")
    q14 = rule_q("L", ["Start at 1 and add 1 each time", "Start at 2 and add 2 each time",
                       "Start at 1 and add 3 each time"])
    q15 = rule_q("dec", ["Start at 12 and add 2 each time", "Start at 12 and subtract 1 each time",
                         "Start at 10 and subtract 2 each time"], " The figures get smaller, so the rule subtracts.")
    q16 = rule_q("towers", ["Start at 3 and add 3 each time", "Start at 6 and add 6 each time",
                            "Start at 6 and subtract 3 each time"], " 6 is where it starts. Each new tower adds 3.")
    q17 = tmiss("tri", 2, [6, 8, 10])
    q18 = tmiss("ctr", 3, [7, 4, 5], " 4 is the figure number.")
    tv = [cnt("towers", k) for k in (1, 2, 3, 4)]
    q19 = mcq(fig(tov_svg([1, 2, 3, 4], tv, HEADS("towers"))) + "In this table, 12 is under 3. What does that mean?",
              "Figure 3 has 12 cubes", ["Figure 12 has 3 cubes", "Each figure adds 12 cubes", "Each figure adds 3 cubes"],
              "Read down the column: the figure number is on top and the number of cubes is below it. "
              "So <b>Figure 3 has 12 cubes</b>.")
    st = [cnt("stairs", k) for k in range(1, 6)]
    q20 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 4?", st[3],
                   [8, 9, 12],
                   "Count: 1, 3, 6. The jumps are +2, then +3. Each jump is 1 more than the last, so the next jump is +4. "
                   "6 + 4 = <b>10</b>. 8 uses only the first step (+2).")
    out = [q1, q2, q3, q4, q14, q7, q5, q6, q15, q8, q19, q9, q10, q16, q11, q17, q12, q13, q18, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Shape patterns with tables", "items": out}


# ============================================================ set 4: write the rule in words
def set_rules():
    def rr(nums, wrong, extra=""):
        assert is_pattern(nums)
        d = nums[1] - nums[0]
        e = "The pattern starts at %d. %d %s %d = %d. The jump is the same every time, so the rule is <b>%s</b>.%s" % (
            nums[0], nums[0], "+" if d > 0 else MINUS, abs(d), nums[1], rule_text(nums[0], d).lower(), extra)
        return mcq(track(nums) + "Which rule describes this pattern in words?", rule_text(nums[0], d),
                   [rule_text(s, k) for s, k in wrong], e)

    q1 = rr([3, 6, 9, 12], [(0, 3), (3, -3), (3, 6)], " The first number is 3, so start at 3.")
    q2 = rr([40, 38, 36, 34], [(40, 2), (38, -2), (40, -4)], " The numbers get smaller, so the rule subtracts.")
    q3 = rr([11, 21, 31, 41], [(11, 1), (11, 11), (1, 10)], " Only the tens digit goes up, so the jump is 10.")
    q4 = rr([95, 90, 85, 80], [(95, 5), (95, -10), (90, -5)])
    q5 = rr([250, 300, 350, 400], [(250, 5), (300, 50), (250, -50)])
    q6 = rr([777, 677, 577, 477], [(777, -10), (777, 100), (677, -100)], " Only the hundreds digit goes down.")

    def trule(heads, top, bot, wrong, extra):
        d = bot[1] - bot[0]
        e = "Read the bottom row: %s. It starts at %d and changes by %s each time. The rule is <b>%s</b>.%s" % (
            lst(bot), bot[0], jump(d), rule_text(bot[0], d).lower(), extra)
        return mcq(fig(tov_svg(top, bot, heads)) + "What is the rule for the bottom row?", rule_text(bot[0], d),
                   [rule_text(s, k) for s, k in wrong], e)

    q7 = trule(["Week", "Books read"], [1, 2, 3, 4], [7, 14, 21, 28], [(1, 7), (7, 1), (7, 14)],
               " The top row goes up by 1, but that is the week number.")
    q8 = trule(["Day", "Apples left"], [1, 2, 3, 4], [30, 26, 22, 18], [(30, 4), (30, -1), (26, -4)],
               " The apples get fewer, so the rule subtracts.")
    q9 = mcq("Owen says the rule for 4, 7, 10, 13 is “start at 4 and add 4 each time.” What is his mistake?",
             "He used the first number as the jump",
             ["The pattern is decreasing", "He should add 7 each time", "He has no mistake"],
             "4 is where the pattern starts. The jump is 7 − 4 = 3. The rule is start at 4 and add 3 each time. "
             "<b>He used the first number as the jump</b>.")
    q10 = mcq("Leah says the rule for 60, 55, 50, 45 is “start at 60 and add 5 each time.” What is her mistake?",
              "The numbers get smaller, so she must subtract",
              ["She should start at 45", "The jump is 10", "She has no mistake"],
              "The pattern is decreasing. The rule is start at 60 and subtract 5 each time. "
              "<b>The numbers get smaller, so she must subtract</b>.")
    q11 = mcq("Ryan says the rule for 2, 5, 8, 12 is “start at 2 and add 3 each time.” Is he right?",
              "No, 8 + 3 is 11, not 12",
              ["Yes, 2 + 3 = 5", "Yes, 5 + 3 = 8", "No, the rule is add 4"],
              "Check every jump, not only the first: 2 + 3 = 5, 5 + 3 = 8, but 8 + 3 = 11. "
              "So <b>no, 8 + 3 is 11, not 12</b>. This is not a pattern with the same jump.")
    q12 = mcq(fig(nline_svg(120, [15] * 3)) + "Which rule matches the jumps on the number line?",
              "Start at 120 and add 15 each time",
              ["Start at 120 and add 10 each time", "Start at 135 and add 15 each time",
               "Start at 120 and subtract 15 each time"],
              "The number line starts at 120. Each jump is +15. The rule is <b>start at 120 and add 15 each time</b>.")
    q13 = mcq(fig(pattern_svg("tables")) + "Which rule tells the number of chairs?", "Start at 4 and add 2 each time",
              ["Start at 4 and add 4 each time", "Start at 1 and add 1 each time", "Start at 2 and add 2 each time"],
              "Count the chairs: 4, 6, 8. Each new table adds 2 chairs. The rule is <b>start at 4 and add 2 each time</b>. "
              "“Start at 1 and add 1” counts the tables, not the chairs.")
    q14 = mcq(fig(pattern_svg("ctr")) + "Which rule tells the number of counters?", "Start at 15 and subtract 3 each time",
              ["Start at 15 and add 3 each time", "Start at 15 and subtract 1 each time",
               "Start at 3 and add 3 each time"],
              "Count: 15, 12, 9. Each figure loses one column of 3. The rule is <b>start at 15 and subtract 3 each time</b>.")
    q15 = mcq("Which pattern matches the rule “start at 90 and subtract 15 each time”?", "90, 75, 60, 45",
              ["90, 105, 120, 135", "75, 60, 45, 30", "90, 85, 80, 75"],
              "90 − 15 = 75, 75 − 15 = 60, 60 − 15 = 45. The pattern is <b>90, 75, 60, 45</b>. "
              "90, 105, 120, 135 goes the wrong way.")
    q16 = mcq("Which pattern matches the rule “start at 208 and add 100 each time”?", "208, 308, 408, 508",
              ["208, 218, 228, 238", "208, 209, 210, 211", "308, 408, 508, 608"],
              "Adding 100 changes only the hundreds digit: <b>208, 308, 408, 508</b>. 208, 218, 228 adds 10.")
    q17 = mcq("Kai saves money each week. He has $4, then $9, then $14, then $19. What is the rule?",
              "Start at $4 and add $5 each week",
              ["Start at $4 and add $4 each week", "Start at $5 and add $4 each week",
               "Start at $19 and add $5 each week"],
              "$4 + $5 = $9, $9 + $5 = $14, $14 + $5 = $19. The rule is <b>start at $4 and add $5 each week</b>.")
    q18 = mcq(track([1, 2, 4, 7, 11]) + "Which rule describes this pattern?",
              "Start at 1 and add 1, then 2, then 3, then 4",
              ["Start at 1 and add 1 each time", "Start at 1 and add 2 each time", "Start at 1 and add 4 each time"],
              "Check every jump: +1, +2, +3, +4. The jump gets 1 bigger each time. "
              "“Add 1 each time” uses only the first step.")
    q19 = mcq("Pattern A is 5, 10, 15, 20. Pattern B is 20, 15, 10, 5. Which is true?",
              "A adds 5 each time and B subtracts 5 each time",
              ["Both add 5 each time", "A adds 5 each time and B subtracts 10 each time", "Both subtract 5 each time"],
              "A gets bigger: +5 each time. B gets smaller: −5 each time. So <b>A adds 5 each time and B subtracts 5 each time</b>.")
    nad = seq(360, -30, 6)
    assert 320 not in nad and all(v in nad for v in (330, 300, 270))
    q20 = mcq("Nadia’s rule is “start at 360 and subtract 30 each time.” Which number is NOT in her pattern?", "320",
              ["330", "300", "270"],
              "Her pattern is %s … The numbers 330, 300 and 270 are in it. <b>320</b> is not." % lst(nad))
    out = [q1, q2, q3, q4, q5, q6, q7, q12, q8, q13, q9, q14, q10, q15, q16, q17, q11, q19, q18, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Write the pattern rule in words", "items": out}


# ============================================================ set 5: predictions and real-life patterns
def set_predict(P):
    def story(t, ans, cands, e, pic="", unit=None):
        d = P.next()
        return nums_mcq(pic + t.format(**d), ans, cands, e.format(**d), unit or str)

    dol = lambda v: "$%d" % v
    cm = lambda v: "%d cm" % v
    q1 = story("The table shows apples in bags. How many apples are in 10 bags?", 60, [54, 66, 16],
               "Each bag adds 6 apples: 6, 12, 18, 24 … 54, <b>60</b>. 54 is 9 bags.",
               fig(tov_svg([1, 2, 3, 4], [6, 12, 18, 24], ["Bags", "Apples"])))
    q2 = story("A Grade 3 class collects money for the Terry Fox Run. They have $35 after week 1, $60 after week 2 "
               "and $85 after week 3. The pattern continues. How much do they have after week 5?", 135, [110, 160, 125],
               "The rule is start at $35 and add $25 each week: $35, $60, $85, $110, <b>$135</b>. $110 is week 4.",
               unit=dol)
    q3 = story("A class counts salmon in a creek. They see 12 on day 1, 20 on day 2 and 28 on day 3. "
               "The pattern continues. How many salmon will they see on day 6?", 52, [36, 60, 48],
               "The rule is add 8 each day: 12, 20, 28, 36, 44, <b>52</b>. 36 is only the next day.")
    q4 = story("{n} has a water bottle with 900 mL of water. {He} drinks 150 mL each hour. "
               "How much water is left after 4 hours?", 300, [750, 450, 600],
               "Start at 900 and subtract 150 each hour: 750, 600, 450, <b>300 mL</b>. 750 is only the first hour. 450 is 3 hours.",
               unit=lambda v: "%d mL" % v)
    q5 = story("A rain barrel in Vancouver has 80 L of water. {n} uses 15 L each day to water the garden. "
               "How much water is left after 5 days?", 5, [65, 20, 155],
               "Start at 80 and subtract 15 each day: 65, 50, 35, 20, <b>5 L</b>. 155 goes the wrong way.",
               unit=lambda v: "%d L" % v)
    q6 = mcq("A ferry leaves every 2 hours: 7:00 a.m., 9:00 a.m., 11:00 a.m. … When does the 5th ferry leave?",
             "3:00 p.m.", ["1:00 p.m.", "5:00 p.m.", "4:00 p.m."],
             "Add 2 hours each time: 7:00 a.m., 9:00 a.m., 11:00 a.m., 1:00 p.m., <b>3:00 p.m.</b> "
             "1:00 p.m. is the 4th ferry.")
    q7 = story("The school gym has 240 chairs set up. Students stack 30 chairs each minute. "
               "How many chairs are still set up after 5 minutes?", 90, [210, 120, 390],
               "Start at 240 and subtract 30 each minute: 210, 180, 150, 120, <b>90</b>. 390 goes the wrong way.")
    q8 = story("{n} goes skiing at Whistler. {He} skis 3 runs on day 1, 5 runs on day 2 and 7 runs on day 3. "
               "The pattern continues. How many runs does {he} ski on day 6?", 13, [9, 15, 18],
               "Start at 3 and add 2 each day: 3, 5, 7, 9, 11, <b>13</b>. 9 is only day 4. 15 is day 7.")
    q9 = mcq("A SkyTrain leaves the station every 5 minutes: 8:00 a.m., 8:05 a.m., 8:10 a.m. … "
             "When does the 6th train leave?", "8:25 a.m.", ["8:30 a.m.", "8:15 a.m.", "8:20 a.m."],
             "Add 5 minutes each time: 8:00, 8:05, 8:10, 8:15, 8:20, <b>8:25 a.m.</b> From the 1st to the 6th train "
             "there are 5 jumps, not 6.")
    p = seq(7, 4, 10)
    q10 = nums_mcq(track(p[:4] + [None]) + "The rule is “start at 7 and add 4 each time.” What is the 10th number?",
                   p[9], [47, 40, 39],
                   "From the 1st to the 10th number there are 9 jumps. 9 × 4 = 36. 7 + 36 = <b>43</b>. "
                   "47 makes 10 jumps, one too many.")
    q11 = story("One table seats 4 people. Two tables pushed together seat 6. Three tables seat 8. "
                "How many tables are needed to seat 14 people?", 6, [7, 4, 5],
                "Start at 4 and add 2 for each table: 4, 6, 8, 10, 12, 14. That is <b>6</b> tables. "
                "7 is 14 ÷ 2, but the first table seats 4, not 2.",
                fig(pattern_svg("tables")), unit=lambda v: "%d tables" % v)
    q12 = story("{n} has 45 hockey cards. {He} gives 5 cards away each week. "
                "After how many weeks will {he} have 20 cards?", 5, [25, 4, 6],
                "Count back by 5s: 40, 35, 30, 25, 20. That is <b>5</b> weeks. 25 is how many cards {he} gives away.",
                unit=lambda v: "%d weeks" % v)
    q13 = story("A bean plant in {n}’s class is 5 cm tall. It grows 3 cm each week. How tall is it after 6 weeks?",
                23, [8, 18, 26],
                "Start at 5 and add 3 each week: 8, 11, 14, 17, 20, <b>23 cm</b>. 8 is only 1 week. "
                "18 forgets the 5 cm it started with.", unit=cm)
    d = P.next()
    q14 = mcq("{n} counts back by 10s from 500: 500, 490, 480 … Will {he} say 405?".format(**d),
              "No, every number will end in 0",
              ["Yes, 405 is less than 500", "Yes, 405 has a 0 in it", "No, {he} will stop at 450".format(**d)],
              "Counting back by 10s from 500 changes only the tens and hundreds. Every number ends in 0. "
              "405 ends in 5, so <b>no</b>.")
    q15 = story("One paper cup is 10 cm tall. Each cup added to the stack makes it 2 cm taller. "
                "How tall is a stack of 6 cups?", 20, [12, 22, 60],
                "Start at 10 and add 2 for each new cup: 10, 12, 14, 16, 18, <b>20 cm</b>. "
                "6 cups means 5 cups added. 60 is 6 × 10, but cups fit inside each other.", unit=cm)
    d = P.next()
    q16 = mcq("{n} builds a cube pattern: 4, 7, 10 cubes. {He} has 30 cubes. Can {he} build Figure 9?".format(**d),
              "Yes, Figure 9 needs 28 cubes",
              ["No, Figure 9 needs 31 cubes", "No, Figure 9 needs 36 cubes", "Yes, Figure 9 needs 27 cubes"],
              "Start at 4 and add 3 each time. From Figure 1 to Figure 9 there are 8 jumps: 8 × 3 = 24. "
              "4 + 24 = 28. 28 is less than 30, so <b>yes</b>.")
    assert seq(4, 3, 9)[8] == 28
    q17 = story("A family in Prince George has 96 logs of firewood. They burn 8 logs each night. "
                "How many logs are left after 7 nights?", 40, [88, 48, 152],
                "Start at 96 and subtract 8 each night: 88, 80, 72, 64, 56, 48, <b>40</b>. 88 is only 1 night. "
                "48 is 6 nights.")
    q18 = story("The table shows the cost to rent a kayak. The pattern continues. How much does it cost for 6 hours?",
                40, [90, 45, 35],
                "The cost goes up by $5 each hour: $15, $20, $25, $30, $35, <b>$40</b>. $90 is 6 × $15, "
                "but each extra hour costs only $5.",
                fig(tov_svg([1, 2, 3], ["$15", "$20", "$25"], ["Hours", "Cost"])), unit=dol)
    q19 = mcq("{n} has lacrosse practice every 7 days. The first three practices are on May 3, May 10 and May 17. "
              "What is the date of the 4th practice?".format(**P.next()),
              "May 24", ["May 25", "May 31", "May 18"],
              "Add 7 days each time: 3, 10, 17, <b>24</b>. May 31 is the 5th practice. May 18 adds only 1 day.")
    q20 = story("A garden centre in Kelowna has 900 tulip bulbs. It sells 75 bulbs each day. "
                "How many bulbs are left after 4 days?", 600, [525, 825, 675],
                "Start at 900 and subtract 75 each day: 825, 750, 675, <b>600</b>. 825 is only 1 day. 525 is 5 days.")
    assert 900 - 4 * 75 == 600 and 240 - 5 * 30 == 90 and 96 - 7 * 8 == 40 and 80 - 5 * 15 == 5
    assert 12 + 5 * 8 == 52 and 35 + 4 * 25 == 135 and 5 + 6 * 3 == 23 and 3 + 5 * 2 == 13
    out = [q1, q3, q2, q8, q6, q9, q7, q13, q4, q5, q10, q12, q11, q15, q14, q19, q18, q17, q16, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Predictions and real-life patterns", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Increasing and decreasing patterns</h2>"
        "<p>In an <b>increasing pattern</b>, the numbers get bigger by the same amount each time. "
        "In a <b>decreasing pattern</b>, they get smaller by the same amount each time. "
        "Find the jump between two numbers next to each other. Then check that the same jump works every time.</p>"
        "<figure class='sn-fig'>" + nline_svg(150, [25, 25, 25], ticks=["150", "175", "200", "225"]) +
        "<figcaption>150, 175, 200, 225 is increasing. The rule is start at 150 and add 25 each time.</figcaption></figure>"
        "<h2>The pattern rule in words</h2>"
        "<p>A <b>pattern rule</b> says where to start and what to do each time. "
        "For 60, 55, 50, 45 the rule is <b>start at 60 and subtract 5 each time</b>.</p>"
        "<h2>Shape patterns and tables</h2>"
        "<p>Build or draw each figure and count. Put the counts in a table. The top row is the figure number. "
        "The bottom row is how many objects.</p>"
        "<figure class='sn-fig'>" + pattern_svg("ctr") +
        "<figcaption>Figure 1 has 15 counters, Figure 2 has 12, Figure 3 has 9.</figcaption></figure>"
        + table(["Figure number", "1", "2", "3", "4"], [["Number of counters", "15", "12", "9", "6"]]) +
        "<p>Each figure loses 3 counters. The rule is <b>start at 15 and subtract 3 each time</b>.</p>"
        + ex("Missing number", "805, 795, ☐, 775",
             "The rule is subtract 10. 795 − 10 = 785. Check: 785 − 10 = 775.", "785")
        + ex("Make a prediction", "Start at 7 and add 4 each time. What is the 10th number?",
             "From the 1st number to the 10th there are 9 jumps. 9 × 4 = 36. 7 + 36 = 43.", "43") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using only the first step: 2, 5, 8, 12 is “add 3”", "Check every jump: 8 + 3 is 11, not 12"],
            ["Going the wrong way: 50, 45, 40, then 45", "The numbers get smaller, so subtract: 35"],
            ["Using the first number as the jump: 4, 7, 10 is “add 4”", "Start at 4 and add 3 each time"],
            ["Mixing up the figure number and the number of objects", "The figure number is on top of the table. The count is below it"],
            ["10 jumps for the 10th number", "From the 1st to the 10th number there are 9 jumps"],
        ])
    )


FAQ = [
    {"q": "What patterns do Grade 3 students learn in BC math?",
     "a": "In the BC curriculum (Patterning), Grade 3 students work with increasing and decreasing patterns. They describe pattern rules using words and numbers, show patterns with objects and tables, and make predictions."},
    {"q": "What is the difference between an increasing and a decreasing pattern?",
     "a": "An increasing pattern gets bigger by the same amount each time, like 120, 130, 140. A decreasing pattern gets smaller by the same amount each time, like 300, 280, 260."},
    {"q": "How do you write a pattern rule in Grade 3?",
     "a": "Say where the pattern starts and what happens each time, for example “start at 60 and subtract 5 each time.” Check that the same jump works for every pair of numbers, not just the first two."},
    {"q": "How can I practise patterns with my child at home?",
     "a": "Build growing and shrinking towers with blocks or Lego, then count each one and write the numbers in a table. Count by 5s, 10s and 25s forwards and backwards, and ask your child to predict the next number and explain the rule."},
]


def gen():
    rnd = random.Random(53806)
    P = People(rnd)
    sets = [set_increasing(), set_decreasing(), set_shapes(), set_rules(), set_predict(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "increasing-and-decreasing-patterns",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Increasing and Decreasing Patterns: Pattern Rules, Tables and Predictions",
        "seo_title": "Grade 3 Increasing and Decreasing Patterns Worksheets: Pattern Rules and Tables (BC Math)",
        "short_title": "Increasing and decreasing patterns",
        "domain": "Patterning",
        "standard_code": "Grade 3: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Increasing and decreasing patterns",
        "meta_desc": "Free Grade 3 math worksheets on increasing and decreasing patterns: extend number patterns to 1000, build shape patterns with tables, write the pattern rule in words and numbers, and make predictions. 100 questions with an answer key, matched to the BC curriculum.",
        "key_big": "A pattern rule tells where to start and what to do each time.",
        "key_sub": "Find the jump and check it works every time. If the numbers get bigger, add. If they get smaller, subtract: 60, 55, 50 is “start at 60 and subtract 5 each time.” For the 10th number, there are 9 jumps from the 1st.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number track|number line|shape pattern|table of values)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
