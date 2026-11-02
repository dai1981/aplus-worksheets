# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Tessellations and transformations
(Ontario Curriculum 2020, Spatial Sense E1.1 and E1.4)
  python3 tools/gen_caon_math_g8_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

Canadian English (counterclockwise, centre, neighbour). Grid helpers and point transformations come from
gen_caon_math_g7_transformations.py; tessellation pictures (exact regular polygons, border strips, quilt block)
come from gen_au_maths_y6_tessellations.py. Whole-number coordinates; every grid runs from −6 to 6 (lesson
grids −5 to 5), is square and exact, and is drawn from the data. Negative numbers use the real minus sign.
Every image is computed by T(); every "which transformation" answer is checked: the right one maps the shape
onto the image and no wrong choice does. Angles at a point are checked in code (interior(n) and 360°).
Wrong answers come from real Grade 8 mistakes: thinking every regular polygon (pentagon, octagon) tessellates,
mixing up interior and exterior angles, rotating the wrong way, only swapping the numbers in a 90° turn,
reflecting in the wrong axis or line, stopping on the mirror line, adding the scale factor, multiplying only one
coordinate, using the inverse scale factor, doubling the area instead of multiplying by 4, and doing the steps
of a combination in the wrong order.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
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
SHADE = "#4fae74"
SHADE_B = "#6d9fd8"
THIN = "#a8a8a8"
LETTERS = ["A", "B", "C", "D"]


def T(p, st):
    """One transformation. t = translation, rx / ry = reflection in an axis, vx = in the line x = a,
    hy = in the line y = b, cw / ccw / half = rotation about the origin, d = dilation, centre at the origin."""
    x, y = p
    k = st[0]
    if k == "t":
        return (x + st[1], y + st[2])
    if k == "rx":
        return (x, -y)
    if k == "ry":
        return (-x, y)
    if k == "vx":
        return (2 * st[1] - x, y)
    if k == "hy":
        return (x, 2 * st[1] - y)
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
    if k in ("vx", "hy"):
        i = 0 if k == "vx" else 1
        a = st[1]
        v = p[i]
        line = "%s = %s" % ("x" if k == "vx" else "y", num(a))
        if v == a:
            return "%s is on the mirror line %s, so it stays at %s." % (pair(*p), line, pair(*r))
        d = abs(v - a)
        if k == "vx":
            side, other = ("right", "left") if v > a else ("left", "right")
        else:
            side, other = ("above", "below") if v > a else ("below", "above")
        far = "%s of" % side if k == "vx" else side
        oth = "%s of" % other if k == "vx" else other
        new = a - (v - a)
        return ("%s is %s %s the line %s, so the image is %s %s it: %s = %s %s %d = %s. %s stays %s. %s → %s."
                % (pair(*p), units(d), far, line, units(d), oth, "x" if k == "vx" else "y", num(a),
                   "+" if new > a else MINUS, d, num(new), "y" if k == "vx" else "x", num(p[1 - i]), pair(*p), pair(*r)))
    if k == "cw":
        return ("Rotate 90° clockwise: (x, y) → (y, %sx). Swap the numbers, then change the sign of the second one. %s → %s."
                % (MINUS, pair(*p), pair(*r)))
    if k == "ccw":
        return ("Rotate 90° counterclockwise: (x, y) → (%sy, x). Swap the numbers, then change the sign of the first one. %s → %s."
                % (MINUS, pair(*p), pair(*r)))
    if k == "d":
        f = Fraction(st[1])
        if f.denominator == 1:
            return ("Dilate by %s: multiply both coordinates by %s. %s × %s = %s and %s × %s = %s. %s → %s."
                    % (f, f, num(p[0]), f, num(r[0]), num(p[1]), f, num(r[1]), pair(*p), pair(*r)))
        if f.numerator == 1:
            return ("Dilate by %s: multiply both coordinates by %s, which is the same as dividing by %d. %s ÷ %d = %s and %s ÷ %d = %s. %s → %s."
                    % (kname(f), kname(f), f.denominator, num(p[0]), f.denominator, num(r[0]), num(p[1]), f.denominator, num(r[1]),
                       pair(*p), pair(*r)))
        n, dd = f.numerator, f.denominator
        return ("Dilate by %s: divide each coordinate by %d, then multiply by %d. %s ÷ %d × %d = %s and %s ÷ %d × %d = %s. %s → %s."
                % (kname(f), dd, n, num(p[0]), dd, n, num(r[0]), num(p[1]), dd, n, num(r[1]), pair(*p), pair(*r)))
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


def mcq_num(q, correct, cands, e, fmt="%d"):
    ch = []
    for c in cands:
        if c >= 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [fmt % c for c in ch], fmt % correct, e)


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


# ------------------------------------------------------------ set 1: which shapes tessellate?
def an(word):
    return ("an " if word[0] in "aeiou" else "a ") + word


