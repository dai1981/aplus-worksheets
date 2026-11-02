# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Transformations and tessellations
(Australian Curriculum v9.0, AC9M6SP03)
  python3 tools/gen_au_maths_y6_tessellations.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

Grid helpers are copied from gen_au_maths_y5_transformations.py. The shapes that are moved on grids
(a right-angled triangle 3 by 2, an L-shape and a right-angled trapezium) have no symmetry, so every
picture has exactly one correct move; classify() works it out from the coordinates. Two-step answers
and "which two steps" choices are checked by doing each step in code. Tessellation pictures are built
from exact regular polygons (reg_from_vertex) and the number of shapes at a marked corner is counted.
Wrong answers come from real Year 6 mistakes: calling a half turn a reflection, thinking all regular
shapes tessellate, doing only one step of a combination or the steps in the wrong order, measuring
straight from the first shape to the last, adding instead of multiplying when counting tiles.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MIRROR = "#8e44ad"
SHADE = "#4fae74"
SHADE_B = "#6d9fd8"
THIN = "#a8a8a8"
FONT = "Arial, Helvetica, sans-serif"
HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
LETTERS = ["A", "B", "C", "D"]
MOVES = ["a translation", "a reflection", "a rotation", "it changed size"]
ROT = ["a quarter turn clockwise", "a quarter turn anticlockwise", "a half turn", "a reflection"]


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
    """Choices keep their order (A B C D, numbers from small to large, fixed lists)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e, fmt="%d"):
    ch = []
    for c in cands:
        if c >= 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [fmt % c for c in ch], fmt % correct, e)


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


def pair(x, y):
    return "(%d, %d)" % (x, y)


def plist(pts):
    return ", ".join(pair(*p) for p in pts)


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def sgn(v):
    return (v > 0) - (v < 0)


def inside(p):
    return 0 <= p[0] <= 10 and 0 <= p[1] <= 10


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
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ coordinate grid
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


def seg_hits(p, q, box, m=1.5):
    """Does the straight line p-q (px) pass through the box (px)?"""
    n = 80
    for i in range(n + 1):
        t = i / float(n)
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if box[0] - m <= x <= box[2] + m and box[1] - m <= y <= box[3] + m:
            return True
    return False


class Grid:
    """First-quadrant grid from 0 to nx across and 0 to ny up. One square = u px."""

    def __init__(self, nx, ny, u=22):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u = nx, ny, u
        self.ox = tw(ny, 14) + 15
        self.oy = 30 + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26))
        self.pts, self.segs, self.arrows, self.notes, self.polys, self.mirrors = [], [], [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def ok(self, p):
        return 0 <= p[0] <= self.nx and 0 <= p[1] <= self.ny

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and self.ok((x, y)), (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def poly(self, pts, col=GREEN, name=None, at=None):
        for p in pts:
            assert self.ok(p), p
        self.polys.append((pts, col))
        for i in range(len(pts)):
            self.segs.append((pts[i], pts[(i + 1) % len(pts)], col, 2.5))
        if name:
            if at is None:
                at = (sum(p[0] for p in pts) / float(len(pts)), sum(p[1] for p in pts) / float(len(pts)))
            self.note(at[0], at[1], name, col=col, fs=16)
        return self

    def mirror(self, kind, m):
        """kind 'v': the line x = m; kind 'h': the line y = m."""
        if kind == "v":
            assert 2 <= m <= self.nx, m
        else:
            assert 1 <= m <= self.ny, m
            self.W = max(self.W, int(math.ceil(self.ox + self.nx * self.u + 10 + tw("y = %d" % m, 14, True) + 4)))
        self.mirrors.append((kind, m))
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _edges(self):
        return [(self.P(*a), self.P(*b)) for a, b, col, w in self.segs] + \
               [(self.P(*a), self.P(*b)) for a, b, col in self.arrows] + \
               [self._mline(k, m) for k, m in self.mirrors]

    def _mline(self, kind, m):
        u, ox, oy = self.u, self.ox, self.oy
        if kind == "v":
            return ((ox + m * u, oy), (ox + m * u, oy - self.ny * u - 6))
        return ((ox, oy - m * u), (ox + self.nx * u + 6, oy - m * u))

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not self.ok((cx, cy)):
                continue
            corners = {(x + dx, y), (x, y + dy), (x + dx, y + dy)}
            if corners & others:                     # the square touches another point: the label could be misread
                continue
            cell = (min(x, cx), min(y, cy))
            if cell in used:
                continue
            c = self.P(x + dx / 2.0, y + dy / 2.0)
            box = (c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7)
            if any(overlap(box, b) for b in boxes):
                continue
            if any(seg_hits(p, q, box) for p, q in self._edges()):
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
        for pts, col in self.polys:
            s.append("<polygon points='%s' fill='%s' fill-opacity='0.16' stroke='none'/>"
                     % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), col))
        xe, ye = ox + nx * u + 12, oy - ny * u - 12
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, xe - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox, ye + 4, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (xe, oy, xe - 9, oy - 4.5, xe - 9, oy + 4.5, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (ox, ye, ox - 4.5, ye + 9, ox + 4.5, ye + 9, INK))
        s.append(text(xe + 4, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox, ye - 6, "y", 15, bold=True, extra=" font-style='italic'"))
        for k in range(1, nx + 1):
            s.append(text(ox + k * u, oy + 18, k, 14))
        for k in range(1, ny + 1):
            s.append(text(ox - 9, oy - k * u + 5, k, 14, anchor="end"))
        s.append(text(ox - 9, oy + 18, 0, 14, anchor="end"))
        boxes = []
        # mirror lines: dashed, with their name outside the grid
        for kind, m in self.mirrors:
            p, q = self._mline(kind, m)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                     % (p[0], p[1], q[0], q[1], MIRROR))
            if kind == "v":
                t = "x = %d" % m
                w = tw(t, 14, True)
                cx, base = ox + m * u, oy - ny * u - 10
                box = (cx - w / 2, base - 11, cx + w / 2, base + 1)
                assert box[0] > ox + 6, ("mirror name on the y label", m)
                assert box[2] <= self.W and box[1] >= 0
                s.append(text(cx, base, t, 14, bold=True, col=MIRROR))
            else:
                t = "y = %d" % m
                w = tw(t, 14, True)
                x0, base = ox + nx * u + 10, oy - m * u + 5
                box = (x0, base - 11, x0 + w, base + 1)
                assert box[2] <= self.W
                s.append(text(x0, base, t, 14, anchor="start", bold=True, col=MIRROR))
            boxes.append(box)
        for a, b, col, w in self.segs:
            p, q = self.P(*a), self.P(*b)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                     % (p[0], p[1], q[0], q[1], col, w))
        for a, b, col in self.arrows:
            p, q = self.P(*a), self.P(*b)
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            d = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
            e = (q[0] - d[0] * 10, q[1] - d[1] * 10)
            n = (-d[1], d[0])
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (p[0], p[1], e[0] + d[0] * 2, e[1] + d[1] * 2, col))
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (q[0], q[1], e[0] + n[0] * 5.5, e[1] + n[1] * 5.5, e[0] - n[0] * 5.5, e[1] - n[1] * 5.5, col))
        edges = self._edges()
        for gx, gy, t, anchor, col, fs in self.notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0 = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0, c[1] - fs * 0.4, x0 + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("notes overlap", t)
            for p, q in edges:
                assert not seg_hits(p, q, box, 0.5), ("note on a line", t)
            boxes.append(box)
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col, extra=HALO))
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
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=RED if col == RED else INK, extra=HALO))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def grid_for(pts, extra=1, lo=6, mirror=None):
    """Grid just big enough for the points and the mirror line (smaller grids print larger)."""
    xs = [p[0] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "v" else [])
    ys = [p[1] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "h" else [])
    G = Grid(min(10, max(lo, max(xs) + extra)), min(10, max(lo, max(ys) + extra)))
    if mirror:
        G.mirror(*mirror)
    return G


def pick_letters(target, others, pos):
    """The 4 points with letters A-D (target at the next position) and the answer letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    assert len(set(cells)) == 4 and all(inside(c) for c in cells), cells
    return [(c[0], c[1], LETTERS[k]) for k, c in enumerate(cells)], LETTERS[p]


