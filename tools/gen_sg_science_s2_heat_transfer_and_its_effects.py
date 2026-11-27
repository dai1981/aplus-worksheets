# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Transfer of Heat Energy and its Effects
  python tools/gen_sg_science_s2_heat_transfer_and_its_effects.py
The kelvin as the SI unit of temperature, expansion and contraction and their effects and uses, heat transfer by conduction,
convection and radiation and their uses (cooling, heating, insulation), how surface colour, texture and temperature affect
radiation, density changes on heating, different materials conduct heat at different rates, and global warming.
UK KS3 thermal energy makers are reused (winter heating and lofts are left out).
Wrong answers come from real mistakes: "cold flows into the drink", "black surfaces reflect radiation", "convection happens in
solids", "air is a good conductor".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64203)
R = U.R
P = People(R)
TH = luse(U, "gen_uk_science_y9_thermal_energy", drop=[r"radiator", r"\bloft", r"heating bills", r"double-glazed", r"warmer\b.*homes", r"winter"])

WAYS = [("The handle of a metal spoon in hot soup becomes hot.", "conduction"), ("The air near the ceiling of a room is warmer than near the floor.", "convection"),
        ("You feel the heat from a charcoal fire at a satay stall without touching it.", "radiation"), ("Water at the bottom of a pot heats up and rises.", "convection"),
        ("An air-conditioner is fixed high up on the wall to cool a whole room.", "convection"), ("The Sun warms the Earth across space.", "radiation"),
        ("A hot iron presses the creases out of a shirt.", "conduction"), ("A cold drink can warms up in your hand.", "conduction"),
        ("The freezer compartment is at the top of an old refrigerator.", "convection"), ("A thermal camera detects people in the dark.", "radiation"),
        ("A sea breeze blows from the sea towards the land in the afternoon.", "convection"), ("A road surface feels hot after the Sun shines on it.", "radiation")]


def g_way():
    s, a = R.choice(WAYS)
    if not once(("wy", s)):
        return None
    return item(s + " Which process mainly transfers the heat?", a, [x for x in ["conduction", "convection", "radiation", "evaporation"] if x != a],
                {"conduction": "Heat passes through a solid or between objects in contact.", "convection": "Warmer fluid is less dense and rises; cooler fluid sinks.",
                 "radiation": "Heat travels as infrared waves, even through a vacuum."}[a])


def g_kelvin():
    c = R.choice([-273, -100, -40, 0, 20, 25, 37, 100, 150, 300])
    k = R.choice(["toK", "toC"])
    if not once(("kv", c, k)):
        return None
    K = c + 273
    if k == "toK":
        return item("What is %d °C in kelvin?" % c, "%d K" % K, ["%d K" % (c - 273), "%d K" % c, "%d K" % (K + 100)], "K = °C + 273 = %d + 273 = %d K." % (c, K))
    return item("What is %d K in degrees Celsius?" % K, "%d °C" % c, ["%d °C" % (K + 273), "%d °C" % K, "%d °C" % (c + 10)], "°C = K − 273 = %d − 273 = %d °C." % (K, c))


SURF = [("dull black", "best absorber and best emitter of radiation"), ("shiny silver", "worst absorber and worst emitter of radiation"), ("white", "reflects most radiation")]
CANS = [("dull black", 3), ("matt white", 2), ("shiny silver", 1)]


def g_surf():
    k = R.choice(["hot", "cold"])
    nm, he, his = P.next()
    start = R.choice([60, 65, 70, 75, 80, 85, 90]) if k == "hot" else R.choice([10, 12, 15, 18, 20])
    if not once(("sf", k, start)) or not once(("sfk", k), 2):
        return None
    if k == "hot":
        drop = {c: d * R.choice([4, 5, 6]) for c, d in CANS}
        rows = [[c, str(start), str(start - drop[c])] for c, _ in CANS]
        tb = table(["Can", "Start (°C)", "After 20 min (°C)"], rows)
        return item(tb + "%s filled three cans with hot water. Which can emitted radiation fastest?" % nm, "the dull black can", ["the shiny silver can", "the matt white can", "they all cooled at the same rate"],
                    "The dull black can cooled the most, so it is the best emitter.")
    rise = {c: d * R.choice([3, 4, 5]) for c, d in CANS}
    rows = [[c, str(start), str(start + rise[c])] for c, _ in CANS]
    tb = table(["Can", "Start (°C)", "After 20 min in the sun (°C)"], rows)
    return item(tb + "%s left three cans of cold water in the sun. Which can absorbed radiation fastest?" % nm, "the dull black can", ["the shiny silver can", "the matt white can", "they all warmed at the same rate"],
                "Dull black surfaces are the best absorbers of radiation.")


