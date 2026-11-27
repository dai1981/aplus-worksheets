# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Habitats, populations and communities (Interactions)
  python tools/gen_sg_science_p6_habitats_populations_and_communities.py
A habitat is the place where an organism lives. A population is a group of one kind of organism living in a habitat
at the same time. A community is all the populations living together in a habitat. Environmental factors
(light, temperature, water, air) affect where organisms live and how many there are.
Singapore habitats: pond, mangrove swamp, school field, rocky shore, forest at Bukit Timah, rotting log.
Wrong answers come from real mistakes: "a population is all the animals in a place", "one fish is a population",
"a community includes the water and soil", "a habitat is a group of animals".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, upto

U = Unit(63607)
R = U.R
P = People(R)

# habitat -> organisms (plural, count range)
HAB = {
    "pond": [("guppies", "guppy"), ("water lilies", "water lily"), ("snails", "snail"), ("dragonflies", "dragonfly"), ("frogs", "frog"), ("Hydrilla plants", "Hydrilla plant")],
    "mangrove swamp": [("mudskippers", "mudskipper"), ("mangrove trees", "mangrove tree"), ("fiddler crabs", "fiddler crab"), ("kingfishers", "kingfisher"), ("mangrove snails", "mangrove snail")],
    "school field": [("grasshoppers", "grasshopper"), ("earthworms", "earthworm"), ("mynahs", "mynah"), ("ants", "ant"), ("butterflies", "butterfly"), ("love grass plants", "love grass plant")],
    "rocky shore": [("barnacles", "barnacle"), ("sea anemones", "sea anemone"), ("crabs", "crab"), ("seaweed plants", "seaweed plant"), ("limpets", "limpet")],
    "forest at Bukit Timah": [("long-tailed macaques", "long-tailed macaque"), ("ferns", "fern"), ("tembusu trees", "tembusu tree"), ("squirrels", "squirrel"), ("millipedes", "millipede")],
    "rotting log": [("millipedes", "millipede"), ("earthworms", "earthworm"), ("mushrooms", "mushroom"), ("ants", "ant"), ("centipedes", "centipede")],
}
HN = sorted(HAB)


FEW = {"kingfishers", "long-tailed macaques", "tembusu trees", "mangrove trees", "frogs", "mynahs", "squirrels", "crabs", "fiddler crabs"}


def a_(h):
    return ("on " if h == "rocky shore" else "in ") + ("an " + h if h[0] in "aeiou" else "a " + h)


def at(h):
    return ("on the " if h == "rocky shore" else "in the ") + h


def g_term():
    h = R.choice(HN)
    pl, sg = R.choice(HAB[h])
    k = R.choice(["hab", "pop", "com", "org"])
    if not once(("tm", h, k), 2 if k in ("pop", "org") else 1) or not once(("tm2", pl, k), 1):
        return None
    desc = {"hab": "the %s itself, where the living things are found" % h,
            "pop": "all the %s living %s" % (pl, at(h)),
            "com": "all the different plants and animals living %s" % at(h),
            "org": "one %s %s" % (sg, at(h))}[k]
    ans = {"hab": "a habitat", "pop": "a population", "com": "a community", "org": "an organism"}
    return item("Which word best describes %s?" % desc, ans[k], [v for kk, v in ans.items() if kk != k],
                {"hab": "A habitat is the place where organisms live.",
                 "pop": "A population is one kind of organism in a habitat at the same time.",
                 "com": "A community is all the populations living together in a habitat.",
                 "org": "One living thing is an organism, not a population."}[k])


def g_which():
    h = R.choice(HN)
    k = R.choice(["pop", "com"])
    if not once(("wh", h, k), 2 if k == "pop" else 1):
        return None
    orgs = HAB[h]
    pl, sg = R.choice(orgs)
    o2 = R.choice([o for o in orgs if o[0] != pl])
    if k == "pop":
        return item("Which of these is a population %s?" % at(h), "all the %s %s" % (pl, at(h)),
                    ["all the %s and %s %s" % (pl, o2[0], at(h)), "one %s %s" % (sg, at(h)), "the water and soil of the %s" % h if h != "rocky shore" else "the rocks and sea water of the shore"],
                    "A population is made up of one kind of organism only.")
    return item("Which of these is a community %s?" % at(h), "all the plants and animals living %s" % at(h),
                ["all the %s %s" % (pl, at(h)), "only the animals %s" % at(h), "the %s and the air above it" % h],
                "A community has all the populations: plants and animals together.")


