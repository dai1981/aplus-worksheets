# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Adding and Subtracting Similar Fractions and Mixed Numbers (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_similar_fractions.py
Adding and subtracting fractions with the same denominator, mixed numbers, whole numbers and fractions, and word
problems (US Grade 4 and Singapore Primary 4 makers with Filipino names).
Wrong answers come from real mistakes: adding the denominators, forgetting to regroup a whole, and subtracting the
whole numbers only.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_add_subtract_fractions as usf
adopt(usf)
if hasattr(usf, 'R'): usf.R = random.Random(704120)
import gen_sg_maths_p4_add_sub_fractions as sgf
adopt(sgf)
if hasattr(sgf, 'R'): sgf.R = random.Random(704121)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Add similar fractions", [("run", usf.set_add, ("rnd", usf.People), 20)]),
        ("Subtract similar fractions", [("run", usf.set_subtract, ("rnd", usf.People), 20)]),
        ("Similar fractions and wholes", [("run", sgf.set_like, ("rnd",), 10), ("run", sgf.set_whole, ("rnd",), 10)]),
        ("Mixed numbers", [("run", usf.set_mixed, ("rnd",), 20)]),
        ("Word problems", [("run", usf.set_words, ("rnd", usf.People), 20)]),
    ], 70412)
    finish(sets, R)
    body = lesson("<ul><li><b>Similar fractions</b> have the same denominator, like <span class='fr'><span class='fn'>2</span><span class='fd'>7</span></span> and <span class='fr'><span class='fn'>3</span><span class='fd'>7</span></span>.</li><li>To add or subtract them, add or subtract the numerators. Keep the denominator.</li><li>Mixed numbers: add or subtract the fractions, then the wholes. If the fraction part is too small to subtract, regroup 1 whole.</li><li>Change an improper answer to a mixed number.</li></ul>",
        [example("2 <span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> + 1 <span class='fr'><span class='fn'>4</span><span class='fd'>5</span></span>", ["3 + <span class='fr'><span class='fn'>7</span><span class='fd'>5</span></span>", "<span class='fr'><span class='fn'>7</span><span class='fd'>5</span></span> = 1 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>"], "4 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>")],
        [['Adding the denominators', 'The denominator stays the same.'], ['Not regrouping a whole', 'Change 1 whole into fifths when needed.'], ['Subtracting only the wholes', 'Subtract the fractions too.']])
    faq = [('What does MATATAG Math 4 ask about similar fractions?', 'Add and subtract similar fractions: two proper fractions, two mixed numbers, a mixed number and a proper fraction, a whole number and a proper fraction, and a whole number and a mixed number.'), ('What are similar fractions?', 'Fractions with the same denominator.'), ('How do I subtract a fraction from a whole number?', 'Write the whole number as a fraction with the same denominator, or regroup 1 whole.'), ('Should I simplify the answer?', 'Yes, if your teacher asks for the simplest form.')]
    make('adding-and-subtracting-similar-fractions', 12, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Add and subtract similar fractions: two proper fractions, two mixed numbers, a mixed number and a proper fraction, a whole number and a proper fraction, and a whole number and a mixed number.',
         'Adding and Subtracting Similar Fractions and Mixed Numbers', 'Similar Fractions',
         'Free Grade 4 worksheets on adding and subtracting similar fractions for the DepEd MATATAG curriculum: proper fractions, mixed numbers, whole numbers and word problems. 100 questions with answers.',
         'Add or subtract the numerators; keep the denominator.', 'Regroup 1 whole when the fraction part is too small.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
