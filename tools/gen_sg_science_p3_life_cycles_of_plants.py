# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Life cycles of plants (Cycles)
  python tools/gen_sg_science_p3_life_cycles_of_plants.py
A flowering plant's life cycle: seed -> germination -> seedling -> young plant -> adult plant with flowers -> fruits with seeds.
A seed needs water, air and warmth to germinate (not light, not soil); the seed leaves give the seedling food until its
green leaves can make food. Different plants take different times to complete their life cycles.
PSLE-style germination experiments (wet and dry cotton wool, a fridge, a dark cupboard, boiled water) are written here;
UK Year 3 questions about fruits and fair tests are reused with Singapore names.
Wrong answers come from real mistakes: "seeds need soil to germinate", "seeds need light to germinate",
"the shoot grows out first", "all plants take the same time to grow".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63305)
R = U.R
P = People(R)
FL = use(U, "gen_uk_science_y3_flowers_pollination_and_seeds", drop=["winter", "pollinat", "anther", "stigma", "conker", "acorn", "dandelion", "start growing"])
WN = use(U, "gen_uk_science_y3_what_plants_need_to_grow", drop=["winter", "shed", "chocolate", "fizzy", "music", "Monday", "sugar lumps"])

STAGES = ["seed", "germinating seed", "seedling", "young plant", "adult plant with flowers", "fruits with seeds"]
SEEDS = ["green bean", "red bean", "balsam", "chilli", "sunflower", "papaya", "tomato", "corn"]


def g_stage():
    i = R.randrange(len(STAGES) - 1)
    k = R.choice(["after", "before"])
    if not once(("sg", i, k)):
        return None
    if k == "after":
        a, s0 = STAGES[i + 1], STAGES[i]
        q = "In the life cycle of a flowering plant, what comes after the %s?" % s0
    else:
        a, s0 = STAGES[i], STAGES[i + 1]
        q = "In the life cycle of a flowering plant, what comes just before the %s?" % s0
    w = [x for x in STAGES if x not in (a, s0)]
    return item(q, a, R.sample(w, 3), "seed → germinating seed → seedling → young plant → adult plant with flowers → fruits with seeds.")


NEEDS = {"water": True, "air": True, "warmth (a suitable temperature)": True, "light": False, "soil": False, "fertiliser": False}


def g_need():
    k = R.choice(sorted(NEEDS))
    if not once(("nd", k)):
        return None
    if NEEDS[k]:
        return item("Does a seed need %s to germinate?" % k, "Yes. A seed needs water, air and warmth to germinate.",
                    ["No. A seed needs only light.", "No. A seed needs only soil.", "Only seeds planted in pots need it."],
                    "Seeds germinate when they have water, air and a suitable temperature.")
    return item("Does a seed need %s to germinate?" % k, "No. A seed can germinate without it.",
                ["Yes. A seed cannot germinate without it.", "Yes, but only in the day.", "Only small seeds need it."],
                "Seeds can germinate on wet cotton wool in the dark. They need %s later, when the young plant grows." % ("light" if k == "light" else "minerals from the soil"))


def g_germ():
    setups = [("wet cotton wool, in a warm room", True, None), ("dry cotton wool, in a warm room", False, "water"),
              ("wet cotton wool, in a fridge", False, "warmth"), ("wet cotton wool, in a dark cupboard", True, None),
              ("cooled boiled water covered with a layer of oil", False, "air"), ("wet sand, in a warm room", True, None),
              ("wet tissue paper, in a sealed jar with no air", False, "air")]
    pick = R.sample(setups, 4)
    if sum(1 for _, g, _ in pick if g) not in (1, 2, 3):
        return None
    seed = R.choice(SEEDS)
    k = R.choice(["which", "not", "why", "var"])
    names = "ABCD"
    tb = table(["Set-up", "Where the seeds were kept", "Germinated after 5 days?"], [[n, s, "yes" if g else "no"] for n, (s, g, _) in zip(names, pick)])
    q0 = "%s put 10 %s seeds in each set-up below.<br>%s" % (P.next()[0], seed, tb)
    key = tuple(sorted(s for s, _, _ in pick))
    if k == "which":
        yes = [n for n, (_, g, _) in zip(names, pick) if g]
        if len(yes) != 1:
            return None
        a = yes[0]
        if not once(("gw", key)):
            return None
        return item(q0 + "In which set-up did the seeds germinate?", a, [n for n in names if n != a], "The seeds had water, air and warmth there.")
    if k == "not":
        no = [(n, why) for n, (_, g, why) in zip(names, pick) if not g]
        n, why = R.choice(no)
        if not once(("gn", why)):
            return None
        return item(q0 + "Why did the seeds in %s not germinate?" % n, "They had no %s." % why,
                    ["They had no %s." % x for x in ["light", "soil", "fertiliser", "water", "air", "warmth"] if x != why][:3],
                    "Seeds need water, air and warmth to germinate.")
    if k == "why":
        dark = [n for n, (s, _, _) in zip(names, pick) if "dark" in s]
        if not dark:
            return None
        if not once(("gd",)):
            return None
        return item(q0 + "The seeds in %s germinated in the dark. What does this show?" % dark[0], "Seeds do not need light to germinate.",
                    ["Seeds need light to germinate.", "Seeds need soil to germinate.", "Seeds grow faster in the dark."], "Light is needed later, for the leaves to make food.")
    if not once(("gv",)):
        return None
    return item(q0 + "Why were 10 seeds of the same kind used in each set-up?", "so that the results are fair and reliable",
                ["so that they germinate faster", "so that they need less water", "so that they need no air"], "Using more than one seed and the same kind of seed makes the test fair and reliable.")


