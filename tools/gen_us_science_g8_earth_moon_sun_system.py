# -*- coding: utf-8 -*-
"""
US Grade 8 Science: The Earth-Moon-Sun System (MS-ESS1-1)
  python tools/gen_us_science_g8_earth_moon_sun_system.py
Develop and use a model of the Earth-sun-moon system to describe the cyclic patterns of lunar phases, eclipses of
the sun and moon, and seasons. Phases (as seen from the Northern Hemisphere), the 29.5-day cycle, solar and lunar
eclipses, and seasons from the 23.5° tilt of Earth's axis.
Wrong answers come from real mistakes: "phases are caused by Earth's shadow", "seasons happen because Earth is closer to
the Sun in summer", "there is an eclipse every month", "the far side of the Moon is always dark".
"""
import math
from sci_common import Unit, item, bank, lesson, make, fig, svg_wrap, circle, text, People, INK, GRAY

U = Unit(80118)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


PH = ["new moon", "waxing crescent", "first quarter", "waxing gibbous", "full moon", "waning gibbous", "third quarter", "waning crescent"]
DARK, LIT = "#3b3f4a", "#f4e7a1"


def moon(i, cx=0, cy=0, r=40):
    """Phase i (0-7) as seen from the Northern Hemisphere. Waxing = lit on the right."""
    th = i * 45
    s = circle(cx, cy, r, DARK, INK, 1.5)
    if th in (0,):
        return s
    if th == 180:
        return circle(cx, cy, r, LIT, INK, 1.5)
    waxing = th < 180
    t = th if waxing else 360 - th          # 0..180 from new to full
    rx = abs(math.cos(math.radians(t))) * r
    side = 1 if waxing else 0              # sweep for the outer lit semicircle
    # outer edge: semicircle on the lit side; terminator: ellipse arc back to the top
    bulge_lit = t < 90                     # crescent: terminator bulges toward the lit side
    sweep2 = (1 - side) if bulge_lit else side
    d = "M%g %g A%g %g 0 0 %d %g %g A%g %g 0 0 %d %g %g Z" % (cx, cy - r, r, r, side, cx, cy + r, max(rx, 0.01), r, sweep2, cx, cy - r)
    return s + "<path d='%s' fill='%s' stroke='none'/>" % (d, LIT) + circle(cx, cy, r, "none", INK, 1.5)


def moon_svg(i, label=None):
    return svg_wrap(110, 100, moon(i, 55, 50, 40), label or "the Moon in the %s phase" % PH[i])


def row_svg(idx):
    s = ""
    for k, i in enumerate(idx):
        s += moon(i, 55 + 100 * k, 50, 36) + text(55 + 100 * k, 108, "ABCD"[k], 15)
    return svg_wrap(100 * len(idx) + 10, 118, s, "four Moon phases labeled A to D")


def g_name():
    i = R.randrange(8)
    who = P.next()[0]
    if not once(("n", i), 2):
        return None
    w = [PH[(i + d) % 8] for d in (1, -1, 4)]
    if i in (0, 4):
        w = [PH[(i + d) % 8] for d in (1, -1, 2)]
    return item(fig(moon_svg(i, "a Moon phase")) + "%s sketches the Moon from the Northern Hemisphere. Which phase is shown?" % who, PH[i], w,
                "Waxing phases are lit on the right; waning phases are lit on the left." if i not in (0, 4) else "New: no lit side visible. Full: the whole face is lit.")


