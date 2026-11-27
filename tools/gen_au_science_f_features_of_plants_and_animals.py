# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Foundation, AC9SFU01: observing the external features of plants and animals - body parts,
coverings (fur, feathers, scales), legs, wings and fins, and the parts of a plant.
  python tools/gen_au_science_f_features_of_plants_and_animals.py
Reuses the UK Year 1 animal bodies and parts of a plant makers and the US Grade 1 plant and animal parts makers with Australian
names, plus own picture-free questions on Australian animals. Very short sentences for 5-6 year olds.
Wrong answers come from real mistakes: mixing up fur and feathers, thinking all animals have legs, and calling roots leaves.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import sci_kids as K

YEAR, SORT = 0, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

AB = "gen_uk_science_y1_animal_bodies"
PP = "gen_uk_science_y1_parts_of_a_plant"
PA = "gen_us_science_g1_plant_and_animal_parts"
a_has = limit(src(AB, "g_has"), 8)
a_legs = src(AB, "g_legs")
a_job = limit(src(AB, "g_job"), 6)
a_pic = src(AB, "g_pic", drop=["possum"])
a_both = src(AB, "g_both")
a_b1 = src.B(AB, "B1")
a_b5 = src.B(AB, "B5")
p_pic = limit(src(PP, "g_pic"), 10)
p_desc = src(PP, "g_desc")
p_grow = limit(src(PP, "g_grow"), 4)
p_b1 = src.B(PP, "B1")
u_part = limit(src(PA, "g_part", drop=["possum"]), 12)
u_pick = limit(src(PA, "g_pick", drop=["possum"]), 9)

POOL1 = pool(R, [
    ("What covers a koala's body?", "fur", ["feathers", "scales", "a shell"], "Koalas are mammals with soft grey fur."),
    ("What covers a kookaburra's body?", "feathers", ["fur", "scales", "a shell"], "All birds have feathers."),
    ("What covers a goanna's body?", "scales", ["feathers", "fur", "a shell"], "Lizards have dry, scaly skin."),
    ("What covers an echidna's back?", "sharp spines", ["feathers", "scales", "leaves"], "Spines keep the echidna safe."),
    ("How many legs does a kangaroo have?", "2 big back legs and 2 small front legs", ["6 legs", "no legs", "8 legs"], "Kangaroos hop on their big back legs."),
    ("What does a fish use to swim?", "fins and a tail", ["wings", "legs", "fur"], "Fins help fish move and steer."),
    ("Which animal has no legs?", "a snake", ["a dog", "a bird", "a frog"], "Snakes slide on their bellies."),
    ("Which part of a plant is under the soil?", "the roots", ["the flower", "the leaves", "the fruit"], "Roots take in water."),
    ("Which part of a plant is often green and flat?", "a leaf", ["a root", "a seed", "a petal"], "Leaves catch sunlight."),
    ("Which animal has a pouch?", "a kangaroo", ["a cat", "a duck", "a fish"], "A baby kangaroo is called a joey."),
    ("What does a platypus have?", "a bill like a duck and fur", ["feathers and wings", "scales and fins", "a shell"], "The platypus is a special Australian animal."),
    ("Which part of a plant is often bright and colourful?", "the flower", ["the root", "the stem", "the soil"], "Bright flowers attract bees."),
])
POOL5 = pool(R, [
    ("Mia looks at a bird with a magnifying glass. What can she see?", "feathers, a beak and two legs", ["fur and four legs", "scales and fins", "roots and leaves"], "Look closely and describe what you see."),
    ("Jack draws a gum tree. Which parts should he draw?", "roots, trunk, branches and leaves", ["fur, legs and a tail", "fins and scales", "feathers and a beak"], "A trunk is a thick, woody stem."),
    ("Ruby feels a leaf. It is smooth and flat. What is she doing?", "observing with her sense of touch", ["counting", "guessing", "sleeping"], "We use our senses to observe."),
    ("Kai counts the legs on a beetle. How many will he count?", "6", ["2", "4", "8"], "All insects have 6 legs."),
    ("Ella counts the legs on a spider. How many will she count?", "8", ["6", "4", "2"], "Spiders have 8 legs, so they are not insects."),
    ("Noah sees an animal with wings, feathers and a beak. What is it?", "a bird", ["a fish", "a lizard", "a frog"], "Feathers tell you it is a bird."),
])


def main():
    sets = U.sets([
        ("Animal body parts", [(a_has, 6), (a_job, 4), (POOL1, 4), (a_pic, 3), (a_b1, 3)]),
        ("Fur, feathers and scales", [(POOL1, 5), (a_both, 4), (a_has, 2), (u_part, 5), (a_legs, 4)]),
        ("Legs, wings and fins", [(a_legs, 5), (u_pick, 4), (a_job, 2), (POOL1, 3), (u_part, 1), (a_pic, 3), (POOL5, 2)]),
        ("Parts of a plant", [(p_pic, 7), (p_desc, 6), (p_grow, 3), (p_b1, 4)]),
        ("Looking closely", [(POOL5, 4), (a_b5, 4), (p_pic, 1), (p_grow, 1), (u_part, 4), (u_pick, 3), (p_desc, 3)]),
    ])
    pic = K.row(["bird", "fish", "frog", "flower"], words=["feathers", "fins", "legs", "petals"], size=80, label="a bird, a fish, a frog and a flower")
    make_au(YEAR, "features-of-plants-and-animals", SORT, "AC9SFU01", "Biological sciences",
            "Observe external features of plants and animals and describe ways they can be grouped based on these features "
            "(Australian Curriculum v9.0 Science content description).",
            "Features of Plants and Animals", "Plant and animal features",
            "Free Foundation science worksheets on the features of plants and animals: body parts, fur, feathers and scales, legs, "
            "wings and fins, and the parts of a plant. 100 questions with answers.",
            "Look closely at plants and animals.", "Animals have body parts like legs, wings and fur. Plants have roots, stems and leaves.",
            ("Living things have parts we can see.", ["Animals: legs, wings, fins, fur, feathers or scales.", "Plants: roots, stem, leaves and flowers.",
                                                      "Use your eyes and hands to observe."]),
            [("What covers a kookaburra?", ["it is a bird"], "feathers")],
            ["Mixing up fur and feathers.", "Thinking all animals have legs (snakes and fish do not)."],
            [("What are external features?", "They are the parts you can see on the outside, such as legs, wings, fur, leaves and flowers."),
             ("How can children observe features?", "Look closely with a magnifying glass, touch gently, count legs and draw what you see."),
             ("Why does Australia have special animals?", "Animals like the kangaroo, koala, platypus and echidna live naturally only in Australia.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
