# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Combinations of Transformations
(BC Mathematics Curriculum, Grade 6: Geometry and measurement, "combinations of transformations")
  python3 tools/gen_cabc_math_g6_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10 (Grade 6 does not use negative coordinates).
Canadian English (counterclockwise, centre, colour). Lines of reflection are vertical (x = m) or horizontal (y = m);
rotations are 90° clockwise, 90° counterclockwise or 180° about a grid point. Up to two transformations in a row.
Every image is computed by the transformation functions below; every "which combination" answer is checked:
the right steps map the shape onto the image and no wrong choice does.
Wrong answers come from real mistakes: doing the steps in the wrong order, turning the wrong way, reflecting in
the wrong kind of line, counting the line of reflection or the start point as a jump, swapping the numbers in a
turn, translating the wrong way, and stopping after the first step.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MIRROR = "#8e44ad"
THIN = "#a8a8a8"
FONT = "Arial, Helvetica, sans-serif"
HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
LETTERS = ["A", "B", "C", "D"]
MOVES = ["a slide (translation)", "a flip (reflection)", "a turn (rotation)", "it changed size"]
NAME = {"a translation": MOVES[0], "a reflection": MOVES[1], "a rotation": MOVES[2]}
ROTS = ["90° clockwise", "90° counterclockwise", "180°", "360°"]
CHECK = ["Yes, it is correct", "No, it is 1 unit too close to the line", "No, it was turned, not flipped", "No, it was slid, not flipped"]


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


def units(n):
    return "%d unit%s" % (n, "" if n == 1 else "s")


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


# ------------------------------------------------------------ first-quadrant grid
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
    """First-quadrant grid from 0 to nx across and 0 to ny up. One grid space = u px."""

    def __init__(self, nx, ny, u=22):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u = nx, ny, u
        self.ox = tw(ny, 14) + 15
        self.oy = 30 + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26))
        self.pts, self.segs, self.arrows, self.notes, self.polys, self.mirrors, self.arcs = [], [], [], [], [], [], []

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

    def arc(self, c, a, b, cw, col=RED):
        """Turning arrow about the centre c from point a to point b (same distance from c)."""
        assert (a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2 == (b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2
        self.arcs.append((c, a, b, cw, col))
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
        # lines of reflection: dashed, with their name outside the grid
        for kind, m in self.mirrors:
            p, q = self._mline(kind, m)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                     % (p[0], p[1], q[0], q[1], MIRROR))
            if kind == "v":
                t = "x = %d" % m
                w = tw(t, 14, True)
                cx, base = ox + m * u, oy - ny * u - 10
                box = (cx - w / 2, base - 11, cx + w / 2, base + 1)
                assert box[0] > ox + 6, ("line name on the y label", m)
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
        for c, a, b, cw, col in self.arcs:
            cc, p, q = self.P(*c), self.P(*a), self.P(*b)
            r = math.hypot(p[0] - cc[0], p[1] - cc[1])
            d = 1 if cw else -1                       # screen y is down: clockwise = growing angle
            ang2 = math.atan2(q[1] - cc[1], q[0] - cc[0]) - d * 15.0 / r
            ang0 = math.atan2(p[1] - cc[1], p[0] - cc[0]) + d * 7.0 / r
            e = (cc[0] + r * math.cos(ang2), cc[1] + r * math.sin(ang2))
            start = (cc[0] + r * math.cos(ang0), cc[1] + r * math.sin(ang0))
            sweep_ang = (d * (ang2 - ang0)) % (2 * math.pi)
            large = 1 if sweep_ang > math.pi else 0
            s.append("<path d='M%.1f,%.1f A%.1f,%.1f 0 %d %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (start[0], start[1], r, r, large, 1 if cw else 0, e[0], e[1], col))
            v = (e[0] - cc[0], e[1] - cc[1])
            t = (-v[1] / r, v[0] / r) if cw else (v[1] / r, -v[0] / r)
            tip = (e[0] + t[0] * 9, e[1] + t[1] * 9)
            n = (-t[1], t[0])
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (tip[0], tip[1], e[0] + n[0] * 5, e[1] + n[1] * 5, e[0] - n[0] * 5, e[1] - n[1] * 5, col))
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
    """Grid just big enough for the points and the line (smaller grids print larger)."""
    xs = [p[0] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "v" else [])
    ys = [p[1] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "h" else [])
    G = Grid(min(10, max(lo, max(xs) + extra)), min(10, max(lo, max(ys) + extra)))
    if mirror:
        G.mirror(*mirror)
    return G


def pts_grid(pts, label, ref=None, lo=6):
    G = grid_for([p[:2] for p in pts], lo=lo)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


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
        parts.append("%s %s" % (units(abs(dx)), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%s %s" % (units(abs(dy)), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def move_cands(p, dx, dy, i=0):
    """Where students land by mistake: wrong way, x and y moves mixed up, only one number changed."""
    x, y = p
    c = [(x - dx, y + dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (x + dx, y - dy), (x - dx, y - dy)]
    c = c[i % 3:] + c[:i % 3]
    c += [(x + dx + sgn(dx), y + dy + sgn(dy)), (y + dy, x + dx)]
    return [q for q in c if inside(q) and q != (x + dx, y + dy) and q != (x, y)]


def describe_cands(dx, dy, i=0):
    """Wrong descriptions: numbers swapped, wrong direction, counted the lines (1 too many)."""
    out = [mv(dx - sgn(dx), dy - sgn(dy))]
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
        s += "Across: %d to %d is %s %s. " % (a[0], b[0], units(abs(dx)), "right" if dx > 0 else "left")
    else:
        s += "The x-coordinate stays %d, so there is no move left or right. " % a[0]
    if dy:
        s += "Up and down: %d to %d is %s %s. " % (a[1], b[1], units(abs(dy)), "up" if dy > 0 else "down")
    else:
        s += "The y-coordinate stays %d, so there is no move up or down. " % a[1]
    return s + "Count the jumps, not the point you start on."


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %d changes x: %d %s %d = %d" % (
            "Right" if dx > 0 else "Left", abs(dx), x, "+" if dx > 0 else "−", abs(dx), q[0]))
    else:
        parts.append("x stays %d" % x)
    if dy:
        parts.append("%s %d changes y: %d %s %d = %d" % (
            "Up" if dy > 0 else "Down", abs(dy), y, "+" if dy > 0 else "−", abs(dy), q[1]))
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
    return ("the vertical line x = %d" if line[0] == "v" else "the horizontal line y = %d") % line[1]


def refl_e(p, line, name="The point"):
    k, m = line
    r = reflect(p, line)
    if r == p:
        return "%s %s is on the line of reflection %s, so it does not move: %s." % (name, pair(*p), lname(line), pair(*r))
    if k == "v":
        d = p[0] - m
        side, other = ("left", "right") if d < 0 else ("right", "left")
        return ("%s %s is %s to the %s of the line %s. The image is %s to the %s of it: %d %s %d = %d. "
                "y stays %d. The image is %s." % (name, pair(*p), units(abs(d)), side, lname(line), units(abs(d)), other,
                                                  m, "+" if d < 0 else "−", abs(d), r[0], p[1], pair(*r)))
    d = p[1] - m
    side, other = ("below", "above") if d < 0 else ("above", "below")
    return ("%s %s is %s %s the line %s. The image is %s %s it: %d %s %d = %d. "
            "x stays %d. The image is %s." % (name, pair(*p), units(abs(d)), side, lname(line), units(abs(d)), other,
                                              m, "+" if d < 0 else "−", abs(d), r[1], p[0], pair(*r)))


def refl_kinds(p, line):
    """Mistakes for reflecting a point: (point, why, key)."""
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
    out = [(far, "it is 1 unit too far from the line", "far"),
           (stop, "it stops on the line of reflection", "stop"),
           (short, "it is 1 unit too close to the line (the line was counted as the first jump)", "short"),
           (wrong, why_w, "wrong"),
           ((r[1], r[0]), "x and y are swapped", "swap")]
    return [(q, w, k) for q, w, k in out if inside(q) and q != r and q != p]


# ------------------------------------------------------------ A-D panels (small grids with shapes)
def poly_el(pts, col, cs, ox, oy, rows):
    P = lambda p: (ox + p[0] * cs, oy + (rows - p[1]) * cs)
    return ("<polygon points='%s' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % P(p) for p in pts), col, col))


def panel_el(cols, rows, shape, image, cs, ox, oy, line=None, centre=None):
    el = []
    for c in range(1, cols):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox + c * cs, oy, ox + c * cs, oy + rows * cs, THIN))
    for r in range(1, rows):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox, oy + r * cs, ox + cols * cs, oy + r * cs, THIN))
    el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
              % (ox, oy, cols * cs, rows * cs, INK))
    el.append(poly_el(shape, GREEN, cs, ox, oy, rows))
    el.append(poly_el(image, BLUE, cs, ox, oy, rows))
    if line:
        o = 6
        if line[0] == "v":
            x = ox + line[1] * cs
            seg = (x, oy - o, x, oy + rows * cs + o)
        else:
            y = oy + (rows - line[1]) * cs
            seg = (ox - o, y, ox + cols * cs + o, y)
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                  % (seg + (MIRROR,)))
    if centre:
        el.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (ox + centre[0] * cs, oy + (rows - centre[1]) * cs, RED))
    return el