def g_count():
    h = R.choice(HN)
    orgs = R.sample(HAB[h], R.randint(3, len(HAB[h])))
    cnt = [R.randint(1, 8) if o[0] in FEW else R.randint(6, 40) for o in orgs]
    nm = P.next()[0]
    k = R.choice(["pops", "size", "total"])
    tb = table(["Organism", "Number counted"], [[o[0][0].upper() + o[0][1:], str(c)] for o, c in zip(orgs, cnt)])
    if k == "pops":
        if not once(("cp", h, len(orgs)), 1):
            return None
        n = len(orgs)
        return item(tb + "%s counted the organisms %s. How many populations did %s record?" % (nm, a_(h), nm), str(n),
                    [str(sum(cnt)), str(n - 1), str(n + 1)], "Each kind of organism is one population, so there are %d." % n)
    if k == "size":
        i = R.randrange(len(orgs))
        if not once(("cs", h, orgs[i][0])):
            return None
        a = cnt[i]
        w = [str(sum(cnt)), str(len(orgs)), str(a + R.choice([1, 2, 3]))]
        if len(set(w + [str(a)])) < 4:
            return None
        return item(tb + "%s counted the organisms %s. How many organisms make up the population of %s?" % (nm, a_(h), orgs[i][0]), str(a), w,
                    "The population of %s is all the %s: %d." % (orgs[i][0], orgs[i][0], a))
    if not once(("ct", h), 1):
        return None
    t = sum(cnt)
    w = [str(len(orgs)), str(t - cnt[0]), str(max(cnt))]
    if len(set(w + [str(t)])) < 4:
        return None
    return item(tb + "%s counted the organisms %s. How many organisms are there in this community altogether?" % (nm, a_(h)), str(t), w,
                "Add the numbers of all the populations: %d." % t)


# chamber experiments: animal, condition pair, preferred
EXP = [("earthworms", "damp soil", "dry soil", "water"), ("millipedes", "dark side", "bright side", "light"),
       ("earthworms", "dark side", "bright side", "light"), ("millipedes", "damp side", "dry side", "water"),
       ("woodlice", "damp side", "dry side", "water"), ("woodlice", "dark side", "bright side", "light"),
       ("mealworms", "dark side", "bright side", "light"), ("snails", "damp side", "dry side", "water")]


