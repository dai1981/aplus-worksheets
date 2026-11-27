# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Plant transport system (Systems)
  python tools/gen_sg_science_p5_plant_transport_system.py
Water-carrying tubes carry water and mineral salts from the roots up the stem to all parts of the plant;
food-carrying tubes carry food made in the leaves to all parts. Water is lost from the leaves (so more is drawn up).
Ring-barking removes the food-carrying tubes in the outer layer: the part above the ring swells with food and the roots
starve, so the tree eventually dies. Coloured-water and ring-barking experiments; UK Year 3 water-in-plants questions reused.
Wrong answers come from real mistakes: "food is carried only upwards", "water-carrying tubes carry food",
"ring-barking stops water reaching the leaves at once", "roots make food".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63506)
R = U.R
P = People(R)
WM = use(U, "gen_uk_science_y3_how_water_moves_in_plants", drop=["winter"])

TUBES = {"water-carrying tubes": "water and mineral salts from the roots to the other parts", "food-carrying tubes": "food from the leaves to the other parts"}


def g_which():
    k = R.choice(["water", "minerals", "food", "sugar to fruit", "food to roots", "water to leaves", "water to flowers", "food to seeds"])
    a = "food-carrying tubes" if k.startswith(("food", "sugar")) else "water-carrying tubes"
    if not once(("wh", k)):
        return None
    q = {"water": "Which tubes carry water up the stem?", "minerals": "Which tubes carry mineral salts from the roots?", "food": "Which tubes carry food made in the leaves?",
         "sugar to fruit": "Which tubes carry sugar to a ripening mango?", "food to roots": "Which tubes carry food down to the roots?",
         "water to leaves": "Which tubes carry water to the leaves for making food?", "water to flowers": "Which tubes carry coloured water to the petals of a white flower?",
         "food to seeds": "Which tubes carry food to the developing seeds?"}[k]
    return item(q, "the " + a, ["the " + ("water-carrying tubes" if a.startswith("food") else "food-carrying tubes"), "the roots only", "the chloroplasts"],
                "The %s carry %s." % (a, TUBES[a]))


PATH_W = ["soil", "roots", "stem", "leaves"]
PATH_F = ["leaves", "stem", "roots"]


def g_path():
    k = R.choice(["w", "f"])
    if k == "w":
        i = R.randrange(3)
        if not once(("pw", i)):
            return None
        w = [x for x in ["the soil", "the roots", "the stem", "the leaves", "the air"] if x not in ("the " + PATH_W[i], "the " + PATH_W[i + 1])][:3]
        return item("Water moves through a plant. Where does it go after the %s?" % PATH_W[i], "the " + PATH_W[i + 1], w,
                    "Water: soil → roots → stem → leaves.")
    i = R.randrange(2)
    if not once(("pf", i)):
        return None
    w = ["the " + x for x in PATH_F if x not in (PATH_F[i], PATH_F[i + 1])] + ["the soil", "the air"]
    return item("Food moves from the leaves to the roots. Where does it go after the %s?" % PATH_F[i], "the " + PATH_F[i + 1], w[:3], "Food: leaves → stem → roots (and to fruits, seeds and growing parts).")


def g_ring():
    k = R.choice(["swell", "roots", "die", "why", "which", "water", "leaves"])
    if not once(("rg", k)):
        return None
    q0 = "A ring of the outer layer of bark was removed from the trunk of a young tree (ring-barking)."
    rows = {"swell": (q0 + " After some weeks, the trunk just above the ring swelled. Why?", "Food carried down from the leaves collected above the ring.",
                      ["Water collected above the ring.", "The roots pushed food up.", "The tree grew new roots there."], "The food-carrying tubes were cut, so food could not pass the ring."),
            "roots": (q0 + " What happens to the roots?", "They do not get food and slowly die.", ["They get more water.", "They grow faster.", "They make their own food."],
                      "Roots cannot make food; they depend on the food-carrying tubes."),
            "die": (q0 + " Why does the tree eventually die?", "The roots die without food, so water and mineral salts can no longer be taken in.",
                    ["The leaves get no water at once.", "The tree gets too much food.", "The bark grows back too fast."], "First the roots starve; then the whole tree suffers."),
            "why": (q0 + " Which tubes were removed?", "the food-carrying tubes", ["the water-carrying tubes", "both kinds of tubes", "no tubes"],
                    "The food-carrying tubes are near the outside of the stem; the water-carrying tubes are deeper inside."),
            "which": (q0 + " Which part of the tree swells?", "the part just above the ring", ["the part just below the ring", "the roots", "the tips of the leaves"],
                      "Food moving down cannot pass the ring."),
            "water": (q0 + " Why do the leaves stay green for some time?", "The water-carrying tubes deeper inside are not cut, so water still reaches the leaves.",
                      ["The leaves stop needing water.", "The leaves take in water from the air.", "The food-carrying tubes carry water."], "Only the outer layer was removed."),
            "leaves": (q0 + " Can the leaves still make food?", "Yes, for a time, because they still get water and light.", ["No, the leaves die at once.", "No, the leaves need the bark to make food.", "Only at night."],
                       "The problem is that the food cannot reach the roots.")}
    return item(*rows[k])


