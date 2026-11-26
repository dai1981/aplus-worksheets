# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Ocean and Atmosphere Circulation (MS-ESS2-6)
  python tools/gen_us_science_g6_ocean_and_atmosphere_circulation.py
Unequal heating of Earth (direct sunlight at the equator, slanted at the poles) and Earth's rotation cause
patterns of atmospheric and oceanic circulation (global winds, convection cells, the Coriolis effect, surface
currents like the Gulf Stream and the California Current) that shape regional climates. Mountains (rain
shadow) and large bodies of water also affect climate.
Assessment boundary: no Coriolis mechanism details; qualitative patterns only.
Wrong answers come from real mistakes: "the equator is hotter because it is closer to the sun",
"ocean currents are caused by fish", "warm air sinks".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(60110)
R = U.R
P = People(R)

CURR = [("the Gulf Stream", "warm", "from the Gulf of Mexico up the east coast of North America and toward Western Europe", "makes Western Europe warmer than other places that far north"),
        ("the California Current", "cold", "south along the west coast of the United States", "keeps summers on the California coast cool and foggy"),
        ("the Humboldt Current", "cold", "north along the west coast of South America", "makes the coast of Peru and Chile cool and dry"),
        ("the Kuroshio Current", "warm", "north along the coast of Japan", "brings warmer water and milder weather to southern Japan"),
        ("the Labrador Current", "cold", "south from the Arctic along the coast of Canada", "makes the coast of Newfoundland cold and foggy")]


def g_current():
    name, kind, path, effect = R.choice(CURR)
    who = P.next()[0]
    k = R.choice(["kind", "effect"])
    if k == "kind":
        return item("%s reads that %s flows %s. Is it a warm or a cold current?" % (who, name, path), "a %s current" % kind,
                    ["a %s current" % ("cold" if kind == "warm" else "warm"), "a current with no temperature", "a current of air, not water"],
                    "Currents that flow from near the equator toward the poles are warm; currents from the poles are cold.")
    others = [c[3] for c in CURR if c[0] != name]
    return item("%s studies %s, a %s current. How does it affect climate?" % (who, name, kind), "It " + effect + ".", ["It " + o + "." for o in R.sample(others, 3)],
                "%s %s." % (name[0].upper() + name[1:], effect))


def g_sun():
    who = P.next()[0]
    k = R.choice(["eq", "pole", "model"])
    if k == "eq":
        return item("%s asks why the equator is the warmest part of Earth on average. What is the best explanation?" % who,
                    "Sunlight hits the equator at the most direct angle, so the energy is concentrated in a small area.",
                    ["The equator is closer to the sun.", "There is more ocean at the equator.", "The moon heats the equator more."],
                    "Unequal heating comes from the angle of sunlight, not the distance to the sun.")
    if k == "pole":
        return item("%s asks why the poles are the coldest parts of Earth. What is the best explanation?" % who,
                    "Sunlight hits the poles at a slant, so the energy is spread over a large area.",
                    ["The poles are much farther from the sun.", "The poles never get any sunlight.", "Snow makes cold energy."],
                    "Slanted sunlight spreads the same energy over more area.")
    return item("%s shines a flashlight straight down and then at a slant onto graph paper. The slanted light covers more squares and is dimmer. What does this model?" % who,
                "Sunlight is spread out near the poles, so they get less energy per area.", ["The poles are farther from the sun.", "The equator has more water.", "Flashlights are like the moon."],
                "The angle of sunlight explains unequal heating.")


WIND = [("Warm air at the equator", "rises, because it is less dense"), ("Cold air at the poles", "sinks, because it is more dense"),
        ("Air near the ground", "moves from high pressure toward low pressure"), ("Winds in the Northern Hemisphere", "curve to the right because Earth rotates")]


def g_wind():
    a, b = R.choice(WIND)
    w = [x[1] for x in WIND if x[1] != b] + ["stays perfectly still", "moves in a straight line no matter what"]
    who = P.next()[0]
    return item("%s completes the sentence: “%s ____.”" % (who, a), b, R.sample(w, 3), "%s %s." % (a, b))


