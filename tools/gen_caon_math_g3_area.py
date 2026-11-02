# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Area (Ontario Curriculum 2020, Spatial Sense E2.7, E2.8, E2.9)
  python3 tools/gen_ca_math_g3_area.py
Compare areas by covering (pattern blocks, sticky notes, unit size), count square units and half squares,
gaps and overlaps, square centimetres and square metres, estimating the area of curved shapes on a grid,
word problems (carpet tiles, gardens). No area formula yet: rows of squares are counted or skip counted.
Wrong choices come from real mistakes (counting the perimeter, the edge squares, gaps, wrong units).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
SQ = {"cm": "cm²", "m": "m²"}
NBSP = "\u00a0"



# ------------------------------------------------------------ helpers
def fmt(n):
    """4536 -> 4536, 10800 -> 10 800 (no-break space, Ontario style)."""
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




def strip(shapes):
    """Place shapes side by side, 1 square apart, with a 1-square margin."""
    out, c = [], 1
    maxh = max(size(s)[1] for s in shapes)
    for s in shapes:
        w, h = size(s)
        out.append((s, c, 1 + maxh - h))
        c += w + 1
    return out, c, maxh + 2




def skip(r, c):
    """'3 rows of 5' -> '5, 10, 15' (skip counting by the row)."""
    return ", ".join(str(c * i) for i in range(1, r + 1))


def row_sum(cells):
    rows = {}
    for c, r in cells:
        rows[r] = rows.get(r, 0) + 1
    v = [rows[k] for k in sorted(rows)]
    assert sum(v) == len(cells)
    return plus(v)


def an(word):
    return ("an " if word[0] in "aeiou" else "a ") + word


# ------------------------------------------------------------ pattern blocks (triangle units)
H3 = math.sqrt(3) / 2


def tri_pts(t):
    a, b, d = t
    if d == "u":
        return [(a, b), (a + 1, b), (a, b + 1)]
    return [(a + 1, b), (a, b + 1), (a + 1, b + 1)]


def tri_row(k):
    return [(a, 0, "u") for a in range((k + 1) // 2)] + [(a, 0, "d") for a in range(k // 2)]


def tri_big(n):
    return ([(a, b, "u") for a in range(n) for b in range(n) if a + b <= n - 1] +
            [(a, b, "d") for a in range(n) for b in range(n) if a + b <= n - 2])


TRI_HEX = [(1, 1, "u"), (0, 1, "u"), (1, 0, "u"), (0, 1, "d"), (1, 0, "d"), (0, 0, "d")]
TRI_RHOMBUS = [(a, b, d) for a in range(2) for b in range(2) for d in "ud"]


def tri_edges(tris):
    """Number of triangle sides on the outside of the shape."""
    cnt = {}
    for t in tris:
        p = tri_pts(t)
        for i in range(3):
            e = frozenset([p[i], p[(i + 1) % 3]])
            cnt[e] = cnt.get(e, 0) + 1
    return sum(1 for v in cnt.values() if v == 1)


def tri_svg(tris, label, k=40):
    polys = []
    for t in tris:
        polys.append([((a + b / 2) * k, -b * H3 * k) for a, b in tri_pts(t)])
    xs = [x for p in polys for x, y in p]
    ys = [y for p in polys for x, y in p]
    m = 5
    ox, oy = min(xs) - m, min(ys) - m
    W, H = int(math.ceil(max(xs) - ox + m)), int(math.ceil(max(ys) - oy + m))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in p), FILL, GREEN) for p in polys]
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ tiles on a tray (gaps and overlaps)
TC = 20          # tile size in the panels


def tray_panel(kind, x0, y0, cols=4, rows=3):
    """Tray (cols x rows tiles) with tiles placed: ok / gap / overlap / edge."""
    Wt, Ht = cols * TC, rows * TC
    tiles, op = [], 1
    if kind == "ok":
        tiles = [(i * TC, j * TC) for i in range(cols) for j in range(rows)]
    elif kind == "gap":
        tiles = [(x, y) for x in (0, 30, 60) for y in (0, 40)]
    elif kind == "overlap":
        tiles = [(i * 15, j * TC) for i in range(5) for j in range(rows)]
        op = 0.55
    else:  # edge
        tiles = [(i * TC + TC // 2, j * TC + TC // 2) for i in range(cols) for j in range(rows)]
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (x0, y0, Wt, Ht)]
    for x, y in tiles:
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' fill-opacity='%s' stroke='%s' "
                 "stroke-width='1.5'/>" % (x0 + x, y0 + y, TC, TC, "#7fbf95" if op < 1 else FILL, op, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0, y0, Wt, Ht, INK))
    return "".join(s)


