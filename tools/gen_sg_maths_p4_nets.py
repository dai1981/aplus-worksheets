# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Nets (MOE 2021 Primary Mathematics Syllabus, Standard, Geometry)
  python3 tools/gen_sg_maths_p4_nets.py
HTML attributes use single quotes (no backslashes in the JSON). Singapore (British) English.

P4 students identify 2D drawings of cube, cuboid, cone, cylinder, prism and pyramid, identify nets
and the solid formed by a net.

Pictures (checked in code):
  solids      drawn from 3-D vertices and faces; a face is shown when it faces the viewer, edges of hidden
              faces only are dashed; faces, edges and vertices are counted from the same data (V − E + F = 2)
  cube nets   fold3d() really folds the squares round a unit cube. A pattern is a net only when the 6 squares
              land on 6 different faces (cross-checked with the rolling-cube test fold_cube()).
              All 35 hexominoes are enumerated: exactly 11 are nets of a cube (asserted).
  cuboid nets a strip L, W, L, W wide (all H tall) with an L × W lid on the top edge and the bottom edge
              of L-wide faces; broken nets are checked against the same rule (box_ok()).
  prism nets  regular polygon bases with every side glued to a rectangle edge of the same length
  labels      never touch each other, are inside one face or outside all faces, and no line crosses them
Wrong answers come from real student mistakes: any 6 squares make a cube, prism vs pyramid, cube vs cuboid,
cylinder vs cone, counting only the faces you can see, edges and vertices swapped, a 2D shape name for a solid.
"""
import itertools, json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GREY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
DZX, DZY = 0.55, 0.40

CUBE, RP, TP, SP, TPY = "cube", "cuboid", "triangular prism", "square pyramid", "triangular pyramid"
CYL, CONE = "cylinder", "cone"
CUBOID, TET = RP, TPY

def num(x):
    """4.0 -> 4, 4.5 -> 4.5"""
    return "%g" % x


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("0 ") or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


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


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ drawing
def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3 - t.count(".") * 0.6) * fs * 0.6


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def circle_pts(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


class Canvas:
    """Collects shapes and text (screen coordinates, y down), tracks the bounding box, then writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2, col=GREEN, dashed=False):
        self.el.append(("p", pts, fill, sw, col, dashed))
        self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=3, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.polys.append(circle_pts(c, r))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

    def dot(self, c, r=4, col=INK):
        self.el.append(("c", c, r, col, 0, col))
        self.segs.append((c, c))
        self.grow(c[0] - r, c[1] - r, c[0] + r, c[1] + r)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", pts, dashed, sw, col))
        for a, b in zip(pts, pts[1:]):
            self.segs.append((a, b))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:                                   # labels never touch each other
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        """Each label is inside one face or outside all faces, and no line runs through it."""
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert all(h == len(pts) for h in hit), ("label crosses a face edge", (x0, y0, x1, y1), hit)
            for a, b in self.segs:
                for i in range(41):
                    x, y = a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40
                    assert not (x0 - 2 < x < x1 + 2 and y0 - 2 < y < y1 + 2), ("line through a label", (x0, y0))

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3],
                            " stroke-dasharray='6 4'" if e[5] else ""))
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            elif e[0] == "pl":
                _, pts, dashed, sw, col = e
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5, check=True):
        if check:
            self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1
        return svg_wrap(W, H, self.body(ox, oy), label)


