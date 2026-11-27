# -*- coding: utf-8 -*-
"""Year 12 Chemistry (Australian Curriculum: Senior Secondary Chemistry, Units 3 and 4) for au_sr.build."""
from au_sr import SR

CH = "Chemistry"
KE = "kinetics-and-equilibria"
AB = "acids-bases-and-electrode-potentials"
RX = "redox-and-inorganic-chemistry"
OR = "organic-chemistry-alkanes-alkenes-and-alcohols"
FO = "further-organic-chemistry-and-analysis"

EQ = [
    ("What is a dynamic equilibrium?", "the forward and reverse reactions happen at the same rate, so concentrations stay constant", ["both reactions have stopped", "the concentrations of reactants and products are equal", "only the forward reaction happens"], "It needs a closed system."),
    ("Why must a system be closed to reach equilibrium?", "no reactants or products can enter or leave", ["so the temperature rises", "so a catalyst can be added", "so the reaction goes to completion"], "Open systems cannot reach equilibrium."),
    ("What does Le Chatelier's principle state?", "if a system at equilibrium is changed, the position of equilibrium shifts to partly oppose the change", ["equilibrium cannot be changed", "a catalyst shifts equilibrium to the right", "equilibrium always lies to the right"], "It predicts the direction of shift."),
    ("What effect does a catalyst have on an equilibrium?", "it makes equilibrium reached faster but does not change its position or K", ["it shifts equilibrium to the right", "it increases K", "it shifts equilibrium to the left"], "It speeds up both directions equally."),
    ("For an exothermic reaction, what happens to K when the temperature is raised?", "K decreases", ["K increases", "K stays the same", "K becomes zero"], "Only temperature changes the value of K."),
    ("What does a very large value of K (such as 10¹⁰) tell you?", "at equilibrium there are mostly products", ["at equilibrium there are mostly reactants", "the reaction is very fast", "the reaction is endothermic"], "K describes position, not rate."),
    ("In the Haber process, N₂ + 3H₂ ⇌ 2NH₃ (exothermic), why is a high pressure used?", "there are fewer gas moles on the right, so high pressure shifts equilibrium towards ammonia", ["it lowers the activation energy", "it makes the reaction endothermic", "it increases K"], "About 200 atm is used."),
    ("Why is the Haber process run at about 450 °C, even though a lower temperature gives more ammonia?", "a lower temperature would make the rate too slow; 450 °C is a compromise", ["450 °C gives the highest yield", "the catalyst works only above 1000 °C", "ammonia decomposes below 400 °C"], "Yield and rate are balanced."),
    ("If the concentration of a reactant is increased, which way does the equilibrium shift?", "to the right, to use up some of the added reactant", ["to the left", "it does not shift", "it stops"], "K stays the same."),
    ("What is the reaction quotient Q?", "the same expression as K but with the concentrations at any moment", ["the equilibrium constant at 25 °C", "the rate constant", "the amount of catalyst"], "If Q < K the reaction goes forward."),
    ("Why does a cold drink lose its fizz more slowly than a warm one?", "CO₂ is more soluble at lower temperatures, so less leaves the solution", ["cold drinks have no CO₂", "warm drinks contain more CO₂", "temperature does not affect solubility"], "Gas solubility falls as temperature rises."),
    ("In blood, CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻. What happens to blood pH if a person breathes too fast and loses CO₂?", "pH rises, because the equilibria shift left and [H⁺] falls", ["pH falls", "pH does not change", "blood becomes neutral"], "This is respiratory alkalosis."),
    ("For 2NO₂(g) ⇌ N₂O₄(g), the brown colour fades when the mixture is cooled. What does this show?", "the forward reaction is exothermic", ["the forward reaction is endothermic", "a catalyst was added", "pressure increased"], "Cooling favours the exothermic direction."),
    ("Why do pure solids and pure liquids not appear in an equilibrium expression?", "their concentrations do not change", ["they do not react", "they are always products", "they are gases"], "Water as a solvent is also left out."),
]
ACID = [
    ("What is the ionisation constant of water, Kw, at 25 °C?", "1.0 × 10⁻¹⁴", ["1.0 × 10⁻⁷", "7", "14"], "Kw = [H₃O⁺][OH⁻]."),
    ("What is the pH of a 0.010 mol/L NaOH solution at 25 °C?", "12", ["2", "10", "7"], "[OH⁻] = 0.010, [H₃O⁺] = 10⁻¹², pH = 12."),
    ("What is a conjugate acid–base pair?", "two species that differ by one proton (H⁺)", ["an acid and any base", "two acids", "a salt and water"], "NH₄⁺ / NH₃ is a pair."),
    ("What is the conjugate base of HSO₄⁻?", "SO₄²⁻", ["H₂SO₄", "HSO₃⁻", "OH⁻"], "Remove one H⁺."),
    ("What is an amphiprotic substance?", "one that can act as an acid or a base, such as water or HCO₃⁻", ["one that is always an acid", "one with no protons", "a strong base"], "Water donates or accepts protons."),
    ("Which is a strong base?", "sodium hydroxide, NaOH", ["ammonia, NH₃", "ethanoic acid", "sodium chloride"], "Strong bases dissociate fully."),
    ("What happens to the pH of a strong acid when it is diluted 10 times?", "it rises by 1", ["it falls by 1", "it rises by 10", "it does not change"], "[H₃O⁺] falls by a factor of 10."),
    ("What is the pH of 0.050 mol/L H₂SO₄, assuming both protons ionise?", "1", ["1.3", "0.05", "2"], "[H₃O⁺] = 0.10 mol/L."),
    ("What is a buffer?", "a solution that resists changes in pH when small amounts of acid or base are added", ["a strong acid", "a solution of pH 7 only", "a catalyst"], "It contains a weak acid and its conjugate base."),
    ("What does a higher Ka mean?", "a stronger weak acid that ionises more", ["a weaker acid", "a stronger base", "a higher pH"], "pKa = −log Ka, so a lower pKa means a stronger acid."),
    ("Why is the pH at the equivalence point of a weak acid–strong base titration above 7?", "the conjugate base of the weak acid reacts with water to form OH⁻", ["there is excess acid", "the indicator is basic", "water is a strong base"], "Choose phenolphthalein for this titration."),
    ("Which indicator suits a strong acid–weak base titration?", "methyl orange (changes around pH 3–4.5)", ["phenolphthalein", "no indicator works", "litmus only"], "The equivalence point is below 7."),
    ("What is the purpose of a primary standard in titrations?", "to make a solution of exactly known concentration", ["to change colour at the end point", "to speed up the reaction", "to act as a catalyst"], "Anhydrous sodium carbonate is a common primary standard."),
    ("Why should a burette be rinsed with the solution it will contain, not with water?", "water would dilute the solution and change its concentration", ["water reacts with the burette", "to make it faster", "to remove the indicator"], "Pipettes are rinsed the same way."),
    ("What is a concordant titre?", "titres that agree within 0.10 mL", ["the first rough titre", "the largest titre", "a titre with no indicator"], "Average the concordant titres."),
    ("Why is ocean acidification a concern for the Great Barrier Reef?", "lower pH reduces carbonate ions, so corals find it harder to build calcium carbonate skeletons", ["it makes the water colder", "it adds more carbonate", "it raises the pH"], "Dissolved CO₂ forms carbonic acid."),
    ("What does the pH scale measure?", "the concentration of hydronium ions, pH = −log[H₃O⁺]", ["the concentration of all ions", "the strength of a base only", "the temperature"], "A change of 1 pH unit is a factor of 10."),
]
REDOX = [
    ("What is oxidation?", "loss of electrons (or an increase in oxidation number)", ["gain of electrons", "gain of hydrogen", "a decrease in oxidation number"], "OIL RIG: oxidation is loss, reduction is gain."),
    ("What is reduction?", "gain of electrons (or a decrease in oxidation number)", ["loss of electrons", "gain of oxygen", "an increase in oxidation number"], "The oxidising agent is reduced."),
    ("In Zn + Cu²⁺ → Zn²⁺ + Cu, what is the reducing agent?", "zinc", ["Cu²⁺", "Zn²⁺", "copper"], "Zinc loses electrons and is oxidised."),
    ("In Zn + Cu²⁺ → Zn²⁺ + Cu, what is the oxidising agent?", "Cu²⁺", ["zinc", "Zn²⁺", "copper metal"], "Cu²⁺ gains electrons and is reduced."),
    ("What happens when a strip of zinc is placed in copper(II) sulfate solution?", "copper forms on the zinc and the blue colour fades", ["nothing happens", "zinc forms on the copper", "the solution turns green and hydrogen forms"], "Zinc is more reactive than copper."),
    ("Which metal would NOT displace copper from copper(II) sulfate?", "silver", ["zinc", "iron", "magnesium"], "Silver is less reactive than copper."),
    ("What is the oxidation number of an element in its uncombined state?", "0", ["+1", "−1", "it depends on its group"], "For example, O₂ and Fe have 0."),
    ("What is the oxidation number of oxygen in most compounds?", "−2", ["+2", "0", "−1"], "In peroxides it is −1."),
    ("Why is rusting a redox reaction?", "iron is oxidised to iron(III) and oxygen is reduced", ["iron gains electrons", "no electrons are transferred", "water is oxidised to hydrogen"], "Water and oxygen are both needed."),
    ("How does galvanising protect steel?", "a coating of zinc is oxidised in preference to iron (sacrificial protection)", ["zinc makes the steel stronger", "zinc reacts with water to make paint", "zinc stops all oxygen reaching the air"], "Even scratched, the zinc protects."),
    ("Why are blocks of magnesium or zinc attached to ship hulls?", "they corrode instead of the steel hull (sacrificial anodes)", ["to make the ship heavier", "to stop barnacles", "to increase speed"], "They are replaced as they wear away."),
    ("When balancing a half-equation in acid, which species are added to balance oxygen and hydrogen?", "H₂O for oxygen, then H⁺ for hydrogen", ["O₂ and H₂", "OH⁻ only", "electrons only"], "Finally add electrons to balance charge."),
]
CELL = [
    ("In a galvanic cell, where does oxidation happen?", "at the anode, which is the negative electrode", ["at the cathode", "in the salt bridge", "at the positive electrode"], "AN OX and RED CAT."),
    ("In a galvanic cell, where does reduction happen?", "at the cathode, which is the positive electrode", ["at the anode", "in the salt bridge", "in the wire"], "Electrons flow from anode to cathode."),
    ("What is the job of a salt bridge?", "to let ions flow and keep each half-cell electrically neutral", ["to carry electrons", "to stop the reaction", "to act as a catalyst"], "It often contains KNO₃."),
    ("Which way do electrons flow in the external circuit of a galvanic cell?", "from the anode to the cathode", ["from the cathode to the anode", "through the salt bridge", "in both directions"], "Anions move towards the anode in the salt bridge."),
    ("What does a more positive standard electrode potential (E°) mean?", "the species is more easily reduced (a stronger oxidising agent)", ["it is more easily oxidised", "it is a stronger reducing agent", "it is a metal"], "F₂ has the most positive E°."),
    ("How is the e.m.f. of a standard cell calculated?", "E°cell = E°(reduction half, cathode) − E°(oxidation half, anode)", ["E°cell = E°anode + E°cathode", "E°cell = E°anode × E°cathode", "E°cell is always 1.5 V"], "A positive E°cell means the reaction is spontaneous."),
    ("What are standard conditions for electrode potentials?", "1 mol/L solutions, 100 kPa for gases and 25 °C", ["any concentration at 100 °C", "pure water at 0 °C", "1 g of each substance"], "The reference is the standard hydrogen electrode (0.00 V)."),
    ("How is an electrolytic cell different from a galvanic cell?", "it uses electrical energy to drive a non-spontaneous reaction", ["it produces electrical energy from a reaction", "it has no electrodes", "it needs no electrolyte"], "Recharging a battery is electrolysis."),
    ("In an electrolytic cell, which electrode is negative?", "the cathode, where reduction happens", ["the anode", "both electrodes", "neither"], "The anode is positive in electrolysis."),
    ("What is produced at the cathode when molten sodium chloride is electrolysed?", "sodium metal", ["chlorine gas", "hydrogen gas", "oxygen gas"], "Chlorine forms at the anode."),
    ("Why is aluminium made by electrolysis rather than by heating its oxide with carbon?", "aluminium is too reactive to be reduced by carbon", ["carbon is too expensive", "aluminium oxide is a gas", "electrolysis is cheaper than heating"], "Bauxite from Queensland and WA is refined to alumina first."),
    ("What is the standard hydrogen electrode?", "the reference half-cell, 2H⁺ + 2e⁻ ⇌ H₂, given E° = 0.00 V", ["a cell with E° = 1.00 V", "a type of battery", "an electrolytic cell"], "All E° values are measured against it."),
    ("Why does a battery go flat?", "the reactants are used up, so the redox reaction can no longer supply a current", ["the electrons are destroyed", "the salt bridge evaporates", "the voltage rises"], "Rechargeable cells can reverse the reaction."),
    ("What is a fuel cell?", "a galvanic cell that is continuously supplied with fuel, such as hydrogen, and oxygen", ["a battery that cannot be recharged", "an electrolytic cell", "a cell that burns fuel"], "The hydrogen fuel cell makes only water."),
    ("What happens in a rechargeable lithium-ion battery during recharging?", "electrical energy forces the reverse (non-spontaneous) reaction, so it acts as an electrolytic cell", ["it produces electricity", "the electrolyte evaporates", "nothing chemical happens"], "Australia mines much of the world's lithium."),
    ("What does the half-equation Cu²⁺ + 2e⁻ → Cu represent?", "reduction", ["oxidation", "neutralisation", "precipitation"], "Electrons are gained."),
]
ORG = [
    ("What is a homologous series?", "a family of compounds with the same functional group and general formula, each differing by CH₂", ["compounds with the same molecular formula", "compounds made from one element", "polymers only"], "Alkanes: CₙH₂ₙ₊₂."),
    ("What is the general formula of the alkenes?", "CₙH₂ₙ", ["CₙH₂ₙ₊₂", "CₙH₂ₙ₋₂", "CₙH₂ₙ₊₁OH"], "Alkenes have one C=C double bond."),
    ("Which test distinguishes an alkene from an alkane?", "bromine water decolourises with an alkene", ["limewater turns milky", "a glowing splint relights", "universal indicator turns green"], "Addition across the C=C bond."),
    ("What type of reaction happens when ethene reacts with hydrogen?", "addition", ["substitution", "elimination", "condensation"], "The double bond breaks."),
    ("What is the functional group of the alcohols?", "hydroxyl, –OH", ["carboxyl, –COOH", "amino, –NH₂", "C=C"], "Ethanol is CH₃CH₂OH."),
    ("What is the functional group of the carboxylic acids?", "carboxyl, –COOH", ["hydroxyl, –OH", "ester, –COO–", "amide, –CONH–"], "Ethanoic acid is in vinegar."),
    ("What are structural isomers?", "compounds with the same molecular formula but different structural formulae", ["compounds with the same structure", "atoms of the same element with different neutrons", "polymers of different lengths"], "Butane and methylpropane are isomers."),
    ("What forms when a primary alcohol is oxidised fully with acidified dichromate?", "a carboxylic acid", ["a ketone", "an alkene", "an ester"], "The orange colour turns green."),
    ("What forms when a secondary alcohol is oxidised?", "a ketone", ["a carboxylic acid", "an aldehyde", "no reaction"], "Tertiary alcohols do not oxidise easily."),
    ("Why do alcohols have higher boiling points than alkanes of similar mass?", "alcohols form hydrogen bonds between molecules", ["alcohols are ionic", "alkanes have stronger dispersion forces", "alcohols have more carbon atoms"], "The –OH group allows hydrogen bonding."),
    ("What is an addition polymer?", "a long chain made by joining many alkene monomers, with no other product", ["a chain that forms with water as a by-product", "a small molecule", "a protein"], "Polyethene comes from ethene."),
    ("What is a condensation polymer?", "a polymer made when monomers join and release a small molecule such as water", ["a polymer made only from alkenes", "a polymer that melts easily", "a mixture of salts"], "Polyesters, nylon and proteins are condensation polymers."),
    ("Which monomer makes polyethene?", "ethene", ["ethane", "ethanol", "ethanoic acid"], "n CH₂=CH₂ → –(CH₂–CH₂)ₙ–"),
    ("What is the IUPAC name of CH₃COOH?", "ethanoic acid", ["methanoic acid", "ethanol", "propanoic acid"], "Two carbons, with the carboxyl carbon counted."),
    ("Which functional group is found in amines?", "amino, –NH₂", ["hydroxyl, –OH", "carboxyl, –COOH", "ester, –COO–"], "Amines are weak bases."),
    ("Which polymer is made from an amine and a carboxylic acid?", "a polyamide such as nylon", ["polyethene", "PVC", "polystyrene"], "Amide links form with loss of water."),
    ("Why are biodegradable polymers such as polylactic acid useful?", "microorganisms can break them down, reducing plastic waste", ["they never break down", "they are made from crude oil only", "they are stronger than steel"], "PLA is made from plant starch."),
    ("Why are many plastics a problem in the environment?", "most do not biodegrade and persist for hundreds of years", ["they dissolve quickly in water", "they are made from metals", "they are always toxic gases"], "Microplastics are found in Australian waters."),
    ("What type of bond joins amino acids in a protein?", "a peptide (amide) bond", ["an ester bond", "a glycosidic bond", "a metallic bond"], "Water is released in a condensation reaction."),
    ("Which property of a polymer increases with longer chains and more cross-links?", "strength and melting point", ["flexibility only", "solubility in water", "electrical conductivity"], "Cross-linked thermosets do not melt."),
]
SYN = [
    ("What is the percentage yield?", "actual yield ÷ theoretical yield × 100", ["theoretical yield ÷ actual yield × 100", "mass of product ÷ mass of reactants", "moles of product × 100"], "Losses lower the yield."),
    ("What is atom economy?", "the mass of the desired product ÷ total mass of all products × 100", ["the actual yield", "the rate of reaction", "the mass of catalyst used"], "Addition reactions have 100% atom economy."),
    ("Why is a high atom economy part of green chemistry?", "less waste is produced, so fewer resources are used", ["it makes reactions faster", "it uses more energy", "it increases waste"], "Green chemistry designs less hazardous processes."),
    ("Which reaction type always has 100% atom economy?", "addition", ["substitution", "elimination", "decomposition"], "All atoms of the reactants end up in one product."),
    ("What is an esterification reaction?", "a carboxylic acid reacts with an alcohol to form an ester and water", ["an alkene reacts with hydrogen", "an alcohol is oxidised", "an ester burns in oxygen"], "Concentrated sulfuric acid is a catalyst."),
    ("What is the name of the ester made from ethanol and ethanoic acid?", "ethyl ethanoate", ["ethanoyl ethyl", "methyl ethanoate", "ethyl methanoate"], "Alcohol part first (-yl), acid part second (-oate)."),
    ("Why is biodiesel made from vegetable oils described as renewable?", "the oils come from crops that can be regrown", ["it is made from crude oil", "it never burns", "it produces no CO₂ at all"], "It is made by transesterification."),
    ("What is the purpose of heating under reflux?", "to heat a reaction for a long time without losing volatile substances", ["to separate a mixture", "to cool a reaction", "to measure a boiling point"], "Vapours condense and drip back."),
    ("What does a mass spectrum's molecular ion peak (M⁺) tell you?", "the relative molecular mass of the compound", ["the number of carbon atoms only", "the functional groups present", "the boiling point"], "The highest m/z peak (ignoring isotopes)."),
    ("What does an infrared spectrum show about an organic compound?", "which functional groups (bonds) are present", ["its molar mass", "the number of hydrogen environments", "its melting point"], "A broad O–H peak near 3300 cm⁻¹ shows an alcohol."),
    ("A broad infrared absorption at 2500–3300 cm⁻¹ together with a strong peak near 1700 cm⁻¹ suggests which functional group?", "a carboxylic acid", ["an alkane", "an alkene", "an ether"], "O–H of an acid and C=O."),
    ("What does the number of peaks in a ¹³C NMR spectrum show?", "the number of different carbon environments", ["the total number of carbon atoms", "the molar mass", "the number of oxygen atoms"], "Symmetry reduces the number of peaks."),
    ("What does chromatography (such as HPLC) separate substances by?", "their different attraction to the stationary and mobile phases", ["their colour only", "their mass only", "their charge only"], "Retention time identifies substances."),
    ("Why do chemists consider yield, rate, cost and safety when designing an industrial process?", "the best process gives enough product quickly, cheaply, safely and with little waste", ["only yield matters", "only rate matters", "cost never matters"], "This involves many compromises."),
]


