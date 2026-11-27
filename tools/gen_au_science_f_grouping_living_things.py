# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Foundation, AC9SFU01: grouping plants and animals by their features - living or not living,
animal groups (birds, fish, mammals, insects), what animals eat, and kinds of plants and trees.
  python tools/gen_au_science_f_grouping_living_things.py
Reuses the UK Year 1 animal groups, carnivores and herbivores and trees makers and the UK Year 2 living, dead and never alive
makers with Australian names, plus own questions on Australian animals. Very short sentences.
Wrong answers come from real mistakes: calling a whale a fish, calling a bat a bird, and thinking a seed is not living.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import sci_kids as K

YEAR, SORT = 0, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

AG = "gen_uk_science_y1_animal_groups"
CH = "gen_uk_science_y1_carnivores_herbivores_and_omnivores"
TR = "gen_uk_science_y1_deciduous_and_evergreen_trees"
LD = "gen_uk_science_y2_living_dead_and_never_alive"
NO = ["possum", "squirrel", "deciduous", "evergreen", "autumn"]
g_group = limit(src(AG, "g_group", drop=NO), 6)
g_pick = limit(src(AG, "g_pick", drop=NO), 10)
g_feat = src(AG, "g_feat", drop=NO)
g_trick = src(AG, "g_trick", drop=NO)
g_pic = src(AG, "g_pic", drop=NO)
g_b1 = src.B(AG, "B1", drop=NO)
c_food = limit(src(CH, "g_food", drop=NO + ["wombat", "echidna"]), 10)
c_kind = limit(src(CH, "g_kind", drop=NO + ["wombat", "echidna"]), 9)
c_b1 = src.B(CH, "B1", drop=NO + ["wombat", "echidna"])
l_pick = limit(src(LD, "g_pick", drop=NO), 10)
l_sort = limit(src(LD, "g_sort", drop=NO), 8)
l_pic = src(LD, "g_picture", drop=NO)
l_trick = src(LD, "g_trick", drop=NO)
l_b5 = src.B(LD, "B5", drop=NO)

POOL1 = pool(R, [
    ("Is a koala living or not living?", "living", ["not living", "a toy", "a rock"], "Living things grow, eat and breathe."),
    ("Is a rock living or not living?", "not living", ["living", "a plant", "an animal"], "Rocks do not grow or eat."),
    ("Which one is a mammal with fur?", "a wombat", ["a magpie", "a goanna", "a barramundi"], "Mammals have fur or hair."),
    ("Which one is a bird?", "an emu", ["a kangaroo", "a crocodile", "a turtle"], "Emus have feathers but cannot fly."),
    ("Which one is a fish?", "a barramundi", ["a dolphin", "a frog", "a platypus"], "Fish have fins and scales."),
    ("Which one is an insect?", "a bee", ["a spider", "a worm", "a snail"], "Insects have 6 legs."),
    ("Which group are a kangaroo, a koala and a wombat in?", "animals with pouches", ["birds", "fish", "insects"], "They are marsupials."),
    ("What does a koala eat?", "gum leaves", ["meat", "fish", "insects"], "Koalas eat eucalyptus leaves."),
    ("Which animal eats other animals?", "a crocodile", ["a koala", "a wombat", "a kangaroo"], "Crocodiles are meat eaters."),
    ("Which two animals belong in the same group?", "a magpie and a kookaburra", ["a magpie and a snake", "a kookaburra and a fish", "a frog and a bird"], "Both are birds."),
    ("Sort these: a gum tree, grass and a wattle. What are they all?", "plants", ["animals", "rocks", "insects"], "They all grow from seeds and have leaves."),
    ("Which one is not an animal?", "a gum tree", ["a lizard", "a frog", "a moth"], "A tree is a plant."),
])
POOL5 = pool(R, [
    ("Mia sorts pictures into 'has fur' and 'has feathers'. Where does a cockatoo go?", "has feathers", ["has fur", "both", "neither"], "Cockatoos are birds."),
    ("Jack sorts animals into 'swims' and 'flies'. Where does a pelican go?", "both", ["swims only", "flies only", "neither"], "Pelicans fly and float on water."),
    ("Ruby sorts animals by number of legs. Which group has 6 legs?", "a beetle and an ant", ["a dog and a cat", "a spider and a scorpion", "a bird and a person"], "Insects have 6 legs."),
    ("Kai makes two groups: 'living' and 'not living'. Where does a seed go?", "living", ["not living", "neither", "both"], "A seed can grow into a plant."),
    ("Ella makes a group of animals that lay eggs. Which one belongs?", "a platypus", ["a kangaroo", "a dog", "a koala"], "The platypus is a mammal that lays eggs."),
    ("Noah sorts leaves by shape. What is he using to group them?", "a feature he can see", ["their names", "their smell only", "how old they are"], "Grouping by features is what scientists do."),
])


def main():
    sets = U.sets([
        ("Living or not living?", [(l_pick, 6), (l_sort, 4), (l_pic, 3), (POOL1, 4), (l_trick, 3)]),
        ("Animal groups", [(g_group, 6), (g_pick, 5), (POOL1, 4), (g_feat, 3), (g_b1, 2)]),
        ("Tricky animals", [(g_trick, 5), (g_pic, 5), (g_feat, 3), (POOL1, 4), (g_b1, 3)]),
        ("What animals eat", [(c_food, 5), (c_kind, 5), (c_b1, 4), (POOL1, 3), (l_trick, 3)]),
        ("Sorting and grouping", [(POOL5, 6), (l_b5, 4), (g_pick, 3), (l_sort, 2), (c_kind, 2), (c_food, 3)]),
    ])
    pic = K.row(["dog", "bird", "fish", "bug"], words=["fur", "feathers", "fins", "6 legs"], size=80, label="a dog, a bird, a fish and a bug")
    make_au(YEAR, "grouping-living-things", SORT, "AC9SFU01", "Biological sciences",
            "Observe external features of plants and animals and describe ways they can be grouped based on these features "
            "(Australian Curriculum v9.0 Science content description).",
            "Grouping Living Things", "Grouping living things",
            "Free Foundation science worksheets on grouping living things: living or not living, birds, fish, mammals and insects, "
            "what animals eat, and sorting by features. 100 questions with answers.",
            "Sort living things by what you see.", "Animals with the same features go in the same group, such as fur, feathers or fins.",
            ("We can sort living things into groups.", ["Living things grow, eat and breathe.", "Birds have feathers; fish have fins.",
                                                         "Mammals have fur; insects have 6 legs."]),
            [("A kookaburra: which group?", ["it has feathers"], "birds")],
            ["Calling a whale a fish (it is a mammal).", "Calling a bat a bird (it is a mammal with fur)."],
            [("How do scientists group animals?", "They look at features such as fur, feathers, scales, fins and the number of legs."),
             ("Is a seed living?", "Yes. A seed is alive. It can grow into a new plant when it gets water and warmth."),
             ("What is special about Australian mammals?", "Many have pouches, like kangaroos and koalas. The platypus and echidna lay eggs.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
