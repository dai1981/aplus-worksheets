# -*- coding: utf-8 -*-
"""Class 11 Chemistry (NCERT Chemistry Part I and II, 9 chapters): question makers and UNITS()."""
import math
import re
from in_sci import _R
from in_srs import ch, A, N, B, SU, pairs, tq, nf, al_chem as C, al_phys as P

CH = "Chemistry"
SUBS = [("mol⁻² dm⁶", "mol⁻² L²"), ("mol² dm⁻⁶", "mol² L⁻²"), ("dm⁻³", "L⁻¹"), ("dm³", "L"), ("cm³", "mL"), ("(L = ", "(N<sub>A</sub> = "),
        ("relative formula mass", "molar mass (in g mol⁻¹)"), ("Relative formula mass", "Molar mass"), ("M<sub>r</sub> = ", "molar mass = "), ("and Mr = ", "and molar mass ")]


def ri(a, b, step=1):
    return _R[0].randrange(a, b + 1, step)


def rf(a, b, step):
    return round(_R[0].randint(round(a / step), round(b / step)) * step, 6)


def fm(s):
    """C2H6 -> C<sub>2</sub>H<sub>6</sub>"""
    return re.sub(r"(?<=[A-Za-z\)])(\d+)", r"<sub>\1</sub>", s)


def T(f, *kinds):
    """al_chem maker with NCERT units (L, mL, mol L⁻¹, molar mass)"""
    g0 = A(f, *kinds)

    def g():
        it = g0()
        if not it:
            return None
        for k in ("q", "e"):
            for a, b in SUBS:
                it[k] = it[k].replace(a, b)
        it["c"] = [_sub(c) for c in it["c"]]
        return it
    g.__name__ = g0.__name__
    return g


def _sub(s):
    for a, b in SUBS:
        s = s.replace(a, b)
    return s


# =================================================================== 1 some basic concepts
SOLUTE = [("NaOH", 40), ("NaCl", 58.5), ("glucose (C₆H₁₂O₆)", 180), ("urea (NH₂CONH₂)", 60), ("KCl", 74.5), ("Na₂CO₃", 106), ("H₂SO₄", 98), ("KOH", 56), ("CaCl₂", 111), ("sucrose (C₁₂H₂₂O₁₁)", 342)]


def b_conc(k=None):
    k = k or ch(["M", "m", "x", "pct", "mass", "dil"])
    nm, M = ch(SOLUTE)
    if k == "M":
        w, V = rf(1, 40, 0.5), ch([100, 200, 250, 500, 1000])
        n = w / M
        return N("%s g of %s is dissolved in water to make %d mL of solution. What is the molarity? (molar mass %s g mol⁻¹)" % (nf(w), nm, V, nf(M)), n / (V / 1000),
                 [n / V, w / (V / 1000), n * V / 1000], " mol L⁻¹", "Moles = %s ÷ %s = %s mol; M = moles ÷ volume in L = %s ÷ %s = <b>%s mol L⁻¹</b>." % (nf(w), nf(M), nf(n), nf(n), nf(V / 1000), nf(n / (V / 1000))))
    if k == "m":
        w, W = rf(1, 30, 0.5), ch([100, 200, 250, 400, 500])
        n = w / M
        return N("%s g of %s is dissolved in %d g of water. What is the molality of the solution? (molar mass %s g mol⁻¹)" % (nf(w), nm, W, nf(M)), n / (W / 1000),
                 [n / W, n / ((W + w) / 1000), w / (W / 1000)], " mol kg⁻¹", "Molality = moles of solute ÷ mass of solvent in kg = %s ÷ %s = <b>%s mol kg⁻¹</b>." % (nf(n), nf(W / 1000), nf(n / (W / 1000))))
    if k == "x":
        a, b = rf(0.5, 5, 0.5), rf(1, 10, 0.5)
        return N("A solution contains %s mol of ethanol and %s mol of water. What is the mole fraction of ethanol?" % (nf(a), nf(b)), a / (a + b), [a / b, b / (a + b), a / (a + b) * 100], "",
                 "x = n(ethanol) ÷ (total moles) = %s ÷ %s = <b>%s</b>." % (nf(a), nf(a + b), nf(a / (a + b))))
    if k == "pct":
        w, W = ri(2, 40), ri(60, 400, 10)
        return N("%d g of %s is dissolved in %d g of water. What is the mass percentage of the solute?" % (w, nm, W), w / (w + W) * 100, [w / W * 100, W / (w + W) * 100, w / (w + W)], "%",
                 "Mass %% = mass of solute ÷ mass of solution × 100 = %d ÷ %d × 100 = <b>%s%%</b>." % (w, w + W, nf(w / (w + W) * 100)))
    if k == "mass":
        Mv, V = rf(0.1, 2, 0.1), ch([100, 250, 500, 1000])
        return N("What mass of %s is needed to make %d mL of a %s mol L⁻¹ solution? (molar mass %s g mol⁻¹)" % (nm, V, nf(Mv), nf(M)), Mv * V / 1000 * M, [Mv * V * M, Mv * M, Mv * V / 1000], " g",
                 "Moles = M × V = %s × %s = %s mol; mass = moles × molar mass = <b>%s g</b>." % (nf(Mv), nf(V / 1000), nf(Mv * V / 1000), nf(Mv * V / 1000 * M)))
    M1, V2 = ch([1, 2, 5, 0.5, 10]), ch([100, 250, 500, 1000])
    M2 = ch([0.1, 0.2, 0.25, 0.05])
    if M2 >= M1:
        return None
    return N("What volume of a %s M stock solution is needed to make %d mL of a %s M solution?" % (nf(M1), V2, nf(M2)), M2 * V2 / M1, [M1 * V2 / M2, M1 * M2 * V2, V2 - M2 * V2 / M1], " mL",
             "M₁V₁ = M₂V₂, so V₁ = %s × %d ÷ %s = <b>%s mL</b>." % (nf(M2), V2, nf(M1), nf(M2 * V2 / M1)))


LIMIT = [("2H₂ + O₂ → 2H₂O", "H₂", 2, 2, "O₂", 32, 1, "H₂O", 18, 2), ("N₂ + 3H₂ → 2NH₃", "N₂", 28, 1, "H₂", 2, 3, "NH₃", 17, 2),
         ("C + O₂ → CO₂", "C", 12, 1, "O₂", 32, 1, "CO₂", 44, 1), ("2Mg + O₂ → 2MgO", "Mg", 24, 2, "O₂", 32, 1, "MgO", 40, 2),
         ("CH₄ + 2O₂ → CO₂ + 2H₂O", "CH₄", 16, 1, "O₂", 32, 2, "CO₂", 44, 1), ("Zn + 2HCl → ZnCl₂ + H₂", "Zn", 65, 1, "HCl", 36.5, 2, "H₂", 2, 1)]


def b_limit(k=None):
    eq, a, Ma, ca, b, Mb, cb, p, Mp, cp = ch(LIMIT)
    na, nb = rf(0.5, 6, 0.5), rf(0.5, 6, 0.5)
    if abs(na / ca - nb / cb) < 1e-9:
        return None
    lim, other = (a, b) if na / ca < nb / cb else (b, a)
    if (k or ch(["which", "mass"])) == "which":
        return tq("For %s, %s mol of %s reacts with %s mol of %s. Which is the limiting reagent?" % (eq, nf(na), a, nf(nb), b), lim, [other, p, "neither; both are used up"],
                  "Divide moles by the coefficients: %s ÷ %d = %s and %s ÷ %d = %s. The smaller one, <b>%s</b>, runs out first." % (nf(na), ca, nf(na / ca), nf(nb), cb, nf(nb / cb), lim))
    ext = min(na / ca, nb / cb)
    m = ext * cp * Mp
    return N("For %s, %s mol of %s reacts with %s mol of %s. What mass of %s forms? (molar mass of %s = %s g mol⁻¹)" % (eq, nf(na), a, nf(nb), b, p, p, nf(Mp)), m,
             [max(na / ca, nb / cb) * cp * Mp, ext * Mp, (na + nb) * Mp], " g", "The limiting reagent decides the amount: %s × %d mol × %s g mol⁻¹ = <b>%s g</b>." % (nf(ext), cp, nf(Mp), nf(m)))


B1 = [("Which law says a compound always contains the same elements in the same proportion by mass?", "the law of definite proportions", ["the law of multiple proportions", "the law of conservation of mass", "Avogadro's law"], "Proust's law."),
      ("Which law is shown by H₂O and H₂O₂, where the masses of oxygen combining with the same mass of hydrogen are in the ratio 1 : 2?", "the law of multiple proportions", ["the law of definite proportions", "Gay-Lussac's law", "the law of conservation of mass"], "Dalton's law of multiple proportions."),
      ("Who stated the law of conservation of mass?", "Antoine Lavoisier", ["John Dalton", "Joseph Proust", "Amedeo Avogadro"], "Matter is neither created nor destroyed in a reaction."),
      ("Which law says gases react in simple whole-number ratios by volume?", "Gay-Lussac's law of gaseous volumes", ["Boyle's law", "the law of multiple proportions", "Dalton's law"], "2 volumes of H₂ + 1 volume of O₂ → 2 volumes of steam."),
      ("Equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules. Whose law is this?", "Avogadro's", ["Dalton's", "Lavoisier's", "Proust's"], "Avogadro's law."),
      ("What is one atomic mass unit (u)?", "one-twelfth of the mass of a carbon-12 atom", ["the mass of a hydrogen atom", "the mass of a proton exactly", "one gram"], "1 u = 1.66 × 10⁻²⁴ g."),
      ("Which quantity changes with temperature: molarity or molality?", "molarity", ["molality", "both", "neither"], "Volume changes with temperature; mass does not."),
      ("What is the SI unit of the amount of substance?", "the mole", ["the gram", "the litre", "the kilogram"], "1 mol = 6.022 × 10²³ particles."),
      ("What is the number of particles in one mole called?", "Avogadro's number", ["the gas constant", "the atomic number", "the mass number"], "N<sub>A</sub> = 6.022 × 10²³ mol⁻¹."),
      ("Which is a homogeneous mixture?", "sugar dissolved in water", ["sand and water", "oil and water", "iron filings and sulphur"], "Its composition is the same throughout."),
      ("What does the empirical formula show?", "the simplest whole-number ratio of atoms", ["the actual number of atoms", "the shape of the molecule", "the molar mass"], "The molecular formula is a whole-number multiple of it."),
      ("Which reactant is called the limiting reagent?", "the one that is used up first", ["the one in excess", "the catalyst", "the product"], "It decides how much product forms."),
      ("What is the molar mass of water?", "18 g mol⁻¹", ["16 g mol⁻¹", "10 g mol⁻¹", "20 g mol⁻¹"], "2 × 1 + 16."),
      ("Which is the correct number of significant figures in 0.0025?", "2", ["4", "5", "3"], "Leading zeros do not count."),
      ("What is a pure substance?", "a substance with a fixed composition, an element or a compound", ["any mixture", "only an element", "a solution"], "Its properties are the same throughout."),
      ("Which statement about a mole of oxygen gas (O₂) is correct?", "it contains 6.022 × 10²³ molecules", ["it contains 6.022 × 10²³ atoms", "it has a mass of 16 g", "it fills 1 L at STP"], "Each molecule has two atoms, so 2 × N<sub>A</sub> atoms.")]


# =================================================================== 2 structure of atom
SUB = "spdf"


