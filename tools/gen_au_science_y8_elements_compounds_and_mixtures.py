# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U06: elements, compounds and mixtures - atoms and molecules, chemical symbols
and formulas, metals and non-metals, and pure substances compared with mixtures.
  python tools/gen_au_science_y8_elements_compounds_and_mixtures.py
Reuses the UK Year 7 elements makers and the SG Secondary 1 elements, compounds and mixtures and atoms and molecules makers
with Australian names, plus own particle diagrams and questions on Australian minerals and salt lakes.
Wrong answers come from real mistakes: calling a molecule of an element a compound, thinking a mixture has a fixed ratio,
and counting the subscript as belonging to the next symbol.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

E7 = "gen_uk_science_y7_elements_atoms_and_compounds"
S1 = "gen_sg_science_s1_elements_compounds_and_mixtures"
A1 = "gen_sg_science_s1_atoms_and_molecules"
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
FX = [(r"(?<=[A-Za-z)])(\d+)", lambda m: m.group(1).translate(SUB))]
NOATOM = ["proton", "neutron", "electron", "nucle", "Dalton", "models of the atom", "Melamine"]
u_class = src(E7, "g_class", rep=FX, drop=NOATOM)
u_count = limit(src(E7, "g_count", rep=FX, drop=NOATOM), 8)
u_name = src(E7, "g_name", rep=FX, drop=NOATOM)
u_sym = limit(src(E7, "g_sym", rep=FX, drop=NOATOM), 8)
u_b1 = src.B(E7, "B1", rep=FX, drop=NOATOM)
u_b5 = src.B(E7, "B5", rep=FX, drop=NOATOM)
s_metal = limit(src(S1, "g_metal", rep=FX, drop=NOATOM), 7)
s_sol = src(S1, "g_sol")
s_susp = src(S1, "g_susp")
s_b1 = src.B(S1, "B1", rep=FX, drop=NOATOM)
s_b5 = src.B(S1, "B5", rep=FX, drop=NOATOM)
a_atom = limit(src(A1, "g_atom", rep=FX, drop=NOATOM), 7)
a_form = limit(src(A1, "g_form", rep=FX, drop=NOATOM), 8)
a_part = src(A1, "g_part", rep=FX, drop=NOATOM)
a_b1 = src.B(A1, "B1", rep=FX, drop=NOATOM)
a_b5 = src.B(A1, "B5", rep=FX, drop=NOATOM)

COL = {"A": "#e05a47", "B": "#4a7bd0", "C": "#f2c230"}


def atom(x, y, k):
    return "<circle cx='%d' cy='%d' r='9' fill='%s' stroke='#333'/>" % (x, y, COL[k])


def particle(kind):
    """kind: element-atoms, element-molecules, compound, mixture"""
    out = []
    spots = [(25, 25), (70, 22), (115, 28), (28, 70), (75, 72), (118, 68), (40, 112), (95, 115)]
    for i, (x, y) in enumerate(spots[:6] if kind != "mixture" else spots):
        if kind == "element-atoms":
            out.append(atom(x, y, "A"))
        elif kind == "element-molecules":
            out.append(atom(x - 8, y, "B") + atom(x + 8, y, "B"))
        elif kind == "compound":
            out.append(atom(x - 8, y, "A") + atom(x + 8, y, "B"))
        else:
            out.append(atom(x, y, "C") if i % 2 else atom(x - 8, y, "B") + atom(x + 8, y, "B"))
    return "".join(out)


DESC = {"element-atoms": "an element made of single atoms", "element-molecules": "an element made of molecules",
        "compound": "a compound", "mixture": "a mixture"}


def g_diag():
    order = R.sample(list(DESC), 4)
    svg = "<svg viewBox='0 0 600 170' width='600' role='img' aria-label='four particle diagrams A to D'>%s</svg>" % "".join(
        "<g transform='translate(%d,0)'><rect x='2' y='2' width='140' height='135' fill='#fff' stroke='#333' stroke-width='2'/>%s"
        "<text x='72' y='160' text-anchor='middle' font-size='16' font-weight='bold'>%s</text></g>" % (6 + i * 150, particle(k), "ABCD"[i])
        for i, k in enumerate(order))
    i = R.randrange(4)
    if R.random() < 0.5:
        return tq("%s<br>What does diagram %s show?" % (svg, "ABCD"[i]), DESC[order[i]], [DESC[k] for k in order if k != order[i]],
                  "Same coloured atoms only: element. Different atoms joined: compound. Different particles not joined: mixture.")
    k = order[i]
    return tq("%s<br>Which diagram shows %s?" % (svg, DESC[k]), "diagram " + "ABCD"[i], ["diagram " + "ABCD"[j] for j in range(4) if j != i],
              "Look at whether the atoms are the same or different, and whether they are joined.")


