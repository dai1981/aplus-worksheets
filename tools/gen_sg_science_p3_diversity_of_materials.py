# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Diversity of materials (Diversity)
  python tools/gen_sg_science_p3_diversity_of_materials.py
Common materials (wood, metal, plastic, glass, ceramic, rubber, fabric) and their properties:
strength, flexibility, waterproof, transparency, ability to float or sink, hardness. Uses depend on properties.
UK Year 2 and Year 5 material questions are reused with Singapore names (no magnets or conductors here: those come later);
fair-test tables (float or sink, strength, bending, absorbing water) are written here.
Wrong answers come from real mistakes: "heavy things always sink", "metal is flexible so it is good for an umbrella frame only",
"glass is chosen because it is strong", "a material that bends easily is weak".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63303)
R = U.R
P = People(R)
DROP = ["magnet", "conduct", "solub", "dissolv", "insulat", "winter", "snow", "thermal"]
PM = use(U, "gen_uk_science_y5_properties_of_materials", drop=DROP)
EM = use(U, "gen_uk_science_y2_uses_of_everyday_materials", drop=DROP)

MATS = {"wood": dict(strong=1, flex=0, wp=0, clear=0, floats=1), "metal": dict(strong=1, flex=None, wp=1, clear=0, floats=0),
        "plastic": dict(strong=1, flex=1, wp=1, clear=1, floats=1), "glass": dict(strong=0, flex=0, wp=1, clear=1, floats=0),
        "ceramic": dict(strong=1, flex=0, wp=1, clear=0, floats=0), "rubber": dict(strong=1, flex=1, wp=1, clear=0, floats=1),
        "cotton fabric": dict(strong=0, flex=1, wp=0, clear=0, floats=None)}
USES = [("a window pane", "glass", "it lets light through (it is transparent)", ["wood", "cotton fabric", "ceramic"]),
        ("a raincoat", "plastic", "it is waterproof and flexible", ["cotton fabric", "glass", "wood"]),
        ("the soles of school shoes", "rubber", "it is flexible, waterproof and not slippery", ["glass", "ceramic", "cotton fabric"]),
        ("a dinner plate", "ceramic", "it is hard, strong and waterproof", ["cotton fabric", "rubber", "paper"]),
        ("a towel", "cotton fabric", "it absorbs water", ["plastic", "glass", "metal"]),
        ("a cooking pot", "metal", "it is strong and does not melt on the stove", ["plastic", "glass", "cotton fabric"]),
        ("a cricket bat", "wood", "it is hard and strong", ["glass", "cotton fabric", "rubber"]),
        ("a rubber band", "rubber", "it stretches and goes back to its shape", ["glass", "wood", "ceramic"]),
        ("a pencil", "wood", "it is strong and easy to sharpen", ["glass", "rubber", "metal"]),
        ("a water bottle for a toddler", "plastic", "it is waterproof, light and does not break easily", ["glass", "cotton fabric", "wood"]),
        ("the cover of a playground slide", "plastic", "it is smooth, waterproof and strong", ["glass", "cotton fabric", "paper"]),
        ("the strings of a badminton racket", "a synthetic fibre such as nylon", "it is strong and flexible", ["glass", "ceramic", "wood"])]


def g_use():
    thing, a, why, w = R.choice(USES)
    if not once(("us", thing)):
        return None
    k = R.choice(["mat", "why"])
    if k == "mat":
        return item("Which material is best for %s?" % thing, a, w, "%s is used because %s." % (a[0].upper() + a[1:], why))
    other = ["it is the most colourful", "it is the heaviest", "it can be seen in the dark"]
    return item("%s is often used for %s. Why?" % (a[0].upper() + a[1:], thing), "because " + why, ["because " + o for o in other],
                "A material is chosen for its properties.")


PROPQ = [("flex", "Which material is NOT flexible (does not bend easily)?", "Which material is flexible (bends easily without breaking)?"),
         ("wp", "Which material is NOT waterproof?", "Which material is waterproof?"), ("clear", "Which material is NOT transparent?", "Which material can be transparent (lets most light through)?"),
         ("floats", "Which material sinks in water?", "Which material floats in water?")]


def g_prop():
    p, qno, qyes = R.choice(PROPQ)
    yes = sorted(m for m in MATS if MATS[m][p] == 1)
    no = sorted(m for m in MATS if MATS[m][p] == 0)
    k = R.choice(["yes", "no"])
    if k == "yes":
        if len(no) < 3:
            return None
        a = R.choice(yes)
        w = R.sample(no, 3)
        q = qyes
    else:
        if len(yes) < 3:
            return None
        a = R.choice(no)
        w = R.sample(yes, 3)
        q = qno
    if not once(("pr", p, k, a)):
        return None
    return item(q, a, w, "Each material has its own properties. Think about how %s behaves." % a)


