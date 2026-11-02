# -*- coding: utf-8 -*-
"""
British Columbia Grade 8 Math: Views and nets of 3D objects (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g8_views_nets.py
Canadian English, metric units, π ≈ 3.14 with decimal.Decimal (never float for answers).
HTML attributes use single quotes (no backslashes in the JSON).

Pictures (checked in code):
  cube structures  stacks of unit cubes on a grid, drawn in isometric view (front face lower left, right face
                   lower right, red arrow = the front). Cubes are painted far to near (x + y − z), so the
                   picture is exact. Every stack's top face must be visible (its centre and 7 of 9 sample points,
                   tested against all nearer cubes), so no stack is hidden and the cubes can be counted.
  views            computed from the same data: front = tallest stack in each column (left to right),
                   right side = tallest stack in each row seen from the right (front of the object on the LEFT,
                   third-angle convention), top = footprint with the front at the bottom.
  matching         every wrong structure differs from the given views in at least one view (asserted);
                   least / greatest number of cubes from 3 views is found by brute force over all heights.
  nets             prism, pyramid and cylinder nets drawn to scale; a cylinder's rectangle is 2πr long and the
                   circles touch the edges of that length; triangles of pyramids fold to one apex (equal slant edges).
Wrong answers come from real student mistakes: front and side views mixed up, the side view drawn the
wrong way round (from the left), the top view flipped, only the front row counted, counting only the cubes
you can see, prism vs pyramid, the bases of a prism on the same side of the net, a cylinder's rectangle as
long as the diameter or πr, using the diameter as r.
"""
import itertools, json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
PI = Dm("3.14")
NB = " "
C30 = math.sqrt(3) / 2
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

CUBE, RP, TP, SP, TPY = "cube", "rectangular prism", "triangular prism", "square-based pyramid", "triangular pyramid"
PP, HP, PPY, HPY, RPY = "pentagonal prism", "hexagonal prism", "pentagonal pyramid", "hexagonal pyramid", "rectangular pyramid"
CYL, CONE = "cylinder", "cone"


def N(x):
    """Decimal text without trailing zeros; 5+ digit whole parts get no-break spaces."""
    s = format(Dm(str(x)).normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    whole, _, frac = s.partition(".")
    if len(whole) >= 5:
        g = []
        while whole:
            g.insert(0, whole[-3:])
            whole = whole[:-3]
        whole = NB.join(g)
    return whole + ("." + frac if frac else "")


def words(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("0 ") or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q[-80:], correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
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
    """Positions for picture answers (A-D), spread evenly."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ drawing
def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count(".") * 0.6 - t.count(NB) * 0.3) * fs * 0.6


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
    """Shapes and text in screen coordinates (y down); writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2, col=GREEN, dashed=False, solid=True):
        self.el.append(("p", pts, fill, sw, col, dashed))
        if solid:
            self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=2, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.polys.append(circle_pts(c, r))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert all(h == len(pts) for h in hit), ("label crosses a face edge", (x0, y0, x1, y1), hit)
            for a, b in self.segs:
                for i in range(41):
                    x, y = a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40
                    assert not (x0 - 2 < x < x1 + 2 and y0 - 2 < y < y1 + 2), ("line through a label", (x0, y0))

    def merge(self, o, dx, dy):
        """Copy canvas o into this one, shifted by (dx, dy)."""
        S = lambda p: (p[0] + dx, p[1] + dy)
        for e in o.el:
            if e[0] == "p":
                self.el.append(("p", [S(p) for p in e[1]]) + e[2:])
            elif e[0] == "c":
                self.el.append(("c", S(e[1])) + e[2:])
            elif e[0] == "l":
                self.el.append(("l", S(e[1]), S(e[2])) + e[3:])
            else:
                self.el.append(("t", e[1] + dx, e[2] + dy) + e[3:])
        for b in o.boxes:
            nb = (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)
            for b2 in self.boxes:
                assert nb[2] < b2[0] or b2[2] < nb[0] or nb[3] < b2[1] or b2[3] < nb[1], "labels touch"
            self.boxes.append(nb)
        self.polys += [[S(p) for p in poly] for poly in o.polys]
        self.segs += [(S(a), S(b)) for a, b in o.segs]
        self.grow(o.x0 + dx, o.y0 + dy, o.x1 + dx, o.y1 + dy)

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


def place(main, cv, x, y, w=None, h=None):
    """Put canvas cv with its top-left corner at (x, y), centred in a w × h box if given."""
    cw, ch = cv.size()
    dx = x - cv.x0 + ((w - cw) / 2 if w else 0)
    dy = y - cv.y0 + ((h - ch) / 2 if h else 0)
    main.merge(cv, dx, dy)


def row_svg(cvs, caps, label, gap=24, fs=17, col=GREEN):
    """Pictures side by side with a caption under each."""
    H = max(cv.size()[1] for cv in cvs)
    main = Canvas()
    x = 0
    for cv, cap in zip(cvs, caps):
        cv.check()
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        place(main, cv, x, 0, cw, H)
        main.text(x + cw / 2, H + 10 + fs / 2, cap, fs, col=col)
        x += cw + gap
    return main.svg(label, check=False)


# ------------------------------------------------------------ cube structures
def norm_struct(cols):
    x0 = min(x for x, z in cols)
    z0 = min(z for x, z in cols)
    return {(x - x0, z - z0): h for (x, z), h in cols.items() if h > 0}


def skey(cols):
    return tuple(sorted(norm_struct(cols).items()))


def dims(cols):
    return max(x for x, z in cols) + 1, max(z for x, z in cols) + 1


def cubes_of(cols):
    return [(x, y, z) for (x, z), h in cols.items() for y in range(h)]


def depth(c):
    return c[0] + c[1] - c[2]


def isoP(x, y, z, k):
    return ((x + z) * C30 * k, ((x - z) * 0.5 - y) * k)


def hull(pts):
    pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def cube_hull(c):
    x, y, z = c
    return hull([isoP(x + a, y + b, z + d, 1) for a in (0, 1) for b in (0, 1) for d in (0, 1)])


def connected(cols):
    cells = list(cols)
    seen, todo = {cells[0]}, [cells[0]]
    while todo:
        c = todo.pop()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if n in cols and n not in seen:
                seen.add(n)
                todo.append(n)
    return len(seen) == len(cells)


def tops_visible(cols):
    """Every stack's top face is visible in the isometric picture (its centre and at least 7 of 9 sample points)."""
    cs = cubes_of(cols)
    hulls = {c: cube_hull(c) for c in cs}
    for (x, z), h in cols.items():
        top = (x, h - 1, z)
        seen = 0
        for u in (0.1, 0.5, 0.9):
            for v in (0.1, 0.5, 0.9):
                p = isoP(x + u, h, z + v, 1)
                hid = any(depth(c) > depth(top) and inside(p, hulls[c]) for c in cs)
                if hid and u == v == 0.5:
                    return False
                seen += not hid
        if seen < 7:
            return False
    return True


def visible_cubes(cols):
    """Cubes with at least one face you can see in the picture."""
    cs = cubes_of(cols)
    hulls = {c: cube_hull(c) for c in cs}
    n = 0
    for c in cs:
        x, y, z = c
        centres = [isoP(x + 0.5, y + 1, z + 0.5, 1), isoP(x + 0.5, y + 0.5, z, 1), isoP(x + 1, y + 0.5, z + 0.5, 1)]
        if any(not any(depth(o) > depth(c) and inside(p, hulls[o]) for o in cs) for p in centres):
            n += 1
    return n


def valid(cols):
    return cols and connected(cols) and tops_visible(cols)


# views: a view is a frozenset of squares (i, j): i from the left, j from the bottom
def v_front(cols):
    W, D = dims(cols)
    return frozenset((x, j) for x in range(W) for j in range(max([cols.get((x, z), 0) for z in range(D)])))


def heights_front(cols):
    W, D = dims(cols)
    return [max(cols.get((x, z), 0) for z in range(D)) for x in range(W)]


def heights_right(cols):
    """Seen from the right: the front of the object is on the left of the view."""
    W, D = dims(cols)
    return [max(cols.get((x, z), 0) for x in range(W)) for z in range(D)]


def from_heights(hs):
    return frozenset((i, j) for i, h in enumerate(hs) for j in range(h))


def v_right(cols):
    return from_heights(heights_right(cols))


def v_left(cols):
    return from_heights(heights_right(cols)[::-1])


def v_back(cols):
    return from_heights(heights_front(cols)[::-1])


def v_top(cols):
    return frozenset((x, z) for (x, z) in cols)


def v_top_mirror(cols):
    W, D = dims(cols)
    return frozenset((W - 1 - x, z) for (x, z) in cols)


def v_top_flip(cols):
    W, D = dims(cols)
    return frozenset((x, D - 1 - z) for (x, z) in cols)


def v_front_row(cols):
    """Mistake: only the cubes in the front row."""
    W, D = dims(cols)
    return from_heights([cols.get((x, 0), 0) for x in range(W)])


def vnorm(v):
    i0 = min(i for i, j in v)
    j0 = min(j for i, j in v)
    return frozenset((i - i0, j - j0) for i, j in v)


def views3(cols):
    return (vnorm(v_top(cols)), vnorm(v_front(cols)), vnorm(v_right(cols)))


def view_cv(v, k=16, nums=None, fill=FILL):
    v = vnorm(v)
    J = max(j for i, j in v)
    cv = Canvas()
    for i, j in sorted(v):
        x, y = i * k, (J - j) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], fill, 1.8)
        if nums:
            cv.text(x + k / 2, y + k / 2, str(nums[(i, j)]), 16, col=GREEN)
    return cv


