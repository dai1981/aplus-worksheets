# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Angles and shapes (National Curriculum in England, Geometry – properties of shapes)
  python tools/gen_uk_maths_y4_angles_shapes.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 4 compares angles with a right angle (no protractor: that is Year 5).
  acute < right angle (a square corner, 90°) < obtuse < straight line (two right angles, 180°)
Triangles: equilateral (3 equal sides), isosceles (exactly 2 equal sides), scalene (no equal sides),
right-angled (one right angle; it can also be isosceles or scalene).
Quadrilaterals: square, rectangle, rhombus, parallelogram, trapezium (exactly 1 pair of parallel sides), kite.
Every drawing is exact and checked: tick marks show equal sides, arrows show parallel sides and small
squares show right angles, all computed from the real geometry. Unmarked angles are at least 10° away
from a right angle, sides that are not equal differ by more than 9%, and no label touches a line.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
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

    def line(self, p, q, w=3, col=GREEN):
        self.el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' "
                       "stroke-linecap='round'/>" % (p[0], p[1], q[0], q[1], col, w))
        self._seg(p, q, w / 2.0)

    def dot(self, p, r=4):
        self.el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (p[0], p[1], r, INK))
        self._seg(p, p, r)

    def label(self, p, t, d, off=7, fs=16):
        d = norm(d)
        w, h = len(t) * fs * 0.68, fs * 0.72
        k = off + abs(d[0]) * w / 2 + abs(d[1]) * h / 2 + 2 * abs(d[0] * d[1]) * min(w, h) / 2
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

    def mark(self, pts, w=1.8):
        self.el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round' "
                       "stroke-linecap='round'/>" % (" ".join("%.1f,%.1f" % p for p in pts), INK, w))
        for i in range(len(pts) - 1):
            self._seg(pts[i], pts[i + 1], w / 2.0)

    def right_mark(self, v, u1, u2, k=10):
        q1 = add(v, u1, k)
        self.mark([q1, add(q1, u2, k), add(v, u2, k)], w=1.6)

    def arc(self, v, a1, a2, r):
        """Arc from direction a1 to a2 (degrees, anticlockwise)."""
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

    def svg(self, label, pad=5):
        body, bb = self.render()
        W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
        if W == H:
            W += 1                                     # keep figures out of the larger 'square' print size
        dx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
        dy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
        return svg_wrap(W, H, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (dx, dy, body), label)


def angle_fig(deg, rot=0, L=80, L2=None, F=None, at=(0.0, 0.0)):
    """Angle made of two arms from vertex `at`: one at direction rot, one at rot + deg.
    Right angles get a square mark, other angles an arc. L2 = length of the second arm."""
    F = F or Fig()
    V = at
    L2 = L2 or L
    d1, d2 = dirv(rot), dirv(rot + deg)
    F.line(V, add(V, d1, L))
    F.line(V, add(V, d2, L2))
    if abs(deg - 90) < 1e-9:
        F.right_mark(V, d1, d2, 12)
    else:
        assert abs(deg - 90) >= 15, deg
        r = min(L, L2) * (0.42 if deg < 60 else 0.34 if deg < 150 else 0.26)
        F.arc(V, rot, rot + deg, max(10, min(r, 24)))
    return F


def kind_of(deg):
    return "acute" if deg < 90 else "right angle" if deg == 90 else "obtuse" if deg < 180 else "straight line"


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def side_lens(pts):
    n = len(pts)
    return [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]


def angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        u = norm(sub(pts[i - 1], pts[i]))
        v = norm(sub(pts[(i + 1) % n], pts[i]))
        out.append(math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1])))))
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "shape must be convex"
    return out


def eq(a, b):
    return abs(a - b) < 1e-6 * max(a, b)


def facts(pts):
    L = side_lens(pts)
    A = angles(pts)
    n = len(pts)
    sides = [sub(pts[(i + 1) % n], pts[i]) for i in range(n)]
    par = [(i, j) for i in range(n) for j in range(i + 1, n) if dir_diff(sides[i], sides[j]) < 1e-6]
    groups = []
    for i, x in enumerate(L):
        for g in groups:
            if eq(L[g[0]], x):
                g.append(i)
                break
        else:
            groups.append([i])
    return {"n": n, "lens": L, "angles": A, "rights": [i for i, a in enumerate(A) if abs(a - 90) < 1e-6],
            "acute": sum(a < 90 - 1e-6 for a in A), "obtuse": sum(a > 90 + 1e-6 for a in A),
            "par": par, "groups": groups, "sides": sides}


def tri_name(pts):
    f = facts(pts)
    big = max(len(g) for g in f["groups"])
    sides = "equilateral" if big == 3 else "isosceles" if big == 2 else "scalene"
    return ("right-angled " if f["rights"] else "") + sides


def quad_name(pts):
    f = facts(pts)
    L = f["lens"]
    all_eq = len(f["groups"]) == 1
    if all_eq and len(f["rights"]) == 4:
        return "square"
    if len(f["rights"]) == 4:
        return "rectangle"
    if all_eq:
        return "rhombus"
    if len(f["par"]) == 2:
        return "parallelogram"
    if len(f["par"]) == 1:
        return "trapezium"
    if (eq(L[0], L[1]) and eq(L[2], L[3])) or (eq(L[1], L[2]) and eq(L[3], L[0])):
        return "kite"
    return "quadrilateral"


def shape_name(pts):
    n = len(pts)
    return tri_name(pts) if n == 3 else quad_name(pts) if n == 4 else {5: "pentagon", 6: "hexagon"}[n]


def S(pts, kind):
    sh = {"pts": [(float(x), float(y)) for x, y in pts], "kind": kind}
    assert shape_name(sh["pts"]) == kind, (kind, shape_name(sh["pts"]))
    return sh


