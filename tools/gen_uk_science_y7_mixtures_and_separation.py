# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Chemistry): Mixtures and Separation
  python tools/gen_uk_science_y7_mixtures_and_separation.py
Pure and impure substances; mixtures, including dissolving (solute, solvent, solution, soluble, insoluble, saturated);
simple techniques for separating mixtures: filtration, evaporation, distillation and chromatography; conservation of
mass when dissolving; and identifying pure substances by their sharp melting points.
Wrong answers come from real mistakes: "salt disappears when it dissolves", "filtering salt water removes the salt",
"pure means natural", "the solvent is the solid that dissolves".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61709)
R = U.R
P = People(R)

METHOD = [("sand from water", "filtration"), ("chalk from water", "filtration"), ("salt from salt water", "evaporation (crystallisation)"),
          ("copper sulfate crystals from copper sulfate solution", "evaporation (crystallisation)"), ("pure water from sea water", "distillation"),
          ("ethanol from a mixture of ethanol and water", "distillation"), ("the different dyes in a black ink", "chromatography"), ("the colours in a food colouring", "chromatography"),
          ("iron filings from sulfur powder", "using a magnet"), ("tea leaves from tea", "filtration")]
METH = ["filtration", "evaporation (crystallisation)", "distillation", "chromatography", "using a magnet"]


def g_method():
    m, a = R.choice(METHOD)
    k = R.random() < 0.6
    if not once(("me", m, k)):
        return None
    if k:
        return item("Which method would you use to separate %s?" % m, a, R.sample([x for x in METH if x != a], 3), "Choose the method from the properties of the substances.")
    return item("Which of these could be separated by %s?" % a, m, R.sample([x[0] for x in METHOD if x[1] != a], 3), "Choose the method from the properties of the substances.")


VOC = [("solute", "the substance that dissolves"), ("solvent", "the liquid that the solute dissolves in"), ("solution", "a mixture of a solute dissolved in a solvent"),
       ("soluble", "able to dissolve"), ("insoluble", "not able to dissolve"), ("filtrate", "the liquid that passes through the filter paper"),
       ("residue", "the solid left in the filter paper"), ("saturated solution", "a solution in which no more solute can dissolve")]


def g_voc():
    w, d = R.choice(VOC)
    k = R.random() < 0.5
    if not once(("vo", w, k)):
        return None
    if k:
        return item("What does '%s' mean?" % w, d, R.sample([x[1] for x in VOC if x[1] != d], 3), "Learn the key words of dissolving and filtering.")
    return item("Which word means %s?" % d, w, R.sample([x[0] for x in VOC if x[0] != w], 3), "Learn the key words of dissolving and filtering.")


def g_mass():
    s = R.choice([2, 5, 8, 10, 12, 15, 20, 25, 30])
    w = R.choice([50, 80, 100, 120, 150, 200, 250])
    what = R.choice(["salt", "sugar", "copper sulfate"])
    if not once(("ma", s, w)):
        return None
    t = s + w
    g = "%d g" % t
    return item("%d g of %s dissolves completely in %d g of water. What is the mass of the solution?" % (s, what, w), g, uniq(g, ["%d g" % w, "%d g" % (w - s), "%d g" % s, "%d g" % (t + 10)]),
                "Mass is conserved: %d + %d = %d g. The solute is still there, just spread out." % (s, w, t))


INKS = ["A", "B", "C", "D"]


def g_chrom():
    who = P.next()[0]
    pool = [2, 3, 4, 5, 6, 7, 8]
    inks = {i: sorted(R.sample(pool, R.randint(1, 3))) for i in INKS}
    if len({tuple(v) for v in inks.values()}) < 4:
        return None
    match = R.choice(INKS)
    k = R.choice(["match", "most", "pure", "count"])
    if not once(("cr", tuple(tuple(inks[i]) for i in INKS), k)):
        return None
    tab = table(["Sample", "Heights of the coloured spots (cm)"], [["ink " + i, ", ".join(str(x) for x in inks[i])] for i in INKS] + [["ink from the note", ", ".join(str(x) for x in inks[match])]])
    intro = tab + "%s ran a chromatogram of four pens and the ink on a mystery note. " % who
    if k == "match":
        return item(intro + "Which pen wrote the note?", "ink " + match, ["ink " + i for i in INKS if i != match], "Its spots are at exactly the same heights.")
    if k == "most":
        n = {i: len(inks[i]) for i in INKS}
        m = max(n.values())
        top = [i for i in INKS if n[i] == m]
        if len(top) > 1:
            return None
        return item(intro + "Which pen's ink contains the most dyes?", "ink " + top[0], ["ink " + i for i in INKS if i != top[0]], "Count the spots.")
    if k == "pure":
        one = [i for i in INKS if len(inks[i]) == 1]
        if len(one) != 1:
            return None
        return item(intro + "Which ink could be a single pure dye?", "ink " + one[0], ["ink " + i for i in INKS if i != one[0]], "A pure substance gives one spot.")
    i = R.choice(INKS)
    g = str(len(inks[i]))
    return item(intro + "How many different dyes are in ink %s?" % i, g, [str(x) for x in range(1, 6) if x != len(inks[i])][:3], "Each spot is a different dye.")


