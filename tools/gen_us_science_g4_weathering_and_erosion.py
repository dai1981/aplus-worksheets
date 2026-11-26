# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Weathering and Erosion (4-ESS2-1)
  python tools/gen_us_science_g4_weathering_and_erosion.py
Weathering breaks rock into smaller pieces (water, ice, wind, plant roots, living things);
erosion moves the pieces (water, wind, ice, gravity); deposition drops them in a new place.
Evidence comes from observations and measurements: stream tables, slope tests, angle of slope,
amount of water, vegetation.
Assessment boundary: a single form of weathering or erosion at a time.
Wrong answers come from real mistakes: "weathering and erosion are the same", "erosion only happens
in storms", "plants cause more erosion".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, classifier, People

U = Unit(40113)
R = U.R
P = People(R)

POOLS = {"weathering": ["Ice freezes in a crack and splits a rock.", "Tree roots grow into a crack and break a rock apart.", "Rain slowly wears down a stone statue.",
                        "Wind blows sand that scratches and wears down a rock.", "Waves crash on a cliff and break off small pieces.", "A rock tumbling in a stream gets rounded and smooth.",
                        "Moss growing on a rock slowly breaks its surface.", "Hot days and cold nights crack a desert rock."],
         "erosion": ["A river carries sand and mud downstream.", "Wind blows sand off a beach into the dunes.", "A glacier drags rocks across a valley.",
                     "Rain washes soil down a hillside.", "Waves carry sand away from a beach.", "A landslide moves rocks down a mountain.",
                     "Water flowing down a street carries away loose dirt.", "Wind blows dry topsoil off a farm field."],
         "deposition": ["Sand is dropped where a river enters the ocean, forming a delta.", "Wind drops sand that piles into a dune.", "A glacier melts and leaves a pile of rocks behind.",
                        "Mud settles at the bottom of a calm pond.", "Waves drop sand on a beach, making it wider.", "A flood leaves a layer of mud on a field."]}
WHY = {"weathering": "Weathering breaks rock into smaller pieces.", "erosion": "Erosion moves pieces of rock and soil to a new place.",
       "deposition": "Deposition drops the moved pieces in a new place."}
c_which, _ = classifier(R, POOLS, "Which is an example of {k}?", "{x}", WHY)


def c_what():
    k = R.choice(sorted(POOLS))
    x = R.choice(POOLS[k])
    return item("%s Is this weathering, erosion or deposition?" % x, k, [c for c in sorted(POOLS) if c != k] + ["melting"], WHY[k])

AGENT = {"water": ["A river carves a deep canyon.", "Rain makes gullies on a dirt hill.", "Waves wear away a sea cliff."],
         "wind": ["Blowing sand shapes a desert rock into an arch.", "A dust storm carries soil far away.", "Sand dunes move across the desert."],
         "ice": ["Water freezes and widens cracks in a sidewalk.", "A glacier carves a U-shaped valley.", "Ice in a crack splits a boulder."],
         "plants": ["Tree roots lift and crack a sidewalk.", "Roots grow into cracks and split a rock.", "A small tree grows in a crack in a cliff and widens it."],
         "gravity": ["Rocks fall from a cliff and pile up at the bottom.", "A mudslide slides down a steep hill.", "Loose rocks roll down a mountainside."]}
a_which, a_what = classifier(R, AGENT, "Which is caused mainly by {k}?", "{x} What is the main cause?")


def g_slope():
    angles = sorted(R.sample([5, 10, 15, 20, 25, 30, 35], 3))
    soil = sorted(R.sample(range(20, 160, 5), 3))
    rows = [["%d°" % a, "%d g" % s] for a, s in zip(angles, soil)]
    p = P.next()
    tab = table(["Slope of the soil", "Soil washed away"], rows)
    k = R.choice(["most", "pattern", "keep"])
    if k == "most":
        return item(tab + "%s poured the same amount of water down soil at three slopes. Which slope lost the most soil?" % p[0], "%d°" % angles[2],
                    ["%d°" % angles[0], "%d°" % angles[1], "All lost the same amount."], "The steepest slope (%d°) lost %d g." % (angles[2], soil[2]))
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % p[0], "The steeper the slope, the more soil was eroded.",
                    ["The steeper the slope, the less soil was eroded.", "Slope does not change erosion.", "Only the gentlest slope eroded."],
                    "From %d° to %d°, the soil lost went from %d g to %d g. Water flows faster down steeper slopes." % (angles[0], angles[2], soil[0], soil[2]))
    return item(tab + "In %s's test, what must stay the same for a fair test?" % p[0], "the amount of water and the type of soil", ["the slope", "nothing", "the amount of soil lost"],
                "Only the slope should change.")


