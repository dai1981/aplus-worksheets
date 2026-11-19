# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Counting to 20 (TEKS K.2A, K.2C)
  python3 tools/gen_ustx_math_gk_counting_to_20.py
Counting objects 1 to 5, 6 to 10 and 11 to 20, how counting works, and counting stories (the US Kindergarten
makers with Texas names).
Wrong answers come from real mistakes: counting one object twice, skipping one, and saying one more than the last
number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_counting_to_20 as c20
adopt(c20)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Count 1 to 5", [("run", c20.set_1_to_5, ("rnd", c20.People), 20)]),
        ("Count 6 to 10", [("run", c20.set_6_to_10, ("rnd", c20.People), 20)]),
        ("Count 11 to 20", [("run", c20.set_11_to_20, ("rnd", c20.People), 20)]),
        ("How counting works", [("run", c20.set_ideas, ("rnd", c20.People), 20)]),
        ("Counting stories", [("run", c20.set_stories, ("rnd", c20.People), 20)]),
    ], 69001)
    finish(sets, R)
    body = lesson('<ul><li>Touch each thing once and say one number.</li><li>The <b>last number</b> you say tells how many.</li><li>Moving the things does not change how many.</li><li>Count forward: 1, 2, 3 … Count back: 20, 19, 18 …</li></ul>',
        [example("Count the apples", ["1, 2, 3, 4, 5, 6, 7"], "7 apples")],
        [['Counting one thing twice', 'Touch each thing once.'], ['Skipping a thing', 'Move each thing as you count it.'], ['Saying a number after the last one', 'Stop when every thing is counted.']])
    faq = [('What does TEKS K.2A ask?', 'Count forward and backward to at least 20 with and without objects.'), ('What does TEKS K.2C ask?', 'Count a set of objects up to at least 20 and demonstrate that the last number said tells the number of objects in the set regardless of their arrangement or order.'), ('Does moving the things change how many?', 'No. The number stays the same.'), ('How can I help my child count?', 'Count real things together and touch each one.')]
    make('counting-to-20', 1, 'Number and Operations', 'K.2A, K.2C',
         'K.2A count forward and backward to at least 20 with and without objects; K.2C count a set of objects up to at least 20 and demonstrate that the last number said tells the number of objects in the set regardless of their arrangement or order',
         'Counting to 20', 'Counting to 20',
         'Free kindergarten counting worksheets for Texas TEKS K.2A and K.2C: count objects to 20, how counting works and counting stories with pictures. 100 questions with answers.',
         'Touch each one. The last number tells how many.', '1, 2, 3, 4, 5 … 20',
         body, faq, sets, seo_title='Kindergarten Counting to 20 Worksheets (TEKS K.2C)')


if __name__ == "__main__":
    build()
