# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Chemistry): Reactivity and Extraction of Metals
  python tools/gen_uk_science_y9_reactivity_and_extraction.py
The reactivity series including carbon and hydrogen, displacement reactions, oxidation and reduction (gain and loss of
oxygen), extracting metals from their ores by heating with carbon or by electrolysis, metals found as elements,
ores, and the efficacy of recycling. Reuses the reactivity-series questions of the Year 8 unit (new seed), the
displacement question of the US Chemistry unit and the resource questions of the US Grade 7 unit in British English.
Wrong answers come from real mistakes: "aluminium is extracted with carbon", "the metal oxide is oxidised",
"gold is extracted by electrolysis", "recycling saves no energy".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
import gen_uk_science_y8_metals_and_non_metals as M8

U = Unit(61905)
R = U.R
P = People(R)
M8.U, M8.R, M8.P = U, R, P
uk_sci.USED.clear()
TR = adopt_us("gen_us_science_chem_types_of_chemical_reactions", U)
NR = adopt_us("gen_us_science_g7_natural_resources", U)
us_act, us_use, us_origin = ukm(TR.g_act), ukm(NR.g_use), ukm(NR.g_origin)

SER = ["potassium", "sodium", "calcium", "magnesium", "aluminium", "(carbon)", "zinc", "iron", "tin", "lead", "(hydrogen)", "copper", "silver", "gold"]
METALS = [m for m in SER if not m.startswith("(")]
CI = SER.index("(carbon)")


def how(m):
    i = SER.index(m)
    if m in ("silver", "gold"):
        return "found as the pure metal (or heated simply)"
    return "electrolysis" if i < CI else "heating the oxide with carbon"


def g_ext():
    m = R.choice(METALS)
    if not once(("ex", m)):
        return None
    a = how(m)
    tab = table(["Reactivity series (most reactive first)"], [[", ".join(SER)]])
    return item(tab + "How is %s usually extracted from its ore?" % m, a, [x for x in ["electrolysis", "heating the oxide with carbon", "found as the pure metal (or heated simply)", "dissolving the ore in water"] if x != a],
                "Metals above carbon need electrolysis; metals below carbon can be reduced by carbon; the least reactive are found pure.")


RED = [("iron oxide", "iron"), ("copper oxide", "copper"), ("lead oxide", "lead"), ("zinc oxide", "zinc"), ("tin oxide", "tin")]


def g_red():
    ox, m = R.choice(RED)
    k = R.choice(["prod", "reduced", "oxidised", "gas"])
    if not once(("re", ox, k)):
        return None
    eq = "%s + carbon → %s + carbon dioxide" % (ox, m)
    if k == "prod":
        return item("Complete the word equation: %s + carbon → ? + carbon dioxide" % ox, m, [ox, "carbon monoxide", m + " carbonate"], "Carbon takes the oxygen.")
    if k == "reduced":
        return item("%s. Which substance is reduced?" % (eq[0].upper() + eq[1:]), ox, ["carbon", "carbon dioxide", m], "Reduction is the loss of oxygen.")
    if k == "oxidised":
        return item("%s. Which substance is oxidised?" % (eq[0].upper() + eq[1:]), "carbon", [ox, m, "carbon dioxide"], "Oxidation is the gain of oxygen.")
    return item("%s. Why can carbon be used?" % (eq[0].upper() + eq[1:]), "Carbon is more reactive than %s." % m, ["Carbon is less reactive than %s." % m, "Carbon is a metal.", "%s is above carbon in the series." % m.capitalize()], "Displacement of the metal from its oxide.")


ORE = [("haematite", "iron oxide", "iron"), ("bauxite", "aluminium oxide", "aluminium"), ("malachite", "copper carbonate", "copper"), ("galena", "lead sulfide", "lead"), ("cassiterite", "tin oxide", "tin")]


def g_ore():
    o, c, m = R.choice(ORE)
    if not once(("or", o)):
        return None
    return item("Which metal is extracted from the ore %s (%s)?" % (o, c), m, R.sample([x[2] for x in ORE if x[2] != m], 3), "An ore is a rock with enough metal compound to be worth extracting.")


def g_rec():
    who = P.next()[0]
    m = R.choice(["aluminium", "steel", "copper"])
    save = {"aluminium": 95, "steel": 70, "copper": 85}[m]
    k = R.choice(["save", "why", "left"])
    if not once(("rc", m, k)):
        return None
    if k == "save":
        return item("%s reads that recycling %s uses about %d%% less energy than extracting it from ore. If extracting 1 tonne uses 100 units of energy, about how much does recycling 1 tonne use?" % (who, m, save),
                    "%d units" % (100 - save), ["%d units" % save, "100 units", "%d units" % (100 + save)], "100 − %d = %d." % (save, 100 - save))
    if k == "why":
        return item("Why is recycling %s a good idea?" % m, "It saves ore and energy and reduces waste and mining damage.", ["It uses more energy than mining.", "Ores never run out.", "Recycled metal is weaker."], "Conserving resources.")
    return item("Why are metal ores described as a limited resource?", "There is a fixed amount in the Earth's crust and it took millions of years to form.", ["New ore forms every year.", "Ores are made by plants.", "They can be grown in labs cheaply."], "Finite.") if once(("lim",)) else None


