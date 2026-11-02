# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Perimeter and Area (Australian Curriculum v9.0, AC9M4M02)
  python3 tools/gen_au_maths_y4_perimeter_area.py
Perimeter by adding sides (rectangles, squares, rectilinear shapes on grids, missing sides);
area by counting square units and half squares; estimating the area of irregular shapes on a grid;
cm² and m²; choosing a unit. No area formula yet (counting rows × columns is fine).
Wrong choices come from real mistakes (area vs perimeter, counting corner squares once, units).
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
SQ = {"cm": "cm²", "m": "m²"}
NBSP = " "


# ------------------------------------------------------------ helpers
def fmt(n):
    """4536 -> 4536, 10800 -> 10 800 (no-break space, Australian Curriculum style)."""
    return "{:,}".format(n).replace(",", NBSP) if n >= 10000 else str(n)

def half(x):
    """Fraction with halves -> '10½', '8'."""
    x = Fraction(x)
    assert x.denominator in (1, 2), x
    w = int(x)
    return str(w) if x.denominator == 1 else ("%d½" % w if w else "½")


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
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
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(NBSP) * 0.3 - t.count(" ") * 0.3) * fs * 0.6


def text(x, y, t, fs=17, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, col, t))


def plus(nums):
    return " + ".join(str(n) for n in nums)


# ------------------------------------------------------------ labelled shapes (drawn to scale)
FS = 17


def shape_svg(pts, labels, label):
    """Polygon with horizontal/vertical sides. labels[i] belongs to the side pts[i] -> pts[i+1]
    ('' = no label, a label with '?' is red). Labels sit outside the middle of their side and slide
    along it if they would touch another label or a side. Returns None if no place is found."""
    n = len(pts)
    sa = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))

    def clash(bx, placed):
        for B in placed:
            if bx[0] < B[2] + 16 and B[0] < bx[2] + 16 and bx[1] < B[3] + 8 and B[1] < bx[3] + 8:
                return True
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            if x1 == x2:
                if bx[0] - 3 < x1 < bx[2] + 3 and min(y1, y2) < bx[3] and bx[1] < max(y1, y2):
                    return True
            elif bx[1] - 3 < y1 < bx[3] + 3 and min(x1, x2) < bx[2] and bx[0] < max(x1, x2):
                return True
        return False

    boxes, texts = [], []
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = (dy / L, -dx / L) if sa > 0 else (-dy / L, dx / L)       # outward normal
        hw = tw(t, FS) / 2
        off = 8 + abs(nx) * hw + abs(ny) * 11
        for fr in (0.5, 0.62, 0.38, 0.72, 0.28, 0.8, 0.2):
            mx, my = x1 + dx * fr, y1 + dy * fr
            cx, cy = mx + nx * off, my + ny * off
            bx = (cx - hw, cy - 11, cx + hw, cy + 11)
            if not clash(bx, boxes):
                break
        else:
            return None
        boxes.append(bx)
        texts.append((cx, cy, t))
    xs = [p[0] for p in pts] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for p in pts] + [b[1] for b in boxes] + [b[3] for b in boxes]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.0f,%.0f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for cx, cy, t in texts:
        s.append(text(cx - ox, cy - oy + 6, t, FS, RED if "?" in t else INK))
    return svg_wrap(W, H, "".join(s), label)


def rect_svg(L, W, top, left, label, max_w=200, max_h=100):
    k = min(max_w / L, max_h / W, 26)
    pts = [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]
    s = shape_svg(pts, [top, "", "", left], label)
    assert s, (L, W)
    return s


def l_sides(Wt, Ht, cw, ch):
    """Sides of an L (Wt by Ht with a cw by ch corner cut), in drawing order."""
    return [Wt - cw, ch, cw, Ht - ch, Wt, Ht]


def l_pts(Wt, Ht, cw, ch, corner, k):
    p = [(0, 0), (Wt - cw, 0), (Wt - cw, ch), (Wt, ch), (Wt, Ht), (0, Ht)]
    if corner in ("tl", "bl"):
        p = [(Wt - x, y) for x, y in p]
    if corner in ("br", "bl"):
        p = [(x, Ht - y) for x, y in p]
    return [(x * k, y * k) for x, y in p]


def l_svg(Wt, Ht, cw, ch, corner, labels, label="rectilinear L-shape with side lengths"):
    k = min(240 / Wt, 130 / Ht)
    return shape_svg(l_pts(Wt, Ht, cw, ch, corner, k), labels, label)


def step_sides(W, H, x1, x2, y1, y2):
    """Staircase: (0,0)->(x1,0)->(x1,y1)->(x2,y1)->(x2,y2)->(W,y2)->(W,H)->(0,H)."""
    return [x1, y1, x2 - x1, y2 - y1, W - x2, H - y2, W, H]


def step_svg(W, H, x1, x2, y1, y2, labels, flip, label="rectilinear step shape with side lengths"):
    k = min(300 / W, 170 / H)
    p = [(0, 0), (x1, 0), (x1, y1), (x2, y1), (x2, y2), (W, y2), (W, H), (0, H)]
    if flip:
        p = [(W - x, y) for x, y in p]
    return shape_svg([(x * k, y * k) for x, y in p], labels, label)


# ------------------------------------------------------------ squared grids
def rect_cells(w, h, c0=0, r0=0):
    return {(c0 + i, r0 + j) for i in range(w) for j in range(h)}


def norm(cells):
    c0 = min(c for c, r in cells)
    r0 = min(r for c, r in cells)
    return frozenset((c - c0, r - r0) for c, r in cells)


def size(cells):
    return max(c for c, r in cells) + 1, max(r for c, r in cells) + 1


def perim(cells):
    n = 0
    for (c, r) in cells:
        for (dc, dr) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (c + dc, r + dr) not in cells:
                n += 1
    return n


def border(cells):
    """Number of squares that touch the edge (the 'count the squares round the edge' mistake)."""
    return sum(1 for (c, r) in cells
               if any((c + dc, r + dr) not in cells for dc, dr in [(0, -1), (0, 1), (-1, 0), (1, 0)]))


def inside_poly(x, y, poly):
    ins = False
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            ins = not ins
    return ins


def poly_area(poly):
    n = len(poly)
    return abs(Fraction(sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
                            for i in range(n)), 2))


def poly_counts(poly):
    """(full squares, half squares) covered by a polygon whose sides are straight or at 45 degrees."""
    full = halves = 0
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    for c in range(min(xs), max(xs)):
        for r in range(min(ys), max(ys)):
            hit = sum(inside_poly(c + (i + 0.3) / 20, r + (j + 0.6) / 20, poly) for i in range(20) for j in range(20))
            fr = hit / 400
            if fr > 0.97:
                full += 1
            elif 0.4 < fr < 0.6:
                halves += 1
            else:
                assert fr < 0.03, (poly, c, r, fr)
    assert poly_area(poly) == full + Fraction(halves, 2), poly
    return full, halves


