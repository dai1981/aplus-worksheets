# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Photosynthesis (MS-LS1-6)
  python tools/gen_us_science_g7_photosynthesis.py
Construct a scientific explanation based on evidence for the role of photosynthesis in the cycling of matter
and flow of energy into and out of organisms. 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2 in chloroplasts.
Inputs: carbon dioxide (air, through stomata), water (roots), light energy. Outputs: sugar (food, stored
energy, building material), oxygen. Evidence: Elodea bubble counts vs. light, starch tests on covered leaves,
van Helmont's tree (mass comes mostly from CO2 in the air).
Wrong answers come from real mistakes: "plants get their food from the soil", "plants take in oxygen and give
off CO2 only", "the mass of a tree comes from the soil".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(70106)
R = U.R
P = People(R)

PARTS = {"carbon dioxide": ("an input", "comes from the air and enters through tiny openings in leaves (stomata)"),
         "water": ("an input", "comes from the soil through the roots"),
         "light energy": ("an input", "comes from the sun and is captured by chlorophyll"),
         "glucose (sugar)": ("an output", "stores energy and is used as food and building material"),
         "oxygen": ("an output", "is released into the air through the leaves")}


def g_io():
    x = R.choice(sorted(PARTS))
    kind, why = PARTS[x]
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s lists the parts of photosynthesis. Is %s an input or an output?" % (who, x), kind, ["an output" if kind == "an input" else "an input", "neither", "both"],
                    "%s %s." % (x[0].upper() + x[1:], why))
    w = [PARTS[y][1] for y in PARTS if y != x]
    return item("%s asks where %s fits in photosynthesis. Which is true?" % (who, x), "It " + why + ".", ["It " + y + "." for y in R.sample(w, 3)], "%s %s." % (x[0].upper() + x[1:], why))


def g_elodea():
    ds = [10, 20, 30, 40]
    b = sorted(R.sample(range(4, 40), 4), reverse=True)
    rows = [["%d cm" % d, "%d" % v] for d, v in zip(ds, b)]
    who = P.next()[0]
    tab = table(["Distance of lamp from Elodea plant", "Oxygen bubbles per minute"], rows)
    k = R.choice(["most", "pattern", "gas"])
    if k == "most":
        return item(tab + "%s counted bubbles from a water plant. At which distance was photosynthesis fastest?" % who, "10 cm", ["20 cm", "30 cm", "40 cm"],
                    "The most bubbles (%d per minute) came at 10 cm, where the light was brightest." % b[0])
    if k == "pattern":
        return item(tab + "What does %s's data show?" % who, "More light makes photosynthesis faster.", ["Less light makes photosynthesis faster.", "Light does not affect photosynthesis.", "Bubbles come from the lamp."],
                    "Closer lamp = brighter light = more oxygen bubbles.")
    return item(tab + "What gas is in the bubbles in %s's experiment?" % who, "oxygen", ["carbon dioxide", "nitrogen", "water vapor"], "Oxygen is an output of photosynthesis.")


def g_leaf():
    who = P.next()[0]
    k = R.choice(["starch", "dark", "tree"])
    if k == "starch":
        return item("%s covers half of a leaf with foil for two days, then tests the leaf for starch with iodine. Only the uncovered half turns dark blue-black. What does this show?" % who,
                    "Light is needed to make food (sugar and starch).", ["Foil makes starch.", "Leaves make food in the dark.", "Iodine makes food."], "No light, no photosynthesis.")
    if k == "dark":
        days = R.choice([5, 7, 10])
        return item("%s keeps one bean plant in a dark closet for %d days and one in a sunny window. The closet plant turns yellow and weak. Why?" % (who, days),
                    "It could not do photosynthesis, so it could not make enough food.", ["It got too much food.", "Darkness makes plants grow stronger.", "It got too much water."],
                    "Plants need light energy to make sugar.")
    g = R.choice([2, 3, 5])
    kg = R.choice([60, 70, 75, 80])
    return item("%s reads about an experiment: a tree planted in a pot gained %d kg in 5 years, but the soil lost only %d kg. Where did most of the tree's mass come from?" % (who, kg, g),
                "carbon dioxide from the air (and water) turned into sugar by photosynthesis", ["the soil", "the sunlight itself", "fertilizer only"],
                "This is like van Helmont's experiment: the carbon in a tree comes from carbon dioxide in the air.")


