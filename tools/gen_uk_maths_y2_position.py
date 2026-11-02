# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Position and direction (National Curriculum in England, Geometry – position and direction)
  python tools/gen_uk_maths_y2_position.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 2 pupils (6–7 years old) describe where things are (above, below, on the left of, on the right of,
between, next to), move in straight lines on a grid, make quarter, half and three-quarter turns clockwise
and anticlockwise (a quarter turn is a right angle), and continue repeating and turning patterns.
Left and right in a picture mean the left and right of the page, unless a robot or a person turns:
then it is THEIR left or right. Every answer is worked out in code (grid moves, turns, patterns).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRID = "#9a948a"
GRAY = "#c9c2b8"
YELLOW = "#f2c94c"
RED = "#e06666"
BLUE = "#9fc5e8"
ORANGE = "#f6a04d"
PINK = "#f4a6c0"
BROWN = "#a0692a"
STONE = "#b7b2aa"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

DIRS = ["up", "right", "down", "left"]                 # clockwise order on the page
DV = [(0, -1), (1, 0), (0, 1), (-1, 0)]
TURNS = ["quarter turn", "half turn", "three-quarter turn", "whole turn"]


# ------------------------------------------------------------ question helpers
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
    """Choices keep their order (A B C D, directions, turns, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c > 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Pos:
    """Positions for letter answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ geometry
def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dirv(deg):
    """Direction for an angle in degrees, anticlockwise on screen (SVG y goes down)."""
    t = math.radians(deg)
    return (math.cos(t), -math.sin(t))


def P(pts):
    return " ".join("%.1f,%.1f" % p for p in pts)


# ------------------------------------------------------------ small pictures (centred on cx, cy; s = half size)
def star_pts(cx, cy, s, n=5):
    out = []
    for i in range(2 * n):
        r = s if i % 2 == 0 else s * 0.45
        out.append(add((cx, cy), dirv(90 + 180.0 * i / n), r))
    return out


def icon(kind, cx, cy, s=18):
    k = s / 18.0
    st = "stroke='%s' stroke-width='2' stroke-linejoin='round'" % GREEN
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' %s/>" % (cx, cy, 15 * k, FILL, st)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' %s/>" % (cx - 14 * k, cy - 14 * k, 28 * k, 28 * k, FILL, st)
    if kind == "triangle":
        return "<polygon points='%s' fill='%s' %s/>" % (P([(cx, cy - 16 * k), (cx + 17 * k, cy + 13 * k), (cx - 17 * k, cy + 13 * k)]), FILL, st)
    if kind == "star":
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>" % (
            P(star_pts(cx, cy + 1.5 * k, 17 * k)), YELLOW, BROWN)
    if kind == "heart":
        pts = [(0, 0.85), (-1.1, 0.05), (-0.9, -0.75), (-0.45, -0.75), (-0.15, -0.75), (0, -0.5), (0, -0.35),
               (0, -0.5), (0.15, -0.75), (0.45, -0.75), (0.9, -0.75), (1.1, 0.05), (0, 0.85)]
        p = [(cx + x * 16 * k, cy + 1 * k + y * 16 * k) for x, y in pts]
        d = "M%.1f,%.1f C%s C%s C%s C%s Z" % (p[0] + (P(p[1:4]), P(p[4:7]), P(p[7:10]), P(p[10:13])))
        return "<path d='%s' fill='%s' stroke='#a33' stroke-width='2' stroke-linejoin='round'/>" % (d, RED)
    if kind == "moon":
        r1, r2 = 15 * k, 12 * k
        a = (cx + 4 * k, cy - 14.5 * k)
        b = (cx + 4 * k, cy + 14.5 * k)
        d = "M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f Z" % (a + (r1, r1) + b + (r2, r2) + a)
        return "<path d='%s' fill='#fff1a8' stroke='%s' stroke-width='2'/>" % (d, BROWN)
    if kind == "sun":
        out = []
        for i in range(8):
            u = dirv(45 * i)
            p, q = add((cx, cy), u, 11 * k), add((cx, cy), u, 17 * k)
            out.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                       % (p + q + (ORANGE,)))
        out.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, 8.5 * k, YELLOW, ORANGE))
        return "".join(out)
    if kind == "tree":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 3 * k, cy + 2 * k, 6 * k, 15 * k, BROWN) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#7cc48a' %s/>" % (cx, cy - 4 * k, 12 * k, st))
    if kind == "house":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f3e3c3' stroke='%s' stroke-width='2'/>"
                % (cx - 12 * k, cy - 2 * k, 24 * k, 18 * k, BROWN) +
                "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
                % (P([(cx - 16 * k, cy - 1 * k), (cx, cy - 16 * k), (cx + 16 * k, cy - 1 * k)]), RED, "#a33") +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 3.5 * k, cy + 6 * k, 7 * k, 10 * k, BROWN))
    if kind == "fish":
        return ("<polygon points='%s' fill='%s' stroke='#b76a1f' stroke-width='2' stroke-linejoin='round'/>"
                % (P([(cx + 6 * k, cy), (cx + 17 * k, cy - 9 * k), (cx + 17 * k, cy + 9 * k)]), ORANGE) +
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='#b76a1f' stroke-width='2'/>"
                % (cx - 3 * k, cy, 13 * k, 9 * k, ORANGE) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx - 9 * k, cy - 2 * k, 1.8 * k, INK))
    if kind == "flower":
        out = ["<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (cx, cy, cx, cy + 17 * k, GREEN)]
        for i in range(5):
            p = add((cx, cy - 3 * k), dirv(90 + 72 * i), 7 * k)
            out.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#c2577a' stroke-width='1.5'/>" % (p[0], p[1], 5.5 * k, PINK))
        out.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy - 3 * k, 4 * k, YELLOW))
        return "".join(out)
    if kind == "ball":
        r = 14 * k
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#3d6f99' stroke-width='2'/>" % (cx, cy, r, BLUE) +
                "<path d='M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' fill='none' stroke='#3d6f99' stroke-width='2'/>"
                % (cx - r, cy, cx, cy - 12 * k, cx + r, cy) +
                "<path d='M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' fill='none' stroke='#3d6f99' stroke-width='2'/>"
                % (cx - r, cy, cx, cy + 12 * k, cx + r, cy))
    if kind == "pond":
        return "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='#3d6f99' stroke-width='2'/>" % (cx, cy + 2 * k, 16 * k, 10 * k, BLUE)
    if kind == "flag":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                % (cx - 8 * k, cy - 16 * k, cx - 8 * k, cy + 16 * k, INK) +
                "<polygon points='%s' fill='%s' stroke='#a33' stroke-width='1.5' stroke-linejoin='round'/>"
                % (P([(cx - 7 * k, cy - 15 * k), (cx + 14 * k, cy - 8 * k), (cx - 7 * k, cy - 1 * k)]), RED))
    if kind == "rock":
        pts = [(-15, 12), (-12, -2), (-4, -11), (8, -9), (15, 2), (13, 12)]
        return "<polygon points='%s' fill='%s' stroke='#6f6a62' stroke-width='2' stroke-linejoin='round'/>" % (
            P([(cx + x * k, cy + y * k) for x, y in pts]), STONE)
    if kind == "chest":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='#6b4316' stroke-width='2'/>"
                % (cx - 15 * k, cy - 10 * k, 30 * k, 22 * k, 3 * k, BROWN) +
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4316' stroke-width='2'/>" % (cx - 15 * k, cy - 2 * k, cx + 15 * k, cy - 2 * k) +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='#6b4316' stroke-width='1.2'/>"
                % (cx - 3 * k, cy - 4 * k, 6 * k, 7 * k, YELLOW))
    if kind == "tent":
        return ("<polygon points='%s' fill='%s' stroke='#b76a1f' stroke-width='2' stroke-linejoin='round'/>"
                % (P([(cx, cy - 15 * k), (cx + 17 * k, cy + 13 * k), (cx - 17 * k, cy + 13 * k)]), ORANGE) +
                "<polygon points='%s' fill='#fff3e0' stroke='#b76a1f' stroke-width='1.5' stroke-linejoin='round'/>"
                % P([(cx, cy - 1 * k), (cx + 6 * k, cy + 13 * k), (cx - 6 * k, cy + 13 * k)]))
    raise KeyError(kind)


