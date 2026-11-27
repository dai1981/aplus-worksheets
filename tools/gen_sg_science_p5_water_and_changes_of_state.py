# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Water and changes of state (Cycles)
  python tools/gen_sg_science_p5_water_and_changes_of_state.py
Water exists as ice, water and water vapour. Melting (0 °C) and boiling (100 °C) need heat gain; freezing and
condensation involve heat loss; evaporation happens at any temperature, only at the surface, and is faster with higher
temperature, more wind, a larger exposed surface area and lower humidity. Condensation forms water droplets on cold surfaces.
UK Year 4 changes-of-state questions are reused with Singapore names; Singapore examples and evaporation tables are written here.
Wrong answers come from real mistakes: "the water on a cold can leaked through it", "evaporation needs 100 °C",
"steam you can see is water vapour", "ice melts at 100 °C", "boiling and evaporation are the same".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63503)
R = U.R
P = People(R)
CS = use(U, "gen_uk_science_y4_changes_of_state", rep=[(r"\bhob\b", "stove")], drop=["winter", "snow", "salt", "icy road", "newton"])
WC = use(U, "gen_uk_science_y4_the_water_cycle", drop=["winter", "snow", "hail", "hills"])

CHG = {"melting": ("solid", "liquid", "gain"), "freezing": ("liquid", "solid", "loss"), "boiling": ("liquid", "gas", "gain"),
       "evaporation": ("liquid", "gas", "gain"), "condensation": ("gas", "liquid", "loss")}
EX = [("An ice kachang melts in the hot sun.", "melting"), ("Water in an ice-cube tray turns into ice in the freezer.", "freezing"),
      ("Water droplets form on the outside of a cold can of drink.", "condensation"), ("Wet clothes dry on a bamboo pole.", "evaporation"),
      ("Bubbles form all through the water in a kettle at 100 °C.", "boiling"), ("Puddles on a school field disappear after the rain stops.", "evaporation"),
      ("The bathroom mirror becomes misty after a hot shower.", "condensation"), ("Chocolate in a pocket becomes soft and runny.", "melting"),
      ("Molten candle wax drips and becomes hard.", "freezing"), ("Water droplets form on the inside of the lid of a pot of soup.", "condensation"),
      ("Sweat on your skin dries on a breezy day.", "evaporation"), ("Spectacles mist up when you walk out of an air-conditioned room.", "condensation"),
      ("A wet floor dries after it is mopped.", "evaporation")]


def g_ex():
    s, a = R.choice(EX)
    if not once(("ex", s)):
        return None
    w = [x for x in CHG if x != a]
    if a == "evaporation":
        w = ["boiling"] + [x for x in w if x != "boiling"][:2]
    elif a == "boiling":
        w = ["evaporation"] + [x for x in w if x != "evaporation"][:2]
    else:
        w = R.sample(w, 3)
    return item("%s Which process is this?" % s, a, w, "%s: %s → %s (heat %s)." % (a.capitalize(), CHG[a][0], CHG[a][1], CHG[a][2]))


def g_heat():
    p = R.choice(sorted(CHG))
    k = R.choice(["gain", "states"])
    if not once(("ht", p, k)):
        return None
    if k == "gain":
        g = CHG[p][2]
        return item("During %s, does water gain heat or lose heat?" % p, "It %s heat." % ("gains" if g == "gain" else "loses"),
                    ["It %s heat." % ("loses" if g == "gain" else "gains"), "Neither: heat does not matter.", "It gains heat and loses heat equally."],
                    "%s: %s → %s." % (p.capitalize(), CHG[p][0], CHG[p][1]))
    a = "from a %s to a %s" % (CHG[p][0], CHG[p][1])
    w = ["from a %s to a %s" % (x, y) for x, y in [("solid", "liquid"), ("liquid", "solid"), ("liquid", "gas"), ("gas", "liquid"), ("solid", "gas")] if "from a %s to a %s" % (x, y) != a]
    return item("What change of state happens during %s?" % p, a, R.sample(w, 3), "%s changes water %s." % (p.capitalize(), a))


