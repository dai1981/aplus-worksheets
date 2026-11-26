# -*- coding: utf-8 -*-
"""
UK Year 3 science: What Plants Need to Grow (Plants)
  python tools/gen_uk_science_y3_what_plants_need_to_grow.py
The requirements of plants for life and growth (air, light, water, nutrients from soil, room to grow and warmth),
how they vary from plant to plant, what seeds need to start growing, and reading results from simple
investigations (plants in the dark, with no water, with different amounts of water).
Wrong answers come from real mistakes: "plants need soil to make food", "more water is always better",
"seeds need light to start growing", "plants in the dark just stop and stay the same".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, bar_chart, fig, People, once
from sci_phys import uniq

U = Unit(61302)
R = U.R
P = People(R)

NEED = ["light", "water", "air", "nutrients from the soil", "room to grow", "warmth"]
NOT = ["chocolate", "music", "sugar lumps", "plastic", "salt", "noise", "fizzy drinks", "darkness all day"]


def g_need():
    a = R.choice(NEED)
    w = R.sample(NOT, 3)
    if not once(("nd", a), 4):
        return None
    o = sorted([a] + w)
    return item("Which of these does a plant need to grow well: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Plants need light, water, air, nutrients, room and warmth.")


WHAT = [("Leaves turn yellow and the stem grows tall, thin and pale.", "light"), ("The leaves droop and the soil is dry.", "water"),
        ("Many seedlings are packed tightly in one small pot and stay small.", "room to grow"), ("A plant in a cold shed grows very slowly in winter.", "warmth"),
        ("A plant has been in the same old soil for years and its leaves are small and pale.", "nutrients from the soil"),
        ("A plant has been on a dark shelf in the corner of a room for weeks.", "light"), ("A plant on a hot windowsill has crispy brown leaves and dry soil.", "water"),
        ("Two sunflowers in a tiny pot grow much smaller than one sunflower in a big pot.", "room to grow"),
        ("Tomato plants put outside in early spring stop growing on frosty nights.", "warmth"),
        ("A plant pushed behind a thick curtain all summer has long, weak, pale shoots.", "light"),
        ("Basil seedlings sown very close together are thin and weak, and many die.", "room to grow"),
        ("A plant left while its owners were on holiday for three weeks has floppy leaves.", "water"),
        ("A pot plant grown in sand with no compost has small, yellowish leaves.", "nutrients from the soil")]


def g_what():
    s, a = R.choice(WHAT)
    if not once(("wh", s)):
        return None
    return item("%s What is the plant probably not getting enough of?" % s, a, [x for x in ["light", "water", "room to grow", "warmth", "nutrients from the soil"] if x != a][:3] if a != "light" else ["water", "room to grow", "nutrients from the soil"],
                "Look at the clue: pale and stretched means not enough light; drooping means not enough water.")


DAYS = [0, 3, 6, 9, 12]


def g_test():
    who = P.next()[0]
    var = R.choice(["light", "water"])
    if var == "light":
        groups = ["in a sunny place", "in a dark cupboard"]
        good = [3, 5, 7, 9, 11]
        bad = [3, 4, 4, 3, 2]
        col, unit, what = "number of green leaves", "%d leaves", "How many green leaves did"
    else:
        groups = ["watered every day", "never watered"]
        good = [3, 5, 7, 9, 11]
        bad = [3, 4, 4, 3, 2]
        col, unit, what = "height in cm", "%d cm", "How tall was"
    sc = R.choice([1, 1, 2])
    good = [x * sc for x in good]
    bad = [x * sc for x in bad]
    k = R.choice(["read", "best", "diff", "change", "same", "concl"])
    ri = R.randrange(1, 5)
    if not once(("te", var, sc, k, ri if k in ("read", "diff") else 0)) or (k not in ("read", "diff") and not once(("tk", var, k))):
        return None
    tab = table(["Day"] + ["Plant " + g + " (%s)" % col for g in groups], [[str(d), str(a), str(b)] for d, a, b in zip(DAYS, good, bad)])
    intro = tab + "%s grew two of the same kind of plant: one %s and one %s. " % (who, groups[0], groups[1])
    if k == "read":
        g = unit % bad[ri]
        if var == "light":
            q = "How many green leaves did the plant %s have on day %d?" % (groups[1], DAYS[ri])
        else:
            q = "How tall was the plant %s on day %d?" % (groups[1], DAYS[ri])
        return item(intro + q, g, uniq(g, [unit % good[ri], unit % (bad[ri] + 2 * sc), unit % DAYS[ri], unit % bad[0]]), "Read across from day %d." % DAYS[ri])
    if k == "best":
        return item(intro + "Which plant grew better?", "the plant " + groups[0], ["the plant " + groups[1], "They grew the same.", "Neither plant grew at all."], "Its results kept going up.")
    if k == "diff":
        d = good[ri] - bad[ri]
        g = unit % d
        q = ("On day %d, how many more green leaves did the plant %s have?" if var == "light" else "On day %d, how much taller was the plant %s?") % (DAYS[ri], groups[0])
        return item(intro + q, g, uniq(g, [unit % good[ri], unit % bad[ri], unit % (good[ri] + bad[ri]), unit % (d + 1)]),
                    "%d − %d = %d." % (good[ri], bad[ri], d))
    if k == "change":
        return item(intro + "What did %s change in this test?" % who, "how much %s the plants got" % var, ["the kind of plant", "the size of the pots", "the " + col.replace(" in cm", "")], "Only one thing is changed in a fair test.")
    if k == "same":
        return item(intro + "Which should %s keep the same for a fair test?" % who, "the kind of plant, the pot and the soil", ["how much %s the plants got" % var, "the " + col.replace(" in cm", ""), "nothing at all"], "Keep everything else the same.")
    return item(intro + "What does this test show?", "Plants need %s to grow well." % var, ["Plants grow better %s." % groups[1], "Plants do not need %s." % var, "All plants grow in the same way."], "Compare the two plants.")


def g_amount():
    who = P.next()[0]
    amt = [0, 25, 50, 100, 400]
    base = [2, 9, 12, 14, 4]
    sc = R.choice([1, 2])
    h = [x * sc for x in base]
    k = R.choice(["best", "most", "none", "pattern"])
    if not once(("am", sc, k)):
        return None
    ch = bar_chart(["%d ml" % a for a in amt], h, "cm", "bar chart of plant height for each amount of water a day", title="Height after 3 weeks (cm)")
    intro = fig(ch) + "%s gave five bean plants different amounts of water each day. " % who
    if k == "best":
        return item(intro + "Which amount of water gave the tallest plant?", "100 ml", ["400 ml", "0 ml", "25 ml"], "The tallest bar is at 100 ml.")
    if k == "most":
        return item(intro + "What happened to the plant given 400 ml a day?", "It grew badly, because too much water is not good for roots.", ["It grew the tallest.", "It grew exactly like the 100 ml plant.", "It turned into a tree."],
                    "Waterlogged soil has no air for the roots.")
    if k == "none":
        return item(intro + "Why did the plant with 0 ml grow so little?", "It had no water.", ["It had too much water.", "It had too much light.", "It had no soil."], "Plants need water.")
    return item(intro + "What do the results show?", "Plants need some water, but too much is bad for them.", ["The more water, the taller the plant, always.", "Water makes no difference.", "Plants grow best with no water."],
                "The bars go up and then down again.")


SEED = [("water", "yes"), ("warmth", "yes"), ("air", "yes"), ("light", "no"), ("soil", "no")]


def g_seed():
    n, a = R.choice(SEED)
    if not once(("se", n)):
        return None
    ans = "Yes, a seed needs %s to start growing." % n if a == "yes" else "No. A seed has food stored inside, so it can start growing without %s." % n
    return item("Does a seed need %s to start growing (germinate)?" % n, ans,
                ["No, a seed never needs %s." % n if a == "yes" else "Yes, a seed cannot start without %s." % n, "Only on Mondays.", "Only if it is a big seed."],
                "Seeds need water, warmth and air to germinate. They use food stored inside them until their leaves grow.")


VARY = [("a cactus", "very little water"), ("a water lily", "lots of water, growing in a pond"), ("a fern on a forest floor", "shade, not bright sunlight"),
        ("a sunflower", "lots of bright sunlight"), ("a seaweed", "salty sea water")]


def g_vary():
    p, n = R.choice(VARY)
    if not once(("va", p)):
        return None
    return item("Different plants need different amounts of things. What does %s grow best with?" % p, n, R.sample([x[1] for x in VARY if x[1] != n], 3), "Plants are suited to where they live.")


B1 = bank([
    ("What do plants use light for?", "to make their own food in their leaves", ["to keep their roots cool", "to drink water", "to make soil"], "No light, no food."),
    ("Why do plants need water?", "to stay firm, carry nutrients and help make food", ["to make them heavy", "to scare insects", "they do not need water"], "Wilting means thirsty."),
    ("Which part of the plant takes in nutrients from the soil?", "the roots", ["the flowers", "the leaves", "the petals"], "Dissolved in water."),
    ("What does a gardener add to soil to give plants more nutrients?", "compost or fertiliser", ["sand", "sugar", "salt"], "Plant food."),
    ("Why should seedlings be planted with space between them?", "so each has room to grow and enough light, water and nutrients", ["so they can talk", "so they grow smaller", "to make the soil warm"], "Crowded plants compete."),
    ("Which season do most plants in the UK grow fastest?", "spring and summer", ["winter", "only in snow", "they never grow"], "More light and warmth."),
    ("Do plants need air?", "Yes, they take in air through tiny holes in their leaves.", ["No, never.", "Only at night through flowers.", "Only seeds need air."], "They use a gas in the air to make food."),
    ("Why do house plants lean towards a window?", "They grow towards the light.", ["They want to look outside.", "The wind pushes them.", "The pot is heavy."], "Turn them to keep them straight."),
])
B5 = bank([
    ("Why is a plant in a dark cupboard tall, thin and pale?", "It stretches to try to find light and cannot make its green colour well.", ["It is very healthy.", "It has too much light.", "It has too many nutrients."], "Pale and stretched means too little light."),
    ("Can plants grow without soil?", "Yes, if their roots get water with nutrients in it.", ["No, never.", "Only in the dark.", "Only if they are given sugar."], "Soil gives nutrients and support."),
    ("Why do farmers in the UK use greenhouses?", "to keep plants warm and grow them for longer each year", ["to keep the plants in the dark", "to stop them getting water", "to keep birds warm"], "Warmth speeds growth."),
    ("Why do seeds not need light to start growing?", "They have stored food inside to use until their leaves grow.", ["They cannot see.", "They grow only at night forever.", "Light kills seeds."], "Leaves come later."),
    ("Why should you not water a cactus every day?", "It is suited to dry places, and too much water rots its roots.", ["It hates water completely.", "Cactuses need no water ever.", "Water makes it too tall."], "Different plants, different needs."),
])


def body():
    think = ("<p><b>Plants need light, water, air, nutrients, room to grow and warmth.</b></p>"
             "<ul><li>Light lets leaves make food. Water and nutrients come in through the roots.</li>"
             "<li>Too little or too much of something can harm a plant. Different plants need different amounts.</li>"
             "<li>Seeds need water, warmth and air to start growing, but not light.</li></ul>")
    ex = [("A plant is pale and thin. Missing?", ["Pale and stretched"], "light"),
          ("Leaves droop, soil dry. Missing?", ["Drooping"], "water")]
    mist = ["Thinking plants get their food from the soil.", "Thinking more water is always better.", "Thinking seeds need light to start growing."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What plants need", B1 + [(g_need, 12)]),
        ("Spot the problem", [(g_what, 8), (g_need, 7), (g_seed, 3), (g_vary, 2)]),
        ("Plant growth tests", [(g_test, 20)]),
        ("Seeds and different plants", [(g_seed, 2), (g_vary, 3), (g_amount, 5), (g_test, 6), (g_what, 4)]),
        ("Thinking about growth", B5 + [(g_test, 9), (g_amount, 3), (g_what, 3)]),
    ])
    make_uk(3, "what-plants-need-to-grow", 2, "Plants",
            "Explore the requirements of plants for life and growth (air, light, water, nutrients from soil, and room to grow) and how they vary from plant to plant.",
            "What Plants Need to Grow",
            "Year 3 Science: What Plants Need to Grow Worksheets (Light, Water, Nutrients)",
            "What Plants Need",
            "Free Year 3 science worksheets on what plants need to grow: light, water, air, nutrients, room and warmth, seeds, and simple plant growth tests. 100 questions with answers.",
            "Light, water, air, nutrients, room.",
            "Too little or too much of something can harm a plant.",
            body(),
            [("What do plants need to grow?", "Plants need light, water, air, nutrients from the soil, room to grow and warmth."),
             ("What happens to a plant with no light?", "It cannot make food. It grows tall, thin and pale as it stretches to find light, and in the end it dies."),
             ("Do seeds need light to grow?", "Not at first. A seed needs water, warmth and air to start growing. It uses food stored inside it until its leaves grow and can use light.")],
            sets)


if __name__ == "__main__":
    main()
