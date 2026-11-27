# -*- coding: utf-8 -*-
"""Year 11 Chemistry (Australian Curriculum: Senior Secondary Chemistry, Units 1 and 2) for au_sr.build."""
from au_sr import SR

CH = "Chemistry"
AT = "atomic-structure-and-amount-of-substance"
BE = "bonding-and-energetics"

# ------------------------------------------------------------------ Unit 1: atoms
ATOM = [
    ("What is the relative atomic mass of an element?", "the weighted mean mass of its isotopes compared with 1/12 of a carbon-12 atom", ["the number of protons in its nucleus", "the mass of its most common isotope only", "the number of neutrons plus electrons"], "Ar takes the abundance of each isotope into account."),
    ("What does a mass spectrometer measure for each ion?", "its mass-to-charge ratio (m/z) and relative abundance", ["its colour", "its boiling point", "its electronegativity"], "Peaks show the isotopes present."),
    ("A mass spectrum of chlorine has peaks at m/z 35 and 37 in a ratio of 3 : 1. What is Ar for chlorine?", "35.5", ["36.0", "35.0", "37.0"], "(35 × 3 + 37 × 1) ÷ 4 = 35.5."),
    ("Why do isotopes of an element have the same chemical properties?", "they have the same number of electrons, arranged the same way", ["they have the same number of neutrons", "they have the same mass", "they are all radioactive"], "Chemistry depends on electrons."),
    ("What causes the coloured lines in an emission spectrum?", "electrons fall from higher to lower energy levels and release photons of particular energies", ["electrons are removed from the nucleus", "the nucleus splits", "atoms absorb heat and turn into light"], "Each element has its own pattern of lines."),
    ("Why is an emission spectrum made of separate lines rather than a continuous band?", "electrons can only have particular energy levels, so only certain energy differences occur", ["the spectroscope blocks most colours", "atoms give out every colour equally", "electrons move in random orbits"], "Energy levels are quantised."),
    ("A flame test gives a lilac (pale purple) flame. Which ion is present?", "potassium, K⁺", ["sodium, Na⁺", "copper, Cu²⁺", "calcium, Ca²⁺"], "Na⁺ is yellow-orange, Cu²⁺ blue-green, Ca²⁺ orange-red."),
    ("A flame test gives a strong yellow-orange flame. Which ion is present?", "sodium, Na⁺", ["potassium, K⁺", "lithium, Li⁺", "barium, Ba²⁺"], "Sodium's yellow can hide other colours."),
    ("A flame test gives a blue-green flame. Which ion is present?", "copper(II), Cu²⁺", ["sodium, Na⁺", "lithium, Li⁺", "potassium, K⁺"], "Copper compounds colour fireworks green-blue."),
    ("A flame test gives a crimson red flame. Which ion is present?", "lithium, Li⁺", ["sodium, Na⁺", "copper(II), Cu²⁺", "potassium, K⁺"], "Strontium gives a similar red."),
    ("Which technique measures the concentration of a metal such as lead in a water sample, and was developed in Australia by Alan Walsh?", "atomic absorption spectroscopy (AAS)", ["paper chromatography", "titration", "a flame test"], "AAS was developed at CSIRO in the 1950s."),
    ("How does atomic absorption spectroscopy work?", "atoms of the element absorb light at its own wavelengths; more absorbance means a higher concentration", ["the sample is weighed before and after heating", "the sample changes colour with an indicator", "the sample is separated on paper"], "A calibration curve converts absorbance to concentration."),
    ("Which statement about ionisation energy across period 3 is correct?", "it generally increases, because nuclear charge increases while shielding stays similar", ["it decreases because atoms get bigger", "it stays the same", "it is highest for sodium"], "Electrons are held more tightly across a period."),
    ("Why does atomic radius decrease across a period?", "more protons pull the electrons in the same shell closer", ["more shells are added", "electrons repel each other more", "neutrons push the electrons out"], "Shielding is about the same across a period."),
    ("Why does atomic radius increase down a group?", "each element has an extra electron shell", ["nuclear charge falls", "there are fewer electrons", "neutrons take up more space"], "Outer electrons are further from the nucleus."),
    ("Which element has the highest electronegativity?", "fluorine", ["caesium", "oxygen", "chlorine"], "Electronegativity increases across a period and up a group."),
    ("Why are group 1 metals more reactive further down the group?", "the outer electron is further from the nucleus and more shielded, so it is lost more easily", ["they have more outer electrons", "their nuclei have fewer protons", "they are less dense"], "First ionisation energy falls down the group."),
    ("Which block of the periodic table contains the transition metals?", "the d-block", ["the s-block", "the p-block", "the f-block"], "Their outer electrons fill d orbitals."),
]


def u6(X):
    return [
        ("Atoms, isotopes and relative atomic mass", [(X.gen("gen_us_science_chem_atomic_structure_and_isotopes", "g_avg"), 6), (X.gen("gen_us_science_chem_atomic_structure_and_isotopes", "g_pne"), 6), (X.pool(ATOM), 4), (X.al(__import__("al_chem").c_ram), 4)]),
        ("Electron configurations", [(X.ch("al_chem", AT, 1, 12), 16), (X.pool(ATOM), 4)]),
        ("Emission spectra and flame tests", [(X.pool(ATOM), 8), (X.al(__import__("al_phys").p_levels), 6), (X.gen("gen_us_science_ess_stars_and_the_origin_of_elements", "g_spec"), 6)]),
        ("Periodic trends", [(X.gen("gen_us_science_chem_periodic_table_and_trends", "g_trend"), 10), (X.ch("in_s11c", "classification-of-elements-and-periodicity-in-properties", 4), 6), (X.pool(ATOM), 4)]),
        ("Interpreting atomic data", [(X.gen("gen_us_science_chem_atomic_structure_and_isotopes", "g_avg"), 6), (X.ch("al_chem", AT, 1, 12), 6), (X.gen("gen_us_science_chem_periodic_table_and_trends", "g_trend"), 6), (X.pool(ATOM), 2)]),
    ]


