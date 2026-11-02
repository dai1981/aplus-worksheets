# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Volume and capacity (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g6_volume.py
Drawing engine (unit cubes, labelled boxes) copied from gen_cabc_math_g7_volume.py; all wording rewritten for Grade 6.
Canadian English, metric units (cm³, m³, mL, L), SI number style (4 digits plain, 5+ digits with a no-break space).
Every answer is computed with decimal.Decimal and checked in code. HTML attributes use single quotes.

Pictures (checked in code):
  cube prisms   every unit cube is drawn (back to front); the number of cubes equals l × w × h
  boxes         oblique view, hidden edges dashed, edge labels outside the solid; labels never touch
  jugs          measuring jug, labels every 200 mL, small marks every 50 mL, water drawn to its level
Wrong answers come from real student mistakes: adding the edges, stopping at one layer (the base),
counting only the cubes you can see, writing cm² for a volume, ×100 instead of ×1000 for mL and L,
reading “2.5 L” as 2 L 5 mL, and reading each small jug mark as 10 mL.
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
WATER = "#b9dcf2"
WATER_EDGE = "#2e86c1"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
DZX, DZY = 0.55, 0.40          # one unit of depth goes this far right and up (oblique view)
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


def mL(x):
    return N(x) + " mL"


def L(x):
    return N(x) + " L"


UNIT = {"cm³": ("v", 1), "mL": ("v", 1), "L": ("v", 1000), "m³": ("v", 1000000),
        "cm²": ("a", 1), "m²": ("a", 10000), "cm": ("l", 1), "m": ("l", 100)}
NUM = re.compile("^(?:about )?([\\d" + NB + "]+(?:\\.\\d+)?) (\\S+)$")


def val(c):
    """(kind, value) of a choice like '72 000 cm³' or '2.5 L'; None if it is not one amount."""
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
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def proj(X, Y, Z, k):
    """x to the right, y up, z (depth) to the back."""
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


# ------------------------------------------------------------ unit-cube pictures
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
    cubes = [(x, y, z) for x in range(l) for y in range(h) for z in range(w)]
    assert len(cubes) == l * w * h
    return cube_svg(cubes, label or "rectangular prism made of %d centimetre cubes" % (l * w * h), gap=gap)


def visible_cubes(l, w, h):
    """Cubes that show at least one face: front, top or right side."""
    return l * w * h - (l - 1) * (w - 1) * (h - 1)


# ------------------------------------------------------------ boxes with labels
def disp_dims(*v):
    """Draw very different sizes a little closer together so the solid stays readable."""
    v = [float(x) for x in v]
    m = max(v)
    return tuple(max(x, m / 3.2) for x in v)


