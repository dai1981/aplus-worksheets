# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Angles and lines (National Curriculum in England, Geometry – properties of shapes)
  python tools/gen_uk_maths_y3_angles_lines.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 3 sees an angle as a turn or a corner of a shape. Pupils compare angles with a right angle
(quarter turn): 2 right angles make a half turn, 3 a three-quarter turn and 4 a whole turn.
They also meet horizontal, vertical, perpendicular and parallel lines.
Every drawing is exact and checked in code: right angles are true right angles, any angle that is
not a right angle is at least 20° away from one, and no label touches a line.
Pictures where pupils must judge an angle have NO right-angle marks (they check with their eyes or
a paper right-angle checker); the lesson pictures use the small square mark.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
ROAD = "#b9b2a7"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


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
    """Choices keep their order (A B C D, turns, compass points, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c >= 0 and c != correct][:3]))
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

    def dot(self, p, r=4, col=INK):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (p[0], p[1], r, col))
        self._seg(p, p, r)

    def circle(self, p, r, fill=FILL, w=2.5):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='%s' stroke-width='%g'/>"
                       % (p[0], p[1], r, fill, GREEN, w))
        self.ext += [(p[0] - r - w, p[1] - r - w), (p[0] + r + w, p[1] + r + w)]
        self.segs.append((p, p, r + w / 2.0))

    def label(self, p, t, d, off=7, fs=16):
        d = norm(d)
        w, h = len(t) * fs * 0.62, fs * 0.72
        k = off + abs(d[0]) * w / 2 + abs(d[1]) * h / 2
        c = add(p, d, k)
        box = (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)
        self.boxes.append(box)
        self.ext += [box[:2], box[2:]]
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (c[0], c[1] + h / 2, fs, INK, t))

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

    def head(self, tip, d, col=GREEN, L=9, W=6):
        """Filled arrowhead with its tip at `tip`, pointing along d."""
        d = norm(d)
        nr = (-d[1], d[0])
        b = add(tip, d, -L)
        pts = [tip, add(b, nr, W), add(b, nr, -W)]
        self.el.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col))
        for i in range(3):
            self._seg(pts[i], pts[(i + 1) % 3], 0.5)

    def right_mark(self, v, u1, u2, k=10):
        q1 = add(v, u1, k)
        self.mark([q1, add(q1, u2, k), add(v, u2, k)], w=1.6)

    def arc(self, v, a1, a2, r, col=INK, w=1.8):
        n = max(6, int(abs(a2 - a1) / 6))
        self.mark([add(v, dirv(a1 + (a2 - a1) * i / n), r) for i in range(n + 1)], w=w, col=col)

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


def angle_fig(deg, rot=0, L=80, L2=None, marked=False, F=None):
    """Angle: two arms from a vertex, one at direction rot and one at rot + deg.
    marked=True draws the small square on a right angle (lesson only). Without marks, any angle
    that is not a right angle is at least 20° away from one, so pupils can judge it."""
    F = F or Fig()
    V = (0.0, 0.0)
    L2 = L2 or L
    d1, d2 = dirv(rot), dirv(rot + deg)
    assert deg == 90 or abs(deg - 90) >= 20, deg
    F.line(V, add(V, d1, L))
    F.line(V, add(V, d2, L2))
    F.dot(V, 3.5)
    if marked and deg == 90:
        F.right_mark(V, d1, d2, 12)
    return F


def cmp_word(deg):
    return "less than a right angle" if deg < 90 else "a right angle" if deg == 90 else \
        "greater than a right angle" if deg < 180 else "a straight line"


CMP = ["less than a right angle", "a right angle", "greater than a right angle", "a straight line"]


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def interior(pts):
    """Interior angles of a simple polygon (convex or not)."""
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


def rights(pts):
    return [i for i, a in enumerate(interior(pts)) if abs(a - 90) < 1e-6]


def tri_ang(a, b, base=120):
    """Triangle with angle a at the left end of the base and angle b at the right end (apex above)."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    return [(0.0, 0.0), (float(base), 0.0), add((0.0, 0.0), dirv(a), side)]


def para(a, b, deg):
    return [(0, 0), (a, 0), add((a, 0), dirv(deg), b), add((0, 0), dirv(deg), b)]


SQ = [(0, 0), (100, 0), (100, 100), (0, 100)]
RECT = [(0, 0), (150, 0), (150, 80), (0, 80)]
RECT2 = [(0, 0), (140, 0), (140, 70), (0, 70)]
EQUI = tri_ang(60, 60)
RTRI = tri_ang(90, 35)                     # right angle at the first corner
RTRI2 = tri_ang(90, 58)
OBTRI = tri_ang(25, 40)                    # obtuse angle at the apex
PARA = para(150, 80, 60)
RTRAP = [(0, 80), (150, 80), (80, 0), (0, 0)]
HEX = [add((0, 0), dirv(60 * i), 60) for i in range(6)]
HOUSE = [(0, 40), (40, 0), (80, 40), (80, 110), (0, 110)]
LSHAPE = [(0, 0), (50, 0), (50, 60), (110, 60), (110, 100), (0, 100)]
TSHAPE = [(0, 0), (120, 0), (120, 35), (80, 35), (80, 100), (40, 100), (40, 35), (0, 35)]
CUT = [(0, 0), (90, 0), (130, 40), (130, 90), (0, 90)]


def placed(pts, rot, bw, bh):
    P = [rot_pt(p, rot) for p in pts]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [((p[0] - mx) * k, (p[1] - my) * k) for p in P]


