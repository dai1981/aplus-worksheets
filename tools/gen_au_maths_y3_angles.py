# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Angles as turns (Australian Curriculum v9.0, AC9M3M05)
  python3 tools/gen_au_maths_y3_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 3 students see an angle as a measure of turn and compare angles with a right angle
(a quarter turn): 2 right angles make a half turn, 3 a three-quarter turn and 4 a full turn.
No degrees (that is Year 5). Every drawing is exact and checked in code: right angles are true
right angles, any angle that is not a right angle is at least 20 degrees away from one, and no
label touches a line. Pictures where students must judge an angle have NO right-angle marks.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
RED = "#c8102e"
WOOD = "#e6d3b3"
GLASS = "#dcecf5"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


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


# ------------------------------------------------------------ set 1: turns
def set_turns(rnd, P):
    its = []
    q = "What turn does the arrow show? It starts at the dashed line."
    for frac, cw, ans, e in [
        (0.25, True, "quarter turn", "The arrow goes a quarter of the way round. That is a quarter turn."),
        (0.5, False, "half turn", "The arrow goes halfway round, so the end line points the opposite way. That is a half turn."),
        (0.75, True, "three-quarter turn", "The arrow goes three quarters of the way round. That is a three-quarter turn."),
        (1.0, False, "full turn", "The arrow goes all the way round, back to the dashed line. That is a full turn."),
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
    its.append(mcq("Which way do the hands on an analog clock turn?", "clockwise",
                   ["anticlockwise", "both ways", "up and down"],
                   "Clock hands always turn the same way: clockwise. Anticlockwise is the opposite way.", rnd))
    for n, wrong, t, e in [
        (2, [1, 3, 4], "a half turn", "A half turn is 2 quarter turns: a quarter and another quarter make a half."),
        (4, [2, 3, 1], "a full turn", "A full turn is 4 quarter turns. Four quarters make one whole."),
        (3, [1, 2, 4], "a three-quarter turn", "A three-quarter turn is 3 quarter turns."),
    ]:
        its.append(mcq_num("How many quarter turns make %s?" % t, n, wrong, e))
    its.append(mcq("Which turn takes you back to where you started?", "a full turn",
                   ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "A full turn goes all the way round, so you face the same way again.", rnd))
    its.append(mcq("Which turn makes you face the opposite way?", "a half turn",
                   ["a quarter turn", "a full turn", "a three-quarter turn"],
                   "A half turn goes halfway round, so you end up facing the opposite way.", rnd))
    a, b = P.next(), P.next()
    its.append(mcq("%s and %s both face the board. %s makes a half turn clockwise. %s makes a half turn anticlockwise. What is true now?"
                   % (a[0], b[0], a[0], b[0]),
                   "They face the same way", ["They face opposite ways", "%s faces the board" % a[0], "%s faces the board" % b[0]],
                   "A half turn either way ends facing the opposite way to the start. So they both face away from the board: the same way.", rnd))
    its.append(mcq("A quarter turn clockwise ends facing the same way as which other turn?", "a three-quarter turn anticlockwise",
                   ["a quarter turn anticlockwise", "a half turn clockwise", "a three-quarter turn clockwise"],
                   "Going 1 quarter one way ends in the same place as going 3 quarters the other way. 1 + 3 = 4 quarters, a full turn.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_fig(0.5, True).svg("half turn clockwise")) + "%s says this arrow shows a quarter turn. Is %s right?" % (n, he),
                   "No, it is a half turn", ["Yes, it is a quarter turn", "No, it is a full turn", "No, it is a three-quarter turn"],
                   "The end line points the opposite way to the dashed line. The arrow goes halfway round: a half turn.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(turn_fig(0.25, False).svg("quarter turn anticlockwise")) + "%s says this turn is clockwise. Is %s right?" % (n, he),
                   "No, it is anticlockwise", ["Yes, it is clockwise", "No, it is a half turn", "Yes, all turns are clockwise"],
                   "Clock hands go from 12 to 3, to the right at the top. This arrow goes to the left at the top: anticlockwise.", rnd))
    room = ["door", "window", "board", "bookshelf"]
    n, he, his = P.next()
    its.append(mcq_fixed(fig(facing_fig(room, 1, fs=16, R=50).svg("student in a classroom facing the window")) +
                         "%s faces the window. %s makes a full turn. What does %s face now?" % (n, he.capitalize(), he),
                         ["the " + r for r in room], "the window",
                         "A full turn goes all the way round, so %s faces the window again." % he))
    n, he, his = P.next()
    its.append(mcq_fixed("%s makes a quarter turn clockwise. Then %s makes a half turn clockwise. What turn is that altogether?" % (n, he),
                         TURNS, "three-quarter turn", "1 quarter turn + 2 quarter turns = 3 quarter turns. That is a three-quarter turn."))
    assert len(its) == 20, len(its)
    return {"title": "Quarter, half, three-quarter and full turns", "items": its}


# ------------------------------------------------------------ set 2: a quarter turn makes a right angle
def set_quarter(rnd, P):
    its = []
    lab = "four angles labelled A to D"
    its.append(mcq(fig(angle_fig(90, 20, 64, marked=True).svg("right angle with a small square")) +
                   "What does the small square in the corner show?", "a right angle",
                   ["a square shape", "a small angle", "a half turn"],
                   "A small square in a corner shows a right angle: a square corner, like the corner of a page.", rnd))
    for n, wrong, e in [(1, [2, 3, 4], "A quarter turn makes 1 right angle."),
                        (2, [1, 3, 4], "A half turn is 2 quarter turns, so it is 2 right angles."),
                        (3, [1, 2, 4], "A three-quarter turn is 3 quarter turns, so it is 3 right angles."),
                        (4, [1, 2, 3], "A full turn is 4 quarter turns, so it is 4 right angles.")]:
        t = {1: "a quarter turn", 2: "a half turn", 3: "a three-quarter turn", 4: "a full turn"}[n]
        its.append(mcq_num("How many right angles make %s?" % t, n, wrong, e))
    its.append(mcq_fixed("A right angle is the same as which turn?", TURNS, "quarter turn",
                         "A right angle is a quarter turn: the corner you make when you turn a quarter of the way round."))
    its.append(mcq("Two right angles side by side make what?", "a straight line",
                   ["a square", "a full turn", "a smaller angle"],
                   "2 right angles make a half turn. The two outside arms point opposite ways, so they make a straight line.", rnd))
    q2 = "%s faces %s. %s makes a %s %s. Which way does %s face now?"
    for start, k, cw in [(0, 1, True), (3, 1, False), (2, 2, True), (0, 1, False)]:
        n, he, his = P.next()
        end = (start + (k if cw else -k)) % 4
        turn = {1: "quarter turn", 2: "half turn"}[k]
        cwa = "clockwise" if cw else "anticlockwise"
        if k == 2:
            e = "A half turn makes you face the opposite way. %s is opposite %s." % (POINTS[end].capitalize(), POINTS[start])
        else:
            e = "A quarter turn %s goes from %s to %s." % (cwa, POINTS[start], POINTS[end])
            e += " Clockwise goes N, E, S, W." if cw else " Anticlockwise goes N, W, S, E."
        its.append(mcq_fixed(fig(compass_svg(start)) + q2 % (n, POINTS[start], he.capitalize(), turn, cwa, he),
                             POINTS, POINTS[end], e))
    n, he, his = P.next()
    its.append(mcq_num("%s faces north. %s turns until %s faces south. How many right angles has %s turned through?" % (n, he.capitalize(), he, he),
                       2, [1, 3, 4], "North to south is a half turn: north to east is 1 right angle, east to south is 1 more. That is 2."))
    n, he, his = P.next()
    its.append(mcq_num("%s faces north. %s turns clockwise until %s faces west. How many right angles has %s turned through?" % (n, he.capitalize(), he, he),
                       3, [1, 2, 4], "Clockwise from north: east (1), south (2), west (3). That is 3 right angles: a three-quarter turn."))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, 30, 56), angle_fig(60, 10, 64), angle_fig(120, 20, 50), angle_fig(65, 100, 64)],
                         "makes a square corner. It is tilted, but it is still a right angle. Check with the corner of a piece of paper.", 0, lab))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, -20, 40), angle_fig(115, 0, 62), angle_fig(45, 20, 66), angle_fig(150, 15, 44)],
                         "makes a square corner. Its arms are short, but arm length does not change an angle.", 3, lab))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(90, 35, 66).svg("tilted right angle")) +
                   "%s says this is not a right angle because it is tilted. Is %s right?" % (n, he),
                   "No, it is still a right angle", ["Yes, it is less than a right angle", "Yes, it is greater than a right angle", "No, it is a straight line"],
                   "Turn the page and the arms make a square corner. Tilting an angle does not change its size.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a piece of paper in half, then in half again. What does the folded corner make?" % n,
                   "a right angle", ["a straight line", "a half turn", "an angle greater than a right angle"],
                   "The first fold makes a straight edge (a half turn). Folding that in half makes a quarter turn: a right angle. This is a right-angle checker.", rnd))
    its.append(mcq_fixed(fig(turn_fig(0.25, True).svg("quarter turn clockwise")) +
                         "The arrow shows a quarter turn. What angle do the dashed line and the solid line make?",
                         CMP, "a right angle", "A quarter turn makes a right angle between the start line and the end line."))
    its.append(mcq_fixed("Which turn is the same as 3 right angles?", TURNS, "three-quarter turn",
                         "Each right angle is a quarter turn. 3 quarter turns make a three-quarter turn."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s turns clockwise through 1 right angle, then 1 more right angle. What turn is that altogether?" % n,
                         TURNS, "half turn", "1 right angle + 1 right angle = 2 right angles. 2 quarter turns make a half turn."))
    assert len(its) == 20, len(its)
    return {"title": "A quarter turn makes a right angle", "items": its}


