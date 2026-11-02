# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Surface Area Using Nets (6.G.A.4)
  python tools/gen_us_math_g6_surface_area.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above are written with commas; units are cm², in², ft², m².

Pictures (checked in code):
  cube nets      squares on a grid; fold_cube() rolls a cube over the net, so a net is valid only when
                 the 6 squares land on 6 different faces (this also gives the opposite faces)
  prism nets     a strip of 4 faces with the two bases attached above and below a face of length l
  triangle nets  right triangles are a-b-c triples (3-4-5 ...); isosceles triangles are two right
                 triangles, so every edge is a whole number; each triangle edge is glued to a
                 rectangle edge of the same length (asserted)
  labels         never touch each other, and a label is either fully inside one face or outside all
                 faces, and no line crosses it (asserted)
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE = "#cfe6d6", "#f6dcb4", "#a9d3b6"
TOP3 = "#e6f2e9"
PAIR = ["#cfe6d6", "#f6dcb4", "#d9e4f5"]          # matching faces of a box (lesson only)
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
UNITS = ["cm", "in", "ft", "m"]
HALF = "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"
DZX, DZY = 0.55, 0.40

CUBE, RP, TP, SP, TPY = "cube", "rectangular prism", "triangular prism", "square pyramid", "triangular pyramid"


# ------------------------------------------------------------ helpers
def f(n):
    """2400 -> 2,400."""
    return "{:,}".format(n)


def sq(n, u):
    return "%s %s²" % (f(n), u)


def cb(n, u):
    return "%s %s³" % (f(n), u)


def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors (no zero or negative amounts). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$").replace(",", "")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set.
    Items with '_fix' keep their choices in order (Net 1 ... Net 4) and redraw the picture instead."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_fix" in it:
                it["c"] = ["Net 1", "Net 2", "Net 3", "Net 4"]
                it["q"], it["e"] = it.pop("_fix")(t)
                it["a"] = t
                continue
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


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

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

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

    def fits(self, box, poly):
        """True when the text box is fully inside poly (2 px margin)."""
        x0, y0, x1, y1 = box
        return all(inside(p, poly) for p in [(x0 - 2, y0 - 2), (x1 + 2, y0 - 2), (x0 - 2, y1 + 2), (x1 + 2, y1 + 2)])

    def check(self):
        """Each label is inside one face or outside all faces, and no line runs through it."""
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert hit == [] or hit == [len(pts)], ("label crosses a face edge", (x0, y0, x1, y1), hit)
            for a, b in self.segs:
                for i in range(41):
                    x, y = a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40
                    assert not (x0 - 1 < x < x1 + 1 and y0 - 1 < y < y1 + 1), ("line through a label", (x0, y0))

    def svg(self, label, pad=5, check=True):
        if check:
            self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def dim_line(cv, x0, x1, y, t, above=True):
    """|<-- t -->| measuring from x0 to x1, drawn at height y, label above (or below)."""
    a, b = x0 + 5, x1 - 5
    cv.line((a, y), (b, y), sw=1.4, col=INK)
    cv.line((a, y - 5), (a, y + 5), sw=1.4, col=INK)
    cv.line((b, y - 5), (b, y + 5), sw=1.4, col=INK)
    cv.text((a + b) / 2, y - 15 if above else y + 15, t)


def dim_v(cv, x, y0, y1, t):
    """Vertical |<-- t -->| from y0 to y1 at x, label to the left."""
    a, b = min(y0, y1) + 2, max(y0, y1) - 2
    cv.line((x, a), (x, b), sw=1.4, col=INK)
    cv.line((x - 5, a), (x + 5, a), sw=1.4, col=INK)
    cv.line((x - 5, b), (x + 5, b), sw=1.4, col=INK)
    cv.text(x - 8, (a + b) / 2, t, anchor="end")


def height_label(cv, tri, base_mid, apex, t):
    """Dashed height from base_mid to apex, with its label beside the line inside the triangle."""
    cv.line(base_mid, apex, dashed=True, sw=1.6, col=INK)
    fs = 16
    w = tw(t, fs)
    (bx, by), (ax, ay) = base_mid, apex
    for i in range(1, 30):
        r = i / 30
        x, y = bx + (ax - bx) * r, by + (ay - by) * r
        if abs(ax - bx) < 1e-6:                        # vertical height: label to the right of it
            for anchor, x0 in (("start", x + 5), ("end", x - 5 - w)):
                box = (x0, y - fs / 2, x0 + w, y + fs / 2)
                if cv.fits(box, tri):
                    cv.text(x + 5 if anchor == "start" else x - 5, y, t, fs, anchor)
                    return
        else:                                          # horizontal height: label above it
            box = (x - w / 2, y - 6 - fs, x + w / 2, y - 6)
            if cv.fits(box, tri):
                cv.text(x, y - 6 - fs / 2, t, fs)
                return
    raise AssertionError("height label does not fit: " + t)


# ------------------------------------------------------------ cube nets
def rot_y(s):
    return ((0, 0, s), (0, 1, 0), (-s, 0, 0))


def rot_x(s):
    return ((1, 0, 0), (0, 0, -s), (0, s, 0))


def mat(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def fold_cube(cells):
    """Roll a cube over the squares. Returns {cell: face} (face = which side of the cube lies on that square)
    or None when two squares land on the same face (not a net)."""
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
    face = {}
    for c, m in R.items():
        face[c] = tuple(m[2][i] * -1 for i in range(3))     # R^T (0,0,-1): the cube's side that is down
    return face if len(set(face.values())) == 6 else None


def opposite(cells, a):
    face = fold_cube(cells)
    fa = face[a]
    return [c for c in cells if face[c] == tuple(-v for v in fa)][0]


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
BAD_NETS = [
    ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 0)], "the two end squares fold onto the same face, so they overlap and one face is left open"),
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], "it has a 2-by-2 block of squares, but only 3 faces of a cube meet at a corner, so two squares overlap"),
    ([(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 0)], "5 squares in a row wrap all the way around, so the first and last squares overlap"),
    ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (1, 0)], "it has a 2-by-2 block of squares, but only 3 faces of a cube meet at a corner, so two squares overlap"),
]
for _n in CUBE_NETS:
    assert fold_cube(_n), _n
for _n, _w in BAD_NETS:
    assert fold_cube(_n) is None, _n


