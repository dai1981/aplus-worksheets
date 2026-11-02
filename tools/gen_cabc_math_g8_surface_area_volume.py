# -*- coding: utf-8 -*-
"""
British Columbia Grade 8 Math: Surface area and volume of prisms and cylinders
(BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g8_surface_area_volume.py
Canadian English, metric units (cm², cm³, m², m³, mL, L), SI number style (4 digits plain, 5+ digits with a no-break space).
Every answer is computed with decimal.Decimal (π ≈ 3.14 exactly, never float).
HTML attributes use single quotes (no backslashes in the JSON).

Pictures (checked in code):
  prisms        oblique view, hidden edges dashed, edge labels outside the solid; labels never touch;
                every solid is drawn to scale (no edge is stretched)
  triangular    right-triangle prism lying on a face; right-angle mark; hidden edges dashed
  triangle ends an isosceles triangle with its height dashed; the sloped side is labelled too
  cylinders     upright; top ellipse, hidden half of the bottom dashed; radius (centre to edge) or
                diameter (edge to edge) drawn on the top; height shown with a dimension line
  box nets      strip of 4 faces with the top and bottom attached (drawn to scale)
  prism nets    3 rectangles side by side with a triangle on each end; each triangle edge is glued to a
                rectangle edge of the same length (asserted)
  cylinder nets a rectangle 2πr long and h high with a circle touching the top and the bottom (to scale)
  nets          a label is either fully inside one face or outside all faces, and no line crosses it (asserted)
Wrong answers come from real student mistakes: using the diameter as the radius, writing cm² for a volume
(or cm³ for an area), forgetting the ½ for a triangle, using the sloped side instead of the height,
r × 2 instead of r², counting only one circle or only the rectangle of a cylinder net, leaving out a face,
adding the third side of a right triangle instead of using the Pythagorean theorem, and slipping a
decimal place when changing cm³ to L.
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
BASE = "#f6dcb4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)
PI = Dm("3.14")
NB = "\u00a0"


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


def cm3(x):
    return N(x) + " cm³"


def cm2(x):
    return N(x) + " cm²"


UNIT = {"cm³": ("v", 1), "mL": ("v", 1), "L": ("v", 1000), "m³": ("v", 1000000),
        "cm²": ("a", 1), "m²": ("a", 10000), "cm": ("l", 1), "m": ("l", 100)}
NUM = re.compile(r"^(?:about )?([\d ]+(?:\.\d+)?) (\S+)$")


def val(c):
    """(kind, value) of a choice like '72 000 cm³' or 'about 339 mL'; None if it is not one amount."""
    m = NUM.match(c)
    if not m:
        return None
    v = Dm(m.group(1).replace(NB, ""))
    if m.group(2) in UNIT:
        k, f = UNIT[m.group(2)]
        return (k, v * f)
    return (m.group(2), v)


def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors. No two choices may be the same amount (1 L and 1000 mL)."""
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


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(".") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


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

    def poly(self, pts, fill, sw=1.6, col=GREEN):
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
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def fits(self, box, poly):
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

    def svg(self, label, pad=5, check=False):
        if check:
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


def proj(X, Y, Z, k):
    """x to the right, y up, z (depth) to the back."""
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


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


# ------------------------------------------------------------ 3D pictures
def box_faces(cv, L, W, H, k):
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(L, 0, 0), p(L, H, 0), p(0, H, 0)], FILL, 2.4)
    cv.poly([p(0, H, 0), p(L, H, 0), p(L, H, W), p(0, H, W)], TOP, 2.4)
    cv.poly([p(L, 0, 0), p(L, 0, W), p(L, H, W), p(L, H, 0)], SIDE, 2.4)
    return p


def disp_dims(*v):
    """Draw very different sizes a little closer together so the solid stays readable."""
    v = [float(x) for x in v]
    m = max(v)
    return tuple(max(x, m / 3.2) for x in v)


def prism_svg(L, W, H, lab_l, lab_w, lab_h, label):
    dL, dW, dH = disp_dims(L, W, H)
    k = min(165 / (dL + dW * DZX), 100 / (dH + dW * DZY))
    cv = Canvas()
    p = box_faces(cv, dL, dW, dH, k)
    for a, b in [((0, 0, dW), (dL, 0, dW)), ((0, 0, dW), (0, dH, dW)), ((0, 0, dW), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True)
    col = lambda t: RED if "?" in t else INK
    x, y = p(dL / 2, 0, 0)
    cv.text(x, y + 17, lab_l, 16, col=col(lab_l))
    x, y = p(0, dH / 2, 0)
    cv.text(x - 8, y, lab_h, 16, "end", col(lab_h))
    x, y = p(dL, 0, dW / 2)
    cv.text(x + 7, y + 11, lab_w, 16, "start", col(lab_w))
    return cv.svg(label)


def tri_svg(a, b, L, u, label):
    """Prism whose ends are right triangles (legs a across and b up), length L going back."""
    da, db, dL = disp_dims(a, b, L)
    k = min(165 / (da + dL * DZX), 110 / (db + dL * DZY))
    cv = Canvas()
    p = lambda x, y, z: proj(x, y, z, k)
    cv.poly([p(0, 0, 0), p(da, 0, 0), p(0, db, 0)], FILL, 2.4)
    cv.poly([p(0, db, 0), p(da, 0, 0), p(da, 0, dL), p(0, db, dL)], TOP, 2.4)
    for s, t in [((0, 0, 0), (0, 0, dL)), ((0, 0, dL), (da, 0, dL)), ((0, 0, dL), (0, db, dL))]:
        cv.line(p(*s), p(*t), dashed=True)
    ox, oy = p(0, 0, 0)
    cv.raw(lambda X, Y: "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
           % (ox + 11 - X, oy - Y, ox + 11 - X, oy - 11 - Y, ox - X, oy - 11 - Y, GREEN), (ox, oy - 11, ox + 11, oy))
    x, y = p(da / 2, 0, 0)
    cv.text(x, y + 17, "%s %s" % (N(a), u), 16)
    x, y = p(0, db / 2, 0)
    cv.text(x - 8, y, "%s %s" % (N(b), u), 16, "end")
    x, y = p(da, 0, dL / 2)
    cv.text(x + 7, y + 11, "%s %s" % (N(L), u), 16, "start")
    return cv.svg(label)


def cyl_svg(r, h, u, show_d=False, label=None, hlab=None):
    """Upright cylinder. show_d: the label goes across the whole top (diameter); else centre to edge (radius)."""
    dr, dh = disp_dims(2 * r, h)
    dr /= 2
    k = min(62 / dr, 115 / dh)
    R, H = dr * k, dh * k
    ry = R * 0.3
    cv = Canvas()
    cv.raw(lambda X, Y: "<path d='M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f Z' fill='%s' stroke='%s' "
           "stroke-width='2.4' stroke-linejoin='round'/>"
           % (-R - X, -H - Y, -R - X, -Y, R, ry, R - X, -Y, R - X, -H - Y, SIDE, GREEN), (-R - 2, -H - 2, R + 2, ry + 2))
    cv.raw(lambda X, Y: "<path d='M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 4'/>" % (-R - X, -Y, R, ry, R - X, -Y, GREEN), (-R, -ry, R, 0))
    cv.raw(lambda X, Y: "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='2.4'/>"
           % (-X, -H - Y, R, ry, TOP, GREEN), (-R - 2, -H - ry - 2, R + 2, -H + ry + 2))
    if show_d:
        cv.line((-R, -H), (R, -H), sw=2.2, col=RED)
        cv.text(0, -H - ry - 12, "%s %s" % (N(2 * r), u), 16)
    else:
        cv.line((0, -H), (R, -H), sw=2.2, col=RED)
        cv.raw(lambda X, Y: "<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s'/>" % (-X, -H - Y, RED), (-4, -H - 4, 4, -H + 4))
        cv.text(R / 2, -H - ry - 12, "%s %s" % (N(r), u), 16)
    xd = R + 14
    cv.line((xd, 0), (xd, -H), sw=1.6, col=INK)
    cv.line((xd - 5, 0), (xd + 5, 0), sw=1.6, col=INK)
    cv.line((xd - 5, -H), (xd + 5, -H), sw=1.6, col=INK)
    ht = hlab or "%s %s" % (N(h), u)
    cv.text(xd + 9, -H / 2, ht, 16, "start", RED if "?" in ht else INK)
    what = "diameter" if show_d else "radius"
    hl = "an unknown height" if hlab else "height %s %s" % (N(h), u)
    return cv.svg(label or "cylinder with %s %s %s and %s" % (what, N(2 * r if show_d else r), u, hl))


# ------------------------------------------------------------ nets
def box_net_svg(L, W, H, u, label=None):
    """Strip of 4 faces (l, w, l, w wide, h tall) with an l × w face above and below the first face."""
    k = min(300 / (2 * L + 2 * W), 185 / (H + 2 * W), 30)
    assert min(L, W, H) * k >= 22, (L, W, H, k)
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cv = Canvas()
    for i in range(4):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL)
    cv.poly([(0, -W * k), (L * k, -W * k), (L * k, 0), (0, 0)], BASE)
    cv.poly([(0, H * k), (L * k, H * k), (L * k, (H + W) * k), (0, (H + W) * k)], BASE)
    cv.text(L / 2 * k, -W * k - 12, "%s %s" % (N(L), u))
    cv.text(L * k + 7, -W / 2 * k, "%s %s" % (N(W), u), anchor="start")
    cv.text(xs[4] * k + 7, H / 2 * k, "%s %s" % (N(H), u), anchor="start")
    return cv.svg(label or "net of a rectangular prism %s by %s by %s %s" % (N(L), N(W), N(H), u), check=True)


