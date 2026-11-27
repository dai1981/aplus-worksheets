# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 11: Organisms and their Environment
  python tools/gen_sg_science_s4_organisms_and_their_environment.py
Ecological terms (habitat, population, community, ecosystem, niche); food chains and food webs, trophic levels, producers,
consumers and decomposers; energy flow and energy losses between trophic levels; pyramids of numbers and biomass; the carbon cycle;
human impact: deforestation, pollution of water (eutrophication), overfishing, climate change; conservation in Singapore.
SG Primary 6 food webs, US NGSS energy and carbon makers and UK KS4 ecology makers are reused (Singapore names); the rest is here.
Wrong answers come from real mistakes: "energy is recycled in an ecosystem", "the arrows point to what is eaten", "a pyramid of numbers
is always pyramid-shaped", "eutrophication is caused by too few nutrients", "decomposers are consumers at the top".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 21
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

P6 = "gen_sg_science_p6_food_chains_and_food_webs"
p6_eats = src(P6, "g_eats", rep=[("pupils", "students")])
p6_kind = src(P6, "g_kind", rep=[("pupils", "students")])
p6_down = src(P6, "g_down", rep=[("pupils", "students")])
p6_up = src(P6, "g_up", rep=[("pupils", "students")])
us_ten = src("gen_uk_science_y11_ecology", "us_ten")
uk_quad = src("gen_uk_science_y11_ecology", "g_quad")
us_proc = src("gen_us_science_bio_carbon_cycle", "g_proc", drop=["geosphere", "hydrosphere"])

TERM = [("a habitat", "the place where an organism lives"), ("a population", "a group of organisms of one species living in the same area at the same time"),
        ("a community", "all the populations of different species living in an area"), ("an ecosystem", "a community and its non-living environment interacting together"),
        ("a producer", "an organism that makes its own food by photosynthesis"), ("a decomposer", "an organism that breaks down dead organic matter, such as bacteria and fungi"),
        ("a trophic level", "the position of an organism in a food chain"), ("a niche", "the role of a species in its ecosystem, including what it eats and where it lives")]
g_term = rows(R, TERM, "What is %s?", "Which term means %s?")


def g_eff():
    e1 = R.choice([10000, 12000, 15000, 20000, 25000, 40000, 50000, 80000])
    pc = R.choice([10, 8, 12, 15, 20, 5])
    e2 = e1 * pc / 100
    if R.random() < 0.5:
        return nq("Producers in a mangrove trap %d kJ/m² per year. Primary consumers gain %d kJ/m² per year. What is the efficiency of energy transfer?" % (e1, e2), pc,
                  [100 - pc, e1 / e2, pc * 10], "%", "Efficiency = %d ÷ %d × 100." % (e2, e1))
    return nq("Energy in the producers is %d kJ. If %d%% is passed to the primary consumers, how much energy do they get?" % (e1, pc), e2, [e1 - e2, e1 * pc, e1 / pc], " kJ",
              "%d × %d ÷ 100." % (e1, pc))


CHAINS = [("a rain tree", "caterpillars", "mynah birds", 1, (400, 900), (6, 20)), ("grass", "grasshoppers", "frogs", (2000, 6000), (200, 500), (5, 20)),
          ("phytoplankton", "zooplankton", "small fish", (50000, 90000), (3000, 8000), (40, 200)), ("a mango tree", "aphids", "ladybirds", 1, (2000, 5000), (30, 90)),
          ("algae", "snails", "fish", (30000, 60000), (300, 900), (8, 30))]


