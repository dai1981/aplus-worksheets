# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Reflection and translation (National Curriculum in England,
Year 5: Geometry - position and direction)
  python3 tools/gen_uk_maths_y5_reflection_translation.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10. Mirror lines are vertical (x = m) or
horizontal (y = m) and are drawn on the grid as a dashed purple line with their name.
Every grid is drawn exactly. Letter labels sit in the middle of a grid square next to their own
point, never in a square that touches another point and never on a line, note or other label
(checked in Grid.render).
Wrong answers come from real Year 5 mistakes: counting grid lines including the start (1 too far),
moving the wrong way, swapping x and y, changing only one coordinate, stopping on the mirror line,
reflecting across instead of up/down, sliding a shape instead of flipping it, changing the size.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
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
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
LETTERS = ["A", "B", "C", "D"]
MOVES = ["a translation", "a reflection", "it got bigger", "it got smaller"]
CHECK = ["Yes, it is correct", "No: it is too far from the line", "No: it was slid, not flipped", "No: it is bigger"]


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
    """Where pupils land by mistake: wrong way, x/y moves mixed up, only one number changed."""
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
    (("v", 4), 8, 5, ["....", ".#..", ".#..", ".##.", "...."], ["slide", "far", "bigger"]),
    (("h", 4), 6, 8, ["......", ".#....", ".###..", "......"], ["slide", "turn", "far"]),
    (("v", 4), 8, 5, ["....", "###.", "#...", "#...", "...."], ["slide", "turn", "bigger"]),
    (("h", 4), 6, 8, ["......", "..##..", "...#..", "...#.."], ["turn", "far", "bigger"]),
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