def grid_svg(cols, rows, shapes, cell=26, label="shape on a squared grid", letters=None):
    """Squared grid cols x rows. shapes: list of (cells or polygon, dc, dr). cells = set of (c, r);
    polygon = list of grid points. Letters (A, B...) are written under each shape."""
    m = 6
    lh = 26 if letters else 0
    W, H = cols * cell + 2 * m, rows * cell + 2 * m + lh
    fills, lines = [], []
    for shp, dc, dr in shapes:
        if isinstance(shp, (set, frozenset)):
            for (c, r) in sorted(shp):
                fills.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                             % (m + (c + dc) * cell, m + (r + dr) * cell, cell, cell, FILL))
            for (c, r) in sorted(shp):
                x, y = m + (c + dc) * cell, m + (r + dr) * cell
                for (ec, er, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                                  (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
                    if (c + ec, r + er) not in shp:
                        lines.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' "
                                     "stroke-linecap='round'/>" % (x1, y1, x2, y2, GREEN))
        else:
            pts = " ".join("%d,%d" % (m + (x + dc) * cell, m + (y + dr) * cell) for x, y in shp)
            fills.append("<polygon points='%s' fill='%s'/>" % (pts, FILL))
            lines.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='3.5' stroke-linejoin='round'/>"
                         % (pts, GREEN))
    g = []
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    t = []
    if letters:
        for (shp, dc, dr), L in zip(shapes, letters):
            if isinstance(shp, (set, frozenset)):
                w = max(c for c, r in shp) + 1
            else:
                w = max(x for x, y in shp)
            t.append(text(m + (dc + w / 2) * cell, m + rows * cell + 21, L, 17, INK))
    return svg_wrap(W, H, "".join(fills + g + lines + t), label)


def one_grid(shp, label, cell=26):
    """One shape with a 1-square margin of empty grid round it."""
    if isinstance(shp, (set, frozenset)):
        w, h = size(shp)
    else:
        w, h = max(x for x, y in shp), max(y for x, y in shp)
    return grid_svg(w + 2, h + 2, [(shp, 1, 1)], cell, label)


def flipcells(cells, rnd):
    w, h = size(cells)
    if rnd.random() < 0.5:
        cells = {(w - 1 - c, r) for c, r in cells}
    if rnd.random() < 0.5:
        cells = {(c, h - 1 - r) for c, r in cells}
    return frozenset(cells)


def rand_shape(rnd, kind, maxw=6, maxh=4):
    """Rectilinear shape made of squares (no holes)."""
    while True:
        if kind == "L":
            w2, h2 = rnd.randint(3, maxw), rnd.randint(1, maxh - 1)
            w1, h1 = rnd.randint(1, w2 - 1), rnd.randint(1, maxh - h2)
            cells = rect_cells(w1, h1) | rect_cells(w2, h2, 0, h1)
        elif kind == "T":
            w = rnd.choice([3, 5]) if maxw >= 5 else 3
            sw = rnd.choice([1, w - 2]) if w > 3 else 1
            top = rnd.randint(1, 2)
            st = rnd.randint(1, maxh - top)
            cells = rect_cells(w, top) | rect_cells(sw, st, (w - sw) // 2, top)
        elif kind == "U":
            w, h = rnd.randint(3, maxw), rnd.randint(2, maxh)
            nw = rnd.randint(1, w - 2)
            nd = rnd.randint(1, h - 1)
            c0 = rnd.randint(1, w - 1 - nw)
            cells = rect_cells(w, h) - rect_cells(nw, nd, c0, 0)
        elif kind == "step":
            ws = [rnd.randint(1, 2) for _ in range(3)]
            hs = sorted(rnd.sample(range(1, maxh + 1), 3), reverse=True)
            cells, c = set(), 0
            for w, h in zip(ws, hs):
                cells |= rect_cells(w, h, c, maxh - h)
                c += w
        else:
            raise ValueError(kind)
        cells = flipcells(cells, rnd)
        w, h = size(cells)
        if w <= maxw and h <= maxh:
            return cells


# ------------------------------------------------------------ set 1: perimeter of rectangles and squares

# ------------------------------------------------------------ irregular shapes on a cm grid
def blob_r(params, th):
    R, sx, sy, waves = params
    r = 1 + sum(a * math.sin(k * th + ph) for a, k, ph in waves)
    return R * r


def inside_blob(params, cx, cy, x, y):
    R, sx, sy, waves = params
    dx, dy = (x - cx) / sx, (y - cy) / sy
    return math.hypot(dx, dy) < blob_r(params, math.atan2(dy, dx))


def blob_poly(params, cx, cy, n=180):
    R, sx, sy, waves = params
    out = []
    for i in range(n):
        th = 2 * math.pi * i / n
        r = blob_r(params, th)
        out.append((cx + sx * r * math.cos(th), cy + sy * r * math.sin(th)))
    return out


def coverage(params, cx, cy, cols, rows, S):
    """Fraction of each grid square covered by the blob (numpy array rows x cols)."""
    R, sx, sy, waves = params
    xs = (np.arange(cols * S) + 0.5) / S
    ys = (np.arange(rows * S) + 0.5) / S
    X, Y = np.meshgrid(xs, ys)
    dx, dy = (X - cx) / sx, (Y - cy) / sy
    th = np.arctan2(dy, dx)
    r = R * (1 + sum(a * np.sin(k * th + ph) for a, k, ph in waves))
    ins = (np.hypot(dx, dy) < r).astype(float)
    return ins.reshape(rows, S, cols, S).mean(axis=(1, 3))


def blob_counts(params, cx, cy, cols, rows, S=12):
    """(whole squares, half-or-more part squares, less-than-half part squares, coverage sum).
    Returns None when a square is close to half covered (hard to judge by eye)."""
    for s in (S, 40):                       # quick check, then a fine check
        fr = coverage(params, cx, cy, cols, rows, s)
        if ((fr > 0.33) & (fr < 0.67)).any():
            return None
    whole = int((fr == 1).sum())
    more = int(((fr >= 0.67) & (fr < 1)).sum())
    less = int(((fr > 0) & (fr <= 0.33)).sum())
    return whole, more, less, float(fr.sum())


def make_blob(rnd, used, nmin=10, nmax=26):
    for _ in range(40000):
        R = rnd.uniform(1.9, 3.0)
        sx, sy = rnd.uniform(1.0, 1.5), rnd.uniform(0.8, 1.05)
        waves = [(rnd.uniform(0.06, 0.16), 2, rnd.uniform(0, 6.28)), (rnd.uniform(0.04, 0.12), 3, rnd.uniform(0, 6.28)),
                 (rnd.uniform(0.0, 0.06), 5, rnd.uniform(0, 6.28))]
        params = (R, sx, sy, waves)
        ext = max(blob_r(params, 2 * math.pi * i / 90) for i in range(90))
        cols = int(math.ceil(2 * ext * sx)) + 2
        rows = int(math.ceil(2 * ext * sy)) + 2
        if cols > 10 or rows > 7:
            continue
        cx = cols / 2 + rnd.uniform(-0.3, 0.3)
        cy = rows / 2 + rnd.uniform(-0.3, 0.3)
        poly = blob_poly(params, cx, cy)
        if min(x for x, y in poly) < 0.5 or max(x for x, y in poly) > cols - 0.5:
            continue
        if min(y for x, y in poly) < 0.5 or max(y for x, y in poly) > rows - 0.5:
            continue
        res = blob_counts(params, cx, cy, cols, rows)
        if not res:
            continue
        whole, more, less, tot = res
        N = whole + more
        if not (nmin <= N <= nmax) or more < 3 or less < 3 or abs(tot - N) > 1.5:
            continue
        key = (whole, more, less)
        if key in used:
            continue
        used.add(key)
        return poly, cols, rows, whole, more, less
    raise RuntimeError("no blob")


def blob_svg(poly, cols, rows, label, cell=22):
    m = 6
    W, H = cols * cell + 2 * m, rows * cell + 2 * m
    pts = " ".join("%.1f,%.1f" % (m + x * cell, m + y * cell) for x, y in poly)
    g = ["<polygon points='%s' fill='%s'/>" % (pts, FILL)]
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    g.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (pts, GREEN))
    return svg_wrap(W, H, "".join(g), label)


