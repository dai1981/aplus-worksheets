# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Chemistry): The Periodic Table
  python tools/gen_uk_science_y8_periodic_table.py
Groups and periods, Mendeleev's table, where metals and non-metals are, and patterns in group 1 (alkali metals),
group 7 (halogens) and group 0 (noble gases): physical properties, reactions with water, displacement and uses.
Group numbers use the UK school numbering (1–7 and 0). Reuses the classification, family and reactivity questions
of the US Chemistry unit in British English.
Wrong answers come from real mistakes: "a period is a column", "elements in the same period react alike",
"reactivity increases down group 7", "noble gases react easily".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_chem import EL, MAIN

U = Unit(61806)
R = U.R
P = People(R)
uk_sci.USED.clear()
PT = adopt_us("gen_us_science_chem_periodic_table_and_trends", U)
us_class, us_fam, us_react = ukm(PT.g_class), ukm(PT.g_fam), ukm(PT.g_react)
UKG = {1: "1", 2: "2", 13: "3", 14: "4", 15: "5", 16: "6", 17: "7", 18: "0"}
EZ = [e for e in MAIN if e[2] <= 36]


def _g_group():
    e = R.choice(EZ)
    k = R.random() < 0.5
    if not once(("gr", e[0], k)):
        return None
    if k:
        g = UKG[e[5]]
        return item("Which group of the periodic table is %s (%s) in?" % (e[1], e[0]), "group " + g, ["group " + x for x in R.sample([v for v in UKG.values() if v != g], 3)],
                    "Groups are columns. %s has the same number of outer electrons as the other elements in its group." % e[1].capitalize())
    p = e[6]
    return item("Which period (row) of the periodic table is %s (%s) in?" % (e[1], e[0]), "period %d" % p, ["period %d" % x for x in R.sample([v for v in (1, 2, 3, 4, 5) if v != p], 3)],
                "Periods are rows. Count down from hydrogen and helium in period 1.")


g_group = ukm(_g_group)


G1 = [("lithium", "fizzes steadily and moves slowly on the surface"), ("sodium", "melts into a ball and whizzes around"), ("potassium", "bursts into a lilac flame")]
G7 = [("fluorine", "pale yellow gas"), ("chlorine", "green gas"), ("bromine", "red-brown liquid"), ("iodine", "grey-black solid")]


def g_g1():
    k = R.choice(["obs", "prod", "trend", "store", "name", "pred"])
    m, obs = R.choice(G1)
    if not once(("g1", k, m if k == "obs" else "")):
        return None
    if k == "obs":
        return item("What do you see when a small piece of %s is put in water?" % m, "It " + obs + ".", ["It " + x[1] + "." for x in G1 if x[0] != m] + ["Nothing happens."], "Reactivity increases down group 1.")
    if k == "prod":
        return item("When sodium reacts with water, what are the products?", "sodium hydroxide and hydrogen", ["sodium chloride and oxygen", "sodium oxide and carbon dioxide", "only steam"], "metal + water → metal hydroxide + hydrogen.")
    if k == "trend":
        return item("How does the reactivity of the alkali metals change going down group 1?", "It increases.", ["It decreases.", "It stays the same.", "It goes up then down."], "Lithium < sodium < potassium.")
    if k == "store":
        return item("Why are lithium, sodium and potassium stored under oil?", "to stop them reacting with air and water", ["to keep them warm", "to make them shiny", "because they are liquids"], "Very reactive.")
    if k == "name":
        return item("What is the name for the elements in group 1?", "the alkali metals", ["the halogens", "the noble gases", "the transition metals"], "They make alkaline solutions with water.")
    return item("Rubidium is below potassium in group 1. How would it react with water?", "even more violently than potassium", ["more slowly than lithium", "not at all", "exactly like lithium"], "Predict from the trend.")


def g_g7():
    k = R.choice(["state", "trend", "disp", "nodisp", "name", "astat", "use"])
    h, st = R.choice(G7)
    if not once(("g7", k, h if k == "state" else "")):
        return None
    if k == "state":
        return item("What is %s like at room temperature?" % h, "a " + st, ["a " + x[1] for x in G7 if x[0] != h], "Going down group 7 the halogens get darker and their melting points rise.")
    if k == "trend":
        return item("How does the reactivity of the halogens change going down group 7?", "It decreases.", ["It increases.", "It stays the same.", "It goes up then down."], "Fluorine is the most reactive.")
    if k == "disp":
        return item("Chlorine water is added to potassium bromide solution and the solution turns orange. Why?", "Chlorine is more reactive and displaces bromine.", ["Bromine displaces chlorine.", "No reaction happens.", "Potassium turns orange."], "A more reactive halogen displaces a less reactive one.")
    if k == "nodisp":
        return item("Iodine solution is added to potassium chloride solution. What happens?", "Nothing, because iodine is less reactive than chlorine.", ["Iodine displaces chlorine.", "Chlorine gas bubbles off.", "The solution turns green."], "No displacement.")
    if k == "name":
        return item("What is the name for the elements in group 7?", "the halogens", ["the alkali metals", "the noble gases", "the metalloids"], "Halogen means salt-maker.")
    if k == "astat":
        return item("Astatine is at the bottom of group 7. What would you predict about it?", "a dark solid that is less reactive than iodine", ["a pale gas more reactive than fluorine", "a shiny metal", "a noble gas"], "Use the trends.")
    return item("Why is chlorine added to swimming pool water?", "It kills bacteria.", ["It makes the water warm.", "It adds colour.", "It removes salt."], "Halogens are toxic to microbes.")


