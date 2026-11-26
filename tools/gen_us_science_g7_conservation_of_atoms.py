# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Conservation of Atoms in Reactions (MS-PS1-5)
  python tools/gen_us_science_g7_conservation_of_atoms.py
In a chemical reaction atoms are rearranged, not created or destroyed, so the number of each kind of atom
and the total mass stay the same. Counting atoms in balanced equations; finding a missing coefficient;
mass data in closed vs. open systems (gas escaping).
Assessment boundary: balancing only with simple whole-number coefficients; no moles.
Wrong answers come from real mistakes: "mass is lost when gas forms", "you can change subscripts to balance",
"products have more atoms because they are new substances".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70104)
R = U.R
P = People(R)


def f(parts):
    return "".join(el + ("<sub>%d</sub>" % n if n > 1 else "") for el, n in parts)


def side(terms):
    return " + ".join((("%d" % c) if c > 1 else "") + f(m) for c, m in terms)


# (name, reactants, products) with terms (coefficient, [(el, n)])
EQ = [("hydrogen burning", [(2, [("H", 2)]), (1, [("O", 2)])], [(2, [("H", 2), ("O", 1)])]),
      ("methane burning", [(1, [("C", 1), ("H", 4)]), (2, [("O", 2)])], [(1, [("C", 1), ("O", 2)]), (2, [("H", 2), ("O", 1)])]),
      ("making ammonia", [(1, [("N", 2)]), (3, [("H", 2)])], [(2, [("N", 1), ("H", 3)])]),
      ("carbon burning", [(1, [("C", 1)]), (1, [("O", 2)])], [(1, [("C", 1), ("O", 2)])]),
      ("photosynthesis", [(6, [("C", 1), ("O", 2)]), (6, [("H", 2), ("O", 1)])], [(1, [("C", 6), ("H", 12), ("O", 6)]), (6, [("O", 2)])]),
      ("rusting of iron", [(4, [("Fe", 1)]), (3, [("O", 2)])], [(2, [("Fe", 2), ("O", 3)])]),
      ("making salt", [(2, [("Na", 1)]), (1, [("Cl", 2)])], [(2, [("Na", 1), ("Cl", 1)])]),
      ("magnesium burning", [(2, [("Mg", 1)]), (1, [("O", 2)])], [(2, [("Mg", 1), ("O", 1)])])]
NAMES = {"H": "hydrogen", "O": "oxygen", "C": "carbon", "N": "nitrogen", "Fe": "iron", "Na": "sodium", "Cl": "chlorine", "Mg": "magnesium"}


def count(terms, el):
    return sum(c * dict(m).get(el, 0) for c, m in terms)


def eqn(e):
    return side(e[1]) + " → " + side(e[2])


def g_count():
    e = R.choice(EQ)
    els = sorted({el for _, m in e[1] for el, _ in m})
    el = R.choice(els)
    n = count(e[1], el)
    who = P.next()[0]
    where = R.choice(["reactants (left side)", "products (right side)"])
    w = sorted({n + 1, n * 2, max(1, n - 1), n + 2} - {n})
    return item("%s studies %s: <b>%s</b>. How many %s atoms are in the %s?" % (who, e[0], eqn(e), NAMES[el], where), "%d" % n, ["%d" % x for x in w[:3]],
                "Multiply each coefficient by the subscript and add. The number is the same on both sides: %d." % n)


def g_balanced():
    e = R.choice(EQ)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s checks the equation for %s: <b>%s</b>. Is it balanced?" % (who, e[0], eqn(e)), "Yes. Each kind of atom has the same number on both sides.",
                    ["No. The products have more atoms.", "No. The reactants have more atoms.", "Balance does not matter in reactions."], "Atoms are only rearranged, so the counts match.")
    # make it unbalanced by changing one coefficient
    terms = [list(t) for t in e[1]]
    i = R.randrange(len(terms))
    terms[i][0] += 1
    bad = [tuple(t) for t in terms]
    if all(count(bad, el) == count(e[2], el) for el in NAMES):
        return None
    return item("%s writes this equation for %s: <b>%s → %s</b>. Is it balanced?" % (who, e[0], side(bad), side(e[2])), "No. The number of some atoms is different on each side.",
                ["Yes. It is balanced.", "Yes, because both sides have the same substances.", "It cannot be checked."], "Count each kind of atom on both sides; at least one does not match.")


