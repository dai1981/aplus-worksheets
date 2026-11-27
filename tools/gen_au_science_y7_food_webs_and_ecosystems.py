# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U02: food webs, energy flow, interactions between organisms (competition,
predation, mutualism, parasitism) and the effects of human activity, including introduced species in Australia.
  python tools/gen_au_science_y7_food_webs_and_ecosystems.py
Australian food webs (au_webs.py) with the SG Primary 6 web makers, the SG Secondary 2 interaction makers, the UK Year 8 pyramid
makers and the US Grade 7 interaction makers, plus own questions on cane toads, rabbits, foxes and feral cats.
Wrong answers come from real mistakes: thinking energy is recycled like matter, thinking a predator's removal only helps the ecosystem,
and calling every close relationship mutualism.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit
import au_webs

YEAR, SORT = 7, 2
U, R, P, src = AU(seed_of(YEAR, SORT))
au_webs.add()
NA = ["zebra", "oxpecker", "lynx", "hare", "wolves", "wolf", "elk", "moose", "deer", "otter", "corn", "macaque", "polar bear", "sparrowhawk", "blue tit", "oak", "shrew", "seal", "durian"]
SG = "gen_sg_science_p6_food_chains_and_food_webs"
src.mod(SG).WEBS = au_webs.NAMES
w_down = src(SG, "g_down", drop=NA)
w_up = src(SG, "g_up", drop=NA)
w_count = limit(src(SG, "g_count"), 3)
w_kind = limit(src(SG, "g_kind"), 4)
S2 = "gen_sg_science_s2_interactions_within_ecosystems"
s2_energy = limit(src(S2, "g_energy"), 4)
s2_rel = src(S2, "g_rel", drop=NA)
s2_fact = src(S2, "g_fact", drop=NA)
s2_b1 = src.B(S2, "B1", drop=NA)
s2_b5 = src.B(S2, "B5", drop=NA)
Y8 = "gen_uk_science_y8_ecosystems_and_food_webs"
y8_pyr = limit(src(Y8, "g_pyr", drop=NA), 4)
y8_bio = limit(src(Y8, "g_bio", drop=NA), 3)
y8_poll = src(Y8, "g_poll", drop=NA)
y8_b1 = src.B(Y8, "B1", drop=NA)
G7 = "gen_us_science_g7_interactions_in_ecosystems"
g7_kind = src(G7, "g_kind", drop=NA)
g7_which = src(G7, "g_which", drop=NA)
g7_pred = src(G7, "g_predict", drop=NA)
g7_b1 = src.B(G7, "B1")
g7_b5 = src.B(G7, "B5")

INTRO = [("cane toads", "eat native insects and poison native predators such as quolls and goannas that eat them"),
         ("European rabbits", "eat grasses and seedlings and compete with native herbivores, causing erosion"),
         ("red foxes", "hunt small native mammals and ground-nesting birds"),
         ("feral cats", "hunt native birds, reptiles and small mammals"),
         ("carp", "stir up mud in rivers, making the water cloudy for native fish"),
         ("lantana", "forms thick bushes that crowd out native plants", 1),
         ("feral pigs", "dig up soil and eat native plants and frogs")]


def g_intro():
    row = R.choice(INTRO)
    a, eff = row[0], row[1]
    if len(row) == 3:
        return None
    w = sorted({x[1] for x in INTRO if x[0] != a and len(x) == 2})
    return tq("How do %s harm Australian ecosystems?" % a, "They " + eff + ".", ["They " + x + "." for x in R.sample(w, 3)],
              "Introduced species often have no natural predators here, so their numbers grow quickly.")


