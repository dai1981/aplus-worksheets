# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Interactions within Ecosystems
  python tools/gen_sg_science_s2_interactions_within_ecosystems.py
An ecosystem is a community interacting with its physical environment; physical factors (air, water, temperature, light, minerals,
pH) affect survival; structural and behavioural adaptations; relationships between organisms: predator-prey, mutualism and
parasitism; energy flow through food chains and food webs (photosynthesis and respiration); decomposers recycle nutrients;
investigating an environment with data loggers; human impact and conservation.
The Singapore food webs (sg_webs) and the Primary 6 food web makers are reused with a new seed, at Secondary level wording.
Wrong answers come from real mistakes: "mutualism means one benefits and the other is harmed", "energy is recycled",
"decomposers are consumers that hunt", "an ecosystem is only the living things".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People
import gen_sg_science_p6_food_chains_and_food_webs as FW6

U = Unit(64206)
R = U.R
P = People(R)
FW6.U, FW6.R, FW6.P = U, R, P
EC = luse(U, "gen_uk_science_y8_ecosystems_and_food_webs", drop=[r"oak", r"blue tit", r"sparrowhawk", r"polar bear", r"seal", r"rabbit", r"fox", r"shrew", r"owl",
                                                               r"periwinkle", r"gull", r"apple", r"hedge", r"wildflower"])

REL = [("Clownfish live among sea anemones; the clownfish is protected and the anemone is cleaned and fed.", "mutualism"),
       ("Bees collect nectar from flowers and pollinate them.", "mutualism"),
       ("Bacteria in a cow's gut digest cellulose; the bacteria get food and shelter.", "mutualism"),
       ("Lichen is made of a fungus and an alga; the alga makes food and the fungus holds water.", "mutualism"),
       ("Oxpecker birds eat ticks off the backs of buffalo.", "mutualism"),
       ("A tapeworm lives in a human's intestine and absorbs digested food.", "parasitism"),
       ("Mosquitoes feed on human blood.", "parasitism"), ("Ticks feed on the blood of a dog.", "parasitism"),
       ("Mistletoe takes water and minerals from the tree it grows on.", "parasitism"), ("Head lice live on the human scalp and feed on blood.", "parasitism"),
       ("A kingfisher catches and eats mudskippers.", "predator-prey"), ("A python catches and eats rats.", "predator-prey"),
       ("A ladybird eats aphids on a hibiscus plant.", "predator-prey"), ("A shark hunts squid.", "predator-prey"),
       ("Long-tailed macaques and squirrels both eat the same fruits in a forest.", "competition")]


def g_rel():
    s, a = R.choice(REL)
    if not once(("rl", s)):
        return None
    return item(s + " Which relationship is this?", a, [x for x in ["mutualism", "parasitism", "predator-prey", "competition"] if x != a],
                {"mutualism": "Both organisms benefit.", "parasitism": "The parasite benefits and the host is harmed.",
                 "predator-prey": "One organism hunts and eats the other.", "competition": "Both need the same limited resource."}[a])


FACT = [("Few plants grow on the dark floor of a dense rainforest.", "light"), ("Mangrove trees grow in salty, waterlogged mud with little oxygen.", "air (oxygen)"),
        ("Corals die when sea water becomes too warm.", "temperature"), ("Fish in a pond die when the water becomes too acidic.", "pH (acidity or alkalinity)"),
        ("Plants grow poorly in soil that lacks nitrates.", "minerals"), ("Cacti survive in deserts where it rarely rains.", "water"),
        ("Fish gather near the surface of a pond with very little dissolved oxygen.", "air (oxygen)"), ("Seedlings grow towards a window.", "light"),
        ("Pitcher plants catch insects because the soil is poor in nitrogen.", "minerals"), ("A fern dries up when moved to a sunny, dry spot.", "water")]
FALL = ["light", "air (oxygen)", "temperature", "pH (acidity or alkalinity)", "minerals", "water"]


def g_fact():
    s, a = R.choice(FACT)
    if not once(("fc", s)):
        return None
    return item(s + " Which physical factor is most important here?", a, R.sample([x for x in FALL if x != a], 3), "Physical factors in the environment affect which organisms can survive.")