def draw_cells(cv, cells, k, ox=0, oy=0, letters=None, fill=FILL):
    c0 = min(c for c, r in cells)
    r0 = min(r for c, r in cells)
    for c, r in cells:
        x, y = ox + (c - c0) * k, oy + (r - r0) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], fill)
    if letters:
        for (c, r), t in letters.items():
            cv.text(ox + (c - c0 + 0.5) * k, oy + (r - r0 + 0.5) * k, t, 18, col=GREEN)
    return (max(c for c, r in cells) - c0 + 1) * k, (max(r for c, r in cells) - r0 + 1) * k


def cube_net_svg(cells, label="net of a cube", k=40, letters=None, side=None):
    cv = Canvas()
    draw_cells(cv, cells, k, letters=letters)
    if side:
        c0, r0 = min(c for c, r in cells), min(r for c, r in cells)
        top = min((c, r) for c, r in cells if r == r0)
        cv.text((top[0] - c0 + 0.5) * k, -12, side)
    return cv.svg(label)


def four_nets_svg(nets, label):
    k, gap = 20, 26
    cv = Canvas()
    x = 0
    for i, cells in enumerate(nets):
        w, h = draw_cells(cv, cells, k, ox=x)
        cv.text(x + w / 2, 3 * k + 16, str(i + 1), 17, col=GREEN)
        x += w + gap
    return cv.svg(label)


# ------------------------------------------------------------ prism and pyramid nets
def box_net(cv, L, W, H, k, top_on=0, bot_on=0, cols=None):
    """Strip of 4 faces (l, w, l, w wide, h tall) with an l × w face above face top_on and below face bot_on."""
    assert top_on in (0, 2) and bot_on in (0, 2)
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cols = cols or [FILL] * 6
    faces = []
    for i in range(4):
        faces.append([(xs[i], 0), (xs[i + 1], 0), (xs[i + 1], H), (xs[i], H)])
    faces.append([(xs[top_on], -W), (xs[top_on] + L, -W), (xs[top_on] + L, 0), (xs[top_on], 0)])
    faces.append([(xs[bot_on], H), (xs[bot_on] + L, H), (xs[bot_on] + L, H + W), (xs[bot_on], H + W)])
    for pts, col in zip(faces, cols):
        cv.poly([(x * k, y * k) for x, y in pts], col)
    return xs


def box_scale(L, W, H, mw=300, mh=185):
    k = min(mw / (2 * L + 2 * W), mh / (H + 2 * W), 30)
    assert min(L, W, H) * k >= 22, (L, W, H, k)
    return k


def box_net_svg(L, W, H, u=None, top_on=0, bot_on=0, letters=None, label=None, cols=None):
    k = box_scale(L, W, H)
    cv = Canvas()
    xs = box_net(cv, L, W, H, k, top_on, bot_on, cols)
    if u:
        xt = xs[top_on]
        cv.text((xt + L / 2) * k, -W * k - 12, "%d %s" % (L, u))
        cv.text((xt + L) * k + 7, -W / 2 * k, "%d %s" % (W, u), anchor="start")
        cv.text(xs[4] * k + 7, H / 2 * k, "%d %s" % (H, u), anchor="start")
    if letters:
        centers = [((xs[i] + xs[i + 1]) / 2, H / 2) for i in range(4)]
        centers += [(xs[top_on] + L / 2, -W / 2), (xs[bot_on] + L / 2, H + W / 2)]
        for (x, y), t in zip(centers, letters):
            cv.text(x * k, y * k, t, 18, col=GREEN)
    return cv.svg(label or "net of a rectangular prism")


def tri_prism_net_svg(tri, L, u=None, label="net of a triangular prism"):
    """tri = ('right', a, b, c) with legs a, b and long side c, or ('iso', b, h, s) with base b, height h, sides s.
    The 3 rectangles are side by side (L tall); the triangles sit on the middle rectangle."""
    kind = tri[0]
    if kind == "right":
        _, a, b, c = tri
        assert a * a + b * b == c * c
        widths = [a, b, c]
        top = [(a, 0), (a + b, 0), (a, -a)]                 # right angle at (a, 0): leg a up, leg b along the base
        tall = a
    else:
        _, b, h, s = tri
        assert (2 * h) ** 2 + b * b == (2 * s) ** 2
        widths = [s, b, s]
        top = [(s, 0), (s + b, 0), (s + b / 2, -h)]
        tall = h
    W = sum(widths)
    bot = [(x, L - y) for x, y in top]
    # every triangle edge matches the rectangle edge it folds onto
    d = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
    assert abs(d(top[0], top[1]) - widths[1]) < 1e-9
    assert abs(d(top[0], top[2]) - widths[0]) < 1e-9 and abs(d(top[1], top[2]) - widths[2]) < 1e-9
    k = min(310 / W, 210 / (L + 2 * tall), 30)
    assert min(widths + [L, tall]) * k >= 22, (tri, L, k)
    cv = Canvas()
    x = 0
    for w in widths:
        cv.poly([(x * k, 0), ((x + w) * k, 0), ((x + w) * k, L * k), (x * k, L * k)], FILL)
        x += w
    tk = [(x * k, y * k) for x, y in top]
    cv.poly(tk, BASE)
    cv.poly([(x * k, y * k) for x, y in bot], BASE)
    if u:
        x0 = widths[0]
        cv.text(widths[0] / 2 * k, L * k + 14, "%d %s" % (widths[0], u))
        cv.text((x0 + widths[1] + widths[2] / 2) * k, L * k + 14, "%d %s" % (widths[2], u))
        dim_line(cv, x0 * k, (x0 + widths[1]) * k, L / 2 * k + 10, "%d %s" % (widths[1], u))
        cv.text(W * k + 7, L / 2 * k, "%d %s" % (L, u), anchor="start")
        if kind == "iso":
            cv.line(((x0 + widths[1] / 2) * k, 0), tk[2], dashed=True, sw=1.6, col=INK)
            dim_v(cv, x0 * k - 8, 0, tk[2][1], "%d %s" % (tall, u))
    return cv.svg(label)


