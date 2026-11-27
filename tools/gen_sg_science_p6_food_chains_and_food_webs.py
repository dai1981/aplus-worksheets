# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Food chains and food webs (Interactions)
  python tools/gen_sg_science_p6_food_chains_and_food_webs.py
Food chains and food webs show what eats what and how energy passes from the Sun to producers and then to consumers.
Producers (plants) make food; consumers are herbivores, carnivores or omnivores; predators hunt prey; decomposers
(bacteria and fungi) break down dead matter. Removing one organism affects others in the web.
Singapore webs (mangrove swamp, school garden, pond, coral reef) are in sg_webs.py and drawn with sci_foodweb.picture.
Wrong answers come from real mistakes: "the arrow points to what is eaten", "the Sun is a producer",
"a top predator has no effect on the web", "decomposers are consumers that hunt".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto
import sg_webs
import sci_foodweb as FW

sg_webs.add()
U = Unit(63606)
R = U.R
P = People(R)
DROP = ["blue tit", "sparrowhawk", "periwinkle", "herring gull", "vole", "hedgehog", "oak", "badger", "fox", "rabbit", "woodlouse", "thrush", "wolf", "bear", "acorn", "tawny owl", "wood mouse", "mayfly", "trout"]
FC = use(U, "gen_uk_science_y4_food_chains", drop=DROP)
WEBS = sg_webs.NAMES


def pic(w):
    return "<div class='qfig'>%s</div>" % FW.picture(w)


def intro(w):
    return pic(w) + "Look at the food web of a %s. " % FW.WEBS[w]["name"]


def cons(w):
    return sorted(FW.WEBS[w]["eats"])


def g_eats():
    w = R.choice(WEBS)
    x = R.choice(cons(w))
    d = FW.diet(w, x)
    if not once(("ea", w, x)):
        return None
    a = R.choice(d)
    others = [o for o in FW.organisms(w) if o not in d and o != x]
    if len(others) < 3:
        return None
    return item(intro(w) + "Which of these does the %s eat?" % x, a, R.sample(others, 3), "The arrow points from the food to the %s." % x)


def g_by():
    w = R.choice(WEBS)
    x = R.choice(FW.organisms(w))
    e = FW.eaters_of(w, x)
    if not e or not once(("by", w, x)):
        return None
    a = R.choice(e)
    others = [o for o in cons(w) if o not in e]
    if len(others) < 3:
        return None
    return item(intro(w) + "Which animal eats the %s?" % x, a, R.sample(others, 3), "Follow the arrow away from the %s." % x)


def g_prod():
    w = R.choice(WEBS)
    a = R.choice(FW.WEBS[w]["producers"])
    if not once(("pr", w, a)):
        return None
    return item(intro(w) + "Which organism is a producer?", a, R.sample(cons(w), 3), "Producers are plants that make their own food using light.")


def g_kind():
    w = R.choice(WEBS)
    x = R.choice(cons(w))
    k = FW.kind(w, x)
    if not once(("kd", w, x)):
        return None
    return item(intro(w) + "In this web, the %s eats %s. What kind of consumer is it?" % (x, " and ".join(FW.plural(d) for d in FW.diet(w, x))), k,
                [z for z in ["herbivore", "carnivore", "omnivore", "producer"] if z != k], "Herbivores eat only plants, carnivores only animals, omnivores both.")


def g_chain():
    w = R.choice(WEBS)
    chs = [c for c in FW.chains(w) if len(c) >= 3]
    c = R.choice(chs)
    if not once(("ch", w, tuple(c))):
        return None
    wrong = [" → ".join(c[::-1])]
    sw = list(c)
    sw[0], sw[1] = sw[1], sw[0]
    wrong.append(" → ".join(sw))
    other = [o for o in FW.organisms(w) if o not in c]
    br = list(c)
    br[-1] = R.choice(other) if other else br[-1]
    if " → ".join(br) in [" → ".join(x) for x in FW.chains(w)]:
        br = c[:1] + c[2:]
        wrong.append(" → ".join(br) if len(br) >= 2 else "the Sun → " + " → ".join(c))
    else:
        wrong.append(" → ".join(br))
    return item(intro(w) + "Which food chain is part of this food web?", " → ".join(c), wrong, "Each arrow points from the food to the animal that eats it.")


def g_down():
    w = R.choice(WEBS)
    x = R.choice(FW.organisms(w))
    e = [o for o in FW.eaters_of(w, x) if FW.diet(w, o) == [x]]
    if not e or not once(("dn", w, x)):
        return None
    a = e[0]
    others = [o for o in cons(w) if o not in FW.eaters_of(w, x) and o != x]
    if len(others) < 3:
        return None
    return item(intro(w) + "A disease kills most of the %s. Which population is most likely to decrease first?" % FW.plural(x), "the " + FW.plural(a),
                ["the " + FW.plural(o) for o in R.sample(others, 3)], "The %s eats only %s in this web, so it loses its food." % (a, FW.a(x)))


