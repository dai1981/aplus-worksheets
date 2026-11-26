# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Gravity and Space
  python tools/gen_uk_science_y9_gravity_and_space.py
Gravity force, weight = mass × gravitational field strength (g), the different strengths of gravity on the Earth, the
Moon and other planets, mass and weight, gravity keeping planets and moons in orbit, our Sun as a star, other stars in
our galaxy and other galaxies, the light year as a unit of astronomical distance, and the seasons and the Earth's tilt.
Reuses the gravity and solar-system questions of the US Grade 8 units in British English.
Wrong answers come from real mistakes: "mass and weight are the same", "there is no gravity in space",
"summer happens because the Earth is closer to the Sun", "a light year is a unit of time".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61912)
R = U.R
P = People(R)
uk_sci.USED.clear()
GM = adopt_us("gen_us_science_g8_gravity_and_mass", U)
GS = adopt_us("gen_us_science_g8_gravity_in_the_solar_system", U)
us_cmp, us_claim, us_tab = ukm(GM.g_compare), ukm(GM.g_claim), ukm(GM.g_table)
us_pl, us_scale, us_scn = ukm(GS.g_pl), ukm(GS.g_scale), ukm(GS.g_scn)

G = [("the Earth", 10), ("the Moon", 1.6), ("Mars", 3.7), ("Jupiter", 25), ("Venus", 8.9), ("Neptune", 11)]


def gs(x):
    x = round(x, 1)
    return "{:,}".format(int(x)) if x == int(x) else "{:,}".format(x)


def g_weight():
    who = P.next()[0]
    place, g = R.choice(G)
    m = R.choice([2, 5, 10, 20, 40, 45, 50, 60, 70, 80])
    k = R.choice(["w", "w", "m"])
    if not once(("we", place, m, k)):
        return None
    w = round(m * g, 1)
    wt = "{:,}".format(int(w)) if w == int(w) else "{:,}".format(w)
    if k == "w":
        g_ = "%s N" % wt
        return item("Gravitational field strength on %s is %s N/kg. What is the weight there of an object with a mass of %d kg?" % (place, gs(g), m), g_,
                    uniq(g_, ["%d N" % m, "%s kg" % wt, "%s N" % gs(round(m / g, 1)), "%s N" % gs(m + g)]), "weight = mass × g = %d × %s = %s N." % (m, gs(g), wt))
    g_ = "%d kg" % m
    return item("On %s (g = %s N/kg), %s's backpack weighs %s N. What is its mass?" % (place, gs(g), who, wt), g_,
                uniq(g_, ["%s kg" % wt, "%s kg" % gs(round(w * g, 1)), "%d N" % m, "%d kg" % (m * 2)]), "mass = weight ÷ g = %s ÷ %s = %d kg." % (wt, gs(g), m))


MW = [("Which quantity stays the same on the Moon as on the Earth: mass or weight?", "mass", ["weight", "both change", "neither stays the same"]),
      ("What unit is weight measured in?", "newtons (N)", ["kilograms (kg)", "metres (m)", "joules (J)"]),
      ("What unit is mass measured in?", "kilograms (kg)", ["newtons (N)", "newtons per kilogram", "watts (W)"]),
      ("What is weight?", "the force of gravity on an object", ["the amount of matter in an object", "the size of an object", "the speed of an object"]),
      ("What is mass?", "the amount of matter in an object", ["the force of gravity on it", "its height", "its volume only"]),
      ("Why do astronauts weigh less on the Moon?", "The Moon's gravity is weaker because it has less mass than the Earth.", ["They have less mass there.", "There is no gravity on the Moon.", "Their suits are lighter."]),
      ("Is there gravity in space?", "Yes. Gravity acts everywhere, getting weaker with distance.", ["No, there is none at all.", "Only near the Sun.", "Only inside spacecraft."]),
      ("What keeps the Moon in orbit around the Earth?", "the gravitational pull of the Earth", ["the Moon's magnetism", "air pressure", "the Sun's light"])]


def g_mw():
    q, a, w = R.choice(MW)
    if not once(("mw", q)):
        return None
    return item(q, a, w, "Mass (kg) stays the same; weight (N) depends on gravity.")


SEASON = [("What causes the seasons on Earth?", "the tilt of the Earth's axis as it orbits the Sun", ["the Earth's changing distance from the Sun", "the Moon's orbit", "clouds blocking the Sun"]),
          ("Why are days longer in summer in the UK?", "The northern hemisphere is tilted towards the Sun.", ["The Earth spins slower in summer.", "The Sun is bigger in summer.", "The Earth is closer to the Sun."]),
          ("Why is it warmer in summer?", "The Sun is higher in the sky, so its energy is more concentrated and days are longer.", ["The Earth is much closer to the Sun.", "The Sun gives out more energy.", "There is less air."]),
          ("When it is summer in the UK, what season is it in Australia?", "winter", ["summer", "spring", "autumn"]),
          ("How long does the Earth take to orbit the Sun?", "about 365¼ days (one year)", ["one day", "one month", "ten years"]),
          ("How long does the Earth take to spin once on its axis?", "about 24 hours (one day)", ["one year", "one week", "one hour"])]


def g_season():
    q, a, w = R.choice(SEASON)
    if not once(("se", q)):
        return None
    return item(q, a, w, "The Earth's axis is tilted at about 23.5°.")


DIST = [("Proxima Centauri (the nearest star after the Sun)", 4.2), ("Sirius", 8.6), ("Vega", 25), ("the centre of the Milky Way", 26000), ("the Andromeda Galaxy", 2500000)]