def arrow(cv, tail, tip, col=RED):
    cv.line(tail, tip, sw=2.6, col=col)
    dx, dy = tip[0] - tail[0], tip[1] - tail[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    a = (tip[0] - ux * 10 + uy * 5, tip[1] - uy * 10 - ux * 5)
    b = (tip[0] - ux * 10 - uy * 5, tip[1] - uy * 10 + ux * 5)
    cv.poly([tip, a, b], col, 1, col, solid=False)


def iso_cv(cols, k=22, front=True, word=True):
    cv = Canvas()
    for c in sorted(cubes_of(cols), key=lambda c: (depth(c), c)):
        x, y, z = c
        P = lambda a, b, d: isoP(a, b, d, k)
        cv.poly([P(x, y + 1, z), P(x + 1, y + 1, z), P(x + 1, y + 1, z + 1), P(x, y + 1, z + 1)], TOP3, 1.6, solid=False)
        cv.poly([P(x, y, z), P(x + 1, y, z), P(x + 1, y + 1, z), P(x, y + 1, z)], FILL, 1.6, solid=False)
        cv.poly([P(x + 1, y, z), P(x + 1, y, z + 1), P(x + 1, y + 1, z + 1), P(x + 1, y + 1, z)], SIDE, 1.6, solid=False)
    for c in cubes_of(cols):
        cv.polys.append([(px * k, py * k) for px, py in cube_hull(c)])
    if front:
        W, D = dims(cols)
        xm = W / 2
        tip = isoP(xm, 0, -0.3, k)
        tail = isoP(xm, 0, -1.5, k)
        arrow(cv, tail, tip)
        if word:
            t = isoP(xm, 0, -1.5, k)
            cv.text(t[0] - 24, t[1] + 14, "Front", 14, col=RED)
    return cv


def iso_svg(cols, label="structure of cubes, the red arrow shows the front", k=22):
    return iso_cv(cols, k).svg(label)


def mat_cv(cols, k=30, word=True):
    """Top view with the number of cubes in each stack; front at the bottom."""
    v = v_top(cols)
    nums = {(x, z): cols[(x, z)] for (x, z) in cols}
    cv = view_cv(v, k, nums)
    if word:
        W, D = dims(cols)
        cv.text(W * k / 2, D * k + 16, "Front", 14, col=RED)
    return cv


def rand_struct(rnd, W, D, hmax=3, n_lo=4, n_hi=12, hmin_top=2):
    for _ in range(4000):
        cols = {}
        for x in range(W):
            for z in range(D):
                h = rnd.choice([0, 1, 1, 2, 2, 3][:3 + hmax])
                if h:
                    cols[(x, z)] = h
        if not cols:
            continue
        cols = norm_struct(cols)
        if dims(cols) != (W, D):
            continue
        n = sum(cols.values())
        if not (n_lo <= n <= n_hi) or max(cols.values()) < hmin_top:
            continue
        if valid(cols):
            return cols
    raise AssertionError("no structure")


# ------------------------------------------------------------ set 1: views of cube structures
VIEWF = {"front": v_front, "right": v_right, "left": v_left, "back": v_back, "top": v_top,
         "top_mirror": v_top_mirror, "top_flip": v_top_flip, "front_row": v_front_row}
VNAME = {"front": "the front view", "right": "the right side view", "left": "the view from the left side",
         "back": "the view from the back", "top": "the top view", "top_mirror": "the top view flipped left to right",
         "top_flip": "the top view upside down (front at the top)", "front_row": "only the front row of cubes"}
DISTRACT = {"front": ["right", "front_row", "left", "back", "top"],
            "right": ["front", "left", "back", "top", "front_row"],
            "top": ["top_flip", "top_mirror", "front", "right"]}


def pick_views(cols, ask, rnd):
    want = vnorm(VIEWF[ask](cols))
    got, tags = [want], []
    for d in DISTRACT[ask]:
        if d == "front_row" and 0 in [cols.get((x, 0), 0) for x in range(dims(cols)[0])]:
            continue                                  # a front row with gaps would look like a smaller structure
        v = vnorm(VIEWF[d](cols))
        if v not in got:
            got.append(v)
            tags.append(d)
        if len(tags) == 3:
            break
    if len(tags) < 3:
        return None
    return want, list(zip(got[1:], tags))


def struct_views_svg(left_cv, views, label, cap_fs=16):
    """Structure (or mat) on the left, 4 views A-D in a 2 x 2 grid on the right."""
    main = Canvas()
    lw, lh = left_cv.size()
    cw = max(view_cv(v).size()[0] for v in views)
    ch = max(view_cv(v).size()[1] for v in views)
    cw = max(cw, 40)
    cellw, cellh = cw + 34, ch + 30
    gx = lw + 34
    H = max(lh, 2 * cellh)
    place(main, left_cv, 0, (H - lh) / 2)
    for i, v in enumerate(views):
        cx, cy = gx + (i % 2) * cellw, (i // 2) * cellh + (H - 2 * cellh) / 2
        main.text(cx + 8, cy + 9, "ABCD"[i], cap_fs, col=BLUE)
        place(main, view_cv(v), cx + 24, cy + 2, cw, ch)
    return main.svg(label, check=True)


def views_q(rnd, cols, ask, p, use_mat=False):
    r = pick_views(cols, ask, rnd)
    assert r
    want, wrong = r
    rnd.shuffle(wrong)
    opts = wrong[:p] + [(want, ask)] + wrong[p:]
    left = mat_cv(cols) if use_mat else iso_cv(cols)
    lab = "mat plan and four views labelled A to D" if use_mat else "structure of cubes and four views labelled A to D"
    svg = struct_views_svg(left, [v for v, t in opts], lab)
    L = "ABCD"
    if use_mat:
        intro = "The mat plan shows how many cubes are in each stack (the front is at the bottom). "
    else:
        intro = "The red arrow shows the front of the structure. "
    if ask == "front":
        q = intro + "Which is the front view?"
        hs = heights_front(cols)
        e = ("Look from the front. From left to right, the tallest stack in each column has %s cubes, so the front view is %s."
             % (words(hs), L[p]))
    elif ask == "right":
        q = intro + "Which is the view from the right side?"
        hs = heights_right(cols)
        e = ("Stand on the right and look across: the front of the structure is on your left. From front to back, the tallest "
             "stack in each row has %s cubes, so the right side view is %s." % (words(hs), L[p]))
    else:
        q = intro + "Which is the top view?"
        e = ("From above, each stack shows as one square, however tall it is. With the front at the bottom, the top view is %s."
             % L[p])
    notes = []
    for i, (v, t) in enumerate(opts):
        if i != p and t in ("front", "right", "left", "top_flip"):
            notes.append("%s is %s" % (L[i], VNAME[t]))
    if notes:
        e += " " + "; ".join(notes) + "."
    if use_mat and ask in ("front", "right"):
        e = e.replace("Look from the front.", "Read the mat plan from the bottom (the front).")
    return mcq_fixed(fig(svg) + q, list(L), L[p], e)


def set_views(rnd, used):
    its = []
    pos = Pos(rnd)
    asks = ["front"] * 7 + ["right"] * 7 + ["top"] * 6
    sizes = [(3, 2), (2, 3), (3, 3), (3, 2), (2, 2), (3, 3), (2, 3)]
    i = 0
    for ask in asks:
        while True:
            W, D = sizes[i % len(sizes)]
            i += 1
            cols = rand_struct(rnd, W, D, n_hi=11)
            if skey(cols) in used or not pick_views(cols, ask, rnd):
                continue
            if vnorm(v_front(cols)) == vnorm(v_right(cols)):
                continue
            if ask in ("front", "right") and len(set((heights_front if ask == "front" else heights_right)(cols))) == 1:
                continue                              # a plain rectangle is too easy
            if ask == "top" and vnorm(v_top(cols)) == vnorm(v_top_mirror(cols)) == vnorm(v_top_flip(cols)):
                continue
            break
        used.add(skey(cols))
        its.append(views_q(rnd, cols, ask, pos.next()))
    assert len(its) == 20
    return {"title": "Top, front and side views of cube structures", "items": its}


# ------------------------------------------------------------ set 2: which object matches the views?
def rot90(cols):
    W, D = dims(cols)
    return norm_struct({(z, W - 1 - x): h for (x, z), h in cols.items()})


def mirror(cols):
    W, D = dims(cols)
    return norm_struct({(W - 1 - x, z): h for (x, z), h in cols.items()})


def variants(cols, rnd):
    out = [("turn", rot90(cols)), ("mirror", mirror(cols)), ("turn", rot90(rot90(rot90(cols))))]
    cells = sorted(cols)
    W, D = dims(cols)
    for a in cells:
        if cols[a] > 1 or len(cols) > 1:
            for b in [(x, z) for x in range(W) for z in range(D)]:
                if b != a:
                    n = dict(cols)
                    n[a] -= 1
                    if n[a] == 0:
                        del n[a]
                    n[b] = n.get(b, 0) + 1
                    if n[b] <= 3 and n:
                        out.append(("move", norm_struct(n)))
    for a in cells:
        n = dict(cols)
        n[a] += 1
        if n[a] <= 3:
            out.append(("add", norm_struct(n)))
    rnd.shuffle(out)
    return out


VIEW_NAMES = ("top view", "front view", "right side view")


def match_q(rnd, cols, p):
    want = views3(cols)
    cands = []
    seen = {skey(cols)}
    for tag, v in variants(cols, rnd):
        if skey(v) in seen or not valid(v) or dims(v)[0] > 3 or dims(v)[1] > 3:
            continue
        w3 = views3(v)
        diff = [VIEW_NAMES[i] for i in range(3) if w3[i] != want[i]]
        if not diff:
            continue
        seen.add(skey(v))
        cands.append((len(diff), tag, v, diff))
    # prefer wrong objects that match 2 of the 3 views; always include a turned one (front and side swapped)
    cands.sort(key=lambda c: (c[0], c[1] != "turn"))
    turned = [c for c in cands if c[1] == "turn"]
    pick = (turned[:1] + [c for c in cands if c not in turned[:1]])[:3]
    assert len(pick) == 3
    rnd.shuffle(pick)
    opts = [c[2] for c in pick]
    opts.insert(p, cols)
    for i, o in enumerate(opts):
        assert (views3(o) == want) == (i == p)
    # picture: 3 views on top, 4 structures below
    main = Canvas()
    vk = 16
    vcs = [view_cv(want[0], vk), view_cv(want[1], vk), view_cv(want[2], vk)]
    caps = ["Top", "Front", "Right side"]
    ws = [max(c.size()[0], tw(cap, 15) + 4) for c, cap in zip(vcs, caps)]
    top_w = sum(ws) + 2 * 40
    ics = [iso_cv(o, 17, front=True, word=False) for o in opts]
    ih = max(c.size()[1] for c in ics)
    iw = max(c.size()[0] for c in ics)
    tot = 4 * (iw + 22) - 22
    x = max(0, (tot - top_w) / 2)
    vh = max(c.size()[1] for c in vcs)
    for c, cap, w in zip(vcs, caps, ws):
        place(main, c, x, 0, w, vh)
        main.text(x + w / 2, vh + 14, cap, 15, col=INK)
        x += w + 40
    y0 = vh + 40
    sx = max(0, (top_w - tot) / 2)
    for i, c in enumerate(ics):
        cx = sx + i * (iw + 22)
        place(main, c, cx, y0, iw, ih)
        main.text(cx + iw / 2, y0 + ih + 14, "ABCD"[i], 16, col=BLUE)
    svg = main.svg("top, front and right side views and four structures labelled A to D")
    notes = []
    for i, (n, tag, v, diff) in enumerate(pick):
        j = i if i < p else i + 1
        if tag == "turn" and "front view" in diff and "right side view" in diff:
            notes.append("%s has the front and side views swapped (it is turned a quarter turn)" % "ABCD"[j])
        else:
            notes.append("%s has a different %s" % ("ABCD"[j], words(diff)))
    e = ("Only %s matches all three views. Check each view in turn: %s." % ("ABCD"[p], "; ".join(sorted(notes))))
    q = fig(svg) + "Which structure has these three views? The red arrows show the front."
    return mcq_fixed(q, list("ABCD"), "ABCD"[p], e)


def mat_match_q(rnd, cols, p):
    """Mat plan -> which structure."""
    cands = []
    seen = {skey(cols)}
    for tag, v in variants(cols, rnd):
        if skey(v) in seen or not valid(v) or dims(v)[0] > 3 or dims(v)[1] > 3:
            continue
        seen.add(skey(v))
        cands.append((tag, v))
    cands.sort(key=lambda c: (c[0] not in ("turn", "mirror"), abs(sum(c[1].values()) - sum(cols.values()))))
    pick = cands[:3]
    rnd.shuffle(pick)
    opts = [c[1] for c in pick]
    opts.insert(p, cols)
    main = Canvas()
    m = mat_cv(cols, 26)
    ics = [iso_cv(o, 17, front=True, word=False) for o in opts]
    ih = max(c.size()[1] for c in ics)
    iw = max(c.size()[0] for c in ics)
    mw, mh = m.size()
    place(main, m, 0, (2 * (ih + 30) - mh) / 2 if 2 * (ih + 30) > mh else 0)
    gx = mw + 40
    for i, c in enumerate(ics):
        cx, cy = gx + (i % 2) * (iw + 40), (i // 2) * (ih + 30)
        main.text(cx + 6, cy + 9, "ABCD"[i], 16, col=BLUE)
        place(main, c, cx + 22, cy, iw, ih)
    svg = main.svg("mat plan and four structures labelled A to D")
    notes = []
    for i, (tag, v) in enumerate(pick):
        j = i if i < p else i + 1
        notes.append("%s %s" % ("ABCD"[j], {"turn": "is turned a quarter turn", "mirror": "is a mirror image (left and right swapped)",
                                          "move": "has a cube in a different stack", "add": "has an extra cube"}[tag]))
    e = ("Match each number to a stack, with the front at the bottom of the mat plan. Only %s has exactly these stacks. %s."
         % ("ABCD"[p], "; ".join(sorted(notes))))
    q = fig(svg) + "Which structure matches this mat plan? The red arrows show the front."
    return mcq_fixed(q, list("ABCD"), "ABCD"[p], e)


def set_match(rnd, used):
    its = []
    pos = Pos(rnd)
    sizes = [(3, 2), (2, 3), (3, 3), (2, 2), (3, 2), (2, 3)]
    i = 0
    while len(its) < 10:
        W, D = sizes[i % len(sizes)]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=4, n_hi=9)
        if skey(cols) in used or views3(cols) == views3(rot90(cols)):
            continue
        p = pos.next()
        try:
            q = match_q(rnd, cols, p)
        except AssertionError:
            pos.q.append(p)
            continue
        used.add(skey(cols))
        its.append(q)
    asks = ["front", "front", "front", "right", "right", "right"]
    while len(its) < 16:
        W, D = sizes[i % len(sizes)]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=5, n_hi=12)
        ask = asks[len(its) - 10]
        if skey(cols) in used or not pick_views(cols, ask, rnd) or vnorm(v_front(cols)) == vnorm(v_right(cols)):
            continue
        used.add(skey(cols))
        its.append(views_q(rnd, cols, ask, pos.next(), use_mat=True))
    while len(its) < 20:
        W, D = sizes[i % len(sizes)]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=4, n_hi=9)
        if skey(cols) in used:
            continue
        used.add(skey(cols))
        its.append(mat_match_q(rnd, cols, pos.next()))
    return {"title": "Which object matches the views?", "items": its}


