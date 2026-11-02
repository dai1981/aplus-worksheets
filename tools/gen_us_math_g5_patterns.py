# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Patterns and Relationships (5.OA.B.3)
  python tools/gen_us_math_g5_patterns.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.

Two patterns made from two rules, the relationship between corresponding terms, ordered pairs
(Pattern A term, Pattern B term) and their graphs in the first quadrant.
Every grid is drawn exactly: a point sits on a grid intersection, labels sit in the middle of a
grid square next to their own point and never touch another point (checked in Grid.render).
Wrong answers come from real mistakes: describing a "times" relationship as "add" (comparing only
the first pair), using the other pattern's rule, switching the order in an ordered pair, pairing
terms that do not correspond, using the rule one time too many, reading grid spaces instead of
the scale, reversing the relationship (A is 2 times B).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
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
    """Grade 5 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def money(n):
    return "$" + f(n)


def pair(x, y):
    return "(%s, %s)" % (x, y)


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
    """Choices keep their order (point letters, graph numbers, numbers from small to large)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e, fmt=f):
    """Number answers: 3 distractors from real mistakes (positive, unique); positions are balanced later."""
    ch = []
    for c in cands:
        if c > 0 and c != correct and c not in ch:
            ch.append(c)
    assert len(ch) >= 3, (q, ch)
    return {"q": q, "c": [fmt(c) for c in ch[:3]] + [fmt(correct)], "a": 3, "e": e}


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


def seq(s, k, n):
    return [s + i * k for i in range(n)]


def lst(xs):
    return ", ".join(f(x) for x in xs)


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def rules(sA, kA, sB, kB):
    return ("Pattern A: start at %s, Add %s. Pattern B: start at %s, Add %s."
            % (f(sA), f(kA), f(sB), f(kB)))


