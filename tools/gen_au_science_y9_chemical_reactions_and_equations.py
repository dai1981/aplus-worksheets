# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U07: modelling the rearrangement of atoms in chemical reactions with word
equations, balanced symbol equations and models; conservation of mass; combustion and the reactions of acids with metals,
bases and carbonates; acids, bases and the pH scale.
  python tools/gen_au_science_y9_chemical_reactions_and_equations.py
Reuses the US Chemistry balancing equations makers, the SG Secondary 2 acids and alkalis makers and the UK Year 7 acids and
alkalis and Year 8 chemical reactions makers with Australian names, plus own questions on salts and Australian contexts.
Wrong answers come from real mistakes: changing subscripts to balance an equation, thinking pH 7 is acidic, and forgetting the
gas in the products of an acid and a carbonate.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

BA = "gen_us_science_chem_balancing_chemical_equations"
SA = "gen_sg_science_s2_acids_and_alkalis"
KA = "gen_uk_science_y7_acids_and_alkalis"
K8 = "gen_uk_science_y8_chemical_reactions"
b_check = limit(src(BA, "g_check", drop=[r"\b1 atoms\b"]), 8)
b_count = limit(src(BA, "g_count"), 6)
b_mass = limit(src(BA, "g_mass"), 5)
b_miss = limit(src(BA, "g_missing"), 6)
b_pick = limit(src(BA, "g_pick"), 4)
b_b1 = src.B(BA, "B1")
b_b5 = src.B(BA, "B5")
s_rx = src(SA, "g_rx")
s_ph = limit(src(SA, "g_ph"), 7)
s_b1 = src.B(SA, "B1")
s_b5 = src.B(SA, "B5")
k_salt = src(KA, "g_salt")
k_ui = limit(src(KA, "g_ui"), 7)
k_b5 = src.B(KA, "B5")
k_burn = src(K8, "g_burn")

POOL1 = pool(R, [
    ("Why must a chemical equation be balanced?", "Atoms are not created or destroyed, so each side must have the same number of each atom.", ["To make it look neat.", "Because mass is lost.", "Because products are heavier."], "This shows conservation of mass."),
    ("Which change is NOT allowed when balancing an equation?", "changing the small numbers (subscripts) in a formula", ["adding a big number in front of a formula", "counting atoms", "checking both sides"], "Changing H₂O to H₂O₂ makes a different substance."),
    ("Write the word equation for an acid reacting with a metal.", "acid + metal → salt + hydrogen", ["acid + metal → salt + water", "acid + metal → water + carbon dioxide", "acid + metal → oxygen"], "Hydrogen 'pops' with a lit splint."),
    ("Write the word equation for an acid reacting with a carbonate.", "acid + carbonate → salt + water + carbon dioxide", ["acid + carbonate → salt + hydrogen", "acid + carbonate → water only", "acid + carbonate → oxygen + salt"], "The fizzing is carbon dioxide."),
    ("Write the word equation for an acid reacting with a base (neutralisation).", "acid + base → salt + water", ["acid + base → hydrogen", "acid + base → carbon dioxide only", "acid + base → acid"], "The products are neutral."),
    ("What is the balanced equation for the complete combustion of methane?", "CH₄ + 2O₂ → CO₂ + 2H₂O", ["CH₄ + O₂ → CO₂ + H₂O", "CH₄ + O₂ → C + H₂O", "CH₄ → CO₂ + H₂"], "1 C, 4 H and 4 O on each side."),
    ("What pH does a neutral solution have?", "7", ["0", "1", "14"], "Below 7 is acidic; above 7 is basic."),
    ("Which salt forms when hydrochloric acid reacts with sodium hydroxide?", "sodium chloride", ["sodium sulfate", "sodium nitrate", "chlorine hydroxide"], "Hydrochloric acid makes chloride salts."),
    ("Which salt forms when sulfuric acid reacts with magnesium?", "magnesium sulfate", ["magnesium chloride", "magnesium nitrate", "magnesium oxide"], "Sulfuric acid makes sulfate salts."),
    ("Farmers in Western Australia spread lime (calcium carbonate) on acidic soils. Why?", "It neutralises the acid in the soil.", ["It makes the soil more acidic.", "It adds hydrogen.", "It is a fertiliser only."], "Soil acidity is a big problem in WA wheat belts."),
    ("Why do people take antacid tablets for heartburn?", "They are bases that neutralise excess stomach acid.", ["They are acids.", "They add more acid.", "They change the pH to 1."], "Stomach acid is hydrochloric acid."),
    ("In 2Mg + O₂ → 2MgO, how many oxygen atoms are on each side?", "2", ["1", "4", "3"], "O₂ has 2; 2MgO has 2."),
])
POOL5 = pool(R, [
    ("Mia reacts 2.4 g of magnesium with acid in an open flask. The flask loses 0.2 g. Why?", "Hydrogen gas escaped into the air.", ["Magnesium was destroyed.", "The flask lost glass.", "Mass is not conserved in reactions."], "In a closed flask the mass would stay the same."),
    ("Jack adds drops of indicator to vinegar, water and bicarb soda solution. Which will show the highest pH?", "the bicarb soda solution", ["vinegar", "water", "all the same"], "Bicarb soda solution is weakly basic."),
    ("Ruby adds marble chips to acid and records the mass every minute. The mass falls quickly, then slowly, then stops. Why does it stop?", "The acid or marble has been used up, so no more carbon dioxide is made.", ["Mass starts to be created.", "The balance breaks.", "The reaction speeds up."], "Reactions stop when a reactant runs out."),
    ("Kai tests a gas from acid and zinc with a lit splint. It makes a squeaky pop. What is the gas?", "hydrogen", ["oxygen", "carbon dioxide", "nitrogen"], "Oxygen relights a glowing splint; CO₂ turns limewater milky."),
    ("Ella adds sodium hydroxide drop by drop to acid with universal indicator. The colour changes from red to green. What has happened?", "The acid has been neutralised (pH 7).", ["It became more acidic.", "It became strongly basic.", "No reaction happened."], "Green means neutral."),
    ("Noah builds a ball-and-stick model of 2H₂ + O₂ → 2H₂O. How many hydrogen balls does he need on each side?", "4", ["2", "6", "1"], "2H₂ has 4 hydrogen atoms; 2H₂O has 4."),
    ("Zara tests which antacid neutralises the most acid by counting drops of acid until the colour changes. What must she keep the same?", "the mass of each antacid and the volume of water", ["the type of antacid", "the number of drops", "nothing"], "Only the antacid should change."),
    ("Liam burns a candle under a glass jar. The flame goes out. Why?", "The oxygen in the jar has been used up.", ["The jar adds oxygen.", "Carbon dioxide is a fuel.", "Candles need no oxygen."], "Combustion needs oxygen."),
])


