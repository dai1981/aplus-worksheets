# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Prime, composite and square numbers (Australian Curriculum v9.0, AC9M6N02)
  python3 tools/gen_au_maths_y6_primes_squares.py
Factors and prime or composite numbers (1 is neither), square numbers shown as square arrays and square
roots of perfect squares, prime factorisation with factor trees, using these properties to simplify
calculations (25 × 4 × 7), and word problems (students in a square, rows of chairs).
Every factor, prime, square, product and answer is checked in code.
Wrong answers come from real mistakes: 1 is prime, 9 / 27 / 51 / 57 / 91 are prime, 2 is composite because
it is even, 4² = 8 (4 × 2), halving for a square root, writing a non-prime (or 1) in a prime factorisation,
adding instead of multiplying, dividing an area by 4 to find a side.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from math import prod, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ maths
def num(x):
    """Australian style: 4 digits plain, 5+ digits grouped with a no-break space."""
    x = int(x)
    return str(x) if abs(x) < 10000 else "{:,}".format(x).replace(",", NB)


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


def is_prime(x):
    return len(factors(x)) == 2


def is_comp(x):
    return len(factors(x)) > 2


def is_sq(x):
    return x >= 1 and isqrt(x) ** 2 == x


def primes_of(x):
    out, d = [], 2
    while x > 1:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    return out