def g_missing():
    e = R.choice([x for x in EQ if any(c > 1 for c, _ in x[1] + x[2])])
    allt = [("r", i) for i in range(len(e[1]))] + [("p", i) for i in range(len(e[2]))]
    side_, i = R.choice([t for t in allt if (e[1] if t[0] == "r" else e[2])[t[1]][0] > 1])
    terms = e[1] if side_ == "r" else e[2]
    c = terms[i][0]
    shown_r = " + ".join(("?" if side_ == "r" and j == i else (("%d" % t[0]) if t[0] > 1 else "")) + f(t[1]) for j, t in enumerate(e[1]))
    shown_p = " + ".join(("?" if side_ == "p" and j == i else (("%d" % t[0]) if t[0] > 1 else "")) + f(t[1]) for j, t in enumerate(e[2]))
    who = P.next()[0]
    return item("%s's equation for %s is missing a coefficient: <b>%s → %s</b>. What number goes in place of the question mark?" % (who, e[0], shown_r, shown_p), "%d" % c,
                ["%d" % x for x in sorted({1, c + 1, c * 2, c + 2} - {c})[:3]], "With %d, every kind of atom has the same number on both sides." % c)


def g_mass():
    a = R.randint(20, 80)
    b = R.randint(10, 60)
    who = P.next()[0]
    closed = R.random() < 0.5
    gas = R.randint(2, 8)
    after = a + b if closed else a + b - gas
    what = R.choice([("vinegar", "baking soda"), ("lemon juice", "baking soda"), ("an antacid tablet", "water")])
    rows = [["%s" % what[0], "%d g" % a], ["%s" % what[1], "%d g" % b], ["total after reaction", "%d g" % after]]
    tab = table(["", "Mass"], rows)
    if closed:
        return item(tab + "%s mixed %s and %s inside a sealed bag. Gas formed. What does the data show?" % (who, what[0], what[1]),
                    "Mass was conserved because no matter could escape.", ["Mass was lost because a gas formed.", "Mass was created by the reaction.", "The scale is broken."],
                    "%d + %d = %d g before and after." % (a, b, a + b))
    return item(tab + "%s mixed %s and %s in an open cup. Gas bubbled out. Why is the total mass after the reaction %d g less?" % (who, what[0], what[1], gas),
                "The gas escaped into the air, but the atoms were not destroyed.", ["Atoms were destroyed in the reaction.", "Reactions always lose mass.", "The gas had no mass."],
                "In an open system, gas leaves the cup. In a sealed bag, the mass would stay the same.")


B1 = bank([
    ("What happens to atoms in a chemical reaction?", "They are rearranged into new substances; none are created or destroyed.", ["They are destroyed.", "New atoms are created.", "They turn into energy."],
     "This is the law of conservation of mass."),
    ("What is the law of conservation of mass?", "In a closed system, the total mass before and after a reaction is the same.", ["Mass always increases.", "Mass is lost as heat.", "Mass only matters in solids."],
     "Same atoms, same mass."),
    ("In a chemical equation, what are the reactants?", "the substances you start with (left side)", ["the substances made (right side)", "the arrow", "the energy"], "Reactants → products."),
    ("Why can't you balance an equation by changing subscripts?", "Changing a subscript makes it a different substance.", ["Subscripts do not matter.", "It makes the equation longer.", "You can, it is fine."],
     "H₂O and H₂O₂ are different substances."),
    ("A burning candle gets lighter. Does this break the law of conservation of mass?", "No. The wax reacts with oxygen to form gases that go into the air.", ["Yes, mass is destroyed.", "Yes, fire makes mass disappear.", "Candles have no mass."],
     "If you trapped the gases, the total mass would stay the same."),
    ("What is a closed system?", "a system where no matter can enter or leave", ["a system with no atoms", "an open cup", "a system where gas can escape"], "A sealed bag is a closed system."),
    ("If 10 g of reactants react completely in a closed jar, what is the mass of the products?", "10 g", ["less than 10 g", "more than 10 g", "0 g"], "Mass is conserved."),
    ("In 2H₂ + O₂ → 2H₂O, how many oxygen atoms are on each side?", "2", ["1", "4", "3"], "O₂ has 2; 2H₂O has 2 × 1 = 2."),
])
B5 = bank([
    ("Ava weighs a sealed bottle with vinegar and a balloon of baking soda: 210 g. She tips the baking soda in and it fizzes. What should the scale read?", "210 g", ["less than 210 g", "more than 210 g", "0 g"],
     "In a closed system the mass stays the same."),
    ("Leo burns steel wool in air. The ash weighs more than the steel wool did. Where did the extra mass come from?", "oxygen atoms from the air joined the iron", ["new atoms were created", "the scale is wrong", "heat has mass"],
     "Iron + oxygen → iron oxide."),
    ("Mia models a reaction with colored beads: 4 red and 2 blue before, then rearranges them. How many beads should she have after?", "4 red and 2 blue", ["more red beads", "fewer blue beads", "only red beads"],
     "Atoms are rearranged, not created or destroyed."),
    ("Why do scientists do conservation-of-mass experiments in sealed containers?", "so that gases cannot escape and change the measured mass", ["so the reaction is slower", "so it is darker", "to make new atoms"],
     "A closed system keeps all the matter."),
    ("A student says products have more atoms because they are new substances. How would you correct this?", "The same atoms are rearranged into new substances; the number stays the same.", ["Products do have more atoms.", "Products have fewer atoms.", "Atoms change into other atoms."],
     "Count atoms on both sides to check."),
])


