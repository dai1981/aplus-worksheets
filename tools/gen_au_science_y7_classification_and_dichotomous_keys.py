# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U01: classifying living things by their features, using and making
dichotomous keys, the main groups of animals and plants, and mammal groups in Australia (monotremes, marsupials, placentals).
  python tools/gen_au_science_y7_classification_and_dichotomous_keys.py
Reuses the UK Year 6 classification and key makers with Australian names; own questions on Australian animals and scientific names.
Wrong answers come from real mistakes: classifying by habitat or size instead of body features, calling spiders insects,
calling a platypus a bird because it lays eggs, and writing key questions that are opinions ("Is it pretty?").
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

K = "gen_uk_science_y6_classification_keys"
C = "gen_uk_science_y6_classifying_living_things"
NA = ["puffin", "stickleback", "blackbird", "otter", "horse chestnut", "holly", "bluebell", "hedgehog", "badger", "robin", "trout", "squirrel"]
k_follow = limit(src(K, "g_follow", drop=NA), 6)
k_split = limit(src(K, "g_split", drop=NA), 6)
k_pair = limit(src(K, "g_pair", drop=NA), 6)
k_count = limit(src(K, "g_count", drop=NA), 3)
k_facts = limit(src(K, "g_facts", drop=NA), 4)
k_b1 = src.B(K, "B1")
k_b5 = src.B(K, "B5", drop=["lose their leaves", "deciduous", "winter"])
c_group = limit(src(C, "g_group", drop=NA), 6)
c_vert = limit(src(C, "g_vert", drop=NA), 4)
c_char = src(C, "g_char", drop=NA)
c_which = limit(src(C, "g_which", drop=NA), 5)
c_odd = limit(src(C, "g_odd", drop=NA), 4)
c_plant = src(C, "g_plant", drop=NA)
c_repro = src(C, "g_repro")
c_b1 = src.B(C, "B1")
c_b5 = src.B(C, "B5")

MAM = [("platypus", "monotreme"), ("short-beaked echidna", "monotreme"), ("red kangaroo", "marsupial"), ("koala", "marsupial"),
       ("common wombat", "marsupial"), ("Tasmanian devil", "marsupial"), ("bilby", "marsupial"), ("sugar glider", "marsupial"),
       ("dingo", "placental mammal"), ("flying fox", "placental mammal"), ("dugong", "placental mammal"), ("hopping mouse", "placental mammal")]
DEF = {"monotreme": "a mammal that lays eggs", "marsupial": "a mammal whose young grow in a pouch", "placental mammal": "a mammal whose young grow inside the mother, fed by a placenta"}


def g_mam():
    o, k = R.choice(MAM)
    if R.random() < 0.6:
        return tq("Which group of mammals does the %s belong to?" % o, k, [x for x in ["monotreme", "marsupial", "placental mammal"] if x != k] + ["reptile"],
                  "A %s is %s." % (k, DEF[k]))
    w = [x for x, y in MAM if y != k]
    return tq("Which of these animals is %s?" % DEF[k], o, R.sample(w, 3), "The %s is a %s." % (o, k))


SCI = [("koala", "Phascolarctos cinereus"), ("platypus", "Ornithorhynchus anatinus"), ("emu", "Dromaius novaehollandiae"),
       ("laughing kookaburra", "Dacelo novaeguineae"), ("thorny devil", "Moloch horridus"), ("Tasmanian devil", "Sarcophilus harrisii")]

