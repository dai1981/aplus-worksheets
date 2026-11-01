# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Perimeter (3.MD.D.8)
  python tools/gen_us_math_g3_perimeter.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
NAMES = ["Maya", "Leo", "Ava", "Noah", "Mia", "Eli", "Zoe", "Sam", "Lily", "Ben", "Emma", "Omar", "Kai", "Nora", "Jack", "Ruby"]
UNITS = ["cm", "in", "m", "ft"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    seen = {correct}
    pick = []
    for c in cands:
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead == "0":
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
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def plus(nums):
    return " + ".join(str(n) for n in nums)


def polygon_svg(pts, labels, label="polygon with side lengths"):
    """Polygon (pixel points) with a label outside the middle of each side. A label of '' is not drawn;
    a label containing '?' is drawn in red. The picture is sized to fit the labels."""
    CW, TH = 9.6, 13                                 # approx. width of one character, half text height
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    n = len(pts)
    texts = []
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny                       # point away from the middle of the shape
        hw = CW * len(t) / 2
        off = 7 + abs(nx) * hw + abs(ny) * TH       # far enough that the text box clears the side
        texts.append((mx + nx * off, my + ny * off, hw, t))
    xs = [p[0] for p in pts] + [x - hw for x, y, hw, t in texts] + [x + hw for x, y, hw, t in texts]
    ys = [p[1] for p in pts] + [y - TH for x, y, hw, t in texts] + [y + TH for x, y, hw, t in texts]
    pad = 6
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(max(xs) - ox + pad), int(max(ys) - oy + pad)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.0f,%.0f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for x, y, hw, t in texts:
        col = RED if "?" in t else INK
        s.append("<text x='%.0f' y='%.0f' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x - ox, y - oy + 6, col, t))
    return svg_wrap(W, H, "".join(s), label)


def grid_svg(cells_w, cells_h, filled, cell=28, label="shape on a grid"):
    """Grid of cells_w x cells_h squares; `filled` is a set of (col, row) squares that make the shape.
    The outline of the shape is drawn thick so the sides can be counted."""
    W, H = cells_w * cell + 20, cells_h * cell + 20
    s = []
    for (c, r) in filled:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (10 + c * cell, 10 + r * cell, cell, cell, FILL, GREEN))
    for (c, r) in filled:                            # outer edges only
        x, y = 10 + c * cell, 10 + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                          (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (c + dc, r + dr) not in filled:
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
                         % (x1, y1, x2, y2, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def edges(filled):
    n = 0
    for (c, r) in filled:
        for (dc, dr) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (c + dc, r + dr) not in filled:
                n += 1
    return n


def rect_cells(w, h, c0=0, r0=0):
    return {(c0 + i, r0 + j) for i in range(w) for j in range(h)}


def rect_pts(L, W, max_w=210, max_h=110):
    k = min(max_w / L, max_h / W)
    k = min(k, 26)
    return [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]


# shape templates (pixel points) for "add the sides"
TRI = [[(0, 120), (90, 0), (200, 120)], [(0, 110), (40, 0), (190, 110)], [(0, 0), (180, 40), (40, 120)]]
QUAD = [[(0, 0), (150, 0), (200, 110), (20, 110)], [(30, 0), (170, 20), (200, 120), (0, 100)],
        [(0, 20), (120, 0), (190, 90), (60, 120)]]
PENT = [[(100, 0), (200, 60), (165, 140), (35, 140), (0, 60)], [(0, 50), (90, 0), (190, 30), (170, 130), (20, 130)]]
HOUSE = [(0, 50), (90, 0), (180, 50), (180, 140), (0, 140)]


def reg_pts(n, r=70):
    return [(r + r * math.cos(2 * math.pi * i / n - math.pi / 2), r + r * math.sin(2 * math.pi * i / n - math.pi / 2))
            for i in range(n)]


SHAPE_NAME = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}


def tri_sides(rnd):
    while True:
        a, b, c = rnd.randint(3, 12), rnd.randint(3, 12), rnd.randint(4, 14)
        if a + b > c and a + c > b and b + c > a and len({a, b, c}) >= 2:
            return [a, b, c]


def tri_pts(a, b, c, size=190):
    """Triangle drawn to scale: base c, the other sides a (right) and b (left). Returns points and labels order."""
    k = size / max(a, b, c)
    A, B, C = a * k, b * k, c * k
    x = (B * B - A * A + C * C) / (2 * C)           # apex position along the base
    y = math.sqrt(max(B * B - x * x, 1))
    return [(0, y), (x, 0), (C, y)]                  # sides: left (b), right (a), base (c)


def scaled_sides(pts, rnd, lo=2, hi=15):
    """Integer side lengths in proportion to a template, so the picture matches the numbers."""
    n = len(pts)
    lens = [math.hypot(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]
    for _ in range(50):
        unit = max(lens) / rnd.randint(max(lo + 3, 6), hi)
        sides = [max(lo, int(round(L / unit))) for L in lens]
        if max(sides) <= hi:
            return sides
    return sides


def tri_shape(rnd):
    x, y, c = sorted(tri_sides(rnd))                 # longest side on the bottom looks most natural
    a, b = (x, y) if rnd.random() < 0.5 else (y, x)
    return tri_pts(a, b, c), [b, a, c]


def sum_cands(sides, total):
    """Typical slips: leaving out a side, counting a side twice, regrouping by 10."""
    c = [total - max(sides), total - min(sides), total + min(sides), total + 10, total - 10, total + 1, total - 1]
    return c


# ------------------------------------------------------------ sets
def set_grid(rnd):
    its = []
    rects = [(w, h) for w in range(2, 8) for h in range(2, 6) if w > h and w * h != 2 * (w + h)]
    rnd.shuffle(rects)
    rects = [(w, h) if i % 3 else (h, w) for i, (w, h) in enumerate(rects)]   # some stand up tall
    for w, h in rects[:12]:
        p, a = 2 * (w + h), w * h
        cand = [a, w + h, p - 2, p + 2, p + 4]
        its.append(mcq(fig(grid_svg(w, h, rect_cells(w, h), label="rectangle %d by %d on a grid" % (w, h))) +
                       "Each square is 1 unit on each side. What is the perimeter of the rectangle?",
                       "%d units" % p, ["%d units" % v for v in cand],
                       "Count the unit sides all the way around: %d + %d + %d + %d = %d units. "
                       "(%d is the area, the squares inside.)" % (w, h, w, h, p, a), rnd))
    for s in [2, 3, 4, 5]:
        p = 4 * s
        its.append(mcq(fig(grid_svg(s, s, rect_cells(s, s), label="square %d by %d on a grid" % (s, s))) +
                       "Each square is 1 unit on each side. What is the perimeter of the square?",
                       "%d units" % p, ["%d units" % v for v in [s * s, 2 * s, p + 2, p - 2, p + 4]],
                       "All 4 sides are %d units: %d + %d + %d + %d = %d units." % (s, s, s, s, s, p), rnd))
    done = 0
    while done < 4:                                  # L shapes: count the short step too
        w1 = rnd.randint(1, 3)
        w2 = rnd.randint(w1 + 2, 6)
        h1, h2 = rnd.randint(1, 3), rnd.randint(1, 3)
        cells = rect_cells(w1, h1) | rect_cells(w2, h2, 0, h1)
        p = edges(cells)
        if p == len(cells):                          # area = perimeter would make the hint confusing
            continue
        done += 1
        assert p == 2 * (w2 + h1 + h2)
        its.append(mcq(fig(grid_svg(w2, h1 + h2, cells, label="L-shaped figure on a grid")) +
                       "Each square is 1 unit on each side. What is the perimeter of the shape?",
                       "%d units" % p, ["%d units" % v for v in [len(cells), p - 2, p - 4, p + 2]],
                       "Go around the outside and count every unit side, including the short step: %d units. "
                       "There are %d squares inside, but that is the area." % (p, len(cells)), rnd))
    rnd.shuffle(its)
    return {"title": "Count the units around", "items": its}


def set_add(rnd):
    its = []
    plan = ["tri"] * 5 + ["quad"] * 5 + ["pent"] * 3 + ["house"] + ["reg"] * 6
    regs = [(3, rnd.randint(4, 9)), (4, rnd.randint(5, 9)), (5, rnd.randint(3, 6)), (6, rnd.randint(3, 6)),
            (6, rnd.randint(7, 9)), (8, rnd.randint(2, 4))]
    ri = 0
    for kind in plan:
        u = rnd.choice(UNITS)
        if kind == "reg":
            n, s = regs[ri]
            ri += 1
            p = n * s
            pts = reg_pts(n)
            lab = ["%d %s" % (s, u)] + [""] * (n - 1)
            its.append(mcq(fig(polygon_svg(pts, lab, "%s with equal sides" % SHAPE_NAME[n])) +
                           "This %s has %d sides. All the sides are the same length. What is its perimeter?"
                           % (SHAPE_NAME[n], n),
                           "%d %s" % (p, u),
                           ["%d %s" % (v, u) for v in [(n - 1) * s, n + s, (n + 1) * s, 4 * s, s * s]],
                           "There are %d sides of %d %s. %d × %d = %d %s." % (n, s, u, n, s, p, u), rnd))
            continue
        if kind == "tri":
            pts, sides = tri_shape(rnd)
        elif kind == "quad":
            pts = rnd.choice(QUAD)
            sides = scaled_sides(pts, rnd)
        elif kind == "pent":
            pts = rnd.choice(PENT)
            sides = scaled_sides(pts, rnd, hi=12)
        else:
            pts = HOUSE
            sides = scaled_sides(pts, rnd, hi=12)
        p = sum(sides)
        name = SHAPE_NAME[len(sides)]
        lab = ["%d %s" % (v, u) for v in sides]
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with side lengths" % name)) +
                       "What is the perimeter of this %s?" % name,
                       "%d %s" % (p, u), ["%d %s" % (v, u) for v in sum_cands(sides, p)],
                       "Add every side: %s = %d %s. Check that you used all %d sides." % (plus(sides), p, u, len(sides)), rnd))
    return {"title": "Add the side lengths", "items": its}


def set_rect(rnd):
    its = []
    seen = set()
    while len(its) < 14:
        L, W = rnd.randint(4, 12), rnd.randint(2, 9)
        if L <= W or (L, W) in seen:
            continue
        seen.add((L, W))
        u = UNITS[len(its) % 4]
        p = 2 * (L + W)
        pts = rect_pts(L, W)
        lab = ["%d %s" % (L, u), "", "", "%d %s" % (W, u)]
        q = (fig(polygon_svg(pts, lab, "rectangle %d by %d" % (L, W))) +
             "What is the perimeter of the rectangle?") if len(its) % 2 == 0 else \
            ("A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u))
        its.append(mcq(q, "%d %s" % (p, u),
                       ["%d %s" % (v, u) for v in [L + W, L * W, 2 * L + W, L + 2 * W, p + 2]],
                       "A rectangle has 2 long sides and 2 short sides: %d + %d + %d + %d = %d %s. "
                       "Adding only %d + %d = %d forgets the other two sides." % (L, W, L, W, p, u, L, W, L + W), rnd))
    for s in rnd.sample(range(3, 13), 6):
        u = UNITS[s % 4]
        p = 4 * s
        q = (fig(polygon_svg(rect_pts(s, s), ["%d %s" % (s, u), "", "", ""], "square")) +
             "This is a square. What is its perimeter?") if s % 2 else \
            ("A square has sides that are %d %s long. What is its perimeter?" % (s, u))
        its.append(mcq(q, "%d %s" % (p, u), ["%d %s" % (v, u) for v in [2 * s, s * s, s + 4, 3 * s, p + 4]],
                       "A square has 4 equal sides: %d + %d + %d + %d = %d %s, or 4 × %d = %d." % (s, s, s, s, p, u, s, p), rnd))
    rnd.shuffle(its)
    return {"title": "Rectangles and squares", "items": its}


def set_missing(rnd):
    its = []
    for i in range(10):                              # polygon with one unknown side
        u = rnd.choice(UNITS)
        if i % 2 == 0:
            pts, sides = tri_shape(rnd)
        else:
            pts = rnd.choice(QUAD)
            sides = scaled_sides(pts, rnd, hi=14)
        k = rnd.randrange(len(sides))
        p, x = sum(sides), sides[k]
        known = [v for j, v in enumerate(sides) if j != k]
        lab = ["%d %s" % (v, u) for v in sides]
        lab[k] = "? %s" % u
        name = SHAPE_NAME[len(sides)]
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with one unknown side" % name)) +
                       "The perimeter of this %s is %d %s. What is the missing side length?" % (name, p, u),
                       "%d %s" % (x, u),
                       ["%d %s" % (v, u) for v in [sum(known), p - known[0], x + 2, x - 2, x + 10, x + 1]],
                       "Add the sides you know: %s = %d. Then subtract from the perimeter: %d − %d = %d %s."
                       % (plus(known), sum(known), p, sum(known), x, u), rnd))
    seen = set()
    while len(its) < 16:                             # rectangle: perimeter and length -> width
        L, W = rnd.randint(5, 12), rnd.randint(2, 8)
        if L <= W or (L, W) in seen:
            continue
        seen.add((L, W))
        u = rnd.choice(UNITS)
        p = 2 * (L + W)
        its.append(mcq("A rectangle has a perimeter of %d %s. It is %d %s long. How wide is it?" % (p, u, L, u),
                       "%d %s" % (W, u),
                       ["%d %s" % (v, u) for v in [p - L, p - 2 * L, p // 2, W + 1, W + 2]],
                       "The two lengths use %d + %d = %d %s. That leaves %d − %d = %d %s for the two widths, "
                       "so each width is %d %s." % (L, L, 2 * L, u, p, 2 * L, 2 * W, u, W, u), rnd))
    for s in rnd.sample(range(3, 11), 4):            # square: perimeter -> side
        u = rnd.choice(UNITS)
        p = 4 * s
        its.append(mcq("A square has a perimeter of %d %s. How long is each side?" % (p, u), "%d %s" % (s, u),
                       ["%d %s" % (v, u) for v in [p // 2, p - 4, s + 2, s * s, s + 1]],
                       "A square has 4 equal sides. %d ÷ 4 = %d %s. Check: 4 × %d = %d." % (p, s, u, s, p), rnd))
    rnd.shuffle(its)
    return {"title": "Find the missing side", "items": its}


def set_story(rnd):
    its = []
    names = NAMES[:]
    rnd.shuffle(names)

    def nm():
        n = names.pop(0)
        names.append(n)
        return n

    # 10 word problems
    L, W = 9, 6
    its.append(mcq("%s wants to put a fence around a garden that is %d meters long and %d meters wide. "
                   "How many meters of fence are needed?" % (nm(), L, W), "%d m" % (2 * (L + W)),
                   ["%d m" % v for v in [L + W, L * W, 2 * L + W]],
                   "The fence goes all the way around: %d + %d + %d + %d = %d m." % (L, W, L, W, 2 * (L + W)), rnd))
    s = 8
    its.append(mcq("%s glues ribbon around the edge of a square picture frame. Each side is %d inches. "
                   "How much ribbon is needed?" % (nm(), s), "%d in" % (4 * s),
                   ["%d in" % v for v in [2 * s, s * s, 3 * s]],
                   "4 equal sides: 4 × %d = %d inches." % (s, 4 * s), rnd))
    a, b, c = 120, 150, 90
    its.append(mcq("A park is shaped like a triangle. Its sides are %d m, %d m and %d m. %s walks once around the park. "
                   "How far does %s walk?" % (a, b, c, "Leo", "he"), "%d m" % (a + b + c),
                   ["%d m" % v for v in [a + b, a + b + c - 100, a + b + c + 10]],
                   "Add the 3 sides: %d + %d + %d = %d m." % (a, b, c, a + b + c), rnd))
    L, W = 7, 5
    its.append(mcq("A rug is %d feet long and %d feet wide. Trim is sewn around all of its edges. "
                   "How many feet of trim are used?" % (L, W), "%d ft" % (2 * (L + W)),
                   ["%d ft" % v for v in [L * W, L + W, 2 * L + 2]],
                   "Perimeter = %d + %d + %d + %d = %d ft. (%d sq ft would be the area of the rug.)"
                   % (L, W, L, W, 2 * (L + W), L * W), rnd))
    L, W = 10, 4
    its.append(mcq("A rabbit pen is %d feet long and %d feet wide. One long side is against a wall, so it needs no fence. "
                   "How many feet of fence are needed for the other 3 sides?" % (L, W), "%d ft" % (L + 2 * W),
                   ["%d ft" % v for v in [2 * (L + W), 2 * L + W, L + W]],
                   "Only 3 sides get fence: %d + %d + %d = %d ft." % (L, W, W, L + 2 * W), rnd))
    p, L = 30, 9
    its.append(mcq("%s used %d feet of fence to go around a rectangular dog run. The dog run is %d feet long. "
                   "How wide is it?" % (nm(), p, L), "%d ft" % (p // 2 - L),
                   ["%d ft" % v for v in [p - L, p - 2 * L, p // 2]],
                   "Two lengths: %d + %d = %d. %d − %d = %d for two widths. %d ÷ 2 = %d ft."
                   % (L, L, 2 * L, p, 2 * L, p - 2 * L, p - 2 * L, p // 2 - L), rnd))
    s = 25
    its.append(mcq("A square playground has sides of %d meters. A coach runs around it 2 times. "
                   "How far does the coach run?" % s, "%d m" % (8 * s),
                   ["%d m" % v for v in [4 * s, 2 * s, 6 * s]],
                   "Once around is 4 × %d = %d m. Two times around is %d + %d = %d m." % (s, 4 * s, 4 * s, 4 * s, 8 * s), rnd))
    sides = [6, 6, 4, 4, 5]
    its.append(mcq("A sign has 5 sides: %s inches. What is the perimeter of the sign?" % ", ".join(str(v) for v in sides),
                   "%d in" % sum(sides), ["%d in" % v for v in [sum(sides) - 5, sum(sides) - 6, sum(sides) + 4]],
                   "Add all 5 sides: %s = %d inches." % (plus(sides), sum(sides)), rnd))
    L, W = 30, 20
    its.append(mcq("A classroom table is %d inches long and %d inches wide. %s puts tape around the top edge. "
                   "A roll has 120 inches of tape. Is one roll enough?" % (L, W, nm()),
                   "Yes, the edge is 100 in",
                   ["No, the edge is 600 in", "No, the edge is 150 in", "Yes, the edge is 50 in"],
                   "Perimeter = %d + %d + %d + %d = 100 inches. 100 is less than 120, so one roll is enough. "
                   "(600 is the area. 50 is only one length and one width.)" % (L, W, L, W), rnd))
    p, n = 24, 6
    its.append(mcq("A garden shaped like a hexagon has %d equal sides. The fence around it is %d meters long. "
                   "How long is each side?" % (n, p), "%d m" % (p // n),
                   ["%d m" % v for v in [p - n, p // 2, p // 3]],
                   "%d equal sides share the %d meters: %d ÷ %d = %d m." % (n, p, p, n, p // n), rnd))

    # 5: which rectangle has this perimeter? (wrong ones show the area mix-up and the half-perimeter mix-up)
    for P in [20, 24, 16, 28, 18]:
        half = P // 2
        good = [(a, half - a) for a in range(2, half // 2 + 1) if a != half - a]
        a, b = rnd.choice(good)
        area_like = [(x, P // x) for x in range(2, P) if P % x == 0 and x < P // x and 2 * (x + P // x) != P]
        half_like = [(x, P - x) for x in range(2, P // 2) if 2 * (x + P - x) != P]
        cand = []
        if area_like:
            cand.append("%d by %d" % rnd.choice(area_like))
        cand.append("%d by %d" % rnd.choice(half_like[:4]))
        other = [(x, y) for x in range(2, 9) for y in range(x + 1, 12) if 2 * (x + y) != P and x * y != P]
        rnd.shuffle(other)
        cand += ["%d by %d" % o for o in other]
        its.append(mcq("Each rectangle is measured in units. Which rectangle has a perimeter of %d units?" % P,
                       "%d by %d" % (a, b), cand,
                       "%d + %d + %d + %d = %d. A quick way: length + width must be half of %d, which is %d."
                       % (a, b, a, b, P, P, half), rnd))

    # 5: same area / same perimeter
    pairs_area = [((2, 8), (4, 4)), ((3, 8), (4, 6)), ((2, 9), (3, 6)), ((1, 12), (3, 4))]
    pairs_per = [((3, 7), (5, 5)), ((2, 8), (4, 6))]
    for (a1, b1), (a2, b2) in rnd.sample(pairs_area, 3):
        A, P1, P2 = a1 * b1, 2 * (a1 + b1), 2 * (a2 + b2)
        its.append(mcq("Rectangle A is %d by %d units. Rectangle B is %d by %d units. Both have an area of %d square units. "
                       "Which has the greater perimeter?" % (a1, b1, a2, b2, A),
                       "A (%d units)" % P1, ["B (%d units)" % P2, "They are the same", "B, because it is wider"],
                       "A: %d + %d + %d + %d = %d units. B: %d + %d + %d + %d = %d units. "
                       "Same area does not mean same perimeter. The long, thin rectangle has more edge."
                       % (a1, b1, a1, b1, P1, a2, b2, a2, b2, P2), rnd))
    for (a1, b1), (a2, b2) in pairs_per:
        P, A1, A2 = 2 * (a1 + b1), a1 * b1, a2 * b2
        its.append(mcq("Rectangle A is %d by %d units. Rectangle B is %d by %d units. Both have a perimeter of %d units. "
                       "Which has the greater area?" % (a1, b1, a2, b2, P),
                       "B (%d sq units)" % A2, ["A (%d sq units)" % A1, "They are the same", "A, because it is longer"],
                       "A: %d × %d = %d square units. B: %d × %d = %d square units. Same perimeter does not mean "
                       "same area. The shape closer to a square holds more space." % (a1, b1, A1, a2, b2, A2), rnd))
    return {"title": "Word problems: perimeter and area", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_Q = [8, 7, 10, 6]                       # in proportion to QUAD[0]


def body_html():
    return (
        "<h2>What perimeter means</h2>"
        "<p>Perimeter is the <b>distance all the way around</b> a flat shape. Imagine an ant walking along every edge "
        "until it gets back to where it started. Perimeter is measured in units of length: cm, in, m or ft.</p>"
        "<figure class='sn-fig'>" + grid_svg(5, 3, rect_cells(5, 3), cell=36, label="rectangle 5 by 3 on a grid") +
        "<figcaption>Count the unit sides around the outside: 5 + 3 + 5 + 3 = 16 units.</figcaption></figure>"
        "<h2>Add every side</h2>"
        "<p>For any shape with straight sides, <b>add the lengths of all the sides</b>. Touch each side as you add it "
        "so you do not skip one.</p>"
        "<figure class='sn-fig'>" + polygon_svg(QUAD[0], ["%d cm" % v for v in LESSON_Q], "quadrilateral with side lengths") +
        "<figcaption>%s = %d cm.</figcaption></figure>" % (plus(LESSON_Q), sum(LESSON_Q)) +
        "<h2>Rectangles and squares</h2>"
        "<p>Opposite sides of a rectangle are the same length, so a picture often shows only two numbers. "
        "You still have to add <b>four</b> sides.</p>" +
        table(["Shape", "How to find the perimeter", "Perimeter"], [
            ["Rectangle 6 ft by 4 ft", "6 + 4 + 6 + 4", "20 ft"],
            ["Square with 7 cm sides", "4 × 7", "28 cm"],
            ["Hexagon with 5 in sides", "6 × 5", "30 in"],
        ]) +
        ex("Example", "A rectangle is 8 m long and 3 m wide. What is its perimeter?",
           "8 + 3 + 8 + 3 = 22. Shortcut: 8 + 3 = 11, and 11 + 11 = 22.", "22 m") +
        "<h2>Find a missing side</h2>"
        "<p>If you know the perimeter, add the sides you know and <b>subtract</b> from the perimeter.</p>" +
        ex("Example", "A triangle has a perimeter of 20 cm. Two sides are 6 cm and 8 cm. How long is the third side?",
           "6 + 8 = 14. 20 − 14 = 6.", "6 cm") +
        ex("Example", "A rectangle has a perimeter of 18 ft. It is 5 ft long. How wide is it?",
           "Two lengths: 5 + 5 = 10. 18 − 10 = 8 for the two widths. 8 ÷ 2 = 4.", "4 ft") +
        "<h2>Same area, different perimeter</h2>"
        "<p>Two rectangles can cover the same space but have different edges.</p>" +
        table(["Rectangle", "Area", "Perimeter"], [
            ["1 by 12", "12 sq units", "26 units"],
            ["2 by 6", "12 sq units", "16 units"],
            ["3 by 4", "12 sq units", "14 units"],
        ]) +
        "<p>The long, thin rectangle has the most edge. The one closest to a square has the least.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding only the two numbers shown (6 + 4 = 10)", "A rectangle has 4 sides: 6 + 4 + 6 + 4 = 20"],
            ["Multiplying length × width", "That is the area. Perimeter adds the sides"],
            ["Skipping a side of a shape", "Touch and count each side as you add it"],
            ["Writing sq cm", "Perimeter is a length: cm, not sq cm"],
        ])
    )


FAQ = [
    {"q": "What is perimeter in 3rd grade math?",
     "a": "Perimeter is the distance around the outside of a flat shape. Add the lengths of all the sides. A rectangle that is 6 cm by 4 cm has a perimeter of 6 + 4 + 6 + 4 = 20 cm."},
    {"q": "What is the difference between perimeter and area?",
     "a": "Perimeter is the length around the edge, measured in units such as cm or ft. Area is the space inside, measured in square units such as sq cm or sq ft."},
    {"q": "How do you find a missing side when you know the perimeter?",
     "a": "Add the sides you know, then subtract that sum from the perimeter. For a rectangle, subtract the two known sides and divide what is left by 2."},
    {"q": "Can two rectangles have the same area but different perimeters?",
     "a": "Yes. A 2 by 6 rectangle and a 3 by 4 rectangle both have an area of 12 square units, but their perimeters are 16 and 14 units."},
]


def gen_perimeter():
    rnd = random.Random(37)
    sets = [set_grid(rnd), set_add(rnd), set_rect(rnd), set_missing(rnd), set_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "perimeter", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Perimeter of Polygons",
        "seo_title": "Grade 3 Perimeter Worksheets: Add the Sides, Rectangles, Missing Sides and Word Problems",
        "short_title": "Perimeter",
        "domain": "Measurement and Data",
        "standard_code": "3.MD.D.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/MD/D/8/",
        "standard_text": "Solve real world and mathematical problems involving perimeters of polygons, including finding the perimeter given the side lengths, finding an unknown side length, and exhibiting rectangles with the same perimeter and different areas or with the same area and different perimeters.",
        "meta_desc": "Free Grade 3 perimeter worksheets with pictures: count units around a shape, add side lengths, perimeter of rectangles and squares, find a missing side, and perimeter vs. area word problems. 100 practice questions with answers.",
        "key_big": "Perimeter = the distance around. Add every side.",
        "key_sub": "A rectangle has 4 sides, even when only 2 numbers are shown: length + width + length + width. Perimeter is a length (cm, ft). Area is square units.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_perimeter()
    path = os.path.join(OUT, "perimeter.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
