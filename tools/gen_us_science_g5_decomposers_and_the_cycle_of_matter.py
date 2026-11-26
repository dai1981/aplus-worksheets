# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Decomposers and the Cycle of Matter (5-LS2-1)
  python tools/gen_us_science_g5_decomposers_and_the_cycle_of_matter.py
Matter moves in a cycle: plants take in air (carbon dioxide) and water, animals eat plants,
and decomposers (bacteria and fungi, helped by earthworms and other soil animals) break down
dead organisms and wastes, returning matter to the soil and air for plants to use again.
Pictures: a cycle diagram with numbered arrows. Data: compost and rotting-fruit investigations.
Wrong answers come from real mistakes: "dead things just disappear", "plants eat soil",
"decomposers are harmful and useless", "matter is used up".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, text, arrow, table, bar_chart, People, INK, GREEN, BROWN
import sci_foodweb as FW

U = Unit(50110)
R = U.R
P = People(R)

DECOMP = ["mushrooms", "mold", "bacteria", "fungi"]
HELPERS = ["earthworms", "pill bugs", "millipedes", "termites"]
NOTDEC = ["hawks", "grass", "rabbits", "oak trees", "frogs", "deer", "sunflowers", "foxes"]


def cycle(label="cycle of matter with numbered arrows"):
    W, H = 420, 270
    box = {"air": (210, 30, "Air (carbon dioxide)"), "plants": (70, 135, "Plants"), "animals": (350, 135, "Animals"),
           "decomp": (210, 240, "Decomposers and soil")}
    s = []
    for k, (x, y, t) in box.items():
        w = 9 * len(t) * 0.82 + 22
        s.append(rect(x - w / 2, y - 16, w, 32, "#e3f1df" if k == "plants" else ("#fdf0dc" if k == "animals" else ("#dceefb" if k == "air" else "#efe2d2")), INK, 1.5, 8))
        s.append(text(x, y + 5, t, 13))
    A = [(1, (140, 40), (78, 117)), (2, (232, 223), (122, 152)), (3, (122, 128), (298, 128)), (4, (52, 152), (132, 238)),
         (5, (340, 152), (250, 222)), (6, (330, 117), (270, 45))]
    for n, (x1, y1), (x2, y2) in A:
        s.append(arrow(x1, y1, x2, y2, "#555555", 2.2, 10))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (mx, my, INK))
        s.append(text(mx, my + 5, str(n), 13))
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-pf='xl' ", 1)


ARROWS = {1: "Plants take in carbon dioxide from the air.", 2: "Plants take in water and nutrients from the soil.", 3: "Animals eat plants.",
          4: "Dead plants and fallen leaves are broken down by decomposers.", 5: "Dead animals and animal wastes are broken down by decomposers.",
          6: "Animals breathe out carbon dioxide into the air."}


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ makers
def g_arrow():
    n = R.randint(1, 6)
    if R.random() < 0.5:
        return item(fig(cycle()) + "Which arrow shows this: %s" % ARROWS[n], "arrow %d" % n,
                    ["arrow %d" % k for k in R.sample([k for k in range(1, 7) if k != n], 3)], "Arrow %d: %s" % (n, ARROWS[n]))
    return item(fig(cycle()) + "What does arrow %d show?" % n, ARROWS[n], R.sample([v for k, v in ARROWS.items() if k != n], 3), "Arrow %d points %s." % (n, {
        1: "from the air to the plants", 2: "from the soil to the plants", 3: "from the plants to the animals", 4: "from the plants to the decomposers",
        5: "from the animals to the decomposers", 6: "from the animals to the air"}[n]))


def g_which_dec():
    a = R.choice(DECOMP)
    w = R.sample(NOTDEC, 3)
    return item("Which of these is a decomposer?", a, w, cap(a) + " break down dead plants and animals. The others are producers or consumers.")


