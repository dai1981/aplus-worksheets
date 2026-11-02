# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: Perimeter (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g4_perimeter.py
Grid shapes are drawn from sets of unit squares; the perimeter is counted from the outside edges in code.
Polygons and composite shapes are drawn to scale from their side lengths, and every answer is parsed
back to millimetres and checked. Canadian English (centimetre, metre, colour), metric units only.
4-digit numbers have no separator; 5 or more digits use a no-break space (13 500).
HTML attributes use single quotes (no backslashes in the JSON).
Wrong answers come from real mistakes: counting the squares inside (area), leaving out a side,
adding only the two numbers shown on a rectangle, using 4 sides for every shape, adding instead of
multiplying, forgetting to halve, and mixing cm and m (2 m + 40 cm = 42).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GRIDLINE = "#c9d3cc"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "


# ------------------------------------------------------------ units and checking
UNIT = {"mm": 1, "cm": 10, "m": 1000, "km": 1000000}
TOK = re.compile(r"([\d" + NBSP + r"]+)\s*(km|mm|cm|m)(?![a-zA-Z])")


def parse(s):
    """'1250 m' -> 1250000 (mm). None if the string is not a plain length."""
    s = s.strip()
    pos, tot, hit = 0, 0, False
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        tot += int(mt.group(1).replace(NBSP, "")) * UNIT[mt.group(2)]
        pos, hit = mt.end(), True
    if not hit or s[pos:].strip():
        return None
    return tot


def n(v):
    """BC style: 4 digits plain (1250), 5 or more digits grouped with a no-break space (13 500)."""
    if v < 10000:
        return str(v)
    return "{:,}".format(v).replace(",", NBSP)


def L(v, u):
    return "%s %s" % (n(v), u)


def plus(nums):
    return " + ".join(n(x) for x in nums)


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, want=None):
    """Correct answer + the first 3 usable distractors from cands (no repeats, no equal lengths,
    nothing zero or negative). want = value in mm checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == want, (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc} if pc is not None else set()
    pick = []
    for x in cands:
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        pv = parse(x)
        if pv is not None:
            if pv in vals:
                continue
            vals.add(pv)
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def fixed(q, choices, a, e):
    """Choices are picture labels (A, B, ...): keep this order; the answer position is fixed."""
    assert len(set(choices)) == 4
    return {"q": q, "c": list(choices), "a": a, "e": e, "fix": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.get("fix"):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ grid figures
def edges(cells):
    k = 0
    for (cc, r) in cells:
        for (dc, dr) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (cc + dc, r + dr) not in cells:
                k += 1
    return k


def rect_cells(w, h, c0=0, r0=0):
    return {(c0 + i, r0 + j) for i in range(w) for j in range(h)}


def grid_body(cells, x0, y0, cw, ch, cell):
    """Grid paper of cw x ch squares at (x0, y0); the shape's squares are filled, its outline is thick."""
    s = []
    for i in range(cw + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 + i * cell, y0, x0 + i * cell, y0 + ch * cell, GRIDLINE))
    for j in range(ch + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0, y0 + j * cell, x0 + cw * cell, y0 + j * cell, GRIDLINE))
    for (cc, r) in sorted(cells):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x0 + cc * cell, y0 + r * cell, cell, cell, FILL, "#9cc5aa"))
    for (cc, r) in sorted(cells):
        x, y = x0 + cc * cell, y0 + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                          (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (cc + dc, r + dr) not in cells:
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
                         % (x1, y1, x2, y2, GREEN))
    return "".join(s)


def bbox(cells):
    return max(c for c, r in cells) + 1, max(r for c, r in cells) + 1


def grid_svg(cells, cell=26, label="shape on a grid"):
    """Shape on grid paper with one empty square all around it."""
    cw, ch = bbox(cells)
    sh = {(c + 1, r + 1) for c, r in cells}
    W, H = (cw + 2) * cell + 12, (ch + 2) * cell + 12
    return svg_wrap(W, H, grid_body(sh, 6, 6, cw + 2, ch + 2, cell), label)


def grid_pair_svg(a, b, cell=24, label="grid shapes A and B"):
    """Two shapes on grid paper, labelled A and B, side by side."""
    (aw, ah), (bw, bh) = bbox(a), bbox(b)
    ch = max(ah, bh)
    gap = 40
    xa, xb = 6, 6 + aw * cell + gap
    y0 = 30
    W = xb + bw * cell + 6
    H = y0 + ch * cell + 6
    body = (text(xa + aw * cell / 2, 22, "A", 20) + text(xb + bw * cell / 2, 22, "B", 20) +
            grid_body(a, xa, y0, aw, ah, cell) + grid_body(b, xb, y0, bw, bh, cell))
    return svg_wrap(W, H, body, label)


# ------------------------------------------------------------ polygon figures
def inside(pt, pts):
    x, y = pt
    k = False
    m = len(pts)
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                k = not k
    return k


def polygon_svg(pts, labels, label="polygon with side lengths", ticks=False):
    """Polygon (pixel points) with a label outside the middle of each side. A label of '' is not drawn;
    a label containing '?' is red. Works for shapes with inside corners (outside is tested point by point).
    ticks=True draws a small mark on every side to show the sides are equal."""
    CW, TH = 9.6, 13
    m = len(pts)
    texts, marks = [], []
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % m]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        Ln = math.hypot(dx, dy)
        nx, ny = dy / Ln, -dx / Ln
        if inside((mx + nx * 2, my + ny * 2), pts):
            nx, ny = -nx, -ny
        if ticks:
            marks.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                         % (mx - nx * 7, my - ny * 7, mx + nx * 7, my + ny * 7, INK))
        t = labels[i]
        if not t:
            continue
        hw = CW * len(t) / 2
        off = 8 + abs(nx) * hw + abs(ny) * TH + (6 if ticks else 0)
        texts.append((mx + nx * off, my + ny * off, hw, t))
    xs = [p[0] for p in pts] + [x - hw for x, y, hw, t in texts] + [x + hw for x, y, hw, t in texts]
    ys = [p[1] for p in pts] + [y - TH for x, y, hw, t in texts] + [y + TH for x, y, hw, t in texts]
    pad = 8
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(max(xs) - ox + pad), int(max(ys) - oy + pad)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for mk in marks:
        s.append(re.sub(r"([xy][12])='([\d.\-]+)'",
                        lambda mt: "%s='%.1f'" % (mt.group(1), float(mt.group(2)) - (ox if mt.group(1)[0] == "x" else oy)),
                        mk))
    for x, y, hw, t in texts:
        s.append(text(x - ox, y - oy + 6, t, 17, col=RED if "?" in t else INK))
    return svg_wrap(W, H, "".join(s), label)