def set_tessellate(rnd, P):
    its = []
    pos = Pos(rnd)
    for n, wrong in [(4, [3, 5, 2]), (3, [3, 4, 5]), (6, [2, 4, 6])]:
        a = interior(n)
        k = 360 // a
        assert k * a == 360
        its.append(mcq_num(fig(angle_svg(n, "%d°" % a)) + "Each angle of %s is %d°. How many %ss fit together around one point with no gaps?"
                           % (an(NAME[n]), a, NAME[n]), k, [w for w in wrong if w != k],
                           "The angles around a point add up to 360°. 360° ÷ %d° = %d, so %d %ss fit exactly around each point."
                           % (a, k, k, NAME[n])))
    assert interior(5) == 108 and interior(8) == 135
    its.append(mcq_num("What is the size of each angle of a regular pentagon?", 108, [72, 540, 120],
                       "The angles of a pentagon add up to (5 %s 2) × 180° = 540°. A regular pentagon has 5 equal angles: 540° ÷ 5 = 108°. "
                       "(72° is the turn at each corner as you walk around it, and 540° is the total.)" % MINUS, fmt="%d°"))
    its.append(mcq_num("What is the size of each angle of a regular octagon?", 135, [45, 1080, 120],
                       "The angles of an octagon add up to (8 %s 2) × 180° = 1080°. 1080° ÷ 8 = 135°. "
                       "(45° is the turn at each corner, 1080° is the total, and 120° is the angle of a regular hexagon.)" % MINUS, fmt="%d°"))
    its.append(mcq(fig(angle_svg(5, "108°")) + "Each angle of a regular pentagon is 108°. Do regular pentagons tessellate on their own?",
                   "No: 3 × 108° = 324°, which leaves a gap",
                   ["Yes: 3 regular pentagons fit exactly", "Yes: 4 regular pentagons fit exactly", "Yes: every regular polygon tessellates"],
                   "3 × 108° = 324°, which is less than 360°, so there is a gap. 4 × 108° = 432°, which is more than 360°, "
                   "so a fourth pentagon would overlap. Regular pentagons do not tessellate.", rnd))
    its.append(mcq_num(fig(vertex_svg([5, 5, 5], "?", "three regular pentagons around a point with a gap")) +
                       "Three regular pentagons meet at the red dot. Each angle is 108°. What is the size of the gap?",
                       36, [72, 108, 54],
                       "3 × 108° = 324°. A full turn is 360°, so the gap is 360° %s 324° = 36°. No regular polygon has a 36° angle."
                       % MINUS, fmt="%d°"))
    its.append(mcq(fig(angle_svg(8, "135°")) + "Each angle of a regular octagon is 135°. Why do regular octagons not tessellate on their own?",
                   "2 make 270° (a gap) and 3 make 405° (an overlap)",
                   ["They have too many sides", "135° is an obtuse angle", "Their sides are too short"],
                   "Around a point the angles must add up to exactly 360°. 2 × 135° = 270° leaves a gap and 3 × 135° = 405° is too much. "
                   "135° does not divide exactly into 360°. (Regular hexagons have obtuse angles too, and they do tessellate.)", rnd))
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
                         "The regular pentagon (%s): 360° ÷ 108° is not a whole number. Squares (4 × 90°), equilateral triangles (6 × 60°) "
                         "and regular hexagons (3 × 120°) all fit exactly around a point." % "ABCD"[p]))
    its.append(mcq("Which regular polygons tessellate on their own?", "Only equilateral triangles, squares and regular hexagons",
                   ["Every regular polygon", "Only squares", "Every regular polygon with an even number of sides"],
                   "A regular polygon tessellates only if its angle divides exactly into 360°: 60° (6 fit), 90° (4 fit) and 120° (3 fit). "
                   "Regular pentagons (108°) and octagons (135°) do not, even though an octagon has an even number of sides.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says, “All regular polygons tessellate.” Which shape shows that %s is wrong?" % (n, he), "a regular pentagon",
                   ["a square", "an equilateral triangle", "a regular hexagon"],
                   "Regular pentagons leave a 36° gap around a point (3 × 108° = 324°). Squares, equilateral triangles and regular hexagons "
                   "do tessellate, so they cannot show that %s is wrong." % n, rnd))
    its.append(mcq_num("Copies of any triangle tessellate. A triangle has angles of 40°, 60° and 80°. In its tessellation, each angle appears twice "
                       "at every meeting point. How many triangles meet at each point?", 6, [3, 4, 2],
                       "Each angle appears twice: 2 × (40° + 60° + 80°) = 2 × 180° = 360°. That is 6 angles, so 6 triangles meet at each point. "
                       "(3 triangles give only 180°.)"))
    its.append(mcq("Does every quadrilateral (even an irregular one) tessellate?", "Yes: its four angles add up to 360°",
                   ["No: only squares and rectangles do", "No: its sides must be equal", "Only if it has a right angle"],
                   "The angles of any quadrilateral add up to 360°. Put one copy of each angle around a point and they fill it exactly, "
                   "so any quadrilateral tessellates.", rnd))
    its.append(mcq_num(fig(vertex_svg([8, 8], "?", "two regular octagons around a point with a gap")) +
                       "Two regular octagons meet at the red dot. Each angle is 135°. What is the size of the gap?",
                       90, [45, 135, 270],
                       "2 × 135° = 270°, and 360° %s 270° = 90°. A square fits the gap exactly, so octagons and squares tessellate together." % MINUS,
                       fmt="%d°"))
    its.append(mcq_num(fig(vertex_svg([6, 6], "?", "two regular hexagons around a point with a gap")) +
                       "Two regular hexagons meet at the red dot. How many equilateral triangles fill the gap?", 2, [1, 3, 4],
                       "2 × 120° = 240°, so the gap is 360° %s 240° = 120°. Each equilateral triangle has 60° angles: 120° ÷ 60° = 2 triangles." % MINUS))
    its.append(mcq_num("Two squares meet at a point. How many equilateral triangles fill the rest of the space around the point?", 3, [2, 4, 6],
                       "2 × 90° = 180°, so 360° %s 180° = 180° is left. 180° ÷ 60° = 3 equilateral triangles." % MINUS))
    its.append(mcq_num("At each corner of a tiling, a regular hexagon, two squares and one more regular polygon meet. What is the angle of the missing polygon?",
                       60, [150, 90, 120],
                       "120° + 90° + 90° = 300°. 360° %s 300° = 60°, so the missing tile is an equilateral triangle. "
                       "(150° forgets the second square.)" % MINUS, fmt="%d°"))
    its.append(mcq("Each angle of a regular dodecagon (12 sides) is 150°. Does it tessellate on its own?",
                   "No: 2 make 300° and 3 make 450°",
                   ["Yes: it has an even number of sides", "Yes: 150° is less than 180°", "Yes: 12 divides into 360"],
                   "2 × 150° = 300° leaves a 60° gap and 3 × 150° = 450° overlaps. 360° ÷ 150° is not a whole number, so it does not "
                   "tessellate on its own. (An equilateral triangle could fill the 60° gap.)", rnd))
    its.append(mcq_num("In a tessellation, what do the angles that meet at a point add up to?", 360, [180, 90, 540],
                       "The tiles go all the way around the point with no gaps and no overlaps: a full turn, 360°. "
                       "(180° is the sum of the angles on a straight line or in a triangle.)", fmt="%d°"))
    its.insert(0, its.pop())          # the basic fact first
    assert len(its) == 20, len(its)
    return {"title": "Which shapes tessellate? Angles at a point", "items": its}


# ------------------------------------------------------------ set 2: transformations in tessellations
STRIP = ["a translation", "a reflection", "a rotation of 180°", "a reflection and a translation"]


