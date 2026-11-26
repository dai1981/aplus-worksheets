# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Chemistry): Quantitative Chemistry
  python tools/gen_uk_science_y10_quantitative_chemistry.py
Conservation of mass and balanced symbol equations, relative formula mass (Mr), mass changes when a reactant or
product is a gas, moles (mass = Mr × moles), reacting masses and the concentration of solutions in g/dm³.
Reuses the balancing, mole and reacting-mass questions of the US Chemistry units in British English.
Wrong answers come from real mistakes: "mass is lost when a gas is made", "Mr of H₂O = 1 + 16",
"cm³ and dm³ are the same", "moles = Mr ÷ mass".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build
from sci_chem import AM, molar, num, sub
from sci_phys import uniq

U, R, P, us = U4(62007)
BAL = "chem_balancing_chemical_equations"
MO = "chem_the_mole_and_molar_mass"
ST = "chem_stoichiometry"
us_check, us_count, us_bmass, us_miss = [us(BAL, "g_" + n) for n in ("check", "count", "mass", "missing")]
us_g2mol, us_mol2g, us_mm = us(MO, "g_g2mol"), us(MO, "g_mol2g"), us(MO, "g_mm")
us_smass = us(ST, "g_mass", drop=("limiting", "yield"))

FORM = ["H2O", "CO2", "NaCl", "MgO", "CaCO3", "H2SO4", "NaOH", "CH4", "NH3", "CuO", "HCl", "Ca(OH)2", "MgCl2", "Na2CO3", "C2H6", "KCl", "Al2O3", "Fe2O3", "SO2", "O2"]


def g_mr():
    f = R.choice(FORM)
    if not once(("mr", f)):
        return None
    m = molar(f)
    g = num(m)
    els = sorted(set(k for k in AM if k in f))
    wrong = [num(sum(AM[e] for e in els)), num(m + 16), num(m - 1), num(m * 2), num(m + AM.get(els[0], 1))]
    return item("Using relative atomic masses (H = 1, C = 12, N = 14, O = 16, Na = 23, Mg = 24, Al = 27, S = 32, Cl = 35.5, K = 39, Ca = 40, Fe = 56, Cu = 63.5), what is the relative formula mass (Mr) of %s?" % sub(f), g,
                uniq(g, wrong), "Add the relative atomic masses of every atom in the formula.")


def g_conc():
    k = R.choice(["c", "m", "v"])
    vol = R.choice([100, 200, 250, 500, 1000, 2000])
    c = R.choice([2, 4, 5, 8, 10, 20, 25, 40, 50])
    m = c * vol / 1000
    if m != int(m) and m * 10 != int(m * 10) or not once(("co", k, vol, c)):
        return None
    ms, vs = num(m), "{:,}".format(vol)
    if k == "c":
        g = "%d g/dm³" % c
        return item("%s g of salt is dissolved to make %s cm³ of solution. What is the concentration in g/dm³?" % (ms, vs), g,
                    uniq(g, ["%s g/dm³" % num(m / vol), "%s g/dm³" % num(m * vol), "%s g/dm³" % ms, "%s g/dm³" % num(c * 10)]), "%s cm³ = %s dm³. %s ÷ %s = %d g/dm³." % (vs, num(vol / 1000), ms, num(vol / 1000), c))
    if k == "m":
        g = "%s g" % ms
        return item("What mass of solute is in %s cm³ of %s %d g/dm³ solution?" % (vs, "an" if c in (8, 18, 80) else "a", c), g, uniq(g, ["{:,} g".format(c * vol), "%s g" % num(c / (vol / 1000)), "%d g" % c, "%s g" % num(m * 10)]), "mass = concentration × volume = %d × %s dm³." % (c, num(vol / 1000)))
    g = "%s cm³" % vs
    return item("What volume of %s %d g/dm³ solution contains %s g of solute? Give your answer in cm³." % ("an" if c in (8, 18, 80) else "a", c, ms), g, uniq(g, ["%s cm³" % num(m * c), "%s cm³" % num(vol / 1000), "%s cm³" % num(vol * 10), "%s cm³" % num(vol / 10)]), "volume = %s ÷ %d = %s dm³ = %s cm³." % (ms, c, num(vol / 1000), vs))


def g_gas():
    who = P.next()[0]
    k = R.choice(["metal", "carb"])
    a = R.choice([2.4, 4.8, 1.2, 3.6, 6.0])
    if k == "metal":
        b = round(a * 40 / 24, 1)
        if not once(("ga", k, a)):
            return None
        return item("%s heats %s g of magnesium in a crucible. The magnesium oxide formed has a mass of %s g. Why has the mass increased?" % (who, num(a), num(b)), "Oxygen from the air has joined with the magnesium.",
                    ["Mass is created when things are heated.", "The crucible has melted.", "Magnesium has absorbed heat."], "Increase = %s g of oxygen." % num(b - a))
    m = R.choice([5.0, 10.0, 20.0, 25.0])
    if not once(("ga", k, m)):
        return None
    lost = num(m * 44 / 100)
    return item("%s heats %s g of calcium carbonate: CaCO₃ → CaO + CO₂. Afterwards the solid has lost %s g. Why?" % (who, num(m), lost), "Carbon dioxide gas escaped into the air.",
                ["Mass was destroyed.", "Calcium oxide evaporated.", "The scale was wrong."], "Conservation of mass: the gas left the open container.")


