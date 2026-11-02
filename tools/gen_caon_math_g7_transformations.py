# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Transformations and dilations
(Ontario Curriculum 2020, Spatial Sense E1.3 and E1.4)
  python3 tools/gen_caon_math_g7_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

Canadian English (counterclockwise, centre, colour). Whole-number coordinates; every grid runs from −6 to 6
(lesson grids −5 to 5), is square and exact, and is drawn from the data. Negative numbers use the real minus sign.
Every image is computed by the transformation functions below; every "which transformation" answer is checked:
the right one maps the shape onto the image and no wrong choice does.
Dilations have their centre at the origin and scale factor 2, 3 or 1/2 (only points with even coordinates are
halved, so every image has whole-number coordinates).
Wrong answers come from real mistakes: translating the wrong way, changing the wrong coordinate, swapping the two
amounts, subtracting sizes when a move crosses an axis, counting grid lines, reflecting in the wrong axis, changing
both signs, rotating the wrong way, swapping the numbers in a 90° turn without changing a sign, mixing up 90° and
180°, adding the scale factor instead of multiplying, multiplying only one coordinate, and doubling instead of halving.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2f6fb5"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
QUADS = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]
AXES = ["the x-axis", "the y-axis", "both axes", "neither axis"]
TURNS4 = ["90° clockwise", "90° counterclockwise", "180°", "360°"]


# ------------------------------------------------------------ numbers and pairs
def num(v):
    if isinstance(v, Fraction):
        assert v.denominator == 1, v
        v = int(v)
    return (MINUS + str(-v)) if v < 0 else str(v)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, d)


HALF = Fraction(1, 2)


def kname(k):
    """Scale factor as HTML: 2, 3 or a fraction."""
    k = Fraction(k)
    return str(k.numerator) if k.denominator == 1 else fr(k.numerator, k.denominator)


def pair(x, y):
    return "(%s, %s)" % (num(x), num(y))


def plist(pts):
    return ", ".join(pair(*p) for p in pts)


def quad(x, y):
    assert x != 0 and y != 0
    return {(1, 1): "Quadrant I", (-1, 1): "Quadrant II", (-1, -1): "Quadrant III", (1, -1): "Quadrant IV"}[
        (1 if x > 0 else -1, 1 if y > 0 else -1)]


def units(k):
    return "%d unit" % k if k == 1 else "%d units" % k


def mv(dx, dy):
    """'5 units right and 3 units down' (x first)."""
    a = "" if dx == 0 else "%s %s" % (units(abs(dx)), "right" if dx > 0 else "left")
    b = "" if dy == 0 else "%s %s" % (units(abs(dy)), "up" if dy > 0 else "down")
    assert a or b
    return " and ".join(t for t in (a, b) if t)


def add_e(a, d):
    """'−2 + 5 = 3' or '4 − 6 = −2'."""
    return "%s %s %d = %s" % (num(a), "+" if d >= 0 else MINUS, abs(d), num(a + d))


# ------------------------------------------------------------ transformations
def T(p, st):
    x, y = p
    k = st[0]
    if k == "t":
        return (x + st[1], y + st[2])
    if k == "rx":
        return (x, -y)
    if k == "ry":
        return (-x, y)
    if k == "cw":
        return (y, -x)
    if k == "ccw":
        return (-y, x)
    if k == "half":
        return (-x, -y)
    if k == "d":
        f = Fraction(st[1])
        a, b = x * f, y * f
        assert a.denominator == 1 and b.denominator == 1, (p, st)
        return (int(a), int(b))
    raise ValueError(st)


def run(p, steps):
    for st in steps:
        p = T(p, st)
    return p


def runs(pts, steps):
    return [run(p, steps) for p in pts]


def sname(st):
    """Noun phrase for one step."""
    k = st[0]
    if k == "t":
        return "a translation %s" % mv(st[1], st[2])
    if k == "d":
        return "a dilation by a scale factor of %s" % kname(st[1])
    return {"rx": "a reflection in the x-axis", "ry": "a reflection in the y-axis",
            "cw": "a rotation of 90° clockwise", "ccw": "a rotation of 90° counterclockwise",
            "half": "a rotation of 180°"}[k]


def sverb(st):
    """Verb phrase for one step: 'translate it 3 units left', 'reflect it in the x-axis'."""
    k = st[0]
    if k == "t":
        return "translate %s" % mv(st[1], st[2])
    if k == "d":
        return "dilate by a scale factor of %s" % kname(st[1])
    return {"rx": "reflect in the x-axis", "ry": "reflect in the y-axis",
            "cw": "rotate 90° clockwise about the origin", "ccw": "rotate 90° counterclockwise about the origin",
            "half": "rotate 180° about the origin"}[k]


def step_e(p, st):
    """One step of working: 'Translate 5 units right: x: −2 + 5 = 3, y stays 4. (−2, 4) → (3, 4).'"""
    r = T(p, st)
    k = st[0]
    if k == "t":
        dx, dy = st[1], st[2]
        xs = ("x: " + add_e(p[0], dx)) if dx else ("x stays " + num(p[0]))
        ys = ("y: " + add_e(p[1], dy)) if dy else ("y stays " + num(p[1]))
        return "Translate %s: %s, %s. %s → %s." % (mv(dx, dy), xs, ys, pair(*p), pair(*r))
    if k == "rx":
        if p[1] == 0:
            return "%s is on the x-axis (the mirror line), so it stays at %s." % (pair(*p), pair(*r))
        return "Reflect in the x-axis: x stays, y changes sign. %s → %s." % (pair(*p), pair(*r))
    if k == "ry":
        if p[0] == 0:
            return "%s is on the y-axis (the mirror line), so it stays at %s." % (pair(*p), pair(*r))
        return "Reflect in the y-axis: y stays, x changes sign. %s → %s." % (pair(*p), pair(*r))
    if k == "cw":
        return ("Rotate 90° clockwise: (x, y) → (y, %sx). Swap the numbers, then change the sign of the second one. %s → %s."
                % (MINUS, pair(*p), pair(*r)))
    if k == "ccw":
        return ("Rotate 90° counterclockwise: (x, y) → (%sy, x). Swap the numbers, then change the sign of the first one. %s → %s."
                % (MINUS, pair(*p), pair(*r)))
    if k == "d":
        f = Fraction(st[1])
        if f == HALF:
            return ("Dilate by %s: multiply both coordinates by %s, which halves them. %s ÷ 2 = %s and %s ÷ 2 = %s. %s → %s."
                    % (kname(f), kname(f), num(p[0]), num(r[0]), num(p[1]), num(r[1]), pair(*p), pair(*r)))
        return ("Dilate by %s: multiply both coordinates by %s. %s × %s = %s and %s × %s = %s. %s → %s."
                % (f, f, num(p[0]), f, num(r[0]), num(p[1]), f, num(r[1]), pair(*p), pair(*r)))
    return "Rotate 180°: both signs change. %s → %s." % (pair(*p), pair(*r))


def steps_e(p, steps):
    out = []
    for st in steps:
        out.append(step_e(p, st))
        p = T(p, st)
    return " ".join(out)


def same_set(a, b):
    return sorted(a) == sorted(b)


def is_translation(a, b):
    sa, sb = sorted(a), sorted(b)
    d = (sb[0][0] - sa[0][0], sb[0][1] - sa[0][1])
    return all((q[0] - p[0], q[1] - p[1]) == d for p, q in zip(sa, sb))


