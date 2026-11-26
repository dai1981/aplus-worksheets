# -*- coding: utf-8 -*-
"""
US High School Chemistry: Stoichiometry (HS-PS1-7)
  python tools/gen_us_science_chem_stoichiometry.py
Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical
reaction.
Mole ratios from balanced equations, mole-to-mole, mass-to-mass, limiting reactants and percent yield.
Atomic masses are rounded classroom values (sci_chem.AM) and molar masses are given in each question.
Wrong answers come from real mistakes: "ignore the coefficients", "use grams instead of moles in the ratio",
"the reactant with less mass is always limiting", "percent yield = theoretical ÷ actual".
"""
from fractions import Fraction
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import sub, split_eq, eq_html, molar, num, STOICH

U = Unit(90208)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def pick2():
    e, ctx = R.choice(STOICH)
    l, r = split_eq(e)
    s = l + r
    a, b = R.sample(s, 2)
    return e, ctx, l, r, a, b


def verb(l, a, b, mass=False):
    u = "What mass of" if mass else "How many moles of"
    ra, rb = a in l, b in l
    if ra and not rb:
        return u + " %s form from %s"
    if rb and not ra:
        return u + " %s are needed to make %s"
    if ra and rb:
        return u + " %s react with %s"
    return u + " %s form along with %s"


def fr(x):
    x = Fraction(x).limit_denominator(100)
    if x.denominator == 1:
        return num(x.numerator)
    return num(float(x)) if (x * 100).denominator == 1 else None


def g_ratio():
    e, ctx, l, r, a, b = pick2()
    if not once(("rt", e, a[1], b[1])):
        return None
    good = "%d : %d" % (a[0], b[0])
    w = ["%d : %d" % (b[0], a[0]), "1 : 1", "%d : %d" % (a[0] + 1, b[0])]
    w.append("%d : %d" % (a[0], b[0] + 2))
    val = Fraction(a[0], b[0])
    w = [x for x in dict.fromkeys(w) if Fraction(*map(int, x.split(" : "))) != val][:3]
    if len(w) < 3:
        return None
    return item("When %s: %s. What is the mole ratio of %s to %s?" % (ctx, eq_html(l, r), sub(a[1]), sub(b[1])), good, w[:3], "Use the coefficients: %d : %d." % (a[0], b[0]))


def g_mol():
    e, ctx, l, r, a, b = pick2()
    n = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 0.5, 1.5])
    v = fr(Fraction(str(n)) * b[0] / a[0])
    if v is None or not once(("ml", e, a[1], b[1], n)):
        return None
    w = [num(n), fr(Fraction(str(n)) * a[0] / b[0]), fr(Fraction(str(n)) * a[0] * b[0]), fr(Fraction(str(n)) * b[0])]
    w = [x + " mol" for x in dict.fromkeys(z for z in w if z and z != v)][:3]
    if len(w) < 3:
        return None
    return item(("When %s: %s. " + verb(l, a, b) + "?") % (ctx, eq_html(l, r), sub(b[1]), "%s mol of %s" % (num(n), sub(a[1]))), v + " mol", w,
                "%s mol %s × (%d mol %s ÷ %d mol %s) = %s mol." % (num(n), sub(a[1]), b[0], sub(b[1]), a[0], sub(a[1]), v))


def g_mass():
    e, ctx, l, r, a, b = pick2()
    n = R.choice([0.5, 1, 2, 3, 4, 0.25, 0.2, 0.1])
    ma, mb = molar(a[1]), molar(b[1])
    ga = ma * n
    nb = Fraction(str(n)) * b[0] / a[0]
    gb = float(nb) * mb
    if round(ga, 2) != ga or round(gb, 2) != gb or not once(("ms", e, a[1], b[1], n)):
        return None
    good = num(gb) + " g"
    w = [num(ga * b[0] / a[0]) + " g", num(n * mb) + " g", num(ga) + " g", num(gb * 2) + " g"]
    w = [x for x in dict.fromkeys(w) if x != good][:3]
    if len(w) < 3:
        return None
    return item(("When %s: %s. " + verb(l, a, b, True) + "? (%s = %s g/mol, %s = %s g/mol)") % (
        ctx, eq_html(l, r), sub(b[1]), "%s g of %s" % (num(ga), sub(a[1])), sub(a[1]), num(ma), sub(b[1]), num(mb)), good, w,
        "%s g ÷ %s = %s mol; × %d/%d = %s mol; × %s = %s g." % (num(ga), num(ma), num(n), b[0], a[0], fr(nb) or num(float(nb)), num(mb), num(gb)))