def g_pyr():
    p, c1, c2, n0, r1, r2 = R.choice(CHAINS)
    n0 = n0 if isinstance(n0, int) else R.randrange(*n0, 100)
    n1, n2 = R.randrange(*r1), R.randrange(*r2)
    k = R.choice(["shape", "bio"])
    data = "%s: %d; %s: %d; %s: %d" % (p.capitalize() if not p.startswith("a ") else "rain tree" if "rain" in p else "mango tree", n0, c1, n1, c2, n2)
    if k == "bio":
        return tq("A food chain is %s → %s → %s. Numbers counted: %s. Which trophic level has the largest biomass?" % (p, c1, c2, data), "the producers",
                  ["the primary consumers", "the secondary consumers", "they all have the same biomass"], "Biomass decreases at each trophic level because energy is lost; a pyramid of biomass is upright.")
    if n0 < n1:
        a = "inverted at the bottom: a narrow producer bar under a wider primary consumer bar"
    else:
        a = "upright: each bar narrower than the one below"
    return tq("A food chain is %s → %s → %s. Numbers counted: %s. What shape is the pyramid of numbers?" % (p, c1, c2, data), a,
              [x for x in ("inverted at the bottom: a narrow producer bar under a wider primary consumer bar", "upright: each bar narrower than the one below",
                           "all bars the same width", "widest at the top") if x != a], "Compare the numbers at each level: a single large producer can support many consumers.")


LOSS = [("respiration releasing energy as heat", True), ("undigested food lost in faeces", True), ("parts of organisms not eaten, such as bones and roots", True),
        ("excretion of urea", True), ("photosynthesis in the leaves of the producer", False), ("energy being recycled back to the Sun", False)]


def g_loss():
    good = [x for x, t in LOSS if t]
    bad = [x for x, t in LOSS if not t]
    if R.random() < 0.6:
        a = R.choice(good)
        return tq("Which is a way that energy is lost between trophic levels?", a, bad + ["energy being stored as nitrogen gas"], "Energy is lost as heat in respiration and in faeces, urine and uneaten parts.")
    a = R.choice(bad)
    w = R.sample(good, 3)
    return tq("Which is NOT a way that energy is lost between trophic levels?", a, w, "Energy flows one way through a food chain and is not recycled.")


HUM = [("cutting down rainforests", "loss of habitats and biodiversity, more carbon dioxide in the air and soil erosion"),
       ("fertiliser running off farmland into a lake", "eutrophication: algae grow quickly, die, and decomposers use up the oxygen, killing fish"),
       ("untreated sewage entering a river", "bacteria use up oxygen as they decompose it, so fish and other animals die"),
       ("catching too many fish (overfishing)", "fish populations fall below the level at which they can recover"),
       ("burning large amounts of fossil fuels", "more carbon dioxide in the air, contributing to global warming"),
       ("dumping plastic waste in the sea", "animals are trapped or swallow plastic, and microplastics enter food chains")]
g_hum = rows(R, HUM, "What is an effect of %s?", "Which human activity leads to this? “%s”")

EUT = ["Fertiliser containing nitrates and phosphates enters the lake.", "Algae grow rapidly and cover the surface (algal bloom).",
       "Light cannot reach plants below the surface, so they die.", "Decomposers break down dead plants and algae and use up oxygen.", "Fish and other animals die from lack of oxygen."]


def g_eut():
    i = R.randrange(len(EUT) - 1)
    a = EUT[i + 1]
    return tq("In eutrophication, which step comes straight after this: “%s”" % EUT[i], a, [x for j, x in enumerate(EUT) if j not in (i, i + 1)][:3],
              "Nutrients → algal bloom → plants die → decomposers use oxygen → fish die.")


CONS = [("Sungei Buloh Wetland Reserve", "protects mangroves and migratory birds"), ("Bukit Timah Nature Reserve", "protects primary rainforest and its species"),
        ("Sisters' Islands Marine Park", "protects coral reefs and marine life"), ("seed banks", "store seeds of plant species so they can be regrown"),
        ("fishing quotas and larger mesh sizes", "allow young fish to escape and fish populations to recover"), ("breeding programmes in zoos", "increase numbers of endangered species")]
g_cons = rows(R, CONS, "What is the conservation role of %s?", "Which conservation measure %s?")

