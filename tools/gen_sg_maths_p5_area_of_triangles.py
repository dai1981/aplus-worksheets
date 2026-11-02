# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Area of Triangles (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: Area and Volume)
  python3 tools/gen_sg_maths_p5_area_of_triangles.py
Base and height of a triangle (the height is perpendicular to the base and can fall outside an obtuse
triangle), area of triangle = 1/2 × base × height, a missing base or height, composite figures made of
rectangles, squares and triangles, and word problems (some with bar models).
Drawing engine and composite figures are adapted from gen_cabc_math_g6_area.py (rewritten for Singapore).
Every figure is drawn to scale from its numbers. Heights are red dashed lines with a right-angle mark;
slanted sides are labelled with their true lengths, so they act as distractors.
Singapore style: cm and m, 4-digit numbers without a separator, 5 or more digits with a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
WHITE = "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
MINUS = "−"
UNITS = [("cm", "cm²"), ("m", "m²")]
HALF = "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"


# ------------------------------------------------------------ helpers
def num(x):
    """Exact number as text, Singapore style: 4536, 13 500 (no-break space), 22.5."""
    x = Fr(x)
    assert x >= 0, x
    s = format(Decimal(x.numerator) / Decimal(x.denominator), "f")
    assert clean(x), x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, fpart = s.partition(".")
    i = int(i)
    t = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    return t + ("." + fpart if fpart else "")


def clean(x):
    """True when x is a short terminating decimal (at most 2 decimal places)."""
    return (Fr(x) * 100).denominator == 1


def ar(x, unit):
    return "%s %s" % (num(x), unit)


def hx(b, h):
    """1/2 × b × h = A"""
    return "%s × %s × %s = %s" % (HALF, num(b), num(h), num(Fr(b * h, 2)))


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero, negative or untidy numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith(MINUS) or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def maybe(x, unit):
    """ar() when x is a positive tidy number, else None (mcq skips it)."""
    x = Fr(x)
    return ar(x, unit) if x > 0 and clean(x) else None


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


def render(polys, label, lines=(), rights=(), labels=(), maxw=200, maxh=110, mirror=False, flip=False, rot=0,
           names=()):
    """Draw a figure to scale. Coordinates are in the problem's units, y going up.
    polys  = [(points, fill)]
    lines  = [(p, q, style)]  style: 'h' height (red dashed), 's' split (red dashed), 'x' extension (grey dashed)
    rights = [(F, A, B)]      right-angle mark at F between rays FA and FB
    labels = [(p, q, text, mode)] text next to segment pq; mode = polygon points (put it outside that polygon),
             'up'/'down'/'left'/'right', or None (try both sides).
    names  = [(p, letter, away)] a vertex letter next to point p, pushed away from point `away`
             (None: away from the middle of the first polygon).
    rot    = turn the whole figure by this many degrees (counterclockwise).
    Returns None when the labels cannot be placed without touching a line."""
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(p):
        x = float(-p[0] if mirror else p[0])
        y = float(-p[1] if flip else p[1])
        return (x * cr - y * sr, x * sr + y * cr)
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
    if names:
        q0 = pp[0][0]
        cen = (sum(p[0] for p in q0) / len(q0), sum(p[1] for p in q0) / len(q0))
    for p, t, away in names:
        c = P(p)
        r = cen if away is None else P(away)
        dx, dy = c[0] - r[0], c[1] - r[1]
        L = math.hypot(dx, dy)
        base = math.atan2(dy / L, dx / L)
        hw = max(tw(t, FS) / 2, 6)
        done = False
        for off in (14, 18, 23):
            for da in (0, 30, -30, 55, -55, 80, -80):
                ang = base + math.radians(da)
                cx, cy = c[0] + math.cos(ang) * (off + hw * 0.4), c[1] + math.sin(ang) * off
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


# ------------------------------------------------------------ triangles
def right_tri_svg(a, b, la, lb, lc, orient_i, label="right-angled triangle"):
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


def tri_named(b, p, h, L, rot=0, label="triangle with a dashed height"):
    """Triangle L[1]L[2]L[0]: base L[1]L[2] from (0,0) to (b,0), top vertex L[0] at (p,h),
    dashed height L[0]L[3] down to the base line (extended in grey when it falls outside)."""
    A, B, C, D = (p, h), (0, 0), (b, 0), (p, 0)
    pts = [B, C, A]
    lines = [(A, D, "h")]
    if p > b:
        lines.append((C, D, "x"))
        rights = [(D, B, A)]
    elif p < 0:
        lines.append((B, D, "x"))
        rights = [(D, C, A)]
    else:
        rights = [(D, C, A)]
    names = [(A, L[0], None), (B, L[1], None), (C, L[2], None), (D, L[3], A)]
    return render([(pts, FILL)], label, lines, rights, names=names, rot=rot, maxw=190, maxh=110)


def foot(P_, A, B):
    """Foot of the perpendicular from P_ to line AB (floats)."""
    ax, ay = float(A[0]), float(A[1])
    bx, by = float(B[0]), float(B[1])
    px, py = float(P_[0]), float(P_[1])
    t = ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)
    return (ax + t * (bx - ax), ay + t * (by - ay))


def tri_two_heights(b, p, h, rot=0):
    """Acute triangle ABC with heights AD (to BC) and BE (to AC)."""
    A, B, C = (p, h), (0, 0), (b, 0)
    D, E = (p, 0), foot((0, 0), A, C)
    lines = [(A, D, "h"), (B, E, "h")]
    rights = [(D, C, A), (E, C, B)]
    names = [(A, "A", None), (B, "B", None), (C, "C", None), (D, "D", A), (E, "E", B)]
    return render([([B, C, A], FILL)], "triangle ABC with two dashed heights", lines, rights, names=names, rot=rot,
                  maxw=190, maxh=115)


def right_named(a, c, rot=0):
    """Right-angled triangle ABC, right angle at B, AB = a up, BC = c across, height BD to AC."""
    A, B, C = (0, a), (0, 0), (c, 0)
    D = foot(B, A, C)
    lines = [(B, D, "h")]
    rights = [(B, C, A), (D, C, B)]
    names = [(A, "A", None), (B, "B", None), (C, "C", None), (D, "D", B)]
    return render([([B, C, A], FILL)], "right-angled triangle ABC with a dashed line BD", lines, rights,
                  names=names, rot=rot, maxw=190, maxh=110)


