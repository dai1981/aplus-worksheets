# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Energy in Chemical Reactions (MS-PS1-6)
  python tools/gen_us_science_g7_energy_in_chemical_reactions.py
Undertake a design project to construct, test and modify a device that either releases or absorbs thermal
energy by chemical processes. Exothermic (releases heat: hand warmers with iron powder, burning, calcium
chloride dissolving) and endothermic (absorbs heat: instant cold packs with ammonium nitrate, baking soda and
vinegar, ammonium chloride dissolving). Temperature data, criteria and constraints, modifying a design.
Assessment boundary: amount of reactant, temperature and time only; no bond energies.
Wrong answers come from real mistakes: "a cold pack releases cold", "endothermic means it gets hot",
"more of one reactant always means more heat no matter what".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70105)
R = U.R
P = People(R)

EXO = ["a hand warmer heats up when its iron powder reacts with oxygen", "wood burns in a campfire", "calcium chloride dissolves in water and the cup gets warm",
       "a self-heating can of soup warms up", "a match burns", "a glow stick gives off light", "steel wool burns in a flame"]
ENDO = ["an instant cold pack gets cold when it is squeezed", "baking soda and vinegar react and the cup gets colder", "ammonium chloride dissolves in water and the cup feels cold",
        "plants take in light energy to make sugar", "citric acid and baking soda mix in water and the water cools", "baking a cake takes in heat to cause chemical changes"]


def g_kind():
    who = P.next()[0]
    if R.random() < 0.5:
        x = R.choice(EXO)
        return item("%s observes that %s. Is this reaction exothermic or endothermic?" % (who, x), "exothermic (releases thermal energy)",
                    ["endothermic (absorbs thermal energy)", "neither; no energy changes", "It releases cold."], "The surroundings get warmer, so energy is released.")
    x = R.choice(ENDO)
    return item("%s observes that %s. Is this reaction exothermic or endothermic?" % (who, x), "endothermic (absorbs thermal energy)",
                ["exothermic (releases thermal energy)", "neither; no energy changes", "It releases cold."], "Energy is taken in from the surroundings, so they get colder.")


def g_data():
    t0 = R.choice([20, 21, 22])
    kind = R.choice(["exo", "endo"])
    d = R.randint(8, 25)
    t1 = t0 + d if kind == "exo" else t0 - d
    sub = R.choice(["calcium chloride", "a hand-warmer mix"]) if kind == "exo" else R.choice(["ammonium nitrate", "ammonium chloride", "baking soda and citric acid"])
    rows = [["before mixing", "%d °C" % t0], ["after 2 minutes", "%s °C" % (("−" if t1 < 0 else "") + str(abs(t1)))]]
    who = P.next()[0]
    tab = table(["Time", "Temperature of the water"], rows)
    k = R.choice(["kind", "change", "use"])
    if k == "kind":
        return item(tab + "%s added %s to water. Was the process exothermic or endothermic?" % (who, sub), "exothermic" if kind == "exo" else "endothermic",
                    ["endothermic" if kind == "exo" else "exothermic", "neither", "both at the same time"], "The temperature %s, so energy was %s." % ("rose" if kind == "exo" else "fell", "released" if kind == "exo" else "absorbed"))
    if k == "change":
        return item(tab + "By how many degrees did the temperature change in %s's test?" % who, "%d °C" % d, ["%d °C" % (d + 2), "%d °C" % (t0 + d), "%d °C" % t0],
                    "%d and %d differ by %d °C." % (t0, t1, d))
    return item(tab + "Which product could %s design with this process?" % who, "a hand warmer" if kind == "exo" else "an instant cold pack",
                ["an instant cold pack" if kind == "exo" else "a hand warmer", "a battery", "a magnet"], "%s processes are used for %s." % ("Exothermic" if kind == "exo" else "Endothermic", "warmers" if kind == "exo" else "cold packs"))


