# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Plant parts and functions (Systems)
  python tools/gen_sg_science_p4_plant_parts_and_functions.py
Leaves make food; the stem holds the plant up and carries water and food; roots hold the plant in the soil and take in
water and mineral salts; flowers make fruits and seeds. Some parts store food (sweet potato, ginger, sugar cane).
Plant parts work together as a system. UK Year 3 plant questions are reused with Singapore names;
Singapore vegetables and PSLE-style experiments (removing leaves, cutting the stem, coloured water) are written here.
Wrong answers come from real mistakes: "roots make food", "plants take in food from the soil",
"ginger is a root", "the stem only holds the plant up".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63401)
R = U.R
P = People(R)
PP = use(U, "gen_uk_science_y3_parts_of_a_flowering_plant", drop=["parsnip", "winter", "conker", "blossom"])
WM = use(U, "gen_uk_science_y3_how_water_moves_in_plants", drop=["winter"])

FOOD = [("sweet potato", "the root"), ("carrot", "the root"), ("tapioca", "the root"), ("radish", "the root"),
        ("ginger", "the stem"), ("potato", "the stem"), ("sugar cane", "the stem"), ("spinach", "the leaves"), ("lettuce", "the leaves"),
        ("cabbage", "the leaves"), ("broccoli", "the flowers"), ("cauliflower", "the flowers"), ("peanuts", "the seeds"), ("corn kernels", "the seeds"),
        ("rice", "the seeds"), ("mango", "the fruit"), ("lady's fingers (okra)", "the fruit"), ("chilli", "the fruit")]
PARTS = ["the root", "the stem", "the leaves", "the flowers", "the fruit", "the seeds"]


def g_food():
    f, p = R.choice(FOOD)
    if not once(("fd", f)):
        return None
    w = R.sample([x for x in PARTS if x != p], 3)
    note = {"ginger": "Ginger grows underground, but it is a stem: it has buds and grows sideways.",
            "potato": "A potato grows underground, but it is a stem that stores food."}.get(f.split()[0], "We eat %s of the %s plant." % (p, f.split(" (")[0]))
    return item("Which part of the plant do we eat when we eat %s?" % f, p, w, note)


JOBS = [("the roots", "hold the plant firmly in the soil"), ("the roots", "take in water and mineral salts from the soil"),
        ("the stem", "hold the plant upright"), ("the stem", "carry water from the roots to the leaves"), ("the stem", "carry food from the leaves to other parts"),
        ("the leaves", "make food for the plant using light"), ("the flowers", "make fruits and seeds")]


def g_job():
    p, j = R.choice(JOBS)
    if not once(("jb", j)):
        return None
    w = [x for x in ["the roots", "the stem", "the leaves", "the flowers"] if x != p]
    return item("Which part of a plant helps to %s?" % j, p, w, "%s help%s to %s." % (p[0].upper() + p[1:], "" if p.endswith("s") else "s", j))


def g_remove():
    cases = [("all its leaves were removed", "It cannot make enough food, so it grows weakly or dies.",
              ["It cannot take in water.", "It cannot stand upright.", "It grows more flowers."]),
             ("its roots were cut off", "It cannot take in water and mineral salts, so it wilts and dies.",
              ["It cannot make seeds only.", "It grows taller.", "It makes more food."]),
             ("its stem was bent and broken", "Water cannot reach the leaves, so the leaves wilt.",
              ["The roots grow more.", "It makes more flowers.", "It takes in more water."]),
             ("all its flowers were picked off", "It cannot make fruits and seeds.", ["It cannot take in water.", "It cannot make food.", "It cannot stand upright."]),
             ("it was kept in a dark cupboard", "Its leaves cannot make food, so it grows weakly.", ["Its roots cannot hold it.", "It cannot take in water.", "It grows more flowers."])]
    i = R.randrange(len(cases))
    if not once(("rm", i)):
        return None
    c, a, w = cases[i]
    return item("A healthy plant was left for two weeks after %s. What most likely happened?" % c, a, w, "Each part of the plant has a job; the plant needs all of them.")