def main():
    sets = U.sets([
        ("Word and symbol equations", [(POOL1, 5), (b_count, 6), (b_pick, 4), (b_b1, 3), (k_burn, 2)]),
        ("Balancing equations", [(b_check, 6), (b_miss, 6), (b_count, 2), (POOL1, 3), (b_mass, 3)]),
        ("Conservation of mass", [(b_mass, 6), (b_b1, 3), (POOL1, 3), (k_burn, 3), (POOL5, 3), (b_miss, 2)]),
        ("Acids, bases and their reactions", [(s_rx, 5), (k_salt, 5), (s_ph, 3), (k_ui, 3), (s_b1, 3), (POOL1, 1)]),
        ("Investigations", [(POOL5, 5), (b_b5, 4), (s_b5, 4), (k_b5, 4), (k_ui, 1), (s_ph, 2), (b_check, 1)]),
    ])
    make_au(YEAR, "chemical-reactions-and-equations", SORT, "AC9S9U07", "Chemical sciences",
            "Model the rearrangement of atoms in chemical reactions using a range of representations, including word and simple "
            "balanced chemical equations, and use these to explain the law of conservation of mass; including combustion and the "
            "reactions of acids (summary of the Australian Curriculum v9.0 Science content description).",
            "Chemical Reactions and Equations", "Chemical equations",
            "Free Year 9 science worksheets on chemical reactions: word and balanced symbol equations, conservation of mass, combustion, "
            "acids and bases, pH, neutralisation and reactions of acids with metals and carbonates. 100 questions with answers.",
            "Balance atoms, not subscripts.", "Atoms are rearranged in a reaction, so each element has the same number of atoms on both sides.",
            "<p><b>In a chemical reaction, atoms are rearranged into new substances.</b></p><ul>"
            "<li>Word equation: reactants → products. A balanced symbol equation shows the same number of each atom on both sides.</li>"
            "<li>Balance by putting numbers in front of formulas; never change the small subscripts.</li>"
            "<li>Acid + metal → salt + hydrogen; acid + base → salt + water; acid + carbonate → salt + water + carbon dioxide.</li></ul>",
            [("Balance: H₂ + O₂ → H₂O", ["2 O on the left", "make 2H₂O", "then 2H₂"], "2H₂ + O₂ → 2H₂O"),
             ("Hydrochloric acid + zinc → ?", ["acid + metal → salt + hydrogen"], "zinc chloride + hydrogen")],
            ["Changing subscripts (H₂O to H₂O₂) to balance an equation.", "Thinking pH 7 is acidic (it is neutral).",
             "Leaving out carbon dioxide when an acid reacts with a carbonate."],
            [("How do I balance a chemical equation?", "Count each type of atom on both sides. Put whole numbers (coefficients) in front of formulas until every element matches. Never change the subscripts."),
             ("Why does mass seem to change in some reactions?", "If a gas escapes from an open container or joins from the air, the measured mass changes. In a closed system the total mass stays the same."),
             ("What is neutralisation?", "It is the reaction of an acid with a base to make a salt and water. Antacids and lime for soil both work by neutralisation.")],
            sets)


if __name__ == "__main__":
    main()
