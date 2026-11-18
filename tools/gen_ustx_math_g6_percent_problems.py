# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Percent Problems: Part, Whole and Percent (TEKS 6.5B)
  python3 tools/gen_ustx_math_g6_percent_problems.py
Finding the percent of a quantity, the whole from a part and a percent, and the percent from a part and a whole,
mixed problems, and word problems with tests, discounts and surveys (the US Grade 6 makers, plus own makers).
Wrong answers come from real mistakes: dividing by the percent instead of multiplying, putting the part and whole
the wrong way round, and forgetting to subtract a discount.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_percents as pc
adopt(pc)
tx_common.GRADE = "grade-6"

from fractions import Fraction as F

NICE = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (7, 20), (9, 20), (11, 20),
        (1, 25), (3, 25), (6, 25), (12, 25), (1, 8), (3, 8), (5, 8), (7, 8), (5, 4), (3, 2), (7, 4), (6, 5), (1, 50), (13, 50)]


def dec(v):
    s = ("%.3f" % float(v)).rstrip("0").rstrip(".")
    return s


def pct(v):
    p = v * 100
    return (str(p.numerator) if p.denominator == 1 else dec(p)) + "%"


def frs(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, n = divmod(v.numerator, v.denominator)
    return (str(w) if w else "") + fr(n, v.denominator)


def one_pct(r):
    w = r.choice([20, 25, 40, 50, 80, 200, 300, 400, 500])
    p = r.choice([5, 10, 15, 20, 25, 30, 40, 45, 60, 75, 80, 90])
    part = w * p // 100
    if w * p % 100 or part == 0:
        return None
    return mcq("What percent of %d is %d?" % (w, part), "%d%%" % p, ["%d%%" % (w * 100 // part) if w * 100 % part == 0 else "%d%%" % (p + 10), "%d%%" % part, "%d%%" % (p * 2) if p * 2 <= 100 else "%d%%" % (p // 5)],
               "%d/%d = %s = <b>%d%%</b>." % (part, w, dec(F(part, w)), p))


def one_three(r):
    k = Kid(r).next()
    kind = r.choice(["part", "whole", "pct"])
    w = r.choice([20, 25, 40, 50, 60, 80, 120, 200, 240, 300])
    p = r.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
    part = w * p // 100
    if w * p % 100:
        return None
    ctx = r.choice([("students in the band", "play a brass instrument", "students"), ("seats on the bus", "are taken", "seats"), ("pecan trees in the orchard", "are fully grown", "trees"), ("photos on %s's phone" % k["n"], "show the Gulf Coast", "photos")])
    if kind == "part":
        return mcq("There are %d %s. %d%% of them %s. How many is that?" % (w, ctx[0], p, ctx[1]), str(part), [str(w - part), str(part * 10) if part * 10 != w else str(part + p), str(p)],
                   "%d%% of %d = %s × %d = <b>%d</b>." % (p, w, dec(F(p, 100)), w, part))
    if kind == "whole":
        return mcq("%d of the %s %s. That is %d%% of them. How many %s are there in all?" % (part, ctx[0], ctx[1], p, ctx[2]), str(w), [str(part * p // 10) if part * p % 10 == 0 else str(part + p), str(part * 100 // p + part), str(part + 100)],
                   "%d is %d%% of the whole. Whole = %d ÷ %s = <b>%d</b>." % (part, p, part, dec(F(p, 100)), w))
    return mcq("%d of the %d %s %s. What percent is that?" % (part, w, ctx[0], ctx[1]), "%d%%" % p, ["%d%%" % part, "%d%%" % (100 - p), "%d%%" % (p * 2) if p * 2 <= 100 else "%d%%" % (p // 2)],
               "%d/%d = %s = <b>%d%%</b>." % (part, w, dec(F(part, w)), p))


def build():
    sets, R = build_sets([
        ("Find the percent of a quantity", [("run", pc.set_pof, ("rnd",), 20)]),
        ("Find the whole from a part and a percent", [("run", pc.set_whole, ("rnd",), 20)]),
        ("Find the percent from a part and a whole", [("collect", one_pct, 20)]),
        ("Part, whole or percent?", [("collect", one_three, 20)]),
        ("Word problems: tests, discounts and surveys", [("run", pc.set_words, ("rnd",), 20)]),
    ], 66010)
    finish(sets, R)
    body = lesson('<ul><li>Every percent problem has a <b>part</b>, a <b>whole</b> and a <b>percent</b>: part = percent × whole.</li><li><b>Part</b>: 30% of 70 = 0.3 × 70 = 21.</li><li><b>Whole</b>: 12 is 25% of what? 12 ÷ 0.25 = 48.</li><li><b>Percent</b>: 18 out of 20 = 18/20 = 0.9 = 90%.</li></ul>',
        [example("What is 15% of 80?", ["10% = 8, 5% = 4", "8 + 4"], "12"), example("12 is 25% of a number.", ["25% = 1/4", "12 × 4"], "48")],
        [['Dividing by the percent when finding a part', 'Part = percent × whole: 30% of 70 = 21.'], ['Using the part as the whole', "The whole is the total amount, after 'of'."], ['Forgetting to subtract a discount', 'A 20% discount means you pay 80%.']])
    faq = [('What does TEKS 6.5B ask?', 'Solve real-world problems to find the whole given a part and the percent, to find the part given the whole and the percent, and to find the percent given the part and the whole, including the use of concrete and pictorial models.'), ('How can I find 10% fast?', 'Move the decimal point one place left: 10% of 70 is 7.'), ('How do I find the whole?', 'Divide the part by the percent written as a decimal: 12 ÷ 0.25 = 48.'), ('Which number is the whole?', "The total amount, usually after the word 'of'.")]
    make('percent-problems', 10, 'Proportionality', '6.5B',
         '6.5B solve real-world problems to find the whole given a part and the percent, to find the part given the whole and the percent, and to find the percent given the part and the whole, including the use of concrete and pictorial models',
         'Percent Problems: Part, Whole and Percent', 'Percent Problems',
         'Free Grade 6 percent worksheets for Texas TEKS 6.5B: find the part, the whole and the percent, mixed problems, and word problems with tests, discounts and surveys. 100 questions with answers.',
         'Part = percent × whole.', '30% of 70 = 21. 12 is 25% of 48. 18 out of 20 = 90%.',
         body, faq, sets, seo_title='Grade 6 Percent Problems Worksheets: Find the Part, Whole and Percent (TEKS 6.5B, STAAR)')


if __name__ == "__main__":
    build()