# ------------------------------------------------------------------ Unit 1: materials
MAT = [
    ("Why do ionic compounds have high melting points?", "strong electrostatic attraction between oppositely charged ions in a lattice must be overcome", ["the molecules are very large", "they have delocalised electrons", "the covalent bonds inside molecules are strong"], "Every ion is attracted to many neighbours."),
    ("Why do ionic compounds conduct electricity when molten but not when solid?", "the ions are free to move only when molten or dissolved", ["electrons move only when molten", "solid ionic compounds have no ions", "melting makes new electrons"], "In the solid the ions are fixed in the lattice."),
    ("Why are metals malleable?", "layers of cations can slide over each other while the delocalised electrons keep holding them together", ["the bonds are very weak", "metals have no bonds", "the ions repel each other strongly"], "Metallic bonding is not directional."),
    ("Why do metals conduct electricity?", "they have a sea of delocalised electrons that can move through the lattice", ["their ions move to the electrodes", "their atoms share electron pairs", "they contain water"], "Electrons carry the charge."),
    ("Why does diamond have a very high melting point?", "each carbon is covalently bonded to four others in a giant network", ["it has weak forces between molecules", "it is ionic", "it contains delocalised electrons"], "All the strong covalent bonds must be broken."),
    ("Why does graphite conduct electricity but diamond does not?", "each carbon in graphite bonds to three others, leaving one delocalised electron", ["graphite is a metal", "diamond has free ions", "graphite has no covalent bonds"], "The electrons move along the layers."),
    ("What is a nanomaterial?", "a material with particles or structures 1–100 nm in size", ["any material made of metal", "a material more than 1 mm thick", "a material with no atoms"], "Nanoparticles have a very large surface area to volume ratio."),
    ("Why do nanoparticles often behave differently from the bulk material?", "they have a much larger surface area to volume ratio", ["they are made of different elements", "they have no electrons", "they are always magnetic"], "Zinc oxide nanoparticles in sunscreen look clear, not white."),
    ("What is graphene?", "a single layer of carbon atoms in a hexagonal network", ["a type of diamond", "an ionic compound of carbon", "a carbon chain polymer"], "It is very strong and conducts electricity."),
    ("Which property makes copper suitable for electrical wiring?", "it is a good conductor and is ductile", ["it is brittle", "it is a good insulator", "it has a low melting point"], "Metals can be drawn into wires."),
    ("What is an alloy?", "a mixture of a metal with other elements, such as steel (iron and carbon)", ["a pure metal", "an ionic compound", "a metal oxide"], "Different-sized atoms stop layers sliding, so alloys are harder."),
    ("Why is an alloy usually harder than the pure metal?", "atoms of different sizes disrupt the layers so they cannot slide easily", ["alloys have ionic bonds", "alloys have no delocalised electrons", "alloys are always lighter"], "Bronze and steel are harder than copper and iron."),
    ("How can sand be separated from salt water?", "filtration", ["distillation", "chromatography", "magnetism"], "Insoluble solids stay on the filter paper."),
    ("How can pure water be obtained from sea water?", "distillation", ["filtration", "chromatography", "decanting"], "Water evaporates and condenses; salt is left behind."),
    ("How can ethanol be separated from water?", "fractional distillation, because their boiling points are different", ["filtration", "magnetic separation", "sieving"], "Ethanol boils at 78 °C, water at 100 °C."),
    ("What does a high Rf value mean in paper chromatography?", "the substance is more attracted to the mobile phase and moves further", ["the substance is insoluble in the solvent", "the substance is more attracted to the paper", "the substance is a mixture"], "Rf = distance moved by spot ÷ distance moved by solvent."),
    ("Crude oil is separated into fractions at a refinery. Which property is used?", "different boiling points", ["different colours", "different magnetism", "different densities in a centrifuge"], "Smaller hydrocarbons boil at lower temperatures."),
    ("Which type of bonding is found in sodium chloride?", "ionic", ["covalent", "metallic", "hydrogen bonding"], "A metal and a non-metal: electron transfer."),
    ("Which type of bonding is found in water molecules?", "covalent", ["ionic", "metallic", "no bonding"], "Non-metals share electron pairs."),
]


def u7(X):
    al_chem = __import__("al_chem")
    return [
        ("Ionic, covalent and metallic bonding", [(X.gen("gen_us_science_chem_chemical_bonding", "g_btype"), 8), (X.pool(MAT), 6), (X.gen("gen_us_science_chem_chemical_bonding", "g_formula"), 6)]),
        ("Properties of materials", [(X.pool(MAT), 8), (X.ch("al_chem", BE, 2, 12), 8), (X.gen("gen_us_science_chem_molecular_structure_and_materials", "g_poly"), 4)]),
        ("Shapes of molecules", [(X.ch("al_chem", BE, 1, 12), 16), (X.pool(MAT), 4)]),
        ("Ionic formulae and naming", [(X.gen("gen_us_science_chem_chemical_bonding", "g_name"), 10), (X.gen("gen_us_science_chem_chemical_bonding", "g_formula"), 6), (X.pool(MAT), 4)]),
        ("Separating mixtures", [(X.pool(MAT), 6), (X.al(__import__("al_chem").c_anal, "rf"), 8), (X.gen("gen_us_science_chem_chemical_bonding", "g_polar"), 6)]),
    ]


