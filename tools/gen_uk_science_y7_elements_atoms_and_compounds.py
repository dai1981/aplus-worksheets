# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Chemistry): Elements, Atoms and Compounds
  python tools/gen_uk_science_y7_elements_atoms_and_compounds.py
A simple (Dalton) atomic model; the differences between atoms, elements and compounds; chemical symbols and formulae
for elements and compounds; counting atoms in a formula; naming the elements in simple compounds; and telling
elements, compounds and mixtures apart.
Wrong answers come from real mistakes: "water is an element", "air is a compound", "CO has the same atoms as CO2",
"a compound is just a mixture of elements".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, People, once
from sci_chem import atoms, sub
from sci_phys import uniq

U = Unit(61707)
R = U.R
P = People(R)

SYM = [("hydrogen", "H"), ("helium", "He"), ("carbon", "C"), ("nitrogen", "N"), ("oxygen", "O"), ("sodium", "Na"), ("magnesium", "Mg"), ("aluminium", "Al"),
       ("sulfur", "S"), ("chlorine", "Cl"), ("potassium", "K"), ("calcium", "Ca"), ("iron", "Fe"), ("copper", "Cu"), ("zinc", "Zn"), ("silver", "Ag"),
       ("gold", "Au"), ("lead", "Pb")]


def g_sym():
    n, s = R.choice(SYM)
    k = R.random() < 0.5
    if not once(("sy", n, k)):
        return None
    if k:
        w = [x[1] for x in SYM if x[1] != s and x[1][0] == s[0]] + [x[1] for x in R.sample(SYM, 6) if x[1] != s]
        return item("What is the chemical symbol for %s?" % n, s, list(dict.fromkeys(w))[:3] if len(dict.fromkeys(w)) >= 3 else R.sample([x[1] for x in SYM if x[1] != s], 3),
                    "Symbols have one capital letter, sometimes followed by a small letter. Some come from Latin names (Fe, Cu, Ag, Au, Pb, Na, K).")
    return item("Which element has the symbol %s?" % s, n, R.sample([x[0] for x in SYM if x[0] != n], 3), "Some symbols come from Latin names: Fe (ferrum) is iron.")


CLASS = [("oxygen", "an element"), ("iron", "an element"), ("gold", "an element"), ("carbon", "an element"), ("helium", "an element"),
         ("water (H₂O)", "a compound"), ("carbon dioxide (CO₂)", "a compound"), ("sodium chloride (salt)", "a compound"), ("methane (CH₄)", "a compound"), ("sugar (glucose)", "a compound"),
         ("air", "a mixture"), ("sea water", "a mixture"), ("orange juice", "a mixture"), ("soil", "a mixture"), ("crude oil", "a mixture"), ("nitrogen", "an element"), ("copper", "an element"),
         ("ammonia (NH₃)", "a compound"), ("salty water", "a mixture"), ("milk", "a mixture")]


def g_class():
    x, c = R.choice(CLASS)
    if not once(("cl", x)):
        return None
    return item("Is %s an element, a compound or a mixture?" % x, c, [y for y in ["an element", "a compound", "a mixture"] if y != c] + ["a single atom only"],
                "Element: one type of atom. Compound: different atoms chemically joined. Mixture: substances not chemically joined.")


FORM = [("H2O", "water"), ("CO2", "carbon dioxide"), ("CH4", "methane"), ("NH3", "ammonia"), ("NaCl", "sodium chloride"), ("CaCO3", "calcium carbonate"),
        ("H2SO4", "sulfuric acid"), ("C6H12O6", "glucose"), ("O2", "oxygen"), ("Fe2O3", "iron oxide"), ("MgO", "magnesium oxide"), ("HCl", "hydrochloric acid"),
        ("CuSO4", "copper sulfate"), ("C2H5OH", "ethanol"), ("KCl", "potassium chloride"), ("HNO3", "nitric acid"),
        ("CaO", "calcium oxide"), ("NaOH", "sodium hydroxide"), ("C3H8", "propane"), ("SO2", "sulfur dioxide")]


def g_count():
    f, n = R.choice(FORM)
    k = R.choice(["total", "elements"])
    if not once(("co", f, k)):
        return None
    a = atoms(f)
    if k == "total":
        t = sum(a.values())
        g = str(t)
        return item("How many atoms are there in one molecule or formula unit of %s (%s)?" % (n, sub(f)), g, uniq(g, [str(t + 1), str(t - 1), str(len(a)), str(t + 2)]),
                    "Add the numbers: %s." % " + ".join("%d %s" % (v, k2) for k2, v in a.items()))
    e = len(a)
    g = str(e)
    return item("How many different elements are in %s (%s)?" % (n, sub(f)), g, uniq(g, [str(sum(a.values())), str(e + 1), str(max(1, e - 1)), str(e + 2)]),
                "The elements are %s." % ", ".join(a.keys()))


NAMES = [("sodium chloride", "sodium and chlorine"), ("magnesium oxide", "magnesium and oxygen"), ("iron sulfide", "iron and sulfur"), ("copper oxide", "copper and oxygen"),
         ("calcium chloride", "calcium and chlorine"), ("zinc oxide", "zinc and oxygen"), ("carbon dioxide", "carbon and oxygen"), ("hydrogen chloride", "hydrogen and chlorine"),
         ("potassium bromide", "potassium and bromine"), ("aluminium oxide", "aluminium and oxygen")]


