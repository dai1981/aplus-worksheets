# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Water on Earth (5-ESS2-2)
  python tools/gen_us_science_g5_water_on_earth.py
About 97% of Earth's water is salt water in the ocean; only about 3% is fresh water. Of the fresh
water, about 69% is frozen in glaciers and ice caps, about 30% is groundwater, and only about 1%
is in lakes, rivers, swamps and the air. Questions use circle graphs, bar graphs, percentages and
"if all of Earth's water filled a container" models.
Wrong answers come from real mistakes: "most water is fresh", "most fresh water is in lakes and
rivers", "groundwater is a small underground lake", adding percents that do not make 100.
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, pie, bar_chart, table, People, BLUE

U = Unit(50115)
R = U.R
P = People(R)
EARTH = [("ocean (salt water)", 97), ("fresh water", 3)]
FRESH = [("glaciers and ice caps", 69), ("groundwater", 30), ("lakes, rivers and other", 1)]


def pct_pic():
    return pie([("ocean (salt water) 97%", 97, "#2f6fae"), ("fresh water 3%", 3, "#8fd0f0")], "circle graph: 97% of Earth's water is in the ocean, 3% is fresh")


def fresh_pic():
    return pie([("glaciers and ice caps 69%", 69, "#d7eef8"), ("groundwater 30%", 30, "#7aa8d8"), ("lakes, rivers, other 1%", 1, "#1f5fa8")],
               "circle graph of Earth's fresh water")


def fresh_bar():
    return bar_chart(["ice", "ground", "surface"], [69, 30, 1], "percent", "bar graph of where Earth's fresh water is", ymax=80, step=20, col=BLUE, w=230)


