# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 10: How do I Spend my Day? (Time)
Morning, afternoon, evening and night; before and after; days of the week; earlier and later; o'clock times."""
from in_prim import unit, mod, rn
dt = mod("gen_au_maths_f_days_and_times_of_day", 601101)
uk = mod("gen_uk_maths_y1_time", 601102)
us = mod("gen_us_math_g1_time", 601103)
unit(1, "how-do-i-spend-my-day", 10, "M", 10, "How do I Spend my Day?", "Time of Day and Days of the Week", "time",
     "Time: sequencing events of the day, morning, afternoon, evening and night, longer and shorter durations, days of the week (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 How do I Spend my Day? worksheet (Joyful Mathematics Chapter 10): times of day, order of events, days of the week and o'clock times. 100 picture questions with answers.",
     "Morning, afternoon, evening, night.", "Seven days make a week.",
     "<ul><li>We wake up in the <b>morning</b>, have lunch in the <b>afternoon</b>, play in the <b>evening</b> and sleep at <b>night</b>.</li><li>The days of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.</li></ul>",
     [("What comes after Wednesday?", ["Say the days in order"], "Thursday")],
     [["Mixing up yesterday and tomorrow", "Yesterday was before today; tomorrow comes after."], ["Reading the short hand as minutes", "On a clock the short hand shows the hour."]],
     [("How many days are in a week?", "Seven."), ("What should Class 1 children know about clocks?", "Reading o'clock times and knowing the order of daily events.")],
     [("Times of day", [rn(dt, "set_sky", 10), rn(dt, "set_when", 10)]),
      ("What happens first?", [rn(dt, "set_order", 10), rn(uk, "set_order", 10)]),
      ("Days of the week", [rn(dt, "set_days", 10), rn(dt, "set_yt", 10)]),
      ("O'clock", [rn(uk, "set_oclock", 10), rn(us, "set_hour", 10)]),
      ("Time in my day", [rn(uk, "set_life", 10), rn(us, "set_life", 10)])], 60110)