def shape_fig(pts0, rot=0, bw=130, bh=80, sw=3, marks=False, arrows=False, vlabels=None, F=None, fs=16):
    """Shape drawn to scale. marks: small squares on the right angles. arrows: arrows on parallel sides.
    Every corner that is not a right angle is at least 20° away from one."""
    F = F or Fig()
    pts = placed(pts0, rot, bw, bh)
    n = len(pts)
    A = interior(pts)
    for a in A:
        assert abs(a - 90) < 1e-6 or abs(a - 90) >= 20, A
    F.poly(pts, w=sw)
    if marks:
        for i in rights(pts):
            v = pts[i]
            L1, L2 = math.hypot(*sub(pts[i - 1], v)), math.hypot(*sub(pts[(i + 1) % n], v))
            F.right_mark(v, norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v)), min(10, 0.2 * min(L1, L2)))
    if arrows:
        sides = [sub(pts[(i + 1) % n], pts[i]) for i in range(n)]
        par = [(i, j) for i in range(n) for j in range(i + 1, n) if dir_diff(sides[i], sides[j]) < 1e-6]
        for c, (i, j) in enumerate(par):
            d = norm(sides[i])
            nr = (-d[1], d[0])
            for s_ in (i, j):
                a, b = pts[s_], pts[(s_ + 1) % n]
                m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                for r in range(c + 1):
                    tip = add(m, d, r * 5 - c * 2.5 + 4)
                    F.mark([add(add(tip, d, -7), nr, 5), tip, add(add(tip, d, -7), nr, -5)], w=2)
    if vlabels:
        for i, t in enumerate(vlabels):
            u1, u2 = norm(sub(pts[i - 1], pts[i])), norm(sub(pts[(i + 1) % n], pts[i]))
            F.label(pts[i], t, (-(u1[0] + u2[0]), -(u1[1] + u2[1])), off=5, fs=fs)
    return F


def shape_svg(pts, rot=0, bw=130, bh=80, label="shape", **kw):
    return shape_fig(pts, rot, bw, bh, **kw).svg(label)


# ------------------------------------------------------------ turns, compass, clocks, roads
def turn_fig(frac, cw=True, r=30):
    """Dashed start line pointing up, a curved arrow for the turn and a solid end line."""
    F = Fig()
    c = (0.0, 0.0)
    F.line(c, add(c, dirv(90), r + 12), w=2.4, col=INK, dash="5 4", cap="butt")
    sweep = 360.0 * frac
    sg = -1 if cw else 1
    draw = min(sweep - 20, 330.0)              # the arrowhead stops just before the end line
    n = max(8, int(draw / 5))
    end_a = 90 + sg * draw
    pts = [add(c, dirv(90 + sg * draw * i / n), r) for i in range(n + 1)]
    F.mark(pts, w=3, col=GREEN)
    end = add(c, dirv(end_a), r)
    F.head(add(end, dirv(end_a + sg * 90), 8), dirv(end_a + sg * 90), L=11, W=7)
    if frac < 1:
        F.line(c, add(c, dirv(90 + sg * sweep), r + 12), w=3, col=INK)
    F.dot(c, 4)
    return F


TURNS = ["quarter turn", "half turn", "three-quarter turn", "whole turn"]
TURN_FR = {"quarter turn": 0.25, "half turn": 0.5, "three-quarter turn": 0.75, "whole turn": 1.0}
POINTS = ["north", "east", "south", "west"]


def facing_fig(names, face, fs=16, R=50):
    """A pupil (circle) in the middle with an arrow to the way they face; names on the 4 sides
    (top, right, bottom, left)."""
    F = Fig()
    c = (0.0, 0.0)
    for i, t in enumerate(names):
        d = dirv(90 - 90 * i)
        F.label(add(c, d, R), t, d, off=0, fs=fs)
    d = dirv(90 - 90 * face)
    F.circle(c, 11)
    F.line(add(c, d, 13), add(c, d, 32), w=3.4, col=INK, cap="butt")
    F.head(add(c, d, 40), d, col=INK, L=10, W=7)
    return F


def compass_svg(face, label=None):
    return facing_fig(["N", "E", "S", "W"], face, fs=18, R=48).svg(label or "pupil facing %s" % POINTS[face])


def clock_face(s, c):
    s.append("<circle cx='56' cy='56' r='52' fill='#ffffff' stroke='%s' stroke-width='3'/>" % GREEN)
    for i in range(12):
        d = dirv(90 - 30 * i)
        a, b = add(c, d, 47), add(c, d, 41 if i % 3 == 0 else 44)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>"
                 % (a + b + (INK, 2.4 if i % 3 == 0 else 1.4)))
    for num, i in (("12", 0), ("3", 3), ("6", 6), ("9", 9)):
        p = add(c, dirv(90 - 30 * i), 33)
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (p[0], p[1] + 5.4, INK, num))


def clock_svg(h):
    """Analogue clock at h o'clock. Square picture (printed large)."""
    c = (56.0, 56.0)
    s = []
    clock_face(s, c)
    hd, md = dirv(90 - 30 * (h % 12)), dirv(90)
    hh, mh = add(c, hd, 17), add(c, md, 25)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock showing %d o’clock" % h)


