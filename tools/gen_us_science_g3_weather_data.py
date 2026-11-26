# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Weather Data and Seasons (3-ESS2-1)
  python tools/gen_us_science_g3_weather_data.py
Represent data in tables and graphical displays to describe typical weather conditions expected during a
particular season: average temperature and precipitation by month or season, weather tools
(thermometer, rain gauge, wind vane, anemometer), and predicting typical weather from patterns.
Assessment boundary: graphs are bar graphs, pictographs and tables (no climate change).
Wrong answers come from real mistakes: "one cold day means the season is winter", "the rainiest month
is the hottest", "a rain gauge measures wind".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(30113)
R = U.R
P = People(R)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FULL = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
        "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"}
SEASON = {"Dec": "winter", "Jan": "winter", "Feb": "winter", "Mar": "spring", "Apr": "spring", "May": "spring", "Jun": "summer", "Jul": "summer", "Aug": "summer",
          "Sep": "fall", "Oct": "fall", "Nov": "fall"}
TOWNS = ["Maple Falls", "Cedar City", "Pine Grove", "Lake Town", "Riverside", "Hill Valley", "Sun Prairie", "Fox Hollow", "Elm Park", "Stone Creek"]


def temps():
    base = R.randint(-2, 8)
    amp = R.randint(10, 14)
    import math
    out = []
    for i in range(12):
        v = base + amp + amp * math.sin((i - 3.5) / 12 * 2 * math.pi) * 1.0
        out.append(int(round(v + R.uniform(-1, 1))))
    return out


def g_temp():
    town = R.choice(TOWNS)
    ts = temps()
    show = R.choice([[0, 2, 4, 6, 8, 10], [1, 3, 5, 7, 9, 11]])
    labs = [MONTHS[i] for i in show]
    vals = [ts[i] for i in show]
    if min(vals) < 0:
        return None
    ch = bar_chart(labs, vals, "°C", "bar graph of average temperature by month", ymax=40, step=10, w=380)
    k = R.choice(["hot", "cold", "season"])
    if k == "hot":
        m = labs[vals.index(max(vals))]
        if vals.count(max(vals)) > 1:
            return None
        return item(fig(ch) + "The graph shows the average temperature in %s. Which of these months is warmest?" % town, FULL[m], [FULL[x] for x in R.sample([l for l in labs if l != m], 3)],
                    "%s has the tallest bar (%d °C)." % (FULL[m], max(vals)))
    if k == "cold":
        m = labs[vals.index(min(vals))]
        if vals.count(min(vals)) > 1:
            return None
        return item(fig(ch) + "The graph shows the average temperature in %s. Which of these months is coldest?" % town, FULL[m], [FULL[x] for x in R.sample([l for l in labs if l != m], 3)],
                    "%s has the shortest bar (%d °C)." % (FULL[m], min(vals)))
    return item(fig(ch) + "In %s, during which season is the weather usually warmest?" % town, "summer", ["winter", "fall", "spring"],
                "The tallest bars are in the summer months.")


def g_rain():
    town = R.choice(TOWNS)
    seasons = ["winter", "spring", "summer", "fall"]
    vals = R.sample([20, 30, 40, 50, 60, 70, 80, 90], 4)
    rows = [[s, "%d mm" % v] for s, v in zip(seasons, vals)]
    tab = table(["Season", "Average rain"], rows)
    k = R.choice(["most", "least", "compare"])
    if k == "most":
        s = seasons[vals.index(max(vals))]
        return item(tab + "This table shows the average rain each season in %s. Which season usually gets the most rain?" % town, s, [x for x in seasons if x != s],
                    "%s: %d mm, the largest amount." % (s.capitalize(), max(vals)))
    if k == "least":
        s = seasons[vals.index(min(vals))]
        return item(tab + "This table shows the average rain each season in %s. Which season is usually the driest?" % town, s, [x for x in seasons if x != s],
                    "%s: only %d mm." % (s.capitalize(), min(vals)))
    a, b = R.sample(range(4), 2)
    d = abs(vals[a] - vals[b])
    return item(tab + "Compare %s and %s. How much more rain does %s usually get in the wetter of the two seasons?" % (seasons[a], seasons[b], town), "%d mm more" % d,
                ["%d mm more" % (vals[a] + vals[b]), "%d mm more" % max(vals[a], vals[b]), "the same amount"],
                "%d − %d = %d mm." % (max(vals[a], vals[b]), min(vals[a], vals[b]), d))


