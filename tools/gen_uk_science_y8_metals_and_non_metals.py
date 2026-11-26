# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Chemistry): Metals and Non-metals
  python tools/gen_uk_science_y8_metals_and_non_metals.py
The properties of metals and non-metals, the reactions of metals with acids (salt + hydrogen) and with oxygen
(metal oxides), naming salts, the reactivity series, displacement reactions, and the reactions of metal and non-metal
oxides with water (alkaline and acidic). Reuses the displacement question of the US Chemistry unit in British English.
Wrong answers come from real mistakes: "all metals are magnetic", "gold reacts quickly with acid", "the gas is oxygen",
"a less reactive metal can displace a more reactive one".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us

U = Unit(61807)
R = U.R
P = People(R)
uk_sci.USED.clear()
TR = adopt_us("gen_us_science_chem_types_of_chemical_reactions", U)
us_act = ukm(TR.g_act)

PROP = [("is shiny when freshly cut", "metals"), ("conducts electricity well", "metals"), ("conducts heat well", "metals"), ("is malleable (can be hammered into shape)", "metals"),
        ("is ductile (can be pulled into wires)", "metals"), ("is sonorous (rings when hit)", "metals"), ("has a high density", "metals"),
        ("is brittle as a solid", "non-metals"), ("is dull", "non-metals"), ("is a poor conductor of heat", "non-metals"), ("is a gas at room temperature, like most of the elements in this group", "non-metals"),
        ("forms acidic oxides", "non-metals"), ("forms basic oxides", "metals")]


def g_prop():
    p, a = R.choice(PROP)
    if not once(("pr", p)):
        return None
    return item("Which type of element usually %s?" % p, a, [x for x in ["metals", "non-metals", "both metals and non-metals", "neither"] if x != a],
                "Metals: shiny, conduct, malleable, ductile, sonorous. Non-metals: dull, brittle, poor conductors (graphite is an exception).")


MET = ["magnesium", "zinc", "iron", "calcium", "aluminium"]
ACID = [("hydrochloric acid", "chloride"), ("sulfuric acid", "sulfate"), ("nitric acid", "nitrate")]


def g_acid():
    m = R.choice(MET)
    ac, an = R.choice(ACID)
    k = R.choice(["salt", "gas", "salt", "test"])
    if k == "test":
        if not once(("ac", "test", m)):
            return None
        return item("%s reacts with %s and bubbles of gas are given off. How can you test for this gas?" % (m.capitalize(), ac), "A lit splint gives a squeaky pop.",
                    ["A glowing splint relights.", "Limewater turns milky.", "Damp litmus paper is bleached."], "Hydrogen burns with a squeaky pop.")
    if not once(("ac", m, ac, k)):
        return None
    if k == "gas":
        return item("Which gas is made when %s reacts with %s?" % (m, ac), "hydrogen", ["oxygen", "carbon dioxide", "chlorine"], "metal + acid → salt + hydrogen.")
    salt = "%s %s" % (m, an)
    w = ["%s %s" % (m, x[1]) for x in ACID if x[1] != an] + ["%s oxide" % m]
    return item("Complete the word equation: %s + %s → ? + hydrogen" % (m, ac), salt, w, "Hydrochloric → chloride, sulfuric → sulfate, nitric → nitrate.")


def g_oxide():
    k = R.random() < 0.5
    m = R.choice(MET + ["copper", "sodium", "potassium"] if k else ["sodium", "potassium", "calcium", "magnesium", "lithium"])
    if not once(("ox", m, k)):
        return None
    if k:
        return item("What is made when %s reacts with oxygen?" % m, "%s oxide" % m, ["%s hydroxide" % m, "%s chloride" % m, "%s carbonate" % m], "metal + oxygen → metal oxide.")
    return item("%s oxide is added to water with universal indicator. What colour is the indicator likely to be?" % m.capitalize(), "blue or purple (alkaline)", ["red (acidic)", "green (neutral)", "colourless"],
                "Metal oxides that dissolve make alkaline solutions.")


NMOX = [("carbon dioxide", "carbon"), ("sulfur dioxide", "sulfur"), ("nitrogen dioxide", "nitrogen"), ("phosphorus oxide", "phosphorus")]


def g_nmox():
    o, e = R.choice(NMOX)
    k = R.random() < 0.5
    if not once(("nm", o, k)):
        return None
    if k:
        return item("%s dissolves in water. What kind of solution does it make?" % o.capitalize(), "an acidic solution", ["an alkaline solution", "a neutral solution", "a metal"], "Non-metal oxides are acidic.")
    return item("Which oxide forms when %s burns in oxygen?" % e, o, R.sample([x[0] for x in NMOX if x[0] != o] + ["water"], 3), "non-metal + oxygen → non-metal oxide.")


RS = ["potassium", "sodium", "calcium", "magnesium", "aluminium", "zinc", "iron", "copper", "silver", "gold"]


