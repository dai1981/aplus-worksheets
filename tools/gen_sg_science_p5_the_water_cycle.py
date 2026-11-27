# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: The water cycle (Cycles)
  python tools/gen_sg_science_p5_the_water_cycle.py
Water evaporates from seas, rivers and reservoirs and from plants, rises as water vapour, cools and condenses into tiny water
droplets that form clouds, and falls as rain; it flows back into reservoirs, rivers and the sea. The water cycle keeps
fresh water available. Water is important to living things; Singapore's Four National Taps (local catchment water,
imported water, NEWater, desalinated water), water pollution and ways to save water.
UK Year 4 water cycle questions are reused with Singapore names (no snow or hail).
Wrong answers come from real mistakes: "clouds are made of water vapour", "the Sun boils the sea",
"water is used up and disappears", "only the sea gives water vapour".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63504)
R = U.R
P = People(R)
WC = use(U, "gen_uk_science_y4_the_water_cycle", drop=["winter", "snow", "hail", "hills", "glacier"])

STAGES = [("evaporation", "Heat from the Sun makes water from seas, rivers, reservoirs and plants change into water vapour."),
          ("condensation", "The water vapour rises, cools and condenses into tiny water droplets that form clouds."),
          ("rain (precipitation)", "The water droplets join to form bigger drops that fall as rain."),
          ("collection", "Rainwater flows into drains, canals, rivers, reservoirs and the sea.")]


def g_stage():
    i = R.randrange(4)
    k = R.choice(["name", "desc", "next"])
    if not once(("sg", i, k)):
        return None
    n, d = STAGES[i]
    if k == "name":
        return item("Which part of the water cycle is this?<br><i>%s</i>" % d, n, [x for x, _ in STAGES if x != n], d)
    if k == "desc":
        return item("What happens during %s in the water cycle?" % n, d, [y for x, y in STAGES if x != n], d)
    j = (i + 1) % 4
    return item("In the water cycle, what comes after %s?" % n, STAGES[j][0], [x for x, _ in STAGES if x not in (n, STAGES[j][0])] + ["melting"], "evaporation → condensation → rain → collection → evaporation …")


SCENES = [("Water in Bedok Reservoir slowly turns into water vapour on a hot afternoon.", "evaporation"),
          ("Dark clouds gather over Pulau Ubin before a storm.", "condensation"), ("Heavy rain falls during the monsoon season.", "rain (precipitation)"),
          ("Rainwater flows along the drains and canals into Marina Reservoir.", "collection"), ("Water vapour escapes from the leaves of trees in the Botanic Gardens.", "evaporation"),
          ("Water vapour rises high into the cooler air and forms clouds.", "condensation"), ("Rain runs off rooftops into the drains.", "collection"),
          ("The sea along East Coast Park gives off water vapour in the hot sun.", "evaporation")]


def g_scene():
    s, a = R.choice(SCENES)
    if not once(("sc", s)):
        return None
    return item("%s Which part of the water cycle is this?" % s, a, [x for x, _ in STAGES if x != a], "evaporation → condensation → rain → collection.")


TAPS = [("water collected from rain in reservoirs", "local catchment water"), ("water bought from Johor, Malaysia", "imported water"),
        ("used water cleaned with advanced membranes and ultraviolet light", "NEWater"), ("seawater treated to remove the salt", "desalinated water")]


def g_tap():
    d, a = R.choice(TAPS)
    k = R.choice(["name", "desc"])
    if not once(("tp", a, k)):
        return None
    if k == "name":
        return item("Which of Singapore's Four National Taps is %s?" % d, a, [x for _, x in TAPS if x != a], "Singapore gets water from four sources: local catchment water, imported water, NEWater and desalinated water.")
    return item("What is %s?" % a, d, [x for x, y in TAPS if y != a], "These are Singapore's Four National Taps.")


SAVE = ["taking shorter showers", "turning off the tap while brushing teeth", "using a cup to rinse the mouth", "fixing leaking taps",
        "washing clothes only when there is a full load", "using a pail instead of a hose to wash the car", "watering plants with water used to wash rice"]
WASTE = ["leaving the tap running while soaping hands", "using a hose to wash the car for a long time", "washing a few clothes in a full machine",
         "taking a long bath every day", "letting a leaking tap drip", "thawing frozen food under a running tap"]


def g_save():
    k = R.choice(["save", "waste"])
    a = R.choice(SAVE if k == "save" else WASTE)
    if not once(("sv", a)):
        return None
    if k == "save":
        return item("Which of these is a way to save water?", a, R.sample(WASTE, 3), "Saving water means using only what we need.")
    return item("Which of these wastes water?", a, R.sample(SAVE, 3), "Water is precious; every drop counts.")


