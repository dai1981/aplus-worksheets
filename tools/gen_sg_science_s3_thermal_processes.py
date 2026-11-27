# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 8: Thermal Processes
  python tools/gen_sg_science_s3_thermal_processes.py
Thermal equilibrium; conduction (particle vibrations, and free electrons in metals), convection (density changes and convection
currents in fluids) and radiation (infrared, no medium needed); the effect of surface colour and texture, surface temperature and
surface area on the rate of emission and absorption of radiation; everyday uses and the vacuum flask.
SG and UK heat transfer makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "cold flows into your hand", "heat rises" (instead of hot fluid rises), "radiation needs
air to travel", "shiny surfaces are good emitters", "convection happens in solids".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto

LV, SUBJ, SORT = 3, "Physics", 8
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

sg_way = src("gen_sg_science_s2_heat_transfer_and_its_effects", "g_way")
sg_rods = src("gen_sg_science_s2_heat_transfer_and_its_effects", "g_rods")
sg_mat = src("gen_sg_science_s2_heat_transfer_and_its_effects", "g_mat")
uk_way = src("gen_uk_science_y9_thermal_energy", "g_way")

WAY = [("The handle of a metal spoon in hot soup becomes hot.", "conduction"), ("Warm air from a heater rises to the top of a room.", "convection"),
       ("You feel the warmth of the Sun on your face.", "radiation"), ("Water at the bottom of a kettle is heated and the whole kettle of water warms up.", "convection"),
       ("You feel warmth on your hands near a campfire, from the side.", "radiation"), ("A metal pot's base becomes hot on a gas stove.", "conduction"),
       ("A sea breeze blows onto the beach on a sunny afternoon.", "convection"), ("Heat reaches the Earth from the Sun through space.", "radiation"),
       ("Your feet feel cold on a ceramic tile floor.", "conduction"), ("Cold air from an air-conditioner sinks to the floor.", "convection"),
       ("A car parked in the sun becomes very hot inside.", "radiation"), ("Ice cream in a cone melts where your hand holds the cone.", "conduction"),
       ("Smoke from a fire rises up a chimney.", "convection"), ("A light bulb warms your hand held a few centimetres beside it.", "radiation"),
       ("A soldering iron's tip heats the wire it touches.", "conduction"), ("A pot of soup on the stove warms evenly from bottom to top.", "convection"),
       ("You feel warm standing in front of an open oven door.", "radiation"), ("A steel bridge railing feels hot to touch at noon.", "conduction")]


COND = [("copper", "good"), ("aluminium", "good"), ("steel", "good"), ("silver", "good"), ("glass", "poor"), ("wood", "poor"), ("plastic", "poor"), ("air", "poor"),
        ("wool", "poor"), ("polystyrene foam", "poor"), ("water", "poor"), ("cotton", "poor")]
RANKC = ["copper", "aluminium", "steel", "glass", "water", "wood", "air"]


def g_cond():
    if R.random() < 0.5:
        m, a = R.choice(COND)
        return tq("Is %s a good or a poor conductor of heat?" % m, "a %s conductor" % a, ["a %s conductor" % ("poor" if a == "good" else "good"), "it does not conduct heat at all", "it only conducts when wet"],
                  "Metals are good conductors (free electrons); non-metals, liquids and gases are poor conductors (insulators).")
    xs = sorted(R.sample(RANKC, 4), key=RANKC.index)
    k = R.choice(["best", "worst"])
    a = xs[0] if k == "best" else xs[-1]
    return tq("Which of these is the %s conductor of heat: %s?" % (k, ", ".join(R.sample(xs, 4))), a, [x for x in xs if x != a],
              "Order from best to worst: copper, aluminium, steel, glass, water, wood, air.")


SRF = ["dull black", "shiny black", "dull white", "shiny silver"]