# ------------------------------------------------------------ composite figures
CL = "composite figure"


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
    return render([(pts, FILL)], CL + " (rectangle with a triangle on top)", lines, rights, labels, maxw=200, maxh=125)


def arrow_svg(w, a, t, u, mirror):
    """Rectangle w by a with a triangle (base a, height t) on its right side."""
    pts = [(0, 0), (w, 0), (w + t, Fr(a, 2)), (w, a), (0, a)]
    lines = [((w, 0), (w, a), "s"), ((w, Fr(a, 2)), (w + t, Fr(a, 2)), "h"),
             ((w, 0), (w + t, 0), "x"), ((w + t, 0), (w + t, Fr(a, 2)), "x")]
    rights = [((w, Fr(a, 2)), (w + t, Fr(a, 2)), (w, a))]
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts),
              ((w, 0), (w + t, 0), "%s %s" % (num(t), u), "down")]
    return render([(pts, FILL)], CL + " (rectangle and triangle)", lines, rights, labels, mirror=mirror, maxw=230, maxh=110)


def corner_svg(w, a, d, c, u, mirror):
    """Rectangle w by a with a right-angled triangle (d across, c down) cut off its top right corner."""
    pts = [(0, 0), (w, 0), (w, a - c), (w - d, a), (0, a)]
    lines = [((w - d, a), (w, a), "x"), ((w, a), (w, a - c), "x")]
    labels = [((0, 0), (w, 0), "%s %s" % (num(w), u), pts), ((0, a), (0, 0), "%s %s" % (num(a), u), pts),
              ((w - d, a), (w, a), "%s %s" % (num(d), u), "up"), ((w, a), (w, a - c), "%s %s" % (num(c), u), "right")]
    return render([(pts, FILL)], CL + " (rectangle with a corner cut off)", lines, labels=labels, mirror=mirror,
                  maxw=220, maxh=110)


def rtrap_split_svg(w, t, a, u, mirror):
    """Rectangle w by a with a right-angled triangle (t across, a up) on its right."""
    pts = [(0, 0), (w + t, 0), (w, a), (0, a)]
    lines = [((w, a), (w, 0), "s")]
    rights = [((0, 0), (1, 0), (0, 1)), ((w, 0), (w + t, 0), (w, a))]
    labels = [((0, 0), (w + t, 0), "%s %s" % (num(w + t), u), pts), ((w, a), (0, a), "%s %s" % (num(w), u), pts),
              ((0, a), (0, 0), "%s %s" % (num(a), u), pts)]
    return render([(pts, FILL)], CL + " (rectangle and right-angled triangle)", lines, rights, labels, mirror=mirror,
                  maxw=230, maxh=110)


def hex_svg(w, a, t, u):
    """Rectangle w by a with a triangle (base a, height t) on each end."""
    pts = [(t, 0), (t + w, 0), (2 * t + w, Fr(a, 2)), (t + w, a), (t, a), (0, Fr(a, 2))]
    lines = [((t, 0), (t, a), "s"), ((t + w, 0), (t + w, a), "s"), ((t + w, Fr(a, 2)), (2 * t + w, Fr(a, 2)), "h"),
             ((t + w, 0), (2 * t + w, 0), "x"), ((2 * t + w, 0), (2 * t + w, Fr(a, 2)), "x")]
    rights = [((t + w, Fr(a, 2)), (2 * t + w, Fr(a, 2)), (t + w, a))]
    labels = [((t, 0), (t + w, 0), "%s %s" % (num(w), u), pts), ((t, a), (t, 0), "%s %s" % (num(a), u), "right"),
              ((t + w, 0), (2 * t + w, 0), "%s %s" % (num(t), u), "down")]
    return render([(pts, FILL)], CL + " (rectangle with a triangle on each end)", lines, rights, labels, maxw=240, maxh=110)


def rect_tri_svg(L, W, x0, x1, ax, u, shade_tri=True, part=False):
    """Rectangle L by W. A triangle has its base (x0..x1) on the bottom side and its top vertex at (ax, W)
    on the top side. shade_tri: the triangle is shaded; otherwise the rest of the rectangle is shaded.
    part: the base is only part of the bottom side, and its length is labelled under it."""
    rect = [(0, 0), (L, 0), (L, W), (0, W)]
    tri = [(x0, 0), (x1, 0), (ax, W)]
    polys = [(rect, WHITE), (tri, FILL)] if shade_tri else [(rect, FILL), (tri, WHITE)]
    if part:
        labels = [((0, W), (L, W), "%s %s" % (num(L), u), "up"), ((L, 0), (L, W), "%s %s" % (num(W), u), "right"),
                  ((x0, 0), (x1, 0), "%s %s" % (num(x1 - x0), u), "down")]
    else:
        labels = [((0, 0), (L, 0), "%s %s" % (num(L), u), "down"), ((L, 0), (L, W), "%s %s" % (num(W), u), "right")]
    what = "square" if L == W else "rectangle"
    lab = CL + " (%s with %s)" % (what, "a shaded triangle" if shade_tri else "two shaded triangles")
    return render(polys, lab, labels=labels, maxw=200, maxh=105)


# integer right triangles (d across, h up, s slanted)
TRIPLES = sorted({(d, h, int(math.isqrt(d * d + h * h))) for d in range(1, 41) for h in range(1, 41)
                  if math.isqrt(d * d + h * h) ** 2 == d * d + h * h})


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
                if d1 < d2 and b.denominator == 1 and d2 <= 36 and b >= 4 and b >= 0.35 * d2 and 0.6 <= d2 / h <= 3 \
                        and d1 >= 0.25 * h:
                    obtuse.add((b, d2, h, s2, s1))   # base, top x, height, left side, right side
    return sorted(acute), sorted(obtuse)