def g_rain():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    mm = [R.randrange(100, 300, 10) for _ in months]
    if len(set(mm)) < 6:
        return None
    k = R.choice(["most", "least", "diff", "total"])
    if not once(("rn", k), 2):
        return None
    tb = table(["Month"] + months, [["Rainfall (mm)"] + [str(x) for x in mm]])
    q0 = "The table shows the rainfall at a weather station in Singapore.<br>%s" % tb
    s = sorted(zip(mm, months))
    if k == "most":
        return item(q0 + "Which month had the most rainfall?", s[-1][1], [m for _, m in s[:3]], "Look for the largest number.")
    if k == "least":
        return item(q0 + "Which month had the least rainfall?", s[0][1], [m for _, m in s[-3:]], "Look for the smallest number.")
    if k == "diff":
        d = s[-1][0] - s[0][0]
        return item(q0 + "How much more rain fell in the wettest month than in the driest month?", "%d mm" % d, ["%d mm" % s[-1][0], "%d mm" % (s[-1][0] + s[0][0]), "%d mm" % (d + 20)],
                    "%d − %d = %d mm." % (s[-1][0], s[0][0], d))
    t = sum(mm[:3])
    return item(q0 + "What was the total rainfall from Jan to Mar?", "%d mm" % t, ["%d mm" % (t + 50), "%d mm" % sum(mm), "%d mm" % (t - 30)], "%s = %d mm." % (" + ".join(str(x) for x in mm[:3]), t))


B1 = bank([
    ("What provides the heat that drives the water cycle?", "the Sun", ["the Moon", "the wind only", "the clouds"], "Heat from the Sun causes evaporation."),
    ("What are clouds made of?", "tiny water droplets", ["water vapour, which is invisible", "smoke", "cotton"], "Water vapour condenses into droplets to form clouds."),
    ("Why does water vapour condense high up in the sky?", "The air there is cooler, so the water vapour loses heat.", ["The air there is hotter.", "The Sun is closer.", "The wind makes it heavy."], "Condensation involves heat loss."),
    ("Why is the water cycle important?", "It keeps fresh water available for living things.", ["It makes the sea saltier.", "It uses up all the water.", "It stops rain from falling."], "Water is recycled again and again."),
    ("Is the total amount of water on Earth used up?", "No. It goes round and round in the water cycle.", ["Yes, it is used up every year.", "Yes, it disappears into space.", "Only rainwater is used up."], "Water changes state and moves, but is not destroyed."),
    ("Which two changes of state take place in the water cycle?", "evaporation and condensation", ["melting and freezing", "boiling and melting", "freezing and boiling"], "Water evaporates, then condenses into clouds."),
    ("Why does rain fall from clouds?", "Tiny droplets join to form drops that are too heavy to stay up.", ["Clouds become too hot.", "The wind pushes the rain down.", "The Sun melts the clouds."], "Bigger drops fall as rain."),
    ("Do plants take part in the water cycle?", "Yes. Water vapour escapes from their leaves.", ["No, only the sea does.", "No, plants keep all their water.", "Only dead plants do."], "Plants give off water vapour through tiny openings in their leaves."),
])
B2 = bank([
    ("Why do living things need water?", "All living things need water to survive and carry out life processes.", ["Only plants need water.", "Only animals need water.", "Water is needed only for washing."], "Water is needed for digestion, transport and photosynthesis."),
    ("Why does Singapore need to save water?", "It has limited land to collect and store rainwater.", ["It never rains in Singapore.", "Water is free.", "Singapore has big rivers and lakes."], "Singapore depends on all four national taps."),
    ("What is NEWater?", "used water that is treated to make it clean enough to reuse", ["seawater with salt", "rainwater from the roof", "water from Johor"], "It is cleaned using advanced membranes and ultraviolet light."),
    ("Which of these causes water pollution?", "throwing rubbish into drains", ["planting trees near reservoirs", "collecting rainwater", "fixing a leaking tap"], "Drains lead to canals and reservoirs."),
    ("How can water pollution harm living things?", "Fish and other water animals may die.", ["It makes the water cleaner.", "It makes plants grow faster.", "It has no effect."], "Polluted water may have harmful substances."),
    ("Why are reservoirs connected to drains and canals in Singapore?", "to collect as much rainwater as possible", ["to make floods worse", "to send water to the sea", "to keep the water salty"], "Two-thirds of Singapore's land area is water catchment."),
])
B3 = bank([
    ("A glass of water is left on a sunny windowsill for a week. The water level drops. Where has the water gone?", "It has evaporated into the air as water vapour.", ["It has soaked into the glass.", "It has been destroyed.", "It has turned into ice."], "The water will become part of the water cycle."),
    ("Why does a plastic sheet placed over a hole in the sand collect water on its underside on a sunny day?", "Water evaporates from the sand and condenses on the cooler sheet.", ["The plastic makes water.", "Rain falls through the sheet.", "The sand melts."], "This is a model of the water cycle."),
    ("In a model of the water cycle, a bowl of hot water is covered with cling film and ice is put on top. What does the ice do?", "It cools the cling film so water vapour condenses on it.", ["It heats the water.", "It makes rain fall faster.", "It stops evaporation."], "The cold film is like the cool air high up."),
    ("In the same model, what do the drops falling back into the bowl represent?", "rain", ["evaporation", "clouds", "the Sun"], "Water droplets join and fall back."),
    ("Why is it important to keep reservoirs clean?", "Reservoir water is treated and used as drinking water.", ["Dirty water evaporates faster.", "Reservoirs are only for fish.", "Dirty water makes more rain."], "Pollution makes water harder and more costly to treat."),
])
B5 = bank([
    ("Siti put 200 ml of water in a covered and an uncovered beaker in the same sunny place. After a week, which had more water left?", "the covered beaker", ["the uncovered beaker", "both the same", "neither had any water"], "The cover stopped the water vapour from escaping."),
    ("Water droplets formed on the inside of the cover. What processes took place?", "evaporation, then condensation", ["condensation, then evaporation", "melting, then freezing", "boiling, then freezing"], "Water evaporated and condensed on the cooler cover."),
    ("Ravi's family used 600 litres of water in a week. They cut their use by 120 litres the next week. How much did they use the next week?", "480 litres", ["720 litres", "120 litres", "500 litres"], "600 − 120 = 480 litres."),
    ("A shower uses about 9 litres of water a minute. How much water is saved by cutting a shower from 10 minutes to 5 minutes?", "45 litres", ["90 litres", "50 litres", "5 litres"], "5 minutes × 9 litres = 45 litres."),
    ("A pupil left identical bowls of water in an open field and under a shelter. The water in the open field evaporated faster. Which factor most likely caused this?", "more sunlight and wind in the open field", ["the colour of the bowls", "the amount of water", "the shape of the bowls"], "Temperature and wind speed up evaporation."),
])