def maps(a, b, st):
    """Does the step (or the word 'translation') map shape a onto shape b?"""
    if st == "translation":
        return is_translation(a, b)
    return same_set(runs(a, [st]), b)


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
    """Choices keep their order (A B C D, quadrant and axis words, turns)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


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
    n = 80
    for i in range(n + 1):
        t = i / float(n)
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if box[0] - m <= x <= box[2] + m and box[1] - m <= y <= box[3] + m:
            return True
    return False


class Grid:
    """Square grid from -R to R on both axes. Grid space = u px. Every axis number is written."""

    def __init__(self, R, u=22):
        assert 3 <= R <= 7
        self.R, self.u = R, u
        side = 2 * R * u
        self.ox = 24 + R * u
        self.oy = 34 + R * u
        self.W = self.H = int(math.ceil(24 + side + 34))
        self.pts, self.segs, self.arrows, self.notes, self.arcs, self.polys = [], [], [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def ok(self, p):
        return abs(p[0]) <= self.R and abs(p[1]) <= self.R

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
            self.segs.append((pts[i], pts[(i + 1) % len(pts)], col, 2.5, False))
        if name:
            if at is None:
                at = (sum(p[0] for p in pts) / float(len(pts)), sum(p[1] for p in pts) / float(len(pts)))
            self.note(at[0], at[1], name, col=col, fs=16)
        return self

    def seg(self, a, b, col=GREEN, w=3, dash=False):
        self.segs.append((a, b, col, w, dash))
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def arc(self, a, b, cw, col=RED):
        """Turning arrow about the origin from point a to point b (same distance from the origin)."""
        assert a[0] ** 2 + a[1] ** 2 == b[0] ** 2 + b[1] ** 2
        self.arcs.append((a, b, cw, col))
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
            s.append("<polygon points='%s' fill='%s' fill-opacity='0.16' stroke='none'/>"
                     % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), col))
        # axes with arrows at both ends
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
        # no "0" at the origin: next to the x-axis "-1" it would read as "-10"
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
        for a, b, cw, col in self.arcs:
            p, q = self.P(*a), self.P(*b)
            r = math.hypot(a[0], a[1]) * u
            d = 1 if cw else -1                       # screen y is down: clockwise = growing angle
            ang2 = math.atan2(q[1] - oy, q[0] - ox) - d * 15.0 / r
            ang0 = math.atan2(p[1] - oy, p[0] - ox) + d * 7.0 / r
            e = (ox + r * math.cos(ang2), oy + r * math.sin(ang2))
            start = (ox + r * math.cos(ang0), oy + r * math.sin(ang0))
            sweep_ang = (d * (ang2 - ang0)) % (2 * math.pi)
            large = 1 if sweep_ang > math.pi else 0
            s.append("<path d='M%.1f,%.1f A%.1f,%.1f 0 %d %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5' stroke-dasharray='7 4'/>"
                     % (start[0], start[1], r, r, large, 1 if cw else 0, e[0], e[1], col))
            v = (e[0] - ox, e[1] - oy)
            t = (-v[1] / r, v[0] / r) if cw else (v[1] / r, -v[0] / r)
            tip = (e[0] + t[0] * 9, e[1] + t[1] * 9)
            n = (-t[1], t[0])
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (tip[0], tip[1], e[0] + n[0] * 5, e[1] + n[1] * 5, e[0] - n[0] * 5, e[1] - n[1] * 5, col))
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
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=RED if col == RED else INK, extra=HALO))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def pick_letters(target, others, pos):
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    return [(c[0], c[1], "ABCD"[k]) for k, c in enumerate(cells)], "ABCD"[p]


def pick_grid(p, target, others, pos, label="coordinate grid with point P and points A to D"):
    """Grid with P (red) and A-D (green). Returns (svg, answer letter, {point: letter})."""
    assert len(set([target] + list(others) + [p])) == 5, (p, target, others)
    pts, ans = pick_letters(target, others, pos)
    G = Grid(6)
    G.point(p[0], p[1], "P", RED)
    for t in pts:
        G.point(*t)
    return G.svg(label), ans, {(t[0], t[1]): t[2] for t in pts}


def two_shapes(a, b, label, at_a=None, at_b=None):
    """Grid with shape A (red) and shape B (green). Labels at the centroid unless a place is given."""
    G = Grid(6)
    G.poly(a, RED, "A", at=at_a)
    G.poly(b, GREEN, "B", at=at_b)
    return G.svg(label)


# ------------------------------------------------------------ set 1: translations
def trans_cands(p, dx, dy):
    """Opposite way, wrong coordinate or swapped amounts, one direction wrong, counted grid lines."""
    x, y = p
    out = [(x - dx, y - dy)]
    if dx and dy:
        sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
        out += [(x + sx * abs(dy), y + sy * abs(dx)), (x + dx, y - dy), (x - dx, y + dy)]
    elif dx:
        out += [(x, y + dx), (x + dx + (1 if dx > 0 else -1), y), (x, y - dx)]
    else:
        out += [(x + dy, y), (x, y + dy + (1 if dy > 0 else -1)), (x - dy, y)]
    return [pair(*c) for c in out]


def describe_cands(a, b):
    """Wrong descriptions of the move a -> b: sizes subtracted across an axis, the move back, amounts swapped,
    one grid line too many."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    out = []
    sx = abs(abs(b[0]) - abs(a[0])) if a[0] * b[0] < 0 else abs(dx)
    sy = abs(abs(b[1]) - abs(a[1])) if a[1] * b[1] < 0 else abs(dy)
    if (sx, sy) != (abs(dx), abs(dy)) and sx and sy:
        out.append(mv(sx * (1 if dx > 0 else -1), sy * (1 if dy > 0 else -1)))
    out.append(mv(-dx, -dy))
    if dx and dy and abs(dx) != abs(dy):
        out.append(mv(abs(dy) * (1 if dx > 0 else -1), abs(dx) * (1 if dy > 0 else -1)))
    out.append(mv(dx + (1 if dx > 0 else -1 if dx < 0 else 0), dy + (1 if dy > 0 else -1 if dy < 0 else 0)))
    out.append(mv(dx, -dy) if dy else mv(-dx, dy))
    return out


