# -*- coding: utf-8 -*-
"""
UK Year 1 science: Animal Groups (Animals, including humans)
  python tools/gen_uk_science_y1_animal_groups.py
Identify and name a variety of common animals including fish, amphibians, reptiles, birds and mammals: sorting
animals into groups, the features of each group (fur, feathers, scales, fins, moist skin), and tricky animals
(whales, bats, penguins). Picture questions use simple drawings.
Wrong answers come from real mistakes: "a whale is a fish", "a bat is a bird", "a penguin is not a bird because it
cannot fly", "a frog is a reptile".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, People, once
from uk_ks1 import card, name
import sci_kids as K

U = Unit(61104)
R = U.R
P = People(R)

GR = {"fish": ["a goldfish", "a shark", "a salmon", "a trout", "a cod", "a stickleback", "a tuna", "a clownfish"],
      "amphibians": ["a frog", "a toad", "a newt", "a salamander", "a tree frog"],
      "reptiles": ["a snake", "a lizard", "a tortoise", "a crocodile", "a turtle", "a gecko", "an adder"],
      "birds": ["a robin", "a penguin", "an owl", "a duck", "an eagle", "a pigeon", "an ostrich", "a parrot", "a swan", "a blackbird"],
      "mammals": ["a dog", "a cat", "a human", "a whale", "a bat", "a horse", "a mouse", "a dolphin", "an elephant", "a rabbit", "a lion", "a squirrel", "a cow"]}
G = sorted(GR)


def g_group():
    gname = R.choice(G)
    a = R.choice(GR[gname])
    if not once(("gr", a)):
        return None
    return item("Which animal group does %s belong to?" % a, gname, R.sample([x for x in G if x != gname], 3),
                "Fish, amphibians, reptiles, birds and mammals are animal groups.")


def g_pick():
    gname = R.choice(G)
    a = R.choice(GR[gname])
    others = [x for g in G if g != gname for x in GR[g]]
    if not once(("pk", a)):
        return None
    w = R.sample(others, 3)
    o = sorted([a] + w)
    sing = {"fish": "a fish", "amphibians": "an amphibian", "reptiles": "a reptile", "birds": "a bird", "mammals": "a mammal"}[gname]
    return item("Which of these is %s: %s or %s?" % (sing, ", ".join(o[:3]), o[3]), a, w, "Think about the animal's body covering and how it has young.")


FEAT = [("feathers and a beak", "birds"), ("fur or hair", "mammals"), ("scales and fins, and breathes with gills", "fish"),
        ("dry, scaly skin and lays eggs on land", "reptiles"), ("smooth, damp skin and lives on land and in water", "amphibians"),
        ("babies that drink their mother's milk", "mammals"), ("eggs with hard shells, kept warm in a nest", "birds"), ("young that start life as tadpoles", "amphibians")]


def g_feat():
    f, gname = R.choice(FEAT)
    if not once(("fe", f)):
        return None
    return item("Which animal group has %s?" % f, gname, R.sample([x for x in G if x != gname], 3), "Each group has its own features.")


PICS = [("fish", "fish"), ("frog", "amphibians"), ("duck", "birds"), ("bird", "birds"), ("cat", "mammals"), ("dog", "mammals"), ("rabbit", "mammals"),
        ("bear", "mammals"), ("squirrel", "mammals")]


def g_pic():
    kind, gname = R.choice(PICS)
    if not once(("pi", kind)):
        return None
    return item(card(kind) + "This is a %s. Which animal group is it in?" % name(kind), gname, R.sample([x for x in G if x != gname], 3), "Look at its body covering.")


TRICK = [("Is a whale a fish or a mammal?", "a mammal: it breathes air and feeds its babies milk", ["a fish, because it swims", "a bird", "an amphibian"]),
         ("Is a bat a bird or a mammal?", "a mammal: it has fur and feeds its babies milk", ["a bird, because it flies", "a reptile", "an insect"]),
         ("Is a penguin a bird?", "Yes. It has feathers and a beak and lays eggs, even though it cannot fly.", ["No, it is a fish.", "No, it is a mammal.", "No, because it cannot fly."]),
         ("Is a frog a reptile or an amphibian?", "an amphibian: it has damp skin and starts life as a tadpole", ["a reptile", "a fish", "a mammal"]),
         ("Is a dolphin a fish?", "No. It is a mammal that breathes air.", ["Yes, because it swims.", "Yes, it has gills.", "No, it is a bird."]),
         ("Are humans animals?", "Yes. Humans are mammals.", ["No, humans are plants.", "No, humans are not living.", "Yes, humans are birds."]),
         ("Is a tortoise an amphibian or a reptile?", "a reptile: it has dry, scaly skin", ["an amphibian", "a mammal", "a bird"]),
         ("Is an ostrich a bird even though it cannot fly?", "Yes. It has feathers and a beak and lays eggs.", ["No, it is a mammal.", "No, it is a reptile.", "No, birds must fly."])]


def g_trick():
    q, a, w = R.choice(TRICK)
    if not once(("tr", q)):
        return None
    return item(q, a, w, "Sort animals by their features, not just how they move.")


B1 = bank([
    ("What covers a bird's body?", "feathers", ["fur", "scales", "damp skin"], "All birds have feathers."),
    ("What covers most mammals' bodies?", "fur or hair", ["feathers", "fins", "shells"], "Dogs, cats and humans."),
    ("What do fish use to breathe under water?", "gills", ["lungs", "beaks", "feathers"], "Gills take air from water."),
    ("Where do amphibians live?", "both on land and in water", ["only in the sea", "only in deserts", "only in trees"], "Frogs and newts."),
    ("What kind of skin do reptiles have?", "dry and scaly", ["soft fur", "feathers", "damp and slimy"], "Snakes and lizards."),
    ("Which group feeds its babies milk?", "mammals", ["birds", "fish", "reptiles"], "Cows, cats, humans."),
    ("Which group of animals has feathers and lays eggs?", "birds", ["mammals", "fish", "amphibians"], "Robins and ducks."),
    ("Which group are you in?", "mammals", ["birds", "fish", "reptiles"], "Humans have hair and drink milk as babies."),
])
B5 = bank([
    ("How could you sort a set of animal pictures?", "into groups such as fish, amphibians, reptiles, birds and mammals", ["by size only", "by colour only", "into big and tiny"], "Classify by features."),
    ("A new animal has fur and feeds its babies milk. Which group is it in?", "mammals", ["birds", "fish", "reptiles"], "Use the features."),
    ("An animal has feathers but cannot fly. Is it still a bird?", "Yes, all animals with feathers are birds.", ["No, birds must fly.", "No, it is a fish.", "It is a mammal."], "Feathers mean bird."),
    ("Why is a whale not a fish?", "It breathes air with lungs and feeds its babies milk.", ["It is too big.", "It lives in the sea.", "It has gills."], "Mammal features."),
    ("Why does a frog need a pond?", "It lays its eggs in water, and tadpoles live in water.", ["Frogs are fish.", "Frogs only eat water.", "There is no reason."], "Amphibians need water."),
])


def body():
    pic = K.row(["fish", "frog", "bird", "cat"], words=["fish", "amphibian", "bird", "mammal"], size=80, label="a fish, an amphibian, a bird and a mammal")
    ex = [("A robin is a?", ["Feathers and a beak"], "bird"),
          ("A whale is a?", ["Breathes air, feeds milk"], "mammal")]
    mist = ["Thinking a whale is a fish.", "Thinking a bat is a bird.", "Thinking a penguin is not a bird."]
    return kid_lesson(pic, "Fish, amphibians, reptiles, birds and mammals.",
                      ["Fish have fins and scales. Birds have feathers.", "Mammals have fur and feed their babies milk.", "Amphibians have damp skin; reptiles have dry, scaly skin."], ex, mist)


def main():
    sets = U.sets([
        ("Animal groups", B1 + [(g_group, 12)]),
        ("Which group?", [(g_group, 10), (g_pic, 9), (g_feat, 1)]),
        ("Features of groups", [(g_feat, 7), (g_pick, 11), (g_group, 2)]),
        ("Tricky animals", [(g_trick, 8), (g_pick, 10), (g_group, 2)]),
        ("Thinking about animals", B5 + [(g_pick, 9), (g_group, 3)]),
    ])
    make_uk(1, "animal-groups", 4, "Animals, including humans",
            "Identify and name a variety of common animals including fish, amphibians, reptiles, birds and mammals. Describe and compare the structure of a variety of common animals.",
            "Animal Groups",
            "Year 1 Science: Animal Groups Worksheets (Fish, Amphibians, Reptiles, Birds, Mammals)",
            "Animal Groups",
            "Free Year 1 science worksheets on animal groups: fish, amphibians, reptiles, birds and mammals, their features, and tricky animals like whales, bats and penguins. 100 questions with answers.",
            "Animals can be sorted into groups.",
            "Sort animals by features such as fur, feathers and scales.",
            body(),
            [("What are the main animal groups?", "Fish, amphibians, reptiles, birds and mammals."),
             ("How do I know which group an animal is in?", "Look at its features. Birds have feathers; mammals have fur and feed babies milk; fish have fins, scales and gills; reptiles have dry scales; amphibians have damp skin."),
             ("Is a whale a fish?", "No. A whale is a mammal. It breathes air and feeds its babies milk.")],
            sets)


if __name__ == "__main__":
    main()