def u7(X):
    return [
        ("Dynamic equilibrium", [(X.pool(EQ), 8), (X.gen("gen_us_science_chem_chemical_equilibrium", "g_reach"), 8), (X.gen("gen_us_science_chem_chemical_equilibrium", "g_more"), 4)]),
        ("Le Chatelier's principle", [(X.ch("al_chem", KE, 2, 12), 10), (X.gen("gen_us_science_chem_chemical_equilibrium", "g_shift"), 8), (X.pool(EQ), 2)]),
        ("Equilibrium expressions", [(X.ch("al_chem", KE, 3, 12), 18), (X.pool(EQ), 2)]),
        ("Calculating K", [(X.ch("al_chem", KE, 4, 12), 20)]),
        ("Equilibrium amounts and industrial processes", [(X.ch("al_chem", KE, 5, 12), 16), (X.ch("al_chem", KE, 2, 12), 4)]),
    ]


def u8(X):
    al_chem = __import__("al_chem")
    return [
        ("Acids, bases and conjugate pairs", [(X.pool(ACID), 8), (X.ch("in_s11c", "equilibrium", 3), 8), (X.al(al_chem.c_ph, "base"), 4)]),
        ("pH of strong acids and bases", [(X.ch("al_chem", AB, 1, 13), 18), (X.pool(ACID), 2)]),
        ("Weak acids and Ka", [(X.ch("al_chem", AB, 2, 13), 12), (X.ch("in_s11c", "equilibrium", 4), 8)]),
        ("Buffers", [(X.ch("al_chem", AB, 3, 13), 18), (X.pool(ACID), 2)]),
        ("Titrations", [(X.al(al_chem.c_titr), 16), (X.pool(ACID), 4)]),
    ]