# ------------------------------------------------------------ bar models
def text(x, y, t, fs=16, col=INK, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def model_svg(rows, uw, brackets, total=None):
    """Comparison bar model. rows = [(name, [segment widths in units], [text inside each segment])].
    Segments of width 1 are drawn as equal units. brackets = [(row, from, to, text)] in unit positions:
    above the first row or below the last row. total = text for a bracket on the right over all rows."""
    X0, RH, GAP = 104, 34, 18
    top = 44 if any(b[0] == 0 for b in brackets) else 8
    ys = [top + i * (RH + GAP) for i in range(len(rows))]
    s = []
    right_end = 0
    for (name, segs, inner), y in zip(rows, ys):
        s.append(text(X0 - 10, y + RH / 2.0 + 6, name, 15, anchor="end"))
        x = X0
        for w, t in zip(segs, inner):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, w * uw, RH, FILL, INK))
            if t:
                s.append(text(x + w * uw / 2.0, y + RH / 2.0 + 5, t, 14))
            x += w * uw
        right_end = max(right_end, x)
    bottom = ys[-1] + RH
    H = bottom + (44 if any(b[0] == len(rows) - 1 and len(rows) > 1 for b in brackets) else 8)
    for r, a, b, t in brackets:
        xa, xb = X0 + a * uw, X0 + b * uw
        col = RED if "?" in t else INK
        if r == 0:
            y = ys[0] - 6
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (xa, y, xa, y - 8, xb, y - 8, xb, y, col))
            s.append(text((xa + xb) / 2.0, y - 15, t, 16, col))
        else:
            y = ys[r] + RH + 6
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (xa, y, xa, y + 8, xb, y + 8, xb, y, col))
            s.append(text((xa + xb) / 2.0, y + 30, t, 16, col))
    W = right_end + 12
    if total:
        xr = right_end + 10
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xr, ys[0], xr + 8, ys[0], xr + 8, bottom, xr, bottom, INK))
        s.append(text(xr + 16, (ys[0] + bottom) / 2.0 + 6, total, 16, INK, anchor="start"))
        W = xr + 16 + tw(total, 16) + 10
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), "bar model comparing two areas")


# ------------------------------------------------------------ set 1: base and height
LETTERS = [("A", "B", "C", "D"), ("P", "Q", "R", "S"), ("X", "Y", "Z", "W"), ("K", "L", "M", "N"),
           ("E", "F", "G", "H"), ("R", "S", "T", "U"), ("J", "K", "L", "M"), ("A", "B", "C", "E"),
           ("P", "Q", "R", "T")]