# ------------------------------------------------------------ nets of prisms and pyramids
def box_net_cv(L, W, H, k, top_on=0, bot_on=0):
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cv = Canvas()
    for i in range(4):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL)
    cv.poly([(xs[top_on] * k, -W * k), ((xs[top_on] + L) * k, -W * k), ((xs[top_on] + L) * k, 0), (xs[top_on] * k, 0)], BASE)
    cv.poly([(xs[bot_on] * k, H * k), ((xs[bot_on] + L) * k, H * k), ((xs[bot_on] + L) * k, (H + W) * k), (xs[bot_on] * k, (H + W) * k)], BASE)
    return cv


def ngon_on_edge(x0, x1, n, up=True, y=0):
    """Regular n-gon standing on the edge (x0, y)-(x1, y), above it (up) or below it."""
    s = x1 - x0
    pts, p, h = [], (x0, 0.0), 0.0
    for _ in range(n):
        pts.append(p)
        p = (p[0] + s * math.cos(math.radians(h)), p[1] + s * math.sin(math.radians(h)))
        h += 360.0 / n
    return [(px, y - py if up else y + py) for px, py in pts]


def prism_net_cv(n, s, L, k, ends=(("top", 0), ("bot", 0)), rects=None):
    """Prism with a regular n-gon base (side s), length L: a strip of rectangles with the n-gons on its edges.
    n = 3 gives an equilateral triangular prism. rects < n or both ends on the same side gives a broken net."""
    rects = n if rects is None else rects
    cv = Canvas()
    for i in range(rects):
        cv.poly([(i * s * k, 0), ((i + 1) * s * k, 0), ((i + 1) * s * k, L * k), (i * s * k, L * k)], FILL)
    for side, i in ends:
        pts = ngon_on_edge(i * s, (i + 1) * s, n, up=(side == "top"), y=0 if side == "top" else L)
        cv.poly([(x * k, y * k) for x, y in pts], BASE)
    return cv