SPECIAL = [("Why does a money plant have roots along its stem?", "to cling to a wall or a pole so it can climb towards light", ["to make food", "to catch insects", "to store water only"],
            "These roots help the weak stem to climb."),
           ("Why do mangrove trees have roots that stick up out of the mud?", "to take in air, because the mud has very little air", ["to make food", "to catch fish", "to stand upright only"],
            "These breathing roots get air for the roots below."),
           ("Why does a cactus have a thick, green stem?", "to store water and make food", ["to catch insects", "to hold seeds", "to make it heavy"],
            "Its leaves are spines, so the green stem makes food."),
           ("Why do some plants such as the rain tree have a thick, woody trunk?", "to hold up the heavy branches and leaves", ["to store seeds", "to make flowers", "to take in water from the air"],
            "A strong stem holds the plant up."),
           ("Why do the leaves of most plants face the light?", "to get more light to make food", ["to keep warm only", "to take in water", "to hide from insects"],
            "Leaves need light to make food."),
           ("Why are some stems, such as the stem of the kangkong, hollow and soft?", "They do not need to hold up a heavy plant and help it float in water.", ["They make food in the roots.", "They store seeds.", "They are dead."],
            "Kangkong grows in water and wet soil.")]


def g_special():
    q, a, w, e = R.choice(SPECIAL)
    if not once(("sp", q)):
        return None
    return item(q, a, w, e)


def g_mass():
    k = R.choice(["leaf", "root", "var", "same"])
    if not once(("ms", k)):
        return None
    m = R.randint(40, 60)
    tb = table(["Plant", "What was done", "Mass after 2 weeks (g)"],
               [["A", "nothing", str(m + R.randint(8, 15))], ["B", "all leaves removed", str(m - R.randint(4, 8))], ["C", "half the roots cut off", str(m + R.randint(1, 4))]])
    q0 = "%s had three identical plants of mass %d g. Each was watered daily in sunlight.<br>%s" % (P.next()[0], m, tb)
    if k == "leaf":
        return item(q0 + "Why did plant B lose mass?", "It could not make food without leaves.", ["It took in too much water.", "Its roots grew too long.", "It made too many flowers."],
                    "Leaves make food for growth.")
    if k == "root":
        return item(q0 + "Why did plant C grow less than plant A?", "It could take in less water and mineral salts.", ["It had more leaves.", "It got less light.", "It had no stem."],
                    "Roots take in water and mineral salts.")
    if k == "var":
        return item(q0 + "Which plant is the control?", "plant A", ["plant B", "plant C", "none of them"], "Nothing was removed from plant A, so the others are compared with it.")
    return item(q0 + "Which should be kept the same for all three plants?", "the amount of water and light", ["the parts removed", "the mass after 2 weeks", "the number of leaves"],
                "Only the part removed should be different.")