def pyramid_net_svg(s, l, u=None, label="net of a square pyramid"):
    """Square base s × s with a triangle (base s, height l) on each side."""
    assert 2 * l > s
    k = min(260 / (s + 2 * l), 34)
    cv = Canvas()
    S, Lk = s * k, l * k
    cv.poly([(0, 0), (S, 0), (S, S), (0, S)], BASE)
    tris = [[(0, 0), (S, 0), (S / 2, -Lk)], [(0, S), (S, S), (S / 2, S + Lk)],
            [(0, 0), (0, S), (-Lk, S / 2)], [(S, 0), (S, S), (S + Lk, S / 2)]]
    for t in tris:
        cv.poly(t, FILL)
    if u:
        assert S >= 60
        dim_line(cv, 0, S, S / 2 + 10, "%d %s" % (s, u))
        cv.line((S, S / 2), (S + Lk, S / 2), dashed=True, sw=1.6, col=INK)
        dim_line(cv, S, S + Lk, S + 12, "%d %s" % (l, u), above=False)
    return cv.svg(label)


def tri_pyramid_net_svg(label="net of a triangular pyramid"):
    k = 80
    H = math.sqrt(3)
    P = lambda x, y: (x * k, y * k)
    p0, p1, p2 = P(0, H), P(2, H), P(1, 0)
    m01, m12, m02 = P(1, H), P(1.5, H / 2), P(0.5, H / 2)
    cv = Canvas()
    for t in [[p0, m01, m02], [m01, p1, m12], [m02, m12, p2]]:
        cv.poly(t, FILL)
    cv.poly([m02, m01, m12], BASE)
    return cv.svg(label)


# ------------------------------------------------------------ 3D box (oblique view)
def proj(X, Y, Z, k):
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def prism_svg(L, W, H, u, label):
    k = min(165 / (L + W * DZX), 100 / (H + W * DZY), 26)
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(L, 0, 0), p(L, H, 0), p(0, H, 0)], FILL, 2.4)
    cv.poly([p(0, H, 0), p(L, H, 0), p(L, H, W), p(0, H, W)], TOP3, 2.4)
    cv.poly([p(L, 0, 0), p(L, 0, W), p(L, H, W), p(L, H, 0)], SIDE, 2.4)
    for a, b in [((0, 0, W), (L, 0, W)), ((0, 0, W), (0, H, W)), ((0, 0, W), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True, sw=1.6)
    x, y = p(L / 2, 0, 0)
    cv.text(x, y + 17, "%d %s" % (L, u))
    x, y = p(0, H / 2, 0)
    cv.text(x - 8, y, "%d %s" % (H, u), anchor="end")
    x, y = p(L, 0, W / 2)
    cv.text(x + 7, y + 11, "%d %s" % (W, u), anchor="start")
    return cv.svg(label, check=False)


# ------------------------------------------------------------ surface area formulas
def sa_box(L, W, H):
    return 2 * (L * W + L * H + W * H)


def box_e(L, W, H, u):
    a, b, c = L * W, L * H, W * H
    return ("Top and bottom: 2 × (%d × %d) = %d. Front and back: 2 × (%d × %d) = %d. Two sides: 2 × (%d × %d) = %d. "
            "Add: %d + %d + %d = %s %s²." % (L, W, 2 * a, L, H, 2 * b, W, H, 2 * c, 2 * a, 2 * b, 2 * c, f(sa_box(L, W, H)), u))


def sa_pyr(s, l):
    return s * s + 2 * s * l


def pyr_e(s, l, u):
    t = s * l // 2 if s * l % 2 == 0 else None
    tri = f(t) if t else "%g" % (s * l / 2)
    return ("Base: %d × %d = %d. One triangle: %s × %d × %d = %s. Four triangles: 4 × %s = %s. "
            "Total: %d + %s = %s %s²." % (s, s, s * s, HALF, s, l, tri, tri, f(2 * s * l), s * s, f(2 * s * l), f(sa_pyr(s, l)), u))


def tri_parts(tri):
    if tri[0] == "right":
        _, a, b, c = tri
        return a * b, a + b + c, (a, b)                    # area of 2 triangles, perimeter, base × height
    _, b, h, s = tri
    return b * h, 2 * s + b, (b, h)


def sa_tri(tri, L):
    two, per, _ = tri_parts(tri)
    return two + per * L


def tri_e(tri, L, u):
    two, per, (bb, hh) = tri_parts(tri)
    sides = (tri[1], tri[2], tri[3]) if tri[0] == "right" else (tri[3], tri[1], tri[3])
    return ("Two triangles: 2 × %s × %d × %d = %d. Three rectangles: (%d + %d + %d) × %d = %d × %d = %s. "
            "Total: %d + %s = %s %s²." % (HALF, bb, hh, two, sides[0], sides[1], sides[2], L, per, L, f(per * L),
                                          two, f(per * L), f(two + per * L), u))


# ------------------------------------------------------------ set 1: name the solid from its net
WRONG_SOLID = {CUBE: [RP, SP, TP], RP: [CUBE, TP, SP], TP: [TPY, SP, RP], SP: [TPY, TP, CUBE], TPY: [SP, TP, CUBE]}
ASK = ["What solid does this net fold into?", "This net is folded up. What solid does it make?",
       "Which solid has this net?"]


def solid_e(solid):
    return {
        CUBE: "There are 6 squares that are all the same size. They fold into a cube.",
        RP: "There are 6 rectangles in 3 matching pairs (not all squares). They fold into a rectangular prism.",
        TP: "There are 2 triangles (the bases) and 3 rectangles. They fold into a triangular prism.",
        SP: "There is 1 square (the base) and 4 triangles that meet at the top. They fold into a square pyramid.",
        TPY: "There are 4 triangles and no rectangles. They fold into a triangular pyramid.",
    }[solid]


def cube_choice(nets, odd, kind, why):
    """4 nets in one picture; the odd one is drawn in the place balance() chooses."""
    def fix(t):
        order = list(nets)
        order.insert(t, odd)
        if kind == "not":
            q = (fig(four_nets_svg(order, "four patterns of 6 squares, numbered 1 to 4")) +
                 "Which pattern is NOT a net of a cube?")
            e = "Net %d is not a net of a cube: %s. The other three each fold into a cube." % (t + 1, why)
        else:
            q = (fig(four_nets_svg(order, "four patterns of 6 squares, numbered 1 to 4")) +
                 "Which pattern is a net of a cube?")
            e = ("Net %d folds into a cube with no overlaps. The others cannot: %s." % (t + 1, why))
        return q, e
    return {"q": "", "c": ["Net 1", "Net 2", "Net 3", "Net 4"], "a": 0, "e": "", "_fix": fix}


def set_identify(rnd):
    its = []
    nets = []
    for i, cells in enumerate([CUBE_NETS[0], CUBE_NETS[6], CUBE_NETS[8]]):
        nets.append((fig(cube_net_svg(cells, k=36)), CUBE))
    for L, W, H, t, b in [(4, 2, 3, 0, 0), (5, 3, 2, 2, 0), (3, 2, 5, 0, 2)]:
        nets.append((fig(box_net_svg(L, W, H, top_on=t, bot_on=b)), RP))
    for tri, L in [(("right", 3, 4, 5), 7), (("iso", 6, 4, 5), 8), (("iso", 8, 3, 5), 5)]:
        nets.append((fig(tri_prism_net_svg(tri, L)), TP))
    for s, l in [(4, 3), (5, 6)]:
        nets.append((fig(pyramid_net_svg(s, l)), SP))
    nets.append((fig(tri_pyramid_net_svg()), TPY))
    for i, (pic, solid) in enumerate(nets):
        its.append(mcq(pic + ASK[i % 3], solid, WRONG_SOLID[solid], solid_e(solid)))
    # which is (not) a cube net
    good = CUBE_NETS[:]
    rnd.shuffle(good)
    its.append(cube_choice(good[0:3], BAD_NETS[0][0], "not", BAD_NETS[0][1]))
    its.append(cube_choice(good[3:6], BAD_NETS[2][0], "not", BAD_NETS[2][1]))
    its.append(cube_choice([BAD_NETS[1][0], BAD_NETS[0][0], BAD_NETS[3][0]], good[6], "is",
                           "they have a 2-by-2 block of squares, or two squares fold onto the same face"))
    its.append(cube_choice([BAD_NETS[2][0], BAD_NETS[3][0], BAD_NETS[1][0]], good[7], "is",
                           "they have 5 squares in a row or a 2-by-2 block of squares"))
    # nets described in words
    its.append(mcq("A net is made of 6 squares that are all the same size. What solid does it fold into?", CUBE,
                   [RP, SP, TP], solid_e(CUBE)))
    its.append(mcq("A net has 1 square and 4 triangles. What solid does it fold into?", SP,
                   [TP, TPY, CUBE], solid_e(SP)))
    its.append(mcq("A net has 2 triangles and 3 rectangles. What solid does it fold into?", TP,
                   [SP, TPY, RP], solid_e(TP)))
    its.append(mcq("A net has 6 rectangles: 3 pairs that match, and they are not all squares. What solid does it fold into?",
                   RP, [CUBE, TP, SP], solid_e(RP)))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Match a net to its solid", "items": its}


# ------------------------------------------------------------ set 2: faces, edges, vertices and matching faces
COUNTS = {CUBE: (6, 12, 8), RP: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5)}


