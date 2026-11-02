# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Coordinates and transformations (National Curriculum in England,
Year 6: Geometry - position and direction)
  python3 tools/gen_uk_maths_y6_coordinates.py
HTML attributes use single quotes (no backslashes in the JSON).

All four quadrants, whole-number coordinates from -6 to 6. Negative numbers use the real minus sign.
British English. Every grid is drawn exactly and is square: a point (x, y) sits x squares right
(left if x < 0) of the origin and y squares up (down if y < 0). Axis numbers, notes, dots, letter
labels and shape edges never overlap (checked in Grid.render).
Wrong answers come from real Year 6 mistakes: swapping x and y, sign errors when crossing an axis
(2 - 4 = 2 instead of -2; 4 - 3 = 1 instead of 4 + 3 = 7), moving the wrong way, a translation that
changes only one coordinate, reflecting in the wrong axis, changing both signs, counting grid lines
instead of squares, doing two transformations in the wrong order.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
LETTERS = ["A", "B", "C", "D"]
AXES = ["the x-axis", "the y-axis", "both axes", "neither axis"]
MOVES = ["reflected in the x-axis", "reflected in the y-axis", "translated", "reflected in both axes"]


# ------------------------------------------------------------ numbers and pairs
def num(v):
    return (MINUS + str(-v)) if v < 0 else str(v)


def pair(x, y):
    return "(%s, %s)" % (num(x), num(y))


def plist(pts):
    s = [pair(*p) for p in pts]
    return ", ".join(s[:-1]) + " and " + s[-1]


def sgn(v):
    return (v > 0) - (v < 0)


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def op(a, d):
    """'2 − 4 = −2' style working for a + d."""
    return "%s %s %d = %s" % (num(a), "+" if d > 0 else MINUS, abs(d), num(a + d))


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
    """Choices keep their order (A B C D, numbers from small to large, axis words)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_int(q, correct, cands, e, unit=""):
    """Whole-number answers (negative wrong answers allowed), shown from small to large."""
    ch = []
    for c in cands:
        if c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)

    def f(v):
        return num(v) + (unit[:-1] if abs(v) == 1 and unit.endswith("s") else unit)
    return mcq_fixed(q, [f(c) for c in ch], f(correct), e)


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


HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"


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


# ------------------------------------------------------------ four-quadrant grid
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


def seg_hits(p, q, box, m=1.5):
    """Does the straight line p-q (px) pass through the box (px)?"""
    n = 60
    for i in range(n + 1):
        t = i / float(n)
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if box[0] - m <= x <= box[2] + m and box[1] - m <= y <= box[3] + m:
            return True
    return False


class Grid:
    """Square grid from -R to R on both axes. One square = u px. Every axis number is written."""

    def __init__(self, R, u=22):
        assert 3 <= R <= 6
        self.R, self.u = R, u
        side = 2 * R * u
        self.ox = 24 + R * u
        self.oy = 34 + R * u
        self.W = self.H = int(math.ceil(24 + side + 34))
        self.pts, self.segs, self.arrows, self.notes, self.polys = [], [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and abs(x) <= self.R and abs(y) <= self.R, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def seg(self, a, b, col=GREEN, w=3, dash=False):
        """Any straight side (sloping sides are allowed: labels are checked against them)."""
        for p in (a, b):
            assert abs(p[0]) <= self.R and abs(p[1]) <= self.R, p
        self.segs.append((a, b, col, w, dash))
        return self

    def poly(self, pts, col=GREEN, name=None):
        """A filled shape. name is written at its centre."""
        for p in pts:
            assert abs(p[0]) <= self.R and abs(p[1]) <= self.R, p
        self.polys.append((pts, col))
        for i in range(len(pts)):
            self.seg(pts[i], pts[(i + 1) % len(pts)], col, 2.5)
        if name:
            cx = sum(p[0] for p in pts) / float(len(pts))
            cy = sum(p[1] for p in pts) / float(len(pts))
            self.note(cx, cy, name, col=col, fs=16)
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _edges(self):
        return [(self.P(*a), self.P(*b)) for a, b, col, w, dash in self.segs] + \
               [(self.P(*a), self.P(*b)) for a, b, col in self.arrows]

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not (abs(cx) <= self.R and abs(cy) <= self.R):
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
        u, ox, oy, R = self.u, self.ox, self.oy, self.R
        s = []
        lo, hi = -R * u, R * u
        for k in range(-R, R + 1):
            if k == 0:
                continue
            x = ox + k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, oy - hi, x, oy - lo, GRID))
            y = oy - k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ox + lo, y, ox + hi, y, GRID))
        for pts, col in self.polys:
            s.append("<polygon points='%s' fill='%s' fill-opacity='0.14' stroke='none'/>"
                     % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), col))
        x0, x1 = ox + lo - 14, ox + hi + 14
        y0, y1 = oy - hi - 14, oy - lo + 14
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 + 4, oy, x1 - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, y0 + 4, ox, y1 - 4, INK))
        for (ax, ay, dx, dy) in [(x1, oy, 1, 0), (x0, oy, -1, 0), (ox, y0, 0, -1), (ox, y1, 0, 1)]:
            bx, by = ax - dx * 9, ay - dy * 9
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (ax, ay, bx - dy * 4.5, by + dx * 4.5, bx + dy * 4.5, by - dx * 4.5, INK))
        s.append(text(x1 + 3, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox + 12, y0 + 8, "y", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        assert x1 + 3 + 10 <= self.W and y0 - 4 >= 0
        boxes, nums = [], []
        for k in range(-R, R + 1):
            if k == 0:
                continue
            t = num(k)
            w = tw(t, 14)
            cx = ox + k * u
            boxes.append((cx - w / 2, oy + 5, cx + w / 2, oy + 15.5))
            nums.append(text(cx, oy + 15.5, t, 14, extra=HALO))
            cy = oy - k * u
            boxes.append((ox - 6 - w, cy - 5, ox - 6, cy + 5))
            nums.append(text(ox - 6, cy + 5, t, 14, anchor="end", extra=HALO))
        # no "0" at the origin: next to the x-axis "−1" it would read as "−10"
        for a, b, col, w, dash in self.segs:
            p, q = self.P(*a), self.P(*b)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'%s/>"
                     % (p[0], p[1], q[0], q[1], col, w, " stroke-dasharray='6 5'" if dash else ""))
        for a, b, col in self.arrows:
            p, q = self.P(*a), self.P(*b)
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            d = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
            e = (q[0] - d[0] * 10, q[1] - d[1] * 10)
            n = (-d[1], d[0])
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (p[0], p[1], e[0] + d[0] * 2, e[1] + d[1] * 2, col))
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (q[0], q[1], e[0] + n[0] * 5.5, e[1] + n[1] * 5.5, e[0] - n[0] * 5.5, e[1] - n[1] * 5.5, col))
        s.extend(nums)
        edges = self._edges()
        for gx, gy, t, anchor, col, fs in self.notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0_ = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0_, c[1] - fs * 0.4, x0_ + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("note overlaps", t)
            for p, q in edges:
                assert not seg_hits(p, q, box, 0.5), ("note on a line", t)
            boxes.append(box)
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col, extra=HALO))
        allpts = {(p[0], p[1]) for p in self.pts}
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            dot = (c[0] - 4.5, c[1] - 4.5, c[0] + 4.5, c[1] + 4.5)
            for b in boxes:
                assert not overlap(dot, b, 0), ("dot on a number or note", x, y)
        used = set()
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (c[0], c[1], col))
            if name:
                lc, box = self._label_cell(x, y, used, allpts - {(x, y)}, boxes, where)
                boxes.append(box)
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=col if col == RED else INK))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def grid_for(pts, lo=4):
    R = max(lo, max(max(abs(p[0]), abs(p[1])) for p in pts) + 1)
    return Grid(min(R, 6))


def pts_grid(pts, label="coordinate grid", ref=None):
    """pts: (x, y, name). ref: name of a point drawn in red (the starting point)."""
    G = grid_for(pts)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


def pick_letters(target, others, pos):
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    assert len(set(cells)) == 4, cells
    return [(c[0], c[1], LETTERS[k]) for k, c in enumerate(cells)], LETTERS[p]


# ------------------------------------------------------------ explanations and mistakes
def walk(x, y):
    a = "go 0 left or right" if x == 0 else ("go %d right" % x if x > 0 else "go %d left" % -x)
    b = "0 up or down" if y == 0 else ("%d up" % y if y > 0 else "%d down" % -y)
    return "Start at the origin, %s, then %s" % (a, b)


def read_cands(x, y):
    out = []
    for c in [(y, x), (abs(x), abs(y)), (-x, y), (x, -y), (-x, -y), (-y, -x)]:
        if c != (x, y) and c not in out:
            out.append(c)
    return [pair(*c) for c in out]


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


def sign_slip(a, d):
    """The answer a pupil gets when crossing 0 by mistake: 2 − 4 = 2, −3 + 5 = −2 (the sign is wrong)."""
    r = a + d
    if a != 0 and r != 0 and sgn(a) != sgn(r):
        return -r
    return r


def move_cands(p, dx, dy, i=0):
    """Where pupils land by mistake: sign slip at an axis, wrong way, moves swapped, only one coordinate changed."""
    x, y = p
    q = (x + dx, y + dy)
    first = [(sign_slip(x, dx), sign_slip(y, dy))]
    c = [(x - dx, y + dy), (x + dx, y - dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (q[1], q[0])]
    c = c[i % 4:] + c[:i % 4]
    return [pair(*v) for v in first + c if v != q and v != p]


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %d changes x: %s" % ("Right" if dx > 0 else "Left", abs(dx), op(x, dx)))
    else:
        parts.append("x stays %s" % num(x))
    if dy:
        parts.append("%s %d changes y: %s" % ("Up" if dy > 0 else "Down", abs(dy), op(y, dy)))
    else:
        parts.append("y stays %s" % num(y))
    s = ". ".join(parts) + ". The new point is %s." % pair(*q)
    if (x and q[0] and sgn(x) != sgn(q[0])) or (y and q[1] and sgn(y) != sgn(q[1])):
        s += " When you cross an axis, count to 0 first, then keep going."
    return s


def describe_cands(a, b, i=0):
    """Wrong descriptions: subtracted the sizes across an axis, numbers swapped, wrong way, one too many."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    out = []
    sx = sgn(dx) * abs(abs(b[0]) - abs(a[0])) if a[0] * b[0] < 0 else dx
    sy = sgn(dy) * abs(abs(b[1]) - abs(a[1])) if a[1] * b[1] < 0 else dy
    if (sx, sy) != (dx, dy) and (sx or sy):
        out.append(mv(sx, sy))
    rest = []
    if dx and dy:
        rest.append("%d %s, %d %s" % (abs(dy), "right" if dx > 0 else "left", abs(dx), "up" if dy > 0 else "down"))
    rest += [mv(-dx, dy), mv(dx, -dy), mv(dx + sgn(dx), dy + sgn(dy)), mv(-dx, -dy)]
    rest = rest[i % 3:] + rest[:i % 3]
    return [c for c in out + rest if c and c != mv(dx, dy)]


