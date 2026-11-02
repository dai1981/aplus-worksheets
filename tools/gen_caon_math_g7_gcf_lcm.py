# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: GCF and LCM (Ontario Mathematics Curriculum 2020, Grade 7: B2.6)
  python3 tools/gen_caon_math_g7_gcf_lcm.py
Factors and common factors, the greatest common factor of whole numbers up to 144 (lists and factor trees),
multiples and common multiples, the lowest common multiple of two or three numbers, and word problems
(hot dogs and buns, arranging chairs, buses leaving together).
Every factor, multiple, GCF and LCM is checked in code.
Wrong answers come from real student mistakes: a common factor that is not the greatest, a factor of only
one number, swapping GCF and LCM, multiplying the numbers for the LCM, using only two of three numbers,
using each shared prime only once, mixing up factors and multiples, adding the numbers, and answering
with the wrong quantity (packs instead of items, groups instead of items per group).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, os, random, re
from math import gcd, prod

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ math
def n(x):
    """Ontario style: 4 digits with no separator, 5 or more digits grouped with a no-break space."""
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


def lcm_primes(*xs):
    out = []
    for p in sorted(set(q for x in xs for q in primes_of(x))):
        out += [p] * max(primes_of(x).count(p) for x in xs)
    return out


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


def factor_rows_svg(a, b):
    """Lesson: the factors of a and b in two rows, the common ones circled, the GCF in red."""
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
            if d in fa and d in fb:
                s.append("<circle cx='%.1f' cy='%d' r='15' fill='%s' stroke='%s' stroke-width='2'/>"
                         % (x, y - 6, "#f6d5d0" if d == g else FILL, RED if d == g else GREEN))
            s.append(text(x, y, str(d), 15, col=RED if d == g else INK))
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