B1 = bank([
    ("In the periodic table, what is a group?", "a column of elements with similar properties", ["a row of elements", "a type of compound", "a mixture of metals"], "Groups are vertical."),
    ("In the periodic table, what is a period?", "a row of elements", ["a column of elements", "the time an element lasts", "a group of noble gases"], "Periods are horizontal."),
    ("Where are the metals in the periodic table?", "on the left and in the middle", ["on the far right", "only in the top row", "only at the bottom"], "Non-metals are on the right."),
    ("How did Mendeleev arrange the elements?", "in order of atomic mass, grouping elements with similar properties", ["alphabetically", "by colour", "by the date they were found"], "He left gaps."),
    ("Why did Mendeleev leave gaps in his table?", "for elements that had not been discovered yet", ["to make it look neat", "because he ran out of space", "for compounds"], "He predicted their properties."),
    ("What is the modern periodic table arranged by?", "atomic number (number of protons)", ["atomic mass only", "date of discovery", "colour"], "Increasing atomic number."),
])
B5 = bank([
    ("Why are the noble gases (group 0) unreactive?", "Their atoms have full outer shells of electrons.", ["They are very heavy.", "They are metals.", "They are always hot."], "Stable."),
    ("Why is helium used in party balloons?", "It is less dense than air and does not burn.", ["It is heavier than air.", "It burns brightly.", "It is green."], "Safe and light."),
    ("Why is argon used inside some light bulbs?", "It is unreactive, so the hot filament does not burn away.", ["It glows red.", "It is a fuel.", "It conducts heat away."], "Inert gas."),
    ("Which property do all group 1 metals share?", "They are soft and can be cut with a knife.", ["They are hard and dull.", "They are gases.", "They do not react with water."], "Soft, shiny when cut."),
    ("Why does the shiny surface of freshly cut sodium go dull?", "It reacts quickly with oxygen in the air.", ["It melts.", "It dries out.", "It absorbs light."], "Oxidation."),
    ("Element X is a shiny solid that conducts electricity. Where is it most likely to be in the periodic table?", "on the left or in the middle", ["in group 0", "in group 7", "on the far right"], "Metals."),
])


def body():
    think = ("<p><b>The periodic table puts elements with similar properties in the same group.</b></p>"
             "<ul><li>Groups are columns, periods are rows. Metals are on the left and in the middle; non-metals are on the right.</li>"
             "<li>Group 1 (alkali metals) get more reactive going down. Group 7 (halogens) get less reactive going down.</li>"
             "<li>Group 0 (noble gases) are very unreactive.</li></ul>")
    ex = [("Potassium or lithium: more reactive?", ["Lower in group 1"], "potassium"),
          ("Chlorine or iodine: more reactive?", ["Higher in group 7"], "chlorine")]
    mist = ["Mixing up groups (columns) and periods (rows).", "Thinking reactivity increases down group 7.", "Thinking noble gases react easily."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Groups and periods", B1 + [(g_group, 14)]),
        ("Metals and non-metals", [(us_class, 12), (g_group, 8)]),
        ("Group 1", [(g_g1, 7), (us_react, 4), (us_fam, 9)]),
        ("Group 7", [(g_g7, 9), (us_react, 4), (us_fam, 7)]),
        ("Group 0 and predictions", B5 + [(us_fam, 6), (us_class, 4), (g_group, 4)]),
    ])
    make_ks3(8, "periodic-table", 6, "Chemistry", "The Periodic Table",
             "The varying physical and chemical properties of different elements; the principles underpinning the Mendeleev Periodic Table; the Periodic Table: periods and groups; metals and non-metals; how patterns in reactions can be predicted with reference to the Periodic Table; the properties of metals and non-metals.",
             "The Periodic Table",
             "Year 8 Science: Periodic Table Worksheets (Groups, Periods, Alkali Metals, Halogens)",
             "Periodic Table",
             "Free Year 8 science worksheets on the periodic table: groups and periods, Mendeleev, metals and non-metals, alkali metals, halogens and noble gases. 100 questions with answers.",
             "Elements in a group have similar properties.",
             "Group 1 gets more reactive going down; group 7 gets less reactive.",
             body(),
             [("What is the difference between a group and a period?", "A group is a column of elements with similar properties. A period is a row."),
              ("How do group 1 metals react with water?", "They fizz and make a metal hydroxide and hydrogen gas. Lithium reacts gently, sodium faster and potassium bursts into a lilac flame."),
              ("What is a displacement reaction of halogens?", "A more reactive halogen takes the place of a less reactive one in a compound, for example chlorine displaces bromine from potassium bromide.")],
             sets)


if __name__ == "__main__":
    main()
