# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Mixtures and Solutions (5-PS1-3, 5-PS1-4)
  python tools/gen_us_science_g5_mixtures_and_solutions.py
A mixture keeps the properties of its parts, so the parts can be separated by their properties:
magnet, sieve, filter, floating and evaporation. A solution is a mixture where one substance
dissolves in another. Stirring, warm water and smaller pieces make it dissolve faster;
a saturated solution cannot dissolve any more.
Wrong answers come from real mistakes: "a filter takes salt out of water", "dissolved means gone",
"the mixture weighs less than its parts", "stirring makes more dissolve forever".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(50104)
R = U.R
P = People(R)

METHODS = ["use a magnet", "pour it through a filter", "let the water evaporate", "shake it through a sieve (screen)",
           "add water and skim off what floats", "let it settle and pour off the top layer"]
SEP = [("iron filings and sand", 0, "Iron is attracted to a magnet; sand is not."),
       ("steel paper clips and rice", 0, "The steel clips are attracted to a magnet; rice is not."),
       ("sand and water", 1, "The filter paper lets water through but stops the sand grains."),
       ("mud and water", 1, "The filter catches the bits of soil and lets the water through."),
       ("salt dissolved in water", 2, "Salt is dissolved, so a filter cannot catch it. When the water evaporates, the salt is left."),
       ("sugar dissolved in water", 2, "Dissolved sugar passes through a filter. Evaporating the water leaves the sugar."),
       ("pebbles and sand", 3, "The small sand grains fall through the holes in the screen, and the pebbles stay on top."),
       ("dried beans and flour", 3, "The flour falls through the sieve; the beans are too big."),
       ("wood chips and sand", 4, "Wood floats in water and sand sinks, so the wood chips can be skimmed off."),
       ("cork pieces and gravel", 4, "Cork floats and gravel sinks."),
       ("oil and water", 5, "Oil does not dissolve in water; it floats as a layer on top that can be poured or scooped off.")]

SOLUTIONS = ["salt water", "sugar water", "lemonade made from powder", "tea", "vinegar", "ocean water", "a sports drink", "honey stirred into warm water"]
NOT_SOL = ["trail mix", "a salad", "sand in water", "cereal with milk", "oil and water", "a bowl of fruit", "pebbles in water", "rice and beans"]


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 1: mixtures and solutions
def g_is_solution():
    if R.random() < 0.5:
        a = R.choice(SOLUTIONS)
        return item("Which of these is a <b>solution</b>?", a, R.sample(NOT_SOL, 3),
                    cap(a) + " has one substance dissolved evenly in water, so you cannot see the parts. The others are mixtures with parts you can see.")
    a = R.choice(NOT_SOL)
    return item("Which of these is a mixture but <b>not</b> a solution?", a, R.sample(SOLUTIONS, 3),
                "In " + a + " you can still see the separate parts. Nothing is dissolved evenly.")


B1 = bank([
    ("What is a mixture?", "two or more substances mixed together that keep their own properties", ["one new substance made from two", "a substance that cannot be separated", "only a liquid with something in it"],
     "In a mixture, each part keeps its own properties, so the parts can be separated again."),
    ("What is a solution?", "a mixture in which one substance dissolves evenly in another", ["any mixture with a solid in it", "a mixture you can see the parts of", "a new substance"],
     "In a solution like salt water, the salt is spread evenly through the water and you cannot see it."),
    ("In salt water, the salt is the", "solute (the substance that dissolves)", ["solvent (the substance that does the dissolving)", "filter", "precipitate"],
     "The solute dissolves. The solvent, usually water, does the dissolving."),
    ("In sugar water, the water is the", "solvent", ["solute", "mixture", "sediment"],
     "Water is the solvent: the substance the sugar dissolves into."),
    ("Is every solution a mixture?", "Yes. A solution is a special kind of mixture.", ["No. Solutions are new substances.", "No. Solutions cannot be separated.", "Only solutions with salt are mixtures."],
     "A solution is a mixture where one part is dissolved. The parts can still be separated, for example by evaporation."),
    ("Why is trail mix a mixture?", "The nuts, raisins and pieces keep their own properties and can be picked apart.", ["It is a new substance.", "Everything in it dissolves.", "It is a liquid."],
     "You can pick out each part. Nothing changes into a new substance."),
    ("Water is called a good solvent because", "many substances dissolve in it", ["it is a solid", "nothing dissolves in it", "it is attracted to magnets"],
     "Salt, sugar and many other substances dissolve in water."),
    ("Which mixture has parts that are spread evenly so every sip tastes the same?", "sugar dissolved in tea", ["a bowl of soup with vegetables", "sand in water", "a fruit salad"],
     "In a solution the dissolved sugar spreads evenly through the tea."),
])


