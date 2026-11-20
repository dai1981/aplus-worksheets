# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Solving Problems: Money, Rate and Ratio (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_money_rate_ratio.py
Shopping and change, budgets, rates such as rand per kilogram, sharing in a ratio and equivalent ratios (makers from
the Grade 4 generator, UK Year 6 and BC Grade 6 makers).
Wrong answers come from real mistakes: giving the cost instead of the change, sharing equally when the story gives a
ratio, and adding instead of multiplying to scale a ratio.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_money_rate_ratio as zm4
adopt(zm4)
if isinstance(getattr(zm4, 'R', None), random.Random): zm4.R = random.Random(806160)
import gen_uk_maths_y6_ratio as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(806161)
import gen_cabc_math_g6_ratios as cbr
adopt(cbr)
if isinstance(getattr(cbr, 'R', None), random.Random): cbr.R = random.Random(806162)
import gen_cabc_math_g6_budgeting as cbb
adopt(cbb)
if isinstance(getattr(cbb, 'R', None), random.Random): cbb.R = random.Random(806163)
za_common.GRADE = "grade-6"

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


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)


GOODS = [("rice", "kg"), ("washing powder", "kg"), ("orange juice", "ℓ"), ("milk", "ℓ"), ("sugar", "kg"), ("cooking oil", "ℓ")]


def one_best(r):
    g, u = r.choice(GOODS)
    s1, s2 = r.choice([(1, 2), (2, 5), (1, 5), (2, 3), (3, 5)])
    p1 = r.randint(15, 40) * s1
    unit2 = r.randint(12, 45)
    p2 = unit2 * s2
    if p1 // s1 == unit2 or p1 % s1:
        raise AssertionError
    u1 = p1 // s1
    best = "the %d %s pack" % (s1, u) if u1 < unit2 else "the %d %s pack" % (s2, u)
    other = "the %d %s pack" % (s2, u) if u1 < unit2 else "the %d %s pack" % (s1, u)
    q = "Which is the better buy: %d %s of %s for R%s or %d %s for R%s?" % (s1, u, g, comma(p1), s2, u, comma(p2))
    return mcq(q, best, [other, "they cost the same per %s" % u, "the pack with the lower price"],
               "Price per %s: R%s ÷ %d = R%d and R%s ÷ %d = R%d. <b>%s</b> is cheaper per %s." % (u, comma(p1), s1, u1, comma(p2), s2, unit2, best[0].upper() + best[1:], u))


ITEMS6 = [("a pair of school shoes", 350, 650), ("a soccer ball", 180, 400), ("a school bag", 250, 500), ("a jacket", 400, 900), ("a bicycle", 1200, 3000), ("a pair of earphones", 150, 450)]


def one_disc(r):
    it, lo, hi = r.choice(ITEMS6)
    p = r.randint(lo // 10, hi // 10) * 10
    pc = r.choice([10, 20, 25, 30, 40, 50, 15, 5])
    d = p * pc / 100
    if d != int(d):
        raise AssertionError
    d = int(d)
    if r.random() < 0.5:
        return mcq("%s costs R%s. It is on sale at %d%% off. What is the sale price?" % (it[0].upper() + it[1:], comma(p), pc), "R" + comma(p - d), ["R" + comma(d), "R" + comma(p - pc), "R" + comma(p + d)],
                   "%d%% of R%s = R%s. R%s − R%s = <b>R%s</b>." % (pc, comma(p), comma(d), comma(p), comma(d), comma(p - d)))
    return mcq("%s costs R%s. The shop gives %d%% off. How much do you save?" % (it[0].upper() + it[1:], comma(p), pc), "R" + comma(d), ["R" + comma(p - d), "R" + comma(pc), "R" + comma(d * 10)],
               "%d%% of R%s: R%s ÷ 100 × %d = <b>R%s</b>." % (pc, comma(p), comma(p), pc, comma(d)))


def build():
    sets, R = build_sets([
        ("Shopping and change", [("collect", zm4.uniq(zm4.one_buy), 20)]),
        ("Best buys", [("collect", uniq(one_best), 20)]),
        ("Rates", [("collect", zm4.uniq(zm4.one_rate), 20)]),
        ("Ratio", [("run", cbr.set_equivalent, (), 10, dec3), ("run", ukr.set_sharing, ("rnd", ukr.People), 10, dec3)]),
        ("Ratio and rate problems", [("collect", zm4.uniq(zm4.one_ratio), 10), ("run", ukr.set_words, ("rnd", ukr.People), 10, dec3)]),
    ], 80616)
    finish(sets, R)
    body = lesson('<ul><li>Change = money paid − total cost.</li><li>A <b>rate</b> compares different kinds of quantities: R18 per kg, 60 km per hour.</li><li>A <b>ratio</b> compares quantities of the same kind: 2 : 3.</li><li>To share in a ratio, add the parts, find one part, then multiply.</li></ul>',
        [example("Share R450 in the ratio 2 : 3", ["5 parts: R450 ÷ 5 = R90"], "R180 and R270")],
        [['Cost instead of change', 'Subtract from the money paid.'], ['Sharing equally', 'Use the ratio.'], ['Adding to scale', 'Multiply both parts by the same number.']])
    faq = [('What does CAPS Grade 6 say about problem solving?', 'Solve problems in financial contexts (profit, loss, discount, budgets) and problems that compare quantities of the same kind (ratio) and of different kinds (rate).'), ('What is a best buy?', 'The item with the lowest price per unit.'), ('Is 2 : 3 the same as 4 : 6?', 'Yes, equivalent ratios.'), ('What is profit?', 'Selling price − cost price.')]
    make('money-rate-and-ratio-problems', 16, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Solve problems in contexts involving whole numbers, including financial contexts (profit, loss, discount and budgets), comparing two or more quantities of the same kind (ratio), and comparing two quantities of different kinds (rate).',
         'Solving Problems: Money, Rate and Ratio', 'Money, Rate and Ratio',
         'Free CAPS Grade 6 money worksheets: shopping and change, budgets, best buys, rates and ratio problems. 100 questions with memos.',
         'Rate: different kinds. Ratio: same kind.', 'Ratio sharing: add the parts, find one part.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
