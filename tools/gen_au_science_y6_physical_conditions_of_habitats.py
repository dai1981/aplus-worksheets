# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U01: physical conditions of habitats (temperature, water, light, soil,
salinity) and how changing conditions affect the growth and survival of living things.
  python tools/gen_au_science_y6_physical_conditions_of_habitats.py
Australian habitats (outback, rainforest, alpine, coral reef, mangroves, the Murray-Darling) and changes such as drought,
coral bleaching, salinity and bushfire. Reuses the SG Primary 6 habitat makers and the US Grade 3 habitat makers.
Wrong answers come from real mistakes: naming a living thing as a physical condition, thinking all plants need the same
amount of light and water, and thinking a change in conditions affects only one kind of living thing.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

SG = "gen_sg_science_p6_habitats_populations_and_communities"
US = "gen_us_science_g3_habitats_and_survival"
sg_exp = limit(src(SG, "g_exp"), 6)
sg_b2 = src.B(SG, "B2", drop=["durian"])
sg_b3 = src.B(SG, "B3", drop=["durian"])
sg_b5 = src.B(SG, "B5", drop=["durian"])
NA = ["sloth", "jaguar", "toucan", "walrus", "roadrunner", "polar bear", "durian", "deer", "camel", "penguin", "monkey", "sage", "arctic", "Arctic"]
us_move = src(US, "g_move", drop=NA)
us_data = src(US, "g_data", drop=NA)
us_b5 = src.B(US, "B5", drop=NA)

PC = ["temperature", "amount of water", "amount of light", "type of soil", "amount of salt (salinity)", "amount of oxygen in the water"]
LIVE = ["the number of kangaroos", "the kinds of birds", "the number of trees", "the amount of grass eaten by sheep", "the number of predators"]
SC = [("Inland rivers dry up during a long drought.", "amount of water"),
      ("A hot summer heats the shallow water over a coral reef.", "temperature"),
      ("Tall gum trees shade the forest floor.", "amount of light"),
      ("Salty groundwater rises into farm paddocks.", "amount of salt (salinity)"),
      ("Algae grow in a still creek and use up the oxygen at night.", "amount of oxygen in the water"),
      ("Snow covers the alpine grasslands in winter.", "temperature"),
      ("Sandy soil in the desert holds very little water.", "type of soil"),
      ("A bushfire burns the canopy, so more sunlight reaches the ground.", "amount of light"),
      ("Floods cover a red gum forest for several months.", "amount of water"),
      ("The tide comes in twice a day over the mangrove mud.", "amount of salt (salinity)"),
      ("Clay soil stays waterlogged after rain.", "type of soil"),
      ("A dam is built and the river below it gets colder water.", "temperature")]


def g_pc():
    s, c = R.choice(SC)
    return tq("%s Which physical condition has changed?" % s, c, R.sample([x for x in PC if x != c], 3),
              "Physical conditions are the non-living parts of a habitat, such as %s." % c)


AUW = [("a thorny devil", "the hot, dry outback", "Its skin channels dew and rain to its mouth."),
       ("a snow gum", "the cold Australian Alps", "It can survive frost and snow and regrows after fire."),
       ("a grey mangrove", "salty, muddy shores", "Its leaves get rid of salt and its roots poke up to take in air."),
       ("a red kangaroo", "dry inland grasslands", "It rests in the shade by day and needs little water."),
       ("a hard coral", "warm, clear, shallow sea water", "Tiny algae inside it need sunlight to make food."),
       ("a tree fern", "shady, wet gullies", "Its large fronds catch the little light on the forest floor."),
       ("a mountain pygmy possum", "alpine boulder fields", "It hibernates under the snow in winter."),
       ("a water-holding frog", "dry inland claypans", "It burrows and seals itself in a cocoon until rain returns."),
       ("a saltbush", "dry, salty inland soils", "Its grey, hairy leaves reflect heat and it copes with salt."),
       ("a river red gum", "inland riverbanks that flood", "Its seeds sprout after floods and its roots survive wet soil.")]


def g_auw():
    o, h, why = R.choice(AUW)
    if R.random() < 0.5:
        w = sorted({x[1] for x in AUW if x[0] != o})
        return tq("Which conditions does %s survive best in?" % o, h, R.sample(w, 3), why)
    w = sorted({x[2] for x in AUW if x[0] != o})
    return tq("How is %s suited to %s?" % (o, h), why, R.sample(w, 3), "Its features suit these physical conditions.")


def g_isp():
    from au_sci import once
    c = R.choice(PC)
    if not once(("isp", c)) or len([1 for k in list(__import__("uk_sci").USED) if k[0] == "isp"]) > 3:
        return None
    return tq("Which of these is a physical (non-living) condition of a habitat?", c, R.sample(LIVE, 3),
              "Physical conditions include temperature, water, light, soil and salt. Living things are not physical conditions.")


