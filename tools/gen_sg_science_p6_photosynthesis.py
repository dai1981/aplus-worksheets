# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Photosynthesis (Energy: Energy forms and uses)
  python tools/gen_sg_science_p6_photosynthesis.py
What a plant needs to make food (light, water, carbon dioxide, chlorophyll), what it makes (sugar and oxygen),
where it happens (green parts, mostly leaves), the Sun as the source of energy stored in food,
plants respiring all the time, and PSLE-style experiments (water plants giving off bubbles, covered leaves,
variegated leaves, plants kept in the dark).
Wrong answers come from real mistakes: "plants get their food from the soil", "plants take in oxygen to make food",
"plants only respire at night", "the gas in the bubbles is carbon dioxide", "white parts of a leaf make food".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once

U = Unit(63601)
R = U.R
P = People(R)

NEEDS = ["light", "water", "carbon dioxide", "chlorophyll"]
NOT_NEEDED = ["oxygen", "soil", "sugar", "fertiliser", "nitrogen", "darkness"]
PLANTS = ["balsam plant", "money plant", "hibiscus plant", "pandan plant", "bean plant", "spinach plant", "orchid", "rain tree seedling", "chilli plant", "kangkong plant"]
WATER_PLANTS = ["Hydrilla", "water plant", "pondweed"]


def g_need():
    k = R.choice(NEEDS)
    if not once(("nd", k)):
        return None
    others = [x for x in NEEDS if x != k]
    w = R.sample(NOT_NEEDED, 3)
    q = R.choice(["Which of these does a plant need to make food?", "A plant makes food by photosynthesis. Which of these does it need?"])
    return item(q, k, w, "A plant needs light, water, carbon dioxide and chlorophyll to make food. It does not need %s to make food." % w[0])


def g_need2():
    have = R.sample(NEEDS, 3)
    miss = [x for x in NEEDS if x not in have][0]
    if not once(("n2", miss)):
        return None
    w = [x for x in ["oxygen", "soil", "sugar", "nitrogen", "fertiliser"]][:3]
    R.shuffle(w)
    return item("A plant has %s, %s and %s. What else does it need to make food?" % tuple(have), miss, w,
                "The four things needed for photosynthesis are light, water, carbon dioxide and chlorophyll.")


def g_products():
    k = R.choice(["food", "gas"])
    if not once(("pr", k)):
        return None
    if k == "food":
        return item("What food does a plant make during photosynthesis?", "sugar", ["protein", "soil", "carbon dioxide"],
                    "Plants make sugar. Some of it is stored as starch.")
    return item("Which gas does a plant give out when it makes food?", "oxygen", ["carbon dioxide", "nitrogen", "water vapour"],
                "Photosynthesis takes in carbon dioxide and gives out oxygen.")


def g_word():
    blanks = [("light energy", ["heat from the soil", "sound energy", "electrical energy"]),
              ("carbon dioxide", ["oxygen", "nitrogen", "water vapour"]),
              ("water", ["sugar", "oxygen", "starch"]),
              ("sugar", ["water", "carbon dioxide", "soil"]),
              ("oxygen", ["carbon dioxide", "nitrogen", "light"]),
              ("chlorophyll", ["soil", "roots", "sugar"])]
    a, w = R.choice(blanks)
    if not once(("wd", a)):
        return None
    eq = {"light energy": "water + carbon dioxide <b>——[ ? , chlorophyll ]——&gt;</b> sugar + oxygen",
          "carbon dioxide": "water + <b>?</b> ——[light, chlorophyll]——&gt; sugar + oxygen",
          "water": "<b>?</b> + carbon dioxide ——[light, chlorophyll]——&gt; sugar + oxygen",
          "sugar": "water + carbon dioxide ——[light, chlorophyll]——&gt; <b>?</b> + oxygen",
          "oxygen": "water + carbon dioxide ——[light, chlorophyll]——&gt; sugar + <b>?</b>",
          "chlorophyll": "water + carbon dioxide ——[light, <b>?</b>]——&gt; sugar + oxygen"}[a]
    return item("What is missing from the word equation for photosynthesis?<br>%s" % eq, a, w,
                "water + carbon dioxide → sugar + oxygen, using light energy, with chlorophyll to trap the light.")


