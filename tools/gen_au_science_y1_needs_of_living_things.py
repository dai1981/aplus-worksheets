# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 1, AC9S1U01: the basic needs of plants and animals - air, water, food, light and shelter -
and caring for living things.
  python tools/gen_au_science_y1_needs_of_living_things.py
Reuses the US Kindergarten needs makers and the UK Year 2 animal and plant needs makers with Australian names, plus own questions
on Australian animals and pets. Short sentences.
Wrong answers come from real mistakes: thinking plants eat soil, thinking animals do not need air, and forgetting that pets need shelter.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import sci_kids as K

YEAR, SORT = 1, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

KN = "gen_us_science_gk_what_plants_and_animals_need"
AN = "gen_uk_science_y2_what_animals_need_to_survive"
PN = "gen_uk_science_y2_what_plants_need_to_stay_healthy"
k_need = limit(src(KN, "g_need", drop=["possum"]), 6)
k_eat = src(KN, "g_eat", drop=["possum"])
k_living = limit(src(KN, "g_living", drop=["possum"]), 5)
k_kind = src(KN, "g_kind", drop=["possum"])
k_obs = src(KN, "g_obs", drop=["possum"])
k_b1 = src.B(KN, "B1", drop=["possum"])
k_b5 = src.B(KN, "B5", drop=["possum"])
a_need = src(AN, "g_need")
a_pet = src(AN, "g_pet")
a_air = src(AN, "g_air")
a_table = limit(src(AN, "g_table"), 5)
a_wild = src(AN, "g_wild")
a_b1 = src.B(AN, "B1")
p_need = src(PN, "g_need")
p_place = src(PN, "g_place")
p_b1 = src.B(PN, "B1")
p_b5 = src.B(PN, "B5")

POOL1 = pool(R, [
    ("What do all animals need to stay alive?", "air, water, food and shelter", ["toys and games", "only sunlight", "only water"], "These are basic needs."),
    ("What do plants need to grow?", "light, water, air and space", ["meat and milk", "toys", "only soil"], "Plants make their own food using light."),
    ("Where does a koala get water?", "mostly from the gum leaves it eats", ["from a tap", "from milk", "it never needs water"], "Koalas also drink from creeks when it is hot."),
    ("What does a joey need from its mother?", "milk and the warm, safe pouch", ["grass only", "a nest of sticks", "nothing"], "The pouch gives shelter."),
    ("Why does a fish need water?", "It takes in air from the water with its gills.", ["It does not need water.", "To keep its fur dry.", "To eat sand."], "Fish cannot breathe out of water."),
    ("What does a pet dog need every day?", "food, fresh water and a safe place to sleep", ["only toys", "sunscreen", "a car ride"], "Pets depend on us."),
    ("Why do birds build nests?", "for shelter and to keep their eggs safe", ["to store toys", "to dig for water", "to make light"], "A nest is a kind of shelter."),
    ("What happens to a plant with no water?", "it wilts and can die", ["it grows faster", "it turns blue", "nothing"], "Plants need water."),
    ("What happens to a plant kept in a dark cupboard?", "it turns pale and weak", ["it grows big and green", "it makes flowers", "nothing"], "Plants need light."),
    ("Why do we need to breathe?", "Our bodies need air (oxygen) to live.", ["To make noise only.", "We do not need air.", "To grow hair."], "All animals need air."),
])
POOL5 = pool(R, [
    ("Mia puts one bean plant in the sun and one in a dark cupboard. Which grows better?", "the one in the sun", ["the one in the dark", "both the same", "neither"], "Plants need light."),
    ("Jack waters one plant and does not water another. What will he see?", "the plant with no water wilts", ["both grow the same", "the dry plant grows faster", "nothing changes"], "Plants need water."),
    ("Ruby wants to look after a pet guinea pig. What should she give it?", "food, water and a clean hutch", ["only a ball", "salt water", "nothing"], "Pets need food, water and shelter."),
    ("Kai sees a bird bath in a garden on a hot day. Why does it help birds?", "Birds can drink and cool down.", ["Birds eat the water.", "It gives birds toys.", "It has no use."], "Animals need water."),
    ("Ella plants seeds in two pots. Why must she give them the same water?", "so it is a fair test", ["so they look nice", "so they grow different colours", "it does not matter"], "Change only one thing."),
    ("Noah sees a lizard lying on a warm rock in the morning. Why?", "It needs to warm its body in the sun.", ["It is sleeping forever.", "It is eating the rock.", "It needs shade."], "Lizards warm up in the sun."),
])


def main():
    sets = U.sets([
        ("What living things need", [(POOL1, 6), (k_need, 6), (k_living, 4), (k_b1, 4)]),
        ("What animals need", [(a_need, 5), (a_air, 4), (a_wild, 4), (k_eat, 3), (POOL1, 2), (a_b1, 2)]),
        ("What plants need", [(p_need, 7), (p_place, 5), (p_b1, 4), (POOL1, 2), (k_kind, 2)]),
        ("Looking after pets", [(a_pet, 6), (a_table, 5), (k_obs, 4), (k_kind, 3), (POOL5, 2)]),
        ("Let's test it", [(POOL5, 4), (k_b5, 4), (p_b5, 4), (a_table, 3), (k_eat, 3), (k_obs, 2)]),
    ])
    pic = K.row(["sun", "drop", "apple", "house"], words=["light", "water", "food", "shelter"], size=80, label="the sun, a water drop, an apple and a house")
    make_au(YEAR, "needs-of-living-things", SORT, "AC9S1U01", "Biological sciences",
            "Identify the basic needs of plants and animals, including air, water, food or shelter, and describe how the places they live "
            "meet those needs (summary of the Australian Curriculum v9.0 Science content description).",
            "Needs of Living Things", "Needs of living things",
            "Free Year 1 science worksheets on the needs of living things: air, water, food, light and shelter for plants and animals, "
            "and looking after pets. 100 questions with answers.",
            "Living things need air, water and food.", "Animals also need shelter. Plants need light and water to make their own food.",
            ("All living things have needs.", ["Animals need air, water, food and shelter.", "Plants need light, water, air and space.",
                                               "Pets need us to give them these things."]),
            [("A plant is in a dark cupboard. What is missing?", ["plants need light"], "light")],
            ["Thinking plants eat soil (they make food using light).", "Forgetting that animals need air and shelter."],
            [("What are basic needs?", "Basic needs are things a living thing must have to stay alive: air, water, food and shelter for animals, and light, water and air for plants."),
             ("Do plants eat food?", "Plants make their own food in their leaves using sunlight, water and air."),
             ("How can children care for living things?", "Water plants, put out fresh water for birds on hot days and give pets food, water and a clean place to sleep.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
