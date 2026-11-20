# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Time: 12-Hour and 24-Hour Time, Calendars and Time Intervals (Grade 4: 4.4 Time)
  python3 tools/gen_za_maths_g4_time.py
Reading analogue and digital clocks, 12-hour and 24-hour time, converting units of time, durations, calendars and
timetables (UK Year 4 and Australia Year 4 makers with South African names).
Wrong answers come from real mistakes: reading the hour hand as the minutes, adding 10 instead of 12 for p.m. times,
and counting the start date when finding the number of days.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_time as ukt
adopt(ukt)
if hasattr(ukt, 'R'): ukt.R = random.Random(804240)
import gen_au_maths_y4_time as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(804241)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Read the clock", [("run", ukt.set_words, ("rnd",), 20)]),
        ("12-hour and 24-hour time", [("run", ukt.set_digital, ("rnd", lambda r: __import__("itertools").cycle(ukt.PEOPLE) if hasattr(ukt, "PEOPLE") else ukt.People(r)), 20)]),
        ("Units of time", [("run", ukt.set_convert, ("rnd",), 20)]),
        ("Time intervals", [("run", ukt.set_durations, ("rnd",), 20)]),
        ("Calendars and timetables", [("run", aut.set_calendar, (), 10), ("run", ukt.set_timetables, ("rnd", lambda r: __import__("itertools").cycle(ukt.PEOPLE) if hasattr(ukt, "PEOPLE") else ukt.People(r)), 10)]),
    ], 80424)
    finish(sets, R)
    body = lesson('<ul><li>On an analogue clock, the short hand shows the hour and the long hand the minutes.</li><li>12-hour time uses a.m. (midnight to noon) and p.m. (noon to midnight). 24-hour time counts from 00:00 to 23:59: 3:15 p.m. = 15:15.</li><li>60 seconds = 1 minute, 60 minutes = 1 hour, 24 hours = 1 day, 7 days = 1 week.</li><li>To find a time interval, count on in hours, then minutes.</li></ul>',
        [example("From 08:40 to 11:15", ["08:40 → 10:40 is 2 hours", "10:40 → 11:15 is 35 minutes"], "2 hours 35 minutes")],
        [['Hour hand as minutes', 'The long hand shows the minutes.'], ['Adding 10 for p.m.', 'Add 12: 7 p.m. = 19:00.'], ['Counting the start date', 'From 3 to 10 May is 7 days.']])
    faq = [('What does CAPS Grade 4 say about time?', 'Read, tell and write time in 12-hour and 24-hour formats on analogue and digital instruments in hours, minutes and seconds, use calendars, and calculate time intervals.'), ('What is 20:30 in 12-hour time?', '8:30 p.m.'), ('How many days are in a leap year?', '366.'), ('What is a.m.?', 'Times from midnight to just before noon.')]
    make('time', 24, 'Measurement', 'Grade 4: 4.4 Time',
         'Read, tell and write time in 12-hour and 24-hour formats on both analogue and digital instruments in hours, minutes and seconds; use clocks, calendars and stopwatches; calculate the number of days between dates and time intervals given in whole hours or whole minutes.',
         'Time: 12-Hour and 24-Hour Time, Calendars and Time Intervals', 'Time',
         'Free CAPS Grade 4 time worksheets: analogue and digital clocks, 12-hour and 24-hour time, units of time, time intervals, calendars and timetables. 100 questions with memos.',
         'p.m. to 24-hour time: add 12.', 'Count on hours, then minutes.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