B1 = bank([
    ("Which part of a plant makes food?", "the leaves", ["the roots", "the flowers", "the seeds"], "Leaves use light to make food."),
    ("Which part of a plant takes in water from the soil?", "the roots", ["the leaves", "the flowers", "the fruits"], "Roots take in water and mineral salts."),
    ("What does the stem do?", "It holds the plant up and carries water and food.", ["It makes seeds.", "It takes in water from the soil.", "It attracts insects."], "The stem connects the roots to the leaves."),
    ("What do the flowers of a plant develop into?", "fruits with seeds", ["roots", "leaves", "stems"], "Seeds grow into new plants."),
    ("Which two parts of a plant are usually above the ground?", "the stem and the leaves", ["the roots and the leaves", "the roots and the stem", "only the roots"], "The roots are usually under the soil."),
    ("Which part of a plant holds it firmly in the soil?", "the roots", ["the leaves", "the flowers", "the fruits"], "Roots spread into the soil and anchor the plant."),
    ("Which part of a plant carries food from the leaves to other parts?", "the stem", ["the roots only", "the flowers", "the seeds"], "Food made in the leaves is carried by the stem to the roots, fruits and seeds."),
    ("Does a plant take in food from the soil?", "No. It takes in water and mineral salts; it makes its own food in the leaves.", ["Yes, all of its food.", "Yes, through its leaves.", "Only at night."], "Soil does not give plants food."),
])
B2 = bank([
    ("A sweet potato is a swollen root. What is stored in it?", "food made by the leaves", ["water from the air", "soil", "oxygen"], "Food is carried down the stem and stored in the root."),
    ("Why is sugar cane sweet?", "Its stem stores the sugar made in the leaves.", ["It takes in sugar from the soil.", "Its roots make sugar.", "Rain puts sugar into it."], "The stem stores food."),
    ("Why do the leaves of a plant wilt when the roots are damaged?", "Not enough water can be taken in and carried to the leaves.", ["The leaves make too much food.", "The flowers take all the water.", "The stem grows too long."], "The plant parts work together."),
    ("How do the roots and the leaves work together?", "Roots take in water for the leaves to use in making food, and leaves make food for the roots.", ["They do not need each other.", "Roots make food for the leaves.", "Leaves take in water for the roots."], "Parts of a plant work as a system."),
    ("Why do some plants grow tall stems?", "to reach more light for their leaves", ["to reach water underground", "to stay cool", "to hide from animals"], "Taller plants are not shaded by others."),
    ("Which part of a plant is like a 'pipe' that carries water?", "the stem", ["the leaf blade", "the flower petal", "the seed coat"], "Tubes in the stem carry water up."),
    ("Which plant part would be damaged by a caterpillar that eats leaves?", "the part that makes food", ["the part that holds the plant in the soil", "the part that makes seeds", "the part that takes in water"], "Leaves make food."),
    ("A plant has many fine, hair-like roots. How does this help?", "They give a large surface to take in more water.", ["They make the plant lighter.", "They make food faster.", "They attract insects."], "More roots touch more soil water."),
])
B3 = bank([
    ("Why is ginger called an underground stem and not a root?", "It has buds that grow into new shoots.", ["It grows in the soil.", "It is brown.", "It stores food."], "Roots do not have buds."),
    ("Why does a gardener tie a young papaya plant to a stick?", "Its stem is not yet strong enough to hold it up.", ["to help it take in water", "to make food", "to keep insects away"], "The stick helps support the plant."),
    ("Which of these vegetables is a leaf?", "kangkong leaves", ["sweet potato", "ginger", "lady's fingers"], "We eat the leaves and soft stems of kangkong."),
    ("A plant has been watered but its leaves are still drooping on a hot day. What is the most likely reason?", "It is losing water from its leaves faster than its roots can take it in.", ["It is making too much food.", "It has too many flowers.", "Its roots are too long."], "Plants lose water through their leaves on hot days."),
    ("Why should we not pull up a plant when moving it to a new pot?", "The roots may be damaged and the plant cannot take in water.", ["The leaves will fall off at once.", "The flowers will turn into seeds.", "The stem will make food."], "Keep the roots and soil together."),
    ("Which part of a pandan plant do we use in cooking?", "the leaves", ["the roots", "the flowers", "the seeds"], "Pandan leaves give a sweet smell to kueh and rice."),
])
B5 = bank([
    ("Siti placed a white flower in water with blue colouring. After a day, the petals turned blue. What does this show?", "Water travels up the stem to the flower.", ["Flowers make blue colouring.", "Water travels down from the flower.", "The colouring is food for the flower."], "The coloured water was carried up through the stem."),
    ("Ravi cut a stem across after it stood in red water. He saw red dots. What are they?", "the water-carrying tubes", ["the food-carrying tubes", "seeds", "drops of blood"], "The tubes carried the red water up."),
    ("Mei Ling covered all the leaves of a plant with black paper for a week. What did she want to find out?", "whether leaves need light to make food", ["whether roots need water", "whether stems need soil", "whether flowers need air"], "Only the light reaching the leaves was changed."),
    ("A pupil grew two identical plants. Plant P had all its leaves; plant Q had half its leaves removed. Which plant grew taller after 3 weeks?", "plant P", ["plant Q", "both the same", "neither"], "More leaves make more food for growth."),
    ("Why should both plants in an experiment get the same amount of water and light?", "so that only one variable is changed", ["so that both die", "so that they grow flowers", "so that they need less soil"], "This makes the test fair."),
    ("A pupil put a plant with roots in a measuring cylinder of water and covered the water with oil. The water level dropped. Why?", "The roots took in water.", ["The oil drank the water.", "The water evaporated through the oil.", "The leaves pushed water down."], "The oil stops evaporation, so the water went into the plant."),
])


