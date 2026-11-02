# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Coordinates and transformations
(Australian Curriculum v9.0, AC9M5SP03 with AC9M5SP02)
  python3 tools/gen_au_maths_y5_transformations.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

First quadrant only, whole-number coordinates 0-10. Mirror lines are vertical (x = m) or
horizontal (y = m), drawn as a dashed purple line with their name. Rotations are quarter and
half turns about a marked point O. Every grid is drawn exactly. Letter labels sit in the middle
of a grid square next to their own point, never in a square that touches another point and never
on a line, note or other label (checked in Grid.render). Lines of symmetry and the order of
rotational symmetry of every shape picture are worked out from the drawn shape (sym_counts).
Wrong answers come from real Year 5 mistakes: swapping x and y, counting grid lines instead of
squares (1 too far), moving the wrong way, sliding instead of flipping, stopping on the mirror
line, rotating the wrong way or turning a half turn instead of a quarter turn, thinking the shape
changes size, counting the diagonals of a rectangle as lines of symmetry.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
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


def variants(shape, line, cols, rows):
    ok = frozenset(mir(x, line) for x in shape)
    b0, b1 = bbox(shape), bbox(ok)
    dc, dr = b1[0] - b0[0], b1[1] - b0[1]
    out = {"ok": ok,
           "slide": frozenset((c + dc, r + dr) for c, r in shape),
           "turn": frozenset((b0[0] + b0[2] - c + dc, b0[1] + b0[3] - r + dr) for c, r in shape)}
    if line[0] == "v":
        s = sgn(b1[0] - line[1] + 0.5)
        out["far"] = frozenset((c + s, r) for c, r in ok)
        out["bigger"] = frozenset(ok | {(c, r + 1) for c, r in ok if r == b1[3]})
    else:
        s = sgn(b1[1] - line[1] + 0.5)
        out["far"] = frozenset((c, r + s) for c, r in ok)
        out["bigger"] = frozenset(ok | {(c + 1, r) for c, r in ok if c == b1[2]})
    return out


PANEL_WHY = {"slide": "the shape was slid across, not flipped (it points the same way)",
             "far": "the image is 1 square too far from the mirror line",
             "turn": "the shape was turned upside down, not flipped",
             "bigger": "the image has more squares, so its size changed"}


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


PANELS = [
    (("v", 4), 8, 5, ["....", "..#.", ".##.", "..#.", "...."], ["slide", "far", "bigger"]),
    (("h", 4), 6, 8, ["......", "....#.", ".####.", "......"], ["slide", "turn", "far"]),
    (("v", 4), 8, 5, ["....", ".###", ".#..", ".#..", "...."], ["slide", "turn", "bigger"]),
    (("h", 4), 6, 8, ["......", ".##...", "..#...", "..###."], ["turn", "far", "bigger"]),
]


def panel_q(line, cols, rows, half, wrongs, pos, rnd):
    shape = cells_of(half)
    V = variants(shape, line, cols, rows)
    V = {k: V[k] for k in ["ok"] + wrongs}
    for k, s in V.items():
        assert all(0 <= c < cols and 0 <= r < rows for c, r in s), k
        assert not (s & shape), k
    assert len(set(V.values())) == len(V)
    p = pos.next()
    w = wrongs[:]
    rnd.shuffle(w)
    keys = w[:p] + ["ok"] + w[p:]
    cs = 14
    svg = panel_svg(cols, rows, shape, [V[k] for k in keys], line, cs, "four grid pictures A to D with a dashed mirror line")
    where = "row" if line[0] == "v" else "column"
    q = (fig(svg) + "The green shape is reflected in the dashed mirror line. In which picture is the blue image correct?")
    others = "; ".join("%s: %s" % ("ABCD"[j], PANEL_WHY[k]) for j, k in enumerate(keys) if k != "ok")
    e = ("Each blue square must be the same number of squares from the mirror line as its green partner, on the other side, "
         "in the same %s. Only <b>%s</b> is a true mirror image. Others: %s." % (where, "ABCD"[p], others))
    return mcq_fixed(q, LETTERS, "ABCD"[p], e)


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


ROT_WHY = {"cw": "it was turned clockwise", "acw": "it was turned anticlockwise", "half": "it was turned a half turn",
           "flipv": "it was flipped in a mirror line, not turned", "fliph": "it was flipped upside down, not turned"}

ROT_PANELS = [
    ("cw", ["...#..", "...#..", "...##.", "......", "......", "......"], ["acw", "half", "flipv"]),
    ("acw", ["......", ".....#", "...###", "......", "......", "......"], ["cw", "half", "fliph"]),
    ("half", ["....#.", "...##.", "...#..", "......", "......", "......"], ["cw", "acw", "flipv"]),
    ("cw", ["....#.", "....#.", "...##.", "......", "......", "......"], ["acw", "half", "fliph"]),
]


def rot_panel_q(kind, half, wrongs, pos, rnd):
    shape = cells_of(half)
    piv = (3, 3)
    V = {k: rot_cells(shape, piv, k) for k in [kind] + wrongs}
    for k, s in V.items():
        assert all(0 <= c < 6 and 0 <= r < 6 for c, r in s), k
        assert not (s & shape), k
    assert len(set(V.values())) == 4
    p = pos.next()
    w = wrongs[:]
    rnd.shuffle(w)
    keys = w[:p] + [kind] + w[p:]
    svg = panel_svg(6, 6, shape, [V[k] for k in keys], ("o", piv), 14, "four grid pictures A to D with a red dot")
    q = fig(svg) + "The green shape is turned %s about the red dot. In which picture is the blue image correct?" % TURN[kind]
    others = "; ".join("%s: %s" % ("ABCD"[j], ROT_WHY[k]) for j, k in enumerate(keys) if k != kind)
    e = ("The red dot stays still and the shape turns around it. In %s, %s. Follow the part of the shape that touches the dot. "
         "Only <b>%s</b> is correct, and the shape is still the same size. Others: %s." % (TURN[kind], WAYS[kind], "ABCD"[p], others))
    return mcq_fixed(q, LETTERS, "ABCD"[p], e)


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


