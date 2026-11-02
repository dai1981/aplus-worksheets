# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Area of Parallelograms, Triangles, Trapezoids, Kites and Composite Polygons
(Ontario Curriculum 2020, Spatial Sense E2)
  python3 tools/gen_ca_math_g6_area.py
Drawing engine and composite figures are copied from gen_us_math_g6_area_polygons.py.
Every figure is drawn to scale from its numbers. Heights are red dashed lines with a right-angle mark;
slanted sides are labelled only with their true lengths (integer right triangles), so they can act as distractors.
Canadian style: metric units only (mm, cm, m), 4-digit numbers without a separator, 5 or more digits with a
no-break space (13 500). Trapezoids and kites are found by decomposing into rectangles and triangles.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
WHITE = "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
UNITS = [("cm", "cm²"), ("m", "m²"), ("mm", "mm²"), ("cm", "cm²")]
HALF = "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"


# ------------------------------------------------------------ helpers
def num(x):
    """Exact number as text, Ontario style: 4536, 13 500 (no-break space), 22.5."""
    x = Fr(x)
    assert x >= 0, x
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
    i = int(i)
    t = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    return t + ("." + fpart if fpart else "")


def ar(x, unit):
    return "%s %s" % (num(x), unit)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
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
    """Approximate width of bold Arial text in px. Periods and spaces are narrow."""
    t = str(t)
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - (t.count(" ") + t.count(NBSP)) * 0.3) * fs * 0.6


# ------------------------------------------------------------ drawing engine
FS = 16
HH = 10          # half height of a label box