def tri_prism_net_svg(tri, L, u, label=None):
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
    x0 = widths[0]
    cv.text(widths[0] / 2 * k, L * k + 14, "%d %s" % (widths[0], u))
    cv.text((x0 + widths[1] + widths[2] / 2) * k, L * k + 14, "%d %s" % (widths[2], u))
    dim_line(cv, x0 * k, (x0 + widths[1]) * k, L / 2 * k + 10, "%d %s" % (widths[1], u))
    cv.text(W * k + 7, L / 2 * k, "%d %s" % (L, u), anchor="start")
    if kind == "iso":
        cv.line(((x0 + widths[1] / 2) * k, 0), tk[2], dashed=True, sw=1.6, col=INK)
        dim_v(cv, x0 * k - 8, 0, tk[2][1], "%d %s" % (tall, u))
    return cv.svg(label or "net of a triangular prism", check=True)


def circle_pts(cx, cy, r, n=72):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def cyl_net_svg(r, h, u, show_d=False, circ=None, label=None):
    """Net of a cylinder drawn to scale: rectangle 2πr by h, one circle touching the top edge, one the bottom."""
    k = min(290 / (2 * math.pi * r), 190 / (h + 4 * r), 30)
    R, Cw, Hh = r * k, 2 * math.pi * r * k, h * k
    assert R >= 16 and Hh >= (46 if circ else 24), (r, h, k)
    cv = Canvas()
    cv.poly([(0, 0), (Cw, 0), (Cw, Hh), (0, Hh)], FILL)
    cx = Cw / 2
    cv.poly(circle_pts(cx, -R, R), BASE)
    cv.poly(circle_pts(cx, Hh + R, R), BASE)
    if show_d:
        cv.line((cx - R, -R), (cx + R, -R), sw=2.2, col=RED)
        cv.text(cx + R + 8, -R, "d = %s %s" % (N(2 * r), u), anchor="start")
    else:
        cv.line((cx, -R), (cx + R, -R), sw=2.2, col=RED)
        cv.raw(lambda X, Y: "<circle cx='%.1f' cy='%.1f' r='3.2' fill='%s'/>" % (cx - X, -R - Y, RED),
               (cx - 4, -R - 4, cx + 4, -R + 4))
        cv.text(cx + R + 8, -R, "r = %s %s" % (N(r), u), anchor="start")
    cv.text(Cw + 7, Hh / 2, "%s %s" % (N(h), u), anchor="start")
    if circ:
        dim_line(cv, 0, Cw, Hh - 10, circ)
    wd = ("diameter %s" if show_d else "radius %s") % N(2 * r if show_d else r)
    return cv.svg(label or "net of a cylinder with %s %s and height %s %s" % (wd, u, N(h), u), check=True)


# ------------------------------------------------------------ formulas
def cv_(r, h):
    return PI * Dm(str(r)) * Dm(str(r)) * Dm(str(h))


def sa_box(L, W, H):
    return 2 * (L * W + L * H + W * H)


def sa_cyl(r, h):
    r, h = Dm(str(r)), Dm(str(h))
    return 2 * PI * r * r + 2 * PI * r * h



def exact(*v):
    """The picture is drawn to scale only when no edge is shorter than max / 3.2 (see disp_dims)."""
    v = [float(x) for x in v]
    assert min(v) >= max(v) / 3.2, v


def sa_tri(tri, L):
    """(two triangles, perimeter, total) for ('right', a, b, c) or ('iso', b, h, s)."""
    if tri[0] == "right":
        _, a, b, c = tri
        assert a * a + b * b == c * c
        return a * b, a + b + c, a * b + (a + b + c) * L
    _, b, h, s = tri
    assert (2 * h) ** 2 + b * b == (2 * s) ** 2
    return b * h, 2 * s + b, b * h + (2 * s + b) * L


def tri_end_svg(b, h, s, u, label):
    """Isosceles triangle (the end of a prism): base b, height h dashed from the top, sloped sides s."""
    assert (2 * h) ** 2 + b * b == (2 * s) ** 2
    k = min(220 / b, 140 / h)
    B, Hh = b * k, h * k
    cv = Canvas()
    cv.poly([(0, 0), (B, 0), (B / 2, -Hh)], BASE, 2.4)
    cv.line((B / 2, -Hh), (B / 2, 0), dashed=True, col=INK)
    cv.raw(lambda X, Y: "<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.6'/>"
           % (B / 2 + 10 - X, -Y, B / 2 + 10 - X, -10 - Y, B / 2 - X, -10 - Y, INK), (B / 2, -10, B / 2 + 10, 0))
    cv.text(B / 2, 17, "%s %s" % (N(b), u))
    cv.text(B / 2 + 6, -Hh * 0.3, "%s %s" % (N(h), u), anchor="start")
    cv.text(B / 4 - 12 - 8 * (b / 2) / h, -Hh / 2, "%s %s" % (N(s), u), anchor="end")
    return cv.svg(label, check=True)


