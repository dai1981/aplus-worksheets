# -*- coding: utf-8 -*-
"""
UK Year 6 science: Classifying Living Things (Living things and their habitats)
  python tools/gen_uk_science_y6_classifying_living_things.py
Vertebrates and invertebrates, the five vertebrate groups, invertebrate groups (insects, arachnids, molluscs,
crustaceans, worms), flowering and non-flowering plants, and the characteristics used to sort them.
Wrong answers come from real mistakes: "a whale is a fish", "a bat is a bird", "a spider is an insect",
"a slow worm is a worm", "a woodlouse is an insect", "grass is not a flowering plant".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61601)
R = U.R
P = People(R)

AN = {"mammal": ["fox", "badger", "hedgehog", "bat", "whale", "dolphin", "rabbit", "otter", "seal", "squirrel", "mole", "horse"],
      "bird": ["robin", "penguin", "owl", "ostrich", "puffin", "swan", "eagle", "blackbird", "kiwi", "pigeon"],
      "fish": ["salmon", "shark", "cod", "trout", "goldfish", "seahorse", "eel", "stickleback"],
      "reptile": ["snake", "lizard", "tortoise", "crocodile", "adder", "slow worm", "turtle", "gecko"],
      "amphibian": ["frog", "toad", "newt", "salamander", "axolotl"],
      "insect": ["bee", "ant", "ladybird", "butterfly", "beetle", "dragonfly", "wasp", "grasshopper"],
      "arachnid": ["spider", "scorpion", "harvestman", "tick"],
      "mollusc": ["snail", "slug", "octopus", "mussel", "squid"],
      "crustacean": ["crab", "lobster", "woodlouse", "shrimp", "barnacle"]}
VERT = ["mammal", "bird", "fish", "reptile", "amphibian"]
INV = ["insect", "arachnid", "mollusc", "crustacean"]
PL = {"mammal": "mammals", "bird": "birds", "fish": "fish", "reptile": "reptiles", "amphibian": "amphibians", "insect": "insects",
      "arachnid": "arachnids", "mollusc": "molluscs", "crustacean": "crustaceans"}
TRICK = {"whale": "Whales breathe air with lungs and feed their young on milk, so they are mammals.",
         "dolphin": "Dolphins breathe air and feed their young on milk: mammals.",
         "bat": "Bats have fur and feed their young on milk: mammals, not birds.",
         "seal": "Seals have fur, breathe air and feed their young on milk.",
         "penguin": "Penguins cannot fly, but they have feathers and lay eggs: birds.",
         "ostrich": "Ostriches cannot fly, but they have feathers: birds.", "kiwi": "Kiwis have feathers and lay eggs: birds.",
         "slow worm": "A slow worm is a legless lizard with dry, scaly skin: a reptile.",
         "eel": "Eels have gills and fins: fish.", "seahorse": "Seahorses have gills and fins: fish.",
         "woodlouse": "A woodlouse has a hard outer shell and 14 legs: a crustacean, not an insect.",
         "spider": "Spiders have 8 legs and 2 body parts: arachnids, not insects.",
         "harvestman": "Harvestmen have 8 legs: arachnids.", "tick": "Ticks have 8 legs: arachnids.",
         "turtle": "Turtles have dry, scaly skin and lay eggs on land: reptiles.", "axolotl": "Axolotls are amphibians that keep their gills.",
         "barnacle": "Barnacles are crustaceans that stick to rocks.", "octopus": "An octopus has a soft body: a mollusc.",
         "squid": "A squid has a soft body: a mollusc."}
CHAR = {"mammal": ["has hair or fur and feeds its young on milk", "breathes with lungs and gives birth to live young that drink milk"],
        "bird": ["has feathers, a beak and lays eggs with hard shells", "has feathers and wings, and lays hard-shelled eggs"],
        "fish": ["lives in water, breathes with gills and has scales and fins", "has fins and scales and takes oxygen from water with gills"],
        "reptile": ["has dry, scaly skin and lays eggs with leathery shells on land", "is cold-blooded with dry scales and lays leathery eggs"],
        "amphibian": ["has moist skin and its young live in water and breathe with gills", "starts life in water as a tadpole-like larva and later lives on land"],
        "insect": ["has six legs and three body parts", "has a head, thorax and abdomen and six jointed legs"],
        "arachnid": ["has eight legs and two body parts", "has eight jointed legs and no antennae"],
        "mollusc": ["has a soft body and often a shell", "has a soft body and moves on a muscular foot"],
        "crustacean": ["has a hard outer shell and many jointed legs, and most live in water", "has a hard outer skeleton, two pairs of antennae and lots of legs"]}


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def why(a, g):
    return TRICK.get(a, "%s is %s." % (cap(an(a)), an(g)))


def cap(s):
    return s[0].upper() + s[1:]


def g_group():
    g = R.choice(VERT + INV)
    a = R.choice(AN[g])
    if not once(("gr", a)):
        return None
    pool = VERT if g in VERT and R.random() < 0.7 else INV if g in INV and R.random() < 0.7 else VERT + INV
    w = R.sample([PL[x] for x in pool if x != g], 3)
    if a == "whale":
        w = ["fish"] + [x for x in w if x != "fish"][:2]
    if a == "bat" or a == "penguin":
        w = ["birds" if a == "bat" else "mammals"] + [x for x in w if x not in ("birds", "mammals")][:2]
    if a == "spider" or a == "woodlouse":
        w = ["insects"] + [x for x in w if x != "insects"][:2]
    if a == "slow worm":
        w = ["worms"] + [x for x in w if x != "worms"][:2]
    return item("Which group does %s belong to?" % an(a), PL[g], w, why(a, g))


def g_which():
    g = R.choice(VERT + INV)
    a = R.choice(AN[g])
    others = [x for x in AN if x != g]
    w = [R.choice(AN[o]) for o in R.sample(others, 3)]
    if not once(("wh", g, a)):
        return None
    return item("Which of these animals is %s?" % an(g), a, w, why(a, g))


def g_char():
    g = R.choice(VERT + INV)
    c = R.choice(CHAR[g])
    if not once(("ch", c)):
        return None
    pool = VERT if g in VERT else INV
    w = R.sample([PL[x] for x in pool if x != g], 3)
    return item("An animal %s. Which group does it belong to?" % c, PL[g], w, "This is a key characteristic of %s." % PL[g])


def g_vert():
    g = R.choice(VERT + INV)
    a = R.choice(AN[g])
    if not once(("vt", a)):
        return None
    ans = "vertebrate" if g in VERT else "invertebrate"
    return item("Is %s a vertebrate or an invertebrate?" % an(a), ans,
                ["invertebrate" if ans == "vertebrate" else "vertebrate", "a plant", "a micro-organism"],
                "Vertebrates have a backbone; invertebrates do not. %s" % why(a, g))


def g_odd():
    g = R.choice(VERT + INV)
    if len(AN[g]) < 3:
        return None
    same = R.sample(AN[g], 3)
    o = R.choice([x for x in AN if x != g])
    odd = R.choice(AN[o])
    if not once(("od", tuple(sorted(same)), odd)):
        return None
    ch = [odd] + same
    return item("Which animal does NOT belong with the others: %s?" % ", ".join(sorted(ch)), odd, same,
                "The other three are %s; %s is %s." % (PL[g], an(odd), "one of the " + PL[o] if o != "fish" else "a fish"))


FLOW = ["oak tree", "daisy", "grass", "sunflower", "apple tree", "holly", "dandelion", "bluebell", "rose", "wheat", "horse chestnut tree"]
NOFL = ["fern", "moss", "pine tree", "liverwort", "fir tree", "horsetail"]


def g_plant():
    k = R.random() < 0.5
    if k:
        a = R.choice(FLOW)
        if not once(("pf", a)):
            return None
        return item("Is %s a flowering or a non-flowering plant?" % an(a), "flowering", ["non-flowering", "a fungus", "a micro-organism"],
                    "%s makes flowers and seeds%s." % (cap(an(a)), " (grass and wheat have small green flowers)" if a in ("grass", "wheat") else ""))
    a = R.choice(NOFL)
    if not once(("pn", a)):
        return None
    how = "spores" if a in ("fern", "moss", "liverwort", "horsetail") else "seeds in cones"
    return item("Is %s a flowering or a non-flowering plant?" % an(a), "non-flowering", ["flowering", "a fungus", "an animal"],
                "%s does not make flowers. It reproduces with %s." % (cap(an(a)), how))


def g_repro():
    a = R.choice(NOFL)
    if not once(("rp", a)):
        return None
    if a in ("pine tree", "fir tree"):
        return item("How does %s reproduce?" % an(a), "with seeds made in cones", ["with spores", "with flowers and fruits", "with eggs"],
                    "Conifers such as pines and firs make seeds in cones.")
    return item("How does %s reproduce?" % an(a), "with spores", ["with seeds in cones", "with flowers and fruits", "with eggs"],
                "Ferns, mosses, liverworts and horsetails make tiny spores.")


B1 = bank([
    ("What does classifying living things mean?", "sorting them into groups by what they have in common", ["giving every animal a pet name", "putting them in order of size", "counting how many there are"], "Scientists sort by observable characteristics."),
    ("What is a vertebrate?", "an animal with a backbone", ["an animal without a backbone", "a plant with flowers", "an animal that lives in water"], "Vertebrates have a spine."),
    ("Which group do most kinds of animal on Earth belong to?", "invertebrates", ["mammals", "birds", "fish"], "About 97% of animal species are invertebrates."),
    ("Who created the system of two-part Latin names, such as Homo sapiens?", "Carl Linnaeus", ["Charles Darwin", "Mary Anning", "Isaac Newton"], "Linnaeus, a Swedish scientist, in the 1700s."),
    ("Which three broad groups are living things often sorted into?", "animals, plants and micro-organisms", ["only animals and plants", "only mammals and birds", "rocks, water and air"], "Micro-organisms are a third big group."),
    ("Which body part do all fish use to breathe?", "gills", ["lungs", "fins", "scales"], "Gills take oxygen from water."),
    ("How do you tell an insect from an arachnid?", "Insects have six legs; arachnids have eight.", ["Insects have eight legs; arachnids have six.", "Arachnids have wings.", "They are the same."], "Count the legs."),
    ("Which characteristic do all mammals share?", "They feed their young on milk.", ["They all live on land.", "They all lay eggs.", "They can all fly."], "Whales and bats are mammals too."),
])
B5 = bank([
    ("A newly found animal has fur, breathes air and feeds its young milk, but lives in the sea. How should it be classified?", "as a mammal", ["as a fish", "as an amphibian", "as a crustacean"], "Classify by characteristics, not by where it lives."),
    ("Why do scientists use characteristics rather than habitat to classify animals?", "Animals in the same habitat can be very different, such as a shark and a whale.", ["Habitats never change.", "Characteristics are easier to spell.", "Habitat is a better guide."], "Shared features show relationships."),
    ("Ella says a slow worm is a worm because it has no legs. What is wrong with her reasoning?", "It has dry, scaly skin and a backbone, so it is a reptile.", ["Nothing; it is a worm.", "It is an amphibian.", "It is an insect."], "Look at more than one characteristic."),
    ("Which question would sort a bee from a spider?", "Does it have six legs?", ["Is it an animal?", "Is it alive?", "Does it have a body?"], "Choose a feature that only one has."),
    ("Why might two scientists classify the same plant differently at first?", "They might choose different characteristics to group by.", ["One must be lying.", "Plants cannot be classified.", "Plants change group every year."], "Classification is based on chosen features."),
])


def body():
    think = ("<p><b>Living things are sorted into groups by the characteristics they share.</b></p>"
             "<ul><li>Animals: vertebrates (backbone) are mammals, birds, fish, reptiles and amphibians; invertebrates (no backbone) include insects, arachnids, molluscs, crustaceans and worms.</li>"
             "<li>Plants: flowering plants make flowers and seeds; non-flowering plants use spores (ferns, mosses) or cones (conifers).</li>"
             "<li>Micro-organisms are tiny living things such as bacteria and some fungi.</li></ul>")
    ex = [("A whale lives in the sea. Is it a fish?", ["It breathes air and feeds its young milk"], "No, it is a mammal."),
          ("A woodlouse has 14 legs and a hard shell. Insect?", ["Insects have 6 legs"], "No, it is a crustacean.")]
    mist = ["Classifying by where an animal lives (a whale is not a fish).", "Calling a spider an insect.", "Thinking grass and trees are not flowering plants."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Vertebrates and invertebrates", B1 + [(g_vert, 8), (g_group, 4)]),
        ("Animal groups", [(g_group, 12), (g_which, 8)]),
        ("Characteristics", [(g_char, 14), (g_which, 6)]),
        ("Plants", [(g_plant, 12), (g_repro, 4), (g_vert, 4)]),
        ("Thinking like a scientist", B5 + [(g_odd, 10), (g_group, 5)]),
    ])
    make_uk(6, "classifying-living-things", 1, "Living things and their habitats",
            "Describe how living things are classified into broad groups according to common observable characteristics and based on similarities and differences, including micro-organisms, plants and animals. "
            "Give reasons for classifying plants and animals based on specific characteristics.",
            "Classifying Living Things",
            "Year 6 Science: Classifying Living Things Worksheets (Vertebrates, Invertebrates, Plants)",
            "Classifying Living Things",
            "Free Year 6 science worksheets on classifying living things: vertebrates and invertebrates, mammals, birds, fish, reptiles, amphibians, insects, arachnids and flowering plants. 100 questions with answers.",
            "Group living things by what they share.",
            "Backbone or not, then fur, feathers, scales or six legs.",
            body(),
            [("How are animals classified?", "First by whether they have a backbone (vertebrates) or not (invertebrates), then by characteristics such as fur, feathers, scales, number of legs or a shell."),
             ("Is a whale a fish?", "No. A whale breathes air with lungs and feeds its young on milk, so it is a mammal, even though it lives in the sea."),
             ("Are spiders insects?", "No. Spiders have eight legs and two body parts, so they are arachnids. Insects have six legs and three body parts.")],
            sets)


if __name__ == "__main__":
    main()
