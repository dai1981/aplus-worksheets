# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, AC9S3U01: life cycles of plants and animals, including Australian animals with
unusual life cycles (the platypus and echidna lay eggs; kangaroo joeys grow in a pouch; emu fathers sit on the eggs).
  python tools/gen_au_science_y3_life_cycles.py
Own Australian life cycles plus the SG Primary 3 animal and plant life-cycle makers and the US Grade 3 life-cycle makers.
Wrong answers come from real mistakes: thinking all mammals give birth to live young, mixing up larva and pupa, and thinking
a young animal always looks like its parent.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

SA = "gen_sg_science_p3_life_cycles_of_animals"
SP = "gen_sg_science_p3_life_cycles_of_plants"
US = "gen_us_science_g3_life_cycles"
sa_order = src(SA, "g_order")
sa_table = limit(src(SA, "g_table"), 3)
sa_where = src(SA, "g_where")
sa_b1 = src.B(SA, "B1")
sa_b2 = src.B(SA, "B2")
sa_b3 = src.B(SA, "B3")
sa_b5 = src.B(SA, "B5", drop=["in March"])
sp_parts = src(SP, "g_parts")
sp_stage = src(SP, "g_stage")
sp_time = src(SP, "g_time", drop=["durian", "coconut"])
sp_b1 = src.B(SP, "B1")
sp_b2 = src.B(SP, "B2")
sp_b5 = src.B(SP, "B5")
NA = ["salmon", "alevin", "fry", "parr", "smolt"]
us_first = limit(src(US, "g_first", drop=NA), 4)
us_missing = limit(src(US, "g_missing", drop=NA), 4)
us_next = limit(src(US, "g_next", drop=NA), 5)
us_compare = src(US, "g_compare")
us_b1 = src.B(US, "B1")
us_b5 = src.B(US, "B5")

LC = {"platypus": ["egg", "puggle (baby platypus)", "young platypus", "adult platypus"],
      "red kangaroo": ["tiny newborn joey", "joey in the pouch", "young kangaroo out of the pouch", "adult kangaroo"],
      "green sea turtle": ["egg buried in sand", "hatchling", "young turtle", "adult turtle"],
      "emu": ["egg", "striped chick", "young emu", "adult emu"],
      "green tree frog": ["egg", "tadpole", "froglet", "adult frog"],
      "Ulysses butterfly": ["egg", "caterpillar (larva)", "pupa", "adult butterfly"],
      "Christmas beetle": ["egg", "grub (larva)", "pupa", "adult beetle"],
      "gum tree": ["seed", "seedling", "young tree", "adult tree with flowers"]}


def g_lc():
    o = R.choice(sorted(LC))
    st = LC[o]
    k = R.choice(["first", "after", "last", "missing"])
    if k == "first":
        return tq("What is the first stage in the life cycle of %s %s?" % (("an" if o[0] in "aeiouAE" else "a"), o), st[0], st[1:], "The cycle starts with %s." % st[0])
    if k == "last":
        return tq("In the life cycle of %s %s, which stage can reproduce?" % (("an" if o[0] in "aeiouAE" else "a"), o), st[3], st[:3], "Only the adult can reproduce.")
    if k == "after":
        i = R.randrange(3)
        return tq("In the life cycle of %s %s, what comes after the %s?" % (("an" if o[0] in "aeiouAE" else "a"), o, st[i].split(" (")[0]), st[i + 1],
                  [x for j, x in enumerate(st) if j != i + 1], " → ".join(st) + ".")
    i = R.randrange(1, 3)
    shown = " → ".join(x if j != i else "?" for j, x in enumerate(st))
    return tq("Which stage is missing from this life cycle of %s %s? %s" % (("an" if o[0] in "aeiouAE" else "a"), o, shown), st[i],
              [x for j, x in enumerate(st) if j != i] , "The full cycle: " + " → ".join(st) + ".")