class Pos:
    """Positions for picture answers, spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ two-pattern table
def two_table(a, b, la, lb, label="two patterns table"):
    """Three rows: Term 1..n, Pattern A, Pattern B. Values are numbers or '?'."""
    n = len(a)
    assert len(b) == n
    LW = int(max(tw(la, 16, True), tw(lb, 16, True), tw("Term", 15, True)) + 20)
    cells = [f(v) if isinstance(v, int) else v for v in a + b]
    CW = int(max(44, max(tw(c, 17, True) for c in cells) + 18))
    RH = 30
    s = []
    rows = [("Term", [str(i + 1) for i in range(n)], True), (la, a, False), (lb, b, False)]
    for r, (name, vals, head) in enumerate(rows):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (y, LW, RH, FILL2 if head else FILL, GREEN))
        s.append(text(2 + LW / 2.0, y + RH / 2.0 + 5.5, name, 15 if head else 16, bold=True))
        for i, v in enumerate(vals):
            x = 2 + LW + i * CW
            t = f(v) if isinstance(v, int) else v
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, CW, RH, FILL2 if head else "#ffffff", GREEN))
            s.append(text(x + CW / 2.0, y + RH / 2.0 + 6, t, 15 if head else 17, bold=not head,
                          col=RED if t == "?" else INK))
    return svg_wrap(4 + LW + CW * n, 4 + RH * 3, "".join(s), label)


def ab_table(sA, kA, sB, kB, n=5, hide=None):
    """hide: (row 'A' or 'B', index) shown as '?'."""
    a, b = seq(sA, kA, n), seq(sB, kB, n)
    a = list(a)
    b = list(b)
    if hide:
        (a if hide[0] == "A" else b)[hide[1]] = "?"
    return fig(two_table(a, b, "A: Add %s" % f(kA), "B: Add %s" % f(kB)))


# ------------------------------------------------------------ coordinate grid
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
        # x-axis numbers must not touch each other
        assert tw(nx * sx, 14) + 3 <= u, ("x numbers too wide", nx * sx, u)
        if xt:
            assert tw(xt, 14, True) < self.W
        if yt:
            assert tw(yt, 14, True) < ny * u + 20, yt
        self.pts, self.notes = [], []

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
            cell = (min(x, cx), min(y, cy))
            if cell in used:
                continue
            c = self.P(x + dx / 2.0, y + dy / 2.0)
            box = (c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7)
            if any(overlap(box, b) for b in boxes):
                continue
            used.add(cell)
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
            s.append(text(ox + k * u, oy + 18, k * self.sx, 14))
        for k in range(1, ny + 1):
            s.append(text(ox - 9, oy - k * u + 5, k * self.sy, 14, anchor="end"))
        s.append(text(ox - 9, oy + 18, 0, 14, anchor="end"))
        if self.xt:
            s.append(text(ox + nx * u / 2.0, oy + 40, self.xt, 14, bold=True))
        if self.yt:
            my = oy - ny * u / 2.0
            s.append(text(13, my, self.yt, 14, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % my))
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

    def svg(self, label="graph of ordered pairs from two patterns"):
        return svg_wrap(self.W, self.H, self.render(), label)


def mini_graphs(graphs):
    """Four small 0-4 grids side by side, titled Graph 1 to Graph 4 (no labels on the points)."""
    U, N = 18, 4
    L, T, R, B = 24, 30, 12, 24
    w1 = L + N * U + R
    gap = 18
    s = []
    for g, pts in enumerate(graphs):
        x0 = g * (w1 + gap)
        ox, oy = x0 + L, T + N * U
        s.append(text(x0 + L + N * U / 2.0, 17, "Graph %d" % (g + 1), 15, bold=True))
        for k in range(N + 1):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                     % (ox + k * U, oy, ox + k * U, oy - N * U, GRID))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                     % (ox, oy - k * U, ox + N * U, oy - k * U, GRID))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox + N * U + 6, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox, oy - N * U - 6, INK))
        for k in range(N + 1):
            s.append(text(ox + k * U, oy + 17, k, 14))
            if k:
                s.append(text(ox - 9, oy - k * U + 5, k, 14, anchor="end"))
        for x, y in pts:
            assert 0 <= x <= N and 0 <= y <= N
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (ox + x * U, oy - y * U, GREEN))
    W = len(graphs) * w1 + (len(graphs) - 1) * gap
    return svg_wrap(W, T + N * U + B, "".join(s), "four graphs of ordered pairs")


# ------------------------------------------------------------ set 1: make two patterns from two rules
def set_generate(rnd):
    its = []
    # A: missing term in a two-row table
    for sA, kA, sB, kB, row, i in [
        (0, 3, 0, 6, "B", 2), (0, 2, 0, 8, "B", 3), (0, 4, 0, 12, "A", 3), (0, 5, 0, 10, "B", 4),
        (0, 1, 0, 7, "B", 2), (2, 3, 5, 3, "B", 3), (0, 10, 0, 30, "B", 3), (0, 250, 0, 500, "B", 4),
    ]:
        s, k, so, ko = (sB, kB, sA, kA) if row == "B" else (sA, kA, sB, kB)
        ans = s + i * k
        prev = ans - k
        other = so + i * ko
        cands = [prev + ko, ans + k, other]
        if s:
            cands.append(i * k)
        cands += [prev]
        e = ("Pattern %s adds %s each time. The term before the ? is %s, so %s + %s = %s."
             % (row, f(k), f(prev), f(prev), f(k), f(ans)))
        if prev + ko != ans:
            e += " (Adding %s uses the rule of the other pattern.)" % f(ko)
        q = ab_table(sA, kA, sB, kB, 5, (row, i)) + rules(sA, kA, sB, kB) + " What number goes in the ? box?"
        its.append(mcq_num(q, ans, cands, e))
    # B: the first five terms
    for name, s, k, so, ko in [("B", 0, 8, 0, 4), ("B", 0, 15, 0, 5), ("A", 0, 6, 0, 12),
                               ("B", 3, 4, 0, 4), ("B", 0, 120, 0, 40), ("A", 1, 2, 4, 2)]:
        xs = seq(s, k, 5)
        right = lst(xs)
        wrong = [lst(seq(s + k, k, 5)), lst(seq(s, ko, 5))]
        if s:
            wrong.append(lst(seq(0, k, 5)))
        else:
            wrong.append(lst([0, k, 2 * k, 4 * k, 8 * k]))
        wrong.append(lst(seq(s, s, 5)) if s else "")
        sA, kA, sB, kB = (so, ko, s, k) if name == "B" else (s, k, so, ko)
        e = ("Pattern %s starts at %s, and the start is the 1st term. Then add %s each time: %s."
             % (name, f(s), f(k), right))
        its.append(mcq(rules(sA, kA, sB, kB) + " Which list shows the first five terms of Pattern %s?" % name,
                       right, wrong, e, rnd))
    # C: a later term (count the jumps)
    for name, s, k, n, so, ko in [("B", 0, 12, 6, 0, 4), ("B", 0, 9, 8, 0, 3), ("B", 5, 4, 7, 0, 4),
                                  ("B", 0, 150, 10, 0, 50), ("A", 0, 6, 9, 0, 18), ("B", 0, 25, 12, 0, 5)]:
        ans = s + (n - 1) * k
        sA, kA, sB, kB = (so, ko, s, k) if name == "B" else (s, k, so, ko)
        e = ("From the 1st term to the %s term there are %d jumps, not %d. %s + %d × %s = %s."
             % (ordn(n), n - 1, n, f(s), n - 1, f(k), f(ans)))
        its.append(mcq_num(rules(sA, kA, sB, kB) + " What is the %s term of Pattern %s?" % (ordn(n), name), ans,
                           [s + n * k, so + (n - 1) * ko, s + (n - 2) * k], e))
    assert len(its) == 20, len(its)
    return {"title": "Make two patterns from two rules", "items": its}


# ------------------------------------------------------------ set 2: relationships between corresponding terms
def rel_text(sA, kA, sB, kB):
    """The true relationship (B compared with A) and three statements from real mistakes."""
    if sA == 0 and sB == 0:
        m = kB // kA
        assert m * kA == kB
        right = "B is %d times A" % m
        wrong = ["B is %s more than A" % f(kB - kA), "A is %d times B" % m, "B is %d more than A" % m]
        return right, wrong, m, None
    d = sB - sA
    assert kA == kB and d > 0
    right = "B is %d more than A" % d
    wrong = ["B is %s more than A" % f(kA), "B is %d times A" % d, "A is %d more than B" % d]
    return right, wrong, None, d


def set_relationship(rnd):
    its = []
    for sA, kA, sB, kB in [(0, 3, 0, 6), (0, 2, 0, 8), (0, 5, 0, 15), (0, 4, 0, 20), (0, 6, 0, 12),
                           (0, 7, 0, 21), (0, 3, 4, 3), (1, 5, 7, 5)]:
        right, wrong, m, d = rel_text(sA, kA, sB, kB)
        a, b = seq(sA, kA, 5), seq(sB, kB, 5)
        if m:
            e = ("Look down each column: %s. Each B term is %d times the A term. (“B is %s more than A” works only "
                 "for %s and %s: %s is %s more than %s.)"
                 % (", ".join("%s × %d = %s" % (f(x), m, f(y)) for x, y in zip(a[1:4], b[1:4])), m, f(kB - kA),
                    f(a[1]), f(b[1]), f(b[2]), f(b[2] - a[2]), f(a[2])))
        else:
            e = ("Look down each column: %s. Each B term is %d more than the A term. The rule Add %d tells how each "
                 "pattern grows, not how A and B compare."
                 % (", ".join("%d + %d = %d" % (x, d, y) for x, y in zip(a[:3], b[:3])), d, kA))
        its.append(mcq(ab_table(sA, kA, sB, kB) + "Compare each B term with the A term in the same column. "
                       "Which is true for every pair of corresponding terms?", right, wrong, e, rnd))
    # why does it happen?
    its.append(mcq(rules(0, 3, 0, 6) + " Why is each B term 2 times the A term?",
                   "Both start at 0, and 6 is 2 × 3",
                   ["B always adds 3 more than A", "B starts at a bigger number", "6 is 3 more than 3"],
                   "Both patterns start at 0. Each step, B adds 6 and A adds 3, and 6 = 2 × 3. After any number of "
                   "steps, B has added 2 times as much as A, so B is 2 times A: for example 4 × 3 = 12 and 4 × 6 = 24.", rnd))
    its.append(mcq(rules(0, 5, 4, 5) + " Why is each B term always 4 more than the A term?",
                   "Both add 5, and B starts 4 higher",
                   ["B adds 4 more each time", "B is 4 times A", "5 is 4 more than 1"],
                   "B starts 4 higher (4 − 0 = 4). Each step both patterns add the same number, 5, so the difference "
                   "never changes: 0 and 4, 5 and 9, 10 and 14.", rnd))
    its.append(mcq(rules(0, 4, 0, 12) + " Will the 100th term of B still be 3 times the 100th term of A?",
                   "Yes, both use the same number of jumps",
                   ["No, the difference keeps growing", "No, it works only for small terms", "Yes, because B adds 8 more"],
                   "The 100th term of each pattern comes after 99 jumps. A is 99 × 4 and B is 99 × 12 = 99 × 3 × 4. "
                   "B is 3 times A for every term, however far you go.", rnd))
    its.append(mcq("Pattern A: 0, 5, 10, 15. Pattern B: 0, 20, 40, 60. Owen says, “B is 15 more than A.” What mistake did he make?",
                   "He checked only one pair",
                   ["He switched A and B", "He used the wrong rule for A", "No mistake. He is right"],
                   "20 is 15 more than 5, but 40 is 30 more than 10. Check every pair: 5 × 4 = 20, 10 × 4 = 40, "
                   "15 × 4 = 60. B is 4 times A.", rnd))
    # use the relationship
    its.append(mcq_num(rules(0, 3, 0, 12) + " A term in Pattern A is 27. What is the corresponding term in Pattern B?",
                       108, [31, 39, 81],
                       "12 = 4 × 3 and both start at 0, so each B term is 4 times the A term: 27 × 4 = 108. "
                       "(Adding 4 or adding 12 to 27 does not use the relationship.)"))
    its.append(mcq_num(rules(0, 2, 0, 10) + " A term in Pattern B is 60. What is the corresponding term in Pattern A?",
                       12, [300, 55, 50],
                       "Each B term is 5 times the A term (10 = 5 × 2). Work backward: 60 ÷ 5 = 12. "
                       "Check: 12 × 5 = 60. (300 = 60 × 5 goes the wrong way.)"))
    its.append(mcq_num(rules(0, 5, 6, 5) + " A term in Pattern A is 45. What is the corresponding term in Pattern B?",
                       51, [270, 39, 50],
                       "Both patterns add 5, and B starts 6 higher, so each B term is 6 more than the A term: 45 + 6 = 51. "
                       "(45 × 6 = 270 treats it as times.)"))
    its.append(mcq_num(rules(0, 250, 0, 750) + " A term in Pattern A is 1,500. What is the corresponding term in Pattern B?",
                       4500, [1750, 2250, 500],
                       "750 = 3 × 250, so each B term is 3 times the A term: 1,500 × 3 = 4,500. "
                       "(1,500 + 750 = 2,250 is just one more jump of B's rule.)"))
    its.append(mcq_num("Each term in Pattern B is 6 times the corresponding term in Pattern A. The 5th term of Pattern A is 32. "
                       "What is the 5th term of Pattern B?", 192, [38, 26, 160],
                       "Corresponding terms are in the same place: the 5th term with the 5th term. 32 × 6 = 192. "
                       "(32 + 6 = 38 adds instead of multiplying, and 32 × 5 uses the term number.)"))
    its.append(mcq_num(rules(0, 9, 0, 18) + " A term in Pattern B is 126. What is the corresponding term in Pattern A?",
                       63, [252, 117, 108],
                       "Each B term is 2 times the A term (18 = 2 × 9). So A is half of B: 126 ÷ 2 = 63. "
                       "Check: 63 × 2 = 126."))
    # rule vs relationship
    its.append(mcq("Pattern A: 0, 5, 10, 15, 20. Pattern B: 0, 15, 30, 45, 60. What is the <b>rule</b> for Pattern B?",
                   "Add 15", ["B is 3 times A", "Add 5", "Add 10"],
                   "A rule tells how to get the next term in the same pattern: 0 + 15 = 15, 15 + 15 = 30. "
                   "“B is 3 times A” is the relationship between the two patterns, not B's rule.", rnd))
    its.append(mcq("Pattern A: 0, 5, 10, 15, 20. Pattern B: 0, 15, 30, 45, 60. Which describes the <b>relationship</b> between "
                   "corresponding terms?", "B is 3 times A", ["Add 15", "B is 10 more than A", "A is 3 times B"],
                   "Compare terms in the same place: 5 and 15, 10 and 30, 15 and 45. Each B term is 3 times the A term. "
                   "Add 15 is only B's rule.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Relationships between corresponding terms", "items": its}


# ------------------------------------------------------------ set 3: ordered pairs
def set_pairs(rnd):
    its = []
    for sA, kA, sB, kB, i in [(0, 3, 0, 6, 2), (0, 2, 0, 10, 3), (0, 4, 0, 12, 1), (0, 5, 0, 20, 3),
                              (1, 2, 4, 2, 2), (0, 100, 0, 300, 2)]:
        a, b = seq(sA, kA, 6), seq(sB, kB, 6)
        x, y = a[i], b[i]
        right = pair(f(x), f(y))
        wrong = [pair(f(y), f(x)), pair(f(x), f(b[i + 1])), pair(f(a[i + 1]), f(y))]
        e = ("%s is the %s term of A and %s is the %s term of B, so they correspond. Write the A term first: %s. "
             "%s has the numbers switched." % (f(x), ordn(i + 1), f(y), ordn(i + 1), right, wrong[0]))
        its.append(mcq(ab_table(sA, kA, sB, kB) + "Ordered pairs are written (A term, B term). "
                       "Which ordered pair is made from corresponding terms?", right, wrong, e, rnd))
    for k, K in [(2, 6), (4, 8), (5, 20), (1, 3), (25, 75)]:
        shown = ", ".join(pair(i * k, i * K) for i in range(4))
        x, y = 4 * k, 4 * K
        right = pair(x, y)
        wrong = [pair(x, 3 * K + k), pair(y, x), pair(5 * k, 5 * K)]
        e = ("The first numbers go up by %d and the second numbers go up by %d. After %s comes (%d + %d, %d + %d) = %s."
             % (k, K, pair(3 * k, 3 * K), 3 * k, k, 3 * K, K, right))
        its.append(mcq("These ordered pairs come from two patterns: <b>%s, ?</b> Which ordered pair comes next?" % shown,
                       right, wrong, e, rnd))
    its.append(mcq(rules(0, 3, 0, 12) + " Which ordered pair (A term, B term) is <b>not</b> made from corresponding terms?",
                   "(24, 6)", ["(3, 12)", "(6, 24)", "(9, 36)"],
                   "6 is in A and 24 is in B, so the pair must be written (6, 24). (24, 6) has the numbers switched. "
                   "The other pairs all have B = 4 × A.", rnd))
    its.append(mcq(rules(0, 2, 0, 10) + " Which ordered pair (A term, B term) is <b>not</b> made from corresponding terms?",
                   "(6, 40)", ["(2, 10)", "(4, 20)", "(8, 40)"],
                   "6 is the 4th term of A, but 40 is the 5th term of B. The 4th term of B is 30, so the pair should be (6, 30). "
                   "In every correct pair, B is 5 times A.", rnd))
    its.append(mcq(rules(0, 5, 2, 5) + " Which ordered pair (A term, B term) is <b>not</b> made from corresponding terms?",
                   "(15, 20)", ["(0, 2)", "(5, 7)", "(10, 12)"],
                   "Each B term is 2 more than the A term, so the pair for 15 is (15, 17). (15, 20) adds 5, the rule, "
                   "instead of the relationship.", rnd))
    its.append(mcq("Ordered pairs are written (Pattern A term, Pattern B term). Where does the first number come from?",
                   "Pattern A", ["Pattern B", "the term number", "the rule of A"],
                   "The first number is a term of Pattern A and the second number is the term in the same place in Pattern B.", rnd))
    its.append(mcq(rules(0, 4, 0, 12) + " Which ordered pair (A term, B term) will be in the list?",
                   "(20, 60)", ["(60, 20)", "(20, 24)", "(24, 60)"],
                   "Each B term is 3 times the A term, so 20 goes with 20 × 3 = 60: (20, 60). (20, 24) adds 4, "
                   "and (24, 60) pairs the 7th term of A with the 6th term of B.", rnd))
    its.append(mcq_num(rules(0, 6, 0, 30) + " The ordered pair (30, ?) is in the list. What is the missing number?",
                       150, [60, 35, 180],
                       "30 is the 6th term of A. The 6th term of B is 5 × 30 = 150, because 30 = 5 × 6. "
                       "(180 is the 7th term of B: one jump too many.)"))
    its.append(mcq_num(rules(0, 125, 0, 500) + " In one ordered pair (A term, B term), the first number is 1,000. What is the second number?",
                       4000, [1500, 1125, 4500],
                       "500 = 4 × 125, so each B term is 4 times the A term: 1,000 × 4 = 4,000. "
                       "(4,500 is the next B term: one jump too many.)"))
    its.append(mcq(rules(1, 1, 4, 1) + " The pairs start (1, 4), (2, 5), (3, 6). What is the 5th ordered pair?",
                   "(5, 8)", ["(8, 5)", "(6, 9)", "(5, 20)"],
                   "The 5th terms are 1 + 4 = 5 and 4 + 4 = 8, so the pair is (5, 8). Each B term is 3 more than the A term. "
                   "(5, 20) treats (1, 4) as “B is 4 times A,” but 2 × 4 is not 5.", rnd))
    its.append(mcq(rules(2, 2, 6, 6) + " Which list shows the first three ordered pairs (A term, B term)?",
                   "(2, 6), (4, 12), (6, 18)",
                   ["(6, 2), (12, 4), (18, 6)", "(2, 6), (4, 8), (6, 10)", "(0, 0), (2, 6), (4, 12)"],
                   "A: 2, 4, 6. B: 6, 12, 18. Pair the 1st terms, the 2nd terms and the 3rd terms, A first. "
                   "The patterns start at 2 and 6, not 0.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Form ordered pairs from corresponding terms", "items": its}


# ------------------------------------------------------------ set 4: graph the ordered pairs
LET = ["P", "Q", "R", "S"]


def pat_grid(kA, kB, sx, sy, nx, ny, u=22):
    return Grid(nx, ny, u=u, sx=sx, sy=sy, xt="Pattern A", yt="Pattern B")


def set_graph(rnd):
    its = []
    pos = Pos(rnd)
    # A: which graph matches the table (graphs 1-4)
    for (sA, kA, sB, kB, n), right, wrongs, e in [
        ((0, 1, 0, 2, 3), [(0, 0), (1, 2), (2, 4)],
         [[(0, 0), (2, 1), (4, 2)], [(0, 1), (1, 2), (2, 3)], [(1, 0), (2, 2), (3, 4)]],
         "The pairs are (0, 0), (1, 2), (2, 4): go right by the A term and up by the B term. "
         "Graph {w0} has x and y switched."),
        ((0, 1, 1, 1, 4), [(0, 1), (1, 2), (2, 3), (3, 4)],
         [[(1, 0), (2, 1), (3, 2), (4, 3)], [(0, 0), (1, 2), (2, 4)], [(0, 2), (1, 3), (2, 4)]],
         "The pairs are (0, 1), (1, 2), (2, 3), (3, 4): each point is 1 higher than it is far right. "
         "Graph {w0} has x and y switched."),
        ((0, 2, 1, 1, 3), [(0, 1), (2, 2), (4, 3)],
         [[(1, 0), (2, 2), (3, 4)], [(0, 0), (2, 1), (4, 2)], [(0, 1), (1, 2), (2, 3)]],
         "The pairs are (0, 1), (2, 2), (4, 3). Pattern A goes 0, 2, 4, so the points are 2 apart across. "
         "Graph {w0} has x and y switched."),
    ]:
        p = pos.next()
        gs = list(wrongs)
        gs.insert(p, right)
        a, b = seq(sA, kA, n), seq(sB, kB, n)
        w0 = (gs.index(wrongs[0]) + 1)
        q = (ab_table(sA, kA, sB, kB, n) + fig(mini_graphs(gs)) +
             "Which graph shows the ordered pairs (A term, B term) from the table?")
        its.append(mcq_fixed(q, ["Graph 1", "Graph 2", "Graph 3", "Graph 4"], "Graph %d" % (p + 1),
                             "Graph %d. " % (p + 1) + e.format(w0=w0)))
    # B: read a point
    for kA, kB, sx, sy, nx, ny, i in [(1, 2, 1, 1, 5, 9, 3), (2, 6, 2, 3, 5, 8, 2), (3, 6, 3, 3, 5, 9, 3),
                                      (5, 10, 5, 5, 5, 9, 2), (4, 12, 4, 6, 4, 8, 3)]:
        G = pat_grid(kA, kB, sx, sy, nx, ny)
        for t in range(5):
            if t * kA <= nx * sx and t * kB <= ny * sy:
                G.data_point(t * kA, t * kB, "P" if t == i else None)
        x, y = i * kA, i * kB
        cands = [pair(y, x)]
        if sx > 1 or sy > 1:
            cands.append(pair(x // sx, y // sy))
        cands += [pair(x, y - kB), pair(x + kA, y), pair(x, y + sy)]
        e = ("Go down from P to the x-axis: %d. Go across from P to the y-axis: %d. So P is (%d, %d), "
             "the %s terms of A and B." % (x, y, x, y, ordn(i + 1)))
        if sx > 1 or sy > 1:
            e += " Read the numbers on the axes, not the number of grid spaces."
        its.append(mcq(fig(G.svg()) + rules(0, kA, 0, kB) + " Each point is (A term, B term). Which ordered pair does point P show?",
                       pair(x, y), cands, e, rnd))
    # C: which point comes next
    for sA, kA, sB, kB, shown, wrong, nx, ny, sx, sy, why in [
        (0, 1, 0, 2, 4, [(8, 4), (4, 7), (5, 10)], 9, 10, 1, 1,
         "(8, 4) has x and y switched, and (4, 7) adds 1 to the B term instead of 2."),
        (0, 2, 0, 4, 4, [(16, 8), (8, 14), (10, 20)], 9, 10, 2, 2,
         "(16, 8) has x and y switched, and (10, 20) skips a pair: one jump too many."),
        (0, 1, 0, 3, 3, [(9, 3), (3, 7), (2, 9)], 10, 10, 1, 1,
         "(9, 3) has x and y switched, and (2, 9) pairs the 3rd A term with the 4th B term."),
        (0, 1, 3, 1, 4, [(7, 4), (5, 8), (3, 7)], 8, 9, 1, 1,
         "(7, 4) has x and y switched, and (5, 8) is one jump too many."),
    ]:
        G = pat_grid(kA, kB, sx, sy, nx, ny)
        for t in range(shown):
            G.data_point(sA + t * kA, sB + t * kB, None)
        nxt = (sA + shown * kA, sB + shown * kB)
        p = pos.next()
        cand = list(wrong)
        cand.insert(p, nxt)
        for c, L in zip(cand, LET):
            G.data_point(c[0], c[1], L, RED)
        e = ("Point %s. Pattern A adds %d and Pattern B adds %d, so the next pair is %s. "
             % (LET[p], kA, kB, pair(*nxt))) + why
        its.append(mcq_fixed(fig(G.svg()) + rules(sA, kA, sB, kB) + " The green points show the first %d ordered pairs. "
                             "Which red point shows the next ordered pair?" % shown, LET, LET[p], e))
    # D: which point was plotted wrong
    for sA, kA, sB, kB, mk, kind in [(0, 1, 0, 2, "swap", None), (0, 2, 0, 1, "skip", None), (1, 1, 3, 1, "skip", None)]:
        good = [(sA + t * kA, sB + t * kB) for t in range(1, 5)]
        p = pos.next()
        pts = list(good)
        x, y = good[p]
        if mk == "swap":
            pts[p] = (y, x)
            why = "It is at %s, but the pair is %s: x and y are switched." % (pair(y, x), pair(x, y))
        else:
            pts[p] = (x, y + kB)
            why = ("It is at %s, but the %s A term, %d, goes with the %s B term, %d. "
                   "The point uses the next B term." % (pair(x, y + kB), ordn(p + 2), x, ordn(p + 2), y))
        nx = max(5, max(c[0] for c in pts) + 1)
        ny = max(5, max(c[1] for c in pts) + 1)
        G = pat_grid(kA, kB, 1, 1, nx, ny)
        for c, L in zip(pts, LET):
            G.point(c[0], c[1], L)
        q = (fig(G.svg()) + rules(sA, kA, sB, kB) + " Points P, Q, R and S should show the 2nd to 5th ordered pairs "
             "(A term, B term). Which point was plotted wrong?")
        its.append(mcq_fixed(q, LET, LET[p], "Point %s. " % LET[p] + why))
    # E: reading the graph without a picture
    its.append(mcq(rules(0, 3, 0, 9) + " The ordered pairs (A term, B term) are graphed. Which point is also on the graph?",
                   "(15, 45)", ["(45, 15)", "(15, 24)", "(15, 18)"],
                   "Each B term is 3 times the A term, so 15 goes with 45: (15, 45). (15, 24) adds 9 and (15, 18) adds 3 "
                   "instead of using the relationship.", rnd))
    its.append(mcq(rules(0, 2, 0, 6) + " The point (6, 18) is on the graph. How do you get from it to the next point?",
                   "right 2, up 6", ["right 6, up 2", "right 2, up 2", "right 6, up 6"],
                   "The x-coordinate is the A term, which grows by 2. The y-coordinate is the B term, which grows by 6. "
                   "So move right 2 and up 6, to (8, 24).", rnd))
    its.append(mcq("On a graph of (A term, B term), every point has a y-coordinate that is 4 times its x-coordinate. "
                   "What does this tell you?", "Each B term is 4 times the A term",
                   ["Each A term is 4 times the B term", "Each B term is 4 more than the A term", "Pattern B adds 4"],
                   "The x-coordinate is the A term and the y-coordinate is the B term. y = 4 × x means each B term is 4 times "
                   "the corresponding A term.", rnd))
    its.append(mcq(rules(0, 2, 0, 4) + " What do you notice about the graphed points?",
                   "They are on a straight line", ["They make a curve", "They are all on the x-axis", "They go down to the right"],
                   "Each step goes right 2 and up 4, the same move every time, so the points line up in a straight line "
                   "that starts at the origin.", rnd))
    its.append(mcq(rules(0, 5, 0, 15) + " The first graphed point is (0, 0). What does it show?",
                   "Both patterns start at 0", ["Both rules are Add 0", "The patterns are the same", "It is not a pair of terms"],
                   "(0, 0) is the 1st ordered pair: the 1st term of A is 0 and the 1st term of B is 0.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Graph the ordered pairs", "items": its}


# ------------------------------------------------------------ set 5: word problems
def savings_grid(label_pt=True):
    G = Grid(5, 9, sx=3, sy=3, xt="Maya ($)", yt="Leo ($)")
    for t in range(5):
        G.data_point(3 * t, 6 * t, "P" if (label_pt and t == 3) else None)
    return G.svg("graph of Maya's and Leo's savings")


def set_words(rnd):
    its = []
    sv = "Maya and Leo both start with $0. Each week Maya saves $3 and Leo saves $6. "
    its.append(mcq_num(sv + "How much has Leo saved after 5 weeks?", 30, [36, 15, 24],
                       "Leo's pattern: $0, $6, $12, $18, $24, $30. After 5 weeks he has 5 × $6 = $30. "
                       "($36 is one week too many.)", fmt=money))
    its.append(mcq(sv + "Which is true every week?", "Leo has 2 times as much",
                   ["Leo has $3 more", "Maya has 2 times as much", "Leo has $6 more"],
                   "Week 1: $3 and $6. Week 2: $6 and $12. Week 3: $9 and $18. Leo always has 2 times as much, "
                   "because he saves 2 times as much each week. The difference grows ($3, $6, $9), so “$3 more” is wrong.", rnd))
    its.append(mcq_num(sv + "When Maya has $24, how much does Leo have?", 48, [27, 30, 12],
                       "Leo always has 2 times as much as Maya: 2 × $24 = $48. (Maya has $24 after 8 weeks, and 8 × $6 = $48.)",
                       fmt=money))
    its.append(mcq(fig(savings_grid()) + sv + "The graph shows (Maya's savings, Leo's savings). What does point P mean?",
                   "Maya has $9 when Leo has $18.",
                   ["Maya has $18 when Leo has $9.", "Leo saves $18 each week.", "After 9 weeks, Leo has $18."],
                   "P is at (9, 18). The x-axis is Maya's money and the y-axis is Leo's money, so when Maya has $9, Leo has $18 "
                   "(after 3 weeks).", rnd))
    its.append(mcq(fig(savings_grid(False)) + sv + "The graph shows (Maya's savings, Leo's savings). Which ordered pair comes after (12, 24)?",
                   "(15, 30)", ["(15, 27)", "(30, 15)", "(18, 36)"],
                   "Each week Maya's savings go up $3 and Leo's go up $6: (12 + 3, 24 + 6) = (15, 30). "
                   "(15, 27) adds $3 to both.", rnd))
    lem = "A lemonade recipe uses 1 cup of lemon juice for every 4 cups of water. "
    its.append(mcq_num(lem + "Lemon juice: 1, 2, 3, … cups. Water: 4, 8, 12, … cups. How many cups of water go with 5 cups of lemon juice?",
                       20, [9, 8, 16],
                       "The water pattern adds 4 and the juice pattern adds 1, so the water is always 4 times the juice: "
                       "5 × 4 = 20 cups. (5 + 4 = 9 adds instead of multiplying.)", fmt=lambda v: "%d cups" % v))
    its.append(mcq(lem + "The ordered pairs are (cups of lemon juice, cups of water). Which ordered pair fits the recipe?",
                   "(3, 12)", ["(12, 3)", "(3, 7)", "(4, 12)"],
                   "3 cups of juice need 3 × 4 = 12 cups of water. Juice comes first: (3, 12). (3, 7) adds 4 instead.", rnd))
    hk = "Ava and Ben start hiking at the same time from the same place. Ava hikes 2 miles each hour and Ben hikes 4 miles each hour. "
    its.append(mcq_num(hk + "How far has Ben hiked when Ava has hiked 7 miles?", 14, [9, 11, 28],
                       "Each hour Ben hikes 2 times as far as Ava, and both start at 0, so Ben's distance is always 2 times Ava's: "
                       "2 × 7 = 14 miles.", fmt=lambda v: "%d miles" % v))
    its.append(mcq(hk + "Why is Ben's distance always 2 times Ava's distance?",
                   "Both start at 0, and 4 is 2 × 2",
                   ["Ben always hikes 2 more miles", "Ben started first", "They hike for the same time"],
                   "Every hour Ben adds 4 miles and Ava adds 2 miles. 4 = 2 × 2, so after any number of hours Ben has added "
                   "2 times as much. Because both started at 0, Ben's total is always 2 times Ava's.", rnd))
    its.append(mcq_num("For a fundraiser, Class A raises $150 each week and Class B raises $450 each week. Both start at $0. "
                       "How much has Class B raised after 8 weeks?", 3600, [4050, 1200, 3150],
                       "Class B adds $450 each week: 8 × $450 = $3,600. It is also 3 times Class A's $1,200. "
                       "($4,050 is one week too many.)", fmt=money))
    its.append(mcq_num("Two empty tanks are filled with water. Tank A gets 25 liters each minute and tank B gets 100 liters each minute. "
                       "When tank A has 500 liters, how much does tank B have?", 2000, [575, 600, 125],
                       "100 = 4 × 25, and both start empty, so tank B always has 4 times as much: 500 × 4 = 2,000 liters.",
                       fmt=lambda v: "%s liters" % f(v)))
    its.append(mcq_num("Zoe is 8 years old and her brother is 5. Each year, both get 1 year older. How old will Zoe be when her brother is 12?",
                       15, [36, 9, 13],
                       "Zoe is 3 years older (8 − 5 = 3), and both add 1 each year, so she stays 3 years older: 12 + 3 = 15. "
                       "(12 × 3 = 36 treats it as times.)", fmt=lambda v: "%d years old" % v))
    its.append(mcq("Zoe is 8 years old and her brother is 5. Why will Zoe always be 3 years older than her brother?",
                   "Both get 1 year older each year",
                   ["Zoe gets 3 years older each year", "Zoe's age is 3 times his age", "Her brother grows more slowly"],
                   "The difference starts at 8 − 5 = 3. Each year both ages add the same number, 1, so the difference stays 3: "
                   "8 and 5, 9 and 6, 10 and 7.", rnd))
    its.append(mcq_num("Nora swims 2 laps each day and Sam swims 6 laps each day. They start on the same day. "
                       "When Sam has swum 42 laps in all, how many laps has Nora swum?", 14, [126, 38, 40],
                       "6 = 3 × 2, so Sam's total is always 3 times Nora's. Work backward: 42 ÷ 3 = 14 laps. "
                       "(Both have swum for 7 days: 7 × 2 = 14.)", fmt=lambda v: "%d laps" % v))
    its.append(mcq("A motorcycle has 2 wheels and a car has 4 wheels. The ordered pairs are (wheels on the motorcycles, wheels on the cars) "
                   "for the same number of each. Which ordered pair is for 7 motorcycles and 7 cars?",
                   "(14, 28)", ["(28, 14)", "(7, 28)", "(2, 4)"],
                   "7 motorcycles have 7 × 2 = 14 wheels and 7 cars have 7 × 4 = 28 wheels: (14, 28). "
                   "(7, 28) uses the number of motorcycles, not their wheels, and (2, 4) is for only 1 of each.", rnd))
    its.append(mcq("Maya's pattern starts at 0 and adds 4. Leo wants each term of his pattern to be 3 times the matching term of Maya's. "
                   "His pattern also starts at 0. Which rule should he use?",
                   "Add 12", ["Add 7", "Add 3", "Add 4"],
                   "Each step Leo must add 3 times as much as Maya: 3 × 4 = 12. Check: 4 and 12, 8 and 24, 12 and 36. "
                   "(Add 7 is 4 + 3.)", rnd))
    its.append(mcq("Ruby's Pattern A starts at 2 and adds 6. She wants each term of Pattern B to be 5 more than the matching A term. "
                   "Which start and rule should Pattern B have?",
                   "Start at 7, Add 6",
                   ["Start at 2, Add 11", "Start at 7, Add 11", "Start at 10, Add 30"],
                   "To stay 5 more, B must start 5 higher (2 + 5 = 7) and grow by the same amount, 6. Adding 11 each time "
                   "would make the difference grow: 7 and 2, 18 and 8.", rnd))
    its.append(mcq_num("Printer A prints 120 pages each minute and printer B prints 480 pages each minute. They start at the same time. "
                       "When printer A has printed 1,080 pages, how many has printer B printed?", 4320, [1560, 1440, 270],
                       "480 = 4 × 120, so printer B always prints 4 times as many pages: 1,080 × 4 = 4,320 pages.",
                       fmt=lambda v: "%s pages" % f(v)))
    its.append(mcq("Ava reads 10 pages each day and Eli reads 30 pages each day, starting on the same day. "
                   "Ava says Eli has always read 20 more pages than she has. Is she right?",
                   "No, he has read 3 times as many",
                   ["Yes, 30 − 10 = 20", "Yes, the difference stays 20", "No, he has read 20 times as many"],
                   "Day 1: 10 and 30 (20 more). Day 2: 20 and 60 (40 more). The difference grows, but Eli's total is always "
                   "3 times Ava's, because 30 = 3 × 10.", rnd))
    its.append(mcq("A pancake recipe uses 2 cups of flour for every 1 cup of milk. The ordered pairs (cups of milk, cups of flour) "
                   "are graphed. Which point is <b>not</b> on the graph?",
                   "(8, 4)", ["(2, 4)", "(5, 10)", "(7, 14)"],
                   "The flour is always 2 times the milk, and milk comes first. (8, 4) has the numbers switched: "
                   "8 cups of milk would need 16 cups of flour.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: two patterns in real life", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(5, 9, sx=3, sy=3, xt="Pattern A", yt="Pattern B")
    for t in range(5):
        G.data_point(3 * t, 6 * t, None)
    G.note(3.3, 6, "(9, 18)", anchor="start")
    graph = G.svg("graph of the ordered pairs (0, 0), (3, 6), (6, 12), (9, 18), (12, 24)")
    return (
        "<h2>Two rules make two patterns</h2>"
        "<p>Each pattern has a <b>start number</b> and a <b>rule</b>. Write the start number first, "
        "then use the rule again and again. Put the two patterns in a table so the terms in the same place line up.</p>" +
        table(["Term", "1st", "2nd", "3rd", "4th", "5th"], [
            ["Pattern A: start 0, Add 3", "0", "3", "6", "9", "12"],
            ["Pattern B: start 0, Add 6", "0", "6", "12", "18", "24"],
        ]) +
        "<h2>Compare corresponding terms</h2>"
        "<p><b>Corresponding terms</b> are in the same place: the 3rd term of A (6) and the 3rd term of B (12). "
        "Compare down each column: 3 × 2 = 6, 6 × 2 = 12, 9 × 2 = 18. Each B term is <b>2 times</b> the A term.</p>"
        "<p><b>Why?</b> Both patterns start at 0, and every step B adds 6 while A adds 3. 6 is 2 × 3, so B has always "
        "added 2 times as much as A.</p>" +
        ex("Example", "Pattern A: start at 0, Add 4. Pattern B: start at 0, Add 12. A term of A is 20. What is the B term?",
           "12 = 3 × 4, so each B term is 3 times the A term. 20 × 3 = 60.", "60") +
        "<p>If both patterns add the <b>same</b> number but start at different numbers, the difference stays the same: "
        "start 0 and start 4, both Add 3, gives 0 and 4, 3 and 7, 6 and 10. B is always 4 more than A.</p>"
        "<h2>Make ordered pairs</h2>"
        "<p>Write each column as an ordered pair (A term, B term): (0, 0), (3, 6), (6, 12), (9, 18), (12, 24). "
        "The A term comes first.</p>"
        "<h2>Graph the ordered pairs</h2>"
        "<figure class='sn-fig'>" + graph +
        "<figcaption>Each step goes right 3 (A adds 3) and up 6 (B adds 6), so the points lie on a straight line. "
        "Each axis here counts by 3.</figcaption></figure>" +
        ex("Example", "Which ordered pair comes after (12, 24)?",
           "A adds 3 and B adds 6: (12 + 3, 24 + 6).", "(15, 30)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Comparing only the first pair: 3 and 6, so “B is 3 more”", "Check every column: 6 and 12 are 6 apart, but B is always 2 times A"],
            ["Mixing up the rule and the relationship", "The rule (Add 6) goes along a row. The relationship (2 times) goes down a column"],
            ["Switching the order: (6, 3)", "Write (A term, B term): (3, 6)"],
            ["Pairing terms from different places, like (6, 18)", "Pair the 3rd term with the 3rd term: (6, 12)"],
            ["Counting grid spaces on a scaled axis", "Read the numbers on the axes"],
        ])
    )


FAQ = [
    {"q": "What does 5.OA.B.3 mean?",
     "a": "It is the Common Core Grade 5 standard for making two number patterns from two rules, comparing the terms in the same place, writing them as ordered pairs and graphing them on a coordinate plane."},
    {"q": "What are corresponding terms?",
     "a": "They are the terms in the same place in two patterns, such as the 4th term of Pattern A and the 4th term of Pattern B. With Add 3 and Add 6 from 0, the 4th terms are 9 and 18."},
    {"q": "Why is one pattern twice the other when the rules are Add 3 and Add 6?",
     "a": "Both start at 0, and each step the second pattern adds 6, which is 2 times 3. So it has always added twice as much, and each term is 2 times the matching term."},
    {"q": "How do you graph two numerical patterns?",
     "a": "Pair the terms in the same place as (first pattern term, second pattern term), then plot each pair: go right by the first number and up by the second."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    (graph numbers, point letters, numbers from small to large) stay as they are; the other questions fill the gaps."""
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