def g_limit():
    e, ctx = R.choice([x for x in STOICH if len(split_eq(x[0])[0]) == 2])
    l, r = split_eq(e)
    (ca, fa), (cb, fb) = l
    pc, pf = r[0]
    na = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
    nb = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
    ra, rb = Fraction(na, ca), Fraction(nb, cb)
    if ra == rb or not once(("lm", e, na, nb)):
        return None
    lim, other = (fa, fb) if ra < rb else (fb, fa)
    prod = min(ra, rb) * pc
    k = R.random() < 0.5
    if k:
        why = "%s needs %s : %s = %d : %d; %d mol %s ÷ %d = %s, %d mol %s ÷ %d = %s. The smaller one runs out first." % (
            "The equation", sub(fa), sub(fb), ca, cb, na, sub(fa), ca, num(float(ra)), nb, sub(fb), cb, num(float(rb)))
        return item("When %s: %s. You start with %d mol of %s and %d mol of %s. Which is the limiting reactant?" % (ctx, eq_html(l, r), na, sub(fa), nb, sub(fb)), sub(lim),
                    [sub(other), "Neither; both run out together.", sub(pf)], why)
    v = fr(prod)
    if v is None:
        return None
    w = [fr(max(ra, rb) * pc), fr(Fraction(na + nb, 1)), fr(min(ra, rb))]
    w = [x + " mol" for x in dict.fromkeys(z for z in w if z and z != v)][:3]
    if len(w) < 3:
        return None
    return item("When %s: %s. You start with %d mol of %s and %d mol of %s. How many moles of %s can form?" % (ctx, eq_html(l, r), na, sub(fa), nb, sub(fb), sub(pf)), v + " mol", w,
                "%s is limiting; it gives %s mol of %s." % (sub(lim), v, sub(pf)))


def g_yield():
    who = P.next()[0]
    th = R.choice([20, 25, 40, 50, 60, 80, 100, 120, 150, 200, 250])
    p = R.choice([50, 60, 70, 75, 80, 85, 90, 95])
    ac = th * p / 100
    k = R.choice(["pct", "act"])
    if ac != round(ac, 1) or not once(("yd", th, p, k)):
        return None
    prod = R.choice(["aspirin", "copper", "magnesium oxide", "sodium chloride", "calcium carbonate", "iron"])
    if k == "pct":
        return item("%s's calculation says %s g of %s should form, but she collects %s g. What is the percent yield?" % (who, num(th), prod, num(ac)), "%d%%" % p,
                    ["%s%%" % num(round(100 * th / ac, 1)), "%d%%" % (100 - p), "%s%%" % num(ac)], "actual ÷ theoretical × 100 = %s ÷ %s × 100 = %d%%." % (num(ac), num(th), p))
    return item("The theoretical yield of %s is %s g. %s gets a yield of %d%%. What mass does %s collect?" % (prod, num(th), who, p, who), num(ac) + " g",
                [num(th) + " g", num(th - ac) + " g", num(th + ac) + " g"], "%d%% of %s g = %s g." % (p, num(th), num(ac)))