POOL1 = pool(R, [
    ("Where does almost all the energy in an ecosystem come from?", "the Sun", ["the soil", "decomposers", "the top predator"], "Producers capture light energy."),
    ("Why do food chains rarely have more than five links?", "Energy is lost at each step, mostly as heat, so little reaches the top.", ["Animals run out of food at night.", "Predators eat plants.", "Energy is made at each step."], "Only about 10% passes on."),
    ("Is energy recycled in an ecosystem like matter is?", "No. Energy flows through and is lost as heat; matter is recycled.", ["Yes, exactly the same way.", "Energy is made by decomposers.", "Matter is lost as heat."], "Matter cycles; energy flows."),
    ("What is competition?", "organisms trying to get the same limited resource", ["one organism eating another", "both organisms helping each other", "a parasite living on a host"], "For example, kangaroos and rabbits compete for grass."),
    ("Clownfish live among sea anemone tentacles and clean them; the anemone protects the clownfish. Which relationship is this?", "mutualism", ["parasitism", "predation", "competition"], "Both benefit."),
    ("A tick feeds on a koala's blood. Which relationship is this?", "parasitism", ["mutualism", "competition", "producer–consumer"], "The tick benefits; the koala is harmed."),
    ("Why were cane toads introduced to Queensland in 1935?", "to control cane beetles in sugar cane crops", ["to feed koalas", "to clean rivers", "as pets"], "They did not control the beetles and spread widely."),
    ("Crown-of-thorns starfish eat coral. What happens to a reef when their numbers explode?", "Large areas of coral die, affecting the fish that depend on it.", ["The coral grows faster.", "Nothing changes.", "More fish arrive."], "One population change spreads through the food web."),
    ("Which human activity helps protect food webs?", "removing feral animals and protecting habitats", ["clearing native bush", "dumping rubbish in rivers", "bringing in new predators"], "Conservation keeps ecosystems balanced."),
    ("Why does a food web with many species usually cope better with change?", "If one food source is lost, animals can eat others.", ["There is less energy.", "There are fewer predators.", "Plants grow faster."], "Diversity makes ecosystems more stable."),
])
POOL5 = pool(R, [
    ("A survey counts 1000 grasshoppers, 80 lizards and 5 kookaburras in a paddock. What does this pattern show?", "There are fewer organisms at each higher feeding level.", ["Top predators are the most common.", "Grasshoppers eat kookaburras.", "Energy increases up the chain."], "Less energy reaches higher levels."),
    ("Foxes are removed from a reserve. Bilby numbers rise, then grass seeds become scarce. What is the best explanation?", "More bilbies eat more seeds, so food becomes limited.", ["Foxes ate the seeds.", "Bilbies stopped eating.", "Seeds grow faster without foxes."], "Changes pass along the web."),
    ("Scientists count frogs in a wetland each spring for 10 years. Why collect data for so long?", "to see real trends, not just changes from one year to the next", ["because frogs are slow", "to make the data smaller", "it is not useful"], "Long-term data shows patterns."),
    ("Which method is best for estimating the number of plants in a large paddock?", "count plants in several random 1 m squares (quadrats) and scale up", ["count every plant", "guess", "count only the biggest plants"], "Sampling saves time and is reliable if random."),
    ("A student says, 'Removing all predators is good for an ecosystem.' Why is this not correct?", "Prey numbers can grow too large and eat out their food supply.", ["Predators make energy.", "Predators are producers.", "Prey stop eating without predators."], "Predators help keep balance."),
    ("Why do scientists test a biological control (such as a virus for rabbits) carefully before releasing it?", "It might also harm native species.", ["It is always harmless.", "It makes rabbits bigger.", "Testing is not needed."], "Cane toads show what can go wrong."),
])


def main():
    sets = U.sets([
        ("Energy in ecosystems", [(POOL1, 5), (s2_energy, 4), (y8_pyr, 4), (y8_b1, 4), (w_kind, 3)]),
        ("Food web changes", [(w_down, 7), (w_up, 7), (w_count, 3), (g7_pred, 3)]),
        ("Interactions", [(s2_rel, 6), (g7_kind, 5), (g7_which, 4), (s2_b1, 3), (POOL1, 2)]),
        ("Human impact in Australia", [(g_intro, 7), (POOL1, 3), (s2_fact, 4), (y8_bio, 3), (y8_poll, 3)]),
        ("Investigations", [(POOL5, 6), (s2_b5, 4), (g7_b5, 3), (g7_b1, 3), (g_intro, 2), (w_down, 2)]),
    ])
    make_au(YEAR, "food-webs-and-ecosystems", SORT, "AC9S7U02", "Biological sciences",
            "Use models of food webs to describe how energy flows through ecosystems and how organisms interact, and explain how human "
            "activities can affect these interactions (summary of the Australian Curriculum v9.0 Science content description).",
            "Food Webs and Ecosystems", "Food webs and ecosystems",
            "Free Year 7 science worksheets on food webs and ecosystems: energy flow and pyramids, competition, predation, mutualism and "
            "parasitism, and introduced species such as cane toads and foxes. 100 questions with answers.",
            "Energy flows; matter cycles.", "Changes to one population spread through the whole food web.",
            "<p><b>A food web shows how energy flows from producers to consumers in an ecosystem.</b></p><ul>"
            "<li>Only about 10% of the energy at one level passes to the next; the rest is lost, mostly as heat.</li>"
            "<li>Organisms interact through predation, competition, mutualism (both benefit) and parasitism (one is harmed).</li>"
            "<li>Introduced species such as cane toads, rabbits, foxes and cats can upset Australian food webs.</li></ul>",
            [("Producers have 10 000 kJ. About how much reaches herbivores?", ["about 10% passes on"], "about 1000 kJ"),
             ("A tick on a koala. Relationship?", ["the tick benefits", "the koala is harmed"], "parasitism")],
            ["Thinking energy is recycled like matter.", "Thinking removing predators always helps an ecosystem.",
             "Calling every close relationship mutualism (in parasitism one is harmed)."],
            [("Why is energy lost along a food chain?", "Each organism uses most of the energy it takes in to live, move and keep warm. This energy is lost as heat, so only about 10% is passed on."),
             ("Why are cane toads a problem?", "Cane toads are poisonous. Native predators such as quolls, goannas and some snakes die when they eat them, and the toads compete with native animals for food."),
             ("What is the difference between mutualism and parasitism?", "In mutualism both organisms benefit. In parasitism the parasite benefits and the host is harmed.")],
            sets)


if __name__ == "__main__":
    main()
