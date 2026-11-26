# -*- coding: utf-8 -*-
"""
US High School Chemistry: Atomic Structure and Isotopes (HS-PS1-1)
  python tools/gen_us_science_chem_atomic_structure_and_isotopes.py
Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons
in the outermost energy level of atoms.
Protons, neutrons and electrons; atomic number and mass number; isotopes and isotope notation; average atomic mass;
ions; electron shells (Bohr model) and valence electrons.
Wrong answers come from real mistakes: "neutrons = atomic number", "mass number = protons + electrons",
"an ion changes its number of protons", "average mass is the simple average of the isotopes".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import EL, BY, valence, ion_charge, shells, ion, nuclide

U = Unit(90201)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def three(a, cands):
    """first 3 distinct candidates that are not the answer"""
    out = []
    for c in cands:
        c = str(c)
        if c != str(a) and c not in out and not c.startswith("-"):
            out.append(c)
    return out[:3] if len(out) >= 3 else None


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def iso_a(e):
    """a believable mass number for an isotope of e"""
    a = e[3] + R.choice([0, 0, 1, 2, -1]) if e[2] > 2 else e[3]
    return max(a, e[2])


def g_pne():
    e = R.choice(EL)
    a = iso_a(e)
    z = e[2]
    n = a - z
    k = R.choice(["n", "p", "e", "n2"])
    if not once(("pne", e[0], a, k)):
        return None
    if k == "n":
        return item("How many neutrons are in an atom of %s-%d?" % (e[1], a), str(n), three(n, [z, a, a + z, n + 1]), "Neutrons = mass number − atomic number = %d − %d = %d." % (a, z, n))
    if k == "n2":
        return item("How many neutrons are in %s?" % nuclide(e[0], a, z), str(n), three(n, [z, a, n + 1, n - 1]), "%d − %d = %d." % (a, z, n))
    if k == "p":
        return item("How many protons are in an atom of %s-%d?" % (e[1], a), str(z), three(z, [n, a, z + 1, z + 2, a - 1]),
                    "The atomic number (%d) is the number of protons." % z)
    return item("A neutral atom of %s has a mass number of %d. How many electrons does it have?" % (e[1], a), str(z), three(z, [n, a, z - 1, z + 1, z + 2]),
                "In a neutral atom, electrons = protons = %d." % z)


def g_find():
    e = R.choice(EL)
    a = iso_a(e)
    k = R.choice(["el", "mass", "el2"])
    if not once(("fd", e[0], a, k)):
        return None
    z = e[2]
    if k == "el":
        others = [x[1] for x in R.sample([x for x in EL if abs(x[2] - z) <= 3 and x != e] or EL, 3)]
        if len(set(others)) < 3:
            return None
        return item("An atom has %d protons. Which element is it?" % z, e[1], others, "The number of protons decides the element.")
    if k == "mass":
        return item("An atom has %d protons and %d neutrons. What is its mass number?" % (z, a - z), str(a), three(a, [z, a - z, a + z, a + 1]), "%d + %d = %d." % (z, a - z, a))
    wrong = []
    for x in EL:
        if x[2] == a - z and x != e:
            wrong.append(x[1])
    near = [x[1] for x in EL if x[2] in (z - 1, z + 1)]
    pool = list(dict.fromkeys(wrong + near + [x[1] for x in R.sample(EL, 6)]))
    pool = [p for p in pool if p != e[1]][:3]
    return item("An atom has %d neutrons and %d protons. Which element is it?" % (a - z, z), e[1], pool, "Use the protons (%d), not the neutrons." % z)


def g_iso():
    e = R.choice([x for x in EL if x[2] > 2])
    a = e[3]
    b = a + R.choice([1, 2])
    k = R.choice(["same", "diff", "pick"])
    if not once(("is", e[0], b, k)):
        return None
    if k == "same":
        return item("%s-%d and %s-%d are isotopes. What do they have the same number of?" % (e[1].capitalize(), a, e[1], b), "protons", ["neutrons", "mass number", "total particles in the nucleus"],
                    "Isotopes have the same protons but different neutrons.")
    if k == "diff":
        return item("How many more neutrons does %s have than %s?" % (nuclide(e[0], b), nuclide(e[0], a)), str(b - a), [str(e[2]), "0", str(b)], "%d − %d = %d." % (b, a, b - a))
    o = R.choice([x for x in EL if x[2] in (e[2] - 1, e[2] + 1)])
    good = "%s and %s" % (nuclide(e[0], a, e[2]), nuclide(e[0], b, e[2]))
    w = ["%s and %s" % (nuclide(e[0], a, e[2]), nuclide(o[0], a, o[2])), "%s and %s" % (nuclide(e[0], b, e[2]), nuclide(o[0], b, o[2])),
         "%s and %s" % (nuclide(o[0], o[3], o[2]), nuclide(e[0], o[3], e[2]))]
    if len({good, *w}) < 4:
        return None
    return item("Which pair are isotopes of the same element?", good, w, "Same atomic number, different mass numbers.")


def g_avg():
    who = P.next()[0]
    a = R.randint(10, 80)
    p = R.choice([10, 15, 20, 25, 30, 40, 60, 70, 75, 80, 85, 90])
    avg = (a * p + (a + 2) * (100 - p)) / 100
    if not once(("av", a, p)):
        return None
    s = "%.2f" % avg
    w = ["%.2f" % (a + 1), "%.2f" % ((a * (100 - p) + (a + 2) * p) / 100), "%.2f" % (a + 2)]
    if len({s, *w}) < 4:
        return None
    return item("%s finds that element X has two isotopes: %d%% has mass %d u and %d%% has mass %d u. What is the average atomic mass?" % (who, p, a, 100 - p, a + 2), s + " u", [x + " u" for x in w],
                "%d × %.2f + %d × %.2f = %s u." % (a, p / 100, a + 2, (100 - p) / 100, s))


def arr(z):
    return ", ".join(map(str, shells(z)))


def g_shell():
    e = R.choice([x for x in EL if x[2] <= 20])
    z = e[2]
    k = R.choice(["arr", "val", "n"])
    if not once(("sh", e[0], k)):
        return None
    sh = shells(z)
    if k == "arr":
        w = set()
        if len(sh) >= 2:
            w.add(", ".join(map(str, [sh[0] + 1] + sh[1:-1] + [sh[-1] - 1])) if sh[-1] > 1 else ", ".join(map(str, sh[:-1] + [sh[-1] + 1])))
        w.add(", ".join(map(str, [z])) if z > 2 else "1, %d" % (z - 1) if z == 2 else "0, 1")
        w.add(", ".join(map(str, [min(8, z)] + ([z - 8] if z > 8 else []))) if z > 2 else "2, %d" % z)
        w.add(", ".join(map(str, list(reversed(sh)))) if len(sh) > 1 and sh != list(reversed(sh)) else "8, %d" % z)
        w.add("2, 2, %d" % max(z - 4, 1))
        w = [x for x in w if x != arr(z)]
        if len(w) < 3:
            return None
        return item("What is the electron arrangement (shells) of %s atom (%d electrons)?" % (an(e[1]), z), arr(z), R.sample(sorted(w), 3), "Fill 2, then 8, then 8, then 2.")
    if k == "val":
        v = sh[-1]
        return item("%s atom has the electron arrangement %s. How many valence electrons does it have?" % (an(e[1]).capitalize(), arr(z)), str(v),
                    [str(x) for x in R.sample([x for x in range(1, 9) if x != v and x != z], 3)], "Valence electrons are in the outer shell.")
    n = len(sh)
    return item("How many electron shells are occupied in %s atom?" % an(e[1]), str(n), [str(x) for x in (1, 2, 3, 4, 5) if x != n][:3], "%d electrons: %s." % (z, arr(z)))


def g_ion():
    e = R.choice([x for x in EL if ion_charge(x)])
    c = ion_charge(e)
    z = e[2]
    k = R.choice(["e", "p", "why"])
    if not once(("io", e[0], k)):
        return None
    if k == "e":
        return item("How many electrons are in the ion %s?" % ion(e[0], c), str(z - c), three(z - c, [z, z + c, z - c + 1, z - c - 1]),
                    "%d protons; charge %s means %s electrons." % (z, ("+%d" % c) if c > 0 else "−%d" % (-c), z - c))
    if k == "p":
        return item("How many protons are in the ion %s?" % ion(e[0], c), str(z), three(z, [z - c, z + c, z + 1, z + 2]),
                    "Forming an ion changes electrons, not protons.")
    word = "loses %d electron%s" % (c, "s" if c > 1 else "") if c > 0 else "gains %d electron%s" % (-c, "s" if c < -1 else "")
    other = "gains %d electron%s" % (abs(c), "s" if abs(c) > 1 else "") if c > 0 else "loses %d electron%s" % (-c, "s" if c < -1 else "")
    return item("How does %s atom form the ion %s?" % (an(e[1]), ion(e[0], c)), "It %s." % word, ["It %s." % other, "It gains %d protons." % abs(c), "It loses %d neutrons." % abs(c)],
                "Ions form by gaining or losing electrons.")


B1 = bank([
    ("Which particle has a positive charge?", "proton", ["neutron", "electron", "nucleus"], "Protons are +1."),
    ("Which particle has no charge?", "neutron", ["proton", "electron", "ion"], "Neutrons are neutral."),
    ("Where are electrons found?", "in energy levels (shells) around the nucleus", ["inside the nucleus", "inside protons", "only in ions"], "The nucleus holds protons and neutrons."),
    ("Which part of the atom has almost all of its mass?", "the nucleus", ["the electron cloud", "the outer shell", "the valence electrons"], "Protons and neutrons are about 1,800 times heavier than electrons."),
    ("What does the atomic number tell you?", "the number of protons", ["the number of neutrons", "the mass of the atom", "protons plus neutrons"], "It identifies the element."),
    ("What is the mass number?", "protons + neutrons", ["protons + electrons", "only neutrons", "only protons"], "Particles in the nucleus."),
    ("What are isotopes?", "atoms of the same element with different numbers of neutrons", ["atoms of different elements", "atoms with different numbers of protons", "charged atoms"], "Carbon-12 and carbon-14."),
    ("What are valence electrons?", "the electrons in the outermost shell", ["all the electrons in an atom", "electrons in the nucleus", "the electrons in the first shell"], "They decide how an atom reacts."),
])
B5 = bank([
    ("Rutherford fired particles at gold foil. Most passed through, but a few bounced back. What did this show?", "Atoms have a small, dense, positive nucleus and are mostly empty space.",
     ["Atoms are solid balls.", "Electrons are in the nucleus.", "Atoms have no charge."], "The gold foil experiment."),
    ("Why do elements in the same column have similar properties?", "They have the same number of valence electrons.", ["They have the same mass.", "They have the same number of neutrons.", "They are the same size."], "Outer electrons decide reactions."),
    ("Chlorine's average atomic mass is 35.45 u. Which isotope is more common?", "chlorine-35", ["chlorine-37", "They are equally common.", "chlorine-36"], "The average is closer to 35."),
    ("Thomson discovered that atoms contain tiny negative particles. What were they?", "electrons", ["protons", "neutrons", "nuclei"], "Cathode ray experiments."),
    ("Why is an atom neutral overall?", "It has equal numbers of protons and electrons.", ["It has no protons.", "Neutrons cancel the charge.", "It has equal protons and neutrons."], "+ and − balance."),
])


def body():
    think = ("<p><b>Protons decide the element; electrons decide how it reacts.</b></p>"
             "<ul><li>Atomic number = protons. Mass number = protons + neutrons. Neutral atom: electrons = protons.</li>"
             "<li>Isotopes: same protons, different neutrons. Average atomic mass is weighted by how common each isotope is.</li>"
             "<li>Electrons fill shells 2, 8, 8, … The outer (valence) electrons control chemistry. Ions gain or lose electrons.</li></ul>")
    ex = [("Neutrons in sodium-23 (atomic number 11)?", ["23 − 11"], "12"),
          ("Electrons in O<sup>2−</sup> (8 protons)?", ["Gain 2 electrons: 8 + 2"], "10")]
    mist = ["Using the mass number as the number of neutrons.", "Thinking an ion changes its number of protons.", "Taking a simple average of isotope masses."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Particles in the atom", B1 + [(g_pne, 12)]),
        ("Counting particles", [(g_pne, 12), (g_find, 8)]),
        ("Isotopes", [(g_iso, 10), (g_avg, 6), (g_find, 4)]),
        ("Electron shells and ions", [(g_shell, 14), (g_ion, 6)]),
        ("Models and evidence", B5 + [(g_avg, 6), (g_ion, 4), (g_shell, 5)]),
    ])
    make("chemistry", "atomic-structure-and-isotopes", 1, "HS-PS1-1",
         "Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons in the outermost energy level of atoms.",
         "Atomic Structure and Isotopes",
         "Atomic Structure Worksheets: Protons, Neutrons, Electrons and Isotopes (High School Chemistry)",
         "Atomic Structure",
         "Free high school chemistry worksheets on atomic structure (NGSS HS-PS1-1): protons, neutrons and electrons, isotopes, average atomic mass, ions and electron shells. 100 questions with answers.",
         "Protons decide the element.",
         "Neutrons make isotopes; outer electrons decide how an atom reacts.",
         body(),
         [("How do you find the number of neutrons?", "Subtract the atomic number from the mass number. For carbon-14: 14 − 6 = 8 neutrons."),
          ("What is the difference between isotopes and ions?", "Isotopes have different numbers of neutrons. Ions have gained or lost electrons and carry a charge."),
          ("How is average atomic mass calculated?", "Multiply each isotope's mass by its fraction (percent ÷ 100) and add the results.")],
         sets)


if __name__ == "__main__":
    main()
