# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 5 Math: Area and Perimeter (BC Mathematics Curriculum,
Geometry and measurement: area measurement of squares and rectangles; relationships between area and perimeter)
  python3 tools/gen_cabc_math_g5_area_perimeter.py
Count unit squares (rectangles, L-shapes, rows and columns) -> area = length × width in cm² and m²;
perimeter = 2 × length + 2 × width; missing sides from the area or the perimeter; the same area with
different perimeters; BC word problems. Wrong choices come from real mistakes (adding the sides, mixing
area and perimeter, writing cm for cm², subtracting instead of dividing, forgetting to halve).
Every answer is worked out in code. Drawing helpers copied from gen_caon_math_g4_area.py.
BC style: Canadian English, 4-digit numbers without a separator, 5 or more digits with a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRIDC = "#8db59b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
SQ = {"cm": "cm²", "m": "m²"}
NBSP = " "


# ------------------------------------------------------------ helpers
def fmt(n):
    """4536 -> 4536, 30000 -> 30 000 (no-break space, BC style)."""
    return "{:,}".format(n).replace(",", NBSP) if n >= 10000 else str(n)


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


def rot(c, k):
    r = k % len(c)
    return c[r:] + c[:r]


# ------------------------------------------------------------ labelled rectangle (drawn to scale)
FS = 17


def rect_svg(L, W, top, left, label, inner="", max_w=190, max_h=95):
    """L × W rectangle drawn to scale. top/left = side labels ('?' labels are red); inner = text inside."""
    k = min(max_w / L, max_h / W, 24)
    Wp, Hp = L * k, W * k
    pad = 5
    lw = tw(left, FS) + 10 if left else 0
    th = 26 if top else 0
    ox, oy = pad + lw, pad + th
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>"
         % (ox, oy, Wp, Hp, FILL, GREEN)]
    if top:
        s.append(text(ox + Wp / 2, oy - 9, top, FS, RED if "?" in top else INK))
    if left:
        s.append(text(ox - lw / 2 - 2, oy + Hp / 2 + 6, left, FS, RED if "?" in left else INK))
    if inner:
        assert Wp >= tw(inner, 15) + 10 and Hp >= 26, (L, W, inner)
        s.append(text(ox + Wp / 2, oy + Hp / 2 + 5, inner, 15, GREEN))
    W_ = max(ox + Wp + pad, tw(top, FS) + 2 * pad if top else 0)
    return svg_wrap(int(math.ceil(W_)), int(math.ceil(oy + Hp + pad)), "".join(s), label)


# ------------------------------------------------------------ squared grids
def cells_body(cells, x0, y0, cols, rows, cell, m=0):
    """Grid lines over cols × rows, shaded cells, and a thick outline around the shaded shape."""
    g = []
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + c * cell, y0 + r * cell, cell, cell, FILL))
    for i in range(cols + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 - m * cell + i * cell, y0 - m * cell, x0 - m * cell + i * cell, y0 - m * cell + rows * cell, GRIDC))
    for j in range(rows + 1):
        g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (x0 - m * cell, y0 - m * cell + j * cell, x0 - m * cell + cols * cell, y0 - m * cell + j * cell, GRIDC))
    # outline: every cell edge that has no shaded neighbour on the other side
    for (c, r) in cells:
        x, y = x0 + c * cell, y0 + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                         (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (c + dc, r + dr) not in cells:
                g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='square'/>"
                         % (x1, y1, x2, y2, GREEN))
    return "".join(g)


def shape_svg(cells, label, cell=22):
    """Shaded cells on a grid with a 1-square margin all round."""
    L = max(c for c, r in cells) + 1
    W = max(r for c, r in cells) + 1
    m = 4
    cols, rows = L + 2, W + 2
    body = cells_body(set(cells), m + cell, m + cell, cols, rows, cell, m=1)
    return svg_wrap(cols * cell + 2 * m, rows * cell + 2 * m, body, label)


def rect_cells(L, W):
    return {(c, r) for c in range(L) for r in range(W)}


def grid_svg(L, W, label, mode="full", cell=22):
    """L × W rectangle on a grid. mode 'edge': only the top row and the left column of squares are drawn."""
    if mode == "full":
        return shape_svg(rect_cells(L, W), label, cell)
    m = 4
    x0, y0 = m, m
    g = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (x0, y0, L * cell, W * cell)]
    cells = {(c, 0) for c in range(L)} | {(0, r) for r in range(W)}
    for (c, r) in sorted(cells):
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + c * cell, y0 + r * cell, cell, cell, FILL, GREEN))
    g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0, y0, L * cell, W * cell, INK))
    return svg_wrap(L * cell + 2 * m, W * cell + 2 * m, "".join(g), label)


def l_cells(L, W, c, r):
    """L × W rectangle with a c × r piece cut from the top-right corner."""
    return {(x, y) for x in range(L) for y in range(W) if not (x >= L - c and y < r)}