def lst(xs):
    return ", ".join(num(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def sup(b, p=2):
    return "%d<sup>%d</sup>" % (b, p)


def why_not_prime(x):
    if x == 1:
        return "1 has only one factor, so it is not prime"
    s = pairs(x)[1]
    return "%d = %d × %d, so %d is not prime" % (x, s[0], s[1], x)


def ev(expr):
    """Value of a product written with ×."""
    return prod(int(v) for v in expr.split(" × "))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
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
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


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
    """Tag pictures that must print larger so every number stays readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def T(v, a=None, b=None):
    """Tree node: v splits into a and b (themselves nodes or ints)."""
    if a is None:
        return (v, None)
    a = a if isinstance(a, tuple) else (a, None)
    b = b if isinstance(b, tuple) else (b, None)
    assert a[0] * b[0] == v, (v, a[0], b[0])
    return (v, [a, b])


def split(x):
    """Most balanced factor pair of x (both > 1), or None if x is prime."""
    best = None
    for a in range(2, isqrt(x) + 1):
        if x % a == 0:
            best = (a, x // a)
    return best


def auto_tree(x):
    s = split(x)
    return T(x) if s is None else T(x, auto_tree(s[0]), auto_tree(s[1]))


def leaves(t):
    return [t[0]] if t[1] is None else leaves(t[1][0]) + leaves(t[1][1])


def depth(t):
    return 1 if t[1] is None else 1 + max(depth(c) for c in t[1])


def tree_svg(t, hide=None, step=46, dy=50):
    """Factor tree: each number splits into a factor pair; the primes at the ends of the branches are circled.
    'hide' is a value shown as ? (in a red box)."""
    assert prod(leaves(t)) == t[0]
    assert all(is_prime(v) for v in leaves(t))
    o = 22
    W = (len(leaves(t)) - 1) * step + 2 * o
    H = (depth(t) - 1) * dy + 2 * o
    pos = {}
    s = []
    cnt = [0]

    def place(node, lvl):
        if node[1] is None:
            px = o + cnt[0] * step
            cnt[0] += 1
        else:
            xs = [place(c, lvl + 1) for c in node[1]]
            px = sum(xs) / 2
        pos[id(node)] = (px, o + lvl * dy)
        return px

    place(t, 0)
    hidden = [0]

    def draw(node):
        px, py = pos[id(node)]
        if node[1] is not None:
            for c in node[1]:
                cx, cy = pos[id(c)]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                         % (px, py + 9, cx, cy - 15, GREY))
                draw(c)
        if node[0] == hide and not hidden[0]:
            hidden[0] = 1
            s.append("<rect x='%.1f' y='%.1f' width='30' height='28' rx='4' fill='#fff' stroke='%s' stroke-width='2'/>"
                     % (px - 15, py - 14, RED))
            s.append(text(px, py + 6, "?", 18, col=RED))
            return
        if node[1] is None:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (px, py, FILL, GREEN))
        s.append(text(px, py + 6, str(node[0]), 17))

    draw(t)
    lab = "factor tree for %s" % ("a number" if hide == t[0] else t[0]) + (" with one number missing" if hide else "")
    return svg_wrap(W, H, "".join(s), lab)


def square_svg(n, cell=16):
    """n rows of n dots: a square array."""
    o = 6
    W = H = n * cell + 2 * o
    s = ["<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s'/>" % (o + j * cell + cell / 2, o + i * cell + cell / 2, GREEN)
         for i in range(n) for j in range(n)]
    return svg_wrap(W, H, "".join(s), "square array of dots")


def squares_row_svg(k=4, cell=14, gap=26):
    """Lesson: square numbers 1, 4, 9, 16 as squares of dots, with the number below."""
    o = 8
    W = o * 2 + sum(i * cell for i in range(1, k + 1)) + gap * (k - 1)
    H = o + k * cell + 28
    s = []
    x = o
    for i in range(1, k + 1):
        y0 = o + (k - i) * cell
        for r in range(i):
            for c in range(i):
                s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x + c * cell + cell / 2, y0 + r * cell + cell / 2, GREEN))
        s.append(text(x + i * cell / 2, o + k * cell + 22, str(i * i), 16))
        x += i * cell + gap
    return svg_wrap(W, H, "".join(s), "square numbers 1, 4, 9 and 16 shown as square arrays of dots")


def rows_svg(rows, cols, cell=16):
    """Lesson: a non-square array (composite) of dots with its size written underneath."""
    o = 6
    W = max(cols * cell + 2 * o, 70)
    H = rows * cell + 2 * o + 24
    x0 = (W - cols * cell) / 2
    s = ["<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x0 + j * cell + cell / 2, o + i * cell + cell / 2, GREEN)
         for i in range(rows) for j in range(cols)]
    s.append(text(W / 2, H - 6, "%d × %d" % (rows, cols), 15))
    return s, W, H


def arrays_svg():
    """Lesson: 12 can be a rectangle (composite); 13 can only be one row (prime)."""
    gap = 28
    a, wa, ha = rows_svg(3, 4)
    b, wb, hb = rows_svg(2, 6)
    c, wc, hc = rows_svg(1, 13)
    H = max(ha, hb, hc)
    parts = []
    x = 0
    for p, w, h in [(a, wa, ha), (b, wb, hb), (c, wc, hc)]:
        parts.append("<g transform='translate(%d %d)'>%s</g>" % (x, H - h, "".join(p)))
        x += w + gap
    W = x - gap
    return svg_wrap(W, H, "".join(parts), "12 dots as 3 rows of 4 and 2 rows of 6, and 13 dots in only 1 row")


# ============================================================ set 1: factors, prime and composite
def set_prime_composite(P):
    its = []
    for x, drop in [(12, (3, 4)), (20, (4, 5)), (30, (5, 6)), (42, (6, 7))]:
        fs = factors(x)
        right = lst(fs)
        missing = lst([d for d in fs if d not in drop])
        multi = lst([x * k for k in range(1, 5)])
        no_ends = lst(fs[1:-1])
        e = ("Find the factor pairs: %s. So the factors are <b>%s</b>. Do not forget 1 and %d, and do not miss "
             "%d × %d. %s are multiples of %d, not factors."
             % (", ".join("%d × %d" % p for p in pairs(x)), right, x, drop[0], drop[1], multi, x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, right, [missing, no_ends, multi], e))

    assert factors(1) == [1]
    its.append(mcq("Is 1 a prime number, a composite number or neither?", "Neither",
                   ["Prime", "Composite", "Both"],
                   "A prime number has exactly two factors. A composite number has more than two. 1 has only "
                   "<b>one</b> factor (itself), so it is <b>neither</b> prime nor composite."))

    nm, he, his = P.next()
    assert is_prime(2)
    its.append(mcq("%s says 2 is a composite number because it is even. Is %s right?" % (nm, he),
                   "No. 2 is prime", ["Yes. 2 is even", "Yes. 2 = 1 × 2", "No. 2 is neither"],
                   "The factors of 2 are 1 and 2: exactly two factors, so <b>2 is prime</b>. It is the only even "
                   "prime. Every other even number has 2 as a factor as well, so it is composite."))

    for right, wrong in [(7, [9, 1, 15]), (19, [21, 27, 25]), (31, [33, 39, 35]), (47, [49, 51, 57])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("%d has exactly two factors, 1 and %d, so <b>%d</b> is prime. " % (right, right, right)
             + ". ".join(cap(why_not_prime(w)) for w in wrong) + ".")
        if 9 in wrong or 51 in wrong:
            e += " Being odd does not make a number prime."
        its.append(mcq("Which of these is a prime number?", right, wrong, e))

    for right, wrong in [(9, [2, 7, 1]), (27, [23, 29, 31]), (91, [83, 89, 97])]:
        assert is_comp(right) and not any(is_comp(w) for w in wrong)
        e = ("%s, so <b>%d</b> has more than two factors (%s). It is composite. "
             % (cap(why_not_prime(right)).split(", so")[0], right, lst(factors(right))))
        e += "%s are prime: each has exactly two factors." % " and ".join(str(w) for w in wrong if w != 1).replace(
            " and ", ", ", len([w for w in wrong if w != 1]) - 2)
        if 1 in wrong:
            e += " 1 is neither prime nor composite."
        its.append(mcq("Which of these is a composite number?", right, wrong, e))

    assert all(is_prime(v) for v in (2, 3, 5, 7)) and not is_prime(9) and not is_prime(15) and not is_prime(1)
    its.append(mcq("Which list shows <b>only</b> prime numbers?", "2, 3, 5, 7",
                   ["1, 3, 5, 7", "3, 5, 7, 9", "5, 7, 11, 15"],
                   "2, 3, 5 and 7 each have exactly two factors, so <b>2, 3, 5, 7</b> are all prime. "
                   "1 is not prime, 9 = 3 × 3 and 15 = 3 × 5."))

    ps = [v for v in range(1, 21) if is_prime(v)]
    assert ps == [2, 3, 5, 7, 11, 13, 17, 19] and len([v for v in range(1, 21) if v % 2]) == 10
    its.append(mcq("How many prime numbers are there from 1 to 20?", 8, [9, 7, 10],
                   "The primes are 2, 3, 5, 7, 11, 13, 17 and 19: <b>8</b> primes. 9 comes from counting 1, 7 from "
                   "leaving out 2, and 10 is the number of odd numbers (9 and 15 are odd but not prime)."))

    assert factors(16) == [1, 2, 4, 8, 16] and len(pairs(16)) == 3
    its.append(mcq("How many factors does 16 have?", 5, [6, 3, 8],
                   "The factor pairs are 1 × 16, 2 × 8 and 4 × 4. The factors are 1, 2, 4, 8 and 16: <b>5</b> factors. "
                   "Count 4 only once (6 counts it twice), 3 is the number of factor pairs, and 8 is half of 16."))

    assert [len(factors(v)) for v in (25, 12, 15, 17)] == [3, 6, 4, 2]
    its.append(mcq("Which number has exactly 3 factors?", 25, [12, 15, 17],
                   "The factors of 25 are 1, 5 and 25, so <b>25</b> has 3 factors. 12 has 6 factors (1, 2, 3, 4, 6, 12), "
                   "15 has 4 (1, 3, 5, 15) and 17 is prime, so it has 2."))

    assert [v for v in range(1, 10) if is_comp(v)][0] == 4
    its.append(mcq("What is the smallest composite number?", 4, [1, 2, 9],
                   "1 is neither prime nor composite, and 2 and 3 are prime. 4 = 2 × 2 has three factors (1, 2, 4), "
                   "so the smallest composite number is <b>4</b>."))

    assert all(is_comp(v) for v in range(4, 101, 2))
    its.append(mcq("Which statement is true?", "Every even number bigger than 2 is composite",
                   ["Every odd number is prime", "1 is the smallest prime number", "All prime numbers are odd"],
                   "Every even number bigger than 2 has 1, 2 and itself as factors, so <b>it is composite</b>. "
                   "9 is odd but not prime, 1 is not prime, and 2 is an even prime."))

    nm, he, his = P.next()
    assert 57 == 3 * 19 and 56 == 7 * 8
    its.append(mcq("%s says 57 is prime because it is odd and is not in %s times tables. Is %s right?" % (nm, his, he),
                   "No. 57 = 3 × 19", ["Yes. 57 is odd", "Yes. It has 2 factors", "No. 57 = 7 × 8"],
                   "5 + 7 = 12, a multiple of 3, so 57 divides by 3: <b>57 = 3 × 19</b>. Its factors are 1, 3, 19 and 57, "
                   "so it is composite. 7 × 8 = 56, not 57."))
    assert len(its) == 20, len(its)
    return {"title": "Factors, prime and composite numbers", "items": its}


# ============================================================ set 2: square numbers and square roots
def set_squares(P):
    its = []
    for k, wrong, why in [(4, [8, 12, 9], "9 is 3 × 3, one row too few"), (5, [10, 16, 20], "20 is 5 × 4, one row too few"),
                          (6, [12, 20, 30], "30 is 6 × 5, one row too few")]:
        assert wrong[0] == 2 * k and 4 * k - 4 in wrong
        e = ("There are %d rows of %d dots. %d × %d = %s = <b>%d</b>. %d is %d × 2, %d counts only the dots "
             "around the edge, and %s." % (k, k, k, k, sup(k), k * k, 2 * k, k, 4 * k - 4, why))
        its.append(mcq(fig(square_svg(k)) + "The dots make a square array. Which square number does it show?",
                       k * k, wrong, e))

    for k, wrong in [(4, [8, 6, 64]), (7, [14, 9, 77]), (9, [18, 11, 72]), (12, [24, 14, 132])]:
        assert k * k not in wrong and wrong[0] == 2 * k and wrong[1] == k + 2
        e = "%s means %d × %d = <b>%d</b>. It does not mean %d × 2 = %d or %d + 2 = %d." % (
            sup(k), k, k, k * k, k, 2 * k, k, k + 2)
        if k == 4:
            e += " 64 is 4 × 4 × 4."
        if k == 9:
            e += " 72 is 9 × 8."
        if k == 12:
            e += " 132 is 12 × 11."
        if k == 7:
            e += " 77 is just two 7s written side by side."
        its.append(mcq("What is %s?" % sup(k), k * k, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s says %s = 8. Is %s right?" % (nm, sup(4), he), "No. It is 4 × 4 = 16",
                   ["Yes. 4 × 2 = 8", "Yes. 4 + 4 = 8", "No. It is 4 + 2 = 6"],
                   "The small 2 means “multiply the number by itself”. %s = 4 × 4 = <b>16</b>, not 4 × 2." % sup(4)))

    assert is_sq(81) and not any(is_sq(w) for w in (18, 27, 72))
    its.append(mcq("Which of these is a square number?", 81, [18, 27, 72],
                   "9 × 9 = <b>81</b>, so 81 is a square number. 18 = 9 × 2, 27 = 3 × 3 × 3 and 72 = 8 × 9: "
                   "none of them is a number times itself."))
    assert not is_sq(40) and all(is_sq(w) for w in (16, 49, 121))
    its.append(mcq("Which number is <b>not</b> a square number?", 40, [16, 49, 121],
                   "16 = 4 × 4, 49 = 7 × 7 and 121 = 11 × 11. 6 × 6 = 36 and 7 × 7 = 49, so <b>40</b> is not a square "
                   "number."))
    its.append(mcq("Which list shows the first five square numbers?", "1, 4, 9, 16, 25",
                   ["2, 4, 6, 8, 10", "4, 9, 16, 25, 36", "1, 2, 4, 8, 16"],
                   "1 × 1 = 1, 2 × 2 = 4, 3 × 3 = 9, 4 × 4 = 16, 5 × 5 = 25. The first square number is <b>1</b>. "
                   "2, 4, 6, 8, 10 are the multiples of 2."))

    for x, wrong in [(36, [18, 12, 1296]), (64, [32, 16, 4096]), (100, [50, 20, 10000]), (144, [72, 24, 11])]:
        r = isqrt(x)
        assert r * r == x and wrong[0] * 2 == x and wrong[1] == 2 * r
        e = "%d × %d = %d, so √%d = <b>%d</b>. Do not halve: %d × %d = %s, not %d. %d is %d × 2." % (
            r, r, x, x, r, wrong[0], wrong[0], num(wrong[0] ** 2), x, wrong[1], r)
        if wrong[2] == x * x:
            e += " %s is %d × %d." % (num(x * x), x, x)
        if x == 144:
            e += " 11 × 11 = 121, which is too small."
        its.append(mcq("What is √%d (the square root of %d)?" % (x, x), r, [num(w) for w in wrong], e))

    assert isqrt(49) == 7 and 49 / 4 == 12.25 and 49 / 2 == 24.5
    its.append(mcq("A square has an area of 49 cm<sup>2</sup>. How long is each side?", "7 cm",
                   ["12.25 cm", "24.5 cm", "14 cm"],
                   "The area of a square is side × side. 7 × 7 = 49, so each side is <b>7 cm</b>. "
                   "49 ÷ 4 = 12.25 mixes up area and perimeter, and 49 ÷ 2 = 24.5 halves the area."))

    assert 49 < 50 < 64
    its.append(mcq("50 is between which two square numbers?", "49 and 64",
                   ["36 and 49", "25 and 36", "40 and 60"],
                   "7 × 7 = 49 and 8 × 8 = 64, so 50 is between <b>49 and 64</b>. 40 and 60 are not square numbers."))

    assert 3 ** 2 + 4 ** 2 == 25
    its.append(mcq("Work out %s + %s" % (sup(3), sup(4)), 25, [14, 49, 12],
                   "%s = 9 and %s = 16. 9 + 16 = <b>25</b>. 14 comes from 3 × 2 + 4 × 2, and 49 from adding first "
                   "(3 + 4 = 7, 7 × 7 = 49)." % (sup(3), sup(4))))

    assert 10 ** 2 - 6 ** 2 == 64
    its.append(mcq("Work out %s − %s" % (sup(10), sup(6)), 64, [16, 8, 136],
                   "%s = 100 and %s = 36. 100 − 36 = <b>64</b>. 16 comes from subtracting first (10 − 6 = 4, 4 × 4 = 16), "
                   "8 from 20 − 12, and 136 is 100 + 36." % (sup(10), sup(6))))

    sqs = [v for v in range(1, 101) if is_sq(v)]
    assert len(sqs) == 10
    its.append(mcq("How many square numbers are there from 1 to 100?", 10, [9, 8, 50],
                   "1, 4, 9, 16, 25, 36, 49, 64, 81 and 100 (1 × 1 up to 10 × 10). That is <b>10</b> square numbers. "
                   "Remember to count 1 and 100: 9 leaves one of them out, 8 leaves both out, "
                   "and 50 is half of 100."))
    assert len(its) == 20, len(its)
    return {"title": "Square numbers and square roots", "items": its}


# ============================================================ set 3: prime factorisation
def set_factor_trees(P):
    its = []
    for x in [12, 18, 20, 40, 63, 75]:
        t = auto_tree(x)
        ps = sorted(leaves(t))
        assert ps == primes_of(x)
        first = times(split(x))
        once = times(sorted(set(ps)))
        with1 = times([1] + ps)
        notp = [v for v in split(x) if not is_prime(v)]
        e = ("Keep splitting until every branch ends in a prime: %d = <b>%s</b>. %s is not finished, because %s "
             "not prime. 1 is not prime, so it is not written."
             % (x, times(ps), first, " and ".join(str(v) for v in notp) + (" are" if len(notp) > 1 else " is")))
        if once != first:
            e += " %s leaves out a repeated prime: %s = %d." % (once, once, ev(once))
        its.append(mcq(fig(tree_svg(t)) + "Which shows %d as a product of prime factors?" % x, times(ps),
                       [first, once, with1], e))

    # missing numbers in a factor tree
    t = T(48, T(6, 2, 3), T(8, 2, T(4, 2, 2)))
    its.append(mcq(fig(tree_svg(t, hide=8)) + "What number is missing from the factor tree?", 8, [42, 54, 288],
                   "The two branches multiply to make 48. 6 × ? = 48, and 6 × 8 = 48, so the missing number is <b>8</b>. "
                   "Check: 8 = 2 × 4. 42 is 48 − 6, 54 is 48 + 6, and 288 is 48 × 6."))
    t = T(90, T(9, 3, 3), T(10, 2, 5))
    its.append(mcq(fig(tree_svg(t, hide=5)) + "What number is missing from the factor tree?", 5, [8, 12, 20],
                   "10 splits into 2 × ?. 2 × 5 = 10, so the missing number is <b>5</b>. 8 is 10 − 2, 12 is 10 + 2 "
                   "and 20 is 10 × 2. So 90 = 2 × 3 × 3 × 5."))
    t = T(72, T(8, 2, T(4, 2, 2)), T(9, 3, 3))
    its.append(mcq(fig(tree_svg(t, hide=72)) + "What number is at the top of the factor tree?", 72, [17, 89, 63],
                   "The top number is 8 × 9 = <b>72</b>. Check: 2 × 2 × 2 × 3 × 3 = 72. 17 is 8 + 9, "
                   "89 is just 8 and 9 written side by side, and 63 is 7 × 9."))

    assert primes_of(30) == [2, 3, 5]
    its.append(mcq("What are the prime factors of 30?", "2, 3 and 5", ["1, 2, 3 and 5", "5 and 6", "2 and 15"],
                   "30 = 2 × 3 × 5, and 2, 3 and 5 are all prime. So the prime factors are <b>2, 3 and 5</b>. "
                   "1 is not prime, 6 = 2 × 3 and 15 = 3 × 5."))

    assert ev("2 × 2 × 3 × 5") == 60
    its.append(mcq("Which number is 2 × 2 × 3 × 5?", 60, [12, 30, 120],
                   "2 × 2 = 4, 4 × 3 = 12, 12 × 5 = <b>60</b>. 12 comes from adding (2 + 2 + 3 + 5), "
                   "30 from using only one 2, and 120 from using three 2s."))
    assert ev("2 × 3 × 3 × 7") == 126
    its.append(mcq("Which number is 2 × 3 × 3 × 7?", 126, [15, 42, 63],
                   "2 × 3 = 6, 6 × 3 = 18, 18 × 7 = <b>126</b>. 15 comes from adding (2 + 3 + 3 + 7), "
                   "42 from using only one 3, and 63 from leaving out the 2."))

    assert primes_of(36) == [2, 2, 3, 3]
    its.append(mcq("Which is the prime factorisation of 36?", "2 × 2 × 3 × 3", ["4 × 9", "6 × 6", "2 × 3"],
                   "36 = 6 × 6, and 6 = 2 × 3. So 36 = <b>2 × 2 × 3 × 3</b>. 4 × 9 and 6 × 6 are correct products, "
                   "but 4, 6 and 9 are not prime. 2 × 3 is only 6."))

    assert primes_of(100) == [2, 2, 5, 5] and ev("2 × 2 × 2 × 5 × 5") == 200
    its.append(mcq("Which is the prime factorisation of 100?", "2 × 2 × 5 × 5",
                   ["10 × 10", "2 × 5", "2 × 2 × 2 × 5 × 5"],
                   "100 = 10 × 10, and 10 = 2 × 5. So 100 = <b>2 × 2 × 5 × 5</b>. 10 is not prime, 2 × 5 = 10 and "
                   "2 × 2 × 2 × 5 × 5 = 200."))

    assert primes_of(32) == [2] * 5
    its.append(mcq("Which is the prime factorisation of 32?", "2 × 2 × 2 × 2 × 2",
                   ["2 × 16", "4 × 8", "2 × 2 × 2 × 2"],
                   "32 = 2 × 16 = 2 × 2 × 8 = 2 × 2 × 2 × 4 = <b>2 × 2 × 2 × 2 × 2</b>. 16, 4 and 8 are not prime, "
                   "and 2 × 2 × 2 × 2 = 16."))

    nm, he, his = P.next()
    assert 2 * 3 * 4 == 24
    its.append(mcq("%s writes 24 = 2 × 3 × 4 as the prime factorisation of 24. What is wrong?" % nm,
                   "4 is not prime", ["1 is missing", "It should be 2 × 12", "Nothing. It is right"],
                   "2 × 3 × 4 does equal 24, but 4 = 2 × 2 is not prime. The prime factorisation is "
                   "24 = 2 × 2 × 2 × 3. So the mistake is <b>4 is not prime</b>. 1 is never written."))

    assert primes_of(90) == [2, 3, 3, 5]
    its.append(mcq("What is the largest prime factor of 90?", 5, [9, 45, 3],
                   "90 = 2 × 3 × 3 × 5, so the prime factors are 2, 3 and 5. The largest is <b>5</b>. "
                   "9 and 45 are factors of 90, but they are not prime."))

    assert 60 % 8 and all(60 % v == 0 for v in (4, 15, 12))
    its.append(mcq("60 = 2 × 2 × 3 × 5. Which number is <b>not</b> a factor of 60?", 8, [4, 15, 12],
                   "8 = 2 × 2 × 2 needs three 2s, but 60 has only two, so <b>8</b> is not a factor. "
                   "4 = 2 × 2, 15 = 3 × 5 and 12 = 2 × 2 × 3 can all be made from the primes of 60."))

    assert primes_of(60) == [2, 2, 3, 5] and 6 * 10 == 60 == 4 * 15
    its.append(mcq("Two students start factor trees for 60. One starts 6 × 10, the other starts 4 × 15. Which is true?",
                   "Both end with 2, 2, 3 and 5", ["They end with different primes", "Only 6 × 10 works",
                                                   "Only 4 × 15 works"],
                   "6 × 10 = 2 × 3 × 2 × 5 and 4 × 15 = 2 × 2 × 3 × 5. <b>Both trees end with 2, 2, 3 and 5.</b> "
                   "Every number has only one prime factorisation, whichever pair you start with."))

    assert primes_of(144) == [2, 2, 2, 2, 3, 3] and (2 * 2 * 3) ** 2 == 144
    its.append(mcq("144 = 2 × 2 × 2 × 2 × 3 × 3. Use this to find √144.", 12, [72, 6, 24],
                   "Split the primes into two equal groups: (2 × 2 × 3) × (2 × 2 × 3) = 12 × 12. So √144 = <b>12</b>. "
                   "72 is half of 144, and 6 × 6 = 36."))
    assert len(its) == 20, len(its)
    return {"title": "Prime factorisation and factor trees", "items": its}


# ============================================================ set 4: properties that simplify calculations
def set_simplify(P):
    its = []

    def q_prod(expr, right, wrong, e):
        assert ev(expr) == right, (expr, right)
        assert right not in wrong
        its.append(mcq("Work out %s" % expr, num(right), [num(w) for w in wrong], e))

    q_prod("25 × 7 × 4", 700, [175, 36, 7000],
           "Multiply the friendly pair first: 25 × 4 = 100, then 100 × 7 = <b>700</b>. "
           "175 is only 25 × 7, 36 is 25 + 7 + 4, and 7000 has one zero too many.")
    q_prod("5 × 13 × 2", 130, [65, 20, 1300],
           "5 × 2 = 10, then 10 × 13 = <b>130</b>. 65 is only 5 × 13, 20 is 5 + 13 + 2, and 1300 is 100 × 13.")
    q_prod("4 × 19 × 25", 1900, [475, 48, 190],
           "4 × 25 = 100, then 100 × 19 = <b>1900</b>. 475 is only 19 × 25, 48 is 4 + 19 + 25, and 190 is 10 × 19.")
    q_prod("2 × 17 × 50", 1700, [850, 69, 170],
           "2 × 50 = 100, then 100 × 17 = <b>1700</b>. 850 is only 17 × 50, 69 is 2 + 17 + 50, and 170 is 10 × 17.")
    q_prod("2 × 2 × 5 × 5 × 3", 300, [17, 100, 150],
           "Pair each 2 with a 5: (2 × 5) × (2 × 5) × 3 = 10 × 10 × 3 = <b>300</b>. 17 is the sum, 100 leaves out "
           "the 3, and 150 uses only one 2.")
    q_prod("125 × 8", 1000, [10000, 133, 250],
           "8 = 2 × 2 × 2, so double three times: 125 → 250 → 500 → <b>1000</b>. 250 doubles only once, "
           "10 000 has one zero too many, and 133 is 125 + 8.")

    assert 16 * 25 == 400
    its.append(mcq("Use 16 = 4 × 4 to work out 16 × 25.", 400, [100, 41, 4000],
                   "16 × 25 = 4 × 4 × 25 = 4 × 100 = <b>400</b>. 100 forgets the other 4, and 41 is 16 + 25."))
    assert 35 * 4 == 140
    its.append(mcq("Use 4 = 2 × 2 to work out 35 × 4 by doubling twice.", 140, [70, 280, 39],
                   "35 × 2 = 70, then 70 × 2 = <b>140</b>. 70 doubles only once, 280 doubles three times, "
                   "and 39 is 35 + 4."))
    assert 48 * 5 == 240
    its.append(mcq("Use 5 = 10 ÷ 2 to work out 48 × 5.", 240, [480, 2400, 53],
                   "48 × 10 = 480, then 480 ÷ 2 = <b>240</b>. 480 forgets to halve, 2400 is 48 × 50, and 53 is 48 + 5."))
    nm, he, his = P.next()
    assert 6 * 45 == 3 * 90 == 270
    its.append(mcq("%s works out 6 × 45 as 3 × 90 (halve one number, double the other). What is the answer?" % nm,
                   270, [135, 540, 93],
                   "6 × 45 = 3 × 90 = <b>270</b>. Halving 6 and doubling 45 keeps the answer the same. 135 halves "
                   "without doubling, 540 doubles without halving, and 93 is 3 + 90."))
    assert 14 * 15 == 7 * 30 and 7 * 15 != 210 and 28 * 30 != 210 and 15 * 15 != 210
    its.append(mcq("Which is equal to 14 × 15?", "7 × 30", ["7 × 15", "28 × 30", "15 × 15"],
                   "Halve 14 and double 15: <b>7 × 30</b> = 210, the same as 14 × 15. 7 × 15 = 105 only halves, "
                   "28 × 30 = 840 doubles both, and 15 × 15 = 225."))

    assert 25 * 36 == 900
    its.append(mcq("Use 36 = 4 × 9 to work out 25 × 36.", 900, [450, 225, 9000],
                   "25 × 36 = 25 × 4 × 9 = 100 × 9 = <b>900</b>. 450 is 25 × 18, 225 is 25 × 9 (forgetting the 4), "
                   "and 9000 has one zero too many."))
    assert 25 * 24 == 600
    its.append(mcq("Use 24 = 4 × 6 to work out 25 × 24.", 600, [6000, 150, 49],
                   "25 × 24 = 25 × 4 × 6 = 100 × 6 = <b>600</b>. 150 is 25 × 6 (forgetting the 4), 6000 has one zero "
                   "too many, and 49 is 25 + 24."))

    assert 20 ** 2 == 400
    its.append(mcq("What is %s?" % sup(20), 400, [40, 4000, 22],
                   "%s = 20 × 20 = 2 × 2 × 10 × 10 = 4 × 100 = <b>400</b>. 40 is 20 × 2, 22 is 20 + 2, "
                   "and 4000 has one zero too many." % sup(20)))
    assert 80 * 80 == 6400
    its.append(mcq("8 × 8 = 64. Use this to work out 80 × 80.", 6400, [640, 64000, 160],
                   "80 × 80 = 8 × 8 × 10 × 10 = 64 × 100 = <b>6400</b>. 640 multiplies by only one 10, %s by 1000, "
                   "and 160 is 80 × 2." % num(64000)))
    its[-1]["c"] = [num(v) if v.isdigit() else v for v in its[-1]["c"]]

    assert 3 ** 2 * 2 ** 2 == 36 == 6 ** 2
    its.append(mcq("Work out %s × %s" % (sup(3), sup(2)), 36, [13, 25, 12],
                   "%s × %s = 9 × 4 = <b>36</b>. It is also (3 × 2) × (3 × 2) = %s. 13 is 9 + 4, 25 is %s "
                   "(3 + 2 = 5), and 12 is 3 × 2 × 2." % (sup(3), sup(2), sup(6), sup(5))))
    assert 5 ** 2 * 4 == 100
    its.append(mcq("Work out %s × 4" % sup(5), 100, [40, 400, 29],
                   "%s = 25, and 25 × 4 = <b>100</b>. 40 comes from 5 × 2 × 4, 400 is 20 × 20, and 29 is 25 + 4."
                   % sup(5)))

    good, bad = "2 × 2 × 5 × 5", ["2 × 5 × 5", "2 × 2 × 2 × 5", "3 × 5 × 5"]
    assert is_sq(ev(good)) and not any(is_sq(ev(b)) for b in bad)
    its.append(mcq("Which product is a square number?", good, bad,
                   "In a square number every prime comes in pairs. 2 × 2 × 5 × 5 = (2 × 5) × (2 × 5) = 10 × 10 = 100, "
                   "so <b>2 × 2 × 5 × 5</b> is square. 2 × 5 × 5 = 50, 2 × 2 × 2 × 5 = 40 and 3 × 5 × 5 = 75."))

    assert 84 == 2 * 2 * 3 * 7 and 12 == 2 * 2 * 3 and 84 // 12 == 7
    its.append(mcq("84 = 2 × 2 × 3 × 7 and 12 = 2 × 2 × 3. Use this to work out 84 ÷ 12.", 7, [6, 8, 72],
                   "12 uses the 2, 2 and 3 from 84. The prime left over is 7, so 84 ÷ 12 = <b>7</b>. "
                   "Check: 12 × 7 = 84. 72 is 84 − 12."))

    assert 7 * 11 * 13 == 1001 and 1001 // 77 == 13
    its.append(mcq("7 × 11 × 13 = 1001. Use this to work out 1001 ÷ 77.", 13, [11, 7, 91],
                   "77 = 7 × 11. Take the 7 and the 11 away from 7 × 11 × 13, and <b>13</b> is left. So 1001 ÷ 77 = 13. "
                   "91 is 7 × 13, which is 1001 ÷ 11."))
    assert len(its) == 20, len(its)
    return {"title": "Using properties to simplify calculations", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    assert isqrt(36) == 6
    its.append(mcq("The 36 students in a Year 6 class stand in a square array for the class photo. "
                   "How many students are in each row?", "6 students", ["9 students", "18 students", "12 students"],
                   "A square array has the same number of rows and columns. 6 × 6 = 36, so there are <b>6 students</b> "
                   "in each row. 9 comes from 36 ÷ 4 and 18 from 36 ÷ 2. 3 rows of 12 is a rectangle, not a square."))

    nm, he, his = P.next()
    assert 49 + 15 == 64 and 8 * 8 == 64
    its.append(mcq(fig(square_svg(7, cell=13)) + "%s sets out 49 chairs in a square: 7 rows of 7. %s wants to make the "
                   "next bigger square. How many more chairs does %s need?" % (nm, cap(he), he),
                   "15 chairs", ["8 chairs", "7 chairs", "64 chairs"],
                   "The next square is 8 rows of 8 = 64 chairs. 64 − 49 = <b>15 chairs</b>. Adding one row of 7 or 8 "
                   "is not enough: the square needs an extra row <b>and</b> an extra column."))

    assert is_prime(23) and all(is_comp(v) for v in (24, 25, 21))
    its.append(mcq("A teacher wants to set out chairs in equal rows, with more than one row and more than one chair "
                   "in each row. Which number of chairs <b>cannot</b> be set out this way?", "23 chairs",
                   ["24 chairs", "25 chairs", "21 chairs"],
                   "23 is prime: its only factors are 1 and 23, so the only array is 1 row of 23. "
                   "<b>23 chairs</b> cannot work. 24 = 4 × 6, 25 = 5 × 5 and 21 = 3 × 7."))

    nm, he, his = P.next()
    assert is_prime(29)
    its.append(mcq("%s has 29 counters. %s can only arrange them in 1 row of 29. Why?" % (nm, cap(he)),
                   "29 is prime", ["29 is odd", "29 is composite", "29 is a square number"],
                   "29 has exactly two factors, 1 and 29, so <b>29 is prime</b> and the only array is 1 × 29. "
                   "Being odd is not the reason: 27 is odd and makes 3 rows of 9."))

    assert isqrt(144) == 12
    its.append(mcq("At the athletics carnival, 144 students march in as a square: the same number of rows as "
                   "students in each row. How many rows are there?", "12 rows", ["36 rows", "72 rows", "11 rows"],
                   "12 × 12 = 144, so there are <b>12 rows</b> of 12 students. 36 is 144 ÷ 4, 72 is 144 ÷ 2, and 11 × 11 = 121 is too few."))

    assert isqrt(64) == 8 and 4 * 8 == 32
    its.append(mcq("A square vegetable garden at school has an area of 64 m<sup>2</sup>. How much fencing is needed "
                   "to go all the way around it?", "32 m", ["16 m", "8 m", "256 m"],
                   "Side × side = 64, and 8 × 8 = 64, so each side is 8 m. The perimeter is 4 × 8 = <b>32 m</b>. "
                   "16 m is 64 ÷ 4, 8 m is only one side, and 256 is 64 × 4."))

    nm, he, his = P.next()
    ans = [v for v in range(21, 30) if is_prime(v) and sum(map(int, str(v))) == 11]
    assert ans == [29] and is_prime(23) and not is_prime(27) and not is_prime(38)
    its.append(mcq("%s thinks of a prime number between 20 and 30. Its digits add up to 11. What is the number?" % nm,
                   29, [38, 23, 27],
                   "The primes between 20 and 30 are 23 and 29. 2 + 9 = 11, so the number is <b>29</b>. "
                   "2 + 3 = 5, 27 = 3 × 9 is not prime, and 38 is not between 20 and 30."))

    ans = [v for v in range(51, 90) if is_sq(v) and v % 2]
    assert ans == [81]
    its.append(mcq("I am a square number between 50 and 90. I am odd. What number am I?", 81, [64, 49, 63],
                   "The square numbers between 50 and 90 are 64 (8 × 8) and 81 (9 × 9). 64 is even, so the number is "
                   "<b>81</b>. 49 is below 50, and 63 is not a square number."))

    ans = [v for v in range(21, 50) if is_sq(v) and v % 4 == 0]
    assert ans == [36]
    its.append(mcq("I am a square number between 20 and 50. I am also a multiple of 4. What number am I?", 36,
                   [24, 25, 16],
                   "The square numbers between 20 and 50 are 25, 36 and 49. Only <b>36</b> is a multiple of 4 "
                   "(4 × 9 = 36). 24 is not square, 25 is not a multiple of 4, and 16 is less than 20."))

    nm, he, his = P.next()
    assert is_comp(15) and all(is_prime(v) for v in (3, 7, 13))
    its.append(mcq("%s says every odd number is prime. Which number shows %s is wrong?" % (nm, he), 15, [3, 7, 13],
                   "15 is odd, but 15 = 3 × 5, so it is composite. <b>15</b> shows the statement is wrong. "
                   "3, 7 and 13 are odd and prime, so they do not prove anything."))

    good, bad = (3, 17), [(1, 19), (9, 11), (5, 15)]
    assert sum(good) == 20 and all(is_prime(v) for v in good)
    assert all(sum(p) == 20 and not all(is_prime(v) for v in p) for p in bad)
    its.append(mcq("Which pair of prime numbers adds up to 20?", "3 and 17", ["%d and %d" % p for p in bad],
                   "3 and 17 are both prime, and 3 + 17 = <b>20</b>. 1 is not prime, 9 = 3 × 3 and 15 = 3 × 5."))

    nm, he, his = P.next()
    ans = [v for v in factors(36) if is_sq(v) and 5 < v < 20]
    assert ans == [9] and 36 % 16 and not is_sq(12) and not is_sq(6)
    its.append(mcq("%s is thinking of a number between 5 and 20. It is a factor of 36 and a square number. "
                   "What is the number?" % nm, 9, [16, 12, 6],
                   "The factors of 36 between 5 and 20 are 6, 9, 12 and 18. Only <b>9</b> is square (3 × 3). "
                   "16 is square but 36 ÷ 16 does not work, and 12 and 6 are not square."))

    nm, he, his = P.next()
    assert 7 * 7 <= 50 < 8 * 8
    its.append(mcq("%s has 50 square tiles. What is the biggest square %s can make with them?" % (nm, he),
                   "7 tiles by 7 tiles", ["5 tiles by 10 tiles", "8 tiles by 8 tiles", "25 tiles by 25 tiles"],
                   "7 × 7 = 49 tiles fits (1 tile is left over), but 8 × 8 = 64 needs too many. So the answer is "
                   "<b>7 tiles by 7 tiles</b>. 5 by 10 is a rectangle, not a square, and 25 is half of 50."))

    assert 72 % 3 == 0 and 72 % 5 and 72 % 7 and 72 % 9 == 0 and not is_prime(9)
    its.append(mcq("72 students go on a school excursion. They split into equal groups, and the number in each group "
                   "is a prime number. How many students could be in each group?", "3 students",
                   ["5 students", "7 students", "9 students"],
                   "72 = 2 × 2 × 2 × 3 × 3, so its prime factors are 2 and 3. Groups of <b>3 students</b> work "
                   "(24 groups). 72 ÷ 5 and 72 ÷ 7 leave a remainder, and 9 works but is not prime."))

    nm, he, his = P.next()
    assert 77 == 7 * 11 and is_prime(11)
    its.append(mcq("%s’s locker number is a prime factor of 77, and it is bigger than 10. What is %s locker number?"
                   % (nm, his), 11, [7, 77, 13],
                   "77 = 7 × 11, so the prime factors of 77 are 7 and 11. The one bigger than 10 is <b>11</b>. "
                   "77 is not prime, and 13 is not a factor of 77."))

    assert 4 * 25 * 9 == 900
    its.append(mcq("For the sausage sizzle, each of 9 classes gets 4 packs of 25 sausages. How many sausages is that "
                   "altogether?", "900 sausages", ["225 sausages", "38 sausages", "9000 sausages"],
                   "4 × 25 = 100 sausages for each class, and 100 × 9 = <b>900 sausages</b>. 225 forgets the 4 packs "
                   "(9 × 25), 9000 has one zero too many, and 38 is 9 + 4 + 25."))

    assert 25 * 12 == 300
    its.append(mcq("The school orders 25 boxes of pencils. Each box has 12 pencils. Use 12 = 4 × 3 to find how many "
                   "pencils there are.", "300 pencils", ["3000 pencils", "37 pencils", "100 pencils"],
                   "25 × 12 = 25 × 4 × 3 = 100 × 3 = <b>300 pencils</b>. 100 forgets the × 3, 3000 has one zero too many, and 37 is 25 + 12."))

    nm, he, his = P.next()
    assert 84 == 2 * 2 * 3 * 7 and 84 % 12 == 0 and all(84 % v for v in (8, 9, 10))
    its.append(mcq("There are 84 students in Year 6 (84 = 2 × 2 × 3 × 7). %s wants equal teams with no one left out. "
                   "Which team size works?" % nm, "12 students", ["8 students", "9 students", "10 students"],
                   "12 = 2 × 2 × 3 is made from the primes of 84, so <b>12 students</b> works (7 teams). 8 needs three "
                   "2s, 9 needs two 3s and 10 needs a 5, and 84 does not have them."))

    assert 15 * 15 == 225 and 225 - 180 == 45
    its.append(mcq("The school hall has 15 rows of 15 chairs. 180 people come to the concert. How many chairs are "
                   "empty?", "45 chairs", ["35 chairs", "15 chairs", "225 chairs"],
                   "15 × 15 = %s = 225 chairs. 225 − 180 = <b>45 chairs</b> are empty. 35 comes from 15 × 15 = 215, "
                   "15 is one row, and 225 is all the chairs." % sup(15)))

    good, bad = (36, 64), [(50, 50), (25, 75), (19, 81)]
    assert sum(good) == 100 and all(is_sq(v) for v in good)
    assert all(sum(p) == 100 and not all(is_sq(v) for v in p) for p in bad)
    its.append(mcq("Which two square numbers add up to 100?", "36 and 64", ["%d and %d" % p for p in bad],
                   "36 = 6 × 6 and 64 = 8 × 8, and 36 + 64 = <b>100</b>. 50 and 75 are not square, and 19 is not "
                   "square (81 is)."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with prime and square numbers", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Prime and composite numbers</h2>"
        "<p>A <b>prime number</b> has exactly two factors: 1 and itself. A <b>composite number</b> has more than "
        "two factors. 1 is <b>neither</b>, because it has only one factor. 2 is the only even prime.</p>"
        "<p>A composite number can be set out as a rectangle with more than one row. A prime number can only make "
        "one row.</p>"
        "<figure class='sn-fig'>" + arrays_svg() +
        "<figcaption>12 makes 3 × 4 and 2 × 6, so 12 is composite. 13 only makes 1 × 13, so 13 is prime.</figcaption></figure>"
        + table(["Prime numbers to 50"], [["2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47"]])
        + "<p>Odd does not mean prime: 9 = 3 × 3, 27 = 3 × 9, 51 = 3 × 17, 57 = 3 × 19 and 91 = 7 × 13.</p>"
        + ex("Example", "Is 39 prime or composite?",
             "Test small primes. 39 ÷ 3 = 13, so 39 = 3 × 13. Its factors are 1, 3, 13 and 39.", "composite")
        + "<h2>Square numbers and square roots</h2>"
        "<p>A <b>square number</b> is a number times itself. Its dots make a square array. "
        "We write 5 × 5 as 5<sup>2</sup> (“5 squared”).</p>"
        "<figure class='sn-fig'>" + squares_row_svg() +
        "<figcaption>Square numbers make square arrays: 1, 4, 9, 16 …</figcaption></figure>"
        + table(["n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                [["n<sup>2</sup>"] + [str(k * k) for k in range(1, 13)]])
        + "<p>The <b>square root</b> undoes squaring. √49 = 7, because 7 × 7 = 49.</p>"
        + ex("Example", "A square has an area of 81 cm<sup>2</sup>. How long is each side?",
             "Side × side = 81. 9 × 9 = 81, so √81 = 9.", "9 cm")
        + "<h2>Prime factorisation</h2>"
        "<p>Every composite number can be written as a product of primes. Use a <b>factor tree</b>: split the "
        "number into a factor pair, and keep splitting until every branch ends in a prime.</p>"
        "<figure class='sn-fig'>" + tree_svg(T(60, T(6, 2, 3), T(10, 2, 5))) +
        "<figcaption>60 = 6 × 10 = 2 × 3 × 2 × 5. In order: 60 = 2 × 2 × 3 × 5. Starting with 4 × 15 gives the "
        "same primes.</figcaption></figure>"
        + "<h2>Using the properties to simplify calculations</h2>"
        "<p>Split numbers into factors and multiply a friendly pair first: 2 × 5 = 10, 4 × 25 = 100, 8 × 125 = 1000.</p>"
        + ex("Example 1", "Work out 25 × 4 × 7.", "25 × 4 = 100, then 100 × 7 = 700.", "700")
        + ex("Example 2", "Work out 16 × 25.", "16 = 4 × 4, so 16 × 25 = 4 × 4 × 25 = 4 × 100.", "400")
        + "<p>In a square number every prime comes in pairs: 36 = 2 × 2 × 3 × 3 = (2 × 3) × (2 × 3) = 6 × 6.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Saying 1 is prime", "A prime has exactly two factors. 1 has only one, so it is neither"],
            ["Saying 9 or 57 is prime because it is odd", "Test small primes: 9 = 3 × 3, 57 = 3 × 19"],
            ["Saying 2 is composite because it is even", "2 has two factors, 1 and 2. It is the only even prime"],
            ["4<sup>2</sup> = 8", "4<sup>2</sup> = 4 × 4 = 16, not 4 × 2"],
            ["√64 = 32", "Do not halve. 8 × 8 = 64, so √64 = 8"],
            ["24 = 2 × 3 × 4", "4 is not prime. Keep splitting: 24 = 2 × 2 × 2 × 3"],
        ])
    )


FAQ = [
    {"q": "What is the difference between prime and composite numbers?",
     "a": "A prime number has exactly two factors, 1 and itself (for example 7). A composite number has more than two factors (for example 8 = 1, 2, 4, 8)."},
    {"q": "Is 1 a prime number?",
     "a": "No. 1 has only one factor, so it is neither prime nor composite. The smallest prime number is 2, which is also the only even prime."},
    {"q": "What are the square numbers up to 144?",
     "a": "1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121 and 144. They are 1 × 1 up to 12 × 12, so knowing the multiplication facts makes them easy to find."},
    {"q": "When do students learn prime, composite and square numbers in the Australian Curriculum?",
     "a": "In Year 6 (AC9M6N02), students identify and describe prime, composite and square numbers and use them to solve problems. This prepares them for index notation and prime factorisation in Year 7 and the Year 7 NAPLAN numeracy test."},
]


def gen():
    rnd = random.Random(6802)
    P = People(rnd)
    sets = [set_prime_composite(P), set_squares(P), set_factor_trees(P), set_simplify(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "prime-composite-and-square-numbers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Prime, Composite and Square Numbers",
        "seo_title": "Year 6 Prime, Composite and Square Numbers Worksheets: Factor Trees and Square Roots",
        "short_title": "Prime, composite and square numbers",
        "domain": "Number",
        "standard_code": "AC9M6N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Identify and describe the properties of prime, composite and square numbers and use these properties to solve problems and simplify calculations",
        "meta_desc": "Free Year 6 maths worksheets on prime, composite and square numbers: factors, square arrays, square roots, prime factorisation with factor trees and using these properties to simplify calculations. 100 questions with an answer key, aligned to the Australian Curriculum.",
        "key_big": "A prime number has exactly two factors. A square number is a number times itself.",
        "key_sub": "1 is neither prime nor composite, and 2 is the only even prime. 4² = 4 × 4 = 16, not 8. A factor tree splits a number until every branch ends in a prime: 60 = 2 × 2 × 3 × 5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "factor tree")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
