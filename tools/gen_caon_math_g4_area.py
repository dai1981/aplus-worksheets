# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Area of Rectangles (Ontario Curriculum 2020, Spatial Sense E2.5, E2.6)
  python3 tools/gen_caon_math_g4_area.py
Rows and columns of unit squares (arrays) lead to area = length × width; areas in cm² and m²;
missing side from the area (area ÷ known side); area vs perimeter; word problems (gardens, a backyard rink,
carpet tiles). Wrong choices come from real mistakes (adding the sides, finding the perimeter,
writing cm or m for an area, subtracting instead of dividing). Every answer is worked out in code.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
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


def skip(r, c):
    """'3 rows of 5' -> '5, 10, 15'."""
    return ", ".join(str(c * i) for i in range(1, r + 1))


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
def grid_svg(L, W, label, mode="full", cell=22, margin=1):
    """L × W rectangle of unit squares on a grid with a 1-square margin.
    mode 'full': all squares shaded; 'edge': only the top row and the left column of squares are drawn."""
    m = 4
    if mode == "edge":
        margin = 0
    cols, rows = L + 2 * margin, W + 2 * margin
    Wd, Hd = cols * cell + 2 * m, rows * cell + 2 * m
    g = []
    x0, y0 = m + margin * cell, m + margin * cell
    if mode == "full":
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, L * cell, W * cell, FILL))
        for i in range(cols + 1):
            g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (m + i * cell, m, m + i * cell, m + rows * cell, GRIDC))
        for j in range(rows + 1):
            g.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (m, m + j * cell, m + cols * cell, m + j * cell, GRIDC))
    else:
        g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (x0, y0, L * cell, W * cell))
        cells = {(c, 0) for c in range(L)} | {(0, r) for r in range(W)}
        for (c, r) in sorted(cells):
            g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x0 + c * cell, y0 + r * cell, cell, cell, FILL, GREEN))
    g.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0, y0, L * cell, W * cell, GREEN if mode == "full" else INK))
    return svg_wrap(Wd, Hd, "".join(g), label)


