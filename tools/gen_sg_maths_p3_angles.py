# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Angles (MOE 2021 Primary Mathematics Syllabus, Standard - Geometry)
  python3 tools/gen_sg_maths_p3_angles.py
Concepts of angle (two straight arms meeting at a vertex), right angles in shapes and objects,
angles greater than or smaller than a right angle, counting angles in shapes, turns and clock hands.
No degrees (that is P4). Every drawing is exact and checked in code: right angles are true right
angles, any angle that is not a right angle is at least 20 degrees away from one, and no label touches
a line. Pictures where students must judge an angle have NO right-angle marks.
Singapore style: British spelling, Singapore names, 12-hour times with a dot. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#1f4e79"
FILL = "#cfe0f1"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
RED = "#c8102e"
WOOD = "#e6d3b3"
GLASS = "#dcecf5"
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

    def poly(self, pts, fill=FILL, w=3, col=GREEN):
        P = " ".join("%.1f,%.1f" % p for p in pts)
        self.el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                       % (P, fill, col, w))
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

    def text(self, c, t, fs=16, col=INK):
        """Text centred at c that is meant to sit inside a shape (not checked against strokes)."""
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (c[0], c[1] + fs * 0.36, fs, col, t))

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


# ------------------------------------------------------------ turns, compass, clocks
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


TURNS = ["quarter turn", "half turn", "three-quarter turn", "full turn"]
POINTS = ["north", "east", "south", "west"]


def facing_fig(names, face, fs=16, R=50):
    """A student (circle) in the middle with an arrow to the way they face; names on the 4 sides
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
    return facing_fig(["N", "E", "S", "W"], face, fs=18, R=48).svg(label or "student facing %s" % POINTS[face])


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
    """Analog clock at h o'clock. Square picture (printed large)."""
    c = (56.0, 56.0)
    s = []
    clock_face(s, c)
    hd, md = dirv(90 - 30 * (h % 12)), dirv(90)
    hh, mh = add(c, hd, 17), add(c, md, 25)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(112, 112, "".join(s), "analog clock showing %d o’clock" % h)


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
    return svg_wrap(112, 112, "".join(s), "analog clock with the minute hand turning")

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


def pick_grid(q, figs, why, p, label="four pictures labelled A to D"):
    """figs[0] is the right answer. It goes to position p; the others keep their order."""
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
        if ch == "O":
            c = (k * cw + cw / 2.0, 36.0)
            F.mark([(c[0] + 21 * math.cos(math.pi * i / 24), c[1] + 30 * math.sin(math.pi * i / 24)) for i in range(49)], w=6, col=GREEN)
            continue
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


# ------------------------------------------------------------ everyday objects
def rect_pts(w, h):
    return [(0.0, 0.0), (float(w), 0.0), (float(w), float(h)), (0.0, float(h))]


def corner_marks(F, pts, k=9):
    for i in rights(pts):
        v = pts[i]
        F.right_mark(v, norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % len(pts)], v)), k)


def closed(F, pts, w=2, col=GREEN):
    F.mark(pts + [pts[0]], w=w, col=col)


def book_fig(marks=False):
    F = Fig()
    pts = rect_pts(62, 82)
    F.poly(pts, fill=FILL, w=3)
    F.line((12, 0), (12, 82), w=2.4)
    F.line((24, 20), (52, 20), w=3, col=INK)
    F.line((24, 31), (46, 31), w=3, col=INK)
    if marks:
        corner_marks(F, pts)
    return F


def door_fig(marks=False):
    F = Fig()
    pts = rect_pts(52, 96)
    F.poly(pts, fill=WOOD, w=3)
    closed(F, [(12, 13), (36, 13), (36, 43), (12, 43)])
    closed(F, [(12, 54), (36, 54), (36, 83), (12, 83)])
    F.dot((44, 50), 3.4)
    if marks:
        corner_marks(F, pts)
    return F


def window_fig(marks=False):
    F = Fig()
    pts = rect_pts(84, 66)
    F.poly(pts, fill=GLASS, w=3)
    F.line((42, 0), (42, 66), w=3, cap="butt")
    F.line((0, 33), (84, 33), w=3, cap="butt")
    if marks:
        corner_marks(F, pts)
    return F


def pizza_fig():
    """A slice of pizza: the tip is a 30 degree angle, the crust is curved."""
    F = Fig()
    tip = (0.0, 76.0)
    arc = [add(tip, dirv(75 + 2 * i), 76) for i in range(16)]
    F.poly([tip] + arc, fill="#f3d27a", w=2.5, col="#b8862e")
    F.mark(arc, w=7, col="#c8955a")
    for p in ((0, 46), (-6, 22), (7, 28)):
        F.dot(p, 4.2, RED)
    return F


def hanger_fig():
    F = Fig()
    F.poly([(-42.0, 38.0), (42.0, 38.0), (0.0, 8.0)], fill="none", w=3, col=INK)
    c = (7.0, -6.0)
    F.mark([(0.0, 8.0), (0.0, -6.0)] + [add(c, dirv(180 - 10 * i), 7) for i in range(23)], w=3, col=INK)
    return F