def g_parts():
    parts = [("seed coat", "protects the inside of the seed"), ("seed leaf", "stores food for the young plant"),
             ("young root", "grows downwards and takes in water"), ("young shoot", "grows upwards towards the light")]
    i = R.randrange(4)
    k = R.choice(["job", "part"])
    if not once(("pt", i, k)):
        return None
    p, job = parts[i]
    if k == "job":
        return item("What does the %s of a seed do?" % p, "It %s." % job, ["It %s." % j for x, j in parts if x != p], "Each part of the seed has a job.")
    return item("Which part of a germinating seed %s?" % job, "the " + p, ["the " + x for x, _ in parts if x != p], "Each part of the seed has a job.")


def g_time():
    plants = [("balsam", "about 3 months"), ("green bean", "about 2 months"), ("rice", "about 4 months"), ("mango tree", "about 5 years"),
              ("durian tree", "about 8 years"), ("tomato", "about 4 months"), ("coconut tree", "about 6 years")]
    a, b = R.sample(plants, 2)
    longer = a if ("year" in a[1]) > ("year" in b[1]) or (("year" in a[1]) == ("year" in b[1]) and int(a[1].split()[1]) > int(b[1].split()[1])) else b
    if int(a[1].split()[1]) == int(b[1].split()[1]) and ("year" in a[1]) == ("year" in b[1]):
        return None
    if not once(("tm", tuple(sorted([a[0], b[0]])))) or not once(("tmn",), 6):
        return None
    nm = lambda x: x if x.endswith("tree") else x + " plant"
    return item("A %s takes %s to grow from a seed to a plant that makes seeds. A %s takes %s. Which has the longer life cycle?" % (nm(a[0]), a[1], nm(b[0]), b[1]),
                "the " + longer[0], ["the " + (b if longer == a else a)[0], "They take the same time.", "Neither has a life cycle."],
                "Different plants take different lengths of time to complete their life cycles.")


def g_height():
    seed = R.choice(SEEDS[:5])
    days = [2, 4, 6, 8, 10]
    h = [0]
    for _ in range(4):
        h.append(h[-1] + R.randint(1, 4))
    k = R.choice(["d8", "grow", "fast", "pred"])
    if not once(("ht", k), 1 if k == "pred" else 2):
        return None
    tb = table(["Day", "Height of seedling (cm)"], [[str(d), str(x)] for d, x in zip(days, h)])
    q0 = "%s measured a %s seedling every 2 days.<br>%s" % (P.next()[0], seed, tb)
    if k == "d8":
        w = sorted({h[2], h[4], h[3] + 5} - {h[3]})
        if len(w) < 3:
            return None
        return item(q0 + "How tall was the seedling on day 8?", "%d cm" % h[3], ["%d cm" % x for x in w],
                    "Read the row for day 8.")
    if k == "grow":
        return item(q0 + "How much did it grow from day 2 to day 10?", "%d cm" % (h[4] - h[0]), ["%d cm" % h[2], "%d cm" % (h[4] + 2), "%d cm" % (h[4] - h[1] + 10)],
                    "%d − %d = %d cm." % (h[4], h[0], h[4] - h[0]))
    if k == "fast":
        g = [h[i + 1] - h[i] for i in range(4)]
        m = max(g)
        if g.count(m) > 1:
            return None
        i = g.index(m)
        lab = ["day %d to day %d" % (days[j], days[j + 1]) for j in range(4)]
        return item(q0 + "Between which days did it grow the most?", lab[i], [x for j, x in enumerate(lab) if j != i], "It grew %d cm then." % m)
    return item(q0 + "What does the table show?", "The seedling grew taller as the days went on.", ["The seedling got shorter.", "The seedling did not grow.", "The seedling grew only on day 2."],
                "The height increased every time it was measured.")


