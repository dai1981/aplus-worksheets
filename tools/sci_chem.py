# -*- coding: utf-8 -*-
"""
Shared chemistry data for the US high school Chemistry units (gen_us_science_chem_*).
EL: main-group and a few common transition elements with symbol, name, atomic number, mass number of the most common
isotope, average atomic mass (to 2 decimals, as on a classroom periodic table), group (1-18) and period.
"""

# (symbol, name, Z, A of most common isotope, average atomic mass, group, period, kind)
EL = [
    ("H", "hydrogen", 1, 1, 1.01, 1, 1, "nonmetal"), ("He", "helium", 2, 4, 4.00, 18, 1, "nonmetal"),
    ("Li", "lithium", 3, 7, 6.94, 1, 2, "metal"), ("Be", "beryllium", 4, 9, 9.01, 2, 2, "metal"),
    ("B", "boron", 5, 11, 10.81, 13, 2, "metalloid"), ("C", "carbon", 6, 12, 12.01, 14, 2, "nonmetal"),
    ("N", "nitrogen", 7, 14, 14.01, 15, 2, "nonmetal"), ("O", "oxygen", 8, 16, 16.00, 16, 2, "nonmetal"),
    ("F", "fluorine", 9, 19, 19.00, 17, 2, "nonmetal"), ("Ne", "neon", 10, 20, 20.18, 18, 2, "nonmetal"),
    ("Na", "sodium", 11, 23, 22.99, 1, 3, "metal"), ("Mg", "magnesium", 12, 24, 24.31, 2, 3, "metal"),
    ("Al", "aluminum", 13, 27, 26.98, 13, 3, "metal"), ("Si", "silicon", 14, 28, 28.09, 14, 3, "metalloid"),
    ("P", "phosphorus", 15, 31, 30.97, 15, 3, "nonmetal"), ("S", "sulfur", 16, 32, 32.07, 16, 3, "nonmetal"),
    ("Cl", "chlorine", 17, 35, 35.45, 17, 3, "nonmetal"), ("Ar", "argon", 18, 40, 39.95, 18, 3, "nonmetal"),
    ("K", "potassium", 19, 39, 39.10, 1, 4, "metal"), ("Ca", "calcium", 20, 40, 40.08, 2, 4, "metal"),
    ("Fe", "iron", 26, 56, 55.85, 8, 4, "metal"), ("Cu", "copper", 29, 63, 63.55, 11, 4, "metal"),
    ("Zn", "zinc", 30, 64, 65.38, 12, 4, "metal"), ("Ga", "gallium", 31, 69, 69.72, 13, 4, "metal"),
    ("Ge", "germanium", 32, 74, 72.63, 14, 4, "metalloid"), ("As", "arsenic", 33, 75, 74.92, 15, 4, "metalloid"),
    ("Se", "selenium", 34, 80, 78.97, 16, 4, "nonmetal"), ("Br", "bromine", 35, 79, 79.90, 17, 4, "nonmetal"),
    ("Kr", "krypton", 36, 84, 83.80, 18, 4, "nonmetal"), ("Rb", "rubidium", 37, 85, 85.47, 1, 5, "metal"),
    ("Sr", "strontium", 38, 88, 87.62, 2, 5, "metal"), ("Ag", "silver", 47, 107, 107.87, 11, 5, "metal"),
    ("Sn", "tin", 50, 120, 118.71, 14, 5, "metal"), ("I", "iodine", 53, 127, 126.90, 17, 5, "nonmetal"),
    ("Xe", "xenon", 54, 132, 131.29, 18, 5, "nonmetal"), ("Cs", "cesium", 55, 133, 132.91, 1, 6, "metal"),
    ("Ba", "barium", 56, 138, 137.33, 2, 6, "metal"), ("Au", "gold", 79, 197, 196.97, 11, 6, "metal"),
    ("Pb", "lead", 82, 208, 207.2, 14, 6, "metal"),
]
BY = {e[0]: e for e in EL}
MAIN = [e for e in EL if e[5] in (1, 2, 13, 14, 15, 16, 17, 18)]
FAMILY = {1: "alkali metals", 2: "alkaline earth metals", 17: "halogens", 18: "noble gases"}


def valence(e):
    """valence electrons of a main-group element (He has 2)"""
    if e[0] == "He":
        return 2
    g = e[5]
    return g if g <= 2 else g - 10


def ion_charge(e):
    """usual ion charge of a main-group element, or None"""
    if e[5] in (1, 2) and e[0] != "H":
        return e[5]
    if e[0] in ("Al", "Ga"):
        return 3
    if e[0] in ("N", "P"):
        return -3
    if e[0] in ("O", "S", "Se"):
        return -2
    if e[5] == 17:
        return -1
    return None


def shells(z):
    """Bohr shells for Z <= 20: 2, 8, 8, 2"""
    out = []
    for cap in (2, 8, 8, 2):
        if z <= 0:
            break
        out.append(min(cap, z))
        z -= cap
    return out


def chg(c):
    """+2 -> '2+', -1 -> '−' style superscript text"""
    if c == 0:
        return ""
    n = "" if abs(c) == 1 else str(abs(c))
    return n + ("+" if c > 0 else "−")


def ion(sym, c):
    return "%s<sup>%s</sup>" % (sym, chg(c))


def nuclide(sym, a, z=None):
    """isotope notation with mass number on top"""
    if z is None:
        return "<sup>%d</sup>%s" % (a, sym)
    return "<sup>%d</sup><sub>%d</sub>%s" % (a, z, sym)


def sub(formula):
    """'H2O' -> H<sub>2</sub>O"""
    out = ""
    for ch in formula:
        out += "<sub>%s</sub>" % ch if ch.isdigit() else ch
    return out.replace("</sub><sub>", "")


# trend data for main-group elements: electronegativity (Pauling), first ionization energy (kJ/mol), atomic radius (pm)
EN = {"H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90,
      "P": 2.19, "S": 2.58, "Cl": 3.16, "K": 0.82, "Ca": 1.00, "Ga": 1.81, "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96, "Rb": 0.82,
      "Sr": 0.95, "Sn": 1.96, "I": 2.66, "Cs": 0.79, "Ba": 0.89}
IE = {"H": 1312, "He": 2372, "Li": 520, "Be": 899, "B": 801, "C": 1086, "N": 1402, "O": 1314, "F": 1681, "Ne": 2081, "Na": 496, "Mg": 738,
      "Al": 578, "Si": 787, "P": 1012, "S": 1000, "Cl": 1251, "Ar": 1521, "K": 419, "Ca": 590, "Ga": 579, "Ge": 762, "As": 947, "Se": 941,
      "Br": 1140, "Kr": 1351, "Rb": 403, "Sr": 549, "Sn": 709, "I": 1008, "Xe": 1170, "Cs": 376, "Ba": 503}
RAD = {"Li": 152, "Be": 112, "B": 85, "C": 77, "N": 75, "O": 73, "F": 72, "Na": 186, "Mg": 160, "Al": 143, "Si": 118, "P": 110, "S": 103,
       "Cl": 99, "K": 227, "Ca": 197, "Ga": 135, "Ge": 122, "As": 120, "Se": 119, "Br": 114, "Rb": 248, "Sr": 215, "Sn": 140, "I": 133,
       "Cs": 265, "Ba": 222}