def g_compost():
    start = R.choice([400, 500, 600, 800])
    weeks = [0, 2, 4, 6, 8]
    vals = [start]
    for _ in weeks[1:]:
        vals.append(vals[-1] - R.choice([40, 50, 60, 70, 80]))
    ch = bar_chart(["wk %d" % w for w in weeks], vals, "grams", "bar graph: mass of leaves in a compost bin", ymax=(start // 200 + 1) * 200, step=200, col="#8a5a2b", w=300)
    p = P.next()
    ask = R.choice(["loss", "why"])
    if ask == "loss":
        d = vals[0] - vals[-1]
        return item(fig(ch) + "%s weighs the dead leaves in a compost bin every 2 weeks. How much mass did the leaves lose in 8 weeks?" % p[0],
                    "%d g" % d, ["%d g" % vals[-1], "%d g" % vals[0], "%d g" % (vals[0] - vals[1])],
                    "%d − %d = %d g. Decomposers broke down that much of the leaves." % (vals[0], vals[-1], d))
    return item(fig(ch) + "%s weighs the dead leaves in a compost bin every 2 weeks. Why does the mass go down?" % p[0],
                "Decomposers break the leaves down into nutrients, water and gases.", ["The leaves are destroyed and the matter is gone.", "The leaves turn into rocks.", "The scale gets less accurate."],
                "The matter is not destroyed. It goes into the soil as nutrients and into the air as carbon dioxide and water vapor.")


def g_rot_table():
    conds = [("warm and moist", R.randint(4, 6)), ("cold and moist", R.randint(12, 18)), ("warm and dry", R.randint(20, 26)), ("cold and dry", R.randint(30, 40))]
    R.shuffle(conds)
    k = R.choice(["apple slice", "piece of bread", "slice of pumpkin", "banana peel"])
    rows = [[c, "%d days" % d] for c, d in conds]
    best = min(conds, key=lambda c: c[1])
    return item(table(["Place", "Days until mold covered the %s" % k], rows) + "Which conditions helped the decomposers work fastest?",
                best[0], [c for c, _ in conds if c != best[0]],
                "Mold covered the %s in only %d days when it was %s. Decomposers grow fastest with warmth and moisture." % (k, best[1], best[0]))


def g_return():
    w = R.choice(sorted(FW.WEBS))
    x = R.choice(FW.organisms(w))
    verb = "die" if x in ("wildflowers",) else "dies"
    return item("%s in the %s %s. What happens to the matter in it?" % (cap(FW.a(x)), FW.WEBS[w]["name"], verb),
                "Decomposers break it down and return it to the soil and air.", ["It disappears completely.", "It stays the same forever.", "It turns into sunlight."],
                "Bacteria and fungi break down the body. The nutrients go back into the soil and carbon dioxide goes into the air, where plants can use them again.")


B1 = bank([
    ("What is a decomposer?", "an organism that breaks down dead plants and animals", ["an animal that hunts", "a plant that makes food", "a rock in the soil"],
     "Bacteria and fungi are decomposers. They feed on dead matter and wastes."),
    ("Which two kinds of organisms are the main decomposers?", "bacteria and fungi", ["hawks and owls", "grass and trees", "rabbits and deer"],
     "Bacteria and fungi (like mold and mushrooms) do most of the decomposing."),
    ("Earthworms eat dead leaves and mix them into the soil. How do they help?", "They help break down dead matter so nutrients return to the soil.", ["They make food from sunlight.", "They stop leaves from rotting.", "They remove all the soil."],
     "Earthworms and other small soil animals help decomposers by breaking dead matter into small pieces."),
    ("What would happen if there were no decomposers?", "Dead plants and animals would pile up, and soil would lose its nutrients.", ["Nothing would change.", "Plants would grow faster.", "Animals would stop eating."],
     "Without decomposers, matter would stay locked in dead things instead of cycling back to plants."),
    ("Where do plants get most of the matter they need to grow?", "carbon dioxide from the air and water", ["the soil only", "the sun's matter", "other plants"],
     "Plants build their bodies mostly from air and water. Soil gives small amounts of nutrients."),
    ("Mold growing on old bread is an example of", "a decomposer at work", ["a producer", "a predator", "a chemical made in a factory"],
     "Mold is a fungus. It breaks down the bread."),
    ("Which statement about matter in an ecosystem is true?", "Matter moves around in a cycle and is used again and again.", ["Matter is used up and disappears.", "New matter is made every day by the sun.", "Matter only moves from animals to plants."],
     "The same matter cycles among plants, animals, decomposers, soil and air."),
    ("What do decomposers return to the soil?", "nutrients", ["sunlight", "rocks", "heat only"],
     "Nutrients from dead matter go back into the soil, where plant roots take them in."),
    ("What gas do decomposers, animals and plants give off into the air when they use food?", "carbon dioxide", ["oxygen only", "helium", "smoke"],
     "Living things that break down food give off carbon dioxide. Plants take it in again."),
    ("A fallen log in a forest gets soft and crumbly over many years. Why?", "Fungi, bacteria and insects are breaking it down.", ["The log is melting.", "The log is turning into stone.", "Rain is washing all of it away at once."],
     "Decomposers slowly break the wood into nutrients, water and carbon dioxide."),
])
B5 = bank([
    ("Ava sets up two bags with apple slices: one sealed with a moist paper towel, one dry. Which variable is she testing?", "moisture", ["temperature", "the kind of fruit", "the size of the bag"],
     "Only the moisture is different."),
    ("Leo puts a slice of bread in the freezer and one on the counter. The counter slice molds first. What can he conclude?", "Decomposers work faster where it is warm.", ["Cold air makes mold grow.", "Freezers create mold.", "Mold needs light."],
     "The freezer is too cold for mold to grow quickly."),
    ("A sealed terrarium has soil, plants, worms and water. It stays healthy for months. Why?", "Matter cycles inside: plants, animals and decomposers reuse it.", ["Someone adds food every day.", "The plants do not need air.", "The jar makes new matter."],
     "Water, carbon dioxide and nutrients keep cycling inside the closed jar."),
    ("Why do gardeners add compost to soil?", "Compost has nutrients that decomposers released from dead matter.", ["Compost kills all bacteria.", "Compost makes soil dry.", "Compost is made of rocks."],
     "Compost returns nutrients to the soil that plants can use."),
    ("Which should NOT go into a compost bin for decomposers to break down?", "plastic bags", ["fruit peels", "dead leaves", "coffee grounds"],
     "Decomposers cannot break down plastic. Food scraps and leaves decompose."),
    ("A class measures the temperature in the middle of a compost pile: 45 °C, much warmer than the air. What causes the heat?", "Decomposers using the food in the dead matter", ["The sun shining through the pile", "Worms running around", "The pile is on fire"],
     "When bacteria break down food, they release energy as heat."),
    ("Which model best shows how matter moves in an ecosystem?", "a cycle with arrows from air and soil to plants, plants to animals, and both to decomposers and back", ["a straight line from the sun to the soil", "a single arrow from animals to plants", "a picture of one plant"],
     "Matter goes around in a cycle and is reused."),
    ("Why are decomposers sometimes called nature's recyclers?", "They break down dead things so the matter can be used again.", ["They collect cans.", "They make new matter.", "They eat only living plants."],
     "Like recycling, decomposing lets old matter become new living things."),
])


def body():
    think = ("<p>Matter moves around an ecosystem in a <b>cycle</b>. It is not used up; it is used again and again.</p>"
             "<ul><li><b>Plants</b> take in carbon dioxide from the air and water (and a few nutrients) from the soil to build their bodies.</li>"
             "<li><b>Animals</b> eat plants or other animals. They breathe out carbon dioxide and leave wastes.</li>"
             "<li><b>Decomposers</b>, mainly bacteria and fungi, break down dead plants, dead animals and wastes. Earthworms and other soil animals help. "
             "Nutrients go back to the soil and carbon dioxide goes back to the air.</li></ul>"
             + figure(cycle(), "The cycle of matter. Follow the numbered arrows: matter keeps moving among air, soil, plants, animals and decomposers."))
    ex = [("A leaf falls and rots. Where does its matter go?", ["Fungi and bacteria break the leaf down.", "Nutrients go into the soil; carbon dioxide and water go into the air."], "Back into the soil and air, for plants to use again."),
          ("Bread molds in 5 days on a warm, damp counter and in 30 days in the fridge. Why?", ["Mold is a decomposer.", "Decomposers grow faster where it is warm and moist."], "Warmth speeds up decomposers.")]
    mist = ["Thinking dead things just disappear. Decomposers turn them into nutrients and gases.",
            "Thinking plants get their food from the soil. They build their bodies mostly from air and water.",
            "Thinking matter is used up. It cycles and is reused.",
            "Thinking all bacteria and fungi are harmful. Decomposers are needed in every ecosystem."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What decomposers do", B1 + [(g_which_dec, 6), (g_return, 4)]),
        ("The cycle of matter", [(g_arrow, 12), (g_return, 4), (g_which_dec, 4)]),
        ("Compost data", [(g_compost, 10), (g_rot_table, 10)]),
        ("Matter in food webs", [(g_return, 8), (g_arrow, 6), (g_rot_table, 6)]),
        ("Investigations", B5 + [g_compost, g_rot_table, g_arrow]),
    ])
    make("grade-5", "decomposers-and-the-cycle-of-matter", 10, "5-LS2-1",
         "Develop a model to describe the movement of matter among plants, animals, decomposers, and the environment.",
         "Decomposers and the Cycle of Matter",
         "Grade 5 Decomposers Worksheets: Bacteria, Fungi, Compost and the Cycle of Matter",
         "Decomposers",
         "Free Grade 5 science worksheets on decomposers and the cycle of matter (NGSS 5-LS2-1): bacteria, fungi and earthworms, compost data, and how matter moves among plants, animals, soil and air. 100 practice questions with answers.",
         "Decomposers return matter from dead things to the soil and air.",
         "Matter cycles: plants take in air and water, animals eat plants, and bacteria and fungi break down the dead so the matter is used again.",
         body(),
         [("What do decomposers do?", "They break down dead plants, dead animals and wastes. This returns nutrients to the soil and carbon dioxide to the air, so plants can use the matter again."),
          ("What are examples of decomposers?", "Bacteria and fungi, such as mold and mushrooms. Earthworms, pill bugs and millipedes help by breaking dead matter into small pieces."),
          ("Why is the cycle of matter important?", "Matter is not used up. It moves again and again among air, soil, plants, animals and decomposers, so living things always have materials to grow."),
          ("What makes decomposers work faster?", "Warmth and moisture. Food rots faster on a warm, damp counter than in the fridge.")],
         sets)


if __name__ == "__main__":
    main()
