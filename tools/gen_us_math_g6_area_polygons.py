# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Area of Triangles, Special Quadrilaterals and Polygons (6.G.A.1)
  python tools/gen_us_math_g6_area_polygons.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above with commas, − (U+2212) for minus.
Every figure is drawn to scale from its numbers. Heights are red dashed lines with a right-angle mark;
slanted sides are labeled only with their true lengths (integer triangles), so they can act as distractors.
Areas are written as cm², m², in², ft², yd² everywhere.
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
WHITE = "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
UNITS = [("cm", "cm²"), ("m", "m²"), ("in", "in²"), ("ft", "ft²")]
HALF = "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"


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


def frac(x):
    """Fraction or mixed number in HTML: 9/16, 1 1/8."""
    x = Fr(x)
    if x.denominator == 1:
        return num(x)
    w, r = divmod(x.numerator, x.denominator)
    s = "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (r, x.denominator)
    return ("%d %s" % (w, s)) if w else s


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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px. Commas, periods and spaces are narrow."""
    t = str(t)
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - t.count(" ") * 0.3) * fs * 0.6


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
    lines  = [(p, q, style)]  style: 'h' height (red dashed), 's' split (red dashed), 'x' extension (gray dashed)
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
    straight down to the base line; when p is outside 0..b the base is extended with a gray dashed line.
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
    by the red dashed line, and measured on a gray dashed extension of the bottom side."""
    pts = [(0, 0), (w, 0), (w + t, Fr(a, 2)), (w, a), (0, a)]
    lines = [((w, 0), (w, a), "s"), ((w, Fr(a, 2)), (w + t, Fr(a, 2)), "h"),
             ((w, 0), (w + t, 0), "x"), ((w + t, 0), (w + t, Fr(a, 2)), "x")]
    rights = [((w, Fr(a, 2)), (w + t, Fr(a, 2)), (w, a))]
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts),
              ((w, 0), (w + t, 0), "%s %s" % (num(t), u), "down")]
    return render([(pts, FILL)], CL + " (rectangle and triangle)", lines, rights, labels, mirror=mirror, maxw=230, maxh=110)


def corner_svg(w, a, d, c, u, mirror):
    """Rectangle w by a with a right triangle (legs d across, c down) cut off its top right corner.
    The cut-off corner is outlined with gray dashed lines."""
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


# ------------------------------------------------------------ set 1: right triangles
def hx(b, h):
    """½ × b × h = ½ × bh."""
    return "%s × %s × %s = %s × %s" % (HALF, num(b), num(h), HALF, num(b * h))


