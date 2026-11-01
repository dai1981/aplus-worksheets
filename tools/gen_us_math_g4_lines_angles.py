# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Lines, Angles and Shapes (4.G.A.1-2)
  python tools/gen_us_math_g4_lines_angles.py
HTML attributes use single quotes (no backslashes in the JSON).

Definitions used everywhere (as in the lesson):
  point          an exact spot, drawn as a dot, named by one capital letter
  line           straight, goes on forever both ways (arrows on both ends); line AB = line BA
  line segment   part of a line with 2 endpoints (dots); segment AB = segment BA
  ray            1 endpoint, goes on forever one way (one arrow); ray AB starts at A
  angle          two rays with the same endpoint (the vertex); angle ABC has its vertex B in the middle
  acute < right (exactly a square corner, 90 degrees) < obtuse < straight (180 degrees)
  parallel       lines that never meet; perpendicular: lines that meet at right angles;
                 intersecting: lines that cross. "Best word" questions ask for the most exact word.
  right / acute / obtuse triangle: has a right angle / all 3 angles acute / has an obtuse angle
Every drawing is exact and checked: right-angle squares are drawn only where the angle is exactly
90 degrees, every other angle is at least 10 degrees away from 90, parallel lines are exactly parallel,
and no point label touches a line, arrow, dot or another label.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#f3f7f2"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


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
    """Choices keep their order (A B C D, acute right obtuse straight, numbers)."""
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
    """Direction for an angle in degrees, counterclockwise on screen (SVG y goes down)."""
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

    def line(self, p, q, w=3, col=GREEN):
        self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' "
                       "stroke-linecap='round'/>" % (p[0], p[1], q[0], q[1], col, w))
        self._seg(p, q, w / 2.0)

    def arrow(self, tip, d, col=GREEN, L=12, hw=5.5):
        n = (-d[1], d[0])
        b = add(tip, d, -L)
        w1, w2 = add(b, n, hw), add(b, n, -hw)
        self.el.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (tip + w1 + w2 + (col,)))
        for a, c in ((tip, w1), (tip, w2), (w1, w2)):
            self._seg(a, c, 0.5)

    def stroke(self, p, q, start=False, end=False, w=3):
        """Straight stroke from p to q with optional arrowheads at either end."""
        d = norm(sub(q, p))
        a = add(p, d, 9) if start else p
        b = add(q, d, -9) if end else q
        self.line(a, b, w)
        if end:
            self.arrow(q, d)
        if start:
            self.arrow(p, (-d[0], -d[1]))

    def dot(self, p, r=4.5):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (p[0], p[1], r, INK))
        self._seg(p, p, r)

    def label(self, p, t, d, off=9, fs=16):
        d = norm(d)
        w, h = len(t) * fs * 0.68, fs * 0.72
        k = off + abs(d[0]) * w / 2 + abs(d[1]) * h / 2 + 2 * abs(d[0] * d[1]) * min(w, h) / 2
        c = add(p, d, k)
        box = (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)
        self.boxes.append(box)
        self.ext += [box[:2], box[2:]]
        self.el.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (c[0], c[1] + h / 2, fs, INK, t))

    def poly(self, pts, fill=FILL, w=3, closed=True):
        P = " ".join("%.1f,%.1f" % p for p in pts)
        if closed:
            self.el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                           % (P, fill, GREEN, w))
        else:
            self.el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' "
                           "stroke-linejoin='round'/>" % (P, GREEN, w))
        n = len(pts)
        for i in range(n if closed else n - 1):
            self._seg(pts[i], pts[(i + 1) % n], w / 2.0)

    def mark(self, pts, w=1.8):
        self.el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                       % (" ".join("%.1f,%.1f" % p for p in pts), INK, w))
        for i in range(len(pts) - 1):
            self._seg(pts[i], pts[i + 1], w / 2.0)

    def right_mark(self, v, u1, u2, k=10):
        q1 = add(v, u1, k)
        self.mark([q1, add(q1, u2, k), add(v, u2, k)])

    def arc(self, v, a1, a2, r):
        """Arc from direction a1 to a2 (degrees, counterclockwise)."""
        n = max(6, int(abs(a2 - a1) / 6))
        self.mark([add(v, dirv(a1 + (a2 - a1) * i / n), r) for i in range(n + 1)], w=1.8)

    def render(self):
        for b in self.boxes:
            for p, q, hw in self.segs:
                assert not seg_hits_box(p, q, b, hw + 1.5), ("label touches a stroke", b, p, q)
        for i, b in enumerate(self.boxes):
            for c in self.boxes[i + 1:]:
                assert b[2] + 2 < c[0] or c[2] + 2 < b[0] or b[3] + 2 < c[1] or c[3] + 2 < b[1], "labels overlap"
        xs, ys = [p[0] for p in self.ext], [p[1] for p in self.ext]
        return "".join(self.el), (min(xs), min(ys), max(xs), max(ys))

    def svg(self, label, pad=5, size=None):
        body, bb = self.render()
        if size:
            W, H = size
            assert bb[0] >= 0 and bb[1] >= 0 and bb[2] <= W and bb[3] <= H, (label, bb, size)
            return svg_wrap(W, H, body, label)
        W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
        if W == H:
            W += 1                                     # keep figures out of the larger 'square' print size
        dx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
        dy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
        return svg_wrap(W, H, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body), label)


def up_normal(d, side=1):
    """Normal to direction d pointing up (or left for a vertical direction); side=-1 flips it."""
    n = (-d[1], d[0])
    if n[1] > 1e-9 or (abs(n[1]) <= 1e-9 and n[0] > 0):
        n = (-n[0], -n[1])
    return n if side == 1 else (-n[0], -n[1])


def basic(kind, rot=0, names=("A", "B"), L=96, ext=32, side=1, fs=16):
    """point, line, segment or ray. names[0] is the first point (the endpoint of a ray)."""
    F = Fig()
    d = dirv(rot)
    A = (0.0, 0.0)
    B = add(A, d, L)
    n = up_normal(d, side)
    if kind == "point":
        F.dot(A)
        F.label(A, names[0], (0.7, -0.7), fs=fs)
        return F
    if kind == "segment":
        F.line(A, B)
    elif kind == "ray":
        F.stroke(A, add(B, d, ext), end=True)
    elif kind == "line":
        F.stroke(add(A, d, -ext), add(B, d, ext), start=True, end=True)
    F.dot(A)
    F.dot(B)
    if names:
        F.label(A, names[0], n, fs=fs)
        F.label(B, names[1], n, fs=fs)
    return F


def angle_fig(deg, rot=0, L=80, names=None, F=None, at=(0.0, 0.0), fs=16, arrows=True):
    """Angle made of two rays from vertex `at`: one at direction rot, one at rot + deg.
    Right angles get a square mark, other angles an arc. names = (on ray 1, vertex, on ray 2)."""
    F = F or Fig()
    V = at
    d1, d2 = dirv(rot), dirv(rot + deg)
    F.stroke(V, add(V, d1, L), end=arrows)
    F.stroke(V, add(V, d2, L), end=arrows)
    if abs(deg - 90) < 1e-9:
        F.right_mark(V, d1, d2, 12)
    else:
        assert abs(deg - 90) >= 10, deg
        F.arc(V, rot, rot + deg, 26 if deg < 50 else 20 if deg < 150 else 16)
    F.dot(V)
    if names:
        P1, P2 = add(V, d1, L * 0.62), add(V, d2, L * 0.62)
        F.dot(P1)
        F.dot(P2)
        F.label(P1, names[0], dirv(rot - 90), fs=fs)
        F.label(P2, names[2], dirv(rot + deg + 90), fs=fs)
        F.label(V, names[1], dirv(rot + deg / 2.0 + 180), off=8, fs=fs)
    return F


