# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U03: the relative positions and movements of the Sun, Earth and Moon cause
phases of the Moon, eclipses, tides and seasons (southern-hemisphere view).
  python tools/gen_au_science_y7_earth_sun_and_moon.py
Reuses the US Grade 8 Earth-Moon-Sun makers (phases in order, eclipses, seasons; northern-hemisphere pictures dropped) and the
UK Year 7 space makers with Australian names, plus own questions on tides and on how the Moon looks from Australia.
Wrong answers come from real mistakes: thinking Earth's shadow causes the phases, thinking seasons come from distance to the Sun,
and thinking there are eclipses every month.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

EM = "gen_us_science_g8_earth_moon_sun_system"
NH = ["Northern Hemisphere", "U.S.", "United States", "sketches the Moon", "photographed"]
em_ecl = src(EM, "g_ecl")
em_next = limit(src(EM, "g_next"), 8)
em_season = limit(src(EM, "g_season", drop=["U.S.", "United States"]), 6)
em_b1 = src.B(EM, "B1")
em_b5 = src.B(EM, "B5", drop=NH)
SP = "gen_uk_science_y7_space"
sp_ly = limit(src(SP, "g_ly"), 3)
sp_size = limit(src(SP, "g_size"), 4)
sp_tilt = src(SP, "g_tilt")
sp_b1 = src.B(SP, "B1")
sp_b5 = src.B(SP, "B5")

PH = ["new moon", "waxing crescent", "first quarter", "waxing gibbous", "full moon", "waning gibbous", "last quarter", "waning crescent"]


def g_ph():
    i = R.randrange(8)
    k = R.choice(["after", "before", "days"])
    if k == "after":
        return tq("Which phase of the Moon comes after the %s?" % PH[i], PH[(i + 1) % 8], R.sample([p for p in PH if p != PH[(i + 1) % 8]], 3),
                  "The order is " + ", ".join(PH) + ".")
    if k == "before":
        return tq("Which phase of the Moon comes just before the %s?" % PH[i], PH[i - 1], R.sample([p for p in PH if p != PH[i - 1]], 3),
                  "The order is " + ", ".join(PH) + ".")
    if PH[i] not in ("new moon", "full moon"):
        return None
    o = "full moon" if PH[i] == "new moon" else "new moon"
    return tq("About how many days after a %s is the next %s?" % (PH[i], o), "about 15 days", ["about 1 day", "about 7 days", "about 365 days"],
              "A full cycle of phases takes about 29.5 days, so opposite phases are about half that apart.")


TIDE = [("How many high tides do most Australian beaches have each day?", "about two", ["one", "none", "about ten"], "High tides happen about every 12 hours 25 minutes."),
        ("What mainly causes ocean tides?", "the pull of the Moon's gravity on Earth's oceans", ["wind", "the Earth's magnetism", "rain"], "The Sun's gravity has a smaller effect."),
        ("When are spring tides (the biggest tides) most likely?", "at new moon and full moon", ["at first quarter only", "only in spring", "only in winter"], "The Sun and Moon pull in a line."),
        ("When are neap tides (the smallest tides) most likely?", "at first and last quarter moon", ["at full moon", "at new moon", "every Sunday"], "The Sun and Moon pull at right angles."),
        ("Which part of Australia has some of the biggest tides, up to about 11 m?", "the Kimberley coast in Western Australia", ["Sydney Harbour", "Lake Eyre", "the Murray River"], "The shape of the coast makes tides bigger there."),
        ("High tide is at 6:00 am. When is the next high tide, roughly?", "about 6:25 pm", ["about 6:00 am the next day", "about 9:00 am", "about 12:00 noon"], "Tides repeat about every 12 hours 25 minutes."),
        ("Why are tides about 50 minutes later each day?", "The Moon moves along its orbit, so Earth must turn a bit further to face it again.", ["Clocks are wrong.", "The ocean slows down.", "The Sun moves faster."], "The Moon's position changes each day."),
        ("A rock pool is only visible at low tide. Why should you check a tide chart before exploring it?", "The rising tide can cut you off or knock you over.", ["Rock pools disappear forever.", "Tide charts show the weather.", "Fish only come at night."], "Tides change the shoreline every few hours.")]
