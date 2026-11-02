# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Rectangles and squares (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p4_rectangles_squares.py
Properties of rectangle and square, excluding diagonal properties: identify them (a square is a special
rectangle, a turned square is still a square), 4 right angles, opposite sides equal and parallel,
find unknown sides, find unknown angles when a corner is split by a line, and word problems with bar models.
Every shape is drawn from its own corner points; right-angle marks, equal-side ticks and the name of the
shape are worked out in code from the same points. Labels never touch each other, and no line runs
through a label (checked in Canvas). Every answer is computed in code; wrong answers are real mistakes
(180° − x instead of 90° − x, perimeter ÷ 2 for the side of a square, one length + one breadth for the
perimeter, a turned square called a “diamond”, “a rectangle has 4 equal sides”, diagonal properties).
Singapore style: British spelling, ∠ABC, AB // DC, AB ⊥ BC, m and cm. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
LINE = "#1f4e79"
FILL = "#cfe0f1"
SHADE = "#f2b8a2"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ question helpers
NUMRX = re.compile(r"^(\d+(?:\.\d+)?)( ?(cm|m|°))?$")


def mcq(q, correct, wrong, e):
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4 and len(set(ch)) == 4, (q, ch)
    vals = [F(m.group(1)) for m in (NUMRX.match(c) for c in ch) if m]
    assert len(set(vals)) == len(vals), (q, ch)
    for v in vals:
        assert v > 0, (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def D(x):
    return "%s°" % x


def CM(x, u="cm"):
    x = F(x)
    s = str(x.numerator) if x.denominator == 1 else ("%.2f" % float(x)).rstrip("0").rstrip(".")
    return "%s %s" % (s, u)


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
    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ geometry (screen coordinates, y down)
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def unit(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def ang(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1]))))


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count(".") * 0.6 - t.count("°") * 0.4) * fs * 0.6


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def quad_facts(pts):
    """Right angles, equal sides and the name of a quadrilateral, from its points."""
    n = 4
    L = [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]
    A = []
    for i in range(n):
        u1, u2 = unit(sub(pts[i - 1], pts[i])), unit(sub(pts[(i + 1) % n], pts[i]))
        A.append(ang(u1, u2))
    assert abs(sum(A) - 360) < 1e-6
    rights = [i for i in range(n) if abs(A[i] - 90) < 1e-6]
    for a in A:
        assert abs(a - 90) < 1e-6 or abs(a - 90) >= 12, ("almost a right angle", A)
    eqs = max(L) - min(L) < 1e-6 * max(L)
    if len(rights) == 4:
        name = "square" if eqs else "rectangle"
    else:
        name = "other"
    return {"L": L, "A": A, "rights": rights, "eqs": eqs, "name": name}


def tick_groups(L):
    gs = []
    for i, v in enumerate(L):
        for g in gs:
            if abs(L[g[0]] - v) < 1e-6 * v:
                g.append(i)
                break
        else:
            gs.append([i])
    for g1 in gs:
        for g2 in gs:
            if g1 is not g2:
                a, b = L[g1[0]], L[g2[0]]
                assert abs(a - b) / max(a, b) > 0.1, ("sides look equal", L)
    out, k = {}, 0
    for g in gs:
        if len(g) < 2:
            continue
        k += 1
        for i in g:
            out[i] = k
    return out


