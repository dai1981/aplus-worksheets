# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Composite area and volume (Ontario Curriculum 2020, Spatial Sense, E2.3)
  python3 tools/gen_caon_math_g8_composite.py
Perimeter and area of composite shapes (rectangles, triangles, semicircles), volume and surface area of
composite prisms and cylinders, and word problems (running track, pool, house with a roof).
pi is always 3.14 (every question that needs it says so). Every answer and every wrong choice is worked out
with decimal.Decimal from a named student mistake: counting a shared side, a full circle for a semicircle,
the diameter used as r, forgetting the 1/2 for a triangle, the outer box instead of the composite shape,
adding a touching face to the surface area, and slipping when changing units.
Canadian English, metric units, SI number style (no-break space in numbers of 5 or more digits).
Pictures are drawn to the data; labels never touch each other, and in the flat shapes no line runs through a label.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)
PI = Dm("3.14")
NB = " "
USE = " Use π ≈ 3.14."
HALF = Dm("0.5")


# ------------------------------------------------------------ numbers
def N(x):
    """Decimal text without trailing zeros; 5+ digit whole parts get no-break spaces (72 000)."""
    d = Dm(str(x))
    s = format(d.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    ip, _, fp = s.partition(".")
    if len(ip) >= 5:
        g = []
        while ip:
            g.insert(0, ip[-3:])
            ip = ip[:-3]
        ip = NB.join(g)
    assert Dm(ip.replace(NB, "") + ("." + fp if fp else "")) == d
    return ip + ("." + fp if fp else "")


def U(x, u):
    return "%s %s" % (N(x), u)


def money(x):
    return "$%.2f" % Dm(x)


UNIT = {"cm³": ("v", 1), "mL": ("v", 1), "L": ("v", 1000), "m³": ("v", 1000000),
        "cm²": ("a", 1), "m²": ("a", 10000), "cm": ("l", 1), "m": ("l", 100), "mm": ("l", Dm("0.1"))}
NUM = re.compile("^([\\d ]+(?:\\.\\d+)?) (.+)$")


def val(c):
    """(kind, value) of a choice like '72 000 cm³', '$608.40' or '6 laps'; None if it is not one amount."""
    if c.startswith("$"):
        return ("$", Dm(c[1:]))
    m = NUM.match(c)
    if not m:
        return None
    v = Dm(m.group(1).replace(NB, ""))
    if m.group(2) in UNIT:
        k, f = UNIT[m.group(2)]
        return (k, v * f)
    return (m.group(2), v)


def mcq(q, correct, cands, e):
    """correct + 3 distractors (the first 3 that are new). No two choices may be the same amount."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        v = val(c)
        if v is not None and v[1] <= 0:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = [correct] + pick
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


# ------------------------------------------------------------ drawing
def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(".") * 0.6 - t.count(" ") * 0.3 - t.count(NB) * 0.3) * fs * 0.6


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


class Canvas:
    """Shapes and text (y down); tracks the bounding box and writes a tight SVG.
    flat=True: also check that each label is inside one shape or outside all, and no line runs through it."""

    def __init__(self, flat=False):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.flat = flat
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def raw(self, fn, box):
        """fn(ox, oy) writes the element; box is its extent (x0, y0, x1, y1)."""
        self.el.append(("r", fn))
        self.grow(*box)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:                                   # labels never touch each other
            assert box[2] + 3 < b[0] or b[2] + 3 < box[0] or box[3] + 2 < b[1] or b[3] + 2 < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert all(h == len(pts) for h in hit), ("label crosses an edge", (x0, y0, x1, y1), hit)
            for a, b in self.segs:
                for i in range(41):
                    x, y = a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40
                    assert not (x0 - 2 < x < x1 + 2 and y0 - 2 < y < y1 + 2), ("line through a label", (x0, y0))

    def svg(self, label, pad=5):
        if self.flat:
            self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                  # keep these pictures out of the 'square' print size
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, 1.6 if dashed else sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            elif e[0] == "r":
                s.append(e[1](ox, oy))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def arc(cx, cy, r, a0, a1, n=36):
    """Points on a circle (model coordinates, y up) from angle a0 to a1 in degrees."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def dim_v(cv, x, y0, y1, t, side="left"):
    """Vertical dimension line (screen coordinates) with end ticks and its label beside it."""
    cv.line((x, y0), (x, y1), sw=1.6, col=INK)
    cv.line((x - 5, y0), (x + 5, y0), sw=1.6, col=INK)
    cv.line((x - 5, y1), (x + 5, y1), sw=1.6, col=INK)
    if side == "left":
        cv.text(x - 9, (y0 + y1) / 2, t, 16, "end")
    else:
        cv.text(x + 9, (y0 + y1) / 2, t, 16, "start")


class Flat:
    """A flat composite shape: outline in model units (y up), scaled to fit; labels outside the edges."""

    def __init__(self, pts, mw=190, mh=120, k=None):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        self.k = k or min(mw / (max(xs) - min(xs)), mh / (max(ys) - min(ys)))
        self.cv = Canvas(flat=True)
        self.scr = [self.s(p) for p in pts]
        self.cv.poly(self.scr, FILL)

    def s(self, p):
        return (p[0] * self.k, -p[1] * self.k)

    def edge(self, p, q, t, col=INK):
        """Label the edge p-q (model units) on the outside of the shape."""
        a, b = self.s(p), self.s(q)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        if inside((mx + nx * 3, my + ny * 3), self.scr):
            nx, ny = -nx, -ny
        w = tw(t, 16)
        off = abs(nx) * w / 2 + abs(ny) * 8 + 6
        self.cv.text(mx + nx * off, my + ny * off, t, 16, col=col)

    def dash(self, p, q):
        self.cv.line(self.s(p), self.s(q), dashed=True)

    def label_in(self, p, t, anchor="middle"):
        x, y = self.s(p)
        self.cv.text(x, y, t, 16, anchor)

    def svg(self, label):
        return self.cv.svg(label)


# ---------- flat shapes
def lshape_pts(W, H, a, b):
    """W by H rectangle with an a by b notch cut from the top right corner."""
    return [(0, 0), (W, 0), (W, H - b), (W - a, H - b), (W - a, H), (0, H)]


def lshape_svg(W, H, a, b, u, ask=False):
    f = Flat(lshape_pts(W, H, a, b))
    f.edge((0, 0), (W, 0), U(W, u))
    f.edge((0, H), (0, 0), U(H, u))
    f.edge((W - a, H), (0, H), U(W - a, u))
    f.edge((W, 0), (W, H - b), U(H - b, u))
    if ask:
        f.edge((W - a, H - b), (W, H - b), "?", RED)
    return f.svg("L-shaped figure %s by %s with a corner cut out" % (U(W, u), U(H, u)))


def tomb_pts(w, h):
    return [(0, 0), (w, 0), (w, h)] + arc(w / 2, h, w / 2, 0, 180)[1:-1] + [(0, h)]


def tomb_svg(w, h, u):
    """Rectangle w by h with a semicircle (diameter w) on top; the shared side is dashed."""
    f = Flat(tomb_pts(float(w), float(h)), mh=130)
    f.dash((0, float(h)), (float(w), float(h)))
    f.edge((0, 0), (float(w), 0), U(w, u))
    f.edge((0, float(h)), (0, 0), U(h, u))
    return f.svg("rectangle %s wide and %s tall with a semicircle on top" % (U(w, u), U(h, u)))


def semi_svg(d, u):
    d = float(d)
    f = Flat([(0, 0), (d, 0)] + arc(d / 2, 0, d / 2, 0, 180)[1:-1], mw=150, mh=80)
    f.edge((0, 0), (d, 0), U(d, u))
    return f.svg("semicircle with a diameter of %s" % U(d, u))


def stadium_pts(L, d):
    r = d / 2
    return ([(0, 0), (L, 0)] + arc(L, r, r, -90, 90)[1:-1] + [(L, d), (0, d)] + arc(0, r, r, 90, 270)[1:-1])


def stadium_svg(L, d, u, label=None):
    """Rectangle L by d with a semicircle on each end; the shared sides are dashed."""
    L, d = float(L), float(d)
    f = Flat(stadium_pts(L, d), mw=210, mh=110)
    f.dash((0, 0), (0, d))
    f.dash((L, 0), (L, d))
    f.edge((0, 0), (L, 0), U(L, u))
    x, y = f.s((0, d / 2))
    f.cv.text(x + 8, y, U(d, u), 16, "start")
    return f.svg(label or "rectangle %s long with a semicircle on each end, diameter %s" % (U(L, u), U(d, u)))


def bite_pts(w, h, d):
    """w by h rectangle with a semicircle (diameter d) cut out of the middle of the top side."""
    c, r = w / 2, d / 2
    return [(0, 0), (w, 0), (w, h), (c + r, h)] + arc(c, h, r, 0, -180)[1:-1] + [(c - r, h), (0, h)]


def bite_svg(w, h, d, u):
    w, h, d = float(w), float(h), float(d)
    f = Flat(bite_pts(w, h, d))
    f.dash((w / 2 - d / 2, h), (w / 2 + d / 2, h))
    f.edge((0, 0), (w, 0), U(w, u))
    f.edge((0, h), (0, 0), U(h, u))
    f.edge((w / 2 + d / 2, h), (w / 2 - d / 2, h), U(d, u))
    return f.svg("rectangle %s by %s with a semicircle of diameter %s cut out of the top" % (U(w, u), U(h, u), U(d, u)))


def house_flat_svg(w, h, t, s, u, mode):
    """House front: w by h rectangle with a triangle on top (height t, sloped sides s).
    mode 'p': label w, h and one sloped side. mode 'a': label w, h, t (dimension lines) and a sloped side."""
    w, h, t = float(w), float(h), float(t)
    f = Flat([(0, 0), (w, 0), (w, h), (w / 2, h + t), (0, h)], mw=170, mh=130)
    f.dash((0, h), (w, h))
    f.edge((0, 0), (w, 0), U(w, u))
    if mode == "p":
        f.edge((0, h), (0, 0), U(h, u))
        f.edge((w / 2, h + t), (0, h), U(s, u))
    else:
        f.edge((w, h), (w / 2, h + t), U(s, u))
        f.dash((w / 2, h + t), (w / 2, h))
        k = f.k
        f.cv.line((-14, -(h + t) * k), (w / 2 * k - 4, -(h + t) * k), dashed=True, col=INK)
        dim_v(f.cv, -14, 0, -h * k, U(h, u))
        dim_v(f.cv, -14, -h * k, -(h + t) * k, U(t, u))
    return f.svg("house shape: rectangle %s by %s with a triangle on top" % (U(w, u), U(h, u)))


def pool_svg(L, a, sd, dd, u):
    """Side view of the water in a pool: shallow part a long and sd deep, then the deep part to the end."""
    L, a, sd, dd = float(L), float(a), float(sd), float(dd)
    f = Flat([(0, 0), (L, 0), (L, -dd), (a, -dd), (a, -sd), (0, -sd)], k=9.0)
    f.edge((0, 0), (L, 0), U(L, u))
    f.edge((0, -sd), (0, 0), U(sd, u))
    f.edge((L, 0), (L, -dd), U(dd, u))
    f.edge((0, -sd), (a, -sd), U(a, u))
    f.edge((a, -dd), (L, -dd), U(L - a, u))
    return f.svg("side view of a pool %s long, %s deep at the shallow end and %s deep at the deep end"
                 % (U(L, u), U(sd, u), U(dd, u)))


# ---------- solids
def proj(X, Y, Z, k):
    """x to the right, y up, z (depth) to the back."""
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def box_faces(cv, x0, y0, z0, L, H, W, k):
    p = lambda a, b, c: proj(x0 + a, y0 + b, z0 + c, k)
    cv.poly([p(0, 0, 0), p(L, 0, 0), p(L, H, 0), p(0, H, 0)], FILL)
    cv.poly([p(0, H, 0), p(L, H, 0), p(L, H, W), p(0, H, W)], TOP)
    cv.poly([p(L, 0, 0), p(L, 0, W), p(L, H, W), p(L, H, 0)], SIDE)
    return p


def depth_label(cv, k, x, D, t):
    """Label the depth on the bottom-right edge of a solid whose front-right bottom corner is at (x, 0, 0)."""
    sx, sy = proj(x, 0, D / 2, k)
    cv.text(sx + 7, sy + 11, t, 16, "start")


def prism_svg(L, W, H, u, label=None):
    L, W, H = float(L), float(W), float(H)
    k = min(165 / (L + W * DZX), 100 / (H + W * DZY))
    cv = Canvas()
    p = box_faces(cv, 0, 0, 0, L, H, W, k)
    for a, b in [((0, 0, W), (L, 0, W)), ((0, 0, W), (0, H, W)), ((0, 0, W), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True)
    x, y = p(L / 2, 0, 0)
    cv.text(x, y + 17, U(L, u), 16)
    x, y = p(0, H / 2, 0)
    cv.text(x - 8, y, U(H, u), 16, "end")
    depth_label(cv, k, L, W, U(W, u))
    return cv.svg(label or "rectangular prism %s by %s by %s" % (U(L, u), U(W, u), U(H, u)))


def tri_svg(a, b, L, u, label=None):
    """Prism whose ends are right triangles (legs a across and b up), length L going back."""
    a, b, L = float(a), float(b), float(L)
    k = min(165 / (a + L * DZX), 110 / (b + L * DZY))
    cv = Canvas()
    p = lambda x, y, z: proj(x, y, z, k)
    cv.poly([p(0, 0, 0), p(a, 0, 0), p(0, b, 0)], FILL)
    cv.poly([p(0, b, 0), p(a, 0, 0), p(a, 0, L), p(0, b, L)], TOP)
    for s, t in [((0, 0, 0), (0, 0, L)), ((0, 0, L), (a, 0, L)), ((0, 0, L), (0, b, L))]:
        cv.line(p(*s), p(*t), dashed=True)
    ox, oy = p(0, 0, 0)
    cv.raw(lambda X, Y: "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
           % (ox + 11 - X, oy - Y, ox + 11 - X, oy - 11 - Y, ox - X, oy - 11 - Y, GREEN), (ox, oy - 11, ox + 11, oy))
    x, y = p(a / 2, 0, 0)
    cv.text(x, y + 17, U(a, u), 16)
    x, y = p(0, b / 2, 0)
    cv.text(x - 8, y, U(b, u), 16, "end")
    depth_label(cv, k, a, L, U(L, u))
    return cv.svg(label or "triangular prism with right-triangle ends %s by %s, length %s" % (U(a, u), U(b, u), U(L, u)))


def extrude_svg(front, D, k, cv, arcs=()):
    """Prism with a convex front face (model units, y up) going back D. arcs: indexes of edges on a curve."""
    n = len(front)
    p = lambda x, y, z: proj(x, y, z, k)
    vis = []
    for i in range(n):
        (x1, y1), (x2, y2) = front[i], front[(i + 1) % n]
        nx, ny = (y2 - y1), -(x2 - x1)                       # outward normal for a counterclockwise outline
        vis.append(nx * DZX + ny * DZY > 1e-9)
    for i in range(n):
        if vis[i]:
            (x1, y1), (x2, y2) = front[i], front[(i + 1) % n]
            curve = i in arcs
            cv.el.append(("p", [p(x1, y1, 0), p(x2, y2, 0), p(x2, y2, D), p(x1, y1, D)],
                          TOP if x1 > x2 and not curve else SIDE,
                          0.8 if curve else 2.4, SIDE if curve else GREEN))
            cv.polys.append([p(x1, y1, 0), p(x2, y2, 0), p(x2, y2, D), p(x1, y1, D)])
            for q in [p(x1, y1, D), p(x2, y2, D)]:
                cv.grow(q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2)
    # silhouette of the curved part: back edges of visible curve strips next to hidden or flat strips
    for i in range(n):
        if vis[i] and i in arcs:
            (x1, y1), (x2, y2) = front[i], front[(i + 1) % n]
            cv.line(p(x1, y1, D), p(x2, y2, D), sw=2.4)
            prev_curve = ((i - 1) % n) in arcs and vis[(i - 1) % n]
            next_curve = ((i + 1) % n) in arcs and vis[(i + 1) % n]
            if not prev_curve and vis[(i - 1) % n] is False:
                cv.line(p(x1, y1, 0), p(x1, y1, D), sw=2.4)
            if not next_curve and not vis[(i + 1) % n]:
                cv.line(p(x2, y2, 0), p(x2, y2, D), sw=2.4)
    cv.poly([p(x, y, 0) for x, y in front], FILL)
    return p


def mailbox_svg(w, h, D, u):
    """Box w wide, h high and D deep with half a cylinder (diameter w) on top."""
    w, h, D = float(w), float(h), float(D)
    front = [(0, 0), (w, 0), (w, h)] + arc(w / 2, h, w / 2, 0, 180, 24)[1:-1] + [(0, h)]
    arcs = set(range(2, 2 + 24))
    k = min(160 / (w + D * DZX), 125 / (h + w / 2 + D * DZY))
    cv = Canvas()
    p = extrude_svg(front, D, k, cv, arcs)
    cv.line(p(0, h, 0), p(w, h, 0), dashed=True)
    x, y = p(w / 2, 0, 0)
    cv.text(x, y + 17, U(w, u), 16)
    x, y = p(0, h / 2, 0)
    cv.text(x - 8, y, U(h, u), 16, "end")
    depth_label(cv, k, w, D, U(D, u))
    return cv.svg("box %s wide, %s high and %s long with half a cylinder on top" % (U(w, u), U(h, u), U(D, u)))


def house_svg(w, h, t, D, u):
    """House-shaped prism: front is a w by h rectangle with a triangle (height t) on top; D long."""
    w, h, t, D = float(w), float(h), float(t), float(D)
    front = [(0, 0), (w, 0), (w, h), (w / 2, h + t), (0, h)]
    k = min(160 / (w + D * DZX), 125 / (h + t + D * DZY))
    cv = Canvas()
    p = extrude_svg(front, D, k, cv)
    cv.line(p(0, h, 0), p(w, h, 0), dashed=True)
    x, y = p(w / 2, 0, 0)
    cv.text(x, y + 17, U(w, u), 16)
    cv.line((-14, -(h + t) * k), (w / 2 * k - 4, -(h + t) * k), dashed=True, col=INK)
    dim_v(cv, -14, 0, -h * k, U(h, u))
    dim_v(cv, -14, -h * k, -(h + t) * k, U(t, u))
    depth_label(cv, k, w, D, U(D, u))
    return cv.svg("house-shaped prism %s wide and %s long, walls %s high, roof %s high" % (U(w, u), U(D, u), U(h, u), U(t, u)))


def step_svg(L, H, L2, r, D, u):
    """Two boxes: lower L long and H - r high; upper L2 long and r high, on the left end. Both D deep."""
    L, H, L2, r, D = float(L), float(H), float(L2), float(r), float(D)
    k = min(165 / (L + D * DZX), 115 / (H + D * DZY))
    cv = Canvas()
    box_faces(cv, 0, 0, 0, L, H - r, D, k)
    p = box_faces(cv, 0, H - r, 0, L2, r, D, k)
    x, y = proj(L / 2, 0, 0, k)
    cv.text(x, y + 17, U(L, u), 16)
    x, y = proj(0, H / 2, 0, k)
    cv.text(x - 8, y, U(H, u), 16, "end")
    depth_label(cv, k, L, D, U(D, u))
    x, y = proj(L2 / 2, H, D, k)
    cv.text(x, y - 15, U(L2, u), 16)
    x, y = proj(L2, H - r / 2, D, k)
    cv.text(x + 8, y, U(r, u), 16, "start")
    return cv.svg("step-shaped prism: %s long, %s high and %s deep, top step %s long and %s high"
                  % (U(L, u), U(H, u), U(D, u), U(L2, u), U(r, u)))


def cubebox_svg(L, W, H, a, u):
    """a-cube centred on top of an L by W by H box."""
    L, W, H, a = float(L), float(W), float(H), float(a)
    k = min(165 / (L + W * DZX), 120 / (H + a + W * DZY))
    cv = Canvas()
    box_faces(cv, 0, 0, 0, L, H, W, k)
    box_faces(cv, (L - a) / 2, H, (W - a) / 2, a, a, a, k)
    x, y = proj(L / 2, 0, 0, k)
    cv.text(x, y + 17, U(L, u), 16)
    x, y = proj(0, H / 2, 0, k)
    cv.text(x - 8, y, U(H, u), 16, "end")
    depth_label(cv, k, L, W, U(W, u))
    x, y = proj(L / 2, H + a, (W + a) / 2, k)
    cv.text(x, y - 15, U(a, u), 16)
    return cv.svg("cube with %s edges on top of a box %s by %s by %s" % (U(a, u), U(L, u), U(W, u), U(H, u)))


def cyl_body(cv, cx, base, R, Hh, ry):
    """Upright cylinder centred at x = cx with its bottom at screen y = base."""
    cv.raw(lambda X, Y: "<path d='M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f Z' fill='%s' stroke='%s' "
           "stroke-width='2.4' stroke-linejoin='round'/>"
           % (cx - R - X, base - Hh - Y, cx - R - X, base - Y, R, ry, cx + R - X, base - Y, cx + R - X, base - Hh - Y,
              SIDE, GREEN), (cx - R - 2, base - Hh - 2, cx + R + 2, base + ry + 2))
    cv.raw(lambda X, Y: "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='2.4'/>"
           % (cx - X, base - Hh - Y, R, ry, TOP, GREEN), (cx - R - 2, base - Hh - ry - 2, cx + R + 2, base - Hh + ry + 2))


def cyl_svg(r, h, u, show_d=False):
    r, h = float(r), float(h)
    k = min(62 / r, 115 / h)
    R, H = r * k, h * k
    ry = R * 0.3
    cv = Canvas()
    cyl_body(cv, 0, 0, R, H, ry)
    cv.raw(lambda X, Y: "<path d='M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 4'/>" % (-R - X, -Y, R, ry, R - X, -Y, GREEN), (-R, -ry, R, 0))
    if show_d:
        cv.line((-R, -H), (R, -H), sw=2.2, col=RED)
        cv.text(0, -H - ry - 12, U(2 * r, u), 16)
    else:
        cv.line((0, -H), (R, -H), sw=2.2, col=RED)
        cv.raw(lambda X, Y: "<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s'/>" % (-X, -H - Y, RED), (-4, -H - 4, 4, -H + 4))
        cv.text(R / 2, -H - ry - 12, U(r, u), 16)
    dim_v(cv, R + 14, 0, -H, U(h, u), "right")
    what = "diameter" if show_d else "radius"
    return cv.svg("cylinder with %s %s and height %s" % (what, U(2 * r if show_d else r, u), U(h, u)))


def cake_svg(d1, h1, d2, h2, u):
    """Cylinder (diameter d2, height h2) centred on top of a wider cylinder (d1, h1). Diameters shown."""
    d1, h1, d2, h2 = float(d1), float(h1), float(d2), float(h2)
    k = min(150 / d1, 120 / (h1 + h2))
    R1, R2, H1, H2 = d1 / 2 * k, d2 / 2 * k, h1 * k, h2 * k
    ry1, ry2 = R1 * 0.3, R2 * 0.3
    cv = Canvas()
    cyl_body(cv, 0, 0, R1, H1, ry1)
    cyl_body(cv, 0, -H1, R2, H2, ry2)
    cv.line((-R2, -H1 - H2), (R2, -H1 - H2), sw=2.2, col=RED)
    cv.text(0, -H1 - H2 - ry2 - 12, U(d2, u), 16)
    yb = ry1 + 16
    cv.line((-R1, ry1 + 4), (-R1, yb + 5), sw=1.2, col=INK)
    cv.line((R1, ry1 + 4), (R1, yb + 5), sw=1.2, col=INK)
    cv.line((-R1, yb), (R1, yb), sw=1.6, col=INK)
    cv.text(0, yb + 15, U(d1, u), 16)
    xd = R1 + 16
    cv.line((R2 + 4, -H1 - H2), (xd + 5, -H1 - H2), dashed=True, col=INK)
    cv.line((xd, 0), (xd, -H1 - H2), sw=1.6, col=INK)
    for y in (0, -H1, -H1 - H2):
        cv.line((xd - 5, y), (xd + 5, y), sw=1.6, col=INK)
    cv.text(xd + 9, -H1 / 2, U(h1, u), 16, "start")
    cv.text(xd + 9, -H1 - H2 / 2, U(h2, u), 16, "start")
    return cv.svg("two cylinders stacked: bottom diameter %s and height %s, top diameter %s and height %s"
                  % (U(d1, u), U(h1, u), U(d2, u), U(h2, u)))


# ------------------------------------------------------------ formulas (all Decimal)
def D(x):
    return Dm(str(x))


def semi_arc(d):
    return PI * D(d) / 2


def semi_area(d):
    r = D(d) / 2
    return PI * r * r / 2


def circ_area(r):
    return PI * D(r) * D(r)


# ============================================================ set 1: perimeter
def set_perimeter():
    its = []
    its.append(mcq("What is the perimeter of a composite shape?", "the distance around its outside edge",
                   ["the sum of the perimeters of all its parts", "the space inside the shape",
                    "the length of its longest side"],
                   "Perimeter is the distance <b>around the outside edge</b>. Lines inside the shape, where two parts "
                   "meet, are not part of it. That is why adding the perimeters of the parts gives too much."))
    its.append(mcq("A semicircle has a diameter d. How long is its curved edge?", "π × d ÷ 2",
                   ["π × d", "2 × π × d", "π × r × r ÷ 2"],
                   "A full circle has a circumference of π × d. A semicircle is half a circle, so its curved edge is "
                   "<b>π × d ÷ 2</b>. π × r × r ÷ 2 is the <b>area</b> of a semicircle."))
    # missing side
    W, H, a, b = 13, 9, 5, 3
    its.append(mcq("Find the length of the side marked with a red question mark." + fig(lshape_svg(W, H, a, b, "m", ask=True)),
                   U(a, "m"), [U(W + W - a, "m"), U(W, "m"), U(H - b, "m")],
                   "The bottom is %s long and the top is only %s, so the missing side is %s − %s = <b>%s</b>."
                   % (U(W, "m"), U(W - a, "m"), N(W), N(W - a), U(a, "m"))))
    # L-shapes
    for W, H, a, b, u in [(10, 8, 4, 3, "cm"), (12, 9, 5, 4, "m"), (15, 10, 6, 4, "cm"), (9, 7, 3, 2, "m"),
                          (14, 11, 8, 5, "cm")]:
        P = 2 * (W + H)
        lab = W + H + (W - a) + (H - b)
        split = P + 2 * (H - b)
        its.append(mcq("Find the perimeter of this shape." + fig(lshape_svg(W, H, a, b, u)), U(P, u),
                       [U(lab, u), U(split, u), U(P - a, u)],
                       "Find the 2 missing sides: %s − %s = %s and %s − %s = %s. Add all 6 sides: "
                       "%s + %s + %s + %s + %s + %s = <b>%s</b>. Adding only the 4 labelled sides gives %s."
                       % (N(W), N(W - a), N(a), N(H), N(H - b), N(b),
                          N(W), N(H - b), N(a), N(b), N(W - a), N(H), U(P, u), U(lab, u))))
    # house fronts
    for w, h, t, s, u in [(8, 5, 3, 5, "m"), (12, 6, 8, 10, "cm"), (6, 4, 4, 5, "m")]:
        P = w + 2 * h + 2 * s
        its.append(mcq("The front of this shed is a rectangle with a triangle on top. The two sloped sides are equal. "
                       "Find the perimeter." + fig(house_flat_svg(w, h, t, s, u, "p")), U(P, u),
                       [U(2 * w + 2 * h + 2 * s, u), U(w + 2 * h + s, u), U(2 * (w + h), u)],
                       "Go around the outside: bottom %s, two walls %s + %s, two sloped sides %s + %s. "
                       "%s + %s + %s + %s + %s = <b>%s</b>. The dashed line is inside the shape, so do not count it."
                       % (N(w), N(h), N(h), N(s), N(s), N(w), N(h), N(h), N(s), N(s), U(P, u))))
    # semicircle alone
    for d, u, f in [(10, "cm", True), (8, "m", False)]:
        c = semi_arc(d)
        P = c + d
        q = ("Find the perimeter of this semicircle." + USE + fig(semi_svg(d, u)) if f else
             "A semicircle has a diameter of %s. Find its perimeter.%s" % (U(d, u), USE))
        its.append(mcq(q, U(P, u), [U(c, u), U(2 * c + d, u), U(c + D(d) / 2, u)],
                       "Curved edge: 3.14 × %s ÷ 2 = %s. Add the straight side (the diameter): %s + %s = <b>%s</b>."
                       % (N(d), N(c), N(c), N(d), U(P, u))))
    # rectangle + semicircle on top
    for w, h, u, f in [(10, 12, "cm", True), (6, 8, "m", True), (4, 5, "m", False)]:
        c = semi_arc(w)
        P = w + 2 * h + c
        q = ("Find the perimeter of this shape." + USE + fig(tomb_svg(w, h, u)) if f else
             "A window is a rectangle %s wide and %s tall with a semicircle on top. Find the perimeter of the "
             "window.%s" % (U(w, u), U(h, u), USE))
        its.append(mcq(q, U(P, u),
                       [U(w + 2 * h + 2 * c, u), U(2 * w + 2 * h + c, u), U(w + 2 * h + c / 2, u)],
                       "Curved edge: 3.14 × %s ÷ 2 = %s. Straight sides: %s + %s + %s = %s. "
                       "Total: %s + %s = <b>%s</b>. The top of the rectangle is inside the shape, so it is not counted."
                       % (N(w), N(c), N(w), N(h), N(h), N(w + 2 * h), N(w + 2 * h), N(c), U(P, u))))
    # stadium
    for L, d, u in [(20, 10, "cm"), (30, 14, "m")]:
        c = PI * d
        P = 2 * L + c
        its.append(mcq("This shape is a rectangle with a semicircle on each end. Find its perimeter." + USE
                       + fig(stadium_svg(L, d, u)), U(P, u),
                       [U(2 * L + 2 * c, u), U(2 * L + 2 * d + c, u), U(2 * L + c / 2, u)],
                       "Two semicircles make one full circle: 3.14 × %s = %s. Two straight sides: 2 × %s = %s. "
                       "%s + %s = <b>%s</b>. The dashed lines are inside, so they are not counted."
                       % (N(d), N(c), N(L), N(2 * L), N(2 * L), N(c), U(P, u))))
    # rectangle with a semicircle cut out
    for w, h, d, u in [(12, 8, 6, "cm"), (16, 10, 8, "m")]:
        c = semi_arc(d)
        P = 2 * (w + h) - d + c
        its.append(mcq("A semicircle is cut out of the top of this rectangle. Find the perimeter of the shape that is left."
                       + USE + fig(bite_svg(w, h, d, u)), U(P, u),
                       [U(2 * (w + h), u), U(2 * (w + h) + c, u), U(2 * (w + h) - d + 2 * c, u)],
                       "Rectangle: 2 × (%s + %s) = %s. Take away the %s gap: %s − %s = %s. Add the curved edge "
                       "3.14 × %s ÷ 2 = %s: %s + %s = <b>%s</b>."
                       % (N(w), N(h), N(2 * (w + h)), U(d, u), N(2 * (w + h)), N(d), N(2 * (w + h) - d),
                          N(d), N(c), N(2 * (w + h) - d), N(c), U(P, u))))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter of composite shapes", "items": its}


# ============================================================ set 2: area
def set_area():
    its = []
    its.append(mcq("How can you find the area of a composite shape?",
                   "Split it into simple shapes, then add or subtract their areas",
                   ["Multiply its longest side by its shortest side", "Add the lengths of all its sides",
                    "Multiply all the labelled sides together"],
                   "<b>Split it into simple shapes</b> (rectangles, triangles, semicircles). Add the parts, or "
                   "subtract a part that is cut out."))
    its.append(mcq("Which formula gives the area of a semicircle with radius r?", "A = π × r × r ÷ 2",
                   ["A = π × r × r", "A = π × d ÷ 2", "A = π × d × d ÷ 2"],
                   "A semicircle is half a circle, so its area is half of πr²: <b>A = π × r × r ÷ 2</b>. "
                   "π × d ÷ 2 is the length of its curved edge."))
    for W, H, a, b, u in [(11, 8, 5, 3, "cm"), (14, 10, 6, 4, "m"), (12, 7, 4, 3, "cm"), (16, 12, 7, 5, "m")]:
        A = W * H - a * b
        over = (W - a) * H + W * (H - b)
        its.append(mcq("Find the area of this shape." + fig(lshape_svg(W, H, a, b, u)), U(A, u + "²"),
                       [U(W * H, u + "²"), U(over, u + "²"), U(2 * (W + H), u + "²")],
                       "Whole rectangle: %s × %s = %s. Corner cut out: %s × %s = %s. %s − %s = <b>%s</b>. "
                       "(%s adds two rectangles that overlap, so a part is counted twice.)"
                       % (N(W), N(H), N(W * H), N(a), N(b), N(a * b), N(W * H), N(a * b), U(A, u + "²"),
                          N(over))))
    for w, h, t, s, u in [(8, 5, 3, 5, "m"), (12, 6, 8, 10, "cm"), (6, 4, 4, 5, "m")]:
        tri = D(w) * t / 2
        A = w * h + tri
        its.append(mcq("Find the area of this house shape." + fig(house_flat_svg(w, h, t, s, u, "a")), U(A, u + "²"),
                       [U(w * h + w * t, u + "²"), U(w * h + D(w) * s / 2, u + "²"), U(w * h, u + "²")],
                       "Rectangle: %s × %s = %s. Triangle: ½ × %s × %s = %s (use the height %s, not the sloped side). "
                       "%s + %s = <b>%s</b>."
                       % (N(w), N(h), N(w * h), N(w), N(t), N(tri), N(t), N(w * h), N(tri), U(A, u + "²"))))
    for w, h, u, f in [(10, 12, "cm", True), (6, 8, "m", True), (8, 5, "cm", False)]:
        sa = semi_area(w)
        A = w * h + sa
        q = ("Find the area of this shape." + USE + fig(tomb_svg(w, h, u)) if f else
             "A shape is a rectangle %s wide and %s tall with a semicircle on the %s side. Find its area.%s"
             % (U(w, u), U(h, u), U(w, u), USE))
        its.append(mcq(q, U(A, u + "²"),
                       [U(w * h + 2 * sa, u + "²"), U(w * h + PI * w * w / 2, u + "²"), U(w * h, u + "²")],
                       "Rectangle: %s × %s = %s. Semicircle: r = %s ÷ 2 = %s, so 3.14 × %s × %s ÷ 2 = %s. "
                       "%s + %s = <b>%s</b>."
                       % (N(w), N(h), N(w * h), N(w), N(D(w) / 2), N(D(w) / 2), N(D(w) / 2), N(sa),
                          N(w * h), N(sa), U(A, u + "²"))))
    for L, d, u in [(20, 10, "cm"), (30, 14, "m")]:
        circ = circ_area(D(d) / 2)
        A = L * d + circ
        its.append(mcq("This shape is a rectangle with a semicircle on each end. Find its area." + USE
                       + fig(stadium_svg(L, d, u)), U(A, u + "²"),
                       [U(L * d + 2 * circ, u + "²"), U(L * d + circ / 2, u + "²"), U(L * d + circ_area(d), u + "²")],
                       "Rectangle: %s × %s = %s. Two semicircles make one circle with r = %s: 3.14 × %s × %s = %s. "
                       "%s + %s = <b>%s</b>."
                       % (N(L), N(d), N(L * d), N(D(d) / 2), N(D(d) / 2), N(D(d) / 2), N(circ),
                          N(L * d), N(circ), U(A, u + "²"))))
    for w, h, d, u in [(12, 8, 6, "cm"), (16, 10, 8, "m")]:
        sa = semi_area(d)
        A = w * h - sa
        its.append(mcq("A semicircle is cut out of this rectangle. Find the area of the shape that is left." + USE
                       + fig(bite_svg(w, h, d, u)), U(A, u + "²"),
                       [U(w * h - 2 * sa, u + "²"), U(w * h + sa, u + "²"), U(w * h, u + "²")],
                       "Rectangle: %s × %s = %s. Semicircle: r = %s, so 3.14 × %s × %s ÷ 2 = %s. "
                       "The semicircle is cut out, so subtract: %s − %s = <b>%s</b>."
                       % (N(w), N(h), N(w * h), N(D(d) / 2), N(D(d) / 2), N(D(d) / 2), N(sa),
                          N(w * h), N(sa), U(A, u + "²"))))
    for W, H, w, h in [(30, 24, 20, 14), (40, 30, 30, 16)]:
        A = W * H - w * h
        its.append(mcq("A picture frame is a %s cm by %s cm rectangle with a %s cm by %s cm opening in the middle. "
                       "What is the area of the frame?" % (N(W), N(H), N(w), N(h)), U(A, "cm²"),
                       [U((W - w) * (H - h), "cm²"), U(W * H + w * h, "cm²"), U(W * H, "cm²")],
                       "Outside rectangle: %s × %s = %s. Opening: %s × %s = %s. Frame: %s − %s = <b>%s</b>."
                       % (N(W), N(H), N(W * H), N(w), N(h), N(w * h), N(W * H), N(w * h), U(A, "cm²"))))
    its.append(mcq("A rectangle is 10 m by 6 m. A right triangle with legs of 4 m and 3 m is cut off one corner. "
                   "What is the area that is left?", "54 m²", ["48 m²", "60 m²", "66 m²"],
                   "Rectangle: 10 × 6 = 60 m². Triangle: ½ × 4 × 3 = 6 m². 60 − 6 = <b>54 m²</b>. "
                   "48 m² forgets the ½ for the triangle."))
    assert 10 * 6 - Dm(4) * 3 / 2 == 54
    tri, sa = Dm(8) * 12 / 2, semi_area(8)
    A = tri + sa
    assert A == Dm("73.12")
    its.append(mcq("An ice cream cone shape is a triangle with a base of 8 cm and a height of 12 cm, with a semicircle "
                   "(diameter 8 cm) on the base. Find the total area." + USE, U(A, "cm²"),
                   [U(2 * tri + sa, "cm²"), U(tri + 2 * sa, "cm²"), U(tri + PI * 64 / 2, "cm²")],
                   "Triangle: ½ × 8 × 12 = 48 cm². Semicircle: r = 4, so 3.14 × 4 × 4 ÷ 2 = 25.12 cm². "
                   "48 + 25.12 = <b>73.12 cm²</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Area of composite shapes", "items": its}


# ============================================================ set 3: volume
def set_volume():
    its = []
    its.append(mcq("How do you find the volume of a composite solid?",
                   "Add the volumes of its parts, or subtract a part that is removed",
                   ["Multiply all the labelled lengths together", "Add the areas of all its faces",
                    "Find the volume of the largest part only"],
                   "Split the solid into prisms and cylinders. <b>Add their volumes</b>, or <b>subtract</b> a part "
                   "that is cut out. Adding the areas of the faces gives the surface area."))
    its.append(mcq("A prism has the same shape all the way through. Which rule gives its volume?",
                   "area of the base × length", ["perimeter of the base × length", "area of the base + length",
                                                 "area of the base ÷ length"],
                   "Every slice of a prism is the same shape as its base, so V = <b>area of the base × length</b> "
                   "(or height). This works for any base, even an L shape or a house shape."))
    for L, H, L2, r, Dd, u in [(10, 8, 4, 3, 5, "cm"), (12, 9, 5, 4, 6, "cm"), (8, 6, 3, 2, 10, "m"),
                               (15, 10, 5, 4, 8, "cm")]:
        low, up = L * (H - r) * Dd, L2 * r * Dd
        V = low + up
        its.append(mcq("This solid is made of two rectangular prisms. Find its volume." + fig(step_svg(L, H, L2, r, Dd, u)),
                       U(V, u + "³"), [U(L * H * Dd, u + "³"), U(low + L2 * H * Dd, u + "³"), U(low, u + "³")],
                       "Bottom prism: %s × %s × %s = %s (its height is %s − %s = %s). Top prism: %s × %s × %s = %s. "
                       "%s + %s = <b>%s</b>."
                       % (N(L), N(Dd), N(H - r), N(low), N(H), N(r), N(H - r), N(L2), N(Dd), N(r), N(up),
                          N(low), N(up), U(V, u + "³"))))
    for w, h, t, Dd, u in [(8, 5, 3, 10, "m"), (6, 4, 4, 10, "cm"), (12, 6, 8, 20, "cm")]:
        front = w * h + D(w) * t / 2
        V = front * Dd
        its.append(mcq("Find the volume of this house-shaped prism." + fig(house_svg(w, h, t, Dd, u)), U(V, u + "³"),
                       [U((w * h + w * t) * Dd, u + "³"), U(w * h * Dd, u + "³"), U(front, u + "³")],
                       "Front (base): %s × %s + ½ × %s × %s = %s + %s = %s %s². Volume: %s × %s = <b>%s</b>."
                       % (N(w), N(h), N(w), N(t), N(w * h), N(D(w) * t / 2), N(front), u, N(front), N(Dd), U(V, u + "³"))))
    for w, h, Dd, u in [(20, 15, 40, "cm"), (10, 6, 30, "cm"), (4, 3, 10, "m")]:
        sa = semi_area(w)
        front = w * h + sa
        V = front * Dd
        q = ("A mailbox is a box with half a cylinder on top. Find its volume." if u == "cm" and w == 20 else
             "This solid is a box with half a cylinder on top. Find its volume." if u == "cm" else
             "A storage shed is a box with half a cylinder for a roof. Find its volume.")
        its.append(mcq(q + USE + fig(mailbox_svg(w, h, Dd, u)), U(V, u + "³"),
                       [U((w * h + 2 * sa) * Dd, u + "³"), U(w * h * Dd, u + "³"),
                        U((w * h + PI * w * w / 2) * Dd, u + "³")],
                       "Front: rectangle %s × %s = %s, plus a semicircle 3.14 × %s × %s ÷ 2 = %s. "
                       "Front area: %s %s². Volume: %s × %s = <b>%s</b>."
                       % (N(w), N(h), N(w * h), N(D(w) / 2), N(D(w) / 2), N(sa), N(front), u, N(front), N(Dd),
                          U(V, u + "³"))))
    for d1, h1, d2, h2, u in [(30, 10, 20, 8, "cm"), (20, 6, 10, 4, "cm"), (8, 5, 4, 6, "m")]:
        r1, r2 = D(d1) / 2, D(d2) / 2
        v1, v2 = PI * r1 * r1 * h1, PI * r2 * r2 * h2
        V = v1 + v2
        its.append(mcq("One cylinder sits on top of another. Find the total volume." + USE + fig(cake_svg(d1, h1, d2, h2, u)),
                       U(V, u + "³"),
                       [U(PI * (D(d1) ** 2 * h1 + D(d2) ** 2 * h2), u + "³"), U(PI * r1 * r1 * (h1 + h2), u + "³"),
                        U(v1, u + "³")],
                       "Bottom: r = %s, so 3.14 × %s × %s × %s = %s. Top: r = %s, so 3.14 × %s × %s × %s = %s. "
                       "%s + %s = <b>%s</b>."
                       % (N(r1), N(r1), N(r1), N(h1), N(v1), N(r2), N(r2), N(r2), N(h2), N(v2), N(v1), N(v2),
                          U(V, u + "³"))))
    for l, w, h, r, kind in [(10, 10, 10, 2, "r"), (20, 12, 5, 3, "d")]:
        box, hole = l * w * h, circ_area(r) * h
        V = box - hole
        q = ("A wooden cube with 10 cm edges has a round hole drilled straight through it. The hole has a radius of 2 cm. "
             "What volume of wood is left?" if kind == "r" else
             "A block is 20 cm long, 12 cm wide and 5 cm high. A round hole with a diameter of 6 cm goes straight down "
             "through it (5 cm deep). What volume is left?")
        its.append(mcq(q + USE, U(V, "cm³"), [U(box + hole, "cm³"), U(box - circ_area(2 * r) * h, "cm³"), U(box, "cm³")],
                       "Block: %s × %s × %s = %s cm³. Hole: %s3.14 × %s × %s × %s = %s cm³. "
                       "The hole is removed, so subtract: %s − %s = <b>%s</b>."
                       % (N(l), N(w), N(h), N(box), "" if kind == "r" else "r = 6 ÷ 2 = 3, so ", N(r), N(r), N(h),
                          N(hole), N(box), N(hole), U(V, "cm³"))))
    box, cyl = 10 * 10 * 4, circ_area(3) * 5
    its.append(mcq("A trophy has a cylinder (radius 3 cm, height 5 cm) on top of a 10 cm × 10 cm × 4 cm box. "
                   "Find its total volume." + USE, U(box + cyl, "cm³"),
                   [U(box + circ_area(6) * 5, "cm³"), U(box, "cm³"), U(box + PI * 6 * 5, "cm³")],
                   "Box: 10 × 10 × 4 = 400 cm³. Cylinder: 3.14 × 3 × 3 × 5 = 141.3 cm³. "
                   "400 + 141.3 = <b>541.3 cm³</b>. r² means 3 × 3, not 3 × 2."))
    assert box + cyl == Dm("541.3")
    V = circ_area(5) * 20 / 2
    its.append(mcq("A solid is half of a cylinder. The cylinder had a radius of 5 cm and a length of 20 cm. "
                   "Find the volume of the half." + USE, U(V, "cm³"),
                   [U(2 * V, "cm³"), U(circ_area(10) * 20 / 2, "cm³"), U(PI * 5 * 20, "cm³")],
                   "Whole cylinder: 3.14 × 5 × 5 × 20 = 1570 cm³. Half: 1570 ÷ 2 = <b>785 cm³</b>."))
    assert V == 785
    V = PI * (25 - 9) * 10
    its.append(mcq("A pipe is a cylinder with a hole through the middle. The outside radius is 5 cm, the inside radius "
                   "is 3 cm and the pipe is 10 cm long. What volume of material is in the pipe?" + USE, U(V, "cm³"),
                   [U(PI * 4 * 10, "cm³"), U(circ_area(5) * 10, "cm³"), U(PI * 34 * 10, "cm³")],
                   "Outside cylinder: 3.14 × 5 × 5 × 10 = 785 cm³. Hole: 3.14 × 3 × 3 × 10 = 282.6 cm³. "
                   "785 − 282.6 = <b>502.4 cm³</b>. (Using r = 5 − 3 = 2 gives only 125.6 cm³.)"))
    assert V == Dm("502.4")
    assert len(its) == 20, len(its)
    return {"title": "Volume of composite prisms and cylinders", "items": its}


# ============================================================ set 4: surface area
def set_surface():
    its = []
    its.append(mcq("What is the surface area of a solid?", "the total area of all its faces",
                   ["the space inside the solid", "the distance around its base", "the area of its base"],
                   "Surface area is <b>the total area of all its faces</b> (like the paper needed to wrap it). "
                   "The space inside is the volume."))
    its.append(mcq("Two solids are glued together face to face. What happens to the faces that touch?",
                   "They are hidden, so they are not part of the surface area",
                   ["They count twice", "They count once", "They are added to the volume"],
                   "The faces that touch are inside the new solid. Nobody could paint them, so <b>they are not part "
                   "of the surface area</b>. Subtract the touching area from <b>both</b> solids."))
    its.append(mcq("The curved surface of a cylinder is unrolled. Which shape does it make?",
                   "a rectangle as long as the circumference", ["a circle", "a rectangle as long as the radius",
                                                                "a triangle"],
                   "Unrolled, the curved surface is <b>a rectangle</b>. One side is the height; the other is the "
                   "circumference 2πr. So its area is 2πr × h."))
    for L, W, H, u in [(6, 4, 5, "cm"), (8, 5, 3, "m"), (12, 10, 4, "cm")]:
        SA = 2 * (L * W + L * H + W * H)
        its.append(mcq("Find the surface area of this rectangular prism." + fig(prism_svg(L, W, H, u)), U(SA, u + "²"),
                       [U(SA // 2, u + "²"), U(2 * (L * H + W * H), u + "²"), U(L * W * H, u + "²")],
                       "Three pairs of faces: 2 × (%s × %s) + 2 × (%s × %s) + 2 × (%s × %s) = %s + %s + %s = <b>%s</b>."
                       % (N(L), N(W), N(L), N(H), N(W), N(H), N(2 * L * W), N(2 * L * H), N(2 * W * H), U(SA, u + "²"))))
    for r, h, u in [(3, 10, "cm"), (5, 8, "cm"), (2, 6, "m")]:
        base, lat = circ_area(r), 2 * PI * r * h
        SA = 2 * base + lat
        its.append(mcq("Find the surface area of this cylinder." + USE + fig(cyl_svg(r, h, u)), U(SA, u + "²"),
                       [U(base + lat, u + "²"), U(lat, u + "²"), U(2 * circ_area(2 * r) + 2 * PI * 2 * r * h, u + "²")],
                       "Two circles: 2 × 3.14 × %s × %s = %s. Curved surface: 2 × 3.14 × %s × %s = %s. "
                       "%s + %s = <b>%s</b>."
                       % (N(r), N(r), N(2 * base), N(r), N(h), N(lat), N(2 * base), N(lat), U(SA, u + "²"))))
    base, lat = circ_area(5), PI * 10 * 20
    its.append(mcq("A cylinder has a diameter of 10 cm and a height of 20 cm. Find its surface area." + USE,
                   U(2 * base + lat, "cm²"), [U(2 * circ_area(10) + 2 * lat, "cm²"), U(base + lat, "cm²"), U(lat, "cm²")],
                   "r = 5 cm. Two circles: 2 × 3.14 × 5 × 5 = 157 cm². Curved surface: 3.14 × 10 × 20 = 628 cm². "
                   "157 + 628 = <b>785 cm²</b>."))
    assert 2 * base + lat == 785
    for a, b, c, L, u in [(3, 4, 5, 10, "cm"), (6, 8, 10, 15, "cm")]:
        ends = D(a) * b
        SA = ends + (a + b + c) * L
        its.append(mcq("The ends of this prism are right triangles with sides %s, %s and %s %s. "
                       "Find its surface area." % (N(a), N(b), N(c), u) + fig(tri_svg(a, b, L, u)), U(SA, u + "²"),
                       [U(2 * ends + (a + b + c) * L, u + "²"), U(ends + (a + b) * L, u + "²"), U(ends / 2 * L, u + "²")],
                       "Two triangles: 2 × ½ × %s × %s = %s. Three rectangles: (%s + %s + %s) × %s = %s. "
                       "%s + %s = <b>%s</b>. Do not forget the sloped face (%s %s wide)."
                       % (N(a), N(b), N(ends), N(a), N(b), N(c), N(L), N((a + b + c) * L), N(ends), N((a + b + c) * L),
                          U(SA, u + "²"), N(c), u)))
    for l, w, h in [(30, 20, 10), (50, 40, 30)]:
        SA = l * w + 2 * l * h + 2 * w * h
        its.append(mcq("An open box (no lid) is %s cm long, %s cm wide and %s cm high. What is the area of cardboard "
                       "needed to make it?" % (N(l), N(w), N(h)), U(SA, "cm²"),
                       [U(SA + l * w, "cm²"), U(2 * l * h + 2 * w * h, "cm²"), U(l * w + l * h + w * h, "cm²")],
                       "Bottom: %s × %s = %s. Front and back: 2 × %s × %s = %s. Two ends: 2 × %s × %s = %s. "
                       "No lid, so %s + %s + %s = <b>%s</b>."
                       % (N(l), N(w), N(l * w), N(l), N(h), N(2 * l * h), N(w), N(h), N(2 * w * h),
                          N(l * w), N(2 * l * h), N(2 * w * h), U(SA, "cm²"))))
    for L, W, H, a, u in [(10, 8, 4, 4, "cm"), (12, 10, 5, 6, "cm"), (20, 20, 10, 10, "cm")]:
        s1, s2, t = 2 * (L * W + L * H + W * H), 6 * a * a, a * a
        SA = s1 + s2 - 2 * t
        its.append(mcq("A cube sits on top of a box. Find the surface area of the whole solid." + fig(cubebox_svg(L, W, H, a, u)),
                       U(SA, u + "²"), [U(s1 + s2, u + "²"), U(s1 + s2 - t, u + "²"), U(s1, u + "²")],
                       "Box: %s. Cube: 6 × %s × %s = %s. The touching faces (%s × %s = %s) are hidden on the box "
                       "<b>and</b> on the cube: %s + %s − 2 × %s = <b>%s</b>."
                       % (N(s1), N(a), N(a), N(s2), N(a), N(a), N(t), N(s1), N(s2), N(t), U(SA, u + "²"))))
    L, H, L2, r, Dd = 12, 8, 5, 3, 6
    front = L * (H - r) + L2 * r
    P = 2 * (L + H)
    SA = 2 * front + P * Dd
    its.append(mcq("Find the surface area of this solid. (Hint: 2 × front area + perimeter of the front × depth.)"
                   + fig(step_svg(L, H, L2, r, Dd, "cm")), U(SA, "cm²"),
                   [U(2 * (L * H + L * Dd + H * Dd), "cm²"), U(front + P * Dd, "cm²"), U(2 * front + (L + H + L2 + r) * Dd, "cm²")],
                   "Front: %s × %s + %s × %s = %s cm². Perimeter of the front: all 6 sides = %s cm. "
                   "2 × %s + %s × %s = %s + %s = <b>%s</b>."
                   % (N(L), N(H - r), N(L2), N(r), N(front), N(P), N(front), N(P), N(Dd), N(2 * front), N(P * Dd), U(SA, "cm²"))))
    assert SA == 390
    w, h, t, s, l = 8, 5, 3, 5, 10
    front = w * h + D(w) * t / 2
    rect = (w + 2 * h + 2 * s) * l
    SA = 2 * front + rect
    its.append(mcq("A shed is shaped like a house: the front is an 8 m by 5 m rectangle with a triangle on top "
                   "(height 3 m, sloped sides 5 m). The shed is 10 m long. Find its surface area, including the floor.",
                   U(SA, "m²"), [U(2 * (w * h + w * t) + rect, "m²"), U(2 * front + (w + 2 * h + 2 * t) * l, "m²"),
                                 U(SA - w * l, "m²")],
                   "Front and back: 2 × (8 × 5 + ½ × 8 × 3) = 2 × 52 = 104 m². Floor 8 × 10 = 80, walls 2 × 5 × 10 = 100, "
                   "roof 2 × 5 × 10 = 100. 104 + 80 + 100 + 100 = <b>384 m²</b>."))
    assert SA == 384
    s1 = 2 * circ_area(10) + 2 * PI * 10 * 5
    s2 = 2 * circ_area(5) + 2 * PI * 5 * 5
    SA = s1 + s2 - 2 * circ_area(5)
    its.append(mcq("A cylinder (radius 5 cm, height 5 cm) is glued on top of a bigger cylinder (radius 10 cm, height 5 cm). "
                   "Find the surface area of the whole solid." + USE, U(SA, "cm²"),
                   [U(s1 + s2, "cm²"), U(s1 + s2 - circ_area(5), "cm²"), U(SA - circ_area(5), "cm²")],
                   "Big cylinder: 2 × 314 + 314 = 942 cm². Small: 2 × 78.5 + 157 = 314 cm². The touching circle "
                   "(78.5 cm²) is hidden on both: 942 + 314 − 2 × 78.5 = <b>1099 cm²</b>."))
    assert SA == 1099
    assert len(its) == 20, len(its)
    return {"title": "Surface area of composite solids", "items": its}


# ============================================================ set 5: word problems
def set_story():
    its = []
    # 1 garden fence
    P = 6 + 6 + 4 + semi_arc(4)
    its.append(mcq("Hana’s garden is a 6 m by 4 m rectangle with a semicircle on one 4 m side. She puts a fence all the "
                   "way around it. How much fence does she need?" + USE, U(P, "m"),
                   [U(16 + PI * 4, "m"), U(20 + semi_arc(4), "m"), U(16 + semi_arc(2), "m")],
                   "Straight sides: 6 + 6 + 4 = 16 m (the side the semicircle sits on is not fenced). "
                   "Curve: 3.14 × 4 ÷ 2 = 6.28 m. 16 + 6.28 = <b>22.28 m</b>."))
    assert P == Dm("22.28")
    # 2 track lap
    lap = 200 + PI * 60
    its.append(mcq("The school track has two straight sides of 100 m and a semicircle at each end. Each semicircle has a "
                   "diameter of 60 m. How long is one lap?" + USE + fig(stadium_svg(100, 60, "m", "running track: "
                   "two straight sides of 100 m and semicircle ends with a diameter of 60 m")), U(lap, "m"),
                   [U(200 + 2 * PI * 60, "m"), U(320 + PI * 60, "m"), U(200 + PI * 30, "m")],
                   "The two semicircles make one circle: 3.14 × 60 = 188.4 m. 100 + 100 + 188.4 = <b>388.4 m</b>."))
    assert lap == Dm("388.4")
    # 3 laps for 2 km
    its.append(mcq("For the Terry Fox Run, Kai wants to run at least 2 km on that track (one lap is 388.4 m). "
                   "How many full laps must he run?", "6 laps", ["5 laps", "4 laps", "7 laps"],
                   "2 km = 2000 m. 2000 ÷ 388.4 ≈ 5.15. Five laps are only 1942 m, so he needs <b>6 laps</b>."))
    assert 5 * lap < 2000 < 6 * lap
    # 4 field inside the track
    A = 100 * 60 + circ_area(30)
    its.append(mcq("The grass field inside the same track is a 100 m by 60 m rectangle with a semicircle on each end "
                   "(diameter 60 m). What is the area of the grass?" + USE, U(A, "m²"),
                   [U(6000 + 2 * circ_area(30), "m²"), U(6000 + circ_area(60), "m²"), U(6000 + circ_area(30) / 2, "m²")],
                   "Rectangle: 100 × 60 = 6000 m². Two semicircles = one circle with r = 30: 3.14 × 30 × 30 = 2826 m². "
                   "6000 + 2826 = <b>8826 m²</b>."))
    assert A == 8826
    # 5 window trim
    P = Dm("1.2") + 3 + semi_arc("1.2")
    its.append(mcq("A window at the cottage is a rectangle 1.2 m wide and 1.5 m tall with a semicircle on top. "
                   "Wood trim goes around the outside. How long is the trim?" + USE, U(P, "m"),
                   [U(Dm("4.2") + PI * Dm("1.2"), "m"), U(Dm("5.4") + semi_arc("1.2"), "m"),
                    U(Dm("4.2") + semi_arc("0.6"), "m")],
                   "Straight sides: 1.2 + 1.5 + 1.5 = 4.2 m. Curve: 3.14 × 1.2 ÷ 2 = 1.884 m. "
                   "4.2 + 1.884 = <b>6.084 m</b>."))
    assert P == Dm("6.084")
    # 6 fence cost
    P = 28 + semi_arc(8)
    cost = P * 15
    its.append(mcq("A dog run is a 10 m by 8 m rectangle with a semicircle on one 8 m side. Fencing costs $15 per metre. "
                   "How much does the fence around the outside cost?" + USE, money(cost),
                   [money((28 + PI * 8) * 15), money((36 + semi_arc(8)) * 15), money(36 * 15)],
                   "Straight sides: 10 + 10 + 8 = 28 m. Curve: 3.14 × 8 ÷ 2 = 12.56 m. Fence: 40.56 m. "
                   "40.56 × $15 = <b>$608.40</b>."))
    assert cost == Dm("608.40")
    # 7 pool cover
    A = 32 + semi_area(4)
    its.append(mcq("A backyard pool is an 8 m by 4 m rectangle with a semicircle on one 4 m end. What area does a "
                   "pool cover need to have?" + USE, U(A, "m²"),
                   [U(32 + 2 * semi_area(4), "m²"), U(32 + PI * 16 / 2, "m²"), U(32, "m²")],
                   "Rectangle: 8 × 4 = 32 m². Semicircle: r = 2, so 3.14 × 2 × 2 ÷ 2 = 6.28 m². "
                   "32 + 6.28 = <b>38.28 m²</b>."))
    assert A == Dm("38.28")
    # 8 gable wall paint
    A = 8 * 3 + Dm(8) * 3 / 2 - 2
    its.append(mcq("The end wall of a house is an 8 m by 3 m rectangle with a triangle on top (height 3 m). "
                   "It has a door 1 m by 2 m. How much wall area needs paint?", U(A, "m²"),
                   [U(24 + 24 - 2, "m²"), U(A + 2, "m²"), U(22, "m²")],
                   "Rectangle: 8 × 3 = 24 m². Triangle: ½ × 8 × 3 = 12 m². Wall: 36 m². "
                   "Take away the door (1 × 2 = 2 m²): 36 − 2 = <b>34 m²</b>."))
    assert A == 34
    # 9 paint cans
    its.append(mcq("Mateo paints two end walls of 34 m² each. One can of paint covers 10 m². How many cans must he buy?",
                   "7 cans", ["6 cans", "4 cans", "68 cans"],
                   "Total: 2 × 34 = 68 m². 68 ÷ 10 = 6.8. Six cans are not enough, so he buys <b>7 cans</b>."))
    # 10 roof shingles
    its.append(mcq("A house is 8 m wide and 10 m long. Its roof is 3 m high at the peak, and each of its two rectangular sides "
                   "is 5 m from the peak down to the edge. What area of shingles covers the whole roof?", "100 m²", ["50 m²", "60 m²", "80 m²"],
                   "Each side: 5 × 10 = 50 m². Two sides: 2 × 50 = <b>100 m²</b>. "
                   "(60 m² uses the roof height 3 m instead of the sloped length 5 m.)"))
    # 11 house volume
    V = 8 * 3 * 10 + Dm(8) * 3 / 2 * 10
    its.append(mcq("A house is 8 m wide and 10 m long. The walls are 3 m high, and the roof is a triangular prism 3 m high. "
                   "What is the volume of the house, including the attic?", U(V, "m³"),
                   [U(480, "m³"), U(240, "m³"), U(120, "m³")],
                   "Walls part: 8 × 10 × 3 = 240 m³. Attic: ½ × 8 × 3 × 10 = 120 m³. 240 + 120 = <b>360 m³</b>. "
                   "480 m³ forgets the ½ for the triangle."))
    assert V == 360
    # 12 pool volume
    V = 10 * (15 * 1 + 10 * 2)
    its.append(mcq("A pool is 10 m wide. The side view below shows the water. How many litres of water does the pool hold?"
                   + fig(pool_svg(25, 15, 1, 2, "m")), U(V * 1000, "L"),
                   [U(25 * 10 * 2 * 1000, "L"), U(Dm("1.5") * 25 * 10 * 1000, "L"), U(V * 100, "L")],
                   "Side view: 15 × 1 + 10 × 2 = 15 + 20 = 35 m². Volume: 35 × 10 = 350 m³. "
                   "1 m³ = 1000 L, so 350 × 1000 = <b>350" + NB + "000 L</b>."))
    # 13 backyard rink
    A = 12 * 6 + circ_area(3)
    V = A * Dm("0.05")
    its.append(mcq("A backyard rink is a 12 m by 6 m rectangle with a semicircle on each 6 m end. Owen floods it with "
                   "water 5 cm deep. How many litres of water does he need?" + USE, U(V * 1000, "L"),
                   [U((72 + 2 * circ_area(3)) * Dm("0.05") * 1000, "L"), U(72 * Dm("0.05") * 1000, "L"),
                    U(A * Dm("0.5") * 1000, "L")],
                   "Area: 12 × 6 + 3.14 × 3 × 3 = 72 + 28.26 = 100.26 m². 5 cm = 0.05 m. "
                   "100.26 × 0.05 = 5.013 m³ = <b>5013 L</b>."))
    assert V * 1000 == 5013
    # 14 sandbox
    V = (3 * 2 - 1) * Dm("0.3")
    its.append(mcq("An L-shaped sandbox is a 3 m by 2 m rectangle with a 1 m by 1 m corner cut out. Sand fills it "
                   "30 cm deep. What volume of sand is needed?", U(V, "m³"),
                   [U(Dm("1.8"), "m³"), U(5 * 30, "m³"), U(Dm("1.2"), "m³")],
                   "Area: 3 × 2 − 1 × 1 = 5 m². 30 cm = 0.3 m. 5 × 0.3 = <b>1.5 m³</b>."))
    assert V == Dm("1.5")
    # 15 concrete steps
    front = 30 * 20 + 30 * 40 + 30 * 60
    V = Dm(front * 100) / 1000000
    its.append(mcq("Concrete steps have 3 steps. Each step is 30 cm deep and 20 cm high, and the steps are 1 m wide. "
                   "The steps are solid concrete down to the ground. What volume of concrete is needed?", U(V, "m³"),
                   [U(Dm(90 * 60 * 100) / 1000000, "m³"), U(Dm(90 * 20 * 100) / 1000000, "m³"),
                    U(Dm(front * 100) / 100, "m³")],
                   "Side view: columns 30 × 20 + 30 × 40 + 30 × 60 = 600 + 1200 + 1800 = 3600 cm². "
                   "Volume: 3600 × 100 = 360" + NB + "000 cm³. 1 m³ = 1" + NB + "000" + NB + "000 cm³, so it is <b>0.36 m³</b>."))
    assert V == Dm("0.36")
    # 16 trough
    V = circ_area(30) * 200 / 2
    its.append(mcq("A water trough at a farm is half a cylinder with a diameter of 60 cm and a length of 2 m. "
                   "How many litres does it hold when full?" + USE, U(V / 1000, "L"),
                   [U(2 * V / 1000, "L"), U(circ_area(60) * 200 / 2 / 1000, "L"), U(V / 100, "L")],
                   "r = 30 cm and 2 m = 200 cm. Half cylinder: 3.14 × 30 × 30 × 200 ÷ 2 = 282" + NB + "600 cm³. "
                   "1000 cm³ = 1 L, so <b>282.6 L</b>."))
    assert V / 1000 == Dm("282.6")
    # 17 soup can label
    lat = 2 * PI * 4 * 11
    its.append(mcq("A soup can has a radius of 4 cm and a height of 11 cm. The paper label covers only the curved side. "
                   "What is the area of the label?" + USE, U(lat, "cm²"),
                   [U(lat + 2 * circ_area(4), "cm²"), U(2 * PI * 8 * 11, "cm²"), U(PI * 4 * 11, "cm²")],
                   "The label unrolls into a rectangle: circumference × height = 2 × 3.14 × 4 × 11 = <b>276.32 cm²</b>. "
                   "The top and bottom are not covered."))
    assert lat == Dm("276.32")
    # 18 tent
    ends = Dm("2.4") * Dm("1.6")
    SA = ends + 2 * 2 * 3
    its.append(mcq("A tent is a triangular prism 3 m long. Each triangle end has a base of 2.4 m and a height of 1.6 m, "
                   "and each sloped side is 2 m wide. The tent has no floor. How much fabric is needed?", U(SA, "m²"),
                   [U(SA + Dm("2.4") * 3, "m²"), U(2 * ends + 12, "m²"), U(ends + 2 * Dm("1.6") * 3, "m²")],
                   "Two triangles: 2 × ½ × 2.4 × 1.6 = 3.84 m². Two sloped sides: 2 × 2 × 3 = 12 m². "
                   "3.84 + 12 = <b>15.84 m²</b>."))
    assert SA == Dm("15.84")
    # 19 cake icing
    top = circ_area(15)
    sides = 2 * PI * 15 * 10 + 2 * PI * 10 * 8
    A = top + sides
    its.append(mcq("A two-layer birthday cake has a bottom layer with a radius of 15 cm and a height of 10 cm, and a top "
                   "layer with a radius of 10 cm and a height of 8 cm. Icing covers the top and the sides, but not the "
                   "bottom. What area is iced?" + USE, U(A, "cm²"),
                   [U(A + circ_area(15), "cm²"), U(A + circ_area(10), "cm²"), U(sides, "cm²")],
                   "Seen from above, the tops together make one circle of r = 15: 3.14 × 15 × 15 = 706.5 cm². "
                   "Sides: 2 × 3.14 × 15 × 10 + 2 × 3.14 × 10 × 8 = 942 + 502.4 = 1444.4 cm². "
                   "706.5 + 1444.4 = <b>2150.9 cm²</b>."))
    assert A == Dm("2150.9")
    # 20 culvert
    V = PI * (Dm("0.25") - Dm("0.16")) * 2
    its.append(mcq("A concrete culvert pipe is 2 m long. Its outside radius is 0.5 m and its inside radius is 0.4 m. "
                   "What volume of concrete is in the pipe?" + USE, U(V, "m³"),
                   [U(PI * Dm("0.01") * 2, "m³"), U(PI * Dm("0.25") * 2, "m³"), U(PI * Dm("0.41") * 2, "m³")],
                   "Outside: 3.14 × 0.5 × 0.5 × 2 = 1.57 m³. Hole: 3.14 × 0.4 × 0.4 × 2 = 1.0048 m³. "
                   "1.57 − 1.0048 = <b>0.5652 m³</b>."))
    assert V == Dm("0.5652")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: tracks, pools and houses", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>What a composite shape is</h2>"
        "<p>A <b>composite shape</b> is made of simple shapes: rectangles, triangles and semicircles. "
        "A <b>composite solid</b> is made of prisms and cylinders. To measure one, split it into parts you know, "
        "measure each part, then put the answers together.</p>"
        + table(["Part", "Perimeter piece", "Area"], [
            ["Rectangle", "the outside sides only", "l × w"],
            ["Triangle", "the outside sides only", "½ × b × h"],
            ["Semicircle", "curve = π × d ÷ 2", "π × r × r ÷ 2"],
        ])
        + "<h2>Perimeter: only the outside edge</h2>"
        "<p>Walk around the outside of the shape and add every length. A line where two parts meet is inside the shape, "
        "so it is <b>not</b> part of the perimeter. A semicircle adds only half a circle: π × d ÷ 2.</p>"
        "<figure class='sn-fig'>" + tomb_svg(10, 12, "cm") +
        "<figcaption>The dashed line is inside the shape, so it is not counted.</figcaption></figure>"
        + ex("Example 1", "Find the perimeter of the shape above. Use π ≈ 3.14.",
             "Curve: 3.14 × 10 ÷ 2 = 15.7 cm. Straight sides: 10 + 12 + 12 = 34 cm. 34 + 15.7 = 49.7 cm.", "49.7 cm")
        + "<h2>Area: add or subtract the parts</h2>"
        "<p>Split the shape into rectangles, triangles and semicircles. Add their areas. If a part is cut out, "
        "subtract it. Often the fastest way is “big rectangle minus the missing corner.”</p>"
        "<figure class='sn-fig'>" + lshape_svg(11, 8, 5, 3, "cm") +
        "<figcaption>Whole rectangle 11 × 8 = 88 cm², minus the corner 5 × 3 = 15 cm²: 73 cm².</figcaption></figure>"
        + ex("Example 2", "Find the area of the shape in Example 1.",
             "Rectangle: 10 × 12 = 120 cm². Semicircle: r = 5, so 3.14 × 5 × 5 ÷ 2 = 39.25 cm². 120 + 39.25.",
             "159.25 cm²")
        + "<h2>Volume of composite solids</h2>"
        "<p>Add the volumes of the parts, or subtract a part that is removed. For any prism, "
        "<b>V = area of the front (base) × length</b>, even when the front is a composite shape.</p>"
        "<figure class='sn-fig'>" + house_svg(8, 5, 3, 10, "m") +
        "<figcaption>Front: 8 × 5 + ½ × 8 × 3 = 40 + 12 = 52 m². Volume: 52 × 10 = 520 m³.</figcaption></figure>"
        + ex("Example 3", "A cylinder (r = 3 cm, h = 5 cm) sits on a 10 cm × 10 cm × 4 cm box. Find the total volume.",
             "Box: 10 × 10 × 4 = 400 cm³. Cylinder: 3.14 × 3 × 3 × 5 = 141.3 cm³. 400 + 141.3.", "541.3 cm³")
        + "<h2>Surface area of composite solids</h2>"
        "<p>Surface area is the total area of all the outside faces. When two solids are joined, the faces that touch "
        "are hidden. Take the touching area away from <b>both</b> solids.</p>"
        "<figure class='sn-fig'>" + cubebox_svg(10, 8, 4, 4, "cm") +
        "<figcaption>Box 304 cm² + cube 96 cm² − 2 × 16 cm² (the hidden squares) = 368 cm².</figcaption></figure>"
        "<p>For a cylinder, the curved side unrolls into a rectangle: <b>2πr × h</b>. Add the two circles: "
        "SA = 2πr² + 2πrh.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the line where two parts meet in the perimeter", "Count only the outside edge"],
            ["Using a full circle (π × d) for a semicircle", "Halve it: π × d ÷ 2 and π × r × r ÷ 2"],
            ["Using the diameter as r", "Halve the diameter first: d = 10, r = 5"],
            ["Forgetting ½ for a triangle", "Triangle area = ½ × b × h"],
            ["Using the sloped side as the height of a triangle", "Use the height, at a right angle to the base"],
            ["Adding the surface areas of two joined solids", "Subtract the touching area twice"],
        ])
    )


FAQ = [
    {"q": "How do you find the perimeter of a shape with a semicircle?",
     "a": "Add the straight outside sides and half of the circle’s circumference, π × d ÷ 2. Do not count the diameter "
          "where the semicircle joins the rectangle, because it is inside the shape."},
    {"q": "How do you find the area of a composite shape in Grade 8?",
     "a": "Split the shape into rectangles, triangles and semicircles, find each area, then add them (or subtract a part "
          "that is cut out). For a semicircle use π × r × r ÷ 2 with π ≈ 3.14."},
    {"q": "Where is composite area and volume in the Ontario Grade 8 math curriculum?",
     "a": "It is in Spatial Sense, expectation E2.3: students solve problems with the perimeter, circumference, area, "
          "volume and surface area of composite two-dimensional shapes and three-dimensional objects."},
    {"q": "How do you find the surface area of two solids that are joined together?",
     "a": "Add the surface areas of both solids, then subtract the area where they touch twice, once for each solid. "
          "Those faces are hidden inside the new solid."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48818)
    sets = [set_perimeter(), set_area(), set_volume(), set_surface(), set_story()]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "composite-area-and-volume", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Composite Area and Volume: Shapes with Semicircles, Prisms and Cylinders",
        "seo_title": "Grade 8 Composite Area and Volume Worksheets: Perimeter, Area, Volume and Surface Area, Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Composite area and volume",
        "domain": "Spatial Sense",
        "standard_code": "Grade 8: E2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve problems involving the perimeter, circumference, area, volume, and surface area of composite two-dimensional shapes and three-dimensional objects, using appropriate formulas",
        "meta_desc": "Free Grade 8 math worksheets on composite shapes and solids for the Ontario curriculum: perimeter with semicircles, area of L-shapes and house shapes, volume of composite prisms and cylinders, and surface area of joined solids, with running track, pool and house problems. 100 questions with an answer key.",
        "key_big": "Split a composite shape or solid into simple parts, find each part, then add (or subtract a part that is cut out).",
        "key_sub": "Perimeter counts only the outside edge, not the line where two parts meet. A semicircle is half a circle: curve π × d ÷ 2, area π × r × r ÷ 2 (π ≈ 3.14). Faces that touch are not part of the surface area.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(side view of a pool|running track)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