def set_right(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] < t[1] <= 24 and t[1] / t[0] <= 3 and t[0] >= 3]
    rnd.shuffle(tr)
    tri_used = []
    for i in range(8):
        u, su = UNITS[i % 4]
        while True:
            if i % 2 == 0:
                a, b, c = tr.pop()
                if rnd.random() < 0.5:
                    a, b = b, a
            else:
                a, b, c = rnd.randint(4, 15), rnd.randint(3, 12), None
                if a == b or max(a, b) / min(a, b) > 2.6:
                    continue
            if ("rt", a, b) in seen or ("rt", b, a) in seen:
                continue
            svg = right_tri_svg(a, b, "%d %s" % (a, u), "%d %s" % (b, u), "%d %s" % (c, u) if c else "", i % 4)
            if svg:
                break
        seen.add(("rt", a, b))
        if c:
            tri_used.append((a, b, c))
        A = Fr(a * b, 2)
        q = fig(svg) + "What is the area of the right triangle?"
        e = ("The two sides that meet at the right angle are the base and the height. "
             "A = %s = %s %s." % (hx(a, b), num(A), su))
        if c:
            e += " The %d %s side is slanted, so it is not the height." % (c, u)
            cands = [ar(a * b, su), ar(Fr(max(a, b) * c, 2), su), ar(A, u), ar(a + b + c, su)]
        else:
            cands = [ar(a * b, su), ar(A, u), ar(a + b, su), ar(2 * (a + b), su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # half of a rectangle
    for i in range(4):
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
    # text: two sides at the right angle / all three sides
    for i, (a, b, u, su) in enumerate([(9, 14, "cm", "cm²"), (7, 11, "ft", "ft²")]):
        A = Fr(a * b, 2)
        q = ("The two sides that meet at the right angle of a right triangle are %d %s and %d %s long. "
             "What is the area of the triangle?" % (a, u, b, u))
        e = "A = %s = %s %s. Do not forget the %s: a triangle is half of a rectangle." % (hx(a, b), num(A), su, HALF)
        its.append(mcq(q, ar(A, su), [ar(a * b, su), ar(A, u), ar(a + b, su)], e, rnd))
    for a, b, c, u, su in [(8, 6, 10, "m", "m²"), (20, 21, 29, "in", "in²")]:
        A = Fr(a * b, 2)
        q = "A right triangle has sides that are %d %s, %d %s and %d %s long. What is its area?" % (a, u, b, u, c, u)
        e = ("The longest side (%d %s) is across from the right angle, so it is slanted. Use the two shorter sides: "
             "A = %s = %s %s." % (c, u, hx(a, b), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(a * b, su), ar(Fr(b * c, 2), su), ar(a + b + c, su), ar(Fr(a * c, 2), su)], e, rnd))
    # which expression?
    picks = [t for t in tr if t[0] * t[1] not in [x[0] * x[1] for x in tri_used]][:2]
    for i, (a, b, c) in enumerate(picks):
        u = UNITS[(i + 2) % 4][0]
        svg = must(right_tri_svg(a, b, "%d %s" % (a, u), "%d %s" % (b, u), "%d %s" % (c, u), (i * 3) % 4))
        q = fig(svg) + "Which expression gives the area of this right triangle?"
        right = "%s × %d × %d" % (HALF, a, b)
        wrong = ["%d × %d" % (a, b), "%s × %d × %d" % (HALF, b, c), "%d + %d + %d" % (a, b, c)]
        e = ("Use the two sides that make the right angle: they are the base and the height. "
             "%s = %s %s². %d × %d forgets the %s, and %d %s is the slanted side."
             % (right, num(Fr(a * b, 2)), u, a, b, HALF, c, u))
        its.append(mcq(q, right, wrong, e, rnd))
    # missing side
    for A, s, u, su in [(30, 5, "ft", "ft²"), (42, 12, "cm", "cm²")]:
        o = Fr(2 * A, s)
        q = ("A right triangle has an area of %d %s. One of the sides that meet at the right angle is %d %s. "
             "How long is the other one?" % (A, su, s, u))
        e = ("%s × %d × ? = %d, so %d × ? = %d × 2 = %d. %d ÷ %d = %s %s. Check: %s = %d."
             % (HALF, s, A, s, A, 2 * A, 2 * A, s, num(o), u, hx(s, o), A))
        its.append(mcq(q, ar(o, u), [ar(Fr(A, s), u), ar(A - s, u), ar(o, su), ar(A * s, u)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of right triangles", "items": its}


# ------------------------------------------------------------ set 2: any triangle (base and height)
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


def set_any(rnd, seen):
    its = []
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    used_bh = set()
    for i in range(12):
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
            mir, flp = rnd.random() < 0.5, i in (4, 9)
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
            e += " This triangle has an obtuse angle, so its height falls outside it and meets the gray dashed extension of the base."
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(Fr(b * s, 2), su), ar(A, u), ar(b * s, su)], e, rnd))
    for b, h, u, su in [(Fr(15, 2), 4, "m", "m²"), (12, Fr(13, 2), "in", "in²"), (9, 5, "ft", "ft²"), (15, Fr(42, 5), "cm", "cm²")]:
        A = Fr(b * h, 2)
        q = "A triangle has a base of %s %s and a height of %s %s. What is its area?" % (num(b), u, num(h), u)
        e = "A = %s = %s %s." % (hx(b, h), num(A), su)
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(A, u), ar(b + h, su)], e, rnd))
    for A, k, u, su, what, other in [(36, 9, "cm", "cm²", "base", "height"), (42, 7, "m", "m²", "height", "base")]:
        o = Fr(2 * A, k)
        q = "A triangle has an area of %d %s. Its %s is %d %s. What is its %s?" % (A, su, what, k, u, other)
        e = ("%s × %d × ? = %d. Double the area first: %d × 2 = %d. Then %d ÷ %d = %s %s. Check: %s = %d %s."
             % (HALF, k, A, A, 2 * A, 2 * A, k, num(o), u, hx(k, o), A, su))
        its.append(mcq(q, ar(o, u), [ar(Fr(A, k), u), ar(A - k, u), ar(o, su), ar(Fr(A, 2), u)], e, rnd))
    for i in range(2):
        u = ["m", "ft"][i]
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
    assert len(its) == 20, len(its)
    return {"title": "Area of any triangle: base and height", "items": its}


