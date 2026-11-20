# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Percentages: Fractions, Decimals and Percentages of Whole Numbers (Grade 6: 1.2 Common fractions)
  python3 tools/gen_za_maths_g6_percentages.py
Percentages as fractions and decimals, finding percentages of whole numbers and amounts, discounts and problems
(UK Year 6, Australia Year 6 and BC Grade 6 makers), with rand and South African decimal commas.
Wrong answers come from real mistakes: reading 5% as 0,5, dividing by the percentage, and giving the discount instead
of the new price.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_percentages as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(806150)
import gen_au_maths_y6_percentages as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806151)
import gen_cabc_math_g6_percents as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806152)
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
        ("Percentages, fractions and decimals", [("run", aup.set_fractions, ("rnd",), 10, dec3), ("run", cbp.set_fdp, (), 10, dec3)]),
        ("Simple percentages", [("run", ukp.set_simple, ("rnd",), 15, dec3), ("run", ukp.set_what, ("rnd", ukp.People), 5, dec3)]),
        ("Percentages of amounts", [("run", ukp.set_build, ("rnd", ukp.People), 10, dec3), ("run", cbp.set_percent_of, (), 10, dec3)]),
        ("Discounts", [("collect", uniq(one_disc), 20)]),
        ("Percentage problems", [("run", ukp.set_words, ("rnd", ukp.People), 10, dec3), ("run", aup.set_problems, ("rnd", aup.People), 10, dec3)]),
    ], 80615)
    finish(sets, R)
    body = lesson("<ul><li>Per cent means out of 100: 35% = <span class='fr'><span class='fn'>35</span><span class='fd'>100</span></span> = 0,35.</li><li>50% is a half, 25% is a quarter, 10% is a tenth.</li><li>To find 10%, divide by 10. Build other percentages from it: 30% = 3 × 10%.</li><li>A discount is taken off the price: new price = price − discount.</li></ul>",
        [example("35% of R240", ["10% = R24", "30% = R72, 5% = R12"], "R84")],
        [['5% as 0,5', '5% = 0,05.'], ['Dividing by the percentage', 'Find 1% or 10% first.'], ['The discount, not the price', 'Subtract the discount.']])
    faq = [('What does CAPS Grade 6 say about percentages?', 'Find percentages of whole numbers, and recognise and use the equivalence of common fractions, decimal fractions and percentages.'), ('What is 20% of 50?', '10.'), ('Is 100% the whole?', 'Yes.'), ('How do I find 15%?', '10% + 5% (half of 10%).')]
    make('percentages', 15, 'Numbers, Operations and Relationships', 'Grade 6: 1.2 Common fractions',
         'Find percentages of whole numbers; recognise and use equivalent forms of common fractions, decimal fractions and percentages; solve problems in context involving percentages.',
         'Percentages: Fractions, Decimals and Percentages of Whole Numbers', 'Percentages',
         'Free CAPS Grade 6 percentages worksheets: percentages as fractions and decimals, percentages of amounts, discounts and problems. 100 questions with memos.',
         'Per cent means out of 100.', 'Find 10%, then build the percentage.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
