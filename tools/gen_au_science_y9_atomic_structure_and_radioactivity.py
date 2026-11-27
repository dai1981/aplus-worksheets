# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U06: how the model of the atom changed with the discovery of electrons, protons
and neutrons; atomic number, mass number and isotopes; and radioactive decay (alpha, beta, gamma, half-life).
  python tools/gen_au_science_y9_atomic_structure_and_radioactivity.py
Reuses the US Chemistry atomic structure and nuclear chemistry makers and the UK Year 10 atomic structure and radioactivity makers
with Australian names, plus own questions on the history of atomic models and Australian uses of radioisotopes (ANSTO, Lucas Heights).
Wrong answers come from real mistakes: thinking the mass number is the number of neutrons, thinking isotopes are different elements,
and thinking that after two half-lives nothing is left.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

AT = "gen_us_science_chem_atomic_structure_and_isotopes"
NU = "gen_us_science_chem_nuclear_chemistry"
K10 = "gen_uk_science_y10_atomic_structure_and_radioactivity"
NUM = [(r"\bproton number\b", "atomic number"), (r"\bnucleon number\b", "mass number"), (r"\bProton number\b", "Atomic number"), (r"\bNucleon number\b", "Mass number")]
NO = ["fission", "fusion", "MeV", "amu", "weighted", "positron"]
a_pne = limit(src(AT, "g_pne", rep=NUM, drop=NO), 12)
a_iso = limit(src(AT, "g_iso", rep=NUM, drop=NO), 6)
a_find = limit(src(AT, "g_find", rep=NUM, drop=NO), 5)
a_shell = limit(src(AT, "g_shell", rep=NUM, drop=NO), 5)
a_b1 = src.B(AT, "B1", rep=NUM, drop=NO)
a_b5 = src.B(AT, "B5", rep=NUM, drop=NO)
n_change = limit(src(NU, "g_change", rep=NUM, drop=NO), 6)
n_half = limit(src(NU, "g_half", rep=NUM, drop=NO), 9)
n_decay = limit(src(NU, "g_decay", rep=NUM, drop=NO), 5)
n_pen = src(NU, "g_pen", rep=NUM, drop=NO)
n_b1 = src.B(NU, "B1", rep=NUM, drop=NO)
n_b5 = src.B(NU, "B5", rep=NUM, drop=NO)
k_eq = limit(src(K10, "g_eq", rep=NUM, drop=NO), 4)
k_hl = limit(src(K10, "g_hl", rep=NUM, drop=NO), 8)
k_rad = src(K10, "g_rad", rep=NUM, drop=NO)
k_b1 = src.B(K10, "B1", rep=NUM, drop=NO)

POOL1 = pool(R, [
    ("Which scientist discovered the electron in 1897 and proposed the 'plum pudding' model?", "J. J. Thomson", ["Ernest Rutherford", "James Chadwick", "John Dalton"], "Electrons were dotted through a positive sphere."),
    ("In Rutherford's gold foil experiment, most alpha particles went straight through. What did this show?", "Most of the atom is empty space.", ["The atom is solid.", "Electrons are in the nucleus.", "Gold has no atoms."], "A few bounced back, showing a small, dense nucleus."),
    ("Why did a few alpha particles bounce back from the gold foil?", "They hit a tiny, dense, positive nucleus.", ["They hit electrons.", "The foil was too thick.", "Alpha particles are negative."], "This led to the nuclear model of the atom."),
    ("Who discovered the neutron in 1932?", "James Chadwick", ["J. J. Thomson", "Niels Bohr", "Marie Curie"], "Neutrons explained the extra mass in the nucleus."),
    ("What did Niels Bohr add to the model of the atom?", "Electrons orbit the nucleus in fixed energy levels (shells).", ["Atoms are solid balls.", "Atoms have no nucleus.", "Neutrons are outside the nucleus."], "Bohr's model explained the light given off by atoms."),
    ("Why did the model of the atom change over time?", "New experiments gave evidence that the old model could not explain.", ["Scientists guessed differently each year.", "Atoms changed.", "Old scientists were wrong on purpose."], "Science models improve with evidence."),
    ("What does the atomic number tell you?", "the number of protons in the nucleus", ["the number of neutrons", "the number of protons plus neutrons", "the mass of the atom in grams"], "It identifies the element."),
    ("What does the mass number tell you?", "the number of protons plus neutrons", ["the number of neutrons only", "the number of electrons", "the number of shells"], "Neutrons = mass number − atomic number."),
    ("What are isotopes?", "atoms of the same element with different numbers of neutrons", ["atoms of different elements", "atoms with different numbers of protons", "charged atoms"], "Carbon-12 and carbon-14 are isotopes."),
    ("ANSTO's reactor at Lucas Heights, Sydney, makes radioisotopes such as technetium-99m. What are they mainly used for?", "medical imaging and treating disease", ["making electricity for Sydney", "making nuclear weapons", "heating homes"], "Millions of patients use nuclear medicine."),
    ("Which type of radiation is stopped by a sheet of paper?", "alpha", ["beta", "gamma", "none of them"], "Alpha particles are large and heavily charged."),
    ("What is a half-life?", "the time for half of the radioactive atoms in a sample to decay", ["half the time the atom exists", "the time for all atoms to decay", "the age of the sample"], "After each half-life, half of what is left decays."),
])
POOL5 = pool(R, [
    ("A sample has 800 radioactive atoms and a half-life of 6 hours. How many are left after 18 hours?", "100", ["0", "200", "400"], "18 h = 3 half-lives: 800 → 400 → 200 → 100."),
    ("Mia measures the count rate of a source: 400, 200, 100 counts per minute every 10 minutes. What is the half-life?", "10 minutes", ["20 minutes", "5 minutes", "30 minutes"], "The count halves every 10 minutes."),
    ("Why do scientists measure the background radiation before an experiment?", "to subtract it from the readings so only the source is measured", ["to make the source stronger", "because background radiation is zero", "to change the half-life"], "Background radiation comes from rocks, space and food."),
    ("Jack places paper, aluminium and lead between a source and a detector. The count drops only with lead. Which radiation is it?", "gamma", ["alpha", "beta", "neutron"], "Gamma passes through paper and aluminium."),
    ("Why is a radioisotope with a short half-life used for medical scans?", "It decays quickly, so the patient is exposed for only a short time.", ["It lasts for years in the body.", "It is not radioactive.", "Short half-lives are stronger forever."], "Technetium-99m has a half-life of about 6 hours."),
    ("Ruby models an atom with a pea in the middle of a football field. What does the pea stand for?", "the nucleus, which is tiny compared with the atom", ["an electron", "the whole atom", "a neutron outside the atom"], "The atom is mostly empty space."),
    ("Kai tests 100 dice: each throw, dice showing 6 are 'decayed' and removed. What does this model?", "random radioactive decay and half-life", ["chemical bonding", "electron shells", "the plum pudding model"], "Each atom has a fixed chance of decaying."),
    ("Carbon-14 has a half-life of about 5700 years. A bone has 1/4 of its original carbon-14. About how old is it?", "about 11 400 years", ["about 5700 years", "about 1425 years", "about 22 800 years"], "1/4 means two half-lives."),
])


