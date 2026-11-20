# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Multiplication and Division Facts to 10 × 10 (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_times_tables.py
Multiplication facts to 10 × 10, division facts, strategies for facts, multiplying by 10 and 100, and word problems
(Australia Year 4 makers with South African names).
Wrong answers come from real mistakes: mixing up neighbouring facts, adding instead of multiplying, and confusing
× 0 and × 1.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_multiplication_facts as auf
adopt(auf)
if hasattr(auf, 'R'): auf.R = random.Random(804050)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Multiplication facts", [("run", auf.set_facts, ("rnd",), 20)]),
        ("Division facts", [("run", auf.set_division, ("rnd",), 20)]),
        ("Strategies for facts", [("run", auf.set_strategies, ("rnd",), 20)]),
        ("Multiply by 10 and 100", [("run", auf.set_zeros, ("rnd",), 20)]),
        ("Times table problems", [("run", auf.set_words, (auf.People,), 20)]),
    ], 80405)
    finish(sets, R)
    body = lesson('<ul><li>Know the times tables up to 10 × 10 by heart.</li><li>Use facts you know: 7 × 8 = 7 × 4 doubled = 56.</li><li>Every multiplication fact gives two division facts: 6 × 7 = 42, so 42 ÷ 6 = 7 and 42 ÷ 7 = 6.</li><li>To multiply by 10, the digits move one place to the left: 36 × 10 = 360.</li></ul>',
        [example("9 × 7", ["10 × 7 = 70", "70 − 7"], "63")],
        [['Neighbouring facts', '6 × 8 = 48, not 42.'], ['Adding', '6 × 8 is not 6 + 8.'], ['× 0 and × 1', 'Any number × 0 = 0; × 1 keeps the number.']])
    faq = [('What does CAPS Grade 4 say about times tables?', 'Learners recall multiplication and division facts up to 10 × 10.'), ('How can learners practise?', 'A few minutes of mental maths every day.'), ('Which tables are hardest?', 'Usually 6, 7 and 8.'), ('Why learn division facts?', 'They are the multiplication facts in reverse.')]
    make('multiplication-tables-to-10-x-10', 5, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Multiplication of whole numbers to at least 10 × 10 (mental calculations); recall multiplication and division facts.',
         'Multiplication and Division Facts to 10 × 10', 'Times Tables',
         'Free CAPS Grade 4 times tables worksheets: multiplication and division facts to 10 × 10, strategies, multiplying by 10 and 100 and word problems. 100 questions with memos.',
         'Know the facts to 10 × 10 by heart.', 'One multiplication fact gives two division facts.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
