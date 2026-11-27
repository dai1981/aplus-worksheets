# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Heat and temperature (Energy)
  python tools/gen_sg_science_p4_heat_and_temperature.py
Heat is a form of energy; temperature is a measure of how hot or cold something is (thermometer, °C).
Heat flows from a hotter place or object to a colder one until both are at the same temperature.
Effects of heat gain and loss: temperature change, expansion and contraction, change of state.
Thermometer readings and cooling curves are drawn and computed here; some UK and US cooling questions are reused
(without particles or radiation and convection, which come later).
Wrong answers come from real mistakes: "cold flows into the hot drink", "heat and temperature are the same",
"a bigger object at the same temperature is hotter", "objects expand when they lose heat".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, svg_wrap, text, line, rect, circle, RED, INK, GRAY

U = Unit(63405)
R = U.R
P = People(R)
REP = [(r"thermal energy", "heat"), (r"Thermal energy", "Heat")]
DROP = ["equilibrium", "particle", "kinetic", "radiation", "convection", "conduction", "loft", "double-glaz", "winter", "snow", "heating bill"]
TE = use(U, "gen_uk_science_y9_thermal_energy", rep=REP, drop=DROP)
UT = use(U, "gen_us_science_g6_thermal_energy_and_temperature", rep=REP, drop=DROP + ["spark", "lake"])


def thermo(t, lo=0, hi=100, step=10):
    """a simple glass thermometer, vertical, scale every `step` degrees"""
    H, top, bot = 260, 20, 220
    x = 60

    def y(v):
        return bot - (v - lo) * (bot - top) / float(hi - lo)
    p = [rect(x - 8, top - 8, 16, bot - top + 16, fill="#ffffff", stroke=INK, rx=8), circle(x, bot + 16, 14, fill=RED, stroke=INK),
         rect(x - 4, y(t), 8, bot - y(t) + 10, fill=RED, stroke="none")]
    v = lo
    while v <= hi:
        p.append(line(x + 8, y(v), x + 20, y(v), col=INK))
        p.append(text(x + 24, y(v) + 4, "%d" % v, fs=12, anchor="start"))
        v += step
    v = lo
    while v <= hi:
        p.append(line(x + 8, y(v), x + 15, y(v), col=INK, w=1))
        v += step / 2.0
    p.append(text(x + 52, top - 6, "°C", fs=12, anchor="start"))
    return svg_wrap(160, H + 20, "".join(p), "thermometer")


def g_read():
    k = R.choice(["10", "2"])
    if k == "10":
        t = R.choice(range(5, 100, 5))
        svg = thermo(t, 0, 100, 10)
        w = sorted({t + 5, t - 5, t + 10, t - 10} - {t})
    else:
        t = R.choice(range(30, 51))
        svg = thermo(t, 30, 50, 2)
        w = sorted({t + 1, t - 1, t + 2, t - 2} - {t})
    if not once(("rd", k, t)) or not once(("rdn", k), 4):
        return None
    w = R.sample([x for x in w if x >= 0], 3)
    return item("<div class='qfig'>%s</div>What temperature does the thermometer show?" % svg, "%d °C" % t, ["%d °C" % x for x in w],
                "Read the scale at the top of the red liquid.")


def g_flow():
    pairs = [("a cup of hot tea", "the air in the room", 0), ("an ice cube", "your hand", 1), ("a hot iron", "a cotton shirt", 0),
             ("a cold can of drink", "the air in the room", 1), ("hot soup", "a metal spoon", 0), ("your warm hand", "a cold metal railing", 0),
             ("a hot pan", "the cold water poured into it", 0), ("ice", "the warm drink in a glass", 1), ("a sunny road", "your bare feet", 0),
             ("a cold towel", "the forehead of a person with a fever", 1)]
    a, b, h = R.choice(pairs)
    hot, cold = (a, b) if h == 0 else (b, a)
    k = R.choice(["dir", "gain", "lose"])
    if not once(("fl", a, k)) or not once(("fln", k), 6):
        return None
    if k == "dir":
        return item("%s touches %s. In which direction does heat flow?" % (a[0].upper() + a[1:], b), "from %s to %s" % (hot, cold),
                    ["from %s to %s" % (cold, hot), "both ways equally", "heat does not flow"], "Heat flows from a hotter object to a colder one.")
    if k == "gain":
        return item("%s touches %s. Which one gains heat?" % (a[0].upper() + a[1:], b), cold, [hot, "both of them", "neither of them"],
                    "The colder object gains heat from the hotter one.")
    return item("%s touches %s. Which one loses heat?" % (a[0].upper() + a[1:], b), hot, [cold, "both of them", "neither of them"],
                "The hotter object loses heat to the colder one.")


