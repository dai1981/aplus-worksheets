# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Area, Perimeter and Volume (National Curriculum in England, Year 6 Measurement)
  python3 tools/gen_uk_maths_y6_area_volume.py
Rectangles and compound (rectilinear) shapes, same area / different perimeter, triangles (½ × b × h),
parallelograms (b × h), cubes and cuboids (l × w × h, cm³, m³, mm³), SATs-style word problems.
Every figure is drawn to scale from its numbers. Perpendicular heights are red dashed lines with a right-angle mark;
slanted sides carry their true lengths (whole-number triangles), so they work as distractors.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#f6dcb4"
TOP, SIDE = "#e6f2e9", "#a9d3b6"
WHITE = "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
AREA_U = [("cm", "cm²"), ("m", "m²"), ("mm", "mm²"), ("cm", "cm²")]
VOL_U = [("cm", "cm³", "cm²"), ("m", "m³", "m²"), ("mm", "mm³", "mm²")]
HALF = "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"
DZX, DZY = 0.55, 0.40          # oblique view: one unit of depth goes this far right and up


# ------------------------------------------------------------ helpers
def num(x):
    """Exact number as text: 1050 -> 1,050; 45/2 -> 22.5 (only terminating decimals)."""
    x = Fr(x)
    if x.denominator == 1:
        return "{:,}".format(x.numerator)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    assert d == 1, x
    s = format(Decimal(x.numerator) / Decimal(x.denominator), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, fpart = s.partition(".")
    return "{:,}".format(int(i)) + ("." + fpart if fpart else "")


def ar(x, unit):
    return "%s %s" % (num(x), unit)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers, never equal in value)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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
    """Approximate width of bold Arial text in px. Commas, full stops and spaces are narrow."""
    t = str(t)
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - t.count(" ") * 0.3) * fs * 0.6


def must(svg):
    assert svg, "figure did not fit"
    return svg


# ------------------------------------------------------------ 2-D drawing engine (labels never touch lines)
FS = 16
HH = 10


def seg_hits_box(p, q, b):
    x0, y0, x1, y1 = b
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def render(polys, label, lines=(), rights=(), labels=(), maxw=200, maxh=110, mirror=False, flip=False, letters=()):
    """Draw to scale. Coordinates in the problem's units, y up.
    polys  = [(points, fill)]; lines = [(p, q, style)] 'h' height (red dashed), 's' split (red dashed), 'x' grey dashed
    rights = [(F, A, B)] right-angle mark at F; labels = [(p, q, text, mode)] (mode: polygon -> outside it, 'up'.. or None)
    letters = [(point, text)] big green letters (A, B) placed at a point.
    Returns None when the labels cannot be placed without touching a line."""
    def T(p):
        return ((-p[0] if mirror else p[0]), (-p[1] if flip else p[1]))
    allp = [T(p) for pts, _ in polys for p in pts] + [T(p) for a, b, _ in lines for p in (a, b)]
    x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
    y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)
    k = min(maxw / (x1 - x0), maxh / (y1 - y0))

    def P(p):
        p = T(p)
        return ((p[0] - x0) * k, (y1 - p[1]) * k)
    segs, pp = [], []
    for pts, fill in polys:
        q = [P(p) for p in pts]
        pp.append((q, fill))
        segs += [(q[i], q[(i + 1) % len(q)]) for i in range(len(q))]
    ll = []
    for a, b, st in lines:
        a, b = P(a), P(b)
        ll.append((a, b, st))
        segs.append((a, b))
    marks = []
    for F, A, B in rights:
        F, A, B = P(F), P(A), P(B)
        u = ((A[0] - F[0]), (A[1] - F[1]))
        v = ((B[0] - F[0]), (B[1] - F[1]))
        lu, lv = math.hypot(*u), math.hypot(*v)
        s = 9
        a = (F[0] + u[0] / lu * s, F[1] + u[1] / lu * s)
        c = (F[0] + v[0] / lv * s, F[1] + v[1] / lv * s)
        m = (a[0] + c[0] - F[0], a[1] + c[1] - F[1])
        marks.append((a, m, c))
        segs += [(a, m), (m, c)]

    def clash(bx, boxes):
        for B in boxes:
            if bx[0] < B[2] + 8 and B[0] < bx[2] + 8 and bx[1] < B[3] + 5 and B[1] < bx[3] + 5:
                return True
        e = (bx[0] - 4, bx[1] - 3, bx[2] + 4, bx[3] + 3)
        return any(seg_hits_box(a, b, e) for a, b in segs)

    boxes, texts = [], []
    for pt0, t in letters:
        cx, cy = P(pt0)
        bx = (cx - 7, cy - 11, cx + 7, cy + 11)
        if clash(bx, boxes):
            return None
        boxes.append(bx)
        texts.append((cx, cy, t, 20, GREEN))
    for a, b, t, mode in labels:
        a, b = P(a), P(b)
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        n1 = (dy / L, -dx / L)
        if isinstance(mode, str):
            d = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[mode]
            d = (-d[0] if mirror else d[0], d[1] if flip else -d[1])
            sides = [n1 if n1[0] * d[0] + n1[1] * d[1] > 0 else (-n1[0], -n1[1])]
        elif mode is not None:
            poly = [P(p) for p in mode]
            mx, my = (a[0] + b[0]) / 2 + n1[0] * 2, (a[1] + b[1]) / 2 + n1[1] * 2
            sides = [(-n1[0], -n1[1]) if inside(poly, mx, my) else n1]
        else:
            sides = [n1, (-n1[0], -n1[1])]
        hw = tw(t, FS) / 2
        done = False
        for fr in (0.5, 0.4, 0.6, 0.3, 0.7, 0.22, 0.78, 0.15, 0.85):
            for nx, ny in sides:
                off = 6 + abs(nx) * hw + abs(ny) * HH
                cx, cy = a[0] + dx * fr + nx * off, a[1] + dy * fr + ny * off
                bx = (cx - hw, cy - HH, cx + hw, cy + HH)
                if not clash(bx, boxes):
                    done = True
                    break
            if done:
                break
        if not done:
            return None
        boxes.append(bx)
        texts.append((cx, cy, t, FS, RED if "?" in t else INK))
    xs = [p[0] for q, _ in pp for p in q] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for q, _ in pp for p in q] + [b[1] for b in boxes] + [b[3] for b in boxes]
    xs += [p[0] for a, b, _ in ll for p in (a, b)]
    ys += [p[1] for a, b, _ in ll for p in (a, b)]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    if W == H:
        W += 1

    def pt(p):
        return "%.1f,%.1f" % (p[0] - ox, p[1] - oy)
    s = []
    for q, fill in pp:
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                 % (" ".join(pt(p) for p in q), fill, GREEN))
    for a, b, st in ll:
        col, wdt, da = (GREY, 2, "5 4") if st == "x" else (RED, 2.5, "7 5")
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s' stroke-dasharray='%s'/>"
                 % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, wdt, da))
    for a, m, c in marks:
        s.append("<polyline points='%s %s %s' fill='none' stroke='%s' stroke-width='1.8'/>" % (pt(a), pt(m), pt(c), INK))
    for cx, cy, t, fs, col in texts:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx - ox, cy - oy + fs * 0.36, fs, col, t))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ 2-D shapes