def right_tri_prism_cv(a, b, c, L, k):
    """Rectangles a, b, c wide; right triangle (legs a, b) on the b rectangle, top and bottom."""
    assert a * a + b * b == c * c
    xs = [0, a, a + b, a + b + c]
    cv = Canvas()
    for i in range(3):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, L * k), (xs[i] * k, L * k)], FILL)
    # triangle on the b edge: right angle at x = a; leg a goes up (it must meet rectangle a's edge when folded)
    cv.poly([(a * k, 0), ((a + b) * k, 0), (a * k, -a * k)], BASE)
    cv.poly([(a * k, L * k), ((a + b) * k, L * k), (a * k, (L + a) * k)], BASE)
    assert abs(math.hypot(b, a) - c) < 1e-9
    return cv


def pyramid_net_cv(n, s, l, k, sides=None):
    """Regular n-gon base (side s) with an isosceles triangle (height l) on each listed side."""
    R = s / (2 * math.sin(math.pi / n))
    base = [(R * math.cos(math.radians(90 + 180.0 / n + 360.0 * i / n)), R * math.sin(math.radians(90 + 180.0 / n + 360.0 * i / n)))
            for i in range(n)]
    cv = Canvas()
    cv.poly([(x * k, y * k) for x, y in base], BASE)
    sides = range(n) if sides is None else sides
    for i in sides:
        A, B = base[i], base[(i + 1) % n]
        M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
        L = math.hypot(M[0], M[1])
        apex = (M[0] + M[0] / L * l, M[1] + M[1] / L * l)
        cv.poly([(A[0] * k, A[1] * k), (B[0] * k, B[1] * k), (apex[0] * k, apex[1] * k)], FILL)
    return cv


def rect_pyramid_cv(L, W, H, k):
    """Rectangle L × W with triangles whose heights come from an apex H above the centre (all slant edges equal)."""
    hl = math.sqrt(H * H + (W / 2) ** 2)      # triangle on an L side
    hw = math.sqrt(H * H + (L / 2) ** 2)      # triangle on a W side
    e1 = math.sqrt(hl * hl + (L / 2) ** 2)
    e2 = math.sqrt(hw * hw + (W / 2) ** 2)
    assert abs(e1 - e2) < 1e-9                # the 4 slant edges are equal, so the triangles meet at one apex
    cv = Canvas()
    P = lambda x, y: (x * k, y * k)
    cv.poly([P(0, 0), P(L, 0), P(L, W), P(0, W)], BASE)
    cv.poly([P(0, 0), P(L, 0), P(L / 2, -hl)], FILL)
    cv.poly([P(0, W), P(L, W), P(L / 2, W + hl)], FILL)
    cv.poly([P(0, 0), P(0, W), P(-hw, W / 2)], FILL)
    cv.poly([P(L, 0), P(L, W), P(L + hw, W / 2)], FILL)
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


# cube nets (rolling test) ---------------------------------------------------
def rot_y(s):
    return ((0, 0, s), (0, 1, 0), (-s, 0, 0))


def rot_x(s):
    return ((1, 0, 0), (0, 0, -s), (0, s, 0))


def mat3(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def fold_cube(cells):
    cells = list(cells)
    I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    R = {cells[0]: I}
    todo = [cells[0]]
    while todo:
        c = todo.pop(0)
        for (dc, dr), M in [((1, 0), rot_y(1)), ((-1, 0), rot_y(-1)), ((0, 1), rot_x(-1)), ((0, -1), rot_x(1))]:
            n = (c[0] + dc, c[1] + dr)
            if n in cells and n not in R:
                R[n] = mat3(M, R[c])
                todo.append(n)
    assert len(R) == 6
    face = {c: tuple(-m[2][i] for i in range(3)) for c, m in R.items()}
    return face if len(set(face.values())) == 6 else None


def is_net(cells):
    return fold_cube(cells) is not None


def opp(cells, a):
    f = fold_cube(cells)
    return [c for c in cells if f[c] == tuple(-v for v in f[a])][0]


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
assert len(GOOD) == 11


def cdims(cells):
    return (max(c for c, r in cells) - min(c for c, r in cells) + 1, max(r for c, r in cells) - min(r for c, r in cells) + 1)


BAD_POOL = [b for b in BAD if max(cdims(b)) <= 4]


def orient(cells, rnd):
    opts = [s for s in _syms(cells) if cdims(s)[0] >= cdims(s)[1]]
    return list(rnd.choice(sorted(set(opts))))


def has_run(cells, n):
    s = set(cells)
    return any(all((c + i, r) in s for i in range(n)) or all((c, r + i) in s for i in range(n)) for c, r in cells)


def has_block(cells):
    s = set(cells)
    return any({(c + 1, r), (c, r + 1), (c + 1, r + 1)} <= s for c, r in cells)


def bad_reason(cells):
    if has_block(cells):
        return "it has a 2-by-2 block of squares, but only 3 faces of a cube meet at a corner"
    return "two of its squares fold onto the same face, so one face of the cube is left open"


def cells_cv(cells, k, letters=None):
    cv = Canvas()
    c0, r0 = min(c for c, r in cells), min(r for c, r in cells)
    for c, r in cells:
        x, y = (c - c0) * k, (r - r0) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], FILL)
    if letters:
        for (c, r), t in letters.items():
            cv.text((c - c0 + 0.5) * k, (r - r0 + 0.5) * k, t, 18, col=GREEN)
    return cv


def four_row(cvs, label):
    return row_svg(cvs, list("ABCD"), label, gap=26)


NET_E = {
    CUBE: "6 equal squares fold into a cube.",
    RP: "6 rectangles in 3 matching pairs fold into a rectangular prism.",
    TP: "2 triangles (the bases) and 3 rectangles fold into a triangular prism.",
    SP: "1 square base and 4 triangles that meet at one point fold into a square-based pyramid.",
    TPY: "4 triangles fold into a triangular pyramid: one is the base and the other 3 meet at a point.",
    PP: "2 pentagons (the bases) and 5 rectangles fold into a pentagonal prism.",
    HP: "2 hexagons (the bases) and 6 rectangles fold into a hexagonal prism.",
    PPY: "1 pentagon base and 5 triangles that meet at one point fold into a pentagonal pyramid.",
    HPY: "1 hexagon base and 6 triangles that meet at one point fold into a hexagonal pyramid.",
    RPY: "1 rectangle base and 4 triangles that meet at one point fold into a rectangular pyramid.",
}
WRONG_NAME = {RP: [CUBE, TP, SP], TP: [TPY, SP, RP], SP: [TP, CUBE, TPY], TPY: [SP, TP, "triangular prism with no ends"],
              PP: [PPY, HP, TP], HP: [HPY, PP, RP], PPY: [PP, HPY, SP], HPY: [HP, PPY, SP], RPY: [SP, RP, TP]}


