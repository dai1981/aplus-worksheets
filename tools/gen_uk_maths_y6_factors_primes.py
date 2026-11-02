# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Factors, multiples and primes (National Curriculum in England)
  python3 tools/gen_uk_maths_y6_factors_primes.py
Identify common factors, common multiples and prime numbers, with a light recap of prime factors,
square numbers and cube numbers from Year 5.
Every factor, multiple, prime, HCF and LCM is checked in code.
Wrong answers come from real mistakes: 1 is prime, 9 / 27 / 51 / 91 are prime, 2 is not prime,
confusing factors and multiples, a × b as the LCM, a common factor that is not the highest, a missing
factor pair, 4³ = 12, writing 1 in a prime factor list.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from math import gcd, prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ maths
def n(x):
    """1,000 and above get a comma."""
    return "{:,}".format(int(x))


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


def cfs(a, b):
    return [d for d in factors(min(a, b)) if a % d == 0 and b % d == 0]


def lcm(a, b):
    return a * b // gcd(a, b)


def is_prime(x):
    return len(factors(x)) == 2


def primes_of(x):
    out, d = [], 2
    while x > 1:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    return out


def lst(xs):
    return ", ".join(n(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def mults(d, upto):
    return [d * k for k in range(1, upto // d + 1)]


def why_not_prime(x):
    """Short reason a number is not prime."""
    if x == 1:
        return "1 has only one factor, so it is not prime"
    s = pairs(x)[1]
    return "%d = %d × %d, so %d is not prime" % (x, s[0], s[1], x)


def sup(b, p):
    return "%d<sup>%d</sup>" % (b, p)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def split(x):
    """Most balanced factor pair of x (both > 1), or None if x is prime."""
    best = None
    for a in range(2, int(x ** 0.5) + 1):
        if x % a == 0:
            best = (a, x // a)
    return best


def tree(x):
    s = split(x)
    return (x, None) if s is None else (x, [tree(s[0]), tree(s[1])])


def leaves(t):
    return [t[0]] if t[1] is None else leaves(t[1][0]) + leaves(t[1][1])


def depth(t):
    return 1 if t[1] is None else 1 + max(depth(c) for c in t[1])


def tree_svg(x, step=44, dy=50):
    """Factor tree: each number splits into a factor pair; the primes at the ends are circled."""
    t = tree(x)
    assert prod(leaves(t)) == x
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

    def draw(node):
        px, py = pos[id(node)]
        if node[1] is not None:
            for c in node[1]:
                cx, cy = pos[id(c)]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                         % (px, py + 9, cx, cy - 15, GREY))
                draw(c)
        else:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (px, py, FILL, GREEN))
        s.append(text(px, py + 6, str(node[0]), 17))

    draw(t)
    return svg_wrap(W, H, "".join(s), "factor tree for %d" % x)


def rainbow_svg(x, step=40):
    """Factor rainbow: the factors of x in a row, each factor pair joined by an arc."""
    fs = factors(x)
    o, top = 20, 76
    W = (len(fs) - 1) * step + 2 * o
    xs = {f: o + i * step for i, f in enumerate(fs)}
    s = []
    ps = pairs(x)
    for k, (a, b) in enumerate(ps):
        if a == b:
            continue
        ry = 16 + 14 * (len(ps) - 1 - k)
        s.append("<path d='M %d %d A %d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xs[a], top, (xs[b] - xs[a]) // 2, ry, xs[b], top, GREEN))
    for f in fs:
        s.append(text(xs[f], top + 22, str(f), 18))
    return svg_wrap(W, top + 30, "".join(s), "factor rainbow for %d" % x)


def factor_rows_svg(a, b):
    """Lesson: the factors of a and b in two rows, the common ones circled, the HCF in red."""
    fa, fb = factors(a), factors(b)
    g = gcd(a, b)
    step, lx, o = 40, 66, 8
    cols = sorted(set(fa) | set(fb))
    W = lx + len(cols) * step + o
    H = 2 * 40 + 2 * o
    s = []
    for r, (v, fs) in enumerate([(a, fa), (b, fb)]):
        y = o + 26 + r * 40
        s.append(text(lx - 14, y, "%d:" % v, 17, anchor="end"))
        for d in fs:
            x = lx + cols.index(d) * step + step / 2
            if d in fa and d in fb:
                s.append("<circle cx='%.1f' cy='%d' r='16' fill='%s' stroke='%s' stroke-width='2'/>"
                         % (x, y - 6, "#f6d5d0" if d == g else FILL, RED if d == g else GREEN))
            s.append(text(x, y, str(d), 16, col=RED if d == g else INK))
    return svg_wrap(W, H, "".join(s), "factors of %d and %d with the common factors circled" % (a, b))


def multiples_svg(a, b, top):
    """Lesson: multiples of a and b placed by size on two rows; common multiples joined."""
    sc, ox = 8, 52
    W = ox + top * sc + 22
    H = 116
    ya, yb = 34, 92
    s = []
    for v, y in [(a, ya), (b, yb)]:
        s.append(text(ox - 22, y + 6, "%d:" % v, 17, anchor="end"))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (ox, y, ox + top * sc + 6, y, GREY))
    for m in range(lcm(a, b), top + 1, lcm(a, b)):
        x = ox + m * sc
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                 % (x, ya + 12, x, yb - 12, RED))
    for v, y, up in [(a, ya, True), (b, yb, False)]:
        for m in mults(v, top):
            x = ox + m * sc
            common = m % a == 0 and m % b == 0
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (x, y, RED if common else GREEN))
            s.append(text(x, y - 10 if up else y + 22, str(m), 14, col=RED if common else INK))
    return svg_wrap(W, H, "".join(s), "multiples of %d and %d up to %d" % (a, b, top))


def squares_svg(k=4, cell=14, gap=26):
    """Lesson: square numbers 1, 4, 9, 16 as squares of dots."""
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
    return svg_wrap(W, H, "".join(s), "square numbers 1, 4, 9 and 16 shown as squares of dots")


# ============================================================ set 1: factors, factor pairs and multiples
def set_factors(P):
    its = []
    for x, drop in [(18, (3, 6)), (28, (4, 7)), (36, (4, 9)), (40, (5, 8))]:
        fs = factors(x)
        right = lst(fs)
        missing = lst([d for d in fs if d not in drop])
        multi = lst([x * k for k in range(1, 5)])
        no_ends = lst(fs[1:-1])
        e = ("Find the factor pairs: %s. So the factors are <b>%s</b>. Do not forget 1 and %d, and do not miss %d × %d. "
             "%s are multiples of %d, not factors."
             % (", ".join("%d × %d" % p for p in pairs(x)), right, x, drop[0], drop[1], multi, x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, right, [missing, no_ends, multi], e))

    for x, bad, good in [(48, 18, [12, 16, 6]), (60, 8, [12, 15, 20]), (72, 16, [8, 12, 24]), (90, 20, [15, 18, 30])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d remainder %d, so <b>%d</b> is not a factor of %d. %s"
             % (x, bad, x // bad, x % bad, bad, x,
                " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for x, good, bad in [(84, 14, [16, 168, 24]), (96, 32, [36, 192, 28])]:
        assert x % good == 0 and all(x % b for b in bad) and bad[1] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a multiple of %d, not a factor, and %d and %d "
             "leave a remainder." % (good, x // good, x, good, x, bad[1], x, bad[0], bad[2]))
        its.append(mcq("Which number is a factor of %d?" % x, good, bad, e))

    k = len(pairs(36))
    assert k == 5 and len(factors(36)) == 9
    its.append(mcq("How many factor pairs does 36 have?", 5, [4, 9, 6],
                   "1 × 36, 2 × 18, 3 × 12, 4 × 9 and 6 × 6. That is <b>5</b> factor pairs. 6 × 6 counts as a pair, "
                   "and 9 is the number of factors, not pairs."))

    nm, he, his = P.next()
    shown = [(1, 72), (2, 36), (3, 24), (6, 12), (8, 9)]
    assert sorted(shown + [(4, 18)]) == pairs(72)
    its.append(mcq("%s lists the factor pairs of 72: %s. Which pair did %s miss?"
                   % (nm, ", ".join("%d × %d" % p for p in shown), he), "4 × 18", ["9 × 8", "7 × 10", "5 × 14"],
                   "Test 1, 2, 3, 4 … in order. 72 ÷ 4 = 18, so <b>4 × 18</b> is missing. 9 × 8 is the same pair as 8 × 9, "
                   "and 7 × 10 and 5 × 14 both make 70, not 72."))

    for v, right, wrong in [(7, 63, [27, 17, 57]), (8, 96, [58, 18, 84]), (9, 108, [109, 98, 119])]:
        assert right % v == 0 and all(w % v for w in wrong)
        e = "%d × %d = %d, so <b>%d</b> is a multiple of %d. %s" % (
            v, right // v, right, right, v,
            " ".join("%d ÷ %d = %d remainder %d." % (w, v, w // v, w % v) for w in wrong))
        if v == 7:
            e += " Having a 7 as a digit does not make a number a multiple of 7."
        if v == 8:
            e += " 84 is in the 4 and 12 times tables, but not the 8 times table."
        its.append(mcq("Which number is a multiple of %d?" % v, right, wrong, e))

    assert 63 % 6 and all(x % 6 == 0 for x in (42, 54, 72))
    its.append(mcq("Which number is <b>not</b> a multiple of 6?", 63, [42, 54, 72],
                   "Multiples of 6 are even. 63 is odd, so <b>63</b> is not a multiple of 6 (it is a multiple of 3, 7 and 9). "
                   "6 × 7 = 42, 6 × 9 = 54 and 6 × 12 = 72."))

    assert 7 * 12 == 84
    its.append(mcq("What is the 12th multiple of 7?", 84, [77, 91, 19],
                   "The 12th multiple of 7 is 7 × 12 = <b>84</b>. 77 is the 11th multiple, 91 is the 13th, and 19 is 7 + 12."))

    its.append(mcq("Which list shows the first five multiples of 6?", "6, 12, 18, 24, 30",
                   ["1, 2, 3, 6", "12, 18, 24, 30, 36", "6, 16, 26, 36, 46"],
                   "The multiples of 6 are 6 × 1, 6 × 2, 6 × 3 …: <b>6, 12, 18, 24, 30</b>. The first multiple is 6 itself. "
                   "1, 2, 3, 6 are the factors of 6."))

    nm, he, his = P.next()
    its.append(mcq("%s says 4 is a multiple of 12. Is %s right?" % (nm, he), "No. 4 is a factor of 12",
                   ["Yes. 4 × 3 = 12", "Yes. 12 ÷ 4 = 3", "No. 4 is a prime number"],
                   "4 × 3 = 12, so 4 is a <b>factor</b> of 12 and 12 is a multiple of 4. A factor divides the number; "
                   "a multiple is in its times table. 4 is not prime: 4 = 2 × 2."))

    its.append(mcq("Which statement is true?", "36 is a multiple of 9",
                   ["9 is a multiple of 36", "36 is a factor of 9", "8 is a factor of 36"],
                   "9 × 4 = 36, so <b>36 is a multiple of 9</b> (and 9 is a factor of 36). 36 ÷ 8 = 4 remainder 4, "
                   "so 8 is not a factor of 36."))
    assert 36 % 8
    assert len(its) == 20, len(its)
    return {"title": "Factors, factor pairs and multiples", "items": its}


# ============================================================ set 2: prime, square and cube numbers
def set_primes(P):
    its = []
    for right, wrong in [(23, [21, 27, 1]), (37, [39, 57, 33]), (53, [51, 49, 9]), (41, [91, 87, 81])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("%d has exactly two factors, 1 and %d, so <b>%d</b> is prime. " % (right, right, right)
             + ". ".join(cap(why_not_prime(w)) for w in wrong) + ".")
        its.append(mcq("Which of these is a prime number?", right, wrong, e))

    for right, wrong in [(1, [2, 3, 5]), (51, [2, 53, 47]), (91, [89, 97, 31])]:
        assert not is_prime(right) and all(is_prime(w) for w in wrong)
        e = cap(why_not_prime(right)).replace(str(right) + " is not", "<b>%d</b> is not" % right, 1) + ". "
        e += "%s are prime: each has exactly two factors." % ", ".join(str(w) for w in wrong[:-1]) + ""
        e = e.replace(" are prime", " and %d are prime" % wrong[-1])
        if 2 in wrong:
            e += " 2 is prime, even though it is even."
        its.append(mcq("Which number is <b>not</b> a prime number?", right, wrong, e))

    for x in [24, 60, 45]:
        ps = sorted(leaves(tree(x)))
        assert all(is_prime(p) for p in ps) and prod(ps) == x
        first = times(split(x))
        once = times(sorted(set(ps)))
        with1 = times([1] + ps)
        e = ("Keep splitting until every branch ends in a prime: %d = <b>%s</b>. %s is not finished, because %s "
             "not prime. 1 is not prime, so it is not written."
             % (x, times(ps), first,
                " and ".join(str(v) for v in split(x) if not is_prime(v)) +
                (" are" if sum(not is_prime(v) for v in split(x)) > 1 else " is")))
        its.append(mcq(fig(tree_svg(x)) + "Which shows %d as a product of prime factors?" % x, times(ps),
                       [first, once, with1], e))

    assert primes_of(30) == [2, 3, 5]
    its.append(mcq("What are the prime factors of 30?", "2, 3 and 5", ["1, 2, 3 and 5", "5 and 6", "2 and 15"],
                   "30 = 2 × 3 × 5, and 2, 3 and 5 are all prime. So the prime factors are <b>2, 3 and 5</b>. "
                   "1 is not prime, 6 = 2 × 3 and 15 = 3 × 5."))

    ps = [p for p in range(10, 21) if is_prime(p)]
    assert ps == [11, 13, 17, 19]
    its.append(mcq("How many prime numbers are there between 10 and 20?", 4, [5, 3, 6],
                   "The primes are 11, 13, 17 and 19: <b>4</b> primes. 15 is odd but not prime (15 = 3 × 5)."))

    nm, he, his = P.next()
    its.append(mcq("%s says 1 is a prime number. Is %s right?" % (nm, he), "No. 1 has only one factor",
                   ["Yes. 1 divides by itself", "Yes. 1 is an odd number", "No. 1 is a composite number"],
                   "A prime number has <b>exactly two</b> factors: 1 and itself. 1 has only one factor, so it is not prime. "
                   "It is not composite either."))
    nm, he, his = P.next()
    its.append(mcq("%s says 2 is not a prime number because it is even. Is %s right?" % (nm, he),
                   "No. 2 has exactly two factors",
                   ["Yes. All primes are odd", "Yes. 2 has only one factor", "No. 2 is a square number"],
                   "The factors of 2 are 1 and 2, so <b>2 is prime</b>. It is the only even prime: every other even "
                   "number can be divided by 2."))

    # square and cube numbers (Year 5 recap)
    sq = lambda v: int(v ** 0.5) ** 2 == v
    cube = lambda v: round(v ** (1 / 3)) ** 3 == v
    assert sq(49) and not any(sq(w) for w in (14, 27, 50))
    its.append(mcq("Which of these is a square number?", 49, [14, 27, 50],
                   "7 × 7 = <b>49</b>, so 49 is a square number. 14 is 7 × 2, 27 is a cube number (3 × 3 × 3), "
                   "and 50 is between 7 × 7 and 8 × 8."))
    its.append(mcq("What is %s?" % sup(6, 2), 36, [12, 8, 216],
                   "6<sup>2</sup> means 6 × 6 = <b>36</b>. It does not mean 6 × 2 = 12 or 6 + 2 = 8. "
                   "216 is 6<sup>3</sup>."))
    its.append(mcq("What is %s?" % sup(4, 3), 64, [12, 16, 7],
                   "4<sup>3</sup> means 4 × 4 × 4 = 16 × 4 = <b>64</b>. 12 is 4 × 3, 16 is 4<sup>2</sup>, and 7 is 4 + 3."))
    assert sq(64) and cube(64) and sq(16) and not cube(16) and cube(27) and not sq(27) and cube(8) and not sq(8)
    its.append(mcq("Which number is both a square number and a cube number?", 64, [16, 27, 8],
                   "64 = 8 × 8 and 64 = 4 × 4 × 4, so <b>64</b> is both. 16 = 4 × 4 is only square. "
                   "27 = 3 × 3 × 3 and 8 = 2 × 2 × 2 are only cube numbers."))
    its.append(mcq("Which list shows the first five cube numbers?", "1, 8, 27, 64, 125",
                   ["3, 6, 9, 12, 15", "1, 4, 9, 16, 25", "8, 27, 64, 125, 216"],
                   "1 × 1 × 1 = 1, 2 × 2 × 2 = 8, 3 × 3 × 3 = 27, 4 × 4 × 4 = 64, 5 × 5 × 5 = 125. "
                   "The first cube number is <b>1</b>. 1, 4, 9, 16, 25 are the square numbers."))
    assert 5 ** 2 + 2 ** 3 == 33
    its.append(mcq("Work out %s + %s" % (sup(5, 2), sup(2, 3)), 33, [16, 31, 18],
                   "5<sup>2</sup> = 5 × 5 = 25 and 2<sup>3</sup> = 2 × 2 × 2 = 8. 25 + 8 = <b>33</b>. "
                   "16 comes from 5 × 2 + 2 × 3, 18 from 5 × 2 + 8, and 31 from using 2 × 3 = 6."))
    assert len(its) == 20, len(its)
    return {"title": "Prime, square and cube numbers", "items": its}


# ============================================================ set 3: common factors and the HCF
def hcf_e(a, b):
    return ("Factors of %d: %s. Factors of %d: %s. Common factors: %s. The highest is <b>%d</b>."
            % (a, lst(factors(a)), b, lst(factors(b)), lst(cfs(a, b)), gcd(a, b)))


def one_only(a, b):
    """Biggest factor of the smaller number (less than it) that is NOT a factor of the other number."""
    s, l = min(a, b), max(a, b)
    xs = [d for d in factors(s) if l % d and d < s]
    return xs[-1] if xs else None


def set_hcf(P):
    its = []
    for a, b in [(12, 18), (16, 40), (24, 36)]:
        c = cfs(a, b)
        e = hcf_e(a, b) + " Keep 1 and the highest common factor in the list, and use only numbers that divide <b>both</b>."
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c),
                       [lst(c[:-1]), lst(factors(min(a, b))), lst(c[1:])], e))

    for a, b, right, wrong in [(36, 54, 9, [4, 27, 108]), (42, 60, 6, [7, 10, 420])]:
        assert a % right == 0 and b % right == 0
        assert a % wrong[0] == 0 and b % wrong[0] and b % wrong[1] == 0 and a % wrong[1] and wrong[2] == lcm(a, b)
        e = ("%d × %d = %d and %d × %d = %d, so <b>%d</b> is a common factor. %d is a factor of %d only, "
             "%d is a factor of %d only, and %d is a common <b>multiple</b>."
             % (right, a // right, a, right, b // right, b, right, wrong[0], a, wrong[1], b, wrong[2]))
        its.append(mcq("Which number is a common factor of %d and %d?" % (a, b), right, wrong, e))

    for a, b, bad, good in [(48, 80, 6, [2, 8, 16]), (60, 90, 4, [5, 6, 15])]:
        assert all(a % g == 0 and b % g == 0 for g in good) and (a % bad == 0) != (b % bad == 0)
        only = a if a % bad == 0 else b
        other = b if only == a else a
        e = ("%d is a factor of %d, but %d ÷ %d = %d remainder %d, so <b>%d</b> is not a common factor. "
             "%d, %d and %d divide both numbers." % ((bad, only, other, bad, other // bad, other % bad, bad) + tuple(good)))
        its.append(mcq("Which number is <b>not</b> a common factor of %d and %d?" % (a, b), bad, good, e))

    first = True
    for a, b in [(14, 21), (20, 30), (18, 27), (13, 52), (9, 20), (28, 42), (48, 72), (36, 90), (54, 81)]:
        g = gcd(a, b)
        c = cfs(a, b)
        cands = []
        if len(c) > 1 and c[-2] > 1:
            cands.append(c[-2])
        if one_only(a, b):
            cands.append(one_only(a, b))
        if min(a, b) != g:
            cands.append(min(a, b))
        cands.append(lcm(a, b))
        big = [d for d in factors(max(a, b)) if min(a, b) % d and d < max(a, b)]
        cands += big[-1:] + [n(a * b)]
        e = hcf_e(a, b)
        if g == 1:
            e += " %d and %d share no factor except 1, so their HCF is 1." % (a, b)
        elif g == min(a, b):
            e += " %d divides %d (%d × %d = %d), so the smaller number is the HCF." % (a, b, a, b // a, b)
        elif len(c) > 1 and c[-2] > 1:
            e += " %d is a common factor too, but not the highest." % c[-2]
        else:
            e += " %d is a factor of %d only, so it is not a common factor." % (one_only(a, b), min(a, b))
        name = "highest common factor (HCF)" if first else "HCF"
        first = False
        its.append(mcq("What is the %s of %d and %d?" % (name, a, b), g, cands, e))

    nm, he, his = P.next()
    its.append(mcq("%s says the HCF of 30 and 45 is 5, because 5 is a factor of both. Is %s right?" % (nm, he),
                   "No. The HCF is 15", ["Yes. 5 divides both", "No. The HCF is 90", "No. The HCF is 30"],
                   "5 is a common factor, but not the highest. 15 × 2 = 30 and 15 × 3 = 45, so the HCF is <b>15</b>. "
                   "90 is the LCM, and 30 is not a factor of 45."))
    nm, he, his = P.next()
    its.append(mcq("%s says the HCF of 16 and 48 is 16. Is %s right?" % (nm, he),
                   "Yes. 16 divides 48", ["No. The HCF is 8", "No. It can’t be 16", "No. The HCF is 4"],
                   "16 × 3 = 48, so 16 is a factor of both numbers, and no factor of 16 is bigger than 16. "
                   "The HCF <b>can</b> be the smaller number."))
    assert gcd(30, 45) == 15 and gcd(16, 48) == 16

    good, bad = (8, 15), [(9, 15), (8, 14), (12, 15)]
    assert gcd(*good) == 1 and all(gcd(*p) > 1 for p in bad)
    its.append(mcq("Which pair of numbers has only 1 as a common factor?", "8 and 15", ["%d and %d" % p for p in bad],
                   "Factors of 8: 1, 2, 4, 8. Factors of 15: 1, 3, 5, 15. The only common factor is 1, so the answer is "
                   "<b>8 and 15</b>. 9 and 15 share 3, 8 and 14 share 2, and 12 and 15 share 3."))

    good, bad = (18, 24), [(12, 24), (2, 3), (24, 36)]
    assert gcd(*good) == 6 and all(gcd(*p) != 6 for p in bad) and 2 * 3 == 6
    its.append(mcq("Which pair of numbers has a highest common factor of 6?", "18 and 24",
                   ["%d and %d" % p for p in bad],
                   "18 = 6 × 3 and 24 = 6 × 4, and 3 and 4 share no factor except 1, so the HCF is <b>6</b>. "
                   "The HCF of 12 and 24 is 12, of 24 and 36 is 12, and 2 × 3 = 6 but the HCF of 2 and 3 is 1."))
    assert len(its) == 20, len(its)
    return {"title": "Common factors and the highest common factor", "items": its}


# ============================================================ set 4: common multiples and the LCM
def lcm_e(a, b):
    l = lcm(a, b)
    lo, hi = sorted((a, b))
    return ("Multiples of %d: %s. Multiples of %d: %s. The first number in both lists is <b>%d</b>."
            % (hi, lst(mults(hi, l)), lo, lst(mults(lo, l)), l))


def set_lcm(P):
    its = []
    for a, b in [(4, 6), (6, 9), (10, 12)]:
        l = lcm(a, b)
        right = [l, 2 * l, 3 * l]
        byprod = [a * b, 2 * a * b, 3 * a * b]
        mixed = [a, b, l]
        big = mults(b, 3 * b)
        e = (lcm_e(a, b) + " The common multiples are the multiples of the LCM: %s. "
             "Counting in %d × %d = %ds skips %d." % (lst(right), a, b, a * b, l))
        its.append(mcq("Which list shows the first 3 common multiples of %d and %d?" % (a, b), lst(right),
                       [lst(byprod), lst(mixed), lst(big)], e))

    first = True
    for a, b in [(3, 4), (4, 8), (4, 10), (6, 10), (5, 7), (8, 10), (9, 12), (4, 9), (6, 12), (3, 10)]:
        l = lcm(a, b)
        g = gcd(a, b)
        cands = []
        if a * b != l:
            cands.append(a * b)
        cands += [2 * l, max(a, b), a + b] if g == 1 else [2 * l, g, max(a, b), a + b]
        e = lcm_e(a, b)
        if a * b == l:
            e += " %d and %d share no factor except 1, so here the LCM is %d × %d." % (a, b, a, b)
        elif l == max(a, b):
            e += " %d is a multiple of %d, so the bigger number is the LCM." % (max(a, b), min(a, b))
        else:
            e += " %d × %d = %d is a common multiple, but not the lowest." % (a, b, a * b)
        name = "lowest common multiple (LCM)" if first else "LCM"
        first = False
        its.append(mcq("What is the %s of %d and %d?" % (name, a, b), l, cands, e))

    for a, b, right, wrong in [(3, 8, 48, [11, 32, 30]), (5, 6, 60, [11, 25, 36])]:
        assert right % a == 0 and right % b == 0 and wrong[0] == a + b
        assert all(w % a or w % b for w in wrong)
        e = ("%d = %d × %d and %d = %d × %d, so <b>%d</b> is a common multiple. %d is %d + %d. "
             "%d is a multiple of only one of the numbers, and so is %d."
             % (right, a, right // a, right, b, right // b, right, wrong[0], a, b, wrong[1], wrong[2]))
        its.append(mcq("Which number is a common multiple of %d and %d?" % (a, b), right, wrong, e))

    assert 30 % 4 and all(x % 4 == 0 and x % 10 == 0 for x in (20, 40, 60))
    its.append(mcq("Which number is <b>not</b> a common multiple of 4 and 10?", 30, [20, 40, 60],
                   "30 is a multiple of 10, but 30 ÷ 4 = 7 remainder 2, so <b>30</b> is not a multiple of 4. "
                   "The LCM of 4 and 10 is 20, and 20, 40 and 60 are all multiples of 20."))

    nm, he, his = P.next()
    its.append(mcq("%s says the LCM of 6 and 8 is 48, because 6 × 8 = 48. Is %s right?" % (nm, he),
                   "No. The LCM is 24", ["Yes. 6 × 8 = 48", "No. The LCM is 2", "No. The LCM is 14"],
                   lcm_e(6, 8) + " 48 is a common multiple, but not the lowest. 2 is the HCF, and 14 is 6 + 8."))
    nm, he, his = P.next()
    its.append(mcq("%s says the LCM of 5 and 10 is 50. Is %s right?" % (nm, he),
                   "No. The LCM is 10", ["Yes. 5 × 10 = 50", "No. The LCM is 5", "No. The LCM is 15"],
                   "10 is a multiple of 5 (5 × 2 = 10) and of 10, so the LCM is <b>10</b>. "
                   "When one number is a multiple of the other, the bigger number is the LCM."))
    assert lcm(6, 8) == 24 and lcm(5, 10) == 10

    pairs_ = ["5 and 8", "4 and 6", "6 and 9", "8 and 12"]
    ok = [lcm(*map(int, p.split(" and "))) == prod(map(int, p.split(" and "))) for p in pairs_]
    assert ok == [True, False, False, False]
    its.append(mcq("For which pair is the LCM equal to the two numbers multiplied together?", pairs_[0], pairs_[1:],
                   "5 and 8 share no factor except 1, so the LCM is 5 × 8 = <b>40</b>. The other pairs share a factor: "
                   "the LCM of 4 and 6 is 12 (not 24), of 6 and 9 is 18 (not 54), and of 8 and 12 is 24 (not 96)."))

    good, bad = "6 and 8", ["4 and 6", "2 and 12", "6 and 12"]
    assert lcm(6, 8) == 24 and all(lcm(*map(int, p.split(" and "))) != 24 for p in bad)
    its.append(mcq("Which pair of numbers has an LCM of 24?", good, bad,
                   "Multiples of 8: 8, 16, 24. Multiples of 6: 6, 12, 18, 24. So the LCM of 6 and 8 is <b>24</b>. "
                   "4 × 6 = 24 and 2 × 12 = 24, but their LCM is 12. The LCM of 6 and 12 is also 12."))
    assert len(its) == 20, len(its)
    return {"title": "Common multiples and the lowest common multiple", "items": its}


# ============================================================ set 5: reasoning and word problems
def set_words(P):
    its = []

    # SATs-style reasoning
    ans = [v for v in range(41, 50) if is_prime(v) and sum(map(int, str(v))) == 7]
    assert ans == [43] and is_prime(41) and is_prime(47) and not is_prime(49)
    its.append(mcq("I am a prime number between 40 and 50. The digits of my number add up to 7. What number am I?",
                   43, [41, 47, 49],
                   "The primes between 40 and 50 are 41, 43 and 47. 4 + 3 = 7, so the number is <b>43</b>. "
                   "49 is not prime: 49 = 7 × 7."))

    ans = [v for v in range(1, 50) if int(v ** 0.5) ** 2 == v and v % 6 == 0]
    assert ans == [36]
    its.append(mcq("I am a square number less than 50. I am also a multiple of 6. What number am I?", 36, [16, 24, 18],
                   "The square numbers less than 50 are 1, 4, 9, 16, 25, 36 and 49. Only <b>36</b> is a multiple of 6 "
                   "(6 × 6 = 36). 16 is square but not a multiple of 6, and 24 and 18 are multiples of 6 but not square."))

    ans = [v ** 3 for v in range(1, 6) if 20 < v ** 3 < 100 and v ** 3 % 2]
    assert ans == [27]
    its.append(mcq("I am an odd cube number between 20 and 100. What number am I?", 27, [64, 25, 81],
                   "The cube numbers between 20 and 100 are 27 (3 × 3 × 3) and 64 (4 × 4 × 4). 64 is even, so the "
                   "number is <b>27</b>. 25 and 81 are square numbers, not cube numbers."))

    nm, he, his = P.next()
    ans = [v for v in factors(36) if v % 4 == 0 and 10 < v < 20]
    assert ans == [12] and 36 % 16 and 18 % 4
    its.append(mcq("%s thinks of a number between 10 and 20. It is a factor of 36 and a multiple of 4. "
                   "What is %s number?" % (nm, his), 12, [36, 18, 16],
                   "Factors of 36 between 10 and 20: 12 and 18. Only 12 is a multiple of 4, so the number is <b>12</b>. "
                   "18 is a factor of 36 but not a multiple of 4, and 16 is a multiple of 4 but not a factor of 36."))

    ps = [v for v in range(20, 31) if is_prime(v)]
    assert ps == [23, 29] and sum(ps) == 52 and 23 + 27 + 29 == 79 and 21 + 23 + 29 == 73
    its.append(mcq("What is the total of all the prime numbers between 20 and 30?", 52, [79, 73, 100],
                   "The primes between 20 and 30 are 23 and 29. 23 + 29 = <b>52</b>. 21 = 3 × 7, 25 = 5 × 5 and "
                   "27 = 3 × 9 are odd, but not prime. 100 is 21 + 23 + 27 + 29."))

    good, bad = (11, 13), [(9, 15), (1, 23), (2, 22)]
    assert sum(good) == 24 and all(is_prime(v) for v in good) and all(sum(p) == 24 and not all(is_prime(v) for v in p) for p in bad)
    its.append(mcq("Which pair of prime numbers has a total of 24?", "11 and 13", ["%d and %d" % p for p in bad],
                   "11 and 13 are both prime, and 11 + 13 = <b>24</b>. 9 and 15 are not prime, 1 is not prime, "
                   "and 22 = 2 × 11 is not prime."))

    # HCF word problems
    nm, he, his = P.next()
    its.append(mcq("%s has 24 pencils and 36 rubbers. %s wants to make identical packs with nothing left over. "
                   "What is the greatest number of packs %s can make?" % (nm, cap(he), he),
                   "12 packs", ["6 packs", "72 packs", "3 packs"],
                   "Find the HCF of 24 and 36. Common factors: %s. The HCF is <b>12</b>, so %s can make 12 packs, "
                   "each with 2 pencils and 3 rubbers. 6 packs would work too, but 12 is greater. 72 is the LCM."
                   % (lst(cfs(24, 36)), he)))
    assert gcd(24, 36) == 12 and lcm(24, 36) == 72

    nm, he, his = P.next()
    its.append(mcq("%s has two ribbons, 48 cm and 60 cm long. %s cuts both into pieces that are all the same length, "
                   "with nothing left over. What is the longest each piece can be?" % (nm, cap(he)),
                   "12 cm", ["6 cm", "240 cm", "4 cm"],
                   "The length must divide both 48 and 60. Common factors: %s. The HCF is <b>12 cm</b>: "
                   "4 pieces from the first ribbon and 5 from the second. 240 is the LCM, longer than both ribbons."
                   % lst(cfs(48, 60))))
    assert gcd(48, 60) == 12 and lcm(48, 60) == 240

    assert gcd(18, 27) == 9
    its.append(mcq("A PE teacher has 18 boys and 27 girls. Every team must have the same number of boys and the same "
                   "number of girls, with no one left out. What is the greatest number of teams?",
                   "9 teams", ["3 teams", "54 teams", "45 teams"],
                   "Find the HCF of 18 and 27. Common factors: %s. The HCF is <b>9</b>, so there are 9 teams, "
                   "each with 2 boys and 3 girls. 45 is 18 + 27, the number of children." % lst(cfs(18, 27))))

    nm, he, his = P.next()
    assert gcd(30, 42) == 6 and lcm(30, 42) == 210
    its.append(mcq("%s cuts a piece of card 30 cm by 42 cm into equal squares, as large as possible, with none left "
                   "over. What is the side length of each square?" % nm,
                   "6 cm", ["3 cm", "2 cm", "210 cm"],
                   "The side must divide both 30 and 42. Common factors: %s. The HCF is <b>6 cm</b>, which gives "
                   "5 rows of 7 squares. 210 is the LCM, and it is bigger than the card." % lst(cfs(30, 42))))

    nm, he, his = P.next()
    assert gcd(30, 45) == 15
    its.append(mcq("%s has 30 biscuits and 45 sweets. %s makes the greatest number of identical party bags with "
                   "nothing left over. How many sweets are in each bag?" % (nm, cap(he)),
                   "3 sweets", ["15 sweets", "2 sweets", "9 sweets"],
                   "The HCF of 30 and 45 is 15, so there are 15 bags. 45 ÷ 15 = <b>3 sweets</b> in each bag "
                   "(and 30 ÷ 15 = 2 biscuits). 15 is the number of bags, not sweets."))

    assert gcd(45, 60) == 15 and 45 // 5 + 60 // 5 == 21
    its.append(mcq("A florist has 45 roses and 60 tulips. She makes the greatest number of identical bunches with "
                   "nothing left over. How many flowers are in each bunch?",
                   "7 flowers", ["15 flowers", "12 flowers", "21 flowers"],
                   "The HCF of 45 and 60 is 15, so there are 15 bunches. Each has 45 ÷ 15 = 3 roses and "
                   "60 ÷ 15 = 4 tulips: 3 + 4 = <b>7 flowers</b>. 21 comes from making only 5 bunches."))

    # LCM word problems
    assert lcm(15, 20) == 60 and 15 * 20 == 300
    its.append(mcq("The number 12 bus leaves the bus station every 15 minutes. The number 7 bus leaves every 20 minutes. "
                   "Both buses leave at 8:00 am. When will they next leave at the same time?",
                   "9:00 am", ["8:35 am", "1:00 pm", "8:30 am"],
                   lcm_e(15, 20) + " So they leave together again 60 minutes later, at <b>9:00 am</b>. "
                   "8:35 am comes from 15 + 20 minutes, and 1:00 pm from 15 × 20 = 300 minutes."))

    its.append(mcq("A red light flashes every 4 seconds and a blue light flashes every 10 seconds. They flash together "
                   "now. In how many seconds will they next flash together?",
                   "20 seconds", ["40 seconds", "14 seconds", "2 seconds"],
                   lcm_e(4, 10) + " 4 × 10 = 40 is a later time they flash together, and 2 is the HCF."))

    nm, he, his = P.next()
    assert lcm(6, 8) == 24
    its.append(mcq("Sausages come in packs of 8 and bread rolls come in packs of 6. %s wants the same number of sausages "
                   "and rolls for a barbecue. What is the lowest number of each %s can buy?" % (nm, he),
                   "24 of each", ["48 of each", "14 of each", "2 of each"],
                   lcm_e(6, 8) + " That is 3 packs of sausages and 4 packs of rolls. 6 × 8 = 48 also works, "
                   "but it is not the lowest."))

    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    assert lcm(4, 6) == 12
    its.append(mcq("%s goes swimming every 4 days. %s goes swimming every 6 days. They both swim on 1 March. "
                   "On what date will they next both swim on the same day?" % (nm, nm2),
                   "13 March", ["25 March", "11 March", "3 March"],
                   lcm_e(4, 6) + " 12 days after 1 March is <b>13 March</b>. 25 March is 24 days later (4 × 6), "
                   "and 11 March is 10 days later (4 + 6)."))

    nm, he, his = P.next()
    assert lcm(9, 12) == 36
    its.append(mcq("Star stickers come in sheets of 9 and heart stickers come in sheets of 12. %s wants the same number "
                   "of star and heart stickers, as few as possible. How many sheets of star stickers should %s buy?"
                   % (nm, he),
                   "4 sheets", ["36 sheets", "3 sheets", "12 sheets"],
                   lcm_e(9, 12) + " %s needs 36 star stickers: 36 ÷ 9 = <b>4 sheets</b>. 3 sheets is the number of "
                   "heart sticker sheets (36 ÷ 12)." % cap(he)))

    assert lcm(6, 9) == 18
    its.append(mcq("Two lighthouses flash at the same moment. One flashes every 6 seconds and the other every 9 seconds. "
                   "How many seconds will it be until they next flash at the same moment?",
                   "18 seconds", ["54 seconds", "15 seconds", "3 seconds"],
                   lcm_e(6, 9) + " 54 is 6 × 9, 15 is 6 + 9, and 3 is the HCF."))

    # HCF or LCM?
    nm, he, his = P.next()
    assert gcd(36, 48) == 12
    its.append(mcq("%s has 36 pens and 48 stickers. %s wants to make the greatest number of identical gift bags with "
                   "nothing left over. What should %s work out?" % (nm, cap(he), he),
                   "The HCF of 36 and 48", ["The LCM of 36 and 48", "36 × 48", "48 − 36"],
                   "%s is sharing things into equal groups, and the number of bags must divide both 36 and 48. "
                   "That is the <b>HCF</b> (12 bags)." % cap(he)))
    assert lcm(8, 12) == 24
    its.append(mcq("A green light flashes every 8 seconds and a yellow light flashes every 12 seconds. They flash "
                   "together now. To find when they next flash together, what should you work out?",
                   "The LCM of 8 and 12", ["The HCF of 8 and 12", "8 × 12", "8 + 12"],
                   "The flashes repeat and must line up again, so you need a common <b>multiple</b>: the <b>LCM</b> "
                   "(24 seconds). 8 × 12 = 96 is a common multiple, but not the first."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems and SATs-style reasoning", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors and multiples</h2>"
        "<p>A <b>factor</b> divides a number exactly. A <b>multiple</b> is in its times table. "
        "3 × 8 = 24, so 3 and 8 are factors of 24, and 24 is a multiple of 3 and of 8.</p>"
        "<p>To find all the factors, find the <b>factor pairs</b>. Test 1, 2, 3, 4 … in order and stop when the pairs meet.</p>"
        "<figure class='sn-fig'>" + rainbow_svg(36) +
        "<figcaption>The factor pairs of 36: 1 × 36, 2 × 18, 3 × 12, 4 × 9 and 6 × 6. 36 has 9 factors.</figcaption></figure>"
        + "<h2>Prime numbers</h2>"
        "<p>A <b>prime number</b> has exactly two factors: 1 and itself. A number with more than two factors is "
        "<b>composite</b>. 1 is neither, because it has only one factor. 2 is the only even prime.</p>"
        + table(["Prime numbers to 50"], [["2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47"]])
        + "<p>Watch out for odd numbers that look prime: 9 = 3 × 3, 27 = 3 × 9, 51 = 3 × 17, 57 = 3 × 19 and 91 = 7 × 13.</p>"
        "<figure class='sn-fig'>" + tree_svg(60) +
        "<figcaption>A factor tree splits 60 until every branch ends in a prime: 60 = 2 × 2 × 3 × 5. "
        "These are the prime factors of 60.</figcaption></figure>"
        + "<h2>Square and cube numbers</h2>"
        "<p>A <b>square number</b> is a number times itself: 5<sup>2</sup> = 5 × 5 = 25. "
        "A <b>cube number</b> is a number times itself, three times: 2<sup>3</sup> = 2 × 2 × 2 = 8.</p>"
        "<figure class='sn-fig'>" + squares_svg() +
        "<figcaption>Square numbers make squares of dots: 1, 4, 9, 16, 25 … Cube numbers: 1, 8, 27, 64, 125 …</figcaption></figure>"
        + "<h2>Common factors and the highest common factor (HCF)</h2>"
        "<p>A <b>common factor</b> divides both numbers. List the factors of each number and circle the ones in both "
        "lists. The highest one is the <b>HCF</b>.</p>"
        "<figure class='sn-fig'>" + factor_rows_svg(24, 36) +
        "<figcaption>The common factors of 24 and 36 are 1, 2, 3, 4, 6 and 12. The HCF is 12.</figcaption></figure>"
        + ex("Example", "Find the HCF of 18 and 45.",
             "Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 45: 1, 3, 5, 9, 15, 45. Common factors: 1, 3, 9.", "9")
        + "<h2>Common multiples and the lowest common multiple (LCM)</h2>"
        "<p>A <b>common multiple</b> is in the times table of both numbers. The first one is the <b>LCM</b>. "
        "Count in the bigger number and stop at the first multiple of the smaller number.</p>"
        "<figure class='sn-fig'>" + multiples_svg(6, 8, 48) +
        "<figcaption>Multiples of 6 and of 8 meet at 24 and again at 48. The LCM is 24, not 6 × 8 = 48.</figcaption></figure>"
        + ex("Example", "Find the LCM of 9 and 12.",
             "Count in 12s: 12, 24, 36. 12 and 24 are not multiples of 9, but 36 = 9 × 4.", "36")
        + "<h2>HCF or LCM?</h2>"
        + table(["The problem asks…", "Use", "Example"], [
            ["The greatest number of identical packs, bags or teams", "HCF", "24 pencils and 36 rubbers make 12 packs"],
            ["The longest equal pieces or largest squares with nothing left over", "HCF", "48 cm and 60 cm ribbons: 12 cm pieces"],
            ["When two repeating things happen together again", "LCM", "Buses every 15 and 20 minutes: 60 minutes"],
            ["The lowest number to buy so two pack sizes match", "LCM", "Packs of 8 and 6: 24 of each"],
        ])
        + "<p>Check your answer: the HCF is never bigger than the smaller number, and the LCM is never smaller than "
        "the bigger number.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Saying 1 is prime", "A prime has exactly two factors. 1 has only one"],
            ["Saying 2 is not prime because it is even", "2 has two factors, 1 and 2. It is the only even prime"],
            ["Thinking 9, 27, 51 or 91 are prime", "Test small factors: 51 = 3 × 17, 91 = 7 × 13"],
            ["Mixing up factors and multiples: 4 is a multiple of 12", "4 is a factor of 12; 12 is a multiple of 4"],
            ["Missing a factor pair", "Test 1, 2, 3, 4 … in order until the pairs meet"],
            ["Multiplying for the LCM: LCM of 6 and 8 is 48", "48 is a common multiple, but 24 comes first"],
            ["Stopping at any common factor: HCF of 30 and 45 is 5", "Find the highest one: 15"],
            ["4<sup>3</sup> = 12", "4<sup>3</sup> = 4 × 4 × 4 = 64"],
        ])
    )


FAQ = [
    {"q": "What is a prime number?",
     "a": "A prime number has exactly two factors: 1 and itself. The prime numbers below 20 are 2, 3, 5, 7, 11, 13, 17 and 19."},
    {"q": "Is 1 a prime number?",
     "a": "No. 1 has only one factor, so it is not prime and not composite. The smallest prime number is 2, which is also the only even prime."},
    {"q": "What is the difference between a factor and a multiple?",
     "a": "A factor divides a number exactly; a multiple is in its times table. 4 is a factor of 12, and 12 is a multiple of 4."},
    {"q": "Are factors, multiples and prime numbers in the Year 6 SATs?",
     "a": "Yes. Questions on factors, multiples, prime, square and cube numbers often appear in the KS2 maths SATs, especially in the reasoning papers."},
]


def gen():
    rnd = random.Random(6605)
    P = People(rnd)
    sets = [set_factors(P), set_primes(P), set_hcf(P), set_lcm(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "factors-multiples-and-primes", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Factors, Multiples and Prime Numbers",
        "seo_title": "Year 6 Factors, Multiples and Primes Worksheets: Common Factors, HCF, LCM, Square and Cube Numbers",
        "short_title": "Factors, multiples and primes",
        "domain": "Addition, subtraction, multiplication and division",
        "standard_code": "Year 6: Addition, subtraction, multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Identify common factors, common multiples and prime numbers.",
        "meta_desc": "Free Year 6 maths worksheets on factors, multiples and prime numbers: factor pairs, prime factors, square and cube numbers, common factors (HCF), common multiples (LCM) and SATs-style word problems. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "A prime number has exactly two factors. The HCF divides both numbers; the LCM is the first number both divide into.",
        "key_sub": "1 is not prime, and 2 is the only even prime. For 6 and 8, the HCF is 2 and the LCM is 24, not 6 × 8 = 48. Use the HCF for equal groups and pieces, and the LCM for things that repeat and line up.",
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