def g_evap():
    fac = R.choice(["temp", "wind", "area", "humid"])
    setups = {"temp": (["in an air-conditioned room", "in a shady corridor", "on a sunny windowsill"], "the temperature of the surroundings", "The higher the temperature, the faster the water evaporates."),
              "wind": (["in still air", "near a fan on low speed", "near a fan on high speed"], "the amount of wind", "The windier it is, the faster the water evaporates."),
              "area": (["in a narrow cup", "in a bowl", "in a wide plate"], "the exposed surface area", "The larger the exposed surface area, the faster the water evaporates."),
              "humid": (["in a closed bathroom after a shower", "in a classroom", "in a dry, air-conditioned office"], "the amount of water vapour in the air (humidity)", "The drier the air, the faster the water evaporates.")}
    places, var, e = setups[fac]
    lost = sorted(R.sample(range(5, 60), 3))
    k = R.choice(["most", "least", "var", "same"])
    if not once(("ev", fac, k)):
        return None
    tb = table(["Where the water was", "Water lost after 1 day (ml)"], [[p, str(l)] for p, l in zip(places, lost)])
    q0 = "%s put 100 ml of water in containers and left them in different places.<br>%s" % (P.next()[0], tb)
    if k == "most":
        return item(q0 + "Where did the water evaporate the fastest?", places[2], places[:2] + ["it was the same everywhere"], e)
    if k == "least":
        return item(q0 + "Where did the water evaporate the slowest?", places[0], places[1:] + ["it was the same everywhere"], e)
    if k == "var":
        others = [v for f, (_, v, _) in setups.items() if f != fac]
        return item(q0 + "Which factor affecting evaporation was being tested?", var, others, e)
    return item(q0 + "Why was 100 ml of water used each time?", "to make the test fair", ["to make the water evaporate faster", "to keep the water cold", "to stop the water from boiling"],
                "Only the factor being tested should change.")


def g_bvse():
    rows = [("Which happens only at 100 °C for pure water?", "boiling", ["evaporation", "condensation", "melting"], "Evaporation can happen at any temperature."),
            ("Which happens only at the surface of the water?", "evaporation", ["boiling", "freezing", "melting"], "Boiling happens throughout the water, with bubbles."),
            ("Which can happen at room temperature?", "evaporation", ["boiling", "freezing at room temperature", "melting of ice at −5 °C"], "Puddles dry without boiling."),
            ("Which happens throughout the liquid, with bubbles forming inside?", "boiling", ["evaporation", "condensation", "freezing"], "Evaporation is only at the surface."),
            ("Which needs a large amount of heat quickly from a heat source such as a stove?", "boiling", ["evaporation", "condensation", "freezing"], "Evaporation is slow and can use heat from the surroundings.")]
    i = R.randrange(len(rows))
    if not once(("bv", i)):
        return None
    return item(*rows[i])


def g_cond():
    k = R.choice(range(6))
    if not once(("cd", k)):
        return None
    rows = [("Water droplets form on the outside of a glass of iced water. Where did the water come from?", "water vapour in the air that condensed on the cold glass",
             ["water leaking through the glass", "the ice melting through the glass", "the table"], "Water vapour loses heat to the cold glass and condenses."),
            ("Why do water droplets form on the outside of a cold can but not a can at room temperature?", "The cold can makes water vapour lose heat and condense.",
             ["The cold can leaks.", "Room-temperature cans are waterproof.", "Cold cans make water."], "Condensation needs a cold surface."),
            ("Why does a bathroom mirror mist up after a hot shower?", "Warm water vapour condenses on the cooler mirror.", ["The mirror melts.", "Steam leaks from the mirror.", "The mirror evaporates."],
             "The mirror is cooler than the water vapour."),
            ("What is the white 'steam' we see above a boiling kettle?", "tiny water droplets formed when water vapour cools", ["water vapour, which is invisible", "smoke", "air"],
             "Water vapour is invisible; the white mist is condensed droplets."),
            ("Why do spectacles mist up when you walk from an air-conditioned room into the hot air outside?", "Water vapour in the warm air condenses on the cold lenses.",
             ["The lenses evaporate.", "The lenses become hot.", "The air-conditioned air leaks out."], "The lenses are colder than the outside air."),
            ("Water droplets appear on the inside of a lunch box lid. What happened?", "Water vapour from the warm food condensed on the cooler lid.",
             ["The lid leaked.", "The food froze.", "The lid melted."], "Water vapour loses heat to the lid.")]
    return item(*rows[k])


