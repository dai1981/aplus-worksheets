# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Chemistry): Chemistry of the Atmosphere
  python tools/gen_uk_science_y11_chemistry_of_the_atmosphere.py
The proportions of gases in the atmosphere, how the atmosphere evolved (volcanoes, oceans, photosynthesis, sedimentary
rocks and fossil fuels), greenhouse gases and human activities, global climate change and its evidence, the carbon
footprint and ways to reduce it, and atmospheric pollutants from fuels (carbon monoxide, sulfur dioxide, oxides of
nitrogen, particulates). Reuses the US Earth and Space climate questions in British English.
Wrong answers come from real mistakes: "air is mostly oxygen", "nitrogen is a greenhouse gas", "carbon monoxide
causes acid rain", "the early atmosphere had lots of oxygen".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62108)
CE, CC = "ess_coevolution_of_life_and_earth", "ess_climate_change_data_and_models"
us_oxy = us(CE, "g_oxy")
us_imp = us(CC, "g_imp", drop=("U.S.", "Alaska", "western"))
us_rate, us_fc, us_sea, us_scen = us(CC, "g_rate", drop=("U.S.",)), us(CC, "g_fc"), us(CC, "g_sea"), us(CC, "g_scen")

COMP = [("nitrogen", "about 80% (four-fifths)"), ("oxygen", "about 20% (one-fifth)"), ("carbon dioxide", "about 0.04%"), ("argon", "just under 1%")]


def g_comp():
    g, p = R.choice(COMP)
    k = R.choice(["pct", "gas"])
    if not once(("cp", g, k)):
        return None
    if k == "pct":
        return item("About how much of the air today is %s?" % g, p, [x[1] for x in COMP if x[0] != g], "Nitrogen ~80%, oxygen ~20%, small amounts of argon, carbon dioxide and water vapour.")
    return item("Which gas makes up %s of the air today?" % p, g, [x[0] for x in COMP if x[0] != g], "Nitrogen ~80%, oxygen ~20%.")


EVO = ["Volcanoes released carbon dioxide, water vapour and nitrogen.", "Water vapour condensed to form the oceans.",
       "Algae and plants began to produce oxygen by photosynthesis.", "Carbon became locked in sedimentary rocks and fossil fuels."]


def g_evo():
    i, j = sorted(R.sample(range(4), 2))
    a, b = (EVO[i], EVO[j]) if R.random() < 0.5 else (EVO[j], EVO[i])
    if not once(("ev", a, b)):
        return None
    return item("Which happened first in the evolution of Earth's atmosphere? A: %s B: %s" % (a, b), "A" if a == EVO[i] else "B",
                ["B" if a == EVO[i] else "A", "They happened at the same time.", "Neither has happened."], "Volcanoes → oceans → oxygen from algae and plants → carbon locked away.")


GHG = [("carbon dioxide", True), ("methane", True), ("water vapour", True), ("nitrogen", False), ("oxygen", False), ("argon", False)]
SRC = [("cattle farming", "methane"), ("rice paddy fields", "methane"), ("landfill sites", "methane"), ("burning fossil fuels", "carbon dioxide"),
       ("deforestation", "carbon dioxide"), ("burning wood", "carbon dioxide")]


def g_ghg():
    k = R.choice(["is", "is", "src"])
    if k == "is":
        g, y = R.choice(GHG)
        if not once(("gh", g)):
            return None
        return item("Is %s a greenhouse gas?" % g, "Yes" if y else "No", ["No" if y else "Yes", "Only at night", "Only in summer"],
                    "Carbon dioxide, methane and water vapour are greenhouse gases; nitrogen and oxygen are not.")
    s, g = R.choice(SRC)
    if not once(("gs", s)):
        return None
    return item("Which greenhouse gas is mainly increased by %s?" % s, g, [x for x in ["methane", "carbon dioxide", "nitrogen", "oxygen"] if x != g],
                "Methane: cattle, rice, landfill. Carbon dioxide: burning fuels, deforestation.")


FOOT = [("drives a petrol car", 0.17, "km", [20, 30, 40, 50, 60, 80, 120, 150, 200]), ("uses electricity", 0.2, "kWh", [5, 10, 15, 20, 25, 30, 40, 60, 80]),
        ("takes a bus", 0.1, "km", [10, 20, 30, 40, 50, 60, 70, 80])]