def g_where():
    parts = [("leaves", "They are green and flat, so they trap the most light."),
             ("green stems", "Green stems also have chlorophyll, so they can make some food.")]
    p, why = R.choice(parts)
    if not once(("wh", p)):
        return None
    if p == "leaves":
        return item("Which part of most plants makes the most food?", "the leaves", ["the roots", "the flowers", "the fruits"], why)
    return item("A cactus has no proper leaves. Which part of it makes food?", "its green stem", ["its roots", "its spines", "its flowers"], why)


def g_chloro():
    k = R.choice(range(5))
    if not once(("ch", k)):
        return None
    rows = [("What does chlorophyll do in a leaf?", "It traps light energy.", ["It takes in water.", "It stores sugar.", "It lets oxygen out."],
             "Chlorophyll is the green substance that traps light energy."),
            ("Why are leaves green?", "They contain chlorophyll.", ["They contain water.", "They are full of oxygen.", "They reflect sugar."],
             "Chlorophyll gives the green colour."),
            ("Where in a leaf cell is chlorophyll found?", "in the chloroplasts", ["in the cell wall", "in the nucleus", "in the cell membrane"],
             "Chloroplasts contain chlorophyll."),
            ("Which part of a leaf lets carbon dioxide in?", "tiny openings on the leaf surface", ["the leaf stalk only", "the chlorophyll", "the roots"],
             "Gases move in and out through tiny openings (stomata), mostly on the underside of the leaf."),
            ("How does water reach the leaves to make food?", "Roots take it in and the water-carrying tubes carry it up.", ["Leaves take it in from the air.", "Food-carrying tubes carry it down.", "It is made in the flowers."],
             "Water travels from the roots up the stem to the leaves.")]
    return item(*rows[k])


def g_energy():
    k = R.choice(range(3))
    if not once(("en", k)):
        return None
    org, food = [("cow", "grass"), ("caterpillar", "leaves"), ("bird", "papaya")][k]
    if k == 2:
        return item("A bird eats a ripe papaya. The energy in the papaya was first trapped by which part of the papaya tree?", "its leaves",
                    ["its roots", "its flowers", "its seeds"], "Leaves trap light energy from the Sun and the food made there is stored in the fruit.")
    if k == 1:
        return item("A caterpillar eats leaves to get energy. Where does all of this energy start?", "the Sun",
                    ["the soil", "the rainwater", "the caterpillar's body"], "Plants trap light energy from the Sun; the caterpillar gets it by eating the leaves.")
    return item("A cow eats grass. Where did the energy in the grass first come from?", "the Sun",
                ["the soil", "the water", "the cow"], "Plants trap light energy from the Sun and store it in the food they make. Animals get this energy by eating plants.")


def g_day_night():
    t = R.choice(["day", "night"])
    k = R.choice(["take", "give"])
    if not once(("dn", t, k)):
        return None
    if t == "day" and k == "give":
        return item("On a sunny afternoon, which gas does a healthy plant give out the most?", "oxygen", ["carbon dioxide", "nitrogen", "no gas at all"],
                    "In bright light, photosynthesis is faster than respiration, so the plant gives out oxygen overall.")
    if t == "day":
        return item("On a sunny afternoon, which gas does a healthy plant take in the most?", "carbon dioxide", ["oxygen", "nitrogen", "no gas at all"],
                    "In bright light, the plant uses carbon dioxide to make food faster than respiration makes it.")
    if k == "give":
        return item("At night, which gas does a plant give out?", "carbon dioxide", ["oxygen", "nitrogen", "no gas at all"],
                    "There is no light at night, so there is no photosynthesis. The plant still respires and gives out carbon dioxide.")
    return item("At night, which gas does a plant take in?", "oxygen", ["carbon dioxide", "nitrogen", "no gas at all"],
                "At night the plant only respires: it takes in oxygen and gives out carbon dioxide.")