def g_rods():
    mats = {"copper": (1, 2), "aluminium": (3, 4), "iron": (6, 8), "glass": (25, 30), "wood": (40, 50)}
    pick = R.sample(sorted(mats), 3)
    t = {m: R.randint(*mats[m]) * 10 for m in pick}
    nm = P.next()[0]
    k = R.choice(["best", "worst"])
    if not once(("rd", tuple(sorted(pick)), k)):
        return None
    tb = table(["Rod", "Time for wax at the far end to melt (s)"], [[m, str(t[m])] for m in pick])
    best = min(pick, key=lambda m: t[m]) if k == "best" else max(pick, key=lambda m: t[m])
    return item(tb + "%s heated one end of rods of the same size. Which material is the %s conductor of heat?" % (nm, "best" if k == "best" else "poorest"), best,
                [m for m in pick if m != best] + ["they all conduct equally"], "The %s the wax melted, the %s the material conducts heat." % ("sooner" if k == "best" else "longer", "better" if k == "best" else "worse"))


EXP = [("A bimetallic strip bends when heated.", "The two metals expand by different amounts."), ("Overhead power lines are hung loosely.", "They contract on cool nights and would snap if pulled tight."),
       ("A stuck metal lid on a glass jar opens after hot water is run over it.", "The metal lid expands more than the glass."),
       ("Mercury rises in a clinical thermometer.", "The liquid expands when it is warmed."), ("Expansion gaps are left in long concrete pavements.", "The concrete expands on hot days and needs room."),
       ("A hot-air balloon rises.", "Heated air expands, becomes less dense and rises.")]


def g_exp():
    s, a = R.choice(EXP)
    if not once(("ex", s)):
        return None
    return item(s + " Which is the best explanation?", a, R.sample([x[1] for x in EXP if x[0] != s], 2) + ["The particles become bigger when heated."],
                "Heating makes particles move faster and further apart, so the substance expands.")


MAT = [("the base of a frying pan", "aluminium, because it is a good conductor of heat"), ("the handle of a kettle", "plastic, because it is a poor conductor of heat"),
       ("a cooler box to keep drinks cold", "polystyrene foam, because it traps air, a poor conductor"), ("an oven glove", "thick cloth with trapped air, because it is an insulator"),
       ("a heat sink in a computer", "aluminium with fins, because it conducts heat away and has a large surface area"), ("a takeaway cup for hot kopi", "paper with an air gap, because it slows heat loss"),
       ("the walls of a vacuum flask", "silvered glass, because shiny surfaces reflect radiation"), ("a solar water heater on a roof", "pipes painted dull black, because they absorb radiation well")]


def g_mat():
    u, a = R.choice(MAT)
    if not once(("mt", u)):
        return None
    w = [x[1] for x in MAT if x[0] != u and x[1].split()[0] != a.split()[0] and ("conduct" in x[1]) != ("conduct" in a and "good" in a)]
    if len(w) < 3:
        return None
    return item("Which choice is best for %s?" % u, a[0].upper() + a[1:] + ".", [x[0].upper() + x[1:] + "." for x in R.sample(w, 3)], "Choose good conductors to transfer heat and insulators to stop it.")


B1 = bank([
    ("What is the SI unit of temperature?", "the kelvin (K)", ["the degree Celsius (°C)", "the joule (J)", "the watt (W)"], "0 °C = 273 K."),
    ("Why does heat flow from a hot cup of coffee to the surroundings?", "Heat always flows from a region of higher temperature to a region of lower temperature.", ["Cold flows into the coffee.", "Heat flows from cold to hot.", "The cup creates cold."], "It stops when the temperatures are equal."),
    ("Why can convection not happen in a solid?", "The particles in a solid cannot move from place to place.", ["Solids have no particles.", "Solids are always cold.", "Solids reflect heat."], "Convection needs a fluid: a liquid or a gas."),
    ("Why is a convection current set up when water is heated from below?", "Heated water expands, becomes less dense and rises; cooler, denser water sinks.", ["Hot water is denser and sinks.", "Water particles get bigger.", "Heat travels in straight lines."], "Heating changes density."),
    ("Why does air trapped in a woolly sweater or a cooler box keep heat in?", "Still air is a poor conductor of heat.", ["Air is a good conductor.", "Air creates heat.", "Air reflects all radiation."], "Insulators slow down heat transfer."),
    ("Which surface is the best emitter of infrared radiation?", "dull black", ["shiny silver", "shiny white", "polished glass"], "Good absorbers are also good emitters."),
    ("Why are many buildings and cars in Singapore painted white or light colours?", "Light, shiny surfaces reflect more radiation, so they stay cooler.", ["White surfaces absorb more heat.", "Dark colours reflect heat.", "Colour does not affect heat."], "This reduces the need for air-conditioning."),
    ("How do greenhouse gases cause global warming?", "They trap more infrared radiation from the Earth, so the Earth's average temperature rises.", ["They make the Sun hotter.", "They create a hole in the Earth.", "They reflect all sunlight back into space."], "Burning fuels and clearing forests add carbon dioxide."),
])
B5 = bank([
    ("Why are cooking pots made of metal but have plastic or wooden handles?", "Metal conducts heat to the food; plastic and wood are insulators that keep the handle cool.", ["Metal is an insulator.", "Plastic conducts heat well.", "Handles are for decoration."], "Choose materials by how they conduct heat."),
    ("A vacuum flask has a vacuum between two silvered walls. How does the vacuum keep a drink hot?", "It stops heat transfer by conduction and convection.", ["It stops radiation only.", "It creates heat.", "It makes the drink denser."], "The silvered walls reduce radiation."),
    ("Why does the density of air decrease when it is heated?", "The same mass of air expands to a larger volume.", ["The air loses mass.", "The particles get smaller.", "The air becomes a liquid."], "Density = mass ÷ volume."),
    ("Why is the cooling unit at the top of a refrigerator?", "Cold air is denser and sinks, setting up a convection current that cools the whole space.", ["Cold air rises.", "Heat travels down only.", "It saves space."], "Cooling from the top uses convection."),
    ("A metal spoon and a plastic spoon have been in the same room for hours. The metal one feels colder. Why?", "Metal conducts heat away from your hand faster; both are at the same temperature.", ["The metal spoon is colder.", "Plastic is warmer than the room.", "Metal creates cold."], "Feeling cold depends on how fast heat leaves your hand."),
    ("The Earth's average temperature is rising. Which human activity contributes most?", "burning fossil fuels, which adds carbon dioxide to the air", ["planting trees", "using solar panels", "recycling paper"], "Natural causes such as volcanoes also play a smaller part."),
])