# ------------------------------------------------------------ set 2: separating mixtures
def g_sep():
    mix, k, why = R.choice(SEP)
    w = [m for i, m in enumerate(METHODS) if i != k]
    if k == 2:
        w = ["pour it through a filter"] + R.sample([m for m in w if m != "pour it through a filter"], 2)
    else:
        w = R.sample(w, 3)
    stem = R.choice(["How can you separate a mixture of %s?", "What is the best way to separate %s?", "Which method separates %s?"])
    return item(stem % mix, METHODS[k], w, why)


def g_prop_used():
    mix, k, _ = R.choice(SEP)
    props = ["attraction to a magnet", "particle size", "solubility (it dissolves)", "particle size", "floating and sinking", "floating and sinking"]
    ans = props[k]
    w = [p for p in ["attraction to a magnet", "particle size", "solubility (it dissolves)", "floating and sinking", "color"] if p != ans]
    w = R.sample(w, 3)
    return item("To separate %s, you %s. Which property does this method use?" % (mix, METHODS[k]), ans, w,
                "This method works because the parts differ in " + ans + ".")


B2 = bank([
    ("Can a filter separate salt from salt water?", "No. The dissolved salt passes through the filter with the water.", ["Yes, the filter catches the salt.", "Yes, if you use two filters.", "Only if the water is cold."],
     "Dissolved particles are too small to be caught. Evaporate the water to get the salt."),
    ("A mixture of sand, salt and iron filings needs three steps. What should you do first?", "Pull out the iron filings with a magnet.", ["Evaporate the water.", "Burn the mixture.", "Freeze the mixture."],
     "Magnet first (iron), then add water to dissolve the salt, filter out the sand, and evaporate the water to get the salt."),
    ("After you add water to sand and salt and filter it, what passes through the filter?", "salt water", ["sand", "dry salt", "nothing"],
     "The salt dissolves, so it passes through with the water. The sand stays on the filter."),
    ("Why can the parts of a mixture be separated?", "Each part keeps its own properties.", ["The parts are new substances.", "All parts are the same.", "Mixtures have no properties."],
     "Different properties, like size, magnetism or solubility, let you pull the parts apart."),
    ("Gold miners swirl sand and gold in a pan of water. The heavy gold stays at the bottom. Which property are they using?", "Gold sinks faster and stays at the bottom.", ["Gold is attracted to magnets.", "Gold dissolves in water.", "Gold floats."],
     "Gold is much heavier for its size than sand, so it settles while water washes the sand away."),
    ("A coffee filter is used to make coffee. What does it separate?", "the coffee grounds from the coffee drink", ["the water from the sugar", "the color from the water", "the heat from the coffee"],
     "The grounds are too big to pass through. The water with dissolved coffee passes through."),
    ("Why does a sieve separate pebbles from sand but not salt from water?", "Salt in water is dissolved into particles far smaller than the holes.", ["Salt is magnetic.", "Pebbles dissolve.", "Water blocks the holes."],
     "A sieve only catches pieces bigger than its holes. Dissolved salt is far too small."),
])


