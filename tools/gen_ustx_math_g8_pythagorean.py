# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: The Pythagorean Theorem and Its Converse (TEKS 8.6C, 8.7C)
  python3 tools/gen_ustx_math_g8_pythagorean.py
Finding the hypotenuse, finding a missing leg, the converse (is it a right triangle?), real-world problems, and 3D
and reasoning (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: adding the legs without squaring, forgetting the square root, and putting a
leg in place of the hypotenuse.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_pythagorean_theorem as pyt
adopt(pyt)
pyt.R = random.Random(680150)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Find the hypotenuse", [("run", pyt.set_hyp, (), 20)]),
        ("Find a missing leg", [("run", pyt.set_leg, (), 20)]),
        ("Is it a right triangle? The converse", [("run", pyt.set_converse, (), 20)]),
        ("Real-world problems", [("run", pyt.set_world, (), 20)]),
        ("3D and reasoning", [("run", pyt.set_3d, (), 20)]),
    ], 68015)
    finish(sets, R)
    body = lesson('<ul><li>In a right triangle, <b>a² + b² = c²</b>, where c is the hypotenuse (the side across from the right angle).</li><li>Find the hypotenuse: add the squares of the legs, then take the square root.</li><li>Find a leg: subtract, then take the square root: b = √(c² − a²).</li><li><b>Converse</b>: if a² + b² = c², the triangle is a right triangle.</li></ul>',
        [example("Legs 6 and 8", ["36 + 64 = 100", "√100"], "10"), example("Ladder 10 ft, foot 6 ft from the wall", ["100 − 36 = 64", "√64"], "8 ft")],
        [['Adding the legs: 6 + 8 = 14', 'Square first: 36 + 64 = 100, then √100 = 10.'], ['Forgetting the square root', 'c² = 100 means c = 10.'], ['Using a leg as the hypotenuse', 'The hypotenuse is always the longest side.']])
    faq = [('What does TEKS 8.7C ask?', 'Use the Pythagorean Theorem and its converse to solve problems.'), ('What does TEKS 8.6C ask?', 'Use models and diagrams to explain the Pythagorean theorem.'), ('Does a² + b² = c² work for any triangle?', 'No. Only for right triangles.'), ('What are Pythagorean triples?', 'Whole-number sides like 3, 4, 5 and 5, 12, 13.')]
    make('pythagorean-theorem', 15, 'Expressions, Equations and Relationships', '8.6C, 8.7C',
         '8.6C use models and diagrams to explain the Pythagorean theorem; 8.7C use the Pythagorean Theorem and its converse to solve problems',
         'The Pythagorean Theorem and Its Converse', 'Pythagorean Theorem',
         'Free Grade 8 Pythagorean theorem worksheets for Texas TEKS 8.6C and 8.7C: find the hypotenuse, a missing leg, the converse and real-world problems. 100 questions with answers.',
         'a² + b² = c², where c is the hypotenuse.', 'Legs 6 and 8: c = √100 = 10.',
         body, faq, sets, seo_title='Grade 8 Pythagorean Theorem Worksheets (TEKS 8.7C, STAAR)')


if __name__ == "__main__":
    build()
