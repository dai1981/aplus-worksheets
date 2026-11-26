# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Biology): Ecosystems and Food Webs
  python tools/gen_uk_science_y8_ecosystems_and_food_webs.py
Relationships in an ecosystem: food chains and webs, interdependence (what happens when one population changes),
energy transfer between trophic levels, competition, predator and prey, limiting factors, how organisms affect their
environment, the accumulation of toxic materials in food chains, and the importance of insect pollinators.
Reuses the food-web, energy, interaction, population and ecosystem-change questions of the US Grade 7 units in
British English and adds UK questions (pyramids of numbers, bioaccumulation, pollinators).
Wrong answers come from real mistakes: "arrows point to what is eaten", "removing a predator has no effect",
"energy is recycled in a food chain", "poison is diluted up a food chain".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61805)
R = U.R
P = People(R)
uk_sci.USED.clear()
IN = adopt_us("gen_us_science_g7_interactions_in_ecosystems", U)
CY = adopt_us("gen_us_science_g7_cycling_of_matter_and_energy_flow", U)
RP = adopt_us("gen_us_science_g7_resources_and_populations", U)
EC = adopt_us("gen_us_science_g7_ecosystem_changes", U)
us_kind, us_which, us_pred = ukm(IN.g_kind), ukm(IN.g_which), ukm(IN.g_predict)
us_web, us_energy = ukm(CY.g_web), ukm(CY.g_energy)
us_table, us_graph, us_limit = ukm(RP.g_table), ukm(RP.g_graph), ukm(RP.g_limit)
us_data, us_type = ukm(EC.g_data), ukm(EC.g_type)

CHAINS = [["plankton", "small fish", "seal", "polar bear"], ["grass", "insect", "shrew", "owl"], ["algae", "water flea", "minnow", "pike"],
          ["oak leaves", "caterpillar", "blue tit", "sparrowhawk"], ["seaweed", "periwinkle", "crab", "gull"]]
TOX = [("DDT (an insecticide)", "ppm"), ("mercury", "ppm"), ("a pesticide", "ppm")]


