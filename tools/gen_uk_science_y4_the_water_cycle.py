# -*- coding: utf-8 -*-
"""
UK Year 4 science: The Water Cycle (States of matter)
  python tools/gen_uk_science_y4_the_water_cycle.py
Evaporation, condensation, precipitation and collection in the water cycle; what makes water evaporate faster
(temperature, wind, surface area); and investigations with dishes of water and drying washing.
Wrong answers come from real mistakes: "clouds are made of water vapour (gas)" (they are tiny droplets),
"water only evaporates when it boils", "the water cycle makes new water", "evaporation is faster in the cold".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61409)
R = U.R
P = People(R)

CYC = [("evaporation", "The Sun warms water in seas, lakes and puddles, and it turns into water vapour."),
       ("condensation", "Water vapour rises, cools and turns into tiny droplets that form clouds."),
       ("precipitation", "Droplets join together and fall as rain, sleet, snow or hail."),
       ("collection", "Water runs into rivers, lakes, the sea and underground, and collects there.")]


def g_name():
    n, d = R.choice(CYC)
    k = R.random() < 0.5
    if not once(("nm", n, k)):
        return None
    if k:
        return item("Which stage of the water cycle is this? %s" % d, n, [x[0] for x in CYC if x[0] != n], "Evaporation → condensation → precipitation → collection.")
    return item("What happens during %s in the water cycle?" % n, d, [x[1] for x in CYC if x[0] != n], "Evaporation → condensation → precipitation → collection.")


def g_next():
    i = R.randrange(4)
    k = R.random() < 0.5
    if not once(("nx", i, k)):
        return None
    if k:
        a = CYC[(i + 1) % 4][0]
        return item("In the water cycle, what comes after %s?" % CYC[i][0], a, [x[0] for x in CYC if x[0] not in (a, CYC[i][0])] + ["boiling"], "The cycle repeats again and again.")
    a = CYC[(i - 1) % 4][0]
    return item("In the water cycle, what comes just before %s?" % CYC[i][0], a, [x[0] for x in CYC if x[0] not in (a, CYC[i][0])] + ["melting"], "The cycle repeats again and again.")


EVE = [("A puddle shrinks on a sunny day.", "evaporation"), ("Snow falls on the hills.", "precipitation"), ("Clouds form above the sea.", "condensation"),
       ("A river carries rainwater to the sea.", "collection"), ("Rain soaks into the ground and fills underground rocks.", "collection"), ("Hailstones bounce on the playground.", "precipitation"),
       ("Mist forms over a lake on a cold morning.", "condensation"), ("Water rises from a warm sea into the air.", "evaporation")]


def g_eve():
    s, n = R.choice(EVE)
    if not once(("ev", s)):
        return None
    return item("%s Which part of the water cycle is this?" % s, n, [x[0] for x in CYC if x[0] != n], "Match what you see to the stage.")


def g_dish():
    who = P.next()[0]
    places = [("sunny windowsill", 40), ("warm classroom", 70), ("shady corridor", 85), ("fridge", 95)]
    rows = R.sample(places, 3)
    rows = sorted(rows, key=lambda r: r[1])
    v = [r[1] + R.choice([-3, 0, 2]) for r in rows]
    k = R.choice(["fast", "slow", "read", "why", "var", "lost"])
    ri = R.randrange(3)
    if not once(("di", tuple(r[0] for r in rows), tuple(v), k, ri if k in ("read", "lost") else 0)) or (k in ("why", "var") and not once(("dk", k), 3)):
        return None
    tab = table(["Where the dish was left", "Water left after 3 days (ml)"], [[r[0], str(x)] for r, x in zip(rows, v)])
    intro = tab + "%s put 100 ml of water in identical dishes in different places. " % who
    if k == "fast":
        return item(intro + "Where did the water evaporate fastest?", rows[0][0], [r[0] for r in rows[1:]] + ["It evaporated equally everywhere."], "The least water left means the most evaporated.")
    if k == "slow":
        return item(intro + "Where did the water evaporate most slowly?", rows[-1][0], [r[0] for r in rows[:-1]] + ["It evaporated equally everywhere."], "The most water left means the least evaporated.")
    if k == "read":
        g = "%d ml" % v[ri]
        return item(intro + "How much water was left in the dish on the %s?" % rows[ri][0], g, uniq(g, ["%d ml" % x for x in v] + ["%d ml" % (100 - v[ri])]), "Read the row.")
    if k == "lost":
        g = "%d ml" % (100 - v[ri])
        return item(intro + "How much water evaporated from the dish on the %s?" % rows[ri][0], g, uniq(g, ["%d ml" % v[ri], "100 ml", "%d ml" % (100 - v[ri] + 10), "%d ml" % (v[ri] - 10)]),
                    "100 − %d = %d ml." % (v[ri], 100 - v[ri]))
    if k == "why":
        return item(intro + "What do the results show?", "Water evaporates faster where it is warmer.", ["Water evaporates faster where it is colder.", "Temperature makes no difference.", "Water only evaporates in fridges."], "Warmth speeds up evaporation.")
    return item(intro + "What should %s keep the same?" % who, "the amount of water and the type of dish", ["the place", "the amount of water left", "nothing"], "Only the place changes.")


def g_dry():
    who = P.next()[0]
    days = [("Monday", "cold, still and cloudy", 9), ("Tuesday", "warm, sunny and still", 5), ("Wednesday", "warm, sunny and windy", 3), ("Thursday", "cool and windy", 6)]
    rows = R.sample(days, 3)
    k = R.choice(["fast", "slow", "read"])
    ri = R.randrange(3)
    if not once(("dr", tuple(r[0] for r in rows), k, ri if k == "read" else 0)):
        return None
    tab = table(["Day", "Weather", "Hours for a T-shirt to dry"], [[a, b, str(c)] for a, b, c in rows])
    intro = tab + "%s timed how long the same wet T-shirt took to dry on the washing line. " % who
    if k == "fast":
        a = min(rows, key=lambda r: r[2])[0]
        return item(intro + "On which day did the T-shirt dry fastest?", a, [r[0] for r in rows if r[0] != a] + ["They were all the same."], "Warm, sunny and windy weather speeds up evaporation.")
    if k == "slow":
        a = max(rows, key=lambda r: r[2])[0]
        return item(intro + "On which day did the T-shirt dry most slowly?", a, [r[0] for r in rows if r[0] != a] + ["They were all the same."], "Cold, still weather slows evaporation.")
    a, b, c = rows[ri]
    g = "%d hours" % c
    return item(intro + "How long did the T-shirt take to dry on %s?" % a, g, uniq(g, ["%d hours" % r[2] for r in rows] + ["%d hours" % (c + 2)]), "Read the row.")


B1 = bank([
    ("What powers the water cycle?", "heat from the Sun", ["the Moon", "wind only", "the Earth's magnetism"], "The Sun evaporates water."),
    ("What are clouds made of?", "tiny droplets of water (or ice crystals)", ["water vapour gas", "smoke", "cotton wool"], "Vapour condenses into droplets."),
    ("What is water vapour?", "water as an invisible gas", ["very small ice cubes", "fog you can see", "a cloud"], "We cannot see it."),
    ("Does water have to boil to evaporate?", "No. It evaporates at any temperature, just faster when warm.", ["Yes, always at 100 °C.", "Yes, it must boil first.", "No, it never evaporates."], "Puddles dry without boiling."),
    ("What is precipitation?", "water falling from clouds as rain, sleet, snow or hail", ["water rising as vapour", "water running in rivers", "water freezing in a pond"], "It falls."),
    ("Does the water cycle make new water?", "No. The same water moves round and round.", ["Yes, every day.", "Yes, in clouds.", "Only in winter."], "The water on Earth is reused."),
    ("Why does a cold drink can get wet on the outside?", "Water vapour in the air condenses on the cold surface.", ["Water leaks through the can.", "The drink sweats.", "It is raining inside."], "Condensation."),
    ("Which part of the water cycle happens when a puddle dries up?", "evaporation", ["condensation", "precipitation", "collection"], "Liquid to gas."),
])
B5 = bank([
    ("Why does washing dry faster on a windy day?", "Wind carries water vapour away, so more water can evaporate.", ["Wind makes water heavier.", "Wind is cold, so it dries faster.", "Wind stops evaporation."], "Moving air speeds evaporation."),
    ("Why does water in a wide plate evaporate faster than in a narrow cup?", "More of the water's surface is open to the air.", ["Plates are warmer.", "Cups are magic.", "Plates hold more water."], "Surface area."),
    ("How could you show that evaporation depends on temperature?", "Put the same amount of water in identical dishes in warm and cold places and measure what is left.", ["Use different dishes.", "Use different amounts of water.", "Put them all in one place."], "Fair test."),
    ("Why is it important to have clean rivers, even though water is recycled?", "Pollution can stay in the water as it moves through the cycle.", ["Rivers are not part of the water cycle.", "Pollution evaporates away safely.", "Clean water is not needed."], "Protect water."),
    ("Why do the windows of a warm kitchen steam up in winter?", "Water vapour from cooking condenses on the cold glass.", ["The glass melts.", "It rains indoors.", "The windows evaporate."], "Warm vapour meets cold glass."),
])


def body():
    think = ("<p><b>The same water moves round and round the water cycle, powered by the Sun.</b></p>"
             "<ul><li>Evaporation: the Sun heats water and it becomes water vapour. Condensation: vapour cools into droplets that form clouds.</li>"
             "<li>Precipitation: rain, sleet, snow or hail falls. Collection: water gathers in rivers, lakes, seas and underground.</li>"
             "<li>Water evaporates faster when it is warmer, windier and spread out more.</li></ul>")
    ex = [("A puddle disappears on a hot day. Stage?", ["Liquid → gas"], "evaporation"),
          ("Dish: 100 ml at start, 45 ml left. Evaporated?", ["100 − 45"], "55 ml")]
    mist = ["Thinking clouds are water vapour gas (they are droplets).", "Thinking water must boil to evaporate.", "Thinking the water cycle makes new water."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The water cycle", B1 + [(g_name, 8), (g_next, 4)]),
        ("Stages of the cycle", [(g_next, 4), (g_eve, 8), (g_dry, 8)]),
        ("Evaporation investigation", [(g_dish, 20)]),
        ("Drying washing", [(g_dry, 10), (g_dish, 10)]),
        ("Thinking about water", B5 + [(g_dish, 10), (g_dry, 5)]),
    ])
    make_uk(4, "the-water-cycle", 9, "States of matter",
            "Identify the part played by evaporation and condensation in the water cycle and associate the rate of evaporation with temperature.",
            "The Water Cycle",
            "Year 4 Science: The Water Cycle Worksheets (Evaporation and Condensation)",
            "The Water Cycle",
            "Free Year 4 science worksheets on the water cycle: evaporation, condensation, precipitation and collection, and investigations into how temperature and wind affect evaporation. 100 questions with answers.",
            "Evaporate, condense, fall, collect.",
            "The Sun drives the water cycle; warmer water evaporates faster.",
            body(),
            [("What are the stages of the water cycle?", "Evaporation, condensation, precipitation and collection. Then the cycle starts again."),
             ("What is the difference between evaporation and condensation?", "Evaporation is a liquid turning into a gas. Condensation is a gas cooling and turning back into a liquid."),
             ("What makes water evaporate faster?", "Higher temperatures, wind and a bigger surface area all make water evaporate faster.")],
            sets)


if __name__ == "__main__":
    main()
