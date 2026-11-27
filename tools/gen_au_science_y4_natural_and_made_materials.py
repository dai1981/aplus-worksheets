# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U04: natural and made materials, their properties, and how properties decide
their uses (including First Nations uses of natural materials, such as bark, spinifex resin and stone).
  python tools/gen_au_science_y4_natural_and_made_materials.py
Reuses the UK Year 5 and Year 2 material makers, the US Grade 2 choosing-materials makers and the US Grade 7 synthetic material
makers with Australian names. Wrong answers come from real mistakes: thinking made materials are always better, thinking paper
or glass are natural because they come from natural things, and choosing a material by colour instead of a property.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 4, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

M5 = "gen_uk_science_y5_properties_of_materials"
M2 = "gen_uk_science_y2_uses_of_everyday_materials"
C2 = "gen_us_science_g2_choosing_materials"
S7 = "gen_us_science_g7_synthetic_materials"
m5_pick = limit(src(M5, "g_pick"), 5)
m5_prop = limit(src(M5, "g_prop"), 5)
m5_use = src(M5, "g_use")
m5_ins = limit(src(M5, "g_ins"), 3)
m5_b1 = src.B(M5, "B1")
m5_b5 = src.B(M5, "B5")
m2_why = limit(src(M2, "g_why"), 9)
m2_bad = src(M2, "g_bad")
c2_job = limit(src(C2, "g_job"), 4)
c2_test = limit(src(C2, "g_test"), 3)
s7_kind = limit(src(S7, "g_kind"), 4)
s7_source = limit(src(S7, "g_source", drop=["aspirin", "Kevlar", " are made", "medicine"]), 2)
s7_b1 = src.B(S7, "B1", drop=["polymer", "society", "molecule"])

NM = [("wool", "natural"), ("cotton", "natural"), ("wood", "natural"), ("stone", "natural"), ("clay", "natural"), ("bark", "natural"),
      ("leather", "natural"), ("rubber from a rubber tree", "natural"), ("sand", "natural"), ("beeswax", "natural"),
      ("plastic", "made"), ("glass", "made"), ("paper", "made"), ("concrete", "made"), ("steel", "made"), ("nylon", "made"),
      ("brick", "made"), ("polyester", "made"), ("aluminium foil", "made"), ("polystyrene", "made")]
FROM = {"glass": "sand", "paper": "wood", "plastic": "oil", "brick": "clay", "steel": "iron ore", "concrete": "rock, sand and cement", "nylon": "oil", "aluminium foil": "bauxite (a rock)"}


def g_nm():
    m, k = R.choice(NM)
    e = "Natural materials are found in nature and used with little change." if k == "natural" else \
        "Made (processed) materials are made by people by changing natural materials%s." % (", such as %s from %s" % (m, FROM[m]) if m in FROM else "")
    return tq("Is %s a natural material or a made material?" % m, "a %s material" % k,
              ["a %s material" % ("made" if k == "natural" else "natural"), "not a material", "a living thing"], e)


def g_from():
    m = R.choice(sorted(FROM))
    w = sorted({v for k, v in FROM.items() if v != FROM[m]})
    return tq("Which natural material is %s mainly made from?" % m, FROM[m], R.sample(w, 3), "%s is made from %s." % (m[0].upper() + m[1:], FROM[m]))