def g_city():
    pairs = [("San Francisco (on the coast)", "Sacramento (inland)", "the coast", "The ocean warms and cools slowly, so coastal places have milder temperatures."),
             ("Seattle (west of the Cascade Mountains)", "Yakima (east of the Cascades)", "Seattle", "Moist ocean air rises over the mountains and drops rain on the west side; the east side is in a rain shadow."),
             ("London, England (near the Gulf Stream)", "Calgary, Canada (inland, about as far north)", "London", "The warm Gulf Stream keeps London's winters mild.")]
    a, b, ans, why = R.choice(pairs)
    who = P.next()[0]
    if "Seattle" in a:
        return item("%s compares %s and %s. Which gets more rain?" % (who, a, b), "Seattle", ["Yakima", "They get the same rain.", "Neither gets rain."], why)
    if "London" in a:
        return item("%s compares %s and %s. Which has milder winters?" % (who, a, b), "London", ["Calgary", "They are the same.", "Neither has winter."], why)
    return item("%s compares %s and %s. Which has a smaller difference between summer and winter temperatures?" % (who, a, b), "San Francisco", ["Sacramento", "They are the same.", "Neither changes."], why)


def g_table():
    cities = R.sample([("Lima, Peru", 12, 19, 15), ("Quito, Ecuador", 0, 14, 14), ("Singapore", 1, 27, 2300), ("Anchorage, Alaska", 61, 3, 410),
                       ("Miami, Florida", 26, 25, 1500), ("Oslo, Norway", 60, 6, 760), ("Cairo, Egypt", 30, 22, 25)], 3)
    rows = [[c[0], "%d°" % c[1], "%d °C" % c[2], "{:,} mm".format(c[3])] for c in cities]
    tab = table(["City", "Latitude", "Average temperature", "Yearly rain"], rows)
    who = P.next()[0]
    k = R.choice(["cold", "dry"])
    if k == "cold":
        a = min(cities, key=lambda c: c[2])
        return item(tab + "%s's table shows three cities. Which has the coldest average temperature?" % who, a[0], [c[0] for c in cities if c != a] + ["They are all the same."],
                    "%s: %d °C." % (a[0], a[2]))
    a = min(cities, key=lambda c: c[3])
    return item(tab + "%s's table shows three cities. Which is the driest?" % who, a[0], [c[0] for c in cities if c != a] + ["They all get the same rain."], "%s gets only %d mm a year." % (a[0], a[3]))


B1 = bank([
    ("Why does the equator get more energy from the sun than the poles?", "Sunlight hits the equator more directly, so the energy is concentrated.", ["The equator is closer to the sun.", "The equator has more water.", "The poles are covered by clouds all the time."],
     "The angle of sunlight causes unequal heating."),
    ("What does unequal heating of Earth cause?", "air and water to move, creating winds and ocean currents", ["the moon's phases", "earthquakes", "the seasons to stop"],
     "Heat differences drive circulation."),
    ("Does warm air rise or sink?", "rise, because it is less dense", ["sink, because it is heavier", "stay still", "move only sideways"], "Rising and sinking air form convection cells."),
    ("What makes global winds curve instead of blowing straight north or south?", "Earth's rotation (the Coriolis effect)", ["the moon", "mountains only", "ocean animals"],
     "In the Northern Hemisphere, winds curve to the right."),
    ("What mainly drives surface ocean currents?", "global winds blowing over the water", ["fish swimming", "the moon only", "ships"], "Winds push the surface water."),
    ("How do warm ocean currents affect nearby land?", "They make the climate warmer and often wetter.", ["They make it colder.", "They have no effect.", "They stop rain."], "The ocean shares its heat with the air."),
    ("What is a rain shadow?", "a dry area on the side of a mountain away from the ocean wind", ["a shady forest", "a cloud's shadow", "a rainy valley"],
     "Air drops its rain on the windward side."),
    ("Why do coastal areas have milder temperatures than inland areas?", "Water heats up and cools down more slowly than land.", ["The ocean makes its own heat.", "Coasts get less sunlight.", "Sand reflects all heat."],
     "Large bodies of water moderate climate."),
])
B5 = bank([
    ("Ava heats one side of a tank of water and cools the other. Food coloring moves in a loop. What does this model?", "convection currents in the ocean and atmosphere", ["earthquakes", "the moon's orbit", "photosynthesis"],
     "Warm fluid rises, cool fluid sinks, and a loop forms."),
    ("Leo notices that Western Europe is warmer in winter than eastern Canada at the same latitude. Which evidence explains this?", "The warm Gulf Stream flows toward Western Europe.", ["Europe is closer to the sun.", "Canada has more people.", "Europe has more mountains."],
     "Ocean currents carry heat."),
    ("Mia places a thermometer in sunlight at a steep angle and one at a direct angle. Which warms faster?", "the one in direct light", ["the one at a steep angle", "They warm the same.", "Neither warms."],
     "Direct light delivers more energy per area."),
    ("Why do trade winds near the equator blow from the east?", "Air moving toward the equator is turned by Earth's rotation.", ["The sun rises in the east and pulls air.", "Ocean waves push the air.", "Mountains block the west."],
     "Rotation curves the winds."),
    ("A city lies on the dry east side of a tall mountain range. What best explains its climate?", "It is in a rain shadow.", ["It is near a warm current.", "It is at the equator.", "It gets direct sunlight all year."],
     "Mountains block moist air."),
])