B1 = bank([
    ("In which three states can water exist?", "ice (solid), water (liquid) and water vapour (gas)", ["ice, steam and clouds only", "solid, liquid and air", "water, juice and milk"], "Water is the same substance in all three states."),
    ("At what temperature does pure ice melt?", "0 °C", ["100 °C", "37 °C", "10 °C"], "Pure water melts and freezes at 0 °C."),
    ("At what temperature does pure water boil?", "100 °C", ["0 °C", "50 °C", "37 °C"], "At boiling point, water changes into water vapour quickly."),
    ("What is the freezing point of pure water?", "0 °C", ["100 °C", "−100 °C", "20 °C"], "The freezing point and melting point are the same temperature."),
    ("What is water vapour?", "water in the gas state, which is invisible", ["a white cloud", "tiny drops of water", "smoke"], "We cannot see water vapour."),
    ("What happens to the temperature of ice while it is melting?", "It stays at 0 °C until all the ice has melted.", ["It rises quickly.", "It falls.", "It goes to 100 °C."], "The heat gained is used to change the state."),
])
B2 = bank([
    ("Which processes involve heat gain?", "melting, boiling and evaporation", ["freezing and condensation", "melting and freezing", "condensation and evaporation"], "Heat is needed to change a solid to a liquid or a liquid to a gas."),
    ("Which processes involve heat loss?", "freezing and condensation", ["melting and boiling", "evaporation and boiling", "melting and evaporation"], "Heat is lost when a gas becomes a liquid or a liquid becomes a solid."),
    ("Why do we feel cool after swimming on a windy day?", "Water on our skin evaporates and takes heat from our body.", ["Wind is always cold.", "Water gives us cold.", "The pool is frozen."], "Evaporation causes cooling."),
    ("Why does sweating help to cool the body?", "Sweat evaporates and takes heat away from the skin.", ["Sweat is cold.", "Sweat freezes on the skin.", "Sweat stops heat from leaving."], "The body loses heat as the sweat evaporates."),
    ("Why does a puddle dry up faster on a hot day?", "Water evaporates faster at higher temperatures.", ["The puddle boils.", "The puddle freezes.", "The water sinks into the air."], "Temperature affects the rate of evaporation."),
    ("Why do clothes dry faster when they are spread out than when folded?", "A larger surface area is exposed to the air.", ["Spread clothes are hotter.", "Folded clothes have more water.", "Folding stops the wind."], "Exposed surface area affects the rate of evaporation."),
])
B3 = bank([
    ("Which shows the correct order when ice is heated until it boils?", "ice → water → water vapour", ["water vapour → water → ice", "ice → water vapour → water", "water → ice → water vapour"], "Melting first, then boiling."),
    ("Why is food in a covered pot slow to dry out?", "Water vapour condenses on the lid and drips back.", ["The lid makes the food colder.", "The lid boils the water.", "Covered food has no water."], "The water vapour cannot escape."),
    ("Why do wet clothes dry slowly on a rainy day?", "The air already has a lot of water vapour.", ["There is no sunlight at all.", "Rain makes clothes heavier.", "Clothes cannot evaporate."], "Humid air slows down evaporation."),
    ("Water is left in an open dish in a classroom at 30 °C. Will it evaporate?", "Yes, slowly, even though it is below 100 °C.", ["No, it must reach 100 °C.", "No, it must freeze first.", "Only at night."], "Evaporation happens at any temperature."),
    ("Why does a glass of iced water become wet on the outside on a humid day in Singapore?", "There is a lot of water vapour in the air to condense on the cold glass.", ["The glass leaks more on humid days.", "Humid air is cold.", "The ice evaporates out of the glass."], "Singapore's air is often humid."),
])
B5 = bank([
    ("Siti heated ice and recorded the temperature every minute. The temperature stayed at 0 °C for 4 minutes. What was happening?", "The ice was melting.", ["The water was boiling.", "The water was freezing.", "The thermometer was broken."], "The temperature stays at 0 °C while ice melts."),
    ("Ravi heated water. The temperature rose to 100 °C and then stayed the same. Why?", "The water was boiling and the heat was used to change it into water vapour.", ["The water stopped gaining heat.", "The water was freezing.", "The water became ice."], "The temperature stays at 100 °C while water boils."),
    ("Mei Ling put the same amount of water in a cup and a plate in the same place. The plate dried first. What was she testing?", "how the exposed surface area affects the rate of evaporation", ["how temperature affects evaporation", "how wind affects evaporation", "how heavy water is"], "Only the container shape was different."),
    ("Why should the containers be left for the same length of time?", "so that the test is fair", ["so that the water boils", "so that the water freezes", "to make the water cooler"], "Time is a variable to keep the same."),
    ("A pupil put a cold metal tray above a kettle of boiling water. Water dripped from the tray. Which processes happened?", "boiling, then condensation", ["melting, then freezing", "condensation, then boiling", "freezing, then evaporation"], "The water boiled into water vapour, which condensed on the cold tray."),
])