POOL1 = pool(R, [
    ("What is a natural material?", "a material found in nature, such as wood, wool or stone", ["a material made in a factory", "any material that is shiny", "only materials that are alive"], "Natural materials come from plants, animals or the ground."),
    ("Why are bricks used to build houses?", "They are strong, hard and do not burn easily.", ["They are soft and bendy.", "They are transparent.", "They float."], "Choose materials by their properties."),
    ("Why is wool used for jumpers?", "It is warm and soft.", ["It is waterproof and hard.", "It is transparent.", "It conducts electricity."], "Wool traps air and keeps us warm."),
    ("First Nations Australians used bark to make canoes. Which property made bark useful?", "It is light, strong and floats.", ["It is heavy and sinks.", "It is transparent.", "It is magnetic."], "People chose materials for their properties."),
    ("Spinifex resin was used by First Nations people as a glue for spear heads. Which property mattered?", "It becomes sticky when heated and sets hard.", ["It is soft forever.", "It is transparent.", "It dissolves in rain."], "Natural materials can be very useful."),
    ("Why are kitchen benches often made of stone?", "Stone is hard and resists heat and scratches.", ["Stone is soft and bendy.", "Stone absorbs water.", "Stone is see-through."], "Hardness and heat resistance matter in kitchens."),
    ("Why is cotton good for summer T-shirts in Australia?", "It is soft and lets sweat dry.", ["It keeps all heat in.", "It is waterproof.", "It is very heavy."], "Cotton absorbs moisture."),
    ("Why should plastic bags not go into the ocean?", "They do not break down and can harm turtles and birds.", ["They dissolve quickly.", "They are food for fish.", "They make the water cleaner."], "Some made materials last a very long time."),
    ("Which property makes glass good for windows?", "It is transparent.", ["It is soft.", "It is magnetic.", "It is absorbent."], "Light passes through it."),
    ("Why is rubber used for car tyres?", "It is flexible, tough and grips the road.", ["It is brittle.", "It is transparent.", "It is magnetic."], "Rubber bends without breaking."),
])
POOL5 = pool(R, [
    ("Mia tests four fabrics for a raincoat by dripping 10 drops of water on each. Which result shows the best fabric?", "The paper towel under it stays dry.", ["The fabric soaks up all the water.", "The fabric changes colour.", "The fabric smells nice."], "A raincoat must be waterproof."),
    ("In Mia's test, what should she keep the same?", "the number of drops and the size of each fabric piece", ["the type of fabric", "nothing", "only the colour"], "Only the fabric should change."),
    ("Jack wants to find the strongest paper for a shopping bag. Which test is fair?", "Add the same masses, one at a time, to the same size bag made of each paper.", ["Use a bigger bag for each paper.", "Test only one paper.", "Drop different masses on each."], "Change only the paper."),
    ("Ruby says plastic is always better than wood because it is made by people. Why is this not right?", "The best material depends on the job and its properties.", ["Wood is always better.", "Plastic is natural.", "Materials do not have properties."], "Each material suits different uses."),
    ("Kai compares a wool sock and a cotton sock by wrapping each around a cup of warm water. After 20 minutes, the wool cup is 45 °C and the cotton cup is 38 °C. Which is the better insulator?", "wool", ["cotton", "both the same", "neither"], "The water stayed warmer in wool."),
    ("Why do scientists test new materials before they are used in buildings?", "to make sure they are strong and safe enough", ["to change their colour", "because tests are fun", "to make them heavier"], "Testing shows a material's properties."),
])


def main():
    sets = U.sets([
        ("Natural or made?", [(g_nm, 10), (POOL1, 4), (s7_kind, 4), (g_from, 2)]),
        ("Where materials come from", [(g_from, 6), (s7_source, 2), (s7_b1, 2), (g_nm, 4), (POOL1, 2), (m2_why, 4)]),
        ("Properties of materials", [(m5_pick, 5), (m5_prop, 5), (m5_b1, 4), (POOL1, 2), (m2_bad, 4)]),
        ("Choosing materials for a job", [(m5_use, 6), (m2_why, 5), (c2_job, 4), (POOL1, 2), (m2_bad, 3)]),
        ("Investigations", [(POOL5, 6), (m5_b5, 4), (m5_ins, 3), (c2_test, 3), (g_nm, 2), (m5_use, 2)]),
    ])
    make_au(YEAR, "natural-and-made-materials", SORT, "AC9S4U04", "Chemical sciences",
            "Compare the properties of natural and made materials and relate their properties to their uses, including materials used by "
            "First Nations Australians (summary of the Australian Curriculum v9.0 Science content description).",
            "Natural and Made Materials", "Natural and made materials",
            "Free Year 4 science worksheets on natural and made materials: where materials come from, their properties, and choosing the "
            "best material for a job. 100 questions with answers.",
            "Choose a material by its properties.", "Natural materials come from nature; made materials are changed by people.",
            "<p><b>Materials can be natural or made (processed).</b></p><ul>"
            "<li>Natural materials are found in nature: wood, wool, cotton, stone, clay, bark.</li>"
            "<li>Made materials are made by people from natural ones: glass from sand, paper from wood, plastic from oil, bricks from clay.</li>"
            "<li>We choose a material by its properties: strong, flexible, waterproof, transparent, hard, absorbent or a good insulator.</li></ul>",
            [("Is glass natural or made?", ["it is made by heating sand"], "made"),
             ("Best material for a raincoat?", ["it must keep water out"], "a waterproof material such as plastic")],
            ["Thinking paper or glass are natural because they come from natural things.", "Choosing a material by colour instead of its properties.",
             "Thinking made materials are always better than natural ones."],
            [("What is the difference between natural and made materials?", "Natural materials, such as wood and wool, come from nature. Made materials, such as plastic and glass, are made by people by changing natural materials."),
             ("How do we choose the best material?", "Think about the job, then choose the properties it needs: for example, waterproof for a raincoat or transparent for a window."),
             ("Which natural materials did First Nations Australians use?", "They used bark for canoes and shelters, stone for tools, wood for spears and shields, and plant resins such as spinifex resin as glue.")],
            sets)


if __name__ == "__main__":
    main()
