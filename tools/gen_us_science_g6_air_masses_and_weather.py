# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Air Masses and Weather (MS-ESS2-5)
  python tools/gen_us_science_g6_air_masses_and_weather.py
Air masses (maritime/continental, tropical/polar) move and meet at fronts, causing weather changes:
cold front (warm air pushed up fast, thunderstorms, then cooler and drier), warm front (light, steady rain,
then warmer), high pressure (clear, calm), low pressure (clouds and precipitation). Data tables of
temperature, pressure and humidity over time used to infer a front passed.
Assessment boundary: no weather map symbols beyond fronts and H/L; no calculations.
Wrong answers come from real mistakes: "a cold front brings warmer weather", "low pressure means clear skies",
"air masses take on the weather of where they are going, not where they formed".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(60109)
R = U.R
P = People(R)

MASS = {"maritime tropical": ("over warm ocean water near the equator", "warm and humid", ["the Gulf of Mexico", "the warm Atlantic near Florida", "the Pacific near Hawaii"]),
        "continental tropical": ("over hot, dry land", "hot and dry", ["the deserts of northern Mexico", "the deserts of the Southwest"]),
        "maritime polar": ("over cold ocean water", "cool and humid", ["the North Pacific", "the cold North Atlantic"]),
        "continental polar": ("over cold land far north", "cold and dry", ["northern Canada", "central Canada in winter"])}


def g_mass():
    k = R.choice(sorted(MASS))
    where, what, places = MASS[k]
    pl = R.choice(places)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s learns that an air mass formed over %s. What will it most likely be like?" % (who, pl), what, [MASS[x][1] for x in MASS if x != k],
                    "Air masses take on the temperature and humidity of where they form: %s." % where)
    return item("%s reads about a %s air mass. Where did it most likely form?" % (who, what), pl, R.sample([p for x in MASS if x != k for p in MASS[x][2]], 3),
                "A %s air mass forms %s." % (k, where))


FRONT = {"cold front": ("A cold air mass pushes under a warm air mass and forces it up quickly.", "thunderstorms or heavy rain, then cooler and drier weather"),
         "warm front": ("A warm air mass slides up over a cold air mass.", "light, steady rain or drizzle, then warmer and more humid weather"),
         "stationary front": ("Two air masses meet but neither moves much.", "many days of cloudy, wet weather"),
         "occluded front": ("A cold front catches up to a warm front and lifts the warm air off the ground.", "clouds and precipitation, often cooler")}


def g_front():
    k = R.choice(sorted(FRONT))
    how, wx = FRONT[k]
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s's forecast says a %s is coming. What weather should %s expect?" % (who, k, who), wx[0].upper() + wx[1:] + ".",
                    [FRONT[x][1][0].upper() + FRONT[x][1][1:] + "." for x in FRONT if x != k], how)
    return item("%s reads: “%s” What kind of front is this?" % (who, how), "a " + k if k[0] not in "aeiou" else "an " + k,
                [("an " if x[0] in "aeiou" else "a ") + x for x in FRONT if x != k], "That describes a %s." % k)


