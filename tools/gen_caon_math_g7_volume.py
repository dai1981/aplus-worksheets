# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Surface area and volume of prisms and cylinders (Ontario Curriculum 2020, Spatial Sense E2.1, E2.6, E2.7)
  python3 tools/gen_caon_math_g7_volume.py
Canadian English, metric units (cm², cm³, m³, mL, L), SI number style (4 digits plain, 5+ digits with a no-break space).
Every answer is computed with decimal.Decimal (π ≈ 3.14 exactly, never float).
HTML attributes use single quotes (no backslashes in the JSON).

Pictures (checked in code):
  prisms        oblique view, hidden edges dashed, edge labels outside the solid; labels never touch
  triangular    right-triangle prism lying on a face; right-angle mark; hidden edges dashed
  cylinders     upright; top ellipse, hidden half of the bottom dashed; radius (centre to edge) or
                diameter (edge to edge) drawn on the top; height shown with a dimension line
  box nets      strip of 4 faces with the top and bottom attached (drawn to scale)
  prism nets    3 rectangles side by side with a triangle on each end; each triangle edge is glued to a
                rectangle edge of the same length (asserted)
  cylinder nets a rectangle 2πr long and h high with a circle touching the top and the bottom (to scale)
  nets          a label is either fully inside one face or outside all faces, and no line crosses it (asserted)
Wrong answers come from real student mistakes: adding the dimensions, stopping at the base area,
forgetting the ½ for a triangle, using the diameter as r, r × 2 instead of r², forgetting π,
counting only one circle or only the rectangle of a cylinder net, cm² for a volume (or cm³ for an area),
and slipping a decimal place when changing cm³ to L.
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
BASE = "#f6dcb4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)
PI = Dm("3.14")
NB = " "


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


