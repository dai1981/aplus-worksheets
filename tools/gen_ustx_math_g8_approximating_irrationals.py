# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Approximating Irrational Numbers (TEKS 8.2B)
  python3 tools/gen_ustx_math_g8_approximating_irrationals.py
Perfect squares and square roots, square roots between two whole numbers, estimating to the nearest tenth, locating
irrational numbers on a number line, and area problems (US Grade 8 makers with a new seed, plus an own number line
maker).
Wrong answers come from real mistakes: halving instead of taking the square root, picking the wrong pair of
perfect squares, and placing √n closer to the wrong whole number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_square_and_cube_roots as scr
adopt(scr)
scr.R = random.Random(680020)
import gen_us_math_g8_rational_and_irrational_numbers as rai
adopt(rai)
rai.R = random.Random(680021)
tx_common.GRADE = "grade-8"

import math
from fractions import Fraction as F
from ws_common import num


def sq(n):
    return "√%d" % n


def realval(s):
    return s[1]

INK = "#1f2937"


def nl_svg(lo, hi, pts):
    W, x0, x1 = 340, 20, 320
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / float(hi - lo)
    s = ["<svg viewBox='0 0 %d 80' width='%d' data-pf='lg' role='img' aria-label='number line from %d to %d'>" % (W, W, lo, hi)]
    s.append("<line x1='%d' y1='45' x2='%d' y2='45' stroke='%s' stroke-width='2'/>" % (x0, x1, INK))
    for t in range(lo, hi + 1):
        s.append("<line x1='%.1f' y1='38' x2='%.1f' y2='52' stroke='%s' stroke-width='2'/><text x='%.1f' y='70' font-size='13' text-anchor='middle' fill='%s'>%d</text>" % (sx(t), sx(t), INK, sx(t), INK, t))
        if t < hi:
            for j in range(1, 10):
                s.append("<line x1='%.1f' y1='42' x2='%.1f' y2='48' stroke='%s'/>" % (sx(t + j / 10.0), sx(t + j / 10.0), INK))
    for lab, v in pts:
        s.append("<circle cx='%.1f' cy='45' r='5' fill='#2563eb'/><text x='%.1f' y='26' font-size='14' font-weight='bold' text-anchor='middle' fill='#2563eb'>%s</text>" % (sx(v), sx(v), lab))
    s.append("</svg>")
    return fig("".join(s))


def one_locate(r):
    n = r.choice([k for k in range(3, 150) if int(math.isqrt(k)) ** 2 != k])
    v = math.sqrt(n)
    lo = int(v) - 1
    hi = lo + 3
    if lo < 0:
        lo, hi = 0, 3
    cands = [v]
    while len(cands) < 4:
        c = round(lo + r.random() * (hi - lo), 1)
        if c > lo and c < hi and all(abs(c - x) > 0.35 for x in cands):
            cands.append(c)
    order = sorted(cands)
    labs = "ABCD"
    pts = [(labs[i], x) for i, x in enumerate(order)]
    right = labs[order.index(v)]
    return mcq(nl_svg(lo, hi, pts) + "Which point best shows √%d?" % n, "Point %s" % right, ["Point %s" % l for l in labs if l != right],
               "%d² = %d and %d² = %d, so √%d is between %d and %d, about %.1f. That is <b>point %s</b>." % (int(v), int(v) ** 2, int(v) + 1, (int(v) + 1) ** 2, n, int(v), int(v) + 1, v, right))


def one_pi(r):
    kind = r.choice(["pi", "2pi", "half", "pi2"])
    val = {"pi": math.pi, "2pi": 2 * math.pi, "half": math.pi / 2, "pi2": math.pi + 2}[kind]
    lab = {"pi": "π", "2pi": "2π", "half": "π ÷ 2", "pi2": "π + 2"}[kind]
    a = int(val)
    return mcq("Between which two whole numbers is %s?" % lab, "%d and %d" % (a, a + 1), ["%d and %d" % (a - 1, a), "%d and %d" % (a + 1, a + 2), "%d and %d" % (a + 2, a + 3)],
               "π ≈ 3.14, so %s ≈ %.2f, between <b>%d and %d</b>." % (lab, val, a, a + 1))


def build():
    sets, R = build_sets([
        ("Perfect squares and square roots", [("run", scr.set_sqrt, (), 20)]),
        ("Between which two whole numbers?", [("run", scr.set_estimate, (), 16), ("collect", one_pi, 4)]),
        ("Estimate to the nearest tenth", [("run", rai.set_estimate, (), 20)]),
        ("Locate on a number line", [("collect", one_locate, 20)]),
        ("Area and reasoning", [("run", scr.set_words, (), 20)]),
    ], 68002)
    finish(sets, R)
    body = lesson('<ul><li>Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225.</li><li>To estimate √n, find the perfect squares on either side: √50 is between √49 = 7 and √64 = 8.</li><li>50 is very close to 49, so √50 ≈ 7.1.</li><li>π ≈ 3.14, so π is between 3 and 4.</li></ul>',
        [example("Estimate √30.", ["25 < 30 < 36", "5 < √30 < 6", "5.5² = 30.25"], "≈ 5.5")],
        [['Halving instead of taking the square root', '√36 = 6, not 18.'], ['Picking the wrong perfect squares', 'List the squares near the number first.'], ['Placing √n closer to the wrong number', '√50 is near 7 because 50 is near 49.']])
    faq = [('What does TEKS 8.2B ask?', 'Approximate the value of an irrational number, including π and square roots of numbers less than 225, and locate that rational number approximation on a number line.'), ('Why less than 225?', '225 = 15², so you only need the squares up to 15.'), ('How can I check an estimate?', 'Square it: 7.1² = 50.41, close to 50.'), ('Is √2 about 1.4?', 'Yes. 1.4² = 1.96.')]
    make('approximating-irrational-numbers', 2, 'Number and Operations', '8.2B',
         '8.2B approximate the value of an irrational number, including π and square roots of numbers less than 225, and locate that rational number approximation on a number line',
         'Approximating Irrational Numbers', 'Approximating Irrational Numbers',
         'Free Grade 8 worksheets for Texas TEKS 8.2B: perfect squares, estimating square roots and π, the nearest tenth and locating irrational numbers on a number line. 100 questions with answers.',
         'Find the perfect squares on either side.', '√50 is between 7 and 8, about 7.1.',
         body, faq, sets, seo_title='Grade 8 Approximating Irrational Numbers and Square Roots Worksheets (TEKS 8.2B, STAAR)')


if __name__ == "__main__":
    build()