# ------------------------------------------------------------ makers
def g_model():
    tot = R.choice([100, 200, 500, 1000, 2000])
    unit = R.choice(["liters", "milliliters", "cups", "drops"])
    ask = R.choice(["ocean", "fresh"])
    v = tot * (97 if ask == "ocean" else 3) // 100
    o = tot - v
    return item("Imagine all of Earth's water is %d %s. About 97%% is ocean water and 3%% is fresh water. About how many %s would be %s?" % (tot, unit, unit, "ocean water" if ask == "ocean" else "fresh water"),
                "%d %s" % (v, unit), ["%d %s" % (o, unit), "%d %s" % (tot // 2, unit), "%d %s" % (tot * (3 if ask == "ocean" else 97) // 10, unit)],
                "%d%% of %d = %d %s." % (97 if ask == "ocean" else 3, tot, v, unit))


def g_fresh_model():
    tot = R.choice([100, 200, 300, 400, 500, 600, 1000, 2000])
    k = R.choice([0, 1])
    name, p = FRESH[k]
    v = tot * p // 100
    return item(fig(fresh_pic()) + "Imagine all of Earth's fresh water is %d liters. About how many liters would be in %s?" % (tot, name),
                "%d liters" % v, ["%d liters" % (tot * FRESH[1 - k][1] // 100), "%d liters" % (tot // 100), "%d liters" % (tot - v + tot // 100)],
                "%d%% of %d = %d liters." % (p, tot, v))


def g_read_pie():
    k = R.randrange(3)
    name, p = FRESH[k]
    return item(fig(fresh_pic()) + "According to the graph, what percent of Earth's fresh water is in %s?" % name, "about %d%%" % p,
                ["about %d%%" % FRESH[(k + 1) % 3][1], "about %d%%" % FRESH[(k + 2) % 3][1], "about 97%"],
                "The graph shows about %d%% in %s." % (p, name))


def g_most():
    ask = R.choice(["most", "least"])
    k = 0 if ask == "most" else 2
    return item(fig(fresh_bar()) + "Where is the %s of Earth's fresh water?" % ask, FRESH[k][0], [FRESH[1][0] if k == 0 else FRESH[0][0], "the ocean", FRESH[1][0] if k == 2 else FRESH[2][0]],
                "The %s bar is for %s (%d%%)." % ("tallest" if ask == "most" else "shortest", FRESH[k][0], FRESH[k][1]))


def g_diff():
    a, b = R.sample(range(3), 2)
    hi, lo = (a, b) if FRESH[a][1] > FRESH[b][1] else (b, a)
    d = FRESH[hi][1] - FRESH[lo][1]
    return item(fig(fresh_bar()) + "How many more percentage points of fresh water are in %s than in %s?" % (FRESH[hi][0], FRESH[lo][0]),
                str(d), [str(FRESH[hi][1] + FRESH[lo][1]), str(FRESH[hi][1]), str(abs(d - 10))], "%d − %d = %d." % (FRESH[hi][1], FRESH[lo][1], d))


def g_bar_model():
    n = R.choice([100, 200, 300, 400, 500, 1000])
    vals = [n * p // 100 for _, p in FRESH]
    ch = bar_chart(["ice", "ground", "surface"], vals, "drops", "bar graph of a class model of fresh water", ymax=(max(vals) // 100 + 1) * 100, step=100 if n >= 300 else 50, col=BLUE, w=240)
    k = R.choice(["ground", "ice", "diff", "total"])
    q = fig(ch) + "A class used %d drops of water to model Earth's fresh water (ice, groundwater and surface water). " % n
    if k == "ground":
        return item(q + "How many drops stand for groundwater?", str(vals[1]), [str(vals[0]), str(vals[2]), str(n)], "30%% of %d = %d drops." % (n, vals[1]))
    if k == "ice":
        return item(q + "How many drops stand for ice?", str(vals[0]), [str(vals[1]), str(n), str(vals[2])], "69%% of %d = %d drops." % (n, vals[0]))
    if k == "diff":
        return item(q + "How many more drops are ice than groundwater?", str(vals[0] - vals[1]), [str(vals[0] + vals[1]), str(vals[0]), str(vals[1])],
                    "%d − %d = %d drops." % (vals[0], vals[1], vals[0] - vals[1]))
    return item(q + "How many drops are not frozen (groundwater plus surface water)?", str(vals[1] + vals[2]), [str(vals[0]), str(vals[1]), str(n)],
                "%d + %d = %d drops." % (vals[1], vals[2], vals[1] + vals[2]))


def g_compare():
    r = R.choice([("an ocean", "salt"), ("the Great Salt Lake", "salt"), ("a glacier", "fresh"), ("groundwater in a well", "fresh"), ("a river", "fresh"),
                  ("Lake Michigan", "fresh"), ("an ice cap in Antarctica", "fresh"), ("the Gulf of Mexico", "salt"), ("a rain puddle", "fresh"), ("the Pacific Ocean", "salt"), ("the Mississippi River", "fresh"), ("the Atlantic Ocean", "salt"), ("a pond in a park", "fresh"), ("the Dead Sea", "salt"), ("a snowbank", "fresh"), ("Lake Superior", "fresh")])
    return item("Is the water in %s salt water or fresh water?" % r[0], r[1] + " water", ["salt water" if r[1] == "fresh" else "fresh water", "neither: it is not water", "half salt water, half fresh water"],
                "%s has %s water." % (r[0][0].upper() + r[0][1:], r[1]))


B1 = bank([
    ("Where is most of Earth's water?", "in the ocean", ["in lakes and rivers", "in glaciers", "underground"],
     "About 97% of Earth's water is salt water in the ocean."),
    ("About what percent of Earth's water is fresh water?", "about 3%", ["about 97%", "about 50%", "about 30%"],
     "Only about 3 out of every 100 liters of Earth's water is fresh."),
    ("Where is most of Earth's fresh water?", "frozen in glaciers and ice caps", ["in lakes", "in rivers", "in the air"],
     "About 69% of fresh water is ice, mostly in Antarctica and Greenland."),
    ("What is groundwater?", "water that fills tiny spaces between soil and rock underground", ["a big underground lake of open water", "water in the ocean", "water in clouds"],
     "Groundwater soaks into the ground and fills cracks and spaces. People reach it with wells."),
    ("Why can't people drink ocean water?", "It is too salty.", ["It is frozen.", "It is too deep to reach.", "It has no water in it."],
     "Drinking salt water makes the body lose water. Fresh water is needed."),
    ("Which source of fresh water is easiest for people to use?", "lakes and rivers", ["glaciers in Antarctica", "deep ocean water", "ice caps"],
     "Lakes and rivers are easy to reach, but they hold only about 1% of Earth's fresh water."),
    ("Why is fresh water called a limited resource?", "Only a tiny part of Earth's water is fresh and easy to reach.", ["There is no fresh water left.", "Fresh water is always frozen.", "Fresh water can be made from nothing."],
     "Most water is salty or frozen, so we must use fresh water carefully."),
    ("About what percent of fresh water is groundwater?", "about 30%", ["about 3%", "about 69%", "about 97%"],
     "About 30% of fresh water is underground."),
    ("Which part of Earth's system includes all its water?", "the hydrosphere", ["the geosphere", "the biosphere", "the atmosphere"],
     "The hydrosphere includes oceans, ice, groundwater, lakes, rivers and water vapor."),
])
B5 = bank([
    ("A student made a circle graph of Earth's water with 50% ocean and 50% fresh. What is wrong?", "The ocean should be about 97% and fresh water about 3%.", ["Nothing is wrong.", "The graph should have no ocean.", "Fresh water should be 97%."],
     "Almost all of Earth's water is in the ocean."),
    ("Ava uses 100 drops of water to model Earth's water. How many drops should she set aside for fresh water?", "3 drops", ["97 drops", "50 drops", "30 drops"],
     "3% of 100 is 3."),
    ("Leo's town gets water from a well. Which part of Earth's fresh water does his town use?", "groundwater", ["glaciers", "the ocean", "clouds only"],
     "Wells pump groundwater from underground."),
    ("Why do some dry coastal places build plants that remove salt from ocean water?", "Fresh water is scarce there, but ocean water is plentiful.", ["Ocean water is already fresh.", "Salt water is better to drink.", "They have too much fresh water."],
     "Removing salt (desalination) turns some ocean water into fresh water."),
    ("If glaciers melt into the ocean, what happens to that fresh water?", "It becomes part of the salty ocean.", ["It stays fresh forever.", "It turns into groundwater.", "It disappears."],
     "Melting ice that flows into the ocean mixes with salt water."),
    ("Which graph best shows that most fresh water is ice?", "a circle graph with a large section for glaciers and ice caps", ["a line graph of temperature", "a bar graph of rainfall in one city", "a map of rivers only"],
     "A circle graph shows parts of a whole, like percentages of fresh water."),
])


def body():
    pics = figure(pct_pic(), "All of Earth's water.") + figure(fresh_pic(), "Earth's fresh water.")
    think = ("<p>Most of Earth is covered with water, but almost all of it is <b>salt water in the ocean (about 97%)</b>. "
             "Only about <b>3%</b> is fresh water.</p>"
             "<p>Most fresh water is hard to use: about <b>69% is frozen</b> in glaciers and ice caps and about <b>30% is groundwater</b> under the ground. "
             "Only about <b>1%</b> is in lakes, rivers, swamps and the air.</p>" + pics)
    ex = [("If all of Earth's water were 1,000 liters, about how much would be fresh?", ["3% of 1,000", "1,000 × 3 ÷ 100 = 30"], "about 30 liters"),
          ("Of 30 liters of fresh water, about how much is ice?", ["about 69%, a little more than two-thirds", "about 21 liters"], "about 21 liters")]
    mist = ["Thinking most water is fresh. Only about 3% is.",
            "Thinking most fresh water is in lakes and rivers. Most is frozen.",
            "Thinking groundwater is an underground lake. It fills tiny spaces in soil and rock.",
            "Making a circle graph whose parts do not add up to 100%."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Where is Earth's water?", B1 + [(g_compare, 8), (g_model, 3)]),
        ("Salt water and fresh water", [(g_model, 10), (g_compare, 10)]),
        ("Reading water graphs", [(g_read_pie, 3), (g_most, 2), (g_diff, 3), (g_bar_model, 12)]),
        ("Water models", [(g_fresh_model, 10), (g_model, 5), (g_bar_model, 5)]),
        ("Using the evidence", B5 + [g_fresh_model, g_bar_model, g_compare]),
    ])
    make("grade-5", "water-on-earth", 15, "5-ESS2-2",
         "Describe and graph the amounts and percentages of water and fresh water in various reservoirs to provide evidence about the distribution of water on Earth.",
         "Water on Earth",
         "Grade 5 Water on Earth Worksheets: Salt Water, Fresh Water, Ice and Groundwater Graphs",
         "Water on Earth",
         "Free Grade 5 science worksheets on water on Earth (NGSS 5-ESS2-2): 97% ocean and 3% fresh water, glaciers, groundwater, lakes and rivers, circle graphs and percent models. 100 practice questions with answers.",
         "About 97% of Earth's water is salt water; only 3% is fresh.",
         "Most fresh water is frozen in ice (69%) or underground (30%). Only about 1% is in lakes, rivers and the air.",
         body(),
         [("How much of Earth's water is fresh?", "Only about 3%. About 97% is salt water in the ocean."),
          ("Where is most of Earth's fresh water?", "About 69% is frozen in glaciers and ice caps, about 30% is groundwater, and only about 1% is in lakes, rivers, swamps and the air."),
          ("What is groundwater?", "Water that soaks into the ground and fills the tiny spaces in soil and rock. People reach it with wells."),
          ("Why is fresh water precious?", "Only a tiny part of Earth's water is fresh and easy to reach, so it must be used carefully.")],
         sets)


if __name__ == "__main__":
    main()