def g_amount():
    who = P.next()[0]
    gs = [5, 10, 15, 20]
    base = R.randint(2, 4)
    exo = R.random() < 0.5
    ch = [base * g // 5 + R.randint(0, 1) for g in gs]
    rows = [["%d g" % g, ("+" if exo else "−") + "%d °C" % c] for g, c in zip(gs, ch)]
    tab = table(["Amount of %s in 100 mL water" % ("calcium chloride" if exo else "ammonium chloride"), "Temperature change"], rows)
    if R.random() < 0.5:
        return item(tab + "What pattern does %s's data show?" % who, "More of the substance caused a bigger temperature change.",
                    ["More of the substance caused a smaller change.", "The amount did not matter.", "The water got colder and hotter randomly."], "From 5 g to 20 g the change grew from %d to %d °C." % (ch[0], ch[-1]))
    return item(tab + "%s wants a %s that changes the water temperature by at least %d °C. What is the least amount that works in the table?" % (who, "hand warmer" if exo else "cold pack", ch[2]),
                "15 g", ["5 g", "10 g", "20 g"] if ch[1] < ch[2] else ["5 g", "20 g", "25 g"], "15 g gave a change of %d °C." % ch[2])


DESIGN = [("Ava's hand warmer gets warm but cools after 5 minutes. The criterion is 20 minutes. What should she test next?", "a larger amount of iron powder or better insulation, changing one at a time",
           ["less iron powder", "a thinner bag with holes", "stop testing because it works"]),
          ("Leo's cold pack gets cold too slowly. What could he try?", "crushing the solid into a finer powder so it dissolves faster", ["using bigger chunks", "warming the water first", "using less water and no solid"]),
          ("Mia's cold pack leaks when squeezed. Which modification fixes this?", "use a stronger outer bag and test it again", ["add more water", "use a hotter solid", "remove the inner pouch"]),
          ("Noah's warmer works but costs $6. The constraint is $3. What should he do?", "find cheaper materials and retest the temperature", ["ignore the cost", "add more expensive parts", "change the constraint to $6"]),
          ("Ruby's cold pack only reaches 15 °C. The criterion is 10 °C or colder. What should she test?", "more of the dissolving solid in the same amount of water", ["less of the solid", "warmer water", "a smaller thermometer"]),
          ("Omar's hand warmer heats up before anyone opens it. What is the most likely problem?", "air is leaking into the package", ["the iron powder is too cold", "the package is too thick", "there is no iron"]),
          ("Grace tests her cold pack once and it works. Why should she test it two more times?", "to make sure the result is reliable", ["to use up the materials", "to make it colder", "because the first test never counts"]),
          ("Kai's warmer is hot in the middle but cold at the edges. Which change should he test?", "spread the reacting powder more evenly in the pouch", ["put all the powder in one corner", "remove the pouch", "use a metal bag with holes"])]


def g_design():
    q, a, w = R.choice(DESIGN)
    return item(q, a, w, "Engineers modify one part at a time and test again against the criteria and constraints.")


B1 = bank([
    ("What is an exothermic process?", "one that releases thermal energy, so the surroundings get warmer", ["one that absorbs thermal energy", "one with no energy change", "one that releases cold"],
     "Exo = out. Energy goes out."),
    ("What is an endothermic process?", "one that absorbs thermal energy, so the surroundings get colder", ["one that releases thermal energy", "one that makes things hot", "one that releases cold"],
     "Endo = in. Energy goes in."),
    ("Why does a cold pack feel cold?", "The reaction absorbs thermal energy from your hand.", ["It releases cold.", "It contains ice.", "It is magnetic."], "Cold is the absence of heat; energy moves into the pack."),
    ("Burning gas on a stove is an example of", "an exothermic reaction", ["an endothermic reaction", "a physical change only", "a reaction with no energy change"], "Burning releases heat and light."),
    ("Which tool is most important for testing a hand-warmer design?", "a thermometer", ["a ruler", "a magnet", "a compass"], "Measure temperature change over time."),
    ("Photosynthesis takes in energy from sunlight. What kind of process is it?", "endothermic", ["exothermic", "neither", "a physical change"], "Plants absorb light energy to make sugar."),
    ("In a design project for a cold pack, which is a constraint?", "It must cost less than $2 to make.", ["It must stay below 10 °C for 15 minutes.", "It must get cold.", "It must feel cold on skin."],
     "Constraints are limits."),
    ("Why do hand warmers stay sealed until you open them?", "The reaction needs oxygen from the air to start.", ["They need sunlight.", "They need water from the ground.", "They are magnets."],
     "Iron reacts with oxygen and releases heat."),
])
B5 = bank([
    ("Ava tests 3 hand-warmer designs. What should she keep the same in each test?", "the starting temperature, the amount of water and the way she measures", ["nothing", "only the bag color", "the design being tested"],
     "Only the design should change."),
    ("Leo's best design reached 45 °C, but the criterion says no higher than 40 °C for safety. What should he do?", "use a little less of the reacting substance and retest", ["use more of it", "keep it as is", "remove the thermometer"],
     "Safety is a criterion too."),
    ("Mia mixes vinegar and baking soda in a cup with a thermometer. The temperature drops 4 °C. What can she conclude?", "The reaction is endothermic.", ["The reaction is exothermic.", "No reaction happened.", "The thermometer is broken."],
     "Falling temperature means energy was absorbed."),
    ("Why do engineers make several versions of a cold pack?", "to compare results and keep the best features", ["to waste materials", "because the first is always best", "to make it heavier"],
     "Testing and modifying improves designs."),
    ("A self-heating meal heats food when water is added to a pouch. What kind of process happens in the pouch?", "exothermic", ["endothermic", "freezing", "no change"], "It releases thermal energy."),
])


def body():
    think = ("<p>Chemical processes can <b>release</b> or <b>absorb</b> thermal energy.</p>"
             "<ul><li><b>Exothermic</b>: releases energy, so the surroundings get <b>warmer</b> (hand warmers, burning, calcium chloride dissolving).</li>"
             "<li><b>Endothermic</b>: absorbs energy, so the surroundings get <b>colder</b> (instant cold packs, baking soda and vinegar).</li></ul>"
             "<p>Engineers use these processes to design warmers and cold packs. They test with a thermometer, compare against <b>criteria</b> (how hot or cold, how long) and <b>constraints</b> (cost, safety, size), "
             "and <b>modify one thing at a time</b>, such as the amount of a substance.</p>")
    ex = [("Water goes from 21 °C to 9 °C after a powder is added. Exothermic or endothermic?", ["It got colder.", "Energy was absorbed."], "endothermic"),
          ("Which process would you use for a hand warmer?", ["You need heat released."], "an exothermic one")]
    mist = ["Saying a cold pack releases cold. It absorbs heat.",
            "Mixing up exo (out) and endo (in).",
            "Changing several things at once when improving a design."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Releasing and absorbing energy", B1 + [(g_kind, 12)]),
        ("Exothermic or endothermic?", [(g_kind, 12), (g_data, 8)]),
        ("Temperature data", [(g_data, 14), (g_amount, 6)]),
        ("Amount and temperature change", [(g_amount, 12), (g_design, 4), (g_data, 4)]),
        ("Designing warmers and cold packs", B5 + [g_design, g_amount, g_data, g_kind]),
    ])
    make("grade-7", "energy-in-chemical-reactions", 5, "MS-PS1-6",
         "Undertake a design project to construct, test, and modify a device that either releases or absorbs thermal energy by chemical processes.",
         "Energy in Chemical Reactions",
         "Grade 7 Exothermic and Endothermic Worksheets: Hand Warmers and Cold Packs",
         "Energy in Chemical Reactions",
         "Free middle school science worksheets on energy in chemical reactions (NGSS MS-PS1-6): exothermic and endothermic processes, temperature data, and designing hand warmers and cold packs. 100 practice questions with answers.",
         "Some reactions release heat; others absorb it.",
         "Exothermic processes warm the surroundings (hand warmers). Endothermic processes cool them (cold packs).",
         body(),
         [("What is the difference between exothermic and endothermic?", "Exothermic processes release thermal energy and warm the surroundings. Endothermic processes absorb thermal energy and cool the surroundings."),
          ("How does an instant cold pack work?", "When the inner pouch breaks, a substance dissolves in water and absorbs thermal energy, so the pack feels cold."),
          ("How do you improve a hand-warmer design?", "Test it, compare the results with the criteria and constraints, change one thing such as the amount of iron powder, and test again.")],
         sets)


if __name__ == "__main__":
    main()