def body():
    think = ("<p>Earth is heated <b>unequally</b>: sunlight hits the equator directly and the poles at a slant, so the equator gets more energy per area.</p>"
             "<p>Unequal heating makes air and water move. Warm air <b>rises</b> and cool air <b>sinks</b>, forming <b>convection cells</b> and global winds. "
             "Earth's <b>rotation</b> makes winds and currents curve. Winds push the ocean surface into <b>currents</b>: warm currents (like the Gulf Stream) carry heat toward the poles, "
             "and cold currents (like the California Current) cool coasts.</p>"
             "<p>Together with mountains and oceans, these patterns create <b>regional climates</b>.</p>")
    ex = [("Why is it warmer at the equator?", ["Sunlight hits it directly."], "It gets more concentrated energy from the sun."),
          ("How does the Gulf Stream affect England?", ["It is a warm current."], "It keeps winters milder.")]
    mist = ["Thinking the equator is hotter because it is closer to the sun.",
            "Thinking warm air sinks.",
            "Forgetting that oceans carry heat and affect the climate on land."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Unequal heating", B1 + [(g_sun, 6), (g_wind, 6)]),
        ("Winds and convection", [(g_wind, 12), (g_sun, 8)]),
        ("Ocean currents", [(g_current, 14), (g_city, 6)]),
        ("Regional climates", [(g_city, 8), (g_table, 12)]),
        ("Modeling circulation", B5 + [g_current, g_table, g_city, g_wind]),
    ])
    make("grade-6", "ocean-and-atmosphere-circulation", 10, "MS-ESS2-6",
         "Develop and use a model to describe how unequal heating and rotation of the Earth cause patterns of atmospheric and oceanic circulation that determine regional climates.",
         "Ocean and Atmosphere Circulation",
         "Grade 6 Climate Worksheets: Unequal Heating, Global Winds and Ocean Currents",
         "Ocean and Atmosphere Circulation",
         "Free middle school science worksheets on ocean and atmosphere circulation (NGSS MS-ESS2-6): unequal heating, convection and global winds, ocean currents like the Gulf Stream, and regional climates. 100 practice questions with answers.",
         "Unequal heating and Earth's spin move air and water.",
         "These moving winds and ocean currents carry heat around Earth and shape the climate of each region.",
         body(),
         [("Why is Earth heated unequally?", "Sunlight hits the equator directly and the poles at a slant, so the equator gets more energy per area."),
          ("What causes ocean currents?", "Mostly winds blowing over the ocean, along with differences in temperature and Earth's rotation."),
          ("How do ocean currents affect climate?", "Warm currents carry heat toward the poles and warm nearby land; cold currents cool nearby coasts.")],
         sets)


if __name__ == "__main__":
    main()
