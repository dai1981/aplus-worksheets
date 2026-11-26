# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Atoms and Molecules (MS-PS1-1)
  python tools/gen_us_science_g7_atoms_and_molecules.py
Develop models to describe the atomic composition of simple molecules and extended structures.
Atoms, elements, molecules, compounds; reading chemical formulas (H2O, CO2, O2, NH3, CH4, C6H12O6);
counting atoms; extended structures (NaCl crystal, diamond, metals) vs. molecules.
Assessment boundary: no valence electrons or bonding energy; no ionic/covalent naming rules.
Wrong answers come from real mistakes: "H2O has 2 oxygen atoms", "a subscript applies to the whole formula",
"O2 is a compound", "a coefficient and a subscript mean the same thing".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, circle, line, text, People, INK

U = Unit(70101)
R = U.R
P = People(R)

NAMES = {"H": "hydrogen", "O": "oxygen", "C": "carbon", "N": "nitrogen", "Na": "sodium", "Cl": "chlorine", "S": "sulfur", "Ca": "calcium", "Fe": "iron"}
MOL = [("water", [("H", 2), ("O", 1)]), ("carbon dioxide", [("C", 1), ("O", 2)]), ("oxygen gas", [("O", 2)]), ("ammonia", [("N", 1), ("H", 3)]),
       ("methane", [("C", 1), ("H", 4)]), ("glucose (sugar)", [("C", 6), ("H", 12), ("O", 6)]), ("hydrogen peroxide", [("H", 2), ("O", 2)]),
       ("ozone", [("O", 3)]), ("sulfuric acid", [("H", 2), ("S", 1), ("O", 4)]), ("propane", [("C", 3), ("H", 8)]),
       ("ethanol", [("C", 2), ("H", 6), ("O", 1)]), ("nitrogen gas", [("N", 2)]), ("calcium carbonate (chalk)", [("Ca", 1), ("C", 1), ("O", 3)])]


def formula(parts):
    return "".join(el + ("<sub>%d</sub>" % n if n > 1 else "") for el, n in parts)


def g_count():
    name, parts = R.choice(MOL)
    k = R.choice(["total", "one"])
    who = P.next()[0]
    if k == "total" or len(parts) == 1:
        t = sum(n for _, n in parts)
        w = [t + 1, t - 1, len(parts)] if len(parts) != t - 1 and t - 1 > 0 else [t + 1, t + 2, len(parts) + 5]
        w = [x for x in dict.fromkeys(w) if x != t and x > 0]
        if len(w) < 3:
            w.append(t * 2)
        return item("%s looks up %s, %s. How many atoms are in one molecule?" % (who, name, formula(parts)), "%d" % t, ["%d" % x for x in w[:3]],
                    " + ".join("%d %s" % (n, NAMES[el]) for el, n in parts) + " = %d atoms." % t)
    el, n = R.choice(parts)
    w = sorted({n + 1, max(1, n - 1), sum(m for _, m in parts), 1, 2} - {n})
    return item("How many %s atoms are in one molecule of %s, %s?" % (NAMES[el], name, formula(parts)), "%d" % n, ["%d" % x for x in R.sample(w, 3)],
                "The subscript after %s is %s." % (el, n if n > 1 else "not written, which means 1"))


def g_coef():
    name, parts = R.choice([m for m in MOL if len(m[1]) > 1])
    c = R.choice([2, 3, 4])
    el, n = R.choice(parts)
    who = P.next()[0]
    return item("%s writes %d%s. How many %s atoms are there in all?" % (who, c, formula(parts), NAMES[el]), "%d" % (c * n),
                ["%d" % x for x in sorted({n, c + n, c * n + c, c * sum(m for _, m in parts)} - {c * n})][:3], "The coefficient %d multiplies everything: %d × %d = %d." % (c, c, n, c * n))


ELEM = ["O<sub>2</sub> (oxygen gas)", "N<sub>2</sub> (nitrogen gas)", "Fe (iron)", "He (helium)", "O<sub>3</sub> (ozone)", "C (diamond)", "Cu (copper)", "H<sub>2</sub> (hydrogen gas)"]
COMP = ["H<sub>2</sub>O (water)", "CO<sub>2</sub> (carbon dioxide)", "NaCl (table salt)", "CH<sub>4</sub> (methane)", "NH<sub>3</sub> (ammonia)", "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> (glucose)",
        "CaCO<sub>3</sub> (chalk)", "H<sub>2</sub>O<sub>2</sub> (hydrogen peroxide)"]


