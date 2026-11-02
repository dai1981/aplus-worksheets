# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Combinations of transformations
(BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g7_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

Canadian English (counterclockwise, centre, colour). Whole-number coordinates; every grid runs from −6 to 6
(lesson grids −5 to 5), is square and exact, and is drawn from the data. Negative numbers use the real minus sign.
Every image is computed by the transformation functions below; every "which transformation" answer is checked:
the right one maps the shape onto the image and no wrong choice does.
Wrong answers come from real mistakes: translating the wrong way, changing the wrong coordinate, swapping the two
amounts, subtracting sizes when a move crosses an axis, counting grid lines, reflecting in the wrong axis, changing
both signs, rotating the wrong way, swapping the numbers in a 90° turn without changing a sign, mixing up 90° and
180°, and doing the steps of a combination in the wrong order.
Grade 7 students add and subtract integers, so translations are explained with integer sums (−2 + 5 = 3).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2f6fb5"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
QUADS = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]
AXES = ["the x-axis", "the y-axis", "both axes", "neither axis"]
TURNS4 = ["90° clockwise", "90° counterclockwise", "180°", "360°"]


# ------------------------------------------------------------ numbers and pairs
def num(v):
    return (MINUS + str(-v)) if v < 0 else str(v)


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
    return {"rx": "a reflection in the x-axis", "ry": "a reflection in the y-axis",
            "cw": "a rotation of 90° clockwise", "ccw": "a rotation of 90° counterclockwise",
            "half": "a rotation of 180°"}[k]


def sverb(st):
    """Verb phrase for one step: 'translate it 3 units left', 'reflect it in the x-axis'."""
    k = st[0]
    if k == "t":
        return "translate %s" % mv(st[1], st[2])
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


