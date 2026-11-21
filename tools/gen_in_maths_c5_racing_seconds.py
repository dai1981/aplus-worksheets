# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 12: Racing Seconds (Time: Seconds, Minutes and Hours)
Seconds, minutes and hours, 12- and 24-hour clocks, durations and race problems (AU Year 5 and BC Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

au = mod("gen_au_maths_y5_time", 605120)
bc = mod("gen_cabc_math_g5_time", 605121)
unit(5, "racing-seconds", 12, "M", 12, "Racing Seconds", "Time: Seconds, Minutes and Hours", "time",
     "Time: measuring short durations in seconds, converting between seconds, minutes and hours, 24-hour time, and solving problems (summary of NCERT Maths Mela Class 5)",
     "Class 5 Racing Seconds worksheet (Maths Mela Chapter 12): seconds, minutes, 24-hour time, durations and race problems. 100 questions with answers.",
     "60 seconds = 1 minute; 60 minutes = 1 hour.", "24-hour time: 3:45 p.m. is 15:45.",
     "<ul><li>1 minute = 60 seconds; 1 hour = 60 minutes.</li><li>Add 12 to p.m. hours for the 24-hour clock: 7:20 p.m. → 19:20.</li><li>Find a duration by counting on to the next hour, then on.</li></ul>",
     [('Ravi ran 100 m in 1 minute 5 seconds. How many seconds?', ['60 + 5'], '65 seconds')],
     [['Using 100 seconds in a minute', 'There are 60 seconds in a minute.'], ['Writing 2 p.m. as 2:00 in 24-hour time', 'It is 14:00.']],
     [('What is the 24-hour clock?', 'A way to show time from 00:00 to 23:59 without a.m. or p.m.'), ('How many seconds are in an hour?', '3,600.')],
     [('Clocks', [rn(au, "set_clocks", 20)]),
      ('To 24-hour time', [rn(au, "set_to24", 10), rn(bc, "set_24", 10)]),
      ('To 12-hour time', [rn(au, "set_to12", 20)]),
      ('Units of time', [rn(bc, "set_units", 14), rn(bc, "set_start_end", 6)]),
      ('Durations and races', [rn(au, "set_durations", 10), rn(bc, "set_elapsed", 10)])], 60512)