def g_dye():
    col = R.choice(["red", "blue", "green"])
    pl = R.choice(["balsam plant", "celery stalk", "white daisy", "white chrysanthemum", "Chinese cabbage leaf"])
    k = R.choice(["where", "cut", "which", "time"])
    if not once(("dy", pl, k)) or not once(("dyn", k), 2):
        return None
    q0 = "%s put a %s in %s-coloured water for a day." % (P.next()[0], pl, col)
    if k == "where":
        return item(q0 + " Where would the colour be seen first?", "in the stem, just above the water", ["at the tips of the leaves", "in the roots only", "nowhere"],
                    "Water moves up from the bottom of the stem.")
    if k == "cut":
        return item(q0 + " The stem was then cut across. What do the coloured spots show?", "the water-carrying tubes", ["the food-carrying tubes", "the chloroplasts", "the seeds"],
                    "The coloured water travels up the water-carrying tubes.")
    if k == "which":
        return item(q0 + " What does the experiment show?", "Water is carried up the stem to the leaves and flowers.", ["Food is carried down to the roots.", "Plants make coloured water.", "Leaves take in water from the air."],
                    "The colour travels with the water.")
    return item(q0 + " Why would the colour move up faster on a hot, windy day?", "More water is lost from the leaves, so more water is drawn up.",
                ["The colour is lighter.", "The roots push harder.", "The stem becomes shorter."], "Water loss from the leaves pulls water up the stem.")


def g_loss():
    t = [0, 2, 4, 6]
    lost = [0]
    for _ in range(3):
        lost.append(lost[-1] + R.randint(3, 8))
    v0 = 100
    k = R.choice(["at4", "why", "oil", "ctrl"])
    if not once(("ls", k), 2 if k == "at4" else 1):
        return None
    tb = table(["Time (h)", "Water in the cylinder (ml)"], [[str(a), str(v0 - b)] for a, b in zip(t, lost)])
    q0 = "%s put a leafy shoot in a measuring cylinder of water. A layer of oil was added on top of the water.<br>%s" % (P.next()[0], tb)
    if k == "at4":
        return item(q0 + "How much water was taken up by the shoot in the first 4 hours?", "%d ml" % lost[2], ["%d ml" % (v0 - lost[2]), "%d ml" % lost[3], "%d ml" % lost[1]],
                    "%d − %d = %d ml." % (v0, v0 - lost[2], lost[2]))
    if k == "why":
        return item(q0 + "Why did the water level fall?", "The shoot took up water, which was lost from the leaves.", ["Water evaporated through the oil.", "The oil drank the water.", "The cylinder leaked."],
                    "The oil stops water evaporating from the surface.")
    if k == "oil":
        return item(q0 + "Why was oil added?", "to stop water evaporating from the surface", ["to give the shoot food", "to make the water warmer", "to colour the water"],
                    "Any water lost must have gone into the shoot.")
    return item(q0 + "Which set-up would be a good control?", "an identical cylinder of water and oil with no shoot", ["a shoot with more leaves", "a cylinder with no oil", "a cylinder of coloured water"],
                "It shows that the water level does not fall without the shoot.")


B1 = bank([
    ("What do the water-carrying tubes carry?", "water and mineral salts from the roots to the other parts", ["food from the leaves", "air from the leaves", "light from the Sun"], "They run from the roots, up the stem, to the leaves."),
    ("What do the food-carrying tubes carry?", "food from the leaves to the other parts of the plant", ["water from the roots", "soil", "air"], "Food is carried up and down."),
    ("In which direction do the water-carrying tubes carry water?", "upwards, from the roots to the leaves", ["downwards only", "in both directions", "sideways only"], "Water moves up from the roots."),
    ("In which direction is food carried?", "to all parts of the plant, up and down", ["only upwards", "only to the roots", "only to the leaves"], "Food goes to roots, fruits, seeds and growing tips."),
    ("Why do the roots need food from the leaves?", "Roots cannot make food because they have no chloroplasts and get no light.", ["Roots make too much food.", "Roots need food to make light.", "Roots do not need food."], "All living cells need food."),
    ("Why are the transport tubes compared to the blood vessels of animals?", "Both carry substances to all parts of the living thing.", ["Both are red.", "Both pump blood.", "Both make food."], "The plant transport system moves water and food."),
])
B2 = bank([
    ("Why does a plant wilt on a hot day?", "It loses water from its leaves faster than it takes in water.", ["It makes too much food.", "Its food-carrying tubes are blocked.", "It gets too much light."], "Wilting means the cells have too little water."),
    ("Why do the leaves of a cut flower droop after a few hours out of water?", "No water is reaching the leaves through the water-carrying tubes.", ["The food-carrying tubes are full.", "The flower makes too much food.", "The petals take all the food."], "The stem has no water supply."),
    ("Why does a farmer water plants at the roots, not on the leaves?", "The roots take in water and the water-carrying tubes carry it up.", ["Leaves take in water through their tubes.", "Water on leaves turns to food.", "Roots do not need water."], "Water enters the plant through the roots."),
    ("Where are the mineral salts in the soil taken in?", "at the roots", ["at the leaves", "at the flowers", "at the fruits"], "They are carried up with the water."),
    ("Which part of a plant stores food carried by the food-carrying tubes?", "a sweet potato root", ["a leaf vein only", "the water-carrying tubes", "the soil"], "Food is carried down and stored."),
    ("A mango fruit ripens and becomes sweet. Where did the sugar come from?", "the leaves, through the food-carrying tubes", ["the soil, through the roots", "the rain", "the water-carrying tubes"], "Food made in the leaves is carried to the fruit."),
])
B5 = bank([
    ("Siti ring-barked a hibiscus stem and left it for two weeks. Which part swelled?", "the part just above the ring", ["the part just below the ring", "the roots", "the flowers"], "Food moving down collected above the ring."),
    ("Why did Siti's plant still have green leaves after a week?", "The water-carrying tubes were not removed.", ["The leaves stored water.", "The food-carrying tubes carried water.", "It rained a lot."], "Only the outer layer with the food-carrying tubes was removed."),
    ("Ravi wants to show that water moves up a stem. What should he do?", "Put a white flower in coloured water and observe the petals.", ["Remove all the leaves.", "Put the plant in the dark.", "Cover the leaves with plastic."], "The petals change colour as coloured water moves up."),
    ("Mei Ling put two identical celery sticks in red water: one with leaves and one without. Which would most likely draw up water faster?", "the one with leaves", ["the one without leaves", "both the same", "neither"], "Water lost from the leaves draws more water up."),
    ("Why was a layer of oil added to the water in the experiment?", "to stop water from evaporating directly from the cylinder", ["to feed the plant", "to colour the water", "to keep insects away"], "Then any loss of water is due to the plant."),
])