def g_exp():
    an, good, bad, fac = R.choice(EXP)
    k = R.choice(["fact", "pref"])
    if not once(("ex", an, fac, k)):
        return None
    n = R.choice([10, 12, 16, 20])
    g = R.randint(int(n * .7), n - 1)
    nm, he, his = P.next()
    tb = table(["Time", "Number on the %s" % good, "Number on the %s" % bad], [["Start", str(n // 2), str(n - n // 2)], ["After 15 minutes", str(g), str(n - g)]])
    if k == "fact":
        return item(tb + "%s put %d %s in a box. One side was the %s and the other was the %s. Which environmental factor was %s testing?" % (nm, n, an, good, bad, he),
                    {"water": "amount of water", "light": "amount of light"}[fac],
                    [x for x in ["amount of light", "amount of water", "temperature", "amount of food"] if x != {"water": "amount of water", "light": "amount of light"}[fac]],
                    "Only the %s changed between the two sides." % {"water": "amount of water", "light": "amount of light"}[fac])
    return item(tb + "%s put %d %s in a box with a %s and a %s. What does %s result show?" % (nm, n, an, good, bad, his),
                "The %s prefer the %s." % (an, good), ["The %s prefer the %s." % (an, bad), "The %s did not move." % an, "The %s need more food." % an],
                "After 15 minutes, %d of %d were on the %s." % (g, n, good))


B1 = bank([
    ("What is a habitat?", "the place where an organism lives", ["a group of the same kind of animal", "all the plants in a garden", "the food an animal eats"], "A pond, a field and a mangrove swamp are habitats."),
    ("What is a population?", "a group of one kind of organism living in a habitat at the same time", ["all the animals in a habitat", "one organism", "all the plants and animals in a habitat"], "All the guppies in a pond form a population."),
    ("What is a community?", "all the populations of plants and animals living together in a habitat", ["one kind of organism in a habitat", "the place where organisms live", "only the animals in a habitat"], "Plants are part of a community too."),
    ("Which of these is not part of a community?", "the water in a pond", ["the water lilies in a pond", "the guppies in a pond", "the snails in a pond"], "Water is non-living; a community is only living things."),
    ("A pond has guppies, snails, frogs, water lilies and Hydrilla plants. How many populations are there?", "5", ["1", "2", "3"], "Each kind of organism is one population."),
    ("Which habitat is found where the land meets the sea in Singapore and has muddy, salty water?", "mangrove swamp", ["forest", "school field", "pond"], "Sungei Buloh Wetland Reserve has a mangrove swamp."),
    ("Which statement about a habitat is correct?", "A habitat provides food, water, shelter and air for organisms.", ["A habitat has only one kind of organism.", "A habitat is always very large.", "Organisms do not need a habitat."], "Habitats can be big (a forest) or small (a rotting log)."),
    ("A rotting log is home to millipedes, ants and mushrooms. What is the rotting log?", "a habitat", ["a population", "a community", "an organism"], "It is the place where they live."),
])
B2 = bank([
    ("Which environmental factors affect where organisms live?", "light, temperature, water and air", ["only food", "only the colour of the soil", "only the size of the animals"], "These are called physical factors."),
    ("Ferns grow well under tall trees in a forest. Which factor most likely helps them grow there?", "less light and more moisture", ["more sunlight", "very dry soil", "cold air"], "Many ferns grow well in shady, damp places."),
    ("Earthworms come up to the surface of a field after heavy rain. Which factor has changed?", "amount of water in the soil", ["amount of light", "amount of food", "number of birds"], "The soil is full of water, so they come up."),
    ("Water plants such as Hydrilla help fish in a pond. How?", "They give out oxygen when they make food in light.", ["They eat the fish's waste.", "They make the water warm.", "They block all the light."], "Fish need oxygen dissolved in the water."),
    ("Why do fewer plants grow under a big rain tree than in the open field?", "Less light reaches the ground under the tree.", ["The soil is too cold.", "There is no air.", "Plants cannot grow near trees."], "Plants need light to make food."),
    ("Organisms in a community depend on each other. Which is an example?", "Bees get nectar from flowers and help to pollinate them.", ["A rock gives shelter to a fish.", "Rain falls on a pond.", "The Sun heats the soil."], "Both organisms are living."),
    ("Which change would most likely cause the population of guppies in a pond to decrease?", "The pond becomes polluted with oil.", ["More water plants grow in the pond.", "More mosquito larvae hatch.", "Fewer herons visit the pond."], "Oil stops oxygen from entering the water."),
    ("Why do the barnacles on a rocky shore close up at low tide?", "to keep in water so they do not dry out", ["to catch more food", "to keep warm", "to hide from fish"], "At low tide they are out of the water."),
])
B3 = bank([
    ("Mangrove trees give shelter to crabs and mudskippers. What does this show?", "Organisms in a community depend on each other.", ["Mangrove trees eat crabs.", "Crabs make food for the trees.", "Mudskippers are producers."], "Plants give animals food and shelter."),
    ("Why does a pond community have more snails when there are more water plants?", "The snails have more food.", ["The snails make their own food.", "Water plants eat snails.", "Snails do not need food."], "Snails feed on water plants and algae."),
    ("Bats visit durian flowers at night. How does this help the durian trees?", "The bats pollinate the flowers.", ["The bats make the fruit ripen.", "The bats water the trees.", "The bats eat the leaves."], "Pollen sticks to the bats and is carried to other flowers."),
    ("A population of a kind of organism can increase when", "there is more food and fewer predators", ["there is less food", "there are more predators", "the habitat is destroyed"], "Food and predators both affect population size."),
    ("Mosquito larvae live in still water. Why does clearing stagnant water in flower pot plates reduce mosquitoes?", "It removes the habitat where the larvae grow.", ["It kills adult mosquitoes in the air.", "It gives the larvae more food.", "It makes the water warmer."], "This is why Singapore asks people to do the 'Mozzie Wipeout'."),
    ("Which habitat would most likely have the largest community?", "a large forest with many kinds of plants and animals", ["a small puddle", "a flower pot", "a dry rock"], "More food and shelter supports more populations."),
])
B5 = bank([
    ("Mei Ling counted 40 guppies in a pond in January and 12 in June. The pond became very shallow in June. What is the best explanation?", "There was less water and less space, so fewer guppies survived.", ["Guppies prefer shallow water.", "The guppies grew bigger.", "More food grew in the pond."], "A change in a habitat affects the population."),
    ("A gardener cleared all the dead leaves from under a tree. What would most likely happen to the millipedes living there?", "Their population decreases because they lose food and shelter.", ["Their population increases.", "They start to make food.", "Nothing happens to them."], "Millipedes feed on and shelter in dead leaves."),
    ("Ravi wants to find out if earthworms prefer damp or dry soil. Which must he keep the same on both sides?", "the amount of light and the type of soil", ["the amount of water in the soil", "the number of earthworms that move", "nothing at all"], "Only the factor tested may change."),
    ("A pond had many water plants. After they were removed, the fish swam near the surface. Why?", "There was less oxygen in the water.", ["The fish wanted more light.", "The water became warmer.", "There was more food at the surface."], "Water plants add oxygen to the water."),
    ("An oil spill covered a mangrove swamp. Which statement is most likely true?", "Many populations in the community would decrease.", ["Only the trees would be affected.", "The community would grow bigger.", "The mudskippers would increase."], "Organisms in a community depend on each other."),
    ("Siti counted 5 kinds of animals and 3 kinds of plants in a garden. How many populations are there in the community?", "8", ["5", "3", "1"], "Each kind of plant and animal is one population."),
])


def body():
    think = ("<p><b>A habitat is where an organism lives. A population is one kind of organism there. A community is all the populations living together.</b></p>"
             "<ul><li>One guppy is an <b>organism</b>. All the guppies in the pond are a <b>population</b>.</li>"
             "<li>All the plants and animals in the pond together are a <b>community</b>. Water and soil are not part of it.</li>"
             "<li>Environmental factors: <b>light, temperature, water and air</b>. They affect where organisms live.</li>"
             "<li>Organisms in a community depend on each other for food, shelter and pollination.</li></ul>")
    ex = [("A pond has guppies, snails and water lilies. How many populations are there?", ["Count the kinds of organisms"], "3"),
          ("Earthworms move to the damp side of a box. Which factor affects them?", ["Only water changes"], "the amount of water")]
    mist = ["Calling all the animals in a habitat a population. A population is one kind only.",
            "Leaving plants out of a community. Plants are populations too.",
            "Putting water, soil or rocks in a community. A community is only living things.",
            "Changing two factors at once in an experiment."]
    return lesson(think, ex, mist)


C = upto(g_count, 16)


def main():
    sets = U.sets([
        ("Habitats, populations and communities", B1 + [(g_term, 6), (g_which, 4)]),
        ("Which is which?", [(g_term, 8), (g_which, 6), (C, 4)]),
        ("Counting populations", [(C, 8), (g_term, 6), (g_which, 2)] + B3[:3]),
        ("Environmental factors", B2 + [(g_exp, 6)] + B3[3:]),
        ("PSLE-style questions", B5 + [(g_exp, 4), (C, 4), (g_term, 4)]),
    ])
    make_sg(6, "habitats-populations-and-communities", 7, "Interactions", "Interactions within the environment (Habitats, populations and communities)",
            "Recognise that a habitat is the place where an organism lives, a population is a group of one kind of organism living in a habitat, and a community is all the populations "
            "living together in a habitat. Investigate how environmental factors (light, temperature, water and air) affect the distribution of organisms (summary of the MOE Primary Science Syllabus).",
            "Habitats, Populations and Communities",
            "Primary 6 Science: Habitats, Populations and Communities Worksheets (PSLE Practice)",
            "Habitats and communities",
            "Free Primary 6 science worksheets for Singapore pupils on habitats, populations and communities: counting populations, environmental factors and fair experiments. PSLE practice with answers.",
            "One kind = population. All kinds = community.",
            "A habitat is the place where they live.",
            body(),
            [("What is the difference between a population and a community?", "A population is one kind of organism in a habitat. A community is all the populations living there together."),
             ("Is the water in a pond part of the community?", "No. A community is only the living things. Water is part of the habitat."),
             ("Which environmental factors affect organisms?", "Light, temperature, water and air affect where organisms can live and how many there are.")],
            sets)


if __name__ == "__main__":
    main()
