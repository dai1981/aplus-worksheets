# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Area of Parallelograms and Triangles (Ontario Curriculum 2020, Spatial Sense E2.5, E2.6)
  python3 tools/gen_caon_math_g5_area.py
Drawing engine copied from gen_caon_math_g6_area.py. Every figure is drawn to scale from its numbers.
Heights are red dashed lines with a right-angle mark; slanted sides carry their true lengths
(integer right triangles), so they can act as distractors. Triangle areas are whole numbers (base × height is even).
Canadian style: metric units, 4-digit numbers without a separator, 5 or more digits with a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
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
UNITS = [("cm", "cm²"), ("m", "m²")]
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

def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


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



# ------------------------------------------------------------ Grade 5 figures
def rect_svg(L, W, u, label="rectangle"):
    pts = [(0, 0), (L, 0), (L, W), (0, W)]
    return render([(pts, FILL)], label, rights=[((0, 0), (L, 0), (0, W))],
                  labels=[((0, 0), (L, 0), "%s %s" % (num(L), u), pts), ((L, 0), (L, W), "%s %s" % (num(W), u), pts)],
                  maxw=190, maxh=100)


def grid_svg(w, h, label="rectangle on a grid of squares"):
    """A w by h rectangle made of unit squares (each square 22 px)."""
    c, pad = 22, 4
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad, pad, w * c, h * c, FILL)]
    for i in range(1, w):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad + i * c, pad, pad + i * c, pad + h * c, GREEN))
    for j in range(1, h):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad, pad + j * c, pad + w * c, pad + j * c, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (pad, pad, w * c, h * c, GREEN))
    return svg_wrap(w * c + 2 * pad, h * c + 2 * pad, "".join(s), label)