def g_type():
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s sorts substances. Which one is an element (made of only one kind of atom)?" % who, R.choice(ELEM), R.sample(COMP, 3),
                    "An element contains only one kind of atom, even if the atoms are joined in pairs.")
    return item("%s sorts substances. Which one is a compound (two or more kinds of atoms bonded together)?" % who, R.choice(COMP), R.sample(ELEM, 3),
                "A compound contains two or more different elements chemically joined.")


COL = {"H": "#ffffff", "O": "#e04b3c", "C": "#444444", "N": "#3b6fd1"}


def mol_svg(parts, label):
    """Draw a simple ball model: central atom with others around it."""
    atoms = [el for el, n in parts for _ in range(n)]
    center = max(parts, key=lambda p: (p[0] != "H", -p[1]))[0] if len(parts) > 1 else atoms[0]
    others = list(atoms)
    others.remove(center)
    import math
    cx, cy = 100, 80
    s = []
    for i, el in enumerate(others):
        a = 2 * math.pi * i / max(1, len(others)) - math.pi / 2
        x, y = cx + 58 * math.cos(a), cy + 58 * math.sin(a)
        s.append(line(cx, cy, x, y, INK, 3) + circle(x, y, 15 if el == "H" else 19, COL.get(el, "#aaa"), INK, 1.5) + text(x, y + 5, el, 13, col="#fff" if el != "H" else INK))
    s.append(circle(cx, cy, 21, COL.get(center, "#aaa"), INK, 1.5) + text(cx, cy + 5, center, 14, col="#fff" if center != "H" else INK))
    return svg_wrap(200, 160, "".join(s), label)


def g_model():
    choices = [m for m in MOL if all(el in COL for el, _ in m[1]) and sum(n for _, n in m[1]) <= 5 and m[0] != "hydrogen peroxide"]
    name, parts = R.choice(choices)
    who = P.next()[0]
    others = [formula(p) for n_, p in choices if formula(p) != formula(parts)]
    return item(fig(mol_svg(parts, "a ball-and-stick model of a molecule")) + "%s built this model. Each ball is an atom (H = hydrogen, O = oxygen, C = carbon, N = nitrogen). Which formula matches it?" % who,
                formula(parts), R.sample(others, 3), "Count each kind of atom: %s." % ", ".join("%d %s" % (n, NAMES[el]) for el, n in parts))


B1 = bank([
    ("What is an atom?", "the smallest unit of an element that keeps its properties", ["a group of molecules", "a kind of cell", "a mixture of elements"], "Everything is made of atoms."),
    ("What is a molecule?", "two or more atoms joined together", ["a single atom", "a kind of element", "a cell part"], "O₂ and H₂O are molecules."),
    ("In H₂O, what does the small 2 mean?", "There are 2 hydrogen atoms.", ["There are 2 oxygen atoms.", "There are 2 molecules.", "Multiply the whole formula by 2."],
     "A subscript tells how many atoms of the element just before it."),
    ("How is a compound different from an element?", "A compound has two or more kinds of atoms bonded together; an element has only one kind.", ["They are the same.", "An element always has more atoms.", "A compound has only one kind of atom."],
     "Water is a compound; oxygen gas is an element."),
    ("What is an extended structure?", "a large repeating pattern of atoms, like a salt crystal or a diamond", ["a single small molecule", "a gas", "one atom"],
     "NaCl forms a cube-shaped repeating pattern."),
    ("Why do water and hydrogen peroxide have different properties even though both have H and O?", "They have different numbers and arrangements of atoms.", ["They are the same substance.", "One has no hydrogen.", "Properties do not depend on atoms."],
     "H₂O and H₂O₂ are different molecules."),
    ("About how many kinds of elements are known?", "about 118", ["about 10", "millions", "exactly 4"], "They are arranged in the periodic table."),
    ("What does the number 3 mean in 3CO₂?", "There are 3 molecules of carbon dioxide.", ["There are 3 oxygen atoms in each molecule.", "There are 3 carbon atoms in one molecule.", "Nothing; it is decoration."],
     "A coefficient in front counts molecules."),
])
B5 = bank([
    ("Ava builds a model of methane with one black ball and four white balls. What do the balls represent?", "one carbon atom and four hydrogen atoms", ["four carbon atoms and one hydrogen atom", "five molecules", "five elements"],
     "CH₄ has 1 C and 4 H."),
    ("Leo's model of CO₂ has one black ball and one red ball. What is wrong?", "It needs two red balls for two oxygen atoms.", ["It needs two black balls.", "It is correct.", "CO₂ has no carbon."],
     "CO₂ has 1 carbon and 2 oxygen atoms."),
    ("Mia looks at salt grains with a magnifier. They are tiny cubes. What does the cube shape suggest?", "The atoms are arranged in a repeating pattern.", ["Salt is made of one atom.", "Salt is a gas.", "Salt has no atoms."],
     "The repeating pattern shows up in the crystal shape."),
    ("Why do scientists use models of atoms and molecules?", "Atoms are far too small to see, so models help explain their arrangement.", ["Models are bigger than atoms, so they are wrong.", "Atoms do not exist.", "Models change the atoms."],
     "Models make the invisible understandable."),
    ("Noah compares O₂ and O₃. What is the difference?", "O₂ has 2 oxygen atoms per molecule; O₃ (ozone) has 3.", ["They are the same.", "O₃ has 3 different elements.", "O₂ is a compound."],
     "Both are forms of the element oxygen."),
])


