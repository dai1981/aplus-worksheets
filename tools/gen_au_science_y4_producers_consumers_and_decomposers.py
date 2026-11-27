# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U01: the roles of producers, consumers and decomposers in a habitat.
  python tools/gen_au_science_y4_producers_consumers_and_decomposers.py
Australian living things sorted by role (gum trees, seagrass, koalas, dingoes, fungi, dung beetles, earthworms), plus the US
Grade 5 decomposer makers and the SG Primary 6 food-web makers on Australian webs (au_webs.py).
Wrong answers come from real mistakes: calling fungi plants (producers), thinking decomposers are pests that only spoil food,
and thinking animals make their own food.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import au_webs

YEAR, SORT = 4, 1
U, R, P, src = AU(seed_of(YEAR, SORT))
au_webs.add()
SG = "gen_sg_science_p6_food_chains_and_food_webs"
src.mod(SG).WEBS = au_webs.NAMES
sg_kind = limit(src(SG, "g_kind"), 5)
sg_prod = limit(src(SG, "g_prod"), 4)
DC = "gen_us_science_g5_decomposers_and_the_cycle_of_matter"
us_arrow = limit(src(DC, "g_arrow"), 4)
us_compost = limit(src(DC, "g_compost"), 3)
us_which = src(DC, "g_which_dec")
us_b1 = src.B(DC, "B1")
us_b5 = src.B(DC, "B5")

ROLE = [("gum tree", "producer"), ("saltbush", "producer"), ("seagrass", "producer"), ("algae", "producer"), ("wattle", "producer"),
        ("banksia", "producer"), ("spinifex", "producer"), ("phytoplankton", "producer"), ("koala", "consumer"), ("kangaroo", "consumer"),
        ("dingo", "consumer"), ("dugong", "consumer"), ("kookaburra", "consumer"), ("platypus", "consumer"), ("honey possum", "consumer"),
        ("emu", "consumer"), ("mushroom", "decomposer"), ("bracket fungus", "decomposer"), ("bacteria in the soil", "decomposer"),
        ("earthworm", "decomposer"), ("dung beetle", "decomposer"), ("mould on bread", "decomposer"), ("slater", "decomposer")]


def g_role():
    o, r = R.choice(ROLE)
    e = {"producer": "Producers make their own food from sunlight.", "consumer": "Consumers get energy by eating other living things.",
         "decomposer": "Decomposers break down dead plants, animals and waste."}[r]
    if o in ("algae", "phytoplankton", "bacteria in the soil"):
        q = "Are %s producers, consumers or decomposers?" % o
    elif o in ("seagrass", "spinifex", "saltbush", "mould on bread", "wattle", "banksia"):
        q = "Is %s a producer, a consumer or a decomposer?" % o
    else:
        q = "Is %s a producer, a consumer or a decomposer?" % (("an " if o[0] in "aeiou" else "a ") + o)
    return tq(q, "a " + r,
              ["a " + x for x in ["producer", "consumer", "decomposer"] if x != r] + ["a non-living thing"], e)


DEAD = [("A koala dies in the bush.", "bush"), ("A gum tree falls over in a storm.", "bush"), ("A kangaroo dies in a paddock.", "bush"),
        ("A possum dies under a tree.", "bush"), ("Leaves fall from a wattle onto the ground.", "bush"), ("A goanna dies in the outback.", "outback"),
        ("A saltbush dies in a drought.", "outback"), ("A kookaburra dies in a garden.", "bush")]


def g_ret():
    st, _ = R.choice(DEAD)
    return tq("%s What happens to the matter in it over time?" % st, "Decomposers break it down and return nutrients to the soil.",
              ["It stays the same forever.", "It turns into a rock.", "The Sun takes it away."], "Fungi, bacteria and small animals recycle dead matter.")


def g_pick():
    r = R.choice(["producer", "consumer", "decomposer"])
    a = R.choice([o for o, x in ROLE if x == r])
    w = R.sample([o for o, x in ROLE if x != r], 3)
    return tq("Which of these is a %s?" % r, a, w, "%s is a %s." % (a[0].upper() + a[1:], r))