def body():
    think = ("<p><b>Water can change from one state to another when it gains or loses heat.</b></p>"
             "<ul><li>Heat gain: <b>melting</b> (ice → water, at 0 °C), <b>boiling</b> (water → water vapour, at 100 °C), <b>evaporation</b> (water → water vapour, at any temperature).</li>"
             "<li>Heat loss: <b>freezing</b> (water → ice, at 0 °C), <b>condensation</b> (water vapour → water, on cold surfaces).</li>"
             "<li>Evaporation is faster when it is hotter, windier, drier and when more surface is exposed.</li></ul>")
    ex = [("Droplets form on a cold can. Where did the water come from?", ["Water vapour in the air touches the cold can", "It loses heat and condenses"], "From the air."),
          ("Wet clothes dry faster on a windy day. Why?", ["Wind carries water vapour away", "More water can evaporate"], "Wind speeds up evaporation.")]
    mist = ["Thinking the water on a cold can leaked through it. It condensed from the air.",
            "Thinking evaporation needs 100 °C. It happens at any temperature.",
            "Calling the white mist above a kettle 'water vapour'. Water vapour is invisible; the mist is tiny droplets.",
            "Mixing up boiling and evaporation. Boiling happens throughout the liquid at 100 °C; evaporation is only at the surface."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Three states of water", B1 + [(g_heat, 6), (CS.g_word, 4), (CS.g_temp, 4)]),
        ("Gaining and losing heat", B2 + [(g_ex, 8), (g_heat, 4), (CS.g_ex, 2)]),
        ("Evaporation and condensation", B3 + [(g_cond, 6), (g_bvse, 5), (g_ex, 4)]),
        ("Factors affecting evaporation", CS.B1 + [(g_evap, 8), (WC.g_dish, 4), (CS.g_mp, 3), (g_cond, 2)]),
        ("PSLE-style experiments", B5 + [(g_evap, 6), (CS.g_heat, 4), (WC.g_dry, 3), (WC.g_dish, 2)]),
    ])
    make_sg(5, "water-and-changes-of-state", 3, "Cycles", "Cycles in matter and water (Water: changes of state)",
            "Recognise that water can exist in three states and that it changes from one state to another when it gains or loses heat: melting, freezing, "
            "boiling, evaporation and condensation. Investigate the factors that affect the rate of evaporation: temperature, wind, exposed surface area and "
            "humidity (summary of the MOE Primary Science Syllabus).",
            "Water and Changes of State",
            "Primary 5 Science: Water and Changes of State Worksheets (with Answers)",
            "Changes of state",
            "Free Primary 5 science worksheets for Singapore pupils on water and changes of state: melting, freezing, boiling, evaporation, condensation and factors affecting evaporation. 100 questions with answers.",
            "Water changes state when it gains or loses heat.",
            "Melting, freezing, boiling, evaporation, condensation.",
            body(),
            [("What is the difference between evaporation and boiling?", "Evaporation happens at any temperature, only at the surface of the water. Boiling happens at 100 °C throughout the water, with bubbles."),
             ("Why do water droplets form on a cold glass?", "Water vapour in the air loses heat to the cold glass and condenses into water droplets."),
             ("What makes water evaporate faster?", "A higher temperature, more wind, a larger exposed surface area and drier air (lower humidity).")],
            sets)


if __name__ == "__main__":
    main()