def tri_ang(a, b, kind, base=120):
    """Triangle with angle a at the left end of the base and angle b at the right end (apex above)."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    return S([(0.0, 0.0), (float(base), 0.0), add((0.0, 0.0), dirv(a), side)], kind)


def rect(a, b, kind="rectangle"):
    return S([(0, 0), (a, 0), (a, b), (0, b)], kind)


def para(a, b, deg, kind="parallelogram"):
    return S([(0, 0), (a, 0), add((a, 0), dirv(deg), b), add((0, 0), dirv(deg), b)], kind)


def trap(bottom, top, h, off):
    return S([(0, h), (bottom, h), (off + top, 0), (off, 0)], "trapezium")


def rtrap(bottom, top, h):
    return S([(0, h), (bottom, h), (top, 0), (0, 0)], "trapezium")


def kite(w, a, b):
    return S([(0, 0), (w, a), (0, a + b), (-w, a)], "kite")


def regular(n, kind, r=60, start=90):
    return S([add((0, 0), dirv(start + 360.0 * i / n), r) for i in range(n)], kind)


EQUI = tri_ang(60, 60, "equilateral")
ISO_AC = tri_ang(70, 70, "isosceles")
ISO_TALL = tri_ang(76, 76, "isosceles")
ISO_OB = tri_ang(30, 30, "isosceles")
ISO_RT = tri_ang(45, 45, "right-angled isosceles")
SCA_AC = tri_ang(40, 62, "scalene")
SCA_AC2 = tri_ang(50, 72, "scalene")
SCA_OB = tri_ang(25, 40, "scalene")
SCA_RT = tri_ang(90, 35, "right-angled scalene")
SCA_RT2 = tri_ang(90, 58, "right-angled scalene")

SQ = rect(100, 100, "square")
RECT = rect(150, 80)
RECT2 = rect(140, 70)
RHO = para(100, 100, 60, "rhombus")
RHO2 = para(100, 100, 65, "rhombus")
PARA = para(150, 80, 60)
PARA2 = para(140, 75, 115)
TRAP = trap(150, 70, 80, 40)
TRAP2 = trap(150, 90, 70, 20)
RTRAP = rtrap(150, 80, 80)
KITE = kite(50, 35, 120)
KITE2 = kite(40, 50, 100)
HEX = regular(6, "hexagon", start=0)
HOUSE = S([(0, 40), (40, 0), (80, 40), (80, 110), (0, 110)], "pentagon")
NOT_TRI = S([(0, 72), (130, 72), (54.17, 30), (0, 30)], "trapezium")     # a right-angled triangle with its corner cut off


def placed(sh, rot, bw, bh):
    P = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [((p[0] - mx) * k, (p[1] - my) * k) for p in P]


ARROW_KINDS = ("parallelogram", "trapezium")


def shape_fig(sh, rot=0, bw=130, bh=80, sw=3, F=None, ticks=True, arrows=None, vlabels=None, fs=16):
    """Shape with its marks, all computed from the geometry.
    Tick marks: equal sides (not on parallelograms, where the arrows show the pairs).
    Small squares: right angles. Arrows: parallel sides (parallelograms and trapeziums by default;
    arrows=True draws them on every shape with parallel sides, arrows=False on none).
    vlabels: letters for the corners, written outside the shape."""
    F = F or Fig()
    pts = placed(sh, rot, bw, bh)
    n = len(pts)
    assert shape_name(pts) == sh["kind"], (sh["kind"], shape_name(pts))
    f = facts(pts)
    F.poly(pts, w=sw)
    for i, a in enumerate(f["angles"]):
        assert i in f["rights"] or abs(a - 90) >= 10, (sh["kind"], f["angles"])
    G = f["groups"]
    for g1 in G:
        for g2 in G:
            if g1 is not g2:
                a, b = f["lens"][g1[0]], f["lens"][g2[0]]
                assert abs(a - b) / max(a, b) > 0.09, (sh["kind"], f["lens"])
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in f["par"]:
                assert dir_diff(f["sides"][i], f["sides"][j]) >= 8, (sh["kind"], "almost parallel")
    draw_arrows = arrows if arrows is not None else sh["kind"] in ARROW_KINDS
    tick_at = set()
    cnt = 0
    if ticks:
        for g in G:
            if len(g) < 2 or (sh["kind"] == "parallelogram" and draw_arrows):
                continue
            cnt += 1
            for i in g:
                a, b = pts[i], pts[(i + 1) % n]
                d = norm(sub(b, a))
                nr = (-d[1], d[0])
                m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                tick_at.add(i)
                for j in range(cnt):
                    o = (j - (cnt - 1) / 2.0) * 5
                    c = add(m, d, o)
                    F.mark([add(c, nr, -6), add(c, nr, 6)], w=2)
    for i in f["rights"]:
        v = pts[i]
        k = min(10, 0.2 * min(f["lens"][i - 1], f["lens"][i]))
        F.right_mark(v, norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v)), k)
    if draw_arrows:
        for c, (i, j) in enumerate(f["par"]):
            d = norm(f["sides"][i])
            nr = (-d[1], d[0])
            for s_ in (i, j):
                a, b = pts[s_], pts[(s_ + 1) % n]
                m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                shift = 13 if s_ in tick_at else 0
                for r in range(c + 1):
                    o = shift + r * 5 - c * 2.5
                    tip = add(m, d, o + 4)
                    F.mark([add(add(tip, d, -7), nr, 5), tip, add(add(tip, d, -7), nr, -5)], w=2)
    if vlabels:
        for i, t in enumerate(vlabels):
            u1, u2 = norm(sub(pts[i - 1], pts[i])), norm(sub(pts[(i + 1) % n], pts[i]))
            F.label(pts[i], t, (-(u1[0] + u2[0]), -(u1[1] + u2[1])), off=5, fs=fs)
    return F


def shape_svg(sh, rot=0, bw=130, bh=80, label="shape", **kw):
    return shape_fig(sh, rot, bw, bh, **kw).svg(label)


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


# ------------------------------------------------------------ clocks, signs and letters
def clock_svg(h, label=None):
    """Analogue clock at h o'clock. Square picture (printed large)."""
    W = 112
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
    hh, mh = add(c, hd, 16), add(c, md, 24)
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>" % (hh + (INK,)))
    s.append("<line x1='56' y1='56' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (mh + (INK,)))
    s.append("<circle cx='56' cy='56' r='4' fill='%s'/>" % INK)
    return svg_wrap(W, W, "".join(s), label or "clock showing %d o’clock" % h)


def sign_svg(down=False, label="road sign"):
    """Triangular road sign with a red border (equilateral triangle)."""
    r = 50.0
    c = (60.0, 58.0 if not down else 46.0)
    pts = [add(c, dirv((270 if down else 90) + 120 * i), r) for i in range(3)]
    s = ["<polygon points='%s' fill='#ffffff' stroke='%s' stroke-width='9' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % p for p in pts), RED)]
    if not down:
        s.append("<rect x='56.5' y='40' width='7' height='22' rx='2' fill='%s'/><circle cx='60' cy='70' r='4' fill='%s'/>" % (INK, INK))
    return svg_wrap(121, 112, "".join(s), label)


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
    """Kinds of the angles between strokes that meet (the angles you see inside the letter)."""
    st = LETTERS[ch]
    out = []
    pts = {}
    for a, b in st:
        for p in (a, b):
            pts.setdefault(p, [])
    # every place where a stroke ends on another stroke or two strokes cross
    found = {}
    for i, (a, b) in enumerate(st):
        for j, (c, d) in enumerate(st):
            if j <= i:
                continue
            x = None
            r = sub(b, a)
            s = sub(d, c)
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
            a, b = st[i]
            for p in (a, b):
                if math.hypot(p[0] - x[0], p[1] - x[1]) > 1e-6:
                    dirs.append(math.degrees(math.atan2(p[1] - x[1], p[0] - x[0])) % 360)
        dirs.sort()
        for k in range(len(dirs)):
            g = (dirs[(k + 1) % len(dirs)] - dirs[k]) % 360
            if g < 180 - 1e-6:                      # angles inside the letter (skip straight and reflex)
                out.append(kind_of(round(g, 6)) if abs(g - 90) > 1e-6 else "right angle")
    return out


# ------------------------------------------------------------ text
TYPES = ["acute", "right angle", "obtuse", "straight line"]
TYPE_E = {
    "acute": "The angle is smaller than a right angle (a square corner), so it is acute.",
    "right angle": "The small square shows a square corner, so it is a right angle (90°).",
    "obtuse": "The angle is bigger than a right angle but smaller than a straight line, so it is obtuse.",
    "straight line": "The two arms point in opposite directions and make a straight line. That is two right angles (180°).",
}
TRI = ["equilateral", "isosceles", "scalene", "not a triangle"]
TRI_E = {
    "equilateral": "The tick marks show that all 3 sides are equal, so it is an equilateral triangle.",
    "isosceles": "The tick marks show exactly 2 equal sides, so it is an isosceles triangle.",
    "scalene": "There are no tick marks: all 3 sides are different lengths, so it is a scalene triangle.",
}
QUAD_E = {
    "square": "The tick marks show 4 equal sides and the small squares show 4 right angles, so it is a square.",
    "rectangle": "The small squares show 4 right angles, and only the opposite sides are equal, so it is a rectangle.",
    "rhombus": "The tick marks show 4 equal sides, and there are no right angles, so it is a rhombus.",
    "parallelogram": "The arrows show 2 pairs of parallel sides. There are no right angles and the sides are not all equal, so it is a parallelogram.",
    "trapezium": "The arrows show exactly 1 pair of parallel sides, so it is a trapezium.",
    "kite": "The tick marks show 2 pairs of equal sides that are next to each other, not opposite. It has no parallel sides, so it is a kite.",
}


# ------------------------------------------------------------ set 1: acute, right or obtuse?
def set_kinds(rnd, P):
    its = []
    pos = Pos(rnd)
    q = "What kind of angle is this?"
    for deg, rot, L, L2 in [(30, 15, 90, 90), (45, 200, 60, 80), (60, 100, 76, 76), (70, -30, 46, 46),
                            (90, 0, 80, 80), (90, 35, 60, 90), (90, -125, 76, 76),
                            (110, 20, 64, 64), (135, 160, 80, 56), (155, -20, 60, 60), (180, 20, 56, 56)]:
        k = kind_of(deg)
        e = TYPE_E[k]
        if k == "right angle" and rot:
            e += " Turning an angle does not change its size."
        its.append(mcq_fixed(fig(angle_fig(deg, rot, L, L2).svg(k + " angle" if k != "right angle" else k)) + q, TYPES, k, e))
    its.append(pick_grid("Which angle is acute?",
                         [angle_fig(40, 70, 64), angle_fig(90, 45, 56), angle_fig(115, 10, 54), angle_fig(180, 0, 44)],
                         "is smaller than a right angle. The others are a right angle, an obtuse angle and a straight line.", pos,
                         "four angles labelled A to D"))
    its.append(pick_grid("Which angle is obtuse?",
                         [angle_fig(125, -40, 46), angle_fig(50, 20, 66), angle_fig(90, 20, 56), angle_fig(180, 0, 44)],
                         "is bigger than a right angle but smaller than a straight line. A straight line is two right angles, not an obtuse angle.", pos,
                         "four angles labelled A to D"))
    its.append(pick_grid("Which angle is a right angle?",
                         [angle_fig(90, 60, 60), angle_fig(60, 0, 70), angle_fig(120, 30, 50), angle_fig(35, 100, 66)],
                         "has the small square that shows a right angle. It is turned, but turning does not change an angle.", pos,
                         "four angles labelled A to D"))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(130, 25, 34).svg("obtuse angle with short arms")) +
                   "%s says this angle is acute because its arms are short. Is %s right?" % (n, he),
                   "No, it is obtuse", ["Yes, short arms make it acute", "No, it is a right angle", "Yes, it is a small angle"],
                   "The size of an angle is how far it opens, not how long its arms are. This angle opens wider than a right angle, so it is obtuse.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(angle_fig(90, 40, 70).svg("turned right angle")) +
                   "%s says this is not a right angle because it is turned. Is %s right?" % (n, he),
                   "No, it is still a right angle", ["Yes, it is acute", "Yes, it is obtuse", "No, it is a straight line"],
                   "The small square shows a square corner. Turning an angle does not change its size, so it is still a right angle.", rnd))
    its.append(mcq("What is an acute angle?", "smaller than a right angle",
                   ["bigger than a right angle", "exactly a right angle", "two right angles"],
                   "An acute angle is smaller than a right angle (less than 90°).", rnd))
    its.append(mcq("What is an obtuse angle?", "between a right angle and a straight line",
                   ["smaller than a right angle", "exactly a right angle", "bigger than a straight line"],
                   "An obtuse angle is bigger than a right angle (90°) but smaller than a straight line (180°).", rnd))
    its.append(mcq_num("How many right angles make a straight line?", 2, [1, 3, 4],
                       "A right angle is 90° and a straight line is 180°. 90° + 90° = 180°, so 2 right angles make a straight line."))
    its.append(mcq("A right angle is a quarter turn. How many degrees is a right angle?", "90°", ["180°", "45°", "100°"],
                   "A right angle is 90°. A straight line (two right angles) is 180°.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Acute, right or obtuse?", "items": its}


# ------------------------------------------------------------ set 2: compare and order angles
def order_q(rnd, angs, ask_small=True):
    """angs: (deg, arm) for A, B, C. Order by size, not by arm length."""
    degs = [d for d, _ in angs]
    assert len(set(degs)) == 3 and min(abs(a - b) for a in degs for b in degs if a != b) >= 20
    F = [(angle_fig(d, 10 if d < 150 else 0, L), c) for (d, L), c in zip(angs, "ABC")]
    svg = strip_svg(F, cw=118, label="three angles labelled A, B and C")
    key = sorted(range(3), key=lambda i: degs[i])
    if not ask_small:
        key = key[::-1]
    s = lambda o: ", ".join("ABC"[i] for i in o)
    correct = s(key)
    by_arm = sorted(range(3), key=lambda i: angs[i][1])
    if not ask_small:
        by_arm = by_arm[::-1]
    assert s(by_arm) != correct
    perms = ["A, B, C", "A, C, B", "B, A, C", "B, C, A", "C, A, B", "C, B, A"]
    rnd.shuffle(perms)
    cands = [s(key[::-1]), s(by_arm)] + perms
    word = "smallest to largest" if ask_small else "largest to smallest"
    e = ("Look at how far each angle opens, not at the length of its arms. From %s: %s." % (word, correct) +
         " The arm lengths do not change the size.")
    return mcq(fig(svg) + "Put the angles in order from <b>%s</b>." % word, correct, cands, e, rnd)


def set_compare(rnd, P):
    its = []
    pos = Pos(rnd)
    lab = "four angles labelled A to D"
    its.append(pick_grid("Which angle is the largest?",
                         [angle_fig(150, 0, 40), angle_fig(40, 30, 76), angle_fig(90, 10, 60), angle_fig(110, 30, 50)],
                         "opens the widest: it is obtuse and nearly a straight line. Long arms do not make an angle bigger.", pos, lab))
    its.append(pick_grid("Which angle is the largest?",
                         [angle_fig(130, 200, 42), angle_fig(70, 15, 76), angle_fig(30, 40, 76), angle_fig(105, 30, 56)],
                         "opens the widest. The other obtuse angle is only a little bigger than a right angle.", pos, lab))
    its.append(pick_grid("Which angle is the largest?",
                         [angle_fig(180, 0, 42), angle_fig(140, 20, 44), angle_fig(90, 30, 60), angle_fig(60, 10, 76)],
                         "is a straight line: two right angles. That is bigger than any obtuse angle.", pos, lab))
    its.append(pick_grid("Which angle is the smallest?",
                         [angle_fig(25, 20, 76), angle_fig(60, 10, 50), angle_fig(90, 0, 44), angle_fig(140, 20, 40)],
                         "opens the least. Its arms are long, but the gap between them is the smallest.", pos, lab))
    its.append(pick_grid("Which angle is the smallest?",
                         [angle_fig(50, 120, 40), angle_fig(75, 0, 76), angle_fig(120, 10, 52), angle_fig(90, 135, 66)],
                         "opens the least, even though it has the shortest arms.", pos, lab))
    its.append(order_q(rnd, [(120, 40), (35, 76), (70, 60)]))
    its.append(order_q(rnd, [(60, 76), (150, 56), (90, 50)]))
    its.append(order_q(rnd, [(45, 76), (180, 40), (110, 60)], ask_small=False))
    its.append(order_q(rnd, [(70, 70), (130, 44), (30, 56)], ask_small=False))
    pair = strip_svg([(angle_fig(60, 10, 80), "P"), (angle_fig(60, 10, 36), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Are angle P and angle Q the same size?", "Yes, they open the same amount",
                   ["No, P is larger: its arms are longer", "No, Q is larger", "No, P is a right angle"],
                   "Both angles open by the same amount. P only has longer arms, and arm length does not change the size of an angle.", rnd))
    pair = strip_svg([(angle_fig(50, 20, 82), "P"), (angle_fig(120, 10, 38), "Q")], cw=118, label="angle P and angle Q")
    its.append(mcq(fig(pair) + "Which angle is larger?", "angle Q",
                   ["angle P", "They are the same size", "You cannot tell"],
                   "Angle Q is obtuse and angle P is acute, so Q is larger. P has longer arms, but that does not make the angle bigger.", rnd))
    t = shape_svg(SCA_OB, 0, 140, 64, label="triangle ABC", vlabels="ABC")
    its.append(mcq_fixed(fig(t) + "Which angle in this triangle is obtuse?", ["angle A", "angle B", "angle C", "none of them"], "angle C",
                         "Angle C, at the top, opens wider than a right angle, so it is obtuse. Angles A and B are acute."))
    k = shape_svg(KITE, 90, 140, 80, label="kite ABCD", vlabels="ABCD")
    fk = facts(placed(KITE, 90, 140, 80))
    assert min(range(4), key=lambda i: fk["angles"][i]) == 2
    its.append(mcq_fixed(fig(k) + "Which angle in this kite is the smallest?", ["angle A", "angle B", "angle C", "angle D"], "angle C",
                         "Angle C is the only acute angle: it is the sharpest point of the kite. Angles A, B and D are obtuse."))
    tp = shape_svg(TRAP, 0, 140, 72, label="trapezium ABCD", vlabels="ABCD")
    ft = facts(placed(TRAP, 0, 140, 72))
    assert [a > 90 for a in ft["angles"]] == [False, False, True, True]
    its.append(mcq(fig(tp) + "Which two angles in this trapezium are obtuse?", "C and D", ["A and B", "A and C", "B and D"],
                   "The two top angles, C and D, open wider than a right angle. The two bottom angles, A and B, are acute.", rnd))
    counts = [
        (HEX, "How many obtuse angles does this shape have?", "obtuse", [0, 2, 3],
         "All 6 angles of this hexagon are bigger than a right angle, so all 6 are obtuse."),
        (HOUSE, "How many right angles does this shape have?", "right", [2, 4, 5],
         "The small squares show 3 right angles: the 2 bottom corners and the top of the roof. The 2 angles where the roof meets the walls are obtuse."),
        (RTRAP, "How many acute angles does this shape have?", "acute", [0, 2, 3],
         "Two angles are right angles (small squares), one is obtuse and only one is acute: the sharp corner on the right."),
    ]
    for sh, qq, key, wrong, e in counts:
        f = facts(sh["pts"])
        val = len(f["rights"]) if key == "right" else f[key]
        its.append(mcq_num(fig(shape_svg(sh, 0, 120, 76, label=sh["kind"])) + qq, val, wrong, e))
    its.append(mcq("Which list goes from the smallest angle to the largest?",
                   "acute, right angle, obtuse", ["obtuse, right angle, acute", "right angle, acute, obtuse", "acute, obtuse, right angle"],
                   "An acute angle is smaller than a right angle, and an obtuse angle is bigger than a right angle.", rnd))
    its.append(mcq("Which is larger: an obtuse angle or a right angle?", "an obtuse angle",
                   ["a right angle", "They are the same", "It depends on the arms"],
                   "An obtuse angle is always bigger than a right angle. That is what obtuse means.", rnd))
    n, he, his = P.next()
    its.append(mcq_fixed("%s draws an angle that is bigger than one right angle but smaller than two right angles. What kind of angle is it?" % n,
                         TYPES, "obtuse",
                         "Two right angles make a straight line. An angle between one right angle and a straight line is obtuse."))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order angles", "items": its}


# ------------------------------------------------------------ set 3: triangles
def set_triangles(rnd, P):
    its = []
    pos = Pos(rnd)
    q = "What type of triangle is this? Look at the marks on the sides."
    for sh, rot in [(EQUI, 0), (EQUI, 180), (ISO_AC, 0), (ISO_TALL, 90), (ISO_OB, 0), (SCA_AC, 0), (SCA_OB, 20)]:
        k = sh["kind"]
        e = TRI_E[k]
        if rot:
            e += " Turning a triangle does not change its type."
        its.append(mcq_fixed(fig(shape_svg(sh, rot, 120, 80, label=k + " triangle")) + q, TRI, k, e))
    its.append(mcq_fixed(fig(shape_svg(NOT_TRI, 0, 130, 70, label="shape with 4 sides", arrows=False)) + q, TRI, "not a triangle",
                         "Count the sides: there are 4, because the top corner is cut off. A triangle has exactly 3 sides."))
    its.append(mcq(fig(shape_svg(SCA_RT, 0, 130, 80, label="right-angled scalene triangle")) +
                   "This triangle has a right angle. Which names fit it?", "right-angled and scalene",
                   ["right-angled and isosceles", "right-angled and equilateral", "isosceles only"],
                   "The small square shows a right angle, so it is right-angled. No sides are marked equal, so it is also scalene.", rnd))
    its.append(mcq(fig(shape_svg(ISO_RT, 180, 120, 70, label="right-angled isosceles triangle")) +
                   "Which names fit this triangle?", "right-angled and isosceles",
                   ["right-angled and scalene", "equilateral", "isosceles, not right-angled"],
                   "The small square shows a right angle, and the tick marks show 2 equal sides. So it is right-angled and isosceles.", rnd))
    lab = "four triangles labelled A to D"
    g = dict(bw=74, bh=74, sw=2.6)
    its.append(pick_grid("Which is a right-angled triangle?",
                         [shape_fig(SCA_RT2, 200, **g), shape_fig(SCA_AC, 10, **g), shape_fig(ISO_OB, 0, 80, 50, sw=2.6), shape_fig(EQUI, 180, **g)],
                         "has a right angle (the small square). The others have no right angle.", pos, lab))
    its.append(pick_grid("Which triangle is equilateral?",
                         [shape_fig(EQUI, 30, **g), shape_fig(ISO_TALL, 0, 60, 80, sw=2.6), shape_fig(ISO_OB, 0, 80, 50, sw=2.6), shape_fig(SCA_AC2, 0, **g)],
                         "has the same tick mark on all 3 sides. The two isosceles triangles have only 2 equal sides, and the scalene one has none.", pos, lab))
    its.append(pick_grid("Which triangle is isosceles?",
                         [shape_fig(ISO_AC, 160, **g), shape_fig(SCA_AC, 0, **g), shape_fig(SCA_RT, 0, **g), shape_fig(SCA_OB, 0, 80, 50, sw=2.6)],
                         "has exactly 2 sides with tick marks. The others have no equal sides: they are scalene.", pos, lab))
    its.append(pick_grid("Which triangle is scalene?",
                         [shape_fig(SCA_AC2, 30, **g), shape_fig(EQUI, 0, **g), shape_fig(ISO_RT, 0, **g), shape_fig(ISO_TALL, 0, 60, 80, sw=2.6)],
                         "has no tick marks: all 3 sides are different lengths. The others have at least 2 equal sides.", pos, lab))
    its.append(mcq("A triangle has sides of 5 cm, 5 cm and 8 cm. What type of triangle is it?", "isosceles",
                   ["equilateral", "scalene", "not a triangle"],
                   "Two sides are 5 cm, so exactly 2 sides are equal. That makes it isosceles. It is not equilateral, because 8 cm is different.", rnd))
    its.append(mcq("A triangle has sides of 6 cm, 7 cm and 9 cm. What type of triangle is it?", "scalene",
                   ["isosceles", "equilateral", "right-angled"],
                   "All 3 sides are different lengths, so it is scalene.", rnd))
    its.append(mcq_num("How many equal sides does an isosceles triangle have?", 2, [3, 1, 0],
                       "An isosceles triangle has exactly 2 equal sides. A triangle with 3 equal sides is equilateral."))
    n, he, his = P.next()
    its.append(mcq(fig(shape_svg(ISO_TALL, 0, 70, 90, label="isosceles triangle")) +
                   "%s says this triangle is equilateral. Is %s right?" % (n, he),
                   "No, only 2 sides are equal", ["Yes, it is pointy", "Yes, all sides are equal", "No, it is scalene"],
                   "Only the 2 long sides have tick marks, so exactly 2 sides are equal. It is isosceles, not equilateral.", rnd))
    its.append(mcq("Can a triangle have 2 right angles?", "No, the sides would not meet",
                   ["Yes, like a rectangle", "Yes, if it is very big", "Only if it is turned"],
                   "If 2 angles were right angles, the 2 sides going up from them would be parallel and never meet. The shape could not close.", rnd))
    its.append(mcq("What is true about the angles of an equilateral triangle?", "All 3 angles are equal",
                   ["It has a right angle", "It has an obtuse angle", "Only 2 angles are equal"],
                   "An equilateral triangle has 3 equal sides and 3 equal angles. Each angle is acute (60°).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equilateral, isosceles, scalene and right-angled triangles", "items": its}


# ------------------------------------------------------------ set 4: quadrilaterals
QUADS = ["square", "rectangle", "rhombus", "parallelogram", "trapezium", "kite"]


def set_quads(rnd, P):
    its = []
    pos = Pos(rnd)
    q = "What is the name of this quadrilateral?"
    names = [
        (SQ, 45, ["rhombus", "kite", "rectangle"], " Standing on a corner does not change it: it is still a square."),
        (RECT, 20, ["square", "parallelogram", "trapezium"], ""),
        (RHO, 0, ["square", "kite", "parallelogram"], ""),
        (PARA, 0, ["rectangle", "rhombus", "trapezium"], ""),
        (TRAP, 0, ["parallelogram", "rectangle", "kite"], ""),
        (RTRAP, 180, ["rectangle", "parallelogram", "kite"], " The right angles do not make it a rectangle: a rectangle has 4."),
        (KITE, 0, ["rhombus", "trapezium", "parallelogram"], ""),
        (KITE2, 90, ["rhombus", "parallelogram", "square"], ""),
    ]
    for sh, rot, wrong, extra in names:
        k = sh["kind"]
        its.append(mcq(fig(shape_svg(sh, rot, 130, 84, label=k)) + q, k, wrong, QUAD_E[k] + extra, rnd))
    lab = "four quadrilaterals labelled A to D"
    g = dict(bw=74, bh=70, sw=2.6)
    its.append(pick_grid("The arrows show parallel sides. Which shape is NOT a parallelogram?",
                         [shape_fig(TRAP2, 0, arrows=True, ticks=False, **g), shape_fig(RECT2, 0, arrows=True, ticks=False, **g),
                          shape_fig(PARA2, 0, arrows=True, ticks=False, **g), shape_fig(RHO2, 0, arrows=True, ticks=False, **g)],
                         "has only 1 pair of parallel sides, so it is a trapezium. A parallelogram has 2 pairs. "
                         "Rectangles and rhombuses have 2 pairs of parallel sides, so they are special parallelograms.", pos, lab))
    its.append(pick_grid("Which shape has exactly one pair of parallel sides?",
                         [shape_fig(TRAP, 0, arrows=True, ticks=False, **g), shape_fig(PARA, 0, arrows=True, ticks=False, **g),
                          shape_fig(RECT, 20, arrows=True, ticks=False, **g), shape_fig(KITE, 90, **g)],
                         "is a trapezium: only its top and bottom are parallel. The parallelogram and rectangle have 2 pairs, and the kite has none.", pos, lab))
    its.append(pick_grid("Which shape has 4 equal sides but no right angles?",
                         [shape_fig(RHO2, 20, **g), shape_fig(SQ, 0, bw=70, bh=70, sw=2.6),
                          shape_fig(KITE, 0, **g), shape_fig(RECT2, 0, **g)],
                         "is a rhombus: all 4 sides have the same tick mark and there are no small squares. The square has right angles, "
                         "and the kite and rectangle do not have 4 equal sides.", pos, lab))
    its.append(pick_grid("Which shape has 4 right angles but NOT 4 equal sides?",
                         [shape_fig(RECT2, 25, **g), shape_fig(SQ, 45, bw=70, bh=70, sw=2.6),
                          shape_fig(RHO, 0, **g), shape_fig(RTRAP, 0, **g)],
                         "is a rectangle. The turned square has 4 right angles too, but its 4 sides are equal. "
                         "The rhombus has no right angles, and the trapezium has only 2.", pos, lab))
    n, he, his = P.next()
    its.append(mcq(fig(shape_svg(TRAP2, 0, 130, 70, label="trapezium")) +
                   "%s says every shape with 4 sides is a rectangle. Is %s right?" % (n, he),
                   "No, a rectangle needs 4 right angles", ["Yes, it has 4 sides", "Yes, it has 4 corners", "No, it is a square"],
                   "This shape has 4 sides but no right angles, so it is not a rectangle. It is a trapezium: only 1 pair of sides is parallel.", rnd))
    its.append(mcq_num("How many pairs of parallel sides does a parallelogram have?", 2, [1, 4, 0],
                       "The opposite sides of a parallelogram are parallel: top and bottom, left and right. That is 2 pairs (4 is the number of sides)."))
    its.append(mcq("Is a square also a rectangle?", "Yes, it has 4 right angles",
                   ["No, its sides are all equal", "No, a square is smaller", "Only if it is turned"],
                   "A rectangle is a 4-sided shape with 4 right angles. A square has 4 right angles too, so it is a special rectangle with 4 equal sides.", rnd))
    its.append(mcq(fig(shape_svg(TRAP2, 0, 130, 70, label="trapezium with arrows")) + "What do the arrows on the top and bottom sides show?",
                   "The sides are parallel", ["The sides are equal", "The angles are right angles", "The shape is turned"],
                   "Matching arrows show parallel sides: they go in the same direction and never meet.", rnd))
    its.append(mcq(fig(shape_svg(KITE2, 0, 110, 84, label="kite with tick marks")) + "What do the small lines (tick marks) on the sides show?",
                   "Those sides are equal", ["Those sides are parallel", "Those angles are right angles", "Those sides are curved"],
                   "Sides with the same tick marks are the same length. One tick shows one pair, two ticks show another pair.", rnd))
    its.append(mcq("Which shape has 2 pairs of equal sides that are next to each other, and no parallel sides?", "kite",
                   ["rhombus", "parallelogram", "rectangle"],
                   "A kite has 2 pairs of equal sides next to each other. A parallelogram and a rectangle have equal sides opposite each other.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s sorts shapes into “has a right angle” and “no right angle”. Which shape goes in “no right angle”?" % n,
                   "rhombus", ["square", "rectangle", "right-angled triangle"],
                   "A rhombus that is not a square has no right angles. A square and a rectangle have 4, and a right-angled triangle has 1.", rnd))
    its.append(mcq("A shape has 2 pairs of parallel sides. Its opposite sides are equal, but not all 4 sides are equal, and it has no right angles. What is it?",
                   "parallelogram", ["rectangle", "rhombus", "trapezium"],
                   "2 pairs of parallel sides make a parallelogram. With no right angles it is not a rectangle, and without 4 equal sides it is not a rhombus.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Quadrilaterals: square, rectangle, rhombus, parallelogram, trapezium and kite", "items": its}


# ------------------------------------------------------------ set 5: problems
def set_problems(rnd, P):
    its = []
    pos = Pos(rnd)
    clocks = [(3, "right angle", "At 3 o’clock the hands make a square corner: a quarter turn, 90°."),
              (10, "acute", "At 10 o’clock the hands are 2 hour marks apart. That is less than a quarter turn (3 hour marks), so the angle is acute."),
              (4, "obtuse", "At 4 o’clock the hands are 4 hour marks apart. A right angle is 3 hour marks, and a straight line is 6, so the angle is obtuse."),
              (6, "straight line", "At 6 o’clock one hand points to 12 and the other to 6. Together they make a straight line: two right angles.")]
    for h, k, e in clocks:
        its.append(mcq_fixed(fig(clock_svg(h)) + "What kind of angle do the hands make?", TYPES, k, e))
    its.append(mcq_fixed("A clock shows 2 o’clock. What kind of angle do the hour hand and the minute hand make?", TYPES, "acute",
                         "At 2 o’clock the hands are 2 hour marks apart. A right angle is 3 hour marks, so the angle is smaller: it is acute."))
    its.append(mcq_fixed("A clock shows 8 o’clock. What kind of angle is the smaller angle between the hands?", TYPES, "obtuse",
                         "From 8 to 12 is 4 hour marks. That is more than a right angle (3 hour marks) but less than a straight line (6), so it is obtuse."))
    its.append(mcq("At which time do the hands of a clock make a straight line?", "6 o’clock",
                   ["3 o’clock", "12 o’clock", "9 o’clock"],
                   "At 6 o’clock the hands point to 12 and 6, in opposite directions, so they make a straight line. At 3 and 9 o’clock they make right angles, "
                   "and at 12 o’clock they are on top of each other.", rnd))
    its.append(mcq("At which time do the hands of a clock make a right angle?", "9 o’clock",
                   ["6 o’clock", "12 o’clock", "10 o’clock"],
                   "At 9 o’clock the hands point to 12 and 9: a quarter turn apart, which is a right angle.", rnd))
    its.append(mcq(fig(sign_svg(False, "triangular warning road sign")) +
                   "A warning road sign is a triangle with 3 equal sides. What type of triangle is it?", "equilateral",
                   ["isosceles", "scalene", "right-angled"],
                   "3 equal sides make an equilateral triangle. Its 3 angles are equal too.", rnd))
    n, he, his = P.next()
    its.append(mcq(fig(sign_svg(True, "upside-down triangular give way sign")) +
                   "A give way sign is the same triangle turned upside down. %s says it is not equilateral any more. Is %s right?" % (n, he),
                   "No, it is still equilateral", ["Yes, it is now isosceles", "Yes, it is now scalene", "No, it is now right-angled"],
                   "Turning a shape does not change its sides or angles. The 3 sides are still equal, so it is still equilateral.", rnd))
    for ch, wrong in (("T", [1, 3, 4]), ("E", [2, 3, 5])):
        ka = letter_angles(ch)
        assert all(k == "right angle" for k in ka), (ch, ka)
        e = {"T": "Where the top line meets the stem, there is a right angle on each side. That is 2 right angles.",
             "E": "There is 1 right angle at the top corner, 1 at the bottom corner and 2 where the middle line meets the upright: 4 in all."}[ch]
        its.append(mcq_num(fig(letters_svg([ch], "capital letter " + ch)) + "How many right angles are inside the capital letter %s?" % ch,
                           len(ka), wrong, e))
    for what, test, letters, why in [
        ("an acute angle", lambda ks: "acute" in ks, ["V", "L", "T", "H"],
         "V has an acute angle at the bottom point. L, T and H only have right angles."),
        ("an obtuse angle", lambda ks: "obtuse" in ks, ["X", "L", "E", "F"],
         "Where the two lines of X cross, two of the angles are obtuse (and two are acute). L, E and F only have right angles."),
    ]:
        assert [test(letter_angles(c)) for c in letters] == [True, False, False, False], letters
        p = pos.next()
        row = letters[1:]
        row.insert(p, letters[0])
        its.append(mcq_fixed(fig(letters_svg(row)) + "Which capital letter has %s?" % what, row, letters[0],
                             why))
    riddles = [
        ("I have 4 equal sides and no right angles. What shape am I?", "rhombus", ["square", "rectangle", "kite"],
         "4 equal sides with no right angles make a rhombus. A square has 4 equal sides too, but it has 4 right angles."),
        ("I have 4 sides and exactly one pair of parallel sides. What shape am I?", "trapezium", ["parallelogram", "rectangle", "kite"],
         "Exactly 1 pair of parallel sides makes a trapezium. A parallelogram and a rectangle have 2 pairs, and a kite has none."),
        ("I have 4 right angles and 4 equal sides. What shape am I?", "square", ["rectangle", "rhombus", "kite"],
         "4 right angles and 4 equal sides make a square. A rectangle has 4 right angles, but not always 4 equal sides."),
        ("I am a triangle. Exactly 2 of my sides are equal. What am I?", "isosceles triangle",
         ["equilateral triangle", "scalene triangle", "right-angled triangle"],
         "A triangle with exactly 2 equal sides is isosceles. Equilateral would need 3 equal sides."),
    ]
    for qq, ans, wrong, e in riddles:
        its.append(mcq(qq, ans, wrong, e, rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds a square piece of paper in half from one corner to the opposite corner. What type of triangle does %s make?" % (n, he),
                   "right-angled isosceles", ["equilateral", "right-angled scalene", "scalene"],
                   "The triangle keeps one corner of the square, which is a right angle. Its two short sides are sides of the square, so they are equal: it is right-angled and isosceles.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s opens a door a little way, less than a right angle from the wall. What kind of angle do the door and the wall make?" % n,
                   "acute", ["obtuse", "right angle", "straight line"],
                   "The door has turned less than a right angle, so the angle is acute.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Clocks, road signs, letters and shape riddles", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    kinds = strip_svg([(angle_fig(50, 10, 70), "acute"), (angle_fig(90, 0, 64), "right angle"),
                       (angle_fig(130, 10, 58), "obtuse"), (angle_fig(180, 0, 52), "straight line")],
                      cw=130, label="acute angle, right angle, obtuse angle and straight line")
    same = strip_svg([(angle_fig(55, 10, 86), "long arms"), (angle_fig(55, 10, 36), "short arms")], cw=128,
                     label="two angles of the same size with long and short arms")
    tris = strip_svg([(shape_fig(EQUI, 0, 90, 72, sw=2.8), "equilateral"), (shape_fig(ISO_AC, 0, 90, 72, sw=2.8), "isosceles"),
                      (shape_fig(SCA_AC, 0, 96, 66, sw=2.8), "scalene"), (shape_fig(SCA_RT, 0, 96, 66, sw=2.8), "right-angled")],
                     cw=128, label="equilateral, isosceles, scalene and right-angled triangles")
    q1 = strip_svg([(shape_fig(SQ, 0, 66, 66, sw=2.8), "square"), (shape_fig(RECT, 0, 100, 56, sw=2.8), "rectangle"),
                    (shape_fig(RHO, 0, 100, 66, sw=2.8), "rhombus")], cw=130, label="square, rectangle and rhombus")
    q2 = strip_svg([(shape_fig(PARA, 0, 100, 60, sw=2.8), "parallelogram"), (shape_fig(TRAP, 0, 100, 60, sw=2.8), "trapezium"),
                    (shape_fig(KITE, 90, 104, 62, sw=2.8), "kite")], cw=130, label="parallelogram, trapezium and kite")
    return (
        "<h2>Acute, right angle or obtuse?</h2>"
        "<p>An angle shows how far something turns. Compare every angle with a <b>right angle</b>: "
        "a square corner, like the corner of a page. A small square in a corner shows a right angle.</p>"
        "<figure class='sn-fig'>" + kinds +
        "<figcaption>Acute is smaller than a right angle. Obtuse is bigger than a right angle but smaller than a straight line.</figcaption></figure>" +
        table(["Angle", "Compared with a right angle"], [
            ["Acute", "Smaller than a right angle (less than 90°)"],
            ["Right angle", "A square corner, a quarter turn (90°)"],
            ["Obtuse", "Bigger than a right angle, smaller than a straight line"],
            ["Straight line", "Two right angles (180°)"],
        ]) +
        ex("Example", "A clock shows 4 o’clock. What kind of angle do the hands make?",
           "A right angle is 3 hour marks (3 o’clock). A straight line is 6 hour marks (6 o’clock). 4 hour marks is in between.", "obtuse") +
        "<h2>Compare and order angles</h2>"
        "<p>To compare angles, look at how wide each one <b>opens</b>. Do not look at the length of the arms.</p>"
        "<figure class='sn-fig'>" + same +
        "<figcaption>These two angles are the same size. Longer arms do not make an angle bigger.</figcaption></figure>" +
        ex("Example", "Order these angles from smallest to largest: an obtuse angle, a right angle, an acute angle.",
           "Acute is smaller than a right angle, and obtuse is bigger.", "acute, right angle, obtuse") +
        "<h2>Triangles</h2>"
        "<p>Small lines on the sides, called <b>tick marks</b>, show sides that are the same length.</p>"
        "<figure class='sn-fig'>" + tris +
        "<figcaption>A right-angled triangle can also be isosceles or scalene. This one is right-angled and scalene.</figcaption></figure>" +
        table(["Triangle", "What it has"], [
            ["Equilateral", "3 equal sides and 3 equal angles"],
            ["Isosceles", "Exactly 2 equal sides (and 2 equal angles)"],
            ["Scalene", "No equal sides"],
            ["Right-angled", "1 right angle"],
        ]) +
        "<h2>Quadrilaterals</h2>"
        "<p>A quadrilateral has 4 straight sides. Arrows on two sides show that they are <b>parallel</b>: "
        "they go the same way and never meet.</p>"
        "<figure class='sn-fig'>" + q1 + "</figure>"
        "<figure class='sn-fig'>" + q2 +
        "<figcaption>One arrow marks one pair of parallel sides, two arrows mark another pair.</figcaption></figure>" +
        table(["Shape", "Equal sides", "Parallel sides", "Right angles"], [
            ["Square", "4 equal sides", "2 pairs", "4"],
            ["Rectangle", "Opposite sides equal", "2 pairs", "4"],
            ["Rhombus", "4 equal sides", "2 pairs", "None (unless it is a square)"],
            ["Parallelogram", "Opposite sides equal", "2 pairs", "None (unless it is a rectangle)"],
            ["Trapezium", "Can vary", "Exactly 1 pair", "Can have 2"],
            ["Kite", "2 pairs next to each other", "None", "Usually none"],
        ]) +
        ex("Example", "I have 4 equal sides and no right angles. What shape am I?",
           "4 equal sides could be a square or a rhombus. A square has 4 right angles, so it is not a square.", "a rhombus") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking longer arms make a bigger angle", "Look at how wide the angle opens"],
            ["Saying a turned square is not a square", "Turning does not change a shape. Check the sides and angles"],
            ["Calling every 4-sided shape a rectangle", "A rectangle must have 4 right angles"],
            ["Mixing up isosceles and equilateral", "Isosceles: exactly 2 equal sides. Equilateral: all 3 equal"],
            ["Calling an angle bigger than a straight line obtuse", "Obtuse angles are smaller than a straight line (two right angles)"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 children learn about angles?",
     "a": "They learn to spot acute and obtuse angles by comparing them with a right angle, and to compare and order angles up to two right angles (a straight line)."},
    {"q": "Do Year 4 pupils measure angles with a protractor?",
     "a": "No. In Year 4 they compare angles with a right angle. Measuring angles in degrees with a protractor starts in Year 5."},
    {"q": "What is the difference between an isosceles and an equilateral triangle?",
     "a": "An isosceles triangle has exactly 2 equal sides. An equilateral triangle has all 3 sides equal and all 3 angles equal."},
    {"q": "What is a trapezium?",
     "a": "A trapezium is a quadrilateral with exactly one pair of parallel sides. In the US the same shape is called a trapezoid."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order
    (A-D pictures, angle kinds, numbers) stay as they are; the other questions fill the gaps."""
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
    rnd = random.Random(4414)
    P = People(rnd)
    sets = [set_kinds(rnd, P), set_compare(rnd, P), set_triangles(rnd, P), set_quads(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "angles-and-shapes", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Angles and Shapes: Acute and Obtuse Angles, Triangles and Quadrilaterals",
        "seo_title": "Year 4 Angles and Shapes Worksheets: Acute and Obtuse Angles, Triangles, Quadrilaterals (Free, with Answers)",
        "short_title": "Angles and shapes",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 4: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Compare and classify geometric shapes, including quadrilaterals and triangles, based on their properties and sizes; identify acute and obtuse angles and compare and order angles up to two right angles by size.",
        "meta_desc": "Free Year 4 maths worksheets on angles and shapes: acute, right and obtuse angles, comparing and ordering angles, equilateral, isosceles, scalene and right-angled triangles, and quadrilaterals such as the trapezium, rhombus and kite. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Compare every angle with a right angle: smaller is acute, bigger is obtuse, and two right angles make a straight line.",
        "key_sub": "The size of an angle is how wide it opens, not how long its arms are. Sort triangles and quadrilaterals by their equal sides, parallel sides and right angles; turning a shape never changes its name.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, rows of angles) so they stay readable."""
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
        mark_large(u, "(four [a-z]+ labelled A to D|three angles labelled|angle P and angle Q|capital letters made)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
