# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 2, AC9S2U01: Earth is a planet in the solar system; patterns in the changing position of
the Sun, Moon, planets and stars in the sky; day and night; the Moon's changing shape; and First Nations sky knowledge.
  python tools/gen_au_science_y2_earth_and_the_sky.py
Reuses the US Grade 1 Sun, Moon and stars and daylight makers with Australian names (northern-hemisphere season questions are
dropped), plus own questions on the planets and the Southern Cross. Short sentences.
Wrong answers come from real mistakes: thinking the Sun moves around the Earth, thinking the Moon makes its own light, and thinking
the Sun is not a star.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 2, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

SM = "gen_us_science_g1_sun_moon_and_stars"
DS = "gen_us_science_g1_daylight_and_seasons"
NO = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",
      "summer", "winter", "spring", "autumn", "fall", "season", "North Star", "Big Dipper", "sunset", "minutes of daylight", "hours of daylight"]
s_pick = src(SM, "g_pick", drop=NO)
s_pred = src(SM, "g_pred", drop=NO)
s_when = src(SM, "g_when", drop=NO)
s_see = src(SM, "g_see", drop=NO)
s_time = src(SM, "g_time", drop=NO)
s_phase = src(SM, "g_phase", drop=NO)
s_b1 = src.B(SM, "B1", drop=NO)
s_b5 = src.B(SM, "B5", drop=NO)
d_obs = limit(src(DS, "g_obs", drop=NO), 6)
d_b1 = src.B(DS, "B1", drop=NO)

PLANETS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


def g_planet():
    k = R.choice(["first", "third", "biggest", "rings", "red", "after", "before"])
    i = R.randrange(1, 7)
    if not once(("pl", k, i if k in ("after", "before") else 0)):
        return None
    if k == "first":
        return tq("Which planet is closest to the Sun?", "Mercury", ["Earth", "Jupiter", "Neptune"], "Mercury is the first planet.")
    if k == "third":
        return tq("Which planet do we live on?", "Earth", ["Mars", "Venus", "the Moon"], "Earth is the third planet from the Sun.")
    if k == "biggest":
        return tq("Which is the biggest planet?", "Jupiter", ["Earth", "Mars", "Mercury"], "Jupiter is a giant planet.")
    if k == "rings":
        return tq("Which planet has big, bright rings?", "Saturn", ["Mars", "Earth", "Mercury"], "Saturn's rings are made of ice and rock.")
    if k == "red":
        return tq("Which planet is called the red planet?", "Mars", ["Venus", "Jupiter", "Neptune"], "Mars has red dust.")
    if k == "after":
        a = PLANETS[i + 1]
        return tq("Which planet comes after %s, going out from the Sun?" % PLANETS[i], a, [p for p in PLANETS if p not in (a, PLANETS[i])][:3], "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.")
    a = PLANETS[i - 1]
    return tq("Which planet comes before %s, going out from the Sun?" % PLANETS[i], a, [p for p in PLANETS if p not in (a, PLANETS[i])][-3:], "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.")


KIND = [("the Sun", "a star"), ("Earth", "a planet"), ("Mars", "a planet"), ("the Moon", "a moon"), ("Jupiter", "a planet"),
        ("Venus", "a planet"), ("Saturn", "a planet"), ("Sirius, the brightest star at night", "a star"), ("Alpha Centauri", "a star"),
        ("Neptune", "a planet"), ("Mercury", "a planet")]


def g_kind():
    o, a = R.choice(KIND)
    if not once(("kd", o)):
        return None
    return tq("What is %s?" % o, a, [x for x in ["a star", "a planet", "a moon", "a cloud"] if x != a], "Stars make light. Planets and moons reflect it.")


POS = [("in the morning", "low in the east"), ("at midday", "high in the sky"), ("in the evening", "low in the west")]


def g_sun():
    t, a = R.choice(POS)
    who = R.choice(["Mia", "Jack", "Ruby", "Kai", "Ella", "Noah"])
    if not once(("sun", t, who)):
        return None
    return tq("%s looks at the Sun %s (never look straight at it). Where is it?" % (who, t), a, [x[1] for x in POS if x[1] != a] + ["under the ground"],
              "The Sun rises in the east and sets in the west.")