# ------------------------------------------------------------------ Unit 1: chemical reactions
REAC = [
    ("What is an exothermic reaction?", "one that releases energy to the surroundings, so ΔH is negative", ["one that takes in energy, so ΔH is positive", "one that needs a catalyst", "one with no energy change"], "Combustion and neutralisation are exothermic."),
    ("What is an endothermic reaction?", "one that absorbs energy from the surroundings, so ΔH is positive", ["one that releases heat", "one in which no bonds break", "one that happens only in sunlight"], "Photosynthesis and thermal decomposition are endothermic."),
    ("Why is bond breaking endothermic?", "energy is needed to overcome the attraction between the atoms", ["bonds release energy when they break", "atoms gain mass", "breaking bonds makes new bonds"], "Bond making releases energy."),
    ("In an energy profile diagram, what is the activation energy?", "the energy difference between the reactants and the top of the energy barrier", ["the energy of the products", "the energy released by the reaction", "the energy difference between reactants and products"], "ΔH is reactants to products; Ea is reactants to the peak."),
    ("What does the law of conservation of mass state?", "mass is not created or destroyed in a chemical reaction", ["mass always increases in a reaction", "gases have no mass", "products are always heavier than reactants"], "Atoms are rearranged, not lost."),
    ("Why must a chemical equation be balanced?", "atoms are neither created nor destroyed, so each element must have the same number on both sides", ["so the charges are all zero", "to show the reaction is fast", "so the molecules have the same mass"], "Change only the coefficients, never the formulae."),
    ("What is the molar volume of a gas at 25 °C and 100 kPa (SLC)?", "24.8 L", ["22.4 L", "1.0 L", "6.02 × 10²³ L"], "At SLC 1 mol of any gas occupies 24.8 L."),
    ("What is the mole?", "the amount of substance containing 6.02 × 10²³ particles", ["the mass of one atom", "1 g of any substance", "the volume of 1 L of gas"], "This number is Avogadro's constant."),
    ("Which equation links amount, mass and molar mass?", "n = m ÷ M", ["m = n ÷ M", "n = m × M", "n = c × V"], "Amount (mol) = mass (g) ÷ molar mass (g/mol)."),
    ("What is the empirical formula of a compound?", "the simplest whole-number ratio of the atoms of each element", ["the actual number of atoms in a molecule", "the mass of one molecule", "the structural diagram"], "Glucose C₆H₁₂O₆ has the empirical formula CH₂O."),
    ("What is the products of the complete combustion of a hydrocarbon?", "carbon dioxide and water", ["carbon monoxide and hydrogen", "carbon and water only", "oxygen and methane"], "Incomplete combustion can give CO and soot."),
    ("Why is incomplete combustion of fuels dangerous?", "it can make carbon monoxide, a toxic gas", ["it makes too much oxygen", "it produces only water", "it uses up nitrogen"], "CO binds to haemoglobin."),
    ("Which energy unit is used for enthalpy changes of reactions?", "kilojoules per mole (kJ mol⁻¹)", ["grams per mole", "joules per gram per kelvin only", "moles per litre"], "ΔH is given per mole of reaction as written."),
    ("What is the specific heat capacity of water used in calorimetry?", "4.18 J g⁻¹ K⁻¹", ["1.00 J g⁻¹ K⁻¹", "418 J g⁻¹ K⁻¹", "0.418 J g⁻¹ K⁻¹"], "q = m × c × ΔT."),
    ("Why does a calorimetry experiment usually give a smaller value of ΔH than the data book?", "heat is lost to the surroundings and the combustion may be incomplete", ["the thermometer adds heat", "water has no heat capacity", "the fuel gains mass"], "Insulating the calorimeter reduces the loss."),
]


def u8(X):
    return [
        ("The mole and molar mass", [(X.ch("al_chem", AT, 2, 12), 14), (X.gen("gen_us_science_chem_the_mole_and_molar_mass", "g_pct"), 3), (X.pool(REAC), 3)]),
        ("Empirical formulae and balancing equations", [(X.ch("al_chem", AT, 4, 12, only=[1]), 8), (X.gen("gen_us_science_chem_balancing_chemical_equations", "g_check"), 6), (X.gen("gen_us_science_chem_balancing_chemical_equations", "g_missing"), 6)]),
        ("Mass calculations from equations", [(X.gen("gen_us_science_chem_stoichiometry", "g_mass"), 8), (X.gen("gen_us_science_chem_stoichiometry", "g_limit"), 6), (X.ch("in_s11c", "some-basic-concepts-of-chemistry", 4), 6)]),
        ("Exothermic and endothermic reactions", [(X.pool(REAC), 8), (X.gen("gen_us_science_chem_energy_in_chemical_reactions", "g_diag"), 6), (X.gen("gen_us_science_chem_energy_in_chemical_reactions", "g_bond"), 6)]),
        ("Calorimetry and enthalpy", [(X.ch("al_chem", BE, 3, 12), 16), (X.pool(REAC), 4)]),
    ]


