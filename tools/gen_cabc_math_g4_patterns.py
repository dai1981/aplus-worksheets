# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: Increasing and decreasing patterns (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g4_patterns.py
Increasing and decreasing number patterns to 10 000 and their pattern rules, shape patterns with
tables (figure number -> count), input/output tables and rule boxes (algebraic relationships among
quantities), predicting later terms and real-life patterns in BC settings.
Wrong answers come from real mistakes: using only the first step, mixing up the figure number and
the count, going the wrong way, changing the wrong digit, one jump too many for the 10th term,
reading along the Out row instead of In -> Out, and using the start number as the jump.
Every answer is computed and checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
CUBE = "#8fc7a0"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#a0522d"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NB = " "


# ------------------------------------------------------------ helpers
def f(n):
    """BC/SI style: 4 digits no separator, 5+ digits grouped with a no-break space."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return (MINUS if n < 0 else "") + s


def mcq(q, correct, cands, e):
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
    return ", ".join(f(x) for x in xs)


def seq(start, step, n):
    return [start + step * k for k in range(n)]


def jump(d):
    return ("+" + f(d)) if d > 0 else (MINUS + f(-d))


def pm(d):
    return "+" if d > 0 else MINUS


def rule_text(start, d):
    if d > 0:
        return "Start at %s and add %s each time" % (f(start), f(d))
    return "Start at %s and subtract %s each time" % (f(start), f(-d))


def is_pattern(xs):
    d = xs[1] - xs[0]
    return d != 0 and all(xs[i + 1] - xs[i] == d for i in range(len(xs) - 1))


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def tw(s, fs):
    """Rough width of bold Arial text."""
    return sum(0.36 if ch in "  " else (0.62 if ch.isdigit() else 0.66) for ch in s) * fs


# ------------------------------------------------------------ number track, number line, tables
def track_svg(nums):
    labels = ["?" if v is None else f(v) for v in nums]
    cw = max(52, int(max(tw(t, 17) for t in labels) + 16))
    m, TH = 4, 36
    W, H = 2 * m + len(nums) * cw, 2 * m + TH
    s = []
    for i, t in enumerate(labels):
        x = m + i * cw
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, cw, TH, FILL if t == "?" else "#ffffff", GREEN))
        s.append(text(x + cw / 2, m + 24, t, 17, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number track")


def track(nums, hide=()):
    return fig(track_svg([None if k in hide else v for k, v in enumerate(nums)]))


def nline_svg(start, jumps, ticks=None):
    if ticks is None:
        ticks = [f(start)] + [None] * (len(jumps) - 1) + ["?"]
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
        f(start), ", ".join(jl).replace(MINUS, "minus ")))


def tov_svg(top, bot, heads, label="table of values"):
    """Two-row table. '?' shows red. Numbers are formatted."""
    def lab(v):
        return v if isinstance(v, str) else f(v)
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


def io_svg(ins, outs):
    return tov_svg(ins, outs, ["In", "Out"], "input output table")


def machine_svg(parts):
    """parts: [in, rule, (rule,) out]. Values in white boxes, rules in green boxes, arrows between."""
    m, gap, BH, top = 4, 26, 40, 22
    widths = []
    for i, p in enumerate(parts):
        rule = 0 < i < len(parts) - 1
        widths.append(max(62 if rule else 52, int(tw(p, 18) + 24)))
    W = 2 * m + sum(widths) + gap * (len(parts) - 1)
    H = top + BH + m
    s, x = [], m
    for i, (p, w) in enumerate(zip(parts, widths)):
        rule = 0 < i < len(parts) - 1
        y = top
        if rule:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, BH, FILL, GREEN))
            s.append(text(x + w / 2, y + 27, p, 19, col=GREEN))
        else:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                     % (x, y, w, BH, INK))
            s.append(text(x + w / 2, y + 27, p, 19, col=RED if p == "?" else INK))
            s.append(text(x + w / 2, top - 6, "In" if i == 0 else "Out", 14))
        if i < len(parts) - 1:
            ax1, ax2, ay = x + w + 3, x + w + gap - 3, top + BH / 2
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (ax1, ay, ax2 - 4, ay, INK))
            s.append("<polygon points='%d,%.1f %d,%.1f %d,%.1f' fill='%s'/>" % (ax2, ay, ax2 - 8, ay - 5, ax2 - 8, ay + 5, INK))
        x += w + gap
    return svg_wrap(W, H, "".join(s), "rule machine")


# ------------------------------------------------------------ shape patterns
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


# ------------------------------------------------------------ shared question builders
def nxt(nums, cands, extra=""):
    assert is_pattern(nums)
    d = nums[1] - nums[0]
    a = nums[-1] + d
    e = "Each number is %s %s than the one before. %s %s %s = <b>%s</b>.%s" % (
        f(abs(d)), "more" if d > 0 else "less", f(nums[-1]), pm(d), f(abs(d)), f(a), extra)
    return nums_mcq(track(nums + [None]) + "What number comes next?", a, cands, e)


def rq(nums, wrong, extra=""):
    assert is_pattern(nums)
    d = nums[1] - nums[0]
    for s0, k in wrong:
        assert seq(s0, k, len(nums)) != nums
    e = "%s %s %s = %s, and every jump is the same. The rule is <b>%s</b>.%s" % (
        f(nums[0]), pm(d), f(abs(d)), f(nums[1]), rule_text(nums[0], d).lower(), extra)
    return mcq(track(nums) + "What is the pattern rule?", rule_text(nums[0], d),
               [rule_text(s, k) for s, k in wrong], e)


def miss(nums, i, cands, extra=""):
    assert is_pattern(nums)
    d = nums[1] - nums[0]
    a = nums[i]
    if i == 0:
        e = "The rule is %s. Go back one step from %s: %s %s %s = <b>%s</b>." % (
            jump(d), f(nums[1]), f(nums[1]), MINUS if d > 0 else "+", f(abs(d)), f(a))
    else:
        e = "The rule is %s. %s %s %s = <b>%s</b>." % (jump(d), f(nums[i - 1]), pm(d), f(abs(d)), f(a))
        if i < len(nums) - 1:
            e += " Check: %s %s %s = %s." % (f(a), pm(d), f(abs(d)), f(nums[i + 1]))
    return nums_mcq(track(nums, (i,)) + "What number is missing?", a, cands, e + extra)


# ============================================================ set 1: increasing patterns
def set_increasing():
    q1 = nxt([12, 16, 20, 24], [25, 32, 26], " 25 only adds 1.")
    q2 = nxt([35, 40, 45, 50], [51, 60, 56])
    q3 = nxt([120, 130, 140, 150], [151, 250, 170], " Only the tens digit changes.")
    q4 = nxt([250, 500, 750], [760, 1250, 800], " Four 250s make 1000.")
    q5 = nxt([1200, 1300, 1400], [1401, 2400, 1410], " Only the hundreds digit changes. 2400 changes the thousands digit.")
    q6 = nxt([2025, 3025, 4025], [4026, 4125, 6025], " Only the thousands digit changes.")
    q7 = nxt([6, 13, 20, 27], [33, 28, 35], " Check the jump: 13 − 6 = 7, not 6.")
    q8 = nxt([475, 500, 525, 550], [600, 560, 551], " Counting by 25s, the numbers end in 00, 25, 50 or 75.")
    q9 = nxt([1950, 1975, 2000], [2050, 2005, 2100], " 2050 adds 50, not 25.")
    q10 = nxt([9700, 9800, 9900], [1000, 9901, 9990],
              " 99 hundreds + 1 hundred = 100 hundreds. Write it with a space: 10 000. 1000 is missing a zero.")
    q11 = rq([8, 14, 20, 26], [(8, 8), (6, 6), (14, 6)], " 8 is where the pattern starts. It is not the jump.")
    q12 = rq([300, 450, 600, 750], [(300, 300), (300, 100), (150, 150)])
    q13 = rq([1015, 1040, 1065, 1090], [(1015, 15), (1015, 20), (1040, 25)], " 1040 − 1015 = 25.")
    q14 = miss([64, 72, 80, 88, 96], 2, [73, 81, 84])
    q15 = miss([500, 540, 580, 620], 0, [580, 520, 510], " Going back means subtract, not add.")
    q16 = nums_mcq(track([3, 4, 6, 9, 13, None]) + "What number comes next?", 18, [17, 14, 19],
                   "The jumps are +1, +2, +3, +4. Each jump is 1 more than the last, so the next jump is +5. "
                   "13 + 5 = <b>18</b>. 14 uses only the first step (+1). 17 adds +4 again.")
    q17 = nums_mcq(track([5, 10, 20, 40, None]) + "What number comes next?", 80, [45, 60, 50],
                   "The jumps are +5, +10, +20. Each number is double the one before: 40 × 2 = <b>80</b>. "
                   "45 uses only the first step (+5).")
    want = seq(150, 75, 4)
    q18 = mcq("Which pattern follows the rule “Start at 150 and add 75 each time”?", lst(want),
              ["75, 150, 225, 300", "150, 175, 200, 225", "150, 225, 300, 365"],
              "150 + 75 = 225, 225 + 75 = 300, 300 + 75 = 375. The pattern is <b>%s</b>. "
              "75, 150, … starts at the jump, not at 150." % lst(want))
    q19 = nums_mcq("Olivia counts by 250s from 0: 0, 250, 500, 750, 1000 … Which number will she say?", 2250,
                   [2200, 2025, 2150],
                   "Counting by 250s from 0, every number ends in 000, 250, 500 or 750. Only <b>2250</b> ends that way. "
                   "2025 ends in 25, not 250.")
    bad = [1100, 1250, 1400, 1500, 1700]
    assert seq(1100, 150, 5)[3] == 1550
    q20 = nums_mcq(track(bad) + "One number in this pattern is wrong. Which one?", 1500, [1250, 1400, 1700],
                   "The rule is +150: 1100, 1250, 1400, 1550, 1700. <b>1500</b> should be 1550.")
    out = [q1, q2, q3, q7, q4, q8, q14, q11, q5, q6, q12, q15, q9, q13, q10, q18, q16, q17, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Increasing patterns and the pattern rule", "items": out}


# ============================================================ set 2: decreasing patterns
def set_decreasing():
    q1 = nxt([50, 45, 40, 35], [34, 40, 25], " The numbers get smaller, so do not go back up to 40.")
    q2 = nxt([96, 88, 80, 72], [71, 80, 62])
    q3 = nxt([900, 800, 700], [699, 800, 690], " Only the hundreds digit changes.")
    q4 = nxt([1000, 975, 950, 925], [924, 950, 875], " 875 subtracts 50, not 25.")
    q5 = nxt([4500, 4000, 3500], [3400, 4000, 2500], " 4000 goes the wrong way.")
    q6 = nxt([8250, 7250, 6250], [6150, 7250, 6240], " Only the thousands digit changes.")
    q7 = nxt([10000, 9000, 8000], [6000, 9000, 7900], " 9000 goes the wrong way. 7900 subtracts only 100.")
    q8 = nxt([3005, 2905, 2805], [2795, 2905, 2704], " Only the hundreds digit changes.")
    q9 = rq([84, 77, 70, 63], [(84, 7), (84, -6), (77, -7)], " The numbers get smaller, so the rule subtracts.")
    q10 = rq([2400, 2200, 2000, 1800], [(2400, 200), (2400, -100), (2200, -200)])
    q11 = mcq(track([5000, 4750, 4500, 4250]) + "How does this pattern change?", "decreasing by 250 each time",
              ["increasing by 250 each time", "decreasing by 25 each time", "decreasing by 750 each time"],
              "The numbers get smaller, so the pattern is decreasing. 5000 − 250 = 4750, 4750 − 250 = 4500. "
              "It is <b>decreasing by 250 each time</b>.")
    q12 = nums_mcq(fig(nline_svg(1200, [-150] * 3)) + "Start at 1200. Make the jumps. Where do you land?", 750,
                   [1650, 1050, 900], "Count back by 150s 3 times: 1050, 900, <b>750</b>. 1650 goes the wrong way.")
    q13 = nums_mcq(fig(nline_svg(3000, [-500] * 4)) + "Start at 3000. Make the jumps. Where do you land?", 1000,
                   [5000, 1500, 500], "Count back by 500s 4 times: 2500, 2000, 1500, <b>1000</b>. 1500 is only 3 jumps.")
    q14 = miss([7200, 7100, 7000, 6900], 2, [7090, 6800, 7150], " 7090 subtracts only 10.")
    q15 = miss([680, 630, 580, 530], 0, [580, 640, 730],
               " The pattern goes down, so the number before 630 is bigger.")
    seq16 = [960, 840, 720, 600, 480]
    assert is_pattern(seq16)
    q16 = mcq(track(seq16, (2, 4)) + "Which two numbers are missing, in order?", "720, 480",
              ["740, 500", "720, 500", "480, 720"],
              "The rule is −120. 840 − 120 = 720 and 600 − 120 = 480. The missing numbers are <b>720, 480</b>. "
              "740, 500 subtracts only 100. Write the numbers in order from left to right.")
    q17 = nums_mcq(track([100, 90, 81, 73, None]) + "What number comes next?", 66, [63, 65, 64],
                   "The jumps are −10, −9, −8. Each jump is 1 less, so the next jump is −7. 73 − 7 = <b>66</b>. "
                   "63 uses only the first step (−10).")
    want = seq(2000, -250, 4)
    q18 = mcq("Which pattern follows the rule “Start at 2000 and subtract 250 each time”?", lst(want),
              ["2000, 2250, 2500, 2750", "2000, 1975, 1950, 1925", "2000, 1750, 1550, 1350"],
              "2000 − 250 = 1750, 1750 − 250 = 1500, 1500 − 250 = 1250. The pattern is <b>%s</b>. "
              "2000, 2250, … adds instead of subtracting." % lst(want))
    bad = [4800, 4600, 4400, 4100, 4000]
    assert seq(4800, -200, 5)[3] == 4200
    q19 = nums_mcq(track(bad) + "One number in this pattern is wrong. Which one?", 4100, [4600, 4400, 4000],
                   "The rule is −200: 4800, 4600, 4400, 4200, 4000. <b>4100</b> should be 4200.")
    q20 = nums_mcq("Hana counts back by 25s from 1000: 1000, 975, 950 … Which number will she say?", 875,
                   [860, 905, 940],
                   "Counting back by 25s from 1000, every number ends in 00, 25, 50 or 75: 925, 900, <b>875</b>. "
                   "860, 905 and 940 do not end that way.")
    out = [q1, q2, q3, q4, q9, q5, q14, q6, q12, q10, q8, q15, q11, q7, q13, q18, q19, q16, q17, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Decreasing patterns", "items": out}


# ============================================================ set 3: shape patterns and tables
def HEADS(nm):
    return ["Figure number", "Number of " + thing(nm)]


def set_shapes():
    def d_of(nm):
        return cnt(nm, 2) - cnt(nm, 1)

    def next_q(nm, cands, extra=""):
        th = thing(nm)
        a, last, d = cnt(nm, 4), cnt(nm, 3), d_of(nm)
        e = "Count each figure: %s. Each figure has %d %s %s. %d %s %d = <b>%d</b> %s in Figure 4.%s" % (
            lst([cnt(nm, k) for k in (1, 2, 3)]), abs(d), "more" if d > 0 else "fewer", th,
            last, pm(d), abs(d), a, th, extra)
        return nums_mcq(fig(pattern_svg(nm)) + "The pattern keeps going. How many %s are in Figure 4?" % th, a, cands, e)

    def rule_q(nm, wrong, extra=""):
        d, s0 = d_of(nm), cnt(nm, 1)
        for a, b in wrong:
            assert (a, b) != (s0, d)
        e = "Figure 1 has %d %s. Count each figure: %s. The pattern rule is <b>%s</b>.%s" % (
            s0, thing(nm), lst([cnt(nm, k) for k in (1, 2, 3)]), rule_text(s0, d).lower(), extra)
        return mcq(fig(pattern_svg(nm)) + "What is the pattern rule for the number of %s?" % thing(nm),
                   rule_text(s0, d), [rule_text(a, b) for a, b in wrong], e)

    def table_q(nm, shown, k, cands, extra=""):
        th = thing(nm)
        vals = [cnt(nm, j) for j in range(1, k + 1)]
        d = d_of(nm)
        e = "The table goes up by %d each time. Keep going: %s. Figure %d has <b>%d</b> %s.%s" % (
            d, lst(vals[shown - 1:]), k, vals[-1], th, extra)
        return nums_mcq(fig(tov_svg(list(range(1, shown + 1)), vals[:shown], HEADS(nm))) +
                        "This table shows a shape pattern. How many %s are in Figure %d?" % (th, k),
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
    q2 = next_q("sq", [14, 16, 11], " 16 counts 4 sticks for every square, but squares next to each other share a stick.")
    q3 = next_q("tri", [8, 12, 11], " Count the sticks, not the triangles.")
    q4 = next_q("dec", [10, 7, 4], " This pattern is decreasing, so do not add.")
    q5 = next_q("tables", [9, 12, 16], " 16 counts 4 chairs for every table, but no chairs fit where tables touch.")
    q6 = table_q("sq", 4, 6, [22, 16, 24], " 24 is 6 × 4, but the jump is 3, not 4.")
    q7 = table_q("tri", 4, 8, [16, 15, 24], " 15 is Figure 7.")
    q8 = table_q("towers", 4, 7, [21, 27, 28], " 21 is Figure 6.")
    q9 = rule_q("sq", [(4, 4), (3, 3), (1, 3)], " 4 is how many sticks Figure 1 has. It is not the jump.")
    q10 = rule_q("tables", [(4, 4), (2, 2), (4, 6)])
    q11 = rule_q("dec", [(12, 2), (12, -1), (10, -2)], " The pattern gets smaller, so the rule subtracts.")
    q12 = which_q("sq", 22)
    q13 = which_q("tables", 20)
    tv = [cnt("towers", k) for k in range(1, 6)]
    q14 = mcq(fig(tov_svg([1, 2, 3, 4, 5], tv, HEADS("towers"))) + "In this table, 18 is under 5. What does that mean?",
              "Figure 5 has 18 cubes", ["Figure 18 has 5 cubes", "Each figure adds 18 cubes", "Each figure adds 5 cubes"],
              "Read down the column. The figure number is on top and the number of cubes is below. "
              "So <b>Figure 5 has 18 cubes</b>.")
    sv = [cnt("sq", k) for k in range(1, 11)]
    q15 = nums_mcq(fig(pattern_svg("sq")) + "The pattern keeps going. How many sticks are in Figure 10?", sv[9],
                   [34, 30, 40],
                   "Start at 4 and add 3 each time. From Figure 1 to Figure 10 there are 9 jumps: 9 × 3 = 27. "
                   "4 + 27 = <b>31</b>. 34 makes 10 jumps. 40 is 10 × 4.")
    tv2 = [cnt("tri", k) for k in range(1, 11)]
    q16 = nums_mcq(fig(pattern_svg("tri")) + "The pattern keeps going. How many sticks are in Figure 10?", tv2[9],
                   [20, 30, 23],
                   "Start at 3 and add 2 each time. From Figure 1 to Figure 10 there are 9 jumps: 9 × 2 = 18. "
                   "3 + 18 = <b>21</b>. 30 counts 3 sticks for every triangle, but triangles share sticks.")
    t3 = [cnt("tri", k) for k in (1, 2, 3)]
    q17 = nums_mcq(fig(pattern_svg("tri", hide=2)) + "Figure 2 is hidden. How many sticks are in Figure 2?", t3[1],
                   [4, 6, 10],
                   "Figure 1 has 3 sticks and Figure 3 has 7 sticks. The pattern grows by the same amount each time: "
                   "3, <b>5</b>, 7. The rule is add 2.")
    dv = [cnt("dots", k) for k in range(1, 6)]
    row = [v if k != 3 else "?" for k, v in enumerate(dv)]
    q18 = nums_mcq(fig(tov_svg([1, 2, 3, 4, 5], row, HEADS("dots"))) + "What number is missing from the table?", dv[3],
                   [16, 4, 22],
                   "The number of dots goes up by 5 each time: %s. The missing number is <b>%d</b>. "
                   "4 is the figure number, not the number of dots." % (lst(dv), dv[3]))
    st = [cnt("stairs", k) for k in range(1, 6)]
    q19 = nums_mcq(fig(pattern_svg("stairs")) + "The pattern keeps going. How many tiles are in Figure 5?", st[4],
                   [14, 9, 16],
                   "Count: 1, 3, 6. The jumps are +2, +3, so the next jumps are +4 and +5: 6, 10, <b>15</b>. "
                   "9 uses only the first step (+2) each time.")
    dec = [cnt("dec", k) for k in range(1, 7)]
    assert dec[5] == 2
    q20 = nums_mcq(fig(pattern_svg("dec")) + "The pattern keeps going. How many tiles are in Figure 6?", dec[5],
                   [0, 4, 22],
                   "Start at 12 and subtract 2 each time: %s. Figure 6 has <b>2</b> tiles. "
                   "22 goes the wrong way. 0 makes one jump too many." % lst(dec))
    out = [q1, q3, q2, q4, q5, q14, q9, q10, q6, q7, q11, q8, q18, q17, q12, q13, q15, q16, q20, q19]
    assert len({id(x) for x in out}) == 20
    return {"title": "Shape patterns with tables", "items": out}


# ============================================================ set 4: input/output tables and rule boxes
OPS = {"+": lambda a, b: a + b, MINUS: lambda a, b: a - b, "×": lambda a, b: a * b, "÷": lambda a, b: a // b}
WORD = {"+": "Add", MINUS: "Subtract", "×": "Multiply by", "÷": "Divide by"}


def ap(op, x, k):
    if op == "÷":
        assert x % k == 0
    return OPS[op](x, k)


def rname(op, k):
    return "%s %s" % (WORD[op], f(k))


def set_io():
    def out_q(x, op, k, cands, extra=""):
        a = ap(op, x, k)
        e = "Put %s into the rule: %s %s %s = <b>%s</b>.%s" % (f(x), f(x), op, f(k), f(a), extra)
        return nums_mcq(fig(machine_svg([f(x), "%s %s" % (op, f(k)), "?"])) + "What number comes out?", a, cands, e)

    def in_q(op, k, y, cands, extra=""):
        inv = {"+": MINUS, MINUS: "+", "×": "÷", "÷": "×"}[op]
        x = ap(inv, y, k)
        assert ap(op, x, k) == y
        e = "Work backward. Undo %s %s with %s %s: %s %s %s = <b>%s</b>. Check: %s %s %s = %s.%s" % (
            op, f(k), inv, f(k), f(y), inv, f(k), f(x), f(x), op, f(k), f(y), extra)
        return nums_mcq(fig(machine_svg(["?", "%s %s" % (op, f(k)), f(y)])) + "What number went in?", x, cands, e)

    def rule_q(ins, op, k, wrong, extra=""):
        outs = [ap(op, x, k) for x in ins]
        for wo, wk in wrong:
            assert [ap(wo, x, wk) if (wo != "÷" or x % wk == 0) else None for x in ins] != outs
        e = "Look at each In number and the Out number below it: %s. The rule is <b>%s</b>.%s" % (
            ", ".join("%s %s %s = %s" % (f(x), op, f(k), f(y)) for x, y in zip(ins, outs)), rname(op, k), extra)
        return mcq(fig(io_svg(ins, outs)) + "What is the rule for this table?", rname(op, k),
                   [rname(a, b) for a, b in wrong], e)

    def tab_out(ins, op, k, cands, extra=""):
        outs = [ap(op, x, k) for x in ins]
        a = outs[-1]
        e = "Use the rule on the In number above the ?: %s %s %s = <b>%s</b>.%s" % (f(ins[-1]), op, f(k), f(a), extra)
        return nums_mcq(fig(io_svg(ins, outs[:-1] + ["?"])) + "The rule is <b>%s</b>. What is the missing Out number?"
                        % rname(op, k), a, cands, e)

    q1 = out_q(7, "+", 5, [2, 35, 13], " 35 multiplies instead of adding.")
    q2 = out_q(30, MINUS, 8, [38, 23, 21], " 38 adds instead of subtracting.")
    q3 = out_q(6, "×", 4, [10, 2, 28], " 10 adds 4 instead of multiplying.")
    q4 = out_q(45, "÷", 5, [40, 50, 8], " 40 subtracts 5 instead of dividing.")
    q5 = out_q(250, "+", 100, [260, 150, 1250], " Adding 100 changes the hundreds digit.")
    q6 = tab_out([2, 4, 5, 7], "×", 3, [18, 10, 24],
                 " 18 adds 3 to the last Out number, but the In numbers do not go up by 1.")
    q7 = tab_out([10, 20, 25, 40], "+", 15, [45, 25, 50], " 45 adds 5 to the last Out number. Use the rule on 40.")
    q8 = rule_q([3, 5, 8, 10], "+", 7, [("+", 2), ("+", 3), ("×", 3)],
                " “Add 2” only describes how the Out row changes from 10 to 12.")
    q9 = rule_q([2, 3, 5, 6], "×", 2, [("+", 2), ("+", 4), ("×", 4)],
                " “Add 2” works for 2 → 4 only. Check every column: 3 + 2 is 5, not 6.")
    q10 = rule_q([20, 30, 45, 60], MINUS, 5, [("+", 5), ("+", 10), (MINUS, 10)],
                 " The Out numbers are smaller, so the rule makes numbers smaller.")
    q11 = rule_q([12, 18, 24, 36], "÷", 6, [(MINUS, 10), ("+", 1), ("÷", 3)],
                 " “Subtract 10” works for the first column only: 18 − 10 is 8, not 3.")
    q12 = in_q("+", 9, 30, [39, 20, 22], " 39 adds 9 again.")
    q13 = in_q("×", 3, 27, [81, 24, 30], " 81 multiplies again instead of undoing.")
    q14 = in_q(MINUS, 40, 75, [35, 105, 125], " 35 subtracts again instead of undoing.")
    ins = [2, 4, 7, 9]
    outs = [ap("×", x, 5) for x in ins]
    q15 = nums_mcq(fig(io_svg([2, 4, "?", 9], outs)) + "The rule is <b>Multiply by 5</b>. What is the missing In number?",
                   7, [6, 175, 30],
                   "Which number times 5 is 35? Work backward: 35 ÷ 5 = <b>7</b>. Check: 7 × 5 = 35. "
                   "6 only looks at the In row (2, 4, 6). 175 multiplies 35 by 5.")
    pairs = {"8 → 48": 8 * 6 == 48, "8 → 14": 8 * 6 == 14, "8 → 56": 8 * 6 == 56, "6 → 42": 6 * 6 == 42}
    assert [k for k, v in pairs.items() if v] == ["8 → 48"]
    q16 = mcq("The rule is <b>Multiply by 6</b>. Which In → Out pair follows the rule?", "8 → 48",
              ["8 → 14", "8 → 56", "6 → 42"],
              "8 × 6 = 48, so <b>8 → 48</b> follows the rule. 8 → 14 adds 6. 8 → 56 is 8 × 7. 6 × 6 is 36, not 42.")
    q17 = out_q(1200, "+", 350, [850, 1505, 1650], " Add 3 hundreds and 5 tens: 1200 + 300 + 50.")
    q18 = out_q(5000, MINUS, 1250, [6250, 4750, 3850], " 6250 adds instead of subtracting.")
    q19 = tab_out([4, 7, 12, 25], "×", 10, [35, 2500, 130],
                  " 130 adds 10 to the last Out number. 2500 multiplies by 100.")
    a20 = ap("+", ap("×", 6, 3), 4)
    assert a20 == 22
    q20 = nums_mcq(fig(machine_svg(["6", "× 3", "+ 4", "?"])) + "The number goes through both rules, in order. "
                   "What number comes out?", a20, [30, 13, 18],
                   "First 6 × 3 = 18. Then 18 + 4 = <b>22</b>. 30 does the rules in the wrong order: (6 + 4) × 3. "
                   "18 forgets the second rule.")
    out = [q1, q3, q2, q4, q5, q16, q12, q6, q7, q13, q9, q8, q14, q17, q10, q18, q11, q15, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Input/output tables and rule boxes", "items": out}


# ============================================================ set 5: predict later terms and real-life patterns
def set_predict():
    dol = lambda v: "$%s" % f(v)
    cm = lambda v: "%s cm" % f(v)

    p = seq(15, 4, 10)
    q1 = nums_mcq(track(p[:4] + [None]) + "The rule is “Start at 15 and add 4 each time.” What is the 10th number?",
                  p[9], [55, 40, 47],
                  "From the 1st to the 10th number there are 9 jumps. 9 × 4 = 36. 15 + 36 = <b>%d</b>. "
                  "55 makes 10 jumps, one too many." % p[9])
    p = seq(200, -15, 10)
    assert p[9] == 65
    q2 = nums_mcq(track(p[:4] + [None]) + "The rule is “Start at 200 and subtract 15 each time.” What is the 10th number?",
                  p[9], [50, 335, 80],
                  "From the 1st to the 10th number there are 9 jumps. 9 × 15 = 135. 200 − 135 = <b>65</b>. "
                  "50 makes 10 jumps. 335 goes the wrong way.")
    q3 = nums_mcq("Liam has $12. He saves $5 each week. How much money does he have after 6 weeks?", 12 + 6 * 5,
                  [30, 47, 37],
                  "Start at $12 and add $5 each week: $17, $22, $27, $32, $37, <b>$42</b>. "
                  "$30 forgets the $12 he started with.", dol)
    q4 = nums_mcq(fig(tov_svg([0, 1, 2, 3], [24, 21, 18, 15], ["Hours", "Height (cm)"], "table of values candle")) +
                  "A candle gets shorter as it burns. How tall is it after 5 hours?", 24 - 5 * 3, [39, 12, 21],
                  "The candle gets 3 cm shorter each hour: 24, 21, 18, 15, 12, <b>9 cm</b>. "
                  "39 cm goes the wrong way. 12 cm is after 4 hours.", cm)
    raised = seq(60, 35, 6)
    q5 = nums_mcq("A Grade 4 class raises money for the Terry Fox Run. They have $60 after week 1, $95 after week 2 "
                  "and $130 after week 3. The pattern continues. How much do they have after week 6?",
                  raised[5], [270, 210, 165],
                  "The rule is add $35 each week: %s. After week 6 they have <b>$%d</b>. "
                  "$210 is 6 × $35, but the class started at $60." % (", ".join(dol(v) for v in raised), raised[5]), dol)
    q6 = mcq("On a summer day, a BC Ferries ship leaves Horseshoe Bay at 7:20 a.m., 9:20 a.m. and 11:20 a.m. "
             "The pattern continues. When does the 5th ferry leave?", "3:20 p.m.",
             ["1:20 p.m.", "5:20 p.m.", "3:20 a.m."],
             "Add 2 hours each time: 7:20 a.m., 9:20 a.m., 11:20 a.m., 1:20 p.m., <b>3:20 p.m.</b> "
             "After noon, the times are p.m. 1:20 p.m. is the 4th ferry.")
    salmon = seq(40, 15, 5)
    q7 = nums_mcq("Kai counts salmon swimming up a creek near Nanaimo. He sees 40 on Monday, 55 on Tuesday and "
                  "70 on Wednesday. The pattern continues. How many does he see on Friday?", salmon[4], [115, 85, 75],
                  "Add 15 each day: Monday 40, Tuesday 55, Wednesday 70, Thursday 85, Friday <b>%d</b>. "
                  "85 is Thursday." % salmon[4])
    rain = seq(4, 3, 8)
    q8 = nums_mcq(fig(tov_svg([1, 2, 3], [4, 7, 10], ["Hours", "Rain (mm)"], "table of values rain")) +
                  "It rains all day in Vancouver. The table shows the total rain. The pattern continues. "
                  "How much rain is there after 8 hours?", rain[7], [24, 28, 13],
                  "Add 3 mm each hour. From hour 1 to hour 8 there are 7 jumps: 7 × 3 = 21. 4 + 21 = <b>25 mm</b>. "
                  "24 is 8 × 3, but hour 1 already has 4 mm.", lambda v: "%d mm" % v)
    q9 = mcq("A SkyTrain comes every 6 minutes. The first three trains come at 8:04 a.m., 8:10 a.m. and 8:16 a.m. "
             "When does the 6th train come?", "8:34 a.m.", ["8:40 a.m.", "8:28 a.m.", "8:36 a.m."],
             "From the 1st to the 6th train there are 5 jumps of 6 minutes. 5 × 6 = 30. "
             "8:04 + 30 minutes = <b>8:34 a.m.</b> 8:40 a.m. makes 6 jumps.")
    snow = seq(180, -15, 7)
    q10 = nums_mcq("In spring, the snow on a mountain near Whistler is 180 cm deep. It melts 15 cm each week. "
                   "How deep is the snow after 6 weeks?", snow[6], [270, 105, 95],
                   "Subtract 15 cm each week: %s. After 6 weeks it is <b>%d cm</b>. "
                   "270 cm goes the wrong way. 105 cm is after 5 weeks." % (", ".join(cm(v) for v in snow), snow[6]), cm)
    assert 20 + 5 * 16 == 100
    q11 = mcq("Simran has $20. She saves $16 each week. After how many weeks will she have $100?", "5 weeks",
              ["6 weeks", "4 weeks", "80 weeks"],
              "Count on by $16: $36, $52, $68, $84, $100. That is <b>5 weeks</b>. "
              "6 weeks counts one week too many.")
    barrel = seq(180, -12, 8)
    q12 = nums_mcq("A rain barrel holds 180 L of water. Emma uses 12 L each day to water her garden. "
                   "How much water is left after 7 days?", barrel[7], [264, 108, 84],
                   "She uses 7 × 12 = 84 L. 180 − 84 = <b>96 L</b>. 84 L is the water she used, not what is left. "
                   "264 L goes the wrong way.", lambda v: "%d L" % v)
    seats = [cnt("tables", k) for k in range(1, 11)]
    q13 = nums_mcq(fig(pattern_svg("tables")) + "Picnic tables at Stanley Park are pushed together in a row. "
                   "How many people can sit at 8 tables?", seats[7], [32, 16, 20],
                   "Start at 4 and add 2 for each table: %s. 8 tables seat <b>%d</b> people. "
                   "32 counts 4 seats for every table, but no one sits where tables touch." % (lst(seats[:8]), seats[7]))
    q14 = mcq("Ava makes a bead pattern. Figure 1 has 7 beads. Each figure has 7 more beads than the one before. "
              "Which figure has 63 beads?", "Figure 9", ["Figure 63", "Figure 10", "Figure 8"],
              "Count by 7s: 7, 14, 21, 28, 35, 42, 49, 56, 63. That is <b>Figure 9</b>. "
              "63 is the number of beads, not the figure number.")
    assert 1630 % 25 != 0
    q15 = mcq("Owen counts by 25s from 0. He says, “I will say 1630.” Is he right?",
              "No, counting by 25s gives numbers ending in 00, 25, 50 or 75",
              ["Yes, 1630 is less than 10 000", "Yes, 1630 ends in 0", "No, he can only count to 1000"],
              "Counting by 25s from 0 gives 25, 50, 75, 100 … Every number ends in 00, 25, 50 or 75. "
              "1630 ends in 30, so <b>he is not right</b>.")
    tree = seq(30, 15, 9)
    q16 = nums_mcq("A cedar seedling is 30 cm tall. It grows 15 cm each year. How tall is it after 8 years?",
                   tree[8], [120, 165, 135],
                   "8 years means 8 jumps of 15 cm: 8 × 15 = 120. 30 + 120 = <b>150 cm</b>. "
                   "120 cm forgets the 30 cm it started with. 165 cm is after 9 years.", cm)
    bike = seq(3, 2, 10)
    q17 = nums_mcq("Mei bikes on the Stanley Park Seawall. She bikes 3 km in week 1, 5 km in week 2 and 7 km in week 3. "
                   "The pattern continues. How far does she bike in week 10?", bike[9], [20, 23, 30],
                   "Add 2 km each week. From week 1 to week 10 there are 9 jumps: 9 × 2 = 18. 3 + 18 = <b>21 km</b>. "
                   "23 km makes 10 jumps. 30 km is 10 × 3.", lambda v: "%d km" % v)
    seedb = seq(5000, -250, 13)
    assert seedb[12] == 2000
    q18 = nums_mcq("A bag of birdseed has 5000 g. Harjot puts 250 g in the bird feeder each day. "
                   "How much birdseed is left after 12 days?", seedb[12], [3000, 2250, 8000],
                   "He uses 12 × 250 = 3000 g. 5000 − 3000 = <b>2000 g</b>. 3000 g is how much he used. "
                   "2250 g is after 11 days.", lambda v: "%s g" % f(v))
    q19 = nums_mcq(fig(io_svg([1, 2, 3, 4], [3, 6, 9, 12])) + "Each canoe holds 3 people. In is the number of "
                   "canoes and Out is the number of people. How many people can 15 canoes hold?", 45, [18, 42, 48],
                   "The rule is <b>Multiply by 3</b>. 15 × 3 = <b>45</b>. 18 adds 3 to 15 instead of multiplying.")
    hana = [8 * w for w in range(10)]
    owen = [24 + 5 * w for w in range(10)]
    same = [w for w in range(10) if hana[w] == owen[w]]
    assert same == [8]
    q20 = mcq("Nadia has $0 and saves $8 each week. Ryan has $24 and saves $5 each week. "
              "After how many weeks will they have the same amount?", "8 weeks",
              ["3 weeks", "24 weeks", "9 weeks"],
              "Make a table. Nadia: $0, $8, $16, $24, $32, $40, $48, $56, $64. "
              "Ryan: $24, $29, $34, $39, $44, $49, $54, $59, $64. After <b>8 weeks</b> they both have $64. "
              "3 weeks is when Nadia has $24, but Ryan has more by then.")
    out = [q1, q3, q4, q2, q7, q5, q6, q10, q8, q9, q12, q14, q11, q13, q16, q17, q19, q15, q18, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Predict later terms and real-life patterns", "items": out}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Increasing and decreasing patterns</h2>"
        "<p>In an <b>increasing pattern</b>, the numbers get bigger. In a <b>decreasing pattern</b>, they get smaller. "
        "Find the jump between two numbers next to each other. Then check that the same jump works every time.</p>"
        "<figure class='sn-fig'>" + track_svg([1015, 1040, 1065, 1090]) +
        "<figcaption>Each number is 25 more. The pattern rule is: start at 1015 and add 25 each time.</figcaption></figure>"
        "<figure class='sn-fig'>" + nline_svg(1200, [-150, -150, -150], ticks=["1200", "1050", "900", "750"]) +
        "<figcaption>A decreasing pattern: start at 1200 and subtract 150 each time.</figcaption></figure>"
        "<p>A <b>pattern rule</b> tells where to start and what to do each time.</p>"
        "<h2>Shape patterns and tables</h2>"
        "<p>Count each figure. Put the figure number in the top row and the count in the bottom row.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sq") +
        "<figcaption>Figure 1 has 4 sticks, Figure 2 has 7, Figure 3 has 10.</figcaption></figure>"
        + table(["Figure number", "1", "2", "3", "4"], [["Number of sticks", "4", "7", "10", "13"]]) +
        "<p>The rule is <b>start at 4 and add 3 each time</b>.</p>"
        "<h2>Input/output tables and rule boxes</h2>"
        "<p>A rule box changes each In number into an Out number. Use the rule on the In number in the same column.</p>"
        "<figure class='sn-fig'>" + machine_svg(["6", "× 4", "24"]) +
        "<figcaption>The rule is multiply by 4: 6 × 4 = 24.</figcaption></figure>"
        "<p>To find a missing In number, work backward. Undo × with ÷, and undo + with −.</p>"
        + ex("Find the rule", "In: 2, 3, 5, 6. Out: 4, 6, 10, 12.",
             "“Add 2” works for 2 → 4 only. Check every column: 2 × 2 = 4, 3 × 2 = 6, 5 × 2 = 10, 6 × 2 = 12.",
             "Multiply by 2")
        + ex("Predict the 10th number", "Start at 15 and add 4 each time. What is the 10th number?",
             "From the 1st number to the 10th there are 9 jumps. 9 × 4 = 36. 15 + 36 = 51.", "51")
        + ex("A candle gets shorter", "A candle is 24 cm tall. It burns 3 cm each hour. How tall is it after 5 hours?",
             "Subtract 3 each hour: 24, 21, 18, 15, 12, 9.", "9 cm") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using only the first step: 3, 4, 6, 9 is “add 1”", "Check every jump: +1, +2, +3, so the next jump is +4"],
            ["Mixing up the figure number and the count", "The figure number is on top. The count is below it"],
            ["Extending the wrong way: 50, 45, 40, then 45", "A decreasing pattern keeps getting smaller"],
            ["Using the start as the jump: 8, 14, 20 is “add 8”", "Start at 8 and add 6 each time"],
            ["10 jumps for the 10th number", "From the 1st to the 10th number there are 9 jumps"],
            ["Reading along the Out row in an In/Out table", "Use the rule on the In number in the same column"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about patterns in the BC math curriculum?",
     "a": "In the BC curriculum, Grade 4 students work with increasing and decreasing patterns, show them in tables and charts, and describe the pattern rule. They also explore algebraic relationships, such as input/output tables and one-step equations."},
    {"q": "What is the difference between an increasing and a decreasing pattern?",
     "a": "In an increasing pattern the numbers get bigger each time, like 15, 19, 23. In a decreasing pattern they get smaller, like 200, 185, 170."},
    {"q": "How do you find the rule in an input/output table?",
     "a": "Compare each In number with the Out number below it and test the rule on every column, not just the first. For In 2, 3, 5 and Out 4, 6, 10, the rule is multiply by 2."},
    {"q": "Are patterns on the Grade 4 FSA?",
     "a": "The Grade 4 FSA numeracy component is based on the BC curriculum, and patterning is part of Grade 4 math. Practice with pattern rules, tables and input/output problems is good preparation."},
]


def gen():
    rnd = random.Random(34809)
    sets = [set_increasing(), set_decreasing(), set_shapes(), set_io(), set_predict()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "increasing-and-decreasing-patterns",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Increasing and Decreasing Patterns",
        "seo_title": "Grade 4 Increasing and Decreasing Patterns Worksheets: Pattern Rules, Tables and Input/Output (BC Math)",
        "short_title": "Increasing and decreasing patterns",
        "domain": "Patterning",
        "standard_code": "Grade 4: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Increasing and decreasing patterns, using tables and charts",
        "meta_desc": "Free Grade 4 math worksheets on increasing and decreasing patterns: find pattern rules for numbers to 10 000, extend shape patterns with tables, solve input/output tables and rule boxes, and predict later terms in real-life patterns. 100 questions with an answer key, matched to the BC curriculum and good FSA practice.",
        "key_big": "A pattern rule tells where to start and what to do each time.",
        "key_sub": "Find the jump and check it works every time: 1015, 1040, 1065 is “start at 1015 and add 25 each time.” In an input/output table, use the rule on the In number in the same column. For the 10th term, there are 9 jumps from the 1st.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number track|number line|shape pattern|table of values|input output table|rule machine)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