B1 = bank([
    ("What is germination?", "when a seed starts to grow into a new plant", ["when a plant makes flowers", "when a fruit falls from a tree", "when a plant dies"], "The young root and shoot grow out of the seed."),
    ("Which grows out of a germinating seed first?", "the young root", ["the young shoot", "a flower", "a fruit"], "The root grows first and takes in water."),
    ("What does a seed need to germinate?", "water, air and warmth", ["light, soil and water", "fertiliser and light", "only soil"], "Seeds do not need light or soil to germinate."),
    ("What does a flowering plant make after its flowers?", "fruits with seeds", ["roots", "seedlings", "spores"], "The flowers develop into fruits that contain seeds."),
    ("What is a seedling?", "a young plant that has just grown from a seed", ["a seed that has not germinated", "an old plant", "a fruit"], "A seedling has its first leaves."),
    ("Where do the seeds of a flowering plant develop?", "inside the fruit", ["inside the roots", "inside the leaves", "in the soil"], "A papaya fruit contains many seeds."),
    ("Which stage of a flowering plant can make seeds?", "the adult plant", ["the seed", "the seedling", "the germinating seed"], "Only the adult plant makes flowers and fruits."),
    ("Why does the young shoot grow upwards?", "to reach light so the leaves can make food", ["to look for water in the sky", "to hide from insects", "to find soil"], "The young root grows downwards to find water."),
])
B2 = bank([
    ("Why do the seed leaves of a bean seedling shrivel after a few days?", "Their stored food is used up by the growing seedling.", ["They are eaten by the roots.", "They get too much water.", "They turn into flowers."], "The green leaves then make food for the plant."),
    ("Where does a germinating seed get its food before it has green leaves?", "from the food stored in its seed leaves", ["from the soil", "from the light", "from the water"], "That is why seeds can germinate without soil."),
    ("Why does a seedling need light after it has germinated?", "Its green leaves need light to make food.", ["Light makes the roots grow longer.", "Light softens the seed coat.", "It does not need light."], "Once the stored food is used up, the leaves must make food."),
    ("A mango seed and a balsam seed were planted at the same time. Which will make fruits first?", "the balsam plant", ["the mango tree", "both at the same time", "neither"], "Balsam completes its life cycle in a few months; a mango tree takes years."),
    ("Which statement about plant life cycles is correct?", "Different plants take different lengths of time to complete their life cycles.", ["All plants take one year.", "Trees have the shortest life cycles.", "Plants with big seeds always grow fastest."], "A bean plant takes weeks; a durian tree takes years."),
    ("Which part of the seed protects it?", "the seed coat", ["the seed leaf", "the young root", "the young shoot"], "The seed coat is the hard outer covering."),
    ("Why does the seed coat split during germination?", "The seed takes in water and swells.", ["The seed dries out.", "The sun burns it.", "Insects eat it."], "Water makes the seed swell and soften."),
    ("What do the fruits of a plant do in the life cycle?", "They protect the seeds and help spread them.", ["They make food from light.", "They take in water from the soil.", "They hold the plant up."], "The seeds inside grow into new plants."),
])
B3 = bank([
    ("Why does a farmer soak green bean seeds in water before planting them?", "Water helps the seeds start to germinate.", ["Water kills insects.", "Water makes the seeds float.", "Water makes the seeds smaller."], "Seeds need water to germinate."),
    ("Seeds stored in a dry, cold place do not germinate for months. Why?", "They have no water and it is too cold.", ["They have no soil.", "They have no light.", "They are dead."], "They will germinate when they get water and warmth."),
    ("Which of these would a seed NOT need to germinate?", "sunlight", ["water", "air", "warmth"], "Seeds can germinate in the dark."),
    ("Why will a seed planted very deep in waterlogged soil not germinate?", "It cannot get enough air.", ["It gets too much light.", "It is too warm.", "It has too many minerals."], "The water fills the air spaces in the soil."),
    ("A seedling kept in the dark grew tall, thin and yellow. What did it lack?", "light to make food", ["water", "air", "warmth"], "It used its stored food to grow tall searching for light."),
    ("Which shows the correct order?", "seed → seedling → adult plant → flowers → fruits", ["fruits → seed → flowers → seedling", "seedling → seed → fruits → adult plant", "flowers → seedling → seed → fruits"], "The fruits contain new seeds, so the cycle starts again."),
])
B5 = bank([
    ("Siti put bean seeds on wet cotton wool in two dishes. Dish A was in the classroom; dish B was in a fridge. Only the seeds in A germinated. What was she testing?", "whether seeds need warmth to germinate", ["whether seeds need water", "whether seeds need light", "whether seeds need soil"], "Only the temperature was different."),
    ("Ravi wants to test whether seeds need water to germinate. Which pair of set-ups should he use?", "wet cotton wool and dry cotton wool, both in the same warm room", ["wet cotton wool in the light and in the dark", "wet cotton wool in a fridge and dry cotton wool in a room", "wet sand and wet soil"], "Change only the water."),
    ("Why was a layer of oil poured on the boiled water in a germination experiment?", "to stop air from dissolving into the water", ["to keep the seeds warm", "to give the seeds food", "to give the seeds light"], "Boiling removes the air; the oil stops air from getting back in."),
    ("A pupil put seeds on wet cotton wool in a dark cupboard. They germinated. What can she conclude?", "Light is not needed for germination.", ["Light is needed for germination.", "Water is not needed for germination.", "Seeds need soil."], "The seeds germinated without light."),
    ("Mei Ling planted 20 seeds. 16 germinated. How many did not germinate?", "4", ["16", "20", "36"], "20 − 16 = 4."),
    ("Why do pupils use more than one seed in each set-up?", "Some seeds may not germinate, so using many gives a reliable result.", ["To use up the seeds.", "So that they grow taller.", "So that they need less water."], "One seed might be dead."),
    ("A pupil measured the height of two seedlings: one by the window and one in a dark cupboard. Which variable did she change?", "the amount of light", ["the amount of water", "the type of seed", "the size of the pot"], "Only the place (light) was different."),
])