B1 = bank([
    ("What does the law of conservation of mass say?", "No atoms are lost or made in a reaction, so the mass of products equals the mass of reactants.", ["Mass always decreases in reactions.", "Mass always increases.", "Only gases have mass."], "Balanced equations show this."),
    ("What is the relative formula mass (Mr)?", "the sum of the relative atomic masses of the atoms in the formula", ["the number of atoms in the formula", "the mass of one electron", "the atomic number of the first element"], "No units."),
    ("How many particles are in one mole of a substance?", "6.02 × 10²³ (the Avogadro constant)", ["100", "6.02 × 10³", "1"], "Higher tier."),
    ("How do you convert cm³ to dm³?", "divide by 1,000", ["multiply by 1,000", "divide by 100", "multiply by 10"], "1 dm³ = 1,000 cm³."),
])
B5 = bank([
    ("What is the equation linking mass, Mr and moles?", "number of moles = mass ÷ Mr", ["moles = Mr ÷ mass", "moles = mass × Mr", "moles = mass + Mr"], "Higher tier."),
    ("Why might the mass of a reaction flask decrease during a reaction?", "A gas is made and escapes from the flask.", ["Atoms are destroyed.", "The flask evaporates.", "Mass cannot change."], "Open system."),
    ("What does a balanced symbol equation show?", "the same number of each type of atom on both sides", ["the same number of molecules on both sides", "only the products", "the temperature of the reaction"], "Conservation of atoms."),
    ("Why is a solution's concentration higher if the same mass is dissolved in less water?", "There is more solute in each dm³.", ["The solute disappears.", "Concentration does not depend on volume.", "Water makes more solute."], "Mass per volume."),
])

if __name__ == "__main__":
  build(U, 10, "quantitative-chemistry", 7, "Chemistry", "Quantitative chemistry",
      "Conservation of mass and balanced chemical equations; relative formula mass; mass changes when a reactant or product is a gas; chemical measurements and uncertainty; moles (higher tier) and amounts of substances in equations; using moles to balance equations; concentration of solutions in g/dm³.",
      "Quantitative Chemistry", "Quantitative Chemistry",
      "Free Year 10 GCSE Combined Science worksheets on quantitative chemistry: conservation of mass, balancing equations, relative formula mass, moles, reacting masses and concentration in g/dm³. 100 questions with answers.",
      "Mass of reactants = mass of products.",
      "Mr is the sum of the atomic masses; concentration = mass ÷ volume in dm³.",
      "<p><b>Atoms are not lost or made in a reaction.</b></p><ul><li>Balanced equations have the same number of each atom on both sides.</li>"
      "<li>Mr = the sum of the relative atomic masses. Moles = mass ÷ Mr.</li>"
      "<li>Concentration (g/dm³) = mass (g) ÷ volume (dm³). 1 dm³ = 1,000 cm³.</li></ul>",
      [("Mr of CO₂ (C = 12, O = 16)?", ["12 + 16 + 16"], "44"), ("10 g in 250 cm³. Concentration?", ["250 cm³ = 0.25 dm³", "10 ÷ 0.25"], "40 g/dm³")],
      ["Thinking mass is lost when a gas forms.", "Forgetting to multiply by the small numbers in a formula.", "Using cm³ instead of dm³ in concentration."],
      [("How do you calculate relative formula mass?", "Add up the relative atomic masses of all the atoms in the formula. For H₂SO₄: 2 × 1 + 32 + 4 × 16 = 98."),
       ("How do you calculate concentration?", "Divide the mass of solute in grams by the volume of solution in dm³. Convert cm³ to dm³ by dividing by 1,000."),
       ("Why does the mass change when magnesium burns?", "Oxygen from the air combines with the magnesium, so the product is heavier. The total mass of all the substances is still conserved.")],
      [("Conservation of mass", B1 + [(us_check, 6), (us_count, 6), (g_gas, 4)]),
       ("Relative formula mass", [(g_mr, 14), (us_mm, 6)]),
       ("Moles", [(us_g2mol, 8), (us_mol2g, 8), (us_miss, 4)]),
       ("Reacting masses", [(us_smass, 8), (us_bmass, 8), (g_gas, 4)]),
       ("Concentration", B5 + [(g_conc, 16)])])
