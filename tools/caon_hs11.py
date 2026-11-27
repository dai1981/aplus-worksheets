# -*- coding: utf-8 -*-
"""Ontario Grade 11 science: SBI3U Biology, SCH3U Chemistry, SPH3U Physics (2008). Built with caon_hs."""
from caon_hs import HU

G = "gen_us_science_"


def molar_volume(R):
    """gas volumes at STP (22.4 L/mol, 0 °C and 101.325 kPa) and SATP (24.8 L/mol, 25 °C and 100 kPa)"""
    from sci_common import item
    gases = [("oxygen", "O₂", 32.0), ("nitrogen", "N₂", 28.0), ("carbon dioxide", "CO₂", 44.0), ("methane", "CH₄", 16.0),
             ("hydrogen", "H₂", 2.0), ("ammonia", "NH₃", 17.0), ("helium", "He", 4.0), ("argon", "Ar", 39.9)]

    def g():
        name, f, M = R.choice(gases)
        cond = R.choice(["STP", "SATP"])
        vm = 22.4 if cond == "STP" else 24.8
        other = 24.8 if cond == "STP" else 22.4
        k = R.choice(["mol2v", "v2mol", "g2v"])
        if k == "mol2v":
            n = R.choice([0.25, 0.50, 1.50, 2.00, 2.50, 3.00, 0.20, 0.40, 1.25, 4.00])
            v = n * vm
            q = "What volume does %.2f mol of %s gas (%s) occupy at %s?" % (n, name, f, cond)
            a = "%.1f L" % v
            w = ["%.1f L" % (n * other), "%.1f L" % (vm / n), "%.2f L" % (n / vm * 100)]
            e = "V = n × V<sub>m</sub> = %.2f mol × %.1f L/mol = %.1f L." % (n, vm, v)
        elif k == "v2mol":
            n = R.choice([0.25, 0.50, 1.50, 2.00, 0.10, 0.75, 1.20, 3.00])
            v = round(n * vm, 1)
            q = "A sample of %s (%s) occupies %.1f L at %s. How many moles are present?" % (name, f, v, cond)
            a = "%.2f mol" % (v / vm)
            w = ["%.2f mol" % (v / other), "%.0f mol" % (v * vm), "%.2f mol" % (v / vm / 2)]
            e = "n = V ÷ V<sub>m</sub> = %.1f L ÷ %.1f L/mol = %.2f mol." % (v, vm, v / vm)
        else:
            n = R.choice([0.25, 0.50, 2.00, 0.10, 1.50, 0.20])
            m = n * M
            v = n * vm
            q = "What volume does %.1f g of %s (%s, M = %.1f g/mol) occupy at %s?" % (m, name, f, M, cond)
            a = "%.2f L" % v
            w = ["%.2f L" % (n * other), "%.2f L" % (m * vm), "%.2f L" % (vm / n)]
            e = "n = %.1f g ÷ %.1f g/mol = %.2f mol, so V = %.2f mol × %.1f L/mol = %.2f L." % (m, M, n, n, vm, v)
        if len({a} | set(w)) < 4:
            return None
        return item(q, a, w, e)
    return g