def clip_line(p, d, W, H, m=3):
    """Ends of the line through p with direction d inside the box [m, W-m] x [m, H-m]."""
    lo, hi = -1e9, 1e9
    for k, (a, b) in enumerate(((m, W - m), (m, H - m))):
        if abs(d[k]) < 1e-12:
            assert a <= p[k] <= b
            continue
        t1, t2 = (a - p[k]) / d[k], (b - p[k]) / d[k]
        lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
    assert hi - lo > 40
    return add(p, d, lo), add(p, d, hi)


def meet(p1, d1, p2, d2):
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
    return add(p1, d1, t)


def lines_fig(specs, W=190, H=92, label="two lines", names=(), arrows=True):
    """specs: (point, deg) for each line, drawn across a W x H box with arrows on both ends.
    Perpendicular lines get a right-angle mark where they cross. names: (line index, distance, letter, label dir)."""
    F = Fig()
    ends = []
    for p, deg in specs:
        d = dirv(deg)
        a, b = clip_line(p, d, W, H)
        ends.append((a, b))
        F.stroke(a, b, start=arrows, end=arrows)
    for i in range(len(specs)):
        for j in range(i + 1, len(specs)):
            (p1, g1), (p2, g2) = specs[i], specs[j]
            d1, d2 = dirv(g1), dirv(g2)
            diff = dir_diff(d1, d2)
            x = meet(p1, d1, p2, d2)
            if diff < 1e-9:
                # truly parallel: keep them clearly apart
                gap = abs((p2[0] - p1[0]) * d1[1] - (p2[1] - p1[1]) * d1[0])
                assert gap >= 24, ("parallel lines too close", gap)
                continue
            assert diff >= 8, ("almost parallel", diff)
            inside = 0 <= x[0] <= W and 0 <= x[1] <= H
            if abs(diff - 90) < 1e-9:
                assert inside
                F.right_mark(x, d1, d2, 11)
            else:
                assert abs(diff - 90) >= 15, ("almost perpendicular", diff)
                if not inside:
                    # they meet off the picture: make sure the gap is easy to see
                    assert min(abs(x[0] - W / 2.0), abs(x[1] - H / 2.0)) > 0, x
    for li, dist, t, dd in names:
        p, deg = specs[li]
        q = add(p, dirv(deg), dist)
        F.dot(q)
        F.label(q, t, dd)
    return F.svg(label, size=(W, H))


# ------------------------------------------------------------ letters made of line segments
LETTERS = {
    "H": [((0, 0), (0, 60)), ((40, 0), (40, 60)), ((0, 30), (40, 30))],
    "T": [((0, 0), (44, 0)), ((22, 0), (22, 60))],
    "Z": [((0, 0), (40, 0)), ((40, 0), (0, 60)), ((0, 60), (40, 60))],
    "V": [((0, 0), (20, 60)), ((20, 60), (40, 0))],
    "L": [((0, 0), (0, 60)), ((0, 60), (36, 60))],
    "E": [((0, 0), (0, 60)), ((0, 0), (36, 0)), ((0, 30), (30, 30)), ((0, 60), (36, 60))],
    "F": [((0, 0), (0, 60)), ((0, 0), (36, 0)), ((0, 30), (30, 30))],
    "N": [((0, 60), (0, 0)), ((0, 0), (40, 60)), ((40, 60), (40, 0))],
    "X": [((0, 0), (40, 60)), ((40, 0), (0, 60))],
    "A": [((0, 60), (20, 0)), ((20, 0), (40, 60)), ((9.33, 32), (30.67, 32))],
}


def letter_facts(ch):
    st = LETTERS[ch]
    par = perp = False
    for i in range(len(st)):
        for j in range(i + 1, len(st)):
            a, b = sub(st[i][1], st[i][0]), sub(st[j][1], st[j][0])
            dd = dir_diff(a, b)
            if dd < 1e-9:
                par = True
            elif abs(dd - 90) < 1e-9:
                perp = True
            else:
                assert dd >= 15 and abs(dd - 90) >= 15, (ch, dd)
    return par, perp


def letters_svg(chars, label="letters made of line segments"):
    cw = 66
    F = Fig()
    for k, ch in enumerate(chars):
        st = LETTERS[ch]
        xs = [p[0] for s in st for p in s]
        ox = k * cw + (cw - max(xs)) / 2.0
        for a, b in st:
            F.line((ox + a[0], 6 + a[1]), (ox + b[0], 6 + b[1]), w=6)
    return F.svg(label, size=(cw * len(chars), 72))


# ------------------------------------------------------------ street map
def map_svg():
    W, H = 280, 132
    s = ["<rect x='1' y='1' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (W - 2, H - 2, FILL2, GRAY)]
    road = "stroke='%s' stroke-width='5' stroke-linecap='butt'" % GREEN
    s.append("<line x1='2' y1='30' x2='%d' y2='30' %s/>" % (W - 2, road))          # Oak St
    s.append("<line x1='2' y1='100' x2='%d' y2='100' %s/>" % (W - 2, road))        # Elm St
    s.append("<line x1='70' y1='2' x2='70' y2='%d' %s/>" % (H - 2, road))          # Main St
    # Lake Rd: through (190, 65) at 60 degrees
    d = dirv(60)
    a, b = clip_line((190, 65), d, W, H, m=2)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (a + b + (road,)))
    t = "<text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='%s' text-anchor='middle'%s>%s</text>"
    s.append(t % (130, 22, INK, "", "Oak St"))
    s.append(t % (130, 118, INK, "", "Elm St"))
    s.append(t % (58, 65, INK, " transform='rotate(-90 58 65)'", "Main St"))
    c = add((190, 65), dirv(-30), 14)
    s.append(t % (c[0], c[1] + 5, INK, " transform='rotate(-60 %.1f %.1f)'" % (c[0], c[1]), "Lake Rd"))
    return svg_wrap(W, H, "".join(s), "street map")


# ------------------------------------------------------------ polygons
def angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        u = norm(sub(pts[i - 1], pts[i]))
        v = norm(sub(pts[(i + 1) % n], pts[i]))
        out.append(math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1])))))
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "shape must be convex"
    return out


def pfacts(pts):
    n = len(pts)
    A = angles(pts)
    sides = [sub(pts[(i + 1) % n], pts[i]) for i in range(n)]
    par, perp = [], []
    for i in range(n):
        for j in range(i + 1, n):
            dd = dir_diff(sides[i], sides[j])
            if dd < 1e-6:
                par.append((i, j))
            elif abs(dd - 90) < 1e-6:
                perp.append((i, j))
            else:
                assert dd >= 8 and abs(dd - 90) >= 8, ("sides look parallel or perpendicular", dd)
    for a in A:
        assert abs(a - 90) < 1e-6 or abs(a - 90) >= 10, ("angle looks like a right angle", A)
    return {"n": n, "angles": A, "right": sum(abs(a - 90) < 1e-6 for a in A),
            "acute": sum(a < 90 - 1e-6 for a in A), "obtuse": sum(a > 90 + 1e-6 for a in A),
            "par": len(par), "perp": len(perp) > 0}


