# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Addition within 10: Joining (TEKS K.3A, K.3B)
  python3 tools/gen_ustx_math_gk_addition.py
Putting groups together, adding with ten frames and number lines, number sentences, and stories (the US Kindergarten
makers with Texas names).
Wrong answers come from real mistakes: counting a group twice, counting only one group, and being off by 1.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_addition_within_10 as ad
adopt(ad)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Put together", [("run", ad.set_groups, ("rnd", ad.Kids), 20)]),
        ("Add with ten frames", [("run", ad.set_frames, ("rnd", ad.Kids), 20)]),
        ("Add on a number line", [("run", ad.set_line, ("rnd", ad.Kids), 20)]),
        ("Number sentences", [("run", ad.set_sentences, ("rnd", ad.Kids), 20)]),
        ("Addition stories", [("run", ad.set_stories, ("rnd", ad.Kids), 20)]),
    ], 69007)
    finish(sets, R)
    body = lesson('<ul><li><b>Adding</b> means joining groups together.</li><li>Count all, or start at the bigger number and count on.</li><li>Write it as a number sentence: 4 + 3 = 7.</li></ul>',
        [example("4 ducks and 3 more ducks", ["4, 5, 6, 7"], "7 ducks")],
        [['Counting a group twice', 'Touch each thing once.'], ['Counting only one group', 'Join both groups.'], ['Being off by 1', 'Start counting on at the next number.']])
    faq = [('What does TEKS K.3A ask?', 'Model the action of joining to represent addition and the action of separating to represent subtraction.'), ('What does TEKS K.3B ask?', 'Solve word problems using objects and drawings to find sums up to 10 and differences within 10.'), ('What does + mean?', 'Plus: put together.'), ('How can a ten frame help?', 'It shows the total quickly.')]
    make('addition-within-10', 7, 'Number and Operations', 'K.3A, K.3B',
         'K.3A model the action of joining to represent addition and the action of separating to represent subtraction; K.3B solve word problems using objects and drawings to find sums up to 10 and differences within 10',
         'Addition within 10: Joining', 'Addition within 10',
         'Free kindergarten addition worksheets for Texas TEKS K.3A and K.3B: put together, ten frames, number lines, number sentences and stories within 10. 100 questions with answers.',
         'Adding means joining.', '4 + 3 = 7',
         body, faq, sets, seo_title='Kindergarten Addition within 10 Worksheets (TEKS K.3B)')


if __name__ == "__main__":
    build()
