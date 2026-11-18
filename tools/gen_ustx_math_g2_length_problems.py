# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Length Word Problems and Number Lines (TEKS 2.9C, 2.9E)
  python3 tools/gen_ustx_math_g2_length_problems.py
Lengths on a number line, jumps on a number line, joining lengths, taking away and comparing lengths, and unknown
lengths (the US Grade 2 makers with Texas names).
Wrong answers come from real mistakes: adding when you should subtract, mixing units, and counting the start mark
as a jump.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_length_problems as lp
adopt(lp)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Lengths on a number line", [("run", lp.set_lengths, ("rnd", lp.People), 20)]),
        ("Jumps on a number line", [("run", lp.set_jumps, ("rnd", lp.People), 20)]),
        ("Join lengths", [("run", lp.set_join, ("rnd", lp.People), 20)]),
        ("Take away and compare", [("run", lp.set_take_compare, ("rnd", lp.People), 20)]),
        ("Find the unknown length", [("run", lp.set_unknown, ("rnd", lp.People), 20)]),
    ], 69216)
    finish(sets, R)
    body = lesson('<ul><li>Lengths are numbers, so you can add and subtract them.</li><li>Joining two pieces: add. Cutting off or comparing: subtract.</li><li>On a number line, each jump is a distance from one number to another.</li><li>Keep the same unit: inches with inches, meters with meters.</li></ul>',
        [example("A ribbon is 45 cm. Ava cuts off 18 cm.", ["45 − 18"], "27 cm")],
        [['Adding when you should subtract', 'Cut off or how much longer means subtract.'], ['Mixing units', 'Use the same unit for every length.'], ['Counting the start as a jump', 'Count the spaces you jump over.']])
    faq = [('What does TEKS 2.9E ask?', 'Determine a solution to a problem involving length, including estimating lengths.'), ('What does TEKS 2.9C ask?', 'Represent whole numbers as distances from any given location on a number line.'), ('How do I compare two lengths?', 'Subtract the shorter length from the longer one.'), ('Can I estimate first?', 'Yes. An estimate helps you check your answer.')]
    make('length-word-problems', 16, 'Geometry and Measurement', '2.9C, 2.9E',
         '2.9C represent whole numbers as distances from any given location on a number line; 2.9E determine a solution to a problem involving length, including estimating lengths',
         'Length Word Problems and Number Lines', 'Length Word Problems',
         'Free Grade 2 length word problem worksheets for Texas TEKS 2.9C and 2.9E: lengths and jumps on a number line, joining, comparing and unknown lengths. 100 questions with answers.',
         'Join lengths: add. Cut off or compare: subtract.', '45 cm − 18 cm = 27 cm.',
         body, faq, sets, seo_title='Grade 2 Length Word Problems Worksheets (TEKS 2.9E)')


if __name__ == "__main__":
    build()
