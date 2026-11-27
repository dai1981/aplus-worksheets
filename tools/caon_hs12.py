# -*- coding: utf-8 -*-
"""Ontario Grade 12 science: SBI4U Biology, SCH4U Chemistry, SPH4U Physics (2008). Built with caon_hs."""
from caon_hs import HU

G = "gen_us_science_"


def _rel(X):
    import au_sr12p
    return au_sr12p.rel_makers(X.R)


def UNITS():
    return [
        # ---------------- SBI4U Biology ----------------
        HU("SBI4U", "B", 1, "biochemistry", "B3.1, B3.2, B3.3, B3.4, B3.5",
           "The structure and function of carbohydrates, lipids, proteins and nucleic acids; functional groups; dehydration synthesis and hydrolysis; "
           "enzymes and the factors that affect them; and the structure of the cell membrane and transport across it.",
           "Biochemistry", "biochemistry",
           "Free Grade 12 Biology (SBI4U) worksheets on biochemistry: carbohydrates, lipids, proteins, nucleic acids, functional groups, enzymes, the fluid mosaic model and membrane transport. 100 questions with answers.",
           "Large biological molecules are built by dehydration synthesis and broken by hydrolysis.", "Enzymes lower the activation energy and are specific to their substrate.",
           "<p>The four groups of macromolecules are carbohydrates (monosaccharides such as glucose), lipids (fatty acids and glycerol), proteins (amino acids joined by peptide bonds) "
           "and nucleic acids (nucleotides). Joining monomers releases water (dehydration synthesis); breaking them apart uses water (hydrolysis).</p>"
           "<p>An enzyme's active site fits its substrate. High temperature or the wrong pH changes its shape (denaturation). "
           "The cell membrane is a phospholipid bilayer with proteins (the fluid mosaic model); small non-polar molecules diffuse through it, while ions need channels or pumps.</p>",
           [("How many water molecules are released when 4 glucose molecules join in a chain?", ["Each new bond releases one water molecule."], "3"),
            ("Why does an enzyme stop working at 70 °C?", ["Heat breaks the bonds that hold its shape."], "it is denatured: the active site changes shape")],
           ["Saying enzymes are used up in a reaction.", "Thinking denaturation means the enzyme is killed: proteins are not alive.", "Mixing up active transport (uses ATP) and facilitated diffusion (no ATP)."],
           [("What makes a fat saturated?", "Its fatty-acid chains have only single C–C bonds, so they hold the most hydrogen and pack tightly."),
            ("What is a competitive inhibitor?", "A molecule that fits the active site and blocks the substrate.")],
           lambda X: [
               ("Carbohydrates and lipids", [(X.ch("al_bio", "biological-molecules", 1, 12), 10), (X.ch("in_s11b", "biomolecules", 1), 10)]),
               ("Proteins and nucleic acids", [(X.ch("al_bio", "biological-molecules", 2, 12), 8), (X.ch("in_s11b", "biomolecules", 2), 6), (X.ch("in_s11b", "biomolecules", 3), 6)]),
               ("Enzymes", [(X.ch("in_s11b", "biomolecules", 4), 14), (X.ch("al_bio", "biological-molecules", 4, 12), 6)]),
               ("Functional groups and reactions", [(X.gen(G + "bio_carbon_and_macromolecules", "g_mono"), 7), (X.gen(G + "bio_carbon_and_macromolecules", "g_dehyd"), 8), (X.gen(G + "bio_carbon_and_macromolecules", "g_ex"), 5)]),
               ("Membranes and transport", [(X.ch("al_bio", "cells-and-the-immune-system", 3, 12), 10), (X.gen("gen_sg_science_s3_movement_of_substances", "g_sav"), 5), (X.gen("gen_sg_science_s3_movement_of_substances", "g_pct"), 5)]),
           ]),
        HU("SBI4U", "C", 2, "metabolic-processes", "C3.1, C3.2, C3.3, C3.4, C3.5",
           "Energy and ATP; the stages of aerobic cellular respiration (glycolysis, the Krebs cycle, the electron transport chain and chemiosmosis); "
           "anaerobic respiration and fermentation; and the light-dependent and light-independent reactions of photosynthesis.",
           "Metabolic Processes", "metabolic processes",
           "Free Grade 12 Biology (SBI4U) worksheets on metabolic processes: ATP, glycolysis, the Krebs cycle, the electron transport chain, fermentation, and the light reactions and Calvin cycle of photosynthesis. 100 questions with answers.",
           "Cellular respiration releases energy from glucose; photosynthesis stores it.", "Glycolysis → Krebs cycle → electron transport chain.",
           "<p>Aerobic respiration: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy (about 36 ATP). Glycolysis in the cytoplasm splits glucose into two pyruvate (net 2 ATP). "
           "In the mitochondria, the Krebs cycle releases CO₂ and loads NADH and FADH₂; the electron transport chain pumps H⁺ ions, and ATP synthase makes most of the ATP. Oxygen is the final electron acceptor.</p>"
           "<p>Without oxygen, cells use fermentation (lactate in muscles, ethanol and CO₂ in yeast) and make only 2 ATP per glucose. "
           "Photosynthesis: the light reactions in the thylakoids split water, release O₂ and make ATP and NADPH; the Calvin cycle in the stroma uses them to fix CO₂ into sugar.</p>",
           [("Where does glycolysis happen?", ["It is the first stage and does not need mitochondria."], "in the cytoplasm"),
            ("What is the role of oxygen in respiration?", ["It accepts electrons at the end of the chain."], "final electron acceptor, forming water")],
           ["Thinking plants do not respire: plant cells respire all the time.", "Saying the oxygen released in photosynthesis comes from CO₂: it comes from water.", "Thinking fermentation makes as much ATP as aerobic respiration."],
           [("Why is the electron transport chain important?", "It makes most of the ATP by pumping H⁺ ions that then flow back through ATP synthase."),
            ("What does the Calvin cycle need from the light reactions?", "ATP and NADPH.")],
           lambda X: [
               ("Energy and ATP", [(X.gen(G + "bio_cellular_respiration", "g_atp"), 6), (X.gen(G + "bio_cellular_respiration", "g_ratio"), 6), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 2, 13), 8)]),
               ("Glycolysis and the Krebs cycle", [(X.ch("in_s11b", "respiration-in-plants", 1), 10), (X.ch("in_s11b", "respiration-in-plants", 2), 10)]),
               ("Electron transport and fermentation", [(X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 3, 13), 6), (X.gen(G + "bio_cellular_respiration", "g_ferm"), 4), (X.gen(G + "bio_cellular_respiration", "g_yeast"), 4), (X.ch("in_s11b", "respiration-in-plants", 4), 6)]),
               ("The light reactions", [(X.ch("in_s11b", "photosynthesis-in-higher-plants", 1), 6), (X.ch("in_s11b", "photosynthesis-in-higher-plants", 2), 8), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 1, 13), 6)]),
               ("The Calvin cycle and photorespiration", [(X.ch("in_s11b", "photosynthesis-in-higher-plants", 3), 10), (X.gen(G + "bio_photosynthesis", "g_stage"), 5), (X.gen(G + "bio_photosynthesis", "g_io"), 5)]),
           ]),
        HU("SBI4U", "D", 3, "molecular-genetics", "D3.1, D3.2, D3.3, D3.4, D3.5",
           "The structure of DNA and the experiments that found it; DNA replication; transcription and translation; the genetic code; "
           "mutations; gene regulation; and genetic engineering and biotechnology.",
           "Molecular Genetics", "molecular genetics",
           "Free Grade 12 Biology (SBI4U) worksheets on molecular genetics: DNA structure, replication, transcription, translation, the genetic code, mutations, gene regulation and biotechnology. 100 questions with answers.",
           "DNA → mRNA → protein.", "A pairs with T (U in RNA); G pairs with C.",
           "<p>DNA is a double helix of nucleotides; the strands are antiparallel and held by hydrogen bonds between A–T and G–C. "
           "Replication is semi-conservative: helicase unwinds the helix and DNA polymerase builds new strands 5′ to 3′ (leading strand continuously, lagging strand in Okazaki fragments).</p>"
           "<p>In transcription, RNA polymerase copies a gene into mRNA. In translation, ribosomes read the mRNA in codons of three bases and tRNA brings the matching amino acids. "
           "Mutations change the base sequence: a substitution may change one amino acid, while an insertion or deletion shifts the reading frame.</p>",
           [("DNA strand: 3′-TAC GGA-5′. mRNA?", ["Pair each base; U replaces T."], "5′-AUG CCU-3′"),
            ("A DNA sample is 30% A. What percent is G?", ["T = 30%, so A + T = 60%", "G + C = 40%, G = 20%"], "20%")],
           ["Pairing A with U in DNA.", "Forgetting that the two strands run in opposite directions.", "Thinking every mutation is harmful: many are silent."],
           [("Why is replication called semi-conservative?", "Each new DNA molecule has one old strand and one new strand."),
            ("What is a frameshift mutation?", "An insertion or deletion that changes how all the following codons are read.")],
           lambda X: [
               ("DNA structure", [(X.ch("in_s12b", "molecular-basis-of-inheritance", 1), 10), (X.gen(G + "bio_dna_and_protein_synthesis", "g_comp"), 5), (X.gen("gen_sg_science_s4_molecular_genetics", "g_pct"), 5)]),
               ("DNA replication", [(X.ch("in_s12b", "molecular-basis-of-inheritance", 3), 12), (X.ch("in_s12b", "molecular-basis-of-inheritance", 2), 8)]),
               ("Transcription and translation", [(X.ch("in_s12b", "molecular-basis-of-inheritance", 4), 10), (X.gen(G + "bio_dna_and_protein_synthesis", "g_mrna"), 5), (X.gen(G + "bio_dna_and_protein_synthesis", "g_trans"), 5)]),
               ("Mutations and gene regulation", [(X.gen(G + "bio_dna_and_protein_synthesis", "g_mut"), 5), (X.gen(G + "bio_dna_and_protein_synthesis", "g_sub"), 3), (X.ch("in_s12b", "molecular-basis-of-inheritance", 5), 6), (X.ch("al_bio", "gene-expression-and-biotechnology", 2, 13), 6)]),
               ("Biotechnology", [(X.ch("al_bio", "gene-expression-and-biotechnology", 3, 13), 6), (X.ch("al_bio", "gene-expression-and-biotechnology", 4, 13), 6), (X.ch("al_bio", "gene-expression-and-biotechnology", 5, 13), 8)]),
           ]),
        HU("SBI4U", "E", 4, "homeostasis", "E3.1, E3.2, E3.3, E3.4, E3.5",
           "Negative and positive feedback; thermoregulation; the endocrine system and hormones; the control of blood glucose; "
           "the nervous system, nerve impulses and synapses; and the kidney, water balance and excretion.",
           "Homeostasis", "homeostasis",
           "Free Grade 12 Biology (SBI4U) worksheets on homeostasis: feedback loops, temperature control, hormones, blood glucose, nerve impulses, synapses and the kidney. 100 questions with answers.",
           "Negative feedback brings a variable back to its set point.", "Hormones act slowly and widely; nerves act fast and locally.",
           "<p>Homeostasis keeps the internal environment stable. In a negative feedback loop, a receptor detects a change, a control centre (often the hypothalamus) responds, "
           "and an effector reverses the change. Positive feedback (such as contractions during birth) increases the change until an end point.</p>"
           "<p>Insulin lowers blood glucose and glucagon raises it. ADH makes the kidney collecting ducts reabsorb more water. "
           "A nerve impulse is an action potential: Na⁺ rushes in (depolarization), then K⁺ flows out (repolarization); at a synapse, neurotransmitters cross the gap.</p>",
           [("Blood glucose rises after a meal. Which hormone is released?", ["The pancreas responds to high glucose."], "insulin"),
            ("A person is dehydrated. What happens to ADH and urine?", ["More ADH, more water reabsorbed"], "ADH rises and urine is more concentrated")],
           ["Saying insulin turns glucose into energy: it makes cells take up glucose and store it as glycogen.", "Calling a fever a positive feedback loop.", "Thinking impulses jump across a synapse electrically."],
           [("What is the role of the hypothalamus?", "It is the control centre for temperature and water balance, and it links the nervous and endocrine systems."),
            ("What does the nephron do?", "It filters blood, reabsorbs useful substances and water, and makes urine.")],
           lambda X: [
               ("Feedback and temperature control", [(X.gen(G + "bio_homeostasis_and_feedback", "g_temp"), 4), (X.gen(G + "bio_homeostasis_and_feedback", "g_loop"), 6), (X.gen("gen_sg_science_s4_homeostasis_coordination_and_response", "g_skin"), 6), (X.ch("al_bio", "response-and-homeostasis", 5, 13), 4)]),
               ("The endocrine system", [(X.ch("in_s11b", "chemical-coordination-and-integration", 1), 8), (X.ch("in_s11b", "chemical-coordination-and-integration", 2), 6), (X.ch("in_s11b", "chemical-coordination-and-integration", 3), 6)]),
               ("Blood glucose", [(X.ch("al_bio", "response-and-homeostasis", 3, 13), 10), (X.gen("gen_sg_science_s4_homeostasis_coordination_and_response", "g_glu"), 5), (X.ch("al_bio", "response-and-homeostasis", 5, 13), 5)]),
               ("Nerve impulses and synapses", [(X.ch("al_bio", "response-and-homeostasis", 1, 13), 8), (X.ch("al_bio", "response-and-homeostasis", 2, 13), 6), (X.ch("in_s11b", "neural-control-and-coordination", 1), 6)]),
               ("The kidney and water balance", [(X.ch("in_s11b", "excretory-products-and-their-elimination", 2), 8), (X.ch("al_bio", "response-and-homeostasis", 4, 13), 6), (X.gen("gen_sg_science_s4_excretion_in_humans", "g_adh"), 3), (X.gen("gen_sg_science_s4_excretion_in_humans", "g_where"), 3)]),
           ]),
        HU("SBI4U", "F", 5, "population-dynamics", "F3.1, F3.2, F3.3, F3.4, F3.5",
           "Population size, density and distribution; birth, death, immigration and emigration; exponential and logistic growth; carrying capacity and limiting factors; "
           "interactions between species; and the human population and sustainability.",
           "Population Dynamics", "population dynamics",
           "Free Grade 12 Biology (SBI4U) worksheets on population dynamics: density, mark–recapture, growth rates, exponential and logistic growth, carrying capacity, species interactions and the human population. 100 questions with answers.",
           "Population change = (births + immigration) − (deaths + emigration).", "Logistic growth levels off at the carrying capacity.",
           "<p>Population density = number of individuals ÷ area. The mark–recapture estimate is N = (number marked × number caught the second time) ÷ number recaptured with marks. "
           "A population grows when births and immigration are greater than deaths and emigration.</p>"
           "<p>With unlimited resources, a population grows exponentially (a J-shaped curve). Limiting factors such as food, space and disease slow growth, "
           "giving a logistic, S-shaped curve that levels off at the carrying capacity. Density-dependent factors (competition, disease) get stronger as the population grows.</p>",
           [("50 deer are tagged. Later 40 are caught and 10 have tags. Estimate the population.", ["N = 50 × 40 ÷ 10"], "200 deer"),
            ("A town of 2000 has 60 births, 20 deaths, 10 immigrants and 30 emigrants in a year. Change?", ["(60 + 10) − (20 + 30)"], "+20")],
           ["Thinking carrying capacity never changes: it changes when the environment does.", "Calling a predator–prey relationship mutualism.", "Forgetting immigration and emigration in population change."],
           [("What is a density-independent factor?", "A factor such as a flood or frost that affects a population whatever its density."),
            ("Why do predator and prey numbers rise and fall in cycles?", "More prey feeds more predators; more predators then reduce the prey, so the predators fall too.")],
           lambda X: [
               ("Population size and density", [(X.ch("in_s12b", "organisms-and-populations", 1), 10), (X.gen(G + "bio_populations_and_carrying_capacity", "g_density"), 5), (X.gen(G + "bio_populations_and_carrying_capacity", "g_mark"), 5)]),
               ("Population growth", [(X.ch("in_s12b", "organisms-and-populations", 2), 8), (X.gen(G + "bio_populations_and_carrying_capacity", "g_change"), 4), (X.gen(G + "bio_populations_and_carrying_capacity", "g_double"), 4), (X.gen(G + "bio_populations_and_carrying_capacity", "g_logistic"), 4)]),
               ("Carrying capacity and limiting factors", [(X.gen(G + "bio_populations_and_carrying_capacity", "g_fact"), 6), (X.gen(G + "g7_resources_and_populations", "g_graph"), 4), (X.gen(G + "g7_resources_and_populations", "g_limit"), 4), (X.gen("gen_uk_science_y11_ecology", "g_factor"), 6)]),
               ("Interactions between species", [(X.ch("in_s12b", "organisms-and-populations", 4), 10), (X.gen(G + "g7_interactions_in_ecosystems", "g_kind"), 5), (X.gen(G + "g7_interactions_in_ecosystems", "g_which"), 5)]),
               ("Human population and sustainability", [(X.gen(G + "ess_sustainability_and_human_impact", "g_pop"), 5), (X.gen(G + "ess_sustainability_and_human_impact", "g_fish"), 4), (X.gen(G + "ess_sustainability_and_human_impact", "g_foot"), 3), (X.ch("in_s12b", "ecosystem", 4), 8)]),
           ]),
        # ---------------- SCH4U Chemistry ----------------
        HU("SCH4U", "B", 6, "organic-chemistry", "B3.1, B3.2, B3.3, B3.4",
           "Naming and drawing hydrocarbons (alkanes, alkenes, alkynes, aromatics); functional groups (alcohols, aldehydes, ketones, carboxylic acids, esters, ethers, amines, amides); "
           "isomers; addition, substitution, condensation, combustion and polymerization reactions.",
           "Organic Chemistry", "organic chemistry",
           "Free Grade 12 Chemistry (SCH4U) worksheets on organic chemistry: naming hydrocarbons, functional groups, alcohols, aldehydes, ketones, carboxylic acids, esters, amines, isomers and organic reactions. 100 questions with answers.",
           "The functional group decides the family and most of the properties.", "Name from the longest chain; number from the end nearest the functional group.",
           "<p>Alkanes (C<sub>n</sub>H<sub>2n+2</sub>) have only single bonds, alkenes have a C=C double bond and alkynes a C≡C triple bond. "
           "Prefixes give the chain length: meth-, eth-, prop-, but-, pent-, hex-. Number the chain so the double bond or functional group gets the lowest number.</p>"
           "<p>Functional groups: –OH (alcohol, -ol), –CHO (aldehyde, -al), C=O in the chain (ketone, -one), –COOH (carboxylic acid, -oic acid), –COO– (ester, -oate), –NH₂ (amine). "
           "Alkenes undergo addition; an alcohol and an acid form an ester and water (condensation); many small monomers join into polymers.</p>",
           [("Name CH₃CH₂CH₂OH.", ["Three carbons: prop-", "–OH on carbon 1"], "propan-1-ol (1-propanol)"),
            ("Ethanoic acid + methanol → ?", ["Acid + alcohol → ester + water"], "methyl ethanoate and water")],
           ["Counting the longest chain wrongly when it bends on the page.", "Mixing up aldehydes (C=O at the end) and ketones (C=O inside the chain).", "Naming the ester with the acid part first: the alcohol part comes first (methyl ethanoate)."],
           [("What are isomers?", "Compounds with the same molecular formula but a different arrangement of atoms."),
            ("Why do alcohols have higher boiling points than alkanes of similar size?", "The –OH group forms hydrogen bonds between molecules.")],
           lambda X: [
               ("Naming hydrocarbons", [(X.ch("in_s11c", "hydrocarbons", 1), 8), (X.ch("al_chem", "organic-chemistry-alkanes-alkenes-and-alcohols", 1, 12), 6), (X.gen("gen_sg_science_s4_organic_chemistry", "g_series"), 6)]),
               ("Functional groups", [(X.ch("in_s11c", "organic-chemistry-some-basic-principles-and-techniques", 2), 10), (X.ch("al_chem", "organic-chemistry-alkanes-alkenes-and-alcohols", 4, 12), 10)]),
               ("Alcohols, aldehydes and ketones", [(X.ch("in_s12c", "alcohols-phenols-and-ethers", 1), 6), (X.ch("in_s12c", "aldehydes-ketones-and-carboxylic-acids", 1), 6), (X.ch("al_chem", "further-organic-chemistry-and-analysis", 2, 13), 8)]),
               ("Acids, esters and amines", [(X.ch("in_s12c", "aldehydes-ketones-and-carboxylic-acids", 4), 6), (X.ch("al_chem", "further-organic-chemistry-and-analysis", 1, 13), 8), (X.ch("in_s12c", "amines", 1), 6)]),
               ("Isomers, reactions and polymers", [(X.ch("al_chem", "organic-chemistry-alkanes-alkenes-and-alcohols", 5, 12), 8), (X.gen("gen_sg_science_s4_organic_chemistry", "g_poly"), 4), (X.gen("gen_sg_science_s4_organic_chemistry", "g_ester"), 4), (X.ch("in_s11c", "organic-chemistry-some-basic-principles-and-techniques", 3), 4)]),
           ]),
        HU("SCH4U", "C", 7, "structure-and-properties-of-matter", "C3.1, C3.2, C3.3, C3.4, C3.5",
           "The development of the atomic model; the quantum mechanical model, quantum numbers and orbitals; electron configurations; "
           "VSEPR theory and molecular shapes; hybridization; polarity, intermolecular forces and the properties of ionic, molecular, covalent network and metallic solids.",
           "Structure and Properties of Matter", "structure and properties of matter",
           "Free Grade 12 Chemistry (SCH4U) worksheets on the structure of matter: the quantum mechanical model, quantum numbers, electron configurations, VSEPR shapes, hybridization, polarity and types of solids. 100 questions with answers.",
           "Electrons fill orbitals in order of energy: 1s 2s 2p 3s 3p 4s 3d.", "VSEPR: electron pairs spread out as far as possible.",
           "<p>The quantum mechanical model describes electrons by four quantum numbers (n, l, m<sub>l</sub>, m<sub>s</sub>). "
           "Orbitals fill from lowest energy (aufbau principle), each holds two electrons of opposite spin (Pauli), and electrons spread out singly before pairing (Hund).</p>"
           "<p>VSEPR theory predicts shape from the number of bonding and lone pairs around the central atom: 4 bonding pairs give a tetrahedral shape (109.5°), 3 bonding pairs and 1 lone pair a trigonal pyramidal shape (107°), "
           "2 bonding and 2 lone pairs a bent shape (104.5°). A molecule with polar bonds is polar only if the dipoles do not cancel.</p>",
           [("Electron configuration of sulfur (Z = 16)?", ["Fill 1s 2s 2p 3s 3p"], "1s² 2s² 2p⁶ 3s² 3p⁴"),
            ("Shape of NH₃?", ["3 bonding pairs, 1 lone pair"], "trigonal pyramidal")],
           ["Filling 3d before 4s.", "Calling CO₂ polar because its bonds are polar: the linear shape cancels the dipoles.", "Forgetting lone pairs when choosing a molecular shape."],
           [("What is hybridization?", "Mixing atomic orbitals to make equal new orbitals, such as the four sp³ orbitals of carbon in methane."),
            ("Why do network solids like diamond have very high melting points?", "Every atom is held by strong covalent bonds in a giant structure.")],
           lambda X: [
               ("The quantum mechanical model", [(X.ch("in_s11c", "structure-of-atom", 2), 6), (X.ch("in_s11c", "structure-of-atom", 4), 6), (X.ch("in_s11c", "structure-of-atom", 5), 8)]),
               ("Electron configurations", [(X.ch("al_chem", "atomic-structure-and-amount-of-substance", 1, 12), 10), (X.ch("in_s12c", "the-d-and-f-block-elements", 2), 10)]),
               ("VSEPR shapes", [(X.ch("in_s11c", "chemical-bonding-and-molecular-structure", 2), 10), (X.ch("al_chem", "bonding-and-energetics", 1, 12), 10)]),
               ("Bond angles and hybridization", [(X.ch("in_s11c", "chemical-bonding-and-molecular-structure", 3), 10), (X.ch("in_s11c", "chemical-bonding-and-molecular-structure", 4), 10)]),
               ("Polarity, forces and solids", [(X.ch("al_chem", "bonding-and-energetics", 2, 12), 8), (X.gen(G + "chem_molecular_structure_and_materials", "g_sp"), 4), (X.gen("gen_sg_science_s3_chemical_bonding_and_structure", "g_why"), 4), (X.gen("gen_sg_science_s3_chemical_bonding_and_structure", "g_pairs"), 4)]),
           ], allow=("units",)),
        HU("SCH4U", "D", 8, "energy-changes-and-rates-of-reaction", "D3.1, D3.2, D3.3, D3.4, D3.5",
           "Endothermic and exothermic reactions; enthalpy change; calorimetry; Hess's law and bond energies; potential-energy diagrams; "
           "collision theory, activation energy and catalysts; factors affecting rate; and rate laws.",
           "Energy Changes and Rates of Reaction", "energy changes and rates of reaction",
           "Free Grade 12 Chemistry (SCH4U) worksheets on energy changes and rates: enthalpy, calorimetry, Hess's law, bond energies, energy diagrams, collision theory, catalysts and rate laws. 100 questions with answers.",
           "ΔH is negative for exothermic reactions and positive for endothermic ones.", "Rate increases with concentration, temperature, surface area and catalysts.",
           "<p>The enthalpy change ΔH is the heat absorbed or released at constant pressure. In a calorimeter, q = mcΔT, and ΔH = −q ÷ n for the reaction. "
           "Hess's law: ΔH for a reaction is the same whatever the route, so you can add equations (and their ΔH). From bond energies, ΔH = bonds broken − bonds formed.</p>"
           "<p>Particles must collide with enough energy (the activation energy) and the right orientation. Raising the temperature, concentration or surface area increases the rate; "
           "a catalyst gives a route with a lower activation energy. A rate law has the form rate = k[A]<sup>m</sup>[B]<sup>n</sup>, with orders found by experiment.</p>",
           [("100 g of water warms by 5.0 °C in a calorimeter. Heat absorbed? (c = 4.18 J/g·°C)", ["q = 100 × 4.18 × 5.0"], "2090 J"),
            ("Doubling [A] quadruples the rate. Order with respect to A?", ["2ⁿ = 4"], "second order")],
           ["Giving an exothermic ΔH a positive sign.", "Thinking a catalyst changes ΔH: it only lowers the activation energy.", "Reading the orders of a rate law from the balanced equation."],
           [("Why does a higher temperature speed up a reaction?", "More particles have at least the activation energy and they collide more often."),
            ("What does Hess's law let you do?", "Find ΔH for a reaction that is hard to measure by combining reactions with known ΔH values.")],
           lambda X: [
               ("Enthalpy and calorimetry", [(X.ch("al_chem", "bonding-and-energetics", 3, 12), 10), (X.gen(G + "chem_thermal_energy_and_specific_heat", "g_cal"), 5), (X.gen(G + "chem_thermal_energy_and_specific_heat", "g_mix"), 5)]),
               ("Hess's law and bond energies", [(X.ch("al_chem", "bonding-and-energetics", 4, 12), 10), (X.ch("al_chem", "bonding-and-energetics", 5, 12), 10)]),
               ("Energy diagrams", [(X.gen(G + "chem_energy_in_chemical_reactions", "g_exo"), 5), (X.gen(G + "chem_energy_in_chemical_reactions", "g_diag"), 4), (X.gen(G + "chem_energy_in_chemical_reactions", "g_bond"), 5), (X.gen("gen_sg_science_s4_chemical_energetics", "g_prof"), 6)]),
               ("Collision theory and catalysts", [(X.ch("al_chem", "kinetics-and-equilibria", 1, 12), 8), (X.gen(G + "chem_reaction_rates", "g_factor"), 6), (X.gen(G + "chem_reaction_rates", "g_rate"), 6)]),
               ("Rate laws", [(X.ch("in_s12c", "chemical-kinetics", 2), 10), (X.ch("in_s12c", "chemical-kinetics", 4), 4), (X.ch("al_chem", "thermodynamics-and-rate-equations", 3, 13), 6)]),
           ]),
        HU("SCH4U", "E", 9, "chemical-systems-and-equilibrium", "E3.1, E3.2, E3.3, E3.4, E3.5",
           "Dynamic equilibrium; Le Châtelier's principle; the equilibrium constant K and ICE tables; acids and bases (Brønsted–Lowry, K<sub>a</sub>, pH and pOH); "
           "buffers; and solubility equilibria and K<sub>sp</sub>.",
           "Chemical Systems and Equilibrium", "chemical systems and equilibrium",
           "Free Grade 12 Chemistry (SCH4U) worksheets on chemical equilibrium: dynamic equilibrium, Le Châtelier's principle, equilibrium constants, ICE tables, pH and Ka, buffers and Ksp. 100 questions with answers.",
           "At equilibrium the forward and reverse rates are equal.", "Le Châtelier: a system shifts to reduce a change.",
           "<p>At equilibrium, reactants and products both remain and their concentrations stay constant. For aA + bB ⇌ cC + dD, K = [C]<sup>c</sup>[D]<sup>d</sup> ÷ ([A]<sup>a</sup>[B]<sup>b</sup>) (solids and liquids are left out). "
           "Use an ICE table (initial, change, equilibrium) to find unknown concentrations.</p>"
           "<p>Adding a reactant, removing a product or changing pressure or temperature shifts the position; only temperature changes K. "
           "pH = −log[H₃O⁺] and pH + pOH = 14 at 25 °C. A weak acid has a small K<sub>a</sub>. A buffer (a weak acid and its conjugate base) resists pH change.</p>",
           [("[H₃O⁺] = 1.0 × 10⁻³ mol/L. pH?", ["pH = −log(1.0 × 10⁻³)"], "3.0"),
            ("N₂ + 3H₂ ⇌ 2NH₃ is exothermic. The temperature is raised. Which way does it shift?", ["Heat is a product; adding it shifts away from it."], "to the left (less NH₃)")],
           ["Thinking the reaction stops at equilibrium.", "Putting solids or pure liquids in the K expression.", "Saying a catalyst shifts the equilibrium: it only gets there faster."],
           [("What does a large K mean?", "At equilibrium there are mostly products."),
            ("What is a conjugate base?", "What is left when an acid gives away a proton, such as Cl⁻ from HCl.")],
           lambda X: [
               ("Equilibrium and Le Châtelier's principle", [(X.ch("al_chem", "kinetics-and-equilibria", 2, 12), 8), (X.gen(G + "chem_chemical_equilibrium", "g_shift"), 7), (X.gen(G + "chem_chemical_equilibrium", "g_more"), 5)]),
               ("Equilibrium constants", [(X.ch("al_chem", "kinetics-and-equilibria", 3, 12), 10), (X.ch("al_chem", "kinetics-and-equilibria", 4, 12), 10)]),
               ("ICE tables", [(X.ch("al_chem", "kinetics-and-equilibria", 5, 12), 10), (X.ch("in_s11c", "equilibrium", 1), 10)]),
               ("pH, pOH and Ka", [(X.ch("al_chem", "acids-bases-and-electrode-potentials", 1, 13), 8), (X.ch("al_chem", "acids-bases-and-electrode-potentials", 2, 13), 8), (X.ch("in_s11c", "equilibrium", 4), 4)]),
               ("Buffers and solubility", [(X.ch("al_chem", "acids-bases-and-electrode-potentials", 3, 13), 10), (X.ch("in_s11c", "equilibrium", 5), 10)]),
           ]),
        HU("SCH4U", "F", 10, "electrochemistry", "F3.1, F3.2, F3.3, F3.4, F3.5",
           "Oxidation and reduction; oxidation numbers; balancing redox half-reactions; galvanic cells and standard reduction potentials; "
           "electrolytic cells and electrolysis; batteries, fuel cells and corrosion.",
           "Electrochemistry", "electrochemistry",
           "Free Grade 12 Chemistry (SCH4U) worksheets on electrochemistry: oxidation numbers, redox half-reactions, galvanic cells, standard reduction potentials, electrolysis, batteries and corrosion. 100 questions with answers.",
           "OIL RIG: oxidation is loss of electrons, reduction is gain.", "E°cell = E°cathode − E°anode.",
           "<p>Oxidation is the loss of electrons (oxidation number goes up); reduction is the gain of electrons (oxidation number goes down). "
           "To balance a redox reaction, write the two half-reactions, balance atoms and charge with electrons, and make the electrons equal.</p>"
           "<p>In a galvanic cell, a spontaneous reaction makes electricity: oxidation at the anode (−), reduction at the cathode (+), and electrons flow through the wire from anode to cathode. "
           "E°<sub>cell</sub> = E°<sub>cathode</sub> − E°<sub>anode</sub>; a positive value means spontaneous. An electrolytic cell uses electricity to drive a non-spontaneous reaction.</p>",
           [("Oxidation number of Mn in MnO₄⁻?", ["4 × (−2) = −8", "Mn − 8 = −1"], "+7"),
            ("Zn²⁺/Zn E° = −0.76 V; Cu²⁺/Cu E° = +0.34 V. E°cell?", ["Cu is reduced (cathode).", "0.34 − (−0.76)"], "+1.10 V")],
           ["Saying the anode is always positive: in a galvanic cell it is negative.", "Multiplying E° values when you multiply a half-reaction.", "Mixing up the oxidizing agent (it is reduced) and the reducing agent (it is oxidized)."],
           [("Why does iron rust faster near salt water?", "Salt water is a good electrolyte, so the redox reactions of corrosion happen faster."),
            ("What does a salt bridge do?", "It lets ions move between the half-cells so the charges stay balanced and the current keeps flowing.")],
           lambda X: [
               ("Oxidation numbers", [(X.ch("in_s11c", "redox-reactions", 2), 10), (X.ch("al_chem", "redox-and-inorganic-chemistry", 1, 12), 10)]),
               ("Redox reactions and half-reactions", [(X.ch("in_s11c", "redox-reactions", 1), 6), (X.ch("in_s11c", "redox-reactions", 4), 8), (X.ch("al_chem", "redox-and-inorganic-chemistry", 2, 12), 6)]),
               ("Galvanic cells", [(X.ch("in_s12c", "electrochemistry", 1), 10), (X.ch("al_chem", "acids-bases-and-electrode-potentials", 4, 13), 10)]),
               ("Electrolysis", [(X.ch("in_s12c", "electrochemistry", 4), 8), (X.gen("gen_uk_science_y10_chemical_changes", "g_elec"), 6), (X.gen("gen_sg_science_s4_redox_chemistry", "g_elec"), 6)]),
               ("Batteries and corrosion", [(X.ch("in_s12c", "electrochemistry", 5), 10), (X.gen("gen_sg_science_s4_redox_chemistry", "g_cell"), 5), (X.ch("in_s11c", "redox-reactions", 3), 5)]),
           ]),
        # ---------------- SPH4U Physics ----------------
        HU("SPH4U", "B", 11, "dynamics", "B3.1, B3.2, B3.3, B3.4",
           "Motion in two dimensions and projectiles; Newton's laws with free-body diagrams, inclines, friction and connected objects; "
           "uniform circular motion, centripetal acceleration and centripetal force; and frames of reference.",
           "Dynamics", "dynamics",
           "Free Grade 12 Physics (SPH4U) worksheets on dynamics: projectiles, forces on inclines, friction, pulleys and elevators, uniform circular motion and centripetal force. 100 questions with answers.",
           "Resolve forces into components and apply Fnet = ma along each direction.", "Circular motion: ac = v²/r towards the centre.",
           "<p>Treat projectile motion as two independent motions: constant horizontal velocity and a vertical acceleration of 9.8 m/s² downwards. "
           "On an incline, split the weight into mg sin θ along the slope and mg cos θ into the slope; the normal force balances mg cos θ.</p>"
           "<p>An object moving in a circle at constant speed accelerates towards the centre: a<sub>c</sub> = v²/r = 4π²r/T². "
           "The centripetal force F<sub>c</sub> = mv²/r is not a new force; it is provided by tension, friction, gravity or a normal force.</p>",
           [("A 1000 kg car rounds a curve of radius 50 m at 20 m/s. Centripetal force?", ["F = mv²/r = 1000 × 400 ÷ 50"], "8000 N"),
            ("A box slides down a frictionless 30° ramp. Acceleration?", ["a = g sin 30°"], "4.9 m/s²")],
           ["Drawing a 'centrifugal' force outwards on a free-body diagram.", "Using mg instead of mg cos θ for the normal force on a ramp.", "Letting the horizontal velocity of a projectile change."],
           [("What keeps a satellite in orbit?", "Gravity supplies the centripetal force that keeps it turning."),
            ("Why do you feel heavier in an elevator that accelerates upwards?", "The floor must push up with more than your weight to give you an upward acceleration.")],
           lambda X: [
               ("Forces in two dimensions", [(X.ch("al_phys", "mechanics-and-materials", 1, 12), 10), (X.ch("in_s11p", "laws-of-motion", 1), 10)]),
               ("Friction, pulleys and elevators", [(X.ch("in_s11p", "laws-of-motion", 3), 10), (X.ch("in_s11p", "laws-of-motion", 4), 10)]),
               ("Uniform circular motion", [(X.ch("in_s11p", "motion-in-a-plane", 4), 10), (X.ch("al_phys", "circular-motion-and-oscillations", 1, 13), 10)]),
               ("Centripetal force", [(X.ch("al_phys", "circular-motion-and-oscillations", 2, 13), 12), (X.ch("in_s11p", "laws-of-motion", 5), 8)]),
               ("Projectile motion", [(X.ch("in_s11p", "motion-in-a-plane", 2), 10), (X.ch("in_s11p", "motion-in-a-plane", 3), 10)]),
           ]),
        HU("SPH4U", "C", 12, "energy-and-momentum", "C3.1, C3.2, C3.3, C3.4",
           "Work and the work–energy theorem; kinetic, gravitational and elastic potential energy; Hooke's law; momentum and impulse; "
           "conservation of momentum in one and two dimensions; elastic and inelastic collisions.",
           "Energy and Momentum", "energy and momentum",
           "Free Grade 12 Physics (SPH4U) worksheets on energy and momentum: work, the work–energy theorem, Hooke's law and elastic energy, momentum, impulse and collisions. 100 questions with answers.",
           "Momentum is conserved in every collision; kinetic energy only in elastic ones.", "Impulse = FΔt = Δp.",
           "<p>The work–energy theorem: the net work done on an object equals its change in kinetic energy. A spring obeys Hooke's law F = kx and stores elastic energy E<sub>e</sub> = ½kx².</p>"
           "<p>Momentum p = mv is a vector. Impulse FΔt equals the change in momentum, so a longer stopping time means a smaller force (air bags, helmets). "
           "With no external force, total momentum is conserved. In an elastic collision kinetic energy is also conserved; in an inelastic collision some becomes heat and sound.</p>",
           [("A spring (k = 200 N/m) is stretched 0.10 m. Elastic energy?", ["E = ½ × 200 × 0.10²"], "1.0 J"),
            ("A 2.0 kg cart at 3.0 m/s hits and sticks to a 1.0 kg cart at rest. Final speed?", ["6.0 kg·m/s = 3.0 kg × v"], "2.0 m/s")],
           ["Forgetting that momentum has a direction (signs for opposite motions).", "Assuming kinetic energy is conserved when objects stick together.", "Using x instead of x² in elastic potential energy."],
           [("Why does an air bag reduce injury?", "It makes the stopping time longer, so the force needed to stop the person is smaller."),
            ("What is a perfectly inelastic collision?", "A collision in which the objects stick together and move as one.")],
           lambda X: [
               ("Work and energy", [(X.ch("in_s11p", "work-energy-and-power", 1), 8), (X.ch("in_s11p", "work-energy-and-power", 2), 6), (X.gen(G + "phys_kinetic_and_potential_energy", "g_work"), 6)]),
               ("Springs and elastic energy", [(X.ch("in_s11p", "mechanical-properties-of-solids", 2), 10), (X.gen(G + "phys_kinetic_and_potential_energy", "g_spring"), 6), (X.gen("gen_uk_science_y9_work_and_moments", "g_hooke"), 4)]),
               ("Momentum and impulse", [(X.ch("in_s11p", "laws-of-motion", 2), 10), (X.gen(G + "phys_impulse_and_collision_safety", "g_imp"), 5), (X.gen(G + "phys_impulse_and_collision_safety", "g_ratio"), 5)]),
               ("Collisions", [(X.ch("in_s11p", "work-energy-and-power", 5), 10), (X.gen(G + "phys_momentum_and_collisions", "g_stick"), 4), (X.gen(G + "phys_momentum_and_collisions", "g_recoil"), 3), (X.gen(G + "phys_momentum_and_collisions", "g_after"), 3)]),
               ("Momentum problems", [(X.ch("al_phys", "mechanics-and-materials", 3, 12), 12), (X.gen(G + "phys_momentum_and_collisions", "g_p"), 4), (X.gen(G + "phys_momentum_and_collisions", "g_cmp"), 4)]),
           ]),
        HU("SPH4U", "D", 13, "gravitational-electric-and-magnetic-fields", "D3.1, D3.2, D3.3, D3.4",
           "Newton's law of universal gravitation and gravitational fields; satellites and orbits; Coulomb's law; electric fields and electric potential; "
           "magnetic fields and the forces on moving charges and currents.",
           "Gravitational, Electric and Magnetic Fields", "gravitational, electric and magnetic fields",
           "Free Grade 12 Physics (SPH4U) worksheets on fields: universal gravitation, orbits, Coulomb's law, electric fields and potential, and magnetic forces on charges and currents. 100 questions with answers.",
           "Gravity and electric force both follow an inverse-square law.", "F = Gm₁m₂/r² and F = kq₁q₂/r².",
           "<p>Newton's law of universal gravitation: F = Gm₁m₂/r² with G = 6.67 × 10⁻¹¹ N·m²/kg². Doubling the distance gives a quarter of the force. "
           "For a circular orbit, gravity provides the centripetal force: Gm/r = v².</p>"
           "<p>Coulomb's law F = kq₁q₂/r² (k = 8.99 × 10⁹ N·m²/C²) has the same form, but charges can repel as well as attract. "
           "The electric field ε = F/q points the way a positive charge would move. A charge moving through a magnetic field feels F = qvB sin θ; a current feels F = BIL sin θ.</p>",
           [("Two charges are moved three times as far apart. The force becomes?", ["Inverse square: 1/3²"], "1/9 as large"),
            ("A proton (q = 1.6 × 10⁻¹⁹ C) moves at 2.0 × 10⁶ m/s at right angles to a 0.50 T field. Force?", ["F = qvB"], "1.6 × 10⁻¹³ N")],
           ["Using r as the distance from the surface instead of from the centre of a planet.", "Forgetting to square the distance.", "Thinking a magnetic field does work on a moving charge: the force is always at right angles to the motion."],
           [("Why do astronauts in orbit feel weightless?", "They and their craft are falling around Earth together, with gravity giving the centripetal acceleration."),
            ("What is electric potential?", "The electric potential energy per unit charge at a point, in volts.")],
           lambda X: [
               ("Universal gravitation", [(X.ch("al_phys", "gravitational-and-electric-fields", 1, 13), 10), (X.ch("in_s11p", "gravitation", 2), 10)]),
               ("Satellites and orbits", [(X.ch("al_phys", "gravitational-and-electric-fields", 2, 13), 10), (X.ch("in_s11p", "gravitation", 4), 10)]),
               ("Coulomb's law", [(X.ch("in_s12p", "electric-charges-and-fields", 2), 10), (X.ch("al_phys", "gravitational-and-electric-fields", 3, 13), 10)]),
               ("Electric fields and potential", [(X.ch("in_s12p", "electric-charges-and-fields", 3), 8), (X.ch("in_s12p", "electrostatic-potential-and-capacitance", 1), 6), (X.ch("al_phys", "gravitational-and-electric-fields", 4, 13), 6)]),
               ("Magnetic forces", [(X.ch("in_s12p", "moving-charges-and-magnetism", 1), 10), (X.ch("in_s12p", "moving-charges-and-magnetism", 2), 6), (X.ch("al_phys", "capacitors-and-magnetic-fields", 3, 13), 4)]),
           ]),
        HU("SPH4U", "E", 14, "the-wave-nature-of-light", "E3.1, E3.2, E3.3, E3.4, E3.5",
           "Refraction, Snell's law and total internal reflection; Huygens' principle; diffraction; Young's double-slit experiment; "
           "interference in diffraction gratings and thin films; polarization; and the electromagnetic spectrum.",
           "The Wave Nature of Light", "the wave nature of light",
           "Free Grade 12 Physics (SPH4U) worksheets on the wave nature of light: refraction, Snell's law, diffraction, Young's double slits, diffraction gratings, polarization and the electromagnetic spectrum. 100 questions with answers.",
           "Interference and diffraction show that light is a wave.", "Double slit: bright fringes where d sin θ = mλ.",
           "<p>Light slows down in a denser medium: n = c/v and n₁ sin θ₁ = n₂ sin θ₂. When light goes from a denser to a less dense medium at more than the critical angle, it is totally internally reflected.</p>"
           "<p>Huygens' principle treats every point on a wavefront as a source of wavelets, which explains diffraction. In Young's experiment, bright fringes (constructive interference) appear where the path difference is a whole number of wavelengths: "
           "d sin θ = mλ, and the fringe spacing is Δy = λL/d. A diffraction grating with many slits gives sharp, bright maxima. Polarization shows that light is a transverse wave.</p>",
           [("Light goes from air into glass (n = 1.50) at 30°. Angle of refraction?", ["sin θ₂ = sin 30° ÷ 1.50 = 0.333"], "19.5°"),
            ("λ = 600 nm, d = 0.20 mm, L = 2.0 m. Fringe spacing?", ["Δy = 600 × 10⁻⁹ × 2.0 ÷ 0.20 × 10⁻³"], "6.0 mm")],
           ["Measuring angles from the surface instead of from the normal.", "Thinking a wider slit spacing gives wider fringes: it gives narrower ones.", "Saying sound can be polarized: only transverse waves can."],
           [("Why was Young's experiment important?", "The interference pattern could only be explained if light behaves as a wave."),
            ("What causes the colours in a soap bubble?", "Thin-film interference between light reflected from the front and the back of the film.")],
           lambda X: [
               ("Refraction and total internal reflection", [(X.ch("al_phys", "waves-and-optics", 2, 12), 10), (X.gen("gen_sg_science_s3_light", "g_snell"), 5), (X.gen("gen_sg_science_s3_light", "g_crit"), 5)]),
               ("Huygens' principle and diffraction", [(X.ch("in_s12p", "wave-optics", 1), 8), (X.ch("in_s12p", "wave-optics", 4), 12)]),
               ("Young's double-slit experiment", [(X.ch("al_phys", "waves-and-optics", 4, 12), 10), (X.ch("in_s12p", "wave-optics", 2), 10)]),
               ("Interference and diffraction gratings", [(X.ch("al_phys", "waves-and-optics", 5, 12), 10), (X.ch("in_s12p", "wave-optics", 3), 10)]),
               ("Polarization and the electromagnetic spectrum", [(X.ch("in_s12p", "wave-optics", 5), 6), (X.ch("in_s12p", "electromagnetic-waves", 4), 8), (X.gen("gen_sg_science_s3_electromagnetic_spectrum", "g_order"), 6)]),
           ]),
        HU("SPH4U", "F", 15, "revolutions-in-modern-physics", "F3.1, F3.2, F3.3, F3.4, F3.5",
           "Photons and the photoelectric effect; wave–particle duality and de Broglie wavelength; the postulates of special relativity, "
           "time dilation, length contraction and mass–energy equivalence; and the standard model of elementary particles.",
           "Revolutions in Modern Physics", "modern physics",
           "Free Grade 12 Physics (SPH4U) worksheets on modern physics: photons, the photoelectric effect, de Broglie wavelength, special relativity, time dilation, length contraction, E = mc² and the standard model. 100 questions with answers.",
           "Light comes in photons of energy E = hf.", "Moving clocks run slow: Δt = γΔt₀.",
           "<p>A photon has energy E = hf = hc/λ (h = 6.63 × 10⁻³⁴ J·s). In the photoelectric effect, a photon frees an electron only if hf is at least the work function: E<sub>k,max</sub> = hf − W. "
           "Particles also behave as waves with de Broglie wavelength λ = h/p.</p>"
           "<p>Special relativity: the laws of physics are the same in every inertial frame and light travels at c for every observer. "
           "So moving clocks run slow (Δt = γΔt₀), moving lengths contract (L = L₀/γ), with γ = 1/√(1 − v²/c²), and mass is a form of energy (E = mc²). "
           "The standard model builds matter from quarks and leptons, with forces carried by bosons.</p>",
           [("Energy of a photon of frequency 5.0 × 10¹⁴ Hz?", ["E = hf = 6.63 × 10⁻³⁴ × 5.0 × 10¹⁴"], "3.3 × 10⁻¹⁹ J"),
            ("γ for v = 0.6c?", ["γ = 1 ÷ √(1 − 0.36)"], "1.25")],
           ["Thinking brighter light gives photoelectrons more energy: it gives more electrons; frequency sets the energy.", "Applying time dilation to the clock that is at rest with the observer.", "Saying a proton is a fundamental particle: it is made of quarks."],
           [("Why does the photoelectric effect support the photon model?", "Below a threshold frequency no electrons are emitted however bright the light, which waves cannot explain."),
            ("What is a muon's lifetime evidence for?", "Muons made high in the atmosphere reach the ground because their clocks run slow at high speed (time dilation).")],
           lambda X: [
               ("Photons and the photoelectric effect", [(X.ch("al_phys", "particles-and-quantum-phenomena", 3, 12), 10), (X.ch("in_s12p", "dual-nature-of-radiation-and-matter", 2), 10)]),
               ("Wave–particle duality", [(X.ch("al_phys", "particles-and-quantum-phenomena", 4, 12), 10), (X.ch("in_s12p", "dual-nature-of-radiation-and-matter", 5), 10)]),
               ("Time dilation and length contraction", [(X.w(_rel(X)[0]), 10), (X.w(_rel(X)[1]), 6), (X.w(_rel(X)[2]), 4)]),
               ("Mass–energy equivalence", [(X.w(_rel(X)[3]), 10), (X.ch("in_s12p", "nuclei", 3), 10)]),
               ("The standard model", [(X.pool(__import__("au_sr12p").STD), 10), (X.ch("al_phys", "particles-and-quantum-phenomena", 5, 12), 10)]),
           ]),
    ]
