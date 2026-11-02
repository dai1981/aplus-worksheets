# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Area and Perimeter (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: Area and Volume)
  python3 tools/gen_sg_maths_p3_area_perimeter.py
Area by counting squares (square units, cm²), perimeter by counting 1-unit sides, perimeter of
rectangles and squares, area of rectangles and squares (cm², m²), perimeter of rectilinear figures and
word problems (fencing, tiles, ribbon) with bar models.
Grid and polygon helpers adapted from gen_uk_maths_y3_perimeter.py and gen_cabc_math_g5_area_perimeter.py
(rewritten for Singapore). Every figure is drawn to scale from its numbers.
Singapore style: length and breadth, cm and m, cm² and m², $ for money.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
FS = 16
NBSP = " "
SQ = {"cm": "cm²", "m": "m²", "units": "square units"}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, fixed=False):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers).
    fixed=True keeps the given order (choices are picture labels A, B, C, D)."""
    correct = str(correct)
    if fixed:
        assert len(cands) == 4 and correct in cands
        return {"q": q, "c": list(cands), "a": cands.index(correct), "e": e, "fixed": True}
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
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


def rot(c, k):
    r = k % len(c)
    return c[r:] + c[:r]


def plus(nums):
    return " + ".join(str(n) for n in nums)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count(NBSP) * 0.3) * fs * 0.6


def text(x, y, t, fs=FS, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ squared grids
def rect_cells(w, h, c0=0, r0=0):
    return {(c0 + i, r0 + j) for i in range(w) for j in range(h)}


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
    """Squares that touch the edge (the 'count the squares round the edge' mistake)."""
    return sum(1 for (c, r) in cells
               if any((c + dc, r + dr) not in cells for dc, dr in [(0, -1), (0, 1), (-1, 0), (1, 0)]))


def bbox_perim(cells):
    w, h = size(cells)
    return 2 * (w + h)


def cells_body(cells, x0, y0, cols, rows, cell):
    """Grid lines over cols × rows starting at (x0, y0), shaded cells, thick outline round the shape."""
    g = []
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                 % (x0 + c * cell, y0 + r * cell, cell, cell, FILL))
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 + i * cell, y0, x0 + i * cell, y0 + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0, y0 + j * cell, x0 + cols * cell, y0 + j * cell, GRIDC))
    for (c, r) in sorted(cells):
        x, y = x0 + c * cell, y0 + r * cell
        for (ec, er, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                          (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (c + ec, r + er) not in cells:
                g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' "
                         "stroke-linecap='round'/>" % (x1, y1, x2, y2, GREEN))
    return "".join(g)


def one_grid(cells, label, cell=24):
    """Shape on a grid with one empty square all round."""
    w, h = size(cells)
    m = 5
    moved = {(c + 1, r + 1) for c, r in cells}
    body = cells_body(moved, m, m, w + 2, h + 2, cell)
    return svg_wrap((w + 2) * cell + 2 * m, (h + 2) * cell + 2 * m, body, label)


def multi_grid(shapes, label, cell=18):
    """Several shapes side by side on one grid, labelled A, B, C, D above."""
    m, th = 5, 24
    rows = max(size(s)[1] for s in shapes) + 2
    cols = 1 + sum(size(s)[0] + 1 for s in shapes)
    allc, x = set(), 1
    xs = []
    for s in shapes:
        w, h = size(s)
        allc |= {(c + x, r + 1) for c, r in s}
        xs.append(x + w / 2.0)
        x += w + 1
    assert not any((c + 1, r) in allc and False for c, r in allc)
    body = cells_body(allc, m, m + th, cols, rows, cell)
    for k, cx in enumerate(xs):
        body += text(m + cx * cell, m + 18, "ABCD"[k], 17)
    return svg_wrap(cols * cell + 2 * m, rows * cell + 2 * m + th, body, label)


def flipcells(cells, rnd):
    w, h = size(cells)
    if rnd.random() < 0.5:
        cells = {(w - 1 - c, r) for c, r in cells}
    if rnd.random() < 0.5:
        cells = {(c, h - 1 - r) for c, r in cells}
    return frozenset(cells)


def connected(cells):
    cells = set(cells)
    start = next(iter(cells))
    seen, todo = {start}, [start]
    while todo:
        c, r = todo.pop()
        for dc, dr in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            n = (c + dc, r + dr)
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return len(seen) == len(cells)


def rand_shape(rnd, kind):
    """A rectilinear shape made of squares."""
    if kind == "L":
        w2, h2 = rnd.randint(4, 6), rnd.randint(1, 3)
        w1, h1 = rnd.randint(1, w2 - 2), rnd.randint(1, 3)
        cells = rect_cells(w1, h1) | rect_cells(w2, h2, 0, h1)
    elif kind == "T":
        top, st, sw = rnd.randint(1, 2), rnd.randint(1, 3), rnd.randint(1, 2)
        cells = rect_cells(5, top) | rect_cells(sw, st, (5 - sw) // 2, top)
    elif kind == "U":
        w, h = rnd.choice([(5, 3), (5, 4), (6, 3), (6, 4)])
        gw, gh = rnd.randint(1, w - 4), rnd.randint(1, h - 1)
        cells = rect_cells(w, h) - rect_cells(gw, gh, (w - gw) // 2, 0)
    elif kind == "plus":
        cells = rect_cells(3, 1, 0, 1) | rect_cells(1, 3, 1, 0)
        if rnd.random() < 0.5:
            cells = rect_cells(4, 2, 0, 1) | rect_cells(2, 4, 1, 0)
    else:  # step
        a, b, c = rnd.randint(1, 2), rnd.randint(1, 2), rnd.randint(1, 2)
        cells = rect_cells(a, 3) | rect_cells(b, 2, a, 1) | rect_cells(c, 1, a + b, 2)
    return flipcells(cells, rnd)


# ------------------------------------------------------------ labelled shapes (drawn to scale)
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
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


class Crowded(Exception):
    pass


def polygon_svg(upts, labels, label, max_w=230, max_h=130, kmax=26):
    """Polygon from unit points (scaled). labels[i] belongs to side i -> i+1 ('' = none, '?' = red).
    Each label sits outside the middle of its side; labels may not touch the shape or each other."""
    xs0 = [p[0] for p in upts]
    ys0 = [p[1] for p in upts]
    k = min(max_w / float(max(xs0) - min(xs0)), max_h / float(max(ys0) - min(ys0)), kmax)
    pts = [((x - min(xs0)) * k, (y - min(ys0)) * k) for x, y in upts]
    n = len(pts)
    sa = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    boxes, texts = [], []
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = (dy / L, -dx / L) if sa > 0 else (-dy / L, dx / L)        # outward normal
        hw = tw(t, FS) / 2
        off = 6 + abs(nx) * hw + abs(ny) * 10
        cx, cy = (x1 + x2) / 2 + nx * off, (y1 + y2) / 2 + ny * off
        bx = (cx - hw, cy - 10, cx + hw, cy + 10)
        for B in boxes:
            if bx[0] < B[2] + 16 and B[0] < bx[2] + 16 and bx[1] < B[3] + 10 and B[1] < bx[3] + 10:
                raise Crowded(labels)
        grow = (bx[0] - 2, bx[1] - 2, bx[2] + 2, bx[3] + 2)
        for j in range(n):
            if seg_hits_box(pts[j], pts[(j + 1) % n], grow):
                raise Crowded(labels)
        if inside(pts, cx, cy):
            raise Crowded(labels)
        boxes.append(bx)
        texts.append((cx, cy, t))
    xs = [p[0] for p in pts] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for p in pts] + [b[1] for b in boxes] + [b[3] for b in boxes]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for cx, cy, t in texts:
        s.append(text(cx - ox, cy - oy + 6, t, FS, RED if "?" in t else INK))
    return svg_wrap(W, H, "".join(s), label)


def rect_svg(L, B, u, label, top=None, left=None, max_w=190, max_h=95):
    """L × B rectangle with the length on top and the breadth on the left."""
    top = "%d %s" % (L, u) if top is None else top
    left = "%d %s" % (B, u) if left is None else left
    return polygon_svg([(0, 0), (L, 0), (L, B), (0, B)], [top, "", "", left], label, max_w, max_h, 24)


def sides_of(upts):
    n = len(upts)
    return [abs(upts[(i + 1) % n][0] - upts[i][0]) + abs(upts[(i + 1) % n][1] - upts[i][1]) for i in range(n)]


def flip_pts(upts, fx, fy):
    W = max(p[0] for p in upts)
    H = max(p[1] for p in upts)
    return [((W - x) if fx else x, (H - y) if fy else y) for x, y in upts]


# ------------------------------------------------------------ bar model (drawn to scale)
def model_svg(rows, label, W=400):
    """rows: dicts with name, segs [(length, text, shaded)], over/under [(start, end, text)]."""
    names = [r.get("name", "") for r in rows]
    nw = (max(tw(n, 15) for n in names) + 12) if any(names) else 0
    L = 8 + nw
    R = W - 10
    tot = max(sum(a for a, _, _ in r["segs"]) for r in rows)
    sc = (R - L) / float(tot)
    s = []
    y = 4
    for r in rows:
        over, under = r.get("over", []), r.get("under", [])
        if over:
            y += 24
            for a, b, t in over:
                x1, x2 = L + a * sc, L + b * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 6, x1, y, x2, y, x2, y + 6, col))
                assert tw(t, 15) <= x2 - x1 + 20, t
                s.append(text((x1 + x2) / 2, y - 6, t, 15, col))
            y += 8
        bh = 34
        x = L
        for a, t, sh in r["segs"]:
            w = a * sc
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, w, bh, FILL if sh else "#ffffff", INK))
            if t:
                assert tw(t, 14) + 4 <= w, ("text too wide", t, w)
                s.append(text(x + w / 2, y + bh / 2 + 5, t, 14, RED if "?" in t else INK))
            x += w
        if r.get("name"):
            s.append(text(8, y + bh / 2 + 5, r["name"], 15, INK, "start"))
        y += bh
        if under:
            for a, b, t in under:
                x1, x2 = L + a * sc, L + b * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 4, x1, y + 10, x2, y + 10, x2, y + 4, col))
                s.append(text((x1 + x2) / 2, y + 28, t, 15, col))
            y += 32
        y += 10
    return svg_wrap(W, y - 4, "".join(s), label)


# ------------------------------------------------------------ set 1: area by counting squares
def set_count(rnd):
    its = []
    seen = set()
    for k, (L, B, un) in enumerate([(4, 3, "units"), (5, 2, "units"), (7, 3, "cm"), (3, 3, "cm"),
                                    (6, 2, "cm"), (5, 4, "units"), (6, 4, "cm")]):
        cells = frozenset(rect_cells(L, B))
        seen.add(cells)
        A, P, bd = L * B, 2 * (L + B), border(cells)
        assert A != P
        shape = "square" if L == B else "rectangle"
        unit = SQ[un]
        if un == "cm":
            q = fig(one_grid(cells, "%s %d squares by %d squares on a grid" % (shape, L, B))) + \
                "Each small square is 1 cm². What is the area of the shaded %s?" % shape
            cands = rot(["%d cm²" % P, "%d cm²" % bd, "%d cm²" % (L + B)], k) + ["%d cm" % A, "%d cm²" % (A + L)]
        else:
            q = fig(one_grid(cells, "%s %d squares by %d squares on a grid" % (shape, L, B))) + \
                "Each small square is 1 square unit. What is the area of the shaded %s?" % shape
            cands = rot(["%d square units" % P, "%d square units" % bd, "%d square units" % (L + B)], k) + \
                ["%d square units" % (A + L)]
        e = ("Count the squares inside: %d rows of %d squares. %d × %d = %d, so the area is %d %s. "
             "(%d is the perimeter, the distance round the edge.)" % (B, L, B, L, A, A, unit, P))
        its.append(mcq(q, "%d %s" % (A, unit), cands, e, rnd))
    # rectilinear shapes: count the squares
    for k, kind in enumerate(["L", "T", "U", "step", "L", "plus"]):
        while True:
            cells = rand_shape(rnd, kind)
            A, P = len(cells), perim(cells)
            w, h = size(cells)
            if cells in seen or A == P or w * h == A or not connected(cells):
                continue
            seen.add(cells)
            break
        un = "cm" if k % 2 else "units"
        unit = SQ[un]
        q = fig(one_grid(cells, "shape made of squares on a grid")) + \
            ("Each small square is 1 cm². What is the area of the shaded figure?" if un == "cm" else
             "Each small square is 1 square unit. What is the area of the shaded figure?")
        cands = rot(["%d %s" % (w * h, unit), "%d %s" % (P, unit), "%d %s" % (A - 1, unit)], k)
        if un == "cm":
            cands = cands[:2] + ["%d cm" % A] + cands[2:]
        e = ("Count the shaded squares one by one, and tick each one so you count it only once: %d squares. "
             "The area is %d %s. (Do not count the empty squares that make it a full rectangle.)" % (A, A, unit))
        its.append(mcq(q, "%d %s" % (A, unit), cands, e, rnd))
    # a frame of squares: corner squares counted twice
    for k, (L, B) in enumerate([(5, 4), (7, 3)]):
        cells = frozenset(rect_cells(L, B) - rect_cells(L - 2, B - 2, 1, 1))
        A = len(cells)
        assert A == 2 * (L + B) - 4
        q = fig(one_grid(cells, "frame of squares on a grid")) + \
            "Each small square is 1 cm². What is the area of the shaded frame?"
        e = ("Count each square once. Top and bottom rows: %d + %d = %d. The sides have %d + %d more "
             "(the corner squares are already counted). %d + %d = %d cm². "
             "(%d cm² counts the 4 corner squares twice.)" % (L, L, 2 * L, B - 2, B - 2, 2 * L, 2 * (B - 2), A,
                                                              2 * (L + B)))
        cands = rot(["%d cm²" % (2 * (L + B)), "%d cm²" % (L * B), "%d cm²" % ((L - 2) * (B - 2))], k)
        its.append(mcq(q, "%d cm²" % A, cands, e, rnd))
    # A–D pictures: which shape has the largest / smallest area
    for target, mode in [(2, "largest"), (1, "smallest")]:
        for _ in range(500):
            shapes = []
            for kind in ["L", "T", "step", "U"]:
                c = rand_shape(rnd, kind)
                while not connected(c) or size(c)[0] > 6 or size(c)[1] > 4:
                    c = rand_shape(rnd, kind)
                shapes.append(c)
            rnd.shuffle(shapes)
            areas = [len(s) for s in shapes]
            ext = max(areas) if mode == "largest" else min(areas)
            widest = max(range(4), key=lambda i: size(shapes[i])[0] * 10 + size(shapes[i])[1])
            if (len(set(areas)) == 4 and areas.index(ext) == target and widest != target
                    and sum(size(s)[0] for s in shapes) <= 18):
                break
        else:
            raise RuntimeError("no A-D shapes")
        q = fig(multi_grid(shapes, "four shapes A, B, C and D on a grid")) + \
            "Each small square is 1 square unit. Which shape has the %s area?" % mode
        e = ("Count the squares in each shape: A = %d, B = %d, C = %d, D = %d. Shape %s has the %s area, "
             "%d square units. (The shape that looks widest does not always cover the most squares.)"
             % (areas[0], areas[1], areas[2], areas[3], "ABCD"[target], mode, ext))
        its.append(mcq(q, "Shape " + "ABCD"[target], ["Shape A", "Shape B", "Shape C", "Shape D"], e, rnd, True))
    # rows of squares in words
    for k, (r, c, un) in enumerate([(3, 7, "cm"), (4, 6, "m")]):
        A = r * c
        q = ("A rectangle is covered with %d rows of 1 %s squares. There are %d squares in each row. "
             "What is its area?" % (r, SQ[un], c))
        e = "%d rows of %d squares: %d × %d = %d squares, so the area is %d %s." % (r, c, r, c, A, A, SQ[un])
        cands = rot(["%d %s" % (r + c, SQ[un]), "%d %s" % (2 * (r + c), SQ[un])], k) + ["%d %s" % (A, un)]
        its.append(mcq(q, "%d %s" % (A, SQ[un]), cands, e, rnd))
    its.append(mcq("What does the area of a figure tell you?", "How much surface it covers",
                   ["The distance round its edge", "How many sides it has", "How long its longest side is"],
                   "Area is the amount of surface a figure covers. We find it by counting the squares inside. "
                   "The distance round the edge is the perimeter.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area by counting squares", "items": its}


# ------------------------------------------------------------ set 2: perimeter by counting units
def set_count_p(rnd):
    its = []
    seen = set()
    for k, (L, B, un) in enumerate([(4, 2, "cm"), (5, 3, "units"), (6, 2, "cm"), (3, 3, "units"),
                                    (7, 3, "cm"), (5, 4, "m"), (6, 5, "cm"), (4, 4, "units")]):
        cells = frozenset(rect_cells(L, B))
        seen.add(cells)
        A, P, bd = L * B, 2 * (L + B), border(cells)
        shape = "square" if L == B else "rectangle"
        unit = un
        if un == "units":
            intro = "Each small square has sides of 1 unit."
        else:
            intro = "Each small square has sides of 1 %s." % un
        q = fig(one_grid(cells, "%s %d squares by %d squares on a grid" % (shape, L, B))) + \
            intro + " What is the perimeter of the %s?" % shape
        pool = ["%d %s" % (v, unit) for v in [bd, A, L + B]]
        pool = rot(pool, k)
        if un != "units":
            pool = pool[:2] + ["%d %s" % (P, SQ[un])] + pool[2:]
        pool.append("%d %s" % (P + 4, unit))
        e = ("Count the sides of the small squares all the way round: %d + %d + %d + %d = %d %s. "
             "A corner square has 2 sides on the edge, so count both." % (L, B, L, B, P, unit))
        if A != P:
            e += " (%d is the number of squares inside: that is the area.)" % A
        its.append(mcq(q, "%d %s" % (P, unit), pool, e, rnd))
    for k, kind in enumerate(["L", "U", "T", "step", "U", "plus", "L", "T"]):
        while True:
            cells = rand_shape(rnd, kind)
            A, P, bd = len(cells), perim(cells), border(cells)
            if cells in seen or not connected(cells) or bd == P or A == P:
                continue
            seen.add(cells)
            break
        un = ["cm", "units", "m"][k % 3]
        intro = "Each small square has sides of 1 unit." if un == "units" else \
            "Each small square has sides of 1 %s." % un
        q = fig(one_grid(cells, "shape made of squares on a grid")) + intro + \
            " What is the perimeter of the figure?"
        bp = bbox_perim(cells)
        pool = ["%d %s" % (bd, un), "%d %s" % (A, un)]
        pool.append("%d %s" % (bp if bp != P else P - 2, un))
        pool = rot(pool, k) + ["%d %s" % (P + 2, un)]
        e = ("Start at one corner and count every 1-%s side round the outside, including the short sides "
             "that go in and out: %d %s. Count the sides, not the squares (there are %d squares)."
             % ("unit" if un == "units" else un, P, un, A))
        its.append(mcq(q, "%d %s" % (P, un), pool, e, rnd))
    # A–D: which shape has the longest perimeter
    for target in [3]:
        for _ in range(2000):
            shapes = []
            for kind in ["L", "T", "step", "U"]:
                c = rand_shape(rnd, kind)
                while not connected(c) or size(c)[0] > 6 or size(c)[1] > 4:
                    c = rand_shape(rnd, kind)
                shapes.append(c)
            rnd.shuffle(shapes)
            ps = [perim(s) for s in shapes]
            ars = [len(s) for s in shapes]
            if (len(set(ps)) == 4 and ps.index(max(ps)) == target and ars.index(max(ars)) != target
                    and sum(size(s)[0] for s in shapes) <= 18):
                break
        else:
            raise RuntimeError("no A-D shapes")
        q = fig(multi_grid(shapes, "four shapes A, B, C and D on a grid")) + \
            "Each small square has sides of 1 cm. Which shape has the longest perimeter?"
        e = ("Count the 1 cm sides round each shape: A = %d cm, B = %d cm, C = %d cm, D = %d cm. "
             "Shape %s has the longest perimeter. (The shape with the most squares does not always have "
             "the longest perimeter.)" % (ps[0], ps[1], ps[2], ps[3], "ABCD"[target]))
        its.append(mcq(q, "Shape " + "ABCD"[target], ["Shape A", "Shape B", "Shape C", "Shape D"], e, rnd, True))
    # two rectangles with the same area
    a, b = frozenset(rect_cells(6, 2)), frozenset(rect_cells(4, 3))
    q = fig(multi_grid([a, b], "two shapes A and B on a grid")) + \
        "Each small square has sides of 1 cm. Which sentence is true?"
    e = ("A: 12 squares, perimeter 6 + 2 + 6 + 2 = 16 cm. B: 12 squares, perimeter 4 + 3 + 4 + 3 = 14 cm. "
         "Same area, but A has the longer perimeter.")
    its.append(mcq(q, "A has the longer perimeter", ["B has the longer perimeter", "A has the bigger area",
                                                     "B has the bigger area"], e, rnd))
    its.append(mcq("What is the perimeter of a figure?", "The distance round it",
                   ["The squares it covers", "The length of one side", "The number of corners"],
                   "Perimeter is the total length of the sides all the way round a figure. "
                   "The squares a figure covers give its area.", rnd))
    its.append(mcq("Mei Ling walks once round the edge of a square mat. Each side is 3 m. How far does she walk?",
                   "12 m", ["9 m", "6 m", "12 m²", "3 m"],
                   "Once round the edge is the perimeter: 3 + 3 + 3 + 3 = 12 m. (9 m² would be the area.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter by counting units", "items": its}


# ------------------------------------------------------------ set 3: perimeter of rectangles and squares
def set_rect_p(rnd):
    its = []
    seen = set()
    k = 0
    while len(its) < 8:
        u = "cm" if len(its) % 3 != 2 else "m"
        L, B = rnd.randint(5, 15), rnd.randint(2, 9)
        if L <= B + 1 or L > 2.5 * B + 4 or (L, B) in seen:
            continue
        seen.add((L, B))
        P = 2 * (L + B)
        q = fig(rect_svg(L, B, u, "rectangle %d %s by %d %s" % (L, u, B, u))) + \
            "What is the perimeter of this rectangle?"
        pool = rot(["%d %s" % (v, u) for v in [L + B, 2 * L + B, L * B]], k) + ["%d %s" % (P, SQ[u])]
        k += 1
        e = ("A rectangle has 4 sides. Opposite sides are equal, so the sides are %d, %d, %d and %d. "
             "%d + %d + %d + %d = %d %s. (%d + %d = %d %s is only half the way round.)"
             % (L, B, L, B, L, B, L, B, P, u, L, B, L + B, u))
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (s, u) in enumerate([(6, "cm"), (9, "cm"), (8, "m")]):
        P = 4 * s
        q = fig(polygon_svg([(0, 0), (s, 0), (s, s), (0, s)], ["%d %s" % (s, u), "", "", ""],
                            "square with %d %s sides" % (s, u), 95, 95, 12)) + \
            "This is a square. What is its perimeter?"
        pool = rot(["%d %s" % (v, u) for v in [s * s, 2 * s, 3 * s]], k) + ["%d %s" % (P, SQ[u])]
        e = ("A square has 4 equal sides: %d + %d + %d + %d = %d %s. Or use multiplication: 4 × %d = %d. "
             "(%d × %d = %d is the area, not the perimeter.)" % (s, s, s, s, P, u, s, P, s, s, s * s))
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (L, B, u) in enumerate([(12, 7, "cm"), (25, 10, "m")]):
        P = 2 * (L + B)
        q = "A rectangle has a length of %d %s and a breadth of %d %s. What is its perimeter?" % (L, u, B, u)
        e = "%d + %d + %d + %d = %d %s." % (L, B, L, B, P, u)
        pool = rot(["%d %s" % (v, u) for v in [L + B, 2 * L + B, L * B]], k)
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (s, u) in enumerate([(7, "m"), (15, "cm")]):
        P = 4 * s
        q = "A square has sides of %d %s. What is its perimeter?" % (s, u)
        e = "4 equal sides: %d + %d + %d + %d = %d %s. (4 × %d = %d.)" % (s, s, s, s, P, u, s, P)
        pool = rot(["%d %s" % (v, u) for v in [s * s, 2 * s, s + 4]], k)
        its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (P, u) in enumerate([(32, "cm"), (24, "m")]):
        s = P // 4
        q = "A square has a perimeter of %d %s. How long is each side?" % (P, u)
        e = "The 4 sides are equal: %d ÷ 4 = %d %s. Check: 4 × %d = %d." % (P, s, u, s, P)
        pool = rot(["%d %s" % (v, u) for v in [P // 2, P - 4, P + 4]], k)
        its.append(mcq(q, "%d %s" % (s, u), pool, e, rnd))
    L, B, P = 9, 6, 30
    q = fig(rect_svg(L, B, "cm", "rectangle with one missing side", left="? cm")) + \
        "The perimeter of this rectangle is %d cm. What is the length of the side marked ?" % P
    e = ("The two long sides are 9 + 9 = 18 cm. 30 − 18 = 12 cm is left for the two short sides. "
         "12 ÷ 2 = 6 cm. Check: 9 + 6 + 9 + 6 = 30.")
    its.append(mcq(q, "6 cm", ["21 cm", "12 cm", "15 cm"], e, rnd))
    its.append(mcq("Which number sentence gives the perimeter of a square with sides of 7 cm?",
                   "7 + 7 + 7 + 7", ["7 × 7", "7 + 7", "7 + 4"],
                   "Perimeter adds all 4 sides: 7 + 7 + 7 + 7 = 28 cm. 7 × 7 gives the area.", rnd))
    its.append(mcq("Which number sentence gives the perimeter of a rectangle 8 m long and 3 m wide?",
                   "8 + 3 + 8 + 3", ["8 × 3", "8 + 3", "8 + 8 + 3"],
                   "A rectangle has 4 sides: 8 + 3 + 8 + 3 = 22 m. 8 × 3 gives the area. "
                   "8 + 3 is only 2 of the 4 sides.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter of rectangles and squares", "items": its}


# ------------------------------------------------------------ set 4: area of rectangles and squares
def set_rect_a(rnd):
    its = []
    for k, (L, B, u) in enumerate([(5, 3, "cm"), (8, 4, "m"), (7, 5, "cm"), (9, 6, "cm"), (6, 2, "m"),
                                   (9, 7, "m"), (8, 6, "cm")]):
        A, P = L * B, 2 * (L + B)
        assert A != P
        q = fig(rect_svg(L, B, u, "rectangle %d %s by %d %s" % (L, u, B, u))) + \
            "What is the area of this rectangle?"
        e = "Area = length × breadth = %d × %d = %d %s. (%d %s is the perimeter.)" % (L, B, A, SQ[u], P, u)
        pool = rot(["%d %s" % (P, SQ[u]), "%d %s" % (L + B, SQ[u]), "%d %s" % (A, u)], k)
        its.append(mcq(q, "%d %s" % (A, SQ[u]), pool, e, rnd))
    for k, (s, u) in enumerate([(5, "cm"), (8, "m"), (9, "cm")]):
        A = s * s
        q = fig(polygon_svg([(0, 0), (s, 0), (s, s), (0, s)], ["%d %s" % (s, u), "", "", ""],
                            "square with %d %s sides" % (s, u), 95, 95, 12)) + \
            "This is a square. What is its area?"
        e = ("All sides of a square are equal, so the length and the breadth are both %d %s. "
             "%d × %d = %d %s. (%d %s is the perimeter.)" % (s, u, s, s, A, SQ[u], 4 * s, u))
        pool = rot(["%d %s" % (4 * s, SQ[u]), "%d %s" % (2 * s, SQ[u]), "%d %s" % (A, u)], k)
        its.append(mcq(q, "%d %s" % (A, SQ[u]), pool, e, rnd))
    for k, (L, B, u) in enumerate([(12, 5, "cm"), (15, 4, "m"), (11, 8, "cm"), (20, 3, "m")]):
        A, P = L * B, 2 * (L + B)
        q = "A rectangle has a length of %d %s and a breadth of %d %s. What is its area?" % (L, u, B, u)
        t, o = divmod(L, 10)
        e = ("Area = length × breadth = %d × %d. %d × %d = %d and %d × %d = %d. %d + %d = %d %s."
             % (L, B, t * 10, B, t * 10 * B, o, B, o * B, t * 10 * B, o * B, A, SQ[u])) if o else \
            ("Area = length × breadth = %d × %d = %d %s." % (L, B, A, SQ[u]))
        pool = rot(["%d %s" % (P, SQ[u]), "%d %s" % (L + B, SQ[u]), "%d %s" % (A, u)], k)
        its.append(mcq(q, "%d %s" % (A, SQ[u]), pool, e, rnd))
    U4 = ["cm", "m", "cm²", "m²"]
    for thing, right, why in [
        ("the area of a postage stamp", "cm²", "A stamp is small, and area is the surface it covers, so use square centimetres."),
        ("the area of a classroom floor", "m²", "A floor is big, and area is the surface it covers, so use square metres."),
        ("the length of a pencil", "cm", "Length is not an area. A pencil is short, so use centimetres."),
    ]:
        its.append(mcq("Which unit is best for %s?" % thing, right, [x for x in U4 if x != right],
                       why + " cm and m measure length; cm² and m² measure area.", rnd))
    for k, (A, L, u) in enumerate([(24, 6, "cm"), (45, 9, "m")]):
        B = A // L
        q = fig(rect_svg(L, B, u, "rectangle with an area of %d %s and one side missing" % (A, SQ[u]),
                         left="? %s" % u)) + \
            "The area of this rectangle is %d %s. What is the length of the side marked ?" % (A, SQ[u])
        e = "Length × breadth = area, so %d × ? = %d. %d ÷ %d = %d %s. Check: %d × %d = %d." % (
            L, A, A, L, B, u, L, B, A)
        pool = rot(["%d %s" % (A - L, u), "%d %s" % (B, SQ[u]), "%d %s" % (A // 2 - L if A % 2 == 0 else B + 1, u)], k)
        pool.append("%d %s" % (B + 1, u))
        its.append(mcq(q, "%d %s" % (B, u), pool, e, rnd))
    its.append(mcq("Rectangle A is 6 cm long and 4 cm wide. Square B has sides of 5 cm. Which has the bigger area?",
                   "B, by 1 cm²", ["A, by 1 cm²", "They are the same", "B, by 4 cm²"],
                   "A: 6 × 4 = 24 cm². B: 5 × 5 = 25 cm². 25 − 24 = 1, so B is bigger by 1 cm². "
                   "(Their perimeters are both 20 cm, but the areas are different.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area of rectangles and squares (cm² and m²)", "items": its}


# ------------------------------------------------------------ set 5: rectilinear figures and word problems
def L_pts(a, b, c, d):
    """L-shape: top a, right b, inner step, bottom c, left d."""
    return [(0, 0), (a, 0), (a, b), (c, b), (c, d), (0, d)]


def T_pts(a, b, o, s, h):
    return [(0, 0), (a, 0), (a, b), (o + s, b), (o + s, b + h), (o, b + h), (o, b), (0, b)]


def U_pts(p, g, h1, a, H):
    return [(0, 0), (p, 0), (p, h1), (p + g, h1), (p + g, 0), (a, 0), (a, H), (0, H)]


def S_pts(x1, x2, x3, y1, y2, y3):
    return [(0, 0), (x1, 0), (x1, y1), (x2, y1), (x2, y2), (x3, y2), (x3, y3), (0, y3)]


def rect_fig(rnd, kind, u):
    """Random rectilinear figure with all sides labelled. Returns (svg, sides)."""
    for _ in range(3000):
        if kind == "L":
            a, d = rnd.randint(8, 16), rnd.randint(6, 12)
            c, b = rnd.randint(3, a - 4), rnd.randint(2, d - 3)
            if min(c, a - c) < 0.3 * a or min(b, d - b) < 0.3 * d:
                continue
            pts = L_pts(a, b, c, d)
        elif kind == "T":
            a, b, s, h = rnd.randint(10, 16), rnd.randint(2, 4), rnd.randint(3, 5), rnd.randint(4, 7)
            o = (a - s) // 2
            pts = T_pts(a, b, o, s, h)
        elif kind == "U":
            a, H = rnd.randint(10, 15), rnd.randint(6, 9)
            p, g = rnd.randint(3, 5), rnd.randint(5, 7)
            h1 = rnd.randint(3, H - 2)
            if p + g > a - 3:
                continue
            pts = U_pts(p, g, h1, a, H)
        else:
            x1 = rnd.randint(3, 5)
            x2 = x1 + rnd.randint(4, 5)
            x3 = x2 + rnd.randint(4, 5)
            y1 = rnd.randint(2, 4)
            y2 = y1 + rnd.randint(2, 4)
            y3 = y2 + rnd.randint(2, 4)
            pts = S_pts(x1, x2, x3, y1, y2, y3)
        pts = flip_pts(pts, rnd.random() < 0.5, rnd.random() < 0.5 and kind != "T")
        sides = sides_of(pts)
        try:
            svg = polygon_svg(pts, ["%d %s" % (v, u) for v in sides], "rectilinear figure with labelled sides")
        except Crowded:
            continue
        return svg, sides
    raise RuntimeError(kind)


def set_story(rnd):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    # rectilinear figures, all sides labelled
    for k, (kind, u) in enumerate([("L", "cm"), ("T", "cm"), ("U", "m"), ("T", "m"), ("L", "m")]):
        svg, sides = rect_fig(rnd, kind, u)
        P = sum(sides)
        e = ("Add all %d sides: %s = %d %s. Tick each side as you add it so you do not miss one."
             % (len(sides), plus(sides), P, u))
        pool = ["%d %s" % (P - min(sides), u), "%d %s" % (P + sides[0], u), "%d %s" % (P, SQ[u]),
                "%d %s" % (P - sides[-1], u)]
        add(fig(svg) + "All the angles are right angles. What is the perimeter of this figure?", "%d %s" % (P, u),
            rot(pool, k), e)
    # L-shapes with two unlabelled sides
    for k, (a, b, c, d, u) in enumerate([(10, 3, 4, 8, "cm"), (12, 5, 7, 9, "m"), (9, 4, 4, 7, "cm")]):
        pts = L_pts(a, b, c, d)
        lab = ["%d %s" % (a, u), "%d %s" % (b, u), "", "", "%d %s" % (c, u), "%d %s" % (d, u)]
        fx, fy = [(False, False), (True, False), (False, True)][k]
        pts = flip_pts(pts, fx, fy)
        svg = polygon_svg(pts, lab, "rectilinear figure with two sides not labelled")
        P = 2 * (a + d)
        x, y = a - c, d - b
        assert P == a + b + x + y + c + d
        e = ("Find the two sides with no label first. The one that goes across: %d − %d = %d %s. "
             "The one that goes up and down: %d − %d = %d %s. Perimeter: %s = %d %s."
             % (a, c, x, u, d, b, y, u, plus([a, b, x, y, c, d]), P, u))
        lsum = a + b + c + d
        pool = rot(["%d %s" % (lsum, u), "%d %s" % (lsum + x, u), "%d %s" % (lsum + y, u)], k) + \
            ["%d %s" % (P, SQ[u])]
        add(fig(svg) + "All the angles are right angles. What is the perimeter of this figure?", "%d %s" % (P, u),
            pool, e)
    # word problems
    add("Mr Tan puts a fence round his rectangular garden. The garden is 9 m long and 6 m wide. "
        "He leaves a gap of 2 m for a gate. How much fence does he need?", "28 m", ["30 m", "15 m", "32 m"],
        "Perimeter: 9 + 6 + 9 + 6 = 30 m. The gate has no fence: 30 − 2 = 28 m.")
    add("Mr Rahman fences a rectangular plot in a community garden. The plot is 8 m long and 5 m wide. "
        "One long side is against a wall and needs no fence. How much fence does he need?", "18 m",
        ["26 m", "21 m", "13 m"],
        "Only 3 sides need fence: 8 + 5 + 5 = 18 m. (26 m would fence all 4 sides.)")
    add("Mdm Wong covers her kitchen floor with square tiles. Each tile is 1 m². The floor is 4 m long and "
        "3 m wide. How many tiles does she need?", "12 tiles", ["14 tiles", "7 tiles", "10 tiles"],
        "Tiles cover the surface, so find the area: 4 × 3 = 12 m². Each tile is 1 m², so she needs 12 tiles. "
        "(14 is the perimeter.)")
    frame = frozenset(rect_cells(6, 4) - rect_cells(4, 2, 1, 1))
    assert len(frame) == 16
    add(fig(one_grid(frame, "border of tiles round a patio on a grid")) +
        "Hafiz lays 1 m² tiles only round the edge of a patio 6 m long and 4 m wide, as shown. "
        "How many tiles does he use?", "16 tiles", ["20 tiles", "24 tiles", "8 tiles"],
        "Top and bottom rows: 6 + 6 = 12 tiles. Each side has 2 more tiles between the corners: 2 + 2 = 4. "
        "12 + 4 = 16 tiles. (20 counts the 4 corner tiles twice. 24 would cover the whole patio.)")
    add("Chloe has 60 cm of ribbon. She sticks ribbon round the edge of a card 15 cm long and 10 cm wide. "
        "How much ribbon is left?", "10 cm", ["35 cm", "50 cm", "110 cm"],
        "Perimeter of the card: 15 + 10 + 15 + 10 = 50 cm. Left: 60 − 50 = 10 cm.")
    add("During Sports Day practice, Ryan runs round a rectangular field 2 times. The field is 80 m long and "
        "50 m wide. How far does he run?", "520 m", ["260 m", "130 m", "4000 m"],
        "Once round: 80 + 50 + 80 + 50 = 260 m. 2 times round: 260 + 260 = 520 m. "
        "(80 × 50 = 4000 is the area of the field, not a distance.)")
    add("A square garden has sides of 7 m. Fencing costs $9 for each metre. How much does it cost to fence "
        "the whole garden?", "$252", ["$63", "$441", "$189"],
        "Perimeter: 4 × 7 = 28 m. Cost: 28 × $9 = $252. ($441 uses the area, 7 × 7 = 49, instead of the perimeter. $63 pays for only one side.)")
    add("Siti’s bedroom floor is 5 m long and 4 m wide. A carpet costs $8 for each square metre. "
        "How much does a carpet for the whole floor cost?", "$160", ["$144", "$72", "$20"],
        "Carpet covers the floor, so find the area: 5 × 4 = 20 m². Cost: 20 × $8 = $160. "
        "($144 uses the perimeter, 18 m, instead of the area.)")
    m1 = model_svg([{"name": "Breadth", "segs": [(1, "4 cm", True)]},
                    {"name": "Length", "segs": [(1, "", True)] * 3, "under": [(0, 3, "?")]}],
                   "bar model: the length is 3 times the breadth")
    add(fig(m1) + "The length of a rectangle is 3 times its breadth. The breadth is 4 cm. "
        "What is the perimeter of the rectangle?", "32 cm", ["16 cm", "28 cm", "48 cm"],
        "1 unit = 4 cm, so the length is 3 units = 3 × 4 = 12 cm. "
        "Perimeter: 12 + 4 + 12 + 4 = 32 cm. (16 cm is only one length and one breadth.)")
    m2 = model_svg([{"name": "", "segs": [(1, "?", True)] + [(1, "", True)] * 3, "over": [(0, 4, "36 cm")]}],
                   "bar model: 4 equal sides make 36 cm")
    add(fig(m2) + "Raju bends a piece of wire 36 cm long to make a square. How long is each side of the square?",
        "9 cm", ["18 cm", "32 cm", "6 cm"],
        "The square has 4 equal sides. 4 units = 36 cm, so 1 unit = 36 ÷ 4 = 9 cm. "
        "(6 × 6 = 36 would be an area, but 36 cm is the perimeter.)")
    m3 = model_svg([{"name": "", "segs": [(40, "used", True), (10, "?", False)], "over": [(0, 50, "50 m")]}],
                   "bar model: 50 m of fencing, some used and some left")
    add(fig(m3) + "Mr Kumar has 50 m of fencing. He fences a rectangular pen 12 m long and 8 m wide. "
        "How much fencing is left?", "10 m", ["30 m", "40 m", "90 m"],
        "Fencing used is the perimeter: 12 + 8 + 12 + 8 = 40 m. Left: 50 − 40 = 10 m. "
        "(30 m comes from using only 12 + 8 = 20 m.)")
    add("Xin Yi makes a rectangle with 12 square tiles: 6 tiles long and 2 tiles wide. Zhi Hao makes a rectangle "
        "with 12 tiles: 4 tiles long and 3 tiles wide. Each tile has sides of 1 cm. "
        "Whose rectangle has the longer perimeter?", "Xin Yi’s, by 2 cm",
        ["Zhi Hao’s, by 2 cm", "They are the same", "Xin Yi’s, by 4 cm"],
        "Both have an area of 12 cm². Xin Yi: 6 + 2 + 6 + 2 = 16 cm. Zhi Hao: 4 + 3 + 4 + 3 = 14 cm. "
        "16 − 14 = 2 cm, so Xin Yi’s is longer by 2 cm.")
    assert len(its) == 20, len(its)
    return {"title": "Rectilinear figures and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    g = frozenset(rect_cells(5, 3))
    assert len(g) == 15 and perim(g) == 16 and border(g) == 12
    Lp = L_pts(10, 3, 4, 8)
    lab = ["10 cm", "3 cm", "", "", "4 cm", "8 cm"]
    assert 2 * (10 + 8) == 36 and 10 + 3 + 6 + 5 + 4 + 8 == 36
    return (
        "<h2>Area: count the squares</h2>"
        "<p><b>Area</b> is the amount of surface a figure covers. We measure it in squares. "
        "If each square is 1 square unit, count the squares inside. "
        "Squares of 1 cm by 1 cm give the area in <b>square centimetres (cm²)</b>. "
        "Big spaces like a floor are measured in <b>square metres (m²)</b>.</p>"
        "<figure class='sn-fig'>" + one_grid(g, "rectangle 5 squares by 3 squares on a grid") +
        "<figcaption>3 rows of 5 squares: 3 × 5 = 15. Area = 15 cm².</figcaption></figure>"
        "<h2>Perimeter: the distance round</h2>"
        "<p><b>Perimeter</b> is the total length of the sides all the way round a figure. "
        "On a grid, count the sides of the small squares along the thick green line, not the squares. "
        "Perimeter is a length, so it is in <b>cm</b> or <b>m</b>.</p>"
        "<p>For the same rectangle: 5 + 3 + 5 + 3 = <b>16 cm</b>. A corner square has 2 sides on the edge, "
        "so count both sides.</p>"
        "<h2>Rectangles and squares</h2>"
        "<p><b>Area of a rectangle = length × breadth.</b> "
        "<b>Perimeter of a rectangle</b> = add all 4 sides (length + breadth + length + breadth). "
        "A square has 4 equal sides.</p>"
        "<figure class='sn-fig'>" + rect_svg(8, 5, "cm", "rectangle 8 cm by 5 cm") +
        "<figcaption>Area: 8 × 5 = 40 cm². Perimeter: 8 + 5 + 8 + 5 = 26 cm.</figcaption></figure>" +
        ex("Example", "A square has sides of 6 m. Find its area and its perimeter.",
           "Area: 6 × 6 = 36 m². Perimeter: 6 + 6 + 6 + 6 = 24 m.", "36 m² and 24 m") +
        "<h2>Perimeter of a rectilinear figure</h2>"
        "<p>A <b>rectilinear figure</b> has only straight sides that meet at right angles. "
        "Find any side with no label first, then add all the sides.</p>"
        "<figure class='sn-fig'>" + polygon_svg(Lp, lab, "rectilinear figure with two sides not labelled") +
        "<figcaption>Missing sides: 10 − 4 = 6 cm and 8 − 3 = 5 cm. "
        "Perimeter: 10 + 3 + 6 + 5 + 4 + 8 = 36 cm.</figcaption></figure>"
        "<h2>Area or perimeter?</h2>"
        "<p>Tiles, carpet and paint cover a surface: find the <b>area</b>. "
        "A fence, a border or a ribbon goes round the edge: find the <b>perimeter</b>.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides for the area (8 + 5 = 13)", "Multiply: 8 × 5 = 40 cm²"],
            ["Multiplying for the perimeter (8 × 5 = 40)", "Add all 4 sides: 8 + 5 + 8 + 5 = 26 cm"],
            ["Adding only 2 sides of a rectangle (8 + 5)", "A rectangle has 4 sides"],
            ["Counting the squares round the edge for the perimeter (12)", "Count the sides of the squares (16)"],
            ["Counting the corner squares twice for a border of tiles", "Count each square only once"],
            ["Writing cm for an area, or cm² for a perimeter", "Area: cm² or m². Perimeter: cm or m"],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 area and perimeter?",
     "a": "Primary 3 students find area by counting squares in square units, cm² and m², find the area of "
          "rectangles and squares, and find the perimeter of rectangles, squares and rectilinear figures."},
    {"q": "How do I explain the difference between area and perimeter to my child?",
     "a": "Area is the surface a shape covers, like the tiles on a floor. Perimeter is the distance round the edge, "
          "like a fence round a garden."},
    {"q": "What is the most common mistake in area and perimeter?",
     "a": "Mixing them up: adding the sides when the question asks for area, or multiplying when it asks for "
          "perimeter. Writing cm for an area instead of cm² is another common slip."},
    {"q": "Is area and perimeter in the MOE Primary 3 syllabus?",
     "a": "Yes. It is in Measurement and Geometry (Area and Volume) of the MOE 2021 Primary Mathematics Syllabus. "
          "Primary 4 then moves on to composite figures made of rectangles and squares."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position) in every set. Picture-label items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(63810)
    sets = [set_count(rnd), set_count_p(rnd), set_rect_p(rnd), set_rect_a(rnd), set_story(rnd)]
    for s in sets:
        rnd.shuffle(s["items"])
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
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "area-and-perimeter", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Area and Perimeter",
        "seo_title": "P3 Area and Perimeter Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Area and perimeter",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 3: Area and Volume",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Concepts of area and perimeter; area in square units, cm² and m²; perimeter of rectilinear "
                         "figures, rectangles and squares; area of rectangles and squares",
        "meta_desc": "Free P3 maths practice: count squares for area, find perimeters, area of rectangles in cm² "
                     "and m², rectilinear figures. 100 questions with answers.",
        "key_big": "Area is the surface inside (cm², m²). Perimeter is the distance round (cm, m).",
        "key_sub": "A rectangle 8 cm by 5 cm: area = 8 × 5 = 40 cm², perimeter = 8 + 5 + 8 + 5 = 26 cm.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "[^']*(grid|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
