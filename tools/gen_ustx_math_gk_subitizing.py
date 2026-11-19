# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Subitizing: How Many at a Glance? (TEKS K.2D)
  python3 tools/gen_ustx_math_gk_subitizing.py
Small groups, dot cubes, ten frames, finding the group, and two parts at a glance (the Australian Foundation makers
with US spelling).
Wrong answers come from real mistakes: counting one by one too slowly and losing track, mixing up 4 and 5, and
adding the two parts wrong.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_au_maths_f_subitising as sb
adopt(sb)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Small groups", [("run", sb.set_groups, ("rnd",), 20)]),
        ("Dot cubes", [("run", sb.set_dice, ("rnd",), 20)]),
        ("Ten frames", [("run", sb.set_frames, ("rnd",), 20)]),
        ("Find the group", [("run", sb.set_find, ("rnd",), 20)]),
        ("Two parts at a glance", [("run", sb.set_parts, ("rnd",), 20)]),
    ], 69003)
    finish(sets, R)
    body = lesson('<ul><li><b>Subitizing</b> means seeing how many without counting one by one.</li><li>Dot cubes and ten frames show numbers in patterns.</li><li>A full row of a ten frame is 5.</li><li>See two small groups, then put them together: 3 and 2 make 5.</li></ul>',
        [example("A ten frame with 1 full row and 2 more", ["5 and 2"], "7")],
        [['Losing track while counting', 'Look for a pattern you know.'], ['Mixing up 4 and 5', '5 has a dot in the middle.'], ['Adding the parts wrong', 'See each part, then put them together.']])
    faq = [('What does TEKS K.2D ask?', 'Recognize instantly the quantity of a small group of objects in organized and random arrangements.'), ('What is subitizing?', 'Knowing how many at a glance.'), ('Why use ten frames?', 'Rows of 5 make numbers easy to see.'), ('How can I practice at home?', 'Show dot cubes or fingers quickly and ask how many.')]
    make('subitizing', 3, 'Number and Operations', 'K.2D',
         'K.2D recognize instantly the quantity of a small group of objects in organized and random arrangements',
         'Subitizing: How Many at a Glance?', 'Subitizing',
         'Free kindergarten subitizing worksheets for Texas TEKS K.2D: see how many at a glance with small groups, dot cubes and ten frames. 100 questions with answers.',
         'See how many without counting.', 'A full row of a ten frame is 5.',
         body, faq, sets, seo_title='Kindergarten Subitizing Worksheets (TEKS K.2D)')


if __name__ == "__main__":
    build()
