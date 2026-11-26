# -*- coding: utf-8 -*-
"""
UK Year 6 science: Micro-organisms (Living things and their habitats)
  python tools/gen_uk_science_y6_micro_organisms.py
Bacteria and fungi (yeast and moulds), how small they are, helpful and harmful micro-organisms, mould and yeast
investigations, and stopping germs from spreading.
Wrong answers come from real mistakes: "all micro-organisms are harmful", "the fridge kills bacteria",
"yeast works best when it is very hot", "micro-organisms are too small to be living".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61603)
R = U.R
P = People(R)

USES = [("making bread rise", "yeast"), ("making yoghurt from milk", "bacteria"), ("the blue veins in Stilton cheese", "mould"),
        ("food poisoning from undercooked chicken", "bacteria"), ("the first antibiotic, penicillin", "mould"), ("colds and flu", "viruses"),
        ("tooth decay", "bacteria"), ("athlete's foot", "fungi"), ("brewing beer", "yeast"), ("fuzzy green patches on old bread", "mould"),
        ("breaking down dead leaves in a compost heap", "bacteria"), ("chickenpox", "viruses"), ("turning cabbage into sauerkraut", "bacteria"),
        ("making soy sauce", "mould")]
GOOD = [("Yeast makes bread dough rise.", "helpful"), ("Bacteria turn milk into yoghurt.", "helpful"), ("Bacteria in the gut help digest food.", "helpful"),
        ("Decomposers break down dead plants and return nutrients to the soil.", "helpful"), ("Penicillin mould is used to make medicine.", "helpful"),
        ("Bacteria in soil help peas and beans get nitrogen.", "helpful"), ("Bacteria on unwashed hands spread illness.", "harmful"),
        ("Mould grows on bread left in a warm, damp place.", "harmful"), ("Bacteria in plaque cause tooth decay.", "harmful"),
        ("Bacteria multiply in chicken left out of the fridge.", "harmful"), ("Mould spores in a damp house can trigger asthma.", "harmful"),
        ("A fungus makes potato plants rot (potato blight).", "harmful")]


def g_use():
    u, m = R.choice(USES)
    if not once(("us", u)):
        return None
    w = [x for x in ["bacteria", "yeast", "mould", "viruses", "fungi"] if x != m and not (m == "fungi" and x in ("yeast", "mould")) and not (m in ("yeast", "mould") and x == "fungi")]
    return item("Which kind of micro-organism is linked to %s?" % u, m, R.sample(w, 3),
                "%s: %s. (Yeast and moulds are both fungi.)" % (u[0].upper() + u[1:], m))


def g_good():
    s, h = R.choice(GOOD)
    if not once(("go", s)):
        return None
    return item("%s Is this micro-organism helpful or harmful to people?" % s, h,
                ["harmful" if h == "helpful" else "helpful", "neither, because micro-organisms are not alive", "neither, because it is a plant"],
                "Some micro-organisms help us; others cause illness or spoil food.")


def g_mould():
    who = P.next()[0]
    place = [("fridge (5 °C)", R.choice([10, 11, 12, 13, 14, 15, 16])), ("kitchen (20 °C)", R.choice([5, 6, 7, 8])), ("airing cupboard (30 °C)", R.choice([2, 3, 4]))]
    damp = R.random() < 0.5
    k = R.choice(["fast", "slow", "var", "why"])
    j = R.randrange(3)
    if k == "slow":
        if not once(("mo", j, place[j][1], damp)):
            return None
    elif not once(("mk", k), 2):
        return None
    tab = table(["Where the bread was kept", "Days until mould appeared"], [[p, str(d)] for p, d in place])
    intro = tab + "%s kept three %sslices of the same bread in different places. " % (who, "damp " if damp else "")
    if k == "fast":
        return item(intro + "Where did mould grow fastest?", "airing cupboard (30 °C)", ["fridge (5 °C)", "kitchen (20 °C)", "It grew at the same speed everywhere."],
                    "Fewest days = fastest: mould grows faster when it is warm.")
    if k == "slow":
        nm = place[j][0].split(" (")[0]
        w = [place[x][1] for x in range(3) if x != j] + [place[j][1] + 1, place[j][1] - 1]
        w = ["%d days" % x for x in dict.fromkeys(w) if x != place[j][1]][:3]
        return item(intro + "How many days did the bread in the %s take to go mouldy?" % nm, "%d days" % place[j][1], w, "Read the %s row." % nm)
    if k == "var":
        return item(intro + "Which variable did %s change?" % who, "the temperature", ["the type of bread", "the size of the slice", "the number of days"],
                    "Only the place (temperature) changed; everything else was kept the same.")
    return item(intro + "Why does bread last longer in the fridge?", "The cold slows down the growth of mould.", ["The cold kills all the mould.", "Mould needs light to grow.", "The fridge is dry, so mould cannot exist."],
                "Cold slows micro-organisms down but does not kill them.")


def g_yeast():
    who = P.next()[0]
    temps = [5, 20, 40, 70]
    size = {5: R.choice([1, 2, 3]), 20: R.choice([5, 6, 7, 8, 9]), 40: R.choice([14, 15, 16, 17, 18, 19, 20]), 70: 0}
    k = R.choice(["best", "hot", "gas", "read", "fair"])
    t = R.choice([5, 20, 40])
    if k == "read":
        if not once(("ye", t, size[t])):
            return None
    elif not once(("yk", k), 2):
        return None
    tab = table(["Water temperature (°C)", "Balloon grew by (cm)"], [[str(t), str(size[t])] for t in temps])
    intro = tab + "%s mixed yeast, sugar and water in four bottles and put a balloon on each. " % who
    if k == "best":
        return item(intro + "At which temperature was the yeast most active?", "40 °C", ["5 °C", "20 °C", "70 °C"], "The balloon grew most at 40 °C: warm, not too hot.")
    if k == "hot":
        return item(intro + "Why did the balloon not grow at 70 °C?", "The heat killed the yeast.", ["Yeast works best when very hot.", "There was too much sugar.", "Balloons cannot stretch when hot."],
                    "Very hot water kills yeast cells.")
    if k == "gas":
        return item(intro + "Which gas made the balloons grow?", "carbon dioxide", ["oxygen", "nitrogen", "steam"], "Yeast feeds on sugar and gives off carbon dioxide.")
    if k == "read":
        w = ["%d cm" % x for x in dict.fromkeys([size[u] for u in temps if u != t] + [size[t] + 1]) if x != size[t]][:3]
        return item(intro + "By how much did the balloon grow at %d °C?" % t, "%d cm" % size[t], w, "Read the %d °C row." % t)
    return item(intro + "What should %s keep the same to make it a fair test?" % who, "the amount of yeast, sugar and water", ["the temperature", "the balloon size results", "nothing at all"],
                "Change only one variable: the temperature.")


def g_size():
    s = R.choice([1, 2, 4, 5, 10, 20])
    mm = R.choice([1, 2, 5])
    n = mm * 1000 // s
    if not once(("sz", s, mm)):
        return None
    g = format(n, ",")
    from sci_phys import uniq
    return item("A micro-organism is %d micrometres (µm) long. 1 mm = 1,000 µm. How many could fit end to end across %d mm?" % (s, mm), g,
                uniq(g, [format(x, ",") for x in (n * 10, mm * 1000 * s, mm * 1000, n // 10) if x]),
                "%s ÷ %d = %s." % (format(mm * 1000, ","), s, g))


B1 = bank([
    ("What is a micro-organism?", "a living thing that is too small to see without a microscope", ["any small insect", "a tiny rock", "a plant seed"], "Micro means very small."),
    ("Which tool do we need to see bacteria?", "a microscope", ["a magnifying glass", "a telescope", "a periscope"], "Bacteria are about 1 to 5 µm long."),
    ("Which group of living things do yeast and moulds belong to?", "fungi", ["plants", "animals", "bacteria"], "Mushrooms are fungi too."),
    ("Are all micro-organisms harmful?", "No. Many are helpful, such as yeast and the bacteria in yoghurt.", ["Yes, they all cause illness.", "Yes, they all spoil food.", "No, they are all helpful."], "Some help, some harm."),
    ("Who discovered penicillin in 1928?", "Alexander Fleming", ["Charles Darwin", "Louis Pasteur", "Carl Linnaeus"], "He noticed mould killing bacteria on a dish."),
    ("What do decomposers such as bacteria and fungi do?", "break down dead plants and animals", ["make sunlight", "eat only living animals", "turn soil into rock"], "They recycle nutrients."),
    ("Which is the best way to stop germs spreading?", "washing hands with soap and water", ["blowing on your hands", "sharing cups", "sneezing into your hand"], "Soap removes germs."),
    ("Why do we cook chicken thoroughly?", "to kill harmful bacteria", ["to make it raw", "to add bacteria", "to make it colder"], "Heat kills bacteria."),
])
B5 = bank([
    ("How could you test whether salt stops mould growing on bread?", "Put salted and unsalted slices in the same warm place and compare.", ["Put one slice in the fridge and one in the oven.", "Eat both slices.", "Use one slice only."], "Change one variable."),
    ("Why should you not open a sealed dish of mould in class?", "Mould spores can be breathed in and make people ill.", ["Mould is too heavy.", "It will stop growing.", "It is boring to look at."], "Safety first."),
    ("A yoghurt maker keeps milk warm for 8 hours. Why warm?", "The helpful bacteria grow fastest when warm.", ["Warm milk kills all bacteria.", "Cold makes yoghurt faster.", "Bacteria need light."], "Use the conditions microbes like."),
    ("Why does catching sneezes in a tissue help?", "It traps droplets that carry germs.", ["It makes germs grow.", "It cools the air.", "It makes germs visible."], "Catch it, bin it, kill it."),
    ("Bread with no preservatives goes mouldy faster. What do preservatives do?", "slow the growth of micro-organisms", ["add more yeast", "kill the flour", "make bread warmer"], "Food lasts longer."),
])


def body():
    think = ("<p><b>Micro-organisms are living things too small to see without a microscope.</b></p>"
             "<ul><li>Bacteria and fungi (such as yeast and moulds) are micro-organisms. Viruses are germs that cause illness.</li>"
             "<li>Helpful: yeast makes bread rise, bacteria make yoghurt, decomposers recycle dead things, mould gave us penicillin.</li>"
             "<li>Harmful: bacteria cause food poisoning and tooth decay; moulds spoil food. Washing hands, cooking food and cold storage help.</li></ul>")
    ex = [("Bread in a fridge or a warm cupboard: which goes mouldy first?", ["Mould grows faster when warm"], "the warm cupboard"),
          ("A bacterium is 2 µm long. How many across 1 mm?", ["1 mm = 1,000 µm", "1,000 ÷ 2"], "500")]
    mist = ["Thinking all micro-organisms are harmful.", "Thinking the fridge kills bacteria (it only slows them down).", "Thinking yeast works best in very hot water."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What micro-organisms are", B1 + [(g_use, 8), (g_size, 4)]),
        ("Helpful or harmful", [(g_good, 12), (g_use, 6), (g_size, 2)]),
        ("Mould investigation", [(g_mould, 16), (g_size, 4)]),
        ("Yeast investigation", [(g_yeast, 16), (g_good, 4)]),
        ("Using what we know", B5 + [(g_mould, 5), (g_yeast, 5), (g_size, 5)]),
    ])
    make_uk(6, "micro-organisms", 3, "Living things and their habitats",
            "Describe how living things are classified into broad groups according to common observable characteristics and based on similarities and differences, including micro-organisms, plants and animals.",
            "Micro-organisms",
            "Year 6 Science: Micro-organisms Worksheets (Bacteria, Yeast and Mould)",
            "Micro-organisms",
            "Free Year 6 science worksheets on micro-organisms: bacteria, yeast and mould, helpful and harmful microbes, mould and yeast investigations and stopping germs. 100 questions with answers.",
            "Tiny living things: helpful and harmful.",
            "Bacteria and fungi are too small to see, but they make bread, yoghurt and illness.",
            body(),
            [("What are micro-organisms?", "Living things that are too small to see with the naked eye, such as bacteria and some fungi (yeast and moulds). You need a microscope to see them."),
             ("Are micro-organisms good or bad?", "Both. Yeast makes bread rise, bacteria make yoghurt and decomposers recycle nutrients, but some bacteria cause food poisoning and moulds spoil food."),
             ("Why does food last longer in the fridge?", "Cold slows down the growth of bacteria and moulds. It does not kill them, so food still goes off in time.")],
            sets)


if __name__ == "__main__":
    main()