# ------------------------------------------------------------------ Unit 2: intermolecular forces and gases
IMF = [
    ("Which intermolecular force is present between all molecules?", "dispersion forces", ["hydrogen bonds", "dipole–dipole forces", "ionic bonds"], "Dispersion forces come from temporary dipoles."),
    ("Why does the boiling point of the alkanes increase as the chain gets longer?", "larger molecules have more electrons, so dispersion forces are stronger", ["longer chains form hydrogen bonds", "covalent bonds in the chain break", "longer chains are ionic"], "Methane is a gas; octane is a liquid."),
    ("Which molecule can form hydrogen bonds with other molecules of itself?", "ammonia, NH₃", ["methane, CH₄", "hydrogen sulfide, H₂S", "carbon dioxide, CO₂"], "H must be bonded to N, O or F."),
    ("Why is water's boiling point (100 °C) much higher than that of H₂S (−60 °C)?", "water molecules form hydrogen bonds with each other", ["water has stronger covalent bonds", "H₂S is ionic", "water molecules are larger"], "H₂S has only dipole–dipole and dispersion forces."),
    ("Why is ice less dense than liquid water?", "hydrogen bonds hold the molecules in an open lattice", ["ice contains air bubbles in every case", "the covalent bonds lengthen", "ice has fewer molecules"], "So ice floats and lakes freeze from the top."),
    ("Why is CO₂ a non-polar molecule even though its C=O bonds are polar?", "it is linear, so the bond dipoles cancel", ["carbon and oxygen have the same electronegativity", "it has no electrons", "it is ionic"], "Molecular shape decides overall polarity."),
    ("Why is water a polar molecule?", "its O–H bonds are polar and its bent shape means the dipoles do not cancel", ["it is linear", "it contains ions", "oxygen and hydrogen share electrons equally"], "Oxygen is more electronegative than hydrogen."),
    ("Which substance would dissolve best in water?", "ethanol, which can hydrogen bond with water", ["hexane", "oil", "iodine"], "‘Like dissolves like’."),
    ("Why does hexane not dissolve in water?", "hexane is non-polar and cannot form hydrogen bonds with water", ["hexane is ionic", "hexane molecules are too small", "water is non-polar"], "Water molecules attract each other more strongly."),
    ("What does the kinetic molecular theory say about gas particles?", "they move randomly and rapidly, and their mean kinetic energy depends on temperature", ["they are fixed in place", "they attract each other strongly", "they all move at the same speed"], "Collisions with the walls cause pressure."),
    ("What happens to the pressure of a gas if its volume is halved at constant temperature?", "it doubles", ["it halves", "it stays the same", "it becomes four times greater"], "Boyle's law: pV is constant."),
    ("Which temperature scale must be used in gas law calculations?", "kelvin (K)", ["degrees Celsius", "the scale printed on the thermometer", "any scale, as long as it is the same throughout"], "T(K) = T(°C) + 273."),
    ("What is the ideal gas equation?", "pV = nRT", ["p = VnRT", "pV = nR ÷ T", "V = pnRT"], "R = 8.31 J mol⁻¹ K⁻¹ with p in kPa and V in L."),
    ("Why does a gas behave less ideally at high pressure?", "the particles are close together, so their own volume and attractions matter", ["the particles stop moving", "the temperature becomes zero", "the gas becomes ionic"], "Ideal gases have no volume and no attractions."),
]


def u9(X):
    al_phys = __import__("al_phys")
    return [
        ("Types of intermolecular forces", [(X.gen("gen_us_science_chem_intermolecular_forces_and_properties", "g_imf"), 8), (X.pool(IMF), 6), (X.ch("al_chem", BE, 2, 12), 6)]),
        ("Polarity and molecular shape", [(X.gen("gen_us_science_chem_chemical_bonding", "g_polar"), 10), (X.ch("al_chem", BE, 1, 12), 6), (X.pool(IMF), 4)]),
        ("Boiling points and solubility", [(X.gen("gen_us_science_chem_intermolecular_forces_and_properties", "g_bp"), 10), (X.gen("gen_us_science_chem_intermolecular_forces_and_properties", "g_order"), 6), (X.pool(IMF), 4)]),
        ("Gas laws", [(X.al(al_phys.t_gas, "boyle", "charles"), 14), (X.pool(IMF), 6)]),
        ("The ideal gas equation and molar volume", [(X.ch("al_chem", AT, 4, 12, only=[0]), 10), (X.al(al_phys.t_gas, "pV", "n"), 10)]),
    ]


