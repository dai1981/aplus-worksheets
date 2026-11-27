# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U01: food chains and food webs in Australian habitats.
  python tools/gen_au_science_y4_food_chains_and_food_webs.py
Australian food webs (bushland, billabong, Great Barrier Reef, outback desert) from au_webs.py, drawn with sci_foodweb and asked
with the SG Primary 6 food-web makers; the UK Year 4 food-chain makers with Australian animals.
Wrong answers come from real mistakes: drawing arrows from the eater to the food, putting the producer last, and thinking that
removing a predator makes every other population fall.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import au_webs

YEAR, SORT = 4, 2
U, R, P, src = AU(seed_of(YEAR, SORT))
au_webs.add()
SG = "gen_sg_science_p6_food_chains_and_food_webs"
src.mod(SG).WEBS = au_webs.NAMES
sg_eats = src(SG, "g_eats")
sg_kind = src(SG, "g_kind")
sg_prod = src(SG, "g_prod")
sg_count = limit(src(SG, "g_count"), 4)
sg_top = src(SG, "g_top")
sg_pp = src(SG, "g_pp")
sg_down = src(SG, "g_down")
sg_up = src(SG, "g_up")
sg_b1 = src.B(SG, "B1")
sg_b2 = src.B(SG, "B2")
sg_b5 = src.B(SG, "B5", drop=["mynah"])
UK = "gen_uk_science_y4_food_chains"
NA = ["otter", "trout", "badger", "hedgehog", "squirrel", "robin", "blue tit", "sparrowhawk", "polar bear", "seal", "lion", "zebra", "deer", "fox",
      "owl", "hawk", "rabbit", "vole", "thrush", "kestrel", "heron", "mayfly", "pike", "stoat", "weasel", "whale", "penguin", "orca", "walrus", "wolf"]
uk_word = src(UK, "g_word", drop=["a prey"])
uk_b1 = src.B(UK, "B1")
uk_b5 = src.B(UK, "B5")

CH = [["gum tree", "koala"], ["grass", "kangaroo", "dingo"], ["grass", "grasshopper", "kookaburra"], ["grass", "mouse", "brown snake"],
      ["gum tree", "possum", "powerful owl"], ["algae", "tadpole", "dragonfly nymph", "platypus"], ["waterweed", "yabby", "Murray cod"],
      ["phytoplankton", "zooplankton", "small fish", "coral trout", "reef shark"], ["seaweed", "green turtle"], ["native grass", "ant", "thorny devil"],
      ["native grass", "grasshopper", "bearded dragon", "goanna"], ["banksia flowers", "honey possum"], ["leaves", "caterpillar", "magpie"]]


def g_chain():
    ch = R.choice(CH)
    k = R.choice(["first", "last", "arrow"])
    if k == "first":
        return tq("In the food chain %s, which living thing is the producer?" % " → ".join(ch), ch[0], [x for x in ch[1:]] + ["the Sun"][:max(0, 4 - len(ch))] +
                  ["the decomposers"][:max(0, 3 - len(ch[1:]))], "The producer makes its own food from sunlight and comes first.")
    if k == "last":
        if len(ch) < 3:
            return None
        return tq("In the food chain %s, which animal is the top predator?" % " → ".join(ch), ch[-1], ch[:-1][-3:] if len(ch) >= 4 else ch[:-1] + ["the Sun"],
                  "The top predator is at the end of the chain; nothing in the chain eats it.")
    i = R.randrange(len(ch) - 1)
    a, b = ch[i], ch[i + 1]
    return tq("In a food chain, what does the arrow in “%s → %s” mean?" % (a, b), "The %s eats the %s." % (b, a),
              ["The %s eats the %s." % (a, b), "The %s and the %s are the same size." % (a, b), "The %s lives far from the %s." % (a, b)],
              "Arrows point from the food to the eater: they show which way energy flows.")