def b_qn(k=None):
    k = k or ch(["name", "orbs", "shell", "shello", "ml", "valid"])
    n = ri(1, 6)
    l = ri(0, min(n - 1, 3))
    if k == "name":
        return tq("Which orbital has n = %d and l = %d?" % (n, l), "%d%s" % (n, SUB[l]),
                  ["%d%s" % (n, SUB[(l + 1) % 4]), "%d%s" % (n + 1, SUB[l]), "%d%s" % (l, SUB[min(n - 1, 3)])], "l = 0, 1, 2, 3 are s, p, d, f, so the orbital is <b>%d%s</b>." % (n, SUB[l]))
    if k == "orbs":
        return N("How many orbitals are there in a %d%s subshell?" % (n, SUB[l]), 2 * l + 1, [2 * (2 * l + 1), l + 1, n * n], "", "There are 2l + 1 values of m<sub>l</sub>: <b>%d</b>." % (2 * l + 1)) if l else None
    if k == "shell":
        return N("What is the greatest number of electrons in the shell with n = %d?" % n, 2 * n * n, [n * n, 2 * n, 8], "", "Maximum electrons = 2n² = <b>%d</b>." % (2 * n * n)) if n > 1 else None
    if k == "shello":
        return N("How many orbitals are there altogether in the shell with n = %d?" % n, n * n, [2 * n * n, n, 2 * n], "", "Number of orbitals = n² = <b>%d</b>." % (n * n)) if n > 1 else None
    if k == "ml":
        return tq("What are the allowed values of m<sub>l</sub> for a %d%s electron?" % (n, SUB[l]), ", ".join(str(x).replace("-", "−") for x in range(-l, l + 1)),
                  ["0 to %d" % (2 * l + 1), ", ".join(str(x) for x in range(0, l + 2)), "1 to %d" % n], "m<sub>l</sub> runs from −l to +l.") if l else None
    return None


SERIES = {1: "Lyman", 2: "Balmer", 3: "Paschen", 4: "Brackett", 5: "Pfund"}


def b_bohr(k=None):
    k = k or ch(["En", "dE", "lam", "r", "series", "Z"])
    n1 = ri(1, 3)
    n2 = ri(n1 + 1, 6)
    if k == "En":
        n = ri(1, 6)
        return N("What is the energy of the electron in the n = %d orbit of a hydrogen atom? (E<sub>n</sub> = −13.6/n² eV)" % n, -13.6 / n / n, [-13.6 / n, 13.6 / n / n, -13.6 * n * n], " eV",
                 "E = −13.6 ÷ %d = <b>%s eV</b>." % (n * n, nf(-13.6 / n / n)))
    if k == "dE":
        d = 13.6 * (1 / n1 ** 2 - 1 / n2 ** 2)
        return N("How much energy is given out when the electron in a hydrogen atom falls from n = %d to n = %d?" % (n2, n1), d, [13.6 / n1 ** 2, 13.6 * (1 / n1 - 1 / n2), 13.6 / n2 ** 2], " eV",
                 "ΔE = 13.6(1/%d² − 1/%d²) = <b>%s eV</b>." % (n1, n2, nf(d)))
    if k == "lam":
        lam = 1 / (1.097e7 * (1 / n1 ** 2 - 1 / n2 ** 2)) * 1e9
        return N("What is the wavelength of light given out when the electron in a hydrogen atom falls from n = %d to n = %d? (R<sub>H</sub> = 1.097 × 10⁷ m⁻¹)" % (n2, n1), lam,
                 [1 / (1.097e7 * (1 / n1 - 1 / n2)) * 1e9, lam / 2, 1 / (1.097e7 / n1 ** 2) * 1e9], " nm", "1/λ = R(1/n₁² − 1/n₂²), λ = <b>%s nm</b>." % nf(lam))
    if k == "r":
        n = ri(1, 5)
        Z = ch([1, 1, 2, 3])
        ion = {1: "a hydrogen atom", 2: "He⁺", 3: "Li²⁺"}[Z]
        return N("What is the radius of the n = %d orbit in %s? (r = 52.9 n²/Z pm)" % (n, ion), 52.9 * n * n / Z, [52.9 * n / Z, 52.9 * n * n * Z, 52.9 * n * n], " pm", "r = 52.9 × %d ÷ %d = <b>%s pm</b>." % (n * n, Z, nf(52.9 * n * n / Z)))
    if k == "series":
        n1 = ri(1, 5)
        n2 = ri(n1 + 1, 7)
        return tq("An electron in a hydrogen atom falls from n = %d to n = %d. Which spectral series does the line belong to?" % (n2, n1), SERIES[n1], [v for kk, v in SERIES.items() if kk != n1],
                  "The series is named after the lower level: n = %d is the <b>%s</b> series." % (n1, SERIES[n1]))
    Z, nm = ch([(2, "He⁺"), (3, "Li²⁺")])
    n = ri(1, 3)
    return N("What is the energy of the electron in the n = %d orbit of %s? (E<sub>n</sub> = −13.6 Z²/n² eV)" % (n, nm), -13.6 * Z * Z / n / n, [-13.6 * Z / n / n, -13.6 / n / n, -13.6 * Z * Z / n], " eV",
             "E = −13.6 × %d ÷ %d = <b>%s eV</b>." % (Z * Z, n * n, nf(-13.6 * Z * Z / n / n)))


B2 = [("Who discovered the electron, using cathode rays?", "J. J. Thomson", ["Ernest Rutherford", "James Chadwick", "Niels Bohr"], "He measured its charge-to-mass ratio."),
      ("Who discovered the neutron?", "James Chadwick", ["J. J. Thomson", "Ernest Rutherford", "Eugen Goldstein"], "In 1932."),
      ("What did Rutherford's α-particle scattering experiment show?", "an atom has a tiny, dense, positive nucleus", ["electrons are in fixed orbits", "the atom is a uniform positive sphere", "neutrons exist"], "Most α-particles passed straight through."),
      ("Which principle says no two electrons in an atom can have the same four quantum numbers?", "the Pauli exclusion principle", ["Hund's rule", "the Aufbau principle", "Heisenberg's uncertainty principle"], "An orbital holds at most two electrons with opposite spins."),
      ("Which rule says electrons occupy degenerate orbitals singly before pairing?", "Hund's rule of maximum multiplicity", ["the Pauli exclusion principle", "the Aufbau principle", "the (n + l) rule only"], "Unpaired spins are parallel."),
      ("In the Aufbau principle, which orbital fills first?", "the one with the lower (n + l) value", ["the one with the larger n", "the d orbital always", "the one with the larger l"], "If n + l is equal, the lower n fills first."),
      ("Which orbital fills before 3d?", "4s", ["4p", "4d", "5s"], "4s has n + l = 4; 3d has 5."),
      ("What does the Heisenberg uncertainty principle say?", "the exact position and momentum of an electron cannot both be known", ["electrons have no mass", "energy is quantised", "an orbital holds two electrons"], "Δx × Δp ≥ h/4π."),
      ("Why is Bohr's model not suitable for atoms with many electrons?", "it cannot explain their spectra or electron–electron effects", ["it predicts no spectra", "it has no nucleus", "it is only for metals"], "It works only for hydrogen-like species."),
      ("Which quantum number gives the shape of an orbital?", "the azimuthal quantum number l", ["the principal quantum number n", "the magnetic quantum number m<sub>l</sub>", "the spin quantum number"], "l = 0 is spherical (s), l = 1 dumb-bell (p)."),
      ("Which quantum number gives the orientation of an orbital in space?", "the magnetic quantum number m<sub>l</sub>", ["the principal quantum number n", "the azimuthal quantum number l", "the spin quantum number"], "There are 2l + 1 orientations."),
      ("What are isotopes?", "atoms of an element with the same atomic number but different mass numbers", ["atoms with the same mass number", "different elements", "ions of an element"], "e.g. ¹H, ²H and ³H."),
      ("What are isobars?", "atoms of different elements with the same mass number", ["atoms with the same atomic number", "atoms with the same neutrons", "ions"], "e.g. ⁴⁰Ar and ⁴⁰Ca."),
      ("Why is the configuration of chromium 3d⁵ 4s¹, not 3d⁴ 4s²?", "half-filled d orbitals are extra stable", ["4s is higher than 4p", "chromium has 25 electrons", "d orbitals cannot hold 4 electrons"], "Copper is 3d¹⁰ 4s¹ for the same reason (filled d)."),
      ("What is the photoelectric effect?", "electrons are ejected from a metal when light of high enough frequency falls on it", ["light bends round a corner", "metals glow when heated", "atoms split"], "It showed that light comes in photons."),
      ("What does the de Broglie relation say?", "a moving particle has a wavelength λ = h/mv", ["light has mass", "energy equals mc²", "electrons have no wavelength"], "This dual nature is important for electrons.")]


# =================================================================== 3 classification of elements
SYM = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe "
       "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn").split()


def pos(Z):
    for p, (a, b) in enumerate([(1, 2), (3, 10), (11, 18), (19, 36), (37, 54), (55, 86)], 1):
        if a <= Z <= b:
            i = Z - a + 1
            if p == 1:
                grp = 1 if Z == 1 else 18
            elif p <= 3:
                grp = i if i <= 2 else i + 10
            elif p <= 5:
                grp = i
            else:
                if 57 <= Z <= 71:
                    return p, None, "f"
                grp = i if Z <= 56 else Z - 68
            blk = "s" if grp <= 2 or Z == 2 else ("d" if grp <= 12 else "p")
            return p, grp, blk


def b_table(k=None):
    k = k or ch(["period", "group", "block"])
    Z = ri(1, 86)
    p, grp, blk = pos(Z)
    if grp is None:
        return None
    el = "%s (Z = %d)" % (SYM[Z - 1], Z)
    if k == "period":
        return N("In which period of the periodic table is %s?" % el, p, [p + 1, p - 1 if p > 1 else p + 2, grp if grp != p else p + 3], "", "The highest shell used is n = %d, so it is in period <b>%d</b>." % (p, p))
    if k == "group":
        return N("In which group of the periodic table is %s?" % el, grp, [grp + 1 if grp < 18 else 17, grp - 1 if grp > 1 else 3, p if p != grp else grp + 2], "",
                 "%s is in group <b>%d</b> (the %s-block)." % (SYM[Z - 1], grp, blk))
    return tq("To which block of the periodic table does %s belong?" % el, "%s-block" % blk, ["%s-block" % x for x in "spdf" if x != blk],
              "The last electron enters a%s %s orbital, so it is a <b>%s-block</b> element." % ("n" if blk == "s" else "", blk, blk))


ROOT = ["nil", "un", "bi", "tri", "quad", "pent", "hex", "sept", "oct", "enn"]


def iupac(Z):
    d = [int(x) for x in str(Z)]
    name = "".join(ROOT[x] for x in d) + "ium"
    name = name.replace("biium", "bium").replace("triium", "trium").replace("ennnil", "ennil")
    sym = "".join(ROOT[x][0] for x in d)
    return name, sym[0].upper() + sym[1:]


def b_iupac(k=None):
    Z = ri(101, 130)
    name, sym = iupac(Z)
    if (k or ch(["name", "sym"])) == "name":
        w = [iupac(Z + d)[0] for d in (1, -1, 10)]
        return tq("What is the IUPAC temporary name of the element with atomic number %d?" % Z, name, w, "Each digit has a root (0 nil, 1 un, 2 bi, …) and the name ends in -ium: <b>%s</b>." % name)
    return tq("What is the IUPAC temporary symbol of the element with atomic number %d?" % Z, sym, [iupac(Z + d)[1] for d in (1, -1, 10)], "Take the first letter of each root: <b>%s</b>." % sym)