def g_bubbles():
    plant = R.choice(WATER_PLANTS)
    d = sorted(R.sample([10, 20, 30, 40, 50, 60], 4))
    base = R.randint(30, 48)
    vals = []
    for i, x in enumerate(d):
        vals.append(max(2, base - i * R.randint(6, 10)))
    k = R.choice(["trend", "most", "gas", "var", "same", "why", "meas", "off", "repeat", "reliable", "predict"])
    if not once(("bb", k), 2 if k == "most" else 1):
        return None
    tb = table(["Distance of lamp from plant (cm)", "Bubbles in 1 minute"], [[str(a), str(b)] for a, b in zip(d, vals)])
    q0 = "%s put a %s in water and counted the bubbles it gave off, with a lamp at different distances.<br>%s" % (P.next()[0], plant, tb)
    if k == "trend":
        return item(q0 + "What does the table show?", "The nearer the lamp, the more bubbles the plant gave off.",
                    ["The further the lamp, the more bubbles.", "The distance made no difference.", "The plant gave off bubbles only when the lamp was far away."],
                    "Nearer the lamp, the light is brighter, so the plant makes food faster and gives off more oxygen.")
    if k == "most":
        return item(q0 + "At which distance was the plant making food the fastest?", "%d cm" % d[0], ["%d cm" % x for x in d[1:]],
                    "The most bubbles of oxygen means the fastest photosynthesis.")
    if k == "gas":
        return item(q0 + "Which gas is in the bubbles?", "oxygen", ["carbon dioxide", "water vapour", "nitrogen"],
                    "The plant gives off oxygen when it makes food.")
    if k == "var":
        return item(q0 + "What was changed in this experiment?", "the amount of light reaching the plant",
                    ["the type of plant", "the amount of water", "the number of bubbles"],
                    "Moving the lamp changes how much light reaches the plant. The number of bubbles was measured.")
    if k == "same":
        return item(q0 + "Which of these should be kept the same for a fair test?", "the size and type of the water plant",
                    ["the distance of the lamp", "the number of bubbles", "the amount of light"],
                    "Only the light (the distance) is changed; everything else is kept the same.")
    if k == "meas":
        return item(q0 + "What was measured to show how fast the plant made food?", "the number of bubbles given off in 1 minute",
                    ["the distance of the lamp", "the size of the plant", "the temperature of the room"], "More bubbles of oxygen mean faster photosynthesis.")
    if k == "off":
        return item(q0 + "What would most likely happen if the lamp were switched off in a dark room?", "Very few or no bubbles would be given off.",
                    ["More bubbles would be given off.", "The bubbles would turn into carbon dioxide.", "The number of bubbles would stay the same."],
                    "Without light the plant cannot make food, so it stops giving off oxygen.")
    if k == "repeat":
        return item(q0 + "Why should the bubbles be counted three times at each distance?", "to make the results more reliable",
                    ["to make the plant grow faster", "to change the variable", "to use up the carbon dioxide"], "Repeating and taking an average reduces the effect of counting errors.")
    if k == "reliable":
        return item(q0 + "Which would be a more accurate measurement than counting bubbles?", "the volume of gas collected in a measuring tube",
                    ["the colour of the leaves", "the height of the water plant", "the number of leaves"], "Bubbles can be different sizes, so measuring the volume of gas is more accurate.")
    if k == "predict":
        far = d[-1] + 20
        return item(q0 + "Predict the number of bubbles if the lamp were %d cm away." % far, "fewer than %d" % vals[-1],
                    ["more than %d" % vals[0], "exactly %d" % vals[0], "between %d and %d" % (vals[1], vals[0])],
                    "The trend continues: the further the lamp, the fewer the bubbles.")
    return item(q0 + "Why did the number of bubbles change?", "The amount of light changed, so the rate of photosynthesis changed.",
                ["The amount of carbon dioxide in the air changed.", "The plant got tired.", "The water got colder near the lamp."],
                "Light is needed for photosynthesis; more light gives faster photosynthesis.")


