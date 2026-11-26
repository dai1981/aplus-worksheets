# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Climates of the World (3-ESS2-2)
  python tools/gen_us_science_g3_climates_of_the_world.py
Climate is the typical weather pattern of a place over many years; weather is what happens on one day.
Different regions have different climates: tropical (hot and rainy all year), desert (very dry),
polar (very cold), temperate (four seasons), mountain (cooler higher up).
Wrong answers come from real mistakes: "climate is today's weather", "deserts are always hot",
"places near the equator have cold winters".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(30114)
R = U.R
P = People(R)

WEATHER = ["It is raining in Chicago this afternoon.", "Yesterday it snowed 5 cm in Denver.", "Tomorrow will be sunny and windy in Boston.",
           "It is 30 °C in Miami right now.", "A thunderstorm hit Dallas last night.", "This morning was foggy in San Francisco.",
           "It hailed for ten minutes in Kansas City today.", "Today is cloudy and cool in Portland."]
CLIMATE = ["Phoenix is hot and dry most of the year.", "Alaska has long, very cold winters.", "Hawaii is warm all year round.",
           "Seattle usually gets a lot of rain in winter.", "Chicago has cold, snowy winters and warm summers.", "Rain forests are hot and wet all year.",
           "Antarctica is very cold every month of the year.", "Florida has warm winters and hot, rainy summers."]


def g_wc():
    if R.random() < 0.5:
        x = R.choice(WEATHER)
        return item("%s reads this sentence: “%s” Is it about weather or climate?" % (P.next()[0], x), "weather", ["climate", "both weather and climate the same", "neither"],
                    "It tells what is happening at one time, so it is weather.")
    x = R.choice(CLIMATE)
    return item("%s reads this sentence: “%s” Is it about weather or climate?" % (P.next()[0], x), "climate", ["weather", "both weather and climate the same", "neither"],
                "It describes the usual pattern over many years, so it is climate.")


REG = {"tropical": ("hot and rainy all year", ["the Amazon rain forest", "Hawaii", "central Africa near the equator", "Indonesia"]),
       "desert": ("very dry, with little rain", ["the Sahara", "Phoenix, Arizona", "Death Valley", "the Mojave Desert"]),
       "polar": ("very cold all year, with ice and snow", ["Antarctica", "northern Alaska", "Greenland", "the North Pole"]),
       "temperate": ("four seasons: cold winters, warm summers", ["Chicago", "New York", "Ohio", "Michigan"]),
       "mountain": ("cooler and windier as you go higher", ["the Rocky Mountains", "the top of Mount Rainier", "the Andes Mountains", "the Himalayas"])}


def g_region():
    k = R.choice(sorted(REG))
    desc, places = REG[k]
    pl = R.choice(places)
    if R.random() < 0.5:
        return item("Which climate does %s have?" % pl, "a %s climate: %s" % (k, desc), ["a %s climate: %s" % (x, REG[x][0]) for x in R.sample([y for y in REG if y != k], 3)],
                    "%s has a %s climate." % (pl[0].upper() + pl[1:], k))
    others = [x for y in REG if y != k for x in REG[y][1]]
    return item("Which place has a climate that is %s?" % desc, pl, R.sample(others, 3), "%s has a %s climate." % (pl[0].upper() + pl[1:], k))


CITIES = [("Miami", 25, 1500), ("Phoenix", 24, 200), ("Seattle", 12, 950), ("Anchorage", 3, 400), ("Chicago", 10, 950), ("Honolulu", 26, 450),
          ("Denver", 10, 400), ("Boston", 11, 1100), ("Las Vegas", 21, 100), ("New Orleans", 21, 1600), ("Minneapolis", 8, 800), ("San Diego", 18, 250)]


