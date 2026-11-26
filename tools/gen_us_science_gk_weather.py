# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Weather (K-ESS2-1)
  python tools/gen_us_science_gk_weather.py
Use and share observations of local weather conditions to describe patterns over time.
Sunny, cloudy, rainy, snowy, windy and stormy; a weather chart for a week; counting days of each kind; afternoons are
usually warmer than mornings; summer is warmer than winter. Very short sentences; almost every question has a picture.
Wrong answers come from real mistakes: "it snows in summer", "mornings are warmer than afternoons", "count only the first row".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, bar_chart, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9106)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


W = {"sun": "sunny", "cloud": "cloudy", "rain": "rainy", "snow": "snowy", "wind": "windy", "storm": "stormy"}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def g_word():
    k = R.choice(sorted(W))
    who = P.next()[0]
    if not once(("w", k)):
        return None
    return item(fig(K.card(k)) + "%s looks out the window. What is the weather?" % who, W[k], R.sample([W[x] for x in W if x != k], 3), "The picture shows %s weather." % W[k])


WEAR = {"rain": ("a raincoat and boots", "umbrella"), "snow": ("a warm coat, hat and mittens", "coat"), "sun": ("a sun hat and shorts", "hat"),
        "wind": ("a jacket that zips up", "coat"), "cloud": ("a light sweater", None), "storm": ("stay inside", "house")}


def g_wear():
    k = R.choice(sorted(WEAR))
    who = P.next()[0]
    if not once(("we", k)):
        return None
    a = WEAR[k][0]
    w = R.sample([WEAR[x][0] for x in WEAR if x != k and not (k in ("snow", "wind") and x in ("snow", "wind"))], 3)
    return item(fig(K.card(k)) + "It is %s. What should %s wear or do?" % (W[k], who), a, w, "Dress for the weather.")


def week_svg(ws):
    s = ""
    for i, (d, k) in enumerate(zip(DAYS, ws)):
        x = 40 + i * 72
        s += "<rect x='%d' y='6' width='66' height='96' rx='6' fill='#fff' stroke='%s' stroke-width='1.4'/>" % (x - 33, INK)
        s += text(x, 24, d, 13) + K.icon(k, x, 64, 0.55)
    return svg_wrap(40 + 5 * 72 - 6, 108, s, "weather chart: " + ", ".join("%s %s" % (d, W[k]) for d, k in zip(DAYS, ws)))


def g_week():
    pool = R.choice([["sun", "cloud", "rain"], ["sun", "cloud", "wind"], ["snow", "cloud", "sun"], ["rain", "cloud", "storm"]])
    ws = [R.choice(pool) for _ in DAYS]
    cnt = {k: ws.count(k) for k in set(ws)}
    who = P.next()[0]
    q = R.choice(["count", "most", "day"])
    if not once(tuple(ws)) or not once(("q", q), 20):
        return None
    pic = fig(week_svg(ws))
    if q == "count":
        k = R.choice(sorted(cnt))
        n = cnt[k]
        return item(pic + "%s made this weather chart. How many days were %s?" % (who, W[k]), str(n), [str(x) for x in [n + 1, n - 1 if n > 1 else n + 2, n + 2 if n > 1 else n + 3]],
                    "Count the %s pictures: %d." % (W[k], n))
    if q == "most":
        top = max(cnt.values())
        tops = [k for k in cnt if cnt[k] == top]
        if len(tops) != 1:
            return None
        a = W[tops[0]]
        return item(pic + "Look at %s's chart. Which weather happened the most this week?" % who, a, [W[x] for x in pool if W[x] != a] + ["They were all the same."], "%s: %d days." % (a.capitalize(), top))
    d = R.randrange(5)
    a = W[ws[d]]
    return item(pic + "In %s's chart, what was the weather on %s?" % (who, {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}[DAYS[d]]), a,
                R.sample([W[x] for x in W if W[x] != a], 3), "Find the day and look at the picture.")


