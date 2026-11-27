# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Diversity): Exploring Diversity of Matter using Separation Techniques
  python tools/gen_sg_science_s1_separation_techniques.py
Magnetic attraction, filtration, evaporation, distillation and paper chromatography, the principles behind them, and their uses
in water treatment (filtration, distillation, reverse osmosis), food safety and waste management; Singapore's water supply
(the Four National Taps: local catchment, imported water, NEWater and desalinated water).
UK KS3 mixtures makers are reused for methods, words and chromatograms.
Wrong answers come from real mistakes: "filtration removes dissolved salt", "distillation collects the solid",
"the residue passes through the filter paper", "the start line is drawn in ink".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64104)
R = U.R
P = People(R)
MX = luse(U, "gen_uk_science_y7_mixtures_and_separation", drop=[r"crystallisation", r"fractional"])

MIX = [("sand and water", "filtration", "Sand is insoluble, so it stays on the filter paper."),
       ("chalk powder and water", "filtration", "Chalk is insoluble."),
       ("salt from salt solution", "evaporation", "The water evaporates and leaves the salt behind."),
       ("sugar from sugar solution", "evaporation", "Heat gently: the solvent evaporates and the solute remains."),
       ("pure water from sea water", "distillation", "Water boils, turns into vapour and is condensed back into a liquid."),
       ("pure water from ink", "distillation", "The water is collected as the distillate."),
       ("the dyes in a black marker ink", "paper chromatography", "The dyes move different distances up the paper."),
       ("the colourings in a sweet", "paper chromatography", "Each colouring travels at its own rate."),
       ("iron filings and sand", "magnetic attraction", "Iron is magnetic; sand is not."),
       ("steel cans and aluminium cans at a recycling plant", "magnetic attraction", "Steel is attracted to a magnet; aluminium is not."),
       ("tea leaves and tea", "filtration", "The tea leaves are the residue."),
       ("pure water from orange juice", "distillation", "Only the water boils off and is condensed.")]
METHODS = ["filtration", "evaporation", "distillation", "paper chromatography", "magnetic attraction"]


def g_meth():
    m, a, e = R.choice(MIX)
    if not once(("me", m)):
        return None
    return item("Which method is best for separating %s?" % m, a, R.sample([x for x in METHODS if x != a], 3), e)


PRIN = [("filtration", "Insoluble solid particles are too big to pass through the tiny holes in the filter paper."),
        ("evaporation", "The solvent changes into a gas and escapes, leaving the dissolved solid behind."),
        ("distillation", "The liquid with the lower boiling point boils first, and its vapour is cooled and condensed."),
        ("paper chromatography", "Different dyes have different solubilities in the solvent, so they travel different distances."),
        ("magnetic attraction", "Only magnetic materials such as iron, steel, nickel and cobalt are attracted to a magnet.")]


def g_prin():
    m, p = R.choice(PRIN)
    k = R.choice(["m", "p"])
    if not once(("pr", m, k)):
        return None
    if k == "m":
        return item("Which separation technique works on this principle? %s" % p, m, R.sample([x[0] for x in PRIN if x[0] != m], 3), "This is how %s works." % m)
    return item("What is the principle behind %s?" % m, p, R.sample([x[1] for x in PRIN if x[0] != m], 3), "This is how %s works." % m)


DIST = [("the condenser", "cools the vapour so that it condenses into a liquid"), ("the thermometer", "measures the temperature of the vapour"),
        ("the distillate", "is the pure liquid collected in the receiver"), ("boiling chips", "make the liquid boil smoothly"),
        ("the cold water in the condenser", "flows in at the bottom and out at the top so that the condenser stays full and cold"),
        ("the residue", "is what is left behind on the filter paper in filtration")]


def g_dist():
    p, j = R.choice(DIST)
    if not once(("ds", p)):
        return None
    return item("In a separation experiment, which statement about %s is correct?" % p, "It %s." % j, ["It %s." % x[1] for x in R.sample([x for x in DIST if x[0] != p], 3)],
                "%s %s." % (p[0].upper() + p[1:], j))


