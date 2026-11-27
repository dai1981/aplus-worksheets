# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 1, AC9S1U01: habitats - the places plants and animals live (bushland, ocean, desert,
rainforest, wetland, under logs) and how these places meet their needs.
  python tools/gen_au_science_y1_habitats.py
Reuses the UK Year 2 habitats and microhabitats makers and the US Kindergarten where plants and animals live makers with Australian
names, plus own questions on Australian habitats. Short sentences.
Wrong answers come from real mistakes: thinking all animals can live anywhere, and putting sea animals on land.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import sci_kids as K

YEAR, SORT = 1, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

HB = "gen_uk_science_y2_habitats"
MH = "gen_uk_science_y2_microhabitats"
WL = "gen_us_science_gk_where_plants_and_animals_live"
NO = ["polar bear", "penguin", "arctic", "Arctic", "squirrel", "hedgehog", "badger", "fox", "robin", "oak", "possum"]
h_home = limit(src(HB, "g_home", drop=NO), 7)
h_suit = limit(src(HB, "g_suit", drop=NO), 6)
h_count = limit(src(HB, "g_count", drop=NO), 9)
h_b1 = src.B(HB, "B1", drop=NO)
m_where = src(MH, "g_where", drop=NO)
m_cond = src(MH, "g_cond", drop=NO)
m_hunt = limit(src(MH, "g_hunt", drop=NO), 8)
m_b5 = src.B(MH, "B5", drop=NO)
w_pick = limit(src(WL, "g_pick", drop=NO), 10)
w_why = src(WL, "g_why", drop=NO)
w_where = src(WL, "g_where", drop=NO)
w_b1 = src.B(WL, "B1", drop=NO)

POOL1 = pool(R, [
    ("What is a habitat?", "the place where an animal or plant lives", ["a kind of food", "a type of weather", "a toy"], "A habitat gives food, water and shelter."),
    ("Where does a clownfish live?", "on a coral reef in the ocean", ["in the desert", "in a tree", "under a log"], "The Great Barrier Reef is a habitat for many fish."),
    ("Where does a koala live?", "in gum trees in the bush", ["in the ocean", "in the snow", "in a pond"], "Koalas eat gum leaves."),
    ("Where does a thorny devil live?", "in the dry desert", ["in a rainforest pond", "in the sea", "in the snow"], "It is a small spiky lizard."),
    ("Where does a platypus live?", "in creeks and rivers", ["in the desert", "in the sky", "on a reef"], "It digs a burrow in the creek bank."),
    ("Where do slaters and worms like to live?", "under logs where it is dark and damp", ["on hot rocks", "in the sea", "in the sky"], "This small habitat is a microhabitat."),
    ("Why does a frog live near a pond?", "It needs water to keep its skin damp and to lay eggs.", ["It likes dry sand.", "It eats rocks.", "It cannot swim."], "Frogs need water."),
    ("Where does a cassowary live?", "in the rainforest", ["in the ocean", "in the desert", "in a snowy forest"], "Cassowaries eat rainforest fruit."),
    ("Which animal lives in the ocean?", "a dolphin", ["a kangaroo", "a wombat", "an emu"], "Dolphins swim in the sea."),
    ("Why can't a fish live in the desert?", "There is no water for it to swim and breathe in.", ["The desert is too cold.", "Fish like sand.", "Fish can live anywhere."], "A habitat must meet an animal's needs."),
])
POOL5 = pool(R, [
    ("Mia lifts a log and finds worms, slaters and beetles. Why do they live there?", "It is dark, damp and has rotting wood to eat.", ["It is sunny and dry.", "It is in the ocean.", "They are lost."], "Always put the log back gently."),
    ("Jack counts birds in the school garden. Where does he see the most?", "near the bird bath and the trees", ["on the empty concrete", "in the car park", "on the roof only"], "Birds need water and shelter."),
    ("Ruby makes a habitat box for a snail. What should she put in it?", "damp soil, leaves and a cover", ["dry sand only", "a cup of salt", "nothing"], "Snails need damp places."),
    ("Kai wants to see which habitat in the school yard has the most minibeasts. What should he do?", "look in the same-sized area in each place for the same time", ["look in only one place", "guess", "count the trees"], "This is a fair test."),
    ("Ella sees a magpie building a nest in a gum tree. What does the tree give the magpie?", "shelter and a safe place for eggs", ["water to swim", "a burrow", "snow"], "Trees are part of a habitat."),
    ("Noah finds a lizard on a warm rock. Which habitat clue is this?", "it needs sunshine to warm up", ["it needs snow", "it needs the sea", "it needs a cave"], "Lizards warm themselves in the sun."),
])


def main():
    sets = U.sets([
        ("What is a habitat?", [(POOL1, 6), (h_home, 6), (w_b1, 4), (h_b1, 4)]),
        ("Animals and their homes", [(h_home, 1), (w_pick, 5), (w_where, 5), (POOL1, 3), (h_suit, 4), (w_why, 2)]),
        ("Small habitats", [(m_where, 6), (m_cond, 5), (m_hunt, 4), (POOL1, 1), (POOL5, 4)]),
        ("How habitats meet needs", [(h_suit, 2), (w_why, 5), (h_count, 4), (POOL1, 4), (m_cond, 2), (h_b1, 3)]),
        ("Let's explore", [(POOL5, 2), (m_b5, 4), (m_hunt, 1), (h_count, 4), (w_pick, 3), (w_where, 3), (m_where, 3)]),
    ])
    pic = K.row(["tree", "fish", "cactus", "frog"], words=["bush", "ocean", "desert", "pond"], size=80, label="a tree, a fish, a cactus and a frog")
    make_au(YEAR, "habitats", SORT, "AC9S1U01", "Biological sciences",
            "Identify the basic needs of plants and animals, including air, water, food or shelter, and describe how the places they live "
            "meet those needs (summary of the Australian Curriculum v9.0 Science content description).",
            "Habitats", "Habitats",
            "Free Year 1 science worksheets on habitats: where plants and animals live in Australia, small habitats under logs, and "
            "how habitats give food, water and shelter. 100 questions with answers.",
            "A habitat is a home.", "A habitat gives plants and animals the food, water and shelter they need.",
            ("Every living thing has a habitat.", ["Koalas live in gum trees.", "Fish live in water.", "Worms live in damp soil."]),
            [("Where does a platypus live?", ["it swims and digs"], "in creeks and rivers")],
            ["Thinking any animal can live anywhere.", "Putting sea animals in a land habitat."],
            [("What is a habitat?", "A habitat is the place where a plant or animal lives. It gives the living thing what it needs."),
             ("What is a microhabitat?", "A microhabitat is a very small habitat, such as under a log or a rock, where minibeasts live."),
             ("What habitats are in Australia?", "Australia has bushland, rainforests, deserts, wetlands, rivers, beaches and coral reefs.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
