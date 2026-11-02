# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Factors, multiples and primes (National Curriculum in England)
  python3 tools/gen_uk_maths_y5_factors_primes.py
Factor pairs and all factors, multiples, common factors of two numbers, prime and composite numbers,
primes to 19, prime factors, square numbers (²) and cube numbers (³). No HCF / LCM (that is Year 6).
Every factor, multiple, prime, square and cube is checked in code.
Wrong answers come from real mistakes: 1 is prime, 2 is not prime, 51 / 57 / 91 are prime, all odd numbers
are prime, 7² = 14, 3³ = 9, a missing factor pair, confusing factors and multiples, 1 in a prime factor list.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
SUP = {2: "²", 3: "³"}


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


def is_prime(x):
    return len(factors(x)) == 2


def is_sq(v):
    return math.isqrt(v) ** 2 == v


def is_cube(v):
    return round(v ** (1 / 3)) ** 3 == v


def lst(xs):
    return ", ".join(n(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def pw(b, p):
    return "%d%s" % (b, SUP[p])


def why_not_prime(x):
    if x == 1:
        return "1 has only one factor, so it is not prime"
    s = pairs(x)[1]
    return "%d = %d × %d, so %d is not prime" % (x, s[0], s[1], x)


def pair_txt(x):
    return ", ".join("%d × %d" % p for p in pairs(x))


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
    assert prod(leaves(t)) == x and all(is_prime(p) for p in leaves(t))
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


def rainbow_svg(x, hide=None, step=40):
    """Factor rainbow: the factors of x in a row, each factor pair joined by an arc. 'hide' shows as ?."""
    fs = factors(x)
    ps = pairs(x)
    o = 20
    arcs = [p for p in ps if p[0] != p[1]]
    top = 16 + 14 * (len(ps) - 1) + 8
    W = (len(fs) - 1) * step + 2 * o
    xs = {f: o + i * step for i, f in enumerate(fs)}
    s = []
    for k, (a, b) in enumerate(ps):
        if a == b:
            continue
        ry = 16 + 14 * (len(ps) - 1 - k)
        s.append("<path d='M %d %d A %d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xs[a], top, (xs[b] - xs[a]) // 2, ry, xs[b], top, GREEN))
    assert arcs
    for f in fs:
        if f == hide:
            s.append("<rect x='%d' y='%d' width='28' height='26' rx='4' fill='#fff' stroke='%s' stroke-width='2'/>"
                     % (xs[f] - 14, top + 3, RED))
            s.append(text(xs[f], top + 22, "?", 18, col=RED))
        else:
            s.append(text(xs[f], top + 22, str(f), 18))
    lab = "factor rainbow for %d" % x + (" with one factor missing" if hide else "")
    return svg_wrap(W, top + 34, "".join(s), lab)


def array_svg(r, c, cell=18):
    """r rows of c dots."""
    o = 6
    W, H = c * cell + 2 * o, r * cell + 2 * o
    s = ["<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (o + j * cell + cell / 2, o + i * cell + cell / 2, GREEN)
         for i in range(r) for j in range(c)]
    return svg_wrap(W, H, "".join(s), "array of dots in %d rows" % r)


def track_svg(top, shaded, cell=34):
    """Number track 1..top in one row; shaded squares filled."""
    o = 4
    W, H = top * cell + 2 * o, cell + 2 * o
    s = []
    for v in range(1, top + 1):
        x = o + (v - 1) * cell
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, o, cell, cell, FILL if v in shaded else "#fff", GREEN))
        s.append(text(x + cell / 2, o + cell / 2 + 6, str(v), 15))
    return svg_wrap(W, H, "".join(s), "number track from 1 to %d" % top)


def dots_square_svg(k, cell=16):
    o = 6
    W = k * cell + 2 * o
    s = ["<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s'/>" % (o + j * cell + cell / 2, o + i * cell + cell / 2, GREEN)
         for i in range(k) for j in range(k)]
    return svg_wrap(W, W, "".join(s), "square of dots")


def squares_svg(k=4, cell=14, gap=26):
    """Lesson: square numbers 1, 4, 9, 16 as squares of dots."""
    o, lab = 8, 54  # each column is at least as wide as its label (about 50 units at 15px)
    colw = [max(i * cell, lab) for i in range(1, k + 1)]
    W = o * 2 + sum(colw) + gap * (k - 1)
    H = o + k * cell + 28
    s = []
    x = o
    for i in range(1, k + 1):
        cw = colw[i - 1]
        x0 = x + (cw - i * cell) / 2
        y0 = o + (k - i) * cell
        for r in range(i):
            for c in range(i):
                s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x0 + c * cell + cell / 2, y0 + r * cell + cell / 2, GREEN))
        s.append(text(x + cw / 2, o + k * cell + 22, "%d%s = %d" % (i, SUP[2], i * i), 15))
        x += cw + gap
    return svg_wrap(W, H, "".join(s), "square numbers 1, 4, 9 and 16 shown as squares of dots")


def cube_svg(k, u=None):
    """A k × k × k cube of small cubes, drawn in isometric view (three faces with grid lines)."""
    u = u or {2: 26, 3: 20, 4: 16}[k]
    cx, cy = math.cos(math.pi / 6) * u, math.sin(math.pi / 6) * u
    o = 4

    def P(a, b, c):
        # a along the right, b along the left, c up
        return (a * cx - b * cx, a * cy + b * cy - c * u)

    pts = [P(a, b, c) for a in (0, k) for b in (0, k) for c in (0, k)]
    minx, miny = min(p[0] for p in pts), min(p[1] for p in pts)
    maxx, maxy = max(p[0] for p in pts), max(p[1] for p in pts)
    dx, dy = o - minx, o - miny
    W, H = int(math.ceil(maxx - minx + 2 * o)), int(math.ceil(maxy - miny + 2 * o))

    def Q(a, b, c):
        x, y = P(a, b, c)
        return "%.1f,%.1f" % (x + dx, y + dy)

    s = []
    faces = [  # (corner function, colour)
        (lambda i, j: [Q(i, j, k), Q(i + 1, j, k), Q(i + 1, j + 1, k), Q(i, j + 1, k)], "#e3f1e7"),  # top
        (lambda i, j: [Q(i, k, j), Q(i + 1, k, j), Q(i + 1, k, j + 1), Q(i, k, j + 1)], FILL),  # left front
        (lambda i, j: [Q(k, i, j), Q(k, i + 1, j), Q(k, i + 1, j + 1), Q(k, i, j + 1)], "#9fcbb0"),  # right front
    ]
    for f, col in faces:
        for i in range(k):
            for j in range(k):
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.5'/>" % (" ".join(f(i, j)), col, GREEN))
    return svg_wrap(W, H, "".join(s), "cube made of small cubes, %d along each edge" % k)


