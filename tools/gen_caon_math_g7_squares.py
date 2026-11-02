# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Perfect squares and square roots (Ontario Mathematics Curriculum 2020, Grade 7: B1.2)
  python3 tools/gen_caon_math_g7_squares.py
Perfect squares shown as square arrays of tiles, the squares of 1 to 20, square roots of perfect squares,
deciding whether a number is a perfect square (last digit, squares on either side, prime factor pairs,
odd number of factors), and word problems with the area and side length of a square (a square garden of 144 m²).
Every square, root, area, perimeter and answer is checked in code.
Wrong answers come from real student mistakes: √36 = 18 (halving), 7² = 14 (multiplying by 2), squaring the
answer instead of taking the root, dividing the area by 4 (mixing up area and perimeter), squaring each digit
(13² = 19), counting only the edge tiles of an array, √(a + b) = √a + √b, a row of 2 × 8 tiles “proves” 16 is
not square, and “ends in 0 / ends in 6 so it is square”.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, os, random, re
from fractions import Fraction
from math import isqrt, prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
ORANGE = "#d9822b"
OFILL = "#fbe3c9"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ math
def n(x):
    """Ontario style: 4 digits with no separator, 5 or more digits grouped with a no-break space.
    Decimals keep their decimal point."""
    if isinstance(x, (Fraction, float)) and x != int(x):
        s = str(float(x))
        return s
    x = int(x)
    return str(x) if abs(x) < 10000 else "{:,}".format(x).replace(",", NBSP)


def sq(k):
    return "%s²" % k


def is_sq(x):
    return x >= 0 and isqrt(x) ** 2 == x


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def primes_of(x):
    out, d = [], 2
    while x > 1:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    return out


