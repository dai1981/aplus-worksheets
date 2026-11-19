# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Composing and Decomposing Numbers to 10 (TEKS K.2I)
  python3 tools/gen_ustx_math_gk_compose_decompose.py
Number bonds, ways to make a number, two colors in one number, hidden parts, and filling a ten frame (the US
Kindergarten makers with Texas names).
Wrong answers come from real mistakes: giving the whole instead of the part, counting the shown part again, and
missing a way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_decompose_numbers_to_10 as dk
adopt(dk)
import gen_us_math_gk_make_10 as mk
adopt(mk)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Two colors, one number", [("run", dk.set_colours, ("rnd", dk.Kids), 20)]),
        ("Number bonds", [("run", dk.set_bonds, ("rnd", dk.Kids), 20)]),
        ("Ways to make a number", [("run", dk.set_ways, ("rnd", dk.Kids), 15), ("run", dk.set_stories, ("rnd", dk.Kids), 5)]),
        ("How many are hidden?", [("run", dk.set_box, ("rnd", dk.Kids), 20)]),
        ("Make 10", [("run", mk.set_fill, ("rnd", mk.Kids), 20)]),
    ], 69006)
    finish(sets, R)
    body = lesson('<ul><li>A number can be broken into two parts: 5 is 3 and 2.</li><li>The parts put together make the <b>whole</b>.</li><li>There are many ways: 5 is 4 and 1, 3 and 2, 5 and 0.</li><li>A ten frame shows how many more make 10.</li></ul>',
        [example("7 is 4 and ☐", ["4 and 3 make 7"], "3")],
        [['Giving the whole instead of the part', 'The part is smaller than the whole.'], ['Counting the shown part again', 'Count only the hidden part.'], ['Missing a way', 'Try 0 and the whole number too.']])
    faq = [('What does TEKS K.2I ask?', 'Compose and decompose numbers up to 10 with objects and pictures.'), ('What is a number bond?', 'A picture that shows a whole and its two parts.'), ('How many ways can you make 5?', '0 and 5, 1 and 4, 2 and 3, and the turn-arounds.'), ('Why practice making 10?', 'It helps with adding later.')]
    make('composing-and-decomposing-numbers-to-10', 6, 'Number and Operations', 'K.2I',
         'K.2I compose and decompose numbers up to 10 with objects and pictures',
         'Composing and Decomposing Numbers to 10', 'Composing and Decomposing to 10',
         'Free kindergarten worksheets for Texas TEKS K.2I: compose and decompose numbers to 10 with number bonds, two colors, hidden parts and ten frames. 100 questions with answers.',
         'Two parts make a whole.', '5 is 3 and 2, or 4 and 1.',
         body, faq, sets, seo_title='Kindergarten Composing and Decomposing Numbers to 10 Worksheets (TEKS K.2I)')


if __name__ == "__main__":
    build()