def panel_svg(cols, rows, shape, images, cs, label, line=None, centre=None):
    LW, gap, pad, o = 22, 16, 8, 7
    gw, gh = cols * cs, rows * cs
    W = 2 * pad + 2 * (LW + gw + 2 * o) + gap
    H = 2 * pad + 2 * (gh + 2 * o) + gap
    el = []
    for k, img in enumerate(images):
        cx, cy = k % 2, k // 2
        x0 = pad + cx * (LW + gw + 2 * o + gap)
        y0 = pad + cy * (gh + 2 * o + gap)
        el += panel_el(cols, rows, shape, img, cs, x0 + LW + o, y0 + o, line, centre)
        el.append(text(x0, y0 + o + 16, "ABCD"[k], 18, anchor="start", bold=True))
    if W == H:
        W += 1
    return svg_wrap(W, H, "".join(el), label)


def same(a, b):
    return set(a) == set(b)


def panel_pick(cands, pos, rnd):
    """cands: {'ok': pts, key: pts, ...}. Returns the keys in A-D order and the answer letter."""
    vals = list(cands.values())
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            assert not same(vals[i], vals[j]), "two pictures are the same"
    p = pos.next()
    w = [k for k in cands if k != "ok"]
    rnd.shuffle(w)
    return w[:p] + ["ok"] + w[p:], "ABCD"[p]

# ------------------------------------------------------------ rotations about a vertex
TURNS = {"cw": "90° clockwise", "ccw": "90° counterclockwise", "half": "180°"}
WAYS = {"cw": "right turns into down, down into left, left into up and up into right",
        "ccw": "right turns into up, up into left, left into down and down into right",
        "half": "right turns into left, left into right, up into down and down into up"}


def rot(p, c, kind):
    dx, dy = p[0] - c[0], p[1] - c[1]
    r = {"cw": (dy, -dx), "ccw": (-dy, dx), "half": (-dx, -dy)}[kind]
    return (c[0] + r[0], c[1] + r[1])


def rel(dx, dy):
    a = "" if dx == 0 else ("%d right" % dx if dx > 0 else "%d left" % -dx)
    b = "" if dy == 0 else ("%d up" % dy if dy > 0 else "%d down" % -dy)
    return " and ".join(t for t in (a, b) if t)


def rot_e(p, c, kind, pn="The point", cn="the centre"):
    r = rot(p, c, kind)
    return ("From %s %s, %s %s is %s. In a %s turn, %s. So from %s, the image is %s: %s."
            % (cn, pair(*c), pn[0].lower() + pn[1:] if pn.startswith(("The", "Vertex")) else pn, pair(*p),
               rel(p[0] - c[0], p[1] - c[1]), TURNS[kind], WAYS[kind], pair(*c), rel(r[0] - c[0], r[1] - c[1]), pair(*r)))


def rot_kinds(p, c, kind):
    """Mistakes for a rotation: (point, why)."""
    dx, dy = p[0] - c[0], p[1] - c[1]
    out = []
    if kind == "half":
        out += [(rot(p, c, "cw"), "a 90° turn clockwise, not 180°"), (rot(p, c, "ccw"), "a 90° turn counterclockwise, not 180°")]
    else:
        other = "ccw" if kind == "cw" else "cw"
        out += [(rot(p, c, other), "turned the wrong way (%s)" % TURNS[other]), (rot(p, c, "half"), "a 180° turn, not 90°")]
    out += [((c[0] + dy, c[1] + dx), "the numbers were swapped, but the directions were not turned"),
            ((c[0] - dx, c[1] + dy), "a flip left to right, not a turn"),
            ((c[0] + dx, c[1] - dy), "a flip upside down, not a turn")]
    r = rot(p, c, kind)
    if dx == 0 or dy == 0:
        out.append(((r[0] + sgn(r[0] - c[0]), r[1] + sgn(r[1] - c[1])), "1 unit too far"))
    res, seen = [], set()
    for q, w in out:
        if inside(q) and q != r and q != p and q != c and q not in seen:
            seen.add(q)
            res.append((q, w))
    return res

# ------------------------------------------------------------ set 5: which transformation? and word problems
def classify(A, B):
    """Every way (translation, reflection in a vertical or horizontal line, rotation about a grid point) A maps onto B."""
    SB = set(B)
    out = set()
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            if set(shift(A, dx, dy)) == SB:
                out.add("a translation")
    for m2 in range(0, 21):
        if {(m2 - x, y) for x, y in A} == SB or {(x, m2 - y) for x, y in A} == SB:
            out.add("a reflection")
    for cx2 in range(-20, 41):                    # centres on grid points and halfway between them
        for cy2 in range(-20, 41):
            for k in TURNS:
                if {rot(p, (cx2 / 2.0, cy2 / 2.0), k) for p in A} == SB:
                    out.add("a rotation")
    return out

# ------------------------------------------------------------ lesson
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
        assert sum(need) == len(free), (s["title"], cnt, len(free))
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


# ------------------------------------------------------------ slides
def jumps(dx, dy):
    parts = []
    if dx:
        parts.append("%d jump%s %s" % (abs(dx), "" if abs(dx) == 1 else "s", "right" if dx > 0 else "left"))
    if dy:
        parts.append("%d jump%s %s" % (abs(dy), "" if abs(dy) == 1 else "s", "up" if dy > 0 else "down"))
    return " and ".join(parts)


def slide_kinds(p, dx, dy):
    """Mistakes for sliding a point: (point, why, key)."""
    x, y = p
    out = [((x + dx - sgn(dx), y + dy - sgn(dy)), "1 unit short (the starting point was counted as 1)", "short"),
           ((x + dx + sgn(dx), y + dy + sgn(dy)), "1 unit too far", "far")]
    if dx and dy:
        out += [((x - dx, y + dy), "it went %s, not %s" % ("left" if dx > 0 else "right", "right" if dx > 0 else "left"), "wayx"),
                ((x + dx, y - dy), "it went %s, not %s" % ("down" if dy > 0 else "up", "up" if dy > 0 else "down"), "wayy"),
                ((x + dy, y + dx), "the two moves were mixed up", "swap"),
                ((x + dx, y), "only the move %s was made" % ("right" if dx > 0 else "left"), "one")]
    elif dx:
        out += [((x - dx, y), "it went the wrong way", "way"), ((x, y + abs(dx)), "it went up, not across", "turn")]
    else:
        out += [((x, y - dy), "it went the wrong way", "way"), ((x + abs(dy), y), "it went right, not %s" % ("up" if dy > 0 else "down"), "turn")]
    q = (x + dx, y + dy)
    return [(c, w, k) for c, w, k in out if inside(c) and c != q and c != p]


def flip_x(pts):
    """Mirror image left to right, in the same place."""
    c = min(p[0] for p in pts) + max(p[0] for p in pts)
    return [(c - x, y) for x, y in pts]


def flip_y(pts):
    c = min(p[1] for p in pts) + max(p[1] for p in pts)
    return [(x, c - y) for x, y in pts]


