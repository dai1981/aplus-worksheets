# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Repeating Patterns (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_patterns.py
Finding the next term in a repeating pattern of shapes, colors and numbers, the part that repeats, missing terms,
and making patterns (Australia Year 1 makers).
Wrong answers come from real mistakes: finding the repeating part too short, continuing from the wrong place, and
changing the order of the parts.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y1_repeating_patterns as aup
adopt(aup)
if hasattr(aup, 'R'): aup.R = random.Random(701190)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("What comes next?", [("run", aup.set_next, ("rnd",), 20)]),
        ("The part that repeats", [("run", aup.set_unit, ("rnd",), 20)]),
        ("Fill the gaps", [("run", aup.set_gaps, ("rnd",), 20)]),
        ("Number patterns", [("run", aup.set_numbers, ("rnd",), 20)]),
        ("Pattern stories", [("run", aup.set_stories, ("rnd", aup.People), 20)]),
    ], 70119)
    finish(sets, R)
    body = lesson('<ul><li>A <b>repeating pattern</b> has a part that repeats again and again: red, blue, red, blue …</li><li>Find the part that repeats. Then say it again to find what comes next.</li><li>Patterns can use shapes, colors, sounds, movements or numbers: clap, stamp, clap, stamp.</li></ul>',
        [example("▲ ● ● ▲ ● ● ▲ …", ["the part ▲ ● ● repeats"], "next: ●")],
        [['Repeating part too short', 'Check the part repeats all the way.'], ['Wrong place', 'Continue from the last term.'], ['Changing the order', 'Keep the same order every time.']])
    faq = [('What does MATATAG Math 1 ask about patterns?', 'Determine the next term in a repeating pattern, and create repeating patterns using objects, images, or numbers.'), ('What is the core of a pattern?', 'The part that repeats.'), ('Can numbers make a repeating pattern?', 'Yes: 1, 2, 3, 1, 2, 3.'), ('Where are patterns in real life?', 'Weaving, beads, songs and dances.')]
    make('repeating-patterns', 19, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Determine the next term/s in a repeating pattern (patterns could use rhythmic properties, visual elements in the arts, and other objects); create repeating patterns using objects, images, or numbers.',
         'Repeating Patterns', 'Repeating Patterns',
         'Free Grade 1 repeating pattern worksheets for the DepEd MATATAG curriculum: what comes next, the part that repeats, missing terms and number patterns. 100 questions with pictures and answers.',
         'Find the part that repeats.', 'Keep the same order every time.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
