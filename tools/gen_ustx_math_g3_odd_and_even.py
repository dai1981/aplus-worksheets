# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Odd and Even Numbers (TEKS 3.4I)
  python3 tools/gen_ustx_math_g3_odd_and_even.py
Odd or even by pairing and by the ones digit (the divisibility rule for 2), patterns on number lines, rules for
sums, differences and products, predicting odd or even without calculating, and word problems. The question
makers come from the Australian Year 4 odd and even unit, with Texas names, US spelling and new numbers.
Wrong answers come from real mistakes: looking at the first digit instead of the ones digit, thinking an odd
number plus an odd number is odd, and thinking every product with an odd factor is odd.
"""
import random
from tx_common import (mcq, finish, make, figure, lesson, S, run, adopt, People, example)
import gen_au_maths_y4_odd_even as au

adopt(au)
au.People = People
R = random.Random(61001)


def build():
    sets = [S("Odd or even? Look at the ones digit", run(au.set_odd_even, "rnd", seed=111)["items"]),
            S("Patterns and number lines", run(au.set_patterns, "rnd", seed=112)["items"]),
            S("Odd and even rules for +, − and ×", run(au.set_rules, "rnd", seed=113)["items"]),
            S("Predict odd or even without calculating", run(au.set_predict, "rnd", seed=114)["items"]),
            S("Odd and even word problems", run(au.set_words, People, seed=115)["items"])]
    finish(sets, R)
    body = lesson(
        "<ul><li>An <b>even</b> number can be split into 2 equal groups, or into pairs with none left over: 0, 2, 4, 6, 8 …</li>"
        "<li>An <b>odd</b> number always has 1 left over when you make pairs: 1, 3, 5, 7, 9 …</li>"
        "<li><b>Divisibility rule for 2</b>: look only at the ones digit. If it is 0, 2, 4, 6 or 8, the number is even. 3,578 is even because 8 is even.</li>"
        "<li>even + even = even, odd + odd = even, odd + even = odd. A product is odd only when both factors are odd.</li></ul>",
        [example("Is 4,671 odd or even?", ["Look at the ones digit: 1.", "1 is odd."], "4,671 is odd"),
         example("Is 37 + 25 odd or even?", ["37 is odd and 25 is odd.", "odd + odd = even (37 + 25 = 62)"], "even")],
        [["Looking at the first digit: 8,325 is even", "Only the ones digit decides. 5 is odd, so 8,325 is odd."],
         ["Thinking odd + odd = odd", "The two left-over ones make a pair: odd + odd = even."],
         ["Thinking a product is odd if one factor is odd", "3 × 4 = 12 is even. Both factors must be odd for an odd product."]])
    faq = [("What does TEKS 3.4I ask?", "Determine if a number is even or odd using divisibility rules."),
           ("What is the divisibility rule for 2?", "A whole number is divisible by 2 (even) when its ones digit is 0, 2, 4, 6 or 8."),
           ("Is 0 even or odd?", "0 is even. It can be split into 2 equal groups of 0, and its ones digit is 0."),
           ("Why learn odd and even?", "It helps with skip counting, sharing equally, checking answers and spotting patterns in a hundreds chart.")]
    make("odd-and-even-numbers", 10, "Number and Operations", "3.4I",
         "3.4I determine if a number is even or odd using divisibility rules",
         "Odd and Even Numbers: The Divisibility Rule for 2", "Odd and Even Numbers",
         "Free Grade 3 odd and even worksheets for Texas TEKS 3.4I: odd or even by the ones digit, number line patterns, rules for sums and products, predicting without calculating and word problems. 100 questions with answers.",
         "Look at the ones digit: 0, 2, 4, 6, 8 means even.", "odd + odd = even. A product is odd only when both factors are odd.",
         body, faq, sets, seo_title="Grade 3 Odd and Even Numbers Worksheets: Divisibility Rule (TEKS 3.4I, STAAR)")


if __name__ == "__main__":
    build()
