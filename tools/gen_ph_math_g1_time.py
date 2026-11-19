# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Telling Time to the Hour, Half Hour and Quarter Hour (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_time.py
Reading and writing time on an analog clock to the hour, half hour and quarter hour, matching clocks and times, and
daily routines (Australia Year 2 and US Grade 1 makers with Filipino names).
Wrong answers come from real mistakes: mixing up the hour hand and minute hand, reading half past 4 as 5:30, and
thinking quarter past is 15 minutes before.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y2_time as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(701230)
import gen_us_math_g1_time as ust
adopt(ust)
if hasattr(ust, 'R'): ust.R = random.Random(701231)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Time to the hour", [("run", aut.set_oclock, ("rnd",), 20)]),
        ("Half past", [("run", aut.set_half, ("rnd",), 20)]),
        ("Quarter past and quarter to", [("run", aut.set_quarter, ("rnd",), 20)]),
        ("Match the clocks", [("run", aut.set_match, ("rnd",), 10), ("run", ust.set_hands, ("rnd",), 10)]),
        ("Time in my day", [("run", aut.set_routines, ("rnd", lambda r: __import__("itertools").cycle(aut.PEOPLE)), 10), ("run", ust.set_life, ("rnd", ust.People), 10)]),
    ], 70123)
    finish(sets, R)
    body = lesson("<ul><li>The short hand is the <b>hour hand</b>. The long hand is the <b>minute hand</b>.</li><li>When the minute hand points to 12, it is o'clock: 7:00.</li><li>When it points to 6, it is half past: 7:30. The hour hand is halfway between 7 and 8.</li><li>Quarter past is :15 (minute hand at 3). Quarter to is :45 (minute hand at 9).</li></ul>",
        [example("Minute hand at 3, hour hand just past 9", ["quarter past 9"], "9:15")],
        [['Mixing the hands', 'The short hand shows the hour.'], ['Half past 4 as 5:30', 'Half past 4 is 4:30.'], ['Quarter past or to?', 'Quarter past: 15 minutes after.']])
    faq = [('What does MATATAG Math 1 ask about time?', 'Read and write time by the hour, half hour, and quarter hour using an analog clock, and solve problems involving time.'), ('How many minutes are in an hour?', '60.'), ('What time is quarter to 8?', '7:45.'), ('Why learn analog clocks?', 'Many clocks at home and school have hands.')]
    make('telling-time', 23, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Read and write time by the hour, half hour, and quarter hour using an analog clock.',
         'Telling Time to the Hour, Half Hour and Quarter Hour', 'Telling Time',
         "Free Grade 1 telling time worksheets for the DepEd MATATAG curriculum: o'clock, half past, quarter past and quarter to on analog clocks, and daily routines. 100 questions with pictures and answers.",
         'Short hand: hour. Long hand: minutes.', 'Half past: minute hand at 6.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
