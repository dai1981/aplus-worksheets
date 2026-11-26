# -*- coding: utf-8 -*-
"""
US High School Chemistry: The Mole and Molar Mass (HS-PS1-7)
  python tools/gen_us_science_chem_the_mole_and_molar_mass.py
Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical
reaction (the mole links counted particles to measured mass).
Avogadro's number, molar mass, grams to moles and moles to grams, particles, moles of atoms in a compound and percent
composition. Atomic masses are rounded classroom values (H = 1, C = 12, O = 16, Cl = 35.5 …) and are given in each question.
Wrong answers come from real mistakes: "multiply by molar mass to get moles", "forget the subscript", "a mole of water
has 1 mole of atoms".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import sub, atoms

U = Unit(90207)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


AM = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "Al": 27, "S": 32, "Cl": 35.5, "K": 39, "Ca": 40, "Fe": 56, "Cu": 63.5}
CMP = [("water", "H2O"), ("carbon dioxide", "CO2"), ("methane", "CH4"), ("ammonia", "NH3"), ("sodium chloride", "NaCl"), ("glucose", "C6H12O6"),
       ("calcium carbonate", "CaCO3"), ("sulfuric acid", "H2SO4"), ("magnesium oxide", "MgO"), ("oxygen gas", "O2"), ("nitrogen gas", "N2"),
       ("sodium hydroxide", "NaOH"), ("ethanol", "C2H6O"), ("propane", "C3H8"), ("iron(III) oxide", "Fe2O3"), ("calcium chloride", "CaCl2"),
       ("potassium chloride", "KCl"), ("aluminum oxide", "Al2O3"), ("copper(II) sulfate", "CuSO4"), ("hydrogen chloride", "HCl"), ("sodium carbonate", "Na2CO3"),
       ("magnesium chloride", "MgCl2"), ("nitric acid", "HNO3"), ("sucrose", "C12H22O11")]


def num(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return "{:,}".format(int(s)) if "." not in s and abs(x) >= 1000 else s


def mm(f):
    return sum(AM[k] * v for k, v in atoms(f).items())


def given(f):
    return ", ".join("%s = %s" % (k, num(AM[k])) for k in sorted(atoms(f), key=lambda k: list(AM).index(k)))


def nm(c):
    return "%s (%s)" % (c[0], sub(c[1]))


def g_mm():
    c = R.choice(CMP)
    if not once(("mm", c[1])):
        return None
    a = atoms(c[1])
    m = mm(c[1])
    w = [sum(AM[k] for k in a), m + AM[min(a, key=lambda k: AM[k])], sum(AM[k] * v for k, v in a.items() if k != "H") if "H" in a else m - AM[max(a, key=lambda k: AM[k])], m * 2]
    w = [num(x) + " g/mol" for x in dict.fromkeys(w) if x != m and x > 0][:3]
    if len(w) < 3:
        return None
    parts = " + ".join("%d × %s" % (v, num(AM[k])) if v > 1 else num(AM[k]) for k, v in a.items())
    return item("What is the molar mass of %s? (%s)" % (nm(c), given(c[1])), num(m) + " g/mol", w, "%s = %s g/mol." % (parts, num(m)))


MOLES = [0.1, 0.2, 0.25, 0.5, 1.5, 2, 2.5, 3, 4, 5, 0.75, 10]


def g_g2mol():
    c = R.choice(CMP)
    n = R.choice(MOLES)
    m = mm(c[1])
    g = m * n
    if g != round(g, 1) or not once(("gm", c[1], n)):
        return None
    w = [m / g if g else 1, n * 2, n / 2, n + 1]
    w = [num(round(x, 2)) + " mol" for x in dict.fromkeys(w) if round(x, 2) != n and x > 0][:3]
    if len(w) < 3:
        return None
    return item("How many moles are in %s g of %s? (Molar mass = %s g/mol)" % (num(g), nm(c), num(m)), num(n) + " mol", w, "moles = mass ÷ molar mass = %s ÷ %s = %s mol." % (num(g), num(m), num(n)))


def g_mol2g():
    c = R.choice(CMP)
    n = R.choice(MOLES)
    m = mm(c[1])
    g = m * n
    if g != round(g, 1) or not once(("mg", c[1], n)):
        return None
    w = [m / n, m, g * 2, g + m]
    w = [num(round(x, 2)) + " g" for x in dict.fromkeys(w) if round(x, 2) != round(g, 2) and x > 0][:3]
    if len(w) < 3:
        return None
    return item("What is the mass of %s mol of %s? (Molar mass = %s g/mol)" % (num(n), nm(c), num(m)), num(g) + " g", w, "mass = moles × molar mass = %s × %s = %s g." % (num(n), num(m), num(g)))


def sci(x):
    e = 0
    while x >= 10:
        x /= 10
        e += 1
    while x < 1:
        x *= 10
        e -= 1
    return "%.2f × 10<sup>%d</sup>" % (x, e)


def g_part():
    c = R.choice(CMP)
    n = R.choice([0.5, 2, 3, 0.25, 1.5, 4, 5, 0.1, 10])
    k = R.choice(["n2p", "p2n"])
    if not once(("pt", c[1], n, k)):
        return None
    p = 6.02e23 * n
    if k == "n2p":
        w = [sci(6.02e23 / n), sci(p * 10), "%s" % num(n * 6.02)]
        w = list(dict.fromkeys(x for x in w if x != sci(p)))
        if len(w) < 3:
            return None
        return item("How many particles (molecules or formula units) are in %s mol of %s?" % (num(n), nm(c)), sci(p), w, "%s × 6.02 × 10<sup>23</sup> = %s." % (num(n), sci(p)))
    w = [num(n * 2), num(round(1 / n, 2)) if n != 1 else "6.02", sci(p)]
    w = [x + (" mol" if "10" not in x else " mol") for x in dict.fromkeys(w) if x != num(n)][:3]
    if len(w) < 3:
        return None
    return item("A sample has %s particles of %s. How many moles is that?" % (sci(p), nm(c)), num(n) + " mol", w, "%s ÷ 6.02 × 10<sup>23</sup> = %s mol." % (sci(p), num(n)))


def g_atoms():
    c = R.choice([x for x in CMP if len(atoms(x[1])) > 1])
    a = atoms(c[1])
    n = R.choice([1, 2, 3, 0.5, 4])
    k = R.choice(["el", "all"])
    el = R.choice(sorted(a))
    if not once(("at", c[1], n, k, el if k == "el" else "")):
        return None
    if k == "el":
        v = a[el] * n
        w = [n, a[el], v * 2, v + n]
        w = [num(x) + " mol" for x in dict.fromkeys(w) if x != v and x > 0][:3]
        if len(w) < 3:
            return None
        return item("How many moles of %s atoms are in %s mol of %s?" % (el, num(n), nm(c)), num(v) + " mol", w, "Each formula has %d %s, so %s × %d = %s mol." % (a[el], el, num(n), a[el], num(v)))
    t = sum(a.values())
    v = t * n
    w = [n, t, v * 2, v - n]
    w = [num(x) + " mol" for x in dict.fromkeys(w) if x != v and x > 0][:3]
    if len(w) < 3:
        return None
    return item("How many moles of atoms in total are in %s mol of %s?" % (num(n), nm(c)), num(v) + " mol", w, "Each formula has %d atoms, so %s × %d = %s mol." % (t, num(n), t, num(v)))


def g_pct():
    c = R.choice(CMP)
    a = atoms(c[1])
    el = R.choice(sorted(a))
    m = mm(c[1])
    p = 100 * AM[el] * a[el] / m
    if not once(("pc", c[1], el)):
        return None
    s = "%.1f%%" % p
    w = ["%.1f%%" % (100 * AM[el] / m), "%.1f%%" % (100 - p), "%.1f%%" % (100 * a[el] / sum(a.values()))]
    w = list(dict.fromkeys(x for x in w if x != s))
    if len(w) < 3:
        w.append("%.1f%%" % (p / 2))
        w = list(dict.fromkeys(x for x in w if x != s))
    if len(w) < 3:
        return None
    return item("What percent of the mass of %s is %s? (%s; molar mass = %s g/mol)" % (nm(c), el, given(c[1]), num(m)), s, w[:3],
                "%d × %s ÷ %s × 100 = %s." % (a[el], num(AM[el]), num(m), s))


B1 = bank([
    ("What is a mole?", "6.02 × 10²³ particles of a substance", ["the mass of one atom", "1 gram of any substance", "1 liter of gas"], "Avogadro's number."),
    ("What is molar mass?", "the mass in grams of one mole of a substance", ["the mass of one molecule in kilograms", "the number of atoms in a molecule", "the volume of one mole"], "Units: g/mol."),
    ("How do you change grams to moles?", "divide by the molar mass", ["multiply by the molar mass", "multiply by 6.02 × 10²³", "add the molar mass"], "mol = g ÷ (g/mol)."),
    ("How do you change moles to grams?", "multiply by the molar mass", ["divide by the molar mass", "divide by 6.02 × 10²³", "subtract the molar mass"], "g = mol × g/mol."),
    ("Why do chemists use moles?", "Atoms are too small to count one by one, so moles link counts to masses we can weigh.", ["Moles are lighter.", "Grams do not exist in chemistry.", "Moles change in reactions."], "Counting by weighing."),
    ("One mole of carbon (12 g) and one mole of oxygen gas (32 g) have the same what?", "number of particles", ["mass", "density", "color"], "Both 6.02 × 10²³ particles."),
    ("Which has more atoms: 1 mol of H₂O or 1 mol of He?", "1 mol of H₂O (3 mol of atoms)", ["1 mol of He", "They have the same number of atoms", "It cannot be known"], "Each H₂O has 3 atoms."),
    ("Where do you find the molar mass of an element?", "the average atomic mass on the periodic table, in g/mol", ["the atomic number", "the group number", "the number of neutrons"], "Carbon: 12.01 g/mol."),
])
B5 = bank([
    ("A recipe for a reaction needs 2 mol of NaCl. Why does a chemist weigh 117 g instead of counting?", "117 g of NaCl contains 2 mol (2 × 58.5 g/mol).", ["Counting is faster.", "Moles cannot be weighed.", "117 g is 1 mol."], "Molar mass links them."),
    ("Which sample has the most molecules: 18 g of water, 44 g of CO₂ or 16 g of CH₄?", "They all have the same number (1 mol each).", ["18 g of water", "44 g of CO₂", "16 g of CH₄"], "Each is one mole."),
    ("A student says 2 g of hydrogen gas has more molecules than 32 g of oxygen gas because it sounds smaller. What is right?", "Both are 1 mol, so they have the same number of molecules.", ["Hydrogen has more.", "Oxygen has more.", "Neither has molecules."], "2 g/mol vs 32 g/mol."),
    ("Why is the molar mass of chlorine 35.45 and not a whole number?", "It is an average of its isotopes weighted by abundance.", ["Chlorine atoms are broken.", "It is measured badly.", "It includes electrons only."], "Isotopes."),
    ("A sample of iron has a mass of 112 g (Fe = 56). How many atoms is that?", "2 mol = 1.20 × 10²⁴ atoms", ["56 atoms", "112 atoms", "6.02 × 10²³ atoms"], "112 ÷ 56 = 2 mol."),
])


def body():
    think = ("<p><b>The mole links counting to weighing.</b></p>"
             "<ul><li>1 mol = 6.02 × 10<sup>23</sup> particles. Molar mass (g/mol) = sum of the atomic masses in the formula.</li>"
             "<li>grams ÷ molar mass = moles; moles × molar mass = grams; moles × 6.02 × 10<sup>23</sup> = particles.</li>"
             "<li>Subscripts tell how many moles of each atom are in one mole of the compound.</li></ul>")
    ex = [("Molar mass of H<sub>2</sub>O (H = 1, O = 16)?", ["2 × 1 + 16"], "18 g/mol"),
          ("Moles in 36 g of water?", ["36 ÷ 18"], "2 mol")]
    mist = ["Multiplying by molar mass when changing grams to moles.", "Forgetting a subscript when adding atomic masses.", "Thinking 1 mol of a compound has 1 mol of atoms."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Molar mass", B1 + [(g_mm, 12)]),
        ("Grams and moles", [(g_mm, 6), (g_g2mol, 7), (g_mol2g, 7)]),
        ("Particles and atoms", [(g_part, 10), (g_atoms, 10)]),
        ("Mole conversions", [(g_g2mol, 7), (g_mol2g, 7), (g_atoms, 6)]),
        ("Percent composition", B5 + [(g_pct, 10), (g_part, 5)]),
    ])
    make("chemistry", "the-mole-and-molar-mass", 7, "HS-PS1-7",
         "Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical reaction.",
         "The Mole and Molar Mass",
         "Mole Worksheets: Molar Mass, Grams to Moles and Avogadro's Number (High School Chemistry)",
         "The Mole",
         "Free high school chemistry worksheets on the mole (NGSS HS-PS1-7): molar mass, grams to moles, moles to particles with Avogadro's number and percent composition. 100 questions with answers.",
         "One mole = 6.02 × 10²³ particles.",
         "Molar mass turns grams into moles, and moles into particles.",
         body(),
         [("How do you find molar mass?", "Add the atomic masses of all the atoms in the formula, multiplying each by its subscript. For H₂O: 2 × 1 + 16 = 18 g/mol."),
          ("How do you convert grams to moles?", "Divide the mass in grams by the molar mass in g/mol."),
          ("What is Avogadro's number?", "6.02 × 10²³, the number of particles in one mole of a substance.")],
         sets)


if __name__ == "__main__":
    main()
