# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Perpendicular and parallel lines
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 3: Geometry — identifying perpendicular and
 parallel lines; drawing perpendicular and parallel lines on a square grid)
  python3 tools/gen_sg_maths_p3_lines.py
Every picture is built from exact coordinates. On a square grid every line joins grid points, so
"parallel" (same steps, cross product 0) and "perpendicular" (steps swapped and turned, dot product 0)
are tested in code with whole numbers. Every answer is the one found here.
Wrong answers come from real P3 mistakes: thinking lines must touch to be perpendicular, thinking
slanting lines cannot be parallel, thinking lines of different lengths cannot be parallel, taking the
mirror slant (2 right 1 up instead of 2 right 1 down) for a perpendicular, swapping the steps without
turning, miscounting squares by one, and calling any pair of crossing lines perpendicular.
HTML attributes use single quotes (no backslashes in the JSON). British spelling as used in Singapore.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
GRID = "#d9d3c9"
BLUE = "#2f6db5"
ROAD = "#b9b2a7"
BROWN = "#8a5a2b"
WHITE = "#ffffff"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


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
    """Choices keep their order (A B C D pictures, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, wrong, e):
    ch = sorted(set([correct] + [c for c in wrong if c >= 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


# ------------------------------------------------------------ geometry
def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dirv(deg):
    """Direction for an angle in degrees, anticlockwise on screen (SVG y goes down)."""
    t = math.radians(deg)
    return (math.cos(t), -math.sin(t))


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) + p[1] * math.sin(t), -p[0] * math.sin(t) + p[1] * math.cos(t))


def dir_diff(a, b):
    """Angle 0..90 between the directions of two vectors (as lines)."""
    t = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0]))) % 180
    return min(t, 180 - t)


def is_par(u, v):
    return dir_diff(u, v) < 1e-6


def is_perp(u, v):
    return abs(dir_diff(u, v) - 90) < 1e-6


def seg_hits_box(p, q, box, m):
    """Does segment pq come within m of the rectangle box (x0, y0, x1, y1)?"""
    x0, y0, x1, y1 = box[0] - m, box[1] - m, box[2] + m, box[3] + m
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return False
        else:
            r = qq / pp
            if pp < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True


def segs_touch(a, b, c, d):
    """Do closed segments ab and cd share a point?"""
    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)

    def on(p, q, r):
        return min(p[0], q[0]) - 1e-9 <= r[0] <= max(p[0], q[0]) + 1e-9 and min(p[1], q[1]) - 1e-9 <= r[1] <= max(p[1], q[1]) + 1e-9
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return (o1 == 0 and on(a, b, c)) or (o2 == 0 and on(a, b, d)) or (o3 == 0 and on(c, d, a)) or (o4 == 0 and on(c, d, b))


# ------------------------------------------------------------ drawing
class Fig:
    """Collects SVG elements, the strokes they draw and the label boxes, then checks that
    no label touches a stroke or another label."""

    def __init__(self):
        self.el, self.segs, self.boxes, self.ext = [], [], [], []

    def _seg(self, p, q, hw):
        self.segs.append((p, q, hw))
        for a in (p, q):
            self.ext += [(a[0] - hw, a[1] - hw), (a[0] + hw, a[1] + hw)]

    def line(self, p, q, w=3, col=GREEN, dash=None, cap="round"):
        d = " stroke-dasharray='%s'" % dash if dash else ""
        self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' "
                       "stroke-linecap='%s'%s/>" % (p[0], p[1], q[0], q[1], col, w, cap, d))
        self._seg(p, q, w / 2.0)

    def rect(self, x, y, w, h, fill, stroke="none", sw=0):
        self.el.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>"
                       % (x, y, w, h, fill, stroke, sw))
        self.ext += [(x - sw / 2.0, y - sw / 2.0), (x + w + sw / 2.0, y + h + sw / 2.0)]

    def dot(self, p, r=4, col=INK):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (p[0], p[1], r, col))
        self._seg(p, p, r)

    def _box(self, p, t, d, off, fs):
        d = norm(d)
        w, h = len(t) * fs * 0.62, fs * 0.72
        k = off + abs(d[0]) * w / 2 + abs(d[1]) * h / 2
        c = add(p, d, k)
        return c, (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2), h

    def _free(self, box, m=1.5):
        for p, q, hw in self.segs:
            if seg_hits_box(p, q, box, hw + m):
                return False
        for c in self.boxes:
            if not (box[2] + 2 < c[0] or c[2] + 2 < box[0] or box[3] + 2 < c[1] or c[3] + 2 < box[1]):
                return False
        return True

    def label(self, p, t, d, off=7, fs=16, halo=False, col=INK):
        c, box, h = self._box(p, t, d, off, fs)
        self.boxes.append(box)
        self.ext += [box[:2], box[2:]]
        hs = " stroke='%s' stroke-width='4' stroke-linejoin='round' paint-order='stroke'" % WHITE if halo else ""
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'%s>%s</text>"
                       % (c[0], c[1] + h / 2, fs, col, hs, t))

    def label_auto(self, p, t, dirs, off=6, fs=16, halo=True, col=INK):
        """Put the label in the first direction where it touches nothing."""
        for d in dirs:
            _, box, _ = self._box(p, t, d, off, fs)
            if self._free(box):
                self.label(p, t, d, off, fs, halo, col)
                return
        raise AssertionError("no room for label " + t)

    def poly(self, pts, fill=FILL, w=3):
        P = " ".join("%.1f,%.1f" % p for p in pts)
        self.el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                       % (P, fill, GREEN, w))
        n = len(pts)
        for i in range(n):
            self._seg(pts[i], pts[(i + 1) % n], w / 2.0)

    def mark(self, pts, w=1.8, col=INK):
        self.el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round' "
                       "stroke-linecap='round'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col, w))
        for i in range(len(pts) - 1):
            self._seg(pts[i], pts[i + 1], w / 2.0)

    def right_mark(self, v, u1, u2, k=10):
        q1 = add(v, u1, k)
        self.mark([q1, add(q1, u2, k), add(v, u2, k)], w=1.6)

    def arrow_mark(self, a, b, n=1, col=INK):
        """Small arrowheads in the middle of segment ab: the sign for parallel lines."""
        d = norm(sub(b, a))
        nr = (-d[1], d[0])
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        for r in range(n):
            tip = add(m, d, r * 6 - (n - 1) * 3 + 4)
            self.mark([add(add(tip, d, -7), nr, 5), tip, add(add(tip, d, -7), nr, -5)], w=2, col=col)

    def render(self):
        for b in self.boxes:
            for p, q, hw in self.segs:
                assert not seg_hits_box(p, q, b, hw + 1.5), ("label touches a stroke", b, p, q)
        for i, b in enumerate(self.boxes):
            for c in self.boxes[i + 1:]:
                assert b[2] + 2 < c[0] or c[2] + 2 < b[0] or b[3] + 2 < c[1] or c[3] + 2 < b[1], "labels overlap"
        xs, ys = [p[0] for p in self.ext], [p[1] for p in self.ext]
        return "".join(self.el), (min(xs), min(ys), max(xs), max(ys))

    def svg(self, label, pad=5):
        body, bb = self.render()
        W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
        if W == H:
            W += 1                                     # keep figures out of the larger 'square' print size
        dx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
        dy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
        return svg_wrap(W, H, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body), label)


DIRS8 = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, -1), (1, 1), (-1, 1)]


# ------------------------------------------------------------ square grid pictures
class GridFig(Fig):
    """A square grid (cols x rows squares of side s). Lines join grid points (x, y), y going down."""

    def __init__(self, cols, rows, s=20):
        Fig.__init__(self)
        self.s, self.cols, self.rows = s, cols, rows
        for i in range(cols + 1):
            self.el.append("<line x1='%d' y1='0' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (i * s, i * s, rows * s, GRID))
        for j in range(rows + 1):
            self.el.append("<line x1='0' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (j * s, cols * s, j * s, GRID))
        self.ext += [(0, 0), (cols * s, rows * s)]

    def P(self, g):
        assert 0 <= g[0] <= self.cols and 0 <= g[1] <= self.rows, ("off the grid", g)
        return (float(g[0] * self.s), float(g[1] * self.s))

    def gline(self, a, b, col=GREEN, w=3.4):
        self.line(self.P(a), self.P(b), w=w, col=col)

    def ends(self, a, b, names, fs=16):
        """Dots and letters at both ends of line ab (letters go beyond the ends where there is room)."""
        p, q = self.P(a), self.P(b)
        d = norm(sub(q, p))
        for pt, nm, out in ((p, names[0], (-d[0], -d[1])), (q, names[1], d)):
            self.dot(pt, 3.6)
        for pt, nm, out in ((p, names[0], (-d[0], -d[1])), (q, names[1], d)):
            if nm:
                self.label_auto(pt, nm, [out] + [(out[0] + e[0] * 0.8, out[1] + e[1] * 0.8) for e in DIRS8] + DIRS8, off=5, fs=fs)

    def tag(self, a, b, name, fs=16):
        """Letter naming a whole line, put near one end (A, B, C, D for choices)."""
        p, q = self.P(a), self.P(b)
        d = norm(sub(q, p))
        nr = (-d[1], d[0])
        if nr[1] > 0 or (nr[1] == 0 and nr[0] > 0):
            nr = (-nr[0], -nr[1])                       # first try the side above (or to the left of) the line
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        tries = [(m, nr), (m, (-nr[0], -nr[1]))]
        for end, out in ((p, (-d[0], -d[1])), (q, d)):
            tries += [(end, out), (end, add(out, nr, 0.9)), (end, add(out, nr, -0.9)), (end, nr), (end, (-nr[0], -nr[1]))]
        for end, dd in tries:
            _, box, _ = self._box(end, name, dd, 5, fs)
            if self._free(box):
                self.label(end, name, dd, 5, fs, True, BLUE)
                return
        raise AssertionError("no room for line name " + name)

    def point(self, g, name, fs=16, col=INK):
        p = self.P(g)
        self.dot(p, 4.2, col)
        return p


def sq(n):
    return "1 square" if n == 1 else "%d squares" % n


def steps(v):
    """How a line goes on the grid, read from left to right: e.g. '2 squares right and 1 square up'."""
    dx, dy = v
    if dx < 0 or (dx == 0 and dy > 0):
        dx, dy = -dx, -dy
    if dy == 0:
        return "%s straight across" % sq(dx)
    if dx == 0:
        return "%s straight up" % sq(-dy)
    return "%s right and %s %s" % (sq(dx), sq(abs(dy)), "up" if dy < 0 else "down")


def kind_word(v):
    if v[1] == 0:
        return "horizontal"
    if v[0] == 0:
        return "vertical"
    return "slanting"


def fit_shift(segs, pts=()):
    """Move grid coordinates so that the picture has a margin of 1 square all round."""
    allp = [p for s in segs for p in s[:2]] + list(pts)
    mx, my = min(p[0] for p in allp), min(p[1] for p in allp)
    W, H = max(p[0] for p in allp) - mx + 2, max(p[1] for p in allp) - my + 2
    return (1 - mx, 1 - my), W, H


def pair_svg(ab, cd, label, s=20, names="ABCD"):
    """Two lines AB and CD on a square grid. ab, cd: ((x, y), (x, y)) grid points."""
    (ox, oy), W, H = fit_shift([ab, cd])
    G = GridFig(W, H, s)
    mv = lambda p: (p[0] + ox, p[1] + oy)
    G.gline(mv(ab[0]), mv(ab[1]))
    G.gline(mv(cd[0]), mv(cd[1]))
    G.ends(mv(ab[0]), mv(ab[1]), names[:2])
    G.ends(mv(cd[0]), mv(cd[1]), names[2:])
    return G.svg(label + " on a square grid")


# ------------------------------------------------------------ plain line pairs (no grid)
def lines_fig(kind, rot=0, L=72):
    """A pair of lines. kinds: 'par' (parallel), 'parlen' (parallel, different lengths),
    'meet' (getting closer: would meet), 'perp' (cross at a right angle), 'perpT' (T shape),
    'perpL' (L corner), 'gap' (at right angles but not touching), 'cross' (cross at 55°),
    'V' (meet at one end at 50°), 'slantT' (one ends on the other at 60°)."""
    F = Fig()
    o = (0.0, 0.0)
    d = dirv(rot)
    nr = dirv(rot + 90)
    if kind == "par":
        for k in (-15, 15):
            c = add(o, nr, k)
            F.line(add(c, d, -L / 2), add(c, d, L / 2))
    elif kind == "parlen":
        c = add(o, nr, -15)
        F.line(add(c, d, -L / 2), add(c, d, L / 2))
        c = add(o, nr, 15)
        F.line(add(c, d, -L / 4), add(c, d, L / 3))
    elif kind == "meet":
        for sgn in (-1, 1):
            dd = dirv(rot + sgn * 9)
            c = add(o, nr, sgn * 15)
            F.line(add(c, dd, -L / 2), add(c, dd, L / 2))
    elif kind == "perp":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(add(o, nr, -L / 2), add(o, nr, L / 2))
    elif kind == "perpT":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(o, add(o, nr, L * 0.6))
    elif kind == "perpL":
        a = add(o, d, -L / 2)
        F.line(a, add(o, d, L / 2))
        F.line(a, add(a, nr, L * 0.7))
    elif kind == "gap":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(add(o, nr, 14), add(o, nr, L * 0.75))
    elif kind == "cross":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        e = dirv(rot + 55)
        F.line(add(o, e, -L / 2), add(o, e, L / 2))
    elif kind == "V":
        a = add(o, d, -L / 2)
        F.line(a, add(o, d, L / 2))
        F.line(a, add(a, dirv(rot + 50), L * 0.9))
    elif kind == "slantT":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(o, add(o, dirv(rot + 60), L * 0.65))
    return F


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def interior(pts):
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u, v = norm(sub(a, b)), norm(sub(c, b))
        base = math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1]))))
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out.append(base if cr * area > 0 else 360 - base)
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "not a simple polygon"
    return out


def placed(pts, rot, bw, bh):
    P = [rot_pt(p, rot) for p in pts]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [((p[0] - mx) * k, (p[1] - my) * k) for p in P]


def shape_fig(pts0, rot=0, bw=130, bh=80, sw=3, marks=False, arrows=False, vlabels=None, F=None, fs=16):
    """Shape drawn to scale. marks: small squares on right angles. arrows: arrow signs on parallel sides."""
    F = F or Fig()
    pts = placed(pts0, rot, bw, bh)
    n = len(pts)
    for a in interior(pts):
        assert abs(a - 90) < 1e-6 or abs(a - 90) >= 20, interior(pts)
    F.poly(pts, w=sw)
    if marks:
        A = interior(pts)
        for i in range(n):
            if abs(A[i] - 90) < 1e-6:
                v = pts[i]
                L1, L2 = math.hypot(*sub(pts[i - 1], v)), math.hypot(*sub(pts[(i + 1) % n], v))
                F.right_mark(v, norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v)), min(10, 0.2 * min(L1, L2)))
    if arrows:
        sides = [sub(pts[(i + 1) % n], pts[i]) for i in range(n)]
        par = [(i, j) for i in range(n) for j in range(i + 1, n) if is_par(sides[i], sides[j])]
        for c, (i, j) in enumerate(par):
            ref = sides[i]
            for s_ in (i, j):
                a, b = pts[s_], pts[(s_ + 1) % n]
                if sides[s_][0] * ref[0] + sides[s_][1] * ref[1] < 0:
                    a, b = b, a
                F.arrow_mark(a, b, c + 1)
    if vlabels:
        A = interior(pts)
        for i, t in enumerate(vlabels):
            u1, u2 = norm(sub(pts[i - 1], pts[i])), norm(sub(pts[(i + 1) % n], pts[i]))
            sg = 1 if A[i] > 180 else -1                # a corner that points inwards: put the letter outside
            F.label(pts[i], t, (sg * (u1[0] + u2[0]), sg * (u1[1] + u2[1])), off=5, fs=fs)
    return F


def shape_svg(pts, rot=0, bw=130, bh=80, label="shape", **kw):
    return shape_fig(pts, rot, bw, bh, **kw).svg(label)


def sides_of(pts, names):
    """(name, vector) for every side; a side is named with its letters in alphabetical order (AB, BC, CD, AD)."""
    n = len(pts)
    out = []
    for i in range(n):
        nm = "".join(sorted(names[i] + names[(i + 1) % n]))
        out.append((nm, sub(pts[(i + 1) % n], pts[i]), i))
    return out


def side_pairs(pts, test):
    S = sides_of(pts, "ABCDEFGH"[:len(pts)])
    return [(S[i][0], S[j][0]) for i in range(len(S)) for j in range(i + 1, len(S)) if test(S[i][1], S[j][1])]


def partners(pts, names, side, test):
    S = sides_of(pts, names)
    v = [s[1] for s in S if s[0] == side][0]
    return sorted(s[0] for s in S if s[0] != side and test(s[1], v))


RECT = [(0, 0), (150, 0), (150, 80), (0, 80)]                  # A top left, clockwise on screen
SQ = [(0, 0), (100, 0), (100, 100), (0, 100)]
TRAP = [(0, 80), (160, 80), (115, 0), (45, 0)]                 # AB at the bottom, CD at the top
RTRAP = [(0, 80), (150, 80), (90, 0), (0, 0)]                  # right angles at A and D
PARA = [(0, 80), (130, 80), (170, 0), (40, 0)]
RTRI = [(0, 0), (0, 90), (130, 90)]                            # right angle at B
TRI = [(0, 50), (150, 50), (60, 0)]
HEX = [add((0, 0), dirv(60 * i), 60) for i in range(6)]
LSHAPE = [(0, 0), (50, 0), (50, 60), (110, 60), (110, 100), (0, 100)]


# ------------------------------------------------------------ capital letters
LETTERS = {
    "H": [((0, 0), (0, 60)), ((40, 0), (40, 60)), ((0, 30), (40, 30))],
    "T": [((0, 0), (44, 0)), ((22, 0), (22, 60))],
    "E": [((0, 0), (0, 60)), ((0, 0), (36, 0)), ((0, 30), (30, 30)), ((0, 60), (36, 60))],
    "F": [((0, 0), (0, 60)), ((0, 0), (36, 0)), ((0, 30), (30, 30))],
    "L": [((0, 0), (0, 60)), ((0, 60), (36, 60))],
    "V": [((0, 0), (20, 60)), ((20, 60), (40, 0))],
    "N": [((0, 60), (0, 0)), ((0, 0), (40, 60)), ((40, 60), (40, 0))],
    "X": [((0, 0), (40, 60)), ((40, 0), (0, 60))],
    "Z": [((0, 0), (40, 0)), ((40, 0), (0, 60)), ((0, 60), (40, 60))],
    "A": [((0, 60), (20, 0)), ((20, 0), (40, 60)), ((10, 30), (30, 30))],
}


def letters_svg(chars, label="capital letters made of straight lines"):
    cw = 66
    F = Fig()
    for k, ch in enumerate(chars):
        st = LETTERS[ch]
        xs = [p[0] for s in st for p in s]
        ox = k * cw + (cw - max(xs)) / 2.0
        for a, b in st:
            F.line((ox + a[0], 6 + a[1]), (ox + b[0], 6 + b[1]), w=6)
    body, _ = F.render()
    return svg_wrap(cw * len(chars), 72, body, label)


def letter_pairs(ch, kind):
    """Pairs of strokes in a letter that are parallel, or perpendicular (meeting at a right angle)."""
    st = LETTERS[ch]
    n = 0
    for i in range(len(st)):
        for j in range(i + 1, len(st)):
            u, v = sub(st[i][1], st[i][0]), sub(st[j][1], st[j][0])
            if kind == "par" and is_par(u, v):
                n += 1
            if kind == "perp" and is_perp(u, v):
                n += 1
    return n


# ------------------------------------------------------------ A-D pictures
CELL = 118


def grid4_svg(figs, label="four pictures labelled A to D"):
    W = H = 2 * CELL
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, F in enumerate(figs):
        body, bb = F.render()
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        aw, ah = CELL - 26, CELL - 10
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        assert bw <= aw and bh <= ah, ("too big for the grid", bw, bh)
        dx = x0 + 21 + (aw - bw) / 2 - bb[0]
        dy = y0 + 5 + (ah - bh) / 2 - bb[1]
        s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)


def strip_svg(items, cw=128, label="figures", fs=15):
    rend = [F.render() for F, _ in items]
    top = max(bb[3] - bb[1] for _, bb in rend) + 8
    s = []
    for k, ((body, bb), (_, cap)) in enumerate(zip(rend, items)):
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        assert bw <= cw - 6, (cap, bw)
        dx = k * cw + (cw - bw) / 2 - bb[0]
        dy = (top - bh) / 2 - bb[1]
        s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body))
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (k * cw + cw / 2.0, top + 16, fs, INK, cap))
    return svg_wrap(cw * len(items), int(top + 24), "".join(s), label)


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def pick_grid(q, figs, why, pos, label="four pictures labelled A to D"):
    """figs[0] is the right answer. It goes to position p; the others keep their order."""
    p = pos.next()
    cells = figs[1:]
    cells.insert(p, figs[0])
    return mcq_fixed(fig(grid4_svg(cells, label)) + q, ["A", "B", "C", "D"], "ABCD"[p], "Picture %s %s" % ("ABCD"[p], why))


# ------------------------------------------------------------ set 1: perpendicular or not
def set_perp(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq("Two lines meet at a right angle. What are they called?", "perpendicular lines",
                   ["parallel lines", "horizontal lines", "curved lines"],
                   "Lines that meet at a right angle are perpendicular lines. Parallel lines never meet.", rnd))
    F = lines_fig("perpL", 0, 70)
    F.right_mark((-35.0, 0.0), (1.0, 0.0), dirv(90), 11)
    its.append(mcq(fig(F.svg("two lines with a small square in the corner")) +
                   "What does the small square in the corner show?", "The lines meet at a right angle",
                   ["The lines are parallel", "The shape is a square", "The lines are the same length"],
                   "The small square is the sign for a right angle. So these lines are perpendicular.", rnd))
    lab = "four pairs of lines labelled A to D"
    its.append(pick_grid("Which pair of lines is perpendicular?",
                         [lines_fig("perp", 0), lines_fig("cross", 10), lines_fig("par", 0), lines_fig("meet", 90)],
                         "shows two lines that cross at a right angle. The other crossing lines meet at a slant.", pos, lab))
    its.append(pick_grid("Which pair of lines is perpendicular?",
                         [lines_fig("perpT", 30), lines_fig("slantT", 0), lines_fig("V", 20), lines_fig("par", 120)],
                         "shows a line that meets the other line at a right angle. It is turned, but the angle is still a right angle.", pos, lab))
    its.append(pick_grid("Which pair of lines is perpendicular?",
                         [lines_fig("gap", 0), lines_fig("cross", 100), lines_fig("meet", 0), lines_fig("V", 200)],
                         "shows lines that do not touch, but if we make the short line longer, it meets the other line at a right angle. So they are perpendicular.", pos, lab))
    its.append(pick_grid("Which pair of lines is NOT perpendicular?",
                         [lines_fig("slantT", 20), lines_fig("perp", 30), lines_fig("perpL", 0), lines_fig("gap", 90)],
                         "shows a line that meets the other line at a slant, not at a right angle. The other three pairs are at right angles.", pos, lab))

    YES = "Yes, they meet at a right angle"
    YES_EXT = "Yes, they would meet at a right angle"
    NO = "No, they do not meet at a right angle"
    NO_PAR = "No, they are parallel"
    q = "Are lines AB and CD perpendicular?"
    cases = [
        (((0, 3), (6, 3)), ((3, 0), (3, 6)), YES, [NO, "No, they cross in the middle", NO_PAR],
         "AB goes straight across and CD goes straight up. They cross at a right angle, so they are perpendicular."),
        (((0, 4), (6, 4)), ((2, 4), (2, 0)), YES, [NO, "No, they do not cross", NO_PAR],
         "CD goes straight up from AB. It meets AB at a right angle, so the lines are perpendicular. They do not need to cross."),
        (((0, 3), (4, 1)), ((1, 0), (3, 4)), YES, ["No, both lines are slanting", NO, NO_PAR],
         "AB goes 2 squares right and 1 square up. CD goes 1 square right and 2 squares down. The steps swap and turn, so the lines meet at a right angle."),
        (((0, 4), (6, 4)), ((3, 0), (3, 3)), YES_EXT, ["No, they do not touch", NO_PAR, NO],
         "If we make CD longer, it meets AB at a right angle. Perpendicular lines do not need to touch in the picture."),
        (((0, 3), (6, 3)), ((1, 0), (5, 6)), NO, [YES, "Yes, they cross each other", NO_PAR],
         "CD goes 4 squares right and 6 squares down. It crosses AB at a slant, not at a right angle. Crossing lines are not always perpendicular."),
        (((0, 0), (0, 5)), ((2, 1), (6, 1)), YES_EXT, ["No, they do not touch", NO, NO_PAR],
         "AB is vertical and CD is horizontal. If we make CD longer to the left, it meets AB at a right angle."),
        (((0, 4), (6, 4)), ((3, 4), (5, 0)), NO, [YES, "Yes, they meet each other", NO_PAR],
         "CD meets AB, but it slants: it goes 2 squares right and 4 squares up. A line perpendicular to AB would go straight up."),
        (((0, 2), (6, 2)), ((0, 5), (6, 5)), NO_PAR, [YES_EXT, NO, "Yes, they are both straight"],
         "Both lines go straight across and stay 3 squares apart. They are parallel, so they never meet."),
    ]
    for ab, cd, ans, wrong, e in cases:
        u, v = sub(ab[1], ab[0]), sub(cd[1], cd[0])
        touch = segs_touch(ab[0], ab[1], cd[0], cd[1])
        if ans == YES:
            assert is_perp(u, v) and touch
        elif ans == YES_EXT:
            assert is_perp(u, v) and not touch
        elif ans == NO_PAR:
            assert is_par(u, v)
        else:
            assert not is_perp(u, v) and not is_par(u, v) and touch
        its.append(mcq(fig(pair_svg(ab, cd, "lines AB and CD")) + q, ans, wrong, e, rnd))
    n, he, his = P.next()
    ab, cd = ((0, 0), (5, 0)), ((2, 2), (2, 5))
    assert is_perp(sub(ab[1], ab[0]), sub(cd[1], cd[0])) and not segs_touch(ab[0], ab[1], cd[0], cd[1])
    its.append(mcq(fig(pair_svg(ab, cd, "lines AB and CD")) +
                   "%s says AB and CD are not perpendicular because they do not touch. Is %s right?" % (n, he),
                   "No, if we make CD longer, it meets AB at a right angle",
                   ["Yes, perpendicular lines must touch", "Yes, they are parallel", "No, they are parallel"],
                   "Make CD longer upwards and it meets AB at a right angle. Lines can be perpendicular even when they do not touch.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says that any two lines that cross are perpendicular. Is %s right?" % (n, he),
                   "No, they must cross at a right angle",
                   ["Yes, crossing lines are always perpendicular", "No, perpendicular lines never cross", "Yes, if the lines are long"],
                   "Perpendicular lines meet at a right angle. Lines can cross at a slant, and then they are not perpendicular.", rnd))
    row = ["L", "V", "X", "N"]
    assert [letter_pairs(c, "perp") > 0 for c in row] == [True, False, False, False]
    p = pos.next()
    r = row[1:]
    r.insert(p, row[0])
    its.append(mcq_fixed(fig(letters_svg(r)) + "Which capital letter has perpendicular lines?", r, "L",
                         "The 2 lines of L meet at a right angle. The lines in V, X and N meet at a slant."))
    its.append(mcq_num(fig(lines_fig("perp", 0, 70).svg("two lines crossing at a right angle")) +
                       "These two lines are perpendicular. How many right angles do they make where they cross?",
                       4, [1, 2, 3], "Where two perpendicular lines cross, they make 4 square corners: 4 right angles."))
    its.append(mcq("A horizontal line and a vertical line meet. How are the two lines?", "They are perpendicular",
                   ["They are parallel", "They are both slanting", "They make a straight line"],
                   "A horizontal line and a vertical line always meet at a right angle, so they are perpendicular.", rnd))
    its.append(mcq("Line CD is vertical. Line AB is perpendicular to CD. What kind of line is AB?", "horizontal",
                   ["vertical", "slanting", "curved"],
                   "A line perpendicular to a vertical line goes straight across, so AB is horizontal.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Perpendicular or not?", "items": its}


# ------------------------------------------------------------ set 2: parallel or not
def set_par(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq("What are parallel lines?", "lines that stay the same distance apart and never meet",
                   ["lines that meet at a right angle", "lines that are the same length", "lines that cross in the middle"],
                   "Parallel lines always stay the same distance apart, like railway tracks. They never meet, however long they are.", rnd))
    F = lines_fig("par", 25, 76)
    nr, d = dirv(115), dirv(25)
    for k in (-15, 15):
        c = add((0.0, 0.0), nr, k)
        F.arrow_mark(add(c, d, -38), add(c, d, 38))
    its.append(mcq(fig(F.svg("two lines with arrow signs")) + "What do the small arrows on these lines show?",
                   "The lines are parallel", ["The lines are perpendicular", "The lines will meet", "The lines go up"],
                   "Matching arrow signs on two lines show that the lines are parallel.", rnd))
    lab = "four pairs of lines labelled A to D"
    its.append(pick_grid("Which pair of lines is parallel?",
                         [lines_fig("par", 0), lines_fig("meet", 0), lines_fig("perp", 0), lines_fig("cross", 20)],
                         "shows lines that stay the same distance apart all the way along. The lines that get closer would meet if they were longer.", pos, lab))
    its.append(pick_grid("Which pair of lines is parallel?",
                         [lines_fig("par", 60), lines_fig("meet", 60), lines_fig("perpT", 0), lines_fig("V", 0)],
                         "shows slanting lines that stay the same distance apart. Slanting lines can be parallel too.", pos, lab))
    its.append(pick_grid("Which pair of lines is parallel?",
                         [lines_fig("parlen", 90), lines_fig("meet", 90), lines_fig("gap", 0), lines_fig("slantT", 10)],
                         "shows two lines of different lengths that stay the same distance apart. Parallel lines do not need to be the same length.", pos, lab))
    its.append(pick_grid("Which pair of lines is NOT parallel?",
                         [lines_fig("meet", 30), lines_fig("par", 90), lines_fig("parlen", 0), lines_fig("par", 135)],
                         "shows lines that get closer together, so they would meet if they were longer. The other three pairs stay the same distance apart.", pos, lab))

    YES = "Yes, they stay the same distance apart"
    NO_MEET = "No, they get closer and would meet"
    NO_PERP = "No, they are perpendicular"
    q = "Are lines AB and CD parallel?"
    cases = [
        (((0, 1), (6, 1)), ((0, 4), (6, 4)), YES, [NO_MEET, NO_PERP, "No, they are horizontal"],
         "Both lines go straight across and stay 3 squares apart. So they are parallel."),
        (((1, 0), (1, 5)), ((4, 0), (4, 5)), YES, ["No, they are vertical", NO_MEET, NO_PERP],
         "Both lines go straight up and stay 3 squares apart. Vertical lines can be parallel."),
        (((0, 4), (2, 0)), ((3, 4), (5, 0)), YES, ["No, they are slanting", NO_MEET, NO_PERP],
         "Both lines go 2 squares right and 4 squares up. They slant the same way, so they are parallel."),
        (((0, 3), (6, 0)), ((2, 5), (4, 4)), YES, ["No, they are not the same length", NO_MEET, NO_PERP],
         "AB goes 6 right and 3 up. CD goes 2 right and 1 up: for every 2 squares right, both go 1 square up. They are parallel even though CD is shorter."),
        (((0, 1), (6, 1)), ((0, 3), (6, 4)), NO_MEET, [YES, "Yes, they do not touch", NO_PERP],
         "The gap is 2 squares on the left but 3 squares on the right. The lines are not the same distance apart, so they are not parallel."),
        (((0, 0), (2, 4)), ((3, 0), (5, 3)), NO_MEET, [YES, "Yes, they slant the same way", NO_PERP],
         "AB goes 2 right and 4 down, but CD goes 2 right and only 3 down. The gap changes, so they are not parallel."),
        (((0, 4), (2, 0)), ((3, 0), (5, 4)), "No, they slant different ways", [YES, NO_PERP, "Yes, they are the same length"],
         "AB goes up to the right, but CD goes down to the right. They slant different ways, so they are not parallel."),
        (((0, 3), (6, 3)), ((3, 0), (3, 5)), NO_PERP, [YES, NO_MEET, "Yes, they are straight lines"],
         "AB goes straight across and CD goes straight up. They cross at a right angle, so they are perpendicular, not parallel."),
    ]
    for ab, cd, ans, wrong, e in cases:
        u, v = sub(ab[1], ab[0]), sub(cd[1], cd[0])
        if ans == YES:
            assert is_par(u, v)
        elif ans == NO_PERP:
            assert is_perp(u, v)
        else:
            assert not is_par(u, v) and not is_perp(u, v) and not segs_touch(ab[0], ab[1], cd[0], cd[1])
        its.append(mcq(fig(pair_svg(ab, cd, "lines AB and CD")) + q, ans, wrong, e, rnd))
    n, he, his = P.next()
    ab, cd = ((0, 4), (4, 0)), ((3, 5), (6, 2))
    assert is_par(sub(ab[1], ab[0]), sub(cd[1], cd[0]))
    its.append(mcq(fig(pair_svg(ab, cd, "slanting lines AB and CD")) +
                   "%s says AB and CD cannot be parallel because they are slanting. Is %s right?" % (n, he),
                   "No, they slant the same way and stay the same distance apart",
                   ["Yes, parallel lines must go straight across", "Yes, they will meet", "No, they are perpendicular"],
                   "Both lines go 1 square right for every 1 square up. Slanting lines can be parallel.", rnd))
    n, he, his = P.next()
    ab, cd = ((0, 1), (7, 1)), ((2, 3), (5, 3))
    its.append(mcq(fig(pair_svg(ab, cd, "a long line AB and a short line CD")) +
                   "%s says AB and CD are not parallel because CD is shorter. Is %s right?" % (n, he),
                   "No, parallel lines can be different lengths",
                   ["Yes, parallel lines must be the same length", "Yes, the lines will meet", "No, they are perpendicular"],
                   "Both lines go straight across and stay 2 squares apart. Length does not matter: they are parallel.", rnd))
    row = ["H", "L", "T", "V"]
    assert [letter_pairs(c, "par") > 0 for c in row] == [True, False, False, False]
    p = pos.next()
    r = row[1:]
    r.insert(p, row[0])
    its.append(mcq_fixed(fig(letters_svg(r)) + "Which capital letter has a pair of parallel lines?", r, "H",
                         "The 2 upright lines of H are parallel. L, T and V have no lines going the same way."))
    row = ["V", "E", "Z", "H"]
    assert [letter_pairs(c, "par") == 0 for c in row] == [True, False, False, False]
    p = pos.next()
    r = row[1:]
    r.insert(p, row[0])
    its.append(mcq_fixed(fig(letters_svg(r)) + "Which capital letter has NO parallel lines?", r, "V",
                         "The 2 lines of V meet at the bottom, so they are not parallel. E, Z and H all have lines going the same way."))
    its.append(mcq("Line AB is horizontal. Line CD is parallel to AB. What kind of line is CD?", "horizontal",
                   ["vertical", "slanting", "perpendicular to the floor"],
                   "A line parallel to a horizontal line goes the same way: straight across. So CD is horizontal.", rnd))
    its.append(mcq("If we make two parallel lines longer and longer, what happens?", "They never meet",
                   ["They meet far away", "They cross at a right angle", "They get closer"],
                   "Parallel lines stay the same distance apart all the way along, so they never meet.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel or not?", "items": its}


# ------------------------------------------------------------ set 3: pairs of lines in shapes and letters
def set_shapes(rnd, P):
    its = []
    pos = Pos(rnd)
    nm = "ABCD"
    g = dict(bw=130, bh=76, vlabels=nm)

    def sv(pts, label, rot=0, **kw):
        k = dict(g)
        k.update(kw)
        return fig(shape_svg(pts, rot, label=label, **k))

    assert partners(RECT, nm, "AB", is_par) == ["CD"]
    its.append(mcq(sv(RECT, "rectangle ABCD") + "Which side of rectangle ABCD is parallel to AB?", "CD",
                   ["BC", "AD", "none of them"],
                   "AB is the top side and CD is the bottom side. They stay the same distance apart, so CD is parallel to AB.", rnd))
    assert partners(RECT, nm, "AB", is_perp) == ["AD", "BC"]
    its.append(mcq(sv(RECT, "rectangle ABCD") + "Which sides of rectangle ABCD are perpendicular to AB?", "AD and BC",
                   ["CD only", "BC only", "AD and CD"],
                   "AD and BC meet AB at the corners A and B. Both corners are right angles, so AD and BC are perpendicular to AB.", rnd))
    n = len(side_pairs(RECT, is_par))
    its.append(mcq_num(sv(RECT, "rectangle ABCD") + "How many pairs of parallel sides does a rectangle have?", n, [1, 4, 3],
                       "AB is parallel to CD, and AD is parallel to BC. That is 2 pairs. (4 is the number of sides.)"))
    n = len(side_pairs(RECT, is_perp))
    its.append(mcq_num(sv(RECT, "rectangle ABCD") + "How many pairs of perpendicular sides does a rectangle have?", n, [2, 1, 3],
                       "Each of the 4 corners is a right angle, and each corner has a pair of perpendicular sides: AB and BC, BC and CD, CD and AD, AD and AB. That is 4 pairs."))
    n = len(side_pairs(placed(SQ, 30, 90, 90), is_par))
    its.append(mcq_num(sv(SQ, "square turned on a slant", 30, bw=90, bh=86, vlabels=None) +
                       "How many pairs of parallel sides does this turned square have?", n, [0, 1, 4],
                       "Turning a square does not change its sides. Opposite sides still stay the same distance apart: 2 pairs."))
    assert partners(TRAP, nm, "AB", is_par) == ["CD"]
    its.append(mcq(sv(TRAP, "trapezium ABCD") + "Which side of trapezium ABCD is parallel to AB?", "CD",
                   ["AD", "BC", "none of them"],
                   "AB at the bottom and CD at the top both go straight across and stay the same distance apart. So CD is parallel to AB.", rnd))
    n = len(side_pairs(TRAP, is_par))
    its.append(mcq_num(sv(TRAP, "trapezium ABCD") + "How many pairs of parallel sides does this trapezium have?", n, [2, 4, 3],
                       "Only AB and CD are parallel. AD and BC get closer at the top. A trapezium has exactly 1 pair of parallel sides."))
    assert not is_par(sides_of(TRAP, nm)[3][1], sides_of(TRAP, nm)[1][1])
    its.append(mcq(sv(TRAP, "trapezium ABCD") + "Are sides AD and BC of this trapezium parallel?", "No, they get closer at the top",
                   ["Yes, they are both slanting", "Yes, they are the same length", "No, they are perpendicular"],
                   "AD and BC lean towards each other: the gap is wider at the bottom than at the top. So they are not parallel.", rnd))
    assert partners(RTRAP, nm, "AD", is_perp) == ["AB", "CD"]
    its.append(mcq(sv(RTRAP, "trapezium ABCD with two right angles") + "Which two sides are perpendicular to AD?", "AB and CD",
                   ["BC and CD", "AB and BC", "BC only"],
                   "AD goes straight up. AB and CD go straight across and meet AD at right angles. BC is slanting.", rnd))
    n = len(side_pairs(RTRAP, is_perp))
    its.append(mcq_num(sv(RTRAP, "trapezium ABCD with two right angles") + "How many pairs of perpendicular sides does this shape have?",
                       n, [1, 4, 3], "AB and AD meet at a right angle, and AD and CD meet at a right angle. That is 2 pairs. BC meets the others at a slant."))
    assert partners(PARA, nm, "AD", is_par) == ["BC"]
    its.append(mcq(sv(PARA, "parallelogram ABCD") + "Which side of parallelogram ABCD is parallel to AD?", "BC",
                   ["AB", "CD", "none of them"],
                   "AD and BC slant the same way and stay the same distance apart. Slanting sides can be parallel."
                   , rnd))
    n = len(side_pairs(PARA, is_perp))
    its.append(mcq_num(sv(PARA, "parallelogram ABCD") + "How many pairs of perpendicular sides does this parallelogram have?",
                       n, [2, 4, 1], "None of the corners is a right angle, so no two sides are perpendicular. It has 2 pairs of parallel sides, but 0 pairs of perpendicular sides."))
    L6 = "ABCDEF"
    assert partners(LSHAPE, L6, "AB", is_par) == ["CD", "EF"]
    its.append(mcq_num(sv(LSHAPE, "L-shaped figure ABCDEF", bw=110, bh=96, vlabels=L6) +
                       "How many sides of this figure are parallel to AB?", 2, [1, 3, 5],
                       "AB goes straight across. CD and EF also go straight across, so 2 sides are parallel to AB."))
    assert partners(LSHAPE, L6, "AB", is_perp) == ["AF", "BC", "DE"]
    its.append(mcq_num(sv(LSHAPE, "L-shaped figure ABCDEF", bw=110, bh=96, vlabels=L6) +
                       "How many sides of this figure are perpendicular to AB?", 3, [2, 1, 5],
                       "AF, BC and DE go straight up and down, so all 3 are perpendicular to AB. DE does not touch AB, but it is still perpendicular."))
    S = sides_of(RTRI, "ABC")
    perp = [(S[i][0], S[j][0]) for i in range(3) for j in range(i + 1, 3) if is_perp(S[i][1], S[j][1])]
    assert perp == [("AB", "BC")], perp
    its.append(mcq(sv(RTRI, "right-angled triangle ABC", vlabels="ABC") + "Which two sides of triangle ABC are perpendicular?",
                   "AB and BC", ["AB and AC", "AC and BC", "none of them"],
                   "Sides AB and BC meet at corner B, which is a right angle. So AB and BC are perpendicular.", rnd))
    n = len(side_pairs(HEX, is_par))
    its.append(mcq_num(sv(HEX, "hexagon", bw=110, bh=96, vlabels=None) + "How many pairs of parallel sides does this hexagon have?",
                       n, [0, 1, 2], "Each side is parallel to the side opposite it. 6 sides make 3 pairs."))
    n = letter_pairs("E", "perp")
    its.append(mcq_num(fig(letters_svg(["E"], "capital letter E")) + "How many pairs of perpendicular lines are in the capital letter E?",
                       n, [1, 2, 4], "The upright line meets each of the 3 lines going across at a right angle. That is 3 pairs."))
    n = letter_pairs("H", "par")
    its.append(mcq_num(fig(letters_svg(["H"], "capital letter H")) + "How many pairs of parallel lines are in the capital letter H?",
                       n, [2, 3, 4], "Only the 2 upright lines are parallel: 1 pair. The middle line is perpendicular to them."))
    lab = "four shapes labelled A to D"
    k = dict(bw=80, bh=58, sw=2.6)
    its.append(pick_grid("Which shape has exactly 1 pair of parallel sides?",
                         [shape_fig(TRAP, 0, **k), shape_fig(RECT, 0, **k), shape_fig(PARA, 0, **k), shape_fig(TRI, 0, **k)],
                         "is a trapezium: only its top and bottom are parallel. The rectangle and the parallelogram have 2 pairs, and the triangle has none.", pos, lab))
    its.append(pick_grid("Which shape has NO perpendicular sides?",
                         [shape_fig(PARA, 0, **k), shape_fig(RECT, 0, **k), shape_fig(RTRI, 0, **k), shape_fig(RTRAP, 0, **k)],
                         "is a parallelogram: none of its corners is a right angle. The other shapes all have right angles.", pos, lab))
    assert len(side_pairs(placed(TRAP, 0, 80, 58), is_par)) == 1 and len(side_pairs(placed(TRI, 0, 80, 58), is_par)) == 0
    assert len(side_pairs(placed(PARA, 0, 80, 58), is_perp)) == 0
    assert all(len(side_pairs(placed(s, 0, 80, 58), is_perp)) > 0 for s in (RECT, RTRI, RTRAP))
    assert len(its) == 20, len(its)
    return {"title": "Find pairs of lines in shapes and letters", "items": its}


# ------------------------------------------------------------ set 4: on a square grid
SLOT = 4                                    # each choice line sits in a 4 x 4 box of squares


def fits(v):
    return v != (0, 0) and abs(v[0]) <= SLOT and abs(v[1]) <= SLOT


def slot_svg(pq, cands, label, s=18):
    """Line PQ on the left; four lines in boxes A B / C D on the right of one square grid."""
    cols, rows = 16, 10
    G = GridFig(cols, rows, s)
    vx, vy = pq
    assert abs(vx) <= 4 and abs(vy) <= rows - 2
    x0 = (4 - abs(vx)) // 2 + (0 if vx >= 0 else abs(vx))
    y0 = (rows - abs(vy)) // 2 + (0 if vy >= 0 else abs(vy))
    a, b = (x0, y0), (x0 + vx, y0 + vy)
    G.gline(a, b, col=INK, w=3.6)
    G.ends(a, b, "PQ")
    origins = [(6, 0), (12, 0), (6, 6), (12, 6)]
    for k, (v, o) in enumerate(zip(cands, origins)):
        assert fits(v), v
        sx = o[0] + (SLOT - abs(v[0])) // 2 + (0 if v[0] >= 0 else abs(v[0]))
        sy = o[1] + (SLOT - abs(v[1])) // 2 + (0 if v[1] >= 0 else abs(v[1]))
        p, q = (sx, sy), (sx + v[0], sy + v[1])
        G.gline(p, q)
        G.tag(p, q, "ABCD"[k])
    return G.svg(label)


def flip(v):
    return (v[0], -v[1])


def turn(v):
    return (v[1], -v[0])


def set_grid(rnd, P):
    its = []
    pos = Pos(rnd)
    lab = "line PQ and lines A to D on a square grid"

    def ask(pq, want, cands, why):
        """cands[0] is the answer. Checks that exactly one line is parallel (or perpendicular) to PQ."""
        test = is_par if want == "parallel" else is_perp
        assert [test(c, pq) for c in cands] == [True, False, False, False], (pq, cands)
        assert len(set(cands)) == 4
        p = pos.next()
        cells = cands[1:]
        cells.insert(p, cands[0])
        L = "ABCD"[p]
        e = "PQ goes %s. Line %s goes %s. %s" % (steps(pq), L, steps(cands[0]), why.replace("#", L))
        return mcq_fixed(fig(slot_svg(pq, cells, lab)) + "Which line is %s to PQ?" % want, list("ABCD"), L, e)

    # parallel: same steps (or the same steps made smaller)
    its.append(ask((4, 0), "parallel", [(3, 0), (0, 4), (4, 1), (3, -1)],
                   "Both go straight across, so # is parallel to PQ. Being shorter does not matter."))
    its.append(ask((0, 6), "parallel", [(0, 4), (4, 0), (1, 4), (-1, 4)],
                   "Both go straight up, so # is parallel to PQ."))
    its.append(ask((4, -2), "parallel", [(2, -1), (2, 1), (1, 2), (3, -1)],
                   "For every 2 squares right, both go 1 square up, so # is parallel. A line going 2 right and 1 down slants the other way."))
    its.append(ask((2, 4), "parallel", [(2, 4), (2, -4), (4, -2), (2, 3)],
                   "Both go the same steps, so # is parallel to PQ. Check the steps: 2 right and 3 down is a different slant."))
    its.append(ask((3, -1), "parallel", [(3, -1), (1, -3), (3, 1), (1, 3)],
                   "The steps are the same, so # is parallel. Swapping the steps (1 right and 3 up) gives a different line."))
    its.append(ask((3, 3), "parallel", [(4, 4), (3, -3), (3, 2), (2, 4)],
                   "For every 1 square right, both go 1 square down, so # is parallel. The line going up to the right is perpendicular."))
    # perpendicular: swap the steps and turn
    its.append(ask((4, 0), "perpendicular", [(0, 4), (4, 0), (1, 4), (3, 3)],
                   "So they meet at a right angle if we make them longer: # is perpendicular to PQ."))
    its.append(ask((0, 6), "perpendicular", [(4, 0), (0, 3), (4, 1), (4, -2)],
                   "So # is perpendicular to PQ, even though they do not touch."))
    its.append(ask((4, -2), "perpendicular", [(2, 4), (4, 2), (2, -4), (4, -2)],
                   "Swap the steps (2 and 4) and turn the slant: # is perpendicular. 4 right and 2 down is only the mirror slant, not a right angle."))
    its.append(ask((1, -3), "perpendicular", [(3, 1), (3, -1), (1, 3), (1, -3)],
                   "The steps 1 and 3 are swapped and the slant is turned, so # meets PQ at a right angle."))
    its.append(ask((2, 4), "perpendicular", [(4, -2), (4, 2), (2, -4), (3, -2)],
                   "The steps 2 and 4 are swapped and the slant is turned, so # is perpendicular to PQ."))
    its.append(ask((3, 3), "perpendicular", [(3, -3), (3, 3), (4, 3), (3, 0)],
                   "PQ goes down to the right and # goes up to the right, 1 square for every 1 square. They meet at a right angle."))
    # counting
    c4 = [(2, -1), (4, -2), (1, -2), (4, 2)]
    pq = (4, -2)
    n = sum(1 for c in c4 if is_par(c, pq))
    assert n == 2
    its.append(mcq_fixed(fig(slot_svg(pq, c4, lab)) + "How many of the lines A to D are parallel to PQ?", ["1", "2", "3", "4"], str(n),
                         "PQ goes 4 right and 2 up. A goes 2 right and 1 up, and B goes 4 right and 2 up: both are parallel. C and D slant differently."))
    c4 = [(3, 0), (0, 4), (2, 0), (4, 0)]
    pq = (0, 6)
    n = sum(1 for c in c4 if is_perp(c, pq))
    assert n == 3
    its.append(mcq_fixed(fig(slot_svg(pq, c4, lab)) + "How many of the lines A to D are perpendicular to PQ?", ["1", "2", "3", "4"], str(n),
                         "PQ is vertical. Lines A, C and D go straight across, so all 3 are perpendicular to PQ. B is vertical: it is parallel to PQ."))

    # drawing from a point
    def draw(pq_a, pq_b, R, want, good, wrong, why):
        test = is_par if want == "parallel" else is_perp
        v = sub(pq_b, pq_a)
        pts = [add(R, good)] + [add(R, w) for w in wrong]
        pts = [(int(p[0]), int(p[1])) for p in pts]
        assert test(good, v) and not any(test(w, v) for w in wrong), (v, good, wrong)
        assert len(set(pts)) == 4
        for i, u in enumerate([R] + pts):
            for w in ([R] + pts)[i + 1:]:
                assert math.hypot(u[0] - w[0], u[1] - w[1]) >= 2, ("points too close", u, w)
        p = pos.next()
        cells = pts[1:]
        cells.insert(p, pts[0])
        allp = [pq_a, pq_b, R] + cells
        mx, my = min(q[0] for q in allp), min(q[1] for q in allp)
        sh = lambda q: (q[0] - mx + 1, q[1] - my + 1)
        W = max(q[0] for q in allp) - mx + 2
        H = max(q[1] for q in allp) - my + 2
        G = GridFig(W, H, 20)
        G.gline(sh(pq_a), sh(pq_b), col=INK, w=3.6)
        G.ends(sh(pq_a), sh(pq_b), "PQ")
        G.point(sh(R), "R", col=GREEN)
        for k, c in enumerate(cells):
            G.point(sh(c), "ABCD"[k], col=BLUE)
        G.label_auto(G.P(sh(R)), "R", DIRS8, off=8, col=GREEN)
        for k, c in enumerate(cells):
            G.label_auto(G.P(sh(c)), "ABCD"[k], DIRS8, off=8, col=BLUE)
        L = "ABCD"[p]
        n, he, his = P.next()
        q = ("%s draws a line from point R. %s wants it to be %s to PQ. Which point should %s join R to?"
             % (n, he.capitalize(), want, he))
        e = "PQ goes %s. From R to %s goes %s. %s" % (steps(v), L, steps(good), why)
        return mcq_fixed(fig(G.svg("line PQ, point R and points A to D on a square grid")) + q, list("ABCD"), L, e)

    its.append(draw((1, 1), (5, 1), (1, 4), "parallel", (4, 0), [(4, 2), (0, 3), (3, -2)],
                    "Both go straight across, so the lines are parallel."))
    its.append(draw((0, 2), (3, 0), (1, 6), "parallel", (6, -4), [(3, 2), (2, -3), (4, -2)],
                    "For every 3 squares right, both lines go 2 squares up, so they are parallel. Be careful: 2 right and 3 up swaps the steps."))
    its.append(draw((1, 1), (1, 5), (3, 3), "perpendicular", (4, 0), [(4, 2), (0, 3), (3, -2)],
                    "PQ is vertical and the new line is horizontal, so they meet at a right angle if we make them longer."))
    its.append(draw((0, 3), (4, 1), (5, 4), "perpendicular", (2, 4), [(4, 2), (2, -4), (4, -2)],
                    "Swap the steps (4 and 2) and turn the slant: up becomes down. 4 right and 2 down is only the mirror slant."))
    its.append(mcq("Line PQ goes 3 squares right and 1 square up. A line parallel to PQ goes …", "3 squares right and 1 square up",
                   ["1 square right and 3 squares up", "3 squares right and 1 square down", "1 square right and 3 squares down"],
                   "A parallel line has the same steps: 3 squares right and 1 square up (it can start anywhere).", rnd))
    assert is_perp((1, 3), (3, -1))
    its.append(mcq("Line PQ goes 3 squares right and 1 square up. A line perpendicular to PQ goes …", "1 square right and 3 squares down",
                   ["1 square right and 3 squares up", "3 squares right and 1 square down", "3 squares right and 1 square up"],
                   "Swap the steps and turn the slant: 1 square right and 3 squares down. 1 right and 3 up only swaps the numbers, so it is not a right angle."
                   , rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel and perpendicular lines on a square grid", "items": its}


# ------------------------------------------------------------ set 5: real life
def railway_svg():
    F = Fig()
    for x in range(8, 260, 26):
        F.rect(x, 0, 12, 64, BROWN)
    F.line((0, 14), (272, 14), w=5, col=INK, cap="butt")
    F.line((0, 50), (272, 50), w=5, col=INK, cap="butt")
    return F.svg("railway track with two rails and sleepers")


def window_svg():
    F = Fig()
    F.rect(0, 0, 120, 90, "#e8f1f8", GREEN, 7)
    F.line((60, 0), (60, 90), w=6)
    F.line((0, 45), (120, 45), w=6)
    return F.svg("window frame with crossing bars")


def ladder_svg():
    F = Fig()
    F.line((0, 0), (0, 120), w=6, col=BROWN)
    F.line((54, 0), (54, 120), w=6, col=BROWN)
    for y in (16, 46, 76, 106):
        F.line((0, y), (54, y), w=5, col=BROWN)
    return F.svg("ladder with side rails and rungs")


def zebra_svg():
    F = Fig()
    F.rect(0, 0, 220, 80, ROAD)
    for x in range(10, 210, 30):
        F.rect(x, 6, 16, 68, WHITE)
    return F.svg("zebra crossing with white stripes")


def clock_svg(h):
    c = (56.0, 56.0)
    s = ["<circle cx='56' cy='56' r='52' fill='#ffffff' stroke='%s' stroke-width='3'/>" % GREEN]
    for i in range(12):
        d = dirv(90 - 30 * i)
        a, b = add(c, d, 47), add(c, d, 41 if i % 3 == 0 else 44)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>"
                 % (a + b + (INK, 2.4 if i % 3 == 0 else 1.4)))
    for num, i in (("12", 0), ("3", 3), ("6", 6), ("9", 9)):
        p = add(c, dirv(90 - 30 * i), 33)
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (p[0], p[1] + 5.4, INK, num))
    hd, md = dirv(90 - 30 * (h % 12)), dirv(90)
    hh, mh = add(c, hd, 20), add(c, md, 28)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock showing %d o’clock" % h)


def map_svg():
    F = Fig()
    F.line((0, 0), (300, 0), w=12, col=ROAD, cap="butt")          # School Road
    F.line((0, 90), (300, 90), w=12, col=ROAD, cap="butt")        # Park Road
    F.line((40, -25), (40, 115), w=12, col=ROAD, cap="butt")      # Lake Avenue
    F.line((210, -25), (270, 115), w=12, col=ROAD, cap="butt")    # Market Street
    F.label((128, -6), "School Road", (0, -1), off=4, fs=14)
    F.label((128, 96), "Park Road", (0, 1), off=4, fs=14)
    F.label((46, 45), "Lake Avenue", (1, 0), off=6, fs=14)
    F.label((247, 45), "Market Street", (1, 0), off=8, fs=14)
    return F.svg("street map with four roads")


def set_life(rnd, P):
    its = []
    rail = railway_svg()
    its.append(mcq(fig(rail) + "How are the two rails of a railway track?", "They are parallel",
                   ["They are perpendicular", "They meet far away", "They cross each other"],
                   "The rails stay the same distance apart all the way, so the train wheels can run on them. They are parallel.", rnd))
    its.append(mcq(fig(rail) + "The brown bars under the rails are called sleepers. How is each sleeper to the rails?", "perpendicular",
                   ["parallel", "slanting", "neither parallel nor perpendicular"],
                   "Each sleeper goes across the rails at a right angle, so it is perpendicular to the rails.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s looks along a long MRT track. The rails look as if they meet far away. Are the rails parallel?" % n,
                   "Yes, they only look closer far away",
                   ["No, they really meet far away", "No, they are perpendicular", "Yes, because they are long"],
                   "Things far away look smaller, so the gap looks smaller. The real gap stays the same, so the rails are parallel.", rnd))
    win = window_svg()
    its.append(mcq(fig(win) + "The two bars of this window cross in the middle. How are the bars?", "perpendicular",
                   ["parallel", "slanting", "neither parallel nor perpendicular"],
                   "One bar is vertical and one is horizontal. They cross at a right angle, so they are perpendicular.", rnd))
    its.append(mcq(fig(win) + "How are the top and bottom edges of this window frame?", "parallel",
                   ["perpendicular", "slanting", "they would meet"],
                   "The top and bottom edges both go straight across and stay the same distance apart. They are parallel.", rnd))
    lad = ladder_svg()
    its.append(mcq(fig(lad) + "How are the rungs (steps) of this ladder to each other?", "parallel",
                   ["perpendicular", "they would meet", "slanting"],
                   "All the rungs go straight across and stay the same distance apart, so they are parallel.", rnd))
    its.append(mcq(fig(lad) + "How is each rung of the ladder to the two side rails?", "perpendicular",
                   ["parallel", "slanting", "they do not meet"],
                   "Each rung meets the side rails at a right angle, so the rungs are perpendicular to the side rails.", rnd))
    YES = "Yes, they make a right angle"
    its.append(mcq(fig(clock_svg(3)) + "Look at the hands of the clock. Are they perpendicular?", YES,
                   ["No, the angle is too small", "No, they make a straight line", "No, they are parallel"],
                   "At 3 o’clock the minute hand points to 12 and the hour hand points to 3. They make a right angle, so they are perpendicular.", rnd))
    its.append(mcq(fig(clock_svg(1)) + "Look at the hands of the clock. Are they perpendicular?",
                   "No, the angle is smaller than a right angle",
                   [YES, "No, they make a straight line", "Yes, they meet in the middle"],
                   "At 1 o’clock the hands are only 1 hour mark apart. A right angle needs 3 hour marks, so they are not perpendicular.", rnd))
    its.append(mcq("At which of these times are the hands of a clock perpendicular?", "9 o’clock",
                   ["6 o’clock", "12 o’clock", "1 o’clock"],
                   "At 9 o’clock the hands point to 12 and 9: 3 hour marks apart, a right angle. At 6 o’clock they make a straight line.", rnd))
    m = map_svg()
    its.append(mcq(fig(m) + "Which road is parallel to School Road?", "Park Road",
                   ["Lake Avenue", "Market Street", "none of them"],
                   "Park Road goes across the map, the same way as School Road, and they stay the same distance apart. So they are parallel.", rnd))
    its.append(mcq(fig(m) + "Which road is perpendicular to School Road?", "Lake Avenue",
                   ["Park Road", "Market Street", "none of them"],
                   "Lake Avenue goes straight up and down the map and meets School Road at a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(m) + "%s says Market Street is perpendicular to School Road because they cross. Is %s right?" % (n, he),
                   "No, Market Street crosses at a slant",
                   ["Yes, roads that cross are perpendicular", "No, they are parallel", "Yes, it goes up and down"],
                   "Market Street slants. It crosses School Road, but not at a right angle, so it is not perpendicular.", rnd))
    its.append(mcq(fig(zebra_svg()) + "How are the white stripes of this zebra crossing?", "parallel",
                   ["perpendicular", "they would meet", "slanting"],
                   "Every stripe goes the same way and the stripes stay the same distance apart. They are parallel.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a square piece of paper in half, then in half again the other way. %s opens it. How are the two fold lines?"
                   % (n, he.capitalize()), "perpendicular", ["parallel", "slanting", "they do not meet"],
                   "The second fold goes across the first fold at a right angle, so the fold lines are perpendicular.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a long strip of paper in half, then in half again the same way. %s opens it. How are the fold lines?"
                   % (n, he.capitalize()), "parallel", ["perpendicular", "they cross", "slanting"],
                   "Every fold goes the same way across the strip, so the fold lines are parallel.", rnd))
    its.append(mcq("Which of these is NOT a pair of parallel lines?", "the hands of a clock at 3 o’clock",
                   ["the two rails of a railway track", "the top and bottom edges of a door", "the two lines of a running lane"],
                   "The hands at 3 o’clock meet at a right angle: they are perpendicular. The others stay the same distance apart.", rnd))
    its.append(mcq("In an HDB flat, the floor is horizontal and a wall is vertical. How are the floor and the wall?", "perpendicular",
                   ["parallel", "slanting", "they never meet"],
                   "A horizontal floor meets a vertical wall at a right angle, so they are perpendicular.", rnd))
    n, he, his = P.next()
    its.append(mcq("On Sports Day, %s runs in lane 3 on the straight part of the track. How are the lines of %s lane?" % (n, his),
                   "parallel", ["perpendicular", "they meet at the finish line", "slanting"],
                   "The two lines of a lane stay the same distance apart, so every runner has the same room. They are parallel.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws a ladder on square grid paper. The first rung goes 4 squares straight across. How should %s draw the next rung?"
                   % (n, he), "4 squares straight across, higher up",
                   ["4 squares straight up", "4 squares right and 1 square up", "1 square right and 4 squares up"],
                   "The rungs must be parallel, so the next rung goes the same way: straight across.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel and perpendicular lines around us", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    a = lines_fig("perp", 0, 70)
    a.right_mark((0.0, 0.0), (1.0, 0.0), dirv(90), 10)
    b = lines_fig("perpT", 30, 70)
    b.right_mark((0.0, 0.0), dirv(30), dirv(120), 10)
    c = lines_fig("gap", 0, 70)
    c.line((0.0, -3.0), (0.0, -14.0), w=2, col=INK, dash="3 3", cap="butt")
    perp = strip_svg([(a, "cross"), (b, "meet"), (c, "extend")], cw=120,
                     label="three pairs of perpendicular lines")
    pa = lines_fig("par", 0, 70)
    pb = lines_fig("par", 60, 70)
    pc = lines_fig("parlen", 90, 70)
    for F, rot, L1, L2 in ((pa, 0, 35, 35), (pb, 60, 35, 35)):
        d, nr = dirv(rot), dirv(rot + 90)
        for k in (-15, 15):
            cc = add((0.0, 0.0), nr, k)
            F.arrow_mark(add(cc, d, -L1), add(cc, d, L2))
    par = strip_svg([(pa, "across"), (pb, "slanting"), (pc, "different lengths")], cw=128,
                    label="three pairs of parallel lines")
    G = GridFig(14, 6, 20)
    G.gline((1, 4), (5, 2), col=INK, w=3.6)
    G.gline((6, 5), (10, 3))
    G.gline((11, 1), (13, 5))
    G.ends((1, 4), (5, 2), "PQ")
    G.ends((6, 5), (10, 3), "RS")
    G.ends((11, 1), (13, 5), "TU")
    assert is_par((4, -2), (4, -2)) and is_perp((4, -2), (2, 4))
    grid = G.svg("lines PQ, RS and TU on a square grid")
    shapes = strip_svg([(shape_fig(RECT, 0, 96, 56, sw=2.8, marks=True, arrows=True), "rectangle"),
                        (shape_fig(TRAP, 0, 100, 56, sw=2.8, arrows=True), "trapezium")],
                       cw=128, label="rectangle and trapezium with their parallel sides marked")
    return (
        "<h2>Perpendicular lines</h2>"
        "<p><b>Perpendicular lines</b> meet at a <b>right angle</b>. A small square in the corner shows the right angle. "
        "The lines can cross, meet at one end, or not touch at all: if we make them longer, they meet at a right angle.</p>"
        "<figure class='sn-fig'>" + perp +
        "<figcaption>All three pairs are perpendicular. In the last one, make the short line longer and it meets the other line at a right angle.</figcaption></figure>"
        "<p>We can write <b>AB ⊥ CD</b> for “AB is perpendicular to CD”.</p>"
        "<h2>Parallel lines</h2>"
        "<p><b>Parallel lines</b> stay the same distance apart. They never meet, however long we make them. "
        "They can go across, up and down or slanting, and they can be different lengths. Matching arrow signs show parallel lines.</p>"
        "<figure class='sn-fig'>" + par + "</figure>"
        "<p>We can write <b>AB // CD</b> for “AB is parallel to CD”.</p>"
        "<h2>On a square grid</h2>"
        "<p>Count the squares from one end of the line to the other. "
        "A <b>parallel</b> line has the same steps. A <b>perpendicular</b> line swaps the two numbers and turns the slant.</p>"
        "<figure class='sn-fig'>" + grid +
        "<figcaption>PQ and RS both go 4 squares right and 2 squares up: RS is parallel to PQ. "
        "TU goes 2 squares right and 4 squares down: TU is perpendicular to PQ.</figcaption></figure>" +
        ex("Example", "Line PQ goes 3 squares right and 1 square up. How does a line perpendicular to PQ go?",
           "Swap the numbers: 1 and 3. Turn the slant: up becomes down.", "1 square right and 3 squares down") +
        ex("Example", "Line AB goes 2 squares right and 1 square up. Line CD goes 4 squares right and 2 squares up. Are they parallel?",
           "For every 2 squares right, both lines go 1 square up. They have the same slant.", "Yes, AB // CD") +
        "<h2>In shapes and around us</h2>"
        "<p>A rectangle has 2 pairs of parallel sides and 4 right angles. A trapezium has exactly 1 pair of parallel sides. "
        "Railway tracks, ladder rungs and zebra crossings show parallel lines. The bars of a window cross at right angles.</p>"
        "<figure class='sn-fig'>" + shapes + "</figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking perpendicular lines must touch", "Make the lines longer: do they meet at a right angle?"],
            ["Thinking slanting lines cannot be parallel", "Check the gap: does it stay the same all the way?"],
            ["Thinking parallel lines must be the same length", "Length does not matter, only the direction"],
            ["Calling any crossing lines perpendicular", "Check the corner with a right angle"],
            ["On a grid, using the mirror slant for a perpendicular line", "Swap the steps and turn: 2 right 1 up becomes 1 right 2 down"],
        ])
    )


FAQ = [
    {"q": "What do P3 students learn about perpendicular and parallel lines?",
     "a": "They find perpendicular lines (lines that meet at a right angle) and parallel lines (lines that stay the same distance apart), and draw both kinds of lines on a square grid."},
    {"q": "How do I explain parallel lines to my child?",
     "a": "Show railway tracks or the lines of a running lane: the gap between the two lines stays the same, so they never meet. On grid paper, a parallel line goes the same number of squares across and up."},
    {"q": "What is the most common mistake with perpendicular lines?",
     "a": "Thinking that the lines must touch. Two lines are perpendicular if they would meet at a right angle when we make them longer."},
    {"q": "Is this topic in the MOE syllabus for Primary 3?",
     "a": "Yes. Identifying perpendicular and parallel lines and drawing them on a square grid are part of Geometry in the MOE 2021 Primary 3 syllabus. Angles in degrees follow in P4."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order
    (A-D pictures, numbers) stay as they are; the other questions fill the gaps."""
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
    rnd = random.Random(63812)
    P = People(rnd)
    sets = [set_perp(rnd, P), set_par(rnd, P), set_shapes(rnd, P), set_grid(rnd, P), set_life(rnd, P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "perpendicular-and-parallel-lines", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Perpendicular and Parallel Lines",
        "seo_title": "P3 Perpendicular and Parallel Lines Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Perpendicular and parallel lines",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 3: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Perpendicular and parallel lines; drawing them on a square grid",
        "meta_desc": "Free P3 maths practice: find perpendicular and parallel lines in shapes, letters and real life, and draw them on a square grid. 100 questions with answers.",
        "key_big": "Perpendicular lines meet at a right angle; parallel lines stay the same distance apart and never meet.",
        "key_sub": "On a grid: PQ goes 2 right and 1 up, a parallel line goes 2 right and 1 up, a perpendicular line goes 1 right and 2 down.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, grids, letters, the map) so they stay readable."""
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
        mark_large(u, "(four [a-z ]+ labelled A to D|[^']*square grid|capital letters made|street map|railway|zebra)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