def g_ly():
    k = R.choice(["what", "order", "time"])
    if k == "what":
        return item("What is a light year?", "the distance light travels in one year", ["the time light takes to travel one metre", "a year on another planet", "the age of a star"], "A unit of distance, about 9.5 million million km.") if once(("lyw",)) else None
    if k == "order":
        a, b = R.sample(DIST, 2)
        if not once(("lyo", a[0], b[0])):
            return None
        far = a if a[1] > b[1] else b
        tab = table(["Object", "Distance (light years)"], [[x[0], "{:,}".format(x[1]) if x[1] == int(x[1]) else str(x[1])] for x in (a, b)])
        return item(tab + "Which is further from the Earth?", far[0], [x for x in (a[0], b[0]) if x != far[0]] + ["They are the same distance.", "the Moon"], "Bigger number of light years: further away.")
    o, d = R.choice(DIST[:3])
    if not once(("lyt", o)):
        return None
    ds = str(d)
    return item("%s is %s light years away. How long does its light take to reach us?" % (o[0].upper() + o[1:], ds), "%s years" % ds, ["%s days" % ds, "%s seconds" % ds, "it arrives instantly"], "One light year is the distance light travels in a year.")


B1 = bank([
    ("What is the gravitational field strength on the Earth?", "about 10 N/kg", ["about 1 N/kg", "about 100 N/kg", "0 N/kg"], "More precisely 9.8 N/kg."),
    ("What does the size of gravitational attraction between two objects depend on?", "their masses and the distance between them", ["their colour", "only their speed", "their temperature"], "More mass, closer: stronger."),
    ("What is the Sun?", "a star", ["a planet", "a moon", "a galaxy"], "Our nearest star."),
    ("What is a galaxy?", "a huge group of billions of stars held together by gravity", ["a single star", "a planet with rings", "a group of moons"], "We live in the Milky Way."),
])
B5 = bank([
    ("Why does the Sun's gravity keep the planets in orbit?", "The Sun has by far the most mass in the solar system.", ["The Sun is hot.", "The planets are magnetic.", "The planets push each other."], "Gravitational attraction."),
    ("Why do objects fall at the same rate on the Moon (where there is no air)?", "Without air resistance, gravity accelerates all objects equally.", ["Heavier objects fall slower.", "There is no gravity.", "Lighter objects float up."], "The hammer and feather test."),
    ("Why does a satellite need to keep moving fast to stay in orbit?", "Its speed sideways balances its fall towards the Earth.", ["It is held up by air.", "Gravity stops in orbit.", "It is magnetic."], "Falling around the Earth."),
    ("Why would you weigh more on Jupiter than on the Earth?", "Jupiter has a much greater mass, so its gravity is stronger.", ["Jupiter is colder.", "Your mass doubles.", "Jupiter spins slower."], "Higher g."),
])


def body():
    think = ("<p><b>Gravity pulls masses together; weight is the force of gravity on a mass.</b></p>"
             "<ul><li>weight (N) = mass (kg) × g (N/kg). On Earth g ≈ 10 N/kg; on the Moon about 1.6 N/kg. Mass stays the same.</li>"
             "<li>Gravity keeps the Moon and planets in orbit. Stars are grouped into galaxies; distances are measured in light years.</li>"
             "<li>Seasons are caused by the tilt of the Earth's axis, not by its distance from the Sun.</li></ul>")
    ex = [("50 kg on Earth (10 N/kg). Weight?", ["50 × 10"], "500 N"),
          ("Same 50 kg on the Moon (1.6 N/kg)?", ["50 × 1.6"], "80 N")]
    mist = ["Mixing up mass and weight.", "Thinking there is no gravity in space.", "Thinking summer happens because the Earth is closer to the Sun."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Mass and weight", B1[:2] + [(g_mw, 7), (g_weight, 11)]),
        ("Weight on other worlds", [(g_weight, 14), (us_cmp, 6)]),
        ("Gravity and orbits", [(us_claim, 5), (us_scn, 6), (us_scale, 5), (us_tab, 4)]),
        ("Stars, galaxies and light years", B1[2:] + [(g_ly, 8), (us_pl, 6), (us_tab, 4)]),
        ("Seasons", B5 + [(g_season, 5), (us_cmp, 6), (g_weight, 5)]),
    ])
    make_ks3(9, "gravity-and-space", 12, "Physics", "Space physics",
             "Gravity force, weight = mass × gravitational field strength (g), on Earth g = 10 N/kg, different on other planets and stars; gravity forces between Earth and Moon, and between Earth and Sun (qualitative only); our Sun as a star, other stars in our galaxy, other galaxies; the seasons and the Earth's tilt, day length at different times of year, in different hemispheres; the light year as a unit of astronomical distance.",
             "Gravity and Space",
             "Year 9 Science: Gravity and Space Worksheets (Weight = Mass × g, Light Years, Seasons)",
             "Gravity and Space",
             "Free Year 9 science worksheets on gravity and space: mass and weight, weight = mass × g, gravity on other planets, orbits, stars and galaxies, light years and the seasons. 100 questions with answers.",
             "weight = mass × g",
             "On Earth g ≈ 10 N/kg; mass stays the same everywhere.",
             body(),
             [("What is the difference between mass and weight?", "Mass is the amount of matter, in kilograms, and is the same everywhere. Weight is the force of gravity on it, in newtons, and depends on where you are."),
              ("How do you calculate weight?", "Multiply the mass by the gravitational field strength: weight = mass × g. On Earth, g is about 10 N/kg."),
              ("What causes the seasons?", "The Earth's axis is tilted. When the northern hemisphere tilts towards the Sun it has summer: longer days and the Sun higher in the sky.")],
             sets)


if __name__ == "__main__":
    main()
