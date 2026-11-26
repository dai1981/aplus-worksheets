# -*- coding: utf-8 -*-
"""
US High School Chemistry: Types of Chemical Reactions (HS-PS1-2)
  python tools/gen_us_science_chem_types_of_chemical_reactions.py
Construct and revise an explanation for the outcome of a simple chemical reaction based on the outermost electron states
of atoms, trends in the periodic table, and knowledge of the patterns of chemical properties.
Synthesis, decomposition, single replacement, double replacement and combustion; the activity series; predicting
products of metal + nonmetal and hydrocarbon combustion; evidence of a chemical change.
Wrong answers come from real mistakes: "any metal replaces any other metal", "combustion makes only CO2",
"melting is a chemical change", "Na + Cl2 makes NaCl2".
"""
from math import gcd
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import BY, ion_charge, sub

U = Unit(90205)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def eq(s):
    """'2H2 + O2 -> 2H2O' with subscripts (a leading coefficient stays normal size)"""
    out = []
    for part in s.split(" "):
        if part in ("+", "->"):
            out.append("→" if part == "->" else "+")
            continue
        i = 0
        while i < len(part) and part[i].isdigit():
            i += 1
        out.append(part[:i] + sub(part[i:]))
    return " ".join(out)


TYPES = ["synthesis", "decomposition", "single replacement", "double replacement", "combustion"]
EQS = [("2Na + Cl2 -> 2NaCl", 0), ("2Mg + O2 -> 2MgO", 0), ("N2 + 3H2 -> 2NH3", 0), ("CaO + H2O -> Ca(OH)2", 0), ("4Al + 3O2 -> 2Al2O3", 0), ("2H2 + O2 -> 2H2O", 0),
       ("S + O2 -> SO2", 0), ("2H2O -> 2H2 + O2", 1), ("CaCO3 -> CaO + CO2", 1), ("2KClO3 -> 2KCl + 3O2", 1), ("2HgO -> 2Hg + O2", 1), ("2H2O2 -> 2H2O + O2", 1),
       ("2NaN3 -> 2Na + 3N2", 1), ("Zn + 2HCl -> ZnCl2 + H2", 2), ("Fe + CuSO4 -> FeSO4 + Cu", 2), ("Cu + 2AgNO3 -> Cu(NO3)2 + 2Ag", 2), ("Cl2 + 2KBr -> 2KCl + Br2", 2),
       ("Mg + 2HCl -> MgCl2 + H2", 2), ("2Na + 2H2O -> 2NaOH + H2", 2), ("AgNO3 + NaCl -> AgCl + NaNO3", 3), ("HCl + NaOH -> NaCl + H2O", 3), ("BaCl2 + Na2SO4 -> BaSO4 + 2NaCl", 3),
       ("Pb(NO3)2 + 2KI -> PbI2 + 2KNO3", 3), ("CaCO3 + 2HCl -> CaCl2 + H2CO3", 3), ("CH4 + 2O2 -> CO2 + 2H2O", 4), ("C3H8 + 5O2 -> 3CO2 + 4H2O", 4),
       ("2C2H6 + 7O2 -> 4CO2 + 6H2O", 4), ("C6H12O6 + 6O2 -> 6CO2 + 6H2O", 4), ("2C8H18 + 25O2 -> 16CO2 + 18H2O", 4), ("C2H5OH + 3O2 -> 2CO2 + 3H2O", 4)]
PAT = ["A + B → AB", "AB → A + B", "A + BC → AC + B", "AB + CD → AD + CB", "fuel + O₂ → CO₂ + H₂O"]


def g_type():
    e, k = R.choice(EQS)
    t = R.random() < 0.75
    if not once(("ty", e, t)):
        return None
    if t:
        return item("What type of reaction is %s?" % eq(e), TYPES[k], [x for x in TYPES if x != TYPES[k]], "Pattern: %s." % PAT[k])
    return item("Which general pattern matches %s?" % eq(e), PAT[k], R.sample([x for x in PAT if x != PAT[k]], 3), "This is %s." % TYPES[k])


