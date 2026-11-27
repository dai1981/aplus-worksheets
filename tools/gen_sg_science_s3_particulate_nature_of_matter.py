# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 2: The Particulate Nature of Matter
  python tools/gen_sg_science_s3_particulate_nature_of_matter.py
Solids, liquids and gases and changes of state in terms of the kinetic particle theory; diffusion and the effect of molecular
mass and temperature on its rate; atomic structure (protons, neutrons, electrons, their relative charges and masses), proton
and nucleon numbers and nuclide notation, isotopes, and electronic configuration of the first 20 elements.
US atomic-structure makers and SG diffusion makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "the nucleon number is the number of neutrons", "isotopes have different numbers of
protons", "heavier gas molecules diffuse faster", "the temperature keeps rising while a substance boils".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 14
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

NOAVG = lambda it: "relative atomic mass" not in it["q"] and "ionisation" not in it["q"] and "valence" not in it["q"].lower()
us_pne = keep(src("gen_us_science_chem_atomic_structure_and_isotopes", "g_pne"), NOAVG)
us_iso = keep(src("gen_us_science_chem_atomic_structure_and_isotopes", "g_iso"), NOAVG)
us_ion = keep(src("gen_us_science_chem_atomic_structure_and_isotopes", "g_ion"), NOAVG)
us_find = keep(src("gen_us_science_chem_atomic_structure_and_isotopes", "g_find"), NOAVG)
sg_dif = src("gen_sg_science_s1_particulate_nature_of_matter", "g_dif")

Z20 = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca"]
NAMES = ["hydrogen", "helium", "lithium", "beryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon", "sodium", "magnesium", "aluminium", "silicon",
         "phosphorus", "sulfur", "chlorine", "argon", "potassium", "calcium"]


def conf(z):
    out = []
    for cap in (2, 8, 8, 2):
        if z <= 0:
            break
        out.append(min(cap, z))
        z -= min(cap, z)
    return ", ".join(str(x) for x in out)


def g_conf():
    z = R.randint(3, 20)
    k = R.choice(["conf", "conf", "outer", "shells", "which"])
    c = conf(z)
    if k == "conf":
        wr = {conf(z - 1), conf(z + 1) if z < 20 else "2, 8, 9", ", ".join(c.split(", ")[::-1]) if len(c.split(", ")) > 1 else "1, %d" % (z - 1), "2, %d" % (z - 2) if z > 10 else "8, %d" % z}
        wr.discard(c)
        return tq("What is the electronic configuration of %s (proton number %d)?" % (NAMES[z - 1], z), c, sorted(wr)[:3],
                  "Fill the shells in order: 2 in the first, 8 in the second, 8 in the third. %s: %s." % (NAMES[z - 1].capitalize(), c))
    if k == "outer":
        o = int(c.split(", ")[-1])
        return nq("How many electrons are in the outer shell of a %s atom (proton number %d)?" % (NAMES[z - 1], z), o, [z, len(c.split(", ")), 8 - o if o != 4 else 2], "",
                  "Configuration %s, so %d outer electron%s." % (c, o, "" if o == 1 else "s"))
    if k == "shells":
        n = len(c.split(", "))
        return nq("How many occupied electron shells does a %s atom (proton number %d) have?" % (NAMES[z - 1], z), n, [n + 1, n - 1 if n > 1 else 4, int(c.split(", ")[-1])], "",
                  "Configuration %s: %d shells." % (c, n))
    return tq("Which element has the electronic configuration %s?" % c, NAMES[z - 1], [NAMES[i] for i in R.sample([x for x in range(20) if x != z - 1 and abs(x - (z - 1)) <= 3], 3)],
              "Add up the electrons: %d, so the proton number is %d." % (z, z))


ISO = [("C", 6, 12, 14), ("Cl", 17, 35, 37), ("O", 8, 16, 18), ("Mg", 12, 24, 26), ("H", 1, 1, 2), ("Li", 3, 6, 7), ("Ne", 10, 20, 22), ("K", 19, 39, 41)]


def nuc(s, z, a):
    return "<sup>%d</sup><sub>%d</sub>%s" % (a, z, s)


def g_iso():
    s, z, a1, a2 = R.choice(ISO)
    k = R.choice(["diff", "same", "nn"])
    if k == "diff":
        return tq("%s and %s are isotopes. In what way are their atoms different?" % (nuc(s, z, a1), nuc(s, z, a2)), "They have different numbers of neutrons.",
                  ["They have different numbers of protons.", "They have different numbers of electrons.", "They have different chemical properties."],
                  "Isotopes have the same proton number but different nucleon numbers; same electron configuration, so same chemical properties.")
    if k == "same":
        return tq("Why do %s and %s have the same chemical properties?" % (nuc(s, z, a1), nuc(s, z, a2)), "They have the same number of electrons, arranged in the same way.",
                  ["They have the same number of neutrons.", "They have the same mass.", "They have the same nucleon number."], "Chemical properties depend on the electrons.")
    return nq("How many more neutrons does %s have than %s?" % (nuc(s, z, a2), nuc(s, z, a1)), a2 - a1, [a2 - z, a1 - z, a2 + a1 - 2 * z], "",
              "Neutrons: %d − %d = %d and %d − %d = %d; difference = %d." % (a2, z, a2 - z, a1, z, a1 - z, a2 - a1))


