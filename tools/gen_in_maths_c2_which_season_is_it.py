# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 9: Which Season is it? (Measurement of Time)
Days of the week, months of the year and their order, reading a calendar, days in a month, seasons in India (AU Year 2 calendar
set makers and own makers)."""
from in_prim import unit, mod, rn, co, mcq
ca = mod("gen_au_maths_y2_calendars", 602091)
on = mod("gen_caon_math_g1_calendar", 602092)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS = {"January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30, "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31}
WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def one_month(r):
    kind = r.choice(["after", "before", "days", "num", "week"])
    i = r.randrange(12)
    m = MONTHS[i]
    if kind == "after":
        return mcq("Which month comes just after <b>%s</b>?" % m, MONTHS[(i + 1) % 12], [MONTHS[(i - 1) % 12], MONTHS[(i + 2) % 12], MONTHS[(i + 6) % 12]], "<b>%s</b> comes after %s." % (MONTHS[(i + 1) % 12], m))
    if kind == "before":
        return mcq("Which month comes just before <b>%s</b>?" % m, MONTHS[(i - 1) % 12], [MONTHS[(i + 1) % 12], MONTHS[(i - 2) % 12], MONTHS[(i + 6) % 12]], "<b>%s</b> comes before %s." % (MONTHS[(i - 1) % 12], m))
    if kind == "days":
        return mcq("How many days are there in <b>%s</b> (not a leap year)?" % m, DAYS[m], [d for d in (28, 29, 30, 31) if d != DAYS[m]], "%s has <b>%d days</b>." % (m, DAYS[m]))
    if kind == "num":
        return mcq("Which month is the <b>%s</b> month of the year?" % ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"][i], m,
                   [MONTHS[(i + 1) % 12], MONTHS[(i - 1) % 12], MONTHS[(i + 3) % 12]], "Count from January: <b>%s</b>." % m)
    j = r.randrange(7)
    k = r.randint(2, 6)
    return mcq("Today is <b>%s</b>. What day will it be in %d days?" % (WEEK[j], k), WEEK[(j + k) % 7], [WEEK[(j + k + 1) % 7], WEEK[(j + k - 1) % 7], WEEK[(j - k) % 7]],
               "Count on %d days: <b>%s</b>." % (k, WEEK[(j + k) % 7]))


SEASON = [("Diwali usually comes in October or November. In much of India the weather is then", "getting cooler", ["very hot", "very rainy", "snowy everywhere"]),
          ("In most of India, the hottest months are", "April, May and June", ["December and January", "July and August", "October and November"]),
          ("In most of India, the rainy season (monsoon) is from about", "June to September", ["December to February", "March to April", "October to November"]),
          ("In most of north India, the coldest months are", "December and January", ["May and June", "July and August", "March and April"]),
          ("Which season brings the monsoon rains?", "The rainy season", ["Winter", "Summer", "Spring"]),
          ("In which season do we carry umbrellas most?", "The rainy season", ["Winter", "Summer", "Spring"]),
          ("In which season do we wear woollen sweaters in north India?", "Winter", ["Summer", "The rainy season", "Spring"]),
          ("In which season do we eat lots of mangoes and keep cool?", "Summer", ["Winter", "The rainy season", "Autumn"]),
          ("Republic Day, 26 January, comes in which season in north India?", "Winter", ["Summer", "The rainy season", "Spring"]),
          ("Independence Day, 15 August, comes in which season?", "The rainy season", ["Winter", "Summer", "Spring"]),
          ("How many months are there in a year?", "12", ["7", "10", "52"]),
          ("How many days are there in a week?", "7", ["5", "10", "12"])]


def one_season(r):
    q, a, w = r.choice(SEASON)
    return mcq(q if q.endswith("?") else q + " ___.", a, w, "<b>%s</b>." % a)


unit(2, "which-season-is-it", 9, "M", 9, "Which Season is it?", "Days, Months, Calendars and Seasons", "time and seasons",
     "Measurement of time: days of the week, months of the year, reading a calendar, and seasons in a year (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Which Season is it? worksheet (Joyful Mathematics Chapter 9): days of the week, months, reading a calendar, days in a month and seasons in India. 100 questions with answers.",
     "7 days make a week; 12 months make a year.", "Summer, the rainy season and winter come in turn.",
     "<ul><li>The months: January, February, March, April, May, June, July, August, September, October, November, December.</li><li>Most months have 30 or 31 days; February has 28 (29 in a leap year).</li><li>In most of India: summer (April–June), rainy season (July–September), winter (December–February).</li></ul>",
     [("What day is it 3 days after Friday?", ["Saturday, Sunday, Monday"], "Monday")],
     [["Forgetting that the week starts again after Sunday", "After Sunday comes Monday."], ["Thinking every month has 30 days", "Count on your knuckles: knuckle months have 31 days."]],
     [("How many days are in a year?", "365 days (366 in a leap year)."), ("What are the seasons in India?", "Summer, the rainy season (monsoon) and winter; many places also talk about spring and autumn.")],
     [("Months of the year", [co(one_month, 12), rn(ca, "set_order", 8)]),
      ("Reading a calendar", [rn(ca, "set_read", 20)]),
      ("Next and between", [rn(ca, "set_next", 10), rn(ca, "set_between", 10)]),
      ("Days and dates", [co(one_month, 14), rn(on, "set_count", 6)]),
      ("Seasons", [co(one_season, 12), co(one_month, 8)])], 60209)
