# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Biology): Ecology
  python tools/gen_uk_science_y11_ecology.py
Communities and interdependence, abiotic and biotic factors, adaptations, trophic levels and food chains, sampling
with quadrats and transects, the carbon and water cycles and decomposition, biodiversity and human impacts (land use,
deforestation, global warming, pollution) and ways of maintaining biodiversity. Reuses the US Biology ecosystem, energy
flow, population and carbon cycle questions in British English.
Wrong answers come from real mistakes: "temperature is a biotic factor", "the mean per quadrat is the population",
"decomposers are producers", "all the energy passes to the next trophic level".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62104)
ES, EF, PC, CC = "bio_ecosystem_stability_and_biodiversity", "bio_energy_flow_and_matter_cycling", "bio_populations_and_carrying_capacity", "bio_carbon_cycle"
us_dist, us_survey, us_edata = us(ES, "g_dist"), us(ES, "g_survey"), us(ES, "g_data")
us_lvl, us_pyr, us_role, us_matter = us(EF, "g_lvl"), us(EF, "g_pyr"), us(EF, "g_role"), us(EF, "g_matter")
us_ten = us(EF, "g_ten", rep=(("The grass capture", "The grass captures"),))
us_density = us(PC, "g_density")
us_air, us_path, us_ml = us(CC, "g_air"), us(CC, "g_path"), us(CC, "g_ml")

FAC = [("light intensity", "abiotic"), ("temperature", "abiotic"), ("moisture levels", "abiotic"), ("soil pH", "abiotic"), ("wind intensity", "abiotic"),
       ("carbon dioxide levels", "abiotic"), ("oxygen levels in water", "abiotic"), ("mineral content of the soil", "abiotic"),
       ("availability of food", "biotic"), ("new predators arriving", "biotic"), ("new pathogens", "biotic"), ("competition between species", "biotic"), ("number of pollinators", "biotic")]


def g_factor():
    f, a = R.choice(FAC)
    if not once(("fa", f)):
        return None
    return item("Is %s a biotic or an abiotic factor?" % f, a, [x for x in ["biotic", "abiotic", "neither", "both"] if x != a],
                "Abiotic factors are non-living; biotic factors are living.")


AD = [("A camel can go for days without drinking.", "functional"), ("A polar bear has thick fur and a layer of fat.", "structural"),
      ("Swallows migrate south in winter.", "behavioural"), ("A cactus has spines instead of leaves.", "structural"), ("A desert rat makes very concentrated urine.", "functional"),
      ("Hedgehogs hibernate through the winter.", "behavioural"), ("An arctic fox has small ears.", "structural"), ("A frog lays thousands of eggs.", "functional")]


def g_adapt():
    s, a = R.choice(AD)
    if not once(("ad", s)):
        return None
    return item("%s What type of adaptation is this?" % s, a, [x for x in ["structural", "behavioural", "functional", "not an adaptation"] if x != a],
                "Structural: body shape. Behavioural: how it acts. Functional: processes inside the body.")


PL = [("daisies", "a school field"), ("buttercups", "a meadow"), ("dandelions", "a park lawn"), ("clover plants", "a playing field"), ("limpets", "a rocky shore")]


def g_quad():
    sp, place = R.choice(PL)
    n = R.choice([4, 5, 6])
    mean = R.choice(range(2, 13))
    cs = [mean + R.choice([-2, -1, 0, 1, 2]) for _ in range(n - 1)]
    cs.append(mean * n - sum(cs))
    if min(cs) < 0 or len(set(cs)) < 3:
        return None
    area = R.choice([50, 80, 100, 120, 150, 200, 250, 300, 400, 500])
    if not once(("qd", tuple(cs), area)):
        return None
    tab = table(["Quadrat"] + [str(i + 1) for i in range(n)], [["Number of %s" % sp] + [str(c) for c in cs]])
    k = R.choice(["mean", "pop", "pop"])
    if k == "mean":
        return item(tab + "These are counts of %s in 1 m² quadrats on %s. What is the mean number per quadrat?" % (sp, place), str(mean),
                    [str(sum(cs)), str(max(cs)), "{:,}".format(mean * area)], "%d ÷ %d = %d." % (sum(cs), n, mean))
    return item(tab + "These are counts of %s in 1 m² quadrats on %s. The area is %d m². Estimate the population." % (sp, place, area), "{:,}".format(mean * area),
                ["{:,}".format(sum(cs) * area), str(mean), "{:,}".format(sum(cs))], "Mean %d per m² × %d m² = {:,}.".format(mean * area) % (mean, area))


