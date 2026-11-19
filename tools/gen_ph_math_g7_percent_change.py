# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Percentage Increase and Decrease (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_percent_change.py
Increasing and decreasing an amount by a percentage, multipliers, finding the percentage change, finding the original
amount (UK Year 7 and Year 8 makers with pesos), and Philippine word problems (own maker).
Wrong answers come from real mistakes: dividing the change by the new amount, finding the change but not the new
amount, and taking the percentage of the new price to undo a change.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y7_percentages_of_amounts as uk7
adopt(uk7)
if hasattr(uk7, 'R'): uk7.R = random.Random(707040)
import gen_uk_maths_y8_percentage_change_and_interest as uk8
adopt(uk8)
if hasattr(uk8, 'R'): uk8.R = random.Random(707041)
uk8.money = peso
uk7.money = peso
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


from fractions import Fraction as F

CHANGES = [("The enrollment of a school went from %(a)s to %(b)s learners.", "learners"), ("The price of a kilo of rice went from %(a)s to %(b)s.", "peso"),
           ("A town's population went from %(a)s to %(b)s.", "people"), ("A jeepney fare went from %(a)s to %(b)s.", "peso"),
           ("A farm's mango harvest went from %(a)s kg to %(b)s kg.", "kg"), ("Monthly visitors to a museum in Cebu went from %(a)s to %(b)s.", "people")]


def one_pch(r):
    t, u = r.choice(CHANGES)
    a = r.choice({"learners": [400, 500, 600, 800, 1200, 1500], "peso": [40, 50, 60, 80], "people": [2000, 5000, 8000, 12000, 20000],
                  "kg": [200, 400, 500, 800]}[u])
    p = r.choice([5, 10, 15, 20, 25, 30, 40, 50])
    up = r.random() < 0.55
    b = F(a * (100 + p if up else 100 - p), 100)
    if b.denominator != 1 or (u == "peso" and a == 40 and p in (15,)):
        raise AssertionError
    b = int(b)
    fmt = peso if u == "peso" else comma
    q = (t % {"a": fmt(a), "b": fmt(b)}) + " What is the percentage %s?" % ("increase" if up else "decrease")
    ch = abs(b - a)
    wr = [F(ch * 100, b), F(ch), F(b * 100, a)]
    wr = ["%s%%" % ("%g" % float(w)) for w in wr if w.denominator in (1, 2, 4)]
    return mcq(q, "%d%%" % p, [w for w in wr if w != "%d%%" % p] + ["%d%%" % (p + 5)],
               "Change: %s − %s = %s. Percentage %s = change ÷ original × 100 = %s ÷ %s × 100 = <b>%d%%</b>." % (comma(max(a, b)), comma(min(a, b)), comma(ch), "increase" if up else "decrease", comma(ch), comma(a), p))


def build():
    sets, R = build_sets([
        ("Increase or decrease an amount", [("collect", uk7.one_change, 20)]),
        ("Multipliers", [("collect", uk8.one_mult, 20)]),
        ("Find the percentage change", [("collect", uk8.one_change, 20)]),
        ("Find the original amount", [("collect", uk8.one_reverse, 20)]),
        ("Percentage change problems", [("collect", uniq(one_pch), 20)]),
    ], 70704)
    finish(sets, R)
    body = lesson('<ul><li><b>Percentage change</b> = change ÷ original amount × 100%.</li><li>To increase by 15%, multiply by 1.15 (100% + 15%). To decrease by 15%, multiply by 0.85 (100% − 15%).</li><li>To find the original amount, divide the new amount by the multiplier.</li><li>Always compare the change with the <b>original</b> amount.</li></ul>',
        [example("₱50 to ₱60", ["change ₱10", "10 ÷ 50 × 100"], "20% increase"), example("₱680 after a 15% decrease", ["680 ÷ 0.85"], "₱800 originally")],
        [['Dividing by the new amount', 'Divide the change by the original amount.'], ['Stopping at the change', 'Add or subtract the change to get the new amount.'], ['Undoing with the same percent', 'A 20% increase is not undone by a 20% decrease.']])
    faq = [('What does MATATAG Math 7 ask about percentage change?', 'Solve problems involving percentage increase and percentage decrease.'), ('What is a multiplier?', 'The decimal you multiply by to make a percentage change in one step.'), ('Can a percentage increase be more than 100%?', 'Yes. Doubling is a 100% increase.'), ('How do I find the original price?', 'Divide the new price by the multiplier.')]
    make('percentage-increase-and-decrease', 4, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Solve problems involving: a. percentage increase, and b. percentage decrease.',
         'Percentage Increase and Decrease', 'Percentage Increase and Decrease',
         'Free Grade 7 percentage increase and decrease worksheets for the DepEd MATATAG curriculum: multipliers, percentage change, original amounts and word problems with pesos. 100 questions with answers.',
         'Percentage change = change ÷ original × 100%.', 'Increase 15%: × 1.15. Decrease 15%: × 0.85.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
