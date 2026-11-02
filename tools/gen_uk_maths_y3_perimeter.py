# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Perimeter (National Curriculum in England, Year 3 Measurement)
  python3 tools/gen_uk_maths_y3_perimeter.py
Measure the perimeter of simple 2-D shapes (cm and m). No area (that is Year 4).
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
FS = 17


# ------------------------------------------------------------ helpers
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3) * fs * 0.6


def text(x, y, t, fs=FS, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, col, t))


def plus(nums):
    return " + ".join(str(n) for n in nums)


# ------------------------------------------------------------ shapes with labelled sides (drawn to scale)
def polygon_svg(pts, labels, label):
    """Polygon (pixel points). labels[i] belongs to side pts[i] -> pts[i+1] ('' = none, '?' = red).
    Each label sits outside the middle of its side; the viewBox is computed to fit everything."""
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
        off = 7 + abs(nx) * hw + abs(ny) * 11
        cx, cy = (x1 + x2) / 2 + nx * off, (y1 + y2) / 2 + ny * off
        bx = (cx - hw, cy - 11, cx + hw, cy + 11)
        for B in boxes:
            assert not (bx[0] < B[2] + 4 and B[0] < bx[2] + 4 and bx[1] < B[3] and B[1] < bx[3]), (labels, pts)
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


def rect_pts(L, W, max_w=190, max_h=95):
    k = min(max_w / L, max_h / W, 24)
    return [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]


def reg_pts(n, r=55):
    return [(r + r * math.cos(2 * math.pi * i / n - math.pi / 2), r + r * math.sin(2 * math.pi * i / n - math.pi / 2))
            for i in range(n)]


def tri_pts(a, b, c, size=180):
    """Triangle drawn to scale: base c, right side a, left side b. Sides in order: left (b), right (a), base (c)."""
    k = size / max(a, b, c)
    A, B, C = a * k, b * k, c * k
    x = (B * B - A * A + C * C) / (2 * C)
    y = math.sqrt(max(B * B - x * x, 1))
    return [(0, y), (x, 0), (C, y)]


def tri_shape(rnd, lo=3, hi=12):
    while True:
        a, b, c = sorted([rnd.randint(lo, hi), rnd.randint(lo, hi), rnd.randint(lo + 1, hi + 2)])
        if a + b >= c + 3 and len({a, b, c}) >= 2:
            break
    if rnd.random() < 0.5:
        a, b = b, a
    return tri_pts(a, b, c), [b, a, c]


QUAD = [[(0, 0), (150, 0), (200, 100), (20, 100)], [(30, 0), (170, 20), (200, 115), (0, 95)],
        [(0, 20), (120, 0), (190, 90), (60, 115)], [(40, 0), (160, 0), (200, 100), (0, 100)]]
PENT = [[(100, 0), (200, 60), (165, 135), (35, 135), (0, 60)], [(0, 50), (90, 0), (190, 30), (170, 125), (20, 125)]]
HOUSE = [(0, 50), (90, 0), (180, 50), (180, 135), (0, 135)]
SHAPE_NAME = {3: "triangle", 4: "shape with 4 sides", 5: "pentagon", 6: "hexagon", 8: "octagon"}