def g_emit():
    a, b = sorted(R.sample(SRF, 2), key=SRF.index)
    k = R.choice(["absorber", "emitter"])
    return tq("Two identical cans differ only in their surfaces: %s and %s. Which is the better %s of radiation?" % (b, a, k), "the %s can" % a,
              ["the %s can" % b, "both are the same", "neither: cans do not %s radiation" % ("absorb" if k == "absorber" else "emit")],
              "Best to worst absorbers and emitters: dull black, shiny black, dull white, shiny silver.")


def g_way():
    q, a = R.choice(WAY)
    return tq(q + " Which process transfers the thermal energy mainly?", a, [x for x in ("conduction", "convection", "radiation") if x != a] + ["evaporation"],
              "Conduction: through solids by particle collisions. Convection: in fluids by moving hot fluid. Radiation: by infrared waves, no medium needed.")


SURF = [("dull black", "good absorber and good emitter"), ("shiny silver", "poor absorber and poor emitter (good reflector)"),
        ("white", "poor absorber of radiation from the Sun (reflects it)"), ("rough matt", "better emitter than a smooth shiny surface of the same colour")]

RAD = [("Which can of hot water cools fastest: dull black, dull white, shiny silver or shiny white?", "dull black", ["shiny silver", "dull white", "shiny white"], "Dull black surfaces are the best emitters."),
       ("Which can of cold water warms up fastest in sunlight: dull black, shiny silver, white or polished aluminium?", "dull black", ["shiny silver", "white", "polished aluminium"], "Dull black surfaces are the best absorbers."),
       ("Two identical black cans hold water at 80 °C and 50 °C. Which emits radiation at the greater rate at first?", "the can at 80 °C", ["the can at 50 °C", "both the same", "neither: only hot gases emit radiation"], "A hotter surface emits radiation faster."),
       ("Two black metal plates at the same temperature have areas of 0.1 m² and 0.4 m². Which emits more radiation each second?", "the 0.4 m² plate", ["the 0.1 m² plate", "both the same", "neither"], "A larger surface area emits more radiation."),
       ("Why are the cooling fins on the back of a fridge painted black?", "Black is a good emitter of radiation.", ["Black is a good reflector.", "Black is a poor emitter.", "Black looks neat."], "Fins also have a large area."),
       ("Why are many HDB roofs and walls painted in light colours?", "Light colours reflect more of the Sun's radiation, keeping the flats cooler.", ["Light colours absorb more radiation.", "Light colours emit more radiation at night.", "Light paint conducts heat away."], "Poor absorbers stay cooler."),
       ("Why are solar water heater panels painted dull black?", "to absorb as much of the Sun's radiation as possible", ["to reflect radiation", "to look modern", "to reduce conduction"], "Black is the best absorber."),
       ("Why are emergency blankets shiny silver?", "Shiny surfaces are poor emitters, so less thermal energy is lost by radiation.", ["Shiny surfaces absorb more heat from the body.", "Silver conducts heat into the body.", "Silver traps convection currents in."], "Also a good reflector of radiation back to the body."),
       ("Which factor does NOT affect how fast a surface emits radiation?", "the mass of the object", ["its colour", "its surface temperature", "its surface area"], "Colour and texture, temperature and area matter.")]


def g_rad():
    return tq(*R.choice(RAD))


VF = [("the vacuum between the two glass walls", "stops conduction and convection"), ("the silvered inner surfaces of the glass walls", "reduce heat transfer by radiation"),
      ("the stopper (cork or plastic)", "reduces conduction and stops convection and evaporation at the top"), ("the plastic or felt supports holding the inner bottle", "are poor conductors, so they reduce conduction")]
g_vf = rows(R, VF, "In a vacuum flask, what does %s do?", "Which part of a vacuum flask %s?")

