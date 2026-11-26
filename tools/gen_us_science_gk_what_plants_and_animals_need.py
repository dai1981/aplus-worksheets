# -*- coding: utf-8 -*-
"""
US Kindergarten Science: What Plants and Animals Need (K-LS1-1)
  python tools/gen_us_science_gk_what_plants_and_animals_need.py
Use observations to describe patterns of what plants and animals (including humans) need to survive.
All animals need food, water and air; some eat plants, some eat animals, some eat both. Plants need water and light;
they make their own food. Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "plants eat food like we do", "rocks need water", "all animals eat plants".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, People
import sci_kids as K

U = Unit(9105)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ANIMALS = ["dog", "cat", "bear", "rabbit", "duck", "bird", "frog", "fish", "squirrel", "bee", "butterfly", "worm"]
PLANTS = ["tree", "flower", "plant", "cactus", "sprout"]
THINGS = ["rock", "ball", "block", "cup", "spoon", "crayon", "sock"]
EATS = {"dog": "dog food and meat", "cat": "fish and mice", "bear": "berries, fish and honey", "rabbit": "grass and carrots",
        "duck": "seeds, water plants and bugs", "bird": "seeds and worms", "frog": "bugs", "fish": "tiny plants and animals in the water",
        "squirrel": "nuts and seeds", "bee": "nectar from flowers", "butterfly": "nectar from flowers", "worm": "dead leaves in the soil"}


def g_need():
    k = R.choice(ANIMALS + PLANTS)
    who = P.next()[0]
    plant = k in PLANTS
    q = R.choice(["need", "not"])
    if not once((k, q)):
        return None
    nm = K.name(k)
    if q == "need":
        a = "water and sunlight" if plant else "food, water and air"
        w = ["food, water and air", "toys and blankets", "rocks and sand"] if plant else ["only sunlight", "toys and blankets", "rocks and sand"]
        return item(fig(K.card(k)) + "%s takes care of a %s. What does it need to live?" % (who, nm), a, w, "%s need %s." % ("Plants" if plant else "Animals", a))
    a = "toys" if not plant else R.choice(["candy", "toys"])
    return item(fig(K.card(k)) + "Which one does a %s NOT need to live?" % nm, a, (["water", "sunlight", "air"] if plant else ["food", "water", "air"]), "%s is not a need." % a.capitalize())


def g_eat():
    k = R.choice(sorted(EATS))
    who = P.next()[0]
    if not once(("eat", k)):
        return None
    w = R.sample(sorted({v for x, v in EATS.items() if x != k and v != EATS[k]}), 3)
    return item(fig(K.card(k)) + "%s learns about a %s at the nature center. What does it eat?" % (who, K.name(k)), EATS[k], w, "A %s eats %s." % (K.name(k), EATS[k]))


KIND = {"rabbit": "plants", "squirrel": "plants", "bee": "plants", "butterfly": "plants", "cat": "animals", "frog": "animals", "bear": "both", "duck": "both", "bird": "both"}


def g_kind():
    k = R.choice(sorted(KIND))
    who = P.next()[0]
    if not once(("kind", k)):
        return None
    a = {"plants": "only plants", "animals": "mostly animals", "both": "plants and animals"}[KIND[k]]
    return item(fig(K.card(k)) + "%s reads about a %s. What does it eat?" % (who, K.name(k)), a, [x for x in ["only plants", "mostly animals", "plants and animals"] if x != a] + ["rocks"],
                "Some animals eat plants, some eat animals, and some eat both.")


def g_living():
    q = R.choice(["living", "not"])
    if q == "living":
        a = R.choice(ANIMALS + PLANTS)
        others = R.sample(THINGS, 3)
    else:
        a = R.choice(THINGS)
        others = R.sample(ANIMALS, 2) + [R.choice(PLANTS)]
    kinds = [a] + others
    R.shuffle(kinds)
    if not once((tuple(kinds), q)) or not once(("l", a), 2):
        return None
    L = "ABCD"
    who = P.next()[0]
    pic = K.row(kinds, words=["%s. %s" % (L[i], K.name(k)) for i, k in enumerate(kinds)], size=90)
    i = kinds.index(a)
    qq = "Which one is alive and needs water to live?" if q == "living" else "Which one does NOT need food or water?"
    return item(fig(pic) + "%s looks at these. %s" % (who, qq), "%s (%s)" % (L[i], K.name(a)), ["%s (%s)" % (L[j], K.name(k)) for j, k in enumerate(kinds) if j != i],
                "Living things need water. A %s is %s." % (K.name(a), "alive" if q == "living" else "not alive"))


OBS = [("A plant in a dark closet turns yellow and droopy.", "It needs light."), ("A plant that is not watered wilts.", "It needs water."),
       ("A fish is taken out of the water. It cannot breathe.", "It needs water to get air."), ("A hamster with no food gets weak.", "It needs food."),
       ("A bean plant by the window grows tall and green.", "It got light and water."), ("A puppy pants on a hot day and drinks a lot.", "It needs water."),
       ("A bird visits the feeder every morning.", "It needs food."), ("A cactus lives in the desert with little rain.", "It still needs some water."),
       ("Kids get tired and hungry after playing.", "People need food."), ("A goldfish bowl needs fresh water.", "Fish need clean water.")]


def g_obs():
    s, a = R.choice(OBS)
    who = P.next()[0]
    if not once(s):
        return None
    w = R.sample([x[1] for x in OBS if x[1] != a and x[1].split()[-1] != a.split()[-1]], 2) + ["It needs toys."]
    return item("%s sees this: %s What does it show?" % (who, s), a, w, "Living things need food or light, water and air.")


B1 = bank([
    ("What do all animals need?", "food, water and air", ["toys and books", "only sunlight", "rocks"], "Animals need food, water and air."),
    ("What do plants need?", "water and light", ["food from a store", "toys", "candy"], "Plants make their own food."),
    ("Do plants eat food like we do?", "No. They make their own food with light.", ["Yes, pizza.", "Yes, candy.", "Yes, meat."], "Leaves make food."),
    ("Does a rock need water to live?", "No. A rock is not alive.", ["Yes.", "Yes, a lot.", "Only in summer."], "Only living things need water."),
    ("What do people need to live?", "food, water and air", ["toys and TV", "only candy", "rocks"], "People are animals too."),
    ("Which animal eats only plants?", "a rabbit", ["a cat", "a frog", "a lion"], "Rabbits eat grass and carrots."),
    ("Which animal eats other animals?", "a frog (it eats bugs)", ["a rabbit", "a cow", "a horse"], "Frogs eat bugs."),
    ("Which animal eats both plants and animals?", "a bear", ["a rabbit", "a cow", "a cactus"], "Bears eat berries and fish."),
])
B5 = bank([
    ("Ava puts one plant in a closet and one by the window. Which grows better?", "the one by the window", ["the one in the closet", "both the same", "neither"], "Plants need light."),
    ("Leo forgets to feed his fish. What could happen?", "The fish gets sick or weak.", ["It gets bigger.", "Nothing.", "It turns into a plant."], "Animals need food."),
    ("Mia sees a squirrel burying nuts. Why?", "to have food for later", ["to plant toys", "to play hide and seek with Mia", "to make a bed"], "Animals need food."),
    ("Kai waters one plant and not the other. What pattern will he see?", "The watered plant stays healthy.", ["The dry plant grows more.", "Both grow the same.", "Both turn blue."], "Plants need water."),
    ("Why does a deer drink from a stream?", "Animals need water.", ["To wash its fur.", "To look at fish.", "To cool the stream."], "Water is a need."),
])


def body():
    pic = K.row(["rabbit", "flower", "rock"], words=["food, water, air", "water, light", "nothing"], size=110)
    ex = [("What does a dog need to live?", ["It is an animal."], "food, water and air"),
          ("What does a plant need to live?", ["Plants make food with light."], "water and light")]
    mist = ["Thinking plants eat food like we do.",
            "Thinking rocks need water. They are not alive.",
            "Thinking all animals eat plants."]
    return kid_lesson(pic, "Living things have needs.",
                      ["Animals: food, water, air.", "Plants: water and light.", "Some animals eat plants. Some eat animals."], ex, mist)


def main():
    sets = U.sets([
        ("What do living things need?", B1 + [(g_need, 6), (g_living, 6)]),
        ("Plants and animals", [(g_need, 10), (g_living, 6), (g_obs, 4)]),
        ("What animals eat", [(g_eat, 12), (g_kind, 8)]),
        ("Observing needs", [(g_obs, 6), (g_need, 8), (g_living, 6)]),
        ("Needs detectives", B5 + [(g_living, 8), (g_need, 6), (g_kind, 1)]),
    ])
    make("kindergarten", "what-plants-and-animals-need", 5, "K-LS1-1",
         "Use observations to describe patterns of what plants and animals (including humans) need to survive.",
         "What Plants and Animals Need",
         "Kindergarten Living Things Worksheets: What Plants and Animals Need to Live",
         "Plant and Animal Needs",
         "Free kindergarten science worksheets on what plants and animals need (NGSS K-LS1-1): food, water, air and light, and what animals eat. 100 picture questions with answers.",
         "Living things have needs.",
         "Animals need food, water and air. Plants need water and light.",
         body(),
         [("What do animals need?", "Food, water and air. People are animals too, so we need them as well."),
          ("What do plants need?", "Water and light. Plants make their own food in their leaves."),
          ("Do all animals eat the same food?", "No. Rabbits eat plants, frogs eat bugs and bears eat both plants and animals.")],
         sets)


if __name__ == "__main__":
    main()