B1 = bank([
    ("What are the Four National Taps of Singapore?", "local catchment water, imported water, NEWater and desalinated water", ["rain, rivers, lakes and the sea", "tap water, bottled water, ice and steam", "only reservoirs"], "Having four sources keeps the water supply secure."),
    ("How is NEWater made from used water?", "by microfiltration, reverse osmosis and ultraviolet disinfection", ["by adding salt", "by boiling it only", "by mixing it with sea water"], "NEWater is very clean and is used mostly by industries."),
    ("What does desalination remove from sea water?", "dissolved salts", ["only sand", "only fish", "only oil"], "Singapore uses reverse osmosis to desalinate sea water."),
    ("Why can filtration not remove dissolved salt from sea water?", "Dissolved salt particles are small enough to pass through filter paper.", ["Salt is a liquid.", "Filter paper dissolves in sea water.", "Salt is magnetic."], "Distillation or reverse osmosis is needed."),
    ("In reverse osmosis, what is pushed through a partially permeable membrane?", "water molecules, leaving dissolved salts and impurities behind", ["salt, leaving the water behind", "sand only", "bacteria only"], "High pressure forces water through."),
    ("What is the filtrate?", "the liquid that passes through the filter paper", ["the solid left on the filter paper", "the vapour in a condenser", "the dye on a chromatogram"], "The solid left behind is the residue."),
    ("How can chromatography help to keep food safe?", "It can show whether a food contains a banned colouring.", ["It cooks the food.", "It removes all bacteria.", "It makes the food sweeter."], "The spots are compared with known dyes."),
    ("Why is it important to use water wisely in Singapore?", "Singapore has limited land to collect and store rainwater.", ["Singapore has no rain.", "Water is free to make.", "All water comes from the sea."], "Saving water makes our water supply sustainable."),
])
B5 = bank([
    ("How can you get pure dry salt from a mixture of salt and sand?", "Add water and stir, filter, then evaporate the filtrate.", ["Filter the dry mixture.", "Use a magnet.", "Distil the dry mixture."], "Salt dissolves; sand does not."),
    ("In a chromatogram, a food colouring gives two spots. What does this show?", "It is a mixture of two dyes.", ["It is a pure substance.", "It is a compound.", "It has no dyes."], "A pure dye gives only one spot."),
    ("Why must the solvent level be below the start line in paper chromatography?", "So that the dyes do not dissolve straight into the solvent in the beaker.", ["So that the paper does not get wet.", "So that the dyes move faster.", "It does not matter."], "The solvent must carry the dyes up the paper."),
    ("Ethanol boils at 78 °C and water at 100 °C. A mixture of the two is heated. Which liquid is collected first?", "ethanol", ["water", "both at the same time", "neither"], "The liquid with the lower boiling point boils off first."),
    ("A recycling plant uses a large magnet on a moving belt. What does it remove?", "steel cans", ["aluminium cans", "glass bottles", "paper"], "Steel contains iron, which is magnetic."),
    ("A student heats copper(II) sulfate solution until it is dry. Why might she stop before it is completely dry?", "To get crystals instead of a powder that may decompose with too much heat.", ["To make it a liquid again.", "To make it magnetic.", "To get more water."], "Heat gently and let crystals form as it cools."),
])


def body():
    think = ("<p><b>Mixtures can be separated because their parts have different physical properties.</b></p>"
             "<ul><li><b>Magnetic attraction</b>: magnetic from non-magnetic. <b>Filtration</b>: insoluble solid from a liquid.</li>"
             "<li><b>Evaporation</b>: a dissolved solid from its solvent. <b>Distillation</b>: a pure liquid from a solution, by boiling and condensing.</li>"
             "<li><b>Paper chromatography</b>: the dyes in a mixture, because they travel different distances.</li>"
             "<li>Singapore's water: local catchment, imported water, <b>NEWater</b> and <b>desalinated</b> water (reverse osmosis).</li></ul>")
    ex = [("How do you separate sand from water?", ["Sand is insoluble"], "filtration"), ("How do you get pure water from sea water?", ["Boil and condense the water"], "distillation")]
    mist = ["Using filtration to remove dissolved salt. Salt passes through filter paper.", "Thinking distillation collects the solid. It collects the pure liquid.",
            "Mixing up residue (stays on the paper) and filtrate (passes through).", "Drawing the start line in ink. Use pencil; ink dissolves in the solvent."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Choosing a method", [(g_meth, 10), (MX.g_method, 6)] + MX.B1[:4]),
        ("How the methods work", [(g_prin, 10), (g_dist, 6), (MX.g_voc, 4)]),
        ("Chromatography", [(MX.g_chrom, 10), (MX.g_voc, 4), (g_prin, 4), (g_meth, 2)]),
        ("Water treatment in Singapore", B1 + [(MX.g_mass, 4), (g_dist, 4), (MX.g_method, 4)]),
        ("Exam-style questions", B5 + MX.B5 + [(MX.g_chrom, 4), (g_meth, 2), (MX.g_method, 3)]),
    ])
    make_lss(1, "separation-techniques", 4, "Diversity", "Exploring Diversity of Matter using Separation Techniques",
             "Explain how magnetic attraction, filtration, evaporation, distillation and paper chromatography separate the parts of a mixture and investigate the principles behind them; "
             "describe their uses in water treatment (filtration, distillation, reverse osmosis), food safety and waste management, and appreciate Singapore's sustainable supply of "
             "potable water (summary of the MOE Lower Secondary Science Syllabus).",
             "Separation Techniques", seo(1, "Separation Techniques"), "Separation techniques",
             "Free Secondary 1 science worksheets for Singapore students on separation techniques: filtration, evaporation, distillation, chromatography, magnets, NEWater and desalination. With answers.",
             "Separate mixtures by their different properties.", "Insoluble solid: filter. Dissolved solid: evaporate. Pure liquid: distil.",
             body(),
             [("Which method separates salt from salt water?", "Evaporation, to keep the salt; distillation, to collect the pure water."),
              ("How does paper chromatography work?", "The dyes dissolve in the solvent and travel different distances up the paper, so they separate into spots."),
              ("What is NEWater?", "High-grade reclaimed water made from used water by microfiltration, reverse osmosis and ultraviolet disinfection.")],
             sets)


if __name__ == "__main__":
    main()