def g_leaf_test():
    k = R.choice(["dark", "cover", "white", "vaseline", "box", "destarch"])
    who = P.next()[0]
    plant = R.choice(PLANTS)
    if not once(("lt", k)):
        return None
    if k == "dark":
        return item("%s kept a %s in a dark cupboard for 3 days, then tested a leaf for starch. What did %s find?" % (who, plant, who),
                    "very little or no starch", ["a lot of starch", "a lot of chlorophyll", "a lot of oxygen"],
                    "With no light, the plant cannot make food, and it uses up the starch it had.")
    if k == "cover":
        return item("Part of a leaf on a %s was covered with black paper and left in sunlight for a day. Which part had starch?" % plant,
                    "only the uncovered part", ["only the covered part", "both parts equally", "neither part"],
                    "The covered part got no light, so it could not make food.")
    if k == "white":
        return item("A %s has leaves with green and white parts. After a sunny day, which parts of a leaf have starch?" % plant,
                    "only the green parts", ["only the white parts", "both parts", "neither part"],
                    "The white parts have no chlorophyll, so they cannot trap light to make food.")
    if k == "vaseline":
        return item("Both sides of a leaf on a %s were covered with Vaseline. Why did the leaf stop making food?" % plant,
                    "Carbon dioxide could not get into the leaf.", ["Light could not reach the leaf.", "The leaf lost its chlorophyll.", "Water could not leave the leaf."],
                    "Vaseline blocks the tiny openings, so carbon dioxide cannot get in. Light still passes through.")
    if k == "box":
        return item("A %s was placed in a box with a hole on one side. After a week, it grew towards the hole. Why is this useful?" % plant,
                    "It gets more light to make food.", ["It gets more soil.", "It avoids carbon dioxide.", "It gets less water."],
                    "Plants grow towards light so their leaves can make more food.")
    return item("Before an experiment, a %s was kept in the dark for 2 days. Why?" % plant,
                "to use up the starch already in its leaves", ["to make more chlorophyll", "to make the leaves grow", "to give it more water"],
                "Then any starch found later must have been made during the experiment.")


def g_compare():
    setups = [("in light", "in the dark", "Light"), ("watered", "not watered", "Water"), ("in normal air", "in air with the carbon dioxide removed", "Carbon dioxide")]
    i = R.randrange(3)
    a, b, need = setups[i]
    k = R.choice(["food", "aim"])
    if not once(("cp", i, k)):
        return None
    plant = R.choice(PLANTS)
    if k == "food":
        return item("Two identical %ss were kept for a week, one %s and one %s. Everything else was the same. Which plant made more food?" % (plant, a, b),
                    "the plant %s" % a, ["the plant %s" % b, "both made the same amount", "neither made any food"],
                    "%s is needed for photosynthesis." % need)
    return item("Two identical %ss were kept for a week, one %s and one %s. Everything else was the same. What was being tested?" % (plant, a, b),
                "whether %s is needed for a plant to make food" % need.lower(), ["whether the plant needs soil", "whether the plant needs oxygen to make food", "whether the plant can grow flowers"],
                "Only one thing was different between the two plants: %s." % need.lower())


