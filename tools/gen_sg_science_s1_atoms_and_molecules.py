# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Models): Model of Matter - Atoms and Molecules
  python tools/gen_sg_science_s1_atoms_and_molecules.py
An atom is electrically neutral: a positively charged nucleus (protons and neutrons) with negatively charged electrons moving
around it; most of the mass is in the nucleus; each element has its own number of protons (proton number); a molecule is two
or more atoms chemically combined; reading the numbers and types of atoms in a formula; atoms are tiny; models of the atom
change with new evidence.
Wrong answers come from real mistakes: "neutrons are negative", "electrons are in the nucleus", "an atom has more electrons
than protons", "CO2 has 2 types of atoms and 2 atoms".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64108)
R = U.R
P = People(R)
EL = luse(U, "gen_uk_science_y7_elements_atoms_and_compounds", drop=[r"formula unit", r"NaOH", r"sodium chloride", r"salt"])

ATOMS = [("hydrogen", "H", 1, 1), ("helium", "He", 2, 4), ("lithium", "Li", 3, 7), ("carbon", "C", 6, 12), ("nitrogen", "N", 7, 14), ("oxygen", "O", 8, 16),
         ("fluorine", "F", 9, 19), ("neon", "Ne", 10, 20), ("sodium", "Na", 11, 23), ("magnesium", "Mg", 12, 24), ("aluminium", "Al", 13, 27), ("silicon", "Si", 14, 28),
         ("sulfur", "S", 16, 32), ("chlorine", "Cl", 17, 35), ("argon", "Ar", 18, 40), ("potassium", "K", 19, 39), ("calcium", "Ca", 20, 40)]


def g_atom():
    nm, sy, z, a = R.choice(ATOMS)
    k = R.choice(["p", "e", "n", "which"])
    if not once(("at", sy, k)) or not once(("atk", k), 8):
        return None
    d = "An atom of %s (%s) has a proton number of %d and a nucleon number of %d." % (nm, sy, z, a)
    if k == "p":
        return item(d + " How many protons does it have?", str(z), [str(a), str(a - z), str(a + z)], "The proton number is the number of protons.")
    if k == "e":
        return item(d + " How many electrons does it have?", str(z), [str(a), str(a - z), str(z + 1)] if a - z != z else [str(a), str(z + 1), str(z - 1) if z > 1 else "0"],
                    "An atom is neutral, so it has the same number of electrons as protons.")
    if k == "n":
        w = [str(a), str(z), str(a + z)]
        if str(a - z) in w:
            w = [str(a), str(a + z), str(a - z + 2)]
        return item(d + " How many neutrons does it have?", str(a - z), w, "Neutrons = nucleon number − proton number = %d − %d = %d." % (a, z, a - z))
    others = R.sample([x for x in ATOMS if x[2] != z], 3)
    return item("An atom has %d protons. Which element is it?" % z, nm, [x[0] for x in others], "Every atom of %s has %d protons; the proton number identifies the element." % (nm, z))


PART = [("proton", "positive (+)", "in the nucleus"), ("neutron", "no charge (neutral)", "in the nucleus"), ("electron", "negative (−)", "moving around the nucleus")]


def g_part():
    p, c, w = R.choice(PART)
    k = R.choice(["c", "w", "which"])
    if not once(("pt", p, k)):
        return None
    if k == "c":
        return item("What is the charge on %s %s?" % ("an" if p == "electron" else "a", p), c, [x for x in ["positive (+)", "negative (−)", "no charge (neutral)", "it changes all the time"] if x != c], "Protons are positive, electrons are negative, neutrons have no charge.")
    if k == "w":
        return item("Where is %s %s found in an atom?" % ("an" if p == "electron" else "a", p), w, [x for x in ["in the nucleus", "moving around the nucleus", "outside the atom", "only in molecules"] if x != w], "Protons and neutrons are in the nucleus; electrons move around it.")
    return item("Which particle in an atom %s and is %s?" % ("has " + c if p != "neutron" else "has no charge", w), p, [x for x in ["proton", "neutron", "electron", "molecule"] if x != p],
                "Protons (+) and neutrons (0) are in the nucleus; electrons (−) move around it.")