def pick_l(rnd, used, lo=(7, 5), hi=(14, 10)):
    while True:
        Wt, Ht = rnd.randint(lo[0], hi[0]), rnd.randint(lo[1], hi[1])
        if Wt <= Ht or Wt / Ht > 2:
            continue
        cw = rnd.randint(int(math.ceil(Wt * 0.35)), int(Wt * 0.6))
        ch = rnd.randint(int(math.ceil(Ht * 0.35)), int(Ht * 0.6))
        if cw == Wt - cw or ch == Ht - ch or cw == ch or (Wt, Ht, cw, ch) in used:
            continue
        used.add((Wt, Ht, cw, ch))
        return Wt, Ht, cw, ch


def pick_step(rnd, used):
    while True:
        W, H = rnd.randint(9, 15), rnd.randint(6, 10)
        if W / H > 2.2 or W <= H:
            continue
        x1 = rnd.randint(3, W - 6)
        x2 = rnd.randint(x1 + 3, W - 3)
        y1 = rnd.randint(2, H - 4)
        y2 = rnd.randint(y1 + 2, H - 2)
        sides = step_sides(W, H, x1, x2, y1, y2)
        if len(set(sides)) < 6 or (W, H, x1, x2, y1, y2) in used:
            continue
        return W, H, x1, x2, y1, y2


def l_figure(rnd, used, labeller, label="rectilinear L-shape with side lengths"):
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used)
        corner = rnd.choice(["tr", "tl", "br", "bl"])
        sides = l_sides(Wt, Ht, cw, ch)
        svg = l_svg(Wt, Ht, cw, ch, corner, labeller(sides), label)
        if svg:
            return Wt, Ht, cw, ch, sides, svg
    raise RuntimeError("no L fits")



def strip(shapes):
    """Place shapes side by side, 1 square apart, with a 1-square margin."""
    out, c = [], 1
    maxh = max(size(s)[1] for s in shapes)
    for s in shapes:
        w, h = size(s)
        out.append((s, c, 1 + maxh - h))
        c += w + 1
    return out, c, maxh + 2


# ------------------------------------------------------------ set 1: perimeter by adding the sides
def set_add_sides(rnd):
    its = []
    rects = [(w, h) for w in range(2, 8) for h in range(2, 5) if w > h and w * h != 2 * (w + h)]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:6]):
        if i % 3 == 2:
            w, h = h, w                                   # some stand up tall
        cells = rect_cells(w, h)
        p, a, b = 2 * (w + h), w * h, border(cells)
        q = (fig(one_grid(cells, "rectangle %d by %d on a centimetre grid" % (w, h))) +
             "Each square has sides of 1 cm. What is the perimeter of the rectangle?")
        pool = ["%d cm" % b, "%d cm" % a, "%d cm" % (w + h), "%d cm²" % p, "%d cm" % (p - 2)]
        r = i % 3
        pool = pool[r:3] + pool[:r] + pool[3:]
        e = ("Count the 1 cm sides all the way around: %d + %d + %d + %d = %d cm. "
             "Do not count the squares: a corner square has 2 sides on the edge." % (w, h, w, h, p))
        its.append(mcq(q, "%d cm" % p, pool, e, rnd))
    sizes = [(9, 4, "cm"), (12, 5, "cm"), (8, 6, "cm"), (15, 7, "cm"), (14, 9, "m"), (20, 6, "m")]
    rnd.shuffle(sizes)
    for i, (L, W, u) in enumerate(sizes):
        P = 2 * (L + W)
        if i < 4:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
                 "What is the perimeter of this rectangle?")
        else:
            q = "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
        pool = ["%d %s" % (L + W, u), "%d %s" % (2 * L + W, u), "%d %s" % (L * W, u), "%d %s" % (P, SQ[u])]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("A rectangle has 2 long sides and 2 short sides: %d + %d + %d + %d = %d %s. "
             "Adding only %d + %d = %d leaves out two sides." % (L, W, L, W, P, u, L, W, L + W))
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (s, u) in enumerate([(6, "cm"), (9, "m"), (11, "cm")]):
        P = 4 * s
        if k < 2:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u), max_h=95)) +
                 "This is a square. What is its perimeter?")
        else:
            q = "A square has sides of %d %s. What is its perimeter?" % (s, u)
        pool = ["%d %s" % (s * s, u), "%d %s" % (2 * s, u), "%d %s" % (3 * s, u), "%d %s" % (P, SQ[u])]
        if k % 2:
            pool = [pool[1], pool[2], pool[0]]
        e = ("All 4 sides of a square are the same length: %d + %d + %d + %d = %d %s."
             % (s, s, s, s, P, u))
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for (a, b, c, u) in [(6, 8, 10, "cm"), (7, 7, 9, "m")]:
        P = a + b + c
        q = "A triangle has sides of %d %s, %d %s and %d %s. What is its perimeter?" % (a, u, b, u, c, u)
        e = "A triangle has 3 sides. Add all 3: %d + %d + %d = %d %s." % (a, b, c, P, u)
        pool = ["%d %s" % (a + b, u), "%d %s" % (P + max(a, b, c), u), "%d %s" % (P, SQ[u]), "%d %s" % (3 * c, u)]
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for (sd, u, what) in [((3, 5, 4, 6), "m", "A garden bed"), ((12, 9, 15, 10), "cm", "A four-sided card"),
                          ((8, 5, 8, 7), "m", "A school vegetable patch")]:
        P = sum(sd)
        q = ("%s has four sides: %s. What is its perimeter?"
             % (what, ", ".join("%d %s" % (v, u) for v in sd[:3]) + " and %d %s" % (sd[3], u)))
        e = "Add all 4 sides: %s = %d %s. Every side counts, even when they are all different." % (plus(sd), P, u)
        pool = ["%d %s" % (P - sd[3], u), "%d %s" % (2 * (sd[0] + sd[1]), u), "%d %s" % (P, SQ[u]),
                "%d %s" % (P - sd[0], u)]
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Perimeter: add all the sides", "items": its}