OPS = {"id": lambda x, y: (x, y), "cw": lambda x, y: (y, -x), "ccw": lambda x, y: (-y, x), "half": lambda x, y: (-x, -y),
       "fx": lambda x, y: (-x, y), "fy": lambda x, y: (x, -y), "d1": lambda x, y: (y, x), "d2": lambda x, y: (-y, -x)}
KIND = {"id": "slide", "cw": "turn", "ccw": "turn", "half": "turn", "fx": "flip", "fy": "flip", "d1": "flip", "d2": "flip"}


def norm(S):
    mx, my = min(p[0] for p in S), min(p[1] for p in S)
    return frozenset((x - mx, y - my) for x, y in S)


# ============================================================ Grade 6: steps and combinations
def T(p, st):
    k = st[0]
    if k == "t":
        return (p[0] + st[1], p[1] + st[2])
    if k == "ref":
        return reflect(p, st[1])
    if k == "rot":
        return rot(p, st[1], st[2])
    raise ValueError(st)


def run(p, steps):
    for st in steps:
        p = T(p, st)
    return p


def runs(pts, steps):
    return [run(p, steps) for p in pts]


def sverb(st):
    k = st[0]
    if k == "t":
        return "translate %s" % mv_long(st[1], st[2])
    if k == "ref":
        return "reflect in the line %s" % lname(st[1])
    return "rotate %s about %s" % (TURNS[st[2]], pair(*st[1]))


def combo_text(steps):
    s = ", then ".join(sverb(st) for st in steps)
    return s[0].upper() + s[1:]


def step_e(p, st):
    k = st[0]
    if k == "t":
        return move_e(p, st[1], st[2])
    if k == "ref":
        return refl_e(p, st[1])
    return rot_e(p, st[1], st[2])


def steps_e(p, steps):
    out = []
    for i, st in enumerate(steps):
        out.append("Step %d (%s): %s" % (i + 1, sverb(st), step_e(p, st)))
        p = T(p, st)
    return " ".join(out)


def other_line(line):
    return ("h" if line[0] == "v" else "v", line[1])


def mistake(st):
    """The step done with a typical mistake, and why."""
    k = st[0]
    if k == "t":
        return ("t", -st[1], -st[2]), "the translation went the wrong way"
    if k == "ref":
        o = other_line(st[1])
        return ("ref", o), "it was reflected in the line %s instead of %s" % (lname(o), lname(st[1]))
    if st[2] == "half":
        return ("rot", st[1], "cw"), "it was turned only 90°, not 180°"
    o = "ccw" if st[2] == "cw" else "cw"
    return ("rot", st[1], o), "it was turned the wrong way (%s)" % TURNS[o]


def ref_short(p, line):
    """Counted the line of reflection as a jump: the image is 1 unit too close to the line."""
    r = reflect(p, line)
    k, m = line
    if k == "v":
        return (r[0] - sgn(r[0] - m), r[1])
    return (r[0], r[1] - sgn(r[1] - m))


def combo_kinds(p, steps):
    """Where students land by mistake in a two-step move: (point, why)."""
    r = run(p, steps)
    out = [(run(p, list(reversed(steps))), "the steps were done in the wrong order"),
           (run(p, steps[:1]), "only the first step was done")]
    m2, w2 = mistake(steps[1])
    out.append((run(p, [steps[0], m2]), "in step 2, " + w2))
    m1, w1 = mistake(steps[0])
    out.append((run(p, [m1, steps[1]]), "in step 1, " + w1))
    for i, st in enumerate(steps):
        if st[0] == "ref":
            q = run(p, steps[:i])
            q = ref_short(q, st[1])
            q = run(q, steps[i + 1:])
            out.append((q, "the line of reflection was counted as a jump"))
    for i, st in enumerate(steps):
        q = run(p, steps[:i])
        if st[0] == "rot":
            c = st[1]
            q = (c[0] + (q[1] - c[1]), c[1] + (q[0] - c[0]))
            why = "the numbers were swapped in the turn, but the directions were not turned"
        elif st[0] == "t" and st[1] and st[2] and abs(st[1]) != abs(st[2]):
            q = T(q, ("t", sgn(st[1]) * abs(st[2]), sgn(st[2]) * abs(st[1])))
            why = "the two amounts in the translation were mixed up"
        else:
            continue
        out.append((run(q, steps[i + 1:]), why))
    res, seen = [], set()
    for q, w in out:
        if inside(q) and q != r and q != p and q not in seen:
            seen.add(q)
            res.append((q, w))
    return res


def tcands(p, dx, dy, i=0):
    """move_cands plus the slide mistakes (1 short, 1 too far, turned the move)."""
    return move_cands(p, dx, dy, i) + [q for q, w, k in slide_kinds(p, dx, dy)]


def describe_moves(dx, dy):
    """Wrong descriptions of a translation: 1 short, numbers swapped, wrong way, 1 too far."""
    out = [(dx - sgn(dx), dy - sgn(dy))]
    if dx and dy and abs(dx) != abs(dy):
        out.append((sgn(dx) * abs(dy), sgn(dy) * abs(dx)))
    out += [(-dx, dy), (dx, -dy), (dx + sgn(dx), dy + sgn(dy)), (-dx, -dy)]
    if not dx:
        out += [(dy, 0), (-dy, 0)]
    if not dy:
        out += [(0, dx), (0, -dx)]
    return [mv_long(a, b) for a, b in out if (a, b) != (0, 0) and (a, b) != (dx, dy)]


def grid_pick_q(p, r, kinds, pos, ask, steps_expl, mirror=None, centre=None, label="coordinate grid with point P and points A to D"):
    """Grid with P (red), maybe a centre R or a line, and points A-D. kinds: [(point, why)]."""
    K = kinds[:3]
    assert len(K) == 3, (p, kinds)
    pts, ans = pick_letters(r, [q for q, w in K], pos)
    where = {(t[0], t[1]): t[2] for t in pts}
    extra = [p] + ([centre] if centre else [])
    G = grid_for(extra + [t[:2] for t in pts], lo=7, mirror=mirror)
    G.point(p[0], p[1], "P", RED)
    if centre:
        G.point(centre[0], centre[1], "R", INK)
    for t in pts:
        G.point(*t)
    e = steps_expl + " That is point %s. " % ans + " ".join("Point %s: %s." % (where[q], w if w.startswith("x ") else w[0].upper() + w[1:]) for q, w in K)
    return mcq_fixed(fig(G.svg(label)) + ask, LETTERS, ans, e)


def two_shapes(A, B, label, centre=None, at=None, lines=None):
    G = Grid(10, 10)
    for ln in lines or []:
        G.mirror(*ln)
    G.poly(A, GREEN, "A", at[0] if at else None).poly(B, BLUE, "B", at[1] if at else None)
    if centre:
        G.point(centre[0], centre[1], None, RED)
    return G.svg(label)


def pts_or(pts_list):
    return [plist(v) for v in pts_list if all(inside(q) for q in v)]


