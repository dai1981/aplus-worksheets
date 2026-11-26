# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Physics): Space
  python tools/gen_uk_science_y7_space.py
Our Sun as a star, other stars in our galaxy, other galaxies; the light year as a unit of astronomical distance; the
seasons and the Earth's tilt, day length at different times of year and in different hemispheres; gravity between the
Earth and the Moon and the Earth and the Sun (qualitative); the planets. Reuses the planet questions of the Year 5
unit (new seed).
Wrong answers come from real mistakes: "a light year is a unit of time", "summer happens because the Earth is closer to
the Sun", "the Sun is the biggest star", "it is summer everywhere in July".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y5_the_solar_system as S5
from sci_phys import uniq

S5.U = Unit(61713)
S5.R = S5.U.R
S5.P = People(S5.R)
uk_sci.USED.clear()
U, R, P = S5.U, S5.R, S5.P

SIZE = ["the Moon", "the Earth", "the Sun", "the Solar System", "the Milky Way galaxy", "the Universe"]


def g_size():
    i, j = sorted(R.sample(range(len(SIZE)), 2))
    k = R.random() < 0.5
    if not once(("si", i, j, k)):
        return None
    a, b = SIZE[i], SIZE[j]
    o = [a, b] if R.random() < 0.5 else [b, a]
    if k:
        return item("Which is bigger: %s or %s?" % tuple(o), b, [a, "They are the same size.", "You cannot compare them."], "Moon < Earth < Sun < Solar System < galaxy < Universe.")
    return item("Which is smaller: %s or %s?" % tuple(o), a, [b, "They are the same size.", "You cannot compare them."], "Moon < Earth < Sun < Solar System < galaxy < Universe.")


STAR = [("Proxima Centauri", 4.2), ("Sirius", 8.6), ("Vega", 25), ("Arcturus", 37), ("Polaris", 430), ("Betelgeuse", 550), ("Rigel", 860)]


def g_ly():
    s, d = R.choice(STAR)
    k = R.choice(["time", "far", "compare"])
    if not once(("ly", s, k)):
        return None
    ds = "%g" % d
    if k == "time":
        g = "%s years" % ds
        return item("%s is about %s light years away. How long does its light take to reach us?" % (s, ds), g, uniq(g, ["%s days" % ds, "%s minutes" % ds, "%s seconds" % ds, "8 minutes"]),
                    "A light year is the distance light travels in one year, so the light takes %s years." % ds)
    if k == "far":
        return item("What does it mean that %s is %s light years away?" % (s, ds), "Light from it takes %s years to reach Earth." % ds,
                    ["It takes %s years to fly there by plane." % ds, "It is %s km away." % ds, "It was born %s years ago." % ds], "A light year is a distance, not a time.")
    t, u = R.sample(STAR, 2)
    if t[1] == u[1]:
        return None
    a = t[0] if t[1] < u[1] else u[0]
    return item("Which star is closer to Earth: %s (%g light years) or %s (%g light years)?" % (t[0], t[1], u[0], u[1]), a, [t[0] if a == u[0] else u[0], "They are the same distance.", "You cannot tell."],
                "Fewer light years means closer.")


SEAS = [("June", "summer", "winter"), ("July", "summer", "winter"), ("December", "winter", "summer"), ("January", "winter", "summer"), ("April", "spring", "autumn"), ("October", "autumn", "spring")]


def g_hemi():
    m, n, s = R.choice(SEAS)
    k = R.random() < 0.5
    if not once(("he", m, k)):
        return None
    if k:
        return item("It is %s in the UK. Which season is it in Australia?" % m, s, [x for x in ["spring", "summer", "autumn", "winter"] if x != s], "The hemispheres have opposite seasons because of the Earth's tilt.")
    return item("Which season is it in the UK in %s?" % m, n, [x for x in ["spring", "summer", "autumn", "winter"] if x != n], "In the UK, summer is June–August and winter is December–February.")


TILT = [("Why do we have seasons?", "The Earth's axis is tilted, so each hemisphere leans towards the Sun for part of the year.", ["The Earth gets closer to the Sun in summer.", "The Sun gets hotter in summer.", "The Moon blocks the Sun in winter."]),
        ("Why are days longer in summer in the UK?", "The northern hemisphere is tilted towards the Sun, so the Sun is up for longer.", ["The Earth spins slower in summer.", "The Sun is bigger in summer.", "Clouds disappear in summer."]),
        ("Why is it warmer in summer?", "The Sun is higher in the sky, so its energy is more concentrated and the days are longer.", ["The Earth is much closer to the Sun.", "The Moon is further away.", "The Sun burns more fuel."]),
        ("When is the Earth closest to the Sun?", "in early January, during the UK winter", ["in July, during the UK summer", "every day the same", "in April only"]),
        ("At about what angle is the Earth's axis tilted?", "about 23.5°", ["0°", "90°", "about 5°"]),
        ("What causes day and night?", "the Earth spinning on its axis once every 24 hours", ["the Earth orbiting the Sun once a year", "the Moon blocking the Sun", "the Sun moving around the Earth"]),
        ("How long does the Earth take to orbit the Sun?", "about 365¼ days (one year)", ["24 hours", "about 28 days", "about 10 years"]),
        ("What keeps the Moon in orbit around the Earth?", "the force of gravity between them", ["magnetism", "air resistance", "nothing; it floats"])]


