# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Good and poor conductors of heat (Energy)
  python tools/gen_sg_science_p4_heat_conductors_and_insulators.py
Good conductors of heat (metals) let heat flow through them quickly; poor conductors (wood, plastic, rubber, cloth,
styrofoam, air) let heat flow slowly and are used to keep things hot or cold. A metal object feels colder than a wooden
one at the same temperature because it conducts heat away from the hand faster.
Fair tests are written here: wax on rods of different materials, ice wrapped in different materials, hot water in cups.
UK and US heat-insulation questions are reused with Singapore names ("thermal energy" is called heat here).
Wrong answers come from real mistakes: "a metal spoon is colder than a wooden spoon in the same room",
"a woollen blanket gives out heat", "insulators only keep things hot", "air is a good conductor".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63406)
R = U.R
P = People(R)
REP = [(r"thermal energy", "heat"), (r"\bthermal insulator", "poor conductor of heat"), (r"\bthermal conductor", "conductor of heat")]
DROP = ["magnet", "electric", "transparen", "solub", "dissolv", "scratch", "winter", "snow", "absorb", "waterproof", "flexib", "conduction", "convection", "radiation", "particle", "kinetic"]
PM = use(U, "gen_uk_science_y5_properties_of_materials", rep=REP, drop=DROP)
DH = use(U, "gen_us_science_g6_designing_to_control_heat_transfer", rep=REP, drop=DROP)

GOOD = ["copper", "aluminium", "iron", "steel", "silver", "brass"]
POOR = ["wood", "plastic", "rubber", "cotton cloth", "styrofoam", "wool", "cork", "air", "glass", "paper"]


def g_class():
    k = R.choice(["good", "poor"])
    a = R.choice(GOOD if k == "good" else POOR)
    if not once(("cl", a)):
        return None
    if k == "good":
        return item("Which of these is a good conductor of heat?", a, R.sample(POOR, 3), "%s is a metal. Metals are good conductors of heat." % a.capitalize())
    return item("Which of these is a poor conductor of heat?", a, R.sample(GOOD, 3), "%s lets heat flow through slowly." % a.capitalize())


USES = [("the handle of a frying pan", "plastic or wood", "It is a poor conductor of heat, so the handle does not get too hot to hold.", ["copper", "steel", "aluminium"]),
        ("the bottom of a cooking pot", "copper or steel", "It is a good conductor of heat, so heat from the stove reaches the food quickly.", ["wood", "plastic", "styrofoam"]),
        ("oven gloves", "thick cloth", "It is a poor conductor of heat and protects the hands from hot trays.", ["aluminium", "steel", "thin plastic film"]),
        ("a cooler box for drinks", "styrofoam", "It is a poor conductor of heat, so heat from outside enters slowly and the drinks stay cold.", ["copper", "aluminium", "steel"]),
        ("a cup for hot coffee to take away", "a paper cup with a cardboard sleeve", "The sleeve is a poor conductor of heat, so it protects your hand.", ["a thin aluminium cup", "a copper cup", "a steel cup with no sleeve"]),
        ("a baking tray", "aluminium", "It is a good conductor of heat, so the food cooks evenly.", ["wood", "styrofoam", "cloth"]),
        ("the soles of shoes for walking on a hot road", "rubber", "It is a poor conductor of heat, so the feet do not get burnt.", ["aluminium", "copper", "iron"]),
        ("a spoon for stirring hot soup", "wood", "It is a poor conductor of heat, so the spoon handle stays cool.", ["copper", "silver", "aluminium"])]


def g_use():
    thing, a, why, w = R.choice(USES)
    k = R.choice(["mat", "why"])
    if not once(("us", thing, k)) or not once(("usn", k), 6):
        return None
    if k == "mat":
        return item("Which material is best for %s?" % thing, a, w, why)
    wrong = ["It is a good conductor of heat, so heat flows through it quickly." if "poor" in why else "It is a poor conductor of heat, so heat flows through it slowly.",
             "It is the heaviest material.", "It is the most colourful material."]
    return item("Why is %s used for %s?" % (a, thing), why, wrong, "Choose a material by how well it conducts heat.")


