# -*- coding: utf-8 -*-
"""
US High School Chemistry: Balancing Chemical Equations (HS-PS1-7)
  python tools/gen_us_science_chem_balancing_chemical_equations.py
Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical
reaction.
Counting atoms in formulas with coefficients and parentheses; checking whether an equation is balanced; choosing and
finding coefficients; conservation of mass calculations.
Every equation in BAL is checked to be balanced when the script runs.
Wrong answers come from real mistakes: "change the subscripts to balance", "the coefficient multiplies only the first
atom", "mass is lost when a gas forms".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import sub, atoms, split_eq, tally, eq_html

U = Unit(90206)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


BAL = ["2H2 + O2 -> 2H2O", "N2 + 3H2 -> 2NH3", "2Na + Cl2 -> 2NaCl", "4Fe + 3O2 -> 2Fe2O3", "2Mg + O2 -> 2MgO", "4Al + 3O2 -> 2Al2O3", "2KClO3 -> 2KCl + 3O2",
       "CH4 + 2O2 -> CO2 + 2H2O", "C3H8 + 5O2 -> 3CO2 + 4H2O", "2C2H6 + 7O2 -> 4CO2 + 6H2O", "C6H12O6 + 6O2 -> 6CO2 + 6H2O", "6CO2 + 6H2O -> C6H12O6 + 6O2",
       "Zn + 2HCl -> ZnCl2 + H2", "2Al + 6HCl -> 2AlCl3 + 3H2", "2Na + 2H2O -> 2NaOH + H2", "Cu + 2AgNO3 -> Cu(NO3)2 + 2Ag", "Cl2 + 2KBr -> 2KCl + Br2",
       "CaCO3 -> CaO + CO2", "2H2O2 -> 2H2O + O2", "2HgO -> 2Hg + O2", "N2 + O2 -> 2NO", "2SO2 + O2 -> 2SO3", "P4 + 5O2 -> P4O10", "2K + Br2 -> 2KBr",
       "BaCl2 + Na2SO4 -> BaSO4 + 2NaCl", "Pb(NO3)2 + 2KI -> PbI2 + 2KNO3", "H2SO4 + 2NaOH -> Na2SO4 + 2H2O", "Fe2O3 + 3CO -> 2Fe + 3CO2", "C2H5OH + 3O2 -> 2CO2 + 3H2O",
       "2C4H10 + 13O2 -> 8CO2 + 10H2O", "3Ca(OH)2 + 2H3PO4 -> Ca3(PO4)2 + 6H2O", "Al2(SO4)3 + 6NaOH -> 2Al(OH)3 + 3Na2SO4", "2NaN3 -> 2Na + 3N2", "4NH3 + 5O2 -> 4NO + 6H2O"]
for e in BAL:
    l, r = split_eq(e)
    assert tally(l) == tally(r), e


def g_count():
    e = R.choice(BAL)
    l, r = split_eq(e)
    c, f = R.choice(l + r)
    a = atoms(f)
    el = R.choice(sorted(a))
    n = c * a[el]
    if not once(("ct", c, f, el)):
        return None
    term = ("%d" % c if c > 1 else "") + sub(f)
    w = [a[el], c + a[el], n + c, c, n * 2, sum(a.values()) * c]
    w = [str(x) for x in dict.fromkeys(w) if x != n and x > 0][:3]
    if len(w) < 3:
        return None
    return item("How many atoms of %s are in %s?" % (el, term), str(n), w,
                "%s: the coefficient %d multiplies every atom in the formula, so %d × %d = %d." % (term, c, c, a[el], n) if c > 1 else "Count the subscripts (including any outside parentheses): %d." % n)


def bad(e):
    """an unbalanced version: change one coefficient"""
    l, r = split_eq(e)
    s = l + r
    i = R.randrange(len(s))
    c, f = s[i]
    nc = R.choice([x for x in (1, 2, 3, 4) if x != c])
    s[i] = (nc, f)
    l2, r2 = s[:len(l)], s[len(l):]
    if tally(l2) == tally(r2):
        return None
    return l2, r2


def g_check():
    e = R.choice(BAL)
    k = R.random() < 0.5
    if not once(("ck", e, k)):
        return None
    if k:
        l, r = split_eq(e)
        return item("Is this equation balanced? %s" % eq_html(l, r), "Yes. Each element has the same number of atoms on both sides.",
                    ["No. There are more molecules on the right.", "No. The subscripts must match.", "It cannot be checked."], "Count each element on both sides.")
    b = bad(e)
    if not b:
        return None
    l, r = b
    tl, tr = tally(l), tally(r)
    el = [x for x in sorted(tl) if tl[x] != tr.get(x, 0)][0]
    return item("Is this equation balanced? %s" % eq_html(l, r), "No. %s has %d atoms on the left and %d on the right." % (el, tl[el], tr[el]),
                ["Yes. Each element is balanced.", "Yes. Both sides have the same elements.", "No. There are too many arrows."], "Count each element on both sides.")


def coef(e):
    l, r = split_eq(e)
    return [c for c, f in l + r]


def skel(e):
    l, r = split_eq(e)
    return eq_html([(1, f) for c, f in l], [(1, f) for c, f in r]).replace(" + ", " + ").replace("→", "→")


def g_pick():
    e = R.choice([x for x in BAL if max(coef(x)) > 1])
    if not once(("pk", e)):
        return None
    cs = coef(e)
    good = ", ".join(map(str, cs))
    w = set()
    for _ in range(30):
        x = list(cs)
        i = R.randrange(len(x))
        x[i] = max(1, x[i] + R.choice([-1, 1, 2]))
        if x != cs and [v * 2 for v in cs] != x:
            w.add(", ".join(map(str, x)))
    w.add(", ".join("1" for _ in cs))
    w = sorted(w - {good})
    if len(w) < 3:
        return None
    return item("Which coefficients (in order) balance this equation? %s" % skel(e), good, R.sample(w, 3), "Check: %s." % eq_html(*split_eq(e)))


def g_missing():
    e = R.choice([x for x in BAL if max(coef(x)) > 1])
    l, r = split_eq(e)
    s = l + r
    i = R.choice([j for j, (c, f) in enumerate(s) if c > 1] or [0])
    c, f = s[i]
    if not once(("ms", e, i)):
        return None
    shown = [(("?" if j == i else ("%d" % cc if cc > 1 else "")) + sub(ff)) for j, (cc, ff) in enumerate(s)]
    txt = " + ".join(shown[:len(l)]) + " → " + " + ".join(shown[len(l):])
    w = [str(x) for x in (1, 2, 3, 4, 5, 6, 8) if x != c]
    return item("What number replaces ? to balance the equation? %s" % txt, str(c), R.sample(w, 3), "Balanced: %s." % eq_html(l, r))


MR = [("iron", "sulfur", "iron sulfide", 7, 4), ("magnesium", "oxygen", "magnesium oxide", 3, 2), ("carbon", "oxygen", "carbon dioxide", 3, 8),
      ("hydrogen", "oxygen", "water", 1, 8), ("sodium", "chlorine", "sodium chloride", 23, 35.5), ("copper", "sulfur", "copper(I) sulfide", 4, 1)]


def g_mass():
    who = P.next()[0]
    k = R.choice(["prod", "react", "gas"])
    if k == "gas":
        m = R.randint(1, 12)
        t, a, b = 25 * m, 14 * m, 11 * m
        if not once(("ms", k, m)):
            return None
        return item("%s heats %d g of calcium carbonate in an open dish. It leaves %d g of calcium oxide. What mass of carbon dioxide gas escaped?" % (who, t, a), "%d g" % b,
                    ["0 g, because mass is lost", "%d g" % t, "%d g" % a], "Mass is conserved: %d − %d = %d g of gas." % (t, a, b))
    r = R.choice([x for x in MR if isinstance(x[4], int)])
    m = R.randint(2, 12)
    a, b = r[3] * m, r[4] * m
    if not once(("ms", k, r[0], m)):
        return None
    if k == "prod":
        return item("%s reacts %d g of %s with %d g of %s. Both are used up. What mass of %s forms?" % (who, a, r[0], b, r[1], r[2]), "%d g" % (a + b),
                    ["%d g" % abs(a - b), "%d g" % max(a, b), "%d g" % (a + b + 10)], "Mass is conserved: %d + %d = %d g." % (a, b, a + b))
    t = a + b
    return item("In %s's sealed flask, some %s reacts with %d g of %s and makes %d g of %s. What mass of %s reacted?" % (who, r[0], b, r[1], t, r[2], r[0]), "%d g" % a,
                ["%d g" % t, "%d g" % b, "%d g" % (t + b)], "%d − %d = %d g." % (t, b, a))


B1 = bank([
    ("Why must chemical equations be balanced?", "Atoms are not created or destroyed in a reaction.", ["To make the equation look neat.", "Because molecules must be equal.", "To make the products heavier."], "Conservation of mass."),
    ("What does the coefficient 3 in 3H₂O mean?", "three water molecules", ["three hydrogen atoms only", "water with 3 oxygen atoms", "three times heavier water"], "Coefficients count molecules."),
    ("What does the subscript 2 in H₂O mean?", "two hydrogen atoms in each molecule", ["two water molecules", "two oxygen atoms", "two reactions"], "Subscripts are part of the formula."),
    ("When balancing, what may you change?", "only the coefficients", ["only the subscripts", "both subscripts and coefficients", "the elements"], "Changing subscripts changes the substance."),
    ("What is the law of conservation of mass?", "Total mass of reactants equals total mass of products.", ["Products always weigh more.", "Gases have no mass.", "Mass is lost as heat."], "Lavoisier."),
    ("In a balanced equation, what must be the same on both sides?", "the number of atoms of each element", ["the number of molecules", "the number of compounds", "the coefficients"], "Atoms, not molecules."),
    ("Why does a burning candle seem to lose mass?", "The products (CO₂ and water vapor) escape into the air.", ["Mass is destroyed.", "Wax has no mass.", "Heat removes atoms."], "Open system."),
    ("What is the first step in balancing an equation?", "count the atoms of each element on both sides", ["change the subscripts", "add more products", "remove an element"], "Make a tally."),
])
B5 = bank([
    ("A student balances H₂ + O₂ → H₂O by writing H₂O₂. What is wrong?", "She changed a subscript, which made a different substance (hydrogen peroxide).", ["Nothing is wrong.", "She should remove the oxygen.", "She needed more arrows."],
     "Use 2H₂ + O₂ → 2H₂O."),
    ("A sealed bag of baking soda and vinegar is weighed before and after reacting. What will the scale show?", "the same mass", ["less mass", "more mass", "zero mass"], "Closed system."),
    ("Why do we use the lowest whole-number coefficients?", "It is the simplest ratio of the substances.", ["Smaller numbers make less product.", "It changes the reaction.", "Big numbers are wrong atoms."], "4H₂ + 2O₂ → 4H₂O is the same ratio."),
    ("Burning steel wool on a balance gets heavier. Why?", "Oxygen from the air combines with the iron.", ["Mass is created.", "Heat has mass.", "Iron gains protons."], "The product includes oxygen atoms."),
    ("How can a model with colored beads show conservation of mass?", "The same beads are rearranged into new groups, none added or removed.", ["Beads disappear.", "New beads appear.", "Beads change color."], "Atoms rearrange."),
])


def body():
    think = ("<p><b>Atoms are rearranged, never created or destroyed.</b></p>"
             "<ul><li>Count every element on both sides. A coefficient multiplies every atom in its formula; a subscript outside parentheses multiplies everything inside.</li>"
             "<li>Balance by changing only coefficients, never subscripts.</li>"
             "<li>Total mass of reactants = total mass of products (in a closed system).</li></ul>")
    ex = [("Atoms of O in 3Ca(OH)<sub>2</sub>?", ["Each formula has 2 O", "3 × 2"], "6"),
          ("Balance ? H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O", ["4 H on the right"], "2")]
    mist = ["Changing subscripts to balance (H<sub>2</sub>O → H<sub>2</sub>O<sub>2</sub>).", "Multiplying only the first atom by the coefficient.", "Thinking mass is lost when a gas forms."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Coefficients and subscripts", B1 + [(g_count, 12)]),
        ("Counting atoms", [(g_count, 12), (g_check, 8)]),
        ("Is it balanced?", [(g_check, 10), (g_missing, 10)]),
        ("Balancing equations", [(g_pick, 14), (g_missing, 6)]),
        ("Conservation of mass", B5 + [(g_mass, 10), (g_pick, 5)]),
    ])
    make("chemistry", "balancing-chemical-equations", 6, "HS-PS1-7",
         "Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical reaction.",
         "Balancing Chemical Equations",
         "Balancing Equations Worksheets: Coefficients and Conservation of Mass (High School Chemistry)",
         "Balancing Equations",
         "Free high school chemistry worksheets on balancing chemical equations (NGSS HS-PS1-7): counting atoms, coefficients and subscripts, checking and balancing equations, and conservation of mass. 100 questions with answers.",
         "Atoms are conserved in reactions.",
         "Balance with coefficients so each element has the same count on both sides.",
         body(),
         [("How do you balance a chemical equation?", "Count the atoms of each element on both sides, then change coefficients (never subscripts) until every element matches."),
          ("What is the difference between a coefficient and a subscript?", "A coefficient tells how many molecules or formula units. A subscript tells how many atoms are in one formula."),
          ("Why is mass conserved?", "The same atoms are only rearranged into new substances, so the total mass stays the same in a closed system.")],
         sets)


if __name__ == "__main__":
    main()
