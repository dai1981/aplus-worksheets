# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Food Chains and Food Webs (5-LS2-1)
  python tools/gen_us_science_g5_food_webs.py
Producers, consumers (herbivores, carnivores, omnivores) and decomposers; arrows point from the food
to the eater (the way matter and energy move); food chains inside a food web; what happens when one
population changes. Five real ecosystems (meadow, pond, ocean, forest, desert) drawn as pictures.
Wrong answers come from real mistakes: arrows read as "eats", the producer called a consumer,
"only the animal that eats it directly is affected".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, People
import sci_foodweb as FW

U = Unit(50109)
R = U.R
P = People(R)
WEBS = sorted(FW.WEBS)


def cap(s):
    return s[0].upper() + s[1:]


def web():
    return R.choice(WEBS)


def intro(w):
    n = FW.WEBS[w]["name"]
    return fig(FW.picture(w)) + R.choice(["Use the %s food web. " % n, "Look at the %s food web. " % n, "This is %s %s food web. " % ("an" if n[0] in "aeiou" else "a", n)])


# ------------------------------------------------------------ makers
def g_eats():
    w = web()
    x = R.choice(list(FW.WEBS[w]["eats"]))
    d = FW.diet(w, x)
    f = R.choice(d)
    others = [o for o in FW.organisms(w) if o not in d and o != x]
    stem = "What does the %s eat?" % x if len(d) == 1 else "Which of these is food for the %s?" % x
    return item(intro(w) + stem, f, R.sample(others, 3), "The arrow goes from the %s to the %s, so the %s eats %s." % (f, x, x, FW.a(f) if f not in FW.ART else f))


def g_eaten_by():
    w = web()
    cands = [o for o in FW.organisms(w) if FW.eaters_of(w, o)]
    x = R.choice(cands)
    e = R.choice(FW.eaters_of(w, x))
    others = [o for o in FW.WEBS[w]["eats"] if o not in FW.eaters_of(w, x) and o != x]
    if len(others) < 3:
        return None
    return item(intro(w) + "Which animal eats the %s?" % x, e, R.sample(others, 3), "An arrow goes from the %s to the %s." % (x, e))


def g_producer():
    w = web()
    p = R.choice(FW.WEBS[w]["producers"])
    return item(intro(w) + "Which organism is a producer?", p, R.sample(list(FW.WEBS[w]["eats"]), 3),
                cap(p) + " makes its own food using energy from sunlight, air and water. It is a producer.")


def g_kind():
    w = web()
    x = R.choice(list(FW.WEBS[w]["eats"]))
    k = FW.kind(w, x)
    why = {"herbivore": "It eats only plants (producers).", "carnivore": "It eats only animals.", "omnivore": "It eats both plants and animals."}[k]
    d = FW.diet(w, x)
    return item(intro(w) + "In this web, the %s's food is: %s. What kind of consumer is it?" % (x, ", ".join(d)),
                k, [z for z in ["herbivore", "carnivore", "omnivore", "producer"] if z != k], why)


def g_chain():
    w = web()
    chs = [c for c in FW.chains(w) if len(c) >= 3]
    c = R.choice(chs)
    good = " → ".join(c)
    rev = " → ".join(reversed(c))
    orgs = FW.organisms(w)
    bad1 = list(c)
    i = R.randrange(1, len(c))
    swap = [o for o in orgs if o not in c and o not in FW.eaters_of(w, c[i - 1])]
    if not swap:
        return None
    bad1[i] = R.choice(swap)
    bad2 = [c[-1]] + c[:-1]
    w3 = [rev, " → ".join(bad1), " → ".join(bad2)]
    if len(set(w3 + [good])) < 4:
        return None
    return item(intro(w) + "Which food chain is part of this food web?", good, w3,
                "Each arrow points from the food to the eater: %s." % good)


def g_remove():
    w = web()
    opts = []
    for x in FW.organisms(w):
        only = [e for e in FW.eaters_of(w, x) if FW.diet(w, e) == [x]]
        for e in only:
            opts.append((x, e))
    if not opts:
        return None
    x, e = R.choice(opts)
    others = [o for o in FW.WEBS[w]["eats"] if o != e and o != x and x not in FW.diet(w, o)]
    if len(others) < 3:
        others = [o for o in FW.WEBS[w]["eats"] if o != e and o != x]
    return item(intro(w) + "A disease kills most of the %s. Which population would most likely go down first?" % FW.plural(x),
                "the " + e, ["the " + o for o in R.sample(others, 3)],
                "The %s eats only %s. Without them, the %s has little food." % (e, FW.plural(x), e))


