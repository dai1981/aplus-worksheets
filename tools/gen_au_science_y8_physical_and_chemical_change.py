# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U07: physical and chemical change - indicators of a chemical change, energy
changes in reactions, word equations, combustion and corrosion, and conservation of mass.
  python tools/gen_au_science_y8_physical_and_chemical_change.py
Reuses the US Grade 5 and Grade 7 change makers, the UK Year 8 chemical reactions makers and the SG Secondary 2 chemical
changes makers with Australian names, plus own questions on bushfires, rusting near the coast and campfire cooking.
Wrong answers come from real mistakes: calling every change of state or colour a chemical change, thinking mass is lost when a
gas escapes from an open container, and thinking dissolving makes a new substance.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

G5 = "gen_us_science_g5_physical_and_chemical_changes"
G7 = "gen_us_science_g7_properties_and_chemical_reactions"
K8 = "gen_uk_science_y8_chemical_reactions"
S2 = "gen_sg_science_s2_chemical_changes"
a_class = limit(src(G5, "g_classify"), 8)
a_chem = limit(src(G5, "g_which_chem"), 6)
a_phys = limit(src(G5, "g_which_phys"), 6)
a_sign = src(G5, "g_sign_example")
a_mass = limit(src(G5, "g_mass_hint"), 5)
a_b2 = src.B(G5, "B2")
a_b5 = src.B(G5, "B5")
b_kind = limit(src(G7, "g_kind"), 6)
b_which = limit(src(G7, "g_which"), 6)
b_b1 = src.B(G7, "B1")
k_burn = src(K8, "g_burn")
k_cons = src(K8, "g_cons")
k_sign = src(K8, "g_sign")
k_type = src(K8, "g_type")
k_b5 = src.B(K8, "B5")
s_cause = src(S2, "g_cause")
s_ch = src(S2, "g_ch")
s_mass = src(S2, "g_mass")
s_we = src(S2, "g_we")
s_b1 = src.B(S2, "B1")
s_b5 = src.B(S2, "B5")

POOL1 = pool(R, [
    ("What is the main difference between a physical change and a chemical change?", "A chemical change makes a new substance; a physical change does not.", ["A physical change always involves heat.", "A chemical change can always be reversed.", "There is no difference."], "Melting ice is still water."),
    ("Which is an indicator of a chemical change?", "an unexpected colour change and a gas forming", ["a solid melting", "sugar dissolving", "water boiling"], "Colour, gas, light, heat or a precipitate can show a new substance."),
    ("In a bushfire, eucalyptus trees burn. What kind of change is this?", "a chemical change: wood reacts with oxygen to make carbon dioxide, water and ash", ["a physical change: the wood melts", "a physical change: the wood dissolves", "no change"], "Burning (combustion) is a chemical change."),
    ("Why does a steel boat trailer rust faster near the beach at the Gold Coast?", "Salty, damp air speeds up the reaction of iron with oxygen and water.", ["Sand is a metal.", "Salt stops rusting.", "Sunlight turns iron into rust."], "Rusting is a chemical change that needs oxygen and water."),
    ("What is an exothermic reaction?", "a reaction that releases energy to the surroundings, so they get warmer", ["a reaction that takes in heat", "a reaction with no energy change", "a reaction that only happens in the cold"], "Burning is exothermic."),
    ("What is an endothermic reaction?", "a reaction that takes in energy, so the surroundings get colder", ["a reaction that gives out heat", "a reaction that makes light only", "a physical change"], "A sports cold pack gets cold because the reaction is endothermic."),
    ("Write the word equation for burning methane (natural gas).", "methane + oxygen → carbon dioxide + water", ["methane → oxygen + water", "carbon dioxide + water → methane", "methane + water → oxygen"], "Reactants are on the left, products on the right."),
    ("What are the reactants in: magnesium + oxygen → magnesium oxide?", "magnesium and oxygen", ["magnesium oxide", "oxygen only", "magnesium oxide and oxygen"], "Reactants are the starting substances."),
    ("Dissolving sugar in water: physical or chemical change?", "physical: the sugar can be recovered by evaporating the water", ["chemical: the sugar disappears", "chemical: a new substance forms", "neither"], "Dissolving does not make a new substance."),
    ("Cooking a sausage on a barbecue: physical or chemical change?", "chemical: new substances form and it cannot be uncooked", ["physical: it only gets hot", "physical: it changes state", "neither"], "Cooking food is a chemical change."),
])
POOL5 = pool(R, [
    ("Mia mixes vinegar and bicarb soda in an open beaker. The mass drops from 150 g to 146 g. Why?", "Carbon dioxide gas escaped into the air.", ["Mass was destroyed.", "The beaker lost mass.", "The scale was broken."], "In a closed container, the mass would stay the same."),
    ("Jack repeats the test in a sealed bag. What will happen to the total mass?", "It stays the same.", ["It increases.", "It decreases.", "It becomes zero."], "Atoms are rearranged, not created or destroyed."),
    ("Ruby measures the temperature of a reaction: 21 °C at the start, 29 °C after 2 minutes. What does this show?", "The reaction is exothermic.", ["The reaction is endothermic.", "No reaction happened.", "The thermometer is broken."], "The temperature rose, so energy was released."),
    ("Kai puts iron nails in tap water, salt water and dry air for a week. Which nail rusts most?", "the nail in salt water", ["the nail in dry air", "all the same", "none rust"], "Salt speeds up rusting; dry air slows it."),
    ("Ella wants a fair test of how temperature affects how fast a tablet fizzes. What should she keep the same?", "the volume of water and the size of the tablet", ["the water temperature", "nothing", "the time she measures"], "Only the temperature should change."),
    ("Noah heats copper carbonate. It turns from green to black and a gas is given off. What evidence shows a chemical change?", "the colour change and the gas", ["the copper carbonate got hot", "the test tube was glass", "the solid was green"], "A new substance (copper oxide) formed."),
    ("Zara burns 1 g of magnesium ribbon and collects all the ash. It has a mass of about 1.7 g. Why is it heavier?", "Oxygen from the air joined with the magnesium.", ["Mass was created.", "The ash absorbed water only.", "Magnesium is lighter when hot."], "Magnesium oxide includes the oxygen atoms."),
    ("Liam sees ice melt and says 'a chemical change happened because it looks different'. What is wrong?", "Melting is a change of state; no new substance forms.", ["Nothing is wrong.", "Melting makes hydrogen.", "Ice is a compound that breaks down."], "Changes of state are physical."),
])