# ------------------------------------------------------------ set 2: rectilinear shapes and missing sides
def set_rectilinear(rnd):
    its = []
    used = set()
    seen = set()
    kinds = ["L", "T", "U", "step", "L", "U"]
    for i in range(6):
        while True:
            cells = rand_shape(rnd, kinds[i])
            p, a, b = perim(cells), len(cells), border(cells)
            if cells in seen or p == a or len(cells) < 5 or b == p - 2 or b == p + 2:
                continue
            seen.add(cells)
            break
        q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
             "Each square has sides of 1 cm. What is the perimeter of the shape?")
        e = ("Go around the outside and count every 1 cm side, including the short steps: %d cm. "
             "There are %d squares, but counting squares gives the area, not the perimeter." % (p, a))
        its.append(mcq(q, "%d cm" % p, ["%d cm" % b, "%d cm" % a, "%d cm" % (p - 2), "%d cm" % (p + 2)], e, rnd))
    for i in range(4):
        u = ["cm", "m"][i % 2]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lambda s: ["%d %s" % (v, u) for v in s])
        P = sum(sides)
        e = ("Add all 6 sides: %s = %d %s. Do not skip the two short sides at the inside corner." % (plus(sides), P, u))
        cands = ["%d %s" % (P - cw - ch, u), "%d %s" % (Wt + Ht, u), "%d %s" % (P - sides[1], u), "%d %s" % (P, SQ[u])]
        its.append(mcq(fig(svg) + "What is the perimeter of this shape?", "%d %s" % (P, u), cands, e, rnd))
    for i in range(2):
        u = ["m", "cm"][i]
        for _ in range(5000):
            W, H, x1, x2, y1, y2 = pick_step(rnd, used)
            sides = step_sides(W, H, x1, x2, y1, y2)
            svg = step_svg(W, H, x1, x2, y1, y2, ["%d %s" % (v, u) for v in sides], i == 1)
            if svg:
                used.add((W, H, x1, x2, y1, y2))
                break
        else:
            raise RuntimeError("no step fits")
        P = sum(sides)
        e = "Add all 8 sides: %s = %d %s." % (plus(sides), P, u)
        cands = ["%d %s" % (W + H, u), "%d %s" % (P - sides[2] - sides[3], u), "%d %s" % (P - sides[4], u),
                 "%d %s" % (P, SQ[u])]
        its.append(mcq(fig(svg) + "What is the perimeter of this shape?", "%d %s" % (P, u), cands, e, rnd))
    for i in range(4):
        u = ["cm", "m", "cm", "m"][i]
        mi = [0, 3, 3, 0][i]

        def lab(s, mi=mi, u=u):
            out = ["%d %s" % (v, u) for v in s]
            out[mi] = "? %s" % u
            return out
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lab)
        if mi == 0:
            ans, big, small = Wt - cw, Wt, cw
            e = ("Going across, the two top sides (? and %d %s) together are as long as the bottom side, %d %s. "
                 "%d − %d = %d %s." % (cw, u, Wt, u, Wt, cw, ans, u))
        else:
            ans, big, small = Ht - ch, Ht, ch
            e = ("Going up and down, the two short sides (? and %d %s) together are as long as the long side, %d %s. "
                 "%d − %d = %d %s." % (ch, u, Ht, u, Ht, ch, ans, u))
        cands = ["%d %s" % (big + small, u), "%d %s" % (small, u), "%d %s" % (big, u), "%d %s" % (ans + 1, u)]
        its.append(mcq(fig(svg) + "What is the length of the side marked ?", "%d %s" % (ans, u), cands, e, rnd))
    for i in range(4):
        u = ["m", "cm"][i % 2]
        hide = [(0, 3), (1, 2)][i % 2]

        # only ONE side is not labelled: find it, then add all the sides
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lambda s, hide=hide, u=u:
                                              ["" if j == hide[0] else "%d %s" % (v, u) for j, v in enumerate(s)])
        P = sum(sides)
        shown = P - sides[hide[0]]
        j = hide[0]
        if j == 0:
            miss = "%d − %d = %d %s" % (Wt, cw, Wt - cw, u)
        else:
            miss = "%d − %d = %d %s" % (Ht, Ht - ch, ch, u)
        e = ("First find the missing side: %s. Then add all 6 sides: %s = %d %s." % (miss, plus(sides), P, u))
        cands = ["%d %s" % (shown, u), "%d %s" % (Wt + Ht, u), "%d %s" % (P + 1, u), "%d %s" % (P, SQ[u])]
        if i % 2:
            cands = [cands[1], cands[0]] + cands[2:]
        q = fig(svg) + "One side is not labelled. What is the perimeter of the shape?"
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Rectilinear shapes and missing sides", "items": its}


# ------------------------------------------------------------ set 3: area by counting squares and half squares
HALF_SHAPES = [
    [(0, 0), (0, 4), (4, 4)],                                   # right-angled triangle
    [(0, 2), (2, 0), (4, 2), (4, 5), (0, 5)],                   # house
    [(0, 3), (3, 0), (6, 0), (6, 3)],                           # trapezium
    [(0, 0), (4, 0), (5, 1), (5, 4), (0, 4)],                   # rectangle with one corner cut
    [(2, 0), (4, 2), (2, 4), (0, 2)],                           # diamond
    [(0, 0), (3, 0), (3, 2), (5, 2), (5, 3), (4, 4), (0, 4)],   # L with a cut corner
]
HALF_NAMES = ["triangle", "house shape", "trapezium", "shape", "diamond shape", "shape"]