def giveway_fig():
    F = Fig()
    F.poly([(-42.0, 0.0), (42.0, 0.0), (0.0, 42 * math.sqrt(3))], fill="#ffffff", w=7, col=RED)
    return F


def stop_fig():
    F = Fig()
    F.poly([add((0, 0), dirv(22.5 + 45 * i), 42) for i in range(8)], fill=RED, w=2, col=RED)
    F.text((0, 0), "STOP", fs=17, col="#ffffff")
    return F


RAMP = [(0, 60), (104, 60), (104, 0)]          # A: front (on the ground), B: back corner, C: top


def ramp_svg():
    return shape_svg(RAMP, 0, 140, 70, label="skateboard ramp with corners A, B and C", vlabels="ABC")


PENT = [add((0, 0), dirv(60 * i), 60) for i in range(1, 6)]        # hexagon with one corner cut off: 5 angles
CMP = ["smaller than a right angle", "a right angle", "greater than a right angle", "you cannot tell"]


def cmp_word(deg):
    assert deg < 180
    return "smaller than a right angle" if deg < 90 else "a right angle" if deg == 90 else "greater than a right angle"


# ------------------------------------------------------------ set 1 pictures
def named_angle_svg(deg, rot, L, names, label="angle with four points labelled A to D"):
    """names = (end of arm 1, vertex, end of arm 2, a point in the middle of arm 1)."""
    F = angle_fig(deg, rot, L)
    V = (0.0, 0.0)
    d1, d2 = dirv(rot), dirv(rot + deg)
    e1, e2, m = add(V, d1, L), add(V, d2, L), add(V, d1, L * 0.55)
    for p in (e1, e2, m):
        F.dot(p, 3.2)
    F.label(V, names[1], (-(d1[0] + d2[0]), -(d1[1] + d2[1])), off=10)
    F.label(e1, names[0], d1, off=8)
    F.label(e2, names[2], d2, off=8)
    nr = (-d1[1], d1[0])
    if nr[0] * d2[0] + nr[1] * d2[1] > 0:
        nr = (-nr[0], -nr[1])
    F.label(m, names[3], nr, off=8)
    return F.svg(label)


def curves_fig():
    """Two curved lines that meet at a point (not an angle: the arms are not straight)."""
    F = Fig()
    for base, bend in ((10, 1), (75, -1)):
        d = dirv(base)
        nr = (-d[1], d[0])
        F.mark([add(add((0.0, 0.0), d, 62 * t / 10.0), nr, bend * 14 * math.sin(math.pi * t / 10.0)) for t in range(11)],
               w=3, col=GREEN)
    F.dot((0.0, 0.0), 3.5)
    return F


def gap_fig():
    """Two straight lines that do not meet."""
    F = Fig()
    F.line(add((0, 0), dirv(15), 16), add((0, 0), dirv(15), 66))
    F.line(add((0, 0), dirv(80), 16), add((0, 0), dirv(80), 66))
    return F


def one_line_fig():
    F = Fig()
    F.line(add((0, 0), dirv(30), -40), add((0, 0), dirv(30), 40))
    return F


def circle_fig(r=40):
    F = Fig()
    F.circle((0.0, 0.0), r)
    return F


def arm_lesson_svg():
    F = angle_fig(55, 10, 110)
    d1, d2 = dirv(10), dirv(65)
    F.label((0.0, 0.0), "vertex", (-(d1[0] + d2[0]), -(d1[1] + d2[1])), off=10, fs=15)
    F.label(add((0, 0), d1, 70), "arm", (-d1[1], d1[0]), off=6, fs=15)
    F.label(add((0, 0), d2, 70), "arm", (d2[1], -d2[0]), off=6, fs=15)
    return F


