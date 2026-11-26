# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Daylight and Seasons (1-ESS1-2)
  python tools/gen_us_science_g1_daylight_and_seasons.py
Make observations at different times of year to relate the amount of daylight to the time of year.
In most of the United States, summer days are long (about 15 hours of daylight in June) and winter days are short
(about 9 hours in December). Reading bar graphs and sunset tables; the order of the seasons.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "every day has the same daylight", "winter days are longest", "the sun sets later in winter".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, bar_chart, svg_wrap, People
from ws_common import text
import sci_kids as K

U = Unit(10109)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# hours of daylight (rounded, middle of the US) and sunset time
MONTH = {"January": (10, "5:00 p.m."), "February": (11, "5:40 p.m."), "March": (12, "7:15 p.m."), "April": (13, "7:45 p.m."), "May": (14, "8:15 p.m."),
         "June": (15, "8:30 p.m."), "July": (15, "8:30 p.m."), "August": (14, "8:00 p.m."), "September": (12, "7:15 p.m."), "October": (11, "6:30 p.m."),
         "November": (10, "4:45 p.m."), "December": (9, "4:30 p.m.")}
SEASON = {"December": "winter", "January": "winter", "February": "winter", "March": "spring", "April": "spring", "May": "spring",
          "June": "summer", "July": "summer", "August": "summer", "September": "fall", "October": "fall", "November": "fall"}
ORDER = list(MONTH)


def g_chart():
    ms = sorted(R.sample(ORDER, 3), key=ORDER.index)
    vals = [MONTH[m][0] for m in ms]
    if len(set(vals)) < 3:
        return None
    who = P.next()[0]
    k = R.choice(["most", "least", "diff", "season"])
    if not once((tuple(ms), k)) or not once(("k", k), 7):
        return None
    ch = bar_chart([m[:3] for m in ms], vals, "hours of daylight", "bar graph of hours of daylight: " + ", ".join("%s %d" % (m, v) for m, v in zip(ms, vals)), ymax=16, step=2, w=300)
    if k == "most":
        a = ms[vals.index(max(vals))]
        return item(fig(ch) + "%s's graph shows daylight in 3 months. Which month has the most daylight?" % who, a, [m for m in ms if m != a] + ["They are the same."], "The tallest bar: %s." % a)
    if k == "least":
        a = ms[vals.index(min(vals))]
        return item(fig(ch) + "%s's graph shows daylight in 3 months. Which month has the least daylight?" % who, a, [m for m in ms if m != a] + ["They are the same."], "The shortest bar: %s." % a)
    if k == "diff":
        x, y = sorted(zip(ms, vals), key=lambda t: -t[1])[:2]
        if x[1] == y[1]:
            return None
        lo = min(vals)
        hi = max(vals)
        xm, ym = ms[vals.index(hi)], ms[vals.index(lo)]
        d = hi - lo
        return item(fig(ch) + "Look at %s's graph. How many more hours of daylight does %s have than %s?" % (who, xm, ym), str(d), [str(hi), str(hi + lo), str(d + 2)],
                    "%d − %d = %d." % (hi, lo, d))
    a = ms[vals.index(max(vals))]
    return item(fig(ch) + "The tallest bar in %s's graph is %s. Which season is %s in?" % (who, a, a), SEASON[a], [s for s in ["winter", "spring", "summer", "fall"] if s != SEASON[a]],
                "%s is in %s." % (a, SEASON[a]))


def g_sunset():
    ms = sorted(R.sample(ORDER, 3), key=ORDER.index)
    if len({MONTH[m][1] for m in ms}) < 3 or len({MONTH[m][0] for m in ms}) < 3:
        return None
    who = P.next()[0]
    k = R.choice(["early", "late", "play"])
    if not once((tuple(ms), k)) or not once(("s", k), 8):
        return None
    tab = table(["Month", "Sunset"], [[m, MONTH[m][1]] for m in ms])
    if k == "early":
        a = min(ms, key=lambda m: MONTH[m][0])
        return item(tab + "%s writes down sunset times. In which month does it get dark earliest?" % who, a, [m for m in ms if m != a] + ["All the same."], "%s: sunset at %s." % (a, MONTH[a][1]))
    if k == "late":
        a = max(ms, key=lambda m: MONTH[m][0])
        return item(tab + "%s writes down sunset times. In which month does it stay light latest?" % who, a, [m for m in ms if m != a] + ["All the same."], "%s: sunset at %s." % (a, MONTH[a][1]))
    a = max(ms, key=lambda m: MONTH[m][0])
    return item(tab + "%s wants to play outside after dinner while it is still light. Which month is best?" % who, a, [m for m in ms if m != a] + ["All the same."],
                "%s has the latest sunset." % a)


def g_season():
    s = R.choice(["summer", "winter", "spring", "fall"])
    who = P.next()[0]
    k = R.choice(["length", "month"])
    m = R.choice([x for x in ORDER if SEASON[x] == s])
    if not once((s, k, m if k == "month" else "")):
        return None
    if k == "length":
        a = {"summer": "the longest days", "winter": "the shortest days", "spring": "days getting longer", "fall": "days getting shorter"}[s]
        return item(fig(K.card({"summer": "sun", "winter": "snow", "spring": "flower", "fall": "leaf"}[s])) + "%s notices the daylight in %s. What are the days like?" % (who, s), a,
                    [x for x in ["the longest days", "the shortest days", "days getting longer", "days getting shorter"] if x != a], "Daylight changes through the year.")
    return item("%s's birthday is in %s. What season is that?" % (who, m), s, [x for x in ["winter", "spring", "summer", "fall"] if x != s], "%s is in %s." % (m, s))