def g_increase():
    w = web()
    opts = []
    for x in FW.WEBS[w]["eats"]:
        for prey in FW.diet(w, x):
            if FW.eaters_of(w, prey) == [x]:
                opts.append((x, prey))
    if not opts:
        return None
    x, prey = R.choice(opts)
    others = [o for o in FW.organisms(w) if o not in (x, prey)]
    return item(intro(w) + "Most of the %s are removed from the %s. Which population would most likely go up at first?" % (FW.plural(x), FW.WEBS[w]["name"]),
                "the " + prey, ["the " + o for o in R.sample(others, 3)],
                "Only the %s eats %s. With fewer predators, more %s survive." % (x, FW.plural(prey), FW.plural(prey)))


def g_sun():
    w = web()
    x = R.choice([o for o in FW.WEBS[w]["eats"] if FW.level(w, o) >= 2])
    return item(intro(w) + "The energy in the %s's food first came from" % x, "the sun", ["the soil", "the %s itself" % x, "the water"],
                "Plants (producers) capture energy from sunlight. That energy passes along the food chain to the %s." % x)


def g_count():
    w = web()
    x = R.choice(list(FW.WEBS[w]["eats"]))
    n = len(FW.diet(w, x))
    return item(intro(w) + "How many kinds of food does the %s eat in this web?" % x, str(n), [str(k) for k in (1, 2, 3, 4) if k != n],
                "Count the arrows pointing to the %s: %s." % (x, ", ".join(FW.diet(w, x))))


# ------------------------------------------------------------ bank
B1 = bank([
    ("What is a producer?", "an organism that makes its own food, like a plant", ["an animal that eats plants", "an animal that eats other animals", "a living thing that breaks down dead matter"],
     "Producers, such as plants and algae, use sunlight to make their own food."),
    ("What is a consumer?", "an organism that gets energy by eating other organisms", ["a plant that makes its own food", "the sun", "a rock in the soil"],
     "Animals are consumers. They cannot make their own food."),
    ("A herbivore eats", "only plants", ["only animals", "both plants and animals", "dead matter only"],
     "Rabbits and deer are herbivores."),
    ("A carnivore eats", "only other animals", ["only plants", "only seeds", "nothing"],
     "Hawks and wolves are carnivores."),
    ("An omnivore eats", "both plants and animals", ["only plants", "only animals", "only dead leaves"],
     "Bears and many birds are omnivores."),
    ("In a food chain, what does an arrow show?", "the direction food energy and matter move, from the food to the eater", ["which animal is bigger", "that the first organism eats the second", "where the animal lives"],
     "An arrow from grass to rabbit means the rabbit eats the grass; matter and energy move to the rabbit."),
    ("What is a food web?", "many food chains in one ecosystem that connect", ["a single food chain", "a web made by a spider", "a list of plants"],
     "A food web shows how many food chains overlap, because most animals eat more than one thing."),
    ("Which organisms break down dead plants and animals?", "decomposers, such as fungi and bacteria", ["producers", "carnivores", "herbivores"],
     "Decomposers return matter from dead organisms to the soil."),
    ("Every food chain starts with", "a producer", ["a carnivore", "a decomposer", "a top predator"],
     "Producers make the food that all the other organisms depend on."),
    ("What do we call an animal that hunts and eats other animals?", "a predator", ["a prey animal", "a producer", "a decomposer"],
     "The animal that is eaten is the prey. The hunter is the predator."),
])
B5 = bank([
    ("Why is a food web a better model of an ecosystem than one food chain?", "Most animals eat more than one kind of food, and a web shows all the links.", ["Food chains are always wrong.", "Food webs have no producers.", "Webs show only plants."],
     "One food chain leaves out many feeding links."),
    ("Wolves were brought back to a park where deer had eaten most young trees. Later, more young trees grew. Why?", "Wolves ate some deer, so fewer deer ate the trees.", ["Wolves planted the trees.", "Deer started eating wolves.", "Trees grow faster near wolves."],
     "A change at the top of a food web can spread down to the plants."),
    ("A farmer sprays a field to kill all the insects. Which effect is most likely?", "Birds that eat insects have less food.", ["The grass dies right away.", "Hawks get more food.", "Nothing else changes."],
     "Removing one population affects the animals that eat it."),
    ("Ava says the arrow in “grass → rabbit” means the grass eats the rabbit. How should she read it?", "The arrow shows the rabbit eats the grass (matter moves to the rabbit).", ["She is right.", "The arrow shows the rabbit is bigger.", "The arrow shows the rabbit lives in grass."],
     "Arrows point to the eater, in the direction matter and energy move."),
    ("Which change would affect the most organisms in a food web?", "removing the producers", ["removing one top predator", "adding one more rabbit", "a rainy afternoon"],
     "Every food chain begins with producers, so all consumers depend on them."),
    ("Sea otters eat sea urchins, and sea urchins eat kelp. What happens to the kelp if the sea otters disappear?", "It decreases, because more sea urchins eat it.", ["It increases.", "It stays the same.", "It eats the urchins."],
     "Fewer otters means more urchins, and more urchins eat more kelp."),
])