def g_month():
    who = P.next()[0]
    season = R.choice(["winter", "spring", "summer", "fall"])
    data = {"winter": [("sunny", 8), ("cloudy", 9), ("snowy", 11), ("rainy", 2)], "spring": [("sunny", 10), ("cloudy", 8), ("rainy", 12), ("snowy", 0)],
            "summer": [("sunny", 20), ("cloudy", 6), ("rainy", 4), ("snowy", 0)], "fall": [("sunny", 12), ("cloudy", 10), ("rainy", 8), ("snowy", 0)]}[season]
    data = [(a, max(0, b + R.randint(-1, 1))) for a, b in data]
    if len({b for _, b in data}) < 4:
        return None
    k = R.choice(["most", "least", "season"])
    if not once((season, k)):
        return None
    labs = [a for a, _ in data]
    vals = [b for _, b in data]
    ch = bar_chart(labs, vals, "days", "bar graph of the weather for one month: " + ", ".join("%s %d" % (a, b) for a, b in data), ymax=22, step=2, w=320)
    if k == "most":
        a = labs[vals.index(max(vals))]
        return item(fig(ch) + "%s's class counted the weather for a month. Which weather happened most?" % who, a, [x for x in labs if x != a], "The tallest bar: %s." % a)
    if k == "least":
        a = labs[vals.index(min(vals))]
        return item(fig(ch) + "%s's class counted the weather for a month. Which weather happened least?" % who, a, [x for x in labs if x != a], "The shortest bar: %s." % a)
    return item(fig(ch) + "%s's class counted the weather for a month. Which season was it most likely?" % who, season, [x for x in ["winter", "spring", "summer", "fall"] if x != season],
                {"winter": "Snowy days mean winter.", "spring": "Lots of rain and no snow: spring.", "summer": "Mostly sunny and warm: summer.", "fall": "A mix of sun and clouds and some rain: fall."}[season])


TEMP = [("morning", "afternoon", "the afternoon", "The sun warms the air during the day."), ("summer", "winter", "summer", "Summer is the warmest season."),
        ("a sunny day", "a cloudy day", "a sunny day", "Sunshine warms the air."), ("noon", "midnight", "noon", "The sun is up at noon."),
        ("winter", "spring", "spring", "It gets warmer in spring."), ("a snowy day", "a sunny summer day", "a sunny summer day", "Summer days are warm.")]


def g_temp():
    a, b, ans, why = R.choice(TEMP)
    who = P.next()[0]
    if not once(a + b):
        return None
    x, y = (a, b) if R.random() < 0.5 else (b, a)
    other = b if ans == a or ans == "the " + a else a
    ans_txt = ans
    oth_txt = ("the " + other) if ans.startswith("the ") else other
    return item("%s checks the thermometer. Which is usually warmer: %s or %s?" % (who, x, y), ans_txt, [oth_txt, "They are always the same.", "It is never warm."], why)


CLUE = [("Dark clouds fill the sky and you hear thunder.", "a storm is coming"), ("Flags flap and leaves blow across the yard.", "it is windy"),
        ("There are puddles everywhere and the grass is wet.", "it rained"), ("Icicles hang from the roof.", "it is very cold"),
        ("People wear sunglasses and there are no clouds.", "it is sunny"), ("White flakes fall and cover the cars.", "it is snowing"),
        ("Gray clouds cover the whole sky, but nothing falls.", "it is cloudy"), ("A rainbow appears after a shower.", "the sun came out after rain")]


def g_clue():
    c, a = R.choice(CLUE)
    who = P.next()[0]
    if not once(c):
        return None
    return item("%s looks outside. %s What does this tell %s?" % (who, c, who), a, R.sample([x[1] for x in CLUE if x[1] != a], 3), "Clues tell us about the weather.")


SEAS = [("January", "snowy and cold", "winter"), ("July", "hot and sunny", "summer"), ("April", "rainy and mild", "spring"), ("October", "cool with falling leaves", "fall"),
        ("December", "cold, maybe snowy", "winter"), ("August", "hot and sunny", "summer"), ("May", "warm with spring showers", "spring"), ("November", "chilly and windy", "fall")]


def g_seas():
    m, a, s_ = R.choice(SEAS)
    who = P.next()[0]
    if not once(m):
        return None
    w = R.sample(sorted({x[1] for x in SEAS if x[2] != s_}), 3)
    return item(fig(K.card({"winter": "snow", "summer": "sun", "spring": "rain", "fall": "leaf"}[s_])) + "In many places in the United States, what is the weather often like in %s, %s asks." % (m, who) if False else
                fig(K.card({"winter": "snow", "summer": "sun", "spring": "rain", "fall": "leaf"}[s_])) + "%s asks: what is the weather often like in %s?" % (who, m), a, w, "%s is in %s." % (m, s_))