def body():
    think = ("<p>All matter is made of <b>atoms</b>. An <b>element</b> has only one kind of atom. Atoms join to form <b>molecules</b>; a <b>compound</b> has two or more kinds of atoms.</p>"
             "<p>A <b>chemical formula</b> shows the atoms: in H<sub>2</sub>O, the subscript 2 means 2 hydrogen atoms, and O with no number means 1 oxygen atom. "
             "A <b>coefficient</b> in front counts molecules: 3H<sub>2</sub>O has 6 H and 3 O.</p>"
             + figure(mol_svg([("C", 1), ("H", 4)], "a model of methane"), "Methane, CH₄: 1 carbon atom and 4 hydrogen atoms.")
             + "<p>Some substances, like salt (NaCl) and diamond, form <b>extended structures</b>: huge repeating patterns of atoms instead of small molecules.</p>")
    ex = [("How many atoms are in C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>?", ["6 + 12 + 6"], "24"),
          ("How many oxygen atoms are in 2CO<sub>2</sub>?", ["Each CO₂ has 2 O.", "2 × 2"], "4")]
    mist = ["Reading H₂O as 2 oxygen atoms. The 2 belongs to H.",
            "Thinking a subscript multiplies the whole formula. Only a coefficient does that.",
            "Thinking O₂ is a compound. It has only one kind of atom, so it is an element."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Atoms, elements and compounds", B1 + [(g_type, 6), (g_count, 6)]),
        ("Reading chemical formulas", [(g_count, 14), (g_type, 6)]),
        ("Coefficients and subscripts", [(g_coef, 14), (g_count, 6)]),
        ("Molecule models", [(g_model, 12), (g_type, 4), (g_coef, 4)]),
        ("Modeling matter", B5 + [g_model, g_count, g_coef, g_type]),
    ])
    make("grade-7", "atoms-and-molecules", 1, "MS-PS1-1",
         "Develop models to describe the atomic composition of simple molecules and extended structures.",
         "Atoms and Molecules",
         "Grade 7 Atoms and Molecules Worksheets: Elements, Compounds and Chemical Formulas",
         "Atoms and Molecules",
         "Free middle school science worksheets on atoms and molecules (NGSS MS-PS1-1): elements and compounds, reading chemical formulas, subscripts and coefficients, molecule models and extended structures. 100 practice questions with answers.",
         "Molecules are atoms joined together.",
         "A formula like H₂O shows the atoms in a molecule. Subscripts count atoms; coefficients count molecules.",
         body(),
         [("What does H₂O mean?", "One molecule of water has 2 hydrogen atoms and 1 oxygen atom."),
          ("What is the difference between an element and a compound?", "An element has only one kind of atom. A compound has two or more kinds of atoms bonded together."),
          ("What is the difference between a subscript and a coefficient?", "A subscript (small number after an element) counts atoms of that element. A coefficient (number in front) counts whole molecules.")],
         sets)


if __name__ == "__main__":
    main()