def g_foot():
    act, f, u, xs = R.choice(FOOT)
    x = R.choice(xs)
    k = R.choice(["calc", "calc", "save"])
    name = P.next()[0]
    if not once(("ft", act, x, k)):
        return None
    v = round(f * x, 2)
    if k == "calc":
        return item("Each %s releases about %g kg of carbon dioxide. %s %s for %d %s. How much carbon dioxide is that?" % (u, f, name, act, x, u), "%g kg" % v,
                    [x2 for x2 in ["%g kg" % round(x / f, 1), "%g kg" % round(f + x, 2), "%g kg" % round(v * 10, 1), "%g kg" % round(v / 10, 3)] if x2 != "%g kg" % v][:3],
                    "%g × %d = %g kg." % (f, x, v))
    if act != "drives a petrol car":
        return None
    b = round(0.1 * x, 2)
    return item("A petrol car releases 0.17 kg of carbon dioxide per km and a bus about 0.1 kg per passenger per km. %s takes the bus for a %d km journey instead of driving. How much carbon dioxide is saved?" % (name, x),
                "%g kg" % round(v - b, 2), ["%g kg" % v, "%g kg" % b, "%g kg" % round(v + b, 2)], "%g − %g = %g kg." % (v, b, round(v - b, 2)))


POL = [("carbon monoxide", "incomplete combustion of fuels", "It is toxic: it stops blood carrying oxygen."),
       ("sulfur dioxide", "sulfur impurities in fuels burning", "It forms sulfuric acid in rain, which damages buildings and plants."),
       ("oxides of nitrogen", "nitrogen and oxygen reacting at the high temperatures in engines", "They react in sunlight to make smog, which worsens asthma."),
       ("particulates (soot)", "incomplete combustion of fuels", "They cause global dimming and damage the lungs.")]


def g_poll():
    g, src, eff = R.choice(POL)
    k = R.choice(["src", "eff", "which"])
    if not once(("pl", g, k)):
        return None
    if k == "src":
        return item("How %s %s produced?" % ("are" if g.startswith(("oxides", "particulates")) else "is", g), src, list(dict.fromkeys([x[1] for x in POL if x[1] != src]))[:2] + ["photosynthesis in plants"], "Burning fuels releases these pollutants.")
    if k == "eff":
        return item("What is a harmful effect of %s?" % g, eff, [x[2] for x in POL if x[0] != g], "Learn the effect of each pollutant.")
    return item("Which pollutant is this? “%s”" % eff, g, [x[0] for x in POL if x[0] != g], "Learn the effect of each pollutant.")


B1 = bank([
    ("What were the main gases in Earth's early atmosphere?", "carbon dioxide with water vapour and some nitrogen", ["mostly oxygen", "mostly argon", "mostly hydrogen and helium only"], "Released by volcanoes; there was little or no oxygen."),
    ("How did the amount of carbon dioxide in the early atmosphere decrease?", "It dissolved in the oceans, was used in photosynthesis and became locked in rocks and fossil fuels.", ["Volcanoes absorbed it.", "It turned into nitrogen.", "It escaped into space."], "Limestone, coal, oil and gas."),
    ("Where did the oxygen in the atmosphere come from?", "photosynthesis by algae and plants", ["volcanoes", "the oceans boiling", "meteorites"], "About 2.7 billion years ago algae started producing oxygen."),
    ("Why is there uncertainty about Earth's early atmosphere?", "It formed billions of years ago, so there is little evidence.", ["Nobody has studied it.", "It was the same as today.", "Scientists agree on every detail."], "Theories change with new evidence."),
])
B2 = bank([
    ("How do greenhouse gases keep Earth warm?", "They absorb long-wavelength radiation given off by the Earth.", ["They reflect all sunlight.", "They make the Sun hotter.", "They block all short-wavelength radiation."], "This keeps the temperature high enough for life."),
    ("Which human activity increases carbon dioxide in the air?", "burning fossil fuels", ["planting trees", "using wind turbines", "recycling paper"], "Also deforestation."),
    ("Why is the evidence for climate change sometimes simplified in the media?", "The climate is complex, so it is hard to model fully.", ["Scientists hide data.", "There is no evidence.", "Weather never changes."], "Peer-reviewed evidence shows human activities cause warming."),
    ("Give one effect of global climate change.", "sea level rising", ["more ozone in the air", "more oxygen in the air", "colder summers everywhere"], "Also more extreme weather and changes to food production."),
    ("Which statement is about weather rather than climate?", "It rained heavily in Leeds yesterday.", ["Average UK temperatures have risen since 1900.", "Arctic ice has shrunk over 40 years.", "Global sea level is rising."], "Climate is the long-term average."),
])
B4 = bank([
    ("What is a carbon footprint?", "the total amount of carbon dioxide and other greenhouse gases released over the life of a product, service or event", ["the mark left by a coal fire", "the mass of carbon in a person", "the area of a forest"], "Measured in kg or tonnes of CO₂."),
    ("Give one way to reduce a carbon footprint.", "using renewable energy such as wind or solar power", ["burning more coal", "driving more", "cutting down forests"], "Also energy saving and carbon capture."),
    ("What is carbon capture and storage?", "trapping carbon dioxide from power stations and storing it underground", ["burning carbon faster", "turning carbon into oxygen", "storing coal in warehouses"], "Reduces emissions."),
])
B5 = bank([
    ("Why does incomplete combustion happen?", "There is not enough oxygen.", ["There is too much oxygen.", "The fuel is too cold.", "The fuel has no carbon."], "Makes carbon monoxide and soot."),
    ("Why is carbon monoxide hard to detect?", "It is colourless and odourless.", ["It is bright yellow.", "It smells strongly.", "It is a solid."], "Homes use carbon monoxide alarms."),
    ("How can sulfur dioxide emissions be reduced?", "removing sulfur from fuels before they are burned", ["adding more sulfur", "burning fuel at lower temperatures only", "using more coal"], "Also scrubbing waste gases."),
    ("How do catalytic converters help?", "They change carbon monoxide and oxides of nitrogen into less harmful gases.", ["They add more carbon monoxide.", "They burn sulfur.", "They make particulates."], "Fitted to car exhausts."),
])