TOOLS = [("thermometer", "temperature"), ("rain gauge", "how much rain fell"), ("wind vane", "which way the wind is blowing"),
         ("anemometer", "how fast the wind is blowing"), ("barometer", "air pressure")]


def g_tool():
    t, what = R.choice(TOOLS)
    p = P.next()
    if R.random() < 0.5:
        return item("%s wants to measure %s. Which tool should %s use?" % (p[0], what, p[1]), "a " + t if t[0] not in "aeiou" else "an " + t,
                    [("an " if x[0] in "aeiou" else "a ") + x for x, _ in R.sample([y for y in TOOLS if y[0] != t], 3)], "A %s measures %s." % (t, what))
    return item("%s reads a %s at the school weather station. What does it measure?" % (p[0], t), what, [w for x, w in R.sample([y for y in TOOLS if y[0] != t], 3)],
                "A %s measures %s." % (t, what))


def g_predict():
    town = R.choice(TOWNS)
    ts = temps()
    rows = [[FULL[m], "%d °C" % ts[i]] for i, m in enumerate(MONTHS) if i % 2 == 0]
    if min(ts[::2]) < -5:
        return None
    m = R.choice(["Jan", "Jul"])
    t = ts[MONTHS.index(m)]
    if m == "Jul":
        exp, opts = "warm or hot weather", ["cold weather, maybe snow", "freezing weather with ice", "the coldest weather of the year"]
    elif t <= 2:
        exp, opts = "cold weather, maybe snow", ["hot weather", "warm beach weather", "the warmest weather of the year"]
    elif t <= 14:
        exp, opts = "cool weather", ["hot weather", "warm beach weather", "the warmest weather of the year"]
    else:
        return None
    p = P.next()
    return item(table(["Month", "Average temperature"], rows) + "%s is planning a trip to %s in %s. Based on the data, what weather should %s expect?" % (p[0], town, FULL[m], p[1]),
                exp, opts, "The average temperature in %s is %d °C." % (FULL[m], t))


B1 = bank([
    ("What is weather?", "what the air outside is like at a certain time and place", ["the same as climate", "the shape of the land", "the time of day"],
     "Temperature, rain, wind and clouds are parts of weather."),
    ("Which tool measures temperature?", "a thermometer", ["a rain gauge", "a wind vane", "a ruler"], "Thermometers show degrees Celsius or Fahrenheit."),
    ("Which tool shows which way the wind is blowing?", "a wind vane", ["a thermometer", "a rain gauge", "a balance"], "The arrow points into the wind."),
    ("Why do scientists record weather for many years?", "to find patterns and know what weather is typical in each season", ["to change the weather", "to make it rain", "to stop storms"],
     "Patterns help us predict."),
    ("In most of the United States, which season is usually the coldest?", "winter", ["summer", "spring", "fall"], "December, January and February are winter months."),
    ("Which months are summer in the United States?", "June, July and August", ["December, January and February", "March, April and May", "September, October and November"],
     "Summer is the warmest season in most places."),
    ("One day in April is very cold. Does this mean April is a winter month?", "No. One day is weather; the typical pattern is shown by many years of data.", ["Yes, always.", "Yes, if it snows.", "Only in Alaska."],
     "Typical weather comes from averages."),
    ("What does precipitation mean?", "water that falls from clouds, like rain, snow, sleet or hail", ["wind", "sunshine", "fog only"], "Rain gauges measure it."),
])
B5 = bank([
    ("Ava records the temperature every day for a month. What is the best way to show her data?", "a line graph or bar graph", ["a map of the world", "a poem", "a single number"],
     "Graphs show patterns clearly."),
    ("Leo's class finds that their town gets the most snow in January. What should they expect next January?", "a good chance of snow", ["no chance of snow", "hot weather", "a hurricane for sure"],
     "Patterns help predict typical weather."),
    ("Mia's rain gauge shows 12 mm on Monday and 8 mm on Tuesday. How much rain fell in all?", "20 mm", ["4 mm", "12 mm", "8 mm"], "12 + 8 = 20 mm."),
    ("A town's average July temperature is 30 °C. What clothes should a visitor pack?", "shorts, T-shirts and a sun hat", ["a heavy winter coat", "snow boots", "a wool hat and mittens"],
     "30 °C is hot."),
    ("Noah compares two towns. Town A's average January temperature is −5 °C and Town B's is 15 °C. Which town is more likely to have snow in January?", "Town A", ["Town B", "both equally", "neither"],
     "Below 0 °C, water freezes and snow is likely."),
])