# ------------------------------------------------------------------ Unit 2: aqueous solutions and acidity
AQ = [
    ("Which ions are present in a solution of an acid?", "hydrogen ions, H⁺ (as H₃O⁺)", ["hydroxide ions, OH⁻", "sodium ions only", "no ions"], "Acids donate protons."),
    ("What is the Brønsted–Lowry definition of an acid?", "a proton (H⁺) donor", ["a proton acceptor", "an electron donor", "a substance with a pH above 7"], "A base is a proton acceptor."),
    ("What is the difference between a strong acid and a concentrated acid?", "a strong acid ionises fully; a concentrated acid has many moles per litre", ["they mean the same thing", "a strong acid is always more dangerous", "a concentrated acid always ionises fully"], "A dilute solution of HCl is still a strong acid."),
    ("Which is a weak acid?", "ethanoic acid (vinegar)", ["hydrochloric acid", "nitric acid", "sulfuric acid"], "Weak acids ionise only partly."),
    ("What is the pH of a 0.010 mol/L solution of HCl?", "2", ["1", "0.010", "12"], "pH = −log[H⁺] = −log(0.010) = 2."),
    ("A solution has pH 3. Another has pH 5. How do their H⁺ concentrations compare?", "the pH 3 solution has 100 times the H⁺ concentration", ["the pH 3 solution has 2 times the concentration", "the pH 5 solution has more H⁺", "they are the same"], "Each pH unit is a factor of 10."),
    ("What is the product of the ionic equation H⁺ + OH⁻?", "H₂O", ["H₂", "O₂", "H₂O₂"], "This is the reaction in every neutralisation."),
    ("What are the products when an acid reacts with a metal carbonate?", "a salt, water and carbon dioxide", ["a salt and hydrogen", "a salt only", "a base and oxygen"], "The fizz is CO₂."),
    ("What are the products when an acid reacts with a reactive metal such as zinc?", "a salt and hydrogen gas", ["a salt, water and carbon dioxide", "a base and water", "oxygen and a salt"], "Hydrogen gives a pop with a lit splint."),
    ("Which indicator changes colour around pH 8–10 and is used for weak acid–strong base titrations?", "phenolphthalein", ["methyl orange", "litmus only", "universal indicator"], "It is colourless in acid and pink in base."),
    ("What is the end point of a titration?", "when the indicator changes colour", ["when the burette is empty", "when the solution boils", "when all the base has evaporated"], "Ideally it matches the equivalence point."),
    ("What is a precipitate?", "an insoluble solid formed when two solutions are mixed", ["a gas formed in a reaction", "a solution that is very concentrated", "a liquid that does not mix with water"], "Silver chloride forms a white precipitate."),
    ("Silver nitrate is added to a solution and a white precipitate forms. Which ion is likely to be present?", "chloride, Cl⁻", ["nitrate, NO₃⁻", "sodium, Na⁺", "sulfate, SO₄²⁻"], "Ag⁺ + Cl⁻ → AgCl(s)."),
    ("Which compound is insoluble in water?", "barium sulfate, BaSO₄", ["sodium chloride, NaCl", "potassium nitrate, KNO₃", "ammonium chloride, NH₄Cl"], "All sodium, potassium, ammonium and nitrate salts are soluble."),
    ("Which ions are spectator ions when solutions of NaCl and AgNO₃ are mixed?", "Na⁺ and NO₃⁻", ["Ag⁺ and Cl⁻", "Na⁺ and Cl⁻", "Ag⁺ and NO₃⁻"], "Spectator ions stay in solution unchanged."),
    ("Why is water a good solvent for ionic compounds?", "polar water molecules surround and separate the ions", ["water molecules are ionic", "water is non-polar", "ions dissolve in any liquid"], "The ions are hydrated."),
    ("What does ‘ppm’ mean when it is used for the concentration of lead in drinking water?", "parts per million, such as milligrams per litre", ["percentage by mass", "moles per litre", "grams per 100 g"], "1 ppm = 1 mg/L for dilute water solutions."),
    ("Why does a high concentration of dissolved carbon dioxide lower the pH of the ocean?", "CO₂ reacts with water to form carbonic acid, which releases H⁺ ions", ["CO₂ is a strong base", "CO₂ removes all ions from water", "CO₂ makes the ocean freeze"], "Ocean acidification threatens corals and shellfish."),
]


def u10(X):
    al_chem = __import__("al_chem")
    return [
        ("Concentration", [(X.ch("in_s11c", "some-basic-concepts-of-chemistry", 3), 12), (X.al(al_chem.c_conc), 6), (X.pool(AQ), 2)]),
        ("Solubility and precipitation", [(X.pool(AQ), 8), (X.gen("gen_us_science_chem_types_of_chemical_reactions", "g_prod"), 6), (X.gen("gen_us_science_chem_types_of_chemical_reactions", "g_type"), 6)]),
        ("Acids, bases and pH", [(X.pool(AQ), 6), (X.al(al_chem.c_ph, "strong"), 10), (X.al(al_chem.c_ph, "H"), 4)]),
        ("Acid–base reactions and titrations", [(X.al(al_chem.c_titr), 12), (X.pool(AQ), 4), (X.al(al_chem.c_ph, "base"), 4)]),
        ("Water quality and solution problems", [(X.al(al_chem.c_conc), 8), (X.al(al_chem.c_ph, "dil"), 6), (X.ch("in_s11c", "some-basic-concepts-of-chemistry", 3), 6)]),
    ]


