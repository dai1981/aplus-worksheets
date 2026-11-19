# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Simplifying Expressions with Integers: GEMDAS and Number Properties (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_gemdas.py
The order of operations (GEMDAS: grouping, exponents, multiplication and division, addition and subtraction) with
whole numbers and integers, left to right, grouping symbols, and word problems (BC Grade 7 makers).
Wrong answers come from real mistakes: adding before multiplying, multiplying before a division that comes first,
and squaring a negative number without its parentheses.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_cabc_math_g7_order_of_operations as cbo
adopt(cbo)
if hasattr(cbo, 'R'): cbo.R = random.Random(707240)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Order of operations", [("run", cbo.set_order, ("rnd", "seen"), 20)]),
        ("Left to right", [("run", cbo.set_ltr, ("rnd", "seen"), 20)]),
        ("Grouping symbols", [("run", cbo.set_brackets, ("rnd", "seen"), 20)]),
        ("Expressions with integers", [("run", cbo.set_integers, ("rnd", "seen"), 20)]),
        ("GEMDAS word problems", [("run", cbo.set_words, ("rnd", "seen"), 20)]),
    ], 70724)
    finish(sets, R)
    body = lesson('<ul><li><b>GEMDAS</b>: Grouping symbols first, then Exponents, then Multiplication and Division (left to right), then Addition and Subtraction (left to right).</li><li>Grouping symbols include parentheses ( ), brackets [ ] and fraction bars.</li><li>(−3)² = 9, but −3² = −9: the exponent acts only on what it touches.</li><li>Number properties (commutative, associative, distributive) can make the work easier: 4 × 17 × 25 = (4 × 25) × 17.</li></ul>',
        [example("−2 + 3 × (4 − 7)²", ["(−3)² = 9", "3 × 9 = 27", "−2 + 27"], "25")],
        [['Adding first', '× and ÷ come before + and −.'], ['× before an earlier ÷', 'Work left to right.'], ['−3² as 9', 'Only (−3)² is 9.']])
    faq = [('What does MATATAG Math 7 ask about GEMDAS?', 'Simplify numerical expressions involving integers using number properties and the order of operations (GEMDAS).'), ('What does the G in GEMDAS stand for?', 'Grouping symbols, such as parentheses and brackets.'), ('Is GEMDAS the same as PEMDAS?', 'Yes. P (parentheses) is one kind of grouping symbol.'), ('Do I always multiply before dividing?', 'No. Do them in order from left to right.')]
    make('order-of-operations-gemdas', 24, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Simplify numerical expressions involving integers using number properties and the order of operations (GEMDAS).',
         'Simplifying Expressions with Integers: GEMDAS and Number Properties', 'GEMDAS',
         'Free Grade 7 GEMDAS worksheets for the DepEd MATATAG curriculum: order of operations with integers, grouping symbols, exponents, number properties and word problems. 100 questions with answers.',
         'GEMDAS: Grouping, Exponents, × ÷, + −.', '× and ÷ (and + and −) go left to right.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