def arrow(cx, cy, d, L=34, col=GREEN, w=7):
    """Thick arrow through (cx, cy) pointing in page direction d (0 up, 1 right, 2 down, 3 left)."""
    u = DV[d]
    tip = (cx + u[0] * L / 2, cy + u[1] * L / 2)
    tail = (cx - u[0] * L / 2, cy - u[1] * L / 2)
    base = (tip[0] - u[0] * 13, tip[1] - u[1] * 13)
    nr = (-u[1], u[0])
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>" % (tail + base + (col, w)) +
            "<polygon points='%s' fill='%s'/>" % (P([tip, add(base, nr, 10), add(base, nr, -10)]), col))


def robot(cx, cy, d):
    u = DV[d]
    nr = (-u[1], u[0])
    tip = (cx + u[0] * 9, cy + u[1] * 9)
    b = (cx - u[0] * 4, cy - u[1] * 4)
    return ("<circle cx='%.1f' cy='%.1f' r='12' fill='%s'/>" % (cx, cy, GREEN) +
            "<polygon points='%s' fill='#ffffff'/>" % P([tip, add(b, nr, 6.5), add(b, nr, -6.5)]))


# ------------------------------------------------------------ position grid and rows
POS_THINGS = ["star", "heart", "moon", "sun", "tree", "house", "fish", "flower", "ball"]


def grid3_svg(g, C=56):
    """3 x 3 grid of pictures. g[r][c] = name."""
    s = []
    for r in range(3):
        for c in range(3):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                     % (4 + c * C, 4 + r * C, C, C, GRID))
            s.append(icon(g[r][c], 4 + c * C + C / 2.0, 4 + r * C + C / 2.0))
    return svg_wrap(3 * C + 8, 3 * C + 9, "".join(s), "grid of 9 pictures: " + ", ".join(", ".join(row) for row in g))


def row_svg(things, C=56, nums=False, label=None):
    s = []
    H = C + (22 if nums else 0)
    s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (C - 2, len(things) * C + 4, C - 2, BROWN))
    for i, t in enumerate(things):
        s.append(icon(t, 4 + i * C + C / 2.0, C / 2.0 - 3))
        if nums:
            s.append(text(4 + i * C + C / 2.0, C + 16, str(i + 1), 15))
    return svg_wrap(len(things) * C + 8, H + 2, "".join(s), label or "row of pictures: " + ", ".join(things))


def pattern_svg(things, gap_at=None, nums=False, C=46, label=None):
    """A row of shapes (or 'up'/'right'/... arrows). gap_at: index drawn as a dashed box with '?'.
    A trailing None is drawn as a '?' box too."""
    s = []
    for i, t in enumerate(things):
        cx, cy = 4 + i * C + C / 2.0, 4 + C / 2.0
        if t is None or i == gap_at:
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='#ffffff' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (cx - C / 2.0 + 4, cy - C / 2.0 + 4, C - 8, C - 8, INK))
            s.append(text(cx, cy + 7, "?", 20))
        elif t in DIRS:
            s.append(arrow(cx, cy, DIRS.index(t), L=32, w=6))
        else:
            s.append(icon(t, cx, cy, 16))
        if nums:
            s.append(text(cx, C + 22, str(i + 1), 15))
    W = len(things) * C + 8
    H = C + 8 + (22 if nums else 0)
    names = ["?" if (t is None or i == gap_at) else (t + " arrow" if t in DIRS else t) for i, t in enumerate(things)]
    return svg_wrap(W, H, "".join(s), label or "pattern: " + ", ".join(names))


# ------------------------------------------------------------ robot grid
GC, GR, CS = 6, 5, 34


def map_svg(objs, cols=GC, rows=GR, C=CS, label="grid"):
    """objs: list of (col, row, kind, arg). kind: 'robot' (arg = direction), 'letter' (arg = A-D),
    or an icon name."""
    s = ["<rect x='4' y='4' width='%d' height='%d' fill='#ffffff'/>" % (cols * C, rows * C)]
    for i in range(cols + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.3'/>" % (4 + i * C, 4 + i * C, 4 + rows * C, GRID))
    for j in range(rows + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.3'/>" % (4 + j * C, 4 + cols * C, 4 + j * C, GRID))
    taken = set()
    for c, r, kind, arg in objs:
        assert 0 <= c < cols and 0 <= r < rows, (c, r)
        assert (c, r) not in taken, ("two things in one square", c, r)
        taken.add((c, r))
        cx, cy = 4 + c * C + C / 2.0, 4 + r * C + C / 2.0
        if kind == "robot":
            s.append(robot(cx, cy, arg))
        elif kind == "letter":
            s.append(text(cx, cy + 6.5, arg, 18))
        else:
            s.append(icon(kind, cx, cy, 14))
    return svg_wrap(cols * C + 8, rows * C + 8, "".join(s), label)


def run(start, d, cmds, cols=GC, rows=GR):
    """Follow the instructions. Returns (end square, facing) or None if the robot leaves the grid."""
    x, y = start
    for c in cmds:
        if c == "R":
            d = (d + 1) % 4
        elif c == "L":
            d = (d + 3) % 4
        else:
            k, n = c
            sg = 1 if k == "F" else -1
            x, y = x + DV[d][0] * n * sg, y + DV[d][1] * n * sg
            if not (0 <= x < cols and 0 <= y < rows):
                return None
    return (x, y), d


def say(cmds):
    out = []
    for c in cmds:
        if c == "R":
            out.append("turn right")
        elif c == "L":
            out.append("turn left")
        else:
            k, n = c
            out.append("%s %d" % ("forwards" if k == "F" else "backwards", n))
    return ", ".join(out)


def mistakes(cmds):
    """Instructions a pupil follows by mistake: left and right mixed up, a forward move one short
    (counting the robot's own square) or one too long, the turn missed out, forwards for backwards."""
    out = []
    if "R" in cmds or "L" in cmds:
        out.append([{"R": "L", "L": "R"}.get(c, c) if isinstance(c, str) else c for c in cmds])
    idx = [i for i, c in enumerate(cmds) if not isinstance(c, str)]
    for i in reversed(idx):
        k, n = cmds[i]
        if n > 1:
            out.append(cmds[:i] + [(k, n - 1)] + cmds[i + 1:])
    for i in reversed(idx):
        k, n = cmds[i]
        out.append(cmds[:i] + [(k, n + 1)] + cmds[i + 1:])
    if "R" in cmds or "L" in cmds:
        out.append([c for c in cmds if not isinstance(c, str)])
    for i in idx:
        k, n = cmds[i]
        out.append(cmds[:i] + [("B" if k == "F" else "F", n)] + cmds[i + 1:])
    return out


FACE_TXT = ["faces up the page", "faces right", "faces down the page", "faces left"]


def letters_q(q_head, start, d, cmds, pos, e, extra=None):
    end = run(start, d, cmds)
    assert end, (start, cmds)
    ans = end[0]
    cells = []
    for m in mistakes(cmds):
        r = run(start, d, m)
        if r and r[0] != ans and r[0] != start and r[0] not in cells:
            cells.append(r[0])
    for c in (extra or []):
        if c != ans and c != start and c not in cells:
            cells.append(c)
    assert len(cells) >= 3, (start, cmds, cells)
    cells = cells[:3]
    p = pos.next()
    order = cells[:]
    order.insert(p, ans)
    objs = [(start[0], start[1], "robot", d)] + [(c[0], c[1], "letter", "ABCD"[i]) for i, c in enumerate(order)]
    svg = map_svg(objs, label="grid with a robot and squares A to D")
    return mcq_fixed(fig(svg) + q_head, ["A", "B", "C", "D"], "ABCD"[p], e)


# ------------------------------------------------------------ turns
def turn_fig_svg(frac, cw=True, r=28):
    """Dashed start line pointing up, a curved arrow for the turn and a solid end line."""
    s = []
    c = (60.0, 52.0)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-dasharray='5 4'/>"
             % (c + add(c, dirv(90), r + 12) + (INK,)))
    sweep = 360.0 * frac
    sg = -1 if cw else 1
    draw = min(sweep - 20, 330.0)
    n = max(8, int(draw / 5))
    pts = [add(c, dirv(90 + sg * draw * i / n), r) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (P(pts), GREEN))
    end_a = 90 + sg * draw
    d = dirv(end_a + sg * 90)
    tip = add(add(c, dirv(end_a), r), d, 8)
    nr = (-d[1], d[0])
    b = add(tip, d, -11)
    s.append("<polygon points='%s' fill='%s'/>" % (P([tip, add(b, nr, 7), add(b, nr, -7)]), GREEN))
    if frac < 1:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (c + add(c, dirv(90 + sg * sweep), r + 12) + (INK,)))
    s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (c + (INK,)))
    return s