def g_name():
    c, e = R.choice(NAMES)
    if not once(("na", c)):
        return None
    return item("Which elements are joined in %s?" % c, e, R.sample([x[1] for x in NAMES if x[1] != e], 3), "A name ending in -ide usually has just two elements.")


B1 = bank([
    ("What is an atom?", "the smallest particle of an element", ["a mixture of elements", "a type of cell", "a group of compounds"], "Everything is made of atoms."),
    ("What is an element?", "a substance made of only one type of atom", ["a substance made of two types of atom joined together", "any mixture", "a liquid"], "About 118 elements are known."),
    ("What is a compound?", "a substance made of two or more types of atom chemically joined", ["only one type of atom", "a mixture that can be sieved", "a single atom"], "Water, H₂O."),
    ("What is a molecule?", "two or more atoms joined together", ["a single atom on its own", "a type of mixture", "half an atom"], "O₂ and H₂O are molecules."),
    ("Who suggested that all matter is made of tiny atoms that cannot be broken down, in the early 1800s?", "John Dalton", ["Isaac Newton", "Charles Darwin", "Robert Hooke"], "Dalton's atomic model."),
    ("Where can you find all the known elements arranged in order?", "the periodic table", ["a food web", "a tally chart", "the reactivity table of rocks"], "Rows and columns."),
    ("What does the formula CO₂ tell you?", "one carbon atom joined to two oxygen atoms", ["two carbon atoms and one oxygen atom", "one carbon atom only", "a mixture of coal and air"], "The small number is for the atom before it."),
    ("How are the properties of a compound different from its elements?", "A compound usually has very different properties from the elements in it.", ["They are always the same.", "A compound is just the elements mixed.", "Compounds have no properties."], "Sodium + chlorine → salt."),
])
B5 = bank([
    ("Why is water a compound and not a mixture?", "Hydrogen and oxygen atoms are chemically joined in a fixed ratio.", ["It can be sieved apart.", "It has only one type of atom.", "It is a liquid."], "Fixed ratio, chemically joined."),
    ("Sodium is a reactive metal and chlorine is a poisonous gas. What do they make when they react?", "sodium chloride, which is table salt", ["a mixture of metal and gas", "pure sodium", "water"], "New properties."),
    ("What is the difference between O and O₂?", "O is one oxygen atom; O₂ is a molecule of two oxygen atoms.", ["They are the same.", "O₂ is a compound.", "O is a molecule."], "Symbols and formulae."),
    ("Why is air a mixture?", "Its gases are not chemically joined and can be separated.", ["It is one element.", "It is a compound of nitrogen and oxygen.", "It has no particles."], "Mixtures can be separated physically."),
    ("Why does CO behave differently from CO₂?", "They are different compounds with different numbers of oxygen atoms.", ["They are the same substance.", "CO has no oxygen.", "CO₂ has no carbon."], "Formula matters."),
])


def body():
    think = ("<p><b>All matter is made of atoms.</b></p>"
             "<ul><li>An element has only one type of atom. A compound has different atoms chemically joined.</li>"
             "<li>Each element has a symbol (O, Fe, Na). A formula shows the atoms in a compound: H₂O has 2 hydrogen and 1 oxygen.</li>"
             "<li>A mixture contains substances that are not chemically joined.</li></ul>")
    ex = [("Atoms in CH₄?", ["1 C + 4 H"], "5"),
          ("Symbol for iron?", ["From the Latin ferrum"], "Fe")]
    mist = ["Thinking water is an element.", "Thinking air is a compound.", "Thinking a compound is just a mixture of elements."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Atoms and elements", B1 + [(g_sym, 12)]),
        ("Chemical symbols", [(g_sym, 12), (g_class, 8)]),
        ("Elements, compounds, mixtures", [(g_class, 9), (g_name, 8), (g_sym, 3)]),
        ("Formulae", [(g_count, 20)]),
        ("Thinking about compounds", B5 + [(g_count, 12), (g_sym, 3)]),
    ])
    make_ks3(7, "elements-atoms-and-compounds", 7, "Chemistry", "Atoms, elements and compounds",
             "A simple (Dalton) atomic model; differences between atoms, elements and compounds; chemical symbols and formulae for elements and compounds; conservation of mass changes of state and chemical reactions.",
             "Elements, Atoms and Compounds",
             "Year 7 Science: Elements, Atoms and Compounds Worksheets (Symbols and Formulae)",
             "Elements and Compounds",
             "Free Year 7 science worksheets on elements, atoms and compounds: chemical symbols, formulae, counting atoms, naming compounds and telling elements, compounds and mixtures apart. 100 questions with answers.",
             "Elements have one type of atom.",
             "Compounds have different atoms chemically joined; H₂O has 2 H and 1 O.",
             body(),
             [("What is the difference between an element and a compound?", "An element contains only one type of atom, like oxygen or iron. A compound contains two or more different atoms chemically joined, like water (H₂O)."),
              ("How do you read a chemical formula?", "Each symbol is an element, and the small number after it tells you how many of those atoms there are. CO₂ has one carbon and two oxygen atoms."),
              ("Is air a compound?", "No. Air is a mixture of gases (mainly nitrogen and oxygen) that are not chemically joined.")],
             sets)


if __name__ == "__main__":
    main()