def trays_svg(kinds, letters="ABCD"):
    pw, pad = 4 * TC + 24, 12      # panel: tray + room for tiles over the edge
    s = []
    for i, k in enumerate(kinds):
        x0 = pad + i * (pw + 10)
        s.append(tray_panel(k, x0, pad))
        if letters:
            s.append(text(x0 + 2 * TC, pad + 3 * TC + TC // 2 + 24, letters[i], 17))
    W = pad + (len(kinds) - 1) * (pw + 10) + 4 * TC + TC // 2 + pad
    H = pad + 3 * TC + TC // 2 + 32
    return svg_wrap(W, H, "".join(s), "four trays A to D covered with square tiles")


def partial_svg(w, h, mode, missing=(), cell=24):
    """mode 'edge': only the first row and the first column of tiles are shown.
    mode 'gaps': every tile except the missing ones."""
    m = 6
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (m, m, w * cell, h * cell)]
    for i in range(w):
        for j in range(h):
            if mode == "edge" and not (i == 0 or j == 0):
                continue
            if mode == "gaps" and (i, j) in missing:
                continue
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (m + i * cell, m + j * cell, cell, cell, FILL, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (m, m, w * cell, h * cell, INK))
    return svg_wrap(w * cell + 2 * m, h * cell + 2 * m, "".join(s), "rectangle with square tiles")


# ------------------------------------------------------------ set 1: compare areas by covering
TRI_SHAPES = [(tri_big(2), "triangle"), (tri_row(5), "trapezoid"), (TRI_HEX, "hexagon"),
              (tri_row(7), "trapezoid"), (TRI_RHOMBUS, "parallelogram"), (tri_big(3), "triangle")]


def compare_strip(rnd, lib, word, target):
    for _ in range(20000):
        shapes = rnd.sample(lib, 4)
        A = [len(s) for s in shapes]
        Pm = [perim(s) for s in shapes]
        if len(set(A)) < 4 or max(A) - min(A) > 4:
            continue
        best = max(A) if word == "largest" else min(A)
        if A.index(best) != target:
            continue
        # the shape with the longest outline must not be the answer (perimeter mistake)
        if Pm.count(max(Pm)) == 1 and Pm.index(max(Pm)) == target:
            continue
        return shapes, A
    raise RuntimeError("no strip")


def set_cover(rnd, P, fixed_pos):
    its = []
    kinds = ["L", "T", "U", "step"]
    lib = set()
    for _ in range(3000):
        if rnd.random() < 0.25:
            lib.add(frozenset(rect_cells(rnd.randint(1, 4), rnd.randint(1, 3))))
        else:
            lib.add(rand_shape(rnd, rnd.choice(kinds), maxw=4, maxh=3))
    lib = sorted((x for x in lib if len(x) >= 4), key=lambda x: sorted(x))
    for word, target in zip(["largest", "smallest", "largest"], fixed_pos):
        shapes, A = compare_strip(rnd, lib, word, target)
        placed, cols, rows = strip(shapes)
        svg = grid_svg(cols, rows, placed, 18, "four shapes A to D on a squared grid", letters="ABCD")
        q = fig(svg) + "Each shape is covered by square units. Which shape has the %s area?" % word
        e = ("Count the squares that cover each shape: A %d, B %d, C %d, D %d. Shape %s covers the %s "
             "squares, so it has the %s area." % (A[0], A[1], A[2], A[3], "ABCD"[target],
                                                    "most" if word == "largest" else "fewest", word))
        its.append({"q": q, "c": ["A", "B", "C", "D"], "a": target, "e": e, "fixed": True})
    order = list(range(len(TRI_SHAPES)))
    rnd.shuffle(order)
    for k in order:
        tris, name = TRI_SHAPES[k]
        n = len(tris)
        up = sum(1 for t in tris if t[2] == "u")
        ed = tri_edges(tris)
        q = (fig(tri_svg(tris, "%s covered by triangle pattern blocks" % name)) +
             "This %s is covered by green triangle pattern blocks. What is its area in triangles?" % name)
        e = ("Count every triangle, the ones pointing up and the ones pointing down: %d up + %d down = %d triangles."
             % (up, n - up, n))
        cands = ["%d triangles" % up, "%d triangles" % ed, "%d triangles" % (n + 1), "%d triangles" % (n - 1)]
        its.append(mcq(q, "%d triangles" % n, cands, e, rnd))
    its.append(mcq("A yellow hexagon pattern block is covered exactly by 6 green triangles. How many green triangles "
                   "cover 2 hexagons?", "12 triangles", ["6 triangles", "8 triangles", "4 triangles"],
                   "Each hexagon is 6 triangles. 2 hexagons: 6 + 6 = 12 triangles. "
                   "(6 + 2 = 8 adds the number of hexagons instead.)", rnd))
    its.append(mcq("A blue rhombus pattern block is covered by 2 green triangles. A shape is covered by 4 blue "
                   "rhombuses. What is its area in triangles?", "8 triangles",
                   ["4 triangles", "6 triangles", "2 triangles"],
                   "Each rhombus is 2 triangles. 4 rhombuses: 2 + 2 + 2 + 2 = 8 triangles.", rnd))
    its.append(mcq("A red trapezoid pattern block covers the same space as 3 green triangles. "
                   "Which covers more space: 2 trapezoids or 5 triangles?", "2 trapezoids",
                   ["5 triangles", "They are the same", "You cannot tell"],
                   "Change the trapezoids into triangles: 2 trapezoids = 3 + 3 = 6 triangles. 6 is more than 5. "
                   "Compare areas in the same unit.", rnd))
    # size of the unit (E2.8)
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(mcq("%s and %s cover the same table. %s uses 8 big cards. %s uses 24 small sticky notes. Why are the "
                   "numbers different?" % (n1, n2, n1, n2), "Sticky notes are smaller units",
                   ["Sticky notes are bigger units", "The table got bigger", "%s counted wrongly" % n1],
                   "It is the same table, so the area is the same. Smaller units are needed in bigger numbers.", rnd))
    its.append(mcq("Which unit would you need the most of to cover a desk?", "Sticky notes",
                   ["Sheets of paper", "Placemats", "Floor mats"],
                   "The smaller the unit, the more of them you need. Sticky notes are the smallest here.", rnd))
    its.append(mcq("Which unit would you need the fewest of to cover the gym floor?", "Big floor mats",
                   ["Sheets of paper", "Sticky notes", "Playing cards"],
                   "The bigger the unit, the fewer you need. Floor mats are the biggest units here.", rnd))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(mcq("%s covers shape A with 6 big tiles. %s covers shape B with 6 small tiles. Which is true?"
                   % (n1, n2), "Shape A is bigger",
                   ["They have the same area", "Shape B is bigger", "Each has an area of 6 cm²"],
                   "Both counts are 6, but the units are different sizes. 6 big tiles cover more space than "
                   "6 small tiles. To compare areas, use the same unit.", rnd))
    n1, he, his = P.next()
    its.append(mcq("%s covers a rug with large square tiles and needs 10. How many tiles will %s need if %s uses "
                   "smaller tiles?" % (n1, he, he), "More than 10",
                   ["Fewer than 10", "Exactly 10", "Exactly 5"],
                   "The rug does not change. Smaller tiles each cover less, so more of them are needed.", rnd))
    # covering in rows (non-standard units)
    for (r, c, unit, thing) in [(3, 5, "sticky notes", "a placemat"), (3, 6, "index cards", "a desk"),
                                (4, 5, "sheets of paper", "a bulletin board")]:
        n1, he, his = P.next()
        a = r * c
        q = ("%s covers %s with %s, with no gaps or overlaps. There are %d rows of %d. "
             "What is the area in %s?" % (n1, thing, unit, r, c, unit))
        e = ("Count by rows: %d rows of %d is %s. The area is %d %s. "
             "(%d + %d = %d only adds the rows and the columns.)" % (r, c, skip(r, c), a, unit, r, c, r + c))
        cands = ["%d %s" % (r + c, unit), "%d %s" % (2 * (r + c) - 4, unit), "%d %s" % (a - c, unit)]
        its.append(mcq(q, "%d %s" % (a, unit), cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare areas by covering", "items": its}


# ------------------------------------------------------------ set 2: count square units and half squares
HALF_SHAPES = [
    [(0, 0), (0, 4), (4, 4)],                                   # right triangle
    [(0, 2), (2, 0), (4, 2), (4, 5), (0, 5)],                   # house
    [(0, 3), (3, 0), (6, 0), (6, 3)],                           # trapezoid
    [(0, 0), (4, 0), (5, 1), (5, 4), (0, 4)],                   # rectangle with one corner cut
    [(2, 0), (4, 2), (2, 4), (0, 2)],                           # square turned on its corner
    [(0, 0), (3, 0), (3, 2), (5, 2), (5, 3), (4, 4), (0, 4)],   # L with a cut corner
]
HALF_NAMES = ["triangle", "house shape", "trapezoid", "shape", "diamond shape", "shape"]
HALF_CM = [
    ([(0, 1), (3, 1), (3, 0), (5, 2), (3, 4), (3, 3), (0, 3)], "arrow shape"),
    ([(0, 2), (2, 2), (2, 0), (4, 2), (6, 2), (5, 3), (1, 3)], "sailboat shape"),
    ([(2, 0), (4, 2), (3, 2), (3, 4), (1, 4), (1, 2), (0, 2)], "tree shape"),
]


def half_q(poly, name, un, rnd, gridword):
    full, halves = poly_counts(poly)
    A = poly_area(poly)
    bw, bh = max(x for x, y in poly), max(y for x, y in poly)
    if un == "square units":
        q = (fig(one_grid(poly, "%s with half squares on a %s" % (name, gridword))) +
             "What is the area of the shaded %s? Two half squares make one whole square." % name)
    else:
        q = (fig(one_grid(poly, "%s with half squares on a %s" % (name, gridword))) +
             "Each square is 1 cm². What is the area of the shaded %s?" % name)
    hv = Fraction(halves, 2)
    if halves == 1:
        hs, mk = "1 half square", "1 half square is ½ of a square."
    else:
        hs = "%d half squares" % halves
        mk = "%d halves make %s %s." % (halves, half(hv), "whole square" if hv == 1 else "whole squares")
    e = ("There are %d whole squares and %s. %s %d + %s = %s %s."
         % (full, hs, mk, full, half(hv), half(A), un))
    pool = ["%s %s" % (half(full + halves), un), "%s %s" % (half(full), un), "%s %s" % (half(bw * bh), un),
            "%s %s" % (half(A + 1), un)]
    if un == "cm²":
        pool = [pool[0], "%s cm" % half(A), pool[1], pool[2]]
    return mcq(q, "%s %s" % (half(A), un), pool, e, rnd)


def set_count(rnd, seen):
    its = []
    rects = [(w, h) for w in range(3, 7) for h in range(2, 5) if w > h]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:4]):
        if i % 2:
            w, h = h, w
        cells = frozenset(rect_cells(w, h))
        seen.add(cells)
        a, p = w * h, 2 * (w + h)
        un = "square units" if i < 2 else "cm²"
        if un == "square units":
            q = fig(one_grid(cells, "rectangle %d by %d on a squared grid" % (w, h))) + "What is the area of the shaded rectangle?"
        else:
            q = (fig(one_grid(cells, "rectangle %d by %d on a centimetre grid" % (w, h))) +
                 "Each square is 1 cm². What is the area of the shaded rectangle?")
        e = ("Count the squares inside, row by row: %d rows of %d is %s. The area is %d %s. "
             "(%d is the number of sides around the edge: that is the perimeter.)" % (h, w, skip(h, w), a, un, p))
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
            a, p, b = len(cells), perim(cells), border(cells)
            w, h = size(cells)
            if cells in seen or a == p or a < 6 or w * h in (a + 1, a - 1) or b == a:
                continue
            seen.add(cells)
            break
        un = "square units" if i < 4 else "cm²"
        if un == "square units":
            q = fig(one_grid(cells, "rectilinear shape on a squared grid")) + "What is the area of the shaded shape?"
        else:
            q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
                 "Each square is 1 cm². What is the area of the shaded shape?")
        e = ("Count the shaded squares, row by row: %s = %d. The area is %d %s. Count each square once, "
             "not the sides around the edge (that would be the perimeter, %d)." % (row_sum(cells), a, a, un, p))
        pool = ["%d %s" % (p, un), "%d %s" % (b, un), "%d %s" % (w * h, un), "%d %s" % (a + 1, un)]
        if un == "cm²":
            pool = [pool[0], "%d cm" % a, pool[1], pool[2]]
        if i % 2:
            pool = [pool[1], pool[0]] + pool[2:]
        its.append(mcq(q, "%d %s" % (a, un), pool, e, rnd))
    order = list(range(len(HALF_SHAPES)))
    rnd.shuffle(order)
    for n, k in enumerate(order):
        un = "square units" if n < 3 else "cm²"
        gw = "squared grid" if n < 3 else "centimetre grid"
        its.append(half_q(HALF_SHAPES[k], HALF_NAMES[k], un, rnd, gw))
    for (wh, hf) in [(8, 4), (11, 2), (6, 6)]:
        A = wh + hf // 2
        q = ("A shape on a grid covers %d whole squares and %d half squares. What is its area in square units?"
             % (wh, hf))
        e = ("Two half squares make one whole square, so %d half squares make %d. %d + %d = %d square units."
             % (hf, hf // 2, wh, hf // 2, A))
        its.append(mcq(q, "%d square units" % A, ["%d square units" % (wh + hf), "%d square units" % wh,
                                                   "%d square units" % (wh + 2 * hf)], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Count square units and half squares", "items": its}


# ------------------------------------------------------------ set 3: gaps and overlaps
TRAY_WORD = {"ok": "no gaps and no overlaps", "gap": "gaps between the tiles",
             "overlap": "tiles that overlap", "edge": "tiles hanging over the edge"}


def set_gaps(rnd, P):
    its = []
    base = ["ok", "gap", "overlap", "edge"]
    used_perm = set()
    for ask, qtext in [("ok", "Which picture shows the right way to measure the area of the tray?"),
                       ("gap", "Which picture has gaps between the tiles?"),
                       ("overlap", "Which picture has tiles that overlap?")]:
        while True:
            kinds = base[:]
            rnd.shuffle(kinds)
            if tuple(kinds) not in used_perm and kinds.index(ask) not in [p.index(ask) for p in map(list, used_perm)]:
                used_perm.add(tuple(kinds))
                break
        t = kinds.index(ask)
        desc = " ".join("%s has %s." % (L, TRAY_WORD[k]) for L, k in zip("ABCD", kinds))
        if ask == "ok":
            e = desc + " Tiles must fit inside the edge with no gaps and no overlaps, as in %s." % "ABCD"[t]
        else:
            e = desc + " So the answer is %s." % "ABCD"[t]
        its.append({"q": fig(trays_svg(kinds)) + "Each picture shows square tiles on a tray. " + qtext,
                    "c": ["A", "B", "C", "D"], "a": t, "e": e, "fixed": True})
    # first row and first column
    for (w, h) in [(5, 3), (4, 4), (6, 3), (5, 4), (4, 3), (6, 4)]:
        a = w * h
        shown = w + h - 1
        q = (fig(partial_svg(w, h, "edge")) +
             "Square tiles are placed along the top row and down one side. How many tiles will cover the "
             "whole rectangle?")
        e = ("The top row shows %d tiles fit across. The side shows there are %d rows. "
             "%d rows of %d: %s. The rectangle needs %d tiles." % (w, h, h, w, skip(h, w), a))
        cands = ["%d tiles" % shown, "%d tiles" % (2 * (w + h) - 4), "%d tiles" % (w + h), "%d tiles" % (a - w)]
        its.append(mcq(q, "%d tiles" % a, cands, e, rnd))
    # trays with missing tiles
    specs = [(5, 3, 3, "more"), (4, 4, 4, "more"), (6, 3, 5, "more"), (5, 4, 3, "area"), (6, 4, 3, "area")]
    for (w, h, k, ask) in specs:
        cells = [(i, j) for i in range(w) for j in range(h)]
        while True:
            miss = rnd.sample(cells, k)
            inner = [c for c in miss if 0 < c[0] < w - 1 and 0 < c[1] < h - 1]
            edge = [c for c in miss if c not in inner]
            adj = any(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a in miss for b in miss if a != b)
            if inner and edge and not adj:
                break
        t = w * h
        shown = t - k
        svg = partial_svg(w, h, "gaps", set(miss))
        n1, he, his = P.next()
        if ask == "more":
            q = (fig(svg) + "%s is covering a tray with square tiles. How many more tiles does %s need so there are "
                 "no gaps?" % (n1, he))
            e = ("Count the empty spaces, including the ones at the edge: %d. "
                 "(%d tiles are already down, and %d is the total.)" % (k, shown, t))
            cands = ["%d tiles" % shown, "%d tiles" % t, "%d tiles" % (k - 1), "%d tiles" % (k + 1)]
            its.append(mcq(q, "%d tiles" % k, cands, e, rnd))
        else:
            q = (fig(svg) + "Some tiles are missing from this tray. What is the area of the tray in square tiles?")
            e = ("The area is the whole tray, gaps too. %d rows of %d: %s, so %d tiles. "
                 "Counting only the tiles you see (%d) leaves out the gaps." % (h, w, skip(h, w), t, shown))
            cands = ["%d tiles" % shown, "%d tiles" % (2 * (w + h)), "%d tiles" % (w + h)]
            its.append(mcq(q, "%d tiles" % t, cands, e, rnd))
    n1, he, his = P.next()
    its.append(mcq("%s covers %s desk with sticky notes but leaves gaps between them. %s counts 20 sticky notes. "
                   "What is the real area of the desk?" % (n1, his, cap(he)), "More than 20 sticky notes",
                   ["Less than 20 sticky notes", "Exactly 20 sticky notes", "Exactly 10 sticky notes"],
                   "The gaps are part of the desk too, but no sticky notes were counted there. "
                   "So the real area is more than 20 sticky notes.", rnd))
    n1, he, his = P.next()
    its.append(mcq("%s covers a book with index cards, but the cards overlap. %s counts 14 cards. "
                   "What is the real area of the book?" % (n1, cap(he)), "Less than 14 cards",
                   ["More than 14 cards", "Exactly 14 cards", "Exactly 28 cards"],
                   "Where cards overlap, the same space is counted twice. So the real area is less than 14 cards.",
                   rnd))
    its.append(mcq("Why are square tiles better than round counters for measuring area?",
                   "Circles leave gaps", ["Circles are too small", "Squares are easier to lift", "Circles overlap less"],
                   "Round counters cannot fit together without gaps, so some space is not counted. "
                   "Squares fit together with no gaps and no overlaps.", rnd))
    n1, he, his = P.next()
    its.append(mcq("%s lets some tiles hang over the edge of a tray. What happens to %s count?" % (n1, his),
                   "It is too big", ["It is too small", "It is exactly right", "It is half the area"],
                   "Parts of the tiles are outside the tray, but they are counted anyway. "
                   "So the count is bigger than the real area.", rnd))
    its.append(mcq("Which rule helps you measure area correctly?", "No gaps and no overlaps",
                   ["Leave small gaps", "Overlap the edges a bit", "Mix big and small units"],
                   "Cover the whole shape with units of the same size, with no gaps and no overlaps.", rnd))
    n1, he, his = P.next()
    n2, _, _ = P.next()
    its.append(mcq("%s counts 18 square tiles on a mat. %s covers the same mat with the same tiles and counts 24, "
                   "with no gaps or overlaps. What did %s do wrong?" % (n1, n2, n1),
                   "%s left gaps" % cap(he), ["%s overlapped tiles" % cap(he), "%s used smaller tiles" % cap(he),
                                               "%s counted too many" % cap(he)],
                   "%s got fewer tiles than the correct count. Gaps make a count too small. "
                   "(Overlaps would make it too big.)" % n1, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Gaps and overlaps", "items": its}


# ------------------------------------------------------------ set 4: square centimetres and square metres
def set_units(rnd, seen):
    its = []
    U4 = ["cm", "m", "cm²", "m²"]
    for thing, right, why in [
        ("the area of a classroom floor", "m²", "A floor is big and we cover the space inside it, so use square metres."),
        ("the area of a postage stamp", "cm²", "A stamp is small and we cover the space inside it, so use square centimetres."),
        ("the area of an outdoor skating rink", "m²", "A rink is big and area is the space inside, so use square metres."),
        ("the area of the front of a cereal box", "cm²", "A cereal box is small and area is the space inside, so use square centimetres."),
        ("the distance around a photo", "cm", "The distance around is a length (the perimeter), not an area. A photo is small, so use centimetres."),
        ("the length of the school hallway", "m", "This is a length, not an area. A hallway is long, so use metres."),
    ]:
        q = "Which unit is best for measuring %s?" % thing
        its.append(mcq(q, right, [x for x in U4 if x != right],
                       why + " cm and m are for lengths; cm² and m² are for areas.", rnd))
    its.append(mcq("Which has an area of about 1 cm²?", "A fingernail",
                   ["A sticky note", "A notebook cover", "A classroom door"],
                   "1 cm² is a square 1 cm long and 1 cm wide, about the size of the nail on your little finger.", rnd))
    its.append(mcq("About how big is the floor of a classroom?", "About 60 m²",
                   ["About 6 m²", "About 600 m²", "About 60 cm²"],
                   "A classroom is about 8 m by 8 m: 8 rows of 8 one-metre squares is 64, so about 60 m². "
                   "6 m² is a small rug. A floor needs square metres, not square centimetres.", rnd))
    its.append(mcq("About how big is the cover of a notebook?", "About 600 cm²",
                   ["About 6 cm²", "About 60 m²", "About 600 cm"],
                   "A notebook is about 28 cm by 21 cm, so about 600 squares of 1 cm² cover it. "
                   "60 m² would be a whole classroom, and cm is for length, not area.", rnd))
    its.append(mcq("About how big is a square sticky note?", "About 60 cm²",
                   ["About 6 cm²", "About 60 m²", "About 600 cm²"],
                   "A sticky note is about 8 cm by 8 cm: 8 rows of 8 is 64, so about 60 cm².", rnd))
    # counting cm² on a grid (shapes not used in set 2)
    for i, kd in enumerate(["L", "T", "step"]):
        while True:
            cells = rand_shape(rnd, kd)
            a, p = len(cells), perim(cells)
            w, h = size(cells)
            if cells in seen or a == p or a < 6 or w * h == a:
                continue
            seen.add(cells)
            break
        q = (fig(one_grid(cells, "rectilinear shape on a centimetre grid")) +
             "Each square is 1 cm². What is the area of the shaded shape?")
        e = ("Count the squares, row by row: %s = %d. Each square is 1 cm², so the area is %d cm². "
             "Area uses square units: cm², not cm." % (row_sum(cells), a, a))
        cands = [["%d cm" % a, "%d m²" % a, "%d cm²" % p], ["%d cm²" % p, "%d cm" % a, "%d cm²" % (w * h)],
                 ["%d m²" % a, "%d cm²" % (w * h), "%d cm" % a]][i]
        its.append(mcq(q, "%d cm²" % a, cands, e, rnd))
    for poly, name in HALF_CM:
        its.append(half_q(poly, name, "cm²", rnd, "centimetre grid"))
    its.append(mcq("Which is bigger: 5 m² or 50 cm²?", "5 m²", ["50 cm²", "They are the same", "You cannot tell"],
                   "1 m² is a square 1 m (100 cm) on each side. Even one m² is far bigger than 50 squares of 1 cm². "
                   "Look at the unit, not only the number.", rnd))
    its.append(mcq("Which area is the biggest?", "3 m²", ["30 cm²", "300 cm²", "90 cm²"],
                   "A square metre is much bigger than a square centimetre: a 1 m² square holds far more than "
                   "300 squares of 1 cm². So 3 m² is the biggest.", rnd))
    for k, (kd, what) in enumerate([("U", "a school garden"), ("L", "a classroom reading corner")]):
        while True:
            cells = rand_shape(rnd, kd, maxw=6, maxh=4)
            a, p = len(cells), perim(cells)
            w, h = size(cells)
            if cells in seen or a == p or a < 8:
                continue
            seen.add(cells)
            break
        q = (fig(one_grid(cells, "rectilinear plan on a squared grid")) +
             "This is a plan of %s. Each square is 1 m². What is its area?" % what)
        e = "Count the squares: %s = %d. Each square is 1 m², so the area is %d m²." % (row_sum(cells), a, a)
        its.append(mcq(q, "%d m²" % a, ["%d m" % a, "%d m²" % p, "%d cm²" % a], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Square centimetres and square metres", "items": its}


# ------------------------------------------------------------ set 5: curved shapes and word problems
BLOB_THINGS = [("leaf", "cm"), ("pond", "m"), ("handprint", "cm"), ("flower bed", "m"), ("ink blot", "cm"),
               ("paint splat", "cm")]


def set_story(rnd, P, seen):
    its = []
    used_blobs = set()
    for k, (thing, u) in enumerate(BLOB_THINGS):
        poly, cols, rows, whole, more, less = make_blob(rnd, used_blobs, 8, 20)
        N, T = whole + more, whole + more + less
        svg = blob_svg(poly, cols, rows, "curved shape of %s on a squared grid" % an(thing))
        what = ("This map of a %s is drawn on a grid. Each square is 1 m²." % thing if u == "m"
                else "Each square is 1 cm².")
        q = (fig(svg) + "%s Estimate the area of the %s. Count whole squares and squares that are half or more "
             "covered." % (what, thing))
        e = ("Whole squares: %d. Squares half or more covered: %d. Estimate: %d + %d = %d %s. "
             "Squares less than half covered (%d) are not counted." % (whole, more, whole, more, N, SQ[u], less))
        cands = ["%d %s" % (whole, SQ[u]), "%d %s" % (T, SQ[u]), "%d %s" % (whole + less, SQ[u]), "%d %s" % (N, u)]
        r = k % 3
        cands = cands[r:3] + cands[:r] + cands[3:]
        its.append(mcq(q, "%d %s" % (N, SQ[u]), cands, e, rnd))
    its.append(mcq("You estimate the area of a curved shape on a grid. Which squares do you count?",
                   "Whole and half or more covered",
                   ["Only whole squares", "Every square it touches", "Only part squares"],
                   "Count every whole square, and count a square as 1 if half or more of it is covered. "
                   "Leave out squares that are less than half covered. The bits you count and leave out "
                   "roughly balance.", rnd))

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    r, c = 4, 6
    add("The reading corner floor is covered with square carpet tiles. Each tile is 1 m². There are %d rows of %d "
        "tiles. What is the area of the reading corner?" % (r, c), "%d m²" % (r * c),
        ["%d m²" % (r + c), "%d m²" % (2 * (r + c)), "%d m" % (r * c)],
        "Each tile is 1 m², so count the tiles: %d rows of %d is %s. The area is %d m²." % (r, c, skip(r, c), r * c))
    add("The teacher has 30 carpet tiles. The carpet for circle time needs 5 rows of 5 tiles. How many tiles are "
        "left over?", "5 tiles", ["25 tiles", "55 tiles", "10 tiles"],
        "Carpet: 5 rows of 5 is 5, 10, 15, 20, 25 tiles. Left over: 30 − 25 = 5 tiles.")
    n, he, his = P.next()
    add("%s’s family plants a vegetable garden. It is marked into 1 m squares: 3 rows of 5 squares. "
        "What is the area of the garden?" % n, "15 m²", ["8 m²", "16 m²", "15 m"],
        "3 rows of 5: 5, 10, 15. Each square is 1 m², so the area is 15 m². (16 is the distance around, in m.)")
    add("In a school garden, tomatoes fill 6 squares, beans fill 4 squares and carrots fill 5 squares. "
        "Each square is 1 m². What area is planted?", "15 m²", ["3 m²", "10 m²", "15 m"],
        "Add the squares: 6 + 4 + 5 = 15. Each square is 1 m², so 15 m² is planted.")
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    add("%s’s garden covers 12 squares of 1 m². %s’s garden covers 9 squares of 1 m². How much bigger is %s’s "
        "garden?" % (n1, n2, n1), "3 m²", ["21 m²", "3 m", "12 m²"],
        "Find the difference: 12 − 9 = 3. %s’s garden is 3 m² bigger. (21 m² is both gardens together.)" % n1)
    while True:
        cells = rand_shape(rnd, "L", maxw=6, maxh=4)
        a, p = len(cells), perim(cells)
        w, h = size(cells)
        if cells in seen or a == p or a < 9 or w * h - a < 3 or w * h == p:
            continue
        seen.add(cells)
        break
    add(fig(one_grid(cells, "rectilinear plan of a patio on a squared grid")) +
        "This is a plan of a patio. Each square is 1 m². How many 1 m² patio stones cover it with no gaps?",
        "%d stones" % a, ["%d stones" % p, "%d stones" % (w * h), "%d stones" % (a - 1)],
        "Count the squares, row by row: %s = %d. One stone covers each square, so %d stones are needed. "
        "(%d counts the empty squares in the corner too.)" % (row_sum(cells), a, a, w * h))
    add("Each gym mat covers 2 m². The class lays 6 mats on the floor with no gaps or overlaps. "
        "What area do the mats cover?", "12 m²", ["6 m²", "8 m²", "12 m"],
        "6 mats of 2 m² each: 2, 4, 6, 8, 10, 12. They cover 12 m². (6 + 2 = 8 adds instead.)")
    add("On a snow day, the class marks out a square area for a snow fort, 5 m by 5 m, in 1 m squares. "
        "What is its area?", "25 m²", ["10 m²", "20 m²", "25 m"],
        "5 rows of 5: 5, 10, 15, 20, 25. The area is 25 m². (20 m is the distance around.)")
    n, he, his = P.next()
    add("For Thanksgiving, %s covers a paper placemat with square stickers: 3 rows of 7 stickers, with no gaps. "
        "What is the area of the placemat in stickers?" % n, "21 stickers",
        ["10 stickers", "16 stickers", "14 stickers"],
        "3 rows of 7: 7, 14, 21 stickers. (16 is only the stickers around the edge, and 14 is 2 rows.)")
    add("A floor needs 4 rows of 5 square tiles. 13 tiles are already down. How many more tiles are needed?",
        "7 tiles", ["20 tiles", "33 tiles", "9 tiles"],
        "Whole floor: 4 rows of 5 is 5, 10, 15, 20 tiles. Still needed: 20 − 13 = 7 tiles.")
    add("A hallway rug covers 8 m². A bedroom rug covers 6 m². What area do the two rugs cover together?",
        "14 m²", ["2 m²", "14 m", "48 m²"],
        "Add the areas: 8 + 6 = 14 m². Area is in square metres, so the answer is 14 m², not 14 m.")
    n, he, his = P.next()
    add("%s wants to know how much carpet will cover %s bedroom floor. What should %s find?" % (n, his, he),
        "The area, in m²", ["The perimeter, in m", "The area, in m", "The length, in cm"],
        "Covering a floor is area: the space inside. A floor is big, so the area is in square metres (m²).")
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    add("%s’s garden is 4 rows of 3 squares. %s’s garden is 2 rows of 5 squares. Each square is 1 m². "
        "Whose garden has the bigger area?" % (n1, n2), "%s’s, by 2 m²" % n1,
        ["%s’s, by 2 m²" % n2, "They are the same", "%s’s, by 1 m²" % n2],
        "%s: 4 rows of 3 is 12 m². %s: 2 rows of 5 is 10 m². 12 − 10 = 2, so %s’s garden is bigger by 2 m². "
        "(4 + 3 and 2 + 5 are both 7, but that is not the area. A longer row does not mean a bigger area.)" % (n1, n2, n1))
    assert len(its) == 20, len(its)
    return {"title": "Curved shapes and word problems", "items": its}


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
    rnd = random.Random(33813 + 7)
    poly, cols, rows, whole, more, less = make_blob(rnd, set(), 10, 16)
    return blob_svg(poly, cols, rows, "curved shape of a leaf on a squared grid"), whole, more, less


def body_html():
    assert len(LESSON_L) == 14 and perim(LESSON_L) == 18
    assert poly_counts(HALF_SHAPES[1]) == (14, 4)
    assert len(TRI_HEX) == 6 and tri_edges(TRI_HEX) == 6
    bsvg, whole, more, less = lesson_blob()
    return (
        "<h2>What is area?</h2>"
        "<p><b>Area</b> is the amount of space a flat shape covers. We measure it by <b>covering</b> the shape "
        "with units that are all the same size, and counting them.</p>"
        "<figure class='sn-fig'>" + tri_svg(TRI_HEX, "hexagon covered by triangle pattern blocks") +
        "<figcaption>This hexagon is covered by 6 triangles. Its area is 6 triangles.</figcaption></figure>"
        "<p>The size of the unit matters. Small units: you need <b>more</b> of them. Big units: you need "
        "<b>fewer</b>. To compare two areas, use the same unit.</p>"
        "<h2>No gaps and no overlaps</h2>"
        "<p>Units must cover the whole shape, with no gaps, no overlaps and nothing hanging over the edge.</p>"
        "<figure class='sn-fig'>" + trays_svg(["ok", "gap", "overlap", "edge"]) +
        "<figcaption>A is right. B has gaps (the count is too small). C has overlaps and D hangs over the edge "
        "(the count is too big).</figcaption></figure>"
        "<h2>Count square units</h2>"
        "<p>Squares are the best units: they fit together with no gaps. Count the squares inside, row by row.</p>"
        "<figure class='sn-fig'>" + one_grid(LESSON_L, "rectilinear shape on a squared grid") +
        "<figcaption>2 + 2 + 5 + 5 = 14 squares. The area is 14 square units.</figcaption></figure>" +
        ex("Example", "A rectangle has 3 rows of 5 squares. What is its area?",
           "Skip count by the row: 5, 10, 15.", "15 square units") +
        "<p>Two half squares make one whole square.</p>"
        "<figure class='sn-fig'>" + one_grid(HALF_SHAPES[1], "house shape with half squares on a squared grid") +
        "<figcaption>14 whole squares and 4 half squares. 4 halves make 2 squares. Area = 14 + 2 = 16 square units."
        "</figcaption></figure>"
        "<h2>Square centimetres and square metres</h2>"
        "<p>A <b>square centimetre (1 cm²)</b> is a square 1 cm on each side, about the size of a fingernail. "
        "Use cm² for small things such as a stamp or a page.</p>"
        "<p>A <b>square metre (1 m²)</b> is a square 1 m on each side. Use m² for big spaces such as a floor, "
        "a garden or a rink.</p>" +
        table(["Measuring", "Small things", "Big things"], [
            ["Length (cm, m)", "cm: a pencil, a photo", "m: a hallway, a hockey rink"],
            ["Area (cm², m²)", "cm²: a stamp, a sticky note", "m²: a classroom floor, a garden"],
        ]) +
        "<h2>Estimate the area of a curved shape</h2>"
        "<p>Curved shapes do not fit the squares exactly, so we estimate. Count each whole square. "
        "Count a square as 1 if <b>half or more</b> is covered. Leave out squares that are less than half covered.</p>"
        "<figure class='sn-fig'>" + bsvg +
        "<figcaption>Each square is 1 cm². Whole squares: %d. Half or more covered: %d. "
        "Estimate: %d + %d = %d cm².</figcaption></figure>" % (whole, more, whole, more, whole + more) +
        ex("Example", "A garden is marked into 1 m squares: 4 rows of 5. What is its area?",
           "4 rows of 5: 5, 10, 15, 20. Each square is 1 m².", "20 m²") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the sides around the edge", "That is the perimeter. For area, count the squares inside"],
            ["Counting only the squares along the edge", "Count every square, the inside ones too"],
            ["Leaving gaps or overlapping units", "Cover with no gaps and no overlaps"],
            ["Comparing counts of different-size units", "Use the same unit for both shapes"],
            ["Counting a half square as a whole one", "Two half squares make one square"],
            ["Writing cm or m for an area", "Area is in square units: cm² or m²"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about area in the Ontario math curriculum?",
     "a": "They measure area by covering shapes with same-size units with no gaps or overlaps, see that smaller units mean a bigger count, and use square centimetres (cm²) and square metres (m²) to estimate, measure and compare areas, including shapes with curved sides."},
    {"q": "What is the difference between area and perimeter?",
     "a": "Area is the space inside a shape, measured in square units such as cm² or m². Perimeter is the distance around the outside, measured in cm or m."},
    {"q": "Why do gaps and overlaps matter when measuring area?",
     "a": "Gaps leave space uncounted, so the area comes out too small. Overlaps and units hanging over the edge count space twice or outside the shape, so the area comes out too big."},
    {"q": "Is area on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, and measurement, including area, is part of it. Counting square units and choosing cm² or m² are good skills to practise."},
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
    rnd = random.Random(33813)
    P = People(rnd)
    fixed_pos = [0, 1, 2, 3]
    rnd.shuffle(fixed_pos)
    seen = set()
    sets = [set_cover(rnd, P, fixed_pos[:3]), set_count(rnd, seen), set_gaps(rnd, P), set_units(rnd, seen),
            set_story(rnd, P, seen)]
    for i in (0, 4):
        rnd.shuffle(sets[i]["items"])
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "area", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Area",
        "seo_title": "Grade 3 Area Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Area",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E2.9",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use square centimetres (cm²) and square metres (m²) to estimate, measure, and compare the areas of various two-dimensional shapes, including those with curved sides",
        "meta_desc": "Free Grade 3 area worksheets for the Ontario math curriculum (E2.7, E2.8, E2.9): compare areas by covering, count square units and half squares, avoid gaps and overlaps, use cm² and m², and estimate curved shapes on a grid. 100 questions with an answer key, great EQAO practice.",
        "key_big": "Area is the space a shape covers. Cover it with same-size squares, with no gaps and no overlaps, and count them.",
        "key_sub": "Two half squares make one square. Use cm² for small things and m² for big spaces. For curved shapes, count squares that are half or more covered.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(grid|trays|rectangle with square tiles)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