def row_svg(cvs, caps, label, gap=24, fs=17, col=GREEN):
    """Pictures side by side with a caption (A, B, C, D or a word) under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, cap in zip(cvs, caps):
        cv.check()
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - (H - h) / 2
        parts.append(cv.body(ox, oy))
        parts.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + cw / 2, H + 8 + fs * 0.86, fs, col, cap))
        x += cw + gap
    W = x - gap
    pad = 5
    body = "<g transform='translate(%d,%d)'>%s</g>" % (pad, pad, "".join(parts))
    return svg_wrap(int(math.ceil(W + 2 * pad)), int(math.ceil(H + 8 + fs * 1.1 + 2 * pad)), body, label)


def grid_svg(cvs, label, cell=118):
    """2 x 2 grid of pictures labelled A-D."""
    W = H = 2 * cell
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, cell, H - 4, GREY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, W - 4, cell, GREY)]
    for k, cv in enumerate(cvs):
        cv.check()
        x0, y0 = (k % 2) * cell, (k // 2) * cell
        aw, ah = cell - 26, cell - 10
        w, h = cv.size()
        assert w <= aw and h <= ah, ("too big for the grid", w, h)
        ox = cv.x0 - (x0 + 21 + (aw - w) / 2)
        oy = cv.y0 - (y0 + 5 + (ah - h) / 2)
        s.append(cv.body(ox, oy))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)

# ------------------------------------------------------------ cube nets
def rot_y(s):
    return ((0, 0, s), (0, 1, 0), (-s, 0, 0))


def rot_x(s):
    return ((1, 0, 0), (0, 0, -s), (0, s, 0))


def mat(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def fold_cube(cells):
    """Roll a cube over the squares. Returns {cell: face} or None when two squares land on the same face."""
    cells = list(cells)
    assert len(cells) == 6 and len(set(cells)) == 6
    I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    R = {cells[0]: I}
    todo = [cells[0]]
    while todo:
        c = todo.pop(0)
        for (dc, dr), M in [((1, 0), rot_y(1)), ((-1, 0), rot_y(-1)), ((0, 1), rot_x(-1)), ((0, -1), rot_x(1))]:
            n = (c[0] + dc, c[1] + dr)
            if n in cells and n not in R:
                R[n] = mat(M, R[c])
                todo.append(n)
    assert len(R) == 6, "squares are not connected"
    face = {c: tuple(m[2][i] * -1 for i in range(3)) for c, m in R.items()}
    return face if len(set(face.values())) == 6 else None


def opposite(cells, a):
    face = fold_cube(cells)
    return [c for c in cells if face[c] == tuple(-v for v in face[a])][0]


CUBE_NETS = [
    [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)],      # cross
    [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (0, 2)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 2)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (2, 0), (1, 2)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (2, 2)],
    [(0, 1), (1, 1), (2, 1), (3, 1), (3, 0), (0, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],      # staircase
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1)],      # 3 and 3
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (1, 2)],      # 2-3-1
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2)],
]
SAME_SIDE = "two squares are on the same side of the row of 4, so they fold onto the same face and one face is left open"
BAD_NETS = [
    ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 0)], SAME_SIDE),
    ([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (3, 0)], SAME_SIDE),
    ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (2, 2)], SAME_SIDE),
    ([(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 0)], "5 squares in a row wrap all the way round, so the first and last squares overlap"),
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], "it has a 2-by-2 block of squares, but only 3 faces of a cube meet at a corner, so two squares overlap"),
]
for _n in CUBE_NETS:
    assert fold_cube(_n), _n
for _n, _w in BAD_NETS:
    assert fold_cube(_n) is None, _n


def draw_cells(cv, cells, k, ox=0, oy=0, letters=None, fill=FILL, fs=18):
    c0 = min(c for c, r in cells)
    r0 = min(r for c, r in cells)
    for c, r in cells:
        x, y = ox + (c - c0) * k, oy + (r - r0) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], fill)
    if letters:
        for (c, r), t in letters.items():
            cv.text(ox + (c - c0 + 0.5) * k, oy + (r - r0 + 0.5) * k, t, fs, col=GREEN if t != "?" else RED)


def cube_net_cv(cells, k=40, letters=None):
    cv = Canvas()
    draw_cells(cv, cells, k, letters=letters)
    return cv


# ------------------------------------------------------------ other nets
def box_net_cv(L, W, H, k, top_on=0, bot_on=0):
    """Strip of 4 faces (L, W, L, W wide, H tall) with an L × W face above face top_on and below face bot_on."""
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cv = Canvas()
    for i in range(4):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL)
    cv.poly([(xs[top_on] * k, -W * k), ((xs[top_on] + L) * k, -W * k), ((xs[top_on] + L) * k, 0), (xs[top_on] * k, 0)], FILL)
    cv.poly([(xs[bot_on] * k, H * k), ((xs[bot_on] + L) * k, H * k), ((xs[bot_on] + L) * k, (H + W) * k), (xs[bot_on] * k, (H + W) * k)], FILL)
    return cv


def tri_prism_cv(k, tri=("equi", 2), L=3, rects=3, ends=(("top", 1), ("bot", 1))):
    """Triangular prism net: rectangles side by side (L tall); each triangle sits on the top or bottom edge
    of a rectangle. tri = ('equi', s) or ('right', a, b, c). rects < 3 or one end gives broken nets."""
    if tri[0] == "equi":
        s = tri[1]
        widths = [s, s, s]
    else:
        _, a, b, c = tri
        assert a * a + b * b == c * c
        widths = [a, b, c]
    cv = Canvas()
    xs = [0]
    for w in widths[:rects]:
        xs.append(xs[-1] + w)
    for i in range(rects):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, L * k), (xs[i] * k, L * k)], FILL)
    for side, i in ends:
        x0, x1 = xs[i], xs[i + 1]
        if tri[0] == "equi":
            apex = ((x0 + x1) / 2, -s * math.sqrt(3) / 2)
            other = [abs(widths[(i + 1) % 3] - s), abs(widths[(i + 2) % 3] - s)]
            assert max(other) < 1e-9                          # every edge of the triangle matches a rectangle edge
        else:
            assert i == 1                                     # leg b on the middle rectangle, leg a up from its left end
            apex = (x0, -a)
            assert abs(math.hypot(x1 - apex[0], apex[1]) - c) < 1e-9 and abs(-apex[1] - widths[0]) < 1e-9
        pts = [(x0, 0), (x1, 0), apex]
        if side == "bot":
            pts = [(x, L - y) for x, y in pts]
        cv.poly([(x * k, y * k) for x, y in pts], BASE)
    return cv


def pyramid_cv(s, l, k, sides=(0, 1, 2, 3)):
    """Square base s × s with a triangle (base s, height l) on the listed sides."""
    S, Lk = s * k, l * k
    cv = Canvas()
    cv.poly([(0, 0), (S, 0), (S, S), (0, S)], BASE)
    tris = [[(0, 0), (S, 0), (S / 2, -Lk)], [(S, 0), (S, S), (S + Lk, S / 2)],
            [(0, S), (S, S), (S / 2, S + Lk)], [(0, 0), (0, S), (-Lk, S / 2)]]
    for i in sides:
        cv.poly(tris[i], FILL)
    return cv


def tetra_cv(k):
    H = math.sqrt(3)
    P = lambda x, y: (x * k, y * k)
    p0, p1, p2 = P(0, H), P(2, H), P(1, 0)
    m01, m12, m02 = P(1, H), P(1.5, H / 2), P(0.5, H / 2)
    cv = Canvas()
    for t in [[p0, m01, m02], [m01, p1, m12], [m02, m12, p2]]:
        cv.poly(t, FILL)
    cv.poly([m02, m01, m12], BASE)
    return cv


# ------------------------------------------------------------ 3-D shapes
class Solid:
    def __init__(self, verts, faces):
        self.v, self.f = verts, faces
        cx = sum(p[0] for p in verts) / len(verts)
        cy = sum(p[1] for p in verts) / len(verts)
        cz = sum(p[2] for p in verts) / len(verts)
        self.normals = []
        for fc in faces:
            a, b, c = (verts[i] for i in fc[:3])
            u = [b[i] - a[i] for i in range(3)]
            w = [c[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            if sum(n[i] * (a[i] - (cx, cy, cz)[i]) for i in range(3)) < 0:
                n = [-x for x in n]
            self.normals.append(n)
        edges = {}
        for fi, fc in enumerate(faces):
            for i in range(len(fc)):
                e = tuple(sorted((fc[i], fc[(i + 1) % len(fc)])))
                edges.setdefault(e, []).append(fi)
        assert all(len(x) == 2 for x in edges.values())
        self.edges = edges
        F, E, V = len(faces), len(edges), len(verts)
        assert V - E + F == 2, (V, E, F)
        self.count = {"faces": F, "edges": E, "vertices": V}

    def cv(self, k):
        view = (DZX, DZY, -1)
        vis = [sum(n[i] * view[i] for i in range(3)) > 1e-9 for n in self.normals]
        P = lambda p: ((p[0] + p[2] * DZX) * k, -(p[1] + p[2] * DZY) * k)
        cv = Canvas()
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = self.normals[fi]
                L = math.sqrt(sum(x * x for x in n))
                col = TOP3 if n[1] / L > 0.6 else SIDE if n[0] / L > 0.6 else FILL
                cv.poly([P(self.v[i]) for i in fc], col, 2.4)
        for (a, b), fs in self.edges.items():
            if not any(vis[f] for f in fs):
                cv.line(P(self.v[a]), P(self.v[b]), dashed=True, sw=1.6)
        return cv


def cuboid(L=1.7, H=1.0, W=0.9):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(v, f)


def prism(base, D):
    """base: polygon in the x-y plane (front), extruded back by D."""
    n = len(base)
    v = [(x, y, 0) for x, y in base] + [(x, y, D) for x, y in base]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


def pyramid(base, apex):
    """base: polygon in the x-z plane (y = 0); apex: (x, y, z)."""
    n = len(base)
    v = [(x, 0, z) for x, z in base] + [apex]
    f = [list(range(n))] + [[i, (i + 1) % n, n] for i in range(n)]
    return Solid(v, f)


def reg(n, r, start=-90):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


SOLIDS = {
    CUBE: lambda: cuboid(1.2, 1.2, 1.2),
    CUBOID: lambda: cuboid(),
    TP: lambda: prism([(0, 0), (1.3, 0), (0.65, 1.0)], 1.5),
    SP: lambda: pyramid([(0, 0), (1.4, 0), (1.4, 1.4), (0, 1.4)], (0.7, 1.5, 0.7)),
    TET: lambda: pyramid([(0, 0.6), (1.0, 0), (1.4, 1.1)], (0.8, 1.5, 0.55)),
    "pentagonal prism": lambda: prism([(-p[0], -p[1]) for p in reg(5, 0.7)], 1.3),
    "hexagonal prism": lambda: prism(reg(6, 0.7, 0), 1.3),
    "pentagonal pyramid": lambda: pyramid(reg(5, 0.8, -100), (0, 1.5, 0)),
    "hexagonal pyramid": lambda: pyramid(reg(6, 0.8, -15), (0, 1.5, 0)),
}


def loft(bot, H):
    """Upright prism: base polygon in the x-z plane at y = 0, top at y = H."""
    n = len(bot)
    v = [(x, 0, z) for x, z in bot] + [(x, H, z) for x, z in bot]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


# other drawings of the same solids (key -> name, solid)
DRAW = {
    "cuboid tall": (CUBOID, lambda: cuboid(0.9, 1.7, 0.8)),
    "cuboid flat": (CUBOID, lambda: cuboid(1.8, 0.55, 1.1)),
    "triangular prism standing": (TP, lambda: loft([(0, 0), (1.4, 0), (0.4, 1.2)], 1.5)),
}
COUNTS = {CUBE: (6, 12, 8), CUBOID: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5), TET: (4, 6, 4),
          "pentagonal prism": (7, 15, 10), "hexagonal prism": (8, 18, 12),
          "pentagonal pyramid": (6, 10, 6), "hexagonal pyramid": (7, 12, 7)}
for _k, _f in SOLIDS.items():
    assert tuple(_f().count[x] for x in ("faces", "edges", "vertices")) == COUNTS[_k], _k
for _k, (_n, _f) in DRAW.items():
    assert tuple(_f().count[x] for x in ("faces", "edges", "vertices")) == COUNTS[_n], _k
    SOLIDS[_k] = _f


def solid_cv(kind, k=60):
    return SOLIDS[kind]().cv(k)


def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def cylinder_cv(rx=42, ry=13, h=90):
    cv = Canvas()
    body = ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)
    cv.poly(body, FILL, 0.01)
    cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
    cv.line((-rx, 0), (-rx, h))
    cv.line((rx, 0), (rx, h))
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    return cv


def cone_cv(rx=46, ry=14, h=100):
    cv = Canvas()
    cv.poly([(0, 0)] + ellipse(0, h, rx, ry, 180, 0), FILL, 0.01)
    cv.line((0, 0), (-rx, h))
    cv.line((0, 0), (rx, h))
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    return cv


def shape_svg(kind, label=None):
    cv = cylinder_cv() if kind == "cylinder" else cone_cv() if kind == "cone" else solid_cv(kind)
    return cv.svg(label or "a solid")


# ------------------------------------------------------------ folding a net round a cube (3-D)
SIDES = {"T": ((0, 0), (1, 0), (0, -1)), "B": ((0, 1), (1, 1), (0, 1)),
         "L": ((0, 0), (0, 1), (-1, 0)), "R": ((1, 0), (1, 1), (1, 0))}


def vadd(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(3))


def vneg(v):
    return tuple(-x for x in v)


def fold3d(cells):
    """Fold the squares round the unit cube [0,1]^3. Each square gets a frame (O, U, V, N): the point of the
    square at (u, v) is O + u·U + v·V and N points into the cube. Folding is done along a spanning tree."""
    cells = list(cells)
    fr = {cells[0]: ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))}
    todo = [cells[0]]
    while todo:
        c = todo.pop(0)
        O, U, V, N = fr[c]
        nb = {(1, 0): (vadd(O, U), N, V, vneg(U)), (-1, 0): (vadd(O, N), vneg(N), V, U),
              (0, 1): (vadd(O, V), U, N, vneg(V)), (0, -1): (vadd(O, N), U, vneg(N), V)}
        for (dc, dr), f in nb.items():
            n = (c[0] + dc, c[1] + dr)
            if n in cells and n not in fr:
                fr[n] = f
                todo.append(n)
    assert len(fr) == 6, "squares are not connected"
    return fr


def centre2(f):
    O, U, V, N = f
    return tuple(2 * O[i] + U[i] + V[i] for i in range(3))


def is_net(cells):
    fr = fold3d(cells)
    return len({centre2(f) for f in fr.values()}) == 6


def pt3(f, u, v):
    O, U, V, N = f
    return tuple(O[i] + u * U[i] + v * V[i] for i in range(3))


def opp(cells, a):
    fr = fold3d(cells)
    want = tuple(2 - x for x in centre2(fr[a]))
    return [c for c in cells if centre2(fr[c]) == want][0]


def touching3d(cells, a):
    """Faces next to face a on the folded cube (all except a and its opposite)."""
    return [c for c in cells if c != a and c != opp(cells, a)]


def corner_faces(cells, pt):
    """pt = screen corner (x, y) in cell units. Returns the 3 cells that meet at that corner of the cube."""
    fr = fold3d(cells)
    p = None
    for c in cells:
        u, v = pt[0] - c[0], pt[1] - c[1]
        if u in (0, 1) and v in (0, 1):
            p = pt3(fr[c], u, v)
            break
    assert p is not None
    out = []
    for c in cells:
        for u in (0, 1):
            for v in (0, 1):
                if pt3(fr[c], u, v) == p and c not in out:
                    out.append(c)
    assert len(out) == 3, out
    return out


def boundary_sides(cells):
    return [(c, s) for c in cells for s, (_, _, d) in SIDES.items() if (c[0] + d[0], c[1] + d[1]) not in cells]


def side3d(cells, cs):
    fr = fold3d(cells)
    c, s = cs
    a, b, _ = SIDES[s]
    return frozenset([pt3(fr[c], *a), pt3(fr[c], *b)])


def glue_partner(cells, cs):
    """The other open edge of the net that is taped to edge cs when the cube is folded."""
    me = side3d(cells, cs)
    p = [x for x in boundary_sides(cells) if x != cs and side3d(cells, x) == me]
    assert len(p) == 1, (cs, p)
    return p[0]


# all 35 hexominoes; exactly 11 are nets of a cube
def _norm(cells):
    x0 = min(c for c, r in cells)
    y0 = min(r for c, r in cells)
    return tuple(sorted((c - x0, r - y0) for c, r in cells))


def _syms(cells):
    out = []
    for fx in (1, -1):
        for sw in (False, True):
            for fy in (1, -1):
                out.append(_norm([((r if sw else c) * fx, (c if sw else r) * fy) for c, r in cells]))
    return out


def hexominoes():
    shapes = {((0, 0),)}
    for _ in range(5):
        nxt = set()
        for sh in shapes:
            for c, r in sh:
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (c + d[0], r + d[1])
                    if n not in sh:
                        nxt.add(min(_syms(list(sh) + [n])))
        shapes = nxt
    return sorted(shapes)


HEX = hexominoes()
assert len(HEX) == 35
GOOD = [h for h in HEX if is_net(h)]
BAD = [h for h in HEX if not is_net(h)]
assert len(GOOD) == 11 and len(BAD) == 24
for _h in HEX:                                              # two different folding tests agree
    assert (fold_cube(_h) is not None) == is_net(_h)
    if is_net(_h):
        for _c in _h:                                       # every open edge is taped to exactly one other
            glue_partner(_h, (_c, "T")) if (_c[0], _c[1] - 1) not in _h else None
        assert len(boundary_sides(_h)) == 14


def dims(cells):
    return (max(c for c, r in cells) - min(c for c, r in cells) + 1, max(r for c, r in cells) - min(r for c, r in cells) + 1)


def orient(cells, rnd):
    """A random turn or flip that keeps the pattern wider than tall."""
    opts = [s for s in _syms(cells) if dims(s)[0] >= dims(s)[1]]
    return list(rnd.choice(sorted(set(opts))))


def has_run(cells, n):
    s = set(cells)
    for c, r in cells:
        if all((c + i, r) in s for i in range(n)) or all((c, r + i) in s for i in range(n)):
            return True
    return False


def has_block(cells):
    s = set(cells)
    return any({(c + 1, r), (c, r + 1), (c + 1, r + 1)} <= s for c, r in cells)


def bad_reason(cells):
    if has_run(cells, 5):
        return "5 squares in a row wrap all the way round, so the first and last squares land on the same face"
    if has_block(cells):
        return "it has a 2-by-2 block of squares, but only 3 faces of a cube meet at a corner, so two squares overlap"
    return "two of its squares fold onto the same face, so one face of the cube is left open"


BAD_POOL = [b for b in BAD if max(dims(b)) <= 5]             # no silly row of 6


# ------------------------------------------------------------ drawing nets
def cube_cells_cv(cells, k, letters=None, fs=18):
    cv = Canvas()
    draw_cells(cv, cells, k, letters=letters, fs=fs)
    return cv


def four_nets(nets, k=18):
    return row_svg([cube_cells_cv(n, k) for n in nets], list("ABCD"), "four nets labelled A to D", gap=26)


def grid_row(cvs):
    return row_svg(cvs, list("ABCD"), "four nets labelled A to D", gap=26)


def box_net(L, W, H, k, top_on=0, bot_on=0):
    assert top_on in (0, 2) and bot_on in (0, 2)              # the L × W faces sit on an L-wide face
    return box_net_cv(L, W, H, k, top_on, bot_on)


def cyl_net_cv(r, h, k, mode="ok"):
    """Rectangle 2πr long and h tall (it rolls into the curved surface); the circles touch the long edges.
    mode: ok | same (both circles on the top edge) | one (only one circle) | short (circles on the short edges)."""
    W = 2 * math.pi * r
    cv = Canvas()
    cv.poly([(0, 0), (W * k, 0), (W * k, h * k), (0, h * k)], FILL)
    if mode == "ok":
        cs = [(W * 0.3 * k, -r * k), (W * 0.62 * k, (h + r) * k)]
    elif mode == "same":
        cs = [(W * 0.25 * k, -r * k), (W * 0.75 * k, -r * k)]
    elif mode == "one":
        cs = [(W * 0.5 * k, -r * k)]
    else:
        cs = [(-r * k, h * k / 2), ((W + r) * k, h * k / 2)]
    for c in cs:
        cv.circle(c, r * k, BASE, 2)
    return cv


def cone_net_cv(r, s, k, base=True):
    """Sector (radius s = slant height, arc = 2πr) opening downwards, with the base circle touching the arc."""
    th = 360.0 * r / s
    S = s * k
    arc = [(S * math.cos(math.radians(90 - th / 2 + th * i / 48)), S * math.sin(math.radians(90 - th / 2 + th * i / 48)))
           for i in range(49)]
    cv = Canvas()
    cv.poly([(0, 0)] + arc, FILL)
    if base:
        cv.circle((0, S + r * k), r * k, BASE, 2)
    return cv


def tri_circle_cv(k):
    """Wrong net for a cone: a triangle and a circle (a cone has a curved surface, not a flat triangle)."""
    cv = Canvas()
    cv.poly([(-1.1 * k, 2.6 * k), (1.1 * k, 2.6 * k), (0, 0)], FILL)
    cv.circle((0, 3.4 * k), 0.8 * k, BASE, 2)
    return cv




# ------------------------------------------------------------ more nets: regular prisms, pyramids, cuboids
def flat_bottom(n, r):
    return reg(n, r, -90 + 180.0 / n)


def cen(b):
    return (sum(p[0] for p in b) / len(b), sum(p[1] for p in b) / len(b))


def poly_on_edge(p, q, n, d):
    """Regular n-gon with edge p-q, built on the side of the edge that the unit vector d points to."""
    s = math.hypot(q[0] - p[0], q[1] - p[1])
    a = s / (2 * math.tan(math.pi / n))
    c = ((p[0] + q[0]) / 2 + d[0] * a, (p[1] + q[1]) / 2 + d[1] * a)
    r = math.hypot(p[0] - c[0], p[1] - c[1])
    t0 = math.atan2(p[1] - c[1], p[0] - c[0])
    for sg in (1, -1):
        pts = [(c[0] + r * math.cos(t0 + sg * 2 * math.pi * i / n), c[1] + r * math.sin(t0 + sg * 2 * math.pi * i / n)) for i in range(n)]
        if math.hypot(pts[1][0] - q[0], pts[1][1] - q[1]) < 1e-6:
            for i in range(n):                                  # every side the same length as the rectangle edge
                j = (i + 1) % n
                assert abs(math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]) - s) < 1e-6
            return pts
    raise AssertionError("no polygon")


def prism_net_cv(n, k, L=1.7, rects=None, bases=(("top", 1), ("bot", 1))):
    """n rectangles (1 wide, L tall) side by side; a regular n-gon base on the top or bottom edge of a rectangle."""
    rects = n if rects is None else rects
    cv = Canvas()
    for i in range(rects):
        cv.poly([(i * k, 0), ((i + 1) * k, 0), ((i + 1) * k, L * k), (i * k, L * k)], FILL)
    for side, i in bases:
        assert i < rects
        if side == "top":
            pts = poly_on_edge((i * k, 0), ((i + 1) * k, 0), n, (0, -1))
        else:
            pts = poly_on_edge((i * k, L * k), ((i + 1) * k, L * k), n, (0, 1))
        cv.poly(pts, BASE)
    return cv


def pyramid_net_cv(n, k, l=1.15, sides=None):
    """Regular n-gon base (side 1) with an isosceles triangle (height l) on each listed side."""
    base = [(x * k, -y * k) for x, y in flat_bottom(n, 0.5 / math.sin(math.pi / n))]
    assert l > 0.5 / math.tan(math.pi / n) + 0.05               # the triangles are tall enough to fold up and meet
    cv = Canvas()
    cv.poly(base, BASE)
    cx, cy = cen(base)
    for i in (range(n) if sides is None else sides):
        p, q = base[i], base[(i + 1) % n]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        d = math.hypot(mx - cx, my - cy)
        cv.poly([p, q, (mx + (mx - cx) / d * l * k, my + (my - cy) / d * l * k)], FILL)
    return cv


def box_ok(ws, H, lids):
    """A strip of 4 rectangles (widths ws, all H tall) folds into a ring when opposite faces match.
    The ring is closed by one lid on the top edge and one on the bottom edge; a lid on face i is ws[i] wide
    and must be as deep as the next face (ws[i + 1]) to fit."""
    if len(ws) != 4 or ws[0] != ws[2] or ws[1] != ws[3]:
        return False
    if sorted(s for s, i, d in lids) != ["bot", "top"]:
        return False
    return all(d == ws[(i + 1) % 4] for s, i, d in lids)


def box_any(ws, H, k, lids):
    xs = [0]
    for w in ws:
        xs.append(xs[-1] + w)
    cv = Canvas()
    for i in range(len(ws)):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL)
    for s, i, d in lids:
        y0, y1 = (-d, 0) if s == "top" else (H, H + d)
        cv.poly([(xs[i] * k, y0 * k), (xs[i + 1] * k, y0 * k), (xs[i + 1] * k, y1 * k), (xs[i] * k, y1 * k)], BASE)
    return cv


BL, BW, BH = 2, 1, 1.4
BOX_GOOD = [
    ([BL, BW, BL, BW], [("top", 0, BW), ("bot", 0, BW)]),
    ([BL, BW, BL, BW], [("top", 0, BW), ("bot", 2, BW)]),
    ([BL, BW, BL, BW], [("top", 1, BL), ("bot", 3, BL)]),
    ([BL, BW, BL, BW], [("top", 2, BW), ("bot", 0, BW)]),
]
BOX_BAD = [  # (strip, lids, reason)
    ([BL, BW, BL, BW], [("top", 0, BW), ("top", 2, BW)],
     "both lids are on the top edge, so they fold onto the same face and the bottom is left open"),
    ([BL, BL, BW, BW], [("top", 0, BW), ("bot", 0, BW)],
     "the 4 sides are in the wrong order, so the faces that should be opposite are not the same size"),
    ([BL, BW, BL, BW], [("top", 0, BW), ("bot", 0, BL)],
     "one lid is too long, so it does not match the face opposite it"),
    ([BL, BW, BL, BW], [("top", 1, BL)],
     "it has only 5 faces, so one face of the cuboid is missing"),
]
for _w, _l in BOX_GOOD:
    assert box_ok(_w, BH, _l)
for _w, _l, _r in BOX_BAD:
    assert not box_ok(_w, BH, _l)


def box_cv(spec, k=16):
    return box_any(spec[0], BH, k, spec[1])


# ------------------------------------------------------------ set 1: name the solid from its drawing
NAME_ASK = ["What is the name of this solid?", "Name this solid.", "Which solid is shown in this drawing?"]
DRAW_E = {
    CUBE: "All 6 faces are squares of the same size, so it is a cube.",
    CUBOID: "It has 6 rectangular faces, and the faces opposite each other match, so it is a cuboid. "
            "It is not a cube, because its faces are not all squares.",
    TP: "It has 2 matching triangles at the ends, joined by rectangles, so it is a triangular prism.",
    SP: "It has 1 square base and 4 triangles that meet at a point at the top, so it is a square pyramid. "
        "A pyramid is named after the shape of its base.",
    TPY: "It has a triangle base and 3 more triangles that meet at a point, so it is a triangular pyramid.",
    "pentagonal prism": "It has 2 matching pentagons (5 sides) at the ends, joined by rectangles, so it is a pentagonal prism.",
    "hexagonal prism": "It has 2 matching hexagons (6 sides) at the ends, joined by rectangles, so it is a hexagonal prism.",
    "hexagonal pyramid": "It has 1 hexagon base (6 sides) and triangles that meet at a point, so it is a hexagonal pyramid. "
                         "A prism would have 2 hexagons and rectangles.",
    CYL: "It has 2 flat circular faces and 1 curved surface, so it is a cylinder.",
    CONE: "It has 1 flat circular face, 1 curved surface and a point at the top, so it is a cone.",
}
DRAW_WRONG = {
    CUBE: ["square", SP, TP], CUBOID: [CUBE, "rectangle", TP], "cuboid flat": [CUBE, "rectangle", SP],
    TP: [TPY, SP, "triangle"], "triangular prism standing": [TPY, CUBOID, "triangle"],
    SP: [TPY, TP, "triangle"], TPY: [SP, TP, "triangle"],
    "pentagonal prism": ["hexagonal prism", "pentagonal pyramid", "pentagon"],
    "hexagonal prism": ["pentagonal prism", "hexagonal pyramid", "hexagon"],
    "hexagonal pyramid": ["hexagonal prism", "pentagonal pyramid", TPY],
    CYL: [CONE, "circle", CUBOID], CONE: [CYL, "pyramid", "triangle"],
}


def name_of(key):
    return DRAW[key][0] if key in DRAW else key


def solid_any(key, small=False):
    if key == CYL:
        return cylinder_cv(26, 8, 56) if small else cylinder_cv()
    if key == CONE:
        return cone_cv(28, 8, 60) if small else cone_cv()
    return solid_cv(key, 40 if small else 60)


def four_solids(keys):
    return row_svg([solid_any(x, True) for x in keys], list("ABCD"), "four solids labelled A to D", gap=26)


def set_draw(rnd, pos):
    its = []
    keys = [CUBE, CUBOID, "cuboid flat", TP, "triangular prism standing", SP, TPY, "pentagonal prism",
            "hexagonal prism", "hexagonal pyramid", CYL, CONE]
    for i, key in enumerate(keys):
        nm = name_of(key)
        extra = " A prism can stand on its end; it is still a prism." if key == "triangular prism standing" else ""
        its.append(mcq(fig(solid_any(key).svg("a solid")) + NAME_ASK[i % 3], nm, DRAW_WRONG[key], DRAW_E[nm] + extra))
    its.append(mcq(fig(solid_any("cuboid tall").svg("a cuboid with dashed lines")) +
                   "In this drawing of a cuboid, what do the dashed lines show?",
                   "edges at the back that you cannot see", ["the edges at the front", "lines to cut along", "the middle of the faces"],
                   "A drawing of a solid is flat. Dashed lines show the hidden edges at the back, so you can see the whole shape."))
    asks = [("Which of these solids is a cuboid?", CUBOID, [TP, SP, CYL],
             "%s has 6 rectangular faces. The others are a triangular prism, a square pyramid and a cylinder."),
            ("Which of these solids is a pyramid?", SP, [TP, CUBOID, CYL],
             "%s has a square base and triangles that meet at a point. A prism has 2 matching ends joined by rectangles."),
            ("Which of these solids is a prism?", "hexagonal prism", ["hexagonal pyramid", CONE, TPY],
             "%s has 2 matching hexagons at the ends joined by rectangles. The others come to a point, so they are not prisms."),
            ("Which of these solids is a cylinder?", CYL, [CONE, "pentagonal prism", SP],
             "%s has 2 flat circular faces and a curved surface. A cone has only 1 circle and a point.")]
    for q, right, wrong, e in asks:
        p = pos.next()
        ks = wrong[:]
        rnd.shuffle(ks)
        ks.insert(p, right)
        its.append(mcq_fixed(fig(four_solids(ks)) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    its.append(mcq("A solid has 2 flat faces that are circles and 1 curved surface. What is the solid?", CYL, [CONE, "circle", CUBOID],
                   DRAW_E[CYL] + " A cone has only 1 circle."))
    its.append(mcq("A solid has 1 flat face that is a circle, 1 curved surface and a point at the top. What is the solid?", CONE,
                   [CYL, "pyramid", "triangle"], DRAW_E[CONE] + " A pyramid has flat triangles, not a curved surface."))
    its.append(mcq("The base of a pyramid is a pentagon. What is the name of the pyramid?", "pentagonal pyramid",
                   ["pentagonal prism", SP, "hexagonal pyramid"],
                   "A pyramid is named after its base. A pentagon has 5 sides, so it is a pentagonal pyramid. A prism would have 2 pentagons."))
    assert len(its) == 20, len(its)
    return {"title": "Name the solid from its drawing", "items": its}


# ------------------------------------------------------------ set 2: faces, edges and vertices
FACES_DESC = {CUBE: "6 square faces", RP: "6 rectangular faces", TP: "5 faces (2 triangles and 3 rectangles)",
              SP: "5 faces (1 square and 4 triangles)", TPY: "4 triangular faces",
              "pentagonal prism": "7 faces (2 pentagons and 5 rectangles)", "hexagonal prism": "8 faces (2 hexagons and 6 rectangles)",
              "hexagonal pyramid": "7 faces (1 hexagon and 6 triangles)"}


def fev_e(kind):
    F, E, V = COUNTS[kind]
    return "A %s has %s, %d edges and %d vertices." % (kind, FACES_DESC[kind], E, V)


def set_fev(rnd):
    its = []
    D = " Dashed lines show the edges at the back that you cannot see."
    rows = [  # kind, what, wrong, picture, extra explanation
        (CUBE, "vertices", [6, 12, 4], True, " Vertices are the corners: 4 at the front and 4 at the back."),
        (RP, "faces", [3, 4, 12], True, " You can see only 3 faces. The bottom, the back and one side are hidden, but they still count."),
        (RP, "edges", [8, 6, 9], False, " There are 4 edges on the top, 4 on the bottom and 4 going up the sides."),
        (TP, "faces", [6, 3, 9], True, D),
        (TP, "edges", [6, 5, 12], True, " 3 edges round each triangle end and 3 long edges joining them: 3 + 3 + 3 = 9."),
        (TP, "vertices", [5, 9, 3], False, " There are 3 corners on each triangle end: 3 + 3 = 6."),
        (SP, "faces", [4, 8, 6], True, " Do not forget the square base underneath."),
        (SP, "edges", [4, 5, 12], True, " 4 edges round the base and 4 going up to the top: 4 + 4 = 8."),
        (SP, "vertices", [4, 8, 6], False, " 4 corners on the base and 1 at the top: 4 + 1 = 5."),
        (TPY, "faces", [3, 6, 5], True, " Do not forget the triangle base underneath."),
        (TPY, "edges", [4, 3, 8], False, " 3 edges round the base and 3 going up to the top: 3 + 3 = 6."),
        ("pentagonal prism", "faces", [5, 10, 15], True, " 2 pentagon ends + 5 rectangles = 7."),
        ("hexagonal prism", "vertices", [6, 18, 8], False, " 6 corners on each hexagon end: 6 + 6 = 12."),
    ]
    for kind, what, wrong, pic, extra in rows:
        ans = dict(zip(("faces", "edges", "vertices"), COUNTS[kind]))[what]
        if pic:
            q = fig(shape_svg(kind, "a " + kind)) + "This is a %s. How many %s does it have?" % (kind, what)
        else:
            q = "How many %s does a %s have?" % (what, kind)
        its.append(mcq(q, ans, wrong, fev_e(kind) + extra))
    its.append(mcq(fig(shape_svg(CYL, "a cylinder")) + "How many flat faces does a cylinder have?", 2, [1, 0, 3],
                   "A cylinder has 2 flat circular faces, one at each end, and 1 curved surface round the side."))
    its.append(mcq(fig(shape_svg(CONE, "a cone")) + "What surfaces does a cone have?", "1 flat face and 1 curved surface",
                   ["2 flat faces and 1 curved surface", "1 flat face only", "2 curved surfaces"],
                   "A cone has 1 flat circular face (the base) and 1 curved surface that comes to a point."))
    its.append(mcq(fig(shape_svg("hexagonal pyramid")) + "This is a hexagonal pyramid. How many faces does it have?", 7, [8, 6, 12],
                   "The base is 1 hexagon, and there is 1 triangle on each of its 6 sides: 1 + 6 = 7 faces. "
                   "8 is the number of faces of a hexagonal prism (2 hexagons and 6 rectangles)."))
    its.append(mcq(fig(shape_svg("hexagonal pyramid")) + "This is a hexagonal pyramid. How many edges does it have?", 12, [6, 7, 18],
                   "6 edges round the hexagon base and 6 edges going up to the top: 6 + 6 = 12. 7 is the number of vertices (6 + 1)."))
    its.append(mcq("Which solid has 5 faces and 5 vertices?", SP, [TP, RP, TPY],
                   "A square pyramid has 5 faces (1 square, 4 triangles) and 5 vertices (4 on the base, 1 at the top). "
                   "A triangular prism also has 5 faces, but it has 6 vertices."))
    its.append(mcq("Which solid has 9 edges and 6 vertices?", TP, [SP, RP, TPY],
                   "A triangular prism has 9 edges (3 + 3 + 3) and 6 vertices (3 on each triangle end)."))
    its.append(mcq("A cube and a cuboid are compared. Which statement is true?", "They have the same number of edges",
                   ["A cuboid has more faces", "A cube has more vertices", "A cuboid has fewer edges"],
                   "Both have 6 faces, 12 edges and 8 vertices. Only the shapes of the faces are different: a cube has 6 squares."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 3: which nets make a cube?
def add_square_q(rnd, base_net, p):
    """5 squares of a net + 4 dashed places A-D; only the place at index p completes a net of a cube."""
    cells = list(base_net)
    for drop in rnd.sample(cells, len(cells)):
        five = [c for c in cells if c != drop]
        s = set(five)
        # still in one piece?
        seen, todo = {five[0]}, [five[0]]
        while todo:
            c = todo.pop()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n in s and n not in seen:
                    seen.add(n)
                    todo.append(n)
        if len(seen) < 5:
            continue
        spots = sorted({(c[0] + d[0], c[1] + d[1]) for c in five for d in ((1, 0), (-1, 0), (0, 1), (0, -1))} - s)
        ok = [x for x in spots if is_net(five + [x])]
        bad = [x for x in spots if not is_net(five + [x])]
        if len(bad) >= 3:
            break
    else:
        raise AssertionError("no base")
    right = rnd.choice(ok)
    wrong = rnd.sample(bad, 3)
    places = wrong[:p] + [right] + wrong[p:]
    k = 34
    allc = five + places
    c0, r0 = min(c for c, r in allc), min(r for c, r in allc)
    cv = Canvas()
    for c, r in five:
        x, y = (c - c0) * k, (r - r0) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], FILL)
    for i, (c, r) in enumerate(places):
        x, y = (c - c0) * k, (r - r0) * k
        cv.poly([(x + 3, y + 3), (x + k - 3, y + 3), (x + k - 3, y + k - 3), (x + 3, y + k - 3)], "#ffffff", 1.6, BLUE, True)
        cv.text(x + k / 2, y + k / 2, "ABCD"[i], 17, col=BLUE)
    for i, x in enumerate(places):
        assert is_net(five + [x]) == (i == p)
    q = (fig(cv.svg("five squares of a net and places A to D for one more square")) +
         "These 5 squares are part of a net of a cube. Where should the 6th square go?")
    e = ("With the square at %s, the 6 squares fold onto 6 different faces. At each of the other places, two squares "
         "would fold onto the same face and one face would be left open." % "ABCD"[p])
    return mcq_fixed(q, list("ABCD"), "ABCD"[p], e)


YES = "Yes, it folds into a cube"
NO = "No, two squares land on the same face"


def set_cube_nets(rnd):
    its = []
    pos = Pos(rnd)
    good = GOOD[:]
    rnd.shuffle(good)
    bad = BAD_POOL[:]
    rnd.shuffle(bad)
    gi = bi = 0
    for _ in range(5):                                   # which IS a net
        p = pos.next()
        cells = [orient(b, rnd) for b in bad[bi:bi + 3]]
        bi += 3
        cells.insert(p, orient(good[gi % 11], rnd))
        gi += 1
        for x, c in enumerate(cells):
            assert is_net(c) == (x == p)
        e = ("%s folds into a cube with no gaps and no overlaps. Each of the others has two squares that fold onto "
             "the same face, so one face is left open." % "ABCD"[p])
        its.append(mcq_fixed(fig(four_nets(cells)) + "Which of these is a net of a cube?", list("ABCD"), "ABCD"[p], e))
    for _ in range(5):                                   # which is NOT a net
        p = pos.next()
        b = bad[bi % len(bad)]
        bi += 1
        cells = [orient(good[(gi + j) % 11], rnd) for j in range(3)]
        gi += 3
        cells.insert(p, orient(b, rnd))
        for x, c in enumerate(cells):
            assert is_net(c) == (x != p)
        e = "%s is not a net of a cube: %s. The other three each fold into a cube." % ("ABCD"[p], bad_reason(b))
        its.append(mcq_fixed(fig(four_nets(cells)) + "Which of these is NOT a net of a cube?", list("ABCD"), "ABCD"[p], e))
    for j in range(4):                                   # add the 6th square
        its.append(add_square_q(rnd, good[(gi + j) % 11], pos.next()))
    gi += 4
    # one pattern: does it fold into a cube?
    ch = [YES, NO, "No, a cube needs 8 squares", "No, a cube needs 12 squares"]
    tests = [good[gi % 11], good[(gi + 1) % 11], [b for b in BAD_POOL if has_run(b, 5)][0],
             [b for b in BAD_POOL if has_block(b) and not has_run(b, 4)][0]]
    for t in tests:
        cells = orient(t, rnd)
        if is_net(cells):
            e = ("Yes. Fold the squares one at a time: they cover all 6 faces of the cube with no overlaps. "
                 "A cube has 6 faces, so its net has 6 squares (8 is the number of vertices and 12 the number of edges).")
            its.append(mcq(fig(cube_cells_cv(cells, 30).svg("a pattern of 6 squares")) + "Does this pattern fold into a cube?", YES, ch[1:], e))
        else:
            e = "No: %s. A cube has 6 faces, so 6 squares is the right number, but they must be in the right places." % bad_reason(cells)
            its.append(mcq(fig(cube_cells_cv(cells, 30).svg("a pattern of 6 squares")) + "Does this pattern fold into a cube?", NO,
                           [YES] + ch[2:], e))
    # how many of 4 are nets
    cells = [orient(good[(gi + 2) % 11], rnd), orient(bad[bi % len(bad)], rnd), orient(good[(gi + 3) % 11], rnd),
             orient(good[(gi + 4) % 11], rnd)]
    n = sum(is_net(c) for c in cells)
    assert n == 3
    its.append(mcq(fig(four_nets(cells)) + "How many of these patterns are nets of a cube?", n, [4, 2, 1],
                   "Fold each one in your head. A, C and D fold into a cube. B does not: %s." % bad_reason(cells[1])))
    its.append(mcq("How many different nets does a cube have? (A net that is only turned or flipped over counts as the same net.)",
                   11, [6, 12, 8],
                   "A cube has 11 different nets. 6 is the number of faces, 12 the number of edges and 8 the number of vertices."))
    assert len(its) == 20, len(its)
    return {"title": "Which nets fold into a cube?", "items": its}


# ------------------------------------------------------------ lettered nets
def lettered(cells, rnd):
    letters = list("ABCDEF")
    rnd.shuffle(letters)
    return dict(zip(cells, letters))


def dice_q(rnd, cells):
    nums = {}
    k = 1
    for c in cells:
        if c in nums:
            continue
        o = opp(cells, c)
        nums[c], nums[o] = k, 7 - k
        k += 1
    hide = rnd.choice(cells)
    ans = nums[hide]
    o = opp(cells, hide)
    near = [c for c in cells if c not in (hide, o) and abs(c[0] - hide[0]) + abs(c[1] - hide[1]) == 1]
    rest = [c for c in cells if c not in (hide, o) and c not in near]
    show = [o] + (near + rest)[:2]
    lab = {c: str(nums[c]) for c in show}
    lab[hide] = "?"
    q = (fig(cube_cells_cv(cells, 40, lab).svg("net of a dice with some numbers missing")) +
         "This is a net of a dice. The numbers on opposite faces add up to 7. What number goes on the face marked ?")
    wrong = [7 - nums[c] for c in show[1:]] + [nums[o], 7]
    return mcq(q, ans, wrong,
               "When the net is folded, the face marked ? is opposite the %d. So the missing number is 7 − %d = %d." % (nums[o], nums[o], ans))


def box_letters_q(L, W, H, k, top_on, bot_on, ask):
    """Cuboid net: strip faces P, Q, R, S (L, W, L, W wide), lid T above face top_on, lid U below face bot_on.
    In the ring, face i is opposite face i + 2; the two lids are opposite each other."""
    assert box_ok([L, W, L, W], H, [("top", top_on, W), ("bot", bot_on, W)])
    cv = box_any([L, W, L, W], H, k, [("top", top_on, W), ("bot", bot_on, W)])
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    letters = list("PQRSTU")
    centres = [((xs[i] + xs[i + 1]) / 2 * k, H / 2 * k) for i in range(4)]
    centres += [((xs[top_on] + L / 2) * k, -W / 2 * k), ((xs[bot_on] + L / 2) * k, (H + W / 2) * k)]
    for (x, y), t in zip(centres, letters):
        cv.text(x, y, t, 17, col=GREEN)
    oppo = {"P": "R", "R": "P", "Q": "S", "S": "Q", "T": "U", "U": "T"}
    near = {"P": ["Q", "S", "T", "U"], "Q": ["P", "R", "T", "U"], "R": ["Q", "S", "T", "U"], "S": ["R", "P", "T", "U"],
            "T": ["PQRS"[top_on]] + [x for x in "PQRS" if x != "PQRS"[top_on]], "U": ["PQRS"[bot_on]] + [x for x in "PQRS" if x != "PQRS"[bot_on]]}
    q = (fig(cv.svg("net of a cuboid with faces P to U")) +
         "This net is folded into a cuboid. Which face is opposite face %s?" % ask)
    b = oppo[ask]
    if ask in "TU":
        e = ("Faces T and U are the two lids: one folds over the top and the other folds under the bottom, so they are opposite. "
             "Face %s touches face %s in the net, so it is next to it, not opposite." % (near[ask][0], ask))
    else:
        mid = "PQRS"[("PQRS".index(ask) + 1) % 4] if "PQRS".index(ask) < 2 else "PQRS"[("PQRS".index(ask) - 1) % 4]
        e = ("Faces %s and %s are the same size and have one face (%s) between them in the strip, so they fold onto opposite sides. "
             "In a cuboid, opposite faces are always the same size and shape." % (ask, b, mid))
    return mcq(q, "face " + b, ["face " + x for x in near[ask]], e)


# ------------------------------------------------------------ set 4: nets of cuboids, prisms and pyramids
SHAPES4 = ["triangle", "rectangle", "square", "circle"]


def set_nets(rnd, pos):
    its = []
    good, bad = BOX_GOOD[:], BOX_BAD[:]
    rnd.shuffle(good)
    rnd.shuffle(bad)
    # which IS a net of a cuboid (twice)
    for j in range(2):
        p = pos.next()
        ws = bad[3 * j % 4: 3 * j % 4 + 3] if j == 0 else [bad[3], bad[0], bad[1]]
        cvs = [box_cv(b) for b in ws]
        cvs.insert(p, box_cv(good[j]))
        reasons = "; ".join("%s: %s" % ("ABCD"[x if x < p else x + 1], b[2]) for x, b in enumerate(ws))
        its.append(mcq_fixed(fig(grid_row(cvs)) + "Which of these is a net of a cuboid?", list("ABCD"), "ABCD"[p],
                             "%s folds into a closed cuboid. The others do not (%s)." % ("ABCD"[p], reasons)))
    # which is NOT a net of a cuboid
    p = pos.next()
    b = bad[2]
    cvs = [box_cv(g) for g in good[1:4]]
    cvs.insert(p, box_cv(b))
    its.append(mcq_fixed(fig(grid_row(cvs)) + "Which of these is NOT a net of a cuboid?", list("ABCD"), "ABCD"[p],
                         "%s is not a net of a cuboid: %s. The other three each fold into a closed cuboid." % ("ABCD"[p], b[2])))
    # triangular prism, square pyramid, triangular pyramid, pentagonal prism
    p = pos.next()
    cvs = [pyramid_cv(2, 2.2, 15), tri_prism_cv(16, ("equi", 2), 2.6, rects=2, ends=(("top", 0), ("bot", 0))), tetra_cv(40)]
    cvs.insert(p, tri_prism_cv(16, ("equi", 2), 2.6))
    its.append(mcq_fixed(fig(grid_row(cvs)) + "Which net folds into a triangular prism?", list("ABCD"), "ABCD"[p],
                         "%s has 2 triangles and 3 rectangles. Of the others, one makes a square pyramid, one makes a triangular pyramid, "
                         "and one has only 2 rectangles, so it cannot close up." % "ABCD"[p]))
    p = pos.next()
    cvs = [pyramid_cv(2, 2.2, 15, sides=(0, 1, 2)), tri_prism_cv(16, ("equi", 2), 2.6), box_cv(good[0])]
    cvs.insert(p, pyramid_cv(2, 2.2, 15))
    its.append(mcq_fixed(fig(grid_row(cvs)) + "Which net folds into a square pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has 1 square and 4 triangles, one on each side of the square. One wrong net has only 3 triangles, "
                         "so one side is left open. The others make a triangular prism and a cuboid." % "ABCD"[p]))
    p = pos.next()
    cvs = [pyramid_cv(2, 2.2, 15), pyramid_net_cv(3, 40, math.sqrt(3) / 2, sides=(0, 1)), tri_prism_cv(16, ("equi", 2), 2.6)]
    cvs.insert(p, tetra_cv(40))
    its.append(mcq_fixed(fig(grid_row(cvs)) + "Which net folds into a triangular pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has 4 triangles: 1 base and 3 that fold up to meet at a point. One wrong net has only 3 triangles. "
                         "The others make a square pyramid and a triangular prism." % "ABCD"[p]))
    p = pos.next()
    cvs = [prism_net_cv(5, 14, 1.5, bases=(("top", 2),)), prism_net_cv(6, 13, 1.4, bases=(("top", 1), ("bot", 3))),
           pyramid_net_cv(5, 18, 1.2)]
    cvs.insert(p, prism_net_cv(5, 14, 1.5, bases=(("top", 2), ("bot", 1))))
    its.append(mcq_fixed(fig(grid_row(cvs)) + "Which net folds into a pentagonal prism?", list("ABCD"), "ABCD"[p],
                         "%s has 2 pentagons and 5 rectangles. One wrong net has only 1 pentagon, one has 2 hexagons "
                         "(a hexagonal prism) and one has 1 pentagon with triangles (a pentagonal pyramid)." % "ABCD"[p]))
    # what shape is the missing face?
    its.append(mcq(fig(tri_prism_cv(24, ("equi", 2), 3, ends=(("top", 1),)).svg("net with a face missing")) +
                   "This net of a triangular prism has one face missing. What shape is the missing face?", "triangle",
                   ["rectangle", "square", "circle"],
                   "A triangular prism has 2 triangles and 3 rectangles. The net shows 3 rectangles and only 1 triangle, "
                   "so the missing face is the second triangle (the other end)."))
    its.append(mcq(fig(pyramid_cv(2, 2.2, 22, sides=(0, 1, 3)).svg("net with a face missing")) +
                   "This net of a square pyramid has one face missing. What shape is the missing face?", "triangle",
                   ["square", "rectangle", "circle"],
                   "A square pyramid has 1 square and 4 triangles. The net shows only 3 triangles, so a triangle is missing "
                   "on the bottom side of the square. The square base is already there."))
    its.append(mcq(fig(box_any([BL, BW, BL, BW], BH, 22, [("top", 0, BW)]).svg("net with a face missing")) +
                   "This net of a cuboid has one face missing. What shape is the missing face?", "rectangle",
                   ["square", "triangle", "circle"],
                   "A cuboid has 6 faces. The net shows 5, so the bottom is missing. It must match the top face, "
                   "which is a rectangle, because opposite faces of a cuboid are the same."))
    # opposite faces of a cuboid
    its.append(box_letters_q(3, 2, 1.5, 22, 2, 0, "Q"))
    its.append(box_letters_q(3, 1.5, 2, 20, 0, 2, "T"))
    # counting and measuring
    its.append(mcq("A cuboid measures 5 cm by 3 cm by 2 cm. How many faces in its net measure 5 cm by 3 cm?", 2, [1, 4, 3],
                   "The top and the bottom are both 5 cm by 3 cm. Opposite faces of a cuboid are the same, so the faces come in 3 pairs."))
    its.append(mcq("How many triangles are there in the net of a square pyramid?", 4, [5, 1, 8],
                   "There is 1 triangle on each side of the square base: 4 triangles. Together with the square, the net has 5 faces."))
    its.append(mcq("How many rectangles are there in the net of a hexagonal prism?", 6, [2, 8, 12],
                   "A hexagon has 6 sides, and each side joins a rectangle, so there are 6 rectangles. The net also has 2 hexagons: 8 faces in all."))
    its.append(mcq("The net of a pyramid has 1 pentagon. How many triangles does it have?", 5, [2, 6, 10],
                   "A pentagon has 5 sides, and there is 1 triangle on each side: 5 triangles. 2 would be the pentagons of a prism."))
    its.append(mcq("Which shapes make the net of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "1 square and 4 triangles", "4 triangles"],
                   "The 2 triangles are the ends and the 3 rectangles join them. 1 square and 4 triangles is the net of a square pyramid."))
    its.append(mcq("The ends of a triangular prism are triangles with all 3 sides 3 cm. The prism is 10 cm long. "
                   "What size is each rectangle in its net?", "3 cm by 10 cm", ["3 cm by 3 cm", "10 cm by 10 cm", "6 cm by 10 cm"],
                   "Each rectangle is as wide as one side of the triangle (3 cm) and as long as the prism (10 cm)."))
    its.append(mcq("In the net of a square pyramid, the square has sides of 6 cm. How long is the bottom edge of each triangle?",
                   "6 cm", ["12 cm", "24 cm", "3 cm"],
                   "Each triangle is joined to one side of the square, so its bottom edge is as long as that side: 6 cm. "
                   "24 cm is the distance all the way round the square."))
    its.append(mcq("A cube has edges of 4 cm. Which shapes make its net?", "6 squares of side 4 cm",
                   ["4 squares and 2 rectangles", "8 squares of side 4 cm", "6 squares of side 24 cm"],
                   "A cube has 6 faces, and every face is a square with sides as long as the edges: 4 cm. "
                   "8 is the number of vertices, not faces."))
    assert len(its) == 20, len(its)
    return {"title": "Nets of cuboids, prisms and pyramids", "items": its}


# ------------------------------------------------------------ set 5: which solid does this net make?
NET_ASK = ["Which solid does this net make?", "This net is folded up. Which solid does it make?",
           "What solid can be made from this net?"]
NET_E = {
    CUBE: "There are 6 squares, all the same size. They fold into a cube.",
    CUBOID: "There are 6 rectangles in 3 matching pairs. They fold into a cuboid.",
    TP: "There are 2 triangles (the ends) and 3 rectangles joining them. They fold into a triangular prism.",
    SP: "There is 1 square (the base) and 4 triangles that meet at a point. They fold into a square pyramid.",
    TPY: "There are 4 triangles and nothing else. One is the base and the other 3 meet at a point, so they fold into a triangular pyramid.",
    CYL: "There are 2 circles (the flat ends) and a rectangle that rolls up into the curved surface. They fold into a cylinder.",
    CONE: "There is 1 circle (the base) and a fan shape (part of a circle) that rolls up into a curved surface with a point. They fold into a cone.",
    "pentagonal prism": "There are 2 pentagons (the ends) and 5 rectangles joining them. They fold into a pentagonal prism.",
    "hexagonal pyramid": "There is 1 hexagon (the base) and 6 triangles that meet at a point. They fold into a hexagonal pyramid.",
}
WRONG_NAME = {CUBE: ["square", SP, TP], CUBOID: [CUBE, TP, "rectangle"], TP: [TPY, SP, CUBOID], SP: [TP, TPY, CUBE],
              TPY: [SP, TP, "triangle"], CYL: [CONE, "circle", CUBOID], CONE: [CYL, SP, "circle"],
              "pentagonal prism": ["pentagonal pyramid", "hexagonal prism", CUBOID],
              "hexagonal pyramid": ["hexagonal prism", "pentagonal pyramid", "hexagon"]}


def set_which(rnd, P):
    its = []
    nets = [(cube_cells_cv(orient(GOOD[3], rnd), 32), CUBE, ""),
            (box_any([3, 2, 3, 2], 1.5, 20, [("top", 2, 2), ("bot", 0, 2)]), CUBOID, ""),
            (box_any([2.5, 2.5, 2.5, 2.5], 1, 18, [("top", 0, 2.5), ("bot", 2, 2.5)]), CUBOID,
             " The top and bottom are squares, but the 4 sides are thin rectangles, so it is not a cube."),
            (tri_prism_cv(24, ("right", 3, 4, 5), 2.5), TP, " The triangles do not have to have equal sides."),
            (pyramid_cv(2, 2.2, 26), SP, ""),
            (tetra_cv(62), TPY, ""),
            (cyl_net_cv(0.75, 2.2, 24), CYL, ""),
            (cone_net_cv(1, 2.6, 30), CONE, ""),
            (prism_net_cv(5, 22, 1.5, bases=(("top", 1), ("bot", 3))), "pentagonal prism", ""),
            (pyramid_net_cv(6, 26, 1.25), "hexagonal pyramid", "")]
    for i, (cv, obj, extra) in enumerate(nets):
        its.append(mcq(fig(cv.svg("net of a solid")) + NET_ASK[i % 3], obj, WRONG_NAME[obj], NET_E[obj] + extra))
    n, he, his = P.next()
    its.append(mcq("Mrs Lim’s class makes gift boxes for Children’s Day. Each net has 6 rectangles in 3 matching pairs. "
                   "What solid is each box?", CUBOID, [CUBE, TP, SP],
                   "6 rectangles in matching pairs fold into a cuboid. A cube would need 6 squares, all the same size."))
    n, he, his = P.next()
    its.append(mcq("%s makes a birthday party hat from a fan shape (part of a circle). The hat has no base. "
                   "What solid shape is the hat?" % n, CONE, [CYL, "pyramid", "triangle"],
                   "The fan shape rolls up into a curved surface that comes to a point, so the hat is a cone without its circle base. "
                   "A triangle has straight edges, so it cannot roll into a round hat."))
    n, he, his = P.next()
    its.append(mcq("%s draws a net with 2 hexagons and 6 rectangles for a gift box. Which solid will the box be?" % n,
                   "hexagonal prism", ["hexagonal pyramid", CUBOID, "pentagonal prism"],
                   "2 matching hexagons joined by rectangles make a prism, so it is a hexagonal prism. A pyramid has only 1 base and triangles."))
    n, he, his = P.next()
    cells = orient(GOOD[7], rnd)
    d = dice_q(rnd, cells)
    d["q"] = d["q"].replace("This is a net of a dice.", "%s makes a dice for a maths game from this net." % n)
    its.append(d)
    n, he, his = P.next()
    its.append(mcq("%s’s Scouts CCA puts up a tent shaped like a triangular prism, with a floor. "
                   "Each face is one piece of fabric. How many pieces of fabric does the tent have?" % n, 5, [3, 6, 4],
                   "A triangular prism has 5 faces: 2 triangle ends and 3 rectangles (2 sloping sides and the floor)."))
    n, he, his = P.next()
    its.append(mcq("%s builds a model of a square pyramid with straws and balls of plasticine: one straw for each edge and one ball "
                   "for each vertex. What does %s need?" % (n, he), "8 straws, 5 balls",
                   ["5 straws, 8 balls", "8 straws, 4 balls", "5 straws, 5 balls"],
                   "A square pyramid has 8 edges (4 round the base and 4 up to the top) and 5 vertices (4 on the base and 1 at the top)."))
    n, he, his = P.next()
    its.append(mcq("%s makes a model cube with straws, one straw for each edge. Each straw is 10 cm long. "
                   "What is the total length of the straws?" % n, "120 cm", ["60 cm", "80 cm", "100 cm"],
                   "A cube has 12 edges: 12 × 10 = 120 cm. 60 cm counts the faces (6) and 80 cm counts the vertices (8)."))
    n, he, his = P.next()
    its.append(mcq("%s cuts out a net of a cube (6 squares in one piece) and folds it. How many edges must %s tape to close the cube?" % (n, he),
                   7, [12, 6, 5],
                   "A cube has 12 edges. The 6 squares of the net are joined by 5 folds, so 12 − 5 = 7 edges are still open and need tape."))
    n, he, his = P.next()
    its.append(mcq("%s makes a net of a cube from card. Each square is 10 cm by 10 cm. What is the area of the net?" % n,
                   "600 cm²", ["400 cm²", "100 cm²", "60 cm²"],
                   "Each square has an area of 10 × 10 = 100 cm². There are 6 squares: 6 × 100 = 600 cm². "
                   "400 cm² counts only 4 faces."))
    its.append(mcq("A drink can is a cylinder. Its paper label goes all the way round the can once, with no overlap. "
                   "What shape is the label when it is peeled off and laid flat?", "rectangle",
                   ["circle", "triangle", "fan shape"],
                   "The curved surface of a cylinder unrolls into a rectangle. The 2 circles are the top and bottom of the can."))
    assert len(its) == 20, len(its)
    return {"title": "Which solid does the net make? Boxes, hats and tents", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


CROSS = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)]
SAME_SIDE_BAD = [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 0)]
assert is_net(CROSS) and not is_net(SAME_SIDE_BAD)


def body_html():
    solids1 = row_svg([solid_any(CUBE, True), solid_any(CUBOID, True), solid_any(CYL, True)],
                      [CUBE, CUBOID, CYL], "drawings of a cube, a cuboid and a cylinder", gap=34, fs=14, col=INK)
    solids2 = row_svg([solid_any(CONE, True), solid_any(TP, True), solid_any(SP, True)],
                      [CONE, "prism", "pyramid"], "drawings of a cone, a prism and a pyramid", gap=34, fs=14, col=INK)
    row1 = row_svg([cube_cells_cv(CROSS, 22), box_any([2, 1, 2, 1], 1.4, 15, [("top", 0, 1), ("bot", 0, 1)]),
                    tri_prism_cv(18, ("equi", 2), 2.6)],
                   [CUBE, CUBOID, TP], "nets of a cube, a cuboid and a triangular prism", gap=34, fs=14, col=INK)
    row2 = row_svg([pyramid_cv(2, 2.2, 17), cyl_net_cv(0.5, 1.3, 22), cone_net_cv(1, 2.4, 22)],
                   [SP, CYL, CONE], "nets of a square pyramid, a cylinder and a cone", gap=34, fs=14, col=INK)
    good_bad = row_svg([cube_cells_cv(CUBE_NETS[6], 22), cube_cells_cv(SAME_SIDE_BAD, 22)],
                       ["a net of a cube", "NOT a net of a cube"], "a net of a cube and a pattern that is not a net", gap=40, fs=14, col=INK)
    lab = dict(zip(CROSS, "ABCDEF"))
    assert lab[opp(CROSS, (0, 1))] == "C" and lab[opp(CROSS, (1, 0))] == "F"
    letters = cube_cells_cv(CROSS, 34, lab).svg("net of a cube with faces A to F")
    return (
        "<h2>Drawings of solids</h2>"
        "<p>A <b>solid</b> takes up space. On paper we draw it flat. <b>Dashed lines</b> show the edges at the back that you cannot see.</p>"
        "<figure class='sn-fig'>" + solids1 + "</figure>"
        "<figure class='sn-fig'>" + solids2 +
        "<figcaption>A prism has 2 matching ends joined by rectangles. A pyramid has 1 base and triangles that meet at a point.</figcaption></figure>"
        "<p>A prism or a pyramid is named after its base: a triangular prism has triangle ends, a square pyramid has a square base.</p>"
        "<h2>What is a net?</h2>"
        "<p>A <b>net</b> is a flat shape that folds up to make a solid. Each part of the net becomes one face. "
        "Count the shapes in the net to name the solid.</p>"
        "<figure class='sn-fig'>" + row1 + "</figure>"
        "<figure class='sn-fig'>" + row2 +
        "<figcaption>A cylinder’s rectangle rolls into a tube. A cone’s fan shape rolls into a curved surface with a point.</figcaption></figure>" +
        table(["Solid", "Shapes in the net", "Faces", "Edges", "Vertices"], [
            ["Cube", "6 equal squares", "6", "12", "8"],
            ["Cuboid", "6 rectangles (3 matching pairs)", "6", "12", "8"],
            ["Triangular prism", "2 triangles, 3 rectangles", "5", "9", "6"],
            ["Square pyramid", "1 square, 4 triangles", "5", "8", "5"],
            ["Triangular pyramid", "4 triangles", "4", "6", "4"],
            ["Cylinder", "2 circles, 1 rectangle", "2 flat faces, 1 curved surface", "–", "–"],
            ["Cone", "1 circle, 1 fan shape", "1 flat face, 1 curved surface", "–", "–"],
        ]) +
        ex("Example 1", "A net has 1 square and 4 triangles. Which solid does it make?",
           "The square is the base. The 4 triangles fold up and meet at a point.", "a square pyramid") +
        "<h2>Nets of a cube</h2>"
        "<p>A cube has <b>11</b> different nets. A pattern of 6 squares is <b>not</b> a net if two squares fold onto the same face.</p>"
        "<figure class='sn-fig'>" + good_bad +
        "<figcaption>On the right, the two top squares are on the same side of the row of 4. They fold onto the same face, so one face is left open.</figcaption></figure>"
        "<p>These are never nets of a cube: <b>5 squares in a row</b>, a <b>2-by-2 block</b> of squares, "
        "and two squares on the <b>same side</b> of a row of 4.</p>"
        "<p>Squares in a straight line with <b>one square between them</b> become <b>opposite</b> faces.</p>"
        "<figure class='sn-fig'>" + letters + "</figure>" +
        ex("Example 2", "This net is folded into a cube. Which face is opposite face A?",
           "A, B and C are in a straight line, with B between A and C. So A and C are opposite.", "face C") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking any 6 squares make a cube", "Fold each square in your head. No row of 5, no 2-by-2 block, no two squares on the same side of a row of 4"],
            ["Mixing up prisms and pyramids", "A prism has 2 matching ends and rectangles; a pyramid has 1 base and triangles that meet at a point"],
            ["Counting only the faces you can see", "Count the hidden faces too: a cuboid always has 6 faces"],
            ["Calling every box a cube", "A cube has 6 equal squares; a cuboid has rectangles in matching pairs"],
            ["Mixing up a cylinder and a cone", "A cylinder’s net has 2 circles and a rectangle; a cone’s has 1 circle and a fan shape"],
            ["Swapping edges and vertices", "Edges are the lines where faces meet; vertices are the corners"],
        ])
    )


FAQ = [
    {"q": "What do P4 students learn about nets?",
     "a": "In Primary 4, students recognise drawings of cubes, cuboids, cones, cylinders, prisms and pyramids, identify the net of a solid, and name the solid that a net folds into."},
    {"q": "How many nets does a cube have?",
     "a": "A cube has 11 different nets. Each one has 6 squares, and no two squares fold onto the same face."},
    {"q": "What is the most common mistake with nets?",
     "a": "Thinking that any 6 squares make a cube. A row of 5 squares, a 2-by-2 block, or two squares on the same side of a row of 4 will never fold into a cube."},
    {"q": "Are nets in the MOE syllabus?",
     "a": "Yes. Nets are part of Geometry in the Primary 4 MOE Mathematics Syllabus (2021), and the ideas come back in later work on solids and in the PSLE."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. A-D picture questions keep their order."""
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
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64816)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_draw(rnd, pos), set_fev(rnd), set_cube_nets(rnd), set_nets(rnd, Pos(rnd)), set_which(rnd, P)]
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
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "nets", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Nets of Solids: Cubes, Cuboids, Prisms and Pyramids",
        "seo_title": "P4 Nets Worksheets: Free Primary 4 Maths on Solids and Nets with Answers (MOE Syllabus)",
        "short_title": "Nets",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 4: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Identifying and drawing 2D representations of cube, cuboid, cone, cylinder, prism and pyramid; identifying nets; identifying the solid formed by a net",
        "meta_desc": "Free P4 maths practice on nets: name solids, count faces, edges and vertices, find nets of a cube and cuboid. 100 questions with answers.",
        "key_big": "A net is a flat shape that folds into a solid: each part of the net becomes one face.",
        "key_sub": "6 equal squares make a cube; 2 triangles and 3 rectangles make a triangular prism; 1 square and 4 triangles make a square pyramid.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four [a-z]+ labelled A to D|five squares of a net")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