def g_data():
    kind = R.choice(["cold", "warm"])
    hours = ["8 a.m.", "11 a.m.", "2 p.m.", "5 p.m.", "8 p.m."]
    if kind == "cold":
        t = [R.randint(22, 26)]
        t += [t[0] + R.randint(0, 2), t[0] + R.randint(0, 1)]
        t += [t[2] - R.randint(7, 10), t[2] - R.randint(10, 13)]
        wx = ["cloudy", "cloudy", "thunderstorm", "clearing", "clear"]
    else:
        t = [R.randint(8, 12)]
        t += [t[0] + R.randint(0, 1), t[0] + R.randint(1, 2)]
        t += [t[2] + R.randint(5, 8), t[2] + R.randint(7, 10)]
        wx = ["cloudy", "drizzle", "light rain", "light rain", "cloudy"]
    if len(set(t)) < 4:
        return None
    rows = [[h, "%d °C" % x, w] for h, x, w in zip(hours, t, wx)]
    who = P.next()[0]
    tab = table(["Time", "Temperature", "Weather"], rows)
    q = R.choice(["front", "when"])
    if q == "front":
        a = "a cold front" if kind == "cold" else "a warm front"
        return item(tab + "%s recorded the weather in one day. What most likely passed through?" % who, a,
                    ["a warm front" if kind == "cold" else "a cold front", "a high-pressure system with clear skies all day", "no change in air masses"],
                    "The temperature %s after %s." % ("dropped sharply after a thunderstorm" if kind == "cold" else "rose after light, steady rain", "2 p.m." if kind == "cold" else "the rain"))
    if kind != "cold":
        return None
    return item(tab + "In %s's data, between which times did the cold front most likely pass?" % who, "2 p.m. and 5 p.m.", ["8 a.m. and 11 a.m.", "11 a.m. and 2 p.m. only", "after 8 p.m."],
                "The temperature fell from %d °C to %d °C after the thunderstorm." % (t[2], t[3]))


def g_pressure():
    k = R.choice(["high", "low", "falling", "rising"])
    who = P.next()[0]
    if k == "high":
        return item("%s sees a big H (high pressure) over the town on the weather map. What weather is likely?" % who, "clear skies and calm weather",
                    ["clouds and rain", "a thunderstorm", "a hurricane"], "Sinking air in a high-pressure area keeps clouds from forming.")
    if k == "low":
        return item("%s sees a big L (low pressure) over the town on the weather map. What weather is likely?" % who, "clouds and precipitation",
                    ["clear, sunny skies", "dry, calm weather for a week", "no weather at all"], "Rising air in a low-pressure area cools and forms clouds.")
    if k == "falling":
        return item("%s's barometer reading has been falling all morning. What does this suggest?" % who, "Stormy or rainy weather may be coming.",
                    ["Clear weather is coming.", "The barometer is measuring temperature.", "It will snow for sure."], "Falling pressure often means a low-pressure system is arriving.")
    return item("%s's barometer reading has been rising after a storm. What does this suggest?" % who, "The weather is likely clearing.",
                ["A bigger storm is coming.", "It will rain all week.", "The barometer is broken."], "Rising pressure often means a high-pressure system is arriving.")


B1 = bank([
    ("What is an air mass?", "a huge body of air with about the same temperature and humidity throughout", ["a small gust of wind", "a single cloud", "the air inside a house"],
     "Air masses can cover thousands of kilometers."),
    ("What is a front?", "the boundary where two different air masses meet", ["the front of a cloud", "a strong wind", "the top of the atmosphere"], "Weather often changes at fronts."),
    ("What causes air masses to move?", "winds and differences in air pressure", ["the moon", "ocean animals", "mountains pushing them"], "Air moves from high to low pressure."),
    ("After a cold front passes, the weather usually becomes", "cooler and drier", ["warmer and more humid", "foggy for weeks", "exactly the same"], "Cold, dry air replaces warm, moist air."),
    ("Why do cold fronts often bring thunderstorms?", "Warm, moist air is pushed up quickly, cools and forms tall clouds.", ["Cold air holds more water.", "The sun is hidden.", "The ground is wet."],
     "Fast-rising air builds storm clouds."),
    ("What does a barometer measure?", "air pressure", ["temperature", "wind speed", "rainfall"], "Changes in pressure help forecast weather."),
    ("Which air mass would bring warm, humid weather to the southeastern United States?", "maritime tropical air from the Gulf of Mexico", ["continental polar air from Canada", "dry air from the desert", "cold air from the North Pacific"],
     "Maritime = ocean (humid), tropical = warm."),
    ("Why does weather in most of the United States usually move from west to east?", "The prevailing winds (westerlies) carry air masses east.", ["The Earth is tilted east.", "The ocean pushes them east.", "Mountains push them."],
     "Forecasters look west to see what is coming."),
])
B5 = bank([
    ("Ava's weather station records a drop from 25 °C to 14 °C in two hours with a wind shift. What most likely happened?", "A cold front passed.", ["A warm front passed.", "A high-pressure system stayed.", "Nothing changed."],
     "A sharp temperature drop is a sign of a cold front."),
    ("Leo sees thin, high clouds, then thicker, lower clouds and light rain over a day, and then it gets warmer. What is this pattern?", "a warm front arriving", ["a cold front", "high pressure", "a stationary front lasting a week"],
     "Warm fronts bring gradual changes and light rain."),
    ("Mia wants to forecast tomorrow's weather. Which data would help most?", "the air masses and fronts moving toward her town from the west", ["the weather in her town last year", "the color of the sky at noon only", "the phase of the moon"],
     "Weather moves; look at what is coming."),
    ("Why are humid summer days followed by cooler days after a storm?", "A cold, dry air mass moved in behind a cold front.", ["The sun got weaker overnight.", "The storm made new air.", "Humidity always lasts forever."],
     "New air masses change the weather."),
    ("A meteorologist sees a cold air mass moving toward warm, humid air. What should she warn people about?", "possible thunderstorms as the front passes", ["a heat wave", "a drought", "no weather change"],
     "Cold fronts can bring strong storms."),
])


