# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Odd and Even Numbers to 40 (TEKS 2.7A)
  python3 tools/gen_ustx_math_g2_odd_even.py
Pairing objects, the ones digit, doubles, sums of odd and even numbers, and stories (the US Grade 2 makers with
Texas names).
Wrong answers come from real mistakes: looking at the tens digit, thinking 0 is odd, and counting one object
twice.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_odd_even as oe
adopt(oe)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Make pairs", [("run", oe.set_pairs, (oe.People, "rnd"), 20)]),
        ("Look at the ones digit", [("run", oe.set_ones_digit, (oe.People,), 20)]),
        ("Doubles are even", [("run", oe.set_doubles, (oe.People,), 20)]),
        ("Sums of equal numbers", [("run", oe.set_sums, (oe.People,), 20)]),
        ("Odd and even stories", [("run", oe.set_stories, (oe.People,), 20)]),
    ], 69209)
    finish(sets, R)
    body = lesson('<ul><li>Put objects in <b>pairs</b>. If every object has a partner, the number is <b>even</b>. If one is left over, it is <b>odd</b>.</li><li>Even numbers end in 0, 2, 4, 6 or 8. Odd numbers end in 1, 3, 5, 7 or 9.</li><li>A double, like 9 + 9, is always even.</li></ul>',
        [example("Is 27 odd or even?", ["Ones digit is 7"], "odd"), example("Is 34 odd or even?", ["17 pairs, none left over"], "even")],
        [['Looking at the tens digit', 'Only the ones digit tells odd or even.'], ['Thinking 0 is odd', '0 is even.'], ['Counting an object twice', 'Cross out each pair as you count.']])
    faq = [('What does TEKS 2.7A ask?', 'Determine whether a number up to 40 is even or odd using pairings of objects to represent the number.'), ('Is 0 even?', 'Yes. 0 has no object left over.'), ('Is every double even?', 'Yes. A double makes pairs with nothing left over.'), ('How can I check quickly?', 'Look at the ones digit.')]
    make('odd-and-even-numbers', 9, 'Algebraic Reasoning', '2.7A',
         '2.7A determine whether a number up to 40 is even or odd using pairings of objects to represent the number',
         'Odd and Even Numbers to 40', 'Odd and Even Numbers',
         'Free Grade 2 odd and even worksheets for Texas TEKS 2.7A: pairing objects, the ones digit, doubles, sums and stories. 100 questions with answers.',
         'Even: every object has a partner. Odd: one is left over.', 'Even numbers end in 0, 2, 4, 6 or 8.',
         body, faq, sets, seo_title='Grade 2 Odd and Even Numbers Worksheets (TEKS 2.7A)')


if __name__ == "__main__":
    build()