def describe_e(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    parts = []
    if dx:
        parts.append("x: %s %s %s = %s, so %s %s" % (num(b[0]), MINUS, "(" + num(a[0]) + ")" if a[0] < 0 else num(a[0]), num(dx),
                                                    units(abs(dx)), "right" if dx > 0 else "left"))
    else:
        parts.append("x does not change")
    if dy:
        parts.append("y: %s %s %s = %s, so %s %s" % (num(b[1]), MINUS, "(" + num(a[1]) + ")" if a[1] < 0 else num(a[1]), num(dy),
                                                    units(abs(dy)), "up" if dy > 0 else "down"))
    else:
        parts.append("y does not change")
    return "Find the change: new minus old. " + "; ".join(parts) + ". The translation is %s." % mv(dx, dy)


def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, dx, dy in [((4, -3), -7, 0), ((-2, 5), 0, -6), ((-6, -1), 9, 0),
                      ((-4, 3), 6, -5), ((5, -2), -7, 4), ((-1, -6), 5, 8), ((6, 2), -4, -6)]:
        r = T(p, ("t", dx, dy))
        its.append(mcq("Translate %s %s. What are the coordinates of the image?" % (pair(*p), mv(dx, dy)),
                       pair(*r), trans_cands(p, dx, dy), step_e(p, ("t", dx, dy)), rnd))
    # grid: which point is the image of P?
    for p, dx, dy in [((-4, 1), 5, -4), ((5, -2), -7, 3), ((3, 4), -5, -2)]:
        r = T(p, ("t", dx, dy))
        swapped = (p[0] + (abs(dy) if dx > 0 else -abs(dy)), p[1] + (abs(dx) if dy > 0 else -abs(dx)))
        wrongway = (p[0] + dx, p[1] - dy)
        lines = (p[0] + dx + (1 if dx > 0 else -1), p[1] + dy + (1 if dy > 0 else -1))
        svg, ans, where = pick_grid(p, r, [swapped, wrongway, lines], pos)
        e = ("P is at %s. %s That is point %s. Point %s moves the wrong way up or down, point %s swaps the two amounts, "
             "and point %s comes from counting grid lines instead of spaces."
             % (pair(*p), step_e(p, ("t", dx, dy)), ans, where[wrongway], where[swapped], where[lines]))
        its.append(mcq_fixed(fig(svg) + "Point P is translated %s. Which point is its image?" % mv(dx, dy),
                             ["A", "B", "C", "D"], ans, e))
    # describe the translation from the coordinates
    for a, b in [((-4, 3), (2, -2)), ((6, -1), (-3, 4)), ((-1, -5), (-5, 2))]:
        dx, dy = b[0] - a[0], b[1] - a[1]
        e = describe_e(a, b)
        if a[0] * b[0] < 0:
            e += " The move crosses the y-axis, so the sizes add: %d + %d = %d." % (abs(a[0]), abs(b[0]), abs(dx))
        its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(a, b), e, rnd))
    # grid with two triangles
    A = [(-5, 3), (-2, 3), (-5, 5)]
    B = runs(A, [("t", 7, -6)])
    its.append(mcq(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B")) +
                   "Triangle B is a translation of triangle A. Describe the translation.",
                   mv(7, -6), [mv(-7, 6), mv(6, -7), mv(8, -7)],
                   "Pick one vertex and its image. The corner %s moves to %s. x: 2 %s (%s5) = 7, so 7 units right. "
                   "y: %s3 %s 3 = %s6, so 6 units down. Every vertex moves the same way." %
                   (pair(-5, 3), pair(2, -3), MINUS, MINUS, MINUS, MINUS, MINUS), rnd))
    its.append(mcq("A translation is written as (x, y) → (x + 3, y %s 5). Describe it in words." % MINUS, mv(3, -5),
                   [mv(-3, 5), mv(5, -3), mv(3, 5)],
                   "x + 3 makes x bigger by 3, so the point moves 3 units right. y %s 5 makes y smaller by 5, so it moves 5 units down." % MINUS, rnd))
    its.append(mcq("Which rule shows a translation 6 units left and 2 units up?", "(x %s 6, y + 2)" % MINUS,
                   ["(x + 6, y %s 2)" % MINUS, "(x %s 2, y + 6)" % MINUS, "(x + 6, y + 2)"],
                   "Left subtracts from x: x %s 6. Up adds to y: y + 2. So (x, y) → (x %s 6, y + 2)." % (MINUS, MINUS), rnd))
    tri = [(-5, 2), (-2, 2), (-2, 6)]
    img = runs(tri, [("t", 4, -7)])
    its.append(mcq("Triangle ABC has vertices A %s, B %s and C %s. It is translated %s. What are the vertices of the image?"
                   % (pair(*tri[0]), pair(*tri[1]), pair(*tri[2]), mv(4, -7)),
                   plist(img), [plist(runs(tri, [("t", -4, 7)])), plist(runs(tri, [("t", 7, -4)])), plist(runs(tri, [("t", 4, 7)]))],
                   "Add 4 to every x and subtract 7 from every y. A: %s. B: %s. C: %s." % (
                       pair(*img[0]), pair(*img[1]), pair(*img[2])), rnd))
    its.append(mcq("After a translation %s, the image of point A is %s. Where was point A before the move?" % (mv(-5, 3), pair(-2, 1)),
                   pair(3, -2), [pair(-7, 4), pair(3, 4), pair(-7, -2)],
                   "Undo the move: go 5 units right and 3 units down. x: %s. y: %s. A was at %s. Check: 5 left and 3 up from %s is %s."
                   % (add_e(-2, 5), add_e(1, -3), pair(3, -2), pair(3, -2), pair(-2, 1)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s translates %s 4 units down and gets %s. What mistake did %s make?" % (n, pair(-1, 5), pair(-5, 5), he),
                   "%s changed x instead of y" % H,
                   ["%s moved up instead of down" % H, "%s counted the grid lines" % H, "No mistake. %s is right" % H],
                   "Down changes only y: %s. The image is %s. %s subtracted 4 from x, which moves the point left." % (
                       add_e(5, -4), pair(-1, 1), n), rnd))
    its.append(mcq("A point moves from %s to %s. How far did it move?" % (pair(-5, -3), pair(3, -3)), "8 units right",
                   ["2 units right", "9 units right", "8 units left"],
                   "Only x changes. 3 %s (%s5) = 3 + 5 = 8, and it is positive, so the point moved 8 units right. "
                   "(2 comes from 5 %s 3: the move crosses the y-axis, so the sizes add.)" % (MINUS, MINUS, MINUS), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations on the Cartesian plane", "items": its}


# ------------------------------------------------------------ set 2: reflections in the axes
def other_axis(ax):
    return "ry" if ax == "rx" else "rx"


def axname(ax):
    return "x-axis" if ax == "rx" else "y-axis"


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, ax in [((4, -5), "ry"), ((-3, 6), "rx"), ((5, 2), "rx"), ((-6, -3), "ry"), ((-2, -4), "rx"), ((1, 6), "ry")]:
        r = T(p, (ax,))
        its.append(mcq("Reflect %s in the %s. What are the coordinates of the image?" % (pair(*p), axname(ax)),
                       pair(*r), [pair(*T(p, (other_axis(ax),))), pair(-p[0], -p[1]), pair(r[1], r[0])],
                       step_e(p, (ax,)), rnd))
    its.append(mcq("Reflect %s in the x-axis. What are the coordinates of the image?" % pair(-6, 0), pair(-6, 0),
                   [pair(6, 0), pair(0, -6), pair(0, 6)], step_e((-6, 0), ("rx",)), rnd))
    its.append(mcq("Reflect %s in the x-axis. What are the coordinates of the image?" % pair(0, 4), pair(0, -4),
                   [pair(0, 4), pair(4, 0), pair(-4, 0)],
                   "%s is on the y-axis, 4 units above the x-axis. Reflect in the x-axis: y changes sign, 4 → %s. "
                   "The image is 4 units below: %s." % (pair(0, 4), num(-4), pair(0, -4)), rnd))
    for p, ax, extra in [((-4, 3), "rx", (-4, 0)), ((5, -3), "ry", (-3, -5)), ((-2, -5), "rx", (-5, -2))]:
        r = T(p, (ax,))
        wrong = T(p, (other_axis(ax),))
        svg, ans, where = pick_grid(p, r, [wrong, (-p[0], -p[1]), extra], pos)
        e = "P is at %s. %s That is point %s. Point %s is the reflection in the %s instead, and point %s changes both signs." % (
            pair(*p), step_e(p, (ax,)), ans, where[wrong], axname(other_axis(ax)), where[(-p[0], -p[1])])
        its.append(mcq_fixed(fig(svg) + "Which point is the reflection of point P in the %s?" % axname(ax),
                             ["A", "B", "C", "D"], ans, e))
    for A, ax in [([(-5, 1), (-2, 1), (-2, 4)], "rx"), ([(-5, -2), (-2, -2), (-5, -5)], "ry")]:
        B = runs(A, [(ax,)])
        assert not maps(A, B, (other_axis(ax),)) and not maps(A, B, ("half",)) and not maps(A, B, "translation")
        k = 1
        e = ("Compare a vertex and its image: %s → %s. %s, so the shape flipped %s. The mirror line is the %s."
             % (pair(*A[k]), pair(*B[k]),
                "x stays the same and y changes sign" if ax == "rx" else "y stays the same and x changes sign",
                "up or down" if ax == "rx" else "left or right", axname(ax)))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its reflection B")) +
                             "Triangle B is the reflection of triangle A. Which axis is the mirror line?", AXES, "the " + axname(ax), e))
    for tri, ax in [([(2, 1), (5, 1), (5, 4)], "rx"), ([(-4, -2), (-1, -2), (-1, -5)], "ry")]:
        img = runs(tri, [(ax,)])
        sign = "y" if ax == "rx" else "x"
        its.append(mcq("A triangle has vertices %s. It is reflected in the %s. What are the vertices of the image?" % (plist(tri), axname(ax)),
                       plist(img), [plist(runs(tri, [(other_axis(ax),)])), plist(runs(tri, [("half",)])),
                                    plist([(q[1], q[0]) for q in img])],
                       "Reflect each vertex in the %s: keep the other coordinate and change the sign of %s. %s → %s."
                       % (axname(ax), sign, plist(tri), plist(img)), rnd))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(3, 4), pair(3, -4)), AXES,
                         "the x-axis", "x stays 3 and y changes sign (4 → %s), so the points flip up and down across the x-axis." % num(-4)))
    its.append(mcq("When you reflect a point in the x-axis, what changes?", "the sign of the y-coordinate",
                   ["the sign of the x-coordinate", "the signs of both coordinates", "the order of the numbers"],
                   "The x-axis is a mirror lying flat. The point flips up or down, so only y changes sign. Example: %s → %s."
                   % (pair(2, 5), pair(2, -5)), rnd))
    its.append(mcq_fixed("Point %s is reflected in the y-axis. Which quadrant is the image in?" % pair(-4, -2), QUADS, "Quadrant IV",
                         "The image is %s: x becomes positive and y stays negative. Right and down is Quadrant IV." % pair(4, -2)))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s in the x-axis and gets %s. What mistake did %s make?" % (n, pair(-5, 3), pair(5, 3), he),
                   "%s reflected in the y-axis" % H,
                   ["%s swapped x and y" % H, "%s changed both signs" % H, "No mistake. %s is right" % H],
                   "%s changed the sign of x. That is a reflection in the y-axis. In the x-axis, y changes sign: %s." % (H, pair(-5, -3)), rnd))
    its.append(mcq("Point Q is the reflection of point P in the y-axis. Q is at %s. Where is P?" % pair(-3, -6), pair(3, -6),
                   [pair(-3, 6), pair(3, 6), pair(-6, -3)],
                   "Reflecting in the y-axis changes the sign of x, and reflecting back does the same. %s → %s." % (pair(-3, -6), pair(3, -6)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in the x-axis and the y-axis", "items": its}


# ------------------------------------------------------------ set 3: rotations about the origin
TNAME = {"cw": "90° clockwise", "ccw": "90° counterclockwise", "half": "180°"}


def rot_cands(p, kind):
    """Rotating the wrong way, swapping the numbers without a sign change, mixing up 90° and 180°."""
    if kind == "half":
        out = [(-p[0], p[1]), (p[0], -p[1]), (p[1], p[0]), (-p[1], -p[0])]
    else:
        other = "ccw" if kind == "cw" else "cw"
        out = [T(p, (other,)), (p[1], p[0]), T(p, ("half",)), (-p[1], -p[0])]
    return [pair(*c) for c in out]


def set_rotate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, kind in [((3, 5), "cw"), ((-4, 2), "cw"), ((-1, -6), "cw"),
                    ((6, -3), "ccw"), ((2, 4), "ccw"), ((-5, 3), "ccw"),
                    ((4, -6), "half"), ((-2, -3), "half")]:
        r = T(p, (kind,))
        its.append(mcq("Rotate %s %s about the origin. What are the coordinates of the image?" % (pair(*p), TNAME[kind]),
                       pair(*r), rot_cands(p, kind), step_e(p, (kind,)), rnd))
    for p, kind in [((4, 2), "cw"), ((-3, 5), "ccw"), ((2, -4), "half")]:
        r = T(p, (kind,))
        if kind == "half":
            others = [(-p[0], p[1]), (p[0], -p[1]), (p[1], p[0])]
        else:
            others = [T(p, ("ccw" if kind == "cw" else "cw",)), (p[1], p[0]), T(p, ("half",))]
        svg, ans, where = pick_grid(p, r, others, pos)
        e = "P is at %s. %s That is point %s." % (pair(*p), step_e(p, (kind,)), ans)
        if kind == "half":
            e += " Points %s and %s change only one sign: those are reflections in an axis." % (where[others[0]], where[others[1]])
        else:
            e += " Point %s is a turn the wrong way, and point %s only swaps the numbers." % (where[others[0]], where[others[1]])
        its.append(mcq_fixed(fig(svg) + "Point P is rotated %s about the origin. Which point is the image?" % TNAME[kind],
                             ["A", "B", "C", "D"], ans, e))
    for A, kind in [([(1, 2), (5, 2), (1, 4)], "ccw"), ([(1, -2), (4, -2), (4, -5)], "cw")]:
        B = runs(A, [(kind,)])
        assert not any(maps(A, B, (k,)) for k in ("cw", "ccw", "half") if k != kind)
        e = ("Follow one vertex: %s → %s. %s The shape turned a quarter turn %s about the origin."
             % (pair(*A[1]), pair(*B[1]), step_e(A[1], (kind,)), "clockwise" if kind == "cw" else "counterclockwise"))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its rotation B")) +
                             "Triangle A is rotated about the origin to give triangle B. Describe the rotation.", TURNS4, TNAME[kind], e))
    its.append(mcq_fixed("Point %s is rotated about the origin and lands on %s. Describe the rotation." % (pair(2, 5), pair(5, -2)),
                         TURNS4, "90° clockwise",
                         "Try the rules. 90° clockwise: (x, y) → (y, %sx), so %s → %s. That matches. "
                         "(90° counterclockwise would give %s.)" % (MINUS, pair(2, 5), pair(5, -2), pair(-5, 2))))
    its.append(mcq_fixed("Point %s is rotated about the origin and lands on %s. Describe the rotation." % (pair(-4, 1), pair(4, -1)),
                         TURNS4, "180°",
                         "Both signs changed and the numbers stayed in the same order. That is a half turn: 180°."))
    its.append(mcq_fixed("Point %s is rotated 90° clockwise about the origin. Which quadrant is the image in?" % pair(-3, 4),
                         QUADS, "Quadrant I",
                         "%s is in Quadrant II. A quarter turn clockwise moves it to the next quadrant clockwise: "
                         "Quadrant I. Check: the image is %s." % (pair(-3, 4), pair(4, 3))))
    its.append(mcq_fixed("Point %s is rotated 180° about the origin. Which quadrant is the image in?" % pair(5, -2),
                         QUADS, "Quadrant II",
                         "A half turn changes both signs: %s → %s. Left and up is Quadrant II, the quadrant opposite Quadrant IV."
                         % (pair(5, -2), pair(-5, 2))))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s rotates %s 90° clockwise about the origin and gets %s. What mistake did %s make?" % (n, pair(4, 2), pair(-2, 4), he),
                   "%s turned it counterclockwise" % H,
                   ["%s swapped the numbers only" % H, "%s turned it 180°" % H, "No mistake. %s is right" % H],
                   "%s used the counterclockwise rule (%sy, x). Clockwise sends the top towards the right. %s"
                   % (n, MINUS, step_e((4, 2), ("cw",))), rnd))
    tri = [(1, 2), (5, 2), (5, 4)]
    img = runs(tri, [("half",)])
    its.append(mcq("A triangle has vertices %s. It is rotated 180° about the origin. What are the vertices of the image?" % plist(tri),
                   plist(img), [plist(runs(tri, [("rx",)])), plist(runs(tri, [("ry",)])), plist(runs(tri, [("cw",)]))],
                   "A 180° rotation changes both signs of every vertex: %s → %s." % (plist(tri), plist(img)), rnd))
    tri = [(1, 1), (4, 1), (4, 3)]
    img = runs(tri, [("ccw",)])
    its.append(mcq("A triangle has vertices %s. It is rotated 90° counterclockwise about the origin. What are the vertices of the image?" % plist(tri),
                   plist(img), [plist(runs(tri, [("cw",)])), plist([(q[1], q[0]) for q in tri]), plist(runs(tri, [("half",)]))],
                   "Use (x, y) → (%sy, x) on every vertex: swap the numbers, then change the sign of the first one. %s → %s."
                   % (MINUS, plist(tri), plist(img)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rotations of 90° and 180° about the origin", "items": its}


# ------------------------------------------------------------ set 4: dilations and similar shapes
def dil_cands(p, k):
    """Adding the scale factor, multiplying only one coordinate, doubling instead of halving."""
    k = Fraction(k)
    x, y = p
    if k == HALF:
        out = [(2 * x, 2 * y), T(p, ("d", k))[:1] + (y,), (x,) + T(p, ("d", k))[1:]]
    else:
        out = [(x + k, y + k), (k * x, y), (x, k * y)]
    return [pair(*(int(v) for v in c)) for c in out]


def kfixed():
    return [kname(HALF), "2", "3", "4"]


def set_dilate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, k in [((3, -2), 2), ((-4, 1), 3), ((-2, -5), 2), ((8, -6), HALF), ((-6, 4), HALF), ((1, -2), 3)]:
        st = ("d", k)
        its.append(mcq("Dilate %s by a scale factor of %s with the centre at the origin. What are the coordinates of the image?"
                       % (pair(*p), kname(k)), pair(*T(p, st)), dil_cands(p, k), step_e(p, st), rnd))
    for p, k in [((2, -3), 2), ((-2, 1), 3)]:
        r = T(p, ("d", k))
        added, xonly, yonly = (p[0] + k, p[1] + k), (k * p[0], p[1]), (p[0], k * p[1])
        svg, ans, where = pick_grid(p, r, [added, xonly, yonly], pos)
        e = ("P is at %s. %s That is point %s. Point %s comes from adding %d instead of multiplying, and points %s and %s "
             "multiply only one coordinate." % (pair(*p), step_e(p, ("d", k)), ans, where[added], k, where[xonly], where[yonly]))
        its.append(mcq_fixed(fig(svg) + "Point P is dilated by a scale factor of %d with the centre at the origin. Which point is the image?" % k,
                             ["A", "B", "C", "D"], ans, e))
    for A, k, at in [([(1, 1), (3, 1), (3, 2)], 2, (3.55, 1.45)), ([(2, 4), (6, 4), (6, 6)], HALF, None)]:
        B = runs(A, [("d", k)])
        big = k == 2
        e = ("Compare a vertex and its image: %s → %s. Each coordinate is multiplied by %s. Check a side: the bottom side of A is "
             "%d units long and the bottom side of B is %d units long. %s"
             % (pair(*A[1]), pair(*B[1]), kname(k), A[1][0] - A[0][0], B[1][0] - B[0][0],
                "B is bigger, so the scale factor is more than 1. (" + kname(HALF) + " would take B back to A.)" if big else
                "B is smaller, so the scale factor is less than 1. (2 would take B back to A.)"))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its dilation B",
                                           at_a=at if big else None, at_b=None if big else (2.0, 1.45))) +
                             "Triangle B is a dilation of triangle A with the centre at the origin. What is the scale factor?",
                             kfixed(), kname(k), e))
    rect = [(1, 1), (3, 1), (3, 2), (1, 2)]
    img = runs(rect, [("d", 3)])
    its.append(mcq("A rectangle has vertices %s. It is dilated by a scale factor of 3 with the centre at the origin. What are the vertices of the image?"
                   % plist(rect), plist(img),
                   [plist([(x + 3, y + 3) for x, y in rect]), plist([(3 * x, y) for x, y in rect]), plist([(x, 3 * y) for x, y in rect])],
                   "Multiply both coordinates of every vertex by 3: %s → %s. (Adding 3 slides the rectangle but keeps its size.)"
                   % (plist(rect), plist(img)), rnd))
    its.append(mcq("Point %s is dilated with the centre at the origin, and its image is %s. What is the scale factor?" % (pair(8, -4), pair(4, -2)),
                   kname(HALF), ["2", "4", MINUS + "4"],
                   "Image ÷ original: 4 ÷ 8 = %s and %s2 ÷ (%s4) = %s. Both coordinates are halved, so the scale factor is %s. "
                   "(2 is the scale factor from the image back to the original, and 4 or %s4 is the difference, not a scale factor.)"
                   % (kname(HALF), MINUS, MINUS, kname(HALF), kname(HALF), MINUS), rnd))
    its.append(mcq("A rectangle is 4 cm long and 3 cm wide. It is dilated by a scale factor of 2. What are the length and width of the image?",
                   "8 cm and 6 cm", ["6 cm and 5 cm", "8 cm and 3 cm", "2 cm and 1.5 cm"],
                   "Multiply every length by 2: 4 × 2 = 8 cm and 3 × 2 = 6 cm. Adding 2 to each side (6 cm and 5 cm) does not keep the same shape.", rnd))
    its.append(mcq("A triangle has an angle of 50°. It is dilated by a scale factor of 3. What is the matching angle in the image?",
                   "50°", ["150°", "53°", "It cannot be found"],
                   "A dilation changes the side lengths, not the angles. Matching angles in similar shapes are equal, so the angle is still 50°.", rnd))
    its.append(mcq("A triangle has a perimeter of 18 cm. It is dilated by a scale factor of %s. What is the perimeter of the image?" % kname(HALF),
                   "9 cm", ["36 cm", "17.5 cm", "4.5 cm"],
                   "Every side is multiplied by %s, so the perimeter is too: 18 × %s = 9 cm. (36 cm is multiplying by 2; 17.5 cm is subtracting %s.)"
                   % (kname(HALF), kname(HALF), kname(HALF)), rnd))
    its.append(mcq("A shape is dilated by a scale factor of 3. How is the image related to the original shape?",
                   "Similar: same shape, sides 3 times as long",
                   ["Congruent: same shape and same size", "Same shape, every side 3 cm longer", "Same sides, angles 3 times as large"],
                   "A dilation makes a similar shape. The angles stay the same and every side is multiplied by the scale factor, 3. "
                   "It is not congruent because the size changes.", rnd))
    its.append(mcq("A triangle has sides 3 cm, 4 cm and 5 cm. Which triangle is similar to it?",
                   "6 cm, 8 cm, 10 cm", ["5 cm, 6 cm, 7 cm", "6 cm, 8 cm, 5 cm", "4 cm, 5 cm, 6 cm"],
                   "Similar shapes have every side multiplied by the same scale factor. 3 × 2 = 6, 4 × 2 = 8 and 5 × 2 = 10. "
                   "Adding the same amount (5, 6, 7) or doubling only some sides (6, 8, 5) does not give a similar triangle.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s dilates %s by a scale factor of 3 with the centre at the origin and gets %s. What mistake did %s make?"
                   % (n, pair(4, -5), pair(7, -2), he),
                   "%s added 3 instead of multiplying" % H,
                   ["%s multiplied only x by 3" % H, "%s used a scale factor of %s" % (H, kname(Fraction(1, 3))), "No mistake. %s is right" % H],
                   "4 + 3 = 7 and %s5 + 3 = %s2, so %s added. Multiply instead. %s" % (MINUS, MINUS, he, step_e((4, -5), ("d", 3))), rnd))
    its.append(mcq_fixed("Which scale factor makes the image smaller than the original shape?", [kname(HALF), "1", "2", "3"], kname(HALF),
                         "A scale factor less than 1 shrinks the shape: %s makes every side half as long. "
                         "A scale factor of 1 keeps the same size, and 2 or 3 enlarges it." % kname(HALF)))
    end = (-6, 8)
    start = T(end, ("d", HALF))
    its.append(mcq("Point A is dilated by a scale factor of 2 with the centre at the origin. The image is %s. Where is point A?" % pair(*end),
                   pair(*start), [pair(-12, 16), pair(-4, 6), pair(-3, 8)],
                   "Undo the dilation: divide both coordinates by 2. %s ÷ 2 = %s and 8 ÷ 2 = 4, so A is %s. Check: %s"
                   % (num(-6), num(-3), pair(*start), step_e(start, ("d", 2))), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Dilations and similar shapes", "items": its}


# ------------------------------------------------------------ set 5: which transformation? and word problems
def is_dilation(a, b):
    for k in (2, 3, HALF, Fraction(1, 3), 4):
        if all(Fraction(x) * k == int(Fraction(x) * k) and Fraction(y) * k == int(Fraction(y) * k) for x, y in a):
            if same_set(runs(a, [("d", k)]), b):
                return True
    return False


SINGLE = {"a translation": "translation", "a reflection in the x-axis": ("rx",), "a reflection in the y-axis": ("ry",),
          "a rotation of 90° clockwise": ("cw",), "a rotation of 90° counterclockwise": ("ccw",), "a rotation of 180°": ("half",),
          "a dilation": "dilation"}
ORDER = list(SINGLE)


def maps2(a, b, what):
    if what == "dilation":
        return is_dilation(a, b)
    return maps(a, b, what)


def which_q(A, B, choices):
    """Exactly one of the choices maps A onto B."""
    choices = sorted(choices, key=ORDER.index)
    right = [c for c in choices if maps2(A, B, SINGLE[c])]
    assert len(right) == 1, (A, B, right)
    return choices, right[0]


def set_which(rnd, P):
    its = []
    four = ["a translation", "a reflection in the y-axis", "a rotation of 180°", "a dilation"]
    for A, st in [([(-5, 2), (-2, 2), (-5, 5)], ("t", 6, -6)), ([(-5, 1), (-2, 1), (-2, 3)], ("ry",)),
                  ([(2, 1), (5, 1), (2, 4)], ("half",)), ([(1, 1), (2, 1), (1, 2)], ("d", 3))]:
        B = runs(A, [st])
        ch, ans = which_q(A, B, four)
        if st[0] == "t":
            e = ("Triangle B is the same size and points the same way as triangle A: it only slid. That is a translation (%s)."
                 % mv(st[1], st[2]))
        elif st[0] == "d":
            e = ("Triangle B has the same shape as triangle A but is bigger, so it is a dilation. %s Translations, reflections "
                 "and rotations never change the size." % step_e(A[1], st))
        else:
            e = ("Follow one vertex: %s → %s. %s Check the other vertices: they all land on triangle B, so it is %s."
                 % (pair(*A[1]), pair(*B[1]), step_e(A[1], st), ans))
        at_a = (2.5, 1.5) if st[0] == "d" else None
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B", at_a=at_a)) +
                             "Which single transformation maps triangle A onto triangle B?", ch, ans, e))
    for A, st, choices in [
        ([(-1, 3), (-1, 5), (-4, 5)], ("cw",), ["a reflection in the x-axis", "a rotation of 90° clockwise", "a rotation of 90° counterclockwise", "a rotation of 180°"]),
        ([(1, 2), (2, 2), (2, 1)], ("d", 3), ["a translation", "a rotation of 90° clockwise", "a rotation of 180°", "a dilation"]),
    ]:
        B = runs(A, [st])
        ch, ans = which_q(A, B, choices)
        e = "Compare each vertex with its image. %s The rule works for every vertex, so it is %s." % (step_e(A[0], st), ans)
        if st[0] == "d":
            e += " The image is similar to the triangle, with sides 3 times as long."
        its.append(mcq_fixed("Triangle PQR has vertices %s. Its image has vertices %s, in the same order. Which single transformation was used?"
                             % (plist(A), plist(B)), ch, ans, e))
    its.append(mcq_fixed("Which transformation can change the size of a shape?", ["a translation", "a reflection", "a rotation", "a dilation"],
                         "a dilation",
                         "Translations, reflections and rotations give a congruent image (same size and shape). "
                         "A dilation gives a similar image that can be larger or smaller."))
    # word problems in Ontario contexts
    n, he, his = P.next()
    its.append(mcq("%s has a photo 4 cm wide and 6 cm tall. %s enlarges it by a scale factor of 3 for a Terry Fox Run poster. "
                   "What size is the enlarged photo?" % (n, he.capitalize()),
                   "12 cm by 18 cm", ["7 cm by 9 cm", "12 cm by 6 cm", "8 cm by 12 cm"],
                   "Multiply both lengths by 3: 4 × 3 = 12 cm and 6 × 3 = 18 cm. Adding 3 (7 cm by 9 cm) would stretch the photo out of shape.", rnd))
    its.append(mcq("On a grid map of a canoe trip in Algonquin Park, the campsite is at %s. A canoe paddles %s. Where does it land?"
                   % (pair(-5, -2), mv(7, 5)), pair(2, 3), trans_cands((-5, -2), 7, 5),
                   step_e((-5, -2), ("t", 7, 5)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a loon on a calm lake. The shoreline is the x-axis, and the tip of the loon’s beak is at %s. "
                   "%s draws the loon’s reflection in the water. Where is the tip of the reflected beak?" % (n, pair(3, 4), he.capitalize()),
                   pair(3, -4), [pair(-3, 4), pair(-3, -4), pair(4, -3)],
                   "The water line is the x-axis, so reflect in the x-axis: x stays 3, y changes sign. %s → %s." % (pair(3, 4), pair(3, -4)), rnd))
    its.append(mcq("A hockey coach draws a play on a grid with the origin at centre ice. A player starts at %s. The coach copies the play "
                   "to the other half of the rink by reflecting it in the y-axis. Where is the player’s image?" % pair(-4, 2),
                   pair(4, 2), [pair(-4, -2), pair(4, -2), pair(2, -4)], step_e((-4, 2), ("ry",)), rnd))
    its.append(mcq("A Ferris wheel at the CNE in Toronto is drawn on a grid with its centre at the origin. A seat is at %s. "
                   "The wheel turns 90° counterclockwise. Where is the seat now?" % pair(4, 3),
                   pair(-3, 4), rot_cands((4, 3), "ccw"), step_e((4, 3), ("ccw",)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a maple leaf logo with one tip at %s. To make a small button, %s dilates the logo by a scale factor of %s "
                   "with the centre at the origin. Where is that tip now?" % (n, pair(6, -4), he, kname(HALF)),
                   pair(3, -2), dil_cands((6, -4), HALF), step_e((6, -4), ("d", HALF)), rnd))
    its.append(mcq("A drawing of a canoe is 8 cm long. The class dilates it by a scale factor of %s to fit on a bookmark. How long is the canoe on the bookmark?"
                   % kname(HALF), "4 cm", ["16 cm", "7.5 cm", "2 cm"],
                   "Multiply by %s: 8 × %s = 4 cm. (16 cm is multiplying by 2, and 7.5 cm is subtracting %s.)" % (kname(HALF), kname(HALF), kname(HALF)), rnd))
    n, he, his = P.next()
    steps = [("cw",), ("d", 2)]
    r = run((2, 3), steps)
    its.append(mcq("In a coding app, %s’s sprite is at %s. %s rotates it 90° clockwise about the origin, then dilates it by a scale factor of 2 "
                   "with the centre at the origin. Where does it end up?" % (n, pair(2, 3), he.capitalize()),
                   pair(*r), [pair(*run((2, 3), [("ccw",), ("d", 2)])), pair(*T(T((2, 3), ("cw",)), ("t", 2, 2))), pair(*T((2, 3), ("cw",)))],
                   "Do the steps in order. " + steps_e((2, 3), steps), rnd))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert run((3, -5), [("half",)]) == run((3, -5), [("rx",), ("ry",)]) == (-3, 5)
    its.append(mcq_fixed("A game piece moves from %s to %s. %s says it was a rotation of 180° about the origin. %s says it was a reflection in "
                         "the x-axis, then a reflection in the y-axis. Who is right?" % (pair(3, -5), pair(-3, 5), n1, n2),
                         ["Only %s" % n1, "Only %s" % n2, "Both of them", "Neither of them"], "Both of them",
                         "180° rotation: both signs change, %s → %s. Two reflections: %s → %s → %s. Both give the same image."
                         % (pair(3, -5), pair(-3, 5), pair(3, -5), pair(3, 5), pair(-3, 5))))
    n, he, his = P.next()
    its.append(mcq_fixed("%s designs a snow fort on a grid. A corner of the small plan is at %s, and the same corner on the big plan is at %s. "
                         "The big plan is a dilation of the small one with the centre at the origin. What is the scale factor?"
                         % (n, pair(2, -1), pair(6, -3)), kfixed(), "3",
                         "Image ÷ original: 6 ÷ 2 = 3 and %s3 ÷ (%s1) = 3. The scale factor is 3. (4 is the difference 6 %s 2, not a scale factor.)"
                         % (MINUS, MINUS, MINUS)))
    n, he, his = P.next()
    end = (2, -5)
    start = T(end, ("ccw",))
    assert T(start, ("cw",)) == end
    its.append(mcq("In a board game, %s’s piece is rotated 90° clockwise about the origin and ends at %s. Where did it start?" % (n, pair(*end)),
                   pair(*start), [pair(*T(end, ("cw",))), pair(*T(end, ("half",))), pair(-5, 2)],
                   "Undo the turn by turning the other way. %s Check: %s" % (step_e(end, ("ccw",)), step_e(start, ("cw",))), rnd))
    n, he, his = P.next()
    a, b = (-5, 2), (2, -3)
    assert run(a, [("t", 4, -3), ("t", 3, -2)]) == b
    its.append(mcq("%s plans a bike ride on a grid map of Ottawa. From %s, %s rides %s, then %s. Which single translation "
                   "takes %s from the start to the end?" % (n, pair(*a), he, mv(4, -3), mv(3, -2), "her" if he == "she" else "him"),
                   mv(7, -5), [mv(1, -1), mv(7, 5), mv(-7, 5)],
                   "Add the moves. x: 4 + 3 = 7, so 7 units right. y: %s3 + (%s2) = %s5, so 5 units down. Check: %s → %s."
                   % (MINUS, MINUS, MINUS, pair(*a), pair(*b)), rnd))
    its.append(mcq("A teacher enlarges a triangle with angles 30°, 60° and 90° by a scale factor of 2 for a bulletin board. What are the angles of the enlarged triangle?",
                   "30°, 60° and 90°", ["60°, 120° and 180°", "32°, 62° and 92°", "15°, 30° and 45°"],
                   "A dilation makes a similar triangle. The sides double, but the angles stay the same: 30°, 60° and 90°. "
                   "(The angles of any triangle add up to 180°, so they cannot all double.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Which transformation? Word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    A = [(-4, 1), (-1, 1), (-4, 3)]
    B = runs(A, [("t", 5, -4)])
    assert B == [(1, -3), (4, -3), (1, -1)]
    G = Grid(5)
    G.poly(A, RED, "A").poly(B, GREEN, "B")
    G.arrow((-1, 1), (4, 1)).arrow((4, 1), (4, -3))
    G.note(1.5, 1.5, "right 5").note(3.8, 0.45, "down 4", anchor="end")
    trans = G.svg("triangle A translated 5 units right and 4 units down to triangle B")
    A = [(1, 1), (4, 1), (1, 3)]
    G = Grid(5)
    G.poly(A, RED, "A").poly(runs(A, [("ry",)]), GREEN, "B").poly(runs(A, [("rx",)]), BLUE, "C")
    refl = G.svg("triangle A reflected in the y-axis to triangle B and in the x-axis to triangle C")
    A = [(1, 2), (4, 2), (1, 4)]
    B = runs(A, [("cw",)])
    assert B == [(2, -1), (2, -4), (4, -1)]
    G = Grid(5)
    G.poly(A, RED, "A").poly(B, GREEN, "B")
    G.arc((4, 2), (2, -4), True)
    rota = G.svg("triangle A rotated 90° clockwise about the origin to triangle B")
    A = [(1, 1), (3, 1), (1, 2)]
    B = runs(A, [("d", 2)])
    assert B == [(2, 2), (6, 2), (2, 4)]
    G = Grid(6)
    for q in B:
        G.seg((0, 0), q, BLUE, 1.5, dash=True)
    G.poly(A, RED).poly(B, GREEN)
    G.note(2.75, 0.4, "A", col=RED, fs=16).note(3.5, 2.7, "B", col=GREEN, fs=16)
    dil = G.svg("triangle A dilated by a scale factor of 2 with the centre at the origin to triangle B")
    return (
        "<h2>Four kinds of transformation</h2>"
        "<p>A <b>transformation</b> moves or resizes a shape on the Cartesian plane. The new shape is called the <b>image</b>. "
        "Translations, reflections and rotations keep the size, so the image is <b>congruent</b>. "
        "A dilation changes the size, so the image is <b>similar</b>.</p>" +
        table(["Transformation", "What it does", "Rule for (x, y)"], [
            ["Translation", "slides the shape", "add or subtract: (x + a, y + b)"],
            ["Reflection in the x-axis", "flips it up or down", "(x, −y)"],
            ["Reflection in the y-axis", "flips it left or right", "(−x, y)"],
            ["Rotation of 90° clockwise", "turns it a quarter turn", "(y, −x)"],
            ["Rotation of 90° counterclockwise", "turns it a quarter turn the other way", "(−y, x)"],
            ["Rotation of 180°", "turns it a half turn", "(−x, −y)"],
            ["Dilation by scale factor k", "makes it larger or smaller", "(kx, ky)"],
        ]) +
        "<p>Rotations and dilations here use the origin, (0, 0), as the centre. Move every vertex with the same rule, then join the new vertices.</p>"
        "<h2>Translations</h2>"
        "<p>Right adds to x and left subtracts from x. Up adds to y and down subtracts from y.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A moves 5 units right and 4 units down. The vertex (−1, 1) goes to (4, −3).</figcaption></figure>" +
        ex("Example", "Translate (−2, 4) 5 units right and 7 units down.", "x: −2 + 5 = 3. y: 4 − 7 = −3.", "(3, −3)") +
        ex("Example", "Describe the move from (−3, 2) to (4, −1).",
           "New minus old. x: 4 − (−3) = 7, so 7 units right. y: −1 − 2 = −3, so 3 units down.", "7 units right and 3 units down") +
        "<h2>Reflections in the axes</h2>"
        "<p>The axis is the mirror line. In the <b>x-axis</b>, the sign of <b>y</b> changes. "
        "In the <b>y-axis</b>, the sign of <b>x</b> changes. Each image is the same distance from the mirror as the shape.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>A is reflected in the y-axis to give B, and in the x-axis to give C. The vertex (4, 1) goes to (−4, 1) and to (4, −1).</figcaption></figure>" +
        ex("Example", "Reflect (−4, 5) in the x-axis.", "x stays −4. y changes sign: 5 → −5.", "(−4, −5)") +
        "<h2>Rotations about the origin</h2>"
        "<p>For a quarter turn, swap the two numbers, then change one sign. Clockwise (the way clock hands move): change the sign of the "
        "<b>second</b> number. Counterclockwise: change the sign of the <b>first</b> number. For a half turn (180°), change both signs.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A turns 90° clockwise about the origin. The vertex (4, 2) goes to (2, −4).</figcaption></figure>" +
        ex("Example", "Rotate (2, 5) 90° counterclockwise about the origin.",
           "Swap: (5, 2). Change the sign of the first number: (−5, 2). Check: (2, 5) is in Quadrant I, and a counterclockwise quarter turn "
           "takes it to Quadrant II.", "(−5, 2)") +
        "<h2>Dilations</h2>"
        "<p>A <b>dilation</b> with the centre at the origin <b>multiplies</b> both coordinates by the <b>scale factor</b>. "
        "A scale factor greater than 1 enlarges the shape; a scale factor between 0 and 1, like " + kname(HALF) + ", shrinks it. "
        "The image is <b>similar</b> to the original: the angles stay the same and every side is multiplied by the scale factor.</p>"
        "<figure class='sn-fig'>" + dil +
        "<figcaption>Triangle A is dilated by a scale factor of 2. The vertex (3, 1) goes to (6, 2), twice as far from the origin. "
        "The bottom side grows from 2 units to 4 units.</figcaption></figure>" +
        ex("Example", "Dilate (−3, 2) by a scale factor of 3 with the centre at the origin.", "−3 × 3 = −9 and 2 × 3 = 6.", "(−9, 6)") +
        ex("Example", "Dilate (8, −6) by a scale factor of " + kname(HALF) + ".", "Halve both coordinates: 8 ÷ 2 = 4 and −6 ÷ 2 = −3.", "(4, −3)") +
        ex("Similar shapes", "A rectangle 5 cm by 2 cm is dilated by a scale factor of 3. Find the new size.",
           "Multiply every side by 3: 5 × 3 = 15 and 2 × 3 = 6. The angles are still 90°.", "15 cm by 6 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Translating the wrong way", "Right and up add; left and down subtract"],
            ["From −6 to 1 doing 6 − 1 = 5", "New minus old: 1 − (−6) = 7"],
            ["Reflecting in the wrong axis", "In the x-axis, y changes sign. In the y-axis, x changes sign"],
            ["Rotating the wrong way", "Clockwise goes the way clock hands move: from the top to the right"],
            ["Only swapping the numbers in a 90° turn: (3, 1) → (1, 3)", "Swap and change one sign: (1, −3) clockwise, (−1, 3) counterclockwise"],
            ["Adding the scale factor: (4, −5) by 3 → (7, −2)", "Multiply both coordinates: (12, −15)"],
            ["Multiplying only one coordinate", "Multiply x and y by the same scale factor"],
            ["Thinking a dilation changes the angles", "Angles stay the same; only the side lengths change"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about transformations in the Ontario math curriculum?",
     "a": "In Grade 7 Spatial Sense (E1.3 and E1.4), students perform dilations and describe how the image is similar to the original shape, and they use translations, reflections and rotations on the Cartesian plane in all four quadrants."},
    {"q": "What is a dilation in Grade 7 math?",
     "a": "A dilation enlarges or shrinks a shape by a scale factor. With the centre at the origin, multiply both coordinates by the scale factor: (3, −2) dilated by 2 becomes (6, −4)."},
    {"q": "Is a dilated shape similar or congruent?",
     "a": "It is similar: the angles stay the same and every side is multiplied by the scale factor. It is congruent only if the scale factor is 1, which keeps the same size."},
    {"q": "How do you rotate a point 90° about the origin?",
     "a": "Swap the two numbers, then change one sign. For 90° clockwise, (x, y) becomes (y, −x); for 90° counterclockwise, it becomes (−y, x). A 180° turn changes both signs."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    stay as they are; the other questions fill the gaps."""
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
    rnd = random.Random(47817)
    P = People(rnd)
    sets = [set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P), set_dilate(rnd, P), set_which(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "/", x) for x in it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "transformations-and-dilations", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Transformations and Dilations: Translations, Reflections, Rotations and Similar Shapes",
        "seo_title": "Grade 7 Math: Transformations and Dilations Worksheets (Free, Ontario Curriculum, Answer Key)",
        "short_title": "Transformations and dilations",
        "domain": "Spatial Sense",
        "standard_code": "Grade 7: E1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Perform dilations and describe the similarity between the image and the original shape",
        "meta_desc": "Free Grade 7 math worksheets on transformations for the Ontario curriculum: translate points, reflect them in the x- and y-axis, rotate them 90° and 180° about the origin, dilate shapes by a scale factor of 2, 3 or 1/2 and describe similar shapes. 100 questions with an answer key.",
        "key_big": "A dilation multiplies both coordinates by the scale factor. The image is similar: same angles, sides scaled.",
        "key_sub": "Translation: right and up add, left and down subtract. Reflection in the x-axis changes the sign of y; in the y-axis, the sign of x. Rotation about the origin: 90° clockwise (x, y) → (y, −x), 90° counterclockwise (−y, x), 180° (−x, −y). Dilation by k: (kx, ky).",
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
        mark_large(u, "coordinate grid")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