def u9(X):
    return [
        ("Oxidation and reduction", [(X.pool(REDOX), 6), (X.ch("in_s11c", "redox-reactions", 3), 10), (X.gen("gen_us_science_chem_types_of_chemical_reactions", "g_act"), 4)]),
        ("Oxidation numbers", [(X.ch("al_chem", RX, 1, 12), 19), (X.pool(REDOX), 1)]),
        ("Half-equations", [(X.ch("al_chem", RX, 2, 12), 19), (X.pool(REDOX), 1)]),
        ("Reactivity and displacement", [(X.gen("gen_us_science_chem_types_of_chemical_reactions", "g_act"), 13), (X.al(__import__("al_chem").c_disp), 6), (X.pool(REDOX), 1)]),
        ("Corrosion and redox titrations", [(X.ch("al_chem", "transition-metals", 4, 13), 18), (X.pool(REDOX), 2)]),
    ]


def u10(X):
    return [
        ("Galvanic cells", [(X.pool(CELL), 6), (X.ch("al_chem", AB, 4, 13), 14)]),
        ("Standard electrode potentials", [(X.ch("al_chem", AB, 4, 13), 18), (X.pool(CELL), 2)]),
        ("Electrolytic cells", [(X.pool(CELL), 4), (X.ch("in_s12c", "electrochemistry", 4, drop=["Kohlrausch", "conductivity", "conductance"]), 10), (X.ch("al_chem", AB, 5, 13, only=[1]), 6)]),
        ("Batteries and fuel cells", [(X.pool(CELL), 2), (X.ch("al_chem", AB, 4, 13), 12), (X.ch("in_s12c", "electrochemistry", 4, drop=["Kohlrausch", "conductivity", "conductance"]), 6)]),
        ("Predicting redox reactions", [(X.ch("al_chem", AB, 5, 13, only=[1]), 12), (X.ch("al_chem", RX, 2, 12), 8)]),
    ]


