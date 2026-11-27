# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U03: electrical conductors and insulators, and how energy is transferred
and transformed in circuits and appliances (light, sound, heat, movement); generating electricity in Australia.
  python tools/gen_au_science_y6_conductors_insulators_and_energy.py
Reuses the UK Year 4 conductor makers, the SG Primary 5 conductor and energy makers and the US Grade 4 energy conversion makers
with Australian names. Wrong answers come from real mistakes: thinking all shiny or hard things conduct, thinking graphite and
water never conduct, and thinking a device makes energy instead of changing it from one form to another.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

C4 = "gen_uk_science_y4_conductors_and_insulators"
SGc = "gen_sg_science_p5_conductors_and_circuit_diagrams"
SGe = "gen_sg_science_p5_electrical_circuits"
EC = "gen_us_science_g4_energy_conversions"
uk_mat = src(C4, "g_mat")
uk_test = limit(src(C4, "g_test"), 4)
uk_why = src(C4, "g_why")
uk_b1 = src.B(C4, "B1")
uk_b5 = src.B(C4, "B5")
uk_cond = limit(src("gen_uk_science_y6_circuits_and_switches", "g_cond"), 5)
sg_pick = src(SGc, "g_pick")
sg_use = src(SGc, "g_use", rep=[(r"Why is the rubber gloves", "Why are the rubber gloves")])
sg_tester = limit(src(SGc, "g_tester"), 3)
sg_b1 = src.B(SGc, "B1")
sg_conv = src(SGe, "g_conv")
sg_save = src(SGe, "g_save")
sg_b3 = src.B(SGe, "B3")
us_out = src(EC, "g_out")
us_which = src(EC, "g_which")
us_chain = src(EC, "g_chain")
us_extra = src(EC, "g_extra")
us_b1 = src.B(EC, "B1")

POOL = pool(R, [
    ("What is an electrical conductor?", "a material that lets electricity flow through it", ["a material that stops electricity", "a material that makes electricity", "a material that stores light"], "Metals such as copper are good conductors."),
    ("Why are electrical wires made of copper inside and plastic outside?", "Copper conducts the current; plastic insulates to keep people safe.", ["Copper is cheap and plastic conducts.", "Both conduct electricity.", "Plastic makes the current faster."], "Conductor inside, insulator outside."),
    ("Which energy change happens in a solar panel?", "light energy to electrical energy", ["electrical energy to light energy", "sound energy to heat energy", "heat energy to sound energy"], "Many Australian homes have rooftop solar panels."),
    ("Which energy change happens in a wind turbine?", "movement (kinetic) energy to electrical energy", ["electrical energy to wind", "light energy to sound energy", "heat energy to light energy"], "Wind farms operate in several Australian states."),
    ("What energy change happens in the Snowy Hydro power stations?", "the energy of moving water to electrical energy", ["electrical energy to snow", "light energy to heat energy", "sound energy to electrical energy"], "Falling water spins turbines."),
    ("A lamp gets hot as well as giving light. What does this show?", "Some electrical energy is changed into heat.", ["The lamp makes new energy.", "Heat makes electricity.", "The lamp is a conductor of heat only."], "Energy is changed, not made."),
    ("Which kind of lamp wastes the least energy as heat?", "an LED lamp", ["an old filament bulb", "a heat lamp", "a toaster"], "LEDs change more of the energy into light."),
    ("Where does the electrical energy in a battery come from?", "chemical energy stored inside the battery", ["the air", "light from the room", "the wires"], "The chemicals change their energy into electrical energy."),
    ("Why is it dangerous to fly a kite near power lines?", "Electricity can travel through the kite string, especially if it is wet.", ["Power lines are insulators.", "Kites make electricity.", "Power lines are too low."], "Water and some materials can conduct."),
    ("Which material is a conductor even though it is not a metal?", "graphite (pencil lead)", ["plastic", "rubber", "glass"], "Graphite lets electricity flow."),
])
POOL5 = pool(R, [
    ("Mia tests materials in a circuit tester. The lamp lights with foil, a steel nail and graphite, but not with wood or plastic. Which conclusion fits?", "Metals and graphite conduct; wood and plastic insulate.", ["All solids conduct.", "Only foil conducts.", "Nothing conducts."], "Use all the results."),
    ("Jack wants to test which material is the best insulator for a handle. What should he keep the same?", "the size of each piece, the cell and the lamp", ["the material", "nothing", "only the colour"], "Change only the material."),
    ("Ruby measures the brightness of a lamp with different wires: copper 900, steel 400, graphite 150 units. Which is the best conductor?", "copper", ["steel", "graphite", "they are all the same"], "Brighter lamp, better conductor."),
    ("Kai says, 'A torch makes light energy.' How could he say this more accurately?", "A torch changes chemical energy into electrical energy, then into light and heat.", ["A torch makes energy from nothing.", "A torch stores light.", "A torch changes light into chemicals."], "Energy is changed from one form to another."),
    ("Ella compares an old bulb and an LED. Both are equally bright, but the old bulb is much hotter. Which uses energy better?", "the LED", ["the old bulb", "both the same", "neither"], "Less energy is wasted as heat."),
    ("A family installs rooftop solar panels. Which is a benefit?", "They use energy from sunlight, so less electricity comes from burning coal or gas.", ["They work best at night.", "They make the house colder.", "They stop all power cuts."], "Solar energy is renewable."),
])