def set_base_height(rnd):
    its = []
    lets = LETTERS[:]
    rnd.shuffle(lets)
    rots = [0, 22, -18, 180, 160]
    # acute triangles, height inside
    for i in range(5):
        L = lets[i]
        while True:
            b, h = rnd.randint(8, 14), rnd.randint(5, 10)
            p = rnd.randint(2, b - 2)
            if 2 * p == b:
                continue
            svg = tri_named(b, p, h, L, rot=rots[i])
            if svg:
                break
        base, ht = L[1] + L[2], L[0] + L[3]
        q = fig(svg) + "%s is the base of triangle %s. Which line is the height?" % (base, L[0] + L[1] + L[2])
        e = ("%s is perpendicular to the base %s: it meets %s at a right angle (see the small square). "
             "%s and %s are slanted sides, not the height." % (ht, base, base, L[0] + L[1], L[0] + L[2]))
        its.append(mcq(q, ht, [L[0] + L[1], L[0] + L[2], L[1] + L[3]], e, rnd))
    # obtuse triangles, height outside
    rots = [0, 15, 180, -20]
    for i in range(4):
        L = lets[5 + i]
        while True:
            b, o, h = rnd.randint(6, 11), rnd.randint(3, 6), rnd.randint(5, 9)
            p = b + o if i % 2 == 0 else -o
            svg = tri_named(b, p, h, L, rot=rots[i], label="obtuse-angled triangle with its height outside")
            if svg:
                break
        base, ht = L[1] + L[2], L[0] + L[3]
        near = L[2] + L[3] if p > b else L[1] + L[3]
        q = fig(svg) + "%s is the base of triangle %s. Which line is the height?" % (base, L[0] + L[1] + L[2])
        e = ("%s is the height. It is outside the triangle because the triangle has an obtuse angle. "
             "It meets the base line %s (extended with the grey dashed line) at a right angle. "
             "%s and %s are slanted sides." % (ht, base, L[0] + L[1], L[0] + L[2]))
        its.append(mcq(q, ht, [L[0] + L[1], L[0] + L[2], near], e, rnd))
    # right-angled triangle with a dashed line BD
    for a, c, rot, base, right, wrong, why in [
            (6, 9, 0, "BC", "AB", ["AC", "BD", "CD"], "AB meets BC at a right angle at B, so AB is the height."),
            (8, 6, 15, "AC", "BD", ["AB", "BC", "AD"], "BD meets AC at a right angle at D, so BD is the height."),
            (5, 10, 180, "AB", "BC", ["AC", "BD", "AD"], "BC meets AB at a right angle at B, so BC is the height.")]:
        svg = must(right_named(a, c, rot))
        q = fig(svg) + "Triangle ABC has a right angle at B. %s is the base. Which line is the height?" % base
        e = why + " In a right-angled triangle, the two sides that meet at the right angle are a base and its height."
        its.append(mcq(q, right, wrong, e, rnd))
    # one triangle, two heights
    for base, right, wrong, why in [
            ("BC", "AD", ["BE", "AB", "AC"], "AD meets BC at a right angle. BE is the height for the base AC."),
            ("AC", "BE", ["AD", "BC", "AB"], "BE meets AC at a right angle. AD is the height for the base BC.")]:
        svg = must(tri_two_heights(12, 5, 9, rot=0 if base == "BC" else 180))
        q = fig(svg) + "Triangle ABC has two dashed heights. Which line is the height for the base %s?" % base
        e = why + " Every side can be a base, and each base has its own height."
        its.append(mcq(q, right, wrong, e, rnd))
    # read the height from labelled lengths
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    for i in range(3):
        u, su = UNITS[i % 2]
        pool = obtuse if i == 1 else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            side = "L" if i == 1 else rnd.choice("LR")
            s = sl if side == "L" else sr
            if s in (b, h) or b == h:
                continue
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(s, u), side), rnd.random() < 0.5, False,
                          label="obtuse-angled triangle with its height outside" if i == 1 else "triangle with its height")
            if svg:
                break
        q = fig(svg) + "The base of the triangle is %s. What is its height?" % ar(b, u)
        e = ("The height is the dashed line, perpendicular to the base: %s. The %s side is slanted, so it is not the height."
             % (ar(h, u), ar(s, u)))
        its.append(mcq(q, ar(h, u), [ar(s, u), ar(b, u), ar(h, su)], e, rnd))
    svg = must(right_tri_svg(12, 5, "12 cm", "5 cm", "13 cm", 1))
    q = fig(svg) + "The base of this right-angled triangle is 12 cm. What is its height?"
    e = "The 5 cm side meets the 12 cm base at a right angle, so the height is 5 cm. The 13 cm side is slanted."
    its.append(mcq(q, "5 cm", ["13 cm", "12 cm", "5 cm²"], e, rnd))
    # facts
    q = "Which sentence about the height of a triangle is always true?"
    e = ("The height is always perpendicular to the base. It is not always a side, and in an obtuse-angled triangle "
         "it can be outside the triangle.")
    its.append(mcq(q, "It is perpendicular to the base.", ["It is the longest side.", "It is one of the sides.",
                                                          "It is inside the triangle."], e, rnd))
    q = "How many different sides of a triangle can be used as its base?"
    e = "Any of the 3 sides can be the base. Each base has its own height, drawn from the opposite vertex."
    its.append(mcq(q, "3", ["1", "2", "4"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Base and height of a triangle", "items": its}


# ------------------------------------------------------------ set 2: area = 1/2 × base × height
def set_area(rnd, used):
    its = []
    tr = [t for t in TRIPLES if t[0] < t[1] <= 24 and t[1] / t[0] <= 3 and t[0] >= 3 and (t[0] * t[1]) % 2 == 0]
    rnd.shuffle(tr)
    for i in range(4):
        u, su = UNITS[i % 2]
        while True:
            a, b, c = tr.pop()
            if rnd.random() < 0.5:
                a, b = b, a
            svg = right_tri_svg(a, b, ar(a, u), ar(b, u), ar(c, u), i % 4)
            if svg:
                break
        used.add((a, b))
        A = Fr(a * b, 2)
        q = fig(svg) + "Find the area of the right-angled triangle."
        e = ("The two sides that meet at the right angle are the base and the height. Area = %s %s. "
             "The %s side is slanted, so it is not the height." % (hx(a, b), su, ar(c, u)))
        its.append(mcq(q, ar(A, su), [ar(a * b, su), maybe(Fr(max(a, b) * c, 2), su), ar(A, u), ar(a + b + c, su)], e, rnd))
    for i in range(2):
        u, su = UNITS[(i + 1) % 2]
        while True:
            L, W = rnd.randint(6, 16), rnd.randint(3, 10)
            if L <= W or L / W > 3 or (L * W) % 2:
                continue
            break
        q = (fig(must(half_rect_svg(L, W, u, i % 2))) +
             "A diagonal cuts the rectangle into two equal triangles. Find the area of the shaded triangle.")
        A = Fr(L * W, 2)
        e = ("The rectangle is %d × %d = %d %s. The shaded triangle is half of it: %s %s."
             % (L, W, L * W, su, hx(L, W), su))
        its.append(mcq(q, ar(A, su), [ar(L * W, su), ar(A, u), ar(2 * (L + W), su), ar(L + W, su)], e, rnd))
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    for i in range(8):
        u, su = UNITS[i % 2]
        pool = obtuse if i % 2 else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            if (b, h) in used or (b * h) % 2:
                continue
            side = "L" if i % 2 else rnd.choice("LR")
            s = sl if side == "L" else sr
            if s == h or s == b:
                continue
            mir, flp = rnd.random() < 0.5, i == 4
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(s, u), side), mir, flp,
                          label="obtuse-angled triangle with its height outside" if i % 2 else "triangle with its height")
            if svg:
                break
        used.add((b, h))
        A = Fr(b * h, 2)
        q = fig(svg) + "Find the area of the triangle."
        e = ("The height is the dashed line: it is perpendicular to the base. Area = %s × base × height = %s %s. "
             "The %s side is slanted, so it is not the height." % (HALF, hx(b, h), su, ar(s, u)))
        if i % 2:
            e += " The triangle has an obtuse angle, so its height is outside it."
        its.append(mcq(q, ar(A, su), [ar(b * h, su), maybe(Fr(b * s, 2), su), ar(A, u), ar(b * s, su)], e, rnd))
    for b, h, u, su in [(16, 9, "cm", "cm²"), (15, 7, "m", "m²"), (24, 11, "cm", "cm²"), (Fr(9, 2), 6, "m", "m²")]:
        A = Fr(b * h, 2)
        q = "A triangle has a base of %s and a height of %s. Find its area." % (ar(b, u), ar(h, u))
        e = "Area = %s × base × height = %s %s. Do not forget the %s." % (HALF, hx(b, h), su, HALF)
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(A, u), ar(b + h, su)], e, rnd))
    for i in range(2):
        u = ["m", "cm"][i]
        while True:
            b, p, h, sl, sr = obtuse.pop()
            if (b, h) in used or sl == b or sl == h:
                continue
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(sl, u), "L"), i == 1, False,
                          label="obtuse-angled triangle with its height outside")
            if svg:
                break
        used.add((b, h))
        q = fig(svg) + "Which gives the area of the triangle?"
        right = "%s × %s × %s" % (HALF, num(b), num(h))
        wrong = ["%s × %s × %s" % (HALF, num(b), num(sl)), "%s × %s" % (num(b), num(h)),
                 "%s × %s × %s" % (HALF, num(sl), num(h))]
        e = ("The base is %s and the height is the dashed %s line, which meets the base line at a right angle outside "
             "the triangle. Area = %s %s²." % (ar(b, u), ar(h, u), hx(b, h), u))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of a triangle: ½ × base × height", "items": its}


# ------------------------------------------------------------ set 3: missing base or height
def miss_cands(A, k, other, u, su):
    """Wrong answers for 'area A, one length k, find the other': forgot to double (A ÷ k),
    halved instead of doubling (A ÷ 2 ÷ k), square units, doubled twice."""
    return [maybe(Fr(A, k), u), maybe(Fr(A, 2 * k), u), ar(other, su), maybe(2 * other, u), maybe(A - k, u)]


def miss_e(A, k, other, u, su, what):
    return ("Area = %s × base × height, so %s × %s × ? = %s. Double the area: %s × 2 = %s. "
            "Then %s ÷ %s = %s. Check: %s %s." % (HALF, HALF, num(k), num(A), num(A), num(2 * A),
                                                 num(2 * A), num(k), ar(other, u), hx(k, other), su))


