# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Single Transformations (slides, flips and turns)
(BC Mathematics Curriculum, Grade 5: Geometry and measurement, "single transformations")
  python3 tools/gen_cabc_math_g5_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10. Canadian English (counterclockwise, centre, colour).
Lines of reflection are vertical (x = m) or horizontal (y = m), drawn as a dashed purple line with their name.
Turns are quarter turns (90°) clockwise or counterclockwise and half turns (180°) about a vertex, so every
image stays in the first quadrant. Every grid is drawn exactly; letter labels never sit on a line, note or
other label (checked in Grid.render).
Wrong answers come from real Grade 5 mistakes: counting the start square or point as "one" (1 unit short),
counting the line of reflection as a jump, flipping instead of turning (and turning instead of flipping),
sliding instead of flipping, moving the wrong way, swapping x and y, turning the wrong way, mixing up
quarter and half turns.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
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


def looks(A, B):
    """What B looks like compared with A, ignoring where it is: a set of 'slide', 'turn', 'flip'.
    A shape that is both (for example a flip that is also a turn) is ambiguous for students."""
    return {KIND[k] for k, f in OPS.items() if norm([f(*p) for p in A]) == norm(B)}


def place(S, ok):
    """Move S so its corner sits where the corner of ok is."""
    return shift(S, min(p[0] for p in ok) - min(p[0] for p in S), min(p[1] for p in ok) - min(p[1] for p in S))


def half_turn(pts):
    """Half turn about the centre of the shape, in the same place."""
    return flip_x(flip_y(pts))


SLIDE_WHY = {"short": "1 unit short (the starting point was counted as 1)", "flip": "a flip (mirror image), not a slide",
             "turn": "a turn (the shape is upside down), not a slide", "far": "1 unit too far"}
SLIDE_PANELS = [
    (9, 4, [(0, 1), (3, 1), (3, 2), (1, 2), (1, 3), (0, 3)], 5, 0),
    (5, 7, [(1, 5), (4, 5), (4, 6), (2, 6), (2, 7), (1, 7)], 0, -4),
]


def slide_panel_q(cols, rows, A, dx, dy, pos, rnd):
    ok = shift(A, dx, dy)
    short = shift(A, dx - sgn(dx), dy - sgn(dy))
    cands = {"ok": ok, "short": short, "flip": flip_x(ok), "turn": half_turn(ok)}
    for k, v in cands.items():
        assert all(0 <= x <= cols and 0 <= y <= rows for x, y in v), k
        assert looks(A, v) == {"slide" if k in ("ok", "short") else k}, (k, looks(A, v))
    keys, ans = panel_pick(cands, pos, rnd)
    svg = panel_svg(cols, rows, A, [cands[k] for k in keys], 14, "four grid pictures A to D of a slide")
    others = "; ".join("%s: %s" % ("ABCD"[j], SLIDE_WHY[k]) for j, k in enumerate(keys) if k != "ok")
    e = ("In a slide the shape faces the same way, and every vertex moves %s. Only <b>%s</b> shows that. Others: %s."
         % (units(abs(dx or dy)) + " " + ("right" if dx > 0 else "left" if dx < 0 else "up" if dy > 0 else "down"), ans, others))
    return mcq_fixed(fig(svg) + "The green shape slides %s. In which picture is the blue image correct?" % mv_long(dx, dy),
                     LETTERS, ans, e)


# ------------------------------------------------------------ set 1: slides
def set_slide(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq("Which sentence is true about a slide (translation)?", "The shape faces the same way",
                   ["The shape becomes a mirror image", "The shape turns about a point", "The shape gets bigger"],
                   "A slide moves a shape left or right and up or down. It does not flip or turn, so the shape faces the same way and keeps its size.", rnd))
    its.append(mcq("A triangle slides 5 units left. Its top vertex moves 5 units left. How does its bottom-right vertex move?",
                   "5 units left", ["5 units right", "4 units left", "It does not move"],
                   "In a slide every vertex moves the same distance in the same direction. So every vertex moves 5 units left.", rnd))
    its.append(mcq("A square with sides of 4 cm slides 3 units up on grid paper. How long are its sides now?", "4 cm",
                   ["7 cm", "1 cm", "12 cm"],
                   "A slide only moves the square. It does not stretch it, so the sides are still 4 cm long.", rnd))
    # which point? (pictures)
    for i, (p, dx, dy, pick) in enumerate([((5, 4), 4, 0, ["short", "turn", "way"]), ((2, 5), 0, -3, ["short", "way", "turn"]),
                                           ((1, 2), 5, 3, ["short", "swap", "one"]), ((8, 2), -5, 4, ["short", "one", "far"])]):
        q = (p[0] + dx, p[1] + dy)
        K = {k: (c, w) for c, w, k in slide_kinds(p, dx, dy)}
        wrong = [K[k] for k in pick]
        pts, ans = pick_letters(q, [c for c, w in wrong], pos)
        where = {(c[0], c[1]): c[2] for c in pts}
        G = grid_for([p] + [c[:2] for c in pts], lo=7)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        e = ("From P, count %s. Count the jumps, not the point you start on. P lands on point %s. " % (jumps(dx, dy), ans) +
             " ".join("Point %s: %s." % (where[c], w) for c, w in wrong))
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P slides %s. Which point shows where it lands?" % mv_long(dx, dy), LETTERS, ans, e))
    # describe a slide from A to B
    for i, (a, b) in enumerate([((2, 3), (6, 3)), ((5, 7), (5, 2)), ((1, 1), (6, 4)), ((7, 6), (2, 2))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A slides to point B. Describe the slide.", mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    for cols, rows, A, dx, dy in SLIDE_PANELS:
        its.append(slide_panel_q(cols, rows, A, dx, dy, pos, rnd))
    shapes = [
        ([(1, 5), (4, 5), (1, 8)], 5, -4, None),
        ([(6, 5), (9, 5), (9, 6), (7, 6), (7, 8), (6, 8)], -5, -4, (6.5, 5.5)),
        ([(6, 1), (9, 1), (9, 3)], -5, 4, None),
    ]
    for i, (A, dx, dy, at) in enumerate(shapes):
        B = shift(A, dx, dy)
        G = Grid(10, 8)
        G.poly(A, GREEN, "A", at).poly(B, BLUE, "B", (at[0] + dx, at[1] + dy) if at else None)
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                       "Shape A slides to shape B. Describe the slide.", mv(dx, dy), describe_cands(dx, dy, i + 1),
                       "Follow one vertex. The vertex of A at %s moves to %s in B. That is %s. Every vertex moves the same way."
                       % (pair(*A[0]), pair(*B[0]), mv_long(dx, dy)), rnd))
    its.append(mcq("A point slides 3 units right, then 2 more units right. Describe this as one slide.", "5 units right",
                   ["3 units right and 2 units up", "1 unit right", "6 units right"],
                   "Both moves go right, so add them: 3 + 2 = 5. It is one slide of 5 units right.", rnd))
    its.append(mcq_num("A shape slides 6 units right. One vertex started 2 units from the left edge of the grid. How far from the left edge is it now?",
                       8, [6, 4, 7],
                       "Sliding right moves the vertex farther from the left edge: 2 + 6 = 8 units. "
                       "(7 comes from counting the starting point as 1.)", fmt="%d units"))
    n, he, his = P.next()
    its.append(mcq_num("%s slides a counter 5 units right. %s says “one” on the starting point and stops when %s says “five”. "
                       "How far did the counter really move?" % (n, he.capitalize(), he), 4, [5, 6, 3],
                       "Saying “one” on the starting point does not move the counter. Only 4 of the counts are jumps, so it moved 4 units: 1 unit short. "
                       "Count “one” on the first jump.", fmt="%d units"))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s slides a shape 4 units down, but %s image is 4 units above the shape. What mistake did %s make?" % (n, his, he),
                   "%s moved it the wrong way" % H,
                   ["%s counted the starting point" % H, "%s flipped it" % H, "No mistake. %s is right" % H],
                   "Down makes the shape lower on the grid. The image is higher, so %s moved it up instead of down. "
                   "The distance, 4 units, is right." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Slides (translations) on a grid", "items": its}