def clock_turn_svg(start, quarters):
    """Minute hand: dashed where it started (pointing at `start`), solid where it ends after
    `quarters` quarter turns clockwise, with a curved arrow for the turn."""
    c = (56.0, 56.0)
    s = []
    clock_face(s, c)
    a0 = 90 - 30 * start
    sweep = min(90 * quarters - 24, 330)            # the arrowhead stops just before the hand
    n = max(8, int(sweep / 5))
    r = 15
    pts = [add(c, dirv(a0 - sweep * i / n), r) for i in range(n + 1)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (" ".join("%.1f,%.1f" % p for p in pts), GREEN))
    ea = a0 - sweep
    d = dirv(ea - 90)
    tip = add(add(c, dirv(ea), r), d, 8)
    nr = (-d[1], d[0])
    b = add(tip, d, -10)
    s.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in (tip, add(b, nr, 6), add(b, nr, -6))), GREEN))
    p0 = add(c, dirv(a0), 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' stroke-dasharray='4 3'/>" % (p0 + (INK,)))
    p1 = add(c, dirv(a0 - 90 * quarters), 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (p1 + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "clock with the minute hand turning")


def road(F, p, q, w=15):
    F.line(p, q, w=w, col=ROAD, cap="butt")


def junction_fig(kind, rot=0):
    """Road junctions. 'T': side road at a right angle. 'cross': crossroads at a right angle.
    'skew': crossroads at 60°. 'Y': side road at 45°. 'slant': side road at 125°."""
    F = Fig()
    o = (0.0, 0.0)
    if kind in ("T", "Y", "slant"):
        road(F, add(o, dirv(rot), 36), add(o, dirv(rot + 180), 36))
        a = {"T": 90, "Y": 45, "slant": 125}[kind]
        road(F, o, add(o, dirv(rot + a), 36))
    else:
        a = 90 if kind == "cross" else 60
        road(F, add(o, dirv(rot), 36), add(o, dirv(rot + 180), 36))
        road(F, add(o, dirv(rot + a), 36), add(o, dirv(rot + a + 180), 36))
    return F


def lines_fig(kind, rot=0, L=78):
    """One line or a pair of lines. kinds: 'one' (a line at angle rot), 'par' (parallel),
    'perp' (meet at a right angle, crossing), 'perpT' (T shape), 'meet' (getting closer: would meet),
    'cross' (cross at 55°)."""
    F = Fig()
    o = (0.0, 0.0)
    d = dirv(rot)
    nr = dirv(rot + 90)
    if kind == "one":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
    elif kind == "par":
        for k in (-14, 14):
            c = add(o, nr, k)
            F.line(add(c, d, -L / 2), add(c, d, L / 2))
    elif kind == "meet":
        for sgn in (-1, 1):
            dd = dirv(rot + sgn * 8)
            c = add(o, nr, sgn * 14)
            F.line(add(c, dd, -L / 2), add(c, dd, L / 2))
    elif kind == "perp":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(add(o, nr, -L / 2), add(o, nr, L / 2))
    elif kind == "perpT":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        F.line(o, add(o, nr, L * 0.6))
    elif kind == "cross":
        F.line(add(o, d, -L / 2), add(o, d, L / 2))
        e = dirv(rot + 55)
        F.line(add(o, e, -L / 2), add(o, e, L / 2))
    return F


def street_map_svg():
    F = Fig()
    road(F, (0, 0), (300, 0), 12)              # High Street
    road(F, (0, 90), (300, 90), 12)            # Mill Lane
    road(F, (40, -25), (40, 115), 12)          # Station Road
    road(F, (210, -25), (270, 115), 12)        # Park Road
    F.label((128, -6), "High Street", (0, -1), off=4, fs=14)
    F.label((128, 96), "Mill Lane", (0, 1), off=4, fs=14)
    F.label((46, 45), "Station Road", (1, 0), off=6, fs=14)
    F.label((247, 45), "Park Road", (1, 0), off=8, fs=14)
    return F.svg("street map with four roads")


# ------------------------------------------------------------ composite pictures
CELL = 118


def grid_svg(figs, label="four pictures labelled A to D"):
    """2 x 2 grid of Figs labelled A-D. Square picture (printed large)."""
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
    """A row of Figs with a caption under each. items: (Fig, caption)."""
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
    return mcq_fixed(fig(grid_svg(cells, label)) + q, ["A", "B", "C", "D"], "ABCD"[p], "Picture %s %s" % ("ABCD"[p], why))


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


def letter_angles(ch):
    """Sizes of the angles between strokes that meet, inside the letter (less than a straight line)."""
    st = LETTERS[ch]
    out = []
    found = {}
    for i, (a, b) in enumerate(st):
        for j, (c, d) in enumerate(st):
            if j <= i:
                continue
            r, s = sub(b, a), sub(d, c)
            den = r[0] * s[1] - r[1] * s[0]
            if abs(den) < 1e-12:
                continue
            t = ((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0]) / den
            u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
            if -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
                x = (round(a[0] + r[0] * t, 6), round(a[1] + r[1] * t, 6))
                found.setdefault(x, set()).update([i, j])
    for x, idx in found.items():
        dirs = []
        for i in idx:
            for p in st[i]:
                if math.hypot(p[0] - x[0], p[1] - x[1]) > 1e-6:
                    dirs.append(math.degrees(math.atan2(p[1] - x[1], p[0] - x[0])) % 360)
        dirs.sort()
        for k in range(len(dirs)):
            g = (dirs[(k + 1) % len(dirs)] - dirs[k]) % 360
            if g < 180 - 1e-6:
                out.append(round(g, 6))
    return out


def letter_rights(ch):
    return sum(1 for g in letter_angles(ch) if abs(g - 90) < 1e-6)


def letter_has_par(ch):
    st = LETTERS[ch]
    return any(dir_diff(sub(st[i][1], st[i][0]), sub(st[j][1], st[j][0])) < 1e-6
               for i in range(len(st)) for j in range(i + 1, len(st)))


def letter_count(ch, kind):
    st = LETTERS[ch]
    return sum(1 for a, b in st if (a[1] == b[1] if kind == "horizontal" else a[0] == b[0]))


# ------------------------------------------------------------ set 1: turns
def set_turns(rnd, P):
    its = []
    q = "What turn does the arrow show? It starts at the dashed line."
    for frac, cw, ans, e in [
        (0.25, True, "quarter turn", "The arrow goes a quarter of the way round. That is a quarter turn: 1 right angle."),
        (0.5, False, "half turn", "The arrow goes halfway round, so the end line points the opposite way. That is a half turn: 2 right angles."),
        (0.75, True, "three-quarter turn", "The arrow goes three quarters of the way round. That is a three-quarter turn: 3 right angles."),
        (1.0, True, "whole turn", "The arrow goes all the way round, back to the dashed line. That is a whole turn: 4 right angles."),
    ]:
        its.append(mcq_fixed(fig(turn_fig(frac, cw).svg(ans + (" clockwise" if cw else " anticlockwise"))) + q, TURNS, ans, e))
    DIRS = ["quarter turn clockwise", "quarter turn anticlockwise", "three-quarter turn clockwise", "three-quarter turn anticlockwise"]
    q = "Which turn does the arrow show? It starts at the dashed line."
    for frac, cw, e in [
        (0.25, False, "The arrow goes a quarter of the way round, the opposite way to clock hands. That is anticlockwise."),
        (0.75, True, "The arrow goes three quarters of the way round, the same way as clock hands. That is clockwise."),
        (0.25, True, "The arrow goes a quarter of the way round, the same way as clock hands. That is clockwise."),
        (0.75, False, "The arrow goes three quarters of the way round, the opposite way to clock hands. That is anticlockwise."),
    ]:
        name = ("quarter" if frac == 0.25 else "three-quarter") + " turn " + ("clockwise" if cw else "anticlockwise")
        its.append(mcq_fixed(fig(turn_fig(frac, cw).svg(name)) + q, DIRS, name, e))
    its.append(mcq("Which way do the hands on a clock turn?", "clockwise",
                   ["anticlockwise", "both ways", "they turn upside down"],
                   "Clock hands always turn the same way: clockwise. Anticlockwise is the opposite way.", rnd))
    for n, wrong, e in [(1, [2, 3, 4], "A quarter turn is 1 right angle."),
                        (2, [1, 3, 4], "A half turn is 2 right angles: 1 right angle + 1 right angle."),
                        (3, [1, 2, 4], "A three-quarter turn is 3 right angles: three quarter turns."),
                        (4, [1, 2, 3], "A whole turn is 4 right angles: four quarter turns take you all the way round.")]:
        t = {1: "a quarter turn", 2: "a half turn", 3: "a three-quarter turn", 4: "a whole turn"}[n]
        its.append(mcq_num("How many right angles make %s?" % t, n, wrong, e))
    its.append(mcq("Which turn takes you back to where you started?", "a whole turn",
                   ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "A whole turn goes all the way round (4 right angles), so you face the same way again.", rnd))
    q2 = "%s faces %s. %s makes a %s %s. Which way does %s face now?"
    for start, frac, cw in [(0, 0.25, True), (0, 0.25, False), (2, 0.25, True), (1, 0.75, True)]:
        n, he, his = P.next()
        k = int(frac * 4)
        end = (start + (k if cw else -k)) % 4
        turn = {1: "quarter turn", 2: "half turn", 3: "three-quarter turn"}[k]
        cwa = "clockwise" if cw else "anticlockwise"
        e = ("A quarter turn %s goes from %s to %s." % (cwa, POINTS[start], POINTS[end]) if k == 1 else
             "Count the quarter turns clockwise: %s." % ", ".join(POINTS[(start + i) % 4] for i in range(k + 1)))
        e += " Clockwise goes N, E, S, W." if cw else " Anticlockwise goes N, W, S, E."
        its.append(mcq_fixed(fig(compass_svg(start)) + q2 % (n, POINTS[start], he.capitalize(), turn, cwa, he),
                             POINTS, POINTS[end], e))
    room = ["door", "window", "board", "bookcase"]
    for start, k, cw in [(0, 2, True), (1, 1, False)]:
        n, he, his = P.next()
        end = (start + (k if cw else -k)) % 4
        F = facing_fig(room, start, fs=16, R=50)
        turn = "half turn" if k == 2 else "quarter turn anticlockwise"
        e = ("A half turn makes you face the opposite way. The %s is opposite the %s." % (room[end], room[start]) if k == 2 else
             "Anticlockwise is the opposite way to clock hands. A quarter turn anticlockwise from the %s is the %s." % (room[start], room[end]))
        its.append(mcq_fixed(fig(F.svg("pupil in a classroom facing the " + room[start])) +
                             "%s faces the %s. %s makes a %s. What does %s face now?" % (n, room[start], he.capitalize(), turn, he),
                             ["the " + r for r in room], "the " + room[end], e))
    assert len(its) == 20, len(its)
    return {"title": "Quarter, half, three-quarter and whole turns", "items": its}


# ------------------------------------------------------------ set 2: right angles in shapes and around us
def set_rights(rnd, P):
    its = []
    pos = Pos(rnd)
    lab = "four angles labelled A to D"
    its.append(mcq(fig(angle_fig(90, 20, 64, marked=True).svg("right angle with a small square")) +
                   "What does the small square in the corner show?", "a right angle",
                   ["a square shape", "a small angle", "a half turn"],
                   "A small square in a corner shows a right angle: a square corner, like the corner of a page.", rnd))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, 30, 56), angle_fig(60, 10, 64), angle_fig(120, 20, 50), angle_fig(65, 100, 64)],
                         "makes a square corner. It is turned, but it is still a right angle. Check with the corner of a piece of paper.", pos, lab))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, -20, 40), angle_fig(115, 0, 62), angle_fig(45, 20, 66), angle_fig(150, 15, 44)],
                         "makes a square corner. Its arms are short, but arm length does not change an angle.", pos, lab))
    q = "How many right angles does this shape have?"
    shapes = [
        (SQ, 45, 4, [0, 2, 1], "square", "A square has 4 right angles. It is turned, but turning does not change the angles."),
        (RTRI, 0, 1, [0, 3, 2], "right-angled triangle", "Only the bottom-left corner is a square corner. The other 2 corners are smaller."),
        (EQUI, 0, 0, [3, 1, 2], "triangle", "All 3 corners are smaller than a right angle, so there are no right angles."),
        (LSHAPE, 0, 5, [6, 4, 3], "L-shape", "5 corners are square corners. The corner that points inwards is bigger than a right angle, so do not count it."),
        (HOUSE, 0, 3, [5, 2, 4], "house shape", "The 2 bottom corners and the top of the roof are right angles. The 2 corners where the roof meets the walls are bigger."),
        (RTRAP, 0, 2, [4, 1, 0], "shape with 4 sides", "The 2 corners on the left are right angles. The 2 corners on the right are not."),
        (HEX, 0, 0, [6, 2, 1], "hexagon", "This shape has 6 corners, but they are all bigger than a right angle. So there are no right angles."),
        (CUT, 0, 3, [5, 4, 2], "rectangle with one corner cut off", "3 corners are still square corners. Cutting off a corner makes 2 corners that are bigger than a right angle."),
        (TSHAPE, 0, 6, [8, 4, 5], "T-shape", "6 corners are square corners. The 2 corners that point inwards are bigger than a right angle."),
        (PARA, 0, 0, [4, 2, 1], "slanted shape with 4 sides", "The shape leans over. 2 corners are smaller and 2 are bigger than a right angle, so there are no right angles."),
    ]
    for pts, rot, ans, wrong, name, e in shapes:
        assert len(rights(placed(pts, rot, 120, 76))) == ans, name
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label=name)) + q, ans, wrong, e))
    for ch, wrong, e in [("L", [0, 2, 3], "Where the 2 lines of L meet, the inside corner is 1 right angle."),
                         ("T", [0, 1, 4], "Where the top line meets the stem, there is a right angle on each side. That is 2 right angles.")]:
        n = letter_rights(ch)
        its.append(mcq_num(fig(letters_svg([ch], "capital letter " + ch)) + "How many right angles are inside the capital letter %s?" % ch,
                           n, wrong, e))
    its.append(mcq("Which of these usually has 4 right angles?", "a door",
                   ["a slice of pizza", "a coat hanger", "a triangular road sign"],
                   "A door is a rectangle, so it has 4 square corners. A pizza slice and a road sign have pointed corners.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a piece of paper in half, then in half again. What does the folded corner make?" % n,
                   "a right angle", ["a straight line", "a half turn", "an angle greater than a right angle"],
                   "Folding once makes a straight edge. Folding that edge in half again makes a right angle. This is a right-angle checker.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(shape_svg(RECT, 25, 120, 76, label="turned rectangle")) +
                   "%s says this shape has no right angles because it is turned. Is %s right?" % (n, he),
                   "No, it still has 4 right angles", ["Yes, it has no right angles", "No, it has 2 right angles", "Yes, turned shapes have no corners"],
                   "It is a rectangle that has been turned. Turning a shape does not change its angles, so it still has 4 right angles.", rnd))
    lab = "four shapes labelled A to D"
    g = dict(bw=74, bh=70, sw=2.6)
    its.append(pick_grid("Which shape has exactly 1 right angle?",
                         [shape_fig(RTRI2, 200, **g), shape_fig(RECT2, 0, 76, 50, sw=2.6), shape_fig(EQUI, 0, **g), shape_fig(RTRAP, 0, **g)],
                         "is a triangle with one square corner. The rectangle has 4, the other triangle has none and the 4-sided shape has 2.", pos, lab))
    its.append(pick_grid("Which shape has no right angles?",
                         [shape_fig(PARA, 0, 80, 50, sw=2.6), shape_fig(SQ, 45, **g), shape_fig(RTRI, 0, **g), shape_fig(LSHAPE, 0, **g)],
                         "leans over, so none of its corners are square corners. The turned square, the triangle and the L-shape all have right angles.", pos, lab))
    assert len(its) == 20, len(its)
    return {"title": "Right angles in shapes and around us", "items": its}