POOL1 = pool(R, [
    ("In a food chain, what do the arrows show?", "the direction of energy flow, from the organism eaten to the eater", ["what each organism eats, pointing to its food", "the direction of movement", "which organism is bigger"], "Grass → grasshopper means the grasshopper eats grass."),
    ("Where does almost all the energy in an ecosystem come from?", "the Sun", ["the soil", "decomposers", "water"], "Producers capture light energy by photosynthesis."),
    ("Why are food chains rarely longer than five trophic levels?", "Too much energy is lost at each level to support more levels.", ["Animals cannot eat more than five kinds of food.", "There are not enough producers.", "Energy increases along the chain."], "Only about 10% passes on."),
    ("Why can a pyramid of numbers be inverted?", "A single large producer, such as a tree, can support many small consumers.", ["Energy increases up the chain.", "Producers are always the smallest.", "Some animals are not counted."], "A pyramid of biomass is usually upright."),
    ("What do decomposers do in the carbon cycle?", "They break down dead organisms and release carbon dioxide by respiration.", ["They take in carbon dioxide by photosynthesis.", "They turn carbon into oxygen.", "They store carbon as fossil fuels at once."], "They also recycle mineral ions."),
    ("Which process removes carbon dioxide from the air?", "photosynthesis", ["respiration", "combustion", "decay"], "Carbon becomes part of glucose."),
    ("Why is energy described as flowing through an ecosystem, while carbon is recycled?", "Energy is lost as heat and cannot be reused; carbon atoms are used again and again.", ["Energy is recycled by decomposers.", "Carbon is destroyed in respiration.", "Both are recycled."], "New energy comes from the Sun."),
    ("Why are mangrove forests important?", "They protect coasts from erosion, store carbon and provide nursery habitats for fish.", ["They make the sea more salty.", "They release oxygen only at night.", "They remove all pollution from the sea."], "Singapore protects mangroves at Sungei Buloh."),
    ("Why do herbivores need to eat more food than carnivores of the same size?", "Plant food has more indigestible material, so less energy is absorbed.", ["Herbivores are always larger.", "Plants contain no energy.", "Carnivores do not respire."], "More energy is lost in faeces."),
    ("Why is it more efficient for humans to eat plants than animals that eat plants?", "Less energy is lost because there is one fewer trophic level.", ["Plants contain more protein.", "Animals contain no energy.", "Plants grow faster than animals."], "More people can be fed from the same land."),
])
POOL5 = pool(R, [
    ("A pesticide is sprayed on a field. Why is its concentration highest in the top predators?", "It is not broken down or excreted, so it builds up at each trophic level (bioaccumulation).", ["Top predators eat the pesticide directly.", "Pesticides are made by predators.", "The pesticide is diluted along the chain."], "This happened with DDT."),
    ("Sewage enters a river. Why does the oxygen level fall downstream of the outlet?", "Aerobic bacteria multiply and use oxygen as they decompose the sewage.", ["Sewage contains no water.", "Fish make more oxygen.", "Sewage releases oxygen."], "Fish move away or die."),
    ("Why does deforestation increase the carbon dioxide in the air?", "Fewer trees remove CO₂ by photosynthesis, and burning or decay of wood releases CO₂.", ["Trees release CO₂ only at night.", "Soil absorbs more CO₂.", "Deforestation adds oxygen."], "It also reduces biodiversity."),
    ("Why is a pyramid of biomass a better picture of an ecosystem than a pyramid of numbers?", "It takes the size of organisms into account.", ["It counts every organism.", "It is always inverted.", "It shows only producers."], "Biomass is the dry mass of living material."),
    ("In a food web, the snakes are removed. What is likely to happen to the frogs that the snakes ate?", "The frog population increases at first.", ["The frog population falls at once.", "The frogs become producers.", "Nothing changes."], "Then food for frogs may run short."),
    ("Why do fishing quotas help to conserve fish stocks?", "Fewer fish are caught, so enough adults remain to breed.", ["They make fish grow faster.", "They increase pollution.", "They stop all fishing."], "Sustainable fishing."),
    ("Which method gives a fair estimate of the number of plants in a field?", "placing quadrats at random and calculating the mean number per quadrat", ["counting only the area with the most plants", "using one quadrat in the corner", "counting from a photograph of one patch"], "Random sampling avoids bias."),
    ("Why does eutrophication lead to fish deaths even though algae make oxygen?", "When the algae and plants die, decomposers use up the dissolved oxygen.", ["Algae produce poison.", "Fish eat too many algae.", "Algae remove all the carbon dioxide."], "The water becomes anaerobic."),
])


