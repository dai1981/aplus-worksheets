# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Financial Maths: Profit and Loss, Discount, VAT, Budgets and Simple Interest (Grade 7: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g7_financial_maths.py
Profit and loss, discount, VAT at 15%, budgets and simple interest (own makers with rand and South African prices).
Wrong answers come from real mistakes: giving the profit for one item instead of all, adding the discount instead of
subtracting it, and adding only one year of interest.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)

za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))


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


STOCK = [("cooldrinks", 6, 12), ("vetkoek", 4, 9), ("T-shirts", 60, 140), ("phone covers", 35, 90), ("beaded bracelets", 15, 45), ("bags of oranges", 18, 40), ("school socks", 12, 30)]


def one_pl(r):
    kk = Kid(r).next()
    what, lo, hi = r.choice(STOCK)
    n = r.randint(10, 60)
    cp = r.randint(lo, hi)
    sp = cp + r.choice([-3, -2, 2, 3, 4, 5, 8, 10]) * (1 if hi < 50 else 3)
    if sp <= 0:
        raise AssertionError
    tc, ts = n * cp, n * sp
    d = ts - tc
    word = "profit" if d > 0 else "loss"
    q = "%s buys %d %s for R%s each and sells them all for R%s each. What is the %s?" % (kk["n"], n, what, comma(cp), comma(sp), "profit or loss")
    right = "a %s of R%s" % (word, comma(abs(d)))
    other = "a %s of R%s" % ("loss" if d > 0 else "profit", comma(abs(d)))
    return mcq(q, right, [other, "a %s of R%s" % (word, comma(abs(sp - cp))), "a %s of R%s" % (word, comma(ts))],
               "Cost: %d × R%s = R%s. Income: %d × R%s = R%s. R%s − R%s = %sR%s, so <b>%s</b>." % (n, comma(cp), comma(tc), n, comma(sp), comma(ts), comma(ts), comma(tc), "−" if d < 0 else "", comma(abs(d)), right))


GOODS7 = [("a pair of takkies", 400, 1200), ("a school blazer", 450, 900), ("a microwave", 1200, 2500), ("a cellphone", 1500, 6000), ("a bicycle", 1800, 5000), ("a fridge", 4000, 9000)]