def g_up():
    w = R.choice(WEBS)
    x = R.choice(cons(w))
    d = [f for f in FW.diet(w, x) if FW.eaters_of(w, f) == [x]]
    if not d or not once(("up", w, x)):
        return None
    a = d[0]
    others = [o for o in FW.organisms(w) if o not in FW.diet(w, x) and o != x]
    if len(others) < 3:
        return None
    return item(intro(w) + "Most of the %s are removed. Which population is most likely to increase at first?" % FW.plural(x), "the " + FW.plural(a),
                ["the " + FW.plural(o) for o in R.sample(others, 3)], "Only the %s eats %s in this web, so fewer of them are eaten." % (x, FW.plural(a)))


def g_count():
    w = R.choice(WEBS)
    n = len(FW.chains(w))
    k = R.choice(["chains", "food"])
    if k == "chains":
        if not once(("cc", w)):
            return None
        return item(intro(w) + "How many food chains are there in this food web?", str(n), [str(v) for v in (n - 1, n + 1, n + 2)], "Trace every path from a producer to an animal that nothing eats.")
    x = R.choice(cons(w))
    m = len(FW.diet(w, x))
    if not once(("cf", w, x)):
        return None
    return item(intro(w) + "How many kinds of food does the %s eat in this web?" % x, str(m), [str(v) for v in range(1, 5) if v != m][:3], "Count the arrows pointing to the %s." % x)


def g_top():
    w = R.choice(WEBS)
    tops = [o for o in cons(w) if not FW.eaters_of(w, o)]
    a = R.choice(tops)
    if not once(("tp", w, a)):
        return None
    others = [o for o in FW.organisms(w) if FW.eaters_of(w, o)]
    return item(intro(w) + "Which organism is not eaten by any other organism in this web?", a, R.sample(others, 3), "No arrow leaves the %s." % a)


def g_pp():
    w = R.choice(WEBS)
    x = R.choice([o for o in cons(w) if FW.kind(w, o) != "herbivore"])
    preys = [f for f in FW.diet(w, x) if f not in FW.PLANTS]
    if not preys or not once(("pp", w, x)):
        return None
    a = R.choice(preys)
    k = R.choice(["prey", "pred"])
    if k == "prey":
        others = [o for o in FW.organisms(w) if o not in FW.diet(w, x) and o != x]
        return item(intro(w) + "The %s is a predator. Which of these is its prey?" % x, a, R.sample(others, 3), "The %s hunts and eats the %s." % (x, a))
    others = [o for o in FW.organisms(w) if o not in FW.eaters_of(w, a) and o != a]
    return item(intro(w) + "The %s is prey. Which of these is its predator?" % a, x, R.sample(others, 3), "The %s hunts and eats the %s." % (x, a))


B1 = bank([
    ("What does a food chain show?", "what eats what, and how energy passes from one living thing to another", ["where animals live", "how animals move", "how plants drink water"], "Energy passes along the chain."),
    ("What is a producer?", "a plant that makes its own food using light", ["an animal that eats plants", "an animal that hunts", "a fungus that breaks down dead things"], "Every food chain starts with a producer."),
    ("What is a consumer?", "an animal that gets energy by eating other living things", ["a plant that makes food", "the Sun", "a rock"], "Consumers cannot make their own food."),
    ("What is a predator?", "an animal that hunts and eats other animals", ["an animal that is hunted", "a plant", "a decomposer"], "The animal hunted is the prey."),
    ("What is a food web?", "several food chains that are linked together", ["one long food chain", "a spider's web", "a list of plants"], "Most animals eat more than one kind of food."),
    ("Which organisms break down dead plants and animals?", "decomposers such as bacteria and fungi", ["producers", "predators", "herbivores"], "They return nutrients to the soil."),
])
B2 = bank([
    ("Why are food webs more realistic than single food chains?", "Most animals eat more than one kind of food and are eaten by more than one animal.", ["Animals only eat one food.", "Food webs are shorter.", "Plants eat animals in food webs."], "Food webs show many links."),
    ("Why are there usually more producers than top consumers?", "Energy is lost at each step, so less energy reaches the top.", ["Top consumers are bigger.", "Producers eat consumers.", "Top consumers make their own food."], "Only part of the energy is passed on."),
    ("What would happen to a food web if all the producers died?", "All the consumers would eventually die from lack of food.", ["Only the plants would die.", "The top predator would increase.", "Nothing would happen."], "Every chain starts with a producer."),
    ("Why are decomposers important in a food web?", "They break down dead matter and return nutrients to the soil for plants.", ["They hunt predators.", "They make food from light.", "They eat living plants only."], "Nutrients are recycled."),
    ("An animal eats both plants and animals. What is it called?", "an omnivore", ["a herbivore", "a carnivore", "a producer"], "Omni- means all."),
    ("An animal eats only plants. What is it called?", "a herbivore", ["a carnivore", "an omnivore", "a decomposer"], "Herbivores are plant-eaters."),
    ("Can an animal be both a predator and prey?", "Yes. A mudskipper eats snails but is eaten by kingfishers.", ["No, never.", "Only plants can.", "Only top predators can."], "Many animals are both."),
    ("Which statement about energy in a food chain is correct?", "Energy passes from the producer to the consumers.", ["Energy passes from the top predator to the plant.", "Energy is created by each animal.", "Energy comes from the soil."], "It flows in the direction of the arrows."),
])
B5 = bank([
    ("Siti counted the animals in a school garden: 120 aphids, 15 ladybirds. Why are there more aphids than ladybirds?", "Each ladybird eats many aphids, and less energy reaches the ladybirds.", ["Aphids eat ladybirds.", "Ladybirds are producers.", "There is no reason."], "Prey usually outnumber predators."),
    ("Farmers released ladybirds into a vegetable farm with many aphids. What is the most likely result?", "The number of aphids decreases.", ["The number of aphids increases.", "The vegetables die.", "The ladybirds eat the vegetables."], "Ladybirds are predators of aphids."),
    ("The number of mosquitoes in a pond fell after guppies were added. Why?", "Guppies eat mosquito larvae.", ["Guppies eat adult mosquitoes in the air.", "Guppies are producers.", "Mosquitoes eat guppies."], "Guppies are used to control mosquito breeding."),
    ("A pupil drew a food chain: grasshopper → grass → mynah. What is wrong?", "The producer (grass) must come first.", ["The mynah must come first.", "Nothing is wrong.", "Grasshoppers are producers."], "Correct: grass → grasshopper → mynah."),
    ("A graph shows that when the number of snakes in a garden fell, the number of mynahs rose. What is the best explanation?", "Fewer mynahs were eaten by snakes.", ["Mynahs eat snakes.", "Snakes are producers.", "Mynahs make their own food."], "Fewer predators means more prey survive."),
])