def main():
    sets = U.sets([
        ("Ecosystems and food webs", [(g_term, 7), (p6_eats, 4), (p6_kind, 4), (POOL1, 3), (p6_down, 2)]),
        ("Energy flow", [(us_ten, 6), (g_eff, 7), (g_loss, 4), (POOL1, 3)]),
        ("Pyramids and the carbon cycle", [(g_pyr, 7), (us_proc, 4), (POOL1, 4), (uk_quad, 3), (g_loss, 2)]),
        ("Human impact on ecosystems", [(g_hum, 9), (g_eut, 4), (g_cons, 5), (p6_up, 2)]),
        ("Conservation and exam-style questions", [(POOL5, 8), (g_cons, 3), (g_eff, 3), (uk_quad, 3), (g_hum, 3)]),
    ])
    make_ol(LV, SUBJ, "organisms-and-their-environment", SORT, "Organisms and their Environment",
            "Define ecological terms such as habitat, population, community, ecosystem, producer, consumer, decomposer and trophic level; describe food chains and "
            "food webs and the flow of energy through them; explain energy losses between trophic levels; interpret pyramids of numbers and biomass; describe the "
            "carbon cycle; describe the effects of human activities such as deforestation, water pollution and eutrophication, and the need for conservation "
            "(summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Organisms and their Environment", "Organisms and environment",
            "Free Secondary 4 O-Level Biology worksheets on organisms and their environment: food chains and webs, energy flow, pyramids, the carbon cycle, "
            "eutrophication, deforestation and conservation in Singapore. 100 questions with answers.",
            "Energy flows; matter cycles.", "Only about 10% of the energy passes to the next trophic level.",
            "<p><b>Energy enters as sunlight and leaves as heat.</b></p><ul>"
            "<li>Producer → primary consumer → secondary consumer → tertiary consumer; arrows show energy flow.</li>"
            "<li>At each level energy is lost in respiration (heat), faeces and uneaten parts, so pyramids get narrower.</li>"
            "<li>Carbon cycle: photosynthesis removes CO₂; respiration, decay and combustion return it.</li>"
            "<li>Human impact: deforestation, eutrophication, overfishing. Conservation: reserves, quotas, seed banks.</li></ul>",
            [("Producers 20 000 kJ, consumers 2000 kJ. Efficiency?", ["2000 ÷ 20 000 × 100"], "10%"),
             ("Fertiliser in a lake → ?", ["algal bloom", "decomposers use oxygen"], "fish die")],
            ["Saying energy is recycled.", "Drawing arrows to the food that is eaten.", "Saying a pyramid of numbers is always upright.",
             "Saying eutrophication is caused by too few nutrients."],
            [("Why is energy lost between trophic levels?", "Organisms use energy for respiration and lose it as heat; some is lost in faeces and urine, and some parts are not eaten."),
             ("What is eutrophication?", "Extra nutrients such as nitrates enter water and cause an algal bloom. Plants below die, decomposers use up the oxygen and fish die."),
             ("How is carbon recycled?", "Plants take in carbon dioxide in photosynthesis. Carbon passes along food chains and returns to the air by respiration, decomposition and combustion.")],
            sets)


if __name__ == "__main__":
    main()
