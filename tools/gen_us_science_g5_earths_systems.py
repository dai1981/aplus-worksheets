# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Earth's Four Systems (5-ESS2-1)
  python tools/gen_us_science_g5_earths_systems.py
The geosphere (rock, soil, sediment), hydrosphere (water and ice), atmosphere (air) and
biosphere (living things) interact: the ocean shapes landforms, wind carries sand, plants take
in carbon dioxide, roots break rock, and a volcano sends ash into the air.
Wrong answers come from real mistakes: "clouds and rain are part of the atmosphere only",
"people are not part of the biosphere", "the systems work separately".
"""
from sci_common import Unit, item, bank, lesson, make, figure, svg_wrap, rect, circle, text, arrow, table, People, INK

U = Unit(50114)
R = U.R
P = People(R)
SPH = ["geosphere", "hydrosphere", "atmosphere", "biosphere"]
PARTS = {"geosphere": ["rocks", "soil", "sand", "a mountain", "lava from a volcano", "pebbles on a beach", "a canyon wall", "mud at the bottom of a lake"],
         "hydrosphere": ["the ocean", "a river", "a glacier", "groundwater", "a lake", "an iceberg", "rain falling", "sea ice"],
         "atmosphere": ["the air", "oxygen gas in the air", "wind", "carbon dioxide in the air", "the gases around Earth", "nitrogen gas in the air"],
         "biosphere": ["a tree", "a fish", "people", "bacteria in soil", "a coral reef", "a herd of deer", "mushrooms", "seaweed"]}
EVENTS = [("Waves wear away the rocks along a beach.", ("hydrosphere", "geosphere")), ("Wind blows sand into tall dunes.", ("atmosphere", "geosphere")),
          ("Plants take in carbon dioxide from the air.", ("biosphere", "atmosphere")), ("Tree roots grow into a crack and split a rock.", ("biosphere", "geosphere")),
          ("A volcano sends ash and gases into the sky.", ("geosphere", "atmosphere")), ("Water in the ocean evaporates into the air.", ("hydrosphere", "atmosphere")),
          ("A river carves a deep canyon over millions of years.", ("hydrosphere", "geosphere")), ("Earthworms dig through and mix the soil.", ("biosphere", "geosphere")),
          ("Salmon swim up a river to lay their eggs.", ("biosphere", "hydrosphere")), ("A glacier scrapes a valley into a U shape.", ("hydrosphere", "geosphere")),
          ("Hurricane winds push ocean water into huge waves.", ("atmosphere", "hydrosphere")), ("A deer drinks from a stream.", ("biosphere", "hydrosphere")),
          ("Animals breathe in oxygen from the air.", ("biosphere", "atmosphere")), ("Rain soaks into the ground and dissolves minerals from rock.", ("hydrosphere", "geosphere")),
          ("Beavers build a dam that floods a valley.", ("biosphere", "hydrosphere")), ("Ocean water warms the air above it.", ("hydrosphere", "atmosphere")),
          ("Lichens slowly break down the surface of a boulder.", ("biosphere", "geosphere")), ("Ice freezes in cracks and breaks rocks apart.", ("hydrosphere", "geosphere"))]


def pair(p):
    return "%s and %s" % p


def spheres_pic():
    W, H = 420, 230
    pos = {"atmosphere": (210, 40, "#dceefb"), "geosphere": (80, 190, "#efe2d2"), "hydrosphere": (340, 190, "#cfe3f5"), "biosphere": (210, 125, "#e3f1df")}
    s = []
    for k, (x, y, c) in pos.items():
        s.append(rect(x - 62, y - 18, 124, 36, c, INK, 1.5, 10) + text(x, y + 5, k, 14))
    for a, b in [("atmosphere", "geosphere"), ("atmosphere", "hydrosphere"), ("geosphere", "hydrosphere"), ("biosphere", "atmosphere"), ("biosphere", "geosphere"), ("biosphere", "hydrosphere")]:
        (x1, y1, _), (x2, y2, _) = pos[a], pos[b]
        import math
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        s.append(arrow(x1 + ux * 40, y1 + uy * 22, x2 - ux * 40, y2 - uy * 22, "#777777", 1.8, 8) + arrow(x2 - ux * 40, y2 - uy * 22, x1 + ux * 40, y1 + uy * 22, "#777777", 1.8, 8))
    return svg_wrap(W, H, "".join(s), "the four spheres of Earth interact with each other")


# ------------------------------------------------------------ makers
def g_part():
    sp = R.choice(SPH)
    x = R.choice(PARTS[sp])
    return item("%s is part of which Earth system?" % (x[0].upper() + x[1:]), sp, [z for z in SPH if z != sp],
                "%s belongs to the %s (%s)." % (x[0].upper() + x[1:], sp, {"geosphere": "rock, soil and sediment", "hydrosphere": "all of Earth's water and ice",
                                                                         "atmosphere": "the air around Earth", "biosphere": "all living things"}[sp]))


def g_which_part():
    sp = R.choice(SPH)
    x = R.choice(PARTS[sp])
    w = [R.choice(PARTS[z]) for z in SPH if z != sp]
    return item("Which is part of the <b>%s</b>?" % sp, x, w, "%s is part of the %s." % (x[0].upper() + x[1:], sp))


def g_event():
    e, p = R.choice(EVENTS)
    pairs = [(a, b) for i, a in enumerate(SPH) for b in SPH[i + 1:]]
    good = set(p)
    w = [pair(q) for q in pairs if set(q) != good]
    return item(e + " Which two Earth systems are interacting?", pair(p), R.sample(w, 3),
                "%s is the %s, and the other part is the %s." % ("One part", p[0], p[1]))


def g_event_rev():
    e, p = R.choice(EVENTS)
    others = [x for x, q in EVENTS if set(q) != set(p)]
    return item("Which event is an example of the %s and the %s interacting?" % p, e, R.sample(others, 3),
                e + " Here the %s and the %s affect each other." % p)


def g_dune():
    w = R.choice([10, 15, 20, 25, 30])
    y = R.choice([3, 4, 5, 6])
    return item("Wind moves a sand dune about %d meters each year. How far could it move in %d years?" % (w, y), "%d meters" % (w * y),
                ["%d meters" % (w + y), "%d meters" % w, "%d meters" % (w * y + w)],
                "%d × %d = %d meters. The atmosphere (wind) is changing the geosphere (sand)." % (w, y, w * y))


B1 = bank([
    ("What are Earth's four major systems?", "geosphere, hydrosphere, atmosphere and biosphere", ["land, sea, sky and space", "rocks, soil, sand and mud", "sun, moon, stars and planets"],
     "Scientists group Earth into rock, water, air and living things."),
    ("What does the geosphere include?", "rocks, soil, sediment and Earth's inside", ["all living things", "all the air", "only the ocean"],
     "“Geo” means Earth: the solid ground and below."),
    ("What does the hydrosphere include?", "all of Earth's water, including ice and groundwater", ["only the oceans", "only rain", "only living things in water"],
     "Oceans, lakes, rivers, ice, groundwater and even water vapor are part of the hydrosphere."),
    ("What does the atmosphere include?", "the layer of gases (air) around Earth", ["the oceans", "the rocks", "the plants and animals"],
     "The atmosphere is made of nitrogen, oxygen, carbon dioxide and other gases."),
    ("What does the biosphere include?", "all living things, including people", ["only plants", "only wild animals", "only the forests"],
     "Every living thing, from bacteria to whales and humans, is in the biosphere."),
    ("Do Earth's systems work on their own?", "No. They are always interacting and changing each other.", ["Yes, each one stays separate.", "Only the ocean and air interact.", "They interact only during storms."],
     "Water shapes rock, air carries water, living things change soil and air, and so on."),
    ("Where would you find all four systems at once?", "a beach with waves, sand, wind and seagulls", ["a sealed empty jar", "a block of ice in a freezer", "a rock in space"],
     "Sand (geo), waves (hydro), wind (atmo) and seagulls (bio) all meet at a beach."),
    ("Are people part of Earth's systems?", "Yes, people are part of the biosphere.", ["No, people are separate.", "People are part of the geosphere.", "People are part of the atmosphere."],
     "Humans are living things, so they belong to the biosphere."),
])
B5 = bank([
    ("A volcano erupts and its ash blocks sunlight for months. Which systems are affected?", "the geosphere, atmosphere and biosphere", ["only the geosphere", "only the hydrosphere", "none of them"],
     "Ash from the geosphere fills the atmosphere, and less sunlight affects plants and animals in the biosphere."),
    ("Ava pours water on a tray of sand set at a slant. The sand washes down. What does her model show?", "the hydrosphere changing the geosphere (erosion)", ["the atmosphere making rain", "plants growing", "a volcano erupting"],
     "Moving water carries sediment downhill, like a river shaping land."),
    ("Leo puts a plant in a sealed bag. Drops form inside. Which systems is his model showing?", "the biosphere giving water to the atmosphere", ["the geosphere making rocks", "the hydrosphere making soil", "nothing interacting"],
     "Plants release water vapor into the air, which then condenses into drops."),
    ("Why do farmers plant rows of trees as windbreaks?", "Trees (biosphere) slow the wind (atmosphere) so less soil (geosphere) blows away.", ["Trees make wind stronger.", "Trees add more sand.", "Trees stop rain."],
     "This is three systems interacting."),
    ("A model shows rain falling on a mountain, running into a river and flowing to the ocean. Which two systems does it mainly show?", "hydrosphere and geosphere", ["biosphere and atmosphere", "atmosphere only", "biosphere only"],
     "Water moves over and shapes the land."),
    ("Which change to the biosphere would most affect the atmosphere?", "cutting down a large forest", ["one bird building a nest", "a fish laying eggs", "a dog barking"],
     "Forests take in a lot of carbon dioxide and give off oxygen and water vapor."),
])


def body():
    rows = [["geosphere", "rock, soil, sand, mountains"], ["hydrosphere", "oceans, rivers, lakes, ice, groundwater"],
            ["atmosphere", "air: nitrogen, oxygen, carbon dioxide"], ["biosphere", "all living things, including people"]]
    think = ("<p>Scientists think of Earth as four connected systems:</p>" + table(["System", "What it includes"], rows)
             + "<p>The systems are always <b>interacting</b>. Ocean waves (hydrosphere) wear away rock (geosphere). Wind (atmosphere) piles up sand dunes. "
               "Plants (biosphere) take carbon dioxide from the air and their roots break rocks. A volcano sends ash into the air.</p>"
             + figure(spheres_pic(), "Each system can change every other system."))
    ex = [("A river carves a canyon. Which systems interact?", ["River water: hydrosphere.", "Rock of the canyon: geosphere."], "hydrosphere and geosphere"),
          ("Plants take in carbon dioxide. Which systems interact?", ["Plants: biosphere.", "Carbon dioxide in the air: atmosphere."], "biosphere and atmosphere")]
    mist = ["Putting rain or ice only in the atmosphere. All water and ice belong to the hydrosphere.",
            "Leaving people out of the biosphere.",
            "Thinking the systems work separately. A change in one affects the others."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The four systems", B1 + [(g_part, 6), (g_which_part, 6)]),
        ("Parts of each system", [(g_part, 10), (g_which_part, 10)]),
        ("Systems interacting", [(g_event, 14), (g_event_rev, 6)]),
        ("More interactions", [(g_event_rev, 12), (g_event, 4), (g_dune, 4)]),
        ("Models and examples", B5 + [g_event, g_event_rev, g_dune, g_part]),
    ])
    make("grade-5", "earths-systems", 14, "5-ESS2-1",
         "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or atmosphere interact.",
         "Earth's Four Systems",
         "Grade 5 Earth's Systems Worksheets: Geosphere, Hydrosphere, Atmosphere and Biosphere",
         "Earth's Systems",
         "Free Grade 5 science worksheets on Earth's systems (NGSS 5-ESS2-1): the geosphere, hydrosphere, atmosphere and biosphere and how they interact, with real examples like waves, wind, plants and volcanoes. 100 practice questions with answers.",
         "Earth's four systems are always changing each other.",
         "Geosphere = rock and soil, hydrosphere = water and ice, atmosphere = air, biosphere = living things. Waves, wind, plants and volcanoes link them.",
         body(),
         [("What are Earth's four spheres?", "The geosphere (rock and soil), hydrosphere (all water and ice), atmosphere (air) and biosphere (all living things, including people)."),
          ("What is an example of the hydrosphere and geosphere interacting?", "Ocean waves wear away rocks along a beach, or a river carves a canyon."),
          ("How does the biosphere affect the atmosphere?", "Plants take in carbon dioxide and give off oxygen and water vapor, and animals breathe in oxygen."),
          ("Are clouds part of the atmosphere or the hydrosphere?", "Clouds are made of water drops or ice, so the water in them is part of the hydrosphere, even though it floats in the atmosphere.")],
         sets)


if __name__ == "__main__":
    main()