def UNITS():
    return [
        # ---------------- SBI3U Biology ----------------
        HU("SBI3U", "B", 1, "diversity-of-living-things", "B3.1, B3.2, B3.3, B3.4",
           "Classification and taxonomy: the three domains and six kingdoms; binomial nomenclature and the taxonomic ranks; "
           "dichotomous keys; the characteristics of bacteria, archaea, viruses, protists, fungi, plants and animals; and the importance of biodiversity.",
           "Diversity of Living Things", "diversity of living things",
           "Free Grade 11 Biology (SBI3U) worksheets on the diversity of living things: taxonomy, binomial names, domains and kingdoms, bacteria and viruses, protists, fungi, plants and animals. 100 questions with answers.",
           "Living things are grouped by shared features and evolutionary history.", "Domain, kingdom, phylum, class, order, family, genus, species.",
           "<p>Biologists sort the huge variety of life into groups that share features and ancestry. The ranks go from broad to narrow: "
           "domain, kingdom, phylum, class, order, family, genus, species. Every species has a two-part scientific name, the genus and the species, "
           "written in italics (<i>Acer saccharum</i>, the sugar maple).</p>"
           "<p>The three domains are Bacteria, Archaea (both prokaryotes, with no nucleus) and Eukarya (cells with a nucleus). "
           "Eukarya includes protists, fungi, plants and animals. Viruses are not placed in any kingdom: they are not cells and can only reproduce inside a host cell.</p>",
           [("Which two ranks make up a scientific name?", ["Binomial nomenclature uses the genus and the species."], "genus and species"),
            ("A cell has no nucleus and lives in a hot spring. Which domains are possible?", ["No nucleus means prokaryote."], "Bacteria or Archaea")],
           ["Writing the genus with a small letter or not using italics.", "Calling viruses bacteria: viruses are not cells.", "Thinking that fungi are plants: fungi do not photosynthesize and have chitin cell walls."],
           [("Why are fungi not plants?", "Fungi have cell walls made of chitin, cannot photosynthesize and absorb food from their surroundings."),
            ("What is a dichotomous key?", "A tool that identifies an organism by a series of choices between two descriptions.")],
           lambda X: [
               ("Taxonomy and scientific names", [(X.ch("in_s11b", "the-living-world", 2), 8), (X.ch("in_s11b", "the-living-world", 3), 8), (X.ch("al_bio", "genetic-information-and-variation", 5, 12), 4)]),
               ("Domains and kingdoms", [(X.ch("in_s11b", "biological-classification", 1), 10), (X.ch("in_s11b", "the-living-world", 1), 6), (X.ch("in_s11b", "the-living-world", 4), 4)]),
               ("Bacteria, viruses and protists", [(X.ch("in_s11b", "biological-classification", 2), 8), (X.ch("in_s11b", "biological-classification", 4), 8), (X.gen("gen_uk_science_y10_infection_and_response", "g_dis"), 4)]),
               ("Fungi and plants", [(X.ch("in_s11b", "biological-classification", 3), 8), (X.ch("in_s11b", "plant-kingdom", 2), 6), (X.ch("in_s11b", "plant-kingdom", 3), 6)]),
               ("Animals and biodiversity", [(X.ch("in_s11b", "animal-kingdom", 1), 7), (X.ch("in_s11b", "animal-kingdom", 3), 7), (X.gen(G + "bio_ecosystem_stability_and_biodiversity", "g_key"), 3), (X.gen(G + "bio_ecosystem_stability_and_biodiversity", "g_survey"), 3)]),
           ]),
        HU("SBI3U", "C", 2, "evolution", "C3.1, C3.2, C3.3, C3.4",
           "The evidence for evolution (fossils, anatomy, embryology, DNA); natural and artificial selection; mechanisms of evolutionary change "
           "(mutation, genetic drift, gene flow, non-random mating); adaptation and speciation.",
           "Evolution", "evolution",
           "Free Grade 11 Biology (SBI3U) worksheets on evolution: evidence for evolution, natural selection, artificial selection, genetic drift and gene flow, adaptation and speciation. 100 questions with answers.",
           "Evolution is a change in allele frequencies in a population over generations.", "Natural selection: variation, inheritance, overproduction, differential survival.",
           "<p>Natural selection needs four things: individuals vary, the variation is inherited, more offspring are produced than can survive, "
           "and individuals with favourable traits survive and reproduce more. Over many generations the favourable alleles become more common.</p>"
           "<p>Other mechanisms also change allele frequencies: mutation (new alleles), genetic drift (chance, strongest in small populations), "
           "gene flow (migration) and non-random mating. When populations are isolated long enough to stop interbreeding, a new species forms.</p>",
           [("Bacteria in a hospital become resistant to an antibiotic. Which mechanism explains this?", ["Resistant bacteria survive the drug and reproduce."], "natural selection"),
            ("A storm kills most of a small island population at random. What is the change in allele frequency called?", ["Chance events in small populations"], "genetic drift (bottleneck effect)")],
           ["Saying individuals evolve: populations evolve, individuals do not.", "Thinking organisms change because they need to: variation comes first, then selection.", "Mixing up homologous structures (same origin) and analogous structures (same function)."],
           [("What are homologous structures?", "Structures with the same basic plan because they come from a common ancestor, such as the arm of a human and the flipper of a whale."),
            ("How is artificial selection different from natural selection?", "In artificial selection, people choose which individuals breed; in natural selection, the environment does.")],
           lambda X: [
               ("Evidence for evolution", [(X.ch("in_s12b", "evolution", 1), 8), (X.gen(G + "bio_evidence_for_evolution", "g_struct"), 4), (X.gen(G + "bio_evidence_for_evolution", "g_seq"), 4), (X.gen(G + "bio_evidence_for_evolution", "g_layer"), 4)]),
               ("Natural selection", [(X.ch("in_s12b", "evolution", 2), 8), (X.gen(G + "bio_natural_selection_and_adaptation", "g_scen"), 6), (X.gen(G + "bio_natural_selection_and_adaptation", "g_data"), 6)]),
               ("Mechanisms of evolutionary change", [(X.ch("in_s12b", "evolution", 4), 10), (X.gen(G + "bio_changes_in_trait_frequency", "g_select"), 5), (X.gen(G + "bio_changes_in_trait_frequency", "g_freq"), 5)]),
               ("Artificial selection and resistance", [(X.gen(G + "g8_artificial_selection_and_genetic_engineering", "g_meth"), 6), (X.gen(G + "g8_artificial_selection_and_genetic_engineering", "g_data"), 6), (X.gen(G + "bio_natural_selection_and_adaptation", "g_resist"), 8)]),
               ("Adaptation and speciation", [(X.ch("al_bio", "genetics-populations-and-evolution", 4, 13), 10), (X.gen(G + "bio_speciation_extinction_and_biodiversity", "g_iso"), 5), (X.gen(G + "bio_speciation_extinction_and_biodiversity", "g_rate"), 5)]),
           ]),
        HU("SBI3U", "D", 3, "genetic-processes", "D3.1, D3.2, D3.3, D3.4",
           "Meiosis and how it produces variation; Mendel's laws; monohybrid and dihybrid crosses; incomplete dominance, codominance, multiple alleles and sex-linked traits; "
           "pedigrees and genetic disorders; and genetic technologies.",
           "Genetic Processes", "genetic processes",
           "Free Grade 11 Biology (SBI3U) worksheets on genetic processes: meiosis, Punnett squares, monohybrid and dihybrid crosses, incomplete dominance, blood types, sex-linked traits and biotechnology. 100 questions with answers.",
           "Each parent passes on one allele of each gene.", "A Punnett square shows the expected ratios of offspring.",
           "<p>Meiosis makes gametes with half the number of chromosomes (23 in humans). Crossing over and independent assortment make every gamete different. "
           "At fertilization, the zygote gets one allele of each gene from each parent.</p>"
           "<p>Write the parents' genotypes, list their gametes and fill in a Punnett square. A monohybrid cross of two heterozygotes (Aa × Aa) gives a 3 : 1 phenotype ratio; "
           "a dihybrid cross (AaBb × AaBb) gives 9 : 3 : 3 : 1. Not all traits follow simple dominance: incomplete dominance blends, codominance shows both, and X-linked traits appear more often in males.</p>",
           [("Aa × aa. What fraction of the offspring show the recessive trait?", ["Gametes: A, a and a, a", "Offspring: Aa, Aa, aa, aa"], "1/2"),
            ("A colour-blind man (XᵇY) and a woman who is not a carrier (XᴮXᴮ). What fraction of their sons are colour-blind?", ["Sons get the X from their mother: Xᴮ"], "none")],
           ["Confusing genotype (letters) with phenotype (the trait).", "Forgetting that each gamete carries only one allele of each gene.", "Giving sons their X chromosome from the father."],
           [("What is the difference between mitosis and meiosis?", "Mitosis makes two identical diploid cells; meiosis makes four different haploid gametes."),
            ("What is codominance?", "Both alleles are fully shown in the heterozygote, as in blood type AB.")],
           lambda X: [
               ("Meiosis", [(X.ch("in_s11b", "cell-cycle-and-cell-division", 3), 8), (X.gen(G + "bio_meiosis_and_genetic_variation", "g_num"), 4), (X.gen(G + "bio_meiosis_and_genetic_variation", "g_stage"), 4), (X.gen(G + "bio_meiosis_and_genetic_variation", "g_cmp"), 4)]),
               ("Monohybrid crosses", [(X.gen(G + "bio_punnett_squares_and_heredity", "g_mono"), 5), (X.gen(G + "bio_punnett_squares_and_heredity", "g_expect"), 4), (X.gen(G + "bio_punnett_squares_and_heredity", "g_ratio"), 4), (X.ch("in_s12b", "principles-of-inheritance-and-variation", 1), 7)]),
               ("Dihybrid crosses and other patterns", [(X.ch("in_s12b", "principles-of-inheritance-and-variation", 2), 8), (X.ch("in_s12b", "principles-of-inheritance-and-variation", 3), 6), (X.gen(G + "bio_punnett_squares_and_heredity", "g_blood"), 3), (X.gen(G + "bio_punnett_squares_and_heredity", "g_inc"), 3)]),
               ("Sex-linked traits and disorders", [(X.ch("in_s12b", "principles-of-inheritance-and-variation", 4), 8), (X.ch("in_s12b", "principles-of-inheritance-and-variation", 5), 6), (X.gen(G + "bio_punnett_squares_and_heredity", "g_xlink"), 6)]),
               ("Genetic technologies", [(X.ch("in_s12b", "biotechnology-principles-and-processes", 1), 6), (X.ch("in_s12b", "biotechnology-principles-and-processes", 3), 6), (X.ch("al_bio", "gene-expression-and-biotechnology", 4, 13), 4), (X.ch("in_s12b", "biotechnology-and-its-applications", 2), 4)]),
           ]),
        HU("SBI3U", "E", 4, "animals-structure-and-function", "E3.1, E3.2, E3.3, E3.4",
           "The structure and function of the digestive, respiratory and circulatory systems in animals; how they interact; "
           "and disorders and lifestyle factors that affect them.",
           "Animals: Structure and Function", "animal structure and function",
           "Free Grade 11 Biology (SBI3U) worksheets on animal structure and function: digestion and enzymes, the respiratory system, gas exchange, the heart and blood vessels, blood and health. 100 questions with answers.",
           "Digestion, respiration and circulation work together to supply every cell.", "Large surface areas and short distances make exchange fast.",
           "<p>The digestive system breaks large food molecules into small ones (amylase: starch to sugars; protease: proteins to amino acids; lipase: fats to fatty acids and glycerol) "
           "that are absorbed through the villi of the small intestine.</p>"
           "<p>In the lungs, oxygen diffuses from the alveoli into the blood and carbon dioxide diffuses out. The heart pumps blood in two circuits: "
           "the right side sends it to the lungs, the left side to the body. Arteries carry blood away from the heart, veins bring it back, and capillaries are where exchange happens.</p>",
           [("Which enzyme starts digesting starch in the mouth?", ["Starch is a carbohydrate."], "salivary amylase"),
            ("Why is the wall of the left ventricle thicker than the right?", ["The left side pumps to the whole body."], "it must pump blood at higher pressure around the body")],
           ["Saying arteries always carry oxygen-rich blood: the pulmonary artery carries oxygen-poor blood.", "Thinking digestion happens mainly in the stomach: most absorption is in the small intestine.", "Mixing up breathing (moving air) and cellular respiration (releasing energy)."],
           [("Why do alveoli have thin walls?", "A short diffusion distance lets oxygen and carbon dioxide move between air and blood quickly."),
            ("What do the villi do?", "They give the small intestine a huge surface area for absorbing digested food.")],
           lambda X: [
               ("Digestion and enzymes", [(X.ch("al_bio", "exchange-and-transport", 2, 12), 8), (X.gen("gen_sg_science_s3_nutrition_in_humans", "g_enz"), 6), (X.gen("gen_sg_science_s2_human_digestive_system", "g_path"), 3), (X.gen("gen_sg_science_s2_human_digestive_system", "g_org"), 3)]),
               ("The respiratory system", [(X.ch("in_s11b", "breathing-and-exchange-of-gases", 1), 8), (X.ch("in_s11b", "breathing-and-exchange-of-gases", 3), 6), (X.gen("gen_sg_science_s3_respiration_in_humans", "g_mech"), 6)]),
               ("Gas exchange", [(X.ch("al_bio", "exchange-and-transport", 1, 12), 10), (X.ch("in_s11b", "breathing-and-exchange-of-gases", 4), 4), (X.gen("gen_sg_science_s3_respiration_in_humans", "g_air"), 6)]),
               ("The heart and blood vessels", [(X.ch("in_s11b", "body-fluids-and-circulation", 3), 7), (X.ch("al_bio", "exchange-and-transport", 3, 12), 7), (X.gen("gen_sg_science_s3_transport_in_humans", "g_ves"), 6)]),
               ("Blood and health", [(X.ch("in_s11b", "body-fluids-and-circulation", 1), 6), (X.ch("in_s11b", "body-fluids-and-circulation", 2), 6), (X.gen("gen_sg_science_s3_transport_in_humans", "g_chd"), 4), (X.gen("gen_uk_science_y9_health_and_drugs", "g_smoke"), 4)]),
           ]),
        HU("SBI3U", "F", 5, "plants-anatomy-growth-and-function", "F3.1, F3.2, F3.3, F3.4",
           "Plant tissues (dermal, ground, vascular) and organs (roots, stems, leaves); transport of water and sugars in xylem and phloem; "
           "photosynthesis and the factors that affect it; and plant growth, hormones and responses.",
           "Plants: Anatomy, Growth and Function", "plant anatomy, growth and function",
           "Free Grade 11 Biology (SBI3U) worksheets on plants: plant tissues, roots, stems and leaves, xylem and phloem, transpiration, photosynthesis and plant hormones. 100 questions with answers.",
           "Xylem carries water up; phloem carries sugars to where they are used.", "Leaves are built for photosynthesis; stomata control gas exchange and water loss.",
           "<p>Plants have three tissue systems: dermal (epidermis, guard cells, root hairs), ground (parenchyma, collenchyma, sclerenchyma) and vascular (xylem and phloem). "
           "Meristems at root and shoot tips make new cells for growth.</p>"
           "<p>Water enters root hairs by osmosis and is pulled up the xylem by transpiration from the leaves. Sugars made in photosynthesis move in the phloem from sources (leaves) to sinks (roots, fruits). "
           "Hormones such as auxin, gibberellin and abscisic acid control growth and responses like phototropism.</p>",
           [("On a hot, windy day, what happens to the rate of transpiration?", ["More evaporation from the leaves"], "it increases"),
            ("Which hormone makes a shoot bend towards light?", ["Cells on the shaded side grow longer."], "auxin")],
           ["Saying xylem carries sugars: xylem carries water and minerals.", "Thinking plants take in food from the soil: they make sugars by photosynthesis.", "Forgetting that stomata close to save water, which also slows photosynthesis."],
           [("What are guard cells?", "A pair of cells around each stoma that open and close it."),
            ("What is a meristem?", "A region of dividing cells, such as at a root or shoot tip, where a plant grows.")],
           lambda X: [
               ("Plant tissues", [(X.ch("in_s11b", "anatomy-of-flowering-plants", 1), 8), (X.ch("in_s11b", "anatomy-of-flowering-plants", 2), 8), (X.gen("gen_sg_science_s3_cell_structure_and_organisation", "g_spec"), 4)]),
               ("Roots, stems and leaves", [(X.ch("in_s11b", "anatomy-of-flowering-plants", 3), 10), (X.ch("in_s11b", "morphology-of-flowering-plants", 1), 10)]),
               ("Transport in plants", [(X.ch("al_bio", "exchange-and-transport", 5, 12), 10), (X.gen("gen_sg_science_s3_nutrition_and_transport_in_flowering_plants", "g_trp"), 5), (X.gen("gen_sg_science_s3_nutrition_and_transport_in_flowering_plants", "g_pot"), 5)]),
               ("Photosynthesis in leaves", [(X.gen("gen_sg_science_s3_nutrition_and_transport_in_flowering_plants", "g_lim"), 6), (X.gen("gen_sg_science_s3_nutrition_and_transport_in_flowering_plants", "g_bub"), 4), (X.gen(G + "bio_photosynthesis", "g_lim"), 5), (X.gen(G + "bio_photosynthesis", "g_elodea"), 5)]),
               ("Plant growth and hormones", [(X.ch("in_s11b", "plant-growth-and-development", 2), 8), (X.ch("in_s11b", "plant-growth-and-development", 3), 6), (X.ch("in_s11b", "plant-growth-and-development", 1), 6)]),
           ]),
        # ---------------- SCH3U Chemistry ----------------
        HU("SCH3U", "B", 6, "matter-chemical-trends-and-chemical-bonding", "B3.1, B3.2, B3.3, B3.4, B3.5",
           "Atomic structure and isotopes; the periodic table and periodic trends (atomic radius, ionization energy, electron affinity, electronegativity); "
           "ionic and covalent bonding; Lewis structures; polar bonds and intermolecular forces.",
           "Matter, Chemical Trends and Chemical Bonding", "chemical trends and bonding",
           "Free Grade 11 Chemistry (SCH3U) worksheets on matter, periodic trends and bonding: isotopes, atomic radius, ionization energy, electronegativity, ionic and covalent bonds, polarity and intermolecular forces. 100 questions with answers.",
           "Periodic trends come from nuclear charge and the number of electron shells.", "Bond type depends on the electronegativity difference.",
           "<p>Across a period, the nuclear charge rises while the number of shells stays the same, so atoms get smaller and ionization energy and electronegativity increase. "
           "Down a group, more shells are added, so atoms get larger and hold their outer electrons less tightly.</p>"
           "<p>A large electronegativity difference (more than about 1.7) gives an ionic bond; a smaller difference gives a polar covalent bond, and no difference a non-polar covalent bond. "
           "Polar molecules attract each other with dipole–dipole forces; molecules with H bonded to N, O or F form hydrogen bonds, which raise boiling points.</p>",
           [("Which has the larger atomic radius, Na or Cl?", ["Same period; Cl has more protons pulling the electrons in."], "Na"),
            ("Chlorine-35 and chlorine-37: how are they different?", ["Same protons (17)", "Different neutrons"], "chlorine-37 has two more neutrons")],
           ["Thinking atoms get bigger across a period because they gain electrons.", "Calling every bond with a metal and a non-metal covalent.", "Confusing intramolecular bonds (inside molecules) with intermolecular forces (between molecules)."],
           [("What is electronegativity?", "How strongly an atom attracts the shared electrons in a bond. Fluorine has the highest value."),
            ("Why does water have a high boiling point for its size?", "Water molecules form hydrogen bonds with each other, which take extra energy to break.")],
           lambda X: [
               ("Atoms and isotopes", [(X.gen(G + "chem_atomic_structure_and_isotopes", "g_pne"), 6), (X.gen(G + "chem_atomic_structure_and_isotopes", "g_iso"), 5), (X.gen(G + "chem_atomic_structure_and_isotopes", "g_avg"), 4), (X.ch("in_s11c", "structure-of-atom", 1), 5)]),
               ("Periodic trends", [(X.gen(G + "chem_periodic_table_and_trends", "g_trend"), 7), (X.gen(G + "chem_periodic_table_and_trends", "g_fam"), 5), (X.ch("in_s11c", "classification-of-elements-and-periodicity-in-properties", 4), 8)]),
               ("Ionic and covalent bonds", [(X.gen(G + "chem_chemical_bonding", "g_btype"), 6), (X.gen(G + "chem_chemical_bonding", "g_formula"), 5), (X.gen("gen_sg_science_s3_chemical_bonding_and_structure", "g_ion"), 5), (X.gen("gen_sg_science_s3_chemical_bonding_and_structure", "g_formula"), 4)]),
               ("Electronegativity and polarity", [(X.gen(G + "chem_chemical_bonding", "g_polar"), 7), (X.gen(G + "chem_chemical_bonding", "g_cov"), 6), (X.ch("in_s11c", "chemical-bonding-and-molecular-structure", 1), 7)]),
               ("Intermolecular forces and properties", [(X.gen(G + "chem_intermolecular_forces_and_properties", "g_imf"), 6), (X.gen(G + "chem_intermolecular_forces_and_properties", "g_bp"), 5), (X.gen(G + "chem_intermolecular_forces_and_properties", "g_order"), 5), (X.gen(G + "chem_intermolecular_forces_and_properties", "g_state"), 4)]),
           ]),
        HU("SCH3U", "C", 7, "chemical-reactions", "C3.1, C3.2, C3.3, C3.4",
           "The five types of chemical reactions (synthesis, decomposition, single displacement, double displacement, combustion); balancing equations; "
           "the activity series; neutralization; naming and writing formulas for compounds.",
           "Chemical Reactions", "chemical reactions",
           "Free Grade 11 Chemistry (SCH3U) worksheets on chemical reactions: synthesis, decomposition, single and double displacement, combustion, balancing equations, the activity series and neutralization. 100 questions with answers.",
           "Atoms are rearranged, never created or destroyed: balance every equation.", "Synthesis, decomposition, single and double displacement, combustion.",
           "<p>Classify a reaction by its pattern: A + B → AB (synthesis), AB → A + B (decomposition), A + BC → AC + B (single displacement), "
           "AB + CD → AD + CB (double displacement) and fuel + O₂ → CO₂ + H₂O (combustion of a hydrocarbon).</p>"
           "<p>A single displacement happens only if the free element is more reactive than the one it replaces (check the activity series). "
           "A double displacement happens if a precipitate, a gas or water forms. Balance by changing coefficients, never subscripts.</p>",
           [("Zn + CuSO₄ → ? Will it react?", ["Zinc is above copper in the activity series."], "yes: Zn + CuSO₄ → ZnSO₄ + Cu"),
            ("Balance: H₂ + O₂ → H₂O", ["2 O on the left, so 2 H₂O", "Then 4 H, so 2 H₂"], "2H₂ + O₂ → 2H₂O")],
           ["Changing a subscript to balance an equation, which makes a different substance.", "Writing hydrogen or oxygen as single atoms (H, O) instead of H₂ and O₂.", "Predicting a single displacement when the free metal is less reactive."],
           [("What are the products of complete combustion of a hydrocarbon?", "Carbon dioxide and water."),
            ("What is a neutralization reaction?", "A double displacement between an acid and a base that makes a salt and water.")],
           lambda X: [
               ("Types of reactions", [(X.gen(G + "chem_types_of_chemical_reactions", "g_type"), 10), (X.gen(G + "chem_types_of_chemical_reactions", "g_prod"), 5), (X.gen("gen_sg_science_s2_chemical_changes", "g_type"), 5)]),
               ("Balancing equations", [(X.gen(G + "chem_balancing_chemical_equations", "g_check"), 6), (X.gen(G + "chem_balancing_chemical_equations", "g_pick"), 7), (X.gen(G + "chem_balancing_chemical_equations", "g_missing"), 7)]),
               ("The activity series", [(X.gen(G + "chem_types_of_chemical_reactions", "g_act"), 10), (X.gen("gen_uk_science_y9_reactivity_and_extraction", "g_red"), 5), (X.gen("gen_uk_science_y9_reactivity_and_extraction", "g_ext"), 5)]),
               ("Acids, bases and neutralization", [(X.gen("gen_sg_science_s3_acid_base_chemistry", "g_prod"), 7), (X.gen("gen_sg_science_s3_acid_base_chemistry", "g_sol"), 5), (X.gen("gen_uk_science_y10_chemical_changes", "g_salt"), 4), (X.gen("gen_uk_science_y10_chemical_changes", "g_ph"), 4)]),
               ("Names, formulas and evidence of reactions", [(X.gen(G + "chem_chemical_bonding", "g_name"), 10), (X.gen(G + "chem_types_of_chemical_reactions", "g_evid"), 5), (X.gen(G + "chem_balancing_chemical_equations", "g_count"), 5)]),
           ]),
        HU("SCH3U", "D", 8, "quantities-in-chemical-reactions", "D3.1, D3.2, D3.3, D3.4, D3.5",
           "The mole and Avogadro's number; molar mass; converting between mass, moles and number of particles; percentage composition; "
           "empirical and molecular formulas; mole ratios in balanced equations; limiting reagent; theoretical and percentage yield.",
           "Quantities in Chemical Reactions", "quantities in chemical reactions",
           "Free Grade 11 Chemistry (SCH3U) worksheets on quantities in chemical reactions: the mole, molar mass, percentage composition, empirical formulas, stoichiometry, limiting reagent and percentage yield. 100 questions with answers.",
           "n = m ÷ M: change grams to moles before using the equation.", "1 mol = 6.02 × 10²³ particles.",
           "<p>A mole is 6.02 × 10²³ particles. The molar mass M (g/mol) is the mass of one mole, found by adding the atomic masses. "
           "Use n = m ÷ M to change grams to moles and N = n × N<sub>A</sub> for particles.</p>"
           "<p>In stoichiometry, change the given quantity to moles, use the mole ratio from the balanced equation, then change to the unit you want. "
           "The limiting reagent is the reactant that runs out first; it decides the theoretical yield. Percentage yield = actual ÷ theoretical × 100%.</p>",
           [("How many moles are in 36.0 g of water (M = 18.0 g/mol)?", ["n = 36.0 ÷ 18.0"], "2.00 mol"),
            ("2H₂ + O₂ → 2H₂O. How many moles of water form from 3.0 mol of O₂?", ["Ratio H₂O : O₂ = 2 : 1"], "6.0 mol")],
           ["Using grams in the mole ratio instead of moles.", "Choosing the reactant with the smaller mass as the limiting reagent.", "Forgetting to multiply by the subscript when finding molar mass (H₂O has two H)."],
           [("What is an empirical formula?", "The simplest whole-number ratio of atoms in a compound, such as CH₂O for glucose (C₆H₁₂O₆)."),
            ("Why is the actual yield usually less than the theoretical yield?", "Some product is lost, side reactions happen or the reaction does not go to completion.")],
           lambda X: [
               ("The mole and Avogadro's number", [(X.gen(G + "chem_the_mole_and_molar_mass", "g_part"), 7), (X.gen(G + "chem_the_mole_and_molar_mass", "g_atoms"), 6), (X.ch("in_s11c", "some-basic-concepts-of-chemistry", 1), 7)]),
               ("Molar mass and conversions", [(X.gen(G + "chem_the_mole_and_molar_mass", "g_mm"), 7), (X.gen(G + "chem_the_mole_and_molar_mass", "g_g2mol"), 7), (X.gen(G + "chem_the_mole_and_molar_mass", "g_mol2g"), 6)]),
               ("Percentage composition and empirical formulas", [(X.gen(G + "chem_the_mole_and_molar_mass", "g_pct"), 7), (X.gen("gen_sg_science_s3_chemical_calculations", "g_emp"), 7), (X.ch("in_s11c", "some-basic-concepts-of-chemistry", 2), 6)]),
               ("Stoichiometry", [(X.gen(G + "chem_stoichiometry", "g_ratio"), 7), (X.gen(G + "chem_stoichiometry", "g_mol"), 7), (X.gen(G + "chem_stoichiometry", "g_mass"), 6)]),
               ("Limiting reagent and percentage yield", [(X.gen(G + "chem_stoichiometry", "g_limit"), 7), (X.gen(G + "chem_stoichiometry", "g_yield"), 6), (X.ch("al_chem", "atomic-structure-and-amount-of-substance", 5, 12), 7)]),
           ]),
        HU("SCH3U", "E", 9, "solutions-and-solubility", "E3.1, E3.2, E3.3, E3.4, E3.5",
           "Solutions, solubility and the factors that affect it; concentration (mol/L, % and ppm); dilution; acids and bases, pH; "
           "titration; and water quality and treatment.",
           "Solutions and Solubility", "solutions and solubility",
           "Free Grade 11 Chemistry (SCH3U) worksheets on solutions and solubility: solubility, concentration in mol/L, dilution, acids and bases, pH and titration. 100 questions with answers.",
           "Concentration c = n ÷ V, with V in litres.", "Dilution: c₁V₁ = c₂V₂.",
           "<p>A solution is a solute dissolved in a solvent. “Like dissolves like”: polar and ionic solutes dissolve in water; non-polar solutes dissolve in non-polar solvents. "
           "Most solids dissolve better in hot water, but gases dissolve better in cold water.</p>"
           "<p>Molar concentration c = n ÷ V (mol/L). When you dilute a solution the moles of solute do not change, so c₁V₁ = c₂V₂. "
           "In a titration, a solution of known concentration is added until the reaction is complete; the moles that reacted give the unknown concentration.</p>",
           [("0.50 mol of NaCl in 250 mL of solution. Concentration?", ["V = 0.250 L", "c = 0.50 ÷ 0.250"], "2.0 mol/L"),
            ("Dilute 100 mL of 3.0 mol/L acid to 600 mL. New concentration?", ["c₂ = 3.0 × 100 ÷ 600"], "0.50 mol/L")],
           ["Using millilitres instead of litres in c = n ÷ V.", "Thinking a gas dissolves better in warm water.", "Mixing up a strong acid (fully ionized) and a concentrated acid (lots of acid per litre)."],
           [("What does pH 3 mean compared with pH 5?", "pH 3 has 100 times the hydrogen-ion concentration of pH 5."),
            ("What is a saturated solution?", "A solution holding the most solute that can dissolve at that temperature.")],
           lambda X: [
               ("Solutions and solubility", [(X.gen("gen_sg_science_s1_elements_compounds_and_mixtures", "g_solub"), 6), (X.gen("gen_sg_science_s1_elements_compounds_and_mixtures", "g_sol"), 4), (X.ch("in_s12c", "solutions", 1), 10)]),
               ("Concentration", [(X.ch("in_s11c", "some-basic-concepts-of-chemistry", 3), 10), (X.gen("gen_sg_science_s3_chemical_calculations", "g_conc"), 10)]),
               ("Dilution and preparing solutions", [(X.ch("in_s11c", "some-basic-concepts-of-chemistry", 5), 10), (X.ch("al_chem", "atomic-structure-and-amount-of-substance", 3, 12), 10)]),
               ("Acids, bases and pH", [(X.ch("in_s11c", "equilibrium", 3), 10), (X.gen("gen_sg_science_s3_acid_base_chemistry", "g_strong"), 5), (X.gen("gen_uk_science_y10_chemical_changes", "g_ph"), 5)]),
               ("Titration and water quality", [(X.gen("gen_sg_science_s3_chemical_calculations", "g_tit"), 10), (X.ch("al_chem", "acids-bases-and-electrode-potentials", 1, 13), 6), (X.gen("gen_sg_science_s3_qualitative_analysis", "g_cat"), 4)]),
           ]),
        HU("SCH3U", "F", 10, "gases-and-atmospheric-chemistry", "F3.1, F3.2, F3.3, F3.4, F3.5",
           "The kinetic molecular theory; Boyle's, Charles's, Gay-Lussac's and the combined gas laws; the ideal gas law; molar volume at STP and SATP; "
           "gas stoichiometry; and the composition and pollution of the atmosphere.",
           "Gases and Atmospheric Chemistry", "gases and atmospheric chemistry",
           "Free Grade 11 Chemistry (SCH3U) worksheets on gases: the kinetic molecular theory, Boyle's and Charles's laws, the combined and ideal gas laws, molar volume at STP and SATP, and air quality. 100 questions with answers.",
           "Use kelvin in every gas law: T(K) = T(°C) + 273.", "PV = nRT, with R = 8.31 kPa·L/(mol·K).",
           "<p>Gas particles move fast and randomly, and their pressure comes from collisions with the walls. At constant temperature, P₁V₁ = P₂V₂ (Boyle). "
           "At constant pressure, V₁/T₁ = V₂/T₂ (Charles). Together, P₁V₁/T₁ = P₂V₂/T₂.</p>"
           "<p>The ideal gas law PV = nRT links pressure (kPa), volume (L), moles and kelvin temperature. One mole of any gas fills 22.4 L at STP (0 °C, 101.325 kPa) "
           "and 24.8 L at SATP (25 °C, 100 kPa).</p>",
           [("A gas at 100 kPa fills 6.0 L. It is squeezed to 2.0 L at the same temperature. New pressure?", ["P₂ = 100 × 6.0 ÷ 2.0"], "300 kPa"),
            ("Volume of 2.00 mol of oxygen at STP?", ["V = 2.00 × 22.4"], "44.8 L")],
           ["Using °C instead of kelvin in a gas law.", "Mixing up STP (22.4 L/mol) and SATP (24.8 L/mol).", "Thinking heavier gas molecules always take up more space: equal moles of any gas fill equal volumes."],
           [("Why does a balloon shrink in the cold?", "The gas particles slow down and hit the walls less hard, so the volume decreases at the same pressure."),
            ("What gases cause acid rain?", "Sulfur dioxide and nitrogen oxides, which form acids with water in the air.")],
           lambda X: [
               ("The kinetic molecular theory", [(X.gen("gen_sg_science_s3_kinetic_particle_model_of_matter", "g_prop"), 5), (X.gen("gen_sg_science_s3_kinetic_particle_model_of_matter", "g_pres"), 5), (X.gen("gen_sg_science_s3_kinetic_particle_model_of_matter", "g_temp"), 4), (X.ch("in_s11p", "kinetic-theory", 3), 6)]),
               ("Boyle's and Charles's laws", [(X.ch("in_s11p", "kinetic-theory", 2), 12), (X.ch("al_phys", "thermal-physics-and-ideal-gases", 3, 13), 8)]),
               ("The combined and ideal gas laws", [(X.ch("in_s11p", "kinetic-theory", 1), 10), (X.ch("al_phys", "thermal-physics-and-ideal-gases", 4, 13), 10)]),
               ("Molar volume and gas stoichiometry", [(X.f(molar_volume), 20)]),
               ("The atmosphere and air quality", [(X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_comp"), 5), (X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_ghg"), 5), (X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_poll"), 5), (X.gen("gen_sg_science_s4_maintaining_air_quality", "g_rain"), 5)]),
           ]),
        # ---------------- SPH3U Physics ----------------
        HU("SPH3U", "B", 11, "kinematics", "B3.1, B3.2, B3.3, B3.4",
           "Distance, displacement, speed, velocity and acceleration; position–time and velocity–time graphs; the equations of uniformly accelerated motion; "
           "free fall; and motion in two dimensions with vectors.",
           "Kinematics", "kinematics",
           "Free Grade 11 Physics (SPH3U) worksheets on kinematics: displacement and velocity, acceleration, motion graphs, the kinematics equations, free fall and two-dimensional vectors. 100 questions with answers.",
           "Velocity is the slope of a position–time graph; acceleration is the slope of a velocity–time graph.", "Free fall: a = 9.8 m/s² down.",
           "<p>Displacement and velocity are vectors: they have a direction. Average velocity = displacement ÷ time; acceleration = change in velocity ÷ time. "
           "On a velocity–time graph, the slope is the acceleration and the area under the line is the displacement.</p>"
           "<p>For constant acceleration use v₂ = v₁ + aΔt, Δd = v₁Δt + ½aΔt², v₂² = v₁² + 2aΔd and Δd = ½(v₁ + v₂)Δt. "
           "Choose a positive direction first. In free fall the acceleration is 9.8 m/s² downwards.</p>",
           [("A car speeds up from 10 m/s to 25 m/s in 5.0 s. Acceleration?", ["a = (25 − 10) ÷ 5.0"], "3.0 m/s²"),
            ("A stone is dropped from rest. Speed after 2.0 s?", ["v = 9.8 × 2.0"], "19.6 m/s")],
           ["Mixing up distance and displacement after a round trip.", "Forgetting signs: an object thrown up has a negative acceleration if up is positive.", "Reading the height of a v–t graph as the displacement instead of the area."],
           [("What is the velocity at the top of a ball's flight?", "Zero vertically; the acceleration is still 9.8 m/s² downwards."),
            ("How do you add two perpendicular vectors?", "Draw them tip to tail and use the Pythagorean theorem for the size and tan θ for the direction.")],
           lambda X: [
               ("Displacement, speed and velocity", [(X.ch("in_s11p", "motion-in-a-straight-line", 1), 10), (X.gen("gen_sg_science_s3_kinematics", "g_avg"), 10)]),
               ("Acceleration and motion graphs", [(X.gen(G + "phys_motion_and_kinematics", "g_acc"), 7), (X.gen("gen_sg_science_s3_kinematics", "g_acc"), 7), (X.gen("gen_sg_science_s3_kinematics", "g_vt"), 6)]),
               ("The kinematics equations", [(X.ch("in_s11p", "motion-in-a-straight-line", 2), 10), (X.ch("al_phys", "mechanics-and-materials", 2, 12), 10)]),
               ("Free fall", [(X.ch("in_s11p", "motion-in-a-straight-line", 3), 12), (X.gen(G + "phys_motion_and_kinematics", "g_fall"), 8)]),
               ("Vectors in two dimensions", [(X.ch("in_s11p", "motion-in-a-plane", 1), 12), (X.ch("in_s11p", "motion-in-a-straight-line", 5), 8)]),
           ]),
        HU("SPH3U", "C", 12, "forces", "C3.1, C3.2, C3.3, C3.4",
           "Newton's three laws of motion; free-body diagrams and net force; mass, weight and the gravitational field strength; "
           "static and kinetic friction and the coefficient of friction; and applying forces in everyday situations.",
           "Forces", "forces",
           "Free Grade 11 Physics (SPH3U) worksheets on forces: Newton's laws, net force and free-body diagrams, weight, friction and the coefficient of friction, and action–reaction pairs. 100 questions with answers.",
           "Fnet = ma: the net force decides the acceleration.", "Friction: Ff = μFN.",
           "<p>Newton's first law: an object keeps its velocity unless a net force acts. Second law: F<sub>net</sub> = ma. "
           "Third law: forces come in pairs that are equal in size, opposite in direction and act on different objects.</p>"
           "<p>Draw a free-body diagram, add the forces as vectors and use F<sub>net</sub> = ma. Weight F<sub>g</sub> = mg with g = 9.8 N/kg on Earth. "
           "Friction opposes sliding: F<sub>f</sub> = μF<sub>N</sub>, with static friction usually larger than kinetic friction.</p>",
           [("A 1200 kg car accelerates at 2.5 m/s². Net force?", ["F = ma = 1200 × 2.5"], "3000 N"),
            ("A 20 kg box on a horizontal floor, μ<sub>k</sub> = 0.30. Kinetic friction?", ["F<sub>N</sub> = 20 × 9.8 = 196 N", "F<sub>f</sub> = 0.30 × 196"], "58.8 N")],
           ["Thinking a moving object needs a net force to keep moving at constant speed.", "Putting both forces of an action–reaction pair on the same object.", "Confusing mass (kg) with weight (N)."],
           [("Why do you lurch forward when a bus brakes?", "Your body keeps moving forward (inertia) while the bus slows down."),
            ("Is the normal force always equal to the weight?", "Only on flat, horizontal ground with no other vertical forces; on a ramp or in an accelerating elevator it is different.")],
           lambda X: [
               ("Newton's laws of motion", [(X.gen(G + "phys_newtons_laws_and_net_force", "g_law"), 7), (X.gen(G + "phys_newtons_laws_and_net_force", "g_fma"), 6), (X.ch("in_s11p", "laws-of-motion", 1), 7)]),
               ("Net force and free-body diagrams", [(X.gen(G + "phys_newtons_laws_and_net_force", "g_net"), 8), (X.gen("gen_sg_science_s3_dynamics", "g_state"), 6), (X.gen("gen_sg_science_s3_dynamics", "g_fm"), 6)]),
               ("Mass, weight and gravity", [(X.gen(G + "phys_newtons_laws_and_net_force", "g_weight"), 8), (X.gen("gen_sg_science_s3_dynamics", "g_wt"), 6), (X.gen("gen_sg_science_s3_dynamics", "g_mw"), 6)]),
               ("Friction", [(X.ch("in_s11p", "laws-of-motion", 3), 14), (X.gen("gen_sg_science_s3_dynamics", "g_fric"), 6)]),
               ("Forces in action", [(X.ch("in_s11p", "laws-of-motion", 4), 8), (X.gen(G + "g8_newtons_third_law", "g_pair"), 6), (X.gen("gen_uk_science_y11_forces_and_motion", "g_stop"), 6)]),
           ]),
        HU("SPH3U", "D", 13, "energy-and-society", "D3.1, D3.2, D3.3, D3.4, D3.5",
           "Work, kinetic energy and gravitational potential energy; the law of conservation of energy; power and efficiency; "
           "thermal energy and heat; and nuclear energy, half-life and energy sources for society.",
           "Energy and Society", "energy and society",
           "Free Grade 11 Physics (SPH3U) worksheets on energy: work, kinetic and potential energy, conservation of energy, power, efficiency, heat and nuclear energy. 100 questions with answers.",
           "Energy is conserved; it only changes form.", "W = FΔd, Ek = ½mv², Eg = mgΔh, P = E ÷ t.",
           "<p>Work is done when a force moves an object in the direction of the force: W = FΔd cos θ, in joules. Kinetic energy E<sub>k</sub> = ½mv² and gravitational potential energy E<sub>g</sub> = mgΔh. "
           "Without friction, mechanical energy is conserved, so the loss of E<sub>g</sub> equals the gain of E<sub>k</sub>.</p>"
           "<p>Power is the rate of energy transfer: P = E ÷ t, in watts. Efficiency = useful output energy ÷ input energy × 100%. "
           "Heat Q = mcΔT. Nuclear power stations release energy by fission; radioactive waste decays with a fixed half-life.</p>",
           [("A 2.0 kg ball falls 5.0 m from rest. Speed just before it lands (no air resistance)?", ["mgh = ½mv²", "v = √(2 × 9.8 × 5.0)"], "9.9 m/s"),
            ("A motor uses 500 J and does 400 J of useful work. Efficiency?", ["400 ÷ 500 × 100%"], "80%")],
           ["Doing work when no displacement happens (holding a heavy box still does no work).", "Doubling the speed and doubling the kinetic energy: E<sub>k</sub> goes up four times.", "Giving efficiency above 100%."],
           [("What happens to the energy lost to friction?", "It becomes thermal energy (and some sound), so the total energy is still conserved."),
            ("Why is nuclear waste a problem?", "Some products have long half-lives and stay radioactive for thousands of years.")],
           lambda X: [
               ("Work", [(X.ch("in_s11p", "work-energy-and-power", 1), 12), (X.gen(G + "g8_energy_transfer_and_motion", "g_work"), 8)]),
               ("Kinetic and potential energy", [(X.ch("in_s11p", "work-energy-and-power", 2), 10), (X.gen(G + "phys_kinetic_and_potential_energy", "g_ke"), 5), (X.gen(G + "phys_kinetic_and_potential_energy", "g_pe"), 5)]),
               ("Conservation of energy", [(X.ch("in_s11p", "work-energy-and-power", 3), 10), (X.gen(G + "phys_conservation_of_energy", "g_drop"), 5), (X.gen(G + "phys_conservation_of_energy", "g_coast"), 5)]),
               ("Power and efficiency", [(X.ch("in_s11p", "work-energy-and-power", 4), 10), (X.gen(G + "phys_energy_conversion_and_efficiency", "g_eff"), 5), (X.gen(G + "phys_energy_conversion_and_efficiency", "g_power"), 5)]),
               ("Heat and nuclear energy", [(X.gen(G + "chem_thermal_energy_and_specific_heat", "g_q"), 6), (X.gen("gen_sg_science_s3_thermal_properties_of_matter", "g_lat"), 4), (X.gen(G + "chem_nuclear_chemistry", "g_half"), 5), (X.gen(G + "chem_nuclear_chemistry", "g_ff"), 5)]),
           ]),
        HU("SPH3U", "E", 14, "waves-and-sound", "E3.1, E3.2, E3.3, E3.4, E3.5",
           "Transverse and longitudinal waves; frequency, period, wavelength and the universal wave equation; the speed of sound; "
           "interference, standing waves and resonance in strings and air columns; beats and the Doppler effect.",
           "Waves and Sound", "waves and sound",
           "Free Grade 11 Physics (SPH3U) worksheets on waves and sound: wave properties, the wave equation, the speed of sound, echoes, interference, standing waves, resonance in air columns and beats. 100 questions with answers.",
           "v = fλ for every wave.", "Speed of sound in air ≈ 332 + 0.6T m/s.",
           "<p>A wave carries energy without carrying matter. Transverse waves vibrate at right angles to the direction of travel; longitudinal waves (like sound) vibrate along it. "
           "The universal wave equation is v = fλ, and the period T = 1 ÷ f.</p>"
           "<p>The speed of sound in air is about 332 m/s at 0 °C and rises by about 0.6 m/s for each degree. "
           "When waves overlap they interfere; standing waves form in strings and air columns at resonant frequencies. Two close frequencies give beats at f<sub>beat</sub> = |f₁ − f₂|.</p>",
           [("A wave has f = 50 Hz and λ = 4.0 m. Speed?", ["v = fλ = 50 × 4.0"], "200 m/s"),
            ("Two tuning forks: 440 Hz and 444 Hz. Beat frequency?", ["|444 − 440|"], "4 Hz")],
           ["Thinking a higher frequency means a faster wave in the same medium: the wavelength gets shorter instead.", "Forgetting to halve the time for an echo (the sound goes there and back).", "Saying sound can travel through a vacuum."],
           [("Why does sound travel faster in warm air?", "The air particles move faster, so they pass the vibration on more quickly."),
            ("What is resonance?", "A large vibration that happens when something is pushed at its natural frequency.")],
           lambda X: [
               ("Wave properties", [(X.gen(G + "phys_wave_properties", "g_vfl"), 6), (X.gen(G + "phys_wave_properties", "g_period"), 5), (X.ch("in_s11p", "waves", 1), 9)]),
               ("Sound and echoes", [(X.gen("gen_sg_science_s3_general_wave_properties", "g_echo"), 6), (X.gen("gen_sg_science_s3_general_wave_properties", "g_med"), 4), (X.ch("in_s11p", "waves", 3), 10)]),
               ("Interference and standing waves", [(X.ch("in_s11p", "waves", 2), 10), (X.ch("al_phys", "waves-and-optics", 3, 12), 10)]),
               ("Resonance in air columns", [(X.ch("in_s11p", "waves", 4), 14), (X.gen(G + "phys_wave_technologies", "g_echo"), 6)]),
               ("Beats and wave technology", [(X.ch("in_s11p", "waves", 5), 12), (X.gen(G + "phys_wave_technologies", "g_time"), 4), (X.gen(G + "phys_wave_technologies", "g_dev"), 4)]),
           ]),
        HU("SPH3U", "F", 15, "electricity-and-magnetism", "F3.1, F3.2, F3.3, F3.4, F3.5",
           "Electric current, potential difference and resistance; Ohm's law; series and parallel circuits and Kirchhoff's laws; electrical power and energy; "
           "magnetic fields, the motor principle, electromagnetic induction and transformers.",
           "Electricity and Magnetism", "electricity and magnetism",
           "Free Grade 11 Physics (SPH3U) worksheets on electricity and magnetism: current and charge, Ohm's law, series and parallel circuits, power, magnetic fields, the motor principle, induction and transformers. 100 questions with answers.",
           "Ohm's law: V = IR.", "Series: currents equal, voltages add. Parallel: voltages equal, currents add.",
           "<p>Current I = Q ÷ t (amperes); potential difference V = E ÷ Q (volts); resistance R = V ÷ I (ohms). "
           "In series, R<sub>T</sub> = R₁ + R₂ + …; in parallel, 1/R<sub>T</sub> = 1/R₁ + 1/R₂ + …. Kirchhoff: current in = current out at a junction; voltage gains = voltage drops around a loop.</p>"
           "<p>A current makes a magnetic field (right-hand rule). A current-carrying wire in a magnetic field feels a force — the motor principle. "
           "A changing magnetic field induces a current (Faraday, Lenz). A transformer changes voltage: V<sub>s</sub>/V<sub>p</sub> = N<sub>s</sub>/N<sub>p</sub>.</p>",
           [("A 12 V battery drives 0.50 A through a lamp. Resistance?", ["R = V ÷ I = 12 ÷ 0.50"], "24 Ω"),
            ("Two 6 Ω resistors in parallel. Total resistance?", ["1/R = 1/6 + 1/6"], "3 Ω")],
           ["Adding parallel resistances like series ones.", "Thinking current is used up by a lamp: the same current leaves it.", "Thinking a transformer works with direct current."],
           [("Why are homes wired in parallel?", "Each device gets the full voltage and can be switched on or off without affecting the others."),
            ("What does Lenz's law say?", "An induced current flows so that its magnetic field opposes the change that caused it.")],
           lambda X: [
               ("Current, charge and potential difference", [(X.ch("al_phys", "electricity", 1, 12), 10), (X.gen("gen_sg_science_s4_current_of_electricity", "g_q"), 5), (X.gen("gen_sg_science_s4_current_of_electricity", "g_w"), 5)]),
               ("Ohm's law and resistance", [(X.gen("gen_sg_science_s4_current_of_electricity", "g_vir"), 8), (X.gen("gen_sg_science_s4_current_of_electricity", "g_rho"), 4), (X.ch("al_phys", "electricity", 2, 12), 8)]),
               ("Series and parallel circuits", [(X.ch("al_phys", "electricity", 3, 12), 12), (X.gen("gen_sg_science_s4_dc_circuits", "g_par"), 4), (X.gen("gen_sg_science_s4_dc_circuits", "g_mix"), 4)]),
               ("Magnetic fields and the motor principle", [(X.gen("gen_sg_science_s4_electromagnetism", "g_flem"), 7), (X.gen("gen_sg_science_s4_electromagnetism", "g_grip"), 3), (X.gen("gen_uk_science_y11_magnetism_and_electromagnetism", "g_pole"), 5), (X.gen("gen_uk_science_y11_magnetism_and_electromagnetism", "g_bil"), 5)]),
               ("Induction and transformers", [(X.gen("gen_sg_science_s4_electromagnetic_induction", "g_tf"), 8), (X.gen("gen_sg_science_s4_electromagnetic_induction", "g_lenz"), 4), (X.ch("in_s12p", "electromagnetic-induction", 2), 8)]),
           ]),
    ]