def g_rs():
    a, b = sorted(R.sample(range(len(RS)), 2))
    k = R.random() < 0.5
    if not once(("rs", a, b, k)):
        return None
    tab = table(["Reactivity series (most reactive first)"], [[", ".join(RS)]])
    if k:
        return item(tab + "Which is more reactive, %s or %s?" % (RS[b], RS[a]), RS[a], [RS[b], "They are equally reactive.", "Neither reacts with anything."], "Higher in the series means more reactive.")
    return item(tab + "Will %s displace %s from a solution of one of its compounds?" % (RS[b], RS[a]), "No, because %s is less reactive than %s." % (RS[b], RS[a]),
                ["Yes, because %s is less reactive." % RS[b], "Yes, any metal displaces any other.", "Only if the solution is cold."], "Only a more reactive metal displaces a less reactive one.")


B1 = bank([
    ("Which non-metal conducts electricity?", "graphite (a form of carbon)", ["sulfur", "oxygen", "iodine"], "An exception."),
    ("Which metal is a liquid at room temperature?", "mercury", ["iron", "copper", "sodium"], "Another exception."),
    ("Are all metals magnetic?", "No. Only iron, nickel and cobalt (and steel) are magnetic.", ["Yes, all metals are.", "Only gold is.", "Only shiny metals are."], "Test with a magnet."),
    ("Why is copper used for electrical wires?", "It conducts electricity well and is ductile.", ["It is magnetic.", "It is brittle.", "It is an insulator."], "Properties fit uses."),
    ("Why are saucepans made of metal?", "Metals are good conductors of heat.", ["Metals are insulators.", "Metals are brittle.", "Metals are dull."], "Heat reaches the food."),
])
B5 = bank([
    ("Why does gold not react with acids?", "It is very low in the reactivity series.", ["It is too heavy.", "It is a non-metal.", "It is magnetic."], "Found pure in nature."),
    ("Why is iron extracted from its ore by heating with carbon?", "Carbon is more reactive than iron, so it displaces iron from iron oxide.", ["Carbon is a metal.", "Iron is more reactive than carbon.", "Heat alone splits it."], "Carbon in the reactivity series."),
    ("Iron nails are put in copper sulfate solution. A pink-brown coating forms. What is it?", "copper, displaced by the more reactive iron", ["rust", "iron sulfate crystals", "sulfur"], "Displacement."),
    ("What is the test for an alkaline solution with universal indicator?", "It turns blue or purple.", ["It turns red.", "It turns green.", "It turns orange."], "pH above 7."),
    ("Which metal would react most violently with dilute acid?", "potassium (it should never be added to acid in school)", ["copper", "gold", "silver"], "Top of the series."),
])


def body():
    think = ("<p><b>Metals and non-metals have different properties and reactions.</b></p>"
             "<ul><li>Metals are shiny, conduct heat and electricity, and are malleable. Non-metals are usually dull, brittle and poor conductors.</li>"
             "<li>metal + acid → salt + hydrogen; metal + oxygen → metal oxide. Metal oxides are basic; non-metal oxides are acidic.</li>"
             "<li>A more reactive metal displaces a less reactive metal from its compounds.</li></ul>")
    ex = [("Zinc + sulfuric acid → ?", ["Sulfuric → sulfate"], "zinc sulfate + hydrogen"),
          ("Copper in magnesium sulfate: reaction?", ["Copper is less reactive"], "no reaction")]
    mist = ["Thinking all metals are magnetic.", "Thinking the gas from metal + acid is oxygen.", "Thinking a less reactive metal can displace a more reactive one."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Properties", B1 + [(g_prop, 11), (g_nmox, 3), (g_oxide, 1)]),
        ("Metals and acids", [(g_acid, 16), (g_prop, 1), (g_oxide, 3)]),
        ("Metals and oxygen", [(g_oxide, 10), (g_nmox, 4), (g_acid, 6)]),
        ("Reactivity series", [(g_rs, 14), (us_act, 6)]),
        ("Displacement", B5 + [(us_act, 8), (g_rs, 7)]),
    ])
    make_ks3(8, "metals-and-non-metals", 7, "Chemistry", "Metals and non-metals",
             "The order of metals and carbon in the reactivity series; the use of carbon in obtaining metals from metal oxides; properties of ceramics, polymers and composites (qualitative); the chemical properties of metal and non-metal oxides with respect to acidity; reactions of acids with metals to produce a salt plus hydrogen; displacement reactions.",
             "Metals and Non-metals",
             "Year 8 Science: Metals and Non-metals Worksheets (Reactivity Series, Acids, Oxides)",
             "Metals and Non-metals",
             "Free Year 8 science worksheets on metals and non-metals: properties, metals with acids and oxygen, naming salts, acidic and basic oxides, the reactivity series and displacement. 100 questions with answers.",
             "metal + acid → salt + hydrogen.",
             "A more reactive metal displaces a less reactive one.",
             body(),
             [("What is made when a metal reacts with an acid?", "A salt and hydrogen gas. For example, magnesium + hydrochloric acid → magnesium chloride + hydrogen."),
              ("How do you name the salt?", "The metal's name comes first. Hydrochloric acid makes chlorides, sulfuric acid makes sulfates and nitric acid makes nitrates."),
              ("What is a displacement reaction?", "A more reactive metal takes the place of a less reactive metal in a compound, for example iron + copper sulfate → iron sulfate + copper.")],
             sets)


if __name__ == "__main__":
    main()
