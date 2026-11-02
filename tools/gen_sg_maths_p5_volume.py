# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Volume of Cubes and Cuboids (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: Area and Volume)
  python3 tools/gen_sg_maths_p5_volume.py
Counting unit cubes (hidden cubes too), volume = length × breadth × height, cm³ and m³, 1 ℓ = 1000 cm³ and
1 ml = 1 cm³, and water in a rectangular tank (volume of water, how much more to fill) with bar models.
Every figure is drawn from its numbers. HTML attributes use single quotes (no backslashes in the JSON).
Numbers follow the MOE style: 4 digits with no separator, 5 or more digits grouped with a no-break space.
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
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


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


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



# ------------------------------------------------------------ solids made of unit cubes
def hm_cubes(rows):
    """rows[z][x] = height of the column (z = 0 is the front row)."""
    return [(x, y, z) for z, r in enumerate(rows) for x, h in enumerate(r) for y in range(h)]


def visible(cubes):
    k = set(cubes)
    return sum(1 for (x, y, z) in cubes if (x + 1, y, z) not in k or (x, y + 1, z) not in k or (x, y, z - 1) not in k)


def faces_seen(cubes):
    k = set(cubes)
    return sum(((x + 1, y, z) not in k) + ((x, y + 1, z) not in k) + ((x, y, z - 1) not in k) for (x, y, z) in cubes)


def bbox(cubes):
    return ((max(c[0] for c in cubes) + 1) * (max(c[1] for c in cubes) + 1) * (max(c[2] for c in cubes) + 1))


def draw_solid(cv, cubes, k, ox=0.0):
    keys = set(cubes)
    for x, y, z in sorted(cubes, key=lambda c: (-c[2], c[1], c[0])):
        p = lambda a, b, c: (ox + (x + a) * k + (z + c) * k * DZX, -(y + b) * k - (z + c) * k * DZY)
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], FILL)
        if (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], TOP)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], SIDE)


def solid_svg(cubes, label="solid made of 1-cm cubes", k=22):
    cv = Canvas()
    draw_solid(cv, cubes, k)
    return cv.svg(label)


def two_svg(A, B, label="two solids made of 1-cm cubes", k=20):
    cv = Canvas()
    ox = 0.0
    for name, cubes in (("Solid A", A), ("Solid B", B)):
        mx = max(c[0] for c in cubes) + 1
        mz = max(c[2] for c in cubes) + 1
        draw_solid(cv, cubes, k, ox)
        cv.text(ox + mx * k / 2, 16, name, 15)
        ox += max(mx * k + mz * k * DZX, tw(name, 15)) + 34
    return cv.svg(label)