ACT = ["K", "Na", "Ca", "Mg", "Al", "Zn", "Fe", "Pb", "H", "Cu", "Ag", "Au"]
SALT = {"Cu": "copper(II) sulfate", "Ag": "silver nitrate", "Zn": "zinc chloride", "Fe": "iron(II) chloride", "Pb": "lead(II) nitrate", "Mg": "magnesium sulfate", "Al": "aluminum nitrate"}


def g_act():
    k = R.choice(["salt", "acid", "rank"])
    if k == "salt":
        a = R.choice(["Mg", "Al", "Zn", "Fe", "Pb", "Cu", "Ag", "Au"])
        b = R.choice([x for x in SALT if x != a])
        if not once(("as", a, b)):
            return None
        yes = ACT.index(a) < ACT.index(b)
        ans = "Yes. %s is more active than %s, so it replaces it." % (BY[a][1].capitalize(), BY[b][1]) if yes else "No. %s is less active than %s, so no reaction occurs." % (BY[a][1].capitalize(), BY[b][1])
        w = ["No. %s is less active than %s, so no reaction occurs." % (BY[a][1].capitalize(), BY[b][1]) if yes else "Yes. %s is more active than %s, so it replaces it." % (BY[a][1].capitalize(), BY[b][1]),
             "Yes. Any metal replaces any other metal.", "No. Metals never react with solutions."]
        return item("A piece of %s is placed in %s solution. Will a single replacement reaction occur? (Activity series: %s)" % (BY[a][1], SALT[b], " &gt; ".join(ACT)), ans, w,
                    "A metal replaces only metals below it in the activity series.")
    if k == "acid":
        a = R.choice(["Mg", "Al", "Zn", "Fe", "Pb", "Cu", "Ag", "Au", "Ca"])
        if not once(("aa", a)):
            return None
        yes = ACT.index(a) < ACT.index("H")
        ans = "Yes, hydrogen gas bubbles form." if yes else "No, it is below hydrogen in the activity series."
        return item("Does %s react with hydrochloric acid? (Activity series: %s)" % (BY[a][1], " &gt; ".join(ACT)), ans,
                    ["No, it is below hydrogen in the activity series." if yes else "Yes, hydrogen gas bubbles form.", "Yes, it makes oxygen gas.", "Only if the metal is melted."],
                    "Metals above hydrogen replace it from acids.")
    a, b = R.sample([x for x in ACT if x != "H"], 2)
    if not once(("ar", tuple(sorted((a, b))))):
        return None
    hi, lo = (a, b) if ACT.index(a) < ACT.index(b) else (b, a)
    return item("Using the activity series (%s), which metal is more reactive: %s or %s?" % (" &gt; ".join(ACT), BY[a][1], BY[b][1]), BY[hi][1], [BY[lo][1], "They are equally reactive.", "Neither reacts."],
                "Higher in the list = loses electrons more easily.")


MET = ["Li", "Na", "K", "Mg", "Ca", "Al", "Ba"]
NON = {"Cl": "chlorine gas", "Br": "bromine", "O": "oxygen gas", "S": "sulfur", "F": "fluorine gas", "I": "iodine", "N": "nitrogen gas"}


def fm(m, x):
    a, b = ion_charge(BY[m]), -ion_charge(BY[x])
    g = gcd(a, b)
    nm, nx = b // g, a // g
    return sub(m + (str(nm) if nm > 1 else "") + x + (str(nx) if nx > 1 else ""))


