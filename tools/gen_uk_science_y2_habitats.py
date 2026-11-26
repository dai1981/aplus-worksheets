# -*- coding: utf-8 -*-
"""
UK Year 2 science: Habitats (Living things and their habitats)
  python tools/gen_uk_science_y2_habitats.py
Most living things live in habitats to which they are suited; habitats provide the basic needs of animals and plants
(food, water, shelter); naming plants and animals in woodland, pond, seashore, ocean, desert and polar habitats; how
features suit a habitat; and counting animals seen in different habitats (tables and bar charts).
Wrong answers come from real mistakes: "animals can live anywhere", "a habitat is just a house", "fish can live on
land", "polar bears live with penguins".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, bar_chart, fig, People, once
from uk_ks1 import card
import sci_kids as K

U = Unit(61202)
R = U.R
P = People(R)

HOME = [("a crab", "the seashore"), ("a limpet", "the seashore"), ("a starfish", "the seashore"), ("seaweed", "the seashore"),
        ("a squirrel", "a woodland"), ("an owl", "a woodland"), ("a badger", "a woodland"), ("bluebells", "a woodland"), ("an oak tree", "a woodland"),
        ("a frog", "a pond"), ("a duck", "a pond"), ("a newt", "a pond"), ("a water lily", "a pond"), ("a pond snail", "a pond"),
        ("a camel", "a desert"), ("a cactus", "a desert"), ("a scorpion", "a desert"),
        ("a polar bear", "the Arctic"), ("an Arctic fox", "the Arctic"), ("a penguin", "the Antarctic"),
        ("a whale", "the ocean"), ("a shark", "the ocean"), ("a dolphin", "the ocean")]
HABS = ["the seashore", "a woodland", "a pond", "a desert", "the Arctic", "the Antarctic", "the ocean"]


def g_home():
    a, h = R.choice(HOME)
    k = R.random() < 0.6
    if k:
        if not once(("ho", a)):
            return None
        w = [x for x in HABS if x != h and not ({x, h} == {"the Arctic", "the Antarctic"})]
        return item("Which habitat does %s live in?" % a, h, R.sample(w, 3), "Living things live where they can get what they need.")
    if not once(("hw", h), 3):
        return None
    w = R.sample([x[0] for x in HOME if x[1] != h and not ({x[1], h} == {"the Arctic", "the Antarctic"})], 3)
    return item("Which of these lives in %s: %s?" % (h, " or ".join([", ".join(sorted([a] + w)[:3]), sorted([a] + w)[3]])), a, w, "Each habitat has its own plants and animals.")


SUIT = [("a polar bear", "thick white fur and a layer of fat", "keep warm in the cold Arctic"), ("a camel", "wide feet and a hump of fat", "walk on sand and go a long time without food"),
        ("a fish", "gills and fins", "breathe and swim under water"), ("a duck", "webbed feet and waterproof feathers", "swim and stay dry in a pond"),
        ("a cactus", "a thick stem that stores water", "live where it hardly rains"), ("a crab", "a hard shell", "stay safe when waves bash it on the rocks"),
        ("a penguin", "a thick layer of fat and short, tight feathers", "keep warm in icy seas"), ("a squirrel", "sharp claws and a long tail", "climb trees and balance on branches"),
        ("an owl", "big eyes and silent wings", "hunt in the dark woods at night"), ("a frog", "long back legs and webbed feet", "jump and swim in and around a pond")]


def g_suit():
    a, f, j = R.choice(SUIT)
    k = R.random() < 0.5
    if not once(("su", a, k)):
        return None
    if k:
        return item("How do the features of %s help it in its habitat? It has %s." % (a, f), "They help it " + j + ".", ["They help it " + x[2] + "." for x in R.sample([x for x in SUIT if x[0] != a], 3)],
                    "Animals are suited to their habitats.")
    return item("Which living thing has features that help it %s?" % j, a, R.sample([x[0] for x in SUIT if x[0] != a], 3), "%s has %s." % (a[0].upper() + a[1:], f))


MOVE = [("A goldfish is taken out of its pond and left on the grass.", "It cannot breathe out of water, so it will die."),
        ("A cactus is planted in a boggy, wet pond edge.", "Too much water will rot it, because it is suited to dry places."),
        ("A polar bear is moved to a hot desert.", "It will get far too hot in its thick fur."),
        ("A woodland squirrel is moved to a field with no trees.", "It will find it hard to find food and shelter."),
        ("A frog's pond dries up in a hot summer.", "It will need to find another damp place to live."),
        ("A crab is put in a garden flower bed.", "It cannot find the sea water and food it needs.")]


def g_move():
    s, a = R.choice(MOVE)
    if not once(("mv", s)):
        return None
    w = [x[1] for x in MOVE if x[1] != a]
    return item("%s What will happen?" % s, a, R.sample(w, 3), "Living things are suited to their own habitat. In the wrong place their needs are not met.")


SITES = {"the pond": (6, 10), "the woodland": (7, 10), "the field": (4, 8), "the playground": (1, 3), "the hedge": (5, 9)}


def g_count():
    who = P.next()[0]
    s = R.sample(sorted(SITES), 4)
    v = [R.randint(*SITES[x]) for x in s]
    if len(set(v)) < 4:
        return None
    k = R.choice(["most", "fewest", "read", "diff"])
    ri = R.randrange(4)
    if not once(("co", tuple(s), tuple(v), k)):
        return None
    short = [x.replace("the ", "") for x in s]
    ch = bar_chart(short, v, "", "bar chart of how many kinds of animals %s found in each place" % who, ymax=10, step=2, w=330, title="Kinds of animals found")
    intro = fig(ch) + "%s's class counted the kinds of animals in four places near school. " % who
    if k == "most":
        a = short[v.index(max(v))]
        return item(intro + "Which place had the most kinds of animals?", a, [x for x in short if x != a], "The tallest bar.")
    if k == "fewest":
        a = short[v.index(min(v))]
        return item(intro + "Which place had the fewest kinds of animals?", a, [x for x in short if x != a], "The shortest bar.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many kinds of animals were found at the %s?" % short[ri], g, [str(x) for x in v if x != v[ri]][:3], "Read the top of the bar.")
    hi, lo = max(v), min(v)
    g = str(hi - lo)
    w = [str(x) for x in (hi, lo, hi + lo, hi - lo + 1, hi - lo - 1) if x != hi - lo and x >= 0]
    return item(intro + "How many more kinds were found in the place with the most than in the place with the fewest?", g, list(dict.fromkeys(w))[:3], "%d − %d = %d." % (hi, lo, hi - lo))


B1 = bank([
    ("What is a habitat?", "the natural home of a plant or animal", ["a kind of food", "a baby animal", "a type of weather"], "Woodland, pond, seashore."),
    ("What does a habitat give an animal?", "food, water and shelter", ["toys and games", "only sunshine", "nothing"], "Its basic needs."),
    ("Why does a fish live in water?", "It breathes with gills under water.", ["It does not like grass.", "Water is warmer than land.", "Fish can live anywhere."], "Suited to water."),
    ("Which habitat is very cold and icy?", "the Arctic", ["a desert", "a woodland", "a pond"], "Near the North Pole."),
    ("Which habitat is very hot and dry?", "a desert", ["the Arctic", "a pond", "the ocean"], "Little rain."),
    ("Do polar bears and penguins live together?", "No. Polar bears live in the Arctic; penguins live in the Antarctic.", ["Yes, at the North Pole.", "Yes, in the desert.", "Yes, in woodlands."], "Opposite ends of the Earth."),
    ("Which animal would you find in a woodland in the UK?", "a badger", ["a camel", "a shark", "a penguin"], "Badgers dig setts in woods."),
    ("Which animal would you find in a rock pool at the seashore?", "a crab", ["a squirrel", "a camel", "an owl"], "Rock pools are seashore homes."),
])
B5 = bank([
    ("Why do different habitats have different animals?", "Each animal is suited to the place where it lives.", ["Animals choose by colour.", "All animals can live anywhere.", "Habitats are all the same."], "Suited to the habitat."),
    ("A new road is built through a woodland. Why might this be a problem for badgers?", "It takes away part of their habitat and makes it harder to find food.", ["Badgers like roads.", "It gives them more trees.", "It makes no difference."], "Protect habitats."),
    ("How could you find out which animals live in a hedge?", "Look carefully and record what you see.", ["Guess.", "Cut the hedge down.", "Ask a car."], "Observe and record."),
    ("Why should you put animals back where you found them?", "So they stay in the habitat that gives them what they need.", ["So they get lost.", "It does not matter.", "So they can go to a new place."], "Care for living things."),
    ("Why do ponds in gardens help wildlife?", "They give frogs, insects and birds water, food and a place to live.", ["They scare animals away.", "Ponds are only for fish shops.", "Animals do not need water."], "Making habitats."),
])


def body():
    pic = K.row(["fish", "frog", "duck"], words=["fish", "frog", "duck"], size=90, label="a fish, a frog and a duck, which live in a pond habitat")
    ex = [("Where does a camel live?", ["Hot and dry"], "a desert"),
          ("Why does a polar bear have thick fur?", ["Very cold place"], "to keep warm")]
    mist = ["Thinking animals can live anywhere.", "Thinking a habitat is just a house.", "Thinking polar bears live with penguins."]
    return kid_lesson(pic, "A habitat gives food, water and shelter.",
                      ["Woodland, pond, seashore, ocean, desert and polar lands are habitats.", "Living things are suited to their habitat.", "In the wrong habitat, a living thing cannot get what it needs."], ex, mist)


def main():
    sets = U.sets([
        ("What is a habitat?", B1 + [(g_home, 12)]),
        ("Who lives where?", [(g_home, 14), (g_suit, 6)]),
        ("Suited to a habitat", [(g_suit, 12), (g_move, 6), (g_home, 2)]),
        ("Counting animals", [(g_count, 20)]),
        ("Caring for habitats", B5 + [(g_count, 9), (g_home, 4), (g_suit, 2)]),
    ])
    make_uk(2, "habitats", 2, "Living things and their habitats",
            "Identify that most living things live in habitats to which they are suited and describe how different habitats provide for the basic needs of different kinds of animals and plants, and how they depend on each other. "
            "Identify and name a variety of plants and animals in their habitats.",
            "Habitats",
            "Year 2 Science: Habitats Worksheets (Woodland, Pond, Seashore, Desert, Arctic)",
            "Habitats",
            "Free Year 2 science worksheets on habitats: woodland, pond, seashore, ocean, desert and polar habitats, how animals are suited to them and counting animals. 100 questions with answers.",
            "A habitat is a natural home.",
            "It gives food, water and shelter. Animals are suited to their habitat.",
            body(),
            [("What is a habitat?", "The natural home of a plant or animal. It gives the living thing the food, water and shelter it needs."),
             ("Why do animals live in different habitats?", "Each animal is suited to its habitat. A fish has gills for water; a polar bear has thick fur for the cold."),
             ("What habitats are there?", "Woodlands, ponds, the seashore, the ocean, deserts, rainforests and the icy Arctic and Antarctic are all habitats.")],
            sets)


if __name__ == "__main__":
    main()
