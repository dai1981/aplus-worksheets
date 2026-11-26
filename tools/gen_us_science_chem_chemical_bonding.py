# -*- coding: utf-8 -*-
"""
US High School Chemistry: Chemical Bonding (HS-PS1-1, HS-PS1-2)
  python tools/gen_us_science_chem_chemical_bonding.py
Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons in
the outermost energy level of atoms; explain the outcome of simple reactions from outer electron states.
Ionic, covalent and metallic bonds; ionic formulas from ion charges and their names; how many bonds an atom forms;
single, double and triple bonds and lone pairs; bond polarity from electronegativity differences; properties of
ionic and covalent substances.
Wrong answers come from real mistakes: "NaCl atoms share electrons", "MgCl", "the charges are the subscripts in the
same order", "two nonmetals form an ionic bond".
"""
from math import gcd
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import BY, MAIN, EN, ion_charge, sub

U = Unit(90203)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def name(e):
    return "%s (%s)" % (e[1], e[0])


METALS = ["Li", "Na", "K", "Mg", "Ca", "Ba", "Al", "Sr"]
NONMET = ["F", "Cl", "Br", "I", "O", "S", "N", "P"]
ANION = {"F": "fluoride", "Cl": "chloride", "Br": "bromide", "I": "iodide", "O": "oxide", "S": "sulfide", "N": "nitride", "P": "phosphide"}


def formula(m, x):
    a, b = ion_charge(BY[m]), -ion_charge(BY[x])
    g = gcd(a, b)
    nm, nx = b // g, a // g
    return m + (str(nm) if nm > 1 else "") + x + (str(nx) if nx > 1 else ""), nm, nx


def fstr(m, nm, x, nx):
    return m + (str(nm) if nm > 1 else "") + x + (str(nx) if nx > 1 else "")


def g_btype():
    k = R.choice(["mn", "nn", "mm"])
    if k == "mn":
        a, b = BY[R.choice(METALS + ["Fe", "Cu", "Zn"])], BY[R.choice(NONMET)]
        t = "ionic"
    elif k == "nn":
        a, b = [BY[x] for x in R.sample(["H", "C", "N", "O", "F", "S", "Cl", "P", "Br", "I"], 2)]
        t = "covalent"
    else:
        a, b = [BY[x] for x in R.sample(["Na", "Mg", "Al", "Fe", "Cu", "Zn", "Au", "Ag", "Sn", "Pb"], 2)]
        t = "metallic"
    if not once(("bt", tuple(sorted((a[0], b[0]))))):
        return None
    return item("What kind of bond forms between %s and %s?" % (name(a), name(b)), t, [x for x in ["ionic", "covalent", "metallic", "hydrogen bond"] if x != t],
                {"ionic": "A metal gives electrons to a nonmetal.", "covalent": "Two nonmetals share electrons.", "metallic": "Metal atoms share a sea of electrons."}[t])


def g_formula():
    m, x = R.choice(METALS), R.choice(NONMET)
    f, nm, nx = formula(m, x)
    nme = "%s %s" % (BY[m][1], ANION[x])
    k = R.choice(["f", "f2"])
    if not once(("fm", m, x)):
        return None
    a, b = ion_charge(BY[m]), -ion_charge(BY[x])
    w = [fstr(m, a, x, b), fstr(m, 1, x, 1), fstr(m, nx, x, nm), fstr(m, b, x, a), fstr(m, 2 * nm, x, 2 * nx)]
    w = [sub(z) for z in dict.fromkeys(w) if z != f]
    if len(w) < 3:
        return None
    w = R.sample(w, 3)
    cm, cx = BY[m][0], BY[x][0]
    if k == "f":
        return item("What is the formula of %s?" % nme, sub(f), w, "%s forms %s and %s forms %s<sup>%s</sup>; the charges must add to zero." % (
            BY[m][1].capitalize(), "%s<sup>%s</sup>" % (cm, ("%d+" % a) if a > 1 else "+"), BY[x][1], cx, ("%d−" % b) if b > 1 else "−"))
    return item("%s<sup>%s</sup> and %s<sup>%s</sup> ions combine. What is the formula of the compound?" % (cm, ("%d+" % a) if a > 1 else "+", cx, ("%d−" % b) if b > 1 else "−"), sub(f), w,
                "Use the lowest numbers that make the total charge zero: %d × (+%d) + %d × (−%d) = 0." % (nm, a, nx, b))


def g_name():
    m, x = R.choice(METALS), R.choice(NONMET)
    f, nm, nx = formula(m, x)
    if not once(("nm", m, x)):
        return None
    good = "%s %s" % (BY[m][1], ANION[x])
    pre = {2: "di", 3: "tri"}
    w = ["%s %s" % (BY[m][1], BY[x][1]), "%s %s" % (BY[x][1], BY[m][1]), "%s %s%s" % (BY[m][1], pre.get(nx, "mono"), ANION[x])]
    return item("What is the name of %s?" % sub(f), good, w, "Name the metal, then the nonmetal with -ide. Ionic names do not use prefixes.")