# ------------------------------------------------------------ set 3: greater or less than a right angle
def set_compare(rnd, P):
    its = []
    pos = Pos(rnd)
    q = "Is this angle less than a right angle, a right angle or greater than a right angle?"
    for deg, rot, L, L2 in [(40, 10, 80, 80), (120, 30, 60, 60), (90, 40, 70, 70), (60, 200, 50, 70), (150, -20, 60, 60),
                            (90, -120, 50, 80), (30, 100, 70, 70), (110, 190, 76, 76), (180, 20, 56, 56), (65, -40, 46, 46)]:
        k = cmp_word(deg)
        e = {"less than a right angle": "The angle is narrower than a square corner, so it is less than a right angle.",
             "a right angle": "The arms make a square corner, so it is a right angle. Turning an angle does not change it.",
             "greater than a right angle": "The angle opens wider than a square corner, so it is greater than a right angle.",
             "a straight line": "The arms point in opposite directions and make a straight line: 2 right angles (a half turn)."}[k]
        its.append(mcq_fixed(fig(angle_fig(deg, rot, L, L2).svg("angle")) + q, CMP, k, e))
    lab = "four angles labelled A to D"
    its.append(pick_grid("Which angle is greater than a right angle?",
                         [angle_fig(125, 20, 42), angle_fig(50, 10, 76), angle_fig(90, 0, 60), angle_fig(30, 60, 76)],
                         "opens wider than a square corner. Its arms are short, but that does not make it small.", pos, lab))
    its.append(pick_grid("Which angle is less than a right angle?",
                         [angle_fig(45, 100, 50), angle_fig(130, 0, 50), angle_fig(90, 200, 62), angle_fig(110, 60, 56)],
                         "is narrower than a square corner. The others are a right angle or wider.", pos, lab))
    its.append(mcq_fixed(fig(shape_svg(OBTRI, 0, 140, 64, label="triangle ABC", vlabels="ACB")) +
                         "Which angle in this triangle is greater than a right angle?",
                         ["angle A", "angle B", "angle C", "none of them"], "angle B",
                         "Angle B, at the top, opens wider than a square corner. Angles A and C are narrow: less than a right angle."))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(130, 25, 34).svg("wide angle with short arms")) +
                   "%s says this angle is less than a right angle because its arms are short. Is %s right?" % (n, he),
                   "No, it is greater than a right angle", ["Yes, short arms make a small angle", "No, it is a right angle", "Yes, it is a small turn"],
                   "The size of an angle is how wide it opens, not how long its arms are. This angle opens wider than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(50, 15, 82).svg("narrow angle with long arms")) +
                   "%s says this angle is greater than a right angle because its arms are long. Is %s right?" % (n, he),
                   "No, it is less than a right angle", ["Yes, long arms make a big angle", "No, it is a right angle", "Yes, it is a straight line"],
                   "Long arms do not make an angle bigger. This angle is narrower than a square corner, so it is less than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into an angle. The angle is wider than the checker. What is the angle?" % (n, his),
                   "greater than a right angle", ["less than a right angle", "a right angle", "a whole turn"],
                   "The checker is a right angle. If the angle is wider than the checker, it is greater than a right angle.", rnd))
    its.append(mcq("An angle that is less than a right angle has a special name. What is it?", "acute",
                   ["obtuse", "straight", "square"],
                   "An angle less than a right angle is called acute. You will use this word a lot in Year 4.", rnd))
    its.append(mcq("An angle that is greater than a right angle (but less than a straight line) has a special name. What is it?", "obtuse",
                   ["acute", "square", "perpendicular"],
                   "An angle greater than a right angle but less than a straight line is called obtuse.", rnd))
    pair = strip_svg([(angle_fig(50, 20, 82), "P"), (angle_fig(120, 10, 38), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Which angle is greater?", "angle Q",
                   ["angle P", "They are the same size", "You cannot tell"],
                   "Angle Q opens wider than a right angle, and angle P is less than a right angle. So Q is greater, even though P has longer arms.", rnd))
    its.append(mcq_num("A straight line is the same as how many right angles?", 2, [1, 3, 4],
                       "A straight line is a half turn, and a half turn is 2 right angles."))
    assert len(its) == 20, len(its)
    return {"title": "Greater or less than a right angle", "items": its}


# ------------------------------------------------------------ set 4: horizontal, vertical, parallel, perpendicular
def set_lines(rnd, P):
    its = []
    pos = Pos(rnd)
    lab = "four lines labelled A to D"
    its.append(pick_grid("Which line is vertical?",
                         [lines_fig("one", 90), lines_fig("one", 0), lines_fig("one", 65), lines_fig("one", 30)],
                         "goes straight up and down, like a flagpole. That is a vertical line. The line going straight across is horizontal.", pos, lab))
    its.append(pick_grid("Which line is horizontal?",
                         [lines_fig("one", 0), lines_fig("one", 90), lines_fig("one", 20), lines_fig("one", 135)],
                         "goes straight across, like the horizon. That is a horizontal line. The line going straight up and down is vertical.", pos, lab))
    its.append(mcq("A flagpole stands straight up and down. What kind of line does it make?", "vertical",
                   ["horizontal", "parallel", "slanting"],
                   "Straight up and down is vertical. Horizontal lines go straight across, like the horizon.", rnd))
    its.append(mcq("The line where the sea meets the sky goes straight across. What kind of line is it?", "horizontal",
                   ["vertical", "perpendicular", "slanting"],
                   "A line that goes straight across is horizontal. The word comes from horizon, where the sea meets the sky.", rnd))
    n = letter_count("H", "vertical")
    its.append(mcq_num(fig(letters_svg(["H"], "capital letter H")) + "How many vertical lines are in the capital letter H?", n, [1, 3, 0],
                       "The 2 sides of H go straight up and down, so they are vertical. The middle line goes across: it is horizontal."))
    n = letter_count("E", "horizontal")
    its.append(mcq_num(fig(letters_svg(["E"], "capital letter E")) + "How many horizontal lines are in the capital letter E?", n, [1, 2, 4],
                       "The top, middle and bottom lines of E go straight across: 3 horizontal lines. The line on the left is vertical."))
    lab = "four pairs of lines labelled A to D"
    its.append(pick_grid("Which pair of lines is parallel?",
                         [lines_fig("par", 0, 70), lines_fig("perp", 0, 70), lines_fig("meet", 0, 70), lines_fig("cross", 10, 70)],
                         "shows lines that stay the same distance apart all the way along, so they will never meet. The lines that get closer would meet if they were longer.", pos, lab))
    its.append(pick_grid("Which pair of lines is parallel?",
                         [lines_fig("par", 60, 70), lines_fig("meet", 90, 70), lines_fig("cross", 100, 70), lines_fig("perpT", 30, 70)],
                         "shows lines that stay the same distance apart, even though they slant. Parallel lines do not have to be horizontal or vertical.", pos, lab))
    its.append(pick_grid("Which pair of lines is perpendicular?",
                         [lines_fig("perp", 0, 70), lines_fig("par", 90, 70), lines_fig("cross", 0, 70), lines_fig("meet", 30, 70)],
                         "shows lines that meet at a right angle (a square corner). The other crossing lines meet at a slant, not at a right angle.", pos, lab))
    its.append(pick_grid("Which pair of lines is perpendicular?",
                         [lines_fig("perpT", 25, 70), lines_fig("cross", 120, 70), lines_fig("par", 0, 70), lines_fig("meet", 120, 70)],
                         "shows lines that meet at a right angle: they make square corners. They are turned, but the angle is still a right angle.", pos, lab))
    its.append(mcq("What are parallel lines?", "lines that stay the same distance apart and never meet",
                   ["lines that meet at a right angle", "lines that go straight up and down", "lines that cross in the middle"],
                   "Parallel lines always stay the same distance apart, like railway tracks. They never meet, however long they are.", rnd))
    its.append(mcq("What are perpendicular lines?", "lines that meet at a right angle",
                   ["lines that never meet", "lines that go straight across", "lines that meet at any angle"],
                   "Perpendicular lines meet or cross at a right angle. The corner of a page has two perpendicular edges.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(lines_fig("meet", 0, 120).svg("two lines getting closer")) +
                   "%s says these lines are parallel because they do not touch. Is %s right?" % (n, he),
                   "No, they get closer and would meet", ["Yes, lines that do not touch are parallel", "No, they are perpendicular", "Yes, they are both horizontal"],
                   "The gap on the left is bigger than the gap on the right. If the lines were longer, they would meet. Parallel lines stay the same distance apart.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(lines_fig("par", 90, 80).svg("two vertical lines")) +
                   "%s says these lines cannot be parallel because they are not horizontal. Is %s right?" % (n, he),
                   "No, parallel lines can go any way", ["Yes, parallel lines must be horizontal", "No, they are perpendicular", "Yes, they will meet"],
                   "These vertical lines stay the same distance apart, so they are parallel. Parallel lines can be horizontal, vertical or slanting.", rnd))
    for want, row, test, why in [
        ("a pair of parallel lines", ["H", "L", "T", "V"], letter_has_par,
         "The 2 upright lines of H are parallel. L, T and V have no lines going the same way."),
        ("lines that are perpendicular", ["L", "V", "X", "N"], lambda c: letter_rights(c) > 0,
         "The 2 lines of L meet at a right angle. The lines in V, X and N meet at a slant."),
    ]:
        assert [test(c) for c in row] == [True, False, False, False], row
        p = pos.next()
        r = row[1:]
        r.insert(p, row[0])
        its.append(mcq_fixed(fig(letters_svg(r)) + "Which capital letter has %s?" % want, r, row[0], why))
    its.append(mcq_num(fig(shape_svg(RECT, 0, 130, 70, label="rectangle")) + "How many pairs of parallel sides does this rectangle have?",
                       2, [1, 4, 0],
                       "The top and bottom sides are parallel, and the left and right sides are parallel. That is 2 pairs (4 is the number of sides)."))
    its.append(mcq(fig(shape_svg(RTRI, 0, 130, 76, label="right-angled triangle ABC", vlabels="ABC")) +
                   "Which two sides of this triangle are perpendicular?", "AB and AC",
                   ["AB and BC", "AC and BC", "none of them"],
                   "Sides AB and AC meet at corner A, which is a right angle. So AB and AC are perpendicular.", rnd))
    its.append(mcq("A horizontal line and a vertical line meet. What are they?", "perpendicular",
                   ["parallel", "both horizontal", "a straight line"],
                   "A horizontal line and a vertical line meet at a right angle, so they are perpendicular.", rnd))
    its.append(mcq("What can you say about the two rails of a railway track?", "They are parallel",
                   ["They are perpendicular", "They meet far away", "They are vertical"],
                   "The rails stay the same distance apart so the train can run on them. They look like they meet far away, but they never do: they are parallel.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Horizontal, vertical, parallel and perpendicular lines", "items": its}


# ------------------------------------------------------------ set 5: real-life problems
def set_problems(rnd, P):
    its = []
    pos = Pos(rnd)
    q = "The minute hand turns clockwise from the dashed line to where it is now. What turn has it made?"
    for start, k, e in [(12, 1, "From 12 to 3 is a quarter of the way round the clock: a quarter turn."),
                        (3, 2, "From 3 to 9 is halfway round the clock: a half turn."),
                        (6, 3, "From 6 round to 3 is 6 to 9, 9 to 12 and 12 to 3: 3 quarter turns. That is a three-quarter turn."),
                        (9, 4, "The hand goes all the way round from 9 back to 9: a whole turn.")]:
        its.append(mcq_fixed(fig(clock_turn_svg(start % 12, k)) + q, TURNS, TURNS[k - 1], e))
    its.append(mcq("How many minutes does the minute hand take to make a quarter turn?", "15 minutes",
                   ["30 minutes", "45 minutes", "60 minutes"],
                   "A whole turn of the minute hand takes 60 minutes. A quarter of 60 is 15, so a quarter turn takes 15 minutes.", rnd))
    its.append(mcq("It is 2:00 pm. The minute hand makes a half turn. What time is it now?", "2:30 pm",
                   ["2:15 pm", "2:45 pm", "3:00 pm"],
                   "A half turn of the minute hand is 30 minutes. 30 minutes after 2:00 pm is 2:30 pm.", rnd))
    for h, e in [(3, "At 3 o’clock the hands make a square corner: a right angle."),
                 (5, "At 5 o’clock the hands are 5 hour marks apart. A right angle is only 3 hour marks, so this angle is greater."),
                 (1, "At 1 o’clock the hands are only 1 hour mark apart. That is narrower than a right angle (3 hour marks).")]:
        its.append(mcq_fixed(fig(clock_svg(h)) + "What angle do the hands make?", CMP, cmp_word(30 * min(h, 12 - h)), e))
    n, he, his = P.next()
    its.append(mcq_fixed("%s walks north. %s turns right. Which way is %s walking now?" % (n, he.capitalize(), he), POINTS, "east",
                         "Turning right is a quarter turn clockwise. A quarter turn clockwise from north is east."))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(1)) + "%s faces east. %s makes a half turn. Which way does %s face now?" % (n, he.capitalize(), he),
                         POINTS, "west", "A half turn makes you face the opposite way. West is opposite east."))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(2)) + "%s faces south. %s makes a quarter turn anticlockwise. Which way does %s face now?" % (n, he.capitalize(), he),
                         POINTS, "east", "Anticlockwise goes S, E, N, W. A quarter turn anticlockwise from south is east."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s faces west. %s makes a three-quarter turn clockwise. Which way does %s face now?" % (n, he.capitalize(), he),
                         POINTS, "south", "Count 3 quarter turns clockwise from west: north, east, south."))
    m = street_map_svg()
    its.append(mcq(fig(m) + "Which road is parallel to High Street?", "Mill Lane",
                   ["Station Road", "Park Road", "none of them"],
                   "Mill Lane goes across the map, the same way as High Street, and they stay the same distance apart. So they are parallel.", rnd))
    its.append(mcq(fig(m) + "Which road is perpendicular to High Street?", "Station Road",
                   ["Mill Lane", "Park Road", "none of them"],
                   "Station Road goes up and down the map and meets High Street at a right angle. Park Road crosses at a slant, not at a right angle.", rnd))
    its.append(pick_grid("At which junction do the roads meet at a right angle?",
                         [junction_fig("T", 20), junction_fig("Y", 0), junction_fig("skew", 0), junction_fig("slant", 0)],
                         "has a side road that meets the main road at a square corner. The other roads meet at a slant.", pos,
                         "four road junctions labelled A to D"))
    n, he, his = P.next()
    its.append(mcq("%s opens a door until it makes a square corner with the wall. What turn has the door made?" % n,
                   "a quarter turn", ["a half turn", "a three-quarter turn", "a whole turn"],
                   "A square corner is a right angle, and a right angle is a quarter turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s spins round in the playground until %s faces the same way again. What turn has %s made?" % (n, he, he),
                   "a whole turn", ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "Facing the same way again means going all the way round: a whole turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s faces the board. %s turns clockwise through 3 right angles. What turn is that?" % (n, he.capitalize()),
                   "a three-quarter turn", ["a half turn", "a quarter turn", "a whole turn"],
                   "Each right angle is a quarter turn. 3 quarter turns make a three-quarter turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a quarter turn clockwise, then another quarter turn clockwise. What turn is that altogether?" % n,
                   "a half turn", ["a quarter turn", "a whole turn", "a three-quarter turn"],
                   "2 quarter turns make a half turn: 2 right angles.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Clocks, compass turns and roads", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    turns = strip_svg([(turn_fig(f), t) for t, f in (("quarter", 0.25), ("half", 0.5), ("three-quarter", 0.75), ("whole", 1.0))],
                      cw=124, label="quarter, half, three-quarter and whole turns clockwise")
    comp = compass_svg(0, "compass points north, east, south and west")
    kinds = strip_svg([(angle_fig(45, 10, 66), "less than"), (angle_fig(90, 0, 60, marked=True), "right angle"),
                       (angle_fig(130, 10, 54), "greater than")],
                      cw=130, label="angle less than a right angle, a right angle and an angle greater than a right angle")
    same = strip_svg([(angle_fig(55, 10, 86), "long arms"), (angle_fig(55, 10, 36), "short arms")], cw=128,
                     label="two angles of the same size with long and short arms")
    shapes = strip_svg([(shape_fig(RECT, 0, 96, 56, sw=2.8, marks=True), "4 right angles"),
                        (shape_fig(RTRI, 0, 96, 60, sw=2.8, marks=True), "1 right angle"),
                        (shape_fig(LSHAPE, 0, 80, 70, sw=2.8, marks=True), "5 right angles")],
                       cw=130, label="rectangle, right-angled triangle and L-shape with their right angles marked")
    lines = strip_svg([(lines_fig("one", 0, 70), "horizontal"), (lines_fig("one", 90, 70), "vertical"),
                       (lines_fig("par", 30, 70), "parallel"), (lines_fig("perp", 0, 70), "perpendicular")],
                      cw=124, label="horizontal, vertical, parallel and perpendicular lines")
    return (
        "<h2>Angles are turns</h2>"
        "<p>An angle shows a <b>turn</b>. A quarter turn is a <b>right angle</b>. "
        "Clock hands turn <b>clockwise</b>. The other way is <b>anticlockwise</b>.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Each turn starts at the dashed line and goes clockwise.</figcaption></figure>" +
        table(["Turn", "Right angles"], [
            ["Quarter turn", "1"], ["Half turn", "2"], ["Three-quarter turn", "3"], ["Whole turn", "4 (back to the start)"],
        ]) +
        "<figure class='sn-fig'>" + comp +
        "<figcaption>Clockwise from north: north, east, south, west.</figcaption></figure>" +
        ex("Example", "Amelia faces north. She makes a quarter turn clockwise. Which way does she face now?",
           "Clockwise goes north, east, south, west. One quarter turn from north is east.", "east") +
        "<h2>Right angles</h2>"
        "<p>A right angle is a <b>square corner</b>, like the corner of a page. It is 90°. "
        "A small square in a corner shows a right angle.</p>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>Do not count a corner that points inwards: it is bigger than a right angle.</figcaption></figure>"
        "<p>Make a <b>right-angle checker</b>: fold a piece of paper in half, then in half again.</p>"
        "<h2>Greater or less than a right angle</h2>"
        "<p>Put your checker in the angle. If the angle is narrower, it is <b>less than</b> a right angle (acute). "
        "If it is wider, it is <b>greater than</b> a right angle (obtuse).</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>"
        "<figure class='sn-fig'>" + same +
        "<figcaption>These two angles are the same size. Longer arms do not make an angle bigger.</figcaption></figure>"
        "<h2>Lines</h2>"
        "<p><b>Horizontal</b> lines go straight across, like the horizon. <b>Vertical</b> lines go straight up and down. "
        "<b>Parallel</b> lines stay the same distance apart and never meet. "
        "<b>Perpendicular</b> lines meet at a right angle.</p>"
        "<figure class='sn-fig'>" + lines + "</figure>" +
        ex("Example", "How many pairs of parallel sides does a rectangle have?",
           "The top and bottom are parallel. The left and right sides are parallel.", "2 pairs") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at how wide the angle opens"],
            ["Mixing up horizontal and vertical", "Horizontal is like the horizon: straight across"],
            ["Mixing up clockwise and anticlockwise", "Clockwise is the way clock hands go"],
            ["Saying lines are parallel because they do not touch yet", "Parallel lines stay the same distance apart"],
            ["Saying a turned shape has no right angles", "Turning a shape does not change its angles"],
        ])
    )


