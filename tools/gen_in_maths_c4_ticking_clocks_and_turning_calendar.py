# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 12: Ticking Clocks and Turning Calendar (Time and the Calendar)
Time in words and digital form, converting units of time, durations, timetables and the calendar (UK Year 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_time", 604120)
au = mod("gen_au_maths_y4_time", 604121)
unit(4, "ticking-clocks-and-turning-calendar", 12, "M", 12, "Ticking Clocks and Turning Calendar", "Time and the Calendar", "time and calendar",
     "Time: reading clocks to the minute, a.m. and p.m., converting units of time, finding durations and reading calendars (summary of NCERT Maths Mela Class 4)",
     "Class 4 Ticking Clocks and Turning Calendar worksheet (Maths Mela Chapter 12): clocks, digital time, units of time, durations and calendars. 100 questions with answers.",
     "60 minutes = 1 hour; 24 hours = 1 day.", "Count on in steps to find how long.",
     "<ul><li>Write time in words or digits: quarter past 3 = 3:15.</li><li>Find how long by counting on: 9:40 to 10:15 is 20 + 15 = 35 minutes.</li></ul>",
     [('A film starts at 4:35 p.m. and ends at 6:10 p.m.', ['4:35 → 5:35 is 1 h', '5:35 → 6:10 is 35 min'], '1 hour 35 minutes')],
     [['Using 100 minutes in an hour', 'There are 60 minutes in an hour.'], ['Mixing up a.m. and p.m.', 'a.m. is before noon.']],
     [('How many days are in a year?', '365, or 366 in a leap year.'), ('What is a leap year?', 'A year with 29 days in February, usually every 4 years.')],
     [('Time in words', [rn(uk, "set_words", 20)]),
      ('Digital time', [rn(uk, "set_digital", 20)]),
      ('Units of time', [rn(uk, "set_convert", 10), rn(au, "set_units", 10)]),
      ('How long?', [rn(uk, "set_durations", 10), rn(au, "set_durations", 10)]),
      ('Timetables and calendars', [rn(uk, "set_timetables", 10), rn(au, "set_calendar", 10)])], 60412)