# ------------------------------------------------------------ set 3: parallelograms and trapezoids
def set_quads(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] <= 12 and 3 <= t[1] <= 16 and t[0] / t[1] <= 1.4]
    rnd.shuffle(tr)
    for i in range(6):
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
             "not the slanted %d %s side. (Cut off the triangle on one end and move it to the other end: "
             "you get a rectangle that is %d by %d.)" % (b, h, num(A), su, s, u, b, h))
        its.append(mcq(q, ar(A, su), [ar(b * s, su), ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + s), su)], e, rnd))
    H = by_h()
    for i in range(6):
        u, su = UNITS[(i + 1) % 4]
        while True:
            if i % 3 == 2:                                  # right trapezoid
                h = rnd.randint(3, 10)
                b2 = rnd.randint(3, 12)
                b1 = b2 + rnd.randint(2, 8)
                o, leg = 0, None
            else:                                           # symmetric, slanted legs labeled
                h = rnd.choice([x for x in sorted(H) if 3 <= x <= 12 and any(t[0] <= 9 for t in H[x])])
                d, leg = rnd.choice([t for t in H[h] if t[0] <= 9])
                b2 = rnd.randint(3, 12)
                b1, o = b2 + 2 * d, d
            if b1 / h > 3.5 or b1 > 26 or ("tz", b1, b2, h) in seen or leg in (b1, b2, h):
                continue
            svg = trap_svg(b1, b2, o, h, "%d %s" % (b1, u), "%d %s" % (b2, u), "%d %s" % (h, u),
                           "%d %s" % (leg, u) if leg else "", mirror=i % 2 == 1, flip=i == 4)
            if svg:
                break
        seen.add(("tz", b1, b2, h))
        A = Fr((b1 + b2) * h, 2)
        q = fig(svg) + "What is the area of the trapezoid?"
        e = ("A = %s × (b<sub>1</sub> + b<sub>2</sub>) × h = %s × (%d + %d) × %d = %s × %d × %d = %s %s."
             % (HALF, HALF, b1, b2, h, HALF, b1 + b2, h, num(A), su))
        cands = [ar((b1 + b2) * h, su)]
        if leg:
            cands.append(ar(Fr((b1 + b2) * leg, 2), su))
            e += " The %d %s side is slanted, so it is not the height." % (leg, u)
        cands += [ar(b1 * h, su), ar(A, u), ar(Fr(b1 * b2 * h, 2), su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # text
    for b, h, u, su in [(Fr(17, 2), 6, "ft", "ft²"), (14, Fr(23, 2), "cm", "cm²")]:
        A = b * h
        q = "A parallelogram has a base of %s %s and a height of %s %s. What is its area?" % (num(b), u, num(h), u)
        e = "A = base × height = %s × %s = %s %s. No %s here: a parallelogram is a rectangle with a slanted end moved." % (
            num(b), num(h), num(A), su, HALF)
        its.append(mcq(q, ar(A, su), [ar(Fr(A, 2), su), ar(A, u), ar(2 * (b + h), su)], e, rnd))
    for b1, b2, h, u, su in [(12, Fr(15, 2), 4, "m", "m²"), (Fr(21, 2), Fr(11, 2), 7, "in", "in²")]:
        A = Fr(1, 2) * (b1 + b2) * h
        q = ("A trapezoid has parallel sides of %s %s and %s %s. The distance between them (the height) is %s %s. "
             "What is its area?" % (num(b1), u, num(b2), u, num(h), u))
        e = "A = %s × (%s + %s) × %s = %s × %s × %s = %s %s." % (HALF, num(b1), num(b2), num(h), HALF, num(b1 + b2), num(h), num(A), su)
        its.append(mcq(q, ar(A, su), [ar((b1 + b2) * h, su), ar(b1 * h, su), ar(A, u), ar(b1 * b2 * h, su)], e, rnd))
    # missing height
    q = "A parallelogram has an area of 96 m². Its base is 12 m. What is its height?"
    e = "Area = base × height, so 12 × ? = 96. 96 ÷ 12 = 8 m. Check: 12 × 8 = 96."
    its.append(mcq(q, "8 m", ["16 m", "84 m", "8 m²", "4 m"], e, rnd))
    q = "A trapezoid has parallel sides of 7 cm and 13 cm and an area of 60 cm². What is its height?"
    e = ("%s × (7 + 13) × h = 60, so %s × 20 × h = 60, which is 10 × h = 60. h = 60 ÷ 10 = 6 cm. "
         "Check: %s × 20 × 6 = 60." % (HALF, HALF, HALF))
    its.append(mcq(q, "6 cm", ["3 cm", "40 cm", "6 cm²", "12 cm"], e, rnd))
    # which expression
    for i, (b1, b2, d, h, leg) in enumerate([(16, 6, 5, 12, 13), (14, 8, 3, 4, 5)]):
        u = ["ft", "m"][i]
        svg = must(trap_svg(b1, b2, d, h, "%d %s" % (b1, u), "%d %s" % (b2, u), "%d %s" % (h, u), "%d %s" % (leg, u),
                            mirror=i == 1))
        q = fig(svg) + "Which expression gives the area of the trapezoid?"
        right = "%s × (%d + %d) × %d" % (HALF, b1, b2, h)
        wrong = ["(%d + %d) × %d" % (b1, b2, h), "%s × (%d + %d) × %d" % (HALF, b1, b2, leg), "%d × %d" % (b1, h)]
        e = ("Add the two parallel sides, multiply by the height (the dashed line), and take half: "
             "%s = %s × %d × %d = %s %s²." % (right, HALF, b1 + b2, h, num(Fr((b1 + b2) * h, 2)), u))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallelograms and trapezoids", "items": its}


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
        q = fig(svg) + "A triangle is cut off the corner of a rectangle (gray dashed lines). What is the area of the shaded figure?"
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
        e = ("Rectangle: %d × %d = %d %s. The triangle's base is %d − %d = %d %s and its height is %d %s: "
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
    return {"title": "Composite figures: split into rectangles and triangles", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    n, he, his = P.next()
    add("%s's sailboat has a sail shaped like a right triangle. The bottom edge is 9 ft and the mast side is 16 ft. "
        "What is the area of the sail?" % n, "72 ft²", ["144 ft²", "72 ft", "25 ft²"],
        "The bottom edge and the mast meet at a right angle. A = %s = 72 ft²." % hx(9, 16))
    add("A triangular flower bed has a base of 12 m and a height of 7.5 m. How much ground does it cover?",
        "45 m²", ["90 m²", "45 m", "19.5 m²"], "A = %s = 45 m²." % hx(12, Fr(15, 2)))
    n, he, his = P.next()
    add("%s sews 12 triangle pennants for a banner. Each pennant has a base of 10 in and a height of 18 in. "
        "How much fabric do the pennants use in all?" % n, "1,080 in²", ["2,160 in²", "90 in²", "1,080 in"],
        "One pennant: %s = 90 in². Twelve pennants: 12 × 90 = 1,080 in²." % hx(10, 18))
    add("Each side panel of a skateboard ramp is a right triangle. The panel is 6 ft long on the ground and 1.5 ft tall. "
        "Both side panels get painted. How much area is painted?", "9 ft²", ["18 ft²", "4.5 ft²", "9 ft"],
        "One panel: %s = 4.5 ft². Two panels: 2 × 4.5 = 9 ft²." % hx(6, Fr(3, 2)))
    n, he, his = P.next()
    add("%s tiles a patio shaped like a trapezoid. The parallel sides are 14 ft and 10 ft, and they are 8 ft apart. "
        "Tile costs $4.50 per square foot. How much does the tile cost?" % n, "$432", ["$864", "$504", "$360"],
        "Area: %s × (14 + 10) × 8 = %s × 24 × 8 = 96 ft². Cost: 96 × $4.50 = $432." % (HALF, HALF))
    add("A flag is a rectangle 6 ft long and 4 ft tall. A blue triangle on the flag has a base of 4 ft (the short side) "
        "and a height of 3 ft. The rest of the flag is white. What is the area of the white part?",
        "18 ft²", ["12 ft²", "30 ft²", "18 ft"],
        "Flag: 6 × 4 = 24 ft². Triangle: %s = 6 ft². White part: 24 − 6 = 18 ft²." % hx(4, 3))
    add("A parking space is shaped like a parallelogram. It is 10 ft wide along the curb, and the painted slanted lines "
        "are 20 ft long. The distance straight across from the curb to the back of the space is 18 ft. What is its area?",
        "180 ft²", ["200 ft²", "90 ft²", "180 ft"],
        "A = base × height = 10 × 18 = 180 ft². The 20 ft lines are slanted, so they are not the height.")
    add("An L-shaped lawn is a 40 ft by 30 ft rectangle with a 15 ft by 10 ft corner taken out for a patio. "
        "What is the area of the lawn?", "1,050 ft²", ["1,200 ft²", "1,350 ft²", "1,050 ft"],
        "Whole rectangle: 40 × 30 = 1,200 ft². Patio corner: 15 × 10 = 150 ft². Lawn: 1,200 − 150 = 1,050 ft².")
    n, he, his = P.next()
    add("%s paints the front wall of a shed. The wall is a rectangle 24 ft wide and 8 ft tall with a triangle on top "
        "that is 6 ft tall. How much area does %s paint?" % (n, he), "264 ft²", ["336 ft²", "192 ft²", "264 ft"],
        "Rectangle: 24 × 8 = 192 ft². Triangle: %s = 72 ft². Total: 192 + 72 = 264 ft²." % hx(24, 6))
    add("A garden bed is a trapezoid. Its parallel sides are 3.5 m and 5.5 m, and the distance between them is 2 m. "
        "What is its area?", "9 m²", ["18 m²", "7 m²", "9 m"],
        "A = %s × (3.5 + 5.5) × 2 = %s × 9 × 2 = 9 m²." % (HALF, HALF))
    n, he, his = P.next()
    add("%s makes a triangle scarf. Its base is %s yd and its height is %s yd. How much fabric is in the scarf?"
        % (n, frac(Fr(3, 2)), frac(Fr(3, 4))), frac(Fr(9, 16)) + " yd²",
        [frac(Fr(9, 8)) + " yd²", frac(Fr(9, 4)) + " yd²", frac(Fr(9, 16)) + " yd"],
        "A = %s × %s × %s = %s × %s = %s yd²." % (HALF, frac(Fr(3, 2)), frac(Fr(3, 4)), HALF, frac(Fr(9, 8)), frac(Fr(9, 16))))
    add("A corner shelf is a right triangle. The two sides along the walls are each %s ft long. What is the area of the shelf?"
        % frac(Fr(3, 4)), frac(Fr(9, 32)) + " ft²", [frac(Fr(9, 16)) + " ft²", frac(Fr(3, 2)) + " ft²", frac(Fr(9, 32)) + " ft"],
        "The two wall sides meet at a right angle. A = %s × %s × %s = %s × %s = %s ft²."
        % (HALF, frac(Fr(3, 4)), frac(Fr(3, 4)), HALF, frac(Fr(9, 16)), frac(Fr(9, 32))))
    add("A triangular sail has an area of 54 m². Its base is 9 m. How tall is the sail?", "12 m",
        ["6 m", "45 m", "12 m²"], "%s × 9 × h = 54, so 9 × h = 108. h = 108 ÷ 9 = 12 m." % HALF)
    add("A field shaped like a parallelogram has an area of 1,200 m². Its base is 40 m. What is its height?", "30 m",
        ["15 m", "1,160 m", "30 m²"], "Area = base × height, so 40 × h = 1,200. h = 1,200 ÷ 40 = 30 m. "
        "(Halving is only for triangles and trapezoids.)")
    add("Triangle A has a base of 10 cm and a height of 8 cm. Parallelogram B has a base of 5 cm and a height of 8 cm. "
        "Which is true?", "They have the same area.", ["A is larger.", "B is larger.", "A is twice as large as B."],
        "A: %s = 40 cm². B: 5 × 8 = 40 cm². Same area. (Forgetting the %s makes A look twice as large.)" % (hx(10, 8), HALF))
    add("A park is a rectangle 80 m long and 60 m wide. It has a triangular pond with a base of 20 m and a height of 15 m. "
        "The rest of the park is grass. What is the area of the grass?", "4,650 m²", ["4,500 m²", "4,950 m²", "4,650 m"],
        "Park: 80 × 60 = 4,800 m². Pond: %s = 150 m². Grass: 4,800 − 150 = 4,650 m²." % hx(20, 15))
    n, he, his = P.next()
    add("%s covers a stage shaped like a trapezoid with square tiles. The parallel sides are 20 ft and 12 ft, and they are "
        "9 ft apart. Each tile covers 4 ft². How many tiles does %s need?" % (n, he), "36 tiles",
        ["72 tiles", "144 tiles", "576 tiles"],
        "Area: %s × (20 + 12) × 9 = %s × 32 × 9 = 144 ft². Tiles: 144 ÷ 4 = 36." % (HALF, HALF))
    add("A kite is made of two triangles that share a 30 in rod down the middle. Each triangle is 10 in tall, measured from "
        "the rod. How much paper covers the kite?", "300 in²", ["600 in²", "150 in²", "300 in"],
        "Each triangle: base 30 in (the rod), height 10 in: %s = 150 in². Two triangles: 2 × 150 = 300 in²." % hx(30, 10))
    add("A wooden sign is a rectangle 30 in long and 12 in tall with a triangle on one end, like an arrow. "
        "The triangle's base is the 12 in side, and it sticks out 8 in. What is the area of the sign?", "408 in²",
        ["456 in²", "360 in²", "408 in"],
        "Rectangle: 30 × 12 = 360 in². Triangle: %s = 48 in². Total: 360 + 48 = 408 in²." % hx(12, 8))
    add("A triangular sail has sides of 10 ft, 17 ft and 21 ft. The height to the 21 ft side is 8 ft. What is its area?",
        "84 ft²", ["168 ft²", "178.5 ft²", "84 ft"],
        "Use the 21 ft side as the base and the 8 ft height: A = %s = 84 ft². "
        "The 10 ft and 17 ft sides are slanted, so they are not the height." % hx(21, 8))
    assert len(its) == 20, len(its)
    return {"title": "Area word problems", "items": its}


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
        "<h2>The big idea: rearrange into rectangles</h2>"
        "<p>You already know the area of a rectangle: base × height. "
        "Every formula in this unit comes from cutting a shape apart or putting two copies together to make a rectangle. "
        "The <b>height</b> is always measured <b>straight across at a right angle to the base</b>. "
        "It is shown as a dashed line with a small square at the corner.</p>"
        "<h2>Parallelograms: A = b × h</h2>"
        "<p>Cut the triangle off one end and slide it to the other end. The parallelogram becomes a rectangle "
        "with the same base and the same height.</p>"
        "<figure class='sn-fig'>" + must(para_svg(12, 6, 8, "12 cm", "8 cm", "10 cm")) +
        "<figcaption>A = 12 × 8 = 96 cm². The slanted 10 cm side is not the height.</figcaption></figure>"
        "<h2>Triangles: A = " + HALF + " × b × h</h2>"
        "<p>Two copies of any triangle make a parallelogram, so a triangle is half of it. "
        "For a right triangle, the two sides that meet at the right angle are the base and the height.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(14, 5, 12, "14 m", "12 m", ("13 m", "L"))) +
        "<figcaption>A = " + HALF + " × 14 × 12 = " + HALF + " × 168 = 84 m².</figcaption></figure>"
        "<p>In an obtuse triangle the height can fall <b>outside</b> the triangle. Extend the base with a dashed line "
        "and measure the height to that line.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(7, 16, 12, "7 ft", "12 ft", ("20 ft", "L"),
                                              label="obtuse triangle with its height outside")) +
        "<figcaption>A = " + HALF + " × 7 × 12 = 42 ft². Use the base 7 ft, not the dashed extension.</figcaption></figure>"
        "<h2>Trapezoids: A = " + HALF + " × (b<sub>1</sub> + b<sub>2</sub>) × h</h2>"
        "<p>Two copies of a trapezoid, one turned upside down, make a parallelogram with base b<sub>1</sub> + b<sub>2</sub>. "
        "The trapezoid is half of it.</p>"
        "<figure class='sn-fig'>" + must(trap_svg(16, 6, 5, 12, "16 in", "6 in", "12 in", "13 in")) +
        "<figcaption>A = " + HALF + " × (16 + 6) × 12 = " + HALF + " × 22 × 12 = 132 in².</figcaption></figure>" +
        ex("Example", "A trapezoid has parallel sides of 9 m and 5 m. They are 4 m apart. Find the area.",
           "Add the bases: 9 + 5 = 14. Multiply by the height: 14 × 4 = 56. Take half: 56 ÷ 2 = 28.", "28 m²") +
        "<h2>Composite figures: split or subtract</h2>"
        "<p>Split the figure into rectangles and triangles that do not overlap, then add their areas. "
        "Or start with a big rectangle and subtract the piece that is missing.</p>"
        "<figure class='sn-fig'>" + must(house_svg(12, 7, 5, "ft")) +
        "<figcaption>Rectangle 12 × 7 = 84 ft². Triangle " + HALF + " × 12 × 5 = 30 ft². Total 84 + 30 = 114 ft².</figcaption></figure>" +
        ex("Subtract a piece", "A 10 m by 8 m rectangle has a triangle cut out. The triangle has a base of 8 m and a height of 3 m. Find the area left.",
           "Rectangle: 10 × 8 = 80. Triangle: " + HALF + " × 8 × 3 = 12. Subtract: 80 − 12 = 68.", "68 m²") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Triangle: 14 × 12 = 168", "Take half: " + HALF + " × 14 × 12 = 84"],
            ["Using the slanted 13 m side as the height", "Use the dashed height at a right angle to the base"],
            ["Trapezoid: (16 + 6) × 12 = 264", "Take half: " + HALF + " × 22 × 12 = 132"],
            ["Adding the side lengths (that is the perimeter)", "Area multiplies base and height"],
            ["Counting a corner twice in an L-shape", "Split into pieces that do not overlap"],
            ["Writing 84 ft for an area", "Area is in square units: 84 ft²"],
        ])
    )