POOL1 = pool(R, [
    ("What is Earth?", "a planet that goes around the Sun", ["a star", "a moon", "the centre of the universe"], "Earth is one of eight planets."),
    ("What is the Sun?", "a star", ["a planet", "a moon", "a cloud"], "It is the closest star to Earth."),
    ("Why do we have day and night?", "Earth spins around once each day.", ["The Sun goes behind the Moon.", "The Sun turns off.", "Clouds cover the Sun."], "The side facing the Sun has day."),
    ("Does the Moon make its own light?", "No, it reflects light from the Sun.", ["Yes, it glows by itself.", "Yes, at night only.", "It has lamps."], "Only stars make their own light."),
    ("Why does the Moon seem to change shape?", "We see different amounts of its sunlit side.", ["It breaks into pieces.", "Clouds cut it.", "It shrinks."], "These shapes are called phases."),
    ("About how long does the Moon take to go through all its shapes?", "about a month", ["one day", "one hour", "ten years"], "From full moon to full moon is about 29 days."),
    ("Which group of stars is on the Australian flag?", "the Southern Cross", ["the Big Dipper", "the North Star", "the Sun"], "It is seen in the southern sky."),
    ("What do many First Nations peoples see in the dark patches of the Milky Way?", "the Emu in the Sky", ["a koala", "a car", "a kite"], "Its shape tells people when emus lay eggs."),
    ("Why can't we see stars during the day?", "The Sun is so bright that we cannot see them.", ["Stars go away in the day.", "Stars turn off.", "Stars are behind the Earth."], "Stars are always there."),
    ("Where does the Sun rise?", "in the east", ["in the west", "in the north only", "in the south"], "It sets in the west."),
    ("What goes around the Earth?", "the Moon", ["the Sun", "Mars", "the stars"], "The Moon orbits the Earth."),
    ("Why should you never look straight at the Sun?", "It can hurt your eyes.", ["It is too cold.", "It is too small.", "It will go away."], "Use a pinhole viewer instead."),
])
POOL5 = pool(R, [
    ("Mia puts a stick in the ground and marks its shadow every hour. What will she see?", "the shadow moves and changes length", ["the shadow stays still", "the shadow disappears forever", "the shadow turns red"], "The Sun moves across the sky."),
    ("Jack draws the Moon each night for two weeks. What will he notice?", "its shape changes a little each night", ["it is always the same", "it is square", "it is never there"], "This is the pattern of Moon phases."),
    ("Ruby shines a torch on a ball in a dark room and turns the ball. What does this model?", "day and night on the spinning Earth", ["rain", "the wind", "a rainbow"], "The torch is the Sun."),
    ("Kai sees a bright 'star' that does not twinkle near the Moon. What could it be?", "a planet such as Venus", ["a plane on the ground", "the Sun", "a cloud"], "Planets shine with reflected light."),
    ("Ella's shadow is shortest at lunch time. Why?", "The Sun is highest in the sky.", ["The Sun is lowest.", "It is night.", "She is standing still."], "High Sun, short shadow."),
    ("Noah makes a model of the solar system. What should go in the middle?", "the Sun", ["the Earth", "the Moon", "Jupiter"], "All the planets go around the Sun."),
])


def main():
    sets = U.sets([
        ("Earth and the solar system", [(g_planet, 7), (POOL1, 5), (s_pick, 3), (s_b1, 2), (g_kind, 3)]),
        ("Day and night", [(POOL1, 4), (g_sun, 5), (d_obs, 5), (s_time, 3), (d_b1, 3)]),
        ("The Sun's path", [(g_sun, 7), (s_pred, 5), (d_obs, 1), (POOL1, 3), (POOL5, 4)]),
        ("The Moon and stars", [(s_phase, 4), (s_see, 4), (s_when, 5), (POOL1, 4), (g_planet, 3)]),
        ("Sky patterns", [(POOL5, 2), (s_b5, 4), (s_pred, 2), (s_when, 2), (g_planet, 2), (g_sun, 2), (g_kind, 6)]),
    ])
    pic = K.row(["sun", "moon", "star", "rock"], words=["the Sun", "the Moon", "a star", "a planet"], size=80, label="the Sun, the Moon, a star and a planet")
    make_au(YEAR, "earth-and-the-sky", SORT, "AC9S2U01", "Earth and space sciences",
            "Recognise Earth is a planet in the solar system and identify patterns in the changing position of the Sun, Moon, planets "
            "and stars in the sky (summary of the Australian Curriculum v9.0 Science content description).",
            "Earth and the Sky", "Earth and the sky",
            "Free Year 2 science worksheets on Earth and the sky: Earth as a planet, day and night, the Sun's path, the Moon's changing "
            "shape, planets and stars, and the Southern Cross. 100 questions with answers.",
            "Earth is a planet.", "Earth spins to make day and night. The Moon changes shape over about a month.",
            ("Earth is a planet that goes around the Sun.", ["The Sun is a star.", "Earth spins once a day: day and night.",
                                                             "The Moon goes around the Earth."]),
            [("Why is it night?", ["our side of Earth faces away from the Sun"], "Earth spins")],
            ["Thinking the Sun moves around the Earth.", "Thinking the Moon makes its own light."],
            [("Why does the Sun seem to move across the sky?", "The Sun stays still. Earth spins, so the Sun seems to rise in the east and set in the west."),
             ("Why does the Moon change shape?", "The Moon is lit by the Sun. As it goes around the Earth, we see different amounts of the lit side."),
             ("What is the Southern Cross?", "It is a group of bright stars seen from Australia. It is on the Australian flag.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
