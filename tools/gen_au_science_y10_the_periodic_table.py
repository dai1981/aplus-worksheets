# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U06: how the structure of atoms (electron shells and valence electrons) relates
to the organisation of the periodic table - groups and periods, metals, non-metals and metalloids, the alkali metals, halogens
and noble gases, trends in reactivity, and the history of the table.
  python tools/gen_au_science_y10_the_periodic_table.py
Reuses the US Chemistry periodic table makers, the SG Secondary 4 patterns in the periodic table makers and the UK Year 10
atomic structure and periodic table makers with Australian names, plus own questions on Mendeleev and Australian resources
(lithium, rare earths).
Wrong answers come from real mistakes: thinking the period number is the number of valence electrons, thinking reactivity
increases up group 1, and thinking noble gases react easily.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

PT = "gen_us_science_chem_periodic_table_and_trends"
SG = "gen_sg_science_s4_patterns_in_the_periodic_table"
K10 = "gen_uk_science_y10_atomic_structure_and_the_periodic_table"
NO = ["ionization", "ionisation", "electronegativ", "Group VII", "Group I\\b", "Group 0", "d-block", "lanthan"]
p_class = limit(src(PT, "g_class", drop=NO), 5)
p_fam = limit(src(PT, "g_fam", drop=NO), 6)
p_loc = limit(src(PT, "g_loc", drop=NO), 5)
p_react = src(PT, "g_react", drop=NO)
p_trend = limit(src(PT, "g_trend", drop=NO), 9)
p_val = limit(src(PT, "g_val", drop=NO), 10)
p_b1 = src.B(PT, "B1", drop=NO)
p_b5 = src.B(PT, "B5", drop=NO)
s_g1 = limit(src(SG, "g_g1", drop=NO), 5)
s_g17 = src(SG, "g_g17", drop=NO)
k_hist = src(K10, "g_hist", drop=NO)
k_b1 = src.B(K10, "B1", drop=NO)
k_b5 = src.B(K10, "B5", drop=NO)

POOL1 = pool(R, [
    ("How is the modern periodic table arranged?", "in order of increasing atomic number", ["in order of atomic mass only", "alphabetically", "by the date of discovery"], "Elements with similar properties line up in groups."),
    ("What do elements in the same group have in common?", "the same number of valence (outer-shell) electrons", ["the same number of shells", "the same mass", "the same number of neutrons"], "This gives them similar chemical properties."),
    ("What does the period number tell you?", "the number of occupied electron shells", ["the number of valence electrons", "the number of neutrons", "the mass number"], "Period 3 elements have 3 shells."),
    ("Why did Mendeleev leave gaps in his periodic table in 1869?", "He predicted elements that had not yet been discovered.", ["He ran out of space.", "He made a mistake.", "Those elements were too dangerous."], "Gallium and germanium were later found to fit."),
    ("Why are the noble gases (group 18) so unreactive?", "They have a full outer shell of electrons.", ["They have no electrons.", "They are metals.", "They have one valence electron."], "Helium, neon and argon are used where reactions must be avoided."),
    ("How does reactivity change down group 1 (the alkali metals)?", "It increases.", ["It decreases.", "It stays the same.", "It drops to zero."], "The outer electron is further from the nucleus, so it is lost more easily."),
    ("How does reactivity change down group 17 (the halogens)?", "It decreases.", ["It increases.", "It stays the same.", "It changes randomly."], "Fluorine is the most reactive halogen."),
    ("Where are the metals on the periodic table?", "on the left and in the middle", ["only on the right", "only in the top row", "in group 18"], "Non-metals are on the right."),
    ("What are metalloids such as silicon?", "elements with properties between metals and non-metals", ["the most reactive metals", "noble gases", "radioactive elements only"], "Silicon is used in computer chips and solar cells."),
    ("Australia is one of the world's biggest producers of lithium. Which group is lithium in?", "group 1", ["group 2", "group 17", "group 18"], "Lithium is used in rechargeable batteries."),
    ("Sodium has 11 electrons arranged 2, 8, 1. Which group is it in?", "group 1", ["group 3", "group 11", "group 8"], "One valence electron means group 1."),
    ("Why do group 1 metals form ions with a 1+ charge?", "They lose their single valence electron.", ["They gain one electron.", "They lose all their electrons.", "They share electrons."], "This gives them a full outer shell."),
])
POOL5 = pool(R, [
    ("Mia watches a teacher add lithium, sodium and potassium to water. Potassium reacts most violently. What trend does this show?", "Reactivity increases down group 1.", ["Reactivity decreases down group 1.", "All group 1 metals react the same.", "Potassium is not a metal."], "Potassium has the outermost electron furthest from the nucleus."),
    ("Why are alkali metals stored under oil?", "to stop them reacting with oxygen and water in the air", ["to keep them warm", "to make them shiny", "to stop them melting"], "They react quickly with moisture."),
    ("Jack predicts the properties of caesium, below potassium in group 1. Which prediction is best?", "It will react even more violently with water.", ["It will not react with water.", "It will be a gas.", "It will be a halogen."], "Trends help predict properties."),
    ("Ruby bubbles chlorine through potassium bromide solution and it turns orange. What happened?", "Chlorine displaced bromine because chlorine is more reactive.", ["Bromine displaced chlorine.", "No reaction happened.", "Potassium turned orange."], "A more reactive halogen displaces a less reactive one."),
    ("Kai tests the conductivity of samples of copper, sulfur and silicon. Silicon conducts a little. What does this suggest?", "Silicon is a metalloid (semiconductor).", ["Silicon is a metal.", "Silicon is a noble gas.", "Sulfur is a metal."], "Metalloids have in-between properties."),
    ("Ella reads that Australia mines rare earth elements used in magnets for wind turbines. Why is the periodic table useful to the geologists?", "It helps predict which elements occur together because of similar properties.", ["It shows where mines are.", "It tells the price of metals.", "It is not useful."], "Similar elements are often found together."),
])


