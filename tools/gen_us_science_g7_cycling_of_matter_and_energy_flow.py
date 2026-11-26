# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Cycling of Matter and Energy Flow (MS-LS2-3)
  python tools/gen_us_science_g7_cycling_of_matter_and_energy_flow.py
Develop a model to describe the cycling of matter and flow of energy among living and nonliving parts of an
ecosystem: producers, consumers, decomposers; trophic levels; energy pyramids (about 10% of energy passes to the
next level; the rest is used for life processes and lost as heat); matter (carbon, nitrogen) cycles while energy
flows one way.
Assessment boundary: no chemical details of photosynthesis and respiration.
Wrong answers come from real mistakes: "energy is recycled", "arrows point from predator to prey",
"top predators have the most energy", "decomposers are not important".
"""
from sci_common import Unit, item, bank, lesson, make, fig, People, comma
from sci_foodweb import WEBS, picture, chains, kind, level, plural, a as art

U = Unit(70110)
R = U.R
P = People(R)


def g_energy():
    base = R.choice([1000, 2000, 5000, 10000, 20000, 50000])
    lv = R.choice([1, 2, 3])
    ans = base // (10 ** lv)
    names = ["producers", "primary consumers", "secondary consumers", "tertiary consumers"]
    who = P.next()[0]
    return item("%s's energy pyramid shows %s units of energy in the producers. About 10%% passes to each level above. About how much energy reaches the %s?" % (who, comma(base), names[lv]),
                "%s units" % comma(ans), ["%s units" % comma(x) for x in sorted({base, ans * 2, max(1, ans // 10), base - ans} - {ans})[:3]],
                "Divide by 10 for each level: %s." % " → ".join(comma(base // 10 ** i) for i in range(lv + 1)))


def g_web():
    w = R.choice(sorted(WEBS))
    ch = R.choice([c for c in chains(w) if len(c) >= 3])
    who = P.next()[0]
    k = R.choice(["most", "least", "role", "arrow"])
    pic = fig(picture(w, label="a %s food web" % w))
    if k == "most":
        return item(pic + "In %s's %s food web, which organism level holds the most energy?" % (who, w), "the producers, such as %s" % plural(WEBS[w]["producers"][0]),
                    ["the top predators", "the herbivores", "the decomposers only"], "Producers capture energy from sunlight; each level up has less.")
    if k == "least":
        top = ch[-1]
        return item(pic + "In the food chain %s, which organism gets the least energy from the sun?" % " → ".join(ch), top,
                    [x for x in ch[:-1]][-3:] if len(ch) >= 4 else ch[:-1] + ["the sun"], "Energy is lost at each step, so the last organism in the chain gets the least.")
    if k == "role":
        x = R.choice([o for o in ch if o not in WEBS[w]["producers"]])
        kd = kind(w, x)
        role = {"herbivore": "a primary consumer", "carnivore": "a consumer that eats other animals", "omnivore": "a consumer that eats plants and animals"}[kd]
        return item(pic + "In this %s food web, what is the role of the %s?" % (w, x), role, [r for r in ["a producer", "a decomposer", "a primary consumer", "a consumer that eats other animals", "a consumer that eats plants and animals"] if r != role][:3],
                    "Look at what it eats in the web.")
    return item(pic + "In %s's food web, what does an arrow from one organism to another show?" % who, "the direction energy and matter move when one is eaten",
                ["which organism is bigger", "which organism eats the other in reverse", "where the organisms live"], "Arrows point from the food to the eater.")


CYCLE = [("A leaf falls and decomposers break it down.", "Nutrients return to the soil for plants to use again."),
         ("A rabbit eats grass.", "Matter and energy in the grass move into the rabbit."),
         ("A fox breathes out carbon dioxide.", "Carbon goes back into the air, where plants can take it in."),
         ("Plants take in carbon dioxide during photosynthesis.", "Carbon from the air becomes part of the plant."),
         ("A dead tree rots on the forest floor.", "Decomposers return carbon and nutrients to the air and soil."),
         ("Bacteria in soil change nitrogen into a form plants can use.", "Nitrogen cycles from the soil into plants.")]


def g_cycle():
    s, a = R.choice(CYCLE)
    who = P.next()[0]
    others = [c[1] for c in CYCLE if c[1] != a]
    return item("%s observes: “%s” What does this show about matter in the ecosystem?" % (who, s), a, R.sample(others, 3), "Matter cycles among living and nonliving parts of the ecosystem.")


B1 = bank([
    ("Where does almost all the energy in an ecosystem come from?", "the sun", ["the soil", "decomposers", "water"], "Producers capture sunlight."),
    ("Does energy cycle in an ecosystem the way matter does?", "No. Energy flows one way and is lost as heat; matter is recycled.", ["Yes, energy is recycled.", "Matter flows one way only.", "Neither moves."],
     "Matter cycles; energy flows."),
    ("Why does only about 10% of energy pass to the next level?", "Most energy is used for life processes or lost as heat.", ["Animals do not eat enough.", "Energy is destroyed.", "Plants keep it all."],
     "This is why food chains are short."),
    ("What do decomposers do?", "break down dead organisms and return nutrients to the soil", ["make food from sunlight", "hunt other animals", "stop the cycling of matter"], "Fungi and bacteria are decomposers."),
    ("Which organisms are producers?", "plants, algae and some bacteria", ["lions and wolves", "mushrooms", "worms"], "Producers make their own food."),
    ("Why are there usually fewer top predators than herbivores?", "Less energy is available at higher levels.", ["Top predators are lazy.", "Herbivores eat predators.", "There is more energy at the top."],
     "Energy pyramids get narrower at the top."),
    ("What happens to the atoms in an animal after it dies?", "Decomposers return them to the soil and air to be used again.", ["They disappear.", "They turn into energy.", "They stay locked forever."],
     "Matter is conserved and recycled."),
    ("Which is a nonliving part of an ecosystem that cycles matter?", "air, water and soil", ["deer", "bacteria", "trees"], "Matter moves between living and nonliving parts."),
])
B5 = bank([
    ("Ava builds a closed jar ecosystem with a plant, snails and soil. Why can it survive for months?", "Matter is recycled inside, and light from outside provides energy.", ["Energy is recycled inside.", "Snails make sunlight.", "The jar adds new atoms."],
     "Energy must come in; matter cycles."),
    ("Leo removes all decomposers from a model forest. What will happen over time?", "Dead material piles up and nutrients stop returning to the soil.", ["Plants grow faster.", "Nothing changes.", "Energy will be recycled."],
     "Decomposers are essential."),
    ("Mia's pyramid has 10,000 units in grass and 1,000 in rabbits. How many units should foxes that eat rabbits have?", "about 100", ["about 1,000", "about 10,000", "about 10"], "About 10% of 1,000."),
    ("Why is eating plants more energy-efficient for people than eating meat?", "Eating lower on the food chain gets more of the sun's original energy.", ["Plants have no energy.", "Meat has no energy.", "It is not more efficient."],
     "Each step loses about 90%."),
    ("A model shows carbon moving from air → plants → animals → decomposers → air. What does it show?", "Carbon cycles through living and nonliving parts.", ["Carbon is used up.", "Carbon flows one way only.", "Carbon is created by animals."],
     "This is the carbon cycle."),
])


def body():
    think = ("<p>In an ecosystem, <b>energy flows</b> and <b>matter cycles</b>.</p>"
             "<ul><li><b>Producers</b> (plants, algae) capture energy from sunlight and make food.</li>"
             "<li><b>Consumers</b> eat producers or other consumers. <b>Decomposers</b> (fungi, bacteria) break down dead things and return nutrients to the soil.</li>"
             "<li>Only about <b>10%</b> of the energy at one level passes to the next; the rest is used for life processes and lost as heat. That is why an <b>energy pyramid</b> narrows at the top.</li>"
             "<li><b>Matter</b> (carbon, nitrogen, water) is recycled among the air, soil, water and living things.</li></ul>"
             "<p>In a food web, arrows point from the food to the eater, showing the direction energy and matter move.</p>")
    ex = [("Producers have 5,000 units. About how much reaches the primary consumers?", ["10% of 5,000"], "500 units"),
          ("Does energy get recycled?", ["Energy is lost as heat."], "No; matter is recycled, energy flows.")]
    mist = ["Thinking energy is recycled like matter.",
            "Drawing arrows from predator to prey. Arrows go from food to eater.",
            "Thinking top predators have the most energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy flow and matter cycles", B1 + [(g_cycle, 6), (g_energy, 6)]),
        ("Energy pyramids", [(g_energy, 14), (g_cycle, 6)]),
        ("Food webs", [(g_web, 16), (g_energy, 4)]),
        ("Cycling matter", [(g_cycle, 10), (g_web, 10)]),
        ("Modeling ecosystems", B5 + [g_web, g_energy, g_cycle]),
    ])
    make("grade-7", "cycling-of-matter-and-energy-flow", 10, "MS-LS2-3",
         "Develop a model to describe the cycling of matter and flow of energy among living and nonliving parts of an ecosystem.",
         "Cycling of Matter and Energy Flow",
         "Grade 7 Energy Flow Worksheets: Food Webs, Energy Pyramids and Matter Cycles",
         "Matter and Energy in Ecosystems",
         "Free middle school science worksheets on cycling of matter and energy flow (NGSS MS-LS2-3): producers, consumers and decomposers, food webs, the 10% rule and energy pyramids, and the carbon cycle. 100 practice questions with answers.",
         "Matter cycles; energy flows.",
         "Energy enters from the sun and about 10% passes up each level. Decomposers return matter to the soil and air.",
         body(),
         [("What is the difference between energy flow and matter cycling?", "Energy enters from the sun, flows through food chains and is lost as heat. Matter is reused again and again."),
          ("What is the 10% rule?", "About 10% of the energy at one level of a food chain is passed to the next level. The rest is used for life processes or lost as heat."),
          ("Why are decomposers important?", "They break down dead organisms and wastes and return nutrients to the soil and air so producers can use them again.")],
         sets)


if __name__ == "__main__":
    main()