POOL1 = pool(R, [
    ("What does a producer need to make its food?", "sunlight, water and carbon dioxide from the air", ["other animals", "dead leaves only", "darkness"], "Plants make food in their leaves."),
    ("Why are decomposers important?", "They break down dead things and return nutrients to the soil for plants.", ["They hunt large predators.", "They make food from sunlight.", "They stop plants from growing."], "Without them, dead matter would pile up."),
    ("Is a mushroom a plant?", "No. It is a fungus, a decomposer that cannot make its own food.", ["Yes, it is a producer.", "Yes, it eats sunlight.", "No, it is an animal that hunts."], "Fungi get food from dead matter."),
    ("Why were dung beetles brought to Australia?", "to break down cattle dung, which native beetles could not use", ["to eat crops", "to hunt mice", "to pollinate flowers"], "Dung beetles return nutrients to the soil and reduce flies."),
    ("What happens to a fallen gum tree in a forest over many years?", "Fungi, bacteria and insects break it down into soil.", ["It stays the same forever.", "It turns into a rock.", "It grows back by itself."], "Decomposers recycle the matter."),
    ("Which living things are consumers?", "animals, because they eat other living things", ["only plants", "only fungi", "rocks and water"], "Consumers cannot make their own food."),
    ("Where do producers get the energy to make food?", "from the Sun", ["from the soil", "from animals", "from decomposers"], "Plants capture light energy."),
    ("A compost bin turns food scraps into soil. Which living things do this?", "decomposers such as worms, fungi and bacteria", ["producers such as grass", "predators such as dingoes", "the Sun alone"], "Composting uses decomposers."),
    ("Seagrass grows in shallow sea water. What is its role?", "a producer that feeds dugongs and turtles", ["a decomposer", "a predator", "a non-living thing"], "Seagrass makes food from sunlight."),
    ("What would happen if there were no decomposers?", "Dead plants and animals would pile up and soil would lose nutrients.", ["Plants would grow faster.", "Animals would stop eating.", "Nothing would change."], "Decomposers recycle nutrients."),
])
POOL5 = pool(R, [
    ("Mia puts one slice of bread in a warm, damp place and one in a cold, dry place. Which grows mould first?", "the slice in the warm, damp place", ["the slice in the cold, dry place", "both at the same time", "neither will grow mould"], "Decomposers grow best when it is warm and moist."),
    ("In Mia's test, what should she keep the same?", "the kind and size of bread", ["the temperature", "the dampness", "nothing"], "Only the conditions should change."),
    ("Jack buries an apple core and a plastic bottle cap. After 6 weeks, which has changed most?", "the apple core", ["the bottle cap", "both the same", "neither"], "Decomposers break down natural materials, not plastic."),
    ("Ruby weighs leaves in a compost bin each week: 500 g, 410 g, 330 g, 260 g. What does this show?", "The leaves are being broken down by decomposers.", ["The leaves are growing.", "The scale is broken.", "Nothing is happening."], "The mass goes down as they decay."),
    ("Kai says, 'Fungi are producers because they grow in the soil.' What is wrong?", "Fungi cannot make food from sunlight; they feed on dead matter.", ["Fungi are animals.", "Fungi make their own sunlight.", "Nothing is wrong."], "Growing in soil does not make something a producer."),
    ("Why should a compost bin be kept a little damp?", "Decomposers need water to work well.", ["to stop decomposers working", "to grow fish", "because dry food breaks down faster"], "Moisture, warmth and air help decomposition."),
])


def main():
    sets = U.sets([
        ("Producer, consumer or decomposer?", [(g_role, 10), (POOL1, 5), (g_pick, 5)]),
        ("Roles in food webs", [(sg_prod, 4), (sg_kind, 5), (g_pick, 5), (POOL1, 3), (g_role, 3)]),
        ("Decomposers", [(us_which, 3), (g_ret, 6), (us_b1, 6), (POOL1, 2), (g_role, 3)]),
        ("The cycle of matter", [(us_arrow, 4), (g_ret, 2), (us_compost, 3), (g_pick, 5), (us_b1, 3), (g_role, 3)]),
        ("Investigations", [(POOL5, 6), (us_b5, 6), (g_role, 4), (g_pick, 4)]),
    ])
    make_au(YEAR, "producers-consumers-and-decomposers", SORT, "AC9S4U01", "Biological sciences",
            "Explain the roles and interactions of consumers, producers and decomposers within a habitat and how food chains represent "
            "feeding relationships (summary of the Australian Curriculum v9.0 Science content description).",
            "Producers, Consumers and Decomposers", "Producers, consumers and decomposers",
            "Free Year 4 science worksheets on producers, consumers and decomposers in Australian habitats: gum trees, koalas, dingoes, "
            "fungi, earthworms and dung beetles, and how matter is recycled. 100 questions with answers.",
            "Make food, eat food, break down.", "Producers make food, consumers eat it, decomposers recycle dead matter.",
            "<p><b>Every living thing in a habitat has a role.</b></p><ul>"
            "<li>Producers (plants, algae, seagrass) make their own food using sunlight.</li>"
            "<li>Consumers (animals) eat other living things for energy.</li>"
            "<li>Decomposers (fungi, bacteria, earthworms, dung beetles) break down dead things and waste, returning nutrients to the soil.</li></ul>",
            [("A mushroom grows on a log. Role?", ["it cannot make food from sunlight", "it feeds on dead wood"], "decomposer"),
             ("A dugong eats seagrass. Role?", ["it eats another living thing"], "consumer")],
            ["Calling fungi such as mushrooms plants (they are decomposers).", "Thinking decomposers are only pests that spoil food.",
             "Thinking animals can make their own food."],
            [("What is the difference between a producer and a consumer?", "A producer, such as a gum tree, makes its own food from sunlight. A consumer, such as a koala, gets its energy by eating other living things."),
             ("Which living things are decomposers?", "Fungi, bacteria, earthworms, slaters and dung beetles. They break down dead plants, animals and waste."),
             ("Why do decomposers matter?", "They recycle nutrients from dead matter back into the soil, so new plants can grow.")],
            sets)


if __name__ == "__main__":
    main()