# ============================================================ set 1: prisms
def set_prisms(rnd):
    its, seen = [], set()
    for i in range(5):
        while True:
            L, W, H = rnd.randint(6, 14), rnd.randint(3, 8), rnd.randint(3, 11)
            if (L > W and (L, W, H) not in seen and min(L, W, H) >= max(L, W, H) / 3.2 and L * W != W * H
                    and L * W != L * H and L * W * H != sa_box(L, W, H) and L * W != L + W + H):
                break
        seen.add((L, W, H))
        u = "m" if i == 3 else "cm"
        if u == "m":
            L, W, H = L % 4 + 5, W % 2 + 3, H % 3 + 2
        exact(L, W, H)
        V = L * W * H
        lab = lambda v: "%d %s" % (v, u)
        q = (fig(prism_svg(L, W, H, lab(L), lab(W), lab(H), "rectangular prism %d by %d by %d %s" % (L, W, H, u))) +
             "What is the volume of this rectangular prism?")
        pool = ["%s %s³" % (N(L * W), u), "%d %s³" % (L + W + H, u), "%s %s²" % (N(V), u), "%s %s³" % (N(sa_box(L, W, H)), u)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("Area of the base: %d × %d = %d %s². V = area of base × height = %d × %d = <b>%s %s³</b>. "
             "Multiply (do not add), and write cubic units for a volume." % (L, W, L * W, u, L * W, H, N(V), u))
        its.append(mcq(q, "%s %s³" % (N(V), u), pool, e))
    for l, w, h, u, wrong in [("3.5", "4", "2", "cm", ["9.5 cm³", "2.8 cm³", "28 cm²"]),
                              ("1.2", "0.5", "2", "m", ["3.7 m³", "12 m³", "0.12 m³"])]:
        V = Dm(l) * Dm(w) * Dm(h)
        assert "%s %s³" % (N(Dm(l) + Dm(w) + Dm(h)), u) in wrong
        e = ("V = %s × %s × %s = %s × %s = <b>%s %s³</b>. Count the decimal places to check your answer."
             % (l, w, h, N(Dm(l) * Dm(w)), h, N(V), u))
        q = "A rectangular prism is %s %s long, %s %s wide and %s %s high. What is its volume?" % (l, u, w, u, h, u)
        its.append(mcq(q, "%s %s³" % (N(V), u), wrong, e))
    assert Dm("2.5") ** 3 == Dm("15.625")
    its.append(mcq("A cube has edges that are 2.5 cm long. What is its volume?", "15.625 cm³",
                   ["7.5 cm³", "6.25 cm³", "15.625 cm²"],
                   "V = 2.5 × 2.5 × 2.5 = 6.25 × 2.5 = <b>15.625 cm³</b>. 7.5 adds the three edges, "
                   "and 6.25 is the area of one face."))
    for i, (a, b, L) in enumerate([(8, 6, 15), (5, 12, 10), (9, 4, 11), (7, 6, 16), (10, 5, 14)]):
        exact(a, b, L)
        A = Dm(a * b) / 2
        V = A * L
        q = (fig(tri_svg(a, b, L, "cm", "triangular prism, right triangle %d cm by %d cm, length %d cm" % (a, b, L))) +
             "The ends of this prism are right triangles. What is its volume?")
        pool = [cm3(a * b * L), cm3(A), cm3(a + b + L), cm2(V)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("Base (the triangle): ½ × %d × %d = %s cm². V = %s × %d = <b>%s cm³</b>. "
             "Without the ½ you get %s, a whole box, twice too big." % (a, b, N(A), N(A), L, N(V), N(a * b * L)))
        its.append(mcq(q, cm3(V), pool, e))
    for b, h, s, L in [(6, 4, 5, 10), (12, 8, 10, 9), (16, 6, 10, 12)]:
        A = Dm(b * h) / 2
        V = A * L
        slant = Dm(b * s) / 2 * L
        q = (fig(tri_end_svg(b, h, s, "cm", "triangle with base %d cm, height %d cm and sloped sides %d cm" % (b, h, s))) +
             "Each end of a prism is this triangle. The prism is %d cm long. What is its volume?" % L)
        e = ("Use the height (the dashed line), not the sloped side. Base: ½ × %d × %d = %s cm². "
             "V = %s × %d = <b>%s cm³</b>. Using the %d cm sloped side gives %s." % (b, h, N(A), N(A), L, N(V), s, N(slant)))
        its.append(mcq(q, cm3(V), [cm3(slant), cm3(b * h * L), cm2(V)], e))
    its.append(mcq("Which formula gives the volume of <b>any</b> right prism?", "area of base × height",
                   ["length + width + height", "perimeter of base × height", "area of base + height"],
                   "A prism is a stack of layers the same shape as its base. "
                   "V = <b>area of base × height</b>. For a box, the base area is l × w, so V = l × w × h."))
    exact(12, 5, 9)
    assert 12 * 5 * 9 == 540
    its.append(mcq(fig(prism_svg(12, 5, 9, "12 cm", "5 cm", "? cm", "rectangular prism 12 cm by 5 cm with an unknown height")) +
                   "The volume of this rectangular prism is 540 cm³. What is its height?", "9 cm",
                   ["45 cm", "108 cm", "480 cm"],
                   "Area of the base: 12 × 5 = 60 cm². Height = 540 ÷ 60 = <b>9 cm</b>. Check: 12 × 5 × 9 = 540. "
                   "45 divides by 12 only, and 480 subtracts."))
    assert Dm(360) / (Dm(8) * 6 / 2) == 15 and Dm(360) / 48 == Dm("7.5") and Dm(360) / 8 == 45
    its.append(mcq("A triangular prism has a volume of 360 cm³. Each end is a triangle with a base of 8 cm and a height of 6 cm. "
                   "How long is the prism?", "15 cm", ["7.5 cm", "45 cm", "336 cm"],
                   "Area of the triangle: ½ × 8 × 6 = 24 cm². Length = 360 ÷ 24 = <b>15 cm</b>. "
                   "7.5 cm forgets the ½ (360 ÷ 48)."))
    assert (5 + 9) * 4 // 2 * 12 == 336
    its.append(mcq("The base of a prism is a trapezoid with parallel sides of 5 cm and 9 cm and a height of 4 cm. "
                   "The prism is 12 cm long. What is its volume?", "336 cm³", ["672 cm³", "30 cm³", "336 cm²"],
                   "Area of the trapezoid = (5 + 9) ÷ 2 × 4 = 28 cm². V = 28 × 12 = <b>336 cm³</b>. "
                   "Forgetting to divide by 2 gives 672."))
    assert len(its) == 20, len(its)
    return {"title": "Volume of rectangular and triangular prisms", "items": its}


# ============================================================ set 2: cylinders
def set_cyl():
    its = []
    assert PI * 36 == Dm("113.04") and PI * 12 == Dm("37.68") and PI * 144 == Dm("452.16")
    its.append(mcq("A cylinder has a radius of 6 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "113.04 cm²",
                   ["37.68 cm²", "452.16 cm²", "36 cm²"],
                   "Area = π × r² = 3.14 × 6 × 6 = 3.14 × 36 = <b>113.04 cm²</b>. 37.68 is 3.14 × 12 (r × 2, not r × r), "
                   "452.16 uses 12 cm as r, and 36 forgets π."))
    assert PI * 49 == Dm("153.86") and PI * 196 == Dm("615.44") and PI * 14 == Dm("43.96") and PI * 7 == Dm("21.98")
    its.append(mcq("A can has a diameter of 14 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "153.86 cm²",
                   ["615.44 cm²", "43.96 cm²", "21.98 cm²"],
                   "r is half the diameter: 14 ÷ 2 = 7 cm. Area = 3.14 × 7 × 7 = 3.14 × 49 = <b>153.86 cm²</b>. "
                   "615.44 uses the diameter as r, and 43.96 is the circumference."))
    for i, (r, h) in enumerate([(8, 9), (5, 6), (3, 12), (6, 5), (4, 7), (9, 6), (10, 7)]):
        exact(2 * r, h)
        V = cv_(r, h)
        q = fig(cyl_svg(r, h, "cm")) + "What is the volume of this cylinder? (Use π ≈ 3.14.)"
        pool = [cm3(PI * r * 2 * h), cm3(PI * r * h), cm3(r * r * h), cm2(V), cm3(cv_(2 * r, h))]
        rr = i % 4
        pool = pool[rr:4] + pool[:rr] + pool[4:]
        e = ("V = π × r² × h = 3.14 × %d × %d × %d = %s × %d = <b>%s cm³</b>. "
             "r² means r × r = %d, not r × 2 = %d." % (r, r, h, N(PI * r * r), h, N(V), r * r, 2 * r))
        its.append(mcq(q, cm3(V), pool, e))
    for i, (d, h) in enumerate([(4, 10), (10, 6), (16, 5), (8, 7), (18, 6)]):
        exact(d, h)
        r = d // 2
        V = cv_(r, h)
        q = fig(cyl_svg(r, h, "cm", show_d=True)) + "What is the volume of this cylinder? (Use π ≈ 3.14.)"
        pool = [cm3(cv_(d, h)), cm3(PI * d * h), cm3(r * r * h), cm2(V)]
        rr = i % 3
        pool = [pool[0]] + pool[1 + rr:] + pool[1:1 + rr]
        e = ("%d cm goes all the way across the top, so it is the <b>diameter</b>. r = %d ÷ 2 = %d cm. "
             "V = 3.14 × %d × %d × %d = %s × %d = <b>%s cm³</b>. Using %d as r gives %s, 4 times too big."
             % (d, d, r, r, r, h, N(PI * r * r), h, N(V), d, N(cv_(d, h))))
        its.append(mcq(q, cm3(V), pool, e))
    for r, h in [("2.5", "12"), ("6", "4.5"), ("1.2", "5")]:
        V = cv_(r, h)
        rd = Dm(r)
        q = "A cylinder has a radius of %s cm and a height of %s cm. What is its volume? (Use π ≈ 3.14.)" % (r, h)
        e = ("r² = %s × %s = %s. V = 3.14 × %s × %s = %s × %s = <b>%s cm³</b>."
             % (r, r, N(rd * rd), N(rd * rd), h, N(PI * rd * rd), h, N(V)))
        its.append(mcq(q, cm3(V), [cm3(PI * 2 * rd * Dm(h)), cm3(cv_(2 * rd, h)), cm3(PI * rd * Dm(h)), cm3(rd * rd * Dm(h))], e))
    its.append(mcq("Which expression gives the volume of a cylinder with a diameter of 10 cm and a height of 8 cm?",
                   "3.14 × 5 × 5 × 8", ["3.14 × 10 × 10 × 8", "3.14 × 5 × 2 × 8", "3.14 × 10 × 8"],
                   "r = 10 ÷ 2 = 5 cm, and r² = 5 × 5. So V = <b>3.14 × 5 × 5 × 8</b> = 628 cm³."))
    exact(10, 8)
    assert PI * 25 * 8 == 628 and Dm(628) / (PI * 5) == 40 and Dm(628) / 25 == Dm("25.12") and Dm(628) / PI == 200
    its.append(mcq(fig(cyl_svg(5, 8, "cm", hlab="? cm")) +
                   "The volume of this cylinder is 628 cm³. What is its height? (Use π ≈ 3.14.)", "8 cm",
                   ["40 cm", "25.12 cm", "200 cm"],
                   "Base: 3.14 × 5 × 5 = 78.5 cm². Then 78.5 × h = 628, so h = 628 ÷ 78.5 = <b>8 cm</b>. "
                   "40 cm divides by 3.14 × 5 (r, not r²)."))
    assert cv_(4, 10) == Dm("502.4") and cv_(8, 5) == Dm("1004.8")
    its.append(mcq("Cylinder A has a radius of 4 cm and a height of 10 cm. Cylinder B has a radius of 8 cm and a height of 5 cm. "
                   "Which statement is true? (Use π ≈ 3.14.)", "B holds twice as much as A",
                   ["They hold the same amount", "A holds twice as much as B", "B holds 4 times as much as A"],
                   "A: 3.14 × 4 × 4 × 10 = 502.4 cm³. B: 3.14 × 8 × 8 × 5 = 1004.8 cm³. "
                   "Doubling r makes r² 4 times bigger, and halving h cuts that in half, so <b>B holds twice as much</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Volume of cylinders", "items": its}


# ============================================================ set 3: surface area of prisms
def box_e(L, W, H, u):
    a, b, c = L * W, L * H, W * H
    return ("Top and bottom: 2 × (%d × %d) = %d. Front and back: 2 × (%d × %d) = %d. Ends: 2 × (%d × %d) = %d. "
            "SA = %d + %d + %d = <b>%s %s²</b>." % (L, W, 2 * a, L, H, 2 * b, W, H, 2 * c, 2 * a, 2 * b, 2 * c,
                                                     N(sa_box(L, W, H)), u))


def set_prism_sa():
    its = []
    its.append(mcq("Which shapes make the net of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "1 triangle and 3 rectangles"],
                   "A triangular prism has a triangle at each end and a rectangle for each of the 3 sides of the triangle: "
                   "<b>2 triangles and 3 rectangles</b>."))
    its.append(mcq("Liam finds the surface area of a box. Which unit should his answer have?", "cm²",
                   ["cm³", "cm", "mL"],
                   "Surface area is an area (the paper that covers the box), so it is in square units: <b>cm²</b>. "
                   "cm³ and mL are for volume, and cm is for length."))
    for L, W, H, u in [(7, 3, 5, "cm"), (9, 4, 6, "cm"), (8, 5, 4, "cm"), (12, 4, 3, "m"), (6, 2, 8, "cm")]:
        S, V = sa_box(L, W, H), L * W * H
        q = fig(box_net_svg(L, W, H, u)) + "This is the net of a rectangular prism. What is its surface area?"
        wrong = ["%s %s²" % (N(S // 2), u), "%s %s³" % (N(V), u), "%s %s²" % (N(2 * (L * H + W * H)), u),
                 "%s %s²" % (N(6 * L * W), u)]
        its.append(mcq(q, "%s %s²" % (N(S), u), wrong, box_e(L, W, H, u) + " Add all 6 faces."))
    its.append(mcq(fig(box_net_svg(4, 4, 4, "cm", "net of a cube with 4 cm edges")) +
                   "This is the net of a cube. What is its surface area?", "96 cm²", ["64 cm³", "16 cm²", "48 cm²"],
                   "One square: 4 × 4 = 16 cm². A cube has 6 equal faces: 6 × 16 = <b>96 cm²</b>. "
                   "64 cm³ is the volume, and 48 counts only 3 faces."))
    assert 6 * 25 == 150
    its.append(mcq("A cube has a surface area of 150 cm². How long is each edge?", "5 cm", ["25 cm", "37.5 cm", "75 cm"],
                   "6 equal faces: 150 ÷ 6 = 25 cm² for one face. 5 × 5 = 25, so each edge is <b>5 cm</b>. "
                   "25 is the area of a face, not an edge."))
    exact(5, 4, 3)
    assert sa_box(5, 4, 3) == 94
    its.append(mcq(fig(prism_svg(5, 4, 3, "5 cm", "4 cm", "3 cm", "rectangular prism 5 by 4 by 3 cm")) +
                   "What is the surface area of this rectangular prism?", "94 cm²", ["47 cm²", "60 cm³", "120 cm²"],
                   box_e(5, 4, 3, "cm") + " 47 counts only the 3 faces you can see; the hidden faces count too."))
    assert sa_box(10, 6, 4) == 248
    its.append(mcq("A box is 10 cm long, 6 cm wide and 4 cm high. What is its surface area?", "248 cm²",
                   ["124 cm²", "240 cm³", "360 cm²"],
                   box_e(10, 6, 4, "cm") + " 240 is the volume (10 × 6 × 4), and 360 uses the largest face 6 times."))
    assert 10 * 8 + 2 * 10 * 5 + 2 * 8 * 5 == 260 and sa_box(10, 8, 5) == 340
    its.append(mcq("An open tray (no top) is 10 cm long, 8 cm wide and 5 cm high. What is its outside surface area?", "260 cm²",
                   ["340 cm²", "400 cm³", "180 cm²"],
                   "Bottom: 10 × 8 = 80. Two long sides: 2 × 10 × 5 = 100. Two ends: 2 × 8 × 5 = 80. "
                   "SA = 80 + 100 + 80 = <b>260 cm²</b>. 340 includes a top the tray does not have, and 180 leaves out the bottom."))
    for tri, L in [(("right", 6, 8, 10), 15), (("right", 9, 12, 15), 10), (("right", 5, 12, 13), 8),
                   (("right", 8, 15, 17), 6), (("iso", 16, 6, 10), 12)]:
        two, per, S = sa_tri(tri, L)
        if tri[0] == "right":
            _, a, b, c = tri
            bb, hh, sides = a, b, (a, b, c)
        else:
            _, bb, hh, s = tri
            sides = (s, bb, s)
        q = (fig(tri_prism_net_svg(tri, L, "cm", "net of a triangular prism, %d cm long" % L)) +
             "This is the net of a triangular prism. What is its surface area?")
        e = ("Two triangles: 2 × ½ × %d × %d = %d. Three rectangles: (%d + %d + %d) × %d = %d × %d = %d. "
             "SA = %d + %d = <b>%s cm²</b>." % (bb, hh, two, sides[0], sides[1], sides[2], L, per, L, per * L, two, per * L, N(S)))
        its.append(mcq(q, cm2(S), [cm2(2 * two + per * L), cm2(per * L), cm2(Dm(two) / 2 + per * L)], e))
    its.append(mcq("The ends of a triangular prism are right triangles with legs of 5 cm and 12 cm. "
                   "How long is the third side of each triangle?", "13 cm", ["17 cm", "169 cm", "7 cm"],
                   "Use the Pythagorean theorem: c² = 5² + 12² = 25 + 144 = 169. c = √169 = <b>13 cm</b>. "
                   "17 adds the legs, and 169 forgets the square root."))
    assert 8 * 8 + 15 * 15 == 17 * 17
    its.append(mcq("Each end of a prism is an isosceles triangle with a base of 16 cm and a height of 15 cm. "
                   "How long is each sloped side?", "17 cm", ["23 cm", "31 cm", "289 cm"],
                   "The height cuts the base in half, making a right triangle with legs of 8 cm and 15 cm. "
                   "c² = 8² + 15² = 64 + 225 = 289, so c = √289 = <b>17 cm</b>. "
                   "23 adds 8 + 15, 31 adds 16 + 15, and 289 forgets the square root."))
    exact(6, 8, 12)
    two, per, S = sa_tri(("right", 6, 8, 10), 12)
    assert S == 336 and 48 + 14 * 12 == 216 and 96 + 288 == 384 and 24 * 12 == 288
    its.append(mcq(fig(tri_svg(6, 8, 12, "cm", "triangular prism, right triangle 6 cm by 8 cm, length 12 cm")) +
                   "The ends of this prism are right triangles. Find the sloped side with the Pythagorean theorem, "
                   "then find the surface area.", "336 cm²", ["216 cm²", "384 cm²", "288 cm³"],
                   "Sloped side: √(6² + 8²) = √100 = 10 cm. Two triangles: 2 × ½ × 6 × 8 = 48. "
                   "Three rectangles: (6 + 8 + 10) × 12 = 288. SA = 48 + 288 = <b>336 cm²</b>. "
                   "216 leaves out the sloped rectangle, 384 forgets the ½, and 288 cm³ is the volume."))
    assert len(its) == 20, len(its)
    return {"title": "Surface area of prisms from nets", "items": its}


# ============================================================ set 4: surface area of cylinders
def cyl_e(r, h, u):
    r, h = Dm(str(r)), Dm(str(h))
    two, side = 2 * PI * r * r, 2 * PI * r * h
    return ("Two circles: 2 × 3.14 × %s × %s = %s. The rectangle is as long as the circumference: "
            "2 × 3.14 × %s = %s, so its area is %s × %s = %s. SA = %s + %s = <b>%s %s²</b>."
            % (N(r), N(r), N(two), N(r), N(2 * PI * r), N(2 * PI * r), N(h), N(side), N(two), N(side), N(two + side), u))


def set_cyl_sa():
    its = []
    its.append(mcq("Which shapes make the net of a cylinder?", "2 circles and 1 rectangle",
                   ["1 circle and 1 rectangle", "2 circles and 2 rectangles", "2 circles and 1 triangle"],
                   "A cylinder has a circle on the top, a circle on the bottom, and a curved side. "
                   "The curved side unrolls into a rectangle, so the net is <b>2 circles and 1 rectangle</b>."))
    its.append(mcq("In the net of a cylinder, the long side of the rectangle is the same length as …",
                   "the circumference of the circle", ["the radius of the circle", "the diameter of the circle",
                                                        "the area of the circle"],
                   "The rectangle wraps once around the circle, so its long side is <b>the circumference</b>, 2 × π × r."))
    assert 2 * PI * 6 == Dm("37.68") and PI * 6 == Dm("18.84") and PI * 36 == Dm("113.04") and 2 * PI * 12 == Dm("75.36")
    its.append(mcq("A cylinder has a radius of 6 cm. In its net, how long is the rectangle? (Use π ≈ 3.14.)", "37.68 cm",
                   ["18.84 cm", "113.04 cm", "75.36 cm"],
                   "The rectangle is as long as the circumference: 2 × 3.14 × 6 = <b>37.68 cm</b>. "
                   "18.84 forgets the 2, 113.04 is the area of the circle, and 75.36 uses 12 cm (the diameter) as r."))
    for r, h, d in [(1.5, 6, False), (5, 6, False), (3, 7, False), (4, 5, False), (6, 10, False), (4, 9, True), (5, 3, True)]:
        S = sa_cyl(r, h)
        q = fig(cyl_net_svg(r, h, "cm", show_d=d)) + "This is the net of a cylinder. What is its surface area? (Use π ≈ 3.14.)"
        rd, hd = Dm(r), Dm(h)
        one = PI * rd * rd + 2 * PI * rd * hd
        side = 2 * PI * rd * hd
        if d:
            e = ("The %d cm line goes all the way across the circle, so it is the diameter: r = %d cm. "
                 % (2 * r, r) + cyl_e(r, h, "cm"))
            wrong = [cm2(sa_cyl(2 * r, h)), cm2(side), cm2(one)]
        else:
            e = cyl_e(r, h, "cm")
            wrong = [cm2(one), cm2(side), cm2(2 * PI * 2 * rd + side), cm3(cv_(r, h))]
        its.append(mcq(q, cm2(S), wrong, e))
    for r, h, d in [(3, 8, False), (7, 5, False), (6, 5, True), (2, 10, True)]:
        exact(2 * r, h)
        S = sa_cyl(r, h)
        rd, hd = Dm(r), Dm(h)
        one = PI * rd * rd + 2 * PI * rd * hd
        side = 2 * PI * rd * hd
        q = fig(cyl_svg(r, h, "cm", show_d=d)) + "What is the surface area of this cylinder? (Use π ≈ 3.14.)"
        if d:
            e = "%d cm is the diameter, so r = %d ÷ 2 = %d cm. " % (2 * r, 2 * r, r) + cyl_e(r, h, "cm")
            wrong = [cm2(sa_cyl(2 * r, h)), cm2(side), cm2(one), cm3(cv_(r, h))]
        else:
            e = cyl_e(r, h, "cm") + " A closed cylinder has two circles, top and bottom."
            wrong = [cm2(one), cm2(side), cm3(cv_(r, h)), cm2(sa_cyl(2 * r, h))]
        its.append(mcq(q, cm2(S), wrong, e))
    assert 2 * PI * 5 * 12 == Dm("376.8") and PI * 5 * 12 == Dm("188.4") and sa_cyl(5, 12) == Dm("533.8") and cv_(5, 12) == 942
    its.append(mcq("A cylinder has a radius of 5 cm and a height of 12 cm. What is the area of its curved side only? "
                   "(Use π ≈ 3.14.)", "376.8 cm²", ["188.4 cm²", "533.8 cm²", "942 cm³"],
                   "The curved side is the rectangle in the net: circumference × height = (2 × 3.14 × 5) × 12 = 31.4 × 12 = "
                   "<b>376.8 cm²</b>. 188.4 forgets the 2, 533.8 adds the two circles, and 942 cm³ is the volume."))
    assert PI * 16 + 2 * PI * 4 * 9 == Dm("276.32") and sa_cyl(4, 9) == Dm("326.56") and 2 * PI * 4 * 9 == Dm("226.08")
    assert cv_(4, 9) == Dm("452.16")
    its.append(mcq("A cup is a cylinder with no top. Its radius is 4 cm and its height is 9 cm. What is its outside surface area? "
                   "(Use π ≈ 3.14.)", "276.32 cm²", ["326.56 cm²", "226.08 cm²", "452.16 cm³"],
                   "Bottom: 3.14 × 4 × 4 = 50.24. Curved side: 2 × 3.14 × 4 × 9 = 226.08. "
                   "SA = 50.24 + 226.08 = <b>276.32 cm²</b>. 326.56 counts a top the cup does not have."))
    S = sa_cyl("1.5", "4")
    assert S == Dm("51.81") and PI * Dm("2.25") + Dm("37.68") == Dm("44.745") and sa_cyl(3, 4) == Dm("131.88")
    its.append(mcq("A cylinder has a radius of 1.5 m and a height of 4 m. What is its surface area? (Use π ≈ 3.14.)",
                   "51.81 m²", ["44.745 m²", "131.88 m²", "37.68 m²"],
                   "Two circles: 2 × 3.14 × 1.5 × 1.5 = 14.13. Curved side: 2 × 3.14 × 1.5 × 4 = 37.68. "
                   "SA = 14.13 + 37.68 = <b>51.81 m²</b>. 44.745 counts one circle, and 131.88 uses 3 m (the diameter) as r."))
    assert 2 * PI * 5 == Dm("31.4") and Dm("31.4") * 8 == Dm("251.2") and sa_cyl(5, 8) == Dm("408.2")
    assert Dm("251.2") + PI * 25 == Dm("329.7") and Dm("251.2") + 2 * PI * 100 == Dm("879.2")
    its.append(mcq(fig(cyl_net_svg(5, 8, "cm", circ="31.4 cm")) +
                   "The rectangle in this cylinder net is 31.4 cm long. What is the surface area of the cylinder? (Use π ≈ 3.14.)",
                   "408.2 cm²", ["251.2 cm²", "329.7 cm²", "879.2 cm²"],
                   "Rectangle: 31.4 × 8 = 251.2 cm². Two circles: 2 × 3.14 × 5 × 5 = 157 cm². "
                   "SA = 251.2 + 157 = <b>408.2 cm²</b>. 251.2 is only the rectangle, and 329.7 counts one circle."))
    its.append(mcq("Which expression gives the surface area of a cylinder with a radius of 3 cm and a height of 10 cm?",
                   "2 × 3.14 × 3 × 3 + 2 × 3.14 × 3 × 10",
                   ["3.14 × 3 × 3 + 2 × 3.14 × 3 × 10", "3.14 × 3 × 3 × 10", "2 × 3.14 × 6 × 6 + 2 × 3.14 × 6 × 10"],
                   "Surface area = two circles + the rectangle = 2 × π × r² + 2 × π × r × h = "
                   "<b>2 × 3.14 × 3 × 3 + 2 × 3.14 × 3 × 10</b> = 56.52 + 188.4 = 244.92 cm². "
                   "3.14 × 3 × 3 × 10 is the volume."))
    assert sa_cyl(5, 10) == Dm("471") and 6 * 100 - Dm(471) == 129
    its.append(mcq("Which has the greater surface area: a cylinder with a radius of 5 cm and a height of 10 cm, or a cube "
                   "with 10 cm edges? (Use π ≈ 3.14.)", "The cube, by 129 cm²",
                   ["The cylinder, by 129 cm²", "The cube, by 300 cm²", "They are the same"],
                   "Cylinder: 2 × 3.14 × 5 × 5 + 2 × 3.14 × 5 × 10 = 157 + 314 = 471 cm². Cube: 6 × 10 × 10 = 600 cm². "
                   "600 − 471 = 129, so <b>the cube has 129 cm² more</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Surface area of cylinders", "items": its}


# ============================================================ set 5: word problems
def set_story():
    its = []
    assert Dm("6.5") * 4 * 10 == 260
    its.append(mcq("A juice box is 6.5 cm long, 4 cm wide and 10 cm high. How much juice can it hold?", "260 mL",
                   ["26 mL", "2.6 L", "20.5 mL"],
                   "V = 6.5 × 4 × 10 = 26 × 10 = 260 cm³. 1 cm³ holds 1 mL, so it holds <b>260 mL</b>. "
                   "(2.6 L would be 2600 mL, and 20.5 adds the edges.)"))
    assert 50 * 25 * 30 == 37500
    its.append(mcq("Mei’s fish tank is 50 cm long, 25 cm wide and 30 cm high. How many litres does it hold when full?",
                   "37.5 L", ["3.75 L", "375 L", "37" + NB + "500 L"],
                   "V = 50 × 25 × 30 = 1250 × 30 = 37" + NB + "500 cm³ = 37" + NB + "500 mL. "
                   "1000 mL = 1 L, so divide by 1000: <b>37.5 L</b>."))
    assert Dm(36000) / 1800 == 20 and Dm(36000) / 60 == 600 and Dm(36000) / 30 == 1200
    its.append(mcq("An aquarium has a base 60 cm long and 30 cm wide. Ethan pours in 36 L of water. How deep is the water?",
                   "20 cm", ["2 cm", "600 cm", "1200 cm"],
                   "36 L = 36" + NB + "000 cm³. Base area: 60 × 30 = 1800 cm². Depth = 36" + NB + "000 ÷ 1800 = <b>20 cm</b>. "
                   "600 divides by the length only."))
    assert 100 * 40 * 30 == 120000 and Dm(120) / 25 == Dm("4.8")
    its.append(mcq("Hana builds a cedar planter box that is 100 cm long, 40 cm wide and 30 cm deep inside. "
                   "Soil comes in 25 L bags. How many bags does she need to fill the box?", "5 bags",
                   ["4 bags", "48 bags", "120 bags"],
                   "V = 100 × 40 × 30 = 120" + NB + "000 cm³ = 120 L. 120 ÷ 25 = 4.8, so 4 bags are not enough. "
                   "She needs <b>5 bags</b>."))
    assert sa_box(25, 20, 8) == 1720 and 25 * 20 * 8 == 4000
    its.append(mcq("Ava wraps a gift box that is 25 cm long, 20 cm wide and 8 cm high. What is the least amount of "
                   "wrapping paper that covers the whole box?", "1720 cm²", ["860 cm²", "4000 cm²", "3000 cm²"],
                   "Top and bottom: 2 × 25 × 20 = 1000. Front and back: 2 × 25 × 8 = 400. Ends: 2 × 20 × 8 = 320. "
                   "SA = 1000 + 400 + 320 = <b>1720 cm²</b>. 4000 is the volume number, and 860 counts only 3 faces."))
    assert 2 * PI * 4 * 11 == Dm("276.32") and sa_cyl(4, 11) == Dm("376.8") and PI * 16 + Dm("276.32") == Dm("326.56")
    assert PI * 4 * 11 == Dm("138.16")
    its.append(mcq("A paper label wraps once around the curved side of a soup can. The can has a radius of 4 cm and a height of "
                   "11 cm. What is the area of the label? (Use π ≈ 3.14.)", "276.32 cm²",
                   ["376.8 cm²", "326.56 cm²", "138.16 cm²"],
                   "The label is the rectangle in the net: (2 × 3.14 × 4) × 11 = 25.12 × 11 = <b>276.32 cm²</b>. "
                   "The label does not cover the top or bottom, so 376.8 is too much. 138.16 forgets the 2."))
    V = cv_(4, "3.5")
    assert V == Dm("175.84") and cv_(8, "3.5") == Dm("703.36") and PI * 8 * Dm("3.5") == Dm("87.92")
    assert PI * 4 * Dm("3.5") == Dm("43.96")
    its.append(mcq("A tin of BC salmon is a cylinder with a radius of 4 cm and a height of 3.5 cm. About how much does it hold? "
                   "(Use π ≈ 3.14.)", "about 176 mL", ["about 703 mL", "about 88 mL", "about 44 mL"],
                   "V = 3.14 × 4 × 4 × 3.5 = 50.24 × 3.5 = 175.84 cm³. 1 cm³ = 1 mL, so it holds <b>about 176 mL</b>. "
                   "703 uses the diameter (8 cm) as r, and 88 uses r × 2 instead of r × r."))
    two, per, S = sa_tri(("iso", Dm("2.4"), Dm("1.6"), Dm(2)), Dm(3))
    assert S == Dm("23.04") and Dm("7.68") + Dm("19.2") == Dm("26.88")
    its.append(mcq("Noah’s tent at a campsite near Whistler is a triangular prism 3 m long. Each end is a triangle with a base of "
                   "2.4 m, a height of 1.6 m and sloped sides of 2 m. How much nylon covers the whole tent, including the floor?",
                   "23.04 m²", ["26.88 m²", "19.2 m²", "5.76 m³"],
                   "Two triangle ends: 2 × ½ × 2.4 × 1.6 = 3.84. Three rectangles: (2 + 2 + 2.4) × 3 = 6.4 × 3 = 19.2. "
                   "SA = 3.84 + 19.2 = <b>23.04 m²</b>. 26.88 forgets the ½, and 19.2 leaves out the ends."))
    assert Dm("2.4") * Dm("1.6") / 2 * 3 == Dm("5.76") and Dm("2.4") * 2 / 2 * 3 == Dm("7.2")
    its.append(mcq("How much space is inside Noah’s tent? (Each end is a triangle with a base of 2.4 m, a height of 1.6 m and "
                   "sloped sides of 2 m. The tent is 3 m long.)", "5.76 m³", ["7.2 m³", "11.52 m³", "1.92 m³"],
                   "Area of the end: ½ × 2.4 × 1.6 = 1.92 m². V = 1.92 × 3 = <b>5.76 m³</b>. "
                   "7.2 uses the sloped side instead of the height, 11.52 forgets the ½, and 1.92 is only the end."))
    V = cv_(25, 80)
    assert V == 157000 and cv_(50, 80) == 628000
    its.append(mcq("A rain barrel in Vancouver is a cylinder with a diameter of 50 cm and a height of 80 cm. "
                   "How many litres of rain can it hold? (Use π ≈ 3.14.)", "157 L", ["628 L", "15.7 L", "1570 L"],
                   "r = 50 ÷ 2 = 25 cm. V = 3.14 × 25 × 25 × 80 = 1962.5 × 80 = 157" + NB + "000 cm³ = 157" + NB + "000 mL. "
                   "Divide by 1000: <b>157 L</b>. 628 L uses 50 cm as the radius."))
    assert 2 * PI * 1 * Dm("2.5") == Dm("15.7") and Dm("15.7") + PI == Dm("18.84") and sa_cyl(1, "2.5") == Dm("21.98")
    assert cv_(1, "2.5") == Dm("7.85")
    its.append(mcq("A water tank in an Okanagan orchard is a cylinder with a radius of 1 m and a height of 2.5 m. "
                   "Kai paints the curved side and the top, but not the bottom. What area does he paint? (Use π ≈ 3.14.)",
                   "18.84 m²", ["21.98 m²", "15.7 m²", "7.85 m³"],
                   "Curved side: 2 × 3.14 × 1 × 2.5 = 15.7. Top: 3.14 × 1 × 1 = 3.14. Total: 15.7 + 3.14 = <b>18.84 m²</b>. "
                   "21.98 also paints the bottom, and 7.85 m³ is the volume."))
    assert Dm(9) * 4 * Dm("1.5") == 54
    its.append(mcq("A backyard pool in Kelowna is 9 m long and 4 m wide. The water is 1.5 m deep everywhere. "
                   "How many litres of water are in the pool?", "54" + NB + "000 L",
                   ["5400 L", "540" + NB + "000 L", "54 L"],
                   "V = 9 × 4 × 1.5 = 36 × 1.5 = 54 m³. 1 m³ = 1000 L, so 54 × 1000 = <b>54" + NB + "000 L</b>."))
    assert Dm(54000) / 30 == 1800 and Dm(1800) / 60 == 30
    its.append(mcq("A hose fills the same 54" + NB + "000 L pool at 30 L per minute. How many hours does it take to fill?",
                   "30 hours", ["1800 hours", "3 hours", "300 hours"],
                   "54" + NB + "000 ÷ 30 = 1800 minutes. 60 minutes = 1 hour, so 1800 ÷ 60 = <b>30 hours</b>. "
                   "1800 is the number of minutes, not hours."))
    assert cv_(5, 10) == Dm("785") and 9 * 9 * 10 == 810
    its.append(mcq("Container A is a cylinder with a radius of 5 cm and a height of 10 cm. Container B is a box "
                   "9 cm × 9 cm × 10 cm. Which holds more, and by how much? (Use π ≈ 3.14.)", "B, by 25 cm³",
                   ["A, by 25 cm³", "B, by 250 cm³", "They hold the same"],
                   "A: 3.14 × 5 × 5 × 10 = 785 cm³. B: 9 × 9 × 10 = 810 cm³. 810 − 785 = 25. "
                   "So <b>B holds more, by 25 cm³</b>."))
    V = cv_(15, 120)
    assert V == Dm("84780") and cv_(30, 120) == Dm("339120")
    its.append(mcq("A concrete footing for a deck in Surrey is a cylinder with a diameter of 30 cm and a depth of 120 cm. "
                   "How many litres of concrete fill it? (Use π ≈ 3.14.)", "84.78 L", ["339.12 L", "8.478 L", "847.8 L"],
                   "r = 30 ÷ 2 = 15 cm. V = 3.14 × 15 × 15 × 120 = 706.5 × 120 = 84" + NB + "780 cm³. "
                   "1000 cm³ = 1 L, so <b>84.78 L</b>. 339.12 L uses the diameter as r."))
    S = sa_cyl(4, 60)
    assert S == Dm("1607.68") and 2 * PI * 4 * 60 == Dm("1507.2") and Dm("1507.2") + PI * 16 == Dm("1557.44")
    assert sa_cyl(8, 60) == Dm("3416.32")
    its.append(mcq("A cardboard poster tube is a closed cylinder with a radius of 4 cm and a length of 60 cm. "
                   "How much cardboard is needed to make it, including both ends? (Use π ≈ 3.14.)", "1607.68 cm²",
                   ["1557.44 cm²", "1507.2 cm²", "3416.32 cm²"],
                   "Two ends: 2 × 3.14 × 4 × 4 = 100.48. Curved side: 2 × 3.14 × 4 × 60 = 1507.2. "
                   "SA = 100.48 + 1507.2 = <b>1607.68 cm²</b>. 1557.44 counts one end, and 3416.32 uses 8 cm (the diameter) as r."))
    V = cv_(2, 1)
    assert V == Dm("12.56") and cv_(4, 1) == Dm("50.24")
    its.append(mcq("A round tank at a salmon hatchery on Vancouver Island has a radius of 2 m. The water in it is 1 m deep. "
                   "How many litres of water are in the tank? (Use π ≈ 3.14.)", "12" + NB + "560 L",
                   ["50" + NB + "240 L", "1256 L", "6280 L"],
                   "V = 3.14 × 2 × 2 × 1 = 12.56 m³. 1 m³ = 1000 L, so 12.56 × 1000 = <b>12" + NB + "560 L</b>. "
                   "50" + NB + "240 L uses the diameter (4 m) as r, and 6280 L uses r instead of r × r."))
    assert PI * 2 * 1 * 1000 == 6280
    assert 20 * 12 * 8 == 8 * (10 * 6 * 4)
    its.append(mcq("A box is 10 cm long, 6 cm wide and 4 cm high. Arjun makes a new box with every edge twice as long. "
                   "How many times greater is the volume of the new box?", "8 times", ["2 times", "4 times", "6 times"],
                   "Old: 10 × 6 × 4 = 240 cm³. New: 20 × 12 × 8 = 1920 cm³. 1920 ÷ 240 = <b>8</b>. "
                   "Each of the three edges doubles, so the volume is 2 × 2 × 2 = 8 times greater."))
    assert sa_box(20, 12, 8) == 4 * sa_box(10, 6, 4) == 992
    its.append(mcq("For the same two boxes (10 cm × 6 cm × 4 cm and 20 cm × 12 cm × 8 cm), how many times greater is the "
                   "surface area of the new box?", "4 times", ["2 times", "8 times", "6 times"],
                   "Old SA: 2 × (60 + 40 + 24) = 248 cm². New SA: 2 × (240 + 160 + 96) = 992 cm². 992 ÷ 248 = <b>4</b>. "
                   "Each face is 2 times as long and 2 times as wide, so its area is 2 × 2 = 4 times greater."))
    assert 2 * (240 + 160 + 96) == 992
    S = sa_box(30, 20, 15)
    assert S == 2700 and S - 30 * 20 == 2100 and 30 * 20 * 15 == 9000
    its.append(mcq("Olivia makes an open-top storage bin for her classroom from plastic sheet. The bin is 30 cm long, 20 cm wide "
                   "and 15 cm high. How much plastic does she need?", "2100 cm²", ["2700 cm²", "9000 cm²", "1350 cm²"],
                   "Bottom: 30 × 20 = 600. Long sides: 2 × 30 × 15 = 900. Ends: 2 × 20 × 15 = 600. "
                   "Total: 600 + 900 + 600 = <b>2100 cm²</b>. 2700 adds a lid the bin does not have, and 9000 is the volume number. "
                   "1350 counts only one of each face."))
    assert 30 * 15 + 20 * 15 + 30 * 20 == 1350
    assert len(its) == 20, len(its)
    return {"title": "Surface area and volume word problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert cv_(3, 10) == Dm("282.6") and sa_cyl(3, 10) == Dm("244.92") and sa_box(6, 4, 5) == 148
    assert sa_tri(("right", 6, 8, 10), 10) == (48, 24, 288)
    return (
        "<h2>Volume: area of base × height</h2>"
        "<p><b>Volume</b> is the space inside a solid, in cubic units (cm³, m³). A right prism is a stack of layers shaped like "
        "its base, so for every right prism <b>V = area of base × height</b>. Find the area of the base first, then multiply.</p>"
        "<figure class='sn-fig'>" + prism_svg(6, 4, 5, "6 cm", "4 cm", "5 cm", "rectangular prism 6 by 4 by 5 cm") +
        "<figcaption>Base: 6 × 4 = 24 cm². V = 24 × 5 = 120 cm³.</figcaption></figure>"
        "<figure class='sn-fig'>" + tri_svg(6, 8, 10, "cm", "triangular prism, right triangle 6 cm by 8 cm, length 10 cm") +
        "<figcaption>Base: ½ × 6 × 8 = 24 cm². V = 24 × 10 = 240 cm³.</figcaption></figure>"
        "<h2>Cylinders</h2>"
        "<p>A cylinder is like a prism with a circle for a base. The area of the circle is π × r², so "
        "<b>V = π × r² × h</b>. Use π ≈ 3.14. The radius r goes from the centre to the edge; it is half the diameter.</p>"
        "<figure class='sn-fig'>" + cyl_svg(3, 10, "cm") +
        "<figcaption>r = 3 cm and h = 10 cm. Base: 3.14 × 3 × 3 = 28.26 cm². V = 28.26 × 10 = 282.6 cm³.</figcaption></figure>"
        + ex("Example 1", "A can has a diameter of 8 cm and a height of 12 cm. What is its volume?",
             "r = 8 ÷ 2 = 4 cm. V = 3.14 × 4 × 4 × 12 = 50.24 × 12.", "602.88 cm³")
        + "<h2>Surface area of a prism</h2>"
        "<p><b>Surface area</b> is the total area of all the faces, in square units (cm², m²). Unfold the solid into a "
        "<b>net</b> and add the areas of every face. A box has 6 rectangles. A triangular prism has 2 triangles and "
        "3 rectangles.</p>"
        "<figure class='sn-fig'>" + box_net_svg(6, 4, 5, "cm") +
        "<figcaption>Box: 2 × (6 × 4) + 2 × (6 × 5) + 2 × (4 × 5) = 48 + 60 + 40 = 148 cm².</figcaption></figure>"
        "<p>If a side of a right triangle is missing, find it with the <b>Pythagorean theorem</b>: c² = a² + b².</p>"
        + ex("Example 2", "A triangular prism is 10 cm long. Its ends are right triangles with legs of 6 cm and 8 cm. "
             "What is its surface area?",
             "Third side: √(6² + 8²) = √100 = 10 cm. Two triangles: 2 × ½ × 6 × 8 = 48. "
             "Three rectangles: (6 + 8 + 10) × 10 = 240. SA = 48 + 240.", "288 cm²")
        + "<h2>Surface area of a cylinder</h2>"
        "<p>A cylinder unfolds into 2 circles and a rectangle. The rectangle is as long as the circumference "
        "(2 × π × r) and as tall as the cylinder. So <b>SA = 2 × π × r² + 2 × π × r × h</b>.</p>"
        "<figure class='sn-fig'>" + cyl_net_svg(3, 10, "cm", circ="18.84 cm", label="net of a cylinder with radius 3 cm and height 10 cm") +
        "<figcaption>Two circles: 2 × 3.14 × 3 × 3 = 56.52 cm². Rectangle: 18.84 × 10 = 188.4 cm². "
        "SA = 56.52 + 188.4 = 244.92 cm².</figcaption></figure>"
        "<h2>Volume and capacity</h2>"
        "<p><b>Capacity</b> is how much a container can hold. 1 cm³ holds exactly 1 mL.</p>"
        + table(["Volume", "Capacity"], [
            ["1 cm³", "1 mL"],
            ["1000 cm³ (a 10 cm cube)", "1 L"],
            ["1 m³", "1000 L"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the diameter as r", "Halve the diameter first: d = 8, r = 4"],
            ["r² as r × 2", "r² = r × r: 4² = 16, not 8"],
            ["Writing cm² for a volume or cm³ for an area", "Volume: cm³, m³. Surface area: cm², m²"],
            ["Forgetting ½ for a triangle base", "Triangle area = ½ × b × h"],
            ["Using the sloped side as the height of a triangle", "Use the height that meets the base at a right angle"],
            ["Counting only one circle or only the faces you can see", "Add every face of the net: a cylinder has 2 circles"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about surface area and volume in BC?",
     "a": "The BC Grade 8 curriculum covers the surface area and volume of right prisms (including triangular prisms) and cylinders. Students use nets for surface area and V = area of base × height for volume."},
    {"q": "How do you find the surface area of a cylinder?",
     "a": "Add the two circles and the rectangle from the net: SA = 2 × π × r² + 2 × π × r × h. For r = 3 cm and h = 10 cm (π ≈ 3.14): 56.52 + 188.4 = 244.92 cm²."},
    {"q": "Why do I need the Pythagorean theorem for surface area?",
     "a": "A triangular prism has a rectangle on each side of the triangle. If one side of a right triangle is not given, find it with c² = a² + b² before you add the rectangles."},
    {"q": "What is the difference between surface area and volume?",
     "a": "Surface area is the area that covers the outside of a solid, in square units like cm². Volume is the space inside, in cubic units like cm³, and 1 cm³ holds 1 mL."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(58809)
    sets = [set_prisms(rnd), set_cyl(), set_prism_sa(), set_cyl_sa(), set_story()]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "surface-area-and-volume", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Surface Area and Volume of Prisms and Cylinders",
        "seo_title": "Grade 8 Surface Area and Volume Worksheets: Prisms and Cylinders (Free, Answer Key, BC Curriculum)",
        "short_title": "Surface area and volume",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 8: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Surface area and volume of regular solids, including triangular and other right prisms and cylinders",
        "meta_desc": "Free Grade 8 math worksheets on surface area and volume for the BC curriculum: volume of rectangular and triangular prisms, cylinders with V = πr²h (π ≈ 3.14), surface area from nets, the Pythagorean theorem for missing sides, and word problems with tents, cans, rain barrels and fish tanks. 100 questions with an answer key.",
        "key_big": "Volume = area of base × height. Surface area = the area of the whole net.",
        "key_sub": "Use the radius, not the diameter, and r² means r × r. A cylinder net is 2 circles and a rectangle as long as the circumference. Volume is in cm³, surface area in cm².",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "net of")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