def body():
    think = ("<p>In a chemical reaction, <b>atoms are rearranged</b> to make new substances. No atoms are created or destroyed, so the <b>number of each kind of atom</b> is the same before and after, and the <b>total mass</b> stays the same in a closed system.</p>"
             "<p>Example: <b>2H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O</b>. Left: 4 H and 2 O. Right: 4 H and 2 O. The equation is <b>balanced</b>.</p>"
             "<p>Count atoms with <b>coefficient × subscript</b>. In an open container a gas can escape, so the measured mass may drop, but the atoms still exist.</p>")
    ex = [("In CH<sub>4</sub> + 2O<sub>2</sub> → CO<sub>2</sub> + 2H<sub>2</sub>O, how many O atoms are on the right?", ["CO₂: 2", "2H₂O: 2 × 1 = 2", "2 + 2"], "4"),
          ("25 g + 15 g react in a sealed bag. Mass after?", ["Closed system."], "40 g")]
    mist = ["Thinking mass is lost when a gas forms. The gas still has mass.",
            "Changing subscripts to balance an equation. Change only coefficients.",
            "Thinking products have more atoms because they are new substances."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Atoms are conserved", B1 + [(g_count, 6), (g_mass, 6)]),
        ("Counting atoms in equations", [(g_count, 14), (g_balanced, 6)]),
        ("Balanced or not?", [(g_balanced, 12), (g_missing, 8)]),
        ("Mass data", [(g_mass, 12), (g_missing, 8)]),
        ("Modeling reactions", B5 + [g_count, g_balanced, g_missing, g_mass]),
    ])
    make("grade-7", "conservation-of-atoms", 4, "MS-PS1-5",
         "Develop and use a model to describe how the total number of atoms does not change in a chemical reaction and thus mass is conserved.",
         "Conservation of Atoms in Reactions",
         "Grade 7 Conservation of Mass Worksheets: Counting Atoms and Balanced Equations",
         "Conservation of Atoms",
         "Free middle school science worksheets on conservation of atoms and mass (NGSS MS-PS1-5): counting atoms in chemical equations, balanced equations, missing coefficients, and closed vs. open systems. 100 practice questions with answers.",
         "Atoms are rearranged, never created or destroyed.",
         "The number of each kind of atom is the same before and after a reaction, so mass is conserved.",
         body(),
         [("Why is mass conserved in a chemical reaction?", "The same atoms are rearranged into new substances. No atoms are created or destroyed."),
          ("How do you check if an equation is balanced?", "Count each kind of atom on both sides using coefficient × subscript. Every kind must match."),
          ("Why does an open cup of vinegar and baking soda lose mass?", "A gas forms and escapes into the air. In a sealed container the mass would stay the same.")],
         sets)


if __name__ == "__main__":
    main()