HAB = [("the outback desert", "very hot days, cold nights and little water", "a spinifex plant"),
       ("a tropical rainforest", "warm, wet and shady near the ground", "a tree fern"),
       ("the Australian Alps", "cold, windy and snowy in winter", "a snow gum"),
       ("the Great Barrier Reef", "warm, clear, salty water with lots of sunlight", "a hard coral"),
       ("a mangrove swamp", "salty, muddy and covered by tides", "a grey mangrove"),
       ("a freshwater billabong", "fresh, still water that may dry up in summer", "a water lily"),
       ("a sandy beach", "salty wind, loose sand and strong sun", "a spinifex beach grass"),
       ("a cool temperate forest in Tasmania", "cool, wet and shaded", "a moss")]


def g_hab():
    h, cond, liv = R.choice(HAB)
    k = R.choice(["cond", "liv"])
    if k == "cond":
        w = sorted({x[1] for x in HAB if x[0] != h})
        return tq("Which physical conditions best describe %s?" % h, cond, R.sample(w, 3), "%s: %s." % (h[0].upper() + h[1:], cond))
    w = sorted({x[2] for x in HAB if x[0] != h})
    art = "an" if liv[0] in "aeiou" else "a"
    return tq("Which living thing is best suited to %s (%s)?" % (h, cond), liv, R.sample(w, 3),
              "Its features suit these conditions.")


GROW = [("bean seedlings", "with different amounts of light", [("0 hours", 2, "pale and thin"), ("4 hours", 9, "green"), ("8 hours", 15, "green and strong")]),
        ("wheat seedlings", "with different amounts of salt in the water", [("no salt", 18, ""), ("a little salt", 11, ""), ("a lot of salt", 3, "")]),
        ("tomato plants", "with different amounts of water each day", [("0 mL", 4, ""), ("50 mL", 19, ""), ("500 mL", 8, "roots rotted")]),
        ("grass seeds", "at different temperatures", [("5 °C", 2, ""), ("20 °C", 14, ""), ("40 °C", 1, "")])]


def g_grow():
    plant, var, rows = R.choice(GROW)
    from au_sci import once
    k = R.choice(["best", "pattern"])
    if not once(("grow", plant, k)):
        return None
    tab = ("<table class='sn-table'><tr><th>%s</th><th>Height after 2 weeks (cm)</th></tr>%s</table>"
           % ({"with different amounts of light": "Light each day", "with different amounts of salt in the water": "Salt in the water", "with different amounts of water each day": "Water each day", "at different temperatures": "Temperature"}[var], "".join("<tr><td>%s</td><td>%d</td></tr>" % (a, b) for a, b, _ in rows)))
    best = max(rows, key=lambda r: r[1])[0]
    if k == "best":
        return tq("%sA class grew %s %s. Which condition gave the tallest plants?" % (tab, plant, var), best,
                  [r[0] for r in rows if r[0] != best] + ["They all grew the same."], "Read the largest height in the table.")
    if "salt" in var:
        a, w2 = "More salt made the seedlings grow less.", "More salt made the seedlings grow taller."
    elif best == rows[-1][0]:
        a, w2 = "More light made the seedlings grow taller.", "More light made the seedlings grow shorter."
    else:
        a, w2 = "The plants grew best in the middle condition; too little or too much was worse.", "The higher the value, the taller the plants grew."
    w = ["The condition made no difference.", w2, "The plants did not grow at all."]
    return tq("%sA class grew %s %s. What does the data show?" % (tab, plant, var), a, w, "Look at how the height changes down the table.")