GASES = [("hydrogen", 2), ("helium", 4), ("methane", 16), ("ammonia", 17), ("neon", 20), ("nitrogen", 28), ("oxygen", 32), ("hydrogen chloride", 36.5),
         ("carbon dioxide", 44), ("sulfur dioxide", 64), ("chlorine", 71)]


def g_diff():
    (a, ma), (b, mb) = R.sample(GASES, 2)
    fast = a if ma < mb else b
    slow = b if fast == a else a
    k = R.choice(["fast", "why"])
    if k == "fast":
        return tq("Which gas diffuses faster at the same temperature: %s (relative mass %s) or %s (relative mass %s)?" % (a, ex(ma), b, ex(mb)), fast, [slow, "Both diffuse at the same rate.", "Neither diffuses in air."],
                  "Lighter particles move faster on average, so they diffuse faster.")
    return tq("Why does %s diffuse faster than %s?" % (fast, slow), "Its particles have a smaller mass, so they move faster at the same temperature.",
              ["Its particles have a larger mass.", "Its particles are attracted to air.", "It is more reactive."], "Rate of diffusion falls as molecular mass rises.")


PART = [("proton", "+1", "1", "in the nucleus"), ("neutron", "0", "1", "in the nucleus"), ("electron", "−1", "1/1840 (almost 0)", "in shells around the nucleus")]


def g_part():
    p, ch, m, where = R.choice(PART)
    k = R.choice(["ch", "m", "where", "which"])
    if k == "ch":
        return tq("What is the relative charge of a %s?" % p, ch, [x[1] for x in PART if x[0] != p] + ["+2"], "Proton +1, neutron 0, electron −1.")
    if k == "m":
        return tq("What is the relative mass of a %s?" % p, m, ["1840", "2" if m != "2" else "4", "1" if m != "1" else "1/1840 (almost 0)"], "Protons and neutrons have relative mass 1; an electron's is about 1/1840.")
    if k == "where":
        return tq("Where is a %s found in an atom?" % p, where, [x[3] for x in PART if x[3] != where][:1] + ["spread evenly through the atom", "outside the atom"], "The nucleus holds protons and neutrons.")
    return tq("Which particle has a relative charge of %s?" % ch, p, [x[0] for x in PART if x[0] != p] + ["a nucleus"], "Proton +1, neutron 0, electron −1.")


STATE = [("melting", "The particles gain energy and vibrate so much that they break out of their fixed positions."),
         ("boiling", "The particles gain enough energy to overcome the forces of attraction and escape as a gas throughout the liquid."),
         ("freezing", "The particles lose energy and settle into fixed positions in a regular arrangement."),
         ("condensation", "The gas particles lose energy, slow down and come close together to form a liquid."),
         ("evaporation", "Particles with the most energy escape from the surface of the liquid below its boiling point."),
         ("sublimation", "The particles of a solid gain enough energy to escape directly into the gas state.")]
g_state = rows(R, STATE, "Which description matches %s?", "Which change of state is this? “%s”")