def tri_ang(a, b, base=120):
    """Triangle with angle a at the left end of the base and angle b at the right end."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    return [(0.0, 0.0), (float(base), 0.0), add((0.0, 0.0), dirv(a), side)]


def regular(n, r=60, start=90):
    return [add((0, 0), dirv(start + 360.0 * i / n), r) for i in range(n)]


def rect(a, b):
    return [(0, 0), (a, 0), (a, b), (0, b)]


def para(a, b, deg):
    return [(0, 0), (a, 0), add((a, 0), dirv(deg), b), add((0, 0), dirv(deg), b)]


def rhombus(deg, s=100):
    return para(s, s, deg)


def trap(bottom, top, h, off):
    return [(0, h), (bottom, h), (off + top, 0), (off, 0)]


def rtrap(bottom, top, h):
    return [(0, h), (bottom, h), (top, 0), (0, 0)]


SQUARE = rect(100, 100)
RECT = rect(150, 85)
PARA = para(150, 80, 60)
RHOMB = rhombus(65)
TRAP = trap(150, 70, 80, 40)
RTRAP = rtrap(150, 70, 90)
KITE = [(0, 0), (50, 35), (0, 150), (-50, 35)]
PENT = regular(5)
HEX = regular(6, start=0)
HOUSE = [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)]
T_ACUTE = tri_ang(60, 70)
T_ACUTE2 = tri_ang(75, 55)
T_ACUTE3 = tri_ang(65, 62)
T_RIGHT = tri_ang(90, 35)
T_RIGHT2 = tri_ang(90, 50)
T_RIGHT3 = tri_ang(45, 45)
T_OBT = tri_ang(30, 30)
T_OBT2 = tri_ang(25, 40)
T_OBT3 = tri_ang(125, 30)


def tri_kind(pts):
    f = pfacts(pts)
    assert f["n"] == 3
    if f["right"]:
        return "right"
    if f["obtuse"]:
        assert max(f["angles"]) >= 110
        return "obtuse"
    assert max(f["angles"]) <= 78, f["angles"]
    return "acute"


def placed(pts, rot, bw, bh):
    P = [rot_pt(p, rot) for p in pts]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [((p[0] - mx) * k, (p[1] - my) * k) for p in P]


def shape_fig(pts, rot=0, bw=130, bh=80, sw=3, F=None, closed=True):
    F = F or Fig()
    P = placed(pts, rot, bw, bh)
    F.poly(P, fill=FILL if closed else "none", w=sw, closed=closed)
    if closed:
        f = pfacts(P)
        n = len(P)
        L = [math.hypot(*sub(P[(i + 1) % n], P[i])) for i in range(n)]
        for i, a in enumerate(f["angles"]):
            if abs(a - 90) < 1e-6:
                k = min(11, 0.2 * min(L[i - 1], L[i]))
                F.right_mark(P[i], norm(sub(P[i - 1], P[i])), norm(sub(P[(i + 1) % n], P[i])), k)
    return F


def shape_svg(pts, rot=0, bw=130, bh=80, label="shape"):
    return shape_fig(pts, rot, bw, bh).svg(label)


def open_tri():
    """Three sides of a triangle that do not close (gap at the bottom left)."""
    P = tri_ang(60, 70)
    gap = add(P[0], norm(sub(P[1], P[0])), 26)
    return [gap, P[1], P[2], P[0]]


CUT_TRI = [(0, 72), (130, 72), (54.17, 30), (0, 30)]          # 4 sides: a right triangle with its top corner cut off


# ------------------------------------------------------------ composite pictures
CELL = 118


def grid_svg(figs, label="four pictures labeled A to D"):
    """2 x 2 grid of Figs labeled A-D. Square picture (printed large)."""
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


def strip_svg(items, cw=128, label="figures"):
    """Lesson picture: a row of Figs with a caption under each. items: (Fig, caption)."""
    rend = [F.render() for F, _ in items]
    top = max(bb[3] - bb[1] for _, bb in rend) + 8
    s = []
    for k, ((body, bb), (_, cap)) in enumerate(zip(rend, items)):
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        assert bw <= cw - 6, (cap, bw)
        dx = k * cw + (cw - bw) / 2 - bb[0]
        dy = (top - bh) / 2 - bb[1]
        s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body))
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (k * cw + cw / 2.0, top + 16, INK, cap))
    return svg_wrap(cw * len(items), int(top + 24), "".join(s), label)


def pair_lines_fig(specs, W=120, H=80):
    """A small Fig (for strips) with lines across a W x H box."""
    F = Fig()
    for p, deg in specs:
        a, b = clip_line(p, dirv(deg), W, H)
        F.stroke(a, b, start=True, end=True)
    (p1, g1), (p2, g2) = specs
    if abs(dir_diff(dirv(g1), dirv(g2)) - 90) < 1e-9:
        F.right_mark(meet(p1, dirv(g1), p2, dirv(g2)), dirv(g1), dirv(g2), 10)
    F.ext += [(0, 0), (W, H)]
    return F


# ------------------------------------------------------------ text
DEF = {
    "point": "A point is an exact spot. It is drawn as a dot and named with one capital letter.",
    "line": "A line is straight and goes on forever in both directions. The arrows on both ends show this.",
    "line segment": "A line segment is part of a line. It has 2 endpoints, so it does not go on forever.",
    "ray": "A ray has 1 endpoint and goes on forever in one direction. The arrow shows the direction.",
    "angle": "An angle is two rays that share the same endpoint, called the vertex.",
}
ORDER = ["point", "line", "line segment", "ray", "angle"]
CONF = {"point": ["line", "line segment", "ray"], "line": ["line segment", "ray", "angle"],
        "line segment": ["line", "ray", "point"], "ray": ["line", "line segment", "angle"],
        "angle": ["ray", "line", "line segment"]}
TYPES = ["acute", "right", "obtuse", "straight"]
TYPE_E = {
    "acute": "The opening is smaller than a square corner, so it is an acute angle.",
    "right": "The small square shows a square corner, so it is a right angle (90 degrees).",
    "obtuse": "The opening is wider than a square corner but not a straight line, so it is an obtuse angle.",
    "straight": "The two rays point in opposite directions and make a straight line. That is a straight angle (180 degrees), the size of 2 right angles.",
}
TT = ["acute triangle", "right triangle", "obtuse triangle", "not a triangle"]
TRI_E = {
    "acute": "All 3 angles are smaller than a right angle, so it is an acute triangle.",
    "right": "The small square shows one right angle, so it is a right triangle. The other 2 angles are acute.",
    "obtuse": "One angle is wider than a right angle, so it is an obtuse triangle. The other 2 angles are acute.",
}


def kind_of(deg):
    return "acute" if deg < 90 else "right" if deg == 90 else "obtuse" if deg < 180 else "straight"


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def pick_grid(q, figs, why, pos, label="four pictures labeled A to D"):
    """figs[0] is the right answer. It goes to position p; the others keep their order."""
    p = pos.next()
    cells = figs[1:]
    cells.insert(p, figs[0])
    return mcq_fixed(fig(grid_svg(cells, label)) + q, ["A", "B", "C", "D"], "ABCD"[p], "Picture %s %s" % ("ABCD"[p], why))


# ------------------------------------------------------------ set 1: points, lines, segments, rays
def set_figures(rnd):
    its = []
    pos = Pos(rnd)
    pics = [
        ("point", basic("point", names=("K",)), "There is only a dot with a letter, and no length."),
        ("line", basic("line", 0, ("A", "B")), "It has arrows on both ends, so it goes on forever both ways."),
        ("line", basic("line", 32, ("R", "S")), "It has arrows on both ends. Tilting a line does not change what it is."),
        ("line segment", basic("segment", -15, ("C", "D"), L=130), "It stops at 2 endpoints and has no arrows."),
        ("line segment", basic("segment", 90, ("M", "N"), L=80), "It has 2 endpoints and no arrows. Standing up does not change what it is."),
        ("ray", basic("ray", 0, ("E", "F")), "It starts at one endpoint and has one arrow."),
        ("ray", basic("ray", 205, ("G", "H")), "It has one endpoint, G, and one arrow. A ray can point in any direction."),
        ("angle", angle_fig(70, 15, names=None), "Two rays start at the same point, the vertex."),
    ]
    for ans, F, why in pics:
        ch = sorted([ans] + CONF[ans], key=ORDER.index)
        its.append(mcq_fixed(fig(F.svg(ans)) + "What is this figure called?", ch, ans, why + " " + DEF[ans]))
    names = [
        (basic("ray", 0, ("P", "Q")), "ray PQ", ["ray QP", "line PQ", "line segment PQ"],
         "It has one endpoint and one arrow, so it is a ray. Name a ray with its endpoint first: P, then Q. Ray QP would start at Q."),
        (basic("ray", 180, ("L", "K")), "ray LK", ["ray KL", "line KL", "line segment KL"],
         "The endpoint is L, on the right, and the ray goes left through K. Name a ray with its endpoint first, even if you read the letters the other way: ray LK."),
        (basic("ray", 90, ("Y", "X"), L=62, ext=26), "ray YX", ["ray XY", "line XY", "line segment XY"],
         "The endpoint is Y at the bottom, and the arrow goes up through X. The endpoint comes first: ray YX."),
    ]
    for F, ans, wrong, e in names:
        its.append(mcq(fig(F.svg("ray with two labeled points")) + "What is the name of this figure?", ans, wrong, e, rnd))
    its.append(mcq(fig(basic("segment", 20, ("C", "D"), L=120).svg("line segment CD")) + "Which name is correct for this figure?",
                  "line segment DC", ["ray CD", "ray DC", "line CD"],
                  "It has 2 endpoints and no arrows, so it is a line segment. You can name it with its endpoints in either order: CD or DC.", rnd))
    its.append(mcq(fig(basic("line", -20, ("T", "U")).svg("line TU")) + "Which name is correct for this figure?",
                   "line UT", ["ray TU", "line segment TU", "ray UT"],
                   "Arrows on both ends make it a line. A line can be named with its 2 points in either order: TU or UT.", rnd))
    g = dict(L=50, ext=22, fs=15)
    its.append(pick_grid("Which picture shows ray PQ?",
                         [basic("ray", 15, ("P", "Q"), **g), basic("ray", 195, ("Q", "P"), **g),
                          basic("line", 15, ("P", "Q"), **g), basic("segment", 15, ("P", "Q"), L=74, fs=15)],
                         "shows a ray that starts at endpoint P and goes on forever through Q. One picture is ray QP (it starts at Q), one is a line and one is a line segment.", pos))
    its.append(pick_grid("Which picture shows line segment MN?",
                         [basic("segment", -15, ("M", "N"), L=74, fs=15), basic("line", -15, ("M", "N"), **g),
                          basic("ray", -15, ("M", "N"), **g), basic("ray", 165, ("N", "M"), **g)],
                         "has 2 endpoints, M and N, and no arrows. The others go on forever: a line and two rays.", pos))
    its.append(mcq_num("How many endpoints does a ray have?", 1, [0, 2, 3],
                       "A ray has 1 endpoint where it starts. At the other end it goes on forever, so there is no second endpoint."))
    its.append(mcq_num("How many endpoints does a line have?", 0, [1, 2, 3],
                       "A line goes on forever in both directions, so it has no endpoints. The points named on a line are not endpoints."))
    its.append(mcq("Are ray AB and ray BA the same ray?", "No, they start at different points",
                   ["Yes, they use the same 2 points", "Yes, either order is fine", "No, ray BA is longer"],
                   "Ray AB starts at A and goes through B. Ray BA starts at B and goes through A, the other way. "
                   "Only lines and line segments can be named in either order.", rnd))
    its.append(mcq("A flashlight beam starts at the flashlight and goes straight out in one direction. Which figure is it most like?",
                   "ray", ["line", "line segment", "point"],
                   "It has a starting point (the flashlight) and goes on in one direction, like a ray.", rnd))
    its.append(mcq("Which figure is most like the edge of a ruler?", "line segment", ["line", "ray", "point"],
                   "The edge is straight and stops at both ends. It has 2 endpoints, so it is like a line segment.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Points, lines, line segments and rays", "items": its}


# ------------------------------------------------------------ set 2: angles
def set_angles(rnd):
    its = []
    pos = Pos(rnd)
    for deg, rot in [(35, 10), (60, 105), (70, -30), (90, 0), (90, 30), (90, -115), (115, 20), (140, 200), (180, 15)]:
        k = kind_of(deg)
        e = TYPE_E[k]
        if k == "right" and rot % 90:
            e += " Turning an angle does not change its size."
        its.append(mcq_fixed(fig(angle_fig(deg, rot).svg(k + " angle")) + "What kind of angle is this?", TYPES, k, e))
    its.append(mcq(fig(angle_fig(65, 10, names=("A", "B", "C")).svg("angle with points A, B and C")) + "What is a name for this angle?",
                   "angle ABC", ["angle BAC", "angle ACB", "angle BCA"],
                   "The vertex is B, where the two rays meet. The vertex letter always goes in the middle: angle ABC (or angle CBA).", rnd))
    its.append(mcq("Which point is the vertex of angle RST?", "point S", ["point R", "point T", "line RT"],
                   "In an angle's name, the middle letter is the vertex. In angle RST, the middle letter is S.", rnd))
    its.append(pick_grid("Which angle is obtuse?",
                         [angle_fig(125, -40, L=58), angle_fig(50, 20, L=62), angle_fig(90, 20, L=56), angle_fig(180, 0, L=44)],
                         "shows an angle wider than a right angle but less than a straight line. The straight line is a straight angle, not an obtuse angle.", pos,
                         "four angles labeled A to D"))
    its.append(pick_grid("Which angle is acute?",
                         [angle_fig(40, 70, L=64), angle_fig(90, 45, L=56), angle_fig(110, 10, L=56), angle_fig(150, -50, L=54)],
                         "shows an angle smaller than a square corner. The others are a right angle and two obtuse angles.", pos,
                         "four angles labeled A to D"))
    its.append(mcq(fig(angle_fig(90, 40).svg("tilted right angle")) + "Sam says this angle is acute because it is tilted. Is he right?",
                   "No, it is a right angle", ["Yes, tilted angles are acute", "Yes, it looks small", "No, it is obtuse"],
                   "The small square shows a square corner, so it is a right angle. Turning an angle does not change its size.", rnd))
    clocks = [("3:00", 90, "right", "At 3:00 the hands make a square corner: a quarter turn, 90 degrees."),
              ("2:00", 60, "acute", "At 2:00 the hands are 2 hour marks apart. Each hour mark is 30 degrees, so the angle is 60 degrees, smaller than a right angle."),
              ("4:00", 120, "obtuse", "At 4:00 the hands are 4 hour marks apart: 4 × 30 = 120 degrees. That is more than a right angle but less than a straight angle."),
              ("6:00", 180, "straight", "At 6:00 one hand points straight up and the other straight down. Together they make a straight line: 180 degrees.")]
    for t, deg, k, e in clocks:
        its.append(mcq_fixed("A clock shows %s. What kind of angle do the hour hand and the minute hand make?" % t, TYPES, k, e))
    its.append(mcq_num("How many right angles make one straight angle?", 2, [1, 3, 4],
                       "A right angle is 90 degrees and a straight angle is 180 degrees. 90 + 90 = 180, so 2 right angles make a straight angle."))
    its.append(mcq_fixed("Lena opens her laptop. The screen leans back past a square corner, but it is not flat. "
                         "What kind of angle do the screen and the keyboard make?", TYPES, "obtuse",
                         "The angle is wider than a right angle (a square corner) but less than a straight angle (flat), so it is obtuse."))
    assert len(its) == 20, len(its)
    return {"title": "Acute, right, obtuse and straight angles", "items": its}


# ------------------------------------------------------------ set 3: parallel and perpendicular
LW = ["parallel", "perpendicular", "intersecting", "line segments"]


def set_parallel(rnd):
    its = []
    q = "What is the best word for these two lines?"
    pairs = [
        ([((10, 28), 0), ((10, 66), 0)], "parallel",
         "The lines stay the same distance apart and never meet, so they are parallel. The arrows show they are lines, not line segments."),
        ([((60, 46), 120), ((115, 46), 120)], "parallel",
         "The lines tilt the same way and stay the same distance apart. They will never meet, so they are parallel."),
        ([((95, 46), 25), ((95, 46), 115)], "perpendicular",
         "The lines cross and make right angles (see the small square), so they are perpendicular. "
         "They also intersect, but perpendicular is the best word because it tells more."),
        ([((95, 46), 15), ((95, 46), 70)], "intersecting",
         "The lines cross, but not at a right angle. They are intersecting, not perpendicular."),
        ([((5, 20), -4), ((5, 76), 7)], "intersecting",
         "They do not cross on the page, but they get closer and closer. If you keep going to the right, they will meet. "
         "Parallel lines stay the same distance apart."),
    ]
    for specs, ans, e in pairs:
        its.append(mcq_fixed(fig(lines_fig(specs, label="two lines")) + q, LW, ans, e))
    its.append(mcq(fig(lines_fig([((5, 70), 6), ((5, 22), -3)], label="two lines that do not cross on the page")) +
                   "Tom says these two lines are parallel because they do not cross. Is he right?",
                   "No, they would cross", ["Yes, they do not touch", "Yes, both have arrows", "No, they are perpendicular"],
                   "The gap between the lines gets smaller to the right, so the lines would meet if we drew more of them. "
                   "Parallel lines stay the same distance apart everywhere.", rnd))
    # letters
    letter_qs = [
        ("parallel line segments but no perpendicular line segments", lambda f: f == (True, False), ["Z", "H", "T", "V"],
         "Z has a top and a bottom that are parallel, and its slanted middle is not at a right angle to them."),
        ("perpendicular line segments but no parallel line segments", lambda f: f == (False, True), ["L", "E", "N", "H"],
         "L has 2 line segments that meet at a right angle, and nothing parallel."),
        ("both parallel and perpendicular line segments", lambda f: f == (True, True), ["F", "T", "Z", "A"],
         "F has 2 parallel line segments going across, and both are perpendicular to the line segment going down."),
        ("no parallel and no perpendicular line segments", lambda f: f == (False, False), ["V", "H", "T", "E"],
         "V has 2 slanted line segments that meet but not at a right angle, and they are not parallel."),
    ]
    pos = Pos(rnd)
    for what, test, letters, why in letter_qs:
        assert [test(letter_facts(c)) for c in letters] == [True, False, False, False], letters
        p = pos.next()
        row = letters[1:]
        row.insert(p, letters[0])
        its.append(mcq_fixed(fig(letters_svg(row)) + "Which letter has %s?" % what, row, letters[0], why))
    # street map
    m = fig(map_svg())
    its.append(mcq(m + "Which street is parallel to Oak St?", "Elm St", ["Main St", "Lake Rd", "no street"],
                   "Oak St and Elm St both go straight across and stay the same distance apart, so they are parallel. "
                   "Main St and Lake Rd cross Oak St.", rnd))
    its.append(mcq(m + "Which street is perpendicular to Elm St?", "Main St", ["Oak St", "Lake Rd", "no street"],
                   "Main St crosses Elm St at a right angle (a square corner). Lake Rd crosses it too, but at a slant. "
                   "Oak St is parallel to Elm St.", rnd))
    its.append(mcq(m + "Lake Rd crosses Oak St. Are these two streets perpendicular?", "No, not a right angle",
                   ["Yes, they cross", "No, they are parallel", "Yes, both are straight"],
                   "Lake Rd crosses at a slant, so the angles are not right angles. Crossing is not enough: perpendicular lines must meet at right angles.", rnd))
    its.append(mcq(m + "Main St and Lake Rd do not cross on this map. Are they parallel?", "No, they would cross",
                   ["Yes, they do not cross here", "Yes, both are long", "No, they are perpendicular"],
                   "Main St goes straight up and down, but Lake Rd slants. If both streets kept going down past the map, they would meet.", rnd))
    # three named lines
    tl = [((8, 30), 0), ((8, 86), 0), ((150, 58), 90)]
    nm = [(0, 30, "A", (0, -1)), (0, 82, "B", (0, -1)), (1, 30, "C", (0, 1)), (1, 82, "D", (0, 1)),
          (2, 28, "E", (-1, -1)), (2, -28, "F", (-1, 1))]
    tf = fig(lines_fig(tl, W=196, H=116, label="three lines", names=nm))
    its.append(mcq(tf + "Which line is perpendicular to line AB?", "line EF", ["line CD", "line AE", "none of them"],
                   "Line EF crosses line AB at a right angle (see the small square). Line CD is parallel to line AB, "
                   "and line AE is just another name for line AB, because A and E are both on it.", rnd))
    its.append(mcq(tf + "Which line is parallel to line CD?", "line AB", ["line EF", "line CF", "none of them"],
                   "Line AB and line CD go the same way and never meet, so they are parallel. Line EF is perpendicular to both, "
                   "and line CF is the same line as line CD.", rnd))
    its.append(mcq("The two rails of a straight train track never meet. Which word describes them?", "parallel",
                   ["perpendicular", "intersecting", "rays"],
                   "The rails stay the same distance apart and never meet, like parallel lines.", rnd))
    its.append(mcq("Perpendicular lines meet to make what kind of angles?", "right angles",
                   ["acute angles", "obtuse angles", "straight angles"],
                   "Perpendicular lines cross at a square corner, so they make right angles.", rnd))
    its.append(mcq_num("Two lines cross, and one of the angles they make is a right angle. How many right angles do they make in all?", 4, [1, 2, 3],
                       "When two lines cross they make 4 angles. If one is a right angle, all 4 are right angles: the lines are perpendicular."))
    its.append(mcq("Can two parallel lines ever cross?", "No, never", ["Yes, if they are long", "Yes, at a right angle", "Only if they tilt"],
                   "Parallel lines stay the same distance apart forever, so they never cross, no matter how far they go.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallel, perpendicular and intersecting lines", "items": its}


# ------------------------------------------------------------ set 4: triangles
def set_triangles(rnd):
    its = []
    pos = Pos(rnd)
    q = "What kind of triangle is this?"
    for pts, rot in [(T_ACUTE, 0), (T_ACUTE2, 25), (T_RIGHT, 0), (T_RIGHT2, 140), (T_ACUTE3, 200), (T_OBT, 0), (T_OBT2, -35)]:
        k = tri_kind(pts)
        e = TRI_E[k]
        if k == "right" and rot:
            e += " Turning a triangle does not change its angles."
        its.append(mcq_fixed(fig(shape_svg(pts, rot, 130, 80, label=k + " triangle")) + q, TT, k + " triangle", e))
    its.append(mcq_fixed(fig(shape_fig(open_tri(), 0, 130, 80, closed=False).svg("3 line segments with a gap")) + q, TT, "not a triangle",
                         "The sides do not meet at the bottom left, so the shape is not closed. A triangle is a closed shape with 3 sides."))
    its.append(mcq_fixed(fig(shape_svg(CUT_TRI, 0, 130, 75, label="shape with 4 sides")) + q, TT, "not a triangle",
                         "Count the sides: there are 4, because the top corner is cut off. A triangle has exactly 3 sides."))
    its.append(mcq_fixed("A triangle has angles of 90°, 30° and 60°. What kind of triangle is it?", TT, "right triangle",
                         "It has a 90° angle, which is a right angle, so it is a right triangle."))
    its.append(mcq_fixed("A triangle has angles of 110°, 40° and 30°. Two of its angles are acute. What kind of triangle is it?", TT,
                         "obtuse triangle",
                         "110° is more than 90°, so it is obtuse. A triangle is named by its largest angle. Every triangle has at least 2 acute angles, so that does not make it acute."))
    its.append(pick_grid("Which is a right triangle?",
                         [shape_fig(T_RIGHT2, 200, 74, 74, sw=2.6), shape_fig(T_ACUTE3, 10, 74, 74, sw=2.6),
                          shape_fig(T_OBT3, 0, 80, 60, sw=2.6), shape_fig(T_ACUTE, 180, 74, 70, sw=2.6)],
                         "has a right angle (the small square). The others have no right angle.", pos, "four triangles labeled A to D"))
    its.append(pick_grid("Which is an obtuse triangle?",
                         [shape_fig(T_OBT2, 60, 74, 74, sw=2.6), shape_fig(T_RIGHT, 0, 80, 64, sw=2.6),
                          shape_fig(T_ACUTE2, 0, 74, 70, sw=2.6), shape_fig(T_ACUTE3, 150, 74, 74, sw=2.6)],
                         "has one angle wider than a right angle. The others are a right triangle and two acute triangles.", pos,
                         "four triangles labeled A to D"))
    its.append(mcq_num(fig(shape_svg(T_RIGHT, 30, 120, 80, label="right triangle")) + "How many acute angles does this triangle have?",
                       2, [0, 1, 3], "One angle is a right angle (the square). The other 2 angles are smaller, so they are acute."))
    its.append(mcq_num(fig(shape_svg(T_OBT3, 0, 130, 70, label="obtuse triangle")) + "How many obtuse angles does this triangle have?",
                       1, [0, 2, 3], "Only the angle where the bottom side meets the left side is wider than a right angle. A triangle can never have more than 1 obtuse angle."))
    its.append(mcq(fig(shape_svg(T_OBT, 0, 140, 60, label="obtuse triangle")) +
                   "Ana says this is an acute triangle because 2 of its angles are acute. Is she right?",
                   "No, it has an obtuse angle", ["Yes, most angles are acute", "Yes, it is a wide triangle", "No, it is a right triangle"],
                   "The top angle is wider than a right angle, so it is an obtuse triangle. Every triangle has at least 2 acute angles, "
                   "so look at the largest angle.", rnd))
    its.append(mcq("Can a triangle have 2 right angles?", "No, the sides would not meet",
                   ["Yes, like a rectangle", "Yes, if it is very big", "Only if it is tilted"],
                   "If 2 angles were right angles, the 2 sides going up from them would be parallel and never meet. So the shape could not close.", rnd))
    its.append(mcq("Can a triangle have 2 obtuse angles?", "No, the sides would not meet",
                   ["Yes, if it is flat", "Yes, if it is very big", "Only if it is tilted"],
                   "Two obtuse angles would make the 2 sides spread apart, so they could never meet to close the triangle.", rnd))
    its.append(mcq_num("Every triangle has at least how many acute angles?", 2, [0, 1, 3],
                       "A triangle can have at most 1 right angle or 1 obtuse angle. So at least 2 of its 3 angles are always acute."))
    its.append(mcq("A ramp leans against a wall. The wall stands straight up from the flat ground. The ground, the wall and the ramp make a triangle. "
                   "What kind of triangle is it?", "right triangle", ["acute triangle", "obtuse triangle", "not a triangle"],
                   "The wall meets the ground at a square corner, a right angle. A triangle with a right angle is a right triangle.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Right, acute and obtuse triangles", "items": its}


# ------------------------------------------------------------ set 5: classify shapes
def set_classify(rnd, P):
    its = []
    pos = Pos(rnd)
    g = dict(bw=78, bh=74, sw=2.6)

    def grid(q, shapes, test, why):
        for k, (pts, rot) in enumerate(shapes):
            assert test(pfacts(placed(pts, rot, 78, 74))) == (k == 0), (q, k)
        its.append(pick_grid(q, [shape_fig(pts, rot, **g) for pts, rot in shapes], why, pos, "four shapes labeled A to D"))

    grid("Which shape has exactly one pair of parallel sides?", [(TRAP, 0), (PARA, 0), (RECT, 20), (T_RIGHT, 0)],
         lambda f: f["par"] == 1, "is a trapezoid: only its top and bottom are parallel. The parallelogram and rectangle have 2 pairs, and the triangle has none.")
    grid("Which shape has no right angles?", [(RHOMB, 0), (RECT, 0), (T_RIGHT2, 0), (RTRAP, 0)],
         lambda f: f["right"] == 0, "has no square corners. The others each have at least one right angle (see the small squares).")
    grid("Which shape has perpendicular sides but no parallel sides?", [(T_RIGHT, 20), (RECT, 0), (TRAP, 0), (RTRAP, 0)],
         lambda f: f["perp"] and f["par"] == 0, "is a right triangle: 2 sides meet at a right angle, and no sides are parallel. The rectangle and both trapezoids have parallel sides.")
    grid("Which shape has 2 pairs of parallel sides but no right angles?", [(PARA, 0), (SQUARE, 0), (TRAP, 0), (KITE, 0)],
         lambda f: f["par"] == 2 and f["right"] == 0, "is a parallelogram that leans, so it has no right angles. The square has right angles, the trapezoid has only 1 pair of parallel sides, and the kite has none.")
    grid("Which shape has no parallel sides?", [(PENT, 0), (HEX, 0), (TRAP, 0), (RECT, 0)],
         lambda f: f["par"] == 0, "is a pentagon with 5 equal sides. None of its sides go the same way. The hexagon has 3 pairs of parallel sides, the trapezoid 1 pair and the rectangle 2 pairs.")
    grid("Which shape has an obtuse angle?", [(HEX, 0), (SQUARE, 0), (T_ACUTE, 0), (T_RIGHT, 0)],
         lambda f: f["obtuse"] > 0, "is a hexagon. All 6 of its angles are wider than a right angle. The square has right angles only, and the triangles have acute angles and a right angle.")
    counts = [
        (HEX, 0, "How many pairs of parallel sides does this shape have?", "par", [2, 6, 0],
         "This hexagon has 6 sides, and each side is parallel to the side across from it. 6 sides make 3 pairs."),
        (RTRAP, 0, "How many right angles does this shape have?", "right", [1, 4, 0],
         "The small squares show 2 right angles, both on the left side. The other 2 angles are acute and obtuse."),
        (HOUSE, 0, "How many right angles does this shape have?", "right", [2, 4, 5],
         "There are right angles at the 2 bottom corners and at the top point (see the small squares). The 2 angles where the roof meets the walls are obtuse."),
        (TRAP, 0, "How many obtuse angles does this shape have?", "obtuse", [0, 1, 4],
         "The 2 top angles are wider than a right angle, so they are obtuse. The 2 bottom angles are acute."),
    ]
    for pts, rot, qq, key, wrong, e in counts:
        f = pfacts(pts)
        its.append(mcq_num(fig(shape_svg(pts, rot, 120, 76, label="shape with right-angle marks")) + qq, f[key], wrong, e))
    its.append(mcq("Which shape always has 2 pairs of parallel sides and 4 right angles?", "rectangle",
                   ["parallelogram", "trapezoid", "rhombus"],
                   "Every rectangle has 4 right angles and 2 pairs of parallel sides. A parallelogram or a rhombus has right angles only sometimes, "
                   "and a trapezoid has only 1 pair of parallel sides.", rnd))
    its.append(mcq("Which shape can never have parallel sides?", "triangle", ["trapezoid", "rectangle", "hexagon"],
                   "Any 2 sides of a triangle meet at a corner, so no 2 sides can be parallel.", rnd))
    its.append(mcq("Which shape always has perpendicular sides?", "right triangle", ["obtuse triangle", "rhombus", "trapezoid"],
                   "A right triangle always has a right angle, so 2 of its sides are perpendicular. A rhombus or a trapezoid has right angles only sometimes, "
                   "and an obtuse triangle never does.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says every shape with a right angle also has parallel sides. Which shape shows that %s is wrong?" % (n, he),
                   "right triangle", ["rectangle", "square", "right trapezoid"],
                   "A right triangle has a right angle but no parallel sides. The rectangle, the square and the right trapezoid all have parallel sides.", rnd))
    its.append(mcq("A garden bed has 4 sides. Only the front edge and the back edge are parallel, and none of its corners are right angles. What shape is it?",
                   "trapezoid", ["parallelogram", "rectangle", "triangle"],
                   "4 sides with exactly 1 pair of parallel sides make a trapezoid. A parallelogram or a rectangle has 2 pairs.", rnd))
    its.append(mcq("A yield sign is a triangle with 3 equal sides. Each angle is 60°. What kind of triangle is it?", "acute triangle",
                   ["right triangle", "obtuse triangle", "not a triangle"],
                   "60° is less than 90°, so all 3 angles are acute. That makes it an acute triangle.", rnd))
    n, he, his = P.next()
    its.append(mcq("A window has 4 right angles. %s says it has no perpendicular sides because none of its sides cross. Is %s right?" % (n, he),
                   "No, its sides meet at right angles", ["Yes, the sides do not cross", "Yes, the sides are parallel", "No, only 2 sides meet"],
                   "Two sides are perpendicular when they meet at a right angle. They do not have to cross. Every corner of the window joins 2 perpendicular sides.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s cuts a square piece of bread from one corner to the opposite corner. What kind of triangles are the 2 pieces?" % n,
                   "right triangles", ["acute triangles", "obtuse triangles", "one of each kind"],
                   "Each piece keeps one corner of the square, which is a right angle. So both pieces are right triangles.", rnd))
    its.append(mcq_num("A door is a rectangle. How many pairs of parallel sides does it have?", 2, [1, 4, 0],
                       "The top and bottom are parallel, and the 2 sides are parallel. That is 2 pairs (4 is the number of sides)."))
    its.append(mcq("A shape has 4 sides, 2 pairs of parallel sides and no right angles. All 4 sides are the same length. What is it?",
                   "rhombus", ["square", "trapezoid", "rectangle"],
                   "4 equal sides make a rhombus. With no right angles it is not a square, and with 2 pairs of parallel sides it is not a trapezoid.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Classify shapes by sides and angles", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    k = dict(L=62, ext=24)
    pics = {
        "point": basic("point", names=("A",)).svg("point A"),
        "line": basic("line", 0, ("A", "B"), **k).svg("line AB"),
        "segment": basic("segment", 0, ("A", "B"), L=96).svg("line segment AB"),
        "ray": basic("ray", 0, ("A", "B"), **k).svg("ray AB"),
        "angle": angle_fig(55, 0, L=70, names=("A", "B", "C")).svg("angle ABC"),
    }
    types = strip_svg([(angle_fig(50, 10, L=70), "acute"), (angle_fig(90, 0, L=64), "right"),
                       (angle_fig(130, 10, L=60), "obtuse"), (angle_fig(180, 0, L=52), "straight")],
                      label="acute, right, obtuse and straight angles")
    lines = strip_svg([(pair_lines_fig([((60, 26), 15), ((60, 58), 15)]), "parallel"),
                       (pair_lines_fig([((60, 40), 30), ((60, 40), 120)]), "perpendicular"),
                       (pair_lines_fig([((60, 40), 15), ((60, 40), 75)]), "intersecting"),
                       (pair_lines_fig([((0, 16), -4), ((0, 68), 9)]), "not parallel")],
                      cw=132, label="parallel, perpendicular and intersecting lines")
    tris = strip_svg([(shape_fig(T_ACUTE, 0, 100, 70), "acute triangle"), (shape_fig(T_RIGHT, 0, 100, 70), "right triangle"),
                      (shape_fig(T_OBT, 0, 110, 60), "obtuse triangle")], cw=140,
                     label="acute, right and obtuse triangles")
    shapes = strip_svg([(shape_fig(TRAP, 0, 96, 60), "trapezoid"), (shape_fig(PARA, 0, 96, 60), "parallelogram"),
                        (shape_fig(T_RIGHT, 0, 90, 60), "right triangle"), (shape_fig(HEX, 0, 80, 66), "hexagon")],
                       cw=128, label="trapezoid, parallelogram, right triangle and hexagon")
    return (
        "<h2>The building blocks of geometry</h2>"
        "<p>Every shape is made of a few simple figures. Look at the <b>ends</b>: a dot is an <b>endpoint</b> (the figure stops there), "
        "and an <b>arrow</b> means the figure goes on forever.</p>" +
        table(["Figure", "Picture", "What it is", "How to name it"], [
            ["Point", pics["point"], "An exact spot, drawn as a dot", "point A"],
            ["Line", pics["line"], "Straight, goes on forever both ways. No endpoints", "line AB or line BA"],
            ["Line segment", pics["segment"], "Part of a line with 2 endpoints", "line segment AB or BA"],
            ["Ray", pics["ray"], "1 endpoint, goes on forever one way", "ray AB: the endpoint comes first"],
            ["Angle", pics["angle"], "Two rays with the same endpoint, the vertex", "angle ABC: the vertex goes in the middle"],
        ]) +
        ex("Example", "A ray starts at point K and goes through point L. What is its name?",
           "The endpoint is K, so K comes first. The order of the letters on the page does not matter.", "ray KL") +
        "<h2>Kinds of angles</h2>"
        "<p>Compare an angle with a <b>right angle</b>, a square corner like the corner of a sheet of paper. "
        "A small square in a corner shows a right angle.</p>"
        "<figure class='sn-fig'>" + types +
        "<figcaption>Turning an angle does not change its kind. Longer sides do not make an angle bigger.</figcaption></figure>" +
        table(["Angle", "Size"], [
            ["Acute", "Smaller than a right angle (less than 90°)"],
            ["Right", "Exactly a square corner (90°)"],
            ["Obtuse", "Bigger than a right angle, smaller than a straight angle (between 90° and 180°)"],
            ["Straight", "A straight line (180°), the same as 2 right angles"],
        ]) +
        "<h2>Parallel and perpendicular lines</h2>"
        "<p><b>Parallel</b> lines stay the same distance apart and never meet, like train tracks. "
        "<b>Perpendicular</b> lines cross at right angles, like the lines of a plus sign. "
        "Lines that cross at any angle are <b>intersecting</b>.</p>"
        "<figure class='sn-fig'>" + lines +
        "<figcaption>The last two lines do not cross on the page, but they get closer. They would meet, so they are not parallel.</figcaption></figure>"
        "<p>Line segments can be parallel or perpendicular too. The top and bottom of the letter Z are parallel, "
        "and the two line segments of the letter L are perpendicular.</p>"
        "<h2>Classify triangles by their angles</h2>"
        "<figure class='sn-fig'>" + tris +
        "<figcaption>Look at the largest angle. Every triangle has at least 2 acute angles.</figcaption></figure>" +
        table(["Triangle", "What it must have"], [
            ["Acute triangle", "All 3 angles acute"],
            ["Right triangle", "1 right angle"],
            ["Obtuse triangle", "1 obtuse angle"],
        ]) +
        "<p>A triangle can never have 2 right angles or 2 obtuse angles: its sides would not meet.</p>"
        "<h2>Classify shapes by sides and angles</h2>"
        "<p>Sort shapes by asking: Does it have <b>parallel sides</b>? <b>Perpendicular sides</b> (a right angle)? "
        "Any <b>acute</b> or <b>obtuse</b> angles?</p>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>Each shape is sorted by its sides and angles, not by how it is turned.</figcaption></figure>" +
        table(["Shape", "Pairs of parallel sides", "Right angles"], [
            ["Square, rectangle", "2", "4"],
            ["Parallelogram that leans", "2", "0"],
            ["Trapezoid", "exactly 1", "0 or 2"],
            ["Right triangle", "0", "1"],
            ["Hexagon with equal sides", "3", "0 (all 6 are obtuse)"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up lines, line segments and rays", "Look at the ends: 2 arrows = line, 2 dots = line segment, 1 dot and 1 arrow = ray"],
            ["Naming ray KL as ray LK", "The endpoint always comes first"],
            ["Calling a tilted right angle acute", "Turning does not change an angle. Check for a square corner"],
            ["Saying lines are parallel because they do not cross on the page", "Check that they stay the same distance apart"],
            ["Calling an obtuse triangle acute because 2 angles are acute", "Name a triangle by its largest angle"],
        ])
    )


FAQ = [
    {"q": "What is the difference between a line, a line segment and a ray?",
     "a": "A line goes on forever in both directions, a line segment has 2 endpoints, and a ray has 1 endpoint and goes on forever in one direction."},
    {"q": "How do you name a ray?",
     "a": "Write the endpoint first, then another point on the ray. A ray that starts at A and goes through B is ray AB; ray BA would start at B."},
    {"q": "What is the difference between parallel and perpendicular lines?",
     "a": "Parallel lines never meet and stay the same distance apart. Perpendicular lines cross and make 4 right angles."},
    {"q": "How do you classify triangles by their angles?",
     "a": "Look at the largest angle. A right triangle has a right angle, an obtuse triangle has an obtuse angle, and an acute triangle has 3 acute angles."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    (A-D pictures, angle kinds, numbers) stay as they are; the other questions fill the gaps."""
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
        assert max(final) - min(final) <= 2, (s["title"], final)