def two_shapes(a, b, label):
    """Grid with shape A (red) and shape B (green)."""
    G = Grid(6)
    G.poly(a, RED, "A")
    G.poly(b, GREEN, "B")
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
        out.append(mv(dy and abs(dy) * (1 if dx > 0 else -1), abs(dx) * (1 if dy > 0 else -1)))
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
    for p, dx, dy in [((3, -2), -6, 0), ((-1, 4), 0, -7), ((-5, -3), 8, 0),
                      ((-3, 2), 5, -4), ((4, -1), -6, 3), ((-2, -5), 7, 4), ((5, 3), -3, -7)]:
        r = T(p, ("t", dx, dy))
        its.append(mcq("Translate %s %s. What are the coordinates of the image?" % (pair(*p), mv(dx, dy)),
                       pair(*r), trans_cands(p, dx, dy), step_e(p, ("t", dx, dy)), rnd))
    # grid: which point is the image of P?
    for p, dx, dy in [((-5, 2), 6, -3), ((4, -2), -6, 3), ((3, 4), -5, -2)]:
        r = T(p, ("t", dx, dy))
        swapped = (p[0] + (abs(dy) if dx > 0 else -abs(dy)), p[1] + (abs(dx) if dy > 0 else -abs(dx)))
        wrongway = (p[0] + dx, p[1] - dy)
        lines = (p[0] + dx + (1 if dx > 0 else -1), p[1] + dy + (1 if dy > 0 else -1))
        svg, ans, where = pick_grid(p, r, [swapped, wrongway, lines], pos)
        e = ("P is at %s. %s That is point %s. Point %s moves the wrong way up or down, and point %s comes from counting grid lines "
             "instead of spaces." % (pair(*p), step_e(p, ("t", dx, dy)), ans, where[wrongway], where[lines]))
        its.append(mcq_fixed(fig(svg) + "Point P is translated %s. Which point is its image?" % mv(dx, dy),
                             ["A", "B", "C", "D"], ans, e))
    # describe the translation from the coordinates
    for a, b in [((-3, 2), (4, -1)), ((5, -4), (-1, 2)), ((-2, -6), (-6, 1))]:
        dx, dy = b[0] - a[0], b[1] - a[1]
        e = describe_e(a, b)
        if a[0] * b[0] < 0:
            e += " The move crosses the y-axis, so the sizes add: %d + %d = %d." % (abs(a[0]), abs(b[0]), abs(dx))
        its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(a, b), e, rnd))
    # grid with two triangles
    A = [(-5, 2), (-2, 2), (-5, 4)]
    B = runs(A, [("t", 6, -5)])
    its.append(mcq(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B")) +
                   "Triangle B is a translation of triangle A. Describe the translation.",
                   mv(6, -5), [mv(-6, 5), mv(5, -6), mv(7, -6)],
                   "Pick one vertex and its image. The corner %s moves to %s. x: 1 %s (%s5) = 6, so 6 units right. "
                   "y: %s3 %s 2 = %s5, so 5 units down. Every vertex moves the same way." %
                   (pair(-5, 2), pair(1, -3), MINUS, MINUS, MINUS, MINUS, MINUS), rnd))
    its.append(mcq("A translation is written as (x, y) → (x %s 4, y + 2). Describe it in words." % MINUS, mv(-4, 2),
                   [mv(4, 2), mv(-2, 4), mv(-4, -2)],
                   "x %s 4 makes x smaller by 4, so the point moves 4 units left. y + 2 makes y bigger by 2, so it moves 2 units up." % MINUS, rnd))
    its.append(mcq("Which rule shows a translation 5 units right and 3 units down?", "(x + 5, y %s 3)" % MINUS,
                   ["(x %s 5, y + 3)" % MINUS, "(x + 3, y %s 5)" % MINUS, "(x + 5, y + 3)"],
                   "Right adds to x: x + 5. Down subtracts from y: y %s 3. So (x, y) → (x + 5, y %s 3)." % (MINUS, MINUS), rnd))
    tri = [(-4, 1), (-1, 1), (-1, 5)]
    img = runs(tri, [("t", 3, -6)])
    its.append(mcq("Triangle ABC has vertices A %s, B %s and C %s. It is translated %s. What are the vertices of the image?"
                   % (pair(*tri[0]), pair(*tri[1]), pair(*tri[2]), mv(3, -6)),
                   plist(img), [plist(runs(tri, [("t", -3, 6)])), plist(runs(tri, [("t", 6, -3)])), plist(runs(tri, [("t", 3, 6)]))],
                   "Add 3 to every x and subtract 6 from every y. A: %s. B: %s. C: %s." % (
                       pair(*img[0]), pair(*img[1]), pair(*img[2])), rnd))
    its.append(mcq("After a translation %s, the image of point A is %s. Where was point A before the move?" % (mv(-4, 5), pair(-1, 2)),
                   pair(3, -3), [pair(-5, 7), pair(3, 7), pair(-5, -3)],
                   "Undo the move: go 4 units right and 5 units down. x: %s. y: %s. A was at %s. Check: 4 left and 5 up from %s is %s."
                   % (add_e(-1, 4), add_e(2, -5), pair(3, -3), pair(3, -3), pair(-1, 2)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s translates %s 3 units down and gets %s. What mistake did %s make?" % (n, pair(-2, 4), pair(-5, 4), he),
                   "%s changed x instead of y" % H,
                   ["%s moved up instead of down" % H, "%s counted the grid lines" % H, "No mistake. %s is right" % H],
                   "Down changes only y: %s. The image is %s. %s subtracted 3 from x, which moves the point left." % (
                       add_e(4, -3), pair(-2, 1), n), rnd))
    its.append(mcq("A point moves from %s to %s. How far did it move?" % (pair(-6, -2), pair(1, -2)), "7 units right",
                   ["5 units right", "8 units right", "7 units left"],
                   "Only x changes. 1 %s (%s6) = 1 + 6 = 7, and it is positive, so the point moved 7 units right. "
                   "(5 comes from 6 %s 1: the move crosses the y-axis, so the sizes add.)" % (MINUS, MINUS, MINUS), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations: perform and describe", "items": its}


# ------------------------------------------------------------ set 2: reflections in the axes
def other_axis(ax):
    return "ry" if ax == "rx" else "rx"


def axname(ax):
    return "x-axis" if ax == "rx" else "y-axis"


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, ax in [((5, -3), "ry"), ((-2, 6), "rx"), ((4, 1), "rx"), ((-6, -4), "ry"), ((-1, -5), "rx"), ((2, 3), "ry")]:
        r = T(p, (ax,))
        its.append(mcq("Reflect %s in the %s. What are the coordinates of the image?" % (pair(*p), axname(ax)),
                       pair(*r), [pair(*T(p, (other_axis(ax),))), pair(-p[0], -p[1]), pair(r[1], r[0])],
                       step_e(p, (ax,)), rnd))
    its.append(mcq("Reflect %s in the y-axis. What are the coordinates of the image?" % pair(0, -5), pair(0, -5),
                   [pair(0, 5), pair(-5, 0), pair(5, 0)], step_e((0, -5), ("ry",)), rnd))
    its.append(mcq("Reflect %s in the y-axis. What are the coordinates of the image?" % pair(-3, 0), pair(3, 0),
                   [pair(-3, 0), pair(0, 3), pair(0, -3)],
                   "%s is on the x-axis, 3 units left of the y-axis. Reflect in the y-axis: x changes sign, %s → %s. "
                   "The image is 3 units right: %s." % (pair(-3, 0), num(-3), "3", pair(3, 0)), rnd))
    for p, ax, extra in [((-3, 4), "rx", (-3, 0)), ((5, -2), "ry", (-2, -5)), ((-5, -2), "ry", (-2, -5))]:
        r = T(p, (ax,))
        wrong = T(p, (other_axis(ax),))
        svg, ans, where = pick_grid(p, r, [wrong, (-p[0], -p[1]), extra], pos)
        e = "P is at %s. %s That is point %s. Point %s is the reflection in the %s instead." % (
            pair(*p), step_e(p, (ax,)), ans, where[wrong], axname(other_axis(ax)))
        its.append(mcq_fixed(fig(svg) + "Which point is the reflection of point P in the %s?" % axname(ax),
                             ["A", "B", "C", "D"], ans, e))
    for A, ax in [([(-5, 2), (-2, 2), (-2, 5)], "rx"), ([(-5, -1), (-2, -1), (-5, -4)], "ry")]:
        B = runs(A, [(ax,)])
        assert not maps(A, B, (other_axis(ax),)) and not maps(A, B, ("half",)) and not maps(A, B, "translation")
        k = 0 if ax == "rx" else 1
        e = ("Compare a vertex and its image: %s → %s. %s, so the shape flipped %s. The mirror line is the %s."
             % (pair(*A[k]), pair(*B[k]),
                "x stays the same and y changes sign" if ax == "rx" else "y stays the same and x changes sign",
                "up or down" if ax == "rx" else "left or right", axname(ax)))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its reflection B")) +
                             "Triangle B is the reflection of triangle A. Which axis is the mirror line?", AXES, "the " + axname(ax), e))
    for tri, ax in [([(1, 2), (4, 2), (4, 5)], "rx"), ([(-5, -1), (-2, -1), (-2, -3)], "ry")]:
        img = runs(tri, [(ax,)])
        sign = "y" if ax == "rx" else "x"
        its.append(mcq("A triangle has vertices %s. It is reflected in the %s. What are the vertices of the image?" % (plist(tri), axname(ax)),
                       plist(img), [plist(runs(tri, [(other_axis(ax),)])), plist(runs(tri, [("half",)])),
                                    plist([(q[1], q[0]) for q in img])],
                       "Reflect each vertex in the %s: keep the other coordinate and change the sign of %s. %s → %s."
                       % (axname(ax), sign, plist(tri), plist(img)), rnd))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(-5, 2), pair(5, 2)), AXES,
                         "the y-axis", "y stays 2 and x changes sign (%s → 5), so the points flip left and right across the y-axis." % num(-5)))
    its.append(mcq("When you reflect a point in the y-axis, what changes?", "the sign of the x-coordinate",
                   ["the sign of the y-coordinate", "the signs of both coordinates", "the order of the numbers"],
                   "The y-axis is a mirror standing up. The point flips left or right, so only x changes sign. Example: %s → %s."
                   % (pair(3, 5), pair(-3, 5)), rnd))
    its.append(mcq_fixed("Point %s is reflected in the x-axis. Which quadrant is the image in?" % pair(-3, -5), QUADS, "Quadrant II",
                         "The image is %s: x stays negative and y becomes positive. Left and up is Quadrant II." % pair(-3, 5)))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s in the y-axis and gets %s. What mistake did %s make?" % (n, pair(4, -6), pair(4, 6), he),
                   "%s reflected in the x-axis" % H,
                   ["%s swapped x and y" % H, "%s changed both signs" % H, "No mistake. %s is right" % H],
                   "%s changed the sign of y. That is a reflection in the x-axis. In the y-axis, x changes sign: %s." % (H, pair(-4, -6)), rnd))
    its.append(mcq("Point Q is the reflection of point P in the x-axis. Q is at %s. Where is P?" % pair(-4, -1), pair(-4, 1),
                   [pair(4, -1), pair(4, 1), pair(-1, -4)],
                   "Reflecting in the x-axis changes the sign of y, and reflecting back does the same. %s → %s." % (pair(-4, -1), pair(-4, 1)), rnd))
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
    for p, kind in [((2, 5), "cw"), ((-3, 1), "cw"), ((-4, -6), "cw"),
                    ((5, -2), "ccw"), ((1, 3), "ccw"), ((-6, 4), "ccw"),
                    ((3, -4), "half"), ((-5, -1), "half")]:
        r = T(p, (kind,))
        its.append(mcq("Rotate %s %s about the origin. What are the coordinates of the image?" % (pair(*p), TNAME[kind]),
                       pair(*r), rot_cands(p, kind), step_e(p, (kind,)), rnd))
    for p, kind in [((5, 2), "cw"), ((-2, 4), "ccw"), ((3, -5), "half")]:
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
    for A, kind in [([(1, 2), (4, 2), (1, 4)], "cw"), ([(2, -1), (5, -1), (5, -3)], "ccw")]:
        B = runs(A, [(kind,)])
        assert not any(maps(A, B, (k,)) for k in ("cw", "ccw", "half") if k != kind)
        e = ("Follow one vertex: %s → %s. %s The shape turned a quarter turn %s about the origin."
             % (pair(*A[1]), pair(*B[1]), step_e(A[1], (kind,)), "clockwise" if kind == "cw" else "counterclockwise"))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and its rotation B")) +
                             "Triangle A is rotated about the origin to give triangle B. Describe the rotation.", TURNS4, TNAME[kind], e))
    its.append(mcq_fixed("Point %s is rotated about the origin and lands on %s. Describe the rotation." % (pair(4, -1), pair(1, 4)),
                         TURNS4, "90° counterclockwise",
                         "Try the rules. 90° counterclockwise: (x, y) → (%sy, x), so %s → %s. That matches. "
                         "(90° clockwise would give %s.)" % (MINUS, pair(4, -1), pair(1, 4), pair(-1, -4))))
    its.append(mcq_fixed("Point %s is rotated about the origin and lands on %s. Describe the rotation." % (pair(-3, -2), pair(3, 2)),
                         TURNS4, "180°",
                         "Both signs changed and the numbers stayed in the same order. That is a half turn: 180°."))
    its.append(mcq_fixed("Point %s is rotated 90° counterclockwise about the origin. Which quadrant is the image in?" % pair(5, -3),
                         QUADS, "Quadrant I",
                         "%s is in Quadrant IV. A quarter turn counterclockwise moves it to the next quadrant counterclockwise: "
                         "Quadrant I. Check: the image is %s." % (pair(5, -3), pair(3, 5))))
    its.append(mcq("Point %s is rotated 270° clockwise about the origin. Where does it land?" % pair(-2, 6), pair(-6, -2),
                   [pair(6, 2), pair(2, -6), pair(6, -2)],
                   "270° clockwise is three quarter turns clockwise. That ends in the same place as one quarter turn counterclockwise "
                   "(360° %s 270° = 90°). %s" % (MINUS, step_e((-2, 6), ("ccw",))), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s rotates %s 90° counterclockwise about the origin and gets %s. What mistake did %s make?" % (n, pair(3, 1), pair(1, 3), he),
                   "%s swapped the numbers but changed no sign" % H,
                   ["%s turned it clockwise" % H, "%s turned it 180°" % H, "No mistake. %s is right" % H],
                   "A 90° turn swaps the numbers and changes one sign. %s %s is still in Quadrant I, so it cannot be a quarter turn."
                   % (step_e((3, 1), ("ccw",)), pair(1, 3)), rnd))
    tri = [(1, 1), (4, 1), (4, 3)]
    img = runs(tri, [("half",)])
    its.append(mcq("A triangle has vertices %s. It is rotated 180° about the origin. What are the vertices of the image?" % plist(tri),
                   plist(img), [plist(runs(tri, [("rx",)])), plist(runs(tri, [("ry",)])), plist(runs(tri, [("cw",)]))],
                   "A 180° rotation changes both signs of every vertex: %s → %s." % (plist(tri), plist(img)), rnd))
    its.append(mcq_fixed("Which rotation about the origin always gives the same image as a rotation of 90° clockwise?",
                         ["90° counterclockwise", "180°", "270° clockwise", "270° counterclockwise"], "270° counterclockwise",
                         "A full turn is 360°. Going 270° counterclockwise leaves 360° %s 270° = 90° to go, so you end where a "
                         "90° clockwise turn ends." % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Rotations of 90° and 180° about the origin", "items": its}


# ------------------------------------------------------------ set 4: combinations
def combo_cands(p, steps):
    """Wrong order, wrong axis or wrong turn in the second step, only the first step, the translation the wrong way."""
    out = [run(p, list(reversed(steps)))]
    fixed = []
    for st in steps:
        if st[0] in ("rx", "ry"):
            fixed.append((other_axis(st[0]),))
        elif st[0] in ("cw", "ccw"):
            fixed.append(("ccw" if st[0] == "cw" else "cw",))
        else:
            fixed.append(st)
    out.append(run(p, fixed))
    out.append(run(p, steps[:1]))
    out.append(run(p, [("t", -st[1], -st[2]) if st[0] == "t" else st for st in steps]))
    out.append(run(p, [("half",) if st[0] in ("rx", "ry") else st for st in steps]))
    out.append(run(p, [("rx",) if st[0] == "half" else st for st in steps]))     # changed only one sign in a half turn
    out.append(run(p, [("ry",) if st[0] == "half" else st for st in steps]))
    return [pair(*c) for c in out]


def combo_text(steps):
    return ", then ".join(sverb(st) for st in steps)


def set_combine(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, steps in [((-2, 3), [("t", 0, -5), ("rx",)]), ((4, -1), [("t", -6, 0), ("ry",)]),
                     ((1, 2), [("t", 3, -4), ("rx",)]), ((-5, -3), [("t", 2, 6), ("ry",)]),
                     ((3, 4), [("t", -5, -1), ("ry",)]),
                     ((2, -4), [("rx",), ("t", -5, 2)]), ((-3, 1), [("ry",), ("t", -4, -3)]),
                     ((-4, 1), [("t", 3, 2), ("cw",)]), ((2, -5), [("t", -1, 3), ("half",)]),
                     ((3, 2), [("ccw",), ("t", 4, -1)])]:
        r = run(p, steps)
        assert r != run(p, list(reversed(steps))), (p, steps)       # the order matters in every one
        e = "Do the steps in order. " + steps_e(p, steps)
        its.append(mcq("Point %s: %s. Where is the final image?" % (pair(*p), combo_text(steps)),
                       pair(*r), combo_cands(p, steps), e, rnd))
    for p, steps in [((-4, 2), [("t", 0, -5), ("ry",)]), ((1, 3), [("t", 3, 0), ("rx",)])]:
        r = run(p, steps)
        wrong_order = run(p, list(reversed(steps)))
        wrong_axis = run(p, [steps[0], (other_axis(steps[1][0]),)])
        only = run(p, steps[:1])
        if wrong_order == r:
            wrong_order = run(p, [steps[0], ("half",)])
        svg, ans, where = pick_grid(p, r, [wrong_order, wrong_axis, only], pos)
        e = "%s That is point %s. Point %s is the reflection in the wrong axis, and point %s is only the translation." % (
            steps_e(p, steps), ans, where[wrong_axis], where[only])
        its.append(mcq_fixed(fig(svg) + "Point P is %s, then reflected in the %s. Which point is the final image?"
                             % ("translated " + mv(steps[0][1], steps[0][2]), axname(steps[1][0])),
                             ["A", "B", "C", "D"], ans, e))
    its.append(mcq("Reflect %s in the y-axis, then reflect the image in the x-axis. Where does it land?" % pair(4, -3), pair(-4, 3),
                   [pair(-4, -3), pair(4, 3), pair(3, -4)],
                   steps_e((4, -3), [("ry",), ("rx",)]) + " Both signs changed.", rnd))
    its.append(mcq_fixed("A reflection in the x-axis followed by a reflection in the y-axis gives the same result as which single transformation?",
                         ["a translation", "a rotation of 90° clockwise", "a rotation of 180°", "a reflection in the x-axis"],
                         "a rotation of 180°",
                         "The first reflection changes the sign of y and the second changes the sign of x. Both signs change, "
                         "and that is exactly what a 180° rotation about the origin does. Example: %s → %s → %s."
                         % (pair(2, 5), pair(2, -5), pair(-2, -5))))
    tri = [(-4, 1), (-1, 1), (-1, 3)]
    steps = [("t", 2, -4), ("ry",)]
    img = runs(tri, steps)
    assert img != runs(tri, list(reversed(steps)))
    its.append(mcq("A triangle has vertices %s. It is translated %s, then reflected in the y-axis. What are the vertices of the final image?"
                   % (plist(tri), mv(2, -4)),
                   plist(img), [plist(runs(tri, list(reversed(steps)))), plist(runs(tri, [steps[0], ("rx",)])), plist(runs(tri, steps[:1]))],
                   "Translate first: %s. Then reflect in the y-axis (change the sign of x): %s." % (plist(runs(tri, steps[:1])), plist(img)), rnd))
    tri = [(2, 1), (5, 1), (2, 3)]
    steps = [("half",), ("t", 0, 3)]
    img = runs(tri, steps)
    assert img != runs(tri, list(reversed(steps)))
    its.append(mcq("A triangle has vertices %s. It is rotated 180° about the origin, then translated 3 units up. "
                   "What are the vertices of the final image?" % plist(tri),
                   plist(img), [plist(runs(tri, list(reversed(steps)))), plist(runs(tri, [("rx",), steps[1]])), plist(runs(tri, steps[:1]))],
                   "Rotate first (change both signs): %s. Then add 3 to every y: %s." % (plist(runs(tri, steps[:1])), plist(img)), rnd))
    p, steps = (-3, -5), [("t", 0, 2), ("rx",)]
    n, he, his = P.next()
    H = he.capitalize()
    wrong = run(p, list(reversed(steps)))
    its.append(mcq("%s must translate %s 2 units up, then reflect it in the x-axis. %s gets %s. What mistake did %s make?"
                   % (n, pair(*p), H, pair(*wrong), he),
                   "%s reflected first, then translated" % H,
                   ["%s reflected in the y-axis" % H, "%s translated down instead of up" % H, "No mistake. %s is right" % H],
                   "Right order: %s %s did the steps the other way round: %s → %s → %s. The order of the steps matters."
                   % (steps_e(p, steps), n, pair(*p), pair(*T(p, ("rx",))), pair(*wrong)), rnd))
    end = (-1, 4)
    start = run(end, [("ry",), ("t", -3, 0)])
    assert run(start, [("t", 3, 0), ("ry",)]) == end
    its.append(mcq("A point is translated 3 units right, then reflected in the y-axis. The final image is %s. Where did the point start?"
                   % pair(*end), pair(*start),
                   [pair(*run(end, [("t", -3, 0), ("ry",)])), pair(*run(end, [("t", -3, 0)])), pair(*run(end, [("rx",), ("t", -3, 0)]))],
                   "Work backwards and undo the last step first. Undo the reflection: %s → %s. Undo the translation (go 3 units left): "
                   "%s → %s. Check: %s" % (pair(*end), pair(*T(end, ("ry",))), pair(*T(end, ("ry",))), pair(*start),
                                            steps_e(start, [("t", 3, 0), ("ry",)])), rnd))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    p = (1, 2)
    s1, s2 = [("t", 0, 3), ("rx",)], [("rx",), ("t", 0, 3)]
    r1, r2 = run(p, s1), run(p, s2)
    assert r1 == (1, -5) and r2 == (1, 1)
    its.append(mcq("%s translates %s 3 units up, then reflects it in the x-axis. %s reflects %s in the x-axis first, then translates it "
                   "3 units up. What do they get?" % (n1, pair(*p), n2, pair(*p)),
                   "%s: %s, %s: %s" % (n1, pair(*r1), n2, pair(*r2)),
                   ["Both get %s" % pair(*r1), "Both get %s" % pair(*r2), "%s: %s, %s: %s" % (n1, pair(*r2), n2, pair(*r1))],
                   "%s: %s %s: %s The order of the steps changes the answer." % (n1, steps_e(p, s1), n2, steps_e(p, s2)), rnd))
    its.append(mcq_fixed("Point %s is translated 6 units right, then reflected in the x-axis. Which quadrant is the final image in?" % pair(-4, 2),
                         QUADS, "Quadrant IV", steps_e((-4, 2), [("t", 6, 0), ("rx",)]) + " x is positive and y is negative: Quadrant IV."))
    assert len(its) == 20, len(its)
    return {"title": "Combinations: translate, reflect and rotate", "items": its}


# ------------------------------------------------------------ set 5: which transformation? and word problems
SINGLE = {"a translation": "translation", "a reflection in the x-axis": ("rx",), "a reflection in the y-axis": ("ry",),
          "a rotation of 90° clockwise": ("cw",), "a rotation of 90° counterclockwise": ("ccw",), "a rotation of 180°": ("half",)}
ORDER = list(SINGLE)


def which_q(A, B, choices, label, lead, rnd_unused=None):
    """A single transformation question: exactly one of the choices maps A onto B."""
    choices = sorted(choices, key=ORDER.index)
    right = [c for c in choices if maps(A, B, SINGLE[c])]
    assert len(right) == 1, (A, B, right)
    return choices, right[0]


def set_which(rnd, P):
    its = []
    # grids: which single transformation maps A to B?
    for A, st, choices in [
        ([(-5, 2), (-2, 2), (-5, 4)], ("t", 6, -5), ["a translation", "a reflection in the x-axis", "a reflection in the y-axis", "a rotation of 180°"]),
        ([(-5, 1), (-2, 1), (-2, 4)], ("ry",), ["a translation", "a reflection in the x-axis", "a reflection in the y-axis", "a rotation of 180°"]),
        ([(2, 1), (5, 1), (2, 3)], ("half",), ["a translation", "a reflection in the x-axis", "a reflection in the y-axis", "a rotation of 180°"]),
        ([(-5, 1), (-2, 1), (-5, 3)], ("cw",), ["a reflection in the y-axis", "a rotation of 90° clockwise", "a rotation of 90° counterclockwise", "a rotation of 180°"]),
    ]:
        B = runs(A, [st])
        ch, ans = which_q(A, B, choices, None, None)
        if st[0] == "t":
            e = ("Triangle B points the same way as triangle A: it only slid. That is a translation (%s). "
                 "A reflection or a 180° turn would flip or turn the triangle." % mv(st[1], st[2]))
        else:
            e = ("Follow one vertex: %s → %s. %s Check the other vertices: they all land on triangle B, so it is %s."
                 % (pair(*A[1]), pair(*B[1]), step_e(A[1], st), ans))
        its.append(mcq_fixed(fig(two_shapes(A, B, "coordinate grid with triangle A and triangle B")) +
                             "Which single transformation maps triangle A onto triangle B?", ch, ans, e))
    # from coordinates
    for A, st, choices in [
        ([(2, 1), (5, 1), (5, 3)], ("ry",), ["a reflection in the x-axis", "a reflection in the y-axis", "a rotation of 90° clockwise", "a rotation of 180°"]),
        ([(-1, 2), (-1, 5), (-3, 5)], ("cw",), ["a reflection in the x-axis", "a rotation of 90° clockwise", "a rotation of 90° counterclockwise", "a rotation of 180°"]),
    ]:
        B = runs(A, [st])
        ch, ans = which_q(A, B, choices, None, None)
        e = "Compare each vertex with its image. %s The rule works for every vertex, so it is %s." % (step_e(A[0], st), ans)
        its.append(mcq_fixed("Triangle PQR has vertices %s. Its image has vertices %s, in the same order. Which single transformation was used?"
                             % (plist(A), plist(B)), ch, ans, e))
    # which combination?
    for A, steps, wrongs in [
        ([(-3, 2), (-1, 2), (-1, 5)], [("ry",), ("t", 0, -3)],
         [[("rx",), ("t", 0, -3)], [("ry",), ("t", 0, 3)], [("t", 0, -3), ("rx",)]]),
        ([(1, 2), (4, 2), (4, 4)], [("half",), ("t", 5, 0)],
         [[("half",), ("t", -5, 0)], [("ry",), ("t", 5, 0)], [("t", 5, 0), ("half",)]]),
    ]:
        B = runs(A, steps)
        right = combo_text(steps).capitalize()
        cands = []
        for w in wrongs:
            assert not same_set(runs(A, w), B), w
            cands.append(combo_text(w).capitalize())
        its.append(mcq("Triangle ABC has vertices %s. Its image has vertices %s, in the same order. Which combination maps the triangle onto its image?"
                       % (plist(A), plist(B)), right, cands,
                       "Test it on one vertex. " + steps_e(A[0], steps) + " The other vertices work the same way.", rnd))
    # word problems in BC contexts
    its.append(mcq("A BC Ferries route is drawn on a grid map. A ferry leaves a terminal at %s and sails %s. Where does it arrive?"
                   % (pair(-5, -2), mv(7, 4)), pair(2, 2), trans_cands((-5, -2), 7, 4),
                   step_e((-5, -2), ("t", 7, 4)), rnd))
    n, he, his = P.next()
    its.append(mcq("On a whale-watching trip near Victoria, %s marks an orca on a grid map at %s. Later the orca is at %s. "
                   "Describe the orca’s move as a translation." % (n, pair(4, -3), pair(-2, 1)),
                   mv(-6, 4), describe_cands((4, -3), (-2, 1)), describe_e((4, -3), (-2, 1)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a cedar tree beside a lake. The shoreline is the x-axis, and the top of the tree is at %s. "
                   "%s draws the tree’s reflection in the water. Where is the top of the reflection?" % (n, pair(-2, 5), he.capitalize()),
                   pair(-2, -5), [pair(2, 5), pair(2, -5), pair(5, -2)],
                   "The water line is the x-axis, so reflect in the x-axis: x stays %s, y changes sign. %s → %s." % (num(-2), pair(-2, 5), pair(-2, -5)), rnd))
    n, he, his = P.next()
    steps = [("ry",), ("t", 0, -2)]
    its.append(mcq("%s designs a logo for %s school’s lacrosse team in Kamloops. One corner of the left half is at %s. %s reflects it in the y-axis "
                   "to make the right half, then translates the whole logo 2 units down to fit the T-shirt. Where is the image of that corner?"
                   % (n, his, pair(-4, 3), he.capitalize()), pair(*run((-4, 3), steps)), combo_cands((-4, 3), steps),
                   steps_e((-4, 3), steps), rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a quilt square for a class display. A triangle piece has a vertex at %s. %s rotates the piece 90° clockwise "
                   "about the centre of the square (the origin) to place the next piece. Where is the vertex now?" % (n, pair(1, 4), he.capitalize()),
                   pair(4, -1), rot_cands((1, 4), "cw"), step_e((1, 4), ("cw",)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a pinwheel for a Terry Fox Run poster. One blade tip is at %s. The opposite blade is the first one rotated 180° "
                   "about the origin. Where is its tip?" % (n, pair(2, 5)), pair(-2, -5), rot_cands((2, 5), "half"),
                   step_e((2, 5), ("half",)), rnd))
    n, he, his = P.next()
    steps = [("t", 6, -7), ("ry",)]
    its.append(mcq("In a snowboarding video game, %s’s rider is at %s on the screen grid. The rider jumps %s, then the screen is flipped "
                   "(reflected in the y-axis). Where is the rider now?" % (n, pair(-5, 4), mv(6, -7)),
                   pair(*run((-5, 4), steps)), combo_cands((-5, 4), steps), steps_e((-5, 4), steps), rnd))
    n, he, his = P.next()
    steps = [("ccw",), ("t", 4, 0)]
    its.append(mcq("In a coding app, %s’s sprite is at %s. %s rotates it 90° counterclockwise about the origin, then translates it 4 units right. "
                   "Where does it end up?" % (n, pair(3, 2), he.capitalize()),
                   pair(*run((3, 2), steps)), combo_cands((3, 2), steps), steps_e((3, 2), steps), rnd))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert run((3, -5), [("half",)]) == run((3, -5), [("rx",), ("ry",)]) == (-3, 5)
    its.append(mcq_fixed("A game piece moves from %s to %s. %s says it was a rotation of 180° about the origin. %s says it was a reflection in "
                         "the x-axis, then a reflection in the y-axis. Who is right?" % (pair(3, -5), pair(-3, 5), n1, n2),
                         ["Only %s" % n1, "Only %s" % n2, "Both of them", "Neither of them"], "Both of them",
                         "180° rotation: both signs change, %s → %s. Two reflections: %s → %s → %s. Both give the same image."
                         % (pair(3, -5), pair(-3, 5), pair(3, -5), pair(3, 5), pair(-3, 5))))
    n, he, his = P.next()
    end = (2, -3)
    start = run(end, [("rx",), ("t", 0, -4)])
    assert run(start, [("t", 0, 4), ("rx",)]) == end and start == (2, -1)
    its.append(mcq("In a board game, %s’s piece was translated 4 units up, then reflected in the x-axis. It ended at %s. Where did it start?"
                   % (n, pair(*end)), pair(*start),
                   [pair(*run(end, [("t", 0, -4), ("rx",)])), pair(*run(end, [("t", 0, -4)])), pair(*run(end, [("ry",), ("t", 0, -4)]))],
                   "Undo the steps in reverse order. Undo the reflection: %s → %s. Undo the translation (4 units down): y: %s. "
                   "The piece started at %s. Check: %s" % (pair(*end), pair(*T(end, ("rx",))), add_e(3, -4), pair(*start),
                                                          steps_e(start, [("t", 0, 4), ("rx",)])), rnd))
    steps = [("t", 3, 0), ("ry",)]
    its.append(mcq("A soccer coach in Surrey draws a play on a grid with the origin at the centre spot. A player at %s runs 3 units right. "
                   "Then the coach copies the play to the other side by reflecting it in the y-axis. Where is the player’s image?" % pair(-4, 2),
                   pair(*run((-4, 2), steps)), combo_cands((-4, 2), steps), steps_e((-4, 2), steps), rnd))
    n, he, his = P.next()
    a, b = (-6, 1), (3, 0)
    assert run(a, [("t", 5, -3), ("t", 4, 2)]) == b
    its.append(mcq("%s plans a bike ride on a grid map of Stanley Park. From %s, %s rides %s, then %s. Which single translation "
                   "takes %s from the start to the end?" % (n, pair(*a), he, mv(5, -3), mv(4, 2), "her" if he == "she" else "him"),
                   mv(9, -1), [mv(1, -5), mv(9, -5), mv(-9, 1)],
                   "Add the moves. x: 5 + 4 = 9, so 9 units right. y: %s3 + 2 = %s1, so 1 unit down. Check: %s → %s."
                   % (MINUS, MINUS, pair(*a), pair(*b)), rnd))
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
    G = Grid(5)
    assert run((-4, 2), [("t", 3, 0), ("ry",)]) == (1, 2) and run((-4, 2), [("ry",), ("t", 3, 0)]) == (7, 2)
    G.arrow((-4, 2), (-1, 2))
    G.seg((-1, 2), (1, 2), GREEN, 2, dash=True)
    G.point(-4, 2, "P", RED, where=(-1, 1)).point(-1, 2, "Q", where=(-1, -1)).point(1, 2, "R", where=(1, 1))
    comb = G.svg("P (−4, 2) translated 3 units right to Q (−1, 2), then reflected in the y-axis to R (1, 2)")
    return (
        "<h2>Three ways to move a shape</h2>"
        "<p>A <b>transformation</b> moves a shape on the Cartesian plane. The shape keeps its size. "
        "The new shape is called the <b>image</b>. Grade 7 uses three kinds:</p>" +
        table(["Transformation", "What it does", "Rule for (x, y)"], [
            ["Translation", "slides the shape", "add or subtract: (x + a, y + b)"],
            ["Reflection in the x-axis", "flips it up or down", "(x, −y)"],
            ["Reflection in the y-axis", "flips it left or right", "(−x, y)"],
            ["Rotation of 90° clockwise", "turns it a quarter turn", "(y, −x)"],
            ["Rotation of 90° counterclockwise", "turns it a quarter turn the other way", "(−y, x)"],
            ["Rotation of 180°", "turns it a half turn", "(−x, −y)"],
        ]) +
        "<p>All rotations here are about the origin, (0, 0). Move every vertex with the same rule, then join the new vertices.</p>"
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
        "<p>For a quarter turn, swap the two numbers, then change one sign. Clockwise: change the sign of the <b>second</b> number. "
        "Counterclockwise: change the sign of the <b>first</b> number. For a half turn (180°), change both signs.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A turns 90° clockwise about the origin. The vertex (4, 2) goes to (2, −4).</figcaption></figure>" +
        ex("Example", "Rotate (2, 5) 90° counterclockwise about the origin.",
           "Swap: (5, 2). Change the sign of the first number: (−5, 2). Check: (2, 5) is in Quadrant I, and a counterclockwise quarter turn "
           "takes it to Quadrant II.", "(−5, 2)") +
        "<h2>Combinations of transformations</h2>"
        "<p>Do the steps one at a time, <b>in the order given</b>. The image of the first step is the starting point for the next. "
        "The order matters: changing it can give a different answer.</p>"
        "<figure class='sn-fig'>" + comb +
        "<figcaption>P (−4, 2) is translated 3 units right to Q (−1, 2), then reflected in the y-axis to R (1, 2).</figcaption></figure>" +
        ex("Combination", "Translate (−4, 2) 3 units right, then reflect it in the y-axis.",
           "Step 1: x: −4 + 3 = −1, so (−1, 2). Step 2: change the sign of x, so (1, 2). "
           "Doing the steps the other way round gives (4, 2), then (7, 2): a different point.", "(1, 2)") +
        ex("Which transformation?", "Which single transformation maps (3, −5) to (−3, 5)?",
           "Both signs changed and the numbers stayed in the same order. That is a half turn.", "a rotation of 180° about the origin") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Translating the wrong way", "Right and up add; left and down subtract"],
            ["Changing x for an up or down move", "Up and down change only y"],
            ["From −6 to 1 doing 6 − 1 = 5", "New minus old: 1 − (−6) = 7"],
            ["Reflecting in the wrong axis", "In the x-axis, y changes sign. In the y-axis, x changes sign"],
            ["Rotating the wrong way", "Clockwise goes the way clock hands move: from the top to the right"],
            ["Only swapping the numbers in a 90° turn: (3, 1) → (1, 3)", "Swap and change one sign: (1, −3) clockwise, (−1, 3) counterclockwise"],
            ["Doing a combination in the wrong order", "Do the first step, then use its image for the second step"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about transformations in BC?",
     "a": "In the BC Grade 7 curriculum (Geometry and measurement), students perform and describe combinations of transformations: translations, reflections in the axes and rotations about the origin, using coordinates in all four quadrants."},
    {"q": "How do you reflect a point in the x-axis or the y-axis?",
     "a": "In the x-axis, keep x and change the sign of y: (4, 1) becomes (4, −1). In the y-axis, keep y and change the sign of x: (4, 1) becomes (−4, 1)."},
    {"q": "How do you rotate a point 90° about the origin?",
     "a": "Swap the two numbers, then change one sign. For 90° clockwise, (x, y) becomes (y, −x); for 90° counterclockwise, it becomes (−y, x). A 180° turn changes both signs."},
    {"q": "Are transformations on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy assessment is based on the BC curriculum and asks students to apply math to real problems. Practising transformations builds the coordinate and spatial reasoning skills those problems use."},
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
    rnd = random.Random(37813)
    P = People(rnd)
    sets = [set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P), set_combine(rnd, P), set_which(rnd, P)]
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
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "combinations-of-transformations", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Combinations of Transformations: Translations, Reflections and Rotations",
        "seo_title": "Grade 7 Math: Combinations of Transformations Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Combinations of transformations",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 7: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Combinations of transformations",
        "meta_desc": "Free Grade 7 math worksheets on combinations of transformations for the BC curriculum: translate points and shapes, reflect them in the x- and y-axis, rotate them 90° and 180° about the origin, combine steps in order and name the transformation that maps one shape onto another. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Move every vertex with the same rule. In a combination, do the steps in order.",
        "key_sub": "Translation: right and up add, left and down subtract. Reflection in the x-axis changes the sign of y; in the y-axis, the sign of x. Rotation about the origin: 90° clockwise (x, y) → (y, −x), 90° counterclockwise (−y, x), 180° (−x, −y).",
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