B1 = bank([
    ("What is weather?", "what the sky and air are like outside", ["a kind of animal", "a toy", "a food"], "Sunny, rainy, windy..."),
    ("What tool tells how warm it is?", "a thermometer", ["a ruler", "a spoon", "a clock"], "It measures temperature."),
    ("When does it usually snow?", "in winter", ["in summer", "on hot days", "in the desert in July"], "Snow needs cold."),
    ("What do you see on a rainy day?", "rain falling from clouds", ["snowflakes on a hot day", "a bright sun and no clouds", "leaves growing on snow"], "Rain comes from clouds."),
    ("How can you tell it is windy?", "trees and flags move", ["the sun is out", "the ground is dry", "it is quiet"], "Wind moves things."),
    ("Why do we keep a weather chart?", "to see patterns over time", ["to color pictures", "to make it rain", "to stop the wind"], "Patterns help us predict."),
    ("What should you do in a thunderstorm?", "go inside", ["play in a field", "stand under a tall tree", "swim in a lake"], "Stay safe."),
    ("Which season is usually the hottest?", "summer", ["winter", "fall", "spring"], "Summer is warm."),
])
B5 = bank([
    ("Ava's chart shows 3 rainy days and 2 sunny days. How many days in all?", "5", ["3", "2", "6"], "3 + 2 = 5."),
    ("Leo's chart shows snow every day in January. What pattern is that?", "Winter is cold and snowy.", ["Winter is hot.", "January is summer.", "It never snows."], "Weather patterns repeat."),
    ("Mia checks the temperature at 8 a.m. and 2 p.m. When is it warmer?", "2 p.m.", ["8 a.m.", "They are always the same.", "midnight"], "Afternoons are warmer."),
    ("Kai sees dark clouds and hears thunder. What will probably happen?", "a storm with rain", ["a sunny day", "snow in summer", "nothing"], "Dark clouds bring storms."),
    ("Zoe's class counts 20 sunny days in a month. Which month is it most likely?", "July", ["January", "December", "February"], "Summer months are often sunny."),
])


def body():
    pic = K.row(["sun", "cloud", "rain", "snow", "wind"], words=["sunny", "cloudy", "rainy", "snowy", "windy"], size=80)
    ex = [("The picture shows rain. What is the weather?", ["Look at the picture."], "rainy"),
          ("Is the morning or the afternoon warmer?", ["The sun warms the air all day."], "the afternoon")]
    mist = ["Thinking it snows in summer.",
            "Thinking mornings are warmer than afternoons.",
            "Counting only some of the days on the chart."]
    return kid_lesson(pic, "Look at the sky every day.",
                      ["Weather can be sunny, cloudy, rainy, snowy or windy.", "A chart shows patterns.", "Summer is warm. Winter is cold."], ex, mist)


def main():
    sets = U.sets([
        ("What is the weather?", B1 + [(g_word, 6), (g_wear, 6)]),
        ("Weather clues", [(g_clue, 8), (g_week, 8), (g_temp, 4)]),
        ("Weather charts", [(g_week, 14), (g_month, 6)]),
        ("Seasons and weather", [(g_seas, 8), (g_month, 4), (g_temp, 2), (g_week, 6)]),
        ("Weather watchers", B5 + [(g_week, 13), (g_month, 2)]),
    ])
    make("kindergarten", "weather", 6, "K-ESS2-1",
         "Use and share observations of local weather conditions to describe patterns over time.",
         "Weather",
         "Kindergarten Weather Worksheets: Sunny, Rainy, Snowy and Weather Charts",
         "Weather",
         "Free kindergarten science worksheets on weather (NGSS K-ESS2-1): weather words, what to wear, weekly weather charts and patterns over time. 100 picture questions with answers.",
         "Weather changes every day.",
         "Sunny, cloudy, rainy, snowy or windy. Charts show patterns.",
         body(),
         [("What kinds of weather are there?", "Sunny, cloudy, rainy, snowy, windy and stormy."),
          ("What patterns can kids see?", "Afternoons are usually warmer than mornings, and summer is warmer than winter. Snow comes in winter."),
          ("How do you make a weather chart?", "Each day, look outside and draw or stamp the weather. At the end of the week, count each kind.")],
         sets)


if __name__ == "__main__":
    main()
