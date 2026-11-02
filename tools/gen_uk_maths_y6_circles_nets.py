# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Circles and nets (National Curriculum in England, Geometry – properties of shapes)
  python tools/gen_uk_maths_y6_circles_nets.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 6 names the parts of a circle (centre, radius, diameter, circumference) and knows that the
diameter is twice the radius. No π and no circumference calculations (that is Key Stage 3).
3-D shapes: cube, cuboid, triangular prism, square-based pyramid, tetrahedron (faces, edges, vertices).

Pictures (checked in code):
  solids      drawn from 3-D vertices and faces; a face is shown when it faces the viewer, edges of hidden
              faces only are dashed; faces, edges and vertices are counted from the same data (Euler: V − E + F = 2)
  cube nets   fold_cube() rolls a cube over the squares: a net is valid only when the 6 squares land on
              6 different faces (this also gives opposite faces and the dice question)
  prism nets  every triangle edge is glued to a rectangle edge of the same length (asserted)
  labels      never touch each other, are inside one face or outside all faces, and no line crosses them
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
DZX, DZY = 0.55, 0.40

CUBE, CUBOID, TP, SP, TET = "cube", "cuboid", "triangular prism", "square-based pyramid", "tetrahedron"


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

    def poly(self, pts, fill, sw=2, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
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
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
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
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, cell, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, W - 4, cell, GRAY)]
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


# ------------------------------------------------------------ circles
def pol(r, deg):
    """Point at angle deg (anticlockwise, screen y down) and distance r from (0, 0)."""
    t = math.radians(deg)
    return (r * math.cos(t), -r * math.sin(t))


def circ(r=50):
    cv = Canvas()
    cv.circle((0, 0), r)
    return cv


def part_fig(part, deg=0, r=50):
    """Circle with one part in red: radius, diameter, circumference or centre."""
    cv = Canvas()
    if part == "circumference":
        cv.circle((0, 0), r, sw=5, col=RED)
    else:
        cv.circle((0, 0), r)
    if part == "radius":
        cv.line((0, 0), pol(r, deg), sw=4, col=RED)
    elif part == "diameter":
        cv.line(pol(r, deg), pol(r, deg + 180), sw=4, col=RED)
    if part == "centre":
        cv.dot((0, 0), 6, RED)
    else:
        cv.dot((0, 0), 4)
    return cv


def lines_fig(kind, r=40):
    """For 'which picture shows a diameter / radius'."""
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.dot((0, 0), 3.5)
    if kind == "diameter":
        cv.line(pol(r, 25), pol(r, 205), sw=3.5, col=RED)
    elif kind == "radius":
        cv.line((0, 0), pol(r, 120), sw=3.5, col=RED)
    elif kind == "chord":                                   # misses the centre by 14 px
        d = 14
        h = math.sqrt(r * r - d * d)
        cv.line((-h, -d), (h, -d), sw=3.5, col=RED)
    elif kind == "short":                                    # from the centre, stops before the edge
        cv.line((0, 0), pol(r * 0.55, 300), sw=3.5, col=RED)
    elif kind == "half":                                     # through the centre, stops before the far edge
        cv.line(pol(r, 150), pol(r * 0.45, 330), sw=3.5, col=RED)
    elif kind == "outside":                                  # from the centre, past the edge
        cv.line((0, 0), pol(r + 14, 60), sw=3.5, col=RED)
    return cv


def abc_fig():
    """Circle with centre O, diameter AB, radius OC, lines AC and BC."""
    r = 62
    cv = Canvas()
    cv.circle((0, 0), r)
    A, B, C = pol(r, 180), pol(r, 0), pol(r, 65)
    for p, q in [(A, B), ((0, 0), C), (A, C), (B, C)]:
        cv.line(p, q, sw=2.4, col=INK)
    cv.dot((0, 0), 4)
    cv.text(A[0] - 8, A[1], "A", 17, "end")
    cv.text(B[0] + 8, B[1], "B", 17, "start")
    cv.text(C[0] + 4, C[1] - 13, "C", 17)
    cv.text(0, 15, "O", 17)
    return cv.svg("circle with centre O and points A, B and C on the circle")


def radius_fig(val, kind="radius", r=70):
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.dot((0, 0), 4)
    if kind == "radius":
        cv.line((0, 0), (r, 0), sw=3, col=INK)
        cv.text(r / 2, -14, val)
    else:
        cv.line((-r, 0), (r, 0), sw=3, col=INK)
        cv.text(-r * 0.42, -14, val)
    return cv.svg("circle with its %s labelled %s" % (kind, val))


def square_circle_fig(lab, side=120):
    cv = Canvas()
    h = side / 2
    cv.poly([(-h, -h), (h, -h), (h, h), (-h, h)], "#ffffff", 2.4, INK)
    cv.circle((0, 0), h, sw=3)
    cv.dot((0, 0), 4)
    cv.text(0, h + 16, lab)
    return cv.svg("a circle that fits exactly inside a square")