# ------------------------------------------------------------ set 1: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    data = [((2, 5), 4, 3), ((7, 6), -5, 0), ((3, 8), 0, -6), ((1, 2), 6, 5), ((8, 7), -3, -4), ((4, 1), 5, 7), ((9, 4), -7, 2)]
    for i, (p, dx, dy) in enumerate(data):
        r = (p[0] + dx, p[1] + dy)
        assert inside(r)
        its.append(mcq("Translate the point %s %s. What are the coordinates of the image?" % (pair(*p), mv_long(dx, dy)),
                       pair(*r), [pair(*q) for q in tcands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    n, he, his = P.next()
    its.append(mcq("A rectangle has a vertex at %s. %s translates the rectangle 2 units left and 5 units down. Where is the image of that vertex?"
                   % (pair(8, 9), n), pair(6, 4), [pair(*q) for q in tcands((8, 9), -2, -5, 1)], move_e((8, 9), -2, -5), rnd))
    for p, dx, dy in [((2, 6), 5, -3), ((6, 2), -3, 5), ((1, 1), 6, 4)]:
        r = (p[0] + dx, p[1] + dy)
        K = [(q, w) for q, w, k in slide_kinds(p, dx, dy) if k in ("short", "wayx", "wayy", "swap", "way", "turn", "far")]
        its.append(grid_pick_q(p, r, K, pos, "Point P is translated %s. Which point is its image?" % mv_long(dx, dy),
                               "P is at %s. %s" % (pair(*p), move_e(p, dx, dy))))
    for a, b in [((2, 3), (7, 5)), ((9, 8), (4, 2)), ((3, 9), (3, 2))]:
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv_long(dx, dy), describe_moves(dx, dy), describe_e(a, b, "The start", "the image"), rnd))
    A = [(1, 5), (4, 5), (1, 7)]
    B = shift(A, 5, -4)
    its.append(mcq(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B")) +
                   "Triangle B is a translation of triangle A. Describe the translation.",
                   mv_long(5, -4), describe_moves(5, -4),
                   "Follow one vertex: the right angle at (1, 5) moves to (6, 1). Across: 1 to 6 is 5 units right. "
                   "Up and down: 5 to 1 is 4 units down. Every vertex moves the same way.", rnd))
    tri = [(2, 1), (5, 1), (2, 4)]
    img = shift(tri, 3, 5)
    its.append(mcq("Triangle KLM has vertices K %s, L %s and M %s. It is translated %s. What are the vertices of the image?"
                   % (pair(*tri[0]), pair(*tri[1]), pair(*tri[2]), mv_long(3, 5)), plist(img),
                   pts_or([shift(tri, 5, 3), shift(tri, 2, 4), shift(tri, 4, 6), shift(tri, -3, 5)]),
                   "Add 3 to every x and 5 to every y. K: %s. L: %s. M: %s." % (pair(*img[0]), pair(*img[1]), pair(*img[2])), rnd))
    its.append(mcq("After a translation %s, the image of point A is %s. Where was point A before the move?" % (mv_long(3, 2), pair(6, 5)),
                   pair(3, 3), [pair(9, 7), pair(3, 7), pair(9, 3)],
                   "Undo the move: go 3 units left and 2 units down. x: 6 − 3 = 3. y: 5 − 2 = 3. A was at (3, 3). "
                   "Check: 3 right and 2 up from (3, 3) is (6, 5).", rnd))
    its.append(mcq("A translation moves %s to %s. Where does the same translation move %s?" % (pair(1, 2), pair(5, 3), pair(3, 6)),
                   pair(7, 7), [pair(8, 9), pair(4, 10), pair(7, 6)],
                   "First find the move: from (1, 2) to (5, 3) is 4 units right and 1 unit up. Do the same move to (3, 6): "
                   "x: 3 + 4 = 7, y: 6 + 1 = 7. The image is (7, 7).", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s translates %s 4 units up and gets %s. What mistake did %s make?" % (n, pair(5, 2), pair(9, 2), he),
                   "%s changed x instead of y" % H,
                   ["%s moved down instead of up" % H, "%s counted the start point as one" % H, "No mistake. %s is right" % H],
                   "Up changes only y: 2 + 4 = 6, so the image is (5, 6). %s added 4 to x, which moves the point right." % n, rnd))
    its.append(mcq("After a translation, what is true about the image of a shape?", "It is the same size and faces the same way",
                   ["It is a mirror image of the shape", "It is turned a quarter turn", "It is bigger than the shape"],
                   "A translation only slides the shape. Its size, its angles and the way it faces stay the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations on a grid", "items": its}


# ------------------------------------------------------------ set 2: reflections
WRONG_LINE_WHY = {"v": "it was flipped up or down, not across the line", "h": "it was flipped across, not over the horizontal line"}


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, line in [((2, 4), ("v", 5)), ((7, 3), ("v", 4)), ((3, 1), ("h", 4)), ((6, 9), ("h", 6)),
                    ((1, 6), ("v", 3)), ((8, 2), ("h", 5)), ((9, 7), ("v", 7))]:
        r = reflect(p, line)
        assert inside(r)
        its.append(mcq("Reflect the point %s in the line %s. What are the coordinates of the image?" % (pair(*p), lname(line)),
                       pair(*r), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line), rnd))
    for p, line in [((2, 3), ("v", 5)), ((6, 8), ("h", 5)), ((3, 2), ("h", 4))]:
        r = reflect(p, line)
        K = refl_kinds(p, line)
        order = {"short": 0, "wrong": 1, "swap": 2, "stop": 3, "far": 4}
        K = sorted(K, key=lambda t: order[t[2]])
        its.append(grid_pick_q(p, r, [(q, w) for q, w, k in K], pos,
                               "Point P is reflected in the line %s. Which point is its image?" % lname(line),
                               refl_e(p, line, "P"), mirror=line,
                               label="coordinate grid with point P, a line of reflection and points A to D"))
    for tri, line in [([(1, 2), (3, 2), (1, 5)], ("v", 4)), ([(6, 6), (9, 6), (9, 8)], ("h", 5))]:
        img = [reflect(p, line) for p in tri]
        if line[0] == "v":
            slid = shift(tri, 2 * line[1] - min(p[0] for p in tri) - max(p[0] for p in tri), 0)
        else:
            slid = shift(tri, 0, 2 * line[1] - min(p[1] for p in tri) - max(p[1] for p in tri))
        short = [ref_short(p, line) for p in tri]
        wrong = [reflect(p, other_line(line)) for p in tri]
        for v in (slid, short, wrong):
            assert not same(v, img)
        its.append(mcq("A triangle has vertices %s. It is reflected in the line %s. What are the vertices of the image?" % (plist(tri), lname(line)),
                       plist(img), pts_or([slid, short, wrong]),
                       "Reflect each vertex: it stays the same distance from %s, on the other side. %s → %s. "
                       "The image is a mirror image, so the triangle faces the other way." % (lname(line), plist(tri), plist(img)), rnd))
    for A, line, ch in [([(1, 1), (3, 1), (1, 4)], ("v", 5), ["x = 4", "x = 5", "x = 6", "y = 5"]),
                        ([(2, 7), (5, 7), (5, 10)], ("h", 6), ["y = 5", "y = 6", "y = 7", "x = 6"])]:
        B = [reflect(p, line) for p in A]
        a, b = A[1], B[1]
        if line[0] == "v":
            e = ("Match a vertex with its image: %s and %s. The line is halfway between them: (%d + %d) ÷ 2 = %d. "
                 "Each is %s from x = %d." % (pair(*a), pair(*b), a[0], b[0], line[1], units(abs(a[0] - line[1])), line[1]))
        else:
            e = ("Match a vertex with its image: %s and %s. The line is halfway between them: (%d + %d) ÷ 2 = %d. "
                 "Each is %s from y = %d." % (pair(*a), pair(*b), a[1], b[1], line[1], units(abs(a[1] - line[1])), line[1]))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its reflection B")) +
                             "Triangle B is the reflection of triangle A. What is the line of reflection?", ch, lname(line), e))
    its.append(mcq_fixed("The points %s and %s are reflections of each other. What is the line of reflection?" % (pair(2, 3), pair(8, 3)),
                         ["x = 3", "x = 5", "x = 6", "y = 3"], "x = 5",
                         "y stays 3, so the line is vertical. It is halfway between x = 2 and x = 8: (2 + 8) ÷ 2 = 5. "
                         "Both points are 3 units from x = 5. (x = 6 is the distance between them, not the halfway point.)"))
    its.append(mcq_fixed("The points %s and %s are reflections of each other. What is the line of reflection?" % (pair(4, 1), pair(4, 7)),
                         ["y = 3", "y = 4", "y = 6", "x = 4"], "y = 4",
                         "x stays 4, so the line is horizontal. It is halfway between y = 1 and y = 7: (1 + 7) ÷ 2 = 4. "
                         "Both points are 3 units from y = 4."))
    its.append(mcq("Reflect the point %s in the line x = 5. What are the coordinates of the image?" % pair(5, 7), pair(5, 7),
                   [pair(6, 7), pair(5, 3), pair(7, 5)], refl_e((5, 7), ("v", 5)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s in the line x = 5 and gets %s. What mistake did %s make?" % (n, pair(2, 6), pair(7, 6), he),
                   "%s counted the line as a jump" % H,
                   ["%s reflected in a horizontal line" % H, "%s went the wrong way" % H, "No mistake. %s is right" % H],
                   "(2, 6) is 3 units left of x = 5, so the image is 3 units right of it: 5 + 3 = 8. The image is (8, 6). "
                   "%s counted the line itself as the first jump and stopped 1 unit short." % n, rnd))
    its.append(mcq("Point Q is the reflection of point P in the line y = 3. Q is at %s. Where is P?" % pair(6, 1), pair(6, 5),
                   [pair(6, 4), pair(6, 6), pair(0, 1)],
                   "Q is 2 units below y = 3. P is the same distance above the line: 3 + 2 = 5. P is at (6, 5).", rnd))
    its.append(mcq("In a reflection, how far is each point of the image from the line of reflection?",
                   "the same distance as the point, on the other side",
                   ["twice as far as the point", "1 unit farther than the point", "always 1 unit away"],
                   "A line of reflection works like a mirror. Each image point is the same distance from the line as the "
                   "point it came from, but on the other side.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in a vertical or horizontal line", "items": its}


# ------------------------------------------------------------ set 3: rotations about a point
DIRW = {"cw": "Right turned into down (and up into right): that is 90° clockwise.",
        "ccw": "Up turned into left (and right into up): that is 90° counterclockwise.",
        "half": "Right turned into left and up turned into down: that is a half turn, 180°."}


def set_rotate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, c, kind in [((6, 5), (4, 4), "cw"), ((3, 7), (3, 4), "cw"), ((7, 2), (5, 3), "ccw"), ((2, 5), (4, 4), "ccw"),
                       ((8, 5), (6, 4), "half"), ((1, 4), (3, 3), "half"), ((5, 8), (5, 5), "ccw")]:
        r = rot(p, c, kind)
        assert inside(r)
        its.append(mcq("Rotate the point %s %s about the point %s. What are the coordinates of the image?" % (pair(*p), TURNS[kind], pair(*c)),
                       pair(*r), [pair(*q) for q, w in rot_kinds(p, c, kind)], rot_e(p, c, kind), rnd))
    for p, c, kind in [((6, 7), (4, 4), "cw"), ((2, 6), (5, 4), "ccw"), ((2, 3), (4, 4), "half")]:
        r = rot(p, c, kind)
        its.append(grid_pick_q(p, r, rot_kinds(p, c, kind), pos,
                               "Point P is rotated %s about point R. Which point is its image?" % TURNS[kind],
                               rot_e(p, c, kind, "P", "R"), centre=c,
                               label="coordinate grid with point P, centre R and points A to D"))
    for p, c, r in [((5, 5), (5, 2), (2, 2)), ((5, 4), (3, 3), (1, 2))]:
        kind = [k for k in TURNS if rot(p, c, k) == r]
        assert len(kind) == 1
        kind = kind[0]
        its.append(mcq_fixed("A shape is rotated about its vertex %s. Another vertex moves from %s to %s. Describe the rotation."
                             % (pair(*c), pair(*p), pair(*r)), ROTS, TURNS[kind],
                             "%s is %s from the centre. %s is %s from the centre. %s" % (
                                 pair(*p), rel(p[0] - c[0], p[1] - c[1]), pair(*r), rel(r[0] - c[0], r[1] - c[1]), DIRW[kind])))
    for A, c, kind, at in [([(4, 4), (7, 4), (7, 6)], (4, 4), "cw", None),
                           ([(5, 5), (8, 5), (5, 7)], (5, 5), "ccw", None)]:
        B = [rot(p, c, kind) for p in A]
        assert not any(same([rot(p, c, k) for p in A], B) for k in TURNS if k != kind)
        q = A[1]
        e = ("The red vertex %s stays still, so it is the centre. Follow the long side: from the centre it goes %s in A and %s in B. %s"
             % (pair(*c), rel(sgn(q[0] - c[0]), sgn(q[1] - c[1])).replace("1 ", ""),
                rel(sgn(rot(q, c, kind)[0] - c[0]), sgn(rot(q, c, kind)[1] - c[1])).replace("1 ", ""), DIRW[kind]))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its rotation B about a red vertex", centre=c, at=at)) +
                             "Triangle A is rotated about the red vertex to make triangle B. Describe the rotation.", ROTS, TURNS[kind], e))
    tri, c = [(4, 4), (7, 4), (4, 6)], (4, 4)
    img = [rot(p, c, "half") for p in tri]
    its.append(mcq("A triangle has vertices %s. It is rotated 180° about the vertex %s. What are the vertices of the image?" % (plist(tri), pair(*c)),
                   plist(img), pts_or([[rot(p, c, "cw") for p in tri], [rot(p, c, "ccw") for p in tri], [(2 * c[0] - p[0], p[1]) for p in tri]]),
                   "The centre (4, 4) does not move. In a half turn, right turns into left and up turns into down. "
                   "(7, 4) is 3 right, so its image is 3 left: (1, 4). (4, 6) is 2 up, so its image is 2 down: (4, 2).", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    p, c = (7, 3), (4, 3)
    its.append(mcq("%s rotates the point %s 90° clockwise about %s and gets %s. What mistake did %s make?"
                   % (n, pair(*p), pair(*c), pair(*rot(p, c, "ccw")), he),
                   "%s turned it counterclockwise" % H,
                   ["%s turned it 180°" % H, "%s reflected it instead" % H, "No mistake. %s is right" % H],
                   "%s is a quarter turn counterclockwise. %s" % (pair(*rot(p, c, "ccw")), rot_e(p, c, "cw")), rnd))
    p, c = (6, 4), (4, 4)
    r = rot(p, c, "ccw")
    its.append(mcq("Point %s is rotated 270° clockwise about %s. Where does it land?" % (pair(*p), pair(*c)), pair(*r),
                   [pair(*q) for q, w in rot_kinds(p, c, "ccw")],
                   "270° clockwise is three quarter turns clockwise. That ends in the same place as one quarter turn counterclockwise "
                   "(360° − 270° = 90°). " + rot_e(p, c, "ccw"), rnd))
    its.append(mcq_fixed("A shape is rotated 90° clockwise about a point, then 90° clockwise again about the same point. "
                         "Which single rotation gives the same image?", ROTS, "180°",
                         "Two quarter turns the same way make a half turn: 90° + 90° = 180°."))
    its.append(mcq("A rectangle has vertices K (4, 5), L (7, 5), M (7, 7) and N (4, 7). It is rotated 90° clockwise about vertex K. "
                   "Where does vertex M land?", pair(*rot((7, 7), (4, 5), "cw")),
                   [pair(*q) for q, w in rot_kinds((7, 7), (4, 5), "cw")], rot_e((7, 7), (4, 5), "cw", "Vertex M", "vertex K"), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    p, c = (7, 5), (4, 4)
    sw = (c[0] + (p[1] - c[1]), c[1] + (p[0] - c[0]))
    assert sw == (5, 7)
    its.append(mcq("%s rotates %s 90° clockwise about %s and gets %s. What mistake did %s make?" % (n, pair(*p), pair(*c), pair(*sw), he),
                   "%s swapped the numbers but did not turn the directions" % H,
                   ["%s turned it 180°" % H, "%s counted the centre as a jump" % H, "No mistake. %s is right" % H],
                   "From (4, 4), the point is 3 right and 1 up. %s just swapped them to 1 right and 3 up. In a clockwise quarter turn, "
                   "right turns into down and up turns into right: 3 down and 1 right, so the image is %s." % (n, pair(*rot(p, c, "cw"))), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rotations of 90° and 180° about a point", "items": its}


# ------------------------------------------------------------ set 4: two transformations in a row
def set_combine(rnd, P):
    its = []
    pos = Pos(rnd)
    data = [((2, 1), [("t", 0, 3), ("ref", ("h", 5))]),
            ((7, 6), [("t", -4, 0), ("ref", ("v", 4))]),
            ((3, 8), [("ref", ("h", 6)), ("t", 4, -1)]),
            ((1, 3), [("ref", ("v", 3)), ("t", 2, 4)]),
            ((2, 2), [("t", 3, 1), ("rot", (5, 5), "cw")]),
            ((6, 2), [("rot", (4, 4), "half"), ("t", 3, 2)]),
            ((7, 5), [("rot", (5, 5), "ccw"), ("t", -2, -3)]),
            ((1, 6), [("ref", ("v", 3)), ("ref", ("v", 6))]),
            ((3, 2), [("t", 2, 3), ("ref", ("v", 7))]),
            ((8, 3), [("ref", ("h", 4)), ("rot", (6, 6), "cw")]),
            ((9, 8), [("t", -3, -2), ("rot", (3, 3), "ccw")])]
    for p, steps in data:
        r = run(p, steps)
        assert inside(r) and inside(run(p, steps[:1])), (p, steps)
        assert r != run(p, list(reversed(steps))), (p, steps)
        its.append(mcq("Point %s: %s. Where is the final image?" % (pair(*p), combo_text(steps)[0].lower() + combo_text(steps)[1:]),
                       pair(*r), [pair(*q) for q, w in combo_kinds(p, steps)], "Do the steps in order. " + steps_e(p, steps), rnd))
    for p, steps in [((1, 7), [("t", 4, -1), ("ref", ("h", 4))]), ((1, 2), [("t", 1, 3), ("ref", ("v", 4))])]:
        r = run(p, steps)
        K = combo_kinds(p, steps)
        its.append(grid_pick_q(p, r, K, pos,
                               "Point P is translated %s, then reflected in the line %s. Which point is the final image?"
                               % (mv_long(steps[0][1], steps[0][2]), lname(steps[1][1])),
                               steps_e(p, steps), mirror=steps[1][1],
                               label="coordinate grid with point P, a line of reflection and points A to D"))
    for tri, steps in [([(1, 1), (3, 1), (1, 3)], [("t", 2, 4), ("ref", ("v", 5))]),
                       ([(5, 6), (7, 6), (7, 8)], [("rot", (5, 6), "half"), ("t", 3, 0)])]:
        img = runs(tri, steps)
        alts = [runs(tri, list(reversed(steps))), runs(tri, steps[:1]),
                runs(tri, [steps[0], mistake(steps[1])[0]]), runs(tri, [mistake(steps[0])[0], steps[1]])]
        if steps[0][0] == "t":
            alts.append(runs(tri, [("t", steps[0][2], steps[0][1]), steps[1]]))
        for v in alts:
            assert not same(v, img)
        its.append(mcq("A triangle has vertices %s. It is %s. What are the vertices of the final image?"
                       % (plist(tri), " then ".join(["%s," % ("translated " + mv_long(st[1], st[2]) if st[0] == "t" else
                                                               "reflected in the line " + lname(st[1]) if st[0] == "ref" else
                                                               "rotated %s about %s" % (TURNS[st[2]], pair(*st[1]))) for st in steps])[:-1]),
                       plist(img), pts_or(alts),
                       "Step 1: %s. Step 2: %s. Do step 1 to every vertex first, then step 2." % (
                           plist(runs(tri, steps[:1])), plist(img)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    p, steps = (3, 2), [("t", 0, 2), ("ref", ("h", 5))]
    wrong = run(p, list(reversed(steps)))
    assert run(p, steps) == (3, 6) and wrong == (3, 10)
    its.append(mcq("%s must translate %s 2 units up, then reflect it in the line y = 5. %s gets %s. What mistake did %s make?"
                   % (n, pair(*p), H, pair(*wrong), he),
                   "%s reflected first, then translated" % H,
                   ["%s reflected in the line x = 5" % H, "%s translated down instead of up" % H, "No mistake. %s is right" % H],
                   "Right order: %s %s reflected (3, 2) to (3, 8) first, then moved up to (3, 10). The order of the steps matters."
                   % (steps_e(p, steps), n), rnd))
    end = (4, 5)
    start = (5, 5)
    assert run(start, [("t", 3, 0), ("ref", ("v", 6))]) == end
    its.append(mcq("A point is translated 3 units right, then reflected in the line x = 6. The final image is %s. Where did the point start?"
                   % pair(*end), pair(*start), [pair(8, 5), pair(1, 5), pair(7, 5)],
                   "Work backwards: undo the last step first. Undo the reflection: (4, 5) is 2 units left of x = 6, so it came from (8, 5). "
                   "Undo the translation: go 3 units left, 8 − 3 = 5. The point started at (5, 5). Check: (5, 5) → (8, 5) → (4, 5).", rnd))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    p = (2, 2)
    s1, s2 = [("t", 0, 1), ("ref", ("h", 5))], [("ref", ("h", 5)), ("t", 0, 1)]
    r1, r2 = run(p, s1), run(p, s2)
    assert r1 == (2, 7) and r2 == (2, 9)
    its.append(mcq("%s translates %s 1 unit up, then reflects it in the line y = 5. %s reflects %s in the line y = 5 first, then translates it "
                   "1 unit up. What do they get?" % (n1, pair(*p), n2, pair(*p)),
                   "%s: %s, %s: %s" % (n1, pair(*r1), n2, pair(*r2)),
                   ["Both get %s" % pair(*r1), "Both get %s" % pair(*r2), "%s: %s, %s: %s" % (n1, pair(*r2), n2, pair(*r1))],
                   "%s: (2, 2) → (2, 3) → (2, 7). %s: (2, 2) → (2, 8) → (2, 9). The order of the steps changes the answer." % (n1, n2), rnd))
    its.append(mcq("A point is translated 3 units right and 4 units up, then 4 units right and 1 unit down. Which single translation gives the same image?",
                   mv_long(7, 3), [mv_long(7, 5), mv_long(1, 3), mv_long(3, 4)],
                   "Add the moves. Across: 3 right + 4 right = 7 right. Up and down: 4 up and 1 down leaves 3 up. "
                   "The single translation is 7 units right and 3 units up.", rnd))
    its.append(mcq("A shape is rotated 180° about a point, then rotated 180° again about the same point. Where does it end up?",
                   "back where it started", ["a quarter turn from the start", "upside down from the start", "a mirror image of the start"],
                   "180° + 180° = 360°, a full turn. A full turn about the same point brings every vertex back to where it started.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Two transformations in a row", "items": its}


# ------------------------------------------------------------ set 5: which combination? word problems
KINDS4 = ["a translation", "a reflection", "a rotation", "two transformations are needed"]


def set_which(rnd, P):
    its = []
    for A, steps, wrongs, at in [
        ([(1, 1), (3, 1), (1, 4)], [("ref", ("v", 4)), ("t", 0, 4)],
         [[("t", 0, 4), ("ref", ("h", 4))], [("ref", ("v", 4)), ("t", 0, -4)], [("ref", ("v", 5)), ("t", 0, 4)]], None),
        ([(1, 6), (4, 6), (4, 8)], [("rot", (4, 6), "cw"), ("t", 2, -1)],
         [[("rot", (4, 6), "ccw"), ("t", 2, -1)], [("rot", (4, 6), "half"), ("t", 2, -1)], [("rot", (4, 6), "cw"), ("t", -2, 1)]], None),
        ([(2, 7), (5, 7), (2, 9)], [("ref", ("h", 6)), ("t", 4, 0)],
         [[("ref", ("h", 6)), ("t", -4, 0)], [("ref", ("v", 6)), ("t", 4, 0)], [("ref", ("h", 7)), ("t", 4, 0)]], None),
    ]:
        B = runs(A, steps)
        assert all(inside(q) for q in B)
        for w in wrongs:
            assert not same(runs(A, w), B), w
        v = [q for q in A if all(st[0] != "rot" or st[1] != q for st in steps)][0]
        e = ("Test the steps on one vertex. " + steps_e(v, steps) + " The other vertices work the same way, so the steps map A onto B.")
        its.append(mcq(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B", at=at)) +
                       "Which steps map triangle A onto triangle B?", combo_text(steps), [combo_text(w) for w in wrongs], e, rnd))
    A = [(1, 2), (3, 2), (3, 5)]
    steps = [("t", 2, 1), ("ref", ("v", 5))]
    B = runs(A, steps)
    wrongs = [[("ref", ("v", 5)), ("t", 2, 1)], [("t", 2, 1), ("ref", ("h", 5))], [("t", 1, 2), ("ref", ("v", 5))]]
    for w in wrongs:
        assert not same(runs(A, w), B), w
    its.append(mcq("Triangle PQR has vertices %s. Its image has vertices %s, in the same order. Which steps map the triangle onto its image?"
                   % (plist(A), plist(B)), combo_text(steps), [combo_text(w) for w in wrongs],
                   "Test the steps on one vertex. " + steps_e(A[0], steps) + " The other vertices work the same way.", rnd))
    for A, B, ans, e in [
        ([(1, 2), (4, 2), (1, 4)], runs([(1, 2), (4, 2), (1, 4)], [("ref", ("v", 5)), ("t", 0, 4)]), KINDS4[3],
         "B is a mirror image of A, so it was reflected. But B is also higher up: a reflection in a vertical line keeps every y the same. "
         "So two steps are needed: reflect in x = 5, then translate 4 units up."),
        ([(1, 1), (4, 1), (4, 3)], [rot(p, (5, 4), "half") for p in [(1, 1), (4, 1), (4, 3)]], KINDS4[2],
         "B is A upside down and back to front. That is a half turn (180°), here about the point (5, 4). One rotation is enough."),
    ]:
        cl = classify(A, B)
        assert (ans == KINDS4[3] and not cl) or cl == {ans}, (cl, ans)
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B")) +
                             "What is the fewest number of transformations that maps triangle A onto triangle B?", KINDS4, ans, e))
    # word problems in BC contexts
    p = (1, 2)
    its.append(mcq("A BC Ferries route is drawn on a grid map. A ferry leaves a terminal at %s and sails %s. Where does it arrive?"
                   % (pair(*p), mv_long(6, 5)), pair(7, 7), [pair(*q) for q in tcands(p, 6, 5, 2)], move_e(p, 6, 5), rnd))
    n, he, his = P.next()
    its.append(mcq("On a whale-watching trip near Victoria, %s marks an orca on a grid map at %s. Later the orca is at %s. "
                   "Describe the orca’s move as a translation." % (n, pair(8, 3), pair(2, 7)),
                   mv_long(-6, 4), describe_moves(-6, 4), describe_e((8, 3), (2, 7), "The first spot", "the second spot"), rnd))
    n, he, his = P.next()
    p, line = (4, 9), ("h", 5)
    its.append(mcq("%s draws a mountain beside a calm lake. The shoreline is the line y = 5 and the peak is at %s. "
                   "%s draws the mountain’s reflection in the water. Where is the peak of the reflection?" % (n, pair(*p), he.capitalize()),
                   pair(*reflect(p, line)), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line, "The peak"), rnd))
    n, he, his = P.next()
    p, steps = (2, 6), [("ref", ("v", 5)), ("t", 0, -2)]
    its.append(mcq("%s designs a logo for %s school’s lacrosse team in Kamloops. One corner of the left half is at %s. %s reflects it in the line "
                   "x = 5 to make the right half, then translates the whole logo 2 units down. Where is the image of that corner?"
                   % (n, his, pair(*p), he.capitalize()), pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)],
                   steps_e(p, steps), rnd))
    n, he, his = P.next()
    p, c = (5, 8), (5, 5)
    its.append(mcq("%s makes a quilt square for a class display. The centre of the square is at %s. A triangle piece has a vertex at %s. "
                   "%s rotates the piece 90° clockwise about the centre to place the next piece. Where is that vertex now?"
                   % (n, pair(*c), pair(*p), he.capitalize()), pair(*rot(p, c, "cw")),
                   [pair(*q) for q, w in rot_kinds(p, c, "cw")], rot_e(p, c, "cw", "The vertex"), rnd))
    n, he, his = P.next()
    p, c = (7, 9), (5, 5)
    its.append(mcq("%s draws a pinwheel for a Terry Fox Run poster. The pin is at %s and one blade tip is at %s. The opposite blade is the first "
                   "one rotated 180° about the pin. Where is its tip?" % (n, pair(*c), pair(*p)), pair(*rot(p, c, "half")),
                   [pair(*q) for q, w in rot_kinds(p, c, "half")], rot_e(p, c, "half", "The tip", "the pin"), rnd))
    n, he, his = P.next()
    p, steps = (1, 8), [("t", 4, -5), ("ref", ("v", 6))]
    its.append(mcq("In a snowboarding video game, %s’s rider is at %s on the screen grid. The rider jumps %s, then the screen is flipped "
                   "in the line x = 6. Where is the rider now?" % (n, pair(*p), mv_long(4, -5)),
                   pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)], steps_e(p, steps), rnd))
    n, he, his = P.next()
    p, steps = (6, 3), [("rot", (4, 4), "ccw"), ("t", 3, 0)]
    its.append(mcq("In a coding app, %s’s sprite is at %s. %s rotates it 90° counterclockwise about %s, then translates it 3 units right. "
                   "Where does it end up?" % (n, pair(*p), he.capitalize(), pair(4, 4)),
                   pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)], steps_e(p, steps), rnd))
    n, he, his = P.next()
    a = (1, 3)
    assert run(a, [("t", 5, 2), ("t", 3, -1)]) == (9, 4)
    its.append(mcq("%s plans a bike ride on a grid map of Stanley Park. From %s, %s rides %s, then %s. Which single translation "
                   "takes %s from the start to the end?" % (n, pair(*a), he, mv_long(5, 2), mv_long(3, -1), "her" if he == "she" else "him"),
                   mv_long(8, 1), [mv_long(8, 3), mv_long(2, 1), mv_long(5, 2)],
                   "Add the moves. Across: 5 right + 3 right = 8 right. Up and down: 2 up and 1 down leaves 1 up. "
                   "Check: (1, 3) → (9, 4).", rnd))
    p, steps = (2, 4), [("t", 2, 0), ("ref", ("v", 5))]
    its.append(mcq("A soccer coach in Surrey draws a play on a grid. The halfway line is x = 5. A player at %s runs 2 units right. "
                   "Then the coach copies the play to the other half by reflecting it in the halfway line. Where is the player’s image?" % pair(*p),
                   pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)], steps_e(p, steps), rnd))
    n, he, his = P.next()
    end, start = (3, 3), (3, 5)
    assert run(start, [("t", 0, 2), ("ref", ("h", 5))]) == end
    its.append(mcq("In a board game, %s’s piece was translated 2 units up, then reflected in the line y = 5. It ended at %s. Where did it start?"
                   % (n, pair(*end)), pair(*start), [pair(3, 7), pair(3, 9), pair(3, 1)],
                   "Undo the steps in reverse order. Undo the reflection: (3, 3) is 2 units below y = 5, so it came from (3, 7). "
                   "Undo the translation: go 2 units down, 7 − 2 = 5. The piece started at (3, 5). Check: (3, 5) → (3, 7) → (3, 3).", rnd))
    n, he, his = P.next()
    p, steps = (4, 7), [("rot", (4, 4), "cw"), ("t", 3, 0)]
    its.append(mcq("%s designs a tile pattern for a school mural in Burnaby. %s rotates a triangle 90° clockwise about its vertex %s, "
                   "then translates it 3 units right. Another vertex starts at %s. Where does it end up?" % (n, he.capitalize(), pair(4, 4), pair(*p)),
                   pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)], steps_e(p, steps), rnd))
    n, he, his = P.next()
    p = (2, 4)
    right = [("rot", (4, 4), "half"), ("t", 0, 3)]
    kai = list(reversed(right))
    assert run(p, right) == (6, 7) and run(p, kai) == (6, 1)
    its.append(mcq("In a coding club, %s’s robot is at %s. It must turn 180° about %s, then move 3 units up. %s moves it up first, "
                   "then turns it. Where does %s robot end up?" % (n, pair(*p), pair(4, 4), n, his),
                   pair(6, 1), [pair(6, 7), pair(2, 7), pair(6, 4)],
                   "%s did the steps in the wrong order. Up 3: (2, 4) → (2, 7). Then the half turn about (4, 4): (2, 7) is 2 left and 3 up, "
                   "so the image is 2 right and 3 down: (6, 1). In the right order the robot would be at (6, 7)." % n, rnd))
    n, he, his = P.next()
    p, steps = (3, 8), [("ref", ("v", 5)), ("ref", ("h", 5))]
    its.append(mcq("%s makes a paper snowflake design. A point at %s is reflected in the line x = 5, then the image is reflected in the line y = 5. "
                   "Where is the final point?" % (n, pair(*p)), pair(*run(p, steps)), [pair(*q) for q, w in combo_kinds(p, steps)] + [pair(3, 2)],
                   steps_e(p, steps) + " Two reflections in lines that cross at (5, 5) give the same image as a 180° rotation about (5, 5).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Which steps? Transformation word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    G = Grid(10, 8)
    A = [(1, 5), (3, 5), (1, 7)]
    G.poly(A, GREEN, "A").poly(shift(A, 5, -4), BLUE, "B")
    G.arrow((3, 5), (8, 5)).arrow((8, 5), (8, 1))
    G.note(5.5, 5.5, "5 right").note(8.2, 3, "4 down", anchor="start")
    trans = G.svg("triangle A translated 5 units right and 4 units down to triangle B")
    G = Grid(10, 6)
    G.mirror("v", 5)
    Tr = [(1, 1), (4, 1), (1, 4)]
    G.poly(Tr, GREEN, "A").poly([reflect(p, ("v", 5)) for p in Tr], BLUE, "B")
    refl = G.svg("triangle A reflected in the line x = 5 to make triangle B")
    G = Grid(8, 8)
    Tr = [(2, 5), (5, 5), (5, 7)]
    G.poly(Tr, GREEN, "A").poly([rot(p, (2, 5), "cw") for p in Tr], BLUE, "B", (2.6, 2.7))
    G.arc((2, 5), (5, 5), (2, 2), True)
    G.point(2, 5, None, RED)
    rota = G.svg("triangle A rotated 90° clockwise about its vertex (2, 5) to make triangle B")
    G = Grid(10, 9)
    G.mirror("v", 6)
    A = [(1, 6), (3, 6), (1, 8)]
    B = shift(A, 2, -4)
    C = [reflect(p, ("v", 6)) for p in B]
    assert C == [(9, 2), (7, 2), (9, 4)]
    G.poly(A, GREEN, "A").poly(B, BLUE, "B").poly(C, RED, "C")
    G.arrow((1, 6), (3, 6), INK).arrow((3, 6), (3, 2), INK)
    comb = G.svg("triangle A translated 2 units right and 4 units down to B, then B reflected in the line x = 6 to C")
    return (
        "<h2>Three transformations</h2>"
        "<p>A <b>transformation</b> moves a shape on a grid. The shape keeps its size and its angles. "
        "The new shape is the <b>image</b>. In Grade 6 you use three kinds, and you can do two of them in a row.</p>" +
        table(["Transformation", "What it does", "What you need to know"], [
            ["Translation (slide)", "moves every point the same way", "how far right or left, and up or down"],
            ["Reflection (flip)", "makes a mirror image", "the line of reflection, like x = 5"],
            ["Rotation (turn)", "turns the shape about a point", "the centre, the angle (90° or 180°) and the direction"],
        ]) +
        "<h2>Translations</h2>"
        "<p>Right adds to x and left subtracts from x. Up adds to y and down subtracts from y. Count the jumps, not the point you start on.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A moves 5 units right and 4 units down. The vertex (3, 5) goes to (8, 1).</figcaption></figure>" +
        ex("Example", "Translate (2, 5) 4 units right and 3 units up.", "x: 2 + 4 = 6. y: 5 + 3 = 8.", "(6, 8)") +
        "<h2>Reflections</h2>"
        "<p>Each point of the image is the <b>same distance</b> from the line of reflection as the point it came from, on the other side. "
        "A vertical line x = 5 changes only x. A horizontal line y = 5 changes only y.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>(4, 1) is 1 unit left of x = 5, so its image is 1 unit right of it: (6, 1). (1, 4) is 4 units left, so its image is (9, 4).</figcaption></figure>" +
        ex("Example", "Reflect (2, 4) in the line x = 5.", "(2, 4) is 3 units left of the line. Go 3 units past it: 5 + 3 = 8. y stays 4.", "(8, 4)") +
        "<h2>Rotations about a point</h2>"
        "<p>The <b>centre of rotation</b> does not move. Find how far the point is from the centre (right or left, up or down), then turn those directions. "
        "<b>Clockwise</b> is the way clock hands move.</p>" +
        table(["Turn", "right becomes", "up becomes"], [
            ["90° clockwise", "down", "right"],
            ["90° counterclockwise", "up", "left"],
            ["180° (either way)", "left", "down"],
        ]) +
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A turns 90° clockwise about the red vertex (2, 5). The vertex 3 right of the centre ends up 3 down: (5, 5) → (2, 2).</figcaption></figure>" +
        ex("Example", "Rotate (6, 5) 90° clockwise about (4, 4).",
           "From (4, 4), the point is 2 right and 1 up. Turn clockwise: 2 right becomes 2 down, 1 up becomes 1 right. "
           "From (4, 4): 1 right and 2 down.", "(5, 2)") +
        "<h2>Two transformations in a row</h2>"
        "<p>Do the steps one at a time, <b>in the order given</b>. The image from step 1 is the starting shape for step 2. "
        "The order matters: doing the steps the other way round can give a different image.</p>"
        "<figure class='sn-fig'>" + comb +
        "<figcaption>Step 1: A is translated 2 units right and 4 units down to B. Step 2: B is reflected in the line x = 6 to C.</figcaption></figure>" +
        ex("Two steps", "Translate (3, 2) 2 units up, then reflect it in the line y = 5.",
           "Step 1: (3, 2) → (3, 4). Step 2: (3, 4) is 1 unit below y = 5, so the image is 1 unit above it: (3, 6). "
           "Reflecting first gives (3, 8), then (3, 10): a different point.", "(3, 6)") +
        ex("Work backwards", "A point is translated 3 units right, then reflected in x = 6. It ends at (4, 5). Where did it start?",
           "Undo the last step first. Undo the reflection: (4, 5) → (8, 5). Undo the translation: 3 units left, (8, 5) → (5, 5).", "(5, 5)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Doing the two steps in the wrong order", "Do step 1, then use its image for step 2"],
            ["Turning the wrong way", "Clockwise goes like clock hands: from 12 towards 3"],
            ["Swapping the numbers in a turn: 3 right, 1 up → 1 right, 3 up", "Turn the directions: clockwise gives 3 down, 1 right"],
            ["Counting the line of reflection as a jump", "Go the same distance past the line"],
            ["Reflecting in the wrong kind of line", "x = 5 is vertical (changes x); y = 5 is horizontal (changes y)"],
            ["Stopping after the first step", "Check that every step in the list is done"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about transformations in BC?",
     "a": "In the BC Grade 6 curriculum (Geometry and measurement), students perform and describe combinations of transformations: "
          "translations, reflections and rotations of shapes in the first quadrant of a grid, often two in a row."},
    {"q": "Does the order of two transformations matter?",
     "a": "Often it does. Translating 2 units up and then reflecting in y = 5 takes (3, 2) to (3, 6), but reflecting first takes it to (3, 10). "
          "Always do the steps in the order given."},
    {"q": "How do you rotate a point 90° about another point?",
     "a": "Find how far the point is from the centre, such as 3 right and 1 up. For 90° clockwise, right becomes down and up becomes right, "
          "so the image is 1 right and 3 down from the centre."},
    {"q": "How can you find the line of reflection between a shape and its image?",
     "a": "Match a vertex with its image. The line of reflection is halfway between them: for (2, 3) and (8, 3), it is x = (2 + 8) ÷ 2 = 5."},
]


def gen_unit():
    rnd = random.Random(56815)
    P = People(rnd)
    sets = [set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P), set_combine(rnd, P), set_which(rnd, P)]
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
            assert not re.search(r"\(-|, -", plain), plain       # first quadrant only
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "combinations-of-transformations", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Combinations of Transformations: Translate, Reflect and Rotate on a Grid",
        "seo_title": "Grade 6 Math: Combinations of Transformations Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Combinations of transformations",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 6: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Combinations of transformations",
        "meta_desc": "Free Grade 6 math worksheets on combinations of transformations for the BC curriculum: translate, reflect in a line and rotate 90° or 180° about a point in the first quadrant, do two transformations in a row and find the steps that map one shape onto another. 100 questions with an answer key.",
        "key_big": "Do the steps one at a time, in the order given. The image of step 1 is the start of step 2.",
        "key_sub": "Translation: right and up add, left and down subtract. Reflection: the image is the same distance from the line, on the other side. Rotation: the centre stays still; clockwise turns right into down and up into right.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "coordinate grid")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