def across(v, w, word_pos, word_neg):
    d = w - v
    s = "%s to %s is %s %s" % (num(v), num(w), sq(abs(d)), word_pos if d > 0 else word_neg)
    if v * w < 0:
        s += " (%d to the axis, then %d more)" % (abs(v), abs(w))
    return s


def describe_e(a, b, na="A", nb="B"):
    dx, dy = b[0] - a[0], b[1] - a[1]
    s = "%s is at %s and %s is at %s. " % (na, pair(*a), nb, pair(*b))
    s += ("Across: %s. " % across(a[0], b[0], "right", "left")) if dx else "x stays %s, so there is no move left or right. " % num(a[0])
    s += ("Up and down: %s." % across(a[1], b[1], "up", "down")) if dy else "y stays %s, so there is no move up or down." % num(a[1])
    return s


def reflect(p, axis):
    return (p[0], -p[1]) if axis == "x" else (-p[0], p[1])


def refl_e(p, axis):
    r = reflect(p, axis)
    if r == p:
        return ("%s is on the %s-axis, the mirror line itself, so it does not move: %s."
                % (pair(*p), axis, pair(*r)))
    if axis == "x":
        return ("In the x-axis, the point flips up or down: x stays %s and y changes sign, %s → %s. The image is %s."
                % (num(p[0]), num(p[1]), num(-p[1]), pair(*r)))
    return ("In the y-axis, the point flips left or right: y stays %s and x changes sign, %s → %s. The image is %s."
            % (num(p[1]), num(p[0]), num(-p[0]), pair(*r)))


def length_e(a, b):
    """Length of a horizontal or vertical side, with the working across an axis."""
    if a[0] == b[0]:
        k, v, w, ax = "x", a[1], b[1], "x-axis"
    else:
        assert a[1] == b[1]
        k, v, w, ax = "y", a[0], b[0], "y-axis"
    d = abs(v - w)
    same = "Both points have %s = %s. " % (k, num(a[0] if k == "x" else a[1]))
    if v == 0 or w == 0:
        return same + "One point is on the %s, so the length is %d." % (ax, d), d
    if (v > 0) != (w > 0):
        return same + ("They are on opposite sides of the %s: %d to the axis, then %d more. %d + %d = %d."
                       % (ax, abs(v), abs(w), abs(v), abs(w), d)), d
    return same + ("They are on the same side of the %s: %d − %d = %d." % (ax, max(abs(v), abs(w)), min(abs(v), abs(w)), d)), d