def set_faces(rnd):
    its = []
    for solid, what, extra in [(TP, "faces", [6, 3]), (TP, "edges", [12, 8]), (TP, "vertices", [8, 3]),
                               (SP, "faces", [4, 6]), (SP, "edges", [12, 4]), (SP, "vertices", [4, 6]),
                               (RP, "edges", [8, 4]), (CUBE, "vertices", [4, 24])]:
        F, E, V = COUNTS[solid]
        ans = {"faces": F, "edges": E, "vertices": V}[what]
        others = [x for x in (F, E, V) if x != ans]
        e = ("A %s has %d faces, %d edges and %d vertices. Faces are the flat sides, edges are where 2 faces meet, "
             "and vertices are the corners." % (solid, F, E, V))
        its.append(mcq("How many %s does a %s have?" % (what, solid), ans, others + extra, e))
    its.append(mcq("How many triangles are in a net of a square pyramid?", 4, [5, 1, 2],
                   "A square pyramid has 1 square base and 4 triangle faces, so its net has 4 triangles."))
    its.append(mcq("How many rectangles are in a net of a triangular prism?", 3, [2, 5, 6],
                   "A triangular prism has 2 triangle bases and 3 rectangle faces, one for each side of the triangle."))
    its.append(mcq("A rectangular prism is 3 cm by 5 cm by 8 cm. How many of its faces are 3 cm by 5 cm rectangles?", 2,
                   [1, 4, 6],
                   "Faces come in matching pairs: 2 faces are 3 by 5, 2 are 3 by 8 and 2 are 5 by 8."))
    # opposite faces of a cube
    used = set()
    for idx in [0, 1, 6, 7, 8]:
        cells = CUBE_NETS[idx]
        letters = list("ABCDEF")
        rnd.shuffle(letters)
        lab = dict(zip(cells, letters))
        while True:
            a = rnd.choice(cells)
            if (idx, a) not in used:
                break
        used.add((idx, a))
        b = opposite(cells, a)
        touch = [c for c in cells if abs(c[0] - a[0]) + abs(c[1] - a[1]) == 1]
        far = [c for c in cells if c not in touch and c not in (a, b)]
        wrong = ["Face " + lab[c] for c in far + touch]
        if (a[0] == b[0] or a[1] == b[1]) and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 2:
            e = ("Faces %s and %s are in a straight line with one square between them, so they fold onto opposite sides of the cube."
                 % (lab[a], lab[b]))
        else:
            e = ("Fold the net: face %s lands across from face %s. A face that touches %s in the net (%s) is next to it "
                 "on the cube, never opposite." % (lab[b], lab[a], lab[a], ", ".join(sorted(lab[c] for c in touch))))
        q = (fig(cube_net_svg(cells, "net of a cube with faces A to F", k=40, letters=lab)) +
             "This net is folded into a cube. Which face is opposite face %s?" % lab[a])
        its.append(mcq(q, "Face " + lab[b], wrong, e))
    # matching faces of a box
    for (L, W, H, t, bo), ask in zip([(5, 2, 3, 0, 0), (4, 3, 2, 2, 0), (6, 3, 4, 0, 2), (5, 4, 2, 2, 2)], [0, 4, 1, 5]):
        letters = list("ABCDEF")
        rnd.shuffle(letters)
        opp = {0: 2, 2: 0, 1: 3, 3: 1, 4: 5, 5: 4}
        dims = [(L, H), (W, H), (L, H), (W, H), (L, W), (L, W)]
        b = opp[ask]
        wrong = ["Face " + letters[i] for i in range(6) if i not in (ask, b)]
        rnd.shuffle(wrong)
        x, y = dims[ask]
        e = ("Face %s and face %s are both %d by %d rectangles, so they are opposite faces of the box. "
             "A box has 3 pairs of matching faces." % (letters[ask], letters[b], x, y))
        q = (fig(box_net_svg(L, W, H, top_on=t, bot_on=bo, letters=letters, label="net of a rectangular prism with faces A to F")) +
             "This is a net of a rectangular prism. Which face is the same size and shape as face %s?" % letters[ask])
        its.append(mcq(q, "Face " + letters[b], wrong, e))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Faces, edges, vertices and matching faces", "items": its}


