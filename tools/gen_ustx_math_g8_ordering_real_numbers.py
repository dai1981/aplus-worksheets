# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Comparing and Ordering Real Numbers (TEKS 8.2D)
  python3 tools/gen_ustx_math_g8_ordering_real_numbers.py
Comparing two real numbers, ordering sets of real numbers (US Grade 8 maker with a new seed and own makers), numbers
between two values, and real-world ordering.
Wrong answers come from real mistakes: comparing √n with n, forgetting that −√10 is less than −3, and ordering by
the digits only.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_rational_and_irrational_numbers as rai
adopt(rai)
rai.R = random.Random(680040)
tx_common.GRADE = "grade-8"

import math
from fractions import Fraction as F
from ws_common import num


def sq(n):
    return "√%d" % n


def realval(s):
    return s[1]


def item(r):
    t = r.choice(["sq", "sq", "frac", "dec", "pi", "neg"])
    if t == "sq":
        n = r.choice([k for k in range(2, 120) if math.isqrt(k) ** 2 != k])
        return ("√%d" % n, math.sqrt(n))
    if t == "frac":
        b = r.choice([3, 4, 5, 6, 7, 8, 9])
        a = r.randint(b + 1, 9 * b)
        if F(a, b).denominator != b:
            return None
        w, n = divmod(a, b)
        return ("%d%s" % (w, fr(n, b)), a / float(b))
    if t == "dec":
        v = r.randint(10, 99) / 10.0
        return ("%.1f" % v, v)
    if t == "pi":
        k = r.choice([1, 2, 3])
        return ("π" if k == 1 else "%dπ" % k, k * math.pi)
    n = r.choice([k for k in range(2, 60) if math.isqrt(k) ** 2 != k])
    return ("−√%d" % n, -math.sqrt(n))


def several(r, k):
    out = []
    for _ in range(40):
        it = item(r)
        if it and all(abs(it[1] - o[1]) > 0.08 for o in out) and it[0] not in [o[0] for o in out]:
            out.append(it)
        if len(out) == k:
            return out
    return None


def one_compare(r):
    p = several(r, 2)
    if not p:
        return None
    (a, va), (b, vb) = p
    right = "%s &gt; %s" % (a, b) if va > vb else "%s &lt; %s" % (a, b)
    wrong = "%s &lt; %s" % (a, b) if va > vb else "%s &gt; %s" % (a, b)
    return mcq("Which is true?", right, [wrong, "%s = %s" % (a, b), "You cannot compare them"], "%s ≈ %.2f and %s ≈ %.2f, so <b>%s</b>." % (a, va, b, vb, right))


def one_order(r):
    p = several(r, 4)
    if not p:
        return None
    asc = sorted(p, key=lambda x: x[1])
    right = ", ".join(x[0] for x in asc)
    wrongs = [", ".join(x[0] for x in reversed(asc)), ", ".join(x[0] for x in sorted(p, key=lambda x: x[0])), ", ".join(x[0] for x in [asc[1], asc[0], asc[2], asc[3]])]
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    if len(wrongs) < 3:
        wrongs.append(", ".join(x[0] for x in [asc[0], asc[2], asc[1], asc[3]]))
    return mcq("Order from least to greatest.", right, wrongs[:3], "Approximate: %s. Order: <b>%s</b>." % (", ".join("%s ≈ %.2f" % x for x in asc), right))


def one_between(r):
    a = r.randint(2, 11)
    good = r.choice([k for k in range(a * a + 1, (a + 1) ** 2)])
    bad = [r.choice(range((a - 1) ** 2 + 1, a * a)) if a > 2 else 3, (a + 1) ** 2 + r.randint(1, 2 * a), a + r.randint(1, 3)]
    return mcq("Which number is between %d and %d?" % (a, a + 1), "√%d" % good, ["√%d" % b for b in bad[:2]] + ["%d.%d" % (a + 1, r.randint(1, 9))],
               "%d = √%d and %d = √%d, so √%d is between them: <b>√%d</b>." % (a, a * a, a + 1, (a + 1) ** 2, good, good))


def one_world(r):
    names = r.sample(["Ava", "Diego", "Mia", "Luis", "Sofia", "Ethan"], 3)
    vals = several(r, 3)
    if not vals or any(v[1] <= 0 for v in vals):
        return None
    big = max(range(3), key=lambda i: vals[i][1])
    return mcq("Three friends measured plant growth in centimeters: %s: %s, %s: %s, %s: %s. Whose plant grew the most?" % (names[0], vals[0][0], names[1], vals[1][0], names[2], vals[2][0]),
               names[big], [n for i, n in enumerate(names) if i != big] + ["They grew the same"], "%s. The greatest is <b>%s</b> (%s)." % (", ".join("%s ≈ %.2f" % v for v in vals), names[big], vals[big][0]))


def build():
    sets, R = build_sets([
        ("Compare two real numbers", [("collect", one_compare, 20)]),
        ("Compare and order", [("run", rai.set_order, (), 20)]),
        ("Order four real numbers", [("collect", one_order, 20)]),
        ("Numbers between two values", [("collect", one_between, 20)]),
        ("Real-world ordering", [("collect", one_world, 20)]),
    ], 68004)
    finish(sets, R)
    body = lesson('<ul><li>Write every number as a decimal approximation: √10 ≈ 3.16, π ≈ 3.14, 3 1/4 = 3.25.</li><li>Then compare the decimals, or place them on a number line.</li><li>For negative numbers, the one farther from 0 is less: −√10 &lt; −3.</li><li>A square root √n is between the square roots of the perfect squares on either side.</li></ul>',
        [example("Order √10, π, 3 1/4, 3.2", ["3.16, 3.14, 3.25, 3.2"], "π, √10, 3.2, 3 1/4")],
        [['Comparing √n with n', '√10 ≈ 3.16, not 10.'], ['Forgetting negatives reverse the order', '−√10 ≈ −3.16 is less than −3.'], ['Ordering by the digits only', 'Change every number to a decimal first.']])
    faq = [('What does TEKS 8.2D ask?', 'Order a set of real numbers arising from mathematical and real-world contexts.'), ('Is √10 greater than π?', 'Yes. √10 ≈ 3.162 and π ≈ 3.142.'), ('How many decimal places do I need?', 'Use enough places to tell the numbers apart, usually two.'), ('Can I use a number line?', 'Yes. Place each approximation, then read from left to right.')]
    make('ordering-real-numbers', 4, 'Number and Operations', '8.2D',
         '8.2D order a set of real numbers arising from mathematical and real-world contexts',
         'Comparing and Ordering Real Numbers', 'Ordering Real Numbers',
         'Free Grade 8 worksheets for Texas TEKS 8.2D: compare and order real numbers including square roots, π, fractions and decimals, numbers between two values and word problems. 100 questions with answers.',
         'Change every number to a decimal, then compare.', 'π ≈ 3.14 < √10 ≈ 3.16 < 3.2 < 3 1/4.',
         body, faq, sets, seo_title='Grade 8 Comparing and Ordering Real Numbers Worksheets (TEKS 8.2D, STAAR)')


if __name__ == "__main__":
    build()