# ------------------------------------------------------------ set 1: what is an angle
def set_what(rnd, P):
    its = []
    its.append(mcq("Two straight lines meet at a point to make an angle. What is that point called?", "the vertex",
                   ["an arm", "a right angle", "a side"],
                   "The point where the two lines meet is the vertex of the angle.", rnd))
    its.append(mcq("What are the two straight lines of an angle called?", "the arms",
                   ["the vertices", "the turns", "the corners"],
                   "An angle has two arms. They meet at the vertex.", rnd))
    its.append(mcq_num("How many arms does an angle have?", 2, [1, 3, 4], "An angle is made by 2 straight lines, so it has 2 arms."))
    its.append(mcq_num("How many vertices does one angle have?", 1, [0, 2, 3],
                       "The 2 arms meet at just 1 point. So one angle has 1 vertex."))
    q = "Which point is the vertex of the angle?"
    for deg, rot, L, names in [(60, 15, 86, "ABCD"), (110, 200, 80, "CDAB"), (45, 120, 90, "BADC"), (65, -60, 84, "DCBA")]:
        v = names[1]
        its.append(mcq_fixed(fig(named_angle_svg(deg, rot, L, names)) + q, ["A", "B", "C", "D"], v,
                             "%s is where the two arms meet, so %s is the vertex. The other points are on the arms." % (v, v)))
    lab = "four pictures labelled A to D"
    its.append(pick_grid("Which picture shows an angle?",
                         [angle_fig(60, 20, 62), curves_fig(), gap_fig(), one_line_fig()],
                         "", 0, lab))
    its[-1]["e"] = ("Picture A has two straight arms that meet at a point. The others are curved lines, two lines "
                    "that do not meet, or just one line.")
    its.append(pick_grid("Which picture does not show an angle?",
                         [curves_fig(), angle_fig(120, 10, 52), angle_fig(45, 60, 64), angle_fig(65, 190, 60)],
                         "", 2, lab))
    its[-1]["e"] = "Picture C has curved lines. The arms of an angle must be straight lines, so C is not an angle."
    pair = strip_svg([(angle_fig(55, 10, 86), "P"), (angle_fig(55, 10, 36), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Which angle is bigger?", "They are the same size",
                   ["angle P", "angle Q", "You cannot tell"],
                   "Both angles open the same amount. Angle P only has longer arms. Arm length does not change the size of an angle.", rnd))
    pair = strip_svg([(angle_fig(40, 10, 86), "P"), (angle_fig(115, 10, 36), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Which angle is bigger?", "angle Q",
                   ["angle P", "They are the same size", "You cannot tell"],
                   "Angle Q opens wider. Angle P has longer arms, but that does not make it bigger.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws an angle. Then %s makes both arms longer. %s does not move them. What happens to the angle?" % (n, he, he.capitalize()),
                   "It stays the same size", ["It gets bigger", "It gets smaller", "It becomes a right angle"],
                   "The size of an angle is how wide the arms open. Longer arms open the same amount, so the angle stays the same.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens a pair of scissors wider. What happens to the angle between the blades?" % n,
                   "It gets bigger", ["It gets smaller", "It stays the same", "It disappears"],
                   "The blades are like two arms. When they open wider, the angle gets bigger.", rnd))
    its.append(mcq(fig(clock_svg(2)) + "The two hands of this clock make an angle. Where is the vertex?",
                   "at the centre of the clock", ["at the 12", "at the 2", "at the tip of the long hand"],
                   "The hands are the arms. They meet at the centre of the clock, so the vertex is at the centre.", rnd))
    its.append(mcq("Which of these has an angle?", "the corner of a table",
                   ["a round plate", "a ball", "a hula hoop"],
                   "At the corner of a table, two straight edges meet at a point. Round things have no angles.", rnd))
    its.append(mcq_fixed(fig(letters_svg(["L", "V", "O", "N"], "capital letters L, V, O and N")) +
                         "Which capital letter has no angles?", ["L", "V", "O", "N"], "O",
                         "L, V and N are made of straight lines that meet, so they have angles. O is a curve. It has no angles."))
    a, b = P.next(), P.next()
    its.append(mcq("%s says the arms of an angle must be straight lines. %s says the arms can be curved. Who is right?" % (a[0], b[0]),
                   a[0], [b[0], "Both of them", "Neither of them"],
                   "An angle is made by two straight lines that meet at a point. Curved lines do not make an angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens %s laptop. Where is the vertex of the angle between the screen and the keyboard?" % (n, his),
                   "at the hinge", ["at the top of the screen", "at the front of the keyboard", "on the keys"],
                   "The screen and the keyboard are the arms. They meet at the hinge, so the vertex is at the hinge.", rnd))
    its.append(mcq("An angle is made when two straight lines meet at what?", "a point",
                   ["a curve", "a circle", "a right angle"],
                   "Two straight lines that meet at a point make an angle. The point is the vertex.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "What is an angle? Arms and vertex", "items": its}


# ------------------------------------------------------------ set 2: right angles in shapes and objects
def set_rights(rnd, P):
    its = []
    its.append(mcq(fig(angle_fig(90, 20, 64, marked=True).svg("right angle with a small square")) +
                   "What does the small square in the corner show?", "a right angle",
                   ["a square shape", "a small angle", "a straight line"],
                   "A small square in a corner shows a right angle: a square corner, like the corner of a page.", rnd))
    q = "How many right angles does this shape have?"
    shapes = [
        (SQ, 45, 4, [0, 2, 1], "turned square", "A square has 4 right angles. It is turned, but turning does not change the angles."),
        (RTRI, 0, 1, [0, 3, 2], "right-angled triangle", "Only the bottom-left corner is a square corner. The other 2 corners are smaller."),
        (EQUI, 0, 0, [3, 1, 2], "triangle", "All 3 corners are smaller than a right angle, so there are no right angles."),
        (LSHAPE, 0, 5, [6, 4, 3], "L-shape", "5 corners are square corners. The corner that points inwards is greater than a right angle, so do not count it."),
        (HOUSE, 0, 3, [5, 2, 4], "house shape", "The 2 bottom corners and the top of the roof are right angles. The 2 corners where the roof meets the walls are greater."),
        (RTRAP, 0, 2, [4, 1, 0], "shape with 4 sides", "The 2 corners on the left are right angles. The 2 corners on the right are not."),
        (RECT, 30, 4, [0, 2, 3], "turned rectangle", "It is a rectangle that has been turned. It still has 4 square corners: 4 right angles."),
    ]
    for pts, rot, ans, wrong, name, e in shapes:
        assert len(rights(placed(pts, rot, 120, 76))) == ans, name
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label=name)) + q, ans, wrong, e))
    n, he, his = P.next()
    assert len(rights(rect_pts(62, 82))) == 4
    its.append(mcq_num(fig(book_fig().svg("library book")) + "%s checks the corners of %s library book with a right-angle checker. How many corners are right angles?" % (n, his),
                       4, [2, 3, 1], "The front cover is a rectangle. All 4 corners are square corners, so all 4 are right angles."))
    stop = [add((0, 0), dirv(22.5 + 45 * i), 42) for i in range(8)]
    assert rights(stop) == []
    its.append(mcq_num(fig(stop_fig().svg("stop sign")) + "How many right angles does this stop sign have?",
                       0, [8, 4, 1], "A stop sign has 8 corners, but each one is greater than a right angle. So it has no right angles."))
    its.append(mcq_num(fig(window_fig().svg("window with 4 panes of glass")) +
                       "This window of an HDB flat has 4 panes of glass. How many right angles does one pane have?",
                       4, [2, 1, 16], "Each pane is a rectangle, so it has 4 square corners: 4 right angles."))
    lab = "four objects labelled A to D"
    its.append(pick_grid("Which object has a right angle at every corner?",
                         [door_fig(), pizza_fig(), hanger_fig(), giveway_fig()], "", 1, lab))
    its[-1]["e"] = ("Picture B is a door. It is a rectangle, so all 4 corners are right angles. "
                    "The pizza slice, coat hanger and give way sign have pointy or wide corners.")
    its.append(pick_grid("Which object has no right angles?",
                         [giveway_fig(), book_fig(), window_fig(), door_fig()], "", 3, lab))
    its[-1]["e"] = ("Picture D is a give way sign. It is a triangle with 3 corners that are all smaller than a right angle. "
                    "The others are rectangles.")
    lab = "four shapes labelled A to D"
    g = dict(bw=74, bh=70, sw=2.6)
    its.append(pick_grid("Which shape has exactly 1 right angle?",
                         [shape_fig(RTRI2, 200, **g), shape_fig(RECT2, 0, 76, 50, sw=2.6), shape_fig(EQUI, 0, **g), shape_fig(RTRAP, 0, **g)],
                         "", 2, lab))
    its[-1]["e"] = ("Picture C is a turned triangle with one square corner. The rectangle has 4 right angles, "
                    "the other triangle has none and the 4-sided shape has 2.")
    its.append(pick_grid("Which shape has no right angles?",
                         [shape_fig(PARA, 0, 80, 50, sw=2.6), shape_fig(SQ, 45, **g), shape_fig(RTRI, 0, **g), shape_fig(LSHAPE, 0, **g)],
                         "", 0, lab))
    its[-1]["e"] = ("Picture A leans over, so none of its corners are square corners. "
                    "The turned square, the triangle and the L-shape all have right angles.")
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(90, 35, 66).svg("tilted right angle")) +
                   "%s says this is not a right angle because it is turned. Is %s right?" % (n, he),
                   "No, it is still a right angle", ["Yes, it is smaller than a right angle", "Yes, it is greater than a right angle", "Yes, right angles must stand up straight"],
                   "Turn the page and the arms make a square corner. Turning an angle does not change its size.", rnd))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, -20, 40), angle_fig(115, 0, 62), angle_fig(45, 20, 66), angle_fig(65, 100, 64)],
                         "", 3, "four angles labelled A to D"))
    its[-1]["e"] = ("Picture D makes a square corner. It is turned and its arms are short, but it is still a right angle. "
                    "Check with a right-angle checker.")
    n, he, his = P.next()
    its.append(mcq("%s folds a piece of paper in half, then in half again. What does the folded corner make?" % n,
                   "a right angle", ["a straight line", "an angle smaller than a right angle", "an angle greater than a right angle"],
                   "The first fold makes a straight edge. Folding that edge in half makes a square corner: a right angle. This is a right-angle checker.", rnd))
    its.append(mcq("Where can you find a right angle in the classroom?", "the corner of a whiteboard",
                   ["the edge of a round clock", "the tip of a sharp pencil", "the rim of a cup"],
                   "The corner of a whiteboard is a square corner: a right angle. A pencil tip is smaller than a right angle, and round things have no corners.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(pizza_fig().svg("slice of pizza")) + "%s says the tip of this slice of pizza is a right angle. Is %s right?" % (n, he),
                   "No, it is smaller than a right angle", ["Yes, it is a right angle", "No, it is greater than a right angle", "No, it has no angle"],
                   "The tip is much narrower than a square corner, so it is smaller than a right angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Right angles in shapes and objects", "items": its}


# ------------------------------------------------------------ set 3: greater or smaller than a right angle
def set_compare(rnd, P):
    its = []
    q = "Compare this angle with a right angle. What is it?"
    E = {"smaller than a right angle": "The angle is narrower than a square corner, so it is smaller than a right angle.",
         "a right angle": "The arms make a square corner, so it is a right angle. Turning an angle does not change it.",
         "greater than a right angle": "The angle opens wider than a square corner, so it is greater than a right angle."}
    for deg, rot, L, L2 in [(40, 10, 80, 80), (120, 30, 60, 60), (90, 40, 70, 70), (60, 200, 50, 70), (150, -20, 60, 60),
                            (90, -120, 50, 80), (30, 100, 70, 70), (110, 190, 76, 76), (65, -40, 46, 46)]:
        k = cmp_word(deg)
        its.append(mcq(fig(angle_fig(deg, rot, L, L2).svg("angle")) + q, k, [c for c in CMP if c != k], E[k], rnd))
    lab = "four angles labelled A to D"
    its.append(pick_grid("Which angle is greater than a right angle?",
                         [angle_fig(125, 20, 42), angle_fig(50, 10, 76), angle_fig(90, 0, 60), angle_fig(30, 60, 76)],
                         "opens wider than a square corner. Its arms are short, but that does not make it small.", 1, lab))
    its.append(pick_grid("Which angle is smaller than a right angle?",
                         [angle_fig(45, 100, 50), angle_fig(130, 0, 50), angle_fig(90, 200, 62), angle_fig(110, 60, 56)],
                         "is narrower than a square corner. The others are a right angle or wider.", 2, lab))
    its.append(mcq_fixed(fig(shape_svg(OBTRI, 0, 140, 64, label="triangle ABC", vlabels="ACB")) +
                         "Which angle in this triangle is greater than a right angle?",
                         ["angle A", "angle B", "angle C", "none of them"], "angle B",
                         "Angle B, at the top, opens wider than a square corner. Angles A and C are narrow: smaller than a right angle."))
    A = interior(placed(RTRAP, 0, 140, 76))
    assert [cmp_word(round(a, 6)) if abs(a - 90) > 1e-6 else "a right angle" for a in A] == \
        ["a right angle", "smaller than a right angle", "greater than a right angle", "a right angle"], A
    trap = shape_svg(RTRAP, 0, 140, 76, label="shape ABCD", vlabels="ABCD")
    ABCD = ["angle A", "angle B", "angle C", "angle D"]
    its.append(mcq_fixed(fig(trap) + "Which angle in this shape is smaller than a right angle?", ABCD, "angle B",
                         "Angle B is narrower than a square corner. Angles A and D are right angles, and angle C is wider."))
    its.append(mcq_fixed(fig(trap) + "Which angle in this shape is greater than a right angle?", ABCD, "angle C",
                         "Angle C opens wider than a square corner. Angles A and D are right angles, and angle B is narrower."))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(130, 25, 34).svg("wide angle with short arms")) +
                   "%s says this angle is smaller than a right angle because its arms are short. Is %s right?" % (n, he),
                   "No, it is greater than a right angle", ["Yes, short arms make a small angle", "No, it is a right angle", "Yes, it is smaller"],
                   "The size of an angle is how wide the arms open, not how long they are. This angle opens wider than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(50, 15, 82).svg("narrow angle with long arms")) +
                   "%s says this angle is greater than a right angle because its arms are long. Is %s right?" % (n, he),
                   "No, it is smaller than a right angle", ["Yes, long arms make a big angle", "No, it is a right angle", "Yes, it is greater"],
                   "Long arms do not make an angle bigger. This angle is narrower than a square corner, so it is smaller than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into an angle. The angle is wider than the checker. What is the angle?" % (n, his),
                   "greater than a right angle", ["smaller than a right angle", "a right angle", "a straight line"],
                   "The checker is a right angle. If the angle is wider than the checker, it is greater than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into an angle. The checker does not fit: the angle is narrower. What is the angle?" % (n, his),
                   "smaller than a right angle", ["greater than a right angle", "a right angle", "a straight line"],
                   "The checker is a right angle. If the angle is narrower than the checker, it is smaller than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into a corner of the canteen table. It fits exactly. What is the corner?" % (n, his),
                   "a right angle", ["smaller than a right angle", "greater than a right angle", "a straight line"],
                   "The checker is a right angle. If it fits exactly, with no gap, the corner is a right angle too.", rnd))
    trio = strip_svg([(angle_fig(120, 15, 34), "X"), (angle_fig(40, 10, 82), "Y"), (angle_fig(90, 0, 56), "Z")], cw=104,
                     label="angles X, Y and Z")
    its.append(mcq(fig(trio) + "Put the angles in order from the smallest to the greatest.", "Y, Z, X",
                   ["X, Z, Y", "Z, Y, X", "Y, X, Z"],
                   "Y is smaller than a right angle, Z is a right angle and X is greater than a right angle. Look at how wide the arms open, not the arm length.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Greater or smaller than a right angle", "items": its}


# ------------------------------------------------------------ set 4: count angles in shapes
def set_count(rnd, P):
    its = []
    q = "How many angles does this shape have?"
    shapes = [
        (EQUI, 0, [2, 4, 6], "triangle", "A triangle has 3 corners, so it has 3 angles."),
        (SQ, 45, [2, 3, 5], "turned square", "A square has 4 corners, so it has 4 angles. Turning the square does not change this."),
        (PENT, 0, [4, 6, 10], "shape with 5 sides", "Count the corners: there are 5. So the shape has 5 angles."),
        (HEX, 0, [5, 4, 3], "shape with 6 sides", "Count the corners: there are 6. So the shape has 6 angles."),
        (LSHAPE, 0, [5, 4, 7], "L-shape", "Count every corner, also the one that points inwards. There are 6 corners, so 6 angles."),
        (CUT, 0, [4, 6, 3], "rectangle with one corner cut off", "Cutting off a corner turns 1 corner into 2 corners. 3 + 2 = 5 angles."),
        (OBTRI, 0, [2, 1, 0], "wide triangle", "Every triangle has 3 corners, so it has 3 angles, even when one angle is wide."),
        (TSHAPE, 0, [6, 7, 4], "T-shape", "Count every corner, also the 2 that point inwards under the top. There are 8 corners, so 8 angles."),
    ]
    for pts, rot, wrong, name, e in shapes:
        ans = len(interior(pts))
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label=name)) + q, ans, wrong, e))
    its.append(mcq_num(fig(circle_fig().svg("circle")) + q, 0, [1, 2, 4],
                       "A circle has no straight lines and no corners, so it has no angles."))
    for ch, wrong, e in [("E", [3, 2, 5], "E has 1 angle at the top corner, 2 angles where the middle line meets the upright line and 1 at the bottom corner: 4 angles."),
                         ("F", [2, 4, 1], "F has 1 angle at the top corner and 2 angles where the middle line meets the upright line: 3 angles."),
                         ("N", [1, 3, 4], "N has 1 angle at the top-left and 1 angle at the bottom-right, where the lines meet: 2 angles."),
                         ("X", [2, 1, 3], "The two lines of X cross. They make 4 angles around the middle point."),
                         ("T", [1, 3, 4], "The top line meets the stem in the middle. There is 1 angle on each side: 2 angles.")]:
        n = len(letter_angles(ch))
        its.append(mcq_num(fig(letters_svg([ch], "capital letter " + ch)) + "How many angles are there in the capital letter %s?" % ch,
                           n, wrong, e))
    its.append(mcq_num("A closed shape has 7 straight sides. How many angles does it have?", 7, [8, 9, 14],
                       "A shape with straight sides has as many angles as sides. 7 sides, so 7 angles."))
    lab = "four shapes labelled A to D"
    g = dict(bw=74, bh=70, sw=2.6)
    its.append(pick_grid("Which shape has 5 angles?",
                         [shape_fig(HOUSE, 0, **g), shape_fig(RECT2, 0, 76, 50, sw=2.6), shape_fig(EQUI, 0, **g), shape_fig(HEX, 0, **g)],
                         "", 0, lab))
    its[-1]["e"] = "Picture A has 5 corners, so it has 5 angles. The rectangle has 4, the triangle has 3 and the last shape has 6."
    for pts, rot, kind, wrong, name, e in [
        (PARA, 0, "smaller", [1, 3, 4], "parallelogram", "The 2 sharp corners are smaller than a right angle. The 2 wide corners are greater."),
        (RTRAP, 0, "smaller", [2, 3, 4], "shape with 4 sides", "Only the corner at the bottom right is narrower than a square corner. The 2 left corners are right angles and the top right corner is wide."),
        (HOUSE, 0, "greater", [3, 5, 4], "house shape", "The 2 corners where the roof meets the walls are wider than a square corner. The other 3 are right angles."),
    ]:
        A = interior(placed(pts, rot, 120, 76))
        ans = sum(1 for a in A if (a < 90 - 1e-6 if kind == "smaller" else a > 90 + 1e-6))
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label=name)) +
                           "How many angles in this shape are %s than a right angle?" % kind, ans, wrong, e))
    n, he, his = P.next()
    its.append(mcq_num("%s cuts one corner off a square piece of paper with one straight cut. How many angles does the new shape have?" % n,
                       5, [4, 3, 2], "The cut takes away 1 corner but makes 2 new corners. 4 − 1 + 2 = 5 angles."))
    assert len(its) == 20, len(its)
    return {"title": "Count the angles in shapes", "items": its}