def rect_svg(L, W, u, label="rectangle with its length and width", maxw=190, maxh=95):
    pts = [(0, 0), (L, 0), (L, W), (0, W)]
    return render([(pts, FILL)], label, labels=[((0, 0), (L, 0), ar(L, u), pts), ((0, W), (0, 0), ar(W, u), pts)],
                  maxw=maxw, maxh=maxh)


def two_rects_svg(r1, r2, u):
    """Rectangles A and B side by side, drawn to the same scale."""
    (a1, b1), (a2, b2) = r1, r2
    gap = max(a1, a2) * 0.55 + 2
    p1 = [(0, 0), (a1, 0), (a1, b1), (0, b1)]
    p2 = [(a1 + gap, 0), (a1 + gap + a2, 0), (a1 + gap + a2, b2), (a1 + gap, b2)]
    labels = [((0, 0), (a1, 0), ar(a1, u), p1), ((0, b1), (0, 0), ar(b1, u), p1),
              (p2[0], p2[1], ar(a2, u), p2), (p2[3], p2[0], ar(b2, u), p2)]
    letters = [((a1 / 2, b1 / 2), "A"), ((a1 + gap + a2 / 2, b2 / 2), "B")]
    return render([(p1, FILL), (p2, FILL2)], "two rectangles A and B", labels=labels, letters=letters, maxw=280, maxh=90)


def l_pts(Wt, Ht, cw, ch, corner):
    """L-shape: a Wt by Ht rectangle with a cw by ch piece cut from one corner (y up).
    Sides in order: [Wt - cw, ch, cw, Ht - ch, Wt, Ht]."""
    p = [(0, Ht), (Wt - cw, Ht), (Wt - cw, Ht - ch), (Wt, Ht - ch), (Wt, 0), (0, 0)]
    if corner in ("tl", "bl"):
        p = [(Wt - x, y) for x, y in p]
    if corner in ("br", "bl"):
        p = [(x, Ht - y) for x, y in p]
    return p


CL = "compound rectilinear shape"


def l_svg(Wt, Ht, cw, ch, corner, labels, split):
    pts = l_pts(Wt, Ht, cw, ch, corner)
    lab = [(pts[i], pts[(i + 1) % 6], t, pts) for i, t in enumerate(labels) if t]
    lines = []
    if split:
        x = pts[1][0]
        y = pts[2][1]
        lines.append(((x, y), (x, 0 if corner in ("tr", "tl") else Ht), "s"))
    return render([(pts, FILL)], CL + " (L-shape)", lines, labels=lab, maxw=230, maxh=120)


def right_tri_svg(a, b, la, lb, lc, orient_i, label="right-angled triangle"):
    pts = [(0, 0), (a, 0), (0, b)]
    labels = [((0, 0), (a, 0), la, pts), ((0, b), (0, 0), lb, pts)]
    if lc:
        labels.append(((a, 0), (0, b), lc, pts))
    return render([(pts, FILL)], label, rights=[((0, 0), (a, 0), (0, b))], labels=labels,
                  mirror=orient_i in (1, 2), flip=orient_i in (2, 3), maxw=170, maxh=105)


def tri_svg(b, p, h, lb, lh, slant, mirror=False, flip=False, label="triangle with its perpendicular height"):
    """Base (0,0)-(b,0), top vertex (p,h). The height is dashed; outside the base the base line is extended in grey."""
    pts = [(0, 0), (b, 0), (p, h)]
    lines, rights = [], []
    if 0 < p < b:
        rights.append(((p, 0), (b, 0), (p, h)))
    elif p > b:
        lines.append(((b, 0), (p, 0), "x"))
        rights.append(((p, 0), (b, 0), (p, h)))
    elif p < 0:
        lines.append(((p, 0), (0, 0), "x"))
        rights.append(((p, 0), (0, 0), (p, h)))
    lines.append(((p, h), (p, 0), "h"))
    labels = [((0, 0), (b, 0), lb, pts), ((p, h), (p, 0), lh, None)]
    if slant:
        t, side = slant
        labels.append((((0, 0), (p, h), t, pts) if side == "L" else ((b, 0), (p, h), t, pts)))
    return render([(pts, FILL)], label, lines, rights, labels, mirror=mirror, flip=flip, maxw=200, maxh=115)


def para_svg(b, o, h, lb, lh, ls, mirror=False, label="parallelogram with its perpendicular height"):
    pts = [(0, 0), (b, 0), (b + o, h), (o, h)]
    return render([(pts, FILL)], label, lines=[((o, h), (o, 0), "h")], rights=[((o, 0), (b, 0), (o, h))],
                  labels=[((0, 0), (b, 0), lb, pts), ((o, h), (o, 0), lh, None)] + ([((0, 0), (o, h), ls, pts)] if ls else []),
                  mirror=mirror, maxw=200, maxh=100)


TRIPLES = sorted({(d, h, int(math.isqrt(d * d + h * h))) for d in range(1, 41) for h in range(1, 41)
                  if math.isqrt(d * d + h * h) ** 2 == d * d + h * h})


def hx(b, h):
    return "%s × %s × %s = %s × %s" % (HALF, num(b), num(h), HALF, num(b * h))


# ------------------------------------------------------------ 3-D drawing (cuboids)
class Canvas:
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

    def line(self, a, b, dashed=False, sw=2.4):
        self.el.append(("l", a, b, dashed, sw))
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

    def svg(self, label, pad=5):
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
                a, b = e[1], e[2]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, GREEN, 1.6 if e[3] else e[4],
                            " stroke-dasharray='5 4'" if e[3] else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H, "".join(s), label)


def proj(X, Y, Z, k):
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def cubes_svg(l, w, h, label="cuboid made of centimetre cubes", k=22, gap=0.0):
    """Every 1 cm cube is drawn, back to front, so the hidden cubes really are there."""
    cubes = [(i, j, m) for i in range(l) for j in range(h) for m in range(w)]
    keys = set(cubes)
    assert len(keys) == l * w * h
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