def seg_hits_box(p, q, b):
    """Liang-Barsky: does segment pq cross box b = (x0, y0, x1, y1)?"""
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
    """Ray casting: is the point inside the polygon?"""
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def render(polys, label, lines=(), rights=(), labels=(), maxw=200, maxh=110, mirror=False, flip=False):
    """Draw a figure to scale. Coordinates are in the problem's units, y going up.
    polys  = [(points, fill)]
    lines  = [(p, q, style)]  style: 'h' height (red dashed), 's' split (red dashed), 'x' extension (grey dashed)
    rights = [(F, A, B)]      right-angle mark at F between rays FA and FB
    labels = [(p, q, text, mode)] text next to segment pq; mode = polygon points (put it outside that polygon)
             or None (try both sides).
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
    segs = []
    pp = []
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
    for a, b, t, mode in labels:
        a, b = P(a), P(b)
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        n1 = (dy / L, -dx / L)
        if isinstance(mode, str):                       # 'up', 'down', 'left', 'right' before mirror/flip
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
        texts.append((cx, cy, t))
    xs = [p[0] for q, _ in pp for p in q] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for q, _ in pp for p in q] + [b[1] for b in boxes] + [b[3] for b in boxes]
    xs += [p[0] for a, b, _ in ll for p in (a, b)]
    ys += [p[1] for a, b, _ in ll for p in (a, b)]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))

    def pt(p):
        return "%.1f,%.1f" % (p[0] - ox, p[1] - oy)
    s = []
    for q, fill in pp:
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                 % (" ".join(pt(p) for p in q), fill, GREEN))
    for a, b, st in ll:
        col, wdt, da = (GRAY, 2, "5 4") if st == "x" else (RED, 2.5, "7 5")
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s' stroke-dasharray='%s'/>"
                 % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, wdt, da))
    for a, m, c in marks:
        s.append("<polyline points='%s %s %s' fill='none' stroke='%s' stroke-width='1.8'/>" % (pt(a), pt(m), pt(c), INK))
    for cx, cy, t in texts:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx - ox, cy - oy + 6, FS, RED if "?" in t else INK, t))
    return svg_wrap(W, H, "".join(s), label)


def must(svg):
    assert svg, "figure did not fit"
    return svg


# ------------------------------------------------------------ shapes
def right_tri_svg(a, b, la, lb, lc, orient_i, label="right triangle"):
    """Legs a (across) and b (up) meet at the right angle. orient_i 0-3 turns the corner around."""
    pts = [(0, 0), (a, 0), (0, b)]
    labels = [((0, 0), (a, 0), la, pts), ((0, b), (0, 0), lb, pts)]
    if lc:
        labels.append(((a, 0), (0, b), lc, pts))
    return render([(pts, FILL)], label, rights=[((0, 0), (a, 0), (0, b))], labels=labels,
                  mirror=orient_i in (1, 2), flip=orient_i in (2, 3), maxw=170, maxh=105)


def half_rect_svg(L, W, u, which):
    rect = [(0, 0), (L, 0), (L, W), (0, W)]
    tri = [[(0, 0), (L, 0), (L, W)], [(0, 0), (L, W), (0, W)]][which]
    return render([(rect, WHITE), (tri, FILL)], "rectangle cut by a diagonal, one triangle shaded",
                  labels=[((0, 0), (L, 0), "%s %s" % (num(L), u), rect), ((L, 0), (L, W), "%s %s" % (num(W), u), rect)],
                  maxw=190, maxh=100)


def tri_svg(b, p, h, lb, lh, slant, mirror=False, flip=False, label="triangle with its height"):
    """Base from (0,0) to (b,0), top vertex at (p,h). The height is a dashed line from the top vertex
    straight down to the base line; when p is outside 0..b the base is extended with a grey dashed line.
    slant = (text, 'L' or 'R') labels a slanted side."""
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
    if p != 0 and p != b:
        lines.append(((p, h), (p, 0), "h"))
    labels = [((0, 0), (b, 0), lb, pts)]
    if p in (0, b):
        labels.append(((p, h), (p, 0), lh, pts))
        rights.append(((p, 0), (b - p, 0), (p, h)))
    else:
        labels.append(((p, h), (p, 0), lh, None))
    if slant:
        t, side = slant
        labels.append((((0, 0), (p, h), t, pts) if side == "L" else ((b, 0), (p, h), t, pts)))
    return render([(pts, FILL)], label, lines, rights, labels, mirror=mirror, flip=flip, maxw=200, maxh=115)


def para_svg(b, o, h, lb, lh, ls, mirror=False, label="parallelogram with its height"):
    pts = [(0, 0), (b, 0), (b + o, h), (o, h)]
    return render([(pts, FILL)], label, lines=[((o, h), (o, 0), "h")], rights=[((o, 0), (b, 0), (o, h))],
                  labels=[((0, 0), (b, 0), lb, pts), ((o, h), (o, 0), lh, None)] + ([((0, 0), (o, h), ls, pts)] if ls else []),
                  mirror=mirror, maxw=200, maxh=100)


def trap_svg(b1, b2, o, h, l1, l2, lh, lleg, mirror=False, flip=False, label="trapezoid with its height"):
    """Bottom base b1, top base b2 starting at x = o. o = 0 makes a right trapezoid (the left side is the height)."""
    pts = [(0, 0), (b1, 0), (o + b2, h), (o, h)]
    labels = [((0, 0), (b1, 0), l1, pts), ((o + b2, h), (o, h), l2, pts)]
    lines, rights = [], []
    if o == 0:
        rights += [((0, 0), (b1, 0), (0, h)), ((0, h), (b2, h), (0, 0))]
        labels.append(((0, h), (0, 0), lh, pts))
    else:
        lines.append(((o, h), (o, 0), "h"))
        rights.append(((o, 0), (b1, 0), (o, h)))
        labels.append(((o, h), (o, 0), lh, None))
        if lleg:
            labels.append(((0, 0), (o, h), lleg, pts))
    return render([(pts, FILL)], label, lines, rights, labels, mirror=mirror, flip=flip, maxw=200, maxh=100)


def l_pts(Wt, Ht, cw, ch, corner):
    """L shape: a Wt by Ht rectangle with a cw by ch piece cut from one corner (y up).
    Sides in order: [Wt - cw, ch, cw, Ht - ch, Wt, Ht]."""
    p = [(0, Ht), (Wt - cw, Ht), (Wt - cw, Ht - ch), (Wt, Ht - ch), (Wt, 0), (0, 0)]
    if corner in ("tl", "bl"):
        p = [(Wt - x, y) for x, y in p]
    if corner in ("br", "bl"):
        p = [(x, Ht - y) for x, y in p]
    return p


CL = "composite figure"


def l_svg(Wt, Ht, cw, ch, corner, labels, split):
    pts = l_pts(Wt, Ht, cw, ch, corner)
    lab = [(pts[i], pts[(i + 1) % 6], t, pts) for i, t in enumerate(labels) if t]
    lines = []
    if split:
        x = pts[1][0]
        y = pts[2][1]
        lines.append(((x, y), (x, 0 if corner in ("tr", "tl") else Ht), "s"))
    return render([(pts, FILL)], CL + " (L-shape)", lines, labels=lab, maxw=230, maxh=125)


def house_svg(w, a, r, u, total=False):
    pts = [(0, 0), (w, 0), (w, a), (Fr(w, 2), a + r), (0, a)]
    top = (Fr(w, 2), a + r)
    lines = [((0, a), (w, a), "s")]
    if total:
        lines.append((top, (Fr(w, 2), 0), "h"))
        rights = [((Fr(w, 2), 0), (w, 0), top)]
        hl = (top, (Fr(w, 2), 0), "%s %s" % (num(a + r), u), None)
    else:
        lines += [(top, (Fr(w, 2), a), "h"), (top, (w, a + r), "x"), ((w, a + r), (w, a), "x")]
        rights = [((Fr(w, 2), a), (w, a), top)]
        hl = ((w, a + r), (w, a), "%s %s" % (num(r), u), "right")
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts), hl]
    return render([(pts, FILL)], CL + " (house shape)", lines, rights, labels, maxw=200, maxh=125)


def arrow_svg(w, a, t, u, mirror):
    """Rectangle w by a with a triangle (base a, height t) on its right side. The triangle's height t is shown
    by the red dashed line, and measured on a grey dashed extension of the bottom side."""
    pts = [(0, 0), (w, 0), (w + t, Fr(a, 2)), (w, a), (0, a)]
    lines = [((w, 0), (w, a), "s"), ((w, Fr(a, 2)), (w + t, Fr(a, 2)), "h"),
             ((w, 0), (w + t, 0), "x"), ((w + t, 0), (w + t, Fr(a, 2)), "x")]
    rights = [((w, Fr(a, 2)), (w + t, Fr(a, 2)), (w, a))]
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts),
              ((w, 0), (w + t, 0), "%s %s" % (num(t), u), "down")]
    return render([(pts, FILL)], CL + " (rectangle and triangle)", lines, rights, labels, mirror=mirror, maxw=230, maxh=110)


def corner_svg(w, a, d, c, u, mirror):
    """Rectangle w by a with a right triangle (legs d across, c down) cut off its top right corner.
    The cut-off corner is outlined with grey dashed lines."""
    pts = [(0, 0), (w, 0), (w, a - c), (w - d, a), (0, a)]
    lines = [((w - d, a), (w, a), "x"), ((w, a), (w, a - c), "x")]
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts),
              ((w - d, a), (w, a), "%s %s" % (num(d), u), "up"), ((w, a), (w, a - c), "%s %s" % (num(c), u), "right")]
    return render([(pts, FILL)], CL + " (rectangle with a corner cut off)", lines, labels=labels, mirror=mirror,
                  maxw=220, maxh=110)


def rtrap_split_svg(w, t, a, u, mirror):
    """Rectangle w by a with a right triangle (legs t and a) on its right: a right trapezoid."""
    pts = [(0, 0), (w + t, 0), (w, a), (0, a)]
    lines = [((w, a), (w, 0), "s")]
    rights = [((0, 0), (1, 0), (0, 1)), ((w, 0), (w + t, 0), (w, a))]
    labels = [((0, 0), (w + t, 0), "%s %s" % (num(w + t), u), pts), ((w, a), (0, a), "%s %s" % (num(w), u), pts),
              ((0, a), (0, 0), "%s %s" % (num(a), u), pts)]
    return render([(pts, FILL)], CL + " (rectangle and right triangle)", lines, rights, labels, mirror=mirror,
                  maxw=230, maxh=110)


def hex_svg(w, a, t, u):
    """Rectangle w by a with a triangle (base a, height t) on each end."""
    pts = [(t, 0), (t + w, 0), (2 * t + w, Fr(a, 2)), (t + w, a), (t, a), (0, Fr(a, 2))]
    lines = [((t, 0), (t, a), "s"), ((t + w, 0), (t + w, a), "s"), ((t + w, Fr(a, 2)), (2 * t + w, Fr(a, 2)), "h"),
             ((t + w, 0), (2 * t + w, 0), "x"), ((2 * t + w, 0), (2 * t + w, Fr(a, 2)), "x")]
    rights = [((t + w, Fr(a, 2)), (2 * t + w, Fr(a, 2)), (t + w, a))]
    labels = [((t, 0), (t + w, 0), "%s %s" % (num(w), u), pts), ((t, a), (t, 0), "%s %s" % (num(a), u), "right"),
              ((t + w, 0), (2 * t + w, 0), "%s %s" % (num(t), u), "down")]
    return render([(pts, FILL)], CL + " (hexagon)", lines, rights, labels, maxw=240, maxh=110)


# integer right triangles (d across, h up, s slanted)
TRIPLES = sorted({(d, h, int(math.isqrt(d * d + h * h))) for d in range(1, 41) for h in range(1, 41)
                  if math.isqrt(d * d + h * h) ** 2 == d * d + h * h})


def by_h():
    out = {}
    for d, h, s in TRIPLES:
        out.setdefault(h, []).append((d, s))
    return out


def hx(b, h):
    """½ × b × h = ½ × bh."""
    return "%s × %s × %s = %s × %s" % (HALF, num(b), num(h), HALF, num(b * h))


def trap2_svg(b1, b2, o, h, l1, l2, lh, lleg, mirror=False, flip=False, label="trapezoid cut into a rectangle and triangles"):
    """Bottom b1, top b2 starting at x = o. Dashed heights drop from both top corners (where they are inside),
    cutting the trapezoid into a rectangle and one or two triangles."""
    pts = [(0, 0), (b1, 0), (o + b2, h), (o, h)]
    labels = [((0, 0), (b1, 0), l1, pts), ((o + b2, h), (o, h), l2, pts)]
    lines, rights = [], []
    if o > 0:
        lines.append(((o, h), (o, 0), "h"))
        rights.append(((o, 0), (b1, 0), (o, h)))
        labels.append(((o, h), (o, 0), lh, None))
        if lleg:
            labels.append(((0, 0), (o, h), lleg, pts))
    else:
        rights += [((0, 0), (b1, 0), (0, h)), ((0, h), (b2, h), (0, 0))]
        labels.append(((0, h), (0, 0), lh, pts))
    if o + b2 < b1:
        lines.append(((o + b2, h), (o + b2, 0), "h"))
        rights.append(((o + b2, 0), (0, 0), (o + b2, h)))
    return render([(pts, FILL)], label, lines, rights, labels, mirror=mirror, flip=flip, maxw=210, maxh=100)


def trapd_svg(b1, b2, o, h, l1, l2, lh, mirror=False, label="trapezoid cut into two triangles by a diagonal"):
    """A dashed diagonal from the top left corner to the bottom right corner makes two triangles."""
    pts = [(0, 0), (b1, 0), (o + b2, h), (o, h)]
    labels = [((0, 0), (b1, 0), l1, pts), ((o + b2, h), (o, h), l2, pts)]
    lines, rights = [((o, h), (b1, 0), "s")], []
    if o > 0:
        lines.append(((o, h), (o, 0), "h"))
        rights.append(((o, 0), (b1, 0), (o, h)))
        labels.append(((o, h), (o, 0), lh, None))
    else:
        rights += [((0, 0), (b1, 0), (0, h)), ((0, h), (b2, h), (0, 0))]
        labels.append(((0, h), (0, 0), lh, pts))
    return render([(pts, FILL)], label, lines, rights, labels, mirror=mirror, maxw=210, maxh=100)


def kite_svg(w, t, s, u, split=True, label="kite with its diagonals"):
    """Kite (or rhombus when t == s): horizontal diagonal w; the vertical diagonal is t above it and s below it.
    Lengths are shown with dimension lines: w below the figure, t and s (or t + s) on the right."""
    k = min(140.0 / w, 100.0 / (t + s))
    if split and min(t, s) * k < 26:
        return None
    W0, H0 = w * k, (t + s) * k
    pad = 6
    ox, oy = pad, pad
    cx, cy = ox + W0 / 2, oy + t * k
    T, R, B, L = (cx, oy), (ox + W0, cy), (cx, oy + H0), (ox, cy)
    yd = oy + H0 + 14
    xd = ox + W0 + 14
    s_ = []
    s_.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
              % (" ".join("%.1f,%.1f" % p for p in (T, R, B, L)), FILL, GREEN))
    for a, b in ((L, R), (T, B)):
        s_.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-dasharray='7 5'/>"
                  % (a[0], a[1], b[0], b[1], RED))
    s_.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
              % (cx + 9, cy, cx + 9, cy - 9, cx, cy - 9, INK))

    def ln(x1, y1, x2, y2, dash):
        s_.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s/>"
                  % (x1, y1, x2, y2, GRAY if dash else INK, 1 if dash else 1.5,
                     " stroke-dasharray='3 3'" if dash else ""))
    # bottom dimension line (w)
    ln(L[0], L[1] + 6, L[0], yd + 5, True)
    ln(R[0], R[1] + 6, R[0], yd + 5, True)
    ln(ox, yd, ox + W0, yd, False)
    for x in (ox, ox + W0):
        ln(x, yd - 6, x, yd + 6, False)
    txt = [(cx, yd + 22, "middle", "%s %s" % (num(w), u))]
    # right dimension line (t and s, or t + s)
    ys = [oy, cy, oy + H0] if split else [oy, oy + H0]
    ln(T[0] + 6, T[1], xd + 5, T[1], True)
    ln(B[0] + 6, B[1], xd + 5, B[1], True)
    if split:
        ln(R[0] + 6, R[1], xd + 5, R[1], True)
    ln(xd, oy, xd, oy + H0, False)
    for y in ys:
        ln(xd - 6, y, xd + 6, y, False)
    if split:
        txt += [(xd + 10, (oy + cy) / 2 + 6, "start", "%s %s" % (num(t), u)),
                (xd + 10, (cy + oy + H0) / 2 + 6, "start", "%s %s" % (num(s), u))]
    else:
        txt.append((xd + 10, oy + H0 / 2 + 6, "start", "%s %s" % (num(t + s), u)))
    lw = max(tw(x[3], FS) for x in txt[1:])
    for x, y, anc, t_ in txt:
        s_.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                  % (x, y, FS, INK, anc, t_))
    W = int(math.ceil(max(xd + 10 + lw, cx + tw(txt[0][3], FS) / 2) + pad))
    H = int(math.ceil(yd + 22 + 5 + pad))
    return svg_wrap(W, H, "".join(s_), label)


# ------------------------------------------------------------ set 1: parallelograms
def set_para(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] <= 12 and 3 <= t[1] <= 16 and t[0] / t[1] <= 1.4]
    rnd.shuffle(tr)
    for i in range(8):
        u, su = UNITS[i % 4]
        svg = None
        while not svg:
            o, h, s = tr.pop()
            bs = [b for b in range(max(o + 3, 6), 19) if b not in (s, h) and b / h <= 3.2 and ("pa", b, h) not in seen]
            rnd.shuffle(bs)
            for b in bs[:4]:
                svg = para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i % 3 == 1)
                if svg:
                    break
        seen.add(("pa", b, h))
        A = b * h
        q = fig(svg) + "What is the area of the parallelogram?"
        e = ("A = base × height = %d × %d = %s %s. The height is the dashed line at a right angle to the base, "
             "not the slanted %d %s side." % (b, h, num(A), su, s, u))
        if i < 3:
            e += (" (Cut off the triangle at one end and slide it to the other end: you get a rectangle that is "
                  "%d by %d.)" % (b, h))
        its.append(mcq(q, ar(A, su), [ar(b * s, su), ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + s), su)], e, rnd))
    # rhombuses (all four sides equal)
    rh = [t for t in TRIPLES if 3 <= t[0] <= 12 and 4 <= t[1] <= 16 and t[2] <= 17 and t[0] < t[1]]
    rnd.shuffle(rh)
    for i in range(2):
        u, su = UNITS[i + 1]
        while True:
            o, h, s = rh.pop()
            svg = para_svg(s, o, h, "%d %s" % (s, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 1,
                           label="rhombus with its height")
            if svg and ("pa", s, h) not in seen:
                break
        seen.add(("pa", s, h))
        A = s * h
        q = fig(svg) + "This rhombus has four sides of %d %s. What is its area?" % (s, u)
        e = ("A rhombus is a parallelogram, so A = base × height = %d × %d = %s %s. "
             "%d × %d uses a slanted side, not the height." % (s, h, num(A), su, s, s))
        its.append(mcq(q, ar(A, su), [ar(s * s, su), ar(Fr(A, 2), su), ar(4 * s, su), ar(A, u)], e, rnd))
    # cut and slide into a rectangle
    for i, (b, o, h, s, u) in enumerate([(14, 6, 8, 10, "cm"), (10, 5, 12, 13, "m")]):
        svg = must(para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 1))
        q = (fig(svg) + "Cut along the dashed height and slide the triangle to the other end of the parallelogram. "
             "What rectangle do you get?")
        right = "%d %s by %d %s" % (b, u, h, u)
        e = ("The base stays %d %s and the height stays %d %s, so the rectangle is %d %s by %d %s. "
             "That is why the parallelogram’s area is b × h = %d × %d = %d %s²." % (b, u, h, u, b, u, h, u, b, h, b * h, u))
        its.append(mcq(q, right, ["%d %s by %d %s" % (b, u, s, u), "%d %s by %d %s" % (b + o, u, h, u),
                                  "%d %s by %d %s" % (o, u, h, u)], e, rnd))
    q = ("A rectangle is 9 cm by 6 cm. A parallelogram has a base of 9 cm, a height of 6 cm and slanted sides of 7.5 cm. "
         "How do their areas compare?")
    e = ("Rectangle: 9 × 6 = 54 cm². Parallelogram: base × height = 9 × 6 = 54 cm². Same base and same height give "
         "the same area. (9 × 7.5 = 67.5 uses the slanted side.)")
    its.append(mcq(q, "They have the same area.", ["The parallelogram is larger.", "The rectangle is larger.",
                                                  "The parallelogram is half as large."], e, rnd))
    for b, h, u, su in [(Fr(17, 2), 6, "m", "m²"), (14, Fr(23, 2), "cm", "cm²"), (Fr(15, 2), Fr(21, 5), "m", "m²")]:
        A = b * h
        q = "A parallelogram has a base of %s %s and a height of %s %s. What is its area?" % (num(b), u, num(h), u)
        e = ("A = base × height = %s × %s = %s %s. No %s here: a parallelogram is a rectangle with one end "
             "cut off and moved." % (num(b), num(h), num(A), su, HALF))
        its.append(mcq(q, ar(A, su), [ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + h), su), ar(b + h, su)], e, rnd))
    q = "A parallelogram has an area of 96 m². Its base is 12 m. What is its height?"
    e = "Area = base × height, so 12 × ? = 96. 96 ÷ 12 = 8 m. Check: 12 × 8 = 96."
    its.append(mcq(q, "8 m", ["16 m", "84 m", "8 m²", "4 m"], e, rnd))
    q = "A parallelogram has an area of 135 cm². Its height is 9 cm. How long is its base?"
    e = "Area = base × height, so ? × 9 = 135. 135 ÷ 9 = 15 cm. Check: 15 × 9 = 135."
    its.append(mcq(q, "15 cm", ["30 cm", "126 cm", "15 cm²"], e, rnd))
    for i, (b, o, h, s, u) in enumerate([(11, 9, 12, 15, "cm"), (15, 5, 12, 13, "m")]):
        svg = must(para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 0))
        q = fig(svg) + "Which expression gives the area of the parallelogram?"
        right = "%d × %d" % (b, h)
        wrong = ["%d × %d" % (b, s), "%s × %d × %d" % (HALF, b, h), "2 × (%d + %d)" % (b, s)]
        e = ("Area = base × height = %s = %d %s². %d is the slanted side, %s is for triangles, "
             "and 2 × (%d + %d) is the perimeter." % (right, b * h, u, s, HALF, b, s))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallelograms: A = b × h", "items": its}


# ------------------------------------------------------------ set 2: triangles
def tri_options():
    """Triangles whose base, height and slanted sides are exact: two integer right triangles
    (or halves of them) that share the height."""
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
                    obtuse.add((b, d2, h, s2, s1))   # base, top x, height, left side, right side
    return sorted(acute), sorted(obtuse)


def set_tri(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] < t[1] <= 24 and t[1] / t[0] <= 3 and t[0] >= 3]
    rnd.shuffle(tr)
    for i in range(4):
        u, su = UNITS[i % 4]
        while True:
            a, b, c = tr.pop()
            if rnd.random() < 0.5:
                a, b = b, a
            svg = right_tri_svg(a, b, "%d %s" % (a, u), "%d %s" % (b, u), "%d %s" % (c, u), i % 4)
            if svg:
                break
        A = Fr(a * b, 2)
        q = fig(svg) + "What is the area of the right triangle?"
        e = ("The two sides that meet at the right angle are the base and the height. A = %s = %s %s. "
             "The %d %s side is slanted, so it is not the height." % (hx(a, b), num(A), su, c, u))
        its.append(mcq(q, ar(A, su), [ar(a * b, su), ar(Fr(max(a, b) * c, 2), su), ar(A, u), ar(a + b + c, su)], e, rnd))
    for i in range(2):
        u, su = UNITS[(i + 1) % 4]
        while True:
            L, W = rnd.randint(6, 16), rnd.randint(3, 10)
            if L <= W or L / W > 3 or ("hr", L, W) in seen:
                continue
            break
        seen.add(("hr", L, W))
        q = (fig(must(half_rect_svg(L, W, u, i % 2))) +
             "A diagonal cuts this rectangle into two equal triangles. What is the area of the shaded triangle?")
        A = Fr(L * W, 2)
        e = ("The rectangle is %d × %d = %d %s. The shaded triangle is half of it: %d ÷ 2 = %s %s."
             % (L, W, L * W, su, L * W, num(A), su))
        its.append(mcq(q, ar(A, su), [ar(L * W, su), ar(A, u), ar(2 * (L + W), su), ar(L + W, su)], e, rnd))
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    used_bh = set()
    for i in range(6):
        u, su = UNITS[i % 4]
        pool = obtuse if i % 2 else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            if (b, h) in used_bh:
                continue
            side = "L" if i % 2 else rnd.choice("LR")
            s = sl if side == "L" else sr
            if Fr(b * s, 2) == Fr(b * h, 2) or s == b:
                continue
            mir, flp = rnd.random() < 0.5, i == 4
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(s, u), side), mir, flp,
                          label="obtuse triangle with its height outside" if i % 2 else "triangle with its height")
            if svg:
                break
        used_bh.add((b, h))
        A = Fr(b * h, 2)
        q = fig(svg) + "What is the area of the triangle?"
        e = ("The height is the dashed line: it meets the base at a right angle. A = %s × base × height = %s = %s %s. "
             "The %s %s side is slanted, so it is not the height." % (HALF, hx(b, h), num(A), su, num(s), u))
        if i % 2:
            e += " This triangle has an obtuse angle, so its height falls outside it and meets the grey dashed extension of the base."
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(Fr(b * s, 2), su), ar(A, u), ar(b * s, su)], e, rnd))
    for b, h, u, su in [(Fr(15, 2), 4, "m", "m²"), (12, Fr(13, 2), "cm", "cm²"), (15, Fr(42, 5), "cm", "cm²")]:
        A = Fr(b * h, 2)
        q = "A triangle has a base of %s %s and a height of %s %s. What is its area?" % (num(b), u, num(h), u)
        e = "A = %s = %s %s. Do not forget the %s: a triangle is half of a parallelogram." % (hx(b, h), num(A), su, HALF)
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(A, u), ar(b + h, su)], e, rnd))
    for A, k, u, su, what, other in [(36, 9, "cm", "cm²", "base", "height"), (42, 7, "m", "m²", "height", "base")]:
        o = Fr(2 * A, k)
        q = "A triangle has an area of %d %s. Its %s is %d %s. What is its %s?" % (A, su, what, k, u, other)
        e = ("%s × %d × ? = %d. Double the area first: %d × 2 = %d. Then %d ÷ %d = %s %s. Check: %s = %d %s."
             % (HALF, k, A, A, 2 * A, 2 * A, k, num(o), u, hx(k, o), A, su))
        its.append(mcq(q, ar(o, u), [ar(Fr(A, k), u), ar(A - k, u), ar(o, su), ar(Fr(A, 2), u)], e, rnd))
    for i in range(2):
        u = ["m", "cm"][i]
        while True:
            b, p, h, sl, sr = obtuse.pop()
            if (b, h) in used_bh or sl == b:
                continue
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(sl, u), "L"), i == 1, False,
                          label="obtuse triangle with its height outside")
            if svg:
                break
        used_bh.add((b, h))
        q = fig(svg) + "Which expression gives the area of the triangle?"
        right = "%s × %d × %d" % (HALF, b, h)
        wrong = ["%s × %d × %s" % (HALF, b, num(sl)), "%d × %d" % (b, h), "%s × %s × %d" % (HALF, num(sl), h)]
        e = ("The base is %d %s. The height is the dashed %d %s line, which meets the base line at a right angle "
             "outside the triangle. A = %s = %s %s²." % (b, u, h, u, right, num(Fr(b * h, 2)), u))
        its.append(mcq(q, right, wrong, e, rnd))
    q = ("A parallelogram and a triangle have the same base (14 cm) and the same height (9 cm). "
         "The parallelogram’s area is 126 cm². What is the triangle’s area?")
    e = ("Two copies of the triangle make a parallelogram with the same base and height, so the triangle is half of it: "
         "126 ÷ 2 = 63 cm². Check: %s = 63." % hx(14, 9))
    its.append(mcq(q, "63 cm²", ["126 cm²", "252 cm²", "63 cm"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Triangles: A = ½ × b × h", "items": its}


# ------------------------------------------------------------ set 3: trapezoids, rhombuses and kites
def set_decomp(rnd, seen):
    its = []
    H = by_h()
    kinds = ["iso", "gen", "iso", "right", "iso", "gen"]
    for i, kind in enumerate(kinds):
        u, su = UNITS[(i + 1) % 4]
        while True:
            leg = None
            b2 = rnd.randint(3, 12)
            if kind == "iso":
                h = rnd.choice([x for x in sorted(H) if 3 <= x <= 12 and any(t[0] <= 8 for t in H[x])])
                d, leg = rnd.choice([t for t in H[h] if t[0] <= 8])
                o, b1 = d, b2 + 2 * d
            elif kind == "right":
                h = rnd.randint(3, 10)
                o, b1 = 0, b2 + rnd.randint(2, 8)
            else:
                h = rnd.randint(3, 10)
                o, o2 = rnd.randint(1, 5), rnd.randint(1, 5)
                if o == o2:
                    continue
                b1 = b2 + o + o2
            if b1 / h > 3.5 or b1 > 26 or ("tz", b1, b2, h) in seen or leg in (b1, b2, h) or (b1 - b2) % 2 and h % 2:
                continue
            svg = trap2_svg(b1, b2, o, h, "%d %s" % (b1, u), "%d %s" % (b2, u), "%d %s" % (h, u),
                            "%d %s" % (leg, u) if leg else "", mirror=i % 2 == 1, flip=i == 4)
            if svg:
                break
        seen.add(("tz", b1, b2, h))
        R, D = b2 * h, b1 - b2
        T = Fr(D * h, 2)
        A = R + T
        assert A == Fr((b1 + b2) * h, 2)
        q = fig(svg) + "The dashed lines cut the trapezoid into a rectangle and %s. What is its area?" % (
            "a triangle" if kind == "right" else "two triangles")
        if kind == "right":
            e = ("Rectangle: %d × %d = %d %s. Triangle: base %d − %d = %d %s, height %d %s, so %s = %s %s. "
                 "Add: %d + %s = %s %s." % (b2, h, R, su, b1, b2, D, u, h, u, hx(D, h), num(T), su, R, num(T), num(A), su))
        else:
            e = ("Rectangle: %d × %d = %d %s. The two triangles have the same height (%d %s), and their bases add up to "
                 "%d − %d = %d %s. Together: %s = %s %s. Add: %d + %s = %s %s."
                 % (b2, h, R, su, h, u, b1, b2, D, u, hx(D, h), num(T), su, R, num(T), num(A), su))
        cands = [ar(b1 * h, su), ar((b1 + b2) * h, su)]
        if leg:
            e += " The %d %s side is slanted, so it is not the height." % (leg, u)
            cands.append(ar(Fr((b1 + b2) * leg, 2), su))
        cands += [ar(R, su), ar(A, u)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    for i, (b1, b2, o, h, u, su) in enumerate([(13, 7, 0, 6, "m", "m²"), (16, 9, 4, 8, "cm", "cm²")]):
        svg = must(trapd_svg(b1, b2, o, h, "%d %s" % (b1, u), "%d %s" % (b2, u), "%d %s" % (h, u), mirror=i == 1))
        T1, T2 = Fr(b1 * h, 2), Fr(b2 * h, 2)
        A = T1 + T2
        q = fig(svg) + "The dashed diagonal cuts the trapezoid into two triangles. What is its area?"
        e = ("Bottom triangle: base %d %s, height %d %s: %s = %s %s. Top triangle: base %d %s (the top side), same "
             "height: %s = %s %s. Add: %s + %s = %s %s." % (b1, u, h, u, hx(b1, h), num(T1), su, b2, u, hx(b2, h),
                                                         num(T2), su, num(T1), num(T2), num(A), su))
        its.append(mcq(q, ar(A, su), [ar((b1 + b2) * h, su), ar(T1, su), ar(b1 * h, su), ar(A, u)], e, rnd))
    # kites
    kites = [(w, t, s) for w in range(6, 21) for t in range(2, 10) for s in range(t + 2, 19)
             if s <= 2.6 * t and 0.6 <= w / (t + s) <= 1.6]
    rnd.shuffle(kites)
    for i in range(5):
        u, su = UNITS[i % 4]
        split = i < 3
        while True:
            w, t, s = kites.pop()
            if ("kt", w, t + s) in seen or (not split and (w * (t + s)) % 2):
                continue
            svg = kite_svg(w, t, s, u, split)
            if svg:
                break
        seen.add(("kt", w, t + s))
        d = t + s
        A = Fr(w * d, 2)
        if split:
            T1, T2 = Fr(w * t, 2), Fr(w * s, 2)
            q = fig(svg) + "The horizontal diagonal cuts the kite into two triangles. What is the area of the kite?"
            e = ("Both triangles have the %d %s diagonal as their base. Top: %s = %s %s. Bottom: %s = %s %s. "
                 "Add: %s + %s = %s %s." % (w, u, hx(w, t), num(T1), su, hx(w, s), num(T2), su, num(T1), num(T2), num(A), su))
            cands = [ar(w * d, su), ar(T2, su), ar(T1, su), ar(A, u)]
        else:
            q = fig(svg) + "The diagonals of the kite are %d %s and %d %s. What is its area?" % (w, u, d, u)
            e = ("The kite fits inside a rectangle that is %d by %d and fills exactly half of it (its two triangles are each half "
                 "of a smaller rectangle). %s = %s %s." % (w, d, hx(w, d), num(A), su))
            cands = [ar(w * d, su), ar(A, u), ar(2 * (w + d), su), ar(Fr(w * d, 4), su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # rhombuses with diagonals
    for i, (d1, d2, u, su) in enumerate([(16, 12, "cm", "cm²"), (10, 14, "m", "m²"), (18, 8, "mm", "mm²")]):
        svg = must(kite_svg(d1, d2 // 2, d2 // 2, u, False, label="rhombus with its diagonals"))
        A = Fr(d1 * d2, 2)
        q = fig(svg) + "What is the area of the rhombus?"
        e = ("The diagonals cut the rhombus into 4 equal right triangles. It fills half of the %d by %d rectangle "
             "around it: %s = %s %s." % (d1, d2, hx(d1, d2), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(d1 * d2, su), ar(Fr(d1 * d2, 4), su), ar(A, u), ar(2 * (d1 + d2), su)], e, rnd))
    for b1, b2, h, u, su in [(12, Fr(15, 2), 4, "m", "m²"), (Fr(21, 2), Fr(11, 2), 7, "cm", "cm²")]:
        T1, T2 = Fr(b1 * h, 2), Fr(b2 * h, 2)
        A = T1 + T2
        q = ("A trapezoid has parallel sides of %s %s and %s %s. The distance between them (the height) is %s %s. "
             "A diagonal cuts it into two triangles. What is its area?" % (num(b1), u, num(b2), u, num(h), u))
        e = ("Each triangle has one of the parallel sides as its base and the same height. %s = %s and %s = %s. "
             "Add: %s + %s = %s %s." % (hx(b1, h), num(T1), hx(b2, h), num(T2), num(T1), num(T2), num(A), su))
        its.append(mcq(q, ar(A, su), [ar((b1 + b2) * h, su), ar(b1 * h, su), ar(A, u), ar(b1 * b2 * h, su)], e, rnd))
    # which expression
    w, t, s, u = 12, 4, 9, "cm"
    svg = must(kite_svg(w, t, s, u, True))
    q = fig(svg) + "Which expression gives the area of the kite?"
    right = "%s × %d × %d + %s × %d × %d" % (HALF, w, t, HALF, w, s)
    wrong = ["%d × (%d + %d)" % (w, t, s), "%s × %d × %d" % (HALF, w, s), "%d × %d + %s × %d × %d" % (w, t, HALF, w, s)]
    e = ("Two triangles share the %d cm diagonal as their base. Their heights are %d cm and %d cm. "
         "%s = 24 + 54 = 78 cm². %d × (%d + %d) forgets the %s." % (w, t, s, right, w, t, s, HALF))
    its.append(mcq(q, right, wrong, e, rnd))
    b1, b2, d, h, leg, u = 14, 6, 4, 3, 5, "m"
    svg = must(trap2_svg(b1, b2, d, h, "%d %s" % (b1, u), "%d %s" % (b2, u), "%d %s" % (h, u), "%d %s" % (leg, u)))
    q = fig(svg) + "Which expression gives the area of the trapezoid?"
    right = "%d × %d + %s × %d × %d" % (b2, h, HALF, b1 - b2, h)
    wrong = ["%d × %d + %d × %d" % (b2, h, b1 - b2, h), "(%d + %d) × %d" % (b1, b2, h),
             "%d × %d + %s × %d × %d" % (b2, leg, HALF, b1 - b2, leg)]
    e = ("Rectangle %d × %d = 18 m², plus the two triangles together: %s × %d × %d = 12 m² (their bases add up to "
         "%d − %d = %d m). Total 30 m². The %d m side is slanted, so it is not the height."
         % (b2, h, HALF, b1 - b2, h, b1, b2, b1 - b2, leg))
    assert b2 * h == 18 and Fr((b1 - b2) * h, 2) == 12
    its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Trapezoids, rhombuses and kites: split into triangles and rectangles", "items": its}


# ------------------------------------------------------------ set 4: composite figures
def pick_l(rnd, used):
    while True:
        Wt, Ht = rnd.randint(9, 16), rnd.randint(6, 12)
        if Wt <= Ht or Wt / Ht > 2:
            continue
        cw = rnd.randint(int(math.ceil(Wt * 0.4)), int(Wt * 0.6))
        ch = rnd.randint(int(math.ceil(Ht * 0.4)), int(Ht * 0.6))
        if cw == Wt - cw or ch == Ht - ch or (Wt, Ht, cw, ch) in used:
            continue
        used.add((Wt, Ht, cw, ch))
        return Wt, Ht, cw, ch


def set_composite(rnd):
    its = []
    used = set()
    corners = ["tr", "tl", "br", "bl"]
    # L-shapes: split, cut, and two with hidden sides
    for i, kind in enumerate(["split", "split", "cut", "cut", "hidden", "hidden"]):
        u, su = UNITS[i % 4]
        while True:
            Wt, Ht, cw, ch = pick_l(rnd, used)
            corner = corners[i % 4]
            sides = [Wt - cw, ch, cw, Ht - ch, Wt, Ht]
            labels = ["%d %s" % (v, u) for v in sides]
            if kind == "hidden":
                labels[1] = labels[2] = ""
            svg = l_svg(Wt, Ht, cw, ch, corner, labels, kind == "split")
            if svg:
                break
        A = Wt * Ht - cw * ch
        A1, A2 = (Wt - cw) * Ht, cw * (Ht - ch)
        split_e = ("Split it into two rectangles: %d × %d = %d and %d × %d = %d. Add: %d + %d = %d %s."
                   % (Wt - cw, Ht, A1, cw, Ht - ch, A2, A1, A2, A, su))
        cut_e = ("Whole rectangle %d × %d = %d, minus the missing corner %d × %d = %d: %d − %d = %d %s."
                 % (Wt, Ht, Wt * Ht, cw, ch, cw * ch, Wt * Ht, cw * ch, A, su))
        over = (Wt - cw) * Ht + Wt * (Ht - ch)
        if kind == "split":
            q = fig(svg) + "The dashed line splits the figure into two rectangles. What is the area of the figure?"
            e = split_e
        elif kind == "cut":
            q = fig(svg) + "What is the area of the figure?"
            e = cut_e + " Or: " + split_e[0].lower() + split_e[1:]
        else:
            q = fig(svg) + "What is the area of the figure? Find the two missing side lengths first."
            e = ("Missing sides: %d − %d = %d and %d − %d = %d. " % (Wt, Wt - cw, cw, Ht, Ht - ch, ch)) + cut_e
        cands = [ar(over, su), ar(Wt * Ht, su), ar(A, u), ar(2 * (Wt + Ht), su)]
        if kind == "split":
            e += (" Use each part of the figure once: %d × %d + %d × %d = %d counts the %d × %d corner twice."
                  % (Wt - cw, Ht, Wt, Ht - ch, over, Wt - cw, Ht - ch))
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # houses
    for i in range(4):
        u, su = UNITS[(i + 1) % 4]
        total = i >= 2
        while True:
            w = rnd.choice([6, 8, 10, 12, 14, 16])
            a, r = rnd.randint(4, 10), rnd.randint(3, 7)
            if ("ho", w, a, r) in used or r == a:
                continue
            svg = house_svg(w, a, r, u, total)
            if svg:
                break
        used.add(("ho", w, a, r))
        R, T = w * a, Fr(w * r, 2)
        A = R + T
        if total:
            q = fig(svg) + "The figure is a rectangle with a triangle on top. What is its area?"
            e = ("The triangle is %d − %d = %d %s tall. Rectangle: %d × %d = %d %s. Triangle: %s = %s %s. "
                 "Add: %d + %s = %s %s." % (a + r, a, r, u, w, a, R, su, hx(w, r), num(T), su, R, num(T), num(A), su))
            cands = [ar(R + Fr(w * (a + r), 2), su), ar(R + w * r, su), ar(w * (a + r), su), ar(A, u)]
        else:
            q = fig(svg) + "The figure is a rectangle with a triangle on top. What is its area?"
            e = ("Rectangle: %d × %d = %d %s. Triangle: %s = %s %s. Add: %d + %s = %s %s."
                 % (w, a, R, su, hx(w, r), num(T), su, R, num(T), num(A), su))
            cands = [ar(R + w * r, su), ar(w * (a + r), su), ar(A, u), ar(R, su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # rectangle + triangle on the side (arrow)
    for i in range(3):
        u, su = UNITS[(i + 2) % 4]
        while True:
            w, a, t = rnd.randint(6, 14), rnd.choice([4, 6, 8, 10]), rnd.randint(3, 8)
            if ("ar", w, a, t) in used or t >= w or w * a == a * t:
                continue
            svg = arrow_svg(w, a, t, u, mirror=i == 1)
            if svg:
                break
        used.add(("ar", w, a, t))
        R, T = w * a, Fr(a * t, 2)
        A = R + T
        q = fig(svg) + "What is the area of the figure?"
        e = ("Rectangle: %d × %d = %d %s. Triangle: its base is the %d %s side and its height is %d %s, "
             "so %s = %s %s. Add: %d + %s = %s %s." % (w, a, R, su, a, u, t, u, hx(a, t), num(T), su, R, num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R + a * t, su), ar((w + t) * a, su), ar(A, u), ar(R, su)], e, rnd))
    # rectangle with a corner cut off
    for i in range(3):
        u, su = UNITS[(i + 3) % 4]
        while True:
            w, a = rnd.randint(8, 14), rnd.randint(6, 10)
            d, c = rnd.randint(3, w // 2), rnd.randint(2, a // 2)
            if ("cc", w, a, d, c) in used or d == c or w == a:
                continue
            svg = corner_svg(w, a, d, c, u, mirror=i == 2)
            if svg:
                break
        used.add(("cc", w, a, d, c))
        R, T = w * a, Fr(d * c, 2)
        A = R - T
        q = fig(svg) + "A triangle is cut off the corner of a rectangle (grey dashed lines). What is the area of the shaded figure?"
        e = ("Whole rectangle: %d × %d = %d %s. Cut-off right triangle: %s = %s %s. "
             "Subtract: %d − %s = %s %s." % (w, a, R, su, hx(d, c), num(T), su, R, num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R - d * c, su), ar(R + T, su), ar(R, su), ar(A, u)], e, rnd))
    # right trapezoid split into a rectangle and a triangle
    for i in range(2):
        u, su = UNITS[i % 4]
        while True:
            w, t, a = rnd.randint(5, 12), rnd.randint(3, 8), rnd.randint(4, 9)
            if ("rs", w, t, a) in used:
                continue
            svg = rtrap_split_svg(w, t, a, u, mirror=i == 1)
            if svg:
                break
        used.add(("rs", w, t, a))
        R, T = w * a, Fr(t * a, 2)
        A = R + T
        q = fig(svg) + "The dashed line splits the figure into a rectangle and a triangle. What is its area?"
        e = ("Rectangle: %d × %d = %d %s. The triangle’s base is %d − %d = %d %s and its height is %d %s: "
             "%s = %s %s. Add: %d + %s = %s %s." % (w, a, R, su, w + t, w, t, u, a, u, hx(t, a), num(T), su, R, num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar((w + t) * a, su), ar(R + Fr((w + t) * a, 2), su), ar(A, u), ar(R + t * a, su)], e, rnd))
    # hexagon: rectangle + two triangles
    for i in range(2):
        u, su = UNITS[(i + 1) % 4]
        while True:
            w, a, t = rnd.randint(6, 12), rnd.choice([6, 8, 10]), rnd.randint(3, 5)
            if ("hx", w, a, t) in used:
                continue
            svg = hex_svg(w, a, t, u)
            if svg:
                break
        used.add(("hx", w, a, t))
        R, T = w * a, Fr(a * t, 2)
        A = R + 2 * T
        q = fig(svg) + "The hexagon is a rectangle with two equal triangles. What is its area?"
        e = ("Rectangle: %d × %d = %d %s. Each triangle: base %d %s, height %d %s, so %s = %s %s. "
             "Total: %d + %s + %s = %s %s." % (w, a, R, su, a, u, t, u, hx(a, t), num(T), su, R, num(T), num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R + T, su), ar(R + 2 * a * t, su), ar((w + 2 * t) * a, su), ar(A, u)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Composite polygons: split or subtract", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    n, he, his = P.next()
    add("%s’s family plants a vegetable garden shaped like a parallelogram. Its base is 8 m and its height is 5 m. "
        "The slanted sides are 6 m long. What is the area of the garden?" % n,
        ar(40, "m²"), [ar(48, "m²"), ar(20, "m²"), ar(40, "m")],
        "A = base × height = 8 × 5 = 40 m². The 6 m sides are slanted, so they are not the height.")
    add("A sailboat on Lake Ontario has a sail shaped like a right triangle. The bottom edge is 3 m, the edge along "
        "the mast is 4 m and the slanted edge is 5 m. What is the area of the sail?",
        ar(6, "m²"), [ar(12, "m²"), ar(10, "m²"), ar(Fr(15, 2), "m²")],
        "The bottom edge and the mast meet at a right angle, so they are the base and the height. "
        "A = %s = 6 m². The 5 m edge is slanted." % hx(3, 4))
    n, he, his = P.next()
    one = Fr(30 * 45, 2)
    add("%s’s class makes 20 triangular flags for a Terry Fox Run banner. Each flag has a base of 30 cm and a "
        "height of 45 cm. How much fabric do the flags use in all?" % n,
        ar(20 * one, "cm²"), [ar(20 * 30 * 45, "cm²"), ar(one, "cm²"), ar(20 * one, "cm")],
        "One flag: %s = %s cm². Twenty flags: 20 × %s = %s cm²." % (hx(30, 45), num(one), num(one), num(20 * one)))
    add("A team flag is a rectangle 90 cm long and 60 cm tall. A red triangle on the flag has the 60 cm side as its base "
        "and reaches 45 cm into the flag. The rest is white. What is the area of the white part?",
        ar(5400 - 1350, "cm²"), [ar(5400 - 2700, "cm²"), ar(5400 + 1350, "cm²"), ar(4050, "cm")],
        "Flag: 90 × 60 = 5400 cm². Triangle: %s = 1350 cm². White part: 5400 − 1350 = 4050 cm²." % hx(60, 45))
    add("A garden bed at school is a trapezoid. Its parallel sides are 6 m and 4 m, and they are 3 m apart. "
        "What is its area?", ar(15, "m²"), [ar(30, "m²"), ar(18, "m²"), ar(15, "m")],
        "Cut it with a diagonal into two triangles: %s = 9 and %s = 6. Add: 9 + 6 = 15 m²." % (hx(6, 3), hx(4, 3)))
    add("A triangular flower bed has a base of 8 m and a height of 5 m. One packet of wildflower seeds covers 4 m². "
        "How many packets are needed for the whole bed?", "5 packets", ["10 packets", "20 packets", "40 packets"],
        "Area: %s = 20 m². Packets: 20 ÷ 4 = 5." % hx(8, 5))
    add("A parking space is a parallelogram. It is 2.5 m wide along the curb, and its painted slanted lines are 6 m long. "
        "The distance straight back from the curb is 5.5 m. What is its area?",
        ar(Fr(55, 4), "m²"), [ar(15, "m²"), ar(Fr(55, 8), "m²"), ar(Fr(55, 4), "m")],
        "A = base × height = 2.5 × 5.5 = 13.75 m². The 6 m lines are slanted, so they are not the height.")
    n, he, his = P.next()
    add("%s builds a kite. The two crossed sticks (the diagonals) are 60 cm and 80 cm long. How much paper covers the kite?" % n,
        ar(2400, "cm²"), [ar(4800, "cm²"), ar(1200, "cm²"), ar(2400, "cm")],
        "The kite fills half of the 60 cm by 80 cm rectangle around it: %s = 2400 cm²." % hx(60, 80))
    add("The front wall of a cottage is a rectangle 8 m wide and 3 m tall with a triangle on top that is 2 m tall. "
        "What is the area of the wall?", ar(32, "m²"), [ar(40, "m²"), ar(24, "m²"), ar(32, "m")],
        "Rectangle: 8 × 3 = 24 m². Triangle: %s = 8 m². Total: 24 + 8 = 32 m²." % hx(8, 2))
    n, he, his = P.next()
    add("%s stains a deck shaped like a trapezoid. The parallel sides are 5 m and 3 m, and they are 4 m apart. "
        "Stain costs $6 per square metre. How much does the stain cost?" % n, "$96", ["$192", "$120", "$48"],
        "Cut it with a diagonal into two triangles: ½ × 5 × 4 = 10 m² and ½ × 3 × 4 = 6 m². Add: 10 + 6 = 16 m². Cost: 16 × $6 = $96.".replace("½", HALF))
    add("A backyard rink is an L-shape: a 12 m by 8 m rectangle with a 4 m by 3 m corner left out for a shed. "
        "What is the area of the ice?", ar(84, "m²"), [ar(96, "m²"), ar(108, "m²"), ar(84, "m")],
        "Whole rectangle: 12 × 8 = 96 m². Corner: 4 × 3 = 12 m². Ice: 96 − 12 = 84 m².")
    add("A triangular sail has an area of 12 m². Its base is 4 m. How tall is the sail?", "6 m",
        ["3 m", "8 m", "6 m²"], "%s × 4 × h = 12, so 4 × h = 24. h = 24 ÷ 4 = 6 m." % HALF)
    add("A community garden shaped like a parallelogram has an area of 1200 m². Its base is 40 m. What is its height?",
        "30 m", ["15 m", "60 m", "30 m²"],
        "Area = base × height, so 40 × h = 1200. h = 1200 ÷ 40 = 30 m. (Halving is only for triangles.)")
    add("Triangle A has a base of 10 cm and a height of 8 cm. Parallelogram B has a base of 5 cm and a height of 8 cm. "
        "Which is true?", "They have the same area.", ["A is larger.", "B is larger.", "A is twice as large as B."],
        "A: %s = 40 cm². B: 5 × 8 = 40 cm². Same area. (Forgetting the %s makes A look twice as large.)" % (hx(10, 8), HALF))
    add("A park in Winnipeg is a rectangle 80 m long and 60 m wide. It has a triangular pond with a base of 20 m and a "
        "height of 15 m. The rest of the park is grass. What is the area of the grass?",
        ar(4650, "m²"), [ar(4500, "m²"), ar(4950, "m²"), ar(4650, "m")],
        "Park: 80 × 60 = 4800 m². Pond: %s = 150 m². Grass: 4800 − 150 = 4650 m²." % hx(20, 15))
    add("Students paint a mural on a wall shaped like a trapezoid. The parallel sides are 9 m and 7 m, and they are 5 m "
        "apart. One 1 L can of paint covers 10 m². How many cans do they need?", "4 cans", ["8 cans", "2 cans", "40 cans"],
        "Cut it with a diagonal into two triangles: ½ × 9 × 5 = 22.5 m² and ½ × 7 × 5 = 17.5 m². Add: 22.5 + 17.5 = 40 m². Cans: 40 ÷ 10 = 4.".replace("½", HALF))
    add("A wooden sign is a rectangle 60 cm long and 20 cm tall with a triangle on one end, like an arrow. "
        "The triangle’s base is the 20 cm side, and it sticks out 15 cm. What is the area of the sign?",
        ar(1350, "cm²"), [ar(1500, "cm²"), ar(1200, "cm²"), ar(1350, "cm")],
        "Rectangle: 60 × 20 = 1200 cm². Triangle: %s = 150 cm². Total: 1200 + 150 = 1350 cm²." % hx(20, 15))
    add("A triangular sail has sides of 10 m, 17 m and 21 m. The height to the 21 m side is 8 m. What is its area?",
        ar(84, "m²"), [ar(168, "m²"), ar(Fr(357, 2), "m²"), ar(84, "m")],
        "Use the 21 m side as the base and the 8 m height: A = %s = 84 m². "
        "The 10 m and 17 m sides are slanted, so they are not the height." % hx(21, 8))
    n, he, his = P.next()
    add("%s’s family lays a path with 25 patio stones shaped like rhombuses. Each stone has diagonals of 40 cm and "
        "30 cm. What area do the stones cover?" % n, ar(15000, "cm²"), [ar(30000, "cm²"), ar(600, "cm²"), ar(15000, "cm")],
        "One stone: %s = 600 cm². 25 stones: 25 × 600 = 15%s000 cm²." % (hx(40, 30), NBSP))
    add("A corner lot in Halifax is a right triangle. Its sides along the two streets are 30 m and 40 m, and the back "
        "side is 50 m. What is the area of the lot?", ar(600, "m²"), [ar(1200, "m²"), ar(750, "m²"), ar(1000, "m²")],
        "The two street sides meet at a right angle, so they are the base and the height. A = %s = 600 m². "
        "The 50 m side is slanted." % hx(30, 40))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: gardens, sails and flags", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>The big idea: start from the rectangle</h2>"
        "<p>You know the area of a rectangle: base × height. "
        "Every shape in this unit can be cut apart, or doubled, to make a rectangle. "
        "The <b>height</b> is always measured <b>at a right angle to the base</b>. "
        "It is shown as a dashed line with a small square at the corner.</p>"
        "<h2>Parallelograms: A = b × h</h2>"
        "<p>Cut the triangle off one end and slide it to the other end. The parallelogram becomes a rectangle "
        "with the same base and the same height. A rhombus is a parallelogram too.</p>"
        "<figure class='sn-fig'>" + must(para_svg(12, 6, 8, "12 cm", "8 cm", "10 cm")) +
        "<figcaption>A = 12 × 8 = 96 cm². The slanted 10 cm side is not the height.</figcaption></figure>"
        "<h2>Triangles: A = " + HALF + " × b × h</h2>"
        "<p>Two copies of any triangle make a parallelogram with the same base and height, so a triangle is half of it. "
        "In a right triangle, the two sides that meet at the right angle are the base and the height.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(14, 5, 12, "14 m", "12 m", ("13 m", "L"))) +
        "<figcaption>A = " + HALF + " × 14 × 12 = " + HALF + " × 168 = 84 m².</figcaption></figure>"
        "<p>In a triangle with an obtuse angle, the height can fall <b>outside</b> the triangle. Extend the base with a "
        "dashed line and measure the height to that line.</p>"
        "<h2>Trapezoids and kites: cut them up</h2>"
        "<p>Cut a trapezoid into a rectangle and triangles, or into two triangles with a diagonal. "
        "Find each area and add.</p>"
        "<figure class='sn-fig'>" + must(trap2_svg(20, 8, 6, 8, "20 cm", "8 cm", "8 cm", "10 cm")) +
        "<figcaption>Rectangle 8 × 8 = 64 cm². The triangles’ bases add up to 20 − 8 = 12 cm: "
        + HALF + " × 12 × 8 = 48 cm². Total 64 + 48 = 112 cm². The 10 cm side is slanted.</figcaption></figure>"
        "<p>A diagonal cuts a kite (or a rhombus) into two triangles that share it as their base. "
        "A kite fills exactly half of the rectangle drawn around it, so A = " + HALF + " × diagonal × diagonal.</p>"
        "<figure class='sn-fig'>" + must(kite_svg(12, 4, 9, "cm", True)) +
        "<figcaption>Top " + HALF + " × 12 × 4 = 24 cm². Bottom " + HALF + " × 12 × 9 = 54 cm². "
        "Total 78 cm² (= " + HALF + " × 12 × 13).</figcaption></figure>" +
        ex("Example", "A trapezoid has parallel sides of 9 m and 5 m. They are 4 m apart. Find the area.",
           "Cut it with a diagonal into two triangles. " + HALF + " × 9 × 4 = 18 and " + HALF + " × 5 × 4 = 10. "
           "Add: 18 + 10 = 28.", "28 m²") +
        "<h2>Composite polygons: split or subtract</h2>"
        "<p>Split the figure into rectangles and triangles that do not overlap, then add their areas. "
        "Or start with a big rectangle and subtract the piece that is missing.</p>"
        "<figure class='sn-fig'>" + must(house_svg(12, 7, 5, "m")) +
        "<figcaption>Rectangle 12 × 7 = 84 m². Triangle " + HALF + " × 12 × 5 = 30 m². Total 84 + 30 = 114 m².</figcaption></figure>" +
        ex("Subtract a piece", "A 10 m by 8 m rectangle has a triangle cut out. The triangle has a base of 8 m and a height of 3 m. Find the area left.",
           "Rectangle: 10 × 8 = 80. Triangle: " + HALF + " × 8 × 3 = 12. Subtract: 80 − 12 = 68.", "68 m²") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using the slanted side as the height", "Use the dashed height at a right angle to the base"],
            ["Triangle: 14 × 12 = 168", "Take half: " + HALF + " × 14 × 12 = 84"],
            ["Parallelogram: " + HALF + " × 12 × 8 = 48", "No half for a parallelogram: 12 × 8 = 96"],
            ["Kite: 12 × 13 = 156", "Take half: " + HALF + " × 12 × 13 = 78"],
            ["Counting a corner twice in an L-shape", "Split into pieces that do not overlap"],
            ["Writing 84 m for an area", "Area is in square units: 84 m²"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about area in the Ontario math curriculum?",
     "a": "In Grade 6 (Spatial Sense), students use rectangles to develop the formulas for the area of a parallelogram (A = b × h) and a triangle (A = ½ × b × h), and solve problems with them, including shapes they can split into rectangles and triangles."},
    {"q": "Why do you divide by 2 to find the area of a triangle?",
     "a": "Two copies of the same triangle fit together to make a parallelogram with the same base and height. The triangle is half of it, so its area is ½ × base × height."},
    {"q": "How do you find the area of a trapezoid or a kite in Grade 6?",
     "a": "Cut it into shapes you know. A trapezoid splits into a rectangle and triangles, or into two triangles with a diagonal. A kite splits into two triangles, so its area is ½ × one diagonal × the other."},
    {"q": "Is area on the Grade 6 EQAO math assessment?",
     "a": "Yes. The Grade 6 EQAO math assessment is based on the Ontario curriculum, and Spatial Sense, which includes area of parallelograms, triangles and composite shapes, is one of the strands it covers."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(36812)
    P = People(rnd)
    seen = set()
    sets = [set_para(rnd, seen), set_tri(rnd, seen), set_decomp(rnd, seen), set_composite(rnd), set_story(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert not re.search(r"\d,\d{3}", re.sub(r"<svg.*?</svg>", "", x)), x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "area-of-polygons", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Area of Parallelograms, Triangles, Trapezoids, Kites and Composite Polygons",
        "seo_title": "Grade 6 Area of Polygons Worksheets: Parallelograms, Triangles and Composite Shapes (Free, Answer Key)",
        "short_title": "Area of polygons",
        "domain": "Spatial Sense",
        "standard_code": "Grade 6: Spatial Sense, E2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the area relationships among rectangles, parallelograms, and triangles to develop the formulas for the area of a parallelogram and the area of a triangle, and solve related problems",
        "meta_desc": "Free Grade 6 math worksheets on area for the Ontario curriculum: parallelograms (A = b × h), triangles (A = ½ × b × h), trapezoids, rhombuses and kites split into triangles, composite polygons, and word problems about gardens, sails and flags. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Parallelogram: A = b × h. Triangle: A = ½ × b × h.",
        "key_sub": "The height meets the base at a right angle; a slanted side is not the height. A triangle is half of a parallelogram with the same base and height. Split trapezoids, kites and other polygons into rectangles and triangles, then add. Area is in square units (cm², m²).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(?:%s|kite|rhombus with its diagonals)" % CL)


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
