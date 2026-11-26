# -*- coding: utf-8 -*-
"""
UK Year 2 science: Simple Food Chains (Living things and their habitats)
  python tools/gen_uk_science_y2_simple_food_chains.py
Describe how animals obtain their food from plants and other animals, using the idea of a simple food chain, and
identify and name different sources of food (including where our own food comes from).
Wrong answers come from real mistakes: "the arrow points to the thing that gets eaten", "food chains start with an
animal", "milk comes from a factory", "plants eat soil".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, People, once
import sci_kids as K

U = Unit(61204)
R = U.R
P = People(R)

CH = [["grass", "rabbit", "fox"], ["lettuce", "slug", "hedgehog"], ["acorn", "squirrel", "owl"], ["leaves", "caterpillar", "blue tit"],
      ["seeds", "mouse", "owl"], ["grass", "cow", "human"], ["seaweed", "limpet", "crab"], ["pondweed", "tadpole", "fish"],
      ["dandelion", "snail", "thrush"], ["grain", "vole", "kestrel"], ["carrot", "rabbit", "fox"], ["clover", "sheep", "human"]]
A = " → "


def g_eat():
    c = R.choice(CH)
    k = R.choice(["eats1", "eats2", "eaten1", "eaten2"])
    if not once(("ea", tuple(c), k)):
        return None
    intro = "Food chain: <b>%s</b>. " % A.join(c)

    def w(a, subj):
        return ["the " + x for x in c if x not in (a, subj)] + ["the Sun", "the soil"]
    if k == "eats1":
        return item(intro + "What does the %s eat?" % c[1], "the " + c[0], w(c[0], c[1])[:3], "The arrow points from the food to the animal that eats it.")
    if k == "eats2":
        return item(intro + "What does the %s eat?" % c[2], "the " + c[1], w(c[1], c[2])[:3], "The arrow points from the food to the animal that eats it.")
    if k == "eaten1":
        return item(intro + "What eats the %s?" % c[0], "the " + c[1], w(c[1], c[0])[:3], "Follow the arrow from the %s." % c[0])
    return item(intro + "What eats the %s?" % c[1], "the " + c[2], w(c[2], c[1])[:3], "Follow the arrow from the %s." % c[1])


def g_start():
    c = R.choice(CH)
    k = R.choice(["first", "last", "plant"])
    if not once(("st", tuple(c), k)):
        return None
    jumble = sorted(c)
    intro = "These make a food chain: %s. " % ", ".join(jumble)
    if k == "first":
        return item(intro + "Which one comes first in the food chain?", c[0], [c[1], c[2], "the animal at the end"], "A food chain starts with a plant.")
    if k == "last":
        return item(intro + "Which one comes last in the food chain?", c[2], [c[0], c[1], "the plant"], "The last animal eats the one before it.")
    return item(intro + "Which one is a plant?", c[0], [c[1], c[2], "none of them"], "Food chains start with a green plant.")


def g_chain():
    c = R.choice(CH)
    if not once(("ch", tuple(c))):
        return None
    right = A.join(c)
    w = [A.join([c[2], c[1], c[0]]), A.join([c[1], c[0], c[2]]), A.join([c[0], c[2], c[1]])]
    return item("Which food chain is in the right order?", right, w, "Start with the plant; each arrow points to the animal that eats it.")


SRC = [("milk", "an animal (a cow)"), ("eggs", "an animal (a hen)"), ("honey", "an animal (bees)"), ("cheese", "an animal (made from cows' milk)"),
       ("bacon", "an animal (a pig)"), ("fish fingers", "an animal (a fish)"), ("bread", "a plant (wheat)"), ("chips", "a plant (potatoes)"),
       ("an apple", "a plant (an apple tree)"), ("baked beans", "a plant (bean plants)"), ("rice", "a plant (rice plants)"), ("orange juice", "a plant (an orange tree)"),
       ("popcorn", "a plant (maize)"), ("butter", "an animal (made from cows' milk)"), ("lamb chops", "an animal (a sheep)")]


def g_src():
    f, s = R.choice(SRC)
    k = R.random() < 0.6
    if k:
        if not once(("sr", f)):
            return None
        pl = s.startswith("a plant")
        w = R.sample([x[1] for x in SRC if x[1].startswith("a plant") != pl], 2) + [R.choice(["a factory, not a living thing", "the soil, not a living thing", "a rock"])]
        return item("Where does %s come from?" % f, s, w, "All our food comes from plants or from animals.")
    pl = s.startswith("a plant")
    if not once(("sp", pl), 4):
        return None
    yes = [x[0] for x in SRC if x[1].startswith("a plant") == pl]
    no = [x[0] for x in SRC if x[1].startswith("a plant") != pl]
    a = R.choice(yes)
    w = R.sample(no, 3)
    if not once(("sa", a)):
        return None
    o = sorted([a] + w)
    return item("Which of these foods comes from %s: %s or %s?" % ("a plant" if pl else "an animal", ", ".join(o[:3]), o[3]), a, w, "Think about where each food first came from.")


EATS = [("a rabbit", "plants"), ("a cow", "plants"), ("a sheep", "plants"), ("a caterpillar", "plants"), ("a fox", "other animals and some plants"),
        ("an owl", "other animals"), ("a shark", "other animals"), ("a hedgehog", "other animals"), ("a lion", "other animals"), ("a human", "plants and animals"),
        ("a pig", "plants and animals"), ("a badger", "plants and animals")]


def g_food():
    a, f = R.choice(EATS)
    if not once(("fo", a)):
        return None
    w = [x for x in ["plants", "other animals", "plants and animals", "only sunlight"] if x != f and not (f.startswith("other animals and") and x in ("other animals", "plants and animals"))]
    if f == "other animals and some plants":
        f = "plants and animals"
        w = ["only plants", "only sunlight", "only soil"]
    return item("Where does %s get its food from?" % a, f, w[:3], "Animals get their food from plants or from other animals.")


B1 = bank([
    ("What is a food chain?", "a list that shows what eats what", ["a chain made of food", "a list of shops", "a type of necklace"], "Arrows show who eats what."),
    ("What does the arrow in a food chain mean?", "'is eaten by'", ["'eats'", "'is bigger than'", "'lives next to'"], "Grass → rabbit: grass is eaten by the rabbit."),
    ("What does a food chain usually start with?", "a green plant", ["a big animal", "a rock", "a person"], "Plants make their own food."),
    ("Where do plants get their food?", "They make it using sunlight.", ["They eat soil.", "They eat insects.", "People feed them."], "Plants are at the start."),
    ("Can animals make their own food?", "No. They eat plants or other animals.", ["Yes, from sunlight.", "Yes, from soil.", "Only cats can."], "Animals must eat."),
    ("In grass → rabbit → fox, which animal eats the rabbit?", "the fox", ["the grass", "the rabbit", "the Sun"], "Follow the arrow."),
    ("Where does milk come from?", "cows (and some other animals such as goats)", ["a factory only", "plants", "the shop shelf"], "A food from an animal."),
    ("Where does bread come from?", "wheat, a plant", ["a cow", "a chicken", "a rock"], "Flour is made from wheat seeds."),
])
B5 = bank([
    ("In lettuce → slug → hedgehog, what would happen to the hedgehogs if all the slugs disappeared?", "They would have less food.", ["They would have more food.", "Nothing would change.", "They would eat lettuce instead of sleeping."], "Living things depend on each other."),
    ("Why does every food chain start with a plant?", "Plants make their own food; animals cannot.", ["Plants are the biggest.", "Animals are always last.", "Plants eat animals."], "Plants are producers."),
    ("A pupil wrote fox → rabbit → grass. What is wrong?", "The arrows are the wrong way round: it should start with the grass.", ["Nothing is wrong.", "Foxes eat grass.", "It should start with the fox."], "Plants first."),
    ("How could you find out what a garden bird eats?", "Watch it carefully and record what it eats.", ["Guess.", "Ask the bird.", "Look at its colour."], "Observe."),
    ("Which food comes from both a plant and an animal?", "a cheese sandwich", ["an apple", "a glass of milk", "a boiled egg"], "Bread from wheat, cheese from milk."),
])


def body():
    pic = K.row(["leaf", "rabbit", "dog"], words=["grass", "rabbit", "fox"], size=90, label="food chain: grass is eaten by a rabbit, which is eaten by a fox")
    ex = [("Grass → rabbit → fox. What does the fox eat?", ["Follow the arrow"], "the rabbit"),
          ("Where does an egg come from?", ["An animal"], "a hen")]
    mist = ["Thinking the arrow points to the thing that gets eaten.", "Thinking food chains start with an animal.", "Thinking milk comes from a factory."]
    return kid_lesson(pic, "A food chain shows what eats what.",
                      ["It starts with a green plant.", "The arrow means 'is eaten by'.", "All our food comes from plants or animals."], ex, mist)


def main():
    sets = U.sets([
        ("What eats what?", B1 + [(g_food, 8), (g_eat, 4)]),
        ("Reading food chains", [(g_eat, 14), (g_start, 6)]),
        ("Putting chains in order", [(g_chain, 10), (g_start, 10)]),
        ("Where food comes from", [(g_src, 16), (g_food, 4)]),
        ("Thinking about food chains", B5 + [(g_eat, 6), (g_start, 6), (g_src, 3)]),
    ])
    make_uk(2, "simple-food-chains", 4, "Living things and their habitats",
            "Describe how animals obtain their food from plants and other animals, using the idea of a simple food chain, and identify and name different sources of food.",
            "Simple Food Chains",
            "Year 2 Science: Simple Food Chains Worksheets (What Eats What)",
            "Food Chains",
            "Free Year 2 science worksheets on simple food chains: what eats what, reading arrows, putting chains in order and where our food comes from. 100 questions with answers.",
            "A food chain shows what eats what.",
            "It starts with a plant. The arrow means 'is eaten by'.",
            body(),
            [("What is a food chain?", "A food chain shows what eats what, for example grass → rabbit → fox. The grass is eaten by the rabbit, and the rabbit is eaten by the fox."),
             ("Why do food chains start with a plant?", "Plants make their own food using sunlight. Animals cannot, so they eat plants or other animals."),
             ("Where does our food come from?", "All our food comes from plants (bread, apples, chips) or animals (milk, eggs, fish).")],
            sets)


if __name__ == "__main__":
    main()