def pair_svg(shapes, u, label="two shapes"):
    """Two (or more) shapes side by side at the same scale, bottoms lined up.
    shapes = [(letter, b, h, o, s)]: o = 0 is a rectangle; o > 0 is a parallelogram whose top is shifted o to the
    right, s its slanted side. The height of a parallelogram is a red dashed line at its right end."""
    gap, pad = 34, 6
    tot = sum(b + o for _, b, h, o, s in shapes)
    hmax = max(h for _, b, h, o, s in shapes)
    hmin = min(h for _, b, h, o, s in shapes)
    k = max(min(240.0 / tot, 95.0 / hmax), 36.0 / hmin)    # thin shapes stay tall enough for their letter
    yb = pad + hmax * k
    s_ = []
    x = pad
    for letter, b, h, o, sl in shapes:
        hl, bl = "%s %s" % (num(h), u), "%s %s" % (num(b), u)
        if o == 0:
            x0 = x + tw(hl, FS) + 8
            pts = [(x0, yb), (x0 + b * k, yb), (x0 + b * k, yb - h * k), (x0, yb - h * k)]
            s_.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                      % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN))
            s_.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                      % (x0 + 9, yb, x0 + 9, yb - 9, x0, yb - 9, INK))
            s_.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                      % (x0 - 6, yb - h * k / 2 + 6, FS, INK, hl))
            cx = x0 + b * k / 2
            nx = x0 + b * k
        else:
            sll = "%s %s" % (num(sl), u)
            lw = tw(sll, FS) + 16
            x0 = x + max(0.0, lw - o * k / 2)
            pts = [(x0, yb), (x0 + b * k, yb), (x0 + (b + o) * k, yb - h * k), (x0 + o * k, yb - h * k)]
            s_.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                      % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN))
            xr = x0 + (b + o) * k
            s_.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                      % (x0 + b * k, yb, xr, yb, GRAY))
            s_.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-dasharray='7 5'/>"
                      % (xr, yb - h * k, xr, yb, RED))
            s_.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                      % (xr - 9, yb, xr - 9, yb - 9, xr, yb - 9, INK))
            s_.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                      % (x0 + o * k / 2 - 14, yb - h * k / 2 + 6, FS, INK, sll))
            s_.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='start'>%s</text>"
                      % (xr + 6, yb - h * k / 2 + 6, FS, INK, hl))
            cx = x0 + (b + o) * k / 2
            nx = xr + 6 + tw(hl, FS)
        s_.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (x0 + b * k / 2, yb + 20, FS, INK, bl))
        s_.append("<text x='%.1f' y='%.1f' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (cx, yb - h * k / 2 + 7, GREEN, letter))
        x = max(nx, x0 + b * k / 2 + tw(bl, FS) / 2) + gap
    W = int(math.ceil(x - gap + pad))
    H = int(math.ceil(yb + 20 + 5 + pad))
    return svg_wrap(W, H, "".join(s_), label)


def per(a, b):
    return 2 * (a + b)


# ------------------------------------------------------------ set 1: rectangles review
def set_rect(rnd, seen):
    its = []
    used = set()
    # count squares on a grid
    for i in range(3):
        while True:
            w, h = rnd.randint(3, 8), rnd.randint(2, 5)
            if w <= h or (w, h) in used or w * h == per(w, h):
                continue
            break
        used.add((w, h))
        A = w * h
        q = fig(grid_svg(w, h)) + "Each small square is 1 cm². What is the area of the rectangle?"
        e = ("Count the squares: %d rows of %d is %d × %d = %d squares. Each square is 1 cm², so the area is %d cm². "
             "(%d cm is the perimeter: the distance around.)" % (h, w, h, w, A, A, per(w, h)))
        its.append(mcq(q, ar(A, "cm²"), [ar(per(w, h), "cm²"), ar(w + h, "cm²"), ar(A, "cm"), ar(A + w, "cm²")], e, rnd))
    # labelled rectangles
    for i in range(7):
        u, su = UNITS[i % 2]
        while True:
            L, W = rnd.randint(6, 15), rnd.randint(3, 9)
            if L <= W or L / W > 3 or (L, W) in used or L * W == per(L, W):
                continue
            svg = rect_svg(L, W, u)
            if svg:
                break
        used.add((L, W))
        A = L * W
        q = fig(svg) + "What is the area of the rectangle?"
        e = "A = base × height = %d × %d = %d %s." % (L, W, A, su)
        if i < 3:
            e += " Adding the sides (%d + %d + %d + %d = %d) gives the perimeter, not the area." % (L, W, L, W, per(L, W))
        its.append(mcq(q, ar(A, su), [ar(per(L, W), su), ar(L + W, su), ar(A, u), ar(2 * A, su)], e, rnd))
    # bigger rectangles in words
    for L, W, u, su in [(14, 12, "m", "m²"), (25, 8, "cm", "cm²"), (32, 15, "m", "m²")]:
        A = L * W
        q = "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
        e = "A = length × width = %d × %d = %d %s." % (L, W, A, su)
        its.append(mcq(q, ar(A, su), [ar(per(L, W), su), ar(L + W, su), ar(A, u), ar(A - L, su)], e, rnd))
    # squares
    for s, u, su in [(9, "cm", "cm²"), (7, "m", "m²")]:
        A = s * s
        q = "A square has sides of %d %s. What is its area?" % (s, u)
        e = "All four sides are %d %s, so A = %d × %d = %d %s. (4 × %d = %d is the perimeter.)" % (s, u, s, s, A, su, s, 4 * s)
        its.append(mcq(q, ar(A, su), [ar(4 * s, su), ar(2 * s, su), ar(A, u)], e, rnd))
    # missing side
    for A, L, u, su in [(56, 8, "cm", "cm²"), (72, 9, "m", "m²"), (84, 12, "cm", "cm²")]:
        W = A // L
        assert W * L == A
        q = "A rectangle has an area of %d %s. It is %d %s long. How wide is it?" % (A, su, L, u)
        e = ("Area = length × width, so %d × ? = %d. %d ÷ %d = %d %s. Check: %d × %d = %d."
             % (L, A, A, L, W, u, L, W, A))
        its.append(mcq(q, ar(W, u), [ar(A - L, u), ar(A // 2 - L, u), ar(W, su)], e, rnd))
    # expression
    q = "A rectangle is 8 m by 5 m. Which number sentence gives its area?"
    e = "Area = length × width = 8 × 5 = 40 m². 2 × (8 + 5) = 26 is the perimeter."
    its.append(mcq(q, "8 × 5", ["8 + 5", "2 × (8 + 5)", "8 × 5 × 2"], e, rnd))
    # unit
    q = "Which unit is best for the area of a classroom floor?"
    e = "Area is measured in square units. A classroom floor is a few metres long, so square metres (m²) fit best."
    its.append(mcq(q, "square metres (m²)", ["metres (m)", "centimetres (cm)", "kilometres (km)"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of rectangles: review", "items": its}


# ------------------------------------------------------------ set 2: parallelograms
def set_para(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] <= 12 and 3 <= t[1] <= 15 and t[0] / t[1] <= 1.4]
    for i in range(9):
        u, su = UNITS[i % 2]
        svg = None
        while not svg:
            o, h, s = rnd.choice(tr)
            bs = [b for b in range(max(o + 3, 6), 16) if b not in (s, h) and b / h <= 3.2 and ("pa", b, h) not in seen]
            rnd.shuffle(bs)
            for b in bs[:4]:
                svg = para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i % 3 == 1)
                if svg:
                    break
        seen.add(("pa", b, h))
        A = b * h
        q = fig(svg) + "What is the area of the parallelogram?"
        e = ("A = base × height = %d × %d = %d %s. The height is the dashed line that meets the base at a right angle. "
             "It is not the slanted %d %s side." % (b, h, A, su, s, u))
        if i < 3:
            e += (" (Cut off the triangle at one end and slide it to the other end: you get a rectangle that is "
                  "%d by %d.)" % (b, h))
        half = [ar(A // 2, su)] if A % 2 == 0 else []
        its.append(mcq(q, ar(A, su), [ar(b * s, su)] + half + [ar(A, u), ar(per(b, s), su)], e, rnd))
    # rhombus
    o, h, s = 6, 8, 10
    svg = must(para_svg(s, o, h, "10 cm", "8 cm", "10 cm", label="rhombus with its height"))
    q = fig(svg) + "This rhombus has four sides of 10 cm. What is its area?"
    e = "A rhombus is a parallelogram, so A = base × height = 10 × 8 = 80 cm². 10 × 10 = 100 uses a slanted side, not the height."
    its.append(mcq(q, "80 cm²", ["100 cm²", "40 cm²", "40 cm", "80 cm"], e, rnd))
    # cut and slide
    for i, (b, o, h, s, u) in enumerate([(14, 6, 8, 10, "cm"), (9, 5, 12, 13, "m")]):
        svg = must(para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 1))
        q = (fig(svg) + "Cut along the dashed height and slide the triangle to the other end. "
             "What rectangle do you get?")
        right = "%d %s by %d %s" % (b, u, h, u)
        e = ("The base stays %d %s and the height stays %d %s, so the rectangle is %d %s by %d %s. "
             "That is why the area of the parallelogram is base × height = %d × %d = %d %s²."
             % (b, u, h, u, b, u, h, u, b, h, b * h, u))
        its.append(mcq(q, right, ["%d %s by %d %s" % (b, u, s, u), "%d %s by %d %s" % (b + o, u, h, u),
                                  "%d %s by %d %s" % (o, u, h, u)], e, rnd))
    q = ("A rectangle is 9 cm by 6 cm. A parallelogram has a base of 9 cm, a height of 6 cm and slanted sides of 8 cm. "
         "How do their areas compare?")
    e = ("Rectangle: 9 × 6 = 54 cm². Parallelogram: base × height = 9 × 6 = 54 cm². The same base and the same height "
         "give the same area. (9 × 8 = 72 uses the slanted side.)")
    its.append(mcq(q, "They have the same area.", ["The parallelogram is larger.", "The rectangle is larger.",
                                                  "The parallelogram is half as large."], e, rnd))
    for b, h, u, su in [(15, 8, "m", "m²"), (24, 6, "cm", "cm²"), (12, 11, "m", "m²")]:
        A = b * h
        q = "A parallelogram has a base of %d %s and a height of %d %s. What is its area?" % (b, u, h, u)
        e = ("A = base × height = %d × %d = %d %s. Do not take half: a parallelogram is a rectangle with one end "
             "cut off and moved." % (b, h, A, su))
        its.append(mcq(q, ar(A, su), [ar(Fr(A, 2), su), ar(A, u), ar(per(b, h), su), ar(b + h, su)], e, rnd))
    q = "A parallelogram has an area of 96 m². Its base is 12 m. What is its height?"
    e = "Area = base × height, so 12 × ? = 96. 96 ÷ 12 = 8 m. Check: 12 × 8 = 96."
    its.append(mcq(q, "8 m", ["16 m", "84 m", "8 m²"], e, rnd))
    q = "A parallelogram has an area of 63 cm². Its height is 7 cm. How long is its base?"
    e = "Area = base × height, so ? × 7 = 63. 63 ÷ 7 = 9 cm. Check: 9 × 7 = 63."
    its.append(mcq(q, "9 cm", ["18 cm", "56 cm", "9 cm²"], e, rnd))
    for i, (b, o, h, s, u) in enumerate([(11, 9, 12, 15, "cm"), (15, 5, 12, 13, "m")]):
        svg = must(para_svg(b, o, h, "%d %s" % (b, u), "%d %s" % (h, u), "%d %s" % (s, u), mirror=i == 0))
        q = fig(svg) + "Which number sentence gives the area of the parallelogram?"
        right = "%d × %d" % (b, h)
        wrong = ["%d × %d" % (b, s), "%d × %d ÷ 2" % (b, h), "2 × (%d + %d)" % (b, s)]
        e = ("Area = base × height = %s = %d %s². %d is the slanted side, ÷ 2 is for triangles, "
             "and 2 × (%d + %d) is the perimeter." % (right, b * h, u, s, b, s))
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Parallelograms: base × height", "items": its}


# ------------------------------------------------------------ set 3: triangles
def set_tri(rnd, seen):
    its = []
    tr = [t for t in TRIPLES if t[0] < t[1] <= 16 and t[1] / t[0] <= 3 and t[0] >= 3 and t[0] * t[1] % 2 == 0]
    rnd.shuffle(tr)
    for i in range(4):
        u, su = UNITS[i % 2]
        while True:
            a, b, c = tr.pop()
            if rnd.random() < 0.5:
                a, b = b, a
            svg = right_tri_svg(a, b, "%d %s" % (a, u), "%d %s" % (b, u), "%d %s" % (c, u), i % 4)
            if svg:
                break
        A = a * b // 2
        q = fig(svg) + "What is the area of the right triangle?"
        e = ("The two sides that meet at the right angle are the base and the height. A = %d × %d ÷ 2 = %d ÷ 2 = %d %s. "
             "The %d %s side is slanted, so it is not the height." % (a, b, a * b, A, su, c, u))
        its.append(mcq(q, ar(A, su), [ar(a * b, su), ar(Fr(max(a, b) * c, 2), su), ar(A, u), ar(a + b + c, su)], e, rnd))
    for i in range(3):
        u, su = UNITS[(i + 1) % 2]
        while True:
            L, W = rnd.randint(6, 14), rnd.randint(3, 9)
            if L <= W or L / W > 3 or ("hr", L, W) in seen or (L * W) % 2:
                continue
            break
        seen.add(("hr", L, W))
        q = (fig(must(half_rect_svg(L, W, u, i % 2))) +
             "A diagonal cuts this rectangle into two equal triangles. What is the area of the shaded triangle?")
        A = L * W // 2
        e = ("The rectangle is %d × %d = %d %s. The shaded triangle is half of it: %d ÷ 2 = %d %s."
             % (L, W, L * W, su, L * W, A, su))
        its.append(mcq(q, ar(A, su), [ar(L * W, su), ar(A, u), ar(per(L, W), su), ar(L + W, su)], e, rnd))
    acute, obtuse = tri_options()
    acute = [t for t in acute if t[0] <= 20 and t[2] <= 12 and (t[0] * t[2]) % 2 == 0
             and all(Fr(x).denominator == 1 for x in t)]
    obtuse = [t for t in obtuse if t[0] <= 16 and t[2] <= 12 and (t[0] * t[2]) % 2 == 0
              and all(Fr(x).denominator == 1 for x in t)]
    rnd.shuffle(acute)
    rnd.shuffle(obtuse)
    used_bh = set()
    for i in range(6):
        u, su = UNITS[i % 2]
        ob = i == 5
        pool = obtuse if ob else acute
        while True:
            b, p, h, sl, sr = pool.pop()
            if (b, h) in used_bh:
                continue
            side = "L" if ob else rnd.choice("LR")
            s = sl if side == "L" else sr
            if s == b or s == h:
                continue
            svg = tri_svg(b, p, h, ar(b, u), ar(h, u), (ar(s, u), side), rnd.random() < 0.5, i == 3,
                          label="triangle with its height outside" if ob else "triangle with its height")
            if svg:
                break
        used_bh.add((b, h))
        A = b * h // 2
        q = fig(svg) + "What is the area of the triangle?"
        e = ("The height is the dashed line: it meets the base at a right angle. A = base × height ÷ 2 = "
             "%d × %d ÷ 2 = %d ÷ 2 = %d %s. The %s %s side is slanted, so it is not the height."
             % (b, h, b * h, A, su, num(s), u))
        if ob:
            e += " Here the height falls outside the triangle and meets the grey dashed line that extends the base."
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(Fr(b * s, 2), su), ar(A, u), ar(b * s, su)], e, rnd))
    for b, h, u, su in [(12, 7, "m", "m²"), (9, 8, "cm", "cm²"), (16, 5, "cm", "cm²")]:
        A = b * h // 2
        q = "A triangle has a base of %d %s and a height of %d %s. What is its area?" % (b, u, h, u)
        e = ("A = base × height ÷ 2 = %d × %d ÷ 2 = %d ÷ 2 = %d %s. Do not forget to take half: "
             "a triangle is half of a rectangle or parallelogram with the same base and height." % (b, h, b * h, A, su))
        its.append(mcq(q, ar(A, su), [ar(b * h, su), ar(A, u), ar(b + h, su)], e, rnd))
    for A, k, u, su, what, other in [(30, 6, "cm", "cm²", "base", "height"), (40, 8, "m", "m²", "height", "base")]:
        o = 2 * A // k
        q = "A triangle has an area of %d %s. Its %s is %d %s. What is its %s?" % (A, su, what, k, u, other)
        e = ("Base × height ÷ 2 = %d, so base × height = %d × 2 = %d. Then %d ÷ %d = %d %s. "
             "Check: %d × %d ÷ 2 = %d." % (A, A, 2 * A, 2 * A, k, o, u, k, o, A))
        its.append(mcq(q, ar(o, u), [ar(A // k, u), ar(A - k, u), ar(o, su)], e, rnd))
    b, p, h, sl, sr = 21, 5, 12, 13, 20
    assert (b, h) not in used_bh
    svg = must(tri_svg(b, p, h, "21 m", "12 m", ("13 m", "L"), mirror=True, label="triangle with its height"))
    q = fig(svg) + "Which number sentence gives the area of the triangle?"
    right = "21 × 12 ÷ 2"
    e = "The base is 21 m and the dashed height is 12 m. A = 21 × 12 ÷ 2 = 252 ÷ 2 = 126 m². 13 m is a slanted side."
    its.append(mcq(q, right, ["21 × 12", "21 × 13 ÷ 2", "21 + 12 + 13"], e, rnd))
    q = ("A parallelogram and a triangle have the same base (10 cm) and the same height (6 cm). "
         "The area of the parallelogram is 60 cm². What is the area of the triangle?")
    e = ("Two copies of the triangle make a parallelogram with the same base and height. So the triangle is half: "
         "60 ÷ 2 = 30 cm². Check: 10 × 6 ÷ 2 = 30.")
    its.append(mcq(q, "30 cm²", ["60 cm²", "120 cm²", "30 cm"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Triangles: base × height ÷ 2", "items": its}


# ------------------------------------------------------------ set 4: same area, different perimeters
def rect_choice(a, b, u):
    return "%d %s by %d %s" % (a, u, b, u)


def set_same(rnd):
    its = []
    # which rectangle has the same area (distractors share the perimeter)
    for a, b, u in [(4, 6, "cm"), (3, 10, "m"), (4, 9, "cm")]:
        A, P = a * b, per(a, b)
        same_a = [(x, A // x) for x in range(2, a) if A % x == 0 and (x, A // x) != (a, b)]
        same_p = [(x, P // 2 - x) for x in range(2, P // 4 + 1) if x * (P // 2 - x) != A]
        rnd.shuffle(same_a)
        rnd.shuffle(same_p)
        r = same_a[0]
        q = "Which rectangle has the same area as a %s rectangle?" % rect_choice(a, b, u)
        e = ("%d × %d = %d %s². %d × %d = %d %s² too, so the areas are equal. The other rectangles have the same "
             "perimeter (%d %s) but a different area." % (a, b, A, u, r[0], r[1], A, u, P, u))
        ws = [rect_choice(x, y, u) for x, y in same_p[:3]]
        assert len(ws) == 3, (a, b)
        its.append(mcq(q, rect_choice(r[0], r[1], u), ws, e, rnd))
    # area and one side -> perimeter
    for A, L, u in [(24, 8, "cm"), (45, 9, "m"), (36, 12, "cm")]:
        W = A // L
        P = per(L, W)
        q = "A rectangle has an area of %d %s² and a length of %d %s. What is its perimeter?" % (A, u, L, u)
        e = ("First find the width: %d ÷ %d = %d %s. Then add all four sides: %d + %d + %d + %d = %d %s."
             % (A, L, W, u, L, W, L, W, P, u))
        its.append(mcq(q, ar(P, u), [ar(A, u), ar(L + W, u), ar(4 * L, u), ar(P, u + "²")], e, rnd))
    # greatest / least perimeter for one area
    for A, most, u in [(36, True, "m"), (24, False, "cm"), (48, True, "cm")]:
        pairs = [(x, A // x) for x in range(1, int(math.isqrt(A)) + 1) if A % x == 0]
        rnd.shuffle(pairs)
        pairs = pairs[:4] if len(pairs) > 4 else pairs
        best = max(pairs, key=lambda t: per(*t)) if most else min(pairs, key=lambda t: per(*t))
        wrong = [p for p in pairs if p != best]
        word = "greatest" if most else "least"
        q = "Each rectangle has an area of %d %s². Which one has the %s perimeter?" % (A, u, word)
        e = ("The area stays %d %s², but the perimeters change: %s. A long, thin rectangle has a large perimeter; "
             "a rectangle close to a square has a small one."
             % (A, u, ", ".join("%d × %d → %d %s" % (x, y, per(x, y), u) for x, y in sorted(pairs))))
        assert len(wrong) == 3, A
        its.append(mcq(q, rect_choice(best[0], best[1], u), [rect_choice(x, y, u) for x, y in wrong], e, rnd))
    # count rectangles
    for A, n, cand in [(18, 3, ["6", "2", "18"]), (24, 4, ["8", "3", "12"])]:
        pairs = [(x, A // x) for x in range(1, int(math.isqrt(A)) + 1) if A % x == 0]
        assert len(pairs) == n
        q = ("How many different rectangles with whole-number side lengths (in cm) have an area of %d cm²? "
             "A rectangle and the same rectangle turned do not count twice." % A)
        e = "List the pairs that multiply to %d: %s. That makes %d rectangles." % (
            A, ", ".join("%d × %d" % p for p in pairs), n)
        its.append(mcq(q, str(n), cand, e, rnd))
    # two rectangles in a picture
    for i, (r1, r2, u, ask) in enumerate([((9, 2), (6, 3), "cm", "true"), ((8, 3), (6, 4), "m", "diff"),
                                          ((5, 4), (10, 2), "m", "true"), ((12, 2), (8, 3), "cm", "diff")]):
        assert r1[0] * r1[1] == r2[0] * r2[1]
        A = r1[0] * r1[1]
        P1, P2 = per(*r1), per(*r2)
        svg = must(pair_svg([("A", r1[0], r1[1], 0, 0), ("B", r2[0], r2[1], 0, 0)], u, label="two shapes: rectangles A and B"))
        pe = ("A: %d + %d + %d + %d = %d %s. B: %d + %d + %d + %d = %d %s."
              % (r1[0], r1[1], r1[0], r1[1], P1, u, r2[0], r2[1], r2[0], r2[1], P2, u))
        if ask == "true":
            q = fig(svg) + "Which sentence is true?"
            e = ("Areas: %d × %d = %d and %d × %d = %d, so the areas are the same. Perimeters: %s"
                 % (r1[0], r1[1], A, r2[0], r2[1], A, pe))
            big, small = ("A", "B") if P1 > P2 else ("B", "A")
            its.append(mcq(q, "Same area; %s has the greater perimeter." % big,
                           ["Same area; %s has the greater perimeter." % small, "Same area and same perimeter.",
                            "%s has the greater area." % big], e, rnd))
        else:
            q = fig(svg) + "Both rectangles have an area of %d %s². How much greater is the perimeter of A?" % (A, u)
            e = pe + " Difference: %d − %d = %d %s." % (P1, P2, P1 - P2, u)
            d = P1 - P2
            its.append(mcq(q, ar(d, u), [ar(d // 2, u), ar(P1, u), "None. The areas are the same."], e, rnd))
    # rectangle vs parallelogram with the same base and height
    for i, (b, o, h, s, u) in enumerate([(8, 3, 4, 5, "cm"), (9, 6, 8, 10, "m")]):
        svg = must(pair_svg([("A", b, h, 0, 0), ("B", b, h, o, s)], u, label="two shapes: rectangle A and parallelogram B"))
        A = b * h
        PA, PB = per(b, h), per(b, s)
        if i == 0:
            q = fig(svg) + "Rectangle A and parallelogram B have the same base and height. Which sentence is true?"
            e = ("Both areas are %d × %d = %d %s². Perimeters: A is 2 × (%d + %d) = %d %s and B is 2 × (%d + %d) = %d %s. "
                 "The slanted sides make B’s perimeter greater." % (b, h, A, u, b, h, PA, u, b, s, PB, u))
            its.append(mcq(q, "Same area; B has the greater perimeter.",
                           ["Same area; A has the greater perimeter.", "Same area and same perimeter.",
                            "B has the greater area."], e, rnd))
        else:
            q = fig(svg) + "What is the perimeter of parallelogram B?"
            e = ("Add the four sides: %d + %d + %d + %d = %d %s. The dashed height is not a side. "
                 "(Its area, %d × %d = %d %s², is the same as rectangle A.)" % (b, s, b, s, PB, u, b, h, A, u))
            its.append(mcq(q, ar(PB, u), [ar(PA, u), ar(A, u), ar(b + s, u)], e, rnd))
    q = "Rectangle A is 4 m by 6 m. Rectangle B is 3 m by 8 m. Which sentence is true?"
    e = ("Areas: 4 × 6 = 24 m² and 3 × 8 = 24 m². Perimeters: 2 × (4 + 6) = 20 m and 2 × (3 + 8) = 22 m. "
         "Same area, different perimeters.")
    its.append(mcq(q, "Same area; B has the greater perimeter.",
                   ["Same perimeter; B has the greater area.", "Same area and same perimeter.",
                    "Same area; A has the greater perimeter."], e, rnd))
    q = "A square has a perimeter of 24 cm. A rectangle has the same area as the square and is 9 cm long. What is the perimeter of the rectangle?"
    e = ("Square: 24 ÷ 4 = 6 cm sides, so its area is 6 × 6 = 36 cm². Rectangle: 36 ÷ 9 = 4 cm wide. "
         "Perimeter: 9 + 4 + 9 + 4 = 26 cm. Same area, but a different perimeter.")
    its.append(mcq(q, "26 cm", ["24 cm", "36 cm", "13 cm"], e, rnd))
    q = "A triangle has a base of 8 cm and a height of 6 cm. Which rectangle has the same area?"
    e = "Triangle: 8 × 6 ÷ 2 = 24 cm². A 4 cm by 6 cm rectangle is 4 × 6 = 24 cm². (8 cm by 6 cm forgets to take half.)"
    its.append(mcq(q, "4 cm by 6 cm", ["8 cm by 6 cm", "7 cm by 7 cm", "5 cm by 4 cm"], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Same area, different perimeters", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, rnd))

    n, he, his = P.next()
    add("%s’s family plants a vegetable garden shaped like a parallelogram. Its base is 9 m and its height is 6 m. "
        "The slanted sides are 7 m long. What is the area of the garden?" % n,
        "54 m²", ["63 m²", "27 m²", "54 m"],
        "A = base × height = 9 × 6 = 54 m². The 7 m sides are slanted, so they are not the height.")
    add("A sailboat on Lake Ontario has a sail shaped like a right triangle. The bottom edge is 3 m, the edge along "
        "the mast is 4 m and the slanted edge is 5 m. What is the area of the sail?",
        "6 m²", ["12 m²", "10 m²", "12 m"],
        "The bottom edge and the mast meet at a right angle, so they are the base and the height. "
        "A = 3 × 4 ÷ 2 = 6 m². The 5 m edge is slanted.")
    n, he, his = P.next()
    add("%s’s hockey team makes a triangle pennant with a base of 30 cm and a height of 50 cm. "
        "How much felt does the pennant need?" % n,
        "750 cm²", ["1500 cm²", "80 cm²", "750 cm"],
        "A = base × height ÷ 2 = 30 × 50 ÷ 2 = 1500 ÷ 2 = 750 cm².")
    n, he, his = P.next()
    add("%s’s family floods a backyard rink that is 12 m long and 8 m wide. What is the area of the ice?" % n,
        "96 m²", ["40 m²", "20 m²", "96 m"],
        "A = length × width = 12 × 8 = 96 m². (12 + 8 + 12 + 8 = 40 m is the length of the boards around it.)")
    add("Two classrooms both have floors of 48 m². One is 8 m by 6 m. The other is 12 m by 4 m. "
        "How much longer is the perimeter of the 12 m by 4 m room?",
        "4 m", ["2 m", "8 m", "None. The areas are the same."],
        "8 m by 6 m: 8 + 6 + 8 + 6 = 28 m. 12 m by 4 m: 12 + 4 + 12 + 4 = 32 m. 32 − 28 = 4 m. "
        "Same area does not mean same perimeter.")
    add("A triangular flower bed has a base of 8 m and a height of 5 m. One packet of wildflower seeds covers 4 m². "
        "How many packets are needed for the whole bed?", "5 packets", ["10 packets", "20 packets", "4 packets"],
        "Area: 8 × 5 ÷ 2 = 20 m². Packets: 20 ÷ 4 = 5. (Forgetting to take half gives 40 ÷ 4 = 10.)")
    n, he, his = P.next()
    add("At recess, %s draws a parallelogram with sidewalk chalk. Its base is 60 cm, its height is 40 cm and its "
        "slanted sides are 50 cm. What is its area?" % n,
        "2400 cm²", ["3000 cm²", "1200 cm²", "220 cm²"],
        "A = base × height = 60 × 40 = 2400 cm². The 50 cm sides are slanted, so they are not the height.")
    add("The front wall of a cottage is a rectangle 8 m wide and 3 m tall with a triangle on top that is 2 m tall. "
        "What is the area of the wall?", "32 m²", ["40 m²", "24 m²", "28 m²"],
        "Rectangle: 8 × 3 = 24 m². Triangle: 8 × 2 ÷ 2 = 8 m². Total: 24 + 8 = 32 m².")
    n, he, his = P.next()
    add("%s’s class makes 10 triangle flags for a Terry Fox Run banner. Each flag has a base of 20 cm and a height of "
        "30 cm. How much fabric do the flags use in all?" % n,
        "3000 cm²", ["6000 cm²", "300 cm²", "3000 cm"],
        "One flag: 20 × 30 ÷ 2 = 300 cm². Ten flags: 10 × 300 = 3000 cm².")
    add("A triangular sail has an area of 12 m². Its base is 4 m. How tall is the sail?", "6 m",
        ["3 m", "8 m", "6 m²"], "Base × height ÷ 2 = 12, so base × height = 24. Height = 24 ÷ 4 = 6 m.")
    add("A community garden shaped like a parallelogram has an area of 240 m². Its base is 20 m. What is its height?",
        "12 m", ["24 m", "220 m", "12 m²"],
        "Area = base × height, so 20 × ? = 240. 240 ÷ 20 = 12 m. (Doubling is only for triangles.)")
    add("Tiles shaped like parallelograms have a base of 10 cm, a height of 6 cm and slanted sides of 8 cm. "
        "What area do 30 tiles cover?", "1800 cm²", ["2400 cm²", "900 cm²", "1800 cm"],
        "One tile: 10 × 6 = 60 cm². 30 tiles: 30 × 60 = 1800 cm². (10 × 8 uses the slanted side.)")
    add("A park in Winnipeg is a rectangle 60 m long and 40 m wide. It has a triangular pond with a base of 20 m and a "
        "height of 10 m. The rest of the park is grass. What is the area of the grass?",
        "2300 m²", ["2200 m²", "2500 m²", "2400 m²"],
        "Park: 60 × 40 = 2400 m². Pond: 20 × 10 ÷ 2 = 100 m². Grass: 2400 − 100 = 2300 m².")
    n, he, his = P.next()
    add("%s makes two posters with the same area, 1200 cm². One is 40 cm by 30 cm. The other is 60 cm by 20 cm. "
        "%s glues ribbon around the edges. Which poster needs more ribbon, and how much more?" % (n, he.capitalize()),
        "60 cm by 20 cm; 20 cm more", ["40 cm by 30 cm; 20 cm more", "60 cm by 20 cm; 10 cm more", "Neither. They need the same."],
        "40 cm by 30 cm: 40 + 30 + 40 + 30 = 140 cm. 60 cm by 20 cm: 60 + 20 + 60 + 20 = 160 cm. "
        "The 60 cm by 20 cm poster needs 160 − 140 = 20 cm more ribbon.")
    add("The two triangle ends of a shed roof each have a base of 4 m and a height of 3 m. "
        "What is the total area of both ends?", "12 m²", ["24 m²", "6 m²", "14 m²"],
        "One end: 4 × 3 ÷ 2 = 6 m². Two ends: 2 × 6 = 12 m².")
    add("A yield sign is a triangle. Each side is 90 cm, and its height is about 78 cm. "
        "About how much area does the sign have?", "3510 cm²", ["7020 cm²", "4050 cm²", "3510 cm"],
        "Use the 90 cm side as the base and the 78 cm height: 90 × 78 ÷ 2 = 7020 ÷ 2 = 3510 cm². "
        "90 × 90 ÷ 2 uses a slanted side instead of the height.")
    n, he, his = P.next()
    add("%s wants a rectangular garden with an area of 36 m² and whole-metre sides. "
        "%s wants to use as little fence as possible. Which size should %s choose?" % (n, he.capitalize(), he),
        "6 m by 6 m", ["4 m by 9 m", "3 m by 12 m", "2 m by 18 m"],
        "All four have an area of 36 m². Perimeters: 6 by 6 → 24 m, 4 by 9 → 26 m, 3 by 12 → 30 m, 2 by 18 → 40 m. "
        "The square uses the least fence.")
    add("A bulletin board is 3 m long and 2 m tall. Backing paper costs $2 per square metre. "
        "How much does the paper for the board cost?", "$12", ["$20", "$6", "$10"],
        "Area: 3 × 2 = 6 m². Cost: 6 × $2 = $12. ($20 comes from using the perimeter, 10 m.)")
    add("A Canadian flag is 180 cm long and 90 cm tall. The red band at each end is 45 cm wide and 90 cm tall. "
        "What is the area of the two red bands together?", "8100 cm²", ["4050 cm²", "16" + NBSP + "200 cm²", "270 cm²"],
        "One band: 45 × 90 = 4050 cm². Two bands: 2 × 4050 = 8100 cm².")
    add("A rectangular soccer field at school has an area of 2400 m². It is 60 m long. How wide is it?",
        "40 m", ["20 m", "2340 m", "40 m²"],
        "Area = length × width, so 60 × ? = 2400. 2400 ÷ 60 = 40 m. Check: 60 × 40 = 2400.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: gardens, flags and rinks", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>The big idea: start from the rectangle</h2>"
        "<p>The area of a rectangle is base × height. Area is the space inside a shape. "
        "It is measured in square units, like cm² and m². "
        "Parallelograms and triangles can be turned into rectangles, so you can find their area too. "
        "The <b>height</b> is always measured <b>at a right angle to the base</b>. "
        "It is drawn as a dashed line with a small square at the corner.</p>"
        "<h2>Parallelograms: A = base × height</h2>"
        "<p>Cut the triangle off one end and slide it to the other end. The parallelogram becomes a rectangle "
        "with the same base and the same height. So the area does not change.</p>"
        "<figure class='sn-fig'>" + must(para_svg(12, 6, 8, "12 cm", "8 cm", "10 cm")) +
        "<figcaption>A = 12 × 8 = 96 cm². The slanted 10 cm side is not the height.</figcaption></figure>"
        "<h2>Triangles: A = base × height ÷ 2</h2>"
        "<p>Two copies of a triangle fit together to make a parallelogram with the same base and height. "
        "So a triangle is half of it. In a right triangle, the two sides that meet at the right angle are the "
        "base and the height.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(14, 5, 12, "14 m", "12 m", ("13 m", "L"))) +
        "<figcaption>A = 14 × 12 ÷ 2 = 168 ÷ 2 = 84 m².</figcaption></figure>" +
        ex("Example", "A triangle has a base of 10 cm and a height of 7 cm. Find the area.",
           "Multiply the base by the height: 10 × 7 = 70. Take half: 70 ÷ 2 = 35.", "35 cm²") +
        "<h2>Same area, different perimeters</h2>"
        "<p>Area is the space inside. Perimeter is the distance around. Two shapes can have the same area "
        "but different perimeters. A long, thin rectangle has a greater perimeter than one that is close to a square.</p>"
        "<figure class='sn-fig'>" + must(pair_svg([("A", 9, 2, 0, 0), ("B", 6, 3, 0, 0)], "cm",
                                                  label="two shapes: rectangles A and B")) +
        "<figcaption>Both areas are 18 cm². Perimeters: A is 22 cm and B is 18 cm.</figcaption></figure>" +
        ex("Example", "A rectangle is 3 m by 8 m. Find a rectangle with the same area but a smaller perimeter.",
           "Area: 3 × 8 = 24 m². 4 × 6 = 24 too. Perimeters: 3 + 8 + 3 + 8 = 22 m and 4 + 6 + 4 + 6 = 20 m.",
           "4 m by 6 m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using the slanted side as the height", "Use the dashed height at a right angle to the base"],
            ["Triangle: 14 × 12 = 168", "Take half: 14 × 12 ÷ 2 = 84"],
            ["Parallelogram: 12 × 8 ÷ 2 = 48", "No half for a parallelogram: 12 × 8 = 96"],
            ["Thinking the same area means the same perimeter", "Add the sides of each shape to check"],
            ["Writing 84 m for an area", "Area is in square units: 84 m²"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about area in the Ontario math curriculum?",
     "a": "In Grade 5 (Spatial Sense), students use rectangles to develop the formulas for the area of a parallelogram (base × height) and a triangle (base × height ÷ 2) and solve problems with them (E2.5). They also show that shapes with the same area can have different perimeters (E2.6)."},
    {"q": "Why do you divide by 2 to find the area of a triangle?",
     "a": "Two copies of the same triangle fit together to make a parallelogram with the same base and height. The triangle is half of it, so its area is base × height ÷ 2."},
    {"q": "Is the slanted side of a parallelogram its height?",
     "a": "No. The height is the distance straight up from the base, at a right angle to it. The slanted side is always longer than the height, so using it gives an area that is too big."},
    {"q": "Can two shapes have the same area but different perimeters?",
     "a": "Yes. A 2 cm by 9 cm rectangle and a 3 cm by 6 cm rectangle both have an area of 18 cm², but their perimeters are 22 cm and 18 cm."},
]


def gen():
    rnd = random.Random(45818)
    P = People(rnd)
    seen = set()
    sets = [set_rect(rnd, seen), set_para(rnd, seen), set_tri(rnd, seen), set_same(rnd), set_story(rnd, P)]
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
                assert x.count("<svg") <= 1, x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "area-of-parallelograms-and-triangles",
        "sort": 18, "updated": UPDATED, "pdf_url": "",
        "title": "Area of Parallelograms and Triangles",
        "seo_title": "Grade 5 Area of Parallelograms and Triangles Math Worksheets (Free, Answer Key)",
        "short_title": "Area of parallelograms and triangles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 5: E2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the area relationships among rectangles, parallelograms, and triangles to develop the formulas for the area of a parallelogram and the area of a triangle, and solve related problems",
        "meta_desc": "Free Grade 5 math worksheets on area for the Ontario curriculum: rectangles, parallelograms (base × height), triangles (base × height ÷ 2), shapes with the same area but different perimeters, and word problems about gardens, flags and rinks. 100 questions with an answer key.",
        "key_big": "Parallelogram: base × height. Triangle: base × height ÷ 2.",
        "key_sub": "The height meets the base at a right angle, so a slanted side is not the height. A triangle is half of a parallelogram with the same base and height. Shapes with the same area can have different perimeters.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(?:two shapes|rectangle on a grid)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