def main():
    sets = U.sets([
        ("Models of the atom", [(POOL1, 8), (a_b1, 6), (a_shell, 3), (k_b1, 3)]),
        ("Protons, neutrons and electrons", [(a_pne, 8), (a_find, 5), (POOL1, 3), (a_shell, 2), (a_iso, 2)]),
        ("Isotopes and radioactive decay", [(a_iso, 4), (n_change, 5), (k_eq, 4), (n_decay, 4), (POOL1, 1), (k_rad, 2)]),
        ("Types of radiation and half-life", [(n_pen, 5), (k_rad, 3), (n_half, 5), (k_hl, 4), (n_b1, 3)]),
        ("Investigations", [(POOL5, 8), (n_b5, 4), (a_b5, 4), (n_half, 1), (k_hl, 1), (a_pne, 2)]),
    ])
    make_au(YEAR, "atomic-structure-and-radioactivity", SORT, "AC9S9U06", "Chemical sciences",
            "Explain how the model of the atom changed following the discovery of electrons, protons and neutrons and describe "
            "how natural radioactive decay results in stable atoms (summary of the Australian Curriculum v9.0 Science content description).",
            "Atomic Structure and Radioactivity", "Atoms and radioactivity",
            "Free Year 9 science worksheets on atomic structure and radioactivity: models of the atom, protons, neutrons and electrons, "
            "atomic and mass numbers, isotopes, alpha, beta and gamma radiation and half-life. 100 questions with answers.",
            "Protons decide the element.", "Atomic number = protons; mass number = protons + neutrons. Unstable nuclei decay to become stable.",
            "<p><b>An atom has a tiny nucleus of protons and neutrons, with electrons around it.</b></p><ul>"
            "<li>The model changed with evidence: Dalton (solid atom) → Thomson (electrons) → Rutherford (nucleus) → Bohr (shells) → Chadwick (neutrons).</li>"
            "<li>Atomic number = protons. Mass number = protons + neutrons. Isotopes have the same protons but different neutrons.</li>"
            "<li>Unstable nuclei give off alpha, beta or gamma radiation. A half-life is the time for half the nuclei to decay.</li></ul>",
            [("Sodium: atomic number 11, mass number 23. Neutrons?", ["23 − 11"], "12"),
             ("800 atoms, 2 half-lives. Left?", ["800 → 400 → 200"], "200")],
            ["Thinking the mass number is the number of neutrons.", "Thinking isotopes are different elements.",
             "Thinking all of a sample has decayed after two half-lives."],
            [("Why did Rutherford's experiment change the model of the atom?", "Most alpha particles passed through gold foil but a few bounced back, so the atom must be mostly empty space with a tiny, dense, positive nucleus."),
             ("What is the difference between alpha, beta and gamma radiation?", "Alpha particles are helium nuclei stopped by paper; beta particles are fast electrons stopped by thin aluminium; gamma rays are waves reduced by thick lead or concrete."),
             ("How is radioactivity used in Australia?", "ANSTO at Lucas Heights makes radioisotopes for medical scans and cancer treatment, and radioactive dating helps scientists find the age of rocks and fossils.")],
            sets)


if __name__ == "__main__":
    main()