B1 = bank([
    ("What is a community?", "all the populations of different species living in a habitat", ["one species only", "the non-living parts of a habitat", "all the members of one family"], "A population is one species."),
    ("What is interdependence?", "species depending on each other for food, shelter, pollination and seed dispersal", ["one species living alone", "competition for light only", "animals depending on rocks"], "Removing one species can affect the whole community."),
    ("What do animals often compete for?", "food, mates and territory", ["light and carbon dioxide", "minerals from the soil only", "nothing"], "Plants compete for light, space, water and minerals."),
    ("What are extremophiles?", "organisms that live in extreme conditions such as high temperature or salt", ["animals that eat only plants", "very large animals", "plants that grow fast"], "For example, bacteria in deep-sea vents."),
])
B3 = bank([
    ("Why are quadrats placed at random?", "so the sample is not biased", ["to save time", "so you count more plants", "so they overlap"], "Use random coordinates."),
    ("How is a transect used?", "Quadrats are placed along a line to see how numbers change across a habitat.", ["One quadrat is used in the middle.", "Animals are trapped and marked.", "Soil is weighed."], "For example, from a hedge into a field."),
])
B4 = bank([
    ("How do microorganisms return carbon to the atmosphere?", "Decomposers respire as they break down dead material, releasing carbon dioxide.", ["They photosynthesise.", "They make fossil fuels quickly.", "They absorb carbon dioxide."], "Decay also returns mineral ions to the soil."),
    ("Which process removes carbon dioxide from the air?", "photosynthesis", ["respiration", "combustion", "decomposition"], "Plants and algae."),
    ("What is the main way water moves from plants to the air?", "transpiration", ["condensation", "precipitation", "photosynthesis"], "Water evaporates from leaves."),
])
B5 = bank([
    ("What is biodiversity?", "the variety of all the different species of organisms on Earth or in an ecosystem", ["the number of animals of one species", "the size of the largest animal", "the amount of rain"], "High biodiversity makes an ecosystem more stable."),
    ("Why does destroying peat bogs add to global warming?", "Peat releases carbon dioxide when it is burned or decays.", ["Peat absorbs oxygen.", "Peat makes the air cooler.", "Peat is a renewable fuel."], "Peat is also used as compost."),
    ("Give one reason for deforestation.", "to grow crops for biofuels", ["to increase biodiversity", "to absorb more carbon dioxide", "to make more peat"], "Also cattle farming and rice fields."),
    ("Give one way to protect biodiversity.", "breeding programmes for endangered species", ["cutting down hedgerows", "burning more fossil fuels", "building on wetlands"], "Also protecting habitats, hedgerows and recycling."),
    ("Give one effect of global warming on species.", "Some species move to new areas as their habitat changes.", ["All species become larger.", "Sea levels fall.", "No species are affected."], "Distribution changes."),
])

if __name__ == "__main__":
  build(U, 11, "ecology", 4, "Biology", "Ecology",
      "Communities and interdependence; abiotic and biotic factors; adaptations; levels of organisation in an ecosystem and food chains; sampling with quadrats and transects; how materials are cycled (the carbon and water cycles) and decomposition; biodiversity and the effects of human interaction on ecosystems; maintaining biodiversity.",
      "Ecology", "Ecology",
      "Free Year 11 GCSE Combined Science worksheets on ecology: biotic and abiotic factors, adaptations, food chains, quadrats, the carbon and water cycles, biodiversity and human impacts. 100 questions with answers.",
      "Estimate a population: mean per m² × total area.",
      "Abiotic factors are non-living; biotic factors are living.",
      "<p><b>Organisms in a community depend on each other.</b></p><ul><li>Abiotic: light, temperature, water, pH, wind. Biotic: food, predators, pathogens, competition.</li>"
      "<li>Quadrats: find the mean number per m², then multiply by the area.</li>"
      "<li>Carbon is taken in by photosynthesis and returned by respiration, decay and combustion.</li></ul>",
      [("Mean 4 daisies per m². Field 200 m²?", ["4 × 200"], "800"), ("Is soil pH biotic or abiotic?", ["Not living"], "abiotic")],
      ["Thinking temperature is a biotic factor.", "Using the mean per quadrat as the population.", "Thinking all the energy passes to the next level."],
      [("How do you estimate a population with quadrats?", "Place quadrats at random, count the organisms in each, find the mean per quadrat, then multiply by the total area (in quadrat areas)."),
       ("What is the difference between biotic and abiotic factors?", "Biotic factors are living, such as predators and food. Abiotic factors are non-living, such as light, temperature and soil pH."),
       ("Why is biodiversity important?", "High biodiversity makes ecosystems more stable, because species depend on each other for food, shelter and keeping the physical environment.")],
      [("Communities", B1 + [(g_factor, 8), (us_role, 4), (g_adapt, 4)]),
       ("Food chains", [(us_lvl, 8), (us_pyr, 6), (us_ten, 6)]),
       ("Sampling", B3 + [(g_quad, 13), (us_density, 5)]),
       ("Cycles and decay", B4 + [(us_air, 6), (us_path, 4), (us_matter, 3), (us_ml, 4)]),
       ("Biodiversity", B5 + [(us_dist, 6), (us_survey, 5), (us_edata, 4)])])