def set_patterns(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq(fig(patch_svg("brick", label="brick wall pattern")) + "In this brick wall, how is each row placed compared with the row below it?",
                   "translated half a brick along",
                   ["reflected in a vertical line", "rotated 90°", "exactly above the row below"],
                   "Each row is the row below slid half a brick sideways and up one row. Nothing is flipped or turned, so it is a translation.", rnd))
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
                                 "with the mirror line on the edge between the tiles. A rotation of 180° would also turn it upside down."),
        ("half", "a rotation of 180°", "Each flag is upside down and points the other way. It is the one before rotated 180° about the middle "
                                       "of the edge between the tiles. A reflection flips it only one way."),
        ("glide", "a reflection and a translation", "Each flag is upside down but still points right. It is reflected in the line across the middle "
                                                    "of the strip and then slid 1 tile along, like a trail of footprints."),
    ]:
        its.append(mcq_fixed(fig(strip_svg(kind)) + q, STRIP, ans, e))
    p = pos.next()
    right = cwk(FLAG_SQ, 3)
    wr = [("it is turned counterclockwise, back to the second tile", cwk(FLAG_SQ, 1)),
          ("it is a mirror image of the right answer, flipped, not turned", flipx(cwk(FLAG_SQ, 3))),
          ("it is turned 90° too far, back to the start", cwk(FLAG_SQ, 0))]
    rnd.shuffle(wr)
    opts = [w[1] for w in wr]
    opts.insert(p, right)
    assert len({key_of(o) for o in opts}) == 4
    others = "; ".join("%s: %s" % ("ABCD"[j], w[0]) for j, w in zip([j for j in range(4) if j != p], wr))
    its.append(mcq_fixed(fig(next_svg(opts)) + "Each tile is the tile before rotated 90° clockwise. Which tile comes next?", LETTERS, "ABCD"[p],
                         "The flag on the pole points right, then down, then left. One more turn of 90° clockwise makes it point up: <b>%s</b>. "
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
    nxt = [(100 - y, x) for x, y in QUILT_T]
    assert key_of(nxt) != key_of([(100 - x, y) for x, y in QUILT_T]) and key_of(nxt) != key_of([(x + 50, y) for x, y in QUILT_T])
    assert key_of(nxt) != key_of([(100 - x, 100 - y) for x, y in QUILT_T])
    its.append(mcq(fig(quilt_svg()) + "This quilt block has 4 small squares. Going around clockwise, how is each small square made from the one before it?",
                   "a rotation of 90° clockwise about the centre of the block",
                   ["a reflection in the line between them", "a translation", "a rotation of 180° about the centre of the block"],
                   "Look at the long side of each red triangle: it lies along the top of the block, then the right side, then the bottom, "
                   "then the left. Each square is the one before rotated 90° clockwise about the centre. A reflection would make a mirror image.", rnd))
    its.append(mcq("An artist cuts a bump out of the left side of a square tile and attaches the same bump to the right side, without turning it. "
                   "Will copies of the new tile still tessellate?", "Yes: each bump fits into the gap in the next tile",
                   ["No: only regular polygons tessellate", "No: curved edges always leave gaps", "Only if the bump is cut off again"],
                   "The bump was translated from one side to the opposite side, so the gap matches the bump exactly. "
                   "The artist M. C. Escher used this idea to make tessellations of birds, fish and lizards.", rnd))
    its.append(mcq("A triangle is rotated 180° about the midpoint of one of its sides. "
                   "What shape do the triangle and its image make together?", "a parallelogram",
                   ["a bigger triangle", "a kite", "a regular hexagon"],
                   "The 180° rotation puts a copy of the triangle against the same side, upside down. Together they make a parallelogram. "
                   "Rows of parallelograms tessellate, which is why every triangle tessellates.", rnd))
    its.append(mcq("In a tessellation of an irregular quadrilateral, which transformation maps a tile onto the tile that shares one of its sides?",
                   "a rotation of 180° about the midpoint of that side",
                   ["a reflection in that side", "a rotation of 90° about a corner", "a dilation by a scale factor of 2"],
                   "Turning the tile 180° about the midpoint of a side puts the same side back in place, with the matching angles beside each other. "
                   "A reflection of an irregular shape would not fit the pattern, and a dilation changes the size.", rnd))
    its.append(mcq("A trail of footprints in fresh snow goes left foot, right foot, left foot, right foot. How is each footprint made from the one before?",
                   "a reflection and a translation",
                   ["only a translation", "only a reflection", "a rotation of 180°"],
                   "A right foot is a mirror image of a left foot, so there is a reflection. The footprint is also further along the path, "
                   "so there is a translation too.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s rotates a square tile 90° about one corner, again and again. How many tiles fit around that corner?" % n,
                   "4", ["2", "3", "8"],
                   "Each turn is 90°. 360° ÷ 90° = 4, so 4 tiles fill the space around the corner.", rnd))
    its.append(mcq("Which tile could NOT be used on its own to cover a floor with no gaps?", "a regular octagon",
                   ["a rectangle", "a regular hexagon", "an equilateral triangle"],
                   "Regular octagons (135°) leave square gaps, which is why octagon floors have small square tiles between them. "
                   "Rectangles, regular hexagons and equilateral triangles cover a floor on their own.", rnd))
    its.append(mcq("A design has 1 regular hexagon and some equilateral triangles at every corner. "
                   "How many triangles are at each corner?", "4", ["2", "3", "6"],
                   "The hexagon’s angle is 120°, so 360° %s 120° = 240° is left. 240° ÷ 60° = 4 triangles." % MINUS, rnd))
    its.append(mcq("In a honeycomb pattern, which transformation moves a hexagon onto the next hexagon in the same row?", "a translation",
                   ["a reflection only", "a rotation of 90°", "a dilation"],
                   "All the hexagons face the same way, so each one is the one before slid along: a translation. "
                   "A 90° turn would not put a hexagon onto its neighbour, and a dilation changes the size.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Transformations in tessellations", "items": its}


# ------------------------------------------------------------ set 3: translations, reflections and rotations
TNAME = {"cw": "90° clockwise", "ccw": "90° counterclockwise", "half": "180°"}
RULES = ["a reflection in the x-axis", "a reflection in the y-axis", "a rotation of 90° clockwise", "a rotation of 180°"]


def other_axis(ax):
    return "ry" if ax == "rx" else "rx"


def axname(ax):
    return "x-axis" if ax == "rx" else "y-axis"


def rot_cands(p, kind):
    """Rotating the wrong way, swapping the numbers without a sign change, mixing up 90° and 180°."""
    if kind == "half":
        out = [(-p[0], p[1]), (p[0], -p[1]), (p[1], p[0]), (-p[1], -p[0])]
    else:
        other = "ccw" if kind == "cw" else "cw"
        out = [T(p, (other,)), (p[1], p[0]), T(p, ("half",)), (-p[1], -p[0])]
    return [pair(*c) for c in out]


def set_plane(rnd, P):
    its = []
    pos = Pos(rnd)
    p, dx, dy = (-3, 4), 6, -7
    its.append(mcq("Translate %s %s. What are the coordinates of the image?" % (pair(*p), mv(dx, dy)),
                   pair(*T(p, ("t", dx, dy))), trans_cands(p, dx, dy), step_e(p, ("t", dx, dy)), rnd))
    a, b = (-5, 2), (3, -4)
    e = describe_e(a, b) + " The move crosses the y-axis, so the sizes add: 5 + 3 = 8."
    its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                   mv(8, -6), describe_cands(a, b), e, rnd))
    its.append(mcq("Which rule shows a translation 4 units left and 3 units up?", "(x %s 4, y + 3)" % MINUS,
                   ["(x + 4, y %s 3)" % MINUS, "(x %s 3, y + 4)" % MINUS, "(x + 4, y + 3)"],
                   "Left subtracts from x: x %s 4. Up adds to y: y + 3. So (x, y) → (x %s 4, y + 3)." % (MINUS, MINUS), rnd))
    for p, ax in [((-6, 5), "rx"), ((4, -2), "ry")]:
        r = T(p, (ax,))
        its.append(mcq("Reflect %s in the %s. What are the coordinates of the image?" % (pair(*p), axname(ax)),
                       pair(*r), [pair(*T(p, (other_axis(ax),))), pair(-p[0], -p[1]), pair(r[1], r[0])],
                       step_e(p, (ax,)), rnd))
    its.append(mcq("Reflect %s in the line x = 2. What are the coordinates of the image?" % pair(5, 3), pair(*T((5, 3), ("vx", 2))),
                   [pair(-5, 3), pair(-3, 3), pair(5, 1)],
                   step_e((5, 3), ("vx", 2)) + " (%s is the reflection in the y-axis, not in x = 2.)" % pair(-5, 3), rnd))
    assert T((5, 3), ("vx", 2)) == (-1, 3)
    assert T((-4, 6), ("hy", 1)) == (-4, -4)
    its.append(mcq("Reflect %s in the line y = 1. What are the coordinates of the image?" % pair(-4, 6), pair(-4, -4),
                   [pair(-4, -6), pair(-4, -5), pair(6, 6)],
                   step_e((-4, 6), ("hy", 1)) + " (%s is the reflection in the x-axis, not in y = 1.)" % pair(-4, -6), rnd))
    p = (-5, -3)
    r = T(p, ("ry",))
    wrong = T(p, ("rx",))
    svg, ans, where = pick_grid(p, r, [wrong, (5, 3), (-3, -5)], pos)
    its.append(mcq_fixed(fig(svg) + "Which point is the reflection of point P in the y-axis?", LETTERS, ans,
                         "P is at %s. %s That is point %s. Point %s is the reflection in the x-axis instead, and point %s changes both signs."
                         % (pair(*p), step_e(p, ("ry",)), ans, where[wrong], where[(5, 3)])))
    A = [(-5, 1), (-2, 1), (-2, 4)]
    B = runs(A, [("rx",)])
    assert not maps(A, B, ("ry",)) and not maps(A, B, ("half",)) and not maps(A, B, "translation")
    its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its reflection B")) +
                         "Triangle B is the reflection of triangle A. Which axis is the mirror line?", AXES, "the x-axis",
                         "Compare a vertex and its image: %s → %s. x stays the same and y changes sign, so the shape flipped up or down. "
                         "The mirror line is the x-axis." % (pair(*A[1]), pair(*B[1]))))
    for p, kind in [((5, 2), "cw"), ((-3, -4), "ccw"), ((-6, 1), "half")]:
        its.append(mcq("Rotate %s %s about the origin. What are the coordinates of the image?" % (pair(*p), TNAME[kind]),
                       pair(*T(p, (kind,))), rot_cands(p, kind), step_e(p, (kind,)), rnd))
    p = (2, 6)
    r = T(p, ("ccw",))
    its.append(mcq("Rotate %s 270° clockwise about the origin. What are the coordinates of the image?" % pair(*p), pair(*r),
                   [pair(*T(p, ("cw",))), pair(*T(p, ("half",))), pair(6, 2)],
                   "270° clockwise is 90° short of a full turn, so it ends in the same place as 90° counterclockwise. %s" % step_e(p, ("ccw",)), rnd))
    p = (4, 3)
    r = T(p, ("cw",))
    others = [T(p, ("ccw",)), (3, 4), T(p, ("half",))]
    svg, ans, where = pick_grid(p, r, others, pos)
    its.append(mcq_fixed(fig(svg) + "Point P is rotated 90° clockwise about the origin. Which point is the image?", LETTERS, ans,
                         "P is at %s. %s That is point %s. Point %s is a turn the wrong way, and point %s only swaps the numbers."
                         % (pair(*p), step_e(p, ("cw",)), ans, where[others[0]], where[others[1]])))
    A = [(1, 2), (5, 2), (1, 4)]
    B = runs(A, [("ccw",)])
    assert not any(maps(A, B, (k,)) for k in ("cw", "half"))
    its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its rotation B")) +
                         "Triangle A is rotated about the origin to give triangle B. Describe the rotation.", TURNS4, "90° counterclockwise",
                         "Follow one vertex. %s The shape turned a quarter turn counterclockwise about the origin."
                         % step_e(A[1], ("ccw",))))
    tri = [(1, 2), (4, 2), (4, 5)]
    img = runs(tri, [("half",)])
    its.append(mcq("A triangle has vertices %s. It is rotated 180° about the origin. What are the vertices of the image?" % plist(tri),
                   plist(img), [plist(runs(tri, [("rx",)])), plist(runs(tri, [("ry",)])), plist(runs(tri, [("cw",)]))],
                   "A 180° rotation changes both signs of every vertex: %s → %s." % (plist(tri), plist(img)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s rotates %s 90° counterclockwise about the origin and gets %s. What mistake did %s make?" % (n, pair(3, 1), pair(1, -3), he),
                   "%s turned it clockwise" % H,
                   ["%s only swapped the numbers" % H, "%s turned it 180°" % H, "No mistake. %s is right" % H],
                   "%s used the clockwise rule (y, %sx). Counterclockwise is the opposite way to clock hands. %s"
                   % (n, MINUS, step_e((3, 1), ("ccw",))), rnd))
    assert quad(*T((-5, -2), ("cw",))) == "Quadrant II"
    its.append(mcq_fixed("Point %s is rotated 90° clockwise about the origin. Which quadrant is the image in?" % pair(-5, -2), QUADS, "Quadrant II",
                         "%s is in Quadrant III. A quarter turn clockwise moves it to the next quadrant clockwise: Quadrant II. "
                         "Check: the image is %s." % (pair(-5, -2), pair(-2, 5))))
    its.append(mcq_fixed("A transformation follows the rule (x, y) → (%sx, y). What is it?" % MINUS, RULES, "a reflection in the y-axis",
                         "Only x changes sign, so each point flips left or right across the y-axis. Example: %s → %s." % (pair(3, 2), pair(-3, 2))))
    its.append(mcq_fixed("A transformation follows the rule (x, y) → (%sx, %sy). What is it?" % (MINUS, MINUS), RULES, "a rotation of 180°",
                         "Both signs change and the numbers stay in the same order. That is a half turn about the origin. Example: %s → %s. "
                         "(A reflection changes only one sign.)" % (pair(3, 2), pair(-3, -2))))
    assert len(its) == 20, len(its)
    return {"title": "Translations, reflections and rotations", "items": its}


# ------------------------------------------------------------ set 4: dilations
def dil_cands(p, k):
    """Adding the scale factor, multiplying by the inverse, multiplying only one coordinate."""
    k = Fraction(k)
    x, y = p
    r = T(p, ("d", k))
    if k < 1:
        out = [(x * k.denominator, y * k.denominator), (r[0], y), (x, r[1])]
    else:
        out = [(x + k, y + k), (r[0], y), (x, r[1])]
    return [pair(*(int(v) for v in c)) for c in out]


def kfixed():
    return [kname(HALF), "2", "3", "4"]


def set_dilate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, k in [((3, -2), 2), ((-2, 4), 3), ((8, -6), HALF), ((-9, 6), Fraction(1, 3)), ((-5, 1), 4)]:
        st = ("d", k)
        its.append(mcq("Dilate %s by a scale factor of %s with the centre at the origin. What are the coordinates of the image?"
                       % (pair(*p), kname(k)), pair(*T(p, st)), dil_cands(p, k), step_e(p, st), rnd))
    k = Fraction(3, 2)
    assert T((4, -2), ("d", k)) == (6, -3)
    its.append(mcq("Dilate %s by a scale factor of %s with the centre at the origin. What are the coordinates of the image?" % (pair(4, -2), kname(k)),
                   pair(6, -3), [pair(12, -6), pair(6, -2), pair(2, -1)],
                   step_e((4, -2), ("d", k)) + " (%s multiplies by 3 but forgets to divide by 2, and %s divides by 2 only.)"
                   % (pair(12, -6), pair(2, -1)), rnd))
    for p, k in [((2, -3), 2), ((-2, 1), 3)]:
        r = T(p, ("d", k))
        added, xonly, yonly = (p[0] + k, p[1] + k), (k * p[0], p[1]), (p[0], k * p[1])
        svg, ans, where = pick_grid(p, r, [added, xonly, yonly], pos)
        e = ("P is at %s. %s That is point %s. Point %s comes from adding %d instead of multiplying, and points %s and %s "
             "multiply only one coordinate." % (pair(*p), step_e(p, ("d", k)), ans, where[added], k, where[xonly], where[yonly]))
        its.append(mcq_fixed(fig(svg) + "Point P is dilated by a scale factor of %d with the centre at the origin. Which point is the image?" % k,
                             LETTERS, ans, e))
    for A, k, at in [([(1, 1), (3, 1), (3, 2)], 2, (3.55, 1.45)), ([(2, 4), (6, 4), (6, 6)], HALF, None)]:
        B = runs(A, [("d", k)])
        big = k == 2
        e = ("Compare a vertex and its image: %s → %s. Each coordinate is multiplied by %s. Check a side: the bottom side of A is "
             "%d units long and the bottom side of B is %d units long. %s"
             % (pair(*A[1]), pair(*B[1]), kname(k), A[1][0] - A[0][0], B[1][0] - B[0][0],
                "B is bigger, so the scale factor is more than 1." if big else "B is smaller, so the scale factor is less than 1."))
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
    third = Fraction(1, 3)
    assert T((9, -6), ("d", third)) == (3, -2)
    its.append(mcq("Point %s is dilated with the centre at the origin, and its image is %s. What is the scale factor?" % (pair(9, -6), pair(3, -2)),
                   kname(third), ["3", "6", "4"],
                   "Image ÷ original: 3 ÷ 9 = %s and %s2 ÷ (%s6) = %s. Both coordinates are divided by 3, so the scale factor is %s. "
                   "(3 takes the image back to the original, and 6 and 4 are the changes in x and y, not a scale factor.)"
                   % (kname(third), MINUS, MINUS, kname(third), kname(third)), rnd))
    its.append(mcq("A rectangle is 6 cm long and 4 cm wide. It is dilated by a scale factor of 1.5. What are the length and width of the image?",
                   "9 cm and 6 cm", ["7.5 cm and 5.5 cm", "9 cm and 4 cm", "12 cm and 8 cm"],
                   "Multiply every length by 1.5: 6 × 1.5 = 9 cm and 4 × 1.5 = 6 cm. Adding 1.5 to each side (7.5 cm and 5.5 cm) "
                   "does not keep the same shape.", rnd))
    its.append(mcq("A triangle has an angle of 72°. It is dilated by a scale factor of %s. What is the matching angle in the image?" % kname(HALF),
                   "72°", ["36°", "144°", "It cannot be found"],
                   "A dilation changes the side lengths, not the angles. Matching angles in similar shapes are equal, so the angle is still 72°.", rnd))
    its.append(mcq("A triangle has a perimeter of 24 cm. It is dilated by a scale factor of %s. What is the perimeter of the image?" % kname(third),
                   "8 cm", ["72 cm", "21 cm", "12 cm"],
                   "Every side is multiplied by %s, so the perimeter is too: 24 ÷ 3 = 8 cm. (72 cm multiplies by 3, and 21 cm subtracts 3.)"
                   % kname(third), rnd))
    its.append(mcq("A square with sides of 3 cm is dilated by a scale factor of 2. What is the area of the image?",
                   "36 cm²", ["18 cm²", "81 cm²", "24 cm²"],
                   "The image has sides of 3 × 2 = 6 cm, so its area is 6 × 6 = 36 cm². That is 4 times the old area of 9 cm², not 2 times (18 cm²). "
                   "(24 cm is the perimeter of the image, not its area.)", rnd))
    its.append(mcq("A triangle has sides 6 cm, 8 cm and 10 cm. Which triangle is similar to it?",
                   "9 cm, 12 cm, 15 cm", ["8 cm, 10 cm, 12 cm", "9 cm, 12 cm, 10 cm", "7 cm, 9 cm, 11 cm"],
                   "Similar shapes have every side multiplied by the same scale factor. 6 × 1.5 = 9, 8 × 1.5 = 12 and 10 × 1.5 = 15. "
                   "Adding the same amount (8, 10, 12) or scaling only some sides (9, 12, 10) does not give a similar triangle.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s dilates %s by a scale factor of %s with the centre at the origin and gets %s. What mistake did %s make?"
                   % (n, pair(-4, 6), kname(HALF), pair(-8, 12), he),
                   "%s multiplied by 2 instead of by %s" % (H, kname(HALF)),
                   ["%s added %s to each coordinate" % (H, kname(HALF)), "%s multiplied only x" % H, "No mistake. %s is right" % H],
                   "%s doubled both coordinates. A scale factor of %s halves them. %s" % (n, kname(HALF), step_e((-4, 6), ("d", HALF))), rnd))
    its.append(mcq_fixed("Which scale factor makes the image smaller than the original shape?",
                         [kname(third), "1", kname(Fraction(3, 2)), "3"], kname(third),
                         "A scale factor between 0 and 1 shrinks the shape: %s makes every side a third as long. "
                         "A scale factor of 1 keeps the same size, and %s or 3 enlarges it." % (kname(third), kname(Fraction(3, 2)))))
    end = (-6, 9)
    start = T(end, ("d", third))
    its.append(mcq("Point A is dilated by a scale factor of 3 with the centre at the origin. The image is %s. Where is point A?" % pair(*end),
                   pair(*start), [pair(-18, 27), pair(-3, 6), pair(-2, 9)],
                   "Undo the dilation: divide both coordinates by 3. %s ÷ 3 = %s and 9 ÷ 3 = 3, so A is %s. Check: %s"
                   % (num(-6), num(-2), pair(*start), step_e(start, ("d", 3))), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Dilations and scale factors", "items": its}


# ------------------------------------------------------------ set 5: combinations, predictions and word problems
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


def set_problems(rnd, P):
    its = []
    four = ["a translation", "a reflection in the y-axis", "a rotation of 180°", "a dilation"]
    for A, st in [([(-5, 1), (-2, 1), (-5, 4)], ("t", 6, -5)), ([(-5, 2), (-2, 2), (-2, 5)], ("ry",)),
                  ([(2, 2), (5, 2), (2, 5)], ("half",)), ([(1, 1), (2, 1), (1, 2)], ("d", 3))]:
        B = runs(A, [st])
        ch, ans = which_q(A, B, four)
        if st[0] == "t":
            e = ("Triangle B is the same size and faces the same way as triangle A: it only slid. That is a translation (%s)."
                 % mv(st[1], st[2]))
        elif st[0] == "d":
            e = ("Triangle B has the same shape as triangle A but is bigger, so it is a dilation. %s Translations, reflections "
                 "and rotations never change the size." % step_e(A[1], st))
        else:
            e = ("Follow one vertex. %s Check the other vertices: they all land on triangle B, so it is %s."
                 % (step_e(A[1], st), ans))
        at_a = (2.5, 1.5) if st[0] == "d" else None
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B", at_a=at_a)) +
                             "Which single transformation maps triangle A onto triangle B?", ch, ans, e))
    A = [(2, 1), (5, 1), (5, 3)]
    B = runs(A, [("ccw",)])
    ch, ans = which_q(A, B, ["a reflection in the x-axis", "a rotation of 90° clockwise", "a rotation of 90° counterclockwise", "a rotation of 180°"])
    its.append(mcq_fixed("Triangle PQR has vertices %s. Its image has vertices %s, in the same order. Which single transformation was used?"
                         % (plist(A), plist(B)), ch, ans,
                         "Compare each vertex with its image. %s The rule works for every vertex, so it is %s." % (step_e(A[0], ("ccw",)), ans)))
    steps = [("ccw",), ("t", 3, 0)]
    p = (4, 1)
    r = run(p, steps)
    assert r == (2, 4)
    its.append(mcq("Point %s is rotated 90° counterclockwise about the origin, then translated 3 units right. Where does it end up?" % pair(*p),
                   pair(*r), [pair(*run(p, [("cw",), ("t", 3, 0)])), pair(*T(p, ("ccw",))), pair(*run(p, [("t", 3, 0), ("ccw",)]))],
                   "Do the steps in order. " + steps_e(p, steps) +
                   " (Translating first gives %s: the order matters.)" % pair(*run(p, [("t", 3, 0), ("ccw",)])), rnd))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert run((4, -2), [("half",)]) == run((4, -2), [("rx",), ("ry",)]) == (-4, 2)
    its.append(mcq_fixed("A point moves from %s to %s. %s says it was a rotation of 180° about the origin. %s says it was a reflection in "
                         "the x-axis, then a reflection in the y-axis. Who is right?" % (pair(4, -2), pair(-4, 2), n1, n2),
                         ["Only %s" % n1, "Only %s" % n2, "Both of them", "Neither of them"], "Both of them",
                         "180° rotation: both signs change, %s → %s. Two reflections: %s → %s → %s. Both give the same image."
                         % (pair(4, -2), pair(-4, 2), pair(4, -2), pair(4, 2), pair(-4, 2))))
    a1 = run((2, 3), [("rx",), ("t", 0, 4)])
    a2 = run((2, 3), [("t", 0, 4), ("rx",)])
    assert a1 == (2, 1) and a2 == (2, -7)
    its.append(mcq("Point %s is reflected in the x-axis and translated 4 units up. Does the order of the two steps matter?" % pair(2, 3),
                   "Yes: %s or %s" % (pair(*a1), pair(*a2)),
                   ["No: both orders give %s" % pair(*a1), "No: both orders give %s" % pair(*a2), "Yes, but only the x-coordinate changes"],
                   "Reflect first: %s → %s → %s. Translate first: %s → %s → %s. The answers are different, so do the steps in the order given."
                   % (pair(2, 3), pair(2, -3), pair(*a1), pair(2, 3), pair(2, 7), pair(*a2)), rnd))
    its.append(mcq_fixed("A point in Quadrant II is reflected in the x-axis, then rotated 180° about the origin. Predict the quadrant of the final image.",
                         QUADS, "Quadrant I",
                         "Reflecting in the x-axis takes Quadrant II (left, up) to Quadrant III (left, down). A 180° rotation takes it to the "
                         "opposite quadrant: Quadrant I. Example: %s → %s → %s." % (pair(-3, 2), pair(-3, -2), pair(3, 2))))
    its.append(mcq_fixed("A triangle is in Quadrant IV. It is dilated by a scale factor of 2 with the centre at the origin. Predict the quadrant of the image.",
                         QUADS, "Quadrant IV",
                         "Multiplying by a positive scale factor keeps both signs, so the image stays in Quadrant IV, twice as far from the origin. "
                         "Example: %s → %s." % (pair(2, -1), pair(4, -2))))
    # word problems in Canadian contexts
    p, dx, dy = (-4, -3), 7, 5
    its.append(mcq("A drone video of a park in Winnipeg uses a grid with the origin at the fountain, east to the right and north up. The drone is at %s. "
                   "It flies %s east and %s north. Where is it now?" % (pair(*p), units(dx), units(dy)),
                   pair(*T(p, ("t", dx, dy))), trans_cands(p, dx, dy), step_e(p, ("t", dx, dy)), rnd))
    its.append(mcq("A ringette coach draws a drill on a grid with the origin at the centre of the rink. A player starts at %s. "
                   "The coach copies the drill to the other side of the rink by reflecting it in the x-axis. Where is the player’s image?" % pair(5, -2),
                   pair(5, 2), [pair(-5, -2), pair(-5, 2), pair(-2, 5)], step_e((5, -2), ("rx",)), rnd))
    its.append(mcq("A robotics club programs a robot arm that turns about the origin. The gripper is at %s. The arm turns 90° clockwise. "
                   "Where is the gripper now?" % pair(3, 4), pair(*T((3, 4), ("cw",))), rot_cands((3, 4), "cw"), step_e((3, 4), ("cw",)), rnd))
    its.append(mcq("A school yearbook photo is 5 cm wide and 7 cm tall. It is enlarged by a scale factor of 3 for a poster in the gym. "
                   "What size is the enlarged photo?", "15 cm by 21 cm", ["8 cm by 10 cm", "15 cm by 7 cm", "10 cm by 14 cm"],
                   "Multiply both lengths by 3: 5 × 3 = 15 cm and 7 × 3 = 21 cm. Adding 3 (8 cm by 10 cm) would stretch the photo out of shape.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a maple leaf design for a sticker. One tip is at %s. %s dilates the design by a scale factor of %s "
                   "with the centre at the origin. Where is that tip now?" % (n, pair(-8, 6), he.capitalize(), kname(HALF)),
                   pair(-4, 3), dil_cands((-8, 6), HALF), step_e((-8, 6), ("d", HALF)), rnd))
    its.append(mcq("The CN Tower is 553 m tall. A model of it is a dilation with a scale factor of %s. How tall is the model?" % kname(Fraction(1, 1000)),
                   "55.3 cm", ["5.53 cm", "553 cm", "55.3 m"],
                   "553 m ÷ 1000 = 0.553 m. Change to centimetres: 0.553 × 100 = 55.3 cm. (55.3 m divides by 10 only; 553 cm and 5.53 cm move the decimal point the wrong number of places.)", rnd))
    n, he, his = P.next()
    its.append(mcq_fixed("%s plans a snow sculpture on a grid. A corner on the small plan is at %s, and the same corner on the full-size plan is at %s. "
                         "The full-size plan is a dilation of the small one with the centre at the origin. What is the scale factor?"
                         % (n, pair(3, -2), pair(12, -8)), [kname(Fraction(1, 4)), "4", "6", "9"], "4",
                         "Image ÷ original: 12 ÷ 3 = 4 and %s8 ÷ (%s2) = 4. The scale factor is 4. (9 and 6 are the changes in x and y; "
                         "%s would shrink the plan.)" % (MINUS, MINUS, kname(Fraction(1, 4)))))
    n, he, his = P.next()
    end = (-3, 5)
    start = T(end, ("ccw",))
    assert T(start, ("cw",)) == end
    its.append(mcq("In a video game, %s’s character is rotated 90° clockwise about the origin and ends at %s. Where did it start?" % (n, pair(*end)),
                   pair(*start), [pair(*T(end, ("cw",))), pair(*T(end, ("half",))), pair(5, -3)],
                   "Undo the turn by turning the other way. %s Check: %s" % (step_e(end, ("ccw",)), step_e(start, ("cw",))), rnd))
    n, he, his = P.next()
    its.append(mcq("%s is designing floor tiles for a community centre in Ottawa. Each corner must have 2 regular octagons and one other regular tile. "
                   "Which tile fills the space?" % n, "a square",
                   ["an equilateral triangle", "a regular hexagon", "a regular pentagon"],
                   "2 × 135° = 270°, so 360° %s 270° = 90° is left. A square has 90° angles, so it fits exactly." % MINUS, rnd))
    n, he, his = P.next()
    a, b = (-1, 3), (-3, -1)
    assert run(a, [("t", -5, 2), ("t", 3, -6)]) == b
    its.append(mcq("In a coding app, %s moves a sprite from %s %s, then %s. Which single translation does the same?"
                   % (n, pair(*a), mv(-5, 2), mv(3, -6)),
                   mv(-2, -4), [mv(-8, -8), mv(2, 4), mv(-2, -8)],
                   "Add the moves. x: %s5 + 3 = %s2, so 2 units left. y: 2 + (%s6) = %s4, so 4 units down. Check: %s → %s."
                   % (MINUS, MINUS, MINUS, MINUS, pair(*a), pair(*b)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Combinations, predictions and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    fits = vertex_svg([6, 6, 6], None, "three regular hexagons around a point")
    gap = vertex_svg([5, 5, 5], "?", "three regular pentagons around a point with a gap")
    octs = patch_svg("octsq", label="floor tile pattern of octagons and squares")
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
        "<h2>Tessellations</h2>"
        "<p>A shape <b>tessellates</b> when copies of it cover a surface with <b>no gaps and no overlaps</b>. "
        "Where corners meet, the angles must add up to <b>360°</b>. Each angle of a regular polygon with n sides is (n − 2) × 180° ÷ n.</p>"
        "<figure class='sn-fig'>" + fits +
        "<figcaption>3 regular hexagons: 3 × 120° = 360°. They fit exactly, so hexagons tessellate, like a honeycomb.</figcaption></figure>"
        "<figure class='sn-fig'>" + gap +
        "<figcaption>3 regular pentagons: 3 × 108° = 324°. There is a 36° gap, so regular pentagons do not tessellate.</figcaption></figure>" +
        table(["Regular polygon", "Each angle", "Around a point", "Tessellates on its own?"], [
            ["equilateral triangle", "60°", "6 × 60° = 360°", "yes"],
            ["square", "90°", "4 × 90° = 360°", "yes"],
            ["regular hexagon", "120°", "3 × 120° = 360°", "yes"],
            ["regular pentagon", "108°", "3 × 108° = 324° (gap)", "no"],
            ["regular octagon", "135°", "2 × 135° = 270° (gap)", "no"],
        ]) +
        "<p>Any triangle and any quadrilateral tessellates. Two shapes can also tessellate together: 135° + 135° + 90° = 360°.</p>"
        "<figure class='sn-fig'>" + octs +
        "<figcaption>Regular octagons and squares: 2 octagons and 1 square meet at every corner.</figcaption></figure>"
        "<p>Every tessellation is built with transformations. Tiles that face the same way are <b>translations</b> of each other. "
        "Mirror-image tiles come from <b>reflections</b>, and turned tiles from <b>rotations</b>.</p>" +
        ex("Example", "Two regular hexagons meet at a point. How many equilateral triangles fill the gap?",
           "2 × 120° = 240°. 360° − 240° = 120°. 120° ÷ 60° = 2.", "2 triangles") +
        "<h2>Transformations on the Cartesian plane</h2>"
        "<p>Move every vertex with the same rule, then join the new vertices. Translations, reflections and rotations keep the size, "
        "so the image is <b>congruent</b>. A dilation changes the size, so the image is <b>similar</b>.</p>" +
        table(["Transformation", "Rule for (x, y)"], [
            ["Translation a right and b up", "(x + a, y + b)"],
            ["Reflection in the x-axis", "(x, −y)"],
            ["Reflection in the y-axis", "(−x, y)"],
            ["Rotation of 90° clockwise about the origin", "(y, −x)"],
            ["Rotation of 90° counterclockwise about the origin", "(−y, x)"],
            ["Rotation of 180° about the origin", "(−x, −y)"],
            ["Dilation by scale factor k, centre at the origin", "(kx, ky)"],
        ]) +
        ex("Example", "Reflect (5, 3) in the line x = 2.",
           "(5, 3) is 3 units right of the line, so the image is 3 units left of it: x = 2 − 3 = −1. y stays 3.", "(−1, 3)") +
        "<p>For a 90° turn, swap the two numbers, then change one sign. Clockwise (the way clock hands move): change the sign of the "
        "<b>second</b> number. Counterclockwise: change the sign of the <b>first</b> number.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A turns 90° clockwise about the origin. The vertex (4, 2) goes to (2, −4).</figcaption></figure>" +
        ex("Example", "Rotate (2, 5) 90° counterclockwise about the origin.",
           "Swap: (5, 2). Change the sign of the first number: (−5, 2). Check: Quadrant I turns counterclockwise into Quadrant II.", "(−5, 2)") +
        "<h2>Dilations</h2>"
        "<p>A <b>dilation</b> with the centre at the origin <b>multiplies</b> both coordinates by the <b>scale factor</b>. "
        "A scale factor greater than 1 enlarges the shape; a scale factor between 0 and 1 shrinks it. The angles stay the same.</p>"
        "<figure class='sn-fig'>" + dil +
        "<figcaption>Triangle A is dilated by a scale factor of 2. The vertex (3, 1) goes to (6, 2), twice as far from the origin.</figcaption></figure>" +
        ex("Example", "Dilate (−9, 6) by a scale factor of " + kname(Fraction(1, 3)) + ".", "Divide both coordinates by 3: −9 ÷ 3 = −3 and 6 ÷ 3 = 2.", "(−3, 2)") +
        "<h2>Combining and predicting</h2>"
        "<p>Do the steps in order and follow one vertex. The order can change the answer. Predict first, then check: "
        "a reflection in the x-axis moves a point up or down to the other side, a 180° rotation sends it to the opposite quadrant, "
        "and a dilation keeps it in the same quadrant.</p>" +
        ex("Example", "Reflect (2, 3) in the x-axis, then translate it 4 units up.", "(2, 3) → (2, −3) → (2, 1). Doing the steps the other way gives (2, −7).", "(2, 1)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking all regular polygons tessellate", "Only triangles, squares and hexagons: their angles divide exactly into 360°"],
            ["Rotating the wrong way", "Clockwise goes the way clock hands move: from the top to the right"],
            ["Only swapping the numbers in a 90° turn: (3, 1) → (1, 3)", "Swap and change one sign: (1, −3) clockwise, (−1, 3) counterclockwise"],
            ["Reflecting in the wrong axis", "In the x-axis, y changes sign. In the y-axis, x changes sign"],
            ["Adding the scale factor: (4, −5) by 3 → (7, −2)", "Multiply both coordinates: (12, −15)"],
            ["Doing the steps of a combination in a different order", "Follow the order given, one step at a time"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about transformations in the Ontario math curriculum?",
     "a": "In Grade 8 Spatial Sense, students perform translations, reflections, rotations and dilations on the Cartesian plane and predict the results. They also study which shapes tessellate and the transformations used in tessellations."},
    {"q": "Why does a regular pentagon not tessellate?",
     "a": "Each angle is 108°. Three pentagons make 324°, leaving a 36° gap, and four make 432°, which overlaps, so they cannot fill the 360° around a point."},
    {"q": "How do you rotate a point 90° about the origin?",
     "a": "Swap the two numbers, then change one sign. For 90° clockwise, (x, y) becomes (y, −x); for 90° counterclockwise, it becomes (−y, x)."},
    {"q": "Is there a provincial math test in Grade 8 in Ontario?",
     "a": "No. EQAO math assessments are written in Grades 3 and 6, and the next one is in Grade 9. These worksheets help Grade 8 students practise for class tests and get ready for high school."},
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
    rnd = random.Random(48814)
    P = People(rnd)
    sets = [set_tessellate(rnd, P), set_patterns(rnd, P), set_plane(rnd, P), set_dilate(rnd, P), set_problems(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "/", x) for x in it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "tessellations-and-transformations", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Tessellations and Transformations: Translations, Reflections, Rotations and Dilations",
        "seo_title": "Grade 8 Math: Tessellations and Transformations Worksheets (Free, Ontario Curriculum, Answer Key)",
        "short_title": "Tessellations and transformations",
        "domain": "Spatial Sense",
        "standard_code": "Grade 8: E1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe and perform translations, reflections, rotations, and dilations on a Cartesian plane, and predict the results of these transformations",
        "meta_desc": "Free Grade 8 math worksheets on tessellations and transformations for the Ontario curriculum: which shapes tessellate (angles at a point add to 360°), transformations in tile patterns, translations, reflections, rotations and dilations on the Cartesian plane, and predicting the results. 100 questions with an answer key.",
        "key_big": "A shape tessellates when the angles meeting at each point add up to 360°. On the plane, every vertex moves by the same rule.",
        "key_sub": "Equilateral triangles (6 × 60°), squares (4 × 90°) and regular hexagons (3 × 120°) tessellate; regular pentagons (108°) do not. Rotation about the origin: 90° clockwise (x, y) → (y, −x), 90° counterclockwise (−y, x), 180° (−x, −y). Dilation by k: (kx, ky).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (grids and patterns) so their numbers and tiles stay readable."""
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
        mark_large(u, "(coordinate grid|four shapes|four patterns|pattern|brick wall|honeycomb|floor tile)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