def g_rod():
    mats = {"copper": (2, 3), "aluminium": (4, 5), "steel": (7, 9), "glass": (18, 22), "wood": (40, 45), "plastic": (35, 39)}
    pick = R.sample(sorted(mats), 4)
    t = [R.randint(*mats[m]) for m in pick]
    k = R.choice(["best", "worst", "order", "var", "same", "measure"])
    if not once(("rd", k, tuple(sorted(pick)))) or not once(("rdn", k), 1 if k in ("var", "same", "measure") else 3):
        return None
    tb = table(["Rod", "Time for the wax bead to fall (min)"], [[m, str(x)] for m, x in zip(pick, t)])
    q0 = "%s fixed a wax bead at the end of four rods of the same size and put the other ends in hot water.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(t, pick))
    if k == "best":
        return item(q0 + "Which rod is the best conductor of heat?", s[0][1], [m for _, m in s[1:]], "Its bead fell first, so heat flowed through it fastest.")
    if k == "worst":
        return item(q0 + "Which rod is the poorest conductor of heat?", s[-1][1], [m for _, m in s[:-1]], "Its bead took the longest to fall.")
    if k == "order":
        return item(q0 + "Which list shows the rods from the best to the poorest conductor of heat?", ", ".join(m for _, m in s),
                    [", ".join(m for _, m in s[::-1]), ", ".join(pick) if pick != [m for _, m in s] else ", ".join([s[1][1], s[0][1], s[2][1], s[3][1]]), ", ".join([s[0][1], s[2][1], s[1][1], s[3][1]])],
                    "The shorter the time, the better the conductor.")
    if k == "var":
        return item(q0 + "What was changed in this experiment?", "the material of the rod", ["the size of the rods", "the temperature of the water", "the size of the wax beads"],
                    "Only the material was changed.")
    if k == "same":
        return item(q0 + "Which should be kept the same for a fair test?", "the length and thickness of the rods", ["the material of the rods", "the time for the beads to fall", "the order the beads fell"],
                    "Only the material should be different.")
    return item(q0 + "What does the time for the bead to fall tell us?", "how quickly heat flows through the rod", ["how heavy the rod is", "how long the rod is", "how hot the room is"],
                "Heat must flow along the rod to melt the wax.")


def g_ice():
    mats = {"styrofoam": (85, 92), "wool": (75, 82), "newspaper": (60, 68), "cotton cloth": (55, 62), "aluminium foil": (25, 35), "nothing (unwrapped)": (20, 28)}
    pick = R.sample(sorted(mats), 4)
    if "aluminium foil" in pick and "nothing (unwrapped)" in pick:
        return None
    left = [R.randint(*mats[m]) for m in pick]
    k = R.choice(["best", "worst", "why", "box"])
    if not once(("ic", k, tuple(sorted(pick)))) or not once(("icn", k), 1 if k == "why" else 3):
        return None
    tb = table(["Wrapped in", "Mass of ice left after 1 hour (g)"], [[m, str(x)] for m, x in zip(pick, left)])
    q0 = "%s wrapped four 100 g ice cubes in different materials and left them on a table.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(left, pick))
    if k == "best":
        return item(q0 + "Which material is the poorest conductor of heat?", s[-1][1], [m for _, m in s[:-1]], "The most ice was left, so heat flowed in most slowly.")
    if k == "worst":
        return item(q0 + "Which ice cube gained heat the fastest?", "the one in " + s[0][1] if "nothing" not in s[0][1] else "the unwrapped one", ["the one in " + m if "nothing" not in m else "the unwrapped one" for _, m in s[1:]],
                    "The least ice was left.")
    if k == "why":
        return item(q0 + "Why did the ice melt?", "It gained heat from the warmer air around it.", ["It lost heat to the air.", "The materials gave out cold.", "The ice gave out heat to the table."],
                    "Heat flows from the warmer surroundings into the ice.")
    return item(q0 + "Which material would be best for keeping ice cream cold on the way home?", s[-1][1], [m for _, m in s[:-1]], "It slows down heat flowing into the ice cream the most.")