def set_poly_nets(rnd):
    its = []
    pos = Pos(rnd)
    ASK = ["Which 3D object does this net fold into?", "What object can be made from this net?",
           "This net is folded up. Which object does it make?"]
    nets = [
        (box_net_cv(4, 2, 3, 20, 2, 0), RP, " Opposite faces are the same size."),
        (right_tri_prism_cv(3, 4, 5, 3, 20), TP, " The bases are right triangles here; a prism’s bases do not have to be equilateral."),
        (pyramid_net_cv(4, 2, 2.2, 24), SP, ""),
        (tetra_cv(56), TPY, ""),
        (prism_net_cv(5, 1.2, 2.4, 24, (("top", 1), ("bot", 3))), PP, ""),
        (pyramid_net_cv(6, 1.2, 2.0, 24), HPY, " A pyramid is named after its base."),
        (rect_pyramid_cv(3, 2, 2, 22), RPY, " The base is a rectangle that is not a square, so the triangles on the long sides and short sides differ."),
        (pyramid_net_cv(5, 1.4, 2.0, 24), PPY, ""),
        (prism_net_cv(6, 1.0, 2.2, 22, (("top", 2), ("bot", 2))), HP, ""),
    ]
    for i, (cv, obj, extra) in enumerate(nets):
        its.append(mcq(fig(cv.svg("net of a 3D object")) + ASK[i % 3], obj, WRONG_NAME[obj], NET_E[obj] + extra))
    # A-D: which net folds into ...
    p = pos.next()
    cvs = [pyramid_net_cv(5, 1.2, 1.8, 15), prism_net_cv(5, 1.2, 2.2, 15, rects=4),
           prism_net_cv(5, 1.2, 2.2, 15, (("top", 0), ("top", 3)))]
    cvs.insert(p, prism_net_cv(5, 1.2, 2.2, 15, (("top", 1), ("bot", 3))))
    its.append(mcq_fixed(fig(four_row(cvs, "four nets labelled A to D")) + "Which net folds into a pentagonal prism?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 2 pentagons on opposite edges of a strip of 5 rectangles. One wrong net is a pentagonal pyramid, one has "
                         "only 4 rectangles (it cannot close), and one has both pentagons on the same edge, so they fold onto the same end."
                         % "ABCD"[p]))
    p = pos.next()
    cvs = [prism_net_cv(3, 2, 2.4, 15), pyramid_net_cv(4, 2, 2.2, 13, sides=(0, 1, 2)), tetra_cv(36)]
    cvs.insert(p, pyramid_net_cv(4, 2, 2.2, 13))
    its.append(mcq_fixed(fig(four_row(cvs, "four nets labelled A to D")) + "Which net folds into a square-based pyramid?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 1 square and 4 triangles, one on each side of the square. One wrong net has only 3 triangles, "
                         "so one side stays open. The others make a triangular prism and a triangular pyramid." % "ABCD"[p]))
    p = pos.next()
    cvs = [prism_net_cv(6, 1, 2, 16, rects=5), pyramid_net_cv(6, 1, 1.8, 16), prism_net_cv(5, 1.2, 2, 14, (("top", 1), ("bot", 3)))]
    cvs.insert(p, prism_net_cv(6, 1, 2, 16, (("top", 1), ("bot", 4))))
    its.append(mcq_fixed(fig(four_row(cvs, "four nets labelled A to D")) + "Which net folds into a hexagonal prism?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 2 hexagons and 6 rectangles. One wrong net has only 5 rectangles, one is a hexagonal pyramid, "
                         "and one has pentagons, so it makes a pentagonal prism." % "ABCD"[p]))
    # cube nets
    good, bad = GOOD[:], BAD_POOL[:]
    rnd.shuffle(good)
    rnd.shuffle(bad)
    p = pos.next()
    cells = [orient(b, rnd) for b in bad[:3]]
    cells.insert(p, orient(good[0], rnd))
    for x, c in enumerate(cells):
        assert is_net(c) == (x == p)
    its.append(mcq_fixed(fig(four_row([cells_cv(c, 17) for c in cells], "four patterns labelled A to D")) +
                         "Which pattern is a net of a cube?", list("ABCD"), "ABCD"[p],
                         "%s folds into a cube with no gaps and no overlaps. Each of the others has two squares that fold onto the "
                         "same face, so one face is left open." % "ABCD"[p]))
    # opposite face
    cells = orient(good[1], rnd)
    letters = list("ABCDEF")
    rnd.shuffle(letters)
    lab = dict(zip(cells, letters))
    a = sorted(cells)[0]
    b = opp(cells, a)
    touch = [c for c in cells if abs(c[0] - a[0]) + abs(c[1] - a[1]) == 1]
    far = [c for c in cells if c not in touch and c not in (a, b)]
    its.append(mcq(fig(cells_cv(cells, 34, lab).svg("net of a cube with faces A to F")) +
                   "This net is folded into a cube. Which face is opposite face %s?" % lab[a], "face " + lab[b],
                   ["face " + lab[c] for c in far + touch],
                   "Fold the net one square at a time: face %s lands opposite face %s. Faces that touch %s in the net are next to it "
                   "on the cube, never opposite." % (lab[b], lab[a], lab[a])))
    # counts
    its.append(mcq("How many faces does the net of a hexagonal prism have?", 8, [6, 12, 7],
                   "2 hexagons (the bases) + 6 rectangles (one for each side of the hexagon) = 8 faces."))
    its.append(mcq("How many triangles are in the net of an octagonal pyramid?", 8, [9, 16, 4],
                   "An octagon has 8 sides, and there is one triangle on each side. The net has 8 triangles and 1 octagon (9 faces in all)."))
    its.append(mcq("A net has 2 octagons and some rectangles. How many rectangles does it need to fold into a prism?", 8, [2, 6, 10],
                   "A prism has one rectangle for each side of its base. An octagon has 8 sides, so the net needs 8 rectangles."))
    its.append(mcq("A net has 1 hexagon and 6 triangles. Which object does it make?", HPY, [HP, PPY, "triangular prism"],
                   NET_E[HPY]))
    its.append(mcq("A triangular prism is 10 cm long. Its bases are right triangles with sides 6 cm, 8 cm and 10 cm. "
                   "What is the size of the largest rectangle in its net?", "10 cm by 10 cm", ["8 cm by 10 cm", "6 cm by 8 cm", "6 cm by 10 cm"],
                   "Each rectangle is as wide as one side of the triangle and as long as the prism. The longest side is 10 cm, so the "
                   "largest rectangle is 10 cm by 10 cm."))
    its.append(mcq("A box is a rectangular prism 30 cm long, 20 cm wide and 10 cm tall. How many faces in its net measure 30 cm by 10 cm?",
                   2, [1, 4, 3], "The front and the back are both 30 cm by 10 cm. Opposite faces of a rectangular prism match, so faces come in pairs."))
    assert len(its) == 20, len(its)
    return {"title": "Nets of prisms and pyramids", "items": its}


# ------------------------------------------------------------ set 4: nets of cylinders
def cyl_net_cv(r, h, k, mode="ok", labels=None):
    """Rectangle 2πr long (the curved surface) and h tall; the circles touch the edges that are 2πr long.
    modes: ok | same | one | diam (rectangle only as long as the diameter) | tall (h > 2πr: circles on the side edges)."""
    C = 2 * math.pi * r
    cv = Canvas()
    if mode == "tall":                                   # 2πr < h: the circles sit on the short (top and bottom) edges
        assert C < h
        cv.poly([(0, 0), (C * k, 0), (C * k, h * k), (0, h * k)], FILL)
        for c in [(C * k / 2, -r * k), (C * k / 2, (h + r) * k)]:
            cv.circle(c, r * k, BASE, 2)
        return cv
    W = 2 * r if mode == "diam" else C
    cv.poly([(0, 0), (W * k, 0), (W * k, h * k), (0, h * k)], FILL)
    if mode in ("ok", "diam"):
        cs = [(W * 0.3 * k, -r * k), (W * 0.62 * k, (h + r) * k)] if mode == "ok" else [(W * 0.5 * k, -r * k), (W * 0.5 * k, (h + r) * k)]
    elif mode == "same":
        cs = [(W * 0.25 * k, -r * k), (W * 0.75 * k, -r * k)]
    else:
        cs = [(W * 0.5 * k, -r * k)]
    for c in cs:
        cv.circle(c, r * k, BASE, 2)
    if labels:
        hl, wl, rl = labels
        if hl:
            cv.text(W * k + 8, h * k / 2, hl, 15, anchor="start")
        if wl:
            cv.text(W * k * 0.8, h * k / 2, wl, 15)
        if rl:
            cx, cy = cs[0]
            cv.line((cx, cy), (cx - r * k, cy), sw=1.8, col=RED)
            cv.text(cx - r * k - 8, cy - r * k * 0.55, rl, 15, anchor="end", col=RED)
    return cv


