# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U06: pure substances and mixtures, solutions, and separation techniques
(filtration, evaporation, crystallisation, distillation, chromatography, magnetism, decanting) and their uses in Australian
industries (water treatment, desalination, salt ponds, gold panning, sugar cane refining).
  python tools/gen_au_science_y7_mixtures_and_separation.py
Reuses the UK Year 7 mixtures makers and the SG Secondary 1 separation makers with Australian names.
Wrong answers come from real mistakes: thinking filtration removes dissolved salt, thinking a dissolved solute has disappeared,
and calling tap water or air a pure substance.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

M7 = "gen_uk_science_y7_mixtures_and_separation"
S1 = "gen_sg_science_s1_separation_techniques"
m_chrom = limit(src(M7, "g_chrom"), 3)
m_mass = limit(src(M7, "g_mass"), 3)
m_method = src(M7, "g_method")
m_pure = src(M7, "g_pure")
m_voc = src(M7, "g_voc")
m_b1 = src.B(M7, "B1")
m_b5 = src.B(M7, "B5")
s_dist = src(S1, "g_dist", rep=[(r"It make the liquid", "They make the liquid")])
s_meth = src(S1, "g_meth")
s_prin = src(S1, "g_prin")
s_b1 = src.B(S1, "B1", drop=["NEWater"])
s_b5 = src.B(S1, "B5")

IND = [("Perth's desalination plants make drinking water from sea water.", "reverse osmosis (pushing water through a very fine filter) or distillation"),
       ("Salt is collected from shallow ponds near Lake MacDonnell in South Australia.", "evaporation"),
       ("Prospectors in the goldfields swirl gravel in a pan to find gold.", "separating by density (heavier gold sinks)"),
       ("Raw sugar crystals are made from cane juice in Queensland mills.", "evaporation and crystallisation"),
       ("Town water passes through layers of sand and gravel at a treatment plant.", "filtration"),
       ("Iron ore is separated from crushed rock in the Pilbara.", "magnetic separation and separating by density"),
       ("Police test the ink on a forged note.", "chromatography"),
       ("Grain is cleaned of dust by blowing air through it on a farm.", "winnowing (separating by mass with moving air)")]


def g_ind():
    st, m = R.choice(IND)
    w = sorted({x[1] for x in IND if x[1] != m})
    return tq("%s Which separation method is mainly used?" % st, m, R.sample(w, 3), "Choose the method that matches the property that differs.")


PM = [("distilled water", "a pure substance"), ("oxygen gas", "a pure substance"), ("table salt (sodium chloride)", "a pure substance"),
      ("pure gold", "a pure substance"), ("sugar (sucrose)", "a pure substance"), ("tap water", "a mixture"), ("sea water", "a mixture"),
      ("air", "a mixture"), ("milk", "a mixture"), ("soil", "a mixture"), ("orange juice", "a mixture"), ("steel", "a mixture")]


def g_pm():
    o, k = R.choice(PM)
    return tq("Is %s a pure substance or a mixture?" % o, k, [x for x in ["a pure substance", "a mixture", "a solvent only", "a separation method"] if x != k],
              "A pure substance contains only one kind of particle; a mixture contains two or more substances not chemically joined.")


