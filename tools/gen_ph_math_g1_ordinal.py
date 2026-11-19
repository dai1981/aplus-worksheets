# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Ordinal Numbers: 1st to 10th (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_ordinal.py
Positions in a line from 1st to 10th, ordinal words and symbols, counting from the left or the right, before and
after, and stories (Singapore Primary 1 makers with Filipino names).
Wrong answers come from real mistakes: counting from the wrong end, mixing up 3rd and 3, and counting the person
you start from.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_p1_ordinal_numbers as sgo
adopt(sgo)
if hasattr(sgo, 'R'): sgo.R = random.Random(701060)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Who is in the line?", [("run", sgo.set_queue, (sgo.Names,), 20)]),
        ("Words and symbols", [("run", sgo.set_symbols, (sgo.Names,), 20)]),
        ("From the left or the right", [("run", sgo.set_left_right, (sgo.Names, "rnd"), 20)]),
        ("Before and after", [("run", sgo.set_before_after, (sgo.Names,), 20)]),
        ("Ordinal number stories", [("run", sgo.set_word, (sgo.Names,), 20)]),
    ], 70106)
    finish(sets, R)
    body = lesson('<ul><li>Ordinal numbers tell the position: 1st (first), 2nd (second), 3rd (third), 4th (fourth) … 10th (tenth).</li><li>Check where to start counting: from the left, from the right or from the front.</li><li>The 3rd child is one child. 3 children are three children.</li></ul>',
        [example("5 children in a line. Who is 2nd from the right?", ["count from the right: 1st, 2nd"], "the 4th from the left")],
        [['Wrong end', 'Read where to start.'], ['3rd or 3?', '3rd is one position.'], ['Counting the start', 'Start with 1st at the end of the line.']])
    faq = [('What does MATATAG Math 1 ask about ordinal numbers?', 'Describe the position of objects using ordinal numbers: 1st, 2nd, 3rd, up to 10th.'), ('How do you write ninth?', '9th.'), ('Where do children use ordinal numbers?', 'In lines, races and the days of the month.'), ('Is first the same as 1st?', 'Yes.')]
    make('ordinal-numbers', 6, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Describe the position of objects using ordinal numbers: 1st, 2nd, 3rd, up to 10th.',
         'Ordinal Numbers: 1st to 10th', 'Ordinal Numbers',
         'Free Grade 1 ordinal numbers worksheets for the DepEd MATATAG curriculum: 1st to 10th, ordinal words, positions from the left and right, and stories. 100 questions with pictures and answers.',
         'Ordinal numbers tell the position.', 'Check which end you count from.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