def cone_net_cv(r, s, k):
    th = 360.0 * r / s
    S = s * k
    arc = [(S * math.cos(math.radians(90 - th / 2 + th * i / 48)), S * math.sin(math.radians(90 - th / 2 + th * i / 48)))
           for i in range(49)]
    cv = Canvas()
    cv.poly([(0, 0)] + arc, FILL)
    cv.circle((0, S + r * k), r * k, BASE, 2)
    return cv


def set_cyl(rnd, P):
    its = []
    pos = Pos(rnd)
    p = pos.next()
    cvs = [cyl_net_cv(0.45, 1.3, 20, "one"), cyl_net_cv(0.45, 1.3, 20, "same"), cone_net_cv(0.6, 1.5, 24)]
    cvs.insert(p, cyl_net_cv(0.45, 1.3, 20))
    its.append(mcq_fixed(fig(four_row(cvs, "four nets labelled A to D")) + "Which net folds into a closed cylinder?",
                         list("ABCD"), "ABCD"[p],
                         "%s has a rectangle with one circle on each long edge, so the circles close both ends of the tube. "
                         "One wrong net has only 1 circle, one has both circles on the same edge, and one is the net of a cone." % "ABCD"[p]))
    p = pos.next()
    cvs = [cyl_net_cv(0.5, 1.2, 20, "diam"), prism_net_cv(3, 1.1, 1.6, 20), cyl_net_cv(0.4, 1.2, 20, "one")]
    cvs.insert(p, cyl_net_cv(0.4, 1.2, 20))
    its.append(mcq_fixed(fig(four_row(cvs, "four nets labelled A to D")) + "Which net folds into a closed cylinder?",
                         list("ABCD"), "ABCD"[p],
                         "%s is right: the rectangle is as long as the distance around each circle. In one wrong net the rectangle is only "
                         "as long as the diameter, so it is far too short to wrap around the circles. The others are a triangular prism "
                         "and a net with only 1 circle." % "ABCD"[p]))
    its.append(mcq(fig(cyl_net_cv(0.6, 1.6, 22).svg("net of a 3D object")) + "Which 3D object does this net fold into?", CYL,
                   [CONE, RP, "sphere"], "The rectangle rolls into a tube (the curved surface) and the 2 circles close the ends: a cylinder."))
    its.append(mcq("Which part of a cylinder’s net becomes the curved surface?", "the rectangle",
                   ["the two circles", "one of the circles", "the edges of the circles"],
                   "The rectangle rolls up into a tube. The 2 circles are the flat top and bottom."))
    its.append(mcq("In the net of a cylinder, the length of the rectangle that touches the circles is equal to …",
                   "the circumference of the circle", ["the diameter of the circle", "the radius of the circle", "the height of the cylinder"],
                   "That edge wraps once around each circle, so it is as long as the circumference: 2 × π × r."))
    # rectangle length from the radius
    for r, h in [(3, 10), (5, 12), (4, 9), (6, 15), (9, 20)]:
        r = Dm(str(r))
        C = 2 * PI * r
        wrong = [PI * r, 2 * PI * 2 * r, PI * r * r, 2 * r]
        wrong = [w for w in wrong if w != C]
        if r in (Dm(3), Dm(4)):
            q = (fig(cyl_net_cv(float(r) / 4, h / 4, 22, labels=("%d cm" % h, "", "%s cm" % N(r)))
                     .svg("net of a cylinder with the radius and height labelled")) +
                 "This is the net of a cylinder with radius %s cm and height %d cm. How long is the rectangle? (Use π ≈ 3.14.)" % (N(r), h))
        else:
            q = ("A cylinder has a radius of %s cm and a height of %d cm. How long is the rectangle in its net? (Use π ≈ 3.14.)" % (N(r), h))
        its.append(mcq(q, N(C) + " cm", [N(w) + " cm" for w in wrong],
                       "The rectangle is as long as the circumference: 2 × π × r = 2 × 3.14 × %s = %s cm. "
                       "Do not use πr (half the circle) or the diameter in place of r." % (N(r), N(C))))
    # from the diameter
    for d in (10, 12, 16):
        d = Dm(d)
        C = PI * d
        its.append(mcq("A can has a diameter of %s cm. Its paper label wraps around the can once with no overlap. "
                       "How long is the label? (Use π ≈ 3.14.)" % N(d),
                       N(C) + " cm", [N(2 * PI * d) + " cm", N(PI * d / 2) + " cm", N(PI * (d / 2) ** 2) + " cm"],
                       "Circumference = π × d = 3.14 × %s = %s cm. 2 × π × d uses the diameter as if it were the radius." % (N(d), N(C))))
    # height from the net
    r, h = Dm(3), Dm(12)
    C = 2 * PI * r
    its.append(mcq("The rectangle in a cylinder’s net is %s cm by %s cm. Each circle has a radius of 3 cm. How tall is the cylinder?"
                   % (N(h), N(C)), "12 cm", [N(C) + " cm", "6 cm", "3 cm"],
                   "The edge that wraps around the circle is 2 × 3.14 × 3 = %s cm long. The other edge, 12 cm, is the height." % N(C)))
    # radius from the rectangle
    for L in (Dm("31.4"), Dm("43.96")):
        d = L / PI
        r = d / 2
        its.append(mcq("The rectangle in a cylinder’s net is %s cm long, and that edge wraps around the circles. "
                       "What is the radius of each circle? (Use π ≈ 3.14.)" % N(L),
                       N(r) + " cm", [N(d) + " cm", N(L / 2) + " cm", N(r / 2) + " cm"],
                       "Circumference = π × d, so d = %s ÷ 3.14 = %s cm. The radius is half of that: %s cm." % (N(L), N(d), N(r))))
    assert PI * 5 == Dm("15.7")
    its.append(mcq("The circles in a cylinder’s net have a diameter of 5 cm. The rectangle is 12 cm by 15.7 cm. "
                   "What are the radius and the height of the cylinder?", "r = 2.5 cm, h = 12 cm",
                   ["r = 5 cm, h = 12 cm", "r = 2.5 cm, h = 15.7 cm", "r = 5 cm, h = 15.7 cm"],
                   "The radius is half the diameter: 5 ÷ 2 = 2.5 cm. The 15.7 cm edge wraps around the circle (3.14 × 5 = 15.7), "
                   "so the other edge, 12 cm, is the height."))
    # curved surface
    its.append(mcq("A cylinder has a radius of 5 cm and a height of 10 cm. What is the area of the rectangle in its net? (Use π ≈ 3.14.)",
                   "314 cm²", ["785 cm²", "157 cm²", "31.4 cm²"],
                   "The rectangle is 2 × 3.14 × 5 = 31.4 cm long and 10 cm tall: 31.4 × 10 = 314 cm². "
                   "785 is π × r² × h (the volume), and 157 uses πr instead of 2πr."))
    its.append(mcq(fig(cyl_net_cv(0.35, 3.0, 26, "tall").svg("net of a tall thin cylinder")) +
                   "This is the net of a tall, thin tube. Why do the circles touch the short edges of the rectangle?",
                   "The short edges are as long as the circumference",
                   ["The short edges are as long as the diameter", "Circles always go on the short edges", "The long edges are the bottom"],
                   "The circles always touch the edges that wrap around them, and those edges are as long as the circumference. "
                   "For a tall, thin tube, the circumference is shorter than the height, so these are the short edges."))
    n, he, his = P.next()
    its.append(mcq("%s makes a model of a rain barrel shaped like a cylinder. The circles in %s net have a radius of 10 cm. "
                   "How long must the rectangle be? (Use π ≈ 3.14.)" % (n, his), "62.8 cm", ["31.4 cm", "125.6 cm", "314 cm"],
                   "The rectangle wraps around the circles: 2 × 3.14 × 10 = 62.8 cm. 314 is π × r², the area of a circle."))
    assert len(its) == 20, len(its)
    return {"title": "Nets of cylinders", "items": its}