POOL1 = pool(R, [
    ("What does a food chain show?", "which living thing is eaten by which, and how energy passes along", ["where animals live", "how animals grow", "how plants make seeds"], "Energy passes from the food to the eater."),
    ("Where does the energy in every food chain first come from?", "the Sun", ["the soil", "water", "the top predator"], "Producers use sunlight to make food."),
    ("Which living thing is always at the start of a food chain?", "a producer, such as a plant", ["a predator", "a decomposer", "a herbivore"], "Producers make their own food."),
    ("What is a herbivore?", "an animal that eats only plants", ["an animal that eats only animals", "a plant that eats insects", "a decomposer"], "Koalas and kangaroos are herbivores."),
    ("What is a carnivore?", "an animal that eats only other animals", ["an animal that eats only plants", "a plant", "a fungus"], "Dingoes and reef sharks are carnivores."),
    ("What is an omnivore?", "an animal that eats both plants and animals", ["an animal that eats only seeds", "a producer", "an animal that eats nothing"], "Emus, possums and people are often omnivores."),
    ("Why is a food web more useful than one food chain?", "Most animals eat more than one kind of food.", ["Food webs are shorter.", "Food webs have no producers.", "Food chains show more animals."], "A web joins many chains."),
    ("What is a predator?", "an animal that hunts and eats other animals", ["an animal that is hunted", "a plant", "a decomposer"], "The animal that is eaten is the prey."),
    ("In the chain grass → kangaroo → dingo, which is the prey of the dingo?", "the kangaroo", ["the grass", "the dingo", "the Sun"], "Prey is the animal eaten."),
    ("Foxes and cats were brought to Australia. Why are they a problem in food webs?", "They eat many small native animals, such as bilbies and birds.", ["They only eat grass.", "They are producers.", "They have no effect."], "Introduced predators can upset food webs."),
])
POOL5 = pool(R, [
    ("Mia counts animals at a billabong: 200 tadpoles, 30 dragonfly nymphs, 2 platypuses. What pattern does she see?", "There are fewer animals higher up the food chain.", ["There are more animals at the top.", "All levels have the same number.", "Platypuses eat plants."], "Energy is lost at each step, so fewer animals can be supported."),
    ("Jack writes: koala → gum tree. What is wrong?", "The arrow points the wrong way; it should be gum tree → koala.", ["Koalas do not eat gum leaves.", "Gum trees eat koalas.", "Nothing is wrong."], "Arrows go from food to eater."),
    ("A drought kills much of the grass in the outback. Which animals are affected first?", "herbivores such as kangaroos and grasshoppers", ["only dingoes", "nothing", "only the Sun"], "Herbivores depend directly on plants."),
    ("Dingoes are removed from an area. Which change is most likely at first?", "There are more kangaroos.", ["There are fewer kangaroos.", "There is more grass.", "Nothing changes."], "With fewer predators, prey numbers rise."),
    ("Later, after there are many more kangaroos, what may happen to the grass?", "It is eaten down and there is less grass.", ["It grows taller.", "It turns into trees.", "Nothing happens."], "Changes pass along the food web."),
    ("Why do scientists study food webs before letting a new animal into an area?", "A new animal can change the numbers of many other living things.", ["New animals never change anything.", "To find the best colour of animals.", "Food webs only include plants."], "Cane toads are an example of a harmful introduction."),
])


def main():
    sets = U.sets([
        ("Food chains", [(g_chain, 10), (POOL1, 5), (uk_word, 5)]),
        ("Producers and consumers", [(sg_prod, 4), (sg_kind, 6), (uk_b1, 4), (POOL1, 3), (g_chain, 3)]),
        ("Reading food webs", [(sg_eats, 8), (sg_pp, 5), (sg_top, 4), (sg_count, 3)]),
        ("Changes in food webs", [(sg_down, 6), (sg_up, 6), (sg_b2, 4), (sg_b1, 2), (POOL1, 2)]),
        ("Investigations and explanations", [(POOL5, 6), (uk_b5, 4), (sg_b5, 3), (g_chain, 3), (sg_eats, 2), (uk_word, 2)]),
    ])
    make_au(YEAR, "food-chains-and-food-webs", SORT, "AC9S4U01", "Biological sciences",
            "Explain the roles and interactions of consumers, producers and decomposers within a habitat and how food chains represent "
            "feeding relationships (summary of the Australian Curriculum v9.0 Science content description).",
            "Food Chains and Food Webs", "Food chains and food webs",
            "Free Year 4 science worksheets on food chains and food webs in Australian habitats: the bush, a billabong, the Great Barrier "
            "Reef and the outback. Producers, predators and prey. 100 questions with answers.",
            "Arrows go from the food to the eater.", "A food chain starts with a producer; a food web joins many chains.",
            "<p><b>A food chain shows what eats what. The arrow points from the food to the animal that eats it.</b></p><ul>"
            "<li>Every chain starts with a producer (a plant or algae) that uses sunlight to make food.</li>"
            "<li>Consumers eat other living things: herbivores eat plants, carnivores eat animals, omnivores eat both.</li>"
            "<li>A food web joins many chains. If one population changes, others change too.</li></ul>",
            [("Grass → kangaroo → dingo. Which is the producer?", ["the chain starts with the plant"], "grass"),
             ("Dingoes are removed. Kangaroos?", ["fewer predators eat them"], "more kangaroos at first")],
            ["Drawing arrows from the eater to the food.", "Putting the producer at the end of the chain.",
             "Thinking that removing a predator makes every population fall."],
            [("Which way do arrows go in a food chain?", "From the food to the eater. The arrow shows the direction the energy moves: grass → kangaroo means the kangaroo eats the grass."),
             ("What is the difference between a food chain and a food web?", "A food chain is one path of feeding. A food web joins many food chains because most animals eat more than one kind of food."),
             ("What happens if one animal disappears from a food web?", "Its prey may increase and its predators may decrease or switch to other food. One change can affect many living things.")],
            sets)


if __name__ == "__main__":
    main()