POOL1 = pool(R, [
    ("When are two objects in thermal equilibrium?", "when there is no net flow of thermal energy between them because they are at the same temperature", ["when they have the same mass", "when they are both at 0 °C", "when they are made of the same material"], "Thermal energy flows from hotter to colder until temperatures are equal."),
    ("In which direction does thermal energy flow?", "from a region of higher temperature to a region of lower temperature", ["from lower to higher temperature", "from the larger object to the smaller one", "in any direction"], "Until thermal equilibrium is reached."),
    ("Why are metals good conductors of heat?", "They have free electrons that move quickly and carry energy through the metal.", ["Their atoms are far apart.", "They are shiny.", "They are heavy."], "Free electrons add to particle vibrations."),
    ("How is thermal energy conducted in a non-metal such as glass?", "by vibrating particles passing energy to neighbouring particles", ["by free electrons", "by convection currents", "by the particles moving across the solid"], "This is slower than conduction in metals."),
    ("Why are liquids and gases poor conductors?", "Their particles are further apart, so energy is passed on less easily by collisions.", ["They have too many free electrons.", "They have no particles.", "They are always cold."], "Gases are the poorest conductors."),
    ("Why does hot air rise?", "It expands, becomes less dense and is pushed up by the denser cooler air.", ["Heat is light and floats.", "Hot air particles are lighter.", "Gravity does not act on hot air."], "This sets up a convection current."),
    ("Why can convection not happen in a solid?", "The particles in a solid cannot move from place to place.", ["Solids are too hot.", "Solids have no particles.", "Solids are too dense to heat."], "Convection needs a fluid that can flow."),
    ("Why can thermal energy from the Sun reach the Earth only by radiation?", "Space is a vacuum, and radiation is the only process that does not need a medium.", ["Space is very cold.", "Convection is too slow.", "Conduction only works in liquids."], "Radiation is infrared (electromagnetic) waves."),
    ("Why does a woollen jumper keep you warm?", "It traps air, which is a poor conductor.", ["Wool produces heat.", "Wool is a good conductor.", "Wool reflects cold."], "Trapped air cannot move, so convection is reduced too."),
    ("Why is the heating element of an electric kettle at the bottom?", "Heated water rises and cooler water sinks, so convection currents heat all the water.", ["Heat only travels downwards.", "It is safer.", "The water is deepest there."], "Convection current."),
])
POOL5 = pool(R, [
    ("Why is an air-conditioner installed high up on a wall?", "The cool air is denser and sinks, setting up a convection current that cools the whole room.", ["Cool air rises.", "It is out of reach of children only.", "Radiation is stronger near the ceiling."], "Heaters are placed low for the same reason."),
    ("On a sunny day, why does a sea breeze blow from the sea to the land?", "The land heats up faster; air above it rises and cooler air from over the sea moves in to replace it.", ["The sea heats up faster.", "Water evaporates and pushes the air.", "The wind always blows from the sea."], "Land has a lower specific heat capacity than water."),
    ("At night, why does a land breeze blow from the land to the sea?", "The land cools faster, so warmer air over the sea rises and cool air from the land moves out to replace it.", ["The sea cools faster.", "The land heats up at night.", "Air stops moving at night."], "Convection currents reverse at night."),
    ("A metal chair and a wooden chair are in the same room. Why does the metal one feel colder?", "Metal conducts thermal energy away from your skin faster.", ["The metal is at a lower temperature.", "Wood produces heat.", "Metal absorbs cold."], "Both are at room temperature."),
    ("Why are cooking pots made of metal with plastic handles?", "Metal conducts heat to the food quickly; plastic is a poor conductor, so the handle stays cool.", ["Plastic conducts heat well.", "Metal is a poor conductor.", "Both reduce convection."], "Choose conductors and insulators for the job."),
    ("Why does a double-glazed window reduce heat transfer?", "The air (or vacuum) gap between the panes is a poor conductor.", ["The glass is thicker.", "Two panes reflect all light.", "The gap allows convection to cool the room."], "A narrow gap also limits convection."),
    ("A student heats one end of rods of copper, aluminium, iron and glass with wax at the other end. On which rod does the wax melt first?", "copper", ["glass", "iron", "aluminium"], "Copper is the best conductor of these."),
    ("Why does a greenhouse stay warm inside?", "Short-wavelength radiation passes in through the glass, but the longer-wavelength infrared emitted inside is mostly trapped.", ["Glass produces heat.", "Cold air cannot enter through glass.", "The plants give out heat by convection."], "A car in the sun heats up in the same way."),
    ("Why are the cooling fins of a motorcycle engine thin and many?", "They give a large surface area so the engine loses thermal energy faster.", ["They make the engine heavier.", "They reduce air flow.", "They store heat."], "More area: faster emission and convection."),
    ("A hot drink in a cup with a lid cools more slowly. Which process does the lid mainly reduce?", "convection and evaporation from the surface", ["radiation from the sides", "conduction through the base", "absorption of light"], "Hot air and vapour cannot rise away."),
])