def body():
    w = "meadow"
    think = ("<p>Every <b>food chain</b> starts with a <b>producer</b> (a plant or algae) that makes its own food using sunlight. "
             "<b>Consumers</b> get matter and energy by eating: <b>herbivores</b> eat plants, <b>carnivores</b> eat animals and <b>omnivores</b> eat both. "
             "<b>Decomposers</b> break down dead organisms.</p>"
             "<p>Arrows point from the food to the eater, in the direction matter and energy move. Many food chains that connect make a <b>food web</b>.</p>"
             + figure(FW.picture(w), "A meadow food web. Grass → rabbit → fox is one food chain inside it."))
    ex = [("In the meadow web, what does the snake eat?", ["Find the arrows that point to the snake.", "They come from the mouse and the frog."], "mice and frogs"),
          ("If most of the grasshoppers died, which animal would lose its only food?", ["The frog eats only grasshoppers.", "The mouse also eats wildflowers, so it has other food."], "the frog")]
    mist = ["Reading the arrow as “eats”: grass → rabbit means the rabbit eats the grass.",
            "Thinking only the animal that eats the lost organism is affected. Changes spread through the whole web.",
            "Forgetting that every food chain starts with a producer and that its energy first came from the sun."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Producers and consumers", B1 + [g_producer, g_kind]),
        ("Reading a food web", [g_eats, g_eaten_by, g_count, (g_producer, 3)]),
        ("Food chains and energy", [g_chain, g_sun, g_kind, (g_eats, 3)]),
        ("What happens when a population changes?", [(g_remove, 8), (g_increase, 8), (g_chain, 4)]),
        ("Ecosystem problems", B5 + [g_remove, g_increase, g_eaten_by, g_sun]),
    ])
    make("grade-5", "food-webs", 9, "5-LS2-1",
         "Develop a model to describe the movement of matter among plants, animals, decomposers, and the environment.",
         "Food Chains and Food Webs",
         "Grade 5 Food Web Worksheets: Producers, Consumers, Food Chains and Ecosystems",
         "Food Webs",
         "Free Grade 5 science worksheets on food chains and food webs (NGSS 5-LS2-1): producers, herbivores, carnivores, omnivores and decomposers, reading arrows, and what happens when a population changes. 100 practice questions with answers.",
         "Arrows in a food web point from the food to the eater.",
         "Every food chain starts with a producer. Matter and energy move along the arrows, and a change in one population affects the whole web.",
         body(),
         [("What is the difference between a food chain and a food web?", "A food chain shows one path of food, like grass → rabbit → fox. A food web shows many connected food chains in an ecosystem."),
          ("Which way do the arrows point in a food web?", "From the food to the eater. They show the direction matter and energy move."),
          ("What are producers, consumers and decomposers?", "Producers make their own food from sunlight. Consumers eat other organisms. Decomposers break down dead organisms and return matter to the soil."),
          ("What happens if one animal disappears from a food web?", "Animals that eat it may lose food and decrease, and the organisms it ate may increase. The change can spread through the whole web.")],
         sets)


if __name__ == "__main__":
    main()
