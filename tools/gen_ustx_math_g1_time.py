# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Telling Time to the Hour and Half Hour (TEKS 1.7E)
  python3 tools/gen_ustx_math_g1_time.py
Time to the hour and to the half hour, matching analog and digital clocks, where the hands point, and time in daily
life (the US Grade 1 makers with Texas names).
Wrong answers come from real mistakes: mixing up the hands, reading the hour wrong at half past, and writing 3:30 as
3:00.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_time as tm
adopt(tm)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Time to the hour", [("run", tm.set_hour, ("rnd",), 20)]),
        ("Time to the half hour", [("run", tm.set_half, ("rnd",), 20)]),
        ("Match clocks", [("run", tm.set_match, ("rnd",), 20)]),
        ("Where do the hands point?", [("run", tm.set_hands, ("rnd",), 20)]),
        ("Time in daily life", [("run", tm.set_life, ("rnd", tm.People), 20)]),
    ], 69118)
    finish(sets, R)
    body = lesson("<ul><li>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes.</li><li>Long hand on 12: o'clock (3:00).</li><li>Long hand on 6: half past (3:30). The short hand is halfway between 3 and 4.</li></ul>",
        [example("Short hand between 3 and 4, long hand on 6", ["half past 3"], "3:30")],
        [['Mixing up the hands', 'The short hand is the hour.'], ['Reading the next hour at half past', 'Use the number the short hand has passed.'], ['Writing half past 3 as 3:00', 'Half past is :30.']])
    faq = [('What does TEKS 1.7E ask?', 'Tell time to the hour and half hour using analog and digital clocks.'), ('What does half past mean?', '30 minutes after the hour.'), ('Where is the long hand at 7:00?', 'On the 12.'), ('Where is the short hand at 7:30?', 'Halfway between 7 and 8.')]
    make('telling-time-to-the-hour-and-half-hour', 18, 'Geometry and Measurement', '1.7E',
         '1.7E tell time to the hour and half hour using analog and digital clocks',
         'Telling Time to the Hour and Half Hour', 'Time to the Hour and Half Hour',
         'Free Grade 1 time worksheets for Texas TEKS 1.7E: tell time to the hour and half hour on analog and digital clocks. 100 questions with answers.',
         "Long hand on 12: o'clock. On 6: half past.", 'Half past 3 is 3:30.',
         body, faq, sets, seo_title='Grade 1 Telling Time to the Hour and Half Hour Worksheets (TEKS 1.7E)')


if __name__ == "__main__":
    build()