# ------------------------------------------------------------ set 2: flips
REFL_WHY = {"slide": "the shape was slid across, not flipped (it faces the same way)",
            "far": "the image is 1 unit too far from the line",
            "close": "the image is 1 unit too close to the line (the line was counted as the first jump)",
            "turn": "the shape was turned (it is upside down and back to front), not flipped",
            "wrong": "the shape was flipped the wrong way (%s), not over the dashed line"}
REFL_PANELS = [
    (("v", 4), 8, 6, [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)], ["slide", "close", "turn"]),
    (("h", 4), 7, 8, [(1, 5), (5, 5), (5, 6), (2, 6), (2, 7), (1, 7)], ["close", "turn", "wrong"]),
    (("v", 3), 7, 5, [(0, 1), (2, 1), (2, 2), (1, 2), (1, 4), (0, 4)], ["slide", "far", "turn"]),
]


def refl_panel_q(line, cols, rows, A, wrongs, pos, rnd):
    ok = [reflect(p, line) for p in A]
    xs, ys = [p[0] for p in A], [p[1] for p in A]
    if line[0] == "v":
        s = sgn(min(q[0] for q in ok) - line[1]) or 1
        slide = shift(A, min(q[0] for q in ok) - min(xs), 0)
        far, close = shift(ok, s, 0), shift(ok, -s, 0)
    else:
        s = sgn(min(q[1] for q in ok) - line[1]) or -1
        if max(q[1] for q in ok) <= line[1]:
            s = -1
        slide = shift(A, 0, min(q[1] for q in ok) - min(ys))
        far, close = shift(ok, 0, s), shift(ok, 0, -s)
    allc = {"ok": ok, "slide": slide, "far": far, "close": close, "turn": place(half_turn(A), ok),
            "wrong": place(flip_y(A) if line[0] == "v" else flip_x(A), ok)}
    assert classify(A, allc["turn"]) == {"a rotation"} and classify(A, allc["slide"]) == {"a translation"}
    cands = {k: allc[k] for k in ["ok"] + wrongs}
    for k, v in cands.items():
        assert all(0 <= x <= cols and 0 <= y <= rows for x, y in v), k
        assert looks(A, v) == {"slide" if k == "slide" else "turn" if k == "turn" else "flip"}, (k, looks(A, v))
    keys, ans = panel_pick(cands, pos, rnd)
    svg = panel_svg(cols, rows, A, [cands[k] for k in keys], 14, "four grid pictures A to D with a dashed line of reflection", line=line)
    why = dict(REFL_WHY, wrong=REFL_WHY["wrong"] % ("upside down" if line[0] == "v" else "left to right"))
    others = "; ".join("%s: %s" % ("ABCD"[j], why[k]) for j, k in enumerate(keys) if k != "ok")
    e = ("Each vertex of the image must be the same distance from the line as its partner, on the other side. "
         "Only <b>%s</b> is a true mirror image. Others: %s." % (ans, others))
    return mcq_fixed(fig(svg) + "The green shape is flipped (reflected) in the dashed line. In which picture is the blue image correct?",
                     LETTERS, ans, e)