def gen_lines_angles():
    rnd = random.Random(115)
    P = People(rnd)
    sets = [set_figures(rnd), set_angles(rnd), set_parallel(rnd), set_triangles(rnd), set_classify(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
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
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "lines-angles-shapes", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Lines, Angles and Shapes: Rays, Parallel and Perpendicular Lines, Classifying Triangles",
        "seo_title": "Grade 4 Lines, Rays and Angles Worksheets: Parallel and Perpendicular Lines, Right Triangles (4.G.A.1-2)",
        "short_title": "Lines, angles and shapes",
        "domain": "Geometry",
        "standard_code": "4.G.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/G/A/",
        "standard_text": "Draw points, lines, line segments, rays, angles (right, acute, obtuse), and perpendicular and parallel lines. Identify these in two-dimensional figures. Classify two-dimensional figures based on the presence or absence of parallel or perpendicular lines, or the presence or absence of angles of a specified size. Recognize right triangles as a category, and identify right triangles.",
        "meta_desc": "Free Grade 4 geometry worksheets with pictures: points, lines, line segments and rays, acute, right, obtuse and straight angles, parallel and perpendicular lines, right, acute and obtuse triangles, and sorting shapes by sides and angles. 100 practice questions with answers.",
        "key_big": "Look at the ends and the corners: arrows go on forever, dots are endpoints, and a square corner is a right angle.",
        "key_sub": "A ray is named from its endpoint. Parallel lines never meet; perpendicular lines meet at right angles. A triangle is named by its largest angle: acute, right or obtuse.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, the map) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_lines_angles()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(four [a-z]+ labeled A to D|street map|three lines)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