def body():
    think = ("<p><b>A food chain shows what eats what. The arrow points from the food to the eater, the way energy flows.</b></p>"
             "<ul><li>Energy comes from the <b>Sun</b>. <b>Producers</b> (plants) make food.</li>"
             "<li><b>Consumers</b>: herbivores eat plants, carnivores eat animals, omnivores eat both. Predators hunt prey.</li>"
             "<li>A <b>food web</b> is many food chains linked together.</li>"
             "<li>If one population changes, others in the web change too. <b>Decomposers</b> recycle dead matter.</li></ul>")
    ex = [("In 'algae → snail → mudskipper → kingfisher', what eats the snail?", ["Follow the arrow from the snail"], "The mudskipper."),
          ("If all the mudskippers die, what happens to kingfishers that eat only mudskippers?", ["They lose their food"], "Their number decreases.")]
    mist = ["Reading the arrow as 'eats' and pointing it at the food.",
            "Calling the Sun a producer. The Sun is the source of energy; plants are producers.",
            "Thinking removing a top predator has no effect. Its prey may increase.",
            "Forgetting decomposers, which return nutrients to the soil."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Food chains", B1 + FC.B1 + [(FC.g_word, 4), (FC.g_role, 3)]),
        ("Reading a food web", [(g_eats, 5), (g_by, 5), (g_prod, 3), (g_top, 3), (g_count, 4)]),
        ("Producers and consumers", B2 + [(g_kind, 6), (g_pp, 4), (g_chain, 2)]),
        ("Food chains in a web", [(g_chain, 6), (g_pp, 4), (g_count, 3), (g_eats, 3), (g_by, 2), (FC.g_effect, 2)]),
        ("PSLE-style questions", B5 + FC.B5 + [(g_down, 5), (g_up, 5), (FC.g_effect, 2)]),
    ])
    make_sg(6, "food-chains-and-food-webs", 6, "Interactions", "Interactions within the environment (Food chains and food webs)",
            "Identify producers, consumers (herbivores, carnivores, omnivores), predators and prey, and decomposers. Trace energy from the Sun through food chains and food webs, "
            "and predict how a change in one population affects others in a food web (summary of the MOE Primary Science Syllabus).",
            "Food Chains and Food Webs",
            "Primary 6 Science: Food Chains and Food Webs Worksheets (PSLE Practice with Answers)",
            "Food chains and food webs",
            "Free Primary 6 science worksheets for Singapore pupils on food chains and food webs: producers, consumers, predators and prey, and changes in populations in mangrove, garden, pond and reef webs. PSLE practice with answers.",
            "Arrows show where the energy goes.",
            "Producers start every food chain; consumers eat them.",
            body(),
            [("Which way does the arrow point in a food chain?", "From the food to the animal that eats it. It shows the direction energy flows."),
             ("What is the difference between a food chain and a food web?", "A food chain is one path of feeding. A food web is many food chains linked together."),
             ("What happens if one animal in a food web is removed?", "Its prey may increase, and the animals that eat it may decrease, especially if they have no other food.")],
            sets)


if __name__ == "__main__":
    main()