def set_flip(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq("What does a flip (reflection) make?", "a mirror image of the shape",
                   ["a bigger copy of the shape", "the same shape, facing the same way", "a smaller copy of the shape"],
                   "A flip turns the shape over a line, like a mirror. The image faces the other way, but its size does not change.", rnd))
    its.append(mcq("Point P is 3 units to the left of a vertical line of reflection. Where is its image?", "3 units to the right of the line",
                   ["6 units to the right of the line", "3 units to the left of the line", "2 units to the right of the line"],
                   "In a flip the image is the same distance from the line as the point, on the other side. "
                   "(2 units comes from counting the line as the first jump.)", rnd))
    for p, line, pick in [((2, 3), ("v", 4), ["short", "wrong", "swap"]), ((8, 6), ("v", 5), ["short", "stop", "swap"]),
                          ((2, 1), ("h", 3), ["short", "swap", "wrong"]), ((5, 6), ("h", 4), ["short", "wrong", "swap"])]:
        r = reflect(p, line)
        K = {k: (q, w) for q, w, k in refl_kinds(p, line)}
        wrong = [K[j] for j in pick]
        pts, ans = pick_letters(r, [q for q, w in wrong], pos)
        where = {(c[0], c[1]): c[2] for c in pts}
        G = grid_for([p] + [c[:2] for c in pts], lo=7, mirror=line)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        e = (refl_e(p, line, "P") + " That is point %s. " % ans +
             " ".join("Point %s: %s." % (where[q], w) for q, w in wrong))
        its.append(mcq_fixed(fig(G.svg("coordinate grid with a line of reflection, point P and points A to D")) +
                             "Point P is flipped in the dashed line %s. Which point is its image?" % lname(line), LETTERS, ans, e))
    for line, cols, rows, A, wrongs in REFL_PANELS:
        its.append(refl_panel_q(line, cols, rows, A, wrongs, pos, rnd))
    for p, line in [((3, 4), ("v", 5)), ((6, 9), ("h", 6)), ((8, 2), ("v", 6))]:
        r = reflect(p, line)
        its.append(mcq("Reflect the point %s in %s. What are the coordinates of the image?" % (pair(*p), lword(line)),
                       pair(*r), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line), rnd))
    its.append(mcq("Reflect the point (5, 3) in the vertical line x = 5. What are the coordinates of the image?", "(5, 3)",
                   ["(6, 3)", "(3, 5)", "(4, 3)"],
                   refl_e((5, 3), ("v", 5)) + " A point on the line of reflection is its own image.", rnd))
    its.append(mcq_num("The point (4, 2) is reflected in the horizontal line y = 5. How many units apart are the point and its image?",
                       6, [3, 5, 7],
                       "(4, 2) is 3 units below y = 5, so the image (4, 8) is 3 units above it. From the point to the image is 3 + 3 = 6 units. "
                       "(3 is only the distance to the line.)", fmt="%d units"))
    its.append(mcq("The points (2, 6) and (8, 6) are reflections of each other. Where is the line of reflection?", "x = 5",
                   ["x = 6", "x = 4", "y = 6"],
                   "The line is halfway between the points. From 2 to 8 is 6 units, and half of 6 is 3. 2 + 3 = 5, so the line is x = 5. "
                   "(y = 6 goes through both points; it is not between them.)", rnd))
    checks = [
        (("h", 4), [(1, 1), (4, 1), (1, 3)], "ok"),
        (("v", 5), [(1, 1), (1, 5), (3, 1)], "close"),
        (("h", 4), [(2, 1), (6, 1), (2, 3)], "turn"),
    ]
    for line, A, kind in checks:
        ok = [reflect(p, line) for p in A]
        if kind == "ok":
            B, ans = ok, CHECK[0]
            e = "Check each vertex. %s Every vertex works the same way, so B is a correct mirror image." % refl_e(A[0], line, "The vertex")
        elif kind == "close":
            B, ans = shift(ok, -1, 0), CHECK[1]
            e = ("%s is %s from the line %s, so its image should be at %s. B has that vertex at %s: 1 unit too close. "
                 "The line was counted as the first jump." % (pair(*A[0]), units(abs(A[0][0] - line[1])), lname(line), pair(*ok[0]), pair(*B[0])))
        else:
            B, ans = place(half_turn(A), ok), CHECK[2]
            e = ("In A the right angle is at the bottom left. A flip over y = 4 would put it at the top left, at %s. "
                 "In B the right angle is at the top right: B is A turned upside down and back to front. That is a turn, not a flip." % pair(*ok[0]))
        assert classify(A, B) == ({"a rotation"} if kind == "turn" else {"a reflection"}), (kind, classify(A, B))
        assert looks(A, B) == ({"turn"} if kind == "turn" else {"flip"}), (kind, looks(A, B))
        G = Grid(10, 8)
        G.mirror(*line)
        G.poly(A, GREEN, "A").poly(B, BLUE, "B")
        n = P.next()[0]
        its.append(mcq_fixed(fig(G.svg("coordinate grid with a line of reflection, shape A and shape B")) +
                             "%s wants to flip shape A in the dashed line. Is shape B correct?" % n, CHECK, ans, e))
    n, he, his = P.next()
    its.append(mcq("%s flips a right triangle in a vertical line. %s image points the same way as the triangle. What mistake did %s make?"
                   % (n, his.capitalize(), he),
                   "%s slid it instead of flipping it" % he.capitalize(),
                   ["%s made it bigger" % he.capitalize(), "%s flipped it too far" % he.capitalize(), "No mistake. %s is right" % he.capitalize()],
                   "A flip makes a mirror image, so it faces the other way. If the image points the same way, the shape was slid (translated).", rnd))
    n, he, his = P.next()
    its.append(mcq("A point is 4 units from a line of reflection. %s counts “one” on the line and stops at “four”. How far from the line is %s image?"
                   % (n, his), "3 units, 1 unit too close", ["4 units, correct", "5 units, 1 unit too far", "8 units, too far"],
                   "Counting “one” on the line uses up a count without a jump. Only 3 jumps were made, so the image is 3 units from the line. "
                   "It should be 4 units away, the same as the point.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Flips (reflections) in a line", "items": its}


# ------------------------------------------------------------ set 3: turns
ROT_PANELS = [
    ((4, 4), "cw", 8, 8, [(4, 4), (7, 4), (7, 6)], ["ccw", "half", "flip"]),
    ((4, 4), "ccw", 8, 8, [(4, 4), (6, 4), (6, 5), (5, 5), (5, 7), (4, 7)], ["cw", "half", "flip"]),
    ((4, 4), "half", 8, 8, [(4, 4), (7, 4), (7, 5), (5, 5), (5, 6), (4, 6)], ["cw", "ccw", "flip"]),
    ((4, 4), "cw", 8, 8, [(4, 4), (4, 7), (5, 7), (6, 6), (5, 5), (5, 4)], ["ccw", "half", "flip"]),
]
ROT_WHY = {"cw": "a quarter turn clockwise", "ccw": "a quarter turn counterclockwise", "half": "a half turn (180°)",
           "flip": "a flip (mirror image), not a turn"}
TURN_WORDS = {"cw": "a quarter turn (90°) clockwise", "ccw": "a quarter turn (90°) counterclockwise", "half": "a half turn (180°)"}


def rot_panel_q(c, kind, cols, rows, A, wrongs, pos, rnd):
    allc = {"cw": [rot(p, c, "cw") for p in A], "ccw": [rot(p, c, "ccw") for p in A],
            "half": [rot(p, c, "half") for p in A], "flip": [(2 * c[0] - p[0], p[1]) for p in A]}
    cands = {"ok": allc[kind]}
    for k in wrongs:
        cands[k] = allc[k]
    for k, v in cands.items():
        assert all(0 <= x <= cols and 0 <= y <= rows for x, y in v), (k, v)
        assert not same(v, A), k
        assert looks(A, v) == {"flip" if k == "flip" else "turn"}, (k, looks(A, v))
    keys, ans = panel_pick(cands, pos, rnd)
    svg = panel_svg(cols, rows, A, [cands[k] for k in keys], 14, "four grid pictures A to D with a red centre of rotation", centre=c)
    others = "; ".join("%s: %s" % ("ABCD"[j], ROT_WHY[k]) for j, k in enumerate(keys) if k != "ok")
    long_side = [p for p in A if p != c and (p[0] == c[0] or p[1] == c[1])][0]
    r = rot(long_side, c, kind)
    e = ("The red dot does not move. Follow one side: the side from the red dot going %s turns to go %s in %s. "
         "Only <b>%s</b> shows that. Others: %s." % (
             rel(sgn(long_side[0] - c[0]), sgn(long_side[1] - c[1])).replace("1 ", ""),
             rel(sgn(r[0] - c[0]), sgn(r[1] - c[1])).replace("1 ", ""), TURN_WORDS[kind], ans, others))
    return mcq_fixed(fig(svg) + "The green shape is turned %s about the red dot. In which picture is the blue image correct?" % TURNS[kind],
                     LETTERS, ans, e)


def set_turn(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq_num("How many degrees is a quarter turn?", 90, [45, 180, 360],
                       "A full turn is 360°. A quarter turn is one of 4 equal parts: 360° ÷ 4 = 90°. A half turn is 180°.", fmt="%d°"))
    its.append(mcq("Which way do the hands of a clock turn?", "clockwise", ["counterclockwise", "up and down", "left and right"],
                   "Clock hands go from 12 to 3 to 6 to 9: that is clockwise. The other way is counterclockwise.", rnd))
    its.append(mcq("The minute hand of a clock moves from 12 to 3. What turn is that?", "a quarter turn clockwise",
                   ["a half turn clockwise", "a quarter turn counterclockwise", "a full turn"],
                   "From 12 to 3 is one quarter of the way around the clock, and clock hands move clockwise.", rnd))
    its.append(mcq("A triangle is turned about its vertex A. Which point stays in the same place?", "vertex A",
                   ["the vertex farthest from A", "every vertex", "no point"],
                   "The centre of rotation (the turn centre) does not move. Here it is vertex A; every other point turns around it.", rnd))
    its.append(mcq("A shape makes two quarter turns clockwise about the same point. What is that the same as?", "one half turn (180°)",
                   ["one quarter turn counterclockwise", "a full turn (360°)", "a flip"],
                   "Each quarter turn is 90°. 90° + 90° = 180°, which is a half turn.", rnd))
    its.append(mcq("A shape is turned 180° clockwise about a point. A copy of it is turned 180° counterclockwise about the same point. Where do they land?",
                   "in the same place", ["in different places", "one is a mirror image of the other", "one lands twice as far away"],
                   "A half turn is a half turn, whichever way you go. 180° clockwise and 180° counterclockwise end in the same place.", rnd))
    data = [
        ("Turn the point B (6, 4) 90° clockwise about the point A (3, 4). Where does B land?", (6, 4), (3, 4), "cw", "B", "A"),
        ("Turn the point Q (8, 5) 90° counterclockwise about the point P (5, 5). Where does Q land?", (8, 5), (5, 5), "ccw", "Q", "P"),
        ("A rectangle has vertices K (3, 3), L (5, 3), M (5, 6) and N (3, 6). It is turned 90° clockwise about vertex K. Where does vertex M land?",
         (5, 6), (3, 3), "cw", "Vertex M", "vertex K"),
        ("A triangle has vertices A (4, 4), B (1, 5) and C (4, 7). It is turned 180° about vertex A. Where does vertex B land?",
         (1, 5), (4, 4), "half", "Vertex B", "vertex A"),
    ]
    for q, p, c, kind, pn, cn in data:
        r = rot(p, c, kind)
        assert inside(r), (q, r)
        its.append(mcq(q, pair(*r), [pair(*x) for x, w in rot_kinds(p, c, kind)], rot_e(p, c, kind, pn, cn), rnd))
    for c, kind, cols, rows, A, wrongs in ROT_PANELS:
        its.append(rot_panel_q(c, kind, cols, rows, A, wrongs, pos, rnd))
    for p, c, kind in [((7, 5), (4, 3), "cw"), ((3, 7), (5, 4), "half")]:
        r = rot(p, c, kind)
        K = rot_kinds(p, c, kind)[:3]
        pts, ans = pick_letters(r, [q for q, w in K], pos)
        where = {(t[0], t[1]): t[2] for t in pts}
        G = grid_for([p, c] + [t[:2] for t in pts], lo=7)
        G.point(p[0], p[1], "P", RED).point(c[0], c[1], "R", INK)
        for t in pts:
            G.point(*t)
        e = rot_e(p, c, kind, "P", "R") + " That is point %s. " % ans + " ".join("Point %s: %s." % (where[q], w) for q, w in K)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P, centre R and points A to D")) +
                             "Point P is turned %s about point R. Which point is the image?" % TURNS[kind], LETTERS, ans, e))
    for p, c, r in [((6, 4), (4, 4), (4, 2)), ((5, 4), (3, 3), (1, 2))]:
        kind = [k for k in TURNS if rot(p, c, k) == r]
        assert len(kind) == 1
        kind = kind[0]
        its.append(mcq_fixed("A shape is turned about its vertex %s. Another vertex moves from %s to %s. Describe the turn."
                             % (pair(*c), pair(*p), pair(*r)), ROTS, TURNS[kind],
                             "%s is %s from the centre. %s is %s from the centre. %s" % (
                                 pair(*p), rel(p[0] - c[0], p[1] - c[1]), pair(*r), rel(r[0] - c[0], r[1] - c[1]),
                                 "Right turned into down: that is a quarter turn clockwise." if kind == "cw" else
                                 "Right turned into left and up turned into down: that is a half turn, 180°.")))
    n, he, his = P.next()
    H = he.capitalize()
    p, c = (7, 3), (4, 3)
    its.append(mcq("%s turns the point %s 90° clockwise about %s and gets %s. What mistake did %s make?"
                   % (n, pair(*p), pair(*c), pair(*rot(p, c, "ccw")), he),
                   "%s turned it counterclockwise" % H,
                   ["%s turned it 180°" % H, "%s swapped x and y" % H, "No mistake. %s is right" % H],
                   "%s is a quarter turn counterclockwise. %s" % (pair(*rot(p, c, "ccw")), rot_e(p, c, "cw")), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s turns an L-shape a half turn. %s image has the foot of the L still at the bottom, but pointing the other way. What mistake did %s make?"
                   % (n, his.capitalize(), he), "%s flipped it instead of turning it" % H,
                   ["%s turned it a quarter turn" % H, "%s slid it" % H, "No mistake. %s is right" % H],
                   "After a half turn the L is upside down, so the foot ends up at the top. A foot still at the bottom but pointing the other way is a mirror image: a flip.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Turns (rotations): quarter and half turns", "items": its}


# ------------------------------------------------------------ set 4: which transformation?
def set_which(rnd, P):
    its = []
    real = [
        ("SkyTrain moving along a straight piece of track", MOVES[0],
         "The train moves in a straight line and does not turn or flip, so it is a slide."),
        ("the mountains and their upside-down picture in a calm lake", MOVES[1],
         "The picture in the water is a mirror image, upside down over the shoreline. That is a flip."),
        ("a door swinging open on its hinges", MOVES[2],
         "The door turns about the hinges. The hinges stay still, like a turn centre. That is a turn."),
        ("pushing a box straight across the gym floor", MOVES[0],
         "The box moves across without turning or flipping, so it is a slide."),
        ("the hands of a clock moving from 12 to 6", MOVES[2],
         "The hands turn about the centre of the clock. That is a half turn."),
        ("your hand and its image in a mirror", MOVES[1],
         "A mirror image faces the other way: a right hand looks like a left hand. That is a flip."),
    ]
    for thing, ans, e in real:
        its.append(mcq("Which transformation is most like %s?" % thing, ans, [m for m in MOVES if m != ans], e, rnd))
    Lr = [(1, 5), (5, 5), (5, 6), (2, 6), (2, 8), (1, 8)]
    Lh = [(1, 1), (5, 1), (5, 2), (2, 2), (2, 4), (1, 4)]
    T = [(2, 5), (6, 5), (2, 7)]
    Ls = [(1, 5), (3, 5), (3, 6), (2, 6), (2, 8), (1, 8)]
    F = [(1, 2), (2, 2), (2, 4), (5, 4), (5, 5), (1, 5)]
    Q = [(2, 1), (6, 1), (5, 3), (2, 3)]
    R = [(1, 1), (4, 1), (1, 3)]
    cases = [
        ([(1, 1), (4, 1), (1, 3)], [(6, 4), (9, 4), (6, 6)], None,
         "B faces the same way as A and is the same size. Every vertex moved 5 units right and 3 units up, for example (1, 1) → (6, 4). That is a slide."),
        ([(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)], [reflect(p, ("v", 5)) for p in [(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)]],
         ((1.5, 2.5), (8.5, 2.5)),
         "B is a mirror image of A: the foot of the L points the other way, but it is still at the bottom. It is a flip in the line x = 5."),
        (Lr, shift([rot(p, (0, 0), "cw") for p in Lr], 1, 6), ((3, 5.5), (6.5, 2.5)),
         "In A the long arm of the L lies flat along the bottom. In B it stands straight up. A slide or a flip cannot make a flat arm "
         "stand up, but a turn can: B is A turned a quarter turn (90°) clockwise."),
        (Ls, shift(Ls, 5, -4), ((1.5, 5.5), (6.5, 1.5)),
         "B looks exactly like A and faces the same way. Every vertex moved 5 units right and 4 units down. That is a slide."),
        (T, [reflect(p, ("h", 4)) for p in T], None,
         "In A the right angle is at the bottom left; in B it is at the top left. B is A flipped over the line y = 4: "
         "each vertex is the same distance from the line on the other side. That is a flip."),
        (Lh, [rot(p, (5, 2), "half") for p in Lh], ((1.5, 2.5), (8.5, 1.5)),
         "B is A upside down and back to front: a half turn (180°) about the vertex (5, 2). A flip would change only one of these."),
        (F, shift([rot(p, (0, 0), "ccw") for p in F], 11, 0), ((1.5, 3.5), (6.5, 3)),
         "Follow the top edge of A, from (1, 5) to (5, 5): it goes across. In B the same edge goes up and down, from (6, 1) to (6, 5). "
         "A slide or a flip cannot do that, but a turn can: B is A turned a quarter turn (90°) counterclockwise."),
        (Q, [reflect(p, ("h", 4)) for p in Q], None,
         "In A the long side is at the bottom; in B it is at the top, and the square corners are still on the left. "
         "That is a mirror image over the line y = 4: a flip. A half turn would also move the square corners to the right."),
        (R, [rot(p, (5, 3), "half") for p in R], None,
         "In A the right angle is at the bottom left. In B it is at the top right: upside down and back to front. "
         "That is a half turn. A flip would change only one of these."),
        ([(1, 4), (5, 4), (5, 6), (1, 6)], [(7, 1), (9, 1), (9, 2), (7, 2)], None,
         "A is 4 units by 2 units. B is only 2 units by 1 unit, so B is smaller. A slide, a flip or a turn never changes the size."),
    ]
    for A, B, at, e in cases:
        cl = classify(A, B)
        ans = NAME[cl.pop()] if cl else MOVES[3]
        assert not cl, (A, B)
        if ans == MOVES[3]:
            assert len(A) == len(B)
        else:
            assert looks(A, B) == {{MOVES[0]: "slide", MOVES[1]: "flip", MOVES[2]: "turn"}[ans]}, (ans, looks(A, B))
        assert all(inside(p) for p in A + B)
        G = Grid(10, 9 if max(p[1] for p in A + B) > 8 else 8)
        G.poly(A, GREEN, "A", at[0] if at else None).poly(B, BLUE, "B", at[1] if at else None)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) +
                             "What happened to shape A to make shape B?", MOVES, ans, e))
    its.append(mcq("In which transformation does one point always stay still?", "a turn (rotation)",
                   ["a slide (translation)", "a flip (reflection)", "none of them"],
                   "In a turn the centre of rotation does not move. In a slide every point moves. "
                   "In a flip only points on the line stay still, and a shape does not have to touch the line.", rnd))
    its.append(mcq("After which transformation does the shape always face the same way?", "a slide (translation)",
                   ["a flip (reflection)", "a turn (rotation)", "all three"],
                   "A slide only moves the shape. A flip makes a mirror image, and a turn changes the way it points.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s sees an L-shape and its image. The image is upside down and back to front. %s says it is a flip. Is %s right?" % (n, H, he),
                   "No. It is a half turn", ["Yes. It is a flip", "No. It is a slide", "No. It changed size"],
                   "A flip changes only one thing: left to right, or up to down. Upside down and back to front together is a half turn (180°).", rnd))
    n, he, his = P.next()
    its.append(mcq("Shape B is a mirror image of shape A. How could you check?", "Fold the paper along a line and see if they match",
                   ["Spin the paper around once", "Measure only one side", "Count the vertices"],
                   "A flip line works like a fold. If A lands exactly on B when you fold the paper, B is a flip of A.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Which transformation? Slide, flip or turn", "items": its}


# ------------------------------------------------------------ set 5: coordinates and word problems
def walk(x, y):
    a = "do not move across" if x == 0 else "go right %d" % x
    b = "do not move up" if y == 0 else "go up %d" % y
    return "Start at the origin (0, 0), %s, then %s" % (a, b)


def read_cands(x, y, i=0):
    c = [(y, x), (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (y + 1, x)]
    first, rest = c[:1], c[1:]
    rest = rest[i % 4:] + rest[:i % 4]
    return [pair(*q) for q in first + rest if inside(q) and q != (x, y)]


def set_coords(rnd, P):
    its = []
    pos = Pos(rnd)
    for i, pts in enumerate([[(3, 5, "A")], [(6, 2, "B"), (2, 6, "C")], [(0, 4, "G")]]):
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. The x-coordinate (across) is written first." % (walk(x, y), n, pair(x, y))
        if len(pts) > 1:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        if x == 0:
            e += " A point on the y-axis has x-coordinate 0."
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y, i), e, rnd))
    for (x, y), others in [((4, 2), [(2, 4), (5, 3), (4, 3)]), ((1, 6), [(6, 1), (2, 7), (1, 5)])]:
        pts, ans = pick_letters((x, y), others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s. Point %s is at %s: the numbers are swapped." % (walk(x, y), ans, where[(y, x)], pair(y, x))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    its.append(mcq("To plot the point (6, 3), what do you do first from the origin?", "Go right 6",
                   ["Go up 6", "Go right 3", "Go up 3"],
                   "The first number, 6, is the x-coordinate. It tells you how far to go across, so go right 6. Then go up 3.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s plots the point (2, 5). %s starts at the origin, goes up 2, then right 5. What mistake did %s make?" % (n, H, he),
                   "%s swapped x and y" % H,
                   ["%s counted the starting point" % H, "%s should have gone left" % H, "No mistake. %s is right" % H],
                   "In (2, 5), x = 2 comes first: go right 2, then up 5. %s went up 2 and right 5, so %s plotted (5, 2)." % (n, he), rnd))
    its.append(mcq("A point is on the x-axis, 8 units to the right of the origin. What are its coordinates?", pair(8, 0),
                   [pair(0, 8), pair(8, 8), pair(8, 1)],
                   "8 units right gives x = 8. The point is on the x-axis, so it does not go up: y = 0. The point is (8, 0).", rnd))
    n, he, his = P.next()
    its.append(mcq("In a coding lesson, %s’s robot starts at (1, 2). The code says: move 4 right, then move 3 up. Where does the robot stop?" % n,
                   "(5, 5)", [pair(*c) for c, w, k in slide_kinds((1, 2), 4, 3)], move_e((1, 2), 4, 3), rnd))
    n, he, his = P.next()
    its.append(mcq("%s’s robot is at (2, 7). %s wants it to stop at (6, 3). Which code works?" % (n, he.capitalize()),
                   "4 right, 4 down", describe_cands(4, -4, 2), describe_e((2, 7), (6, 3), "The start", "the end"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a board game, each turn moves a counter 2 units right. %s’s counter starts at (1, 4). Where is it after 3 turns?" % n,
                   "(7, 4)", ["(3, 4)", "(6, 4)", "(4, 7)"],
                   "3 turns is 3 × 2 = 6 units right. x: 1 + 6 = 7. y stays 4. The counter is at (7, 4).", rnd))
    its.append(mcq("On a map of a campground near Kamloops, the fire pit is at (3, 5) and the canoe dock is at (8, 1). Describe the slide from the fire pit to the dock.",
                   "5 right, 4 down", describe_cands(5, -4, 1), describe_e((3, 5), (8, 1), "The fire pit", "the dock"), rnd))
    n, he, his = P.next()
    its.append(mcq("On a lacrosse play diagram, %s runs from (2, 3), 6 units right and 4 units up. Where does %s stop?" % (n, he),
                   "(8, 7)", [pair(*c) for c, w, k in slide_kinds((2, 3), 6, 4)], move_e((2, 3), 6, 4), rnd))
    its.append(mcq_num("On a map of Stanley Park, the totem poles are at (4, 1) and the lighthouse is at (4, 7). How many units apart are they?",
                       6, [7, 5, 10],
                       "The x-coordinates are the same, so the lighthouse is straight up from the totem poles. From 1 up to 7 is 7 − 1 = 6 units. "
                       "(7 comes from counting the starting point as 1.)", fmt="%d units"))
    n, he, his = P.next()
    its.append(mcq("%s makes a paper snowflake for the class window. The design is symmetrical in the line x = 5. "
                   "One tip is at (2, 6). Where is the matching tip?" % n,
                   "(8, 6)", [pair(*q) for q, w, k in refl_kinds((2, 6), ("v", 5))], refl_e((2, 6), ("v", 5), "The tip"), rnd))
    its.append(mcq("A class banner is symmetrical in the horizontal line y = 5. One corner is at (3, 2). Where is the matching corner?", "(3, 8)",
                   [pair(*q) for q, w, k in refl_kinds((3, 2), ("h", 5))], refl_e((3, 2), ("h", 5), "The corner"), rnd))
    bed = [(1, 2), (3, 2), (3, 4), (1, 4)]
    img = [reflect(p, ("v", 5)) for p in bed]
    its.append(mcq("A school garden has a path along the line x = 5. A garden bed with vertices at %s is flipped over the path to make a matching bed. "
                   "Which list shows the vertices of the new bed?" % plist(bed), plist(img),
                   [plist(shift(img, -1, 0)), plist(shift(bed, 5, 0)), plist([reflect(p, ("h", 5)) for p in bed])],
                   "Each vertex goes the same distance on the other side of x = 5: (1, 2) is 4 units left, so its image is 4 units right, at (9, 2). "
                   "(3, 2) is 2 units left, so its image is (7, 2).", rnd))
    n, he, his = P.next()
    p, c = (7, 6), (5, 5)
    its.append(mcq("%s draws a pinwheel for a Terry Fox Run poster. One blade tip is at %s. The next blade is the first one turned "
                   "90° counterclockwise about the centre %s. Where is the next tip?" % (n, pair(*p), pair(*c)), pair(*rot(p, c, "ccw")),
                   [pair(*x) for x, w in rot_kinds(p, c, "ccw")], rot_e(p, c, "ccw", "The tip", "the centre"), rnd))
    n, he, his = P.next()
    p, c = (8, 7), (6, 6)
    its.append(mcq("%s makes a quilt pattern. A triangle has a vertex at %s. %s turns the triangle 180° about its vertex %s. "
                   "Where does the vertex at %s go?" % (n, pair(*p), he.capitalize(), pair(*c), pair(*p)), pair(*rot(p, c, "half")),
                   [pair(*x) for x, w in rot_kinds(p, c, "half")], rot_e(p, c, "half", "The vertex", "the centre"), rnd))
    its.append(mcq("A rug on a floor plan covers 6 squares. It is turned 90° about one corner. Which sentence is true?",
                   "It still covers 6 squares", ["It now covers 9 squares", "It now covers 3 squares", "It now covers 12 squares"],
                   "A turn moves the rug but does not stretch it. The side lengths, angles and area stay the same, so it still covers 6 squares.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Coordinates in the first quadrant: word problems", "items": its}


# ------------------------------------------------------------ lesson
def flip_turn_svg():
    """Two small grids: the same L-shape flipped in a line and turned a half turn."""
    cols, rows, cs, o, pad, gap = 7, 5, 18, 8, 8, 34
    A = [(0, 1), (2, 1), (2, 2), (1, 2), (1, 4), (0, 4)]
    line = ("v", 3)
    fl = [reflect(p, line) for p in A]
    tu = [rot(p, (3, 1), "half") for p in A]
    tu = shift(tu, 0, 3)          # keep the half turn on the grid: the turn centre moves with it
    gw, gh = cols * cs, rows * cs
    W = 2 * pad + 2 * (gw + 2 * o) + gap
    H = 2 * pad + gh + 2 * o + 26
    el = []
    for k, (img, name) in enumerate([(fl, "flip: mirror image"), (tu, "turn: upside down")]):
        x0 = pad + k * (gw + 2 * o + gap) + o
        el += panel_el(cols, rows, A, img, cs, x0, pad + o, line if k == 0 else None, None)
        el.append(text(x0 + gw / 2.0, pad + o + gh + o + 18, name, 15, bold=True))
    return svg_wrap(W, H, "".join(el), "an L-shape flipped in a dashed line, and the same L-shape turned a half turn")


def body_html():
    G = Grid(7, 6)
    G.arrow((0, 0), (4, 0)).arrow((4, 0), (4, 3))
    G.note(2, 0.5, "right 4").note(4.2, 1.5, "up 3", anchor="start")
    G.point(4, 3, "A", where=(1, 1))
    plot = G.svg("coordinate grid: from the origin go right 4, then up 3 to point A at (4, 3)")
    G = Grid(10, 7)
    A = [(1, 4), (4, 4), (1, 6)]
    G.poly(A, GREEN, "A").poly(shift(A, 4, -3), BLUE, "B")
    G.arrow((4, 4), (8, 4)).arrow((8, 4), (8, 1))
    G.note(6, 4.5, "4 right").note(8.2, 2.5, "3 down", anchor="start")
    trans = G.svg("triangle A slid 4 units right and 3 units down to triangle B")
    G = Grid(10, 6)
    G.mirror("v", 5)
    T = [(1, 1), (4, 1), (1, 5)]
    G.poly(T, GREEN, "A").poly([reflect(p, ("v", 5)) for p in T], BLUE, "B")
    refl = G.svg("triangle A flipped in the line x = 5 to make triangle B")
    G = Grid(8, 8)
    T = [(2, 5), (5, 5), (5, 7)]
    G.poly(T, GREEN, "A").poly([rot(p, (2, 5), "cw") for p in T], BLUE, "B", (2.6, 2.7))
    G.arc((2, 5), (5, 5), (2, 2), True)
    G.point(2, 5, None, RED)
    rota = G.svg("triangle A turned 90° clockwise about its vertex (2, 5) to make triangle B")
    return (
        "<h2>Three ways to move a shape</h2>"
        "<p>A <b>transformation</b> moves a shape to a new place. In Grade 5 you do one move at a time: "
        "a <b>slide</b> (translation), a <b>flip</b> (reflection) or a <b>turn</b> (rotation). "
        "The shape keeps its size and its angles. Only its place, or the way it faces, changes.</p>" +
        table(["Move", "What happens", "Which way it faces"], [
            ["Slide (translation)", "moves left or right and up or down", "the same way"],
            ["Flip (reflection)", "flips over a line", "mirror image"],
            ["Turn (rotation)", "turns about a point", "turned"],
        ]) +
        "<h2>Slides: count the jumps</h2>"
        "<p>In a <b>slide</b> every vertex moves the same number of units in the same direction. "
        "Count the jumps from one grid point to the next. Do not count the point you start on.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A slides 4 units right and 3 units down to make B. Follow one vertex: (4, 4) → (8, 1).</figcaption></figure>" +
        ex("Example", "A point slides 5 units right. How do you count?",
           "Put your finger on the point. Say “one” on the first jump, not on the start. Stop when you say “five”.", "5 jumps right") +
        "<h2>Flips: the same distance from the line</h2>"
        "<p>A <b>flip</b> makes a mirror image over a <b>line of reflection</b>. "
        "Each vertex ends up the <b>same distance</b> from the line, on the other side.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>(1, 5) is 4 units left of the line x = 5, so its image is 4 units right of the line, at (9, 5).</figcaption></figure>" +
        ex("Example", "A vertex is 2 units left of a vertical line. Where is its image?",
           "Count 2 jumps to the line. Then count 2 more jumps past it. The line itself is not a jump.", "2 units right of the line") +
        "<h2>Turns: quarter turns and half turns</h2>"
        "<p>A <b>turn</b> moves a shape around a point called the <b>centre of rotation</b>. The centre does not move. "
        "Say how far and which way: a <b>quarter turn</b> is 90°, a <b>half turn</b> is 180°. "
        "<b>Clockwise</b> is the way clock hands move; <b>counterclockwise</b> is the other way.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A makes a quarter turn clockwise about the red vertex (2, 5). The side that went 3 right now goes 3 down.</figcaption></figure>" +
        table(["Turn", "right becomes", "up becomes"], [
            ["quarter turn clockwise", "down", "right"],
            ["quarter turn counterclockwise", "up", "left"],
            ["half turn (either way)", "left", "down"],
        ]) +
        "<h2>Flip or turn?</h2>"
        "<p>A flip changes only one thing: left and right swap, <i>or</i> top and bottom swap. "
        "A half turn swaps <i>both</i>: the shape is upside down and back to front.</p>"
        "<figure class='sn-fig'>" + flip_turn_svg() +
        "<figcaption>Left: the L is flipped in the dashed line. Its foot is still at the bottom. Right: the L makes a half turn. Its foot is now at the top.</figcaption></figure>"
        "<h2>Coordinates in the first quadrant</h2>"
        "<p>A point on a grid is named by two numbers: (x, y). Start at the <b>origin</b>, (0, 0). "
        "Go <b>across</b> first (x), then <b>up</b> (y).</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (4, 3), go right 4, then up 3. Point A is at (4, 3), not (3, 4).</figcaption></figure>" +
        ex("Example", "Point (2, 6) slides 3 units right. Where does it land?",
           "Right changes x: 2 + 3 = 5. y stays 6.", "(5, 6)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the start square or point as “one”", "Say “one” on the first jump"],
            ["Counting the line of reflection as a jump", "Go the same distance on the other side"],
            ["Calling a half turn a flip", "Upside down and back to front is a half turn"],
            ["Sliding a shape when it should be flipped", "A flip faces the other way"],
            ["Turning the wrong way", "Clockwise goes like clock hands: from 12 towards 3"],
            ["Swapping x and y", "Go across first (x), then up (y)"],
        ])
    )