def gen_patterns():
    rnd = random.Random(516)
    sets = [set_generate(rnd), set_relationship(rnd), set_pairs(rnd), set_graph(rnd), set_words(rnd)]
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
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "patterns-and-relationships", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Patterns and Relationships: Two Rules, Ordered Pairs and Graphs",
        "seo_title": "Grade 5 Numerical Patterns Worksheets: Two Rules, Corresponding Terms, Ordered Pairs and Graphs (5.OA.B.3)",
        "short_title": "Patterns and relationships",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "5.OA.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/OA/B/3/",
        "standard_text": "Generate two numerical patterns using two given rules. Identify apparent relationships between corresponding terms. Form ordered pairs consisting of corresponding terms from the two patterns, and graph the ordered pairs on a coordinate plane. For example, given the rule “Add 3” and the starting number 0, and given the rule “Add 6” and the starting number 0, generate terms in the resulting sequences, and observe that the terms in one sequence are twice the corresponding terms in the other sequence. Explain informally why this is so.",
        "meta_desc": "Free Grade 5 numerical patterns worksheets: make two patterns from two rules, find the relationship between corresponding terms, form ordered pairs and graph them on a coordinate plane, plus word problems. 100 practice questions with answers.",
        "key_big": "Compare terms in the same place. Add 3 and Add 6 from 0 give 3 and 6, 6 and 12, 9 and 18: B is always 2 times A.",
        "key_sub": "Why: every step B adds 6, which is 2 times 3, so B has always added twice as much. Write each pair as (A term, B term) and graph it: right by the A term, up by the B term.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (tables and graphs) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_patterns()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(two patterns table|graph of|four graphs)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
