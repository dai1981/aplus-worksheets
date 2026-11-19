# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Half Turns and Quarter Turns, Clockwise and Counterclockwise (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_turns.py
Quarter turns and half turns, clockwise and counterclockwise, which way you face after a turn, turning shapes and
everyday turns (Australia Year 2 makers with US spelling).
Wrong answers come from real mistakes: mixing up clockwise and counterclockwise, turning a half turn when the
question says a quarter turn, and turning from the wrong starting direction.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y2_turns as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(701220)
ph_common.GRADE = "grade-1"


import re as _re


def no34(it):
    return not _re.search(r"three-quarter|full turn|3/4|three quarter", _re.sub(r"<[^>]+>", " ", it["q"] + " " + it["c"][it["a"]]), _re.I)


def build():
    sets, R = build_sets([
        ("Quarter turns and half turns", [("run", aut.set_turns, ("rnd", aut.People), 20, no34)]),
        ("Clockwise or counterclockwise?", [("run", aut.set_clockwise, ("rnd", aut.People), 20, no34)]),
        ("Which way are you facing?", [("run", aut.set_facing, ("rnd", aut.People), 20, no34)]),
        ("Turning shapes", [("run", aut.set_shapes, ("rnd", aut.People), 20, no34)]),
        ("Turns in everyday life", [("run", aut.set_life, ("rnd", aut.People), 20, no34)]),
    ], 70122)
    finish(sets, R)
    body = lesson('<ul><li>A <b>quarter turn</b> is one corner of a square. A <b>half turn</b> is two quarter turns: you face the opposite way.</li><li><b>Clockwise</b> is the way the hands of a clock move. <b>Counterclockwise</b> is the other way.</li><li>Facing the board, a quarter turn clockwise makes you face right. A half turn makes you face the back.</li></ul>',
        [example("An arrow points up. A quarter turn clockwise.", ["up → right"], "it points right")],
        [['Clockwise or counterclockwise?', "Think of a clock's hands."], ['Half or quarter?', 'A half turn faces the opposite way.'], ['Wrong start', 'Begin from the way you face now.']])
    faq = [('What does MATATAG Math 1 ask about turns?', 'Identify the position of objects moved in half turn or in quarter turn, in clockwise or in counter-clockwise direction.'), ('How many quarter turns make a half turn?', '2.'), ('Do a half turn clockwise and counterclockwise end the same?', 'Yes.'), ('How can children practice?', 'Stand up, face the board and turn.')]
    make('half-turns-and-quarter-turns', 22, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Identify the position of objects moved in half turn or in quarter turn, in clockwise or in counter-clockwise direction.',
         'Half Turns and Quarter Turns, Clockwise and Counterclockwise', 'Half and Quarter Turns',
         'Free Grade 1 turns worksheets for the DepEd MATATAG curriculum: half turns and quarter turns, clockwise and counterclockwise, and which way you face. 100 questions with pictures and answers.',
         'A half turn = 2 quarter turns.', 'Clockwise: the way clock hands move.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