FORM = [("water", "H<sub>2</sub>O", [("hydrogen", 2), ("oxygen", 1)], "compound"), ("carbon dioxide", "CO<sub>2</sub>", [("carbon", 1), ("oxygen", 2)], "compound"),
        ("oxygen gas", "O<sub>2</sub>", [("oxygen", 2)], "element"), ("ammonia", "NH<sub>3</sub>", [("nitrogen", 1), ("hydrogen", 3)], "compound"),
        ("methane", "CH<sub>4</sub>", [("carbon", 1), ("hydrogen", 4)], "compound"), ("glucose", "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>", [("carbon", 6), ("hydrogen", 12), ("oxygen", 6)], "compound"),
        ("nitrogen gas", "N<sub>2</sub>", [("nitrogen", 2)], "element"), ("ozone", "O<sub>3</sub>", [("oxygen", 3)], "element"),
        ("sulfuric acid", "H<sub>2</sub>SO<sub>4</sub>", [("hydrogen", 2), ("sulfur", 1), ("oxygen", 4)], "compound"), ("ethanol", "C<sub>2</sub>H<sub>5</sub>OH", [("carbon", 2), ("hydrogen", 6), ("oxygen", 1)], "compound"),
        ("hydrogen gas", "H<sub>2</sub>", [("hydrogen", 2)], "element"), ("sulfur dioxide", "SO<sub>2</sub>", [("sulfur", 1), ("oxygen", 2)], "compound"),
        ("hydrogen peroxide", "H<sub>2</sub>O<sub>2</sub>", [("hydrogen", 2), ("oxygen", 2)], "compound"), ("propane", "C<sub>3</sub>H<sub>8</sub>", [("carbon", 3), ("hydrogen", 8)], "compound")]


def g_form():
    nm, f, parts, t = R.choice(FORM)
    k = R.choice(["types", "total", "one", "kind"])
    if not once(("fm", nm, k)):
        return None
    tot = sum(x[1] for x in parts)
    if k == "types":
        n = len(parts)
        return item("The formula of %s is %s. How many different types of atoms are in one molecule?" % (nm, f), str(n), [str(tot), str(n + 1), str(n + 2) if n + 2 != tot else str(n + 3)],
                    "Count the different symbols: %s." % ", ".join(x[0] for x in parts))
    if k == "total":
        return item("The formula of %s is %s. How many atoms are in one molecule?" % (nm, f), str(tot), [str(len(parts)), str(tot + 1), str(tot - 1) if tot - 1 != len(parts) else str(tot + 2)],
                    "Add the numbers: %s = %d." % (" + ".join(str(x[1]) for x in parts), tot))
    if k == "one":
        e, c = R.choice(parts)
        w = sorted({str(c + 1), str(c + 2), str(tot), str(max(c - 1, 0) if c > 1 else 3)} - {str(c)})
        return item("The formula of %s is %s. How many %s atoms are in one molecule?" % (nm, f, e), str(c), R.sample(w, 3) if len(w) >= 3 else None,
                    "The small number after a symbol tells how many atoms of that element there are.") if len(w) >= 3 else None
    a = "a molecule of an element" if t == "element" else "a molecule of a compound"
    return item("Is %s (%s) a molecule of an element or of a compound?" % (nm, f), a,
                [x for x in ["a molecule of an element", "a molecule of a compound", "a single atom", "a mixture of atoms"] if x != a],
                "It contains only one type of atom." if t == "element" else "It contains atoms of more than one element chemically combined.")


B1 = bank([
    ("Why is an atom electrically neutral?", "It has equal numbers of protons and electrons.", ["It has no particles with charge.", "It has more neutrons than protons.", "Its electrons are in the nucleus."], "The positive and negative charges cancel."),
    ("Where is most of the mass of an atom?", "in the nucleus", ["in the electrons", "in the empty space", "spread evenly through the atom"], "Protons and neutrons are much heavier than electrons."),
    ("What makes atoms of one element different from atoms of another element?", "the number of protons", ["the number of neutrons only", "the colour of the atom", "the size of the electrons"], "Each element has a unique proton number."),
    ("What is a molecule?", "two or more atoms chemically combined", ["a single atom", "a mixture of elements", "a charged particle"], "Molecules can be of elements (O₂) or compounds (H₂O)."),
    ("About how big is an atom?", "about 0.0000000001 m across", ["about 1 mm across", "about the size of a grain of sand", "about 1 cm across"], "About ten million atoms side by side would span 1 mm."),
    ("What is the difference between an atom and a molecule?", "An atom is the smallest particle of an element; a molecule is two or more atoms joined together.", ["They are the same thing.", "A molecule is smaller than an atom.", "An atom contains molecules."], "O is an atom; O₂ is a molecule."),
    ("Rutherford found that most alpha particles passed straight through gold foil. What did this suggest?", "An atom is mostly empty space with a tiny, dense nucleus.", ["Atoms are solid balls.", "Gold has no atoms.", "Electrons are in the nucleus."], "This changed the model of the atom."),
    ("Why do scientists change models of the atom over time?", "New evidence from experiments shows that the old model needs improving.", ["Models are changed for fun.", "Atoms change their structure each year.", "Old models were never useful."], "Dalton, Thomson, Rutherford and Bohr each improved the model."),
])
B5 = bank([
    ("An atom has 11 protons and 12 neutrons. What is its nucleon number?", "23", ["11", "12", "1"], "Nucleon number = protons + neutrons = 11 + 12."),
    ("Atom X has 8 protons, 8 neutrons and 8 electrons. Atom Y has 8 protons, 9 neutrons and 8 electrons. What can you conclude?", "X and Y are atoms of the same element.", ["X and Y are different elements.", "Y is a molecule.", "X has no charge but Y does."], "They have the same proton number."),
    ("The formula of a compound is C<sub>2</sub>H<sub>6</sub>. Which statement is correct?", "One molecule has 2 carbon atoms and 6 hydrogen atoms.", ["It has 2 types of atoms and 2 atoms in all.", "It is a mixture of carbon and hydrogen.", "It has 26 atoms."], "8 atoms of 2 types."),
    ("Knowledge of the nucleus led to nuclear power and atomic bombs. Which is a fair statement?", "Scientific knowledge can be used for good or harm, so its uses must be considered carefully.", ["Science is always harmful.", "Science has no effect on society.", "Only bombs use atomic knowledge."], "Scientists and society share responsibility."),
    ("Which shows a molecule of a compound?", "CO", ["Cl<sub>2</sub>", "Ne", "O<sub>2</sub>"], "CO has carbon and oxygen combined."),
    ("A neutral atom has 17 electrons. How many protons does it have?", "17", ["18", "35", "34"], "In a neutral atom, protons = electrons."),
])