def g_float():
    objs = [("a wooden block", 1), ("a metal key", 0), ("a plastic bottle cap", 1), ("a glass marble", 0), ("a rubber duck", 1), ("a ceramic tile", 0),
            ("a cork", 1), ("an iron nail", 0), ("a ping-pong ball", 1), ("a stone", 0), ("a sponge", 1), ("a steel spoon", 0)]
    pick = R.sample(objs, 5)
    if sum(f for _, f in pick) in (0, 5):
        return None
    k = R.choice(["float", "sink", "count", "concl"])
    if not once(("fl", k, tuple(sorted(n for n, _ in pick)))):
        return None
    if not once(("flk", k), 1 if k == "concl" else 3):
        return None
    tb = table(["Object", "Floats or sinks?"], [[n, "floats" if f else "sinks"] for n, f in pick])
    q0 = "%s put five objects in a tank of water.<br>%s" % (P.next()[0], tb)
    fl = [n for n, f in pick if f]
    sk = [n for n, f in pick if not f]
    if k == "float":
        if len(sk) < 3:
            return None
        return item(q0 + "Which object floats?", R.choice(fl), R.sample(sk, 3), "Wood, cork, rubber and many plastics float.")
    if k == "sink":
        if len(fl) < 3:
            return None
        return item(q0 + "Which object sinks?", R.choice(sk), R.sample(fl, 3), "Metal, glass, stone and ceramic sink.")
    if k == "count":
        n = len(fl)
        return item(q0 + "How many objects floated?", str(n), [str(x) for x in range(6) if x != n][:3], "Count the objects marked 'floats'.")
    return item(q0 + "Which material would be best for a toy boat?", "plastic, because it floats and is waterproof",
                ["glass, because it is transparent", "metal, because it is heavy", "cotton fabric, because it absorbs water"], "A boat must float and not let water in.")


def g_strength():
    rng = {"nylon": (25, 30), "plastic sheet": (15, 20), "cotton fabric": (10, 14), "rubber sheet": (6, 9), "aluminium foil": (3, 5), "paper": (1, 2)}
    mats = R.sample(sorted(rng), 4)
    loads = [R.randint(*rng[m]) for m in mats]
    k = R.choice(["strong", "weak", "var", "fair", "order"])
    if not once(("st", k), 1 if k in ("var", "fair") else 3):
        return None
    tb = table(["Strip of material", "Mass held before it tore (kg)"], [[m, str(l)] for m, l in zip(mats, loads)])
    q0 = "%s hung masses on strips of four materials of the same size until each strip tore.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(loads, mats))
    if k == "strong":
        return item(q0 + "Which material is the strongest?", s[-1][1], [m for _, m in s[:-1]], "It held the greatest mass before tearing.")
    if k == "weak":
        return item(q0 + "Which material is the weakest?", s[0][1], [m for _, m in s[1:]], "It held the smallest mass before tearing.")
    if k == "var":
        return item(q0 + "What did she change in this test?", "the type of material", ["the size of the strips", "the place she did the test", "the way she hung the masses"],
                    "Only the material was changed.")
    if k == "fair":
        return item(q0 + "Why were the strips the same size?", "so that the test was fair", ["so that they tore faster", "so that they were easier to colour", "so that she needed fewer masses"],
                    "A wider strip would hold more mass, so the size must be kept the same.")
    return item(q0 + "Which shows the materials from weakest to strongest?", ", ".join(m for _, m in s),
                [", ".join(m for _, m in s[::-1]), ", ".join(mats), ", ".join([s[1][1], s[0][1], s[3][1], s[2][1]])], "Order the masses from smallest to largest.")


def g_absorb():
    rng = {"sponge": (5, 15), "paper towel": (25, 35), "felt": (40, 50), "cotton cloth": (55, 65), "newspaper": (70, 80), "plastic sheet": (95, 100), "aluminium foil": (95, 100)}
    mats = R.sample(sorted(rng), 4)
    if "plastic sheet" in mats and "aluminium foil" in mats:
        return None
    left = [R.randint(*rng[m]) for m in mats]
    k = R.choice(["most", "least", "use", "wp"])
    if not once(("ab", k), 4):
        return None
    tb = table(["Material", "Water left in the dish after 1 minute (ml)"], [[m, str(l)] for m, l in zip(mats, left)])
    q0 = "%s placed four pieces of material of the same size in 100 ml of water, then took them out.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(left, mats))
    if k == "most":
        return item(q0 + "Which material absorbed the most water?", s[0][1], [m for _, m in s[1:]], "The least water was left, so it took in the most.")
    if k == "least":
        return item(q0 + "Which material absorbed the least water?", s[-1][1], [m for _, m in s[:-1]], "The most water was left, so it took in the least.")
    if k == "use":
        return item(q0 + "Which material would be best for wiping up spilt drinks?", s[0][1], [m for _, m in s[1:]], "Choose the material that absorbs the most water.")
    return item(q0 + "Which material would be best for a lunch box cover?", s[-1][1], [m for _, m in s[:-1]], "A cover should keep water out, so it should absorb the least.")