def u11(X):
    return [
        ("Naming organic compounds", [(X.ch("al_chem", OR, 1, 12), 18), (X.pool(ORG), 2)]),
        ("Formulae and homologous series", [(X.ch("al_chem", OR, 2, 12), 16), (X.pool(ORG), 4)]),
        ("Alkenes and alkynes", [(X.ch("in_s11c", "hydrocarbons", 3), 16), (X.pool(ORG), 4)]),
        ("Functional groups and reactions", [(X.pool(ORG), 4), (X.ch("al_chem", OR, 5, 12), 12), (X.ch("al_chem", OR, 3, 12), 4)]),
        ("Polymers", [(X.pool(ORG), 2), (X.gen("gen_us_science_chem_molecular_structure_and_materials", "g_poly"), 12), (X.ch("al_chem", OR, 4, 12), 6)]),
    ]


def u12(X):
    al_chem = __import__("al_chem")
    return [
        ("Yield and atom economy", [(X.ch("al_chem", "atomic-structure-and-amount-of-substance", 5, 12, only=[0]), 16), (X.pool(SYN), 4)]),
        ("Esters and organic synthesis", [(X.ch("al_chem", FO, 1, 13), 16), (X.pool(SYN), 4)]),
        ("Mass spectrometry and chromatography", [(X.al(al_chem.c_anal, "ms"), 12), (X.al(al_chem.c_anal, "rf"), 6), (X.pool(SYN), 2)]),
        ("NMR spectroscopy", [(X.ch("al_chem", FO, 4, 13), 18), (X.pool(SYN), 2)]),
        ("Infrared and combined analysis", [(X.ch("al_chem", FO, 5, 13), 18), (X.pool(SYN), 2)]),
    ]