def g_next():
    i = R.randrange(8)
    who = P.next()[0]
    k = R.choice(["next", "before", "week", "fortnight"])
    if not once((i, k)):
        return None
    if k == "next":
        a, q = PH[(i + 1) % 8], "Which phase comes next?"
    elif k == "before":
        a, q = PH[(i - 1) % 8], "Which phase came just before it?"
    elif k == "week":
        a, q = PH[(i + 2) % 8], "About which phase will %s see one week later?" % who
    else:
        a, q = PH[(i + 4) % 8], "About which phase will %s see about two weeks later?" % who
    w = [p for p in PH if p != a]
    R.shuffle(w)
    near = [PH[(PH.index(a) + d) % 8] for d in (1, -1)]
    w = near + [x for x in w if x not in near][:1]
    return item("Tonight %s sees a %s. %s" % (who, PH[i], q), a, w, "The cycle is new → waxing crescent → first quarter → waxing gibbous → full → waning gibbous → third quarter → waning crescent, about 29.5 days.")


def g_order():
    who = P.next()[0]
    st = R.randrange(8)
    step = R.choice([1, 2])
    seq = [(st + step * k) % 8 for k in range(4)]
    if not once(("o", st, step)):
        return None
    shuf = seq[:]
    R.shuffle(shuf)
    if shuf == seq:
        return None
    letters = {i: "ABCD"[k] for k, i in enumerate(shuf)}
    a = ", ".join(letters[i] for i in seq)
    w = set()
    for _ in range(30):
        x = seq[:]
        R.shuffle(x)
        if x != seq:
            w.add(", ".join(letters[i] for i in x))
    w.discard(a)
    if len(w) < 3:
        return None
    return item(fig(row_svg(shuf)) + "%s photographed these phases %s apart, starting with %s. In what order were they seen?" % (who, "about 3.7 days" if step == 1 else "about one week", PH[seq[0]]), a,
                R.sample(sorted(w), 3), "Follow the cycle: " + " → ".join(PH[i] for i in seq) + ".")


ECL = [("The Moon passes directly between the Sun and Earth, and its shadow falls on Earth.", "a solar eclipse", "new moon"),
       ("Earth passes directly between the Sun and the Moon, and Earth's shadow falls on the Moon.", "a lunar eclipse", "full moon"),
       ("People in a narrow path on Earth see the Sun's disk completely covered for a few minutes.", "a total solar eclipse", "new moon"),
       ("The Moon turns a reddish color for over an hour, and everyone on the night side of Earth can see it.", "a total lunar eclipse", "full moon")]


def g_ecl():
    s, a, ph = R.choice(ECL)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((s, t)):
        return None
    if t:
        return item("%s reads: “%s” What is this?" % (who, s), a, [x[1] for x in ECL if x[1] != a][:2] + ["a new season"], "Solar: Moon blocks the Sun. Lunar: Earth's shadow on the Moon.")
    return item("%s reads: “%s” During which Moon phase can this happen?" % (who, s), ph, [x for x in ["new moon", "full moon", "first quarter", "third quarter"] if x != ph],
                "Solar eclipses happen only at new moon; lunar eclipses only at full moon.")


SEAS = [("June", "Northern", "summer"), ("June", "Southern", "winter"), ("December", "Northern", "winter"), ("December", "Southern", "summer"),
        ("March", "Northern", "spring"), ("September", "Northern", "fall"), ("March", "Southern", "fall"), ("September", "Southern", "spring")]