# ------------------------------------------------------------ set 3: dissolving
def g_rate_table():
    kind = R.choice(["temperature", "stirring", "size"])
    p = P.next()
    if kind == "temperature":
        temps = sorted(R.sample([5, 10, 20, 30, 40, 50, 60], 4))
        base = R.randint(150, 240)
        times = [base - i * R.randint(25, 35) for i in range(4)]
        rows = [["%d °C" % t, "%d s" % s] for t, s in zip(temps, times)]
        tab = table(["Water temperature", "Time for sugar to dissolve"], rows)
        return item(tab + "%s timed how long a sugar cube took to dissolve in water at different temperatures. What pattern does the data show?" % p[0],
                    "The warmer the water, the faster the sugar dissolves.", ["The colder the water, the faster the sugar dissolves.", "Temperature does not change the time.", "Sugar does not dissolve in warm water."],
                    "As the temperature goes up from %d °C to %d °C, the time goes down from %d s to %d s." % (temps[0], temps[-1], times[0], times[-1]))
    if kind == "stirring":
        a = R.randint(150, 260)
        b = R.randint(40, a - 60)
        tab = table(["Cup", "Time to dissolve"], [["not stirred", "%d s" % a], ["stirred", "%d s" % b]])
        return item(tab + "%s dissolved the same amount of salt in two cups of water at the same temperature. How much faster did it dissolve when stirred?" % p[0],
                    "%d s faster" % (a - b), ["%d s faster" % (a + b), "%d s faster" % b, "%d s faster" % a],
                    "%d − %d = %d seconds. Stirring brings fresh water to the salt, so it dissolves faster." % (a, b, a - b))
    a = R.randint(120, 200)
    b = R.randint(20, 60)
    tab = table(["Sugar", "Time to dissolve"], [["one sugar cube", "%d s" % a], ["same mass of granulated sugar", "%d s" % b]])
    return item(tab + "Why did %s's granulated sugar dissolve faster than the cube?" % p[0],
                "Small pieces have more surface touching the water.", ["The granulated sugar has more mass.", "The cube is a different substance.", "Cubes cannot dissolve."],
                "Breaking sugar into small grains lets more water touch it at once, so it dissolves faster (%d s instead of %d s)." % (b, a))


def g_saturate():
    g = R.choice([4, 5, 6])
    n = R.randint(5, 9)
    v = R.choice([50, 100, 200])
    p = P.next()
    return item("%s adds %d-gram scoops of a powder to %d mL of water and stirs after each one. The first %d scoops dissolve. After scoop %d, powder stays at the bottom no matter how long %s stirs. About how many grams dissolved?"
                % (p[0], g, v, n, n + 1, p[1]), "%d g" % (g * n), ["%d g" % (g * (n + 1)), "%d g" % v, "%d g" % (n + 1)],
                "%d scoops × %d g = %d g. The solution is saturated: no more powder can dissolve in that much water." % (n, g, g * n))


B3 = bank([
    ("Which three things make sugar dissolve faster in water?", "stirring, warmer water and smaller pieces", ["cold water, big lumps and no stirring", "a bigger cup only", "adding sand"],
     "All three help more water particles reach the sugar more often."),
    ("A solution that cannot dissolve any more of a substance is called", "saturated", ["filtered", "frozen", "evaporated"],
     "In a saturated solution, extra solute stays undissolved at the bottom."),
    ("Extra salt sits at the bottom of a saturated salt water solution. What could you do to dissolve more?", "Add more water.", ["Add more salt.", "Pour off some water.", "Put it in the freezer."],
     "More water can hold more salt. Warming the water can also help some solids dissolve."),
    ("Does stirring change how much salt can dissolve in a cup of water?", "No. It only makes it dissolve faster.", ["Yes, stirring lets any amount dissolve.", "Yes, stirring stops salt dissolving.", "Only if you stir for an hour."],
     "Stirring speeds things up, but the amount that can dissolve depends on the amount and temperature of the water."),
    ("Why does a sugar cube dissolve faster in hot tea than in iced tea?", "The water particles move faster and hit the sugar more often.", ["Hot tea has more sugar in it.", "Iced tea has no water.", "Sugar melts in hot tea."],
     "Faster-moving water particles pull the sugar particles away more quickly."),
    ("Which will dissolve fastest?", "crushed salt in warm water, stirred", ["a salt block in cold water, not stirred", "a salt block in warm water, not stirred", "crushed salt in cold water, not stirred"],
     "Small pieces, warm water and stirring all speed up dissolving."),
])