def body():
    think = ("<p><b>Water moves round and round between the land, the sea and the sky. This is the water cycle.</b></p>"
             "<ul><li><b>Evaporation</b>: heat from the Sun turns water from seas, reservoirs and plants into water vapour.</li>"
             "<li><b>Condensation</b>: the water vapour rises, cools and condenses into tiny droplets that form clouds.</li>"
             "<li><b>Rain</b>: droplets join into bigger drops that fall.</li>"
             "<li><b>Collection</b>: water flows into drains, canals, reservoirs and the sea, and the cycle continues.</li></ul>"
             "<p>Singapore gets water from its Four National Taps: local catchment water, imported water, NEWater and desalinated water.</p>")
    ex = [("Puddles dry up after rain. Where does the water go?", ["The water gains heat from the Sun", "It evaporates into water vapour"], "Into the air."),
          ("Why do clouds form high in the sky?", ["The air is cooler higher up", "Water vapour loses heat and condenses"], "Water vapour condenses into droplets.")]
    mist = ["Thinking clouds are made of water vapour. They are tiny water droplets.",
            "Thinking the Sun boils the sea. Water evaporates at the surface without boiling.",
            "Thinking water is used up. It goes round in the water cycle.",
            "Forgetting that plants give off water vapour too."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stages of the water cycle", B1 + [(g_stage, 8), (WC.g_name, 2), (WC.g_next, 2)]),
        ("The water cycle around us", WC.B1 + [(g_scene, 7), (g_stage, 4), (WC.g_eve, 4), (WC.g_next, 2)]),
        ("Water in Singapore", B2 + [(g_tap, 7), (g_save, 7)]),
        ("Models of the water cycle", B3 + [(g_save, 5), (g_rain, 4), (g_scene, 2), (g_stage, 2), (WC.g_eve, 2)]),
        ("PSLE-style questions", B5 + WC.B5 + [(g_rain, 4), (WC.g_dish, 4), (WC.g_dry, 4)]),
    ])
    make_sg(5, "the-water-cycle", 4, "Cycles", "Cycles in matter and water (Water cycle)",
            "Describe the water cycle: evaporation, condensation and rain, driven by heat from the Sun, and show how the water cycle keeps water available. "
            "Recognise the importance of water to life, the effects of water pollution and the need to conserve water, including Singapore's water sources "
            "(summary of the MOE Primary Science Syllabus).",
            "The Water Cycle",
            "Primary 5 Science: The Water Cycle Worksheets (with Answers)",
            "Water cycle",
            "Free Primary 5 science worksheets for Singapore pupils on the water cycle: evaporation, condensation, clouds and rain, the Four National Taps, water pollution and saving water. 100 questions with answers.",
            "Water goes round between the land, sea and sky.",
            "Evaporation, condensation, rain and collection.",
            body(),
            [("What are clouds made of?", "Tiny water droplets. Water vapour rises, cools and condenses into droplets, which gather as clouds."),
             ("What are Singapore's Four National Taps?", "Local catchment water, imported water, NEWater and desalinated water."),
             ("Is water used up?", "No. Water changes state and moves around in the water cycle, so the same water is used again and again.")],
            sets)


if __name__ == "__main__":
    main()