# ------------------------------------------------------------ set 5: count cubes from views
def all_fits(top, front, right):
    """All height maps with this top view (cells), front heights and right side heights."""
    cells = sorted(top)
    rngs = [range(1, min(front[x], right[z]) + 1) for x, z in cells]
    out = []
    for hs in itertools.product(*rngs):
        cols = dict(zip(cells, hs))
        if heights_front(cols) == list(front) and heights_right(cols) == list(right):
            out.append(cols)
    return out


def three_views_svg(cols, label="top, front and right side views"):
    main = Canvas()
    w3 = views3(cols)
    vcs = [view_cv(w3[0], 22), view_cv(w3[1], 22), view_cv(w3[2], 22)]
    vh = max(c.size()[1] for c in vcs)
    x = 0
    for c, cap in zip(vcs, ["Top", "Front", "Right side"]):
        w = max(c.size()[0], tw(cap, 15) + 4)
        place(main, c, x, 0, w, vh)
        main.text(x + w / 2, vh + 14, cap, 15, col=INK)
        x += w + 36
    return main.svg(label)


def count_e(cols):
    hs = [cols[c] for c in sorted(cols)]
    return " + ".join(str(h) for h in hs) + " = %d" % sum(hs)


def set_count(rnd, P, used):
    its = []
    sizes = [(3, 3), (3, 2), (2, 3), (3, 3)]
    i = 0
    # count from the picture (some cubes are hidden)
    while len(its) < 5:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=7, n_hi=13, hmin_top=3)
        n, vis = sum(cols.values()), visible_cubes(cols)
        if skey(cols) in used or vis == n:
            continue
        used.add(skey(cols))
        its.append(mcq(fig(iso_svg(cols)) + "How many cubes are in this structure? Every stack stands on the table.", n,
                       [vis, len(cols), sum(heights_front(cols)), n + 1],
                       "Count stack by stack, including the cubes hidden underneath and behind: %s. "
                       "Counting only the cubes you can see gives %d." % (count_e(cols), vis)))
    # mat plans
    while len(its) < 7:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=8, n_hi=16)
        if skey(cols) in used:
            continue
        used.add(skey(cols))
        n = sum(cols.values())
        its.append(mcq(fig(mat_cv(cols).svg("mat plan")) + "The mat plan shows how many cubes are in each stack. How many cubes are there in all?",
                       n, [len(cols), sum(heights_front(cols)), sum(heights_front(cols)) + sum(heights_right(cols)), sum(heights_right(cols)),
                          max(cols.values()) * len(cols)],
                       "Add the numbers on the mat plan: %s. %d is only the number of stacks." % (count_e(cols), len(cols))))
    # three views -> exact count (only one structure fits) and greatest number
    exact = greatest = 0
    while exact < 3 or greatest < 2:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=5, n_hi=12)
        if skey(cols) in used:
            continue
        fits = all_fits(v_top(cols), heights_front(cols), heights_right(cols))
        assert cols in fits
        ns = sorted(sum(f.values()) for f in fits)
        fs, rs, tc = sum(heights_front(cols)), sum(heights_right(cols)), len(cols)
        if len(fits) == 1 and exact < 3:
            exact += 1
            its.append(mcq(fig(three_views_svg(cols)) + "These are the top, front and right side views of a structure of cubes. "
                           "How many cubes are in the structure?", ns[0], [fs + rs, tc, fs, rs, ns[0] + 1],
                           "The top view shows %d stacks. Use the front and side views to find each stack’s height: %s. "
                           "Adding the squares in the front and side views (%d + %d) counts some cubes twice." % (tc, count_e(cols), fs, rs)))
            used.add(skey(cols))
        elif len(fits) > 1 and ns[-1] != ns[0] and greatest < 2:
            greatest += 1
            big = [f for f in fits if sum(f.values()) == ns[-1]][0]
            its.append(mcq(fig(three_views_svg(cols)) + "These are the top, front and right side views of a structure of cubes. "
                           "What is the greatest number of cubes it could have?", ns[-1], [ns[0], fs + rs, tc * max(heights_front(cols)), fs, rs],
                           "Make each stack as tall as both the front view (its column) and the side view (its row) allow: %s. "
                           "The least possible is %d, so the views alone do not fix the number of cubes." % (count_e(big), ns[0])))
            used.add(skey(cols))
    # word problems
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=8, n_hi=13, hmin_top=3)
        if skey(cols) not in used and visible_cubes(cols) < sum(cols.values()):
            break
    used.add(skey(cols))
    n, vis = sum(cols.values()), visible_cubes(cols)
    its.append(mcq(fig(iso_svg(cols)) + "%s has 25 linking cubes. %s builds this structure. How many cubes does %s have left?"
                   % (n_, he.capitalize(), he), 25 - n, [25 - vis, 25 - len(cols), n],
                   "The structure has %s cubes (count the hidden ones too). 25 − %d = %d." % (count_e(cols).split(" = ")[0] + " = %d" % n, n, 25 - n)))
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=7, n_hi=14)
        if skey(cols) not in used and len(cols) == W * D and max(cols.values()) == 3 and min(cols.values()) < 3:
            break
    used.add(skey(cols))
    n = sum(cols.values())
    full = W * D * 3
    its.append(mcq(fig(mat_cv(cols).svg("mat plan")) +
                   "%s wants every stack in this mat plan to be 3 cubes tall, to make a solid rectangular prism. How many more cubes does %s need?"
                   % (n_, he), full - n, [n, full, full - len(cols), W * D, full - n + 1],
                   "A solid prism %d by %d by 3 has %d × %d × 3 = %d cubes. %s already has %d: %d − %d = %d."
                   % (W, D, W, D, full, n_, n, full, n, full - n)))
    its.append(mcq("Shipping containers at the Port of Vancouver are stacked in a solid block. The front view is 5 containers wide and "
                   "3 high. The right side view is 4 containers wide and 3 high. The top view is a full 5 by 4 rectangle. "
                   "How many containers are in the block?", 60, [27, 20, 12],
                   "The top view shows 5 × 4 = 20 stacks, and every stack is 3 high: 20 × 3 = 60. Adding the views (15 + 12) "
                   "counts the outside only."))
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=6, n_hi=12)
        if skey(cols) not in used:
            break
    used.add(skey(cols))
    n = sum(cols.values())
    its.append(mcq(fig(mat_cv(cols).svg("mat plan")) + "%s builds this structure from 1 cm cubes. What is its volume?" % n_,
                   "%d cm³" % n, ["%d cm²" % n, "%d cm³" % len(cols), "%d cm³" % sum(heights_front(cols))],
                   "Each 1 cm cube has a volume of 1 cm³. There are %s cubes, so the volume is %d cm³ (cubic units, not cm²)."
                   % (count_e(cols).split(" = ")[0] + " = %d" % n, n)))
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=6, n_hi=11)
        fsq = len(v_front(cols))
        if skey(cols) not in used and len({fsq, sum(cols.values()), len(v_right(cols)), len(cols)}) == 4:
            break
    used.add(skey(cols))
    its.append(mcq(fig(iso_svg(cols)) + "%s draws the front view of this structure on grid paper, one square for each cube face. "
                   "How many squares does %s shade?" % (n_, he), fsq, [sum(cols.values()), len(v_right(cols)), len(cols)],
                   "From the front, the tallest stacks are %s cubes, so the view has %s = %d squares. Cubes behind the front ones "
                   "are hidden and do not add squares." % (words(heights_front(cols)), " + ".join(map(str, heights_front(cols))), fsq)))
    n_, he, his = P.next()
    top = [(x, z) for x in range(3) for z in range(2)]
    fits = all_fits(top, [2, 2, 2], [2, 2])
    ns = sorted(sum(f.values()) for f in fits)
    assert ns[-1] == 12 and ns[0] == 9
    its.append(mcq("%s builds a structure for a Kelowna art fair. Its top view is a full 3 by 2 rectangle. The front view is 3 cubes wide "
                   "and 2 tall, and the right side view is 2 cubes wide and 2 tall. What is the greatest number of cubes %s could use?"
                   % (n_, he), 12, [9, 10, 6],
                   "Every stack can be 2 cubes tall: 6 stacks × 2 = 12. The least is 9 (only 3 stacks need to be 2 tall). "
                   "10 adds the squares in the front and side views."))
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=6, n_hi=12)
        if skey(cols) in used:
            continue
        fits = all_fits(v_top(cols), heights_front(cols), heights_right(cols))
        ns = sorted(sum(f.values()) for f in fits)
        if ns[0] != ns[-1]:
            break
    used.add(skey(cols))
    small = [f for f in fits if sum(f.values()) == ns[0]][0]
    its.append(mcq(fig(three_views_svg(cols)) + "A sculpture in Victoria is made of 1 m cubes. These are its top, front and right side views. "
                   "What is the least number of cubes it could have?", ns[0], [ns[-1], sum(heights_front(cols)) + sum(heights_right(cols)), len(cols)],
                   "Each stack in the top view needs at least 1 cube, and each column and row must reach the height in the front and "
                   "side views. The fewest that works is %s. The greatest is %d." % (count_e(small), ns[-1])))
    n_, he, his = P.next()
    while True:
        W, D = sizes[i % 4]
        i += 1
        cols = rand_struct(rnd, W, D, n_lo=6, n_hi=12)
        if skey(cols) not in used:
            break
    used.add(skey(cols))
    n = sum(cols.values())
    its.append(mcq(fig(mat_cv(cols).svg("mat plan")) + "%s builds a model of a Surrey apartment block from this mat plan. Each cube is one "
                   "apartment. A cube on top of another is one floor higher. How many apartments are on the ground floor?" % n_,
                   len(cols), [n, max(cols.values()), sum(heights_front(cols))],
                   "Every stack has exactly 1 cube on the ground floor, so count the stacks (the squares in the mat plan): %d. "
                   "%d is the number of apartments in the whole model." % (len(cols), n)))
    assert len(its) == 20, len(its)
    return {"title": "Count the cubes: views and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON = {(0, 0): 2, (1, 0): 2, (2, 0): 1, (0, 1): 3, (1, 1): 2}
assert valid(LESSON)
assert heights_front(LESSON) == [3, 2, 1] and heights_right(LESSON) == [2, 3]


def lesson_views_svg():
    main = Canvas()
    iso = iso_cv(LESSON, 24)
    w3 = views3(LESSON)
    vcs = [view_cv(w3[0], 22), view_cv(w3[1], 22), view_cv(w3[2], 22)]
    iw, ih = iso.size()
    place(main, iso, 0, 0)
    x = iw + 40
    vh = max(c.size()[1] for c in vcs)
    for c, cap in zip(vcs, ["Top", "Front", "Right side"]):
        w = max(c.size()[0], tw(cap, 15) + 4)
        place(main, c, x, (ih - vh) / 2, w, vh)
        main.text(x + w / 2, (ih + vh) / 2 + 16, cap, 15, col=INK)
        x += w + 34
    return main.svg("a structure of cubes and its top, front and right side views")


def body_html():
    nets = row_svg([prism_net_cv(3, 2, 2.6, 16), pyramid_net_cv(4, 2, 2.2, 15), prism_net_cv(5, 1.2, 2.4, 16, (("top", 1), ("bot", 3))),
                    cyl_net_cv(0.5, 1.3, 22)],
                   [TP, SP, PP, CYL], "nets of a triangular prism, a square-based pyramid, a pentagonal prism and a cylinder",
                   gap=30, fs=14, col=INK)
    mat = mat_cv(LESSON, 30).svg("mat plan of the same structure")
    return (
        "<h2>Top, front and side views</h2>"
        "<p>A <b>view</b> is what you see when you look straight at an object from one side. Each cube face you see becomes one square.</p>"
        "<ul><li><b>Front view</b>: look from the front. Draw the tallest stack in each column, left to right.</li>"
        "<li><b>Right side view</b>: look from the right. The front of the object is on your <b>left</b>.</li>"
        "<li><b>Top view</b>: look down from above. Each stack is one square, and the front is at the bottom.</li></ul>"
        "<figure class='sn-fig'>" + lesson_views_svg() +
        "<figcaption>The red arrow shows the front. Front view: stacks of 3, 2 and 1. Right side view (front on the left): 2, then 3. "
        "Top view: 5 squares, one for each stack.</figcaption></figure>" +
        ex("Example 1", "How many cubes are in the structure above?",
           "Count stack by stack, including hidden cubes: 2 + 3 + 2 + 2 + 1.", "10 cubes") +
        "<h2>Mat plans</h2>"
        "<p>A <b>mat plan</b> is a top view with a number in each square: the number of cubes in that stack. "
        "Add the numbers to count the cubes. The largest number in each column gives the front view.</p>"
        "<figure class='sn-fig'>" + mat +
        "<figcaption>Mat plan of the same structure. 2 + 3 + 2 + 2 + 1 = 10 cubes. Column by column, the largest numbers are 3, 2 and 1: "
        "the front view.</figcaption></figure>"
        "<p>Three views do not always fix the number of cubes. Find the <b>greatest</b> number by making each stack as tall as both "
        "its column (front view) and its row (side view) allow.</p>"
        "<h2>Nets of prisms, pyramids and cylinders</h2>"
        "<p>A <b>net</b> is a flat pattern that folds into a 3D object. A <b>prism</b> has 2 matching bases joined by rectangles, "
        "one rectangle for each side of the base. A <b>pyramid</b> has 1 base and a triangle on each side. A <b>cylinder</b> has "
        "2 circles and a rectangle.</p>"
        "<figure class='sn-fig'>" + nets +
        "<figcaption>The two bases of a prism go on opposite edges of the strip of rectangles. If both were on the same edge, they "
        "would fold onto the same end.</figcaption></figure>"
        "<p>The rectangle in a cylinder’s net wraps once around each circle, so its length is the <b>circumference</b>: "
        "2 × π × r.</p>" +
        ex("Example 2", "A cylinder has a radius of 4 cm and a height of 10 cm. What are the dimensions of the rectangle in its net? (Use π ≈ 3.14.)",
           "Length = 2 × 3.14 × 4 = 25.12 cm. The width is the height of the cylinder.", "25.12 cm by 10 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up the front view and the side view", "Find the red arrow (the front) first. The side view is seen from the right"],
            ["Drawing the right side view backwards", "From the right, the front of the object is on your left"],
            ["Drawing a cube for every cube in the front view", "Draw only the tallest stack in each column; cubes behind are hidden"],
            ["Counting only the cubes you can see", "Count each stack from the bottom, including hidden cubes"],
            ["Putting both bases of a prism on the same edge of the net", "Put one base on each long edge of the strip of rectangles"],
            ["Making a cylinder’s rectangle as long as the diameter", "Its length is the circumference: 2 × π × r"],
        ])
    )