def body():
    think = ("<p><b>Heat flows from a hotter region to a colder region by conduction, convection or radiation.</b></p>"
             "<ul><li><b>Conduction</b>: through solids, from particle to particle. Metals are good conductors; air, wood and plastic are insulators.</li>"
             "<li><b>Convection</b>: in liquids and gases. Heated fluid expands, becomes less dense and rises.</li>"
             "<li><b>Radiation</b>: infrared waves, even through a vacuum. Dull black surfaces absorb and emit best; shiny and white surfaces reflect.</li>"
             "<li>Most substances <b>expand</b> on heating. Temperature in kelvin: K = °C + 273.</li></ul>")
    ex = [("What is 27 °C in kelvin?", ["27 + 273"], "300 K"), ("Why does an air-conditioner work best high on a wall?", ["Cold air sinks"], "It sets up a convection current.")]
    mist = ["Saying 'cold flows in'. Heat flows out of the warmer object.", "Saying black surfaces reflect radiation. They absorb it.",
            "Thinking convection happens in solids.", "Calling air a good conductor. Trapped air is an insulator."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Temperature and heat", B1[:2] + TH.B1[:3] + [(g_kelvin, 8), (TH.g_cool, 5)]),
        ("Conduction, convection and radiation", B1[2:4] + [(g_way, 10), (TH.g_way, 5), (B1[4], 1), (TH.B1[4], 1)]),
        ("Conductors, insulators and surfaces", B1[5:7] + [(g_rods, 6), (g_surf, 2), (TH.g_cool, 3), (TH.B1[3], 1), (g_way, 3), (g_exp, 2), (TH.g_way, 1)]),
        ("Expansion and contraction", [(g_exp, 4), (g_kelvin, 5), (g_surf, 1), (g_mat, 3), (g_rods, 4), (B1[7], 1), (TH.g_way, 3), (TH.g_cool, 2)]),
        ("Exam-style questions", B5 + TH.B5 + [(g_rods, 3), (g_surf, 1), (g_kelvin, 2), (TH.g_cool, 3), (g_way, 2), (TH.g_way, 2), (g_mat, 3), (g_exp, 1)]),
    ])
    make_lss(2, "heat-transfer-and-its-effects", 3, "Interactions", "Transfer of Heat Energy and its Effects",
             "State the kelvin as the SI unit of temperature; describe the effects and applications of expansion and contraction; explain heat transfer by conduction, convection and "
             "radiation and their applications; explain how surface colour, texture and temperature affect heat gained or lost by radiation; infer that heating changes volume and density "
             "and that materials conduct heat at different rates; recognise causes of global warming (summary of the MOE Lower Secondary Science Syllabus).",
             "Heat Transfer and its Effects", seo(2, "Heat Transfer"), "Heat transfer",
             "Free Secondary 2 science worksheets for Singapore students on heat transfer: conduction, convection and radiation, conductors and insulators, expansion, kelvin and global warming. With answers.",
             "Heat flows from hot to cold.", "Conduction in solids, convection in fluids, radiation through space.",
             body(),
             [("What are the three ways heat is transferred?", "Conduction (through solids), convection (in liquids and gases) and radiation (infrared waves, even through a vacuum)."),
              ("Which surfaces absorb radiation best?", "Dull black surfaces are the best absorbers and emitters. Shiny, white surfaces reflect radiation."),
              ("How do you change °C to kelvin?", "Add 273. For example, 25 °C = 298 K.")],
             sets)


if __name__ == "__main__":
    main()