B1 = bank([
    ("What is a material?", "what an object is made of", ["the colour of an object", "the shape of an object", "the size of an object"], "A chair may be made of wood, metal or plastic."),
    ("What does waterproof mean?", "does not let water through", ["breaks in water", "floats in water", "lets light through"], "Raincoats are waterproof."),
    ("What does flexible mean?", "can bend without breaking", ["is very hard", "is see-through", "is very heavy"], "Rubber and plastic can be flexible."),
    ("What does transparent mean?", "lets most light through so we can see clearly through it", ["blocks all light", "is very strong", "can bend"], "Clear glass is transparent."),
    ("Which material can be found in nature without being made in a factory?", "wood", ["plastic", "glass", "nylon"], "Wood comes from trees. Plastic and glass are made by people."),
    ("Which of these objects is made of ceramic?", "a teacup", ["a raincoat", "a rubber band", "a cotton T-shirt"], "Cups, plates and tiles are often ceramic."),
    ("Which property of glass makes it easy to break?", "It is not flexible and shatters when hit hard.", ["It is waterproof.", "It is transparent.", "It is smooth."], "Glass is hard but brittle."),
    ("Which material is used to make most tyres?", "rubber", ["glass", "wood", "ceramic"], "Rubber is strong, flexible and waterproof."),
])
B2 = bank([
    ("Why is a metal spoon NOT a good choice for a baby's teething toy?", "It is hard and could hurt the baby.", ["It is waterproof.", "It is shiny.", "It floats."], "A teething toy is usually soft rubber or plastic."),
    ("Why are umbrellas made of nylon fabric instead of cotton fabric?", "Nylon is waterproof; cotton absorbs water.", ["Cotton is heavier than metal.", "Nylon is transparent.", "Cotton is too strong."], "An umbrella must keep the rain out."),
    ("A plastic ruler can bend a little. A wooden ruler cannot. Which property is different?", "flexibility", ["transparency", "colour", "smell"], "Flexibility is how easily a material bends."),
    ("Why are school bags often made of strong fabric with a plastic coating?", "The fabric is strong and the coating makes it waterproof.", ["The coating makes it transparent.", "The fabric absorbs rain.", "The coating makes it heavier."], "Two materials can be used together."),
    ("Which object is made of more than one material?", "a pencil (wood and graphite)", ["a glass marble", "a rubber band", "a ceramic tile"], "Many objects use two or more materials."),
    ("Why is wood used for the handles of some cooking pots?", "It does not get as hot as metal.", ["It is transparent.", "It is flexible.", "It is waterproof."], "Wood heats up slowly, so the handle is safer to hold."),
    ("A pupil says heavy objects always sink. Which is the best example to show she is wrong?", "A large wooden log floats.", ["A small stone sinks.", "A metal key sinks.", "A glass marble sinks."], "Whether something floats depends on its material, not only its mass."),
    ("Which material would make the best curtain to block out light?", "thick dark fabric", ["clear glass", "clear plastic", "thin tissue paper"], "Thick fabric blocks most light."),
])
B3 = bank([
    ("Why are aquarium walls made of glass or clear plastic?", "They are transparent and waterproof.", ["They are flexible.", "They absorb water.", "They are soft."], "We need to see the fish, and the water must stay in."),
    ("Why should a slide in a playground NOT be made of glass?", "Glass can break and cut children.", ["Glass is too soft.", "Glass absorbs water.", "Glass is flexible."], "A slide must be strong and safe."),
    ("Why are the soles of running shoes made of rubber?", "Rubber grips the ground and is flexible.", ["Rubber is transparent.", "Rubber absorbs water.", "Rubber is hard and brittle."], "Rubber soles do not slip easily."),
    ("Which material would be best for a mat in a wet bathroom?", "rubber", ["paper", "cotton wool", "glass"], "A bath mat should be waterproof and not slippery."),
    ("A cup must hold hot soup without melting or leaking. Which material is best?", "ceramic", ["paper", "cotton fabric", "thin plastic film"], "Ceramic is hard, waterproof and does not melt."),
    ("Why are tents made of waterproof fabric?", "to keep rain out", ["to let light in", "to make the tent heavier", "to make it float"], "Campers need to stay dry."),
    ("Why is steel used to build bridges?", "It is very strong.", ["It is transparent.", "It is flexible like rubber.", "It floats."], "Bridges must carry heavy loads."),
])
B5 = bank([
    ("Rui En wants to find out which material is the most waterproof. Which should she keep the same?", "the size of each piece of material and the amount of water dripped on it", ["the type of material", "the colour of the material only", "nothing"], "Change only the material."),
    ("In a bending test, which result shows the most flexible material?", "It bent the most without breaking.", ["It broke first.", "It did not bend at all.", "It was the heaviest."], "Flexible materials bend without breaking."),
    ("Why should the test for floating be done in the same tank of water for every object?", "to make the test fair", ["to make the objects sink", "to make the water warmer", "to save time only"], "Only the object should change."),
    ("Jun Jie needs a material for a bookmark that will not tear when it gets wet. Which test should he do?", "dip strips in water and pull them to see which tears first", ["see which strips float", "shine a torch through each strip", "weigh each strip"], "The test must match what he wants to find out."),
    ("Which result would show that a material is transparent?", "A torch shone through it lights up the wall clearly behind it.", ["It floats in water.", "It bends easily.", "It does not tear."], "Transparent materials let most light through."),
    ("A pupil dripped 10 drops of water onto each of four fabrics. Fabric P let no water through. What can she conclude?", "Fabric P is waterproof.", ["Fabric P is flexible.", "Fabric P is transparent.", "Fabric P is the weakest."], "No water passing through means waterproof."),
])