def body():
    think = ("<p>An <b>air mass</b> is a huge body of air with about the same temperature and humidity. It takes on the conditions of where it forms: "
             "<b>maritime</b> (over ocean, humid) or <b>continental</b> (over land, dry); <b>tropical</b> (warm) or <b>polar</b> (cold).</p>"
             "<p>Air masses move and meet at <b>fronts</b>, where weather changes:</p><ul>"
             + "".join("<li><b>%s</b>: %s Weather: %s.</li>" % (k.capitalize(), v[0], v[1]) for k, v in FRONT.items()) + "</ul>"
             "<p><b>High pressure</b> usually means clear, calm weather. <b>Low pressure</b> usually means clouds and precipitation.</p>")
    ex = [("The temperature drops 10 °C after a thunderstorm. What passed?", ["Sharp drop + storm."], "a cold front"),
          ("An air mass forms over the Gulf of Mexico. What is it like?", ["Ocean = humid.", "Near the tropics = warm."], "warm and humid")]
    mist = ["Thinking a cold front brings warmer weather.",
            "Thinking low pressure means clear skies.",
            "Forgetting that air masses keep the conditions of where they formed."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Air masses", B1 + [(g_mass, 6), (g_front, 6)]),
        ("Where air masses form", [(g_mass, 12), (g_pressure, 8)]),
        ("Fronts", [(g_front, 14), (g_pressure, 6)]),
        ("Weather data", [(g_data, 14), (g_front, 6)]),
        ("Forecasting", B5 + [g_data, g_pressure, g_mass, g_front]),
    ])
    make("grade-6", "air-masses-and-weather", 9, "MS-ESS2-5",
         "Collect data to provide evidence for how the motions and complex interactions of air masses results in changes in weather conditions.",
         "Air Masses, Fronts and Weather",
         "Grade 6 Air Masses Worksheets: Fronts, Air Pressure and Weather Changes",
         "Air Masses and Weather",
         "Free middle school science worksheets on air masses and weather (NGSS MS-ESS2-5): maritime and continental air masses, cold and warm fronts, high and low pressure, and weather data tables. 100 practice questions with answers.",
         "Weather changes when air masses meet.",
         "Cold fronts bring storms and then cooler air. Warm fronts bring light rain and then warmer air. Low pressure means clouds.",
         body(),
         [("What is an air mass?", "A huge body of air that has about the same temperature and humidity throughout, based on where it formed."),
          ("What weather does a cold front bring?", "Often thunderstorms or heavy rain, followed by cooler, drier weather."),
          ("What do high and low pressure mean for weather?", "High pressure usually brings clear, calm weather. Low pressure usually brings clouds and precipitation.")],
         sets)


if __name__ == "__main__":
    main()
