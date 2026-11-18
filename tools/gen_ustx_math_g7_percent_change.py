# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Percent Increase, Decrease and Multi-Step Percent Problems (TEKS 7.4D)
  python3 tools/gen_ustx_math_g7_percent_change.py
Percent of a number, percent increase and decrease, discounts and markups, tax, tips and commission, and word
problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: dividing by the new amount, forgetting to subtract a discount, and adding
percents that act on different amounts.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_percent_problems as pp
adopt(pp)
pp.R = random.Random(670080)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Percent of a number", [("run", pp.set_percent_of, (), 20)]),
        ("Percent increase and decrease", [("run", pp.set_change, (), 20)]),
        ("Discounts and markups", [("run", pp.set_discount, (), 20)]),
        ("Tax, tips and commission", [("run", pp.set_tax_tip, (), 20)]),
        ("Multi-step word problems", [("run", pp.set_words, (), 20)]),
    ], 67008)
    finish(sets, R)
    body = lesson('<ul><li><b>Percent change</b> = change ÷ original amount × 100%.</li><li>An increase from 40 to 50 is 10 ÷ 40 = 25%.</li><li>A <b>discount</b> lowers the price: 25% off means you pay 75%. A <b>markup</b> raises it.</li><li>Tax and tips are added to the price.</li></ul>',
        [example("From 40 to 50", ["Change: 10", "10 ÷ 40"], "25% increase"), example("$80 jacket, 25% off", ["0.75 × 80"], "$60")],
        [['Dividing by the new amount', 'Always divide the change by the original amount.'], ['Forgetting to subtract the discount', 'The discount is taken off the price.'], ['Adding percents on different amounts', 'A 10% raise then 10% cut does not return to the start.']])
    faq = [('What does TEKS 7.4D ask?', 'Solve problems involving ratios, rates and percents, including multi-step problems involving percent increase and percent decrease, and financial literacy problems.'), ('What is the difference between percent increase and decrease?', 'An increase means the new amount is bigger; a decrease means it is smaller.'), ('How do I find a sale price in one step?', 'Multiply by 100% minus the discount: 25% off is × 0.75.'), ('What is commission?', 'Money a salesperson earns as a percent of sales.')]
    make('percent-increase-and-decrease', 8, 'Proportionality', '7.4D',
         '7.4D solve problems involving ratios, rates, and percents, including multi-step problems involving percent increase and percent decrease, and financial literacy problems',
         'Percent Increase, Decrease and Multi-Step Percent Problems', 'Percent Increase and Decrease',
         'Free Grade 7 percent worksheets for Texas TEKS 7.4D: percent of a number, percent increase and decrease, discounts, markups, tax, tips and multi-step problems. 100 questions with answers.',
         'Percent change = change ÷ original.', '40 to 50 is a 25% increase. 25% off means pay 75%.',
         body, faq, sets, seo_title='Grade 7 Percent Increase and Decrease Worksheets (TEKS 7.4D, STAAR)')


if __name__ == "__main__":
    build()