# ------------------------------------------------------------ set 1: counting unit cubes
def set_count(rnd, P):
    its = []
    # cuboids built from cubes
    for i, (l, w, h) in enumerate([(4, 2, 3), (3, 3, 2), (5, 2, 2), (4, 3, 2), (2, 2, 4), (3, 3, 3)]):
        V, vis = l * w * h, visible(hm_cubes([[h] * l] * w))
        sq = l * h + l * w + w * h
        name = "cube" if l == w == h else "cuboid"
        e = ("One layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = %d. "
             "Count the hidden cubes too (only %d cubes can be seen)." % (w, l, l * w, h, l * w, h, V, vis))
        if i % 2 == 0:
            q = fig(cubes_svg(l, w, h, "cuboid made of 1-cm cubes")) + "How many 1-cm cubes make up this %s?" % name
            its.append(mcq(q, str(V), [str(x) for x in (vis, sq, l * w, l + w + h, l * w * (h - 1))], e, rnd))
        else:
            q = fig(cubes_svg(l, w, h, "cuboid made of 1-cm cubes")) + "The %s is made of 1-cm cubes. What is its volume?" % name
            its.append(mcq(q, "%d cm³" % V, ["%d cm³" % x for x in (vis, sq, l * w, l + w + h, l * w * (h - 1))], e + " Each cube is 1 cm³.", rnd))
    # irregular solids
    shapes = [[[3, 2, 1], [3, 2, 1]], [[3, 1, 1], [3, 1, 1]], [[2, 2, 2], [3, 2, 2]],
              [[1, 1, 1], [2, 2, 1], [3, 2, 1]], [[2, 2, 2, 0], [2, 2, 2, 2], [2, 2, 2, 2]], [[2, 2, 2], [3, 3, 3], [3, 3, 3]]]
    for i, rows in enumerate(shapes):
        c = hm_cubes(rows)
        V, vis = len(c), visible(c)
        cols = [h for r in rows for h in r if h]
        e = ("Add the cubes in each column: %s = %d cubes. Some cubes are hidden under or behind others "
             "(only %d can be seen)." % (" + ".join(str(h) for h in cols), V, vis))
        cands = [vis, bbox(c), faces_seen(c), len(cols)]
        if i % 2 == 0:
            q = fig(solid_svg(c)) + "How many 1-cm cubes are used to build this solid?"
            its.append(mcq(q, str(V), [str(x) for x in cands], e, rnd))
        else:
            q = fig(solid_svg(c)) + "The solid is made of 1-cm cubes. What is its volume?"
            its.append(mcq(q, "%d cm³" % V, ["%d cm³" % x for x in cands], e + " Each cube is 1 cm³.", rnd))
    # how many more cubes
    c = hm_cubes([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    assert len(c) == 18
    q = fig(solid_svg(c)) + "How many more 1-cm cubes are needed to make a cube with edges of 3 cm?"
    e = "A cube with edges of 3 cm has 3 × 3 × 3 = 27 cubes. The solid has 3 + 6 + 9 = 18 cubes. 27 − 18 = 9 more."
    its.append(mcq(q, "9", [str(27 - visible(c)), "27", "18", "6"], e, rnd))
    c = hm_cubes([[1, 1, 1], [3, 3, 1]])
    assert len(c) == 10
    q = fig(solid_svg(c)) + "How many more 1-cm cubes are needed to make a cuboid 3 cm long, 2 cm wide and 3 cm high?"
    e = "The cuboid needs 3 × 2 × 3 = 18 cubes. The solid has 3 + 7 = 10 cubes. 18 − 10 = 8 more."
    its.append(mcq(q, "8", [str(18 - visible(c)), "18", "10", "6"], e, rnd))
    c = hm_cubes([[2, 1], [2, 2]])
    assert len(c) == 7 and visible(c) == 6
    q = fig(solid_svg(c)) + "How many more 1-cm cubes are needed to make a cube with edges of 3 cm?"
    e = ("A cube with edges of 3 cm has 3 × 3 × 3 = 27 cubes. The solid has 7 cubes (one is hidden at the back). "
         "27 − 7 = 20 more. (1 more cube would only make a cube with edges of 2 cm.)")
    its.append(mcq(q, "20", ["21", "1", "27"], e, rnd))
    # compare two solids
    A, B = hm_cubes([[3, 3, 3], [3, 3, 3]]), hm_cubes([[1, 1, 1], [2, 2, 1], [2, 2, 2]])
    assert (len(A), len(B)) == (18, 14)
    q = fig(two_svg(A, B)) + "Both solids are made of 1-cm cubes. How much greater is the volume of Solid A than Solid B?"
    e = "Solid A: 3 × 2 × 3 = 18 cm³. Solid B: 3 + 5 + 6 = 14 cm³. 18 − 14 = 4 cm³. Count the hidden cubes in both."
    its.append(mcq(q, "4 cm³", ["%d cm³" % abs(visible(A) - visible(B)), "32 cm³", "4 cm²", "3 cm³"], e, rnd))
    A, B = hm_cubes([[2, 2], [2, 2], [2, 2]]), hm_cubes([[3, 2, 1]])
    assert (len(A), len(B)) == (12, 6)
    q = fig(two_svg(A, B)) + "Both solids are made of 1-cm cubes. What is their total volume?"
    e = "Solid A: 2 × 3 × 2 = 12 cm³. Solid B: 3 + 2 + 1 = 6 cm³. Total = 12 + 6 = 18 cm³."
    its.append(mcq(q, "18 cm³", ["%d cm³" % (visible(A) + visible(B)), "6 cm³", "18 cm²", "12 cm³"], e, rnd))
    # text
    q = "A cuboid is made of 1-cm cubes. Each layer has 4 rows of 6 cubes. There are 3 layers. What is its volume?"
    e = "One layer = 4 × 6 = 24 cubes. 3 layers = 24 × 3 = 72 cubes = 72 cm³."
    its.append(mcq(q, "72 cm³", ["13 cm³", "24 cm³", "72 cm²"], e, rnd))
    n, he, his = P.next()
    q = "%s fills a box with 1-cm cubes. The bottom layer has 15 cubes. The box holds 4 layers. What is the volume of the box?" % n
    e = "15 cubes in each layer × 4 layers = 60 cubes. The volume is 60 cm³."
    its.append(mcq(q, "60 cm³", ["19 cm³", "45 cm³", "60 cm²"], e, rnd))
    n, he, his = P.next()
    q = "%s builds a cube with edges of 4 cm from 1-cm cubes. How many cubes does %s use?" % (n, he)
    e = "4 × 4 = 16 cubes in each layer. There are 4 layers: 16 × 4 = 64 cubes."
    its.append(mcq(q, "64", ["12", "16", "48"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Counting unit cubes", "items": its}


# ------------------------------------------------------------ set 2: volume of cuboids and cubes
def set_volume(rnd, P):
    its = []
    seen = set()
    for i in range(8):
        while True:
            L, B, H = rnd.randint(4, 15), rnd.randint(2, 9), rnd.randint(2, 10)
            if L > B and H not in (L, B) and (L, B, H) not in seen:
                break
        seen.add((L, B, H))
        V = L * B * H
        lab = lambda v: "%d cm" % v
        q = fig(cuboid_svg(L, B, H, lab(L), lab(B), lab(H))) + "Find the volume of the cuboid."
        e = ("Volume = length × breadth × height = %d × %d × %d = %d × %d = %s cm³. Multiply the three lengths; "
             "do not add them." % (L, B, H, L * B, H, num(V)))
        pool = [q_(L * B, "cm³"), q_(L + B + H, "cm³"), q_(V, "cm²"), q_(2 * (L * B + B * H + L * H), "cm³")]
        r = i % 4
        its.append(mcq(q, q_(V, "cm³"), pool[r:] + pool[:r], e, rnd))
    for s in (4, 6, 9):
        V = s ** 3
        q = fig(cuboid_svg(s, s, s, "%d cm" % s, None, None, "cube with edges of %d cm" % s)) + \
            "This is a cube. Find its volume."
        e = "All the edges of a cube are equal: %d × %d × %d = %d × %d = %s cm³." % (s, s, s, s * s, s, num(V))
        its.append(mcq(q, q_(V, "cm³"), [q_(3 * s, "cm³"), q_(s * s, "cm³"), q_(12 * s, "cm³"), q_(V, "cm²")], e, rnd))
    for (L, B, H) in [(12, 5, 8), (20, 15, 6), (25, 10, 12), (16, 9, 5), (30, 20, 15)]:
        V = L * B * H
        q = "A cuboid is %d cm long, %d cm wide and %d cm high. What is its volume?" % (L, B, H)
        e = "Volume = %d × %d × %d = %s × %d = %s cm³." % (L, B, H, num(L * B), H, num(V))
        its.append(mcq(q, q_(V, "cm³"), [q_(L * B, "cm³"), q_(L + B + H, "cm³"), q_(V, "cm²"), q_(V * 10, "cm³")], e, rnd))
    for s in (7, 10):
        V = s ** 3
        q = "A cube has edges of %d cm. Find its volume." % s
        e = "Volume = %d × %d × %d = %d × %d = %s cm³." % (s, s, s, s * s, s, num(V))
        its.append(mcq(q, q_(V, "cm³"), [q_(3 * s, "cm³"), q_(s * s, "cm³"), q_(6 * s * s, "cm³")], e, rnd))
    q = "A cuboid has a square base with sides of 6 cm. Its height is 10 cm. Find its volume."
    e = "The base is 6 cm by 6 cm. Volume = 6 × 6 × 10 = 36 × 10 = 360 cm³."
    its.append(mcq(q, "360 cm³", ["60 cm³", "22 cm³", "240 cm³"], e, rnd))
    n, he, his = P.next()
    q = ("%s's pencil box is 14 cm long. Its breadth is half its length, and its height is 4 cm. "
         "What is the volume of the pencil box?" % n)
    e = "Breadth = 14 ÷ 2 = 7 cm. Volume = 14 × 7 × 4 = 98 × 4 = 392 cm³."
    its.append(mcq(q, "392 cm³", ["784 cm³", "25 cm³", "98 cm³"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Volume of cuboids and cubes", "items": its}


# ------------------------------------------------------------ set 3: cm³ and m³
def set_units(rnd, P):
    its = []
    U4 = ["cm³", "m³", "cm²", "m²"]
    for obj, ans in [("a dice", "cm³"), ("a classroom", "m³"), ("a box of tissues", "cm³"),
                     ("the inside of a lorry", "m³")]:
        q = "Which unit is best for measuring the volume of %s?" % obj
        e = ("Volume uses cubic units. Use cm³ for small objects you can hold and m³ for large spaces such as rooms. "
             "cm² and m² are units of area.")
        its.append(mcq(q, ans, [u for u in U4 if u != ans], e, rnd))
    q = "Which is the best estimate for the volume of an eraser?"
    e = "An eraser is about 4 cm by 2 cm by 1 cm, so about 8 cm³. 8 m³ would fill a cube 2 m wide, and cm² is for area."
    its.append(mcq(q, "8 cm³", ["8 m³", "800 cm³", "8 cm²"], e, rnd))
    q = "Which is the best estimate for the volume of a classroom?"
    e = "A classroom is about 9 m by 8 m by 3 m: 9 × 8 × 3 = 216 m³. So about 200 m³."
    its.append(mcq(q, "200 m³", ["200 cm³", "2 m³", "200 m²"], e, rnd))
    q = "Which is the best estimate for the volume of a shoebox?"
    e = "A shoebox is about 30 cm by 20 cm by 12 cm: 30 × 20 × 12 = 7200 cm³. So about 7000 cm³."
    its.append(mcq(q, "7000 cm³", ["70 cm³", "7 m³", "7000 cm²"], e, rnd))
    for (L, B, H, what) in [(5, 4, 3, "storeroom"), (6, 2, 3, "container"), (20, 15, 6, "school hall")]:
        V = L * B * H
        q = fig(cuboid_svg(L, B, H, "%d m" % L, "%d m" % B, "%d m" % H, "cuboid with lengths in metres")) + \
            "The diagram shows the shape of a %s. Find its volume." % what
        e = "Volume = %d × %d × %d = %s m³. The lengths are in metres, so the volume is in cubic metres (m³)." % (L, B, H, num(V))
        its.append(mcq(q, q_(V, "m³"), [q_(V, "m²"), q_(L + B + H, "m³"), q_(L * B, "m³")], e, rnd))
    q = "A storage box is 2.5 m long, 2 m wide and 1 m high. Find its volume."
    e = "Volume = 2.5 × 2 × 1 = 5 × 1 = 5 m³."
    assert Fr(5, 2) * 2 * 1 == 5
    its.append(mcq(q, "5 m³", ["5.5 m³", "50 m³", "5 m²"], e, rnd))
    q = "A cube has edges of 3 m. Find its volume."
    e = "Volume = 3 × 3 × 3 = 27 m³. 9 m² is the area of one face."
    its.append(mcq(q, "27 m³", ["9 m³", "27 m²", "54 m³"], e, rnd))
    q = "Which measurement is a volume?"
    e = "Volume is measured in cubic units such as m³ and cm³. m² is an area, m is a length and kg is a mass."
    its.append(mcq(q, "36 m³", ["36 m²", "36 m", "36 kg"], e, rnd))
    for (a, b) in [((10, 8, 5), (9, 7, 6)), ((12, 6, 5), (8, 8, 5)), ((15, 4, 4), (10, 6, 3))]:
        va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
        big, small = (a, b) if va > vb else (b, a)
        vB, vS = max(va, vb), min(va, vb)
        q = ("Box A is %d cm by %d cm by %d cm. Box B is %d cm by %d cm by %d cm. "
             "Which box has the greater volume, and by how much?" % (a + b))
        e = ("Box A: %d × %d × %d = %d cm³. Box B: %d × %d × %d = %d cm³. %d − %d = %d cm³."
             % (a + (va,) + b + (vb, vB, vS, vB - vS)))
        gname, sname = ("Box A", "Box B") if va > vb else ("Box B", "Box A")
        d = vB - vS
        sa, sb = sum(a), sum(b)
        bases = abs(a[0] * a[1] - b[0] * b[1])
        cands = ["%s, by %d cm³" % (sname, d), "%s, by %d cm³" % (gname, abs(sa - sb)) if sa != sb else None,
                 "%s, by %d cm³" % (gname, bases) if bases not in (0, d) else None, "%s, by %d cm²" % (gname, d),
                 "%s, by %d cm³" % (gname, vS)]
        its.append(mcq(q, "%s, by %d cm³" % (gname, d), cands, e, rnd))
    q = ("A solid is made of two cuboids. One cuboid is 6 cm by 4 cm by 3 cm. The other is 2 cm by 4 cm by 5 cm. "
         "What is the volume of the solid?")
    e = "6 × 4 × 3 = 72 cm³ and 2 × 4 × 5 = 40 cm³. Total = 72 + 40 = 112 cm³."
    its.append(mcq(q, "112 cm³", ["72 cm³", "24 cm³", "112 cm²"], e, rnd))
    n, he, his = P.next()
    q = ("%s stacks a box 30 cm by 20 cm by 10 cm on top of a box 40 cm by 30 cm by 20 cm. "
         "What is the total volume of the two boxes?" % n)
    e = "30 × 20 × 10 = 6000 cm³ and 40 × 30 × 20 = 24" + NB + "000 cm³. Total = 6000 + 24" + NB + "000 = 30" + NB + "000 cm³."
    its.append(mcq(q, "30" + NB + "000 cm³", ["24" + NB + "000 cm³", "150 cm³", "18" + NB + "000 cm³"], e, rnd))
    q = "Which box has the greatest volume?"
    opts = {"6 cm by 6 cm by 6 cm": 216, "10 cm by 10 cm by 2 cm": 200, "12 cm by 4 cm by 4 cm": 192, "20 cm by 3 cm by 3 cm": 180}
    e = ("6 × 6 × 6 = 216, 10 × 10 × 2 = 200, 12 × 4 × 4 = 192, 20 × 3 × 3 = 180 (all in cm³). "
         "The box with the longest edges is not always the biggest: multiply, do not add.")
    its.append(mcq(q, "6 cm by 6 cm by 6 cm", [k for k in opts if opts[k] != 216], e, rnd))
    q = "Which box has the smallest volume?"
    opts = {"10 cm by 2 cm by 1 cm": 20, "4 cm by 3 cm by 2 cm": 24, "3 cm by 3 cm by 3 cm": 27, "5 cm by 3 cm by 2 cm": 30}
    e = ("10 × 2 × 1 = 20, 4 × 3 × 2 = 24, 3 × 3 × 3 = 27, 5 × 3 × 2 = 30 (all in cm³). "
         "The longest box has the smallest volume: multiply, do not add.")
    its.append(mcq(q, "10 cm by 2 cm by 1 cm", [k for k in opts if opts[k] != 20], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Cubic centimetres and cubic metres", "items": its}


# ------------------------------------------------------------ set 4: litres, millilitres and cm³
def lml(cm3):
    """cm³ as '2 ℓ 450 ml' (or '3 ℓ' / '450 ml')."""
    l, m = divmod(int(cm3), 1000)
    parts = []
    if l:
        parts.append("%s ℓ" % num(l))
    if m:
        parts.append("%d ml" % m)
    return " ".join(parts)


def set_litres(rnd, P):
    its = []
    for l in (3, 7, 12):
        q = "%d ℓ = ? cm³" % l
        e = "1 ℓ = 1000 cm³, so %d ℓ = %d × 1000 = %s cm³." % (l, l, num(l * 1000))
        its.append(mcq(q, q_(l * 1000, "cm³"), [q_(l * 100, "cm³"), q_(l * 10, "cm³"), q_(l, "cm³")], e, rnd))
    for m in (250, 600):
        q = "%d ml = ? cm³" % m
        e = "1 ml = 1 cm³, so %d ml = %d cm³. Do not multiply or divide by 1000." % (m, m)
        its.append(mcq(q, q_(m, "cm³"), [q_(m * 1000, "cm³"), q_(Fr(m, 1000), "cm³"), q_(m * 10, "cm³")], e, rnd))
    for c in (5000, 8000, 20000):
        q = "%s cm³ = ? ℓ" % num(c)
        e = "1000 cm³ = 1 ℓ, so divide by 1000: %s ÷ 1000 = %s ℓ." % (num(c), num(c // 1000))
        its.append(mcq(q, q_(c // 1000, "ℓ"), [q_(c // 100, "ℓ"), q_(c // 10, "ℓ"), q_(c, "ℓ")], e, rnd))
    for c, wrong in [(2450, ["24 ℓ 50 ml", "2 ℓ 45 ml", "245 ℓ"]), (3080, ["3 ℓ 800 ml", "30 ℓ 80 ml", "3 ℓ 8 ml"]),
                     (1605, ["16 ℓ 5 ml", "1 ℓ 65 ml", "1 ℓ 6 ml"])]:
        q = "Write %d cm³ in litres and millilitres." % c
        e = "%d cm³ = %d ml = %d ml + %d ml = %s. The thousands are the litres." % (c, c, c // 1000 * 1000, c % 1000, lml(c))
        its.append(mcq(q, lml(c), wrong, e, rnd))
    q = "1 ℓ 80 ml = ? cm³"
    e = "1 ℓ = 1000 ml. 1000 ml + 80 ml = 1080 ml = 1080 cm³. (80 ml is not 800 ml.)"
    its.append(mcq(q, "1080 cm³", ["1800 cm³", "180 cm³", "81 cm³"], e, rnd))
    q = "4 ℓ 250 ml = ? cm³"
    e = "4 ℓ = 4000 ml. 4000 ml + 250 ml = 4250 ml = 4250 cm³."
    its.append(mcq(q, "4250 cm³", ["4025 cm³", "650 cm³", "425 cm³"], e, rnd))
    for i, (L, B, H) in enumerate([(20, 10, 15), (25, 20, 10), (30, 20, 25), (40, 25, 20)]):
        V = L * B * H
        c = V // 1000
        if i < 2:
            q = (fig(cuboid_svg(L, B, H, "%d cm" % L, "%d cm" % B, "%d cm" % H, "box-shaped container")) +
                 "How many litres of water can this container hold when full?")
        else:
            q = "A container is %d cm long, %d cm wide and %d cm high. What is its capacity in litres?" % (L, B, H)
        e = "Volume = %d × %d × %d = %s cm³. 1000 cm³ = 1 ℓ, so %s ÷ 1000 = %d ℓ." % (L, B, H, num(V), num(V), c)
        its.append(mcq(q, q_(c, "ℓ"), [q_(c * 10, "ℓ"), q_(V, "ℓ"), q_(c * 100, "ℓ")], e, rnd))
    for (L, B, H, wrong) in [(15, 12, 20, ["36 ℓ", "3 ℓ 60 ml", "360 ℓ"]), (18, 10, 15, ["27 ℓ", "2 ℓ 70 ml", "270 ℓ"])]:
        V = L * B * H
        q = "A carton is %d cm long, %d cm wide and %d cm high. What is its capacity in litres and millilitres?" % (L, B, H)
        e = "Volume = %d × %d × %d = %d cm³ = %d ml = %s." % (L, B, H, V, V, lml(V))
        its.append(mcq(q, lml(V), wrong, e, rnd))
    q = "Which is equal to 1 ℓ 50 ml?"
    e = "1 ℓ 50 ml = 1000 ml + 50 ml = 1050 ml = 1050 cm³. 1500 cm³ would be 1 ℓ 500 ml."
    its.append(mcq(q, "1050 cm³", ["1500 cm³", "150 cm³", "1005 cm³"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Litres, millilitres and cm³", "items": its}


# ------------------------------------------------------------ set 5: water in a rectangular tank
def L_(cm3):
    return Fr(cm3, 1000)


def set_tanks(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    def T(L, B, H, d, label="open tank with water in it"):
        return fig(tank_svg(L, B, H, d, "%d cm" % L, "%d cm" % B, "%d cm" % H, "%s cm" % num(d), label))

    for (L, B, H, d) in [(40, 30, 35, 20), (60, 40, 50, 35), (50, 25, 40, 28)]:
        V = L * B * d
        full, empty = L_(L * B * H), L_(L * B * (H - d))
        q = T(L, B, H, d) + "The water in the tank is %d cm deep. How many litres of water are in the tank?" % d
        e = ("Use the depth of the water, not the height of the tank: %d × %d × %d = %s cm³ = %s ℓ."
             % (L, B, d, num(V), num(L_(V))))
        add(q, q_(L_(V), "ℓ"), [q_(full, "ℓ"), q_(empty, "ℓ"), q_(L_(V) * 10, "ℓ")], e)
    for (L, B, H, d) in [(50, 40, 60, 35), (40, 30, 45, 25), (60, 30, 40, 15)]:
        V = L * B * (H - d)
        q = T(L, B, H, d) + "How many more litres of water are needed to fill the tank to the brim?"
        e = ("The empty part is %d − %d = %d cm high. %d × %d × %d = %s cm³ = %s ℓ."
             % (H, d, H - d, L, B, H - d, num(V), num(L_(V))))
        add(q, q_(L_(V), "ℓ"), [q_(L_(L * B * H), "ℓ"), q_(L_(L * B * d), "ℓ"), q_(L_(V) * 10, "ℓ")], e)
    q = ("A tank 40 cm long, 40 cm wide and 50 cm high contains 32 ℓ of water. How many more litres of water are "
         "needed to fill it completely?")
    assert 40 * 40 * 50 == 80000
    e = "Capacity = 40 × 40 × 50 = 80" + NB + "000 cm³ = 80 ℓ. More water needed = 80 − 32 = 48 ℓ."
    add(q, "48 ℓ", ["80 ℓ", "112 ℓ", "52 ℓ"], e)
    q = ("A tank is 50 cm long, 30 cm wide and 40 cm high. It contains 27 ℓ 500 ml of water. How much more water "
         "is needed to fill it?")
    assert 50 * 30 * 40 == 60000 and 60000 - 27500 == 32500
    e = "Capacity = 50 × 30 × 40 = 60" + NB + "000 cm³ = 60 ℓ. 60 ℓ − 27 ℓ 500 ml = 32 ℓ 500 ml."
    add(q, "32 ℓ 500 ml", ["33 ℓ 500 ml", "87 ℓ 500 ml", "60 ℓ"], e)
    q = "A tank is 60 cm long, 50 cm wide and 40 cm high. It is " + frac(3, 4) + " full of water. How many litres of water are in it?"
    e = "Capacity = 60 × 50 × 40 = 120" + NB + "000 cm³ = 120 ℓ. " + frac(3, 4) + " of 120 ℓ = 120 ÷ 4 × 3 = 90 ℓ."
    add(q, "90 ℓ", ["120 ℓ", "30 ℓ", "900 ℓ"], e)
    q = "A tank is 50 cm long, 40 cm wide and 30 cm high. It is " + frac(2, 3) + " full of water. How many litres of water are in it?"
    e = "Capacity = 50 × 40 × 30 = 60" + NB + "000 cm³ = 60 ℓ. " + frac(2, 3) + " of 60 ℓ = 60 ÷ 3 × 2 = 40 ℓ."
    add(q, "40 ℓ", ["20 ℓ", "60 ℓ", "400 ℓ"], e)
    # bar models
    svg = model_svg([("Tank", [(2, UNIT_FILL, "24 ℓ"), (3, WHITE, "?")], "")], "bar model of a tank in 5 units",
                    braces=[(0, 0, 5, "full tank", "above")])
    add(fig(svg) + "Mrs Lim's fish tank is " + frac(2, 5) + " full. It has 24 ℓ of water in it. "
        "How many more litres of water are needed to fill the tank?",
        "36 ℓ", ["60 ℓ", "12 ℓ", "16 ℓ"],
        "2 units = 24 ℓ, so 1 unit = 12 ℓ. The empty part is 3 units = 3 × 12 = 36 ℓ. (The full tank is 5 units = 60 ℓ.)")
    svg = model_svg([("Before", [(1, UNIT_FILL, ""), (3, WHITE, "")], ""),
                     ("After", [(1, UNIT_FILL, ""), (2, UNIT_FILL2, "30 ℓ"), (1, WHITE, "")], "")],
                    "bar model of a tank before and after", braces=[(0, 0, 4, "capacity = ?", "above")], unit=46)
    add(fig(svg) + "A tank is " + frac(1, 4) + " full of water. After 30 ℓ of water is added, it is " +
        frac(3, 4) + " full. What is the capacity of the tank?",
        "60 ℓ", ["40 ℓ", "120 ℓ", "45 ℓ"],
        "The 30 ℓ fills " + frac(3, 4) + " − " + frac(1, 4) + " = " + frac(2, 4) + " of the tank. "
        "2 units = 30 ℓ, so 1 unit = 15 ℓ. Capacity = 4 units = 4 × 15 = 60 ℓ.")
    svg = model_svg([("Tank A", [(1, UNIT_FILL, ""), (1, UNIT_FILL, ""), (1, UNIT_FILL, "")], ""),
                     ("Tank B", [(1, UNIT_FILL2, "")], "")], "bar model comparing water in two tanks",
                    braces=[(0, 0, 3, "?", "above")])
    add(fig(svg) + "Tank A has 3 times as much water as Tank B. Together they hold 48 ℓ of water. "
        "How much water is in Tank A?",
        "36 ℓ", ["12 ℓ", "16 ℓ", "24 ℓ"],
        "4 units = 48 ℓ, so 1 unit = 48 ÷ 4 = 12 ℓ. Tank A = 3 units = 3 × 12 = 36 ℓ. (16 ℓ is 48 ÷ 3.)")
    svg = model_svg([("Tank P", [(3, UNIT_FILL, ""), (1, UNIT_FILL2, "15 ℓ")], ""),
                     ("Tank Q", [(3, UNIT_FILL, "?")], "")], "bar model of two tanks with a difference",
                    braces=[], unit=40)
    add(fig(svg) + "Tank P has 15 ℓ more water than Tank Q. Together they hold 75 ℓ of water. "
        "How much water is in Tank Q?",
        "30 ℓ", ["45 ℓ", "60 ℓ", "37.5 ℓ"],
        "Take away the extra 15 ℓ: 75 − 15 = 60 ℓ. This is 2 equal parts, so Tank Q = 60 ÷ 2 = 30 ℓ. "
        "Tank P = 30 + 15 = 45 ℓ.")
    # rate
    assert 60 * 40 * 50 == 120000 and Fr(120, 8) == 15
    add("An empty tank is 60 cm long, 40 cm wide and 50 cm high. A tap fills it at 8 ℓ per minute. "
        "How long does it take to fill the tank?",
        "15 min", ["150 min", "960 min", "120 min"],
        "Capacity = 60 × 40 × 50 = 120" + NB + "000 cm³ = 120 ℓ. Time = 120 ÷ 8 = 15 min.")
    assert 50 * 40 * (45 - 15) == 60000 and Fr(60, 6) == 10
    add("A tank 50 cm long, 40 cm wide and 45 cm high has water 15 cm deep. Water flows in from a tap at 6 ℓ per minute. "
        "How long will it take to fill the tank to the brim?",
        "10 min", ["15 min", "5 min", "100 min"],
        "The empty part is 45 − 15 = 30 cm high: 50 × 40 × 30 = 60" + NB + "000 cm³ = 60 ℓ. "
        "Time = 60 ÷ 6 = 10 min. (15 min would fill the whole tank of 90 ℓ.)")
    n, he, his = P.next()
    assert 40 * 30 * 25 == 30000 and 30000 // 750 == 40
    add("A tank 40 cm long, 30 cm wide and 25 cm high is full of water. %s pours all the water into bottles. "
        "Each bottle holds 750 ml. How many bottles can %s fill?" % (n, he),
        "40", ["4", "400", "30"],
        "Water = 40 × 30 × 25 = 30" + NB + "000 cm³ = 30" + NB + "000 ml. Bottles = 30" + NB + "000 ÷ 750 = 40.")
    assert 50 * 40 * 60 == 120000 and Fr(40, 100) * 120 == 48
    add("The school's water tank is 50 cm long, 40 cm wide and 60 cm high. It is 40% full. "
        "How many litres of water are in it?",
        "48 ℓ", ["72 ℓ", "3 ℓ", "480 ℓ"],
        "Capacity = 50 × 40 × 60 = 120" + NB + "000 cm³ = 120 ℓ. 40% of 120 ℓ = 120 ÷ 100 × 40 = 48 ℓ.")
    n, he, his = P.next()
    assert 24 * 15 * 13 == 4680
    add("%s's fish tank is 24 cm long, 15 cm wide and 20 cm high. The water in it is 13 cm deep. "
        "What is the volume of the water in litres and millilitres?" % n,
        "4 ℓ 680 ml", ["46 ℓ 80 ml", "7 ℓ 200 ml", "468 ℓ"],
        "Water = 24 × 15 × 13 = 360 × 13 = 4680 cm³ = 4680 ml = 4 ℓ 680 ml. Use the depth (13 cm), not the height.")
    assert 60 * 40 * 30 == 72000 and 72000 - 3 * 8500 == 46500
    add("Mr Tan's tank is 60 cm long, 40 cm wide and 30 cm high. It is full of water. He fills 3 pails with water "
        "from the tank. Each pail holds 8 ℓ 500 ml. How much water is left in the tank?",
        "46 ℓ 500 ml", ["63 ℓ 500 ml", "25 ℓ 500 ml", "47 ℓ 500 ml"],
        "Capacity = 60 × 40 × 30 = 72" + NB + "000 cm³ = 72 ℓ. Water used = 3 × 8 ℓ 500 ml = 25 ℓ 500 ml. "
        "72 ℓ − 25 ℓ 500 ml = 46 ℓ 500 ml.")
    assert len(its) == 20, len(its)
    return {"title": "Water in a rectangular tank", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>Volume is the number of unit cubes</h2>"
        "<p><b>Volume</b> is the amount of space a solid takes up. A 1-cm cube has a volume of 1 cubic centimetre (1 cm³). "
        "Count the cubes in one layer, then multiply by the number of layers. Remember the hidden cubes.</p>"
        "<figure class='sn-fig'>" + cubes_svg(4, 2, 3, "cuboid made of 1-cm cubes") +
        "<figcaption>One layer: 2 rows of 4 = 8 cubes. 3 layers: 8 × 3 = 24 cubes = 24 cm³. "
        "Only 18 cubes can be seen.</figcaption></figure>"
        "<h2>Volume = length × breadth × height</h2>"
        "<p>For a cuboid, multiply the three lengths. A cube has equal edges, so multiply the edge by itself three times. "
        "Write the answer in cubic units: cm³ for small objects, m³ for large spaces such as rooms.</p>"
        "<figure class='sn-fig'>" + cuboid_svg(6, 4, 5, "6 cm", "4 cm", "5 cm") +
        "<figcaption>Volume = 6 × 4 × 5 = 24 × 5 = 120 cm³.</figcaption></figure>" +
        ex("Example 1", "A cube has edges of 5 cm. Find its volume.", "5 × 5 × 5 = 25 × 5 = 125.", "125 cm³") +
        "<h2>Litres and cubic centimetres</h2>"
        "<p>1 ℓ = 1000 cm³ and 1 ml = 1 cm³. To change cm³ to litres, divide by 1000.</p>" +
        table(["Volume", "Same as"], [["1 ml", "1 cm³"], ["250 ml", "250 cm³"], ["1 ℓ", "1000 cm³"],
                                      ["2 ℓ 450 ml", "2450 cm³"], ["30" + NB + "000 cm³", "30 ℓ"]]) +
        "<h2>Water in a rectangular tank</h2>"
        "<p>The water in a tank is a cuboid too. Use the <b>depth of the water</b>, not the height of the tank. "
        "The empty part above the water tells you how much more is needed to fill the tank.</p>"
        "<figure class='sn-fig'>" + tank_svg(50, 40, 40, 30, "50 cm", "40 cm", "40 cm", "30 cm") +
        "<figcaption>Water = 50 × 40 × 30 = 60" + NB + "000 cm³ = 60 ℓ.</figcaption></figure>" +
        ex("Example 2", "How many more litres of water are needed to fill this tank to the brim?",
           "Empty part: 40 − 30 = 10 cm high. 50 × 40 × 10 = 20" + NB + "000 cm³ = 20 ℓ.", "20 ℓ") +
        "<h2>Word problems: use a model</h2>"
        "<p>When a tank is a fraction full, draw the tank as equal units. Find 1 unit first.</p>"
        "<figure class='sn-fig'>" + model_svg([("Tank", [(2, UNIT_FILL, "24 ℓ"), (3, WHITE, "?")], "")],
                                               "bar model of a tank in 5 units",
                                               braces=[(0, 0, 5, "full tank", "above")]) +
        "<figcaption>The tank is " + frac(2, 5) + " full with 24 ℓ. 2 units = 24 ℓ, 1 unit = 12 ℓ. "
        "It needs 3 units = 36 ℓ more.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting only the cubes you can see", "Count layer by layer, including hidden cubes"],
            ["Adding the edges: 6 + 4 + 5 = 15", "Multiply: 6 × 4 × 5 = 120 cm³"],
            ["Writing cm² for a volume", "Area is cm², volume is cm³"],
            ["1 ℓ = 100 cm³", "1 ℓ = 1000 cm³, and 1 ml = 1 cm³"],
            ["Using the height of the tank for the water", "Use the depth of the water"],
        ])
    )


FAQ = [
    {"q": "What is taught about volume in P5 maths?",
     "a": "Primary 5 students find the volume of solids made of unit cubes, find the volume of cubes and cuboids in cm³ and m³, and use 1 ℓ = 1000 cm³ to find the volume of water in a rectangular tank."},
    {"q": "How do I explain volume to my child?",
     "a": "Build a cuboid with small cubes and count them layer by layer. Then show that length × breadth × height gives the same number, for example 4 × 2 × 3 = 24 cm³."},
    {"q": "What is the most common mistake with volume?",
     "a": "Counting only the cubes that can be seen, or adding the length, breadth and height instead of multiplying them. Another is thinking that 1 ℓ = 100 cm³; it is 1000 cm³."},
    {"q": "Is volume in the MOE syllabus for Primary 5?",
     "a": "Yes. Volume of cubes and cuboids, cm³ and m³, and water in rectangular tanks are part of Area and Volume in the MOE Primary 5 syllabus. In Primary 6 students go on to find a missing length from the volume."},
]


def gen():
    rnd = random.Random(65812)
    P = People(rnd)
    sets = [set_count(rnd, P), set_volume(rnd, P), set_units(rnd, P), set_litres(rnd, P), set_tanks(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] if "<svg" in it["q"] else re.sub(r"<[^>]+>", "", it["q"])
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "volume-of-cubes-and-cuboids", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Volume of Cubes and Cuboids",
        "seo_title": "P5 Volume of Cubes and Cuboids Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Volume of cubes and cuboids",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 5: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Volume of cubes and cuboids; measuring volume in cubic units, cm³/m³; finding the volume of liquid in a rectangular tank; relationship between ℓ (or ml) with cm³",
        "meta_desc": "Free P5 volume worksheets: count unit cubes, length × breadth × height, cm³ and m³, 1 ℓ = 1000 cm³ and water in tanks. 100 questions with answers.",
        "key_big": "Volume = length × breadth × height, in cubic units such as cm³ and m³.",
        "key_sub": "A box 6 cm by 4 cm by 5 cm has a volume of 6 × 4 × 5 = 120 cm³, and 1 ℓ = 1000 cm³.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(cuboid made of|solid made of|two solids|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