# ------------------------------------------------------------ set 4: mass of mixtures
def g_mass_mix():
    k = R.choice([("sand", "iron filings"), ("rice", "beans"), ("salt", "water"), ("sugar", "water"), ("pebbles", "sand"), ("raisins", "cereal")])
    a, b = R.randint(15, 90), R.randint(20, 300)
    return item("%d g of %s is mixed with %d g of %s. What is the mass of the mixture?" % (a, k[0], b, k[1]),
                "%d g" % (a + b), ["%d g" % b, "%d g" % abs(b - a), "%d g" % (a + b + 10)],
                "Nothing is added or lost when you mix: %d + %d = %d g." % (a, b, a + b))


def g_mass_sep():
    tot = R.randint(120, 300)
    part = R.randint(20, tot - 40)
    k = R.choice([("sand and iron filings", "iron filings", "sand"), ("pebbles and sand", "pebbles", "sand"), ("salt water", "salt", "water"), ("beans and rice", "beans", "rice")])
    return item("A %d g mixture of %s is separated. The %s has a mass of %d g. What is the mass of the %s?" % (tot, k[0], k[1], part, k[2]),
                "%d g" % (tot - part), ["%d g" % tot, "%d g" % (tot + part), "%d g" % part],
                "The parts add up to the whole: %d − %d = %d g." % (tot, part, tot - part))


B4 = bank([
    ("Salt is dissolved in water and the salt seems to disappear. What happens to the total mass?", "It stays the same as the salt plus the water.", ["It goes down by the mass of the salt.", "It becomes zero.", "It doubles."],
     "The salt particles are still there, so their mass is too."),
    ("When the parts of a mixture are separated, how does their total mass compare with the mixture?", "It is the same (if nothing is spilled or lost).", ["It is always more.", "It is always less.", "It is zero."],
     "Separating does not create or destroy matter. Any difference comes from spills or water left on a filter."),
])


# ------------------------------------------------------------ set 5: investigations
B5 = bank([
    ("Ava tests whether sugar dissolves faster in warm or cold water. What must stay the same?", "the amount of sugar, the amount of water and the stirring", ["the temperature of the water", "nothing", "only the color of the cups"],
     "Only the temperature changes. Everything else stays the same so the test is fair."),
    ("Leo separates a salt and sand mixture. Which order of steps works?", "add water, filter, evaporate the water", ["evaporate, add water, filter", "filter the dry mixture, then add water", "use a magnet, then evaporate"],
     "Water dissolves the salt, the filter catches the sand, and evaporation leaves the salt."),
    ("Maya's mixture of sand and salt had a mass of 50 g. After separating she has 28 g of sand and 20 g of salt. What is the best explanation for the missing 2 g?", "Some sand or salt stayed on the filter paper or cup.", ["Matter was destroyed.", "The salt turned into water.", "The scale added mass."],
     "Matter is not destroyed. Small amounts get left behind on equipment."),
    ("Noah wants to know which dissolves faster in water: salt or sugar. What should he change?", "only the kind of solid", ["the water temperature too", "the amount of water too", "the stirring in one cup only"],
     "Testing one variable at a time shows which solid dissolves faster."),
    ("Why is a magnet not useful for separating sand from salt?", "Neither sand nor salt is attracted to a magnet.", ["Both are attracted.", "Magnets dissolve salt.", "Sand is magnetic."],
     "A magnet only works if one part is attracted and the other is not."),
    ("A water treatment plant lets dirty water sit in a big tank so mud settles, then pours it through sand. Which separation methods are used?", "settling and filtering", ["evaporation and a magnet", "a magnet and a sieve", "freezing and melting"],
     "Heavy mud settles to the bottom, and sand layers filter out smaller bits."),
    ("Sea salt is made by letting seawater sit in shallow ponds in the sun. Which method is this?", "evaporation", ["filtering", "using a magnet", "sieving"],
     "The sun evaporates the water and leaves the salt behind."),
    ("A recycling center uses a big magnet over a moving belt. What does the magnet pull out?", "steel cans", ["aluminum cans", "plastic bottles", "glass jars"],
     "Steel contains iron, so it is attracted. Aluminum, plastic and glass are not."),
    ("Which result shows that mixing iron filings and sulfur powder did not make a new substance?", "A magnet can still pull out the iron filings.", ["The mixture is yellow-gray.", "The mixture is a powder.", "The mixture has a mass."],
     "The iron kept its property of being attracted to a magnet, so it is still iron."),
    ("Omar stirs drink powder into water, and the water turns red. Is this a new substance?", "No. It is a solution; the powder dissolved and spread its color.", ["Yes, because the color changed.", "Yes, because it is sweet.", "Yes, because it cannot be separated."],
     "Evaporating the water would leave the powder. Coloring water by dissolving is a physical change."),
])


