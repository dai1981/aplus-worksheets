# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Scale of the Solar System (MS-ESS1-3)
  python tools/gen_us_science_g8_scale_of_the_solar_system.py
Analyze and interpret data to determine scale properties of objects in the solar system: diameters, distances (AU),
scale models, comparing sizes with ratios, layers and features, light travel time.
Wrong answers come from real mistakes: "the planets are evenly spaced", "a scale model can use the same scale for size
and distance on a desk", "Jupiter is about twice Earth's size", "dividing the wrong way".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80120)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# rounded equatorial diameter (km), distance from Sun (AU)
OBJ = [("Mercury", 4900, 0.4), ("Venus", 12100, 0.7), ("Earth", 12800, 1.0), ("Mars", 6800, 1.5), ("Jupiter", 143000, 5.2), ("Saturn", 120500, 9.5),
       ("Uranus", 51100, 19.2), ("Neptune", 49500, 30.1)]
SUN = 1392000
MOON = 3500


def g_ratio():
    who = P.next()[0]
    pairs = [("Jupiter", 143000, "Earth", 12800, 11), ("Earth", 12800, "the Moon", 3500, 4), ("the Sun", 1392000, "Earth", 12800, 109), ("the Sun", 1392000, "Jupiter", 143000, 10),
             ("Saturn", 120500, "Earth", 12800, 9), ("Uranus", 51100, "Earth", 12800, 4), ("Earth", 12800, "Mars", 6800, 2), ("Earth", 12800, "Mercury", 4900, 3)]
    a, da, b, db, r = R.choice(pairs)
    if not once((a, b)):
        return None
    tab = table(["Object", "Diameter (km)"], [[a, comma(da)], [b, comma(db)]])
    return item(tab + "Using %s's data, about how many times wider is %s than %s?" % (who, a, b), "about %d times" % r,
                ["about %d times" % max(2, r // 2) if r // 2 != r else "about %d times" % (r + 3), "about %d times" % (r * 2), "about %s times" % comma(da - db) if da - db < 100000 else "about the same"],
                "%s ÷ %s ≈ %d." % (comma(da), comma(db), r))


def g_model():
    who = P.next()[0]
    sun_cm = R.choice([100, 140, 200, 280])           # Sun's model diameter in cm
    name, d, _ = R.choice(OBJ)
    if not once(("m", sun_cm, name)):
        return None
    cm = d / SUN * sun_cm
    a = "about %.1f cm" % cm if cm < 10 else "about %d cm" % round(cm)
    w = ["about %d cm" % round(cm * 10), "about %.1f cm" % (cm / 10) if cm >= 1 else "about 0.01 cm", "about %d cm" % sun_cm]
    if a in w:
        return None
    return item("%s builds a scale model with the Sun %d cm wide. The Sun is %s km wide and %s is %s km wide. About how wide should %s be?" % (who, sun_cm, comma(SUN), name, comma(d), name), a, w,
                "%s ÷ %s × %d cm ≈ %s." % (comma(d), comma(SUN), sun_cm, a[6:]))


def g_dist():
    who = P.next()[0]
    k = R.choice(["far", "times", "model", "light"])
    if k == "far":
        rows = sorted(R.sample(OBJ, 4), key=lambda r: r[2])
        if not once(("f", tuple(r[0] for r in rows))):
            return None
        tab = table(["Planet", "Distance from the Sun (AU)"], [[n, "%g" % au] for n, _, au in rows])
        a = "%g AU" % round(rows[-1][2] - rows[0][2], 1)
        return item(tab + "In %s's table, how much farther from the Sun is %s than %s?" % (who, rows[-1][0], rows[0][0]), a,
                    ["%g AU" % rows[-1][2], "%g AU" % round(rows[-1][2] + rows[0][2], 1), "%g AU" % round(rows[-1][2] / 2, 1)], "%g − %g = %s." % (rows[-1][2], rows[0][2], a))
    if k == "times":
        x = R.choice([("Jupiter", 5.2, 5), ("Saturn", 9.5, 10), ("Uranus", 19.2, 19), ("Neptune", 30.1, 30), ("Mars", 1.5, 1.5)])
        if not once(("t", x[0])):
            return None
        return item("%s reads that %s is %g AU from the Sun. About how many times farther from the Sun is it than Earth?" % (who, x[0], x[1]), "about %g times" % x[2],
                    ["about %g times" % (x[2] * 2), "about %g times" % round(x[2] / 2, 1), "about %g times" % (x[2] + 10)], "Earth is 1 AU away, so %g ÷ 1 ≈ %g." % (x[1], x[2]))
    if k == "model":
        m = R.choice([10, 20, 50])
        name, _, au = R.choice(OBJ[3:])
        if not once(("mo", m, name)):
            return None
        v = round(au * m)
        return item("In %s's hallway model, 1 AU = %d cm. About how far from the model Sun should %s go (%g AU)?" % (who, m, name, au), "about %s cm" % comma(v),
                    ["about %s cm" % comma(round(v / 10)), "about %s cm" % comma(v * 10), "about %d cm" % m], "%g × %d ≈ %s cm." % (au, m, comma(v)))
    x = R.choice([("the Moon", "about 1.3 seconds"), ("the Sun", "about 8.3 minutes"), ("Jupiter (at its closest)", "about 35 minutes"), ("Neptune", "about 4 hours")])
    if not once(("l", x[0])):
        return None
    return item("Light travels about 300,000 km per second. %s asks how long light from %s takes to reach Earth. Which is closest?" % (who, x[0]), x[1],
                [y[1] for y in [("the Moon", "about 1.3 seconds"), ("the Sun", "about 8.3 minutes"), ("Jupiter (at its closest)", "about 35 minutes"), ("Neptune", "about 4 hours")] if y[1] != x[1]],
                "Farther objects take longer for light to reach us.")


FACTS = [("largest planet", "Jupiter"), ("smallest planet", "Mercury"), ("planet closest to the Sun", "Mercury"), ("planet farthest from the Sun", "Neptune"),
         ("planet with the most famous rings", "Saturn"), ("hottest planet (thick CO₂ atmosphere)", "Venus"), ("largest rocky planet", "Earth"), ("planet tilted on its side", "Uranus")]


def g_fact():
    f, a = R.choice(FACTS)
    who = P.next()[0]
    if not once(("x", f)):
        return None
    return item("%s's data card asks for the %s. Which is it?" % (who, f), a, R.sample([o[0] for o in OBJ if o[0] != a], 3), "Check sizes and distances in the data table.")


B1 = bank([
    ("About how many Earths could line up across the Sun's diameter?", "about 109", ["about 2", "about 10", "about 1,000,000"], "1,392,000 ÷ 12,800 ≈ 109."),
    ("Why is it hard to build a scale model that shows both sizes and distances on a desk?", "The distances are enormous compared with the sizes, so the planets would be tiny dots far apart.", ["The planets are all the same size.", "The distances are tiny.", "Planets have no size."],
     "Space is mostly empty."),
    ("Are the planets evenly spaced from the Sun?", "No. The outer planets are much farther apart than the inner planets.", ["Yes, exactly 1 AU apart.", "Yes, all touching.", "Only the gas giants."], "Spacing increases outward."),
    ("Which planets are the inner, rocky planets?", "Mercury, Venus, Earth and Mars", ["Jupiter, Saturn, Uranus and Neptune", "Earth and Jupiter only", "All eight"], "Small and rocky."),
    ("Which planets are the giant planets?", "Jupiter, Saturn, Uranus and Neptune", ["Mercury, Venus, Earth and Mars", "Only Jupiter", "Mars and Venus"], "Large and mostly gas or ice."),
    ("Where is the asteroid belt?", "between Mars and Jupiter", ["between Earth and Venus", "beyond Neptune only", "inside the Sun"], "Rocky leftovers."),
    ("What is the Kuiper Belt?", "a region of icy bodies beyond Neptune, including Pluto", ["a ring around Saturn", "a belt of asteroids near Mercury", "a cloud around Earth"], "Far, cold objects."),
    ("Why do scientists use AU instead of kilometers for solar system distances?", "The distances are so large that kilometers give huge numbers.", ["Kilometers are not real.", "AU are smaller.", "It is required by law."], "Choose units that fit the scale."),
])
B5 = bank([
    ("Ava's model Sun is a 1 m ball. Earth would be about 9 mm wide. Roughly how far away should Earth be (Earth is about 107 Sun-diameters away)?", "about 107 m", ["about 1 m", "about 10 cm", "about 10 km"],
     "Distances are huge compared with sizes."),
    ("Leo says Jupiter is about twice as wide as Earth. Using diameters of 143,000 km and 12,800 km, what is a better estimate?", "about 11 times as wide", ["about 2 times", "about 100 times", "about the same"], "143,000 ÷ 12,800 ≈ 11."),
    ("Mia graphs planet diameter against distance from the Sun. What does she see?", "The inner planets are small; the outer planets are much larger.", ["Size increases steadily with distance.", "All planets are the same size.", "The farthest planet is the largest."],
     "Two groups of planets."),
    ("A model uses 1 AU = 1 m. Neptune is 30 AU away. How far should it be placed?", "30 m", ["3 m", "300 m", "1 m"], "30 × 1 m."),
    ("Which statement about the solar system's scale is best supported by data?", "Most of the solar system is empty space.", ["The planets nearly touch.", "The Sun is about the size of Jupiter.", "The Moon is larger than Earth."], "Huge gaps."),
])


def body():
    think = ("<p>Objects in the solar system have enormous differences in <b>size</b> and <b>distance</b>. Use data and ratios to compare them.</p>"
             "<ul><li>Divide to compare sizes: Sun 1,392,000 km ÷ Earth 12,800 km ≈ <b>109</b>; Jupiter is about <b>11</b> times wider than Earth.</li>"
             "<li>Distances are measured in <b>astronomical units</b> (1 AU = Earth-Sun distance ≈ 150 million km). Neptune is about 30 AU away.</li>"
             "<li>In a <b>scale model</b>, every size or distance is multiplied by the same factor. Real distances are so large compared with sizes that most of the solar system is empty space.</li></ul>")
    ex = [("Saturn 120,500 km, Earth 12,800 km. How many times wider?", ["120,500 ÷ 12,800 ≈ 9.4"], "about 9 times"),
          ("1 AU = 10 cm. Jupiter at 5.2 AU?", ["5.2 × 10"], "about 52 cm")]
    mist = ["Thinking the planets are evenly spaced.",
            "Subtracting when you should divide to compare sizes.",
            "Using one scale for sizes and another for distances without saying so."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Sizes in the solar system", B1 + [(g_ratio, 6), (g_fact, 6)]),
        ("Comparing sizes", [(g_ratio, 2), (g_model, 16), (g_fact, 2)]),
        ("Distances", [(g_dist, 20)]),
        ("Scale models", [(g_model, 8), (g_dist, 12)]),
        ("Interpreting data", B5 + [(g_dist, 10), (g_model, 5)]),
    ])
    make("grade-8", "scale-of-the-solar-system", 20, "MS-ESS1-3",
         "Analyze and interpret data to determine scale properties of objects in the solar system.",
         "Scale of the Solar System",
         "Grade 8 Scale of the Solar System Worksheets: Planet Sizes, Distances and Scale Models",
         "Scale of the Solar System",
         "Free middle school science worksheets on the scale of the solar system (NGSS MS-ESS1-3): comparing planet and Sun diameters, distances in AU, scale models and light travel time. 100 practice questions with answers.",
         "Divide to compare sizes; use AU for distances.",
         "The Sun is about 109 Earths wide, and the planets are spread out over huge distances. Most of the solar system is empty space.",
         body(),
         [("How big is the Sun compared with Earth?", "The Sun's diameter is about 109 times Earth's diameter."),
          ("What is an astronomical unit?", "The average distance between Earth and the Sun, about 150 million kilometers."),
          ("Why is it hard to make a scale model of the solar system?", "If the planets are big enough to see, the distances between them become huge, often hundreds of meters or more.")],
         sets)


if __name__ == "__main__":
    main()