def g_bio():
    ch = R.choice(CHAINS)
    tox, u = R.choice(TOX)
    base = R.choice([0.02, 0.04, 0.05])
    f = R.choice([10, 20])
    conc = [round(base * f ** i, 2) for i in range(4)]
    k = R.choice(["most", "why", "times", "least"])
    if not once(("bi", ch[0], k)):
        return None
    tab = table(["Organism", "Concentration of %s (%s)" % (tox, u)], [[o, "{:,}".format(c) if c >= 1 else str(c)] for o, c in zip(ch, conc)])
    intro = tab + "The food chain is %s. " % " → ".join(ch)
    if k == "most":
        return item(intro + "Which organism has the highest concentration of the poison?", ch[3], ch[:3], "The top predator: poison builds up at each level.")
    if k == "least":
        return item(intro + "Which organism has the lowest concentration?", ch[0], ch[1:], "The producer at the bottom.")
    if k == "why":
        return item(intro + "Why does the concentration increase along the chain?", "Each animal eats many of the one below, and the poison is not broken down or excreted.",
                    ["The poison is made by the animals.", "Bigger animals drink more rain.", "The poison is diluted at each step."], "Bioaccumulation.")
    g = "%d times" % f
    return item(intro + "How many times greater is the concentration in the %s than in the %s?" % (ch[2], ch[1]), g, uniq(g, ["%d times" % (f * 2), "%d times" % (f // 2), "2 times", "100 times", "1,000 times"]),
                "%s ÷ %s = %d." % (conc[2], conc[1], f))


POLL = [("Why are insect pollinators such as bees important to farmers?", "Many crops need insects to carry pollen so that fruits and seeds form.", ["Bees eat crop pests only.", "Bees make the soil richer.", "Crops do not need pollen."]),
        ("What could happen to apple harvests if bee numbers fall a lot?", "Fewer flowers are pollinated, so fewer apples grow.", ["More apples grow.", "Apples grow without flowers.", "Nothing would change."]),
        ("Why do some flowers have bright petals and a sweet scent?", "to attract insects that carry pollen", ["to scare away insects", "to make oxygen", "to store water"]),
        ("How do pesticides sprayed on crops sometimes harm bees?", "They can poison bees that visit the flowers.", ["They feed the bees.", "They make bees bigger.", "They have no effect on insects."]),
        ("Which action helps pollinators?", "planting wildflowers and leaving areas uncut", ["paving over gardens", "spraying more pesticide", "removing all hedges"]),
        ("What is interdependence?", "Living things in an ecosystem depend on each other for food, shelter and pollination.", ["Each species lives alone.", "Only plants depend on animals.", "Animals never depend on plants."])]


def g_poll():
    q, a, w = R.choice(POLL)
    if not once(("po", q)):
        return None
    return item(q, a, w, "Plants and animals depend on each other.")


def g_pyr():
    ch = R.choice(CHAINS)
    n = [R.choice([1000, 2000, 5000]), R.choice([200, 300, 400]), R.choice([20, 30, 40]), R.choice([1, 2, 3])]
    k = R.choice(["top", "shape", "energy", "prod"])
    if not once(("py", ch[0], k)):
        return None
    tab = table(["Organism", "Number in the area"], [[o, "{:,}".format(x)] for o, x in zip(ch, n)])
    if k == "top":
        return item(tab + "Which organism is the top predator?", ch[3], ch[:3], "Last in the chain; nothing eats it.")
    if k == "prod":
        return item(tab + "Which organism is the producer?", ch[0], ch[1:], "It makes its own food by photosynthesis.")
    if k == "shape":
        return item(tab + "Why are there fewer animals at each level going up?", "Energy is lost at each level, so less is available to support animals higher up.",
                    ["Bigger animals are always rarer for no reason.", "Energy is recycled.", "Top predators eat producers."], "Energy is lost as heat and movement.")
    return item(tab + "Where does most of the energy taken in by the %s go?" % ch[1], "It is used for life processes and lost as heat, not passed on.", ["All of it passes to the %s." % ch[2], "It is turned into plants.", "It is stored for ever."], "Only about 10% passes on.")


B1 = bank([
    ("In a food chain, what do the arrows show?", "the direction energy flows: from what is eaten to what eats it", ["what eats what, pointing at the food", "the size of each animal", "where each animal lives"], "Arrow means 'is eaten by'."),
    ("What is a producer?", "a plant or alga that makes its own food by photosynthesis", ["an animal that eats plants", "a top predator", "a decomposer"], "Start of every chain."),
    ("What is a consumer?", "an organism that gets energy by eating other organisms", ["a plant", "a source of light", "a mineral"], "Herbivores and carnivores."),
    ("What is a food web?", "many food chains joined together", ["one food chain", "a list of plants", "a spider's web"], "More realistic."),
    ("What do decomposers do?", "break down dead organisms and waste, returning minerals to the soil", ["make food from light", "eat only live animals", "remove oxygen"], "Bacteria and fungi."),
    ("What is an ecosystem?", "all the living things in an area and their non-living surroundings", ["only the animals in an area", "only the weather", "a single food chain"], "Living and non-living parts."),
])
B5 = bank([
    ("Why are food webs more stable when they have more species?", "If one food source falls, animals can eat something else.", ["More species means less food.", "They are not more stable.", "Fewer species share food better."], "Biodiversity."),
    ("A disease kills most of the rabbits in an area. What happens to the foxes?", "Their numbers fall because they have less food.", ["They increase.", "They stay the same.", "They start eating grass."], "Interdependence."),
    ("Why is energy not recycled in a food chain like minerals are?", "Energy is lost as heat to the surroundings at each level.", ["It is recycled by decomposers.", "Plants make new energy from soil.", "It is stored in the predator forever."], "Energy flows, matter cycles."),
    ("Why do predator and prey populations rise and fall in cycles?", "More prey means more food for predators; then more predators eat more prey, so prey fall, then predators fall.", ["They are not linked.", "Predators eat plants when prey fall.", "Prey eat predators."], "Predator–prey cycles."),
])


def body():
    think = ("<p><b>In an ecosystem, living things depend on each other.</b></p>"
             "<ul><li>Food chains start with a producer; arrows show the flow of energy (what is eaten → what eats it).</li>"
             "<li>Only about a tenth of the energy passes on at each level, so there are fewer animals higher up.</li>"
             "<li>Poisons such as DDT build up along food chains, so top predators are harmed most.</li></ul>")
    ex = [("Grass → rabbit → fox: rabbits removed. Foxes?", ["Less food for foxes"], "decrease"),
          ("1,000 units in grass, 10% passed on. Rabbits get?", ["1,000 × 0.1"], "100 units")]
    mist = ["Drawing arrows towards what is eaten.", "Thinking energy is recycled.", "Thinking poison is diluted up a food chain."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Food chains and webs", B1 + [(us_web, 8), (g_pyr, 6)]),
        ("Energy in ecosystems", [(us_energy, 6), (g_pyr, 6), (us_web, 4), (us_kind, 4)]),
        ("Interdependence", [(us_kind, 4), (us_which, 7), (us_pred, 4), (g_poll, 5)]),
        ("Populations", [(us_table, 6), (us_graph, 6), (us_limit, 4), (us_data, 4)]),
        ("Poisons and change", B5 + [(g_bio, 10), (us_type, 3), (us_data, 3)]),
    ])
    make_ks3(8, "ecosystems-and-food-webs", 5, "Biology", "Relationships in an ecosystem",
             "The interdependence of organisms in an ecosystem, including food webs and insect pollinated crops; the importance of plant reproduction through insect pollination in human food security; how organisms affect, and are affected by, their environment, including the accumulation of toxic materials.",
             "Ecosystems and Food Webs",
             "Year 8 Science: Ecosystems and Food Webs Worksheets (Interdependence, Bioaccumulation)",
             "Ecosystems and Food Webs",
             "Free Year 8 science worksheets on ecosystems: food chains and webs, energy transfer, interdependence, populations, pollinators and the build-up of poisons in food chains. 100 questions with answers.",
             "Living things in an ecosystem depend on each other.",
             "Energy flows along food chains; poisons build up at the top.",
             body(),
             [("Which way do food chain arrows point?", "From the organism that is eaten to the one that eats it, showing the direction energy flows."),
              ("What is bioaccumulation?", "The build-up of a poison such as DDT or mercury along a food chain. Each animal eats many of the one below, so top predators get the highest concentration."),
              ("Why do insect pollinators matter for food?", "Many crops, such as apples and strawberries, need insects to carry pollen between flowers so that fruits and seeds can form.")],
             sets)


if __name__ == "__main__":
    main()
