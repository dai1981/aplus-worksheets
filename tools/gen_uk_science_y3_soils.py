# -*- coding: utf-8 -*-
"""
UK Year 3 science: Soils (Rocks)
  python tools/gen_uk_science_y3_soils.py
Soils are made from rocks and organic matter: what is in soil (rock particles, humus, air, water, living things),
sandy, clay and loam soils and their properties, soil layers (topsoil, subsoil, bedrock), the soil-and-water jar,
the drainage test with results to read, and earthworms.
Wrong answers come from real mistakes: "soil is just dirt", "all soils are the same", "humus is a kind of rock",
"clay soil drains fastest".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61309)
R = U.R
P = People(R)

IN = ["tiny pieces of rock", "humus (rotting plants and animals)", "air", "water", "living things such as worms", "small stones", "sand", "dead leaves"]
NOTIN = ["plastic bottles", "sugar", "glass beads", "metal coins", "chocolate", "paper clips"]


def g_made():
    k = R.random() < 0.6
    if k:
        a = R.choice(IN)
        w = R.sample(NOTIN, 3)
        if not once(("mi", a), 2):
            return None
        o = sorted([a] + w)
        return item("Which of these is a natural part of soil: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Soil is made of rock pieces, humus, air, water and living things.")
    a = R.choice(NOTIN)
    w = R.sample(IN, 3)
    if not once(("mn", a)):
        return None
    o = sorted([a] + w)
    return item("Which of these is NOT a natural part of soil: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Soil is made of rock pieces, humus, air, water and living things.")


TYPE = [("sandy soil", "feels gritty and lets water drain through quickly"), ("clay soil", "feels sticky when wet and holds lots of water"),
        ("loam", "is a good mixture of sand, clay and humus that most plants like"), ("sandy soil", "dries out quickly in summer"),
        ("clay soil", "can be moulded into a sausage shape when wet"), ("clay soil", "becomes hard and cracked when it dries"),
        ("loam", "is dark, crumbly and full of humus"), ("sandy soil", "has large grains with big air gaps between them"),
        ("clay soil", "has tiny grains packed tightly together"), ("loam", "holds some water but still drains well"),
        ("chalky soil", "is pale and stony and has white lumps in it"), ("peaty soil", "is very dark and made mostly of rotted plants")]
TN = ["sandy soil", "clay soil", "loam", "chalky soil", "peaty soil"]


def g_type():
    t, d = R.choice(TYPE)
    if not once(("ty", d)):
        return None
    w = R.sample([x for x in TN if x != t], 3)
    return item("Which type of soil %s?" % d, t, w, "Sandy soil drains fast; clay soil holds water; loam is a mixture most plants like.")


DR = {"sandy soil": 80, "loam": 55, "clay soil": 15, "gravel": 95, "peaty soil": 40}


def g_drain():
    who = P.next()[0]
    ss = R.sample(sorted(DR), 4)
    v = [DR[x] + R.choice([-5, 0, 5]) for x in ss]
    k = R.choice(["most", "least", "read", "diff", "plant", "fair"])
    ri = R.randrange(4)
    if not once(("dr", tuple(ss), tuple(v), k)) or (k == "fair" and not once(("df",), 3)):
        return None
    tab = table(["Soil", "Water that drained through in 5 minutes (ml)"], [[a, str(b)] for a, b in zip(ss, v)])
    intro = tab + "%s poured 100 ml of water onto each soil in a funnel. " % who
    if k == "most":
        a = ss[v.index(max(v))]
        return item(intro + "Which soil let water drain through the fastest?", a, [x for x in ss if x != a], "The most water came through it.")
    if k == "least":
        a = ss[v.index(min(v))]
        return item(intro + "Which soil held on to the most water?", a, [x for x in ss if x != a], "The least water came through, so most stayed in the soil.")
    if k == "read":
        g = "%d ml" % v[ri]
        return item(intro + "How much water drained through the %s?" % ss[ri], g, uniq(g, ["%d ml" % x for x in v] + ["%d ml" % (100 - v[ri])]), "Read the row.")
    if k == "diff":
        g = "%d ml" % (100 - v[ri])
        return item(intro + "How much of the 100 ml stayed in the %s?" % ss[ri], g, uniq(g, ["%d ml" % v[ri], "100 ml", "%d ml" % (100 - v[ri] + 10), "0 ml"]), "100 − %d = %d ml." % (v[ri], 100 - v[ri]))
    if k == "plant":
        wet = ss[v.index(min(v))]
        return item(intro + "A plant that likes wet soil should be planted in which of these soils?", wet, [x for x in ss if x != wet], "It keeps the most water.")
    return item(intro + "Why must the same amount of each soil and water be used?", "so the only thing that changes is the type of soil", ["to make it quicker", "so the funnels match the jugs", "it does not matter"], "Fair test.")


JAR = [("the bottom", "small stones and gravel"), ("just above the stones", "sand"), ("near the top of the sediment", "fine clay and silt"), ("floating on the water", "bits of humus such as dead leaves")]


def g_jar():
    where, what = R.choice(JAR)
    k = R.random() < 0.5
    if not once(("ja", where, k)):
        return None
    intro = "Soil is shaken in a jar of water and left to settle for a day. "
    if k:
        return item(intro + "What will be found at %s?" % where, what, [x[1] for x in JAR if x[1] != what], "Heavy pieces sink first; light humus floats.")
    return item(intro + "Where will the %s end up?" % what, where, [x[0] for x in JAR if x[0] != where], "Heavy pieces sink first; light humus floats.")


LAY = [("topsoil", "the top layer, dark and full of humus, roots and living things"), ("subsoil", "the middle layer, paler, with more stones and less humus"),
       ("bedrock", "the solid rock deep underneath")]


def g_lay():
    l, d = R.choice(LAY)
    k = R.random() < 0.5
    if not once(("la", l, k)):
        return None
    if k:
        return item("Which layer of the ground is %s?" % d, l, [x[0] for x in LAY if x[0] != l] + ["the sky"], "Topsoil on top, then subsoil, then bedrock.")
    return item("What is %s?" % l, d, [x[1] for x in LAY if x[1] != d] + ["a layer of plastic under the grass"], "Topsoil on top, then subsoil, then bedrock.")


WORM = [("How do earthworms help soil?", "They mix it and make tunnels that let in air and water.", ["They make it sticky.", "They turn it into rock.", "They take all the water out."]),
        ("What do earthworms eat?", "dead leaves and plant material in the soil", ["stones", "live birds", "plastic"]),
        ("What do earthworms leave behind that is good for plants?", "worm casts full of nutrients", ["glass", "sand only", "nothing at all"]),
        ("Why are worms important to gardeners?", "They help make soil healthy for plants.", ["They eat all the plants.", "They make soil harder.", "They are not important."]),
        ("Where do earthworms like to live?", "in damp soil", ["in dry sand in the sun", "in water bottles", "in the air"]),
        ("What happens to dead leaves on the ground over time?", "They rot and become humus in the soil.", ["They turn into rocks.", "They grow back on the tree.", "They stay the same for ever."])]


def g_worm():
    q, a, w = R.choice(WORM)
    if not once(("wo", q)):
        return None
    return item(q, a, w, "Living things help turn dead material into rich soil.")


B1 = bank([
    ("What is soil made from?", "tiny pieces of rock mixed with humus, air, water and living things", ["only sand", "melted plastic", "only dead leaves"], "Rocks plus organic matter."),
    ("Where do the rock pieces in soil come from?", "Rocks are slowly broken into tiny pieces by weather, water and plant roots.", ["They fall from space.", "People grind them every day.", "They grow from seeds."], "Weathering."),
    ("What is humus?", "rotted remains of dead plants and animals in soil", ["a kind of rock", "a type of worm", "a dip made from chickpeas"], "It makes soil dark and rich."),
    ("Why is humus good for plants?", "It adds nutrients and helps soil hold water.", ["It makes soil too hard.", "It kills roots.", "It stops plants growing."], "Organic matter."),
    ("Is soil the same everywhere?", "No. Soils have different rocks and amounts of humus.", ["Yes, all soil is the same.", "Yes, it is always sand.", "Only in the UK."], "Many kinds."),
    ("What does organic matter mean?", "material that came from living things", ["material made of metal", "material made in factories", "rock that has melted"], "Leaves, roots, dead animals."),
    ("How long does it take to make a few centimetres of new soil?", "hundreds of years", ["a few minutes", "one day", "a week"], "Soil forms very slowly."),
    ("Which tool would help you see the grains in soil?", "a magnifying glass", ["a thermometer", "a stopwatch", "a magnet"], "Look closely."),
])
B5 = bank([
    ("Why do gardeners add compost to clay soil?", "It breaks up the clay so water and air can move through.", ["It makes the clay stickier.", "It turns clay into rock.", "It stops plants growing."], "Improve the soil."),
    ("Why might plants in sandy soil need watering more often?", "Water drains through sandy soil quickly.", ["Sandy soil holds lots of water.", "Sand is poisonous.", "Sand blocks the light."], "Drainage."),
    ("Why should we look after soil?", "Most of our food grows in it, and it takes a very long time to form.", ["Soil is not useful.", "Soil grows back in a day.", "Only worms need soil."], "A precious resource."),
    ("A puddle stays on a field for days after rain. What kind of soil is the field likely to have?", "clay soil", ["sandy soil", "gravel", "no soil at all"], "Clay drains slowly."),
    ("How could you test which soil holds the most water fairly?", "Use the same amount of each soil and pour the same amount of water through each.", ["Use different amounts of each soil.", "Pour water quickly on one and slowly on another.", "Test only one soil."], "Fair test."),
])


def body():
    think = ("<p><b>Soil is made from tiny pieces of rock mixed with organic matter.</b></p>"
             "<ul><li>Soil also has air, water and living things such as worms. Humus is rotted plant and animal material.</li>"
             "<li>Sandy soil drains quickly; clay soil holds water; loam is a good mixture for most plants.</li>"
             "<li>Topsoil is on top, then subsoil, then solid bedrock.</li></ul>")
    ex = [("Water drains fastest through?", ["Big grains, big gaps"], "sandy soil"),
          ("What is humus?", ["From living things"], "rotted plants and animals")]
    mist = ["Thinking soil is just dirt with nothing in it.", "Thinking all soils are the same.", "Thinking clay soil drains fastest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is in soil?", B1 + [(g_made, 8), (g_worm, 4)]),
        ("Types of soil", [(g_type, 12), (g_made, 4), (g_lay, 4)]),
        ("Soil layers and worms", [(g_lay, 2), (g_jar, 8), (g_worm, 2), (g_drain, 8)]),
        ("Drainage test", [(g_drain, 20)]),
        ("Looking after soil", B5 + [(g_drain, 12), (g_made, 3)]),
    ])
    make_uk(3, "soils", 9, "Rocks",
            "Recognise that soils are made from rocks and organic matter.",
            "Soils",
            "Year 3 Science: Soils Worksheets (Rocks, Humus, Sandy and Clay Soil)",
            "Soils",
            "Free Year 3 science worksheets on soils: what soil is made of, humus, sandy, clay and loam soils, soil layers, earthworms and the drainage test. 100 questions with answers.",
            "Rock pieces plus organic matter.",
            "Sandy soil drains fast; clay soil holds water.",
            body(),
            [("What is soil made of?", "Tiny pieces of rock mixed with humus (rotted plants and animals), air, water and living things such as worms."),
             ("What is the difference between sandy and clay soil?", "Sandy soil has big grains, so water drains through quickly. Clay soil has tiny grains packed together, so it holds water and feels sticky."),
             ("Why are earthworms good for soil?", "They mix the soil, make tunnels for air and water, and break down dead leaves into nutrients for plants.")],
            sets)


if __name__ == "__main__":
    main()
