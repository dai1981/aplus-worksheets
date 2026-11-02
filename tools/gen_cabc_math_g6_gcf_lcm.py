# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: GCF and LCM (BC Mathematics Curriculum, Grade 6: Number —
factors and multiples – greatest common factor and least common multiple)
  python3 tools/gen_cabc_math_g6_gcf_lcm.py
Factors and multiples (factor pairs, arrays), prime and composite numbers (1 is neither, factor trees),
the greatest common factor (lists, factor trees, three numbers), the least common multiple (skip counting,
number lines, three numbers), and word problems in BC settings (packages, schedules, equal rows and bags).
Every factor, multiple, prime, GCF and LCM is checked in code.
Wrong answers come from real student mistakes: swapping GCF and LCM, a common factor that is not the
greatest, multiplying the numbers for the LCM, adding the numbers, using only two of three numbers,
mixing up factors and multiples, “odd means prime”, 1 is prime, 2 is not prime, unfinished factor trees,
and answering with the wrong quantity (packs instead of items, bags instead of items per bag).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, os, random, re
from math import gcd, prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ math
def n(x):
    """BC style: 4 digits with no separator, 5 or more digits grouped with a no-break space."""
    x = int(x)
    return str(x) if abs(x) < 10000 else "{:,}".format(x).replace(",", NBSP)


def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def cfs(*xs):
    return [d for d in factors(min(xs)) if all(x % d == 0 for x in xs)]


def G(*xs):
    g = 0
    for x in xs:
        g = gcd(g, x)
    return g


def L(*xs):
    l = 1
    for x in xs:
        l = l * x // gcd(l, x)
    return l


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


def shared_primes(*xs):
    """Primes in every factorization, each used as often as it appears in all of them."""
    out = []
    for p in sorted(set(primes_of(xs[0]))):
        out += [p] * min(primes_of(x).count(p) for x in xs)
    return out


def why_not_prime(x):
    if x == 1:
        return "1 has only one factor, so it is not prime"
    d = primes_of(x)[0]
    return "%d = %d × %d, so %d is not prime" % (x, d, x // d, x)


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


def tree_parts(x, ox, step=44, dy=48, o=20):
    """Elements of one factor tree drawn from x offset ox. Returns (elements, width, height)."""
    t = tree(x)
    assert prod(leaves(t)) == x and all(is_prime(v) for v in leaves(t))
    W = (len(leaves(t)) - 1) * step + 2 * o
    H = (depth(t) - 1) * dy + 2 * o
    pos, s, cnt = {}, [], [0]

    def place(node, lvl):
        if node[1] is None:
            px = ox + o + cnt[0] * step
            cnt[0] += 1
        else:
            px = sum(place(c, lvl + 1) for c in node[1]) / 2
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
        s.append(text(px, py + 6, str(node[0]), 16))

    draw(t)
    return s, W, H


def tree_svg(x):
    s, W, H = tree_parts(x, 0)
    return svg_wrap(W, H, "".join(s), "factor tree for %d" % x)


def tree_pair_svg(a, b, gap=26):
    """Two factor trees side by side in one picture."""
    sa, wa, ha = tree_parts(a, 0)
    sb, wb, hb = tree_parts(b, wa + gap)
    W, H = wa + gap + wb, max(ha, hb)
    sep = "<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='1' stroke-dasharray='3 4'/>" % (
        wa + gap / 2, wa + gap / 2, H - 6, GREY)
    return svg_wrap(W, H, "".join(sa) + sep + "".join(sb), "factor trees for %d and %d" % (a, b))


def factor_rows_svg(a, b, show_gcf=True):
    """The factors of a and b in two rows with the common ones circled. With show_gcf, the GCF is red."""
    fa, fb = factors(a), factors(b)
    g = gcd(a, b)
    step, lx, o = 36, 50, 8
    cols = sorted(set(fa) | set(fb))
    W = lx + len(cols) * step + o
    H = 2 * 40 + 2 * o
    s = []
    for r, (v, fs) in enumerate([(a, fa), (b, fb)]):
        y = o + 26 + r * 40
        s.append(text(lx - 8, y, "%d:" % v, 16, anchor="end"))
        for d in fs:
            x = lx + cols.index(d) * step + step / 2
            hot = show_gcf and d == g
            if d in fa and d in fb:
                s.append("<circle cx='%.1f' cy='%d' r='15' fill='%s' stroke='%s' stroke-width='2'/>"
                         % (x, y - 6, "#f6d5d0" if hot else FILL, RED if hot else GREEN))
            s.append(text(x, y, str(d), 15, col=RED if hot else INK))
    return svg_wrap(W, H, "".join(s), "factors of %d and %d with the common factors circled" % (a, b))


def multiples_svg(a, b, top, show=False, sc=8):
    """Multiples of a and b placed by size on two rows. With show=True, common multiples are red and joined."""
    ox = 48
    W = ox + top * sc + 18
    H = 112
    ya, yb = 34, 80
    s = []
    for v, y in [(a, ya), (b, yb)]:
        s.append(text(ox - 12, y + 6, "%d:" % v, 16, anchor="end"))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (ox, y, ox + top * sc + 6, y, GREY))
    if show:
        for m in range(L(a, b), top + 1, L(a, b)):
            x = ox + m * sc
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                     % (x, ya + 7, x, yb - 7, RED))
    for v, y, up in [(a, ya, True), (b, yb, False)]:
        for m in mults(v, top):
            x = ox + m * sc
            common = show and m % a == 0 and m % b == 0
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (x, y, RED if common else GREEN))
            s.append(text(x, y - 10 if up else y + 23, str(m), 14, col=RED if common else INK))
    return svg_wrap(W, H, "".join(s), "multiples of %d and %d up to %d" % (a, b, top))


