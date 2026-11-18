# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Ratios and Rates (TEKS 6.4B, 6.4C, 6.4D)
  python3 tools/gen_ustx_math_g6_ratios_rates.py
Writing ratios from pictures, ratio language, equivalent ratios, unit rates and comparing rates (the US Grade 6
makers with Texas names).
Wrong answers come from real mistakes: writing the ratio in the wrong order, mixing up part-to-part and
part-to-whole, and dividing the wrong way for a unit rate.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_ratios as ra
import gen_us_math_g6_unit_rates as ur
adopt(ra)
adopt(ur)
tx_common.GRADE = "grade-6"

import re


def no_clock(it):
    """Ratios like 15:75 look like impossible clock times; skip them."""
    return not re.search(r"\b\d{1,2}:[6-9]\d\b", it["q"] + " ".join(it["c"]) + it["e"])


def build():
    sets, R = build_sets([
        ("Write a ratio from a picture", [("run", ra.set_pictures, ("rnd",), 20, no_clock)]),
        ("Ratio language and part-to-whole", [("run", ra.set_language, ("rnd",), 20, no_clock)]),
        ("Equivalent ratios and simplest form", [("run", ra.set_equivalent, ("rnd",), 20, no_clock)]),
        ("Find a unit rate", [("run", ur.set_whole, (ur.People,), 20)]),
        ("Compare rates: the better buy and the faster speed", [("run", ur.set_compare, (ur.People,), 20)]),
    ], 66007)
    finish(sets, R)
    body = lesson('<ul><li>A <b>ratio</b> compares two quantities by multiplication: 3 cats for every 5 dogs is 3 : 5.</li><li>The <b>order</b> matters: dogs to cats is 5 : 3.</li><li>A <b>rate</b> compares quantities with different units, such as 120 miles in 2 hours.</li><li>A <b>unit rate</b> is the amount for 1: 120 ÷ 2 = 60 miles per hour.</li></ul>',
        [example("$4.50 for 3 muffins", ["$4.50 ÷ 3"], "$1.50 per muffin"), example("Which is simpler, 12 : 18 or 2 : 3?", ["12 ÷ 6 = 2, 18 ÷ 6 = 3"], "2 : 3")],
        [['Writing the ratio in the wrong order', 'Follow the order of the words: trucks to cars.'], ['Mixing up part-to-part and part-to-whole', 'Part-to-whole uses the total.'], ['Dividing the wrong way for a unit rate', 'Divide by the quantity you want 1 of.']])
    faq = [('What does TEKS 6.4C ask?', 'Give examples of ratios as multiplicative comparisons of two quantities describing the same attribute.'), ('What does TEKS 6.4D ask?', 'Give examples of rates as the comparison by division of two quantities having different attributes, including rates as quotients.'), ('What is the difference between a ratio and a rate?', 'A rate compares quantities with different units, like miles and hours.'), ('How do I find the better buy?', 'Find the unit price of each and choose the lower one.')]
    make('ratios-and-rates', 7, 'Proportionality', '6.4B, 6.4C, 6.4D',
         '6.4B apply qualitative and quantitative reasoning to solve prediction and comparison of real-world problems involving ratios and rates; 6.4C give examples of ratios as multiplicative comparisons of two quantities describing the same attribute; 6.4D give examples of rates as the comparison by division of two quantities having different attributes, including rates as quotients',
         'Ratios and Rates', 'Ratios and Rates',
         'Free Grade 6 ratio and rate worksheets for Texas TEKS 6.4B, 6.4C and 6.4D: write ratios, ratio language, equivalent ratios, unit rates and better buys. 100 questions with answers.',
         'A ratio compares two quantities; a unit rate is the amount for 1.', '3 : 5 is not the same as 5 : 3. $4.50 for 3 is $1.50 each.',
         body, faq, sets, seo_title='Grade 6 Ratios and Rates Worksheets: Unit Rates and Better Buys (TEKS 6.4, STAAR)')


if __name__ == "__main__":
    build()
