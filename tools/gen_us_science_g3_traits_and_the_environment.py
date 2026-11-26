# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Traits and the Environment (3-LS3-2)
  python tools/gen_us_science_g3_traits_and_the_environment.py
Traits can be influenced by the environment: plants that get too little water or sunlight grow smaller
or paler; plants in poor soil grow less; a dog that is overfed gets heavier; flamingos are pink from the
food they eat; hydrangea flower color changes with the soil; a person who exercises gets stronger.
Students use evidence (plant growth data) to support the explanation.
Wrong answers come from real mistakes: "all traits come only from parents", "the same seeds always grow
the same no matter what", "a plant in the dark grows greener".
"""
from sci_common import Unit, item, bank, lesson, make, fig, bar_chart, table, People

U = Unit(30108)
R = U.R
P = People(R)
PLANTS = ["bean", "sunflower", "pea", "radish", "corn", "tomato", "marigold", "basil"]
FACTORS = [("sunlight", ["full sun", "some shade", "dark closet"]), ("water", ["water every day", "water once a week", "no water"]),
           ("soil", ["rich soil", "sandy soil", "gravel"]), ("space", ["one plant per pot", "five plants per pot", "ten plants per pot"])]


def g_bar():
    plant = R.choice(PLANTS)
    fac, levels = R.choice(FACTORS)
    hs = sorted(R.sample(range(2, 30), 3), reverse=True)
    order = list(range(3))
    R.shuffle(order)
    ch = bar_chart([levels[i] for i in order], [hs[i] for i in order], "height (cm)", "bar graph of plant heights", ymax=30, step=5, w=330)
    p = P.next()
    k = R.choice(["tallest", "why", "same"])
    if k == "tallest":
        return item(fig(ch) + "%s grew %s plants from seeds of the same parent plant, changing only the %s. Which group grew tallest?" % (p[0], plant, fac), levels[0],
                    levels[1:] + ["They all grew the same."], "The %s group grew to %d cm." % (levels[0], hs[0]))
    if k == "why":
        return item(fig(ch) + "All of %s's %s seeds came from the same parent plant. Why did the plants grow to different heights?" % (p[0], plant),
                    "The environment (%s) was different." % fac, ["They inherited different heights.", "Some seeds were tired.", "The bar graph is wrong."],
                    "Same parents, different %s: the environment changed how tall they grew." % fac)
    return item(fig(ch) + "In %s's test of %s plants, what had to stay the same?" % (p[0], plant), "the kind of seed, the pots and everything except the %s" % fac,
                ["only the %s" % fac, "nothing", "the height of the plants"], "Only one thing (the %s) should change in a fair test." % fac)


EXAMPLES = [("A sunflower grown in a dark closet", "is pale and thin", "too little sunlight"),
            ("A tomato plant that gets little water", "has small, dry leaves", "too little water"),
            ("A flamingo that eats lots of shrimp", "has pink feathers", "the food it eats"),
            ("A hydrangea bush in some soils", "has blue flowers instead of pink", "the kind of soil"),
            ("A dog that is fed too much and does not exercise", "becomes overweight", "too much food and too little exercise"),
            ("A person who lifts weights often", "has stronger muscles", "exercise"),
            ("A tree on a windy hilltop", "grows bent to one side", "the strong wind"),
            ("A plant crowded with many other plants", "grows smaller", "not enough space and nutrients"),
            ("A corn plant in poor, sandy soil", "grows short with few ears of corn", "poor soil"),
            ("A goldfish kept in a tiny bowl", "stays smaller", "too little space"),
            ("A person who is out in the sun often", "has tanned skin", "sunlight"),
            ("A pine tree high on a cold mountain", "grows short and twisted", "the cold and wind")]


def g_cause():
    a, b, c = R.choice(EXAMPLES)
    kw = {w.strip(",") for w in c.split() if len(w) > 3}
    others = [x[2] for x in EXAMPLES if x[2] != c and not (kw & {w.strip(",") for w in x[2].split()}) and not ("sun" in c and "sun" in x[2])]
    p = P.next()
    return item("%s notices that %s %s. What in the environment caused this?" % (p[0], a[0].lower() + a[1:], b), c, R.sample(others, 2) + ["only the traits from its parents"], "The environment affected this trait: %s." % c)


def g_both():
    rows = [("A rabbit's ear shape", "parents"), ("A plant's height", "both"), ("A cat's eye color", "parents"), ("A person's weight", "both"),
            ("A flower's number of petals", "parents"), ("A tree's height", "both"), ("A dog's fur color", "parents"), ("A flamingo's pink color", "environment"),
            ("A child's height", "both"), ("A bird's beak shape", "parents"), ("A tomato plant's number of tomatoes", "both"), ("A scar", "environment")]
    t, k = R.choice(rows)
    txt = {"parents": "mostly inherited from parents", "environment": "mostly caused by the environment", "both": "both inherited and affected by the environment"}
    p = P.next()
    return item("%s is making a chart of traits. What mostly decides “%s”?" % (p[0], t.lower()), txt[k],
                [txt[x] for x in txt if x != k] + ["only luck"], "%s is %s." % (t, txt[k]))


B1 = bank([
    ("Can the environment change a living thing's traits?", "Yes. Things like sunlight, water, food and soil can change some traits.", ["No, all traits come only from parents.", "Only for animals.", "Only for plants."],
     "Some traits are affected by the environment."),
    ("Two bean seeds from the same plant are grown in sun and in a dark closet. Which plant will be greener and stronger?", "the plant in the sun", ["the plant in the closet", "They will be the same.", "Neither will grow at all."],
     "Plants need light to grow well."),
    ("Why are flamingos pink?", "The shrimp and algae they eat make their feathers pink.", ["They are painted.", "Pink is the color of all birds.", "The sun turns them pink."],
     "Their food affects their color."),
    ("What happens to a plant that gets too little water?", "It wilts and grows less.", ["It grows faster.", "It turns blue.", "It grows extra flowers."], "Water is part of the plant's environment."),
    ("Identical twins grow up in different places. One eats more healthy food and exercises more. What might be different?", "their weight and strength", ["their eye color", "their blood type", "their ear shape"],
     "Weight and strength can be affected by the environment."),
    ("Which trait is affected by the environment?", "how tall a plant grows", ["the color of a cat's eyes", "the shape of a rabbit's ears", "the number of legs on an insect"],
     "Height depends on water, light and soil, not just parents."),
    ("What is the environment?", "everything around a living thing, like light, water, soil, food and weather", ["only the parents", "only the house it lives in", "only the food"],
     "The environment can affect traits."),
    ("Why might the same kind of tree grow tall in a forest but short on a windy mountain?", "The environment is different.", ["The trees have different parents always.", "Mountain trees are lazy.", "Wind makes trees taller."],
     "Wind and cold can keep trees short."),
])
B5 = bank([
    ("Ava wants to test if fertilizer changes how tall radish plants grow. What should she change?", "only whether the plants get fertilizer", ["the seeds and the fertilizer", "the pots and the water", "nothing"],
     "Change one thing for a fair test."),
    ("Leo grows two groups of seeds from the same parent. One group gets fertilizer and grows taller. What does this show?", "The environment can affect a trait like height.", ["Height is only inherited.", "Fertilizer changes the parents.", "Seeds choose their height."],
     "Same parents, different results means the environment matters."),
    ("Mia measures 3 plants in each group. Why not just 1?", "to make sure the results are not just one unusual plant", ["to use more pots", "to make the plants taller", "because plants are lonely"],
     "More samples give better evidence."),
    ("Noah's hydrangea had pink flowers. After he changed the soil, the flowers turned blue. What caused the change?", "the soil", ["the parent plant", "the color of the pot", "the day of the week"],
     "Soil affects hydrangea flower color."),
    ("A farmer's corn grows taller in a rainy year than in a dry year. Which explanation is best?", "More water helped the corn grow taller.", ["The corn inherited new parents.", "Rain makes corn shorter.", "Corn does not need water."],
     "Water is part of the environment."),
])


def body():
    think = ("<p>Living things inherit many traits from their parents. But the <b>environment</b> can also change some traits.</p>"
             "<ul><li>Plants that get too little <b>light</b> or <b>water</b> grow smaller, paler or weaker.</li>"
             "<li>Plants in poor <b>soil</b> or crowded pots grow less.</li>"
             "<li>Animals that eat too much or too little change size; flamingos turn pink from their <b>food</b>.</li>"
             "<li>People who exercise get stronger.</li></ul>"
             "<p>If seeds from the <b>same parent</b> grow differently, the difference was caused by the environment.</p>")
    ex = [("Bean seeds from one plant grow 25 cm in sun and 8 cm in shade. Why?", ["Same parents.", "Different light."], "The environment (light) affected their height."),
          ("Is a flamingo's pink color inherited or from the environment?", ["It comes from its food."], "from the environment")]
    mist = ["Thinking all traits come only from parents.",
            "Thinking seeds from the same plant always grow exactly the same.",
            "Changing more than one thing in a plant test."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The environment affects traits", B1 + [(g_cause, 6), (g_both, 6)]),
        ("What caused the change?", [(g_cause, 12), (g_both, 8)]),
        ("Plant growth data", [(g_bar, 14), (g_cause, 6)]),
        ("Inherited or environment?", [(g_both, 10), (g_bar, 10)]),
        ("Investigations", B5 + [g_bar, g_cause, g_both]),
    ])
    make("grade-3", "traits-and-the-environment", 8, "3-LS3-2",
         "Use evidence to support the explanation that traits can be influenced by the environment.",
         "Traits and the Environment",
         "Grade 3 Traits and Environment Worksheets: How Light, Water, Soil and Food Change Traits",
         "Traits and the Environment",
         "Free Grade 3 science worksheets on how the environment affects traits (NGSS 3-LS3-2): plants grown with different light, water and soil, flamingos and food, and plant growth data. 100 practice questions with answers.",
         "The environment can change some traits.",
         "Seeds from the same parent can grow differently if they get different light, water, soil or food.",
         body(),
         [("How can the environment affect traits?", "Light, water, soil, food and exercise can change traits like height, color, size and strength."),
          ("Why are flamingos pink?", "The shrimp and algae they eat contain colors that turn their feathers pink."),
          ("How can you show that the environment affects a trait?", "Grow seeds from the same parent plant in different conditions, change only one thing, and compare how they grow.")],
         sets)


if __name__ == "__main__":
    main()
