# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: The Equal Sign and Missing Numbers (TEKS 1.5E, 1.5F)
  python3 tools/gen_ustx_math_g1_equal_sign.py
What the equal sign means, true or false number sentences, missing numbers on either side, and stories (the US
Grade 1 makers with Texas names).
Wrong answers come from real mistakes: thinking = means the answer comes next, adding all the numbers, and
reading 8 = 3 + 5 as false.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_equal_sign as eq
adopt(eq)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("“=” means “the same as”", [("run", eq.set_same_as, (eq.People,), 20)]),
        ("True or false?", [("run", eq.set_true_false, (eq.People,), 20)]),
        ("Find the missing number", [("run", eq.set_right_middle, (eq.People,), 20)]),
        ("Missing number on either side", [("run", eq.set_left_both, (eq.People,), 20)]),
        ("Word problems with a missing number", [("run", eq.set_stories, (eq.People,), 20)]),
    ], 69112)
    finish(sets, R)
    body = lesson('<ul><li>The <b>equal sign</b> means both sides have the <b>same value</b>.</li><li>8 = 3 + 5 is true. 4 + 4 = 3 + 5 is true too.</li><li>To find a missing number, make both sides the same: 6 + ☐ = 10, so ☐ = 4.</li></ul>',
        [example("4 + ☐ = 3 + 6", ["3 + 6 = 9", "4 + 5 = 9"], "5")],
        [['Thinking = means “the answer is next”', '= means the same as.'], ['Adding all the numbers', '4 + ☐ = 3 + 6 is not 13.'], ['Calling 8 = 3 + 5 false', 'The total can be on the left.']])
    faq = [('What does TEKS 1.5E ask?', 'Understand that the equal sign represents a relationship where expressions on each side of the equal sign represent the same value(s).'), ('What does TEKS 1.5F ask?', 'Determine the unknown whole number in an addition or subtraction equation when the unknown may be any one of the three or four terms in the equation.'), ('Is 5 = 5 true?', 'Yes. Both sides are 5.'), ('How do you find the missing number?', 'Make both sides equal.')]
    make('equal-sign-and-missing-numbers', 12, 'Algebraic Reasoning', '1.5E, 1.5F',
         '1.5E understand that the equal sign represents a relationship where expressions on each side of the equal sign represent the same value(s); 1.5F determine the unknown whole number in an addition or subtraction equation when the unknown may be any one of the three or four terms in the equation',
         'The Equal Sign and Missing Numbers', 'Equal Sign and Missing Numbers',
         'Free Grade 1 worksheets for Texas TEKS 1.5E and 1.5F: the meaning of the equal sign, true or false number sentences and missing numbers. 100 questions with answers.',
         '= means both sides have the same value.', '4 + 5 = 3 + 6',
         body, faq, sets, seo_title='Grade 1 Equal Sign and Missing Numbers Worksheets (TEKS 1.5E)')


if __name__ == "__main__":
    build()