def shape_el(parts, x0, y0, bw, bh):
    pts = [p for part in parts for p in part]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    k = min(bw / (maxx - minx), bh / (maxy - miny))
    ox = x0 + (bw - (maxx - minx) * k) / 2.0
    oy = y0 + (bh - (maxy - miny) * k) / 2.0
    el = []
    for part in parts:
        el.append("<polygon points='%s' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                  % (" ".join("%.1f,%.1f" % (ox + (x - minx) * k, oy + (maxy - y) * k) for x, y in part), SHADE, GREEN))
    return el


def shape_svg(name):
    W, H, pad = 150, 110, 8
    return svg_wrap(W, H, "".join(shape_el(SHAPES[name], pad, pad, W - 2 * pad, H - 2 * pad)), "a " + name)


def shapes4_svg(names):
    cw, ch, LW, gap, pad = 110, 80, 24, 14, 6
    el = []
    for k, n in enumerate(names):
        x0 = pad + (k % 2) * (LW + cw + gap)
        y0 = pad + (k // 2) * (ch + gap)
        el.append(text(x0, y0 + 18, "ABCD"[k], 18, anchor="start", bold=True))
        el += shape_el(SHAPES[n], x0 + LW, y0, cw, ch)
    W = 2 * pad + 2 * (LW + cw) + gap
    H = 2 * pad + 2 * ch + gap
    return svg_wrap(W, H, "".join(el), "four shapes A to D")


SYM_WHY = {
    "square": "a square has 4 lines of symmetry: 2 through the middles of opposite sides and 2 along the diagonals",
    "rectangle": "a rectangle has only 2 lines of symmetry, through the middles of opposite sides. The diagonals are not lines of symmetry: "
                 "if you fold along a diagonal, the corners do not meet",
    "equilateral triangle": "an equilateral triangle has 3 equal sides, so it has 3 lines of symmetry, one from each corner to the middle of the opposite side",
    "isosceles triangle": "an isosceles triangle has 1 line of symmetry, down the middle between the 2 equal sides",
    "parallelogram": "a parallelogram has no lines of symmetry. If you fold it in half either way, the halves do not match, because the sides slope",
    "regular hexagon": "a regular hexagon has 6 lines of symmetry: 3 through opposite corners and 3 through the middles of opposite sides",
    "regular octagon": "a regular octagon has 8 lines of symmetry: 4 through opposite corners and 4 through the middles of opposite sides",
    "kite": "a kite has 1 line of symmetry, through the corners where the equal sides meet",
    "rhombus": "a rhombus has 2 lines of symmetry, along its diagonals",
    "pinwheel": "the pinwheel has no lines of symmetry: every blade leans the same way, so a mirror image would lean the other way",
}


def lines_q(name, cands, rnd, intro=None, show=True):
    L, O = sym_counts(SHAPES[name])
    q = (fig(shape_svg(name)) if show else "") + (intro or "How many lines of symmetry does this %s have?" % name)
    return mcq(q, str(L), [str(c) for c in cands], SYM_WHY[name][0].upper() + SYM_WHY[name][1:] + ".", rnd)


def order_q(name, cands, rnd, intro=None, show=True):
    L, O = sym_counts(SHAPES[name])
    q = (fig(shape_svg(name)) if show else "") + (intro or "Turn this %s about its centre. How many times does it fit exactly onto its outline in one full turn?" % name)
    e = ("Turn a tracing of the shape. The %s fits onto its outline %s in one full turn (every %d°), so it has rotational symmetry of order %d. "
         "Count the full turn once, not the start as well." % (name, "once" if O == 1 else "%d times" % O, 360 // O, O))
    return mcq(q, str(O), [str(c) for c in cands], e, rnd)


# ------------------------------------------------------------ set 1: read and plot coordinates
def read_cands(x, y, i):
    c = [(y, x), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y), (x, y + 1)]
    return [q for q in c if inside(q) and q != (x, y)]


def to_compass(t):
    for a, b in [("Right ", "East "), ("Left ", "West "), ("Up ", "North "), ("Down ", "South ")]:
        t = t.replace(a, b)
    return t


def read_e(x, y, name):
    if y == 0:
        return ("Start at (0, 0). Go across to %d and do not go up at all: the point is on the x-axis. %s is at %s. "
                "The x-coordinate is written first." % (x, name, pair(x, y)))
    return ("Start at (0, 0). Go across to %d on the x-axis, then up to %d. %s is at %s. "
            "Across first, then up: the x-coordinate is written first." % (x, y, name, pair(x, y)))


def compass(dx, dy):
    parts = []
    if dx:
        parts.append("%s %s" % (sq(abs(dx)), "east" if dx > 0 else "west"))
    if dy:
        parts.append("%s %s" % (sq(abs(dy)), "north" if dy > 0 else "south"))
    return " and ".join(parts)


def set_coords(rnd, P):
    its = []
    pos = Pos(rnd)
    # read coordinates; a point sits at the swapped spot so the x/y mix-up can be seen
    for i, (t, others) in enumerate([((3, 5), [(5, 3), (7, 1)]), ((6, 2), [(2, 6), (4, 7)]), ((1, 4), [(4, 1), (6, 6)]),
                                     ((7, 6), [(6, 7), (2, 2)]), ((4, 0), [(0, 4), (6, 3)])]):
        names = ["A", "B", "C"]
        rnd.shuffle(names)
        G = grid_for([t] + others, lo=7)
        G.point(t[0], t[1], names[0])
        for o, n in zip(others, names[1:]):
            G.point(o[0], o[1], n)
        its.append(mcq(fig(G.svg("coordinate grid with points A, B and C")) + "What are the coordinates of point %s?" % names[0],
                       pair(*t), [pair(*c) for c in read_cands(t[0], t[1], i)], read_e(t[0], t[1], "Point " + names[0]), rnd))
    # plot: which point is at (x, y)?
    for t, extra in [((2, 5), (1, 4)), ((6, 3), (5, 2)), ((5, 7), (4, 6)), ((0, 6), (1, 6))]:
        x, y = t
        others = [(y, x), extra, (extra[1], extra[0])] if t != (0, 6) else [(6, 0), (6, 6), (1, 7)]
        pts, ans = pick_letters(t, others, pos)
        G = grid_for([c[:2] for c in pts], lo=7)
        for c in pts:
            G.point(*c)
        e = read_e(x, y, "The point") + " That is point %s." % ans
        if t == (0, 6):
            e = ("x = 0 means you do not go across at all. Go straight up the y-axis to 6. That is point %s. "
                 "(6, 0) is on the x-axis instead." % ans)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with points A to D")) + "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    its.append(mcq("In the coordinates (3, 7), which number tells you how far to go across?", "3, the first number",
                   ["7, the second number", "10, the two numbers added", "both numbers"],
                   "The first number is the x-coordinate: how far across. The second number is the y-coordinate: how far up. "
                   "(3, 7) is 3 across and 7 up.", rnd))
    its.append(mcq("What is the point (0, 0) called?", "the origin", ["the x-axis", "the y-axis", "a mirror line"],
                   "(0, 0) is where the x-axis and the y-axis meet. It is called the origin. You start counting from there.", rnd))
    its.append(mcq("Which point is on the y-axis?", "(0, 6)", ["(6, 0)", "(6, 6)", "(1, 6)"],
                   "Every point on the y-axis has x-coordinate 0, because you do not go across. (6, 0) is on the x-axis.", rnd))
    # directional language on a map grid (north is up)
    for i, (who, p, dx, dy, place) in enumerate([
        ("a school excursion to the zoo", (1, 2), 3, 2, "the koala enclosure"),
        ("a school camp", (7, 6), -4, -3, "the dining hall"),
        ("the botanic gardens", (2, 8), 5, -6, "the lily pond"),
    ]):
        n, he, his = P.next()
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("On a map grid of %s, north is up the page. %s starts at %s and walks %s to %s. "
                       "What are the coordinates of %s?" % (who, n, pair(*p), compass(dx, dy), place, place),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)],
                       "East and west change x; north and south change y. " + to_compass(move_e(p, dx, dy)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s is at (4, 6) on a map grid where north is up. %s friend is at (4, 2). In which direction should %s walk to reach %s friend?"
                   % (n, his.capitalize(), he, his), "south", ["north", "east", "west"],
                   "x stays 4, so there is no move east or west. y goes from 6 down to 2, which is down the page: south.", rnd))
    its.append(mcq("On a map grid of a school, north is up the page. The canteen is at (2, 3) and the library is at (7, 3). "
                   "How do you walk from the canteen to the library?", "5 squares east",
                   ["5 squares west", "5 squares north", "6 squares east"],
                   "y stays 3, so there is no move north or south. x goes from 2 up to 7: 7 − 2 = 5 squares to the right, which is east. "
                   "Count squares, not lines (that gives 6).", rnd))
    its.append(mcq("A rectangle has three corners at (1, 1), (6, 1) and (6, 4). What are the coordinates of the fourth corner?", "(1, 4)",
                   ["(4, 1)", "(4, 6)", "(6, 6)"],
                   "The fourth corner is above (1, 1) and across from (6, 4). So it has x-coordinate 1 and y-coordinate 4: (1, 4).", rnd))
    its.append(mcq_num("How many squares apart are the points (2, 6) and (9, 6)?", 7, [8, 9, 11],
                       "The y-coordinates are the same, so the points are on the same row. Take the x-coordinates: 9 − 2 = 7 squares. "
                       "Counting the lines, including the first one, gives 8.", fmt="%d squares"))
    n, he, his = P.next()
    its.append(mcq("%s wants to plot the point (2, 5). %s goes 5 across and then 2 up. What mistake did %s make?" % (n, he.capitalize(), he),
                   "%s swapped x and y" % he.capitalize(),
                   ["%s should go down, not up" % he.capitalize(), "%s should start at (1, 1)" % he.capitalize(), "No mistake: %s is right" % he],
                   "Across first, then up. (2, 5) means 2 across and 5 up. %s plotted (5, 2) instead." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read and plot coordinates", "items": its}


# ------------------------------------------------------------ set 2: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    for i, (a, b) in enumerate([((2, 3), (5, 1)), ((6, 2), (3, 6)), ((3, 6), (3, 1))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    for i, (kind, A, dx, dy, at) in enumerate([
        ("triangle", [(1, 5), (4, 5), (1, 8)], 5, -4, None),
        ("rectangle", [(1, 1), (4, 1), (4, 3), (1, 3)], 5, 4, None),
        ("L-shape", [(6, 5), (9, 5), (9, 6), (7, 6), (7, 8), (6, 8)], -5, -4, (6.5, 5.5)),
    ]):
        B = shift(A, dx, dy)
        G = Grid(10, 8 if max(p[1] for p in A + B) <= 8 else 9)
        G.poly(A, GREEN, "A", at).poly(B, BLUE, "B", (at[0] + dx, at[1] + dy) if at else None)
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                       "Shape A is translated to shape B. Describe the translation.", mv(dx, dy), describe_cands(dx, dy, i + 1),
                       "Follow one corner. The corner of A at %s moves to %s in B. That is %s. Every corner moves the same way."
                       % (pair(*A[0]), pair(*B[0]), mv_long(dx, dy)), rnd))
    for i, (a, b) in enumerate([((2, 7), (8, 3)), ((9, 1), (5, 6))]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq("A corner of a shape moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(dx, dy, i + 2), describe_e(a, b, "The start", "the end"), rnd))
    for i, (p, dx, dy) in enumerate([((3, 4), 2, 3), ((2, 7), 5, -4), ((8, 3), -6, 2), ((1, 2), 0, 6)]):
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    for p, dx, dy in [((2, 6), 4, -3), ((7, 2), -5, 4), ((1, 1), 6, 5)]:
        q = (p[0] + dx, p[1] + dy)
        others = [c for c in move_cands(p, dx, dy) if c != q][:3]
        pts, ans = pick_letters(q, others, pos)
        G = grid_for([p] + [c[:2] for c in pts], lo=7)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is translated %s. Which point shows where it lands?" % mv_long(dx, dy),
                             LETTERS, ans, move_e(p, dx, dy) + " That is point %s." % ans))
    tri = [(2, 1), (5, 1), (2, 3)]
    its.append(mcq("A triangle has corners at %s. It is translated 3 squares right and 4 squares up. Which list shows the new corners?" % plist(tri),
                   plist(shift(tri, 3, 4)),
                   [plist(shift(tri, 3, 0)), plist(shift(tri, 4, 3)), plist([(5, 5), (5, 1), (2, 3)])],
                   "Add 3 to every x-coordinate and 4 to every y-coordinate: %s. Move every corner, not just one."
                   % ", ".join("%s → %s" % (pair(*a), pair(*b)) for a, b in zip(tri, shift(tri, 3, 4))), rnd))
    its.append(mcq("Point B is translated 4 squares right and 3 squares up. It lands on (6, 8). Where did it start?", "(2, 5)",
                   ["(10, 11)", "(3, 4)", "(2, 8)"],
                   "Work backwards and undo each move. 4 right is undone by 4 left: 6 − 4 = 2. 3 up is undone by 3 down: 8 − 3 = 5. B started at (2, 5).", rnd))
    n, he, his = P.next()
    its.append(mcq("Point A is at (2, 4) and point B is at (6, 4). %s counts the grid lines from A to B, starting with 1 on A’s line, "
                   "and says A moved 5 right. What is the correct translation?" % n,
                   "4 right", ["5 right", "4 left", "6 right"],
                   "Count the squares you jump, not the lines: 6 − 2 = 4. %s counted the line A starts on, so %s got 1 too many." % (n, he), rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (6, 4) 2 squares left and gets (8, 4). What mistake did %s make?" % (n, he),
                   "%s moved right, not left" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake: %s is right" % he],
                   "Moving left makes the x-coordinate smaller: 6 − 2 = 4. The correct answer is (4, 4). %s added 2, which is a move to the right." % n, rnd))
    its.append(mcq("A point is translated up or down. Which coordinate changes?", "only the y-coordinate",
                   ["only the x-coordinate", "both coordinates", "neither coordinate"],
                   "Up and down is the y direction. The point does not move left or right, so the x-coordinate stays the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations: slide a shape", "items": its}


# ------------------------------------------------------------ set 3: reflections
def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, line in [((3, 4), ("v", 5)), ((8, 2), ("v", 6)), ((2, 1), ("h", 3)), ((6, 9), ("h", 6)), ((1, 7), ("v", 4)), ((5, 3), ("h", 5))]:
        r = reflect(p, line)
        assert inside(r)
        its.append(mcq("Reflect the point %s in %s. What are the coordinates of the image?" % (pair(*p), lword(line)),
                       pair(*r), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line), rnd))
    for p, line, pick in [((2, 3), ("v", 4), ["far", "stop", "wrong"]), ((7, 5), ("v", 5), ["far", "stop", "swap"]),
                          ((3, 1), ("h", 3), ["far", "stop", "swap"]), ((5, 6), ("h", 4), ["far", "stop", "wrong"])]:
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
        its.append(mcq_fixed(fig(G.svg("coordinate grid with a mirror line, point P and points A to D")) +
                             "Which point is the reflection of point P in the mirror line %s?" % lname(line), LETTERS, ans, e))
    for line, cols, rows, half, wrongs in PANELS:
        its.append(panel_q(line, cols, rows, half, wrongs, pos, rnd))
    its.append(mcq("Reflect the point (5, 3) in the vertical mirror line x = 5. What are the coordinates of the image?", "(5, 3)",
                   ["(6, 3)", "(3, 5)", "(0, 3)"],
                   refl_e((5, 3), ("v", 5)) + " A point on the mirror line is its own reflection.", rnd))
    its.append(mcq("A point is reflected in a vertical mirror line. Which coordinate changes?", "only the x-coordinate",
                   ["only the y-coordinate", "both coordinates", "neither coordinate"],
                   "A vertical mirror line goes up and down. The point flips across it, left to right, so only x changes. y stays the same.", rnd))
    its.append(mcq("Point P is 3 squares to the left of a vertical mirror line. Where is its image?", "3 squares to the right of the line",
                   ["6 squares to the right of the line", "3 squares to the left of the line", "4 squares to the right of the line"],
                   "In a reflection the image is the same distance from the mirror line as the point, on the other side.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s reflects a right-angled triangle in a vertical mirror line. %s image points the same way as the triangle. What mistake did %s make?"
                   % (n, his.capitalize(), he),
                   "%s slid it instead of flipping it" % he.capitalize(),
                   ["%s made it bigger" % he.capitalize(), "%s reflected it too far" % he.capitalize(), "No mistake: %s is right" % he],
                   "A reflection is a mirror image, so it faces the other way. If the image points the same way, the shape was slid (translated).", rnd))
    rect = [(1, 2), (3, 2), (3, 5), (1, 5)]
    line = ("v", 4)
    its.append(mcq("A rectangle has corners at %s. It is reflected in %s. What are the new coordinates of the corner at (1, 5)?"
                   % (plist(rect), lword(line)), pair(*reflect((1, 5), line)), [pair(*q) for q, w, k in refl_kinds((1, 5), line)],
                   refl_e((1, 5), line, "The corner"), rnd))
    tri = [(2, 1), (5, 1), (2, 2)]
    line = ("h", 3)
    img = [reflect(p, line) for p in tri]
    its.append(mcq("A triangle has corners at %s. It is reflected in %s. Which list shows the corners of the image?" % (plist(tri), lword(line)),
                   plist(img), [plist(shift(tri, 0, 3)), plist([reflect(p, ("v", 3)) for p in tri]), plist(shift(img, 0, 1))],
                   "Each corner goes the same distance on the other side of y = 3, and x stays the same. (2, 1) is 2 below the line, so it goes to (2, 5). "
                   "(2, 2) is 1 below, so it goes to (2, 4).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in a vertical or horizontal line", "items": its}


# ------------------------------------------------------------ set 4: rotations
ROT_CASES = [
    ((5, 4), [(5, 4), (8, 4), (7, 6)], "cw", None),
    ((4, 4), [(4, 4), (4, 7), (6, 6)], "acw", None),
    ((5, 4), [(5, 4), (8, 4), (8, 6), (6, 6)], "half", None),
    ((5, 4), [(5, 4), (8, 4), (7, 6)], "refl", None),
    ((4, 3), [(4, 3), (4, 6), (2, 5)], "cw", None),
    ((5, 4), [(5, 4), (8, 4), (7, 2)], "acw", None),
]
DIRW = {(1, 0): "right", (-1, 0): "left", (0, 1): "up", (0, -1): "down"}


def set_rotate(rnd, P):
    its = []
    pos = Pos(rnd)
    for o, p, kind in [((4, 5), (7, 5), "cw"), ((5, 3), (5, 6), "cw"), ((4, 5), (6, 6), "acw"), ((5, 4), (7, 6), "half")]:
        r = rot(p, o, kind)
        cands = [rot(p, o, k) for k in ["cw", "acw", "half"] if k != kind]
        flip = (2 * o[0] - p[0], p[1]) if kind != "half" else (p[0], 2 * o[1] - p[1])
        far = (r[0] + sgn(r[0] - o[0]), r[1] + sgn(r[1] - o[1]))
        why = {flip: "flipped in a mirror line, not turned", far: "turned the right way, but 1 square too far from O"}
        for k in ["cw", "acw", "half"]:
            why[rot(p, o, k)] = "turned %s" % TURN[k]
        cands = [c for c in cands + [flip, far] if c != r and c != p and inside(c)]
        cands = [c for i, c in enumerate(cands) if c not in cands[:i]][:3]
        pts, ans = pick_letters(r, cands, pos)
        G = grid_for([o, p] + [c[:2] for c in pts], lo=7)
        G.point(o[0], o[1], "O", RED).point(p[0], p[1], "P", BLUE)
        for c in pts:
            G.point(*c)
        where = {(c[0], c[1]): c[2] for c in pts}
        e = rot_e(p, o, kind) + " That is point %s. " % ans + " ".join(
            "Point %s: %s." % (where[c], why[c]) for c in cands)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with centre O, point P and points A to D")) +
                             "Point P is rotated %s about point O. Which point shows where it lands?" % TURN[kind], LETTERS, ans, e))
    for o, A, kind, at in ROT_CASES:
        B = [(2 * o[0] - x, y) for x, y in A] if kind == "refl" else rots(A, o, kind)
        G = Grid(10, 8)
        G.poly(A, GREEN, "A").poly(B, BLUE, "B")
        G.point(o[0], o[1], "O", RED)
        v = (A[1][0] - o[0], A[1][1] - o[1])
        w = (B[1][0] - o[0], B[1][1] - o[1])
        d1, d2 = DIRW[(sgn(v[0]), sgn(v[1]))], DIRW[(sgn(w[0]), sgn(w[1]))]
        if kind == "refl":
            e = ("B is a mirror image of A in the vertical line through O: every corner stays at the same height, for example %s → %s. "
                 "A turn about O would keep the shape the same way round; this one is flipped." % (pair(*A[2]), pair(*B[2])))
            ans = "a reflection"
        else:
            e = ("Follow the side that starts at O. In A it goes from O to %s and points %s. In B the matching side goes to %s and points %s. "
                 "%s to %s is %s." % (pair(*A[1]), d1, pair(*B[1]), d2, d1.capitalize(), d2, TURN[kind]))
            ans = TURN[kind]
        its.append(mcq_fixed(fig(G.svg("coordinate grid with centre O, shape A and shape B")) +
                             "Shape A is moved to shape B. Point O does not move. What happened to shape A?", ROT, ans, e))
    for kind, half, wrongs in ROT_PANELS:
        its.append(rot_panel_q(kind, half, wrongs, pos, rnd))
    its.append(mcq("P is 3 squares to the right of O. P is rotated a quarter turn clockwise about O. Where is P now?", "3 squares below O",
                   ["3 squares above O", "3 squares to the left of O", "4 squares below O"],
                   "In a quarter turn clockwise, right turns into down, like the hand of a clock going from 3 to 6. "
                   "P stays the same distance from O: 3 squares below O.", rnd))
    its.append(mcq("P is 2 squares above O. P is rotated a half turn about O. Where is P now?", "2 squares below O",
                   ["2 squares to the right of O", "2 squares to the left of O", "4 squares below O"],
                   "A half turn turns up into down. P stays the same distance from O, so it is 2 squares below O, not 4.", rnd))
    its.append(mcq("P is 4 squares to the left of O. P is rotated a quarter turn anticlockwise about O. Where is P now?", "4 squares below O",
                   ["4 squares above O", "4 squares to the right of O", "5 squares below O"],
                   "Anticlockwise goes the other way to the hands of a clock: left turns into down (from 9 back to 6). P is still 4 squares from O.", rnd))
    its.append(mcq_fixed("Mia faces north. She makes a quarter turn clockwise. Which way does she face now?", ["north", "east", "south", "west"], "east",
                         "Clockwise goes north → east → south → west. A quarter turn is one step: east."))
    n, he, his = P.next()
    its.append(mcq("P is 2 squares to the right of O. %s rotates P a quarter turn clockwise about O and puts it 2 squares above O. What mistake did %s make?"
                   % (n, he), "%s turned it anticlockwise" % he.capitalize(),
                   ["%s turned it a half turn" % he.capitalize(), "%s moved it too far from O" % he.capitalize(), "No mistake: %s is right" % he],
                   "Clockwise turns right into down, so P should be 2 squares below O. Going from right to up is a quarter turn anticlockwise.", rnd))
    o, p = (4, 3), (6, 3)
    its.append(mcq("The point (6, 3) is rotated a half turn about the point (4, 3). What are the coordinates of the image?",
                   pair(*rot(p, o, "half")), [pair(*rot(p, o, "cw")), pair(*rot(p, o, "acw")), pair(*o)],
                   "(6, 3) is 2 squares right of (4, 3). A half turn turns right into left, so the image is 2 squares left: (2, 3). "
                   "It does not stop on the centre.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rotations: quarter and half turns", "items": its}


# ------------------------------------------------------------ set 5: what stays the same, symmetry and problems
def set_same(rnd, P):
    its = []
    pos = Pos(rnd)
    T = [(1, 1), (4, 1), (2, 3)]
    cases = [
        (T, shift(T, 5, 3), "a translation",
         "B faces the same way as A and is the same size. Every corner moved 5 squares right and 3 squares up, for example (1, 1) → (6, 4)."),
        (T, [reflect(q, ("v", 5)) for q in T], "a reflection",
         "B is a mirror image of A in the line x = 5: (1, 1) → (9, 1) and (4, 1) → (6, 1). The shape is flipped but the same size."),
        (T, rots(T, (4, 1), "cw"), "a rotation",
         "B is A turned a quarter turn clockwise about the corner (4, 1): the side from (4, 1) to (1, 1) pointed left and now points up, "
         "to (4, 4). The shape is the same size."),
        (T, [(4, 2), (10, 2), (6, 6)], "it changed size",
         "The bottom side of A is 3 squares long, but the bottom side of B is 6 squares long. B is bigger, so it is not a translation, "
         "a reflection or a rotation."),
    ]
    for A, B, ans, e in cases:
        G = Grid(10, 7)
        G.poly(A, GREEN, "A").poly(B, BLUE, "B")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) + "What happened to shape A to make shape B?", MOVES, ans, e))
    its.append(lines_q("rectangle", [4, 1, 0], rnd))
    its.append(lines_q("equilateral triangle", [1, 6, 0], rnd))
    its.append(lines_q("parallelogram", [2, 1, 4], rnd))
    its.append(lines_q("kite", [2, 4, 0], rnd))
    its.append(order_q("square", [1, 2, 8], rnd))
    its.append(order_q("pinwheel", [1, 2, 8], rnd,
                       intro="This pinwheel pattern is turned about its centre. How many times does it fit exactly onto its outline in one full turn?"))
    names = ["rectangle", "kite", "isosceles triangle"]
    rnd.shuffle(names)
    p = pos.next()
    names.insert(p, "parallelogram")
    for n in names:
        L, O = sym_counts(SHAPES[n])
        assert (L == 0 and O > 1) == (n == "parallelogram"), n
    its.append(mcq_fixed(fig(shapes4_svg(names)) + "Which shape has rotational symmetry but no line of symmetry?", LETTERS, "ABCD"[p],
                         "The parallelogram (%s) fits onto itself after a half turn, but folding it never makes the halves match. "
                         "The rectangle has both kinds of symmetry. The kite and the isosceles triangle have a line of symmetry but no rotational symmetry."
                         % "ABCD"[p]))
    L8, O8 = sym_counts(SHAPES["regular octagon"])
    its.append(mcq(fig(shape_svg("regular octagon")) + "A stop sign is shaped like a regular octagon. How many lines of symmetry does a regular octagon have?",
                   str(L8), ["4", "16", "2"], SYM_WHY["regular octagon"][0].upper() + SYM_WHY["regular octagon"][1:] + ".", rnd))
    L6, O6 = sym_counts(SHAPES["regular hexagon"])
    its.append(mcq("The cells in a honeycomb are shaped like regular hexagons. How many lines of symmetry does a regular hexagon have?",
                   str(L6), ["3", "12", "2"], SYM_WHY["regular hexagon"][0].upper() + SYM_WHY["regular hexagon"][1:] + ".", rnd))
    L3, O3 = sym_counts(SHAPES["equilateral triangle"])
    its.append(mcq("A give way sign is shaped like an equilateral triangle. The triangle is turned about its centre. "
                   "How many times does it fit exactly onto its outline in one full turn?", str(O3), ["1", "6", "2"],
                   "The triangle fits onto its outline after one third of a turn, two thirds of a turn and the full turn: 3 times. "
                   "It has rotational symmetry of order 3.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a triangle with a 50° angle on a grid and rotates it a quarter turn. What is the size of that angle in the image?" % n,
                   "50°", ["140°", "40°", "90°"],
                   "A rotation turns the shape but does not change it. Every angle stays the same, so the angle is still 50°. "
                   "The 90° is how far the shape turned, not an angle of the triangle.", rnd))
    its.append(mcq("On a playground plan, a rectangular sandpit is 4 m long and 3 m wide. It is rotated a half turn. What is the perimeter of the image?",
                   "14 m", ["7 m", "12 m", "28 m"],
                   "A rotation does not change the side lengths. The perimeter is still 4 + 3 + 4 + 3 = 14 m. (12 is the area in square metres.)", rnd))
    n, he, his = P.next()
    its.append(mcq("%s rotates a shape a quarter turn. %s says the image is smaller because it has been turned. Is %s right?" % (n, he.capitalize(), he),
                   "No: a rotation never changes the size",
                   ["Yes: turning makes shapes smaller", "Yes, but only for a quarter turn", "Only if it turns clockwise"],
                   "After a translation, a reflection or a rotation the shape is the same size, with the same side lengths and angles. "
                   "Only its position, and the way it faces, can change.", rnd))
    its.append(mcq("A shape is rotated a quarter turn about one of its corners. Which of these changes?", "the way it faces",
                   ["its size", "its angles", "its side lengths"],
                   "A rotation turns the shape, so it faces a new way (and most of it moves). The size, angles and side lengths stay the same.", rnd))
    its.append(mcq("In a coding lesson, a robot is at (5, 3) on a grid and faces north (up the page). It turns a quarter turn clockwise, "
                   "then moves 3 squares forward. Where is it now?", "(8, 3)", ["(2, 3)", "(5, 6)", "(5, 0)"],
                   "A quarter turn clockwise from north is east, which is to the right. 3 squares east changes x: 5 + 3 = 8. The robot is at (8, 3).", rnd))
    its.append(mcq("A tile in a floor pattern is turned a quarter turn clockwise, 3 times. Which single turn ends in the same place?",
                   "a quarter turn anticlockwise", ["a half turn", "a quarter turn clockwise", "a full turn"],
                   "3 quarter turns clockwise is a three-quarter turn. A full turn is 4 quarter turns, so it is 1 quarter turn short of a full turn: "
                   "the same as a quarter turn the other way, anticlockwise.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "What stays the same, symmetry and problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(7, 6)
    G.arrow((0, 0), (4, 0)).arrow((4, 0), (4, 5))
    G.note(2, 0.5, "4 across").note(4.2, 2.5, "5 up", anchor="start")
    G.point(4, 5, "A", RED, where=(-1, 1))
    coord = G.svg("point A at (4, 5): 4 across, then 5 up")
    G = Grid(10, 7)
    A = [(1, 4), (4, 4), (1, 6)]
    G.poly(A, GREEN, "A").poly(shift(A, 4, -3), BLUE, "B")
    G.arrow((4, 4), (8, 4)).arrow((8, 4), (8, 1))
    G.note(6, 4.5, "4 right").note(8.2, 2.5, "3 down", anchor="start")
    trans = G.svg("triangle A translated 4 squares right and 3 squares down to triangle B")
    G = Grid(10, 6)
    G.mirror("v", 5)
    T = [(1, 1), (4, 1), (1, 4)]
    G.poly(T, GREEN, "A").poly([reflect(p, ("v", 5)) for p in T], BLUE, "B")
    refl = G.svg("triangle A reflected in the mirror line x = 5 to make triangle B")
    G = Grid(9, 7)
    R = [(5, 3), (8, 3), (7, 5)]
    G.poly(R, GREEN, "A").poly(rots(R, (5, 3), "cw"), BLUE, "B")
    G.point(5, 3, "O", RED)
    rotf = G.svg("triangle A turned a quarter turn clockwise about point O to make triangle B")
    return (
        "<h2>Coordinates: across, then up</h2>"
        "<p>A <b>coordinate grid</b> has a horizontal <b>x-axis</b> and a vertical <b>y-axis</b>. They meet at the <b>origin</b>, (0, 0). "
        "Coordinates like (4, 5) tell you to go <b>across first</b>, then up.</p>"
        "<figure class='sn-fig'>" + coord +
        "<figcaption>A is at (4, 5): start at (0, 0), go 4 across, then 5 up. (5, 4) would be a different point.</figcaption></figure>"
        "<p>On a map grid with north up the page, east and west change the x-coordinate, and north and south change the y-coordinate.</p>"
        "<h2>Translations: slide the shape</h2>"
        "<p>A <b>translation</b> slides a shape left or right and up or down. Every corner moves the same number of squares in the same direction.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A is translated 4 squares right and 3 squares down to make B. Follow one corner: (4, 4) → (8, 1).</figcaption></figure>" +
        table(["Move", "What changes", "Example from (5, 4)"], [
            ["right 2", "x gets bigger", "(7, 4)"],
            ["left 2", "x gets smaller", "(3, 4)"],
            ["up 2", "y gets bigger", "(5, 6)"],
            ["down 2", "y gets smaller", "(5, 2)"],
        ]) +
        ex("Example 1", "Describe the translation from (2, 7) to (8, 3).",
           "Across: 2 to 8 is 6 squares right. Up and down: 7 to 3 is 4 squares down.", "6 squares right and 4 squares down") +
        "<h2>Reflections: flip in a mirror line</h2>"
        "<p>A <b>reflection</b> flips a shape over a mirror line. Each corner ends up the <b>same distance</b> from the line, on the other side. "
        "The line x = 5 is vertical; the line y = 4 is horizontal.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>(1, 4) is 4 squares left of x = 5, so its image is 4 squares right, at (9, 4). In a vertical mirror line only x changes.</figcaption></figure>" +
        ex("Example 2", "Reflect (3, 4) in the mirror line x = 5.",
           "(3, 4) is 2 squares left of the line. Go 2 squares right of the line: 5 + 2 = 7. y stays 4.", "(7, 4)") +
        "<h2>Rotations: turn about a point</h2>"
        "<p>A <b>rotation</b> turns a shape about a fixed point, the <b>centre of rotation</b>. A quarter turn is 90°, a half turn is 180°. "
        "<b>Clockwise</b> is the way the hands of a clock go; <b>anticlockwise</b> is the other way.</p>"
        "<figure class='sn-fig'>" + rotf +
        "<figcaption>A quarter turn clockwise about O: the side from O to (8, 3) pointed right and now points down, to (5, 0). O does not move.</figcaption></figure>" +
        table(["Turn", "Right becomes", "Up becomes"], [
            ["quarter turn clockwise", "down", "right"],
            ["quarter turn anticlockwise", "up", "left"],
            ["half turn", "left", "down"],
        ]) +
        "<h2>What changes and what stays the same</h2>"
        "<p>After a translation, reflection or rotation the shape is in a new place, but it is the <b>same shape and size</b>. "
        "Side lengths, angles, perimeter and area stay the same. A reflection faces the other way; a rotation is turned.</p>"
        "<p>A shape has <b>line symmetry</b> if it can be folded so the two halves match exactly. It has <b>rotational symmetry</b> if it fits onto "
        "its outline before a full turn. A square has 4 lines of symmetry and fits onto itself 4 times in a full turn (order 4). "
        "A rectangle has only 2 lines of symmetry: the diagonals are not lines of symmetry.</p>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping x and y: (2, 5) plotted as 5 across, 2 up", "Across first, then up"],
            ["Counting grid lines, starting with 1 on the start line", "Count the squares you jump"],
            ["Reflecting by sliding: the image points the same way", "Flip it: the image must face the other way"],
            ["Turning the wrong way, or a half turn instead of a quarter turn", "Clockwise: right becomes down. A quarter turn is 90°"],
            ["Thinking the shape gets bigger or smaller", "Check every side is the same length as before"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about transformations in the Australian Curriculum?",
     "a": "In Year 5 (AC9M5SP03) students describe and perform translations, reflections and rotations of shapes, recognise what changes and what "
          "stays the same, and identify symmetries. They also use grid coordinates and directional language to describe position and movement (AC9M5SP02)."},
    {"q": "What is the difference between a translation, a reflection and a rotation?",
     "a": "A translation slides a shape, so it still faces the same way. A reflection flips it in a mirror line, and a rotation turns it about a point."},
    {"q": "How do you rotate a shape a quarter turn clockwise?",
     "a": "Keep the centre of rotation still and turn the shape 90° the way clock hands move, so a side that pointed right now points down. "
          "Tracing paper helps: trace the shape, hold the centre with a pencil and turn."},
    {"q": "Does a shape change size when it is translated, reflected or rotated?",
     "a": "No. Only its position and the way it faces can change. The side lengths, angles, perimeter and area stay exactly the same."},
]


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


def gen_unit():
    rnd = random.Random(5815)
    P = People(rnd)
    sets = [set_coords(rnd, P), set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P), set_same(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "coordinates-and-transformations", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Coordinates and Transformations: Translate, Reflect and Rotate",
        "seo_title": "Year 5 Coordinates and Transformations Worksheets: Translations, Reflections, Rotations and Symmetry (Free, Answer Key)",
        "short_title": "Coordinates and transformations",
        "domain": "Space",
        "standard_code": "AC9M5SP03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Describe and perform translations, reflections and rotations of shapes, using dynamic geometric software where appropriate; recognise what changes and what remains the same, and identify any symmetries",
        "meta_desc": "Free Year 5 maths worksheets on coordinates and transformations for the Australian Curriculum (AC9M5SP03, AC9M5SP02): read and plot coordinates, translate, reflect and rotate shapes on a grid, and find line and rotational symmetry. 100 questions with an answer key, good NAPLAN practice.",
        "key_big": "Translate = slide, reflect = flip, rotate = turn. The shape stays the same size.",
        "key_sub": "Coordinates: across first, then up. Count squares, not lines. A quarter turn clockwise turns right into down; a reflection lands the same distance on the other side of the mirror line.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (every grid) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(coordinate grid|four grid pictures|four shapes)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
