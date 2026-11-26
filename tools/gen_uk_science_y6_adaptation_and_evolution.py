# -*- coding: utf-8 -*-
"""
UK Year 6 science: Adaptation and Evolution (Evolution and inheritance)
  python tools/gen_uk_science_y6_adaptation_and_evolution.py
How animals and plants are adapted to their environments, natural selection step by step, Darwin's finches,
peppered moths in industrial Britain, and Charles Darwin and Alfred Russel Wallace.
Wrong answers come from real mistakes: "an animal changes its body because it wants to", "evolution happens in one
lifetime", "the strongest always survive", "dark moths appeared because of soot on their wings".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61609)
R = U.R
P = People(R)

AD = [("a polar bear", "a thick layer of fat", "to keep warm in the freezing Arctic"),
      ("a polar bear", "white fur", "to hide against the snow when hunting"),
      ("a camel", "wide, flat feet", "to stop sinking into soft sand"),
      ("a camel", "a hump that stores fat", "to go a long time without food"),
      ("a cactus", "spines instead of leaves", "to lose less water and keep animals away"),
      ("a cactus", "a thick, fleshy stem", "to store water for dry times"),
      ("a duck", "webbed feet", "to paddle through water"),
      ("an owl", "large forward-facing eyes", "to see prey at night"),
      ("an Arctic fox", "small, rounded ears", "to lose less heat through its ears"),
      ("a fennec fox", "very large ears", "to lose heat in the hot desert"),
      ("a woodpecker", "a strong, chisel-like beak", "to drill into wood to find insects"),
      ("a giraffe", "a long neck", "to reach leaves high in trees"),
      ("a penguin", "a streamlined body and flipper-like wings", "to swim fast to catch fish"),
      ("a water lily", "large, flat, floating leaves", "to catch sunlight on the surface of a pond"),
      ("a mole", "large, spade-like front paws", "to dig tunnels underground")]


def g_ad():
    who, f, h = R.choice(AD)
    k = R.random() < 0.55
    if not once(("ad", f, k)):
        return None
    if k:
        return item("%s has %s. How does this help it survive?" % (who[0].upper() + who[1:], f), "It helps it " + h[3:] + ".",
                    ["It helps it " + x[2][3:] + "." for x in R.sample([x for x in AD if x[0] != who], 3)],
                    "An adaptation is a feature that helps a living thing survive in its habitat.")
    return item("Which feature helps %s %s?" % (who, h[3:]), f, R.sample([x[1] for x in AD if x[0] != who], 3),
                "%s has %s %s." % (who[0].upper() + who[1:], f, h))


HAB = [("polar bear", "the Arctic"), ("camel", "a hot desert"), ("cactus", "a hot desert"), ("penguin", "the Antarctic"),
       ("orangutan", "a tropical rainforest"), ("clownfish", "a coral reef"), ("puffin", "rocky sea cliffs"), ("mountain goat", "steep mountains"),
       ("water lily", "a pond"), ("otter", "a river")]


def g_hab():
    a, h = R.choice(HAB)
    if not once(("hb", a)):
        return None
    return item("Which habitat is the %s best adapted to?" % a, h, R.sample(sorted({x[1] for x in HAB} - {h}), 3), "Its features suit the conditions there.")


FINCH = [("a large, deep, strong beak", "cracking hard seeds"), ("a thin, pointed beak", "picking insects from leaves"),
         ("a long, curved beak", "reaching nectar in cactus flowers"), ("a sharp beak like a parrot's", "tearing fruit and buds")]


def g_finch():
    b, f = R.choice(FINCH)
    k = R.random() < 0.5
    if not once(("fi", b, k)):
        return None
    if k:
        return item("On the Galápagos Islands, Darwin saw a finch with %s. What is it adapted for?" % b, f, [x[1] for x in FINCH if x[0] != b], "Beak shape matches the food.")
    return item("Which Galápagos finch beak is best for %s?" % f, b, [x[0] for x in FINCH if x[1] != f], "Beak shape matches the food.")


def g_moth():
    who = P.next()[0]
    rows = [(1848, R.choice([1, 2])), (1895, R.choice([90, 95, 98])), (1950, R.choice([90, 92, 95])), (1990, R.choice([30, 40, 50])), (2010, R.choice([5, 8, 10]))]
    k = R.choice(["read", "rise", "fall", "why", "diff"])
    if not once(("mo", k, tuple(v for _, v in rows))) or (k in ("rise", "fall", "why") and not once(("mk", k), 3)):
        return None
    tab = table(["Year", "Dark peppered moths near Manchester (%)"], [[str(y), str(v)] for y, v in rows])
    intro = tab + "%s found these records about peppered moths. " % who
    if k == "read":
        y, v = R.choice(rows)
        a = "%d%%" % v
        return item(intro + "What percentage of moths were dark in %d?" % y, a, uniq(a, ["%d%%" % x for _, x in rows] + ["%d%%" % (100 - v)]), "Read the %d row." % y)
    if k == "rise":
        return item(intro + "Why did dark moths become common by 1895?", "Soot made tree bark black, so dark moths were hidden from birds and survived to breed.",
                    ["The moths painted themselves black.", "Soot landed on the moths' wings and stayed.", "Birds preferred to eat dark moths."], "Natural selection: better camouflage, more survivors.")
    if k == "fall":
        return item(intro + "Why did dark moths become rare again after 1950?", "Cleaner air made tree bark pale again, so pale moths were better hidden.",
                    ["Dark moths moved to the sea.", "The moths decided to change colour.", "People caught all the dark moths."], "The environment changed back.")
    if k == "why":
        return item(intro + "What do these records show?", "A population can change over generations when its environment changes.",
                    ["Moths never change.", "One moth changed colour during its life.", "Soot creates new moths."], "Evolution can be observed.")
    d = rows[1][1] - rows[0][1]
    a = "%d percentage points" % d
    return item(intro + "By how much did the percentage of dark moths rise from %d to %d?" % (rows[0][0], rows[1][0]), a,
                uniq(a, ["%d percentage points" % rows[1][1], "%d percentage points" % (rows[1][1] + rows[0][1]), "%d percentage points" % (rows[2][1] - rows[0][1] + 10), "%d percentage points" % (100 - d)]),
                "%d − %d = %d." % (rows[1][1], rows[0][1], d))


NS = ["Animals of one kind vary: some are slightly different from others.", "The environment changes or food is hard to find.",
      "Those best suited to the environment are more likely to survive.", "The survivors breed and pass on their useful characteristics.",
      "Over many generations, the useful characteristic becomes common."]


def g_ns():
    i = R.randrange(len(NS) - 1)
    k = R.random() < 0.5
    if not once(("ns", i, k)):
        return None
    if k:
        a = NS[i + 1]
        return item("Natural selection: \"%s\" What happens next?" % NS[i], a, R.sample([x for x in NS if x not in (a, NS[i])], 3), "Variation → change → survival → breeding → many generations.")
    a = NS[i]
    return item("Natural selection: \"%s\" What comes just before this?" % NS[i + 1], a, R.sample([x for x in NS if x not in (a, NS[i + 1])], 3), "Variation → change → survival → breeding → many generations.")


B1 = bank([
    ("What is an adaptation?", "a feature that helps a living thing survive in its habitat", ["a change an animal decides to make", "a type of habitat", "a fossil"], "Adaptations are inherited."),
    ("What is evolution?", "the slow change of living things over many generations", ["a change in one animal's life", "the way rocks form", "a type of weather"], "Over very long times."),
    ("Who wrote On the Origin of Species in 1859?", "Charles Darwin", ["Mary Anning", "Isaac Newton", "Gregor Mendel"], "He sailed on HMS Beagle."),
    ("Which scientist came up with the idea of natural selection at the same time as Darwin?", "Alfred Russel Wallace", ["Alexander Fleming", "Carl Linnaeus", "William Harvey"], "Wallace worked in South-East Asia."),
    ("Where did Darwin study finches with different beaks?", "the Galápagos Islands", ["the Arctic", "Lyme Regis", "the Moon"], "Islands in the Pacific Ocean."),
    ("Can a giraffe stretch its neck and pass a longer neck to its babies?", "No. Changes during an animal's life are not inherited.", ["Yes, always.", "Yes, if it stretches every day.", "Only female giraffes can."], "Only inherited features pass on."),
    ("How long does evolution of a new species usually take?", "many thousands or millions of years", ["one day", "one year", "one lifetime"], "Many generations."),
    ("Why might an animal not survive if its habitat changes quickly?", "Its adaptations may no longer suit the new conditions.", ["Animals cannot die.", "It will evolve overnight.", "Habitats never change."], "Adaptations suit one environment."),
])
B5 = bank([
    ("Bacteria that are not killed by an antibiotic survive and multiply. What is this an example of?", "natural selection", ["selective breeding", "fossil formation", "photosynthesis"], "Antibiotic resistance."),
    ("How is selective breeding different from natural selection?", "In selective breeding, people choose which ones breed.", ["They are exactly the same.", "Natural selection is done by farmers.", "Selective breeding takes millions of years."], "Who chooses?"),
    ("Why is the variation within a species important for evolution?", "Without differences, nature has nothing to select from.", ["Variation stops evolution.", "All animals are identical.", "Evolution needs no variation."], "Variation is the raw material."),
    ("A rabbit population moves to a snowy island. Which rabbits are most likely to survive over time?", "rabbits with paler fur that are harder for predators to see", ["rabbits with bright orange fur", "rabbits with the shortest legs", "rabbits that cannot hear"], "Camouflage."),
    ("Why do scientists say evolution explains why fossils differ from today's animals?", "Living things have changed over many generations.", ["Fossils are fake.", "Animals have never changed.", "Fossils come from other planets."], "Fossils and evolution fit together."),
])


def body():
    think = ("<p><b>Living things are adapted to their environment, and over many generations they evolve.</b></p>"
             "<ul><li>Adaptations are inherited features, such as a polar bear's thick fat or a cactus's spines.</li>"
             "<li>Natural selection: individuals vary; those best suited survive and breed; their useful features pass on; over many generations the species changes.</li>"
             "<li>Darwin (finches) and Wallace worked this out. Peppered moths changed colour as Britain's air changed.</li></ul>")
    ex = [("A finch has a large, strong beak. Food?", ["Strong beaks crack hard things"], "hard seeds"),
          ("Trees go black with soot. Which moths survive?", ["Dark moths are hidden"], "dark moths")]
    mist = ["Thinking an animal changes its body because it wants or needs to.", "Thinking evolution happens in one lifetime.", "Thinking soot turned the moths black."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Adaptation", B1 + [(g_ad, 8), (g_hab, 4)]),
        ("Adapted to habitats", [(g_ad, 14), (g_hab, 6)]),
        ("Darwin's finches", [(g_finch, 8), (g_ns, 8), (g_ad, 4)]),
        ("Peppered moths", [(g_moth, 18), (g_ns, 2)]),
        ("Evolution in action", B5 + [(g_moth, 7), (g_ad, 6), (g_ns, 2)]),
    ])
    make_uk(6, "adaptation-and-evolution", 9, "Evolution and inheritance",
            "Identify how animals and plants are adapted to suit their environment in different ways and that adaptation may lead to evolution.",
            "Adaptation and Evolution",
            "Year 6 Science: Adaptation and Evolution Worksheets (Darwin, Finches, Peppered Moths)",
            "Adaptation and Evolution",
            "Free Year 6 science worksheets on adaptation and evolution: animal and plant adaptations, natural selection, Darwin's finches, peppered moths and Alfred Russel Wallace. 100 questions with answers.",
            "Suited to survive, changed over time.",
            "Adaptations help survival; natural selection changes species over many generations.",
            body(),
            [("What is the difference between adaptation and evolution?", "An adaptation is an inherited feature that helps a living thing survive. Evolution is the slow change of a species over many generations, as useful adaptations become more common."),
             ("How does natural selection work?", "Individuals vary. Those best suited to their environment survive and breed, passing on their features. Over many generations, the species changes."),
             ("What happened to the peppered moths?", "When soot blackened trees in industrial Britain, dark moths were better hidden from birds and became common. When the air was cleaned, pale moths became common again.")],
            sets)


if __name__ == "__main__":
    main()
