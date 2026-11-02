# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Greatest Common Factor and Least Common Multiple (6.NS.B.4)
  python tools/gen_us_math_g6_gcf_lcm.py
GCF of whole numbers up to 100, LCM of whole numbers up to 12, and factoring out the GCF
with the distributive property (36 + 8 = 4 × (9 + 2)).
Every GCF, LCM, factorization and expression is checked in code.
Wrong answers come from real mistakes: a common factor that is not the greatest, a factor of only
one number, the product a × b as the LCM, swapping GCF and LCM, factoring out a factor that is not
the greatest, dividing only one term, writing each prime only once.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from math import gcd, prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8178"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ math
def f(n):
    return "{:,}".format(int(n))


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def cfs(a, b):
    return [d for d in factors(min(a, b)) if a % d == 0 and b % d == 0]


def lcm(a, b):
    return a * b // gcd(a, b)


def is_prime(n):
    return len(factors(n)) == 2


def primes_of(n):
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def lst(xs):
    return ", ".join(f(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def mults(d, upto):
    return [d * k for k in range(1, upto // d + 1)]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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
def split(n):
    """Most balanced factor pair of n (both > 1), or None if n is prime."""
    best = None
    for a in range(2, int(n ** 0.5) + 1):
        if n % a == 0:
            best = (a, n // a)
    return best


def tree(n):
    s = split(n)
    return (n, None) if s is None else (n, [tree(s[0]), tree(s[1])])


def leaves(t):
    return [t[0]] if t[1] is None else leaves(t[1][0]) + leaves(t[1][1])


def depth(t):
    return 1 if t[1] is None else 1 + max(depth(c) for c in t[1])


def tree_svg(n, step=44, dy=50):
    """Factor tree: each number splits into a factor pair; the primes at the ends are circled."""
    t = tree(n)
    assert prod(leaves(t)) == n
    o = 22
    W = (len(leaves(t)) - 1) * step + 2 * o
    H = (depth(t) - 1) * dy + 2 * o
    pos = {}
    s = []
    cnt = [0]

    def place(node, lvl):
        if node[1] is None:
            x = o + cnt[0] * step
            cnt[0] += 1
        else:
            xs = [place(c, lvl + 1) for c in node[1]]
            x = sum(xs) / 2
        y = o + lvl * dy
        pos[id(node)] = (x, y)
        return x

    place(t, 0)

    def draw(node):
        x, y = pos[id(node)]
        if node[1] is not None:
            for c in node[1]:
                cx, cy = pos[id(c)]
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                         % (x, y + 9, cx, cy - 15, GRAY))
                draw(c)
        if node[1] is None:
            s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, FILL, GREEN))
        s.append(text(x, y + 6, str(node[0]), 17))

    draw(t)
    return svg_wrap(W, H, "".join(s), "factor tree for %d" % n)


def area_svg(a, b, c, unit=16, show=False):
    """Area model for a × (b + c): one rectangle a tall, split into widths b and c."""
    ox, oy = 26, 24
    W = ox + (b + c) * unit + 8
    H = oy + a * unit + 8
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
         % (ox, oy, b * unit, a * unit, FILL, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='#f6e9c8' stroke='%s' stroke-width='2'/>"
         % (ox + b * unit, oy, c * unit, a * unit, GREEN),
         text(ox + b * unit / 2, oy - 7, str(b)), text(ox + b * unit + c * unit / 2, oy - 7, str(c)),
         text(ox - 8, oy + a * unit / 2 + 6, str(a), anchor="end")]
    if show:
        s.append(text(ox + b * unit / 2, oy + a * unit / 2 + 6, "%d × %d = %d" % (a, b, a * b), 15))
        s.append(text(ox + b * unit + c * unit / 2, oy + a * unit / 2 + 6, str(a * c), 15))
    return svg_wrap(W, H, "".join(s), "area model for %d × (%d + %d)" % (a, b, c))


def factor_rows_svg(a, b):
    """Lesson: the factors of a and b in two rows, the common ones circled, the GCF in red."""
    fa, fb = factors(a), factors(b)
    g = gcd(a, b)
    step, lx, o = 40, 66, 8
    cols = sorted(set(fa) | set(fb))
    W = lx + len(cols) * step + o
    H = 2 * 40 + 2 * o
    s = []
    for r, (n, fs) in enumerate([(a, fa), (b, fb)]):
        y = o + 26 + r * 40
        s.append(text(lx - 14, y, "%d:" % n, 17, anchor="end"))
        for d in fs:
            x = lx + cols.index(d) * step + step / 2
            if d in fa and d in fb:
                s.append("<circle cx='%.1f' cy='%d' r='16' fill='%s' stroke='%s' stroke-width='2'/>"
                         % (x, y - 6, "#f6d5d0" if d == g else FILL, RED if d == g else GREEN))
            s.append(text(x, y, str(d), 16, col=RED if d == g else INK))
    return svg_wrap(W, H, "".join(s), "factors of %d and %d with the common factors circled" % (a, b))


def multiples_svg(a, b, top):
    """Lesson: multiples of a and b placed by size on two rows; common multiples joined."""
    sc, ox, o = 8, 52, 8
    W = ox + top * sc + 22
    H = 116
    ya, yb = 34, 92
    s = []
    for n, y in [(a, ya), (b, yb)]:
        s.append(text(ox - 22, y + 6, "%d:" % n, 17, anchor="end"))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (ox, y, ox + top * sc + 6, y, GRAY))
    for m in range(lcm(a, b), top + 1, lcm(a, b)):
        x = ox + m * sc
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                 % (x, ya + 12, x, yb - 12, RED))
    for n, y, up in [(a, ya, True), (b, yb, False)]:
        for m in mults(n, top):
            x = ox + m * sc
            common = m % a == 0 and m % b == 0
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (x, y, RED if common else GREEN))
            s.append(text(x, y - 10 if up else y + 22, str(m), 14, col=RED if common else INK))
    return svg_wrap(W, H, "".join(s), "multiples of %d and %d up to %d" % (a, b, top))