FAQ = [
    {"q": "What are top, front and side views in Grade 8 math?",
     "a": "They are 2D drawings of a 3D object seen from straight above, straight in front and from the right side. Each view shows every cube face you can see from that direction as one square."},
    {"q": "Are views and nets in the BC Grade 8 math curriculum?",
     "a": "Yes. “Construction, views, and nets of 3D objects” is a Grade 8 content standard in Geometry and measurement in the BC Mathematics Curriculum."},
    {"q": "What does the net of a cylinder look like?",
     "a": "It is a rectangle with a circle on each of two opposite edges. The rectangle’s length is the circle’s circumference (2 × π × r) and its width is the height of the cylinder."},
    {"q": "How do you count the cubes from a mat plan?",
     "a": "A mat plan is a top view with the number of cubes in each stack written in its square. Add all the numbers to get the total number of cubes."},
]


def balance(sets, rnd):
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(58811)
    P = People(rnd)
    used = {skey(LESSON)}
    sets = [set_views(rnd, used), set_match(rnd, used), set_poly_nets(rnd), set_cyl(rnd, P), set_count(rnd, P, used)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "views-and-nets", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Views and Nets of 3D Objects",
        "seo_title": "Grade 8 Views and Nets Worksheets: Top, Front and Side Views, Nets of Prisms and Cylinders (Free, Answer Key, BC Curriculum)",
        "short_title": "Views and nets",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 8: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Construction, views, and nets of 3D objects",
        "meta_desc": "Free Grade 8 math worksheets on views and nets for the BC curriculum: top, front and side views of cube structures, matching objects to their views and mat plans, nets of prisms, pyramids and cylinders, and counting cubes from views. 100 questions with an answer key.",
        "key_big": "A view shows an object from one direction; a net is the flat pattern that folds into it.",
        "key_sub": "Front view: the tallest stack in each column. Right side view: the front of the object is on the left. Top view: one square per stack, front at the bottom. A cylinder’s net is a rectangle 2 × π × r long with a circle on each long edge.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(structure of cubes and four|mat plan and four|top, front and right side views and four|four [a-z]+ labelled A to D|top, front and right side views')")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