if __name__ == "__main__":
  build(U, 11, "chemistry-of-the-atmosphere", 8, "Chemistry", "Chemistry of the atmosphere",
      "The proportions of different gases in the atmosphere; the Earth's early atmosphere and how it evolved; how oxygen increased and carbon dioxide decreased; greenhouse gases and human activities; global climate change; the carbon footprint and its reduction; atmospheric pollutants from fuels and their properties and effects.",
      "Chemistry of the Atmosphere", "Chemistry of the Atmosphere",
      "Free Year 11 GCSE Combined Science worksheets on the atmosphere: the gases in air, the early atmosphere, greenhouse gases, climate change, carbon footprints and air pollutants. 100 questions with answers.",
      "Air is about four-fifths nitrogen and one-fifth oxygen.",
      "Greenhouse gases absorb heat radiated by the Earth.",
      "<p><b>Earth's atmosphere has changed over billions of years.</b></p><ul><li>The early atmosphere was mainly carbon dioxide from volcanoes. Algae and plants added oxygen.</li>"
      "<li>Carbon dioxide, methane and water vapour are greenhouse gases. Burning fuels and farming increase them.</li>"
      "<li>Pollutants: carbon monoxide (toxic), sulfur dioxide and oxides of nitrogen (acid rain), particulates (global dimming).</li></ul>",
      [("0.17 kg CO₂ per km, 50 km?", ["0.17 × 50"], "8.5 kg"), ("Which gas is about 80% of air?", ["Four-fifths"], "nitrogen")],
      ["Thinking air is mostly oxygen.", "Thinking nitrogen is a greenhouse gas.", "Thinking carbon monoxide causes acid rain."],
      [("How did the early atmosphere change?", "Volcanoes released carbon dioxide and water vapour. The water formed oceans. Algae and plants made oxygen, and carbon dioxide was locked in rocks and fossil fuels."),
       ("Which gases are greenhouse gases?", "Carbon dioxide, methane and water vapour. They absorb long-wavelength radiation from the Earth and keep it warm."),
       ("Which pollutants come from burning fuels?", "Carbon dioxide, carbon monoxide, soot (particulates), sulfur dioxide and oxides of nitrogen.")],
      [("The early atmosphere", B1 + [(g_evo, 6), (us_oxy, 5), (g_comp, 3), (us_fc, 2)]),
       ("Greenhouse gases", B2 + [(g_ghg, 9), (g_comp, 3), (us_sea, 3)]),
       ("Climate change", [(us_imp, 4), (us_rate, 5), (us_fc, 6), (us_scen, 5)]),
       ("Carbon footprint", B4 + [(g_foot, 14), (us_sea, 3)]),
       ("Air pollutants", B5 + [(g_poll, 9), (g_foot, 7)])])
