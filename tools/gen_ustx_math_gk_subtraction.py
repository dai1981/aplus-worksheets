# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Subtraction within 10: Separating (TEKS K.3A, K.3B)
  python3 tools/gen_ustx_math_gk_subtraction.py
Taking away, subtracting with ten frames and number lines, number sentences, and stories (the US Kindergarten makers
with Texas names).
Wrong answers come from real mistakes: counting the crossed-out ones, adding instead, and being off by 1.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_subtraction_within_10 as sb
adopt(sb)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Take away", [("run", sb.set_cross, ("rnd", sb.Kids), 20)]),
        ("Subtract with ten frames", [("run", sb.set_frames, ("rnd", sb.Kids), 20)]),
        ("Hop back on a number line", [("run", sb.set_line, ("rnd", sb.Kids), 20)]),
        ("Number sentences", [("run", sb.set_sentences, ("rnd", sb.Kids), 20)]),
        ("Subtraction stories", [("run", sb.set_stories, ("rnd", sb.Kids), 20)]),
    ], 69008)
    finish(sets, R)
    body = lesson('<ul><li><b>Subtracting</b> means separating or taking away.</li><li>Cross out the ones that go away. Count the ones that are left.</li><li>Write it as a number sentence: 7 − 3 = 4.</li></ul>',
        [example("7 birds. 3 fly away.", ["Cross out 3", "Count what is left"], "4 birds")],
        [['Counting the crossed-out ones', 'Count only the ones left.'], ['Adding instead', 'Go away means take away.'], ['Being off by 1', 'Count back one hop at a time.']])
    faq = [('What does TEKS K.3A ask?', 'Model the action of joining to represent addition and the action of separating to represent subtraction.'), ('What does TEKS K.3B ask?', 'Solve word problems using objects and drawings to find sums up to 10 and differences within 10.'), ('What does − mean?', 'Minus: take away.'), ('Can the answer be 0?', 'Yes, if all of them go away.')]
    make('subtraction-within-10', 8, 'Number and Operations', 'K.3A, K.3B',
         'K.3A model the action of joining to represent addition and the action of separating to represent subtraction; K.3B solve word problems using objects and drawings to find sums up to 10 and differences within 10',
         'Subtraction within 10: Separating', 'Subtraction within 10',
         'Free kindergarten subtraction worksheets for Texas TEKS K.3A and K.3B: take away, ten frames, number lines, number sentences and stories within 10. 100 questions with answers.',
         'Subtracting means taking away.', '7 − 3 = 4',
         body, faq, sets, seo_title='Kindergarten Subtraction within 10 Worksheets (TEKS K.3B)')


if __name__ == "__main__":
    build()