def UNITS():
    return [
        SR(CH, 3, 7, "chemical-equilibrium", "Chemical equilibrium systems",
           "Reversible reactions and dynamic equilibrium in closed systems; Le Chatelier's principle for changes in concentration, pressure and temperature; equilibrium constants and the reaction quotient; calculations with K; equilibrium in industry and in natural systems.",
           "Chemical Equilibrium and Le Chatelier's Principle", "chemical equilibrium",
           "Free Year 12 Chemistry worksheets on chemical equilibrium: dynamic equilibrium, Le Chatelier's principle, equilibrium expressions, calculating K, the reaction quotient and the Haber process. 100 questions with answers.",
           "K = [products]^coefficients ÷ [reactants]^coefficients.", "Only temperature changes the value of K.",
           "<p>In a closed system a reversible reaction reaches <b>dynamic equilibrium</b>: forward and reverse rates are equal and concentrations stay constant. <b>Le Chatelier's principle</b>: a change in concentration, pressure or temperature shifts the equilibrium to partly oppose it. A catalyst only makes equilibrium come faster.</p>"
           "<p>For aA + bB ⇌ cC + dD, K = [C]ᶜ[D]ᵈ ÷ [A]ᵃ[B]ᵇ. Compare the reaction quotient Q with K to predict the direction. For an exothermic forward reaction, raising the temperature lowers K.</p>",
           [("H₂ + I₂ ⇌ 2HI: [H₂] = [I₂] = 0.10, [HI] = 0.70 mol/L. K?", ["K = 0.70² ÷ (0.10 × 0.10)"], "49"),
            ("Q = 20, K = 49. Which way does the reaction go?", ["Q < K", "more products needed"], "forward (to the right)")],
           ["Saying the concentrations of reactants and products are equal at equilibrium.", "Thinking a catalyst shifts the equilibrium.", "Putting solids or water in the K expression."],
           [("Why is the Haber process a compromise?", "Low temperature gives a higher yield of ammonia but a slow rate; about 450 °C, high pressure and an iron catalyst give a good yield quickly enough."),
            ("Does changing the concentration change K?", "No. The position of equilibrium shifts, but K changes only with temperature.")],
           u7),
        SR(CH, 3, 8, "acids-bases-and-ph", "Chemical equilibrium systems",
           "Brønsted–Lowry acids and bases, conjugate pairs and amphiprotic species; the self-ionisation of water and Kw; pH of strong acids and bases; weak acids, Ka and pKa; buffers; acid–base titrations, indicators and titration curves.",
           "Acids, Bases, pH and Buffers", "acids, bases and pH",
           "Free Year 12 Chemistry worksheets on acids and bases: conjugate pairs, Kw, pH of strong and weak acids, Ka and pKa, buffers, titrations and indicators. 100 questions with answers.",
           "pH = −log[H₃O⁺]; Kw = [H₃O⁺][OH⁻] = 1.0 × 10⁻¹⁴ at 25 °C.", "A buffer is a weak acid with its conjugate base.",
           "<p>An acid donates a proton and its conjugate base can accept one back. Water self-ionises: Kw = [H₃O⁺][OH⁻] = 1.0 × 10⁻¹⁴ at 25 °C, so pH + pOH = 14.</p>"
           "<p>Strong acids ionise completely, so [H₃O⁺] equals the acid concentration (×2 for H₂SO₄). For weak acids use Ka: [H₃O⁺] ≈ √(Ka × c). Buffers resist pH change. In a titration the indicator must change colour near the equivalence point.</p>",
           [("pH of 0.0010 mol/L KOH?", ["[OH⁻] = 10⁻³", "[H₃O⁺] = 10⁻¹¹"], "11"),
            ("0.10 mol/L acid, Ka = 1.0 × 10⁻⁵. pH?", ["[H₃O⁺] = √(10⁻⁶) = 10⁻³"], "3")],
           ["Using [OH⁻] directly in pH = −log[H₃O⁺].", "Treating a weak acid as fully ionised.", "Choosing phenolphthalein for a strong acid–weak base titration."],
           [("Why does a buffer resist pH change?", "Added H₃O⁺ reacts with the conjugate base, and added OH⁻ reacts with the weak acid, so [H₃O⁺] hardly changes."),
            ("Is pH 7 always neutral?", "Only at 25 °C. Kw changes with temperature, so neutral water is slightly below pH 7 when hot.")],
           u8),
        SR(CH, 3, 9, "oxidation-and-reduction", "Oxidation and reduction",
           "Oxidation and reduction as electron transfer; oxidation numbers; oxidising and reducing agents; half-equations in acid; the reactivity series and displacement reactions; corrosion and its prevention; redox titrations.",
           "Oxidation, Reduction and Half-equations", "oxidation and reduction",
           "Free Year 12 Chemistry worksheets on redox: oxidation numbers, oxidising and reducing agents, half-equations, the reactivity series, displacement, corrosion and redox titrations. 100 questions with answers.",
           "OIL RIG: Oxidation Is Loss, Reduction Is Gain (of electrons).", "Balance half-equations: atoms, then O with H₂O, H with H⁺, charge with e⁻.",
           "<p>Oxidation is the loss of electrons (oxidation number goes up); reduction is the gain of electrons (oxidation number goes down). The <b>oxidising agent</b> is reduced; the <b>reducing agent</b> is oxidised.</p>"
           "<p>A more reactive metal displaces a less reactive one from solution. To balance a half-equation in acid: balance the element, add H₂O for oxygen, H⁺ for hydrogen and electrons for charge. Corrosion is oxidation of metals; sacrificial anodes and galvanising protect steel.</p>",
           [("Oxidation number of Mn in MnO₄⁻?", ["x + 4 × (−2) = −1"], "+7"),
            ("Balance MnO₄⁻ → Mn²⁺ in acid", ["add 4H₂O on the right", "add 8H⁺ on the left", "add 5e⁻ on the left"], "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O")],
           ["Saying the oxidising agent is oxidised.", "Forgetting to balance charge with electrons.", "Thinking a less reactive metal can displace a more reactive one."],
           [("How do you identify oxidation and reduction?", "Work out oxidation numbers: the element whose number rises is oxidised; the one whose number falls is reduced."),
            ("Why does galvanised iron not rust even when scratched?", "Zinc is more reactive, so it is oxidised instead of the iron (sacrificial protection).")],
           u9),
        SR(CH, 3, 10, "electrochemical-cells", "Oxidation and reduction",
           "Galvanic cells: anode, cathode, salt bridge and electron flow; standard electrode potentials and the electrochemical series; calculating cell e.m.f.; electrolytic cells and electrolysis; batteries, rechargeable cells and fuel cells.",
           "Galvanic and Electrolytic Cells", "electrochemical cells",
           "Free Year 12 Chemistry worksheets on electrochemistry: galvanic cells, salt bridges, standard electrode potentials, cell e.m.f., electrolysis, batteries and fuel cells. 100 questions with answers.",
           "AN OX, RED CAT: oxidation at the anode, reduction at the cathode.", "E°cell = E°cathode − E°anode.",
           "<p>In a <b>galvanic cell</b> a spontaneous redox reaction makes electricity: oxidation at the anode (negative), reduction at the cathode (positive), electrons through the wire and ions through the salt bridge. The half-cell with the more positive E° is the cathode.</p>"
           "<p>An <b>electrolytic cell</b> uses electricity to drive a non-spontaneous reaction; here the anode is positive. Rechargeable batteries act as galvanic cells when discharging and electrolytic cells when charging. Fuel cells run on a supply of fuel such as hydrogen.</p>",
           [("Zn²⁺/Zn −0.76 V and Cu²⁺/Cu +0.34 V. E°cell?", ["cathode Cu, anode Zn", "0.34 − (−0.76)"], "1.10 V"),
            ("Which electrode is negative in that cell?", ["Zn is oxidised"], "the zinc anode")],
           ["Thinking the anode is always positive: it is negative in a galvanic cell.", "Saying electrons move through the salt bridge.", "Subtracting the E° values the wrong way round."],
           [("What is the difference between a galvanic and an electrolytic cell?", "A galvanic cell turns chemical energy into electrical energy with a spontaneous reaction; an electrolytic cell uses electrical energy to force a non-spontaneous reaction."),
            ("Why are hydrogen fuel cells described as clean?", "The only product is water. But the hydrogen must be made cleanly, for example by electrolysis using solar or wind power.")],
           u10),
        SR(CH, 4, 11, "organic-chemistry", "Properties and structure of organic materials",
           "Homologous series and functional groups (alkanes, alkenes, alcohols, carboxylic acids, esters, amines, amides); IUPAC naming; structural isomers; physical properties and intermolecular forces; addition, substitution and oxidation reactions; addition and condensation polymers.",
           "Organic Chemistry: Naming, Isomers and Polymers", "organic chemistry",
           "Free Year 12 Chemistry worksheets on organic chemistry: homologous series, functional groups, IUPAC names, isomers, addition and substitution reactions, oxidation of alcohols and polymers. 100 questions with answers.",
           "Name = prefix (chain length) + suffix (functional group).", "meth-1, eth-2, prop-3, but-4, pent-5, hex-6.",
           "<p>Organic compounds are grouped into <b>homologous series</b> with the same functional group: alkanes (C–C), alkenes (C=C), alcohols (–OH), carboxylic acids (–COOH), esters (–COO–), amines (–NH₂). IUPAC names give the longest chain, the position of the functional group and any branches.</p>"
           "<p>Alkenes undergo <b>addition</b>; alkanes undergo substitution; primary alcohols oxidise to carboxylic acids. Alkenes join into <b>addition polymers</b>; monomers with two functional groups form <b>condensation polymers</b> such as polyesters and proteins.</p>",
           [("Name CH₃CH₂CH₂OH", ["3 carbons: prop-", "OH on carbon 1"], "propan-1-ol"),
            ("Molecular formula of the alkane with 5 carbons?", ["CₙH₂ₙ₊₂, n = 5"], "C₅H₁₂")],
           ["Numbering the chain from the wrong end.", "Thinking isomers must have the same structure.", "Saying polymerisation of ethene releases water."],
           [("Why do short-chain alcohols dissolve in water but alkanes do not?", "The –OH group forms hydrogen bonds with water; alkanes are non-polar and cannot."),
            ("What is the difference between addition and condensation polymers?", "Addition polymers form from alkenes with no other product; condensation polymers form from monomers with two functional groups and release a small molecule such as water.")],
           u11),
        SR(CH, 4, 12, "chemical-synthesis-and-analysis", "Chemical synthesis and design",
           "Percentage yield and atom economy; green chemistry; esterification and organic synthesis pathways; reflux and purification; identifying compounds with mass spectrometry, infrared spectroscopy, NMR spectroscopy and chromatography.",
           "Chemical Synthesis, Yield and Spectroscopy", "chemical synthesis and analysis",
           "Free Year 12 Chemistry worksheets on synthesis and analysis: percentage yield, atom economy, green chemistry, esters, mass spectra, infrared and NMR spectroscopy and chromatography. 100 questions with answers.",
           "% yield = actual ÷ theoretical × 100.", "Atom economy = mass of desired product ÷ mass of all products × 100.",
           "<p>Chemists design syntheses for a high <b>yield</b> and a high <b>atom economy</b>, with safe, cheap and renewable inputs (green chemistry). Esters form from carboxylic acids and alcohols; reactions are often heated under reflux and the product purified by distillation.</p>"
           "<p>Products are identified by instruments: <b>mass spectrometry</b> gives molar mass and fragments; <b>infrared</b> shows functional groups (O–H, C=O); <b>NMR</b> shows the carbon and hydrogen environments and splitting patterns; <b>chromatography</b> separates and identifies substances.</p>",
           [("Theoretical 12.0 g, actual 9.0 g. % yield?", ["9.0 ÷ 12.0 × 100"], "75%"),
            ("Ethyl ethanoate: which acid and alcohol?", ["-oate from the acid", "ethyl from the alcohol"], "ethanoic acid and ethanol")],
           ["Confusing percentage yield with atom economy.", "Thinking the number of ¹³C NMR peaks equals the number of carbons.", "Naming esters with the acid part first."],
           [("Why can a reaction have a high yield but a low atom economy?", "Yield compares the product you got with the most possible; atom economy shows how much of the reactants end up in the product you want rather than in by-products."),
            ("Which technique tells you the functional groups present?", "Infrared spectroscopy: bonds such as O–H, C=O and N–H absorb at characteristic wavenumbers.")],
           u12),
    ]