def prism_svg(Lx, Wx, Hx, lab_l, lab_w, lab_h, label):
    dL, dW, dH = disp_dims(Lx, Wx, Hx)
    k = min(165 / (dL + dW * DZX), 100 / (dH + dW * DZY))
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, dH, 0), p(0, dH, 0)], FILL, 2.4)
    cv.poly([p(0, dH, 0), p(dL, dH, 0), p(dL, dH, dW), p(0, dH, dW)], TOP, 2.4)
    cv.poly([p(dL, 0, 0), p(dL, 0, dW), p(dL, dH, dW), p(dL, dH, 0)], SIDE, 2.4)
    for a, b in [((0, 0, dW), (dL, 0, dW)), ((0, 0, dW), (0, dH, dW)), ((0, 0, dW), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True)
    x, y = p(dL / 2, 0, 0)
    cv.text(x, y + 17, lab_l, 16)
    x, y = p(0, dH / 2, 0)
    cv.text(x - 8, y, lab_h, 16, "end")
    x, y = p(dL, 0, dW / 2)
    cv.text(x + 7, y + 11, lab_w, 16, "start")
    return cv.svg(label)


def box(l, w, h, u="cm"):
    return prism_svg(float(l), float(w), float(h), "%s %s" % (N(l), u), "%s %s" % (N(w), u), "%s %s" % (N(h), u),
                     "rectangular prism %s %s long, %s %s wide and %s %s high" % (N(l), u, N(w), u, N(h), u))


# ------------------------------------------------------------ measuring jug
def jug_svg(level, top=1000):
    """Measuring jug, 0 to `top` mL. Labels every 200 mL, small marks every 50 mL. Water up to `level` mL."""
    assert level % 50 == 0 and 0 < level < top and level % 200 != 0
    S = 0.16                                    # px per mL
    Hh = top * S
    x0, x1 = 0, 92                              # inside walls of the jug
    yb = 0                                      # bottom of the scale
    ytop = -Hh - 18                             # rim
    cv = Canvas()
    yl = -level * S
    cv.poly([(x0, yl), (x1, yl), (x1, yb), (x0, yb)], WATER, 0.01, WATER)
    cv.line((x0, yl), (x1, yl), sw=2.0, col=WATER_EDGE)
    # outline: left wall, bottom, right wall, spout and handle
    cv.line((x0, ytop), (x0, yb))
    cv.line((x0, yb), (x1, yb))
    cv.line((x1, yb), (x1, ytop))
    cv.line((x0, ytop), (x0 - 12, ytop - 10))
    cv.line((x1, ytop + 14), (x1 + 22, ytop + 14))
    cv.line((x1 + 22, ytop + 14), (x1 + 22, -Hh * 0.45))
    cv.line((x1 + 22, -Hh * 0.45), (x1, -Hh * 0.45))
    for m in range(50, top + 1, 50):
        y = -m * S
        big = m % 200 == 0
        cv.line((x0, y), (x0 + (22 if big else 11), y), sw=1.8 if big else 1.4, col=INK)
        if big:
            cv.text(x0 - 8, y, "%d mL" % m, 14, "end")
    cv.text(-8 - tw("0 mL", 14) / 2, yb, "0 mL", 14)
    return cv.svg("measuring jug marked from 0 to %d mL with water in it" % top)


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
        e = ("The bottom layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = <b>%d cm³</b>. "
             "Count the hidden cubes too: only %d cubes show a face." % (w, l, l * w, h, l * w, h, V, vis))
        its.append(mcq(q, cm3(V), [cm3(vis), cm3(faces), cm3(l + w + h), "%d cm²" % V, cm3(l * h)], e))
    used = set()
    for i in range(4):
        while True:
            l, w, h = pick_dims(rnd, seen, (3, 5), (2, 4), (2, 4))
            if l != w and (l, w) not in used and h != w:
                break
        used.add((l, w))
        q = fig(prism_cubes(l, w, h)) + "How many centimetre cubes are in the <b>bottom layer</b> of this prism?"
        e = ("The bottom layer is %d cubes long and %d cubes deep: %d × %d = <b>%d</b> cubes. "
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
                   "Bottom layer: 10 × 6 = 60 cubes. The box is 4 cm high, so it holds 4 layers: 60 × 4 = <b>240</b> cubes. "
                   "(20 adds the edges, 60 is only one layer, and 64 adds the height to one layer.)"))
    its.append(mcq("A box holds 60 centimetre cubes in each layer. It holds 420 cubes in all. How many layers are there?",
                   "7", ["360", "480", "6"],
                   "Cubes in one layer × number of layers = total, so 60 × ? = 420. 420 ÷ 60 = <b>7</b> layers. "
                   "(360 subtracts and 480 adds.)"))
    assert 60 * 7 == 420
    assert len(its) == 20, len(its)
    return {"title": "Volume by counting cubes", "items": its}