POOL1 = pool(R, [
    ("Which list contains only elements?", "copper, oxygen and helium", ["water, salt and sugar", "air, sea water and soil", "copper, water and air"], "Each is on the periodic table."),
    ("Which list contains only compounds?", "water, carbon dioxide and table salt", ["oxygen, nitrogen and argon", "air, milk and soil", "iron, gold and water"], "Each has two or more elements joined."),
    ("Which list contains only mixtures?", "air, milk and soil", ["water, gold and salt", "oxygen, iron and carbon", "carbon dioxide, water and air"], "Mixtures are not chemically joined."),
    ("Why is air a mixture?", "Its gases (nitrogen, oxygen, argon, carbon dioxide) are not chemically joined.", ["Air is one element.", "Air is a compound of nitrogen and oxygen.", "Air has no particles."], "The amounts of gases in air can vary."),
    ("What is a mixture?", "two or more substances mixed together but not chemically joined", ["one type of atom", "elements joined in a fixed ratio", "a pure substance"], "Mixtures can be separated by physical methods."),
    ("Oxygen gas is O₂. Is it an element or a compound?", "an element, because both atoms are oxygen", ["a compound, because it has two atoms", "a mixture", "neither"], "A molecule of one element is still an element."),
    ("Which of these is a compound?", "carbon dioxide (CO₂)", ["oxygen (O₂)", "iron (Fe)", "air"], "CO₂ has carbon and oxygen joined."),
    ("Which of these is a mixture?", "sea water", ["pure water", "gold", "carbon dioxide"], "Sea water has salt and other substances dissolved in water."),
    ("How many atoms are in one molecule of glucose, C₆H₁₂O₆?", "24", ["3", "6", "18"], "6 + 12 + 6 = 24."),
    ("Why can salt be separated from sea water by evaporation?", "Salt and water are mixed, not chemically joined.", ["Salt is an element.", "Water is an element.", "Evaporation splits atoms."], "Physical methods separate mixtures."),
    ("Which property is typical of metals?", "they conduct electricity", ["they are brittle", "they are dull", "they are poor conductors of heat"], "Copper is used for wires."),
    ("Australia mines a lot of iron ore. What is iron's symbol?", "Fe", ["I", "Ir", "In"], "Fe comes from the Latin ferrum."),
])
POOL5 = pool(R, [
    ("Mia heats a sample of salt water from Lake Eyre until the water evaporates. What is left behind?", "salt crystals", ["nothing", "pure water", "sand only"], "The salt was dissolved in the water."),
    ("Jack adds iron filings to sulfur powder and stirs. How can he show it is a mixture?", "Pull the iron out with a magnet.", ["Heat it until it glows.", "Weigh it.", "Add more sulfur."], "The iron keeps its own properties."),
    ("Jack heats the iron and sulfur and they form iron sulfide. Can a magnet still pull the iron out?", "No, iron sulfide is a new compound with different properties.", ["Yes, the iron is unchanged.", "Yes, but only half of it.", "Only if it is cold."], "A compound has different properties from its elements."),
    ("Ruby tests five solids with a circuit. Which result shows a metal?", "the bulb lights", ["the bulb stays off", "the solid melts", "the solid shatters when tapped"], "Metals conduct electricity."),
    ("Kai says, 'Water is a mixture of hydrogen and oxygen.' Why is this wrong?", "Hydrogen and oxygen are chemically joined in water, so it is a compound.", ["Water is an element.", "Water has no hydrogen.", "Kai is right."], "A compound has a fixed ratio."),
    ("Noah boils pure water and finds it boils at exactly 100 °C. Salty water boils at a higher temperature. What does this show?", "Pure substances have a fixed boiling point; mixtures do not.", ["Salt water is an element.", "Pure water is a mixture.", "Salt makes water boil sooner."], "Fixed melting and boiling points show a pure substance."),
    ("Zara wants to know if a gold-coloured nugget from Kalgoorlie is pure gold. Which test helps most?", "measure its density and compare it with gold's", ["look at its colour", "smell it", "see if it is shiny"], "Many minerals look like gold; density is a better test."),
    ("Liam mixes 10 g of sand with 50 g of water. Then he mixes 30 g of sand with 50 g of water. What does this show about mixtures?", "The amounts in a mixture can vary.", ["Mixtures always have a fixed ratio.", "Sand becomes a compound.", "Sand dissolves in water."], "Compounds have a fixed ratio; mixtures do not."),
    ("Chloe passes an electric current through water and collects two gases. What does this show?", "Water is a compound that can be split into hydrogen and oxygen by a chemical change.", ["Water is an element.", "Water is a mixture of gases.", "Electricity makes atoms."], "Splitting a compound needs a chemical reaction."),
    ("Ethan tests a shiny grey solid. It is brittle and does not conduct electricity. What is it most likely to be?", "a non-metal such as silicon or iodine", ["a metal such as copper", "a mixture of metals", "pure aluminium"], "Metals conduct electricity and bend."),
    ("Amelia filters muddy water from a dam. The water comes through clear but still tastes salty. Why?", "The salt is dissolved, so it passes through the filter paper.", ["Filters remove salt.", "The mud turned into salt.", "Salt is a solid that cannot dissolve."], "Filtering removes undissolved solids only."),
    ("Ella makes a model of methane (CH₄) with balls and sticks. How many balls does she need?", "5", ["4", "2", "1"], "1 carbon + 4 hydrogen."),
])