# ------------------------------------------------------------ set 1: rows and columns of squares
def set_arrays(rnd, P):
    its = []
    # count the squares on a grid
    for k, (L, W, un) in enumerate([(5, 3, "square units"), (6, 4, "square units"), (7, 3, "cm²"),
                                    (8, 4, "cm²"), (6, 5, "cm²"), (9, 3, "square units")]):
        A, Pm, bd = L * W, 2 * (L + W), 2 * (L + W) - 4
        assert len({A, Pm, bd, L + W}) == 4
        svg = grid_svg(L, W, "rectangle %d squares by %d squares on a grid" % (L, W))
        if un == "cm²":
            q = fig(svg) + "Each square is 1 cm². What is the area of the shaded rectangle?"
            cands = rot(["%d cm²" % Pm, "%d cm²" % bd, "%d cm²" % (L + W)], k) + ["%d cm" % A]
        else:
            q = fig(svg) + "What is the area of the shaded rectangle in square units?"
            cands = rot(["%d square units" % Pm, "%d square units" % bd, "%d square units" % (L + W)], k)
        e = ("There are %d rows with %d squares in each row: %d × %d = %d. The area is %d %s. "
             "(%d is the distance around the edge, the perimeter.)" % (W, L, W, L, A, A, un, Pm))
        its.append(mcq(q, "%d %s" % (A, un), cands, e, rnd))
    # which multiplication matches the array
    for k, (L, W) in enumerate([(6, 3), (7, 4), (5, 4), (8, 3)]):
        svg = grid_svg(L, W, "rectangle %d squares by %d squares on a grid" % (L, W))
        q = fig(svg) + "Which multiplication gives the number of squares in this rectangle?"
        e = "There are %d rows of %d squares. %d × %d = %d squares." % (W, L, W, L, W * L)
        cands = rot(["%d + %d" % (W, L), "%d × %d" % (W - 1, L), "%d × %d" % (W, L + 1)], k)
        its.append(mcq(q, "%d × %d" % (W, L), cands, e, rnd))
    # only the top row and the left column are drawn
    for k, (L, W) in enumerate([(6, 4), (7, 3), (8, 5), (9, 4)]):
        A, shown = L * W, L + W - 1
        svg = grid_svg(L, W, "rectangle with only the top row and left column of squares drawn", "edge")
        q = (fig(svg) + "Only the top row and the left column of squares are drawn. "
             "How many squares would cover the whole rectangle?")
        e = ("The top row shows %d squares in each row. The left column shows %d rows. "
             "%d × %d = %d squares." % (L, W, W, L, A))
        cands = rot(["%d squares" % shown, "%d squares" % (L + W), "%d squares" % (2 * (L + W))], k)
        its.append(mcq(q, "%d squares" % A, cands, e, rnd))
    # arrays in words
    for k, (r, c, un) in enumerate([(4, 7, "cm"), (6, 8, "m"), (3, 9, "cm")]):
        A = r * c
        q = ("A rectangle is covered by %d rows of 1 %s² squares. There are %d squares in each row. "
             "What is its area?" % (r, un, c))
        e = "%d rows of %d squares: %d × %d = %d squares, so the area is %d %s." % (r, c, r, c, A, A, SQ[un])
        cands = rot(["%d %s" % (r + c, SQ[un]), "%d %s" % (2 * (r + c), SQ[un])], k) + ["%d %s" % (A, un)]
        its.append(mcq(q, "%d %s" % (A, SQ[un]), cands, e, rnd))
    # ideas
    its.append(mcq("Why can you multiply to find the number of squares in a rectangle?",
                   "Every row has the same number",
                   ["The rows get longer and longer", "Squares can overlap", "You only count the edge"],
                   "In a rectangle, the squares sit in equal rows. Equal groups can be multiplied: "
                   "number of rows × squares in each row.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s counts the squares in a rectangle one by one: 5 rows of 8 squares, 40 in all. "
                   "Which faster way gives the same answer?" % n, "5 × 8",
                   ["5 + 8", "8 + 8", "2 × 5 + 2 × 8"],
                   "5 rows of 8 squares: 5 × 8 = 40. (5 + 8 = 13 adds a row and a column. "
                   "2 × 5 + 2 × 8 = 26 is the perimeter.)", rnd))
    its.append(mcq("Rectangle A has 3 rows of 8 squares. Rectangle B has 8 rows of 3 squares. "
                   "Which is true?", "Both have 24 squares",
                   ["A has more squares", "B has more squares", "Both have 11 squares"],
                   "3 × 8 = 24 and 8 × 3 = 24. Turning a rectangle does not change its area.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Count squares in rows and columns", "items": its}


# ------------------------------------------------------------ set 2: area = length × width
def set_formula(rnd, P):
    its = []
    for i, (L, W, u) in enumerate([(8, 5, "cm"), (9, 4, "m"), (7, 6, "cm"), (12, 3, "m"), (10, 7, "cm"),
                                   (11, 4, "m")]):
        A, Pm = L * W, 2 * (L + W)
        assert A != Pm
        q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))) +
             "What is the area of this rectangle?")
        e = "Area = length × width: %d × %d = %d %s. (%d %s is the perimeter.)" % (L, W, A, SQ[u], Pm, u)
        cands = rot(["%d %s" % (Pm, SQ[u]), "%d %s" % (L + W, SQ[u]), "%d %s" % (A, u)], i)
        its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
    for i, (L, W, u) in enumerate([(14, 5, "cm"), (23, 4, "m"), (16, 6, "cm"), (25, 3, "m"), (18, 7, "cm"),
                                   (32, 2, "m")]):
        A, Pm = L * W, 2 * (L + W)
        t, o = divmod(L, 10)
        part = t * 10 * W + o            # forgot to multiply the ones
        assert A != Pm and part != A
        q = "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
        e = ("Area = length × width: %d × %d. Split %d into %d + %d: %d × %d = %d and %d × %d = %d. "
             "%d + %d = %d %s." % (L, W, L, t * 10, o, t * 10, W, t * 10 * W, o, W, o * W,
                                   t * 10 * W, o * W, A, SQ[u]))
        cands = rot(["%d %s" % (part, SQ[u]), "%d %s" % (Pm, SQ[u]), "%d %s" % (L + W, SQ[u])], i) + \
            ["%d %s" % (A, u)]
        its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
    for k, (s, u) in enumerate([(9, "cm"), (11, "m")]):
        A = s * s
        if k == 0:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "%d %s" % (s, u), "square with %d %s sides" % (s, u))) +
                 "This is a square. What is its area?")
        else:
            q = "A square has sides of %d %s. What is its area?" % (s, u)
        e = "The length and width of a square are the same: %d × %d = %d %s." % (s, s, A, SQ[u])
        cands = ["%d %s" % (4 * s, SQ[u]), "%d %s" % (2 * s, SQ[u]), "%d %s" % (A, u)]
        its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
    U4 = ["cm", "m", "cm²", "m²"]
    for thing, right, why in [
        ("the area of a backyard skating rink", "m²", "A rink is big and area is the space inside, so use square metres."),
        ("the area of a hockey card", "cm²", "A hockey card is small and area is the space inside, so use square centimetres."),
        ("the area of a classroom floor", "m²", "A floor is big and area is the space inside, so use square metres."),
    ]:
        its.append(mcq("Which unit is best for measuring %s?" % thing, right, [x for x in U4 if x != right],
                       why + " cm and m measure length; cm² and m² measure area.", rnd))
    its.append(mcq("Rectangle A is 6 cm by 4 cm. Rectangle B is 8 cm by 3 cm. Which has the bigger area?",
                   "They are the same", ["Rectangle A", "Rectangle B", "You cannot tell"],
                   "A: 6 × 4 = 24 cm². B: 8 × 3 = 24 cm². The areas are the same, even though the shapes "
                   "look different.", rnd))
    its.append(mcq("Rectangle A is 9 m by 5 m. Rectangle B is 7 m by 7 m. Which has the bigger area?",
                   "Rectangle B, by 4 m²", ["Rectangle A, by 4 m²", "They are the same", "Rectangle B, by 2 m²"],
                   "A: 9 × 5 = 45 m². B: 7 × 7 = 49 m². 49 − 45 = 4, so B is bigger by 4 m². "
                   "(9 + 5 and 7 + 7 are both 14, but adding the sides does not give the area.)", rnd))
    its.append(mcq("Which rule gives the area of a rectangle?", "length × width",
                   ["length + width", "length + width + length + width", "length × 4"],
                   "Area counts the squares inside: rows × squares in each row, which is length × width. "
                   "Adding all four sides gives the perimeter.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area = length × width (cm² and m²)", "items": its}


# ------------------------------------------------------------ set 3: missing side
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
    for k, (A, L, u) in enumerate([(24, 6, "cm"), (35, 7, "m"), (48, 8, "cm"), (36, 9, "m"), (54, 6, "cm"),
                                   (40, 8, "m")]):
        its.append(missing(A, L, u, True, rnd, k))
    for k, (A, L, u) in enumerate([(42, 7, "cm"), (45, 9, "m"), (56, 8, "cm"), (60, 10, "m"), (72, 9, "cm"),
                                   (84, 7, "m")]):
        its.append(missing(A, L, u, False, rnd, k))
    for k, (A, u) in enumerate([(36, "cm"), (64, "m"), (100, "cm")]):
        s = math.isqrt(A)
        q = "A square has an area of %d %s. How long is each side?" % (A, SQ[u])
        e = ("Side × side = %d. %d × %d = %d, so each side is %d %s. (%d ÷ 4 = %d would be the side if %d "
             "were the perimeter.)" % (A, s, s, A, s, u, A, A // 4, A))
        cands = rot(["%d %s" % (A // 4, u), "%d %s" % (A // 2, u), "%d %s" % (A - s, u)], k)
        its.append(mcq(q, "%d %s" % (s, u), cands, e, rnd))
    its.append(mcq("A rectangle has an area of 24 cm². Which could be its side lengths?", "6 cm and 4 cm",
                   ["12 cm and 12 cm", "20 cm and 4 cm", "10 cm and 2 cm"],
                   "Area = length × width: 6 × 4 = 24 cm². 12 + 12 and 20 + 4 add to 24 instead. "
                   "10 cm and 2 cm give a perimeter of 24 cm, not an area of 24 cm².", rnd))
    its.append(mcq("A rectangle has an area of 36 m². Which could be its side lengths?", "9 m and 4 m",
                   ["30 m and 6 m", "18 m and 18 m", "10 m and 8 m"],
                   "9 × 4 = 36 m². 30 + 6 and 18 + 18 add to 36 instead. "
                   "10 m and 8 m give a perimeter of 36 m.", rnd))
    for k, (tot, rows) in enumerate([(42, 6), (40, 5), (63, 7)]):
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


# ------------------------------------------------------------ set 4: area vs perimeter
def set_versus(rnd, P):
    its = []
    for i, (L, W, u) in enumerate([(7, 4, "cm"), (8, 3, "m"), (9, 5, "cm"), (6, 2, "m"), (10, 4, "cm"),
                                   (12, 5, "m"), (8, 7, "cm"), (9, 2, "m")]):
        A, Pm = L * W, 2 * (L + W)
        assert A != Pm
        svg = rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d %s by %d %s" % (L, u, W, u))
        if i % 2 == 0:
            q = fig(svg) + "What is the <b>area</b> of this rectangle?"
            e = ("Area is the space inside: %d × %d = %d %s. The perimeter would be %d + %d + %d + %d = %d %s."
                 % (L, W, A, SQ[u], L, W, L, W, Pm, u))
            cands = rot(["%d %s" % (Pm, SQ[u]), "%d %s" % (L + W, SQ[u]), "%d %s" % (A, u)], i // 2)
            its.append(mcq(q, "%d %s" % (A, SQ[u]), cands, e, rnd))
        else:
            q = fig(svg) + "What is the <b>perimeter</b> of this rectangle?"
            e = ("Perimeter is the distance around: %d + %d + %d + %d = %d %s. (%d × %d = %d %s is the area.)"
                 % (L, W, L, W, Pm, u, L, W, A, SQ[u]))
            cands = rot(["%d %s" % (A, u), "%d %s" % (L + W, u), "%d %s" % (Pm, SQ[u])], i // 2)
            its.append(mcq(q, "%d %s" % (Pm, u), cands, e, rnd))
    for (L, W) in [(5, 3), (6, 4)]:
        A, Pm = L * W, 2 * (L + W)
        svg = grid_svg(L, W, "rectangle %d squares by %d squares on a centimetre grid" % (L, W))
        q = fig(svg) + "Each square is 1 cm by 1 cm. What are the area and the perimeter of the rectangle?"
        e = ("Area: %d rows of %d squares, %d × %d = %d cm². Perimeter: %d + %d + %d + %d = %d cm."
             % (W, L, W, L, A, L, W, L, W, Pm))
        right = "Area %d cm², perimeter %d cm" % (A, Pm)
        cands = ["Area %d cm², perimeter %d cm" % (Pm, A), "Area %d cm, perimeter %d cm²" % (A, Pm),
                 "Area %d cm², perimeter %d cm" % (L + W, Pm)]
        its.append(mcq(q, right, cands, e, rnd))
    CH = ["Area, in m²", "Perimeter, in m", "Area, in m", "Perimeter, in m²"]
    CHc = ["Area, in cm²", "Perimeter, in cm", "Area, in cm", "Perimeter, in cm²"]
    for job, right, ch, why in [
        ("put a fence around %s vegetable garden", 1, CH, "A fence goes around the edge, so find the perimeter. "
         "It is a length, in metres."),
        ("buy carpet to cover %s bedroom floor", 0, CH, "Carpet covers the space inside, so find the area. "
         "A floor is big, so use square metres."),
        ("glue ribbon around the edge of %s card", 1, CHc, "Ribbon goes around the edge, so find the perimeter. "
         "A card is small, so use centimetres."),
        ("cover the front of %s notebook with stickers", 0, CHc, "Stickers cover the space inside, so find the "
         "area. A notebook is small, so use square centimetres."),
    ]:
        n, he, his = P.next()
        q = "%s wants to %s. What should %s find?" % (n, job % his, he)
        its.append(mcq(q, ch[right], [x for x in ch if x != ch[right]], why, rnd))
    its.append(mcq("Both rectangles have an area of 24 cm²: one is 6 cm by 4 cm, the other is 8 cm by 3 cm. "
                   "Which has the longer perimeter?", "8 cm by 3 cm",
                   ["6 cm by 4 cm", "They are the same", "You cannot tell"],
                   "6 cm by 4 cm: 6 + 4 + 6 + 4 = 20 cm. 8 cm by 3 cm: 8 + 3 + 8 + 3 = 22 cm. "
                   "The same area can have different perimeters.", rnd))
    its.append(mcq("Both rectangles have a perimeter of 20 m: one is 6 m by 4 m, the other is 9 m by 1 m. "
                   "Which has the bigger area?", "6 m by 4 m",
                   ["9 m by 1 m", "They are the same", "You cannot tell"],
                   "6 × 4 = 24 m² and 9 × 1 = 9 m². The same perimeter can give very different areas.", rnd))
    its.append(mcq("Which rectangle has an area of 12 cm² and a perimeter of 14 cm?", "4 cm by 3 cm",
                   ["6 cm by 2 cm", "5 cm by 2 cm", "12 cm by 1 cm"],
                   "4 × 3 = 12 cm² and 4 + 3 + 4 + 3 = 14 cm. (6 by 2 has a perimeter of 16 cm; "
                   "5 by 2 has an area of 10 cm².)", rnd))
    its.append(mcq("Which rectangle has an area of 16 m² and a perimeter of 16 m?", "4 m by 4 m",
                   ["8 m by 2 m", "6 m by 2 m", "5 m by 3 m"],
                   "4 × 4 = 16 m² and 4 + 4 + 4 + 4 = 16 m. (8 by 2 has a perimeter of 20 m; "
                   "6 by 2 and 5 by 3 have areas of 12 m² and 15 m².)", rnd))
    its.append(mcq("A square has a perimeter of 20 cm. What is its area?", "25 cm²",
                   ["20 cm²", "400 cm²", "5 cm²"],
                   "4 equal sides make 20 cm, so each side is 20 ÷ 4 = 5 cm. Area = 5 × 5 = 25 cm². "
                   "(400 uses 20 as the side.)", rnd))
    its.append(mcq("A rectangle has an area of 24 m² and a length of 8 m. What is its perimeter?", "22 m",
                   ["11 m", "19 m", "24 m"],
                   "First find the width: 24 ÷ 8 = 3 m. Then the perimeter: 8 + 3 + 8 + 3 = 22 m. "
                   "(11 m adds only one length and one width.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Area or perimeter?", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    n, he, his = P.next()
    add("%s’s family floods a backyard rink that is 12 m long and 7 m wide. What is the area of the ice?" % n,
        "84 m²", ["38 m²", "19 m²", "84 m"],
        "Area = length × width: 12 × 7 = 84 m². (12 + 7 + 12 + 7 = 38 m is the distance around.)")
    add("A backyard rink is 12 m long and 7 m wide. Boards go all the way around it. How many metres of boards "
        "are needed?", "38 m", ["84 m", "19 m", "31 m"],
        "Boards go around the edge, so find the perimeter: 12 + 7 + 12 + 7 = 38 m. "
        "(31 m leaves out one side.)")
    n, he, his = P.next()
    add("%s’s class plants a vegetable garden 6 m long and 4 m wide. What is the area of the garden?" % n,
        "24 m²", ["10 m²", "20 m²", "24 m"],
        "6 × 4 = 24 m². (6 + 4 = 10 adds the sides, and 20 m is the perimeter.)")
    add("A garden is 6 m long and 4 m wide. How much fence goes all the way around it?", "20 m",
        ["24 m", "10 m", "24 m²"],
        "A fence goes around the edge: 6 + 4 + 6 + 4 = 20 m. (24 m² is the area.)")
    n, he, his = P.next()
    add("%s’s garden has an area of 32 m². It is 8 m long. How wide is it?" % n, "4 m",
        ["24 m", "8 m", "4 m²"],
        "8 × ? = 32. 32 ÷ 8 = 4, so the garden is 4 m wide. (24 comes from subtracting: 32 − 8.)")
    add("The reading corner is 5 m long and 3 m wide. Each carpet tile covers 1 m². How many tiles cover it?",
        "15 tiles", ["8 tiles", "16 tiles", "20 tiles"],
        "3 rows of 5 tiles: 3 × 5 = 15 tiles. (5 + 3 = 8 adds the sides, and 16 m is the perimeter.)")
    add("The teacher has 30 carpet tiles. The circle-time carpet needs 4 rows of 6 tiles. How many tiles are "
        "left over?", "6 tiles", ["24 tiles", "20 tiles", "10 tiles"],
        "Carpet: 4 × 6 = 24 tiles. Left over: 30 − 24 = 6 tiles. (20 comes from 30 − 4 − 6.)")
    n, he, his = P.next()
    add("%s makes a poster for the Terry Fox Run. It is 50 cm long and 30 cm wide. What is its area?" % n,
        "1500 cm²", ["150 cm²", "160 cm²", "80 cm²"],
        "50 × 30: 5 × 3 = 15, then add the two zeros: 1500 cm². (160 cm is the perimeter; 80 adds the sides.)")
    add("A quilt is made of squares in 8 rows with 7 squares in each row. How many squares are in the quilt?",
        "56 squares", ["15 squares", "26 squares", "49 squares"],
        "8 rows of 7: 8 × 7 = 56 squares. (26 counts only the squares around the edge.)")
    g1, g2 = P.next(), P.next()
    add("%s’s garden is 7 m by 5 m. %s’s garden is 6 m by 6 m. Whose garden has the bigger area?" % (g1[0], g2[0]),
        "%s’s, by 1 m²" % g2[0], ["%s’s, by 1 m²" % g1[0], "They are the same", "%s’s, by 2 m²" % g2[0]],
        "%s: 7 × 5 = 35 m². %s: 6 × 6 = 36 m². 36 − 35 = 1, so %s’s garden is bigger by 1 m². "
        "(7 + 5 and 6 + 6 are both 12, but adding the sides does not give the area.)" % (g1[0], g2[0], g2[0]))
    add("On a snow day, the class marks out a snow fort 5 m long and 5 m wide. What is its area?", "25 m²",
        ["20 m²", "10 m²", "25 m"],
        "5 × 5 = 25 m². (20 m is the distance around, and area is in m², not m.)")
    add("The school has two sandboxes. Each one is 3 m long and 2 m wide. What is the total area of the sandboxes?",
        "12 m²", ["6 m²", "10 m²", "20 m²"],
        "One sandbox: 3 × 2 = 6 m². Two sandboxes: 6 + 6 = 12 m². (10 m is the perimeter of one sandbox.)")
    add("Each gym mat is 2 m long and 1 m wide. The class lays 9 mats on the floor with no gaps or overlaps. "
        "What area do the mats cover?", "18 m²", ["11 m²", "27 m²", "12 m²"],
        "One mat: 2 × 1 = 2 m². 9 mats: 9 × 2 = 18 m². (27 comes from 9 × 3, adding 2 + 1 first.)")
    n, he, his = P.next()
    add("%s paints a garage wall that is 5 m long and 3 m high. One can of paint covers 5 m². How many cans does %s need?"
        % (n, he), "3 cans", ["15 cans", "10 cans", "8 cans"],
        "Area of the wall: 5 × 3 = 15 m². Each can covers 5 m²: 15 ÷ 5 = 3 cans.")
    add("A rectangular garden has an area of 40 m². It is 5 m wide. How much fence goes all the way around it?",
        "26 m", ["13 m", "40 m", "18 m"],
        "Length: 40 ÷ 5 = 8 m. Fence: 8 + 5 + 8 + 5 = 26 m. (13 m adds only one length and one width; "
        "18 m adds the width twice and the length once.)")
    add("A classroom floor is 9 m long and 8 m wide. What is its area?", "72 m²", ["34 m²", "17 m²", "72 m"],
        "9 × 8 = 72 m². Area is in square metres. (34 m is the perimeter.)")
    n, he, his = P.next()
    add("%s makes a bookmark 18 cm long and 5 cm wide. What is its area?" % n, "90 cm²",
        ["46 cm²", "23 cm²", "58 cm²"],
        "18 × 5: 10 × 5 = 50 and 8 × 5 = 40, so 50 + 40 = 90 cm². (58 comes from 10 × 5 + 8, "
        "forgetting to multiply the 8.)")
    n, he, his = P.next()
    add("%s’s bedroom floor is 4 m by 3 m. A rug 2 m by 2 m lies on it. What area of floor is not covered?" % n,
        "8 m²", ["4 m²", "2 m²", "16 m²"],
        "Floor: 4 × 3 = 12 m². Rug: 2 × 2 = 4 m². 12 − 4 = 8 m². "
        "(2 m² comes from (4 − 2) × (3 − 2), which takes away from the sides instead of the areas.)")
    add("A banner for Canada Day is 4 m long and 1 m wide. What area of cloth is needed to make it?", "4 m²",
        ["10 m²", "5 m²", "4 m"],
        "4 × 1 = 4 m². (10 m is the distance around the banner, and 4 + 1 = 5 adds the sides.)")
    n, he, his = P.next()
    add("%s covers a table 9 tiles long and 6 tiles wide with square tiles. %s has put down 30 tiles. "
        "How many more tiles does %s need?" % (n, cap(he), he), "24 tiles",
        ["54 tiles", "15 tiles", "84 tiles"],
        "Whole table: 9 × 6 = 54 tiles. Still needed: 54 − 30 = 24 tiles.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: gardens, rinks and floors", "items": its}


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
    g2 = grid_svg(6, 4, "rectangle with only the top row and left column of squares drawn", "edge")
    r1 = rect_svg(8, 5, "8 cm", "5 cm", "rectangle 8 cm by 5 cm")
    r2 = rect_svg(8, 6, "8 m", "? m", "rectangle with an area of 48 m² and one side missing",
                  inner="Area = 48 m²")
    assert 8 * 5 == 40 and 2 * (8 + 5) == 26 and 48 // 8 == 6
    return (
        "<h2>Rows and columns of squares</h2>"
        "<p><b>Area</b> is the number of unit squares that cover a shape. In a rectangle, the squares sit in "
        "<b>equal rows</b>. So you do not need to count them one by one: multiply.</p>"
        "<figure class='sn-fig'>" + g1 +
        "<figcaption>3 rows of 5 squares: 3 × 5 = 15. The area is 15 square units.</figcaption></figure>"
        "<p>You only need one row and one column to know how many squares fit.</p>"
        "<figure class='sn-fig'>" + g2 +
        "<figcaption>6 squares fit in a row and there are 4 rows: 4 × 6 = 24 squares.</figcaption></figure>"
        "<h2>Area = length × width</h2>"
        "<p>The length tells how many squares are in each row. The width tells how many rows there are. "
        "So <b>area = length × width</b>. Area is written in square units: <b>cm²</b> for small things, "
        "<b>m²</b> for big spaces like a floor, a garden or a rink.</p>"
        "<figure class='sn-fig'>" + r1 +
        "<figcaption>8 × 5 = 40 cm².</figcaption></figure>" +
        ex("Example", "A rectangle is 14 m long and 5 m wide. What is its area?",
           "14 × 5: 10 × 5 = 50 and 4 × 5 = 20. 50 + 20 = 70.", "70 m²") +
        "<h2>Find a missing side</h2>"
        "<p>If you know the area and one side, ask: what times this side gives the area? "
        "Divide: <b>missing side = area ÷ known side</b>.</p>"
        "<figure class='sn-fig'>" + r2 +
        "<figcaption>8 × ? = 48. 48 ÷ 8 = 6, so the missing side is 6 m. Check: 8 × 6 = 48.</figcaption></figure>"
        "<h2>Area or perimeter?</h2>"
        "<p><b>Area</b> is the space inside (cm², m²). <b>Perimeter</b> is the distance around the edge (cm, m). "
        "Carpet, paint and tiles need the area. A fence, a border or rink boards need the perimeter.</p>" +
        table(["Rectangle 8 cm by 5 cm", "How", "Answer"], [
            ["Area", "8 × 5", "40 cm²"],
            ["Perimeter", "8 + 5 + 8 + 5", "26 cm"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides (8 + 5 = 13)", "Multiply: 8 × 5 = 40 cm²"],
            ["Finding the perimeter (8 + 5 + 8 + 5 = 26)", "That is the distance around. Area is the space inside"],
            ["Writing cm or m for an area", "Area is in square units: cm² or m²"],
            ["Subtracting to find a missing side (48 − 8 = 40)", "Divide: 48 ÷ 8 = 6"],
            ["Counting only the squares you can see", "Use rows × squares in each row"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about area in the Ontario math curriculum?",
     "a": "They use the rows and columns of unit squares in a rectangle to see that area = length × width, find areas in cm² and m², and work out a missing side length when they know the area."},
    {"q": "How do you explain area = length × width to a child?",
     "a": "Cover the rectangle with 1 cm squares. The squares make equal rows, so the number of rows times the squares in each row gives the area, which is width × length."},
    {"q": "How do you find a missing side if you know the area?",
     "a": "Divide the area by the side you know. For example, a rectangle with an area of 48 m² and a length of 8 m is 48 ÷ 8 = 6 m wide."},
    {"q": "What is the difference between area and perimeter?",
     "a": "Area is the space inside a shape, measured in square units such as cm² or m². Perimeter is the distance around the outside, measured in cm or m."},
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
    rnd = random.Random(44817)
    P = People(rnd)
    sets = [set_arrays(rnd, P), set_formula(rnd, P), set_missing(rnd, P), set_versus(rnd, P), set_story(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "area-of-rectangles", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Area of Rectangles",
        "seo_title": "Grade 4 Area of Rectangles Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Area of rectangles",
        "domain": "Spatial Sense",
        "standard_code": "Grade 4: E2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the row and column structure of an array to measure the areas of rectangles and to show that the area of any rectangle can be found by multiplying its side lengths",
        "meta_desc": "Free Grade 4 area of rectangles worksheets for the Ontario math curriculum (E2.5, E2.6): count squares in rows and columns, use area = length × width in cm² and m², find a missing side, tell area from perimeter, and solve garden and rink problems. 100 questions with an answer key.",
        "key_big": "Area of a rectangle = length × width.",
        "key_sub": "The squares sit in equal rows, so multiply instead of counting. Missing side = area ÷ known side. Area is in cm² or m²; perimeter is in cm or m.",
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
