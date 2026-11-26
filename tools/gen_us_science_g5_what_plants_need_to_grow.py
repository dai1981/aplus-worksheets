# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Plants Get Matter from Air and Water (5-LS1-1)
  python tools/gen_us_science_g5_what_plants_need_to_grow.py
Plants need light, water, air and a few nutrients. The matter a plant uses to grow comes mostly
from carbon dioxide in the air and water, not from the soil. Evidence: the willow tree experiment
(the soil barely changes mass while the tree gains a lot), plants that grow without soil
(hydroponics), and plant investigations with tables of results.
Wrong answers come from real mistakes: "plants eat soil", "plant food from the store is the plant's
food", "plants get mass from sunlight".
"""
from sci_common import Unit, item, bank, lesson, make, fig, table, bar_chart, People

U = Unit(50108)
R = U.R
P = People(R)
PLANTS = ["bean plant", "sunflower", "tomato plant", "pea plant", "radish", "corn plant", "basil plant", "lettuce plant"]


def kg(v):
    return ("%.1f kg" % v) if v != int(v) else "%d kg" % v


# ------------------------------------------------------------ makers
def g_willow():
    s0 = R.choice([80, 90, 100, 120])
    loss = R.choice([0.1, 0.2])
    t0 = R.choice([2, 3, 4])
    t1 = t0 + R.choice([60, 65, 70, 72, 75])
    yrs = R.choice([4, 5, 6])
    tab = table(["", "Start", "After %d years" % yrs], [["Mass of tree", kg(t0), kg(t1)], ["Mass of dry soil", kg(s0), kg(s0 - loss)]])
    ask = R.choice(["gain", "loss", "concl"])
    intro = tab + "A willow tree was planted in a pot of soil and given only water for %d years. " % yrs
    if ask == "gain":
        return item(intro + "How much mass did the tree gain?", kg(t1 - t0), [kg(t1), kg(loss), kg(t1 + t0)], "%s − %s = %s." % (kg(t1), kg(t0), kg(t1 - t0)))
    if ask == "loss":
        return item(intro + "How much mass did the soil lose?", kg(loss), [kg(t1 - t0), "0 kg, it gained mass", kg(s0)],
                    "%s − %s = %s. That is tiny compared with the tree's gain of %s." % (kg(s0), kg(s0 - loss), kg(loss), kg(t1 - t0)))
    return item(intro + "What is the best conclusion?", "Most of the tree's new mass did not come from the soil.",
                ["The tree's mass came from the soil.", "The tree did not grow.", "Sunlight added mass to the tree."],
                "The tree gained %s, but the soil lost only %s. The matter came mostly from air (carbon dioxide) and water." % (kg(t1 - t0), kg(loss)))


def g_height():
    pl = R.choice(PLANTS)
    var = R.choice([("water each day", "no water"), ("sunny window", "dark closet"), ("open air", "sealed jar with no carbon dioxide")])
    a = [R.randint(2, 4)]
    b = [a[0]]
    for _ in range(3):
        a.append(a[-1] + R.randint(3, 6))
        b.append(b[-1] + R.randint(0, 1))
    tab = table(["Day", "0", "7", "14", "21"], [["Plant A (%s)" % var[0]] + ["%d cm" % v for v in a], ["Plant B (%s)" % var[1]] + ["%d cm" % v for v in b]])
    need = {"water each day": "water", "sunny window": "light", "open air": "carbon dioxide from the air"}[var[0]]
    ask = R.choice(["need", "diff"])
    p = P.next()
    if ask == "need":
        return item(tab + "%s grew two %ss. Everything was the same except one thing. What does the data show?" % (p[0], pl), "The plants need %s to grow well." % need,
                    [x for x in ["The plants need water to grow well.", "The plants need light to grow well.", "The plants need carbon dioxide from the air to grow well.",
                                 "The plants grow best with less of everything."] if need not in x][:3],
                    "Plant A grew from %d cm to %d cm; Plant B hardly grew. The only difference was %s." % (a[0], a[-1], need))
    return item(tab + "How much taller was Plant A than Plant B on day 21?", "%d cm" % (a[-1] - b[-1]), ["%d cm" % a[-1], "%d cm" % b[-1], "%d cm" % (a[-1] + b[-1])],
                "%d − %d = %d cm." % (a[-1], b[-1], a[-1] - b[-1]))


def g_hydro():
    pl = R.choice(["lettuce", "tomatoes", "basil", "strawberries", "spinach"])
    return item("A farm grows %s with their roots in water and a few nutrients, and no soil at all. The plants grow big and healthy. What does this show?" % pl,
                "Plants do not need soil to get the matter they use to grow.", ["Plants eat water only.", "Soil makes plants smaller.", "The plants are not really growing."],
                "This is called hydroponics. The plants get matter from air and water and only small amounts of nutrients.")


def g_mass_bar():
    m0 = R.randint(5, 15)
    m1 = m0 + R.randint(60, 140)
    s = R.randint(1, 3)
    ch = bar_chart(["seed", "plant"], [m0, m1], "grams", "bar graph: mass of a seed and of the plant it grew into", ymax=(m1 // 50 + 1) * 50, step=50, w=200)
    return item(fig(ch) + "A seed grew into a plant in a pot. The soil lost only about %d g. Where did most of the plant's added mass come from?" % s,
                "carbon dioxide from the air and water", ["the soil", "sunlight", "the seed"],
                "The plant gained about %d g but the soil lost only %d g. Plants build their bodies from carbon dioxide and water." % (m1 - m0, s))


B1 = bank([
    ("What do plants need to grow?", "light, water, air and a few nutrients", ["only soil", "only sunlight", "darkness and soil"],
     "Plants need light for energy, water and carbon dioxide (from air) for matter, and small amounts of nutrients."),
    ("Where does most of the matter that makes up a plant's body come from?", "carbon dioxide from the air and water", ["the soil", "sunlight", "plant food from a store"],
     "Plants combine carbon dioxide and water to make sugar, which they use to build their bodies."),
    ("Which gas do plants take in from the air to grow?", "carbon dioxide", ["oxygen only", "helium", "smoke"],
     "Leaves take in carbon dioxide through tiny openings."),
    ("Sunlight gives plants", "energy to make food", ["most of their mass", "water", "soil"],
     "Light is energy, not matter. The matter comes from air and water."),
    ("Through which part do most plants take in water?", "roots", ["flowers", "seeds", "bark only"],
     "Roots take in water, which moves up the stem to the leaves."),
    ("Through which part do plants take in carbon dioxide?", "leaves", ["roots", "flowers", "seeds"],
     "Tiny openings in leaves let carbon dioxide in."),
    ("Soil gives plants", "small amounts of nutrients and a place to anchor their roots", ["most of their mass", "energy", "carbon dioxide"],
     "Soil helps, but it is not where most of a plant's matter comes from."),
    ("Plants make their own food. What is the food they make?", "sugar", ["soil", "salt", "protein from insects"],
     "During photosynthesis plants make sugar from carbon dioxide and water."),
    ("What gas do plants give off when they make food?", "oxygen", ["carbon dioxide", "smoke", "helium"],
     "Plants release oxygen, which animals breathe."),
    ("A huge oak tree grew from a small acorn. Where did most of its wood come from?", "carbon dioxide from the air and water", ["the soil around it", "the acorn", "sunlight turned into wood"],
     "Wood is built mostly from carbon dioxide and water."),
])
B5 = bank([
    ("Ava wants to test if plants need light to grow. Which plan is best?", "Grow two identical plants with the same water and soil, one in light and one in the dark.", ["Put one plant in light and give it more water.", "Use one plant only.", "Put both plants in the dark."],
     "Only the light should be different."),
    ("Why should Ava use several plants in each group, not just one?", "One plant might be sick or different, so more plants make the results more reliable.", ["To use up all the seeds.", "So the plants can talk.", "Because one plant cannot grow."],
     "Many plants show whether the result really comes from the variable being tested."),
    ("Leo weighs a pot of dry soil before planting a seed and again 3 months later when the plant is big. The soil mass is almost the same. What should he conclude?", "The plant's mass did not come mostly from the soil.", ["The plant ate the soil.", "The scale is broken.", "Plants get mass from the pot."],
     "If the plant took its mass from the soil, the soil would have lost a lot of mass."),
    ("A sealed jar with a plant and no carbon dioxide is kept in light with water. The plant does not grow. Why?", "It has no carbon dioxide to make food.", ["It has too much light.", "It has too much water.", "Jars stop sunlight."],
     "Without carbon dioxide, the plant cannot make sugar to build its body."),
    ("Which claim is supported by the evidence that plants grow in water with no soil?", "Plants get the materials for growth chiefly from air and water.", ["Plants need soil to live.", "Plants get energy from water.", "Soil is plant food."],
     "Hydroponic plants grow without soil, so soil cannot be the main source of their matter."),
    ("“Plant food” sold in stores is added to soil. What does it actually give plants?", "nutrients, like vitamins for people", ["most of the plant's mass", "energy", "carbon dioxide"],
     "Plants make their own food. The store product only adds small amounts of nutrients."),
])


def body():
    think = ("<p>Plants need <b>light, water, air and a few nutrients</b>. But where does the matter that makes a plant bigger come from?</p>"
             "<p>Plants build their bodies mostly from <b>carbon dioxide from the air</b> and <b>water</b>. Using energy from light, they make sugar "
             "(photosynthesis), and they use the sugar to build leaves, stems, roots and fruit. Soil gives only small amounts of nutrients.</p>"
             + table(["", "Start", "After 5 years"], [["Mass of willow tree", "2 kg", "74 kg"], ["Mass of dry soil", "90 kg", "89.9 kg"]])
             + "<p>In a famous experiment, a willow tree gained more than 70 kg while the soil lost almost nothing. The new matter came from air and water.</p>")
    ex = [("A plant gains 120 g while the soil in its pot loses 2 g. Where did most of the 120 g come from?", ["2 g is tiny compared with 120 g.", "The rest came from carbon dioxide and water."], "air and water"),
          ("Two identical plants get the same water and soil. One is in a sunny window and one is in a dark closet. What is being tested?", ["Only the light is different."], "whether plants need light")]
    mist = ["Thinking plants “eat” soil. Soil barely loses mass as a plant grows.",
            "Thinking sunlight becomes the plant's matter. Light gives energy, not matter.",
            "Thinking “plant food” from a store is the plant's food. Plants make their own food (sugar).",
            "Changing more than one thing in a plant investigation."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What plants need", B1 + [(g_hydro, 5), (g_mass_bar, 5)]),
        ("The willow tree experiment", [(g_willow, 14), (g_mass_bar, 6)]),
        ("Plant investigations", [(g_height, 14), (g_hydro, 6)]),
        ("Data and evidence", [(g_willow, 7), (g_height, 7), (g_mass_bar, 6)]),
        ("Plan and explain", B5 + [g_willow, g_height, g_hydro, g_mass_bar]),
    ])
    make("grade-5", "what-plants-need-to-grow", 8, "5-LS1-1",
         "Support an argument that plants get the materials they need for growth chiefly from air and water.",
         "Plants Get Matter from Air and Water",
         "Grade 5 Plant Growth Worksheets: What Plants Need, Air, Water and the Willow Tree",
         "What Plants Need",
         "Free Grade 5 science worksheets on what plants need to grow (NGSS 5-LS1-1): light, water, air and nutrients, the willow tree experiment, hydroponics and plant investigations. 100 practice questions with answers.",
         "Plants build their bodies mostly from air and water.",
         "Light gives energy. Carbon dioxide from the air and water give the matter. Soil adds only a few nutrients.",
         body(),
         [("Where do plants get the materials to grow?", "Mostly from carbon dioxide in the air and from water. Soil gives only small amounts of nutrients."),
          ("Do plants get their food from the soil?", "No. Plants make their own food (sugar) from carbon dioxide and water using energy from light."),
          ("What was the willow tree experiment?", "A willow tree grew in a pot for 5 years with only water added. The tree gained about 74 kg, but the soil lost only a tiny amount, so the tree's mass did not come from the soil."),
          ("Can plants grow without soil?", "Yes. In hydroponics, plants grow with their roots in water and a few added nutrients.")],
         sets)


if __name__ == "__main__":
    main()