# ------------------------------------------------------------ set 3: right angles in shapes and everyday objects
def set_rights(rnd, P):
    its = []
    q = "How many right angles does this shape have?"
    shapes = [
        (SQ, 45, 4, [0, 2, 1], "square", "A square has 4 right angles. It is turned, but turning does not change the angles."),
        (RTRI, 0, 1, [0, 3, 2], "right-angled triangle", "Only the bottom-left corner is a square corner. The other 2 corners are smaller."),
        (EQUI, 0, 0, [3, 1, 2], "triangle", "All 3 corners are smaller than a right angle, so there are no right angles."),
        (LSHAPE, 0, 5, [6, 4, 3], "L-shape", "5 corners are square corners. The corner that points inwards is greater than a right angle, so do not count it."),
        (HOUSE, 0, 3, [5, 2, 4], "house shape", "The 2 bottom corners and the top of the roof are right angles. The 2 corners where the roof meets the walls are greater."),
        (RTRAP, 0, 2, [4, 1, 0], "shape with 4 sides", "The 2 corners on the left are right angles. The 2 corners on the right are not."),
        (CUT, 0, 3, [5, 4, 2], "rectangle with one corner cut off", "3 corners are still square corners. Cutting off a corner makes 2 corners that are greater than a right angle."),
    ]
    for pts, rot, ans, wrong, name, e in shapes:
        assert len(rights(placed(pts, rot, 120, 76))) == ans, name
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label=name)) + q, ans, wrong, e))
    for ch, wrong, e in [("L", [0, 2, 3], "Where the 2 lines of L meet, the inside corner is 1 right angle."),
                         ("T", [0, 1, 4], "Where the top line meets the stem, there is a right angle on each side. That is 2 right angles.")]:
        n = letter_rights(ch)
        its.append(mcq_num(fig(letters_svg([ch], "capital letter " + ch)) + "How many right angles are inside the capital letter %s?" % ch,
                           n, wrong, e))
    n, he, his = P.next()
    F = book_fig()
    assert len(rights(rect_pts(62, 82))) == 4
    its.append(mcq_num(fig(F.svg("library book")) + "%s checks the corners of %s library book with a right-angle checker. How many corners are right angles?" % (n, his),
                       4, [2, 3, 1], "The front cover is a rectangle. All 4 corners are square corners, so all 4 are right angles."))
    stop = [add((0, 0), dirv(22.5 + 45 * i), 42) for i in range(8)]
    assert rights(stop) == []
    its.append(mcq_num(fig(stop_fig().svg("stop sign")) + "How many right angles does this stop sign have?",
                       0, [8, 4, 1], "A stop sign has 8 corners, but each one is greater than a right angle. So it has no right angles."))
    its.append(mcq_num(fig(window_fig().svg("window with 4 panes of glass")) +
                       "This window has 4 panes of glass. How many right angles does one pane have?",
                       4, [2, 1, 0], "Each pane is a rectangle, so it has 4 square corners: 4 right angles."))
    lab = "four objects labelled A to D"
    its.append(pick_grid("Which object has a right angle at every corner?",
                         [door_fig(), pizza_fig(), hanger_fig(), giveway_fig()],
                         "is a door. It is a rectangle, so all 4 corners are right angles. The pizza slice, coat hanger and give way sign have pointy or wide corners.", 0, lab))
    its.append(pick_grid("Which object has no right angles?",
                         [giveway_fig(), book_fig(), window_fig(), door_fig()],
                         "is a give way sign. It is a triangle with 3 corners that are all less than a right angle. The others are rectangles.", 0, lab))
    lab = "four shapes labelled A to D"
    g = dict(bw=74, bh=70, sw=2.6)
    its.append(pick_grid("Which shape has exactly 1 right angle?",
                         [shape_fig(RTRI2, 200, **g), shape_fig(RECT2, 0, 76, 50, sw=2.6), shape_fig(EQUI, 0, **g), shape_fig(RTRAP, 0, **g)],
                         "is a triangle with one square corner. The rectangle has 4, the other triangle has none and the 4-sided shape has 2.", 2, lab))
    its.append(pick_grid("Which shape has no right angles?",
                         [shape_fig(PARA, 0, 80, 50, sw=2.6), shape_fig(SQ, 45, **g), shape_fig(RTRI, 0, **g), shape_fig(LSHAPE, 0, **g)],
                         "leans over, so none of its corners are square corners. The turned square, the triangle and the L-shape all have right angles.", 3, lab))
    n, he, his = P.next()
    its.append(mcq(fig(shape_svg(RECT, 25, 120, 76, label="turned rectangle")) +
                   "%s says this shape has no right angles because it is turned. Is %s right?" % (n, he),
                   "No, it still has 4 right angles", ["Yes, it has no right angles", "No, it has 2 right angles", "Yes, turned shapes lose their corners"],
                   "It is a rectangle that has been turned. Turning a shape does not change its angles, so it still has 4 right angles.", rnd))
    its.append(mcq("Which of these usually has 4 right angles?", "a classroom door",
                   ["a slice of pizza", "a coat hanger", "a give way sign"],
                   "A door is a rectangle, so it has 4 square corners. A pizza slice and a give way sign have pointy corners.", rnd))
    its.append(mcq("Where can you find a right angle in the classroom?", "the corner of a book",
                   ["the edge of a round clock", "the tip of a sharp pencil", "the edge of a dinner plate"],
                   "The corner of a book is a square corner: a right angle. A pencil tip is less than a right angle, and round things have no corners.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(pizza_fig().svg("slice of pizza")) + "%s says the tip of this slice of pizza is a right angle. Is %s right?" % (n, he),
                   "No, it is less than a right angle", ["Yes, it is a right angle", "No, it is greater than a right angle", "No, it is a straight line"],
                   "The tip is much narrower than a square corner, so it is less than a right angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Right angles in shapes and everyday objects", "items": its}


# ------------------------------------------------------------ set 4: greater or less than a right angle
def set_compare(rnd, P):
    its = []
    q = "Compare this angle with a right angle. What is it?"
    for deg, rot, L, L2 in [(40, 10, 80, 80), (120, 30, 60, 60), (90, 40, 70, 70), (60, 200, 50, 70), (150, -20, 60, 60),
                            (90, -120, 50, 80), (30, 100, 70, 70), (110, 190, 76, 76), (180, 20, 56, 56), (65, -40, 46, 46)]:
        k = cmp_word(deg)
        e = {"less than a right angle": "The angle is narrower than a square corner, so it is less than a right angle.",
             "a right angle": "The arms make a square corner, so it is a right angle. Tilting an angle does not change it.",
             "greater than a right angle": "The angle opens wider than a square corner, so it is greater than a right angle.",
             "a straight line": "The arms point in opposite directions and make a straight line: 2 right angles (a half turn)."}[k]
        its.append(mcq_fixed(fig(angle_fig(deg, rot, L, L2).svg("angle")) + q, CMP, k, e))
    lab = "four angles labelled A to D"
    its.append(pick_grid("Which angle is greater than a right angle?",
                         [angle_fig(125, 20, 42), angle_fig(50, 10, 76), angle_fig(90, 0, 60), angle_fig(30, 60, 76)],
                         "opens wider than a square corner. Its arms are short, but that does not make it small.", 3, lab))
    its.append(pick_grid("Which angle is less than a right angle?",
                         [angle_fig(45, 100, 50), angle_fig(130, 0, 50), angle_fig(90, 200, 62), angle_fig(110, 60, 56)],
                         "is narrower than a square corner. The others are a right angle or wider.", 3, lab))
    its.append(mcq_fixed(fig(shape_svg(OBTRI, 0, 140, 64, label="triangle ABC", vlabels="ACB")) +
                         "Which angle in this triangle is greater than a right angle?",
                         ["angle A", "angle B", "angle C", "none of them"], "angle B",
                         "Angle B, at the top, opens wider than a square corner. Angles A and C are narrow: less than a right angle."))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(130, 25, 34).svg("wide angle with short arms")) +
                   "%s says this angle is less than a right angle because its arms are short. Is %s right?" % (n, he),
                   "No, it is greater than a right angle", ["Yes, short arms make a small angle", "No, it is a right angle", "Yes, it is a small turn"],
                   "The size of an angle is how far it turns, not how long its arms are. This angle opens wider than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(50, 15, 82).svg("narrow angle with long arms")) +
                   "%s says this angle is greater than a right angle because its arms are long. Is %s right?" % (n, he),
                   "No, it is less than a right angle", ["Yes, long arms make a big angle", "No, it is a right angle", "Yes, it is a straight line"],
                   "Long arms do not make an angle bigger. This angle is narrower than a square corner, so it is less than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into an angle. The angle is wider than the checker. What is the angle?" % (n, his),
                   "greater than a right angle", ["less than a right angle", "a right angle", "a full turn"],
                   "The checker is a right angle. If the angle is wider than the checker, it is greater than a right angle.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s puts %s right-angle checker into a corner of the classroom table. It fits exactly. What is the corner?" % (n, his),
                   "a right angle", ["less than a right angle", "greater than a right angle", "a half turn"],
                   "The checker is a right angle. If it fits exactly, with no gap and no overlap, the corner is a right angle too.", rnd))
    pair = strip_svg([(angle_fig(50, 20, 82), "P"), (angle_fig(120, 10, 38), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Which angle is greater?", "angle Q",
                   ["angle P", "They are the same size", "You cannot tell"],
                   "Angle Q opens wider than a right angle, and angle P is less than a right angle. So Q is greater, even though P has longer arms.", rnd))
    trio = strip_svg([(angle_fig(120, 15, 34), "X"), (angle_fig(40, 10, 82), "Y"), (angle_fig(90, 0, 56), "Z")], cw=104,
                     label="angles X, Y and Z")
    its.append(mcq(fig(trio) + "Put the angles in order from smallest to largest.", "Y, Z, X",
                   ["X, Z, Y", "Z, Y, X", "Y, X, Z"],
                   "Y is less than a right angle, Z is a right angle and X is greater than a right angle. Look at the turn, not the arm length.", rnd))
    its.append(mcq("An angle is a bit more than a quarter turn. What is it?", "greater than a right angle",
                   ["less than a right angle", "a right angle", "a straight line"],
                   "A quarter turn is a right angle. A bit more than a quarter turn is greater than a right angle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Greater than or less than a right angle", "items": its}


# ------------------------------------------------------------ set 5: everyday situations
def set_problems(rnd, P):
    its = []
    q = "The minute hand turns clockwise from the dashed line to where it is now. What turn has it made?"
    for start, k, e in [(12, 1, "From 12 to 3 is a quarter of the way round the clock: a quarter turn."),
                        (3, 2, "From 3 to 9 is halfway round the clock: a half turn."),
                        (6, 3, "From 6 round to 3 is 6 to 9, 9 to 12 and 12 to 3: 3 quarter turns. That is a three-quarter turn."),
                        (9, 4, "The hand goes all the way round from 9 back to 9: a full turn.")]:
        its.append(mcq_fixed(fig(clock_turn_svg(start % 12, k)) + q, TURNS, TURNS[k - 1], e))
    its.append(mcq("How many minutes does the minute hand take to make a quarter turn?", "15 minutes",
                   ["30 minutes", "45 minutes", "60 minutes"],
                   "A full turn of the minute hand takes 60 minutes. A quarter of 60 is 15, so a quarter turn takes 15 minutes.", rnd))
    its.append(mcq("School starts at 8:45 am. The minute hand makes a half turn. What time is it now?", "9:15 am",
                   ["9:00 am", "9:45 am", "8:15 am"],
                   "A half turn of the minute hand is 30 minutes. 30 minutes after 8:45 am is 9:15 am.", rnd))
    for h, e in [(3, "At 3 o’clock the hands make a square corner: a right angle."),
                 (5, "At 5 o’clock the hands are 5 hour marks apart. A right angle is only 3 hour marks, so this angle is greater."),
                 (1, "At 1 o’clock the hands are only 1 hour mark apart. That is narrower than a right angle (3 hour marks)."),
                 (6, "At 6 o’clock the hands point in opposite directions. They make a straight line: a half turn.")]:
        its.append(mcq_fixed(fig(clock_svg(h)) + "What angle do the hands make?", CMP, cmp_word(30 * min(h, 12 - h)), e))
    n, he, his = P.next()
    its.append(mcq_num("%s turns the garden tap on with a half turn. How many right angles has the handle turned through?" % n,
                       2, [1, 3, 4], "A half turn is 2 quarter turns, and each quarter turn is a right angle. So the handle turns through 2 right angles."))
    ramp = ramp_svg()
    its.append(mcq_fixed(fig(ramp) + "This skateboard ramp sits on flat ground. Which corner of the ramp is a right angle?",
                         ["angle A", "angle B", "angle C", "none of them"], "angle B",
                         "At B the upright back of the ramp meets the flat ground. That makes a square corner: a right angle."))
    its.append(mcq_fixed(fig(ramp) + "Angle A is where the ramp meets the ground. Compare it with a right angle.",
                         CMP, "less than a right angle",
                         "The ramp slopes up gently. Angle A is much narrower than a square corner, so it is less than a right angle."))
    n, he, his = P.next()
    its.append(mcq_fixed("%s walks north along the beach. %s turns right. Which way is %s walking now?" % (n, he.capitalize(), he), POINTS, "east",
                         "Turning right is a quarter turn clockwise. A quarter turn clockwise from north is east."))
    n, he, his = P.next()
    its.append(mcq_fixed("On a school excursion, %s faces north to read a map. %s makes a half turn. Which way does %s face now?" % (n, he.capitalize(), he),
                         POINTS, "south", "A half turn makes you face the opposite way. South is opposite north."))
    n, he, his = P.next()
    its.append(mcq_fixed(fig(compass_svg(2)) + "%s faces south. %s makes a three-quarter turn anticlockwise. Which way does %s face now?" % (n, he.capitalize(), he),
                         POINTS, "west", "Anticlockwise from south goes east (1), north (2), west (3). So %s faces west." % he))
    n, he, his = P.next()
    its.append(mcq("%s opens the classroom door until it makes a square corner with the wall. What turn has the door made?" % n,
                   "a quarter turn", ["a half turn", "a three-quarter turn", "a full turn"],
                   "A square corner is a right angle, and a right angle is a quarter turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("At the athletics carnival, %s runs once around the oval and ends where %s started. What turn has %s made?" % (n, he, he),
                   "a full turn", ["a half turn", "a quarter turn", "a three-quarter turn"],
                   "Going all the way round and facing the same way again is a full turn.", rnd))
    n, he, his = P.next()
    its.append(mcq("At the skate park, %s rides forwards and then does a half turn on %s skateboard. Which way is %s facing now?" % (n, his, he),
                   "the opposite way", ["the same way", "sideways", "upside down"],
                   "A half turn is 2 right angles, so %s ends up facing the opposite way." % he, rnd))
    its.append(mcq("From 12 noon to 3 pm, what turn does the hour hand make?", "a quarter turn",
                   ["a half turn", "a full turn", "a three-quarter turn"],
                   "The hour hand moves from 12 to 3. That is a quarter of the way round the clock: a quarter turn.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Angles in everyday situations", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    turns = strip_svg([(turn_fig(f), t) for t, f in (("quarter", 0.25), ("half", 0.5), ("three-quarter", 0.75), ("full", 1.0))],
                      cw=124, label="quarter, half, three-quarter and full turns clockwise")
    comp = compass_svg(0, "compass points north, east, south and west")
    objects = strip_svg([(book_fig(True), "book"), (door_fig(True), "door"), (window_fig(True), "window")],
                        cw=110, label="a book, a door and a window with their right angles marked")
    shapes = strip_svg([(shape_fig(RECT, 0, 96, 56, sw=2.8, marks=True), "4 right angles"),
                        (shape_fig(RTRI, 0, 96, 60, sw=2.8, marks=True), "1 right angle"),
                        (shape_fig(LSHAPE, 0, 80, 70, sw=2.8, marks=True), "5 right angles")],
                       cw=130, label="rectangle, right-angled triangle and L-shape with their right angles marked")
    kinds = strip_svg([(angle_fig(45, 10, 66), "less than"), (angle_fig(90, 0, 60, marked=True), "right angle"),
                       (angle_fig(130, 10, 54), "greater than")],
                      cw=130, label="angle less than a right angle, a right angle and an angle greater than a right angle")
    same = strip_svg([(angle_fig(55, 10, 86), "long arms"), (angle_fig(55, 10, 36), "short arms")], cw=128,
                     label="two angles of the same size with long and short arms")
    return (
        "<h2>An angle is a turn</h2>"
        "<p>An angle measures how far something <b>turns</b>. "
        "Clock hands turn <b>clockwise</b>. The other way is <b>anticlockwise</b>.</p>"
        "<figure class='sn-fig'>" + turns +
        "<figcaption>Each turn starts at the dashed line and goes clockwise.</figcaption></figure>" +
        table(["Turn", "Quarter turns", "Right angles"], [
            ["Quarter turn", "1", "1"], ["Half turn", "2", "2 (a straight line)"],
            ["Three-quarter turn", "3", "3"], ["Full turn", "4", "4 (back to the start)"],
        ]) +
        "<figure class='sn-fig'>" + comp +
        "<figcaption>Clockwise from north: north, east, south, west.</figcaption></figure>" +
        ex("Example", "Mia faces north. She makes a quarter turn clockwise. Which way does she face now?",
           "Clockwise goes north, east, south, west. One quarter turn from north is east.", "east") +
        ex("Example", "Jack faces east. He makes a half turn. Which way does he face now?",
           "A half turn makes you face the opposite way. West is opposite east.", "west") +
        "<h2>A quarter turn makes a right angle</h2>"
        "<p>A <b>right angle</b> is a square corner. It is the angle a quarter turn makes. "
        "A small square in a corner shows a right angle.</p>"
        "<figure class='sn-fig'>" + objects +
        "<figcaption>Books, doors and windows have a right angle at every corner.</figcaption></figure>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>Do not count a corner that points inwards: it is greater than a right angle.</figcaption></figure>"
        "<p>Make a <b>right-angle checker</b>: fold a piece of paper in half, then in half again.</p>"
        "<h2>Greater than or less than a right angle</h2>"
        "<p>Put your checker in the angle. If the angle is narrower, it is <b>less than</b> a right angle. "
        "If it is wider, it is <b>greater than</b> a right angle.</p>"
        "<figure class='sn-fig'>" + kinds + "</figure>"
        "<figure class='sn-fig'>" + same +
        "<figcaption>These two angles are the same size. Longer arms do not make an angle bigger.</figcaption></figure>" +
        ex("Example", "At 5 o’clock, what angle do the hands of an analog clock make?",
           "A right angle is 3 hour marks (like 3 o’clock). 5 hour marks is wider.", "greater than a right angle") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at how far the angle turns, not the arm length"],
            ["Mixing up clockwise and anticlockwise", "Clockwise is the way clock hands go"],
            ["Mixing up a half turn and a quarter turn", "A half turn faces the opposite way; a quarter turn is a square corner"],
            ["Saying a tilted right angle is not a right angle", "Turn the page or use a checker: tilting does not change an angle"],
        ])
    )


FAQ = [
    {"q": "What is AC9M3M05 in the Australian Curriculum?",
     "a": "It is the Year 3 maths content description “identify angles as measures of turn and compare angles with right angles in everyday situations”. Students learn quarter, half, three-quarter and full turns and compare angles with a right angle."},
    {"q": "How do you explain a right angle to a Year 3 child?",
     "a": "A right angle is a square corner, like the corner of a book or a door. It is the angle you make with a quarter turn. Fold a piece of paper in half and in half again to make a right-angle checker."},
    {"q": "Do Year 3 students measure angles in degrees?",
     "a": "No. In Year 3 students compare angles with a right angle. Angle names such as acute and obtuse come in Year 4, and measuring in degrees with a protractor comes in Year 5."},
    {"q": "Are angles and turns in the Year 3 NAPLAN numeracy test?",
     "a": "NAPLAN numeracy is based on the Australian Curriculum, so questions about turns, right angles and compass directions can appear. Practising with clocks, compass points and everyday objects helps."},
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
    rnd = random.Random(3810)
    P = People(rnd)
    sets = [set_turns(rnd, P), set_quarter(rnd, P), set_rights(rnd, P), set_compare(rnd, P), set_problems(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "angles-as-turns", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles as Turns: Quarter, Half and Full Turns and Right Angles",
        "seo_title": "Year 3 Angles as Turns Worksheets: Right Angles, Quarter and Half Turns (Free, Australian Curriculum)",
        "short_title": "Angles as turns",
        "domain": "Measurement",
        "standard_code": "AC9M3M05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify angles as measures of turn and compare angles with right angles in everyday situations",
        "meta_desc": "Free Year 3 maths worksheets on angles as turns: quarter, half, three-quarter and full turns, clockwise and anticlockwise, right angles in shapes and everyday objects, and angles greater or less than a right angle. 100 questions with an answer key, following the Australian Curriculum (AC9M3M05) for NAPLAN practice.",
        "key_big": "An angle is a turn. A quarter turn makes a right angle: a square corner.",
        "key_sub": "A half turn is 2 right angles, a three-quarter turn is 3 and a full turn is 4. Compare every angle with a right angle: narrower is less, wider is greater. Arm length does not change an angle.",
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
        mark_large(u, "(four [a-z ]+ labelled A to D|angle P and angle Q|angles X, Y and Z)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