def body():
    think = ("<p><b>Objects are made of materials. We choose a material because of its properties.</b></p>"
             "<ul><li>Common materials: wood, metal, plastic, glass, ceramic, rubber and fabric.</li>"
             "<li>Properties: <b>strength</b>, <b>flexibility</b>, <b>waterproof</b>, <b>transparency</b>, <b>hardness</b> and the ability to <b>float or sink</b>.</li>"
             "<li>To compare materials fairly, change only the material and keep everything else the same.</li></ul>")
    ex = [("Why is a raincoat made of plastic?", ["It must keep rain out", "Plastic is waterproof and flexible"], "Because plastic is waterproof and flexible."),
          ("A strip of nylon held 20 kg and a strip of paper held 2 kg. Which is stronger?", ["Compare the masses held", "20 kg is more than 2 kg"], "Nylon.")]
    mist = ["Thinking heavy things always sink. A big log floats; a small key sinks.",
            "Mixing up strong and hard. Glass is hard but breaks easily.",
            "Changing two things at once in a test (for example the material and the size of the strip).",
            "Choosing a material because it looks nice instead of because of its properties."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Materials around us", B1 + [(EM.g_mat, 5), (g_prop, 4), (EM.g_many, 3)]),
        ("Properties and uses", B2 + [(g_use, 5), (EM.g_why, 4), (g_prop, 3)]),
        ("Choosing the right material", B3 + [(g_use, 4), (EM.g_bad, 4), (PM.g_prop, 3), (EM.g_why, 2)]),
        ("Testing materials", [(g_float, 5), (g_strength, 4), (g_absorb, 4), (PM.g_scratch, 3), (EM.g_test, 3), (g_prop, 2)]),
        ("PSLE-style investigations", B5 + [(g_strength, 4), (g_absorb, 3), (g_float, 3), (EM.g_test, 2), (PM.g_scratch, 2)]),
    ])
    make_sg(3, "diversity-of-materials", 3, "Diversity", "Diversity of materials",
            "Identify common materials (wood, metal, plastic, glass, ceramic, rubber, fabric) and relate their uses to their properties: "
            "strength, flexibility, waterproof, transparency, hardness and the ability to float or sink. Carry out fair tests to compare materials "
            "(summary of the MOE Primary Science Syllabus).",
            "Diversity of Materials",
            "Primary 3 Science: Diversity of Materials Worksheets (with Answers)",
            "Diversity of materials",
            "Free Primary 3 science worksheets for Singapore pupils on materials and their properties: strength, flexibility, waterproof, transparency, floating and sinking, with fair-test tables. 100 questions with answers.",
            "We choose materials for their properties.",
            "Strength, flexibility, waterproof, transparency and floating.",
            body(),
            [("What are the properties of materials in Primary 3?", "Strength, flexibility, hardness, waterproof, transparency and the ability to float or sink."),
             ("Do heavy objects always sink?", "No. Whether an object floats depends on its material and shape. A large wooden log floats, but a small metal key sinks."),
             ("How do I make a materials test fair?", "Change only the material. Keep the size of each piece, the amount of water or mass, and the way you test it the same.")],
            sets)


if __name__ == "__main__":
    main()
