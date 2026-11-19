# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Reading and Writing Numbers 0 to 20 (TEKS K.2B)
  python3 tools/gen_ustx_math_gk_numbers_0_to_20.py
Matching numbers 0 to 5, 6 to 10 and 11 to 20 to pictures, number names, and stories (the US Kindergarten makers
with Texas names).
Wrong answers come from real mistakes: mixing up 6 and 9, writing 12 as 21, and forgetting that 0 means none.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_writing_numbers_0_to_20 as wn
adopt(wn)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Numbers 0 to 5", [("run", wn.set_0_to_5, ("rnd", wn.People), 20)]),
        ("Numbers 6 to 10", [("run", wn.set_6_to_10, ("rnd", wn.People), 20)]),
        ("Numbers 11 to 20", [("run", wn.set_11_to_20, ("rnd", wn.People), 20)]),
        ("Number names", [("run", wn.set_names, ("rnd", wn.People), 20)]),
        ("Count and write the number", [("run", wn.set_stories, ("rnd", wn.People), 20)]),
    ], 69002)
    finish(sets, R)
    body = lesson('<ul><li>A number tells how many.</li><li><b>0</b> means none.</li><li>Teen numbers start with 1: 12 is ten and two more.</li><li>Number words: one, two, three … twenty.</li></ul>',
        [example("How many dots? 8 dots", ["Count: 1 to 8"], "8")],
        [['Mixing up 6 and 9', '6 has its circle at the bottom.'], ['Writing 12 as 21', 'Teen numbers start with 1.'], ['Forgetting 0', '0 means there are none.']])
    faq = [('What does TEKS K.2B ask?', 'Read, write, and represent whole numbers from 0 to at least 20 with and without objects or pictures.'), ('Is 0 a number?', 'Yes. It means none.'), ('What is 12?', 'Ten and two more.'), ('How do I spell 15?', 'Fifteen.')]
    make('reading-and-writing-numbers-0-to-20', 2, 'Number and Operations', 'K.2B',
         'K.2B read, write, and represent whole numbers from 0 to at least 20 with and without objects or pictures',
         'Reading and Writing Numbers 0 to 20', 'Numbers 0 to 20',
         'Free kindergarten number worksheets for Texas TEKS K.2B: read and write numbers 0 to 20, match numbers to pictures and number words. 100 questions with answers.',
         'A number tells how many. 0 means none.', '12 is ten and two more.',
         body, faq, sets, seo_title='Kindergarten Reading and Writing Numbers 0 to 20 Worksheets (TEKS K.2B)')


if __name__ == "__main__":
    build()