def g_plants():
    cover = ["bare soil", "grass", "small bushes"]
    vals = sorted(R.sample(range(15, 150, 5), 3), reverse=True)
    rows = [[c, "%d g" % v] for c, v in zip(cover, vals)]
    order = list(range(3))
    R.shuffle(order)
    labels = [cover[i] for i in order]
    ch = bar_chart(labels, [vals[i] for i in order], "grams", "bar graph of soil washed away", ymax=160, step=40, w=290)
    p = P.next()
    k = R.choice(["least", "why"])
    if k == "least":
        best = cover[2]
        return item(fig(ch) + "%s sprinkled the same amount of water on three trays of soil. Which tray lost the least soil?" % p[0], best,
                    [c for c in cover if c != best] + ["They all lost the same amount."], "The tray with %s lost only %d g." % (best, vals[2]))
    return item(fig(ch) + "Why did the trays with plants lose less soil in %s's test?" % p[0], "Plant roots hold the soil in place.",
                ["Plants make the water heavier.", "Plants cause more erosion.", "Plants turn soil into rock."], "Roots act like a net that holds soil.")


def g_water():
    amts = sorted(R.sample([100, 200, 300, 400, 500, 600], 3))
    depth = sorted(R.sample(range(1, 15), 3))
    rows = [["%d mL" % a, "%d cm" % d] for a, d in zip(amts, depth)]
    p = P.next()
    return item(table(["Water poured in stream table", "Depth of the channel"], rows) + "In %s's stream table, what happened when more water flowed?" % p[0],
                "The channel became deeper because more sand was eroded.", ["The channel became shallower.", "No sand moved.", "The sand turned into rock."],
                "With %d mL the channel was %d cm deep; with %d mL it was %d cm deep." % (amts[0], depth[0], amts[2], depth[2]))


B1 = bank([
    ("What is weathering?", "the breaking of rock into smaller pieces", ["the moving of rock pieces to a new place", "the dropping of sand in a new place", "the melting of rock"],
     "Weathering breaks; erosion moves."),
    ("What is erosion?", "the moving of rock pieces and soil to a new place", ["the breaking of rock into smaller pieces", "the forming of new rock", "the growth of plants"],
     "Water, wind, ice and gravity cause erosion."),
    ("What is deposition?", "the dropping of moved rock and soil in a new place", ["the breaking of rock", "the moving of soil uphill", "the cooling of lava"],
     "Deltas and sand dunes form by deposition."),
    ("Which happens first?", "Weathering breaks the rock.", ["Erosion carries the rock away.", "Deposition drops the rock.", "They all happen at the same time always."],
     "Rock must be broken before the pieces can be carried."),
    ("How does ice weather rock?", "Water freezes in cracks, expands and pushes the rock apart.", ["Ice melts the rock.", "Ice glues rocks together.", "Ice makes rock heavier."],
     "Water gets bigger when it freezes."),
    ("Which force pulls rocks and soil downhill in a landslide?", "gravity", ["magnetism", "light", "sound"], "Gravity pulls everything down."),
    ("Which slows erosion on a hillside?", "plants with roots that hold the soil", ["removing all the plants", "making the hill steeper", "pouring more water on it"],
     "Roots hold soil in place."),
    ("Why are rocks in a river usually smooth and round?", "Water and other rocks wore down their sharp edges.", ["They were made round.", "Fish polished them.", "The sun melted them."],
     "Weathering by moving water smooths rocks over time."),
])
B5 = bank([
    ("Ava wants to test how wind erodes sand. Which tool helps her make wind?", "a fan", ["a thermometer", "a magnet", "a balance"], "She can change the fan speed and measure how far the sand moves."),
    ("Leo puts chalk pieces in a jar of water and shakes it for 5 minutes. The chalk becomes smaller and rounder. What does this model?", "weathering of rocks in a river", ["deposition in a lake", "a volcano", "rock layers forming"],
     "Shaking models rocks bumping in moving water."),
    ("A town wants to stop a hill from eroding onto a road. Which solution would help most?", "plant grass and build a retaining wall", ["cut down the trees on the hill", "pour water on the hill", "make the hill steeper"],
     "Plants and walls hold soil in place."),
    ("Why do farmers plant rows of trees along the edges of fields?", "to block wind and reduce wind erosion", ["to make more wind", "to dry the soil", "to cause landslides"],
     "Windbreaks slow the wind."),
    ("Mia sees a pile of sand where a stream enters a lake. What happened there?", "deposition", ["weathering", "melting", "freezing"], "The water slowed down and dropped the sand."),
    ("Which measurement shows how fast a beach is eroding?", "the width of the beach each year", ["the color of the sand", "the temperature of the water", "the number of shells"],
     "If the beach gets narrower each year, sand is being eroded."),
])