# ------------------------------------------------------------ translations
def mv(dx, dy):
    parts = []
    if dx:
        parts.append("%d %s" % (abs(dx), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%d %s" % (abs(dy), "up" if dy > 0 else "down"))
    return ", ".join(parts)


def mv_long(dx, dy):
    parts = []
    if dx:
        parts.append("%s %s" % (sq(abs(dx)), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%s %s" % (sq(abs(dy)), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def move_cands(p, dx, dy, i=0):
    """Where students land by mistake: wrong way, x/y moves mixed up, only one number changed."""
    x, y = p
    c = [(x - dx, y + dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (x + dx, y - dy), (x - dx, y - dy)]
    c = c[i % 3:] + c[:i % 3]
    # backups: counted the lines (1 too far), the answer written the wrong way round
    c += [(x + dx + sgn(dx), y + dy + sgn(dy)), (y + dy, x + dx)]
    return [q for q in c if inside(q) and q != (x + dx, y + dy) and q != (x, y)]


def describe_cands(dx, dy, i=0):
    """Wrong descriptions: numbers swapped, wrong direction, counted the lines (1 too many)."""
    out = []
    if dx and dy:
        out.append("%d %s, %d %s" % (abs(dy), "right" if dx > 0 else "left", abs(dx), "up" if dy > 0 else "down"))
    out += [mv(-dx, dy), mv(dx + sgn(dx), dy + sgn(dy)), mv(dx, -dy), mv(-dx, -dy)]
    if not dx:
        out += [mv(dy, 0), mv(-dy, 0)]
    if not dy:
        out += [mv(0, dx), mv(0, -dx)]
    first, rest = out[:1], out[1:]
    rest = rest[i % 3:] + rest[:i % 3]
    return [c for c in first + rest if c and c != mv(dx, dy)]


def describe_e(a, b, na="A", nb="B"):
    dx, dy = b[0] - a[0], b[1] - a[1]
    s = "%s is at %s and %s is at %s. " % (na, pair(*a), nb, pair(*b))
    if dx:
        s += "Across: %d to %d is %s %s. " % (a[0], b[0], sq(abs(dx)), "right" if dx > 0 else "left")
    else:
        s += "The x-coordinate stays %d, so there is no move left or right. " % a[0]
    if dy:
        s += "Up and down: %d to %d is %s %s. " % (a[1], b[1], sq(abs(dy)), "up" if dy > 0 else "down")
    else:
        s += "The y-coordinate stays %d, so there is no move up or down. " % a[1]
    return s + "Count the squares you jump, not the lines you touch."


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %s changes x: %d %s %d = %d" % (
            "Right" if dx > 0 else "Left", sq(abs(dx)), x, "+" if dx > 0 else "−", abs(dx), q[0]))
    else:
        parts.append("x stays %d" % x)
    if dy:
        parts.append("%s %s changes y: %d %s %d = %d" % (
            "Up" if dy > 0 else "Down", sq(abs(dy)), y, "+" if dy > 0 else "−", abs(dy), q[1]))
    else:
        parts.append("y stays %d" % y)
    return ". ".join(parts) + ". The new point is %s." % pair(*q)


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# ------------------------------------------------------------ reflections
def reflect(p, line):
    k, m = line
    return (2 * m - p[0], p[1]) if k == "v" else (p[0], 2 * m - p[1])


def lname(line):
    return ("x = %d" if line[0] == "v" else "y = %d") % line[1]


def lword(line):
    return ("the vertical mirror line x = %d" if line[0] == "v" else "the horizontal mirror line y = %d") % line[1]


def refl_e(p, line, name="The point"):
    k, m = line
    r = reflect(p, line)
    if r == p:
        return "%s %s is on the mirror line %s, so it does not move: %s." % (name, pair(*p), lname(line), pair(*r))
    if k == "v":
        d = p[0] - m
        side, other = ("left", "right") if d < 0 else ("right", "left")
        return ("%s %s is %s to the %s of the line %s. The image is %s to the %s of it: %d %s %d = %d. "
                "y stays %d. The image is %s." % (name, pair(*p), sq(abs(d)), side, lname(line), sq(abs(d)), other,
                                                  m, "+" if d < 0 else "−", abs(d), r[0], p[1], pair(*r)))
    d = p[1] - m
    side, other = ("below", "above") if d < 0 else ("above", "below")
    return ("%s %s is %s %s the line %s. The image is %s %s it: %d %s %d = %d. "
            "x stays %d. The image is %s." % (name, pair(*p), sq(abs(d)), side, lname(line), sq(abs(d)), other,
                                              m, "+" if d < 0 else "−", abs(d), r[1], p[0], pair(*r)))


def refl_kinds(p, line):
    """Mistakes for reflecting a point: (point, why)."""
    k, m = line
    r = reflect(p, line)
    if k == "v":
        s = sgn(r[0] - m)
        far, short, stop = (r[0] + s, r[1]), (r[0] - s, r[1]), (m, p[1])
        wrong = (p[0], 2 * m - p[1])
        why_w = "it was flipped up or down, not across the line"
    else:
        s = sgn(r[1] - m)
        far, short, stop = (r[0], r[1] + s), (r[0], r[1] - s), (p[0], m)
        wrong = (2 * m - p[0], p[1])
        why_w = "it was flipped across, not up or down over the line"
    out = [(far, "it is 1 square too far (the lines were counted, starting with 1 on the line P is on)", "far"),
           (stop, "it stops on the mirror line", "stop"),
           (short, "it is 1 square too close to the mirror line", "short"),
           (wrong, why_w, "wrong"),
           ((r[1], r[0]), "x and y are swapped", "swap")]
    return [(q, w, k) for q, w, k in out if inside(q) and q != r and q != p]


# ------------------------------------------------------------ squared-paper panels (A-D)
def cells_of(rows):
    return frozenset((c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "#")


def mir(cell, line):
    c, r = cell
    return (2 * line[1] - 1 - c, r) if line[0] == "v" else (c, 2 * line[1] - 1 - r)


def bbox(cells):
    return (min(c for c, r in cells), min(r for c, r in cells), max(c for c, r in cells), max(r for c, r in cells))

def panel_el(cols, rows, shape, image, line, cs, ox, oy):
    el = []
    for (c, r) in sorted(shape):
        el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s'/>" % (ox + c * cs, oy + r * cs, cs, cs, SHADE))
    for (c, r) in sorted(image):
        el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s'/>" % (ox + c * cs, oy + r * cs, cs, cs, SHADE_B))
    for c in range(1, cols):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox + c * cs, oy, ox + c * cs, oy + rows * cs, THIN))
    for r in range(1, rows):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox, oy + r * cs, ox + cols * cs, oy + r * cs, THIN))
    el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
              % (ox, oy, cols * cs, rows * cs, INK))
    o = 6
    if line is None:
        return el
    if line[0] == "o":
        px, py = line[1]
        el.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s' stroke='#ffffff' stroke-width='1.5'/>" % (ox + px * cs, oy + py * cs, RED))
        return el
    if line[0] == "v":
        x = ox + line[1] * cs
        seg = (x, oy - o, x, oy + rows * cs + o)
    else:
        y = oy + line[1] * cs
        seg = (ox - o, y, ox + cols * cs + o, y)
    el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
              % (seg + (MIRROR,)))
    return el


def panel_svg(cols, rows, shape, images, line, cs, label):
    LW, gap, pad, o = 22, 16, 8, 7
    gw, gh = cols * cs, rows * cs
    W = 2 * pad + 2 * (LW + gw + 2 * o) + gap
    H = 2 * pad + 2 * (gh + 2 * o) + gap
    el = []
    for k, img in enumerate(images):
        cx, cy = k % 2, k // 2
        x0 = pad + cx * (LW + gw + 2 * o + gap)
        y0 = pad + cy * (gh + 2 * o + gap)
        el += panel_el(cols, rows, shape, img, line, cs, x0 + LW + o, y0 + o)
        el.append(text(x0, y0 + o + 16, "ABCD"[k], 18, anchor="start", bold=True))
    if W == H:
        W += 1
    return svg_wrap(W, H, "".join(el), label)

# ------------------------------------------------------------ rotations (quarter and half turns)
TURN = {"cw": "a quarter turn clockwise", "acw": "a quarter turn anticlockwise", "half": "a half turn"}


def rot(p, o, kind):
    """Grid coordinates (y up). Clockwise: right -> down, up -> right."""
    dx, dy = p[0] - o[0], p[1] - o[1]
    if kind == "cw":
        return (o[0] + dy, o[1] - dx)
    if kind == "acw":
        return (o[0] - dy, o[1] + dx)
    return (o[0] - dx, o[1] - dy)


def rots(pts, o, kind):
    return [rot(p, o, kind) for p in pts]


WAYS = {"cw": "right turns into down, down into left, left into up and up into right",
        "acw": "right turns into up, up into left, left into down and down into right",
        "half": "right turns into left and up turns into down"}


def rot_e(p, o, kind, name="P"):
    r = rot(p, o, kind)
    a, b = (p[0] - o[0], p[1] - o[1]), (r[0] - o[0], r[1] - o[1])
    return ("From O %s, %s %s is %s. In %s, %s. So the image is %s from O: %s."
            % (pair(*o), name, pair(*p), mv(*a), TURN[kind], WAYS[kind], mv(*b), pair(*r)))


def rot_cells(shape, piv, kind):
    """Squared-paper panels (screen rows go down). Clockwise on screen: (dx, dy) -> (-dy, dx)."""
    px, py = piv
    out = set()
    for c, r in shape:
        dx, dy = c + 0.5 - px, r + 0.5 - py
        n = {"cw": (-dy, dx), "acw": (dy, -dx), "half": (-dx, -dy), "flipv": (-dx, dy), "fliph": (dx, -dy)}[kind]
        out.add((int(round(px + n[0] - 0.5)), int(round(py + n[1] - 0.5))))
    return frozenset(out)


# ------------------------------------------------------------ symmetry of shapes (worked out from the drawing)
def regular(n, r=3.0, start=90):
    return [(r * math.cos(math.radians(start + 360.0 * k / n)), r * math.sin(math.radians(start + 360.0 * k / n))) for k in range(n)]


SHAPES = {
    "square": [[(0, 0), (4, 0), (4, 4), (0, 4)]],
    "rectangle": [[(0, 0), (6, 0), (6, 3), (0, 3)]],
    "equilateral triangle": [regular(3)],
    "isosceles triangle": [[(0, 0), (4, 0), (2, 5)]],
    "parallelogram": [[(0, 0), (5, 0), (7, 3), (2, 3)]],
    "regular hexagon": [regular(6, start=0)],
    "regular octagon": [regular(8, start=22.5)],
    "kite": [[(0, 4), (2, 2), (0, -3), (-2, 2)]],
    "rhombus": [[(0, 3), (2, 0), (0, -3), (-2, 0)]],
    "pinwheel": [[(0, 0), (3, 0), (3, 2)], [(0, 0), (0, 3), (-2, 3)], [(0, 0), (-3, 0), (-3, -2)], [(0, 0), (0, -3), (2, -3)]],
}


def _edges(parts):
    out = []
    for pts in parts:
        for i in range(len(pts)):
            out.append((pts[i], pts[(i + 1) % len(pts)]))
    return out


def _same(E1, E2):
    def close(a, b):
        return abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6
    for a, b in E1:
        if not any((close(a, c) and close(b, d)) or (close(a, d) and close(b, c)) for c, d in E2):
            return False
    return True


def sym_counts(parts):
    """(lines of symmetry, order of rotational symmetry) of the drawn shape."""
    pts = [p for part in parts for p in part]
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    E = _edges(parts)
    lines = 0
    for k in range(360):                      # line through the centre at k/2 degrees
        t = math.radians(k / 2.0)
        c2, s2 = math.cos(2 * t), math.sin(2 * t)
        f = lambda p: (cx + (p[0] - cx) * c2 + (p[1] - cy) * s2, cy + (p[0] - cx) * s2 - (p[1] - cy) * c2)
        if _same([(f(a), f(b)) for a, b in E], E):
            lines += 1
    order = 0
    for k in range(1, 721):                   # turns of k/2 degrees up to a full turn
        t = math.radians(k / 2.0)
        c, s = math.cos(t), math.sin(t)
        f = lambda p: (cx + (p[0] - cx) * c - (p[1] - cy) * s, cy + (p[0] - cx) * s + (p[1] - cy) * c)
        if _same([(f(a), f(b)) for a, b in E], E):
            order += 1
    return lines, order

def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

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
        assert sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)