def set_area(rnd):
    its = []
    seen = set()
    rects = [(w, h) for w in range(3, 8) for h in range(2, 5) if w > h]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:4]):
        if i % 2:
            w, h = h, w
        cells = frozenset(rect_cells(w, h))
        seen.add(cells)
        a, p = w * h, 2 * (w + h)
        un = "squares" if i < 2 else "cm²"
        if un == "squares":
            q = fig(one_grid(cells, "rectangle %d by %d on a squared grid" % (w, h))) + "What is the area of the shaded rectangle?"
        else:
            q = (fig(one_grid(cells, "rectangle %d by %d on a centimetre grid" % (w, h))) +
                 "Each square is 1 cm². What is the area of the shaded rectangle?")
        e = ("Count the squares inside: %d rows of %d squares. %d × %d = %d %s. "
             "(%d is the number of 1-unit sides around the edge: that is the perimeter.)" % (h, w, h, w, a, un, p))
        pool = ["%d %s" % (p, un), "%d %s" % (a - w, un), "%d %s" % (w + h, un), "%d %s" % (a + h, un)]
        if un == "cm²":
            pool.insert(1, "%d cm" % a)
        r = i % 4
        pool = pool[r:] + pool[:r]
        its.append(mcq(q, "%d %s" % (a, un), pool, e, rnd))
    kinds = ["L", "T", "U", "step", "L", "U", "step"]
    for i, kd in enumerate(kinds):
        while True:
            cells = rand_shape(rnd, kd)
            a, p = len(cells), perim(cells)
            w, h = size(cells)
            if cells in seen or a == p or a < 6 or w * h in (a + 1, a - 1):
                continue
            seen.add(cells)
            break
        un = "squares" if i < 3 else "cm²"
        if un == "squares":
            q = fig(one_grid(cells, "rectilinear shape on a squared grid")) + "What is the area of the shaded shape?"
        else:
            q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
                 "Each square is 1 cm². What is the area of the shaded shape?")
        e = ("Count the shaded squares, row by row: there are %d, so the area is %d %s. "
             "Count each square once." % (a, a, un))
        if un == "cm²":
            e += " (%d cm is the perimeter.)" % p
        pool = ["%d %s" % (p, un), "%d %s" % (w * h, un), "%d %s" % (a + 1, un), "%d %s" % (a - 1, un)]
        if un == "cm²":
            pool = [pool[0], "%d cm" % a, pool[1], pool[2]]
        if i % 2:
            pool = [pool[1], pool[0]] + pool[2:]
        its.append(mcq(q, "%d %s" % (a, un), pool, e, rnd))
    order = list(range(len(HALF_SHAPES)))
    rnd.shuffle(order)
    for n, k in enumerate(order):
        poly = HALF_SHAPES[k]
        full, halves = poly_counts(poly)
        A = poly_area(poly)
        un = "squares" if n < 3 else "cm²"
        bw, bh = max(x for x, y in poly), max(y for x, y in poly)
        if un == "squares":
            q = (fig(one_grid(poly, "%s with half squares on a squared grid" % HALF_NAMES[k])) +
                 "What is the area of the shaded %s? Two half squares make one whole square." % HALF_NAMES[k])
        else:
            q = (fig(one_grid(poly, "%s with half squares on a centimetre grid" % HALF_NAMES[k])) +
                 "Each square is 1 cm². What is the area of the shaded %s?" % HALF_NAMES[k])
        hs = "%d half squares" % halves if halves > 1 else "1 half square"
        if halves == 1:
            mk = "1 half square is ½ of a square."
        else:
            hv = Fraction(halves, 2)
            mk = "%d halves make %s %s." % (halves, half(hv), "square" if hv == 1 else "squares")
        e = ("There are %d whole squares and %s. %s %d + %s = %s %s."
             % (full, hs, mk, full, half(Fraction(halves, 2)), half(A), un))
        pool = ["%s %s" % (half(full), un), "%s %s" % (half(full + halves), un), "%s %s" % (half(bw * bh), un),
                "%s %s" % (half(A + 1), un)]
        its.append(mcq(q, "%s %s" % (half(A), un), pool, e, rnd))
    P = People(random.Random(41))
    for (n, he, his), (rows, cols, thing) in zip([P.next() for _ in range(3)],
                                                [(4, 6, "square tiles"), (3, 8, "square sticky notes"),
                                                 (5, 7, "square cards")]):
        a = rows * cols
        q = ("%s makes a rectangle from %s. It has %d rows with %d %s in each row. What is its area in squares?"
             % (n, thing, rows, cols, thing.split()[-1]))
        e = ("Count the squares, or count in rows: %d rows of %d is %d × %d = %d squares."
             % (rows, cols, rows, cols, a))
        its.append(mcq(q, "%d squares" % a, ["%d squares" % (rows + cols), "%d squares" % (2 * (rows + cols)),
                                             "%d squares" % (a - cols)], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area: count squares and half squares", "items": its}


# ------------------------------------------------------------ set 4: estimate area, compare and choose units
BLOB_THINGS = ["leaf", "puddle", "handprint", "ink blot", "lake", "footprint"]


def set_estimate(rnd, fixed_pos):
    its = []
    used_blobs = set()
    for k, thing in enumerate(BLOB_THINGS):
        poly, cols, rows, whole, more, less = make_blob(rnd, used_blobs, 8, 20)
        N, T = whole + more, whole + more + less
        svg = blob_svg(poly, cols, rows, "irregular shape of %s %s on a squared grid"
                       % ("an" if thing[0] in "aeiou" else "a", thing))
        u = "m" if thing == "lake" else "cm"
        what = ("This map of a %s is drawn on a grid. Each square is 1 %s." % (thing, SQ[u]) if thing == "lake"
                else "Each square is 1 %s." % SQ[u])
        q = (fig(svg) + "%s Estimate the area of the %s. Count whole squares and squares that are half or more "
             "covered." % (what, thing))
        e = ("Whole squares: %d. Squares half or more covered: %d. Estimate: %d + %d = %d %s. "
             "Squares less than half covered (%d) are not counted." % (whole, more, whole, more, N, SQ[u], less))
        cands = ["%d %s" % (whole, SQ[u]), "%d %s" % (T, SQ[u]), "%d %s" % (whole + less, SQ[u]), "%d %s" % (N, u)]
        r = k % 3
        cands = cands[r:3] + cands[:r] + cands[3:]
        its.append(mcq(q, "%d %s" % (N, SQ[u]), cands, e, rnd))
    its.append(mcq("You estimate the area of a curved shape on a squared grid. Which squares do you count?",
                   "Whole and half or more covered",
                   ["Only whole squares", "Every square it touches", "Only part squares"],
                   "Count every whole square, and count a square as 1 if half or more of it is covered. "
                   "Leave out squares that are less than half covered. The bits you count and leave out "
                   "roughly balance.", rnd))
    # compare shapes A–D (answers fixed to the picture order)
    kinds = ["L", "T", "U", "step"]
    lib = set()
    for _ in range(3000):
        if rnd.random() < 0.25:
            lib.add(frozenset(rect_cells(rnd.randint(1, 4), rnd.randint(1, 3))))
        else:
            lib.add(rand_shape(rnd, rnd.choice(kinds), maxw=4, maxh=3))
    lib = sorted((x for x in lib if len(x) >= 4), key=lambda x: sorted(x))
    groups = {}
    for x in lib:
        groups.setdefault(len(x), []).append(x)
    groups = {k: v for k, v in groups.items() if len({perim(x) for x in v}) >= 3 and len(v) >= 6}
    tasks = [("area", "largest"), ("area", "smallest"), ("perim", "longest")]
    for (what, word), target in zip(tasks, fixed_pos):
        for _ in range(20000):
            if what == "perim":
                N = rnd.choice([g for g in groups if g >= 5])
                shapes = rnd.sample(groups[N], 4)
            else:
                shapes = rnd.sample(lib, 4)
            A = [len(s) for s in shapes]
            Pm = [perim(s) for s in shapes]
            if what == "area" and len(set(A)) < 4:
                continue
            v = Pm if what == "perim" else A
            best = max(v) if word in ("largest", "longest") else min(v)
            if v.count(best) != 1 or v.index(best) != target:
                continue
            if what == "area" and Pm.index(max(Pm)) == target and Pm.count(max(Pm)) == 1:
                continue
            if what == "area" and max(A) - min(A) > 4:
                continue
            break
        else:
            raise RuntimeError("no strip")
        placed, cols, rows = strip(shapes)
        svg = grid_svg(cols, rows, placed, 18, "four shapes A to D on a centimetre grid", letters="ABCD")
        if what == "area":
            q = fig(svg) + "Each square is 1 cm². Which shape has the %s area?" % word
            e = ("Count the squares in each shape: A %d, B %d, C %d, D %d. Shape %s has the %s area (%d cm²)."
                 % (A[0], A[1], A[2], A[3], "ABCD"[target], word, A[target]))
        else:
            q = fig(svg) + "Each shape has an area of %d cm². Which shape has the %s perimeter?" % (A[0], word)
            e = ("Count the 1 cm sides around each shape: A %d cm, B %d cm, C %d cm, D %d cm. "
                 "The same area can have different perimeters. Shape %s has the %s (%d cm)."
                 % (Pm[0], Pm[1], Pm[2], Pm[3], "ABCD"[target], word, Pm[target]))
        its.append({"q": q, "c": ["A", "B", "C", "D"], "a": target, "e": e, "fixed": True})
    # choosing a unit
    U4 = ["cm", "m", "cm²", "m²"]
    for thing, right, why in [
        ("the area of a classroom floor", "m²", "A floor is big and we cover the space inside it, so use square metres."),
        ("the area of a postage stamp", "cm²", "A stamp is small and we cover the space inside it, so use square centimetres."),
        ("the perimeter of the school basketball court", "m", "Perimeter is a length around the edge. A court is big, so use metres."),
        ("the perimeter of a photo", "cm", "Perimeter is a length around the edge. A photo is small, so use centimetres."),
        ("the area of a page in your maths book", "cm²", "A page is small and area is the space inside, so use square centimetres."),
        ("the area of a netball court", "m²", "A netball court is big and area is the space inside, so use square metres."),
    ]:
        q = "Which unit is best for measuring %s?" % thing
        its.append(mcq(q, right, [x for x in U4 if x != right], why + " cm and m are for lengths; cm² and m² are for areas.", rnd))
    # informal units and sensible estimates
    its.append(mcq("Harper covers her desk with sticky notes, with no gaps or overlaps. She uses 4 rows of 6 notes. "
                   "What is the area of her desk in sticky notes?", "24 sticky notes",
                   ["10 sticky notes", "20 sticky notes", "18 sticky notes"],
                   "4 rows of 6: 4 × 6 = 24 sticky notes. 20 is the number of notes around the edge (the perimeter "
                   "idea); 10 is only 4 + 6.", rnd))
    its.append(mcq("Leo and Mia both cover the same table with paper squares. Leo needs 12 squares. Mia needs 48 "
                   "squares. Why?", "Mia’s squares are smaller",
                   ["Mia’s squares are bigger", "Leo counted wrongly", "Mia’s table is bigger"],
                   "It is the same table, so the area is the same. Smaller squares are needed in bigger numbers. "
                   "That is why we use a standard unit such as cm² or m².", rnd))
    its.append(mcq("About how big is the floor of a classroom?", "About 60 m²",
                   ["About 6 m²", "About 600 m²", "About 60 cm²"],
                   "A classroom is roughly 8 m by 8 m: 8 rows of 8 one-metre squares is 64, so about 60 m². "
                   "6 m² is a small rug, 600 m² is bigger than a netball court.", rnd))
    its.append(mcq("About how big is the cover of an exercise book?", "About 500 cm²",
                   ["About 5 cm²", "About 50 m²", "About 50 cm"],
                   "An exercise book is about 25 cm by 20 cm: 20 rows of 25 one-centimetre squares is 500 cm². "
                   "Area needs a square unit, and 50 m² would be a whole room.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Estimate area and choose the unit", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    n, he, his = P.next()
    L, W = 4, 2
    add("%s’s family is building a garden bed %d m long and %d m wide. How much timber edging goes all the way "
        "around it?" % (n, L, W), "%d m" % (2 * (L + W)),
        ["%d m" % (L * W), "%d m" % (L + W), "%d m" % (2 * L + W)],
        "The edging goes along all 4 sides: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    L, W, g = 12, 8, 2
    Pm = 2 * (L + W)
    add("A rectangular vegetable garden is %d m long and %d m wide. A fence goes all the way around, except for a gate "
        "that is %d m wide. How much fence is needed?" % (L, W, g), "%d m" % (Pm - g),
        ["%d m" % Pm, "%d m" % (L + W - g), "%d m" % (Pm + g)],
        "Perimeter: %d + %d + %d + %d = %d m. There is no fence across the gate: %d − %d = %d m."
        % (L, W, L, W, Pm, Pm, g, Pm - g))
    n, he, his = P.next()
    s, pl = 6, 2
    add("%s’s family builds a square chook pen with sides of %d m. Each fence panel is %d m long. How many panels go "
        "all the way around?" % (n, s, pl), "%d panels" % (4 * s // pl),
        ["%d panels" % (4 * s), "%d panels" % (s * s // pl), "%d panels" % (s // pl * 2)],
        "Perimeter: %d + %d + %d + %d = %d m. Each panel is %d m: %d ÷ %d = %d panels."
        % (s, s, s, s, 4 * s, pl, 4 * s, pl, 4 * s // pl))
    used = set()
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used, (9, 6), (14, 9))
        sides = l_sides(Wt, Ht, cw, ch)
        labs = ["%d m" % v for v in sides]
        labs[0] = "? m"
        svg = l_svg(Wt, Ht, cw, ch, "tl", labs, "plan of a rectilinear L-shaped garden bed")
        if svg:
            break
    Pm = sum(sides)
    add(fig(svg) + "This is the plan of an L-shaped garden bed. How much edging goes all the way around it?",
        "%d m" % Pm, ["%d m" % (Pm - sides[0]), "%d m" % (Wt + Ht), "%d m" % (Pm - sides[0] - sides[1])],
        "Missing side: %d − %d = %d m. Add all 6 sides: %s = %d m." % (Wt, cw, Wt - cw, plus(sides), Pm))
    r, c = 7, 9
    add("A classroom floor is covered with square carpet tiles. Each tile is 1 m long and 1 m wide. "
        "There are %d rows of %d tiles. What is the area of the floor?" % (r, c), "%d m²" % (r * c),
        ["%d m²" % (r + c), "%d m²" % (2 * (r + c)), "%d m" % (r * c)],
        "Each tile is 1 m², so count the tiles: %d rows of %d is %d × %d = %d m²." % (r, c, r, c, r * c))
    add("The teacher has 20 carpet squares. Each is 1 m². The reading corner needs 4 rows of 4 squares. How many "
        "carpet squares are left over?", "4 squares", ["16 squares", "12 squares", "8 squares"],
        "Reading corner: 4 rows of 4 = 16 squares. Left over: 20 − 16 = 4 squares.")
    add("A classroom floor plan is drawn on a grid. Each square is 1 m². The floor covers 30 whole squares and "
        "4 half squares. What is the area of the floor?", "32 m²", ["34 m²", "30 m²", "38 m²"],
        "Two half squares make one whole square, so 4 half squares make 2. Area: 30 + 2 = 32 m².")
    L, W = 28, 15
    add("The school basketball court is %d m long and %d m wide. The class jogs once around the edge. "
        "How far is that?" % (L, W), "%d m" % (2 * (L + W)),
        ["%d m" % (L + W), "%d m" % (2 * L + W), "%d m" % (L * W)],
        "Once around is the perimeter: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    n, he, his = P.next()
    L, W = 60, 40
    add("At the athletics carnival warm-up, %s jogs 2 times around a rectangular field. The field is %d m long and "
        "%d m wide. How far does %s jog?" % (n, L, W, he), "%d m" % (4 * (L + W)),
        ["%d m" % (2 * (L + W)), "%d m" % (2 * (2 * L + W)), "%d m" % (L + W)],
        "Once around: %d + %d + %d + %d = %d m. Two times around: 2 × %d = %d m."
        % (L, W, L, W, 2 * (L + W), 2 * (L + W), 4 * (L + W)))
    n, he, his = P.next()
    L, W = 20, 15
    add("%s glues ribbon around the edge of a photo frame. The frame is %d cm long and %d cm wide. "
        "How much ribbon does %s need?" % (n, L, W, he), "%d cm" % (2 * (L + W)),
        ["%d cm" % (L + W), "%d cm" % (L * W), "%d cm" % (2 * L + W)],
        "Ribbon goes around the edge, so find the perimeter: %d + %d + %d + %d = %d cm." % (L, W, L, W, 2 * (L + W)))
    L, W = 120, 90
    add("A pinboard in the classroom is %d cm long and %d cm wide. The teacher staples a paper border around "
        "the edge. How long is the border?" % (L, W), "%d cm" % (2 * (L + W)),
        ["%d cm" % (L + W), "%d cm" % (2 * L + W), "%d cm" % (L + 2 * W)],
        "Border around the edge = perimeter: %d + %d + %d + %d = %d cm." % (L, W, L, W, 2 * (L + W)))
    ch4 = ["Perimeter, in cm", "Area, in cm²", "Perimeter, in cm²", "Area, in cm"]
    n, he, his = P.next()
    add("%s wants to put coloured tape around the edge of a poster. What should %s work out?" % (n, he),
        ch4[0], ch4[1:], "Tape goes around the edge, so find the perimeter. Perimeter is a length, so it is in cm.")
    n, he, his = P.next()
    add("%s wants to cover the front of a book with contact paper. What should %s work out?" % (n, he),
        ch4[1], [ch4[0], ch4[2], ch4[3]],
        "Covering the space inside a shape is area. Area is counted in squares, so it is in cm².")
    add("A square sandpit has a perimeter of 20 m. How long is each side?", "5 m",
        ["10 m", "16 m", "80 m"],
        "A square has 4 equal sides: 20 ÷ 4 = 5 m. Check: 5 + 5 + 5 + 5 = 20 m.")
    Pm, L = 30, 9
    W = Pm // 2 - L
    add("A rectangular flower bed has a perimeter of %d m. One side is %d m long. How long is the side next to it?"
        % (Pm, L), "%d m" % W, ["%d m" % (Pm - L), "%d m" % (Pm - 2 * L), "%d m" % (Pm // 2)],
        "The two %d m sides make %d m. %d − %d = %d m for the other two sides, so each is %d ÷ 2 = %d m. "
        "Check: %d + %d + %d + %d = %d m." % (L, 2 * L, Pm, 2 * L, Pm - 2 * L, Pm - 2 * L, W, L, W, L, W, Pm))
    n, he, his = P.next()
    add("%s has 16 m of fence to make a rectangular pen for %s guinea pigs. Which pen gives them the most space?"
        % (n, his), "4 m by 4 m", ["7 m by 1 m", "6 m by 2 m", "5 m by 3 m"],
        "All four pens use 16 m of fence. Count the 1 m squares inside: 7 × 1 = 7, 6 × 2 = 12, 5 × 3 = 15, "
        "4 × 4 = 16 m². The square has the most space.")
    r, c, k = 6, 4, 5
    add("A school vegetable patch is marked into 1 m squares: %d rows of %d squares. Tomatoes grow in %d squares and "
        "lettuce in the rest. What area is lettuce?" % (r, c, k), "%d m²" % (r * c - k),
        ["%d m²" % (r * c), "%d m²" % (r * c + k), "%d m²" % (2 * (r + c) - k)],
        "Whole patch: %d × %d = %d m². Take away the tomatoes: %d − %d = %d m²." % (r, c, r * c, r * c, k, r * c - k))
    n, he, his = P.next()
    L, W = 20, 12
    Pm = 2 * (L + W)
    add("%s has 1 m of ribbon. %s puts ribbon around the edge of a card that is %d cm by %d cm. "
        "How much ribbon is left?" % (n, cap(he), L, W), "%d cm" % (100 - Pm),
        ["%d cm" % (100 - L - W), "%d cm" % (100 - 2 * L - W), "%d cm" % Pm],
        "1 m = 100 cm. Perimeter of the card: %d + %d + %d + %d = %d cm. Left: 100 − %d = %d cm."
        % (L, W, L, W, Pm, Pm, 100 - Pm))
    add("A cricket pitch is about 20 m long and 3 m wide. The groundskeeper walks once around its edge. "
        "About how far is that?", "46 m", ["23 m", "60 m", "43 m"],
        "Perimeter: 20 + 3 + 20 + 3 = 46 m. 60 is 20 × 3, which is the area in m².")
    n, he, his = P.next()
    add("%s’s bedroom floor is 4 m by 3 m. Carpet squares are 1 m by 1 m. How many carpet squares cover the floor?"
        % n, "12 carpet squares", ["14 carpet squares", "7 carpet squares", "10 carpet squares"],
        "3 rows of 4 squares: 3 × 4 = 12 carpet squares, so the area is 12 m². "
        "14 is the perimeter in metres (4 + 3 + 4 + 3).")
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems: fences, gardens and carpet", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_L = frozenset(rect_cells(2, 2) | rect_cells(5, 2, 0, 2))


def lesson_blob():
    rnd = random.Random(4813 + 7)
    poly, cols, rows, whole, more, less = make_blob(rnd, set(), 10, 16)
    return blob_svg(poly, cols, rows, "irregular shape of a leaf on a squared grid"), whole, more, less


def body_html():
    assert perim(LESSON_L) == 18 and len(LESSON_L) == 14
    assert poly_counts(HALF_SHAPES[1]) == (14, 4)
    lab = ["4 m", "3 m", "5 m", "? m", "9 m", "7 m"]
    assert l_sides(9, 7, 5, 3) == [4, 3, 5, 4, 9, 7]
    bsvg, whole, more, less = lesson_blob()
    return (
        "<h2>Perimeter and area</h2>"
        "<p><b>Perimeter</b> is the distance <b>all the way around</b> a shape. It is a length, so it is in cm or m.</p>"
        "<p><b>Area</b> is the space <b>inside</b> a shape. In Year 4 we find it by <b>counting squares</b>. "
        "If each square is 1 cm² (1 square centimetre), the area is in cm². Big spaces such as a floor are "
        "measured in m² (square metres).</p>"
        "<h2>Perimeter: add all the sides</h2>"
        "<p>Add every side. A rectangle has 2 long sides and 2 short sides.</p>"
        "<figure class='sn-fig'>" + rect_svg(9, 4, "9 cm", "4 cm", "rectangle 9 cm by 4 cm") +
        "<figcaption>9 + 4 + 9 + 4 = 26 cm. Not 9 + 4 = 13: that is only two sides.</figcaption></figure>"
        "<h2>Perimeter on a grid</h2>"
        "<p>Count the sides of the squares around the edge, not the squares. A corner square has 2 sides on the edge.</p>"
        "<figure class='sn-fig'>" + one_grid(LESSON_L, "rectilinear shape on a centimetre grid") +
        "<figcaption>Each square has sides of 1 cm. Going around: perimeter = 18 cm. "
        "There are 14 squares inside: area = 14 cm².</figcaption></figure>"
        "<h2>Find a missing side</h2>"
        "<p>In a shape with right angles, like an L, the short sides on one side add up to the long side opposite.</p>"
        "<figure class='sn-fig'>" + l_svg(9, 7, 5, 3, "tr", lab) +
        "<figcaption>Missing side: 7 − 3 = 4 m. Perimeter: 4 + 3 + 5 + 4 + 9 + 7 = 32 m.</figcaption></figure>" +
        ex("Example", "A garden bed is 12 m long and 5 m wide. How much edging goes around it?",
           "12 + 5 + 12 + 5 = 34. Or 12 + 5 = 17, then double it: 17 + 17 = 34.", "34 m") +
        "<h2>Area: count squares and half squares</h2>"
        "<p>Count the squares inside, row by row. Two half squares make one whole square.</p>"
        "<figure class='sn-fig'>" + one_grid(HALF_SHAPES[1], "house shape with half squares on a squared grid") +
        "<figcaption>14 whole squares and 4 half squares. 4 halves make 2 squares. Area = 14 + 2 = 16 squares.</figcaption></figure>"
        "<p>Counting in rows is quicker: 3 rows of 5 squares is 3 × 5 = 15 squares.</p>"
        "<h2>Estimate the area of a curved shape</h2>"
        "<p>Curved shapes do not fit the squares exactly, so we estimate. Count each whole square. "
        "Count a square as 1 if <b>half or more</b> is covered. Leave out squares that are less than half covered.</p>"
        "<figure class='sn-fig'>" + bsvg +
        "<figcaption>Each square is 1 cm². Whole squares: %d. Half or more covered: %d. "
        "Estimate: %d + %d = %d cm².</figcaption></figure>" % (whole, more, whole, more, whole + more) +
        "<h2>Choose the unit</h2>" +
        table(["Measuring", "Small things", "Big things"], [
            ["Perimeter (a length)", "cm: a photo, a book", "m: a garden bed, a court"],
            ["Area (squares inside)", "cm²: a stamp, a page", "m²: a classroom floor, a backyard"],
        ]) +
        "<p>Informal units work too, such as sticky notes or tiles, but everyone must use the same size square.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding only two sides (9 + 4 = 13 cm)", "Add all 4 sides: 9 + 4 + 9 + 4 = 26 cm"],
            ["Counting squares to find the perimeter", "Count the sides of the squares around the edge"],
            ["Counting a corner square only once", "A corner square has 2 sides on the edge"],
            ["Mixing up area and perimeter", "Area = squares inside. Perimeter = distance around"],
            ["Counting every part square as a whole one", "Count only squares that are half or more covered"],
            ["Writing cm for an area", "Area is in squares, cm² or m². Perimeter is in cm or m"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about perimeter and area in the Australian Curriculum?",
     "a": "They recognise ways of measuring perimeter and area (AC9M4M02): adding the side lengths for perimeter, and counting square units, including half squares, for area. They meet cm² and m² and estimate the area of irregular shapes on a grid."},
    {"q": "What is the difference between perimeter and area?",
     "a": "Perimeter is the distance around the outside of a shape, measured in cm or m. Area is the space inside, measured in square units such as cm² or m²."},
    {"q": "How do you estimate the area of an irregular shape on a grid?",
     "a": "Count the whole squares, then count each square that is half or more covered as 1. Leave out the squares that are less than half covered."},
    {"q": "Do Year 4 students use length × width for area?",
     "a": "Not as a formula yet. They count squares, and seeing that 3 rows of 5 squares is 3 × 5 = 15 is a good shortcut that leads to the formula in later years."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position) in every set.
    Items marked 'fixed' (A–D picture labels) keep their order and their answer."""
    for s in sets:
        fixed = [it for it in s["items"] if it.get("fixed")]
        free = [it for it in s["items"] if not it.get("fixed")]
        targets = [0, 1, 2, 3] * 5
        for it in fixed:
            targets.remove(it["a"])
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        for it in fixed:
            del it["fixed"]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4813)
    P = People(rnd)
    fixed_pos = [0, 1, 2, 3]
    rnd.shuffle(fixed_pos)
    sets = [set_add_sides(rnd), set_rectilinear(rnd), set_area(rnd), set_estimate(rnd, fixed_pos[:3]), set_story(rnd, P)]
    rnd.shuffle(sets[3]["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(k) == 5 for k in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "perimeter-and-area", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 4 Perimeter and Area",
        "seo_title": "Year 4 Perimeter and Area Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Perimeter and area",
        "domain": "Measurement",
        "standard_code": "AC9M4M02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise ways of measuring and approximating the perimeter and area of shapes and enclosed spaces, using appropriate formal and informal units",
        "meta_desc": "Free Year 4 perimeter and area worksheets for the Australian Curriculum (AC9M4M02): add the sides of rectangles and rectilinear shapes, find missing sides, count squares and half squares, estimate irregular areas on a grid and choose cm² or m². 100 questions with an answer key.",
        "key_big": "Perimeter is the distance around the edge. Area is the number of squares inside.",
        "key_sub": "Add every side to find the perimeter, in cm or m. Count whole and half squares to find the area, in cm² or m². For curved shapes, count squares that are half or more covered.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(grid|rectilinear)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