def main():
    sets = U.sets([
        ("Elements, compounds and mixtures", [(POOL1, 5), (u_class, 6), (u_b1, 3), (s_b1, 3), (a_b1, 3)]),
        ("Particle diagrams", [(g_diag, 10), (a_part, 2), (a_atom, 2), (a_form, 3), (POOL1, 3)]),
        ("Symbols and formulas", [(u_sym, 7), (u_name, 4), (u_count, 5), (a_form, 4)]),
        ("Metals, non-metals and mixtures", [(s_metal, 7), (s_sol, 6), (s_susp, 3), (POOL1, 2), (u_count, 2)]),
        ("Investigations", [(POOL5, 10), (u_b5, 4), (s_b5, 3), (a_b5, 3), (a_form, 2)]),
    ])
    make_au(YEAR, "elements-compounds-and-mixtures", SORT, "AC9S8U06", "Chemical sciences",
            "Use particle theory to explain the differences between elements, compounds and mixtures, and represent them with "
            "chemical symbols, formulas and models (summary of the Australian Curriculum v9.0 Science content description).",
            "Elements, Compounds and Mixtures", "Elements and compounds",
            "Free Year 8 science worksheets on elements, compounds and mixtures: atoms and molecules, particle diagrams, chemical "
            "symbols and formulas, metals and non-metals. 100 questions with answers.",
            "Elements, compounds or mixtures?", "Elements have one kind of atom; compounds have atoms joined; mixtures are not joined.",
            "<p><b>Everything is made of atoms.</b></p><ul>"
            "<li>Element: only one kind of atom (Fe, O₂). A molecule of one element is still an element.</li>"
            "<li>Compound: two or more different elements chemically joined in a fixed ratio (H₂O, CO₂).</li>"
            "<li>Mixture: substances mixed but not joined (air, sea water); they can be separated by physical methods.</li></ul>",
            [("Is O₂ an element or a compound?", ["both atoms are oxygen"], "an element"),
             ("How many atoms are in H₂SO₄?", ["2 + 1 + 4"], "7")],
            ["Calling O₂ a compound because it has two atoms.", "Thinking a mixture has a fixed ratio.",
             "Reading the small number as belonging to the next symbol (in H₂O the 2 belongs to H)."],
            [("What is the difference between an atom and a molecule?", "An atom is the smallest particle of an element. A molecule is two or more atoms joined together, such as O₂ or H₂O."),
             ("How can you tell a compound from a mixture?", "A compound has a fixed ratio and new properties, and needs a chemical reaction to separate it. A mixture can have any ratio and can be separated by physical methods."),
             ("What do the small numbers in a formula mean?", "They show how many atoms of the element just before them are in one molecule. In CO₂ there is 1 carbon and 2 oxygen atoms.")],
            sets)


if __name__ == "__main__":
    main()