def rect_pts(Lg, Wd, max_w=190, max_h=95):
    k = min(max_w / Lg, max_h / Wd)
    return [(0, 0), (Lg * k, 0), (Lg * k, Wd * k), (0, Wd * k)]


def rect_svg(Lg, Wd, u, wlab=None, label=None):
    """Rectangle drawn to scale, length on top and width on the left."""
    lab = [L(Lg, u), "", "", wlab if wlab is not None else L(Wd, u)]
    return polygon_svg(rect_pts(Lg, Wd), lab, label or "rectangle %d by %d" % (Lg, Wd))


def reg_pts(k, r=58):
    return [(r + r * math.cos(2 * math.pi * i / k - math.pi / 2 - (math.pi / k if k % 2 == 0 else 0)),
             r + r * math.sin(2 * math.pi * i / k - math.pi / 2 - (math.pi / k if k % 2 == 0 else 0)))
            for i in range(k)]


REG_NAME = {3: "equilateral triangle", 4: "square", 5: "regular pentagon", 6: "regular hexagon", 8: "regular octagon"}


def reg_svg(k, lab):
    return polygon_svg(reg_pts(k), [lab] + [""] * (k - 1), "%s with equal sides" % REG_NAME[k], ticks=True)


def tri_pts(a, b, cc, size=180):
    """Triangle drawn to scale: base cc, right side a, left side b. Side order: left (b), right (a), base (cc)."""
    k = size / max(a, b, cc)
    A, B, C = a * k, b * k, cc * k
    x = (B * B - A * A + C * C) / (2 * C)
    y = math.sqrt(max(B * B - x * x, 1))
    return [(0, y), (x, 0), (C, y)]


def tri_shape(rnd, lo=4, hi=15):
    while True:
        a, b, cc = rnd.randint(lo, hi), rnd.randint(lo, hi), rnd.randint(lo + 1, hi + 2)
        x, y, z = sorted([a, b, cc])
        if x + y > z + 2 and len({a, b, cc}) == 3:
            break
    a, b = (x, y) if rnd.random() < 0.5 else (y, x)
    return tri_pts(a, b, z), [b, a, z]


QUAD = [[(0, 0), (150, 0), (200, 110), (20, 110)], [(30, 0), (170, 20), (200, 120), (0, 100)],
        [(0, 20), (120, 0), (190, 90), (60, 120)]]


def scaled_sides(pts, rnd, lo=3, hi=18):
    """Whole-number side lengths in proportion to a template, so the picture matches the numbers."""
    k = len(pts)
    lens = [math.hypot(pts[(i + 1) % k][0] - pts[i][0], pts[(i + 1) % k][1] - pts[i][1]) for i in range(k)]
    for _ in range(50):
        unit = max(lens) / rnd.randint(max(lo + 4, 8), hi)
        sides = [max(lo, int(round(v / unit))) for v in lens]
        if max(sides) <= hi and len(set(sides)) >= 3:
            return sides
    return sides


def ortho_pts(units, k=None, max_w=230, max_h=150):
    """Composite shape with square corners: vertices in whole units, scaled to pixels."""
    W = max(x for x, y in units)
    H = max(y for x, y in units)
    k = k or min(max_w / W, max_h / H)
    return [(x * k, y * k) for x, y in units]


def ortho_sides(units):
    m = len(units)
    out = []
    for i in range(m):
        (x1, y1), (x2, y2) = units[i], units[(i + 1) % m]
        assert x1 == x2 or y1 == y2
        out.append(abs(x2 - x1) + abs(y2 - y1))
    return out


def ortho_area(units):
    m = len(units)
    a2 = sum(units[i][0] * units[(i + 1) % m][1] - units[(i + 1) % m][0] * units[i][1] for i in range(m))
    return abs(a2) // 2