TIDES = pool(R, TIDE)
POOL1 = pool(R, [
    ("Why does the Moon seem to change shape?", "We see different amounts of its sunlit half as it orbits Earth.", ["Earth's shadow covers it.", "Clouds cover parts of it.", "The Moon grows and shrinks."], "Half the Moon is always lit by the Sun."),
    ("How long does the Moon take to orbit Earth?", "about 27 days (and about 29.5 days from one new moon to the next)", ["24 hours", "about 365 days", "about 7 days"], "This is roughly a month."),
    ("What happens in a solar eclipse?", "The Moon passes between the Sun and Earth and blocks the Sun.", ["Earth blocks sunlight from the Moon.", "The Sun goes out.", "The Moon gives off light."], "Solar eclipses happen at new moon."),
    ("What happens in a lunar eclipse?", "Earth passes between the Sun and Moon, and Earth's shadow falls on the Moon.", ["The Moon blocks the Sun.", "The Moon disappears for a week.", "The Sun passes in front of the Moon."], "Lunar eclipses happen at full moon."),
    ("Why don't eclipses happen every month?", "The Moon's orbit is tilted, so the Sun, Earth and Moon rarely line up exactly.", ["The Moon stops moving.", "Eclipses only happen in winter.", "The Sun is too bright."], "Usually the Moon passes above or below the line."),
    ("From Australia, which side of a waxing crescent Moon is lit?", "the left side", ["the right side", "the top only", "the whole Moon"], "In the southern hemisphere the Moon looks upside down compared with the northern hemisphere."),
    ("Why should you never look straight at a solar eclipse?", "The Sun's light can permanently damage your eyes.", ["The Moon is too bright.", "It is too dark.", "It is only a myth."], "Use eclipse glasses or a pinhole viewer."),
    ("When is it summer in Australia?", "December to February", ["June to August", "March to May", "September to November"], "Australia is in the southern hemisphere."),
    ("What causes the seasons?", "Earth's tilted axis as it orbits the Sun", ["Earth's distance from the Sun", "the Moon's phases", "tides"], "The tilt changes how directly sunlight reaches each place."),
    ("First Nations Australians linked the Moon to tides long before modern science. What does this show?", "Careful observation of patterns over time is science.", ["Tides are random.", "The Moon has no effect on tides.", "Only telescopes reveal patterns."], "Many Yolŋu stories describe the Moon and tides."),
])
POOL5 = pool(R, [
    ("Mia models the Moon's phases with a lamp, a ball and her head. What does the lamp represent?", "the Sun", ["Earth", "the Moon", "a star"], "Her head is Earth."),
    ("In Mia's model, when does the ball look fully lit?", "when the ball is on the opposite side of her head from the lamp", ["when the ball is between her and the lamp", "never", "when the lamp is off"], "That is a full moon."),
    ("Jack records high tide times: Monday 7:10 am, Tuesday 8:00 am, Wednesday 8:50 am. Predict Thursday's morning high tide.", "about 9:40 am", ["about 7:10 am", "about 10:30 pm", "about 8:00 am"], "Each day is about 50 minutes later."),
    ("Ruby draws the Moon every night for a month. What pattern will she see?", "The lit part grows to full, then shrinks back to new.", ["The Moon is the same every night.", "It is always full.", "It changes randomly."], "The cycle repeats about every 29.5 days."),
    ("Kai says the phases happen because Earth's shadow falls on the Moon. Which observation shows he is wrong?", "A crescent moon can be seen when the Moon is near the Sun in the sky, where Earth's shadow cannot reach.", ["The Moon is round.", "The Moon is bright.", "Eclipses happen sometimes."], "Phases depend on the viewing angle, not Earth's shadow."),
    ("Ella photographs the Moon at 8 pm each night. On which night will it rise latest?", "the night after the full moon", ["the night of the new moon", "every night at the same time", "the night of first quarter"], "The Moon rises about 50 minutes later each night."),
    ("Noah sees a lunar eclipse from Perth. Who else on Earth could see it at the same time?", "everyone on the night side of Earth", ["only people in Perth", "only people in daylight", "nobody else"], "Earth's shadow is on the Moon itself."),
    ("Why do surf lifesavers record tide times on beach boards?", "Tides change water depth and currents, which affects swimmers' safety.", ["Tides change the air temperature.", "Tides stop waves.", "Tides only matter for boats."], "Knowing the tide keeps beachgoers safe."),
    ("Why do scientists use models of the Sun, Earth and Moon?", "The real distances and sizes are too big to see at once.", ["Models are more accurate than observations.", "Space does not exist.", "Models change the orbits."], "Models help explain patterns."),
])