FWM = [upto(FW6.g_eats, 6), upto(FW6.g_by, 4), upto(FW6.g_kind, 6), upto(FW6.g_chain, 6), upto(FW6.g_down, 6), upto(FW6.g_up, 6), upto(FW6.g_pp, 5), upto(FW6.g_count, 4)]


def g_energy():
    e = R.choice([10000, 20000, 50000, 100000])
    c = lambda v: "{:,}".format(v)
    k = R.choice(["second", "third", "lost"])
    if not once(("en", e, k)):
        return None
    if k == "second":
        return item("Producers in a food chain trap %s kJ of energy. About 10%% passes to each next level. How much energy reaches the primary consumers?" % c(e), "%s kJ" % c(e // 10),
                    ["%s kJ" % c(e), "%s kJ" % c(e // 100), "%s kJ" % c(e * 10)], "10%% of %s = %s kJ." % (c(e), c(e // 10)))
    if k == "third":
        return item("Producers in a food chain trap %s kJ of energy. About 10%% passes to each next level. How much reaches the secondary consumers?" % c(e), "%s kJ" % c(e // 100),
                    ["%s kJ" % c(e // 10), "%s kJ" % c(e // 1000), "%s kJ" % c(e)], "%s → %s → %s kJ." % (c(e), c(e // 10), c(e // 100)))
    return item("Primary consumers take in %s kJ from producers but pass only %s kJ to secondary consumers. Where does most of the rest go?" % (c(e // 10), c(e // 100)),
                "It is used in respiration for life processes and lost as heat.", ["It is recycled back to the producers.", "It is destroyed.", "It is stored in the Sun."],
                "Energy flows through a food chain and is not recycled.")


B1 = bank([
    ("What is an ecosystem?", "a community of organisms interacting with each other and with their physical environment", ["only the plants in an area", "only the animals in an area", "the weather in an area"], "A pond, a mangrove swamp and a coral reef are ecosystems."),
    ("Which process traps the Sun's energy and brings it into an ecosystem?", "photosynthesis by producers", ["respiration by consumers", "decomposition", "evaporation"], "Producers convert light energy into chemical energy."),
    ("Which process releases the energy in food for organisms to use?", "respiration", ["photosynthesis", "pollination", "condensation"], "glucose + oxygen → carbon dioxide + water"),
    ("What is mutualism?", "a relationship in which both organisms benefit", ["one organism benefits and the other is harmed", "one organism eats the other", "neither organism is affected"], "For example, bees and flowers."),
    ("What is parasitism?", "a relationship in which the parasite benefits and the host is harmed", ["both organisms benefit", "the host benefits", "one organism hunts the other for food"], "A tapeworm is a parasite."),
    ("What do decomposers such as bacteria and fungi do?", "They break down dead organisms and waste, returning nutrients to the soil.", ["They make food by photosynthesis.", "They hunt live animals.", "They destroy energy."], "Plants take up the nutrients again."),
    ("Why is energy said to flow, but nutrients cycle, in an ecosystem?", "Energy is lost as heat at each step, but nutrients are returned to the soil by decomposers and used again.", ["Energy is recycled by decomposers.", "Nutrients are lost as heat.", "Both are recycled in the same way."], "The Sun keeps supplying new energy."),
    ("A student uses a data logger with a light sensor in a forest and in an open field. What is she investigating?", "how light intensity differs between the two habitats", ["the pH of the soil", "the number of birds", "the speed of the wind only"], "Probes can also measure temperature and pH."),
])
B5 = bank([
    ("Why is it important to conserve the mangroves at Sungei Buloh?", "They are habitats for many organisms and protect the coast from erosion.", ["They are only for tourists.", "They have no living things.", "Mangroves cause floods."], "Removing them affects the whole ecosystem."),
    ("Rats were reduced on an island. Then the number of birds that nest on the ground rose. Why?", "Fewer rats ate the birds' eggs and chicks.", ["Rats are producers.", "Birds eat rats.", "Rats help birds lay eggs."], "Removing a predator affects its prey."),
    ("Mosquito fish are added to ponds to control mosquitoes. Which relationship is used?", "predator-prey", ["mutualism", "parasitism", "competition"], "The fish eat mosquito larvae."),
    ("A farmer sprays a pesticide that kills all the insects in a field. Which is a likely result?", "Birds that eat insects lose their food, and plants that need pollinators make fewer seeds.", ["Only the insects are affected.", "The birds increase.", "More plants are pollinated."], "Organisms in an ecosystem are interdependent."),
    ("Why do some cultures leave fields to rest for a season or use crop rotation?", "to let the soil recover its minerals, which is a sustainable practice", ["to make the soil more acidic", "to kill all the decomposers", "to grow weeds"], "Sustainable practices protect ecosystems."),
    ("Corals turn white (bleach) when sea temperatures rise. What does this show?", "A change in a physical factor can affect the survival of organisms.", ["Corals prefer hot water.", "Temperature has no effect.", "Corals are plants that need more light."], "Coral bleaching is linked to global warming."),
])


def body():
    think = ("<p><b>An ecosystem is a community of organisms interacting with each other and with the physical environment.</b></p>"
             "<ul><li>Physical factors: air, water, temperature, light, minerals and pH.</li>"
             "<li>Relationships: <b>predator-prey</b>, <b>mutualism</b> (both benefit), <b>parasitism</b> (parasite benefits, host harmed), competition.</li>"
             "<li>Energy enters by <b>photosynthesis</b> and flows along food chains; only about 10% passes to the next level. Energy is lost as heat in respiration.</li>"
             "<li><b>Decomposers</b> recycle nutrients from dead matter back to the soil.</li></ul>")
    ex = [("Bees pollinate flowers and get nectar. Relationship?", ["Both benefit"], "mutualism"),
          ("Producers trap 10,000 kJ. About how much reaches the primary consumers?", ["About 10% passes on"], "1000 kJ")]
    mist = ["Saying mutualism harms one organism. In mutualism both benefit.", "Saying energy is recycled. Nutrients are recycled; energy flows and is lost as heat.",
            "Leaving out the physical environment: an ecosystem includes non-living factors.", "Thinking removing one organism affects only its predator."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Ecosystems and physical factors", B1[:1] + B1[7:8] + [(g_fact, 10), (EC.g_poll, 3), (g_rel, 4), (B1[1], 1)]),
        ("Relationships between organisms", B1[3:5] + [(g_rel, 12), (FWM[6], 3), (FWM[2], 3)]),
        ("Food chains and food webs", [(FWM[0], 4), (FWM[1], 3), (FWM[3], 5), (FWM[7], 3), (FWM[2], 3), (FWM[6], 2)]),
        ("Energy flow and decomposers", B1[2:3] + B1[5:7] + [(g_energy, 8), (EC.g_pyr, 3), (FWM[4], 3), (FWM[5], 3)]),
        ("Exam-style questions", B5 + EC.B5 + [(FWM[4], 3), (FWM[5], 3), (g_energy, 2), (g_rel, 2), (g_fact, 2)]),
    ])
    make_lss(2, "interactions-within-ecosystems", 6, "Interactions", "Interactions within Ecosystems",
             "Describe an ecosystem as a community interacting with its physical environment; explain how physical factors such as air, water, temperature, light, minerals and pH affect "
             "survival; describe predator-prey, mutualism and parasitism; describe the flow of energy through food chains and food webs, including photosynthesis and respiration, and "
             "nutrient recycling by decomposers; evaluate the impact of human activities on the environment (summary of the MOE Lower Secondary Science Syllabus).",
             "Interactions within Ecosystems", seo(2, "Ecosystems"), "Ecosystems",
             "Free Secondary 2 science worksheets for Singapore students on ecosystems: physical factors, predator-prey, mutualism and parasitism, food webs, energy flow and decomposers. With answers.",
             "Organisms interact with each other and with their environment.", "Energy flows; nutrients cycle.",
             body(),
             [("What is the difference between mutualism and parasitism?", "In mutualism both organisms benefit. In parasitism the parasite benefits and the host is harmed."),
              ("Why is energy lost along a food chain?", "Each organism uses energy for respiration and life processes, and much of it is lost as heat. Only about 10% passes on."),
              ("What do decomposers do?", "They break down dead organisms and waste and return nutrients to the soil.")],
             sets)


if __name__ == "__main__":
    main()