def g_mix():
    t1 = R.choice([60, 70, 80, 90])
    t2 = R.choice([10, 20, 30])
    k = R.choice(["between", "final"])
    if not once(("mx", t1, t2, k)) or not once(("mxn", k), 5):
        return None
    if k == "between":
        return item("Hot water at %d °C is mixed with cold water at %d °C. What could the temperature of the mixture be?" % (t1, t2),
                    "%d °C" % ((t1 + t2) // 2), ["%d °C" % (t1 + t2), "%d °C" % (t1 + 5), "%d °C" % max(0, t2 - 5)],
                    "The mixture is between the two temperatures: the hot water loses heat and the cold water gains heat.")
    room = 28
    return item("A cup of water at %d °C is left in a room at %d °C for a long time. What will its final temperature be?" % (t1, room),
                "about %d °C" % room, ["%d °C" % t1, "0 °C", "%d °C" % (t1 + room)], "It loses heat until it reaches the temperature of the surroundings.")


def g_cool():
    t0 = R.choice([80, 85, 90, 95])
    room = R.choice([26, 28, 30])
    temps = [t0]
    for _ in range(4):
        d = max(1, int((temps[-1] - room) * 0.4))
        temps.append(temps[-1] - d)
    mins = [0, 5, 10, 15, 20]
    k = R.choice(["at10", "drop", "fast", "room", "trend"])
    if not once(("co", k), 1 if k in ("fast", "room", "trend") else 4):
        return None
    tb = table(["Time (min)", "Temperature of water (°C)"], [[str(m), str(t)] for m, t in zip(mins, temps)])
    q0 = "%s left a cup of hot water to cool in a room at %d °C.<br>%s" % (P.next()[0], room, tb)
    if k == "at10":
        return item(q0 + "What was the temperature after 10 minutes?", "%d °C" % temps[2], ["%d °C" % x for x in (temps[1], temps[3], t0 - 10)], "Read the row for 10 min.")
    if k == "drop":
        d = t0 - temps[2]
        w = sorted({temps[2], t0 - temps[1], d + 5} - {d})
        if len(w) < 3:
            return None
        return item(q0 + "By how much did the temperature fall in the first 10 minutes?", "%d °C" % d, ["%d °C" % x for x in w],
                    "%d − %d = %d °C." % (t0, temps[2], t0 - temps[2]))
    if k == "fast":
        return item(q0 + "When did the water cool the fastest?", "in the first 5 minutes", ["from 5 to 10 minutes", "from 10 to 15 minutes", "from 15 to 20 minutes"],
                    "The bigger the difference from the room temperature, the faster it cools.")
    if k == "room":
        return item(q0 + "What is the lowest temperature the water will reach?", "%d °C" % room, ["0 °C", "%d °C" % temps[4], "%d °C" % (room - 10)],
                    "It stops cooling when it reaches the temperature of the room.")
    return item(q0 + "Why did the temperature of the water fall?", "The water lost heat to the cooler air around it.", ["Cold flowed into the water.", "The water gained heat from the room.", "The cup made the water cold."],
                "Heat flows from hotter to colder.")


EXP = [("A dented ping-pong ball is put in hot water and the dent pops out.", "The air inside gains heat and expands."),
       ("A tight metal lid on a glass jar becomes easier to open after hot water is run over it.", "The metal lid gains heat and expands."),
       ("Gaps are left between sections of a railway track.", "The tracks expand on hot days and need room."),
       ("The liquid in a thermometer rises in a hot drink.", "The liquid gains heat and expands."),
       ("Overhead electric cables sag more on hot days.", "The cables gain heat and expand."),
       ("A balloon left in a hot car gets bigger.", "The air inside gains heat and expands."),
       ("A balloon put in a fridge becomes smaller.", "The air inside loses heat and contracts."),
       ("The liquid in a thermometer falls when it is put in ice water.", "The liquid loses heat and contracts.")]


def g_expand():
    s, a = R.choice(EXP)
    if not once(("ex", s)):
        return None
    w = {"expands": ["It loses heat and contracts.", "It gains heat and contracts.", "It loses heat and expands."],
         "contracts": ["It gains heat and expands.", "It gains heat and contracts.", "It loses heat and expands."]}["expands" if "expands" in a else "contracts"]
    subj = a.split(" gains")[0].split(" loses")[0]
    return item("%s Which explains this?" % s, a, [subj + " " + x[3].lower() + x[4:] for x in w], "Most things expand when they gain heat and contract when they lose heat.")


B1 = bank([
    ("What is heat?", "a form of energy", ["a kind of matter", "the same as temperature", "a type of liquid"], "Heat is energy that flows from hotter to colder objects."),
    ("What does temperature tell us?", "how hot or cold something is", ["how much heat something has in total", "how heavy something is", "how big something is"], "Temperature is measured with a thermometer."),
    ("What is the unit of temperature we use in science?", "degrees Celsius (°C)", ["grams (g)", "centimetres (cm)", "millilitres (ml)"], "Water freezes at 0 °C and boils at 100 °C."),
    ("Which instrument measures temperature?", "a thermometer", ["a measuring cylinder", "a balance", "a ruler"], "A data logger with a temperature sensor can also be used."),
    ("What is the main source of heat for the Earth?", "the Sun", ["the Moon", "the sea", "the clouds"], "The Sun gives out light and heat."),
    ("Which of these is NOT a source of heat?", "an ice cube", ["the Sun", "a lit candle", "a gas stove"], "An ice cube takes in heat."),
    ("In which direction does heat flow?", "from a hotter object to a colder object", ["from a colder object to a hotter object", "only upwards", "only through metals"], "Cold does not flow; heat flows."),
    ("When does heat stop flowing between two objects?", "when they are at the same temperature", ["when the hotter one is empty", "after one minute", "never"], "There is no more heat flow when the temperatures are equal."),
])
B2 = bank([
    ("A bucket of water and a cup of water are both at 40 °C. Which is true?", "They have the same temperature, but the bucket has more heat.", ["The bucket is hotter.", "The cup is hotter.", "They have the same amount of heat."], "More water at the same temperature holds more heat."),
    ("Why does a cold drink become warm when left on a table?", "It gains heat from the warmer air around it.", ["It loses cold to the air.", "Cold flows out of it.", "The table cools it."], "Heat flows from the warmer air into the drink."),
    ("What happens to most things when they gain heat?", "They expand.", ["They contract.", "They become heavier.", "They stop moving."], "Expand means get bigger."),
    ("What happens to most things when they lose heat?", "They contract.", ["They expand.", "They melt.", "They become lighter."], "Contract means get smaller."),
    ("Ice is taken out of the freezer. What happens to it?", "It gains heat and melts.", ["It loses heat and melts.", "It gains heat and freezes.", "It loses heat and boils."], "Heat gain can change the state of matter."),
    ("Why do we feel cold when we hold an ice cube?", "Our hand loses heat to the ice.", ["Cold moves from the ice into our hand.", "Our hand gains heat.", "Ice is a source of heat."], "Heat flows from our warm hand to the colder ice."),
    ("Water is heated from 25 °C to 60 °C. What happened to it?", "It gained heat and its temperature rose.", ["It lost heat.", "Its temperature fell.", "Nothing happened."], "Gaining heat raises the temperature."),
    ("Which is the best way to describe a fever?", "a body temperature higher than normal, about 37 °C", ["a body temperature of 0 °C", "a body that has no heat", "a cold body"], "Normal body temperature is about 37 °C."),
])
B3 = bank([
    ("Why do concrete roads have gaps between slabs?", "The slabs expand on hot days and need space.", ["To let rainwater flow through.", "To save concrete.", "To make cars slow down."], "Without gaps the road could crack."),
    ("A glass jar's metal lid is stuck. Why does running hot water over the lid help?", "The metal lid expands more than the glass, so it becomes looser.", ["The glass expands and pushes the lid off.", "Hot water is slippery.", "The lid contracts."], "Metals expand quite a lot when heated."),
    ("Why are electric cables hung loosely between poles?", "They contract on cool nights and would snap if too tight.", ["To make them look nice.", "So birds can sit on them.", "To make electricity flow faster."], "Cables contract when they lose heat."),
    ("Why should a bottle of soft drink not be left in a hot car?", "The gas inside expands and the bottle may burst.", ["The drink will freeze.", "The bottle will shrink.", "The drink will lose its colour."], "Heated gases expand."),
    ("How does a thermometer work?", "The liquid inside expands when heated and contracts when cooled.", ["The glass changes colour.", "The liquid turns into gas.", "The numbers move."], "The liquid moves up and down the scale."),
    ("Why do we see 'steam' above a pot of boiling soup?", "Water gains heat, becomes water vapour and then cools into tiny droplets.", ["Heat is a white gas.", "The pot gives out smoke.", "The soup is melting."], "Heat gain causes a change of state."),
])
B5 = bank([
    ("Siti put a thermometer in hot water every minute. Why should she wait a few seconds before reading it each time?", "to let the liquid in the thermometer stop moving", ["to cool the water", "to make the thermometer hotter", "to save time"], "This gives an accurate reading."),
    ("Ravi poured equal amounts of hot water into a large tank and a small cup at the same temperature. Which loses more heat by the time both reach room temperature?", "the large tank", ["the small cup", "both the same", "neither"], "More water at the same starting temperature has more heat to lose."),
    ("Mei Ling put a flask of 80 °C water and an open cup of 80 °C water in the same room. After 30 minutes, which would be warmer?", "the water in the flask", ["the water in the cup", "both the same", "neither, both would be at room temperature at once"], "The flask slows down heat loss."),
    ("Why is it important to read a thermometer with your eyes at the level of the liquid?", "to get an accurate reading", ["to make the liquid rise", "to cool the thermometer", "to keep the thermometer clean"], "Looking from above or below gives a wrong reading."),
    ("A pupil heated 100 ml and 300 ml of water on the same hot plate for 3 minutes. Which rose more in temperature?", "the 100 ml of water", ["the 300 ml of water", "both the same", "neither"], "The same heat raises the temperature of a smaller amount more."),
])


def body():
    think = ("<p><b>Heat is a form of energy. Temperature tells us how hot or cold something is.</b></p>"
             "<ul><li>Temperature is measured in <b>degrees Celsius (°C)</b> with a <b>thermometer</b>.</li>"
             "<li>Heat flows from a <b>hotter</b> object to a <b>colder</b> one until both are at the same temperature. Cold does not flow.</li>"
             "<li>Gaining heat: temperature rises, things <b>expand</b>, solids may melt. Losing heat: temperature falls, things <b>contract</b>, liquids may freeze.</li></ul>")
    ex = [("A cup of 90 °C tea is left in a 28 °C room. What happens?", ["Heat flows from the tea to the air", "The tea cools until it reaches 28 °C"], "It cools to about 28 °C."),
          ("A dented ping-pong ball is put in hot water. Why does the dent pop out?", ["The air inside gains heat", "The air expands"], "The air expands and pushes out the dent.")]
    mist = ["Saying 'cold flows into' something. Heat flows out of the warmer object.",
            "Thinking heat and temperature are the same. A bathtub of warm water has more heat than a cup at the same temperature.",
            "Thinking things expand when they lose heat. They contract.",
            "Reading a thermometer from above or below the liquid level."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Heat and temperature", B1 + [(g_read, 6), (g_flow, 4), (UT.g_te, 2)]),
        ("Heat flow", B2 + [(g_flow, 6), (g_mix, 4), (g_read, 2)]),
        ("Expanding and contracting", B3 + [(g_expand, 8), (g_flow, 2), (TE.g_cool, 2), (g_read, 2)]),
        ("Reading temperatures", TE.B1 + [(g_read, 5), (g_cool, 6), (g_mix, 2), (UT.g_mass, 3), (g_expand, 2)]),
        ("PSLE-style experiments", B5 + [(g_cool, 6), (UT.g_mass, 3), (UT.g_energy, 3), (TE.g_cool, 3)]),
    ])
    make_sg(4, "heat-and-temperature", 5, "Energy", "Energy forms and uses (Heat)",
            "Recognise that heat is a form of energy and that temperature is a measure of the degree of hotness of an object, measured with a thermometer in °C. "
            "Show that heat flows from a hotter to a colder place or object, and recognise the effects of heat gain and heat loss: temperature change, "
            "expansion and contraction, and change of state (summary of the MOE Primary Science Syllabus).",
            "Heat and Temperature",
            "Primary 4 Science: Heat and Temperature Worksheets (with Answers)",
            "Heat and temperature",
            "Free Primary 4 science worksheets for Singapore pupils on heat and temperature: reading thermometers, heat flow, expansion and contraction, and cooling experiments. 100 questions with answers.",
            "Heat flows from hotter to colder things.",
            "Temperature tells us how hot or cold something is.",
            body(),
            [("What is the difference between heat and temperature?", "Heat is a form of energy. Temperature is a measure of how hot or cold something is. A large pot of water and a small cup can have the same temperature, but the pot has more heat."),
             ("Does cold flow?", "No. Heat flows from the hotter object to the colder one. When you hold ice, your hand loses heat to the ice."),
             ("Why do things expand when heated?", "Most solids, liquids and gases get bigger when they gain heat and smaller when they lose heat. That is why railway tracks have gaps.")],
            sets)


if __name__ == "__main__":
    main()