def set_missing(rnd, used):
    its = []
    acute, obtuse = tri_options()
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    seenq = set()
    for i in range(10):
        u, su = UNITS[i % 2]
        find_h = i < 6
        pool = obtuse if i % 3 == 1 else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            if (b * h) % 2 or (b, h) in used or b == h:
                continue
            side = rnd.choice("LR") if pool is acute else "L"
            s = sl if side == "L" else sr
            if s in (b, h):
                continue
            svg = tri_svg(b, p, h, "?" if not find_h else ar(b, u), "?" if find_h else ar(h, u), (ar(s, u), side),
                          rnd.random() < 0.5, i == 3,
                          label="obtuse-angled triangle with its height outside" if pool is obtuse else "triangle with its height")
            if svg:
                break
        used.add((b, h))
        A = Fr(b * h, 2)
        k, other = (b, h) if find_h else (h, b)
        q = fig(svg) + "The area of the triangle is %s. Find %s." % (ar(A, su), "its height" if find_h else "its base")
        e = miss_e(A, k, other, u, su, "height" if find_h else "base")
        its.append(mcq(q, ar(other, u), miss_cands(A, k, other, u, su) + [ar(s, u)], e, rnd))
    # text questions
    n = 0
    while n < 7:
        u, su = UNITS[n % 2]
        b, h = rnd.randint(4, 20), rnd.choice([4, 8, 12, 16, 6, 10, 14])
        if b == h or (b * h) % 2 or (b, h) in used or ("t", b, h) in seenq:
            continue
        seenq.add(("t", b, h))
        used.add((b, h))
        A = Fr(b * h, 2)
        find_h = n % 2 == 0
        k, other = (b, h) if find_h else (h, b)
        if find_h:
            q = "A triangle has an area of %s and a base of %s. What is its height?" % (ar(A, su), ar(k, u))
        else:
            q = "The area of a triangle is %s. Its height is %s. How long is its base?" % (ar(A, su), ar(k, u))
        e = miss_e(A, k, other, u, su, "height" if find_h else "base")
        its.append(mcq(q, ar(other, u), miss_cands(A, k, other, u, su), e, rnd))
        n += 1
    for A, k, other, u in [(30, 5, 12, "cm"), (54, 9, 12, "m")]:
        su = u + "²"
        q = ("A right-angled triangle has an area of %s. One of the two sides that meet at the right angle is %s. "
             "How long is the other one?" % (ar(A, su), ar(k, u)))
        e = ("The two sides at the right angle are the base and the height. " +
             "%s × 2 = %s, and %s ÷ %s = %s. Check: %s %s." % (num(A), num(2 * A), num(2 * A), num(k), ar(other, u),
                                                              hx(k, other), su))
        its.append(mcq(q, ar(other, u), miss_cands(A, k, other, u, su), e, rnd))
    q = ("Triangle P has a base of 10 cm and a height of 6 cm. Triangle Q has the same area and a base of 4 cm. "
         "What is the height of triangle Q?")
    e = "Area of P = %s cm². For Q: 30 × 2 = 60, and 60 ÷ 4 = 15 cm. Check: %s cm²." % (hx(10, 6), hx(4, 15))
    its.append(mcq(q, "15 cm", ["6 cm", "7.5 cm", "15 cm²"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing base or height", "items": its}


# ------------------------------------------------------------ set 4: composite figures
def set_composite(rnd):
    its = []
    used = set()
    # houses: rectangle (or square) with a triangle on top
    for i in range(4):
        u, su = UNITS[i % 2]
        total = i >= 2
        while True:
            w = rnd.choice([6, 8, 10, 12, 14, 16])
            a = w if i == 1 else rnd.randint(4, 10)
            r = rnd.randint(3, 7)
            if ("ho", w, a, r) in used or r == a:
                continue
            svg = house_svg(w, a, r, u, total)
            if svg:
                break
        used.add(("ho", w, a, r))
        R, T = w * a, Fr(w * r, 2)
        A = R + T
        shape = "square" if w == a else "rectangle"
        q = fig(svg) + "The figure is made up of a %s and a triangle. Find its area." % shape
        if total:
            e = ("The triangle’s height is %d %s %d = %d %s. %s: %d × %d = %d %s. Triangle: %s %s. "
                 "Total: %d + %s = %s %s." % (a + r, MINUS, a, r, u, shape.capitalize(), w, a, R, su, hx(w, r), su,
                                             R, num(T), num(A), su))
            cands = [ar(R + Fr(w * (a + r), 2), su), ar(R + w * r, su), ar(w * (a + r), su), ar(A, u)]
        else:
            e = ("%s: %d × %d = %d %s. Triangle: %s %s. Total: %d + %s = %s %s."
                 % (shape.capitalize(), w, a, R, su, hx(w, r), su, R, num(T), num(A), su))
            cands = [ar(R + w * r, su), ar(w * (a + r), su), ar(A, u), ar(R, su)]
        its.append(mcq(q, ar(A, su), cands, e, rnd))
    # rectangle + triangle on the side
    for i in range(3):
        u, su = UNITS[i % 2]
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
        q = fig(svg) + "The figure is made up of a rectangle and a triangle. Find its area."
        e = ("Rectangle: %d × %d = %d %s. The triangle’s base is the %d %s side and its height is %d %s: "
             "%s %s. Total: %d + %s = %s %s." % (w, a, R, su, a, u, t, u, hx(a, t), su, R, num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R + a * t, su), ar((w + t) * a, su), ar(A, u), ar(R, su)], e, rnd))
    # rectangle with a corner cut off
    for i in range(3):
        u, su = UNITS[(i + 1) % 2]
        while True:
            w, a = rnd.randint(8, 14), rnd.randint(6, 10)
            d, c = rnd.randint(3, w // 2), rnd.randint(2, a // 2)
            if ("cc", w, a, d, c) in used or d == c or w == a or (d * c) % 2:
                continue
            svg = corner_svg(w, a, d, c, u, mirror=i == 2)
            if svg:
                break
        used.add(("cc", w, a, d, c))
        R, T = w * a, Fr(d * c, 2)
        A = R - T
        q = fig(svg) + ("A right-angled triangle is cut off the corner of a rectangle (grey dashed lines). "
                        "Find the area of the figure that is left.")
        e = ("Whole rectangle: %d × %d = %d %s. Triangle cut off: %s %s. "
             "Area left: %d %s %s = %s %s." % (w, a, R, su, hx(d, c), su, R, MINUS, num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R - d * c, su), ar(R + T, su), ar(R, su), ar(A, u)], e, rnd))
    # rectangle + right-angled triangle
    for i in range(2):
        u, su = UNITS[i % 2]
        while True:
            w, t, a = rnd.randint(5, 12), rnd.randint(3, 8), rnd.randint(4, 9)
            if ("rs", w, t, a) in used or (t * a) % 2 or t == w:
                continue
            svg = rtrap_split_svg(w, t, a, u, mirror=i == 1)
            if svg:
                break
        used.add(("rs", w, t, a))
        R, T = w * a, Fr(t * a, 2)
        A = R + T
        q = fig(svg) + "The dashed line divides the figure into a rectangle and a triangle. Find its area."
        e = ("Rectangle: %d × %d = %d %s. The triangle’s base is %d %s %d = %d %s and its height is %d %s: "
             "%s %s. Total: %d + %s = %s %s." % (w, a, R, su, w + t, MINUS, w, t, u, a, u, hx(t, a), su, R, num(T),
                                                num(A), su))
        its.append(mcq(q, ar(A, su), [ar((w + t) * a, su), ar(R + Fr((w + t) * a, 2), su), ar(A, u), ar(R + t * a, su)],
                       e, rnd))
    # rectangle with a triangle on each end
    for i in range(2):
        u, su = UNITS[(i + 1) % 2]
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
        q = fig(svg) + "The figure is made up of a rectangle and two identical triangles. Find its area."
        e = ("Rectangle: %d × %d = %d %s. Each triangle: base %d %s, height %d %s, so %s %s. "
             "Total: %d + %s + %s = %s %s." % (w, a, R, su, a, u, t, u, hx(a, t), su, R, num(T), num(T), num(A), su))
        its.append(mcq(q, ar(A, su), [ar(R + T, su), ar(R + 2 * a * t, su), ar((w + 2 * t) * a, su), ar(A, u)], e, rnd))
    # shaded triangle inside a rectangle or square, base = bottom side, top vertex on the top side
    for L, W, ax, u in [(14, 8, 9, "cm"), (10, 10, 3, "m")]:
        su = u + "²"
        svg = must(rect_tri_svg(L, W, 0, L, ax, u))
        what = "square" if L == W else "rectangle"
        A = Fr(L * W, 2)
        q = fig(svg) + "Find the area of the shaded triangle in the %s." % what
        e = ("The triangle’s base is the %s side. Its top vertex is on the opposite side, so its height is %s, "
             "the breadth of the %s. Area = %s %s. It is half of the %s." % (ar(L, u), ar(W, u), what, hx(L, W), su, what))
        its.append(mcq(q, ar(A, su), [ar(L * W, su), ar(Fr(L * W, 4), su), ar(A, u), ar(2 * (L + W), su)], e, rnd))
    svg = must(rect_tri_svg(16, 9, 0, 16, 6, "cm", shade_tri=False))
    q = fig(svg) + "Find the total area of the two shaded triangles."
    e = ("Rectangle: 16 × 9 = 144 cm². The white triangle: %s cm². "
         "Shaded: 144 %s 72 = 72 cm². The shaded parts are always half of the rectangle." % (hx(16, 9), MINUS))
    its.append(mcq(q, "72 cm²", ["144 cm²", "36 cm²", "72 cm", "54 cm²"], e, rnd))
    # shaded triangle whose base is part of the bottom side
    for L, W, x0, b, ax, u in [(18, 8, 4, 10, 13, "cm"), (15, 6, 2, 9, 5, "m"), (20, 12, 8, 7, 16, "cm")]:
        su = u + "²"
        svg = must(rect_tri_svg(L, W, x0, x0 + b, ax, u, part=True))
        A = Fr(b * W, 2)
        q = fig(svg) + "The top vertex of the shaded triangle is on the top side of the rectangle. Find its area."
        e = ("Base: %s. The height is the distance between the top and bottom sides, the breadth of the rectangle: %s. "
             "Area = %s %s. (The length %s is not needed.)" % (ar(b, u), ar(W, u), hx(b, W), su, ar(L, u)))
        its.append(mcq(q, ar(A, su), [ar(b * W, su), maybe(Fr(L * W, 2), su), ar(A, u), maybe(Fr(b * L, 2), su)], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Composite figures and shaded parts", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    add("For National Day, Siti’s class makes 15 triangular flags. Each flag has a base of 20 cm and a height of 30 cm. "
        "What is the total area of the flags?", "4500 cm²", ["9000 cm²", "300 cm²", "4500 cm"],
        "One flag: %s cm². 15 flags: 15 × 300 = 4500 cm². (9000 cm² forgets the %s.)" % (hx(20, 30), HALF))
    add("Wei Ming makes a kite from two triangles. They share a 40 cm stick as their base. Their heights are 15 cm "
        "and 35 cm. What is the area of the kite?", "1000 cm²", ["2000 cm²", "700 cm²", "1000 cm"],
        "Top triangle: %s cm². Bottom triangle: %s cm². Kite: 300 + 700 = 1000 cm²." % (hx(40, 15), hx(40, 35)))
    add("A garden patch at the void deck of an HDB block is a right-angled triangle. The two sides along the walls are "
        "6 m and 8 m, and the third side is 10 m. Grass costs $5 for each square metre. How much does the grass cost?",
        "$120", ["$240", "$200", "$70"],
        "The 6 m and 8 m sides meet at a right angle. Area = %s m². Cost: 24 × $5 = $120. "
        "($200 uses the slanted 10 m side.)" % hx(6, 8))
    add("Mei Ling has a rectangular card 30 cm long and 20 cm wide. She cuts out a triangle with a base of 18 cm on one "
        "long side and its top vertex on the opposite side. What is the area of the card left?",
        "420 cm²", ["240 cm²", "300 cm²", "180 cm²"],
        "Card: 30 × 20 = 600 cm². The triangle’s height is the width of the card, 20 cm: %s cm². "
        "Left: 600 %s 180 = 420 cm²." % (hx(18, 20), MINUS))
    add("A triangular plot of grass at East Coast Park has a base of 40 m and a height of 25 m. Its slanted sides are "
        "30 m and 32 m long. What is its area?", "500 m²", ["1000 m²", "600 m²", "500 m"],
        "Area = %s m². The 30 m and 32 m sides are slanted, so they are not the height." % hx(40, 25))
    svg = model_svg([("Triangle P", [1, 1, 1], ["", "", ""]), ("Triangle Q", [1], [""])], 70,
                    [(0, 0, 3, "?")], total="96 cm²")
    add(fig(svg) + "The area of triangle P is 3 times the area of triangle Q. Their total area is 96 cm². "
        "What is the area of triangle P?", "72 cm²", ["24 cm²", "32 cm²", "48 cm²"],
        "4 units = 96 cm². 1 unit = 96 ÷ 4 = 24 cm². Triangle P = 3 units = 3 × 24 = 72 cm².")
    add("The sail of Ahmad’s model boat is a triangle with an area of 150 cm². Its base is 15 cm. What is its height?",
        "20 cm", ["10 cm", "20 cm²", "5 cm"],
        "%s × 15 × ? = 150. Double the area: 150 × 2 = 300. 300 ÷ 15 = 20 cm. Check: %s cm²." % (HALF, hx(15, 20)))
    add("A signboard at a hawker centre is a rectangle 80 cm long and 30 cm wide with a triangle at one end, like an "
        "arrow. The triangle’s base is the 30 cm side and its height is 20 cm. What is the area of the signboard?",
        "2700 cm²", ["3000 cm²", "2400 cm²", "2700 cm"],
        "Rectangle: 80 × 30 = 2400 cm². Triangle: %s cm². Total: 2400 + 300 = 2700 cm²." % hx(30, 20))
    add("At a CCA camp, each end of a tent is a triangle with a base of 2 m and a height of 1.5 m. "
        "What is the total area of the two triangular ends?", "3 m²", ["6 m²", "1.5 m²", "3 m"],
        "One end: %s m². Two ends: 2 × 1.5 = 3 m²." % hx(2, Fr(3, 2)))
    svg = must(rect_tri_svg(60, 60, 0, 60, 20, "cm"))
    add(fig(svg) + "A Children’s Day poster is a square of side 60 cm. The shaded triangle has the bottom side as its "
        "base and its top vertex on the top side. What is the area of the shaded triangle?",
        "1800 cm²", ["3600 cm²", "900 cm²", "1800 cm"],
        "The height of the triangle is the side of the square, 60 cm. Area = %s cm², half of the square." % hx(60, 60))
    add("Mr Tan’s rectangular garden is 12 m long and 9 m wide. It has a triangular flower bed with a base of 6 m and a "
        "height of 4 m. The rest is grass. What is the area of the grass?", "96 m²", ["84 m²", "12 m²", "96 m"],
        "Garden: 12 × 9 = 108 m². Flower bed: %s m². Grass: 108 %s 12 = 96 m². "
        "(84 m² forgets the %s.)" % (hx(6, 4), MINUS, HALF))
    add("Xin Yi folds a square piece of paper of side 15 cm along a diagonal to make a triangle. "
        "What is the area of the triangle?", "112.5 cm²", ["225 cm²", "56.25 cm²", "112.5 cm"],
        "The two sides of the square meet at a right angle, so they are the base and the height. "
        "Area = %s cm², half of the square (225 cm²)." % hx(15, 15))
    svg = model_svg([("Triangle A", [1, Fr(3, 4)], ["", "18 cm²"]), ("Triangle B", [1], [""])], 120,
                    [(0, 0, Fr(7, 4), "?")], total="90 cm²")
    add(fig(svg) + "The area of triangle A is 18 cm² more than the area of triangle B. Their total area is 90 cm². "
        "What is the area of triangle A?", "54 cm²", ["36 cm²", "72 cm²", "45 cm²"],
        "Take away the extra 18 cm²: 90 %s 18 = 72 cm² = 2 units. 1 unit = 72 ÷ 2 = 36 cm² (triangle B). "
        "Triangle A = 36 + 18 = 54 cm²." % MINUS)
    add("Two triangles share the same base of 14 cm. One has a height of 9 cm and the other has a height of 5 cm. "
        "How much greater is the area of the taller triangle?", "28 cm²", ["56 cm²", "4 cm²", "28 cm"],
        "Taller: %s cm². Shorter: %s cm². Difference: 63 %s 35 = 28 cm²." % (hx(14, 9), hx(14, 5), MINUS))
    add("Raju draws a square of side 12 cm. He joins two corners at the bottom to the midpoint of the top side "
        "to make a triangle. What fraction of the square is the triangle?",
        HALF, ["<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>",
               "<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>",
               "<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>"],
        "Square: 12 × 12 = 144 cm². Triangle: base 12 cm, height 12 cm, so %s cm². 72 out of 144 is %s."
        % (hx(12, 12), HALF))
    add("A triangular section of a wall at a playground has a base of 6 m and a height of 4 m. One litre of paint "
        "covers 3 m². How many litres of paint are needed for the section?", "4 ℓ", ["8 ℓ", "12 ℓ", "36 ℓ"],
        "Area = %s m². Paint: 12 ÷ 3 = 4 ℓ. (8 ℓ forgets the %s; 36 ℓ multiplies instead of dividing.)" % (hx(6, 4), HALF))
    svg = model_svg([("Rectangle", [1, 1, 1, 1], ["", "", "", ""]), ("Triangle", [1], [""])], 60,
                    [(0, 1, 4, "54 cm²"), (1, 0, 1, "?")])
    add(fig(svg) + "The area of a rectangle is 4 times the area of a triangle. The rectangle’s area is 54 cm² more than "
        "the triangle’s. What is the area of the triangle?", "18 cm²", ["72 cm²", "13.5 cm²", "54 cm²"],
        "The difference is 4 %s 1 = 3 units. 3 units = 54 cm², so 1 unit = 54 ÷ 3 = 18 cm². "
        "(13.5 cm² divides by 4 instead of 3.)" % MINUS)
    add("A triangular banner for Sports Day has a base of 1.2 m and a height of 80 cm. What is its area in square metres?",
        "0.48 m²", ["48 m²", "0.96 m²", "0.48 m"],
        "Use the same unit: 80 cm = 0.8 m. Area = %s m². (48 m² mixes metres and centimetres.)" % hx(Fr(6, 5), Fr(4, 5)))
    add("Hui Min’s triangular vegetable plot has an area of 45 m². Its height is 6 m. What is the length of its base?",
        "15 m", ["7.5 m", "15 m²", "3.75 m"],
        "%s × ? × 6 = 45. Double the area: 45 × 2 = 90. 90 ÷ 6 = 15 m. (7.5 m forgets to double.)" % HALF)
    svg = must(rect_tri_svg(16, 10, 0, 16, 11, "cm", shade_tri=False))
    add(fig(svg) + "Kumar draws a rectangle 16 cm by 10 cm and a white triangle inside it. The two triangles at the "
        "sides are shaded. What is the total shaded area?", "80 cm²", ["160 cm²", "40 cm²", "80 cm"],
        "Rectangle: 16 × 10 = 160 cm². White triangle: %s cm². Shaded: 160 %s 80 = 80 cm²." % (hx(16, 10), MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: flags, gardens and bar models", "items": its}


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
        "<h2>Base and height</h2>"
        "<p>Any side of a triangle can be the <b>base</b>. The <b>height</b> is the line from the opposite vertex "
        "that is <b>perpendicular</b> to the base. It is drawn as a dashed line with a small square at the right angle.</p>"
        "<figure class='sn-fig'>" + must(tri_named(12, 4, 8, ("A", "B", "C", "D"))) +
        "<figcaption>BC is the base. AD is the height, because AD ⊥ BC. AB and AC are slanted sides.</figcaption></figure>"
        "<p>In an <b>obtuse-angled triangle</b>, the height can fall <b>outside</b> the triangle. "
        "Extend the base with a dashed line and draw the height to it.</p>"
        "<figure class='sn-fig'>" + must(tri_named(8, 12, 7, ("P", "Q", "R", "S"),
                                                   label="obtuse-angled triangle with its height outside")) +
        "<figcaption>QR is the base. PS is the height. It meets QR extended at a right angle.</figcaption></figure>"
        "<p>In a right-angled triangle, the two sides that meet at the right angle are a base and its height.</p>"
        "<h2>Area of a triangle</h2>"
        "<p>A triangle is half of a rectangle with the same base and height. So</p>"
        "<p><b>Area of triangle = " + HALF + " × base × height</b></p>"
        "<figure class='sn-fig'>" + must(tri_svg(14, 5, 12, "14 m", "12 m", ("13 m", "L"))) +
        "<figcaption>Area = " + HALF + " × 14 × 12 = 84 m². The slanted 13 m side is not used.</figcaption></figure>"
        + ex("Find a missing height", "A triangle has an area of 36 cm² and a base of 9 cm. Find its height.",
             HALF + " × 9 × ? = 36. Double the area: 36 × 2 = 72. Then 72 ÷ 9 = 8.", "8 cm") +
        "<h2>Composite figures</h2>"
        "<p>Divide the figure into rectangles, squares and triangles. Find each area, then add. "
        "Or find the area of the whole rectangle and subtract the part that is not shaded.</p>"
        "<figure class='sn-fig'>" + must(house_svg(12, 7, 5, "m")) +
        "<figcaption>Rectangle: 12 × 7 = 84 m². Triangle: " + HALF + " × 12 × 5 = 30 m². "
        "Total: 84 + 30 = 114 m².</figcaption></figure>"
        + ex("Shaded triangle in a rectangle",
             "A rectangle is 14 cm by 8 cm. A shaded triangle has the 14 cm side as its base and its top vertex on the "
             "opposite side. Find the shaded area.",
             "The height of the triangle is the breadth of the rectangle, 8 cm. " + HALF + " × 14 × 8 = 56.",
             "56 cm², half of the rectangle") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using the slanted 13 m side as the height", "Use the height that is perpendicular to the base: 12 m"],
            ["Area = 14 × 12 = 168 m²", "Do not forget the " + HALF + ": " + HALF + " × 14 × 12 = 84 m²"],
            ["Height = 36 ÷ 9 = 4 cm", "Double the area first: 36 × 2 ÷ 9 = 8 cm"],
            ["Writing 84 m for an area", "Area is in square units: 84 m²"],
            ["Thinking the height must be inside the triangle", "In an obtuse-angled triangle it can be outside"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 area of triangle?",
     "a": "Primary 5 students learn to identify the base and height of a triangle, find its area with 1/2 × base × height, and find the area of composite figures made up of rectangles, squares and triangles."},
    {"q": "How do I explain the height of a triangle to my child?",
     "a": "The height is the line from a vertex that meets the opposite side (the base) at a right angle. It is not a slanted side, and in an obtuse-angled triangle it can fall outside the triangle."},
    {"q": "What is the most common mistake with area of triangles?",
     "a": "Forgetting the 1/2, or using the slanted side as the height. A triangle with base 14 m and height 12 m has an area of 1/2 × 14 × 12 = 84 m², not 168 m²."},
    {"q": "Is area of triangle in the MOE syllabus for Primary 5?",
     "a": "Yes. Area of triangle and composite figures is in Area and Volume, Measurement and Geometry, for Primary 5 in the MOE 2021 syllabus. It is used again in Primary 6 and in PSLE questions."},
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
    rnd = random.Random(65811)
    used = set()
    sets = [set_base_height(rnd), set_area(rnd, used), set_missing(rnd, used), set_composite(rnd), set_story(rnd)]
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
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"]
            assert k not in keys, it["q"]
            keys.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert not re.search(r"\d,\d{3}", re.sub(r"<svg.*?</svg>", "", x)), x
                assert not re.search(r"\d \d{3}\b", re.sub(r"<svg.*?</svg>", "", x)), x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "area-of-triangles", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Area of Triangles: Base, Height and Composite Figures",
        "seo_title": "P5 Area of Triangle Worksheets: Free Primary 5 Maths Practice with Answers (MOE Syllabus)",
        "short_title": "Area of triangles",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 5: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Concepts of base and height of a triangle; area of triangle; area of composite figures made up of rectangles, squares and triangles",
        "meta_desc": "Free P5 area of triangle practice: base and height, ½ × base × height, missing heights, composite figures and word problems. 100 questions with answers.",
        "key_big": "Area of triangle = ½ × base × height.",
        "key_sub": "The height is perpendicular to the base, not a slanted side: base 14 m, height 12 m gives ½ × 14 × 12 = 84 m².",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(?:%s|bar model)" % CL)


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