# ============================================================ set 1: perimeter on a grid
def set_grid(rnd):
    its = []
    its.append(mcq("What is <b>perimeter</b>?", "the distance all the way around a shape",
                   ["the number of squares inside a shape", "the length of the longest side", "the number of corners"],
                   "Perimeter is the distance around the outside edge. The squares inside show the area, "
                   "not the perimeter."))
    for w, h in [(4, 3), (6, 2), (5, 5), (2, 5), (7, 3), (8, 3)]:
        cells = rect_cells(w, h)
        p, a = edges(cells), w * h
        assert p == 2 * (w + h) and p != a
        shape = "square" if w == h else "rectangle"
        its.append(mcq(fig(grid_svg(cells, label="%s %d by %d on a grid" % (shape, w, h))) +
                       "Each small square is 1 cm on each side. What is the perimeter of the %s?" % shape,
                       L(p, "cm"), [L(v, "cm") for v in [a, w + h, p - h, p - w, p + 4]],
                       "Count the 1 cm sides all the way around: %d + %d + %d + %d = <b>%d cm</b>. "
                       "There are %d squares inside. That is the area, not the perimeter." % (w, h, w, h, p, a),
                       want=p * 10))
    shapes = [
        ("L-shaped figure", rect_cells(2, 4) | rect_cells(3, 2, 2, 2)),
        ("T-shaped figure", rect_cells(5, 2) | rect_cells(1, 3, 2, 2)),
        ("plus-shaped figure", rect_cells(3, 1, 0, 1) | rect_cells(1, 3, 1, 0)),
        ("U-shaped figure", rect_cells(5, 3) - {(2, 0), (2, 1)}),
        ("staircase figure", {(c, r) for r in range(4) for c in range(r + 1)}),
        ("zigzag figure", rect_cells(3, 2) | rect_cells(3, 2, 2, 2)),
    ]
    for name, cells in shapes:
        p, a = edges(cells), len(cells)
        assert p != a, name
        cw, ch = bbox(cells)
        extra = ""
        if p != 2 * (cw + ch):
            extra = " Do not forget the sides that go in and out."
        else:
            extra = " Count the short steps too."
        its.append(mcq(fig(grid_svg(cells, label="%s on a grid" % name)) +
                       "Each small square is 1 cm on each side. What is the perimeter of the shape?",
                       L(p, "cm"), [L(v, "cm") for v in [a, p - 2, p - 4, p + 2]],
                       "Start at one corner and go around the outside, counting every 1 cm side: <b>%d cm</b>.%s "
                       "The %d squares inside are the area." % (p, extra, a), want=p * 10))
    # squares that are 2 cm or 1 m on each side
    cells = rect_cells(4, 2)
    p = edges(cells)
    its.append(mcq(fig(grid_svg(cells, label="rectangle 4 by 2 on a grid")) +
                   "Each small square is <b>2 cm</b> on each side. What is the perimeter of the rectangle?",
                   L(2 * p, "cm"), [L(v, "cm") for v in [p, len(cells), 2 * len(cells) + 2, 2 * p - 4]],
                   "There are %d small sides around the outside. Each one is 2 cm: %d × 2 = <b>%d cm</b>. "
                   "%d cm forgets that each side is 2 cm, not 1 cm." % (p, p, 2 * p, p), want=2 * p * 10))
    cells = rect_cells(3, 3) - {(2, 0)}
    p = edges(cells)
    assert p == 12
    its.append(mcq(fig(grid_svg(cells, label="L-shaped figure on a grid")) +
                   "Each small square is <b>2 m</b> on each side. What is the perimeter of the shape?",
                   L(2 * p, "m"), [L(v, "m") for v in [p, len(cells), 2 * p - 4, 2 * p + 4]],
                   "Count the small sides around the outside: %d. Each one is 2 m: %d × 2 = <b>%d m</b>."
                   % (p, p, 2 * p), want=2 * p * 1000))
    cells = rect_cells(6, 2) | rect_cells(2, 2, 0, 2)
    p, a = edges(cells), len(cells)
    its.append(mcq(fig(grid_svg(cells, label="L-shaped garden plan on a grid")) +
                   "This is a plan of a school garden. Each square is 1 m on each side. How long is the fence "
                   "all the way around it?", L(p, "m"), [L(v, "m") for v in [a, p - 2, p - 4, p + 2]],
                   "Count the 1 m sides around the outside: <b>%d m</b>. %d is the number of squares inside, "
                   "which is the area of the garden." % (p, a), want=p * 1000))
    # compare two shapes (labels A and B keep their order)
    A, B = rect_cells(4, 2), rect_cells(3, 3) - {(2, 0)}
    assert edges(A) == edges(B) == 12 and len(A) == len(B) == 8
    its.append(fixed(fig(grid_pair_svg(A, B, label="grid shapes A and B with the same area")) +
                     "Which shape has the <b>longer perimeter</b>?",
                     ["A", "B", "They are the same", "You can’t tell"], 2,
                     "A: 4 + 2 + 4 + 2 = 12 units. B: count around the outside, including the step: 12 units. "
                     "<b>They are the same.</b>"))
    A, B = rect_cells(6, 1), rect_cells(3, 3)
    assert edges(A) == 14 and edges(B) == 12
    its.append(fixed(fig(grid_pair_svg(A, B, label="grid shapes A and B")) +
                     "Which shape has the <b>longer perimeter</b>?",
                     ["A", "B", "They are the same", "You can’t tell"], 0,
                     "A: 6 + 1 + 6 + 1 = 14 units. B: 3 + 3 + 3 + 3 = 12 units. So <b>A</b> is longer around, "
                     "even though B has more squares inside (9 vs 6). More squares means more area, "
                     "not always more perimeter."))
    # all sides labelled: add them
    pts, sides = tri_shape(rnd)
    p = sum(sides)
    its.append(mcq(fig(polygon_svg(pts, [L(v, "cm") for v in sides], "triangle with side lengths")) +
                   "What is the perimeter of this triangle?", L(p, "cm"),
                   [L(v, "cm") for v in [p - min(sides), p - max(sides), p + min(sides), p + 10]],
                   "Add all 3 sides: %s = <b>%d cm</b>." % (plus(sides), p), want=p * 10))
    pts = QUAD[1]
    sides = scaled_sides(pts, rnd)
    p = sum(sides)
    its.append(mcq(fig(polygon_svg(pts, [L(v, "m") for v in sides], "quadrilateral with side lengths")) +
                   "What is the perimeter of this shape?", L(p, "m"),
                   [L(v, "m") for v in [p - min(sides), p - max(sides), p + min(sides), p + 10]],
                   "Add all 4 sides: %s = <b>%d m</b>. Touch each side as you add it so you do not skip one."
                   % (plus(sides), p), want=p * 1000))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter on a grid: count and add the sides", "items": its}


