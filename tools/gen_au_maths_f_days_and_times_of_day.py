# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Days of the Week and Times of the Day (Australian Curriculum v9.0, AC9MFM02)
  python3 tools/gen_au_maths_f_days_and_times_of_day.py
Morning, lunchtime, afternoon and night time from pictures and familiar events, putting the events of a day
in order, the days of the week in order (before, after, missing day, weekend), and yesterday, today and
tomorrow.
Wrong answers come from real mistakes: mixing up morning and afternoon, starting the day at bedtime,
saying the day before when the day after is asked, and thinking the week starts again after Friday.
"""
import random
from f_common import Kids, mcq, finish, make, fig, figure, mistakes, sky_svg, days_svg, DAYS

R = random.Random(99901)
TIMES = ["Morning", "Lunchtime", "Afternoon", "Night time"]


# ------------------------------------------------------------ set 1: what time of day?
def set_sky(rnd):
    K = Kids(rnd)
    its = []
    desc = {"morning": "The sun is low and coming up (the arrow points up). It is <b>morning</b>.",
            "lunchtime": "The sun is high in the middle of the sky. It is <b>lunchtime</b> (the middle of the day).",
            "afternoon": "The sun is going down (the arrow points down). It is <b>afternoon</b>.",
            "night": "It is dark, with the moon and stars. It is <b>night time</b>."}
    qs = ["What time of day is it?", "Look at the sky. Is it morning, lunchtime, afternoon or night time?", "{n} looks out of the window. What time of day is it?",
          "When could this picture be?", "Which time of day does the picture show?"]
    for i in range(20):
        w = ["morning", "lunchtime", "afternoon", "night"][i % 4]
        kid = K.next()
        q = fig(sky_svg(w)) + qs[i // 4].format(n=kid["n"])
        ans = {"morning": "Morning", "lunchtime": "Lunchtime", "afternoon": "Afternoon", "night": "Night time"}[w]
        its.append(mcq(q, ans, [t for t in TIMES if t != ans], desc[w]))
    return {"title": "Times of the day", "items": its}


# ------------------------------------------------------------ set 2: when do we do it?
EVENTS = [("eat breakfast", "Morning"), ("eat lunch at school", "Lunchtime"), ("go to sleep in bed", "Night time"), ("wake up and get dressed", "Morning"),
          ("go home from school", "Afternoon"), ("see the stars", "Night time"), ("walk to school", "Morning"), ("eat a sandwich in the middle of the school day", "Lunchtime"),
          ("have dinner and a bath", "Night time"), ("play at the park after school", "Afternoon"), ("brush your teeth before school", "Morning"),
          ("hear a bedtime story", "Night time"), ("open your lunchbox at the big break", "Lunchtime"), ("have a snack when you get home from school", "Afternoon"),
          ("put on your school uniform", "Morning"), ("see the moon in a dark sky", "Night time"), ("watch the sun come up", "Morning"),
          ("go to swimming lessons after school", "Afternoon"), ("eat lunch with your class", "Lunchtime"), ("turn off the light and close your eyes", "Night time")]


def set_when(rnd):
    K = Kids(rnd)
    its = []
    for ev, ans in EVENTS:
        kid = K.next()
        q = "When does %s usually %s?" % (kid["n"], ev.replace("your", kid["his"]))
        its.append(mcq(q, ans, [t for t in TIMES if t != ans], "Most children %s %s <b>%s</b>." % (ev.replace("your", "their"), "in the" if ans in ("Morning", "Afternoon") else "at", ans.lower())))
    return {"title": "When do we do it?", "items": its}


# ------------------------------------------------------------ set 3: order of the day
DAY_ORDER = ["wake up", "eat breakfast", "go to school", "eat lunch", "go home", "eat dinner", "go to bed"]


def set_order(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        idx = sorted(rnd.sample(range(len(DAY_ORDER)), 3))
        kind = rnd.choice(["first", "last", "order"])
        key = (tuple(idx), kind)
        if key in seen:
            continue
        seen.add(key)
        ev = [DAY_ORDER[i] for i in idx]
        shown = ev[:]
        rnd.shuffle(shown)
        if shown == ev:
            shown = [ev[1], ev[2], ev[0]]
        if kind == "first":
            q = "Which happens <b>first</b> in a school day: %s?" % ", ".join(shown)
            ans = ev[0].capitalize()
            wr = [e.capitalize() for e in ev[1:]] + ["They all happen at the same time"]
            e = "The day goes in order: %s. <b>%s</b> comes first." % (", ".join(ev), ans)
        elif kind == "last":
            q = "Which happens <b>last</b> in a school day: %s?" % ", ".join(shown)
            ans = ev[-1].capitalize()
            wr = [e.capitalize() for e in ev[:-1]] + ["They all happen at the same time"]
            e = "The day goes in order: %s. <b>%s</b> comes last." % (", ".join(ev), ans)
        else:
            q = "Put these in order for a school day: %s." % ", ".join(shown)
            ans = ", ".join(ev).capitalize()
            wr = [", ".join(ev[::-1]).capitalize(), ", ".join(shown).capitalize(), ", ".join([ev[1], ev[0], ev[2]]).capitalize(), ", ".join([ev[0], ev[2], ev[1]]).capitalize()]
            e = "Start with the earliest thing: <b>%s</b>." % ans
        its.append(mcq(q, ans, wr, e))
    return {"title": "Order of the day", "items": its}


# ------------------------------------------------------------ set 4: days of the week
def set_days(rnd):
    its = []
    for i, d in enumerate(DAYS):
        nxt = DAYS[(i + 1) % 7]
        q = fig(days_svg(DAYS[max(0, i - 1):i + 1] + ["?"], hide=len(DAYS[max(0, i - 1):i + 1]))) + "Which day comes <b>after</b> %s?" % d
        its.append(mcq(q, nxt, [DAYS[(i - 1) % 7], DAYS[(i + 2) % 7], d], "The days go Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, then Monday again. After %s comes <b>%s</b>." % (d, nxt)))
    for i in [2, 4, 0, 6, 3, 5]:
        d = DAYS[i]
        prv = DAYS[(i - 1) % 7]
        its.append(mcq("Which day comes <b>before</b> %s?" % d, prv, [DAYS[(i + 1) % 7], DAYS[(i - 2) % 7], d],
                       "Count back one day from %s: <b>%s</b>." % (d, prv)))
    for start in [0, 2, 4]:
        row = [DAYS[(start + k) % 7] for k in range(4)]
        hide = 2
        q = fig(days_svg(row, hide=hide)) + "Which day is missing?"
        ans = row[hide]
        its.append(mcq(q, ans, [DAYS[(start + 4) % 7], DAYS[(start + 1) % 7] if row[1] != ans else DAYS[(start + 5) % 7], DAYS[(start + 6) % 7]], "The days go in order: %s. The missing day is <b>%s</b>." % (", ".join(row), ans)))
    its.append(mcq("How many days are in one week?", "7", ["5", "10", "12"], "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: <b>7</b> days."))
    its.append(mcq("Which two days are the weekend?", "Saturday and Sunday", ["Monday and Tuesday", "Friday and Saturday", "Sunday and Monday"], "Most children do not go to school on the weekend: <b>Saturday and Sunday</b>."))
    its.append(mcq("How many school days are in one week?", "5", ["7", "2", "6"], "Monday to Friday are school days: <b>5</b>."))
    its.append(mcq("Which day is the <b>first</b> school day of the week?", "Monday", ["Sunday", "Friday", "Tuesday"], "The school week starts on <b>Monday</b>."))
    o = its
    order = [o[0], o[7], o[1], o[13], o[16], o[2], o[8], o[3], o[14], o[17], o[4], o[9], o[5], o[15], o[18], o[6], o[10], o[11], o[19], o[12]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Days of the week", "items": order}


# ------------------------------------------------------------ set 5: yesterday, today, tomorrow
def set_yt(rnd):
    K = Kids(rnd)
    its = []
    acts = ["swimming", "library", "sport", "music", "art", "a visit to Nan", "a soccer game", "a birthday party", "a picnic", "show and tell"]
    for i in range(20):
        kid = K.next()
        t = (i * 3) % 7
        today = DAYS[t]
        kind = i % 4
        act = acts[i % len(acts)]
        if kind == 0:
            q = "Today is %s. What day will it be <b>tomorrow</b>?" % today
            ans = DAYS[(t + 1) % 7]
            its.append(mcq(q, ans, [DAYS[(t - 1) % 7], today, DAYS[(t + 2) % 7]], "Tomorrow is the next day. After %s comes <b>%s</b>." % (today, ans)))
        elif kind == 1:
            q = "Today is %s. What day was it <b>yesterday</b>?" % today
            ans = DAYS[(t - 1) % 7]
            its.append(mcq(q, ans, [DAYS[(t + 1) % 7], today, DAYS[(t - 2) % 7]], "Yesterday is the day before. Before %s comes <b>%s</b>." % (today, ans)))
        elif kind == 2:
            q = "Today is %s. %s has %s on %s. When is that?" % (today, kid["n"], act, DAYS[(t + 1) % 7])
            its.append(mcq(q, "Tomorrow", ["Yesterday", "Today", "Next year"], "%s comes straight after %s, so it is <b>tomorrow</b>." % (DAYS[(t + 1) % 7], today)))
        else:
            q = "Today is %s. %s had %s on %s. When was that?" % (today, kid["n"], act, DAYS[(t - 1) % 7])
            its.append(mcq(q, "Yesterday", ["Tomorrow", "Today", "Next week"], "%s is the day before %s, so it was <b>yesterday</b>." % (DAYS[(t - 1) % 7], today)))
    return {"title": "Yesterday, today and tomorrow", "items": its}


def body():
    return (
        "<h2>Times of the day</h2>"
        "<p>A day has <b>morning</b> (we wake up and go to school), <b>lunchtime</b> (the middle of the day), <b>afternoon</b> (we go home) and <b>night time</b> (we go to bed).</p>"
        + figure(sky_svg("morning"), "Morning: the sun is coming up.")
        + figure(sky_svg("night"), "Night time: it is dark and we see the moon.")
        + "<h2>Days of the week</h2><p>There are 7 days in a week. They always go in the same order, then start again:</p>"
        + figure(days_svg(DAYS[:4]), "Monday, Tuesday, Wednesday, Thursday …")
        + "<p>… Friday, Saturday, Sunday, then Monday again. Saturday and Sunday are the <b>weekend</b>.</p>"
        "<h2>Yesterday, today, tomorrow</h2><p><b>Yesterday</b> is the day before today. <b>Tomorrow</b> is the day after today.</p>"
        + mistakes([["Mixing up morning and afternoon", "Morning is before lunch; afternoon is after lunch"],
                    ["Saying the day before when the day after is asked", "After: count on one day. Before: count back"],
                    ["Thinking the week ends on Friday", "After Friday come Saturday and Sunday, then Monday"]]))


FAQ = [("What do Foundation students learn about time?",
        "They put the days of the week and the times of the day (morning, lunchtime, afternoon and night time) in order and connect them to familiar events (AC9MFM02). Reading clocks starts in Year 1."),
       ("How can I help my child learn the days of the week?",
        "Sing a days-of-the-week song, talk about what happens on each day (library on Tuesday, sport on Friday) and mark the days on a family calendar."),
       ("What is the difference between yesterday and tomorrow?",
        "Yesterday is the day before today and has already happened. Tomorrow is the day after today and has not happened yet."),
       ("Why talk about the order of a day?",
        "Putting events in order (wake up, breakfast, school, lunch, home, dinner, bed) builds the idea that time moves forward and prepares children for clocks and calendars.")]


def build():
    sets = [set_sky(R), set_when(R), set_order(R), set_days(R), set_yt(R)]
    finish(sets, R, max_num=12)
    make("days-and-times-of-day", 9, "AC9MFM02", "Measurement",
         "Days of the Week and Times of the Day",
         "Foundation Time Worksheets: Days of the Week, Morning, Afternoon and Night (Free, with Answers)",
         "Days and times of day",
         "Sequence days of the week and times of the day including morning, lunchtime, afternoon and night time, and connect them to familiar events and actions.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on days of the week and times of the day, matched to the Australian Curriculum (AC9MFM02): morning, lunchtime, afternoon, night time, order of the day, yesterday and tomorrow. 100 questions with answers.",
         "There are 7 days in a week, always in the same order.",
         "Morning, lunchtime, afternoon, night time. Yesterday is before today; tomorrow is after.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