def body():
    think = ("<p><b>Each part of a plant has a job, and the parts work together as a system.</b></p>"
             "<ul><li><b>Leaves</b> make food using light.</li>"
             "<li><b>Stem</b> holds the plant up and carries water (from the roots) and food (from the leaves).</li>"
             "<li><b>Roots</b> hold the plant in the soil and take in water and mineral salts.</li>"
             "<li><b>Flowers</b> develop into fruits with seeds.</li></ul>"
             "<p>Some parts also store food: sweet potato (root), ginger and sugar cane (stem).</p>")
    ex = [("All the leaves of a plant are removed. What happens?", ["Leaves make food", "No leaves, no food"], "The plant grows weakly or dies."),
          ("A celery stalk stands in red water. Where does the red colour go?", ["Water is taken in at the bottom", "It moves up through the stem"], "Up the stem to the leaves.")]
    mist = ["Thinking roots take in food from the soil. Plants make their own food in the leaves.",
            "Thinking ginger and potatoes are roots. They are underground stems.",
            "Forgetting that the stem carries food down as well as water up.",
            "Changing more than one thing in a plant experiment."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a plant", B1 + [(PP.g_pic, 4), (g_job, 5), (PP.g_job, 3)]),
        ("What each part does", B2 + [(g_job, 2), (g_remove, 4), (PP.g_tree, 2), (WM.g_path, 4)]),
        ("Plant parts we eat and use", B3 + [(g_food, 8), (g_special, 4), (PP.g_prob, 2)]),
        ("Water in the plant", WM.B1 + [(WM.g_dye, 4), (WM.g_wilt, 3), (g_special, 2), (g_remove, 1), (WM.g_path, 2)]),
        ("PSLE-style experiments", B5 + [(g_mass, 4), (WM.g_dye, 3), (WM.g_table, 4), (PP.g_prob, 3)]),
    ])
    make_sg(4, "plant-parts-and-functions", 1, "Systems", "Plant system (Plant parts and functions)",
            "Identify the parts of a plant (leaf, stem and root) and their functions: leaves make food, the stem holds the plant up and carries water and food, "
            "and roots hold the plant in the soil and take in water and mineral salts. Recognise that the plant parts work together as a system "
            "(summary of the MOE Primary Science Syllabus).",
            "Plant Parts and Functions",
            "Primary 4 Science: Plant Parts and Functions Worksheets (with Answers)",
            "Plant parts and functions",
            "Free Primary 4 science worksheets for Singapore pupils on plant parts and their functions: leaves, stem, roots, flowers, plant parts we eat, and experiments. 100 questions with answers.",
            "Leaves make food; roots take in water.",
            "The stem holds the plant up and carries water and food.",
            body(),
            [("What are the functions of the roots?", "Roots hold the plant firmly in the soil and take in water and mineral salts."),
             ("What does the stem do?", "The stem holds the plant upright and carries water from the roots to the leaves and food from the leaves to other parts."),
             ("Is ginger a root?", "No. Ginger is an underground stem. It has buds that can grow into new shoots, and it stores food.")],
            sets)


if __name__ == "__main__":
    main()
