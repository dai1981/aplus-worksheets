# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Properties of Multiplication (3.OA.B.5)
  python tools/gen_us_math_g3_properties.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"

COM = "commutative property"
ASSOC = "associative property"
DIST = "distributive property"
IDEN = "identity property of multiplication"
ZERO = "zero property of multiplication"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no negative numbers). 0 is allowed (zero property)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-"):
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


def dots(x0, y0, rows, cols, s, color=GREEN):
    r = max(4, int(s * 0.32))
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (x0 + c * s + s // 2, y0 + j * s + s // 2, r, color)
                   for j in range(rows) for c in range(cols))


def array_svg(rows, cols, s=22):
    W, H = cols * s + 12, rows * s + 12
    return svg_wrap(W, H, dots(6, 6, rows, cols, s), "array of %d rows and %d columns" % (rows, cols))


def turn_svg(rows, cols, s=18):
    """An array and the same array turned on its side, with = between them."""
    gap = 40
    h1, h2 = rows * s, cols * s
    H = max(h1, h2) + 12
    x2 = 6 + cols * s + gap
    W = x2 + rows * s + 6
    body = (dots(6, 6 + (H - 12 - h1) // 2, rows, cols, s) + dots(x2, 6 + (H - 12 - h2) // 2, cols, rows, s, BLUE) +
            "<text x='%d' y='%d' font-size='26' font-weight='700' fill='%s' text-anchor='middle'>=</text>"
            % (6 + cols * s + gap // 2, H // 2 + 9, INK))
    return svg_wrap(W, H, body, "array of %d rows of %d and the same array turned: %d rows of %d" % (rows, cols, cols, rows))


def split_svg(rows, a, b, s=18):
    """rows x (a + b) array split by a dashed line after column a. Labels sit outside: rows on the left,
    a and b above their parts with a bracket."""
    LP, TP, G = 24, 30, 12
    x1, x2 = LP, LP + a * s + G
    W, H = x2 + b * s + 6, TP + rows * s + 6
    sx = LP + a * s + G // 2
    out = [dots(x1, TP, rows, a, s), dots(x2, TP, rows, b, s, BLUE),
           "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5' stroke-dasharray='6 4'/>"
           % (sx, TP - 4, sx, TP + rows * s + 4, RED)]
    for x0, n, col in [(x1, a, GREEN), (x2, b, BLUE)]:
        w = n * s
        out.append("<path d='M%d %d v-6 h%d v6' fill='none' stroke='%s' stroke-width='2'/>" % (x0 + 2, TP - 2, w - 4, col))
        out.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                   % (x0 + w // 2, TP - 12, col, n))
    out.append("<path d='M%d %d h-6 v%d h6' fill='none' stroke='%s' stroke-width='2'/>" % (LP - 2, TP + 2, rows * s - 4, INK))
    out.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
               % (LP - 16, TP + rows * s // 2 + 6, INK, rows))
    return svg_wrap(W, H, "".join(out), "array of %d rows of %d split into %d and %d columns" % (rows, a + b, a, b))


def par(r, a, b):
    """(r × a) + (r × b), the way the standard writes it."""
    return "(%d × %d) + (%d × %d)" % (r, a, r, b)


# ------------------------------------------------------------ sets
def set_commutative(rnd):
    its = []
    pairs = [(r, c) for r in range(2, 7) for c in range(3, 9) if r < c]
    rnd.shuffle(pairs)
    # 6: one array, two multiplications
    for i, (r, c) in enumerate(pairs[:6]):
        if i % 2:
            r, c = c, r                                # some arrays are tall
        its.append(mcq(fig(array_svg(r, c)) + "Which two multiplications both describe this array?",
                       "%d × %d and %d × %d" % (r, c, c, r),
                       ["Only %d × %d" % (r, c), "%d × %d and %d + %d" % (r, c, r, c), "%d + %d and %d + %d" % (r, c, c, r)],
                       "%d rows of %d is %d × %d. Read it by columns and it is %d groups of %d, which is %d × %d. "
                       "Both equal %d." % (r, c, r, c, c, r, c, r, r * c), rnd))
    # 4: an array and the same array turned
    for r, c in pairs[6:10]:
        its.append(mcq(fig(turn_svg(r, c)) + "The second array is the first one turned on its side. Which equation do the two arrays show?",
                       "%d × %d = %d × %d" % (r, c, c, r),
                       ["%d × %d < %d × %d" % (r, c, c, r), "%d × %d = %d + %d" % (r, c, r, c), "%d + %d = %d + %d" % (r, c, c, r)],
                       "Turning an array does not add or remove any dots. Both have %d dots, so %d × %d = %d × %d. "
                       "This is the commutative property." % (r * c, r, c, c, r), rnd))
    # 6: missing factor
    B = "<b>?</b>"
    for x, y, q in [(7, 3, "7 × %s = 3 × 7"), (4, 9, "%s × 4 = 4 × 9"), (6, 8, "6 × 8 = 8 × %s"),
                    (9, 2, "2 × 9 = %s × 2"), (5, 7, "5 × %s = 7 × 5"), (8, 4, "%s × 8 = 8 × 4")]:
        q = q % B
        ans = x if q.count(str(x)) == 1 else y         # the factor that appears only once is missing
        other = y if ans == x else x
        its.append(mcq("Find the missing number: " + q, ans,
                       [other, x * y, x + y, abs(x - y)],
                       "The same two factors give the same product in any order. Both sides use %d and %d, "
                       "so the missing number is %d (%d × %d = %d)." % (x, y, ans, x, y, x * y), rnd))
    # 2: know one fact, know its turn-around
    for x, y in [(6, 8), (9, 4)]:
        p = x * y
        its.append(mcq("You know that %d × %d = %d. What is %d × %d?" % (x, y, p, y, x), p,
                       [x + y, y * (x - 1), y * (x + 1)],
                       "%d × %d is the same fact turned around, so it is also %d. No new work needed." % (y, x, p), rnd))
    # 2: the property is only for multiplication (and addition), not subtraction or division
    for x, y, dv in [(5, 9, "12 ÷ 3 = 3 ÷ 12"), (4, 7, "10 ÷ 2 = 2 ÷ 10")]:
        its.append(mcq("Which equation is true?", "%d × %d = %d × %d" % (x, y, y, x),
                       ["%d − %d = %d − %d" % (y, x, x, y), dv, "%d × %d = %d + %d" % (x, y, x, y)],
                       "You can switch the factors in multiplication: %d × %d = %d × %d = %d. Switching does not work "
                       "for subtraction or division: %d − %d is not the same as %d − %d, and %s is false." % (x, y, y, x, x * y, y, x, x, y, dv), rnd))
    return {"title": "Commutative property: turn the array", "items": its}


def set_one_zero(rnd):
    its = []
    for n, rev in [(8, False), (6, True), (10, False), (3, True)]:   # × 1
        q = "1 × %d" % n if rev else "%d × 1" % n
        its.append(mcq("What is %s?" % q, n, [1, n + 1, 0],
                       "Any number times 1 is that same number. %s = %d. (1 group of %d, or %d groups of 1.)"
                       % (q, n, n, n), rnd))
    for n, rev in [(7, True), (9, False), (5, False), (4, True)]:   # × 0
        q = "0 × %d" % n if rev else "%d × 0" % n
        its.append(mcq("What is %s?" % q, 0, [n, 1, n * 10],
                       "Any number times 0 is 0. %s means %s, so there is nothing at all. "
                       "(Writing a 0 after the number is the rule for × 10, not × 0.)"
                       % (q, "0 groups of %d" % n if rev else "%d groups of 0" % n), rnd))
    # missing numbers
    its.append(mcq("Find the missing number: <b>?</b> × 7 = 7", 1, [0, 7, "any number"],
                   "Only 1 keeps the number the same: 1 × 7 = 7. 0 × 7 is 0, and 7 × 7 is 49.", rnd))
    its.append(mcq("Find the missing number: 8 × <b>?</b> = 0", 0, [1, 8, "any number"],
                   "A product is 0 only when you multiply by 0: 8 × 0 = 0. 8 × 1 is 8.", rnd))
    its.append(mcq("Find the missing number: 9 × <b>?</b> = 9", 1, [0, 9, 10],
                   "9 × 1 = 9: one group of 9 is 9. 9 × 0 is 0, and 9 × 10 is 90.", rnd))
    # which is true
    for n, good in [(6, "%d × 0 = 0"), (5, "%d × 1 = %d"), (2, "0 × %d = 0")]:
        right = good % ((n, n) if good.count("%d") == 2 else n)
        bad = ["%d × 0 = %d" % (n, n), "%d × 1 = 1" % n, "%d × 1 = %d" % (n, n + 1), "0 × %d = %d" % (n, n)]
        its.append(mcq("Which equation is true?", right, bad,
                       "Times 1 keeps the number: %d × 1 = %d. Times 0 gives 0, in either order: %d × 0 = 0 × %d = 0." % (n, n, n, n), rnd))
    # with the commutative property
    its.append(mcq("Find the missing number: 1 × 9 = 9 × <b>?</b>", 1, [9, 0, 10],
                   "Switching the factors keeps the product. Both sides are 9, and 9 × 1 = 9.", rnd))
    its.append(mcq("Find the missing number: 0 × 6 = 6 × <b>?</b>", 0, [6, 1, 60],
                   "0 × 6 = 0, so the other side must also be 0. 6 × 0 = 0.", rnd))
    its.append(mcq("Find the missing number: <b>?</b> × 1 = 1 × 4", 4, [1, 0, 5],
                   "Same factors, different order: 4 × 1 = 1 × 4 = 4.", rnd))
    # stories
    its.append(mcq("There are 7 students. Each student has 1 backpack. How many backpacks are there?",
                   "7 backpacks", ["1 backpack", "8 backpacks", "0 backpacks"],
                   "7 groups of 1: 7 × 1 = 7 backpacks.", rnd))
    its.append(mcq("Sam has 4 jars. There are 0 cookies in each jar. How many cookies are in the jars?",
                   "0 cookies", ["4 cookies", "1 cookie", "40 cookies"],
                   "4 groups of 0: 4 × 0 = 0. Empty jars hold no cookies.", rnd))
    its.append(mcq("Nora has 1 box of crayons. The box holds 24 crayons. How many crayons does she have?",
                   "24 crayons", ["1 crayon", "25 crayons", "0 crayons"],
                   "1 group of 24: 1 × 24 = 24 crayons.", rnd))
    return {"title": "Times 1, times 0 and turn-around facts", "items": its}


def set_associative(rnd):
    its = []
    # 6: find the product, grouping to make 10
    for a, b, c in [(2, 7, 5), (5, 9, 2), (2, 4, 5), (3, 5, 2), (5, 8, 2), (2, 6, 5)]:
        p = a * b * c
        mid = [x for x in (a, b, c) if x not in (2, 5)][0]
        its.append(mcq("What is %d × %d × %d?" % (a, b, c), p,
                       [a + b + c, a * b + c, b * c, 10 + mid],
                       "Group 2 × 5 first: 2 × 5 = 10. Then 10 × %d = %d. Any grouping gives the same product."
                       % (mid, p), rnd))
    # 5: which grouping is easiest
    for a, b, c in [(2, 8, 5), (5, 3, 2), (2, 9, 5), (5, 6, 2), (5, 7, 2)]:   # 2 and 5 are never next to each other
        mid = b
        two_five = "(%d × %d) × %d" % (a, c, mid)
        others = ["(%d × %d) × %d" % (a, b, c), "%d × (%d × %d)" % (a, b, c), "(%d + %d) × %d" % (a, c, mid)]
        its.append(mcq("Which grouping of %d × %d × %d makes a 10 first?" % (a, b, c),
                       two_five, others,
                       "%d × %d = 10, and 10 × %d = %d is easy. The other groupings with × give the same product, "
                       "but with harder steps. (%d + %d) × %d adds instead of multiplying." % (a, c, mid, 10 * mid, a, c, mid), rnd))
    # 5: fill in the grouping
    for a, b, c, side in [(3, 2, 4, "right"), (4, 2, 3, "left"), (2, 3, 5, "right"), (6, 1, 7, "left"), (3, 3, 2, "right")]:
        if side == "right":
            q = "(%d × %d) × %d = %d × (%d × <b>?</b>)" % (a, b, c, a, b)
            ans = c
        else:
            q = "%d × (%d × %d) = (<b>?</b> × %d) × %d" % (a, b, c, b, c)
            ans = a
        its.append(mcq("Find the missing number: " + q, ans, [a * b, b * c, a, b, c, a * b * c],
                       "The associative property moves the parentheses but keeps the same three factors: %d, %d and %d. "
                       "Both sides equal %d." % (a, b, c, a * b * c), rnd))
    # 4: which expression is equal
    for a, b, c in [(4, 2, 5), (3, 2, 6), (2, 5, 9), (7, 2, 3)]:
        p = a * b * c
        its.append(mcq("Which is equal to (%d × %d) × %d?" % (a, b, c), "%d × (%d × %d)" % (a, b, c),
                       ["(%d + %d) × %d" % (a, b, c), "(%d × %d) + %d" % (a, b, c), "%d + (%d × %d)" % (a, b, c)],
                       "Keep every × sign and move only the parentheses: %d × (%d × %d) = %d × %d = %d, "
                       "and (%d × %d) × %d = %d × %d = %d." % (a, b, c, a, b * c, p, a, b, c, a * b, c, p), rnd))
    return {"title": "Associative property: group to make it easy", "items": its}


def set_distributive(rnd):
    its = []
    # 6: which expression matches the split array
    for r, a, b in [(8, 5, 2), (4, 5, 3), (6, 5, 4), (3, 2, 4), (7, 5, 1), (5, 3, 3)]:
        n = a + b
        its.append(mcq(fig(split_svg(r, a, b)) + "Which expression matches the picture?", par(r, a, b),
                       ["(%d × %d) + %d" % (r, a, b), par(r, a, n), "(%d × %d) × (%d × %d)" % (r, a, r, b)],
                       "The array has %d rows. The left part is %d rows of %d, and the right part is %d rows of %d. "
                       "Add the parts: %s = %d × %d." % (r, r, a, r, b, par(r, a, b), r, n), rnd))
    # 6: use the parts to find the product
    for r, a, b in [(8, 5, 3), (6, 5, 2), (9, 5, 2), (7, 5, 3), (4, 5, 4), (3, 5, 4)]:
        n, p = a + b, r * (a + b)
        its.append(mcq(fig(split_svg(r, a, b)) + "%d × %d = %s. What is %d × %d?" % (r, n, par(r, a, b), r, n), p,
                       [r * a + b, r * a, p + r, p - r],
                       "%d × %d = %d and %d × %d = %d. %d + %d = %d." % (r, a, r * a, r, b, r * b, r * a, r * b, p), rnd))
    # 5: missing number in the split
    for r, n, a, miss in [(6, 9, 5, "b"), (7, 8, 5, "a"), (4, 7, 5, "b"), (9, 6, 5, "b"), (8, 9, 4, "a")]:
        b = n - a
        if miss == "b":
            q = "%d × %d = (%d × %d) + (%d × <b>?</b>)" % (r, n, r, a, r)
            ans, known = b, a
        else:
            q = "%d × %d = (%d × <b>?</b>) + (%d × %d)" % (r, n, r, r, b)
            ans, known = a, b
        its.append(mcq("Find the missing number: " + q, ans, [n, known, r * ans, n + known, abs(n - r)],
                       "The two parts must add up to %d: %d + %d = %d. So the missing number is %d." % (n, known, ans, n, ans), rnd))
    # 3: which is equal (no picture)
    for r, n, a in [(7, 8, 5), (9, 7, 5), (6, 6, 4)]:
        b = n - a
        its.append(mcq("Which is equal to %d × %d?" % (r, n), par(r, a, b),
                       ["(%d × %d) + %d" % (r, a, b), "(%d × %d) + (%d × %d)" % (r, a - 1, r, b), par(r, a, n)],
                       "Split %d into %d + %d. Multiply both parts by %d and add: %d + %d = %d. "
                       "The two parts must add up to %d." % (n, a, b, r, r * a, r * b, r * n, n), rnd))
    return {"title": "Distributive property: split the array", "items": its}


def set_name_and_story(rnd):
    its = []
    names = [COM, ASSOC, DIST, IDEN, ZERO]
    confuse = {COM: [ASSOC, DIST, IDEN], ASSOC: [COM, DIST, IDEN], DIST: [ASSOC, COM, IDEN],
               IDEN: [ZERO, COM, ASSOC], ZERO: [IDEN, COM, DIST]}
    why = {COM: "The factors switch places, and the product stays the same.",
           ASSOC: "The factors stay in the same order. Only the parentheses move, which changes what you multiply first.",
           DIST: "One factor is split into two parts. Each part is multiplied, and the products are added.",
           IDEN: "Multiplying by 1 keeps the number the same.",
           ZERO: "Multiplying by 0 always gives 0."}
    for eq, prop in [("4 × 7 = 7 × 4", COM), ("(2 × 3) × 4 = 2 × (3 × 4)", ASSOC),
                     ("6 × (5 + 2) = (6 × 5) + (6 × 2)", DIST), ("9 × 1 = 9", IDEN), ("0 × 8 = 0", ZERO),
                     ("(4 × 5) + (4 × 3) = 4 × 8", DIST)]:
        its.append(mcq("Which property does this equation show?<br><b>%s</b>" % eq, prop, confuse[prop],
                       "This is the %s. %s" % (prop, why[prop]), rnd))
    its.append(mcq("Which equation shows the commutative property?", "3 × 8 = 8 × 3",
                   ["8 × 1 = 8", "8 × 0 = 0", "(3 × 2) × 4 = 3 × (2 × 4)"],
                   "Commutative means the order changes: 3 × 8 and 8 × 3 have the same factors in a different order.", rnd))
    its.append(mcq("Which equation shows the distributive property?", "7 × 6 = (7 × 5) + (7 × 1)",
                   ["7 × 6 = 6 × 7", "(7 × 2) × 3 = 7 × (2 × 3)", "7 × 1 = 7"],
                   "6 is split into 5 + 1. Each part is multiplied by 7, and the two products are added: 35 + 7 = 42.", rnd))
    # 12 word problems
    its.append(mcq("Maya sets up 6 rows of 8 chairs. Leo sets up 8 rows of 6 chairs. Who sets up more chairs?",
                   "Same: 48 each", ["Maya", "Leo", "Same: 14 each"],
                   "6 × 8 = 48 and 8 × 6 = 48, so they set up the same number. Switching the order does not change the product. (14 comes from adding 6 + 8.)", rnd))
    its.append(mcq("A box has 4 rows of 9 crayons. Ava says the total is 4 × 9. Ben says it is 9 × 4. Who is right?",
                   "Both", ["Only Ava", "Only Ben", "Neither"],
                   "4 rows of 9 can also be read as 9 columns of 4. 4 × 9 = 9 × 4 = 36.", rnd))
    its.append(mcq("Each of 9 students gets 1 library card. How many library cards are given out?",
                   "9 cards", ["1 card", "10 cards", "0 cards"],
                   "9 groups of 1: 9 × 1 = 9 cards.", rnd))
    its.append(mcq("Omar has 5 boxes. Each box has 0 marbles left in it. How many marbles are in the boxes?",
                   "0 marbles", ["5 marbles", "1 marble", "50 marbles"],
                   "5 groups of 0: 5 × 0 = 0 marbles.", rnd))
    its.append(mcq("A muffin tray has 3 rows of 4 cups. A baker fills 2 trays. How many muffins does the baker make?",
                   24, [12, 9, 14],
                   "3 × 4 × 2. One tray is 3 × 4 = 12, and 2 trays are 12 × 2 = 24. "
                   "Or group 4 × 2 = 8 first: 3 × 8 = 24.", rnd))
    its.append(mcq("An egg carton has 2 rows of 6 eggs. How many eggs are in 5 cartons?",
                   60, [12, 13, 30],
                   "2 × 6 × 5. Group 2 × 5 = 10 first, then 10 × 6 = 60 eggs.", rnd))
    its.append(mcq("There are 2 tables. Each table has 5 students. Each student has 8 crayons. How many crayons are there in all?",
                   80, [40, 15, 18],
                   "2 × 5 × 8. Group 2 × 5 = 10 students first, then 10 × 8 = 80 crayons.", rnd))
    its.append(mcq("A wall has 7 rows of 3 tiles. Another wall has the same number of tiles in 3 rows. "
                   "How many tiles are in each row of the second wall?",
                   7, [3, 21, 4],
                   "7 × 3 = 21 tiles. 3 rows of 7 is also 21, because 3 × 7 = 7 × 3.", rnd))
    its.append(mcq("Kai plants 6 rows of 7 tomato plants. He knows that 6 × 5 = 30. How can he find 6 × 7?",
                   "30 + 12 = 42", ["30 + 2 = 32", "30 + 7 = 37", "30 × 2 = 60"],
                   "7 = 5 + 2, so 6 × 7 = (6 × 5) + (6 × 2) = 30 + 12 = 42. The extra 2 columns have 6 plants each.", rnd))
    its.append(mcq("Mia knows that 7 × 5 = 35. How can she find 7 × 6?",
                   "35 + 7 = 42", ["35 + 6 = 41", "35 + 1 = 36", "35 + 35 = 70"],
                   "7 × 6 is one more group of 7 than 7 × 5: (7 × 5) + (7 × 1) = 35 + 7 = 42.", rnd))
    its.append(mcq("Noah buys 4 packs of markers with 8 markers in each pack. He splits 8 into 5 + 3. "
                   "How many markers does he buy?",
                   32, [23, 20, 35],
                   "4 × 8 = (4 × 5) + (4 × 3) = 20 + 12 = 32 markers. Both parts are multiplied by 4.", rnd))
    its.append(mcq("Lily knows that 10 × 8 = 80. A sheet has 9 rows of 8 stickers. How many stickers are on the sheet?",
                   72, [79, 88, 70],
                   "9 rows is 1 row fewer than 10 rows. Take away one row of 8: 80 − 8 = 72 stickers.", rnd))
    return {"title": "Name the property and solve word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Why the properties help</h2>"
        "<p>The properties of multiplication are rules that work for <b>every</b> number. "
        "They let you turn a fact you do not know into facts you already know.</p>"
        "<h2>Commutative property: change the order</h2>"
        "<p>Switch the factors and the product stays the same. Turn an array on its side: the dots do not change.</p>"
        "<figure class='sn-fig'>" + turn_svg(3, 5, 22) +
        "<figcaption>3 rows of 5 = 5 rows of 3. 3 × 5 = 5 × 3 = 15.</figcaption></figure>"
        "<p>If you know 6 × 4 = 24, you also know 4 × 6 = 24.</p>"
        "<h2>Identity and zero properties</h2>" +
        table(["Property", "Rule", "Example"], [
            ["Identity property of multiplication", "A number × 1 = the same number", "9 × 1 = 9"],
            ["Zero property of multiplication", "A number × 0 = 0", "9 × 0 = 0"],
        ]) +
        "<h2>Associative property: change the grouping</h2>"
        "<p>With three factors, you may multiply <b>any two first</b>. Look for a pair that makes 10.</p>" +
        ex("Example", "Find 3 × 5 × 2.",
           "(3 × 5) × 2 = 15 × 2 = 30, or 3 × (5 × 2) = 3 × 10 = 30.", "30") +
        "<h2>Distributive property: split the array</h2>"
        "<p>Split one factor into two easier parts. Multiply each part, then <b>add</b> the two products.</p>"
        "<figure class='sn-fig'>" + split_svg(8, 5, 2, 22) +
        "<figcaption>8 × 7 = 8 × (5 + 2) = (8 × 5) + (8 × 2) = 40 + 16 = 56.</figcaption></figure>" +
        ex("Example", "You know 6 × 5 = 30. Find 6 × 9.",
           "9 = 5 + 4. (6 × 5) + (6 × 4) = 30 + 24 = 54.", "54") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["8 × 7 = (8 × 5) + 2", "Multiply both parts: (8 × 5) + (8 × 2) = 56"],
            ["Splitting 7 into 4 + 2", "The parts must add up to the factor: 5 + 2 = 7"],
            ["9 × 0 = 9", "Times 0 is always 0. Times 1 keeps the number"],
            ["9 − 4 = 4 − 9", "Switching the order works for × and +, not for − or ÷"],
            ["Mixing up commutative and associative", "Commutative: the order changes. Associative: the parentheses move"],
        ])
    )


FAQ = [
    {"q": "What is the distributive property in 3rd grade?",
     "a": "It means you can split one factor into two parts, multiply each part, and add the products. For example, 8 × 7 = (8 × 5) + (8 × 2) = 40 + 16 = 56."},
    {"q": "What is the commutative property of multiplication?",
     "a": "Changing the order of the factors does not change the product: 6 × 4 = 4 × 6 = 24. Each fact you learn gives you its turn-around fact for free."},
    {"q": "What is the difference between the commutative and associative properties?",
     "a": "The commutative property changes the order of the factors (3 × 5 = 5 × 3). The associative property keeps the order and changes the grouping: (2 × 7) × 5 = 2 × (7 × 5)."},
    {"q": "Do 3rd graders need to know the names of the properties?",
     "a": "The Common Core standard 3.OA.B.5 says students do not need to use the formal names; they need to use the properties as strategies. Many teachers and tests still use the names, so learning them helps."},
]


def gen_properties():
    rnd = random.Random(45)
    sets = [set_commutative(rnd), set_one_zero(rnd), set_associative(rnd), set_distributive(rnd), set_name_and_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "properties-of-multiplication", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Properties of Multiplication",
        "seo_title": "Grade 3 Properties of Multiplication Worksheets: Commutative, Associative and Distributive (with Arrays)",
        "short_title": "Properties of Multiplication",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "3.OA.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/OA/B/5/",
        "standard_text": "Apply properties of operations as strategies to multiply and divide. Examples: If 6 × 4 = 24 is known, then 4 × 6 = 24 is also known. (Commutative property of multiplication.) 3 × 5 × 2 can be found by 3 × 5 = 15, then 15 × 2 = 30, or by 5 × 2 = 10, then 3 × 10 = 30. (Associative property of multiplication.) Knowing that 8 × 5 = 40 and 8 × 2 = 16, one can find 8 × 7 as 8 × (5 + 2) = (8 × 5) + (8 × 2) = 40 + 16 = 56. (Distributive property.)",
        "meta_desc": "Free Grade 3 properties of multiplication worksheets: commutative, associative and distributive properties with arrays, plus times 1 and times 0. Split arrays, missing numbers and word problems. 100 practice questions with answers.",
        "key_big": "Change the order or the grouping, and the product stays the same. Split a hard fact into two easy ones.",
        "key_sub": "6 × 4 = 4 × 6. (2 × 7) × 5 = 2 × (7 × 5). 8 × 7 = (8 × 5) + (8 × 2). Any number × 1 is itself, and any number × 0 is 0.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_properties()
    path = os.path.join(OUT, "properties-of-multiplication.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
