# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Describing the Rule of a Simple Pattern (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_patterns.py
Using a rule to extend a pattern, finding the rule and the missing number, growing shape patterns, odd and even
features of patterns, and input-output tables and word problems (US Grade 4 makers with Filipino names).
Wrong answers come from real mistakes: using only the first two numbers to find the rule, adding when the pattern
multiplies, and counting the figures wrong.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_patterns as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(704230)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Use a rule", [("run", usp.set_extend, ("rnd",), 20)]),
        ("Find the rule", [("run", usp.set_find_rule, ("rnd",), 20)]),
        ("Growing shape patterns", [("run", usp.set_shapes, ("rnd",), 20)]),
        ("Odd and even in patterns", [("run", usp.set_features, ("rnd", usp.People), 20)]),
        ("Tables and word problems", [("run", usp.set_words, ("rnd", usp.People), 20)]),
    ], 70423)
    finish(sets, R)
    body = lesson('<ul><li>A <b>pattern</b> follows a rule. The rule tells how to get the next term.</li><li>To find the rule, look at how each number changes to the next: add, subtract, multiply or divide by the same number?</li><li>Check the rule on <b>every</b> pair of numbers, not only the first two.</li><li>In a growing shape pattern, count what is added each time.</li></ul>',
        [example("3, 7, 11, 15, …", ["7 − 3 = 4, 11 − 7 = 4, 15 − 11 = 4"], "Rule: add 4. Next: 19"), example("2, 6, 18, 54, …", ["2 × 3 = 6, 6 × 3 = 18"], "Rule: multiply by 3")],
        [['Using only two numbers', '2, 6 could be add 4 or times 3. Check the next pair.'], ['Adding when it multiplies', 'Look at how fast the numbers grow.'], ['Miscounting figures', 'Count what is new in each figure.']])
    faq = [('What does MATATAG Math 4 ask about patterns?', 'Describe the rule used to generate a given simple pattern.'), ('What is a term?', 'Each number or figure in a pattern.'), ('Can a pattern go down?', 'Yes, when the rule subtracts or divides.'), ('How do I find a missing term?', 'Find the rule from the terms you know, then use it.')]
    make('patterns', 23, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Describe the rule used to generate a given simple pattern.',
         'Describing the Rule of a Simple Pattern', 'Patterns',
         'Free Grade 4 pattern worksheets for the DepEd MATATAG curriculum: find and use the rule, missing numbers, growing shape patterns and input-output tables. 100 questions with answers.',
         'Find the change from each term to the next.', 'Check the rule on every pair.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
