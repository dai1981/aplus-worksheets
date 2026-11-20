# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Financial Maths: Hire Purchase, Simple and Compound Interest, and Exchange Rates (Grade 8: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g8_financial_maths.py
Hire purchase, simple and compound interest, exchange rates (own makers) and percentage change (UK Year 8 makers),
with rand.
Wrong answers come from real mistakes: forgetting the deposit, using simple interest for compound interest, and
multiplying instead of dividing when changing rand to another currency.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g7_financial_maths as zf7
adopt(zf7)
if isinstance(getattr(zf7, 'R', None), random.Random): zf7.R = random.Random(808020)
import gen_uk_maths_y8_percentage_change_and_interest as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(808021)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))


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


HP = [("a fridge", 6000, 12000), ("a lounge suite", 8000, 20000), ("a laptop", 5000, 12000), ("a washing machine", 4000, 9000), ("a TV", 3000, 9000), ("a bed", 3000, 8000)]


def one_hp(r):
    kk = Kid(r).next()
    what, lo, hi = r.choice(HP)
    cash = r.randint(lo // 100, hi // 100) * 100
    dep_p = r.choice([10, 15, 20, 25])
    dep = cash * dep_p // 100
    if cash * dep_p % 100:
        raise AssertionError
    n = r.choice([12, 18, 24, 36])
    inst = r.randint((cash - dep) // n // 10 + 2, (cash - dep) // n // 10 + 12) * 10
    total = dep + n * inst
    k = r.choice(["total", "extra", "dep"])
    base = "%s buys %s on hire purchase. The cash price is R%s. %s pays a %d%% deposit and %d monthly instalments of R%s." % (kk["n"], what, comma(cash), kk["He"], dep_p, n, comma(inst))
    if k == "dep":
        return mcq(base + " How much is the deposit?", "R" + comma(dep), ["R" + comma(cash - dep), "R" + comma(dep_p * 10), "R" + comma(inst)],
                   "%d%% of R%s = <b>R%s</b>." % (dep_p, comma(cash), comma(dep)))
    if k == "total":
        return mcq(base + " What is the total hire purchase price?", "R" + comma(total), ["R" + comma(n * inst), "R" + comma(cash), "R" + comma(cash + n * inst)],
                   "Deposit R%s + %d × R%s = R%s + R%s = <b>R%s</b>." % (comma(dep), n, comma(inst), comma(dep), comma(n * inst), comma(total)))
    return mcq(base + " How much more does %s pay than the cash price?" % kk["he"], "R" + comma(total - cash), ["R" + comma(total), "R" + comma(n * inst - cash) if n * inst != cash else "R0", "R" + comma(dep)],
               "Total: R%s + %d × R%s = R%s. R%s − R%s = <b>R%s</b>." % (comma(dep), n, comma(inst), comma(total), comma(total), comma(cash), comma(total - cash)))


CURR = [("euro", "euros", 20), ("Botswana pula", "pula", 1.4), ("Chinese yuan", "yuan", 2.5), ("Indian rupee", "rupees", 0.22), ("Japanese yen", "yen", 0.12)]


def one_fx(r):
    kk = Kid(r).next()
    name, plural, rate = r.choice(CURR)
    if r.random() < 0.5:
        amt = r.choice([50, 100, 200, 250, 400, 500, 1000, 2000]) if rate < 5 else r.choice([20, 50, 80, 120, 150, 300])
        v = amt * rate
        if abs(v - round(v, 2)) > 1e-9:
            raise AssertionError
        ans = rand(round(v, 2))
        q = "Suppose 1 %s = R%s. %s spends %s %s on holiday. How much is that in rand?" % (name, ("%g" % rate).replace(".", ","), kk["n"], comma(amt), plural)
        return mcq(q, ans, [rand(round(amt / rate, 2)), rand(round(v * 10, 2)), rand(round(v + rate, 2))],
                   "%s × R%s = <b>%s</b>." % (comma(amt), ("%g" % rate).replace(".", ","), ans))
    rand_amt = r.choice([200, 400, 500, 1000, 1500, 2000, 3000])
    v = rand_amt / rate
    if abs(v - round(v)) > 1e-9:
        raise AssertionError
    v = int(round(v))
    q = "Suppose 1 %s = R%s. How many %s do you get for R%s?" % (name, ("%g" % rate).replace(".", ","), plural, comma(rand_amt))
    return mcq(q, "%s %s" % (comma(v), plural), ["%s %s" % (comma(x), plural) for x in (int(round(rand_amt * rate)), v * 10, v + 10) if x != v],
               "R%s ÷ R%s = <b>%s %s</b>." % (comma(rand_amt), ("%g" % rate).replace(".", ","), comma(v), plural))


def one_ci(r):
    kk = Kid(r).next()
    P = r.choice([1000, 2000, 5000, 10000, 20000])
    i = r.choice([5, 10, 8, 6])
    n = r.choice([2, 3])
    A = P
    for _ in range(n):
        A = A * (100 + i) / 100
    A = round(A, 2)
    si = P + P * i * n // 100
    return mcq("%s invests R%s at %d%% compound interest per year. How much is in the account after %d years?" % (kk["n"], comma(P), i, n), rand(A),
               [rand(si), rand(round(A - P, 2)), rand(round(P * (1 + i / 100) * 1, 2))],
               "Multiply by 1,%02d each year: R%s × 1,%02d<sup>%d</sup> = <b>%s</b>. (Simple interest would give R%s.)" % (i, comma(P), i, n, rand(A), comma(si)))


def build():
    sets, R = build_sets([
        ("Simple interest", [("collect", zf7.uniq(zf7.one_si), 20)]),
        ("Compound interest", [("collect", uniq(one_ci), 10), ("collect", ukp.one_interest, 10)]),
        ("Hire purchase", [("collect", uniq(one_hp), 20)]),
        ("Exchange rates", [("collect", uniq(one_fx), 20)]),
        ("Percentage change", [("collect", ukp.one_change, 10), ("collect", ukp.one_reverse, 10)]),
    ], 80802)
    finish(sets, R)
    body = lesson('<ul><li>Simple interest is the same each year: I = P × r × n.</li><li>Compound interest adds interest on the interest: multiply by (1 + r) each year.</li><li>Hire purchase: total = deposit + all the instalments. It costs more than the cash price.</li><li>Exchange rate: 1 euro = R20 means multiply euros by 20 to get rand, and divide rand by 20 to get euros.</li></ul>',
        [example("R5 000 at 10% compound interest for 2 years", ["R5 000 × 1,1 = R5 500", "R5 500 × 1,1"], "R6 050")],
        [['Forgetting the deposit', 'Add the deposit to the instalments.'], ['Simple for compound', 'Compound grows on the new amount.'], ['× or ÷?', 'Rand to euros: divide by the rate.']])
    faq = [('What does CAPS Grade 8 say about financial maths?', 'Solve problems involving profit, loss, discount, VAT, budgets, loans, simple and compound interest, hire purchase and exchange rates.'), ('Why is hire purchase more expensive?', 'You pay interest on the money you borrow.'), ('Which earns more, simple or compound interest?', 'Compound interest, after the first year.'), ('What is a deposit?', 'The first payment made at the start.')]
    make('financial-maths', 2, 'Numbers, Operations and Relationships', 'Grade 8: 1.1 Whole numbers',
         'Solve problems that involve whole numbers, percentages and decimal fractions in financial contexts such as profit, loss, discount and VAT, budgets, accounts, loans, simple interest, hire purchase, exchange rates and compound interest.',
         'Financial Maths: Hire Purchase, Simple and Compound Interest, and Exchange Rates', 'Financial Maths',
         'Free CAPS Grade 8 financial maths worksheets: simple and compound interest, hire purchase, exchange rates and percentage change. 100 questions with memos.',
         'Compound interest: × (1 + r) every year.', 'Hire purchase: deposit + instalments.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