def half(x):
    """x ÷ 2 written as a whole number or one decimal place."""
    v = Fraction(x, 2)
    return n(v) if v.denominator == 1 else n(float(v))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fixed=None):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance().
    fixed: a full A-D list kept in that order (picture questions)."""
    if fixed is not None:
        assert len(set(fixed)) == 4 and str(correct) in fixed
        return {"q": q, "c": list(fixed), "a": fixed.index(str(correct)), "e": e, "fixed": True}
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position per set). Fixed-order questions stay as they are."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        assert len(targets) == len(free)
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
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


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so every tile and label stays readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def tiles(x0, y0, rows, cols, cell, extra=None):
    """rows × cols square tiles. extra: set of (r, c) drawn orange (tiles being added)."""
    s = []
    for r in range(rows):
        for c in range(cols):
            add = extra is not None and (r, c) in extra
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x0 + c * cell, y0 + r * cell, cell, cell, OFILL if add else FILL, ORANGE if add else GREEN))
    return s


def array_svg(rows, cols, cell=15):
    """A rows × cols array of square tiles."""
    o = 4
    W, H = cols * cell + 2 * o, rows * cell + 2 * o
    shape = "square" if rows == cols else "rectangular"
    return svg_wrap(W, H, "".join(tiles(o, o, rows, cols, cell)), "%s array of %d rows of %d tiles" % (shape, rows, cols))


def grow_svg(k, cell=15):
    """A k × k square of green tiles with one more row and column of orange tiles: the (k+1) × (k+1) square."""
    o = 4
    m = k + 1
    extra = {(r, c) for r in range(m) for c in range(m) if r == k or c == k}
    W = H = m * cell + 2 * o
    return svg_wrap(W, H, "".join(tiles(o, o, m, m, cell, extra)),
                    "square array of %d by %d green tiles with an extra row and column of orange tiles" % (k, k))


def labelled_arrays_svg(sizes, labels, cell=12, gap=26, caption=None):
    """Arrays side by side, each with a label (A, B, C, D or a number) underneath."""
    o = 4
    hmax = max(r for r, c in sizes) * cell
    W = sum(c * cell for r, c in sizes) + gap * (len(sizes) - 1) + 2 * o
    H = o + hmax + 26
    s, x = [], o
    for (r, c), lab in zip(sizes, labels):
        s += tiles(x, o + hmax - r * cell, r, c, cell)
        s.append(text(x + c * cell / 2, o + hmax + 21, lab, 16))
        x += c * cell + gap
    return svg_wrap(W, H, "".join(s), caption or "tile arrays labelled %s" % ", ".join(labels))


def garden_svg(area, unit="m", side=None):
    """A square plot with its area written inside and its side length (or ?) below."""
    o, S = 6, 120
    W, H = S + 2 * o, S + 2 * o + 26
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (o, o, S, S, FILL, GREEN)]
    s.append(text(o + S / 2, o + S / 2 - 4, "Area =", 15, weight=400))
    s.append(text(o + S / 2, o + S / 2 + 16, "%s %s²" % (n(area), unit), 16))
    s.append(text(o + S / 2, H - 6, side if side else "? %s" % unit, 16, col=INK if side else RED))
    return svg_wrap(W, H, "".join(s), "square with an area of %s square %s" % (n(area), "metres" if unit == "m" else "centimetres"))


def lesson_root_svg():
    """Lesson: a 12 m by 12 m square garden with area 144 m²."""
    o, S = 8, 132
    W, H = S + 2 * o + 52, S + 2 * o + 26
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (o, o, S, S, FILL, GREEN)]
    s.append(text(o + S / 2, o + S / 2 - 4, "Area =", 15, weight=400))
    s.append(text(o + S / 2, o + S / 2 + 16, "144 m²", 16))
    s.append(text(o + S / 2, H - 6, "12 m", 16))
    s.append(text(o + S + 8, o + S / 2 + 6, "12 m", 16, anchor="start"))
    return svg_wrap(W, H, "".join(s), "square garden 12 m by 12 m with an area of 144 square metres")


# ============================================================ set 1: perfect squares as square arrays
def set_arrays(P):
    its = []
    its.append(mcq(fig(array_svg(3, 3)) + "The tiles make a square array. Which perfect square does it show?",
                   9, [6, 8, 12],
                   "There are 3 rows of 3 tiles: 3 × 3 = 3² = <b>9</b>. 6 is 3 × 2, 8 counts only the tiles around the "
                   "edge, and 12 is 3 × 4, a rectangle, not a square."))
    for k, third in [(5, 5 * 4), (6, 6 * 7), (8, 8 * 7)]:
        edge = 4 * k - 4
        wrong = [2 * k, edge, third]
        assert k * k not in wrong and len(set(wrong)) == 3
        e = ("There are %d rows of %d tiles: %d × %d = %s = <b>%d</b>. %d is %d × 2, %d counts only the tiles "
             "around the edge, and %d is %d × %d, a rectangle, not a square."
             % (k, k, k, k, sq(k), k * k, 2 * k, k, edge, third, k, third // k))
        its.append(mcq(fig(array_svg(k, k)) + "The tiles make a square array. Which perfect square does it show?",
                       k * k, wrong, e))

    sizes = [(3, 4), (4, 4), (3, 6), (2, 8)]
    assert [r == c for r, c in sizes] == [False, True, False, False]
    its.append(mcq(fig(labelled_arrays_svg(sizes, "ABCD")) + "Which array is a square array?", "B", [],
                   "A square array has the same number of rows and columns. B has 4 rows of 4 tiles, so <b>B</b> is a "
                   "square and shows 4² = 16. A is 3 × 4 = 12, C is 3 × 6 = 18 and D is 2 × 8 = 16 tiles in a rectangle.",
                   fixed=list("ABCD")))
    sizes = [(4, 6), (3, 8), (2, 12), (5, 5)]
    assert [r * c for r, c in sizes] == [24, 24, 24, 25]
    its.append(mcq(fig(labelled_arrays_svg(sizes, "ABCD")) + "Which array shows a perfect square?", "D", [],
                   "D has 5 rows of 5 tiles: 5² = 25, so <b>D</b> shows a perfect square. A, B and C each have 24 tiles "
                   "(4 × 6, 3 × 8, 2 × 12). 24 tiles cannot make a square, because no whole number times itself is 24.",
                   fixed=list("ABCD")))

    assert 6 * 6 - 5 * 6 == 6
    its.append(mcq(fig(array_svg(5, 6)) + "These 30 tiles make 5 rows of 6. How many more tiles are needed to make "
                   "a 6 × 6 square array?", 6, [5, 11, 1],
                   "6 × 6 = 36 and 36 − 30 = <b>6</b>. That is one more row of 6 tiles. A row of 5 is too short, "
                   "and 11 adds a row and a column."))

    assert 7 * 7 - 6 * 6 == 13
    its.append(mcq(fig(grow_svg(6)) + "The green tiles make a 6 × 6 square. How many orange tiles turn it into the "
                   "next square, 7 × 7?", 13, [12, 14, 7],
                   "7² − 6² = 49 − 36 = <b>13</b>. The new row has 7 tiles and the new column has 6 more (the corner is "
                   "counted once). 12 forgets the corner tile and 14 counts it twice."))

    assert isqrt(81) == 9
    its.append(mcq("A square array has 81 tiles. How many tiles are in each row?", 9, ["40.5", "20.25", 27],
                   "In a square array, rows × rows = 81. 9 × 9 = 81, so there are <b>9</b> tiles in each row. "
                   "40.5 is 81 ÷ 2, 20.25 is 81 ÷ 4 and 27 is 81 ÷ 3."))

    assert is_sq(64) and not any(is_sq(v) for v in (24, 32, 48))
    its.append(mcq("Which number of tiles can be set out as a square array?", 64, [24, 32, 48],
                   "8 × 8 = 64, so <b>64</b> tiles make a square array. 24, 32 and 48 are multiples of 8, but none of "
                   "them is a whole number times itself."))
    assert not is_sq(50) and all(is_sq(v) for v in (49, 36, 100))
    its.append(mcq("Which number of tiles <b>cannot</b> be set out as a square array?", 50, [49, 36, 100],
                   "49 = 7 × 7, 36 = 6 × 6 and 100 = 10 × 10. 7 × 7 = 49 and 8 × 8 = 64, so <b>50</b> is not a "
                   "perfect square."))

    its.append(mcq(fig(labelled_arrays_svg([(1, 1), (2, 2), (3, 3)], ["1", "4", "9"], cell=14,
                                           caption="square arrays of 1, 4 and 9 tiles"))
                   + "The pattern grows by one row and one column each time. How many tiles are in the next array?",
                   16, [14, 12, 15],
                   "The next array is 4 × 4 = <b>16</b>. The squares go up by 3, 5, 7 …: 9 + 7 = 16. "
                   "14 adds 5 again and 12 adds 3 again."))

    assert 11 ** 2 - 10 ** 2 == 21
    its.append(mcq("The perfect squares 1, 4, 9, 16, 25 go up by 3, 5, 7, 9 … What is the perfect square after 100?",
                   121, [119, 110, 102],
                   "100 = 10² and the next square is 11² = <b>121</b>. It is 100 + 21, because 10 + 11 = 21. "
                   "119 adds 19 again (81 to 100 added 19), 110 adds 10 and 102 adds 2."))

    its.append(mcq(fig(array_svg(7, 7, cell=13)) + "Which statement describes this array?", "7² = 49",
                   ["7 × 2 = 14", "7 + 7 = 14", "4 × 7 = 28"],
                   "There are 7 rows of 7 tiles, so the array shows <b>7² = 49</b>. 7² means 7 × 7, not 7 × 2 or "
                   "7 + 7. 4 × 7 = 28 adds the four sides and counts each corner twice."))

    nm, he, his = P.next()
    assert 6 * 6 <= 40 < 7 * 7
    its.append(mcq("%s has 40 tiles. What is the largest square array %s can make?" % (nm, he), "6 by 6",
                   ["7 by 7", "5 by 5", "20 by 20"],
                   "6 × 6 = 36 uses 36 tiles (4 are left over). 7 × 7 = 49 needs 9 more tiles than %s has. "
                   "So the largest is <b>6 by 6</b>. 20 by 20 comes from halving 40." % nm))

    assert 12 * 12 == 144
    its.append(mcq("A square array has 12 tiles in each row. How many tiles are there altogether?", 144,
                   [24, 48, 132],
                   "12 rows of 12: 12² = 12 × 12 = <b>144</b>. 24 is 12 × 2, 48 is 4 × 12 (the four sides), and "
                   "132 is 12 × 11, one row short."))

    nm, he, his = P.next()
    assert is_sq(16) and 2 * 8 == 16
    its.append(mcq("%s sets out 16 tiles as 2 rows of 8. %s says this shows 16 is not a perfect square. Is %s right?"
                   % (nm, cap(he), he), "No. 16 tiles also make 4 rows of 4",
                   ["Yes. 2 rows of 8 is not a square", "Yes. 16 is an even number", "No. 2 × 8 is a square"],
                   "A number is a perfect square if its tiles <b>can</b> make a square. 4 × 4 = 16, so 16 is a perfect "
                   "square, even though 2 × 8 is a rectangle."))

    its.append(mcq("A square array has 11 rows of 11 tiles. Which perfect square does it show?", 121,
                   [22, 111, 40],
                   "11 × 11 = 11² = <b>121</b>. 22 is 11 × 2, 111 just writes another 1, and 40 counts only the tiles "
                   "around the edge (4 × 11 − 4)."))
    assert 4 * 11 - 4 == 40

    assert 81 - 64 == 17
    its.append(mcq("How many more tiles does a 9 × 9 array have than an 8 × 8 array?", 17, [1, 16, 18],
                   "9² − 8² = 81 − 64 = <b>17</b>. The difference is not 1: the bigger square has a whole extra row "
                   "and column. 16 is 8 + 8 and 18 is 9 + 9; the right answer is 8 + 9 = 17."))

    assert 100 * 100 == 10000
    its.append(mcq("A square array has 10%s000 tiles. How many tiles are in each row?" % NBSP, 100,
                   ["5000", "2500", "1000"],
                   "100 × 100 = 10%s000, so there are <b>100</b> tiles in each row. 5000 is half of 10%s000, "
                   "2500 is a quarter, and 1000 × 1000 = 1%s000%s000." % (NBSP, NBSP, NBSP, NBSP)))
    assert len(its) == 20, len(its)
    return {"title": "Perfect squares as square arrays", "items": its}


# ============================================================ set 2: squares of 1 to 20
def set_squares(P):
    its = []
    table_ = [
        (7, [14, 9, 42], "14 is 7 × 2, 9 is 7 + 2, and 42 is 7 × 6"),
        (9, [18, 72, 90], "18 is 9 × 2, 72 is 9 × 8, and 90 is 9 × 10"),
        (11, [22, 111, 110], "22 is 11 × 2, 111 just adds another 1, and 110 is 11 × 10"),
        (12, [24, 132, 14], "24 is 12 × 2, 132 is 12 × 11, and 14 squares each digit (1² = 1, 2² = 4)"),
        (13, [26, 19, 156], "26 is 13 × 2, 19 squares each digit (1² = 1, 3² = 9), and 156 is 13 × 12"),
        (15, [30, 125, 210], "30 is 15 × 2, 125 squares each digit (1² = 1, 5² = 25), and 210 is 15 × 14"),
        (16, [32, 136, 240], "32 is 16 × 2, 136 squares each digit (1² = 1, 6² = 36), and 240 is 16 × 15"),
        (18, [36, 164, 306], "36 is 18 × 2, 164 squares each digit (1² = 1, 8² = 64), and 306 is 18 × 17"),
        (19, [38, 181, 342], "38 is 19 × 2, 181 squares each digit (1² = 1, 9² = 81), and 342 is 19 × 18"),
        (20, [40, 4000, 200], "40 is 20 × 2, 200 is 20 × 10, and 4000 has one zero too many"),
    ]
    for k, wrong, why in table_:
        assert k * k not in wrong and wrong[0] == 2 * k
        for w in wrong:
            assert str(w) in why
        e = "%s means %d × %d = <b>%d</b>. %s." % (sq(k), k, k, k * k, why)
        if k == 12:
            e = e.replace("132 is 12 × 11, and", "132 is 12 × 11, and")
        its.append(mcq("What is %s?" % sq(k), k * k, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s writes 7² = 14. What mistake did %s make?" % (nm, he), "%s found 7 × 2, not 7 × 7" % cap(he),
                   ["%s should have found 7 + 2" % cap(he), "%s should have found 2 × 2 × 2" % cap(he),
                    "There is no mistake"],
                   "The small 2 is an exponent. It means “multiply 7 by itself”: 7² = 7 × 7 = <b>49</b>, not 7 × 2 = 14."))

    assert 14 * 14 == 196
    its.append(mcq("Which whole number squared is 196?", 14, [98, 13, 49],
                   "14 × 14 = 196, so <b>14</b>² = 196. 98 is 196 ÷ 2, 13² = 169, and 49 is 196 ÷ 4."))

    assert 300 - 289 == 11 and 324 - 300 == 24
    its.append(mcq("Which square is closest to 300?", "17²", ["18²", "15²", "150²"],
                   "17² = 289 is 11 away from 300, and 18² = 324 is 24 away. So <b>17²</b> is closest. "
                   "15² = 225 is too small, and 150 is half of 300."))

    its.append(mcq("Which list shows 11², 12², 13², 14² and 15²?", "121, 144, 169, 196, 225",
                   ["22, 24, 26, 28, 30", "121, 132, 143, 154, 165", "121, 124, 129, 136, 145"],
                   "11 × 11 = 121, 12 × 12 = 144, 13 × 13 = 169, 14 × 14 = 196 and 15 × 15 = 225: "
                   "<b>121, 144, 169, 196, 225</b>. 22, 24, 26 … multiplies by 2, and 121, 132, 143 … multiplies by 11. "
                   "121, 124, 129 … adds 3, 5, 7 …, but after 11² the steps are 23, 25, 27 …"))
    assert [k * k for k in range(11, 16)] == [121, 144, 169, 196, 225]

    assert 6 ** 2 + 8 ** 2 == 100 and (6 + 8) ** 2 == 196
    its.append(mcq("Evaluate 6² + 8².", 100, [28, 196, 48],
                   "6² = 36 and 8² = 64. 36 + 64 = <b>100</b>. 28 comes from 6 × 2 + 8 × 2, 196 from adding first "
                   "(14²), and 48 from 6 × 8."))

    assert 13 ** 2 - 12 ** 2 == 25 and 169 + 144 == 313
    its.append(mcq("Evaluate 13² − 12².", 25, [1, 2, 313],
                   "13² = 169 and 12² = 144. 169 − 144 = <b>25</b>. 1 comes from subtracting first (1²), "
                   "2 from 26 − 24, and 313 from adding instead of subtracting."))

    assert (-5) ** 2 == 25
    its.append(mcq("Evaluate (−5)².", 25, ["−25", "−10", "10"],
                   "(−5)² = (−5) × (−5). A negative times a negative is positive, so the answer is <b>25</b>. "
                   "−10 and 10 come from multiplying by 2, and −25 forgets that the two negatives make a positive."))

    assert 2 * 5 ** 2 == 50 and (2 * 5) ** 2 == 100
    its.append(mcq("Evaluate 2 × 5².", 50, [100, 20, 25],
                   "Exponents come before multiplication: 5² = 25, then 2 × 25 = <b>50</b>. "
                   "100 squares 2 × 5 = 10 first, 20 is 2 × 5 × 2, and 25 forgets the 2 ×."))

    nm, he, his = P.next()
    its.append(mcq("%s says 30² = 90. What is 30²?" % nm, 900, [90, 60, "9000"],
                   "30² = 30 × 30 = 3 × 3 × 10 × 10 = <b>900</b>. 90 squares the 3 but keeps only one zero, 60 is 30 × 2, and 9000 has "
                   "one zero too many."))

    sqs = [k * k for k in range(1, 20) if 100 < k * k < 200]
    assert sqs == [121, 144, 169, 196]
    its.append(mcq("How many perfect squares are there between 100 and 200?", 4, [3, 5, 2],
                   "11² = 121, 12² = 144, 13² = 169 and 14² = 196. That is <b>4</b>. 15² = 225 is too big, "
                   "and 100 is not between 100 and 200. Do not forget 196."))
    assert len(its) == 20, len(its)
    return {"title": "Squares of 1 to 20", "items": its}


# ============================================================ set 3: square roots of perfect squares
def set_roots(P):
    its = []
    rows = [
        (36, ["18", "1296", "9"], "18 is 36 ÷ 2, 1296 is 36 × 36, and 9 is 36 ÷ 4"),
        (49, ["24.5", "2401", "14"], "24.5 is 49 ÷ 2, 2401 is 49 × 49, and 14 is 7 × 2"),
        (64, ["32", "16", "4096"], "32 is 64 ÷ 2, 16 is 64 ÷ 4, and 4096 is 64 × 64"),
        (81, ["40.5", "27", "6561"], "40.5 is 81 ÷ 2, 27 is 81 ÷ 3, and 6561 is 81 × 81"),
        (121, ["60.5", "12", "22"], "60.5 is 121 ÷ 2, 12 × 12 = 144, and 22 is 11 × 2"),
        (144, ["72", "36", "20" + NBSP + "736"], "72 is 144 ÷ 2, 36 is 144 ÷ 4, and 20" + NBSP + "736 is 144 × 144"),
        (169, ["84.5", "14", "12"], "84.5 is 169 ÷ 2, 14 × 14 = 196, and 12 × 12 = 144"),
        (225, ["112.5", "25", "5"], "112.5 is 225 ÷ 2, 25 only looks at the last two digits, and 5 is √25"),
        (256, ["128", "64", "65" + NBSP + "536"], "128 is 256 ÷ 2, 64 is 256 ÷ 4, and 65" + NBSP + "536 is 256 × 256"),
    ]
    for x, wrong, why in rows:
        r = isqrt(x)
        assert r * r == x and str(r) not in wrong
        assert wrong[0] in (half(x),) or wrong[0] == str(x // 2)
        for w in wrong:
            assert w in why
        e = "%d × %d = %d, so √%d = <b>%d</b>. %s." % (r, r, x, x, r, cap(why))
        its.append(mcq("What is √%d?" % x, r, wrong, e))
    assert 65536 == 256 ** 2 and 1296 == 36 * 36 and 2401 == 49 ** 2 and 4096 == 64 ** 2 and 6561 == 81 ** 2 and 20736 == 144 ** 2

    for x, wrong, why in [
        (400, ["200", "40", "2"], "200 is 400 ÷ 2, 40 × 40 = 1600, and 2 is √4 with the zeros dropped"),
        (900, ["450", "300", "3"], "450 is 900 ÷ 2, 300 × 300 = 90" + NBSP + "000, and 3 is √9 with the zeros dropped"),
        (1600, ["800", "400", "4"], "800 is 1600 ÷ 2, 400 × 400 = 160" + NBSP + "000, and 4 is √16 with the zeros dropped"),
    ]:
        r = isqrt(x)
        assert r * r == x
        e = ("%d × %d = %d, so √%d = <b>%d</b>. A perfect square ending in two zeros has a root ending in "
             "one zero. %s." % (r, r, x, x, r, cap(why)))
        its.append(mcq("What is √%d?" % x, r, wrong, e))
    assert 40 * 40 == 1600 and 300 * 300 == 90000 and 400 * 400 == 160000

    assert 100 * 100 == 10000
    its.append(mcq("What is √10%s000?" % NBSP, 100, ["5000", "1000", "2500"],
                   "100 × 100 = 10%s000, so √10%s000 = <b>100</b>. 5000 is half, 2500 is a quarter, and "
                   "1000 × 1000 = 1%s000%s000." % (NBSP, NBSP, NBSP, NBSP)))

    its.append(mcq("Which square root equals 9?", "√81", ["√18", "√3", "√27"],
                   "9 × 9 = 81, so <b>√81</b> = 9. √18 is not 9 (9 × 2 = 18), √3 is less than 2, and √27 is not 9 "
                   "(9 × 3 = 27)."))

    nm, he, his = P.next()
    its.append(mcq("%s says √36 = 18. What mistake did %s make?" % (nm, he), "%s divided 36 by 2" % cap(he),
                   ["%s multiplied 36 by 2" % cap(he), "%s should have divided by 4" % cap(he), "There is no mistake"],
                   "The square root is the number that, times <b>itself</b>, gives 36. 6 × 6 = 36, so √36 = 6. "
                   "18 × 18 = 324, not 36. Dividing by 2 is not the same as taking the square root."))

    assert isqrt(25) + isqrt(144) == 17 and isqrt(169) == 13
    its.append(mcq("Evaluate √25 + √144.", 17, [13, 169, "84.5"],
                   "√25 = 5 and √144 = 12, so 5 + 12 = <b>17</b>. 13 comes from adding first: √(25 + 144) = √169 = 13. "
                   "That is not allowed: find each root first. 169 forgets the roots, and 84.5 halves 169."))

    assert isqrt(64) - isqrt(16) == 4
    its.append(mcq("Evaluate √64 − √16.", 4, [48, 24, 12],
                   "√64 = 8 and √16 = 4, so 8 − 4 = <b>4</b>. 48 is 64 − 16 with no roots, 24 is 32 − 8 (halving), "
                   "and 12 adds the roots instead of subtracting."))

    assert 14 * 14 == 196 and 14 ** 3 == 2744
    its.append(mcq("√x = 14. What is x?", 196, [7, 28, 2744],
                   "If √x = 14, then x = 14² = 14 × 14 = <b>196</b>. Check: √196 = 14. 7 is 14 ÷ 2, 28 is 14 × 2, "
                   "and 2744 is 14 × 14 × 14."))

    assert isqrt(4 * 25) == 10 == 2 * 5
    its.append(mcq("Evaluate √(4 × 25).", 10, [50, 100, 7],
                   "4 × 25 = 100 and √100 = <b>10</b>. You can also find √4 × √25 = 2 × 5 = 10. 50 halves 100, "
                   "100 forgets the root, and 7 adds 2 + 5."))

    assert is_sq(64) and not any(is_sq(v) for v in (32, 12, 50))
    its.append(mcq("Which square root is a whole number?", "√64", ["√32", "√12", "√50"],
                   "64 is a perfect square (8 × 8), so <b>√64</b> = 8. 32, 12 and 50 are not perfect squares, so "
                   "their square roots are not whole numbers. √32 is not 16: 16 × 16 = 256."))
    assert len(its) == 20, len(its)
    return {"title": "Square roots of perfect squares", "items": its}


# ============================================================ set 4: is it a perfect square?
def set_test(P):
    its = []
    assert is_sq(64) and not any(is_sq(v) for v in (32, 24, 48))
    its.append(mcq("Which number is a perfect square?", 64, [32, 24, 48],
                   "8 × 8 = 64, so <b>64</b> is a perfect square. 32 = 4 × 8, 24 = 4 × 6 and 48 = 6 × 8: "
                   "none is a whole number times itself."))
    assert is_sq(121) and not any(is_sq(v) for v in (112, 111, 22))
    its.append(mcq("Which number is a perfect square?", 121, [112, 111, 22],
                   "11 × 11 = <b>121</b>. 10² = 100 and 11² = 121, so 111 and 112 fall between two squares. "
                   "22 is 11 × 2."))
    assert not is_sq(90) and all(is_sq(v) for v in (36, 100, 144))
    its.append(mcq("Which number is <b>not</b> a perfect square?", 90, [36, 100, 144],
                   "36 = 6², 100 = 10² and 144 = 12². 9² = 81 and 10² = 100, so <b>90</b> is not a perfect square. "
                   "Ending in 0 like 100 is not enough."))
    assert not is_sq(125) and all(is_sq(v) for v in (25, 225, 625))
    its.append(mcq("Which number is <b>not</b> a perfect square?", 125, [25, 225, 625],
                   "25 = 5², 225 = 15² and 625 = 25². 11² = 121 and 12² = 144, so <b>125</b> is not a perfect square. "
                   "(125 = 5 × 5 × 5.) Ending in 25 is not enough."))

    assert is_sq(196)
    its.append(mcq("Is 196 a perfect square?", "Yes. 14 × 14 = 196",
                   ["No. 196 is even", "No. 196 ÷ 2 = 98", "Yes. 98 × 2 = 196"],
                   "14 × 14 = 196, so <b>yes</b>, 196 = 14². Being even does not matter (4, 16 and 36 are even squares). "
                   "98 × 2 is a product of two different numbers, so it does not show a square."))

    assert 14 ** 2 < 200 < 15 ** 2
    its.append(mcq("Is 200 a perfect square?", "No. 14² = 196 and 15² = 225",
                   ["Yes. 100 × 2 = 200", "Yes. It ends in 0 like 100", "Yes. 20 × 10 = 200"],
                   "200 lies between 14² = 196 and 15² = 225, so <b>no</b> whole number squared makes 200. "
                   "100 × 2 and 20 × 10 are not a number times itself."))

    assert 31 ** 2 == 961 and 32 ** 2 == 1024
    its.append(mcq("Is 1000 a perfect square?", "No. 31² = 961 and 32² = 1024",
                   ["Yes. 10 × 10 × 10 = 1000", "Yes. 500 × 2 = 1000", "Yes. 100 × 10 = 1000"],
                   "1000 lies between 31² = 961 and 32² = 1024, so it is <b>not</b> a perfect square. "
                   "10 × 10 × 10 = 10³ uses three factors, not two equal factors."))

    ends = sorted({(k * k) % 10 for k in range(10)})
    assert ends == [0, 1, 4, 5, 6, 9]
    its.append(mcq("A perfect square can never end in which digit?", 7, [1, 6, 9],
                   "The squares of 0 to 9 end in 0, 1, 4, 9, 6, 5, 6, 9, 4, 1. So a perfect square can end only in "
                   "0, 1, 4, 5, 6 or 9. It can never end in 2, 3, <b>7</b> or 8. 81 ends in 1, 16 in 6 and 49 in 9."))

    assert not is_sq(2028) and [isqrt(v) for v in (2025, 1936, 2116)] == [45, 44, 46]
    assert all(is_sq(v) for v in (2025, 1936, 2116))
    its.append(mcq("Which number <b>cannot</b> be a perfect square? Look at the last digit.", 2028,
                   [2025, 1936, 2116],
                   "No perfect square ends in 8, so <b>2028</b> cannot be one. The others are squares: "
                   "45² = 2025, 44² = 1936 and 46² = 2116."))

    s = [v for v in range(51, 100) if is_sq(v)]
    assert s == [64, 81]
    its.append(mcq("How many perfect squares are there between 50 and 100?", 2, [3, 4, 1],
                   "8² = 64 and 9² = 81. That is <b>2</b>. 7² = 49 is below 50, and 100 is not between 50 and 100."))

    its.append(mcq("Which list has <b>only</b> perfect squares?", "1, 4, 9, 16",
                   ["2, 4, 6, 8", "1, 4, 8, 16", "4, 9, 16, 24"],
                   "1 = 1², 4 = 2², 9 = 3² and 16 = 4², so <b>1, 4, 9, 16</b> are all perfect squares. "
                   "2, 6, 8 and 24 are not."))
    assert all(is_sq(v) for v in (1, 4, 9, 16)) and not is_sq(8) and not is_sq(24)

    good, bad = [2, 2, 3, 3], [[2, 3, 3], [2, 2, 2, 3], [2, 3, 5]]
    pr = lambda f: " × ".join(map(str, f))
    assert is_sq(prod(good)) and not any(is_sq(prod(b)) for b in bad)
    its.append(mcq("Which product is a perfect square?", pr(good), [pr(b) for b in bad],
                   "In a perfect square, the prime factors come in pairs. 2 × 2 × 3 × 3 = (2 × 3) × (2 × 3) = 6 × 6 = 36, "
                   "so <b>2 × 2 × 3 × 3</b> is a perfect square. 2 × 3 × 3 = 18, 2 × 2 × 2 × 3 = 24 and "
                   "2 × 3 × 5 = 30 each have a prime without a partner."))

    assert [len(factors(v)) for v in (36, 24, 30, 40)] == [9, 8, 8, 8]
    its.append(mcq("Which number has an <b>odd</b> number of factors?", 36, [24, 30, 40],
                   "Factors come in pairs, but in a perfect square one pair is a number times itself (6 × 6), so it is "
                   "counted once. 36 has 9 factors: 1, 2, 3, 4, 6, 9, 12, 18, 36. So the answer is <b>36</b>. "
                   "24, 30 and 40 each have 8 factors."))

    nm, he, his = P.next()
    its.append(mcq("%s says 50 is a perfect square because 25 × 2 = 50. Is %s right?" % (nm, he),
                   "No. No whole number times itself is 50",
                   ["Yes. 25 × 2 = 50", "Yes. 50 ends in 0", "No. 50 is even"],
                   "A perfect square is a whole number times <b>itself</b>. 7² = 49 and 8² = 64, so 50 is not a perfect "
                   "square. 25 × 2 uses two different numbers. Being even is not the reason: 64 is even and square."))

    assert [v for v in range(151, 300) if is_sq(v)][0] == 169
    its.append(mcq("What is the smallest perfect square greater than 150?", 169, [144, 160, 196],
                   "12² = 144 is less than 150. The next square is 13² = <b>169</b>. 160 is not a square, and "
                   "196 = 14² is the square after 169."))
    assert [v for v in range(1, 300) if is_sq(v)][-1] == 289
    its.append(mcq("What is the largest perfect square less than 300?", 289, [256, 299, 324],
                   "17² = 289 and 18² = 324. 324 is more than 300, so the answer is <b>289</b>. 256 = 16² is smaller "
                   "than 289, and 299 is not a square."))

    assert is_sq(81) and 81 % 2 and is_sq(64) and not is_sq(99) and not is_sq(27)
    its.append(mcq("Which number is a perfect square <b>and</b> odd?", 81, [64, 99, 27],
                   "81 = 9², and 81 is odd, so the answer is <b>81</b>. 64 = 8² is even, and 99 and 27 are odd but "
                   "not perfect squares (27 = 3 × 3 × 3)."))

    ok = {m: is_sq(18 * m) for m in (2, 3, 4, 9)}
    assert ok == {2: True, 3: False, 4: False, 9: False}
    its.append(mcq("By which number can you multiply 18 to get a perfect square?", 2, [3, 4, 9],
                   "18 = 2 × 3 × 3. The 2 has no partner, so multiply by <b>2</b>: 18 × 2 = 36 = 6². "
                   "18 × 3 = 54, 18 × 4 = 72 and 18 × 9 = 162 are not perfect squares."))

    assert is_sq(2500) and not any(is_sq(v) for v in (250, 25000, 5000))
    its.append(mcq("Which number is a perfect square?", "2500", ["250", "25" + NBSP + "000", "5000"],
                   "50 × 50 = <b>2500</b>. A whole number ending in zeros can be a square only if it ends in an "
                   "<b>even</b> number of zeros (100, 2500, 10" + NBSP + "000). 250 and 25" + NBSP + "000 end in an odd "
                   "number of zeros, and 5000 is double 2500."))

    nm, he, his = P.next()
    assert not is_sq(26) and all(is_sq(v) for v in (16, 36, 196))
    its.append(mcq("%s says every number ending in 6 is a perfect square, like 16 and 36. Which number shows %s "
                   "is wrong?" % (nm, he), 26, [16, 36, 196],
                   "5² = 25 and 6² = 36, so <b>26</b> is not a perfect square, even though it ends in 6. "
                   "16 = 4², 36 = 6² and 196 = 14². The last digit can rule a number out, but it cannot prove it is a square."))
    assert len(its) == 20, len(its)
    return {"title": "Is it a perfect square?", "items": its}


# ============================================================ set 5: area and side length word problems
def set_words(P):
    its = []
    its.append(mcq(fig(garden_svg(144)) + "A square garden has an area of 144 m². How long is each side?",
                   "12 m", ["72 m", "36 m", "24 m"],
                   "The area of a square is side × side. 12 × 12 = 144, so each side is √144 = <b>12 m</b>. "
                   "72 m halves the area, 36 m divides the area by 4, mixing it up with perimeter, and 24 m is 12 × 2."))
    assert 12 * 12 == 144

    assert 4 * 12 == 48
    its.append(mcq("A square garden has an area of 144 m². How many metres of fence go all the way around it?",
                   "48 m", ["12 m", "144 m", "576 m"],
                   "First find the side: √144 = 12 m. The fence goes around 4 sides: 4 × 12 = <b>48 m</b>. "
                   "12 m is only one side, and 576 m is 4 × 144, using the area instead of the side."))

    its.append(mcq("A square floor tile is 30 cm on each side. What is its area?", "900 cm²",
                   ["60 cm²", "120 cm²", "90 cm²"],
                   "Area = side × side = 30 × 30 = <b>900 cm²</b>. 60 is 30 × 2, 120 cm is the perimeter (4 × 30), "
                   "and 90 forgets one zero."))

    assert isqrt(81) == 9
    nm, he, his = P.next()
    its.append(mcq("%s’s family floods a square backyard rink with an area of 81 m². How long is each side?" % nm,
                   "9 m", ["40.5 m", "20.25 m", "27 m"],
                   "9 × 9 = 81, so each side is √81 = <b>9 m</b>. 40.5 halves 81, 20.25 divides it by 4, and 27 divides it by 3."))

    nm, he, his = P.next()
    its.append(mcq("%s sews a square quilt from 64 square patches. How many patches are in each row?" % nm, 8,
                   [32, 16, 4],
                   "The quilt is a square array, so rows × rows = 64. 8 × 8 = 64, so there are <b>8</b> patches in "
                   "each row. 32 is 64 ÷ 2, 16 is 64 ÷ 4, and 4 × 4 = 16, not 64."))

    assert isqrt(225) == 15
    its.append(mcq(fig(garden_svg(225, "cm")) + "A square photo has an area of 225 cm². How long is each side?",
                   "15 cm", ["112.5 cm", "56.25 cm", "25 cm"],
                   "15 × 15 = 225, so each side is √225 = <b>15 cm</b>. 112.5 halves 225, 56.25 divides it by 4, "
                   "and 25 only looks at the last two digits (25 × 25 = 625)."))

    assert isqrt(121) == 11
    its.append(mcq("The 121 students in a school band march in a square formation. How many students are in each row?",
                   11, ["60.5", "30.25", 12],
                   "11 × 11 = 121, so there are <b>11</b> students in each row. 60.5 and 30.25 are not whole students, "
                   "and 12 × 12 = 144."))

    assert 12 * 12 == 144 and 150 - 144 == 6 and 13 * 13 > 150
    its.append(mcq("150 students stand in the largest square formation they can for a Terry Fox Run photo. "
                   "How many students are left out of the square?", 6, [19, 0, 25],
                   "12² = 144 and 13² = 169. 169 is too many, so the square is 12 by 12 = 144 students. "
                   "150 − 144 = <b>6</b> are left out. 19 is how many more students a 13 by 13 square would need."))
    assert 169 - 150 == 19

    assert 12 ** 2 == 4 * 6 ** 2
    its.append(mcq("A square vegetable patch is 6 m on each side. The side length is doubled to 12 m. "
                   "What is the new area?", "144 m²", ["72 m²", "36 m²", "48 m²"],
                   "12 × 12 = <b>144 m²</b>. The old area was 6 × 6 = 36 m², so doubling the side makes the area "
                   "4 times as big, not 2 times (72 m²). 48 m is the new perimeter."))

    assert 24 // 4 == 6 and 6 * 6 == 36
    its.append(mcq("A square sandbox has a perimeter of 24 m. What is its area?", "36 m²",
                   ["24 m²", "144 m²", "576 m²"],
                   "Each side is 24 ÷ 4 = 6 m. The area is 6 × 6 = <b>36 m²</b>. 144 comes from 12 × 12 (24 ÷ 2), "
                   "576 is 24 × 24, and the area is not the same as the perimeter."))

    assert Fraction(12, 10) ** 2 == Fraction(144, 100)
    its.append(mcq("A square bulletin board has an area of 1.44 m². How long is each side?", "1.2 m",
                   ["0.72 m", "12 m", "0.12 m"],
                   "1.2 × 1.2 = 1.44, so each side is <b>1.2 m</b>. 0.72 halves the area. 12 × 12 = 144, not 1.44, "
                   "and 0.12 × 0.12 = 0.0144."))

    nm, he, his = P.next()
    assert 50 * 50 == 2500
    its.append(mcq("%s paints on a square canvas that is 50 cm on each side. What is the area of the canvas?" % nm,
                   "2500 cm²", ["100 cm²", "200 cm²", "250 cm²"],
                   "50 × 50 = <b>2500 cm²</b>. 100 is 50 × 2, 200 cm is the perimeter (4 × 50), and 250 has "
                   "one zero too few."))

    nm, he, his = P.next()
    assert isqrt(900) == 30 and 4 * 30 == 120
    its.append(mcq("A square soccer practice field has an area of 900 m². %s runs once around its edge. "
                   "How far does %s run?" % (nm, he), "120 m", ["30 m", "225 m", "3600 m"],
                   "Each side is √900 = 30 m. Once around is 4 × 30 = <b>120 m</b>. 30 m is only one side, "
                   "225 is 900 ÷ 4 (dividing the area, not the perimeter), and 3600 is 4 × 900."))

    assert isqrt(196) == 14 and 14 // 2 == 7 and 196 // 4 == 49
    its.append(mcq("A square garden with an area of 196 m² is split into 4 equal square beds, 2 rows of 2. "
                   "How long is each side of one bed?", "7 m", ["49 m", "14 m", "3.5 m"],
                   "The garden is √196 = 14 m on each side. Two beds fit across, so each bed is 14 ÷ 2 = <b>7 m</b> "
                   "on each side. Check: 7 × 7 = 49 m², and 4 × 49 = 196. 49 is the area of a bed, not its side."))

    assert isqrt(100) - isqrt(64) == 2 and isqrt(100 - 64) == 6
    its.append(mcq("Two square gardens have areas of 64 m² and 100 m². How much longer is a side of the larger "
                   "garden?", "2 m", ["6 m", "36 m", "18 m"],
                   "The sides are √64 = 8 m and √100 = 10 m. 10 − 8 = <b>2 m</b>. 6 m comes from √(100 − 64) = √36: "
                   "find each root first. 36 is the difference in area, and 18 is 8 + 10."))

    nm, he, his = P.next()
    assert 15 * 15 == 225
    its.append(mcq("%s makes a square mosaic with 15 small tiles along each side. How many tiles does %s use?"
                   % (nm, he), 225, [30, 60, 56],
                   "15 rows of 15: 15² = <b>225</b> tiles. 30 is 15 × 2, 60 is the 4 sides (4 × 15), and 56 counts "
                   "only the tiles around the edge (4 × 15 − 4)."))
    assert 4 * 15 - 4 == 56

    assert isqrt(256) == 16 and 4 * 16 == 64
    its.append(mcq("A square outdoor rink has an area of 256 m². How many metres of boards go all the way around it?",
                   "64 m", ["16 m", "128 m", "1024 m"],
                   "Each side is √256 = 16 m (16 × 16 = 256). The boards go around 4 sides: 4 × 16 = <b>64 m</b>. "
                   "16 m is one side, 128 halves the area, and 1024 is 4 × 256."))

    assert isqrt(400) == 20
    its.append(mcq("A square school garden has an area of 400 m². A row of sunflowers will be planted along one side. "
                   "How long is the row?", "20 m", ["200 m", "100 m", "80 m"],
                   "One side is √400 = <b>20 m</b> (20 × 20 = 400). 200 halves the area, 100 is 400 ÷ 4, "
                   "and 80 m is the whole perimeter (4 × 20)."))

    assert 8 * 8 == 64 and 10 * 10 == 100 and 100 - 64 == 36
    its.append(mcq("A square deck is 8 m on each side. It is made bigger so each side is 10 m. How many square metres "
                   "of decking are added?", "36 m²", ["4 m²", "2 m²", "16 m²"],
                   "New area: 10² = 100 m². Old area: 8² = 64 m². 100 − 64 = <b>36 m²</b>. 2 m is only the change in "
                   "side length, 4 m² is 2², and 16 m² adds one strip of 2 × 8."))

    nm, he, his = P.next()
    assert isqrt(169) == 13 and 13 * 4 == 52
    its.append(mcq("%s’s cottage has a square dock with an area of 169 m². %s walks once around the edge. How far does "
                   "%s walk?" % (nm, cap(he), he), "52 m", ["13 m", "42.25 m", "676 m"],
                   "Each side is √169 = 13 m. Once around is 4 × 13 = <b>52 m</b>. 13 m is only one side, "
                   "42.25 is 169 ÷ 4, and 676 is 4 × 169."))
    assert 169 / 4 == 42.25 and 4 * 169 == 676
    assert len(its) == 20, len(its)
    return {"title": "Word problems: area and side length", "items": its}


# ============================================================ lesson
def body_html():
    sq_rows = [[str(k), "%d²" % k, str(k * k)] for k in range(1, 21)]
    half_ = (len(sq_rows) + 1) // 2
    rows = [a + b for a, b in zip(sq_rows[:half_], sq_rows[half_:])]
    return (
        "<h2>What is a perfect square?</h2>"
        "<p>A <b>perfect square</b> is a whole number times itself. 5 × 5 = 25, so 25 is a perfect square. "
        "We write 5 × 5 as <b>5²</b> (“5 squared”). The small 2 is an exponent: it tells you to multiply 5 by itself.</p>"
        "<p>A perfect square number of tiles can be set out as a <b>square array</b>, with the same number of rows and columns.</p>"
        "<figure class='sn-fig'>" + labelled_arrays_svg([(1, 1), (2, 2), (3, 3), (4, 4)], ["1", "4", "9", "16"], cell=14,
                                                        caption="square arrays of 1, 4, 9 and 16 tiles") +
        "<figcaption>1², 2², 3² and 4². Each square adds one row and one column: the squares go up by 3, 5, 7 …</figcaption></figure>"
        + "<p>Learn the squares of 1 to 20. They come up again and again.</p>"
        + table(["n", "n²", "value", "n", "n²", "value"], rows)
        + ex("Example", "Evaluate 6² + 8².", "6² = 6 × 6 = 36 and 8² = 8 × 8 = 64. Then 36 + 64 = 100.", "100")
        + "<h2>Square roots</h2>"
        "<p>The <b>square root</b> of a number is the number that, times itself, gives that number. "
        "The sign is √. 12 × 12 = 144, so √144 = 12. Squaring and taking the square root undo each other.</p>"
        "<p>For a square, the area is side × side. So the side length is the square root of the area.</p>"
        "<figure class='sn-fig'>" + lesson_root_svg() +
        "<figcaption>A square garden with an area of 144 m² has sides of √144 = 12 m.</figcaption></figure>"
        + ex("Example", "What is √1600?",
             "Think: which number times itself is 1600? 40 × 40 = 1600.", "√1600 = 40")
        + "<h2>Is it a perfect square?</h2>"
        "<ul><li><b>Squares on either side.</b> 14² = 196 and 15² = 225, so 200 is not a perfect square.</li>"
        "<li><b>Last digit.</b> A perfect square ends in 0, 1, 4, 5, 6 or 9. A number ending in 2, 3, 7 or 8 is never a "
        "perfect square. A good last digit does not prove it, though: 26 ends in 6 and is not a square.</li>"
        "<li><b>Prime factors in pairs.</b> 36 = 2 × 2 × 3 × 3 = (2 × 3) × (2 × 3) = 6². 18 = 2 × 3 × 3 has a 2 without a "
        "partner, so it is not a square.</li></ul>"
        + ex("Example", "Is 1000 a perfect square?",
             "31² = 961 and 32² = 1024. 1000 is between them.", "no")
        + "<h2>Area and side length problems</h2>"
        + ex("Example", "A square garden has an area of 144 m². How much fencing goes around it?",
             "Side: √144 = 12 m. Perimeter: 4 × 12 = 48 m.", "48 m of fencing")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["7² = 14", "7² means 7 × 7 = 49, not 7 × 2"],
            ["√36 = 18", "Do not halve. 6 × 6 = 36, so √36 = 6"],
            ["13² = 19 (squaring each digit)", "Multiply the whole number: 13 × 13 = 169"],
            ["√(25 + 144) = √25 + √144", "Find each root first: 5 + 12 = 17. √169 = 13 is different"],
            ["Side = area ÷ 4", "Side = √area. Dividing by 4 works for the perimeter, not the area"],
            ["“16 is 2 × 8, so it is not a square”", "Look for any way to make a square: 4 × 4 = 16"],
        ])
    )


FAQ = [
    {"q": "What is a perfect square in Grade 7 math?",
     "a": "A perfect square is a whole number multiplied by itself, such as 49 = 7 × 7 = 7². In the Ontario Grade 7 math curriculum, students show perfect squares as square arrays and find their square roots."},
    {"q": "How do you find the square root of a perfect square?",
     "a": "Ask which whole number times itself gives the number. 12 × 12 = 144, so √144 = 12. Do not divide by 2: √36 is 6, not 18."},
    {"q": "Which perfect squares should Grade 7 students know?",
     "a": "Students should know the squares of 1 to 20, from 1² = 1 to 20² = 400. Knowing them by heart makes square roots, area problems and the Pythagorean theorem in Grade 8 much faster."},
    {"q": "How do you find the side length of a square from its area?",
     "a": "Take the square root of the area. A square garden with an area of 144 m² has sides of √144 = 12 m, so its perimeter is 4 × 12 = 48 m."},
]


def gen():
    rnd = random.Random(47802)
    P = People(rnd)
    sets = [set_arrays(P), set_squares(P), set_roots(P), set_test(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "perfect-squares-and-square-roots", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Perfect Squares and Square Roots",
        "seo_title": "Grade 7 Perfect Squares and Square Roots Worksheets (Free, Answer Key)",
        "short_title": "Perfect squares and square roots",
        "domain": "Number",
        "standard_code": "Grade 7: B1.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify and represent perfect squares, and determine their square roots, in various contexts",
        "meta_desc": "Free Grade 7 math worksheets for the Ontario curriculum: perfect squares as square arrays, the squares of 1 to 20, square roots of perfect squares, how to tell if a number is a perfect square, and area and side length word problems. 100 questions with an answer key.",
        "key_big": "A perfect square is a whole number times itself. The square root undoes squaring: 12² = 144, so √144 = 12.",
        "key_sub": "7² means 7 × 7 = 49, not 7 × 2. √36 is 6, not 18: never halve. The side of a square is the square root of its area.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "tile arrays labelled")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
