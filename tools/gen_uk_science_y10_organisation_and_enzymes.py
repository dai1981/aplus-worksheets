# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Biology): Organisation and Enzymes
  python tools/gen_uk_science_y10_organisation_and_enzymes.py
Levels of organisation, the digestive system and enzymes (lock and key, optimum temperature and pH, denaturing,
amylase, protease, lipase, bile), food tests, the heart, blood vessels and blood, coronary heart disease, and plant
tissues and transpiration. Reuses the enzyme question of the Year 8 unit and the organisation questions of the US
Biology unit (new seeds).
Wrong answers come from real mistakes: "enzymes are killed by heat", "arteries carry blood to the heart",
"bile is an enzyme", "transpiration is the same as respiration".
"""
from uk_sci import item, bank, table, once
from uk_ks4 import U4, build
from sci_phys import uniq

U, R, P, us = U4(62003)
LO = "bio_levels_of_organization"
us_level, us_sys, us_order = us(LO, "g_level"), us(LO, "g_sys"), us(LO, "g_order")
y8_enz = us.uk("gen_uk_science_y8_food_and_digestion", "g_enz")


def g_rate():
    who = P.next()[0]
    opt = R.choice([30, 35, 40, 45])
    temps = [10, 20, 30, 40, 50, 60]
    peak = R.choice([20, 24, 30, 36])

    def r(t):
        if t <= opt:
            return max(1, round(peak * (t / opt) ** 1.5))
        return max(0, round(peak * (1 - (t - opt) / (62 - opt))))
    vals = [r(t) for t in temps]
    best = temps[vals.index(max(vals))]
    k = R.choice(["opt", "hot", "cold", "dep", "ctrl"])
    if not once(("ra", opt, peak, k)) or not once(("ra", k), 2 if k in ("hot", "cold", "dep", "ctrl") else 10):
        return None
    tab = table(["Temperature (°C)", "Rate (cm³ of oxygen per minute)"], [[str(t), str(v)] for t, v in zip(temps, vals)])
    intro = tab + "%s measured the rate of an enzyme reaction at different temperatures. " % who
    if k == "opt":
        g = "about %d °C" % best
        return item(intro + "What is the optimum temperature for this enzyme?", g, ["about %d °C" % t for t in temps if t != best][:3], "The highest rate.")
    if k == "hot":
        return item(intro + "Why does the rate fall at 60 °C?", "The enzyme is denatured: its active site changes shape, so the substrate no longer fits.", ["The enzyme is killed because it is alive.", "There is too much substrate.", "Particles move too slowly."], "Enzymes are proteins, not living things.")
    if k == "cold":
        return item(intro + "Why is the rate low at 10 °C?", "Particles move slowly, so there are fewer collisions between enzyme and substrate.", ["The enzyme is denatured.", "There is no substrate.", "The enzyme is dead."], "Low kinetic energy.")
    if k == "dep":
        return item(intro + "What is the dependent variable?", "the volume of oxygen per minute", ["the temperature", "the type of enzyme", "the volume of substrate"], "What is measured.")
    return item(intro + "Which variable should be kept the same?", "the pH and the concentration of the enzyme", ["the temperature", "the rate", "the time each reading is taken only"], "Control variables.")


TEST = [("starch", "iodine solution", "orange-brown to blue-black"), ("sugars (glucose)", "Benedict's solution (heated)", "blue to brick-red"),
        ("protein", "biuret reagent", "blue to purple"), ("lipids (fats)", "ethanol (emulsion test)", "a cloudy white emulsion forms")]


def g_test():
    n, r, c = R.choice(TEST)
    k = R.random() < 0.5
    if not once(("te", n, k)):
        return None
    if k:
        return item("Which reagent is used to test for %s?" % n, r, [x[1] for x in TEST if x[1] != r], "Food tests.")
    return item("What is the positive result when testing for %s with %s?" % (n, r), c, [x[2] for x in TEST if x[2] != c], "Food tests.")


HEART = [("the right ventricle", "pumps blood to the lungs"), ("the left ventricle", "pumps blood around the body, so it has the thickest wall"),
         ("the right atrium", "receives blood from the body through the vena cava"), ("the left atrium", "receives blood from the lungs through the pulmonary vein"),
         ("the valves", "stop blood flowing backwards"), ("the coronary arteries", "supply the heart muscle with oxygen"),
         ("the pacemaker", "a group of cells in the right atrium that controls the resting heart rate")]
VESSEL = [("arteries", "carry blood away from the heart under high pressure and have thick, elastic walls"), ("veins", "carry blood back to the heart and have valves"),
          ("capillaries", "have walls one cell thick so substances can diffuse in and out")]
BLOOD = [("red blood cells", "carry oxygen using haemoglobin"), ("white blood cells", "defend the body against pathogens"),
         ("platelets", "help the blood to clot"), ("plasma", "carries dissolved substances such as glucose, carbon dioxide and urea")]


def g_part():
    lst = R.choice([HEART, VESSEL, BLOOD])
    p, j = R.choice(lst)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    if k:
        return item("Which part %s?" % j, p, [x[0] for x in lst if x[0] != p][:3] if len(lst) > 3 else [x[0] for x in lst if x[0] != p] + ["the alveoli"], "Structure fits function.")
    w = [x[1] for x in lst if x[0] != p]
    w = (w if len(w) >= 3 else w + ["store fat for energy"])[:3]
    return item("What do %s do?" % p if not p.startswith("the ") else "What does %s do?" % p, j[0].upper() + j[1:] + ".", [x[0].upper() + x[1:] + "." for x in w], "Structure fits function.")


PLANT = [("xylem", "carries water and mineral ions from the roots to the leaves"), ("phloem", "carries dissolved sugars around the plant (translocation)"),
         ("guard cells", "open and close the stomata"), ("palisade mesophyll", "is where most photosynthesis happens"), ("root hair cells", "absorb water and mineral ions from the soil")]
TRANSP = [("the temperature increases", "increases"), ("the air becomes more humid", "decreases"), ("the wind speed increases", "increases"),
          ("the light intensity increases", "increases"), ("the stomata close", "decreases")]


def g_plant():
    if R.random() < 0.5:
        p, j = R.choice(PLANT)
        if not once(("pl", p)):
            return None
        return item("Which plant tissue %s?" % j, p, [x[0] for x in PLANT if x[0] != p][:3], "Plant organ systems.")
    c, a = R.choice(TRANSP)
    if not once(("tr", c)):
        return None
    return item("What happens to the rate of transpiration when %s?" % c, "It %s." % a, ["It %s." % ("decreases" if a == "increases" else "increases"), "It stays the same.", "It stops completely."], "Transpiration is evaporation of water from leaves.")


B1 = bank([
    ("What is an enzyme?", "a biological catalyst made of protein", ["a type of fat", "a living cell", "a hormone made in the liver"], "Speeds up reactions."),
    ("What is the lock and key model?", "The substrate fits into the enzyme's active site like a key in a lock.", ["Enzymes lock cells shut.", "The enzyme is used up.", "The enzyme changes into the product."], "Specific shape."),
    ("What does bile do?", "neutralises stomach acid and emulsifies fats into small droplets", ["digests protein", "is an enzyme that breaks down starch", "absorbs water"], "Made in the liver, stored in the gall bladder."),
    ("Which organ makes bile?", "the liver", ["the pancreas", "the stomach", "the gall bladder"], "Stored in the gall bladder."),
])
B5 = bank([
    ("What is coronary heart disease?", "Fatty material builds up in the coronary arteries, reducing blood flow to the heart muscle.", ["The heart grows too big.", "Valves stop closing.", "The lungs fill with fluid."], "Treated with stents or statins."),
    ("What does a stent do?", "keeps a narrowed coronary artery open", ["replaces a valve", "lowers cholesterol", "makes the heart beat"], "Treatment for CHD."),
    ("What do statins do?", "reduce cholesterol in the blood", ["open arteries with a balloon", "replace heart valves", "speed up the heart"], "Drug treatment."),
    ("Why does the left ventricle have a thicker wall than the right?", "It pumps blood all around the body at high pressure.", ["It pumps blood to the lungs only.", "It holds more blood.", "It has no valves."], "Double circulation."),
    ("What is transpiration?", "the loss of water vapour from the leaves of a plant", ["the movement of sugars in phloem", "respiration in roots", "the uptake of carbon dioxide"], "Pulls water up the xylem."),
    ("What is translocation?", "the movement of dissolved sugars through the phloem", ["water loss from leaves", "absorption of minerals", "gas exchange"], "Phloem."),
])

if __name__ == "__main__":
  build(U, 10, "organisation-and-enzymes", 3, "Biology", "Organisation",
      "Levels of organisation within a multicellular organism; the digestive system and the role of enzymes (carbohydrases, proteases, lipases) and bile, the lock and key model and the effect of temperature and pH; food tests; the heart, blood vessels and blood; coronary heart disease and its treatment; plant tissues and organs, transpiration and translocation.",
      "Organisation and Enzymes", "Organisation and Enzymes",
      "Free Year 10 GCSE Combined Science worksheets on organisation: enzymes and the lock and key model, food tests, the heart, blood vessels, blood, coronary heart disease and plant transport. 100 questions with answers.",
      "Enzymes are denatured, not killed.",
      "Each enzyme has an optimum temperature and pH; the active site fits one substrate.",
      "<p><b>Cells form tissues, tissues form organs, organs form organ systems.</b></p><ul><li>Enzymes are biological catalysts with an active site. High temperatures or the wrong pH change its shape: the enzyme is denatured.</li>"
      "<li>The heart pumps blood: arteries carry it away, veins bring it back, capillaries exchange substances.</li>"
      "<li>In plants, xylem carries water up (transpiration) and phloem carries sugars (translocation).</li></ul>",
      [("Rate highest at 37 °C. Optimum?", ["The peak"], "37 °C"), ("Test for protein?", ["Biuret: blue to purple"], "biuret reagent")],
      ["Saying enzymes are killed by heat.", "Thinking arteries carry blood to the heart.", "Thinking bile is an enzyme."],
      [("Why do enzymes stop working at high temperatures?", "The bonds holding the protein's shape break, so the active site changes shape and the substrate no longer fits. The enzyme is denatured."),
       ("What are the food tests?", "Iodine for starch (blue-black), Benedict's solution heated for sugars (brick-red), biuret for protein (purple), and the ethanol emulsion test for lipids (cloudy)."),
       ("What is the difference between arteries, veins and capillaries?", "Arteries carry blood away from the heart at high pressure; veins carry it back and have valves; capillaries are one cell thick for exchange.")],
      [("Levels of organisation", B1 + [(us_level, 6), (us_order, 4), (y8_enz, 6)]),
       ("Enzymes", [(g_rate, 12), (g_test, 6), (y8_enz, 2)]),
       ("The heart and blood", [(g_part, 16), (us_sys, 4)]),
       ("Plant tissues", [(g_plant, 8), (g_rate, 4), (us_sys, 6), (g_test, 1), (us_level, 1)]),
       ("Health and transport", B5 + [(g_part, 6), (g_plant, 1), (us_level, 5), (us_order, 2)])])
