# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Area and Perimeter (National Curriculum in England, Year 4 Measurement)
  python3 tools/gen_uk_maths_y4_area_perimeter.py
Perimeter of rectilinear figures in cm and m; area by counting squares.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
SQ = {"cm": "cm²", "m": "m²"}


# ------------------------------------------------------------ helpers
def f(n):
    """Year 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


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
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


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
def set_rect_perimeter(rnd):
    its = []
    rects = [(w, h) for w in range(2, 8) for h in range(2, 5) if w > h and w * h != 2 * (w + h)]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:8]):
        if i % 3 == 2:
            w, h = h, w                                   # some stand up tall
        cells = rect_cells(w, h)
        p, a, b = 2 * (w + h), w * h, border(cells)
        q = (fig(one_grid(cells, "rectangle %d by %d on a centimetre grid" % (w, h))) +
             "Each square has sides of 1 cm. What is the perimeter of the rectangle?")
        pool = ["%d cm" % b, "%d cm" % a, "%d cm" % (w + h), "%d cm²" % p, "%d cm" % (p - 2)]
        r = i % 3
        pool = pool[r:3] + pool[:r] + pool[3:]
        e = ("Count the sides of the squares all the way round: %d + %d + %d + %d = %d cm. "
             "Do not count the squares: a corner square has 2 sides on the edge." % (w, h, w, h, p))
        its.append(mcq(q, "%d cm" % p, pool, e, rnd))
    sizes = [(9, 4, "cm"), (12, 5, "cm"), (8, 6, "cm"), (15, 7, "cm"), (14, 9, "m"), (20, 6, "m"), (25, 10, "m"), (18, 12, "m")]
    rnd.shuffle(sizes)
    for i, (L, W, u) in enumerate(sizes):
        P = 2 * (L + W)
        if i < 5:
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
    for k, (s, u) in enumerate([(6, "cm"), (9, "m"), (8, "cm"), (11, "m")]):
        P = 4 * s
        if k < 2:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u), max_h=95)) +
                 "This is a square. What is its perimeter?")
        else:
            q = "A square has sides of %d %s. What is its perimeter?" % (s, u)
        pool = ["%d %s" % (s * s, u), "%d %s" % (2 * s, u), "%d %s" % (3 * s, u), "%d %s" % (P, SQ[u])]
        if k % 2:
            pool = [pool[1], pool[2], pool[0]]
        e = ("All 4 sides of a square are the same length: %d + %d + %d + %d = 4 × %d = %d %s."
             % (s, s, s, s, s, P, u))
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    rnd.shuffle(its)
    return {"title": "Perimeter of rectangles and squares", "items": its}


# ------------------------------------------------------------ set 2: rectilinear shapes and missing sides
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


def set_rectilinear(rnd):
    its = []
    used = set()
    # count the sides on a grid
    seen = set()
    kinds = ["L", "T", "U", "step"]
    for i in range(4):
        while True:
            cells = rand_shape(rnd, kinds[i])
            p, a, b = perim(cells), len(cells), border(cells)
            if cells in seen or p == a or len(cells) < 5:
                continue
            seen.add(cells)
            break
        q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
             "Each square has sides of 1 cm. What is the perimeter of the shape?")
        e = ("Go round the outside and count every 1 cm side, including the short steps: %d cm. "
             "There are %d squares, but counting squares gives the area, not the perimeter." % (p, a))
        its.append(mcq(q, "%d cm" % p, ["%d cm" % b, "%d cm" % a, "%d cm" % (p - 2), "%d cm" % (p + 2)], e, rnd))
    # L-shapes, all sides labelled
    for i in range(4):
        u = ["cm", "m"][i % 2]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lambda s: ["%d %s" % (v, u) for v in s])
        P = sum(sides)
        e = ("Add all 6 sides: %s = %d %s. Do not skip the two short sides at the inside corner." % (plus(sides), P, u))
        cands = ["%d %s" % (P - cw - ch, u), "%d %s" % (Wt + Ht, u), "%d %s" % (P - sides[1], u), "%d %s" % (P, SQ[u])]
        its.append(mcq(fig(svg) + "What is the perimeter of this shape?", "%d %s" % (P, u),
                       cands, e, rnd))
    # step shapes, all labelled
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
        e = ("Add all 8 sides: %s = %d %s." % (plus(sides), P, u))
        cands = ["%d %s" % (W + H, u), "%d %s" % (P - sides[2] - sides[3], u), "%d %s" % (P - sides[4], u),
                 "%d %s" % (P, SQ[u])]
        its.append(mcq(fig(svg) + "What is the perimeter of this shape?", "%d %s" % (P, u), cands, e, rnd))
    # find a missing side (L)
    for i in range(3):
        u = ["cm", "m", "cm"][i]
        mi = [0, 3, 3][i]

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
    # find a missing side (step): the long side
    for i in range(2):
        u = ["m", "cm"][i]
        for _ in range(5000):
            W, H, x1, x2, y1, y2 = pick_step(rnd, used)
            sides = step_sides(W, H, x1, x2, y1, y2)
            labs = ["%d %s" % (v, u) for v in sides]
            mi = 6 if i == 0 else 7
            labs[mi] = "? %s" % u
            svg = step_svg(W, H, x1, x2, y1, y2, labs, i == 0)
            if svg:
                used.add((W, H, x1, x2, y1, y2))
                break
        else:
            raise RuntimeError("no step fits")
        if mi == 6:
            parts, ans = [sides[0], sides[2], sides[4]], W
            e = ("The long bottom side is as long as the three top steps put together: %s = %d %s." % (plus(parts), ans, u))
        else:
            parts, ans = [sides[1], sides[3], sides[5]], H
            e = ("The long side is as long as the three short up-and-down sides put together: %s = %d %s."
                 % (plus(parts), ans, u))
        cands = ["%d %s" % (parts[0] + parts[1], u), "%d %s" % (max(parts), u), "%d %s" % (ans + parts[0], u),
                 "%d %s" % (ans - 1, u)]
        its.append(mcq(fig(svg) + "What is the length of the side marked ?", "%d %s" % (ans, u), cands, e, rnd))
    # perimeter with two sides not labelled
    for i in range(5):
        u = ["m", "cm"][i % 2]
        hide = [(0, 3), (1, 2)][i % 2]

        def lab(s, hide=hide, u=u):
            return ["" if j in hide else "%d %s" % (v, u) for j, v in enumerate(s)]
        Wt, Ht, cw, ch, sides, svg = l_figure(rnd, used, lab)
        P = sum(sides)
        shown = sum(v for j, v in enumerate(sides) if j not in hide)
        if hide == (0, 3):
            miss = "%d − %d = %d %s and %d − %d = %d %s" % (Wt, cw, Wt - cw, u, Ht, ch, Ht - ch, u)
        else:
            miss = "%d − %d = %d %s and %d − %d = %d %s" % (Ht, Ht - ch, ch, u, Wt, Wt - cw, cw, u)
        e = ("First find the two missing sides: %s. Then add all 6 sides: %s = %d %s."
             % (miss, plus(sides), P, u))
        cands = ["%d %s" % (shown, u), "%d %s" % (shown + sides[hide[0]], u), "%d %s" % (shown + sides[hide[1]], u),
                 "%d %s" % (Wt + Ht, u)]
        if i % 2:
            cands = [cands[0], cands[2], cands[1], cands[3]]
        q = fig(svg) + "Two sides are not labelled. What is the perimeter of the shape?"
        its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Rectilinear shapes and missing sides", "items": its}


# ------------------------------------------------------------ set 3: area by counting squares
HALF_SHAPES = [
    [(0, 0), (0, 4), (4, 4)],                                   # right-angled triangle
    [(0, 2), (2, 0), (4, 2), (4, 5), (0, 5)],                   # house
    [(0, 3), (3, 0), (6, 0), (6, 3)],                           # trapezium
    [(0, 0), (4, 0), (5, 1), (5, 4), (0, 4)],                   # rectangle with one corner cut
    [(2, 0), (4, 2), (2, 4), (0, 2)],                           # diamond
]
HALF_NAMES = ["triangle", "house shape", "trapezium", "shape", "diamond shape"]


def set_area(rnd):
    its = []
    seen = set()
    rects = [(w, h) for w in range(3, 8) for h in range(2, 5) if w > h]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:5]):
        if i % 2:
            w, h = h, w
        cells = frozenset(rect_cells(w, h))
        seen.add(cells)
        a, p = w * h, 2 * (w + h)
        q = fig(one_grid(cells, "rectangle %d by %d on a squared grid" % (w, h))) + "What is the area of the shaded rectangle?"
        e = ("Count the squares inside: %d rows of %d squares. %d × %d = %d squares. "
             "(%d is the number of sides round the edge: that is the perimeter.)" % (h, w, h, w, a, p))
        pool = ["%d squares" % p, "%d squares" % (a - w), "%d squares" % (w + h), "%d squares" % (a + h)]
        r = i % 4
        pool = pool[r:] + pool[:r]
        its.append(mcq(q, "%d squares" % a, pool, e, rnd))
    kinds = ["L", "T", "U", "step", "L", "U", "step"]
    for i, kd in enumerate(kinds):
        while True:
            cells = rand_shape(rnd, kd)
            a, p = len(cells), perim(cells)
            if cells in seen or a == p or a < 6:
                continue
            seen.add(cells)
            break
        w, h = size(cells)
        un = "squares" if i < 4 else "cm²"
        if un == "squares":
            q = fig(one_grid(cells, "rectilinear shape on a squared grid")) + "What is the area of the shaded shape?"
        else:
            q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
                 "Each square is 1 cm². What is the area of the shaded shape?")
        e = ("Count the shaded squares: there are %d, so the area is %d %s. "
             "Count each square once, row by row." % (a, a, un))
        if un == "cm²":
            e += " (%d cm is the perimeter.)" % p
        pool = ["%d %s" % (p, un), "%d %s" % (w * h, un), "%d %s" % (a + 1, un), "%d %s" % (a - 1, un)]
        if i % 2:
            pool = [pool[1], pool[0]] + pool[2:]
        its.append(mcq(q, "%d %s" % (a, un), pool, e, rnd))
    order = list(range(5))
    rnd.shuffle(order)
    for k in order:
        poly = HALF_SHAPES[k]
        full, halves = poly_counts(poly)
        A = poly_area(poly)
        bw, bh = max(x for x, y in poly), max(y for x, y in poly)
        q = (fig(one_grid(poly, "%s with half squares on a squared grid" % HALF_NAMES[k])) +
             "What is the area of the shaded %s? Two half squares make one whole square." % HALF_NAMES[k])
        hs = "%d half squares" % halves if halves > 1 else "1 half square"
        if halves == 1:
            mk = "1 half square is ½ of a square."
        else:
            hv = Fraction(halves, 2)
            mk = "%d halves make %s %s." % (halves, half(hv), "square" if hv == 1 else "squares")
        e = ("There are %d whole squares and %s. %s %d + %s = %s squares."
             % (full, hs, mk, full, half(Fraction(halves, 2)), half(A)))
        pool = ["%s squares" % half(full), "%s squares" % half(full + halves), "%s squares" % half(bw * bh),
                "%s squares" % half(A + 1)]
        its.append(mcq(q, "%s squares" % half(A), pool, e, rnd))
    P = People(random.Random(7))
    for (n, he, his), (rows, cols, thing) in zip([P.next() for _ in range(3)],
                                                [(4, 6, "square tiles"), (3, 8, "square sticky notes"),
                                                 (5, 7, "square cards")]):
        a = rows * cols
        q = ("%s makes a rectangle from %s. It has %d rows with %d %s in each row. What is its area in squares?"
             % (n, thing, rows, cols, thing.split()[-1]))
        e = ("Count the squares, or use the shortcut for a rectangle: %d rows of %d is %d × %d = %d squares."
             % (rows, cols, rows, cols, a))
        its.append(mcq(q, "%d squares" % a, ["%d squares" % (rows + cols), "%d squares" % (2 * (rows + cols)),
                                             "%d squares" % (a - cols)], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area by counting squares", "items": its}


# ------------------------------------------------------------ set 4: compare area and perimeter
def strip(shapes):
    """Place shapes side by side, 1 square apart, with a 1-square margin."""
    out, c = [], 1
    maxh = max(size(s)[1] for s in shapes)
    for s in shapes:
        w, h = size(s)
        out.append((s, c, 1 + maxh - h))
        c += w + 1
    return out, c, maxh + 2


def set_compare(rnd, fixed_pos):
    its = []
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
    tasks = [("area", "largest"), ("perim", "longest"), ("area", "smallest"), ("perim", "longest"), ("perim", "shortest")]
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
                continue                              # the biggest area should not also have the longest perimeter
            if what == "area" and max(A) - min(A) > 4:
                continue                              # keep it a real counting job
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
            q = (fig(svg) + "Each shape has an area of %d cm². Which shape has the %s perimeter?" % (A[0], word))
            e = ("Count the 1 cm sides round each shape: A %d cm, B %d cm, C %d cm, D %d cm. "
                 "The same area can have different perimeters. Shape %s has the %s (%d cm)."
                 % (Pm[0], Pm[1], Pm[2], Pm[3], "ABCD"[target], word, Pm[target]))
        it = {"q": q, "c": ["A", "B", "C", "D"], "a": target, "e": e, "fixed": True}
        its.append(it)
    # two rectangles: same area or same perimeter
    ch = ["Same area; A has the longer perimeter", "Same area; B has the longer perimeter",
          "Same perimeter; A has the larger area", "Same perimeter; B has the larger area"]
    for (a, b, c, d, u) in [(6, 2, 4, 3, "cm"), (4, 4, 8, 2, "m"), (5, 3, 4, 4, "cm"), (6, 6, 9, 4, "m"), (7, 2, 6, 3, "cm")]:
        A1, A2, P1, P2 = a * b, c * d, 2 * (a + b), 2 * (c + d)
        if A1 == A2:
            assert P1 != P2
            right = ch[0] if P1 > P2 else ch[1]
        else:
            assert P1 == P2
            right = ch[2] if A1 > A2 else ch[3]
        sa = "Square A has sides of %d %s." % (a, u) if a == b else "Rectangle A is %d %s by %d %s." % (a, u, b, u)
        sb = "Square B has sides of %d %s." % (c, u) if c == d else "Rectangle B is %d %s by %d %s." % (c, u, d, u)
        q = "%s %s Which is true?" % (sa, sb)
        e = ("A: area %d × %d = %d %s, perimeter %d + %d + %d + %d = %d %s. B: area %d × %d = %d %s, "
             "perimeter %d + %d + %d + %d = %d %s." % (a, b, A1, SQ[u], a, b, a, b, P1, u,
                                                       c, d, A2, SQ[u], c, d, c, d, P2, u))
        its.append(mcq(q, right, [x for x in ch if x != right], e, rnd))
    # area and perimeter of one shape
    seen = set()
    for i in range(5):
        while True:
            if i < 2:
                w, h = rnd.randint(2, 6), rnd.randint(2, 4)
                cells = frozenset(rect_cells(w, h))
            else:
                cells = rand_shape(rnd, ["L", "U", "step"][i - 2], maxw=5, maxh=4)
            a, p = len(cells), perim(cells)
            w, h = size(cells)
            if cells in seen or a == p or p // 2 == a or w * h == a and i >= 2:
                continue
            seen.add(cells)
            break
        fmt = "area %d cm², perimeter %d cm"
        right = fmt % (a, p)
        third = (a, p // 2) if i < 2 else (w * h, p)
        cands = [fmt % (p, a), fmt % third, fmt % (a, border(cells)), fmt % (a + 1, p)]
        q = (fig(one_grid(cells, "shape on a centimetre grid")) +
             "Each square has sides of 1 cm. What are the area and the perimeter of the shape?")
        e = ("Area: count the squares inside = %d cm². Perimeter: count the 1 cm sides round the edge = %d cm."
             % (a, p))
        its.append(mcq(q, right, cands, e, rnd))
    # which rectangle has this area and perimeter?
    for (a, b), others, u in [((3, 4), [(2, 6), (2, 5), (1, 6)], "cm"), ((2, 8), [(4, 4), (3, 7), (1, 9)], "m"),
                              ((3, 6), [(2, 9), (4, 5), (2, 7)], "cm"), ((4, 6), [(3, 8), (5, 5), (2, 8)], "m"),
                              ((2, 9), [(3, 6), (3, 8), (4, 7)], "cm")]:
        A, Pm = a * b, 2 * (a + b)
        for (x, y) in others:
            assert not (x * y == A and 2 * (x + y) == Pm)
        assert any(x * y == A for x, y in others) and any(2 * (x + y) == Pm for x, y in others)
        q = "Which rectangle has an area of %d %s and a perimeter of %d %s?" % (A, SQ[u], Pm, u)
        e = ("%d × %d = %d %s and %d + %d + %d + %d = %d %s. Check both: some rectangles have the right area "
             "but the wrong perimeter." % (a, b, A, SQ[u], a, b, a, b, Pm, u))
        its.append(mcq(q, "%d %s by %d %s" % (a, u, b, u), ["%d %s by %d %s" % (x, u, y, u) for x, y in others], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Compare area and perimeter", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    n, he, his = P.next()
    L, W = 14, 9
    add("%s’s family puts a fence round their rectangular garden. The garden is %d m long and %d m wide. "
        "How much fence do they need?" % (n, L, W), "%d m" % (2 * (L + W)),
        ["%d m" % (L * W), "%d m" % (L + W), "%d m" % (2 * L + W)],
        "The fence goes along all 4 sides: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    n, he, his = P.next()
    L, W = 20, 15
    add("%s glues ribbon round the edge of a photo frame. The frame is %d cm long and %d cm wide. "
        "How much ribbon does %s need?" % (n, L, W, he), "%d cm" % (2 * (L + W)),
        ["%d cm" % (L + W), "%d cm" % (L * W), "%d cm" % (2 * L + W)],
        "Ribbon goes round the edge, so find the perimeter: %d + %d + %d + %d = %d cm." % (L, W, L, W, 2 * (L + W)))
    n, he, his = P.next()
    s = 18
    add("%s puts ribbon round a square photo frame. Each side is %d cm. How much ribbon does %s need?" % (n, s, he),
        "%d cm" % (4 * s), ["%d cm" % (2 * s), "%d cm" % (3 * s), "%d cm" % (s * s)],
        "A square has 4 equal sides: 4 × %d = %d cm." % (s, 4 * s))
    r, c = 7, 9
    add("A classroom floor is covered with square carpet tiles. Each tile is 1 m long and 1 m wide. "
        "There are %d rows of %d tiles. What is the area of the floor?" % (r, c), "%d m²" % (r * c),
        ["%d m²" % (r + c), "%d m²" % (2 * (r + c)), "%d m" % (r * c)],
        "Each tile is 1 m², so count the tiles: %d rows of %d is %d × %d = %d m²." % (r, c, r, c, r * c))
    L, W = 30, 20
    add("The school playground is a rectangle %d m long and %d m wide. How far is it once round the edge?" % (L, W),
        "%d m" % (2 * (L + W)), ["%d m" % (L + W), "%d m" % (L * W), "%d m" % (2 * L + W)],
        "Once round is the perimeter: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    n, he, his = P.next()
    L, W = 25, 15
    add("In PE, %s runs round a rectangular field 2 times. The field is %d m long and %d m wide. "
        "How far does %s run?" % (n, L, W, he), "%d m" % (4 * (L + W)),
        ["%d m" % (2 * (L + W)), "%d m" % (2 * (L + W) + 2), "%d m" % (L * W)],
        "Once round: %d + %d + %d + %d = %d m. Two times round: 2 × %d = %d m."
        % (L, W, L, W, 2 * (L + W), 2 * (L + W), 4 * (L + W)))
    L, W, g = 12, 8, 2
    Pm = 2 * (L + W)
    add("A rectangular vegetable patch is %d m long and %d m wide. A fence goes all the way round, except for a gate "
        "that is %d m wide. How much fence is needed?" % (L, W, g), "%d m" % (Pm - g),
        ["%d m" % Pm, "%d m" % (L + W - g), "%d m" % (Pm + g)],
        "Perimeter: %d + %d + %d + %d = %d m. There is no fence across the gate: %d − %d = %d m."
        % (L, W, L, W, Pm, Pm, g, Pm - g))
    s, pl = 6, 2
    add("A square garden has sides of %d m. Fence panels are %d m long. How many panels go all the way round?" % (s, pl),
        "%d panels" % (4 * s // pl), ["%d panels" % (4 * s), "%d panels" % (s * s // pl), "%d panels" % (s // pl * 2)],
        "Perimeter: 4 × %d = %d m. Each panel is %d m: %d ÷ %d = %d panels." % (s, 4 * s, pl, 4 * s, pl, 4 * s // pl))
    # L-shaped garden plan
    used = set()
    for _ in range(300):
        Wt, Ht, cw, ch = pick_l(rnd, used, (9, 6), (14, 9))
        sides = l_sides(Wt, Ht, cw, ch)
        labs = ["%d m" % v for v in sides]
        labs[0] = labs[3] = ""
        svg = l_svg(Wt, Ht, cw, ch, "tl", labs, "plan of a rectilinear L-shaped garden")
        if svg:
            break
    Pm = sum(sides)
    shown = Pm - sides[0] - sides[3]
    add(fig(svg) + "This is the plan of an L-shaped garden. Two sides are not labelled. "
        "How much fence goes all the way round?", "%d m" % Pm,
        ["%d m" % shown, "%d m" % (Wt + Ht), "%d m" % (shown + sides[0])],
        "Missing sides: %d − %d = %d m and %d − %d = %d m. Add all 6 sides: %s = %d m."
        % (Wt, cw, Wt - cw, Ht, ch, Ht - ch, plus(sides), Pm))
    L, W = 120, 90
    add("A display board in the classroom is %d cm long and %d cm wide. The teacher puts a paper border round "
        "the edge. How long is the border?" % (L, W), "%d cm" % (2 * (L + W)),
        ["%d cm" % (L + W), "%d cm" % (2 * L + W), "%d cm" % (L + 2 * W)],
        "Border round the edge = perimeter: %d + %d + %d + %d = %d cm." % (L, W, L, W, 2 * (L + W)))
    r, c = 5, 4
    add("A patio is made of square paving slabs. Each slab is 1 m by 1 m. There are %d rows of %d slabs. "
        "What is the area of the patio?" % (r, c), "%d m²" % (r * c),
        ["%d m²" % (r + c), "%d m²" % (2 * (r + c)), "%d m" % (r * c)],
        "Count the slabs: %d rows of %d is %d × %d = %d slabs, so the area is %d m²." % (r, c, r, c, r * c, r * c))
    ch4 = ["Perimeter, in cm", "Area, in cm²", "Perimeter, in cm²", "Area, in cm"]
    n, he, his = P.next()
    add("%s wants to put coloured tape round the edge of a picture. What should %s work out?" % (n, he),
        ch4[0], ch4[1:], "Tape goes round the edge, so find the perimeter. Perimeter is a length, so it is in cm.")
    n, he, his = P.next()
    add("%s wants to cover the front of a book with paper. What should %s work out?" % (n, he),
        ch4[1], [ch4[0], ch4[2], ch4[3]],
        "Covering the inside of a shape is area. Area is counted in squares, so it is in cm².")
    add("A chessboard has 8 rows of 8 squares. How many squares are there on the board?", "64 squares",
        ["16 squares", "32 squares", "56 squares"],
        "8 rows of 8 squares: 8 × 8 = 64 squares. (32 is the number of square sides round the edge.)")
    L, W = 100, 60
    add("A football pitch is %d m long and %d m wide. The team jogs once round the edge. How far is that?" % (L, W),
        "%d m" % (2 * (L + W)), ["%d m" % (L + W), "%d m" % (2 * L + W), "%s m" % f(L * W)],
        "Perimeter: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)))
    Pm = 20
    add("A square sandpit has a perimeter of %d m. How long is each side?" % Pm, "%d m" % (Pm // 4),
        ["%d m" % (Pm // 2), "%d m" % (Pm - 4), "%d m" % (Pm * 4)],
        "A square has 4 equal sides: %d ÷ 4 = %d m. Check: %d + %d + %d + %d = %d m."
        % (Pm, Pm // 4, Pm // 4, Pm // 4, Pm // 4, Pm // 4, Pm))
    Pm, L = 30, 9
    W = Pm // 2 - L
    add("A rectangular flower bed has a perimeter of %d m. One side is %d m long. How long is the side next to it?"
        % (Pm, L), "%d m" % W, ["%d m" % (Pm - L), "%d m" % (Pm - 2 * L), "%d m" % (Pm // 2)],
        "The two %d m sides make %d m. %d − %d = %d m for the other two sides, so each is %d ÷ 2 = %d m. "
        "Check: %d + %d + %d + %d = %d m." % (L, 2 * L, Pm, 2 * L, Pm - 2 * L, Pm - 2 * L, W, L, W, L, W, Pm))
    n, he, his = P.next()
    add("%s has 16 m of fence to make a rectangular pen for %s rabbits. Which pen gives the rabbits the most space?"
        % (n, his), "4 m by 4 m", ["7 m by 1 m", "6 m by 2 m", "5 m by 3 m"],
        "All four pens use 16 m of fence. Areas: 7 × 1 = 7 m², 6 × 2 = 12 m², 5 × 3 = 15 m², 4 × 4 = 16 m². "
        "The square has the most space.")
    r, c, k = 6, 4, 5
    add("A vegetable patch is split into 1 m squares: %d rows of %d squares. Carrots grow in %d squares and "
        "potatoes in the rest. What area is potatoes?" % (r, c, k), "%d m²" % (r * c - k),
        ["%d m²" % (r * c), "%d m²" % (r * c + k), "%d m²" % (2 * (r + c) - k)],
        "Whole patch: %d × %d = %d m². Take away the carrots: %d − %d = %d m²." % (r, c, r * c, r * c, k, r * c - k))
    n, he, his = P.next()
    L, W = 20, 12
    Pm = 2 * (L + W)
    add("%s has 1 m of ribbon. %s puts ribbon round the edge of a card that is %d cm by %d cm. "
        "How much ribbon is left?" % (n, cap(he), L, W), "%d cm" % (100 - Pm),
        ["%d cm" % (100 - L - W), "%d cm" % (100 - 2 * L - W), "%d cm" % Pm],
        "1 m = 100 cm. Perimeter of the card: %d + %d + %d + %d = %d cm. Left: 100 − %d = %d cm."
        % (L, W, L, W, Pm, Pm, 100 - Pm))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area and perimeter word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_L = frozenset(rect_cells(2, 2) | rect_cells(5, 2, 0, 2))


def body_html():
    assert perim(LESSON_L) == 18 and len(LESSON_L) == 14
    assert poly_counts(HALF_SHAPES[1]) == (14, 4)
    lab = ["4 m", "3 m", "5 m", "", "9 m", "7 m"]
    assert l_sides(9, 7, 5, 3) == [4, 3, 5, 4, 9, 7]
    return (
        "<h2>Perimeter and area</h2>"
        "<p><b>Perimeter</b> is the distance <b>all the way round</b> a shape. It is a length, so it is in cm or m.</p>"
        "<p><b>Area</b> is the space <b>inside</b> a shape. In Year 4 we find it by <b>counting squares</b>. "
        "If each square is 1 cm², the area is in cm².</p>"
        "<h2>Perimeter of a rectangle</h2>"
        "<p>Add all 4 sides. A rectangle has 2 long sides and 2 short sides.</p>"
        "<figure class='sn-fig'>" + rect_svg(9, 4, "9 cm", "4 cm", "rectangle 9 cm by 4 cm") +
        "<figcaption>9 + 4 + 9 + 4 = 26 cm. Not 9 + 4 = 13: that is only two sides.</figcaption></figure>"
        "<h2>Perimeter on a grid</h2>"
        "<p>Count the sides of the squares round the edge, not the squares. A corner square has 2 sides on the edge.</p>"
        "<figure class='sn-fig'>" + one_grid(LESSON_L, "rectilinear shape on a centimetre grid") +
        "<figcaption>Each square has sides of 1 cm. Going round: perimeter = 18 cm. "
        "There are 14 squares inside: area = 14 cm².</figcaption></figure>"
        "<h2>Rectilinear shapes: find the missing sides</h2>"
        "<p>A rectilinear shape has only straight sides and right angles, like an L. "
        "Opposite parts add up: the short sides on one side match the long side opposite.</p>"
        "<figure class='sn-fig'>" + l_svg(9, 7, 5, 3, "tr", lab) +
        "<figcaption>Missing side: 7 − 3 = 4 m. Perimeter: 4 + 3 + 5 + 4 + 9 + 7 = 32 m.</figcaption></figure>" +
        ex("Example", "A rectangle is 12 m long and 5 m wide. What is its perimeter?",
           "12 + 5 + 12 + 5 = 34. Or 12 + 5 = 17, then double it: 17 + 17 = 34.", "34 m") +
        "<h2>Area by counting squares</h2>"
        "<p>Count the squares inside, row by row. Two half squares make one whole square.</p>"
        "<figure class='sn-fig'>" + one_grid(HALF_SHAPES[1], "house shape with half squares on a squared grid") +
        "<figcaption>14 whole squares and 4 half squares. 4 halves make 2 squares. Area = 14 + 2 = 16 squares.</figcaption></figure>"
        "<p>Shortcut for a rectangle: 3 rows of 5 squares is 3 × 5 = 15 squares. You will learn this as a formula in Year 5.</p>"
        "<h2>Same area, different perimeter</h2>"
        "<p>Rectangles 6 cm by 2 cm and 4 cm by 3 cm both have an area of 12 cm². "
        "Their perimeters are 16 cm and 14 cm. A long, thin shape has a longer perimeter.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding only two sides (9 + 4 = 13 cm)", "Add all 4 sides: 9 + 4 + 9 + 4 = 26 cm"],
            ["Counting squares to find the perimeter", "Count the sides of the squares round the edge"],
            ["Counting a corner square only once", "A corner square has 2 sides on the edge"],
            ["Missing a side in an L-shape", "Find the missing side first, then add all 6 sides"],
            ["Mixing up area and perimeter", "Area = squares inside. Perimeter = distance round"],
            ["Writing cm for an area", "Area is in squares or cm². Perimeter is in cm"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 children learn about area and perimeter?",
     "a": "They measure and calculate the perimeter of rectilinear shapes, including squares, in centimetres and metres, and find the area of rectilinear shapes by counting squares."},
    {"q": "What is a rectilinear shape?",
     "a": "A shape with only straight sides that meet at right angles, such as a rectangle or an L-shape. You can find its perimeter by adding all the sides."},
    {"q": "How do you find a missing side on an L-shape?",
     "a": "Use the side opposite it. The short sides on one side add up to the long side opposite, so subtract the side you know from the long side."},
    {"q": "Do Year 4 pupils use length × width for area?",
     "a": "In Year 4 they count squares. Spotting that 3 rows of 5 squares is 3 × 5 = 15 is a good shortcut; the area formula for rectangles is taught in Year 5."},
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
    rnd = random.Random(4412)
    P = People(rnd)
    fixed_pos = [0, 1, 2, 3, rnd.randint(0, 3)]
    rnd.shuffle(fixed_pos)
    sets = [set_rect_perimeter(rnd), set_rectilinear(rnd), set_area(rnd), set_compare(rnd, fixed_pos), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(k) == 5 for k in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "area-and-perimeter", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Area and Perimeter",
        "seo_title": "Year 4 Area and Perimeter Worksheets: Rectilinear Shapes and Counting Squares",
        "short_title": "Area and perimeter",
        "domain": "Measurement",
        "standard_code": "Year 4: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Measure and calculate the perimeter of a rectilinear figure (including squares) in centimetres and metres; find the area of rectilinear shapes by counting squares.",
        "meta_desc": "Free Year 4 area and perimeter worksheets for the National Curriculum: perimeter of rectangles, squares and rectilinear shapes in cm and m, missing sides, area by counting squares and word problems. 100 questions with an answer key.",
        "key_big": "Perimeter is the distance round the edge. Area is the number of squares inside.",
        "key_sub": "Add every side to find the perimeter, in cm or m. Count the squares to find the area, in squares or cm². For an L-shape, find the missing sides first.",
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