# ------------------------------------------------------------ set 1: describe a translation
def set_describe(rnd, P):
    its = []
    for i, (a, b) in enumerate([((2, 3), (5, 1)), ((6, 2), (3, 6)), ((1, 1), (7, 4)), ((8, 7), (4, 2)),
                                ((3, 6), (3, 1)), ((2, 5), (9, 5))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    shapes = [
        ("triangle", [(1, 5), (4, 5), (1, 8)], 5, -4, None),
        ("rectangle", [(1, 1), (4, 1), (4, 3), (1, 3)], 4, 4, None),
        ("L-shape", [(6, 5), (9, 5), (9, 6), (7, 6), (7, 8), (6, 8)], -5, -4, (6.5, 5.5)),
        ("trapezium", [(1, 4), (5, 4), (4, 6), (2, 6)], 4, -3, None),
        ("square", [(2, 6), (4, 6), (4, 8), (2, 8)], 0, -5, None),
    ]
    for i, (kind, A, dx, dy, at) in enumerate(shapes):
        B = shift(A, dx, dy)
        G = Grid(10, 8 if max(p[1] for p in A + B) <= 8 else 9)
        G.poly(A, GREEN, "A", at).poly(B, BLUE, "B", (at[0] + dx, at[1] + dy) if at else None)
        k = 0
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                       "Shape A is translated to shape B. Describe the translation.", mv(dx, dy), describe_cands(dx, dy, i + 1),
                       "Follow one corner. The corner of A at %s moves to %s in B. That is %s. Every corner moves the same way."
                       % (pair(*A[k]), pair(*B[k]), mv_long(dx, dy)), rnd))
    for i, (a, b) in enumerate([((2, 7), (8, 3)), ((9, 1), (5, 6)), ((4, 4), (4, 9)), ((7, 8), (1, 8))]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq("A corner of a shape moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(dx, dy, i + 2), describe_e(a, b, "The start", "the end"), rnd))
    n, he, his = P.next()
    its.append(mcq("Point A is at (2, 4) and point B is at (6, 4). %s counts the grid lines from A to B, starting with 1 on A’s line. "
                   "%s says A moved 5 right. What is the correct translation?" % (n, he.capitalize()),
                   "4 right", ["5 right", "4 left", "6 right"],
                   "Count the squares you jump, not the lines: 6 − 2 = 4. %s counted the line A starts on, so %s got 1 too many." % (n, he), rnd))
    n, he, his = P.next()
    its.append(mcq("%s describes the move from (1, 6) to (5, 2) as “4 right, 4 up”. What mistake did %s make?" % (n, he),
                   "%s should have said down, not up" % he.capitalize(),
                   ["%s should have said left, not right" % he.capitalize(), "%s swapped the numbers" % he.capitalize(),
                    "No mistake: %s is right" % he],
                   "y goes from 6 to 2. It gets smaller, so the move is down: 6 − 2 = 4 down. The translation is 4 right, 4 down.", rnd))
    its.append(mcq("Which word means sliding a shape without turning it or flipping it?", "translation",
                   ["reflection", "rotation", "symmetry"],
                   "A translation slides a shape left or right and up or down. A reflection flips it in a mirror line.", rnd))
    its.append(mcq("A shape is translated 3 squares left and 2 squares up. Which translation moves it back to where it started?",
                   "3 right, 2 down", ["3 left, 2 up", "2 right, 3 down", "3 right, 2 up"],
                   "Undo each move: 3 left is undone by 3 right, and 2 up is undone by 2 down.", rnd))
    its.append(mcq("To describe the translation of a shape, which corner should you follow?",
                   "Any corner: they all move the same way",
                   ["Only the corner nearest (0, 0)", "Only the top corner", "You must add up every corner’s move"],
                   "In a translation every corner moves by the same amount in the same direction. Follow one corner and count the squares.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Describe a translation", "items": its}


# ------------------------------------------------------------ set 2: coordinates after a translation
def set_after(rnd, P):
    its = []
    pos = Pos(rnd)
    for i, (p, dx, dy) in enumerate([((3, 4), 2, 3), ((2, 7), 5, -4), ((8, 3), -6, 2), ((5, 9), -3, -6),
                                     ((1, 2), 0, 6), ((9, 6), -5, 0)]):
        q = (p[0] + dx, p[1] + dy)
        assert inside(q)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    for p, dx, dy in [((2, 6), 4, -3), ((7, 2), -5, 4), ((1, 1), 6, 5), ((8, 7), -3, -5)]:
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
    for i, (shape, p, dx, dy) in enumerate([
        ("A triangle has corners at (1, 2), (4, 2) and (1, 6).", (4, 2), 5, 1),
        ("A rectangle has corners at (3, 5), (8, 5), (8, 9) and (3, 9).", (8, 9), -2, -4),
        ("A square has corners at (6, 1), (9, 1), (9, 4) and (6, 4).", (6, 4), -4, 5),
    ]):
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("%s It is translated %s. What are the new coordinates of the corner at %s?" % (shape, mv_long(dx, dy), pair(*p)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i + 1)],
                       move_e(p, dx, dy) + " Every corner moves in the same way.", rnd))
    tri = [(2, 1), (5, 1), (2, 3)]
    its.append(mcq("A triangle has corners at %s. It is translated 3 squares right and 4 squares up. Which list shows the new corners?" % plist(tri),
                   plist(shift(tri, 3, 4)),
                   [plist(shift(tri, 3, 0)), plist(shift(tri, 4, 3)), plist([(5, 5), (5, 1), (2, 3)])],
                   "Add 3 to every x-coordinate and 4 to every y-coordinate: %s. Move every corner, not just one."
                   % ", ".join("%s → %s" % (pair(*a), pair(*b)) for a, b in zip(tri, shift(tri, 3, 4))), rnd))
    rect = [(5, 6), (8, 6), (8, 8), (5, 8)]
    its.append(mcq("A rectangle has corners at %s. It is translated 4 squares left and 5 squares down. Which list shows the new corners?" % plist(rect),
                   plist(shift(rect, -4, -5)),
                   [plist(shift(rect, -5, -4)), plist(shift(rect, -4, 0)), plist(shift(rect, -5, -6))],
                   "Take 4 from every x-coordinate and 5 from every y-coordinate. For example, (5, 6) → (1, 1) and (8, 8) → (4, 3).", rnd))
    its.append(mcq("Point B is translated 4 squares right and 3 squares up. It lands on (6, 8). Where did it start?", "(2, 5)",
                   ["(10, 11)", "(3, 4)", "(2, 8)"],
                   "Work backwards and undo each move. 4 right is undone by 4 left: 6 − 4 = 2. 3 up is undone by 3 down: 8 − 3 = 5. B started at (2, 5).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (6, 4) 2 squares left and gets (8, 4). What mistake did %s make?" % (n, he),
                   "%s moved right, not left" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake: %s is right" % he],
                   "Moving left makes the x-coordinate smaller: 6 − 2 = 4. The correct answer is (4, 4). %s added 2, which is a move to the right." % n, rnd))
    its.append(mcq("A point is translated left or right. Which coordinate changes?", "only the x-coordinate",
                   ["only the y-coordinate", "both coordinates", "neither coordinate"],
                   "Left and right is the x direction. The point does not move up or down, so the y-coordinate stays the same.", rnd))
    its.append(mcq("Point C is at (2, 6). It is translated 2 squares left. What are its new coordinates?", "(0, 6)",
                   ["(4, 6)", "(2, 4)", "(1, 6)"],
                   "Left 2 changes only x: 2 − 2 = 0. y stays 6. The point lands on the y-axis at (0, 6).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (5, 2) 3 squares up, then 4 squares right. Where does the point end?" % n, "(9, 5)",
                   ["(8, 6)", "(1, 5)", "(9, 2)"],
                   "Do one move at a time. Up 3: (5, 5). Right 4: (9, 5). The order of the two moves does not change the end point.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Coordinates after a translation", "items": its}


# ------------------------------------------------------------ set 3: reflect in a mirror line
def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, line in [((3, 4), ("v", 5)), ((8, 2), ("v", 6)), ((2, 1), ("h", 3)), ((6, 9), ("h", 6)),
                    ((1, 7), ("v", 4)), ((5, 3), ("h", 5))]:
        r = reflect(p, line)
        assert inside(r)
        its.append(mcq("Reflect the point %s in %s. What are the coordinates of the image?" % (pair(*p), lword(line)),
                       pair(*r), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line), rnd))
    for p, line, pick in [((2, 3), ("v", 4), ["far", "stop", "wrong"]), ((7, 5), ("v", 5), ["far", "stop", "swap"]),
                          ((3, 1), ("h", 3), ["far", "stop", "swap"]), ((5, 6), ("h", 4), ["far", "stop", "wrong"]),
                          ((8, 2), ("v", 6), ["stop", "far", "swap"])]:
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
    its.append(mcq("A point is reflected in a horizontal mirror line. Which coordinate changes?", "only the y-coordinate",
                   ["only the x-coordinate", "both coordinates", "neither coordinate"],
                   "A horizontal mirror line goes across. The point flips up or down over it, so only y changes. x stays the same.", rnd))
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
    r = reflect((1, 5), line)
    its.append(mcq("A rectangle has corners at %s. It is reflected in %s. What are the new coordinates of the corner at (1, 5)?"
                   % (plist(rect), lword(line)), pair(*r), [pair(*q) for q, w, k in refl_kinds((1, 5), line)],
                   refl_e((1, 5), line, "The corner"), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflect in a mirror line", "items": its}


# ------------------------------------------------------------ set 4: translation or reflection?
def set_which(rnd, P):
    its = []
    cases = [
        ([(1, 1), (4, 1), (1, 4)], [(6, 4), (9, 4), (6, 7)], "a translation", None,
         "B points the same way as A. Every corner moved 5 squares right and 3 squares up, for example (1, 1) → (6, 4). That is a translation."),
        ([(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)], [reflect(p, ("v", 5)) for p in [(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)]],
         "a reflection", ((1.5, 2.5), (8.5, 2.5)),
         "B is a mirror image of A: the foot of the L points the other way. It is a reflection in the line x = 5. The size has not changed."),
        ([(6, 1), (7, 1), (7, 3), (9, 3), (9, 5), (6, 5)], shift([(6, 1), (7, 1), (7, 3), (9, 3), (9, 5), (6, 5)], -5, 2),
         "a translation", ((6.5, 2), (1.5, 4)),
         "B faces the same way as A and is the same size. Every corner moved 5 squares left and 2 squares up. That is a translation."),
        ([(2, 5), (6, 5), (2, 7)], [reflect(p, ("h", 4)) for p in [(2, 5), (6, 5), (2, 7)]], "a reflection", None,
         "B is A flipped upside down over the line y = 4: the right angle is now at the top. That is a reflection."),
        ([(1, 1), (3, 1), (1, 3)], [(5, 2), (9, 2), (5, 6)], "it got bigger", None,
         "The sides of A are 2 squares long. The sides of B are 4 squares long. A translation or a reflection never changes the size."),
        ([(1, 4), (5, 4), (5, 6), (1, 6)], [(7, 1), (9, 1), (9, 2), (7, 2)], "it got smaller", None,
         "A is 4 squares by 2 squares. B is only 2 squares by 1 square, so B is smaller. It is not a translation or a reflection."),
    ]
    for A, B, ans, at, e in cases:
        G = Grid(10, 8)
        G.poly(A, GREEN, "A", at[0] if at else None).poly(B, BLUE, "B", at[1] if at else None)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) +
                             "What happened to shape A to make shape B?", MOVES, ans, e))
    checks = [
        ([(1, 2), (4, 2), (1, 5)], [(9, 2), (6, 2), (9, 5)], ("v", 5), CHECK[0],
         "Each corner of B is the same distance from the line x = 5 as its partner in A: (1, 2) is 4 squares left of the line and (9, 2) is 4 squares right. B is correct."),
        ([(1, 1), (4, 1), (1, 3)], [(1, 8), (4, 8), (1, 6)], ("h", 4), CHECK[1],
         "(1, 1) is 3 squares below the line y = 4, so its image should be 3 squares above, at (1, 7). B is at (1, 8): 1 square too far."),
        ([(1, 2), (4, 2), (3, 5), (1, 5)], [(6, 2), (9, 2), (8, 5), (6, 5)], ("v", 5), CHECK[2],
         "In A the sloping side is on the right. In B it is also on the right, so B points the same way: it was slid. A mirror image would have the sloping side on the left."),
        ([(2, 1), (4, 1), (2, 3)], [(9, 1), (6, 1), (9, 4)], ("v", 5), CHECK[3],
         "The sides of A are 2 squares long, but the sides of B are 3 squares long. A reflection never changes the size."),
    ]
    for A, B, line, ans, e in checks:
        G = Grid(10, 8)
        G.mirror(*line)
        G.poly(A, GREEN, "A").poly(B, BLUE, "B")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with a mirror line, shape A and shape B")) +
                             "%s wants to reflect shape A in the dashed mirror line. Is shape B correct?" % P.next()[0], CHECK, ans, e))
    t = [(1, 1), (3, 1), (1, 4)]
    its.append(mcq_fixed("A triangle with corners at %s moves to %s. What happened?" % (plist(t), plist(shift(t, 4, 0))),
                         MOVES, "a translation",
                         "Every corner moved 4 squares right and the y-coordinates stayed the same. The triangle faces the same way: a translation."))
    tr = [reflect(p, ("v", 4)) for p in t]
    its.append(mcq_fixed("A triangle with corners at %s moves to %s. What happened?" % (plist(t), plist(tr)),
                         MOVES, "a reflection",
                         "(1, 1) moved 6 squares but (3, 1) moved only 2, so it is not a slide. Each corner is the same distance from x = 4 "
                         "on the other side: a reflection in the line x = 4."))
    its.append(mcq("A rectangle is 4 squares long and 2 squares wide. It is translated 3 squares right. How long is the image?",
                   "4 squares", ["7 squares", "1 square", "8 squares"],
                   "A translation only moves the shape. It does not stretch it, so the image is still 4 squares long and 2 squares wide.", rnd))
    its.append(mcq("A triangle has an angle of 35°. The triangle is reflected in a mirror line. What is that angle in the image?", "35°",
                   ["70°", "145°", "55°"],
                   "A reflection flips the shape but does not change it. Every angle stays the same, so the angle is still 35°.", rnd))
    its.append(mcq("A rectangle has a perimeter of 14 cm. It is translated 5 cm to the right. What is the perimeter of the image?", "14 cm",
                   ["19 cm", "9 cm", "28 cm"],
                   "The sides do not change length when a shape slides, so the perimeter stays 14 cm. The 5 cm is how far it moved, not a side.", rnd))
    its.append(mcq("Which of these changes when a shape is translated?", "its position",
                   ["its size", "its angles", "its side lengths"],
                   "A translation moves the shape to a new place. The size, side lengths and angles stay the same.", rnd))
    its.append(mcq("Which sentence is true after a reflection?", "The image is the same size, but flipped",
                   ["The image is bigger than the shape", "The image faces the same way", "The angles get smaller"],
                   "A reflection makes a mirror image. It faces the other way, but its size, sides and angles have not changed.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s reflects a shape. %s says the image is smaller because it is further from (0, 0). Is %s right?"
                   % (n, he.capitalize(), he),
                   "No: a reflection never changes the size",
                   ["Yes: further away means smaller", "Yes: reflections always shrink shapes", "Only if the mirror line is far away"],
                   "Moving a shape to a new place does not change its size. Count the squares along each side: they are the same.", rnd))
    its.append(mcq("A right-angled triangle is reflected in a mirror line. Does the image have a right angle?",
                   "Yes: the angles stay the same",
                   ["No: the right angle is lost", "Only if the mirror line is vertical", "Only if the shape is translated"],
                   "Reflecting flips the triangle, but every angle stays the same size. The right angle is still a right angle, it just faces the other way.", rnd))
    its.append(mcq("How can you tell a reflection from a translation?", "A reflection is flipped; a translation faces the same way",
                   ["A reflection is always bigger", "A translation is always upside down", "A translation is always further away"],
                   "Both keep the size and the angles. In a translation the shape slides and still points the same way. In a reflection it is a mirror image.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translation or reflection? The shape has not changed", "items": its}


# ------------------------------------------------------------ set 5: problems
BED = [(1, 4), (3, 4), (3, 8), (1, 8)]
DESK = [(6, 1), (9, 1), (9, 2), (6, 2)]
WARD = [(7, 6), (9, 6), (9, 8), (7, 8)]
LOGO = [(5, 1), (3, 1), (1, 4), (3, 7), (5, 7)]


def plan_fig():
    G = Grid(10, 8)
    G.poly(BED, GREEN, "bed", (2, 6)).poly(DESK, BLUE, "desk", (7.5, 1.5)).poly(WARD, RED, "W", (8, 7))
    return fig(G.svg("plan of a bedroom on a coordinate grid"))


def logo_fig():
    G = Grid(10, 8)
    G.mirror("v", 5)
    G.poly(LOGO, GREEN)
    for p in [(1, 4), (3, 7), (3, 1)]:
        G.point(p[0], p[1], None, GREEN)
    return fig(G.svg("coordinate grid with half of a logo and the mirror line x = 5"))


def set_problems(rnd, P):
    its = []
    pf = plan_fig()
    pkey = "The plan shows Amelia’s bedroom: a bed, a desk and a wardrobe (W). "
    its.append(mcq(pf + pkey + "The bed is translated 4 squares right. What are the new coordinates of its bottom-left corner?", "(5, 4)",
                   ["(1, 8)", "(6, 4)", "(4, 5)"],
                   "The bottom-left corner of the bed is at (1, 4). Right 4 changes only x: 1 + 4 = 5. The corner moves to (5, 4).", rnd))
    its.append(mcq(pf + pkey + "The desk is translated so that its bottom-left corner is at (2, 1). Describe the translation.", mv(-4, 0),
                   describe_cands(-4, 0), describe_e((6, 1), (2, 1), "The corner", "the new corner"), rnd))
    its.append(mcq(pf + pkey + "The wardrobe is translated 3 squares left and 1 square down. What are the new coordinates of its top-left corner?",
                   "(4, 7)", ["(10, 7)", "(4, 9)", "(7, 4)"],
                   "The top-left corner of the wardrobe is at (7, 8). Left 3: 7 − 3 = 4. Down 1: 8 − 1 = 7. It moves to (4, 7).", rnd))
    new_bed = shift(BED, 3, -1)
    its.append(mcq(pf + pkey + "Amelia moves the bed. Its corners are now at %s. Describe the translation." % plist(new_bed), mv(3, -1),
                   describe_cands(3, -1), describe_e(BED[0], new_bed[0], "The bottom-left corner of the bed", "the new corner"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a board game, %s’s counter is at (2, 3). %s moves it 5 squares right and 4 squares up. Where does it land?" % (n, he.capitalize()),
                   "(7, 7)", [pair(*c) for c in move_cands((2, 3), 5, 4, 1)], move_e((2, 3), 5, 4), rnd))
    n, he, his = P.next()
    its.append(mcq("In a board game, %s’s counter moves from (6, 6) to (1, 2). Describe the move." % n, mv(-5, -4),
                   describe_cands(-5, -4), describe_e((6, 6), (1, 2), "The start", "the end"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a game, each turn moves a counter 3 squares right or 3 squares up. %s’s counter starts at (1, 1). "
                   "%s has 2 turns right and 1 turn up. Where is the counter now?" % (n, he.capitalize()), "(7, 4)",
                   ["(4, 7)", "(3, 2)", "(7, 1)"],
                   "2 turns right is 2 × 3 = 6 squares right: 1 + 6 = 7. 1 turn up is 3 squares up: 1 + 3 = 4. The counter is at (7, 4).", rnd))
    n, he, his = P.next()
    its.append(mcq("In a computing lesson, %s’s robot starts at (2, 5). It moves 4 squares right, then 3 squares down, then 1 square left. "
                   "Where does it stop?" % n, "(5, 2)", ["(7, 2)", "(5, 8)", "(6, 2)"],
                   "Follow one move at a time. Right 4: (6, 5). Down 3: (6, 2). Left 1: (5, 2).", rnd))
    its.append(mcq("On a game board, a counter at (1, 6) is reflected in the vertical mirror line x = 4. Where does it land?", "(7, 6)",
                   [pair(*q) for q, w, k in refl_kinds((1, 6), ("v", 4))], refl_e((1, 6), ("v", 4), "The counter at"), rnd))
    lf = logo_fig()
    lkey = "Half of a logo is drawn. The whole logo is symmetrical in the mirror line x = 5. "
    its.append(mcq(lf + lkey + "Which corner on the right matches the corner at (1, 4)?", "(9, 4)",
                   ["(10, 4)", "(5, 4)", "(4, 9)"],
                   refl_e((1, 4), ("v", 5), "The corner") + " (5, 4) is what you get by sliding the half across instead of flipping it.", rnd))
    its.append(mcq(lf + lkey + "Which corner on the right matches the corner at (3, 7)?", "(7, 7)",
                   ["(8, 7)", "(6, 7)", "(5, 7)"],
                   refl_e((3, 7), ("v", 5), "The corner"), rnd))
    its.append(mcq_num(lf + lkey + "How many squares wide is the whole logo?", 8, [4, 9, 10],
                       "The half goes from x = 1 to the mirror line at x = 5: 4 squares. The other half is the same, so 4 + 4 = 8 squares. "
                       "Count squares, not lines (that gives 9)."))
    its.append(mcq("A school logo is reflected in the horizontal mirror line y = 5 to make a pattern. Where does the corner at (3, 2) go?", "(3, 8)",
                   [pair(*q) for q, w, k in refl_kinds((3, 2), ("h", 5))], refl_e((3, 2), ("h", 5), "The corner"), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a house shape with its roof point at (2, 7). %s reflects the house in the mirror line x = 6. Where is the roof point of the image?"
                   % (n, he.capitalize()), "(10, 7)", [pair(*q) for q, w, k in refl_kinds((2, 7), ("v", 6))],
                   refl_e((2, 7), ("v", 6), "The roof point"), rnd))
    its.append(mcq("A shop sign is reflected in the mirror line x = 3. Where does the corner at (5, 6) go?", "(1, 6)",
                   [pair(*q) for q, w, k in refl_kinds((5, 6), ("v", 3))], refl_e((5, 6), ("v", 3), "The corner"), rnd))
    its.append(mcq("A row of tiles is made by translating a tile 3 squares right each time. The first tile has a corner at (1, 2). "
                   "Where is that corner on the 3rd tile?", "(7, 2)", ["(10, 2)", "(4, 2)", "(1, 8)"],
                   "Tile 1: (1, 2). Tile 2 is one move: (4, 2). Tile 3 is two moves: 1 + 3 + 3 = 7, so (7, 2). There are only 2 moves to get to the 3rd tile.", rnd))
    its.append(mcq("On a map, a lorry drives from (1, 5) to (8, 5), then 3 squares down. Where is it now?", "(8, 2)",
                   ["(8, 8)", "(5, 5)", "(11, 5)"],
                   "From (1, 5) to (8, 5) only x changes. Then down 3: 5 − 3 = 2. The lorry is at (8, 2).", rnd))
    pond = [(1, 2), (3, 2), (3, 4), (1, 4)]
    img = [reflect(p, ("v", 5)) for p in pond]
    its.append(mcq("A garden has a path along the line x = 5. A pond with corners at %s is reflected in the path to make a matching pond. "
                   "Which list shows the corners of the new pond?" % plist(pond), plist(img),
                   [plist(shift(img, 1, 0)), plist(shift(pond, 5, 0)), plist([reflect(p, ("h", 5)) for p in pond])],
                   "Each corner goes the same distance on the other side of x = 5: (1, 2) is 4 squares left, so its image is 4 squares right at (9, 2). "
                   "(3, 2) is 2 squares left, so its image is (7, 2).", rnd))
    its.append(mcq("In a game, a counter at (7, 3) is reflected in the horizontal line y = 4, then translated 2 squares left. Where does it end?",
                   "(5, 5)", ["(9, 5)", "(5, 3)", "(5, 6)"],
                   "Reflect first: (7, 3) is 1 square below y = 4, so the image is 1 square above, at (7, 5). Then left 2: 7 − 2 = 5. It ends at (5, 5).", rnd))
    its.append(mcq_num("A rug is 3 squares long and 2 squares wide. It is translated 4 squares across the floor plan. How many squares does it cover now?",
                       6, [12, 5, 10],
                       "The rug covers 3 × 2 = 6 squares. A translation does not change the size, so it still covers 6 squares.", fmt="%d squares"))
    assert len(its) == 20, len(its)
    return {"title": "Problems: plans, games and logos", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
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
    G = Grid(7, 8)
    G.mirror("h", 4)
    G.point(2, 1, "P", RED).point(2, 7, "Q", GREEN).point(5, 4, "R", GREEN, where=(1, 1))
    hor = G.svg("point P (2, 1) reflected in the mirror line y = 4 to Q (2, 7); point R on the line")
    return (
        "<h2>Translations: slide the shape</h2>"
        "<p>A <b>translation</b> slides a shape left or right and up or down. It does not turn or flip. "
        "Every corner moves the same number of squares in the same direction.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A is translated 4 squares right and 3 squares down to make B. Follow one corner: (4, 4) → (8, 1).</figcaption></figure>" +
        table(["Move", "What changes", "Example from (5, 4)"], [
            ["right 2", "x gets bigger", "(7, 4)"],
            ["left 2", "x gets smaller", "(3, 4)"],
            ["up 2", "y gets bigger", "(5, 6)"],
            ["down 2", "y gets smaller", "(5, 2)"],
        ]) +
        ex("Example", "Describe the translation from (2, 7) to (8, 3).",
           "Across: 2 to 8 is 6 squares right. Up and down: 7 to 3 is 4 squares down.", "6 squares right and 4 squares down") +
        "<h2>Reflections: flip in a mirror line</h2>"
        "<p>A <b>reflection</b> flips a shape over a mirror line. The image is a mirror image. "
        "Each corner ends up the <b>same distance</b> from the mirror line, on the other side.</p>"
        "<p>The line <b>x = 5</b> goes straight up through every point with x-coordinate 5. "
        "The line <b>y = 4</b> goes straight across through every point with y-coordinate 4.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>(1, 4) is 4 squares left of x = 5, so its image is 4 squares right, at (9, 4). In a vertical mirror line only x changes.</figcaption></figure>" +
        ex("Example", "Reflect (3, 4) in the mirror line x = 5.",
           "(3, 4) is 2 squares left of the line. Go 2 squares right of the line: 5 + 2 = 7. y stays 4.", "(7, 4)") +
        "<figure class='sn-fig'>" + hor +
        "<figcaption>P (2, 1) is 3 squares below y = 4, so its image Q is 3 squares above, at (2, 7). R is on the line, so it stays where it is.</figcaption></figure>" +
        "<h2>The shape has not changed</h2>"
        "<p>After a translation or a reflection, the shape is in a new place, but it is the <b>same shape and size</b>. "
        "The side lengths, the angles, the perimeter and the area all stay the same.</p>" +
        table(["", "Translation", "Reflection"], [
            ["What happens", "slides", "flips in a mirror line"],
            ["Which way it faces", "the same way", "the other way (mirror image)"],
            ["Size, sides and angles", "the same", "the same"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting grid lines, starting with 1 on the start line", "Count the squares you jump"],
            ["Reflecting by sliding: the image points the same way", "Flip it: the image must face the other way"],
            ["Moving the wrong way: adding for “left” or “down”", "Left and down make the number smaller"],
            ["Stopping on the mirror line, or going past it", "Go the same distance on the other side"],
            ["Drawing the image bigger or smaller", "Check every side is the same length as before"],
        ])
    )


FAQ = [
    {"q": "What do children learn about reflection and translation in Year 5?",
     "a": "Year 5 pupils reflect and translate shapes on a grid in the first quadrant. They describe the new position with coordinates "
          "and the right words, and know that the shape itself has not changed."},
    {"q": "How do you reflect a shape in a mirror line?",
     "a": "Reflect one corner at a time. Count how many squares it is from the mirror line, then count the same number on the other side. "
          "Join the new corners to draw the mirror image."},
    {"q": "What is the difference between a reflection and a translation?",
     "a": "A translation slides a shape, so it still faces the same way. A reflection flips it in a mirror line, so the image faces the other way."},
    {"q": "Does a shape change size when it is translated or reflected?",
     "a": "No. Only its position changes. The side lengths, angles, perimeter and area stay exactly the same."},
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
        while sum(need) > len(free):
            need[need.index(max(need))] -= 1
        while sum(need) < len(free):
            i = min(range(4), key=lambda j: cnt[j] + need[j])
            need[i] += 1
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(5516)
    P = People(rnd)
    sets = [set_describe(rnd, P), set_after(rnd, P), set_reflect(rnd, P), set_which(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "reflection-and-translation", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Reflection and Translation on a Coordinate Grid",
        "seo_title": "Year 5 Reflection and Translation Worksheets: Mirror Lines and Moves on a Grid",
        "short_title": "Reflection and translation",
        "domain": "Geometry – position and direction",
        "standard_code": "Year 5: Geometry – position and direction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Identify, describe and represent the position of a shape following a reflection or translation, using the appropriate language, and know that the shape has not changed.",
        "meta_desc": "Free Year 5 maths worksheets on reflection and translation: describe translations on a grid, find new coordinates, reflect points and shapes in vertical and horizontal mirror lines, and spot what stays the same. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "A translation slides a shape; a reflection flips it in a mirror line. The shape itself does not change.",
        "key_sub": "Count the squares you move, not the lines. In a reflection, each corner ends up the same distance from the mirror line, on the other side.",
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
        mark_large(u, "(coordinate grid|plan of|four grid pictures)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