# ------------------------------------------------------------------ Unit 2: rates
RATE = [
    ("According to collision theory, what must happen for particles to react?", "they must collide with enough energy (at least the activation energy) and the right orientation", ["they must stop moving", "they must be in the same phase", "they must be heated above 100 °C"], "Only a fraction of collisions are successful."),
    ("Why does raising the temperature increase the rate of reaction?", "more particles have energy above the activation energy, and they collide more often", ["the activation energy falls", "the particles get bigger", "the products are removed"], "The effect on energy is the bigger one."),
    ("Why does increasing concentration increase the rate of reaction?", "there are more particles in the same volume, so collisions are more frequent", ["each collision has more energy", "the activation energy falls", "the temperature rises"], "Rate depends on collision frequency."),
    ("Why does powdered marble react faster with acid than marble chips?", "the powder has a larger surface area, so more collisions happen", ["powder has more energy", "powder is a catalyst", "chips are a different substance"], "Only surface particles can collide."),
    ("How does a catalyst increase the rate of reaction?", "it provides an alternative pathway with a lower activation energy", ["it gives particles more kinetic energy", "it raises the temperature", "it is used up in the reaction"], "The catalyst is unchanged at the end."),
    ("What does a Maxwell–Boltzmann distribution show?", "the number of particles with each kinetic energy at one temperature", ["how concentration changes with time", "the energy of products and reactants", "the number of collisions per second"], "The area under the curve is the total number of particles."),
    ("How does a Maxwell–Boltzmann curve change at a higher temperature?", "the peak moves to the right and lowers, and more particles are above Ea", ["the peak moves left and rises", "the area under the curve doubles", "the curve does not change"], "The total number of particles stays the same."),
    ("On a Maxwell–Boltzmann diagram, how does a catalyst change the picture?", "the activation energy line moves to the left, so more particles have enough energy", ["the curve moves right", "the curve becomes taller", "the number of particles increases"], "The distribution itself does not change."),
    ("How can the rate of the reaction between magnesium and acid be measured?", "measure the volume of hydrogen made every 10 seconds", ["measure the colour of the acid", "count the magnesium atoms", "measure the pH once at the end"], "A gas syringe collects the gas."),
    ("On a graph of volume of gas against time, what does a steeper slope mean?", "a faster rate of reaction", ["a slower rate of reaction", "the reaction has stopped", "less gas is made in total"], "Rate = gradient of the curve."),
    ("Why does the rate of reaction decrease as the reaction goes on?", "reactants are used up, so their concentration falls", ["the catalyst is used up", "the products speed it up", "the temperature always rises"], "The curve levels off when a reactant runs out."),
    ("Why are catalytic converters fitted to car exhausts?", "they speed up the conversion of CO, NO and unburnt fuel into less harmful gases", ["they make the engine hotter", "they add oxygen to petrol", "they slow down the engine"], "They contain platinum, palladium and rhodium."),
    ("Why are enzymes important industrial catalysts?", "they work at low temperatures and are very specific, saving energy", ["they work only at high temperature", "they are used up quickly", "they raise the activation energy"], "Enzymes are used in detergents and food processing."),
    ("Which change would NOT increase the rate of reaction between zinc and hydrochloric acid?", "using larger lumps of zinc", ["warming the acid", "using more concentrated acid", "adding a copper catalyst"], "Larger lumps have less surface area."),
]


def u11(X):
    return [
        ("Collision theory", [(X.pool(RATE), 8), (X.ch("al_chem", "kinetics-and-equilibria", 1, 12), 8), (X.gen("gen_us_science_chem_reaction_rates", "g_factor"), 4)]),
        ("Factors that affect rate", [(X.gen("gen_us_science_chem_reaction_rates", "g_factor"), 10), (X.pool(RATE), 6), (X.ch("al_chem", "kinetics-and-equilibria", 1, 12), 4)]),
        ("Measuring rates of reaction", [(X.ch("in_s12c", "chemical-kinetics", 1), 14), (X.pool(RATE), 4), (X.gen("gen_us_science_chem_reaction_rates", "g_data"), 2)]),
        ("Energy profiles and catalysts", [(X.gen("gen_us_science_chem_energy_in_chemical_reactions", "g_diag"), 10), (X.ch("al_chem", "kinetics-and-equilibria", 1, 12), 6), (X.pool(RATE), 4)]),
        ("Rate data and investigations", [(X.gen("gen_us_science_chem_reaction_rates", "g_data"), 12), (X.ch("in_s12c", "chemical-kinetics", 1), 8)]),
    ]