# ============================================================ set 1: factors and common factors
def set_factors(P):
    its = []
    for x in [36, 48, 84]:
        fs = factors(x)
        prs = [(d, x // d) for d in fs if d * d <= x]
        mid = prs[-1]
        no_mid = [d for d in fs if d not in mid]
        no_ends = fs[1:-1]
        ms = mults(x, 4 * x)[:4]
        e = ("Find the factor pairs: %s. So the factors of %d are <b>%s</b>. Check every number from 1 up to the "
             "pair that meets in the middle, and include 1 and %d." % (", ".join("%d × %d" % p for p in prs), x, lst(fs), x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, lst(fs),
                       [lst(no_mid), lst(no_ends), lst(ms)], e))

    for x, wrong, why in [(64, [8, 4, 5], "Counting 8 twice gives 8. Counting pairs gives 4. Leaving out 1 and 64 gives 5."),
                          (90, [6, 10, 4], "Counting pairs gives 6. Leaving out 1 and 90 gives 10. 4 is the number of primes in 2 × 3 × 3 × 5.")]:
        fs = factors(x)
        e = "The factors of %d are %s. That is <b>%d factors</b>. %s" % (x, lst(fs), len(fs), why)
        its.append(mcq("How many factors does %d have?" % x, len(fs), wrong, e))
    assert len(factors(64)) == 7 and len(factors(90)) == 12

    for x, right, wrong in [(126, 14, [252, 12, 16]), (144, 18, [288, 14, 21])]:
        assert x % right == 0 and all(x % w for w in wrong) and wrong[0] == 2 * x
        e = ("%d × %d = %d, so <b>%d</b> is a factor of %d. %d is a <b>multiple</b> of %d, not a factor. "
             "%d ÷ %d and %d ÷ %d have remainders."
             % (right, x // right, x, right, x, wrong[0], x, x, wrong[1], x, wrong[2]))
        its.append(mcq("Which number is a factor of %d?" % x, right, wrong, e))

    for x, bad, good in [(108, 8, [12, 18, 27]), (132, 9, [4, 12, 22])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%d ÷ %d = %d R %d, so <b>%d</b> is not a factor. %s"
             % (x, bad, x // bad, x % bad, bad, " ".join("%d × %d = %d." % (g, x // g, x) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))

    for a, b in [(24, 40), (36, 60), (42, 56), (45, 75)]:
        c = cfs(a, b)
        small = factors(min(a, b))
        e = ("Factors of %d: %s. Factors of %d: %s. The numbers in <b>both</b> lists are <b>%s</b>. "
             "Keep 1 and the greatest one." % (a, lst(factors(a)), b, lst(factors(b)), lst(c)))
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c),
                       [lst(c[:-1]), lst(small), lst(c[1:])], e))

    for a, b, right, wrong in [(54, 72, 9, [4, 27, 216]), (70, 98, 14, [5, 49, 490])]:
        assert a % right == 0 and b % right == 0
        assert (a % wrong[0] == 0) != (b % wrong[0] == 0) and (a % wrong[1] == 0) != (b % wrong[1] == 0)
        assert wrong[2] == L(a, b)
        oa = a if a % wrong[0] == 0 else b
        ob = a if a % wrong[1] == 0 else b
        e = ("%d × %d = %d and %d × %d = %d, so <b>%d</b> is a common factor. %d is a factor of %d only, "
             "%d is a factor of %d only, and %d is a common <b>multiple</b>."
             % (right, a // right, a, right, b // right, b, right, wrong[0], oa, wrong[1], ob, wrong[2]))
        its.append(mcq("Which number is a common factor of %d and %d?" % (a, b), right, wrong, e))

    for a, b, bad, good in [(48, 80, 6, [4, 8, 16]), (60, 90, 4, [5, 6, 15])]:
        assert all(a % g == 0 and b % g == 0 for g in good) and (a % bad == 0) != (b % bad == 0)
        only = a if a % bad == 0 else b
        other = b if only == a else a
        e = ("%d is a factor of %d, but %d ÷ %d = %d R %d, so <b>%d</b> is not a common factor. "
             "%d, %d and %d divide both numbers." % ((bad, only, other, bad, other // bad, other % bad, bad) + tuple(good)))
        its.append(mcq("Which number is <b>not</b> a common factor of %d and %d?" % (a, b), bad, good, e))

    prs = [(d, 120 // d) for d in factors(120) if d * d <= 120]
    shown = ", ".join("%d × %s" % (p[0], "?" if p[0] == 8 else str(p[1])) for p in prs)
    assert (8, 15) in prs
    its.append(mcq("These are the factor pairs of 120: %s. What is the missing number?" % shown, 15, [16, 14, 12],
                   "8 × 15 = 120, so the missing number is <b>15</b>. 8 × 14 = 112 and 8 × 16 = 128. "
                   "12 is already in the pair 10 × 12."))

    nm, he, his = P.next()
    assert 28 % 7 == 0 and 63 % 7 == 0
    its.append(mcq("%s says 7 is a common factor of 28 and 63. Is %s right?" % (nm, he),
                   "Yes. 28 = 7 × 4 and 63 = 7 × 9", ["No. 7 divides 63 only", "No. 63 is odd", "No. Only 1 is common"],
                   "7 divides both numbers with no remainder: 28 = 7 × 4 and 63 = 7 × 9. So <b>7 is a common factor</b>. "
                   "A number can be a common factor of an even and an odd number."))
    nm, he, his = P.next()
    assert 96 % 32 == 0 and 56 % 32
    its.append(mcq("%s says 32 is a common factor of 56 and 96, because 32 is a factor of 96. Is %s right?" % (nm, he),
                   "No. 32 is not a factor of 56", ["Yes. 32 divides 96", "Yes. 32 is less than 56", "No. 32 is a multiple of 56"],
                   "A common factor must divide <b>both</b> numbers. 96 = 32 × 3, but 56 ÷ 32 = 1 R 24. "
                   "So <b>32 is not a common factor</b>. The common factors of 56 and 96 are %s." % lst(cfs(56, 96))))
    assert len(its) == 20, len(its)
    return {"title": "Factors and common factors", "items": its}


# ============================================================ set 2: GCF
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
    for a, b in [(32, 48), (45, 60), (56, 84), (72, 96), (17, 51), (25, 36), (108, 144), (84, 126)]:
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
        cands += [n(a * b), a + b]
        e = gcf_e(a, b)
        if g == 1:
            e += " %d and %d share no factor except 1, so their GCF is 1." % (a, b)
        elif g == min(a, b):
            e += " %d divides %d (%d × %d = %d), so the smaller number is the GCF." % (a, b, a, b // a, b)
        elif len(c) > 1 and c[-2] > 1:
            e += " %d is a common factor too, but not the greatest. %s is the LCM." % (c[-2], n(L(a, b)))
        its.append(mcq("What is the greatest common factor (GCF) of %d and %d?" % (a, b), g, cands, e))

    for a, b in [(60, 84), (72, 108), (90, 126), (48, 120)]:
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
        e += " %s is the LCM." % n(L(a, b))
        its.append(mcq(fig(tree_pair_svg(a, b)) + "Use the factor trees. What is the GCF of %d and %d?" % (a, b),
                       g, [once, n(L(a, b)), c[-2], c[-3]], e))

    for a, b in [(80, 112), (98, 140)]:
        pa, pb = primes_of(a), primes_of(b)
        sh = shared_primes(a, b)
        g = prod(sh)
        assert g == gcd(a, b)
        once = prod(sorted(set(sh)))
        allp = prod(sorted(set(pa + pb)))
        e = ("Circle the primes in <b>both</b> lists: %s. Multiply them: %s = <b>%d</b>. "
             "Use a shared prime as many times as it appears in both lists." % (times(sh), times(sh), g))
        e += " %s is the LCM, and %d uses every prime, not only the shared ones." % (n(L(a, b)), allp)
        its.append(mcq("%d = %s and %d = %s. What is the GCF of %d and %d?" % (a, times(pa), b, times(pb), a, b),
                       g, [once, n(L(a, b)), allp, cfs(a, b)[-2]], e))

    for xs in [(40, 60, 72), (48, 72, 80)]:
        g = G(*xs)
        g12 = gcd(xs[0], xs[1])
        c = cfs(*xs)
        assert g12 != g
        smaller = [d for d in cfs(*xs) if d < g]
        e = ("Common factors of %d, %d and %d: %s. The GCF is <b>%d</b>. The GCF of %d and %d alone is %d, "
             "but %d is not a factor of %d. Check all three numbers." % (xs + (lst(c), g, xs[0], xs[1], g12, g12, xs[2])))
        its.append(mcq("What is the GCF of %d, %d and %d?" % xs, g, [g12, smaller[-1], n(L(*xs))], e))

    nm, he, his = P.next()
    assert gcd(36, 90) == 18
    its.append(mcq("%s says the GCF of 36 and 90 is 9, because 9 is a factor of both. Is %s right?" % (nm, he),
                   "No. The GCF is 18", ["Yes. 9 divides both", "No. The GCF is 180", "No. The GCF is 36"],
                   "9 is a common factor, but not the greatest. 18 × 2 = 36 and 18 × 5 = 90, so the GCF is <b>18</b>. "
                   "180 is the LCM, and 36 is not a factor of 90."))
    nm, he, his = P.next()
    assert gcd(27, 108) == 27
    its.append(mcq("%s says the GCF of 27 and 108 is 27. Is %s right?" % (nm, he),
                   "Yes. 27 × 4 = 108", ["No. The GCF is 9", "No. It can’t be 27", "No. The GCF is 3"],
                   "27 × 4 = 108, so 27 is a factor of both numbers, and no factor of 27 is bigger than 27. "
                   "The GCF <b>can</b> be the smaller number."))
    nm, he, his = P.next()
    assert gcd(35, 64) == 1
    its.append(mcq("%s says 35 and 64 have no common factor, so they have no GCF. Is %s right?" % (nm, he),
                   "No. Their GCF is 1", ["Yes. They have no GCF", "No. Their GCF is 5", "No. Their GCF is 7"],
                   "1 is a factor of every whole number, so 1 is always a common factor. 35 = 5 × 7 and "
                   "64 = 2 × 2 × 2 × 2 × 2 × 2 share no prime, so the GCF is <b>1</b>."))

    good, bad = "36 and 60", ["24 and 48", "3 and 4", "30 and 42"]
    assert gcd(36, 60) == 12 and [gcd(24, 48), gcd(3, 4), gcd(30, 42)] == [24, 1, 6]
    its.append(mcq("Which pair of numbers has a GCF of 12?", good, bad,
                   "36 = 12 × 3 and 60 = 12 × 5, and 3 and 5 share no factor, so the GCF of 36 and 60 is <b>12</b>. "
                   "The GCF of 24 and 48 is 24, of 3 and 4 is 1 (12 is their LCM), and of 30 and 42 is 6."))
    assert len(its) == 20, len(its)
    return {"title": "Greatest common factor (GCF)", "items": its}


# ============================================================ set 3: multiples and common multiples
def set_multiples(P):
    its = []
    for d, wrong in [(7, [[0, 7, 14, 21, 28], [7, 17, 27, 37, 47], [1, 8, 15, 22, 29]]),
                     (12, [[0, 12, 24, 36, 48], [1, 2, 3, 4, 6], [12, 22, 32, 42, 52]])]:
        right = [d * k for k in range(1, 6)]
        assert all(w != right for w in wrong)
        e = ("Multiply %d by 1, 2, 3, 4 and 5: <b>%s</b>. The first multiple of a number is the number itself, "
             "not 0. Count by %d, not by 10, and don’t mix up multiples with factors." % (d, lst(right), d))
        its.append(mcq("Which list shows the first five multiples of %d?" % d, lst(right), [lst(w) for w in wrong], e))

    for d, right, wrong, hint in [(9, 117, [3, 89, 129], "Ending in 9 does not make a number a multiple of 9."),
                                  (12, 132, [6, 122, 112], "Ending in 2 does not make a number a multiple of 12."),
                                  (14, 98, [7, 104, 124], "Ending in 4 does not make a number a multiple of 14.")]:
        assert right % d == 0 and all(w % d for w in wrong) and d % wrong[0] == 0
        e = ("%d × %d = %d, so <b>%d</b> is a multiple of %d. %d is a <b>factor</b> of %d, not a multiple. "
             "%d ÷ %d and %d ÷ %d have remainders. %s"
             % (d, right // d, right, right, d, wrong[0], d, wrong[1], d, wrong[2], d, hint))
        its.append(mcq("Which number is a multiple of %d?" % d, right, wrong, e))

    assert 108 % 8 and all(x % 8 == 0 for x in (96, 120, 144))
    its.append(mcq("Which number is <b>not</b> a multiple of 8?", 108, [96, 120, 144],
                   "108 ÷ 8 = 13 R 4, so <b>108</b> is not a multiple of 8. 96 = 8 × 12, 120 = 8 × 15 and 144 = 8 × 18."))

    its.append(mcq("Which statement is true?", "48 is a multiple of 24",
                   ["48 is a factor of 24", "24 is a multiple of 48", "8 is a multiple of 24"],
                   "24 × 2 = 48, so <b>48 is a multiple of 24</b>, and 24 is a factor of 48. "
                   "A factor is never bigger than the number; a multiple is never smaller."))

    for a, b, top, wrong, note in [
            (4, 6, 36, [[24], [12], [4, 8, 12]], " Not only 4 × 6 = 24: 12 and 36 are in both rows too."),
            (6, 9, 54, [[54], [18], [6, 12, 18]], " Not only 6 × 9 = 54: 18 and 36 are in both rows too."),
            (8, 12, 48, [[24], [8, 16, 24], [12, 24, 36]], " 36 is a multiple of 12 only, and 16 is a multiple of 8 only."),
            (5, 8, 40, [[5, 8], [10, 20, 30], [8, 16, 24, 32]], " 5 and 8 share no factor except 1, so their first common multiple is 5 × 8.")]:
        com = [m for m in range(1, top + 1) if m % a == 0 and m % b == 0]
        assert all(w != com for w in wrong) and all(m <= top for w in wrong for m in w)
        e = ("Look for numbers in <b>both</b> rows. Multiples of %d: %s. Multiples of %d: %s. "
             "The %s <b>%s</b>.%s" % (a, lst(mults(a, top)), b, lst(mults(b, top)),
                                     "common multiples shown are" if len(com) > 1 else "only common multiple shown is", lst(com), note))
        its.append(mcq(fig(multiples_svg(a, b, top)) + "Which numbers in the picture are common multiples of %d and %d?"
                       % (a, b), lst(com), [lst(w) for w in wrong], e))

    m15 = [m for m in range(41, 100) if m % 15 == 0]
    assert m15 == [45, 60, 75, 90]
    its.append(mcq("Which list shows all the multiples of 15 between 40 and 100?", lst(m15),
                   ["45, 60, 75", "30, 45, 60, 75, 90", "50, 60, 70, 80, 90"],
                   "Count by 15: 15, 30, 45, 60, 75, 90, 105. The ones between 40 and 100 are <b>45, 60, 75, 90</b>. "
                   "30 is less than 40, and counting by 10 gives multiples of 10, not 15."))

    for a, b in [(6, 8), (9, 12), (10, 15)]:
        l = L(a, b)
        right = [l, 2 * l, 3 * l]
        byprod = [a * b, 2 * a * b, 3 * a * b]
        mixed = [a, b, l]
        big = mults(b, 3 * b)
        e = ("The LCM of %d and %d is %d. The common multiples are the multiples of the LCM: <b>%s</b>. "
             "Counting by %d × %d = %d skips %d." % (a, b, l, lst(right), a, b, a * b, l))
        its.append(mcq("Which list shows the first three common multiples of %d and %d?" % (a, b), lst(right),
                       [lst(byprod), lst(mixed), lst(big)], e))

    for a, b, right, wrong in [(6, 15, 90, [21, 45, 36]), (8, 12, 72, [20, 64, 36]), (9, 15, 90, [24, 60, 81])]:
        assert right % a == 0 and right % b == 0 and wrong[0] == a + b
        assert all(w % a or w % b for w in wrong)
        e = ("%d = %d × %d and %d = %d × %d, so <b>%d</b> is a common multiple. %d is %d + %d. "
             "%d and %d are each a multiple of only one of the numbers."
             % (right, a, right // a, right, b, right // b, right, wrong[0], a, b, wrong[1], wrong[2]))
        its.append(mcq("Which number is a common multiple of %d and %d?" % (a, b), right, wrong, e))

    assert 40 % 6 and all(x % 6 == 0 and x % 10 == 0 for x in (30, 60, 120))
    its.append(mcq("Which number is <b>not</b> a common multiple of 6 and 10?", 40, [30, 60, 120],
                   "40 is a multiple of 10, but 40 ÷ 6 = 6 R 4, so <b>40</b> is not a multiple of 6. "
                   "The LCM of 6 and 10 is 30, and 30, 60 and 120 are all multiples of 30."))

    nm, he, his = P.next()
    assert L(4, 6) == 12
    its.append(mcq("%s says the common multiples of 4 and 6 are 24, 48, 72, …, because 4 × 6 = 24. Is %s right?" % (nm, he),
                   "No. 12, 36, … are missing", ["Yes. 4 × 6 = 24", "No. They are 2, 4, 6, …", "No. They are 10, 20, 30, …"],
                   "Multiples of 6: 6, 12, 18, 24. 12 is also a multiple of 4. So the common multiples are 12, 24, 36, 48, … "
                   "Counting by 4 × 6 = 24 <b>misses 12, 36, …</b>"))
    assert len(its) == 20, len(its)
    return {"title": "Multiples and common multiples", "items": its}


# ============================================================ set 4: LCM of two or three numbers
def lcm_e(a, b):
    l = L(a, b)
    lo, hi = sorted((a, b))
    return ("Count by %d: %s. The first one that is also a multiple of %d is <b>%d</b>."
            % (hi, lst(mults(hi, l)), lo, l))


def set_lcm(P):
    its = []
    for a, b in [(6, 8), (9, 12), (10, 15), (12, 18), (8, 14), (7, 9), (15, 20), (16, 24)]:
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
            e += " %d × %d = %d is a common multiple, but not the lowest. %d is the GCF." % (a, b, a * b, g)
        its.append(mcq("What is the lowest common multiple (LCM) of %d and %d?" % (a, b), l, cands, e))

    for a, b in [(18, 30), (20, 24)]:
        pa, pb = primes_of(a), primes_of(b)
        need = lcm_primes(a, b)
        l = prod(need)
        assert l == L(a, b)
        once = prod(sorted(set(pa + pb)))
        e = ("Use each prime the greatest number of times it appears in either list: %s = <b>%d</b>. "
             "%d × %d = %d uses the shared primes twice." % (times(need), l, a, b, a * b))
        its.append(mcq("%d = %s and %d = %s. What is the LCM of %d and %d?" % (a, times(pa), b, times(pb), a, b),
                       l, [a * b, once, gcd(a, b), 2 * l], e))
    for xs in [(2, 3, 4), (3, 4, 6), (4, 5, 6), (6, 8, 12), (3, 5, 9), (4, 6, 10)]:
        l = L(*xs)
        p3 = prod(xs)
        l12 = L(xs[0], xs[1])
        cands = []
        if p3 != l:
            cands.append(p3)
        if l12 != l:
            cands.append(l12)
        cands += [sum(xs), 2 * l, max(xs)]
        e = ("Count by the biggest number, %d: %s. The first one that %d and %d also divide is <b>%d</b>."
             % (max(xs), lst(mults(max(xs), l)), sorted(xs)[0], sorted(xs)[1], l))
        if p3 != l:
            e += " %s = %d is a common multiple, but not the lowest." % (times(xs), p3)
        if l12 != l:
            e += " %d is the LCM of %d and %d only." % (l12, xs[0], xs[1])
        its.append(mcq("What is the LCM of %d, %d and %d?" % xs, l, cands, e))

    nm, he, his = P.next()
    assert L(4, 6, 8) == 24
    its.append(mcq("%s says the LCM of 4, 6 and 8 is 192, because 4 × 6 × 8 = 192. Is %s right?" % (nm, he),
                   "No. The LCM is 24", ["Yes. 4 × 6 × 8 = 192", "No. The LCM is 2", "No. The LCM is 48"],
                   "Count by 8: 8, 16, 24. 24 ÷ 4 = 6 and 24 ÷ 6 = 4, so the LCM is <b>24</b>. "
                   "192 is a common multiple, but not the lowest. 2 is the GCF, and 48 is the LCM × 2."))
    nm, he, his = P.next()
    assert gcd(6, 9) == 3 and L(6, 9) == 18
    its.append(mcq("%s says the LCM of 6 and 9 is 3. Is %s right?" % (nm, he),
                   "No. 3 is the GCF. The LCM is 18", ["Yes. 3 divides both", "No. The LCM is 54", "No. The LCM is 15"],
                   "3 is the greatest common <b>factor</b>. A multiple can’t be smaller than the numbers. "
                   "Count by 9: 9, 18. 18 = 6 × 3, so the LCM is <b>18</b>."))
    nm, he, his = P.next()
    assert L(5, 10, 20) == 20
    its.append(mcq("%s says the LCM of 5, 10 and 20 is 20. Is %s right?" % (nm, he),
                   "Yes. 5 and 10 divide 20", ["No. The LCM is 1000", "No. The LCM is 35", "No. The LCM is 5"],
                   "20 = 5 × 4 and 20 = 10 × 2, so 20 is a multiple of all three numbers, and no smaller multiple of 20 "
                   "exists. The LCM is <b>20</b>. When the biggest number is a multiple of the others, it is the LCM."))

    good, bad = "3, 5 and 10", ["4, 5 and 6", "3, 6 and 9", "2, 3 and 6"]
    assert L(3, 5, 10) == 30 and [L(4, 5, 6), L(3, 6, 9), L(2, 3, 6)] == [60, 18, 6]
    its.append(mcq("Which three numbers have an LCM of 30?", good, bad,
                   "30 = 3 × 10 = 5 × 6 = 10 × 3, and no smaller number is a multiple of 3, 5 and 10. So the answer is "
                   "<b>3, 5 and 10</b>. The LCM of 4, 5 and 6 is 60, of 3, 6 and 9 is 18, and of 2, 3 and 6 is 6."))
    assert len(its) == 20, len(its)
    return {"title": "Lowest common multiple (LCM) of two or three numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    nm, he, his = P.next()
    assert L(12, 8) == 24
    its.append(mcq("Hot dogs come in packs of 12 and buns come in packs of 8. %s wants the same number of hot dogs and "
                   "buns for the class barbecue. What is the least number of each %s can buy?" % (nm, he),
                   "24 of each", ["96 of each", "4 of each", "20 of each"],
                   lcm_e(8, 12) + " So %s buys 24 of each. 12 × 8 = 96 also works, but it is not the least. "
                   "4 is the GCF, and 20 is 12 + 8." % he))
    nm, he, his = P.next()
    assert L(12, 8) // 8 == 3
    its.append(mcq("Hot dogs come in packs of 12 and buns come in packs of 8. %s buys the least number of packs so that "
                   "there is a bun for every hot dog, with none left over. How many packs of buns does %s buy?" % (nm, he),
                   "3 packs", ["2 packs", "24 packs", "12 packs"],
                   "The LCM of 12 and 8 is 24, so %s needs 24 buns: 24 ÷ 8 = <b>3 packs</b>. "
                   "2 packs is the number of packs of hot dogs (24 ÷ 12)." % he))
    sz = gcd(96, 72)
    assert sz == 24
    its.append(mcq("The school has 96 blue chairs and 72 red chairs for an assembly in the gym. Each row has only one "
                   "colour, and every row has the same number of chairs. What is the greatest number of chairs in each row?",
                   "24 chairs", ["12 chairs", "8 chairs", "288 chairs"],
                   "The row size must divide both 96 and 72. Common factors: %s. The GCF is <b>24</b>. "
                   "12 and 8 also work, but they are not the greatest. 288 is the LCM." % lst(cfs(96, 72))))
    rows = 96 // 24 + 72 // 24
    assert rows == 7
    its.append(mcq("96 blue chairs and 72 red chairs are set out in rows of 24, and each row has only one colour. "
                   "How many rows are there?", "7 rows", ["24 rows", "21 rows", "168 rows"],
                   "96 ÷ 24 = 4 blue rows and 72 ÷ 24 = 3 red rows. 4 + 3 = <b>7 rows</b>. "
                   "24 is the number of chairs in each row. 21 rows would be rows of 8. 168 is the total number of chairs."))
    assert L(12, 18) == 36
    its.append(mcq("The Route 5 bus leaves the station every 12 minutes. The Route 9 bus leaves every 18 minutes. "
                   "Both buses leave at 7:00 a.m. When will they next leave at the same time?",
                   "7:36 a.m.", ["10:36 a.m.", "7:30 a.m.", "7:06 a.m."],
                   lcm_e(12, 18) + " So they leave together again 36 minutes later, at <b>7:36 a.m.</b> "
                   "12 × 18 = 216 minutes (10:36 a.m.) is not the first time. 30 is 12 + 18, and 6 is the GCF."))
    assert L(10, 15, 20) == 60 and L(10, 15) == 30
    its.append(mcq("Three city buses leave the same stop every 10, 15 and 20 minutes. All three leave at 8:00 a.m. "
                   "When will all three next leave together?", "9:00 a.m.", ["8:30 a.m.", "8:45 a.m.", "8:05 a.m."],
                   "Count by 20: 20, 40, 60. 60 is also a multiple of 10 and of 15, so the LCM is 60 minutes, and they "
                   "leave together at <b>9:00 a.m.</b> 8:30 a.m. works for the first two buses only. 45 is 10 + 15 + 20, "
                   "and 5 is the GCF."))
    nm, he, his = P.next()
    g = gcd(120, 84)
    assert g == 12 and 84 // g == 7 and L(120, 84) == 840
    its.append(mcq("For the Terry Fox Run, %s has 120 water bottles and 84 granola bars. %s packs identical snack bags "
                   "with nothing left over. What is the greatest number of bags %s can make?" % (nm, cap(he), he),
                   "12 bags", ["6 bags", "840 bags", "7 bags"],
                   "The number of bags must divide both 120 and 84. Common factors: %s. The GCF is <b>12</b>. "
                   "840 is the LCM, and 7 is the number of granola bars in each bag." % lst(cfs(120, 84))))
    assert gcd(90, 144) == 18 and L(90, 144) == 720
    its.append(mcq("A bulletin board is 90 cm by 144 cm. The class covers it with equal squares of paper, as large as "
                   "possible, with no gaps or overlaps. What is the side length of each square?",
                   "18 cm", ["9 cm", "6 cm", "720 cm"],
                   "The side must divide both 90 and 144. Common factors: %s. The GCF is <b>18 cm</b>, which gives "
                   "5 rows of 8 squares. 720 is the LCM, and it is bigger than the board." % lst(cfs(90, 144))))
    nm, he, his = P.next()
    assert gcd(105, 135) == 15 and L(105, 135) == 945
    its.append(mcq("%s has two ropes for a canoe trip, 105 cm and 135 cm long. %s cuts both into pieces of the same "
                   "length, as long as possible, with nothing left over. How long is each piece?" % (nm, cap(he)),
                   "15 cm", ["5 cm", "945 cm", "3 cm"],
                   "The length must divide both 105 and 135. Common factors: %s. The GCF is <b>15 cm</b>: "
                   "7 pieces from the first rope and 9 from the second. 945 is the LCM." % lst(cfs(105, 135))))
    assert gcd(28, 42) == 14
    its.append(mcq("The Grade 7 classes have 28 boys and 42 girls. The teachers make teams for a soccer tournament. Each "
                   "team has the same number of boys and the same number of girls, and no one is left out. "
                   "What is the greatest number of teams?", "14 teams", ["7 teams", "70 teams", "84 teams"],
                   "Find the GCF of 28 and 42. Common factors: %s. The GCF is <b>14</b>, so there are 14 teams, each with "
                   "2 boys and 3 girls. 7 teams also works, but it is not the greatest. 70 is the total number of students, "
                   "and 84 is the LCM." % lst(cfs(28, 42))))
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    assert L(40, 60) == 120
    its.append(mcq("At the skating rink, %s skates one lap every 40 seconds and %s skates one lap every 60 seconds. "
                   "They start together. After how many seconds are they both back at the start together?" % (nm, nm2),
                   "120 seconds", ["2400 seconds", "100 seconds", "20 seconds"],
                   lcm_e(40, 60) + " That is 2 minutes. 40 × 60 = 2400 is not the first time, 100 is 40 + 60, and 20 is the GCF."))
    assert L(4, 6, 9) == 36 and L(4, 6) == 12
    its.append(mcq("Three lights on a parade float flash every 4, 6 and 9 seconds. They flash together now. "
                   "In how many seconds will all three next flash together?",
                   "36 seconds", ["216 seconds", "12 seconds", "19 seconds"],
                   "Count by 9: 9, 18, 27, 36. 36 = 4 × 9 and 36 = 6 × 6, so the LCM is <b>36 seconds</b>. "
                   "4 × 6 × 9 = 216 is not the first time. 12 works for the first two lights only, and 19 is 4 + 6 + 9."))
    nm, he, his = P.next()
    assert L(12, 8, 6) == 24
    its.append(mcq("For a picnic, hot dogs come in packs of 12, buns in packs of 8 and juice boxes in packs of 6. "
                   "%s wants the same number of each, as few as possible. How many of each does %s buy?" % (nm, he),
                   "24 of each", ["576 of each", "26 of each", "2 of each"],
                   "Count by 12: 12, 24. 24 is also a multiple of 8 and of 6, so the LCM is <b>24</b>. "
                   "12 × 8 × 6 = 576 is far more than needed, 26 is 12 + 8 + 6, and 2 is the GCF."))
    nm, he, his = P.next()
    assert G(24, 36, 60) == 12 and L(24, 36, 60) == 360
    its.append(mcq("%s packs 24 granola bars, 36 apples and 60 juice boxes for a class field trip. Every bag must be "
                   "identical, with nothing left over. What is the greatest number of bags?" % nm,
                   "12 bags", ["6 bags", "4 bags", "360 bags"],
                   "Common factors of 24, 36 and 60: %s. The GCF is <b>12</b>, so each bag has 2 granola bars, 3 apples "
                   "and 5 juice boxes. 6 and 4 also work, but they are not the greatest. 360 is the LCM." % lst(cfs(24, 36, 60))))
    nm, he, his = P.next()
    assert L(4, 6) == 12
    its.append(mcq("%s has hockey practice every 4 days and swimming lessons every 6 days. Both are on March 1. "
                   "What is the next date when %s has both?" % (nm, he),
                   "March 13", ["March 25", "March 11", "March 3"],
                   "The LCM of 4 and 6 is 12, so both happen again 12 days later: March 1 + 12 days = <b>March 13</b>. "
                   "March 25 uses 4 × 6 = 24 days, March 11 uses 4 + 6 = 10 days, and March 3 uses the GCF, 2."))
    nm, he, his = P.next()
    assert gcd(45, 75) == 15 and 75 // 15 == 5 and 45 // 15 == 3 and gcd(45, 75) != 3
    its.append(mcq("%s makes the greatest number of identical gift bags from 45 pencils and 75 erasers, with nothing left "
                   "over. How many erasers are in each bag?" % nm,
                   "5 erasers", ["15 erasers", "3 erasers", "25 erasers"],
                   "The GCF of 45 and 75 is 15, so there are 15 bags. 75 ÷ 15 = <b>5 erasers</b> in each bag "
                   "(and 45 ÷ 15 = 3 pencils). 15 is the number of bags. 25 would come from using only 3 bags."))
    nm, he, his = P.next()
    assert L(15, 20) == 60
    its.append(mcq("Star stickers come in sheets of 15 and heart stickers come in sheets of 20. %s wants the same number "
                   "of star and heart stickers, as few as possible. How many of each does %s get?" % (nm, he),
                   "60 of each", ["300 of each", "5 of each", "35 of each"],
                   lcm_e(15, 20) + " That is 4 sheets of stars and 3 sheets of hearts. 15 × 20 = 300 is not the least, "
                   "5 is the GCF, and 35 is 15 + 20."))
    its.append(mcq("A teacher sets out 72 chairs and 54 desks in rows. Every row has the same number of items, and each "
                   "row has only chairs or only desks. To find the most items in each row, what should you find?",
                   "The GCF of 72 and 54", ["The LCM of 72 and 54", "72 × 54", "72 + 54"],
                   "The row size must divide both numbers, and it must be as big as possible. That is the <b>GCF</b> (18)."))
    assert gcd(72, 54) == 18
    its.append(mcq("One bus leaves every 14 minutes and another leaves every 21 minutes. To find when they next leave "
                   "together, what should you find?",
                   "The LCM of 14 and 21", ["The GCF of 14 and 21", "14 × 21", "14 + 21"],
                   "The times repeat and must line up again, so you need a common <b>multiple</b>: the <b>LCM</b> "
                   "(42 minutes). 14 × 21 = 294 is a common multiple, but not the first."))
    assert L(14, 21) == 42
    nm, he, his = P.next()
    assert L(10, 8) == 40
    its.append(mcq("Hot dogs come in packs of 10 and buns in packs of 8. %s says %s must buy 80 of each so that every hot "
                   "dog has a bun. Is %s right?" % (nm, he, he),
                   "No. 40 of each is enough", ["Yes. 10 × 8 = 80", "No. 18 of each is enough", "No. 2 of each is enough"],
                   lcm_e(8, 10) + " So 4 packs of hot dogs and 5 packs of buns give <b>40 of each</b>. 80 also works, but it "
                   "is not the least. 18 is 10 + 8, and 2 is the GCF."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: GCF or LCM?", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The greatest common factor (GCF)</h2>"
        "<p>A <b>common factor</b> divides two or more numbers with no remainder. The <b>greatest common factor</b> "
        "is the biggest one. List the factors of each number, circle the ones in every list, and pick the greatest.</p>"
        "<figure class='sn-fig'>" + factor_rows_svg(36, 60) +
        "<figcaption>The common factors of 36 and 60 are 1, 2, 3, 4, 6 and 12. The GCF is 12.</figcaption></figure>"
        + ex("Example", "Find the GCF of 54 and 90.",
             "Factors of 54: 1, 2, 3, 6, 9, 18, 27, 54. Factors of 90: 1, 2, 3, 5, 6, 9, 10, 15, 18, 30, 45, 90. "
             "Common factors: 1, 2, 3, 6, 9, 18.", "18")
        + "<h2>The GCF with factor trees</h2>"
        "<p>For bigger numbers, split each number into primes with a factor tree. The GCF is the product of the "
        "primes that the numbers <b>share</b>. Use a shared prime as many times as it appears in both lists.</p>"
        "<figure class='sn-fig'>" + tree_pair_svg(72, 120) +
        "<figcaption>72 = 2 × 2 × 2 × 3 × 3 and 120 = 2 × 2 × 2 × 3 × 5. They share 2 × 2 × 2 × 3, so the GCF is 24.</figcaption></figure>"
        + ex("Example", "Find the GCF of 72 and 120.",
             "Shared primes: 2, 2, 2 and 3. Multiply them: 2 × 2 × 2 × 3 = 24. Check: 72 = 24 × 3 and 120 = 24 × 5.", "24")
        + "<h2>The lowest common multiple (LCM)</h2>"
        "<p>A <b>common multiple</b> is in the skip-counting list of every number. The <b>lowest common multiple</b> "
        "is the first one. Count by the biggest number and stop at the first number the others divide into.</p>"
        "<figure class='sn-fig'>" + multiples_svg(6, 8, 48, show=True) +
        "<figcaption>Multiples of 6 and of 8. They meet at 24 and again at 48. The LCM is 24, not 6 × 8 = 48.</figcaption></figure>"
        + ex("Example", "Find the LCM of 4, 6 and 10.",
             "Count by 10: 10, 20, 30, 40, 50, 60. 20 is not a multiple of 6, 30 is not a multiple of 4, "
             "but 60 = 4 × 15 = 6 × 10.", "60")
        + "<p>With prime factorizations, use each prime the greatest number of times it appears in any one number. "
        "12 = 2 × 2 × 3 and 18 = 2 × 3 × 3, so the LCM is 2 × 2 × 3 × 3 = 36.</p>"
        "<h2>GCF or LCM?</h2>"
        + table(["The problem asks…", "Use", "Example"], [
            ["The greatest number of identical groups, bags or teams", "GCF", "120 water bottles and 84 granola bars make 12 bags"],
            ["The biggest equal rows, pieces or squares with nothing left over", "GCF", "96 and 72 chairs: rows of 24"],
            ["When repeating events happen together again", "LCM", "Buses every 12 and 18 minutes: 36 minutes"],
            ["The least number to buy so pack sizes match", "LCM", "Hot dogs in 12s, buns in 8s: 24 of each"],
        ])
        + "<p>Check your answer: a GCF is never bigger than the smallest number, and an LCM is never smaller than "
        "the biggest number.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Stopping at any common factor: GCF of 36 and 90 is 9", "Find the greatest one: 18"],
            ["Multiplying for the LCM: LCM of 6 and 8 is 48", "48 is a common multiple, but 24 comes first"],
            ["Multiplying three numbers: LCM of 4, 6 and 8 is 192", "Count by 8: 8, 16, 24. The LCM is 24"],
            ["Mixing up GCF and LCM", "Groups, rows and pieces: GCF. Repeating and matching: LCM"],
            ["Using only two of three numbers", "Check that the answer works for every number"],
            ["Using a shared prime only once", "72 and 120 share 2 × 2 × 2 × 3, so the GCF is 24, not 6"],
        ])
    )


FAQ = [
    {"q": "How do you find the GCF of two numbers?",
     "a": "List the factors of each number and pick the greatest one that is in both lists, or multiply the prime factors the numbers share. For 72 and 120, the GCF is 2 × 2 × 2 × 3 = 24."},
    {"q": "How do you find the LCM of three numbers?",
     "a": "Count by the biggest number until you reach a number the other two also divide. For 4, 6 and 10, count 10, 20, 30, 40, 50, 60; 60 is a multiple of 4 and 6, so the LCM is 60."},
    {"q": "How do you know whether to use GCF or LCM in a word problem?",
     "a": "Use the GCF when you split things into the greatest number of identical groups or the biggest equal rows or pieces. Use the LCM when events repeat and line up again, or when you buy packs so two amounts match, like hot dogs and buns."},
    {"q": "Is GCF and LCM in the Ontario Grade 7 math curriculum?",
     "a": "Yes. Expectation B2.6 of the Ontario Grade 7 math curriculum asks students to find the greatest common factor of whole numbers up to 144 and the lowest common multiple of two or three whole numbers. LCM in Ontario stands for lowest common multiple, which is the same as least common multiple."},
]


def gen():
    rnd = random.Random(47807)
    P = People(rnd)
    sets = [set_factors(P), set_gcf(P), set_multiples(P), set_lcm(P), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "gcf-and-lcm", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Greatest Common Factor and Lowest Common Multiple",
        "seo_title": "Grade 7 GCF and LCM Worksheets: Greatest Common Factor and Lowest Common Multiple (Free, Answer Key)",
        "short_title": "GCF and LCM",
        "domain": "Number",
        "standard_code": "Grade 7: B2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine the greatest common factor of whole numbers up to 144 and the lowest common multiple of two or three whole numbers, using a variety of tools and strategies",
        "meta_desc": "Free Grade 7 math worksheets for the Ontario curriculum: factors and common factors, the greatest common factor with lists and factor trees, multiples, the lowest common multiple of two or three numbers, and GCF or LCM word problems. 100 questions with an answer key.",
        "key_big": "The GCF is the biggest number that divides all the numbers. The LCM is the first number they all divide into.",
        "key_sub": "For 6 and 8: the GCF is 2 and the LCM is 24, not 6 × 8 = 48. Use the GCF for equal groups, rows and pieces, and the LCM for things that repeat and line up, like buses or hot dogs and buns.",
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
