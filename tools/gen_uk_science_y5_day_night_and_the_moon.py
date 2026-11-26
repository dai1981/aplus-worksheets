# -*- coding: utf-8 -*-
"""
UK Year 5 science: Day, Night and the Moon (Earth and space)
  python tools/gen_uk_science_y5_day_night_and_the_moon.py
The Earth's rotation explains day and night and the apparent movement of the Sun across the sky; the Moon orbits the
Earth and shows phases; time differences between places; daylight hours in the UK through the year.
Wrong answers come from real mistakes: "the Sun moves round the Earth each day", "night is when the Sun switches
off", "the Moon makes its own light", "phases are the Earth's shadow on the Moon".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61509)
R = U.R
P = People(R)


def g_turn():
    k = R.choice(["deg", "hrs"])
    if k == "deg":
        h = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 18, 20])
        if not once(("dg", h)):
            return None
        g = "%d°" % (15 * h)
        return item("The Earth turns 360° in 24 hours, which is 15° every hour. How far does it turn in %d hour%s?" % (h, "" if h == 1 else "s"), g,
                    uniq(g, ["%d°" % (24 * h), "%d°" % (360 // h if h else 0), "%d°" % (15 + h), "%d°" % (30 * h)]), "15 × %d = %d°." % (h, 15 * h))
    d = R.choice([30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 210, 240, 270, 300, 330, 360])
    if not once(("hr", d)):
        return None
    g = "%d hours" % (d // 15)
    return item("The Earth turns 15° every hour. How long does it take to turn %d°?" % d, g, uniq(g, ["%d hours" % (d // 15 * 2), "%d hours" % (d // 10), "%d hours" % (d // 15 + 2), "24 hours"]),
                "%d ÷ 15 = %d hours." % (d, d // 15))


SKY = [("At sunrise in the UK, where is the Sun in the sky?", "low in the east", ["high in the south", "low in the west", "directly overhead"]),
       ("At midday in the UK, where is the Sun?", "at its highest, in the south", ["low in the east", "low in the west", "in the north"]),
       ("At sunset in the UK, where is the Sun?", "low in the west", ["low in the east", "high in the south", "in the north"]),
       ("Why does the Sun seem to move across the sky?", "The Earth is spinning from west to east.", ["The Sun orbits the Earth each day.", "The Moon pushes the Sun.", "Clouds carry the Sun."]),
       ("Why is it night in the UK when it is day in Australia?", "The UK and Australia are on opposite sides of the spinning Earth.", ["The Sun switches off over the UK.", "Australia is closer to the Sun.", "The Moon blocks the Sun."]),
       ("How long does the Earth take to spin round once?", "about 24 hours", ["about 365 days", "about 28 days", "about 1 hour"]),
       ("Which way does the Earth spin?", "from west to east", ["from east to west", "from north to south", "it does not spin"]),
       ("When it is day for us, which way is our side of the Earth facing?", "towards the Sun", ["away from the Sun", "towards the Moon only", "towards Mars"])]


def g_sky():
    q, a, w = R.choice(SKY)
    if not once(("sk", q)):
        return None
    return item(q, a, w, "Day and night happen because the Earth spins; the Sun only seems to move.")


PH = ["new moon", "waxing crescent", "first quarter", "waxing gibbous", "full moon", "waning gibbous", "last quarter", "waning crescent"]


def g_phase():
    i = R.randrange(8)
    k = R.random() < 0.5
    if not once(("ph", i, k)):
        return None
    if k:
        a = PH[(i + 1) % 8]
        return item("Which phase of the Moon comes after the %s?" % PH[i], a, R.sample([x for x in PH if x not in (a, PH[i])], 3), "New → waxing crescent → first quarter → waxing gibbous → full → waning gibbous → last quarter → waning crescent.")
    a = PH[(i - 1) % 8]
    return item("Which phase of the Moon comes just before the %s?" % PH[i], a, R.sample([x for x in PH if x not in (a, PH[i])], 3), "Waxing means growing; waning means shrinking.")


def g_zone():
    who = P.next()[0]
    city = R.choice([("New York", -5), ("Tokyo", 9), ("Dubai", 4), ("Beijing", 8), ("Rio de Janeiro", -3), ("Delhi", 5.5), ("Sydney", 11)])
    h = R.choice([8, 9, 10, 12, 14, 15, 16])
    if city[1] == 5.5 or not once(("tz", city[0], h)):
        return None
    t = (h + city[1]) % 24
    fmt = lambda x: "%02d:00" % x
    g = fmt(t)
    return item("In winter, %s is %d hours %s London. It is %s in London. What time is it in %s?" % (city[0], abs(city[1]), "ahead of" if city[1] > 0 else "behind", fmt(h), city[0]), g,
                uniq(g, [fmt((h - city[1]) % 24), fmt(h), fmt((t + 12) % 24), fmt((h + abs(city[1]) + 1) % 24)]),
                "Places to the east see the Sun earlier, so their clocks are ahead.")


DAYL = [("January", 8), ("March", 12), ("May", 15), ("June", 16), ("August", 14), ("October", 11), ("December", 7)]


def g_day():
    who = P.next()[0]
    k = R.choice(["read", "diff", "long", "short"])
    a, b = R.sample(DAYL, 2)
    if not once(("dy", k, a[0] if k == "read" else tuple(sorted((a[0], b[0]))) if k == "diff" else who)) or (k in ("long", "short") and not once(("dk", k), 2)):
        return None
    tab = table(["Month", "About how many hours of daylight in London"], [[m, str(h)] for m, h in DAYL])
    if k == "read":
        g = "about %d hours" % a[1]
        return item(tab + "About how many hours of daylight does London get in %s?" % a[0], g, uniq(g, ["about %d hours" % x for _, x in DAYL] + ["about 24 hours"]), "Read the row.")
    if k == "diff":
        if a[1] == b[1]:
            return None
        d = abs(a[1] - b[1])
        if d < 2:
            return None
        g = "about %d hours" % d
        return item(tab + "About how many more hours of daylight are there in %s than in %s?" % ((a if a[1] > b[1] else b)[0], (b if a[1] > b[1] else a)[0]), g,
                    uniq(g, ["about %d hours" % (a[1] + b[1]), "about %d hours" % max(a[1], b[1]), "about %d hours" % (d + 2), "about 24 hours"]), "Subtract the smaller from the larger.")
    if k == "long":
        return item(tab + "Which month in the table has the longest days?", "June", ["December", "March", "October"], "Summer days are long in the UK.")
    return item(tab + "Which month in the table has the shortest days?", "December", ["June", "May", "August"], "Winter days are short in the UK.")


B1 = bank([
    ("What causes day and night?", "the Earth spinning on its axis", ["the Sun orbiting the Earth", "the Moon blocking the Sun", "the Sun switching off"], "One spin takes about 24 hours."),
    ("What is the Earth's axis?", "an imaginary line through the North and South Poles that it spins around", ["the path round the Sun", "the equator", "a line to the Moon"], "Tilted by about 23°."),
    ("How long does the Moon take to orbit the Earth?", "about 27 days (about a month)", ["about 24 hours", "about 365 days", "about 7 days"], "Moonth = month."),
    ("Why can we see the Moon?", "It reflects light from the Sun.", ["It makes its own light.", "It reflects light from the Earth's cities.", "It is on fire."], "The Moon is not a light source."),
    ("What causes the phases of the Moon?", "We see different amounts of its sunlit half as it orbits the Earth.", ["The Earth's shadow covers it.", "The Moon changes shape.", "Clouds block part of it."], "Half is always lit."),
    ("Why do we always see the same side of the Moon?", "It spins once in the same time it takes to orbit the Earth.", ["It does not spin.", "The other side is dark rock.", "The Earth spins too slowly."], "The far side is not always dark."),
    ("What is a full moon?", "when we see the whole sunlit side of the Moon", ["when the Moon is biggest", "when the Moon disappears", "when it is half lit"], "Earth is between the Sun and Moon."),
    ("Where on Earth is it midnight when it is midday in London?", "on the opposite side of the world", ["in Scotland", "in France", "everywhere"], "Opposite side faces away from the Sun."),
])
B5 = bank([
    ("How could you model day and night in class?", "Shine a torch on a globe and slowly turn the globe.", ["Move the torch round a still globe.", "Turn the lights off.", "Spin the torch."], "The Earth turns."),
    ("Why do shadows change direction during a sunny day?", "The Sun appears to move across the sky as the Earth turns.", ["Objects move.", "Shadows are random.", "The Sun gets bigger."], "Link to the Earth's spin."),
    ("Why were sundials used before clocks?", "The Sun's shadow moves in a regular way as the Earth spins.", ["Shadows never move.", "Sundials work at night.", "The Moon controls them."], "Regular motion."),
    ("A pupil says the Sun goes round the Earth because it moves across the sky. What is a better explanation?", "The Earth spins, so the Sun only seems to move.", ["The pupil is correct.", "The Moon moves the Sun.", "The Sun bounces off clouds."], "Apparent movement."),
    ("Why do astronauts on the International Space Station see about 16 sunrises a day?", "They orbit the Earth about 16 times a day.", ["The Sun moves faster in space.", "There are 16 suns.", "Their clocks are wrong."], "Fast orbit."),
])


def body():
    think = ("<p><b>The Earth spins once every 24 hours, giving day and night.</b></p>"
             "<ul><li>The side facing the Sun has day; the side facing away has night. The Sun only appears to move: it rises in the east and sets in the west.</li>"
             "<li>The Earth turns 15° each hour, so places to the east see the Sun first and their clocks are ahead.</li>"
             "<li>The Moon orbits the Earth in about a month. It reflects sunlight; its phases are the parts of its lit half we can see.</li></ul>")
    ex = [("How far does Earth turn in 4 hours?", ["15° × 4"], "60°"),
          ("After first quarter comes?", ["The lit part grows: waxing"], "waxing gibbous")]
    mist = ["Thinking the Sun moves round the Earth each day.", "Thinking the Moon makes its own light.", "Thinking the phases are the Earth's shadow."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Day and night", B1 + [(g_sky, 8), (g_turn, 4)]),
        ("The spinning Earth", [(g_turn, 10), (g_zone, 10)]),
        ("Phases of the Moon", [(g_phase, 14), (g_turn, 6)]),
        ("Daylight hours", [(g_day, 14), (g_zone, 6)]),
        ("Explaining the sky", B5 + [(g_day, 6), (g_zone, 6), (g_turn, 3)]),
    ])
    make_uk(5, "day-night-and-the-moon", 9, "Earth and space",
            "Describe the movement of the Moon relative to the Earth. Use the idea of the Earth's rotation to explain day and night and the apparent movement of the sun across the sky.",
            "Day, Night and the Moon",
            "Year 5 Science: Day, Night and the Moon Worksheets (Earth's Rotation, Moon Phases)",
            "Day, Night and the Moon",
            "Free Year 5 science worksheets on day and night and the Moon: the Earth's rotation, the Sun's apparent movement, time differences, daylight hours and the phases of the Moon. 100 questions with answers.",
            "The spinning Earth makes day and night.",
            "The Sun only seems to move; the Moon orbits us about once a month.",
            body(),
            [("Why do we have day and night?", "The Earth spins on its axis once about every 24 hours. The half facing the Sun has day, and the half facing away has night."),
             ("Does the Sun move across the sky?", "It only appears to. The Earth spins from west to east, so the Sun seems to rise in the east and set in the west."),
             ("Why does the Moon change shape?", "It doesn't. As the Moon orbits the Earth we see different amounts of the half that is lit by the Sun, which gives the phases.")],
            sets)


if __name__ == "__main__":
    main()