# ------------------------------------------------------------ set 5: turns and clock hands
def set_turns(rnd, P):
    its = []
    q = "The minute hand turns clockwise from the dashed line to where it is now. What turn has it made?"
    for start, k, e in [(12, 1, "From 12 to 3 is a quarter of the way round the clock: a quarter turn."),
                        (3, 2, "From 3 to 9 is halfway round the clock: a half turn."),
                        (6, 3, "From 6 round to 3 is 6 to 9, 9 to 12 and 12 to 3: 3 quarter turns. That is a three-quarter turn."),
                        (9, 4, "The hand goes all the way round from 9 back to 9: a full turn.")]:
        its.append(mcq_fixed(fig(clock_turn_svg(start % 12, k)) + q, TURNS, TURNS[k - 1], e))
    its.append(mcq("How many minutes does the minute hand take to make a quarter turn?", "15 minutes",
                   ["30 minutes", "45 minutes", "25 minutes"],
                   "A full turn of the minute hand takes 60 minutes. A quarter of 60 is 15, so a quarter turn takes 15 minutes.", rnd))
    its.append(mcq("Recess starts at 9.45 am. When it ends, the minute hand has made a half turn. What time does recess end?", "10.15 am",
                   ["10.00 am", "10.45 am", "9.15 am"],
                   "A half turn of the minute hand is 30 minutes. 30 minutes after 9.45 am is 10.15 am.", rnd))
    n, he, his = P.next()
    its.append(mcq("School ends at 1.30 pm. While %s packs %s bag, the minute hand makes a quarter turn. What time is it now?" % (n, his), "1.45 pm",
                   ["2.00 pm", "1.15 pm", "2.30 pm"],
                   "A quarter turn of the minute hand is 15 minutes. 15 minutes after 1.30 pm is 1.45 pm.", rnd))
    for h, e in [(3, "At 3 o’clock the hands make a square corner: a right angle."),
                 (5, "At 5 o’clock the hands are 5 hour marks apart. A right angle is only 3 hour marks, so this angle is greater."),
                 (1, "At 1 o’clock the hands are only 1 hour mark apart. That is narrower than a right angle (3 hour marks).")]:
        k = cmp_word(30 * h)
        its.append(mcq(fig(clock_svg(h)) + "What angle do the hands make?", k, [c for c in CMP if c != k], e, rnd))
    its.append(mcq(fig(clock_svg(6)) + "What do the hands of the clock make at 6 o’clock?", "a straight line",
                   ["a right angle", "a square corner", "an angle smaller than a right angle"],
                   "At 6 o’clock the hands point in opposite directions. Together they make a straight line: a half turn.", rnd))
    its.append(mcq("At which time do the hands of a clock make a right angle?", "3 o’clock",
                   ["6 o’clock", "1 o’clock", "12 o’clock"],
                   "At 3 o’clock the long hand points to 12 and the short hand points to 3. They make a square corner.", rnd))
    its.append(mcq("From 12 noon to 3 pm, what turn does the hour hand make?", "a quarter turn",
                   ["a half turn", "a full turn", "a three-quarter turn"],
                   "The hour hand moves from 12 to 3. That is a quarter of the way round the clock: a quarter turn.", rnd))
    its.append(mcq("From 12 noon to 6 pm, what turn does the hour hand make?", "a half turn",
                   ["a quarter turn", "a full turn", "a three-quarter turn"],
                   "The hour hand moves from 12 to 6. That is halfway round the clock: a half turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens the classroom door until it makes a square corner with the wall. What turn has the door made?" % n,
                   "a quarter turn", ["a half turn", "a three-quarter turn", "a full turn"],
                   "A square corner is a right angle, and a right angle is a quarter turn.", rnd))
    its.append(mcq("A capsule on the Singapore Flyer goes all the way round once. It comes back to where it started. What turn has it made?",
                   "a full turn", ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "Going all the way round and back to the start is a full turn.", rnd))
    n, he, his = P.next()
    its.append(mcq_num("%s turns the tap on with a half turn. How many right angles has the handle turned through?" % n,
                       2, [1, 3, 4], "A half turn is 2 quarter turns, and each quarter turn is a right angle. So the handle turns through 2 right angles."))
    n, he, his = P.next()
    its.append(mcq("%s walks along the void deck. At the lift lobby, %s turns right. What turn does %s make?" % (n, he, he),
                   "a quarter turn", ["a half turn", "a full turn", "a three-quarter turn"],
                   "Turning right makes a square corner with the way you were walking. That is a quarter turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens %s laptop so that the screen leans back a little past a square corner. What angle do the screen and keyboard make?" % (n, his),
                   "greater than a right angle", ["smaller than a right angle", "a right angle", "a straight line"],
                   "A square corner is a right angle. The screen opens a little wider than that, so the angle is greater than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("On Sports Day, %s faces the finishing line. %s makes a half turn. Which way does %s face now?" % (n, he.capitalize(), he),
                   "the opposite way", ["the same way", "to the left side", "to the right side"],
                   "A half turn is 2 right angles. It makes you face the opposite way, away from the finishing line.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Turns and clock hands", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    parts = arm_lesson_svg().svg("an angle with its two arms and its vertex labelled")
    objects = strip_svg([(book_fig(True), "book"), (door_fig(True), "door"), (window_fig(True), "window")],
                        cw=110, label="a book, a door and a window with their right angles marked")
    shapes = strip_svg([(shape_fig(RECT, 0, 96, 56, sw=2.8, marks=True), "4 right angles"),
                        (shape_fig(SQ, 45, 70, 70, sw=2.8, marks=True), "still 4"),
                        (shape_fig(RTRI, 0, 96, 60, sw=2.8, marks=True), "1 right angle")],
                       cw=130, label="rectangle, turned square and right-angled triangle with their right angles marked")
    kinds = strip_svg([(angle_fig(45, 10, 66), "smaller"), (angle_fig(90, 0, 60, marked=True), "right angle"),
                       (angle_fig(130, 10, 54), "greater")],
                      cw=130, label="angle smaller than a right angle, a right angle and an angle greater than a right angle")
    same = strip_svg([(angle_fig(55, 10, 86), "long arms"), (angle_fig(55, 10, 36), "short arms")], cw=128,
                     label="two angles of the same size with long and short arms")
    count = strip_svg([(shape_fig(EQUI, 0, 80, 70, sw=2.8), "3 angles"), (shape_fig(LSHAPE, 0, 80, 70, sw=2.8), "6 angles"),
                       (shape_fig(PENT, 0, 80, 70, sw=2.8), "5 angles")],
                      cw=120, label="a triangle with 3 angles, an L-shape with 6 angles and a shape with 5 angles")
    turns = strip_svg([(turn_fig(f), t) for t, f in (("quarter", 0.25), ("half", 0.5), ("three-quarter", 0.75), ("full", 1.0))],
                      cw=124, label="quarter, half, three-quarter and full turns clockwise")
    return (
        "<h2>What is an angle?</h2>"
        "<p>An <b>angle</b> is made when two straight lines meet at a point. "
        "The two lines are the <b>arms</b>. The point where they meet is the <b>vertex</b>.</p>"
        "<figure class='sn-fig'>" + parts +
        "<figcaption>The size of an angle is how wide the arms open.</figcaption></figure>"
        "<figure class='sn-fig'>" + same +
        "<figcaption>These two angles are the same size. Longer arms do not make an angle bigger.</figcaption></figure>"
        "<h2>Right angles</h2>"
        "<p>A <b>right angle</b> is a square corner. A small square in a corner shows a right angle. "
        "Make a <b>right-angle checker</b>: fold a piece of paper in half, then in half again.</p>"
        "<figure class='sn-fig'>" + objects +
        "<figcaption>Books, doors and windows have a right angle at every corner.</figcaption></figure>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>A turned square still has 4 right angles. Turning a shape does not change its angles.</figcaption></figure>"
        "<h2>Greater or smaller than a right angle</h2>"
        "<p>Put your checker in the angle. If the angle is narrower, it is <b>smaller than</b> a right angle. "
        "If it is wider, it is <b>greater than</b> a right angle.</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>" +
        ex("Example", "At 5 o’clock, what angle do the hands of a clock make?",
           "At 3 o’clock the hands make a right angle (3 hour marks). 5 hour marks is wider.", "greater than a right angle") +
        "<h2>Counting angles in a shape</h2>"
        "<p>Count the corners. Every corner of a shape with straight sides is an angle, "
        "also a corner that points inwards.</p>"
        "<figure class='sn-fig'>" + count + "</figure>" +
        ex("Example", "Priya cuts one corner off a rectangle with one straight cut. How many angles does the new shape have?",
           "The cut takes away 1 corner and makes 2 new corners. 4 − 1 + 2 = 5.", "5 angles") +
        "<h2>Turns and clock hands</h2>"
        "<p>When a clock hand turns, it makes an angle. A <b>quarter turn</b> makes a right angle. "
        "A <b>half turn</b> is 2 right angles and a <b>full turn</b> is 4 right angles.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Each turn starts at the dashed line and goes clockwise, like clock hands.</figcaption></figure>" +
        ex("Example", "The minute hand makes a quarter turn. How many minutes is that?",
           "A full turn is 60 minutes. A quarter of 60 is 15.", "15 minutes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at how wide the arms open, not how long they are"],
            ["Saying a turned square corner is not a right angle", "Turn the page or use a checker: turning does not change an angle"],
            ["Not counting a corner that points inwards", "Count every corner of the shape"],
            ["Calling curved lines an angle", "The arms of an angle are straight lines"],
        ])
    )


