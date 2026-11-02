# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Volume of prisms and cylinders (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g7_volume.py
Canadian English, metric units (cm³, m³, mL, L), SI number style (4 digits plain, 5+ digits with a no-break space).
Every answer is computed with decimal.Decimal (π ≈ 3.14 exactly, never float).
HTML attributes use single quotes (no backslashes in the JSON).

Pictures (checked in code):
  cube prisms   every unit cube is drawn (back to front); the number of cubes must equal l × w × h
  prisms        oblique view, hidden edges dashed, edge labels outside the solid; labels never touch
  triangular    right-triangle prism lying on a face; right-angle mark; hidden edges dashed
  cylinders     upright; top ellipse, hidden half of the bottom dashed; radius (centre to edge) or
                diameter (edge to edge) drawn on the top; height shown with a dimension line
Wrong answers come from real student mistakes: adding the dimensions, stopping at the base area,
forgetting the ½ for a triangle, using the diameter as r, r × 2 instead of r², forgetting π,
cm² instead of cm³, and slipping a decimal place when changing cm³ to L.
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
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


class Canvas:
    """Collects shapes and text, tracks the bounding box, then writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
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

    def svg(self, label, pad=5):
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


# ------------------------------------------------------------ unit-cube pictures
def cubes_box(l, w, h):
    return [(x, y, z) for x in range(l) for y in range(h) for z in range(w)]


def cube_svg(cubes, label, k=22, gap=0.0):
    """Draw every unit cube back to front. gap > 0 pulls the layers apart."""
    keys = set(cubes)
    assert len(keys) == len(cubes)
    cv = Canvas()
    for x, y, z in sorted(cubes, key=lambda c: (-c[2], c[1], c[0])):
        Y = y * (1 + gap)
        p = lambda a, b, c: proj(x + a, Y + b, z + c, k)
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], FILL)
        if gap or (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], TOP)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], SIDE)
    return cv.svg(label)


def prism_cubes(l, w, h, label=None, gap=0.0):
    cubes = cubes_box(l, w, h)
    assert len(cubes) == l * w * h
    return cube_svg(cubes, label or "rectangular prism made of %d centimetre cubes" % (l * w * h), gap=gap)


def visible_cubes(l, w, h):
    """Cubes that show at least one face: front, top or right side."""
    return l * w * h - (l - 1) * (w - 1) * (h - 1)


# ------------------------------------------------------------ prisms with labels
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
    if lab_l:
        x, y = p(dL / 2, 0, 0)
        cv.text(x, y + 17, lab_l, 16, col=col(lab_l))
    if lab_h:
        x, y = p(0, dH / 2, 0)
        cv.text(x - 8, y, lab_h, 16, "end", col(lab_h))
    if lab_w:
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


def cyl_svg(r, h, u, show_d=False, label=None):
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
    cv.text(xd + 9, -H / 2, "%s %s" % (N(h), u), 16, "start")
    what = "diameter" if show_d else "radius"
    return cv.svg(label or "cylinder with %s %s %s and height %s %s" % (what, N(2 * r if show_d else r), u, N(h), u))


# ============================================================ set 1: count cubes
def pick_dims(rnd, seen, lr, wr, hr):
    while True:
        l, w, h = rnd.randint(*lr), rnd.randint(*wr), rnd.randint(*hr)
        if (l, w, h) in seen or l < w or (l - 1) * (w - 1) * (h - 1) == 0:
            continue
        seen.add((l, w, h))
        return l, w, h


def set_count(rnd):
    its, seen = [], set()
    its.append(mcq("A cube has edges that are 1 cm long. What is its volume?", "1 cm³", ["1 cm²", "3 cm³", "1 cm"],
                   "A cube with 1 cm edges is the unit for volume: <b>1 cm³</b> (one cubic centimetre). "
                   "1 cm² is the area of one face, and 1 cm is the length of one edge."))
    for i in range(7):
        l, w, h = pick_dims(rnd, seen, (2, 5), (2, 3), (2, 4))
        V, vis = l * w * h, visible_cubes(l, w, h)
        faces = l * h + l * w + w * h
        q = fig(prism_cubes(l, w, h)) + "Each small cube is 1 cm³. What is the volume of this prism?"
        e = ("Each layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = <b>%d cm³</b>. "
             "Count the hidden cubes, too: only %d cubes show a face." % (w, l, l * w, h, l * w, h, V, vis))
        its.append(mcq(q, cm3(V), [cm3(vis), cm3(faces), cm3(l + w + h), "%d cm²" % V, cm3(l * h)], e))
    used = set()
    for i in range(4):
        while True:
            l, w, h = pick_dims(rnd, seen, (3, 5), (2, 4), (2, 4))
            if l != w and (l, w) not in used and h != w:
                break
        used.add((l, w))
        q = fig(prism_cubes(l, w, h)) + "How many centimetre cubes are in the <b>bottom layer</b> of this prism?"
        e = ("The bottom layer is %d cubes across and %d cubes deep: %d × %d = <b>%d</b> cubes. "
             "The front face shows %d × %d = %d cubes, but that is not a layer." % (l, w, l, w, l * w, l, h, l * h))
        its.append(mcq(q, str(l * w), [l * h, l + w, l * w * h, w * h, l * w + h], e))
    for i in range(4):
        l, w, h = pick_dims(rnd, seen, (3, 5), (2, 3), (2, 4))
        V = l * w * h
        q = (fig(prism_cubes(l, w, h, "rectangular prism of centimetre cubes with its layers pulled apart", gap=0.45)) +
             "The layers of this prism are pulled apart. Each cube is 1 cm³. What is the volume of the whole prism?")
        e = "One layer: %d × %d = %d cubes. %d layers: %d × %d = <b>%d cm³</b>." % (l, w, l * w, h, l * w, h, V)
        its.append(mcq(q, cm3(V), [cm3(l * w), cm3(l * w + h), cm3(visible_cubes(l, w, h)), cm3(l * w * (h - 1))], e))
    for r, c, n, thing in [(6, 4, 5, "box"), (8, 5, 3, "tray")]:
        V = r * c * n
        q = ("The bottom layer of a %s holds %d rows of %d centimetre cubes. The %s holds %d layers. "
             "What is the volume of the %s?" % (thing, r, c, thing, n, thing))
        e = "One layer: %d × %d = %d cubes. %d layers: %d × %d = <b>%d cm³</b>." % (r, c, r * c, n, r * c, n, V)
        its.append(mcq(q, cm3(V), [cm3(r + c + n), cm3(r * c), cm3(r * c + n)], e))
    its.append(mcq("How many 1 cm cubes fit in a box that is 10 cm long, 6 cm wide and 4 cm high?", "240",
                   ["20", "60", "64"],
                   "One layer on the bottom: 10 × 6 = 60 cubes. The box is 4 cm high, so 4 layers: 60 × 4 = <b>240</b> cubes. "
                   "(20 adds the edges, 60 is only one layer, and 64 adds the height to one layer.)"))
    its.append(mcq("A box holds 60 centimetre cubes in each layer. It holds 420 cubes in all. How many layers are there?",
                   "7", ["360", "480", "6"],
                   "Cubes in one layer × number of layers = total, so 60 × ? = 420. 420 ÷ 60 = <b>7</b> layers. "
                   "(360 subtracts and 480 adds.)"))
    assert len(its) == 20, len(its)
    return {"title": "Volume by counting cubes", "items": its}


# ============================================================ set 2: V = l × w × h
def set_rect(rnd):
    its, seen = [], set()
    for i in range(8):
        while True:
            L, W, H = rnd.randint(5, 15), rnd.randint(2, 9), rnd.randint(2, 12)
            if L > W and (L, W, H) not in seen and L * W != W * H and L * W * H != 2 * (L * W + L * H + W * H):
                break
        seen.add((L, W, H))
        u = "m" if i in (3, 6) else "cm"
        if u == "m":
            L, W, H = L % 6 + 3, W % 3 + 2, H % 4 + 2
            if L <= W:
                L = W + 2
        V, SA = L * W * H, 2 * (L * W + L * H + W * H)
        lab = lambda v: "%d %s" % (v, u)
        q = (fig(prism_svg(L, W, H, lab(L), lab(W), lab(H), "rectangular prism %d by %d by %d %s" % (L, W, H, u))) +
             "What is the volume of this rectangular prism?")
        pool = ["%s %s³" % (N(L * W), u), "%d %s³" % (L + W + H, u), "%s %s²" % (N(V), u), "%s %s³" % (N(SA), u)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("V = l × w × h = %d × %d × %d = %d × %d = <b>%s %s³</b>. Multiply all three edges (do not add them), "
             "and write cubic units." % (L, W, H, L * W, H, N(V), u))
        its.append(mcq(q, "%s %s³" % (N(V), u), pool, e))
    dec = [("2.5", "4", "6", "cm", ["600 cm³", "12.5 cm³", "60 cm²"], True),
           ("1.5", "2", "0.8", "m", ["24 m³", "4.3 m³", "0.24 m³"], True),
           ("3.2", "5", "10", "cm", ["1600 cm³", "16 cm³", "18.2 cm³"], False),
           ("0.5", "0.4", "0.3", "m", ["0.6 m³", "1.2 m³", "0.006 m³"], False)]
    for l, w, h, u, wrong, pic in dec:
        V = Dm(l) * Dm(w) * Dm(h)
        S = Dm(l) + Dm(w) + Dm(h)
        lw = Dm(l) * Dm(w)
        e = "V = %s × %s × %s = %s × %s = <b>%s %s³</b>." % (l, w, h, N(lw), h, N(V), u)
        if V < 1:
            e += " Check the decimal places: 0.5 × 0.4 = 0.2, and 0.2 × 0.3 = 0.06 (3 decimal places in all, 0.060)."
        else:
            e += " Count the decimal places to check: the answer is not %s." % wrong[0]
        if pic:
            q = (fig(prism_svg(float(l), float(w), float(h), "%s %s" % (l, u), "%s %s" % (w, u), "%s %s" % (h, u),
                               "rectangular prism %s by %s by %s %s" % (l, w, h, u))) +
                 "What is the volume of this rectangular prism?")
        else:
            q = "A rectangular prism is %s %s long, %s %s wide and %s %s high. What is its volume?" % (l, u, w, u, h, u)
        assert "%s %s³" % (N(S), u) in wrong and val(wrong[0])[1] in (val("%s %s³" % (N(V * 10), u))[1],
                                                                       val("%s %s³" % (N(V / 10), u))[1])
        its.append(mcq(q, "%s %s³" % (N(V), u), wrong, e))
    for s in ["5", "8", "1.5"]:
        S = Dm(s)
        V = S ** 3
        q = "A cube has edges that are %s cm long. What is its volume?" % s
        e = ("All the edges of a cube are equal, so V = %s × %s × %s = %s × %s = <b>%s cm³</b>. "
             "%s × 3 = %s is not the volume." % (s, s, s, N(S * S), s, N(V), s, N(3 * S)))
        its.append(mcq(q, cm3(V), [cm3(3 * S), cm3(S * S), N(V) + " cm²"], e))
    its.append(mcq("A box is 6 cm long, 4 cm wide and 3 cm high. Which expression gives its volume?", "6 × 4 × 3",
                   ["6 + 4 + 3", "6 × 4", "6 × 4 + 3"],
                   "Volume = length × width × height = <b>6 × 4 × 3</b> = 72 cm³. 6 × 4 is only the area of the base."))
    its.append(mcq("A shipping crate is 12 m long, 5 m wide and 2.5 m high. Which expression gives its volume?",
                   "12 × 5 × 2.5", ["12 + 5 + 2.5", "12 × 5 + 2.5", "(12 + 5) × 2.5"],
                   "Length × width × height = <b>12 × 5 × 2.5</b> = 60 × 2.5 = 150 m³. (12 + 5) × 2.5 adds two edges first."))
    for V, a, b, an, bn, miss, ans, wrong in [
            (240, 10, 4, "long", "wide", "high", "6", ["24 cm", "60 cm", "226 cm"]),
            (360, 12, 5, "long", "high", "wide", "6", ["30 cm", "72 cm", "343 cm"]),
            ("36", "4", "2.5", "long", "wide", "high", "3.6", ["9 cm", "14.4 cm", "29.5 cm"])]:
        Vd, ad, bd = Dm(str(V)), Dm(str(a)), Dm(str(b))
        assert Vd / (ad * bd) == Dm(ans)
        u = "m" if V == "36" else "cm"
        wrong = [w.replace(" cm", " " + u) for w in wrong]
        q = "A rectangular prism has a volume of %s %s³. It is %s %s %s and %s %s %s. How %s is it?" % (
            N(Vd), u, N(ad), u, an, N(bd), u, bn, miss)
        e = ("%s × %s × ? = %s, so %s × ? = %s. %s ÷ %s = <b>%s %s</b>. Check: %s × %s × %s = %s."
             % (N(ad), N(bd), N(Vd), N(ad * bd), N(Vd), N(Vd), N(ad * bd), ans, u, N(ad), N(bd), ans, N(Vd)))
        its.append(mcq(q, "%s %s" % (ans, u), wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Rectangular prisms: V = l × w × h", "items": its}


# ============================================================ set 3: base area × height
def set_base():
    its = []
    for B, h, wrong in [("24", "5", None), ("45", "12", None), ("12.5", "8", None), ("36", "7.5", None)]:
        Bd, hd = Dm(B), Dm(h)
        V = Bd * hd
        q = "The base of a prism has an area of %s cm². The prism is %s cm high. What is its volume?" % (B, h)
        e = "V = area of base × height = %s × %s = <b>%s cm³</b>. (Adding gives %s, which is not a volume.)" % (
            B, h, N(V), N(Bd + hd))
        its.append(mcq(q, cm3(V), [cm3(Bd + hd), N(V) + " cm²", cm3(Bd)], e))
    for i, (a, b, L) in enumerate([(6, 4, 10), (8, 5, 12), (10, 6, 15), (5, 4, 9)]):
        A = Dm(a * b) / 2
        V = A * L
        q = (fig(tri_svg(a, b, L, "cm", "triangular prism, triangle %d cm by %d cm, length %d cm" % (a, b, L))) +
             "The ends of this prism are right triangles. What is its volume?")
        pool = [cm3(a * b * L), cm3(A), cm3(a + b + L), N(V) + " cm²"]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("Base (the triangle): %s × %d × %d = %s cm². V = %s × %d = <b>%s cm³</b>. "
             "Do not forget the %s: %d × %d × %d = %s is a whole box, twice too big."
             % ("½", a, b, N(A), N(A), L, N(V), "½", a, b, L, N(a * b * L)))
        its.append(mcq(q, cm3(V), pool, e))
    for text, a, b, L, u in [
            ("A tent is shaped like a triangular prism. Each end is a triangle with a base of 2.4 m and a height of 1.5 m. "
             "The tent is 3 m long. What is the volume of the tent?", "2.4", "1.5", "3", "m"),
            ("A chocolate box is a triangular prism. Each end is a triangle with a base of 4 cm and a height of 3.5 cm. "
             "The box is 20 cm long. What is its volume?", "4", "3.5", "20", "cm"),
            ("A wooden ramp for a skateboard park is a triangular prism. Each side of the ramp is a triangle with a base of "
             "120 cm and a height of 30 cm. The ramp is 80 cm wide. What is its volume?", "120", "30", "80", "cm")]:
        A = Dm(a) * Dm(b) / 2
        V = A * Dm(L)
        e = ("Base: ½ × %s × %s = %s %s². V = %s × %s = <b>%s %s³</b>. Without the ½ you get %s, twice too big."
             % (a, b, N(A), u, N(A), L, N(V), u, N(2 * V)))
        its.append(mcq(text, "%s %s³" % (N(V), u), ["%s %s³" % (N(2 * V), u), "%s %s³" % (N(A), u),
                                                   "%s %s³" % (N(Dm(a) + Dm(b) + Dm(L)), u)], e))
    its.append(mcq("A prism has a base shaped like a parallelogram. The parallelogram has a base of 8 cm, a slanted side of 6 cm "
                   "and a height of 5 cm. The prism is 12 cm long. What is its volume?", "480 cm³",
                   ["576 cm³", "25 cm³", "480 cm²"],
                   "Area of the parallelogram = base × height = 8 × 5 = 40 cm² (use the height, not the slanted side). "
                   "V = 40 × 12 = <b>480 cm³</b>. 8 × 6 × 12 = 576 uses the slanted side."))
    its.append(mcq("The base of a prism is a trapezoid with parallel sides of 4 cm and 6 cm and a height of 3 cm. "
                   "The prism is 10 cm long. What is its volume?", "150 cm³", ["300 cm³", "23 cm³", "150 cm²"],
                   "Area of the trapezoid = (4 + 6) ÷ 2 × 3 = 15 cm². V = 15 × 10 = <b>150 cm³</b>. "
                   "Forgetting to divide by 2 gives 300."))
    its.append(mcq("A box is 8 cm long, 5 cm wide and 3 cm high. Mei turns it so that it stands on its 5 cm × 3 cm face. "
                   "What is its volume now?", "120 cm³", ["15 cm³", "40 cm³", "24 cm³"],
                   "Turning a box does not change the space inside it. Base 5 × 3 = 15 cm², height 8 cm: 15 × 8 = <b>120 cm³</b>, "
                   "the same as 8 × 5 × 3."))
    for V, B, ans, wrong, u in [("360", "45", "8", ["315 cm", "405 cm", "8 cm³"], "cm"),
                                ("150", "25", "6", ["125 cm", "3 cm", "12 cm"], "cm"),
                                ("84", "24", "3.5", ["60 m", "0.35 m", "108 m"], "m")]:
        assert Dm(V) / Dm(B) == Dm(ans)
        q = "A prism has a volume of %s %s³. The area of its base is %s %s². What is its height?" % (V, u, B, u)
        e = "V = area of base × h, so %s × h = %s. h = %s ÷ %s = <b>%s %s</b>." % (B, V, V, B, ans, u)
        if ans == "6":
            e += " The base area is already given, so do not halve or double anything."
        its.append(mcq(q, "%s %s" % (ans, u), wrong, e))
    its.append(mcq("Which formula gives the volume of <b>any</b> prism?", "area of base × height",
                   ["length + width + height", "perimeter of base × height", "area of base + height"],
                   "Every prism is a stack of layers the same shape as its base. "
                   "V = <b>area of base × height</b>. For a box, the base area is l × w, so V = l × w × h."))
    its.append(mcq("A prism has a base area of 30 cm² and a height of 4 cm. The height changes to 8 cm and the base stays the same. "
                   "What is the new volume?", "240 cm³", ["480 cm³", "124 cm³", "120 cm³"],
                   "Old volume: 30 × 4 = 120 cm³. New volume: 30 × 8 = <b>240 cm³</b>. "
                   "Doubling the height doubles the volume (not 4 times)."))
    its.append(mcq("A cylinder has a base area of 28.26 cm² and a height of 10 cm. What is its volume?", "282.6 cm³",
                   ["38.26 cm³", "2826 cm³", "282.6 cm²"],
                   "A cylinder is like a prism with a circle for a base: V = area of base × height = 28.26 × 10 = <b>282.6 cm³</b>. "
                   "Multiplying by 10 moves the decimal point one place, not two."))
    assert len(its) == 20, len(its)
    return {"title": "Volume = area of base × height", "items": its}


# ============================================================ set 4: cylinders
def cv(r, h):
    return PI * Dm(r) * Dm(r) * Dm(h)


def set_cyl(rnd):
    its = []
    its.append(mcq("A cylinder has a radius of 3 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "28.26 cm²",
                   ["18.84 cm²", "9.42 cm²", "113.04 cm²"],
                   "Area = π × r × r = 3.14 × 3 × 3 = 3.14 × 9 = <b>28.26 cm²</b>. 18.84 is 3.14 × 6 (r × 2, not r × r). "
                   "113.04 uses 6 cm, the diameter."))
    its.append(mcq("A can has a diameter of 10 cm. What is the area of its circular base? (Use π ≈ 3.14.)", "78.5 cm²",
                   ["314 cm²", "31.4 cm²", "15.7 cm²"],
                   "r is half the diameter: 10 ÷ 2 = 5 cm. Area = 3.14 × 5 × 5 = 3.14 × 25 = <b>78.5 cm²</b>. "
                   "314 uses the diameter as r, and 31.4 is the circumference."))
    used = set()
    for i, (r, h) in enumerate([(3, 10), (4, 5), (5, 8), (6, 3), (7, 10), (3, 4), (8, 6), (10, 5)]):
        V = cv(r, h)
        used.add((r, h))
        q = fig(cyl_svg(r, h, "cm")) + "What is the volume of this cylinder? (Use π ≈ 3.14.)"
        pool = [cm3(PI * r * 2 * h), cm3(PI * r * h), cm3(r * r * h), N(V) + " cm²", cm3(cv(2 * r, h))]
        rr = i % 4
        pool = pool[rr:4] + pool[:rr] + pool[4:]
        e = ("V = π × r² × h = 3.14 × %d × %d × %d = 3.14 × %d × %d = %s × %d = <b>%s cm³</b>. "
             "r² means r × r = %d, not r × 2 = %d." % (r, r, h, r * r, h, N(PI * r * r), h, N(V), r * r, 2 * r))
        its.append(mcq(q, cm3(V), pool, e))
    for i, (d, h) in enumerate([(6, 5), (8, 10), (10, 4), (12, 5), (14, 2)]):
        r = d // 2
        V = cv(r, h)
        q = fig(cyl_svg(r, h, "cm", show_d=True)) + "What is the volume of this cylinder? (Use π ≈ 3.14.)"
        pool = [cm3(cv(d, h)), cm3(PI * d * h), cm3(r * r * h), N(V) + " cm²"]
        rr = i % 3
        pool = [pool[0]] + pool[1 + rr:] + pool[1:1 + rr]
        e = ("%d cm goes all the way across the top, so it is the <b>diameter</b>. r = %d ÷ 2 = %d cm. "
             "V = 3.14 × %d × %d × %d = %s × %d = <b>%s cm³</b>. Using %d as r gives %s, 4 times too big."
             % (d, d, r, r, r, h, N(PI * r * r), h, N(V), d, N(cv(d, h))))
        its.append(mcq(q, cm3(V), pool, e))
    for r, h in [("4", "10"), ("1.5", "8"), ("10", "2.5")]:
        V = cv(r, h)
        rd = Dm(r)
        q = "A cylinder has a radius of %s cm and a height of %s cm. What is its volume? (Use π ≈ 3.14.)" % (r, h)
        e = ("r² = %s × %s = %s. V = 3.14 × %s × %s = %s × %s = <b>%s cm³</b>."
             % (r, r, N(rd * rd), N(rd * rd), h, N(PI * rd * rd), h, N(V)))
        its.append(mcq(q, cm3(V), [cm3(PI * 2 * rd * Dm(h)), cm3(cv(2 * rd, h)), cm3(PI * rd * Dm(h)), cm3(rd * rd * Dm(h))], e))
    for V, r, ans, wrong in [("471", 5, "6", ["30 cm", "18.84 cm", "150 cm"]),
                             ("1130.4", 6, "10", ["60 cm", "31.4 cm", "360 cm"])]:
        B = PI * r * r
        assert Dm(V) / B == Dm(ans)
        q = ("A cylinder has a volume of %s cm³ and a radius of %d cm. What is its height? (Use π ≈ 3.14.)" % (V, r))
        e = ("Area of the base: 3.14 × %d × %d = %s cm². Then %s × h = %s, so h = %s ÷ %s = <b>%s cm</b>."
             % (r, r, N(B), N(B), V, V, N(B), ans))
        its.append(mcq(q, ans + " cm", wrong, e))
    for V, r, ans, wrong in [("471", 5, "6", ["30 cm", "18.84 cm", "150 cm"]), ("1130.4", 6, "10", ["60 cm", "31.4 cm", "360 cm"])]:
        assert Dm(V) / (PI * r) == Dm(wrong[0].split()[0]) and Dm(V) / (r * r) == Dm(wrong[1].split()[0])
        assert Dm(V) / PI == Dm(wrong[2].split()[0])
    assert len(its) == 20, len(its)
    return {"title": "Cylinders: V = πr²h", "items": its}


# ============================================================ set 5: capacity and word problems
def set_story():
    its = []
    its.append(mcq("A small box has a volume of 250 cm³. How many millilitres of water can it hold?", "250 mL",
                   ["2.5 mL", "25 mL", "250 L"],
                   "1 cm³ holds exactly 1 mL. So 250 cm³ = <b>250 mL</b>."))
    its.append(mcq("A cube-shaped container is 10 cm × 10 cm × 10 cm inside. How much water does it hold when full?", "1 L",
                   ["100 mL", "10 L", "30 mL"],
                   "V = 10 × 10 × 10 = 1000 cm³ = 1000 mL = <b>1 L</b>. (10 × 10 = 100 is only the base, "
                   "and 30 adds the edges.)"))
    its.append(mcq("A jug has a volume of 3500 cm³. How many litres does it hold?", "3.5 L", ["35 L", "350 L", "0.35 L"],
                   "3500 cm³ = 3500 mL. 1000 mL = 1 L, so 3500 ÷ 1000 = <b>3.5 L</b>."))
    its.append(mcq("A water tank holds 2 m³. How many litres is that?", "2000 L", ["200 L", "20 L", "2" + NB + "000" + NB + "000 L"],
                   "1 m³ = 100 cm × 100 cm × 100 cm = 1" + NB + "000" + NB + "000 cm³ = 1000 L. So 2 m³ = <b>2000 L</b>. "
                   "(2" + NB + "000" + NB + "000 is the number of mL, not L.)"))
    assert 100 ** 3 == 1000000
    its.append(mcq("Liam’s fish tank is 60 cm long, 30 cm wide and 40 cm high. How many litres does it hold when full?",
                   "72 L", ["7.2 L", "720 L", "7200 L"],
                   "V = 60 × 30 × 40 = 1800 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. "
                   "Divide by 1000: <b>72 L</b>."))
    its.append(mcq("Liam fills the same fish tank (60 cm long, 30 cm wide, 40 cm high) only up to 35 cm. How much water is in it?",
                   "63 L", ["72 L", "9 L", "630 L"],
                   "Use the height of the water, not the tank: 60 × 30 × 35 = 1800 × 35 = 63" + NB + "000 cm³ = <b>63 L</b>. "
                   "9 L is the empty space at the top."))
    assert 60 * 30 * 35 == 63000 and 60 * 30 * 5 == 9000
    V = cv(3, 12)
    assert V == Dm("339.12") and cv(6, 12) == Dm("1356.48") and PI * 3 * 12 == Dm("113.04") and PI * 6 * 12 == Dm("226.08")
    its.append(mcq("A juice can is a cylinder with a radius of 3 cm and a height of 12 cm. "
                   "About how many millilitres of juice does it hold? (Use π ≈ 3.14.)", "about 339 mL",
                   ["about 1356 mL", "about 113 mL", "about 226 mL"],
                   "V = 3.14 × 3 × 3 × 12 = 28.26 × 12 = 339.12 cm³. 1 cm³ = 1 mL, so it holds <b>about 339 mL</b>. "
                   "1356 uses the diameter (6 cm) as r."))
    V = cv(1, 2)
    assert V == Dm("6.28") and cv(2, 2) == Dm("25.12")
    its.append(mcq("A water tank on a farm near Kamloops is a cylinder with a radius of 1 m and a height of 2 m. "
                   "How many litres does it hold? (Use π ≈ 3.14.)", "6280 L", ["628 L", "25" + NB + "120 L", "6.28 L"],
                   "V = 3.14 × 1 × 1 × 2 = 6.28 m³. 1 m³ = 1000 L, so 6.28 × 1000 = <b>6280 L</b>. "
                   "25" + NB + "120 L uses the diameter (2 m) as r."))
    V = cv(30, 90)
    assert V == Dm("254340") and cv(60, 90) == Dm("1017360")
    its.append(mcq("A rain barrel in Vancouver is a cylinder with a diameter of 60 cm and a height of 90 cm. "
                   "About how many litres of rain can it hold? (Use π ≈ 3.14.)", "about 254 L",
                   ["about 1017 L", "about 2543 L", "about 25 L"],
                   "r = 60 ÷ 2 = 30 cm. V = 3.14 × 30 × 30 × 90 = 2826 × 90 = 254" + NB + "340 cm³ = 254" + NB + "340 mL, "
                   "which is about <b>254 L</b>. 1017 L uses 60 cm as the radius."))
    its.append(mcq("A backyard pool in Kelowna is 8 m long and 4 m wide. The water is 1.5 m deep everywhere. "
                   "How many litres of water are in the pool?", "48" + NB + "000 L",
                   ["4800 L", "480" + NB + "000 L", "48 L"],
                   "V = 8 × 4 × 1.5 = 32 × 1.5 = 48 m³. 1 m³ = 1000 L, so 48 × 1000 = <b>48" + NB + "000 L</b>."))
    assert 120 * 40 * 30 == 144000
    its.append(mcq("Hana builds a cedar planter box that is 120 cm long, 40 cm wide and 30 cm deep inside. "
                   "Soil comes in 50 L bags. How many bags does she need to fill the box?", "3 bags",
                   ["2 bags", "29 bags", "144 bags"],
                   "V = 120 × 40 × 30 = 144" + NB + "000 cm³ = 144 L. 144 ÷ 50 = 2.88, so 2 bags are not enough. "
                   "She needs <b>3 bags</b>."))
    its.append(mcq("A juice box is 6 cm long, 4 cm wide and 10 cm high. How much juice can it hold?", "240 mL",
                   ["20 mL", "24 mL", "2.4 L"],
                   "V = 6 × 4 × 10 = 240 cm³. 1 cm³ = 1 mL, so it holds <b>240 mL</b>. (2.4 L would be 2400 mL.)"))
    assert cv(3, 10) == Dm("282.6") and 7 * 7 * 6 == 294 and Dm(294) - Dm("282.6") == Dm("11.4")
    its.append(mcq("Container A is a cylinder with a radius of 3 cm and a height of 10 cm. Container B is a box 7 cm × 7 cm × 6 cm. "
                   "Which holds more, and by how much? (Use π ≈ 3.14.)", "B, by 11.4 cm³",
                   ["A, by 11.4 cm³", "B, by 114 cm³", "They hold the same"],
                   "A: 3.14 × 3 × 3 × 10 = 282.6 cm³. B: 7 × 7 × 6 = 294 cm³. 294 − 282.6 = 11.4. "
                   "So <b>B holds more, by 11.4 cm³</b>."))
    V = cv(20, 50)
    assert V == Dm("62800") and cv(40, 50) == Dm("251200")
    its.append(mcq("A water cooler at the Terry Fox Run is a cylinder with a diameter of 40 cm and a height of 50 cm. "
                   "How many litres does it hold? (Use π ≈ 3.14.)", "62.8 L", ["251.2 L", "6.28 L", "628 L"],
                   "r = 40 ÷ 2 = 20 cm. V = 3.14 × 20 × 20 × 50 = 1256 × 50 = 62" + NB + "800 cm³. "
                   "Divide by 1000: <b>62.8 L</b>. 251.2 L uses the diameter as r."))
    V = cv(4, 10)
    assert V == Dm("502.4") and int(Dm(2000) / V) == 3 and int(Dm(2000) / (PI * 4 * 10)) == 15 and int(Dm(2000) / 160) == 12
    its.append(mcq("Sofia pours juice from a full 2 L jug into glasses. Each glass is a cylinder with a radius of 4 cm "
                   "and a height of 10 cm. How many glasses can she fill all the way? (Use π ≈ 3.14.)", "3 glasses",
                   ["4 glasses", "15 glasses", "12 glasses"],
                   "One glass: 3.14 × 4 × 4 × 10 = 502.4 cm³ = 502.4 mL. 2 L = 2000 mL. 2000 ÷ 502.4 ≈ 3.98, "
                   "so she can fill <b>3 glasses</b> all the way (the 4th is not full)."))
    its.append(mcq("An aquarium has a base 50 cm long and 25 cm wide. Ethan pours in 25 L of water. "
                   "How deep is the water?", "20 cm", ["2 cm", "200 cm", "500 cm"],
                   "25 L = 25" + NB + "000 cm³. Base area: 50 × 25 = 1250 cm². Depth = 25" + NB + "000 ÷ 1250 = <b>20 cm</b>. "
                   "500 divides by the length only."))
    assert Dm(25000) / 1250 == 20 and Dm(25000) / 50 == 500
    its.append(mcq("A rectangular water tank in an Okanagan orchard is 2 m long, 1.5 m wide and 1 m high. "
                   "How many litres does it hold?", "3000 L", ["300 L", "30" + NB + "000 L", "3 L"],
                   "V = 2 × 1.5 × 1 = 3 m³. 1 m³ = 1000 L, so 3 × 1000 = <b>3000 L</b>."))
    V = cv("3.5", 20)
    assert V == Dm("769.3") and cv(7, 20) == Dm("3077.2") and PI * 7 * 20 == Dm("439.6") and PI * Dm("3.5") * 20 == Dm("219.8")
    its.append(mcq("Owen takes a water bottle on a hike up the Grouse Grind. The bottle is a cylinder with a radius of 3.5 cm "
                   "and a height of 20 cm. How much water does it hold? (Use π ≈ 3.14.)", "769.3 mL",
                   ["439.6 mL", "3077.2 mL", "219.8 mL"],
                   "r² = 3.5 × 3.5 = 12.25. V = 3.14 × 12.25 × 20 = 38.465 × 20 = 769.3 cm³ = <b>769.3 mL</b>. "
                   "439.6 uses r × 2 instead of r × r."))
    its.append(mcq("A storage bin holds 60 L. Its inside base is 50 cm long and 40 cm wide. How high is the inside of the bin?",
                   "30 cm", ["3 cm", "300 cm", "1200 cm"],
                   "60 L = 60" + NB + "000 cm³. Base area: 50 × 40 = 2000 cm². Height = 60" + NB + "000 ÷ 2000 = <b>30 cm</b>. "
                   "1200 divides by the length only."))
    assert Dm(60000) / 2000 == 30 and Dm(60000) / 50 == 1200
    its.append(mcq("A hose fills Liam’s 72 L fish tank at 4 L per minute. How many minutes does it take to fill the tank?",
                   "18 minutes", ["288 minutes", "68 minutes", "1.8 minutes"],
                   "72 ÷ 4 = <b>18 minutes</b>. Check: 18 × 4 = 72 L. (288 multiplies, and 68 subtracts.)"))
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
    return (
        "<h2>What volume means</h2>"
        "<p><b>Volume</b> is the amount of space inside a solid. A cube with 1 cm edges has a volume of "
        "<b>1 cm³</b> (one cubic centimetre). To find a volume, count how many of these cubes fill the solid.</p>"
        "<figure class='sn-fig'>" + prism_cubes(4, 3, 3, "prism of centimetre cubes with its 3 layers pulled apart", gap=0.45) +
        "<figcaption>Each layer has 4 × 3 = 12 cubes. There are 3 layers: 12 × 3 = 36 cm³. "
        "The hidden cubes count, too.</figcaption></figure>"
        "<h2>Rectangular prisms</h2>"
        "<p><b>V = l × w × h</b>. The base l × w tells you how many cubes are in one layer, and h tells you how many layers.</p>"
        "<figure class='sn-fig'>" + prism_svg(6, 4, 5, "6 cm", "4 cm", "5 cm", "rectangular prism 6 by 4 by 5 cm") +
        "<figcaption>Base: 6 × 4 = 24 cm². V = 24 × 5 = 120 cm³.</figcaption></figure>"
        "<h2>Any prism: area of base × height</h2>"
        "<p>Every prism is a stack of layers shaped like its base, so <b>V = area of base × height</b>. "
        "Find the area of the base first, then multiply.</p>"
        "<figure class='sn-fig'>" + tri_svg(6, 4, 10, "cm", "triangular prism, triangle 6 cm by 4 cm, length 10 cm") +
        "<figcaption>Base: ½ × 6 × 4 = 12 cm². V = 12 × 10 = 120 cm³.</figcaption></figure>"
        "<h2>Cylinders</h2>"
        "<p>A cylinder is like a prism with a circle for a base. The area of the circle is π × r², so "
        "<b>V = π × r² × h</b>. Use π ≈ 3.14. The radius r goes from the centre to the edge; it is half the diameter.</p>"
        "<figure class='sn-fig'>" + cyl_svg(3, 10, "cm") +
        "<figcaption>r = 3 cm and h = 10 cm. Base: 3.14 × 3 × 3 = 28.26 cm². V = 28.26 × 10 = 282.6 cm³.</figcaption></figure>"
        + ex("Example 1", "A can has a diameter of 8 cm and a height of 10 cm. What is its volume?",
             "r = 8 ÷ 2 = 4 cm. V = 3.14 × 4 × 4 × 10 = 50.24 × 10.", "502.4 cm³")
        + "<h2>Volume and capacity</h2>"
        "<p><b>Capacity</b> is how much a container can hold. 1 cm³ holds exactly 1 mL.</p>"
        + table(["Volume", "Capacity"], [
            ["1 cm³", "1 mL"],
            ["1000 cm³ (a 10 cm cube)", "1 L"],
            ["1 m³", "1000 L"],
        ])
        + ex("Example 2", "A fish tank is 60 cm × 30 cm × 40 cm. How many litres does it hold?",
             "V = 60 × 30 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. Divide by 1000.", "72 L")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the edges: 6 + 4 + 5 = 15", "Multiply them: 6 × 4 × 5 = 120"],
            ["Stopping at the base: 6 × 4 = 24", "Multiply by the height too"],
            ["Using the diameter as r", "Halve the diameter first: d = 8, r = 4"],
            ["r² as r × 2", "r² = r × r: 4² = 16, not 8"],
            ["Forgetting ½ for a triangle base", "Triangle area = ½ × b × h"],
            ["Writing cm² for a volume", "Volume is in cubic units: cm³, m³"],
        ])
    )


FAQ = [
    {"q": "How do you find the volume of a cylinder in Grade 7?",
     "a": "Find the area of the circular base with π × r × r (π ≈ 3.14), then multiply by the height. For r = 3 cm and h = 10 cm: 3.14 × 9 × 10 = 282.6 cm³."},
    {"q": "What volume topics are in the BC Grade 7 math curriculum?",
     "a": "The BC Grade 7 curriculum includes the volume of rectangular prisms and cylinders. Students connect volume to area of base × height and work with cm³, m³, mL and L."},
    {"q": "What is the difference between volume and capacity?",
     "a": "Volume is the space a solid takes up, in cubic units like cm³. Capacity is how much a container holds, in mL or L, and 1 cm³ = 1 mL."},
    {"q": "Do these volume worksheets help with the Grade 7 FSA?",
     "a": "Yes. The Grade 7 FSA includes numeracy, where students use math to solve problems. Finding how much a tank, can or box holds is good practice for that kind of problem."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(37811)
    sets = [set_count(rnd), set_rect(rnd), set_base(), set_cyl(rnd), set_story()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "volume-of-prisms-and-cylinders", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Volume of Prisms and Cylinders",
        "seo_title": "Grade 7 Volume of Prisms and Cylinders Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Volume of prisms and cylinders",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 7: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Volume of rectangular prisms and cylinders",
        "meta_desc": "Free Grade 7 math worksheets on volume for the BC curriculum: counting cubes, V = l × w × h, area of base × height, cylinders with V = πr²h (π ≈ 3.14), and capacity in mL and L with fish tanks, juice cans and water tanks. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Volume = area of base × height. Rectangular prism: V = l × w × h. Cylinder: V = π × r² × h.",
        "key_sub": "Use the radius, not the diameter, and r² means r × r. Volume is in cubic units (cm³, m³), and 1 cm³ holds 1 mL.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(rectangular prism made of|rectangular prism of centimetre cubes)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
