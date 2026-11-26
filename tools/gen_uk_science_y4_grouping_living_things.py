# -*- coding: utf-8 -*-
"""
UK Year 4 science: Grouping Living Things (Living things and their habitats)
  python tools/gen_uk_science_y4_grouping_living_things.py
Living things can be grouped in different ways: vertebrates and invertebrates, flowering and non-flowering plants,
what animals eat, where they live, how many legs they have, and Carroll diagrams.
Reuses the vertebrate and plant questions of the Year 6 unit (new seed) and adds Year 4 grouping questions.
Wrong answers come from real mistakes: "a spider is an insect", "a whale is a fish", "bears only eat meat",
"a snail has legs".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
import gen_uk_science_y6_classifying_living_things as C

C.U = Unit(61401)
C.R = C.U.R
uk_sci.USED.clear()
U, R = C.U, C.R

DIET = {"herbivore": ["rabbit", "cow", "deer", "caterpillar", "snail", "sheep", "horse", "elephant"],
        "carnivore": ["fox", "owl", "shark", "lion", "spider", "eagle", "ladybird", "frog"],
        "omnivore": ["badger", "hedgehog", "brown bear", "human", "pig", "robin", "chicken", "crow"]}
WHAT = {"herbivore": "only plants", "carnivore": "only other animals", "omnivore": "both plants and animals"}


def g_diet():
    t = R.choice(sorted(DIET))
    a = R.choice(DIET[t])
    if not once(("di", a)):
        return None
    return item("Is a %s a herbivore, a carnivore or an omnivore?" % a, "%s %s" % ("an" if t[0] == "o" else "a", t),
                ["%s %s" % ("an" if x[0] == "o" else "a", x) for x in sorted(DIET) if x != t] + ["a producer"], "A %s eats %s." % (t, WHAT[t]))


LEGS = [("spider", "8"), ("ant", "6"), ("woodlouse", "14"), ("snail", "0"), ("beetle", "6"), ("earthworm", "0"), ("harvestman", "8"), ("bee", "6"), ("slug", "0"), ("crab", "10")]


def g_legs():
    a, n = R.choice(LEGS)
    if not once(("lg", a)):
        return None
    return item("How many legs does %s %s have?" % ("an" if a[0] in "aeiou" else "a", a), n, [x for x in ["0", "6", "8", "14", "10", "4"] if x != n][:3] if n != "4" else ["6", "8", "0"],
                "Counting legs is a quick way to group minibeasts: insects 6, spiders 8.")


HAB = [("frog", "pond"), ("newt", "pond"), ("water boatman", "pond"), ("pond skater", "pond"), ("squirrel", "woodland"), ("woodpecker", "woodland"),
       ("badger", "woodland"), ("bluebell", "woodland"), ("crab", "seashore"), ("limpet", "seashore"), ("starfish", "seashore"), ("seaweed", "seashore"),
       ("camel", "desert"), ("cactus", "desert"), ("scorpion", "desert")]


def g_hab():
    a, h = R.choice(HAB)
    if not once(("hb", a)):
        return None
    P_ = {"pond": "in a pond", "woodland": "in woodland", "seashore": "on the seashore", "desert": "in a desert"}
    return item("Where would you most likely find a %s?" % a, P_[h], [P_[x] for x in P_ if x != h], "Living things live where their needs are met.")


CAR = {"frog": (1, 1), "fish": (0, 1), "dog": (1, 0), "snail": (0, 0), "duck": (1, 1), "slug": (0, 0), "otter": (1, 1), "eel": (0, 1), "spider": (1, 0), "earthworm": (0, 0),
       "crab": (1, 1), "jellyfish": (0, 1), "rabbit": (1, 0), "snake": (0, 0)}


def g_carroll():
    a = R.choice(sorted(CAR))
    if not once(("ca", a)):
        return None
    legs, water = CAR[a]
    box = "%s and %s" % ("has legs" if legs else "has no legs", "lives in water" if water else "does not live in water")
    opts = ["has legs and lives in water", "has legs and does not live in water", "has no legs and lives in water", "has no legs and does not live in water"]
    tab = table(["", "Lives in water", "Does not live in water"], [["Has legs", "", ""], ["Has no legs", "", ""]])
    return item(tab + "In which box of this Carroll diagram should a %s go?" % a, box, [x for x in opts if x != box],
                "Ask both questions: does it have legs? Does it live in water?")


B1 = bank([
    ("Why do scientists group living things?", "to make them easier to study and identify", ["to make them grow faster", "to give them names they like", "to make them all the same"], "Grouping shows what they share."),
    ("Which question would sort a bird from a fish?", "Does it have feathers?", ["Is it alive?", "Does it eat food?", "Does it need water?"], "Choose a feature only one has."),
    ("What is a Carroll diagram?", "a table that sorts things by whether they have each of two features", ["a map of a habitat", "a list of animals in size order", "a food chain"], "Yes/no rows and columns."),
    ("Which group includes all animals with a backbone?", "vertebrates", ["invertebrates", "plants", "fungi"], "Mammals, birds, fish, reptiles, amphibians."),
    ("Is a spider an insect?", "No. It has eight legs, so it is an arachnid.", ["Yes, all minibeasts are insects.", "Yes, it has six legs.", "No, it is a mammal."], "Count the legs."),
    ("Which of these is a non-flowering plant?", "a fern", ["a daisy", "an apple tree", "grass"], "Ferns use spores."),
    ("What is an omnivore?", "an animal that eats both plants and animals", ["an animal that eats only plants", "an animal that eats only meat", "a plant that eats insects"], "Humans are omnivores."),
    ("Which group do mushrooms belong to?", "fungi", ["plants", "animals", "insects"], "They do not make their own food."),
])
B5 = bank([
    ("A pupil groups animals by colour. Why is this not very useful for scientists?", "Colour can vary within one kind of animal and does not show how they are related.", ["Colour is always the same.", "Scientists cannot see colour.", "It is the best way."], "Choose useful features."),
    ("Two pupils sort the same animals into different groups. Can both be right?", "Yes, if each grouping is based on clear features.", ["No, there is only one way.", "No, grouping is not science.", "Only if they use colours."], "Many ways to group."),
    ("Why might a scientist group pond animals by how they breathe?", "It helps explain how each is suited to living in water.", ["It is the only way.", "All pond animals breathe the same.", "Breathing is not a feature."], "Grouping for a purpose."),
    ("Where would you put a whale in a Carroll diagram for 'lives in water' and 'has fur or hair'?", "lives in water and has hair", ["lives in water and has no hair", "does not live in water and has hair", "it cannot go anywhere"], "Whales have a few hairs: they are mammals."),
    ("Why should you put minibeasts back where you found them after a survey?", "so they can survive in their own habitat", ["so they can be found again for fun", "because they are dangerous", "it does not matter"], "Care for living things."),
])


def body():
    think = ("<p><b>Living things can be grouped in many ways, using features we can observe.</b></p>"
             "<ul><li>Animals: vertebrates or invertebrates; what they eat (herbivore, carnivore, omnivore); number of legs.</li>"
             "<li>Plants: flowering or non-flowering. Where they live: pond, woodland, seashore.</li>"
             "<li>Carroll diagrams sort by two yes/no questions at once.</li></ul>")
    ex = [("A badger eats worms and berries. Group?", ["Both animals and plants"], "omnivore"),
          ("A woodlouse has 14 legs. Insect?", ["Insects have 6 legs"], "No")]
    mist = ["Calling a spider an insect.", "Grouping by colour or size only.", "Thinking every animal in water is a fish."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why we group", B1 + [(C.g_vert, 6), (g_legs, 6)]),
        ("Animal groups", [(C.g_group, 8), (C.g_which, 6), (g_legs, 4), (C.g_plant, 2)]),
        ("What animals eat", [(g_diet, 16), (C.g_plant, 4)]),
        ("Habitats and diagrams", [(g_hab, 12), (g_carroll, 8)]),
        ("Grouping for a purpose", B5 + [(g_carroll, 6), (g_hab, 3), (C.g_plant, 4), (g_diet, 2)]),
    ])
    make_uk(4, "grouping-living-things", 1, "Living things and their habitats",
            "Recognise that living things can be grouped in a variety of ways.",
            "Grouping Living Things",
            "Year 4 Science: Grouping Living Things Worksheets (Vertebrates, Diets, Habitats)",
            "Grouping Living Things",
            "Free Year 4 science worksheets on grouping living things: vertebrates and invertebrates, herbivores, carnivores and omnivores, minibeast legs, habitats and Carroll diagrams. 100 questions with answers.",
            "Group living things by what they share.",
            "Backbone, diet, legs or habitat: each grouping uses features you can observe.",
            body(),
            [("How can living things be grouped?", "By features we can observe, such as whether an animal has a backbone, how many legs it has, what it eats, or whether a plant has flowers."),
             ("What is the difference between a herbivore, a carnivore and an omnivore?", "Herbivores eat only plants, carnivores eat only other animals, and omnivores eat both."),
             ("How does a Carroll diagram work?", "It has two yes/no questions, one across the top and one down the side, so each living thing goes in the box that matches both answers.")],
            sets)


if __name__ == "__main__":
    main()