def g_prod():
    k = R.choice(["mn", "mn", "comb"])
    if k == "mn":
        m, x = R.choice(MET), R.choice(list(NON))
        if not once(("pm", m, x)):
            return None
        good = fm(m, x)
        a, b = ion_charge(BY[m]), -ion_charge(BY[x])
        w = [sub(m + x), sub(m + x + "2"), sub(m + "2" + x), sub(m + (str(b) if b > 1 else "") + x + (str(a) if a > 1 else "")), sub(m + (str(a) if a > 1 else "") + x + (str(b) if b > 1 else ""))]
        w = list(dict.fromkeys(z for z in w if z != good))
        if len(w) < 3:
            return None
        return item("%s reacts with %s. What is the formula of the product?" % (BY[m][1].capitalize(), NON[x]), good, R.sample(w, 3),
                    "%s loses %d electron%s and %s gains %d; the charges must cancel." % (BY[m][1].capitalize(), a, "s" if a > 1 else "", BY[x][1], b))
    f = R.choice([("methane", "CH4"), ("propane", "C3H8"), ("butane", "C4H10"), ("ethanol", "C2H5OH"), ("octane", "C8H18"), ("glucose", "C6H12O6"), ("ethane", "C2H6"), ("pentane", "C5H12")])
    if not once(("pc", f[0])):
        return None
    return item("%s (%s) burns completely in oxygen. What are the products?" % (f[0].capitalize(), sub(f[1])), "carbon dioxide and water",
                ["carbon dioxide only", "carbon and hydrogen gas", "oxygen and water"], "Complete combustion of a compound of C and H (and O) gives CO₂ and H₂O.")


EVID = [("Bubbles form when baking soda is added to vinegar.", "chemical"), ("A clear solution turns cloudy and a yellow solid forms when two solutions mix.", "chemical"),
        ("An iron nail turns reddish brown and flaky over weeks.", "chemical"), ("A match gives off light and heat.", "chemical"),
        ("Hydrogen peroxide fizzes and the container gets warm when yeast is added.", "chemical"), ("A sliced apple turns brown in air.", "chemical"),
        ("Ice melts into water on the counter.", "physical"), ("Sugar dissolves in tea.", "physical"), ("Water boils and turns to steam.", "physical"),
        ("A glass bottle is crushed into small pieces.", "physical"), ("Salt water is evaporated and salt crystals are left.", "physical"),
        ("Dry ice turns directly into a gas.", "physical")]


def g_evid():
    s, t = R.choice(EVID)
    if not once(("ev", s)):
        return None
    if t == "chemical":
        return item("%s What kind of change is this?" % s, "a chemical change, because new substances form", ["a physical change, because only the form changes", "no change at all", "a nuclear change"],
                    "Evidence: gas, precipitate, color change, light or temperature change from a reaction.")
    return item("%s What kind of change is this?" % s, "a physical change, because the substance stays the same", ["a chemical change, because new substances form", "a nuclear change", "a combustion reaction"],
                "No new substance forms.")