def twin_svg(a, b, label, cell=20):
    """Two rectangles (L, W) on one grid, labelled A and B."""
    (L1, W1), (L2, W2) = a, b
    m = 4
    rows = max(W1, W2) + 2
    cols = L1 + L2 + 3
    th = 24
    cells = rect_cells(L1, W1) | {(L1 + 1 + x, y) for x in range(L2) for y in range(W2)}
    body = cells_body(cells, m + cell, m + th + cell, cols, rows, cell, m=1)
    body += text(m + cell + L1 * cell / 2, m + 18, "A", 17)
    body += text(m + cell + (L1 + 1 + L2 / 2) * cell, m + 18, "B", 17)
    return svg_wrap(cols * cell + 2 * m, rows * cell + 2 * m + th, body, label)


# ------------------------------------------------------------ set 1: area by counting squares
def set_count(rnd, P):
    its = []
    for k, (L, W, un) in enumerate([(7, 4, "square units"), (8, 3, "cm²"), (6, 6, "cm²"),
                                    (9, 4, "square units"), (10, 3, "cm²"), (8, 5, "cm²")]):
        A, Pm, bd = L * W, 2 * (L + W), 2 * (L + W) - 4
        assert len({A, Pm, bd, L + W}) == 4
        shape = "square" if L == W else "rectangle"
        svg = grid_svg(L, W, "%s %d squares by %d squares on a grid" % (shape, L, W))
        if un == "cm²":
            q = fig(svg) + "Each small square is 1 cm². What is the area of the shaded %s?" % shape
            cands = rot(["%d cm²" % Pm, "%d cm²" % bd, "%d cm²" % (L + W)], k) + ["%d cm" % A]
        else:
            q = fig(svg) + "What is the area of the shaded %s in square units?" % shape
            cands = rot(["%d square units" % Pm, "%d square units" % bd, "%d square units" % (L + W)], k)
        e = ("There are %d rows with %d squares in each row: %d × %d = %d. The area is %d %s. "
             "(%d is the perimeter, the distance around the edge.)" % (W, L, W, L, A, A, un, Pm))
        its.append(mcq(q, "%d %s" % (A, un), cands, e, rnd))
    # L-shapes: count, or split into two rectangles
    for k, (L, W, c, r) in enumerate([(8, 5, 3, 2), (6, 5, 2, 3), (9, 4, 4, 2)]):
        cells = l_cells(L, W, c, r)
        A, box, cut, Pm = len(cells), L * W, c * r, 2 * (L + W)
        assert A == box - cut and len({A, box, cut, Pm}) == 4
        a1, a2 = (L - c) * W, c * (W - r)
        assert a1 + a2 == A
        svg = shape_svg(cells, "shape made of two rectangles on a grid")
        q = fig(svg) + "Each small square is 1 cm². What is the area of the shaded shape?"
        e = ("Split the shape into two rectangles: %d × %d = %d and %d × %d = %d. %d + %d = %d cm². "
             "(%d cm² would count the empty corner too.)" % (W, L - c, a1, W - r, c, a2, a1, a2, A, box))
        cands = rot(["%d cm²" % box, "%d cm²" % Pm, "%d cm" % A], k) + ["%d cm²" % cut]
        its.append(mcq(q, "%d cm²" % A, cands, e, rnd))
    # only the top row and the left column are drawn
    for k, (L, W) in enumerate([(7, 5), (9, 4), (8, 6), (10, 4)]):
        A, shown = L * W, L + W - 1
        svg = grid_svg(L, W, "rectangle with only the top row and left column of squares drawn", "edge")
        q = (fig(svg) + "Only the top row and the left column of squares are drawn. "
             "How many squares would cover the whole rectangle?")
        e = ("The top row shows %d squares in each row. The left column shows %d rows. "
             "%d × %d = %d squares." % (L, W, W, L, A))
        cands = rot(["%d squares" % shown, "%d squares" % (L + W), "%d squares" % (2 * (L + W))], k)
        its.append(mcq(q, "%d squares" % A, cands, e, rnd))
    # which multiplication matches the grid
    for k, (L, W) in enumerate([(7, 3), (8, 4), (9, 5)]):
        svg = grid_svg(L, W, "rectangle %d squares by %d squares on a grid" % (L, W))
        q = fig(svg) + "Which multiplication gives the number of squares in this rectangle?"
        e = "There are %d rows of %d squares. %d × %d = %d squares." % (W, L, W, L, W * L)
        cands = rot(["%d + %d" % (W, L), "%d × %d" % (W - 1, L), "%d × %d" % (W, L + 1)], k)
        its.append(mcq(q, "%d × %d" % (W, L), cands, e, rnd))
    # rows of squares in words
    for k, (r, c, un) in enumerate([(6, 9, "cm"), (7, 12, "m")]):
        A = r * c
        q = ("A rectangle is covered by %d rows of 1 %s² squares, with %d squares in each row. "
             "What is its area?" % (r, un, c))
        e = "%d rows of %d squares: %d × %d = %d squares, so the area is %d %s." % (r, c, r, c, A, A, SQ[un])
        cands = rot(["%d %s" % (r + c, SQ[un]), "%d %s" % (2 * (r + c), SQ[un])], k) + ["%d %s" % (A, un)]
        its.append(mcq(q, "%d %s" % (A, SQ[un]), cands, e, rnd))
    its.append(mcq("Why can you multiply to find the number of squares in a rectangle?",
                   "Every row has the same number",
                   ["The rows get longer and longer", "Squares can overlap", "You only count the edge"],
                   "In a rectangle, the squares sit in equal rows. Equal groups can be multiplied: "
                   "number of rows × squares in each row.", rnd))
    its.append(mcq("Rectangle A has 4 rows of 9 squares. Rectangle B has 9 rows of 4 squares. "
                   "Which is true?", "Both have 36 squares",
                   ["A has more squares", "B has more squares", "Both have 13 squares"],
                   "4 × 9 = 36 and 9 × 4 = 36. Turning a rectangle does not change its area.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the area by counting squares", "items": its}


# ------------------------------------------------------------ set 2: area = length × width
def set_formula(rnd, P):
    its = []
    for i, (L, W, u) in enumerate([(8, 5, "cm"), (9, 6, "m"), (12, 4, "m"), (11, 6, "cm"), (10, 9, "m"),
                                   (13, 5, "cm")]):
        A, Pm = L * W, 2 * (L + W)
        assert A != Pm
        q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
             "What is the area of this rectangle?")
        e = "Area = length × width: %d × %d = %d %s. (%d %s is the perimeter.)" % (L, W, A, SQ[u], Pm, u)
        cands = rot(["%d %s" % (Pm, SQ[u]), "%d %s" % (L + W, SQ[u]), "%d %s" % (A, u)], i)
        its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
    for i, (L, W, u) in enumerate([(24, 6, "cm"), (35, 8, "m"), (15, 12, "cm"), (23, 14, "m"), (32, 25, "cm"),
                                   (36, 15, "m")]):
        A, Pm = L * W, 2 * (L + W)
        if W < 10:
            t, o = divmod(L, 10)
            wrong = t * 10 * W + o            # forgot to multiply the ones
            e = ("Area = length × width: %d × %d. Split %d into %d + %d: %d × %d = %d and %d × %d = %d. "
                 "%d + %d = %d %s." % (L, W, L, t * 10, o, t * 10, W, t * 10 * W, o, W, o * W,
                                       t * 10 * W, o * W, A, SQ[u]))
        else:
            lt, lo = divmod(L, 10)
            wt, wo = divmod(W, 10)
            wrong = lt * wt * 100 + lo * wo   # multiplied tens by tens and ones by ones only
            e = ("Area = length × width: %d × %d. Split %d into %d + %d: %d × %d = %d and %d × %d = %d. "
                 "%d + %d = %d %s. (Multiplying only tens × tens and ones × ones gives %d, which is too small.)"
                 % (L, W, W, wt * 10, wo, L, wt * 10, L * wt * 10, L, wo, L * wo, L * wt * 10, L * wo, A, SQ[u],
                    wrong))
        assert len({A, Pm, wrong, L + W}) == 4
        q = "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
        cands = rot(["%s %s" % (fmt(wrong), SQ[u]), "%d %s" % (Pm, SQ[u]), "%d %s" % (L + W, SQ[u])], i) + \
            ["%s %s" % (fmt(A), u)]
        its.append(mcq(q, "%s %s" % (fmt(A), SQ[u]), cands, e, rnd))
    for k, (s, u) in enumerate([(15, "cm"), (20, "m")]):
        A = s * s
        if k == 0:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "%d %s" % (s, u), "square with %d %s sides" % (s, u))) +
                 "This is a square. What is its area?")
        else:
            q = "A square has sides of %d %s. What is its area?" % (s, u)
        e = ("The length and width of a square are the same: %d × %d = %d %s. (%d %s is the perimeter.)"
             % (s, s, A, SQ[u], 4 * s, u))
        cands = ["%d %s" % (4 * s, SQ[u]), "%d %s" % (2 * s, SQ[u]), "%d %s" % (A, u)]
        its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
    U4 = ["cm", "m", "cm²", "m²"]
    for thing, right, why in [
        ("the area of a soccer field", "m²", "A field is big and area is the space inside, so use square metres."),
        ("the area of a bookmark", "cm²", "A bookmark is small and area is the space inside, so use square centimetres."),
        ("the area of a classroom floor", "m²", "A floor is big and area is the space inside, so use square metres."),
    ]:
        its.append(mcq("Which unit is best for measuring %s?" % thing, right, [x for x in U4 if x != right],
                       why + " cm and m measure length; cm² and m² measure area.", rnd))
    its.append(mcq("Rectangle A is 12 cm by 6 cm. Rectangle B is 9 cm by 8 cm. Which has the bigger area?",
                   "They are the same", ["Rectangle A", "Rectangle B", "You cannot tell"],
                   "A: 12 × 6 = 72 cm². B: 9 × 8 = 72 cm². The areas are the same, even though the shapes "
                   "look different.", rnd))
    its.append(mcq("Rectangle A is 10 m by 7 m. Rectangle B is 9 m by 8 m. Which has the bigger area?",
                   "Rectangle B, by 2 m²", ["Rectangle A, by 2 m²", "They are the same", "Rectangle B, by 1 m²"],
                   "A: 10 × 7 = 70 m². B: 9 × 8 = 72 m². 72 − 70 = 2, so B is bigger by 2 m². "
                   "(10 + 7 and 9 + 8 are both 17, but adding the sides does not give the area.)", rnd))
    its.append(mcq("Which rule gives the area of a rectangle?", "length × width",
                   ["length + width", "2 × length + 2 × width", "length × 4"],
                   "Area counts the squares inside: rows × squares in each row, which is length × width. "
                   "2 × length + 2 × width is the perimeter.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area = length × width (cm² and m²)", "items": its}


# ------------------------------------------------------------ set 3: perimeter
def set_perimeter(rnd, P):
    its = []
    for i, (L, W, u) in enumerate([(9, 4, "cm"), (12, 5, "m"), (15, 8, "cm"), (20, 6, "m"), (11, 7, "cm"),
                                   (25, 10, "m")]):
        A, Pm = L * W, 2 * (L + W)
        assert len({A, Pm, L + W, 2 * L + W}) == 4
        q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
             "What is the perimeter of this rectangle?")
        e = ("Perimeter = 2 × length + 2 × width: %d + %d = %d %s. (%d × %d = %d %s is the area.)"
             % (2 * L, 2 * W, Pm, u, L, W, A, SQ[u]))
        cands = rot(["%d %s" % (L + W, u), "%d %s" % (2 * L + W, u), "%d %s" % (A, u)], i)
        its.append(mcq(q, "%d %s" % (Pm, u), cands, e, rnd))
    for i, (L, W, u) in enumerate([(34, 16, "cm"), (45, 25, "m"), (120, 75, "cm"), (250, 130, "m")]):
        A, Pm = L * W, 2 * (L + W)
        assert len({A, Pm, L + W, 2 * L + W}) == 4
        q = "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
        e = ("Add all four sides: %d + %d + %d + %d = %d %s. (Adding just %d + %d = %d %s goes only halfway "
             "around.)" % (L, W, L, W, Pm, u, L, W, L + W, u))
        cands = rot(["%d %s" % (L + W, u), "%d %s" % (2 * L + W, u), "%s %s" % (fmt(A), u)], i)
        its.append(mcq(q, "%d %s" % (Pm, u), cands, e, rnd))
    for k, (L, W) in enumerate([(7, 3), (6, 5)]):
        A, Pm, bd = L * W, 2 * (L + W), 2 * (L + W) - 4
        svg = grid_svg(L, W, "rectangle %d squares by %d squares on a centimetre grid" % (L, W))
        q = fig(svg) + "Each small square is 1 cm by 1 cm. What is the perimeter of the shaded rectangle?"
        e = ("Count the sides of the squares along the edge: %d + %d + %d + %d = %d cm. "
             "(%d is the number of squares inside, the area. %d counts the edge squares, and corner squares "
             "have two sides on the edge.)" % (L, W, L, W, Pm, A, bd))
        cands = rot(["%d cm" % A, "%d cm" % bd, "%d cm" % (L + W)], k)
        its.append(mcq(q, "%d cm" % Pm, cands, e, rnd))
    for k, (s, u) in enumerate([(13, "cm"), (25, "m")]):
        q = "A square has sides of %d %s. What is its perimeter?" % (s, u)
        e = "A square has 4 equal sides: 4 × %d = %d %s. (%d × %d = %d %s is the area.)" % (
            s, 4 * s, u, s, s, s * s, SQ[u])
        cands = rot(["%d %s" % (2 * s, u), "%d %s" % (s * s, u), "%d %s" % (3 * s, u)], k)
        its.append(mcq(q, "%d %s" % (4 * s, u), cands, e, rnd))
    for k, (Pm, u) in enumerate([(60, "cm"), (36, "m")]):
        s = Pm // 4
        q = "A square has a perimeter of %d %s. How long is each side?" % (Pm, u)
        e = "The 4 sides are equal: %d ÷ 4 = %d %s. Check: 4 × %d = %d %s." % (Pm, s, u, s, Pm, u)
        cands = rot(["%d %s" % (Pm // 2, u), "%d %s" % (Pm - 4, u), "%d %s" % (Pm * 4, u)], k)
        its.append(mcq(q, "%d %s" % (s, u), cands, e, rnd))
    for k, (m_, cm) in enumerate([(2, 60), (3, 80)]):
        L = m_ * 100
        Pm = 2 * (L + cm)
        q = "A rectangle is %d m long and %d cm wide. What is its perimeter in centimetres?" % (m_, cm)
        e = ("Change to one unit first: %d m = %d cm. Then %d + %d + %d + %d = %d cm. "
             "(%d comes from adding %d + %d + %d + %d without changing metres to centimetres.)"
             % (m_, L, L, cm, L, cm, Pm, 2 * (m_ + cm), m_, cm, m_, cm))
        cands = rot(["%d cm" % (2 * (m_ + cm)), "%d cm" % (L + cm), "%d cm" % (m_ + cm)], k)
        its.append(mcq(q, "%d cm" % Pm, cands, e, rnd))
    its.append(mcq("Which rule gives the perimeter of a rectangle?", "2 × length + 2 × width",
                   ["length × width", "length + width", "4 × length × width"],
                   "Perimeter is the distance around: two lengths and two widths. length × width is the area. "
                   "length + width goes only halfway around.", rnd))
    its.append(mcq("Which unit is best for the length of the fence around a school playground?", "m",
                   ["m²", "cm²", "mm"],
                   "A fence is a length around the edge, so use a length unit. A playground is big, so use metres. "
                   "m² and cm² are for area.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter of rectangles and squares", "items": its}


# ------------------------------------------------------------ set 4: missing side
def missing(A, L, u, figure, rnd, k):
    w = A // L
    assert w * L == A and w != L
    if figure:
        X, Y = (L, w) if L >= w else (w, L)
        top, left = ("%d %s" % (L, u), "? %s" % u) if L >= w else ("? %s" % u, "%d %s" % (L, u))
        q = (fig(rect_svg(X, Y, top, left, "rectangle with an area of %d %s and one side missing" % (A, SQ[u]),
                          inner="Area = %d %s" % (A, SQ[u]), max_w=200, max_h=100)) +
             "What is the length of the side marked ?")
    else:
        q = "A rectangle has an area of %d %s. One side is %d %s. How long is the other side?" % (A, SQ[u], L, u)
    e = ("Length × width = area, so think: %d × ? = %d. %d ÷ %d = %d, so the side is %d %s. "
         "Check: %d × %d = %d %s." % (L, A, A, L, w, w, u, L, w, A, SQ[u]))
    cands = ["%d %s" % (A - L, u)]
    if A % 2 == 0 and A // 2 - L > 0 and A // 2 - L not in (w, L):
        cands.append("%d %s" % (A // 2 - L, u))
    cands += ["%d %s" % (w, SQ[u]), "%d %s" % (w + 1, u)]
    cands = rot(cands[:3], k) + cands[3:]
    return mcq(q, "%d %s" % (w, u), cands, e, rnd)


def set_missing(rnd, P):
    its = []
    for k, (A, L, u) in enumerate([(24, 6, "cm"), (35, 7, "m"), (48, 8, "cm"), (54, 9, "m"), (63, 7, "cm"),
                                   (72, 8, "m")]):
        its.append(missing(A, L, u, True, rnd, k))
    for k, (A, L, u) in enumerate([(96, 8, "cm"), (91, 7, "m"), (150, 10, "cm"), (144, 9, "m")]):
        its.append(missing(A, L, u, False, rnd, k))
    for k, (A, u) in enumerate([(64, "cm"), (100, "m"), (144, "cm")]):
        s = math.isqrt(A)
        q = "A square has an area of %d %s. How long is each side?" % (A, SQ[u])
        e = ("Side × side = %d. %d × %d = %d, so each side is %d %s. (%d ÷ 4 = %d would be the side if %d "
             "were the perimeter.)" % (A, s, s, A, s, u, A, A // 4, A))
        cands = rot(["%d %s" % (A // 4, u), "%d %s" % (A // 2, u), "%d %s" % (A - s, u)], k)
        its.append(mcq(q, "%d %s" % (s, u), cands, e, rnd))
    for k, (Pm, L, u) in enumerate([(30, 9, "cm"), (44, 14, "m"), (50, 15, "cm"), (36, 11, "m")]):
        w2 = Pm - 2 * L
        w = w2 // 2
        assert w2 % 2 == 0 and w > 0 and w != L and len({w, Pm - L, w2, Pm // 2}) == 4
        q = "A rectangle has a perimeter of %d %s. Its length is %d %s. What is its width?" % (Pm, u, L, u)
        e = ("The two lengths use %d + %d = %d %s. That leaves %d − %d = %d %s for the two widths. "
             "%d ÷ 2 = %d %s. Check: %d + %d + %d + %d = %d %s."
             % (L, L, 2 * L, u, Pm, 2 * L, w2, u, w2, w, u, L, w, L, w, Pm, u))
        cands = rot(["%d %s" % (Pm - L, u), "%d %s" % (w2, u), "%d %s" % (Pm // 2, u)], k)
        its.append(mcq(q, "%d %s" % (w, u), cands, e, rnd))
    for k, (tot, rows) in enumerate([(72, 8), (96, 6), (84, 7)]):
        n, he, his = P.next()
        each = tot // rows
        q = ("%s covers a rectangle with %d square tiles, with no gaps. There are %d rows. "
             "How many tiles are in each row?" % (n, tot, rows))
        e = "%d rows × ? = %d. %d ÷ %d = %d tiles in each row. Check: %d × %d = %d." % (
            rows, tot, tot, rows, each, rows, each, tot)
        cands = rot(["%d tiles" % (tot - rows), "%d tiles" % (tot + rows), "%d tiles" % (each + 1)], k)
        its.append(mcq(q, "%d tiles" % each, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing side", "items": its}


# ------------------------------------------------------------ set 5: same area, different perimeter + word problems
def set_story(rnd, P):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    def A(l, w):
        return l * w

    def Pr(l, w):
        return 2 * (l + w)

    # relationships between area and perimeter
    assert A(9, 4) == A(12, 3) == 36 and Pr(9, 4) == 26 and Pr(12, 3) == 30
    add("Both rectangles have an area of 36 cm²: one is 9 cm by 4 cm, the other is 12 cm by 3 cm. "
        "Which has the longer perimeter?", "12 cm by 3 cm", ["9 cm by 4 cm", "They are the same", "You cannot tell"],
        "9 cm by 4 cm: 18 + 8 = 26 cm. 12 cm by 3 cm: 24 + 6 = 30 cm. The same area can have different perimeters.")
    assert Pr(6, 6) == Pr(10, 2) == 24 and A(6, 6) == 36 and A(10, 2) == 20
    add("Both rectangles have a perimeter of 24 m: one is 6 m by 6 m, the other is 10 m by 2 m. "
        "Which has the bigger area?", "6 m by 6 m", ["10 m by 2 m", "They are the same", "You cannot tell"],
        "6 × 6 = 36 m² and 10 × 2 = 20 m². The same perimeter can give very different areas.")
    rects24 = [(a, 24 // a) for a in range(1, 5) if 24 % a == 0]
    assert len(rects24) == 4
    add("How many different rectangles with whole-number sides have an area of 24 cm²? "
        "(A turned rectangle counts as the same one.)", "4", ["8", "3", "1"],
        "1 × 24, 2 × 12, 3 × 8 and 4 × 6: 4 rectangles. Their perimeters are all different: "
        "50, 28, 22 and 20 cm. (8 counts each turned rectangle twice.)")
    opts = [(6, 6), (9, 4), (12, 3), (36, 1)]
    assert all(A(*o) == 36 for o in opts) and min(opts, key=lambda o: Pr(*o)) == (6, 6)
    add("All these rectangles have an area of 36 m². Which has the shortest perimeter?", "6 m by 6 m",
        ["9 m by 4 m", "12 m by 3 m", "36 m by 1 m"],
        "Perimeters: 6 by 6 = 24 m, 9 by 4 = 26 m, 12 by 3 = 30 m, 36 by 1 = 74 m. "
        "For the same area, the closer the shape is to a square, the shorter the perimeter.")
    n, he, his = P.next()
    opts = [(5, 5), (6, 4), (7, 3), (8, 2)]
    assert all(Pr(*o) == 20 for o in opts) and max(opts, key=lambda o: A(*o)) == (5, 5)
    add("%s has 20 m of fence for a rectangular garden. Which garden gives the most area?" % n, "5 m by 5 m",
        ["6 m by 4 m", "7 m by 3 m", "8 m by 2 m"],
        "All use 20 m of fence. Areas: 5 × 5 = 25 m², 6 × 4 = 24 m², 7 × 3 = 21 m², 8 × 2 = 16 m². "
        "The square gives the most area.")
    assert A(12, 8) == 4 * A(6, 4)
    add("A rectangle is 6 cm by 4 cm. Both sides are doubled to 12 cm by 8 cm. What happens to the area?",
        "It is 4 times as big", ["It doubles", "It stays the same", "It grows by 2 cm²"],
        "Old area: 6 × 4 = 24 cm². New area: 12 × 8 = 96 cm². 96 ÷ 24 = 4, so it is 4 times as big. "
        "(The perimeter only doubles: 20 cm to 40 cm.)")
    assert A(6, 3) == Pr(6, 3) == 18 and Pr(9, 2) == 22 and A(5, 4) == 20 and A(7, 2) == 14
    add("Which rectangle has an area of 18 cm² and a perimeter of 18 cm?", "6 cm by 3 cm",
        ["9 cm by 2 cm", "5 cm by 4 cm", "7 cm by 2 cm"],
        "6 × 3 = 18 cm² and 6 + 3 + 6 + 3 = 18 cm. (9 by 2 has a perimeter of 22 cm; "
        "5 by 4 and 7 by 2 have areas of 20 cm² and 14 cm².)")

    # word problems in BC
    n, he, his = P.next()
    assert A(14, 9) == 126 and Pr(14, 9) == 46
    add("%s’s class has a plot at a community garden in Kamloops. It is 14 m long and 9 m wide. "
        "What is its area?" % n, "126 m²", ["46 m²", "23 m²", "126 m"],
        "Area = length × width: 14 × 9 = 126 m². (46 m is the distance around, and 14 + 9 = 23 only adds two sides.)")
    add("A community garden plot in Kamloops is 14 m long and 9 m wide. How much fence goes all the way around it?", "46 m",
        ["126 m", "23 m", "37 m"],
        "A fence goes around the edge: 14 + 9 + 14 + 9 = 46 m. (37 m leaves out one side; 126 m² is the area.)")
    n, he, his = P.next()
    assert A(60, 45) == 2700 and Pr(60, 45) == 210
    add("%s makes a poster for the Terry Fox Run. It is 60 cm long and 45 cm wide. What is its area?" % n,
        "2700 cm²", ["210 cm²", "105 cm²", "2700 cm"],
        "60 × 45: 60 × 40 = 2400 and 60 × 5 = 300. 2400 + 300 = 2700 cm². (210 cm is the perimeter.)")
    assert A(100, 60) == 6000 and Pr(100, 60) == 320
    add("A soccer field in Surrey is 100 m long and 60 m wide. What is its area?", "6000 m²",
        ["320 m²", "160 m²", "600 m²"],
        "100 × 60 = 6000 m². (320 m is the distance around the field; 600 is missing a zero.)")
    assert A(250, 120) == 30000 and Pr(250, 120) == 740
    add("A hay field in the Okanagan is 250 m long and 120 m wide. What is its area?", "30" + NBSP + "000 m²",
        ["740 m²", "3000 m²", "300" + NBSP + "000 m²"],
        "250 × 120: 250 × 100 = 25" + NBSP + "000 and 250 × 20 = 5000. 25" + NBSP + "000 + 5000 = 30" + NBSP +
        "000 m². (740 m is the perimeter.)")
    n, he, his = P.next()
    assert A(8, 6) == 48 and 48 // 12 == 4
    add("%s’s family stains a cedar deck at their cabin in Whistler. The deck is 8 m long and 6 m wide. "
        "One can of stain covers 12 m². How many cans do they need?" % n, "4 cans",
        ["48 cans", "36 cans", "60 cans"],
        "Area of the deck: 8 × 6 = 48 m². Each can covers 12 m²: 48 ÷ 12 = 4 cans.")
    n, he, his = P.next()
    assert 96 // 12 == 8
    add("%s’s rectangular vegetable bed has an area of 96 m². It is 12 m long. How wide is it?" % n, "8 m",
        ["84 m", "8 m²", "24 m"],
        "12 × ? = 96. 96 ÷ 12 = 8, so the bed is 8 m wide. (84 comes from subtracting: 96 − 12.)")
    assert A(6, 5) - 18 == 12
    add("The reading corner is 6 m long and 5 m wide. Each carpet tile covers 1 m². The class has put down "
        "18 tiles. How many more tiles are needed?", "12 tiles", ["30 tiles", "11 tiles", "4 tiles"],
        "Whole corner: 6 × 5 = 30 tiles. Still needed: 30 − 18 = 12 tiles. "
        "(4 uses the perimeter, 22, instead of the area.)")
    n, he, his = P.next()
    assert A(5, 4) - A(3, 2) == 14
    add("%s’s bedroom floor is 5 m by 4 m. A rug 3 m by 2 m lies on it. What area of floor is not covered?" % n,
        "14 m²", ["6 m²", "4 m²", "26 m²"],
        "Floor: 5 × 4 = 20 m². Rug: 3 × 2 = 6 m². 20 − 6 = 14 m². "
        "(4 m² comes from (5 − 3) × (4 − 2), which takes away from the sides instead of the areas.)")
    assert Pr(120, 80) == 400
    add("A class banner for a BC Ferries field trip is 120 cm long and 80 cm wide. Ribbon goes all the way "
        "around the edge. How much ribbon is needed?", "400 cm", ["9600 cm", "200 cm", "320 cm"],
        "Ribbon goes around the edge: 120 + 80 + 120 + 80 = 400 cm. "
        "(200 cm goes only halfway around; 9600 cm² would be the area.)")
    assert 64 // 4 == 16 and 16 * 16 == 256
    add("A square photo frame has a perimeter of 64 cm. What is its area?", "256 cm²",
        ["64 cm²", "16 cm²", "4096 cm²"],
        "Each side: 64 ÷ 4 = 16 cm. Area: 16 × 16 = 256 cm². (4096 uses 64 as the side.)")
    g1, g2 = P.next(), P.next()
    assert Pr(4, 4) == Pr(5, 3) == 16 and A(4, 4) - A(5, 3) == 1
    add("%s’s bedroom is 4 m by 4 m. %s’s bedroom is 5 m by 3 m. Both have a perimeter of 16 m. "
        "Whose bedroom has the bigger area?" % (g1[0], g2[0]),
        "%s’s, by 1 m²" % g1[0], ["%s’s, by 1 m²" % g2[0], "They are the same", "%s’s, by 2 m²" % g1[0]],
        "%s: 4 × 4 = 16 m². %s: 5 × 3 = 15 m². 16 − 15 = 1, so %s’s room is bigger by 1 m². "
        "The same perimeter does not mean the same area." % (g1[0], g2[0], g1[0]))
    assert A(9, 3) - A(2, 1) == 25
    add("Students in Nanaimo paint a mural on a school wall 9 m long and 3 m high. A window 2 m by 1 m "
        "is not painted. What area do they paint?", "25 m²", ["27 m²", "29 m²", "24 m²"],
        "Wall: 9 × 3 = 27 m². Window: 2 × 1 = 2 m². 27 − 2 = 25 m². "
        "(29 adds the window instead of taking it away; 24 m is the perimeter of the wall.)")
    assert len(its) == 20, len(its)
    return {"title": "Same area, different perimeter and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    g1 = grid_svg(5, 3, "rectangle 5 squares by 3 squares on a grid")
    r1 = rect_svg(8, 5, "8 cm", "5 cm", "rectangle 8 cm by 5 cm")
    r2 = rect_svg(8, 6, "8 m", "? m", "rectangle with an area of 48 m² and one side missing",
                  inner="Area = 48 m²")
    tw_ = twin_svg((6, 2), (4, 3), "two rectangles on a grid: A is 6 by 2, B is 4 by 3")
    assert 8 * 5 == 40 and 2 * (8 + 5) == 26 and 48 // 8 == 6
    assert 6 * 2 == 4 * 3 == 12 and 2 * (6 + 2) == 16 and 2 * (4 + 3) == 14
    return (
        "<h2>Area: count the squares</h2>"
        "<p><b>Area</b> is the number of unit squares that cover a shape. In a rectangle, the squares sit in "
        "<b>equal rows</b>, so you can multiply instead of counting one by one.</p>"
        "<figure class='sn-fig'>" + g1 +
        "<figcaption>3 rows of 5 squares: 3 × 5 = 15. The area is 15 square units.</figcaption></figure>"
        "<h2>Area = length × width</h2>"
        "<p>The length tells how many squares fit in each row. The width tells how many rows there are. "
        "So <b>area = length × width</b>. Area is in square units: <b>cm²</b> for small things, "
        "<b>m²</b> for big spaces like a floor, a garden or a field.</p>"
        "<figure class='sn-fig'>" + r1 +
        "<figcaption>Area: 8 × 5 = 40 cm². Perimeter: 8 + 5 + 8 + 5 = 26 cm.</figcaption></figure>" +
        ex("Example", "A rectangle is 24 m long and 6 m wide. What is its area?",
           "24 × 6: 20 × 6 = 120 and 4 × 6 = 24. 120 + 24 = 144.", "144 m²") +
        "<h2>Perimeter: the distance around</h2>"
        "<p><b>Perimeter</b> is the length of the edge. For a rectangle, add two lengths and two widths: "
        "<b>perimeter = 2 × length + 2 × width</b>. Perimeter is a length, so it is in <b>cm</b> or <b>m</b>.</p>" +
        ex("Example", "A rectangle is 15 cm long and 8 cm wide. What is its perimeter?",
           "2 × 15 + 2 × 8 = 30 + 16 = 46.", "46 cm") +
        "<h2>Find a missing side</h2>"
        "<p>Know the <b>area</b>? Divide: missing side = area ÷ known side. "
        "Know the <b>perimeter</b>? Take away the two sides you know, then halve what is left.</p>"
        "<figure class='sn-fig'>" + r2 +
        "<figcaption>8 × ? = 48. 48 ÷ 8 = 6, so the missing side is 6 m.</figcaption></figure>" +
        ex("Example", "A rectangle has a perimeter of 30 cm. Its length is 9 cm. What is its width?",
           "30 − 9 − 9 = 12 cm for the two widths. 12 ÷ 2 = 6.", "6 cm") +
        "<h2>Same area, different perimeter</h2>"
        "<p>Two rectangles can have the <b>same area</b> but <b>different perimeters</b>. "
        "A long, thin rectangle has a longer perimeter than one that is closer to a square.</p>"
        "<figure class='sn-fig'>" + tw_ +
        "<figcaption>A: 6 × 2 = 12 squares, perimeter 16. B: 4 × 3 = 12 squares, perimeter 14.</figcaption></figure>"
        "<p>Carpet, paint and tiles need the area. A fence, a border or ribbon needs the perimeter.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides for the area (8 + 5 = 13)", "Multiply: 8 × 5 = 40 cm²"],
            ["Finding the area when the question asks for the perimeter", "Perimeter goes around: 8 + 5 + 8 + 5 = 26 cm"],
            ["Writing cm for an area, or cm² for a perimeter", "Area: cm² or m². Perimeter: cm or m"],
            ["Adding only one length and one width for the perimeter", "Go all the way around: 2 lengths + 2 widths"],
            ["Subtracting to find a missing side (48 − 8 = 40)", "Divide: 48 ÷ 8 = 6"],
            ["Mixing units (2 m and 60 cm)", "Change to one unit first: 2 m = 200 cm"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about area in the BC math curriculum?",
     "a": "In Geometry and measurement, Grade 5 students measure the area of squares and rectangles in cm² and m², "
          "use area = length × width, and explore how area and perimeter are related."},
    {"q": "How do you find the area and perimeter of a rectangle?",
     "a": "Area = length × width, in square units. Perimeter = 2 × length + 2 × width, in length units. "
          "A rectangle 8 cm by 5 cm has an area of 40 cm² and a perimeter of 26 cm."},
    {"q": "Can two rectangles have the same area but different perimeters?",
     "a": "Yes. A 6 cm by 2 cm rectangle and a 4 cm by 3 cm rectangle both have an area of 12 cm², "
          "but their perimeters are 16 cm and 14 cm."},
    {"q": "What is the difference between cm and cm²?",
     "a": "cm measures a length, such as a side or a perimeter. cm² measures an area: the number of 1 cm by 1 cm "
          "squares that cover a shape."},
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
    rnd = random.Random(55811)
    P = People(rnd)
    sets = [set_count(rnd, P), set_formula(rnd, P), set_perimeter(rnd, P), set_missing(rnd, P), set_story(rnd, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "area-and-perimeter", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Area and Perimeter",
        "seo_title": "Grade 5 Area and Perimeter Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Area and perimeter",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 5: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Area measurement of squares and rectangles",
        "meta_desc": "Free Grade 5 math worksheets on area and perimeter for the BC curriculum: count squares, "
                     "use area = length × width in cm² and m², find perimeters, work out missing sides, compare "
                     "rectangles with the same area, and solve garden and field word problems. 100 questions "
                     "with an answer key.",
        "key_big": "Area = length × width (cm², m²). Perimeter = 2 × length + 2 × width (cm, m).",
        "key_sub": "Area is the space inside; perimeter is the distance around. Missing side = area ÷ known side. "
                   "The same area can have different perimeters.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "[^']*(grid|top row)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