B1 = bank([
    ("What does stoichiometry calculate?", "the amounts of reactants and products in a reaction", ["the speed of a reaction", "the color of products", "the temperature of a reaction"], "Uses balanced equations."),
    ("What do the coefficients in a balanced equation give?", "the mole ratio of the substances", ["the mass ratio of the substances", "the number of elements", "the temperature"], "2H₂ : O₂ = 2 : 1."),
    ("Why must you convert grams to moles before using the ratio?", "The coefficients compare moles, not grams.", ["Grams are wrong units.", "Moles are heavier.", "The ratio uses liters."], "Mole bridge."),
    ("What is the limiting reactant?", "the reactant that runs out first and stops the reaction", ["the reactant with the smallest mass", "the product", "the reactant in excess"], "It limits the product."),
    ("What is the excess reactant?", "the reactant left over after the reaction stops", ["the reactant that runs out", "the product", "a catalyst"], "Some remains."),
    ("What is theoretical yield?", "the most product that can form, calculated from the limiting reactant", ["the product you actually collect", "the mass of reactants", "always 100 g"], "Calculated."),
    ("What is percent yield?", "actual yield ÷ theoretical yield × 100", ["theoretical ÷ actual × 100", "actual − theoretical", "mass of reactants ÷ products"], "Usually below 100%."),
    ("In 2H₂ + O₂ → 2H₂O, how many moles of water form from 1 mol of O₂?", "2 mol", ["1 mol", "0.5 mol", "3 mol"], "O₂ : H₂O = 1 : 2."),
])
B5 = bank([
    ("Why is percent yield usually less than 100%?", "Some product is lost, side reactions happen or the reaction is incomplete.", ["Mass is destroyed.", "Calculations are always wrong.", "Atoms disappear."], "Real labs."),
    ("A student gets a 115% yield. What is the most likely reason?", "The product was still wet or impure.", ["Mass was created.", "The reaction was perfect.", "Atoms were added by the scale."], "Above 100% signals error."),
    ("A chemist adds extra oxygen when burning a fuel. Why?", "So the fuel is the limiting reactant and burns completely.", ["Oxygen is the product.", "To make less product.", "To stop the reaction."], "Excess reactant."),
    ("Making sandwiches: 10 slices of bread and 3 slices of cheese (2 bread + 1 cheese each). What limits the number of sandwiches?", "the cheese (only 3 sandwiches)",
     ["the bread (5 sandwiches)", "neither", "both equally"], "Limiting reactant analogy."),
    ("How do stoichiometry calculations show conservation of mass?", "The total mass of reactants used equals the total mass of products formed.", ["Products always weigh more.", "Moles are not conserved.", "Mass is lost as gas."], "Atoms are conserved."),
])


def body():
    think = ("<p><b>Coefficients give the mole ratio.</b></p>"
             "<ul><li>Steps: grams of A → moles of A (÷ molar mass) → moles of B (× ratio) → grams of B (× molar mass).</li>"
             "<li>The limiting reactant runs out first; it decides how much product forms.</li>"
             "<li>Percent yield = actual ÷ theoretical × 100.</li></ul>")
    ex = [("2H<sub>2</sub> + O<sub>2</sub> → 2H<sub>2</sub>O. Moles of water from 3 mol O<sub>2</sub>?", ["3 × 2/1"], "6 mol"),
          ("Expected 50 g, got 40 g. Percent yield?", ["40 ÷ 50 × 100"], "80%")]
    mist = ["Using grams directly in the mole ratio.", "Thinking the reactant with less mass is always limiting.", "Dividing theoretical by actual for percent yield."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Mole ratios", B1 + [(g_ratio, 12)]),
        ("Mole to mole", [(g_mol, 14), (g_ratio, 6)]),
        ("Mass to mass", [(g_mass, 14), (g_mol, 6)]),
        ("Limiting reactants", [(g_limit, 14), (g_yield, 6)]),
        ("Percent yield", B5 + [(g_yield, 8), (g_mass, 4), (g_limit, 3)]),
    ])
    make("chemistry", "stoichiometry", 8, "HS-PS1-7",
         "Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical reaction.",
         "Stoichiometry",
         "Stoichiometry Worksheets: Mole Ratios, Limiting Reactants and Percent Yield (Chemistry)",
         "Stoichiometry",
         "Free high school chemistry worksheets on stoichiometry (NGSS HS-PS1-7): mole ratios, mole-to-mole and mass-to-mass problems, limiting reactants and percent yield. 100 questions with answers.",
         "Coefficients give the mole ratio.",
         "Convert to moles, use the ratio, then convert back; the limiting reactant sets the amount.",
         body(),
         [("How do you do a mass-to-mass stoichiometry problem?", "Change grams of the given substance to moles, use the mole ratio from the balanced equation, then change moles of the new substance to grams."),
          ("How do you find the limiting reactant?", "Divide the moles of each reactant by its coefficient. The smaller result is the limiting reactant."),
          ("How is percent yield calculated?", "Divide the actual yield by the theoretical yield and multiply by 100.")],
         sets)


if __name__ == "__main__":
    main()