B1 = bank([
    ("What is a good conductor of heat?", "a material that lets heat flow through it quickly", ["a material that gives out heat", "a material that stops all heat", "a material that is always cold"], "Metals are good conductors of heat."),
    ("What is a poor conductor of heat?", "a material that lets heat flow through it slowly", ["a material that makes heat", "a material that is always warm", "a material that lets heat flow quickly"], "Wood, plastic and styrofoam are poor conductors."),
    ("Which group of materials are good conductors of heat?", "metals", ["plastics", "fabrics", "woods"], "Copper, aluminium and steel conduct heat well."),
    ("Is air a good or poor conductor of heat?", "a poor conductor", ["a good conductor", "neither", "only cold air is a conductor"], "Trapped air helps to keep things warm or cold."),
    ("Why do we wear thick clothes in a cold country?", "The clothes are poor conductors of heat and slow down heat loss from the body.", ["The clothes give out heat.", "The clothes are good conductors.", "The clothes keep cold in."], "Clothes do not make heat."),
    ("Why do pots have plastic or wooden handles?", "These materials are poor conductors of heat, so the handles stay cool.", ["They are good conductors.", "They are heavy.", "They look nice."], "Heat flows slowly through plastic and wood."),
])
B2 = bank([
    ("A metal spoon and a wooden spoon have been in the same room all day. Why does the metal spoon feel colder?", "Metal conducts heat away from your hand faster.", ["The metal spoon is at a lower temperature.", "Wood gives out heat.", "Metal gives out cold."], "Both are at room temperature."),
    ("A metal railing and a wooden bench are both in the sun at noon. Why does the railing feel hotter?", "Metal conducts heat into your hand faster.", ["The railing is always hotter than wood.", "Wood gives out cold.", "The bench is in the shade."], "Good conductors move heat quickly."),
    ("Why do some cooking pots have copper bottoms?", "Copper is a very good conductor of heat, so the food heats up quickly.", ["Copper keeps heat out.", "Copper is a poor conductor.", "Copper is light."], "Heat from the stove passes quickly to the food."),
    ("Why does a styrofoam box keep fish cold at the market?", "Styrofoam is a poor conductor of heat, so heat from the air enters slowly.", ["Styrofoam is cold.", "Styrofoam gives out cold.", "Styrofoam is a good conductor."], "Poor conductors slow down heat gain as well as heat loss."),
    ("Why do some flasks have a space with very little air between two walls?", "Heat cannot flow easily across the space.", ["The space makes the flask heavier.", "The space stores cold.", "The space lets heat in faster."], "This keeps hot drinks hot and cold drinks cold."),
    ("Which statement is correct?", "Poor conductors of heat can keep things hot and keep things cold.", ["Poor conductors only keep things hot.", "Good conductors keep things cold for longer.", "All materials conduct heat equally."], "They slow down heat flow in either direction."),
])
B3 = bank([
    ("A woollen blanket keeps you warm. Why?", "It is a poor conductor of heat and traps air, so it slows down heat loss from your body.", ["It gives out heat.", "It conducts heat into your body.", "It is a good conductor."], "Your body is the source of the heat."),
    ("Why do birds fluff up their feathers on a cold morning?", "to trap more air, a poor conductor of heat", ["to look bigger", "to let heat out", "to cool down"], "Trapped air slows down heat loss."),
    ("Why is a cup of hot chocolate in a styrofoam cup comfortable to hold?", "Styrofoam is a poor conductor, so little heat flows to your hand.", ["Styrofoam cools the drink at once.", "Styrofoam is a good conductor.", "The drink is not hot."], "Poor conductors protect our hands."),
    ("Which would keep a drink cold for the longest?", "a double-walled plastic bottle", ["a thin aluminium can", "a copper cup", "a steel tray"], "Plastic and trapped air are poor conductors."),
    ("Why are the handles of kettles often made of plastic?", "Plastic is a poor conductor of heat.", ["Plastic is a good conductor of heat.", "Plastic melts easily.", "Plastic is heavy."], "The handle stays cool enough to hold."),
    ("Why does a person feel cold standing barefoot on a tiled floor but not on a carpet?", "Tiles conduct heat away from the feet faster than the carpet does.", ["Tiles are colder than carpet in the same room.", "Carpets give out heat.", "Tiles give out cold."], "Carpet is a poorer conductor."),
])
B5 = bank([
    ("Siti wants to find out which material keeps a drink warm the longest. What should she measure?", "the temperature of the drink after the same time", ["the colour of the material", "the mass of the cup", "the size of the room"], "The warmest drink shows the best material."),
    ("Ravi wrapped three cans of hot water in different materials. Why did he use the same amount of water at the same starting temperature?", "to make the test fair", ["to make the water cool faster", "to make the cans heavier", "to make the materials thicker"], "Only the material should change."),
    ("Why should the cans be put in the same place for the test?", "so that the surroundings are the same for every can", ["so that the water boils", "so that the materials change", "so that the cans are easier to see"], "Different places may be hotter or colder."),
    ("Mei Ling put a metal spoon and a plastic spoon in hot water. After 2 minutes, which handle felt hotter?", "the metal spoon", ["the plastic spoon", "both the same", "neither"], "Heat flowed along the metal faster."),
    ("A pupil found that a can wrapped in wool cooled from 80 °C to 65 °C and an unwrapped can cooled from 80 °C to 50 °C. What can he conclude?", "Wool slows down heat loss.", ["Wool makes heat.", "Wool is a good conductor.", "The unwrapped can gained heat."], "The wrapped can lost less heat."),
])