FAQ = [
    {"q": "What are single transformations in BC Grade 5 math?",
     "a": "In the BC Grade 5 curriculum (Geometry and measurement), students do one transformation at a time on a grid: "
          "a slide (translation), a flip (reflection) or a turn (rotation), and they describe how the shape moved."},
    {"q": "What is the difference between a slide, a flip and a turn?",
     "a": "A slide moves a shape without changing the way it faces, a flip makes a mirror image over a line, and a turn moves it around a point. "
          "None of them changes the shape’s size or angles."},
    {"q": "How can you tell a flip from a half turn?",
     "a": "A flip swaps only left and right, or only top and bottom. A half turn swaps both, so the shape ends up upside down and back to front."},
    {"q": "Why do students land one square short when they slide a shape?",
     "a": "They often say “one” on the square or point where they start. Count “one” on the first jump instead, and the shape lands in the right place."},
]


def gen_unit():
    rnd = random.Random(55814)
    P = People(rnd)
    sets = [set_slide(rnd, P), set_flip(rnd, P), set_turn(rnd, P), set_which(rnd, P), set_coords(rnd, P)]
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
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "single-transformations", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Single Transformations: Slides, Flips and Turns on a Grid",
        "seo_title": "Grade 5 Math: Single Transformations Worksheets – Slides, Flips and Turns (Free, BC Curriculum, Answer Key)",
        "short_title": "Single transformations",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 5: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Single transformations",
        "meta_desc": "Free Grade 5 math worksheets on single transformations for the BC curriculum: slide (translate), flip (reflect) and turn (rotate) shapes on a grid, tell which transformation was used and read points in the first quadrant. 100 questions with an answer key.",
        "key_big": "A slide moves, a flip makes a mirror image, a turn goes around a point. The shape never changes size.",
        "key_sub": "Count the jumps, not the square you start on. In a flip each point stays the same distance from the line. In a turn the centre does not move.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(coordinate grid|four grid pictures)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
