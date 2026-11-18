# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Adding and Subtracting Fractions with Unlike Denominators (TEKS 5.3H, 5.3K)
  python3 tools/gen_ustx_math_g5_add_subtract_fractions.py
Common denominators, adding and subtracting fractions and mixed numbers with unlike denominators, and word
problems with estimates. The question makers come from the US Grade 5 fraction unit with Texas names.
Wrong answers come from real mistakes: adding the denominators, renaming only one fraction, and not simplifying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_add_sub_fractions as usf
adopt(usf)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Find a common denominator", [("run", usf.set_common, ("rnd",), 20)]),
        ("Add fractions with unlike denominators", [("run", usf.set_add, ("rnd", usf.People), 20)]),
        ("Subtract fractions with unlike denominators", [("run", usf.set_subtract, ("rnd", usf.People), 20)]),
        ("Add and subtract mixed numbers", [("run", usf.set_mixed, ("rnd",), 20)]),
        ("Word problems and estimating", [("run", usf.set_words, ("rnd", usf.People), 20)]),
    ], 65008)
    finish(sets, R)
    body = lesson('<ul><li>Fractions can be added or subtracted only when the pieces are the same size. Rename both fractions with a <b>common denominator</b>.</li><li>Then add or subtract the numerators and keep the denominator: 1/3 + 1/4 = 4/12 + 3/12 = 7/12.</li><li>For mixed numbers, rename the fractions, then add or subtract wholes and fractions. Regroup when needed and simplify.</li><li>Estimate with 0, 1/2 and 1 to check.</li></ul>',
        [example("2/3 + 1/4", ["Common denominator 12", "8/12 + 3/12"], "11/12"), example("3 1/4 − 1 2/3", ["3 3/12 − 1 8/12", "Regroup: 2 15/12 − 1 8/12"], "1 7/12")],
        [['Adding the denominators: 1/3 + 1/4 = 2/7', 'Rename with a common denominator first.'], ['Renaming only one fraction', 'Both fractions must have the same denominator.'], ['Forgetting to regroup a whole', 'If the first fraction is smaller, rename 1 whole.']])
    faq = [('What does TEKS 5.3H ask?', 'Represent and solve addition and subtraction of fractions with unequal denominators referring to the same whole using objects, pictorial models and properties of operations.'), ('What does TEKS 5.3K ask?', 'Add and subtract positive rational numbers fluently.'), ('How do you find a common denominator?', 'Find a common multiple of both denominators, often the least common multiple: for 4 and 6, use 12.'), ('Do I have to simplify?', 'Answers are usually written in simplest form, such as 6/8 = 3/4.')]
    make('adding-and-subtracting-fractions', 8, 'Number and Operations', '5.3H, 5.3K',
         '5.3H represent and solve addition and subtraction of fractions with unequal denominators referring to the same whole using objects and pictorial models and properties of operations; 5.3K add and subtract positive rational numbers fluently',
         'Adding and Subtracting Fractions with Unlike Denominators', 'Adding and Subtracting Fractions',
         'Free Grade 5 fraction worksheets for Texas TEKS 5.3H and 5.3K: common denominators, add and subtract fractions and mixed numbers with unlike denominators, and word problems. 100 questions with answers.',
         'Rename with a common denominator, then add or subtract the numerators.', '1/3 + 1/4 = 4/12 + 3/12 = 7/12. Regroup mixed numbers when needed.',
         body, faq, sets, seo_title='Grade 5 Adding and Subtracting Fractions with Unlike Denominators (TEKS 5.3H, STAAR)')


if __name__ == "__main__":
    build()