B1 = bank([
    ("Why are carbon and hydrogen included in the reactivity series even though they are not metals?", "to compare which metals they can displace from compounds", ["because they are metals", "to make the list longer", "because they are the most reactive"], "Useful reference points."),
    ("What is reduction?", "the loss of oxygen from a substance", ["the gain of oxygen", "the loss of mass", "the gain of water"], "Opposite of oxidation."),
    ("What is oxidation?", "the gain of oxygen by a substance", ["the loss of oxygen", "dissolving in water", "the loss of electrons only in metals"], "Rusting and burning."),
    ("Why is aluminium extracted by electrolysis and not with carbon?", "Aluminium is more reactive than carbon.", ["Aluminium is less reactive than carbon.", "Carbon is too expensive.", "Aluminium is found pure."], "Above carbon."),
    ("Why is gold found as the pure metal in the ground?", "It is so unreactive that it does not form compounds easily.", ["It is very reactive.", "It is extracted by electrolysis.", "It reacts with rock."], "Bottom of the series."),
])
B5 = bank([
    ("Why is electrolysis an expensive way to extract metals?", "It uses a lot of electricity.", ["It needs no energy.", "It uses gold.", "It is done by hand."], "Energy cost."),
    ("In a blast furnace, what is used to reduce iron oxide?", "carbon (as coke)", ["oxygen", "aluminium", "water"], "Heated with limestone."),
    ("Which metal was used first by ancient people?", "gold and copper, because they are found pure or are easy to extract", ["aluminium, because it is common", "sodium", "potassium"], "History of metals."),
    ("Why was aluminium once more valuable than gold?", "It was very hard to extract before electrolysis was developed.", ["It is rarer than gold.", "It is magnetic.", "It is very heavy."], "Discovered in the 1800s."),
    ("What is the test for a metal reacting more vigorously with acid?", "More bubbles of hydrogen are given off, faster.", ["The acid turns blue.", "It makes oxygen.", "It gets colder."], "Compare reactivity."),
])


def body():
    think = ("<p><b>A metal's position in the reactivity series decides how it is extracted.</b></p>"
             "<ul><li>Series: K, Na, Ca, Mg, Al, (C), Zn, Fe, Sn, Pb, (H), Cu, Ag, Au.</li>"
             "<li>Above carbon: electrolysis. Below carbon: heat the oxide with carbon (reduction). Gold and silver are found pure.</li>"
             "<li>Reduction is loss of oxygen; oxidation is gain of oxygen. Recycling saves ore and energy.</li></ul>")
    ex = [("Zinc: extraction method?", ["Below carbon"], "heat the oxide with carbon"),
          ("Copper oxide + carbon: what is reduced?", ["It loses oxygen"], "copper oxide")]
    mist = ["Thinking aluminium can be extracted with carbon.", "Mixing up reduction and oxidation.", "Thinking recycling saves no energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The reactivity series", B1[:1] + [(M8.g_rs, 10), (us_act, 9)]),
        ("Extracting metals", B1[1:] + [(g_ext, 11), (g_ore, 4), (g_rec, 1)]),
        ("Oxidation and reduction", [(g_red, 16), (us_act, 4)]),
        ("Displacement", [(us_act, 8), (M8.g_rs, 8), (M8.g_acid, 4)]),
        ("Resources and recycling", B5 + [(g_rec, 5), (us_use, 6), (us_origin, 3), (g_red, 1)]),
    ])
    make_ks3(9, "reactivity-and-extraction", 5, "Chemistry", "Materials",
             "The order of metals and carbon in the reactivity series; the use of carbon in obtaining metals from metal oxides; displacement reactions; Earth as a source of limited resources and the efficacy of recycling.",
             "Reactivity and Extraction of Metals",
             "Year 9 Science: Reactivity Series and Extraction of Metals Worksheets",
             "Reactivity and Extraction",
             "Free Year 9 science worksheets on the reactivity series and extraction of metals: carbon and hydrogen in the series, displacement, oxidation and reduction, electrolysis, ores and recycling. 100 questions with answers.",
             "Carbon can extract metals below it.",
             "Metals above carbon need electrolysis; reduction is the loss of oxygen.",
             body(),
             [("How do you know which method to use to extract a metal?", "Look at the reactivity series. Metals more reactive than carbon are extracted by electrolysis; less reactive ones by heating their oxide with carbon."),
              ("What is the difference between oxidation and reduction?", "Oxidation is the gain of oxygen; reduction is the loss of oxygen. In iron oxide + carbon → iron + carbon dioxide, iron oxide is reduced and carbon is oxidised."),
              ("Why should metals be recycled?", "Ores are limited, and recycling uses far less energy than extracting new metal. Recycling aluminium saves about 95% of the energy.")],
             sets)


if __name__ == "__main__":
    main()