# ============================================================ set 2: V = l × w × h
def set_rect(rnd):
    its, seen = [], set()
    for i in range(8):
        while True:
            Lx, W, H = rnd.randint(5, 15), rnd.randint(2, 9), rnd.randint(2, 12)
            if Lx > W and (Lx, W) not in {k[:2] for k in seen} and Lx * W + H != Lx + W + H:
                break
        u = "m" if i in (3, 6) else "cm"
        if u == "m":
            Lx, W, H = Lx % 6 + 3, W % 3 + 2, H % 4 + 2
            if Lx <= W:
                Lx = W + 2
        seen.add((Lx, W, H))
        V = Lx * W * H
        q = fig(box(Lx, W, H, u)) + "What is the volume of this rectangular prism?"
        pool = ["%s %s³" % (N(Lx * W), u), "%d %s³" % (Lx + W + H, u), "%s %s²" % (N(V), u), "%s %s³" % (N(Lx * W + H), u)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("V = l × w × h = %d × %d × %d = %d × %d = <b>%s %s³</b>. Multiply all three edges (do not add them), "
             "and write cubic units." % (Lx, W, H, Lx * W, H, N(V), u))
        its.append(mcq(q, "%s %s³" % (N(V), u), pool, e))
    for s in [5, 8, 10]:
        V = s ** 3
        q = "A cube has edges that are %d cm long. What is its volume?" % s
        e = ("All the edges of a cube are equal, so V = %d × %d × %d = %d × %d = <b>%s cm³</b>. "
             "%d × 3 = %d is not the volume." % (s, s, s, s * s, s, N(V), s, 3 * s))
        its.append(mcq(q, cm3(V), [cm3(3 * s), cm3(s * s), N(V) + " cm²"], e))
    its.append(mcq("A box is 6 cm long, 4 cm wide and 3 cm high. Which expression gives its volume?", "6 × 4 × 3",
                   ["6 + 4 + 3", "6 × 4", "6 × 4 + 3"],
                   "Volume = length × width × height = <b>6 × 4 × 3</b> = 72 cm³. 6 × 4 is only the area of the base."))
    its.append(mcq("A recycling bin is 50 cm long, 30 cm wide and 20 cm high. Which expression gives its volume?",
                   "50 × 30 × 20", ["50 + 30 + 20", "50 × 30 + 20", "(50 + 30) × 20"],
                   "Length × width × height = <b>50 × 30 × 20</b> = 1500 × 20 = 30" + NB + "000 cm³. "
                   "(50 + 30) × 20 adds two edges first."))
    assert 50 * 30 * 20 == 30000
    for l, w, h, u, wrong in [("2.5", "4", "6", "cm", ["12.5 cm³", "600 cm³", "60 cm²"]),
                              ("1.5", "2", "3", "m", ["6.5 m³", "90 m³", "9 m²"])]:
        V = Dm(l) * Dm(w) * Dm(h)
        assert val(wrong[0])[1] == val("%s %s³" % (N(Dm(l) + Dm(w) + Dm(h)), u))[1]
        q = fig(box(Dm(l), Dm(w), Dm(h), u)) + "What is the volume of this rectangular prism?"
        e = ("V = %s × %s × %s = %s × %s = <b>%s %s³</b>. Multiply decimals the same way, then check the decimal point: "
             "%s × %s = %s." % (l, w, h, N(Dm(l) * Dm(w)), h, N(V), u, l, w, N(Dm(l) * Dm(w))))
        its.append(mcq(q, "%s %s³" % (N(V), u), wrong, e))
    for V, a, b, an, bn, miss, ans, wrong in [
            (240, 10, 4, "long", "wide", "high", 6, [24, 60, 226]),
            (360, 9, 8, "long", "high", "wide", 5, [40, 45, 343]),
            (500, 10, 10, "long", "wide", "high", 5, [50, 25, 480])]:
        assert V == a * b * ans and V // a == wrong[0] and V // b == wrong[1] or (a, b) == (10, 10)
        q = "A rectangular prism has a volume of %d cm³. It is %d cm %s and %d cm %s. How %s is it?" % (V, a, an, b, bn, miss)
        e = ("%d × %d × ? = %d, so %d × ? = %d. %d ÷ %d = <b>%d cm</b>. Check: %d × %d × %d = %d."
             % (a, b, V, a * b, V, V, a * b, ans, a, b, ans, V))
        its.append(mcq(q, "%d cm" % ans, ["%d cm" % x for x in wrong], e))
    assert 500 // 20 == 25 and 500 - 20 == 480 and 360 - 17 == 343 and 240 - 14 == 226
    its.append(mcq("Which box has a volume of 24 cm³?", "4 cm × 3 cm × 2 cm",
                   ["10 cm × 8 cm × 6 cm", "8 cm × 3 cm × 3 cm", "6 cm × 4 cm × 4 cm"],
                   "4 × 3 × 2 = <b>24 cm³</b>. 10 + 8 + 6 is 24, but its volume is 10 × 8 × 6 = 480 cm³. "
                   "8 × 3 = 24 forgets the third edge: 8 × 3 × 3 = 72 cm³."))
    its.append(mcq("A box is 5 cm long, 4 cm wide and 3 cm high. Its length doubles to 10 cm and the other edges stay the same. "
                   "What is the new volume?", "120 cm³", ["65 cm³", "240 cm³", "480 cm³"],
                   "Old volume: 5 × 4 × 3 = 60 cm³. New volume: 10 × 4 × 3 = <b>120 cm³</b>. "
                   "Doubling one edge doubles the volume. 480 cm³ would need all three edges doubled."))
    assert 10 * 8 * 6 == 480 and 8 * 3 * 3 == 72 and 10 * 4 * 3 == 120 and 10 * 8 * 6 == 480
    assert len(its) == 20, len(its)
    return {"title": "Rectangular prisms: V = l × w × h", "items": its}


# ============================================================ set 3: capacity in mL and L
def set_capacity():
    its = []
    for l, wrong, extra in [("3", ["300 mL", "30" + NB + "000 mL", "30 mL"], ""),
                            ("2.5", ["2005 mL", "250 mL", "25" + NB + "000 mL"], " 2.5 L is not 2 L 5 mL."),
                            ("1.2", ["1002 mL", "120 mL", "12" + NB + "000 mL"], " 1.2 L is not 1 L 2 mL."),
                            ("0.75", ["75 mL", "7500 mL", "705 mL"], "")]:
        m = Dm(l) * 1000
        q = "How many millilitres are in %s L?" % l
        e = "1 L = 1000 mL, so multiply by 1000: %s × 1000 = <b>%s mL</b>.%s" % (l, N(m), extra)
        its.append(mcq(q, mL(m), wrong, e))
    for m, wrong in [(4000, ["40 L", "400 L", "0.4 L"]), (1500, ["15 L", "150 L", "0.15 L"]),
                     (2300, ["23 L", "0.23 L", "230 L"]), (250, ["2.5 L", "25 L", "0.025 L"])]:
        l = Dm(m) / 1000
        q = "How many litres are in %s mL?" % N(m)
        e = "1000 mL = 1 L, so divide by 1000: %s ÷ 1000 = <b>%s L</b>. (Dividing by 100 gives %s, which is 10 times too big.)" % (
            N(m), N(l), N(Dm(m) / 100))
        its.append(mcq(q, L(l), wrong, e))
    for lev in [650, 300, 900]:
        major = lev // 200 * 200
        ticks = (lev - major) // 50
        q = fig(jug_svg(lev)) + "How much water is in the measuring jug?"
        wrong = [mL(major + 10 * ticks), mL(major + 200), L(Dm(lev) / 100)]
        e = ("The labels go up by 200 mL, and there are 4 spaces between labels, so each small mark is 200 ÷ 4 = 50 mL. "
             "The water is %d mark%s above %d mL: %d + %d = <b>%d mL</b>."
             % (ticks, "" if ticks == 1 else "s", major, major, 50 * ticks, lev))
        its.append(mcq(q, mL(lev), wrong, e))
    its.append(mcq("Which amount is the <b>most</b>?", "1.5 L", ["1200 mL", "980 mL", "0.95 L"],
                   "Change all of them to millilitres: 1.5 L = 1500 mL and 0.95 L = 950 mL. "
                   "1500 &gt; 1200 &gt; 980 &gt; 950, so <b>1.5 L</b> is the most. A big number in mL can still be less."))
    its.append(mcq("Which amount is the <b>least</b>?", "350 mL", ["0.4 L", "0.5 L", "1.1 L"],
                   "0.4 L = 400 mL, 0.5 L = 500 mL and 1.1 L = 1100 mL. So <b>350 mL</b> is the least, even though 0.4 looks small."))
    its.append(mcq("Which amount is equal to 2.05 L?", "2050 mL", ["2005 mL", "2500 mL", "205 mL"],
                   "2.05 × 1000 = <b>2050 mL</b>. The 0 in the tenths place holds the place: 2.05 L is 2 L and 50 mL."))
    its.append(mcq("About how much does a teaspoon hold?", "5 mL", ["5 L", "50 mL", "500 mL"],
                   "A teaspoon holds a tiny amount: about <b>5 mL</b>. 500 mL is a big water bottle, and 5 L is a big jug."))
    its.append(mcq("About how much water does a full bathtub hold?", "150 L", ["150 mL", "15 L", "1500 L"],
                   "A bathtub holds a lot: about <b>150 L</b>. 15 L would fill only about one bucket and a half."))
    its.append(mcq("About how much does a juice box hold?", "200 mL", ["2 L", "20 mL", "20 L"],
                   "A juice box is small enough for a lunch bag: about <b>200 mL</b>. 2 L is a big bottle of juice."))
    its.append(mcq("Ava drinks 750 mL of water in the morning and 1.5 L in the afternoon. How much does she drink in all?",
                   "2250 mL", ["751.5 mL", "765 mL", "225 mL"],
                   "Use the same unit first: 1.5 L = 1500 mL. 750 + 1500 = <b>2250 mL</b> (2.25 L). "
                   "751.5 adds 750 and 1.5 without changing the units."))
    its.append(mcq("How many 250 mL glasses can you fill from a full 2 L jug?", "8", ["80", "4", "125"],
                   "2 L = 2000 mL. 2000 ÷ 250 = <b>8</b> glasses. (4 glasses is only 1 L, and 80 uses 2 L = 20" + NB + "000 mL.)"))
    its.append(mcq("A 2 L bottle of water is full. Mateo pours out 650 mL. How much is left?", "1350 mL",
                   ["1450 mL", "648 mL", "2650 mL"],
                   "2 L = 2000 mL. 2000 − 650 = <b>1350 mL</b>. 648 takes 2 away from 650 without changing the units, "
                   "and 2650 adds instead of subtracting."))
    assert 750 + 1500 == 2250 and 2000 // 250 == 8 and 2000 - 650 == 1350
    assert len(its) == 20, len(its)
    return {"title": "Capacity in mL and L", "items": its}


# ============================================================ set 4: 1 cm³ = 1 mL
def set_link():
    its = []
    its.append(mcq("A container has a volume of 1 cm³. How much water can it hold?", "1 mL", ["1 L", "10 mL", "100 mL"],
                   "1 cm³ holds exactly <b>1 mL</b>. That is the key link between volume and capacity."))
    its.append(mcq("A cube-shaped container is 10 cm long, 10 cm wide and 10 cm high inside. How much water does it hold?",
                   "1 L", ["100 mL", "10 L", "30 mL"],
                   "V = 10 × 10 × 10 = 1000 cm³ = 1000 mL = <b>1 L</b>. (100 is only the base, and 30 adds the edges.)"))
    for l, w, h in [(5, 4, 10), (8, 5, 6), (12, 5, 5), (10, 10, 4), (9, 6, 5)]:
        V = l * w * h
        q = "A small box is %d cm long, %d cm wide and %d cm high inside. How many millilitres of water can it hold?" % (l, w, h)
        e = "V = %d × %d × %d = <b>%d cm³</b>, and 1 cm³ holds 1 mL, so it holds <b>%d mL</b>." % (l, w, h, V, V)
        its.append(mcq(q, mL(V), [mL(l + w + h), mL(l * w), L(V)], e))
    for l, w, h in [(20, 10, 10), (25, 20, 10), (30, 20, 15)]:
        V = l * w * h
        q = fig(box(l, w, h)) + "This container is full of water. How many litres does it hold?"
        e = ("V = %d × %d × %d = %s cm³ = %s mL. 1000 mL = 1 L, so %s ÷ 1000 = <b>%s L</b>."
             % (l, w, h, N(V), N(V), N(V), N(Dm(V) / 1000)))
        its.append(mcq(q, L(Dm(V) / 1000), [L(Dm(V) / 100), L(Dm(V) / 10000), L(l + w + h)], e))
    for c, wrong in [(3000, ["30 L", "0.3 L", "300 L"]), (1500, ["15 L", "150 L", "0.15 L"]),
                     (750, ["7.5 L", "75 L", "0.075 L"])]:
        q = "A container has a volume of %s cm³. How many litres can it hold?" % N(c)
        e = "%s cm³ = %s mL. Divide by 1000 to get litres: <b>%s L</b>." % (N(c), N(c), N(Dm(c) / 1000))
        its.append(mcq(q, L(Dm(c) / 1000), wrong, e))
    for name, start, end, extra in [("Kai", "300 mL", "340 mL", ""), ("Zara", "500 mL", "575 mL", ""),
                                    ("Lucas", "1.2 L", "1.45 L", " First change litres to millilitres: 1.2 L = 1200 mL and 1.45 L = 1450 mL.")]:
        s, t = val(start)[1], val(end)[1]
        d = t - s
        q = ("A measuring jug has %s of water. %s drops %s rock into it, and the water rises to %s. "
             "What is the volume of the rock?" % (start, name, "a" if name != "Lucas" else "a small", end))
        e = ("The rock pushes the water up by the space it takes. %s%s − %s = %s mL, and 1 mL = 1 cm³, "
             "so the rock is <b>%s cm³</b>." % (extra.strip() + " " if extra else "", N(t), N(s), N(d), N(d)))
        if name == "Lucas":
            wrong = ["0.25 cm³", "25 cm³", "2650 cm³"]
        else:
            wrong = [cm3(t), cm3(s + t), N(d) + " cm²"]
        its.append(mcq(q, cm3(d), wrong, e))
    its.append(mcq("A cube-shaped tank is 1 m long, 1 m wide and 1 m high inside. How many litres does it hold?", "1000 L",
                   ["100 L", "1 L", "3 L"],
                   "1 m = 100 cm, so V = 100 × 100 × 100 = 1" + NB + "000" + NB + "000 cm³ = 1" + NB + "000" + NB + "000 mL. "
                   "Divide by 1000: <b>1000 L</b>. So 1 m³ holds 1000 L."))
    assert 100 ** 3 == 1000000
    its.append(mcq("Which box holds exactly 1 L?", "20 cm × 5 cm × 10 cm",
                   ["10 cm × 10 cm × 5 cm", "10 cm × 10 cm × 1 cm", "100 cm × 10 cm × 10 cm"],
                   "1 L = 1000 mL = 1000 cm³. 20 × 5 × 10 = <b>1000 cm³</b>. The others hold 500 mL, 100 mL and 10 L. "
                   "A box does not need to be a 10 cm cube to hold 1 L."))
    assert 20 * 5 * 10 == 1000 and 10 * 10 * 5 == 500 and 100 * 10 * 10 == 10000
    its.append(mcq("A box has a base 10 cm long and 10 cm wide. It holds 500 mL when full. How high is it?", "5 cm",
                   ["50 cm", "0.5 cm", "480 cm"],
                   "500 mL = 500 cm³. Base: 10 × 10 = 100 cm². Height = 500 ÷ 100 = <b>5 cm</b>. "
                   "50 cm divides by only one edge."))
    its.append(mcq("A milk carton holds 1 L. Its base is 10 cm long and 5 cm wide. How high is the milk when the carton is full?",
                   "20 cm", ["100 cm", "200 cm", "2 cm"],
                   "1 L = 1000 cm³. Base: 10 × 5 = 50 cm². Height = 1000 ÷ 50 = <b>20 cm</b>. "
                   "100 and 200 divide by only one edge."))
    assert len(its) == 20, len(its)
    return {"title": "Volume and capacity: 1 cm³ = 1 mL", "items": its}


# ============================================================ set 5: word problems
def set_story():
    its = []
    its.append(mcq("A juice box is 6 cm long, 4 cm wide and 10 cm high. How much juice can it hold?", "240 mL",
                   ["20 mL", "24 mL", "2.4 L"],
                   "V = 6 × 4 × 10 = 240 cm³. 1 cm³ = 1 mL, so it holds <b>240 mL</b>. (2.4 L would be 2400 mL.)"))
    its.append(mcq("A shoebox is 30 cm long, 20 cm wide and 12 cm high. What is its volume?", "7200 cm³",
                   ["62 cm³", "600 cm³", "7200 cm²"],
                   "V = 30 × 20 × 12 = 600 × 12 = <b>7200 cm³</b>. 600 is only the base, and volume is in cm³, not cm²."))
    its.append(mcq("Liam’s fish tank is 60 cm long, 30 cm wide and 40 cm high. How many litres does it hold when full?",
                   "72 L", ["7.2 L", "720 L", "7200 L"],
                   "V = 60 × 30 × 40 = 1800 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. Divide by 1000: <b>72 L</b>."))
    its.append(mcq("Liam fills the same fish tank (60 cm long, 30 cm wide, 40 cm high) only up to 35 cm. How much water is in it?",
                   "63 L", ["72 L", "9 L", "630 L"],
                   "Use the height of the water, not the tank: 60 × 30 × 35 = 1800 × 35 = 63" + NB + "000 cm³ = <b>63 L</b>. "
                   "9 L is the empty space at the top."))
    assert 60 * 30 * 40 == 72000 and 60 * 30 * 35 == 63000 and 60 * 30 * 5 == 9000
    its.append(mcq("Ji-woo’s fish tank is 50 cm long, 25 cm wide and 30 cm high. How many litres does it hold when full?",
                   "37.5 L", ["375 L", "3.75 L", "105 L"],
                   "V = 50 × 25 × 30 = 1250 × 30 = 37" + NB + "500 cm³ = 37" + NB + "500 mL. "
                   "Divide by 1000: <b>37.5 L</b>. (105 adds the edges.)"))
    assert 50 * 25 * 30 == 37500
    its.append(mcq("A cooler for a class field trip is 40 cm long, 30 cm wide and 25 cm deep inside. How many litres does it hold?",
                   "30 L", ["3 L", "300 L", "95 L"],
                   "V = 40 × 30 × 25 = 1200 × 25 = 30" + NB + "000 cm³. Divide by 1000: <b>30 L</b>."))
    assert 40 * 30 * 25 == 30000
    its.append(mcq("Arjun’s lunch container is 15 cm long, 10 cm wide and 6 cm high. Will 1 L of soup fit in it?",
                   "No, it holds 900 mL", ["Yes, it holds 1 L", "Yes, it holds 9 L", "No, it holds 31 mL"],
                   "V = 15 × 10 × 6 = 900 cm³ = 900 mL. 1 L = 1000 mL, so <b>no</b>: 100 mL of soup would not fit."))
    assert 15 * 10 * 6 == 900
    its.append(mcq("Box A is 8 cm × 5 cm × 4 cm. Box B is 6 cm × 6 cm × 5 cm. Which box has the greater volume, and by how much?",
                   "B, by 20 cm³", ["A, by 20 cm³", "They are the same", "B, by 200 cm³"],
                   "A: 8 × 5 × 4 = 160 cm³. B: 6 × 6 × 5 = 180 cm³. 180 − 160 = 20, so <b>B is greater by 20 cm³</b>. "
                   "Adding the edges gives 17 for both boxes, which is why “the same” is a trap."))
    assert 8 * 5 * 4 == 160 and 6 * 6 * 5 == 180 and 8 + 5 + 4 == 6 + 6 + 5
    its.append(mcq("A tissue box is a cube with edges 12 cm long. What is its volume?", "1728 cm³",
                   ["36 cm³", "144 cm³", "1728 cm²"],
                   "V = 12 × 12 × 12 = 144 × 12 = <b>1728 cm³</b>. 144 is only one face, and 36 adds the edges."))
    assert 12 ** 3 == 1728
    its.append(mcq("Olivia’s water bottle holds 750 mL. On a hike up Grouse Mountain, she drinks 3 full bottles. "
                   "How many litres does she drink?", "2.25 L", ["22.5 L", "0.225 L", "2250 L"],
                   "3 × 750 = 2250 mL. Divide by 1000: <b>2.25 L</b>. (2250 L forgets to change mL to L.)"))
    its.append(mcq("A school in Surrey builds a sandbox 3 m long and 2 m wide. The sand is 0.5 m deep. How much sand is that?",
                   "3 m³", ["5.5 m³", "30 m³", "6 m²"],
                   "V = 3 × 2 × 0.5 = 6 × 0.5 = <b>3 m³</b>. (6 is only the area of the base, and 5.5 adds the edges.)"))
    its.append(mcq("A rectangular rain barrel in Vancouver is 50 cm long, 40 cm wide and 80 cm high. How many litres of rain can it hold?",
                   "160 L", ["16 L", "1600 L", "170 L"],
                   "V = 50 × 40 × 80 = 2000 × 80 = 160" + NB + "000 cm³ = 160" + NB + "000 mL. Divide by 1000: <b>160 L</b>."))
    assert 50 * 40 * 80 == 160000
    its.append(mcq("How many 2 cm cubes fit in a box that is 10 cm long, 6 cm wide and 4 cm high?", "30",
                   ["240", "120", "60"],
                   "Along the length: 10 ÷ 2 = 5 cubes. Across: 6 ÷ 2 = 3. Up: 4 ÷ 2 = 2. 5 × 3 × 2 = <b>30</b> cubes. "
                   "240 counts 1 cm cubes, and 120 divides by 2 only once."))
    assert (10 // 2) * (6 // 2) * (4 // 2) == 30
    its.append(mcq("A rectangular tank at a salmon hatchery on Vancouver Island is 4 m long and 2 m wide. The water is 1 m deep. "
                   "How many litres of water are in the tank?", "8000 L", ["800 L", "80" + NB + "000 L", "7 L"],
                   "V = 4 × 2 × 1 = 8 m³. 1 m³ = 1000 L, so 8 × 1000 = <b>8000 L</b>."))
    its.append(mcq("A water tank in an Okanagan orchard is 2 m long, 1.5 m wide and 1 m high. How many litres does it hold?",
                   "3000 L", ["300 L", "30" + NB + "000 L", "4.5 L"],
                   "V = 2 × 1.5 × 1 = 3 m³. 1 m³ = 1000 L, so 3 × 1000 = <b>3000 L</b>. (4.5 adds the edges.)"))
    assert 120 * 40 * 30 == 144000
    its.append(mcq("Hana builds a cedar planter box that is 120 cm long, 40 cm wide and 30 cm deep inside. "
                   "Soil comes in 50 L bags. How many bags does she need to fill the box?", "3 bags",
                   ["2 bags", "29 bags", "144 bags"],
                   "V = 120 × 40 × 30 = 144" + NB + "000 cm³ = 144 L. 144 ÷ 50 = 2.88, so 2 bags are not enough. "
                   "She needs <b>3 bags</b>."))
    its.append(mcq("A hose fills Liam’s 72 L fish tank at 4 L per minute. How many minutes does it take to fill the tank?",
                   "18 minutes", ["288 minutes", "68 minutes", "1.8 minutes"],
                   "72 ÷ 4 = <b>18 minutes</b>. Check: 18 × 4 = 72 L. (288 multiplies, and 68 subtracts.)"))
    its.append(mcq("An aquarium has a base 50 cm long and 25 cm wide. Ethan pours in 25 L of water. How deep is the water?",
                   "20 cm", ["2 cm", "200 cm", "500 cm"],
                   "25 L = 25" + NB + "000 cm³. Base: 50 × 25 = 1250 cm². Depth = 25" + NB + "000 ÷ 1250 = <b>20 cm</b>. "
                   "500 divides by the length only."))
    assert Dm(25000) / 1250 == 20 and Dm(25000) / 50 == 500
    its.append(mcq("A storage bin holds 60 L. Its inside base is 50 cm long and 40 cm wide. How high is the inside of the bin?",
                   "30 cm", ["3 cm", "300 cm", "1200 cm"],
                   "60 L = 60" + NB + "000 cm³. Base: 50 × 40 = 2000 cm². Height = 60" + NB + "000 ÷ 2000 = <b>30 cm</b>. "
                   "1200 divides by the length only."))
    assert Dm(60000) / 2000 == 30 and Dm(60000) / 50 == 1200
    its.append(mcq("Emma has an empty cube-shaped container with 20 cm edges. She pours in 4 L of water. How deep is the water?",
                   "10 cm", ["200 cm", "20 cm", "1 cm"],
                   "4 L = 4000 cm³. Base: 20 × 20 = 400 cm². Depth = 4000 ÷ 400 = <b>10 cm</b>, so the container is half full. "
                   "200 cm divides by one edge only."))
    assert 4000 // 400 == 10 and 4000 // 20 == 200
    assert len(its) == 20, len(its)
    return {"title": "Word problems: fish tanks and boxes", "items": its}


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
        "<p><b>Volume</b> is the amount of space a solid takes up. A cube with 1 cm edges has a volume of "
        "<b>1 cm³</b> (one cubic centimetre). To find a volume, count how many of these cubes fill the solid.</p>"
        "<figure class='sn-fig'>" + prism_cubes(4, 3, 3, "prism of centimetre cubes with its 3 layers pulled apart", gap=0.45) +
        "<figcaption>Each layer has 4 × 3 = 12 cubes. There are 3 layers: 12 × 3 = 36 cm³. "
        "The hidden cubes count too.</figcaption></figure>"
        "<h2>The formula: V = l × w × h</h2>"
        "<p>Length × width tells you how many cubes are in one layer. The height tells you how many layers there are. "
        "So <b>V = l × w × h</b>, and the answer is in cubic units (cm³, m³).</p>"
        "<figure class='sn-fig'>" + box(6, 4, 5) +
        "<figcaption>One layer: 6 × 4 = 24 cubes. V = 24 × 5 = 120 cm³.</figcaption></figure>"
        + ex("Example 1", "A box is 8 cm long, 5 cm wide and 3 cm high. What is its volume?",
             "V = 8 × 5 × 3 = 40 × 3.", "120 cm³")
        + "<h2>Capacity: millilitres and litres</h2>"
        "<p><b>Capacity</b> is how much a container can hold. We measure it in millilitres (mL) and litres (L). "
        "<b>1 L = 1000 mL</b>, so multiply by 1000 to change litres to millilitres, and divide by 1000 to go back.</p>"
        "<figure class='sn-fig'>" + jug_svg(650) +
        "<figcaption>The labels go up by 200 mL, so each small mark is 50 mL. The water is at 650 mL (0.65 L).</figcaption></figure>"
        "<h2>Volume and capacity together</h2>"
        "<p>A 1 cm³ container holds exactly <b>1 mL</b>. A cube with 10 cm edges has a volume of 1000 cm³, "
        "so it holds 1000 mL, which is 1 L.</p>"
        + table(["Volume", "Capacity"], [
            ["1 cm³", "1 mL"],
            ["1000 cm³ (a 10 cm cube)", "1 L"],
            ["1 m³", "1000 L"],
        ])
        + ex("Example 2", "A fish tank is 60 cm long, 30 cm wide and 40 cm high. How many litres does it hold?",
             "V = 60 × 30 × 40 = 72" + NB + "000 cm³ = 72" + NB + "000 mL. Divide by 1000.", "72 L")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding the edges: 6 + 4 + 5 = 15", "Multiply them: 6 × 4 × 5 = 120"],
            ["Stopping at one layer: 6 × 4 = 24", "Multiply by the height too"],
            ["Counting only the cubes you can see", "Count every layer, hidden cubes too"],
            ["Writing cm² for a volume", "Volume is in cubic units: cm³, m³"],
            ["2.5 L = 2005 mL", "2.5 × 1000 = 2500 mL"],
            ["Multiplying by 100 for mL", "1 L = 1000 mL, so use 1000"],
        ])
    )


