# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Volume of Cubes and Cuboids (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: Area and Volume)
  python3 tools/gen_sg_maths_p6_volume.py
Volume = length × breadth × height, finding a missing dimension, the edge of a cube from its volume (∛) and the side
of a square from its area (√), height from volume and base area, water in tanks (1 ℓ = 1000 cm³) and PSLE-style
multi-step word problems with bar models (units and parts, before and after).
Every figure is drawn from its numbers. HTML attributes use single quotes (no backslashes in the JSON).
Numbers follow the MOE style: 4 digits with no separator, 5 or more digits grouped with a no-break space.
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
NB = " "
GREEN = "#006633"
FILL = "#cfe6d6"
TOP, SIDE = "#e6f2e9", "#a9d3b6"
W_FRONT, W_TOP, W_SIDE, W_LINE = "#9fd0ee", "#cde8f7", "#7fbde3", "#2f7fb5"
UNIT_FILL, UNIT_FILL2, WHITE = "#cfe6d6", "#f6dcb4", "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
DZX, DZY = 0.55, 0.40
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Arjun", "Ethan", "Ryan"]


def frac(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


# ------------------------------------------------------------ numbers
def num(x):
    """Exact number in MOE style: 4536, 10 000 (no-break space), 2.5. Only terminating decimals."""
    x = Fr(x)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    assert d == 1, x
    neg = x < 0
    x = abs(x)
    s = format(Decimal(x.numerator) / Decimal(x.denominator), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, fp = s.partition(".")
    if len(i) >= 5:
        g = []
        while i:
            g.insert(0, i[-3:])
            i = i[:-3]
        i = NB.join(g)
    return ("−" if neg else "") + i + ("." + fp if fp else "")


def terminates(x):
    d = Fr(x).denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def q_(x, u):
    return "%s %s" % (num(x), u)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + the first 3 usable distractors (positive, unique, not equal in value)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def opt(x, u):
    """A distractor only if it is a positive terminating number."""
    x = Fr(x)
    if x <= 0 or not terminates(x):
        return None
    return q_(x, u)


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
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - (t.count(" ") + t.count(NB)) * 0.3) * fs * 0.6


# ------------------------------------------------------------ drawing canvas (screen coordinates, y down)
class Canvas:
    def __init__(self):
        self.el, self.boxes, self.segs = [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN, seg=True):
        self.el.append(("p", pts, fill, sw, col))
        if seg:
            self.segs += [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def rect(self, x, y, w, h, fill, sw=1.6, col=GREEN):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, sw, col)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.segs.append((a, b))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK, free=False):
        """(x, y) is the middle of the text. Labels never touch each other; unless free, no line runs through them."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        if not free:
            self.free_ok = getattr(self, "free_ok", [])
            self.free_ok.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def check(self):
        for (x0, y0, x1, y1) in getattr(self, "free_ok", []):
            for a, b in self.segs:
                for i in range(61):
                    x, y = a[0] + (b[0] - a[0]) * i / 60, a[1] + (b[1] - a[1]) * i / 60
                    assert not (x0 - 1 < x < x1 + 1 and y0 - 1 < y < y1 + 1), ("line through a label", (x0, y0, x1, y1))

    def svg(self, label, pad=5):
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
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, 1.6 if dashed else sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def proj(X, Y, Z, k):
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def disp_dims(*v):
    v = [float(x) for x in v]
    m = max(v)
    return tuple(max(x, m / 3.2) for x in v)


def colr(t):
    return RED if "?" in t else INK


def cuboid_svg(L, B, H, lab_l, lab_b, lab_h, label="cuboid with its length, breadth and height"):
    dL, dB, dH = disp_dims(L, B, H)
    k = min(165 / (dL + dB * DZX), 100 / (dH + dB * DZY), 26)
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, dH, 0), p(0, dH, 0)], FILL, 2.4)
    cv.poly([p(0, dH, 0), p(dL, dH, 0), p(dL, dH, dB), p(0, dH, dB)], TOP, 2.4)
    cv.poly([p(dL, 0, 0), p(dL, 0, dB), p(dL, dH, dB), p(dL, dH, 0)], SIDE, 2.4)
    for a, b in [((0, 0, dB), (dL, 0, dB)), ((0, 0, dB), (0, dH, dB)), ((0, 0, dB), (0, 0, 0))]:
        cv.line(p(*a), p(*b), dashed=True)
    if lab_l:
        x, y = p(dL / 2, 0, 0)
        cv.text(x, y + 17, lab_l, 16, col=colr(lab_l))
    if lab_h:
        x, y = p(0, dH / 2, 0)
        cv.text(x - 8, y, lab_h, 16, "end", colr(lab_h))
    if lab_b:
        x, y = p(dL, 0, dB / 2)
        cv.text(x + 7, y + 11, lab_b, 16, "start", colr(lab_b))
    return cv.svg(label)


def cubes_svg(l, w, h, label="cuboid made of 1-cm cubes", k=22, gap=0.0):
    cubes = [(i, j, m) for i in range(l) for j in range(h) for m in range(w)]
    keys = set(cubes)
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


def visible_cubes(l, w, h):
    return l * w * h - (l - 1) * (w - 1) * (h - 1)


def dim_v(cv, x, y0, y1, t, side="left", col=INK):
    """Vertical |<-->| from y0 to y1 at x, label to the left or right."""
    a, b = min(y0, y1) + 1, max(y0, y1) - 1
    cv.line((x, a), (x, b), sw=1.4, col=col)
    cv.line((x - 5, a), (x + 5, a), sw=1.4, col=col)
    cv.line((x - 5, b), (x + 5, b), sw=1.4, col=col)
    if side == "left":
        cv.text(x - 8, (a + b) / 2, t, 16, "end", colr(t))
    else:
        cv.text(x + 8, (a + b) / 2, t, 16, "start", colr(t))


def tank_svg(L, B, H, d, lab_l, lab_b, lab_h, lab_d, label="open tank with water in it"):
    """Glass tank L × B × H (open top) with water d deep. The water depth is measured on the left of the front,
    the tank height on the right of the back edge."""
    dL, dB, dH = disp_dims(L, B, H)
    k = min(165 / (dL + dB * DZX), 100 / (dH + dB * DZY), 26)
    dw = dH * float(Fr(d) / Fr(H)) if d else 0
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    for a, b in [((0, 0, dB), (dL, 0, dB)), ((0, 0, dB), (0, dH, dB)), ((0, 0, dB), (0, 0, 0)), ((dL, 0, dB), (dL, dH, dB))]:
        cv.line(p(*a), p(*b), dashed=True, col=GREY)
    if dw:
        cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, dw, 0), p(0, dw, 0)], W_FRONT, 1.4, W_LINE)
        cv.poly([p(0, dw, 0), p(dL, dw, 0), p(dL, dw, dB), p(0, dw, dB)], W_TOP, 1.4, W_LINE)
        cv.poly([p(dL, 0, 0), p(dL, 0, dB), p(dL, dw, dB), p(dL, dw, 0)], W_SIDE, 1.4, W_LINE)
    cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, dH, 0), p(0, dH, 0)], "none", 2.4)
    cv.poly([p(dL, 0, 0), p(dL, 0, dB), p(dL, dH, dB), p(dL, dH, 0)], "none", 2.4)
    cv.poly([p(0, dH, 0), p(dL, dH, 0), p(dL, dH, dB), p(0, dH, dB)], "none", 2.4)
    if lab_l:
        x, y = p(dL / 2, 0, 0)
        cv.text(x, y + 17, lab_l, 16, col=colr(lab_l))
    if lab_b:
        x, y = p(dL, 0, dB / 2)
        cv.text(x + 7, y + 11, lab_b, 16, "start", colr(lab_b))
    if lab_d and dw:
        x0, y0 = p(0, 0, 0)
        dim_v(cv, x0 - 10, y0, p(0, dw, 0)[1], lab_d, "left", W_LINE)
    if lab_h:
        xa, ya = p(dL, 0, dB)
        dim_v(cv, xa + 12, ya, p(dL, dH, dB)[1], lab_h, "right")
    return cv.svg(label)


def square_svg(lab_side, lab_area, label="square with its area"):
    cv = Canvas()
    s = 92
    cv.poly([(0, 0), (s, 0), (s, s), (0, s)], FILL, 2.4)
    cv.text(s / 2, s / 2 - 10, "Area", 15, free=True)
    cv.text(s / 2, s / 2 + 10, lab_area, 15, free=True)
    cv.text(s / 2, s + 15, lab_side, 16, col=colr(lab_side))
    return cv.svg(label)


def model_svg(rows, label="bar model", braces=(), unit=None, maxw=250):
    """rows = [(name, [(units, fill, text)], right_text)]. braces = [(row, u0, u1, text, 'above'|'below')].
    Every unit is drawn the same width, so the model is exact. A segment's text goes under a brace below it,
    so no unit line runs through a label."""
    braces = list(braces)
    for ri, (name, segs, right) in enumerate(rows):
        u0 = 0
        for n, fill, t in segs:
            if t:
                braces.append((ri, u0, u0 + n, t, "below"))
            u0 += n
    nw = max(tw(r[0], 15) for r in rows) + 10
    most = max(sum(s[0] for s in r[1]) for r in rows)
    U = unit or min(maxw / most, 46)
    cv = Canvas()
    y = 0
    BH = 28
    for ri, (name, segs, right) in enumerate(rows):
        if any(b[0] == ri and b[4] == "above" for b in braces):
            y += 30
        cv.text(nw - 10, y + BH / 2, name, 15, "end")
        x = nw
        for n, fill, t in segs:
            for j in range(int(n)):
                cv.rect(x + j * U, y, U, BH, fill, 1.6)
            x += n * U
        if right:
            cv.text(x + 8, y + BH / 2, right, 15, "start", colr(right))
        for b in braces:
            if b[0] != ri:
                continue
            _, u0, u1, t, pos = b
            xa, xb = nw + u0 * U + 2, nw + u1 * U - 2
            yy = y - 8 if pos == "above" else y + BH + 8
            tick = 6 if pos == "above" else -6
            cv.line((xa, yy), (xb, yy), sw=1.6, col=INK)
            cv.line((xa, yy), (xa, yy + tick), sw=1.6, col=INK)
            cv.line((xb, yy), (xb, yy + tick), sw=1.6, col=INK)
            cv.text((xa + xb) / 2, yy - 11 if pos == "above" else yy + 11, t, 15, col=colr(t))
        y += BH
        if any(b[0] == ri and b[4] == "below" for b in braces):
            y += 30
        y += 12
    return cv.svg(label)


# ------------------------------------------------------------ set 1: volume of cubes and cuboids
def set_review(rnd):
    its = []
    for (l, w, h) in [(4, 2, 3), (3, 3, 2), (5, 2, 2), (4, 3, 3)]:
        V, vis = l * w * h, visible_cubes(l, w, h)
        faces = l * h + l * w + w * h
        q = fig(cubes_svg(l, w, h)) + "The solid is made of 1-cm cubes. What is its volume?"
        e = ("One layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = %d cm³. "
             "Count the hidden cubes too (only %d cubes can be seen)." % (w, l, l * w, h, l * w, h, V, vis))
        its.append(mcq(q, "%d cm³" % V, ["%d cm³" % x for x in (vis, faces, l * w * (h - 1), l + w + h) if x != V], e, rnd))
    seen = set()
    VOLU = [("cm", "cm³", "cm²"), ("m", "m³", "m²")]
    for i in range(7):
        while True:
            L, B, H = rnd.randint(5, 16), rnd.randint(3, 9), rnd.randint(2, 12)
            if L > B and H != B and H != L and (L, B, H) not in seen:
                break
        seen.add((L, B, H))
        u, cu, sq = VOLU[i % 3 == 2]
        V = L * B * H
        lab = lambda v: "%d %s" % (v, u)
        q = fig(cuboid_svg(L, B, H, lab(L), lab(B), lab(H))) + "Find the volume of the cuboid."
        e = ("Volume = length × breadth × height = %d × %d × %d = %s × %d = %s %s. Multiply all three lengths "
             "and write the answer in cubic units (%s)." % (L, B, H, num(L * B), H, num(V), cu, cu))
        pool = [q_(L * B, cu), q_(L + B + H, cu), q_(V, sq), q_(L * B + B * H + L * H, cu)]
        r = i % 4
        its.append(mcq(q, q_(V, cu), pool[r:] + pool[:r], e, rnd))
    for s, u in [(5, "cm"), (8, "cm"), (12, "m")]:
        V = s ** 3
        q = "A cube has edges of %d %s. Find its volume." % (s, u)
        e = "All the edges of a cube are equal: volume = %d × %d × %d = %d × %d = %s %s³." % (s, s, s, s * s, s, num(V), u)
        its.append(mcq(q, q_(V, u + "³"), [q_(3 * s, u + "³"), q_(s * s, u + "³"), q_(V, u + "²")], e, rnd))
    q = "A cuboid is 2.5 m long, 1.2 m wide and 0.8 m high. Find its volume."
    e = "Volume = 2.5 × 1.2 × 0.8 = 3 × 0.8 = 2.4 m³."
    assert Fr(25, 10) * Fr(12, 10) * Fr(8, 10) == Fr(24, 10)
    its.append(mcq(q, "2.4 m³", ["4.5 m³", "3 m³", "2.4 m²"], e, rnd))
    q = "A block of wood is 1.5 m long, 0.6 m wide and 2 m tall. Find its volume."
    e = "Volume = 1.5 × 0.6 × 2 = 0.9 × 2 = 1.8 m³. 0.9 m² is only the area of the base."
    assert Fr(15, 10) * Fr(6, 10) * 2 == Fr(18, 10)
    its.append(mcq(q, "1.8 m³", ["4.1 m³", "0.9 m³", "1.8 m²"], e, rnd))
    q = "A container has a capacity of 4500 cm³. What is its capacity in litres? (1 ℓ = 1000 cm³)"
    e = "1 ℓ = 1000 cm³, so divide by 1000: 4500 ÷ 1000 = 4.5 ℓ."
    its.append(mcq(q, "4.5 ℓ", ["45 ℓ", "450 ℓ", "4500 ℓ"], e, rnd))
    q = "A jug holds 2 ℓ 350 ml of water. What is this volume in cm³?"
    e = "1 ℓ = 1000 cm³ and 1 ml = 1 cm³. 2 ℓ 350 ml = 2000 ml + 350 ml = 2350 ml = 2350 cm³."
    its.append(mcq(q, "2350 cm³", ["235 cm³", "23" + NB + "500 cm³", "2.35 cm³"], e, rnd))
    q = "How many cubic centimetres are there in 1 m³?"
    e = ("1 m = 100 cm, so a 1 m cube is 100 cm × 100 cm × 100 cm = 1" + NB + "000" + NB + "000 cm³. "
         "(1 m² = 10" + NB + "000 cm², because area has only two lengths.)")
    its.append(mcq(q, "1" + NB + "000" + NB + "000 cm³", ["100 cm³", "1000 cm³", "10" + NB + "000 cm³"], e, rnd))
    q = "Which of these is a volume?"
    e = "Volume is measured in cubic units (cm³, m³). cm² is an area, cm is a length and kg is a mass."
    its.append(mcq(q, "450 cm³", ["450 cm²", "450 cm", "450 kg"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Volume of cubes and cuboids", "items": its}


# ------------------------------------------------------------ set 2: a missing dimension
def set_missing(rnd):
    its = []
    seen = set()
    names = {"l": "length", "b": "breadth", "h": "height"}
    # figure: one length marked "?"
    for i, miss in enumerate(["h", "b", "l", "h"]):
        while True:
            L, B, H = rnd.randint(6, 15), rnd.randint(3, 9), rnd.randint(4, 12)
            if L > B and H not in (L, B) and (L, B, H) not in seen:
                break
        seen.add((L, B, H))
        u, cu = ("cm", "cm³") if i != 2 else ("m", "m³")
        V = L * B * H
        vals = {"l": L, "b": B, "h": H}
        a, b = [vals[x] for x in "lbh" if x != miss]
        ans = vals[miss]
        labs = {x: "%d %s" % (vals[x], u) for x in "lbh"}
        labs[miss] = "? " + u
        q = (fig(cuboid_svg(L, B, H, labs["l"], labs["b"], labs["h"], "cuboid with one unknown length")) +
             "The volume of the cuboid is %s %s. Find the unknown %s." % (num(V), cu, names[miss]))
        e = ("%d × %d × ? = %s, so %d × ? = %s. ? = %s ÷ %d = %d %s. Divide by both of the other lengths. "
             "Check: %d × %d × %d = %s." % (a, b, num(V), a * b, num(V), num(V), a * b, ans, u, L, B, H, num(V)))
        its.append(mcq(q, q_(ans, u), [opt(Fr(V, a), u), opt(Fr(V, b), u), q_(ans, cu), opt(V - a * b, u)], e, rnd))
    # text: missing length / breadth / height
    for i, (L, B, H, miss) in enumerate([(15, 8, 9, "h"), (12, 7, 10, "b"), (20, 6, 5, "l"),
                                          (25, 14, 6, "h"), (18, 15, 8, "b"), (16, 9, 12, "l")]):
        u, cu = "cm", "cm³"
        V = L * B * H
        vals = {"l": L, "b": B, "h": H}
        known = [x for x in "lbh" if x != miss]
        a, b = vals[known[0]], vals[known[1]]
        ans = vals[miss]
        q = ("A cuboid has a volume of %s %s. Its %s is %d %s and its %s is %d %s. Find its %s."
             % (num(V), cu, names[known[0]], a, u, names[known[1]], b, u, names[miss]))
        e = ("%s ÷ (%d × %d) = %s ÷ %d = %d %s. Check: %d × %d × %d = %s."
             % (num(V), a, b, num(V), a * b, ans, u, L, B, H, num(V)))
        its.append(mcq(q, q_(ans, u), [opt(Fr(V, a), u), opt(Fr(V, b), u), q_(ans, cu), opt(V - a - b, u)], e, rnd))
    # square base of side s
    for s, h in [(5, 8), (6, 7), (9, 4)]:
        V = s * s * h
        q = "A cuboid has a square base of side %d cm. Its volume is %s cm³. Find its height." % (s, num(V))
        e = ("Area of base = %d × %d = %d cm². Height = %s ÷ %d = %d cm. (%d × 2 = %d is not the area of the base.)"
             % (s, s, s * s, num(V), s * s, h, s, 2 * s))
        its.append(mcq(q, q_(h, "cm"), [opt(Fr(V, s), "cm"), opt(Fr(V, 2 * s), "cm"), q_(h, "cm²")], e, rnd))
    # base area given
    for A, h in [(80, 5), (120, 8), (250, 4)]:
        V = A * h
        q = "A cuboid has a volume of %s cm³. The area of its base is %d cm². Find its height." % (num(V), A)
        e = ("Volume = area of base × height, so height = volume ÷ area of base = %s ÷ %d = %d cm. "
             "Check: %d × %d = %s." % (num(V), A, h, A, h, num(V)))
        its.append(mcq(q, q_(h, "cm"), [opt(Fr(A, V), "cm"), opt(V - A, "cm"), q_(h, "cm²")], e, rnd))
    # base area from volume and height
    for V, h in [(360, 6), (1350, 9)]:
        A = V // h
        q = "A cuboid has a volume of %s cm³ and a height of %d cm. Find the area of its base." % (num(V), h)
        e = "Area of base = volume ÷ height = %s ÷ %d = %d cm². An area is in square units (cm²)." % (num(V), h, A)
        its.append(mcq(q, q_(A, "cm²"), [q_(A, "cm³"), q_(V - h, "cm²"), q_(V * h, "cm²")], e, rnd))
    # decimals in metres
    q = "A container has a volume of 1.2 m³. It is 2 m long and 0.5 m high. Find its breadth."
    e = "2 × 0.5 = 1 m². Breadth = 1.2 ÷ 1 = 1.2 m. Check: 2 × 1.2 × 0.5 = 1.2 m³."
    assert 2 * Fr(12, 10) * Fr(1, 2) == Fr(12, 10)
    its.append(mcq(q, "1.2 m", ["0.6 m", "2.4 m", "1.2 m³"], e, rnd))
    q = "A concrete block has a volume of 4.8 m³. Its base is 2.4 m by 1.25 m. Find its height."
    e = "Area of base = 2.4 × 1.25 = 3 m². Height = 4.8 ÷ 3 = 1.6 m. Check: 3 × 1.6 = 4.8 m³."
    assert Fr(24, 10) * Fr(125, 100) * Fr(16, 10) == Fr(48, 10)
    its.append(mcq(q, "1.6 m", ["2 m", "3.84 m", "1.6 m³"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Finding a missing length", "items": its}


# ------------------------------------------------------------ set 3: cube roots and square roots
def set_roots(rnd):
    its = []
    vols = [27, 64, 125, 216, 343, 512, 729, 1000]
    rnd.shuffle(vols)
    for i, V in enumerate(vols):
        s = round(V ** (1 / 3))
        assert s ** 3 == V
        u = "m" if i in (3, 6) else "cm"
        third = Fr(V, 3) if V % 3 == 0 else None
        cands = [q_(third, u) if third else None, q_(s * s, u), q_(s, u + "³"), q_(s + 1, u)]
        e = ("Edge × edge × edge = %d. Find the number that multiplies by itself 3 times to give %d: "
             "%d × %d × %d = %d, so ∛%d = %d %s." % (V, V, s, s, s, V, V, s, u))
        if third:
            e += " Do not divide by 3: %d ÷ 3 = %d, and %d × %d × %d is not %d." % (V, third, third, third, third, V)
        if i < 4:
            q = fig(cuboid_svg(s, s, s, "? " + u, None, None, "cube with an unknown edge")) + \
                "The volume of this cube is %s %s³. Find the length of one edge." % (num(V), u)
        else:
            q = "A cube has a volume of %s %s³. What is the length of each edge?" % (num(V), u)
        its.append(mcq(q, q_(s, u), cands, e, rnd))
    for i, (A, u) in enumerate([(49, "cm"), (81, "m"), (121, "cm"), (144, "cm")]):
        s = math.isqrt(A)
        q = "A square has an area of %d %s². Find the length of one side." % (A, u)
        if i < 2:
            q = fig(square_svg("? " + u, "%d %s²" % (A, u))) + q
        e = ("Side × side = %d. %d × %d = %d, so √%d = %d %s. Do not halve the area or divide it by 4 (÷ 4 finds the side from the perimeter)."
             % (A, s, s, A, A, s, u))
        its.append(mcq(q, q_(s, u), [opt(Fr(A, 4), u), opt(Fr(A, 2), u), q_(s, u + "²")], e, rnd))
    for V in [64, 343, 1000, 729]:
        s = round(V ** (1 / 3))
        q = "A cube has a volume of %s cm³. Find the area of one face." % num(V)
        e = ("Edge = ∛%s = %d cm. A face is a %d cm by %d cm square: %d × %d = %d cm². "
             "(All 6 faces would be %s cm².)" % (num(V), s, s, s, s, s, s * s, num(6 * s * s)))
        its.append(mcq(q, q_(s * s, "cm²"), [q_(s, "cm²"), q_(6 * s * s, "cm²"), q_(s * s, "cm³")], e, rnd))
    for A in [49, 81]:
        s = math.isqrt(A)
        V = s ** 3
        q = "One face of a cube has an area of %d cm². Find the volume of the cube." % A
        e = ("Edge = √%d = %d cm. Volume = %d × %d × %d = %d × %d = %s cm³." % (A, s, s, s, s, A, s, num(V)))
        its.append(mcq(q, q_(V, "cm³"), [q_(6 * A, "cm³"), q_(3 * A, "cm³"), q_(V, "cm²")], e, rnd))
    q = "The total length of all the edges of a cube is 96 cm. Find the volume of the cube."
    e = "A cube has 12 equal edges (not 4 or 6). Edge = 96 ÷ 12 = 8 cm. Volume = 8 × 8 × 8 = 512 cm³."
    its.append(mcq(q, "512 cm³", [q_(16 ** 3, "cm³"), q_(24 ** 3, "cm³"), "512 cm²"], e, rnd))
    q = "A cuboid has a square base and a height of 5 cm. Its volume is 245 cm³. Find the length of one side of its base."
    e = "Area of base = 245 ÷ 5 = 49 cm². The base is a square, so its side = √49 = 7 cm."
    its.append(mcq(q, "7 cm", ["49 cm", "24.5 cm", "7 cm²"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Cube roots and square roots", "items": its}


# ------------------------------------------------------------ set 4: water in tanks
def L_(cm3):
    return Fr(cm3, 1000)


def set_tanks(rnd):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    def T(L, B, H, d, lh=True, ld=None, label="open tank with water in it"):
        return fig(tank_svg(L, B, H, d, "%d cm" % L, "%d cm" % B, ("%d cm" % H) if lh else None,
                            ld if ld is not None else ("%s cm" % num(d) if d else None), label))

    # capacity of a full tank
    for i, (L, B, H) in enumerate([(50, 40, 30), (60, 45, 40), (80, 50, 45)]):
        V = L * B * H
        c = L_(V)
        q = "A tank is %d cm long, %d cm wide and %d cm high. How many litres of water can it hold?" % (L, B, H)
        if i == 0:
            q = fig(tank_svg(L, B, H, 0, "%d cm" % L, "%d cm" % B, "%d cm" % H, None, "empty open tank")) + \
                "How many litres of water can this tank hold?"
        e = "Volume = %d × %d × %d = %s cm³. 1 ℓ = 1000 cm³, so %s ÷ 1000 = %s ℓ." % (L, B, H, num(V), num(V), num(c))
        add(q, q_(c, "ℓ"), [q_(c * 10, "ℓ"), q_(c / 10, "ℓ"), q_(V, "ℓ")], e)
    # water to a given depth
    for (L, B, H, d) in [(40, 30, 35, 20), (60, 40, 50, 35), (50, 25, 40, 28)]:
        V = L * B * d
        full, empty = L_(L * B * H), L_(L * B * (H - d))
        q = T(L, B, H, d) + "The water in the tank is %d cm deep. How many litres of water are in the tank?" % d
        e = ("Use the depth of the water, not the height of the tank: %d × %d × %d = %s cm³ = %s ℓ (÷ 1000)."
             % (L, B, d, num(V), num(L_(V))))
        add(q, q_(L_(V), "ℓ"), [q_(full, "ℓ"), q_(empty, "ℓ"), q_(L_(V) * 10, "ℓ")], e)
    # water poured into an empty tank: depth
    for (L, B, H, X) in [(40, 25, 45, 30), (50, 30, 40, 24), (60, 40, 30, 36)]:
        A = L * B
        d = Fr(X * 1000, A)
        q = ("%d ℓ of water is poured into an empty tank. The tank is %d cm long, %d cm wide and %d cm high. "
             "What is the depth of the water?" % (X, L, B, H))
        if X == 24:
            q = T(L, B, H, d, ld="? cm") + "%d ℓ of water is poured into this empty tank. What is the depth of the water?" % X
        e = ("%d ℓ = %s cm³ (1 ℓ = 1000 cm³). Depth = volume ÷ area of base = %s ÷ (%d × %d) = %s ÷ %d = %s cm."
             % (X, num(X * 1000), num(X * 1000), L, B, num(X * 1000), A, num(d)))
        add(q, q_(d, "cm"), [opt(Fr(X * 1000, L), "cm"), opt(Fr(X * 100, A), "cm"), opt(Fr(X, A), "cm"),
                             opt(Fr(X * 1000, B), "cm")], e)
    # water level rises
    q = "A tank has a base 50 cm by 40 cm. 12 ℓ of water is poured into it. By how much does the water level rise?"
    e = "12 ℓ = 12" + NB + "000 cm³. Rise = 12" + NB + "000 ÷ (50 × 40) = 12" + NB + "000 ÷ 2000 = 6 cm."
    add(q, "6 cm", ["240 cm", "0.6 cm", "300 cm"], e)
    q = T(45, 40, 40, 10) + "Ali pours 27 ℓ more water into the tank. What is the new depth of the water?"
    assert Fr(27000, 45 * 40) == 15
    e = "27 ℓ = 27" + NB + "000 cm³. Rise = 27" + NB + "000 ÷ (45 × 40) = 27" + NB + "000 ÷ 1800 = 15 cm. New depth = 10 + 15 = 25 cm."
    add(q, "25 cm", ["15 cm", "37 cm", "35 cm"], e)
    q = ("A tank has a base 30 cm by 20 cm. It contains water 8 cm deep. 4.2 ℓ of water is added. "
         "What is the new depth of the water?")
    assert Fr(4200, 600) == 7
    e = "4.2 ℓ = 4200 cm³. Rise = 4200 ÷ (30 × 20) = 4200 ÷ 600 = 7 cm. New depth = 8 + 7 = 15 cm."
    add(q, "15 cm", ["7 cm", "12.2 cm", "8.7 cm"], e)
    # water drained
    q = ("A tank has a base 60 cm by 30 cm. The water in it is 40 cm deep. 27 ℓ of water is drained out. "
         "What is the depth of the water now?")
    assert Fr(27000, 1800) == 15
    e = "27 ℓ = 27" + NB + "000 cm³. Fall = 27" + NB + "000 ÷ (60 × 30) = 27" + NB + "000 ÷ 1800 = 15 cm. New depth = 40 − 15 = 25 cm."
    add(q, "25 cm", ["15 cm", "13 cm", "55 cm"], e)
    q = T(50, 40, 40, 32) + "Water is let out until the water is 20 cm deep. How many litres of water were let out?"
    e = "The water fell by 32 − 20 = 12 cm. Volume let out = 50 × 40 × 12 = 24" + NB + "000 cm³ = 24 ℓ."
    add(q, "24 ℓ", ["64 ℓ", "40 ℓ", "240 ℓ"], e)
    q = ("A tank has a base 80 cm by 50 cm. The water in it is 45 cm deep. 60 ℓ of water is used. "
         "What is the depth of the water now?")
    assert Fr(60000, 4000) == 15
    e = "60 ℓ = 60" + NB + "000 cm³. Fall = 60" + NB + "000 ÷ (80 × 50) = 60" + NB + "000 ÷ 4000 = 15 cm. New depth = 45 − 15 = 30 cm."
    add(q, "30 cm", ["15 cm", "60 cm", "30 cm³"], e)
    # more water needed to fill
    q = T(50, 40, 60, 35) + "How many more litres of water are needed to fill the tank to the brim?"
    e = "Empty part: 60 − 35 = 25 cm high. 50 × 40 × 25 = 50" + NB + "000 cm³ = 50 ℓ."
    add(q, "50 ℓ", ["70 ℓ", "120 ℓ", "500 ℓ"], e)
    q = ("A tank 40 cm long, 40 cm wide and 50 cm high contains 32 ℓ of water. How many more litres are needed "
         "to fill it completely?")
    assert 40 * 40 * 50 == 80000
    e = "Capacity = 40 × 40 × 50 = 80" + NB + "000 cm³ = 80 ℓ. More water needed = 80 − 32 = 48 ℓ."
    add(q, "48 ℓ", ["80 ℓ", "112 ℓ", "18 ℓ"], e)
    q = ("A tank 60 cm long, 30 cm wide and 45 cm high is empty. Water is poured in until it is 30 cm deep. "
         "How many more litres are needed to fill it to the brim?")
    e = "The empty part is 45 − 30 = 15 cm high. 60 × 30 × 15 = 27" + NB + "000 cm³ = 27 ℓ."
    add(q, "27 ℓ", ["54 ℓ", "81 ℓ", "270 ℓ"], e)
    # fraction of a tank
    q = ("A tank is 60 cm long, 50 cm wide and 40 cm high. It is " + frac(3, 4) + " full of water. "
         "How many litres of water are in it?")
    e = "Capacity = 60 × 50 × 40 = 120" + NB + "000 cm³ = 120 ℓ. " + frac(3, 4) + " of 120 ℓ = 90 ℓ."
    add(q, "90 ℓ", ["120 ℓ", "30 ℓ", "900 ℓ"], e)
    q = ("A tank is 50 cm long, 40 cm wide and 60 cm high. It is " + frac(2, 5) + " full of water. "
         "What is the depth of the water?")
    e = "The water fills " + frac(2, 5) + " of the height: " + frac(2, 5) + " × 60 = 24 cm. The length and breadth do not change."
    add(q, "24 cm", ["36 cm", "20 cm", "16 cm"], e)
    assert len(its) == 20, len(its)
    return {"title": "Water in tanks", "items": its}


# ------------------------------------------------------------ set 5: PSLE-style word problems
def set_psle(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    # 1 tank A poured into tank B
    n, he, his = P.next()
    assert 40 * 30 * 25 == 30000 and Fr(30000, 50 * 40) == 15
    add("%s fills Tank A, 40 cm by 30 cm by 25 cm, to the brim with water. %s then pours all the water into an "
        "empty Tank B with a base 50 cm by 40 cm. What is the depth of the water in Tank B?" % (n, he.capitalize()),
        "15 cm", ["25 cm", "600 cm", "12.5 cm"],
        "Water in A = 40 × 30 × 25 = 30" + NB + "000 cm³. Depth in B = 30" + NB + "000 ÷ (50 × 40) = 30" + NB +
        "000 ÷ 2000 = 15 cm. The water is the same; only the base changes.")
    # 2 fraction full: model
    svg = model_svg([("Tank", [(3, UNIT_FILL, "36 ℓ"), (2, WHITE, "?")], "")], "bar model of a tank in 5 units",
                    braces=[(0, 0, 5, "full tank", "above")])
    add(fig(svg) + "Mrs Lim's tank is " + frac(3, 5) + " full. It has 36 ℓ of water in it. "
        "How many more litres of water are needed to fill the tank?",
        "24 ℓ", ["60 ℓ", "12 ℓ", "21.6 ℓ"],
        "3 units = 36 ℓ, so 1 unit = 12 ℓ. The empty part is 2 units = 2 × 12 = 24 ℓ. (The full tank is 5 units = 60 ℓ.)")
    # 3 before and after
    svg = model_svg([("Before", [(2, UNIT_FILL, ""), (3, WHITE, "")], ""),
                     ("After", [(2, UNIT_FILL, ""), (2, UNIT_FILL2, "18 ℓ"), (1, WHITE, "")], "")],
                    "bar model of a tank before and after", braces=[(0, 0, 5, "capacity = ?", "above")])
    add(fig(svg) + "A tank is " + frac(2, 5) + " full of water. After 18 ℓ of water is added, it is " +
        frac(4, 5) + " full. What is the capacity of the tank?",
        "45 ℓ", ["36 ℓ", "90 ℓ", "22.5 ℓ"],
        "The 18 ℓ fills " + frac(4, 5) + " − " + frac(2, 5) + " = " + frac(2, 5) + " of the tank. "
        "2 units = 18 ℓ, so 1 unit = 9 ℓ. Capacity = 5 units = 5 × 9 = 45 ℓ.")
    # 4 three times as much water
    svg = model_svg([("A", [(3, UNIT_FILL, "")], "3 units"),
                     ("B", [(1, UNIT_FILL2, "")], "1 unit")], "bar model comparing water in two containers")
    n, he, his = P.next()
    add(fig(svg) + "Container A has 3 times as much water as Container B. Together they hold 48 ℓ. "
        "%s pours water from A into B until they have the same amount. How many litres does %s pour?" % (n, he),
        "12 ℓ", ["24 ℓ", "16 ℓ", "36 ℓ"],
        "4 units = 48 ℓ, so 1 unit = 12 ℓ. A has 36 ℓ and B has 12 ℓ. Each needs 48 ÷ 2 = 24 ℓ, "
        "so pour 36 − 24 = 12 ℓ (1 unit).")
    # 5 tap filling
    n, he, his = P.next()
    assert 60 * 40 * 50 == 120000 and Fr(120, 8) == 15
    add("An empty tank is 60 cm long, 40 cm wide and 50 cm high. A tap fills it at 8 ℓ per minute. "
        "How long does it take to fill the tank?",
        "15 min", ["150 min", "1.5 min", "960 min"],
        "Capacity = 60 × 40 × 50 = 120" + NB + "000 cm³ = 120 ℓ. Time = 120 ÷ 8 = 15 min.")
    # 6 partly filled then tap
    assert 50 * 40 * (45 - 15) == 60000 and Fr(60, 6) == 10
    add("A tank 50 cm long, 40 cm wide and 45 cm high has water 15 cm deep. Water flows in from a tap at 6 ℓ per minute. "
        "How long will it take to fill the tank to the brim?",
        "10 min", ["15 min", "5 min", "100 min"],
        "The empty part is 45 − 15 = 30 cm high: 50 × 40 × 30 = 60" + NB + "000 cm³ = 60 ℓ. "
        "Time = 60 ÷ 6 = 10 min. (15 min would fill the whole tank, 90 ℓ.)")
    # 7 cubes in a box
    n, he, his = P.next()
    add("%s packs 3-cm cubes into a box 12 cm long, 9 cm wide and 6 cm high. How many cubes fit in the box?" % n,
        "24", ["216", "648", "27"],
        "Along the length: 12 ÷ 3 = 4. Breadth: 9 ÷ 3 = 3. Height: 6 ÷ 3 = 2. Cubes = 4 × 3 × 2 = 24. "
        "Or: the box is 648 cm³ and one cube is 3 × 3 × 3 = 27 cm³, so 648 ÷ 27 = 24. (648 ÷ 3 = 216 divides by the edge, not the volume of a cube.)")
    # 8 stone raises level
    n, he, his = P.next()
    assert 30 * 20 * 2 == 1200
    add("A tank has a base 30 cm by 20 cm and contains some water. %s puts a stone into it. The stone sinks and the "
        "water level rises by 2 cm. Find the volume of the stone." % n,
        "1200 cm³", ["600 cm³", "120 cm³", "1200 cm²"],
        "The stone pushes up a layer of water 30 cm by 20 cm by 2 cm. Volume of stone = 30 × 20 × 2 = 1200 cm³.")
    # 9 equal heights
    assert 40 * 25 * 30 == 30000 and Fr(30000, 1000 + 1500) == 12
    add("Tank A has a base 40 cm by 25 cm and water 30 cm deep. Tank B has a base 50 cm by 30 cm and is empty. "
        "Water is poured from A into B until the water in both tanks is the same depth. What is this depth?",
        "12 cm", ["15 cm", "20 cm", "18 cm"],
        "Water = 40 × 25 × 30 = 30" + NB + "000 cm³. The two bases together are 1000 + 1500 = 2500 cm². "
        "Depth = 30" + NB + "000 ÷ 2500 = 12 cm. (15 cm is half of 30, but the bases are not the same size.)")
    # 10 clay reshaped
    n, he, his = P.next()
    assert 20 * 12 * 8 == 1920 and 1920 // 64 == 30 and 5 * 3 * 2 == 30
    add("%s has a block of clay 20 cm by 12 cm by 8 cm. %s cuts it into cubes with 4-cm edges. "
        "How many cubes does %s make?" % (n, he.capitalize(), he),
        "30", ["480", "120", "1920"],
        "Clay = 20 × 12 × 8 = 1920 cm³. One cube = 4 × 4 × 4 = 64 cm³. 1920 ÷ 64 = 30 cubes. "
        "Check: 20 ÷ 4 = 5, 12 ÷ 4 = 3, 8 ÷ 4 = 2, and 5 × 3 × 2 = 30. (1920 ÷ 4 = 480 uses the edge, not the volume of a cube.)")
    # 11 cube volume to edges
    add("A wooden cube has a volume of 512 cm³. Ribbon is glued along every edge. How much ribbon is used?",
        "96 cm", ["64 cm", "32 cm", "48 cm"],
        "Edge = ∛512 = 8 cm. A cube has 12 edges: 12 × 8 = 96 cm.")
    # 12 square base height
    add("A box has a square base. Its height is 15 cm and its volume is 960 cm³. Find the length of one side of the base.",
        "8 cm", ["64 cm", "32 cm", "8 cm²"],
        "Area of base = 960 ÷ 15 = 64 cm². The base is a square: side = √64 = 8 cm.")
    # 13 drain
    assert 80 * 50 * 30 == 120000 and Fr(120, 12) == 10
    add("A tank 80 cm long and 50 cm wide has water 45 cm deep. Water drains out at 12 ℓ per minute. "
        "How long does it take for the depth to fall to 15 cm?",
        "10 min", ["15 min", "5 min", "100 min"],
        "The depth falls by 45 − 15 = 30 cm. Water drained = 80 × 50 × 30 = 120" + NB + "000 cm³ = 120 ℓ. "
        "Time = 120 ÷ 12 = 10 min. (15 min would empty the whole 180 ℓ.)")
    # 14 fraction used, remainder model
    svg = model_svg([("Water", [(4, UNIT_FILL2, "used"), (2, UNIT_FILL2, "used"), (6, UNIT_FILL, "36 ℓ left")], "")],
                    "bar model of water used and left", braces=[(0, 0, 12, "72 ℓ", "above")], maxw=264)
    assert 72 - 24 - Fr(1, 4) * 48 == 36 and Fr(36000, 60 * 40) == 15
    add(fig(svg) + "Mr Rahman's tank has a base 60 cm by 40 cm and holds 72 ℓ of water. He uses " + frac(1, 3) +
        " of the water, then " + frac(1, 4) + " of the remaining water. What is the depth of the water left?",
        "15 cm", ["30 cm", "12.5 cm", "36 cm"],
        frac(1, 3) + " of 72 = 24 ℓ, leaving 48 ℓ. " + frac(1, 4) + " of 48 = 12 ℓ, leaving 36 ℓ. "
        "36 ℓ = 36" + NB + "000 cm³. Depth = 36" + NB + "000 ÷ (60 × 40) = 36" + NB + "000 ÷ 2400 = 15 cm. (Take " + frac(1, 4) + " of the remaining 48 ℓ, not of 72 ℓ.)")
    # 15 percentage
    assert 40 * 40 * 50 == 80000
    add("A fish tank is 40 cm long, 40 cm wide and 50 cm high. It is filled to 75% of its height. "
        "How many litres of water are in the tank?",
        "60 ℓ", ["80 ℓ", "20 ℓ", "600 ℓ"],
        "Depth = 75% of 50 = 37.5 cm. Water = 40 × 40 × 37.5 = 60" + NB + "000 cm³ = 60 ℓ. "
        "(Or 75% of the 80 ℓ capacity = 60 ℓ.)")
    # 16 ratio
    svg = model_svg([("P", [(2, UNIT_FILL, "")], ""), ("Q", [(3, UNIT_FILL2, "")], "")],
                    "bar model of the ratio 2 to 3", braces=[(1, 0, 3, "?", "below")])
    add(fig(svg) + "The volumes of water in Containers P and Q are in the ratio 2 : 3. P has 6 ℓ less water than Q. "
        "How much water is in Q?",
        "18 ℓ", ["12 ℓ", "30 ℓ", "6 ℓ"],
        "Q has 1 unit more than P. 1 unit = 6 ℓ. Q = 3 units = 3 × 6 = 18 ℓ. (P has 12 ℓ; together 30 ℓ.)")
    # 17 jugs
    n, he, his = P.next()
    assert 4 * 1250 == 5000 and Fr(5000, 50 * 20) == 5
    add("%s pours 4 jugs of water into an empty tank with a base 50 cm by 20 cm. Each jug holds 1 ℓ 250 ml. "
        "What is the depth of the water in the tank?" % n,
        "5 cm", ["4 cm", "1.25 cm", "50 cm"],
        "4 × 1250 ml = 5000 ml = 5000 cm³. Depth = 5000 ÷ (50 × 20) = 5000 ÷ 1000 = 5 cm.")
    # 18 bottles from full tank
    n, he, his = P.next()
    assert 60 * 30 * 40 == 72000 and 18 * Fr(3, 2) == 27 and Fr(27000, 1800) == 15
    add("A tank 60 cm long, 30 cm wide and 40 cm high is full of water. %s fills 18 bottles of 1.5 ℓ each from the tank. "
        "What is the depth of the water left in the tank?" % n,
        "25 cm", ["15 cm", "22 cm", "27 cm"],
        "Water taken = 18 × 1.5 = 27 ℓ = 27" + NB + "000 cm³. Fall = 27" + NB + "000 ÷ (60 × 30) = 27" + NB +
        "000 ÷ 1800 = 15 cm. Depth left = 40 − 15 = 25 cm.")
    # 19 two cubes
    add("Cube A has edges of 6 cm. The volume of Cube B is 8 times the volume of Cube A. Find the length of an edge of Cube B.",
        "12 cm", ["48 cm", "36 cm", "14 cm"],
        "Volume of A = 6 × 6 × 6 = 216 cm³. Volume of B = 8 × 216 = 1728 cm³. 12 × 12 × 12 = 1728, so the edge is 12 cm. "
        "(8 times the volume does not mean 8 times the edge.)")
    # 20 metal cube into tank (water rises, figure)
    q = (fig(tank_svg(40, 30, 30, 18, "40 cm", "30 cm", "30 cm", "18 cm", "open tank with water 18 cm deep")) +
         "A metal cube with edges of 12 cm is put into this tank. The cube sinks to the bottom. "
         "What is the new depth of the water?")
    assert 12 ** 3 == 1728 and Fr(1728, 1200) == Fr(144, 100)
    add(q, "19.44 cm", ["1.44 cm", "30 cm", "16.56 cm"],
        "Volume of cube = 12 × 12 × 12 = 1728 cm³ (the cube is under the water, since 12 cm < 18 cm). "
        "Rise = 1728 ÷ (40 × 30) = 1728 ÷ 1200 = 1.44 cm. The water goes up, so new depth = 18 + 1.44 = 19.44 cm.")
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Volume = length × breadth × height</h2>"
        "<p><b>Volume</b> is the space inside a solid, in cubic units (cm³, m³). Count the 1-cm cubes in one layer, "
        "then multiply by the number of layers. That is the same as length × breadth × height.</p>"
        "<figure class='sn-fig'>" + cuboid_svg(6, 4, 5, "6 cm", "4 cm", "5 cm") +
        "<figcaption>Volume = 6 × 4 × 5 = 24 × 5 = 120 cm³. The base is 6 × 4 = 24 cm².</figcaption></figure>"
        "<h2>Finding a missing length</h2>"
        "<p>Work backwards. Multiply the two lengths you know, then divide the volume by that answer. "
        "If you know the area of the base, height = volume ÷ area of base.</p>" +
        ex("Example 1", "A cuboid has a volume of 1080 cm³. It is 15 cm long and 8 cm wide. Find its height.",
           "15 × 8 = 120 cm². Height = 1080 ÷ 120 = 9. Check: 15 × 8 × 9 = 1080.", "9 cm") +
        "<h2>Cubes: use the cube root ∛</h2>"
        "<p>All the edges of a cube are equal, so volume = edge × edge × edge. To find the edge, find the cube root (∛) "
        "of the volume. For a square, area = side × side, so side = √area.</p>"
        "<figure class='sn-fig'>" + cuboid_svg(7, 7, 7, "7 cm", None, None, "cube with edges of 7 cm") +
        "<figcaption>7 × 7 × 7 = 343, so a cube of 343 cm³ has edges of ∛343 = 7 cm.</figcaption></figure>" +
        table(["Edge", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
              [["Volume (edge³)", "1", "8", "27", "64", "125", "216", "343", "512", "729", "1000"],
               ["Face area (edge²)", "1", "4", "9", "16", "25", "36", "49", "64", "81", "100"]]) +
        "<h2>Water in tanks: 1 ℓ = 1000 cm³</h2>"
        "<p>The water in a tank is a cuboid too. Use the <b>depth of the water</b>, not the height of the tank. "
        "Then change cm³ to litres by dividing by 1000.</p>"
        "<figure class='sn-fig'>" + tank_svg(50, 40, 40, 30, "50 cm", "40 cm", "40 cm", "30 cm") +
        "<figcaption>Water = 50 × 40 × 30 = 60" + NB + "000 cm³ = 60 ℓ.</figcaption></figure>" +
        ex("Example 2", "12 ℓ of water is poured into this tank. How much does the water level rise?",
           "12 ℓ = 12" + NB + "000 cm³. Rise = volume ÷ area of base = 12" + NB + "000 ÷ (50 × 40) = 12" + NB +
           "000 ÷ 2000.", "6 cm") +
        "<h2>Word problems: use a model</h2>"
        "<p>When a tank is a fraction full, draw it as equal units. Find 1 unit first.</p>"
        "<figure class='sn-fig'>" + model_svg([("Tank", [(3, UNIT_FILL, "36 ℓ"), (2, WHITE, "?")], "")],
                                               "bar model of a tank in 5 units",
                                               braces=[(0, 0, 5, "full tank", "above")]) +
        "<figcaption>The tank is " + frac(3, 5) + " full with 36 ℓ. 3 units = 36 ℓ, 1 unit = 12 ℓ. "
        "It needs 2 units = 24 ℓ more.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Height = 1080 ÷ 15 (dividing by one length only)", "Divide by both: 1080 ÷ (15 × 8) = 9 cm"],
            ["Edge of a 27 cm³ cube = 27 ÷ 3 = 9 cm", "Use the cube root: 3 × 3 × 3 = 27, so 3 cm"],
            ["60" + NB + "000 cm³ = 60" + NB + "000 ℓ", "Divide by 1000: 60" + NB + "000 cm³ = 60 ℓ"],
            ["Using the height of the tank for the water", "Use the depth of the water"],
            ["Writing cm² for a volume", "Area is cm², volume is cm³"],
        ])
    )


FAQ = [
    {"q": "What is taught about volume in P6 maths?",
     "a": "Primary 6 students find a missing length, breadth or height of a cuboid from its volume, find the edge of a cube with ∛, and solve water-tank problems using 1 ℓ = 1000 cm³. These are part of Area and Volume in the MOE syllabus."},
    {"q": "How do I find the height of a cuboid from its volume?",
     "a": "Divide the volume by the area of the base (length × breadth). For 1080 cm³ with a base of 15 cm by 8 cm, the height is 1080 ÷ 120 = 9 cm."},
    {"q": "What is the most common mistake with volume of cubes?",
     "a": "Dividing the volume by 3 instead of finding the cube root. A cube of 27 cm³ has edges of 3 cm, because 3 × 3 × 3 = 27, not 27 ÷ 3 = 9 cm."},
    {"q": "Are water tank questions in the PSLE?",
     "a": "Yes. PSLE Paper 2 often has multi-step tank questions about water poured in or out and the change in water level. Students need 1 ℓ = 1000 cm³ and depth = volume ÷ area of base."},
]


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(66808)
    P = People(rnd)
    sets = [set_review(rnd), set_missing(rnd), set_roots(rnd), set_tanks(rnd), set_psle(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"]
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "volume-of-cubes-and-cuboids", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Volume of Cubes and Cuboids",
        "seo_title": "P6 Volume of Cubes and Cuboids Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE)",
        "short_title": "Volume of cubes and cuboids",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 6: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Finding one dimension, edge, height or face area of a cube or cuboid given its volume; use of √ and ∛",
        "meta_desc": "Free P6 volume worksheets: missing length, cube edge with ∛, water tanks in litres and PSLE-style problems. 100 questions with answers.",
        "key_big": "Volume = length × breadth × height, so a missing length = volume ÷ (the other two lengths).",
        "key_sub": "A cube of 343 cm³ has edges of ∛343 = 7 cm, and 1 ℓ = 1000 cm³.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(cuboid made of|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