FAQ = [
    {"q": "What do Year 3 children learn about angles?",
     "a": "They learn that an angle is a turn, find right angles in shapes, and say whether an angle is greater or less than a right angle. Two right angles make a half turn and four make a whole turn."},
    {"q": "How do you explain a right angle to a Year 3 child?",
     "a": "A right angle is a square corner, like the corner of a book. Fold a piece of paper in half and in half again to make a right-angle checker."},
    {"q": "What is the difference between parallel and perpendicular lines?",
     "a": "Parallel lines stay the same distance apart and never meet, like railway tracks. Perpendicular lines meet at a right angle, like the corner of a page."},
    {"q": "Do Year 3 children need to know acute and obtuse angles?",
     "a": "In Year 3 they say whether an angle is less than or greater than a right angle. The names acute and obtuse are part of the Year 4 curriculum, but many teachers start using them now."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order
    (A-D pictures, turns, compass points, numbers) stay as they are; the other questions fill the gaps."""
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
    rnd = random.Random(3312)
    P = People(rnd)
    sets = [set_turns(rnd, P), set_rights(rnd, P), set_compare(rnd, P), set_lines(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "angles-and-lines", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles and Lines: Turns, Right Angles, Parallel and Perpendicular Lines",
        "seo_title": "Year 3 Angles Worksheets: Turns, Right Angles, Horizontal, Vertical, Parallel and Perpendicular Lines",
        "short_title": "Angles and lines",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 3: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise angles as a property of shape or a description of a turn; identify right angles, recognise that two right angles make a half-turn, three make three quarters of a turn and four a complete turn; identify whether angles are greater than or less than a right angle; identify horizontal and vertical lines and pairs of perpendicular and parallel lines.",
        "meta_desc": "Free Year 3 maths worksheets on angles and lines: quarter, half, three-quarter and whole turns, clockwise and anticlockwise, right angles in shapes, angles greater or less than a right angle, and horizontal, vertical, parallel and perpendicular lines. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "A right angle is a quarter turn: a square corner. Two make a half turn, three a three-quarter turn and four a whole turn.",
        "key_sub": "Compare every angle with a right angle: narrower is less, wider is greater. Arm length does not change an angle. Parallel lines never meet; perpendicular lines meet at a right angle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, rows of figures, the map) so they stay readable."""
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
        mark_large(u, "(four [a-z ]+ labelled A to D|angle P and angle Q|capital letters made|street map)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
