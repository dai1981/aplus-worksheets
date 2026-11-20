# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Financial Maths: Compound Interest, Hire Purchase, Exchange Rates, Commission and Rentals (Grade 9: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g9_financial_maths.py
Compound interest and growth, depreciation, hire purchase, exchange rates (makers from the Grade 8 generator and UK Year 9
makers), commission and rentals (own makers), with rand.
Wrong answers come from real mistakes: using simple interest for compound interest, adding the depreciation
instead of subtracting it, and forgetting the basic salary.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g8_financial_maths as zf8
adopt(zf8)
if isinstance(getattr(zf8, 'R', None), random.Random): zf8.R = random.Random(809020)
import gen_uk_maths_y9_compound_interest_and_growth as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(809021)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))


def uniq(fn):
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


SALES = [("cars", 150000, 400000), ("houses", 800000, 3000000), ("cellphones", 3000, 15000), ("furniture", 5000, 40000)]


def one_comm(r):
    kk = Kid(r).next()
    what, lo, hi = r.choice(SALES)
    pc = r.choice([2, 3, 4, 5, 6, 7, 8, 10])
    total = r.randint(lo // 1000, hi // 1000) * 1000 * r.randint(1, 3)
    c = total * pc // 100
    if total * pc % 100:
        raise AssertionError
    if r.random() < 0.6:
        return mcq("%s sells %s worth R%s this month and earns %d%% commission. How much commission does %s earn?" % (kk["n"], what, comma(total), pc, kk["he"]), "R" + comma(c),
                   ["R" + comma(c * 10), "R" + comma(c // 10), "R" + comma(total - c)], "%d%% of R%s = <b>R%s</b>." % (pc, comma(total), comma(c)))
    base = r.choice([6000, 8000, 10000, 12000])
    return mcq("%s earns a basic salary of R%s plus %d%% commission. This month %s sells %s worth R%s. What does %s earn in total?" % (kk["n"], comma(base), pc, kk["he"], what, comma(total), kk["he"]),
               "R" + comma(base + c), ["R" + comma(c), "R" + comma(base + total), "R" + comma(base + pc * 100)],
               "Commission: %d%% of R%s = R%s. Total: R%s + R%s = <b>R%s</b>." % (pc, comma(total), comma(c), comma(base), comma(c), comma(base + c)))


def one_rent(r):
    kk = Kid(r).next()
    rent = r.randint(40, 120) * 100
    inc = r.choice([5, 6, 8, 10])
    new = rent * (100 + inc) / 100
    if new != int(new):
        raise AssertionError
    new = int(new)
    return mcq("%s rents a flat for R%s a month. The rent goes up by %d%% next year. What will the new monthly rent be?" % (kk["n"], comma(rent), inc), "R" + comma(new),
               ["R" + comma(rent * inc // 100), "R" + comma(rent + inc), "R" + comma(new * 12)],
               "%d%% of R%s = R%s. R%s + R%s = <b>R%s</b>." % (inc, comma(rent), comma(rent * inc // 100), comma(rent), comma(rent * inc // 100), comma(new)))


def build():
    sets, R = build_sets([
        ("Compound interest", [("collect", zf8.uniq(zf8.one_ci), 10), ("collect", ukc.one_mult, 10)]),
        ("Growth and depreciation", [("collect", ukc.one_dep, 10), ("collect", ukc.one_growth, 10)]),
        ("Hire purchase", [("collect", zf8.uniq(zf8.one_hp), 20)]),
        ("Exchange rates", [("collect", zf8.uniq(zf8.one_fx), 20)]),
        ("Commission and rentals", [("collect", uniq(one_comm), 10), ("collect", uniq(one_rent), 10)]),
    ], 80902)
    finish(sets, R)
    body = lesson('<ul><li>Compound interest: A = P(1 + i)ⁿ.</li><li>Depreciation: the value goes down by a percentage each year: A = P(1 − i)ⁿ.</li><li>Commission is a percentage of the sales a person makes.</li><li>Rent increases are a percentage of the old rent.</li></ul>',
        [example("R8 000 at 6% compound interest for 2 years", ["8 000 × 1,06²"], "R8 988,80")],
        [['Simple for compound', 'Use (1 + i)ⁿ.'], ['Adding depreciation', 'Depreciation makes the value smaller.'], ['Forgetting the salary', 'Add the basic salary and the commission.']])
    faq = [('What does CAPS Grade 9 say about financial maths?', 'Solve problems involving simple and compound interest, hire purchase, exchange rates, commission and rentals.'), ('What is depreciation?', 'A loss of value over time, like a car getting older.'), ('What is commission?', 'Money earned as a percentage of sales.'), ('Why is compound interest more?', 'Interest is earned on interest.')]
    make('financial-maths', 2, 'Numbers, Operations and Relationships', 'Grade 9: 1.1 Whole numbers',
         'Solve problems that involve whole numbers, percentages and decimal fractions in financial contexts such as profit, loss, discount and VAT, budgets, accounts, loans, simple interest, hire purchase, exchange rates, commission, rentals and compound interest.',
         'Financial Maths: Compound Interest, Hire Purchase, Exchange Rates, Commission and Rentals', 'Financial Maths',
         'Free CAPS Grade 9 financial maths worksheets: compound interest, depreciation, hire purchase, exchange rates, commission and rentals. 100 questions with memos.',
         'A = P(1 + i)ⁿ.', 'Depreciation: A = P(1 − i)ⁿ.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