TREND = [("Which has the larger atomic radius, Na or Mg?", "Na", ["Mg", "both are equal", "it cannot be said"], "Radius decreases across a period as nuclear charge rises."),
         ("Which has the larger atomic radius, Li or K?", "K", ["Li", "both are equal", "it cannot be said"], "Radius increases down a group as shells are added."),
         ("Which is larger, Na or Na⁺?", "Na", ["Na⁺", "both are equal", "it cannot be said"], "A cation is smaller than its atom."),
         ("Which is larger, Cl or Cl⁻?", "Cl⁻", ["Cl", "both are equal", "it cannot be said"], "An anion is larger than its atom."),
         ("Which has the higher first ionisation enthalpy, N or O?", "N", ["O", "both are equal", "it cannot be said"], "N has a stable half-filled 2p³ configuration."),
         ("Which has the higher first ionisation enthalpy, Be or B?", "Be", ["B", "both are equal", "it cannot be said"], "B's 2p electron is easier to remove than Be's 2s electron."),
         ("Which has the higher first ionisation enthalpy, Na or Cl?", "Cl", ["Na", "both are equal", "it cannot be said"], "Ionisation enthalpy rises across a period."),
         ("Which element has the highest electronegativity?", "fluorine", ["oxygen", "chlorine", "caesium"], "F is 4.0 on the Pauling scale."),
         ("Which has the more negative electron gain enthalpy, F or Cl?", "Cl", ["F", "both are equal", "it cannot be said"], "F is so small that added electrons repel strongly."),
         ("Which has the higher first ionisation enthalpy, Mg or Al?", "Mg", ["Al", "both are equal", "it cannot be said"], "Mg has a filled 3s²; Al's 3p electron is easier to remove."),
         ("Which is the largest ion: Na⁺, Mg²⁺, Al³⁺ or F⁻?", "F⁻", ["Na⁺", "Mg²⁺", "Al³⁺"], "These are isoelectronic; the one with the fewest protons is largest."),
         ("How does metallic character change across a period from left to right?", "it decreases", ["it increases", "it stays the same", "it first rises then falls"], "Elements become non-metals."),
         ("What is the oxide of sodium like?", "basic", ["acidic", "neutral", "amphoteric"], "Na₂O + H₂O → 2NaOH."),
         ("What is aluminium oxide like?", "amphoteric", ["only acidic", "only basic", "neutral"], "It reacts with both acids and bases."),
         ("What is the oxide of sulphur (SO₃) like?", "acidic", ["basic", "amphoteric", "neutral"], "It forms sulphuric acid with water."),
         ("Who arranged elements by atomic mass and left gaps for undiscovered elements?", "Dmitri Mendeleev", ["Henry Moseley", "Johann Döbereiner", "John Newlands"], "He predicted eka-aluminium (gallium)."),
         ("On what is the modern periodic law based?", "atomic number", ["atomic mass", "density", "valency"], "Moseley showed the importance of atomic number."),
         ("What are the elements of groups 1 and 2 called?", "s-block elements", ["p-block elements", "transition elements", "noble gases"], "Their last electron enters an s orbital."),
         ("What are the lanthanoids and actinoids?", "f-block (inner transition) elements", ["s-block metals", "noble gases", "halogens"], "Their last electron enters a 4f or 5f orbital."),
         ("Which group contains the noble gases?", "group 18", ["group 1", "group 17", "group 2"], "They have full outer shells.")]


# =================================================================== 4 bonding
MO = [("H₂", 2), ("H₂⁺", 1), ("He₂", 4), ("He₂⁺", 3), ("Li₂", 6), ("Be₂", 8), ("B₂", 10), ("C₂", 12), ("N₂", 14), ("N₂⁺", 13), ("O₂", 16), ("O₂⁺", 15), ("O₂⁻", 17), ("O₂²⁻", 18), ("F₂", 18), ("Ne₂", 20)]


def mo(nel):
    order = [(2, 1, "s"), (2, -1, "s"), (2, 1, "s"), (2, -1, "s")]
    order += [(4, 1, "pi"), (2, 1, "s")] if nel <= 14 else [(2, 1, "s"), (4, 1, "pi")]
    order += [(4, -1, "pi"), (2, -1, "s")]
    left, nb, na, un = nel, 0, 0, 0
    for cap, b, kind in order:
        e = min(cap, left)
        left -= e
        if b > 0:
            nb += e
        else:
            na += e
        un += (e % 2) if kind == "s" else (e if e <= 2 else 4 - e)
    return (nb - na) / 2, un


def fbo(x):
    return {0.5: "½", 1.5: "1½", 2.5: "2½"}.get(x, str(int(x)))


def b_mo(k=None):
    sp, n = ch(MO)
    bo, un = mo(n)
    if (k or ch(["bo", "mag"])) == "bo":
        return tq("Using molecular orbital theory, what is the bond order of %s?" % sp, fbo(bo), [fbo(x) for x in (bo + 0.5, bo - 0.5 if bo >= 0.5 else bo + 1, bo + 1 if bo + 1 != bo + 0.5 else 3)] + ["3"],
                  "Bond order = ½(N<sub>b</sub> − N<sub>a</sub>) for %d electrons = <b>%s</b>%s." % (n, fbo(bo), " (it does not exist as a stable molecule)" if bo == 0 else ""))
    if bo == 0:
        return None
    a = "paramagnetic (%d unpaired electron%s)" % (un, "" if un == 1 else "s") if un else "diamagnetic (no unpaired electrons)"
    w = ["diamagnetic (no unpaired electrons)", "paramagnetic (1 unpaired electron)", "paramagnetic (2 unpaired electrons)", "paramagnetic (3 unpaired electrons)"]
    return tq("Is %s paramagnetic or diamagnetic?" % sp, a, [x for x in w if x != a], "Fill the molecular orbitals with %d electrons: %s." % (n, a))


HYB = [("BeCl₂", "sp", "linear"), ("CO₂ (carbon)", "sp", "linear"), ("BF₃", "sp²", "trigonal planar"), ("C₂H₄ (each carbon)", "sp²", "trigonal planar"), ("CH₄", "sp³", "tetrahedral"),
       ("NH₃ (nitrogen)", "sp³", "trigonal pyramidal"), ("H₂O (oxygen)", "sp³", "bent (V-shaped)"), ("PCl₅", "sp³d", "trigonal bipyramidal"), ("SF₆", "sp³d²", "octahedral"),
       ("C₂H₂ (each carbon)", "sp", "linear"), ("CCl₄", "sp³", "tetrahedral"), ("SO₃ (sulphur)", "sp²", "trigonal planar")]


B4 = [("What is a covalent bond?", "a shared pair of electrons between two atoms", ["transfer of electrons", "attraction between ions only", "a bond in metals"], "Each atom gets a stable configuration."),
      ("Which molecule does NOT obey the octet rule?", "BF₃", ["CH₄", "NH₃", "H₂O"], "Boron has only six electrons in BF₃."),
      ("Which molecule has an expanded octet?", "PCl₅", ["CH₄", "NH₃", "CO₂"], "Phosphorus has ten electrons around it."),
      ("Which molecule has a zero dipole moment even though its bonds are polar?", "CO₂", ["H₂O", "NH₃", "HCl"], "It is linear, so the bond dipoles cancel."),
      ("Which has the larger dipole moment, NH₃ or NF₃?", "NH₃", ["NF₃", "both are equal", "both are zero"], "In NH₃ the lone pair dipole adds to the bond dipoles."),
      ("What is the order of repulsion in VSEPR theory?", "lone pair–lone pair > lone pair–bond pair > bond pair–bond pair", ["bond pair–bond pair > lone pair–lone pair", "all are equal", "lone pair–bond pair is the largest"], "So bond angles shrink when lone pairs are present."),
      ("Why is the bond angle in water (104.5°) less than in methane (109.5°)?", "two lone pairs on oxygen push the bonds closer", ["oxygen is larger", "water has double bonds", "methane has lone pairs"], "Lone pairs repel more strongly."),
      ("What is a sigma (σ) bond?", "a bond formed by head-on overlap of orbitals", ["a bond formed by sideways overlap", "an ionic bond", "a hydrogen bond"], "It is stronger than a π bond."),
      ("How many σ and π bonds are there in ethyne, C₂H₂?", "3 σ and 2 π", ["2 σ and 3 π", "5 σ and 0 π", "1 σ and 2 π"], "C≡C is one σ + two π; two C–H σ bonds."),
      ("How many σ and π bonds are there in ethene, C₂H₄?", "5 σ and 1 π", ["4 σ and 2 π", "6 σ and 0 π", "4 σ and 1 π"], "Four C–H, one C–C σ, and one π."),
      ("Which compound has intramolecular hydrogen bonding?", "o-nitrophenol", ["p-nitrophenol", "water", "ethanol"], "The –OH and –NO₂ are next to each other."),
      ("Why does ice float on water?", "hydrogen bonds give ice an open structure that is less dense", ["ice has air in it", "ice is lighter by mass", "water has no hydrogen bonds"], "Water is densest at 4 °C."),
      ("What is resonance?", "when one structure cannot describe a molecule and two or more contributing structures are needed", ["vibration of bonds", "magnetism", "ionic bonding"], "Ozone and benzene show resonance."),
      ("What is the formal charge on each oxygen in the O₃ structure O=O⁺–O⁻? (the ends)", "0 on the double-bonded end, −1 on the single-bonded end", ["0 on both", "+1 on both", "−1 on both"], "Formal charge = V − L − ½B."),
      ("Which is more covalent, NaCl or LiCl?", "LiCl", ["NaCl", "both are equal", "neither"], "Fajans' rules: the small Li⁺ polarises Cl⁻ more."),
      ("Which is more covalent, AlCl₃ or NaCl?", "AlCl₃", ["NaCl", "both are equal", "neither"], "Al³⁺ is small and highly charged.")]


# =================================================================== 5 thermodynamics
DNG = [("N₂(g) + 3H₂(g) → 2NH₃(g)", -2), ("CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)", -2), ("C(s) + O₂(g) → CO₂(g)", 0), ("2H₂(g) + O₂(g) → 2H₂O(l)", -3),
       ("CaCO₃(s) → CaO(s) + CO₂(g)", 1), ("PCl₅(g) → PCl₃(g) + Cl₂(g)", 1), ("N₂O₄(g) → 2NO₂(g)", 1), ("2SO₂(g) + O₂(g) → 2SO₃(g)", -1), ("H₂(g) + Cl₂(g) → 2HCl(g)", 0),
       ("C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l)", -1), ("NH₄Cl(s) → NH₃(g) + HCl(g)", 2)]


