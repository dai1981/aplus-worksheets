# -*- coding: utf-8 -*-
"""
US High School Chemistry: Chemical Equilibrium (HS-PS1-6)
  python tools/gen_us_science_chem_chemical_equilibrium.py
Refine the design of a chemical system by specifying a change in conditions that would produce increased amounts of
products at equilibrium.
Reversible reactions, dynamic equilibrium (equal forward and reverse rates), reading when equilibrium is reached, and
Le Chatelier's principle for concentration, temperature and pressure changes (one change at a time, no K calculations,
as in the NGSS assessment boundary).
Wrong answers come from real mistakes: "at equilibrium the reaction stops", "at equilibrium amounts are equal",
"a catalyst makes more product", "heating always shifts to the right".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import sub

U = Unit(90211)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def side(t):
    out = []
    for p in t.split(" + "):
        st = ""
        if p.endswith(")"):
            p, st = p[:-3], p[-3:]
        i = 0
        while i < len(p) and p[i].isdigit():
            i += 1
        out.append(p[:i] + sub(p[i:]) + st)
    return " + ".join(out)


# equation (left, right), ΔH kJ, gas moles left, gas moles right, names of a reactant and a product, context
EQ = [("N2 + 3H2", "2NH3", -92, 4, 2, "N2", "NH3", "making ammonia (Haber process)"), ("2SO2 + O2", "2SO3", -198, 3, 2, "O2", "SO3", "making sulfuric acid (contact process)"),
      ("N2O4", "2NO2", 57, 1, 2, "N2O4", "NO2", "a brown gas mixture"), ("CO + 2H2", "CH3OH", -91, 3, 1, "H2", "CH3OH", "making methanol"),
      ("CaCO3(s)", "CaO(s) + CO2", 178, 0, 1, None, "CO2", "a lime kiln"), ("N2 + O2", "2NO", 181, 2, 2, "O2", "NO", "a hot car engine"),
      ("CO + H2O", "CO2 + H2", -41, 2, 2, "H2O", "H2", "making hydrogen"), ("PCl5", "PCl3 + Cl2", 88, 1, 2, "PCl5", "Cl2", "a closed flask of PCl₅"),
      ("H2 + I2", "2HI", -9, 2, 2, "H2", "HI", "a sealed tube of hydrogen and iodine")]
CHG = ["add reactant", "remove product", "add product", "remove reactant", "heat", "cool", "raise pressure", "lower pressure", "add catalyst"]
DIRS = ["shifts toward the products (right)", "shifts toward the reactants (left)", "no shift"]


def shift(e, c):
    _, _, dh, gl, gr, rx, px, _ = e
    if c == "add reactant" or c == "remove product":
        return 0
    if c == "add product" or c == "remove reactant":
        return 1
    if c in ("heat", "cool"):
        endo = dh > 0
        return 0 if (c == "heat") == endo else 1
    if c in ("raise pressure", "lower pressure"):
        if gl == gr:
            return 2
        fewer_right = gr < gl
        return 0 if (c == "raise pressure") == fewer_right else 1
    return 2


def ctext(e, c):
    rx, px = e[5] or "CaCO3", e[6]
    return {"add reactant": "More %s is added." % sub(rx), "remove product": "Some %s is removed." % sub(px), "add product": "More %s is added." % sub(px),
            "remove reactant": "Some %s is removed." % sub(rx), "heat": "The temperature is raised.", "cool": "The temperature is lowered.",
            "raise pressure": "The pressure is increased (the container is made smaller).", "lower pressure": "The pressure is decreased (the container is made larger).",
            "add catalyst": "A catalyst is added."}[c]


def why(e, c):
    if c.startswith("add") and c != "add catalyst" or c.startswith("remove"):
        return "The system shifts to use up what was added or replace what was removed."
    if c in ("heat", "cool"):
        return "ΔH = %s%d kJ, so the forward reaction is %s. %s favors the %s direction." % ("+" if e[2] > 0 else "−", abs(e[2]), "endothermic" if e[2] > 0 else "exothermic",
                                                                                 "Heating" if c == "heat" else "Cooling", "endothermic" if c == "heat" else "exothermic")
    if c == "add catalyst":
        return "A catalyst speeds up both directions equally, so it does not shift equilibrium."
    if e[3] == e[4]:
        return "Both sides have %d mol of gas, so pressure has no effect." % e[3]
    return "Left: %d mol gas, right: %d mol gas. Higher pressure favors fewer gas moles; lower pressure favors more." % (e[3], e[4])


def eqtxt(e):
    dh = e[2]
    return "%s ⇌ %s, ΔH = %s%d kJ" % (side(e[0]), side(e[1]), "+" if dh > 0 else "−", abs(dh))


def g_shift():
    e = R.choice(EQ)
    c = R.choice(CHG)
    if (c in ("add reactant", "remove reactant") and not e[5]) or not once(("sh", e[0], c)):
        return None
    d = shift(e, c)
    return item("In %s: %s. %s How does the equilibrium respond?" % (e[7], eqtxt(e), ctext(e, c)), DIRS[d], [x for x in DIRS if x != DIRS[d]] + ["the reaction stops"], why(e, c))


def g_more():
    e = R.choice([x for x in EQ if x[5]])
    good = [c for c in CHG if shift(e, c) == 0 and c not in ("add reactant", "remove product")]
    bad = [c for c in CHG if shift(e, c) != 0 and c not in ("add product", "remove reactant")]
    if not good or len(bad) < 3:
        return None
    c = R.choice(good)
    if not once(("mo", e[0], c)):
        return None
    w = R.sample(bad, 3)
    return item("An engineer wants more %s from %s: %s. Which single change increases the amount of %s at equilibrium?" % (sub(e[6]), e[7], eqtxt(e), sub(e[6])), ctext(e, c),
                [ctext(e, x) for x in w], why(e, c))


def g_reach():
    who = P.next()[0]
    t = [0, 10, 20, 30, 40, 50]
    k = R.randint(2, 4)
    a0 = R.choice([1.0, 0.8, 1.2, 0.6])
    end = round(a0 * R.choice([0.3, 0.4, 0.5, 0.6]), 2)
    va = []
    for i in range(6):
        va.append(end if i >= k else round(a0 - (a0 - end) * (i / k) ** 0.6, 2))
    vb = [round((a0 - x) * 2, 2) for x in va]
    q = R.choice(["when", "rates", "amount"])
    if not once(("rc", a0, end, k, q)) or len(set(va[:k + 1])) < k + 1:
        return None
    tab = table(["Time (min)", "[N₂O₄] (mol/L)", "[NO₂] (mol/L)"], [[str(a), "%.2f" % x, "%.2f" % y] for a, x, y in zip(t, va, vb)])
    if q == "when":
        return item(tab + "%s follows N<sub>2</sub>O<sub>4</sub> ⇌ 2NO<sub>2</sub> in a sealed flask. When is equilibrium first reached?" % who, "%d min" % t[k],
                    ["%d min" % t[0], "%d min" % t[5], "%d min" % t[k - 1]], "After %d min the concentrations stop changing." % t[k])
    if q == "rates":
        return item(tab + "In %s's flask after %d min, how do the forward and reverse rates compare?" % (who, t[5]), "They are equal.", ["The forward rate is zero.", "The reverse rate is zero.", "The forward rate is much faster."],
                    "Concentrations are constant because the two rates are equal (dynamic equilibrium).")
    return item(tab + "At equilibrium in %s's flask, what is the concentration of NO<sub>2</sub>?" % who, "%.2f mol/L" % vb[5], ["%.2f mol/L" % va[5], "%.2f mol/L" % vb[1], "0.00 mol/L"],
                "Read the value once it stops changing.")


B1 = bank([
    ("What is a reversible reaction?", "a reaction that can go forward and backward", ["a reaction that only goes forward", "a reaction that never happens", "a nuclear reaction"], "Symbol ⇌."),
    ("What is true at chemical equilibrium?", "The forward and reverse reactions happen at the same rate.", ["Both reactions have stopped.", "Reactants and products are always equal in amount.", "Only products are present."],
     "Dynamic equilibrium."),
    ("At equilibrium, what happens to the concentrations?", "They stay constant (but are not necessarily equal).", ["They keep changing.", "They become zero.", "They are always equal."], "Steady amounts."),
    ("What does Le Chatelier's principle say?", "A system at equilibrium shifts to reduce the effect of a change.", ["A system ignores changes.", "A system always shifts right.", "Equilibrium can never change."], "Counteracts the stress."),
    ("Why must the system be closed for equilibrium?", "So no reactants or products can escape.", ["So it stays cold.", "So light gets in.", "So the catalyst works."], "Sealed container."),
    ("What does a catalyst do to a system at equilibrium?", "It makes equilibrium reach faster but does not shift it.", ["It shifts it to the right.", "It shifts it to the left.", "It stops the reaction."], "Both rates sped up."),
    ("If the forward reaction is exothermic, what does heating do?", "shifts the equilibrium toward the reactants", ["shifts it toward the products", "has no effect", "stops the reaction"], "Heat is like a product."),
    ("Increasing pressure on a gas reaction favors which side?", "the side with fewer moles of gas", ["the side with more moles of gas", "neither side", "the side with solids"], "Fewer particles, less pressure."),
])
B5 = bank([
    ("The Haber process is exothermic, yet factories run it at about 450 °C. Why?", "At low temperature the reaction is too slow; 450 °C is a compromise between rate and yield.",
     ["High temperature increases the yield.", "Ammonia needs to be hot.", "It is cheaper to heat."], "Rate vs yield."),
    ("Why does the Haber process use high pressure (about 200 atm)?", "4 mol of gas form 2 mol, so high pressure shifts toward ammonia.", ["To speed up the catalyst only.", "Ammonia is a solid.", "Pressure has no effect."], "Fewer gas moles."),
    ("Factories remove ammonia as it forms. Why?", "Removing product shifts the equilibrium to make more ammonia.", ["To stop the reaction.", "It is too heavy.", "To make it reversible."], "Le Chatelier."),
    ("A sealed bottle of soda has CO₂ dissolved. Why does it fizz when opened?", "Lower pressure shifts the equilibrium toward CO₂ gas.", ["Opening adds CO₂.", "The soda gets hotter.", "A catalyst escapes."], "Pressure change."),
    ("A student says equilibrium means 50% reactants and 50% products. What is correct?", "Equilibrium means constant amounts and equal rates, not equal amounts.", ["The student is right.", "Equilibrium means no reaction.", "Equilibrium means only products."], "Common misconception."),
])


def body():
    think = ("<p><b>At equilibrium, forward and reverse rates are equal.</b></p>"
             "<ul><li>Amounts stay constant but are usually not equal. The reaction keeps going both ways.</li>"
             "<li>Le Chatelier: add reactant or remove product → shift right. Heat favors the endothermic direction. Higher pressure favors fewer gas moles.</li>"
             "<li>A catalyst speeds up both directions; it does not change how much product forms.</li></ul>")
    ex = [("N<sub>2</sub> + 3H<sub>2</sub> ⇌ 2NH<sub>3</sub>, ΔH = −92 kJ. Heat it?", ["Forward is exothermic", "Heat favors endothermic (left)"], "shifts left"),
          ("Same reaction, raise pressure?", ["4 gas moles → 2 gas moles"], "shifts right")]
    mist = ["Thinking the reaction stops at equilibrium.", "Thinking amounts are equal at equilibrium.", "Thinking a catalyst makes more product."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Dynamic equilibrium", B1 + [(g_reach, 6), (g_shift, 6)]),
        ("Reaching equilibrium", [(g_reach, 10), (g_shift, 10)]),
        ("Le Chatelier's principle", [(g_shift, 20)]),
        ("Temperature and pressure", [(g_shift, 14), (g_more, 6)]),
        ("Designing for more product", B5 + [(g_more, 3), (g_shift, 7), (g_reach, 5)]),
    ])
    make("chemistry", "chemical-equilibrium", 11, "HS-PS1-6",
         "Refine the design of a chemical system by specifying a change in conditions that would produce increased amounts of products at equilibrium.",
         "Chemical Equilibrium",
         "Equilibrium Worksheets: Le Chatelier's Principle and the Haber Process (High School Chemistry)",
         "Equilibrium",
         "Free high school chemistry worksheets on chemical equilibrium (NGSS HS-PS1-6): reversible reactions, dynamic equilibrium and Le Chatelier's principle for concentration, temperature and pressure. 100 questions with answers.",
         "Forward rate = reverse rate.",
         "Change one condition and the system shifts to reduce the change.",
         body(),
         [("What is dynamic equilibrium?", "A state in a closed system where the forward and reverse reactions happen at the same rate, so the amounts stay constant."),
          ("How do you get more product at equilibrium?", "Add reactant, remove product, change the temperature toward the side that favors products, or change the pressure for gas reactions."),
          ("Does a catalyst shift equilibrium?", "No. It speeds up the forward and reverse reactions equally, so the system reaches equilibrium faster but the amounts do not change.")],
         sets)


if __name__ == "__main__":
    main()