POOL1 = pool(R, [
    ("What is a mixture?", "two or more substances mixed together but not chemically joined", ["one substance only", "a new substance made by a reaction", "a liquid only"], "Mixtures can be separated by physical methods."),
    ("What is a solution?", "a mixture in which a solute is dissolved in a solvent", ["a solid that cannot dissolve", "a pure substance", "a separation method"], "Salt water is a solution."),
    ("Can filtration remove dissolved salt from sea water?", "No. Dissolved salt particles pass through the filter paper.", ["Yes, easily.", "Only if the water is hot.", "Only with cloth."], "Use evaporation or distillation instead."),
    ("Which method separates sand from water?", "filtration", ["distillation", "chromatography", "using a magnet"], "Sand is insoluble and is trapped by the filter."),
    ("Which method gets salt back from salt water?", "evaporation", ["filtration", "using a magnet", "decanting"], "The water evaporates and the salt is left."),
    ("Which method gets pure water from salt water?", "distillation", ["filtration", "chromatography", "sieving"], "The water boils, then the steam is condensed and collected."),
    ("What is the substance that dissolves called?", "the solute", ["the solvent", "the solution", "the filtrate"], "The solvent is what it dissolves in."),
    ("What is the liquid that passes through filter paper called?", "the filtrate", ["the residue", "the solute", "the condenser"], "The solid left behind is the residue."),
    ("What does 'insoluble' mean?", "does not dissolve", ["dissolves easily", "evaporates quickly", "is magnetic"], "Sand is insoluble in water."),
    ("Why is tap water not a pure substance?", "It contains dissolved minerals and other substances.", ["It is a gas.", "It is made of only water particles.", "It is solid."], "Only distilled water is close to pure."),
])
POOL5 = pool(R, [
    ("Mia has a mixture of salt, sand and iron filings. Which order of steps separates all three?", "magnet, then dissolve in water and filter, then evaporate", ["evaporate, then magnet, then filter", "filter first without water", "distil, then magnet, then filter"], "Remove iron first, then use solubility."),
    ("Jack dissolves 15 g of salt in 200 g of water. What is the mass of the solution?", "215 g", ["200 g", "185 g", "15 g"], "Mass is conserved when dissolving."),
    ("Ruby's chromatogram shows a black ink splits into blue, red and yellow. What does this show?", "The black ink is a mixture of dyes.", ["The ink is pure.", "Paper made the colours.", "Water is coloured."], "Different dyes travel different distances."),
    ("Why is the start line in chromatography drawn in pencil, not pen?", "Pencil does not dissolve and move up the paper.", ["Pencil is darker.", "Pen is too expensive.", "Pencil is magnetic."], "Pen ink would separate too."),
    ("Kai evaporates sea water and gets 3.5 g of salt from 100 g. How much salt would 1 kg of sea water give?", "35 g", ["3.5 g", "350 g", "1 kg"], "1 kg is 10 times 100 g."),
    ("Why should a distillation flask never be heated until dry?", "It could crack or overheat and is unsafe.", ["It makes more water.", "It cools the condenser.", "It is faster."], "Safety matters in every method."),
])


def main():
    sets = U.sets([
        ("Pure substances and mixtures", [(g_pm, 8), (POOL1, 4), (m_voc, 5), (m_pure, 3)]),
        ("Choosing a method", [(m_method, 8), (s_meth, 6), (POOL1, 4), (m_b1, 2)]),
        ("How methods work", [(s_prin, 6), (s_dist, 5), (s_b1, 4), (m_b1, 3), (POOL1, 2)]),
        ("Separation in Australian industry", [(g_ind, 8), (m_chrom, 3), (m_mass, 3), (g_pm, 2), (m_voc, 4)]),
        ("Investigations", [(POOL5, 6), (m_b5, 4), (s_b5, 5), (g_ind, 3), (m_chrom, 0), (s_meth, 2)]),
    ])
    make_au(YEAR, "mixtures-and-separation", SORT, "AC9S7U06", "Chemical sciences",
            "Classify matter as pure substances or mixtures and investigate techniques for separating mixtures, relating them to the "
            "properties of the substances (summary of the Australian Curriculum v9.0 Science content description).",
            "Mixtures and Separation", "Mixtures and separation",
            "Free Year 7 science worksheets on pure substances, mixtures and solutions, and separation techniques: filtration, evaporation, "
            "distillation, chromatography and magnetism, with Australian industry examples. 100 questions with answers.",
            "Separate a mixture by a property that differs.", "Pure substances have one kind of particle; mixtures can be separated by physical methods.",
            "<p><b>Mixtures can be separated because their parts have different properties.</b></p><ul>"
            "<li>Particle size or solubility: filtration (sand from water). Boiling point: evaporation and distillation (salt and water).</li>"
            "<li>How far dyes travel on paper: chromatography. Magnetism: iron from sand. Density: panning for gold.</li>"
            "<li>A pure substance has only one kind of particle; tap water, air and sea water are mixtures.</li></ul>",
            [("Get salt back from salt water?", ["water evaporates", "salt stays behind"], "evaporation"),
             ("Remove iron filings from sand?", ["iron is magnetic"], "a magnet")],
            ["Thinking filtration removes dissolved salt.", "Thinking a dissolved solute has disappeared.",
             "Calling tap water or air a pure substance."],
            [("What is the difference between evaporation and distillation?", "Evaporation removes the solvent to keep the solid, such as salt. Distillation boils the liquid and condenses the vapour to collect the pure liquid."),
             ("How does chromatography separate inks?", "The solvent moves up the paper and carries each dye a different distance, depending on how soluble it is and how strongly it sticks to the paper."),
             ("How does Perth get drinking water from the sea?", "Desalination plants push sea water through very fine membranes (reverse osmosis) that let water through but hold back the salt.")],
            sets)


if __name__ == "__main__":
    main()