def array_svg(rows, cols, sp=26, r=9, o=8):
    """An array of counters: rows × cols."""
    W = 2 * o + cols * sp
    H = 2 * o + rows * sp
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (o + j * sp + sp // 2, o + i * sp + sp // 2, r, FILL, GREEN))
    return svg_wrap(W, H, "".join(s), "array of %d counters" % (rows * cols))


# ============================================================ set 1: factors and multiples
def set_factors(P):
    its = []
    for x in [24, 36, 48]:
        fs = factors(x)
        prs = [(d, x // d) for d in fs if d * d <= x]
        mid = prs[-1]
        no_mid = [d for d in fs if d not in mid]
        no_ends = fs[1:-1]
        ms = mults(x, 4 * x)[:4]
        e = ("Find the factor pairs: %s. So the factors of %d are <b>%s</b>. Include 1 and %d, and don’t "
             "forget the pair in the middle." % (", ".join("%d × %d" % p for p in prs), x, lst(fs), x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, lst(fs),
                       [lst(no_mid), lst(no_ends), lst(ms)], e))

    assert len(factors(36)) == 9 and len(factors(60)) == 12
    its.append(mcq("How many factors does 36 have?", 9, [10, 5, 7],
                   "The factors of 36 are %s. That is <b>9 factors</b>. 6 × 6 = 36, so 6 is counted only once. "
                   "Counting 6 twice gives 10, counting pairs gives 5, and leaving out 1 and 36 gives 7." % lst(factors(36))))
    its.append(mcq("How many factors does 60 have?", 12, [6, 10, 4],
                   "The factors of 60 are %s. That is <b>12 factors</b>. Counting pairs gives 6, and leaving out "
                   "1 and 60 gives 10. 4 is the number of primes in 2 × 2 × 3 × 5." % lst(factors(60))))

    for x, right, wrong in [(72, 18, [144, 16, 14]), (96, 12, [192, 14, 18])]:
        assert x % right == 0 and all(x % w for w in wrong) and wrong[0] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a <b>multiple</b> of %d, not a factor. "
             "%d ÷ %d and %d ÷ %d have remainders."
             % (right, x // right, x, right, x, wrong[0], x, x, wrong[1], x, wrong[2]))
        its.append(mcq("Which number is a factor of %d?" % x, right, wrong, e))

    for x, bad, good in [(84, 8, [12, 14, 21]), (90, 4, [9, 15, 18])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d R %d, so <b>%d</b> is not a factor. %s"
             % (x, bad, x // bad, x % bad, bad, " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for d, wrong in [(6, [[0, 6, 12, 18, 24], [1, 2, 3, 6], [6, 16, 26, 36, 46]]),
                     (8, [[0, 8, 16, 24, 32], [1, 2, 4, 8], [8, 18, 28, 38, 48]])]:
        right = [d * k for k in range(1, 6)]
        assert all(w != right for w in wrong)
        e = ("Multiply %d by 1, 2, 3, 4 and 5: <b>%s</b>. The first multiple of a number is the number itself, "
             "not 0. Count by %d, not by 10. %s are the factors of %d, not multiples."
             % (d, lst(right), d, lst(wrong[1]), d))
        its.append(mcq("Which list shows the first five multiples of %d?" % d, lst(right), [lst(w) for w in wrong], e))

    for d, right, wrong in [(9, 108, [3, 89, 119]), (8, 96, [4, 58, 108]), (6, 84, [3, 76, 94])]:
        assert right % d == 0 and all(w % d for w in wrong) and d % wrong[0] == 0
        assert str(wrong[1])[-1] == str(d)
        e = ("%d × %d = %d, so <b>%d</b> is a multiple of %d. %d is a <b>factor</b> of %d, not a multiple. "
             "%d ÷ %d and %d ÷ %d have remainders. Ending in %d does not make a number a multiple of %d."
             % (d, right // d, right, right, d, wrong[0], d, wrong[1], d, wrong[2], d, d, d))
        its.append(mcq("Which number is a multiple of %d?" % d, right, wrong, e))

    assert 54 % 7 and all(x % 7 == 0 for x in (42, 63, 77))
    its.append(mcq("Which number is <b>not</b> a multiple of 7?", 54, [42, 63, 77],
                   "54 ÷ 7 = 7 R 5, so <b>54</b> is not a multiple of 7. 42 = 7 × 6, 63 = 7 × 9 and 77 = 7 × 11."))

    its.append(mcq("Which statement is true?", "36 is a multiple of 12",
                   ["36 is a factor of 12", "12 is a multiple of 36", "4 is a multiple of 12"],
                   "12 × 3 = 36, so <b>36 is a multiple of 12</b>, and 12 is a factor of 36. "
                   "A factor is never bigger than the number. A multiple is never smaller."))

    prs = [(d, 48 // d) for d in factors(48) if d * d <= 48]
    assert (3, 16) in prs and (4, 12) in prs
    shown = ", ".join("%d × %s" % (p[0], "?" if p[0] == 3 else str(p[1])) for p in prs)
    its.append(mcq("These are the factor pairs of 48: %s. What is the missing number?" % shown, 16, [15, 17, 12],
                   "3 × 16 = 48, so the missing number is <b>16</b>. 3 × 15 = 45 and 3 × 17 = 51. "
                   "12 is already in the pair 4 × 12."))

    assert 3 * 8 == 24
    its.append(mcq(fig(array_svg(3, 8)) + "This array has 24 counters. Which factor pair of 24 does it show?",
                   "3 × 8", ["4 × 6", "2 × 12", "3 × 7"],
                   "Count the rows and the counters in each row: 3 rows of 8. So the array shows <b>3 × 8</b> = 24. "
                   "4 × 6 and 2 × 12 are also factor pairs of 24, but they are not this array."))

    assert all(36 % x == 0 for x in (12,)) and 8 % 4 == 0 and 36 % 8 and 9 % 4 and 6 % 4
    its.append(mcq("Which number is a factor of 36 <b>and</b> a multiple of 4?", 12, [8, 9, 6],
                   "36 = 12 × 3 and 12 = 4 × 3, so <b>12</b> is both. 8 is a multiple of 4, but not a factor of 36. "
                   "9 and 6 are factors of 36, but not multiples of 4."))

    nm, he, his = P.next()
    its.append(mcq("%s says 3 is a multiple of 12, because 12 ÷ 3 = 4. Is %s right?" % (nm, he),
                   "No. 3 is a factor of 12", ["Yes. 12 ÷ 3 = 4", "Yes. 3 × 4 = 12", "No. 3 is a multiple of 4"],
                   "12 ÷ 3 = 4 with no remainder, so 3 is a <b>factor</b> of 12, and 12 is a multiple of 3. "
                   "The multiples of 12 are 12, 24, 36, … They are never smaller than 12."))
    assert len(its) == 20, len(its)
    return {"title": "Factors and multiples", "items": its}


# ============================================================ set 2: prime and composite numbers
def set_primes(P):
    its = []
    for right, wrong in [(29, [27, 21, 1]), (43, [49, 45, 39]), (59, [57, 51, 55]), (71, [91, 81, 77])]:
        assert is_prime(right) and not any(is_prime(w) for w in wrong)
        e = ("%d has exactly two factors, 1 and %d, so <b>%d</b> is prime. " % (right, right, right)
             + ". ".join(cap(why_not_prime(w)) for w in wrong) + ".")
        its.append(mcq("Which of these is a prime number?", right, wrong, e))

    for right, wrong in [(1, [2, 5, 7]), (39, [2, 41, 43]), (91, [89, 83, 97])]:
        assert not is_prime(right) and all(is_prime(w) for w in wrong)
        e = "<b>" + cap(why_not_prime(right)) + "</b>. "
        e += "%s and %d are prime: each has exactly two factors." % (", ".join(str(w) for w in wrong[:-1]), wrong[-1])
        if 2 in wrong:
            e += " 2 is prime, even though it is even."
        its.append(mcq("Which number is <b>not</b> a prime number?", right, wrong, e))

    comp = lambda v: len(factors(v)) > 2
    for right, wrong in [(25, [1, 2, 23]), (69, [1, 67, 71])]:
        assert comp(right) and not any(comp(w) for w in wrong)
        d = primes_of(right)[0]
        e = ("%d = %d × %d, so %d has more than two factors: <b>%d</b> is composite. " % (right, d, right // d, right, right)
             + "1 is not composite (it has only one factor). "
             + " and ".join(str(w) for w in wrong if w != 1) + " are prime.")
        its.append(mcq("Which of these is a composite number?", right, wrong, e))

    its.append(mcq("Which statement about the number 1 is true?", "It is neither prime nor composite",
                   ["It is a prime number", "It is a composite number", "It is both prime and composite"],
                   "A prime has exactly two factors and a composite number has more than two. 1 has only <b>one</b> "
                   "factor, so it is <b>neither</b>."))

    its.append(mcq("How many factors does every prime number have?", "Exactly 2", ["Exactly 1", "Exactly 3", "More than 2"],
                   "A prime number has <b>exactly two</b> factors: 1 and itself. More than two factors means composite."))

    nm, he, his = P.next()
    its.append(mcq("%s says 2 is not a prime number because it is even. Is %s right?" % (nm, he),
                   "No. 2 has exactly two factors",
                   ["Yes. All primes are odd", "Yes. 2 has only one factor", "No. 2 is composite"],
                   "The factors of 2 are 1 and 2, so <b>2 is prime</b>. It is the only even prime: every other even "
                   "number can be divided by 2, so it is composite."))

    nm, he, his = P.next()
    assert factors(21) == [1, 3, 7, 21]
    its.append(mcq("%s says 21 is a prime number because it is odd. Is %s right?" % (nm, he),
                   "No. 21 = 3 × 7",
                   ["Yes. Odd numbers are prime", "Yes. 21 is not even", "No. 21 has only one factor"],
                   "The factors of 21 are 1, 3, 7 and 21. That is more than two factors, so 21 is <b>composite</b>. "
                   "Many odd numbers are composite: 9, 15, 21, 25, 27, …"))

    ps = [p for p in range(21, 30) if is_prime(p)]
    assert ps == [23, 29]
    its.append(mcq("How many prime numbers are there between 20 and 30?", 2, [5, 3, 4],
                   "Test the odd numbers: 21 = 3 × 7, 23 is prime, 25 = 5 × 5, 27 = 3 × 9 and 29 is prime. "
                   "So there are <b>2</b> primes, 23 and 29. 5 counts every odd number."))
    ps = [p for p in range(41, 50) if is_prime(p)]
    assert ps == [41, 43, 47]
    its.append(mcq("How many prime numbers are there between 40 and 50?", 3, [5, 4, 2],
                   "Test the odd numbers: 41, 43 and 47 are prime, 45 = 5 × 9 and 49 = 7 × 7. "
                   "So there are <b>3</b> primes. 5 counts every odd number, and 4 counts 49 as prime."))

    assert primes_of(51) == [3, 17] and 7 * 7 == 49
    its.append(mcq("Is 51 prime or composite?", "Composite. 51 = 3 × 17",
                   ["Prime. It is odd", "Prime. It is not in a times table", "Composite. 51 = 7 × 7"],
                   "5 + 1 = 6, so 51 is divisible by 3: 51 = 3 × 17. It is <b>composite</b>. "
                   "7 × 7 = 49, not 51."))

    lists = {"2, 17, 23, 37": True, "1, 17, 23, 37": False, "2, 17, 21, 37": False, "2, 19, 23, 39": False}
    assert all(all(is_prime(int(v)) for v in k.split(", ")) == ok for k, ok in lists.items())
    its.append(mcq("Which list has <b>only</b> prime numbers?", "2, 17, 23, 37",
                   ["1, 17, 23, 37", "2, 17, 21, 37", "2, 19, 23, 39"],
                   "2, 17, 23 and 37 each have exactly two factors, so <b>2, 17, 23, 37</b> are all prime. "
                   "1 is not prime, 21 = 3 × 7 and 39 = 3 × 13."))

    for x in [36, 60, 84]:
        t = tree(x)
        ps = primes_of(x)
        assert sorted(leaves(t)) == ps
        first = [c[0] for c in t[1]]
        uniq = sorted(set(ps))
        cands = [times(first), times(uniq), "1 × " + times(ps), times(ps[1:])]
        e = ("Keep splitting until every branch ends in a prime. The circled numbers are the primes: %d = <b>%s</b>. "
             "%s is not finished, because %s not prime. Write a repeated prime every time it appears, "
             "and do not write 1 (1 is not prime)."
             % (x, times(ps), times(first),
                " and ".join(str(v) for v in sorted(set(first)) if not is_prime(v)) +
                (" are" if len([v for v in set(first) if not is_prime(v)]) > 1 else " is")))
        its.append(mcq(fig(tree_svg(x)) + "Use the factor tree. What is the prime factorization of %d?" % x,
                       times(ps), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Prime and composite numbers", "items": its}


# ============================================================ set 3: GCF
def gcf_e(a, b):
    return ("Factors of %d: %s. Factors of %d: %s. Common factors: %s. The greatest is <b>%d</b>."
            % (a, lst(factors(a)), b, lst(factors(b)), lst(cfs(a, b)), gcd(a, b)))


def one_only(a, b):
    """Biggest factor of the smaller number (less than it) that is NOT a factor of the other number."""
    s, l = min(a, b), max(a, b)
    xs = [d for d in factors(s) if l % d and d < s]
    return xs[-1] if xs else None


def set_gcf(P):
    its = []
    for a, b in [(12, 18), (24, 36)]:
        c = cfs(a, b)
        small = factors(min(a, b))
        e = ("Factors of %d: %s. Factors of %d: %s. The numbers in <b>both</b> lists are <b>%s</b>. "
             "Keep 1 and the greatest one." % (a, lst(factors(a)), b, lst(factors(b)), lst(c)))
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c),
                       [lst(c[:-1]), lst(small), lst(c[1:])], e))

    for a, b in [(18, 30), (24, 40)]:
        g = gcd(a, b)
        c = cfs(a, b)
        e = ("The circled numbers are in both lists: %s. The greatest one is <b>%d</b>. %d is a common factor too, "
             "but not the greatest. %d is the least common multiple, not a factor." % (lst(c), g, c[-2], L(a, b)))
        its.append(mcq(fig(factor_rows_svg(a, b, show_gcf=False)) + "The common factors of %d and %d are circled. "
                       "What is the greatest common factor (GCF)?" % (a, b), g, [c[-2], L(a, b), 1], e))

    for a, b in [(12, 16), (18, 24), (20, 30), (16, 40), (27, 36), (14, 21), (9, 16), (15, 45)]:
        g = gcd(a, b)
        c = cfs(a, b)
        cands = []
        if len(c) > 1 and c[-2] > 1:
            cands.append(c[-2])
        if one_only(a, b):
            cands.append(one_only(a, b))
        cands.append(L(a, b))
        if min(a, b) != g:
            cands.append(min(a, b))
        cands += [a * b, a + b]
        e = gcf_e(a, b)
        if g == 1:
            e += " %d and %d share no factor except 1, so their GCF is 1." % (a, b)
        elif g == min(a, b):
            e += " %d divides %d (%d × %d = %d), so the smaller number is the GCF. %d is a common factor, but smaller." % (
                a, b, a, b // a, b, c[-2])
        elif len(c) > 1 and c[-2] > 1:
            e += " %d is a common factor too, but not the greatest. %d is the least common multiple." % (c[-2], L(a, b))
        else:
            e += " %d is the least common multiple." % L(a, b)
        its.append(mcq("What is the greatest common factor (GCF) of %d and %d?" % (a, b), g, cands, e))

    for a, b in [(36, 60), (48, 72)]:
        pa, pb = primes_of(a), primes_of(b)
        sh = shared_primes(a, b)
        g = prod(sh)
        assert g == gcd(a, b)
        once = prod(sorted(set(sh)))
        c = cfs(a, b)
        e = ("The trees give %d = %s and %d = %s. Both lists share %s. Multiply the shared primes: %s = <b>%d</b>."
             % (a, times(pa), b, times(pb), times(sh), times(sh), g))
        if once != g:
            e += " Using each shared prime only once gives %d, which is too small." % once
        e += " %d is the least common multiple." % L(a, b)
        its.append(mcq(fig(tree_pair_svg(a, b)) + "Use the factor trees. What is the GCF of %d and %d?" % (a, b),
                       g, [once, L(a, b), c[-2], c[-3]], e))

    for xs in [(16, 24, 36), (18, 27, 30)]:
        g = G(*xs)
        g12 = gcd(xs[0], xs[1])
        c = cfs(*xs)
        assert g12 != g
        smaller = [d for d in c if d < g]
        e = ("Common factors of %d, %d and %d: %s. The GCF is <b>%d</b>. The GCF of %d and %d alone is %d, "
             "but %d is not a factor of %d. Check all three numbers." % (xs + (lst(c), g, xs[0], xs[1], g12, g12, xs[2])))
        its.append(mcq("What is the GCF of %d, %d and %d?" % xs, g, [g12, smaller[-1], L(*xs)], e))

    nm, he, his = P.next()
    assert gcd(24, 36) == 12 and L(24, 36) == 72 and 36 % 24
    its.append(mcq("%s says the GCF of 24 and 36 is 6, because 6 is a factor of both. Is %s right?" % (nm, he),
                   "No. The GCF is 12", ["Yes. 6 divides both", "No. The GCF is 72", "No. The GCF is 24"],
                   "6 is a common factor, but not the greatest. 12 × 2 = 24 and 12 × 3 = 36, so the GCF is <b>12</b>. "
                   "72 is the least common multiple, and 24 is not a factor of 36."))
    nm, he, his = P.next()
    assert gcd(8, 12) == 4 and L(8, 12) == 24 and 8 * 12 == 96
    its.append(mcq("%s says the GCF of 8 and 12 is 24. Is %s right?" % (nm, he),
                   "No. 24 is the LCM. The GCF is 4", ["Yes. 8 and 12 divide 24", "No. The GCF is 96", "No. The GCF is 2"],
                   "24 is a common <b>multiple</b>. A factor can’t be bigger than the numbers. "
                   "Factors of 8: 1, 2, 4, 8. Factors of 12: 1, 2, 3, 4, 6, 12. The greatest one in both lists is <b>4</b>. "
                   "2 is a common factor, but not the greatest. 96 is 8 × 12."))
    nm, he, his = P.next()
    assert gcd(9, 20) == 1 and L(9, 20) == 180
    its.append(mcq("%s says 9 and 20 have no common factor, so they have no GCF. Is %s right?" % (nm, he),
                   "No. Their GCF is 1", ["Yes. They have no GCF", "No. Their GCF is 3", "No. Their GCF is 180"],
                   "1 is a factor of every whole number, so 1 is always a common factor. 9 = 3 × 3 and "
                   "20 = 2 × 2 × 5 share no prime, so the GCF is <b>1</b>. 180 is their least common multiple."))

    assert gcd(18, 24) == 6 and [gcd(12, 36), gcd(2, 3), gcd(20, 30)] == [12, 1, 10] and L(2, 3) == 6
    its.append(mcq("Which pair of numbers has a GCF of 6?", "18 and 24", ["12 and 36", "2 and 3", "20 and 30"],
                   "18 = 6 × 3 and 24 = 6 × 4, and 3 and 4 share no factor, so the GCF of 18 and 24 is <b>6</b>. "
                   "The GCF of 12 and 36 is 12, of 2 and 3 is 1 (6 is their LCM), and of 20 and 30 is 10."))
    assert len(its) == 20, len(its)
    return {"title": "Greatest common factor (GCF)", "items": its}


# ============================================================ set 4: LCM
def lcm_e(a, b):
    l = L(a, b)
    lo, hi = sorted((a, b))
    return ("Count by %d: %s. The first one that is also a multiple of %d is <b>%d</b>."
            % (hi, lst(mults(hi, l)), lo, l))


def set_lcm(P):
    its = []
    for a, b, top, wrong, note in [
            (3, 5, 30, [[15], [3, 5], [3, 6, 9, 12, 15]], " Not only 3 × 5 = 15: 30 is in both rows too."),
            (4, 6, 36, [[24], [12], [4, 8, 12]], " Not only 4 × 6 = 24: 12 and 36 are in both rows too.")]:
        com = [m for m in range(1, top + 1) if m % a == 0 and m % b == 0]
        assert all(w != com for w in wrong) and all(m <= top for w in wrong for m in w)
        e = ("Look for numbers in <b>both</b> rows. Multiples of %d: %s. Multiples of %d: %s. "
             "The common multiples shown are <b>%s</b>.%s" % (a, lst(mults(a, top)), b, lst(mults(b, top)), lst(com), note))
        its.append(mcq(fig(multiples_svg(a, b, top, sc=10 if a == 3 else 8)) + "Which numbers in the picture are common multiples of %d and %d?"
                       % (a, b), lst(com), [lst(w) for w in wrong], e))

    for a, b, top in [(6, 8, 48), (8, 12, 48)]:
        l = L(a, b)
        g = gcd(a, b)
        assert a * b != l
        e = ("The first number in <b>both</b> rows is %d, so the least common multiple is <b>%d</b>. "
             "%d × %d = %d is a common multiple, but not the least. %d is the GCF, and %d is %d + %d."
             % (l, l, a, b, a * b, g, a + b, a, b))
        its.append(mcq(fig(multiples_svg(a, b, top)) + "Use the picture. What is the least common multiple (LCM) of %d and %d?"
                       % (a, b), l, [a * b, g, a + b], e))

    for a, b in [(4, 6), (6, 9)]:
        l = L(a, b)
        right = [l, 2 * l, 3 * l]
        byprod = [a * b, 2 * a * b, 3 * a * b]
        mixed = [a, b, l]
        big = mults(b, 3 * b)
        e = ("The LCM of %d and %d is %d. The common multiples are the multiples of the LCM: <b>%s</b>. "
             "Counting by %d × %d = %d skips %d." % (a, b, l, lst(right), a, b, a * b, l))
        its.append(mcq("Which list shows the first three common multiples of %d and %d?" % (a, b), lst(right),
                       [lst(byprod), lst(mixed), lst(big)], e))

    for a, b in [(3, 4), (3, 8), (6, 10), (4, 14), (9, 12), (5, 6), (10, 12), (6, 15)]:
        l = L(a, b)
        g = gcd(a, b)
        cands = []
        if a * b != l:
            cands.append(a * b)
        cands += [2 * l, g, a + b, max(a, b)] if g > 1 else [2 * l, a + b, max(a, b)]
        e = lcm_e(a, b)
        if a * b == l:
            e += " %d and %d share no factor except 1, so here the LCM is %d × %d." % (a, b, a, b)
        else:
            e += " %d × %d = %d is a common multiple, but not the least. %d is the GCF." % (a, b, a * b, g)
        its.append(mcq("What is the least common multiple (LCM) of %d and %d?" % (a, b), l, cands, e))

    for xs in [(2, 5, 6), (3, 4, 6)]:
        l = L(*xs)
        p3 = prod(xs)
        l12 = L(xs[0], xs[1])
        cands = []
        if p3 != l:
            cands.append(p3)
        if l12 != l:
            cands.append(l12)
        cands += [sum(xs), 2 * l, max(xs)]
        lo = sorted(xs)
        e = ("Count by the biggest number, %d: %s. The first one that %d and %d also divide is <b>%d</b>."
             % (max(xs), lst(mults(max(xs), l)), lo[0], lo[1], l))
        if p3 != l:
            e += " %s = %d is a common multiple, but not the least." % (times(xs), p3)
        if l12 != l:
            e += " %d is the LCM of %d and %d only." % (l12, xs[0], xs[1])
        e += " %d is %s." % (sum(xs), " + ".join(str(x) for x in xs))
        its.append(mcq("What is the LCM of %d, %d and %d?" % xs, l, cands, e))

    nm, he, his = P.next()
    assert L(4, 10) == 20 and gcd(4, 10) == 2
    its.append(mcq("%s says the LCM of 4 and 10 is 40, because 4 × 10 = 40. Is %s right?" % (nm, he),
                   "No. The LCM is 20", ["Yes. 4 × 10 = 40", "No. The LCM is 2", "No. The LCM is 14"],
                   "Count by 10: 10, 20. 20 = 4 × 5, so the LCM is <b>20</b>. 40 is a common multiple, but not the least. "
                   "2 is the GCF, and 14 is 4 + 10."))
    nm, he, his = P.next()
    assert gcd(6, 9) == 3 and L(6, 9) == 18
    its.append(mcq("%s says the LCM of 6 and 9 is 3. Is %s right?" % (nm, he),
                   "No. 3 is the GCF. The LCM is 18", ["Yes. 3 divides both", "No. The LCM is 54", "No. The LCM is 15"],
                   "3 is the greatest common <b>factor</b>. A multiple can’t be smaller than the numbers. "
                   "Count by 9: 9, 18. 18 = 6 × 3, so the LCM is <b>18</b>."))
    nm, he, his = P.next()
    assert L(3, 12) == 12
    its.append(mcq("%s says the LCM of 3 and 12 is 12. Is %s right?" % (nm, he),
                   "Yes. 12 is a multiple of 3", ["No. The LCM is 36", "No. The LCM is 3", "No. The LCM is 15"],
                   "12 = 3 × 4, so 12 is a multiple of both numbers, and no smaller multiple of 12 exists. "
                   "The LCM is <b>12</b>. When the bigger number is a multiple of the smaller one, it is the LCM."))

    assert L(4, 10) == 20 and [L(2, 10), L(4, 6), L(20, 40)] == [10, 12, 40] and gcd(20, 40) == 20
    its.append(mcq("Which pair of numbers has an LCM of 20?", "4 and 10", ["2 and 10", "4 and 6", "20 and 40"],
                   "Count by 10: 10, 20. 20 = 4 × 5, so the LCM of 4 and 10 is <b>20</b>. The LCM of 2 and 10 is 10, "
                   "of 4 and 6 is 12, and of 20 and 40 is 40 (20 is their GCF)."))
    assert len(its) == 20, len(its)
    return {"title": "Least common multiple (LCM)", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    nm, he, his = P.next()
    assert L(10, 8) == 40 and gcd(10, 8) == 2
    its.append(mcq("Hot dogs come in packs of 10 and buns come in packs of 8. %s wants the same number of hot dogs and "
                   "buns for the school barbecue. What is the least number of each %s can buy?" % (nm, he),
                   "40 of each", ["80 of each", "2 of each", "18 of each"],
                   lcm_e(8, 10) + " So %s buys 40 of each. 10 × 8 = 80 also works, but it is not the least. "
                   "2 is the GCF, and 18 is 10 + 8." % he))
    nm, he, his = P.next()
    assert L(10, 8) // 8 == 5 and L(10, 8) // 10 == 4
    its.append(mcq("Hot dogs come in packs of 10 and buns come in packs of 8. %s buys the least number of packs so that "
                   "there is a bun for every hot dog, with none left over. How many packs of buns does %s buy?" % (nm, he),
                   "5 packs", ["4 packs", "40 packs", "8 packs"],
                   "The LCM of 10 and 8 is 40, so %s needs 40 buns: 40 ÷ 8 = <b>5 packs</b>. "
                   "4 packs is the number of packs of hot dogs (40 ÷ 10). 40 is the number of buns." % he))
    assert gcd(48, 36) == 12
    its.append(mcq("The school has 48 blue chairs and 36 red chairs for an assembly in the gym. Each row has only one "
                   "colour, and every row has the same number of chairs. What is the greatest number of chairs in each row?",
                   "12 chairs", ["6 chairs", "4 chairs", "144 chairs"],
                   "The row size must divide both 48 and 36. Common factors: %s. The GCF is <b>12</b>. "
                   "6 and 4 also work, but they are not the greatest. 144 is the LCM." % lst(cfs(48, 36))))
    assert 48 // 12 + 36 // 12 == 7 and 48 // 6 + 36 // 6 == 14
    its.append(mcq("48 blue chairs and 36 red chairs are set out in rows of 12, and each row has only one colour. "
                   "How many rows are there?", "7 rows", ["12 rows", "14 rows", "84 rows"],
                   "48 ÷ 12 = 4 blue rows and 36 ÷ 12 = 3 red rows. 4 + 3 = <b>7 rows</b>. "
                   "12 is the number of chairs in each row. 14 rows would be rows of 6. 84 is the total number of chairs."))
    assert L(8, 12) == 24 and gcd(8, 12) == 4 and 8 * 12 == 96
    its.append(mcq("In Surrey, one bus leaves a stop every 8 minutes and another bus leaves every 12 minutes. "
                   "Both buses leave at 7:00 a.m. When will they next leave at the same time?",
                   "7:24 a.m.", ["8:36 a.m.", "7:20 a.m.", "7:04 a.m."],
                   lcm_e(8, 12) + " So they leave together again 24 minutes later, at <b>7:24 a.m.</b> "
                   "8 × 12 = 96 minutes (8:36 a.m.) is not the first time. 20 is 8 + 12, and 4 is the GCF."))
    assert L(40, 60) == 120 and gcd(40, 60) == 20
    its.append(mcq("Two whale-watching boats leave Victoria. One leaves every 40 minutes and the other every 60 minutes. "
                   "Both leave at 9:00 a.m. When will they next leave together?",
                   "11:00 a.m.", ["10:00 a.m.", "10:40 a.m.", "9:20 a.m."],
                   lcm_e(40, 60) + " 120 minutes is 2 hours, so they leave together at <b>11:00 a.m.</b> "
                   "10:00 a.m. works for the second boat only. 10:40 a.m. uses 40 + 60 = 100 minutes, and 9:20 a.m. uses the GCF, 20."))
    assert L(2, 3, 5) == 30 and L(2, 3) == 6
    its.append(mcq("Three lights on a float in a Vancouver parade flash every 2, 3 and 5 seconds. They flash together now. "
                   "In how many seconds will all three next flash together?",
                   "30 seconds", ["10 seconds", "6 seconds", "15 seconds"],
                   "Count by 5: 5, 10, 15, 20, 25, 30. 30 is the first one that 2 and 3 also divide, so the LCM is "
                   "<b>30 seconds</b>. 10 is 2 + 3 + 5, 6 works for the first two lights only, and 15 works for the last two only."))
    nm, he, his = P.next()
    assert gcd(36, 48) == 12 and 48 // 12 == 4 and L(36, 48) == 144
    its.append(mcq("For the Terry Fox Run, %s has 36 water bottles and 48 granola bars. %s packs identical snack bags "
                   "with nothing left over. What is the greatest number of bags %s can make?" % (nm, cap(he), he),
                   "12 bags", ["6 bags", "144 bags", "4 bags"],
                   "The number of bags must divide both 36 and 48. Common factors: %s. The GCF is <b>12</b>. "
                   "6 also works, but it is not the greatest. 144 is the LCM, and 4 is the number of granola bars "
                   "in each bag." % lst(cfs(36, 48))))
    assert gcd(60, 84) == 12 and L(60, 84) == 420
    its.append(mcq("A bulletin board is 60 cm by 84 cm. The class covers it with equal squares of paper, as large as "
                   "possible, with no gaps or overlaps. What is the side length of each square?",
                   "12 cm", ["6 cm", "4 cm", "420 cm"],
                   "The side must divide both 60 and 84. Common factors: %s. The GCF is <b>12 cm</b>, which gives "
                   "5 rows of 7 squares. 420 is the LCM, and it is bigger than the board." % lst(cfs(60, 84))))
    nm, he, his = P.next()
    assert gcd(54, 90) == 18 and L(54, 90) == 270
    its.append(mcq("%s has two ropes for a canoe trip, 54 cm and 90 cm long. %s cuts both into pieces of the same "
                   "length, as long as possible, with nothing left over. How long is each piece?" % (nm, cap(he)),
                   "18 cm", ["9 cm", "6 cm", "270 cm"],
                   "The length must divide both 54 and 90. Common factors: %s. The GCF is <b>18 cm</b>: "
                   "3 pieces from the first rope and 5 from the second. 270 is the LCM." % lst(cfs(54, 90))))
    assert gcd(24, 30) == 6 and L(24, 30) == 120
    its.append(mcq("The Grade 6 classes have 24 boys and 30 girls. The teachers make teams for a soccer tournament. Each "
                   "team has the same number of boys and the same number of girls, and no one is left out. "
                   "What is the greatest number of teams?", "6 teams", ["3 teams", "54 teams", "120 teams"],
                   "Find the GCF of 24 and 30. Common factors: %s. The GCF is <b>6</b>, so there are 6 teams, each with "
                   "4 boys and 5 girls. 3 teams also works, but it is not the greatest. 54 is the total number of students, "
                   "and 120 is the LCM." % lst(cfs(24, 30))))
    nm, he, his = P.next()
    assert L(6, 8, 12) == 24 and 6 * 8 * 12 == 576 and G(6, 8, 12) == 2
    its.append(mcq("For a class picnic in Stanley Park, granola bars come in boxes of 6, juice boxes in packs of 8 and "
                   "apples in bags of 12. %s wants the same number of each, as few as possible. How many of each does %s buy?"
                   % (nm, he), "24 of each", ["576 of each", "26 of each", "2 of each"],
                   "Count by 12: 12, 24. 24 is also a multiple of 6 and of 8, so the LCM is <b>24</b>. "
                   "6 × 8 × 12 = 576 is far more than needed, 26 is 6 + 8 + 12, and 2 is the GCF."))
    nm, he, his = P.next()
    assert G(18, 24, 30) == 6 and L(18, 24, 30) == 360
    its.append(mcq("%s packs 18 granola bars, 24 apples and 30 juice boxes for a field trip to Grouse Mountain. Every bag "
                   "must be identical, with nothing left over. What is the greatest number of bags?" % nm,
                   "6 bags", ["3 bags", "2 bags", "360 bags"],
                   "Common factors of 18, 24 and 30: %s. The GCF is <b>6</b>, so each bag has 3 granola bars, 4 apples "
                   "and 5 juice boxes. 3 and 2 also work, but they are not the greatest. 360 is the LCM." % lst(cfs(18, 24, 30))))
    nm, he, his = P.next()
    assert L(4, 6) == 12 and gcd(4, 6) == 2
    its.append(mcq("%s has hockey practice every 4 days and swimming lessons every 6 days. Both are on April 2. "
                   "What is the next date when %s has both?" % (nm, he),
                   "April 14", ["April 26", "April 12", "April 4"],
                   "The LCM of 4 and 6 is 12, so both happen again 12 days later: April 2 + 12 days = <b>April 14</b>. "
                   "April 26 uses 4 × 6 = 24 days, April 12 uses 4 + 6 = 10 days, and April 4 uses the GCF, 2."))
    nm, he, his = P.next()
    assert gcd(36, 60) == 12 and 60 // 12 == 5 and 36 // 12 == 3 and 60 // 4 == 15
    its.append(mcq("%s makes the greatest number of identical gift bags from 36 pencils and 60 erasers, with nothing left "
                   "over. How many erasers are in each bag?" % nm,
                   "5 erasers", ["12 erasers", "3 erasers", "15 erasers"],
                   "The GCF of 36 and 60 is 12, so there are 12 bags. 60 ÷ 12 = <b>5 erasers</b> in each bag "
                   "(and 36 ÷ 12 = 3 pencils). 12 is the number of bags, and 15 would come from using only 4 bags."))
    nm, he, his = P.next()
    assert L(6, 9) == 18 and gcd(6, 9) == 3
    its.append(mcq("Orca stickers come in sheets of 6 and salmon stickers come in sheets of 9. %s wants the same number "
                   "of orca and salmon stickers, as few as possible. How many of each does %s get?" % (nm, he),
                   "18 of each", ["54 of each", "3 of each", "15 of each"],
                   lcm_e(6, 9) + " That is 3 sheets of orcas and 2 sheets of salmon. 6 × 9 = 54 is not the least, "
                   "3 is the GCF, and 15 is 6 + 9."))
    assert gcd(48, 60) == 12
    its.append(mcq("A teacher sets out 48 chairs and 60 desks in rows. Every row has the same number of items, and each "
                   "row has only chairs or only desks. To find the most items in each row, what should you find?",
                   "The GCF of 48 and 60", ["The LCM of 48 and 60", "48 × 60", "48 + 60"],
                   "The row size must divide both numbers, and it must be as big as possible. That is the <b>GCF</b> (12)."))
    assert L(15, 20) == 60
    its.append(mcq("On the SkyTrain platform, one sign flashes every 15 seconds and another every 20 seconds. To find when "
                   "they next flash together, what should you find?",
                   "The LCM of 15 and 20", ["The GCF of 15 and 20", "15 × 20", "15 + 20"],
                   "The flashes repeat and must line up again, so you need a common <b>multiple</b>: the <b>LCM</b> "
                   "(60 seconds). 15 × 20 = 300 is a common multiple, but not the first."))
    nm, he, his = P.next()
    assert L(6, 4) == 12
    its.append(mcq("Juice boxes come in packs of 6 and yogurt cups come in packs of 4. %s says %s must buy 24 of each to "
                   "have the same number. Is %s right?" % (nm, he, he),
                   "No. 12 of each is enough", ["Yes. 6 × 4 = 24", "No. 10 of each is enough", "No. 2 of each is enough"],
                   lcm_e(4, 6) + " So 2 packs of juice boxes and 3 packs of yogurt give <b>12 of each</b>. 24 also works, "
                   "but it is not the least. 10 is 6 + 4, and 2 is the GCF."))
    nm, he, his = P.next()
    assert gcd(16, 24) == 8 and L(16, 24) == 48 and 16 + 24 == 40
    its.append(mcq("%s has 16 red beads and 24 blue beads. %s wants to make the greatest number of identical bracelets "
                   "with no beads left over, so %s finds the LCM of 16 and 24, which is 48. Is %s right?"
                   % (nm, cap(he), he, he),
                   "No. Use the GCF: 8 bracelets", ["Yes. Make 48 bracelets", "No. Use the GCF: 4 bracelets", "No. Make 40 bracelets"],
                   "Sharing beads into equal groups means the number of bracelets must divide 16 and 24: use the "
                   "<b>GCF</b>, which is <b>8</b>. Each bracelet gets 2 red and 3 blue beads. 48 bracelets would need more beads "
                   "than %s has. 4 is a common factor, but not the greatest, and 40 is 16 + 24." % he))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: packages, schedules and equal groups", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors, multiples and primes</h2>"
        "<p>A <b>factor</b> divides a number with no remainder. A <b>multiple</b> is the number times 1, 2, 3, … "
        "The factors of 12 are 1, 2, 3, 4, 6 and 12. The multiples of 12 are 12, 24, 36, …</p>"
        "<p>A <b>prime number</b> has exactly two factors, 1 and itself (2, 3, 5, 7, 11, …). A <b>composite number</b> "
        "has more than two factors. The number 1 is neither.</p>"
        "<h2>The greatest common factor (GCF)</h2>"
        "<p>A <b>common factor</b> divides two or more numbers. The <b>greatest common factor</b> is the biggest one. "
        "List the factors of each number, circle the ones in every list, and pick the greatest.</p>"
        "<figure class='sn-fig'>" + factor_rows_svg(18, 24) +
        "<figcaption>The common factors of 18 and 24 are 1, 2, 3 and 6. The GCF is 6.</figcaption></figure>"
        + ex("Example", "Find the GCF of 20 and 32.",
             "Factors of 20: 1, 2, 4, 5, 10, 20. Factors of 32: 1, 2, 4, 8, 16, 32. Common factors: 1, 2, 4.", "4")
        + "<p>For bigger numbers, use factor trees. Multiply the primes that the numbers <b>share</b>.</p>"
        "<figure class='sn-fig'>" + tree_pair_svg(24, 36) +
        "<figcaption>24 = 2 × 2 × 2 × 3 and 36 = 2 × 2 × 3 × 3. They share 2 × 2 × 3, so the GCF is 12.</figcaption></figure>"
        "<h2>The least common multiple (LCM)</h2>"
        "<p>A <b>common multiple</b> is in the skip-counting list of every number. The <b>least common multiple</b> "
        "is the first one. Count by the biggest number and stop at the first number the others divide into.</p>"
        "<figure class='sn-fig'>" + multiples_svg(4, 6, 36, show=True) +
        "<figcaption>Multiples of 4 and of 6. They meet at 12, 24 and 36. The LCM is 12, not 4 × 6 = 24.</figcaption></figure>"
        + ex("Example", "Find the LCM of 3, 4 and 6.",
             "Count by 6: 6, 12. 6 is not a multiple of 4, but 12 = 3 × 4 = 4 × 3 = 6 × 2.", "12")
        + "<h2>GCF or LCM?</h2>"
        + table(["The problem asks…", "Use", "Example"], [
            ["The greatest number of identical bags, groups or teams", "GCF", "36 water bottles and 48 granola bars make 12 bags"],
            ["The biggest equal rows, pieces or squares with nothing left over", "GCF", "48 and 36 chairs: rows of 12"],
            ["When repeating events happen together again", "LCM", "Buses every 8 and 12 minutes: 24 minutes"],
            ["The least number to buy so pack sizes match", "LCM", "Hot dogs in 10s, buns in 8s: 40 of each"],
        ])
        + "<p>Check your answer: a GCF is never bigger than the smallest number, and an LCM is never smaller than "
        "the biggest number.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up GCF and LCM: “the GCF of 8 and 12 is 24”", "24 is the LCM. The GCF is 4"],
            ["Stopping at any common factor: GCF of 24 and 36 is 6", "Find the greatest one: 12"],
            ["Multiplying for the LCM: LCM of 4 and 6 is 24", "24 is a common multiple, but 12 comes first"],
            ["Thinking every odd number is prime", "21 = 3 × 7, so 21 is composite"],
            ["Calling 1 a prime number", "1 has only one factor. It is neither prime nor composite"],
            ["Using only two of three numbers", "Check that the answer works for every number"],
        ])
    )


FAQ = [
    {"q": "How do you find the GCF of two numbers?",
     "a": "List the factors of each number and pick the greatest one that is in both lists. For 18 and 24, the common factors are 1, 2, 3 and 6, so the GCF is 6."},
    {"q": "How do you find the least common multiple?",
     "a": "Count by the bigger number until you reach a number the other one also divides. For 4 and 6, count 6, 12; 12 is a multiple of 4, so the LCM is 12, not 4 × 6 = 24."},
    {"q": "How do you know whether to use GCF or LCM in a word problem?",
     "a": "Use the GCF when you share things into the greatest number of identical groups, or the biggest equal rows or pieces. Use the LCM when events repeat and line up again, or when you buy packs so two amounts match, like hot dogs and buns."},
    {"q": "Is GCF and LCM in the BC Grade 6 math curriculum?",
     "a": "Yes. The BC Grade 6 math curriculum includes factors and multiples, with the greatest common factor and the least common multiple. Students also use prime and composite numbers to find them."},
]


def gen():
    rnd = random.Random(56802)
    P = People(rnd)
    sets = [set_factors(P), set_primes(P), set_gcf(P), set_lcm(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "gcf-and-lcm", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Greatest Common Factor and Least Common Multiple",
        "seo_title": "Grade 6 GCF and LCM Worksheets (BC Curriculum) – Free Math with Answer Key",
        "short_title": "GCF and LCM",
        "domain": "Number",
        "standard_code": "Grade 6: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Factors and multiples – greatest common factor and least common multiple",
        "meta_desc": "Free Grade 6 math worksheets for the BC curriculum: factors and multiples, prime and composite numbers, the greatest common factor, the least common multiple, and GCF or LCM word problems. 100 questions with an answer key.",
        "key_big": "The GCF is the biggest number that divides all the numbers. The LCM is the first number they all divide into.",
        "key_sub": "For 4 and 6: the GCF is 2 and the LCM is 12, not 4 × 6 = 24. Use the GCF for equal groups, rows and pieces, and the LCM for things that repeat or must match, like buses or hot dogs and buns.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(factor trees|multiples of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