def main():
    sets = U.sets([
        ("Conduction", [POOL1, (g_cond, 7), (sg_rods, 4), (sg_mat, 3), (g_way, 3)]),
        ("Convection", [POOL1, (g_way, 6), (sg_way, 5), (uk_way, 3)]),
        ("Radiation", [(g_rad, 7), (g_emit, 7), (g_way, 3), POOL1]),
        ("Uses: the vacuum flask and everyday examples", [(g_vf, 6), (POOL5, 7), (sg_mat, 3), (g_rad, 4)]),
        ("Exam-style questions", [(POOL5, 8), (g_way, 3), (sg_rods, 3), (g_emit, 3), (g_cond, 2), (g_vf, 1)]),
    ])
    make_ol(LV, SUBJ, "thermal-processes", SORT, "Thermal Processes",
            "Show understanding that thermal energy is transferred from a region of higher temperature to a region of lower temperature and that regions of equal "
            "temperature are in thermal equilibrium; describe, in molecular terms, how energy is transferred by conduction in solids (including by free electrons in "
            "metals) and by convection in fluids; describe radiation as transfer by infrared waves that needs no medium; describe the effect of surface colour and "
            "texture, surface temperature and surface area on the rate of emission and absorption of radiation; explain everyday applications such as the vacuum flask "
            "(summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Thermal Processes", "Thermal processes",
            "Free Secondary 3 O-Level Physics worksheets on thermal processes: thermal equilibrium, conduction, convection, radiation, good and bad emitters and absorbers, and "
            "the vacuum flask. 100 questions with answers.",
            "Thermal energy flows from hot to cold.", "Conduction (solids), convection (fluids), radiation (no medium).",
            "<p><b>Thermal energy always flows from a hotter region to a colder one until they reach thermal equilibrium.</b></p><ul>"
            "<li>Conduction: vibrating particles pass energy on; in metals, free electrons carry energy quickly. Air is a poor conductor.</li>"
            "<li>Convection: a heated fluid expands, becomes less dense and rises; cooler, denser fluid sinks, making a convection current.</li>"
            "<li>Radiation: infrared waves, no medium needed. Dull black surfaces are good absorbers and emitters; shiny surfaces are poor ones. Hotter and larger surfaces emit faster.</li></ul>",
            [("Where should a heater be placed in a room?", ["warm air rises", "cool air sinks to replace it"], "near the floor"),
             ("Which loses heat fastest by radiation: a shiny or a dull black kettle?", ["dull black is a better emitter"], "the dull black kettle")],
            ["Saying 'cold flows in'. Thermal energy flows out from the hotter object.", "Saying heat rises. The hot fluid rises because it is less dense.",
             "Thinking radiation needs air. It travels through a vacuum.", "Calling shiny surfaces good emitters. They are poor emitters and good reflectors."],
            [("What are the three ways thermal energy is transferred?", "Conduction (through solids by particle collisions and free electrons), convection (by the movement of a heated fluid) and radiation (by infrared waves)."),
             ("Which surfaces are the best emitters and absorbers of radiation?", "Dull, black surfaces. Shiny, silvery or white surfaces are the poorest emitters and absorbers."),
             ("How does a vacuum flask keep drinks hot?", "The vacuum stops conduction and convection, the silvered walls reduce radiation, and the stopper reduces convection and evaporation.")],
            sets)


if __name__ == "__main__":
    main()