FAQ = [
    {"q": "How do you find the volume of a rectangular prism in Grade 6?",
     "a": "Multiply length × width × height. A box 6 cm long, 4 cm wide and 5 cm high has a volume of 6 × 4 × 5 = 120 cm³."},
    {"q": "What is the difference between volume and capacity?",
     "a": "Volume is the space a solid takes up, in cubic units like cm³. Capacity is how much a container holds, in mL or L."},
    {"q": "How many millilitres are in 1 cubic centimetre?",
     "a": "Exactly 1 mL. So 1000 cm³ = 1000 mL = 1 L, and a box with a volume of 72" + NB + "000 cm³ holds 72 L."},
    {"q": "Is volume part of the BC Grade 6 math curriculum?",
     "a": "Yes. The BC Grade 6 Geometry and measurement standards include volume and capacity: finding the volume of rectangular prisms and connecting cm³ to mL and L."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(56813)
    sets = [set_count(rnd), set_rect(rnd), set_capacity(), set_link(), set_story()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "volume-and-capacity", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Volume and Capacity",
        "seo_title": "Grade 6 Volume and Capacity Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Volume and capacity",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 6: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Volume and capacity",
        "meta_desc": "Free Grade 6 math worksheets on volume and capacity for the BC curriculum: counting cubes, V = l × w × h, millilitres and litres, 1 cm³ = 1 mL, and word problems about fish tanks, boxes and water tanks. 100 questions with an answer key.",
        "key_big": "Volume of a box = length × width × height. 1 cm³ holds 1 mL, and 1000 mL = 1 L.",
        "key_sub": "Multiply the three edges (do not add them) and write cubic units: cm³, m³. To change cm³ to litres, divide by 1000.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(rectangular prism made of|rectangular prism of centimetre cubes|measuring jug)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