def g_season():
    m, h, a = R.choice(SEAS)
    who = P.next()[0]
    k = R.choice(["what", "why", "day", "angle"])
    if not once((m, h, k)):
        return None
    if k == "angle":
        if a not in ("summer", "winter"):
            return None
        return item("It is %s. How high is the noon Sun in the sky where %s lives in the %s Hemisphere, compared with the rest of the year?" % (m, who, h),
                    "higher than at any other time of year" if a == "summer" else "lower than at any other time of year",
                    ["lower than at any other time of year" if a == "summer" else "higher than at any other time of year", "exactly overhead every day of the year", "below the horizon all day"],
                    "The tilt toward the Sun makes the noon Sun higher in summer and lower in winter.")
    if k == "day":
        if a not in ("summer", "winter"):
            return None
        return item("It is %s. Compared with March, how long are the days where %s lives in the %s Hemisphere?" % (m, who, h), "longer" if a == "summer" else "shorter",
                    ["shorter" if a == "summer" else "longer", "exactly the same", "always 24 hours"], "The hemisphere tilted toward the Sun has longer days.")
    if k == "what":
        return item("It is %s. %s lives in the %s Hemisphere. Which season is it there?" % (m, who, h), a, [x for x in ["summer", "winter", "spring", "fall"] if x != a],
                    "The hemisphere tilted toward the Sun has summer; the seasons are opposite in the two hemispheres.")
    if a not in ("summer", "winter"):
        return None
    toward = a == "summer"
    return item("In %s, it is %s in the %s Hemisphere, where %s lives. What is the main reason?" % (m, a, h, who),
                "That hemisphere is tilted %s the Sun, so sunlight hits it %s and days are %s." % ("toward" if toward else "away from", "more directly" if toward else "at a lower angle", "longer" if toward else "shorter"),
                ["Earth is %s the Sun at that time." % ("closest to" if toward else "farthest from"), "The Moon blocks %s sunlight." % ("less" if toward else "more"), "The Sun gives off %s energy in %s." % ("more" if toward else "less", m)],
                "Seasons come from Earth's 23.5° tilt, not its distance from the Sun.")


B1 = bank([
    ("Why does the Moon have phases?", "We see different amounts of its sunlit half as it orbits Earth.", ["Earth's shadow covers part of it.", "Clouds block part of it.", "The Moon changes shape."], "Half the Moon is always lit by the Sun."),
    ("About how long does one cycle of Moon phases take?", "about 29.5 days", ["1 day", "7 days", "365 days"], "About one month."),
    ("Why don't eclipses happen every month?", "The Moon's orbit is tilted about 5°, so the Sun, Earth and Moon usually do not line up exactly.", ["The Moon stops moving.", "Eclipses do happen every month.", "The Sun is too far away."],
     "They need a near-perfect line-up."),
    ("What causes Earth's seasons?", "the 23.5° tilt of Earth's axis as Earth orbits the Sun", ["Earth's distance from the Sun", "the Moon's phases", "Earth's spinning speed"], "Tilt changes the angle of sunlight."),
    ("Is the far side of the Moon always dark?", "No. It gets sunlight too; we just never see it from Earth.", ["Yes, always.", "Only during eclipses.", "It has no side."], "It is fully lit at new moon."),
    ("Why do we always see the same side of the Moon?", "The Moon rotates once in the same time it takes to orbit Earth.", ["The Moon does not rotate.", "Earth blocks the other side.", "The other side is invisible."], "Synchronous rotation."),
    ("Why is it unsafe to look directly at a solar eclipse without eclipse glasses?", "Sunlight can damage your eyes even when most of the Sun is covered.", ["The Moon is too bright.", "It is safe.", "Eclipses give off radio waves."], "Use proper eye protection."),
    ("When the Northern Hemisphere has summer, what does the Southern Hemisphere have?", "winter", ["summer", "spring", "fall"], "The seasons are opposite."),
])
B5 = bank([
    ("Ava models phases with a lamp (Sun), a ball (Moon) and her head (Earth). Where should the ball be to show a full moon?", "on the opposite side of her head from the lamp", ["between her head and the lamp", "on top of the lamp", "anywhere; it does not matter"],
     "Full moon: Earth is between the Sun and the Moon."),
    ("Leo sees a first-quarter Moon. What fraction of the Moon's face looks lit?", "about half", ["none", "all of it", "about a quarter"], "\"Quarter\" means a quarter of the way through the cycle."),
    ("Mia's model shows Earth closest to the Sun in early January. Why is it still winter in the U.S. then?", "The Northern Hemisphere is tilted away from the Sun.", ["Distance makes it cold.", "The Moon blocks the Sun.", "It is actually summer."],
     "Tilt matters more than distance."),
    ("Which model best explains a solar eclipse?", "Sun → Moon → Earth in a straight line", ["Sun → Earth → Moon in a straight line", "Earth → Sun → Moon in a straight line", "The Moon behind the Sun"], "The Moon's shadow hits Earth."),
    ("Why do more people see a lunar eclipse than a total solar eclipse?", "Everyone on Earth's night side can see the shadowed Moon, but the Moon's shadow on Earth is small.", ["Lunar eclipses are brighter.", "Solar eclipses happen at night.", "Lunar eclipses last only a second."],
     "Earth's shadow is large."),
])