B1 = bank([
    ("Where in a plant cell does photosynthesis happen?", "in the chloroplasts", ["in the nucleus", "in the cell wall", "in the vacuole"], "Chloroplasts contain green chlorophyll."),
    ("What does photosynthesis make?", "glucose (sugar) and oxygen", ["carbon dioxide and water", "soil and minerals", "light and heat"], "6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂."),
    ("Do plants get their food from the soil?", "No. Plants make their own food (sugar) by photosynthesis.", ["Yes, all of it.", "Yes, through their roots.", "Only at night."],
     "Roots take in water and minerals, not food."),
    ("What does chlorophyll do?", "It captures light energy.", ["It stores water.", "It makes soil.", "It releases carbon dioxide."], "Chlorophyll is what makes leaves green."),
    ("How does energy from the sun end up in an animal that eats a plant?", "Light energy is stored in sugar made by the plant; the animal eats the plant.", ["Animals absorb sunlight through their skin.", "The sun heats the animal's food.", "It does not."],
     "Photosynthesis brings energy into food webs."),
    ("What happens to the sugar a plant makes?", "The plant uses it for energy and to build new cells, and stores some as starch.", ["It is thrown away.", "It is turned into soil.", "It all becomes oxygen."],
     "Sugar is both fuel and building material."),
    ("How does carbon dioxide get into a leaf?", "through tiny openings called stomata", ["through the roots", "through the flowers only", "through the bark"], "Stomata also let oxygen and water vapor out."),
    ("Why is photosynthesis important for animals and people?", "It makes the oxygen we breathe and the food at the base of food webs.", ["It makes rain.", "It warms the planet.", "It is not important for animals."],
     "Life depends on it."),
])
B5 = bank([
    ("Ava puts a water plant in water with a lot of dissolved carbon dioxide and another in water with very little. Which will make more oxygen bubbles?", "the one with more carbon dioxide", ["the one with less carbon dioxide", "They will be the same.", "Neither will make bubbles."],
     "CO₂ is an input; more input can speed up photosynthesis."),
    ("Leo says a tree's wood comes mostly from minerals in the soil. Which evidence argues against this?", "Trees gain much more mass than the soil loses.", ["Trees have roots.", "Trees are tall.", "Soil is brown."],
     "Most of the mass comes from CO₂ in the air."),
    ("Mia shines red light, green light and blue light on three identical plants. The plant under green light grows least. Why might that be?", "Plants reflect most green light, so they use less of it.", ["Green light has no energy.", "Green light is too bright.", "Plants cannot see green."],
     "Leaves look green because they reflect green light."),
    ("Why should Ava keep the water temperature the same in her bubble experiment?", "Temperature can also change the rate, so it must be controlled.", ["Bubbles only form in cold water.", "It does not matter.", "To change the light."],
     "Control variables for a fair test."),
    ("Which statement best explains how photosynthesis moves matter in an ecosystem?", "Carbon atoms from CO₂ in the air become part of sugar molecules in plants.", ["Plants create new atoms.", "Matter disappears in plants.", "Light turns into matter."],
     "Atoms are rearranged, not created."),
])


def body():
    think = ("<p><b>Photosynthesis</b> is how plants, algae and some bacteria make their own food in <b>chloroplasts</b>:</p>"
             "<p style='text-align:center'><b>carbon dioxide + water + light energy → glucose (sugar) + oxygen</b><br>6CO<sub>2</sub> + 6H<sub>2</sub>O → C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> + 6O<sub>2</sub></p>"
             "<p><b>Matter</b>: carbon atoms from CO<sub>2</sub> in the air become part of sugar, which builds the plant's body. <b>Energy</b>: light energy is stored in the sugar. "
             "Animals that eat plants get that matter and energy. Plants do not get their food from the soil; roots take in water and minerals.</p>")
    ex = [("Where does a tree get most of its mass?", ["Carbon comes from CO₂ in the air."], "carbon dioxide from the air"),
          ("What gas bubbles from a water plant in bright light?", ["Oxygen is an output."], "oxygen")]
    mist = ["Thinking plants get their food from the soil.",
            "Thinking a tree's mass comes mostly from the soil.",
            "Mixing up the inputs (CO₂, water, light) and the outputs (sugar, oxygen)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Inputs and outputs", B1 + [(g_io, 12)]),
        ("How photosynthesis works", [(g_io, 14), (g_leaf, 6)]),
        ("Light and photosynthesis data", [(g_elodea, 14), (g_leaf, 6)]),
        ("Evidence from experiments", [(g_leaf, 8), (g_elodea, 6), (g_io, 6)]),
        ("Matter and energy", B5 + [g_elodea, g_leaf, g_io]),
    ])
    make("grade-7", "photosynthesis", 6, "MS-LS1-6",
         "Construct a scientific explanation based on evidence for the role of photosynthesis in the cycling of matter and flow of energy into and out of organisms.",
         "Photosynthesis",
         "Grade 7 Photosynthesis Worksheets: Inputs, Outputs, Chloroplasts and Experiments",
         "Photosynthesis",
         "Free middle school science worksheets on photosynthesis (NGSS MS-LS1-6): carbon dioxide, water and light in, sugar and oxygen out, chloroplasts, and evidence from plant experiments. 100 practice questions with answers.",
         "Plants make sugar from CO₂, water and light.",
         "Photosynthesis brings matter (carbon) and energy (from sunlight) into living things and releases oxygen.",
         body(),
         [("What are the inputs and outputs of photosynthesis?", "Inputs: carbon dioxide, water and light energy. Outputs: glucose (sugar) and oxygen."),
          ("Where does a plant's mass come from?", "Mostly from carbon dioxide in the air, which photosynthesis turns into sugar and then into plant material."),
          ("Why is photosynthesis important?", "It makes the food at the base of food webs and the oxygen that animals breathe.")],
         sets)


if __name__ == "__main__":
    main()