def g_hours():
    plant = R.choice(PLANTS)
    hrs = [0, 4, 8, 12]
    g = sorted(R.sample(range(3, 30), 3))
    gain = [-R.randint(1, 3)] + g
    k = R.choice(["trend", "var", "zero", "same", "concl"])
    if not once(("hr", k)):
        return None
    tb = table(["Hours of light each day", "Change in mass after 2 weeks (g)"], [[str(h), ("+%d" % v if v > 0 else "%d" % v)] for h, v in zip(hrs, gain)])
    q0 = "Four identical %ss were given different hours of light each day. Everything else was the same.<br>%s" % (plant, tb)
    if k == "trend":
        return item(q0 + "What is the relationship shown?", "The more hours of light, the more mass the plant gained.",
                    ["The more hours of light, the less mass the plant gained.", "Light had no effect on the mass.", "Only the plant with no light gained mass."],
                    "More light means more food made, so the plant grows more.")
    if k == "var":
        return item(q0 + "What was the changed variable?", "the number of hours of light each day",
                    ["the change in mass", "the type of plant", "the amount of water"], "The hours of light were different for each plant.")
    if k == "zero":
        return item(q0 + "Why did the plant with 0 hours of light lose mass?", "It used stored food to respire but could not make food.",
                    ["It made too much food.", "It took in too much water.", "It gave out too much oxygen."], "Respiration continues in the dark; photosynthesis does not.")
    if k == "same":
        return item(q0 + "Which variable must be kept the same?", "the amount of water given to each plant",
                    ["the hours of light", "the change in mass", "the time the light was switched on"], "Only the hours of light should be different.")
    return item(q0 + "Which conclusion is correct?", "Light is needed for the plant to make food and grow.",
                ["Plants grow best in the dark.", "Water is not needed by plants.", "Plants make food from the soil."], "Plants with more light gained more mass.")


def g_mass():
    plant = R.choice(PLANTS)
    m0 = R.choice([40, 50, 60, 80])
    gain = R.randint(6, 15)
    if not once(("ms",)):
        return None
    tb = table(["Plant", "Mass at start (g)", "Mass after 2 weeks (g)"], [["A (in sunlight)", m0, m0 + gain], ["B (in the dark)", m0, m0 - R.randint(2, 5)]])
    return item("Two %ss were kept in sunlight (A) and in the dark (B). Both were watered.<br>%sWhy did plant B lose mass?" % (plant, tb),
                "It could not make food but still used up food to respire.", ["It got too much water.", "It made too much food.", "It took in too much carbon dioxide."],
                "In the dark there is no photosynthesis, but respiration uses up stored food all the time.")


def g_resp():
    k = R.choice(range(6))
    if not once(("rs", k)):
        return None
    rows = [("When does a plant respire?", "all the time, day and night", ["only at night", "only in the day", "only when it is watered"],
             "All living things respire all the time to release energy."),
            ("Which process releases energy from food in a plant?", "respiration", ["photosynthesis", "transpiration", "pollination"],
             "Respiration breaks down food to release energy."),
            ("What does photosynthesis do with light energy?", "It stores it in food.", ["It turns it into soil.", "It releases it as heat only.", "It destroys it."],
             "Light energy is changed into chemical potential energy in sugar."),
            ("Which statement about photosynthesis and respiration is correct?", "Photosynthesis makes food; respiration uses food to release energy.",
             ["Both make food.", "Respiration makes food; photosynthesis uses it.", "They are the same process."], "They work in opposite directions."),
            ("Which living things can make their own food?", "green plants", ["mushrooms", "animals", "bacteria that cause disease"],
             "Only things with chlorophyll can make food by photosynthesis. Fungi such as mushrooms cannot."),
            ("Why are green plants called food producers?", "They make their own food using light energy.", ["They eat other plants.", "They produce soil.", "They take food from the soil."],
             "Animals depend on the food plants make.")]
    return item(*rows[k])