def g_table():
    cs = R.sample(CITIES, 4)
    if len({c[1] for c in cs}) < 4 or len({c[2] for c in cs}) < 4:
        return None
    rows = [[c[0], "%d °C" % c[1], "%d mm" % c[2]] for c in cs]
    tab = table(["City", "Average yearly temperature", "Average yearly rain"], rows)
    k = R.choice(["dry", "wet", "warm", "cold", "desert"])
    names = [c[0] for c in cs]
    tab = tab + "%s's class collected climate data for four cities. " % P.next()[0]
    if k == "dry":
        a = min(cs, key=lambda c: c[2])[0]
        return item(tab + "Which city has the driest climate?", a, [n for n in names if n != a], "%s gets the least rain each year." % a)
    if k == "wet":
        a = max(cs, key=lambda c: c[2])[0]
        return item(tab + "Which city has the wettest climate?", a, [n for n in names if n != a], "%s gets the most rain each year." % a)
    if k == "warm":
        a = max(cs, key=lambda c: c[1])[0]
        return item(tab + "Which city has the warmest climate?", a, [n for n in names if n != a], "%s has the highest average temperature." % a)
    if k == "cold":
        a = min(cs, key=lambda c: c[1])[0]
        return item(tab + "Which city has the coldest climate?", a, [n for n in names if n != a], "%s has the lowest average temperature." % a)
    hot_dry = [c for c in cs if c[1] >= 18 and c[2] <= 300]
    if len(hot_dry) != 1:
        return None
    a = hot_dry[0][0]
    return item(tab + "Which city most likely has a desert climate (warm and very dry)?", a, [n for n in names if n != a], "%s is warm and gets very little rain." % a)


def g_pack():
    p = P.next()
    trips = [("Antarctica", "a thick coat, gloves and a warm hat"), ("the Sahara Desert", "light clothes, a sun hat and lots of water"),
             ("the Amazon rain forest", "a raincoat and light clothes"), ("Hawaii in January", "shorts, a T-shirt and sunscreen"),
             ("Alaska in January", "a thick coat, boots and mittens"), ("the top of the Rocky Mountains", "a warm jacket, even in summer")]
    place, a = R.choice(trips)
    w = [x[1] for x in trips if x[1] != a and not (("coat" in a or "jacket" in a or "mittens" in a) and ("coat" in x[1] or "jacket" in x[1] or "mittens" in x[1]))]
    if len(w) < 3:
        return None
    return item("%s is going to %s. Based on the climate, what should %s pack?" % (p[0], place, p[1]), a, R.sample(w, 3), "The climate there is %s." % (
        {"Antarctica": "very cold", "the Sahara Desert": "hot and very dry", "the Amazon rain forest": "hot and rainy", "Hawaii in January": "warm all year",
         "Alaska in January": "very cold in winter", "the top of the Rocky Mountains": "cooler higher up"}[place]))


B1 = bank([
    ("What is climate?", "the usual weather in a place over many years", ["the weather on one day", "the shape of the land", "the number of people in a place"],
     "Climate is the long-term pattern."),
    ("What is the difference between weather and climate?", "Weather is what happens on one day; climate is the usual pattern over many years.", ["They are exactly the same.", "Climate changes every hour.", "Weather lasts for 100 years."],
     "Weather is short-term; climate is long-term."),
    ("Places near the equator usually have", "warm temperatures all year", ["long, freezing winters", "snow every day", "no sunlight"], "The sun shines strongly near the equator."),
    ("Places near the North and South Poles usually have", "very cold temperatures", ["hot, sunny beaches", "rain forests", "deserts with cactuses only"], "The poles get weak sunlight."),
    ("Are all deserts hot?", "No. A desert is very dry, and some deserts, like Antarctica, are cold.", ["Yes, always.", "Only at night.", "Only in summer."],
     "Deserts are defined by low rain."),
    ("Why is it often colder on top of a mountain than at the bottom?", "The air is colder higher up.", ["Mountains are made of ice.", "The sun is farther away by a lot.", "Snow makes mountains taller."],
     "Temperature drops as you go higher."),
    ("Why do scientists study climate?", "to know what weather a place usually has so people can plan", ["to change today's weather", "to stop rain", "to make deserts wet"],
     "Climate helps people choose crops, clothes and buildings."),
    ("Which region has four seasons with cold winters and warm summers?", "a temperate region", ["a tropical rain forest", "a polar region", "a hot desert"], "Much of the United States is temperate."),
])
B5 = bank([
    ("Ava reads that a town gets 2,000 mm of rain a year and is hot all year. What kind of climate does it have?", "tropical", ["polar", "desert", "temperate"],
     "Hot and very rainy all year is tropical."),
    ("Leo finds that a city gets only 100 mm of rain a year. What does this tell him about its climate?", "It is very dry, like a desert.", ["It is a rain forest.", "It snows every day.", "It is always cloudy."],
     "Very little rain means a desert climate."),
    ("Mia compares a beach town and a mountain town in the same state. Which is likely cooler?", "the mountain town", ["the beach town", "They are the same.", "You cannot compare them."],
     "Higher places are usually cooler."),
    ("Why do houses in Alaska have thick walls and small windows?", "to keep heat in during long, cold winters", ["to keep rain out of the desert", "to let in more sunlight", "to stay cool in summer"],
     "People design homes for their climate."),
    ("Farmers in a dry climate need to grow crops. Which plan fits the climate best?", "choose crops that need little water and use irrigation", ["grow rice in flooded fields", "plant crops that need daily rain", "grow plants that need snow"],
     "Plans should fit the climate."),
])