def main():
    sets = U.sets([
        ("Physical or chemical?", [(a_class, 6), (a_chem, 4), (a_phys, 4), (b_kind, 3), (POOL1, 3)]),
        ("Indicators of a chemical change", [(a_sign, 6), (k_sign, 5), (b_which, 4), (b_b1, 3), (POOL1, 2)]),
        ("Word equations and reaction types", [(s_we, 7), (k_type, 6), (k_burn, 4), (POOL1, 3)]),
        ("Energy and conservation of mass", [(s_mass, 6), (k_cons, 5), (a_mass, 3), (s_cause, 3), (POOL1, 3)]),
        ("Investigations", [(POOL5, 8), (a_b5, 4), (s_b5, 3), (k_b5, 3), (s_ch, 2)]),
    ])
    make_au(YEAR, "physical-and-chemical-change", SORT, "AC9S8U07", "Chemical sciences",
            "Compare physical and chemical changes, identify indicators of energy change in chemical reactions, and use word equations "
            "to show that atoms are rearranged and mass is conserved (summary of the Australian Curriculum v9.0 Science content description).",
            "Physical and Chemical Change", "Physical and chemical change",
            "Free Year 8 science worksheets on physical and chemical change: indicators of a reaction, exothermic and endothermic reactions, "
            "word equations, combustion, rusting and conservation of mass. 100 questions with answers.",
            "Is a new substance made?", "A chemical change makes a new substance; a physical change does not.",
            "<p><b>Ask: has a new substance been made?</b></p><ul>"
            "<li>Physical changes (melting, dissolving, cutting) do not make new substances and are often easy to reverse.</li>"
            "<li>Indicators of a chemical change: gas, an unexpected colour change, light, a temperature change, or a solid (precipitate).</li>"
            "<li>Word equation: reactants → products. Atoms are rearranged, so the total mass stays the same in a closed container.</li></ul>",
            [("Wood burns in a campfire. Physical or chemical?", ["ash, smoke and gases form"], "chemical"),
             ("A reaction in an open beaker loses 3 g. Why?", ["a gas escaped"], "the mass went into the air")],
            ["Calling melting or dissolving a chemical change.", "Thinking mass is destroyed when a gas escapes.",
             "Thinking every colour change is a reaction (mixing paints is physical)."],
            [("How do I tell a physical change from a chemical change?", "Ask whether a new substance has formed. Look for gas, light, a temperature change, an unexpected colour change or a precipitate."),
             ("Why does mass seem to change in some reactions?", "If a gas escapes or joins from the air, the mass in the open container changes. In a sealed container, the total mass stays the same."),
             ("What is the difference between exothermic and endothermic?", "Exothermic reactions release energy, so the surroundings warm up. Endothermic reactions take in energy, so the surroundings cool down.")],
            sets)


if __name__ == "__main__":
    main()
