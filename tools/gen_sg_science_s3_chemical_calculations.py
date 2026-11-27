# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 4: Chemical Calculations
  python tools/gen_sg_science_s3_chemical_calculations.py
Relative atomic and molecular mass (Ar, Mr), percentage composition by mass, the mole and the Avogadro constant (6 × 10²³),
molar gas volume (24 dm³ at room temperature and pressure), concentration in mol/dm³ and g/dm³, reacting masses and gas
volumes from balanced equations, titration calculations, empirical and molecular formulae, percentage yield and purity.
US mole makers are reused for practice (Singapore names); the rest are worked out here with O-Level relative atomic masses.
Wrong answers come from real mistakes: "using the mass instead of the moles", "forgetting the mole ratio in the equation",
"using cm³ as dm³", "percentage yield = theoretical ÷ actual".
"""
from math import gcd
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 16
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

AR = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "Al": 27, "S": 32, "Cl": 35.5, "K": 39, "Ca": 40, "Fe": 56, "Cu": 64, "Zn": 65}
CPD = [("water", "H2O", {"H": 2, "O": 1}), ("carbon dioxide", "CO2", {"C": 1, "O": 2}), ("sodium chloride", "NaCl", {"Na": 1, "Cl": 1}),
       ("calcium carbonate", "CaCO3", {"Ca": 1, "C": 1, "O": 3}), ("sulfuric acid", "H2SO4", {"H": 2, "S": 1, "O": 4}), ("sodium hydroxide", "NaOH", {"Na": 1, "O": 1, "H": 1}),
       ("magnesium oxide", "MgO", {"Mg": 1, "O": 1}), ("ammonia", "NH3", {"N": 1, "H": 3}), ("copper(II) sulfate", "CuSO4", {"Cu": 1, "S": 1, "O": 4}),
       ("methane", "CH4", {"C": 1, "H": 4}), ("iron(III) oxide", "Fe2O3", {"Fe": 2, "O": 3}), ("aluminium oxide", "Al2O3", {"Al": 2, "O": 3}),
       ("ammonium nitrate", "NH4NO3", {"N": 2, "H": 4, "O": 3}), ("calcium hydroxide", "Ca(OH)2", {"Ca": 1, "O": 2, "H": 2}), ("hydrochloric acid (HCl)", "HCl", {"H": 1, "Cl": 1}),
       ("glucose", "C6H12O6", {"C": 6, "H": 12, "O": 6}), ("sodium carbonate", "Na2CO3", {"Na": 2, "C": 1, "O": 3}), ("zinc chloride", "ZnCl2", {"Zn": 1, "Cl": 2})]


def fh(f):
    import re
    return re.sub(r"(\d+)", r"<sub>\1</sub>", f)


def mr(d):
    return sum(AR[e] * n for e, n in d.items())


ARTXT = lambda d: "(Ar: %s)" % ", ".join("%s = %s" % (e, ex(AR[e])) for e in d)


def g_mr():
    n, f, d = R.choice(CPD)
    M = mr(d)
    k = R.choice(["mr", "mr", "pct"])
    if k == "mr":
        wr = [sum(AR[e] for e in d), M + AR[list(d)[-1]], M - AR[list(d)[0]]]
        return nq("What is the relative molecular mass (Mr) of %s, %s? %s" % (n, fh(f), ARTXT(d)), M, wr, "", "Mr = " + " + ".join("%d × %s" % (c, ex(AR[e])) for e, c in d.items()) + " = %s." % ex(M))
    e = R.choice(list(d))
    p = AR[e] * d[e] / M * 100
    return nq("What is the percentage by mass of %s in %s, %s? %s" % (e, n, fh(f), ARTXT(d)), p, [AR[e] / M * 100, M / (AR[e] * d[e]), 100 - p], "%",
              "%% %s = %d × %s ÷ %s × 100%% = %s%%." % (e, d[e], ex(AR[e]), ex(M), nf(p)))


def g_mol():
    n, f, d = R.choice(CPD)
    M = mr(d)
    mol = R.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1.5, 2, 3])
    m = mol * M
    k = R.choice(["n", "m", "N"])
    if k == "n":
        return nq("How many moles are in %s g of %s, %s? (Mr = %s)" % (ex(m), n, fh(f), ex(M)), mol, [m * M, M / m, m / 100], " mol", "n = mass ÷ Mr = %s ÷ %s = %s mol." % (ex(m), ex(M), ex(mol)))
    if k == "m":
        return nq("What is the mass of %s mol of %s, %s? (Mr = %s)" % (ex(mol), n, fh(f), ex(M)), m, [mol / M, M / mol, M], " g", "mass = n × Mr = %s × %s = %s g." % (ex(mol), ex(M), nf(m)))
    return nq("How many molecules (or formula units) are in %s mol of %s? (Avogadro constant = 6 × 10²³ /mol)" % (ex(mol), n), mol * 6e23, [6e23 / mol, mol * 6e23 * 10, 6e23], "",
              "Number = n × 6 × 10²³ = %s × 6 × 10²³." % ex(mol), sf=2)


GASES = [("carbon dioxide", 44), ("oxygen", 32), ("hydrogen", 2), ("nitrogen", 28), ("ammonia", 17), ("methane", 16), ("chlorine", 71), ("sulfur dioxide", 64)]


def g_gas():
    g, M = R.choice(GASES)
    mol = R.choice([0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.5, 2])
    k = R.choice(["V", "V", "n", "m"])
    if k == "V":
        return nq("What volume does %s mol of %s occupy at room temperature and pressure? (1 mol of gas occupies 24 dm³ at r.t.p.)" % (ex(mol), g), mol * 24, [24 / mol, mol * 22.4, mol * 24000], " dm³",
                  "V = n × 24 = %s × 24 = %s dm³." % (ex(mol), ex(mol * 24)))
    if k == "n":
        V = mol * 24000
        return nq("How many moles of %s are in %s cm³ of the gas at r.t.p.? (molar volume = 24 dm³)" % (g, ex(V)), mol, [V / 24, V * 24 / 1000, 24 / V], " mol",
                  "%s cm³ = %s dm³; n = %s ÷ 24 = %s mol." % (ex(V), ex(V / 1000), ex(V / 1000), ex(mol)))
    m = mol * M
    return nq("What is the volume at r.t.p. of %s g of %s? (Mr = %d; molar volume = 24 dm³)" % (ex(m), g, M), mol * 24, [m * 24, m / M, 24 / mol], " dm³",
              "n = %s ÷ %d = %s mol; V = %s × 24 = %s dm³." % (ex(m), M, ex(mol), ex(mol), ex(mol * 24)))


def g_conc():
    sol = R.choice([("sodium hydroxide", 40), ("sodium chloride", 58.5), ("hydrochloric acid", 36.5), ("sulfuric acid", 98), ("copper(II) sulfate", 160)])
    n, M = sol
    c = R.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1, 2])
    V = R.choice([25, 50, 100, 200, 250, 500])
    mol = c * V / 1000
    k = R.choice(["c", "n", "g", "V"])
    if k == "c":
        return nq("%s mol of %s is dissolved to make %d cm³ of solution. What is its concentration?" % (ex(mol), n, V), c, [mol / V, mol * V, mol * 1000 * V], " mol/dm³",
                  "%d cm³ = %s dm³; c = %s ÷ %s = %s mol/dm³." % (V, ex(V / 1000), ex(mol), ex(V / 1000), ex(c)))
    if k == "n":
        return nq("How many moles of %s are in %d cm³ of a %s mol/dm³ solution?" % (n, V, ex(c)), mol, [c * V, c / V, V / c / 1000], " mol", "n = c × V = %s × %s = %s mol." % (ex(c), ex(V / 1000), ex(mol)))
    if k == "g":
        return nq("A solution of %s has a concentration of %s mol/dm³. What is its concentration in g/dm³? (Mr = %s)" % (n, ex(c), ex(M)), c * M, [c / M, M / c, c * M / 1000], " g/dm³",
                  "g/dm³ = mol/dm³ × Mr = %s × %s = %s g/dm³." % (ex(c), ex(M), nf(c * M)))
    return nq("What volume of %s mol/dm³ %s contains %s mol?" % (ex(c), n, ex(mol)), V, [mol / c, mol * c * 1000, c / mol], " cm³", "V = n ÷ c = %s ÷ %s = %s dm³ = %d cm³." % (ex(mol), ex(c), ex(mol / c), V))


RX = [("Mg + 2HCl → MgCl₂ + H₂", "magnesium", 24, "hydrogen", 2, 1, 1, True),
      ("CaCO₃ → CaO + CO₂", "calcium carbonate", 100, "carbon dioxide", 44, 1, 1, True),
      ("2Mg + O₂ → 2MgO", "magnesium", 24, "magnesium oxide", 40, 2, 2, False),
      ("Zn + H₂SO₄ → ZnSO₄ + H₂", "zinc", 65, "hydrogen", 2, 1, 1, True),
      ("CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂", "calcium carbonate", 100, "carbon dioxide", 44, 1, 1, True),
      ("2H₂O₂ → 2H₂O + O₂", "hydrogen peroxide", 34, "oxygen", 32, 2, 1, True),
      ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", "iron(III) oxide", 160, "iron", 56, 1, 2, False),
      ("CuO + H₂ → Cu + H₂O", "copper(II) oxide", 80, "copper", 64, 1, 1, False)]


def g_react():
    eq, a, Ma, b, Mb, na, nb, gas = R.choice(RX)
    mol_a = R.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1, 2])
    ma = mol_a * Ma
    mol_b = mol_a * nb / na
    if gas and R.random() < 0.5:
        V = mol_b * 24
        return nq("%s. What volume of %s at r.t.p. is made from %s g of %s? (Mr/Ar: %s = %s; molar volume 24 dm³)" % (eq, b, ex(ma), a, a, ex(Ma)), V,
                  [mol_a * 24 * (na / nb if na != nb else 2), ma * 24, ma / Ma], " dm³",
                  "n(%s) = %s ÷ %s = %s mol; n(%s) = %s mol; V = %s × 24 = %s dm³." % (a, ex(ma), ex(Ma), ex(mol_a), b, ex(mol_b), ex(mol_b), ex(V)))
    mb = mol_b * Mb
    return nq("%s. What mass of %s is made from %s g of %s? (relative masses: %s = %s, %s = %s)" % (eq, b, ex(ma), a, a, ex(Ma), b, ex(Mb)), mb,
              [mol_a * Mb if nb != na else mol_a * Mb * 2, ma, mol_b * Ma], " g",
              "n(%s) = %s ÷ %s = %s mol; mole ratio %d : %d gives n(%s) = %s mol; mass = %s × %s = %s g." % (a, ex(ma), ex(Ma), ex(mol_a), na, nb, b, ex(mol_b), ex(mol_b), ex(Mb), nf(mb)))


TIT = [("NaOH + HCl → NaCl + H₂O", "sodium hydroxide", "hydrochloric acid", 1), ("2NaOH + H₂SO₄ → Na₂SO₄ + 2H₂O", "sodium hydroxide", "sulfuric acid", 0.5),
       ("Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂", "sodium carbonate", "hydrochloric acid", 2), ("KOH + HNO₃ → KNO₃ + H₂O", "potassium hydroxide", "nitric acid", 1)]


def g_tit():
    eq, base, acid, r = R.choice(TIT)
    Vb = R.choice([10.0, 20.0, 25.0])
    cb = R.choice([0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25])
    ca = R.choice([0.05, 0.1, 0.125, 0.2, 0.25, 0.5])
    nb = cb * Vb / 1000
    na = nb * r
    Va = na / ca * 1000
    if not (10 <= Va <= 45) or abs(Va * 20 - round(Va * 20)) > 1e-6:
        return None
    if R.random() < 0.5:
        return nq("%s. %.1f cm³ of %s mol/dm³ %s is exactly neutralised by %.2f cm³ of %s. What is the concentration of the %s?" % (eq, Vb, ex(cb), base, Va, acid, acid), ca,
                  [nb / Va * 1000, cb * Va / Vb, ca * (r if r != 1 else 2)], " mol/dm³",
                  "n(%s) = %s × %s = %s mol; n(acid) = %s mol; c = %s ÷ %s = %s mol/dm³." % (base, ex(cb), ex(Vb / 1000), ex(nb), ex(na), ex(na), ex(Va / 1000), ex(ca)))
    return nq("%s. What volume of %s mol/dm³ %s exactly neutralises %.1f cm³ of %s mol/dm³ %s?" % (eq, ex(ca), acid, Vb, ex(cb), base), Va,
              [Vb * cb / ca, Va * 2 if r != 2 else Va / 2, nb * 1000], " cm³", "n(%s) = %s mol; n(acid) = %s mol; V = %s ÷ %s = %s dm³ = %s cm³." % (base, ex(nb), ex(na), ex(na), ex(ca), ex(Va / 1000), ex(Va)))


EMP = [({"C": 1, "H": 2}, "CH₂"), ({"C": 1, "H": 3}, "CH₃"), ({"Mg": 1, "O": 1}, "MgO"), ({"Fe": 2, "O": 3}, "Fe₂O₃"), ({"C": 1, "H": 4}, "CH₄"), ({"N": 1, "O": 2}, "NO₂"),
       ({"Cu": 1, "O": 1}, "CuO"), ({"Cu": 2, "O": 1}, "Cu₂O"), ({"S": 1, "O": 3}, "SO₃"), ({"Al": 2, "O": 3}, "Al₂O₃"), ({"C": 1, "H": 1}, "CH"), ({"Na": 2, "S": 1, "O": 4}, "Na₂SO₄")]


def g_emp():
    d, f = R.choice(EMP)
    scale = R.choice([0.1, 0.2, 0.5, 1])
    masses = {e: AR[e] * n * scale for e, n in d.items()}
    tot = sum(masses.values())
    if R.random() < 0.5:
        txt = ", ".join("%s g of %s" % (ex(round(m, 2)), e) for e, m in masses.items())
        q = "A compound contains %s. What is its empirical formula? %s" % (txt, ARTXT(d))
    else:
        txt = ", ".join("%s%% %s" % (nf(m / tot * 100), e) for e, m in masses.items())
        q = "A compound contains %s by mass. What is its empirical formula? %s" % (txt, ARTXT(d))
    wr = [x[1] for x in EMP if set(x[0]) == set(d) and x[1] != f]
    swap = "".join("%s%s" % (e, "" if n == 1 else str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))) for e, n in zip(d, list(d.values())[::-1]))
    wr += [swap, "".join(e for e in d)]
    wr = [w for w in dict.fromkeys(wr) if w != f]
    if len(wr) < 3:
        wr.append("".join("%s%s" % (e, "₂") for e in d))
    return tq(q, f, wr[:3], "Divide each mass (or %) by Ar, then divide by the smallest number to get the simplest whole-number ratio: " + f + ".")


def g_yield():
    k = R.choice(["yield", "pure"])
    th = R.choice([10, 12, 20, 24, 40, 50, 80, 120])
    p = R.choice([40, 50, 60, 75, 80, 85, 90])
    act = th * p / 100
    if k == "yield":
        return nq("The theoretical yield of a product is %s g, but only %s g is obtained. What is the percentage yield?" % (ex(th), ex(act)), p, [th / act * 100, 100 - p, act], "%",
                  "% yield = actual ÷ theoretical × 100% = " + "%s ÷ %s × 100%% = %d%%." % (ex(act), ex(th), p))
    return nq("A %s g sample of impure limestone contains %s g of calcium carbonate. What is its percentage purity?" % (ex(th), ex(act)), p, [th / act * 100, 100 - p, act / 100], "%",
              "% purity = mass of pure substance ÷ mass of sample × 100% = " + "%s ÷ %s × 100%% = %d%%." % (ex(act), ex(th), p))


POOL1 = pool(R, [
    ("What is the relative atomic mass (Ar) of an element?", "the average mass of its atoms compared with 1/12 of the mass of a carbon-12 atom", ["the number of protons", "the mass of one atom in grams", "the number of neutrons"], "Ar has no units."),
    ("What is one mole of a substance?", "the amount containing 6 × 10²³ particles", ["the mass of one atom", "1 g of any substance", "24 g of any gas"], "The Avogadro constant."),
    ("What is the molar mass of carbon dioxide (C = 12, O = 16)?", "44 g/mol", ["28 g/mol", "44 g", "22 g/mol"], "12 + 2 × 16."),
    ("What volume does 1 mol of any gas occupy at room temperature and pressure?", "24 dm³", ["22.4 cm³", "1 dm³", "24 cm³"], "24 dm³ = 24 000 cm³."),
    ("How do you convert a volume in cm³ to dm³?", "divide by 1000", ["multiply by 1000", "divide by 100", "multiply by 24"], "1 dm³ = 1000 cm³."),
    ("What does a concentration of 2 mol/dm³ mean?", "2 mol of solute in every 1 dm³ of solution", ["2 g of solute per dm³", "2 dm³ of solute", "2 mol of solvent"], "c = n ÷ V."),
    ("What is an empirical formula?", "the simplest whole-number ratio of atoms of each element in a compound", ["the actual number of atoms in a molecule", "the mass of one mole", "the structure of a molecule"], "Glucose C₆H₁₂O₆ has empirical formula CH₂O."),
    ("The empirical formula of a compound is CH₂ and its Mr is 56. What is its molecular formula?", "C₄H₈", ["CH₂", "C₂H₄", "C₅H₁₀"], "CH₂ = 14; 56 ÷ 14 = 4."),
    ("Why is the actual yield usually less than the theoretical yield?", "Some product is lost during separation, or the reaction is incomplete or has side reactions.", ["Mass is destroyed in reactions.", "The equation is always wrong.", "Products gain mass."], "% yield = actual ÷ theoretical × 100%."),
    ("In 2H₂ + O₂ → 2H₂O, what is the mole ratio of hydrogen to water?", "1 : 1", ["2 : 1", "1 : 2", "2 : 3"], "2 mol H₂ make 2 mol H₂O."),
])
POOL5 = pool(R, [
    ("12 g of magnesium burns in oxygen: 2Mg + O₂ → 2MgO. What mass of magnesium oxide forms? (Mg = 24, O = 16)", "20 g", ["24 g", "40 g", "10 g"], "0.5 mol Mg → 0.5 mol MgO × 40 g/mol."),
    ("What mass of sodium hydroxide is needed to make 250 cm³ of 0.2 mol/dm³ solution? (Mr = 40)", "2 g", ["8 g", "50 g", "0.05 g"], "n = 0.2 × 0.25 = 0.05 mol; 0.05 × 40."),
    ("10.0 g of calcium carbonate is heated. What volume of carbon dioxide forms at r.t.p.? (CaCO₃ = 100)", "2.4 dm³", ["24 dm³", "0.1 dm³", "4.4 dm³"], "0.1 mol CaCO₃ → 0.1 mol CO₂ × 24."),
    ("Which contains the most molecules?", "2 g of hydrogen (H₂)", ["16 g of oxygen (O₂)", "14 g of nitrogen (N₂)", "22 g of carbon dioxide"], "2 g H₂ is 1 mol; the others are 0.5 mol."),
    ("Which gas sample has the largest volume at r.t.p.?", "4 g of hydrogen (H₂, Mr = 2)", ["32 g of oxygen (O₂, Mr = 32)", "28 g of nitrogen (N₂, Mr = 28)", "44 g of carbon dioxide (Mr = 44)"], "4 g of H₂ is 2 mol (48 dm³); each of the others is 1 mol (24 dm³)."),
    ("A student's yield is 112%. What is the most likely reason?", "The product was still wet or impure when weighed.", ["Mass was created.", "The reaction was very fast.", "The theoretical yield was too large."], "A yield over 100% means extra mass."),
    ("How many atoms are in 1 mol of water molecules?", "1.8 × 10²⁴", ["6 × 10²³", "3", "1.2 × 10²⁴"], "Each H₂O has 3 atoms: 3 × 6 × 10²³."),
    ("0.1 mol of a metal M reacts to give 0.05 mol of M₂O₃. Which is the correct mole ratio of M to M₂O₃?", "2 : 1", ["1 : 1", "1 : 2", "3 : 2"], "Two M atoms per formula unit."),
])


def main():
    sets = U.sets([
        ("Relative masses and percentage composition", [(g_mr, 10), POOL1, (g_emp, 4)]),
        ("The mole and molar gas volume", [(g_mol, 9), (g_gas, 8), POOL1]),
        ("Concentration and titration", [(g_conc, 9), (g_tit, 8), POOL1]),
        ("Reacting masses and formulae", [(g_react, 10), (g_emp, 6), (g_yield, 4)]),
        ("Exam-style questions", [(POOL5, 8), (g_react, 4), (g_tit, 3), (g_yield, 3), (g_gas, 2)]),
    ])
    make_ol(LV, SUBJ, "chemical-calculations", SORT, "Chemical Calculations",
            "Construct and use word, formula and ionic equations; define relative atomic mass and relative molecular mass and calculate Mr and percentage composition; "
            "use the mole concept and the Avogadro constant; use the molar gas volume of 24 dm³ at room temperature and pressure; calculate concentrations in mol/dm³ and "
            "g/dm³ and solve titration problems; calculate reacting masses and volumes of gases from balanced equations; deduce empirical and molecular formulae; "
            "calculate percentage yield and percentage purity (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Chemical Calculations", "Chemical calculations",
            "Free Secondary 3 O-Level Chemistry worksheets on chemical calculations: Mr, percentage composition, moles, molar gas volume, concentration, titrations, reacting "
            "masses, empirical formulae and percentage yield. 100 questions with answers.",
            "moles = mass ÷ Mr", "Gas: 24 dm³ per mol. Solution: n = c × V (in dm³).",
            "<p><b>Work in moles, then use the mole ratio from the balanced equation.</b></p><ul>"
            "<li>n = mass ÷ Mr; number of particles = n × 6 × 10²³.</li>"
            "<li>Gases at r.t.p.: V (dm³) = n × 24. Solutions: n = c × V, with V in dm³ (cm³ ÷ 1000).</li>"
            "<li>Reacting masses: mass → moles → use the equation's ratio → moles → mass or volume.</li>"
            "<li>Empirical formula: divide each mass by Ar, then by the smallest. % yield = actual ÷ theoretical × 100%.</li></ul>",
            [("Moles in 4.0 g of NaOH (Mr 40)?", ["4.0 ÷ 40"], "0.10 mol"),
             ("Volume of 0.25 mol of CO₂ at r.t.p.?", ["0.25 × 24"], "6.0 dm³"),
             ("25.0 cm³ of 0.1 mol/dm³ NaOH neutralises 20.0 cm³ of HCl. c(HCl)?", ["n = 0.0025 mol", "0.0025 ÷ 0.0200"], "0.125 mol/dm³")],
            ["Forgetting to use the mole ratio from the equation.", "Using a volume in cm³ in n = c × V without dividing by 1000.",
             "Calculating % yield as theoretical ÷ actual.", "Using the mass instead of moles when comparing reactants."],
            [("How do you calculate the number of moles?", "For a solid or liquid, divide the mass in grams by Mr. For a gas at r.t.p., divide the volume in dm³ by 24. For a solution, multiply concentration (mol/dm³) by volume (dm³)."),
             ("How do you do a reacting mass calculation?", "Change the given mass into moles, use the ratio in the balanced equation to find the moles of the other substance, then change back into mass (or volume)."),
             ("How do you find an empirical formula?", "Divide the mass (or percentage) of each element by its Ar, divide by the smallest answer, and round to the simplest whole-number ratio.")],
            sets)


if __name__ == "__main__":
    main()