# ============================================================ set 2: regular polygons
def set_regular():
    its = []
    for k, s, u in [(3, 8, "cm"), (4, 9, "cm"), (5, 6, "cm"), (6, 7, "cm"), (8, 5, "cm"), (3, 15, "m"),
                    (4, 25, "cm"), (5, 12, "m"), (6, 20, "mm"), (8, 11, "cm"), (6, 35, "cm"), (5, 45, "m")]:
        p = k * s
        cands = [s, (k - 1) * s]
        if k != 4:
            cands.append(4 * s)
        else:
            cands.append(s * s)
        cands += [k + s, 2 * s, (k + 1) * s]
        e = ("A%s %s has %d equal sides. Multiply: %d × %d = <b>%s %s</b>."
             % ("n" if REG_NAME[k][0] in "aeiou" else "", REG_NAME[k], k, k, s, n(p), u))
        if k != 4:
            e += " Not every shape has 4 sides: %d × 4 = %d is wrong here." % (s, 4 * s)
        else:
            e += " %d × %d = %d would be the area, not the perimeter." % (s, s, s * s)
        its.append(mcq(fig(reg_svg(k, L(s, u))) +
                       "All the sides of this %s are the same length. What is its perimeter?" % REG_NAME[k],
                       L(p, u), [L(v, u) for v in cands], e, want=p * UNIT[u]))
    its.append(mcq("What is a <b>regular</b> polygon?", "All its sides and all its angles are equal.",
                   ["It always has 4 sides.", "All its sides are different lengths.", "It has one curved side."],
                   "A regular polygon has all sides the same length and all angles the same size, like a square "
                   "or a regular hexagon. So its perimeter = side length × number of sides."))
    its.append(mcq("A regular hexagon has sides of 9 cm. Which number sentence gives its perimeter?",
                   "6 × 9 = 54", ["4 × 9 = 36", "6 + 9 = 15", "9 × 9 = 81"],
                   "A hexagon has 6 sides, each 9 cm. Add 9 six times, or multiply: <b>6 × 9 = 54</b> cm."))
    its.append(mcq("A sign is shaped like a regular octagon. Each side is 30 cm. What is the perimeter of the sign?",
                   "240 cm", ["120 cm", "210 cm", "38 cm", "180 cm"],
                   "An octagon has 8 sides: 8 × 30 = <b>240 cm</b>. 120 cm uses only 4 sides, and 210 cm leaves out one side.",
                   want=2400))
    its.append(mcq("A square floor tile has sides of 15 cm. What is the perimeter of the tile?",
                   "60 cm", ["30 cm", "45 cm", "225 cm"],
                   "A square has 4 equal sides: 4 × 15 = <b>60 cm</b>. 225 is 15 × 15, the area.", want=600))
    its.append(mcq("An equilateral triangle has sides of <b>1 m</b>. What is its perimeter in centimetres?",
                   "300 cm", ["3 cm", "30 cm", "103 cm"],
                   "1 m = 100 cm. 3 sides: 3 × 100 = <b>300 cm</b>. 3 cm forgets to change metres to centimetres.",
                   want=3000))
    its.append(mcq("A regular hexagon has sides of <b>50 cm</b>. What is its perimeter in metres?",
                   "3 m", ["300 m", "30 m", "2 m"],
                   "6 × 50 = 300 cm. 100 cm = 1 m, so 300 cm = <b>3 m</b>. 300 m mixes up cm and m.", want=3000))
    assert 4 * 10 == 5 * 8
    its.append(mcq("Which has the longer perimeter: a square with 10 cm sides or a regular pentagon with 8 cm sides?",
                   "They are the same, 40 cm", ["The square, 40 cm", "The pentagon, 48 cm", "The square, 100 cm"],
                   "Square: 4 × 10 = 40 cm. Pentagon: 5 × 8 = 40 cm. <b>They are the same.</b> "
                   "100 is the area of the square, and 48 uses 6 sides for the pentagon."))
    its.append(mcq("A regular hexagon and a square both have 6 cm sides. How much longer is the hexagon’s perimeter?",
                   "12 cm", ["2 cm", "6 cm", "36 cm"],
                   "Hexagon: 6 × 6 = 36 cm. Square: 4 × 6 = 24 cm. 36 − 24 = <b>12 cm</b>. "
                   "The hexagon has 2 more sides, and 2 × 6 = 12.", want=120))
    assert len(its) == 20, len(its)
    return {"title": "Regular polygons: side length × number of sides", "items": its}