def body():
    think = ("<p><b>A plant has two kinds of transport tubes.</b></p>"
             "<ul><li><b>Water-carrying tubes</b> carry water and mineral salts from the roots, up the stem, to all parts of the plant.</li>"
             "<li><b>Food-carrying tubes</b> carry food made in the leaves to all parts of the plant (up and down).</li>"
             "<li>Water is lost from the leaves, so more water is drawn up from the roots.</li>"
             "<li><b>Ring-barking</b> removes the food-carrying tubes in the outer layer: food collects above the ring and the roots slowly starve.</li></ul>")
    ex = [("A ring of bark is removed from a tree. Which part swells?", ["The food-carrying tubes are cut", "Food moving down collects above the ring"], "The part above the ring."),
          ("A white flower is put in blue water. Why do the petals turn blue?", ["Coloured water enters the stem", "It travels up the water-carrying tubes"], "Water is carried up to the flower.")]
    mist = ["Thinking food is carried only upwards. It goes to all parts, including the roots.",
            "Mixing up the two kinds of tubes.",
            "Thinking ring-barking stops water reaching the leaves at once. The water-carrying tubes are deeper inside.",
            "Thinking roots can make their own food."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Two kinds of tubes", B1 + [(g_which, 8), (g_path, 4), (WM.g_path, 2)]),
        ("Water and food in the plant", B2 + [(g_which, 3), (g_path, 3), (WM.g_wilt, 4), (g_dye, 4)]),
        ("Ring-barking", [(g_ring, 7), (g_which, 3), (g_dye, 4), (WM.g_dye, 3), (WM.g_path, 3)]),
        ("Coloured water and water loss", WM.B1 + [(g_dye, 4), (g_loss, 4), (WM.g_table, 4), (WM.g_wilt, 3), (g_ring, 2)]),
        ("PSLE-style experiments", B5 + WM.B5 + [(g_loss, 3), (WM.g_table, 3), (WM.g_dye, 2), (g_ring, 2)]),
    ])
    make_sg(5, "plant-transport-system", 6, "Systems", "Plant system (Plant transport system)",
            "Identify the plant transport system: water-carrying tubes carry water and mineral salts from the roots to the other parts of the plant, and "
            "food-carrying tubes carry food from the leaves to the other parts. Investigate the movement of water in a plant and the effects of removing "
            "the food-carrying tubes (summary of the MOE Primary Science Syllabus).",
            "Plant Transport System",
            "Primary 5 Science: Plant Transport System Worksheets (with Answers)",
            "Plant transport system",
            "Free Primary 5 science worksheets for Singapore pupils on the plant transport system: water-carrying and food-carrying tubes, coloured-water experiments and ring-barking. 100 questions with answers.",
            "Water goes up; food goes to every part.",
            "Water-carrying tubes and food-carrying tubes.",
            body(),
            [("What do the water-carrying tubes carry?", "Water and mineral salts, taken in by the roots, up the stem to all the other parts of the plant."),
             ("What happens when a tree is ring-barked?", "The food-carrying tubes in the outer layer are removed. Food collects and the stem swells above the ring, the roots get no food and the tree slowly dies."),
             ("Why do leaves stay green for a while after ring-barking?", "The water-carrying tubes are deeper inside the stem and are not removed, so water still reaches the leaves.")],
            sets)


if __name__ == "__main__":
    main()
