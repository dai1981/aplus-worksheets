# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Rates and Speed (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_rates.py
Unit rates, best buys, speed, distance and time, and converting rates (Australia Year 8 and UK Year 8 makers with
Filipino names and pesos).
Wrong answers come from real mistakes: dividing the wrong way, mixing minutes and hours, and comparing total prices
instead of unit prices.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y8_rates as aur
adopt(aur)
if hasattr(aur, 'R'): aur.R = random.Random(707070)
import gen_uk_maths_y8_speed_distance_and_time as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(707071)
if hasattr(aur, 'money'): aur.money = peso
ph_common.GRADE = "grade-7"

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


GOODS = [("rice", "kg", [(2, 104), (5, 250), (10, 480), (25, 1150)]), ("cooking oil", "L", [(1, 95), (2, 180), (4, 340)]),
         ("shampoo", "mL", [(12, 7), (170, 95), (340, 175), (680, 330)]), ("coffee", "g", [(25, 12), (100, 45), (200, 85)]),
         ("laundry soap", "g", [(70, 9), (500, 60), (1000, 115)])]


def one_best(r):
    name, u, sizes = r.choice(GOODS)
    (a, pa), (b, pb) = sorted(r.sample(sizes, 2))
    pa = pa + r.randint(-3, 3)
    pb = pb + r.randint(-5, 5)
    ua, ub = pa / a, pb / b
    if abs(ua - ub) / min(ua, ub) < 0.03:
        raise AssertionError
    A, B_ = "%s %s for %s" % (comma(a), u, peso(pa)), "%s %s for %s" % (comma(b), u, peso(pb))
    better = A if ua < ub else B_
    base = {"kg": 1, "L": 1, "mL": 100, "g": 100}[u]
    show = lambda p_, s_: peso(round(p_ / s_ * base, 2))
    q = "Which is the better buy of %s: %s, or %s?" % (name, A, B_)
    return mcq(q, better, [B_ if better == A else A, "They are the same value", "You cannot tell without more information"],
               "Compare the price per %s%s: %s and %s. <b>%s</b> costs less per unit." % ("" if base == 1 else "%d " % base, u, show(pa, a), show(pb, b), better))


def build():
    sets, R = build_sets([
        ("Unit rates", [("collect", aur.one_unit, 20)]),
        ("Best buys", [("collect", uniq(one_best), 20)]),
        ("Find the speed", [("collect", uks.one_speed, 20)]),
        ("Distance and time", [("collect", uks.one_dt, 20)]),
        ("Converting rates", [("collect", aur.one_conv, 10), ("collect", uks.one_units, 10)]),
    ], 70707)
    finish(sets, R)
    body = lesson('<ul><li>A <b>rate</b> compares two quantities with different units: ₱/kg, km/h, words per minute.</li><li>A <b>unit rate</b> is the amount for 1 unit: ₱150 for 3 kg is ₱50 per kg.</li><li>Speed = distance ÷ time. Distance = speed × time. Time = distance ÷ speed.</li><li>Change minutes to hours before using km/h: 30 minutes = 0.5 hour.</li></ul>',
        [example("120 km in 1.5 hours", ["120 ÷ 1.5"], "80 km/h"), example("₱255 for 3 kg", ["255 ÷ 3"], "₱85 per kg")],
        [['Dividing the wrong way', 'Speed = distance ÷ time, not time ÷ distance.'], ['Minutes as hours', '45 minutes = 0.75 hour.'], ['Comparing totals', 'Compare the price for the same amount.']])
    faq = [('What does MATATAG Math 7 ask about rates?', 'Identify and explain the uses of rates, and solve problems involving rates (for example, speed).'), ('What is the difference between a ratio and a rate?', 'A rate compares quantities with different units.'), ('What are uses of rates?', 'Prices per kilo, speed, typing speed, heart rate, data plans.'), ('How do I change m/s to km/h?', 'Multiply by 3.6.')]
    make('rates-and-speed', 7, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Identify and explain the uses of rates; solve problems involving rates (e.g., speed).',
         'Rates and Speed', 'Rates and Speed',
         'Free Grade 7 rates worksheets for the DepEd MATATAG curriculum: unit rates, best buys, speed, distance and time and converting rates. 100 questions with answers.',
         'Speed = distance ÷ time.', 'Unit rate: the amount for 1 unit.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