def main():
    sets = U.sets([
        ("Organising the periodic table", [(POOL1, 6), (k_hist, 6), (k_b1, 4), (p_b1, 4)]),
        ("Electron shells and groups", [(p_val, 6), (p_loc, 5), (POOL1, 4), (p_class, 3), (p_fam, 2)]),
        ("Metals, non-metals and families", [(p_class, 2), (p_fam, 4), (s_g1, 5), (s_g17, 5), (POOL1, 2), (p_react, 2)]),
        ("Trends and reactivity", [(p_trend, 5), (p_react, 5), (s_g1, 2), (s_g17, 3), (p_loc, 2), (POOL5, 3)]),
        ("Investigations", [(POOL5, 3), (p_b5, 5), (k_b5, 4), (p_trend, 3), (p_val, 3), (k_hist, 2)]),
    ])
    make_au(YEAR, "the-periodic-table", SORT, "AC9S10U06", "Chemical sciences",
            "Explain how the structure and properties of atoms relate to the organisation of the elements in the periodic table "
            "(Australian Curriculum v9.0 Science content description).",
            "The Periodic Table", "The periodic table",
            "Free Year 10 science worksheets on the periodic table: groups and periods, electron shells and valence electrons, "
            "metals, non-metals and metalloids, alkali metals, halogens, noble gases and reactivity trends. 100 questions with answers.",
            "Same group, same outer electrons.", "Elements in a group have the same number of valence electrons, so they react in similar ways.",
            "<p><b>The periodic table arranges elements by atomic number.</b></p><ul>"
            "<li>Groups (columns): same number of valence electrons and similar properties. Periods (rows): same number of shells.</li>"
            "<li>Metals are on the left and middle, non-metals on the right, metalloids along the staircase between them.</li>"
            "<li>Group 1 gets more reactive down the group; group 17 gets less reactive; group 18 (noble gases) hardly react.</li></ul>",
            [("Chlorine: 17 electrons. Arrangement and group?", ["2, 8, 7", "7 valence electrons"], "group 17, period 3"),
             ("Which is more reactive: sodium or potassium?", ["potassium is lower in group 1"], "potassium")],
            ["Thinking the period number is the number of valence electrons.", "Thinking reactivity increases up group 1.",
             "Thinking noble gases react easily."],
            [("Why do elements in the same group react in similar ways?", "They have the same number of electrons in their outer shell, and these valence electrons decide how an atom reacts."),
             ("Why is the periodic table arranged by atomic number, not mass?", "Arranging by atomic number (number of protons) puts every element in a group with similar properties. Mass order had some elements in the wrong place."),
             ("What did Mendeleev do?", "In 1869 he arranged the known elements by their properties and left gaps for undiscovered elements, predicting their properties correctly.")],
            sets)


if __name__ == "__main__":
    main()