# ============================================================ set 1: factor pairs and all factors
def set_factors(P):
    its = []
    for x, drop in [(12, (3, 4)), (20, (4, 5)), (24, (3, 8)), (30, (5, 6))]:
        fs = factors(x)
        right = lst(fs)
        missing = lst([d for d in fs if d not in drop])
        multi = lst([x * k for k in range(1, 5)])
        no_ends = lst(fs[1:-1])
        e = ("Find the factor pairs: %s. So the factors are <b>%s</b>. Do not forget 1 and %d, and do not miss %d × %d. "
             "%s are multiples of %d, not factors." % (pair_txt(x), right, x, drop[0], drop[1], multi, x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, right, [missing, no_ends, multi], e))

    for r, c, other in [(3, 6, (2, 9)), (4, 7, (2, 14))]:
        x = r * c
        assert x % other[0] == 0 and other[0] * other[1] == x
        its.append(mcq(fig(array_svg(r, c)) + "This array shows %d dots. Which factor pair of %d does it show?" % (x, x),
                       "%d × %d" % (r, c), ["%d + %d" % (r, c), "%d × %d" % other, "%d × %d" % (r, c + 1)],
                       "There are %d rows of %d dots: %d × %d = %d. So <b>%d × %d</b> is a factor pair of %d. "
                       "%d × %d is another pair, but it is not the one shown, and %d + %d = %d, not %d."
                       % (r, c, r, c, x, r, c, x, other[0], other[1], r, c, r + c, x)))

    assert 4 * 9 == 36 and 6 * 5 == 30 and 3 * 13 == 39 and 2 * 16 == 32
    its.append(mcq("Which of these is a factor pair of 36?", "4 × 9", ["6 × 5", "3 × 13", "2 × 16"],
                   "4 × 9 = <b>36</b>, so 4 and 9 are a factor pair. 6 × 5 = 30, 3 × 13 = 39 and 2 × 16 = 32. "
                   "The other pairs of 36 are 1 × 36, 2 × 18, 3 × 12 and 6 × 6."))

    for x, hide, partner, wrong in [(24, 8, 3, [21, 9, 7]), (30, 15, 2, [28, 60, 10])]:
        assert x % hide == 0 and hide * partner == x and hide in factors(x)
        assert all(x % w or w in factors(x) for w in wrong)
        e = "The arc joins ? to %d, so %d × ? = %d. %d ÷ %d = <b>%d</b>. " % (partner, partner, x, x, partner, hide)
        if x == 24:
            e += "21 is 24 − 3, not 24 ÷ 3. 9 and 7 are not factors of 24."
        else:
            e += "28 is 30 − 2, 60 is 30 × 2, and 10 is already in the rainbow (it pairs with 3)."
        its.append(mcq(fig(rainbow_svg(x, hide)) + "The factor rainbow shows all the factors of %d. "
                       "Which number is missing?" % x, hide, wrong, e))

    for x, bad, good in [(32, 6, [4, 8, 16]), (45, 6, [3, 9, 15]), (56, 12, [7, 8, 14])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d remainder %d, so <b>%d</b> is not a factor of %d. %s"
             % (x, bad, x // bad, x % bad, bad, x, " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for x, good, bad in [(42, 7, [84, 8, 12]), (54, 9, [108, 8, 12])]:
        assert x % good == 0 and all(x % b for b in bad) and bad[0] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a multiple of %d, not a factor, and %d and %d "
             "leave a remainder." % (good, x // good, x, good, x, bad[0], x, bad[1], bad[2]))
        its.append(mcq("Which number is a factor of %d?" % x, good, bad, e))

    assert len(factors(16)) == 5 and len(pairs(16)) == 3
    its.append(mcq("How many factors does 16 have?", 5, [6, 3, 4],
                   "The factor pairs are 1 × 16, 2 × 8 and 4 × 4. The factors are 1, 2, 4, 8, 16: <b>5</b> factors. "
                   "4 × 4 uses 4 only once, so do not count it twice (6). 3 is the number of pairs."))
    assert len(pairs(24)) == 4 and len(factors(24)) == 8
    its.append(mcq("How many factor pairs does 24 have?", 4, [8, 3, 5],
                   "1 × 24, 2 × 12, 3 × 8 and 4 × 6. That is <b>4</b> factor pairs. 8 is the number of factors, not pairs."))

    nm, he, his = P.next()
    shown = [(1, 48), (2, 24), (3, 16), (6, 8)]
    assert sorted(shown + [(4, 12)]) == pairs(48)
    its.append(mcq("%s lists the factor pairs of 48: %s. Which pair did %s miss?"
                   % (nm, ", ".join("%d × %d" % p for p in shown), he), "4 × 12", ["8 × 6", "5 × 10", "7 × 7"],
                   "Test 1, 2, 3, 4 … in order. 48 ÷ 4 = 12, so <b>4 × 12</b> is missing. 8 × 6 is the same pair as 6 × 8. "
                   "5 × 10 = 50 and 7 × 7 = 49, not 48."))

    assert len(factors(9)) == 3 and len(factors(6)) == 4 and len(factors(7)) == 2 and len(factors(12)) == 6
    its.append(mcq("Which number has exactly 3 factors?", 9, [6, 7, 12],
                   "The factors of 9 are 1, 3 and 9: <b>3</b> factors (3 × 3 counts 3 once). 6 has 4 factors (1, 2, 3, 6), "
                   "7 has 2 (1, 7), and 12 has 6."))

    nm, he, his = P.next()
    assert 27 % 7 == 6 and 7 * 3 != 27
    its.append(mcq("%s says 7 is a factor of 27 because 27 has a 7 in it. Is %s right?" % (nm, he),
                   "No. 27 ÷ 7 = 3 r 6", ["Yes. 27 ends in 7", "Yes. 7 × 3 = 27", "No. 27 is prime"],
                   "7 × 3 = 21 and 7 × 4 = 28, so 27 is not in the 7 times table. 27 ÷ 7 = 3 remainder 6, so 7 is "
                   "<b>not</b> a factor. The digits do not matter. 27 is not prime either: 27 = 3 × 9."))

    assert factors(35) == [1, 5, 7, 35]
    its.append(mcq("What is the largest factor of 35 that is less than 35?", 7, [5, 34, 17],
                   "The factors of 35 are 1, 5, 7 and 35. The largest one below 35 is <b>7</b>. "
                   "34 is 35 − 1, and 35 ÷ 2 is not a whole number, so 17 is not a factor."))
    assert len(its) == 20, len(its)
    return {"title": "Factor pairs and all the factors", "items": its}


# ============================================================ set 2: multiples and common factors
def set_multiples(P):
    its = []
    for v, right, wrong in [(6, 42, [16, 26, 63]), (8, 72, [28, 18, 84]), (9, 81, [19, 39, 89])]:
        assert right % v == 0 and all(w % v for w in wrong)
        e = "%d × %d = %d, so <b>%d</b> is a multiple of %d. %s" % (
            v, right // v, right, right, v,
            " ".join("%d ÷ %d = %d remainder %d." % (w, v, w // v, w % v) for w in wrong))
        e += " Having %s %d as a digit does not make a number a multiple of %d." % ("an" if v == 8 else "a", v, v)
        its.append(mcq("Which number is a multiple of %d?" % v, right, wrong, e))

    assert 47 % 7 and all(x % 7 == 0 for x in (49, 56, 35))
    its.append(mcq("Which number is <b>not</b> a multiple of 7?", 47, [49, 56, 35],
                   "7 × 6 = 42 and 7 × 7 = 49, so <b>47</b> is not in the 7 times table. "
                   "7 × 7 = 49, 7 × 8 = 56 and 7 × 5 = 35."))

    its.append(mcq("What is the 6th multiple of 8?", 48, [40, 56, 14],
                   "The 6th multiple of 8 is 8 × 6 = <b>48</b>. 40 is the 5th multiple, 56 is the 7th, and 14 is 8 + 6."))

    its.append(mcq("Which list shows the first five multiples of 4?", "4, 8, 12, 16, 20",
                   ["1, 2, 4", "8, 12, 16, 20, 24", "4, 14, 24, 34, 44"],
                   "The multiples of 4 are 4 × 1, 4 × 2, 4 × 3 …: <b>4, 8, 12, 16, 20</b>. The first multiple is 4 itself. "
                   "1, 2, 4 are the factors of 4."))

    nm, he, his = P.next()
    shaded = [3, 6, 9, 12, 18]
    miss = [v for v in range(3, 21, 3) if v not in shaded]
    assert miss == [15]
    its.append(mcq(fig(track_svg(20, shaded)) + "%s shades the multiples of 3 on this number track. "
                   "Which multiple of 3 has %s missed?" % (nm, he), 15, [13, 16, 10],
                   "Count in 3s: 3, 6, 9, 12, <b>15</b>, 18. 3 × 5 = 15 is not shaded. 13 has a 3 as a digit, "
                   "but 13 ÷ 3 = 4 remainder 1. 16 and 10 are not multiples of 3."))

    nm, he, his = P.next()
    its.append(mcq("%s says 30 is a factor of 5. Is %s right?" % (nm, he), "No. 30 is a multiple of 5",
                   ["Yes. 5 × 6 = 30", "Yes. 30 ÷ 5 = 6", "No. 5 is a multiple of 30"],
                   "5 × 6 = 30, so 30 is a <b>multiple</b> of 5, and 5 is a factor of 30. A factor divides the number; "
                   "a multiple is in its times table."))

    assert 56 % 7 == 0 and 56 % 6
    its.append(mcq("Which statement is true?", "7 is a factor of 56",
                   ["56 is a factor of 7", "7 is a multiple of 56", "6 is a factor of 56"],
                   "7 × 8 = 56, so <b>7 is a factor of 56</b> (and 56 is a multiple of 7). 56 ÷ 6 = 9 remainder 2, "
                   "so 6 is not a factor of 56."))

    # common factors
    for a, b in [(12, 16), (15, 25), (18, 24)]:
        c = cfs(a, b)
        e = ("Factors of %d: %s. Factors of %d: %s. The numbers in <b>both</b> lists are <b>%s</b>. "
             "Remember 1, and use only numbers that divide both." % (a, lst(factors(a)), b, lst(factors(b)), lst(c)))
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c),
                       [lst(c[:-1]), lst(factors(a)), lst(c[1:])], e))

    for a, b, right, wrong in [(20, 30, 5, [4, 3, 60]), (24, 32, 8, [3, 16, 96])]:
        assert a % right == 0 and b % right == 0
        assert a % wrong[0] == 0 and b % wrong[0] and b % wrong[1] == 0 and a % wrong[1]
        assert wrong[2] % a == 0 and wrong[2] % b == 0
        e = ("%d × %d = %d and %d × %d = %d, so <b>%d</b> is a common factor. %d is a factor of %d only, "
             "%d is a factor of %d only, and %d is a multiple of both, not a factor."
             % (right, a // right, a, right, b // right, b, right, wrong[0], a, wrong[1], b, wrong[2]))
        its.append(mcq("Which number is a common factor of %d and %d?" % (a, b), right, wrong, e))

    for a, b, bad, good in [(36, 48, 9, [2, 4, 12]), (40, 60, 8, [4, 5, 10])]:
        assert all(a % g == 0 and b % g == 0 for g in good) and a % bad == 0 and b % bad
        e = ("%d is a factor of %d, but %d ÷ %d = %d remainder %d, so <b>%d</b> is not a common factor. "
             "%d, %d and %d divide both numbers." % ((bad, a, b, bad, b // bad, b % bad, bad) + tuple(good)))
        its.append(mcq("Which number is <b>not</b> a common factor of %d and %d?" % (a, b), bad, good, e))

    good, bad = (9, 14), [(9, 12), (8, 14), (10, 15)]
    assert cfs(*good) == [1] and all(len(cfs(*p)) > 1 for p in bad)
    its.append(mcq("Which pair of numbers has only 1 as a common factor?", "9 and 14", ["%d and %d" % p for p in bad],
                   "Factors of 9: 1, 3, 9. Factors of 14: 1, 2, 7, 14. The only common factor is 1, so the answer is "
                   "<b>9 and 14</b>. 9 and 12 share 3, 8 and 14 share 2, and 10 and 15 share 5."))

    assert cfs(12, 18) == [1, 2, 3, 6]
    its.append(mcq("How many common factors do 12 and 18 have?", 4, [3, 6, 2],
                   "Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 18: 1, 2, 3, 6, 9, 18. Common factors: 1, 2, 3, 6. "
                   "That is <b>4</b>. Do not forget 1 (that gives 3). 6 is the largest common factor, not how many."))

    nm, he, his = P.next()
    assert 15 % 2 and 10 % 2 == 0
    its.append(mcq("%s says 2 is a common factor of 10 and 15. Is %s right?" % (nm, he),
                   "No. 2 is not a factor of 15",
                   ["Yes. 2 is a factor of 10", "Yes. Both are in the 5 times table", "No. 2 is a prime number"],
                   "A common factor must divide <b>both</b> numbers. 2 divides 10, but 15 is odd, so 15 ÷ 2 = 7 remainder 1. "
                   "2 is <b>not</b> a common factor. The common factors of 10 and 15 are 1 and 5."))

    assert all(v % 6 == 0 for v in (12, 18, 30)) and 18 % 4 and 30 % 9 and 18 % 12
    its.append(mcq("Which number is a common factor of 12, 18 <b>and</b> 30?", 6, [4, 9, 12],
                   "6 × 2 = 12, 6 × 3 = 18 and 6 × 5 = 30, so <b>6</b> divides all three. 4 does not divide 18, "
                   "9 does not divide 12 or 30, and 12 does not divide 18 or 30."))
    assert len(its) == 20, len(its)
    return {"title": "Multiples and common factors", "items": its}


# ============================================================ set 3: prime and composite numbers, prime factors
def set_primes(P):
    its = []
    for right, wrong in [(13, [15, 21, 1]), (29, [27, 39, 49]), (17, [51, 9, 57])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("%d has exactly two factors, 1 and %d, so <b>%d</b> is prime. " % (right, right, right)
             + ". ".join(cap(why_not_prime(w)) for w in wrong) + ".")
        its.append(mcq("Which of these is a prime number?", right, wrong, e))

    for right, wrong in [(1, [2, 3, 5]), (57, [2, 59, 43]), (91, [71, 97, 61])]:
        assert not is_prime(right) and all(is_prime(w) for w in wrong)
        e = cap(why_not_prime(right)).replace(str(right) + " is not", "<b>%d</b> is not" % right, 1) + ". "
        e += "%s and %d are prime: each has exactly two factors." % (", ".join(str(w) for w in wrong[:-1]), wrong[-1])
        if 2 in wrong:
            e += " 2 is prime, even though it is even."
        its.append(mcq("Which number is <b>not</b> a prime number?", right, wrong, e))

    ps = [v for v in range(1, 20) if is_prime(v)]
    assert ps == [2, 3, 5, 7, 11, 13, 17, 19]
    its.append(mcq("Which list shows all the prime numbers up to 19?", lst(ps),
                   ["1, 3, 5, 7, 11, 13, 17, 19", "3, 5, 7, 9, 11, 13, 15, 17, 19", "2, 3, 5, 7, 11, 13, 17"],
                   "The primes up to 19 are <b>2, 3, 5, 7, 11, 13, 17, 19</b>. Learn them by heart. 1 is not prime, "
                   "2 is prime, 9 = 3 × 3 and 15 = 3 × 5 are not prime, and do not leave out 19."))

    assert 51 == 3 * 17 and not is_prime(51) and 5 * 11 == 55
    its.append(mcq("Is 51 a prime number?", "No. 51 = 3 × 17",
                   ["Yes. It is odd", "Yes. It has only two factors", "No. 51 = 5 × 11"],
                   "Test small primes. 5 + 1 = 6, which is in the 3 times table, so 51 divides by 3: 51 = 3 × 17. "
                   "So 51 is <b>not</b> prime. Being odd does not make a number prime, and 5 × 11 = 55."))

    assert not is_prime(39) and is_prime(2) and is_prime(37)
    its.append(mcq("Which number is <b>composite</b>?", 39, [2, 37, 1],
                   "A composite number has more than two factors. 39 = 3 × 13, so <b>39</b> is composite. 2 and 37 are prime. "
                   "1 is neither prime nor composite: it has only one factor."))

    its.append(mcq("How many factors does a prime number have?", "Exactly 2", ["Exactly 1", "More than 2", "Exactly 3"],
                   "A prime number has <b>exactly two</b> factors: 1 and itself. 7 has factors 1 and 7. "
                   "A number with more than two factors is composite."))

    ps = [v for v in range(21, 30) if is_prime(v)]
    assert ps == [23, 29]
    its.append(mcq("How many prime numbers are there between 20 and 30?", 2, [5, 3, 4],
                   "The odd numbers are 21, 23, 25, 27, 29. 21 = 3 × 7, 25 = 5 × 5 and 27 = 3 × 9, so only 23 and 29 are "
                   "prime: <b>2</b> primes. Counting every odd number gives 5, and 3 or 4 means a number like 21, 25 or 27 was counted."))

    nm, he, his = P.next()
    assert not is_prime(15) and is_prime(13) and is_prime(11)
    its.append(mcq("%s says every odd number is prime. Which number shows %s is wrong?" % (nm, he), 15, [13, 11, 2],
                   "15 is odd, but 15 = 3 × 5, so it is not prime. <b>15</b> shows the rule is wrong. 13 and 11 are odd "
                   "and prime, so they fit the rule, and 2 is not odd."))

    nm, he, his = P.next()
    its.append(mcq("%s says 2 is not a prime number because it is even. Is %s right?" % (nm, he),
                   "No. 2 has exactly two factors",
                   ["Yes. All primes are odd", "Yes. 2 has only one factor", "No. 2 is a square number"],
                   "The factors of 2 are 1 and 2, so <b>2 is prime</b>. It is the only even prime: every other even "
                   "number divides by 2."))
    nm, he, his = P.next()
    its.append(mcq("%s says 1 is a prime number. Is %s right?" % (nm, he), "No. 1 has only one factor",
                   ["Yes. 1 divides by itself", "Yes. 1 is an odd number", "No. 1 is a composite number"],
                   "A prime number has <b>exactly two</b> factors: 1 and itself. 1 has only one factor, so it is not prime. "
                   "It is not composite either."))

    for x in [12, 18, 40]:
        ps = sorted(leaves(tree(x)))
        assert all(is_prime(p) for p in ps) and prod(ps) == x
        first = times(split(x))
        once = times(sorted(set(ps)))
        with1 = times([1] + ps)
        notp = [v for v in split(x) if not is_prime(v)]
        e = ("Keep splitting until every branch ends in a prime: %d = <b>%s</b>. %s is not finished, because %s "
             "not prime. 1 is not prime, so it is not written."
             % (x, times(ps), first, " and ".join(map(str, notp)) + (" are" if len(notp) > 1 else " is")))
        if once != first:
            e += " %s = %d, not %d." % (once, prod(sorted(set(ps))), x)
        its.append(mcq(fig(tree_svg(x)) + "Which shows %d as a product of prime factors?" % x, times(ps),
                       [first, once, with1], e))

    assert sorted(set(leaves(tree(42)))) == [2, 3, 7]
    its.append(mcq("What are the prime factors of 42?", "2, 3 and 7", ["1, 2, 3 and 7", "6 and 7", "2 and 21"],
                   "42 = 2 × 3 × 7, and 2, 3 and 7 are all prime. So the prime factors are <b>2, 3 and 7</b>. "
                   "1 is not prime, 6 = 2 × 3 and 21 = 3 × 7."))

    assert 35 % 7 == 0 and is_prime(7) and 35 % 3 and not is_prime(35)
    its.append(mcq("Which number is a prime factor of 35?", 7, [35, 1, 3],
                   "35 = 5 × 7, and 7 is prime, so <b>7</b> is a prime factor. 35 is a factor but not prime, 1 is not prime, "
                   "and 3 is prime but not a factor of 35."))

    assert 2 * 2 * 3 * 5 == 60 and 2 + 2 + 3 + 5 == 12
    its.append(mcq("What is 2 × 2 × 3 × 5?", 60, [12, 30, 120],
                   "2 × 2 = 4, 4 × 3 = 12, 12 × 5 = <b>60</b>. So the prime factors of 60 are 2, 2, 3 and 5. "
                   "12 comes from adding, 30 uses only one 2, and 120 uses three 2s."))
    assert len(its) == 20, len(its)
    return {"title": "Prime numbers, composite numbers and prime factors", "items": its}


# ============================================================ set 4: square and cube numbers
def set_squares(P):
    its = []
    k = 6
    assert k * k == 36 and 4 * (k - 1) == 20
    its.append(mcq(fig(dots_square_svg(k)) + "The dots make a square. How many dots are there?", 36, [12, 20, 25],
                   "There are 6 rows of 6 dots: 6 × 6 = 6%s = <b>36</b>. 36 is a square number. 12 is 6 + 6, 20 counts only "
                   "the dots round the edge, and 25 is 5 × 5." % SUP[2]))

    for b, wrong in [(7, [14, 9, 343]), (9, [18, 11, 729])]:
        e = ("%s means %d × %d = <b>%d</b>. It does not mean %d × 2 = %d or %d + 2 = %d. %s is %s."
             % (pw(b, 2), b, b, b * b, b, 2 * b, b, b + 2, n(b ** 3), pw(b, 3)))
        its.append(mcq("What is %s?" % pw(b, 2), b * b, [n(w) for w in wrong], e))

    its.append(mcq("What is %s?" % pw(3, 3), 27, [9, 6, 81],
                   "3%s means 3 × 3 × 3 = 9 × 3 = <b>27</b>. 9 is only 3 × 3 (3%s), 6 is 3 + 3, and 81 is 9 × 9."
                   % (SUP[3], SUP[2])))
    its.append(mcq("What is %s?" % pw(5, 3), 125, [15, 25, 8],
                   "5%s means 5 × 5 × 5 = 25 × 5 = <b>125</b>. 15 is 5 × 3, 25 is 5%s, and 8 is 5 + 3." % (SUP[3], SUP[2])))

    its.append(mcq(fig(cube_svg(2)) + "This cube is made of small cubes. How many small cubes are there?", 8, [4, 6, 7],
                   "It has 2 layers of 2 × 2 = 4 cubes: 2 × 2 × 2 = 2%s = <b>8</b>. 4 is only the top layer, and 7 counts "
                   "only the cubes you can see: one is hidden at the back." % SUP[3]))
    assert 27 - 8 == 19
    its.append(mcq(fig(cube_svg(3)) + "This cube is made of small cubes. How many small cubes are there?", 27, [9, 19, 18],
                   "It has 3 layers of 3 × 3 = 9 cubes: 3 × 3 × 3 = 3%s = <b>27</b>. 9 is one layer, 18 is two layers, and "
                   "19 counts only the cubes you can see." % SUP[3]))

    for right, wrong in [(81, [18, 27, 90]), (16, [8, 12, 32])]:
        assert is_sq(right) and not any(is_sq(w) for w in wrong)
        r = math.isqrt(right)
        e = "%d × %d = <b>%d</b>, so %d is a square number. " % (r, r, right, right)
        if right == 81:
            e += "18 is 9 × 2, 27 is a cube number (3 × 3 × 3), and 90 is between 9 × 9 and 10 × 10."
        else:
            e += "8 is a cube number (2 × 2 × 2), 12 is 4 × 3, and 32 is between 5 × 5 and 6 × 6."
        its.append(mcq("Which of these is a square number?", right, wrong, e))

    assert is_cube(64) and not any(is_cube(w) for w in (16, 12, 36))
    its.append(mcq("Which of these is a cube number?", 64, [16, 12, 36],
                   "4 × 4 × 4 = 16 × 4 = <b>64</b>, so 64 is a cube number. 16 is 4%s, a square number, 12 is 4 × 3, "
                   "and 36 is 6%s." % (SUP[2], SUP[2])))

    its.append(mcq("Which list shows the first five square numbers?", "1, 4, 9, 16, 25",
                   ["2, 4, 6, 8, 10", "4, 9, 16, 25, 36", "1, 8, 27, 64, 125"],
                   "1 × 1 = 1, 2 × 2 = 4, 3 × 3 = 9, 4 × 4 = 16, 5 × 5 = 25: <b>1, 4, 9, 16, 25</b>. "
                   "The first square number is 1. 2, 4, 6, 8, 10 are multiples of 2, and 1, 8, 27, 64, 125 are cube numbers."))
    its.append(mcq("Which list shows the first four cube numbers?", "1, 8, 27, 64",
                   ["3, 6, 9, 12", "1, 4, 9, 16", "1, 6, 9, 12"],
                   "1 × 1 × 1 = 1, 2 × 2 × 2 = 8, 3 × 3 × 3 = 27, 4 × 4 × 4 = 64: <b>1, 8, 27, 64</b>. "
                   "3, 6, 9, 12 are multiples of 3, and 1, 4, 9, 16 are square numbers."))

    assert 4 ** 2 + 3 ** 2 == 25
    its.append(mcq("Work out %s + %s" % (pw(4, 2), pw(3, 2)), 25, [14, 49, 12],
                   "4%s = 16 and 3%s = 9. 16 + 9 = <b>25</b>. 14 comes from 4 × 2 + 3 × 2, and 49 from adding first: "
                   "7 × 7. 12 is 4 × 3." % (SUP[2], SUP[2])))
    assert 2 ** 3 + 3 ** 2 == 17
    its.append(mcq("Work out %s + %s" % (pw(2, 3), pw(3, 2)), 17, [12, 15, 14],
                   "2%s = 2 × 2 × 2 = 8 and 3%s = 3 × 3 = 9. 8 + 9 = <b>17</b>. 12 is 2 × 3 + 3 × 2, 15 uses 2%s = 6, "
                   "and 14 uses 3%s = 6." % (SUP[3], SUP[2], SUP[3], SUP[2])))
    assert 6 ** 2 - 5 ** 2 == 11
    its.append(mcq("Work out %s − %s" % (pw(6, 2), pw(5, 2)), 11, [1, 2, 61],
                   "6%s = 36 and 5%s = 25. 36 − 25 = <b>11</b>. 1 is 6 − 5, 2 is 12 − 10, and 61 is 36 + 25."
                   % (SUP[2], SUP[2])))

    its.append(mcq("Which is greater, %s or %s?" % (pw(3, 3), pw(5, 2)), "3%s, because 27 &gt; 25" % SUP[3],
                   ["5%s, because 25 &gt; 9" % SUP[2], "5%s, because 10 &gt; 9" % SUP[2], "They are equal"],
                   "3%s = 3 × 3 × 3 = 27 and 5%s = 5 × 5 = 25. 27 is greater, so <b>3%s</b> is greater. "
                   "Using 3%s = 9 or 5%s = 10 gives the wrong answer." % (SUP[3], SUP[2], SUP[3], SUP[3], SUP[2])))

    sq = [v for v in range(51, 70) if is_sq(v)]
    assert sq == [64]
    its.append(mcq("Which number is a square number between 50 and 70?", 64, [56, 49, 63],
                   "7 × 7 = 49 is less than 50 and 9 × 9 = 81 is more than 70. 8 × 8 = <b>64</b>. "
                   "56 is 7 × 8 and 63 is 7 × 9, not square numbers."))

    its.append(mcq("What is the 12th square number?", 144, [24, 122, 121],
                   "The 12th square number is 12%s = 12 × 12 = <b>144</b>. 24 is 12 × 2, 122 is 12 and 2 written "
                   "side by side, and 121 is 11%s, the 11th square number." % (SUP[2], SUP[2])))

    nm, he, his = P.next()
    its.append(mcq("%s says 8%s = 16. Is %s right?" % (nm, SUP[2], he), "No. 8%s = 8 × 8 = 64" % SUP[2],
                   ["Yes. 8 × 2 = 16", "No. 8%s = 8 + 2 = 10" % SUP[2], "No. 8%s = 512" % SUP[2]],
                   "The small 2 means multiply 8 by itself: 8 × 8 = <b>64</b>. It does not mean 8 × 2 or 8 + 2. "
                   "512 is 8%s = 8 × 8 × 8." % SUP[3]))

    assert 4 ** 3 == 64 and 8 ** 2 == 64
    its.append(mcq("Find the missing number: ?%s = 64" % SUP[3], 4, [8, 21, 16],
                   "4 × 4 × 4 = 16 × 4 = 64, so the missing number is <b>4</b>. 8 × 8 = 64 is 8%s, not a cube. "
                   "21 comes from 64 ÷ 3, but cubed means multiply three times, not × 3. 16 is 4%s." % (SUP[2], SUP[2])))
    assert len(its) == 20, len(its)
    return {"title": "Square numbers and cube numbers", "items": its}


# ============================================================ set 5: word problems and reasoning
def set_words(P):
    its = []
    ans = [v for v in range(31, 40) if is_sq(v)]
    assert ans == [36]
    its.append(mcq("I am a square number between 30 and 40. What number am I?", 36, [34, 32, 49],
                   "5 × 5 = 25 and 6 × 6 = 36 and 7 × 7 = 49. The only square number between 30 and 40 is <b>36</b>. "
                   "49 is square but more than 40. 32 and 34 are not square numbers."))

    ans = [v for v in range(31, 40) if is_prime(v) and sum(map(int, str(v))) == 4]
    assert ans == [31] and is_prime(37) and not is_prime(39)
    its.append(mcq("I am a prime number between 30 and 40. My digits add up to 4. What number am I?", 31, [13, 37, 39],
                   "The primes between 30 and 40 are 31 and 37. 3 + 1 = 4, so the number is <b>31</b>. 13 has digits "
                   "that add to 4, but it is not between 30 and 40. 39 = 3 × 13 is not prime."))

    ans = [v ** 3 for v in range(1, 6) if 50 < v ** 3 < 100]
    assert ans == [64]
    its.append(mcq("I am a cube number between 50 and 100. What number am I?", 64, [81, 54, 125],
                   "3%s = 27, 4%s = 64 and 5%s = 125. So the cube number between 50 and 100 is <b>64</b>. "
                   "81 is a square number (9 × 9), and 125 is more than 100." % (SUP[3], SUP[3], SUP[3])))

    assert 36 % 8 and all(36 % g == 0 for g in (4, 6, 9))
    its.append(mcq("A teacher puts 36 chairs in equal rows, with none left over. Which could <b>not</b> be the number "
                   "of chairs in each row?", "8 chairs", ["4 chairs", "6 chairs", "9 chairs"],
                   "The number in each row must be a factor of 36. 36 ÷ 8 = 4 remainder 4, so <b>8 chairs</b> does not work. "
                   "4 × 9 = 36 and 6 × 6 = 36."))

    opts = [(5, 6), (4, 8), (3, 9), (7, 4)]
    assert [r * c == 30 for r, c in opts] == [True, False, False, False]
    its.append(mcq("The hall has 30 chairs for a school assembly. Which layout uses all 30 chairs in equal rows?",
                   "5 rows of 6", ["%d rows of %d" % p for p in opts[1:]],
                   "5 × 6 = <b>30</b>, so 5 rows of 6 works. 4 × 8 = 32, 3 × 9 = 27 and 7 × 4 = 28."))

    nm, he, his = P.next()
    assert is_prime(17)
    its.append(mcq("%s has 17 counters. Can %s put them all in a rectangle with more than one row and the same number "
                   "in each row?" % (nm, he), "No, because 17 is prime",
                   ["Yes, in 2 rows of 8", "Yes, in 3 rows of 6", "No, because 17 is odd"],
                   "17 is prime: its only factors are 1 and 17, so the only rectangle is 1 row of 17. 2 × 8 = 16 and "
                   "3 × 6 = 18. Being odd is not the reason: 15 is odd and makes 3 rows of 5."))

    assert 48 % 6 == 0 and all(v % 6 for v in (26, 16, 40))
    its.append(mcq("Packets of crisps come in multipacks of 6. Which number of packets can you buy exactly?", 48,
                   [26, 16, 40],
                   "You can only buy a multiple of 6. 6 × 8 = <b>48</b>. 26 and 16 have a 6 as a digit but are not "
                   "multiples of 6, and 40 ÷ 6 = 6 remainder 4."))

    nm, he, his = P.next()
    assert 8 * 3 < 30 <= 8 * 4
    its.append(mcq("Biscuits come in packets of 8. %s needs at least 30 biscuits for %s class. What is the fewest "
                   "packets %s can buy?" % (nm, his, he), "4 packets", ["3 packets", "5 packets", "8 packets"],
                   "Multiples of 8: 8, 16, 24, 32. 3 packets give 24, which is not enough. <b>4 packets</b> give 32. "
                   "5 packets give 40, which is more than needed."))

    nm, he, his = P.next()
    assert 12 % 6 == 0 and 18 % 6 == 0 and 12 % 4 == 0 and 18 % 4 and 18 % 9 == 0 and 12 % 9
    its.append(mcq("%s has 12 red beads and 18 blue beads. %s makes bracelets that are all the same, using every bead. "
                   "How many bracelets could %s make?" % (nm, cap(he), he), "6 bracelets",
                   ["4 bracelets", "9 bracelets", "36 bracelets"],
                   "The number of bracelets must be a common factor of 12 and 18. 6 works: each bracelet has 2 red and "
                   "3 blue beads, so <b>6 bracelets</b>. 4 divides 12 but not 18, 9 divides 18 but not 12, and 36 is "
                   "a multiple, not a factor."))

    assert 20 % 10 == 0 and 30 % 10 == 0 and 20 % 3 and 20 % 6 and 30 % 4
    its.append(mcq("A baker has 20 cupcakes and 30 biscuits. She packs them into boxes that are all the same, with none "
                   "left over. How many boxes could she use?", "10 boxes", ["4 boxes", "6 boxes", "60 boxes"],
                   "The number of boxes must divide 20 and 30. 20 ÷ 10 = 2 and 30 ÷ 10 = 3, so <b>10 boxes</b> work. "
                   "4 divides 20 but not 30, 6 divides 30 but not 20, and 60 is a multiple of both."))

    ans = [v for v in range(1, 40) if v % 2 == 0 and v % 3 == 0 and v % 5 == 0]
    assert ans == [30] and 10 % 3 and 15 % 2 and 35 % 2
    its.append(mcq("A class has fewer than 40 pupils. They can line up in 2s, 3s or 5s with no one left over. "
                   "How many pupils are in the class?", 30, [10, 15, 35],
                   "The number must be a multiple of 2, 3 and 5. 2 × 3 × 5 = <b>30</b>. 10 is not a multiple of 3, "
                   "and 15 and 35 are odd, so they are not multiples of 2."))

    nm, he, his = P.next()
    ans = [a for a in range(6, 15) if is_prime(a) and (a + 1) % 6 == 0]
    assert ans == [11] and not is_prime(12) and (13 + 1) % 6
    its.append(mcq("%s is older than 5 and younger than 15. %s age is a prime number. Next year %s age will be a "
                   "multiple of 6. How old is %s?" % (nm, cap(his), his, he), 11, [12, 13, 5],
                   "The primes from 6 to 14 are 7, 11 and 13. Next year they become 8, 12 and 14. Only 12 is a multiple of 6, "
                   "so %s is <b>11</b>. 12 is next year’s age, 13 + 1 = 14 is not a multiple of 6, and 5 is too young."
                   % he))

    assert 7 * 7 == 49
    its.append(mcq("A square patio is made of 49 square tiles. How many tiles are along each side?", "7 tiles",
                   ["14 tiles", "12 tiles", "9 tiles"],
                   "A square has the same number of tiles along each side. 7 × 7 = 49, so there are <b>7 tiles</b>. "
                   "14 comes from 7 × 2, 12 from 49 ÷ 4, and 9 × 9 = 81."))

    assert 4 ** 3 == 64
    its.append(mcq("A big cube is built from small cubes, with 4 small cubes along each edge. How many small cubes "
                   "are used?", 64, [16, 12, 48],
                   "4%s = 4 × 4 × 4 = 16 × 4 = <b>64</b>. 16 is one layer (4 × 4), 12 is 4 × 3, and 48 is only 3 layers."
                   % SUP[3]))

    nm, he, his = P.next()
    assert 4 ** 3 <= 100 < 5 ** 3
    its.append(mcq("%s has 100 small cubes. %s builds the biggest solid cube %s can. How many small cubes does %s use?"
                   % (nm, cap(he), he, he), 64, [100, 125, 81],
                   "Cube numbers: 27, 64, 125. 125 is more than 100, so the biggest cube uses 4 × 4 × 4 = <b>64</b> cubes. "
                   "100 is a square number, not a cube, and 81 is 9 × 9."))

    nm, he, his = P.next()
    ans = [v for v in range(11, 30) if v % 4 == 0 and 40 % v == 0]
    assert ans == [20] and 40 % 12 and 10 % 4 and 40 % 24
    its.append(mcq("%s thinks of a number between 10 and 30. It is a multiple of 4 and a factor of 40. What is %s number?"
                   % (nm, his), 20, [12, 10, 24],
                   "Factors of 40: 1, 2, 4, 5, 8, 10, 20, 40. Between 10 and 30 there is only 20, and 20 = 4 × 5, so the number "
                   "is <b>20</b>. 12 and 24 are multiples of 4 but not factors of 40, and 10 is not a multiple of 4."))

    nm, he, his = P.next()
    its.append(mcq("%s says all prime numbers are odd. Which number shows %s is wrong?" % (nm, he), 2, [9, 1, 15],
                   "<b>2</b> is prime (its factors are 1 and 2), and it is even. 9 and 15 are odd numbers that are not prime, "
                   "and 1 is not prime, so none of them shows the rule is wrong."))

    good = (7, 13)
    bad = [(3, 17), (1, 19), (9, 11)]
    assert all(is_prime(v) for v in good) and sum(good) == 20 and good[1] - good[0] == 6
    assert all(sum(p) == 20 and (p[1] - p[0] != 6 or not all(map(is_prime, p))) for p in bad)
    its.append(mcq("Two prime numbers add up to 20. Their difference is 6. What are they?", "7 and 13",
                   ["%d and %d" % p for p in bad],
                   "7 + 13 = 20 and 13 − 7 = 6, and both are prime: <b>7 and 13</b>. 3 and 17 are prime but differ by 14. "
                   "1 is not prime, and 9 = 3 × 3 is not prime."))

    sizes = [d for d in factors(28) if 1 < d < 10]
    assert sizes == [2, 4, 7]
    its.append(mcq("28 pupils split into equal groups. Each group has more than 1 and fewer than 10 pupils. How many "
                   "different group sizes are possible?", 3, [6, 4, 2],
                   "The group size must be a factor of 28: 1, 2, 4, 7, 14, 28. Between 1 and 10 that leaves 2, 4 and 7: "
                   "<b>3</b> sizes. 6 counts every factor, and 4 wrongly includes 14."))

    assert is_sq(64) and is_cube(64) and is_sq(16) and not is_cube(16) and is_cube(27) and not is_sq(27) and is_sq(81)
    assert [v for v in range(10, 100) if is_sq(v) and is_cube(v)] == [64]
    its.append(mcq("I am a two-digit number. I am a square number and also a cube number. What number am I?", 64,
                   [16, 27, 81],
                   "64 = 8 × 8 and 64 = 4 × 4 × 4, so <b>64</b> is both. 16 and 81 are only square numbers, and "
                   "27 = 3 × 3 × 3 is only a cube number."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems and reasoning", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors and factor pairs</h2>"
        "<p>A <b>factor</b> divides a number exactly, with no remainder. Factors come in <b>pairs</b> that multiply "
        "to make the number. 3 × 4 = 12, so 3 and 4 are a factor pair of 12.</p>"
        "<figure class='sn-fig'>" + array_svg(3, 4) +
        "<figcaption>12 dots in 3 rows of 4: 3 × 4 = 12.</figcaption></figure>"
        "<p>To find <b>all</b> the factors, test 1, 2, 3, 4 … in order. Stop when the pairs meet.</p>"
        "<figure class='sn-fig'>" + rainbow_svg(24) +
        "<figcaption>A factor rainbow for 24: 1 × 24, 2 × 12, 3 × 8 and 4 × 6. 24 has 8 factors.</figcaption></figure>"
        + ex("Example", "Find all the factors of 30.",
             "1 × 30, 2 × 15, 3 × 10, 5 × 6. 4 does not divide 30. The next number, 6, is already in a pair, so stop.",
             "1, 2, 3, 5, 6, 10, 15, 30")
        + "<h2>Multiples and common factors</h2>"
        "<p>A <b>multiple</b> is in a number’s times table: 6, 12, 18, 24 … are multiples of 6. "
        "4 is a factor of 12, and 12 is a multiple of 4.</p>"
        "<p>A <b>common factor</b> divides two numbers. List the factors of each and find the ones in both lists.</p>"
        + ex("Example", "Find the common factors of 12 and 18.",
             "Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 18: 1, 2, 3, 6, 9, 18.", "1, 2, 3 and 6")
        + "<h2>Prime and composite numbers</h2>"
        "<p>A <b>prime number</b> has exactly two factors: 1 and itself. A <b>composite</b> number has more than two "
        "factors. 1 is neither. 2 is the only even prime.</p>"
        + table(["Prime numbers up to 19 (learn these)"], [["2, 3, 5, 7, 11, 13, 17, 19"]])
        + "<p>To check a number up to 100, try dividing by 2, 3, 5 and 7. If none of them works, it is prime.</p>"
        + ex("Example", "Is 51 prime?", "5 + 1 = 6, so 51 divides by 3: 51 = 3 × 17.", "No, 51 is composite")
        + "<p>A <b>prime factor</b> is a factor that is prime. A factor tree splits a number until every branch ends in a prime.</p>"
        "<figure class='sn-fig'>" + tree_svg(36) +
        "<figcaption>36 = 2 × 2 × 3 × 3. The prime factors of 36 are 2 and 3.</figcaption></figure>"
        "<h2>Square numbers and cube numbers</h2>"
        "<p>A <b>square number</b> is a number multiplied by itself. We write 5² (5 squared) for 5 × 5 = 25.</p>"
        "<figure class='sn-fig'>" + squares_svg() +
        "<figcaption>Square numbers make squares of dots: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144.</figcaption></figure>"
        "<p>A <b>cube number</b> is a number multiplied by itself three times. We write 3³ (3 cubed) for 3 × 3 × 3 = 27.</p>"
        "<figure class='sn-fig'>" + cube_svg(3) +
        "<figcaption>3 layers of 3 × 3 = 9 cubes: 3³ = 27. Cube numbers: 1, 8, 27, 64, 125, 1,000 (10³).</figcaption></figure>"
        + ex("Example", "Work out 4³.", "4 × 4 = 16, then 16 × 4 = 64.", "64")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Saying 1 is prime", "A prime has exactly two factors. 1 has only one"],
            ["Saying 2 is not prime because it is even", "2 has two factors, 1 and 2. It is the only even prime"],
            ["Thinking every odd number is prime: 51, 57, 91", "51 = 3 × 17, 57 = 3 × 19, 91 = 7 × 13"],
            ["Missing a factor pair", "Test 1, 2, 3, 4 … in order until the pairs meet"],
            ["Mixing up factors and multiples: 4 is a multiple of 12", "4 is a factor of 12; 12 is a multiple of 4"],
            ["7² = 14", "7² = 7 × 7 = 49"],
            ["3³ = 9", "3³ = 3 × 3 × 3 = 27"],
        ])
    )


FAQ = [
    {"q": "What are factors and multiples in Year 5?",
     "a": "A factor divides a number exactly, and a multiple is in its times table. In Year 5 children find all the factor pairs of a number, multiples, and the common factors of two numbers."},
    {"q": "What prime numbers should Year 5 know?",
     "a": "Year 5 pupils should recall the prime numbers up to 19 (2, 3, 5, 7, 11, 13, 17 and 19) and be able to check whether any number up to 100 is prime."},
    {"q": "Is 1 a prime number?",
     "a": "No. A prime number has exactly two factors, and 1 has only one. 1 is neither prime nor composite, and the smallest prime number is 2."},
    {"q": "What do ² and ³ mean in maths?",
     "a": "² means squared, a number multiplied by itself: 7² = 7 × 7 = 49. ³ means cubed, a number multiplied by itself three times: 3³ = 3 × 3 × 3 = 27."},
]


def gen():
    rnd = random.Random(5505)
    P = People(rnd)
    sets = [set_factors(P), set_multiples(P), set_primes(P), set_squares(P), set_words(P)]
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "factors-multiples-and-primes", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Factors, Multiples and Prime Numbers",
        "seo_title": "Year 5 Factors, Multiples and Primes Worksheets: Factor Pairs, Prime, Square and Cube Numbers",
        "short_title": "Factors, multiples and primes",
        "domain": "Multiplication and division",
        "standard_code": "Year 5: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Identify multiples and factors, including finding all factor pairs of a number, and common factors of two numbers; know and use the vocabulary of prime numbers, prime factors and composite (non-prime) numbers; establish whether a number up to 100 is prime and recall prime numbers up to 19; recognise and use square numbers and cube numbers, and the notation for squared (²) and cubed (³).",
        "meta_desc": "Free Year 5 maths worksheets on factors, multiples and prime numbers: factor pairs, common factors, prime and composite numbers, prime factors, square numbers and cube numbers. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "A factor divides a number exactly; a multiple is in its times table. A prime number has exactly two factors.",
        "key_sub": "1 is not prime, and 2 is the only even prime. Learn the primes to 19: 2, 3, 5, 7, 11, 13, 17, 19. 7² = 7 × 7 = 49 and 3³ = 3 × 3 × 3 = 27.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "factor tree|factor rainbow|number track")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