def row_circles_fig(n, lab, r=36):
    cv = Canvas()
    W = 2 * r * n
    cv.poly([(0, 0), (W, 0), (W, 2 * r), (0, 2 * r)], "#ffffff", 2.4, INK)
    for i in range(n):
        c = (r + 2 * r * i, r)
        cv.circle(c, r, sw=2.6)
        cv.dot(c, 3.5)
    cv.text(W / 2, 2 * r + 16, lab)
    return cv.svg("%d equal circles in a row that fit exactly inside a rectangle" % n)


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
}
COUNTS = {"cube": (6, 12, 8), "cuboid": (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5), TET: (4, 6, 4),
          "pentagonal prism": (7, 15, 10), "hexagonal prism": (8, 18, 12)}
for _k, _f in SOLIDS.items():
    assert tuple(_f().count[x] for x in ("faces", "edges", "vertices")) == COUNTS[_k], _k


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
    return cv.svg(label or "a 3-D shape")


# ------------------------------------------------------------ set 1: parts of a circle
PARTS = ["radius", "diameter", "circumference", "centre"]
PART_E = {
    "radius": "It goes from the centre to the edge of the circle, so it is a radius. A diameter goes all the way across through the centre.",
    "diameter": "It goes from one side of the circle to the other and passes through the centre, so it is a diameter.",
    "circumference": "The circumference is the distance all the way round the edge of the circle. It is the perimeter of the circle.",
    "centre": "The centre is the point in the middle. Every point on the circumference is the same distance from the centre.",
}


def set_parts(rnd, pos):
    its = []
    asks = {"radius": ["What is the red line called?", "The red line is part of this circle. What is it called?",
                       "Which part of the circle is shown in red?"],
            "diameter": ["What is the red line called?", "The red line is part of this circle. What is it called?",
                         "Which part of the circle is shown in red?"],
            "circumference": ["The edge of this circle is shown in red. What is it called?",
                              "What is the red part of this circle called?"],
            "centre": ["What is the red point called?"]}
    wrong = {"radius": ["diameter", "circumference", "centre"], "diameter": ["radius", "circumference", "centre"],
             "circumference": ["diameter", "radius", "centre"], "centre": ["radius", "diameter", "circumference"]}
    for part, degs in [("radius", [35, 160, 250]), ("diameter", [0, 60, 125]), ("circumference", [0, 0]), ("centre", [0])]:
        for i, d in enumerate(degs):
            q = fig(part_fig(part, d).svg("circle with one part shown in red")) + asks[part][i]
            its.append(mcq(q, part, wrong[part], PART_E[part]))
    its.append(mcq("The distance all the way round a circle is called the …", "circumference",
                   ["diameter", "radius", "centre"], PART_E["circumference"]))
    its.append(mcq("A straight line from the centre of a circle to the circumference is called a …", "radius",
                   ["diameter", "circumference", "centre"], "A radius goes from the centre to the edge (the circumference). It is half of a diameter."))
    its.append(mcq("A straight line from one side of a circle to the other that passes through the centre is called a …",
                   "diameter", ["radius", "circumference", "centre"], PART_E["diameter"]))
    its.append(mcq("Which point is the same distance from every point on the circumference of a circle?", "the centre",
                   ["the end of a diameter", "the middle of a radius", "any point inside it"],
                   "Only the centre is the same distance from every point on the circumference. That distance is the radius."))
    abc = fig(abc_fig())
    its.append(mcq(abc + "O is the centre of the circle. Which line is a diameter?", "AB", ["AC", "OC", "BC"],
                   "AB goes from one side of the circle to the other and passes through the centre O. AC and BC do not pass through O, and OC is a radius."))
    its.append(mcq(abc + "O is the centre of the circle. Which line is a radius?", "OC", ["AB", "AC", "BC"],
                   "OC goes from the centre O to the circumference, so it is a radius. AB is a diameter, and AC and BC do not start at the centre."))
    its.append(mcq("Which sentence about a circle is true?", "The diameter is twice the radius.",
                   ["The radius is twice the diameter.", "The radius and the diameter are equal.", "The diameter is half the radius."],
                   "A diameter is made of two radii in a straight line through the centre, so diameter = 2 × radius."))
    its.append(mcq("What is the longest straight line that can be drawn inside a circle, from edge to edge?", "a diameter",
                   ["a radius", "the circumference", "a line close to the edge"],
                   "The longest line across a circle passes through the centre: that is a diameter. A radius is only half as long."))
    its.append(mcq("Ruby draws 5 different radii in the same circle. What is true about them?", "They are all the same length.",
                   ["The longest one is a diameter.", "They are all different lengths.", "They make the circumference."],
                   "Every radius goes from the centre to the circumference, and every point on the circumference is the same distance from the centre."))
    # A-D pictures
    for kind, others, why in [
            ("diameter", ["radius", "chord", "half"],
             "shows a diameter: it goes from edge to edge through the centre. The others are a radius, a line that misses the centre, and a line that stops before the edge."),
            ("radius", ["diameter", "short", "outside"],
             "shows a radius: it goes from the centre exactly to the circumference. The others are a diameter, a line that stops before the edge, and a line that goes past the edge.")]:
        p = pos.next()
        cells = [lines_fig(k) for k in others]
        cells.insert(p, lines_fig(kind))
        q = fig(grid_svg(cells, "four circles labelled A to D")) + "Which picture shows a %s in red?" % kind
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[p], "Picture %s %s" % ("ABCD"[p], why)))
    assert len(its) == 20, len(its)
    return {"title": "Parts of a circle: centre, radius, diameter and circumference", "items": its}