def turn_svg(frac, cw=True, label=None):
    return svg_wrap(121, 104, "".join(turn_fig_svg(frac, cw)), label or "turn")


def turns_strip_svg(items, label):
    """items: (frac, cw, caption)."""
    s = []
    for k, (frac, cw, cap) in enumerate(items):
        s.append("<g transform='translate(%d,0)'>%s</g>" % (k * 124 + 2, "".join(turn_fig_svg(frac, cw))))
        s.append(text(k * 124 + 62, 122, cap, 15))
    return svg_wrap(124 * len(items) + 4, 130, "".join(s), label)


def arrow_svg(d, label=None):
    s = ("<circle cx='40' cy='40' r='34' fill='#ffffff' stroke='%s' stroke-width='1.5' stroke-dasharray='3 4'/>" % GRAY +
         arrow(40, 40, d, L=52, w=8))
    return svg_wrap(81, 80, s, label or "arrow pointing " + DIRS[d])


def facing_svg(names, face, label):
    """A child (circle) in the middle with an arrow to the way they face; things on the 4 sides."""
    W, H = 260, 150
    cx, cy = W / 2.0, H / 2.0
    s = []
    for i, t in enumerate(names):
        if i == 0:
            s.append(text(cx, 20, t, 16))
        elif i == 1:
            s.append(text(cx + 52, cy + 6, t, 16, "start"))
        elif i == 2:
            s.append(text(cx, H - 8, t, 16))
        else:
            s.append(text(cx - 52, cy + 6, t, 16, "end"))
    s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='%s' stroke-width='2.5'/>" % (cx, cy, FILL, GREEN))
    u = DV[face]
    a = (cx + u[0] * 13, cy + u[1] * 13)
    tip = (cx + u[0] * 40, cy + u[1] * 40)
    b = (cx + u[0] * 30, cy + u[1] * 30)
    nr = (-u[1], u[0])
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.4'/>" % (a + b + (INK,)))
    s.append("<polygon points='%s' fill='%s'/>" % (P([tip, add(b, nr, 7), add(b, nr, -7)]), INK))
    return svg_wrap(W, H, "".join(s), label)