def body():
    think = ("<p><b>Weather</b> is what the air is like at a certain time and place: temperature, precipitation (rain or snow), wind and clouds.</p>"
             "<p>Scientists measure weather with tools: a <b>thermometer</b> (temperature), a <b>rain gauge</b> (rain), a <b>wind vane</b> (wind direction) and an <b>anemometer</b> (wind speed).</p>"
             "<p>When we record weather for many years and show it in <b>tables and graphs</b>, we see <b>patterns</b>. "
             "These patterns tell us the <b>typical</b> weather for each season, so we can predict what a January or July will usually be like.</p>")
    ex = [("A graph shows July has the tallest temperature bar. What does this mean?", ["Tallest bar = highest temperature."], "July is usually the warmest month."),
          ("Which tool measures rain?", ["Rain is collected and measured."], "a rain gauge")]
    mist = ["Thinking one unusual day tells you the season's typical weather.",
            "Mixing up the tools: a rain gauge measures rain, not wind.",
            "Reading the wrong bar or row on a graph or table."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Weather and weather tools", B1 + [(g_tool, 6), (g_temp, 6)]),
        ("Temperature graphs", [(g_temp, 14), (g_tool, 6)]),
        ("Rain and snow data", [(g_rain, 14), (g_tool, 6)]),
        ("Predicting typical weather", [(g_predict, 10), (g_temp, 5), (g_rain, 5)]),
        ("Weather investigations", B5 + [g_temp, g_rain, g_predict, g_tool]),
    ])
    make("grade-3", "weather-data", 13, "3-ESS2-1",
         "Represent data in tables and graphical displays to describe typical weather conditions expected during a particular season.",
         "Weather Data and Seasons",
         "Grade 3 Weather Worksheets: Weather Tools, Graphs and Typical Weather by Season",
         "Weather Data",
         "Free Grade 3 science worksheets on weather data (NGSS 3-ESS2-1): thermometers and rain gauges, temperature bar graphs, rain tables and predicting typical weather for each season. 100 practice questions with answers.",
         "Weather data shows patterns for each season.",
         "Graphs and tables of temperature and rain help us know what weather to expect in winter, spring, summer and fall.",
         body(),
         [("How do we know what weather to expect in a season?", "Scientists record weather for many years. Graphs and tables of the data show the typical weather for each season."),
          ("What tools measure weather?", "A thermometer measures temperature, a rain gauge measures rain, a wind vane shows wind direction and an anemometer measures wind speed."),
          ("What is precipitation?", "Water that falls from clouds, such as rain, snow, sleet or hail.")],
         sets)


if __name__ == "__main__":
    main()
