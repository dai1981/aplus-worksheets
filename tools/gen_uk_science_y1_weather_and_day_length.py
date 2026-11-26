# -*- coding: utf-8 -*-
"""
UK Year 1 science: Weather and Day Length (Seasonal changes)
  python tools/gen_uk_science_y1_weather_and_day_length.py
Observe and describe weather associated with the seasons and how day length varies: weather symbols and words, a
week's weather chart, what to do in different weather, and a table of daylight hours through the year.
Wrong answers come from real mistakes: "it is dark early in summer", "days are the same length all year", "snow is
most likely in summer", "a cloud symbol means rain".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
from uk_ks1 import card
import sci_kids as K

U = Unit(61112)
R = U.R
P = People(R)

SYM = [("sun", "sunny"), ("cloud", "cloudy"), ("rain", "rainy"), ("snow", "snowy"), ("storm", "stormy"), ("wind", "windy")]


def g_sym():
    k, w = R.choice(SYM)
    if not once(("sy", k)):
        return None
    return item(card(k) + "What weather does this symbol show?", w, R.sample([x[1] for x in SYM if x[1] != w], 3), "Weather symbols are on weather forecasts.")


DESC = [("Water drops fall from the clouds.", "rainy"), ("The sky is grey and covered in clouds, but it is dry.", "cloudy"), ("The sun is shining and the sky is blue.", "sunny"),
        ("White flakes fall and cover the ground.", "snowy"), ("Trees sway and kites fly well.", "windy"), ("There is thunder and lightning.", "stormy"),
        ("You cannot see far because the air is misty.", "foggy"), ("The grass is white and crunchy in the cold morning.", "frosty")]
WW = ["rainy", "cloudy", "sunny", "snowy", "windy", "stormy", "foggy", "frosty"]


def g_desc():
    d, w = R.choice(DESC)
    k = R.random() < 0.5
    if not once(("de", d, k)):
        return None
    near = {"stormy": {"windy", "rainy", "cloudy"}, "windy": {"stormy"}, "rainy": {"stormy", "cloudy"}, "cloudy": {"foggy", "rainy", "stormy"}, "foggy": {"cloudy"},
            "frosty": {"snowy"}, "snowy": {"frosty"}, "sunny": set()}[w]
    if k:
        return item("%s What is the weather like?" % d, w, R.sample([x for x in WW if x != w and x not in near], 3), "Look and listen to describe the weather.")
    return item("Which of these describes %s weather?" % w, d, R.sample([x[0] for x in DESC if x[0] != d and x[1] not in near], 3), "Look and listen to describe the weather.")


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def g_chart():
    who = P.next()[0]
    ws = [R.choice(["sunny", "cloudy", "rainy", "windy"]) for _ in DAYS]
    k = R.choice(["count", "day", "most"])
    t = R.choice(["sunny", "cloudy", "rainy", "windy"])
    n = ws.count(t)
    if not once(("ch", tuple(ws), k, t)):
        return None
    tab = table(["Day", "Weather"], [[d, w] for d, w in zip(DAYS, ws)])
    intro = tab + "%s kept a weather chart for a week. " % who
    if k == "count":
        g = str(n)
        return item(intro + "How many days were %s?" % t, g, [str(x) for x in range(6) if x != n][:3], "Count the %s days." % t)
    if k == "day":
        i = R.randrange(5)
        a = ws[i]
        return item(intro + "What was the weather on %s?" % DAYS[i], a, [x for x in ["sunny", "cloudy", "rainy", "windy"] if x != a], "Read the row.")
    c = {w: ws.count(w) for w in set(ws)}
    m = max(c.values())
    top = [w for w in c if c[w] == m]
    if len(top) > 1:
        return None
    a = top[0]
    return item(intro + "Which weather happened most often?", a, [x for x in ["sunny", "cloudy", "rainy", "windy"] if x != a], "Count each kind of weather.")


DO = [("sunny", "wear a sun hat and sun cream"), ("rainy", "take an umbrella and wear wellies"), ("snowy", "wear a warm coat, hat and gloves"),
      ("windy", "fly a kite"), ("foggy", "wear bright clothes so people can see you"), ("stormy", "stay indoors and keep safe")]


def g_do():
    w, d = R.choice(DO)
    k = R.random() < 0.5
    if not once(("do", w, k)):
        return None
    if k:
        return item("What is a good thing to do on a %s day?" % w, d, R.sample([x[1] for x in DO if x[1] != d], 3), "We choose clothes and games to suit the weather.")
    return item("On which kind of day would you %s?" % d, "a %s day" % w, ["a %s day" % x[0] for x in R.sample([x for x in DO if x[0] != w], 3)], "We choose clothes and games to suit the weather.")


LIGHT = {"December": 8, "March": 12, "June": 17, "September": 12}


def g_light():
    who = P.next()[0]
    ms = ["March", "June", "September", "December"]
    v = [LIGHT[m] for m in ms]
    k = R.choice(["long", "short", "read", "diff", "same", "dark"])
    ri = R.randrange(4)
    if not once(("li", k, ri if k == "read" else 0, who)) or not once(("lk", k, ri if k == "read" else 0), 2):
        return None
    tab = table(["Month", "Hours of daylight (about)"], [[m, str(x)] for m, x in zip(ms, v)])
    intro = tab + "%s found out how many hours of daylight there are in London. " % who
    if k == "long":
        return item(intro + "Which month has the longest days?", "June", ["December", "March", "September"], "Summer has the longest days.")
    if k == "short":
        return item(intro + "Which month has the shortest days?", "December", ["June", "March", "September"], "Winter has the shortest days.")
    if k == "read":
        g = "%d hours" % v[ri]
        return item(intro + "About how many hours of daylight are there in %s?" % ms[ri], g, [x for x in dict.fromkeys(["%d hours" % y for y in (8, 12, 17, 24, 10)]) if x != g][:3], "Read the row.")
    if k == "diff":
        return item(intro + "How many more hours of daylight are there in June than in December?", "9 hours", ["8 hours", "17 hours", "25 hours"], "17 − 8 = 9.")
    if k == "same":
        return item(intro + "Which two months have about the same day length?", "March and September", ["June and December", "March and June", "September and December"], "Both have about 12 hours.")
    return item(intro + "Why is it often dark when children walk home from school in December?", "The days are short in winter.", ["The days are long in winter.", "The Sun is closer in winter.", "It is always dark at 3 o'clock."], "Short winter days.")


B1 = bank([
    ("What is the weather?", "what it is like outside: sunny, rainy, windy or snowy", ["the time on a clock", "the name of a month", "a kind of plant"], "It changes every day."),
    ("When is it most likely to snow in the UK?", "in winter", ["in summer", "in July", "it never snows"], "Coldest season."),
    ("Which season usually has the most hot, sunny days?", "summer", ["winter", "autumn", "spring"], "Long, warm days."),
    ("In which season are the days longest?", "summer", ["winter", "autumn", "spring"], "It stays light until late."),
    ("In which season are the days shortest?", "winter", ["summer", "spring", "autumn"], "Dark early."),
    ("What tool measures how hot or cold it is?", "a thermometer", ["a ruler", "a clock", "a rain gauge"], "Temperature."),
    ("What does a rain gauge measure?", "how much rain falls", ["how hot it is", "how windy it is", "how long the day is"], "Collect the rain."),
    ("Which way does a windsock point?", "the way the wind is blowing", ["towards the Sun", "always north", "towards the rain"], "It shows wind direction."),
])
B5 = bank([
    ("Why do we need lights on in the morning in winter?", "The Sun rises later, so it is still dark.", ["Lights are pretty.", "The Sun rises earlier.", "It is summer."], "Short days."),
    ("Why should you never look straight at the Sun?", "It can damage your eyes.", ["It is too far away.", "It is cold.", "It is not real."], "Eye safety."),
    ("How could you find out which day of the week had the most rain?", "Measure the rain in a rain gauge each day and record it.", ["Guess.", "Look at one cloud.", "Ask a bird."], "Measure and record."),
    ("Why do weather forecasters use symbols?", "They are quick and easy to understand.", ["They are secret codes.", "Words are not allowed.", "To confuse people."], "Clear information."),
    ("Is the weather the same every day in a season?", "No. It can change from day to day.", ["Yes, always the same.", "Only in winter.", "Only in summer."], "Weather changes."),
])


def body():
    pic = K.row(["sun", "cloud", "rain", "snow", "wind"], words=["sunny", "cloudy", "rainy", "snowy", "windy"], size=74, label="weather symbols: sunny, cloudy, rainy, snowy and windy")
    ex = [("Which season has the longest days?", ["Light until late"], "summer"),
          ("White flakes fall from the sky. Weather?", ["Cold"], "snowy")]
    mist = ["Thinking days are the same length all year.", "Thinking snow is most likely in summer.", "Thinking a cloud symbol always means rain."]
    return kid_lesson(pic, "The weather changes with the seasons.",
                      ["Summer days are long and warm.", "Winter days are short and cold.", "We can record the weather on a chart."], ex, mist)


def main():
    sets = U.sets([
        ("Weather words", B1 + [(g_desc, 8), (g_sym, 4)]),
        ("Weather symbols", [(g_sym, 2), (g_desc, 8), (g_do, 10)]),
        ("Weather chart", [(g_chart, 20)]),
        ("Day length", [(g_light, 12), (g_chart, 8)]),
        ("Thinking about weather", B5 + [(g_chart, 10), (g_light, 5)]),
    ])
    make_uk(1, "weather-and-day-length", 12, "Seasonal changes",
            "Observe and describe weather associated with the seasons and how day length varies.",
            "Weather and Day Length",
            "Year 1 Science: Weather and Day Length Worksheets (Weather Charts)",
            "Weather and Day Length",
            "Free Year 1 science worksheets on weather and day length: weather symbols and words, a weather chart, what to do in different weather and how long the days are. 100 questions with answers.",
            "Weather changes with the seasons.",
            "Summer days are long; winter days are short.",
            body(),
            [("What weather do we get in each season?", "Spring has showers and warmer days, summer is warmest and sunniest, autumn is windy and wet, and winter is coldest, with frost and sometimes snow."),
             ("Why are the days longer in summer?", "In summer the Sun rises early and sets late, so there are more hours of daylight. In winter it rises late and sets early."),
             ("How can we record the weather?", "Keep a weather chart: each day, write or draw the weather. A thermometer and a rain gauge help us measure it.")],
            sets)


if __name__ == "__main__":
    main()