def g_pure():
    who = P.next()[0]
    rows = [("sample 1", "melts at exactly 0 °C"), ("sample 2", "melts between −3 °C and −1 °C"), ("sample 3", "melts between −6 °C and −2 °C")]
    R.shuffle(rows)
    k = R.choice(["pure", "impure", "why"])
    if not once(("pu", tuple(r[0] for r in rows), k)):
        return None
    tab = table(["Sample of 'water'", "Melting point"], [list(r) for r in rows])
    intro = tab + "%s tested three samples that were all sold as water. " % who
    pure = [r[0] for r in rows if "exactly" in r[1]][0]
    if k == "pure":
        return item(intro + "Which sample is pure water?", pure, [r[0] for r in rows if r[0] != pure] + ["none of them"], "A pure substance melts at one sharp temperature.")
    if k == "impure":
        worst = [r[0] for r in rows if "−6" in r[1]][0]
        return item(intro + "Which sample is the most impure?", worst, [r[0] for r in rows if r[0] != worst] + ["they are all equally pure"], "Impurities lower the melting point and make it melt over a range.")
    return item(intro + "How can you tell a substance is pure?", "It melts and boils at fixed, sharp temperatures.", ["It looks clear.", "It is natural.", "It has a nice smell."], "Pure means only one substance.")


B1 = bank([
    ("What is a pure substance in science?", "a single element or compound with nothing else mixed in", ["anything natural", "anything clean", "a mixture of elements"], "Pure orange juice is not pure in science."),
    ("What is a mixture?", "two or more substances that are not chemically joined", ["one element only", "a compound", "a single atom"], "They can be separated."),
    ("What happens to salt when it dissolves in water?", "It breaks into tiny particles that spread between the water particles.", ["It disappears completely.", "It turns into water.", "It becomes a gas."], "It is still there."),
    ("Why does filtering not remove salt from salt water?", "The dissolved salt particles are small enough to pass through the filter paper.", ["Salt is a liquid.", "Filter paper is magnetic.", "Salt sticks to the funnel."], "Filtration removes insoluble solids."),
    ("Which method separates an insoluble solid from a liquid?", "filtration", ["distillation", "chromatography", "evaporation"], "Sand from water."),
    ("What does distillation use to separate liquids?", "their different boiling points", ["their colours", "their magnetism", "their sizes"], "Boil, then condense."),
    ("What is the part of distillation apparatus that cools the gas back into a liquid?", "the condenser", ["the filter", "the beaker of sand", "the chromatography paper"], "Cold water flows around it."),
    ("Why can more sugar dissolve in hot tea than in cold tea?", "Solubility usually increases as temperature rises.", ["Hot tea has less water.", "Sugar melts in hot tea.", "Cold tea has no solvent."], "Temperature and solubility."),
])
B5 = bank([
    ("How would you get pure, dry salt from rock salt (salt mixed with sand and grit)?", "Dissolve in water, filter, then evaporate the filtrate.", ["Filter it dry.", "Use a magnet.", "Boil the rock salt."], "Three steps."),
    ("Why is the start line of a chromatogram drawn in pencil, not ink?", "Pencil does not dissolve and run up the paper.", ["Pencil is cheaper.", "Ink is invisible.", "Pencil makes the dyes move."], "Avoid extra spots."),
    ("Why is the start line kept above the level of the solvent?", "so the ink does not just dissolve into the solvent in the beaker", ["so it dries faster", "so the paper does not tear", "it does not matter"], "Careful method."),
    ("Why is distilled water used in car batteries and steam irons?", "It is pure, with no dissolved solids to leave deposits.", ["It is magnetic.", "It is cheaper than air.", "It contains extra salt."], "Uses of pure substances."),
    ("A sample of 'pure' gold melts over a range of temperatures. What does this suggest?", "It contains impurities.", ["It is extra pure.", "It is not a metal.", "It is a gas."], "Sharp melting point means pure."),
])


def body():
    think = ("<p><b>Mixtures can be separated because their substances have different properties.</b></p>"
             "<ul><li>Filtration: insoluble solid from a liquid. Evaporation: dissolved solid from a solution. Distillation: a liquid from a solution or two liquids.</li>"
             "<li>Chromatography separates dyes. A pure substance gives one spot and has a sharp melting point.</li>"
             "<li>When a solute dissolves in a solvent, mass is conserved.</li></ul>")
    ex = [("Sand and water?", ["Sand is insoluble"], "filtration"),
          ("10 g salt + 100 g water. Mass of solution?", ["Mass is conserved"], "110 g")]
    mist = ["Thinking salt disappears when it dissolves.", "Thinking filtering salt water removes the salt.", "Thinking pure means natural."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Pure substances and mixtures", B1 + [(g_voc, 12)]),
        ("Separation methods", [(g_method, 16), (g_voc, 4)]),
        ("Dissolving", [(g_mass, 12), (g_pure, 6), (g_method, 2)]),
        ("Chromatography", [(g_chrom, 20)]),
        ("Thinking about mixtures", B5 + [(g_chrom, 8), (g_mass, 7)]),
    ])
    make_ks3(7, "mixtures-and-separation", 9, "Chemistry", "Pure and impure substances",
             "The concept of a pure substance; mixtures, including dissolving; diffusion in terms of the particle model; simple techniques for separating mixtures: filtration, evaporation, distillation and chromatography; the identification of pure substances.",
             "Mixtures and Separation",
             "Year 7 Science: Mixtures and Separation Worksheets (Filtration, Distillation, Chromatography)",
             "Mixtures and Separation",
             "Free Year 7 science worksheets on mixtures and separation: pure substances, dissolving, filtration, evaporation, distillation, chromatography and melting points. 100 questions with answers.",
             "Different properties let us separate mixtures.",
             "Filtration, evaporation, distillation and chromatography.",
             body(),
             [("What is a pure substance?", "In science, a pure substance is a single element or compound with nothing else mixed in. It melts and boils at fixed temperatures."),
              ("How do you get salt from salt water?", "Evaporate the water: heat the solution gently so the water evaporates and salt crystals are left."),
              ("What does chromatography show?", "It separates the dyes in a mixture such as ink. Each dye makes a separate spot, and inks can be matched by their spots.")],
             sets)


if __name__ == "__main__":
    main()
