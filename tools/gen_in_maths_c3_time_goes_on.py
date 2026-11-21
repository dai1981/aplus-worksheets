# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 13: Time Goes On (Time and the Calendar)
Telling time to 5 minutes and to the minute, a.m. and p.m., units of time, the calendar and elapsed time (UK Year 3 and BC Grade 3 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y3_time", 603130)
bc = mod("gen_cabc_math_g3_time", 603131)
unit(3, "time-goes-on", 13, "M", 13, "Time Goes On", "Time and the Calendar", "time",
     "Time: reading a clock to the hour, half hour, quarter hour and minute; units of time; reading a calendar; sequence of events (summary of NCERT Maths Mela Class 3)",
     "Class 3 Time Goes On worksheet (Maths Mela Chapter 13): clocks to 5 minutes and to the minute, a.m. and p.m., calendar and how long. 100 questions with answers.",
     "60 minutes make an hour.", "The long hand shows the minutes.",
     "<ul><li>The short hand shows the hour; the long hand shows minutes in steps of 5.</li><li>a.m. is before noon; p.m. is after noon.</li><li>7 days = 1 week, 12 months = 1 year.</li></ul>",
     [('The hour hand is just past 4 and the minute hand points to 3.', ['3 × 5 = 15 minutes'], '4:15')],
     [['Reading the hands the wrong way round', 'Short hand: hour. Long hand: minutes.'], ['Counting the 12 as 12 minutes', 'At 12 the minutes are 0.']],
     [('How many minutes are in an hour?', '60.'), ('What do a.m. and p.m. mean?', 'a.m. is from midnight to noon; p.m. is from noon to midnight.')],
     [('Quarter hours', [rn(uk, "set_quarters", 20)]),
      ('Five minutes', [rn(uk, "set_fives", 20)]),
      ('To the minute', [rn(uk, "set_minute", 20)]),
      ('Time facts and the calendar', [rn(uk, "set_facts", 10), rn(bc, "set_calendar", 10)]),
      ('How long?', [rn(uk, "set_problems", 10), rn(bc, "set_elapsed", 10)])], 60313)