def b_thermo(k=None):
    k = k or ch(["dH", "dng", "w", "dU", "q"])
    if k in ("dH", "dng"):
        eq, dn = ch(DNG)
        if k == "dng":
            return N("What is Δn<sub>g</sub> (change in moles of gas) for %s?" % eq, dn, [-dn if dn else 1, dn + 1, dn - 1], "", "Δn<sub>g</sub> = moles of gaseous products − moles of gaseous reactants = <b>%s</b>." % nf(dn))
        dU = ri(-900, 200, 10)
        dH = dU + dn * 8.314e-3 * 298
        return N("For %s, ΔU = %s kJ mol⁻¹ at 298 K. What is ΔH? (R = 8.314 J K⁻¹ mol⁻¹)" % (eq, nf(dU)), dH, [dU - dn * 8.314e-3 * 298, dU + dn * 8.314 * 298 / 100, dU], " kJ mol⁻¹",
                 "ΔH = ΔU + Δn<sub>g</sub>RT = %s + (%s)(8.314 × 10⁻³)(298) = <b>%s kJ mol⁻¹</b>." % (nf(dU), nf(dn), nf(dH))) if dn else None
    if k == "w":
        p, V1 = ri(1, 5), ri(1, 10)
        V2 = V1 + ri(1, 10)
        return N("A gas expands from %d L to %d L against a constant external pressure of %d bar. What is the work done on the gas? (1 L bar = 100 J)" % (V1, V2, p), -p * (V2 - V1) * 100,
                 [p * (V2 - V1) * 100, -p * (V2 - V1), -p * V2 * 100], " J", "w = −p<sub>ext</sub>ΔV = −%d × %d L bar = <b>%s J</b> (negative: the gas does work)." % (p, V2 - V1, nf(-p * (V2 - V1) * 100)))
    q, w = ri(100, 900, 50), ri(50, 600, 50)
    s = ch([1, -1])
    if k == "dU":
        if s > 0:
            return N("A system absorbs %d J of heat while %d J of work is done on it. What is ΔU?" % (q, w), q + w, [q - w, -q - w, q], " J", "ΔU = q + w = %d + %d = <b>%d J</b>." % (q, w, q + w))
        return N("A system absorbs %d J of heat and does %d J of work on the surroundings. What is ΔU?" % (q, w), q - w, [q + w, w - q, q], " J",
                 "Work done by the system is negative: ΔU = q + w = %d + (−%d) = <b>%s J</b>." % (q, w, nf(q - w)))
    dU = ri(-500, 500, 50)
    return N("The internal energy of a system changes by %s J while %d J of work is done on it. How much heat did it absorb?" % (nf(dU), w), dU - w, [dU + w, w - dU, dU], " J",
             "q = ΔU − w = %s − %d = <b>%s J</b>." % (nf(dU), w, nf(dU - w))) if dU != w and dU else None


B5 = [("What is an isolated system?", "one that exchanges neither energy nor matter with its surroundings", ["one that exchanges only matter", "one that exchanges only energy", "an open beaker"], "A perfectly insulated thermos flask is close to it."),
      ("What is a closed system?", "one that exchanges energy but not matter", ["one that exchanges both", "one that exchanges neither", "one that exchanges only matter"], "A sealed metal container."),
      ("Which is an extensive property?", "enthalpy", ["temperature", "density", "pressure"], "It depends on the amount of matter."),
      ("Which is an intensive property?", "temperature", ["mass", "volume", "internal energy"], "It does not depend on the amount."),
      ("Which is a state function?", "internal energy", ["work", "heat", "path length"], "It depends only on the state, not the path."),
      ("In the chemistry sign convention, what is the sign of w when the system does work on the surroundings?", "negative", ["positive", "zero", "it has no sign"], "ΔU = q + w."),
      ("What is the standard enthalpy of formation of an element in its standard state?", "zero", ["always negative", "always positive", "equal to its bond enthalpy"], "e.g. ΔfH° of O₂(g) is 0."),
      ("What does Hess's law state?", "the enthalpy change of a reaction is the same whatever the route", ["enthalpy is always negative", "entropy always increases", "energy is created in reactions"], "It follows from enthalpy being a state function."),
      ("When is a reaction spontaneous at constant temperature and pressure?", "when ΔG is negative", ["when ΔH is positive", "when ΔS is negative", "when ΔG is positive"], "ΔG = ΔH − TΔS."),
      ("A reaction has ΔH < 0 and ΔS > 0. When is it spontaneous?", "at all temperatures", ["at no temperature", "only at high temperature", "only at low temperature"], "ΔG is always negative."),
      ("A reaction has ΔH > 0 and ΔS > 0. When is it spontaneous?", "at high temperature", ["at low temperature", "at all temperatures", "never"], "TΔS must be larger than ΔH."),
      ("What is the entropy of a perfectly crystalline substance at 0 K?", "zero", ["infinite", "negative", "equal to its enthalpy"], "The third law of thermodynamics."),
      ("What is the relation between ΔG° and the equilibrium constant?", "ΔG° = −RT ln K", ["ΔG° = RT ln K", "ΔG° = K", "ΔG° = −K/RT"], "A large K means a very negative ΔG°."),
      ("What is the enthalpy of combustion?", "the enthalpy change when one mole of a substance burns completely in oxygen", ["the heat to melt one mole", "the heat to form one mole", "the energy to break one bond"], "It is always negative."),
      ("In which process is ΔU = q (all heat goes to internal energy)?", "at constant volume", ["at constant pressure", "always", "never"], "No pV work is done.")]


# =================================================================== 6 equilibrium
KPC = [("N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", -2), ("PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)", 1), ("N₂O₄(g) ⇌ 2NO₂(g)", 1), ("2SO₂(g) + O₂(g) ⇌ 2SO₃(g)", -1), ("H₂(g) + I₂(g) ⇌ 2HI(g)", 0)]


def b_eq(k=None):
    k = k or ch(["kpkc", "ksp", "ksps", "poh", "oh", "k2"])
    if k == "kpkc":
        eq, dn = ch(KPC)
        Kc, T = ch([0.5, 1.5, 2.0, 4.0, 0.06, 26, 0.105]), ch([400, 500, 600, 700, 800])
        Kp = Kc * (0.0831 * T) ** dn
        return N("For %s, K<sub>c</sub> = %s at %d K. What is K<sub>p</sub>? (R = 0.0831 L bar K⁻¹ mol⁻¹)" % (eq, nf(Kc), T), Kp, [Kc * (0.0831 * T) ** (-dn) if dn else Kc * 2, Kc * (8.314 * T) ** dn, Kc * 0.0831 * T if dn != 1 else Kc / (0.0831 * T)], "",
                 "K<sub>p</sub> = K<sub>c</sub>(RT)<sup>Δn</sup> with Δn = %s, so K<sub>p</sub> = <b>%s</b>." % (nf(dn), nf(Kp))) if dn else \
            tq("For %s, K<sub>c</sub> = %s at %d K. What is K<sub>p</sub>?" % (eq, nf(Kc), T), nf(Kc), [nf(Kc * 0.0831 * T), nf(Kc / (0.0831 * T)), nf(Kc * Kc)], "Δn = 0, so K<sub>p</sub> = K<sub>c</sub> = <b>%s</b>." % nf(Kc))
    if k in ("ksp", "ksps"):
        salt, typ = ch([("AgCl", 1), ("BaSO₄", 1), ("AgBr", 1), ("CaF₂", 2), ("PbI₂", 2), ("Mg(OH)₂", 2), ("Ag₂CrO₄", 3)])
        s = rf(1, 9, 1) * 10 ** -ri(3, 5)
        K = s * s if typ == 1 else 4 * s ** 3
        if k == "ksp":
            return N("The solubility of %s is %s mol L⁻¹. What is its solubility product K<sub>sp</sub>?" % (salt, nf(s)), K, [s * s if typ != 1 else 4 * s ** 3, s, 2 * s * s], "",
                     "%s: K<sub>sp</sub> = %s = <b>%s</b>." % (salt, "s²" if typ == 1 else "(2s)²s = 4s³" if typ == 3 else "s(2s)² = 4s³", nf(K)))
        return N("K<sub>sp</sub> of %s is %s. What is its molar solubility?" % (salt, nf(K)), s, [math.sqrt(K) if typ != 1 else (K / 4) ** (1 / 3), K, K / 2], " mol L⁻¹",
                 "s = %s = <b>%s mol L⁻¹</b>." % ("√K<sub>sp</sub>" if typ == 1 else "∛(K<sub>sp</sub>/4)", nf(s)))
    if k == "poh":
        ph = rf(1, 13, 0.5)
        return N("A solution has pH %s at 298 K. What is its pOH?" % nf(ph), 14 - ph, [ph, 7 - ph if ph < 7 else ph - 7, 14 + ph], "", "pH + pOH = 14, so pOH = <b>%s</b>." % nf(14 - ph))
    if k == "oh":
        e = ri(1, 5)
        c = ch([1, 2, 5])
        oh = c * 10 ** -e
        ph = 14 + math.log10(oh)
        return N("What is the pH of a %s M NaOH solution at 298 K?" % nf(oh), ph, [-math.log10(oh), 14 - ph + 1 if ph < 13 else 7, 7 + math.log10(oh) + 7 - 1], "", "pOH = −log %s = %s, so pH = 14 − pOH = <b>%s</b>." % (nf(oh), nf(14 - ph), nf(ph)))
    eq, K = ch([("N₂ + 3H₂ ⇌ 2NH₃", ri(2, 20) * 0.1), ("H₂ + I₂ ⇌ 2HI", ri(20, 80)), ("2SO₂ + O₂ ⇌ 2SO₃", ri(2, 9) * 10)])
    rev = eq.split(" ⇌ ")[1] + " ⇌ " + eq.split(" ⇌ ")[0]
    return N("For %s, K = %s. What is K for the reverse reaction %s?" % (eq, nf(K), rev), 1 / K, [-K, K, K * K], "", "K(reverse) = 1/K = <b>%s</b>." % nf(1 / K))


CONJ = [("NH₃", "NH₄⁺"), ("H₂O", "H₃O⁺"), ("HCO₃⁻", "H₂CO₃"), ("CH₃COO⁻", "CH₃COOH"), ("Cl⁻", "HCl"), ("OH⁻", "H₂O"), ("HSO₄⁻", "H₂SO₄"), ("F⁻", "HF"), ("CO₃²⁻", "HCO₃⁻")]

B6 = [("What does Le Chatelier's principle say?", "a system at equilibrium shifts to reduce the effect of a change", ["equilibrium never changes", "catalysts shift equilibrium", "K changes with pressure"], "e.g. adding reactant shifts it to the right."),
      ("What is the effect of a catalyst on an equilibrium?", "it does not change the position; equilibrium is reached faster", ["it shifts it to the right", "it shifts it to the left", "it increases K"], "It speeds both forward and reverse reactions."),
      ("Which change alters the value of K?", "a change of temperature", ["a change of pressure", "adding a catalyst", "adding more reactant"], "K depends only on temperature."),
      ("At equilibrium, how do the rates of the forward and backward reactions compare?", "they are equal", ["the forward rate is zero", "the backward rate is zero", "the forward rate is always larger"], "Equilibrium is dynamic."),
      ("What is a Lewis acid?", "an electron pair acceptor", ["an electron pair donor", "a proton donor only", "an OH⁻ donor"], "e.g. BF₃ and AlCl₃."),
      ("What is a Brønsted–Lowry base?", "a proton (H⁺) acceptor", ["a proton donor", "an electron pair acceptor", "an OH⁻ acceptor"], "e.g. NH₃ accepts H⁺ to form NH₄⁺."),
      ("What is the common ion effect?", "the solubility or ionisation of a substance falls when a common ion is added", ["the solubility always rises", "ions combine into molecules", "acids become bases"], "e.g. adding NaCl reduces the solubility of AgCl."),
      ("What is the ionic product of water at 298 K?", "1.0 × 10⁻¹⁴", ["1.0 × 10⁻⁷", "14", "7"], "K<sub>w</sub> = [H⁺][OH⁻]."),
      ("What is a buffer solution?", "a solution that resists change in pH when a little acid or base is added", ["a very strong acid", "pure water", "a solution of pH 7 only"], "e.g. CH₃COOH and CH₃COONa."),
      ("What is the pH of a solution of NaCl in pure water at 298 K?", "7", ["less than 7", "more than 7", "0"], "It is a salt of a strong acid and a strong base."),
      ("What is the nature of an aqueous solution of CH₃COONa?", "basic", ["acidic", "neutral", "it cannot be said"], "Salt of a weak acid and a strong base; acetate ions hydrolyse."),
      ("What is the nature of an aqueous solution of NH₄Cl?", "acidic", ["basic", "neutral", "it cannot be said"], "Salt of a weak base and a strong acid."),
      ("When does a precipitate form from a solution of a sparingly soluble salt?", "when the ionic product exceeds K<sub>sp</sub>", ["when the ionic product is less than K<sub>sp</sub>", "always", "never"], "Q > K<sub>sp</sub> means the solution is supersaturated."),
      ("For N₂ + 3H₂ ⇌ 2NH₃ (exothermic), which condition increases the yield of ammonia?", "high pressure and low temperature", ["low pressure and high temperature", "a catalyst only", "removing N₂"], "Fewer moles of gas on the right; heat is given out."),
      ("What does a very large value of K (like 10¹⁵) tell us?", "the reaction goes almost to completion", ["hardly any product forms", "the reaction is very fast", "the reaction is endothermic"], "K says how far, not how fast.")]