def body():
    think = ("<p><b>Heat flows through some materials quickly and through others slowly.</b></p>"
             "<ul><li><b>Good conductors of heat</b>: metals such as copper, aluminium and steel. Used for pots and baking trays.</li>"
             "<li><b>Poor conductors of heat</b>: wood, plastic, rubber, cloth, styrofoam and air. Used for handles, oven gloves and cooler boxes.</li>"
             "<li>Poor conductors keep hot things hot <b>and</b> cold things cold, because they slow down heat flow in both directions.</li>"
             "<li>A metal object feels colder than wood at the same temperature because it takes heat from your hand faster.</li></ul>")
    ex = [("Why is a frying pan handle made of plastic?", ["Plastic is a poor conductor of heat", "Little heat reaches your hand"], "So the handle stays cool."),
          ("Wax on a copper rod melts before wax on a glass rod. Which is the better conductor?", ["Heat reached the wax faster on copper"], "Copper.")]
    mist = ["Thinking a metal object in the same room is colder than a wooden one. Both are at the same temperature.",
            "Thinking blankets and clothes give out heat. They slow down heat loss from your body.",
            "Thinking poor conductors only keep things hot. They also keep cold things cold.",
            "Thinking air is a good conductor. Trapped air is a poor conductor."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Good and poor conductors", B1 + [(g_class, 8), (PM.g_pick, 4), (PM.g_prop, 2)]),
        ("Using conductors and insulators", B2 + [(g_use, 7), (DH.g_material, 5), (g_class, 2)]),
        ("Keeping things hot or cold", B3 + [(g_use, 4), (DH.g_material, 3), (PM.g_pick, 3), (g_ice, 2), (DH.g_example, 2)]),
        ("Reading the results", [(g_rod, 6), (g_ice, 5), (PM.g_ins, 4), (DH.g_test, 3), (g_class, 2)]),
        ("PSLE-style experiments", B5 + [(g_rod, 4), (g_ice, 4), (PM.g_ins, 3), (DH.g_test, 4)]),
    ])
    make_sg(4, "heat-conductors-and-insulators", 6, "Energy", "Energy forms and uses (Heat: good and poor conductors of heat)",
            "Identify good and poor conductors of heat and relate their uses to everyday life, such as cooking pots, handles, oven gloves and cooler boxes. "
            "Investigate how well different materials conduct heat in fair tests (summary of the MOE Primary Science Syllabus).",
            "Good and Poor Conductors of Heat",
            "Primary 4 Science: Conductors and Insulators of Heat Worksheets (with Answers)",
            "Conductors of heat",
            "Free Primary 4 science worksheets for Singapore pupils on good and poor conductors of heat: metals, wood, plastic, styrofoam and air, uses, and fair-test experiments. 100 questions with answers.",
            "Metals conduct heat well; wood and plastic do not.",
            "Poor conductors keep hot things hot and cold things cold.",
            body(),
            [("Which materials are good conductors of heat?", "Metals such as copper, aluminium, iron and steel. Heat flows through them quickly."),
             ("Why does metal feel colder than wood in the same room?", "Both are at the same temperature. Metal conducts heat away from your hand faster, so it feels colder."),
             ("Can a poor conductor keep things cold?", "Yes. A styrofoam cooler box slows down heat flowing in from the warm air, so the drinks inside stay cold longer.")],
            sets)


if __name__ == "__main__":
    main()