def clock_turn_svg(start, quarters):
    """Minute hand: dashed where it started, solid where it ends after `quarters` quarter turns clockwise."""
    c = (56.0, 56.0)
    s = ["<circle cx='56' cy='56' r='52' fill='#ffffff' stroke='%s' stroke-width='3'/>" % GREEN]
    for i in range(12):
        d = dirv(90 - 30 * i)
        a, b = add(c, d, 47), add(c, d, 41 if i % 3 == 0 else 44)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>"
                 % (a + b + (INK, 2.4 if i % 3 == 0 else 1.4)))
    for num, i in (("12", 0), ("3", 3), ("6", 6), ("9", 9)):
        p = add(c, dirv(90 - 30 * i), 33)
        s.append(text(p[0], p[1] + 5.4, num, 15))
    a0 = 90 - 30 * start
    sweep = min(90 * quarters - 24, 330)
    n = max(8, int(sweep / 5))
    r = 15
    pts = [add(c, dirv(a0 - sweep * i / n), r) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (P(pts), GREEN))
    ea = a0 - sweep
    d = dirv(ea - 90)
    tip = add(add(c, dirv(ea), r), d, 8)
    nr = (-d[1], d[0])
    b = add(tip, d, -10)
    s.append("<polygon points='%s' fill='%s'/>" % (P([tip, add(b, nr, 6), add(b, nr, -6)]), GREEN))
    p0 = add(c, dirv(a0), 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-dasharray='4 3'/>" % (p0 + (INK,)))
    p1 = add(c, dirv(a0 - 90 * quarters), 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (p1 + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock with the minute hand turning")


# ------------------------------------------------------------ set 1: position words
def find(g, t):
    for r in range(3):
        for c in range(3):
            if g[r][c] == t:
                return r, c
    raise KeyError(t)


def rel_word(g, a, b):
    """Where is a, compared with b (next to each other)?"""
    ra, ca = find(g, a)
    rb, cb = find(g, b)
    return {(-1, 0): "above", (1, 0): "below", (0, -1): "on the left of", (0, 1): "on the right of"}[(ra - rb, ca - cb)]


REL = ["above", "below", "on the left of", "on the right of"]


def set_position(rnd, P_):
    its = []
    pool = POS_THINGS[:]
    rnd.shuffle(pool)
    g1 = [pool[0:3], pool[3:6], pool[6:9]]
    rnd.shuffle(pool)
    g2 = [pool[0:3], pool[3:6], pool[6:9]]
    s1, s2 = fig(grid3_svg(g1)), fig(grid3_svg(g2))
    the = lambda t: "the " + t

    def at(g, r, c):
        return the(g[r][c])

    # grid 1
    x = g1[1][0]
    its.append(mcq(s1 + "What is <b>above</b> the %s?" % x, at(g1, 0, 0), [at(g1, 2, 0), at(g1, 0, 1), at(g1, 1, 1)],
                   "Above means higher up. Look up from the %s: the next picture is %s." % (x, at(g1, 0, 0)), rnd))
    x = g1[1][2]
    its.append(mcq(s1 + "What is <b>below</b> the %s?" % x, at(g1, 2, 2), [at(g1, 0, 2), at(g1, 2, 1), at(g1, 1, 1)],
                   "Below means lower down. Look down from the %s: the next picture is %s." % (x, at(g1, 2, 2)), rnd))
    x = g1[0][1]
    its.append(mcq(s1 + "What is <b>on the left of</b> the %s?" % x, at(g1, 0, 0), [at(g1, 0, 2), at(g1, 1, 1), at(g1, 1, 0)],
                   "Look to the left side of the page. On the left of the %s is %s. %s is on the right."
                   % (x, at(g1, 0, 0), at(g1, 0, 2).capitalize()), rnd))
    x = g1[2][1]
    its.append(mcq(s1 + "What is <b>on the right of</b> the %s?" % x, at(g1, 2, 2), [at(g1, 2, 0), at(g1, 1, 1), at(g1, 1, 2)],
                   "Look to the right side of the page. On the right of the %s is %s. %s is on the left." % (x, at(g1, 2, 2), at(g1, 2, 0).capitalize()), rnd))
    its.append(mcq(s1 + "What is in the <b>middle</b> of the grid?", at(g1, 1, 1), [at(g1, 0, 1), at(g1, 1, 0), at(g1, 2, 2)],
                   "The middle square has a picture above it, below it, on its left and on its right. It is %s." % at(g1, 1, 1), rnd))
    its.append(mcq(s1 + "What is in the <b>top left</b> corner?", at(g1, 0, 0), [at(g1, 0, 2), at(g1, 2, 0), at(g1, 2, 2)],
                   "Top means the top row. Left means the left side. The top left corner is %s." % at(g1, 0, 0), rnd))
    a, b = g1[1][1], g1[1][2]
    its.append(mcq_fixed(s1 + "Where is the %s? It is ___ the %s." % (a, b), REL, rel_word(g1, a, b),
                         "The %s and the %s are in the same row. The %s is on the left side, so it is on the left of the %s." % (a, b, a, b)))
    a, b = g1[0][0], g1[2][0]
    its.append(mcq(s1 + "What is <b>between</b> the %s and the %s?" % (a, b), at(g1, 1, 0), [at(g1, 1, 1), at(g1, 0, 1), at(g1, 2, 1)],
                   "Between means in the middle of two things. Go down from the %s to the %s. The picture in the middle is %s." % (a, b, at(g1, 1, 0)), rnd))
    # grid 2
    x = g2[2][1]
    its.append(mcq(s2 + "What is <b>just above</b> the %s?" % x, at(g2, 1, 1), [at(g2, 0, 1), at(g2, 2, 0), at(g2, 1, 2)],
                   "Look up from the %s. The picture just above it is %s. %s is above that one." % (x, at(g2, 1, 1), at(g2, 0, 1).capitalize()), rnd))
    x = g2[1][0]
    its.append(mcq(s2 + "What is <b>just on the right of</b> the %s?" % x, at(g2, 1, 1), [at(g2, 0, 0), at(g2, 2, 0), at(g2, 1, 2)],
                   "Look to the right side of the page. Just on the right of the %s is %s." % (x, at(g2, 1, 1)), rnd))
    its.append(mcq(s2 + "What is in the <b>bottom right</b> corner?", at(g2, 2, 2), [at(g2, 2, 0), at(g2, 0, 2), at(g2, 0, 0)],
                   "Bottom means the bottom row. Right means the right side. The bottom right corner is %s." % at(g2, 2, 2), rnd))
    a, b = g2[1][0], g2[1][2]
    its.append(mcq(s2 + "What is <b>between</b> the %s and the %s?" % (a, b), at(g2, 1, 1), [at(g2, 0, 1), at(g2, 2, 1), at(g2, 0, 0)],
                   "The %s and the %s are in the middle row. The picture between them is %s." % (a, b, at(g2, 1, 1)), rnd))
    a, b = g2[0][2], g2[1][2]
    its.append(mcq_fixed(s2 + "Where is the %s? It is ___ the %s." % (a, b), REL, rel_word(g2, a, b),
                         "The %s is in the top row, just over the %s. So it is above the %s." % (a, b, b)))
    a, b = g2[2][0], g2[1][0]
    its.append(mcq_fixed(s2 + "Where is the %s? It is ___ the %s." % (a, b), REL, rel_word(g2, a, b),
                         "The %s is in the bottom row, just under the %s. So it is below the %s." % (a, b, b)))
    # rows on a shelf
    rnd.shuffle(pool)
    r1 = pool[:5]
    rnd.shuffle(pool)
    r2 = pool[:5]
    f1, f2 = fig(row_svg(r1)), fig(row_svg(r2))
    its.append(mcq(f1 + "What is <b>next to</b> the %s, on its left?" % r1[2], the(r1[1]), [the(r1[3]), the(r1[0]), the(r1[4])],
                   "Next to means right beside it. Just on the left of the %s is %s." % (r1[2], the(r1[1])), rnd))
    its.append(mcq(f1 + "What is <b>next to</b> the %s, on its right?" % r1[1], the(r1[2]), [the(r1[0]), the(r1[3]), the(r1[4])],
                   "Just on the right of the %s is %s. %s is on its left." % (r1[1], the(r1[2]), the(r1[0]).capitalize()), rnd))
    its.append(mcq(f1 + "What is <b>between</b> the %s and the %s?" % (r1[2], r1[4]), the(r1[3]), [the(r1[1]), the(r1[0]), the(r1[2])],
                   "Find the %s and the %s. The thing in the middle of them is %s." % (r1[2], r1[4], the(r1[3])), rnd))
    pair = lambda a, b: "the %s and the %s" % (a, b)
    its.append(mcq(f1 + "The %s is next to two things. What are they?" % r1[3], pair(r1[2], r1[4]),
                   [pair(r1[1], r1[2]), pair(r1[0], r1[4]), pair(r1[0], r1[1])],
                   "Next to means right beside. On its left is %s. On its right is %s." % (the(r1[2]), the(r1[4])), rnd))
    its.append(mcq(f2 + "What is <b>between</b> the %s and the %s?" % (r2[0], r2[2]), the(r2[1]), [the(r2[3]), the(r2[4]), the(r2[0])],
                   "The thing in the middle of the %s and the %s is %s." % (r2[0], r2[2], the(r2[1])), rnd))
    its.append(mcq(f2 + "What is <b>2nd from the right</b>?", the(r2[3]), [the(r2[1]), the(r2[4]), the(r2[2])],
                   "Start at the right end and count: 1st is %s, 2nd is %s. Counting from the left gives %s, which is wrong."
                   % (the(r2[4]), the(r2[3]), the(r2[1])), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Position words: above, below, left, right and between", "items": its}


# ------------------------------------------------------------ set 2: turns
def set_turns(rnd, P_):
    its = []
    q = "What turn does the arrow show? It starts at the dashed line."
    for frac, cw, ans, e in [
        (0.25, True, "quarter turn", "The arrow goes a quarter of the way round. That is a quarter turn."),
        (0.5, True, "half turn", "The arrow goes halfway round. The end line points the opposite way. That is a half turn."),
        (0.75, False, "three-quarter turn", "The arrow goes three quarters of the way round. That is a three-quarter turn."),
        (1.0, False, "whole turn", "The arrow goes all the way round, back to the dashed line. That is a whole turn."),
    ]:
        its.append(mcq_fixed(fig(turn_svg(frac, cw, ans + (" clockwise" if cw else " anticlockwise"))) + q, TURNS, ans, e))
    DT = ["quarter turn clockwise", "quarter turn anticlockwise", "half turn clockwise", "half turn anticlockwise"]
    q = "Which turn does the arrow show? It starts at the dashed line."
    for frac, cw, e in [
        (0.25, False, "The arrow goes a quarter of the way round, the opposite way to clock hands. That is anticlockwise."),
        (0.5, True, "The arrow goes halfway round, the same way as clock hands. That is a half turn clockwise."),
        (0.25, True, "The arrow goes a quarter of the way round, the same way as clock hands. That is clockwise."),
        (0.5, False, "The arrow goes halfway round, the opposite way to clock hands. That is a half turn anticlockwise."),
    ]:
        name = ("quarter" if frac == 0.25 else "half") + " turn " + ("clockwise" if cw else "anticlockwise")
        its.append(mcq_fixed(fig(turn_svg(frac, cw, name)) + q, DT, name, e))
    its.append(mcq("Which way do the hands on a clock turn?", "clockwise",
                   ["anticlockwise", "both ways", "up and down"],
                   "Clock hands always turn the same way. That way is called clockwise. The other way is anticlockwise.", rnd))
    q = "The arrow points %s. It makes a %s. Which way does it point now?"
    for d, k, cw, e in [
        (0, 1, True, "Clockwise goes up, right, down, left. A quarter turn clockwise from up is right."),
        (0, 1, False, "Anticlockwise goes up, left, down, right. A quarter turn anticlockwise from up is left."),
        (1, 2, True, "A half turn makes the arrow point the opposite way. The opposite of right is left."),
        (3, 3, True, "Count 3 quarter turns clockwise from left: up, right, down."),
    ]:
        end = (d + (k if cw else -k)) % 4
        turn = {1: "quarter turn", 2: "half turn", 3: "three-quarter turn"}[k] + (" clockwise" if cw else " anticlockwise")
        if k == 2:
            turn = "half turn"
        its.append(mcq_fixed(fig(arrow_svg(d)) + q % (DIRS[d], turn), DIRS, DIRS[end], e))
    for n, wrong, t, e in [(1, [2, 3, 4], "a quarter turn", "A quarter turn is 1 right angle: a square corner."),
                           (2, [1, 3, 4], "a half turn", "A half turn is 2 quarter turns, so it is 2 right angles."),
                           (3, [1, 2, 4], "a three-quarter turn", "A three-quarter turn is 3 quarter turns, so it is 3 right angles.")]:
        its.append(mcq_num("How many right angles make %s?" % t, n, wrong, e))
    its.append(mcq("Jack turns through 2 right angles. What turn is that?", "a half turn",
                   ["a quarter turn", "a three-quarter turn", "a whole turn"],
                   "Each right angle is a quarter turn. 2 quarter turns make a half turn.", rnd))
    room = ["door", "window", "board", "sink"]
    n, he, his = P_.next()
    its.append(mcq_fixed(fig(facing_svg(room, 0, "child in a classroom facing the door")) +
                         "%s faces the door. %s makes a half turn. What does %s face now?" % (n, he.capitalize(), he),
                         ["the " + r for r in room], "the board",
                         "A half turn makes you face the opposite way. The board is opposite the door."))
    n, he, his = P_.next()
    its.append(mcq_fixed(fig(facing_svg(room, 3, "child in a classroom facing the sink")) +
                         "%s faces the sink. %s makes a quarter turn clockwise. What does %s face now?" % (n, he.capitalize(), he),
                         ["the " + r for r in room], "the door",
                         "Clockwise goes the same way as clock hands: from the sink round to the door. That is a quarter turn."))
    its.append(mcq("Ava makes a half turn clockwise. Leo makes a half turn anticlockwise. They both start facing the door. What happens?",
                   "They both face the same way", ["Ava faces the door", "They face opposite ways", "Leo faces the door"],
                   "A half turn either way makes you face the opposite way. So Ava and Leo end up facing the same way.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Quarter, half and three-quarter turns", "items": its}


# ------------------------------------------------------------ set 3: patterns
SHAPE_NAMES = ["circle", "square", "triangle", "star", "heart"]


def set_patterns(rnd, P_):
    its = []
    q = "What comes next in the pattern?"
    for unit, shown in [(["circle", "square"], 7), (["triangle", "circle", "star"], 7), (["square", "square", "heart"], 7),
                        (["star", "heart", "heart"], 6), (["circle", "triangle", "square", "triangle"], 6), (["heart", "heart", "circle", "circle"], 7)]:
        seq = [unit[i % len(unit)] for i in range(shown)]
        ans = unit[shown % len(unit)]
        wrong = [seq[-1], unit[0], unit[(shown + 1) % len(unit)]] + [s for s in SHAPE_NAMES if s not in unit]
        e = "The part that repeats is %s. After %s comes %s." % (", ".join(unit), seq[-1], ans)
        if ans == seq[-1]:
            e = "The part that repeats is %s. The %s comes twice, so the next one is a %s again." % (", ".join(unit), ans, ans)
        its.append(mcq(fig(pattern_svg(seq + [None])) + q, ans, wrong, e, rnd))
    q = "What is missing from the pattern?"
    for unit, n, gap in [(["star", "circle"], 8, 5), (["square", "triangle", "triangle"], 8, 4), (["heart", "star", "square"], 8, 2)]:
        seq = [unit[i % len(unit)] for i in range(n)]
        ans = seq[gap]
        wrong = [seq[gap - 1], seq[gap + 1]] + [u for u in unit if u != ans] + [s for s in SHAPE_NAMES if s not in unit]
        its.append(mcq(fig(pattern_svg(seq, gap_at=gap)) + q, ans, wrong,
                       "The pattern repeats %s. Say it along the row: the gap needs %s." % (", ".join(unit), ans), rnd))
    unit = ["star", "heart", "circle"]
    seq = [unit[i % 3] for i in range(6)]
    assert unit[(10 - 1) % 3] == "star"
    its.append(mcq(fig(pattern_svg(seq)) + "The pattern keeps going. What will the <b>10th</b> shape be?", "star",
                   ["heart", "circle", "square"],
                   "Keep counting the pattern: 7 star, 8 heart, 9 circle, 10 star.", rnd))
    unit = ["square", "square", "triangle"]
    seq = [unit[i % 3] for i in range(6)]
    assert unit[(12 - 1) % 3] == "triangle"
    its.append(mcq(fig(pattern_svg(seq)) + "The pattern keeps going. What will the <b>12th</b> shape be?", "triangle",
                   ["square", "circle", "heart"],
                   "Each group of 3 ends with a triangle: the 3rd, 6th, 9th and 12th shapes. So the 12th shape is a triangle.", rnd))
    seq = ["circle", "circle", "star"] * 2
    its.append(mcq(fig(pattern_svg(seq)) + "Which part of the pattern repeats?", "circle, circle, star",
                   ["circle, star", "circle, circle, star, circle", "star, circle"],
                   "Circle, circle, star, then it starts again: circle, circle, star.", rnd))
    q = "The arrows make a turning pattern. What comes next?"
    for seq, e in [
        (["up", "right", "down"], "Each arrow makes a quarter turn clockwise: up, right, down, left. Next is left."),
        (["up", "left", "down"], "Each arrow makes a quarter turn anticlockwise: up, left, down, right. Next is right."),
        (["up", "down", "up", "down", "up"], "Each arrow makes a half turn: up, down, up, down. After up comes down."),
        (["right", "down", "left"], "Each arrow makes a quarter turn clockwise: right, down, left, up. Next is up."),
    ]:
        k = (DIRS.index(seq[1]) - DIRS.index(seq[0])) % 4
        nxt = DIRS[(DIRS.index(seq[-1]) + k) % 4]
        its.append(mcq_fixed(fig(pattern_svg(seq + [None])) + q, DIRS, nxt, e))
    HOW = ["a quarter turn clockwise", "a quarter turn anticlockwise", "a half turn", "no turn"]
    for seq, ans, e in [
        (["left", "up", "right", "down"], "a quarter turn clockwise",
         "Left to up is a quarter turn the same way as clock hands. So each arrow turns a quarter turn clockwise."),
        (["down", "right", "up", "left"], "a quarter turn anticlockwise",
         "Down to right is a quarter turn the opposite way to clock hands. So each arrow turns a quarter turn anticlockwise."),
    ]:
        k = (DIRS.index(seq[1]) - DIRS.index(seq[0])) % 4
        assert all((DIRS.index(seq[i + 1]) - DIRS.index(seq[i])) % 4 == k for i in range(len(seq) - 1))
        assert ans == {1: HOW[0], 3: HOW[1], 2: HOW[2]}[k]
        its.append(mcq_fixed(fig(pattern_svg(seq)) + "How does the arrow turn each time?", HOW, ans, e))
    seq = ["triangle", "star", "circle", "triangle", "star", "star", "triangle", "star"]
    its.append(mcq_fixed(fig(pattern_svg(seq, nums=True)) + "One shape is wrong in this pattern. Which one?",
                         ["shape 4", "shape 5", "shape 6", "shape 7"], "shape 6",
                         "The pattern is triangle, star, circle. Shape 6 should be a circle, but it is a star."))
    n, he, his = P_.next()
    its.append(mcq_num("%s makes a pattern: circle, square, square. %s keeps going until there are 9 shapes. How many squares are there?"
                       % (n, he.capitalize()), 6, [3, 9, 2],
                       "9 shapes make 3 groups of circle, square, square. Each group has 2 squares. 2 + 2 + 2 = 6."))
    assert len(its) == 20, len(its)
    return {"title": "Patterns and sequences of shapes", "items": its}


# ------------------------------------------------------------ set 4: moving on a grid
def set_grid(rnd, P_):
    its = []
    pos = Pos(rnd)
    q = "The robot %s. It goes <b>%s</b>. Where does it stop?"
    straight = [((1, 4), 0, [("F", 3)]), ((0, 1), 1, [("F", 3)]), ((4, 0), 2, [("F", 3)]), ((5, 3), 3, [("F", 2)])]
    for st, d, cmds in straight:
        n = cmds[0][1]
        e = "Move %d squares %s, one square at a time. Do not count the square the robot starts on." % (
            n, ["up", "to the right", "down", "to the left"][d])
        side = [(st[0] + DV[(d + 1) % 4][0] * n, st[1] + DV[(d + 1) % 4][1] * n), (st[0] + DV[(d + 3) % 4][0] * n, st[1] + DV[(d + 3) % 4][1] * n)]
        side = [c for c in side if 0 <= c[0] < GC and 0 <= c[1] < GR]
        its.append(letters_q(q % (FACE_TXT[d], say(cmds)), st, d, cmds, pos, e, extra=side))
    turn = [((0, 4), 0, [("F", 2), "R", ("F", 3)]), ((5, 4), 0, [("F", 3), "L", ("F", 2)]),
            ((1, 0), 1, [("F", 3), "R", ("F", 2)]), ((5, 1), 3, [("F", 2), "L", ("F", 2)])]
    for st, d, cmds in turn:
        d2 = run(st, d, cmds[:2])[1]
        e = "Go %s first. Turning %s makes the robot face %s. Then go %s." % (
            say(cmds[:1]), "right" if "R" in cmds else "left", ["up the page", "right", "down the page", "left"][d2], say(cmds[2:]))
        its.append(letters_q(q % (FACE_TXT[d], say(cmds)), st, d, cmds, pos, e))
    for st, d, cmds in [((3, 0), 2, [("F", 2), "L", ("F", 2)]), ((2, 0), 2, [("F", 3), "R", ("F", 2)])]:
        lr = "left" if "L" in cmds else "right"
        page = "right" if lr == "left" else "left"
        e = ("The robot faces down the page, so its %s is on the %s of the page. Turn the page upside down to check. "
             "Go %s, turn %s (towards the %s of the page), then %s." % (lr, page, say(cmds[:1]), lr, page, say(cmds[2:])))
        its.append(letters_q(q % (FACE_TXT[d], say(cmds)), st, d, cmds, pos, e))
    for st, d, cmds, ext in [((2, 2), 0, [("B", 2)], [(2, 1)]), ((3, 2), 1, [("B", 2)], [])]:
        e = "Backwards means the robot moves the opposite way to where it faces, without turning. Move 2 squares %s." % (
            ["down", "to the left"][d])
        its.append(letters_q(q % (FACE_TXT[d], say(cmds)), st, d, cmds, pos, e, extra=ext))
    q = "The robot %s. How many squares must it go forwards to reach the star?"
    for st, d, star, wr in [((0, 3), 1, (4, 3), [5, 3, 2]), ((2, 0), 2, (2, 3), [4, 2, 5]), ((5, 4), 3, (3, 4), [3, 4, 5])]:
        n = abs(star[0] - st[0]) + abs(star[1] - st[1])
        assert run(st, d, [("F", n)])[0] == star
        svg = map_svg([(st[0], st[1], "robot", d), (star[0], star[1], "star", None)], label="grid with a robot and a star")
        its.append(mcq_num(fig(svg) + q % FACE_TXT[d], n, wr,
                           "Count the moves, not the robot’s own square. %d squares forwards takes the robot to the star." % n))
    TF = ["turn left", "turn right", "make a half turn", "no turn"]
    for st, d, star, ans, e in [
        ((2, 3), 0, (5, 3), "turn right", "The robot faces up the page. The star is on its right side, so it turns right: a quarter turn clockwise."),
        ((2, 1), 2, (5, 1), "turn left", "The robot faces down the page, so its left is on the right of the page. It turns left to face the star."),
        ((3, 2), 1, (0, 2), "make a half turn", "The star is behind the robot. A half turn makes it face the opposite way."),
    ]:
        dd = [k for k in range(4) if (star[0] - st[0]) * DV[k][0] + (star[1] - st[1]) * DV[k][1] > 0 and
              (star[0] - st[0]) * DV[k][1] - (star[1] - st[1]) * DV[k][0] == 0][0]
        assert ans == {1: "turn right", 3: "turn left", 2: "make a half turn", 0: "no turn"}[(dd - d) % 4]
        svg = map_svg([(st[0], st[1], "robot", d), (star[0], star[1], "star", None)], label="grid with a robot and a star")
        its.append(mcq_fixed(fig(svg) + "The robot %s. What must it do to face the star?" % FACE_TXT[d], TF, ans, e))
    for st, d, star, cmds, wrongs, e in [
        ((0, 4), 0, (4, 2), [("F", 2), "R", ("F", 4)],
         [[("F", 2), "L", ("F", 4)], [("F", 4), "R", ("F", 2)], [("F", 3), "R", ("F", 5)]],
         "Go up 2 squares. Turn right to face the right of the page. Then go 4 squares to reach the star."),
        ((5, 1), 2, (2, 3), [("F", 2), "R", ("F", 3)],
         [[("F", 2), "L", ("F", 3)], [("F", 3), "R", ("F", 2)], [("F", 2), "R", ("F", 4)]],
         "Go down 2 squares. The robot faces down the page, so turning right makes it face the left of the page. Then go 3 squares."),
    ]:
        assert run(st, d, cmds)[0] == star
        for w in wrongs:
            r = run(st, d, w)
            assert r is None or r[0] != star, w
        svg = map_svg([(st[0], st[1], "robot", d), (star[0], star[1], "star", None)], label="grid with a robot and a star")
        its.append(mcq(fig(svg) + "The robot %s. Which instructions take it to the star?" % FACE_TXT[d], say(cmds),
                       [say(w) for w in wrongs], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Moving on a grid: forwards, backwards and turns", "items": its}


# ------------------------------------------------------------ set 5: real-life problems
MAP = {(0, 0): "tree", (3, 0): "flag", (6, 0): "rock", (1, 2): "house", (4, 2): "pond", (6, 3): "tent",
       (0, 4): "rock2", (3, 4): "chest", (5, 4): "tree2"}
MAP_NAME = {"tree": "tree", "flag": "flag", "rock": "rock", "house": "house", "pond": "pond", "tent": "tent",
            "chest": "treasure chest", "tree2": "tree", "rock2": "rock"}


def treasure_svg():
    objs = [(c, r, k.rstrip("2"), None) for (c, r), k in MAP.items()]
    return map_svg(objs, cols=7, rows=5, C=34, label="treasure map grid with a tree, flag, rocks, house, pond, tent and treasure chest")


def walk(start, moves):
    x, y = start
    for d, n in moves:
        x, y = x + DV[d][0] * n, y + DV[d][1] * n
    return (x, y)


def moves_txt(moves):
    return " and ".join("%d square%s %s" % (n, "" if n == 1 else "s", DIRS[d]) for d, n in moves)


def set_problems(rnd, P_):
    its = []
    tm = fig(treasure_svg())
    where = {v: k for k, v in MAP.items()}
    for frm, moves in [("house", [(1, 2), (2, 2)]), ("flag", [(3, 2), (2, 2)]), ("tent", [(0, 1), (3, 2)])]:
        end = walk(where[frm], moves)
        ans = MAP_NAME[MAP[end]]
        cands = []
        for m in ([((d + 2) % 4 if i == 1 else d, n) for i, (d, n) in enumerate(moves)],
                  [((d + 2) % 4 if i == 0 else d, n) for i, (d, n) in enumerate(moves)],
                  [(d, n - 1 if i == 1 else n) for i, (d, n) in enumerate(moves)],
                  [(d, n + 1 if i == 1 else n) for i, (d, n) in enumerate(moves)],
                  [(d, n - 1 if i == 0 else n) for i, (d, n) in enumerate(moves)]):
            c = walk(where[frm], m)
            if c in MAP and MAP_NAME[MAP[c]] != ans:
                cands.append(MAP_NAME[MAP[c]])
        cands += [MAP_NAME[k] for k in ("pond", "flag", "rock", "tent", "house", "tree")]
        its.append(mcq(tm + "Start at the %s. Go %s. What do you find?" % (MAP_NAME[frm], moves_txt(moves)), "the " + ans,
                       ["the " + c for c in cands if c != MAP_NAME[frm]],
                       "From the %s, go %s. You reach the %s." % (MAP_NAME[frm], moves_txt(moves), ans), rnd))
    for frm, to in [("house", "chest"), ("pond", "flag")]:
        a, b = where[frm], where[to]
        dx, dy = b[0] - a[0], b[1] - a[1]
        mv = [(1 if dx > 0 else 3, abs(dx)), (2 if dy > 0 else 0, abs(dy))]
        assert walk(a, mv) == b
        flipv = [mv[0], ((mv[1][0] + 2) % 4, mv[1][1])]
        fliph = [((mv[0][0] + 2) % 4, mv[0][1]), mv[1]]
        plus = [(mv[0][0], mv[0][1] + 1), mv[1]]
        for w in (flipv, fliph, plus):
            assert walk(a, w) != b
        its.append(mcq(tm + "How do you get from the %s to the %s?" % (MAP_NAME[frm], MAP_NAME[to]), moves_txt(mv),
                       [moves_txt(flipv), moves_txt(fliph), moves_txt(plus)],
                       "From the %s, go %s to reach the %s. Do not count the square you start on." % (MAP_NAME[frm], moves_txt(mv), MAP_NAME[to]), rnd))
    # classroom robot
    pos = Pos(rnd)
    n, he, his = P_.next()
    its.append(letters_q("%s programs a toy robot. It %s. It goes <b>forwards 3, turn left, forwards 2</b>. Where does it stop?"
                         % (n, FACE_TXT[0]), (3, 4), 0, [("F", 3), "L", ("F", 2)], pos,
                         "Go up 3 squares. Turning left makes the robot face the left of the page. Then go 2 squares."))
    n, he, his = P_.next()
    its.append(letters_q("%s’s toy robot %s. It goes <b>forwards 2, turn right, forwards 1</b>. Where does it stop?"
                         % (n, FACE_TXT[3]), (4, 3), 3, [("F", 2), "R", ("F", 1)], pos,
                         "Go 2 squares to the left. The robot faces left, so turning right makes it face up the page. Then go 1 square up."))
    # playground
    pg = ["swings", "slide", "gate", "sandpit"]
    for face, k, cw, e in [
        (0, 1, True, "Clockwise is the way clock hands go. A quarter turn clockwise from the swings is the slide."),
        (1, 1, False, "Anticlockwise is the opposite way to clock hands. A quarter turn anticlockwise from the slide is the swings."),
        (3, 2, True, "A half turn makes you face the opposite way. The slide is opposite the sandpit."),
    ]:
        n, he, his = P_.next()
        end = (face + (k if cw else -k)) % 4
        t = "half turn" if k == 2 else "quarter turn " + ("clockwise" if cw else "anticlockwise")
        its.append(mcq_fixed(fig(facing_svg(pg, face, "child in the playground facing the " + pg[face])) +
                             "%s faces the %s. %s makes a %s. What does %s face now?" % (n, pg[face], he.capitalize(), t, he),
                             ["the " + x for x in pg], "the " + pg[end], e))
    # clock
    for start, k, e in [(12, 2, "From 12 to 6 is halfway round the clock: a half turn."),
                        (12, 3, "From 12 to 9 is 3 quarters of the way round: 12 to 3, 3 to 6, 6 to 9. That is a three-quarter turn.")]:
        its.append(mcq_fixed(fig(clock_turn_svg(start % 12, k)) + "The minute hand turns clockwise from the dashed line. What turn has it made?",
                             TURNS, TURNS[k - 1], e))
    # line of children
    kids = ["Ava", "Kai", "Ruby", "Noah", "Evie"]
    s = ["<circle cx='%d' cy='22' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (40 + 76 * i, FILL, GREEN) for i in range(5)]
    s += [text(40 + 76 * i, 60, k, 15) for i, k in enumerate(kids)]
    line = fig(svg_wrap(384, 68, "".join(s), "five children in a line: " + ", ".join(kids)))
    its.append(mcq(line + "Five children stand in a line. Who is <b>between</b> Kai and Noah?", "Ruby",
                   ["Ava", "Evie", "Kai"], "Find Kai and Noah. Ruby is in the middle of them.", rnd))
    its.append(mcq(line + "Who is just on the <b>right</b> of Ruby in the picture?", "Noah",
                   ["Kai", "Evie", "Ava"], "Look to the right side of the page. Next to Ruby on that side is Noah. Kai is on her left.", rnd))
    its.append(mcq(line + "Who is <b>4th from the left</b>?", "Noah",
                   ["Kai", "Ruby", "Evie"], "Count from the left: Ava 1st, Kai 2nd, Ruby 3rd, Noah 4th. Counting from the right gives Kai.", rnd))
    # patterns in real life
    n, he, his = P_.next()
    its.append(mcq("%s puts beads on a string: round, round, square, round, round, square. What is the 10th bead?" % n,
                   "round", ["square", "star", "heart"],
                   "The beads repeat in groups of 3: round, round, square. The 9th bead is square, so the 10th starts a new group: round.", rnd))
    its.append(mcq("Bunting has flags that point down, up, down, up. What does the 9th flag do?", "points down",
                   ["points up", "points left", "points right"],
                   "The odd flags (1st, 3rd, 5th, 7th, 9th) point down. The even flags point up.", rnd))
    # turns in real life
    n, he, his = P_.next()
    its.append(mcq("%s faces the board. %s turns round to face the back wall. What turn has %s made?" % (n, he.capitalize(), he),
                   "a half turn", ["a quarter turn", "a whole turn", "a three-quarter turn"],
                   "The back wall is opposite the board. Turning to face the opposite way is a half turn.", rnd))
    n, he, his = P_.next()
    its.append(mcq("%s spins round in the playground until %s faces the same way again. What turn is that?" % (n, he),
                   "a whole turn", ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "Facing the same way again means going all the way round: a whole turn (4 right angles).", rnd))
    its.append(mcq("You walk forwards and turn right. Which way have you turned?", "a quarter turn clockwise",
                   ["a quarter turn anticlockwise", "a half turn clockwise", "a whole turn"],
                   "Turning right is a quarter turn the same way as clock hands: clockwise. Turning left is anticlockwise.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Real-life problems: maps, robots and the playground", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    g = [["star", "moon", "sun"], ["tree", "house", "flower"], ["fish", "ball", "heart"]]
    grid = grid3_svg(g)
    robo = map_svg([(1, 4, "robot", 0), (1, 2, "letter", "A"), (3, 2, "star", None)], label="robot facing up, square A and a star")
    turns = turns_strip_svg([(0.25, True, "quarter"), (0.5, True, "half"), (0.75, True, "three-quarter"), (0.25, False, "anticlockwise")],
                            "quarter, half and three-quarter turns clockwise and a quarter turn anticlockwise")
    pat = pattern_svg(["circle", "square", "square", "circle", "square", "square", None])
    arr = pattern_svg(["up", "right", "down", "left", None])
    return (
        "<h2>Where is it?</h2>"
        "<p>We use <b>position words</b> to say where things are: <b>above</b>, <b>below</b>, "
        "<b>on the left of</b>, <b>on the right of</b>, <b>between</b> and <b>next to</b>.</p>"
        "<figure class='sn-fig'>" + grid +
        "<figcaption>The house is in the middle. The moon is above it. The ball is below it. "
        "The tree is on its left. The flower is on its right.</figcaption></figure>" +
        ex("Example", "What is between the star and the sun?", "The star and the sun are in the top row. The moon is in the middle.", "the moon") +
        "<h2>Moving on a grid</h2>"
        "<p>A robot moves <b>forwards</b> or <b>backwards</b> in a straight line. "
        "Count the squares it moves. Do not count the square it starts on. "
        "The arrow on the robot shows which way it faces.</p>"
        "<figure class='sn-fig'>" + robo +
        "<figcaption>Forwards 2 takes the robot to A. Then turn right and go forwards 2 to reach the star.</figcaption></figure>"
        "<h2>Turns</h2>"
        "<p><b>Clockwise</b> is the way the hands on a clock turn. <b>Anticlockwise</b> is the other way. "
        "A <b>quarter turn</b> is a <b>right angle</b>, like the corner of a page.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>The first three turns are clockwise. The last one is a quarter turn anticlockwise.</figcaption></figure>" +
        table(["Turn", "Right angles", "You end up facing"], [
            ["Quarter turn", "1", "to the side"], ["Half turn", "2", "the opposite way"],
            ["Three-quarter turn", "3", "the other side"], ["Whole turn", "4", "the same way again"],
        ]) +
        ex("Example", "An arrow points up. It makes a quarter turn clockwise. Which way does it point?",
           "Clockwise goes up, right, down, left. One quarter turn from up is right.", "right") +
        "<h2>Patterns</h2>"
        "<p>Find the part that <b>repeats</b>. Say the pattern out loud, then keep going.</p>"
        "<figure class='sn-fig'>" + pat + "<figcaption>Circle, square, square repeats. Next is a circle.</figcaption></figure>"
        "<figure class='sn-fig'>" + arr + "<figcaption>Each arrow makes a quarter turn clockwise. Next is up.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up left and right when the robot faces down the page", "Turn the page round so you face the same way as the robot"],
            ["Mixing up clockwise and anticlockwise", "Clockwise is the way clock hands go"],
            ["Thinking a half turn is a quarter turn", "A half turn makes you face the opposite way"],
            ["Counting the start square as a move", "Count the moves, not the squares you stand on"],
            ["Starting the pattern again from the wrong shape", "Find the part that repeats and say it out loud"],
        ])
    )


FAQ = [
    {"q": "What do Year 2 children learn about position and direction?",
     "a": "They use words like above, below, left, right and between, move in straight lines on a grid, and make quarter, half and three-quarter turns clockwise and anticlockwise. They also continue patterns of shapes."},
    {"q": "What is the difference between clockwise and anticlockwise?",
     "a": "Clockwise is the way the hands on a clock turn. Anticlockwise is the opposite way."},
    {"q": "How many right angles are in a half turn?",
     "a": "A half turn is 2 right angles. A quarter turn is 1 right angle, a three-quarter turn is 3 and a whole turn is 4."},
    {"q": "How can I help my child learn position and direction at home?",
     "a": "Play games that give directions, such as “take 3 steps forwards, then make a quarter turn clockwise”, or hide a toy and describe where it is. A toy robot or a simple treasure map on squared paper works well."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order stay as they are."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [5 - c for c in cnt]
        assert min(need) >= 0 and sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen():
    rnd = random.Random(2212)
    P_ = People(rnd)
    sets = [set_position(rnd, P_), set_turns(rnd, P_), set_patterns(rnd, P_), set_grid(rnd, P_), set_problems(rnd, P_)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "position-and-direction", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Position and Direction: Left and Right, Turns and Patterns",
        "seo_title": "Year 2 Position and Direction Worksheets: Left, Right, Clockwise and Anticlockwise Turns",
        "short_title": "Position and direction",
        "domain": "Geometry – position and direction",
        "standard_code": "Year 2: Geometry – position and direction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Order and arrange combinations of mathematical objects in patterns and sequences; use mathematical vocabulary to describe position, direction and movement, including movement in a straight line and distinguishing between rotation as a turn and in terms of right angles for quarter, half and three-quarter turns (clockwise and anti-clockwise).",
        "meta_desc": "Free Year 2 maths worksheets on position and direction: above, below, left, right and between, moving a robot on a grid, quarter, half and three-quarter turns clockwise and anticlockwise, and shape patterns. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Clockwise is the way clock hands turn. A quarter turn is 1 right angle, a half turn is 2 and a three-quarter turn is 3.",
        "key_sub": "When you move on a grid, count the moves, not the square you start on. When a robot faces down the page, its left is on the right of the page.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (grids, rows of pictures, patterns) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(grid|row of pictures|pattern|treasure map|five children)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