def body():
    think = ("<p>The <b>Sun</b> always lights half of the Moon. As the Moon orbits Earth (about <b>29.5 days</b>), we see different amounts of that lit half: the <b>phases</b>.</p>"
             "<div class='qfig'>" + svg_wrap(820, 118, "".join(moon(i, 50 + 103 * i, 48, 34) + text(50 + 103 * i, 104, PH[i].replace(" moon", "").replace("waxing ", "wax. ").replace("waning ", "wan. "), 12, weight=400) for i in range(8)),
                                             "the eight Moon phases in order") + "</div>"
             "<p><b>Eclipses</b>: a <b>solar eclipse</b> happens when the Moon is between the Sun and Earth (new moon); a <b>lunar eclipse</b> happens when Earth's shadow falls on the Moon (full moon).</p>"
             "<p><b>Seasons</b> come from Earth's <b>23.5° tilt</b>. The hemisphere tilted toward the Sun gets more direct sunlight and longer days, so it has summer.</p>")
    ex = [("First quarter today. Phase in one week?", ["Two steps forward."], "full moon"),
          ("Which phase can have a solar eclipse?", ["The Moon must be between the Sun and Earth."], "new moon")]
    mist = ["Thinking Earth's shadow causes the phases. It causes only lunar eclipses.",
            "Thinking summer happens because Earth is closer to the Sun.",
            "Thinking there is an eclipse every month."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Sun, Earth and Moon", B1 + [(g_name, 12)]),
        ("Phases of the Moon", [(g_name, 4), (g_next, 10), (g_order, 6)]),
        ("Predicting phases", [(g_next, 12), (g_order, 4), (g_ecl, 4)]),
        ("Eclipses and seasons", [(g_ecl, 4), (g_season, 16)]),
        ("Using the model", B5 + [(g_next, 9), (g_order, 5), (g_season, 1)]),
    ])
    make("grade-8", "earth-moon-sun-system", 18, "MS-ESS1-1",
         "Develop and use a model of the Earth-sun-moon system to describe the cyclic patterns of lunar phases, eclipses of the sun and moon, and seasons.",
         "The Earth-Moon-Sun System",
         "Grade 8 Moon Phases, Eclipses and Seasons Worksheets: The Earth-Moon-Sun System",
         "Earth-Moon-Sun System",
         "Free middle school science worksheets on the Earth-Moon-Sun system (NGSS MS-ESS1-1): the eight Moon phases, solar and lunar eclipses, and how Earth's tilt causes seasons. 100 practice questions with answers.",
         "Phases, eclipses and seasons follow cycles.",
         "Moon phases come from seeing more or less of its sunlit half. Eclipses need a line-up. Seasons come from Earth's tilt.",
         body(),
         [("What causes the phases of the Moon?", "Half of the Moon is always lit by the Sun. As the Moon orbits Earth, we see different amounts of the lit half."),
          ("What is the difference between a solar and a lunar eclipse?", "In a solar eclipse, the Moon blocks the Sun from Earth. In a lunar eclipse, Earth's shadow falls on the Moon."),
          ("What causes seasons?", "Earth's axis is tilted 23.5°. The hemisphere tilted toward the Sun gets more direct sunlight and longer days, so it has summer.")],
         sets)


if __name__ == "__main__":
    main()