# ============================================================ set 3: rectangles
def set_rect():
    its = []
    for Lg, Wd, u in [(9, 4, "cm"), (12, 7, "m"), (15, 6, "cm"), (20, 9, "cm"), (25, 14, "m"),
                      (36, 18, "cm"), (48, 25, "m"), (120, 65, "m")]:
        p = 2 * Lg + 2 * Wd
        cands = [Lg + Wd, 2 * Lg + Wd, Lg + 2 * Wd]
        if Lg * Wd < 2000:
            cands.insert(1, Lg * Wd)
        cands.append(p + 10)
        e = ("A rectangle has 2 lengths and 2 widths: 2 × %d + 2 × %d = %d + %d = <b>%s %s</b>. "
             "%d + %d = %d is only two of the four sides." % (Lg, Wd, 2 * Lg, 2 * Wd, n(p), u, Lg, Wd, Lg + Wd))
        its.append(mcq(fig(rect_svg(Lg, Wd, u)) + "What is the perimeter of the rectangle?",
                       L(p, u), [L(v, u) for v in cands], e, want=p * UNIT[u]))
    for s, u in [(11, "cm"), (16, "m")]:
        p = 4 * s
        its.append(mcq(fig(polygon_svg(rect_pts(s, s), [L(s, u), "", "", ""], "square")) +
                       "This is a square. What is its perimeter?", L(p, u),
                       [L(v, u) for v in [s, 2 * s, s * s, 3 * s]],
                       "All 4 sides of a square are equal: 4 × %d = <b>%d %s</b>." % (s, p, u), want=p * UNIT[u]))
    its.append(mcq("Which gives the perimeter of a rectangle that is 8 cm long and 5 cm wide?",
                   "2 × 8 + 2 × 5", ["8 × 5", "8 + 5", "2 × 8 + 5"],
                   "There are 2 lengths of 8 cm and 2 widths of 5 cm: <b>2 × 8 + 2 × 5</b> = 16 + 10 = 26 cm. "
                   "8 × 5 is the area."))
    its.append(mcq("Liam says the perimeter of a rectangle 10 cm long and 3 cm wide is 13 cm. What mistake did he make?",
                   "He added only 2 of the 4 sides.",
                   ["He found the area.", "He used the wrong unit.", "He counted one side twice."],
                   "10 + 3 = 13 uses one length and one width. The rectangle has 4 sides: "
                   "10 + 3 + 10 + 3 = 26 cm."))
    its.append(mcq("Ava says a rectangle 6 m long and 4 m wide has a perimeter of 24 m. What did she find?",
                   "The area, not the perimeter.",
                   ["Only two of the sides.", "The correct perimeter.", "Three of the sides."],
                   "6 × 4 = 24 is the number of square metres inside: the area. The perimeter is "
                   "6 + 4 + 6 + 4 = 20 m."))
    # mixing cm and m (or mm and cm)
    for Lm, Wc, big, small, mul in [(2, 40, "m", "cm", 100), (3, 75, "m", "cm", 100), (1, 25, "m", "cm", 100),
                                    (12, 45, "cm", "mm", 10)]:
        Lc = Lm * mul
        p = 2 * Lc + 2 * Wc
        its.append(mcq(fig(polygon_svg(rect_pts(Lc, Wc), [L(Lm, big), "", "", L(Wc, small)],
                                       "rectangle %d %s by %d %s" % (Lm, big, Wc, small))) +
                       "What is the perimeter in <b>%s</b>?" % ("centimetres" if small == "cm" else "millimetres"),
                       L(p, small), [L(v, small) for v in [2 * Lm + 2 * Wc, Lc + Wc, 2 * Lc + Wc, Lm + Wc]],
                       "The units are different. Change first: %d %s = %d %s. Then 2 × %d + 2 × %d = %d + %d = "
                       "<b>%d %s</b>. Adding %d + %d + %d + %d = %d mixes %s and %s."
                       % (Lm, big, Lc, small, Lc, Wc, 2 * Lc, 2 * Wc, p, small,
                          Lm, Wc, Lm, Wc, 2 * Lm + 2 * Wc, big, small), want=p * UNIT[small]))
    for Lg, Wd, u, where in [(125, 80, "m", "a school field"), (350, 275, "cm", "a classroom rug"),
                             (2400, 1600, "m", "a farm field in the Fraser Valley")]:
        p = 2 * Lg + 2 * Wd
        its.append(mcq("%s is a rectangle %s long and %s wide. What is its perimeter?"
                       % (where[0].upper() + where[1:], L(Lg, u), L(Wd, u)), L(p, u),
                       [L(v, u) for v in [Lg + Wd, 2 * Lg + Wd, Lg + 2 * Wd, p - 100]],
                       "2 × %s + 2 × %s = %s + %s = <b>%s %s</b>."
                       % (n(Lg), n(Wd), n(2 * Lg), n(2 * Wd), n(p), u), want=p * UNIT[u]))
    assert len(its) == 20, len(its)
    return {"title": "Rectangles: 2 × length + 2 × width", "items": its}