HYD = {"C": ("CH4", 4, 0), "N": ("NH3", 3, 1), "O": ("H2O", 2, 2), "F": ("HF", 1, 3), "Si": ("SiH4", 4, 0), "P": ("PH3", 3, 1), "S": ("H2S", 2, 2), "Cl": ("HCl", 1, 3)}


def g_cov():
    k = R.choice(["hyd", "bonds", "lone", "share"])
    x = R.choice(list(HYD))
    f, nb, lp = HYD[x]
    if k == "share":
        t = R.choice([("single", 2), ("double", 4), ("triple", 6)])
        if not once(("sh", t[0])):
            return None
        return item("How many electrons are shared in a %s covalent bond?" % t[0], str(t[1]), [str(v) for v in (1, 2, 3, 4, 6, 8) if v != t[1]][:3], "Each bond is one shared pair (2 electrons).")
    if not once(("cv", x, k)):
        return None
    e = BY[x]
    if k == "hyd":
        ws = [sub(x + "H" + (str(n) if n > 1 else "")) for n in (1, 2, 3, 4, 5) if n != nb]
        return item("%s has %d valence electrons. What is the formula of the simplest compound it forms with hydrogen?" % (name(e)[0].upper() + name(e)[1:], 8 - nb), sub(f), R.sample(ws, 3),
                    "It shares %d electrons to fill its shell, so it bonds to %d hydrogen atoms." % (nb, nb))
    if k == "bonds":
        return item("How many covalent bonds does %s usually form?" % name(e), str(nb), [str(v) for v in (1, 2, 3, 4, 5, 6) if v != nb and v != 8 - nb][:3],
                    "It needs %d more electrons for a full outer shell." % nb)
    return item("How many lone pairs are on the central atom in %s?" % sub(f), str(lp), [str(v) for v in (0, 1, 2, 3, 4) if v != lp][:3],
                "%s has %d valence electrons; %d are used in bonds, leaving %d pairs." % (e[1].capitalize(), 8 - nb, nb, lp))


def g_polar():
    a, b = R.sample([x for x in EN], 2)
    d = round(abs(EN[a] - EN[b]), 2)
    ka, kb = BY[a][7], BY[b][7]
    if "metal" in (ka, kb) and (ka == kb or d <= 1.7 or "H" in (a, b)):
        return None
    if any(abs(d - c) < 0.08 for c in (0.4, 1.7)):
        return None
    if "metal" not in (ka, kb) and d > 1.7:
        return None
    t = "nonpolar covalent" if d < 0.4 else "polar covalent" if d <= 1.7 else "ionic"
    k = R.random() < 0.7
    if not once(("pl", tuple(sorted((a, b))), k)):
        return None
    ea, eb = BY[a], BY[b]
    if k:
        return item("Electronegativity: %s = %.2f and %s = %.2f. What type of bond forms between them?" % (name(ea), EN[a], name(eb), EN[b]), t,
                    [x for x in ["nonpolar covalent", "polar covalent", "ionic", "metallic"] if x != t],
                    "Difference = %.2f. Below 0.4: nonpolar; 0.4–1.7: polar covalent; above 1.7: ionic." % d)
    if d < 0.4:
        return None
    neg = ea if EN[a] > EN[b] else eb
    pos = eb if neg is ea else ea
    return item("In a bond between %s and %s (electronegativities %.2f and %.2f), which atom gets a partial negative charge?" % (name(ea), name(eb), EN[a], EN[b]), name(neg),
                [name(pos), "Neither; the electrons are shared equally.", "Both atoms."], "The more electronegative atom pulls the shared electrons closer.")