FAQ = [
    {"q": "What is the formula for the area of a triangle?",
     "a": "A = ½ × base × height. The height must meet the base at a right angle, so it is not usually a side of the triangle (except in a right triangle)."},
    {"q": "Why do you divide by 2 to find the area of a triangle?",
     "a": "Two copies of the same triangle fit together to make a parallelogram (or a rectangle for a right triangle). The triangle is half of that shape, so its area is half of base × height."},
    {"q": "How do you find the area of a trapezoid?",
     "a": "Add the two parallel sides, multiply by the height, and take half: A = ½ × (b₁ + b₂) × h. For bases of 16 in and 6 in and a height of 12 in, A = ½ × 22 × 12 = 132 in²."},
    {"q": "How do you find the area of an irregular polygon in Grade 6?",
     "a": "Split it into rectangles and triangles that do not overlap, find each area, and add them. You can also start with a larger rectangle and subtract the missing pieces (6.G.A.1)."},
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
    rnd = random.Random(612)
    P = People(rnd)
    seen = set()
    sets = [set_right(rnd, seen), set_any(rnd, seen), set_quads(rnd, seen), set_composite(rnd), set_story(rnd, P)]
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
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "area-of-polygons", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Area of Triangles, Parallelograms, Trapezoids and Polygons",
        "seo_title": "Grade 6 Area of Polygons Worksheets: Triangles, Parallelograms, Trapezoids and Composite Figures",
        "short_title": "Area of polygons",
        "domain": "Geometry",
        "standard_code": "6.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/G/A/1/",
        "standard_text": "Find the area of right triangles, other triangles, special quadrilaterals, and polygons by composing into rectangles or decomposing into triangles and other shapes; apply these techniques in the context of solving real-world and mathematical problems.",
        "meta_desc": "Free Grade 6 area of polygons worksheets: area of right triangles and other triangles (A = ½bh), parallelograms (A = bh), trapezoids, and composite figures split into rectangles and triangles, plus real-world word problems. 100 practice questions with answer key.",
        "key_big": "Triangle: A = ½ × b × h. Parallelogram: A = b × h. Trapezoid: A = ½ × (b₁ + b₂) × h.",
        "key_sub": "The height always meets the base at a right angle; a slanted side is not the height. For other polygons, split the shape into rectangles and triangles and add, or subtract the missing piece. Area is in square units (ft², m²).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, CL)


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