B1 = bank([
    ("Which of these is NOT needed for photosynthesis?", "oxygen", ["light", "water", "carbon dioxide"], "Oxygen is given out, not taken in, during photosynthesis."),
    ("Why is photosynthesis important to animals?", "It makes the food and oxygen that animals need.", ["It removes all oxygen from the air.", "It makes soil for animals.", "It keeps animals warm."], "Animals eat plants (or eat animals that ate plants) and breathe in oxygen."),
    ("What is photosynthesis?", "the way green plants make food using light energy", ["the way plants take in food from the soil", "the way animals digest food", "the way plants release energy"], "Photo means light; synthesis means making."),
    ("Where does a plant get its food?", "It makes the food itself in its green parts.", ["It takes food from the soil.", "It takes food from rainwater.", "It gets food from insects."], "Soil gives water and minerals, but not food."),
    ("Where does the carbon dioxide for photosynthesis come from?", "the air around the leaves", ["the soil", "the roots", "the Sun"], "It enters the leaves through tiny openings."),
    ("What is the source of energy for photosynthesis?", "light", ["soil", "water", "oxygen"], "Usually sunlight."),
    ("What happens to sugar that a plant does not use straight away?", "Some is stored as starch.", ["It turns into oxygen.", "It is given out through the roots.", "It disappears."], "Starch is stored in leaves, stems, roots, fruits and seeds."),
    ("Which part of a plant carries the food made in the leaves to other parts?", "the food-carrying tubes", ["the water-carrying tubes", "the roots", "the flowers"], "Food-carrying tubes carry sugar all over the plant."),
])
B2 = bank([
    ("Where in a plant is most sugar made?", "in the leaves", ["in the roots", "in the flowers", "in the seeds"], "Leaves have the most chlorophyll and get the most light."),
    ("Which fruit stores food that was made in the leaves?", "a mango", ["none, fruits make their own food", "only fruits that grow underground", "only green fruits"], "Food-carrying tubes carry sugar from the leaves to the fruits."),
    ("In which part of a potato plant is food stored?", "its underground stem (the potato)", ["its roots", "its flowers", "its leaves"], "A potato is a swollen underground stem that stores starch."),
    ("Which of these plants stores food in its root?", "carrot", ["potato", "sugar cane", "onion"], "A carrot is a swollen root. Sugar cane stores sugar in its stem."),
    ("Why does sugar cane taste sweet?", "Its stem stores the sugar made in the leaves.", ["It takes in sugar from the soil.", "Its roots make sugar.", "Rain puts sugar into it."], "Food made in the leaves is carried to the stem and stored."),
    ("What is the stored food in a seed used for?", "to help the young plant grow until it can make its own food", ["to attract insects", "to make the seed float", "to make the seed heavier"], "A seedling uses stored food until its leaves can photosynthesise."),
    ("Which form of energy is stored in the food a plant makes?", "chemical potential energy", ["kinetic energy", "sound energy", "light energy"], "Light energy is changed into chemical potential energy."),
    ("Which energy change happens during photosynthesis?", "light energy to chemical potential energy", ["chemical potential energy to light energy", "heat energy to light energy", "sound energy to chemical potential energy"], "Plants change light energy into energy stored in food."),
    ("A leaf turned blue-black when iodine was added. What does this show?", "The leaf contains starch.", ["The leaf contains oxygen.", "The leaf contains water.", "The leaf has no chlorophyll."], "Iodine turns blue-black with starch."),
])
B3 = bank([
    ("Why does a plant need oxygen?", "for respiration, to release energy from food", ["to make food", "to make chlorophyll", "to take in water"], "Plants use oxygen to respire, like animals."),
    ("At dawn, the light is very dim. Which statement is most likely true?", "The plant makes very little food but still respires.", ["The plant makes food very fast.", "The plant stops respiring.", "The plant gives out only oxygen."], "Little light means slow photosynthesis; respiration goes on all the time."),
    ("A plant was kept in a sealed glass jar on a sunny windowsill. What happened to the amount of oxygen in the jar during the day?", "It increased.", ["It decreased.", "It stayed the same.", "It became zero."], "In bright light the plant gives off more oxygen than it uses."),
    ("A plant was kept in a sealed glass jar in a dark room. What happened to the amount of carbon dioxide in the jar?", "It increased.", ["It decreased.", "It stayed the same.", "It became zero."], "In the dark the plant only respires and gives out carbon dioxide."),
    ("Which gas do both plants and animals give out when they respire?", "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"], "Respiration uses oxygen and gives out carbon dioxide."),
    ("A mouse and a green plant were kept in a sealed jar in sunlight. Why did the mouse live longer than a mouse kept alone?", "The plant gave off oxygen for the mouse.", ["The plant gave off carbon dioxide.", "The plant was food for the mouse.", "The plant made the jar darker."], "The plant takes in the mouse's carbon dioxide and gives out oxygen in light."),
    ("Limewater turns chalky when there is a lot of carbon dioxide. A jar with a plant in the dark had limewater in it. What happened?", "The limewater turned chalky.", ["The limewater stayed clear.", "The limewater turned blue-black.", "The limewater disappeared."], "The plant respired and gave out carbon dioxide, but could not use it without light."),
    ("Why do some people say there is fresh air in a park with many trees?", "The trees give off oxygen in the day.", ["The trees take in oxygen in the day.", "The trees give off carbon dioxide in the day.", "Trees make the air colder only."], "Trees photosynthesise in sunlight and release oxygen."),
])
B4 = bank([
    ("Why is a control set-up used in a plant experiment?", "to compare with the set-up that has one thing changed", ["to make the plant grow faster", "to use up the plant's starch", "to give the plant more light"], "The control shows what happens when nothing is changed."),
    ("Which leaf would make the most food on a sunny day?", "a large green leaf at the top of the plant", ["a white leaf at the top of the plant", "a small leaf in the shade", "a leaf covered with black paper"], "It has chlorophyll and gets the most light."),
    ("Why should the two plants in an experiment be of the same type and size?", "so that the test is fair", ["so that they grow flowers", "so that they need less water", "so that they make more oxygen"], "Only the variable being tested should be different."),
    ("Hui Min wants to find out if the amount of light affects how fast a plant makes food. What should she change?", "the amount of light", ["the type of plant", "the amount of water", "the size of the pot"], "Change only the variable you are testing."),
    ("A plant was kept in sunlight with one leaf in a bag with a chemical that removes carbon dioxide. Why did that leaf have no starch?", "It had no carbon dioxide to make food.", ["It had no light.", "It had no chlorophyll.", "It had too much water."], "Carbon dioxide is needed for photosynthesis."),
    ("Why do plants on the forest floor often have large, wide leaves?", "to trap as much of the little light there as possible", ["to collect more rainwater only", "to keep insects away", "to make more flowers"], "Bigger leaves trap more light where it is shady."),
])
B5 = bank([
    ("Ahmad covered the top of a pot of soil with plastic so no water could evaporate, then weighed a plant over a sunny day. Why did the plant's mass go up a little at the end of the week?", "It made food and stored it, so it grew.", ["The plastic added mass.", "It absorbed oxygen from the air.", "Soil turned into food."], "Food made by photosynthesis is used to grow."),
    ("Why do farmers in Singapore's vertical farms use LED lights for leafy vegetables?", "to give the plants light to make food indoors", ["to keep the plants warm only", "to scare away insects", "to give the plants carbon dioxide"], "Indoor plants need light from lamps to photosynthesise."),
    ("A plant with its leaves removed was kept in sunlight. Why did it stop growing?", "It could not make food without leaves.", ["It had too much light.", "It could not take in water.", "It gave out too much oxygen."], "Leaves are where most food is made."),
    ("Why do plants grown in a dark cupboard turn pale yellow?", "They cannot make chlorophyll without light.", ["They have too much water.", "They have too much carbon dioxide.", "They are respiring too slowly."], "Light is needed to form chlorophyll."),
    ("Which change would make a water plant give off bubbles faster?", "moving a lamp closer to it", ["putting it in a dark cupboard", "covering the beaker with black paper", "removing the carbon dioxide from the water"], "More light speeds up photosynthesis."),
    ("A fish tank has water plants and fish. Why do the water plants help the fish?", "They give off oxygen that the fish need.", ["They give off carbon dioxide.", "They make the water warmer.", "They use up the oxygen."], "Plants add oxygen to the water when they make food in light."),
    ("Jun Jie says plants make food only for themselves. Why is he wrong?", "Animals that eat plants also get the food and energy the plants stored.", ["Plants never store food.", "Animals make their own food too.", "Food made by plants cannot be eaten."], "Plants are at the start of every food chain."),
    ("Why do the leaves at the top of a tree often make more food than leaves lower down?", "They get more sunlight.", ["They get more water from the soil.", "They are older.", "They have no chlorophyll."], "Lower leaves are shaded."),
    ("Why are crops in greenhouses sometimes given extra carbon dioxide?", "to help them make food faster", ["to keep insects away", "to cool the plants", "to stop them respiring"], "More carbon dioxide can speed up photosynthesis."),
    ("A pot plant was watered with water containing a coloured dye. Where would the dye be found first?", "in the water-carrying tubes", ["in the food-carrying tubes", "in the flowers", "in the chlorophyll"], "Water moves up from the roots through water-carrying tubes."),
    ("Siti grew one plant under a red lamp and one under a green lamp of the same brightness. The red-lamp plant grew more. What was she testing?", "how the colour of light affects how a plant makes food", ["how water affects growth", "how soil affects growth", "how the size of the pot affects growth"], "Only the colour of light was changed."),
])