POOL1 = pool(R, [
    ("Why do scientists classify living things?", "to organise them into groups by shared features so they are easier to study", ["to give them nicknames", "to sort them by size only", "to decide which ones are pretty"], "Classification shows relationships."),
    ("What is a dichotomous key?", "a key with pairs of choices at each step that lead to the name of an organism", ["a list of animals in alphabetical order", "a map of habitats", "a key that opens a cage"], "Dichotomous means dividing into two."),
    ("Which is the best question for a dichotomous key?", "Does it have six legs?", ["Is it pretty?", "Is it big?", "Do I like it?"], "Key questions must be about features anyone can observe."),
    ("Why is a spider not an insect?", "It has eight legs and two body parts; insects have six legs and three body parts.", ["It has wings.", "It lives on land.", "It is too small."], "Spiders are arachnids."),
    ("A platypus has fur, lays eggs and feeds its young milk. Which group is it in?", "mammals (monotremes)", ["birds", "reptiles", "fish"], "Fur and milk make it a mammal."),
    ("What is the scientific name of the koala?", "Phascolarctos cinereus", ["Ornithorhynchus anatinus", "Dromaius novaehollandiae", "Moloch horridus"], "Scientific names have two parts: genus and species."),
    ("Why do scientists use two-part Latin names?", "Every scientist in the world can use the same name for a species.", ["Latin names are shorter.", "They are easier to spell.", "Common names are not allowed."], "Common names differ from place to place."),
    ("Which feature do all vertebrates share?", "a backbone", ["feathers", "six legs", "a shell"], "Fish, amphibians, reptiles, birds and mammals are vertebrates."),
    ("Which group do frogs belong to?", "amphibians", ["reptiles", "fish", "mammals"], "Amphibians usually live in water when young and on land as adults."),
    ("Which is a feature of reptiles such as goannas?", "dry, scaly skin", ["feathers", "moist skin without scales", "fur"], "Reptiles lay eggs with leathery shells on land."),
    ("First Nations Australians have named and grouped plants and animals for tens of thousands of years. What does this show?", "Classification is based on careful observation of features and behaviour.", ["Only modern scientists classify.", "Names are random.", "Grouping is not science."], "Traditional knowledge includes detailed classification."),
])
POOL5 = pool(R, [
    ("Mia's key starts 'Does it live in water?' Why is this a weak first question?", "Habitat is not a body feature; very different animals live in water.", ["It is too long.", "It has two answers.", "Animals cannot live in water."], "Use features of the organism."),
    ("Jack finds a new insect. Which feature should he look at first in a key to insects?", "whether it has wings", ["where he found it", "how fast it moves today", "its favourite food"], "Use clear, observable features."),
    ("A key has 5 animals. What is the smallest number of questions that can separate them all?", "4", ["2", "5", "10"], "Each question splits one group into two, so 5 animals need at least 4 questions."),
    ("Ruby's key question is 'Is it large?' What is the problem?", "Large is not clear; people may answer differently.", ["It has a yes/no answer.", "It is a body feature.", "Nothing is wrong."], "Use measurable features, such as 'Is it longer than 10 cm?'"),
    ("A newly found animal has feathers and lays eggs. Which group should it be placed in?", "birds", ["mammals", "reptiles", "amphibians"], "Feathers are only found in birds."),
    ("Why might scientists change the classification of an animal?", "New evidence, such as DNA, shows it is more closely related to another group.", ["They get bored.", "The animal changes colour.", "Its name is too long."], "Science changes with new evidence."),
])


def main():
    sets = U.sets([
        ("Why classify?", [(POOL1, 6), (c_b1, 5), (c_vert, 4), (k_b1, 3), (c_repro, 2)]),
        ("Animal groups", [(c_group, 6), (c_char, 5), (c_which, 5), (c_odd, 4)]),
        ("Australian mammals and plants", [(g_mam, 10), (c_plant, 5), (POOL1, 4), (c_repro, 1)]),
        ("Dichotomous keys", [(k_follow, 6), (k_split, 5), (k_pair, 5), (k_count, 2), (k_facts, 2)]),
        ("Making and testing keys", [(POOL5, 6), (k_b5, 3), (c_b5, 4), (k_pair, 1), (k_facts, 2), (g_mam, 2), (k_count, 1), (POOL1, 1)]),
    ])
    make_au(YEAR, "classification-and-dichotomous-keys", SORT, "AC9S7U01", "Biological sciences",
            "Investigate the role of classification in ordering and organising the diversity of life on Earth and use and develop "
            "dichotomous keys to classify living things (summary of the Australian Curriculum v9.0 Science content description).",
            "Classification and Dichotomous Keys", "Classification and keys",
            "Free Year 7 science worksheets on classification and dichotomous keys: vertebrate and invertebrate groups, monotremes, "
            "marsupials and placental mammals, scientific names and using keys. 100 questions with answers.",
            "Group living things by shared features.", "A dichotomous key uses yes/no questions about observable features.",
            "<p><b>Scientists classify living things into groups by the features they share.</b></p><ul>"
            "<li>Vertebrates (backbone): fish, amphibians, reptiles, birds, mammals. Invertebrates: insects, arachnids, crustaceans, molluscs, worms.</li>"
            "<li>Australian mammals include monotremes (lay eggs), marsupials (pouch) and placental mammals.</li>"
            "<li>A dichotomous key asks pairs of questions about clear, observable features until only one organism is left.</li></ul>",
            [("Eight legs, two body parts. Group?", ["insects have six legs"], "arachnid"),
             ("A koala: which mammal group?", ["the young grow in a pouch"], "marsupial")],
            ["Classifying by habitat or size instead of body features.", "Calling spiders insects.",
             "Writing key questions that are opinions, such as 'Is it pretty?'"],
            [("What are monotremes?", "Monotremes are mammals that lay eggs. The platypus and the echidnas are the only living monotremes, found in Australia and New Guinea."),
             ("How do I write a good dichotomous key?", "Use questions with only two answers about features anyone can see or measure, such as 'Does it have legs?' Split the group at each step until each organism is on its own."),
             ("Why do species have scientific names?", "A two-part scientific name, such as Phascolarctos cinereus for the koala, is the same in every country, so scientists know exactly which species they mean.")],
            sets)


if __name__ == "__main__":
    main()
