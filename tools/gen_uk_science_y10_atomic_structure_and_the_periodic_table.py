# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Chemistry): Atomic Structure and the Periodic Table
  python tools/gen_uk_science_y10_atomic_structure_and_the_periodic_table.py
Protons, neutrons and electrons, atomic and mass numbers, isotopes and relative atomic mass, ions, electronic
structure (2, 8, 8), the development of the model of the atom (plum pudding, Rutherford, Bohr, Chadwick), the periodic
table (Mendeleev, groups 1, 7 and 0) and metals and non-metals. Reuses the US Chemistry atomic-structure and
periodic-table questions in British English and the group questions of the Year 8 unit (UK group numbers 1–7 and 0).
Wrong answers come from real mistakes: "mass number = number of protons", "isotopes have different numbers of protons",
"the nucleus is most of the atom's volume", "reactivity increases down group 7".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62005)
AS = "chem_atomic_structure_and_isotopes"
PT = "chem_periodic_table_and_trends"
us_pne, us_find, us_iso, us_avg, us_ion, us_shell = [us(AS, "g_" + n) for n in ("pne", "find", "iso", "avg", "ion", "shell")]
us_class, us_fam, us_react = us(PT, "g_class"), us(PT, "g_fam"), us(PT, "g_react")
y8_group, y8_g1, y8_g7 = [us.uk("gen_uk_science_y8_periodic_table", n) for n in ("g_group", "g_g1", "g_g7")]

HIST = [("J. J. Thomson", "discovered the electron and proposed the plum pudding model"), ("Ernest Rutherford", "showed with the alpha scattering experiment that the atom has a small, dense, positive nucleus"),
        ("Niels Bohr", "suggested electrons orbit the nucleus at fixed distances (shells)"), ("James Chadwick", "discovered the neutron"),
        ("John Dalton", "described atoms as tiny solid spheres that cannot be divided"), ("Dmitri Mendeleev", "arranged the elements by atomic mass and left gaps for undiscovered elements")]


def g_hist():
    p, j = R.choice(HIST)
    k = R.random() < 0.5
    if not once(("hi", p, k)):
        return None
    if k:
        return item("Which scientist %s?" % j, p, R.sample([x[0] for x in HIST if x[0] != p], 3), "The model of the atom changed as new evidence was found.")
    return item("What did %s contribute?" % p, "He " + j + ".", ["He " + x[1] + "." for x in R.sample([x for x in HIST if x[0] != p], 3)], "Models change with evidence.")


B1 = bank([
    ("What are the relative charges of a proton, a neutron and an electron?", "+1, 0 and −1", ["−1, 0 and +1", "+1, +1 and −1", "0, +1 and −1"], "Atoms are neutral overall."),
    ("Why does an atom have no overall charge?", "It has equal numbers of protons and electrons.", ["It has no protons.", "Neutrons cancel the charge.", "Electrons have no charge."], "Balanced charges."),
    ("What is an isotope?", "an atom of the same element with a different number of neutrons", ["an atom with a different number of protons", "a charged atom", "a compound of two elements"], "Same atomic number, different mass number."),
    ("Roughly how big is an atom?", "about 0.1 nm (1 × 10⁻¹⁰ m)", ["about 1 mm", "about 1 cm", "about 1 µm"], "The nucleus is about 1/10,000 of that."),
    ("Where is most of the mass of an atom?", "in the nucleus", ["in the electron shells", "spread evenly", "in the empty space"], "Protons and neutrons."),
])
B5 = bank([
    ("Why did the alpha scattering experiment replace the plum pudding model?", "Some alpha particles bounced back, showing a tiny dense positive nucleus.", ["All particles passed straight through.", "Electrons were discovered.", "Atoms were found to be solid spheres."], "Evidence changes models."),
    ("Why are elements in the same group similar?", "They have the same number of electrons in their outer shell.", ["They have the same mass.", "They have the same number of neutrons.", "They were found at the same time."], "Outer electrons decide reactions."),
    ("Why do the noble gases not react?", "Their outer shells are full.", ["They are too heavy.", "They are metals.", "They have no electrons."], "Stable arrangement."),
    ("How did Mendeleev's gaps help confirm his table?", "Elements were later discovered that fitted the gaps and matched his predictions.", ["The gaps were mistakes.", "No elements were ever found.", "He moved the gaps each year."], "Germanium fitted a gap."),
])

if __name__ == "__main__":
  build(U, 10, "atomic-structure-and-the-periodic-table", 5, "Chemistry", "Atomic structure and the Periodic Table",
      "A simple model of the atom: protons, neutrons and electrons; the size and mass of atoms; atomic number, mass number and isotopes; relative atomic mass; the development of the model of the atom; electronic structure; the periodic table, its development (Mendeleev) and groups 0, 1 and 7; metals and non-metals.",
      "Atomic Structure and the Periodic Table", "Atomic Structure and Periodic Table",
      "Free Year 10 GCSE Combined Science worksheets on atomic structure: protons, neutrons and electrons, isotopes, relative atomic mass, electron shells, the history of the atom and the periodic table. 100 questions with answers.",
      "Mass number = protons + neutrons.",
      "Isotopes have the same protons but different neutrons; electrons fill shells 2, 8, 8.",
      "<p><b>An atom has a tiny nucleus of protons and neutrons, with electrons in shells.</b></p><ul><li>Atomic number = protons. Mass number = protons + neutrons. Neutrons = mass number − atomic number.</li>"
      "<li>Isotopes have different numbers of neutrons. Electrons fill shells 2, 8, 8.</li>"
      "<li>Groups share the same number of outer electrons, so they react in similar ways.</li></ul>",
      [("Sodium: atomic number 11, mass number 23. Neutrons?", ["23 − 11"], "12"), ("Electron structure of chlorine (17)?", ["2 + 8 + 7"], "2, 8, 7")],
      ["Thinking mass number is the number of protons.", "Thinking isotopes have different numbers of protons.", "Thinking reactivity increases down group 7."],
      [("How do you work out the numbers of protons, neutrons and electrons?", "Protons = atomic number. In a neutral atom electrons = protons. Neutrons = mass number − atomic number."),
       ("What are isotopes?", "Atoms of the same element (same number of protons) with different numbers of neutrons, so they have different mass numbers."),
       ("How has the model of the atom changed?", "Dalton's solid spheres, Thomson's plum pudding, Rutherford's nuclear model, Bohr's shells and Chadwick's neutron each followed new evidence.")],
      [("Inside the atom", B1 + [(us_pne, 9), (us_find, 6)]),
       ("Isotopes and ions", [(us_iso, 8), (us_avg, 6), (us_ion, 6)]),
       ("Electron shells", [(us_shell, 10), (y8_group, 6), (g_hist, 4)]),
       ("The model of the atom", [(g_hist, 6), (us_class, 6), (us_fam, 8)]),
       ("Groups 1, 7 and 0", B5 + [(y8_g1, 5), (y8_g7, 5), (us_react, 3), (y8_group, 3)])])