# ------------------------------------------------------------ set 2: radius and diameter
def set_radius(rnd):
    its = []
    for r, u in [(4, "cm"), (7, "cm"), (2.5, "cm"), (12, "mm"), (15, "m")]:
        q = fig(radius_fig("%s %s" % (num(r), u))) + "The radius of this circle is %s %s. What is the diameter?" % (num(r), u)
        its.append(mcq(q, "%s %s" % (num(2 * r), u), ["%s %s" % (num(x), u) for x in (r / 2, r + 2, r, 4 * r)],
                       "The diameter is twice the radius: 2 × %s = %s %s." % (num(r), num(2 * r), u)))
    for d, u in [(10, "cm"), (18, "cm"), (9, "cm"), (26, "mm"), (3, "m")]:
        q = fig(radius_fig("%s %s" % (num(d), u), "diameter")) + "The diameter of this circle is %s %s. What is the radius?" % (num(d), u)
        its.append(mcq(q, "%s %s" % (num(d / 2), u), ["%s %s" % (num(x), u) for x in (2 * d, d - 2, d, d / 4)],
                       "The radius is half the diameter: %s ÷ 2 = %s %s." % (num(d), num(d / 2), u)))
    its.append(mcq("A circle has a radius of 3 cm. What is its diameter in millimetres?", "60 mm",
                   ["6 mm", "30 mm", "15 mm"],
                   "Diameter = 2 × 3 = 6 cm. 1 cm = 10 mm, so 6 cm = 60 mm."))
    its.append(mcq("A circle has a diameter of 9 cm. What is its radius in millimetres?", "45 mm",
                   ["90 mm", "4.5 mm", "18 mm"],
                   "9 cm = 90 mm. The radius is half the diameter: 90 ÷ 2 = 45 mm."))
    its.append(mcq(fig(square_circle_fig("10 cm")) + "The circle fits exactly inside a square with sides of 10 cm. What is the radius of the circle?",
                   "5 cm", ["10 cm", "20 cm", "2.5 cm"],
                   "The circle touches all 4 sides, so its diameter is the same as the side of the square: 10 cm. Radius = 10 ÷ 2 = 5 cm."))
    its.append(mcq(fig(square_circle_fig("? cm")) + "The circle has a radius of 6 cm and fits exactly inside the square. How long is each side of the square?",
                   "12 cm", ["6 cm", "24 cm", "3 cm"],
                   "The side of the square is the same as the diameter of the circle: 2 × 6 = 12 cm."))
    its.append(mcq("A circle with a radius of 3 cm fits exactly inside a square. What is the perimeter of the square?", "24 cm",
                   ["12 cm", "6 cm", "36 cm"],
                   "Each side of the square equals the diameter: 2 × 3 = 6 cm. Perimeter = 4 × 6 = 24 cm."))
    its.append(mcq(fig(row_circles_fig(2, "? cm")) + "Two equal circles fit exactly inside the rectangle. Each circle has a radius of 4 cm. How long is the rectangle?",
                   "16 cm", ["8 cm", "32 cm", "12 cm"],
                   "Each circle is 2 × 4 = 8 cm across. Two diameters: 8 + 8 = 16 cm."))
    its.append(mcq(fig(row_circles_fig(3, "30 cm")) + "Three equal circles fit exactly inside a rectangle 30 cm long. What is the radius of each circle?",
                   "5 cm", ["10 cm", "15 cm", "30 cm"],
                   "The 3 diameters make 30 cm, so one diameter is 30 ÷ 3 = 10 cm. Radius = 10 ÷ 2 = 5 cm."))
    its.append(mcq("A big circle has a radius of 12 cm. A small circle has a diameter that is the same length as the big circle’s radius. "
                   "What is the radius of the small circle?", "6 cm", ["12 cm", "24 cm", "3 cm"],
                   "The small circle’s diameter is 12 cm, so its radius is 12 ÷ 2 = 6 cm."))
    its.append(mcq("Circle A has a radius of 7 cm. Circle B has a diameter of 12 cm. Which circle is wider, and by how much?",
                   "A, by 2 cm", ["B, by 5 cm", "A, by 1 cm", "They are the same"],
                   "Compare diameters: A is 2 × 7 = 14 cm across and B is 12 cm across. 14 − 12 = 2 cm, so A is wider by 2 cm. "
                   "Do not compare a radius with a diameter (7 with 12), and do not stop at the radii (7 − 6 = 1)."))
    its.append(mcq("Which of these is true for every circle?", "diameter = 2 × radius",
                   ["radius = 2 × diameter", "diameter = radius + 2", "diameter = radius ÷ 2"],
                   "Two radii in a straight line through the centre make a diameter, so diameter = 2 × radius and radius = diameter ÷ 2."))
    assert len(its) == 20, len(its)
    return {"title": "Radius and diameter: the diameter is twice the radius", "items": its}