POOL1 = pool(R, [
    ("Which Australian mammals lay eggs?", "the platypus and the echidna", ["the koala and the wombat", "the kangaroo and the dingo", "all mammals"], "They are called monotremes."),
    ("Where does a newborn kangaroo joey grow?", "in its mother's pouch", ["in an egg", "in a nest of grass", "in the water"], "Kangaroos are marsupials."),
    ("How big is a red kangaroo joey when it is born?", "about the size of a jellybean", ["as big as a dog", "as big as its mother", "about 1 m tall"], "It crawls to the pouch and keeps growing."),
    ("Which parent sits on emu eggs until they hatch?", "the father", ["the mother", "both take turns equally", "no one"], "Emu fathers also care for the chicks."),
    ("Where do green sea turtles lay their eggs?", "in holes they dig in sandy beaches", ["in trees", "on the sea floor", "in rivers"], "The hatchlings crawl to the sea."),
    ("Which stage of a frog's life cycle lives only in water and breathes with gills?", "the tadpole", ["the adult frog", "the froglet on land", "none"], "Tadpoles change into frogs."),
    ("What happens inside a pupa?", "The larva changes into an adult insect.", ["The insect eats a lot.", "It lays eggs.", "Nothing happens."], "This change is called metamorphosis."),
    ("Which young animal does NOT look like its parent?", "a caterpillar", ["a kitten", "a joey", "a puppy"], "Caterpillars change a lot as they grow."),
    ("What is a life cycle?", "the stages a living thing goes through from birth to having young of its own", ["a bike ride", "how long a day is", "the seasons"], "Life cycles repeat."),
    ("Why is a life cycle drawn as a circle?", "The adults make new young, so the cycle starts again.", ["Because circles are easy to draw.", "Because animals walk in circles.", "Because it only happens once."], "It keeps repeating."),
])
POOL5 = pool(R, [
    ("Mia measures a bean plant every 2 days: 0, 2, 5, 9, 14 cm. What pattern does she see?", "It grows more each time.", ["It shrinks.", "It grows the same amount each time.", "It stops growing."], "The gaps get bigger: 2, 3, 4, 5 cm."),
    ("Jack keeps silkworms. He sees eggs, then caterpillars, then cocoons. What should he expect next?", "adult moths", ["more eggs straight away", "tadpoles", "seeds"], "Silkworms become moths."),
    ("Ruby compares life cycle lengths: a mosquito about 2 weeks, a frog about 3 months to adult, a kangaroo about 2 years. Which takes longest to become an adult?", "the kangaroo", ["the mosquito", "the frog", "they are all the same"], "Bigger animals often take longer."),
    ("Kai says all baby animals hatch from eggs. Which animal shows he is wrong?", "a kangaroo", ["a platypus", "a turtle", "an emu"], "Kangaroos give birth to live young."),
])


def main():
    sets = U.sets([
        ("What is a life cycle?", [(POOL1, 5), (us_compare, 5), (us_b1, 4), (g_lc, 6)]),
        ("Australian animals", [(g_lc, 12), (POOL1, 5), (us_next, 3)]),
        ("Insects and frogs", [(sa_order, 4), (sa_where, 4), (sa_b1, 5), (sa_b2, 4), (us_missing, 3)]),
        ("Plant life cycles", [(sp_stage, 6), (sp_parts, 5), (sp_time, 3), (sp_b1, 4), (sp_b2, 2)]),
        ("Investigations", [(POOL5, 4), (sa_b5, 4), (sp_b5, 4), (us_b5, 3), (sa_table, 3), (sa_b3, 2)]),
    ])
    make_au(YEAR, "life-cycles", SORT, "AC9S3U01", "Biological sciences",
            "Compare characteristics of living and non-living things and examine the differences between the life cycles of plants and "
            "animals (summary of the Australian Curriculum v9.0 Science content description).",
            "Life Cycles", "Life cycles",
            "Free Year 3 science worksheets on life cycles of plants and animals: frogs, butterflies, beetles, gum trees and Australian "
            "animals such as the platypus, kangaroo, emu and sea turtle. 100 questions with answers.",
            "Living things are born, grow, reproduce and die.", "Every plant and animal has a life cycle that starts again when it has young.",
            "<p><b>A life cycle is the set of stages a living thing goes through as it grows and has young.</b></p><ul>"
            "<li>Many animals hatch from eggs; the platypus and echidna are mammals that lay eggs.</li>"
            "<li>Kangaroos are born tiny and grow in their mother's pouch. Insects such as butterflies change shape: egg, larva, pupa, adult.</li>"
            "<li>Plants grow from seeds into seedlings and adult plants that make flowers and new seeds.</li></ul>",
            [("Frog: egg → tadpole → ? → adult frog", ["the tadpole grows legs and loses its tail"], "froglet"),
             ("Does a platypus lay eggs?", ["it is a monotreme"], "yes")],
            ["Thinking all mammals give birth to live young (the platypus and echidna lay eggs).", "Mixing up the larva (caterpillar) and the pupa.",
             "Thinking young animals always look like their parents."],
            [("What is a life cycle?", "A life cycle is the series of stages a living thing goes through: for example egg, tadpole, froglet and adult frog."),
             ("How is a kangaroo's life cycle different?", "A kangaroo is born very small, about the size of a jellybean. It crawls into its mother's pouch, drinks milk and grows there for months."),
             ("What is metamorphosis?", "It is a big change in body shape during a life cycle, such as a caterpillar changing into a butterfly or a tadpole into a frog.")],
            sets)


if __name__ == "__main__":
    main()
