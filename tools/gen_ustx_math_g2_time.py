# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Telling Time to the Minute; a.m. and p.m. (TEKS 2.9G)
  python3 tools/gen_ustx_math_g2_time.py
Counting by 5s around the clock, reading the clock to 5 minutes and to 1 minute, time words, and a.m. and p.m.
(the US Grade 2 and Grade 3 makers with Texas names).
Wrong answers come from real mistakes: mixing up the hands, reading the minute hand as the number it points to, and
mixing up a.m. and p.m.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_time as t2
adopt(t2)
import gen_us_math_g3_time as t3
adopt(t3)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Count by 5s around the clock", [("run", t2.set_count5, ("rnd",), 20)]),
        ("Read the clock to 5 minutes", [("run", t3.set_five, ("rnd",), 20)]),
        ("Read the clock to the minute", [("run", t3.set_one, ("rnd",), 20)]),
        ("Time words", [("run", t3.set_words, ("rnd",), 20)]),
        ("a.m. and p.m.", [("run", t2.set_ampm, ("rnd", t2.People), 20)]),
    ], 69218)
    finish(sets, R)
    body = lesson('<ul><li>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes.</li><li>Count by 5s for each number on the clock, then count on by 1s for the little marks.</li><li><b>a.m.</b> is from midnight to noon (morning). <b>p.m.</b> is from noon to midnight (afternoon and evening).</li></ul>',
        [example("Short hand just past 3, long hand 2 marks after the 7", ["7 × 5 = 35, + 2 = 37"], "3:37")],
        [['Mixing up the hands', 'The short hand is the hour.'], ['Reading the minute hand as its number', 'The long hand on 4 means 20 minutes.'], ['Mixing up a.m. and p.m.', 'Breakfast is a.m.; dinner is p.m.']])
    faq = [('What does TEKS 2.9G ask?', 'Read and write time to the nearest one-minute increment using analog and digital clocks and distinguish between a.m. and p.m.'), ('How many minutes are in an hour?', '60 minutes.'), ('Is noon a.m. or p.m.?', '12:00 noon is p.m.'), ('What does quarter past mean?', '15 minutes after the hour.')]
    make('telling-time-to-the-minute', 18, 'Geometry and Measurement', '2.9G',
         '2.9G read and write time to the nearest one-minute increment using analog and digital clocks and distinguish between a.m. and p.m.',
         'Telling Time to the Minute; a.m. and p.m.', 'Telling Time to the Minute',
         'Free Grade 2 time worksheets for Texas TEKS 2.9G: count by 5s around the clock, read clocks to 5 minutes and to the minute, time words and a.m. and p.m. 100 questions with answers.',
         'Count by 5s, then count on by 1s.', 'Short hand: hour. Long hand: minutes. a.m. morning, p.m. afternoon and evening.',
         body, faq, sets, seo_title='Grade 2 Telling Time to the Minute Worksheets (TEKS 2.9G)')


if __name__ == "__main__":
    build()
