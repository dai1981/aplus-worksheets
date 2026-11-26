# -*- coding: utf-8 -*-
"""
UK Year 3 science: How Water Moves in Plants (Plants)
  python tools/gen_uk_science_y3_how_water_moves_in_plants.py
How water is taken in by roots and carried up the stem in tiny tubes to the leaves and flowers, the coloured-water
celery and white flower investigations (with results to read), wilting and recovering, and water leaving the leaves.
Wrong answers come from real mistakes: "leaves suck water in from the air", "water goes down from the leaves to the
roots", "the colour only goes into the petals because they are white", "a wilted plant is always dead".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61303)
R = U.R
P = People(R)

PATH = ["the soil", "the roots", "the stem", "the leaves and flowers", "the air"]


def g_path():
    if R.random() < 0.4:
        i, j = sorted(R.sample(range(len(PATH)), 2))
        if not once(("pf", i, j)):
            return None
        a, b = PATH[i], PATH[j]
        o = [a, b] if R.random() < 0.5 else [b, a]
        return item("Water moves through a plant. Which does the water pass through first: %s or %s?" % tuple(o), a, [b, "They happen at the same time.", "Water does not pass through either."],
                    "Soil → roots → stem → leaves and flowers → out into the air.")
    i = R.randrange(len(PATH) - 1)
    k = R.random() < 0.5
    if not once(("pa", i, k)):
        return None
    if k:
        a = PATH[i + 1]
        return item("Water moves through a plant. Where does it go after %s?" % PATH[i], a, [x for x in PATH if x not in (a, PATH[i])][:3], "Soil → roots → stem → leaves and flowers → out into the air.")
    a = PATH[i]
    return item("Water moves through a plant. Where was the water just before it reached %s?" % PATH[i + 1], a, [x for x in PATH if x not in (a, PATH[i + 1])][:3], "Soil → roots → stem → leaves and flowers → out into the air.")


DYES = ["red", "blue", "green", "purple"]
PLANTS = [("a stick of celery", "the leaves at the top"), ("a white carnation", "the petals"), ("a white rose", "the petals"),
          ("a white daisy", "the petals"), ("a Chinese cabbage leaf", "the thin lines (veins) in the leaf"), ("a white tulip", "the petals"),
          ("a white lily", "the petals"), ("a stick of celery with its leaves", "the leaves at the top")]


def g_dye():
    who = P.next()[0]
    p, part = R.choice(PLANTS)
    c = R.choice(DYES)
    k = R.choice(["where", "why", "shows", "cut"])
    if not once(("dy", p, k)) or not once(("dc", p, c), 2):
        return None
    intro = "%s stood %s in a jar of water with %s food colouring. " % (who, p, c)
    if k == "where":
        return item(intro + "Where will the %s colour appear after a day?" % c, part, [x for x in ["only at the bottom of the stem", "nowhere, the colour stays in the jar", "in the jar lid", part, "the roots"] if x != part][:3],
                    "The coloured water travels up the stem to the top of the plant.")
    if k == "why":
        return item(intro + "Why does the colour spread up the plant?", "The plant takes up the coloured water through tiny tubes in its stem.", ["The colour floats up through the air.", "The plant paints itself.", "Light carries the colour up."],
                    "The tubes carry water up from the bottom.")
    if k == "shows":
        return item(intro + "What does this investigation show?", "Water travels up the stem to the leaves and flowers.", ["Water travels down from the leaves to the roots.", "Plants do not need water.", "Leaves take in water from the air."],
                    "The colour is a way of seeing where the water goes.")
    return item(intro + "When the stem is cut across, what will %s see?" % who, "small %s dots, which are the ends of the water tubes" % c, ["a hollow, empty stem", "a %s stem all the way through, like paint" % c, "no colour at all" ], "The tubes carry the water up the stem.")


TIMES = [0, 2, 4, 6, 24]


def g_table():
    who = P.next()[0]
    base = R.choice([[0, 2, 4, 6, 15], [0, 1, 3, 5, 14], [0, 2, 5, 7, 16], [0, 1, 2, 4, 12], [0, 3, 5, 8, 18], [0, 2, 3, 6, 13]])
    k = R.choice(["read", "read", "pattern", "diff", "predict"])
    ri = R.randrange(1, 5)
    if not once(("tb", tuple(base), k, ri if k in ("read",) else 0)) or (k == "pattern" and not once(("tp",), 2)):
        return None
    tab = table(["Time (hours)", "Height the colour had climbed up the celery (cm)"], [[str(t), str(h)] for t, h in zip(TIMES, base)])
    intro = tab + "%s put celery in coloured water and measured how far up the colour went. " % who
    if k == "read":
        g = "%d cm" % base[ri]
        return item(intro + "How far had the colour climbed after %d hours?" % TIMES[ri], g, uniq(g, ["%d cm" % x for x in base if x] + ["%d cm" % TIMES[ri]]), "Read across from %d hours." % TIMES[ri])
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The longer the time, the higher the colour climbed.", ["The colour went down over time.", "The colour stayed at the bottom.", "The colour climbed, then disappeared."],
                    "The numbers keep going up.")
    if k == "diff":
        d = base[3] - base[1]
        g = "%d cm" % d
        return item(intro + "How much further did the colour climb between 2 hours and 6 hours?", g, uniq(g, ["%d cm" % base[3], "%d cm" % base[1], "4 cm" if d != 4 else "6 cm", "%d cm" % (base[3] + base[1])]),
                    "%d − %d = %d cm." % (base[3], base[1], d))
    return item(intro + "About how high would you expect the colour to be after 5 hours?", "between %d cm and %d cm" % (base[2], base[3]), ["more than %d cm" % base[4], "0 cm", "less than %d cm" % base[1]],
                "5 hours is between 4 and 6 hours.")


WILT = [("A pot plant's leaves droop on a hot day. What will help it most?", "watering the soil", ["watering the flowers only", "putting it in the dark", "cutting off the roots"], "Roots take up the water."),
        ("A drooping plant is watered. What happens a few hours later?", "It stands up again as water reaches the stem and leaves.", ["It stays drooping for ever.", "It falls apart.", "It turns into a seed."], "Water makes the plant firm."),
        ("Why does a plant droop (wilt) when it does not get enough water?", "There is not enough water in the stem and leaves to keep them firm.", ["It is tired.", "It is too cold.", "Its flowers are too heavy."], "Water keeps plants firm."),
        ("Cut flowers in a vase stay fresh longer if you trim their stems. Why?", "A fresh cut lets water travel up the stem more easily.", ["Short stems need no water.", "It makes the petals open.", "It stops the flowers growing roots."], "Fresh tubes take up water."),
        ("Where does most of the water leave a plant?", "through tiny holes in the leaves, into the air", ["out of the roots", "through the flowers only", "it never leaves"], "Water evaporates from leaves."),
        ("Why do leaves feel cooler than the air on a hot day?", "Water evaporating from them cools them down.", ["Leaves are made of ice.", "Leaves are always in shade.", "Leaves have no water."], "Like sweat."),
        ("A plant in a pot with no drainage holes is watered too much. Why might its roots rot?", "Soggy soil has no air for the roots.", ["Roots like lots of standing water.", "Roots need sugar.", "Water makes roots too warm."], "Roots need air too."),
        ("Why are the tubes in a stem like drinking straws?", "They carry water up from the bottom to the top.", ["They are made of plastic.", "They blow bubbles.", "They carry sunlight."], "A good model."),
        ("A plant is pulled up and its roots are washed clean of soil. Why might it wilt after replanting?", "Many tiny root hairs were damaged, so it takes in less water.", ["Roots do not take in water.", "Clean roots are too heavy.", "Soil is not needed for water."], "Root hairs take in water."),
        ("A tree is very tall. How does water reach the top leaves?", "It travels up tiny tubes in the trunk.", ["Rain falls straight into the top leaves only.", "Birds carry it up.", "It does not reach the top."], "A trunk is a stem."),
        ("Why does a plant in a sunny window need watering more often than one in a shady corner?", "More water evaporates from its leaves.", ["Sunlight drinks the water.", "Shady plants need no water.", "Sunny plants have no roots."], "Warm and sunny: more evaporation."),
        ("Why does a bunch of flowers slowly use up the water in its vase?", "The stems take up water, and it evaporates from the leaves and petals.", ["The vase leaks every time.", "Flowers turn water into soil.", "The water turns into air on its own only at night."], "Water moves up and out.")]


def g_wilt():
    q, a, w, e = R.choice(WILT)
    if not once(("wi", q)):
        return None
    return item(q, a, w, e)


B1 = bank([
    ("Which part of a plant takes in water?", "the roots", ["the flowers", "the leaves", "the petals"], "From the soil."),
    ("Which part of a plant carries water up to the leaves?", "the stem", ["the roots only", "the petals", "the seeds"], "It has tiny tubes inside."),
    ("Which way does water travel in a plant?", "up, from the roots to the leaves", ["down, from the leaves to the roots", "sideways only", "it does not move"], "Roots are at the bottom."),
    ("What are root hairs for?", "taking in water from the soil", ["making flowers", "catching sunlight", "making seeds"], "Tiny hairs on the roots."),
    ("Why is food colouring used in the celery investigation?", "so we can see where the water goes", ["to make the celery tasty", "to feed the celery", "to kill the celery"], "Water is clear."),
    ("What happens to a plant that does not get enough water?", "It wilts (droops).", ["It grows faster.", "It turns blue.", "It makes more flowers."], "Water keeps it firm."),
    ("Where does water go after it reaches the leaves?", "Most of it evaporates into the air.", ["It goes back down to the roots.", "It turns into soil.", "It stays in the leaf for ever."], "Through tiny holes."),
    ("What does a white flower in red water look like after a day?", "Its petals have red streaks.", ["It turns completely white.", "It turns green.", "Nothing changes at all."], "The water reaches the petals."),
])
B5 = bank([
    ("Why should every celery stick in a test be the same length?", "so the only thing that changes is what is being tested", ["to make it look nice", "so it fits in the fridge", "length does not matter"], "Fair test."),
    ("Would celery in a warm room or a cold room take up coloured water faster?", "the warm room", ["the cold room", "both exactly the same", "neither would take any"], "Warmth speeds up evaporation from leaves."),
    ("A flower's stem is split in two, with one half in blue water and one in red water. What will the petals look like?", "partly blue and partly red", ["all purple", "all white", "all green"], "Each tube carries its own water."),
    ("Why would celery with its leaves cut off take up water more slowly?", "Less water evaporates from the top to pull more water up.", ["Leaves are where roots grow.", "Leaves push water down.", "It would take up water faster."], "Leaves help pull water up."),
    ("Why do gardeners water plants in the evening in summer?", "Less water evaporates before the roots can take it in.", ["Plants sleep in the day.", "Water is colder at night.", "Roots only work in the dark."], "Use water well."),
])


def body():
    think = ("<p><b>Water travels up a plant: from the soil, into the roots, up the stem, to the leaves and flowers.</b></p>"
             "<ul><li>The stem has tiny tubes, like straws, that carry water upwards.</li>"
             "<li>Celery or a white flower in coloured water shows where the water goes.</li>"
             "<li>Most water leaves through the leaves into the air. A plant without enough water wilts.</li></ul>")
    ex = [("Celery in blue water. Where does blue appear?", ["Water goes up the stem"], "in the leaves at the top"),
          ("After the roots, where does water go?", ["Up the tubes"], "the stem")]
    mist = ["Thinking leaves take in water from the air.", "Thinking water goes down from the leaves to the roots.", "Thinking a wilted plant is always dead."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Roots and stems", B1 + [(g_path, 8), (g_wilt, 4)]),
        ("The path of water", [(g_path, 6), (g_dye, 8), (g_wilt, 6)]),
        ("Coloured water", [(g_dye, 12), (g_table, 8)]),
        ("Reading results", [(g_table, 16), (g_dye, 4)]),
        ("Thinking it through", B5 + [(g_table, 10), (g_dye, 3), (g_wilt, 2)]),
    ])
    make_uk(3, "how-water-moves-in-plants", 3, "Plants",
            "Investigate the way in which water is transported within plants.",
            "How Water Moves in Plants",
            "Year 3 Science: How Water Moves in Plants Worksheets (Celery and Coloured Water)",
            "Water in Plants",
            "Free Year 3 science worksheets on how water moves in plants: roots, stems and leaves, the celery and coloured water investigation, wilting and evaporation. 100 questions with answers.",
            "Roots, up the stem, to the leaves.",
            "Tiny tubes in the stem carry water up from the roots.",
            body(),
            [("How does water get into a plant?", "The roots take in water from the soil. It then travels up tiny tubes in the stem to the leaves and flowers."),
             ("What does the celery investigation show?", "When celery stands in coloured water, the colour travels up the stem to the leaves. This shows that water moves up through the stem."),
             ("Why does a plant wilt?", "When there is not enough water in the stem and leaves, they cannot stay firm, so they droop. Watering the soil usually helps them stand up again.")],
            sets)


if __name__ == "__main__":
    main()