B1 = bank([
    ("Why do atoms form bonds?", "to reach a more stable, full outer shell", ["to gain protons", "to become larger", "to lose neutrons"], "Usually 8 valence electrons (octet)."),
    ("What happens in an ionic bond?", "One atom transfers electrons to another, and opposite ions attract.", ["Atoms share electrons equally.", "Protons move between atoms.", "Neutrons are shared."], "Metal + nonmetal."),
    ("What happens in a covalent bond?", "Two atoms share a pair of electrons.", ["One atom gives away all its electrons.", "Protons are shared.", "Ions attract."], "Nonmetal + nonmetal."),
    ("What is the octet rule?", "Atoms tend to gain, lose or share electrons to have 8 in their outer shell.", ["Atoms always have 8 protons.", "Every atom has 8 shells.", "Molecules have 8 atoms."], "Hydrogen and helium need 2."),
    ("What holds a metal together?", "positive ions in a sea of moving electrons", ["shared pairs between two atoms", "neutrons", "hydrogen bonds"], "Metallic bonding."),
    ("Which pair would form an ionic compound?", "potassium and bromine", ["carbon and oxygen", "nitrogen and hydrogen", "copper and zinc"], "Metal + nonmetal."),
    ("What is a molecule?", "a group of atoms held together by covalent bonds", ["a single ion", "a metal crystal", "a charged atom"], "H₂O, CO₂."),
    ("Why is the formula NaCl and not NaCl₂?", "Na⁺ and Cl⁻ charges cancel in a 1 : 1 ratio.", ["Sodium has 2 electrons to give.", "Chlorine is bigger.", "Formulas are always 1 : 1."], "Total charge = 0."),
])
B5 = bank([
    ("Salt melts at 801 °C but sugar melts at 186 °C. Which explains the difference?", "Salt is ionic with strong attractions between ions; sugar is made of covalent molecules.",
     ["Sugar is a metal.", "Salt has weaker bonds.", "They have the same bonds."], "Ionic solids have high melting points."),
    ("Why does salt water conduct electricity but sugar water does not?", "Dissolved salt makes free-moving ions.", ["Sugar has more electrons.", "Water is a metal.", "Sugar makes ions."], "Ions carry charge."),
    ("Why can copper be drawn into wires?", "Metal ions can slide past each other in the sea of electrons.", ["Copper is ionic.", "Copper is brittle.", "Copper is a gas."], "Malleable and ductile."),
    ("A solid is hard, brittle and dissolves in water to conduct electricity. What type is it most likely?", "ionic", ["metallic", "nonpolar covalent", "a noble gas"], "Ionic properties."),
    ("Why does a water molecule have a partial negative end?", "Oxygen is more electronegative and pulls the shared electrons.", ["Hydrogen is more electronegative.", "Water is ionic.", "The electrons are shared equally."], "Polar bonds."),
])


def body():
    think = ("<p><b>Atoms bond to fill their outer shells.</b></p>"
             "<ul><li>Metal + nonmetal: electrons move, ions form, <b>ionic</b> bond. Charges must add to zero (Mg<sup>2+</sup> + 2 Cl<sup>−</sup> → MgCl<sub>2</sub>).</li>"
             "<li>Nonmetal + nonmetal: electrons are shared, <b>covalent</b> bond. Each shared pair is one bond.</li>"
             "<li>Electronegativity difference: under 0.4 nonpolar, 0.4–1.7 polar covalent, over 1.7 ionic.</li></ul>")
    ex = [("Formula of aluminum oxide?", ["Al<sup>3+</sup> and O<sup>2−</sup>", "2 × (+3) + 3 × (−2) = 0"], "Al<sub>2</sub>O<sub>3</sub>"),
          ("Bond between H (2.20) and Cl (3.16)?", ["Difference 0.96"], "polar covalent")]
    mist = ["Writing MgCl instead of MgCl<sub>2</sub> (charges do not balance).", "Using prefixes like “di” in ionic names.", "Saying two nonmetals form an ionic bond."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why atoms bond", B1 + [(g_btype, 8), (g_cov, 4)]),
        ("Ionic formulas", [(g_formula, 12), (g_name, 8)]),
        ("Covalent molecules", [(g_cov, 12), (g_btype, 4), (g_name, 4)]),
        ("Polar and nonpolar bonds", [(g_polar, 14), (g_formula, 6)]),
        ("Bonds and properties", B5 + [(g_polar, 5), (g_formula, 5), (g_btype, 5)]),
    ])
    make("chemistry", "chemical-bonding", 3, "HS-PS1-1, HS-PS1-2",
         "Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons in the outermost energy level of atoms. "
         "Construct and revise an explanation for the outcome of a simple chemical reaction based on the outermost electron states of atoms, trends in the periodic table, and knowledge of the patterns of chemical properties.",
         "Chemical Bonding",
         "Chemical Bonding Worksheets: Ionic, Covalent and Polar Bonds (High School Chemistry)",
         "Chemical Bonding",
         "Free high school chemistry worksheets on chemical bonding (NGSS HS-PS1-1, HS-PS1-2): ionic and covalent bonds, ionic formulas and names, Lewis structures and bond polarity. 100 questions with answers.",
         "Atoms bond to fill outer shells.",
         "Metals give electrons to nonmetals (ionic); nonmetals share them (covalent).",
         body(),
         [("How do you tell if a bond is ionic or covalent?", "A metal with a nonmetal usually forms an ionic bond. Two nonmetals form a covalent bond. You can also use the electronegativity difference."),
          ("How do you write an ionic formula?", "Find each ion's charge and use the smallest numbers of each ion that make the total charge zero."),
          ("What makes a bond polar?", "The two atoms have different electronegativities, so the shared electrons are pulled toward one atom.")],
         sets)


if __name__ == "__main__":
    main()