def cuboid_svg(L, W, H, lab_l, lab_w, lab_h, label="cuboid with its length, width and height"):
    m = max(L, W, H)
    dL, dW, dH = (max(float(v), m / 3.2) for v in (L, W, H))
    k = min(165 / (dL + dW * DZX), 100 / (dH + dW * DZY), 26)
    cv = Canvas()
    p = lambda a, b, c: proj(a, b, c, k)
    cv.poly([p(0, 0, 0), p(dL, 0, 0), p(dL, dH, 0), p(0, dH, 0)], FILL, 2.4)
    cv.poly([p(0, dH, 0), p(dL, dH, 0), p(dL, dH, dW), p(0, dH, dW)], TOP, 2.4)
    cv.poly([p(dL, 0, 0), p(dL, 0, dW), p(dL, dH, dW), p(dL, dH, 0)], SIDE, 2.4)
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


# ------------------------------------------------------------ set 1: rectangles, compound shapes, same area
def set_rect(rnd):
    its = []
    used = set()
    # rectangles
    for i, (L, W, u) in enumerate([(9, 6, "cm"), (14, 5, "m"), (12, 8, "cm"), (15, 7, "m")]):
        su = u + "²"
        A, Pm = L * W, 2 * (L + W)
        q = fig(must(rect_svg(L, W, u))) + "What is the area of the rectangle?"
        e = ("Area = length × width = %d × %d = %d %s. Adding the sides gives the perimeter (%d %s), not the area."
             % (L, W, A, su, Pm, u))
        its.append(mcq(q, ar(A, su), [ar(Pm, su), ar(A, u), ar(L + W, su)], e, rnd))
    # compound L-shapes: area
    corners = ["tr", "tl", "br", "bl"]
    for i, kind in enumerate(["split", "split", "cut", "cut", "hidden", "hidden"]):
        u = ["cm", "m"][i % 2]
        su = u + "²"
        while True:
            Wt, Ht = rnd.randint(9, 16), rnd.randint(6, 12)
            if Wt <= Ht or Wt / Ht > 2:
                continue
            cw = rnd.randint(int(math.ceil(Wt * 0.4)), int(Wt * 0.6))
            ch = rnd.randint(int(math.ceil(Ht * 0.4)), int(Ht * 0.6))
            if cw == Wt - cw or ch == Ht - ch or (Wt, Ht, cw, ch) in used:
                continue
            sides = [Wt - cw, ch, cw, Ht - ch, Wt, Ht]
            labels = ["%d %s" % (v, u) for v in sides]
            if kind == "hidden":
                labels[1] = labels[2] = ""
            svg = l_svg(Wt, Ht, cw, ch, corners[i % 4], labels, kind == "split")
            if svg:
                break
        used.add((Wt, Ht, cw, ch))
        A = Wt * Ht - cw * ch
        A1, A2 = (Wt - cw) * Ht, cw * (Ht - ch)
        split_e = ("Split it into two rectangles: %d × %d = %d and %d × %d = %d. Add: %d + %d = %d %s."
                   % (Wt - cw, Ht, A1, cw, Ht - ch, A2, A1, A2, A, su))
        cut_e = ("Whole rectangle %d × %d = %d, take away the missing corner %d × %d = %d: %d − %d = %d %s."
                 % (Wt, Ht, Wt * Ht, cw, ch, cw * ch, Wt * Ht, cw * ch, A, su))
        over = (Wt - cw) * Ht + Wt * (Ht - ch)
        if kind == "split":
            q = fig(svg) + "The dashed line splits the shape into two rectangles. What is the area of the shape?"
            e = split_e + (" Use each part once: %d × %d + %d × %d = %d counts the %d × %d corner twice."
                           % (Wt - cw, Ht, Wt, Ht - ch, over, Wt - cw, Ht - ch))
        elif kind == "cut":
            q = fig(svg) + "What is the area of this compound shape?"
            e = cut_e + " Or: " + split_e[0].lower() + split_e[1:]
        else:
            q = fig(svg) + "What is the area of this compound shape? Find the two missing lengths first."
            e = ("Missing lengths: %d − %d = %d and %d − %d = %d. " % (Wt, Wt - cw, cw, Ht, Ht - ch, ch)) + cut_e
        its.append(mcq(q, ar(A, su), [ar(over, su), ar(Wt * Ht, su), ar(A, u), ar(2 * (Wt + Ht), su)], e, rnd))
    # compound L-shapes: perimeter with missing sides
    for i, hide in enumerate([(1, 2), (4, 5), (2, 3)]):
        u = ["m", "cm", "m"][i]
        while True:
            Wt, Ht = rnd.randint(8, 15), rnd.randint(6, 11)
            if Wt <= Ht or Wt / Ht > 2:
                continue
            cw = rnd.randint(int(math.ceil(Wt * 0.35)), int(Wt * 0.6))
            ch = rnd.randint(int(math.ceil(Ht * 0.35)), int(Ht * 0.6))
            if cw == Wt - cw or ch == Ht - ch or (Wt, Ht, cw, ch) in used:
                continue
            sides = [Wt - cw, ch, cw, Ht - ch, Wt, Ht]
            labels = ["%d %s" % (v, u) if j not in hide else "" for j, v in enumerate(sides)]
            svg = l_svg(Wt, Ht, cw, ch, corners[(i + 1) % 4], labels, False)
            if svg:
                break
        used.add((Wt, Ht, cw, ch))
        Pm = sum(sides)
        assert Pm == 2 * (Wt + Ht)
        shown = sum(v for j, v in enumerate(sides) if j not in hide)
        miss = {1: "%d − %d = %d" % (Ht, Ht - ch, ch), 2: "%d − %d = %d" % (Wt, Wt - cw, cw),
                3: "%d − %d = %d" % (Ht, ch, Ht - ch), 4: "%d + %d = %d" % (Wt - cw, cw, Wt),
                5: "%d + %d = %d" % (ch, Ht - ch, Ht)}
        q = fig(svg) + "What is the perimeter of this compound shape?"
        e = ("Find the missing lengths: %s and %s. Then add all 6 sides: %s = %d %s."
             % (miss[hide[0]], miss[hide[1]], " + ".join(str(v) for v in sides), Pm, u))
        A = Wt * Ht - cw * ch
        its.append(mcq(q, ar(Pm, u), [ar(shown, u), ar(shown + sides[hide[0]], u), ar(A, u), ar(Pm, u + "²")], e, rnd))
    # same area, different perimeter (and the other way round)
    q = fig(must(two_rects_svg((8, 3), (6, 4), "cm"))) + "Which statement about rectangles A and B is true?"
    e = ("Area A = 8 × 3 = 24 cm², area B = 6 × 4 = 24 cm². Perimeter A = 8 + 3 + 8 + 3 = 22 cm, "
         "perimeter B = 6 + 4 + 6 + 4 = 20 cm. Same area, different perimeters.")
    its.append(mcq(q, "Same area, different perimeters",
                   ["Same perimeter, different areas", "Same area and same perimeter", "Different areas and perimeters"], e, rnd))
    q = fig(must(two_rects_svg((7, 2), (5, 4), "m"))) + "Which statement about rectangles A and B is true?"
    e = ("Perimeter A = 7 + 2 + 7 + 2 = 18 m, perimeter B = 5 + 4 + 5 + 4 = 18 m. "
         "Area A = 7 × 2 = 14 m², area B = 5 × 4 = 20 m². Same perimeter, different areas.")
    its.append(mcq(q, "Same perimeter, different areas",
                   ["Same area, different perimeters", "Same area and same perimeter", "Different areas and perimeters"], e, rnd))
    q = ("Rectangle A is 8 cm by 3 cm. Rectangle B has the same area as A and is 6 cm long. "
         "What is the perimeter of rectangle B?")
    e = ("Area of A = 8 × 3 = 24 cm². B: 6 × ? = 24, so B is 4 cm wide. Perimeter of B = 6 + 4 + 6 + 4 = 20 cm. "
         "Same area does not mean the same perimeter (A has 22 cm).")
    its.append(mcq(q, "20 cm", ["22 cm", "24 cm", "10 cm"], e, rnd))
    q = "Which rectangle has an area of 24 cm² and a perimeter of 20 cm?"
    e = ("6 × 4 = 24 cm² and 6 + 4 + 6 + 4 = 20 cm. 8 cm by 3 cm has a 22 cm perimeter, 12 cm by 2 cm has 28 cm, "
         "and 5 cm by 5 cm has the right perimeter but an area of 25 cm².")
    its.append(mcq(q, "6 cm by 4 cm", ["8 cm by 3 cm", "12 cm by 2 cm", "5 cm by 5 cm"], e, rnd))
    # squares and a missing side
    q = "A square has a perimeter of 36 cm. What is its area?"
    e = "Each side is 36 ÷ 4 = 9 cm. Area = 9 × 9 = 81 cm²."
    its.append(mcq(q, "81 cm²", ["36 cm²", "9 cm²", "324 cm²"], e, rnd))
    q = "A square has an area of 64 m². What is its perimeter?"
    e = "8 × 8 = 64, so each side is 8 m. Perimeter = 4 × 8 = 32 m."
    its.append(mcq(q, "32 m", ["16 m", "8 m", "256 m"], e, rnd))
    q = "A rectangle has an area of 72 cm². It is 9 cm long. How wide is it?"
    e = "Length × width = area, so 9 × ? = 72. 72 ÷ 9 = 8 cm. Check: 9 × 8 = 72."
    its.append(mcq(q, "8 cm", ["63 cm", "27 cm", "8 cm²"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rectangles, compound shapes and perimeter", "items": its}


# ------------------------------------------------------------ set 2: triangles
def tri_options():
    H = {}
    for d, h, s in TRIPLES:
        for sc in (Fr(1), Fr(1, 2)):
            H.setdefault(h * sc, set()).add((d * sc, s * sc))
    acute, obtuse = set(), set()
    for h, ds in H.items():
        if h.denominator != 1 or not 3 <= h <= 24:
            continue
        for d1, s1 in ds:
            for d2, s2 in ds:
                b = d1 + d2
                if d1 <= d2 and b.denominator == 1 and b <= 30 and 0.8 <= b / h <= 2.8 and b != 2 * h:
                    acute.add((b, d1, h, s1, s2))
                b = d2 - d1
                if d1 < d2 and b.denominator == 1 and d2 <= 36 and b >= 4 and b >= 0.25 * d2 and 0.6 <= d2 / h <= 3:
                    obtuse.add((b, d2, h, s2, s1))
    return sorted(acute), sorted(obtuse)


def set_tri(rnd):
    its = []
    seen = set()
    # right-angled triangles
    tr = [t for t in TRIPLES if t[0] < t[1] <= 24 and t[1] / t[0] <= 3 and t[0] >= 3]
    rnd.shuffle(tr)
    for i in range(4):
        u, su = AREA_U[i % 4]
        while True:
            if i % 2 == 0:
                a, b, c = tr.pop()
                if rnd.random() < 0.5:
                    a, b = b, a
            else:
                a, b, c = rnd.randint(4, 15), rnd.randint(3, 12), None
                if a == b or max(a, b) / min(a, b) > 2.6 or (a * b) % 2:
                    continue
            if (a * b) in seen:
                continue
            svg = right_tri_svg(a, b, "%d %s" % (a, u), "%d %s" % (b, u), "%d %s" % (c, u) if c else "", i % 4)
            if svg:
                break
        seen.add(a * b)
        A = Fr(a * b, 2)
        q = fig(svg) + "What is the area of the right-angled triangle?"
        e = ("The two sides that meet at the right angle are the base and the perpendicular height. "
             "Area = %s = %s %s." % (hx(a, b), num(A), su))
        if c:
            e += " The %d %s side is slanted, so it is not the height." % (c, u)
            cands = [ar(a * b, su), ar(Fr(max(a, b) * c, 2), su), ar(A, u), ar(a + b + c, su)]
        else:
            cands = [ar(a * b, su), ar(A, u), ar(a + b, su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # any triangle drawn, slanted side labelled
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    used_bh = set()
    for i in range(8):
        u, su = AREA_U[(i + 1) % 4]
        pool = obtuse if i % 2 else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            if (b, h) in used_bh or Fr(b * h, 2) in seen:
                continue
            side = "L" if i % 2 else rnd.choice("LR")
            s = sl if side == "L" else sr
            if Fr(b * s, 2) == Fr(b * h, 2) or s == b:
                continue
            mir, flp = rnd.random() < 0.5, i in (2, 7)
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(s, u), side), mir, flp,
                          label="obtuse-angled triangle with its height outside" if i % 2 else "triangle with its perpendicular height")
            if svg:
                break
        used_bh.add((b, h))
        A = Fr(b * h, 2)
        q = fig(svg) + "What is the area of the triangle?"
        e = ("The perpendicular height is the dashed line: it meets the base at a right angle. "
             "Area = %s × base × height = %s = %s %s. The %s %s side is slanted, so it is not the height."
             % (HALF, hx(b, h), num(A), su, num(s), u))
        if i % 2:
            e += " This triangle has an obtuse angle, so its height is outside it and meets the grey dashed line that extends the base."
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(Fr(b * s, 2), su), ar(A, u), ar(b * s, su)], e, rnd))
    # text
    for b, h, u, su in [(Fr(15, 2), 4, "m", "m²"), (12, Fr(13, 2), "cm", "cm²"), (9, 5, "mm", "mm²"), (14, 11, "cm", "cm²")]:
        A = Fr(b * h, 2)
        q = "A triangle has a base of %s %s and a perpendicular height of %s %s. What is its area?" % (num(b), u, num(h), u)
        e = "Area = %s = %s %s." % (hx(b, h), num(A), su)
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(A, u), ar(b + h, su)], e, rnd))
    # missing base / height
    for A, k, u, su, what, other in [(36, 9, "cm", "cm²", "base", "perpendicular height"), (42, 7, "m", "m²", "perpendicular height", "base")]:
        o = Fr(2 * A, k)
        q = "A triangle has an area of %d %s. Its %s is %d %s. What is its %s?" % (A, su, what, k, u, other)
        e = ("%s × %d × ? = %d. Double the area first: %d × 2 = %d. Then %d ÷ %d = %s %s. Check: %s = %d %s."
             % (HALF, k, A, A, 2 * A, 2 * A, k, num(o), u, hx(k, o), A, su))
        its.append(mcq(q, ar(o, u), [ar(Fr(A, k), u), ar(A - k, u), ar(o, su), ar(Fr(A, 2), u)], e, rnd))
    # which calculation
    for i in range(2):
        u = ["m", "cm"][i]
        while True:
            b, p, h, sl, sr = obtuse.pop() if i == 0 else acute.pop()
            if (b, h) in used_bh or sl == b or sl.denominator != 1:
                continue
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(sl, u), "L"), i == 1, False,
                          label="obtuse-angled triangle with its height outside" if i == 0 else "triangle with its perpendicular height")
            if svg:
                break
        used_bh.add((b, h))
        q = fig(svg) + "Which calculation gives the area of the triangle?"
        right = "%s × %d × %d" % (HALF, b, h)
        wrong = ["%s × %d × %s" % (HALF, b, num(sl)), "%d × %d" % (b, h), "%d + %d" % (b, h)]
        e = ("The base is %d %s and the perpendicular height is the dashed %d %s line. Area = %s = %s %s². "
             "%d × %d forgets to halve, and %s %s is a slanted side." % (b, u, h, u, right, num(Fr(b * h, 2)), u, b, h, num(sl), u))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of triangles", "items": its}