# =================================================================== 7 redox
AGENT = [("Zn + Cu²⁺ → Zn²⁺ + Cu", "Cu²⁺", "Zn"), ("2Na + Cl₂ → 2NaCl", "Cl₂", "Na"), ("CuO + H₂ → Cu + H₂O", "CuO", "H₂"), ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", "Fe₂O₃", "CO"),
         ("2Mg + O₂ → 2MgO", "O₂", "Mg"), ("Cl₂ + 2KI → 2KCl + I₂", "Cl₂", "KI (I⁻)"), ("2FeCl₃ + H₂S → 2FeCl₂ + 2HCl + S", "FeCl₃ (Fe³⁺)", "H₂S"),
         ("Mg + 2HCl → MgCl₂ + H₂", "HCl (H⁺)", "Mg"), ("2Al + Fe₂O₃ → Al₂O₃ + 2Fe", "Fe₂O₃", "Al"), ("H₂ + Cl₂ → 2HCl", "Cl₂", "H₂")]


def b_agent(k=None):
    eq, ox, red = ch(AGENT)
    if (k or ch(["ox", "red"])) == "ox":
        return tq("In %s, which is the oxidising agent?" % eq, ox, [red, "neither", "both"], "%s gains electrons (is reduced), so it is the <b>oxidising agent</b>; %s is the reducing agent." % (ox, red))
    return tq("In %s, which is the reducing agent?" % eq, red, [ox, "neither", "both"], "%s loses electrons (is oxidised), so it is the <b>reducing agent</b>." % red)


B7 = [("What is oxidation in terms of electrons?", "loss of electrons", ["gain of electrons", "gain of protons", "loss of neutrons"], "OIL RIG: oxidation is loss."),
      ("What is reduction in terms of oxidation number?", "a decrease in oxidation number", ["an increase in oxidation number", "no change", "becoming zero"], "Gaining electrons lowers the oxidation number."),
      ("What is the oxidation number of oxygen in H₂O₂?", "−1", ["−2", "0", "+1"], "Peroxides have O at −1."),
      ("What is the oxidation number of oxygen in OF₂?", "+2", ["−2", "−1", "0"], "Fluorine is always −1."),
      ("What is the oxidation number of hydrogen in NaH?", "−1", ["+1", "0", "+2"], "In metal hydrides H is −1."),
      ("What is a disproportionation reaction?", "a reaction in which one element is both oxidised and reduced", ["a reaction with no electron transfer", "combustion", "a neutralisation"], "e.g. 2H₂O₂ → 2H₂O + O₂."),
      ("Which is a disproportionation reaction?", "Cl₂ + 2OH⁻ → ClO⁻ + Cl⁻ + H₂O", ["Zn + Cu²⁺ → Zn²⁺ + Cu", "NaOH + HCl → NaCl + H₂O", "C + O₂ → CO₂"], "Chlorine goes from 0 to +1 and −1."),
      ("Which metal will displace copper from copper sulphate solution?", "zinc", ["silver", "gold", "platinum"], "Zinc is more reactive than copper."),
      ("What is the best oxidising agent among the halogens?", "F₂", ["Cl₂", "Br₂", "I₂"], "Fluorine is the most electronegative."),
      ("What is a redox couple?", "the oxidised and reduced forms of a substance together", ["two metals in contact", "an acid and a base", "two catalysts"], "e.g. Zn²⁺/Zn."),
      ("Why can KMnO₄ act only as an oxidising agent?", "Mn is in its highest oxidation state, +7", ["Mn is at its lowest state", "it has no oxygen", "it is a metal"], "It can only be reduced."),
      ("What is the sum of oxidation numbers in a neutral compound?", "zero", ["equal to the charge on the metal", "one", "it depends on the compound"], "In an ion it equals the charge."),
      ("What is the standard electrode potential of the hydrogen electrode?", "0.00 V", ["1.00 V", "−0.76 V", "+0.34 V"], "It is the reference electrode."),
      ("Which happens at the anode of a galvanic cell?", "oxidation", ["reduction", "neither", "both"], "AN OX, RED CAT.")]


# =================================================================== 8 organic chemistry: basic principles
CHYB = [("CH₄", "sp³"), ("C₂H₆", "sp³"), ("C₂H₄", "sp²"), ("C₂H₂", "sp"), ("HCHO (the carbon)", "sp²"), ("CO₂", "sp"), ("C₆H₆ (each carbon)", "sp²"), ("CH₃OH (the carbon)", "sp³"),
        ("HCN (the carbon)", "sp"), ("CH₃CN (the CN carbon)", "sp"), ("CH₃CN (the CH₃ carbon)", "sp³"), ("CH₂=C=CH₂ (the middle carbon)", "sp"), ("CH₂=C=CH₂ (an end carbon)", "sp²"), ("CH₃COOH (the COOH carbon)", "sp²")]
FG = [("–OH (on an alkyl group)", "an alcohol"), ("–CHO", "an aldehyde"), ("–COOH", "a carboxylic acid"), ("–NH₂", "an amine"), ("–CO– (between two carbons)", "a ketone"), ("–COO– (ester link)", "an ester"),
      ("–O– (between two carbons)", "an ether"), ("–CN", "a nitrile"), ("–NO₂", "a nitro compound"), ("–CONH₂", "an amide")]
NE = [("OH⁻", "nucleophile"), ("CN⁻", "nucleophile"), ("NH₃", "nucleophile"), ("H₂O", "nucleophile"), ("Cl⁻", "nucleophile"), ("H⁺", "electrophile"), ("NO₂⁺", "electrophile"),
      ("BF₃", "electrophile"), ("AlCl₃", "electrophile"), ("CH₃⁺ (methyl carbocation)", "electrophile"), ("R–O⁻ (alkoxide)", "nucleophile"), ("Br⁺", "electrophile")]


def b_anal(k=None):
    k = k or ch(["C", "H", "N", "X"])
    m = rf(0.15, 0.6, 0.01)
    if k == "C":
        f = rf(0.2, 0.85, 0.01)
        x = round(m * f * 44 / 12, 3)
        return N("%s g of an organic compound gives %s g of CO₂ on complete combustion. What is the percentage of carbon?" % (nf(m), nf(x)), 12 / 44 * x / m * 100,
                 [x / m * 100, 44 / 12 * x / m * 100 % 100, 12 / 44 * x * 100], "%", "%% C = (12/44) × (mass of CO₂ ÷ mass of compound) × 100 = <b>%s%%</b>." % nf(12 / 44 * x / m * 100))
    if k == "H":
        f = rf(0.02, 0.15, 0.005)
        y = round(m * f * 18 / 2, 3)
        return N("%s g of an organic compound gives %s g of H₂O on complete combustion. What is the percentage of hydrogen?" % (nf(m), nf(y)), 2 / 18 * y / m * 100,
                 [y / m * 100, 1 / 18 * y / m * 100, 2 / 18 * y * 100], "%", "%% H = (2/18) × (mass of H₂O ÷ mass of compound) × 100 = <b>%s%%</b>." % nf(2 / 18 * y / m * 100))
    if k == "N":
        M, V = ch([0.1, 0.05, 0.2]), ri(10, 30)
        n = 2 * M * V / 1000
        pc = 14 * n / m * 100
        if pc > 60:
            return None
        return N("In Kjeldahl's method, the ammonia from %s g of a compound exactly neutralises %d mL of %s M H₂SO₄. What is the percentage of nitrogen?" % (nf(m), V, nf(M)), pc,
                 [pc / 2, 17 * n / m * 100, 14 * M * V / 1000 / m * 100 * 4], "%", "Moles of NH₃ = 2 × %s × %s = %s; %% N = 14 × %s ÷ %s × 100 = <b>%s%%</b>." % (nf(M), nf(V / 1000), nf(n), nf(n), nf(m), nf(pc)))
    w = round(m * rf(0.5, 1.6, 0.01), 3)
    X, Mx, ag = ch([("bromine", 80, 188), ("chlorine", 35.5, 143.5), ("iodine", 127, 235)])
    pc = Mx / ag * w / m * 100
    if pc > 95:
        return None
    sym = {"bromine": "AgBr", "chlorine": "AgCl", "iodine": "AgI"}[X]
    return N("In Carius method, %s g of a compound gives %s g of %s. What is the percentage of %s?" % (nf(m), nf(w), sym, X), pc, [w / m * 100, Mx / ag * w * 100, (ag - Mx) / ag * w / m * 100], "%",
             "%% %s = (%s/%s) × (%s ÷ %s) × 100 = <b>%s%%</b>." % (X, nf(Mx), nf(ag), nf(w), nf(m), nf(pc)))


B8 = [("Which type of isomerism do CH₃CH₂OH and CH₃OCH₃ show?", "functional group isomerism", ["chain isomerism", "position isomerism", "geometrical isomerism"], "Same formula, different functional groups."),
      ("Which type of isomerism do butane and 2-methylpropane show?", "chain isomerism", ["position isomerism", "functional group isomerism", "metamerism"], "Different carbon skeletons."),
      ("Which type of isomerism do propan-1-ol and propan-2-ol show?", "position isomerism", ["chain isomerism", "functional group isomerism", "metamerism"], "The –OH is on a different carbon."),
      ("Which type of isomerism do CH₃OC₃H₇ and C₂H₅OC₂H₅ show?", "metamerism", ["chain isomerism", "position isomerism", "functional group isomerism"], "Different alkyl groups on each side of the same functional group."),
      ("What is homolytic cleavage?", "a bond breaks so each atom keeps one electron, giving free radicals", ["both electrons go to one atom", "no bond breaks", "a bond forms"], "Shown with half-headed (fish-hook) arrows."),
      ("What is heterolytic cleavage?", "a bond breaks so one atom keeps both electrons, giving ions", ["each atom keeps one electron", "a bond forms", "free radicals form"], "Shown with full curved arrows."),
      ("Which carbocation is the most stable?", "tertiary (CH₃)₃C⁺", ["primary CH₃CH₂⁺", "secondary (CH₃)₂CH⁺", "methyl CH₃⁺"], "Alkyl groups release electrons (+I and hyperconjugation)."),
      ("What is the inductive effect?", "a permanent shift of σ-bond electrons caused by an electronegative or electropositive group", ["movement of π electrons", "temporary polarisation by a reagent", "a type of isomerism"], "e.g. –Cl shows a −I effect."),
      ("Which group shows a +I effect?", "–CH₃", ["–NO₂", "–Cl", "–COOH"], "Alkyl groups release electrons."),
      ("Which method separates two liquids whose boiling points are close?", "fractional distillation", ["simple distillation", "sublimation", "crystallisation"], "Used to separate crude oil fractions."),
      ("Which method purifies camphor or naphthalene?", "sublimation", ["distillation", "chromatography", "filtration"], "They change directly from solid to vapour."),
      ("Which test detects nitrogen, sulphur and halogens in an organic compound?", "Lassaigne's test (sodium fusion)", ["Kjeldahl's method", "Carius method", "Dumas method"], "Covalent elements are turned into ionic sodium salts."),
      ("What colour shows nitrogen in Lassaigne's test?", "Prussian blue", ["blood red", "violet", "black"], "Fe₄[Fe(CN)₆]₃ forms."),
      ("What is the IUPAC name of CH₃CH₂CH₂OH?", "propan-1-ol", ["propan-2-ol", "propanol-1", "1-propanal"], "The –OH is on carbon 1."),
      ("What is hyperconjugation?", "delocalisation of σ electrons of a C–H bond into an adjacent empty or π orbital", ["a hydrogen bond", "resonance of a benzene ring only", "an ionic bond"], "It explains carbocation stability."),
      ("What is the IUPAC name of CH₃COCH₃?", "propanone", ["propanal", "propan-2-ol", "ethanone"], "A three-carbon ketone.")]