def body():
    think = ("<p>A <b>mixture</b> is two or more substances put together. Each part keeps its own properties, "
             "so you can separate the parts by using those properties.</p>"
             + table(["Mixture", "Method", "Property used"], [["iron filings + sand", "magnet", "attracted to a magnet"], ["pebbles + sand", "sieve", "size"],
                                                              ["sand + water", "filter", "size"], ["salt dissolved in water", "evaporate the water", "solubility"],
                                                              ["wood chips + sand", "add water, skim", "floats or sinks"]])
             + "<p>A <b>solution</b> is a mixture where one substance (the <b>solute</b>) dissolves evenly in another (the <b>solvent</b>), "
               "like sugar in water. Stirring, warmer water and smaller pieces make it dissolve faster. When no more can dissolve, the solution is <b>saturated</b>.</p>")
    ex = [("How can you get salt back from salt water?", ["A filter will not work: the salt is dissolved.", "Let the water evaporate."], "Evaporate the water; the salt is left."),
          ("30 g of sand is mixed with 200 g of water. What is the mass of the mixture?", ["Mixing does not add or remove matter.", "30 + 200 = 230."], "230 g")]
    mist = ["Trying to filter dissolved salt or sugar. Dissolved particles pass through a filter.",
            "Thinking a dissolved solid is gone. It is still there, and so is its mass.",
            "Thinking stirring lets any amount dissolve. Stirring only makes it faster.",
            "Calling every mixture a solution. In a solution you cannot see the separate parts."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Mixtures and solutions", [g_is_solution] + B1),
        ("Separating mixtures", [g_sep, g_prop_used] + B2),
        ("Dissolving", [g_rate_table, g_saturate] + B3),
        ("Mass of mixtures", [(g_mass_mix, 8), (g_mass_sep, 8)] + B4 + [(g_saturate, 2)]),
        ("Investigations", [(g_sep, 4), (g_rate_table, 4)] + B5),
    ])
    make("grade-5", "mixtures-and-solutions", 3, "5-PS1-3, 5-PS1-4",
         "Make observations and measurements to identify materials based on their properties. Conduct an investigation to determine whether the mixing of two or more substances results in new substances.",
         "Mixtures and Solutions",
         "Grade 5 Mixtures and Solutions Worksheets: Separating Mixtures and Dissolving",
         "Mixtures and Solutions",
         "Free Grade 5 science worksheets on mixtures and solutions (NGSS 5-PS1-3, 5-PS1-4): solute and solvent, separating with a magnet, sieve, filter and evaporation, what makes things dissolve faster, and saturated solutions. 100 practice questions with answers.",
         "Separate a mixture by using the different properties of its parts.",
         "A solution is a mixture where one substance dissolves evenly in another. Filters cannot catch dissolved salt; evaporation can.",
         body(),
         [("What is the difference between a mixture and a solution?", "A mixture is two or more substances put together that keep their own properties. A solution is a kind of mixture where one substance dissolves evenly in another, like salt water."),
          ("How do you separate salt from water?", "Let the water evaporate. A filter does not work because the salt is dissolved into particles small enough to pass through it."),
          ("What makes a solid dissolve faster?", "Stirring, warmer water and smaller pieces. They do not change how much can dissolve, only how fast."),
          ("What is a saturated solution?", "A solution that cannot dissolve any more solute. Extra solute stays at the bottom.")],
         sets)


if __name__ == "__main__":
    main()