def body():
    think = ("<p><b>Green plants make their own food. This is called photosynthesis.</b></p>"
             "<ul><li>They need <b>light</b>, <b>water</b>, <b>carbon dioxide</b> and <b>chlorophyll</b>.</li>"
             "<li>They make <b>sugar</b> (food) and give out <b>oxygen</b>.</li>"
             "<li>It happens in the green parts, mostly the leaves. Chlorophyll traps light energy and the energy is stored in the food.</li>"
             "<li>Plants also <b>respire</b> all the time, day and night.</li></ul>"
             "<p>water + carbon dioxide → sugar + oxygen (light energy, chlorophyll)</p>")
    ex = [("A water plant gives off more bubbles when a lamp is moved nearer. Why?", ["More light reaches the plant", "It makes food faster and gives off more oxygen"], "More light speeds up photosynthesis."),
          ("Part of a leaf is covered with black paper. Which part has starch?", ["The covered part gets no light", "It cannot make food"], "Only the uncovered part.")]
    mist = ["Thinking plants get their food from the soil. Soil gives water and minerals, not food.",
            "Mixing up the gases: plants take in carbon dioxide and give out oxygen when they make food.",
            "Thinking plants respire only at night. They respire all the time.",
            "Thinking the white parts of a leaf can make food. They have no chlorophyll."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What plants need", B1 + [(g_need, 4), (g_need2, 4), (g_products, 2), (g_where, 2), (g_chloro, 2)]),
        ("Making and storing food", B2 + [(g_word, 6), (g_chloro, 3), (g_energy, 3), (g_resp, 1)]),
        ("Gases, day and night", B3 + [(g_day_night, 4), (g_resp, 5), (g_compare, 3), (g_mass, 1), (g_leaf_test, 1)]),
        ("Leaf experiments", B4 + [(g_leaf_test, 5), (g_compare, 3), (g_bubbles, 8)]),
        ("PSLE-style investigations", B5 + [(g_bubbles, 4), (g_hours, 5)]),
    ])
    make_sg(6, "photosynthesis", 1, "Energy", "Energy forms and uses (Photosynthesis)",
            "Recognise that green plants make food by photosynthesis, using light energy, water and carbon dioxide, with chlorophyll to trap light, "
            "and give out oxygen. Recognise that the Sun is the source of energy for plants and that the energy is stored in food. "
            "Investigate the factors that affect the rate of photosynthesis (summary of the MOE Primary Science Syllabus).",
            "Photosynthesis",
            "Primary 6 Science: Photosynthesis Worksheets (PSLE Practice with Answers)",
            "Photosynthesis",
            "Free Primary 6 science worksheets on photosynthesis for Singapore pupils: what plants need, sugar and oxygen, chlorophyll, respiration and PSLE-style experiments. 100 questions with answers.",
            "Plants make food using light energy.",
            "Light, water and carbon dioxide go in; sugar and oxygen come out.",
            body(),
            [("What do plants need for photosynthesis?", "Light, water, carbon dioxide and chlorophyll. Water comes from the roots and carbon dioxide from the air."),
             ("Do plants respire?", "Yes. Plants respire all the time, day and night, just like animals. In bright light they make food faster than they use it, so they give out oxygen overall."),
             ("Why do water plants give off more bubbles near a lamp?", "Brighter light makes photosynthesis faster, so the plant gives off more oxygen. The bubbles are oxygen.")],
            sets)


if __name__ == "__main__":
    main()