# ------------------------------------------------------------ canvas
class Canvas:
    """Shapes and text (y down); tracks the bounding box and writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill=FILL, sw=2.6, col=LINE, track=True):
        self.el.append(("p", pts, fill, sw, col))
        if track:
            self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=INK, track=True):
        self.el.append(("l", a, b, dashed, sw, col))
        if track:
            self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, sw=2, col=INK):
        self.el.append(("o", pts, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK, check=True):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        if check:
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

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "o":
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' "
                         "stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[3], e[2]))
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

    def svg(self, label, pad=5, minw=0):
        self.check()
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W < minw:
            ox -= (minw - W) / 2.0
            W = minw
        if W == H:
            W += 1                                         # keep figures out of the larger 'square' print size
        return svg_wrap(W, H, self.body(ox, oy), label)


# ------------------------------------------------------------ drawing a quadrilateral with its marks
def right_mark(cv, pts, i, k=10):
    v = pts[i]
    u1, u2 = unit(sub(pts[i - 1], v)), unit(sub(pts[(i + 1) % len(pts)], v))
    q1 = add(v, u1, k)
    q2 = add(q1, u2, k)
    q3 = add(v, u2, k)
    cv.line(q1, q2, sw=1.6)
    cv.line(q2, q3, sw=1.6)


def ticks(cv, a, b, cnt):
    d = unit(sub(b, a))
    nr = (-d[1], d[0])
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    for j in range(cnt):
        o = (j - (cnt - 1) / 2.0) * 5
        c = add(m, d, o)
        cv.line(add(c, nr, -6), add(c, nr, 6), sw=2)


def out_label(cv, a, b, t, cen, fs=16, gap=13):
    """Label for segment ab, outside (away from the point cen)."""
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    d = unit(sub(b, a))
    nr = (-d[1], d[0])
    if (m[0] - cen[0]) * nr[0] + (m[1] - cen[1]) * nr[1] < 0:
        nr = (-nr[0], -nr[1])
    off = gap + abs(nr[0]) * tw(t, fs) / 2 + abs(nr[1]) * fs / 2
    p = add(m, nr, off)
    cv.text(p[0], p[1], t, fs)


def in_label(cv, a, b, t, cen, fs=16, gap=7):
    """Label for segment ab, on the side of cen (inside the shape)."""
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    d = unit(sub(b, a))
    nr = (-d[1], d[0])
    if (m[0] - cen[0]) * nr[0] + (m[1] - cen[1]) * nr[1] > 0:
        nr = (-nr[0], -nr[1])
    off = gap + abs(nr[0]) * tw(t, fs) / 2 + abs(nr[1]) * fs / 2
    p = add(m, nr, off)
    cv.text(p[0], p[1], t, fs)


def letter(cv, pts, i, t, cen=None, dist=13, fs=16):
    v = pts[i]
    n = len(pts)
    u1, u2 = unit(sub(pts[i - 1], v)), unit(sub(pts[(i + 1) % n], v))
    b = unit((-(u1[0] + u2[0]), -(u1[1] + u2[1])))
    p = add(v, b, dist)
    cv.text(p[0], p[1], t, fs)


def point_letter(cv, p, side_a, side_b, t, cen, dist=18, fs=16):
    """Letter for a point p on side (side_a, side_b), outside the shape."""
    d = unit(sub(side_b, side_a))
    nr = (-d[1], d[0])
    if (p[0] - cen[0]) * nr[0] + (p[1] - cen[1]) * nr[1] < 0:
        nr = (-nr[0], -nr[1])
    q = add(p, nr, dist)
    cv.text(q[0], q[1], t, fs)


def draw_quad(cv, pts, marks=True, side_text=None, letters=None, fill=FILL, fs=16):
    f = quad_facts(pts)
    cv.poly(pts, fill)
    cen = centroid(pts)
    if marks:
        for i in f["rights"]:
            right_mark(cv, pts, i)
        for i, k in tick_groups(f["L"]).items():
            ticks(cv, pts[i], pts[(i + 1) % 4], k)
    for i, t in (side_text or {}).items():
        out_label(cv, pts[i], pts[(i + 1) % 4], t, cen, fs)
    if letters:
        for i, t in enumerate(letters):
            letter(cv, pts, i, t, fs=fs)
    return f


# ------------------------------------------------------------ shapes
def walk(lens, dirs):
    p = [(0.0, 0.0)]
    for L, d in zip(lens, dirs):
        x, y = p[-1]
        p.append((x + L * math.cos(math.radians(d)), y + L * math.sin(math.radians(d))))
    assert math.hypot(*sub(p[-1], p[0])) < 1e-6, p[-1]
    return p[:-1]


def rect_pts(w, h):
    return [(0.0, 0.0), (float(w), 0.0), (float(w), float(h)), (0.0, float(h))]


SHAPES = {
    "square": rect_pts(100, 100),
    "rect": rect_pts(160, 90),
    "tall": rect_pts(60, 140),
    "near": rect_pts(140, 120),
    "rhombus": walk([100] * 4, [0, 60, 180, 240]),
    "para": walk([140, 80, 140, 80], [0, 62, 180, 242]),
    "rtrap": [(0, 0), (90, 0), (150, 90), (0, 90)],
}
NAME = {"square": "square", "rect": "rectangle", "tall": "rectangle", "near": "rectangle"}
for _k, _p in SHAPES.items():
    assert quad_facts(_p)["name"] == NAME.get(_k, "other"), _k


def placed(key, rot, bw, bh, cx, cy):
    pts = [rot_pt(p, rot) for p in SHAPES[key]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (x - mx) * k, cy + (y - my) * k) for x, y in pts]


def shape_svg(key, rot=0, bw=150, bh=96, side_text=None, label="a four-sided shape"):
    cv = Canvas()
    pts = placed(key, rot, bw, bh, 0, 0)
    draw_quad(cv, pts, side_text=side_text)
    return cv.svg(label)


CELL = 124


def grid_svg(items, label="four shapes labelled A to D"):
    """2 x 2 grid of shapes labelled A-D. items: (key, rot)."""
    cv = Canvas()
    W = H = 2 * CELL
    cv.line((CELL, 4), (CELL, H - 4), sw=1, col=GREY, track=False)
    cv.line((4, CELL), (W - 4, CELL), sw=1, col=GREY, track=False)
    for k, (key, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        pts = placed(key, rot, 78, 78, x0 + 70, y0 + 66)
        for x, y in pts:
            assert x0 + 22 <= x <= x0 + CELL - 6 and y0 + 6 <= y <= y0 + CELL - 6, (key, rot)
        draw_quad(cv, pts)
        cv.text(x0 + 12, y0 + 16, "ABCD"[k], 18)
    cv.grow(0, 0, W, H)
    return cv.svg(label, pad=0)


def strip_svg(items, label, cw=150, bw=100, bh=80, fs=15):
    """A row of shapes with a caption under each. items: (key, rot, caption)."""
    cv = Canvas()
    top = bh + 24
    for k, (key, rot, cap) in enumerate(items):
        pts = placed(key, rot, bw, bh, k * cw + cw / 2.0, top / 2.0)
        draw_quad(cv, pts)
        assert tw(cap, fs) <= cw - 6, cap
        cv.text(k * cw + cw / 2.0, top + fs, cap, fs)
    return cv.svg(label)


# ------------------------------------------------------------ labelled rectangles (ABCD clockwise from top left)
def abcd_svg(w, h, names="ABCD", sides=None, rot=0, marks=True, label=None, scale=1.0):
    pts = [rot_pt((x * scale, y * scale), rot) for x, y in rect_pts(w, h)]
    cv = Canvas()
    draw_quad(cv, pts, marks=marks, side_text=sides, letters=list(names))
    return cv.svg(label or ("%s %s" % ("square" if w == h else "rectangle", names)))


def arc_between(v, u1, u2, r, n=16):
    a1, a2 = math.atan2(u1[1], u1[0]), math.atan2(u2[1], u2[0])
    d = a2 - a1
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    return [(v[0] + r * math.cos(a1 + d * i / n), v[1] + r * math.sin(a1 + d * i / n)) for i in range(n + 1)]


def ray_hit(pts, v_i, d):
    """Where the ray from corner v_i in direction d leaves the rectangle: (point, side index)."""
    v = pts[v_i]
    best = None
    for s in range(4):
        if s == v_i or (s + 1) % 4 == v_i:
            continue
        a, b = pts[s], pts[(s + 1) % 4]
        e = sub(b, a)
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = sub(a, v)
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-9 and -1e-9 <= u <= 1 + 1e-9:
            if best is None or t < best[0]:
                best = (t, add(v, d, t), s)
    assert best is not None
    _, p, s = best
    # keep E away from the corners so the letters do not crowd
    for c in pts:
        assert math.hypot(*sub(p, c)) > 26, ("point too near a corner", p)
    return p, s


def angle_label(cv, v, u1, u2, t, fs=16):
    h = math.radians(ang(u1, u2) / 2)
    b = unit(add(u1, u2))
    d = max(46, (tw(t, fs) / 2 + 9) / math.sin(h))
    p = add(v, b, d)
    cv.text(p[0], p[1], t, fs)


def split_svg(w, h, corner, splits, labels, names="ABCD", pnames=("E", "F"), square_marks=False, label=None, scale=1.0, rot=0):
    """Rectangle with lines from one corner. splits: angles (degrees) measured from the side towards the
    NEXT corner, running round the corner. labels: text for each part (None = arc only)."""
    pts = [rot_pt((x * scale, y * scale), rot) for x, y in rect_pts(w, h)]
    cv = Canvas()
    f = draw_quad(cv, pts, marks=False, letters=list(names))
    if square_marks:
        for i in range(4):
            if i != corner:
                right_mark(cv, pts, i)
        for i in range(4):
            ticks(cv, pts[i], pts[(i + 1) % 4], 1)
    else:
        for i in range(4):
            if i != corner:
                right_mark(cv, pts, i)
    v = pts[corner]
    un, up = unit(sub(pts[(corner + 1) % 4], v)), unit(sub(pts[corner - 1], v))
    acc, rays = 0, [un]
    cen = centroid(pts)
    hits = []
    for k, s in enumerate(splits[:-1]):
        acc += s
        t = math.radians(acc)
        d = (un[0] * math.cos(t) + up[0] * math.sin(t), un[1] * math.cos(t) + up[1] * math.sin(t))
        p, side = ray_hit(pts, corner, d)
        cv.line(v, p, sw=2.4, col=LINE)
        point_letter(cv, p, pts[side], pts[(side + 1) % 4], pnames[k], cen)
        rays.append(d)
        hits.append((p, side))
    assert acc + splits[-1] == 90
    rays.append(up)
    for k in range(len(splits)):
        r = 24 + 4 * (k % 2)
        cv.pline(arc_between(v, rays[k], rays[k + 1], r), sw=1.8, col=RED if labels[k] == "?" else INK)
        if labels[k]:
            angle_label(cv, v, rays[k], rays[k + 1], labels[k])
    return cv.svg(label or "rectangle %s with a line from corner %s" % (names, names[corner])), hits


def angle_svg_two(w, h, a_split, d_split, label):
    """Rectangle ABCD, lines from A and from D to the same point E on BC."""
    pts = rect_pts(w, h)
    cv = Canvas()
    draw_quad(cv, pts, marks=False, letters=list("ABCD"))
    right_mark(cv, pts, 1)
    right_mark(cv, pts, 2)
    A, B, C, Dd = pts
    # E on BC with angle BAE = a_split
    ey = w * math.tan(math.radians(a_split))
    E = (w, ey)
    assert 30 < ey < h - 30
    d_ang = math.degrees(math.atan2(h - ey, w))           # angle EDC
    assert abs(d_ang - d_split) < 1e-6, d_ang
    cen = centroid(pts)
    cv.line(A, E, col=LINE)
    cv.line(Dd, E, col=LINE)
    point_letter(cv, E, B, C, "E", cen)
    uAB, uAE, uAD = unit(sub(B, A)), unit(sub(E, A)), unit(sub(Dd, A))
    uDC, uDE, uDA = unit(sub(C, Dd)), unit(sub(E, Dd)), unit(sub(A, Dd))
    cv.pline(arc_between(A, uAB, uAE, 24), sw=1.8)
    angle_label(cv, A, uAB, uAE, D(a_split))
    cv.pline(arc_between(A, uAE, uAD, 28), sw=1.8)
    cv.pline(arc_between(Dd, uDC, uDE, 24), sw=1.8)
    angle_label(cv, Dd, uDC, uDE, D(d_split))
    cv.pline(arc_between(Dd, uDE, uDA, 28), sw=1.8, col=RED)
    return cv.svg(label)


# ------------------------------------------------------------ other pictures
def squares_row_svg(n, side, below=None, label=None, each=None):
    """n equal squares in a row (one rectangle)."""
    cv = Canvas()
    s = 60
    for i in range(n):
        cv.poly([(i * s, 0), ((i + 1) * s, 0), ((i + 1) * s, s), (i * s, s)])
    for i in range(4):
        right_mark(cv, [(0, 0), (n * s, 0), (n * s, s), (0, s)], i)
    cen = (n * s / 2.0, s / 2.0)
    if below:
        out_label(cv, (0, s), (n * s, s), below, cen)
    if each:
        out_label(cv, (0, 0), (s, 0), each, cen)
    return cv.svg(label or "%d equal squares in a row" % n)


def square_rect_svg(sq, bw, label):
    """Square ABCD (side sq) with rectangle BEFC joined on its right. Lengths in cm, drawn 12 px per cm."""
    k = 12
    S, Bw = sq * k, bw * k
    A, B, C, Dd = (0, 0), (S, 0), (S, S), (0, S)
    E, Fp = (S + Bw, 0), (S + Bw, S)
    cv = Canvas()
    cv.poly([A, B, C, Dd])
    cv.poly([B, E, Fp, C], fill=PARTFILL)
    for p, q in [(A, B), (B, C), (C, Dd), (Dd, A)]:
        ticks(cv, p, q, 1)
    cen = (S / 2.0, S / 2.0)
    for t, p, d in [("A", A, (-1, -1)), ("D", Dd, (-1, 1)), ("E", E, (1, -1)), ("F", Fp, (1, 1))]:
        q = add(p, unit(d), 14)
        cv.text(q[0], q[1], t)
    cv.text(S, -13, "B")
    cv.text(S, S + 13, "C")
    out_label(cv, A, Dd, CM(sq), cen)
    out_label(cv, B, E, CM(bw), (S + Bw / 2.0, S / 2.0), gap=22)
    for i in range(4):
        right_mark(cv, [A, E, Fp, Dd], i)
    return cv.svg(label)


def split_rect_svg(w, h, cut, names, lens, label, k=10):
    """Rectangle ABCD with a line EF from AB to DC at distance cut from A. lens: dict of (p,q) -> text."""
    W, H, X = w * k, h * k, cut * k
    A, B, C, Dd = (0, 0), (W, 0), (W, H), (0, H)
    E, Fp = (X, 0), (X, H)
    cv = Canvas()
    cv.poly([A, E, Fp, Dd])
    cv.poly([E, B, C, Fp], fill=PARTFILL)
    pts = {"A": A, "B": B, "C": C, "D": Dd, "E": E, "F": Fp}
    for i in range(4):
        right_mark(cv, [A, B, C, Dd], i)
    for t, d in [("A", (-1, -1)), ("B", (1, -1)), ("C", (1, 1)), ("D", (-1, 1))]:
        q = add(pts[t], unit(d), 14)
        cv.text(q[0], q[1], names.get(t, t))
    cv.text(X, -13, "E")
    cv.text(X, H + 13, "F")
    cen = (W / 2.0, H / 2.0)
    for (p, q), t in lens.items():
        a, b = pts[p], pts[q]
        if (p, q) in (("E", "F"),):
            in_label(cv, a, b, t, (X - 1, H / 2.0))
        else:
            out_label(cv, a, b, t, cen, gap=28 if a[1] == b[1] else 10)
    return cv.svg(label)


def point_on_side_svg(w, h, at, lens, label, k=10):
    """Rectangle ABCD with a point E on AB (or on DC) at distance at from A (or D). lens: dict seg -> text."""
    W, H = w * k, h * k
    A, B, C, Dd = (0, 0), (W, 0), (W, H), (0, H)
    side, dist = at
    E = (dist * k, 0) if side == "AB" else (dist * k, H)
    cv = Canvas()
    cv.poly([A, B, C, Dd])
    pts = {"A": A, "B": B, "C": C, "D": Dd, "E": E}
    for i in range(4):
        right_mark(cv, [A, B, C, Dd], i)
    for t, d in [("A", (-1, -1)), ("B", (1, -1)), ("C", (1, 1)), ("D", (-1, 1))]:
        q = add(pts[t], unit(d), 14)
        cv.text(q[0], q[1], t)
    cv.line(add(E, (0, -6 if side == "AB" else 6)), add(E, (0, 6 if side == "AB" else -6)), sw=2.4)
    cv.text(E[0], E[1] + (-18 if side == "AB" else 18), "E")
    cen = (W / 2.0, H / 2.0)
    for (p, q), t in lens.items():
        a, b = pts[p], pts[q]
        horiz = abs(a[1] - b[1]) < 1e-9
        if horiz:
            y = a[1]
            out = -1 if y == 0 else 1
            # put labels on the far side of the letters: lift them above/below the letter row
            m = ((a[0] + b[0]) / 2.0, y + out * 30)
            cv.text(m[0], m[1], t)
        else:
            out_label(cv, a, b, t, cen)
    return cv.svg(label)


def frame_svg():
    """A square photo frame hung on one corner (a turned square)."""
    cv = Canvas()
    pts = [rot_pt(p, 45) for p in rect_pts(80, 80)]
    pts = [(x - 0, y) for x, y in pts]
    draw_quad(cv, pts, fill="#f3e2c0")
    top = min(pts, key=lambda p: p[1])
    cv.line(add(top, (0, -2)), (top[0], top[1] - 22), sw=2, col=INK, track=False)
    cv.pline([(top[0] - 4, top[1] - 26), (top[0] + 4, top[1] - 26), (top[0] + 4, top[1] - 18), (top[0] - 4, top[1] - 18),
              (top[0] - 4, top[1] - 26)], sw=2, col=INK)
    return cv.svg("a square photo frame hung on a nail by one corner")


def door_svg(w, h, a_top, label):
    """A rectangular gate with a support bar from the top-left corner; a_top is the angle with the top edge."""
    pts = rect_pts(w, h)
    cv = Canvas()
    draw_quad(cv, pts, marks=False, fill="#e8dcc8")
    for i in (1, 2, 3):
        right_mark(cv, pts, i)
    v = pts[0]
    un, ud = (1.0, 0.0), (0.0, 1.0)
    t = math.radians(a_top)
    d = (math.cos(t), math.sin(t))
    p, side = ray_hit(pts, 0, d)
    cv.line(v, p, sw=4, col="#7a4b1e")
    cv.pline(arc_between(v, un, d, 24), sw=1.8)
    angle_label(cv, v, un, d, D(a_top))
    cv.pline(arc_between(v, d, ud, 28), sw=1.8, col=RED)
    return cv.svg(label)


# ------------------------------------------------------------ bar models
def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def bar_model(rows, total_lab, label, UW=60):
    """rows: (name, units, extra) where extra is (text, width in units) or None. Unit cells drawn equal.
    A bracket on the right spans both rows: total_lab (length + breadth). '?' cells are red."""
    LW = int(max(tw(r[0], 16) for r in rows)) + 14
    X0, TOP, BH, GAP = 4, 6, 34, 14
    x0 = X0 + LW
    o = []
    maxx = 0
    for i, (nm, n, cell, extra) in enumerate(rows):
        y = TOP + i * (BH + GAP)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        for j in range(n):
            o.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + j * UW, y, UW, BH, PARTFILL if i == 0 else HEADFILL, GREEN))
        if cell:
            assert tw(cell, 16) <= UW - 6
            o.append(text(x0 + UW / 2.0, y + BH / 2.0 + 6, cell, 16, col=RED if cell == "?" else INK))
        x = x0 + n * UW
        if extra:
            et, ew = extra
            wpx = ew * UW
            assert tw(et, 16) <= wpx - 6, (et, wpx)
            o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                     % (x, y, wpx, BH, GREEN))
            o.append(text(x + wpx / 2.0, y + BH / 2.0 + 6, et, 16, col=RED if et == "?" else INK))
            x += wpx
        maxx = max(maxx, x)
    yb = TOP + len(rows) * (BH + GAP) - GAP
    bx = maxx + 12
    o.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
             % (bx - 7, TOP, bx, TOP, bx, yb, bx - 7, yb, INK))
    o.append(text(bx + 8, (TOP + yb) / 2.0 + 6, total_lab, 16, anchor="start", col=RED if total_lab == "?" else INK))
    W = int(bx + 8 + tw(total_lab, 16) + 8)
    H = yb + 6
    return svg_wrap(W, H, "".join(o), "bar model: " + label)


# ------------------------------------------------------------ set 1: rectangle, square or neither?
SQ_A, RE_A, NE_A, SR_A = ("a square", "a rectangle, but not a square", "neither a rectangle nor a square",
                          "a square, but not a rectangle")
NAMES4 = [SQ_A, RE_A, NE_A, SR_A]


def ans_for(key):
    return {"square": SQ_A, "rectangle": RE_A}.get(quad_facts(SHAPES[key])["name"], NE_A)


def set_identify(rnd, pos, Pp):
    its = []
    ask = "The marks show right angles and equal sides. What is this shape?"
    plan = [
        ("square", 0, None, "It has 4 right angles and 4 equal sides, so it is a square. (A square is also a rectangle.)"),
        ("rect", 0, None, "It has 4 right angles. Opposite sides are equal, but the long sides and short sides are different. "
                          "It is a rectangle, but not a square."),
        ("square", 45, None, "It stands on a corner, but it still has 4 right angles and 4 equal sides. It is a square. "
                             "Some people call it a “diamond”, but turning a shape does not change it."),
        ("rhombus", 0, None, "Its 4 sides are equal, but it has no right angles. A square must have 4 right angles, so this is "
                             "neither a rectangle nor a square."),
        ("para", 0, None, "Opposite sides are equal and parallel, but there are no right angles. It is neither a rectangle "
                          "nor a square."),
        ("tall", 0, None, "It has 4 right angles, and the long sides are different from the short sides. Standing up tall "
                          "does not matter: it is a rectangle, but not a square."),
        ("rect", 25, None, "It is turned, but it still has 4 right angles and 2 pairs of equal sides. It is a rectangle, "
                           "but not a square."),
        ("rtrap", 0, None, "Only 2 of its angles are right angles, and only 1 pair of sides is parallel. It is neither a "
                           "rectangle nor a square."),
        ("square", 20, None, "It is turned a little, but it has 4 right angles and 4 equal sides. It is a square."),
        ("near", 0, {0: "7 cm", 1: "6 cm"}, "It looks almost like a square, but the sides are 7 cm and 6 cm. The sides are not "
                                             "all equal, so it is a rectangle, but not a square."),
        ("rhombus", 30, None, "It stands on a corner like a turned square, but its angles are not right angles. It is neither "
                              "a rectangle nor a square."),
    ]
    for key, rot, st, e in plan:
        a = ans_for(key)
        its.append(mcq(fig(shape_svg(key, rot, side_text=st)) + ask, a, [x for x in NAMES4 if x != a], e))
    its.append(mcq("Is every square a rectangle?", "Yes, it has 4 right angles and opposite sides equal",
                   ["No, a rectangle must have 2 long sides and 2 short sides", "No, a square has no right angles",
                    "Only when the square is not turned"],
                   "A rectangle has 4 right angles and opposite sides equal. A square has all of this, so a square is a special rectangle."))
    its.append(mcq("Is every rectangle a square?", "No, its 4 sides may not all be equal",
                   ["Yes, it has 4 right angles", "Yes, its opposite sides are equal", "No, a rectangle has no right angles"],
                   "A square needs 4 equal sides. A rectangle such as 9 cm by 4 cm has 4 right angles but its sides are not all equal."))
    its.append(mcq("A shape has 4 right angles. All its sides are 8 cm. What is it?", SQ_A, [RE_A, NE_A, SR_A],
                   "4 right angles and 4 equal sides make a square."))
    its.append(mcq("A shape has 4 right angles. Two sides are 9 cm and two sides are 4 cm. What is it?", RE_A, [SQ_A, NE_A, SR_A],
                   "4 right angles make a rectangle. The sides are not all equal, so it is not a square."))
    its.append(mcq("A shape has 4 sides of 5 cm, but it has no right angles. What is it?", NE_A, [SQ_A, RE_A, SR_A],
                   "Equal sides are not enough. A square and a rectangle must have 4 right angles."))
    p = pos.next()
    cells = [("rect", 0), ("rhombus", 0), ("para", 0)]
    cells.insert(p, ("square", 40))
    its.append(mcq_fixed(fig(grid_svg(cells)) + "Which shape is a square?", list("ABCD"), "ABCD"[p],
                         "%s has 4 right angles and 4 equal sides. It is turned, but it is still a square. The rhombus has "
                         "equal sides but no right angles." % "ABCD"[p]))
    p = pos.next()
    cells = [("square", 0), ("rect", 20), ("tall", 0)]
    cells.insert(p, ("para", 0))
    its.append(mcq_fixed(fig(grid_svg(cells)) + "Which shape is NOT a rectangle?", list("ABCD"), "ABCD"[p],
                         "%s has no right angles, so it is not a rectangle. The square is a rectangle too, and the turned "
                         "rectangle is still a rectangle." % "ABCD"[p]))
    p = pos.next()
    cells = [("square", 0), ("rhombus", 30), ("square", 30)]
    cells.insert(p, ("rect", 0))
    its.append(mcq_fixed(fig(grid_svg(cells)) + "Which shape is a rectangle, but not a square?", list("ABCD"), "ABCD"[p],
                         "%s has 4 right angles, but its long and short sides are different. Two of the others are squares, and "
                         "the rhombus has no right angles." % "ABCD"[p]))
    n, he, his = Pp.next()
    its.append(mcq("%s turns a square card so that it stands on one corner. What shape is the card now?" % n,
                   "still a square", ["a diamond, not a square", "a rectangle, but not a square", "a triangle"],
                   "Turning a shape does not change its sides or angles. It still has 4 equal sides and 4 right angles."))
    assert len(its) == 20, len(its)
    return {"title": "Rectangle, square or neither?", "items": its}


# ------------------------------------------------------------ set 2: properties
def set_properties(rnd, pos, Pp):
    its = []
    R = fig(abcd_svg(170, 96))
    S = fig(abcd_svg(110, 110, names="PQRS"))
    its.append(mcq("How many right angles does a rectangle have?", 4, [2, 1, 3],
                   "Every corner of a rectangle is a right angle (90°), so it has 4 right angles."))
    its.append(mcq(R + "ABCD is a rectangle. Which side is parallel to AB?", "DC", ["BC", "AD", "AC"],
                   "In a rectangle, opposite sides are parallel. The side opposite AB is DC, so AB // DC."))
    its.append(mcq(R + "ABCD is a rectangle. Which side is equal in length to AD?", "BC", ["AB", "DC", "BD"],
                   "Opposite sides of a rectangle are equal. AD and BC are opposite each other, so AD = BC."))
    its.append(mcq(R + "ABCD is a rectangle. Which two sides are perpendicular?", "AB and BC",
                   ["AB and DC", "AD and BC", "AC and BD"],
                   "Sides that meet at a right angle are perpendicular. AB and BC meet at B, so AB ⊥ BC. AB and DC are parallel."))
    its.append(mcq(R + "ABCD is a rectangle. Which statement is true?", "AB // DC", ["AB // BC", "AB ⊥ DC", "AD // AB"],
                   "AB and DC are opposite sides, so they are parallel: AB // DC. AB and BC meet at a right angle, so they are not parallel."))
    its.append(mcq(R + "ABCD is a rectangle. Which statement is true?", "AD ⊥ DC", ["AD // DC", "AD ⊥ BC", "AB ⊥ DC"],
                   "AD and DC meet at D, and ∠ADC = 90°, so AD ⊥ DC. AD and BC are opposite sides, so they are parallel."))
    its.append(mcq(S + "PQRS is a square. Which sides are equal to PQ?", "QR, RS and SP",
                   ["RS only", "QR only", "PR and QS"],
                   "All 4 sides of a square are equal, so QR, RS and SP are all equal to PQ."))
    its.append(mcq("How many pairs of parallel sides does a square have?", 2, [1, 4, 3],
                   "A square has 2 pairs of opposite sides. Each pair is parallel, so there are 2 pairs."))
    its.append(mcq("What is the size of each angle of a square?", D(90), [D(45), D(180), D(360)],
                   "Every angle of a square is a right angle, and a right angle is 90°."))
    its.append(mcq("What do the 4 angles of a rectangle add up to?", D(360), [D(180), D(90), D(400)],
                   "There are 4 right angles: 90° + 90° + 90° + 90° = 360°."))
    its.append(mcq("Which is true about every rectangle?", "It has 4 right angles",
                   ["All 4 sides are equal", "It has only 1 pair of parallel sides", "It has 2 right angles"],
                   "Every rectangle has 4 right angles, and its opposite sides are equal and parallel. Only a square has 4 equal sides."))
    its.append(mcq("Which is NOT true about every rectangle?", "All 4 sides are equal",
                   ["It has 4 right angles", "Opposite sides are equal", "Opposite sides are parallel"],
                   "Only opposite sides of a rectangle must be equal. A rectangle 10 cm by 4 cm does not have 4 equal sides."))
    its.append(mcq("Which is true about every square, but NOT about every rectangle?", "All 4 sides are equal",
                   ["It has 4 right angles", "Opposite sides are parallel", "Opposite sides are equal"],
                   "Both shapes have 4 right angles and opposite sides equal and parallel. Only a square must have 4 equal sides."))
    n, he, his = Pp.next()
    its.append(mcq("%s says, “A rectangle has 4 equal sides.” What is wrong?" % n, "Only opposite sides must be equal",
                   ["A rectangle has 3 equal sides", "Nothing is wrong", "A rectangle has no equal sides"],
                   "In a rectangle, the 2 long sides are equal and the 2 short sides are equal. Only a square has 4 equal sides."))
    n, he, his = Pp.next()
    its.append(mcq(R + "%s draws a line from A to C. %s says ∠BAC must be 45°. Is %s right?" % (n, he.capitalize(), he),
                   "No, the line does not always cut ∠BAD into equal parts",
                   ["Yes, a line from a corner always makes 45°", "Yes, because ∠BAD is 90°", "No, ∠BAC is always 90°"],
                   "We only know that ∠BAD = 90°. In this long rectangle, AC is much closer to AB than to AD, so ∠BAC is "
                   "smaller than 45°. Do not guess 45°."))
    T = fig(abcd_svg(100, 100, names="WXYZ", rot=30, label="square WXYZ turned on its side"))
    its.append(mcq(T + "WXYZ is a square. Which side is parallel to WX?", "ZY", ["XY", "WZ", "WY"],
                   "Turning the square does not change it. The side opposite WX is ZY, so WX // ZY."))
    K = fig(abcd_svg(150, 84, names="KLMN", rot=-20, label="rectangle KLMN turned"))
    its.append(mcq(K + "KLMN is a rectangle. What is the size of ∠KLM?", D(90), [D(45), D(180), D(70)],
                   "Every angle of a rectangle is 90°, even when the rectangle is turned. ∠KLM is the angle at L."))
    its.append(mcq(S + "PQRS is a square. Which angle is ∠PQR?", "the angle at Q", ["the angle at P", "the angle at R",
                                                                                     "the angle at S"],
                   "The middle letter tells you the corner. ∠PQR is the angle at Q, and it is 90°."))
    its.append(mcq("A shape has 4 equal sides, but its angles are not right angles. Is it a square?",
                   "No, a square must have 4 right angles", ["Yes, its 4 sides are equal", "Yes, if it stands on a corner",
                                                             "No, a square has only 2 equal sides"],
                   "A square needs 4 equal sides AND 4 right angles. This shape is a rhombus, not a square."))
    its.append(mcq("Which shape has opposite sides parallel, 4 right angles and 4 equal sides?", "a square",
                   ["a rectangle that is not a square", "a rhombus that is not a square", "a trapezium"],
                   "4 right angles and opposite sides parallel make a rectangle. With 4 equal sides as well, it is a square."))
    assert len(its) == 20, len(its)
    return {"title": "Properties of rectangles and squares", "items": its}


# ------------------------------------------------------------ set 3: unknown sides
def set_sides(rnd, pos, Pp):
    its = []
    f = fig(abcd_svg(14, 6, sides={0: "14 cm", 1: "6 cm"}, scale=11, label="rectangle ABCD, AB 14 cm, BC 6 cm"))
    its.append(mcq(f + "ABCD is a rectangle. Find the length of DC.", CM(14), [CM(6), CM(20), CM(28)],
                   "Opposite sides of a rectangle are equal. DC is opposite AB, so DC = 14 cm."))
    f = fig(abcd_svg(12, 7, sides={0: "12 cm", 1: "7 cm"}, scale=12, label="rectangle ABCD, AB 12 cm, BC 7 cm"))
    its.append(mcq(f + "ABCD is a rectangle. Find the length of AD.", CM(7), [CM(12), CM(5), CM(19)],
                   "AD is opposite BC, so AD = BC = 7 cm."))
    f = fig(abcd_svg(9, 9, names="PQRS", sides={0: "9 cm"}, scale=13, label="square PQRS, PQ 9 cm"))
    its.append(mcq(f + "PQRS is a square. Find the length of QR.", CM(9), [CM(18), CM(36), CM(81)],
                   "All sides of a square are equal, so QR = PQ = 9 cm."))
    its.append(mcq("The perimeter of a square is 36 cm. Find the length of one side.", CM(9), [CM(18), CM(12), CM(32)],
                   "A square has 4 equal sides. 36 ÷ 4 = 9, so each side is 9 cm. (Do not divide by 2.)"))
    its.append(mcq("The perimeter of a square is 52 cm. Find the length of one side.", CM(13), [CM(26), CM(48), CM(208)],
                   "52 ÷ 4 = 13, so each side is 13 cm."))
    its.append(mcq("A rectangle has a perimeter of 30 cm. Its length is 9 cm. Find its breadth.", CM(6), [CM(21), CM(12), CM("7.5")],
                   "Length + breadth = half the perimeter = 30 ÷ 2 = 15 cm. Breadth = 15 − 9 = 6 cm."))
    its.append(mcq("A rectangle has a perimeter of 46 cm. Its breadth is 8 cm. Find its length.", CM(15), [CM(38), CM(30), CM(23)],
                   "Length + breadth = 46 ÷ 2 = 23 cm. Length = 23 − 8 = 15 cm."))
    f = fig(abcd_svg(12, 8, sides={0: "12 cm"}, scale=12, label="rectangle ABCD, AB 12 cm"))
    its.append(mcq(f + "ABCD is a rectangle. Its perimeter is 40 cm. Find BC.", CM(8), [CM(28), CM(16), CM(10)],
                   "AB + BC = 40 ÷ 2 = 20 cm. BC = 20 − 12 = 8 cm."))
    f = fig(squares_row_svg(2, 7, each="7 cm", label="2 equal squares of side 7 cm joined in a row"))
    its.append(mcq(f + "A rectangle is made of 2 equal squares. Each square has sides of 7 cm. Find the length of the rectangle.",
                   CM(14), [CM(7), CM(21), CM(28)], "The length is 2 sides of a square: 7 + 7 = 14 cm."))
    f = fig(squares_row_svg(3, 8, below="24 cm", label="3 equal squares in a row, 24 cm long"))
    its.append(mcq(f + "This rectangle is made of 3 equal squares. It is 24 cm long. Find the length of one side of a square.",
                   CM(8), [CM(12), CM(6), CM(21)],
                   "The length is made of 3 equal sides: 24 ÷ 3 = 8 cm. (Not 24 ÷ 4: there are 3 squares in the row.)"))
    f = fig(point_on_side_svg(14, 6, ("AB", 5), {("A", "E"): "5 cm", ("E", "B"): "9 cm"},
                              "rectangle ABCD with E on AB, AE 5 cm, EB 9 cm", k=14))
    its.append(mcq(f + "ABCD is a rectangle. E is a point on AB. Find the length of DC.", CM(14), [CM(9), CM(5), CM(4)],
                   "AB = 5 + 9 = 14 cm. DC is opposite AB, so DC = 14 cm."))
    f = fig(point_on_side_svg(20, 7, ("DC", 8), {("A", "B"): "20 cm", ("E", "C"): "12 cm"},
                              "rectangle ABCD with E on DC, AB 20 cm, EC 12 cm", k=9))
    its.append(mcq(f + "ABCD is a rectangle. E is a point on DC. Find the length of DE.", CM(8), [CM(12), CM(20), CM(32)],
                   "DC = AB = 20 cm. DE = 20 − 12 = 8 cm."))
    f = fig(square_rect_svg(8, 5, "square ABCD of side 8 cm joined to rectangle BEFC, BE 5 cm"))
    its.append(mcq(f + "ABCD is a square of side 8 cm. BEFC is a rectangle. Find the length of AE.", CM(13), [CM(5), CM(8), CM(3)],
                   "AB is a side of the square, so AB = 8 cm. AE = AB + BE = 8 + 5 = 13 cm."))
    f = fig(square_rect_svg(9, 6, "square ABCD of side 9 cm joined to rectangle BEFC, BE 6 cm"))
    its.append(mcq(f + "ABCD is a square of side 9 cm. BEFC is a rectangle. Find the length of EF.", CM(9), [CM(6), CM(15), CM(3)],
                   "EF is opposite BC in the rectangle BEFC, so EF = BC. BC is a side of the square, so EF = 9 cm."))
    f = fig(split_rect_svg(15, 6, 6, {}, {("A", "D"): "6 cm", ("A", "B"): "15 cm"},
                           "rectangle ABCD split into square AEFD and rectangle EBCF, AB 15 cm, AD 6 cm"))
    its.append(mcq(f + "ABCD is a rectangle. AEFD is a square. Find the length of EB.", CM(9), [CM(6), CM(15), CM(21)],
                   "AE is a side of the square, so AE = AD = 6 cm. EB = 15 − 6 = 9 cm."))
    f = fig(split_rect_svg(16, 9, 10, {}, {("A", "D"): "9 cm", ("A", "E"): "10 cm", ("E", "B"): "6 cm"},
                           "rectangle ABCD split by line EF, AD 9 cm, AE 10 cm, EB 6 cm"))
    its.append(mcq(f + "ABCD is a rectangle. AEFD and EBCF are rectangles. Find the length of EF.", CM(9), [CM(10), CM(6), CM(16)],
                   "EF and AD are opposite sides of the rectangle AEFD, so EF = AD = 9 cm."))
    its.append(mcq("The length of rectangle ABCD is 3 times its breadth. Its breadth, BC, is 7 cm. Find its length, AB.",
                   CM(21), [CM(10), CM(4), CM(28)], "Length = 3 × 7 = 21 cm."))
    its.append(mcq("A square has the same perimeter as a rectangle 10 cm by 6 cm. Find the length of one side of the square.",
                   CM(8), [CM(16), CM(4), CM(32)],
                   "Perimeter of the rectangle = 10 + 6 + 10 + 6 = 32 cm. Side of the square = 32 ÷ 4 = 8 cm."))
    its.append(mcq("A rectangle has a breadth of 9 cm. Its length is 4 cm more than its breadth. Find its perimeter.",
                   CM(44), [CM(22), CM(36), CM(52)],
                   "Length = 9 + 4 = 13 cm. Perimeter = 13 + 9 + 13 + 9 = 44 cm."))
    f = fig(squares_row_svg(4, 5, each="5 cm", label="4 equal squares of side 5 cm in a row"))
    its.append(mcq(f + "4 equal squares with sides of 5 cm are put in a row to make a rectangle. Find the perimeter of the rectangle.",
                   CM(50), [CM(80), CM(25), CM(40)],
                   "The rectangle is 4 × 5 = 20 cm long and 5 cm wide. Perimeter = 20 + 5 + 20 + 5 = 50 cm. "
                   "(80 cm counts the sides inside the rectangle too.)"))
    assert len(its) == 20, len(its)
    return {"title": "Find unknown sides", "items": its}


# ------------------------------------------------------------ set 4: unknown angles
CORNER_NAMES = {0: ("A", "B", "D"), 1: ("B", "C", "A"), 2: ("C", "D", "B"), 3: ("D", "A", "C")}


def wrong_angles(x, other):
    """Real mistakes: 180 − x (straight line instead of right angle), the given angle again, 90 + x."""
    out = []
    for c in (180 - x, x, 90 + x, 360 - x):
        if c != other and c not in out:
            out.append(c)
    return [D(c) for c in out[:3]]


def set_angles(rnd, pos, Pp):
    its = []
    # one line from a corner of a rectangle; give one part, find the other
    plan = [(0, 34, 0, 230, 130), (0, 52, 1, 230, 140), (1, 40, 0, 220, 130), (1, 63, 1, 220, 140),
            (2, 28, 0, 200, 150), (2, 47, 1, 210, 150), (3, 36, 1, 230, 130), (3, 58, 0, 230, 120)]
    for corner, x, given, w, h in plan:
        v, nxt, prv = CORNER_NAMES[corner]
        splits = [x, 90 - x] if given == 0 else [90 - x, x]
        labels = [D(x), None] if given == 0 else [None, D(x)]
        svg, hits = split_svg(w, h, corner, splits, labels)
        # the angle next to the side towards nxt is ∠(nxt)(v)E
        a_nxt = "∠%s%sE" % (nxt, v)
        a_prv = "∠E%s%s" % (v, prv)
        if given == 0:
            known, ask = a_nxt, a_prv
        else:
            known, ask = a_prv, a_nxt
        ansv = 90 - x
        its.append(mcq(fig(svg) + "ABCD is a rectangle. %s = %d°. Find %s." % (known, x, ask), D(ansv), wrong_angles(x, ansv),
                       "The angle at %s is a right angle, 90°. %s = 90° − %d° = %d°." % (v, ask, x, ansv)))
    # squares
    for corner, x, given in [(0, 62, 0), (1, 33, 1), (3, 55, 1)]:
        v, nxt, prv = CORNER_NAMES[corner]
        splits = [x, 90 - x] if given == 0 else [90 - x, x]
        labels = [D(x), None] if given == 0 else [None, D(x)]
        svg, _ = split_svg(160, 160, corner, splits, labels, square_marks=True, label="square ABCD with a line from corner %s" % v)
        known, ask = ("∠%s%sE" % (nxt, v), "∠E%s%s" % (v, prv)) if given == 0 else ("∠E%s%s" % (v, prv), "∠%s%sE" % (nxt, v))
        its.append(mcq(fig(svg) + "ABCD is a square. %s = %d°. Find %s." % (known, x, ask), D(90 - x), wrong_angles(x, 90 - x),
                       "Every angle of a square is 90°. %s = 90° − %d° = %d°." % (ask, x, 90 - x)))
    # two lines from a corner
    for a, c, w, h in [(25, 30, 230, 150), (32, 21, 220, 175)]:
        b = 90 - a - c
        svg, _ = split_svg(w, h, 0, [a, b, c], [D(a), None, D(c)], label="rectangle ABCD with two lines from A")
        its.append(mcq(fig(svg) + "ABCD is a rectangle. ∠BAE = %d° and ∠FAD = %d°. Find ∠EAF." % (a, c), D(b),
                       [D(a + c), D(180 - a - c), D(90 - a)],
                       "The 3 angles at A make a right angle. ∠EAF = 90° − %d° − %d° = %d°." % (a, c, b)))
    a, b, c = 27, 37, 26
    svg, _ = split_svg(220, 150, 1, [a, b, c], [D(a), None, D(c)], label="rectangle ABCD with two lines from B")
    its.append(mcq(fig(svg) + "ABCD is a rectangle. ∠CBE = %d° and ∠FBA = %d°. Find ∠EBF." % (a, c), D(b),
                   [D(a + c), D(180 - a - c), D(90 - c)],
                   "The 3 angles at B make a right angle. ∠EBF = 90° − %d° − %d° = %d°." % (a, c, b)))
    # a turned square
    x = 36
    svg, _ = split_svg(140, 140, 0, [x, 90 - x], [D(x), None], square_marks=True, rot=-20,
                       label="a turned square ABCD with a line from corner A")
    its.append(mcq(fig(svg) + "ABCD is a square that has been turned. ∠BAE = %d°. Find ∠EAD." % x, D(90 - x),
                   wrong_angles(x, 90 - x),
                   "Turning does not change the angles. ∠BAD is still 90°, so ∠EAD = 90° − %d° = %d°." % (x, 90 - x)))
    its.append(mcq("ABCD is a rectangle. A line BE splits ∠ABC into two equal angles. Find ∠ABE.", D(45),
                   [D(90), D(30), D(180)],
                   "∠ABC = 90°. Two equal parts: 90° ÷ 2 = 45°."))
    # one line from A and one from D to the same point E on BC
    ta = 28
    w, h = 240, 0
    ey = w * math.tan(math.radians(ta))
    # choose h so that ∠EDC is a whole number of degrees
    d_split = 26
    h = ey + w * math.tan(math.radians(d_split))
    svg = angle_svg_two(w, h, ta, d_split, "rectangle ABCD with lines from A and D to a point E on BC")
    its.append(mcq(fig(svg) + "ABCD is a rectangle. ∠BAE = %d° and ∠EDC = %d°. Find ∠ADE." % (ta, d_split), D(90 - d_split),
                   [D(90 - ta), D(180 - d_split), D(d_split)],
                   "Look at corner D. ∠ADC = 90°, so ∠ADE = 90° − %d° = %d°. The %d° angle is at A, not at D."
                   % (d_split, 90 - d_split, ta)))
    # comparing parts of a right angle
    its.append(mcq("ABCD is a rectangle. A line AE splits ∠BAD into two parts. ∠BAE is twice as large as ∠EAD. Find ∠EAD.",
                   D(30), [D(45), D(60), D(90)],
                   "∠BAE is 2 units and ∠EAD is 1 unit. 3 units = 90°, so 1 unit = 30°. ∠EAD = 30°."))
    its.append(mcq("ABCD is a square. A line AE splits ∠BAD into two parts. ∠BAE is 20° more than ∠EAD. Find ∠EAD.",
                   D(35), [D(55), D(45), D(70)],
                   "Take away the extra 20°: 90° − 20° = 70°. The two equal parts are 70° ÷ 2 = 35°. ∠EAD = 35° and ∠BAE = 55°."))
    its.append(mcq("ABCD is a rectangle. A line AE splits ∠BAD into two parts. ∠BAE is 4 times as large as ∠EAD. Find ∠BAE.",
                   D(72), [D(18), D(45), D(60)],
                   "∠BAE is 4 units and ∠EAD is 1 unit. 5 units = 90°, so 1 unit = 18°. ∠BAE = 4 × 18° = 72°."))
    assert len(its) == 20, len(its)
    return {"title": "Find unknown angles", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd, pos, Pp):
    its = []
    n, he, his = Pp.next()
    its.append(mcq("%s glues a ribbon around the edge of a rectangular photo frame. The frame is 25 cm long and 18 cm wide. "
                   "How much ribbon does %s need?" % (n, he), CM(86), [CM(43), CM(450), CM(68)],
                   "Perimeter = 25 + 18 + 25 + 18 = 86 cm. (43 cm is only one length and one breadth.)"))
    n, he, his = Pp.next()
    its.append(mcq("%s has a square piece of paper. Its perimeter is 64 cm. What is the length of one side?" % n,
                   CM(16), [CM(32), CM(60), CM(256)], "A square has 4 equal sides: 64 ÷ 4 = 16 cm."))
    its.append(mcq("A rectangular plot in a community garden is 12 m long and 7 m wide. Mr Tan puts a fence all around it. "
                   "How long is the fence?", CM(38, "m"), [CM(19, "m"), CM(84, "m"), CM(31, "m")],
                   "Perimeter = 12 + 7 + 12 + 7 = 38 m."))
    f = bar_model([("Length", 3, None, None), ("Breadth", 1, "?", None)], "32 cm",
                  "length 3 units, breadth 1 unit, together 32 cm")
    its.append(mcq(fig(f) + "The length of a rectangle is 3 times its breadth. Its perimeter is 64 cm. Find its breadth.",
                   CM(8), [CM(16), CM(24), CM(32)],
                   "Length + breadth = 64 ÷ 2 = 32 cm. From the model, 4 units = 32 cm, so 1 unit = 8 cm. The breadth is 8 cm."))
    f = bar_model([("Length", 1, None, ("6 cm", 1)), ("Breadth", 1, None, None)], "20 cm",
                  "length is breadth plus 6 cm, together 20 cm")
    its.append(mcq(fig(f) + "The length of a rectangle is 6 cm longer than its breadth. Its perimeter is 40 cm. Find its length.",
                   CM(13), [CM(7), CM(17), CM(14)],
                   "Length + breadth = 40 ÷ 2 = 20 cm. 2 units = 20 − 6 = 14 cm, so 1 unit = 7 cm. Length = 7 + 6 = 13 cm."))
    n, he, his = Pp.next()
    its.append(mcq("%s bends a 48 cm piece of wire to make a square. What is the length of one side of the square?" % n,
                   CM(12), [CM(24), CM(16), CM(44)], "The wire goes all around the square: 48 ÷ 4 = 12 cm."))
    n, he, his = Pp.next()
    its.append(mcq("%s bends a 48 cm piece of wire to make a rectangle 15 cm long. How wide is the rectangle?" % n,
                   CM(9), [CM(33), CM(18), CM(12)],
                   "Length + breadth = 48 ÷ 2 = 24 cm. Breadth = 24 − 15 = 9 cm."))
    f = squares_row_svg(2, 5, label="2 equal squares joined to make a rectangle")
    n, he, his = Pp.next()
    its.append(mcq(fig(f) + "%s joins 2 equal square tiles to make a rectangle. Each square has a perimeter of 20 cm. "
                   "What is the perimeter of the rectangle?" % n, CM(30), [CM(40), CM(20), CM(25)],
                   "Each side of a square is 20 ÷ 4 = 5 cm. The rectangle is 10 cm by 5 cm. Perimeter = 10 + 5 + 10 + 5 = 30 cm. "
                   "(40 cm counts the side in the middle twice.)"))
    n, he, his = Pp.next()
    its.append(mcq("%s ties a ribbon around a rectangular card 20 cm by 12 cm. %s also needs 8 cm more for a bow. "
                   "How much ribbon does %s need in all?" % (n, he.capitalize(), he), CM(72), [CM(64), CM(40), CM(52)],
                   "Perimeter = 20 + 12 + 20 + 12 = 64 cm. Add the bow: 64 + 8 = 72 cm."))
    its.append(mcq("On Sports Day, Primary 4 students run 3 times round a rectangular field. The field is 90 m long and 50 m wide. "
                   "How far do they run?", CM(840, "m"), [CM(280, "m"), CM(420, "m"), CM(4500, "m")],
                   "One round = 90 + 50 + 90 + 50 = 280 m. 3 rounds = 3 × 280 = 840 m."))
    f = bar_model([("Length", 2, None, None), ("Breadth", 1, "?", None)], "27 cm",
                  "length 2 units, breadth 1 unit, together 27 cm")
    its.append(mcq(fig(f) + "The breadth of a rectangle is half its length. Its perimeter is 54 cm. Find its length.",
                   CM(18), [CM(9), CM(27), CM("13.5")],
                   "Length + breadth = 54 ÷ 2 = 27 cm. 3 units = 27 cm, so 1 unit = 9 cm. Length = 2 units = 18 cm."))
    its.append(mcq("A square playground has sides of 25 m. A fence is put along 3 of its sides. The fourth side is a wall. "
                   "How long is the fence?", CM(75, "m"), [CM(100, "m"), CM(50, "m"), CM(625, "m")],
                   "The fence covers 3 equal sides: 3 × 25 = 75 m."))
    its.append(mcq("A square window has a perimeter of 4 m 80 cm. How long is one side, in centimetres?", CM(120),
                   [CM(240), CM(160), CM(480)],
                   "4 m 80 cm = 480 cm. One side = 480 ÷ 4 = 120 cm."))
    its.append(mcq("Mdm Wong sews lace around a rectangular tablecloth. The tablecloth is 2 m long and 1 m 20 cm wide. "
                   "How much lace does she need?", "6 m 40 cm", ["3 m 20 cm", "6 m 4 cm", "5 m 20 cm"],
                   "1 m 20 cm = 120 cm and 2 m = 200 cm. Perimeter = 200 + 120 + 200 + 120 = 640 cm = 6 m 40 cm."))
    f = door_svg(240, 130, 35, "a rectangular gate with a support bar from the top left corner, 35° to the top edge")
    its.append(mcq(fig(f) + "A rectangular gate has a support bar from one corner. The bar makes an angle of 35° with the top "
                   "edge. What angle does it make with the side edge?", D(55), [D(145), D(35), D(125)],
                   "The corner of the gate is a right angle. 90° − 35° = 55°."))
    f = squares_row_svg(4, 5, each="?", label="4 equal squares in a row")
    n, he, his = Pp.next()
    its.append(mcq(fig(f) + "%s puts 4 equal square stickers in a row with no gaps. The rectangle formed has a perimeter of 50 cm. "
                   "What is the length of one side of a sticker?" % n, CM(5), [CM("12.5"), CM(25), CM("6.25")],
                   "Go round the rectangle: 4 sides along the top, 4 along the bottom and 1 at each end. That is 10 sides. "
                   "50 ÷ 10 = 5 cm."))
    f = bar_model([("Length", 1, None, ("20 cm", 1)), ("Breadth", 1, "?", None)], "60 cm",
                  "length is breadth plus 20 cm, together 60 cm")
    its.append(mcq(fig(f) + "A rectangular poster for Children's Day has a perimeter of 120 cm. Its length is 20 cm longer than "
                   "its breadth. Find its breadth.", CM(20), [CM(40), CM(50), CM(30)],
                   "Length + breadth = 120 ÷ 2 = 60 cm. 2 units = 60 − 20 = 40 cm, so 1 unit = 20 cm. The breadth is 20 cm."))
    svg, _ = split_svg(150, 150, 0, [52, 38], [D(52), None], square_marks=True, label="a square tile with a line from corner A")
    n, he, his = Pp.next()
    its.append(mcq(fig(svg) + "%s paints a straight line from corner A of a square tile ABCD. ∠BAE = 52°. Find ∠EAD." % n,
                   D(38), [D(128), D(52), D(308)], "∠BAD is a right angle. ∠EAD = 90° − 52° = 38°."))
    its.append(mcq(fig(frame_svg()) + "Chloe hangs a square photo frame on a nail by one corner, so it looks like a diamond. "
                   "What is the size of each angle of the frame?", D(90), [D(45), D(60), D(120)],
                   "It is still a square, only turned. Every angle of a square is 90°."))
    n, he, his = Pp.next()
    its.append(mcq("A rectangular notice board at the HDB void deck is 3 m long. Its perimeter is 8 m. "
                   "How wide is the notice board?", CM(1, "m"), [CM(5, "m"), CM(2, "m"), CM(3, "m")],
                   "Length + breadth = 8 ÷ 2 = 4 m. Breadth = 4 − 3 = 1 m. (5 m is 8 − 3: it forgets that there are 2 lengths.)"))
    assert len(its) == 20, len(its)
    return {"title": "Rectangles and squares: word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    intro = strip_svg([("rect", 0, "rectangle"), ("square", 0, "square"), ("square", 45, "turned square")],
                      "a rectangle, a square and a turned square with their marks", cw=160)
    notr = strip_svg([("rhombus", 0, "no right angles"), ("para", 0, "no right angles"), ("rtrap", 0, "2 right angles")],
                     "three shapes that are not rectangles", cw=160)
    R = abcd_svg(170, 96, label="rectangle ABCD with its right angles and equal sides marked")
    s1 = abcd_svg(12, 7, sides={0: "12 cm", 1: "7 cm"}, scale=12, label="rectangle ABCD, AB 12 cm, BC 7 cm")
    a1, _ = split_svg(230, 140, 0, [35, 55], [D(35), None], label="rectangle ABCD with a line from A, angle BAE 35°")
    m1 = bar_model([("Length", 2, None, None), ("Breadth", 1, "?", None)], "18 cm",
                   "length 2 units, breadth 1 unit, together 18 cm")
    return (
        "<h2>What is a rectangle? What is a square?</h2>"
        "<p>A <b>rectangle</b> has 4 sides and <b>4 right angles</b>. Its <b>opposite sides are equal and parallel</b>.</p>"
        "<p>A <b>square</b> is a rectangle with <b>4 equal sides</b>. So a square is a special rectangle.</p>"
        "<p>A small square at a corner shows a right angle. Sides with the same marks are equal.</p>"
        "<figure class='sn-fig'>" + intro +
        "<figcaption>Turning a square does not change it. It still has 4 equal sides and 4 right angles, even if it looks like a “diamond”.</figcaption></figure>"
        "<figure class='sn-fig'>" + notr +
        "<figcaption>These shapes are not rectangles: some or all of their angles are not right angles.</figcaption></figure>"
        "<h2>Properties</h2>"
        "<figure class='sn-fig'>" + R +
        "<figcaption>In rectangle ABCD: AB // DC and AD // BC. AB = DC and AD = BC. AB ⊥ BC.</figcaption></figure>" +
        table(["", "Rectangle", "Square"], [
            ["Right angles", "4 (each 90°)", "4 (each 90°)"],
            ["Equal sides", "opposite sides equal", "all 4 sides equal"],
            ["Parallel sides", "2 pairs", "2 pairs"],
            ["Angles add up to", "360°", "360°"],
        ]) +
        "<p>We write ∠ABC for the angle at B. The middle letter is the corner. // means “is parallel to” and ⊥ means "
        "“is perpendicular to”.</p>"
        "<h2>Find unknown sides</h2>"
        "<p>Use “opposite sides are equal”. For a square, all 4 sides are equal.</p>"
        "<figure class='sn-fig'>" + s1 + "</figure>" +
        ex("Example 1", "ABCD is a rectangle. AB = 12 cm and BC = 7 cm. Find DC and the perimeter.",
           "DC is opposite AB, so DC = 12 cm. Perimeter = 12 + 7 + 12 + 7 = 38 cm.", "DC = 12 cm, perimeter 38 cm") +
        ex("Example 2", "The perimeter of a square is 36 cm. Find one side.",
           "A square has 4 equal sides. 36 ÷ 4 = 9.", "9 cm") +
        "<h2>Find unknown angles</h2>"
        "<p>Each corner of a rectangle or square is <b>90°</b>. When a line splits a corner, the parts add up to 90°.</p>"
        "<figure class='sn-fig'>" + a1 + "</figure>" +
        ex("Example 3", "ABCD is a rectangle. ∠BAE = 35°. Find ∠EAD.",
           "∠BAD = 90°. ∠EAD = 90° − 35° = 55°.", "55°") +
        "<h2>Word problems with a model</h2>"
        "<p>Half the perimeter is one length + one breadth. Draw the length and breadth as bars, then find 1 unit.</p>"
        "<figure class='sn-fig'>" + m1 + "</figure>" +
        ex("Example 4", "The length of a rectangle is twice its breadth. Its perimeter is 36 cm. Find its breadth.",
           "Length + breadth = 36 ÷ 2 = 18 cm. 3 units = 18 cm, so 1 unit = 6 cm.", "6 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["“A turned square is a diamond, not a square.”", "Check the sides and angles. Turning a shape does not change it"],
            ["“A rectangle has 4 equal sides.”", "Only opposite sides are equal. Only a square has 4 equal sides"],
            ["“A square is not a rectangle.”", "A square has 4 right angles, so it is a special rectangle"],
            ["Using 180° for a corner", "A corner of a rectangle is 90°. Subtract from 90°, not 180°"],
            ["Guessing 45° when a line splits a corner", "A line from a corner does not always split it equally. Use the given angle"],
            ["Perimeter ÷ 2 for a side of a square", "A square has 4 sides. Divide the perimeter by 4"],
        ])
    )


FAQ = [
    {"q": "What do P4 students learn about rectangles and squares?",
     "a": "In Primary 4, students learn that a rectangle has 4 right angles with opposite sides equal and parallel, and that a "
          "square also has 4 equal sides. They use these properties to find unknown sides and angles."},
    {"q": "Is a square a rectangle?",
     "a": "Yes. A square has 4 right angles and opposite sides equal and parallel, so it is a special rectangle with 4 equal sides. "
          "A rectangle is a square only when all its sides are equal."},
    {"q": "How do I find an unknown angle in a rectangle?",
     "a": "Every corner of a rectangle is 90°, so subtract the given angle from 90°. For example, if ∠BAE = 35°, then ∠EAD = 90° − 35° = 55°."},
    {"q": "What is the most common mistake with rectangles and squares?",
     "a": "Many children think a square standing on its corner is a “diamond” and not a square, or that a rectangle has 4 equal sides. "
          "Checking the right angles and the equal sides clears up both mistakes."},
]


# ------------------------------------------------------------ build
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64814)
    Pp = People(rnd)
    pos = Pos(rnd)
    sets = [set_identify(rnd, pos, Pp), set_properties(rnd, pos, Pp), set_sides(rnd, pos, Pp), set_angles(rnd, pos, Pp),
            set_words(rnd, pos, Pp)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen_q = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen_q, it["q"]
            seen_q.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "rectangles-and-squares", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Rectangles and Squares",
        "seo_title": "P4 Rectangles and Squares Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Rectangles and squares",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 4: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Properties of rectangle and square, excluding diagonal properties",
        "meta_desc": "Free P4 maths practice on rectangles and squares: properties, unknown sides and angles, and word problems. "
                     "100 questions with answers.",
        "key_big": "A rectangle has 4 right angles and opposite sides equal. A square also has 4 equal sides.",
        "key_sub": "ABCD is a rectangle and ∠BAE = 35°, so ∠EAD = 90° − 35° = 55°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(four shapes labelled A to D|bar model|[0-9] equal squares)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