# ============================================================ set 4: missing side
def set_missing(rnd):
    its = []
    for i in range(6):
        u = ["cm", "m"][i % 2]
        if i < 3:
            pts, sides = tri_shape(rnd, 5, 16)
        else:
            pts = QUAD[[0, 2, 1][i - 3]]
            sides = scaled_sides(pts, rnd, lo=4, hi=20)
        k = rnd.randrange(len(sides))
        p, x = sum(sides), sides[k]
        known = [v for j, v in enumerate(sides) if j != k]
        lab = [L(v, u) for v in sides]
        lab[k] = "? %s" % u
        name = "triangle" if len(sides) == 3 else "quadrilateral"
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with one unknown side" % name)) +
                       "The perimeter of this %s is <b>%d %s</b>. What is the missing side length?" % (name, p, u),
                       L(x, u), [L(v, u) for v in [sum(known), p + sum(known), x + 2, x - 2, x + 10, x + 1]],
                       "Add the sides you know: %s = %d. Subtract from the perimeter: %d − %d = <b>%d %s</b>. "
                       "Check: %s = %d." % (plus(known), sum(known), p, sum(known), x, u, plus(sides), p),
                       want=x * UNIT[u]))
    for P, Lg, u in [(30, 9, "cm"), (46, 15, "cm"), (64, 20, "m"), (100, 35, "m")]:
        Wd = (P - 2 * Lg) // 2
        assert 2 * Lg + 2 * Wd == P and Wd < Lg
        its.append(mcq(fig(rect_svg(Lg, Wd, u, wlab="? %s" % u, label="rectangle with unknown width")) +
                       "The perimeter of the rectangle is <b>%d %s</b>. How wide is it?" % (P, u),
                       L(Wd, u), [L(v, u) for v in [P - 2 * Lg, P - Lg, P // 2, Wd + 1]],
                       "The two lengths use 2 × %d = %d %s. That leaves %d − %d = %d %s for the two widths. "
                       "Each width is %d ÷ 2 = <b>%d %s</b>." % (Lg, 2 * Lg, u, P, 2 * Lg, P - 2 * Lg, u,
                                                                  P - 2 * Lg, Wd, u), want=Wd * UNIT[u]))
    its.append(mcq("A rectangle has a perimeter of <b>54 cm</b>. It is 7 cm wide. How long is it?",
                   "20 cm", ["40 cm", "47 cm", "27 cm"],
                   "The two widths use 2 × 7 = 14 cm. 54 − 14 = 40 cm for the two lengths. "
                   "Each length is 40 ÷ 2 = <b>20 cm</b>. Check: 20 + 7 + 20 + 7 = 54.", want=200))
    for P, u in [(36, "cm"), (84, "m"), (200, "cm")]:
        s = P // 4
        its.append(mcq("A square has a perimeter of <b>%d %s</b>. How long is each side?" % (P, u), L(s, u),
                       [L(v, u) for v in [P // 2, P - 4, P * 4]],
                       "A square has 4 equal sides: %d ÷ 4 = <b>%d %s</b>. Check: 4 × %d = %d. "
                       "Dividing by 2 gives %d, which is two sides together." % (P, s, u, s, P, P // 2),
                       want=s * UNIT[u]))
    for k, P, u in [(3, 36, "cm"), (6, 48, "cm"), (8, 72, "m")]:
        s = P // k
        assert s * k == P
        cands = [P // 4 if P % 4 == 0 else None, P - k, P // 2]
        its.append(mcq("A%s %s has a perimeter of <b>%d %s</b>. How long is each side?" % ("n" if REG_NAME[k][0] in "aeiou" else "", REG_NAME[k], P, u), L(s, u),
                       [L(v, u) for v in cands if v],
                       "A%s %s has %d equal sides: %d ÷ %d = <b>%d %s</b>. Check: %d × %d = %d. "
                       "Dividing by 4 only works for a square." % ("n" if REG_NAME[k][0] in "aeiou" else "",
                                                                   REG_NAME[k], k, P, k, s, u, k, s, P),
                       want=s * UNIT[u]))
    for P, good, wrong, u in [(28, (8, 6), [(4, 7), (20, 8), (8, 7)], "cm"),
                              (40, (12, 8), [(5, 8), (25, 15), (12, 9)], "m"),
                              (50, (15, 10), [(5, 10), (30, 20), (15, 11)], "cm")]:
        a, b = good
        assert 2 * (a + b) == P
        assert wrong[0][0] * wrong[0][1] == P and sum(wrong[1]) == P
        for x, y in wrong:
            assert 2 * (x + y) != P
        cands = ["%d %s by %d %s" % (x, u, y, u) for x, y in wrong]
        e = ("%d + %d + %d + %d = <b>%d %s</b>. Quick check: length + width must be half of %d, which is %d. "
             "%s has an <b>area</b> of %d, not a perimeter of %d."
             % (a, b, a, b, P, u, P, P // 2, cands[0], P, P))
        its.append(mcq("Which rectangle has a perimeter of <b>%d %s</b>?" % (P, u),
                       "%d %s by %d %s" % (a, u, b, u), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing side from the perimeter", "items": its}


# ============================================================ set 5: composite shapes and word problems
def set_story():
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, want=want))

    # composite shapes with square corners (all corners are right angles)
    U1 = [(0, 0), (9, 0), (9, 3), (4, 3), (4, 8), (0, 8)]
    s1 = ortho_sides(U1)
    p1 = sum(s1)
    assert s1 == [9, 3, 5, 5, 4, 8] and p1 == 34 and ortho_area(U1) == 47
    add(fig(polygon_svg(ortho_pts(U1), [L(v, "m") for v in s1], "L-shaped deck with side lengths")) +
        "This is the shape of a deck. What is its perimeter?", L(p1, "m"),
        [L(v, "m") for v in [p1 - 5, p1 - 3, ortho_area(U1), p1 + 4]],
        "Add all 6 sides: %s = <b>%d m</b>. An L shape has 6 sides, so check that you added 6 numbers."
        % (plus(s1), p1), want=p1 * 1000)
    U2 = [(0, 0), (12, 0), (12, 3), (8, 3), (8, 9), (4, 9), (4, 3), (0, 3)]
    s2 = ortho_sides(U2)
    p2 = sum(s2)
    assert s2 == [12, 3, 4, 6, 4, 6, 4, 3] and p2 == 42
    add(fig(polygon_svg(ortho_pts(U2), [L(v, "cm") for v in s2], "T-shaped figure with side lengths")) +
        "What is the perimeter of this shape?", L(p2, "cm"),
        [L(v, "cm") for v in [p2 - 3, p2 - 6, p2 - 4, p2 + 10]],
        "There are 8 sides: %s = <b>%d cm</b>. Count the sides first so you do not miss a short one."
        % (plus(s2), p2), want=p2 * 10)
    U3 = [(0, 0), (12, 0), (12, 5), (5, 5), (5, 9), (0, 9)]
    s3 = ortho_sides(U3)
    p3 = sum(s3)
    assert s3 == [12, 5, 7, 4, 5, 9] and p3 == 42
    lab3 = [L(12, "cm"), L(5, "cm"), "?", "?", L(5, "cm"), L(9, "cm")]
    add(fig(polygon_svg(ortho_pts(U3), lab3, "L-shaped figure with two unknown sides")) +
        "All the corners are square corners. Find the two missing sides. What is the perimeter?",
        L(p3, "cm"), [L(v, "cm") for v in [31, p3 - 7, p3 - 4, 12 * 9]],
        "The top is 12 cm, so the bottom part is 12 − 5 = 7 cm. The left side is 9 cm, so the short side is "
        "9 − 5 = 4 cm. Now add all 6 sides: %s = <b>%d cm</b>. 31 cm adds only the 4 numbers shown."
        % (plus(s3), p3), want=p3 * 10)
    U4 = [(0, 0), (3, 0), (3, 5), (10, 5), (10, 0), (13, 0), (13, 8), (0, 8)]
    s4 = ortho_sides(U4)
    p4 = sum(s4)
    assert s4 == [3, 5, 7, 5, 3, 8, 13, 8] and p4 == 52
    add(fig(polygon_svg(ortho_pts(U4), [L(v, "m") for v in s4], "U-shaped figure with side lengths")) +
        "What is the perimeter of this shape?", L(p4, "m"),
        [L(v, "m") for v in [2 * (13 + 8), p4 - 5, p4 - 7, p4 + 5]],
        "Add all 8 sides: %s = <b>%d m</b>. The notch adds two 5 m sides, so the answer is more than "
        "the 42 m of a plain 13 m by 8 m rectangle." % (plus(s4), p4), want=p4 * 1000)
    U5 = [(0, 0), (3, 0), (3, 2), (6, 2), (6, 4), (9, 4), (9, 6), (0, 6)]
    U5 = [(x, 6 - y) for x, y in U5][::-1]
    s5 = ortho_sides(U5)
    p5 = sum(s5)
    assert p5 == 30
    big = [i for i, v in enumerate(s5) if v in (9, 6)]
    lab5 = [L(v, "m") if v in (9, 6) else "" for v in s5]
    assert len(big) == 2
    add(fig(polygon_svg(ortho_pts(U5), lab5, "staircase garden bed with two side lengths")) +
        "A garden bed has steps on one side. All the corners are square corners. What is its perimeter?",
        L(p5, "m"), [L(v, "m") for v in [15, 21, 54]],
        "The steps that go across add up to the 9 m side, and the steps that go up add up to the 6 m side. "
        "So the perimeter is the same as a 9 m by 6 m rectangle: 9 + 6 + 9 + 6 = <b>30 m</b>.", want=30000)
    # word problems
    add("Simran’s family grows vegetables in Kelowna. Their garden is a rectangle 9 m long and 6 m wide. "
        "How much fence do they need to go all the way around it?", "30 m", ["15 m", "54 m", "24 m"],
        "The fence goes around all 4 sides: 9 + 6 + 9 + 6 = <b>30 m</b>. 15 m is only two sides, "
        "and 54 is the area.", want=30000)
    add("Mateo’s family walks the trail around a lake in Stanley Park. The trail map shows 4 parts: "
        "350 m, 280 m, 400 m and 220 m. How long is the whole loop?", "1250 m", ["1030 m", "900 m", "1150 m"],
        "Add all 4 parts: 350 + 280 = 630, 630 + 400 = 1030, 1030 + 220 = <b>1250 m</b>. "
        "1030 m leaves out the last part.", want=1250000)
    add("The Stanley Park lake loop is 1250 m. How does that compare with 1 km?", "250 m more than 1 km",
        ["250 m less than 1 km", "750 m more than 1 km", "1250 m more than 1 km"],
        "1 km = 1000 m. 1250 − 1000 = 250, so the loop is <b>250 m more than 1 km</b>.")
    add("A hockey rink is about 60 m long and 26 m wide. About how long are the boards all the way around it?",
        "172 m", ["86 m", "146 m", "1560 m"],
        "2 × 60 + 2 × 26 = 120 + 52 = <b>172 m</b>. 86 m is one length and one width, and 1560 is the area.",
        want=172000)
    add("For the Terry Fox Run, Grade 4 runs laps around the school field. The field is 120 m long and 80 m wide. "
        "How many laps make 2 km?", "5", ["10", "2", "4"],
        "One lap: 120 + 80 + 120 + 80 = 400 m. 2 km = 2000 m. 400 × 5 = 2000, so <b>5 laps</b>. "
        "10 laps would be right only if one lap were 200 m (just 120 + 80).")
    add("Harjot builds a dog run 12 m long and 5 m wide. One long side is the wall of the house, so it needs "
        "no fence. How much fence does he need?", "22 m", ["34 m", "17 m", "29 m"],
        "Only 3 sides get fence: 5 + 12 + 5 = <b>22 m</b>. 34 m puts fence along the house wall too.",
        want=22000)
    add("Chloe’s family builds a raised garden bed out of cedar boards. It is 240 cm long and 120 cm wide. "
        "How many centimetres of board go around the edge?", "720 cm", ["360 cm", "600 cm", "480 cm"],
        "2 × 240 + 2 × 120 = 480 + 240 = <b>720 cm</b>. 600 cm leaves out one short side.", want=7200)
    add("Kai’s garden bed is <b>3 m</b> long and <b>80 cm</b> wide. How much edging goes around it?",
        "760 cm", ["166 cm", "380 cm", "680 cm"],
        "Change to the same unit first: 3 m = 300 cm. 300 + 80 + 300 + 80 = <b>760 cm</b>. "
        "166 cm comes from adding 3 + 80 + 3 + 80, which mixes metres and centimetres.", want=7600)
    assert 2 * 150 + 2 * 90 == 480
    add("Ms. Grewal’s bulletin board is 150 cm long and 90 cm wide. She has 4 m of paper border. Is that enough "
        "to go all the way around?", "No, she needs 480 cm.",
        ["Yes, she needs 240 cm.", "Yes, she needs 390 cm.", "No, she needs 13" + NBSP + "500 cm."],
        "Perimeter: 150 + 90 + 150 + 90 = 480 cm. 4 m = 400 cm, and 400 &lt; 480, so <b>it is not enough</b>. "
        "240 cm is only one length and one width.")
    add("A park in Surrey is shaped like a triangle. Its sides are 140 m, 95 m and 115 m. Nadia walks once around "
        "the park. How far does she walk?", "350 m", ["235 m", "255 m", "360 m"],
        "Add the 3 sides: 140 + 95 = 235, 235 + 115 = <b>350 m</b>. 235 m leaves out the 115 m side.",
        want=350000)
    add("Owen uses 34 m of fence to go around a rectangular chicken run. The run is 11 m long. How wide is it?",
        "6 m", ["23 m", "12 m", "17 m"],
        "Two lengths: 11 + 11 = 22 m. 34 − 22 = 12 m for the two widths. 12 ÷ 2 = <b>6 m</b>. "
        "23 m forgets the second length.", want=6000)
    add("A square patio in Nanaimo has a perimeter of 28 m. How long is each side?", "7 m",
        ["14 m", "24 m", "112 m"],
        "A square has 4 equal sides: 28 ÷ 4 = <b>7 m</b>. 14 m is half of 28, which is two sides together.",
        want=7000)
    assert 2 * (10 + 4) == 28 and 2 * (8 + 7) == 30
    add("Garden A is 10 m by 4 m. Garden B is 8 m by 7 m. Which garden needs more fence to go around it?",
        "B, by 2 m", ["A, by 2 m", "They need the same.", "B, by 16 m"],
        "A: 10 + 4 + 10 + 4 = 28 m. B: 8 + 7 + 8 + 7 = 30 m. 30 − 28 = 2, so <b>B needs 2 m more</b>. "
        "16 compares the areas (56 and 40), not the fences.")
    add("Ji-woo walks around a city block in Victoria 3 times. The block is 200 m long and 150 m wide. "
        "How far does he walk in all?", "2100 m", ["1050 m", "700 m", "1400 m"],
        "One time around: 200 + 150 + 200 + 150 = 700 m. 3 times: 3 × 700 = <b>2100 m</b>. "
        "1050 m uses only 200 + 150 for each lap.", want=2100000)
    add("Ryan puts a string of lights around a rectangular window. The window is 120 cm wide and 90 cm tall. "
        "How long is the string of lights?", "4 m 20 cm", ["2 m 10 cm", "3 m 30 cm", "42 m"],
        "120 + 90 + 120 + 90 = 420 cm. 100 cm = 1 m, so 420 cm = <b>4 m 20 cm</b>. "
        "42 m mixes up centimetres and metres.", want=4200)
    order = [0, 1, 3, 5, 6, 8, 9, 7, 11, 12, 14, 10, 16, 15, 13, 2, 4, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Composite shapes and word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


LESSON_L = [(0, 0), (10, 0), (10, 4), (6, 4), (6, 7), (0, 7)]


def body_html():
    sl = ortho_sides(LESSON_L)
    assert sl == [10, 4, 4, 3, 6, 7] and sum(sl) == 34
    lab = [L(10, "m"), L(4, "m"), "?", "?", L(6, "m"), L(7, "m")]
    return (
        "<h2>What is perimeter?</h2>"
        "<p>Perimeter is the <b>distance all the way around</b> a flat shape. To find it, <b>add every side</b>. "
        "Perimeter is a length, so it uses mm, cm, m or km.</p>"
        "<figure class='sn-fig'>" + grid_svg(rect_cells(5, 3), cell=30, label="rectangle 5 by 3 on a grid") +
        "<figcaption>Each square is 1 cm on each side. Go around: 5 + 3 + 5 + 3 = 16 cm. "
        "The 15 squares inside are the area, not the perimeter.</figcaption></figure>"
        "<h2>Regular polygons: multiply</h2>"
        "<p>In a regular polygon, every side is the same length. "
        "Perimeter = side length × number of sides.</p>"
        "<figure class='sn-fig'>" + reg_svg(6, "7 cm") +
        "<figcaption>A regular hexagon has 6 sides of 7 cm: 6 × 7 = 42 cm.</figcaption></figure>"
        "<h2>Rectangles: 2 lengths and 2 widths</h2>"
        "<p>A rectangle has 4 sides, even when only 2 numbers are shown. "
        "Perimeter = 2 × length + 2 × width.</p>"
        "<figure class='sn-fig'>" + rect_svg(9, 4, "cm") +
        "<figcaption>2 × 9 + 2 × 4 = 18 + 8 = 26 cm.</figcaption></figure>" +
        ex("Example 1: find a missing side",
           "A rectangle has a perimeter of 30 cm. It is 9 cm long. How wide is it?",
           "The two lengths use 2 × 9 = 18 cm. 30 − 18 = 12 cm is left for the two widths. 12 ÷ 2 = 6.", "6 cm") +
        "<h2>Composite shapes</h2>"
        "<p>Some shapes are made of rectangles. Use the sides you know to find the missing ones. "
        "Then add <b>every</b> side.</p>"
        "<figure class='sn-fig'>" + polygon_svg(ortho_pts(LESSON_L), lab, "L-shaped figure with two unknown sides") +
        "<figcaption>Missing sides: 10 − 6 = 4 m and 7 − 4 = 3 m. "
        "Perimeter: 10 + 4 + 4 + 3 + 6 + 7 = 34 m.</figcaption></figure>" +
        ex("Example 2: use the same unit",
           "A garden bed is 2 m long and 40 cm wide. What is its perimeter?",
           "Change first: 2 m = 200 cm. Then 200 + 40 + 200 + 40 = 480.", "480 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the squares inside", "That is the area. Perimeter counts the sides around the outside"],
            ["Adding only the 2 numbers shown on a rectangle", "Add all 4 sides: 9 + 4 + 9 + 4"],
            ["Missing a short side on an L shape", "Count the sides first, then add that many numbers"],
            ["Using 4 sides for every shape", "A hexagon has 6 sides, an octagon has 8"],
            ["Adding 2 m + 40 cm as 42", "Change to one unit first: 200 cm + 40 cm"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about perimeter in BC?",
     "a": "In the Geometry and measurement area of the BC Grade 4 math curriculum, students find the perimeter of "
          "regular and irregular shapes using standard units like mm, cm and m."},
    {"q": "What is the formula for the perimeter of a rectangle?",
     "a": "Perimeter = 2 × length + 2 × width. A rectangle 9 cm long and 4 cm wide has a perimeter of "
          "18 + 8 = 26 cm."},
    {"q": "How do you find a missing side when you know the perimeter?",
     "a": "Add the sides you know, then subtract that total from the perimeter. For a rectangle, take away the two "
          "lengths and halve what is left to get the width."},
    {"q": "Do these perimeter worksheets help with the Grade 4 FSA?",
     "a": "Yes. The Grade 4 FSA includes numeracy, where students solve problems in real situations. "
          "Word problems like fencing a garden or walking a trail are good practice for that kind of thinking."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (grid shapes need countable squares)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(34812)
    sets = [set_grid(rnd), set_regular(), set_rect(), set_missing(rnd), set_story()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [parse(x) for x in it["c"]]
            vals = [v for v in vals if v is not None]
            assert len(vals) == len(set(vals)), it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["q"][:400] + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "perimeter", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Perimeter",
        "seo_title": "Grade 4 Perimeter Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Perimeter",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 4: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Perimeter of regular and irregular shapes",
        "meta_desc": "Free Grade 4 math worksheets on perimeter for the BC curriculum: count sides on a grid, "
                     "multiply for regular polygons, use 2 × length + 2 × width for rectangles, find a missing side, "
                     "and solve composite shape and garden fence word problems. 100 questions with an answer key, "
                     "good FSA numeracy practice.",
        "key_big": "Perimeter is the distance all the way around a shape: add every side.",
        "key_sub": "Regular polygon: side × number of sides. Rectangle: 2 × length + 2 × width. "
                   "Count the sides, not the squares inside, and change to one unit first (2 m = 200 cm).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(on a grid|grid shapes)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