def vertex_cands(D, given):
    out = []
    for c in [(D[1], D[0]), (D[0], -D[1]), (-D[0], D[1]), (-D[0], -D[1]), (-D[1], -D[0]), (D[0] + 1, D[1] + 1)]:
        if c != D and c not in given and c not in out:
            out.append(c)
    return [pair(*c) for c in out]


# ------------------------------------------------------------ set 1: read and plot points
def set_read(rnd, P):
    its = []
    pos = Pos(rnd)
    reads = [
        [(-2, 5, "A")], [(4, -3, "B")], [(-5, -2, "C"), (-2, -5, "D")], [(3, -6, "E")],
        [(-4, 1, "F"), (1, -4, "G")], [(-6, -3, "H")], [(0, -5, "J"), (4, 2, "K")], [(-3, 0, "M")],
    ]
    for pts in reads:
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. The x-coordinate comes first; a minus sign means left or down." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y), e, rnd))
    its.append(mcq_int(fig(pts_grid([(-5, 3, "P")], "coordinate grid with labelled points")) +
                       "What is the x-coordinate of point P?", -5, [5, 3, -3],
                       "Point P is 5 squares to the left of the y-axis, so x = %s. Left means negative. (3 is its y-coordinate.)" % num(-5)))
    its.append(mcq_int(fig(pts_grid([(2, -4, "Q")], "coordinate grid with labelled points")) +
                       "What is the y-coordinate of point Q?", -4, [4, 2, -2],
                       "Point Q is 4 squares below the x-axis, so y = %s. Down means negative. (2 is its x-coordinate.)" % num(-4)))
    for (x, y), others in [
        ((-4, 3), [(3, -4), (4, 3), (-4, -3)]),
        ((3, -5), [(-5, 3), (-3, -5), (3, 5)]),
        ((-2, -5), [(-5, -2), (2, -5), (-2, 5)]),
        ((-5, 1), [(1, -5), (5, 1), (-5, -1)]),
        ((0, 4), [(4, 0), (0, -4), (-4, 4)]),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are swapped." % (where[(y, x)], pair(y, x))
        if (-x, y) in where and x != 0:
            e += " Point %s is at %s: the sign of x is wrong." % (where[(-x, y)], pair(-x, y))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    its.append(mcq("To plot %s, what do you do first from the origin?" % pair(-3, 5), "Go 3 left",
                   ["Go 3 right", "Go 3 down", "Go 5 left"],
                   "The first number, %s, is the x-coordinate. It is negative, so go 3 left. Then go 5 up." % num(-3), rnd))
    its.append(mcq("What does a negative x-coordinate tell you?", "The point is left of the y-axis",
                   ["The point is right of the y-axis", "The point is below the x-axis", "The point is above the x-axis"],
                   "The x-coordinate says how far left or right to go. Positive means right; negative means left of the y-axis.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at the origin. %s goes 5 left, then 2 down. What are the coordinates of %s point?" % (n, he.capitalize(), his),
                   pair(-5, -2), [pair(-2, -5), pair(5, 2), pair(5, -2)],
                   "5 left gives x = %s. 2 down gives y = %s. Write x first: %s." % (num(-5), num(-2), pair(-5, -2)), rnd))
    its.append(mcq("A point is 4 squares to the left of the y-axis and 6 squares above the x-axis. What are its coordinates?",
                   pair(-4, 6), [pair(6, -4), pair(4, 6), pair(-4, -6)],
                   "Left of the y-axis means x is negative: x = %s. Above the x-axis means y is positive: y = 6. The point is %s."
                   % (num(-4), pair(-4, 6)), rnd))
    its.append(mcq("Which point is below the x-axis and to the left of the y-axis?", pair(-3, -1),
                   [pair(3, -1), pair(-3, 1), pair(0, -3)],
                   "Left of the y-axis: x is negative. Below the x-axis: y is negative. Only %s has both coordinates negative. "
                   "(%s is on the y-axis, not to the left of it.)" % (pair(-3, -1), pair(0, -3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read and plot points in all four quadrants", "items": its}


# ------------------------------------------------------------ set 2: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    for i, (p, dx, dy) in enumerate([((2, 1), -4, -3), ((-3, 4), 5, -2), ((-1, -2), 0, 6), ((4, -3), -6, 0),
                                     ((3, 5), -7, -4)]):
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), move_cands(p, dx, dy, i), move_e(p, dx, dy), rnd))
    for p, dx, dy, others in [((3, 2), -5, -4, [(2, -2), (-2, 2), (-2, 6)]),
                              ((-4, -1), 6, 3, [(2, -4), (2, -1), (-1, 5)]),
                              ((1, -4), -3, 7, [(1, 3), (4, 3), (-6, -1)]),
                              ((-2, 5), 4, -8, [(2, 3), (2, 5), (-6, -3)])]:
        q = (p[0] + dx, p[1] + dy)
        pts, ans = pick_letters(q, others, pos)
        G = grid_for([p] + [c[:2] for c in pts], lo=5)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is translated %s. Which point shows where it lands?" % mv_long(dx, dy),
                             LETTERS, ans, move_e(p, dx, dy) + " That is point %s." % ans))
    for i, (a, b) in enumerate([((-3, 2), (4, -1)), ((2, 4), (-3, 1)), ((-4, -3), (1, 2)), ((5, -1), (-2, -1))]):
        G = grid_for([a, b], lo=5)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(b[0] - a[0], b[1] - a[1]), describe_cands(a, b, i), describe_e(a, b), rnd))
    for i, (a, b) in enumerate([((-5, 4), (1, -2)), ((3, -5), (-1, 2))]):
        its.append(mcq("A shape’s vertex moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(b[0] - a[0], b[1] - a[1]), describe_cands(a, b, i + 1), describe_e(a, b, "The start", "the end"), rnd))
    its.append(mcq("Point B is translated 4 squares left and 3 squares up. It lands on %s. Where did it start?" % pair(-1, 2), pair(3, -1),
                   [pair(-5, 5), pair(3, 5), pair(-5, -1)],
                   "Work backwards and undo each move. 4 left is undone by 4 right: %s. 3 up is undone by 3 down: %s. B started at %s."
                   % (op(-1, 4), op(2, -3), pair(3, -1)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s translates %s 4 squares left and gets %s. What mistake did %s make?" % (n, pair(3, -1), pair(1, -1), he),
                   "%s worked out 4 − 3, not 3 − 4" % H,
                   ["%s moved right, not left" % H, "%s changed the wrong coordinate" % H, "No mistake: %s is right" % he],
                   "Left 4 from x = 3: 3 − 4 = %s. It goes 3 squares to the y-axis, then 1 more. The answer is %s, not %s."
                   % (num(-1), pair(-1, -1), pair(1, -1)), rnd))
    tri = [(-4, 1), (-1, 1), (-4, 5)]
    p, dx, dy = (-1, 1), 5, -6
    its.append(mcq("A triangle has vertices at %s. It is translated %s. What are the new coordinates of the vertex at %s?"
                   % (plist(tri), mv_long(dx, dy), pair(*p)),
                   pair(p[0] + dx, p[1] + dy), move_cands(p, dx, dy, 2),
                   move_e(p, dx, dy) + " Every vertex moves in the same way, so the shape stays the same size.", rnd))
    G = Grid(6)
    A, B = [(-5, 1), (-2, 1), (-2, 3), (-5, 3)], [(1, -4), (4, -4), (4, -2), (1, -2)]
    G.poly(A, GREEN, "A").poly(B, BLUE, "B")
    its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                   "Shape A is translated to shape B. Describe the translation.", mv(6, -5),
                   describe_cands(A[0], B[0], 2),
                   "Follow one vertex. The bottom-left vertex of A is at %s and of B is at %s. Across: %s. Down: %s. "
                   "That is %s. Every vertex moves the same way."
                   % (pair(*A[0]), pair(*B[0]), across(-5, 1, "right", "left"), across(1, -4, "up", "down"), mv_long(6, -5)), rnd))
    sqr = [(1, 1), (4, 1), (4, 4), (1, 4)]
    dx, dy = -6, -5
    new = [(x + dx, y + dy) for x, y in sqr]
    its.append(mcq("A square has vertices at %s. It is translated %s. Which list shows the new vertices?" % (plist(sqr), mv_long(dx, dy)),
                   plist(new), [plist([(x + dx, y) for x, y in sqr]), plist([(x + dy, y + dx) for x, y in sqr]),
                                plist([(abs(x + dx), abs(y + dy)) for x, y in sqr])],
                   "Subtract 6 from every x-coordinate and 5 from every y-coordinate. For example, (1, 1) → (%s, %s) = %s."
                   % (op(1, -6), op(1, -5), pair(-5, -4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations across the axes", "items": its}


# ------------------------------------------------------------ set 3: reflections
def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, axis in [((3, -2), "y"), ((-4, 5), "x"), ((5, 1), "y"), ((-2, -6), "x"), ((-6, -3), "y")]:
        r = reflect(p, axis)
        other = reflect(p, "y" if axis == "x" else "x")
        its.append(mcq("Reflect %s in the %s-axis. What are the coordinates of the image?" % (pair(*p), axis),
                       pair(*r), [pair(*other), pair(-p[0], -p[1]), pair(r[1], r[0])], refl_e(p, axis), rnd))
    its.append(mcq("Reflect %s in the y-axis. What are the coordinates of the image?" % pair(0, 5), pair(0, 5),
                   [pair(0, -5), pair(5, 0), pair(-5, 0)], refl_e((0, 5), "y"), rnd))
    its.append(mcq("Reflect %s in the x-axis. What are the coordinates of the image?" % pair(-4, 0), pair(-4, 0),
                   [pair(4, 0), pair(0, -4), pair(0, 4)], refl_e((-4, 0), "x"), rnd))
    for p, axis in [((-3, 2), "x"), ((4, -2), "y"), ((-2, -5), "x"), ((5, 3), "y")]:
        r = reflect(p, axis)
        others = [reflect(p, "y" if axis == "x" else "x"), (-p[0], -p[1]), (r[1], r[0])]
        pts, ans = pick_letters(r, others, pos)
        where = {(q[0], q[1]): q[2] for q in pts}
        G = grid_for([p] + [q[:2] for q in pts])
        G.point(p[0], p[1], "P", RED)
        for q in pts:
            G.point(*q)
        e = "P is at %s. %s That is point %s. Point %s is the reflection in the %s-axis instead." % (
            pair(*p), refl_e(p, axis), ans, where[others[0]], "y" if axis == "x" else "x")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Which point is the reflection of point P in the %s-axis?" % axis, LETTERS, ans, e))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(-5, 2), pair(5, 2)), AXES,
                         "the y-axis", "Only the x-coordinate changes sign (%s → 5), so the points flip left and right. The mirror line is the y-axis." % num(-5)))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(3, -4), pair(3, 4)), AXES,
                         "the x-axis", "Only the y-coordinate changes sign (%s → 4), so the points flip up and down. The mirror line is the x-axis." % num(-4)))
    tA = [(2, 1), (5, 1), (2, 4)]
    tB = [(-5, 1), (-1, 1), (-5, 4)]
    tC = [(1, 2), (4, 2), (1, 5)]
    for A, B, ans, e in [
        (tA, [reflect(p, "x") for p in tA], "reflected in the x-axis",
         "Each vertex keeps its x-coordinate and its y-coordinate changes sign, for example %s → %s. "
         "Shape B is a mirror image below the x-axis." % (pair(5, 1), pair(5, -1))),
        (tB, [reflect(p, "y") for p in tB], "reflected in the y-axis",
         "Each vertex keeps its y-coordinate and its x-coordinate changes sign, for example %s → %s. "
         "The right angle is now on the right: a mirror image in the y-axis." % (pair(-5, 1), pair(5, 1))),
        (tC, [(x - 6, y - 6) for x, y in tC], "translated",
         "Every vertex moved 6 squares left and 6 squares down, for example %s → %s. "
         "The shape faces the same way, so it slid: a translation, not a reflection." % (pair(1, 2), pair(-5, -4))),
    ]:
        G = Grid(6)
        G.poly(A, GREEN, "A").poly(B, BLUE, "B")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) +
                             "How has shape A moved to shape B?", MOVES, ans, e))
    tri = [(-4, 1), (-1, 1), (-4, 5)]
    its.append(mcq("A triangle has vertices at %s. It is reflected in the x-axis. Which list shows the vertices of the image?" % plist(tri),
                   plist([reflect(p, "x") for p in tri]),
                   [plist([reflect(p, "y") for p in tri]), plist([(-x, -y) for x, y in tri]),
                    plist([(-4, -1), (-1, -1), (-4, 5)])],
                   "In the x-axis, keep each x and change the sign of each y: %s. Change every vertex, not just some."
                   % ", ".join("%s → %s" % (pair(*p), pair(*reflect(p, "x"))) for p in tri), rnd))
    its.append(mcq("When you reflect a point in the y-axis, what changes?", "the sign of the x-coordinate",
                   ["the sign of the y-coordinate", "the signs of both coordinates", "the order of the numbers"],
                   "The y-axis is a mirror standing up and down. The point flips left or right, so only x changes sign. "
                   "Example: %s → %s." % (pair(4, 3), pair(-4, 3)), rnd))
    rect = [(1, -2), (5, -2), (5, -4), (1, -4)]
    its.append(mcq("A rectangle has vertices at %s. It is reflected in the y-axis. What are the coordinates of the image of %s?"
                   % (plist(rect), pair(5, -2)),
                   pair(-5, -2), [pair(5, 2), pair(-5, 2), pair(-2, -5)],
                   refl_e((5, -2), "y") + " The image rectangle is to the left of the y-axis, the same distance away.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s in the x-axis and gets %s. What mistake did %s make?" % (n, pair(2, 5), pair(-2, 5), he),
                   "%s reflected in the y-axis" % H,
                   ["%s swapped x and y" % H, "%s changed both signs" % H, "No mistake: %s is right" % he],
                   "%s changed the sign of x, which is a reflection in the y-axis. In the x-axis, y changes sign: %s." % (n, pair(2, -5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in the x-axis and y-axis", "items": its}


# ------------------------------------------------------------ set 4: missing vertices and side lengths
def set_vertex(rnd, P):
    its = []
    pos = Pos(rnd)
    for A, B, C, D in [((-4, 3), (2, 3), (2, -2), (-4, -2)),
                       ((-3, -4), (-3, 1), (3, 1), (3, -4)),
                       ((2, 2), (-3, 2), (-3, -3), (2, -3))]:
        G = grid_for([A, B, C, D])
        G.seg(A, B).seg(B, C)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        assert (D[0] == A[0] and D[1] == C[1]) or (D[0] == C[0] and D[1] == A[1])
        same_x = "A" if D[0] == A[0] else "C"
        same_y = "C" if same_x == "A" else "A"
        kind = "square" if abs(A[0] - B[0]) + abs(A[1] - B[1]) == abs(B[0] - C[0]) + abs(B[1] - C[1]) else "rectangle"
        e = ("D is in line with %s up and down, so x = %s. It is in line with %s across, so y = %s. D is at %s."
             % (same_x, num(D[0]), same_y, num(D[1]), pair(*D)))
        its.append(mcq(fig(G.svg("coordinate grid with three vertices of a " + kind)) +
                       "A, B and C are 3 vertices of a %s. What are the coordinates of the 4th vertex, D?" % kind,
                       pair(*D), vertex_cands(D, [A, B, C]), e, rnd))
    for A, B, C, wrong in [((-4, -2), (1, -2), (3, 2), [(-4, 2), (2, -2), (2, 2)]),
                           ((-4, 3), (-2, -1), (3, -1), [(3, 3), (3, 1), (-1, 3)])]:
        D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
        G = grid_for([A, B, C, D], lo=5)
        G.seg(A, B).seg(B, C)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        dx, dy = A[0] - B[0], A[1] - B[1]
        its.append(mcq(fig(G.svg("coordinate grid with three vertices of a parallelogram")) +
                       "A, B and C are 3 vertices of parallelogram ABCD. What are the coordinates of D?",
                       pair(*D), [pair(*w) for w in wrong],
                       "Opposite sides of a parallelogram are parallel and equal. To go from B to A you move %s. "
                       "Make the same move from C: %s → %s. D is at %s." % (mv_long(dx, dy), pair(*C), pair(*D), pair(*D)), rnd))
    corners, tgt, others = [(-3, -2), (1, -2), (1, 2)], (-3, 2), [(3, 2), (2, -3), (-3, 3)]
    pts, ans = pick_letters(tgt, others, pos)
    G = grid_for(corners + [c[:2] for c in pts])
    for c in corners:
        G.point(c[0], c[1], None, RED)
    for c in pts:
        G.point(*c)
    its.append(mcq_fixed(fig(G.svg("coordinate grid with three red vertices and points A to D")) +
                         "The red dots are 3 vertices of a square. Which point is the 4th vertex?", LETTERS, ans,
                         "The missing vertex lines up with the red ones: x = %s (above %s) and y = 2 (across from %s). "
                         "That is %s, point %s." % (num(-3), pair(-3, -2), pair(1, 2), pair(*tgt), ans)))
    for given, D, kind in [([(-2, 5), (4, 5), (4, -3)], (-2, -3), "rectangle"),
                           ([(-1, -1), (3, -1), (3, 3)], (-1, 3), "square"),
                           ([(-5, -2), (3, 4), (-5, 4)], (3, -2), "rectangle")]:
        xs = sorted({c[0] for c in given + [D]})
        ys = sorted({c[1] for c in given + [D]})
        assert set((x, y) for x in xs for y in ys) == set(given + [D])
        its.append(mcq("A %s has vertices at %s. What are the coordinates of the 4th vertex?" % (kind, plist(given)),
                       pair(*D), vertex_cands(D, given),
                       "The vertices of a %s use just two x-coordinates (%s and %s) and two y-coordinates (%s and %s). "
                       "The pair not used yet is %s." % (kind, num(xs[0]), num(xs[1]), num(ys[0]), num(ys[1]), pair(*D)), rnd))
    A, B, C = (-3, -2), (2, -2), (4, 1)
    D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
    its.append(mcq("ABCD is a parallelogram. A is at %s, B is at %s and C is at %s. What are the coordinates of D?" % (pair(*A), pair(*B), pair(*C)),
                   pair(*D), [pair(-3, 1), pair(1, -1), pair(1, 1)],
                   "From B to C you move 2 right and 3 up. The opposite side AD makes the same move: %s → %s. "
                   "(%s would make a rectangle, not this parallelogram.)" % (pair(*A), pair(*D), pair(-3, 1)), rnd))
    for a, b, na, nb, wrong in [((2, -4), (2, 3), "A", "B", [1, 3, 4]), ((-5, 1), (3, 1), "C", "D", [2, 3, 5]),
                                ((-3, -2), (-3, 4), "E", "F", [2, 7, -2])]:
        e, d = length_e(a, b)
        G = grid_for([a, b])
        G.seg(a, b)
        G.point(a[0], a[1], na).point(b[0], b[1], nb)
        its.append(mcq_int(fig(G.svg("coordinate grid with a line segment")) +
                           "How long is the side %s%s? Give your answer in squares." % (na, nb), d, wrong,
                           e + " Add the two parts; do not subtract them or use just one."))
    for a, b, wrong in [((-6, -4), (-1, -4), [7, 6, -5]), ((0, -5), (0, 4), [1, 10, -1]), ((-4, 3), (-4, -2), [1, 2, 3])]:
        e, d = length_e(a, b)
        its.append(mcq_int("A side of a shape goes from %s to %s. How long is it?" % (pair(*a), pair(*b)), d, wrong, e, " squares"))
    its.append(mcq_int("A rectangle has vertices at %s. What is its perimeter?" % plist([(-3, 2), (4, 2), (4, -1), (-3, -1)]),
                       20, [4, 10, 24],
                       "Length: %s to 4 is 3 + 4 = 7 squares. Width: %s to 2 is 1 + 2 = 3 squares. "
                       "Perimeter = 7 + 3 + 7 + 3 = 20 squares. (Doing 4 − 3 and 2 − 1 gives sides of 1 and a perimeter of 4.)"
                       % (num(-3), num(-1)), " squares"))
    its.append(mcq_int("A square has vertices at %s. What is its perimeter?" % plist([(-3, -3), (3, -3), (3, 3), (-3, 3)]),
                       24, [0, 28, 36],
                       "Each side goes from %s to 3: 3 + 3 = 6 squares. Perimeter = 4 × 6 = 24 squares. "
                       "(3 − 3 = 0 comes from subtracting instead of adding; 28 comes from counting 7 dots on each side.)" % num(-3),
                       " squares"))
    its.append(mcq_int("A rectangle has vertices at %s. Each square is 1 cm². What is its area?" % plist([(-5, 3), (2, 3), (2, -2), (-5, -2)]),
                       35, [3, 24, 48],
                       "Length: 5 + 2 = 7 cm (opposite sides of the y-axis). Width: 3 + 2 = 5 cm (opposite sides of the x-axis). "
                       "Area = 7 × 5 = 35 cm².", " cm²"))
    its.append(mcq("A square has vertices at %s and %s. The other two vertices are above the x-axis. "
                   "What are the coordinates of the vertex straight above %s?" % (pair(-2, -1), pair(3, -1), pair(3, -1)),
                   pair(3, 4), [pair(3, 5), pair(3, 0), pair(4, 3)],
                   "The side from %s to %s is 2 + 3 = 5 squares long. All sides of a square are equal, so go 5 up from %s: %s."
                   % (pair(-2, -1), pair(3, -1), pair(3, -1), op(-1, 5)) + " The vertex is at %s." % pair(3, 4), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Missing vertices and side lengths across the axes", "items": its}


# ------------------------------------------------------------ set 5: SATs-style problems
FIELD = [(-4, 3, "T"), (3, 4, "B"), (-3, -4, "P"), (5, -2, "S")]


def set_problems(rnd, P):
    its = []
    its.append(mcq("Point %s is translated 5 squares left and 1 square down. Then it is reflected in the x-axis. Where does it end up?" % pair(2, 3),
                   pair(-3, -2), [pair(-3, 2), pair(-3, -4), pair(3, 2)],
                   "Do the moves in order. Translate: %s → %s. Reflect in the x-axis (y changes sign): %s → %s. "
                   "Reflecting first gives a different answer, %s." % (pair(2, 3), pair(-3, 2), pair(-3, 2), pair(-3, -2), pair(-3, -4)), rnd))
    its.append(mcq("Point %s is reflected in the y-axis. Then it is translated 2 squares left and 5 squares up. Where does it end up?" % pair(-4, -1),
                   pair(2, 4), [pair(6, 4), pair(-6, 4), pair(-6, 6)],
                   "Reflect in the y-axis (x changes sign): %s → %s. Translate: x: %s. y: %s. It ends at %s."
                   % (pair(-4, -1), pair(4, -1), op(4, -2), op(-1, 5), pair(2, 4)), rnd))
    tri = [(1, 1), (4, 1), (1, 4)]
    G = Grid(5)
    G.poly(tri, GREEN)
    G.point(1, 1, "P", where=(-1, -1)).point(4, 1, "Q", where=(1, 1)).point(1, 4, "R", where=(-1, 1))
    its.append(mcq(fig(G.svg("coordinate grid with triangle PQR")) +
                   "Triangle PQR is translated 6 squares left. Then it is reflected in the x-axis. What are the new coordinates of Q?",
                   pair(-2, -1), [pair(-2, 1), pair(2, 1), pair(4, -1)],
                   "Q is at %s. 6 left: %s, so Q moves to %s. Reflect in the x-axis: %s → %s." % (
                       pair(4, 1), op(4, -6), pair(-2, 1), pair(-2, 1), pair(-2, -1)), rnd))
    its.append(mcq("A translation moves point A from %s to %s. The same translation moves point B from %s. Where does B go?"
                   % (pair(-3, 2), pair(2, -1), pair(1, 4)),
                   pair(6, 1), [pair(-4, 7), pair(6, 4), pair(0, 1)],
                   "A moves 5 right (%s to 2) and 3 down (2 to %s). Move B the same way: %s → %s." % (
                       num(-3), num(-1), pair(1, 4), pair(6, 1)), rnd))
    its.append(mcq("ABCD is a rectangle. A is at %s and C is at %s. B is straight to the right of A. What are the coordinates of D?"
                   % (pair(-5, 2), pair(3, -4)),
                   pair(-5, -4), [pair(3, 2), pair(-4, -5), pair(5, -4)],
                   "B is right of A, so B = %s. D is opposite B: straight below A and straight across from C. "
                   "D takes x from A and y from C: %s." % (pair(3, 2), pair(-5, -4)), rnd))
    its.append(mcq("A square has its centre at the origin. Its sides are parallel to the axes. One vertex is at %s. "
                   "What are the coordinates of the vertex below the x-axis and to the left of the y-axis?" % pair(3, 3),
                   pair(-3, -3), [pair(3, -3), pair(-3, 3), pair(-6, -6)],
                   "The square is symmetrical about both axes, so its vertices are %s. Left and below means both are negative: %s."
                   % (plist([(3, 3), (-3, 3), (-3, -3), (3, -3)]), pair(-3, -3)), rnd))
    its.append(mcq("The points %s follow a pattern. What is the next point?" % plist([(-6, 5), (-4, 3), (-2, 1), (0, -1)]),
                   pair(2, -3), [pair(2, 1), pair(2, -1), pair(3, -3)],
                   "Each time x goes up by 2 and y goes down by 2. Next: x = 0 + 2 = 2 and y = %s." % op(-1, -2), rnd))
    its.append(mcq("The points %s lie on a straight line. The steps stay the same. What is the next point?"
                   % plist([(-5, -4), (-3, -1), (-1, 2)]),
                   pair(1, 5), [pair(2, 4), pair(1, 4), pair(-3, 5)],
                   "Each step is 2 right and 3 up: %s and %s. Next: %s and %s." % (op(-5, 2), op(-4, 3), op(-1, 2), op(2, 3)), rnd))
    its.append(mcq("In the points %s, the y-coordinate is always 2 less than the x-coordinate. Which point also fits the rule?"
                   % plist([(-2, -4), (-1, -3), (0, -2), (1, -1)]),
                   pair(5, 3), [pair(3, 5), pair(-5, -3), pair(4, -2)],
                   "Check y = x − 2. For %s: 5 − 2 = 3. Yes. For %s: 3 − 2 = 1, not 5 (the numbers are swapped). "
                   "For %s: %s − 2 = %s, not %s." % (pair(5, 3), pair(3, 5), pair(-5, -3), num(-5), num(-7), num(-3)), rnd))
    its.append(mcq_int("Point P is at (a, 3). It is reflected in the y-axis and lands on %s. What is the value of a?" % pair(-4, 3),
                       4, [-4, 3, -3],
                       "A reflection in the y-axis changes the sign of x. The image has x = %s, so P has x = 4. a = 4." % num(-4)))
    its.append(mcq_int("Point Q is at %s. It is reflected in the x-axis and lands on %s. What is the value of b?" % ("(" + num(-2) + ", b)", pair(-2, 5)),
                       -5, [5, -2, 2],
                       "A reflection in the x-axis changes the sign of y. The image has y = 5, so Q has y = %s. b = %s." % (num(-5), num(-5))))
    G = Grid(6)
    for x, y, n in FIELD:
        G.point(x, y, n)
    fm = fig(G.svg("map of a school field on a coordinate grid"))
    key = ("The map shows the school field. The origin is the centre circle. T = tree, B = bench, P = pond, S = shed. "
           "Each square is 10 m. ")
    its.append(mcq(fm + key + "What are the coordinates of the shed?", pair(5, -2), [pair(-2, 5), pair(5, 2), pair(-5, -2)],
                   "Start at the origin, go 5 right, then 2 down. The shed is at %s." % pair(5, -2), rnd))
    n, he, his = P.next()
    its.append(mcq(fm + key + "%s starts at the tree. %s walks 7 squares right and 1 square up. Where is %s now?" % (n, he.capitalize(), he),
                   "at the bench", ["at the shed", "at the pond", "at the centre circle"],
                   "The tree is at %s. 7 right: %s. 1 up: 3 + 1 = 4. %s is the bench." % (pair(-4, 3), op(-4, 7), pair(3, 4)), rnd))
    its.append(mcq(fm + key + "A flag is placed at the reflection of the pond in the x-axis. What are its coordinates?",
                   pair(-3, 4), [pair(3, -4), pair(3, 4), pair(-4, -3)],
                   "The pond is at %s. In the x-axis, x stays %s and y changes sign: the flag is at %s." % (pair(-3, -4), num(-3), pair(-3, 4)), rnd))
    a, b = (-3, -4), (5, -2)
    its.append(mcq(fm + key + "Describe the translation from the pond to the shed.", mv(8, 2),
                   describe_cands(a, b, 0), describe_e(a, b, "The pond", "the shed"), rnd))
    its.append(mcq_int(fm + key + "A pupil walks along the grid lines from the pond to the tree by the shortest route. How many metres is that?",
                       80, [20, 70, 100],
                       "The pond is at %s and the tree is at %s. Across: 1 square. Up: %s to 3 is 4 + 3 = 7 squares. "
                       "1 + 7 = 8 squares, and 8 × 10 = 80 m." % (pair(-3, -4), pair(-4, 3), num(-4)), " m"))
    sh = [(1, 2), (3, 2), (1, 5)]
    its.append(mcq("A triangle has vertices at %s. It is reflected in the y-axis, then translated 4 squares down. Which list shows the new vertices?" % plist(sh),
                   plist([(-x, y - 4) for x, y in sh]),
                   [plist([(-x, y) for x, y in sh]), plist([(-x, y + 4) for x, y in sh]), plist([(x, -y - 4) for x, y in sh])],
                   "Reflect in the y-axis (x changes sign): %s. Then 4 down (subtract 4 from each y): %s."
                   % (plist([(-x, y) for x, y in sh]), plist([(-x, y - 4) for x, y in sh])), rnd))
    n, he, his = P.next()
    its.append(mcq("In a computer game, %s’s character starts at %s. It moves 5 squares right, 4 squares up, then 6 squares left. Where does it stop?"
                   % (n, pair(-2, -3)),
                   pair(-3, 1), [pair(3, 1), pair(9, 1), pair(1, -3)],
                   "One move at a time. 5 right: %s, so %s. 4 up: %s, so %s. 6 left: %s, so %s."
                   % (op(-2, 5), pair(3, -3), op(-3, 4), pair(3, 1), op(3, -6), pair(-3, 1)), rnd))
    its.append(mcq("Two vertices of a square are at %s and %s. The rest of the square is below this side. What are the other two vertices?"
                   % (pair(-2, 1), pair(2, 1)),
                   pair(2, -3) + " and " + pair(-2, -3),
                   [pair(2, 3) + " and " + pair(-2, 3), pair(2, -4) + " and " + pair(-2, -4), pair(2, 5) + " and " + pair(-2, 5)],
                   "The side is 2 + 2 = 4 squares long. Go 4 down from each vertex: %s." % op(1, -4), rnd))
    its.append(mcq("Point M is at %s. It is reflected in the y-axis, then in the x-axis. Where does it end up?" % pair(-5, 4),
                   pair(5, -4), [pair(5, 4), pair(-5, -4), pair(4, -5)],
                   "In the y-axis: %s → %s. Then in the x-axis: %s → %s. Two reflections change both signs."
                   % (pair(-5, 4), pair(5, 4), pair(5, 4), pair(5, -4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "SATs-style problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(5)
    G.arrow((0, 0), (-3, 0)).arrow((-3, 0), (-3, 4))
    G.note(-1.6, 0.45, "3 left").note(-2.8, 2, "4 up", anchor="start")
    G.point(-3, 4, "A", where=(1, 1))
    plot = G.svg("coordinate grid: from the origin go 3 left, then 4 up to point A at (−3, 4)")
    G = Grid(5)
    G.arrow((2, 1), (-2, 1)).arrow((-2, 1), (-2, -2))
    G.point(2, 1, "A", RED, where=(1, -1)).point(-2, -2, "B", where=(-1, -1))
    G.note(1.1, 1.5, "4 left").note(-2.25, -1.5, "3 down", anchor="end")
    trans = G.svg("coordinate grid: point A at (2, 1) is translated 4 left and 3 down to point B at (−2, −2)")
    G = Grid(5)
    tri = [(1, 1), (4, 1), (1, 3)]
    G.poly(tri, GREEN, "A").poly([reflect(p, "y") for p in tri], BLUE, "B").poly([reflect(p, "x") for p in tri], RED, "C")
    refl = G.svg("triangle A, its reflection B in the y-axis and its reflection C in the x-axis")
    G = Grid(5)
    G.seg((-4, 3), (2, 3)).seg((2, 3), (2, -2)).seg((2, -2), (-4, -2), BLUE, 3, True).seg((-4, -2), (-4, 3), BLUE, 3, True)
    G.point(-4, 3, "A").point(2, 3, "B").point(2, -2, "C").point(-4, -2, "D", RED)
    poly = G.svg("rectangle ABCD with the missing vertex D at (−4, −2)")
    return (
        "<h2>The four quadrants</h2>"
        "<p>In Year 6 the x-axis and the y-axis carry on past 0 into negative numbers. They cross at the <b>origin</b>, (0, 0), "
        "and split the grid into four <b>quadrants</b>.</p>"
        "<p>Coordinates (x, y) still go <b>along the corridor, then up (or down) the stairs</b>. The sign tells the direction. "
        "Positive x: right. Negative x: left. Positive y: up. Negative y: down.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (−3, 4), start at the origin. Go 3 left, then 4 up.</figcaption></figure>" +
        table(["Where", "Signs (x, y)", "Example"], [
            ["top right", "(+, +)", "(2, 5)"],
            ["top left", "(−, +)", "(−3, 4)"],
            ["bottom left", "(−, −)", "(−6, −1)"],
            ["bottom right", "(+, −)", "(4, −2)"],
        ]) +
        "<p>A point on an axis has a 0 in it, like (0, −4) or (5, 0).</p>"
        "<h2>Translations</h2>"
        "<p>A <b>translation</b> slides a point or shape without turning it. Left and right change only x. "
        "Up and down change only y. When you cross an axis, count to 0, then keep going.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>A (2, 1) is translated 4 squares left and 3 squares down. x: 2 − 4 = −2. y: 1 − 3 = −2. It lands on B (−2, −2).</figcaption></figure>" +
        ex("Example", "Describe the translation from (−3, 2) to (4, −1).",
           "Across: −3 to 4 is 3 squares to the y-axis, then 4 more: 7 right. Up and down: 2 to −1 is 3 down.",
           "7 squares right and 3 squares down") +
        "<h2>Reflections in the axes</h2>"
        "<p>An axis works like a mirror. Reflecting in the <b>x-axis</b> changes the sign of <b>y</b>. "
        "Reflecting in the <b>y-axis</b> changes the sign of <b>x</b>. Each vertex stays the same distance from the mirror line.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>Triangle A reflected in the y-axis is B. Reflected in the x-axis, it is C. (1, 3) → (−1, 3) and (1, −3).</figcaption></figure>" +
        ex("Example", "Reflect (−4, 5) in the x-axis.", "The x-axis is the mirror, so the point flips down. x stays −4. y changes sign: 5 → −5.",
           "(−4, −5)") +
        "<h2>Missing vertices and side lengths</h2>"
        "<p>The missing vertex of a rectangle shares its x-coordinate with one vertex and its y-coordinate with another. "
        "For a side that crosses an axis, add the distances on each side: from −4 to 2 is 4 + 2 = 6.</p>"
        "<figure class='sn-fig'>" + poly +
        "<figcaption>D is below A, so x = −4, and across from C, so y = −2. D is at (−4, −2). Side AB is 4 + 2 = 6 squares.</figcaption></figure>" +
        ex("Example", "A parallelogram ABCD has A (−3, −2), B (2, −2) and C (4, 1). Find D.",
           "From B to C is 2 right and 3 up. Do the same move from A: (−3 + 2, −2 + 3).", "(−1, 1)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping the numbers: plotting (−3, 4) at (4, −3)", "Across first (x), then up or down (y)"],
            ["Sign errors at an axis: 2 − 4 = 2", "Count to 0, then keep going: 2 − 4 = −2"],
            ["Finding −4 to 3 as 4 − 3 = 1", "Opposite sides of an axis: add, 4 + 3 = 7"],
            ["Reflecting in the wrong axis", "In the x-axis, y changes sign. In the y-axis, x changes sign"],
            ["Changing only one coordinate in “4 left and 3 down”", "Change x for left/right and y for up/down"],
        ])
    )


FAQ = [
    {"q": "What do children learn about coordinates in Year 6?",
     "a": "Year 6 pupils use the full coordinate grid in all four quadrants. They plot points with negative coordinates, "
          "translate shapes and reflect them in the x-axis and y-axis."},
    {"q": "How do you reflect a shape in the x-axis?",
     "a": "Reflect each vertex: keep the x-coordinate and change the sign of the y-coordinate, so (3, 2) becomes (3, −2). Then join the new vertices."},
    {"q": "How do you describe a translation on a coordinate grid?",
     "a": "Follow one vertex and say how many squares it moves left or right and up or down, for example “6 squares right and 5 squares down”. Every vertex moves the same way."},
    {"q": "Are coordinates in the Year 6 SATs?",
     "a": "Yes. The KS2 reasoning papers can include questions on coordinates in all four quadrants, translations, reflections and finding missing vertices of shapes."},
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
    rnd = random.Random(6618)
    P = People(rnd)
    sets = [set_read(rnd, P), set_translate(rnd, P), set_reflect(rnd, P), set_vertex(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "coordinates-and-transformations", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Coordinates in Four Quadrants, Translations and Reflections",
        "seo_title": "Year 6 Coordinates Worksheets: Four Quadrants, Translations and Reflections",
        "short_title": "Coordinates and transformations",
        "domain": "Geometry – position and direction",
        "standard_code": "Year 6: Geometry – position and direction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Describe positions on the full coordinate grid (all four quadrants); draw and translate simple shapes on the coordinate plane, and reflect them in the axes.",
        "meta_desc": "Free Year 6 maths worksheets on coordinates in all four quadrants: plot points with negative coordinates, translate and reflect shapes in the axes, find missing vertices and solve SATs-style problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "(x, y): x says left or right, y says up or down, and a minus sign means left or down.",
        "key_sub": "A translation changes x for left/right moves and y for up/down moves. Reflecting in the x-axis changes the sign of y; reflecting in the y-axis changes the sign of x. Across an axis, add the distances on each side.",
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
        mark_large(u, "(coordinate grid|map of)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