def UNITS():
    return [
        SR(CH, 1, 6, "atomic-structure-and-the-periodic-table", "Properties and structure of atoms",
           "Atomic structure, isotopes and relative atomic mass from mass spectra; electron configurations; emission spectra, flame tests and atomic absorption spectroscopy; trends in atomic radius, ionisation energy and electronegativity in the periodic table.",
           "Atomic Structure, Spectra and the Periodic Table", "atomic structure and the periodic table",
           "Free Year 11 Chemistry worksheets on atoms: isotopes, relative atomic mass, mass spectra, electron configurations, flame tests, AAS, emission spectra and periodic trends. 100 questions with answers.",
           "Ar = Σ(isotope mass × abundance) ÷ 100.", "Across a period: radius ↓, ionisation energy ↑, electronegativity ↑.",
           "<p>An atom has a nucleus of protons and neutrons with electrons in energy levels (shells and subshells: 1s² 2s² 2p⁶ …). Isotopes have the same number of protons but different neutrons; relative atomic mass is the weighted mean of the isotopes, measured with a mass spectrometer.</p>"
           "<p>When excited electrons fall to lower levels they emit photons of fixed energies: this gives line spectra and flame colours. Atomic absorption spectroscopy, invented at CSIRO, measures metal concentrations.</p>"
           "<p>Across a period nuclear charge rises, so atoms shrink and hold electrons more tightly; down a group atoms get bigger and lose outer electrons more easily.</p>",
           [("Copper: ⁶³Cu 69.2%, ⁶⁵Cu 30.8%. Ar?", ["(63 × 69.2 + 65 × 30.8) ÷ 100"], "63.6"),
            ("Electron configuration of S (Z = 16)?", ["2 + 8 + 6", "1s² 2s² 2p⁶ 3s² 3p⁴"], "1s² 2s² 2p⁶ 3s² 3p⁴")],
           ["Using the mass number of the most common isotope as Ar.", "Thinking atoms get bigger across a period: they get smaller.", "Saying the electrons ‘burn’ in a flame test: they are excited and then emit light."],
           [("Why does each element have its own emission spectrum?", "Each element has its own set of electron energy levels, so the energy differences, and the colours of light emitted, are unique to it."),
            ("Why does ionisation energy decrease down a group?", "The outer electron is in a shell further from the nucleus and more shielded by inner electrons, so less energy is needed to remove it.")],
           u6),
        SR(CH, 1, 7, "bonding-and-properties-of-materials", "Properties and structure of materials",
           "Ionic, covalent (molecular and network) and metallic bonding and the properties they explain; alloys and nanomaterials; shapes of molecules (VSEPR); writing formulae; separating mixtures by filtration, distillation and chromatography.",
           "Bonding, Structure and Properties of Materials", "bonding and properties of materials",
           "Free Year 11 Chemistry worksheets on bonding and materials: ionic, covalent and metallic bonds, lattices, diamond and graphite, alloys, nanomaterials, VSEPR shapes, formulae and separation. 100 questions with answers.",
           "Structure explains properties.", "Ionic: ion lattice. Metallic: cations in a sea of electrons. Covalent: shared pairs.",
           "<p><b>Ionic</b> compounds are lattices of ions: high melting points, brittle, conduct only when molten or dissolved. <b>Metals</b> are cations in a sea of delocalised electrons: conductive and malleable. <b>Covalent</b> substances are either small molecules (low melting points) or giant networks such as diamond and silicon dioxide (very high melting points).</p>"
           "<p>VSEPR theory: electron pairs around the central atom repel, giving shapes such as linear, bent, trigonal pyramidal and tetrahedral. Mixtures are separated using differences in particle size, boiling point or attraction to a stationary phase.</p>",
           [("Shape of NH₃?", ["3 bonding pairs + 1 lone pair", "tetrahedral arrangement, one corner empty"], "trigonal pyramidal"),
            ("Formula of aluminium oxide?", ["Al³⁺ and O²⁻", "2 × (+3) = 3 × (−2)"], "Al₂O₃")],
           ["Saying ionic solids conduct electricity: the ions cannot move.", "Breaking covalent bonds when a molecular substance melts: only the intermolecular forces are overcome.", "Ignoring lone pairs when working out a shape."],
           [("Why does sodium chloride conduct when dissolved but not when solid?", "In the solid the ions are fixed in the lattice; in solution (or molten) they are free to move and carry charge."),
            ("Why are nanomaterials useful?", "Their tiny particles have a huge surface area to volume ratio, so they can be more reactive, stronger or transparent, as in sunscreens and catalysts.")],
           u7),
        SR(CH, 1, 8, "moles-and-chemical-reactions", "Chemical reactions: reactants, products and energy",
           "The mole concept and molar mass; empirical and molecular formulae; balanced equations and mass calculations; limiting reactants; exothermic and endothermic reactions, energy profiles, enthalpy change and calorimetry.",
           "Moles, Equations and Energy in Reactions", "moles and chemical reactions",
           "Free Year 11 Chemistry worksheets on the mole, molar mass, empirical formulae, balancing equations, mass calculations, limiting reactants, ΔH and calorimetry. 100 questions with answers.",
           "n = m ÷ M; N = n × 6.02 × 10²³.", "q = mcΔT; ΔH = −q ÷ n for an exothermic reaction.",
           "<p>The mole counts particles: 1 mol = 6.02 × 10²³ particles, and n = m ÷ M. A balanced equation gives mole ratios, so you can find the mass of product from the mass of reactant: mass → moles → ratio → moles → mass.</p>"
           "<p>Reactions are exothermic (ΔH negative) or endothermic (ΔH positive). In calorimetry the heat absorbed by water is q = m × 4.18 × ΔT; divide by the moles of fuel to find the molar enthalpy.</p>",
           [("Moles in 11.0 g of CO₂ (M = 44.0 g/mol)?", ["n = 11.0 ÷ 44.0"], "0.250 mol"),
            ("0.010 mol of fuel heats 200 g of water by 10 K. ΔH?", ["q = 200 × 4.18 × 10 = 8360 J", "8.36 kJ ÷ 0.010 mol"], "−836 kJ/mol")],
           ["Using the mass ratio instead of the mole ratio from the equation.", "Forgetting the negative sign of ΔH for an exothermic reaction.", "Changing a formula (subscript) to balance an equation."],
           [("How do you find the limiting reactant?", "Work out the moles of each reactant and divide by its coefficient; the smallest value is the limiting reactant, which decides the amount of product."),
            ("What is the difference between ΔH and activation energy?", "ΔH is the energy difference between reactants and products; the activation energy is the energy barrier the reactants must get over.")],
           u8),
        SR(CH, 2, 9, "intermolecular-forces-and-gases", "Intermolecular forces and gases",
           "Dispersion forces, dipole–dipole forces and hydrogen bonding; polarity from bond polarity and shape; boiling points and solubility; the kinetic molecular theory, the gas laws and the ideal gas equation pV = nRT.",
           "Intermolecular Forces, Polarity and Gases", "intermolecular forces and gases",
           "Free Year 11 Chemistry worksheets on intermolecular forces: dispersion, dipole–dipole and hydrogen bonding, polarity, boiling points, solubility, Boyle's and Charles' laws and pV = nRT. 100 questions with answers.",
           "Stronger intermolecular forces → higher boiling point.", "pV = nRT with T in kelvin; R = 8.31 J mol⁻¹ K⁻¹.",
           "<p>Molecules attract each other by <b>dispersion forces</b> (all molecules, stronger for more electrons), <b>dipole–dipole forces</b> (polar molecules) and <b>hydrogen bonds</b> (H on N, O or F). These forces, not the covalent bonds, are overcome when a molecular substance melts or boils.</p>"
           "<p>A molecule is polar if its bonds are polar and its shape does not cancel them (H₂O is polar, CO₂ is not). Gases follow pV = nRT: pressure rises if volume falls (Boyle) and volume rises with kelvin temperature (Charles).</p>",
           [("A gas at 100 kPa is squeezed from 6.0 L to 2.0 L (same T). New pressure?", ["p₁V₁ = p₂V₂", "100 × 6.0 ÷ 2.0"], "300 kPa"),
            ("Moles of gas in 2.48 L at 100 kPa and 298 K?", ["n = pV ÷ RT", "100 × 2.48 ÷ (8.31 × 298)"], "0.100 mol")],
           ["Saying covalent bonds break when water boils: hydrogen bonds between molecules are overcome.", "Using °C in the gas laws.", "Calling every molecule with polar bonds a polar molecule."],
           [("Why does ice float?", "Hydrogen bonds hold water molecules in an open lattice in ice, so ice is less dense than liquid water."),
            ("When is a gas most like an ideal gas?", "At low pressure and high temperature, where the particles are far apart and move fast, so their volume and attractions hardly matter.")],
           u9),
        SR(CH, 2, 10, "aqueous-solutions-and-acidity", "Aqueous solutions and acidity",
           "Water as a solvent; concentration in mol/L, g/L and ppm; solubility rules, precipitation reactions and ionic equations; acids and bases (Brønsted–Lowry), strong and weak acids, pH; neutralisation reactions and titrations.",
           "Aqueous Solutions, Acids and pH", "aqueous solutions and acidity",
           "Free Year 11 Chemistry worksheets on solutions and acids: concentration, dilution, ppm, precipitation, ionic equations, strong and weak acids, pH, neutralisation and titration calculations. 100 questions with answers.",
           "c = n ÷ V; pH = −log[H⁺].", "Each pH unit is a factor of 10 in [H⁺].",
           "<p>Water is polar, so it dissolves many ionic and polar substances. Concentration c = n ÷ V (mol/L); for dilution c₁V₁ = c₂V₂. Mixing solutions can form an insoluble <b>precipitate</b>; the ionic equation leaves out spectator ions.</p>"
           "<p>An acid donates protons (H⁺) and a base accepts them. Strong acids ionise fully; weak acids only partly. pH = −log[H⁺]. In a titration, the mole ratio in the equation links the acid and the base.</p>",
           [("pH of 0.0010 mol/L HCl?", ["[H⁺] = 0.0010", "pH = −log 0.0010"], "3"),
            ("25.0 mL of 0.100 mol/L NaOH is neutralised by 20.0 mL of HCl. c(HCl)?", ["n(NaOH) = 0.00250 mol", "1 : 1, so 0.00250 ÷ 0.0200"], "0.125 mol/L")],
           ["Mixing up strong and concentrated.", "Forgetting to change mL into L in c = n ÷ V.", "Ignoring the 2 : 1 ratio for H₂SO₄ in titrations."],
           [("What does pH 7 mean?", "A neutral solution at 25 °C, where [H⁺] = [OH⁻] = 10⁻⁷ mol/L."),
            ("How do you write an ionic equation for a precipitation?", "Write only the ions that form the solid, such as Ag⁺(aq) + Cl⁻(aq) → AgCl(s); the spectator ions are left out.")],
           u10),
        SR(CH, 2, 11, "rates-of-reaction", "Rates of chemical reactions",
           "Collision theory; the effect of temperature, concentration, surface area and catalysts on reaction rate; Maxwell–Boltzmann energy distributions; energy profile diagrams; measuring and graphing rates of reaction.",
           "Rates of Reaction and Collision Theory", "rates of reaction",
           "Free Year 11 Chemistry worksheets on reaction rates: collision theory, temperature, concentration, surface area, catalysts, Maxwell–Boltzmann curves, energy profiles and rate graphs. 100 questions with answers.",
           "Rate depends on how often particles collide with enough energy.", "A catalyst lowers the activation energy; it is not used up.",
           "<p>For a reaction, particles must collide with at least the activation energy and the right orientation. Higher <b>concentration</b> or pressure and larger <b>surface area</b> make collisions more frequent; higher <b>temperature</b> makes collisions more frequent and, more importantly, more energetic.</p>"
           "<p>A Maxwell–Boltzmann curve shows the spread of particle energies; only particles beyond Eₐ can react. A <b>catalyst</b> provides a pathway with a lower Eₐ. Rate is measured from the gradient of a graph of product or reactant against time.</p>",
           [("40 mL of gas in the first 20 s. Mean rate?", ["40 ÷ 20"], "2.0 mL/s"),
            ("Concentration falls from 0.80 to 0.20 mol/L in 60 s. Mean rate?", ["(0.80 − 0.20) ÷ 60"], "0.010 mol L⁻¹ s⁻¹")],
           ["Saying a catalyst gives particles more energy.", "Thinking higher temperature only makes particles collide more often: energy matters most.", "Drawing the Maxwell–Boltzmann curve with a bigger area at a higher temperature."],
           [("Why does a small temperature rise make a big difference to rate?", "It greatly increases the fraction of particles with energy above the activation energy, so many more collisions are successful."),
            ("How do catalysts help industry?", "They make reactions faster at lower temperatures, saving energy and money, and they can be reused.")],
           u11),
    ]