def mark_large(u, pattern):
    """Tag pictures that must print larger (every grid) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ Year 6: transformations as functions
def T_shift(dx, dy):
    return lambda pts: [(x + dx, y + dy) for x, y in pts]


def T_refl(line):
    return lambda pts: [reflect(p, line) for p in pts]


def T_rot(o, kind):
    return lambda pts: rots(pts, o, kind)


def T_scale(k, o):
    return lambda pts: [(o[0] + (x - o[0]) * k, o[1] + (y - o[1]) * k) for x, y in pts]


def chain(*fs):
    def g(pts):
        for f in fs:
            pts = f(pts)
        return pts
    return g


def area2(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def sides(pts):
    return [round(math.hypot(pts[(i + 1) % len(pts)][0] - pts[i][0], pts[(i + 1) % len(pts)][1] - pts[i][1]), 6) for i in range(len(pts))]


def classify(A, B):
    """What a student should answer for A -> B (A has no symmetry, so the move is unique)."""
    if sides(A) != sides(B):
        return "it changed size"
    d = (B[0][0] - A[0][0], B[0][1] - A[0][1])
    if all((b[0] - a[0], b[1] - a[1]) == d for a, b in zip(A, B)):
        return "a translation"
    return "a reflection" if sgn(area2(A)) != sgn(area2(B)) else "a rotation"


def same_shape(A, B):
    return frozenset((round(x, 6), round(y, 6)) for x, y in A) == frozenset((round(x, 6), round(y, 6)) for x, y in B)


TRI = ((0, 0), (3, 0), (0, 2))                                  # right-angled triangle with sides 3 and 2: no symmetry
ELL = ((0, 0), (3, 0), (3, 1), (1, 1), (1, 2), (0, 2))          # L-shape with arms 3 and 2: no symmetry
TRAP = ((0, 0), (3, 0), (3, 2), (1, 2))                         # right-angled trapezium: no symmetry
AT = {TRI: (1.0, 2 / 3.0), ELL: (0.5, 0.5), TRAP: (1.75, 1.0)}
for _s in (TRI, ELL, TRAP):
    assert sym_counts([list(_s)]) == (0, 1), _s


def place(shape, base):
    return shift(list(shape), *base), shift([AT[shape]], *base)[0]


def pair_grid(shape, base, f, mirror=None, O=None, ny=8, names=("A", "B")):
    A, at = place(shape, base)
    B, bt = f(A), f([at])[0]
    G = Grid(10, ny)
    if mirror:
        G.mirror(*mirror)
    G.poly(A, GREEN, names[0], at).poly(B, BLUE, names[1], bt)
    if O:
        G.point(O[0], O[1], "O", RED)
    return G, A, B


# ------------------------------------------------------------ plain squared-paper panels (A-D)
PWHY = {"slide": "slid (a translation): it faces the same way",
        "flipv": "reflected in a vertical line: it faces the other way, left to right",
        "fliph": "reflected in a horizontal line: it is flipped upside down only",
        "cw": "turned a quarter turn clockwise",
        "acw": "turned a quarter turn anticlockwise",
        "half": "turned a half turn: upside down and back to front"}


def panel_pick(half, kind, wrongs, slide, question, pos, rnd):
    shape = cells_of(half)

    def img(k):
        if k == "slide":
            return frozenset((c + slide[0], r + slide[1]) for c, r in shape)
        return rot_cells(shape, (3, 3), k)
    V = {k: img(k) for k in [kind] + wrongs}
    for k, s in V.items():
        assert all(0 <= c < 6 and 0 <= r < 6 for c, r in s), k
        assert not (s & shape), k
    assert len(set(V.values())) == 4
    p = pos.next()
    w = wrongs[:]
    rnd.shuffle(w)
    keys = w[:p] + [kind] + w[p:]
    svg = panel_svg(6, 6, shape, [V[k] for k in keys], None, 14, "four grid pictures A to D")
    others = "; ".join("%s is %s" % ("ABCD"[j], PWHY[k]) for j, k in enumerate(keys) if k != kind)
    e = "In <b>%s</b> the blue shape is %s. The others: %s." % ("ABCD"[p], PWHY[kind], others)
    return mcq_fixed(fig(svg) + question, LETTERS, "ABCD"[p], e)


# ------------------------------------------------------------ drawing in screen coordinates
def poly_el(pts, fill=SHADE, stroke=GREEN, op=0.35, sw=2):
    return ("<polygon points='%s' fill='%s' fill-opacity='%.2f' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % p for p in pts), fill, op, stroke, sw))


def dot_el(p, r=4.5):
    return "<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='#ffffff' stroke-width='1.5'/>" % (p[0], p[1], r, RED)


def reg_from_vertex(n, s, start):
    """Regular n-gon (maths coordinates, y up) with a corner at (0, 0). Its angle there runs from `start` anticlockwise."""
    pts, x, y, a = [(0.0, 0.0)], 0.0, 0.0, start
    for k in range(n - 1):
        x += s * math.cos(math.radians(a))
        y += s * math.sin(math.radians(a))
        pts.append((x, y))
        a += 360.0 / n
    return pts


def interior(n):
    return 180 * (n - 2) // n


def around(ns, s=1.0, start=0.0):
    out, a = [], start
    for n in ns:
        out.append(reg_from_vertex(n, s, a))
        a += interior(n)
    assert a - start <= 360 + 1e-9, ns
    return out, a


def fit(polys, x0, y0, w, h, extra=()):
    """Scale maths-coordinate shapes (y up) into a screen box. Returns the shapes and a function for single points."""
    pts = [p for P in polys for p in P] + list(extra)
    mnx, mxx = min(p[0] for p in pts), max(p[0] for p in pts)
    mny, mxy = min(p[1] for p in pts), max(p[1] for p in pts)
    k = min(w / (mxx - mnx), h / (mxy - mny))
    ox = x0 + (w - (mxx - mnx) * k) / 2.0
    oy = y0 + (h - (mxy - mny) * k) / 2.0
    f = lambda p: (ox + (p[0] - mnx) * k, oy + (mxy - p[1]) * k)
    return [[f(p) for p in P] for P in polys], f


def vertex_svg(ns, gap_label=None, label="shapes around a point"):
    """Regular shapes meeting at one point; the gap (if any) is marked with a question mark."""
    polys, end = around(ns, 1.0, 90 - sum(interior(n) for n in ns) / 2.0 + 180)
    gap = 360 - sum(interior(n) for n in ns)
    extra = [(0, 0)]
    q = None
    if gap_label:
        mid = math.radians(end + gap / 2.0)
        q = (0.75 * math.cos(mid), 0.75 * math.sin(mid))
        extra.append(q)
    W, H, pad = 170, 130, 10
    S, f = fit(polys, pad, pad, W - 2 * pad, H - 2 * pad, extra)
    el = [poly_el(P, SHADE if i % 2 == 0 else SHADE_B, GREEN if i % 2 == 0 else BLUE) for i, P in enumerate(S)]
    el.append(dot_el(f((0, 0))))
    if q:
        c = f(q)
        el.append(text(c[0], c[1] + 7, gap_label, 20, bold=True, col=RED))
    return svg_wrap(W, H, "".join(el), label)


def angle_svg(n, label):
    """One regular shape with the angle at its bottom-left corner marked."""
    P = reg_from_vertex(n, 1.0, 0)
    W, H, pad = 150, 120, 8
    S, f = fit([P], pad, pad, W - 2 * pad, H - 2 * pad)
    s = math.hypot(S[0][1][0] - S[0][0][0], S[0][1][1] - S[0][0][1])
    I = math.radians(interior(n))
    o = S[0][0]
    rr = (0.15 if n <= 4 else 0.2) * s
    a1 = (o[0] + rr, o[1])
    a2 = (o[0] + rr * math.cos(I), o[1] - rr * math.sin(I))
    d = {3: 0.5, 4: 0.42}.get(n, 0.6) * s
    c = (o[0] + d * math.cos(I / 2), o[1] - d * math.sin(I / 2))
    el = [poly_el(S[0]),
          "<path d='M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (a1[0], a1[1], rr, rr, a2[0], a2[1], RED),
          text(c[0], c[1] + 5, label, 15, bold=True, col=RED)]
    return svg_wrap(W, H, "".join(el), "a " + NAME[n])


NAME = {3: "equilateral triangle", 4: "square", 5: "regular pentagon", 6: "regular hexagon", 8: "regular octagon", 0: "circle"}


def shape_box(n, x0, y0, w, h):
    if n == 0:
        r = min(w, h) / 2.0
        return ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2'/>"
                % (x0 + w / 2.0, y0 + h / 2.0, r, SHADE, GREEN)]
    S, f = fit([reg_from_vertex(n, 1.0, 0)], x0, y0, w, h)
    return [poly_el(S[0])]


def four_boxes(drawers, label, cw=100, ch=76):
    LW, gap, pad = 24, 14, 6
    el = []
    for k, d in enumerate(drawers):
        x0 = pad + (k % 2) * (LW + cw + gap)
        y0 = pad + (k // 2) * (ch + gap)
        el.append(text(x0, y0 + 18, "ABCD"[k], 18, anchor="start", bold=True))
        el += d(x0 + LW, y0, cw, ch)
    W = 2 * pad + 2 * (LW + cw) + gap
    H = 2 * pad + 2 * ch + gap
    return svg_wrap(W, H, "".join(el), label)


# ------------------------------------------------------------ tessellation patches (screen coordinates)
def inbox(polys, x0, y0, w, h):
    e = 0.01
    return [P for P in polys if all(x0 - e <= x <= x0 + w + e and y0 - e <= y <= y0 + h + e for x, y in P)]


def squares_patch(x0, y0, w, h, s):
    out = []
    for i in range(int(w // s)):
        for j in range(int(h // s)):
            out.append([(x0 + i * s, y0 + j * s), (x0 + (i + 1) * s, y0 + j * s), (x0 + (i + 1) * s, y0 + (j + 1) * s), (x0 + i * s, y0 + (j + 1) * s)])
    return out


def tri_patch(x0, y0, w, h, s):
    hh = s * math.sqrt(3) / 2
    rows = int(h // hh)
    oy = y0 + (h - rows * hh) / 2.0
    P = lambda i, j: (x0 + i * s + (j % 2) * s / 2.0, oy + rows * hh - j * hh)
    out = []
    for j in range(rows):
        for i in range(-1, int(w // s) + 2):
            a, b = P(i, j), P(i + 1, j)
            c = (a[0] + s / 2.0 if j % 2 == 0 else a[0] + s / 2.0, a[1] - hh)
            out.append([a, b, c])
            out.append([b, c, (c[0] + s, c[1])])
    return inbox(out, x0, y0, w, h)


def hex_patch(x0, y0, w, h, r):
    out = []
    for i in range(-1, int(w / (1.5 * r)) + 2):
        for j in range(-1, int(h / (math.sqrt(3) * r)) + 2):
            cx = x0 + r + 1.5 * r * i
            cy = y0 + math.sqrt(3) * r * (j + 0.5 * (i % 2)) + math.sqrt(3) * r / 2
            out.append([(cx + r * math.cos(math.radians(60 * k)), cy + r * math.sin(math.radians(60 * k))) for k in range(6)])
    return inbox(out, x0, y0, w, h)


def octsq_patch(x0, y0, w, h, a, squares=True):
    D = a * (1 + math.sqrt(2))
    R = a / (2 * math.sin(math.radians(22.5)))
    octs, sqs = [], []
    for i in range(-1, int(w / D) + 2):
        for j in range(-1, int(h / D) + 2):
            cx, cy = x0 + D / 2 + D * i, y0 + D / 2 + D * j
            octs.append([(cx + R * math.cos(math.radians(22.5 + 45 * k)), cy + R * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)])
            sx, sy, d = cx + D / 2, cy + D / 2, a / math.sqrt(2)
            sqs.append([(sx + d, sy), (sx, sy + d), (sx - d, sy), (sx, sy - d)])
    return inbox(octs, x0, y0, w, h), (inbox(sqs, x0, y0, w, h) if squares else [])


def brick_el(x0, y0, w, h, s):
    """Bricks 2s long and s high; every row is moved half a brick along. Bricks are cut at the edge of the box."""
    el = []
    rows = int(h // s)
    for j in range(rows):
        off = s if j % 2 else 0
        x = x0 - off
        while x < x0 + w - 0.01:
            a, b = max(x, x0), min(x + 2 * s, x0 + w)
            el.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' fill-opacity='%.2f' stroke='%s' stroke-width='2'/>"
                      % (a, y0 + j * s, b - a, s, "#c0563f", 0.55 if j % 2 else 0.4, INK))
            x += 2 * s
    return el


def circles_el(x0, y0, w, h, r):
    el = []
    for i in range(int(w // (2 * r))):
        for j in range(int(h // (2 * r))):
            el.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2'/>"
                      % (x0 + r + 2 * r * i, y0 + r + 2 * r * j, r, SHADE, GREEN))
    return el


def shared_vertex(polys, want, box):
    """The corner nearest the middle of the box where `want` shapes meet."""
    cnt = {}
    for P in polys:
        for p in P:
            k = (round(p[0], 1), round(p[1], 1))
            cnt[k] = cnt.get(k, 0) + 1
    cx, cy = box[0] + box[2] / 2.0, box[1] + box[3] / 2.0
    best = sorted((v for v, c in cnt.items() if c == want), key=lambda v: (v[0] - cx) ** 2 + (v[1] - cy) ** 2)
    assert best, want
    v = best[0]
    assert max(c for c in cnt.values()) == want, (want, max(cnt.values()))
    return v


def centre(polys, box):
    pts = [p for P in polys for p in P]
    dx = box[0] + (box[2] - (max(p[0] for p in pts) - min(p[0] for p in pts))) / 2.0 - min(p[0] for p in pts)
    dy = box[1] + (box[3] - (max(p[1] for p in pts) - min(p[1] for p in pts))) / 2.0 - min(p[1] for p in pts)
    return [[(x + dx, y + dy) for x, y in P] for P in polys]


def patch_svg(kind, dot=False, label="tile pattern"):
    W, H, pad = 220, 120, 6
    box = (pad, pad, W - 2 * pad, H - 2 * pad)
    el, polys = [], []
    if kind == "hex":
        polys = centre(hex_patch(*box, r=20), box)
        el = [poly_el(P, "#e2b93b", "#9a7410", 0.45) for P in polys]
        want = 3
    elif kind == "tri":
        polys = centre(tri_patch(*box, s=40), box)
        el = [poly_el(P, SHADE if k % 2 else SHADE_B, GREEN if k % 2 else BLUE, 0.4) for k, P in enumerate(polys)]
        want = 6
    elif kind == "octsq":
        o, s = octsq_patch(*box, a=20)
        polys = centre(o + s, box)
        o, s = polys[:len(o)], polys[len(o):]
        el = [poly_el(P, SHADE_B, BLUE, 0.4) for P in o] + [poly_el(P, "#e2b93b", "#9a7410", 0.6) for P in s]
        want = 3
    elif kind == "brick":
        el = brick_el(pad, pad, W - 2 * pad, 5 * 20, 20)
        return svg_wrap(W, 2 * pad + 100, "".join(el), label)
    if dot:
        el.append(dot_el(shared_vertex(polys, want, box), 5.5))
    return svg_wrap(W, H, "".join(el), label)


# ------------------------------------------------------------ border strips and a pattern to continue
FLAG = [(8, 6), (14, 6), (42, 18), (14, 30), (14, 64), (8, 64)]     # in a tile 50 wide and 70 high
STRIP = ["a translation", "a reflection", "a half turn", "a reflection and a translation"]
FLIP = {"trans": lambda p: p, "refl": lambda p: (50 - p[0], p[1]),
        "half": lambda p: (50 - p[0], 70 - p[1]), "glide": lambda p: (p[0], 70 - p[1])}


def strip_svg(kind, n=4):
    pad = 8
    el = []
    for k in range(n):
        x0 = pad + 50 * k
        el.append("<rect x='%d' y='%d' width='50' height='70' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x0, pad, THIN))
        f = FLIP[kind] if k % 2 else FLIP["trans"]
        el.append(poly_el([(x0 + f(p)[0], pad + f(p)[1]) for p in FLAG], SHADE, GREEN, 0.5, 2))
    return svg_wrap(2 * pad + 50 * n, 2 * pad + 70, "".join(el), "pattern strip of flag tiles")


FLAG_SQ = [(10, 6), (16, 6), (40, 15), (16, 24), (16, 44), (10, 44)]  # in a tile 50 by 50


def cwk(pts, k):
    for _ in range(k % 4):
        pts = [(50 - y, x) for x, y in pts]     # quarter turn clockwise on the screen about (25, 25)
    return pts


def flipx(pts):
    return [(50 - x, y) for x, y in pts]


def key_of(pts):
    return frozenset((round(x, 3), round(y, 3)) for x, y in pts)


def next_svg(opts):
    pad, g1, LW, g2 = 8, 8, 20, 12
    el = []
    for k in range(4):
        x0, y0 = pad + k * (50 + g1), pad
        el.append("<rect x='%d' y='%d' width='50' height='50' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x0, y0, THIN))
        if k < 3:
            el.append(poly_el([(x0 + x, y0 + y) for x, y in cwk(FLAG_SQ, k)], SHADE, GREEN, 0.5))
        else:
            el.append(text(x0 + 25, y0 + 33, "?", 24, bold=True, col=RED))
    y0 = pad + 50 + 24
    for k, P in enumerate(opts):
        x0 = pad + k * (LW + 50 + g2)
        el.append(text(x0, y0 + 20, "ABCD"[k], 18, anchor="start", bold=True))
        el.append("<rect x='%d' y='%d' width='50' height='50' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x0 + LW, y0, THIN))
        el.append(poly_el([(x0 + LW + x, y0 + y) for x, y in P], SHADE_B, BLUE, 0.5))
    W = 2 * pad + 4 * (LW + 50) + 3 * g2
    return svg_wrap(W, y0 + 50 + pad, "".join(el), "pattern of turning flag tiles with options A to D")


QUILT_T = [(0, 0), (50, 0), (0, 30)]


def quilt_svg():
    pad = 8
    el = []
    for k in range(4):                 # top-left, top-right, bottom-right, bottom-left: each a quarter turn clockwise
        P = QUILT_T
        for _ in range(k):
            P = [(100 - y, x) for x, y in P]
        cell = [(0, 0), (50, 0), (50, 50), (0, 50)]
        for _ in range(k):
            cell = [(100 - y, x) for x, y in cell]
        el.append(poly_el([(pad + x, pad + y) for x, y in cell], "#ffffff", THIN, 1, 1.5))
        el.append(poly_el([(pad + x, pad + y) for x, y in P], "#c0563f", "#8a3a2a", 0.7, 1.5))
    el.append("<rect x='%d' y='%d' width='100' height='100' fill='none' stroke='%s' stroke-width='2'/>" % (pad, pad, INK))
    return svg_wrap(116, 116, "".join(el), "quilt block made of four squares")


# ------------------------------------------------------------ set 1: translation, reflection or rotation?
def set_identify(rnd, P):
    its = []
    pos = Pos(rnd)
    E = {
        "a translation": "Every corner of B is the same number of squares from its matching corner of A, in the same direction, "
                         "and B faces the same way. It was slid: a translation.",
        "a reflection": "B is a mirror image of A: it faces the other way. Each corner of B is the same distance from the mirror line as its "
                        "partner in A. It was flipped: a reflection.",
        "a rotation": "B is A turned about the point O: it is not flipped (it is not a mirror image), and O does not move. It is a rotation.",
        "it changed size": "The sides of B are twice as long as the sides of A. A translation, reflection or rotation never changes the size, "
                           "so B was enlarged.",
    }
    cases = [
        (TRI, (1, 1), T_shift(5, 4), None, None, "%s Every corner moved 5 squares right and 4 squares up."),
        (ELL, (1, 5), T_shift(5, -4), None, None, "%s Every corner moved 5 squares right and 4 squares down."),
        (TRI, (1, 2), T_refl(("v", 5)), ("v", 5), None, "%s The mirror line is x = 5."),
        (ELL, (2, 5), T_refl(("h", 4)), ("h", 4), None, "%s The mirror line is y = 4: B is upside down but is not turned."),
        (TRAP, (1, 3), T_refl(("v", 5)), None, None, "%s The slanted side is on the left of A and on the right of B, at the same height."),
        (TRI, (5, 4), T_rot((5, 4), "cw"), None, (5, 4), "%s The side that pointed right from O now points down: a quarter turn clockwise."),
        (ELL, (6, 5), T_rot((5, 4), "half"), None, (5, 4),
         "%s It is a half turn about O. It looks upside down, but a reflection in a horizontal line would not also swap left and right."),
        (TRAP, (5, 3), T_rot((4, 3), "acw"), None, (4, 3), "%s The bottom side pointed right from O and now points up: a quarter turn anticlockwise."),
        (TRI, (1, 1), T_scale(2, (-2, -1)), None, None, "%s The bottom side of A is 3 squares long; the bottom side of B is 6 squares long."),
    ]
    for shape, base, f, mirror, O, extra in cases:
        G, A, B = pair_grid(shape, base, f, mirror, O)
        ans = classify(A, B)
        what = "Shape A was moved to make shape B. Point O does not move." if O else "Shape A was moved to make shape B."
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) + what + " What happened to shape A?",
                             MOVES, ans, extra % E[ans]))
    its.append(panel_pick(["...#..", "...#..", "...##.", "......", "......", "......"], "flipv", ["slide", "half", "cw"], (-3, 0),
                          "In which picture is the blue shape a reflection of the green shape?", pos, rnd))
    its.append(panel_pick(["......", ".....#", "...###", "......", "......", "......"], "slide", ["fliph", "half", "acw"], (0, 3),
                          "In which picture is the blue shape a translation of the green shape?", pos, rnd))
    its.append(panel_pick(["....#.", "...##.", "...#..", "......", "......", "......"], "cw", ["flipv", "fliph", "slide"], (-3, 0),
                          "In which picture is the blue shape a rotation of the green shape?", pos, rnd))
    its.append(panel_pick(["....#.", "....#.", "...##.", "......", "......", "......"], "fliph", ["half", "flipv", "slide"], (0, 3),
                          "In which picture is the blue shape the green shape reflected in a horizontal mirror line?", pos, rnd))
    L = ["b", "d", "p", "q"]
    its.append(mcq_fixed("The letter <b>b</b> is reflected in a vertical mirror line (flipped left to right). Which letter does it look like?", L, "d",
                         "A vertical mirror flips left and right, so the round part moves to the other side of the stick but stays at the bottom: d."))
    its.append(mcq_fixed("The letter <b>b</b> is reflected in a horizontal mirror line (flipped upside down). Which letter does it look like?", L, "p",
                         "A horizontal mirror flips top and bottom, so the stick now hangs down and the round part stays on the right: p."))
    its.append(mcq_fixed("The letter <b>b</b> is rotated a half turn. Which letter does it look like?", L, "q",
                         "A half turn turns it upside down and back to front at the same time: the stick hangs down and the round part is on the left: q. "
                         "This is not the same as a reflection."))
    its.append(mcq("A lift goes straight up from the ground floor to level 3. Which transformation is this?", "a translation",
                   ["a rotation", "a reflection", "an enlargement"],
                   "The lift slides in one direction without turning or flipping, so it is a translation.", rnd))
    its.append(mcq("A door swings open on its hinges. Which transformation is this?", "a rotation",
                   ["a translation", "a reflection", "an enlargement"],
                   "The door turns about a fixed line (the hinges). Seen from above, it turns about a point: a rotation.", rnd))
    n, he, his = P.next()
    its.append(mcq("Shape B is shape A turned a half turn. %s says, “B is upside down, so it must be a reflection.” What is wrong?" % n,
                   "A half turn also turns a shape upside down",
                   ["Nothing: upside down always means a reflection", "A half turn makes the shape smaller", "A reflection never turns a shape upside down"],
                   "A half turn turns a shape upside down and back to front. A reflection makes a mirror image. "
                   "Check: is B a mirror image of A, or is it A turned?", rnd))
    its.append(mcq("After a translation, a reflection or a rotation, which of these always stays the same?", "the side lengths",
                   ["the position", "the coordinates of the corners", "the way the shape faces"],
                   "These moves change where the shape is (and a reflection or rotation changes the way it faces), but never its size. "
                   "The side lengths and angles always stay the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translation, reflection or rotation?", "items": its}


# ------------------------------------------------------------ set 2: combinations of transformations
def combo_point_cands(p, steps):
    """Answers students get by mistake: only one step, the wrong mirror line, the wrong direction, or the steps in the other order."""
    out = []
    for s in steps:
        out.append(s[1]([p])[0])                        # only one step done
    out.append(chain(*[s[1] for s in reversed(steps)])([p])[0])
    for k, s in enumerate(steps):
        if s[2]:
            out.append(chain(*[(t[2] if j == k else t[1]) for j, t in enumerate(steps)])([p])[0])
    for k, s in enumerate(steps):              # the reflection 1 square too far, or stopping on the mirror line
        if len(s) > 3:
            before = chain(*[t[1] for t in steps[:k]])([p])[0] if k else p
            for q, why, kind in refl_kinds(before, s[3]):
                if kind in ("far", "stop"):
                    out.append(chain(*[t[1] for t in steps[k + 1:]])([q])[0] if k + 1 < len(steps) else q)
    return [q for q in out if inside(q)]


def step_text(s):
    return s[0]


def set_combine(rnd, P):
    its = []

    def R(line):
        other = ("h", line[1]) if line[0] == "v" else ("v", line[1])
        return ("reflected in %s" % lword(line), T_refl(line), T_refl(other), line)

    def S(dx, dy):
        return ("translated %s" % mv_long(dx, dy), T_shift(dx, dy), T_shift(-dx, -dy))

    def Q(o, kind):
        other = {"cw": "acw", "acw": "cw", "half": "cw"}[kind]
        return ("rotated %s about %s" % (TURN[kind], pair(*o)), T_rot(o, kind), T_rot(o, other))

    for p, steps in [((2, 3), [R(("v", 5)), S(0, 2)]), ((7, 1), [R(("h", 3)), S(-4, 0)]), ((1, 6), [R(("v", 4)), S(0, -3)]),
                     ((6, 8), [R(("h", 6)), S(2, 0)]), ((3, 2), [S(2, 0), R(("v", 6))]), ((2, 7), [S(0, -2), R(("h", 4))]),
                     ((7, 4), [Q((5, 4), "cw"), S(3, 0)]), ((5, 6), [Q((5, 4), "half"), S(-2, 0)]),
                     ((8, 2), [Q((6, 2), "acw"), S(0, 3)])]:
        mid = steps[0][1]([p])[0]
        q = steps[1][1]([mid])[0]
        assert inside(mid) and inside(q)
        e1 = _explain(p, steps[0][0], mid)
        e2 = _explain(mid, steps[1][0], q)
        its.append(mcq("Point %s is %s, then %s. Where does it end up?" % (pair(*p), steps[0][0], steps[1][0]),
                       pair(*q), [pair(*c) for c in combo_point_cands(p, steps)],
                       "Do the steps in order. Step 1: %s Step 2: %s" % (e1, e2), rnd))
    for (a, b), (c, d) in [((3, 2), (4, -5)), ((-5, 1), (2, 4))]:
        dx, dy = a + c, b + d
        wrong = [mv(dx, b - d), mv(a - c, dy), mv(dx, -dy), mv(-dx, dy)]
        its.append(mcq("A shape is translated %s, then %s. Which single translation does the same?" % (mv_long(a, b), mv_long(c, d)),
                       mv(dx, dy), wrong,
                       "Combine the moves across and the moves up and down. Across: %s. Up and down: %s. So the single translation is %s."
                       % (_sum_text(a, c, "right", "left"), _sum_text(b, d, "up", "down"), mv_long(dx, dy)), rnd))
    # pictures: A, then the image C after a reflection and a translation; describe the translation
    for i, (shape, base, line, dx, dy) in enumerate([(TRI, (1, 5), ("v", 5), 0, -4), (ELL, (1, 1), ("h", 4), 5, 0), (TRAP, (1, 1), ("v", 5), 0, 5)]):
        f = chain(T_refl(line), T_shift(dx, dy))
        G, A, C = pair_grid(shape, base, f, line, None, names=("A", "C"))
        B = T_refl(line)(A)
        direct = mv(C[0][0] - A[0][0], C[0][1] - A[0][1])
        cands = [direct] + describe_cands(dx, dy, i)
        its.append(mcq(fig(G.svg("coordinate grid with a mirror line, shape A and shape C")) +
                       "Shape A is reflected in the dashed mirror line. Then the image is translated to make shape C. Describe the translation.",
                       mv(dx, dy), cands,
                       "First reflect A in %s: the corner %s goes to %s. Then follow that corner to C: %s → %s is %s. "
                       "Do not measure straight from A to C (that gives %s): A has to be reflected first."
                       % (lname(line), pair(*A[0]), pair(*B[0]), pair(*B[0]), pair(*C[0]), mv_long(dx, dy), direct), rnd))
    # pictures: which two steps?
    for shape, base, right, wrongs in [
        (TRI, (1, 2), ("reflect in x = 5, then translate 3 up", chain(T_refl(("v", 5)), T_shift(0, 3))),
         [("translate 5 right, then translate 3 up", T_shift(5, 3)),
          ("reflect in y = 5, then translate 3 right", chain(T_refl(("h", 5)), T_shift(3, 0))),
          ("rotate a half turn about (5, 4)", T_rot((5, 4), "half"))]),
        (ELL, (1, 5), ("reflect in y = 4, then translate 5 right", chain(T_refl(("h", 4)), T_shift(5, 0))),
         [("translate 5 right, then translate 4 down", T_shift(5, -4)),
          ("rotate a half turn about (5, 4)", T_rot((5, 4), "half")),
          ("reflect in x = 5, then translate 4 down", chain(T_refl(("v", 5)), T_shift(0, -4)))]),
    ]:
        G, A, C = pair_grid(shape, base, right[1], None, None, names=("A", "C"))
        for t, g in wrongs:
            assert not same_shape(g(A), C), t
        why = "; ".join("“%s” puts A at %s" % (t, plist(g(A)[:2]) + ", …") for t, g in wrongs)
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape C")) + "Which two steps move shape A onto shape C?",
                       right[0], [t for t, g in wrongs],
                       "C is a mirror image of A, so one step must be a reflection. Check it corner by corner: %s, so it gives C. "
                       "The others do not: %s." % (", ".join("%s → %s" % (pair(*a), pair(*c)) for a, c in zip(A[:2], right[1](A)[:2])), why), rnd))
    flag = [(2, 1), (2, 3), (3, 3)]
    two = chain(T_refl(("v", 5)), T_refl(("h", 4)))(flag)
    assert same_shape(two, T_rot((5, 4), "half")(flag)) and not same_shape(two, T_rot((5, 4), "cw")(flag))
    its.append(mcq("A shape is reflected in the line x = 5, then the image is reflected in the line y = 4. Which single move does the same?",
                   "a half turn about (5, 4)", ["a reflection in the line y = 4", "a quarter turn about (5, 4)", "a translation 4 squares up"],
                   "Two reflections in lines that cross at right angles make a half turn about the point where they cross, (5, 4). "
                   "For example (2, 1) → (8, 1) → (8, 7), and a half turn about (5, 4) also takes (2, 1) to (8, 7).", rnd))
    two = chain(T_refl(("v", 2)), T_refl(("v", 5)))(flag)
    assert same_shape(two, T_shift(6, 0)(flag))
    its.append(mcq("A shape is reflected in the line x = 2, then the image is reflected in the line x = 5. Which single move does the same?",
                   "a translation 6 squares right", ["a translation 3 squares right", "a half turn about (5, 0)", "a reflection in the line x = 7"],
                   "Two reflections in parallel lines make a translation of twice the gap between the lines: 2 × 3 = 6 squares right. "
                   "For example (3, 1) → (1, 1) → (9, 1), which is 6 squares right of (3, 1).", rnd))
    a1 = chain(T_refl(("v", 4)), T_shift(3, 0))([(2, 3)])[0]
    a2 = chain(T_shift(3, 0), T_refl(("v", 4)))([(2, 3)])[0]
    its.append(mcq("Point (2, 3) is reflected in x = 4 and translated 3 squares right. Does the order of the two steps matter?",
                   "Yes: %s or %s" % (pair(*a1), pair(*a2)),
                   ["No: both orders give %s" % pair(*a1), "No: both orders give %s" % pair(*a2), "Yes, but only the y-coordinate changes"],
                   "Reflect first: (2, 3) → (6, 3) → %s. Translate first: (2, 3) → (5, 3) → %s. The answers are different, so do the steps "
                   "in the order given." % (pair(*a1), pair(*a2)), rnd))
    its.append(mcq("A shape is rotated a quarter turn clockwise about a point, then another quarter turn clockwise about the same point. "
                   "Which single move does the same?", "a half turn about that point",
                   ["a quarter turn anticlockwise", "a reflection", "a full turn"],
                   "Two quarter turns make a half turn: 90° + 90° = 180°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Combinations: reflect, translate and rotate", "items": its}


def _sum_text(a, c, pos_w, neg_w):
    def w(v):
        return "%d %s" % (abs(v), pos_w if v > 0 else neg_w)
    if not a and not c:
        return "none"
    t = a + c
    res = "no move" if t == 0 else w(t)
    return "%s and %s make %s" % (w(a), w(c), res)


def _explain(p, step, q):
    if step.startswith("reflected"):
        m = re.search(r"(x|y) = (\d+)", step)
        line = ("v" if m.group(1) == "x" else "h", int(m.group(2)))
        return refl_e(p, line, "the point").replace("the point", "The point", 1)
    if step.startswith("translated"):
        return "%s → %s." % (pair(*p), pair(*q)) + " " + move_e(p, q[0] - p[0], q[1] - p[1])
    m = re.search(r"rotated (.+) about \((\d+), (\d+)\)", step)
    kind = [k for k, v in TURN.items() if v == m.group(1)][0]
    o = (int(m.group(2)), int(m.group(3)))
    return rot_e(p, o, kind, "the point").replace("From O ", "From the centre ").replace(" from O:", " from the centre:")


# ------------------------------------------------------------ set 3: which shapes tessellate?
def set_which(rnd, P):
    its = []
    pos = Pos(rnd)
    for n, wrong in [(4, [3, 5, 2]), (3, [3, 4, 5]), (6, [2, 4, 6])]:
        a = interior(n)
        k = 360 // a
        assert k * a == 360
        its.append(mcq_num(fig(angle_svg(n, "%d°" % a)) + "Each angle of %s %s is %d°. How many %ss fit together around one point with no gaps?"
                           % ("an" if NAME[n][0] in "aeiou" else "a", NAME[n], a, NAME[n]), k, [w for w in wrong if w != k],
                           "The angles around a point add up to 360°. 360° ÷ %d° = %d, so %d %ss fit exactly around each point."
                           % (a, k, k, NAME[n])))
    its.append(mcq(fig(angle_svg(5, "108°")) + "Each angle of a regular pentagon is 108°. Can regular pentagons fit around a point with no gaps?",
                   "No: 3 × 108° = 324°, which leaves a gap",
                   ["Yes: 3 regular pentagons fit exactly", "Yes: 4 regular pentagons fit exactly", "Yes: every regular shape fits"],
                   "3 × 108° = 324°, which is less than 360°, so there is a gap of 36°. 4 × 108° = 432°, which is more than 360°, "
                   "so a fourth pentagon would overlap. Regular pentagons do not tessellate.", rnd))
    its.append(mcq_num(fig(vertex_svg([5, 5, 5], "?", "three regular pentagons around a point with a gap")) +
                       "Three regular pentagons meet at the red dot. Each angle of a regular pentagon is 108°. What is the size of the gap?",
                       36, [72, 108, 54],
                       "3 × 108° = 324°. A full turn is 360°, so the gap is 360° − 324° = 36°. No regular shape has a 36° angle, so the gap "
                       "cannot be filled with the same tiles.", fmt="%d°"))
    its.append(mcq(fig(angle_svg(8, "135°")) + "Each angle of a regular octagon is 135°. Why do regular octagons not tessellate on their own?",
                   "2 make 270° (a gap) and 3 make 405° (an overlap)",
                   ["They have too many sides", "135° is an obtuse angle", "Their sides are too short"],
                   "Around a point the angles must add up to exactly 360°. 2 × 135° = 270° leaves a gap and 3 × 135° = 405° is too much. "
                   "135° does not divide exactly into 360°.", rnd))
    its.append(mcq("What does it mean when a shape tessellates?", "Copies of it fit together with no gaps and no overlaps",
                   ["Copies of it fit together with small gaps between them", "It has at least one line of symmetry",
                    "It can be turned onto itself"],
                   "A tessellation is a pattern of shapes that covers a surface with no gaps and no overlaps, like the tiles on a floor.", rnd))
    order = [0, 5, 8]
    rnd.shuffle(order)
    p = pos.next()
    order.insert(p, 6)
    its.append(mcq_fixed(fig(four_boxes([(lambda n: lambda x, y, w, h: shape_box(n, x, y, w, h))(n) for n in order], "four shapes A to D")) +
                         "Which shape tessellates on its own?", LETTERS, "ABCD"[p],
                         "The regular hexagon (%s): each angle is 120° and 3 × 120° = 360°. A regular pentagon (108°) and a regular octagon "
                         "(135°) leave gaps, and circles cannot fit together without gaps." % "ABCD"[p]))
    order = [4, 3, 6]
    rnd.shuffle(order)
    p = pos.next()
    order.insert(p, 5)
    its.append(mcq_fixed(fig(four_boxes([(lambda n: lambda x, y, w, h: shape_box(n, x, y, w, h))(n) for n in order], "four shapes A to D")) +
                         "Which shape does NOT tessellate on its own?", LETTERS, "ABCD"[p],
                         "The regular pentagon (%s): its angles are 108° and 360° ÷ 108° is not a whole number. Squares (4 × 90°), "
                         "equilateral triangles (6 × 60°) and regular hexagons (3 × 120°) all fit exactly around a point." % "ABCD"[p]))
    its.append(mcq("Why do circles not tessellate?", "Their curved edges always leave gaps",
                   ["They have no angles, so they fit anywhere", "They are too big", "They only tessellate in rows"],
                   "When circles touch, there are always curved gaps between them. A tessellation can have no gaps.", rnd))
    its.append(mcq("Which regular shapes tessellate on their own?", "Only equilateral triangles, squares and regular hexagons",
                   ["Every regular shape", "Only squares", "Every regular shape with an even number of sides"],
                   "A regular shape tessellates only if its angle divides exactly into 360°: 60° (6 fit), 90° (4 fit) and 120° (3 fit). "
                   "Regular pentagons (108°) and octagons (135°) do not, even though octagons have an even number of sides.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says, “All regular shapes tessellate.” Which shape shows that %s is wrong?" % (n, he), "a regular pentagon",
                   ["a square", "an equilateral triangle", "a regular hexagon"],
                   "Regular pentagons leave a 36° gap around a point (3 × 108° = 324°). Squares, equilateral triangles and regular hexagons "
                   "do tessellate, so they do not show %s is wrong." % n, rnd))
    its.append(mcq_num("In a tessellation, what do the angles that meet at a point add up to?", 360, [180, 90, 540],
                       "The shapes go all the way around the point with no gaps and no overlaps: a full turn, 360°. "
                       "(180° is the angles on a straight line or in a triangle.)", fmt="%d°"))
    its.append(mcq_fixed("A regular shape tessellates on its own only if its angle divides exactly into 360°. Which angle works?",
                         ["108°", "120°", "135°", "140°"], "120°",
                         "360° ÷ 120° = 3 exactly. 360 ÷ 108, 360 ÷ 135 and 360 ÷ 140 are not whole numbers, so those shapes leave gaps."))
    its.append(mcq("Do rectangles tessellate?", "Yes: four 90° corners fill the 360° around a point",
                   ["No: only squares tessellate", "No: their sides are not all equal", "Only if they are turned on an angle"],
                   "Each corner of a rectangle is 90°, and 4 × 90° = 360°. Rows of rectangles, like bricks or floorboards, cover a surface "
                   "with no gaps. The sides do not need to be equal.", rnd))
    its.append(mcq_num("Copies of any triangle can tessellate. A triangle has angles of 50°, 60° and 70°. In a tessellation of this triangle, "
                       "each angle appears twice at every meeting point. How many triangles meet at each point?", 6, [3, 4, 2],
                       "Each angle appears twice: 2 × (50° + 60° + 70°) = 2 × 180° = 360°. That is 6 angles, so 6 triangles meet at each point.",
                       fmt="%d"))
    its.append(mcq_num(fig(vertex_svg([8, 8], "?", "two regular octagons around a point with a gap")) +
                       "Two regular octagons meet at the red dot. Each angle of a regular octagon is 135°. What is the size of the gap?",
                       90, [45, 135, 270],
                       "2 × 135° = 270°, and 360° − 270° = 90°. A square fits the gap exactly, so octagons and squares tessellate together.",
                       fmt="%d°"))
    its.append(mcq_num(fig(vertex_svg([6, 6], "?", "two regular hexagons around a point with a gap")) +
                       "Two regular hexagons meet at the red dot. How many equilateral triangles fill the gap?", 2, [1, 3, 4],
                       "2 × 120° = 240°, so the gap is 360° − 240° = 120°. Each equilateral triangle has 60° angles: 120° ÷ 60° = 2 triangles."))
    its.append(mcq_num("Two squares meet at a point. How many equilateral triangles fill the rest of the space around the point?", 3, [2, 4, 6],
                       "2 × 90° = 180°, so 360° − 180° = 180° is left. 180° ÷ 60° = 3 equilateral triangles."))
    its.append(mcq("Each angle of a regular dodecagon (12 sides) is 150°. Does it tessellate on its own?",
                   "No: 2 make 300° and 3 make 450°",
                   ["Yes: it has an even number of sides", "Yes: 150° is less than 180°", "Yes: 12 divides into 360"],
                   "2 × 150° = 300° leaves a 60° gap and 3 × 150° = 450° overlaps. 360° ÷ 150° is not a whole number, so it does not "
                   "tessellate on its own. (The 60° gap could be filled by an equilateral triangle.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Which shapes tessellate? Angles at a point", "items": its}


# ------------------------------------------------------------ set 4: tessellating patterns in tiles and art
def set_patterns(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq(fig(patch_svg("brick", label="brick wall pattern")) + "In this brick wall, how is each row placed compared with the row below it?",
                   "translated (slid) half a brick along",
                   ["reflected in a vertical line", "rotated a quarter turn", "exactly above the row below"],
                   "Each row is the row below slid half a brick sideways (and up one row). Nothing is flipped or turned, so it is a translation.", rnd))
    its.append(mcq_num(fig(patch_svg("hex", True, "honeycomb pattern of regular hexagons with a red dot")) +
                       "How many hexagons meet at the red dot?", 3, [2, 4, 6],
                       "3 hexagons meet at each corner. Each angle is 120°, and 3 × 120° = 360°."))
    its.append(mcq_num(fig(patch_svg("tri", True, "pattern of equilateral triangles with a red dot")) +
                       "How many triangles meet at the red dot?", 6, [3, 4, 8],
                       "6 triangles meet at each point. Each angle is 60°, and 6 × 60° = 360°."))
    its.append(mcq(fig(patch_svg("octsq", label="floor tile pattern of octagons and squares")) + "Which two shapes make this floor tile pattern?",
                   "regular octagons and squares",
                   ["regular hexagons and squares", "regular octagons and triangles", "regular pentagons and squares"],
                   "The large tiles have 8 equal sides (regular octagons) and the small tiles are squares turned on an angle. At each corner, "
                   "135° + 135° + 90° = 360°.", rnd))
    its.append(mcq_num(fig(patch_svg("octsq", True, "floor tile pattern of octagons and squares with a red dot")) +
                       "How many tiles meet at the red dot?", 3, [2, 4, 5],
                       "2 octagons and 1 square meet at each corner: 135° + 135° + 90° = 360°."))
    q = "This border pattern repeats one flag tile. How is each tile made from the tile before it?"
    for kind, ans, e in [
        ("trans", "a translation", "Every flag points the same way and is the same way up. Each one is the one before slid 1 tile to the right."),
        ("refl", "a reflection", "The flags point right, left, right, left but stay the same way up: each is a mirror image of the one before, "
                                 "with the mirror line on the edge between the tiles. A half turn would also turn it upside down."),
        ("half", "a half turn", "Each flag is upside down and points the other way. It is the one before turned a half turn about the middle "
                                "of the edge between the tiles. A reflection flips it only one way."),
        ("glide", "a reflection and a translation", "Each flag is upside down but still points right. It is reflected in the line across the middle "
                                                    "of the strip and then slid 1 tile along, like a trail of footprints."),
    ]:
        its.append(mcq_fixed(fig(strip_svg(kind)) + q, STRIP, ans, e))
    p = pos.next()
    right = cwk(FLAG_SQ, 3)
    wr = [("it is turned anticlockwise, back to the second tile", cwk(FLAG_SQ, 1)),
          ("it is a mirror image of the right answer, flipped, not turned", flipx(cwk(FLAG_SQ, 3))),
          ("it is turned one quarter turn too far, back to the start", cwk(FLAG_SQ, 0))]
    rnd.shuffle(wr)
    opts = [w[1] for w in wr]
    opts.insert(p, right)
    assert len({key_of(o) for o in opts}) == 4
    others = "; ".join("%s: %s" % ("ABCD"[j], w[0]) for j, w in zip([j for j in range(4) if j != p], wr))
    its.append(mcq_fixed(fig(next_svg(opts)) + "Each tile is the tile before turned a quarter turn clockwise. Which tile comes next?", LETTERS, "ABCD"[p],
                         "The flag on the pole points right, then down, then left. One more quarter turn clockwise makes it point up: <b>%s</b>. "
                         "The others: %s." % ("ABCD"[p], others)))
    p = pos.next()
    wr = [("circles", lambda x, y, w, h: circles_el(x, y, w, h, 16), "the circles leave curved gaps"),
          ("pentagons", lambda x, y, w, h: [poly_el(S) for S in fit(around([5, 5, 5])[0], x + 8, y + 4, w - 16, h - 8)[0]],
           "the pentagons leave a gap"),
          ("octagons", lambda x, y, w, h: [poly_el(S, SHADE_B, BLUE) for S in octsq_patch(x, y + 3, w, h - 6, 14, False)[0]],
           "the octagons leave square gaps")]
    rnd.shuffle(wr)
    draws = [w[1] for w in wr]
    draws.insert(p, lambda x, y, w, h: [poly_el(S, SHADE if (k // 4 + k) % 2 else SHADE_B, GREEN if (k // 4 + k) % 2 else BLUE)
                                        for k, S in enumerate(squares_patch(x + 2, y + 2, w - 4, h - 4, 24))])
    others = "; ".join("%s: %s" % ("ABCD"[j], w[2]) for j, w in zip([j for j in range(4) if j != p], wr))
    its.append(mcq_fixed(fig(four_boxes(draws, "four patterns A to D")) + "Which pattern is a tessellation?", LETTERS, "ABCD"[p],
                         "A tessellation has no gaps and no overlaps. Only the squares (<b>%s</b>) fit together with no gaps. The others: %s."
                         % ("ABCD"[p], others)))
    # the quilt: check which move takes the top-left square to the top-right one
    cellT = [(0, 0), (50, 0), (50, 50), (0, 50)]
    nxt = [(100 - y, x) for x, y in QUILT_T]
    assert same_shape(nxt, [(100 - y, x) for x, y in QUILT_T])
    assert not same_shape(nxt, [(100 - x, y) for x, y in QUILT_T]) and not same_shape(nxt, [(x + 50, y) for x, y in QUILT_T])
    assert not same_shape(nxt, [(100 - x, 100 - y) for x, y in QUILT_T])
    its.append(mcq(fig(quilt_svg()) + "This quilt block has 4 small squares. How is each small square made from the one before it, going round clockwise?",
                   "a quarter turn clockwise about the centre of the block",
                   ["a reflection in the line between them", "a translation", "a half turn about the centre of the block"],
                   "Look at the side of each red triangle that runs the whole width of its small square: it lies along the top of the block, "
                   "then the right side, then the bottom, then the left. "
                   "Each square is the one before turned 90° clockwise about the centre. A reflection would make a mirror image.", rnd))
    its.append(mcq("An artist cuts a bump out of the left side of a square tile and sticks the same bump on the right side, without turning it. "
                   "Will copies of the new tile still tessellate?", "Yes: each bump fits into the gap in the next tile",
                   ["No: only regular shapes tessellate", "No: curved edges always leave gaps", "Only if the bump is cut off again"],
                   "The bump was translated from one side to the opposite side, so the shape of the gap matches the shape of the bump exactly. "
                   "Artists such as M. C. Escher used this idea to make tessellations of animals and birds.", rnd))
    its.append(mcq("In a geometry app, Isla turns a triangle a half turn about the midpoint of one of its sides. "
                   "What shape do the triangle and its image make together?", "a parallelogram",
                   ["a bigger triangle", "a kite", "a regular hexagon"],
                   "The half turn puts a copy of the triangle against the same side, upside down. The two triangles make a parallelogram, "
                   "which has two pairs of parallel sides. Rows of parallelograms tessellate, so any triangle tessellates.", rnd))
    its.append(mcq("In a honeycomb pattern of regular hexagons, how many other hexagons share a side with each hexagon (not at the edge)?",
                       "6", ["3", "4", "12"],
                       "A hexagon has 6 sides, and each side is shared with one neighbour, so it touches 6 others. "
                       "(3 is the number of hexagons that meet at each corner.)", rnd))
    its.append(mcq("A trail of footprints in the sand goes left foot, right foot, left foot, right foot. How is each footprint made from the one before?",
                   "a reflection and a translation",
                   ["only a translation", "only a reflection", "a half turn"],
                   "A right foot is a mirror image of a left foot, so there is a reflection. The footprint is also further along the beach, "
                   "so there is a translation too.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s turns a square tile a quarter turn about one corner, again and again. How many tiles fit around that corner?" % n,
                   "4", ["2", "3", "8"],
                   "Each quarter turn is 90°. 360° ÷ 90° = 4, so 4 tiles fill the space around the corner.", rnd))
    its.append(mcq("Which tile could NOT be used on its own to cover a floor with no gaps?", "a regular octagon",
                   ["a rectangle", "a regular hexagon", "an equilateral triangle"],
                   "Regular octagons (135°) leave square gaps, which is why octagon floors have small square tiles between them. "
                   "Rectangles, regular hexagons and equilateral triangles cover a floor on their own.", rnd))
    its.append(mcq("In an art project, a pattern has 1 regular hexagon and some equilateral triangles at every corner. "
                       "How many triangles are at each corner?", "4", ["2", "3", "6"],
                       "The hexagon’s angle is 120°, so 360° − 120° = 240° is left. 240° ÷ 60° = 4 triangles.", rnd))
    its.append(mcq("In a honeycomb pattern, which transformation moves a hexagon onto the next hexagon in the same row?", "a translation",
                   ["a reflection only", "a quarter turn", "an enlargement"],
                   "All the hexagons face the same way, so each one is the one before slid along: a translation. "
                   "A quarter turn would not put a hexagon onto its neighbour.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Tessellating patterns in tiles and art", "items": its}


# ------------------------------------------------------------ set 5: problems
def money(v):
    return "$%.2f" % v


def set_problems(rnd, P):
    its = []
    n, he, his = P.next()
    its.append(mcq_num("%s is tiling a bathroom floor that is 2 m long and 1.5 m wide with square tiles 50 cm long. How many tiles are needed?" % n,
                       12, [7, 14, 3],
                       "Change metres to centimetres: 200 cm and 150 cm. 200 ÷ 50 = 4 tiles along and 150 ÷ 50 = 3 tiles across. "
                       "4 × 3 = 12 tiles. (4 + 3 = 7 adds instead of multiplying.)", fmt="%d tiles"))
    assert (120 // 20) * (60 // 20) == 18
    its.append(mcq_num("A kitchen splashback is 120 cm long and 60 cm high. It is covered with square tiles 20 cm long. How many tiles are needed?",
                       18, [9, 6, 72], "120 ÷ 20 = 6 tiles along and 60 ÷ 20 = 3 tiles up. 6 × 3 = 18 tiles. (6 is only one row.)", fmt="%d tiles"))
    its.append(mcq("Tiles for the splashback cost $3.50 each. How much do 18 tiles cost?", money(18 * 3.5),
                   [money(18 + 3.5), money(18 * 3), money(18 * 35)],
                   "18 × $3.50 = 18 × $3 + 18 × 50c = $54 + $9 = $63.00.", rnd))
    its.append(mcq_num("A classroom floor is 8 m long and 6 m wide. Carpet tiles are squares 50 cm long. How many carpet tiles cover the floor?",
                       192, [48, 28, 96],
                       "50 cm is half a metre, so 2 tiles fit in each metre. 8 m = 16 tiles along and 6 m = 12 tiles across. 16 × 12 = 192 tiles. "
                       "(48 is the area in square metres, not the number of tiles.)", fmt="%d tiles"))
    its.append(mcq_num("A border of tiles 15 cm long runs along a wall 3 m long. How many tiles are in the border?", 20, [2, 45, 200],
                       "3 m = 300 cm. 300 ÷ 15 = 20 tiles.", fmt="%d tiles"))
    its.append(mcq_num("Floor tiles come in boxes of 12. A tiler needs 100 tiles. How many boxes must be bought?", 9, [8, 12, 88],
                       "100 ÷ 12 = 8 remainder 4. 8 boxes hold only 96 tiles, so a 9th box is needed for the last 4 tiles.", fmt="%d boxes"))
    its.append(mcq("Mosaic tiles for a school mural cost $2.40 each. How much do 25 tiles cost?", money(25 * 2.4),
                   [money(25 + 2.4), money(50), money(600)],
                   "25 × $2.40 = 25 × $2 + 25 × 40c = $50 + $10 = $60.00.", rnd))
    its.append(mcq_num("A tile pattern has a square, a regular hexagon and a regular dodecagon at every corner. The square’s angle is 90° and the hexagon’s angle "
                       "is 120°. What is the angle of the dodecagon?", 150, [270, 240, 210],
                       "The angles around a point add up to 360°. 360° − 90° − 120° = 150°. (270° and 240° take away only one of the angles; 210° uses 60° for the hexagon.)",
                       fmt="%d°"))
    its.append(mcq("In a geometry app, Ruby reflects the point (2, 3) in the line x = 5, then translates it 2 squares up. Where does it end up?",
                   "(8, 5)", ["(8, 3)", "(2, 5)", "(8, 1)"],
                   "(2, 3) is 3 squares left of x = 5, so its image is 3 squares right: (8, 3). Then 2 up: (8, 5).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s designs a logo in a drawing program. The point (7, 4) is rotated a half turn about (5, 4). Where does it go?" % n,
                   "(3, 4)", ["(5, 6)", "(5, 2)", "(1, 4)"],
                   "(7, 4) is 2 squares right of (5, 4). A half turn turns right into left, so the image is 2 squares left: (3, 4). "
                   "(5, 6) and (5, 2) are quarter turns; (1, 4) is too far.", rnd))
    its.append(mcq_num("A stamp makes a pattern along a strip. The first print is at x = 1, and each new print is translated 4 squares right. "
                       "What is the x-coordinate of the 6th print?", 21, [25, 24, 17],
                       "From the 1st print to the 6th print there are 5 moves: 1 + 5 × 4 = 21. (25 counts 6 moves.)"))
    n, he, his = P.next()
    its.append(mcq("%s wants to tile a floor with regular pentagons only. What will happen?" % n, "There will be gaps between the tiles",
                   ["The tiles will fit with no gaps", "The tiles will fit if they are made smaller", "The tiles will fit if there is an even number"],
                   "Each angle of a regular pentagon is 108°. 3 × 108° = 324° leaves a 36° gap at every corner. Making the tiles smaller does not change "
                   "the angles.", rnd))
    its.append(mcq_num("A patio of 3 square metres is paved with hexagon pavers. Each paver covers 0.1 square metres. About how many pavers are needed?",
                       30, [3, 300, 33],
                       "3 ÷ 0.1 = 30 pavers (10 pavers cover each square metre, and 3 × 10 = 30).", fmt="%d pavers"))
    its.append(mcq("A standard Australian brick is 230 mm long. In a brick wall, each row is translated half a brick along. How far is each row moved?",
                   "115 mm", ["230 mm", "460 mm", "57.5 mm"],
                   "Half of 230 mm is 230 ÷ 2 = 115 mm.", rnd))
    its.append(mcq_num("A garden path is 4 m long and 2 pavers wide. The pavers are squares 40 cm long. How many pavers are needed?",
                       20, [10, 40, 5],
                       "4 m = 400 cm. 400 ÷ 40 = 10 pavers along, and the path is 2 pavers wide: 10 × 2 = 20 pavers.", fmt="%d pavers"))
    its.append(mcq("In a coding program, a tile is rotated 270° clockwise. Which rotation ends in the same position?", "90° anticlockwise",
                   ["90° clockwise", "180°", "270° anticlockwise"],
                   "A full turn is 360°. 270° clockwise is 90° short of a full turn, which is the same as turning 90° the other way, anticlockwise.", rnd))
    its.append(mcq("A sprite is translated 3 squares right and 2 squares up, then 1 square left and 4 squares up. Which single translation does the same?",
                   "2 squares right and 6 squares up",
                   ["4 squares right and 6 squares up", "2 squares right and 2 squares down", "4 squares right and 2 squares up"],
                   "Across: 3 right and 1 left make 2 right. Up: 2 up and 4 up make 6 up.", rnd))
    n, he, his = P.next()
    its.append(mcq_num("%s is making a quilt that is 5 blocks across and 6 blocks down. Each block has 4 triangles in a pinwheel. "
                       "How many triangles are there?" % n, 120, [30, 34, 60],
                       "5 × 6 = 30 blocks. 30 × 4 = 120 triangles.", fmt="%d triangles"))
    its.append(mcq_num("A mural design has 2 equal regular octagons and a square at each corner. What is the angle of each octagon?",
                       135, [270, 180, 90],
                       "360° − 90° = 270° for the two octagons. 270° ÷ 2 = 135° each. (270° forgets to share between the two octagons.)",
                       fmt="%d°"))
    n, he, his = P.next()
    its.append(mcq("%s says regular octagons tessellate on their own because 8 is an even number. Which reason shows %s is wrong?" % (n, he),
                   "135° does not divide into 360°: 2 make 270° and 3 make 405°",
                   ["Octagons are too big to tile", "Only shapes with 4 sides tessellate", "Even numbers of sides never tessellate"],
                   "What matters is the angle, not the number of sides. Squares (4 sides) and hexagons (6 sides) do tessellate, but "
                   "octagons leave a 90° gap at every corner.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Tiling and design problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    G = Grid(10, 8)
    G.mirror("v", 5)
    A = [(1, 5), (4, 5), (1, 7)]
    B = T_refl(("v", 5))(A)
    C = T_shift(0, -4)(B)
    G.poly(A, GREEN, "A").poly(B, BLUE, "B").poly(C, RED, "C")
    G.arrow((6, 5), (6, 1))
    G.note(6.2, 3.3, "4 down", anchor="start")
    combo = G.svg("triangle A reflected in x = 5 to make B, then B translated 4 squares down to make C")
    fits = vertex_svg([6, 6, 6], None, "three regular hexagons around a point")
    gap = vertex_svg([5, 5, 5], "?", "three regular pentagons around a point with a gap")
    octs = patch_svg("octsq", label="floor tile pattern of octagons and squares")
    return (
        "<h2>Three ways to move a shape</h2>"
        "<p>A <b>translation</b> slides a shape. A <b>reflection</b> flips it in a mirror line, so it becomes a mirror image. "
        "A <b>rotation</b> turns it about a point. The shape stays the same size and keeps the same angles.</p>" +
        table(["Move", "Faces the same way?", "Check"], [
            ["translation (slide)", "yes", "every corner moves the same distance in the same direction"],
            ["reflection (flip)", "no: mirror image", "each corner is the same distance from the mirror line, on the other side"],
            ["rotation (turn)", "turned", "one point (the centre) stays still"],
        ]) +
        "<h2>Combinations of transformations</h2>"
        "<p>You can do one move after another. Do the steps <b>in order</b>, and follow one corner through each step.</p>"
        "<figure class='sn-fig'>" + combo +
        "<figcaption>Triangle A is reflected in x = 5 to make B, then B is translated 4 squares down to make C. "
        "The corner (4, 5) goes to (6, 5), then to (6, 1).</figcaption></figure>" +
        ex("Example 1", "Reflect (2, 3) in the line x = 5, then translate it 2 squares up.",
           "(2, 3) is 3 squares left of x = 5, so its image is 3 squares right: (8, 3). Then 2 up: (8, 5).", "(8, 5)") +
        "<p>A reflection followed by a translation along the mirror line is like a trail of footprints: left, right, left, right.</p>"
        "<h2>Tessellations</h2>"
        "<p>A shape <b>tessellates</b> when copies of it cover a surface with <b>no gaps and no overlaps</b>. "
        "Where the corners meet, the angles must add up to <b>360°</b>.</p>"
        "<figure class='sn-fig'>" + fits +
        "<figcaption>3 regular hexagons: 3 × 120° = 360°. They fit exactly, so hexagons tessellate (like a honeycomb).</figcaption></figure>"
        "<figure class='sn-fig'>" + gap +
        "<figcaption>3 regular pentagons: 3 × 108° = 324°. There is a 36° gap, so regular pentagons do not tessellate.</figcaption></figure>" +
        table(["Regular shape", "Each angle", "Around a point", "Tessellates on its own?"], [
            ["equilateral triangle", "60°", "6 × 60° = 360°", "yes"],
            ["square", "90°", "4 × 90° = 360°", "yes"],
            ["regular hexagon", "120°", "3 × 120° = 360°", "yes"],
            ["regular pentagon", "108°", "3 × 108° = 324° (gap)", "no"],
            ["regular octagon", "135°", "2 × 135° = 270° (gap)", "no"],
        ]) +
        "<p>Circles never tessellate: curved edges leave gaps. Any triangle and any quadrilateral tessellates, because their angles can fill 360°.</p>"
        "<figure class='sn-fig'>" + octs +
        "<figcaption>Octagons and squares together: 135° + 135° + 90° = 360°. Tile patterns like this use two shapes.</figcaption></figure>" +
        ex("Example 2", "Two regular hexagons meet at a point. How many equilateral triangles fill the gap?",
           "2 × 120° = 240°. 360° − 240° = 120°. 120° ÷ 60° = 2.", "2 triangles") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a half turn a reflection because the shape is upside down", "Check for a mirror image: a half turn also swaps left and right"],
            ["Thinking all regular shapes tessellate", "Only triangles, squares and hexagons: their angles divide exactly into 360°"],
            ["Doing a combination in the wrong order", "Do the steps in the order given and follow one corner"],
            ["Measuring the translation straight from the first shape to the last", "Do the reflection first, then measure the slide"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about transformations and tessellations in the Australian Curriculum?",
     "a": "In Year 6 (AC9M6SP03) students recognise and use combinations of translations, reflections and rotations to create tessellations "
          "and other geometric patterns, often using geometry software."},
    {"q": "Which shapes tessellate?",
     "a": "Equilateral triangles, squares and regular hexagons tessellate on their own, and so does any triangle or quadrilateral. "
          "Regular pentagons, regular octagons and circles do not."},
    {"q": "Why does a regular pentagon not tessellate?",
     "a": "Each angle is 108°. Three pentagons make 324°, leaving a 36° gap, and four make 432°, which overlaps, so they cannot fill the 360° around a point."},
    {"q": "What is a combination of transformations?",
     "a": "It is two or more moves done one after another, such as a reflection followed by a translation. "
          "Do the steps in order; changing the order can give a different result."},
]


def gen_unit():
    rnd = random.Random(6818)
    P = People(rnd)
    sets = [set_identify(rnd, P), set_combine(rnd, P), set_which(rnd, P), set_patterns(rnd, P), set_problems(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "transformations-and-tessellations", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Transformations and Tessellations",
        "seo_title": "Year 6 Transformations and Tessellations Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Transformations and tessellations",
        "domain": "Space",
        "standard_code": "AC9M6SP03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "recognise and use combinations of transformations to create tessellations and other geometric patterns, using dynamic geometric software where appropriate",
        "meta_desc": "Free Year 6 maths worksheets on transformations and tessellations, aligned to the Australian Curriculum (AC9M6SP03): translations, reflections and rotations, combinations of moves, which shapes tessellate and why (angles at a point), tile patterns and design problems. 100 questions with an answer key.",
        "key_big": "A shape tessellates when copies fit around every point with no gaps or overlaps: the angles there must add up to 360°.",
        "key_sub": "Translate = slide, reflect = flip, rotate = turn. Equilateral triangles (6 × 60°), squares (4 × 90°) and regular hexagons (3 × 120°) tessellate; regular pentagons, octagons and circles do not.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(coordinate grid|four grid pictures|four shapes|four patterns|pattern|brick wall|honeycomb|floor tile)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