def body():
    think = ("<p><b>Weather</b> is what the air is like on one day. <b>Climate</b> is the usual weather in a place over many years.</p>"
             "<ul><li><b>Tropical</b>: hot and rainy all year (rain forests, Hawaii).</li>"
             "<li><b>Desert</b>: very dry (Phoenix, the Sahara).</li>"
             "<li><b>Polar</b>: very cold all year (Antarctica, northern Alaska).</li>"
             "<li><b>Temperate</b>: four seasons (Chicago, New York).</li>"
             "<li><b>Mountain</b>: cooler and windier higher up.</li></ul>"
             "<p>Places near the equator are warm; places near the poles are cold. We learn a place's climate from many years of weather data.</p>")
    ex = [("“It is snowing in Denver today.” Weather or climate?", ["It is about one day."], "weather"),
          ("A city gets 150 mm of rain a year. What climate is it?", ["Very little rain."], "desert")]
    mist = ["Thinking one day's weather tells you the climate.",
            "Thinking all deserts are hot. Deserts are dry.",
            "Thinking places near the equator have cold winters."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Weather or climate?", B1 + [(g_wc, 12)]),
        ("Climates of different regions", [(g_region, 14), (g_wc, 6)]),
        ("Comparing climates with data", [(g_table, 16), (g_region, 4)]),
        ("Living in different climates", [(g_pack, 6), (g_table, 8), (g_region, 6)]),
        ("Using climate information", B5 + [g_table, g_region, g_wc, g_pack]),
    ])
    make("grade-3", "climates-of-the-world", 14, "3-ESS2-2",
         "Obtain and combine information to describe climates in different regions of the world.",
         "Climates of the World",
         "Grade 3 Climate Worksheets: Weather vs. Climate and Climates of Different Regions",
         "Climates of the World",
         "Free Grade 3 science worksheets on climate (NGSS 3-ESS2-2): weather vs. climate, tropical, desert, polar, temperate and mountain climates, and comparing city climate data. 100 practice questions with answers.",
         "Climate is the usual weather of a place over many years.",
         "Tropical places are hot and rainy, deserts are dry, polar places are cold, and temperate places have four seasons.",
         body(),
         [("What is the difference between weather and climate?", "Weather is what the air is like on one day. Climate is the usual weather pattern over many years."),
          ("What are the main kinds of climate?", "Tropical (hot and rainy), desert (very dry), polar (very cold), temperate (four seasons) and mountain (cooler higher up)."),
          ("Are all deserts hot?", "No. A desert is a place with very little rain. Antarctica is a cold desert.")],
         sets)


if __name__ == "__main__":
    main()