def one_vat(r):
    what, lo, hi = r.choice(GOODS7)
    p = r.randint(lo // 20, hi // 20) * 20
    v = p * 15 // 100
    if p * 15 % 100:
        raise AssertionError
    if r.random() < 0.5:
        return mcq("%s costs R%s before VAT. VAT is 15%%. What is the price including VAT?" % (what[0].upper() + what[1:], comma(p)), "R" + comma(p + v), ["R" + comma(v), "R" + comma(p + 15), "R" + comma(p - v)],
                   "15%% of R%s = R%s. R%s + R%s = <b>R%s</b>." % (comma(p), comma(v), comma(p), comma(v), comma(p + v)))
    return mcq("How much VAT (15%%) is added to %s that costs R%s before VAT?" % (what, comma(p)), "R" + comma(v), ["R" + comma(p + v), "R" + comma(p // 10), "R15"],
               "10%% of R%s = R%s and 5%% = R%s. 15%% = <b>R%s</b>." % (comma(p), comma(p // 10), comma(p // 20), comma(v)))


def one_si(r):
    kk = Kid(r).next()
    P = r.choice([500, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000, 5000])
    i = r.choice([4, 5, 6, 8, 10, 12])
    n = r.randint(2, 5)
    I = P * i * n // 100
    if P * i * n % 100:
        raise AssertionError
    if r.random() < 0.5:
        return mcq("%s saves R%s at %d%% simple interest per year. How much interest does %s earn in %d years?" % (kk["n"], comma(P), i, kk["he"], n), "R" + comma(I), ["R" + comma(P * i // 100), "R" + comma(P + I), "R" + comma(P * i * n // 10)],
                   "One year: %d%% of R%s = R%s. %d years: %d × R%s = <b>R%s</b>." % (i, comma(P), comma(P * i // 100), n, n, comma(P * i // 100), comma(I)))
    return mcq("%s borrows R%s at %d%% simple interest per year for %d years. How much must %s pay back in total?" % (kk["n"], comma(P), i, n, kk["he"]), "R" + comma(P + I), ["R" + comma(I), "R" + comma(P + P * i // 100), "R" + comma(P + I * 2)],
               "Interest: %d × %d%% of R%s = R%s. Total: R%s + R%s = <b>R%s</b>." % (n, i, comma(P), comma(I), comma(P), comma(I), comma(P + I)))


def one_budget(r):
    kk = Kid(r).next()
    inc = r.choice([800, 1000, 1200, 1500, 2000])
    items = r.sample([("data", 99, 249), ("transport", 150, 400), ("lunch", 120, 350), ("airtime", 30, 100), ("savings", 100, 300), ("clothes", 150, 400), ("a gift", 80, 200)], 3)
    vals = [r.randint(a // 10, b // 10) * 10 for _, a, b in items]
    left = inc - sum(vals)
    if left <= 0:
        raise AssertionError
    q = "%s earns R%s a month. %s budget: %s. How much is left for other things?" % (kk["n"], comma(inc), kk["His"], ", ".join("%s R%s" % (n, comma(v)) for (n, _, _), v in zip(items, vals)))
    return mcq(q, "R" + comma(left), ["R" + comma(sum(vals)), "R" + comma(left + vals[-1]), "R" + comma(left - 10)],
               "R%s − (R%s) = R%s − R%s = <b>R%s</b>." % (comma(inc), " + R".join(comma(v) for v in vals), comma(inc), comma(sum(vals)), comma(left)))


def one_disc7(r):
    what, lo, hi = r.choice(GOODS7)
    p = r.randint(lo // 50, hi // 50) * 50
    pc = r.choice([10, 15, 20, 25, 30, 40])
    d = p * pc // 100
    if p * pc % 100:
        raise AssertionError
    return mcq("%s is marked R%s. The shop gives a discount of %d%%. What is the new price?" % (what[0].upper() + what[1:], comma(p), pc), "R" + comma(p - d), ["R" + comma(d), "R" + comma(p - pc), "R" + comma(p + d)],
               "%d%% of R%s = R%s. R%s − R%s = <b>R%s</b>." % (pc, comma(p), comma(d), comma(p), comma(d), comma(p - d)))


def build():
    sets, R = build_sets([
        ("Profit and loss", [("collect", uniq(one_pl), 20)]),
        ("Discount", [("collect", uniq(one_disc7), 20)]),
        ("VAT", [("collect", uniq(one_vat), 20)]),
        ("Budgets", [("collect", uniq(one_budget), 20)]),
        ("Simple interest", [("collect", uniq(one_si), 20)]),
    ], 80705)
    finish(sets, R)
    body = lesson('<ul><li>Profit = income − cost. If the answer is negative, it is a loss.</li><li>Discount: subtract the percentage from the price.</li><li>VAT in South Africa is 15%: add 15% to the price before VAT.</li><li>Simple interest = principal × rate × years: R2 000 at 8% for 3 years = R480.</li></ul>',
        [example("R2 000 at 8% simple interest for 3 years", ["8% of R2 000 = R160", "3 × R160"], "R480 interest")],
        [['One item only', 'Multiply by the number of items.'], ['Adding the discount', 'Discount makes the price smaller.'], ['One year of interest', 'Multiply by the number of years.']])
    faq = [('What does CAPS Grade 7 say about financial maths?', 'Solve problems involving profit, loss, discount and VAT, budgets, accounts, loans and simple interest.'), ('What is VAT?', 'Value-added tax, 15% in South Africa.'), ('What is the principal?', 'The amount you save or borrow.'), ('Is simple interest the same every year?', 'Yes.')]
    make('financial-maths', 5, 'Numbers, Operations and Relationships', 'Grade 7: 1.1 Whole numbers',
         'Solve problems that involve whole numbers, percentages and decimal fractions in financial contexts such as profit, loss, discount and VAT, budgets, accounts, loans and simple interest.',
         'Financial Maths: Profit and Loss, Discount, VAT, Budgets and Simple Interest', 'Financial Maths',
         'Free CAPS Grade 7 financial maths worksheets: profit and loss, discount, VAT at 15%, budgets and simple interest. 100 questions with memos.',
         'Profit = income − cost.', 'Simple interest = P × r × n.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