def season_row():
    return K.row(["snow", "flower", "sun", "leaf"], words=["winter", "spring", "summer", "fall"], size=90)


def g_next():
    order = ["winter", "spring", "summer", "fall"]
    i = R.randrange(4)
    k = R.choice(["next", "before"])
    who = P.next()[0]
    if not once((i, k)):
        return None
    a = order[(i + 1) % 4] if k == "next" else order[(i - 1) % 4]
    return item(fig(season_row()) + "It is %s. Which season comes %s?" % (order[i], "next" if k == "next" else "just before it"), a, [x for x in order if x != a], "Winter, spring, summer, fall, then winter again.")


def g_obs():
    who = P.next()[0]
    a = R.choice(["November", "December", "January"])
    b = R.choice(["April", "May", "June", "July", "August", "September"])
    if R.random() < 0.5:
        a, b = b, a
    if not once((a, b)):
        return None
    lon = a if MONTH[a][0] > MONTH[b][0] else b
    return item("%s walks home at 5:30 p.m. in %s and in %s. When is it more likely to still be light?" % (who, a, b), "in " + lon, ["in " + (b if lon == a else a), "It is always dark at 5:30 p.m.", "It is always light at 5:30 p.m."],
                "%s has more daylight." % lon)


B1 = bank([
    ("When are days the longest?", "in summer", ["in winter", "in fall", "never"], "Summer has the most daylight."),
    ("When are days the shortest?", "in winter", ["in summer", "in spring", "never"], "Winter has the least daylight."),
    ("Do all days have the same amount of daylight?", "No. It changes during the year.", ["Yes, always.", "Only on weekends.", "Only at the beach."], "Daylight changes."),
    ("In winter, when does it get dark?", "early, before dinner", ["very late at night", "never", "at noon"], "Short days."),
    ("In summer, when does it get dark?", "late in the evening", ["right after lunch", "never", "in the morning"], "Long days."),
    ("What are the four seasons in order?", "winter, spring, summer, fall", ["summer, winter, fall, spring", "fall, summer, spring, winter", "spring, fall, winter, summer"], "Then it repeats."),
    ("What happens to daylight from winter to summer?", "It gets longer.", ["It gets shorter.", "It stays the same.", "It goes away."], "Days grow longer in spring."),
    ("What happens to daylight from summer to winter?", "It gets shorter.", ["It gets longer.", "It stays the same.", "It doubles."], "Days shrink in fall."),
])
B5 = bank([
    ("Ava sees the sun set at 4:30 p.m. in December and 8:30 p.m. in June. How many hours later is the June sunset?", "4", ["3", "8", "12"], "8:30 − 4:30 = 4 hours."),
    ("Leo says it is darker at dinner in summer than in winter. Is he right?", "No. Summer evenings are lighter.", ["Yes.", "They are the same.", "Only on Mondays."], "Summer has longer days."),
    ("Mia records sunset every month for a year. What will she see?", "a pattern: later in summer, earlier in winter", ["the same time every day", "no pattern at all", "sunset at noon"], "It repeats each year."),
    ("Kai has 15 hours of daylight in June and 9 in December. How many more hours in June?", "6", ["24", "9", "15"], "15 − 9 = 6."),
    ("Why do we turn on lights earlier in winter evenings?", "The sun sets earlier.", ["The sun sets later.", "Lamps work better in winter.", "Snow blocks lamps."], "Shorter days."),
])


def body():
    ch = bar_chart(["Dec", "Mar", "Jun", "Sep"], [9, 12, 15, 12], "hours of daylight", "bar graph: December 9 hours, March 12, June 15, September 12", ymax=16, step=2, w=300)
    ex = [("Which month has more daylight, June or December?", ["Look at the bars."], "June"),
          ("In which season does it get dark early?", ["Short days."], "winter")]
    mist = ["Thinking every day has the same daylight.",
            "Thinking winter days are the longest.",
            "Thinking the sun sets later in winter."]
    return kid_lesson(ch, "Daylight changes during the year.",
                      ["Summer: long days.", "Winter: short days.", "The pattern repeats every year."], ex, mist)


def main():
    sets = U.sets([
        ("Long days and short days", B1 + [(g_season, 6), (g_next, 6)]),
        ("Seasons", [(g_season, 4), (g_next, 2), (g_chart, 10), (g_obs, 4)]),
        ("Daylight graphs", [(g_chart, 14), (g_obs, 4), (g_season, 2)]),
        ("Sunset times", [(g_sunset, 14), (g_obs, 3), (g_season, 3)]),
        ("Daylight detectives", B5 + [(g_chart, 4), (g_sunset, 4), (g_obs, 3), (g_season, 4)]),
    ])
    make("grade-1", "daylight-and-seasons", 9, "1-ESS1-2",
         "Make observations at different times of year to relate the amount of daylight to the time of year.",
         "Daylight and Seasons",
         "Grade 1 Daylight and Seasons Worksheets: Long Summer Days, Short Winter Days",
         "Daylight and Seasons",
         "Free grade 1 science worksheets on daylight and seasons (NGSS 1-ESS1-2): long summer days, short winter days, daylight graphs and sunset times. 100 picture questions with answers.",
         "Summer days are long.",
         "Winter days are short. The pattern repeats every year.",
         body(),
         [("Why are summer days longer?", "In summer the sun rises earlier and sets later, so there are more hours of daylight."),
          ("How much daylight is there?", "In much of the United States, about 15 hours in June and about 9 hours in December."),
          ("How can kids observe this?", "Write down the sunset time once a month, or note if it is light or dark at the same time each evening.")],
         sets)


if __name__ == "__main__":
    main()
