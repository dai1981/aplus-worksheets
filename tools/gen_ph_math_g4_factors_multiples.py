# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Factors and Multiples of Numbers up to 100 (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_factors_multiples.py
Multiples of numbers up to 100, checking whether a number is a factor, finding all the factors and factor pairs of a
number up to 100, and word problems with equal rows and packs (own makers).
Wrong answers come from real mistakes: mixing up factors and multiples, forgetting 1 and the number itself, and
leaving out the middle factor pair.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)

ph_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def facs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def pairs(n):
    return [(d, n // d) for d in facs(n) if d <= n // d]


def lst(v):
    return ", ".join(str(x) for x in v)


def one_mult(r):
    a = r.randint(3, 12)
    kind = r.choice(["which", "list", "not"])
    if kind == "which":
        k = r.randint(3, 100 // a)
        right = a * k
        w = [right + 1, right - 1 if right - 1 != a else right + 2, right + (a // 2 or 1) if (right + (a // 2 or 1)) % a else right + 1 + a]
        w = [x for x in w if x % a]
        while len(w) < 3:
            w.append(w[-1] + 2 if (w[-1] + 2) % a else w[-1] + 3)
        return mcq("Which number is a multiple of %d?" % a, right, w,
                   "%d × %d = %d, so %d is a multiple of %d. The others leave a remainder when divided by %d. <b>%d</b>." % (a, k, right, right, a, a, right))
    if kind == "list":
        s = r.randint(1, 4)
        right = lst(a * i for i in range(s, s + 5))
        w = [lst(a + i for i in range(s, s + 5)), lst(d for d in facs(a * 6)[:5]) if len(facs(a * 6)) >= 5 else lst(a * i + 1 for i in range(s, s + 5)), lst(a * i for i in range(s, s + 6, 1) if i != s + 2)]
        q = "Which list shows multiples of %d in order, starting at %d?" % (a, a * s)
        return mcq(q, right, w, "Count by %ds from %d: <b>%s</b>." % (a, a * s, right))
    ms = [a * i for i in r.sample(range(2, 100 // a + 1), 3)]
    odd = r.choice([m + r.choice([1, 2, -1]) for m in ms])
    if odd % a == 0:
        raise AssertionError
    return mcq("Which number is <b>not</b> a multiple of %d?" % a, odd, ms,
               "%d ÷ %d = %d remainder %d, so %d is not a multiple of %d. The others are %s. <b>%d</b>." % (odd, a, odd // a, odd % a, odd, a, lst("%d × %d" % (a, m // a) for m in ms), odd))


def one_isfactor(r):
    n = r.choice([x for x in range(12, 101) if len(facs(x)) >= 6])
    fs = facs(n)
    if r.random() < 0.6:
        right = r.choice(fs[1:-1])
        non = [d for d in range(2, min(n, 30)) if n % d]
        w = r.sample(non, 3)
        return mcq("Which number is a factor of %d?" % n, right, w,
                   "%d × %d = %d, so %d is a factor of %d. The others leave a remainder. <b>%d</b>." % (right, n // right, n, right, n, right))
    right = r.choice([d for d in range(2, min(n, 30)) if n % d])
    w = r.sample(fs[1:-1], 3)
    return mcq("Which number is <b>not</b> a factor of %d?" % n, right, w,
               "%d ÷ %d = %d remainder %d, so %d is not a factor of %d. <b>%d</b>." % (n, right, n // right, n % right, right, n, right))


def one_all(r):
    n = r.choice([x for x in range(12, 101) if len(facs(x)) >= 6])
    fs, ps = facs(n), pairs(n)
    kind = r.choice(["list", "list", "count"])
    if kind == "count":
        right = len(fs)
        sq = any(a == b for a, b in ps)
        w = [len(ps), right - 2, right + 1 if not sq else right + 1]
        return mcq("How many factors does %d have?" % n, right, w,
                   "Factor pairs: %s. The factors are %s, so there are <b>%d</b>." % (", ".join("%d × %d" % p for p in ps), lst(fs), right))
    mid = ps[-1]
    no_mid = [d for d in fs if d not in mid]
    w = [lst(no_mid), lst(fs[1:-1]), lst(n * i for i in range(1, 5))]
    return mcq("Which list shows <b>all</b> the factors of %d?" % n, lst(fs), w,
               "Find the factor pairs: %s. Do not forget 1 and %d. <b>%s</b>." % (", ".join("%d × %d" % p for p in ps), n, lst(fs)))


def one_pair(r):
    n = r.choice([x for x in range(12, 101) if len(facs(x)) >= 4])
    a, b = r.choice([p for p in pairs(n) if p[0] > 1])
    q = "%d × ☐ = %d. What is the missing factor?" % (a, n)
    w = [n - a, b + 1, n + a, a * 2 if a * 2 != b else b - 1]
    return mcq(q, b, w, "%d ÷ %d = %d, so %d × <b>%d</b> = %d." % (n, a, b, a, b, n))


ROWS = [("%(n)s's teacher arranges %(N)d chairs in equal rows.", "rows"), ("A farmer plants %(N)d mango seedlings in equal rows.", "rows"),
        ("%(N)d learners are put into equal groups for a game.", "groups"), ("%(n)s puts %(N)d photos on a wall in equal rows.", "rows")]
PACKS = [("Pandesal is sold in bags of %(a)d.", "pandesal"), ("Eggs come in trays of %(a)d.", "eggs"), ("Pencils come in boxes of %(a)d.", "pencils"),
         ("Bottles of water come in packs of %(a)d.", "bottles")]


def one_word(r):
    k = Kid(r).next()
    if r.random() < 0.5:
        t, what = r.choice(ROWS)
        N = r.choice([x for x in range(18, 101) if len(facs(x)) >= 6])
        bad = r.choice([d for d in range(3, 13) if N % d])
        good = r.sample(facs(N)[1:-1], 3)
        q = (t % {"n": k["n"], "N": N}) + " Which number of %s is <b>not</b> possible?" % what
        return mcq(q, "%d %s" % (bad, what), ["%d %s" % (g, what) for g in good],
                   "%d is not a factor of %d (%d ÷ %d = %d remainder %d). The others are factors. <b>%d %s</b>." % (bad, N, N, bad, N // bad, N % bad, bad, what))
    t, what = r.choice(PACKS)
    a = r.choice([4, 6, 8, 10, 12, 30]) if what == "eggs" else r.randint(4, 12)
    k_ = r.randint(3, 100 // a)
    right = a * k_
    w = [right + 2, right - 3, right + a // 2 + 1]
    w = [x for x in w if x % a]
    q = (t % {"a": a}) + " %s wants to buy whole packs only. Which number of %s can %s buy?" % (k["n"], what, k["he"])
    return mcq(q, right, w, "%d is a multiple of %d: %d × %d = %d. <b>%d</b>." % (right, a, k_, a, right, right))


def build():
    sets, R = build_sets([
        ("Multiples", [("collect", uniq(one_mult), 20)]),
        ("Is it a factor?", [("collect", uniq(one_isfactor), 20)]),
        ("Find all the factors", [("collect", uniq(one_all), 20)]),
        ("Factor pairs", [("collect", uniq(one_pair), 20)]),
        ("Factors and multiples word problems", [("collect", uniq(one_word), 20)]),
    ], 70417)
    finish(sets, R)
    body = lesson('<ul><li>A <b>multiple</b> of a number is what you get when you multiply it by 1, 2, 3, … The multiples of 6 are 6, 12, 18, 24, …</li><li>A <b>factor</b> divides a number exactly, with no remainder. 4 is a factor of 24 because 24 ÷ 4 = 6.</li><li>To find all the factors, list the factor pairs: 1 × 24, 2 × 12, 3 × 8, 4 × 6. Stop when the pairs meet.</li><li>1 and the number itself are always factors.</li></ul>',
        [example("Factors of 36", ["1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6"], "1, 2, 3, 4, 6, 9, 12, 18, 36")],
        [['Mixing up factors and multiples', 'Factors are small (they divide); multiples are big.'], ['Forgetting 1 and the number', 'They are always factors.'], ['Missing the middle pair', '6 × 6 = 36: 6 is a factor too.']])
    faq = [('What does MATATAG Math 4 ask about factors and multiples?', 'Identify the multiples of given numbers up to 100, and find all the factors of a given number up to 100.'), ('Is a number a multiple of itself?', 'Yes: 7 × 1 = 7.'), ('How do I know when I have all the factors?', 'Stop when the factor pairs start to repeat.'), ('Is 1 a factor of every number?', 'Yes.')]
    make('factors-and-multiples', 17, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Identify the multiples of given numbers up to 100; find all the factors of a given number up to 100.',
         'Factors and Multiples of Numbers up to 100', 'Factors and Multiples',
         'Free Grade 4 factors and multiples worksheets for the DepEd MATATAG curriculum: multiples, factors, factor pairs and word problems for numbers up to 100. 100 questions with answers.',
         'Factors divide exactly; multiples come from multiplying.', 'List factor pairs until they meet.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