# ------------------------------------------------------------ set 3: cubes and rectangular prisms
def pick_box(rnd, seen):
    while True:
        L, W, H = rnd.randint(4, 12), rnd.randint(2, 7), rnd.randint(2, 9)
        if len({L, W, H}) < 3 or L < W or max(L, W, H) > 3.5 * min(L, W, H) or (L, W, H) in seen:
            continue
        SA, V = sa_box(L, W, H), L * W * H
        if SA in (V, SA // 2) or V == SA // 2:
            continue
        seen.add((L, W, H))
        return L, W, H


def box_wrong(L, W, H, u, r):
    SA, V = sa_box(L, W, H), L * W * H
    pool = [sq(V, u), sq(SA // 2, u), sq(SA - 2 * L * W, u), cb(SA, u)]
    return pool[r:] + pool[:r]


def set_boxes(rnd, P):
    its, seen = [], set()
    for i, s in enumerate([3, 5, 7, 9]):
        u = UNITS[i]
        SA = 6 * s * s
        cells = CUBE_NETS[[0, 6, 1, 7][i]]
        q = (fig(cube_net_svg(cells, "net of a cube with edge %d %s" % (s, u), k=34, side="%d %s" % (s, u))) +
             "This is a net of a cube. What is the surface area of the cube?")
        e = ("Each face is a square: %d × %d = %d %s². There are 6 faces: 6 × %d = %s %s²."
             % (s, s, s * s, u, s * s, f(SA), u))
        its.append(mcq(q, sq(SA, u), [sq(s ** 3, u), sq(4 * s * s, u), sq(s * s, u), cb(SA, u)][i % 2:], e))
    for i in range(10):
        L, W, H = pick_box(rnd, seen)
        u = UNITS[i % 4]
        t, b = [(0, 0), (2, 0), (0, 2), (2, 2)][i % 4]
        q = (fig(box_net_svg(L, W, H, u, t, b, label="net of a rectangular prism, %d by %d by %d" % (L, W, H))) +
             "What is the surface area of the rectangular prism made from this net?")
        e = box_e(L, W, H, u)
        if i % 3 == 0:
            e += " Do not stop at 3 faces: each face has a matching face."
        its.append(mcq(q, sq(sa_box(L, W, H), u), box_wrong(L, W, H, u, i % 4), e))
    for i in range(3):
        L, W, H = pick_box(rnd, seen)
        u = UNITS[(i + 1) % 4]
        q = (fig(prism_svg(L, W, H, u, "rectangular prism %d by %d by %d" % (L, W, H))) +
             "What is the surface area of this rectangular prism?")
        e = box_e(L, W, H, u) + " Surface area covers the outside, so it is in square units, not cubic units."
        its.append(mcq(q, sq(sa_box(L, W, H), u), box_wrong(L, W, H, u, (i + 1) % 4), e))
    its.append(mcq("A cube has a surface area of 96 cm². What is the area of one face?", "16 cm²",
                   ["24 cm²", "48 cm²", "4 cm²"],
                   "A cube has 6 faces that are the same: 96 ÷ 6 = 16 cm². (Each edge is 4 cm, since 4 × 4 = 16.)"))
    its.append(mcq("A box is 9 in long, 4 in wide and 3 in tall. Which expression gives its surface area?",
                   "2 × 36 + 2 × 27 + 2 × 12", ["9 × 4 × 3", "36 + 27 + 12", "2 × 9 + 2 × 4 + 2 × 3"],
                   "The faces are 9 × 4 = 36, 9 × 3 = 27 and 4 × 3 = 12, and each face has a match: "
                   "2 × 36 + 2 × 27 + 2 × 12 = 150 in². 9 × 4 × 3 is the volume."))
    its.append(mcq("A cube has edges that are 8 ft long. What is its surface area?", "384 ft²",
                   ["512 ft²", "256 ft²", "64 ft²"],
                   "One face: 8 × 8 = 64 ft². Six faces: 6 × 64 = 384 ft². 512 is the volume, and 256 counts only 4 faces."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Surface area of cubes and rectangular prisms", "items": its}


# ------------------------------------------------------------ set 4: pyramids and triangular prisms
def set_pyr_tri(rnd):
    its = []
    for i, (s, l) in enumerate([(4, 6), (6, 5), (5, 8), (8, 7), (10, 12), (6, 9), (7, 10)]):
        u = UNITS[i % 4]
        SA = sa_pyr(s, l)
        q = (fig(pyramid_net_svg(s, l, u, "net of a square pyramid, base %d, triangle height %d" % (s, l))) +
             "What is the surface area of the square pyramid made from this net?")
        pool = [sq(s * s + 4 * s * l, u), sq(2 * s * l, u), sq(s * s + s * l, u), cb(SA, u)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = pyr_e(s, l, u)
        if r == 0:
            e += " Remember the " + HALF + " in the triangle area."
        its.append(mcq(q, sq(SA, u), pool, e))
    tris = [(("right", 3, 4, 5), 7), (("right", 6, 8, 10), 12), (("right", 5, 12, 13), 10), (("right", 9, 12, 15), 20),
            (("right", 3, 4, 5), 9),
            (("iso", 6, 4, 5), 9), (("iso", 8, 3, 5), 10), (("iso", 10, 12, 13), 15), (("iso", 16, 6, 10), 20)]
    for i, (tri, L) in enumerate(tris):
        u = UNITS[(i + 1) % 4]
        two, per, (bb, hh) = tri_parts(tri)
        SA = two + per * L
        vol = two * L // 2
        pool = [sq(2 * two + per * L, u), sq(two // 2 + per * L, u), sq(per * L, u), sq(vol, u)]
        if tri[0] == "iso":
            pool.insert(0, sq(tri[1] * tri[3] + per * L, u))       # used the slanted side as the height
        r = i % 3
        pool = pool[r:] + pool[:r]
        e = tri_e(tri, L, u)
        if tri[0] == "iso":
            e += " Use the dashed height (%d %s), not the slanted side, for the triangles." % (hh, u)
        q = (fig(tri_prism_net_svg(tri, L, u, "net of a triangular prism")) +
             "What is the surface area of the triangular prism made from this net?")
        its.append(mcq(q, sq(SA, u), pool, e))
    for s, h, l, u in [(6, 4, 5, "cm"), (10, 12, 13, "in")]:
        assert (s // 2) ** 2 + h * h == l * l
        SA = sa_pyr(s, l)
        q = ("A square pyramid has a base %d %s on each side. The pyramid is %d %s tall, and the slant height "
             "(the height of each triangle face) is %d %s. What is its surface area?" % (s, u, h, u, l, u))
        e = pyr_e(s, l, u) + " Use the slant height %d, not the height of the pyramid, for the triangle faces." % l
        its.append(mcq(q, sq(SA, u), [sq(sa_pyr(s, h), u), sq(s * s + 4 * s * l, u), sq(2 * s * l, u)], e))
    # expressions
    its.append(mcq(fig(pyramid_net_svg(7, 9, "m", "net of a square pyramid, base 7, triangle height 9")) +
                   "Which expression gives the surface area of this square pyramid?",
                   "7 × 7 + 4 × " + HALF + " × 7 × 9",
                   ["7 × 7 + 4 × 7 × 9", "4 × " + HALF + " × 7 × 9", "7 × 7 × 9"],
                   "The base is 7 × 7. Each of the 4 triangles is " + HALF + " × 7 × 9. "
                   "Total: 49 + 126 = 175 m²."))
    its.append(mcq("A triangular prism has right-triangle bases with sides 3 ft, 4 ft and 5 ft. The prism is 6 ft long. "
                   "Which expression gives its surface area?",
                   "2 × " + HALF + " × 3 × 4 + (3 + 4 + 5) × 6",
                   ["2 × 3 × 4 + (3 + 4 + 5) × 6", HALF + " × 3 × 4 × 6", "(3 + 4 + 5) × 6"],
                   "Two triangles: 2 × " + HALF + " × 3 × 4 = 12. Three rectangles: (3 + 4 + 5) × 6 = 72. "
                   "Total: 12 + 72 = 84 ft²."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Surface area of pyramids and triangular prisms", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []
    n, he, his = P.next()
    L, W, H = 12, 8, 4
    its.append(mcq("%s wraps a gift box that is %d in long, %d in wide and %d in tall. How much wrapping paper covers the box with no overlap?"
                   % (n, L, W, H), sq(sa_box(L, W, H), "in"), [sq(L * W * H, "in"), sq(sa_box(L, W, H) // 2, "in"), cb(sa_box(L, W, H), "in")],
                   box_e(L, W, H, "in")))
    assert sa_box(12, 8, 4) == 352
    n, he, his = P.next()
    # toy box with no top: 4 × 2 × 2 ft
    full, top = sa_box(4, 2, 2), 4 * 2
    its.append(mcq("%s paints the outside of a toy box with no lid. The box is 4 ft long, 2 ft wide and 2 ft tall. "
                   "How many square feet does %s paint?" % (n, he), sq(full - top, "ft"),
                   [sq(full, "ft"), sq(4 * 2 * 2, "ft"), sq(full - 2 * top, "ft")],
                   "All 6 faces: 2 × 8 + 2 × 8 + 2 × 4 = %d ft². There is no top, so subtract one 4 × 2 face: %d − 8 = %d ft²."
                   % (full, full, full - top)))
    # tent with floor
    b, h, s, L = 6, 4, 5, 8
    tent = b * h + (2 * s + b) * L
    its.append(mcq("A tent is a triangular prism. Each end is a triangle with a base of 6 ft and a height of 4 ft, and the "
                   "slanted sides are 5 ft wide. The tent is 8 ft long. How much fabric covers the 2 ends, the 2 slanted sides and the floor?",
                   sq(tent, "ft"), [sq(b * h + 2 * s * L, "ft"), sq(2 * b * h + (2 * s + b) * L, "ft"), sq(b * h * L // 2, "ft")],
                   "Ends: 2 × " + HALF + " × 6 × 4 = 24. Slanted sides: 2 × 5 × 8 = 80. Floor: 6 × 8 = 48. "
                   "Total: 24 + 80 + 48 = %d ft²." % tent))
    # tent with no floor
    b, h, s, L = 8, 3, 5, 10
    nofloor = b * h + 2 * s * L
    its.append(mcq("A tent has no floor. Its ends are triangles with a base of 8 ft and a height of 3 ft. The two slanted sides are "
                   "5 ft by 10 ft. How much fabric is in the tent?", sq(nofloor, "ft"),
                   [sq(nofloor + b * L, "ft"), sq(2 * b * h + 2 * s * L, "ft"), sq(b * h // 2 + 2 * s * L, "ft")],
                   "Ends: 2 × " + HALF + " × 8 × 3 = 24. Sides: 2 × 5 × 10 = 100. No floor, so the total is 24 + 100 = %d ft²." % nofloor))
    n, he, his = P.next()
    its.append(mcq("%s covers a cube-shaped gift box with paper. Each edge is 10 cm. How much paper does %s need?" % (n, he),
                   "600 cm²", ["1,000 cm²", "400 cm²", "100 cm²"],
                   "One face: 10 × 10 = 100 cm². Six faces: 6 × 100 = 600 cm². 1,000 is the volume in cm³."))
    its.append(mcq("A cereal box is 8 in wide, 3 in deep and 12 in tall. How much cardboard is used to make it (no overlaps)?",
                   sq(sa_box(8, 3, 12), "in"), [sq(8 * 3 * 12, "in"), sq(sa_box(8, 3, 12) // 2, "in"), cb(sa_box(8, 3, 12), "in")],
                   box_e(8, 3, 12, "in")))
    its.append(mcq("A roof is shaped like a square pyramid with no bottom. The base is 12 ft on each side, and each triangle has a "
                   "slant height of 10 ft. How many square feet of shingles cover the 4 triangles?", "240 ft²",
                   ["384 ft²", "480 ft²", "120 ft²"],
                   "One triangle: " + HALF + " × 12 × 10 = 60 ft². Four triangles: 4 × 60 = 240 ft². The base is not part of the roof."))
    n, he, his = P.next()
    sa = sa_box(5, 3, 2)
    its.append(mcq("%s paints all 6 faces of a wooden chest that is 5 ft long, 3 ft wide and 2 ft tall. Paint costs $2 for each square foot. "
                   "How much does the paint cost?" % n, "$%d" % (2 * sa), ["$%d" % sa, "$%d" % (2 * 5 * 3 * 2), "$%d" % (sa // 2)],
                   "Surface area: 2 × 15 + 2 × 10 + 2 × 6 = %d ft². Cost: %d × $2 = $%d." % (sa, sa, 2 * sa)))
    its.append(mcq("Box A is a cube with 6 in edges. Box B is 9 in by 4 in by 6 in. Both hold 216 in³. Which box needs more paper to cover it?",
                   "B, by 12 in²", ["A, by 12 in²", "Same amount", "B, by 228 in²"],
                   "A: 6 × 36 = 216 in². B: 2 × 36 + 2 × 54 + 2 × 24 = 228 in². B needs 228 − 216 = 12 in² more. "
                   "The same volume does not mean the same surface area."))
    n, he, his = P.next()
    sides = 2 * (10 * 8 + 6 * 8)
    its.append(mcq("%s covers only the 4 sides of a box (not the top or bottom). The box is 10 cm long, 6 cm wide and 8 cm tall. "
                   "How much paper does %s use?" % (n, he), sq(sides, "cm"),
                   [sq(sa_box(10, 6, 8), "cm"), sq(sides // 2, "cm"), sq(10 * 6 * 8, "cm")],
                   "Front and back: 2 × (10 × 8) = 160. Two sides: 2 × (6 × 8) = 96. Total: 160 + 96 = %d cm²." % sides))
    tank = 20 * 10 + 2 * 20 * 12 + 2 * 10 * 12
    its.append(mcq("A fish tank with no lid is 20 in long, 10 in wide and 12 in tall. How much glass is used to make it?",
                   sq(tank, "in"), [sq(tank + 200, "in"), sq(20 * 10 * 12, "in"), sq(200 + 240 + 120, "in")],
                   "Bottom: 20 × 10 = 200. Front and back: 2 × (20 × 12) = 480. Ends: 2 × (10 × 12) = 240. "
                   "No lid, so the total is 200 + 480 + 240 = %s in²." % f(tank)))
    sand = 6 * 4 + 2 * 6 * 1 + 2 * 4 * 1
    its.append(mcq("A wooden sandbox has a bottom but no top. It is 6 ft long, 4 ft wide and 1 ft tall. How many square feet of wood is it made of?",
                   sq(sand, "ft"), [sq(sand + 24, "ft"), sq(24 + 6 + 4, "ft"), sq(2 * 6 + 2 * 4, "ft")],
                   "Bottom: 6 × 4 = 24. Long sides: 2 × (6 × 1) = 12. Short sides: 2 × (4 × 1) = 8. "
                   "No top: 24 + 12 + 8 = %d ft²." % sand))
    n, he, his = P.next()
    its.append(mcq("%s paints every face of a wooden cube with 3 in edges. How much area does %s paint?" % (n, he),
                   "54 in²", ["27 in²", "36 in²", "9 in²"],
                   "One face: 3 × 3 = 9 in². Six faces: 6 × 9 = 54 in². 27 is the volume, and 36 counts only 4 faces."))
    its.append(mcq("A paperweight is a square pyramid. Its base is 4 cm on each side, and each triangle face has a height of 5 cm. "
                   "What is its total surface area?", "56 cm²", ["96 cm²", "40 cm²", "36 cm²"],
                   "Base: 4 × 4 = 16. Triangles: 4 × " + HALF + " × 4 × 5 = 40. Total: 16 + 40 = 56 cm²."))
    its.append(mcq("A planter is a cube with an open top. Each edge is 2 ft. How much area of the outside is painted (no top)?",
                   "20 ft²", ["24 ft²", "8 ft²", "16 ft²"],
                   "One face: 2 × 2 = 4 ft². The planter has 5 faces (no top): 5 × 4 = 20 ft²."))
    n, he, his = P.next()
    one = sa_box(6, 4, 3)
    its.append(mcq("%s wraps 2 boxes that are the same. Each box is 6 cm by 4 cm by 3 cm. How much paper does %s need for both boxes?"
                   % (n, he), sq(2 * one, "cm"), [sq(one, "cm"), sq(2 * 6 * 4 * 3, "cm"), cb(2 * one, "cm")],
                   "One box: 2 × 24 + 2 × 18 + 2 × 12 = %d cm². Two boxes: 2 × %d = %d cm²." % (one, one, 2 * one)))
    its.append(mcq("A cube has a surface area of 150 cm². How long is each edge?", "5 cm",
                   ["25 cm", "37.5 cm", "50 cm"],
                   "6 faces share 150 cm², so one face is 150 ÷ 6 = 25 cm². A square with area 25 has 5 cm sides (5 × 5 = 25)."))
    ramp = 5 * 12 + (5 + 12 + 13) * 3
    its.append(mcq("A wooden ramp is a triangular prism. Its ends are right triangles with sides 5 ft, 12 ft and 13 ft, and the ramp is 3 ft wide. "
                   "How much area is painted if every face is painted?", sq(ramp, "ft"),
                   [sq(2 * 60 + 90, "ft"), sq(30 + 90, "ft"), sq(30 * 3, "ft")],
                   "Ends: 2 × " + HALF + " × 5 × 12 = 60. Rectangles: (5 + 12 + 13) × 3 = 90. Total: 60 + 90 = %d ft²." % ramp))
    room = 2 * 12 * 8 + 2 * 10 * 8 + 12 * 10
    its.append(mcq("A room is 12 ft long, 10 ft wide and 8 ft tall. How many square feet are painted if the 4 walls and the ceiling are painted, but not the floor?",
                   sq(room, "ft"), [sq(room + 120, "ft"), sq(room - 120, "ft"), sq(960, "ft")],
                   "Walls: 2 × (12 × 8) + 2 × (10 × 8) = 192 + 160 = 352. Ceiling: 12 × 10 = 120. Total: 352 + 120 = %d ft²." % room))
    its.append(mcq("Which unit could be used for the surface area of a box?", "square inches",
                   ["cubic inches", "inches", "pounds"],
                   "Surface area is the area of all the faces, so it is in square units, like in². Cubic inches measure volume."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Surface area word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    pairs = [PAIR[0], PAIR[2], PAIR[0], PAIR[2], PAIR[1], PAIR[1]]
    return (
        "<h2>What a net is</h2>"
        "<p>A <b>net</b> is a flat pattern that folds up into a solid. Each shape in the net is one face of the solid. "
        "<b>Surface area</b> is the total area of all the faces, so it is the area of the whole net.</p>"
        "<figure class='sn-fig'>" + prism_svg(6, 3, 4, "cm", "box 6 by 3 by 4 cm") + " " +
        box_net_svg(6, 3, 4, "cm", label="net of the box 6 by 3 by 4 cm", cols=pairs) +
        "<figcaption>The box and its net. Faces of the same color match: top and bottom, front and back, and the two ends.</figcaption></figure>"
        "<h2>Rectangular prisms and cubes</h2>"
        "<p>Find the area of 3 different faces, then double each one, because every face has a matching face.</p>"
        "<p><b>SA = 2lw + 2lh + 2wh</b>. A cube has 6 faces that are the same: <b>SA = 6 × s × s</b>.</p>" +
        ex("Box", "Find the surface area of the box above: 6 cm long, 3 cm wide, 4 cm tall.",
           "Top and bottom: 2 × (6 × 3) = 36. Front and back: 2 × (6 × 4) = 48. Ends: 2 × (3 × 4) = 24. "
           "36 + 48 + 24 = 108.", "108 cm²") +
        "<h2>Pyramids and triangular prisms</h2>"
        "<p>A triangle face has area " + HALF + " × base × height. Use the height that is at a right angle to the base "
        "(the dashed line), not a slanted side.</p>"
        "<figure class='sn-fig'>" + pyramid_net_svg(6, 5, "cm", "net of a square pyramid, base 6 cm, triangle height 5 cm") +
        "<figcaption>Square pyramid: base 6 × 6 = 36. Four triangles: 4 × " + HALF + " × 6 × 5 = 60. "
        "SA = 36 + 60 = 96 cm².</figcaption></figure>"
        "<figure class='sn-fig'>" + tri_prism_net_svg(("right", 3, 4, 5), 8, "in", "net of a triangular prism with 3-4-5 triangles, 8 in long") +
        "<figcaption>Triangular prism: two triangles 2 × " + HALF + " × 3 × 4 = 12. Three rectangles (3 + 4 + 5) × 8 = 96. "
        "SA = 12 + 96 = 108 in².</figcaption></figure>" +
        ex("Box with no top", "An open box is 5 in long, 4 in wide and 2 in tall. How much cardboard is it made of?",
           "All 6 faces: 2 × 20 + 2 × 10 + 2 × 8 = 76. No top, so subtract one 5 × 4 face: 76 − 20 = 56.", "56 in²") +
        "<h2>Nets of common solids</h2>" +
        table(["Solid", "Faces in the net", "Surface area"], [
            ["Cube", "6 equal squares", "6 × s × s"],
            ["Rectangular prism", "6 rectangles in 3 matching pairs", "2lw + 2lh + 2wh"],
            ["Triangular prism", "2 triangles + 3 rectangles", "2 triangles + (perimeter of triangle) × length"],
            ["Square pyramid", "1 square + 4 triangles", "s × s + 4 × " + HALF + " × s × (slant height)"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Finding the volume (l × w × h)", "Add the areas of the faces"],
            ["Adding only 3 faces of a box", "Double each one: every face has a match"],
            ["Forgetting the " + HALF + " for a triangle", HALF + " × base × height"],
            ["Using the pyramid’s height or a slanted side", "Use the height of the triangle face (slant height)"],
            ["Counting a missing top", "Leave out faces that are not there (open box, roof, tent with no floor)"],
            ["Writing cm³", "Surface area is an area: cm², in², ft²"],
        ])
    )


FAQ = [
    {"q": "How do you find surface area using a net?",
     "a": "Unfold the solid into a net, find the area of each face (rectangles: length × width; triangles: " + HALF + " × base × height), and add all the areas. The answer is in square units."},
    {"q": "What is the formula for the surface area of a rectangular prism?",
     "a": "SA = 2lw + 2lh + 2wh. Find the area of the top, front and side, then double each one, because each face has a matching face on the other side."},
    {"q": "How do you find the surface area of a square pyramid?",
     "a": "Add the area of the square base (s × s) and the 4 triangle faces (4 × " + HALF + " × s × slant height). Use the slant height, which is the height of a triangle face, not the height of the pyramid."},
    {"q": "What is the difference between surface area and volume?",
     "a": "Surface area is the area that covers the outside of a solid, in square units like cm². Volume is the space inside, in cubic units like cm³."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(617)
    P = People(rnd)
    sets = [set_identify(rnd), set_faces(rnd), set_boxes(rnd, P), set_pyr_tri(rnd), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4 and "" not in it["c"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "surface-area-nets", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Surface Area Using Nets",
        "seo_title": "Grade 6 Surface Area and Nets Worksheets: Prisms, Pyramids and Word Problems",
        "short_title": "Surface Area and Nets",
        "domain": "Geometry",
        "standard_code": "6.G.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/G/A/4/",
        "standard_text": "Represent three-dimensional figures using nets made up of rectangles and triangles, and use the nets to find the surface area of these figures. Apply these techniques in the context of solving real-world and mathematical problems.",
        "meta_desc": "Free Grade 6 surface area worksheets: match nets to solids, count faces, and use nets to find the surface area of cubes, rectangular prisms, triangular prisms and square pyramids, plus real-world word problems. 100 practice questions with answers.",
        "key_big": "Surface area = the total area of all the faces (the area of the net).",
        "key_sub": "Unfold the solid into a net, find the area of each rectangle and triangle, and add them. A box has 3 pairs of matching faces: SA = 2lw + 2lh + 2wh. The answer is in square units (cm², ft²).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(net of|four patterns)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