B1 = bank([
    ("What is a chemical reaction?", "a process in which atoms rearrange to form new substances", ["a change in state only", "a change in shape only", "atoms being created"], "Bonds break and form."),
    ("What are reactants?", "the substances at the start of a reaction", ["the substances made by a reaction", "the arrow", "the coefficients"], "Left side."),
    ("What are products?", "the substances made by a reaction", ["the starting substances", "the energy", "the catalyst"], "Right side."),
    ("In a synthesis reaction, what happens?", "two or more substances combine into one", ["one substance breaks apart", "one element replaces another", "a fuel burns"], "A + B → AB."),
    ("In a decomposition reaction, what happens?", "one compound breaks into simpler substances", ["two elements combine", "ions swap partners", "a fuel burns in oxygen"], "AB → A + B."),
    ("What does combustion always need?", "oxygen", ["nitrogen", "water", "a metal"], "Fuel + O₂."),
    ("In a double replacement reaction, what often forms?", "a precipitate, a gas or water", ["a pure metal", "oxygen gas", "a new element"], "Ions swap partners."),
    ("Why does sodium react violently with water but gold does not?", "Sodium loses its 1 valence electron very easily.", ["Gold has no electrons.", "Sodium is heavier.", "Gold is a gas."], "Activity depends on outer electrons."),
])
B5 = bank([
    ("A student adds zinc to copper(II) sulfate. A red-brown solid forms and the blue color fades. What happened?", "Zinc replaced copper, so copper metal formed.",
     ["Copper replaced zinc.", "No reaction happened.", "The solution evaporated."], "Single replacement."),
    ("Why do chlorine and sodium react so easily?", "Sodium easily loses 1 electron and chlorine easily gains 1.", ["Both are noble gases.", "Both are metals.", "Both have 8 valence electrons."], "Outer electrons."),
    ("A gas is made by mixing acid with a metal. A burning splint pops. Which gas is it?", "hydrogen", ["oxygen", "carbon dioxide", "nitrogen"], "The pop test."),
    ("Which observation is the best evidence that a new substance formed?", "a solid precipitate appears when two clear solutions are mixed", ["the liquid gets colder in a fridge", "ice melts", "the sugar disappears in water"], "Precipitate."),
    ("Bromine is less reactive than chlorine. What happens when chlorine gas is bubbled into potassium bromide solution?", "Chlorine replaces bromine, so bromine forms.",
     ["Bromine replaces chlorine.", "Nothing happens.", "Potassium becomes a gas."], "More reactive halogen wins."),
])


def body():
    think = ("<p><b>Reactions follow patterns set by outer electrons.</b></p>"
             "<ul><li>Synthesis A + B → AB; decomposition AB → A + B; single replacement A + BC → AC + B; double replacement AB + CD → AD + CB; combustion: fuel + O<sub>2</sub> → CO<sub>2</sub> + H<sub>2</sub>O.</li>"
             "<li>A metal replaces another only if it is higher in the activity series.</li>"
             "<li>Metal + nonmetal: the charges set the formula of the product.</li></ul>")
    ex = [("Zn + CuSO<sub>4</sub>: reaction?", ["Zn is above Cu"], "yes, Cu forms"),
          ("Mg + O<sub>2</sub>: product?", ["Mg<sup>2+</sup> and O<sup>2−</sup>"], "MgO")]
    mist = ["Thinking any metal can replace any other metal.", "Forgetting water as a product of combustion.", "Calling melting or dissolving a chemical change."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reaction basics", B1 + [(g_type, 8), (g_evid, 4)]),
        ("Five reaction types", [(g_type, 14), (g_evid, 6)]),
        ("Predicting products", [(g_prod, 14), (g_type, 6)]),
        ("The activity series", [(g_act, 18), (g_prod, 2)]),
        ("Explaining outcomes", B5 + [(g_act, 6), (g_prod, 5), (g_type, 4)]),
    ])
    make("chemistry", "types-of-chemical-reactions", 5, "HS-PS1-2",
         "Construct and revise an explanation for the outcome of a simple chemical reaction based on the outermost electron states of atoms, trends in the periodic table, and knowledge of the patterns of chemical properties.",
         "Types of Chemical Reactions",
         "Chemical Reactions Worksheets: Reaction Types, Activity Series and Products (Chemistry)",
         "Reaction Types",
         "Free high school chemistry worksheets on types of chemical reactions (NGSS HS-PS1-2): synthesis, decomposition, replacement and combustion, the activity series and predicting products. 100 questions with answers.",
         "Reactions follow patterns.",
         "Outer electrons and the activity series predict what forms.",
         body(),
         [("What are the five main types of reactions?", "Synthesis, decomposition, single replacement, double replacement and combustion."),
          ("How does the activity series predict reactions?", "A metal can replace another metal (or hydrogen in an acid) only if it is higher in the series."),
          ("What are signs of a chemical reaction?", "A gas, a precipitate, a color change, light, or a temperature change that comes from new substances forming.")],
         sets)


if __name__ == "__main__":
    main()