def g_tilt():
    q, a, w = R.choice(TILT)
    if not once(("ti", q)):
        return None
    return item(q, a, w, "The tilt of the Earth causes the seasons; its spin causes day and night.")


B1 = bank([
    ("What is the Sun?", "a star", ["a planet", "a moon", "a galaxy"], "The closest star to Earth."),
    ("What is a galaxy?", "a huge group of billions of stars", ["a single star", "a planet with rings", "a small moon"], "We live in the Milky Way."),
    ("What is the name of our galaxy?", "the Milky Way", ["Andromeda", "the Solar System", "the Big Dipper"], "A spiral galaxy."),
    ("What is a light year?", "the distance light travels in one year", ["the time it takes light to travel one year", "a year on a light planet", "a very bright year"], "A unit of distance."),
    ("Which force keeps the planets in orbit around the Sun?", "gravity", ["friction", "magnetism", "air resistance"], "The Sun's huge mass pulls them."),
    ("Is the Sun the biggest star in the Universe?", "No. Many stars are much bigger than the Sun.", ["Yes, the biggest.", "It is the only star.", "It is not a star."], "The Sun is a medium-sized star."),
    ("Why do stars look tiny?", "They are extremely far away.", ["They are smaller than the Moon.", "They are made of ice.", "They are close to Earth."], "Distance."),
    ("Why does the Moon shine?", "It reflects light from the Sun.", ["It makes its own light.", "It is a star.", "It reflects light from the Earth only."], "The Moon is not a light source."),
])
B5 = bank([
    ("Why would you weigh less on the Moon than on Earth?", "The Moon's gravity is weaker because it has less mass.", ["Your mass is less on the Moon.", "There is no gravity on the Moon.", "The Moon is closer to the Sun."], "Weight depends on gravity."),
    ("When we look at a star 100 light years away, what are we seeing?", "light that left the star 100 years ago", ["the star as it is right now", "light from the Sun", "a reflection from the Moon"], "Looking back in time."),
    ("Why do astronomers use light years and not kilometres?", "The distances are so huge that kilometres give enormous numbers.", ["Light years are smaller.", "Kilometres do not work in space.", "It is a rule from the Moon."], "Convenient units."),
    ("If the Earth's axis were not tilted, what would happen?", "There would be almost no seasons.", ["There would be no day and night.", "Summer would last all year everywhere.", "The Earth would stop spinning."], "Tilt causes seasons."),
    ("Why is it summer in Australia when it is winter in the UK?", "The southern hemisphere is tilted towards the Sun while the northern is tilted away.", ["Australia is closer to the Sun.", "Australia has a different Sun.", "The Moon warms Australia."], "Opposite hemispheres."),
])


def body():
    think = ("<p><b>The Sun is one star in the Milky Way, one of billions of galaxies.</b></p>"
             "<ul><li>A light year is the distance light travels in a year, about 9.5 million million km.</li>"
             "<li>Seasons happen because the Earth's axis is tilted, not because the Earth gets closer to the Sun.</li>"
             "<li>Gravity keeps the Moon orbiting the Earth and the planets orbiting the Sun.</li></ul>")
    ex = [("A star 8.6 light years away. Light takes?", ["A light year is a distance"], "8.6 years"),
          ("July in the UK. Season in Australia?", ["Opposite hemispheres"], "winter")]
    mist = ["Thinking a light year is a unit of time.", "Thinking summer happens because the Earth is closer to the Sun.", "Thinking the Sun is the biggest star."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stars and galaxies", B1 + [(g_size, 12)]),
        ("The Solar System", [(S5.g_order, 6), (S5.g_type, 6), (g_size, 4), (S5.g_dist, 4)]),
        ("Seasons", [(g_tilt, 8), (g_hemi, 12)]),
        ("Light years", [(g_ly, 18), (g_size, 2)]),
        ("Thinking about space", B5 + [(S5.g_dist, 6), (g_size, 4), (S5.g_order, 3), (g_ly, 2)]),
    ])
    make_ks3(7, "space", 13, "Physics", "Space physics",
             "Gravity force, weight = mass × gravitational field strength (g), on Earth g=10 N/kg, different on other planets and stars; gravity forces between Earth and Moon, and between Earth and Sun (qualitative only); our Sun as a star, other stars in our galaxy, other galaxies; the seasons and the Earth's tilt, day length at different times of year, in different hemispheres; the light year as a unit of astronomical distance.",
             "Space",
             "Year 7 Science: Space Worksheets (Stars, Galaxies, Light Years, Seasons)",
             "Space",
             "Free Year 7 science worksheets on space: the Sun as a star, galaxies, the light year, the planets, gravity and why we have seasons in each hemisphere. 100 questions with answers.",
             "The Sun is a star in the Milky Way.",
             "A light year is a distance. The Earth's tilt causes the seasons.",
             body(),
             [("What is a light year?", "The distance light travels in one year, about 9.5 million million km. It is a unit of distance, not time."),
              ("Why do we have seasons?", "The Earth's axis is tilted. When our hemisphere leans towards the Sun, days are longer and the Sun is higher, so it is summer."),
              ("Is the Sun a star?", "Yes. It is a medium-sized star, one of billions in the Milky Way galaxy.")],
             sets)


if __name__ == "__main__":
    main()