FAQ = [
    {"q": "What do P3 students learn about angles?",
     "a": "They learn that an angle is made by two straight arms meeting at a vertex, find right angles in shapes and objects, and say if an angle is greater or smaller than a right angle. This is part of Geometry in the MOE Primary 3 syllabus."},
    {"q": "How do I explain a right angle to my child?",
     "a": "A right angle is a square corner, like the corner of a book or a door. Fold a piece of paper in half and in half again to make a right-angle checker, then look for square corners at home."},
    {"q": "What is the most common mistake with angles in P3?",
     "a": "Thinking that longer arms make a bigger angle. The size of an angle is how wide the arms open. Another mistake is saying a turned square corner is not a right angle."},
    {"q": "Do Primary 3 students measure angles in degrees?",
     "a": "No. In P3 students compare angles with a right angle. Measuring angles in degrees with a protractor comes in Primary 4."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order
    (A-D pictures, turns, numbers) stay as they are; the other questions fill the gaps."""
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
    rnd = random.Random(63811)
    P = People(rnd)
    sets = [set_what(rnd, P), set_rights(rnd, P), set_compare(rnd, P), set_count(rnd, P), set_turns(rnd, P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "angles", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Angles: Right Angles and Comparing Angles",
        "seo_title": "P3 Angles and Right Angles Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Angles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 3: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Concepts of angle; right angles; angles greater than or smaller than a right angle",
        "meta_desc": "Free P3 maths practice on angles: arms and vertex, right angles, greater or smaller than a right angle, "
                     "counting angles and turns. 100 questions with answers.",
        "key_big": "An angle is two straight arms meeting at a vertex. Its size is how wide the arms open.",
        "key_sub": "At 3 o’clock the clock hands make a right angle; at 1 o’clock the angle is smaller than a right angle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, rows of figures) so they stay readable."""
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
        mark_large(u, "(four [a-z ]+ labelled A to D|angle P and angle Q|angles X, Y and Z|capital letters L, V, O and N)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
