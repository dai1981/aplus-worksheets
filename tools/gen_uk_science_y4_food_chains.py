# -*- coding: utf-8 -*-
"""
UK Year 4 science: Food Chains (Animals, including humans)
  python tools/gen_uk_science_y4_food_chains.py
Construct and interpret food chains: producers, consumers, predators and prey, what the arrows mean, the Sun as the
source of energy, and what happens when one living thing in a chain changes in number. Real British food chains.
Wrong answers come from real mistakes: "the arrow points to what is eaten", "the producer is an animal",
"removing a predator has no effect", "the top predator is the biggest number".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61406)
R = U.R
P = People(R)

CH = [["grass", "rabbit", "fox"], ["oak leaves", "caterpillar", "blue tit", "sparrowhawk"], ["seaweed", "periwinkle", "crab", "herring gull"],
      ["pondweed", "tadpole", "water beetle", "heron"], ["acorns", "wood mouse", "tawny owl"], ["grain", "field vole", "kestrel"],
      ["lettuce", "slug", "hedgehog", "badger"], ["algae", "mayfly larva", "trout", "otter"], ["dandelion", "snail", "song thrush", "cat"],
      ["phytoplankton", "krill", "whale"], ["nettles", "aphid", "ladybird", "blackbird"]]


def arrow(c):
    return " → ".join(c)


def g_role():
    c = R.choice(CH)
    k = R.choice(["prod", "top", "first", "prey", "pred"])
    i = R.randrange(1, len(c) - 1) if len(c) > 3 else 1
    if not once(("ro", tuple(c), k, i if k in ("prey", "pred") else 0)):
        return None
    intro = "Food chain: <b>%s</b>. " % arrow(c)
    others = lambda a: [x for x in c if x != a] + (["the Sun"] if len(c) == 3 else [])
    if k == "prod":
        return item(intro + "Which is the producer?", c[0], others(c[0])[:3], "The producer makes its own food using sunlight; it is always first.")
    if k == "top":
        return item(intro + "Which is the top predator?", c[-1], others(c[-1])[:3], "The top predator is at the end of the chain; nothing in the chain eats it.")
    if k == "first":
        return item(intro + "Which is the first consumer (it eats the producer)?", c[1], others(c[1])[:3], "It eats the plant at the start of the chain.")
    if k == "prey":
        return item(intro + "What does the %s eat in this chain?" % c[i], c[i - 1], ([x for x in c if x not in (c[i - 1], c[i])] + ["the Sun"])[:3],
                    "The arrow points from the food to the animal that eats it.")
    return item(intro + "What eats the %s in this chain?" % c[i], c[i + 1], ([x for x in c if x not in (c[i + 1], c[i])] + ["the Sun", "nothing"])[:3],
                "The arrow points from the food to the animal that eats it.")


def g_effect():
    c = R.choice(CH)
    i = R.randrange(1, len(c))
    k = R.random() < 0.5
    if not once(("ef", tuple(c), i, k)):
        return None
    intro = "Food chain: <b>%s</b>. " % arrow(c)
    if k:
        a = "There would probably be more %s." % plural(c[i - 1])
        return item(intro + "If all the %s were removed, what would most likely happen first?" % plural(c[i]), a,
                    ["There would probably be fewer %s." % plural(c[i - 1]), "Nothing would change.", "The Sun would stop shining."], "With no %s eating them, more %s survive." % (plural(c[i]), plural(c[i - 1])))
    return item(intro + "If the number of %s fell, what would most likely happen to the %s?" % (plural(c[i - 1]), plural(c[i])), "There would be less food, so their numbers would fall.",
                ["Their numbers would rise.", "Nothing would happen.", "They would become producers."], "Animals depend on what they eat.")


IRR = {"grass": "grass", "oak leaves": "oak leaves", "seaweed": "seaweed", "pondweed": "pondweed", "acorns": "acorns", "grain": "grain", "lettuce": "lettuce",
       "algae": "algae", "dandelion": "dandelions", "phytoplankton": "phytoplankton", "nettles": "nettles", "krill": "krill", "trout": "trout",
       "mouse": "mice", "wood mouse": "wood mice", "field vole": "field voles", "fox": "foxes", "mayfly larva": "mayfly larvae", "periwinkle": "periwinkles",
       "herring gull": "herring gulls", "sparrowhawk": "sparrowhawks", "song thrush": "song thrushes", "tawny owl": "tawny owls", "blue tit": "blue tits",
       "water beetle": "water beetles", "ladybird": "ladybirds", "blackbird": "blackbirds", "caterpillar": "caterpillars", "whale": "whales"}


def plural(w):
    return IRR.get(w, w + ("es" if w.endswith(("sh", "ch", "s", "x")) else "s"))


ROLE = [("producer", "makes its own food using energy from sunlight"), ("consumer", "gets its energy by eating other living things"),
        ("predator", "hunts and eats other animals"), ("prey", "is hunted and eaten by other animals"), ("herbivore", "eats only plants"), ("carnivore", "eats only animals")]


def g_word():
    w, d = R.choice(ROLE)
    k = R.random() < 0.5
    if not once(("wd", w, k)):
        return None
    if k:
        return item("In a food chain, what is a %s?" % w, "a living thing that " + d, ["a living thing that " + x[1] for x in R.sample([x for x in ROLE if x[0] != w], 3)], "Learn the food chain words.")
    return item("Which word describes a living thing that %s?" % d, w, R.sample([x[0] for x in ROLE if x[0] != w], 3), "Learn the food chain words.")


def g_order():
    c = R.choice(CH)
    if not once(("or", tuple(c)), 2):
        return None
    sh = list(c)
    wrong = []
    for _ in range(20):
        R.shuffle(sh)
        if sh != c and arrow(sh) not in wrong:
            wrong.append(arrow(sh))
        if len(wrong) == 3:
            break
    if len(wrong) < 3:
        return None
    return item("Which food chain is in the correct order: %s?" % ", ".join(sorted(c)), arrow(c), wrong, "Start with the producer; each arrow points to the animal that eats it.")


B1 = bank([
    ("What does a food chain show?", "what eats what, and how energy passes from one living thing to another", ["how animals move", "where animals sleep", "how plants drink"], "Arrows show energy flow."),
    ("Which way do the arrows in a food chain point?", "from the food to the animal that eats it", ["from the eater to its food", "always upwards", "from big to small"], "Read arrows as 'is eaten by'."),
    ("Where does the energy in almost every food chain come from first?", "the Sun", ["the soil", "water", "the top predator"], "Plants capture sunlight."),
    ("Why does a food chain always start with a plant (or other producer)?", "Producers make their own food from sunlight.", ["Plants are the biggest.", "Animals cannot eat plants.", "Plants are always eaten last."], "Producers come first."),
    ("What is a predator?", "an animal that hunts other animals for food", ["a plant that makes food", "an animal that is hunted", "an animal that eats only plants"], "Foxes, owls and hawks."),
    ("What is prey?", "an animal that is hunted and eaten", ["an animal that hunts", "a plant", "the Sun"], "Rabbits are prey for foxes."),
    ("Can an animal be both predator and prey?", "Yes, for example a blue tit eats caterpillars but is eaten by sparrowhawks.", ["No, never.", "Only plants can.", "Only the top predator can."], "Middle of the chain."),
    ("What is a top predator?", "an animal at the end of a food chain that nothing in the chain eats", ["the first living thing in a chain", "a plant", "the smallest animal"], "Such as an owl or a fox."),
])
B5 = bank([
    ("Why can a fall in the number of bees affect many animals?", "Bees pollinate plants that many animals depend on for food.", ["Bees are top predators.", "Bees eat all the animals.", "Bees make sunlight."], "Living things depend on each other."),
    ("A farmer uses poison to kill slugs. Why might hedgehog numbers fall?", "Hedgehogs lose food and may eat poisoned slugs.", ["Hedgehogs eat poison.", "Hedgehogs eat grass.", "Slugs eat hedgehogs."], "Effects travel along food chains."),
    ("Why are there usually more plants than rabbits, and more rabbits than foxes?", "Energy is lost at each step, so fewer animals can be supported higher up.", ["Foxes are bigger.", "Rabbits eat foxes.", "Plants are predators."], "Energy decreases along the chain."),
    ("Why are food chains in real habitats joined into food webs?", "Most animals eat more than one kind of food.", ["Animals only eat one food.", "Webs are made by spiders.", "Food chains never connect."], "Many links."),
    ("Owls cough up pellets of bones and fur. What can scientists learn from them?", "what the owl has been eating", ["how old the owl is", "how fast the owl flies", "the owl's colour"], "Evidence of diet."),
])


def body():
    think = ("<p><b>A food chain shows what eats what, starting with a producer.</b></p>"
             "<ul><li>Producers (green plants) make food using sunlight. Consumers eat other living things.</li>"
             "<li>Arrows point from the food to the animal that eats it: grass → rabbit → fox.</li>"
             "<li>Predators hunt prey. If one living thing changes in number, others in the chain are affected.</li></ul>")
    ex = [("grass → rabbit → fox. Producer?", ["The chain starts with it"], "grass"),
          ("If foxes are removed?", ["Fewer rabbits are eaten"], "more rabbits")]
    mist = ["Drawing arrows pointing to the food instead of the eater.", "Thinking the producer is an animal.", "Thinking removing one animal has no effect."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Food chain words", B1 + [(g_word, 12)]),
        ("Reading food chains", [(g_role, 20)]),
        ("Building food chains", [(g_order, 14), (g_role, 6)]),
        ("Changes in a chain", [(g_effect, 20)]),
        ("Food chains in habitats", B5 + [(g_effect, 8), (g_role, 7)]),
    ])
    make_uk(4, "food-chains", 6, "Animals, including humans",
            "Construct and interpret a variety of food chains, identifying producers, predators and prey.",
            "Food Chains",
            "Year 4 Science: Food Chains Worksheets (Producers, Predators and Prey)",
            "Food Chains",
            "Free Year 4 science worksheets on food chains: producers, consumers, predators and prey, what the arrows mean, building chains and what happens when numbers change. 100 questions with answers.",
            "Arrows show who eats whom.",
            "Every chain starts with a producer; the arrow points to the eater.",
            body(),
            [("What is a food chain?", "A diagram showing what eats what. It starts with a producer, such as a plant, and arrows point to the animals that eat it."),
             ("What do the arrows mean?", "Each arrow points from the food to the animal that eats it, showing the direction energy moves."),
             ("What happens if one animal is removed?", "Its prey may increase because fewer are eaten, and its predators may decrease because they have less food.")],
            sets)


if __name__ == "__main__":
    main()