def body():
    think = ("<p><b>A flowering plant grows through stages: seed → seedling → young plant → adult plant → flowers → fruits with seeds.</b></p>"
             "<ul><li>A seed <b>germinates</b> when it has <b>water, air and warmth</b>. It does not need light or soil.</li>"
             "<li>The young root grows out first. The seed leaves give food until the green leaves can make food.</li>"
             "<li>The adult plant makes flowers. The flowers become fruits with seeds, and the cycle starts again.</li>"
             "<li>Different plants take different times to complete their life cycles.</li></ul>")
    ex = [("Seeds on dry cotton wool did not germinate. Why?", ["Compare with the wet cotton wool", "Only the water was different"], "They had no water."),
          ("Seeds germinated in a dark cupboard. What does this show?", ["The seeds had water, air and warmth", "They had no light"], "Light is not needed to germinate.")]
    mist = ["Thinking seeds need soil to germinate. They have stored food, so wet cotton wool is enough.",
            "Thinking seeds need light to germinate. Light is needed later, by the leaves.",
            "Thinking the shoot comes out first. The root comes out first.",
            "Changing two things at once in a germination experiment."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stages of a plant's life", B1 + [(g_stage, 5), (FL.g_cycle, 4), (g_parts, 3)]),
        ("Germination and the seedling", B2 + [(g_need, 5), (g_parts, 4), (g_time, 3)]),
        ("What seeds need", B3 + [(g_need, 1), (g_germ, 5), (g_time, 3), (FL.g_cycle, 3), (WN.g_what, 2)]),
        ("Growing plants", FL.B3 + [(g_height, 4), (g_stage, 3), (WN.g_test, 3), (g_time, 2)]),
        ("PSLE-style experiments", B5 + [(g_germ, 8), (g_height, 3), (WN.g_test, 2)]),
    ])
    make_sg(3, "life-cycles-of-plants", 5, "Cycles", "Cycles in plants and animals (Life cycles of plants)",
            "Show an understanding that different plants have different life cycles: seed, germination, seedling, young plant, adult plant, "
            "flowers and fruits with seeds. Investigate the conditions needed for seeds to germinate: water, air and a suitable temperature "
            "(summary of the MOE Primary Science Syllabus).",
            "Life Cycles of Plants",
            "Primary 3 Science: Life Cycles of Plants Worksheets (with Answers)",
            "Life cycles of plants",
            "Free Primary 3 science worksheets for Singapore pupils on life cycles of plants: seed, germination, seedling, adult plant, flowers and fruits, with germination experiments. 100 questions with answers.",
            "A seed grows into a plant that makes new seeds.",
            "Seeds need water, air and warmth to germinate.",
            body(),
            [("What does a seed need to germinate?", "Water, air and a suitable temperature (warmth). It does not need light or soil, because it has food stored inside."),
             ("Which part comes out of a seed first?", "The young root comes out first and grows downwards. Then the young shoot grows upwards."),
             ("Do all plants have the same life cycle length?", "No. A green bean plant can make seeds in about two months, but a durian tree takes many years.")],
            sets)


if __name__ == "__main__":
    main()