# ============================================================ set 1: prisms
def set_prisms(rnd):
    its, seen = [], set()
    for i in range(6):
        while True:
            L, W, H = rnd.randint(5, 14), rnd.randint(2, 8), rnd.randint(3, 12)
            if (L > W and (L, W, H) not in seen and L * W != W * H and L * W != L * H
                    and L * W * H != sa_box(L, W, H) and L * W != L + W + H):
                break
        seen.add((L, W, H))
        u = "m" if i == 4 else "cm"
        if u == "m":
            L, W, H = L % 5 + 4, W % 3 + 2, H % 3 + 2
        V = L * W * H
        lab = lambda v: "%d %s" % (v, u)
        q = (fig(prism_svg(L, W, H, lab(L), lab(W), lab(H), "rectangular prism %d by %d by %d %s" % (L, W, H, u))) +
             "What is the volume of this rectangular prism?")
        pool = ["%s %s³" % (N(L * W), u), "%d %s³" % (L + W + H, u), "%s %s²" % (N(V), u), "%s %s³" % (N(sa_box(L, W, H)), u)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("Area of the base: %d × %d = %d %s². V = area of base × height = %d × %d = <b>%s %s³</b>. "
             "Multiply (do not add), and write cubic units." % (L, W, L * W, u, L * W, H, N(V), u))
        its.append(mcq(q, "%s %s³" % (N(V), u), pool, e))
    for l, w, h, u, wrong in [("2.5", "4", "6", "cm", ["600 cm³", "12.5 cm³", "60 cm²"]),
                              ("1.5", "2", "0.8", "m", ["24 m³", "4.3 m³", "0.24 m³"]),
                              ("0.5", "0.4", "0.3", "m", ["0.6 m³", "1.2 m³", "0.006 m³"])]:
        V = Dm(l) * Dm(w) * Dm(h)
        assert "%s %s³" % (N(Dm(l) + Dm(w) + Dm(h)), u) in wrong
        e = "V = %s × %s × %s = %s × %s = <b>%s %s³</b>." % (l, w, h, N(Dm(l) * Dm(w)), h, N(V), u)
        if V < 1:
            e += " Count decimal places: 0.5 × 0.4 = 0.20, and 0.20 × 0.3 = 0.060."
        q = "A rectangular prism is %s %s long, %s %s wide and %s %s high. What is its volume?" % (l, u, w, u, h, u)
        its.append(mcq(q, "%s %s³" % (N(V), u), wrong, e))
    for i, (a, b, L) in enumerate([(6, 4, 10), (8, 5, 12), (10, 6, 15), (5, 4, 9), (12, 9, 20)]):
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
    for text, a, b, L, u in [
            ("A tent is a triangular prism. Each end is a triangle with a base of 2.4 m and a height of 1.5 m. "
             "The tent is 3 m long. What is the volume of the tent?", "2.4", "1.5", "3", "m"),
            ("A wooden ramp for a skateboard park is a triangular prism. Each side of the ramp is a triangle with a base of "
             "120 cm and a height of 30 cm. The ramp is 80 cm wide. What is its volume?", "120", "30", "80", "cm")]:
        A = Dm(a) * Dm(b) / 2
        V = A * Dm(L)
        e = ("Base: ½ × %s × %s = %s %s². V = %s × %s = <b>%s %s³</b>. Without the ½ you get %s, twice too big."
             % (a, b, N(A), u, N(A), L, N(V), u, N(2 * V)))
        its.append(mcq(text, "%s %s³" % (N(V), u), ["%s %s³" % (N(2 * V), u), "%s %s³" % (N(A), u),
                                                   "%s %s³" % (N(Dm(a) + Dm(b) + Dm(L)), u)], e))
    its.append(mcq("Which formula gives the volume of <b>any</b> prism?", "area of base × height",
                   ["length + width + height", "perimeter of base × height", "area of base + height"],
                   "A prism is a stack of layers the same shape as its base. "
                   "V = <b>area of base × height</b>. For a box, the base area is l × w, so V = l × w × h."))
    its.append(mcq("A cube has edges that are 1.5 cm long. What is its volume?", "3.375 cm³",
                   ["4.5 cm³", "2.25 cm³", "3.375 cm²"],
                   "V = 1.5 × 1.5 × 1.5 = 2.25 × 1.5 = <b>3.375 cm³</b>. 1.5 × 3 = 4.5 adds the edges, "
                   "and 2.25 is the area of one face."))
    its.append(mcq("The base of a prism is a trapezoid with parallel sides of 4 cm and 6 cm and a height of 3 cm. "
                   "The prism is 10 cm long. What is its volume?", "150 cm³", ["300 cm³", "23 cm³", "150 cm²"],
                   "Area of the trapezoid = (4 + 6) ÷ 2 × 3 = 15 cm². V = 15 × 10 = <b>150 cm³</b>. "
                   "Forgetting to divide by 2 gives 300."))
    its.append(mcq("A box is 8 cm long, 5 cm wide and 3 cm high. Mei turns it so that it stands on its 5 cm × 3 cm face. "
                   "What is its volume now?", "120 cm³", ["15 cm³", "40 cm³", "24 cm³"],
                   "Turning a box does not change the space inside it. Base 5 × 3 = 15 cm², height 8 cm: "
                   "15 × 8 = <b>120 cm³</b>, the same as 8 × 5 × 3."))
    assert len(its) == 20, len(its)
    return {"title": "Volume of rectangular and triangular prisms", "items": its}


# ============================================================ set 2: cylinders
def set_cyl():
    its = []
    its.append(mcq("A cylinder has a radius of 3 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "28.26 cm²",
                   ["18.84 cm²", "9.42 cm²", "113.04 cm²"],
                   "Area = π × r² = 3.14 × 3 × 3 = 3.14 × 9 = <b>28.26 cm²</b>. 18.84 is 3.14 × 6 (r × 2, not r × r). "
                   "113.04 uses 6 cm, the diameter."))
    its.append(mcq("A can has a diameter of 10 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "78.5 cm²",
                   ["314 cm²", "31.4 cm²", "15.7 cm²"],
                   "r is half the diameter: 10 ÷ 2 = 5 cm. Area = 3.14 × 5 × 5 = 3.14 × 25 = <b>78.5 cm²</b>. "
                   "314 uses the diameter as r, and 31.4 is the circumference."))
    for i, (r, h) in enumerate([(5, 3), (4, 5), (5, 8), (6, 3), (7, 10), (3, 4), (9, 2), (8, 6)]):
        V = cv_(r, h)
        q = fig(cyl_svg(r, h, "cm")) + "What is the volume of this cylinder? (Use π ≈ 3.14.)"
        pool = [cm3(PI * r * 2 * h), cm3(PI * r * h), cm3(r * r * h), cm2(V), cm3(cv_(2 * r, h))]
        rr = i % 4
        pool = pool[rr:4] + pool[:rr] + pool[4:]
        e = ("V = π × r² × h = 3.14 × %d × %d × %d = %s × %d = <b>%s cm³</b>. "
             "r² means r × r = %d, not r × 2 = %d." % (r, r, h, N(PI * r * r), h, N(V), r * r, 2 * r))
        its.append(mcq(q, cm3(V), pool, e))
    for i, (d, h) in enumerate([(6, 5), (8, 10), (10, 4), (12, 5), (20, 3)]):
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
    for r, h in [("4", "10"), ("1.5", "8"), ("10", "2.5")]:
        V = cv_(r, h)
        rd = Dm(r)
        q = "A cylinder has a radius of %s cm and a height of %s cm. What is its volume? (Use π ≈ 3.14.)" % (r, h)
        e = ("r² = %s × %s = %s. V = 3.14 × %s × %s = %s × %s = <b>%s cm³</b>."
             % (r, r, N(rd * rd), N(rd * rd), h, N(PI * rd * rd), h, N(V)))
        its.append(mcq(q, cm3(V), [cm3(PI * 2 * rd * Dm(h)), cm3(cv_(2 * rd, h)), cm3(PI * rd * Dm(h)), cm3(rd * rd * Dm(h))], e))
    V = cv_(2, 3)
    assert V == Dm("37.68")
    its.append(mcq("A concrete pillar is a cylinder with a radius of 2 m and a height of 3 m. What is its volume? (Use π ≈ 3.14.)",
                   "37.68 m³", ["150.72 m³", "37.68 m²", "18.84 m³"],
                   "V = 3.14 × 2 × 2 × 3 = 12.56 × 3 = <b>37.68 m³</b>. 150.72 uses 4 m (the diameter) as r, "
                   "and 18.84 is 3.14 × 2 × 3 (r × 1, not r × r)."))
    its.append(mcq("Which expression gives the volume of a cylinder with a diameter of 6 cm and a height of 10 cm?",
                   "3.14 × 3 × 3 × 10", ["3.14 × 6 × 6 × 10", "3.14 × 3 × 2 × 10", "3.14 × 6 × 10"],
                   "r = 6 ÷ 2 = 3 cm, and r² = 3 × 3. So V = <b>3.14 × 3 × 3 × 10</b> = 282.6 cm³."))
    assert len(its) == 20, len(its)
    return {"title": "Volume of cylinders: V = πr²h", "items": its}


# ============================================================ set 3: missing measurement
def set_missing():
    its = []
    its.append(mcq("A prism has a volume of 96 cm³ and a base area of 12 cm². Which equation finds its height h?",
                   "12 × h = 96", ["h = 96 × 12", "12 + h = 96", "96 × h = 12"],
                   "Volume = area of base × height, so <b>12 × h = 96</b>. Then h = 96 ÷ 12 = 8 cm."))
    for V, B, u, ans in [("360", "45", "cm", "8"), ("150", "25", "cm", "6"), ("84", "24", "m", "3.5"), ("562.5", "37.5", "cm", "15")]:
        Vd, Bd = Dm(V), Dm(B)
        assert Vd / Bd == Dm(ans)
        q = "A prism has a volume of %s %s³. The area of its base is %s %s². What is its height?" % (V, u, B, u)
        e = "V = area of base × h, so %s × h = %s. h = %s ÷ %s = <b>%s %s</b>. Divide; do not subtract." % (B, V, V, B, ans, u)
        its.append(mcq(q, "%s %s" % (ans, u), ["%s %s" % (N(Vd - Bd), u), "%s %s²" % (ans, u), "%s %s³" % (ans, u)], e))
    for V, h, u, ans in [("480", "12", "cm", "40"), ("270", "7.5", "cm", "36"), ("1.2", "0.4", "m", "3")]:
        Vd, hd = Dm(V), Dm(h)
        assert Vd / hd == Dm(ans)
        q = "A prism has a volume of %s %s³ and a height of %s %s. What is the area of its base?" % (V, u, h, u)
        e = ("V = area of base × h, so area of base × %s = %s. Area of base = %s ÷ %s = <b>%s %s²</b>. "
             "An area is in square units." % (h, V, V, h, ans, u))
        its.append(mcq(q, "%s %s²" % (ans, u), ["%s %s³" % (ans, u), "%s %s²" % (N(Vd - hd), u), "%s %s²" % (N(Vd * hd), u)], e))
    for V, L, W, u, ans in [(420, 10, 6, "cm", 7), (504, 12, 7, "cm", 6), (90, 6, 5, "m", 3)]:
        assert L * W * ans == V
        q = (fig(prism_svg(L, W, ans, "%d %s" % (L, u), "%d %s" % (W, u), "? " + u,
                           "rectangular prism %d %s by %d %s with an unknown height" % (L, u, W, u))) +
             "The volume of this rectangular prism is %d %s³. What is its height?" % (V, u))
        e = ("Area of the base: %d × %d = %d %s². Height = %d ÷ %d = <b>%d %s</b>. Check: %d × %d × %d = %d."
             % (L, W, L * W, u, V, L * W, ans, u, L, W, ans, V))
        its.append(mcq(q, "%d %s" % (ans, u), ["%s %s" % (N(Dm(V) / L), u), "%s %s" % (N(Dm(V) / W), u),
                                               "%d %s" % (V - L * W, u)], e))
    for V, r, show_d, ans in [("471", 5, False, "6"), ("1130.4", 6, False, "10"), ("942", 5, True, "12")]:
        B = PI * r * r
        Vd = Dm(V)
        assert Vd / B == Dm(ans)
        q = (fig(cyl_svg(r, int(ans), "cm", show_d=show_d, hlab="? cm")) +
             "The volume of this cylinder is %s cm³. What is its height? (Use π ≈ 3.14.)" % V)
        if show_d:
            wrong = ["%s cm" % N(Vd / (PI * 4 * r * r)), "%s cm" % N(Vd / (PI * 2 * r)), "%s cm" % N(Vd / (r * r))]
            e = ("The %d cm line is the diameter, so r = %d cm. Base: 3.14 × %d × %d = %s cm². "
                 "h = %s ÷ %s = <b>%s cm</b>. Using %d cm as r gives %s cm." % (2 * r, r, r, r, N(B), V, N(B), ans, 2 * r,
                                                                                 N(Vd / (PI * 4 * r * r))))
        else:
            wrong = ["%s cm" % N(Vd / (PI * r)), "%s cm" % N(Vd / (r * r)), "%s cm" % N(Vd / PI)]
            e = ("Base: 3.14 × %d × %d = %s cm². Then %s × h = %s, so h = %s ÷ %s = <b>%s cm</b>."
                 % (r, r, N(B), N(B), V, V, N(B), ans))
        its.append(mcq(q, ans + " cm", wrong, e))
    its.append(mcq("A cylinder has a volume of 3140 cm³ and a height of 20 cm. What is the area of its base?", "157 cm²",
                   ["157 cm³", "3120 cm²", "62" + NB + "800 cm²"],
                   "V = area of base × h, so area of base = 3140 ÷ 20 = <b>157 cm²</b>. (π is already inside the base area.)"))
    for B, r in [("78.5", 5), ("200.96", 8)]:
        assert PI * r * r == Dm(B)
        q = "The circular base of a cylinder has an area of %s cm². What is its radius? (Use π ≈ 3.14.)" % B
        e = ("3.14 × r² = %s, so r² = %s ÷ 3.14 = %d. r × r = %d, so r = <b>%d cm</b>. "
             "%d is r², not r." % (B, B, r * r, r * r, r, r * r))
        its.append(mcq(q, "%d cm" % r, ["%d cm" % (r * r), "%d cm" % (2 * r), "%s cm" % N(Dm(B) / PI / 2)], e))
    assert Dm(1500) / (15 * 10) == 10
    its.append(mcq("A box holds 1.5 L when full. The inside of its base is 15 cm long and 10 cm wide. "
                   "How tall is the inside of the box?", "10 cm", ["0.01 cm", "100 cm", "1 cm"],
                   "1.5 L = 1500 mL = 1500 cm³. Area of the base: 15 × 10 = 150 cm². Height = 1500 ÷ 150 = <b>10 cm</b>. "
                   "0.01 cm forgets to change litres to cm³, and 1 cm or 100 cm slips a place (1 L = 1000 cm³)."))
    assert Dm(240) / 10 * 2 / 8 == 6
    its.append(mcq("A triangular prism has a volume of 240 cm³ and is 10 cm long. Each end is a triangle with a base of 8 cm. "
                   "What is the height of the triangle?", "6 cm", ["3 cm", "24 cm", "30 cm"],
                   "Area of the triangle: 240 ÷ 10 = 24 cm². ½ × 8 × h = 24, so 4 × h = 24 and h = <b>6 cm</b>. "
                   "3 cm forgets the ½, and 24 cm stops at the area."))
    assert Dm(6) * 5 / 2 * 15 == 225
    its.append(mcq("A triangular prism has a volume of 225 cm³. Each end is a triangle with a base of 6 cm and a height of 5 cm. "
                   "How long is the prism?", "15 cm", ["7.5 cm", "37.5 cm", "45 cm"],
                   "Area of the triangle: ½ × 6 × 5 = 15 cm². Length = 225 ÷ 15 = <b>15 cm</b>. "
                   "7.5 cm forgets the ½ (225 ÷ 30)."))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing base area or height", "items": its}


# ============================================================ set 4: surface area from nets
def box_e(L, W, H, u):
    a, b, c = L * W, L * H, W * H
    return ("Top and bottom: 2 × (%d × %d) = %d. Front and back: 2 × (%d × %d) = %d. Ends: 2 × (%d × %d) = %d. "
            "SA = %d + %d + %d = <b>%s %s²</b>." % (L, W, 2 * a, L, H, 2 * b, W, H, 2 * c, 2 * a, 2 * b, 2 * c,
                                                     N(sa_box(L, W, H)), u))


def cyl_e(r, h, u):
    r, h = Dm(str(r)), Dm(str(h))
    two, side = 2 * PI * r * r, 2 * PI * r * h
    return ("Two circles: 2 × 3.14 × %s × %s = %s. The rectangle is as long as the circumference: "
            "2 × 3.14 × %s = %s, so its area is %s × %s = %s. SA = %s + %s = <b>%s %s²</b>."
            % (N(r), N(r), N(two), N(r), N(2 * PI * r), N(2 * PI * r), N(h), N(side), N(two), N(side), N(two + side), u))


def set_nets():
    its = []
    its.append(mcq("Which shapes make the net of a cylinder?", "2 circles and 1 rectangle",
                   ["1 circle and 1 rectangle", "2 circles and 2 rectangles", "2 circles and 1 triangle"],
                   "A cylinder has a circle on the top, a circle on the bottom, and a curved side. "
                   "The curved side unrolls into a rectangle, so the net is <b>2 circles and 1 rectangle</b>."))
    its.append(mcq("In the net of a cylinder, the long side of the rectangle is the same length as …",
                   "the circumference of the circle", ["the radius of the circle", "the diameter of the circle",
                                                        "the height of the cylinder"],
                   "The rectangle wraps once around the circle, so its long side is <b>the circumference</b>, 2 × π × r."))
    for L, W, H, u in [(6, 4, 5, "cm"), (8, 3, 5, "cm"), (10, 4, 6, "cm"), (12, 5, 3, "m"), (7, 2, 9, "cm")]:
        S, V = sa_box(L, W, H), L * W * H
        q = fig(box_net_svg(L, W, H, u)) + "This is the net of a rectangular prism. What is its surface area?"
        wrong = ["%s %s²" % (N(S // 2), u), "%s %s³" % (N(V), u), "%s %s²" % (N(2 * (L * H + W * H)), u), "%s %s²" % (N(6 * L * W), u)]
        its.append(mcq(q, "%s %s²" % (N(S), u), wrong, box_e(L, W, H, u)))
    its.append(mcq(fig(box_net_svg(5, 5, 5, "cm", "net of a cube with 5 cm edges")) +
                   "This is the net of a cube. What is its surface area?", "150 cm²", ["125 cm²", "25 cm²", "75 cm²"],
                   "One square: 5 × 5 = 25 cm². A cube has 6 equal faces: 6 × 25 = <b>150 cm²</b>. "
                   "125 is the volume (5 × 5 × 5), and 75 counts only 3 faces."))
    for tri, L in [(("right", 3, 4, 5), 10), (("right", 6, 8, 10), 12), (("right", 5, 12, 13), 10), (("iso", 6, 4, 5), 10)]:
        if tri[0] == "right":
            _, a, b, c = tri
            two, per, bb, hh = a * b, a + b + c, b, a
            sides = (a, b, c)
        else:
            _, b, h, s = tri
            two, per, bb, hh = b * h, 2 * s + b, b, h
            sides = (s, b, s)
        S = two + per * L
        q = (fig(tri_prism_net_svg(tri, L, "cm", "net of a triangular prism, %d cm long" % L)) +
             "This is the net of a triangular prism. What is its surface area?")
        e = ("Two triangles: 2 × ½ × %d × %d = %d. Three rectangles: (%d + %d + %d) × %d = %d × %d = %d. "
             "SA = %d + %d = <b>%s cm²</b>." % (bb, hh, two, sides[0], sides[1], sides[2], L, per, L, per * L, two, per * L, N(S)))
        its.append(mcq(q, cm2(S), [cm2(2 * two + per * L), cm2(per * L), cm2(Dm(two) / 2 + per * L)], e))
    its.append(mcq("A cylinder has a radius of 5 cm. In its net, how long is the rectangle? (Use π ≈ 3.14.)", "31.4 cm",
                   ["15.7 cm", "78.5 cm", "62.8 cm"],
                   "The rectangle is as long as the circumference: 2 × 3.14 × 5 = <b>31.4 cm</b>. "
                   "15.7 forgets the 2, 78.5 is the area of the circle, and 62.8 uses 10 cm (the diameter) as r."))
    for r, h, d in [(3, 10, False), (7, 5, False), (5, 4, False), (4, 9, False), (6, 5, True)]:
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
    S = sa_cyl(4, 7)
    assert 2 * PI * 4 == Dm("25.12") and PI * 32 == Dm("100.48") and Dm("25.12") * 7 == Dm("175.84") and S == Dm("276.32")
    its.append(mcq(fig(cyl_net_svg(4, 7, "cm", circ="25.12 cm")) +
                   "The rectangle in this cylinder net is 25.12 cm long. What is the surface area of the cylinder? (Use π ≈ 3.14.)",
                   "276.32 cm²", ["175.84 cm²", "226.08 cm²", "577.76 cm²"],
                   "Rectangle: 25.12 × 7 = 175.84 cm². Two circles: 2 × 3.14 × 4 × 4 = 100.48 cm². "
                   "SA = 175.84 + 100.48 = <b>276.32 cm²</b>. 175.84 is only the rectangle, 226.08 counts one circle, and 577.76 uses 8 cm (the diameter) as r."))
    assert Dm("175.84") + PI * 16 == Dm("226.08") and Dm("175.84") + 2 * PI * 64 == Dm("577.76")
    S = sa_cyl(1, 2)
    assert S == Dm("18.84")
    its.append(mcq("A cylinder has a diameter of 2 m and a height of 2 m. What is its surface area? (Use π ≈ 3.14.)",
                   "18.84 m²", ["50.24 m²", "12.56 m²", "15.7 m²"],
                   "r = 2 ÷ 2 = 1 m. Two circles: 2 × 3.14 × 1 × 1 = 6.28. Rectangle: (2 × 3.14 × 1) × 2 = 12.56. "
                   "SA = 6.28 + 12.56 = <b>18.84 m²</b>. 50.24 uses 2 m as r, and 12.56 is only the rectangle."))
    assert len(its) == 20, len(its)
    return {"title": "Surface area of prisms and cylinders from nets", "items": its}


# ============================================================ set 5: capacity and word problems
def set_story():
    its = []
    its.append(mcq("A small box has a volume of 250 cm³. How many millilitres of water can it hold?", "250 mL",
                   ["2.5 mL", "25 mL", "250 L"],
                   "1 cm³ holds exactly 1 mL. So 250 cm³ = <b>250 mL</b>."))
    its.append(mcq("A jug has a volume of 4500 cm³. How many litres does it hold?", "4.5 L", ["45 L", "450 L", "0.45 L"],
                   "4500 cm³ = 4500 mL. 1000 mL = 1 L, so 4500 ÷ 1000 = <b>4.5 L</b>."))
    its.append(mcq("A water tank holds 2 m³. How many litres is that?", "2000 L", ["200 L", "20 L", "2" + NB + "000" + NB + "000 L"],
                   "1 m³ = 100 cm × 100 cm × 100 cm = 1" + NB + "000" + NB + "000 cm³ = 1000 L. So 2 m³ = <b>2000 L</b>. "
                   "(2" + NB + "000" + NB + "000 is the number of mL, not L.)"))
    its.append(mcq("A juice box is 6 cm long, 4 cm wide and 10 cm high. How much juice can it hold?", "240 mL",
                   ["20 mL", "24 mL", "2.4 L"],
                   "V = 6 × 4 × 10 = 240 cm³. 1 cm³ = 1 mL, so it holds <b>240 mL</b>. (2.4 L would be 2400 mL.)"))
    assert 60 * 30 * 40 == 72000
    its.append(mcq("Liam’s fish tank is 60 cm long, 30 cm wide and 40 cm high. How many litres does it hold when full?",
                   "72 L", ["7.2 L", "720 L", "7200 L"],
                   "V = 60 × 30 × 40 = 1800 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. Divide by 1000: <b>72 L</b>."))
    assert 60 * 30 * 35 == 63000 and 60 * 30 * 5 == 9000
    its.append(mcq("Liam fills the same fish tank (60 cm long, 30 cm wide, 40 cm high) only up to 35 cm. How much water is in it?",
                   "63 L", ["72 L", "9 L", "630 L"],
                   "Use the depth of the water, not the tank: 60 × 30 × 35 = 1800 × 35 = 63" + NB + "000 cm³ = <b>63 L</b>. "
                   "9 L is the empty space at the top."))
    its.append(mcq("A hose fills Liam’s 72 L fish tank at 4 L per minute. How many minutes does it take to fill the tank?",
                   "18 minutes", ["288 minutes", "68 minutes", "1.8 minutes"],
                   "72 ÷ 4 = <b>18 minutes</b>. Check: 18 × 4 = 72 L. (288 multiplies, and 68 subtracts.)"))
    V = cv_(4, 11)
    assert V == Dm("552.64") and cv_(8, 11) == Dm("2210.56") and PI * 8 * 11 == Dm("276.32")
    its.append(mcq("A tin of maple syrup is a cylinder with a radius of 4 cm and a height of 11 cm. "
                   "About how many millilitres of syrup can it hold? (Use π ≈ 3.14.)", "about 553 mL",
                   ["about 2211 mL", "about 276 mL", "about 55 mL"],
                   "V = 3.14 × 4 × 4 × 11 = 50.24 × 11 = 552.64 cm³. 1 cm³ = 1 mL, so it holds <b>about 553 mL</b>. "
                   "2211 uses the diameter (8 cm) as r, and 276 uses r × 2 instead of r × r."))
    assert 30 * 20 * 10 == 6000 and sa_box(30, 20, 10) == 2200
    its.append(mcq("Ava wraps a gift box that is 30 cm long, 20 cm wide and 10 cm high. What is the least amount of "
                   "wrapping paper that covers the whole box?", "2200 cm²", ["1100 cm²", "6000 cm²", "3600 cm²"],
                   "Top and bottom: 2 × 30 × 20 = 1200. Front and back: 2 × 30 × 10 = 600. Ends: 2 × 20 × 10 = 400. "
                   "SA = 1200 + 600 + 400 = <b>2200 cm²</b>. 6000 is the volume, and 1100 counts only 3 faces."))
    assert 2 * PI * 4 * 10 == Dm("251.2") and sa_cyl(4, 10) == Dm("351.68") and PI * 4 * 10 == Dm("125.6")
    its.append(mcq("A paper label wraps once around the curved side of a soup can. The can has a radius of 4 cm and a height of 10 cm. "
                   "What is the area of the label? (Use π ≈ 3.14.)", "251.2 cm²", ["351.68 cm²", "125.6 cm²", "502.4 cm²"],
                   "The label is the rectangle in the net: circumference × height = (2 × 3.14 × 4) × 10 = 25.12 × 10 = "
                   "<b>251.2 cm²</b>. The label does not cover the top and bottom, so 351.68 is too much. "
                   "502.4 is the volume number."))
    assert 3 * 2 + (Dm("2.5") * 2 + 3) * 4 == 38
    its.append(mcq("Noah’s tent is a triangular prism 4 m long. Each end is a triangle with a base of 3 m, a height of 2 m "
                   "and sloped sides of 2.5 m. How much nylon covers the whole tent, including the floor?", "38 m²",
                   ["32 m²", "44 m²", "35 m²"],
                   "Two triangle ends: 2 × ½ × 3 × 2 = 6. Three rectangles: (2.5 + 2.5 + 3) × 4 = 8 × 4 = 32. "
                   "SA = 6 + 32 = <b>38 m²</b>. 44 forgets the ½, and 32 leaves out the ends."))
    assert 120 * 40 * 30 == 144000
    its.append(mcq("Hana builds a cedar planter box that is 120 cm long, 40 cm wide and 30 cm deep inside. "
                   "Soil comes in 50 L bags. How many bags does she need to fill the box?", "3 bags",
                   ["2 bags", "29 bags", "144 bags"],
                   "V = 120 × 40 × 30 = 144" + NB + "000 cm³ = 144 L. 144 ÷ 50 = 2.88, so 2 bags are not enough. "
                   "She needs <b>3 bags</b>."))
    assert Dm(25000) / 1250 == 20 and Dm(25000) / 50 == 500
    its.append(mcq("An aquarium has a base 50 cm long and 25 cm wide. Ethan pours in 25 L of water. "
                   "How deep is the water?", "20 cm", ["2 cm", "200 cm", "500 cm"],
                   "25 L = 25" + NB + "000 cm³. Base area: 50 × 25 = 1250 cm². Depth = 25" + NB + "000 ÷ 1250 = <b>20 cm</b>. "
                   "500 divides by the length only."))
    its.append(mcq("A backyard pool is 8 m long and 4 m wide. The water is 1.5 m deep everywhere. "
                   "How many litres of water are in the pool?", "48" + NB + "000 L",
                   ["4800 L", "480" + NB + "000 L", "48 L"],
                   "V = 8 × 4 × 1.5 = 32 × 1.5 = 48 m³. 1 m³ = 1000 L, so 48 × 1000 = <b>48" + NB + "000 L</b>."))
    V = cv_(30, 90)
    assert V == Dm("254340") and cv_(60, 90) == Dm("1017360")
    its.append(mcq("A rain barrel is a cylinder with a diameter of 60 cm and a height of 90 cm. "
                   "About how many litres of rain can it hold? (Use π ≈ 3.14.)", "about 254 L",
                   ["about 1017 L", "about 2543 L", "about 25 L"],
                   "r = 60 ÷ 2 = 30 cm. V = 3.14 × 30 × 30 × 90 = 2826 × 90 = 254" + NB + "340 cm³ = 254" + NB + "340 mL, "
                   "which is <b>about 254 L</b>. 1017 L uses 60 cm as the radius."))
    assert PI * 900 + 2 * PI * 30 * 90 == Dm("19782") and sa_cyl(30, 90) == Dm("22608") and 2 * PI * 30 * 90 == Dm("16956")
    assert PI * 3600 + 2 * PI * 60 * 90 == Dm("45216")
    its.append(mcq("Arjun paints the outside of the same rain barrel (diameter 60 cm, height 90 cm). He paints "
                   "the curved side and the bottom, but not the top. What area does he paint? (Use π ≈ 3.14.)",
                   "19" + NB + "782 cm²", ["22" + NB + "608 cm²", "16" + NB + "956 cm²", "45" + NB + "216 cm²"],
                   "r = 30 cm. Bottom: 3.14 × 30 × 30 = 2826. Curved side: 2 × 3.14 × 30 × 90 = 16" + NB + "956. "
                   "Total: 2826 + 16" + NB + "956 = <b>19" + NB + "782 cm²</b>. 22" + NB + "608 also paints the top."))
    V = cv_(1, 2)
    assert V == Dm("6.28") and cv_(2, 2) == Dm("25.12")
    its.append(mcq("A water tank at a cottage is a cylinder with a radius of 1 m and a height of 2 m. "
                   "How many litres does it hold? (Use π ≈ 3.14.)", "6280 L", ["628 L", "25" + NB + "120 L", "6.28 L"],
                   "V = 3.14 × 1 × 1 × 2 = 6.28 m³. 1 m³ = 1000 L, so 6.28 × 1000 = <b>6280 L</b>. "
                   "25" + NB + "120 L uses the diameter (2 m) as r."))
    V = cv_(4, 10)
    assert V == Dm("502.4") and int(Dm(2000) / V) == 3 and int(Dm(2000) / (PI * 4 * 10)) == 15 and int(Dm(2000) / 160) == 12
    its.append(mcq("Sofia pours juice from a full 2 L jug into glasses. Each glass is a cylinder with a radius of 4 cm "
                   "and a height of 10 cm. How many glasses can she fill all the way? (Use π ≈ 3.14.)", "3 glasses",
                   ["4 glasses", "15 glasses", "12 glasses"],
                   "One glass: 3.14 × 4 × 4 × 10 = 502.4 cm³ = 502.4 mL. 2 L = 2000 mL. 2000 ÷ 502.4 ≈ 3.98, "
                   "so she can fill <b>3 glasses</b> all the way (the 4th is not full)."))
    assert cv_(3, 10) == Dm("282.6") and 7 * 7 * 6 == 294 and Dm(294) - Dm("282.6") == Dm("11.4")
    its.append(mcq("Container A is a cylinder with a radius of 3 cm and a height of 10 cm. Container B is a box 7 cm × 7 cm × 6 cm. "
                   "Which holds more, and by how much? (Use π ≈ 3.14.)", "B, by 11.4 cm³",
                   ["A, by 11.4 cm³", "B, by 114 cm³", "They hold the same"],
                   "A: 3.14 × 3 × 3 × 10 = 282.6 cm³. B: 7 × 7 × 6 = 294 cm³. 294 − 282.6 = 11.4. "
                   "So <b>B holds more, by 11.4 cm³</b>."))
    assert Dm(60) * 30 * Dm("0.025") == 45
    its.append(mcq("The town builds an outdoor skating rink in Ottawa that is 60 m long and 30 m wide. The ice is 2.5 cm thick. "
                   "How many litres of water make the ice?", "45" + NB + "000 L",
                   ["4500 L", "4" + NB + "500" + NB + "000 L", "450" + NB + "000 L"],
                   "Change 2.5 cm to metres first: 2.5 cm = 0.025 m. V = 60 × 30 × 0.025 = 1800 × 0.025 = 45 m³. "
                   "1 m³ = 1000 L, so 45 × 1000 = <b>45" + NB + "000 L</b>. Using 2.5 as metres gives 4" + NB + "500" + NB + "000 L."))
    assert len(its) == 20, len(its)
    return {"title": "Capacity and word problems", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert cv_(3, 10) == Dm("282.6") and sa_cyl(3, 10) == Dm("244.92")
    return (
        "<h2>Volume: area of base × height</h2>"
        "<p><b>Volume</b> is the space inside a solid, in cubic units (cm³, m³). A prism is a stack of layers shaped like "
        "its base, so for every prism <b>V = area of base × height</b>. Find the area of the base first, then multiply.</p>"
        "<figure class='sn-fig'>" + prism_svg(6, 4, 5, "6 cm", "4 cm", "5 cm", "rectangular prism 6 by 4 by 5 cm") +
        "<figcaption>Base: 6 × 4 = 24 cm². V = 24 × 5 = 120 cm³.</figcaption></figure>"
        "<figure class='sn-fig'>" + tri_svg(6, 4, 10, "cm", "triangular prism, right triangle 6 cm by 4 cm, length 10 cm") +
        "<figcaption>Base: ½ × 6 × 4 = 12 cm². V = 12 × 10 = 120 cm³.</figcaption></figure>"
        "<h2>Cylinders</h2>"
        "<p>A cylinder is like a prism with a circle for a base. The area of the circle is π × r², so "
        "<b>V = π × r² × h</b>. Use π ≈ 3.14. The radius r goes from the centre to the edge; it is half the diameter.</p>"
        "<figure class='sn-fig'>" + cyl_svg(3, 10, "cm") +
        "<figcaption>r = 3 cm and h = 10 cm. Base: 3.14 × 3 × 3 = 28.26 cm². V = 28.26 × 10 = 282.6 cm³.</figcaption></figure>"
        + ex("Example 1", "A can has a diameter of 8 cm and a height of 10 cm. What is its volume?",
             "r = 8 ÷ 2 = 4 cm. V = 3.14 × 4 × 4 × 10 = 50.24 × 10.", "502.4 cm³")
        + "<h2>Finding a missing measurement</h2>"
        "<p>V = area of base × height links three numbers. If you know two, divide to find the third: "
        "<b>height = V ÷ area of base</b> and <b>area of base = V ÷ height</b>.</p>"
        + ex("Example 2", "A cylinder has a volume of 471 cm³ and a radius of 5 cm. How tall is it?",
             "Base: 3.14 × 5 × 5 = 78.5 cm². Height = 471 ÷ 78.5.", "6 cm")
        + "<h2>Surface area from a net</h2>"
        "<p><b>Surface area</b> is the total area of all the faces, in square units (cm², m²). Unfold the solid into a "
        "<b>net</b> and add the areas. A cylinder unfolds into 2 circles and a rectangle. The rectangle is as long as "
        "the circumference (2 × π × r) and as tall as the cylinder.</p>"
        "<figure class='sn-fig'>" + cyl_net_svg(3, 10, "cm", circ="18.84 cm", label="net of a cylinder with radius 3 cm and height 10 cm") +
        "<figcaption>Two circles: 2 × 3.14 × 3 × 3 = 56.52 cm². Rectangle: 18.84 × 10 = 188.4 cm². "
        "SA = 56.52 + 188.4 = 244.92 cm².</figcaption></figure>"
        "<figure class='sn-fig'>" + box_net_svg(6, 4, 5, "cm") +
        "<figcaption>Box: 2 × (6 × 4) + 2 × (6 × 5) + 2 × (4 × 5) = 48 + 60 + 40 = 148 cm².</figcaption></figure>"
        "<h2>Volume and capacity</h2>"
        "<p><b>Capacity</b> is how much a container can hold. 1 cm³ holds exactly 1 mL.</p>"
        + table(["Volume", "Capacity"], [
            ["1 cm³", "1 mL"],
            ["1000 cm³ (a 10 cm cube)", "1 L"],
            ["1 m³", "1000 L"],
        ])
        + ex("Example 3", "A fish tank is 60 cm × 30 cm × 40 cm. How many litres does it hold?",
             "V = 60 × 30 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. Divide by 1000.", "72 L")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Using the diameter as r", "Halve the diameter first: d = 8, r = 4"],
            ["r² as r × 2", "r² = r × r: 4² = 16, not 8"],
            ["Forgetting ½ for a triangle base", "Triangle area = ½ × b × h"],
            ["Counting only one circle in a cylinder net", "A cylinder has 2 circles: top and bottom"],
            ["Writing cm² for a volume or cm³ for an area", "Volume: cm³, m³. Surface area: cm², m²"],
            ["Subtracting to find a missing height", "Divide: h = V ÷ area of base"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about surface area and volume in Ontario?",
     "a": "In Grade 7 Spatial Sense, students find the volume of prisms and cylinders with V = area of base × height, find a missing measurement when two are known, use nets to find the surface area of prisms and cylinders, and use 1 mL = 1 cm³."},
    {"q": "How do you find the volume of a cylinder in Grade 7?",
     "a": "Find the area of the circular base with π × r × r (π ≈ 3.14), then multiply by the height. For r = 3 cm and h = 10 cm: 3.14 × 9 × 10 = 282.6 cm³."},
    {"q": "How do you find the surface area of a cylinder from its net?",
     "a": "The net is 2 circles and a rectangle. Add the two circles (2 × π × r²) and the rectangle, which is the circumference times the height (2 × π × r × h)."},
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
    rnd = random.Random(47819)
    sets = [set_prisms(rnd), set_cyl(), set_missing(), set_nets(), set_story()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "surface-area-and-volume", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Surface Area and Volume of Prisms and Cylinders",
        "seo_title": "Grade 7 Surface Area and Volume Worksheets: Prisms and Cylinders (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Surface area and volume",
        "domain": "Spatial Sense",
        "standard_code": "Grade 7: E2.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the relationship between the area of the base and height to determine the volume of prisms and cylinders, and determine the missing measurement when given two of the three",
        "meta_desc": "Free Grade 7 math worksheets on surface area and volume for the Ontario curriculum: volume of rectangular and triangular prisms, cylinders with V = πr²h (π ≈ 3.14), missing base area or height, surface area from nets, and capacity in mL and L with fish tanks, cans and rain barrels. 100 questions with an answer key.",
        "key_big": "Volume = area of base × height. Cylinder: V = π × r² × h. Surface area = the area of the whole net.",
        "key_sub": "Use the radius, not the diameter, and r² means r × r. A cylinder net is 2 circles and a rectangle as long as the circumference. Volume is in cm³, surface area in cm², and 1 cm³ holds 1 mL.",
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
