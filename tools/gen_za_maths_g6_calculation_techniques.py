# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Calculation Techniques: Estimating, Compensating, Doubling and Halving (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_calculation_techniques.py
Rounding off and compensating, doubling and halving (makers from the Grade 4 generator), estimating products and
quotients and judging answers (Australia Year 6 makers).
Wrong answers come from real mistakes: compensating the wrong way, rounding only one number, and accepting an answer
that is far from the estimate.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_calculation_techniques as zc4
adopt(zc4)
if isinstance(getattr(zc4, 'R', None), random.Random): zc4.R = random.Random(806040)
import gen_au_maths_y6_estimation as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(806041)
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


def _r1(n):
    p = 10 ** (len(str(n)) - 1)
    return (n + p // 2) // p * p


def one_estw(r):
    kk = Kid(r).next()
    k = r.choice(["mul", "div", "add"])
    if k == "mul":
        a, b = r.randint(21, 98), r.randint(102, 989)
        t = r.choice(["A school orders %d boxes of %d pencils. About how many pencils is that?", "%d buses each carry %d kg of luggage. About how much luggage is that in kilograms?", "A farmer packs %d crates with %d oranges each. About how many oranges is that?"])
        q = t % (a, b) if "%d boxes" in t or "crates" in t else t % (a, b)
        est = _r1(a) * _r1(b)
        return mcq(q, comma(est), [comma(est * 10), comma(est // 10), comma(_r1(a) + _r1(b))], "%d is about %d and %d is about %s. %d × %s = <b>%s</b>." % (a, _r1(a), b, comma(_r1(b)), _r1(a), comma(_r1(b)), comma(est)))
    if k == "div":
        b = r.choice([20, 30, 40, 50, 60, 80])
        q0 = r.randint(11, 99)
        n = b * _r1(q0) + r.randint(-b * 2, b * 2)
        est = _r1(n) // b if _r1(n) % b == 0 else None
        if not est or n < 1000:
            raise AssertionError
        m = b + r.choice([-2, -1, 1, 2])
        q = "%s shares %s sweets equally among %d learners. About how many sweets does each learner get?" % (kk["n"], comma(n), m)
        return mcq(q, comma(est), [comma(est * 10), comma(est // 10) if est >= 20 else comma(est + 50), comma(_r1(n) - b)], "%s is about %s and %d is about %d. %s ÷ %d = <b>%s</b>." % (comma(n), comma(_r1(n)), m, b, comma(_r1(n)), b, comma(est)))
    a, b = r.randint(10000, 99999), r.randint(10000, 99999)
    q = "A stadium had %s people on Saturday and %s on Sunday. About how many people is that altogether (round to the nearest 10 000)?" % (comma(a), comma(b))
    ra, rb = (a + 5000) // 10000 * 10000, (b + 5000) // 10000 * 10000
    est = ra + rb
    return mcq(q, comma(est), [comma(est + 10000), comma(est - 10000), comma(a + b)], "%s is about %s and %s is about %s. Total about <b>%s</b>." % (comma(a), comma(ra), comma(b), comma(rb), comma(est)))


def build():
    sets, R = build_sets([
        ("Rounding off and compensating", [("collect", zc4.uniq(zc4.one_comp), 20)]),
        ("Doubling and halving", [("collect", zc4.uniq(zc4.one_dh), 20)]),
        ("Estimate answers", [("run", aue.set_est, (), 20, nine)]),
        ("Is the answer reasonable?", [("run", aue.set_reasonable, (aue.People,), 20, nine)]),
        ("Estimation problems", [("collect", uniq(one_estw), 20)]),
    ], 80604)
    finish(sets, R)
    body = lesson('<ul><li>Round off and compensate: 4 999 + 2 367 = 5 000 + 2 367 − 1.</li><li>Double and halve: 50 × 48 = 100 × 24 = 2 400.</li><li>Estimate a product by rounding both numbers: 398 × 51 is about 400 × 50 = 20 000.</li><li>If your answer is far from the estimate, check again.</li></ul>',
        [example("6 012 − 2 998", ["6 012 − 3 000 = 3 012", "add back 2"], "3 014")],
        [['Compensating the wrong way', 'You took away too much, so add it back.'], ['Rounding one number only', 'Round both numbers.'], ['Ignoring the estimate', 'Compare your answer with it.']])
    faq = [('What does CAPS Grade 6 say about calculation techniques?', 'Use estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, a number line, and inverse operations.'), ('When is doubling and halving useful?', 'When one number halves to an easy number, like 25 × 36 = 50 × 18.'), ('Is an estimate the answer?', 'No, it is close to the answer.'), ('How do I estimate 49 × 61?', '50 × 60 = 3 000.')]
    make('calculation-techniques', 4, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Use a range of techniques to perform and check written and mental calculations of whole numbers, including estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, using a number line, and using addition and subtraction as well as multiplication and division as inverse operations.',
         'Calculation Techniques: Estimating, Compensating, Doubling and Halving', 'Calculation Techniques',
         'Free CAPS Grade 6 mental maths worksheets: rounding off and compensating, doubling and halving, estimating and checking answers. 100 questions with memos.',
         'Round off, calculate, then compensate.', 'Compare every answer with an estimate.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