POOL1 = pool(R, [
    ("What is a habitat?", "the place where a living thing lives and finds what it needs", ["a group of the same animals", "a kind of food", "the weather on one day"], "It provides food, water, shelter and the right conditions."),
    ("Which list contains only physical conditions?", "temperature, light, water, soil", ["trees, birds, light, soil", "food, predators, water, grass", "frogs, rain, wind, insects"], "Physical conditions are non-living."),
    ("Why does a bean plant grown in a dark cupboard become pale and thin?", "It does not get enough light to make food.", ["It gets too much water.", "Cupboards are too cold for all plants.", "Beans only grow at night."], "Plants need light to make their food."),
    ("What happens to many coral when the water stays too hot for weeks?", "They lose their colourful algae and turn white (bleaching).", ["They grow faster.", "They turn into rock straight away.", "They move to deeper water."], "Bleached corals may die if the heat lasts."),
    ("Why do few plants grow in salty farm paddocks?", "Too much salt makes it hard for roots to take in water.", ["Salt makes the soil too cold.", "Salt blocks sunlight.", "Plants are allergic to soil."], "Salinity is a problem in parts of the Murray-Darling Basin."),
    ("How can a long drought affect frogs in a billabong?", "The water dries up, so frogs cannot breed and many die.", ["They grow bigger.", "They have more tadpoles.", "Nothing changes for frogs."], "Water is a key physical condition."),
    ("After a bushfire, more sunlight reaches the forest floor. What happens next?", "Many seedlings sprout and grow quickly.", ["No plants can ever grow again.", "The soil turns into sand.", "The trees grow back in one day."], "Many Australian plants regrow after fire."),
    ("Why do mangroves grow on muddy shores but gum trees do not?", "Mangroves can cope with salty water and waterlogged mud.", ["Mangroves need no water.", "Gum trees grow only in snow.", "Mud is too hot for gum trees."], "Each plant suits certain conditions."),
    ("Which change in a creek would most harm fish?", "less oxygen in the water", ["more shade on a hot day", "clean, cool water", "a few more water plants"], "Fish need oxygen dissolved in the water."),
    ("Why do the same plants not grow in Darwin and in Hobart?", "The temperature and rainfall are very different.", ["Darwin has no soil.", "Hobart has no sunlight.", "Plants only grow in capital cities."], "Climate sets the conditions of a habitat."),
])
POOL5 = pool(R, [
    ("Mia wants to test whether temperature affects how fast cress seeds sprout. What should she change?", "the temperature", ["the type of seed", "the amount of water", "the light"], "Change only the temperature."),
    ("In Mia's cress test, what should she measure?", "the number of seeds that sprout each day", ["the room temperature only", "the colour of the dish", "the time she starts"], "Measure the result of the change."),
    ("Jack counts slaters under logs in a dry area (4) and a damp area (31). What does this suggest?", "Slaters prefer damp conditions.", ["Slaters prefer dry conditions.", "Slaters do not live under logs.", "The number was chance only."], "The big difference suggests a pattern; repeating would check it."),
    ("Ruby measures soil temperature in the sun (38 °C) and under a tree (24 °C). Which living thing is more likely to survive under the tree?", "a worm that dries out in heat", ["a lizard basking in sun", "a spinifex plant", "a cactus"], "Shade keeps soil cooler and damper."),
    ("Which tool would Kai use to measure how much light reaches the forest floor?", "a light meter", ["a thermometer", "a rain gauge", "a ruler"], "Light meters measure brightness."),
    ("Which tool measures rainfall in a habitat?", "a rain gauge", ["a light meter", "a thermometer", "a stopwatch"], "Rainfall is measured in millimetres."),
    ("A scientist finds fewer platypus in a river after a dam is built. Which condition should she measure first?", "the water temperature and flow below the dam", ["the colour of the sky", "the number of cars nearby", "the height of the dam wall"], "Dams change the physical conditions downstream."),
    ("Ella grows two sets of seedlings with the same soil, water and light, but one set is watered with salty water. What is she testing?", "how salinity affects plant growth", ["how light affects growth", "how soil type affects growth", "how temperature affects growth"], "Only the salt changes."),
])


def main():
    sets = U.sets([
        ("Physical conditions", [(g_isp, 3), (g_pc, 9), (POOL1, 4), (sg_b2, 4)]),
        ("Australian habitats", [(g_hab, 10), (g_auw, 8), (POOL1, 2)]),
        ("Changing conditions", [(g_pc, 3), (POOL1, 4), (sg_b3, 4), (us_move, 4), (sg_b5, 3), (g_auw, 2)]),
        ("Growth and survival data", [(g_grow, 8), (us_data, 4), (sg_exp, 4), (g_auw, 4)]),
        ("Investigations", [(POOL5, 8), (sg_exp, 2), (us_b5, 4), (g_hab, 3), (sg_b5, 3)]),
    ])
    make_au(YEAR, "physical-conditions-of-habitats", SORT, "AC9S6U01", "Biological sciences",
            "Investigate the physical conditions of a habitat and analyse how the growth and survival of living things is affected by "
            "changing physical conditions (summary of the Australian Curriculum v9.0 Science content description).",
            "Physical Conditions of Habitats", "Physical conditions of habitats",
            "Free Year 6 science worksheets on the physical conditions of habitats: temperature, water, light, soil and salt, and how "
            "drought, heat and salinity affect Australian plants and animals. 100 questions with answers.",
            "Physical conditions affect growth and survival.", "Temperature, water, light, soil and salt decide what can live in a habitat.",
            "<p><b>The physical conditions of a habitat are its non-living parts: temperature, water, light, soil, salt and oxygen.</b></p><ul>"
            "<li>Each living thing grows best in a certain range of conditions.</li>"
            "<li>When conditions change (drought, flood, heatwave, salinity, bushfire), some living things grow better and others struggle or die.</li>"
            "<li>To test a condition, change only that condition and measure growth or survival.</li></ul>",
            [("Coral turns white in a marine heatwave. Which condition changed?", ["the water stayed too warm"], "temperature"),
             ("Seedlings: 0 h light 2 cm, 8 h light 15 cm. Pattern?", ["height goes up as light goes up"], "more light, more growth")],
            ["Calling a living thing (such as predators or trees) a physical condition.", "Thinking more water or light is always better (too much can harm).",
             "Changing two conditions in one test."],
            [("What are physical conditions in a habitat?", "They are the non-living parts of a habitat, such as temperature, water, light, soil, wind, salt and oxygen in the water."),
             ("How does drought affect living things?", "During a drought, rivers and billabongs dry up and plants wilt. Animals that need water, such as frogs and fish, can die or move away."),
             ("What is coral bleaching?", "When sea water stays too warm, corals push out the tiny algae that live inside them and give them colour and food. The coral turns white and may die.")],
            sets)


if __name__ == "__main__":
    main()