def main():
    sets = U.sets([
        ("Phases of the Moon", [(g_ph, 8), (em_next, 6), (POOL1, 3), (em_b1, 3)]),
        ("Eclipses", [(em_ecl, 7), (POOL1, 4), (em_b1, 3), (sp_tilt, 3), (g_ph, 3)]),
        ("Tides", [(TIDES, 8), (POOL5, 2), (g_ph, 2), (em_next, 2), (sp_b1, 3), (POOL1, 3)]),
        ("Seasons and the solar system", [(em_season, 6), (sp_size, 4), (sp_ly, 3), (sp_b1, 4), (sp_tilt, 3)]),
        ("Models and investigations", [(POOL5, 7), (em_b5, 3), (sp_b5, 4), (g_ph, 4), (em_b1, 2)]),
    ])
    make_au(YEAR, "earth-sun-and-moon", SORT, "AC9S7U03", "Earth and space sciences",
            "Model the cyclic changes in the relative positions of the Earth, sun and moon and explain how these result in phenomena "
            "including seasons, phases of the moon, eclipses and tides (summary of the Australian Curriculum v9.0 Science content description).",
            "Earth, Sun and Moon", "Earth, Sun and Moon",
            "Free Year 7 science worksheets on the Earth, Sun and Moon: phases of the Moon, solar and lunar eclipses, tides and seasons, "
            "seen from Australia. 100 questions with answers.",
            "Positions in space cause phases, eclipses and tides.", "The Moon's orbit causes phases and tides; Earth's tilt causes seasons.",
            "<p><b>The movements of the Sun, Earth and Moon cause regular patterns.</b></p><ul>"
            "<li>Phases: half the Moon is always lit; as it orbits Earth we see different amounts of the lit half (about 29.5 days for a full cycle).</li>"
            "<li>Eclipses: a solar eclipse happens when the Moon blocks the Sun (new moon); a lunar eclipse when Earth's shadow falls on the Moon (full moon).</li>"
            "<li>Tides: the Moon's gravity pulls the oceans, giving about two high tides a day. Seasons come from Earth's tilted axis.</li></ul>",
            [("What comes after first quarter?", ["the lit part keeps growing"], "waxing gibbous"),
             ("High tide 6:00 am. Next high tide?", ["about 12 h 25 min later"], "about 6:25 pm")],
            ["Thinking Earth's shadow causes the phases.", "Thinking seasons come from Earth's distance from the Sun.",
             "Thinking there is an eclipse every month."],
            [("What causes the phases of the Moon?", "The Moon is always half lit by the Sun. As it orbits Earth, we see different amounts of the lit half, from new moon to full moon and back."),
             ("What causes tides?", "Mainly the Moon's gravity pulling on Earth's oceans. The Sun's gravity also helps, giving bigger spring tides at new and full moon."),
             ("Why does the Moon look different from Australia?", "People in the southern hemisphere see the Moon upside down compared with people in the northern hemisphere, so a waxing crescent is lit on the left.")],
            sets)


if __name__ == "__main__":
    main()
