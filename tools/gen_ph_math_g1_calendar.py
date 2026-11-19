# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Days of the Week, Months of the Year and the Calendar (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_calendar.py
The days of the week and the months of the year in order, Philippine holidays, reading a calendar, and time problems
with days and months (own makers and Ontario Grade 1 makers).
Wrong answers come from real mistakes: starting the week on the wrong day, mixing up June and July, and counting
the starting day when counting on.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_caon_math_g1_calendar as cac
adopt(cac)
if hasattr(cac, 'R'): cac.R = random.Random(701240)
ph_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
EVENTS = [("Christmas", "December"), ("New Year's Day", "January"), ("Independence Day", "June"), ("Rizal Day", "December"),
          ("All Saints' Day", "November"), ("Valentine's Day", "February"), ("Bonifacio Day", "November")]


def one_day(r):
    i = r.randrange(7)
    kind = r.choice(["after", "before", "two", "school"])
    if kind == "after":
        right = DAYS[(i + 1) % 7]
        return mcq("What day comes after <b>%s</b>?" % DAYS[i], right, [DAYS[(i - 1) % 7], DAYS[(i + 2) % 7], DAYS[i]], "%s, <b>%s</b>." % (DAYS[i], right))
    if kind == "before":
        right = DAYS[(i - 1) % 7]
        return mcq("What day comes before <b>%s</b>?" % DAYS[i], right, [DAYS[(i + 1) % 7], DAYS[(i - 2) % 7], DAYS[i]], "<b>%s</b>, %s." % (right, DAYS[i]))
    if kind == "two":
        k = r.randint(2, 4)
        right = DAYS[(i + k) % 7]
        return mcq("Today is %s. What day will it be in %d days?" % (DAYS[i], k), right, [DAYS[(i + k - 1) % 7], DAYS[(i + k + 1) % 7], DAYS[(i - k) % 7]],
                   "Count on %d days from %s: <b>%s</b>." % (k, DAYS[i], right))
    return mcq("How many days are in a week?", 7, [5, 12, 30], "Monday to Sunday: <b>7</b> days.")


def one_month(r):
    i = r.randrange(12)
    kind = r.choice(["after", "before", "nth", "event"])
    if kind == "after":
        right = MONTHS[(i + 1) % 12]
        return mcq("What month comes after <b>%s</b>?" % MONTHS[i], right, [MONTHS[(i - 1) % 12], MONTHS[(i + 2) % 12], MONTHS[(i + 6) % 12]], "%s, <b>%s</b>." % (MONTHS[i], right))
    if kind == "before":
        right = MONTHS[(i - 1) % 12]
        return mcq("What month comes before <b>%s</b>?" % MONTHS[i], right, [MONTHS[(i + 1) % 12], MONTHS[(i - 2) % 12], MONTHS[(i + 6) % 12]], "<b>%s</b>, %s." % (right, MONTHS[i]))
    if kind == "nth":
        return mcq("Which month is the <b>%s</b> month of the year?" % ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"][i], MONTHS[i],
                   [MONTHS[(i + 1) % 12], MONTHS[(i - 1) % 12], MONTHS[(i + 3) % 12]], "Count the months from January: <b>%s</b>." % MONTHS[i])
    ev, m = r.choice(EVENTS)
    j = MONTHS.index(m)
    return mcq("In which month is <b>%s</b>?" % ev, m, [MONTHS[(j + 1) % 12], MONTHS[(j - 1) % 12], MONTHS[(j + 5) % 12]], "%s is in <b>%s</b>." % (ev, m))


def one_cal(r):
    m = r.choice(MONTHS)
    start = r.randrange(7)
    nd = 31 if m in ("January", "March", "May", "July", "August", "October", "December") else 30 if m != "February" else 28
    d = r.randint(1, nd)
    day = DAYS[(start + d - 1) % 7]
    kind = r.choice(["day", "count"])
    if kind == "day":
        q = "The 1st of %s is a %s. What day is %s %d?" % (m, DAYS[start], m, d)
        return mcq(q, day, [DAYS[(start + d) % 7], DAYS[(start + d - 2) % 7], DAYS[(start + d + 2) % 7]],
                   "Every 7 days the same day comes back. %s %d is <b>%s</b>." % (m, d, day))
    w = r.randint(1, 4)
    return mcq("How many days are in %d week%s?" % (w, "s" if w > 1 else ""), 7 * w, [7 * w + 7, 5 * w, w + 7], "%d × 7 = <b>%d</b> days." % (w, 7 * w))


def build():
    sets, R = build_sets([
        ("Days of the week", [("collect", uniq(one_day), 20)]),
        ("Months of the year", [("collect", uniq(one_month), 20)]),
        ("Read a calendar", [("run", cac.set_read, (), 20)]),
        ("Days and dates", [("collect", uniq(one_cal), 20)]),
        ("Calendar problems", [("run", cac.set_count, (), 20)]),
    ], 70124)
    finish(sets, R)
    body = lesson('<ul><li>The 7 days of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.</li><li>The 12 months: January, February, March, April, May, June, July, August, September, October, November, December.</li><li>A calendar shows the days of a month in rows of 7.</li><li>Every 7 days, the same day of the week comes back.</li></ul>',
        [example("Today is Friday. What day is it in 3 days?", ["Saturday, Sunday, Monday"], "Monday")],
        [['Wrong order', 'Say the days in order every morning.'], ['June or July?', 'June is the 6th month; July is the 7th.'], ['Counting today', 'Count on from the next day.']])
    faq = [('What does MATATAG Math 1 ask about the calendar?', 'Give the days of the week and months of the year in the correct order, determine the day and month using a calendar, and solve problems involving days in a week and months in a year.'), ('How many months are in a year?', '12.'), ('Which month has the fewest days?', 'February.'), ('When is Philippine Independence Day?', 'June 12.')]
    make('days-of-the-week-and-months-of-the-year', 24, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Give the days of the week and months of the year in the correct order; determine the day and month of the year using a calendar; solve problems involving time (hour, half hour, quarter hour, days in a week, and months in a year).',
         'Days of the Week, Months of the Year and the Calendar', 'Days and Months',
         'Free Grade 1 calendar worksheets for the DepEd MATATAG curriculum: days of the week, months of the year, reading a calendar and problems. 100 questions with answers.',
         '7 days in a week, 12 months in a year.', 'Every 7 days the same day comes back.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
