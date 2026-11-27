# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, AC9S3U01: living things share features that non-living things do not (they need
food, water and air, grow, respond, reproduce, get rid of waste and die); sorting into living, dead (once alive) and never alive.
  python tools/gen_au_science_y3_living_and_non_living_things.py
Reuses the SG Primary 3 and UK Year 2 living-things makers with Australian names, plus own Australian examples.
Wrong answers come from real mistakes: thinking anything that moves is alive (cars, wind, fire), thinking plants are not alive
because they do not walk, and putting wood or wool in "never alive".
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

SG = "gen_sg_science_p3_living_and_non_living_things"
UK = "gen_uk_science_y2_living_dead_and_never_alive"
sg_odd = limit(src(SG, "g_odd", drop=["pandan"]), 8)
sg_show = src(SG, "g_show", drop=["A pupil", "pandan"])
sg_not = src(SG, "g_notchar")
sg_b1 = src.B(SG, "B1")
sg_b2 = src.B(SG, "B2", drop=["pandan"])
sg_b3 = src.B(SG, "B3", drop=["pandan"])
sg_b5 = src.B(SG, "B5", drop=["pandan"])
uk_pick = limit(src(UK, "g_pick"), 5)
uk_sort = limit(src(UK, "g_sort"), 8)
uk_trick = src(UK, "g_trick")
uk_proc = src(UK, "g_proc")
uk_b1 = src.B(UK, "B1")

AUS = [("a koala", "living"), ("a gum tree", "living"), ("a wattle", "living"), ("a magpie", "living"), ("a goanna", "living"), ("a mushroom", "living"),
       ("a dry gum leaf on the ground", "dead (once alive)"), ("a seashell on the beach", "dead (once alive)"), ("a kangaroo skull", "dead (once alive)"),
       ("a wooden boomerang", "dead (once alive)"), ("a cotton T-shirt", "dead (once alive)"), ("a fallen log", "dead (once alive)"),
       ("a rock at Uluru", "never alive"), ("a plastic bucket", "never alive"), ("a steel fence", "never alive"), ("sea water", "never alive"),
       ("a glass bottle", "never alive"), ("a campfire flame", "never alive")]


def g_aus():
    o, k = R.choice(AUS)
    return tq("Is %s living, dead (once alive) or never alive?" % o, k, [x for x in ["living", "dead (once alive)", "never alive", "a living thing that is asleep"] if x != k],
              {"living": "It grows, needs food, water and air, and reproduces.", "dead (once alive)": "It came from something that was alive.",
               "never alive": "It was never part of a living thing."}[k])


POOL1 = pool(R, [
    ("Which of these do ALL living things need?", "food (or energy), water and air", ["sunshine and toys", "only water", "shoes"], "Plants make food; animals eat food."),
    ("A car moves and uses fuel. Why is it not alive?", "It cannot grow or reproduce.", ["It is too big.", "It is made of metal, so it is alive.", "It moves, so it is alive."], "Moving is not enough to be alive."),
    ("Is a gum tree alive even though it cannot walk?", "Yes. It grows, takes in water and makes seeds.", ["No, because it cannot walk.", "No, because it is brown.", "Only in summer."], "Plants are living things."),
    ("A seed is in a packet. Is it alive?", "Yes, it is alive but resting until it gets water and warmth.", ["No, seeds are never alive.", "It is a rock.", "Only if it is green."], "Seeds can grow into new plants."),
    ("Which shows that a plant responds to changes?", "Its leaves turn towards the light.", ["It is green.", "It has a stem.", "It is in a pot."], "Living things respond."),
    ("Which of these can reproduce?", "a kangaroo", ["a rock", "a car", "a cloud"], "Living things make more of their own kind."),
    ("Why is a wooden table 'dead' and not 'never alive'?", "The wood came from a tree that was once alive.", ["Tables are alive.", "Wood was never alive.", "It is painted."], "Wood, paper and cotton came from living things."),
    ("Which of these gets rid of waste?", "a dog", ["a pencil", "a chair", "a stone"], "Living things get rid of waste."),
])
POOL5 = pool(R, [
    ("Mia puts bean seeds on wet cotton wool and on dry cotton wool. Only the wet seeds sprout. What does this show?", "Seeds need water to start growing.", ["Seeds need dry places.", "Cotton wool is alive.", "Seeds are never alive."], "Living things need water."),
    ("Jack sees something moving in a pond. How could he decide if it is alive?", "Watch whether it feeds, grows, breathes and responds.", ["Check if it is shiny.", "See if it floats.", "Check its colour."], "Use the features of living things."),
    ("Ruby sorts items into 'living', 'dead' and 'never alive'. Where should she put a feather?", "dead (once alive)", ["living", "never alive", "it cannot be sorted"], "Feathers come from birds."),
    ("Kai watches a snail for 10 minutes. It moves away when he touches it. Which feature of living things does this show?", "responding to changes", ["growing", "reproducing", "making food"], "Living things respond to their surroundings."),
])


def main():
    sets = U.sets([
        ("Living or non-living?", [(sg_odd, 6), (POOL1, 4), (sg_not, 4), (g_aus, 6)]),
        ("What living things do", [(sg_show, 8), (uk_proc, 5), (sg_b1, 4), (POOL1, 3)]),
        ("Living, dead or never alive", [(g_aus, 8), (uk_sort, 6), (uk_trick, 4), (uk_b1, 2)]),
        ("Needs of living things", [(sg_b2, 6), (sg_b3, 6), (uk_pick, 4), (uk_b1, 2), (POOL1, 1), (sg_odd, 1)]),
        ("Investigations", [(sg_b5, 8), (POOL5, 4), (g_aus, 3), (uk_trick, 2), (uk_sort, 2), (sg_show, 1)]),
    ])
    make_au(YEAR, "living-and-non-living-things", SORT, "AC9S3U01", "Biological sciences",
            "Compare characteristics of living and non-living things and examine the differences between the life cycles of plants and "
            "animals (summary of the Australian Curriculum v9.0 Science content description).",
            "Living and Non-living Things", "Living and non-living things",
            "Free Year 3 science worksheets on living and non-living things: what all living things do, and sorting things into living, "
            "dead (once alive) and never alive. 100 questions with answers.",
            "Living things grow, feed and reproduce.", "Moving is not enough: a living thing grows, needs food, water and air, responds and reproduces.",
            "<p><b>Living things share features that non-living things do not have.</b></p><ul>"
            "<li>Living things need food (or make it), water and air; they grow, respond to changes, get rid of waste, reproduce and die.</li>"
            "<li>Dead things were once alive: a dry leaf, a shell, wood, cotton.</li>"
            "<li>Never-alive things were never part of a living thing: rock, plastic, metal, glass, water.</li></ul>",
            [("A car moves. Is it alive?", ["it cannot grow or reproduce"], "no"),
             ("A wooden spoon: living, dead or never alive?", ["wood comes from a tree"], "dead (once alive)")],
            ["Thinking anything that moves is alive (cars, wind, fire).", "Thinking plants are not alive because they do not walk.",
             "Putting wood, paper or wool in 'never alive'."],
            [("What makes something a living thing?", "Living things need food, water and air. They grow, respond to changes, get rid of waste and reproduce."),
             ("Is fire alive?", "No. Fire can grow and move, but it does not reproduce, respond or grow like a living thing."),
             ("What does 'dead' mean in science?", "Dead means something was once alive but is not alive now, such as a dry leaf, a shell or a piece of wood.")],
            sets)


if __name__ == "__main__":
    main()