POOL1 = pool(R, [
    ("What is the proton number of an atom?", "the number of protons in its nucleus", ["the number of protons and neutrons", "the number of neutrons", "the number of electron shells"], "Also called the atomic number."),
    ("What is the nucleon number of an atom?", "the total number of protons and neutrons in its nucleus", ["the number of neutrons only", "the number of electrons", "the number of protons only"], "Also called the mass number."),
    ("Why is an atom electrically neutral?", "It has equal numbers of protons and electrons.", ["It has equal numbers of protons and neutrons.", "Neutrons cancel the charge.", "It has no charged particles."], "The charges cancel."),
    ("What are isotopes?", "atoms of the same element with different numbers of neutrons", ["atoms of different elements with the same mass", "atoms with different numbers of protons", "ions of the same element"], "Same proton number, different nucleon numbers."),
    ("Why does the temperature stay constant while a pure solid melts?", "The energy taken in is used to overcome the forces between particles.", ["No energy is taken in.", "The thermometer stops working.", "The particles stop moving."], "This is why pure substances have sharp melting points."),
    ("Ammonia and hydrogen chloride are released at opposite ends of a long tube. Where does the white ring of ammonium chloride form?", "nearer the hydrogen chloride end",
     ["nearer the ammonia end", "exactly in the middle", "at both ends"], "Ammonia (Mr 17) diffuses faster than hydrogen chloride (Mr 36.5)."),
    ("How does a rise in temperature affect the rate of diffusion?", "It increases it, because the particles move faster.", ["It decreases it.", "It has no effect.", "It stops diffusion."], "Particles have more kinetic energy."),
    ("What does the kinetic particle theory say about all matter?", "It is made of tiny particles in constant random motion.", ["It is made of particles that never move.", "It is continuous with no gaps.", "Only gases contain particles."], "The particles move faster at higher temperature."),
])
POOL5 = pool(R, [
    ("An atom has 11 protons, 12 neutrons and 11 electrons. What is its nucleon number?", "23", ["11", "12", "34"], "11 + 12 = 23."),
    ("An ion has 12 protons and 10 electrons. What is its charge?", "2+", ["2−", "0", "10+"], "Two more protons than electrons."),
    ("An ion has 17 protons and 18 electrons. What is it?", "a chloride ion, Cl⁻", ["an argon atom", "a chlorine atom", "a potassium ion"], "One extra electron."),
    ("Why do noble gases such as argon not form ions easily?", "Their outer shells are full, which is a stable arrangement.", ["They have no electrons.", "Their nuclei are too large.", "They are radioactive."], "Argon: 2, 8, 8."),
    ("A gas jar of bromine (brown) is placed under a jar of air. After some time both jars are evenly brown. Why?", "Particles of bromine and air move randomly and mix by diffusion.",
     ["Bromine is lighter than air.", "Air reacts with bromine.", "Bromine is pushed up by heat."], "Net movement from high to low concentration."),
    ("Why is the smell of a perfume noticed faster in a warm room than in a cold room?", "Particles move faster at a higher temperature, so diffusion is faster.", ["Perfume is heavier in a cold room.", "Cold air blocks particles.", "Warm air has no particles."], "Higher temperature, faster diffusion."),
    ("Which statement about the nucleus is correct?", "It contains almost all the mass of the atom but is very small.", ["It contains all the electrons.", "It is the largest part of the atom by volume.", "It has a negative charge."], "Electrons have almost no mass."),
    ("Element X has the electronic configuration 2, 8, 6. What is its proton number?", "16", ["6", "8", "14"], "2 + 8 + 6 = 16 (sulfur)."),
])


def main():
    sets = U.sets([
        ("States of matter and changes of state", [(g_state, 8), POOL1, (POOL5, 2), (g_diff, 3)]),
        ("Diffusion", [(g_diff, 8), (sg_dif, 5), POOL1, (POOL5, 2)]),
        ("Protons, neutrons and electrons", [(g_part, 8), (us_pne, 6), (us_find, 3), (us_ion, 3)]),
        ("Isotopes and electronic configuration", [(g_iso, 6), (us_iso, 4), (g_conf, 10)]),
        ("Exam-style questions", [(POOL5, 6), (g_conf, 6), (us_pne, 4), (us_ion, 2), (g_iso, 2)]),
    ])
    make_ol(LV, SUBJ, "particulate-nature-of-matter", SORT, "The Particulate Nature of Matter",
            "Describe the solid, liquid and gaseous states of matter and changes of state in terms of the kinetic particle theory and the energy changes involved; "
            "describe and explain diffusion and the effect of molecular mass and temperature on its rate; state the relative charges and approximate relative masses of "
            "protons, neutrons and electrons; define proton (atomic) number and nucleon (mass) number and use nuclide notation; define isotopes; describe the build-up of "
            "electrons in shells for the first 20 elements (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "The Particulate Nature of Matter", "Particulate nature",
            "Free Secondary 3 O-Level Chemistry worksheets on the particulate nature of matter: kinetic particle theory, changes of state, diffusion, atomic structure, "
            "isotopes and electronic configuration. 100 questions with answers.",
            "Atoms: protons and neutrons in the nucleus, electrons in shells.", "Lighter gas molecules diffuse faster.",
            "<p><b>Matter is made of particles; atoms are made of protons, neutrons and electrons.</b></p><ul>"
            "<li>Changes of state: particles gain or lose energy; the temperature stays constant while a pure substance melts or boils.</li>"
            "<li>Diffusion is faster for lighter molecules and at higher temperature.</li>"
            "<li>Proton +1 (mass 1), neutron 0 (mass 1), electron −1 (mass about 1/1840). Proton number Z; nucleon number A = protons + neutrons.</li>"
            "<li>Isotopes: same Z, different numbers of neutrons. Electron shells hold 2, 8, 8 for the first 20 elements.</li></ul>",
            [("Neutrons in ³⁷₁₇Cl?", ["37 − 17"], "20"),
             ("Electronic configuration of aluminium (Z = 13)?", ["2 + 8 + 3"], "2, 8, 3")],
            ["Calling the nucleon number the number of neutrons. It is protons + neutrons.", "Saying isotopes have different numbers of protons.",
             "Thinking heavier gas molecules diffuse faster.", "Putting more than 2 electrons in the first shell."],
            [("How do you find the number of neutrons?", "Subtract the proton number from the nucleon number: neutrons = A − Z."),
             ("What are isotopes?", "Atoms of the same element (same number of protons) with different numbers of neutrons, so different nucleon numbers. They have the same chemical properties."),
             ("How are electrons arranged in the first 20 elements?", "Up to 2 in the first shell, then up to 8 in the second and 8 in the third; calcium is 2, 8, 8, 2.")],
            sets)


if __name__ == "__main__":
    main()
