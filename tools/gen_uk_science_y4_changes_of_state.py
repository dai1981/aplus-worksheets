# -*- coding: utf-8 -*-
"""
UK Year 4 science: Changes of State (States of matter)
  python tools/gen_uk_science_y4_changes_of_state.py
Melting, freezing, evaporating, boiling and condensing; the temperatures at which they happen in degrees Celsius;
reading thermometers; and a heating investigation of ice turning to water and steam.
Wrong answers come from real mistakes: "water boils at 50 °C", "freezing and melting happen at different
temperatures for water", "steam is the white cloud you see" (that is tiny water droplets), "heating always makes
temperature rise" (it stays at 0 °C while ice melts).
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61408)
R = U.R
P = People(R)

WORD = [("melting", "solid", "liquid", "heated"), ("freezing", "liquid", "solid", "cooled"), ("evaporating", "liquid", "gas", "heated"),
        ("condensing", "gas", "liquid", "cooled"), ("boiling", "liquid", "gas", "heated quickly")]
EX = [("An ice lolly drips on a hot day.", "melting"), ("A puddle disappears on a sunny afternoon.", "evaporating"), ("Water droplets form on a cold can of drink.", "condensing"),
      ("A pond turns to ice in winter.", "freezing"), ("Bubbles form all through a pan of water on a hot hob.", "boiling"), ("Chocolate goes runny in your pocket.", "melting"),
      ("A bathroom mirror mists up after a shower.", "condensing"), ("Wet washing dries on a line.", "evaporating"), ("Melted candle wax drips and goes hard again.", "freezing"),
      ("Butter goes soft and runny in a hot pan.", "melting"), ("Your breath makes tiny droplets on a cold window.", "condensing"), ("Ice cubes form in a freezer tray.", "freezing")]


def g_word():
    w, a, b, h = R.choice(WORD)
    k = R.random() < 0.5
    if not once(("wd", w, k)):
        return None
    if k:
        return item("What is %s?" % w, "a %s changing into a %s when it is %s" % (a, b, h), ["a %s changing into a %s when it is %s" % (x[1], x[2], x[3]) for x in R.sample([x for x in WORD if x[0] != w and (x[1], x[2]) != (a, b)], 3)],
                    "Changes of state happen when materials are heated or cooled.")
    if w == "boiling":
        return None
    return item("Which word describes a %s changing into a %s?" % (a, b), w, [x[0] for x in WORD if x[0] not in (w, "boiling")],
                "Melting, freezing, evaporating (and boiling), condensing.")


def g_ex():
    s, w = R.choice(EX)
    if not once(("ex", s)):
        return None
    return item("%s Which change of state is this?" % s, w, [x for x in ["melting", "freezing", "evaporating", "condensing", "boiling"] if x != w and not (w == "evaporating" and x == "boiling")][:3] if w != "boiling" else ["melting", "freezing", "condensing"],
                "Is it getting hotter or colder? Which state does it start and end in?")


TEMP = [("the temperature at which pure water freezes", "0 °C"), ("the temperature at which pure water boils", "100 °C"), ("about the temperature of a healthy human body", "37 °C"),
        ("about the temperature inside a home freezer", "−18 °C"), ("about the temperature inside a fridge", "4 °C"), ("about the temperature of a warm classroom", "20 °C")]


def g_temp():
    d, t = R.choice(TEMP)
    if not once(("te", d)):
        return None
    return item("What is %s?" % d, t, R.sample([x[1] for x in TEMP if x[1] != t], 3), "Temperature is measured in degrees Celsius (°C).")


MP = [("chocolate", 34), ("butter", 32), ("candle wax", 60), ("ice", 0), ("iron", 1538), ("chocolate spread", 30), ("lead", 327), ("aluminium", 660)]


def g_mp():
    who = P.next()[0]
    rows = R.sample(MP, 4)
    k = R.choice(["first", "last", "room", "read", "hand"])
    ri = R.randrange(4)
    if not once(("mp", tuple(x[0] for x in rows), k, ri if k == "read" else 0)):
        return None
    f = lambda v: format(v, ",") if v >= 1000 else str(v)
    tab = table(["Material", "Melting point (°C)"], [[a, f(b)] for a, b in rows])
    intro = tab + "%s found these melting points. " % who
    if k == "first":
        a = min(rows, key=lambda r: r[1])[0]
        return item(intro + "Which material melts at the lowest temperature?", a, [r[0] for r in rows if r[0] != a], "The lowest melting point melts first as things warm up.")
    if k == "last":
        a = max(rows, key=lambda r: r[1])[0]
        return item(intro + "Which material needs the highest temperature to melt?", a, [r[0] for r in rows if r[0] != a], "The highest melting point.")
    if k == "read":
        a, b = rows[ri]
        g = "%s °C" % f(b)
        return item(intro + "What is the melting point of %s?" % a, g, uniq(g, ["%s °C" % f(r[1]) for r in rows] + ["%s °C" % f(b + 10)]), "Read the row.")
    if k == "room":
        solid = [r[0] for r in rows if r[1] > 20]
        liquid = [r[0] for r in rows if r[1] <= 20]
        if len(liquid) != 1 or len(solid) < 3:
            return None
        a = liquid[0]
        return item(intro + "In a room at 20 °C, which material would already be melted?", a, solid[:3], "Above its melting point, a material is a liquid.")
    warm = [r[0] for r in rows if r[1] < 37]
    w = [r[0] for r in rows if r[1] >= 37]
    if len(warm) != 1:
        return None
    return item(intro + "Your hand is about 37 °C. Which material would melt if you held it?", warm[0], w, "Materials with melting points below 37 °C melt in your hand.")


def g_heat():
    who = P.next()[0]
    t = [-10, -4, 0, 0, 0, 8, 20, 35]
    mins = list(range(0, 16, 2))
    k = R.choice(["read", "flat", "start", "rise"])
    ri = R.randrange(len(t))
    if not once(("he", who, k, ri if k == "read" else 0)) or (k != "read" and not once(("hk", k), 3)):
        return None
    tab = table(["Time (minutes)", "Temperature (°C)"], [[str(a), str(b).replace("-", "−")] for a, b in zip(mins, t)])
    intro = tab + "%s heated some crushed ice in a beaker and took its temperature every 2 minutes. " % who
    if k == "read":
        g = ("%d °C" % t[ri]).replace("-", "−")
        return item(intro + "What was the temperature after %d minutes?" % mins[ri], g, uniq(g, [("%d °C" % x).replace("-", "−") for x in t] + ["100 °C"]), "Read the row.")
    if k == "flat":
        return item(intro + "Why did the temperature stay at 0 °C for a while?", "The ice was melting, using the heat to change state.", ["The thermometer was broken.", "The ice was boiling.", "Heat stopped going in."],
                    "While ice melts, its temperature stays at 0 °C.")
    if k == "start":
        return item(intro + "What was the temperature at the start?", "−10 °C", ["0 °C", "10 °C", "100 °C"], "Read the first row: below freezing.")
    return item(intro + "What happened after all the ice had melted?", "The water's temperature started to rise.", ["The temperature fell.", "The water froze again.", "The water boiled at 8 °C."], "Once melted, the heat warms the water.")


B1 = bank([
    ("At what temperature does pure water freeze?", "0 °C", ["100 °C", "10 °C", "−100 °C"], "Ice melts at the same temperature."),
    ("At what temperature does pure water boil?", "100 °C", ["0 °C", "50 °C", "37 °C"], "At sea level."),
    ("What unit do we use for temperature in science?", "degrees Celsius (°C)", ["metres", "kilograms", "newtons"], "Read with a thermometer."),
    ("Is the white cloud above a boiling kettle steam?", "No. Steam is invisible; the cloud is tiny water droplets formed as steam cools.", ["Yes, steam is white.", "It is smoke.", "It is ice."], "Condensation."),
    ("What is the difference between evaporating and boiling?", "Evaporating happens at the surface at any temperature; boiling happens all through the liquid at the boiling point.", ["They are exactly the same.", "Boiling happens at 0 °C.", "Evaporating needs 100 °C."], "Both make a gas."),
    ("Is melting a reversible change?", "Yes. The liquid can be cooled to make it solid again.", ["No, never.", "Only for chocolate.", "Only in winter."], "Changes of state are reversible."),
    ("Which equipment measures temperature?", "a thermometer", ["a newton meter", "a ruler", "a stopwatch"], "Thermo means heat."),
    ("Do all materials melt at the same temperature?", "No. Each material has its own melting point.", ["Yes, at 0 °C.", "Yes, at 100 °C.", "Only metals melt."], "Butter melts far below iron."),
])
B5 = bank([
    ("Why is salt spread on icy roads in winter?", "Salty water freezes at a lower temperature than pure water, so ice melts.", ["Salt heats the road.", "Salt makes ice harder.", "Salt makes cars lighter."], "Melting point changes."),
    ("How could you find out how fast ice melts in different places?", "Put the same size ice cubes in each place and time how long they take to melt.", ["Use different sized ice cubes.", "Look at them once.", "Put them all in the freezer."], "Fair test."),
    ("Why does chocolate melt in your mouth but not in the wrapper on a cold day?", "Your mouth is about 37 °C, above chocolate's melting point; the cold air is below it.", ["Chocolate likes mouths.", "Saliva is hot oil.", "Wrappers stop melting."], "Compare temperatures."),
    ("Why must you be careful near steam from a kettle?", "Steam is very hot and can burn skin.", ["Steam is cold.", "Steam is a solid.", "Steam is safe to touch."], "Safety."),
    ("How do you read a thermometer accurately?", "with your eye level with the top of the liquid", ["from above at an angle", "without looking", "only in the dark"], "Avoid reading errors."),
])


def body():
    think = ("<p><b>Heating and cooling change the state of a material.</b></p>"
             "<ul><li>Heating: solid → liquid (melting), liquid → gas (evaporating or boiling). Cooling: gas → liquid (condensing), liquid → solid (freezing).</li>"
             "<li>Water freezes and melts at 0 °C and boils at 100 °C. Each material has its own melting point.</li>"
             "<li>While ice melts, its temperature stays at 0 °C until all of it has melted.</li></ul>")
    ex = [("A puddle dries up. Change?", ["Liquid → gas"], "evaporating"),
          ("Butter melts at 32 °C. Room at 20 °C?", ["20 is below 32"], "it stays solid")]
    mist = ["Thinking water boils at 50 °C.", "Thinking the white cloud over a kettle is steam.", "Thinking temperature always rises while heating."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Changing state", B1 + [(g_word, 8), (g_ex, 4)]),
        ("Everyday changes", [(g_ex, 8), (g_word, 2), (g_temp, 6), (g_mp, 4)]),
        ("Melting points", [(g_mp, 20)]),
        ("Heating ice", [(g_heat, 14), (g_mp, 6)]),
        ("Investigating temperature", B5 + [(g_heat, 8), (g_mp, 7)]),
    ])
    make_uk(4, "changes-of-state", 8, "States of matter",
            "Observe that some materials change state when they are heated or cooled, and measure or research the temperature at which this happens in degrees Celsius (°C).",
            "Changes of State",
            "Year 4 Science: Changes of State Worksheets (Melting, Freezing, Boiling, °C)",
            "Changes of State",
            "Free Year 4 science worksheets on changes of state: melting, freezing, evaporating, boiling and condensing, melting points in °C, thermometers and a heating-ice investigation. 100 questions with answers.",
            "Heat or cool to change state.",
            "Water melts at 0 °C and boils at 100 °C; every material has its own melting point.",
            body(),
            [("What are the changes of state?", "Melting (solid to liquid), freezing (liquid to solid), evaporating or boiling (liquid to gas) and condensing (gas to liquid)."),
             ("At what temperatures does water change state?", "Pure water freezes and melts at 0 °C and boils at 100 °C."),
             ("Why does ice stay at 0 °C while it melts?", "The heat going in is used to change the ice into water, so the temperature does not rise until all the ice has melted.")],
            sets)


if __name__ == "__main__":
    main()