# ------------------------------------------------------------ set 3: parallelograms
def set_para(rnd):
    its = []
    seen = set()
    tr = [t for t in TRIPLES if t[0] <= 12 and 3 <= t[1] <= 16 and t[0] / t[1] <= 1.4]
    rnd.shuffle(tr)
    for i in range(10):
        u, su = AREA_U[i % 4]
        svg = None
        j = i
        while not svg:
            o, h, s = tr[j % len(tr)]
            j += 1
            bs = [b for b in range(max(o + 3, 6), 19) if b not in (s, h) and b / h <= 3.2 and b * h not in seen]
            rnd.shuffle(bs)
            for b in bs[:4]:
                svg = para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i % 3 == 1)
                if svg:
                    break
        seen.add(b * h)
        A = b * h
        q = fig(svg) + "What is the area of the parallelogram?"
        e = ("Area = base × perpendicular height = %d × %d = %s %s. The height is the dashed line at a right angle to the base, "
             "not the slanted %d %s side. (Cut the triangle off one end and move it to the other end: "
             "you get %s %d by %d rectangle.)" % (b, h, num(A), su, s, u, "an" if b in (8, 11, 18) else "a", b, h))
        its.append(mcq(q, ar(A, su), [ar(b * s, su), ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + s), su)], e, rnd))
    for b, h, s, u, su in [(Fr(17, 2), 6, None, "m", "m²"), (14, Fr(23, 2), None, "cm", "cm²"), (9, 7, 8, "cm", "cm²")]:
        A = b * h
        if s:
            q = ("A parallelogram has a base of %s %s, a slanted side of %s %s and a perpendicular height of %s %s. "
                 "What is its area?" % (num(b), u, num(s), u, num(h), u))
            e = "Area = base × perpendicular height = %s × %s = %s %s. The slanted %s %s side is not used." % (
                num(b), num(h), num(A), su, num(s), u)
            cands = [ar(b * s, su), ar(Fr(A, 2), su), ar(2 * (b + s), su)]
        else:
            q = "A parallelogram has a base of %s %s and a perpendicular height of %s %s. What is its area?" % (num(b), u, num(h), u)
            e = "Area = base × perpendicular height = %s × %s = %s %s. Do not halve: that is only for triangles." % (
                num(b), num(h), num(A), su)
            cands = [ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + h), su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    q = "A parallelogram has an area of 96 m². Its base is 12 m. What is its perpendicular height?"
    e = "Area = base × height, so 12 × ? = 96. 96 ÷ 12 = 8 m. Check: 12 × 8 = 96."
    its.append(mcq(q, "8 m", ["16 m", "84 m", "8 m²"], e, rnd))
    q = "A parallelogram has an area of 63 cm². Its perpendicular height is 7 cm. How long is its base?"
    e = "Base × 7 = 63. 63 ÷ 7 = 9 cm. Check: 9 × 7 = 63."
    its.append(mcq(q, "9 cm", ["18 cm", "56 cm", "9 cm²"], e, rnd))
    q = "A parallelogram has an area of 45 cm². Its base is 6 cm. What is its perpendicular height?"
    e = "6 × ? = 45. 45 ÷ 6 = 7.5 cm. Check: 6 × 7.5 = 45. (3.75 cm would be halving, as for a triangle.)"
    its.append(mcq(q, "7.5 cm", ["3.75 cm", "39 cm", "7.5 cm²"], e, rnd))
    for i in range(2):
        u = ["m", "cm"][i]
        o, h, s = [(5, 12, 13), (3, 4, 5)][i]
        b = [14, 9][i]
        svg = must(para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 1))
        q = fig(svg) + "Which calculation gives the area of the parallelogram?"
        right = "%d × %d" % (b, h)
        e = ("Base × perpendicular height: %s = %d %s². The %d %s side is slanted, and a parallelogram is not halved."
             % (right, b * h, u, s, u))
        its.append(mcq(q, right, ["%d × %d" % (b, s), "%s × %d × %d" % (HALF, b, h), "%d + %d" % (b, h)], e, rnd))
    q = ("A triangle and a parallelogram both have a base of 10 cm and a perpendicular height of 6 cm. "
         "How much greater is the area of the parallelogram?")
    e = "Parallelogram: 10 × 6 = 60 cm². Triangle: " + hx(10, 6) + " = 30 cm². Difference: 60 − 30 = 30 cm²."
    its.append(mcq(q, "30 cm²", ["60 cm²", "90 cm²", "They have the same area"], e, rnd))
    q = ("Triangle A has a base of 12 cm and a perpendicular height of 8 cm. Parallelogram B has a base of 6 cm "
         "and a perpendicular height of 8 cm. Which is true?")
    e = ("A: %s = 48 cm². B: 6 × 8 = 48 cm². They have the same area. (Forgetting to halve makes A look twice as big.)"
         % hx(12, 8))
    its.append(mcq(q, "They have the same area.", ["A has the greater area.", "B has the greater area.", "A is twice the area of B."], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of parallelograms", "items": its}


# ------------------------------------------------------------ set 4: volume of cubes and cuboids
def set_vol(rnd):
    its = []
    seen = set()
    for i in range(5):
        while True:
            l, w, h = rnd.randint(2, 5), rnd.randint(2, 3), rnd.randint(2, 4)
            if (l, w, h) in seen or l <= w or (l - 1) * (w - 1) * (h - 1) == 0:
                continue
            break
        seen.add((l, w, h))
        V, vis = l * w * h, visible_cubes(l, w, h)
        faces = l * h + l * w + w * h
        q = fig(cubes_svg(l, w, h)) + "Each small cube is 1 cm³. What is the volume of the cuboid?"
        e = ("One layer has %d rows of %d cubes = %d cubes. There are %d layers: %d × %d = %d cm³. "
             "Count the hidden cubes too (only %d cubes can be seen)." % (w, l, l * w, h, l * w, h, V, vis))
        its.append(mcq(q, "%d cm³" % V, ["%d cm³" % x for x in (vis, faces, l + w + h, l * h, l * w * (h - 1)) if x != V], e, rnd))
    for i in range(7):
        while True:
            L, W, H = rnd.randint(4, 15), rnd.randint(2, 9), rnd.randint(2, 12)
            if L > W and (L, W, H) not in seen and L * W != W * H and H != W:
                break
        seen.add((L, W, H))
        u, cu, sq = VOL_U[i % 3]
        V = L * W * H
        SA = 2 * (L * W + L * H + W * H)
        lab = lambda v: "%d %s" % (v, u)
        q = fig(cuboid_svg(L, W, H, lab(L), lab(W), lab(H))) + "What is the volume of the cuboid?"
        e = ("Volume = length × width × height = %d × %d × %d = %s × %d = %s %s. Multiply all three lengths, "
             "and write the answer in cubic units (%s)." % (L, W, H, num(L * W), H, num(V), cu, cu))
        pool = ["%s %s" % (num(L * W), cu), "%d %s" % (L + W + H, cu), "%s %s" % (num(V), sq), "%s %s" % (num(SA), cu)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        its.append(mcq(q, "%s %s" % (num(V), cu), pool, e, rnd))
    for s, (u, cu, sq) in zip([6, 9], VOL_U[:2]):
        V = s ** 3
        q = "A cube has edges of %d %s. What is its volume?" % (s, u)
        e = "Every edge of a cube is %d %s, so volume = %d × %d × %d = %d × %d = %s %s." % (s, u, s, s, s, s * s, s, num(V), cu)
        its.append(mcq(q, "%s %s" % (num(V), cu), ["%d %s" % (3 * s, cu), "%d %s" % (s * s, cu), "%s %s" % (num(V), sq)], e, rnd))
    for i in range(4):
        while True:
            L, W, H = rnd.randint(4, 12), rnd.randint(2, 8), rnd.randint(3, 10)
            V = L * W * H
            if L > W and (L, W, H) not in seen and H not in (L, W):
                break
        seen.add((L, W, H))
        u, cu, sq = VOL_U[i % 2]
        miss = ["h", "l", "w", "h"][i]
        known = {"h": (L, W), "l": (W, H), "w": (L, H)}[miss]
        ans = {"h": H, "l": L, "w": W}[miss]
        a, b = known
        cands = ["%d %s" % (V // a, u), "%d %s" % (V - a - b, u), "%d %s" % (ans, cu), "%d %s" % (a * b, u)]
        e = ("%d × %d × ? = %s, so %d × ? = %s. %s ÷ %d = %d %s. Check: %d × %d × %d = %s."
             % (a, b, num(V), a * b, num(V), num(V), a * b, ans, u, L, W, H, num(V)))
        if i < 2:
            labs = {"l": "%d %s" % (L, u), "w": "%d %s" % (W, u), "h": "%d %s" % (H, u)}
            labs[miss] = "? %s" % u
            q = (fig(cuboid_svg(L, W, H, labs["l"], labs["w"], labs["h"], "cuboid with one unknown length")) +
                 "The volume of this cuboid is %s %s. What is the missing length, marked with a question mark?" % (num(V), cu))
        else:
            word = {"h": "How tall is it?", "l": "How long is it?", "w": "How wide is it?"}[miss]
            given = {"h": "%d %s long and %d %s wide" % (L, u, W, u),
                     "l": "%d %s wide and %d %s tall" % (W, u, H, u),
                     "w": "%d %s long and %d %s tall" % (L, u, H, u)}[miss]
            q = "A cuboid has a volume of %s %s. It is %s. %s" % (num(V), cu, given, word)
        its.append(mcq(q, "%d %s" % (ans, u), cands, e, rnd))
    q = "Which of these would be measured in cubic metres (m³)?"
    e = ("m³ measures volume, the space inside a 3-D shape, such as the water in a pool. "
         "Area is in m², length is in m and mass is in kg or tonnes.")
    its.append(mcq(q, "the water in a swimming pool",
                   ["the area of a football pitch", "the length of a corridor", "the mass of a lorry"], e, rnd))
    q = "How many cubic millimetres (mm³) are there in 1 cm³?"
    e = "1 cm = 10 mm, so a 1 cm cube is 10 mm × 10 mm × 10 mm = 1,000 mm³."
    its.append(mcq(q, "1,000 mm³", ["10 mm³", "100 mm³", "1,000,000 mm³"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Volume of cubes and cuboids", "items": its}


# ------------------------------------------------------------ set 5: SATs-style word problems
def set_story(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    n, he, his = P.next()
    add("%s's rectangular garden is 12 m long and 9 m wide. A patio 4 m by 3 m is in one corner. "
        "The rest is lawn. What is the area of the lawn?" % n, "96 m²", ["108 m²", "120 m²", "96 m"],
        "Garden: 12 × 9 = 108 m². Patio: 4 × 3 = 12 m². Lawn: 108 − 12 = 96 m².")
    n, he, his = P.next()
    add("%s is laying turf on a lawn 8 m long and 6 m wide. Turf costs £4 per m². How much does the turf cost?" % n,
        "£192", ["£112", "£56", "£48"],
        "Area: 8 × 6 = 48 m². Cost: 48 × £4 = £192. (£112 uses the perimeter, 28 m, instead of the area.)")
    add("A lawn is 8 m long and 6 m wide. How much fencing is needed to go all the way round it?",
        "28 m", ["48 m", "14 m", "28 m²"],
        "All the way round is the perimeter: 8 + 6 + 8 + 6 = 28 m. 48 is the area, and 14 m is only two sides.")
    n, he, his = P.next()
    add("%s has 24 square paving slabs, each 1 m by 1 m. %s uses all of them to make a rectangular patio. "
        "Which patio has the shortest perimeter?" % (n, he.capitalize()),
        "6 m by 4 m", ["8 m by 3 m", "12 m by 2 m", "24 m by 1 m"],
        "All four have an area of 24 m². Perimeters: 6 m by 4 m = 20 m, 8 m by 3 m = 22 m, 12 m by 2 m = 28 m, "
        "24 m by 1 m = 50 m. The closer to a square, the shorter the perimeter.")
    n, he, his = P.next()
    add("%s has 20 m of fencing for a rectangular rabbit run. Which run gives the rabbits the most space?" % n,
        "5 m by 5 m", ["6 m by 4 m", "7 m by 3 m", "8 m by 2 m"],
        "Every run has a perimeter of 20 m. Areas: 5 × 5 = 25 m², 6 × 4 = 24 m², 7 × 3 = 21 m², 8 × 2 = 16 m². "
        "Same perimeter, different areas.")
    n, he, his = P.next()
    add("%s paints a wall 5 m wide and 2.4 m high. There is a door in the wall 2 m high and 0.9 m wide. "
        "What area does %s paint?" % (n, he), "10.2 m²", ["12 m²", "13.8 m²", "10.2 m"],
        "Wall: 5 × 2.4 = 12 m². Door: 2 × 0.9 = 1.8 m². Paint: 12 − 1.8 = 10.2 m².")
    add("Two walls are each 5 m wide and 2.6 m high. One tin of paint covers 10 m². How many tins are needed "
        "to paint both walls?", "3 tins", ["2 tins", "26 tins", "4 tins"],
        "One wall: 5 × 2.6 = 13 m². Two walls: 26 m². 26 ÷ 10 = 2.6, so 2 tins are not enough: round up to 3 tins.")
    add("A triangular flower bed has a base of 6 m and a perpendicular height of 3.5 m. What is its area?",
        "10.5 m²", ["21 m²", "9.5 m²", "10.5 m"], "Area = %s = 10.5 m²." % hx(6, Fr(7, 2)))
    n, he, his = P.next()
    add("%s makes bunting from 20 triangular flags. Each flag has a base of 15 cm and a perpendicular height of 20 cm. "
        "How much fabric do the flags use altogether?" % n, "3,000 cm²", ["6,000 cm²", "150 cm²", "3,000 cm"],
        "One flag: %s = 150 cm². 20 flags: 20 × 150 = 3,000 cm²." % hx(15, 20))
    add("A flower bed is a parallelogram. Its base is 5 m, its slanted sides are 3 m, and its perpendicular height "
        "is 2.5 m. What is its area?", "12.5 m²", ["15 m²", "6.25 m²", "16 m²"],
        "Area = base × perpendicular height = 5 × 2.5 = 12.5 m². The 3 m sides are slanted, so they are not used.")
    add("A fish tank is a cuboid 60 cm long, 30 cm wide and 40 cm high. What is its volume?",
        "72,000 cm³", ["1,800 cm³", "130 cm³", "72,000 cm²"],
        "Volume = 60 × 30 × 40 = 1,800 × 40 = 72,000 cm³. 1,800 is only the area of the base.")
    n, he, his = P.next()
    add("%s's fish tank is 50 cm long, 30 cm wide and 40 cm high. 1,000 cm³ = 1 litre. "
        "How many litres of water does the tank hold when it is full?" % n, "60 litres",
        ["600 litres", "6 litres", "60,000 litres"],
        "Volume: 50 × 30 × 40 = 60,000 cm³. Litres: 60,000 ÷ 1,000 = 60 litres.")
    add("A fish tank is 40 cm long, 20 cm wide and 40 cm high. It is filled with water to a depth of 25 cm. "
        "How many litres of water are in the tank? (1,000 cm³ = 1 litre)", "20 litres",
        ["32 litres", "2 litres", "200 litres"],
        "Use the depth of the water, not the height of the tank: 40 × 20 × 25 = 20,000 cm³. "
        "20,000 ÷ 1,000 = 20 litres. (32 litres is the full tank.)")
    add("A box of sugar cubes is 8 cm long, 5 cm wide and 3 cm high. Each sugar cube is 1 cm³. "
        "How many sugar cubes fill the box?", "120", ["16", "40", "158"],
        "One layer: 8 × 5 = 40 cubes. 3 layers: 40 × 3 = 120 sugar cubes.")
    n, he, his = P.next()
    add("%s packs sugar cubes with 2 cm edges into a box 10 cm long, 6 cm wide and 4 cm high. "
        "How many sugar cubes fit?" % n, "30", ["240", "120", "20"],
        "Along each edge: 10 ÷ 2 = 5, 6 ÷ 2 = 3, 4 ÷ 2 = 2. Cubes: 5 × 3 × 2 = 30. "
        "(240 would be 1 cm cubes.)")
    add("A sandpit is 2 m long and 1.5 m wide. It is filled with sand 0.2 m deep. What volume of sand is needed?",
        "0.6 m³", ["3 m³", "3.7 m³", "0.6 m²"],
        "Volume = 2 × 1.5 × 0.2 = 3 × 0.2 = 0.6 m³. 3 m² is only the area of the sandpit.")
    add("A box is a cube with 1 m edges. How many 1 cm cubes would fill it?", "1,000,000",
        ["1,000", "100", "10,000"],
        "1 m = 100 cm, so the box is 100 × 100 × 100 = 1,000,000 cubes. So 1 m³ = 1,000,000 cm³.")
    add("A box has a volume of 480 cm³. Its base is 12 cm by 8 cm. How high is the box?", "5 cm",
        ["40 cm", "460 cm", "5 cm³"],
        "Area of base: 12 × 8 = 96 cm². 96 × ? = 480, so the height is 480 ÷ 96 = 5 cm. Check: 12 × 8 × 5 = 480.")
    add("A swimming pool is 25 m long and 10 m wide. The water is 2 m deep everywhere. What is the volume of the water?",
        "500 m³", ["250 m³", "37 m³", "500 m²"],
        "Volume = 25 × 10 × 2 = 250 × 2 = 500 m³. 250 m² is only the area of the pool.")
    add("Box A is a cube with 10 cm edges. Box B is 20 cm by 5 cm by 8 cm. Which box has the greater volume, and by how much?",
        "A, by 200 cm³", ["B, by 200 cm³", "B, by 3 cm³", "They are the same"],
        "A: 10 × 10 × 10 = 1,000 cm³. B: 20 × 5 × 8 = 800 cm³. A is greater by 1,000 − 800 = 200 cm³. "
        "(Adding the edges gives 30 and 33, but that is not volume.)")
    assert len(its) == 20, len(its)
    return {"title": "SATs-style word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    lab = ["4 m", "3 m", "5 m", "4 m", "9 m", "7 m"]
    return (
        "<h2>Area, perimeter and volume</h2>"
        "<p><b>Perimeter</b> is the distance all the way round a shape (cm, m). "
        "<b>Area</b> is the flat space inside it (cm², m²). "
        "<b>Volume</b> is the space inside a 3-D shape (cm³, m³).</p>"
        "<h2>Rectangles and compound shapes</h2>"
        "<p>Area of a rectangle = length × width. For a compound (rectilinear) shape, split it into rectangles "
        "and add the areas. For the perimeter, find any missing lengths first, then add every side.</p>"
        "<figure class='sn-fig'>" + must(l_svg(9, 7, 5, 3, "tr", lab, True)) +
        "<figcaption>Area: 4 × 7 = 28 and 5 × 4 = 20, so 28 + 20 = 48 m². "
        "Perimeter: 4 + 3 + 5 + 4 + 9 + 7 = 32 m.</figcaption></figure>"
        "<p><b>Same area, different perimeter.</b> 8 cm by 3 cm and 6 cm by 4 cm both have an area of 24 cm², "
        "but their perimeters are 22 cm and 20 cm. It works the other way round too: shapes with the same perimeter "
        "can have different areas.</p>"
        "<h2>Triangles: area = " + HALF + " × base × perpendicular height</h2>"
        "<p>A triangle is half of a rectangle or parallelogram with the same base and height. "
        "The <b>perpendicular height</b> meets the base at a right angle. It is the dashed line, not a slanted side.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(14, 5, 12, "14 cm", "12 cm", ("13 cm", "L"))) +
        "<figcaption>Area = " + HALF + " × 14 × 12 = " + HALF + " × 168 = 84 cm². The 13 cm side is not used.</figcaption></figure>"
        "<p>In an obtuse-angled triangle the height can be <b>outside</b> the triangle. Extend the base and measure to that line.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(7, 16, 12, "7 m", "12 m", ("20 m", "L"),
                                              label="obtuse-angled triangle with its height outside")) +
        "<figcaption>Area = " + HALF + " × 7 × 12 = 42 m². The base is 7 m, not the grey dashed extension.</figcaption></figure>"
        "<h2>Parallelograms: area = base × perpendicular height</h2>"
        "<p>Cut the triangle off one end and slide it to the other end. You get a rectangle with the same base and height.</p>"
        "<figure class='sn-fig'>" + must(para_svg(12, 6, 8, "12 cm", "8 cm", "10 cm")) +
        "<figcaption>Area = 12 × 8 = 96 cm². The slanted 10 cm side is not the height.</figcaption></figure>"
        "<h2>Volume of cubes and cuboids: length × width × height</h2>"
        "<p>Volume counts the 1 cm cubes that fill a shape. Count the cubes in one layer, then multiply by the number of layers.</p>"
        "<figure class='sn-fig'>" + cubes_svg(4, 3, 3, "cuboid of centimetre cubes with its layers pulled apart", gap=0.45) +
        "<figcaption>One layer: 4 × 3 = 12 cubes. 3 layers: 12 × 3 = 36 cm³.</figcaption></figure>"
        "<figure class='sn-fig'>" + cuboid_svg(6, 4, 5, "6 cm", "4 cm", "5 cm") +
        "<figcaption>Volume = 6 × 4 × 5 = 120 cm³.</figcaption></figure>" +
        ex("Missing length", "A cuboid has a volume of 120 cm³. It is 5 cm long and 4 cm wide. How high is it?",
           "5 × 4 × ? = 120, so 20 × ? = 120. 120 ÷ 20 = 6.", "6 cm") +
        "<h2>Units</h2>" +
        table(["Measure", "Units", "Example"], [
            ["Perimeter (length)", "mm, cm, m, km", "32 m"],
            ["Area", "mm², cm², m², km²", "84 cm²"],
            ["Volume", "mm³, cm³, m³, km³", "120 cm³"],
            ["Capacity", "1,000 cm³ = 1 litre", "60,000 cm³ = 60 litres"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Triangle: 14 × 12 = 168 cm²", "Halve it: " + HALF + " × 14 × 12 = 84 cm²"],
            ["Using the slanted side as the height", "Use the perpendicular height (the dashed line)"],
            ["Volume: 6 + 4 + 5 = 15", "Multiply: 6 × 4 × 5 = 120 cm³"],
            ["Writing cm² for a volume", "Area is cm², volume is cm³"],
            ["Missing a side of a compound shape", "Find the missing lengths, then add all the sides"],
            ["Thinking the same area means the same perimeter", "Work out both: 8 cm by 3 cm and 6 cm by 4 cm have different perimeters"],
        ])
    )


FAQ = [
    {"q": "How do you find the area of a triangle in Year 6?",
     "a": "Multiply the base by the perpendicular height and halve it: area = ½ × base × height. For a base of 14 cm and a height of 12 cm, the area is ½ × 168 = 84 cm²."},
    {"q": "What is the formula for the volume of a cuboid?",
     "a": "Volume = length × width × height. A cuboid 6 cm by 4 cm by 5 cm has a volume of 120 cm³, which is 120 centimetre cubes."},
    {"q": "Is area and volume in the Year 6 SATs?",
     "a": "Yes. The reasoning papers often ask for the area of triangles, parallelograms or compound shapes and the volume of cuboids. There is no formula sheet, so pupils need to know the formulae."},
    {"q": "Can two shapes have the same area but different perimeters?",
     "a": "Yes. A rectangle 8 cm by 3 cm and one 6 cm by 4 cm both have an area of 24 cm², but their perimeters are 22 cm and 20 cm."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position) in every set."""
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
    rnd = random.Random(6615)
    P = People(rnd)
    sets = [set_rect(rnd), set_tri(rnd), set_para(rnd), set_vol(rnd), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "area-perimeter-and-volume", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Area, Perimeter and Volume",
        "seo_title": "Year 6 Area, Perimeter and Volume Worksheets: Triangles, Parallelograms and Cuboids",
        "short_title": "Area, perimeter and volume",
        "domain": "Measurement",
        "standard_code": "Year 6: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise that shapes with the same areas can have different perimeters and vice versa; recognise when it is possible to use formulae for area and volume of shapes; calculate the area of parallelograms and triangles; calculate, estimate and compare volume of cubes and cuboids using standard units, including cubic centimetres (cm³) and cubic metres (m³), and extending to other units [for example, mm³ and km³].",
        "meta_desc": "Free Year 6 area, perimeter and volume worksheets for the National Curriculum: compound shapes, same area and different perimeter, area of triangles and parallelograms, volume of cubes and cuboids in cm³ and m³, and SATs-style word problems. 100 questions with an answer key.",
        "key_big": "Triangle: ½ × base × height. Parallelogram: base × height. Cuboid: length × width × height.",
        "key_sub": "Always use the perpendicular height, never a slanted side. Area is in square units (cm², m²); volume is in cubic units (cm³, m³). Shapes with the same area can have different perimeters.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(compound|two rectangles|cuboid made of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