# =================================================================== 9 hydrocarbons
ALK = {1: "methane", 2: "ethane", 3: "propane", 4: "butane", 5: "pentane", 6: "hexane", 7: "heptane", 8: "octane", 9: "nonane", 10: "decane"}


def b_hc(k=None):
    k = k or ch(["yne", "yneO2", "wurtz", "ene"])
    n = ri(2, 12)
    if k in ("aneO2", "eneO2"):
        n = ri(1, 10) if k == "aneO2" else ri(2, 10)
        h = 2 * n + 2 if k == "aneO2" else 2 * n
        o = n + h / 4
        return N("How many moles of O₂ are needed to burn one mole of %s completely?" % fm("C%dH%d" % (n, h)), o, [n + h / 2, (n + h) / 2, 2 * o], " mol",
                 "%s + %s O₂ → %d CO₂ + %d H₂O: O atoms needed = 2 × %d + %d = %d, so <b>%s mol</b> of O₂." % (fm("C%dH%d" % (n, h)), nf(o), n, h // 2, n, h // 2, 2 * n + h // 2, nf(o)))
    if k == "yne":
        return tq("What is the molecular formula of the alkyne with %d carbon atoms?" % n, fm("C%dH%d" % (n, 2 * n - 2)), [fm("C%dH%d" % (n, 2 * n)), fm("C%dH%d" % (n, 2 * n + 2)), fm("C%dH%d" % (n, n))],
                  "Alkynes are C<sub>n</sub>H<sub>2n−2</sub>: <b>%s</b>." % fm("C%dH%d" % (n, 2 * n - 2)))
    if k == "ene":
        return tq("What is the general formula of the hydrocarbon %s?" % ch(["ethene", "propene", "but-1-ene", "pent-1-ene"]), "C<sub>n</sub>H<sub>2n</sub>", ["C<sub>n</sub>H<sub>2n+2</sub>", "C<sub>n</sub>H<sub>2n−2</sub>", "C<sub>n</sub>H<sub>n</sub>"],
                  "It is an alkene: C<sub>n</sub>H<sub>2n</sub>.")
    if k == "yneO2":
        o = (3 * n - 1) / 2
        return N("How many moles of O₂ are needed to burn one mole of the alkyne %s completely?" % fm("C%dH%d" % (n, 2 * n - 2)), o, [(3 * n + 1) / 2, 3 * n / 2, n + 1], " mol",
                 "C<sub>n</sub>H<sub>2n−2</sub> + ((3n − 1)/2)O₂ → nCO₂ + (n − 1)H₂O: <b>%s mol</b>." % nf(o))
    m = ri(1, 4)
    return tq("Which alkane forms when %s reacts with sodium in dry ether (Wurtz reaction)?" % {1: "bromomethane", 2: "bromoethane", 3: "1-bromopropane", 4: "1-bromobutane", 5: "1-bromopentane"}[m],
              ALK[2 * m], [ALK[x] for x in sorted({m, 2 * m + 1, 2 * m - 1 if m > 1 else 3, 2 * m + 2} - {2 * m})][:3], "Two alkyl groups join: 2R–X + 2Na → R–R. A C%d group gives <b>%s</b>." % (m, ALK[2 * m]))


B9 = [("What is the main product when HBr adds to propene (no peroxide)?", "2-bromopropane", ["1-bromopropane", "propane", "1,2-dibromopropane"], "Markovnikov's rule: H goes to the carbon that already has more H atoms."),
      ("What is the main product when HBr adds to propene in the presence of a peroxide?", "1-bromopropane", ["2-bromopropane", "propan-2-ol", "propane"], "The anti-Markovnikov (Kharasch, peroxide) effect."),
      ("Which test shows that a hydrocarbon is unsaturated?", "it decolourises bromine water", ["it burns", "it is a gas", "it dissolves in water"], "Br₂ adds across the C=C."),
      ("What is formed when ethyne is passed through a red-hot iron tube?", "benzene", ["ethane", "ethanol", "methane"], "Three ethyne molecules join (cyclic polymerisation)."),
      ("Which rule decides whether a cyclic, planar molecule is aromatic?", "Hückel's (4n + 2) π electron rule", ["Markovnikov's rule", "Hund's rule", "Saytzeff's rule"], "Benzene has 6 π electrons (n = 1)."),
      ("Which reaction is typical of benzene?", "electrophilic substitution", ["electrophilic addition", "nucleophilic addition", "free-radical addition"], "Substitution keeps the stable aromatic ring."),
      ("What is the electrophile in the nitration of benzene?", "the nitronium ion NO₂⁺", ["NO₃⁻", "H⁺", "OH⁻"], "Made from conc. HNO₃ and conc. H₂SO₄."),
      ("Which alkene shows geometrical (cis–trans) isomerism?", "but-2-ene", ["ethene", "propene", "but-1-ene"], "Each double-bond carbon carries two different groups."),
      ("Which conformation of ethane is more stable?", "staggered", ["eclipsed", "both are equal", "neither"], "The C–H bonds are as far apart as possible."),
      ("What does ozonolysis of ethene give?", "two molecules of methanal (HCHO)", ["ethanol", "ethanoic acid", "carbon dioxide only"], "Ozone cuts the C=C bond."),
      ("Which is more acidic, ethyne or ethane?", "ethyne", ["ethane", "both are equal", "neither"], "The sp carbon holds the electron pair more tightly."),
      ("What is the product of the Friedel–Crafts methylation of benzene (CH₃Cl, anhydrous AlCl₃)?", "toluene (methylbenzene)", ["chlorobenzene", "benzoic acid", "phenol"], "An alkyl group replaces a hydrogen."),
      ("Which type of reaction do alkanes undergo with chlorine in sunlight?", "free-radical substitution", ["addition", "elimination", "electrophilic substitution"], "Hydrogen atoms are replaced by chlorine."),
      ("What is the IUPAC name of CH₃–C≡C–CH₃?", "but-2-yne", ["but-1-yne", "butene", "2-butyne-1"], "The triple bond starts at carbon 2."),
      ("Which gas is given off when calcium carbide reacts with water?", "ethyne", ["methane", "ethene", "hydrogen"], "CaC₂ + 2H₂O → Ca(OH)₂ + C₂H₂."),
      ("What are o-, m- and p- directing groups? Which is ortho/para-directing?", "–OH", ["–NO₂", "–COOH", "–CHO"], "Electron-donating groups direct to ortho and para positions.")]


def UNITS():
    b = {k: B(v) for k, v in [(1, B1), (2, B2), (4, B4), (5, B5), (6, B6), (7, B7), (8, B8), (9, B9)]}
    trend = B(TREND)
    hyb = pairs([(a, b_, "%s: %s hybridised, %s." % (a, b_, c)) for a, b_, c in HYB], "What is the hybridisation of the central atom in %s?", "Which of these has an %s-hybridised central atom?")
    hyb2 = pairs([(a, c) for a, b_, c in HYB if "(" not in a or "oxygen" in a or "nitrogen" in a], "What is the shape of %s?", None)
    chyb = pairs(CHYB, "What is the hybridisation of carbon in %s?", None, pool=["sp³d", "sp³d²"])
    fg = pairs([(x, y, "%s is the functional group of %s." % (x, y)) for x, y in FG], "Which class of compound has the functional group %s?", "Which functional group is found in %s?")
    ne = pairs(NE, "Is %s an electrophile or a nucleophile?", "Which of these is a %s?", pool=["a free radical", "neither"])
    conj = pairs([(a, b_, "Adding H⁺ to %s gives %s." % (a, b_)) for a, b_ in CONJ], "What is the conjugate acid of %s?", "Which species is the conjugate base of %s?")
    return [
        SU(CH, 15, "some-basic-concepts-of-chemistry", 1,
           "General introduction: importance and scope of chemistry. Nature of matter, laws of chemical combination, Dalton's atomic theory: concept of elements, atoms and molecules. Atomic and molecular masses, mole concept and molar mass, percentage composition, empirical and molecular formula, chemical reactions, stoichiometry and calculations based on stoichiometry.",
           "Some Basic Concepts of Chemistry", "basic concepts of chemistry",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 1 Some Basic Concepts of Chemistry: laws of chemical combination, the mole, molar mass, empirical formula, limiting reagent, molarity and molality. 100 questions with answers.",
           "Moles = mass ÷ molar mass.", "Molarity = mol per litre of solution; molality = mol per kg of solvent.",
           "<p>Chemical combination follows laws: conservation of mass, definite proportions, multiple proportions, Gay-Lussac's gaseous volumes and Avogadro's law. One mole is 6.022 × 10²³ particles, and its mass in grams equals the molar mass. The empirical formula is the simplest ratio of atoms; the molecular formula is a multiple of it.</p>"
           "<p>In a reaction the limiting reagent runs out first and fixes the amount of product. Concentration can be given as mass per cent, mole fraction, molarity (mol L⁻¹ of solution) or molality (mol kg⁻¹ of solvent); molality does not change with temperature.</p>",
           [("36 g of water. Moles?", ["36 ÷ 18"], "2 mol"), ("4 g NaOH in 500 mL. Molarity?", ["0.1 mol ÷ 0.5 L"], "0.2 mol L⁻¹")],
           ["Using the mass of solution instead of solvent for molality.", "Using mL instead of L in molarity.", "Picking the reactant with fewer moles as limiting without dividing by coefficients."],
           [("What is the difference between molarity and molality?", "Molarity is moles per litre of solution; molality is moles per kilogram of solvent, so it does not change with temperature."),
            ("What is a limiting reagent?", "The reactant that is completely used up first; it decides the amount of product.")],
           lambda: [("Laws and the mole", [(b[1], 6), (T(C.c_moles, "n", "m", "N"), 14)]), ("Molar mass and formulae", [(T(C.c_moles, "Mr"), 6), (T(C.c_emp, "emp", "mol"), 12), (b[1], 2)]),
                    ("Concentration", [(K(b_conc, "M", "m", "x", "pct"), 18), (b[1], 2)]), ("Stoichiometry", [(K(b_limit, "which", "mass"), 14), (T(C.c_yield, "theo"), 6)]),
                    ("Solutions and mixed problems", [(K(b_conc, "mass", "dil"), 14), (b[1], 3), (T(C.c_yield, "yield"), 3)])]),
        SU(CH, 16, "structure-of-atom", 2,
           "Discovery of electron, proton and neutron, atomic number, isotopes and isobars. Thomson's model and its limitations. Rutherford's model and its limitations, Bohr's model and its limitations, concept of shells and subshells, dual nature of matter and light, de Broglie's relationship, Heisenberg uncertainty principle, concept of orbitals, quantum numbers, shapes of s, p and d orbitals, rules for filling electrons in orbitals – Aufbau principle, Pauli's exclusion principle and Hund's rule, electronic configuration of atoms, stability of half-filled and completely filled orbitals.",
           "Structure of Atom", "structure of atom",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 2 Structure of Atom: subatomic particles, Bohr's model and hydrogen spectrum, photons, de Broglie wavelength, quantum numbers and electronic configuration. 100 questions with answers.",
           "E(n) = −13.6/n² eV for hydrogen.", "An orbital is set by n, l and m(l); it holds two electrons of opposite spin.",
           "<p>An atom has a tiny positive nucleus (protons and neutrons) with electrons around it. Bohr's model gives hydrogen energies E<sub>n</sub> = −13.6/n² eV and radii 52.9 n² pm; a jump between levels gives a spectral line with 1/λ = R<sub>H</sub>(1/n₁² − 1/n₂²). Light and electrons have dual nature: E = hν and λ = h/mv.</p>"
           "<p>Quantum numbers n, l, m<sub>l</sub> and m<sub>s</sub> describe each electron. A subshell has 2l + 1 orbitals and a shell holds 2n² electrons. Electrons fill orbitals by the Aufbau principle (lower n + l first), the Pauli principle and Hund's rule.</p>",
           [("n = 3, l = 2. Orbital?", ["l = 2 is d"], "3d"), ("H, n = 3 → n = 2. Series?", ["lower level 2"], "Balmer")],
           ["Letting l equal n.", "Filling 3d before 4s.", "Forgetting the minus sign in E<sub>n</sub>."],
           [("Why is 4s filled before 3d?", "4s has the lower n + l value (4 compared with 5), so it has lower energy when it fills."),
            ("How many electrons can a shell hold?", "At most 2n² electrons.")],
           lambda: [("Subatomic particles", [(A(P.p_nucleus), 14), (b[2], 6)]), ("Bohr's model", [(K(b_bohr, "En", "r", "Z"), 14), (b[2], 4), (A(P.p_nucleus), 2)]), ("The hydrogen spectrum", [(K(b_bohr, "dE", "lam", "series"), 20)]),
                    ("Photons and matter waves", [(A(P.p_photon, "J", "eV", "f"), 11), (A(P.p_debroglie), 6), (b[2], 3)]), ("Quantum numbers and configuration", [(K(b_qn, "name", "orbs", "shell", "shello", "ml"), 10), (T(C.c_config, "atom", "ion", "count"), 10)])]),
        SU(CH, 17, "classification-of-elements-and-periodicity-in-properties", 3,
           "Significance of classification, brief history of the development of the periodic table, modern periodic law and the present form of the periodic table, periodic trends in properties of elements – atomic radii, ionic radii, inert gas radii, ionisation enthalpy, electron gain enthalpy, electronegativity, valency. Nomenclature of elements with atomic number greater than 100.",
           "Classification of Elements and Periodicity", "classification of elements",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 3 Classification of Elements and Periodicity in Properties: periods, groups and blocks, IUPAC names above 100, atomic radius, ionisation enthalpy and electronegativity. 100 questions with answers.",
           "The modern periodic law is based on atomic number.", "Across a period radius falls and ionisation enthalpy rises; down a group the opposite.",
           "<p>The modern periodic table arranges elements by atomic number into 7 periods and 18 groups. The block (s, p, d, f) is set by the orbital that the last electron enters. The period is the highest shell number. Elements above Z = 100 have temporary IUPAC names built from digit roots: nil, un, bi, tri, quad, pent, hex, sept, oct, enn + ium.</p>"
           "<p>Across a period nuclear charge increases, so atomic radius falls and ionisation enthalpy and electronegativity rise. Down a group new shells are added, so radius rises. Exceptions such as N &gt; O and Be &gt; B in ionisation enthalpy come from stable half-filled and filled subshells.</p>",
           [("Z = 20 (Ca). Period and group?", ["[Ar] 4s²"], "period 4, group 2"), ("Z = 114. IUPAC name?", ["un-un-quad-ium"], "ununquadium")],
           ["Using atomic mass instead of atomic number.", "Writing the IUPAC name as 'biium'.", "Thinking a cation is larger than its atom."],
           [("Why does atomic radius decrease across a period?", "The nuclear charge increases while electrons enter the same shell, so they are pulled closer."),
            ("Why is the first ionisation enthalpy of N greater than that of O?", "N has a stable half-filled 2p³ subshell; in O one 2p electron is paired and easier to remove.")],
           chname="Classification of Elements and Periodicity in Properties", sets=lambda: [("Periods and groups", [(K(b_table, "period", "group"), 16), (trend, 4)]), ("Blocks", [(K(b_table, "block"), 14), (trend, 3), (T(C.c_config, "atom"), 3)]),
                    ("IUPAC names above 100", [(K(b_iupac, "name", "sym"), 18), (trend, 2)]), ("Periodic trends", [(trend, 6), (T(C.c_config, "ion", "count"), 4), (K(b_table, "group"), 10)]),
                    ("Mixed problems", [(K(b_table, "period", "group", "block"), 14), (K(b_iupac, "name"), 6)])]),
        SU(CH, 18, "chemical-bonding-and-molecular-structure", 4,
           "Valence electrons, ionic bond, covalent bond, bond parameters, Lewis structure, polar character of covalent bond, covalent character of ionic bond, valence bond theory, resonance, geometry of covalent molecules, VSEPR theory, concept of hybridization involving s, p and d orbitals and shapes of some simple molecules, molecular orbital theory of homonuclear diatomic molecules (qualitative idea only), hydrogen bond.",
           "Chemical Bonding and Molecular Structure", "chemical bonding",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 4 Chemical Bonding and Molecular Structure: octet rule, VSEPR shapes and bond angles, hybridisation, dipole moment, molecular orbital bond order and hydrogen bonding. 100 questions with answers.",
           "VSEPR: electron pairs repel and get as far apart as possible.", "Bond order = ½(N(b) − N(a)).",
           "<p>Atoms bond to reach stable configurations: by transferring electrons (ionic) or sharing them (covalent). VSEPR theory predicts shape from the electron pairs round the central atom; lone pairs repel more, so H₂O (104.5°) is bent and NH₃ (107°) pyramidal. Hybridisation sp, sp², sp³, sp³d and sp³d² gives linear, trigonal planar, tetrahedral, trigonal bipyramidal and octahedral arrangements.</p>"
           "<p>Molecular orbital theory gives bond order ½(N<sub>b</sub> − N<sub>a</sub>); O₂ has two unpaired electrons, so it is paramagnetic. Polar bonds can still give a non-polar molecule if the dipoles cancel (CO₂). Hydrogen bonds form between H and F, O or N.</p>",
           [("Bond order of N₂?", ["(10 − 4) ÷ 2"], "3"), ("Hybridisation in BF₃?", ["3 bond pairs, no lone pair"], "sp²")],
           ["Giving CO₂ a dipole moment because its bonds are polar.", "Forgetting lone pairs when naming shapes.", "Saying O₂ is diamagnetic."],
           [("Why is O₂ paramagnetic?", "Molecular orbital theory puts two unpaired electrons in its π* orbitals."),
            ("Why is the bond angle of water less than 109.5°?", "Its two lone pairs repel the bonding pairs more strongly and push them together.")],
           lambda: [("Covalent bonds and the octet rule", [(b[4], 5), (T(C.c_shape, "shape"), 7), (hyb2, 3), (chyb, 5)]), ("VSEPR shapes", [(T(C.c_shape, "shape"), 8), (hyb2, 3), (b[4], 2), (chyb, 4), (T(C.c_shape, "angle"), 3)]),
                    ("Bond angles", [(T(C.c_shape, "angle"), 10), (b[4], 2), (chyb, 2), (K(b_mo, "bo"), 6)]), ("Hybridisation", [(hyb, 18), (b[4], 2)]), ("Molecular orbital theory", [(K(b_mo, "bo", "mag"), 18), (b[4], 2)])]),
        SU(CH, 19, "chemical-thermodynamics", 5,
           "Concepts of system and types of systems, surroundings, work, heat, energy, extensive and intensive properties, state functions. First law of thermodynamics – internal energy and enthalpy, heat capacity and specific heat, measurement of ΔU and ΔH, Hess's law of constant heat summation, enthalpy of bond dissociation, combustion, formation, atomization, sublimation, phase transition, ionization, solution and dilution. Second law of thermodynamics (brief introduction). Introduction of entropy as a state function, Gibbs energy change for spontaneous and non-spontaneous processes, criteria for equilibrium. Third law of thermodynamics (brief introduction).",
           "Thermodynamics (Chemistry)", "chemical thermodynamics",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 5 Thermodynamics: systems, the first law, work and heat, ΔH = ΔU + ΔngRT, Hess's law, bond enthalpies, entropy and Gibbs energy. 100 questions with answers.",
           "ΔU = q + w; ΔH = ΔU + Δn(g)RT.", "A process is spontaneous when ΔG = ΔH − TΔS is negative.",
           "<p>Chemistry uses the sign convention ΔU = q + w, where w is work done on the system; expansion against p<sub>ext</sub> gives w = −p<sub>ext</sub>ΔV. Enthalpy H = U + pV, so for gas reactions ΔH = ΔU + Δn<sub>g</sub>RT. Hess's law lets us add equations; ΔH = ΣΔ<sub>f</sub>H(products) − ΣΔ<sub>f</sub>H(reactants), or Σ bonds broken − Σ bonds formed.</p>"
           "<p>Entropy measures disorder; gases and more particles mean higher entropy. Spontaneity is decided by Gibbs energy: ΔG = ΔH − TΔS must be negative. At equilibrium ΔG = 0, and ΔG° = −RT ln K.</p>",
           [("q = 400 J absorbed, 150 J work done by system. ΔU?", ["400 + (−150)"], "250 J"), ("ΔH = −92 kJ, ΔS = −0.2 kJ/K, 298 K. ΔG?", ["−92 + 59.6"], "−32.4 kJ")],
           ["Using the physics sign convention for work.", "Forgetting to change J to kJ in ΔG = ΔH − TΔS.", "Counting liquids and solids in Δn<sub>g</sub>."],
           [("What is the difference between ΔH and ΔU?", "ΔH includes the pV work at constant pressure: ΔH = ΔU + Δn<sub>g</sub>RT for gas reactions."),
            ("When is a reaction spontaneous?", "At constant temperature and pressure, when ΔG = ΔH − TΔS is negative.")],
           chname="Thermodynamics", sets=lambda: [("Systems and the first law", [(b[5], 4), (K(b_thermo, "dU", "q"), 16)]), ("Work and enthalpy", [(K(b_thermo, "w"), 8), (K(b_thermo, "dng", "dH"), 12)]),
                    ("Hess's law and bond enthalpy", [(T(C.c_hess, "form", "bond"), 17), (b[5], 3)]), ("Entropy", [(T(C.c_entropy, "calc", "sign"), 16), (b[5], 3), (T(C.c_gibbs, "feas"), 1)]),
                    ("Gibbs energy and spontaneity", [(T(C.c_gibbs, "G", "T", "feas"), 18), (b[5], 2)])]),
        SU(CH, 20, "equilibrium", 6,
           "Equilibrium in physical and chemical processes, dynamic nature of equilibrium, law of mass action, equilibrium constant, factors affecting equilibrium – Le Chatelier's principle, ionic equilibrium – ionization of acids and bases, strong and weak electrolytes, degree of ionization, ionization of polybasic acids, acid strength, concept of pH, hydrolysis of salts (elementary idea), buffer solution, Henderson equation, solubility product, common ion effect (with illustrative examples).",
           "Equilibrium", "equilibrium",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 6 Equilibrium: Kc and Kp, Le Chatelier's principle, acids and bases, pH and pOH, weak acids, buffers, salt hydrolysis and solubility product. 100 questions with answers.",
           "K(p) = K(c)(RT)^Δn.", "pH = −log[H⁺]; pH + pOH = 14 at 298 K.",
           "<p>At equilibrium the forward and backward rates are equal. The law of mass action gives K<sub>c</sub> = [products]/[reactants] with powers from the equation; for gases K<sub>p</sub> = K<sub>c</sub>(RT)<sup>Δn</sup>. Only temperature changes K; Le Chatelier's principle predicts how concentration, pressure and temperature shift the position.</p>"
           "<p>pH = −log[H⁺] and K<sub>w</sub> = [H⁺][OH⁻] = 10⁻¹⁴ at 298 K. Weak acids partly ionise (K<sub>a</sub>); a buffer keeps pH steady, pH = pK<sub>a</sub> + log([salt]/[acid]). For a salt AB, K<sub>sp</sub> = s²; for AB₂ it is 4s³.</p>",
           [("0.01 M HCl. pH?", ["−log 10⁻²"], "2"), ("AgCl, s = 10⁻⁵ M. Ksp?", ["s²"], "10⁻¹⁰")],
           ["Thinking a catalyst shifts equilibrium.", "Using pH = 14 − log[OH⁻].", "Using s² for an AB₂ salt."],
           [("What changes the value of an equilibrium constant?", "Only a change of temperature. Concentration, pressure and catalysts do not."),
            ("What is a buffer?", "A solution that keeps its pH nearly constant when a little acid or base is added, such as CH₃COOH with CH₃COONa.")],
           lambda: [("Equilibrium constants", [(T(C.c_kc, "expr", "calc"), 12), (K(b_eq, "kpkc", "k2"), 8)]), ("Le Chatelier's principle", [(T(C.c_kc, "shiftT", "shiftP", "cat"), 14), (b[6], 6)]),
                    ("Acids, bases and pH", [(T(C.c_ph, "strong", "H"), 10), (K(b_eq, "poh", "oh"), 6), (conj, 4)]), ("Weak acids and buffers", [(T(C.c_ph, "weak", "ka", "buffer"), 16), (b[6], 4)]),
                    ("Solubility product and mixed problems", [(K(b_eq, "ksp", "ksps"), 14), (b[6], 2), (T(C.c_ice), 4)])]),
        SU(CH, 21, "redox-reactions", 7,
           "Concept of oxidation and reduction, redox reactions, oxidation number, balancing redox reactions in terms of loss and gain of electrons and change in oxidation number, applications of redox reactions.",
           "Redox Reactions", "redox reactions",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 7 Redox Reactions: oxidation and reduction, oxidation numbers, oxidising and reducing agents, half-equations and disproportionation. 100 questions with answers.",
           "Oxidation is loss of electrons; reduction is gain (OIL RIG).", "The oxidising agent is itself reduced.",
           "<p>Oxidation is the loss of electrons, or an increase in oxidation number; reduction is the gain of electrons, or a decrease. They always happen together. The oxidising agent takes electrons and is reduced; the reducing agent gives electrons and is oxidised.</p>"
           "<p>Oxidation numbers follow rules: elements are 0, oxygen is usually −2 (−1 in peroxides), hydrogen +1 (−1 in metal hydrides), and the sum equals the charge. Redox equations are balanced by electrons in half-equations. In disproportionation one element is both oxidised and reduced.</p>",
           [("Oxidation number of Mn in KMnO₄?", ["+1 + x − 8 = 0"], "+7"), ("Zn + Cu²⁺ → Zn²⁺ + Cu. Reducing agent?", ["Zn loses electrons"], "Zn")],
           ["Calling the substance that is oxidised the oxidising agent.", "Taking O as −2 in H₂O₂.", "Forgetting that the sum in an ion equals the charge."],
           [("How do you find an oxidation number?", "Use the rules (O is −2, H is +1, the sum equals the charge) and solve for the unknown element."),
            ("What is a disproportionation reaction?", "A redox reaction in which the same element is both oxidised and reduced.")],
           lambda: [("Oxidation and reduction", [(b[7], 4), (T(C.c_halfe, "kind"), 16)]), ("Oxidation numbers", [(T(C.c_ox), 18), (b[7], 2)]), ("Oxidising and reducing agents", [(K(b_agent, "ox", "red"), 14), (b[7], 3), (T(C.c_ox), 3)]),
                    ("Half-equations", [(T(C.c_halfe, "n"), 14), (T(C.c_ox), 6)]), ("Mixed problems", [(K(b_agent, "ox", "red"), 2), (b[7], 1), (T(C.c_halfe, "n", "kind"), 7), (T(C.c_ox), 10)])]),
        SU(CH, 22, "organic-chemistry-some-basic-principles-and-techniques", 8,
           "General introduction, classification and IUPAC nomenclature of organic compounds. Electronic displacements in a covalent bond: inductive effect, electromeric effect, resonance and hyperconjugation. Homolytic and heterolytic fission of a covalent bond: free radicals, carbocations, carbanions, electrophiles and nucleophiles, types of organic reactions. Methods of purification, qualitative and quantitative analysis.",
           "Organic Chemistry: Basic Principles and Techniques", "basic principles of organic chemistry",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 8 Organic Chemistry – Some Basic Principles and Techniques: hybridisation, functional groups, IUPAC names, isomerism, electrophiles and nucleophiles, and estimation of C, H, N and halogens. 100 questions with answers.",
           "Name by the longest chain, the main functional group and the lowest locants.", "Electrophiles seek electrons; nucleophiles give electron pairs.",
           "<p>Carbon forms four bonds using sp³ (single bonds), sp² (one double bond) or sp (a triple bond or two double bonds) hybrids. Compounds are grouped by functional group and named by IUPAC rules. Isomers can differ in chain, position, functional group or metamerism.</p>"
           "<p>Bonds break homolytically (free radicals) or heterolytically (carbocations and carbanions). Electrophiles such as H⁺ and NO₂⁺ accept electron pairs; nucleophiles such as OH⁻ and NH₃ donate them. Elements are estimated quantitatively: %C = (12/44) × m(CO₂)/m × 100, %H = (2/18) × m(H₂O)/m × 100, N by Kjeldahl's method and halogens by Carius method.</p>",
           [("Hybridisation of C in C₂H₂?", ["triple bond"], "sp"), ("0.2 g gives 0.44 g CO₂. %C?", ["12/44 × 0.44/0.2 × 100"], "60%")],
           ["Calling NH₃ an electrophile.", "Using 44/12 instead of 12/44 for % carbon.", "Numbering a chain from the wrong end."],
           [("How do you tell an electrophile from a nucleophile?", "An electrophile is electron-poor and accepts an electron pair; a nucleophile is electron-rich and donates one."),
            ("Why is a tertiary carbocation the most stable?", "Three alkyl groups release electrons by inductive effect and hyperconjugation, spreading out the positive charge.")],
           chname="Organic Chemistry – Some Basic Principles and Techniques", sets=lambda: [("Hybridisation of carbon", [(chyb, 10), (b[8], 4), (ne, 6)]), ("Functional groups and names", [(fg, 12), (T(C.c_name), 8)]), ("Isomerism and bond fission", [(b[8], 6), (T(C.c_name), 14)]),
                    ("Electrophiles and nucleophiles", [(ne, 10), (b[8], 3), (T(C.c_name), 7)]), ("Quantitative analysis", [(K(b_anal, "C", "H", "N", "X"), 20)])]),
        SU(CH, 23, "hydrocarbons", 9,
           "Classification of hydrocarbons. Aliphatic hydrocarbons: alkanes – nomenclature, isomerism, conformation (ethane only), physical properties, chemical reactions; alkenes – nomenclature, structure of double bond, geometrical isomerism, methods of preparation, chemical reactions: addition of hydrogen, halogen, water, hydrogen halides (Markovnikov's addition and peroxide effect), ozonolysis, oxidation, mechanism of electrophilic addition; alkynes – nomenclature, structure of triple bond, methods of preparation, chemical reactions, acidic character of alkynes. Aromatic hydrocarbons: introduction, IUPAC nomenclature, benzene: resonance, aromaticity, chemical properties, mechanism of electrophilic substitution, directive influence of a functional group in monosubstituted benzene. Carcinogenicity and toxicity.",
           "Hydrocarbons", "hydrocarbons",
           "Free CBSE Class 11 Chemistry worksheets for NCERT Chapter 9 Hydrocarbons: alkanes, alkenes and alkynes, formulae, combustion, Wurtz reaction, Markovnikov's rule, benzene and electrophilic substitution. 100 questions with answers.",
           "Alkanes CₙH₂ₙ₊₂, alkenes CₙH₂ₙ, alkynes CₙH₂ₙ₋₂.", "Alkenes add; benzene substitutes.",
           "<p>Alkanes (C<sub>n</sub>H<sub>2n+2</sub>) are saturated and react by free-radical substitution. Alkenes (C<sub>n</sub>H<sub>2n</sub>) and alkynes (C<sub>n</sub>H<sub>2n−2</sub>) are unsaturated and take part in addition reactions; HX adds by Markovnikov's rule, except HBr with peroxide. The Wurtz reaction joins two alkyl groups with sodium.</p>"
           "<p>Benzene has 6 delocalised π electrons and is aromatic by Hückel's (4n + 2) rule, so it prefers electrophilic substitution such as nitration and Friedel–Crafts reactions. Groups such as –OH and –CH₃ direct new groups to ortho and para positions; –NO₂ directs to meta.</p>",
           [("Alkyne with 4 carbons?", ["CₙH₂ₙ₋₂"], "C₄H₆"), ("HBr + propene?", ["Markovnikov"], "2-bromopropane")],
           ["Writing alkynes as CₙH₂ₙ.", "Forgetting the peroxide effect for HBr.", "Saying benzene adds bromine easily like an alkene."],
           [("What is Markovnikov's rule?", "When HX adds to an unsymmetrical alkene, the hydrogen goes to the carbon that already has more hydrogen atoms."),
            ("Why does benzene undergo substitution rather than addition?", "Substitution keeps the stable aromatic π system; addition would destroy it.")],
           lambda: [("Alkanes", [(T(C.c_formula, "alk"), 10), (K(b_hc, "wurtz"), 3), (T(C.c_name), 7)]), ("Combustion", [(T(C.c_formula, "comb"), 8), (K(b_hc, "aneO2", "eneO2", "yneO2"), 12)]),
                    ("Alkenes", [(T(C.c_formula, "ene"), 8), (b[9], 5), (K(b_hc, "ene"), 2), (T(C.c_name), 5)]), ("Alkynes", [(K(b_hc, "yne"), 8), (b[9], 3), (K(b_hc, "yneO2"), 4), (T(C.c_formula, "alk", "ene"), 5)]),
                    ("Aromatic hydrocarbons and mixed problems", [(b[9], 5), (T(C.c_name), 8), (T(C.c_formula, "comb"), 7)])]),
    ]


def K(f, *kinds):
    return lambda: f(ch(kinds))