def body():
    think = ("<p><b>An atom has a tiny positive nucleus (protons and neutrons) with negative electrons moving around it.</b></p>"
             "<ul><li>Proton: +. Neutron: no charge. Electron: −. Atoms are neutral: <b>protons = electrons</b>.</li>"
             "<li><b>Proton number</b> = number of protons; it identifies the element. Neutrons = nucleon number − proton number.</li>"
             "<li>A <b>molecule</b> is two or more atoms chemically combined: O₂ (element), H₂O (compound).</li>"
             "<li>In a formula, the small number after a symbol is the number of those atoms: CO₂ has 1 C and 2 O.</li></ul>")
    ex = [("Sodium: proton number 11, nucleon number 23. Neutrons?", ["23 − 11"], "12"),
          ("How many atoms are in one molecule of NH₃?", ["1 N + 3 H"], "4")]
    mist = ["Saying neutrons are negative. They have no charge.", "Putting electrons in the nucleus. They move around it.",
            "Thinking the neutron number identifies the element. It is the proton number.", "Counting CO₂ as 2 atoms. It has 3: 1 carbon and 2 oxygen."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Inside an atom", B1[:3] + [(g_part, 9), (g_atom, 6), (B1[6], 1), (B1[7], 1)]),
        ("Protons, neutrons and electrons", [(g_atom, 14), (g_part, 4), (EL.g_sym, 2)]),
        ("Molecules", B1[3:6] + [(g_form, 8), (EL.g_count, 5), (EL.g_class, 4)]),
        ("Chemical formulae", [(g_form, 12), (EL.g_count, 4), (EL.g_sym, 4)]),
        ("Exam-style questions", B5 + [(g_atom, 6), (g_form, 5), (EL.g_count, 3)]),
    ])
    make_lss(1, "atoms-and-molecules", 8, "Models", "Model of Matter – Atoms and Molecules",
             "Describe an atom as electrically neutral, with a positively charged nucleus of protons and neutrons and negatively charged electrons moving around it; recognise that "
             "the mass of an atom is mainly in its nucleus and that atoms of an element have a unique number of protons; describe a molecule as two or more atoms chemically combined "
             "and state the numbers and types of atoms from a chemical formula (summary of the MOE Lower Secondary Science Syllabus).",
             "Atoms and Molecules", seo(1, "Atoms and Molecules"), "Atoms and molecules",
             "Free Secondary 1 science worksheets for Singapore students on atoms and molecules: protons, neutrons and electrons, proton and nucleon numbers, molecules and chemical formulae. With answers.",
             "Protons (+) and neutrons in the nucleus; electrons (−) around it.", "In an atom, protons = electrons.",
             body(),
             [("Why is an atom neutral?", "It has the same number of protons (positive) and electrons (negative)."),
              ("How do you find the number of neutrons?", "Subtract the proton number from the nucleon number."),
              ("What does CO₂ mean?", "One molecule has one carbon atom and two oxygen atoms chemically combined.")],
             sets)


if __name__ == "__main__":
    main()