def body():
    think = ("<p><b>Weathering</b> breaks rock into smaller pieces. Water, ice, wind, plant roots and changing temperatures can weather rock.</p>"
             "<p><b>Erosion</b> moves the pieces of rock and soil to a new place. Water, wind, ice and gravity cause erosion. "
             "<b>Deposition</b> drops the pieces in a new place.</p>"
             "<p>We can test erosion with models: water flows faster down a <b>steeper slope</b> and carries away more soil; "
             "more water cuts deeper channels; <b>plant roots</b> hold soil and slow erosion.</p>")
    ex = [("Ice splits a rock. Is this weathering or erosion?", ["The rock breaks.", "Nothing is carried away yet."], "weathering"),
          ("A river carries sand downstream. Is this weathering or erosion?", ["The sand is moved."], "erosion")]
    mist = ["Mixing up weathering (breaking) and erosion (moving).",
            "Thinking plants cause more erosion. Roots hold soil in place.",
            "Thinking erosion happens only in big storms. It also happens slowly every day."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Weathering, erosion and deposition", B1 + [(c_which, 6), (c_what, 6)]),
        ("Breaking or moving?", [(c_what, 12), (c_which, 8)]),
        ("Causes of weathering and erosion", [(a_which, 10), (a_what, 10)]),
        ("Erosion investigations", [(g_slope, 8), (g_plants, 7), (g_water, 5)]),
        ("Testing and solving erosion problems", B5 + [g_slope, g_plants, g_water, c_what]),
    ])
    make("grade-4", "weathering-and-erosion", 13, "4-ESS2-1",
         "Make observations and/or measurements to provide evidence of the effects of weathering or the rate of erosion by water, ice, wind, or vegetation.",
         "Weathering and Erosion",
         "Grade 4 Weathering and Erosion Worksheets: Water, Wind, Ice and Plants",
         "Weathering and Erosion",
         "Free Grade 4 science worksheets on weathering and erosion (NGSS 4-ESS2-1): breaking vs. moving rock, deposition, causes like water, wind, ice, plants and gravity, and erosion investigations with data. 100 practice questions with answers.",
         "Weathering breaks rock. Erosion moves it.",
         "Water, wind, ice, plants and gravity change Earth's surface. Deposition drops the pieces in a new place.",
         body(),
         [("What is the difference between weathering and erosion?", "Weathering breaks rock into smaller pieces. Erosion moves those pieces to a new place."),
          ("What causes erosion?", "Moving water, wind, ice (glaciers) and gravity carry rock and soil to new places."),
          ("How do plants help stop erosion?", "Plant roots hold soil in place, so less soil is washed or blown away.")],
         sets)


if __name__ == "__main__":
    main()