def scaled_sides(pts, rnd, lo=2, hi=15):
    """Whole-number side lengths in proportion to a template, so the picture matches the numbers."""
    n = len(pts)
    lens = [math.hypot(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]
    for _ in range(100):
        unit = max(lens) / rnd.randint(max(lo + 3, 6), hi)
        sides = [max(lo, int(round(L / unit))) for L in lens]
        if max(sides) <= hi:
            return sides
    raise ValueError(pts)


# ------------------------------------------------------------ centimetre grid
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


def grid_svg(cols, rows, cells, dc, dr, cell=26, label="shape on a centimetre grid"):
    m = 6
    W, H = cols * cell + 2 * m, rows * cell + 2 * m
    fills, lines, g = [], [], []
    for (c, r) in sorted(cells):
        fills.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                     % (m + (c + dc) * cell, m + (r + dr) * cell, cell, cell, FILL))
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    for (c, r) in sorted(cells):
        x, y = m + (c + dc) * cell, m + (r + dr) * cell
        for (ec, er, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                          (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (c + ec, r + er) not in cells:
                lines.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' "
                             "stroke-linecap='round'/>" % (x1, y1, x2, y2, GREEN))
    return svg_wrap(W, H, "".join(fills + g + lines), label)


def one_grid(cells, label, cell=26):
    w, h = size(cells)
    return grid_svg(w + 2, h + 2, cells, 1, 1, cell, label)


def flipcells(cells, rnd):
    w, h = size(cells)
    if rnd.random() < 0.5:
        cells = {(w - 1 - c, r) for c, r in cells}
    if rnd.random() < 0.5:
        cells = {(c, h - 1 - r) for c, r in cells}
    return frozenset(cells)


# ------------------------------------------------------------ set 1: perimeter on a centimetre grid
def set_grid(rnd):
    its = []
    seen = set()
    GQ = "Each square has sides of 1 cm. What is the perimeter of the %s?"
    rects = [(w, h) for w in range(3, 8) for h in range(2, 5) if w > h and w * h != 2 * (w + h)]
    rnd.shuffle(rects)
    for i, (w, h) in enumerate(rects[:8]):
        if i % 3 == 2:
            w, h = h, w
        cells = frozenset(rect_cells(w, h))
        seen.add(cells)
        p = 2 * (w + h)
        pool = ["%d cm" % v for v in [border(cells), w * h, p + 4, w + h]]
        r = i % 4
        pool = pool[r:] + pool[:r]
        e = ("Count the 1 cm sides all the way round: %d + %d + %d + %d = %d cm. "
             "Count the edges, not the squares inside." % (w, h, w, h, p))
        its.append(mcq(fig(one_grid(cells, "rectangle %d cm by %d cm on a centimetre grid" % (w, h))) + GQ % "rectangle",
                       "%d cm" % p, pool, e, rnd))
    for k, s in enumerate([2, 3, 4, 5]):
        cells = frozenset(rect_cells(s, s))
        p = 4 * s
        pool = ["%d cm" % v for v in [s * s, border(cells), 2 * s, p + 4, 3 * s]]
        if k % 2:
            pool = pool[1:] + pool[:1]
        e = "A square has 4 sides the same length. %d + %d + %d + %d = %d cm." % (s, s, s, s, p)
        its.append(mcq(fig(one_grid(cells, "square %d cm by %d cm on a centimetre grid" % (s, s))) + GQ % "square",
                       "%d cm" % p, pool, e, rnd))
    kinds = ["L", "L", "L", "L", "T", "U", "step", "step"]
    for kind in kinds:
        while True:
            if kind == "L":
                w2, h2 = rnd.randint(3, 6), rnd.randint(1, 2)
                w1, h1 = rnd.randint(1, w2 - 2), rnd.randint(1, 2)
                cells = rect_cells(w1, h1) | rect_cells(w2, h2, 0, h1)
            elif kind == "T":
                top, st = rnd.randint(1, 2), rnd.randint(1, 2)
                cells = rect_cells(5, top) | rect_cells(1, st, 2, top)
            elif kind == "U":
                cells = rect_cells(5, 3) - rect_cells(1, 2, 2, 0)
            else:
                w0, w1 = rnd.randint(1, 2), rnd.randint(1, 2)
                h1 = rnd.randint(2, 3) if w0 + w1 < 4 else 2
                cells = rect_cells(w0, h1 + 1) | rect_cells(w1, h1, w0, 1) | rect_cells(1, 1, w0 + w1, h1)
                cells = {(c, r) for c, r in cells}
            cells = flipcells(cells, rnd)
            p, a = perim(cells), len(cells)
            if cells in seen or a == p or border(cells) == p:
                continue
            seen.add(cells)
            break
        pool = ["%d cm" % v for v in [a, border(cells), p - 2, p + 2, p + 4]]
        e = ("Start at one corner and count every 1 cm side round the outside, including the short steps: %d cm. "
             "There are %d squares inside, but we count the edges, not the squares." % (p, a))
        its.append(mcq(fig(one_grid(cells, "shape made of squares on a centimetre grid")) + GQ % "shape",
                       "%d cm" % p, pool, e, rnd))
    rnd.shuffle(its)
    return {"title": "Count the sides on a centimetre grid", "items": its}


# ------------------------------------------------------------ set 2: add the side lengths
def sum_cands(sides, total, u):
    """Real slips: leaving out a side, adding a side twice, a 10 lost or added when exchanging, wrong unit."""
    other = "m" if u == "cm" else "cm"
    return ["%d %s" % (total - sides[-1], u), "%d %s" % (total, other), "%d %s" % (total + sides[0], u),
            "%d %s" % (total - 10, u), "%d %s" % (total + 10, u), "%d %s" % (total - min(sides), u)]


def set_add(rnd):
    its = []
    plan = [("tri", "cm")] * 4 + [("tri", "m")] * 2 + [("quad", "cm")] * 4 + [("quad", "m")] * 2 + \
           [("pent", "cm")] * 2 + [("house", "m")] + [("pent", "m")] + [("text", "cm")] * 2 + [("text", "m")] * 2
    seen = set()
    for kind, u in plan:
        while True:
            if kind == "tri":
                pts, sides = tri_shape(rnd, 3, 12) if u == "cm" else tri_shape(rnd, 5, 20)
            elif kind == "quad":
                pts = rnd.choice(QUAD)
                sides = scaled_sides(pts, rnd, 3, 14 if u == "cm" else 25)
            elif kind == "pent":
                pts = rnd.choice(PENT)
                sides = scaled_sides(pts, rnd, 3, 12 if u == "cm" else 20)
            elif kind == "house":
                pts = HOUSE
                sides = scaled_sides(pts, rnd, 3, 15)
            else:
                pts = None
                n = rnd.choice([3, 4, 5])
                sides = [rnd.randint(4, 15) if u == "cm" else rnd.randint(6, 30) for _ in range(n)]
                if n == 3:
                    a, b, c = sorted(sides)
                    if a + b <= c + 1:
                        continue
            key = tuple(sides) + (u,)
            if key in seen or len(set(sides)) < 2:
                continue
            seen.add(key)
            break
        p = sum(sides)
        name = SHAPE_NAME[len(sides)]
        if pts:
            lab = ["%d %s" % (v, u) for v in sides]
            q = fig(polygon_svg(pts, lab, "%s with side lengths" % name)) + "What is the perimeter of this %s?" % name
        else:
            q = ("A %s has sides of %s and %d %s. What is its perimeter?"
                 % (name, ", ".join("%d %s" % (v, u) for v in sides[:-1]), sides[-1], u))
        e = ("Add every side: %s = %d %s. Touch each side as you add it, so you use all %d sides. "
             "The sides are in %s, so the perimeter is in %s." % (plus(sides), p, u, len(sides), u, u))
        its.append(mcq(q, "%d %s" % (p, u), sum_cands(sides, p, u), e, rnd))
    return {"title": "Add the side lengths", "items": its}


# ------------------------------------------------------------ set 3: rectangles and squares
def set_rect(rnd):
    its = []
    seen = set()
    while len(its) < 12:
        u = "cm" if len(its) % 3 else "m"
        L, W = (rnd.randint(5, 15), rnd.randint(2, 9)) if u == "cm" else (rnd.randint(6, 25), rnd.randint(3, 15))
        if L <= W or L > 2.5 * W + 4 or (L, W) in seen:
            continue
        seen.add((L, W))
        p = 2 * (L + W)
        if len(its) < 8:
            q = (fig(polygon_svg(rect_pts(L, W), ["%d %s" % (L, u), "", "", "%d %s" % (W, u)],
                                 "rectangle %d %s by %d %s" % (L, u, W, u))) +
                 "This is a rectangle. What is its perimeter?")
        else:
            q = "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
        pool = ["%d %s" % (v, u) for v in [L + W, 2 * L + W, L + 2 * W]]
        r = len(its) % 3
        pool = pool[r:] + pool[:r] + ["%d %s" % (p + 2, u)]
        e = ("A rectangle has 4 sides. Opposite sides are the same length, so the sides are %d, %d, %d and %d. "
             "%d + %d + %d + %d = %d %s. Adding only %d + %d = %d leaves out two sides."
             % (L, W, L, W, L, W, L, W, p, u, L, W, L + W))
        its.append(mcq(q, "%d %s" % (p, u), pool, e, rnd))
    for k, (s, u) in enumerate([(4, "cm"), (7, "cm"), (9, "m"), (6, "m"), (8, "cm")]):
        p = 4 * s
        if k < 3:
            q = (fig(polygon_svg(rect_pts(s, s, 95, 95), ["%d %s" % (s, u), "", "", ""], "square with %d %s sides" % (s, u))) +
                 "This is a square. What is its perimeter?")
        else:
            q = "A square has sides of %d %s. What is its perimeter?" % (s, u)
        pool = ["%d %s" % (v, u) for v in [s, 2 * s, 3 * s]]
        if k % 2:
            pool = pool[1:] + pool[:1]
        pool.append("%d %s" % (p + 4, u))
        e = ("A square has 4 sides the same length: %d + %d + %d + %d = %d %s. "
             "You can also use the 4 times table: 4 × %d = %d." % (s, s, s, s, p, u, s, p))
        its.append(mcq(q, "%d %s" % (p, u), pool, e, rnd))
    for n, s, u in [(3, 6, "cm"), (5, 3, "cm"), (6, 4, "m")]:
        p = n * s
        name = SHAPE_NAME[n]
        q = (fig(polygon_svg(reg_pts(n), ["%d %s" % (s, u)] + [""] * (n - 1), "%s with equal sides" % name)) +
             "All the sides of this %s are the same length. What is its perimeter?" % name)
        pool = ["%d %s" % (v, u) for v in [s, (n - 1) * s, (n + 1) * s, n + s]]
        e = "A %s has %d sides. %s = %d %s." % (name, n, plus([s] * n), p, u)
        its.append(mcq(q, "%d %s" % (p, u), pool, e, rnd))
    rnd.shuffle(its)
    return {"title": "Rectangles and squares", "items": its}


# ------------------------------------------------------------ set 4: missing side
def set_missing(rnd):
    its = []
    seen = set()
    i = 0
    while len(its) < 10:
        u = "cm" if i % 3 != 2 else "m"
        if i % 2 == 0:
            pts, sides = tri_shape(rnd, 3, 12)
        else:
            pts = rnd.choice(QUAD)
            sides = scaled_sides(pts, rnd, 3, 14)
        k = rnd.randrange(len(sides))
        key = (tuple(sorted(sides)), sum(sides) - sides[k])
        if key in seen or len(set(sides)) < 2 or sum(sides) in seen:
            continue
        seen.add(key)
        seen.add(sum(sides))
        i += 1
        p, x = sum(sides), sides[k]
        known = [v for j, v in enumerate(sides) if j != k]
        lab = ["%d %s" % (v, u) for v in sides]
        lab[k] = "? %s" % u
        name = SHAPE_NAME[len(sides)]
        cands = ["%d %s" % (v, u) for v in [sum(known), p - known[0], p + sum(known), x + 10, x + 2]]
        if len(its) % 2:
            cands = [cands[1], cands[0]] + cands[2:]
        e = ("Add the sides you know: %s = %d. Then take that away from the perimeter: %d − %d = %d %s. "
             "Check: %s = %d." % (plus(known), sum(known), p, sum(known), x, u, plus(sides), p))
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with one missing side" % name)) +
                       "The perimeter of this %s is %d %s. How long is the missing side?" % (name, p, u),
                       "%d %s" % (x, u), cands, e, rnd))
    while len(its) < 16:
        L, W = rnd.randint(5, 12), rnd.randint(2, 8)
        if L <= W or (L, W) in seen:
            continue
        seen.add((L, W))
        u = "cm" if len(its) % 2 else "m"
        p = 2 * (L + W)
        q = "A rectangle has a perimeter of %d %s. It is %d %s long. How wide is it?" % (p, u, L, u)
        if len(its) % 3 == 0:
            q = (fig(polygon_svg(rect_pts(L, W), ["%d %s" % (L, u), "", "", "? %s" % u],
                                 "rectangle with one missing side")) +
                 "The perimeter of this rectangle is %d %s. How long is the missing side?" % (p, u))
        e = ("The two long sides are %d + %d = %d %s. %d − %d = %d %s is left for the two short sides. "
             "Half of %d is %d, so each short side is %d %s." % (L, L, 2 * L, u, p, 2 * L, 2 * W, u, 2 * W, W, W, u))
        its.append(mcq(q, "%d %s" % (W, u), ["%d %s" % (v, u) for v in [p - L, p - 2 * L, p // 2]], e, rnd))
    for s, u in [(3, "cm"), (5, "m"), (6, "cm"), (8, "cm")]:
        p = 4 * s
        e = "A square has 4 sides the same length. %d ÷ 4 = %d %s. Check: 4 × %d = %d." % (p, s, u, s, p)
        its.append(mcq("A square has a perimeter of %d %s. How long is each side?" % (p, u), "%d %s" % (s, u),
                       ["%d %s" % (v, u) for v in [p // 2, p - 4, 3 * s, p + 4]], e, rnd))
    rnd.shuffle(its)
    return {"title": "Find the missing side", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    L, W = 9, 6
    add("Oliver’s family puts a fence round their garden. The garden is a rectangle %d m long and %d m wide. "
        "How much fence do they need?" % (L, W), "30 m", ["15 m", "24 m", "21 m"],
        "The fence goes along all 4 sides: %d + %d + %d + %d = 30 m. 15 m is only two sides." % (L, W, L, W))
    add("Amelia sticks ribbon round the edge of a birthday card. The card is 15 cm long and 10 cm wide. "
        "How much ribbon does she need?", "50 cm", ["25 cm", "40 cm", "50 m"],
        "Ribbon goes all the way round: 15 + 10 + 15 + 10 = 50 cm. The card is measured in cm, so the answer is in cm.")
    add("The school playground is a rectangle 40 m long and 25 m wide. Harry walks once round the edge. "
        "How far does he walk?", "130 m", ["65 m", "105 m", "120 m"],
        "Once round is the perimeter: 40 + 25 + 40 + 25 = 130 m.")
    add("In PE, Isla runs round the playground 3 times. The playground is a rectangle 20 m long and 10 m wide. "
        "How far does she run?", "180 m", ["60 m", "90 m", "120 m"],
        "One lap: 20 + 10 + 20 + 10 = 60 m. Three laps: 60 + 60 + 60 = 180 m.")
    add("A flower bed is a triangle. Its sides are 4 m, 5 m and 6 m. Mr Patel puts edging all the way round. "
        "How much edging does he use?", "15 m", ["9 m", "11 m", "15 cm"],
        "Add the 3 sides: 4 + 5 + 6 = 15 m.")
    add("A square tablecloth has sides of 90 cm. Grandma sews lace round the edge. How much lace does she need?",
        "360 cm", ["180 cm", "270 cm", "94 cm"],
        "A square has 4 equal sides: 90 + 90 + 90 + 90 = 360 cm. (4 × 9 = 36, so 4 × 90 = 360.)")
    add("A vegetable patch is 8 m long and 5 m wide. A fence goes all the way round, but there is a gate 1 m wide. "
        "How much fence is needed?", "25 m", ["26 m", "27 m", "12 m"],
        "Perimeter: 8 + 5 + 8 + 5 = 26 m. The gate is not fence: 26 − 1 = 25 m.")
    add("A rabbit run is 6 m long and 4 m wide. One long side is against a wall, so it needs no fence. "
        "How much fence is needed for the other sides?", "14 m", ["20 m", "16 m", "10 m"],
        "Only 3 sides need fence: 6 + 4 + 4 = 14 m.")
    add("Mohammed has 50 cm of ribbon. He wants to put it round a square photo frame with sides of 12 cm. "
        "Does he have enough?", "Yes, 2 cm is left", ["No, he is 2 cm short", "Yes, 26 cm is left", "Yes, 38 cm is left"],
        "Perimeter: 12 + 12 + 12 + 12 = 48 cm. 50 − 48 = 2 cm, so there is enough with 2 cm left.")
    add("Freya puts a paper border round a display board. The board is 150 cm long and 100 cm wide. "
        "How long is the border?", "500 cm", ["250 cm", "400 cm", "350 cm"],
        "Border round the edge: 150 + 100 + 150 + 100 = 500 cm.")
    add("Jack makes a rectangle with 30 cm of string. The rectangle is 9 cm long. How wide is it?", "6 cm",
        ["21 cm", "12 cm", "15 cm"],
        "The two long sides use 9 + 9 = 18 cm. 30 − 18 = 12 cm is left for the two short sides. Half of 12 is 6 cm.")
    add("A square sandpit has a perimeter of 12 m. How long is each side?", "3 m", ["6 m", "8 m", "4 m"],
        "A square has 4 equal sides. 12 ÷ 4 = 3 m. Check: 3 + 3 + 3 + 3 = 12 m.")
    add("Poppy walks round a path shaped like a triangle. Its sides are 30 m, 40 m and 50 m. Arjun walks round a square path "
        "with sides of 35 m. Who walks further?", "Arjun, by 20 m",
        ["Poppy, by 20 m", "Arjun, by 5 m", "They walk the same"],
        "Poppy: 30 + 40 + 50 = 120 m. Arjun: 35 + 35 + 35 + 35 = 140 m. 140 − 120 = 20 m, so Arjun walks 20 m further.")
    add("Leo wants to find the perimeter of the school field. Which unit should he use?", "metres (m)",
        ["centimetres (cm)", "millimetres (mm)", "litres (l)"],
        "A field is big, so measure it in metres. Perimeter is a length, so it is never in litres.")
    add("Ava wants to find the perimeter of a bookmark. Which unit should she use?", "centimetres (cm)",
        ["metres (m)", "kilograms (kg)", "kilometres (km)"],
        "A bookmark is small, so measure it in centimetres. Perimeter is a length, so it is not in kilograms.")
    add("A rug is 2 m long and 1 m wide. What is its perimeter?", "6 m", ["6 cm", "3 m", "4 m"],
        "2 + 1 + 2 + 1 = 6 m. The sides are in metres, so the perimeter is in metres, not cm.")
    add("Noah has 1 m of ribbon. He puts ribbon round a card that is 20 cm long and 10 cm wide. "
        "How much ribbon is left?", "40 cm", ["70 cm", "60 cm", "40 m"],
        "1 m = 100 cm. Perimeter of the card: 20 + 10 + 20 + 10 = 60 cm. Left: 100 − 60 = 40 cm.")
    add("A road sign is a pentagon. Each side is 20 cm. Aisha puts tape round the edge. How much tape does she use?",
        "100 cm", ["80 cm", "120 cm", "25 cm"],
        "A pentagon has 5 sides: 20 + 20 + 20 + 20 + 20 = 100 cm.")
    add("A flag is a triangle with 3 equal sides of 25 cm. George sews braid round the edge. How much braid does he use?",
        "75 cm", ["50 cm", "100 cm", "28 cm"],
        "3 sides of 25 cm: 25 + 25 + 25 = 75 cm.")
    add("A square garden has sides of 8 m. Fence panels are 2 m long. How many panels go all the way round?",
        "16 panels", ["32 panels", "4 panels", "8 panels"],
        "Perimeter: 8 + 8 + 8 + 8 = 32 m. Each panel is 2 m: 32 ÷ 2 = 16 panels.")
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Perimeter word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_Q = [8, 7, 10, 6]       # in proportion to QUAD[0]


def body_html():
    grid = frozenset(rect_cells(5, 3))
    assert perim(grid) == 16 and border(grid) == 12
    return (
        "<h2>What is perimeter?</h2>"
        "<p>The <b>perimeter</b> is the distance <b>all the way round</b> the edge of a flat shape. "
        "Imagine an ant walking round the edge until it gets back to the start. "
        "Perimeter is a length, so we measure it in cm or m.</p>"
        "<h2>Perimeter on a centimetre grid</h2>"
        "<p>Each square has sides of 1 cm. Count the <b>sides of the squares</b> round the edge, not the squares.</p>"
        "<figure class='sn-fig'>" + one_grid(grid, "rectangle 5 cm by 3 cm on a centimetre grid") +
        "<figcaption>5 + 3 + 5 + 3 = 16 cm. A corner square has 2 sides on the edge, so count both.</figcaption></figure>"
        "<h2>Add all the sides</h2>"
        "<p>When the sides are labelled, <b>add every side</b>. Touch each side as you add it, so you do not miss one.</p>"
        "<figure class='sn-fig'>" + polygon_svg(QUAD[0], ["%d cm" % v for v in LESSON_Q], "shape with 4 labelled sides") +
        "<figcaption>%s = %d cm.</figcaption></figure>" % (plus(LESSON_Q), sum(LESSON_Q)) +
        "<h2>Rectangles and squares</h2>"
        "<p>Opposite sides of a rectangle are the same length. A picture may show only 2 numbers, "
        "but a rectangle has <b>4 sides</b>. A square has 4 sides the same length.</p>"
        "<figure class='sn-fig'>" + polygon_svg(rect_pts(9, 4), ["9 cm", "", "", "4 cm"], "rectangle 9 cm by 4 cm") +
        "<figcaption>9 + 4 + 9 + 4 = 26 cm. Not 9 + 4 = 13: that is only 2 sides.</figcaption></figure>" +
        ex("Example", "A square has sides of 6 m. What is its perimeter?",
           "6 + 6 + 6 + 6 = 24. Or use the 4 times table: 4 × 6 = 24.", "24 m") +
        "<h2>Find a missing side</h2>"
        "<p>If you know the perimeter, add the sides you know. Then <b>take that away</b> from the perimeter.</p>" +
        ex("Example", "A triangle has a perimeter of 20 cm. Two sides are 6 cm and 8 cm. How long is the third side?",
           "6 + 8 = 14. 20 − 14 = 6.", "6 cm") +
        ex("Example", "A rectangle has a perimeter of 18 m. It is 5 m long. How wide is it?",
           "Two long sides: 5 + 5 = 10. 18 − 10 = 8 for the two short sides. Half of 8 is 4.", "4 m") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the squares inside (15)", "Count the 1 cm sides round the edge (16 cm)"],
            ["Counting the squares round the edge (12)", "A corner square has 2 sides on the edge"],
            ["Adding only the 2 numbers shown (9 + 4 = 13)", "A rectangle has 4 sides: 9 + 4 + 9 + 4 = 26"],
            ["Counting a corner twice when counting dots", "Count the sides between the dots, not the dots"],
            ["Writing m when the sides are in cm", "Use the same unit as the sides"],
        ])
    )


FAQ = [
    {"q": "What is perimeter in Year 3 maths?",
     "a": "Perimeter is the distance all the way round the edge of a flat shape. Year 3 children find it by adding the lengths of all the sides, in centimetres or metres."},
    {"q": "How do you find the perimeter of a rectangle?",
     "a": "Add all 4 sides. Opposite sides are the same, so a rectangle 9 cm by 4 cm has a perimeter of 9 + 4 + 9 + 4 = 26 cm."},
    {"q": "Do Year 3 children learn area?",
     "a": "No. In the National Curriculum, Year 3 measures perimeter. Area by counting squares starts in Year 4."},
    {"q": "How do you find perimeter on a squared grid?",
     "a": "If each square has sides of 1 cm, count the sides of the squares round the outside of the shape. Do not count the squares inside."},
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
    rnd = random.Random(3309)
    sets = [set_grid(rnd), set_add(rnd), set_rect(rnd), set_missing(rnd), set_story(rnd)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(k) == 5 for k in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "perimeter", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Perimeter",
        "seo_title": "Year 3 Perimeter Worksheets: Squared Grids, Rectangles, Missing Sides and Word Problems",
        "short_title": "Perimeter",
        "domain": "Measurement",
        "standard_code": "Year 3: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Measure the perimeter of simple 2-D shapes.",
        "meta_desc": "Free Year 3 perimeter worksheets for the National Curriculum: count round shapes on a centimetre grid, add side lengths in cm and m, rectangles and squares, missing sides and word problems. 100 questions with an answer key.",
        "key_big": "Perimeter is the distance all the way round a shape. Add every side.",
        "key_sub": "A rectangle has 4 sides, even when only 2 numbers are shown. On a grid, count the 1 cm sides round the edge, not the squares. Keep the same unit as the sides: cm or m.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*grid")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