# ------------------------------------------------------------ set 3: 3-D shapes
FACES_DESC = {CUBE: "6 square faces", CUBOID: "6 rectangular faces", TP: "5 faces (2 triangles and 3 rectangles)",
              SP: "5 faces (1 square and 4 triangles)", TET: "4 triangular faces",
              "hexagonal prism": "8 faces (2 hexagons and 6 rectangles)"}


def fev_e(kind):
    F, E, V = COUNTS[kind]
    return ("A %s has %s, %d edges and %d vertices. Faces are the flat surfaces, edges are where two faces meet, "
            "and vertices are the corners." % (kind, FACES_DESC[kind], E, V))


def set_solids(rnd):
    its = []
    name_q = ["What is the name of this 3-D shape?", "Name this 3-D shape.", "What is this 3-D shape called?"]
    for i, (kind, wrong, e) in enumerate([
            (CUBOID, [CUBE, TP, SP], "It has 6 rectangular faces, and they are not all squares, so it is a cuboid."),
            (TP, [SP, TET, CUBOID], "It has 2 triangle faces at the ends joined by 3 rectangles, so it is a triangular prism."),
            (SP, [TP, TET, CUBE], "It has a square base and 4 triangle faces that meet at one vertex, so it is a square-based pyramid."),
            (TET, [SP, TP, "cone"], "It has 4 faces and all of them are triangles, so it is a tetrahedron (a triangular-based pyramid)."),
            ("cylinder", ["circle", "cone", CUBOID], "It has 2 flat circular faces and a curved surface, so it is a cylinder. A circle is a 2-D shape."),
            ("hexagonal prism", ["hexagon", "pentagonal prism", CUBOID],
             "The two end faces are hexagons (6 sides) joined by rectangles, so it is a hexagonal prism. A hexagon is a 2-D shape.")]):
        its.append(mcq(fig(shape_svg(kind)) + name_q[i % 3], kind, wrong, e))
    for kind, what, wrong, pic in [
            (TP, "faces", [6, 9, 3], True), (TP, "edges", [5, 6, 12], True), (TP, "vertices", [5, 9, 3], False),
            (SP, "edges", [5, 4, 12], True), (SP, "vertices", [8, 4, 6], False),
            (CUBOID, "edges", [6, 8, 4], False), (TET, "faces", [6, 3, 5], True), (TET, "edges", [4, 3, 8], False),
            ("hexagonal prism", "faces", [6, 12, 18], True)]:
        ans = dict(zip(("faces", "edges", "vertices"), COUNTS[kind]))[what]
        if pic:
            q = fig(shape_svg(kind)) + "This is a %s. How many %s does it have?" % (kind, what)
        else:
            q = "How many %s does a %s have?" % (what, kind)
        e = fev_e(kind)
        if kind in (TP, SP, TET, "hexagonal prism") and pic:
            e += " Dashed lines show the edges you cannot see."
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq("I am a 3-D shape with 6 faces. All of my faces are squares of the same size. What am I?", CUBE,
                   [CUBOID, SP, TP], "A cube has 6 faces that are all equal squares. A cuboid has rectangular faces."))
    its.append(mcq("I have 5 faces: 1 square and 4 triangles. What am I?", SP, [TP, TET, CUBE],
                   "1 square base and 4 triangles that meet at the top make a square-based pyramid."))
    its.append(mcq("Which 3-D shape has 4 faces, and all of them are triangles?", TET, [SP, TP, "cone"],
                   "A tetrahedron has 4 triangular faces, 6 edges and 4 vertices. A square-based pyramid has a square face as well."))
    its.append(mcq("What shape are the faces of a cuboid?", "rectangles", ["triangles", "circles", "pentagons"],
                   "A cuboid has 6 rectangular faces (some of them can be squares, which are special rectangles)."))
    its.append(mcq("Which of these 3-D shapes has no vertices?", "sphere", [CUBE, SP, TP],
                   "A sphere is round all over: it has no flat faces, no edges and no vertices (corners)."))
    assert len(its) == 20, len(its)
    return {"title": "3-D shapes: faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 4: nets
WRONG_SOLID = {CUBE: [CUBOID, SP, TP], CUBOID: [CUBE, TP, SP], TP: [SP, TET, CUBOID], SP: [TET, TP, CUBE], TET: [SP, TP, CUBE]}
NET_E = {
    CUBE: "There are 6 squares that are all the same size. They fold into a cube.",
    CUBOID: "There are 6 rectangles in 3 matching pairs, and they are not all squares. They fold into a cuboid.",
    TP: "There are 2 triangles (the ends) and 3 rectangles. They fold into a triangular prism.",
    SP: "There is 1 square (the base) and 4 triangles that meet at the top. They fold into a square-based pyramid.",
    TET: "There are 4 triangles and nothing else. They fold into a tetrahedron (a triangular-based pyramid).",
}


def four_nets(nets, k=18):
    return grid_row([cube_net_cv(n, k) for n in nets])


def grid_row(cvs, label="four nets labelled A to D"):
    return row_svg(cvs, list("ABCD"), label, gap=26)


def set_nets(rnd, pos):
    its = []
    ask = ["Which 3-D shape does this net make?", "This net is folded up. What shape does it make?"]
    nets = [(cube_net_cv(CUBE_NETS[0], 34), CUBE), (cube_net_cv(CUBE_NETS[6], 34), CUBE),
            (box_net_cv(4, 2, 3, 22), CUBOID), (box_net_cv(5, 2, 2, 20, 2, 0), CUBOID),
            (tri_prism_cv(26, ("equi", 2), 3), TP), (tri_prism_cv(24, ("right", 3, 4, 5), 2.5, ends=(("top", 1), ("bot", 1))), TP),
            (pyramid_cv(2, 2.2, 26), SP), (tetra_cv(62), TET)]
    for i, (cv, solid) in enumerate(nets):
        its.append(mcq(fig(cv.svg("net of a 3-D shape")) + ask[i % 2], solid, WRONG_SOLID[solid], NET_E[solid]))
    good = CUBE_NETS[:]
    rnd.shuffle(good)
    # which is NOT a net of a cube
    for j, bad in enumerate([0, 3, 2]):
        p = pos.next()
        cells = good[3 * j:3 * j + 3]
        cells.insert(p, BAD_NETS[bad][0])
        for x, c in enumerate(cells):
            assert (fold_cube(c) is None) == (x == p)
        q = fig(four_nets(cells)) + "Which of these is NOT a net of a cube?"
        e = "%s is not a net of a cube: %s. The other three each fold into a cube." % ("ABCD"[p], BAD_NETS[bad][1])
        its.append(mcq_fixed(q, list("ABCD"), "ABCD"[p], e))
    for others, ok in [([1, 4, 3], good[9]), ([4, 0, 2], good[7])]:
        p = pos.next()
        cells = [BAD_NETS[i][0] for i in others]
        cells.insert(p, ok)
        for x, c in enumerate(cells):
            assert (fold_cube(c) is not None) == (x == p)
        q = fig(four_nets(cells)) + "Which of these IS a net of a cube?"
        e = ("%s folds into a cube with no gaps or overlaps. In the others, two squares fold onto the same face "
             "(two squares on the same side of a row of 4, 5 squares in a row, or a 2-by-2 block)." % "ABCD"[p])
        its.append(mcq_fixed(q, list("ABCD"), "ABCD"[p], e))
    # which net makes a square-based pyramid / triangular prism
    p = pos.next()
    cells = [tri_prism_cv(16, ("equi", 2), 2.6), tetra_cv(40), pyramid_cv(2, 2.2, 15, sides=(0, 1, 3))]
    cells.insert(p, pyramid_cv(2, 2.2, 15))
    its.append(mcq_fixed(fig(grid_row(cells)) + "Which net folds into a square-based pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has 1 square and 4 triangles, one on each side of the square. The net with only 3 triangles leaves one side open; "
                         "the others make a triangular prism and a tetrahedron." % "ABCD"[p]))
    p = pos.next()
    cells = [tri_prism_cv(16, ("equi", 2), 2.6, rects=2, ends=(("top", 0), ("bot", 0))),
             tri_prism_cv(16, ("equi", 2), 2.6, ends=(("top", 0), ("top", 1))),
             pyramid_cv(2, 2.2, 15)]
    cells.insert(p, tri_prism_cv(16, ("equi", 2), 2.6))
    its.append(mcq_fixed(fig(grid_row(cells)) + "Which net folds into a triangular prism?", list("ABCD"), "ABCD"[p],
                         "%s has 3 rectangles and 2 triangles, one triangle at each end. One wrong net has only 2 rectangles, "
                         "one has both triangles at the same end, and one is a square-based pyramid." % "ABCD"[p]))
    # opposite faces
    used = set()
    for idx in [0, 6, 8]:
        cells = CUBE_NETS[idx]
        letters = list("ABCDEF")
        rnd.shuffle(letters)
        lab = dict(zip(cells, letters))
        a = rnd.choice(cells)
        used.add((idx, a))
        b = opposite(cells, a)
        touch = [c for c in cells if abs(c[0] - a[0]) + abs(c[1] - a[1]) == 1]
        far = [c for c in cells if c not in touch and c not in (a, b)]
        wrong = ["face " + lab[c] for c in far + touch]
        if (a[0] == b[0] or a[1] == b[1]) and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 2:
            e = ("Faces %s and %s are in a straight line with one square between them, so they fold onto opposite sides of the cube."
                 % (lab[a], lab[b]))
        else:
            e = ("Fold the net: face %s lands opposite face %s. A face that touches %s in the net (%s) is next to it "
                 "on the cube, never opposite." % (lab[b], lab[a], lab[a], ", ".join(sorted(lab[c] for c in touch))))
        q = (fig(cube_net_cv(cells, 40, lab).svg("net of a cube with faces A to F")) +
             "This net is folded into a cube. Which face is opposite face %s?" % lab[a])
        its.append(mcq(q, "face " + lab[b], wrong, e))
    its.append(mcq("How many faces does a net of a square-based pyramid have?", 5, [4, 8, 6],
                   "1 square base and 4 triangles: 1 + 4 = 5 faces."))
    its.append(mcq("Oliver folds a net of 6 rectangles into a cuboid. How many edges does the cuboid have?", 12, [6, 8, 24],
                   "A cuboid has 12 edges (and 6 faces and 8 vertices). 6 is the number of faces."))
    assert len(its) == 20, len(its)
    return {"title": "Nets of 3-D shapes", "items": its}


# ------------------------------------------------------------ set 5: classify and solve problems
def dice_q(rnd):
    cells = CUBE_NETS[3]
    face = fold_cube(cells)
    # numbers 1-6 with opposite faces adding to 7
    pairs = {}
    nums = {}
    k = 1
    for c in cells:
        if c in nums:
            continue
        o = opposite(cells, c)
        nums[c], nums[o] = k, 7 - k
        k += 1
    hide = cells[4]
    ans = nums[hide]
    o = opposite(cells, hide)
    assert nums[o] + ans == 7
    near = [c for c in cells if c not in (hide, o) and abs(c[0] - hide[0]) + abs(c[1] - hide[1]) == 1]
    rest = [c for c in cells if c not in (hide, o) and c not in near]
    show = [o] + (near + rest)[:2]                 # 3 numbers shown; the other 2 faces are blank
    lab = {c: str(nums[c]) for c in show}
    lab[hide] = "?"
    q = (fig(cube_net_cv(cells, 40, lab).svg("net of a dice with some numbers missing")) +
         "This is a net of a dice. The numbers on opposite faces add up to 7. What number goes on the face marked ?")
    wrong = [7 - nums[c] for c in show[1:]] + [nums[o], 7]
    return mcq(q, ans, wrong,
               "When the net is folded, the face marked ? is opposite the %d. So the missing number is 7 − %d = %d." % (nums[o], nums[o], ans))


def set_problems(rnd, P):
    its = []
    its.append(mcq("I am a quadrilateral with 4 equal sides and no right angles. What am I?", "rhombus",
                   ["square", "rectangle", "kite"],
                   "4 equal sides could be a square or a rhombus. A square has 4 right angles, so the shape is a rhombus."))
    its.append(mcq("Which quadrilateral has exactly one pair of parallel sides?", "trapezium",
                   ["parallelogram", "rhombus", "kite"],
                   "A trapezium has exactly one pair of parallel sides. A parallelogram and a rhombus have two pairs; a kite has none."))
    its.append(mcq("Which sentence is true?", "Every square is a rectangle.",
                   ["Every rectangle is a square.", "Every rhombus is a square.", "Every kite is a parallelogram."],
                   "A rectangle has 4 right angles and opposite sides equal. A square has both, so every square is a rectangle, but not every rectangle is a square."))
    its.append(mcq("A triangle has sides of 5 cm, 5 cm and 8 cm. What type of triangle is it?", "isosceles",
                   ["equilateral", "scalene", "right-angled"],
                   "Exactly 2 sides are equal (5 cm and 5 cm), so it is isosceles."))
    its.append(mcq("A regular polygon has 6 equal sides and 6 equal angles. What is it called?", "regular hexagon",
                   ["regular pentagon", "regular octagon", "hexagonal prism"],
                   "A polygon with 6 sides is a hexagon. All sides and angles are equal, so it is a regular hexagon. A hexagonal prism is a 3-D shape."))
    its.append(mcq("A class sorts 3-D shapes into prisms and pyramids. Which shape goes with the pyramids?", TET,
                   [CUBOID, TP, CUBE],
                   "A pyramid has a base and triangle faces that meet at one vertex. A tetrahedron is a triangular-based pyramid. "
                   "Cubes, cuboids and triangular prisms are prisms."))
    n, he, his = P.next()
    its.append(mcq("The wheel on %s’s bike has a diameter of 60 cm. A spoke goes from the centre of the wheel to the rim. How long is a spoke?" % n,
                   "30 cm", ["60 cm", "120 cm", "15 cm"],
                   "A spoke goes from the centre to the edge, so it is a radius: 60 ÷ 2 = 30 cm."))
    its.append(mcq("A pizza has a diameter of 30 cm. It is cut into 8 equal slices with every cut passing through the centre. "
                   "How long is each straight edge of a slice?", "15 cm", ["30 cm", "60 cm", "8 cm"],
                   "Each straight edge goes from the centre to the crust, so it is a radius: 30 ÷ 2 = 15 cm. The number of slices does not change it."))
    its.append(mcq("Four tins of beans stand in a row in a box, touching each other and the ends of the box. Each tin has a radius of 5 cm. "
                   "How long is the box?", "40 cm", ["20 cm", "10 cm", "80 cm"],
                   "Each tin is 2 × 5 = 10 cm across. 4 tins: 4 × 10 = 40 cm. 20 cm uses the radius instead of the diameter."))
    its.append(mcq("A round pond has a diameter of 8 m. A fountain stands at the centre. How far is the fountain from the edge of the pond?",
                   "4 m", ["8 m", "16 m", "2 m"],
                   "From the centre to the edge is a radius: 8 ÷ 2 = 4 m."))
    n, he, his = P.next()
    its.append(mcq("%s lines up 6 round counters in a straight row, each one touching the next. Each counter has a radius of 1.5 cm. "
                   "How long is the row?" % n, "18 cm", ["9 cm", "15 cm", "36 cm"],
                   "Each counter is 2 × 1.5 = 3 cm across. 6 counters: 6 × 3 = 18 cm. 9 cm uses the radius, and 15 cm counts only 5 counters."))
    n, he, his = P.next()
    its.append(mcq("%s glues 2 cubes together, face to face, to make a cuboid. How many faces does the cuboid have?" % n, 6,
                   [12, 10, 11],
                   "The new shape is a cuboid, and every cuboid has 6 faces. The two faces that are glued together are hidden inside."))
    n, he, his = P.next()
    its.append(mcq("%s makes a model of a square-based pyramid. %s uses straws for the edges and balls of modelling clay for the vertices. "
                   "What does %s need?" % (n, he.capitalize(), he), "8 straws, 5 balls",
                   ["5 straws, 8 balls", "8 straws, 4 balls", "5 straws, 5 balls"],
                   "A square-based pyramid has 8 edges (4 round the base and 4 up to the top) and 5 vertices (4 at the base and 1 at the top)."))
    its.append(mcq("A cube model is made from straws, one straw for each edge. Each straw is 10 cm long. "
                   "What is the total length of the straws?", "120 cm", ["60 cm", "80 cm", "100 cm"],
                   "A cube has 12 edges: 12 × 10 = 120 cm. 60 cm counts the faces (6) and 80 cm counts the vertices (8)."))
    its.append(mcq("A tent is shaped like a triangular prism, with a groundsheet as the floor. How many faces does the tent have?", 5,
                   [6, 9, 4],
                   "A triangular prism has 5 faces: 2 triangle ends and 3 rectangles (the 2 sloping sides and the floor)."))
    its.append(dice_q(rnd))
    its.append(mcq("The minute hand of a clock goes from the centre of the clock face exactly to its edge. "
                   "The clock face has a diameter of 30 cm. How long is the minute hand?", "15 cm", ["30 cm", "60 cm", "10 cm"],
                   "From the centre to the edge is a radius: 30 ÷ 2 = 15 cm."))
    n, he, his = P.next()
    its.append(mcq("%s uses a pair of compasses to draw a circle with a diameter of 9 cm. How wide should %s open the compasses?"
                   % (n, he), "4.5 cm", ["9 cm", "18 cm", "3 cm"],
                   "Compasses are opened to the radius: 9 ÷ 2 = 4.5 cm."))
    its.append(mcq("A target is a small circle with a radius of 4 cm and 2 rings around it. Each ring is 4 cm wide. "
                   "What is the diameter of the whole target?", "24 cm", ["12 cm", "16 cm", "48 cm"],
                   "The radius of the whole target is 4 + 4 + 4 = 12 cm, so the diameter is 2 × 12 = 24 cm. "
                   "16 cm forgets that the rings are on both sides of the centre."))
    n, he, his = P.next()
    its.append(mcq("%s paints each face of a cuboid box a different colour. How many colours does %s use?" % (n, he), 6,
                   [12, 8, 4],
                   "A cuboid has 6 faces, so %s needs 6 colours. 12 is the number of edges and 8 is the number of vertices." % he))
    assert len(its) == 20, len(its)
    return {"title": "Classify shapes and solve problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def parts_lesson_svg():
    r = 100
    cv = Canvas()
    cv.circle((0, 0), r, sw=4, col=RED)
    cv.line((-r, 0), (r, 0), sw=3, col=INK)
    cv.line((0, 0), pol(r, 60), sw=3, col=GREEN)
    cv.dot((0, 0), 5)
    cv.text(-50, 14, "diameter")
    cv.text(26, -30, "radius", anchor="start", col=GREEN)
    cv.text(-8, -14, "centre", anchor="end")
    p = pol(r, 135)
    cv.text(p[0] - 6, p[1] - 12, "circumference", anchor="end", col=RED)
    return cv.svg("parts of a circle: centre, radius, diameter and circumference")


def body_html():
    solids = row_svg([solid_cv(CUBE, 50), solid_cv(CUBOID, 50), solid_cv(TP, 56), solid_cv(SP, 56), solid_cv(TET, 56)],
                     ["cube", "cuboid", "triangular prism", "square-based pyramid", "tetrahedron"],
                     "cube, cuboid, triangular prism, square-based pyramid and tetrahedron", gap=22, fs=14, col=INK)
    nets = row_svg([cube_net_cv(CUBE_NETS[0], 22), tri_prism_cv(18, ("equi", 2), 2.6), pyramid_cv(2, 2.2, 17)],
                   ["cube", "triangular prism", "square-based pyramid"],
                   "nets of a cube, a triangular prism and a square-based pyramid", gap=34, fs=14, col=INK)
    good_bad = row_svg([cube_net_cv(CUBE_NETS[6], 22), cube_net_cv(BAD_NETS[0][0], 22)],
                       ["a net of a cube", "NOT a net of a cube"], "a net of a cube and a pattern that is not a net", gap=40, fs=14, col=INK)
    return (
        "<h2>Parts of a circle</h2>"
        "<p>Every point on the edge of a circle is the same distance from the <b>centre</b>.</p>"
        "<ul><li>The <b>radius</b> is a straight line from the centre to the edge.</li>"
        "<li>The <b>diameter</b> is a straight line from edge to edge that passes through the centre.</li>"
        "<li>The <b>circumference</b> is the distance all the way round the circle (its perimeter).</li></ul>"
        "<figure class='sn-fig'>" + parts_lesson_svg() +
        "<figcaption>The diameter is made of two radii in a straight line, so it is twice as long as the radius.</figcaption></figure>"
        "<h2>Diameter = 2 × radius</h2>"
        "<p>To find the diameter, <b>double</b> the radius. To find the radius, <b>halve</b> the diameter.</p>" +
        ex("Example 1", "A circle has a radius of 6.5 cm. What is its diameter?", "Double the radius: 2 × 6.5 = 13.", "13 cm") +
        ex("Example 2", "A circle fits exactly inside a square with sides of 14 cm. What is the radius of the circle?",
           "The circle touches all 4 sides, so its diameter is 14 cm. Halve it: 14 ÷ 2 = 7.", "7 cm") +
        "<h2>3-D shapes: faces, edges and vertices</h2>"
        "<p>A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. A <b>vertex</b> is a corner (two or more are <b>vertices</b>). "
        "Dashed lines show edges at the back that you cannot see.</p>"
        "<figure class='sn-fig'>" + solids + "</figure>" +
        table(["Shape", "Faces", "Edges", "Vertices"], [
            ["Cube", "6 (all squares)", "12", "8"],
            ["Cuboid", "6 (rectangles)", "12", "8"],
            ["Triangular prism", "5 (2 triangles, 3 rectangles)", "9", "6"],
            ["Square-based pyramid", "5 (1 square, 4 triangles)", "8", "5"],
            ["Tetrahedron", "4 (all triangles)", "6", "4"],
        ]) +
        "<h2>Nets</h2>"
        "<p>A <b>net</b> is a flat shape that folds up to make a 3-D shape. Each part of the net becomes one face.</p>"
        "<figure class='sn-fig'>" + nets + "</figure>"
        "<p>A cube has 11 different nets. A pattern of 6 squares is <b>not</b> a net if two squares would fold onto the same face.</p>"
        "<figure class='sn-fig'>" + good_bad +
        "<figcaption>On the right, the two top squares are on the same side of the row of 4. They fold onto the same face, so one face is left open.</figcaption></figure>" +
        ex("Example 3", "A net has 2 triangles and 3 rectangles. What 3-D shape does it make?",
           "The 2 triangles are the ends and the 3 rectangles join them.", "a triangular prism") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Halving the radius to get the diameter", "Diameter = 2 × radius; radius = diameter ÷ 2"],
            ["Calling the circumference the diameter", "The circumference goes all the way round; the diameter goes straight across"],
            ["Calling any line across a circle a diameter", "A diameter must pass through the centre"],
            ["Counting edges when asked for faces", "Faces are flat surfaces; edges are the lines where they meet"],
            ["Forgetting the top vertex of a pyramid", "Count the base corners and the vertex at the top"],
            ["Two squares on the same side of a row of 4 in a cube net", "Put one square on each side of the row"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 pupils learn about circles?",
     "a": "They name the parts of a circle (centre, radius, diameter and circumference) and know that the diameter is twice the radius, so they can find one from the other."},
    {"q": "Do Year 6 children need to calculate the circumference?",
     "a": "No. In Year 6 they only name the circumference. Working out the circumference and area of a circle with π is taught in Key Stage 3."},
    {"q": "How many nets does a cube have?",
     "a": "A cube has 11 different nets. Each one has 6 squares, and no two squares fold onto the same face."},
    {"q": "Are circles and nets in the Year 6 SATs?",
     "a": "They can be. Questions on the properties of shapes, such as radius and diameter or nets of 3-D shapes, can appear in the reasoning papers (Papers 2 and 3)."},
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
    """Tag pictures that must print larger (A-D choices) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(6617)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_parts(rnd, pos), set_radius(rnd), set_solids(rnd), set_nets(rnd, pos), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "circles-and-nets", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Circles and Nets: Radius, Diameter, 3-D Shapes and Nets",
        "seo_title": "Year 6 Circles and Nets Worksheets: Radius, Diameter, Faces, Edges, Vertices and Nets of 3-D Shapes (Free, with Answers)",
        "short_title": "Circles and nets",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 6: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Illustrate and name parts of circles, including radius, diameter and circumference and know that the diameter is twice the radius; recognise, describe and build simple 3-D shapes, including making nets; compare and classify geometric shapes based on their properties and sizes.",
        "meta_desc": "Free Year 6 maths worksheets on circles and nets: name the centre, radius, diameter and circumference, use diameter = 2 × radius, count faces, edges and vertices of 3-D shapes, and spot the nets of cubes, prisms and pyramids. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "The diameter is twice the radius: diameter = 2 × radius, and radius = diameter ÷ 2.",
        "key_sub": "A radius goes from the centre to the edge, a diameter goes across through the centre, and the circumference is the distance all the way round. A net is a flat shape that folds into a 3-D shape: each part becomes one face.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four [a-z]+ labelled A to D)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