# ============================================================ set 1: common factors and the GCF
def gcf_e(a, b):
    g = gcd(a, b)
    return ("Factors of %d: %s. Factors of %d: %s. Common factors: %s. The greatest is <b>%d</b>."
            % (a, lst(factors(a)), b, lst(factors(b)), lst(cfs(a, b)), g))


def one_only(a, b):
    """Biggest factor of the smaller number (less than it) that is NOT a factor of the other number."""
    s, l = min(a, b), max(a, b)
    xs = [d for d in factors(s) if l % d and d < s]
    return xs[-1] if xs else None


def set_gcf(P):
    its = []
    for a, b in [(12, 18), (16, 40), (30, 45), (24, 36)]:
        c = cfs(a, b)
        no_g = c[:-1]
        small = factors(min(a, b))
        no1 = c[1:]
        e = gcf_e(a, b) + " Keep 1 and the GCF in the list, and use only numbers that divide <b>both</b>."
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c),
                       [lst(no_g), lst(small), lst(no1)], e))

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
        e = ("%d is a factor of %d, but %d ÷ %d = %d R %d, so <b>%d</b> is not a common factor. "
             "%d, %d and %d divide both numbers." % ((bad, only, other, bad, other // bad, other % bad, bad) + tuple(good)))
        its.append(mcq("Which number is <b>not</b> a common factor of %d and %d?" % (a, b), bad, good, e))

    for a, b in [(14, 21), (20, 30), (18, 27), (13, 52), (9, 20), (28, 42), (48, 72), (36, 90), (54, 81), (64, 96)]:
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
        cands += big[-1:] + [f(a * b)]
        e = gcf_e(a, b)
        if g == 1:
            e += " 9 and 20 share no factor except 1, so their GCF is 1."
        elif g == min(a, b):
            e += " %d divides %d (%d × %d = %d), so the smaller number is the GCF." % (a, b, a, b // a, b)
        elif len(c) > 1 and c[-2] > 1:
            e += " %d is a common factor too, but not the greatest." % c[-2]
        else:
            e += " %d is a factor of %d only, so it is not a common factor." % (one_only(a, b), min(a, b))
        its.append(mcq("What is the greatest common factor (GCF) of %d and %d?" % (a, b), g, cands, e))

    nm, he, his = P.next()
    its.append(mcq("%s says the GCF of 30 and 45 is 5, because 5 is a factor of both. Is %s right?" % (nm, he),
                   "No. The GCF is 15", ["Yes. 5 divides both", "No. The GCF is 90", "No. The GCF is 30"],
                   "5 is a common factor, but not the greatest. 15 × 2 = 30 and 15 × 3 = 45, so the GCF is <b>15</b>. "
                   "90 is the LCM, and 30 is not a factor of 45."))
    nm, he, his = P.next()
    its.append(mcq("%s says the GCF of 16 and 48 is 16. Is %s right?" % (nm, he),
                   "Yes. 16 divides 48", ["No. The GCF is 8", "No. It can’t be 16", "No. The GCF is 4"],
                   "16 × 3 = 48, so 16 is a factor of both numbers, and no factor of 16 is bigger than 16. "
                   "The GCF <b>can</b> be the smaller number."))
    assert gcd(30, 45) == 15 and gcd(16, 48) == 16
    assert len(its) == 20, len(its)
    return {"title": "Common factors and the GCF", "items": its}


# ============================================================ set 2: common multiples and the LCM
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
             "Counting by %d × %d = %d skips %d." % (lst(right), a, b, a * b, l))
        its.append(mcq("Which list shows the first 3 common multiples of %d and %d?" % (a, b), lst(right),
                       [lst(byprod), lst(mixed), lst(big)], e))

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
            e += " %d × %d = %d is a common multiple, but not the least." % (a, b, a * b)
        its.append(mcq("What is the least common multiple (LCM) of %d and %d?" % (a, b), l, cands, e))

    for a, b, right, wrong in [(3, 8, 48, [11, 32, 30]), (5, 6, 60, [11, 25, 36])]:
        assert right % a == 0 and right % b == 0 and wrong[0] == a + b
        assert all(w % a or w % b for w in wrong)
        e = ("%d = %d × %d and %d = %d × %d, so <b>%d</b> is a common multiple. %d is %d + %d. "
             "%d is a multiple of only one of the numbers, and so is %d."
             % (right, a, right // a, right, b, right // b, right, wrong[0], a, b, wrong[1], wrong[2]))
        its.append(mcq("Which number is a common multiple of %d and %d?" % (a, b), right, wrong, e))

    assert 30 % 4 and all(x % 4 == 0 and x % 10 == 0 for x in (20, 40, 60))
    its.append(mcq("Which number is <b>not</b> a common multiple of 4 and 10?", 30, [20, 40, 60],
                   "30 is a multiple of 10, but 30 ÷ 4 = 7 R 2, so <b>30</b> is not a multiple of 4. "
                   "The LCM of 4 and 10 is 20, and 20, 40 and 60 are all multiples of 20."))

    nm, he, his = P.next()
    its.append(mcq("%s says the LCM of 6 and 8 is 48, because 6 × 8 = 48. Is %s right?" % (nm, he),
                   "No. The LCM is 24", ["Yes. 6 × 8 = 48", "No. The LCM is 2", "No. The LCM is 14"],
                   lcm_e(6, 8) + " 48 is a common multiple, but not the least. 2 is the GCF, and 14 is 6 + 8."))
    nm, he, his = P.next()
    its.append(mcq("%s says the LCM of 5 and 10 is 50. Is %s right?" % (nm, he),
                   "No. The LCM is 10", ["Yes. 5 × 10 = 50", "No. The LCM is 5", "No. The LCM is 15"],
                   "10 is a multiple of 5 (5 × 2 = 10) and of 10, so the LCM is <b>10</b>. "
                   "When one number is a multiple of the other, the bigger number is the LCM."))
    assert lcm(6, 8) == 24 and lcm(5, 10) == 10

    pairs = ["5 and 8", "4 and 6", "6 and 9", "8 and 12"]
    ok = [lcm(*map(int, p.split(" and "))) == prod(map(int, p.split(" and "))) for p in pairs]
    assert ok == [True, False, False, False]
    its.append(mcq("For which pair is the LCM equal to the two numbers multiplied together?", pairs[0], pairs[1:],
                   "5 and 8 share no factor except 1, so the LCM is 5 × 8 = <b>40</b>. The other pairs share a factor: "
                   "the LCM of 4 and 6 is 12 (not 24), of 6 and 9 is 18 (not 54), and of 8 and 12 is 24 (not 96)."))

    good, bad = "6 and 8", ["4 and 6", "2 and 12", "6 and 12"]
    assert lcm(6, 8) == 24 and all(lcm(*map(int, p.split(" and "))) != 24 for p in bad)
    its.append(mcq("Which pair of numbers has an LCM of 24?", good, bad,
                   "Multiples of 8: 8, 16, 24. Multiples of 6: 6, 12, 18, 24. So the LCM of 6 and 8 is <b>24</b>. "
                   "4 × 6 = 24 and 2 × 12 = 24, but their LCM is 12. The LCM of 6 and 12 is also 12."))
    assert len(its) == 20, len(its)
    return {"title": "Common multiples and the LCM", "items": its}


# ============================================================ set 3: prime factorization
def set_primes(P):
    its = []
    for n in [36, 60, 90, 100]:
        t = tree(n)
        ps = sorted(leaves(t))
        assert all(is_prime(p) for p in ps) and prod(ps) == n
        first = times(split(n))
        once = times(sorted(set(ps)))
        with1 = times([1] + ps)
        e = ("Keep splitting until every branch ends in a prime: %s = <b>%s</b>. "
             "%s is not finished, because %s are not prime. 1 is not prime, so it is not written."
             % (n, times(ps), first, " and ".join(str(x) for x in split(n) if not is_prime(x))))
        its.append(mcq(fig(tree_svg(n)) + "What is the prime factorization of %d?" % n, times(ps),
                       [first, once, with1], e))

    for ps in [[2, 2, 3, 5], [2, 3, 3, 5], [2, 2, 2, 7], [3, 3, 7]]:
        v = prod(ps)
        sm = sum(ps)
        once = prod(sorted(set(ps)))
        e = ("Multiply all the primes, including the repeated ones: %s = <b>%d</b>. Adding them gives %d, "
             "and using each prime only once gives %d." % (times(ps), v, sm, once))
        its.append(mcq("Which number has the prime factorization %s?" % times(ps), v,
                       [sm, once, v // ps[0], v // ps[-1], v * ps[0]], e))

    for a, b in [(24, 36), (45, 75), (56, 98), (60, 84)]:
        pa, pb = primes_of(a), primes_of(b)
        shared = []
        rest = list(pb)
        for p in pa:
            if p in rest:
                shared.append(p)
                rest.remove(p)
        g = prod(shared)
        assert g == gcd(a, b)
        once = prod(sorted(set(shared)))
        c = cfs(a, b)
        e = ("Circle the primes the two lists share: %s. Multiply them: %s = <b>%d</b>. "
             "Use a shared prime as many times as it appears in <b>both</b> lists.%s"
             % (times(shared), times(shared), g,
                " Using each shared prime only once gives %d." % once if once != g else ""))
        its.append(mcq("%d = %s and %d = %s. What is the GCF of %d and %d?" % (a, times(pa), b, times(pb), a, b),
                       g, [once, lcm(a, b), c[-2], f(a * b)], e))

    for a, b in [(8, 12), (9, 12), (10, 12)]:
        pa, pb = primes_of(a), primes_of(b)
        l = lcm(a, b)
        need = []
        for p in sorted(set(pa + pb)):
            need += [p] * max(pa.count(p), pb.count(p))
        assert prod(need) == l
        once = prod(sorted(set(pa + pb)))
        e = ("Use each prime the greatest number of times it appears in either list: %s = <b>%d</b>. "
             "%d × %d = %d uses the shared primes twice." % (times(need), l, a, b, a * b))
        its.append(mcq("%d = %s and %d = %s. What is the LCM of %d and %d?" % (a, times(pa), b, times(pb), a, b),
                       l, [a * b, gcd(a, b), once, max(a, b)], e))

    for a, b in [(4, 10), (6, 9), (8, 12), (6, 10), (9, 12)]:
        g, l = gcd(a, b), lcm(a, b)
        c = cfs(a, b)
        cf2 = c[-2] if len(c) > 1 else 1
        ch = lambda x, y: "GCF %d, LCM %d" % (x, y)
        e = ("Factors of %d: %s. Factors of %d: %s. GCF = <b>%d</b>. %s So LCM = <b>%d</b>. "
             "The GCF is never bigger than the numbers, and the LCM is never smaller."
             % (a, lst(factors(a)), b, lst(factors(b)), g, lcm_e(a, b).split(" The first")[0], l))
        its.append(mcq("Which is true for %d and %d?" % (a, b), ch(g, l), [ch(l, g), ch(g, a * b), ch(cf2, l), ch(1, a * b)], e))
    assert len(its) == 20, len(its)
    return {"title": "Prime factorization, GCF and LCM", "items": its}


# ============================================================ set 4: distributive property
def expr(g, x, y):
    return "%d × (%d + %d)" % (g, x, y)


def set_dist(P):
    its = []
    for a, b, c in [(6, 5, 7), (3, 8, 4), (4, 7, 5), (5, 6, 3)]:
        right = "%d + %d" % (a * b, a * c)
        e = ("The two parts of the rectangle are %d × %d = %d and %d × %d = %d. So %s = <b>%s</b>. "
             "Multiply %d by <b>both</b> numbers in the parentheses." % (a, b, a * b, a, c, a * c, expr(a, b, c), right, a))
        cands = ["%d + %d" % (a * b, c), "%d + %d" % (a + b, a + c), "%d + %d" % (a, b * c)]
        vals = [a * b + c, a + b + a + c, a + b * c]
        assert a * (b + c) not in vals
        its.append(mcq(fig(area_svg(a, b, c)) + "The rectangle shows %s. Which sum is equal to %s?"
                       % (expr(a, b, c), expr(a, b, c)), right, cands, e))

    for x, y in [(24, 40), (18, 27), (45, 60), (56, 42), (32, 80), (20, 50), (63, 81), (48, 18)]:
        g = gcd(x, y)
        c = cfs(x, y)
        h = c[-2]
        assert h > 1 and gcd(x // g, y // g) == 1 and g * (x // g + y // g) == x + y
        right = expr(g, x // g, y // g)
        small = expr(h, x // h, y // h)
        onefirst = expr(g, x // g, y)
        nopar = "%d × %d + %d" % (g, x // g, y // g)
        e = ("The GCF of %d and %d is %d. %d = %d × %d and %d = %d × %d, so %d + %d = <b>%s</b>. "
             "Check: %d and %d have no common factor, and %d × %d = %d. %s uses %d, which is not the greatest."
             % (x, y, g, x, g, x // g, y, g, y // g, x, y, right, x // g, y // g, g, x // g + y // g, x + y,
                small, h))
        its.append(mcq("Factor out the GCF to rewrite %d + %d as a product." % (x, y), right,
                       [small, onefirst, nopar], e))

    for x, y, g in [(42, 70, 14), (36, 84, 12)]:
        assert gcd(x, y) == g
        m = y // g
        e = ("%d ÷ %d = %d, so the missing number is <b>%d</b>. Check: %d × (%d + %d) = %d × %d = %d = %d + %d."
             % (y, g, m, m, g, x // g, m, g, x // g + m, g * (x // g + m), x, y))
        its.append(mcq("%d + %d = %d × (%d + <b>?</b>). What number is missing?" % (x, y, g, x // g), m,
                       [y, 2 * m, y - g], e))

    for x, y in [(45, 75), (56, 98)]:
        g = gcd(x, y)
        c = cfs(x, y)
        e = ("%d = %d × %d and %d = %d × %d, so the missing factor is the GCF, <b>%d</b>. Check: %d × %d = %d = %d + %d."
             % (x, g, x // g, y, g, y // g, g, g, x // g + y // g, g * (x // g + y // g), x, y))
        its.append(mcq("%d + %d = <b>?</b> × (%d + %d). What number is missing?" % (x, y, x // g, y // g), g,
                       [c[-2], x + y, x // g + y // g], e))

    claims = [
        (24, 36, 6, "No. Use 12 × (2 + 3)",
         ["Yes. 6 × 10 = 60", "Yes. 6 is a factor of both", "No. Use 2 × (12 + 18)"],
         "6 × (4 + 6) is equal to 60, but 4 and 6 still share the factor 2, so 6 is not the GCF. "
         "The GCF of 24 and 36 is 12: 24 + 36 = <b>12 × (2 + 3)</b>."),
        (30, 45, 15, "Yes. 2 and 3 share no factor",
         ["No. Use 5 × (6 + 9)", "No. Use 3 × (10 + 15)", "No. The GCF is 5"],
         "15 × 2 = 30 and 15 × 3 = 45, and 2 and 3 have no common factor except 1. So 15 is the GCF and "
         "<b>15 × (2 + 3)</b> is right."),
        (16, 40, 8, "No. Use 8 × (2 + 5)",
         ["Yes. 8 is the GCF", "No. Use 4 × (4 + 10)", "No. Use 2 × (8 + 20)"],
         "8 is the GCF, but both numbers must be divided by 8: 16 ÷ 8 = 2 and 40 ÷ 8 = 5. "
         "So 16 + 40 = <b>8 × (2 + 5)</b>. 8 × (2 + 40) = 336, not 56."),
        (27, 63, 9, "Yes. 3 and 7 share no factor",
         ["No. Use 3 × (9 + 21)", "No. Use 9 × 3 + 7", "No. The GCF is 3"],
         "9 × 3 = 27 and 9 × 7 = 63, and 3 and 7 have no common factor except 1. So 9 is the GCF and "
         "<b>9 × (3 + 7)</b> is right. 3 is a common factor, but not the greatest."),
    ]
    written = {24: "6 × (4 + 6)", 30: "15 × (2 + 3)", 16: "8 × (2 + 40)", 27: "9 × (3 + 7)"}
    for x, y, used, right, wrong, e in claims:
        nm, he, his = P.next()
        w = written[x]
        val = eval(w.replace("×", "*"))
        assert (val == x + y and used == gcd(x, y)) == right.startswith("Yes")
        its.append(mcq("%s factors out the GCF and writes %d + %d = %s. Is %s right?" % (nm, x, y, w, he),
                       right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Factor out the GCF: the distributive property", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def kits(n1, t1, n2, t2, unit, wrong, extra=""):
        g = gcd(n1, n2)
        nm, he, his = P.next()
        q = ("%s has %d %s and %d %s. %s wants to make identical %s with nothing left over. "
             "What is the greatest number of %s %s can make?" % (nm, n1, t1, n2, t2, cap(he), unit, unit, he))
        e = ("Find the GCF of %d and %d. Common factors: %s. The GCF is <b>%d</b>, so %s can make %d %s, "
             "each with %d %s and %d %s.%s" % (n1, n2, lst(cfs(n1, n2)), g, he, g, unit, n1 // g, t1, n2 // g, t2, extra))
        return mcq(q, "%d %s" % (g, unit), ["%d %s" % (w, unit) for w in wrong], e)

    its.append(kits(24, "pencils", 36, "erasers", "kits", [6, 72, 3], " 6 kits would work too, but 12 is greater."))
    its.append(kits(40, "apples", 56, "oranges", "baskets", [4, 280, 7], " 280 is the LCM, not the GCF."))
    its.append(kits(16, "red roses", 28, "white roses", "bouquets", [2, 112, 7], " 7 is the number of white roses in each bouquet."))

    nm, he, his = P.next()
    g = gcd(18, 27)
    its.append(mcq("A coach has 18 boys and 27 girls. %s wants teams that each have the same number of boys and the same "
                   "number of girls, with no one left out. What is the greatest number of teams?" % cap(he),
                   "%d teams" % g, ["3 teams", "54 teams", "45 teams"],
                   "Find the GCF of 18 and 27. Common factors: %s. The GCF is <b>9</b>, so there are 9 teams, "
                   "each with 2 boys and 3 girls. 45 is 18 + 27, the total number of students." % lst(cfs(18, 27))))
    assert g == 9

    nm, he, his = P.next()
    its.append(mcq("%s has two ribbons, 48 cm and 60 cm long. %s cuts both into pieces that are all the same length, with "
                   "nothing left over. What is the longest each piece can be?" % (nm, cap(he)),
                   "12 cm", ["6 cm", "240 cm", "4 cm"],
                   "The length must divide both 48 and 60. Common factors: %s. The GCF is <b>12 cm</b>: "
                   "4 pieces from the first ribbon and 5 from the second. 240 is the LCM, longer than both ribbons."
                   % lst(cfs(48, 60))))
    assert gcd(48, 60) == 12 and lcm(48, 60) == 240

    nm, he, his = P.next()
    its.append(mcq("A garden is 30 ft by 42 ft. %s wants to split it into equal square plots with no space left over. "
                   "What is the largest side length the squares can have?" % nm,
                   "6 ft", ["3 ft", "2 ft", "210 ft"],
                   "The side must divide both 30 and 42. Common factors: %s. The GCF is <b>6 ft</b>, which gives "
                   "5 rows of 7 squares. 210 is the LCM, and it is bigger than the garden." % lst(cfs(30, 42))))
    assert gcd(30, 42) == 6 and lcm(30, 42) == 210

    nm, he, his = P.next()
    its.append(mcq("Paper plates come in packs of 12 and cups come in packs of 8. %s wants the same number of plates and "
                   "cups. What is the least number of each %s can buy?" % (nm, he),
                   "24 of each", ["96 of each", "4 of each", "48 of each"],
                   lcm_e(8, 12) + " So %s buys 24 of each: 2 packs of plates and 3 packs of cups. 12 × 8 = 96 also works, "
                   "but it is not the least." % he))

    its.append(mcq("A red light flashes every 4 seconds and a blue light flashes every 10 seconds. They flash together "
                   "now. In how many seconds will they next flash together?",
                   "20 seconds", ["40 seconds", "14 seconds", "2 seconds"],
                   lcm_e(4, 10) + " 4 × 10 = 40 is a later time they flash together, and 2 is the GCF."))

    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    its.append(mcq("%s waters %s plants every 4 days. %s waters %s plants every 6 days. They both water today. "
                   "In how many days will they both water on the same day again?" % (nm, his, nm2, his2),
                   "12 days", ["24 days", "10 days", "2 days"],
                   lcm_e(4, 6) + " 4 × 6 = 24 days is not the first time, and 10 is 4 + 6."))

    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    its.append(mcq("%s runs one lap of a track in 3 minutes. %s runs one lap in 5 minutes. They start together at the "
                   "starting line. After how many minutes will they both be at the starting line again?" % (nm, nm2),
                   "15 minutes", ["8 minutes", "30 minutes", "1 minute"],
                   lcm_e(3, 5) + " 3 and 5 share no factor except 1, so the LCM is 3 × 5. 8 is 3 + 5."))

    nm, he, his = P.next()
    its.append(mcq("Juice boxes come in packs of 6 and granola bars come in packs of 10. %s wants the same number of "
                   "juice boxes and granola bars. What is the least number of each %s can buy?" % (nm, he),
                   "30 of each", ["60 of each", "16 of each", "2 of each"],
                   lcm_e(6, 10) + " That is 5 packs of juice and 3 packs of granola bars. 6 × 10 = 60 works, but it is not the least."))

    t = lcm(6, 9)
    assert t == 18
    its.append(mcq("Bus A leaves the station every 6 minutes. Bus B leaves every 9 minutes. Both buses leave at 8:00 a.m. "
                   "When will they next leave at the same time?",
                   "8:18 a.m.", ["8:54 a.m.", "8:15 a.m.", "8:03 a.m."],
                   lcm_e(6, 9) + " So they leave together again 18 minutes later, at <b>8:18 a.m.</b> "
                   "6 × 9 = 54 minutes is not the first time, and 6 + 9 = 15 is not a multiple of 6."))

    nm, he, his = P.next()
    its.append(mcq("%s has 36 pens and 48 stickers. %s wants to make the greatest number of identical gift bags with "
                   "nothing left over. What should %s find?" % (nm, cap(he), he),
                   "The GCF of 36 and 48", ["The LCM of 36 and 48", "36 × 48", "48 − 36"],
                   "%s is splitting things into equal groups, and the number of bags must divide both 36 and 48. "
                   "That is the <b>GCF</b> (12 bags)." % cap(he)))
    assert gcd(36, 48) == 12
    its.append(mcq("A green light blinks every 8 seconds and a yellow light blinks every 12 seconds. They blink together "
                   "now. To find when they next blink together, what should you find?",
                   "The LCM of 8 and 12", ["The GCF of 8 and 12", "8 × 12", "8 + 12"],
                   "The times repeat and must line up again, so you need a common <b>multiple</b>: the <b>LCM</b> "
                   "(24 seconds). 8 × 12 = 96 is a common multiple, but not the first."))
    nm, he, his = P.next()
    its.append(mcq("%s cuts an 18 in by 24 in sheet of paper into equal squares that are as big as possible, with none "
                   "left over. What should %s find?" % (nm, he),
                   "The GCF of 18 and 24", ["The LCM of 18 and 24", "18 × 24", "24 − 18"],
                   "The side of each square must divide both 18 and 24, and it must be as big as possible. "
                   "That is the <b>GCF</b> (6 in)."))
    assert gcd(18, 24) == 6
    nm, he, his = P.next()
    its.append(mcq("Hot dogs come in packs of 10 and buns come in packs of 8. %s wants the same number of hot dogs "
                   "and buns. To find the least number of each, what should %s find?" % (nm, he),
                   "The LCM of 10 and 8", ["The GCF of 10 and 8", "10 + 8", "10 − 8"],
                   "The totals are multiples of 10 and of 8, and they must match. That is the <b>LCM</b> (40)."))
    assert lcm(10, 8) == 40

    nm, he, his = P.next()
    its.append(mcq("%s has 30 markers and 45 crayons. %s makes the greatest number of identical art kits with nothing "
                   "left over. How many crayons are in each kit?" % (nm, cap(he)),
                   "3 crayons", ["15 crayons", "2 crayons", "9 crayons"],
                   "The GCF of 30 and 45 is 15, so there are 15 kits. 45 ÷ 15 = <b>3 crayons</b> in each kit "
                   "(and 30 ÷ 15 = 2 markers). 15 is the number of kits, not crayons."))
    assert gcd(30, 45) == 15

    nm, he, his = P.next()
    its.append(mcq("Star stickers come in sheets of 9 and heart stickers come in sheets of 12. %s wants the same number "
                   "of star and heart stickers, as few as possible. How many sheets of star stickers should %s buy?"
                   % (nm, he),
                   "4 sheets", ["36 sheets", "3 sheets", "12 sheets"],
                   lcm_e(9, 12) + " %s needs 36 star stickers: 36 ÷ 9 = <b>4 sheets</b>. 3 sheets is the number of "
                   "heart sticker sheets (36 ÷ 12)." % cap(he)))
    assert lcm(9, 12) == 36

    its.append(mcq("A class has 24 boys and 40 girls. They form 8 teams, and each team has the same number of boys and "
                   "the same number of girls. Which expression shows all the students?",
                   "8 × (3 + 5)", ["8 × (24 + 40)", "4 × (6 + 10)", "8 × 3 + 5"],
                   "Each team has 24 ÷ 8 = 3 boys and 40 ÷ 8 = 5 girls, so 24 + 40 = <b>8 × (3 + 5)</b> = 64. "
                   "4 × (6 + 10) is also 64, but it shows 4 teams, not 8."))
    assert 8 * (3 + 5) == 64 and gcd(24, 40) == 8

    nm, he, his = P.next()
    its.append(mcq("A florist has 45 roses and 60 tulips. %s makes the greatest number of identical bouquets with "
                   "nothing left over. How many flowers are in each bouquet?" % cap(he),
                   "7 flowers", ["15 flowers", "12 flowers", "21 flowers"],
                   "The GCF of 45 and 60 is 15, so there are 15 bouquets. Each has 45 ÷ 15 = 3 roses and "
                   "60 ÷ 15 = 4 tulips: 3 + 4 = <b>7 flowers</b>. 21 comes from using 5 bouquets, which is not the greatest."))
    assert gcd(45, 60) == 15 and 45 // 5 + 60 // 5 == 21
    assert len(its) == 20, len(its)
    return {"title": "Word problems: GCF or LCM?", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The greatest common factor (GCF)</h2>"
        "<p>A <b>common factor</b> divides both numbers. The <b>greatest common factor</b> is the biggest one. "
        "List the factors of each number, circle the ones in both lists, and pick the greatest.</p>"
        "<figure class='sn-fig'>" + factor_rows_svg(24, 36) +
        "<figcaption>The common factors of 24 and 36 are 1, 2, 3, 4, 6 and 12. The GCF is 12.</figcaption></figure>"
        + ex("Example", "Find the GCF of 18 and 45.",
             "Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 45: 1, 3, 5, 9, 15, 45. Common factors: 1, 3, 9.",
             "9")
        + "<h2>The least common multiple (LCM)</h2>"
        "<p>A <b>common multiple</b> is in the skip-counting list of both numbers. The <b>least common multiple</b> "
        "is the first one. Count by the bigger number and stop at the first multiple of the smaller number.</p>"
        "<figure class='sn-fig'>" + multiples_svg(6, 8, 48) +
        "<figcaption>Multiples of 6 and of 8. They meet at 24 and again at 48. The LCM is 24, not 6 × 8 = 48.</figcaption></figure>"
        + ex("Example", "Find the LCM of 9 and 12.",
             "Count by 12: 12, 24, 36. 12 and 24 are not multiples of 9, but 36 = 9 × 4.", "36")
        + "<h2>A shortcut: prime factorization</h2>"
        "<p>Split a number into factors until every branch ends in a prime. For the GCF, multiply the primes the "
        "two numbers <b>share</b>. For the LCM, use each prime the most times it appears in either number.</p>"
        "<figure class='sn-fig'>" + tree_svg(36) +
        "<figcaption>36 = 6 × 6 = 2 × 2 × 3 × 3.</figcaption></figure>"
        + ex("Example", "24 = 2 × 2 × 2 × 3 and 36 = 2 × 2 × 3 × 3. Find the GCF.",
             "Shared primes: 2, 2 and 3. Multiply them: 2 × 2 × 3 = 12.", "12")
        + "<h2>Factor out the GCF</h2>"
        "<p>The distributive property lets you write a sum as a product. Divide both numbers by their GCF and "
        "put what is left in parentheses. The two numbers inside should have no common factor except 1.</p>"
        "<figure class='sn-fig'>" + area_svg(4, 9, 2, unit=20, show=True) +
        "<figcaption>36 + 8 = 4 × 9 + 4 × 2 = 4 × (9 + 2).</figcaption></figure>"
        + ex("Example", "Rewrite 36 + 8 as a product using the GCF.",
             "The GCF of 36 and 8 is 4. 36 = 4 × 9 and 8 = 4 × 2. 9 and 2 have no common factor.",
             "36 + 8 = 4 × (9 + 2)")
        + "<h2>GCF or LCM?</h2>"
        + table(["The problem asks…", "Use", "Example"], [
            ["The greatest number of identical groups, kits or teams", "GCF", "24 pencils and 36 erasers make 12 kits"],
            ["The biggest equal pieces or squares with nothing left over", "GCF", "48 cm and 60 cm ribbons: 12 cm pieces"],
            ["When two repeating events happen together again", "LCM", "Buses every 6 and 9 minutes: 18 minutes"],
            ["The least number to buy so two pack sizes match", "LCM", "Packs of 12 and 8: 24 of each"],
        ])
        + "<p>Check your answer: a GCF is never bigger than the smaller number, and an LCM is never smaller than "
        "the bigger number.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Stopping at any common factor: GCF of 30 and 45 is 5", "Find the greatest one: 15"],
            ["Multiplying for the LCM: LCM of 6 and 8 is 48", "48 is a common multiple, but 24 comes first"],
            ["Mixing up GCF and LCM", "Groups and pieces: GCF. Repeating and matching: LCM"],
            ["Thinking the GCF can’t be one of the numbers", "GCF of 16 and 48 is 16, because 16 × 3 = 48"],
            ["Factoring out a smaller factor: 36 + 8 = 2 × (18 + 4)", "18 and 4 still share 2. Use the GCF: 4 × (9 + 2)"],
            ["Dividing only one number: 36 + 8 = 4 × (9 + 8)", "Divide both numbers by the GCF"],
        ])
    )


FAQ = [
    {"q": "How do you find the GCF of two numbers?",
     "a": "List the factors of each number and pick the greatest one that is in both lists. For 24 and 36, the common factors are 1, 2, 3, 4, 6 and 12, so the GCF is 12."},
    {"q": "How do you find the LCM of two numbers?",
     "a": "Count by the bigger number until you reach a multiple of the smaller number. For 6 and 8, count 8, 16, 24; 24 is a multiple of 6, so the LCM is 24."},
    {"q": "How do you know whether to use GCF or LCM in a word problem?",
     "a": "Use the GCF when you split things into the greatest number of equal groups or the biggest equal pieces. Use the LCM when events repeat and line up again, or when you buy packs so two amounts match."},
    {"q": "How do you use the distributive property with the GCF?",
     "a": "Divide both numbers by their GCF and write the GCF times the sum of what is left. For example, 36 + 8 = 4 × (9 + 2), because the GCF of 36 and 8 is 4."},
]


def gen():
    rnd = random.Random(606)
    P = People(rnd)
    sets = [set_gcf(P), set_lcm(P), set_primes(P), set_dist(P), set_words(P)]
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
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "gcf-and-lcm", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Greatest Common Factor and Least Common Multiple",
        "seo_title": "Grade 6 GCF and LCM Worksheets: Greatest Common Factor, Least Common Multiple, Distributive Property",
        "short_title": "GCF and LCM",
        "domain": "The Number System",
        "standard_code": "6.NS.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/B/4/",
        "standard_text": "Find the greatest common factor of two whole numbers less than or equal to 100 and the least common multiple of two whole numbers less than or equal to 12. Use the distributive property to express a sum of two whole numbers 1–100 with a common factor as a multiple of a sum of two whole numbers with no common factor. For example, express 36 + 8 as 4 (9 + 2).",
        "meta_desc": "Free Grade 6 GCF and LCM worksheets: find the greatest common factor and least common multiple, use prime factorization and factor trees, factor out the GCF with the distributive property, and solve GCF or LCM word problems. 100 practice questions with an answer key.",
        "key_big": "The GCF is the biggest number that divides both. The LCM is the first number both divide into.",
        "key_sub": "For 6 and 8: the GCF is 2 and the LCM is 24, not 6 × 8 = 48. Use the GCF for equal groups and pieces, the LCM for things that repeat and line up. Factoring out the GCF: 36 + 8 = 4 × (9 + 2).",
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