def main():
    sets = U.sets([
        ("Conductors and insulators", [(POOL, 3), (uk_mat, 8), (sg_pick, 6), (uk_b1, 3)]),
        ("Testing materials", [(uk_test, 4), (uk_cond, 5), (sg_tester, 3), (uk_why, 4), (sg_use, 4)]),
        ("Safety", [(uk_why, 3), (sg_use, 3), (sg_b1, 4), (sg_b3, 4), (POOL, 3), (uk_mat, 3)]),
        ("Energy in circuits", [(us_out, 5), (us_which, 4), (sg_conv, 4), (us_chain, 3), (POOL, 4)]),
        ("Investigations and saving energy", [(POOL5, 6), (uk_b5, 3), (sg_save, 4), (us_extra, 4), (us_b1, 3)]),
    ])
    make_au(YEAR, "conductors-insulators-and-energy", SORT, "AC9S6U03", "Physical sciences",
            "Investigate the transfer and transformation of energy in electrical circuits, including the role of circuit components, "
            "insulators and conductors (summary of the Australian Curriculum v9.0 Science content description).",
            "Conductors, Insulators and Energy", "Conductors and insulators",
            "Free Year 6 science worksheets on electrical conductors and insulators, safety, and energy changes in circuits, appliances, "
            "solar panels and wind turbines. 100 questions with answers.",
            "Conductors let electricity through.", "Insulators block it, and devices change electrical energy into light, sound, heat or movement.",
            "<p><b>Conductors let electricity flow; insulators stop it.</b></p><ul>"
            "<li>Metals (copper, steel, aluminium) and graphite are conductors. Plastic, rubber, wood, glass and dry paper are insulators.</li>"
            "<li>Wires have a copper core to carry the current and a plastic coat to keep us safe.</li>"
            "<li>Energy is not made or destroyed in a circuit: the cell's chemical energy becomes electrical energy, then light, sound, heat or movement.</li></ul>",
            [("Is a steel spoon a conductor?", ["steel is a metal", "metals conduct"], "yes"),
             ("A fan motor: which energy change?", ["electrical energy in", "movement (and some sound and heat) out"], "electrical to kinetic")],
            ["Thinking every shiny or hard object conducts (glass does not).", "Thinking graphite cannot conduct because it is not a metal.",
             "Saying a device makes energy (it changes energy from one form to another)."],
            [("Which materials are good electrical conductors?", "Metals such as copper, aluminium and steel are good conductors. Graphite, the 'lead' in pencils, also conducts."),
             ("Why are electrical cords covered in plastic?", "Plastic is an insulator. It stops the current from leaving the wire, so people do not get a shock."),
             ("What energy changes happen in a torch?", "Chemical energy in the battery changes into electrical energy, which the lamp changes into light and some heat.")],
            sets)


if __name__ == "__main__":
    main()
