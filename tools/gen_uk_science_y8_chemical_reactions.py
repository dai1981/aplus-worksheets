# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Chemistry): Chemical Reactions
  python tools/gen_uk_science_y8_chemical_reactions.py
Chemical reactions as the rearrangement of atoms, signs of a reaction, word and simple symbol equations, conservation
of mass, types of reaction (combustion, thermal decomposition, oxidation, neutralisation, displacement), exothermic and
endothermic changes, and physical versus chemical changes. Reuses the change, conservation, balancing and energy
questions of the US Grade 7 units in British English.
Wrong answers come from real mistakes: "mass is lost when something burns", "melting is a chemical change",
"atoms are destroyed in a reaction", "endothermic reactions get hotter".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us

U = Unit(61808)
R = U.R
P = People(R)
uk_sci.USED.clear()
PC = adopt_us("gen_us_science_g7_properties_and_chemical_reactions", U)
CA = adopt_us("gen_us_science_g7_conservation_of_atoms", U)
EN = adopt_us("gen_us_science_g7_energy_in_chemical_reactions", U)
us_kind, us_which = ukm(PC.g_kind), ukm(PC.g_which)
us_bal, us_count, us_mass, us_miss = ukm(CA.g_balanced), ukm(CA.g_count), ukm(CA.g_mass), ukm(CA.g_missing)
us_exo, us_edata = ukm(EN.g_kind), ukm(EN.g_data)

EQS = [("methane + oxygen → carbon dioxide + water", "combustion"), ("carbon + oxygen → carbon dioxide", "combustion"), ("hydrogen + oxygen → water", "combustion"),
       ("calcium carbonate → calcium oxide + carbon dioxide", "thermal decomposition"), ("copper carbonate → copper oxide + carbon dioxide", "thermal decomposition"),
       ("zinc carbonate → zinc oxide + carbon dioxide", "thermal decomposition"), ("iron + oxygen → iron oxide", "oxidation"), ("copper + oxygen → copper oxide", "oxidation"),
       ("hydrochloric acid + sodium hydroxide → sodium chloride + water", "neutralisation"), ("sulfuric acid + potassium hydroxide → potassium sulfate + water", "neutralisation"),
       ("magnesium + copper sulfate → magnesium sulfate + copper", "displacement"), ("zinc + copper chloride → zinc chloride + copper", "displacement")]
TYPES = ["combustion", "thermal decomposition", "oxidation", "neutralisation", "displacement"]


def g_type():
    e, t = R.choice(EQS)
    if not once(("ty", e)):
        return None
    w = [x for x in TYPES if x != t]
    if t == "combustion":
        w = [x for x in w if x != "oxidation"]
    if t == "oxidation":
        w = [x for x in w if x != "combustion"]
    return item("Which type of reaction is this? %s" % e, t, R.sample(w, 3),
                "Combustion: burning in oxygen. Thermal decomposition: heat breaks one compound into simpler ones. Neutralisation: acid + alkali → salt + water.")


SIGN = [("A gas is given off (fizzing).", True), ("The colour changes, for example blue copper sulfate turns colourless.", True), ("The temperature changes.", True),
        ("A solid (precipitate) forms when two solutions are mixed.", True), ("Light is given out.", True),
        ("Ice melts into water.", False), ("Salt dissolves in water.", False), ("Water boils.", False), ("A glass breaks into pieces.", False), ("Wax melts.", False)]


def g_sign():
    s, yes = R.choice(SIGN)
    if not once(("si", s)):
        return None
    a = "It is a sign of a chemical reaction (a new substance may have formed)." if yes else "It is a physical change, not a sign of a new substance."
    b = "It is a physical change, not a sign of a new substance." if yes else "It is a sign of a chemical reaction (a new substance may have formed)."
    return item("%s What does this observation tell you?" % s, a, [b, "Atoms have been destroyed.", "Mass has been created."], "Look for new substances.")


FUEL = [("methane (natural gas)", "carbon dioxide and water"), ("propane", "carbon dioxide and water"), ("hydrogen", "water only"), ("carbon (charcoal)", "carbon dioxide"),
        ("sulfur", "sulfur dioxide"), ("magnesium", "magnesium oxide"), ("candle wax (a hydrocarbon)", "carbon dioxide and water")]


def g_burn():
    f, p = R.choice(FUEL)
    if not once(("bu", f)):
        return None
    return item("What is made when %s burns completely in plenty of oxygen?" % f, p, R.sample(sorted({x[1] for x in FUEL if x[1] != p}), 3),
                "Hydrocarbons burn to carbon dioxide and water.")


def g_cons():
    who = P.next()[0]
    k = R.choice(["open", "closed", "mg"])
    a = R.choice([20, 25, 30, 40, 50, 60])
    b = R.choice([5, 8, 10, 12, 15])
    if not once(("co", k, a, b)) or not once(("co", k), 5):
        return None
    if k == "closed":
        g = "%d g" % (a + b)
        return item("%s mixes %d g of one solution with %d g of another in a sealed flask. A precipitate forms. What is the total mass after the reaction?" % (who, a, b), g,
                    ["%d g" % (a + b - 3), "%d g" % a, "%d g" % (a + b + 5)], "Mass is conserved: no atoms are created or destroyed.")
    if k == "open":
        g = "%d g" % (a - b // 5 - 1)
        lost = b // 5 + 1
        return item("%s puts %d g of marble chips and acid in an open flask. After the reaction it has a mass of %s. Why is it lighter?" % (who, a, g), "Carbon dioxide gas escaped into the air.",
                    ["Atoms were destroyed.", "The acid evaporated into nothing.", "Mass is not conserved in reactions."], "The gas leaves the open flask: %d g of it." % lost)
    m = a // 5 * 3
    o = m * 2 // 3
    g = "%d g" % (m + o)
    return item("%d g of magnesium burns in air and joins with %d g of oxygen. What mass of magnesium oxide forms?" % (m, o), g, ["%d g" % m, "%d g" % o, "%d g" % (m - o)],
                "The magnesium gains the mass of the oxygen: %d + %d." % (m, o))


B1 = bank([
    ("What happens to atoms in a chemical reaction?", "They are rearranged to make new substances.", ["They are destroyed.", "New atoms are created.", "They turn into energy."], "Same atoms, new arrangements."),
    ("What are the substances at the start of a reaction called?", "reactants", ["products", "catalysts", "solvents"], "Left of the arrow."),
    ("What are the substances made in a reaction called?", "products", ["reactants", "elements only", "mixtures"], "Right of the arrow."),
    ("In a word equation, what does the arrow mean?", "'reacts to make'", ["'equals' in maths", "'is mixed with'", "'is heated'"], "Reactants → products."),
    ("Is burning a chemical change or a physical change?", "a chemical change", ["a physical change", "neither", "both at once"], "New substances form."),
])
B5 = bank([
    ("What is an exothermic reaction?", "one that transfers energy to the surroundings, so they get warmer", ["one that takes in energy and gets colder", "one with no energy change", "one that needs light"], "Burning, respiration."),
    ("What is an endothermic reaction?", "one that takes in energy from the surroundings, so they get colder", ["one that gives out heat", "one that explodes", "one with no change"], "Sports cold packs."),
    ("What is the test for carbon dioxide?", "It turns limewater milky.", ["It relights a glowing splint.", "It makes a squeaky pop.", "It bleaches litmus."], "Thermal decomposition of carbonates."),
    ("What is the test for oxygen?", "It relights a glowing splint.", ["It turns limewater milky.", "It makes a squeaky pop.", "It turns indicator red."], "Supports burning."),
    ("What is a catalyst?", "a substance that speeds up a reaction without being used up", ["a reactant that is used up", "a product", "a substance that stops a reaction"], "Enzymes are biological catalysts."),
])


def body():
    think = ("<p><b>In a chemical reaction, atoms are rearranged to make new substances.</b></p>"
             "<ul><li>Signs: gas, colour change, temperature change, precipitate, light.</li>"
             "<li>Mass is conserved. If a gas escapes from an open container, the mass seems to fall.</li>"
             "<li>Types: combustion, thermal decomposition, oxidation, neutralisation, displacement. Exothermic reactions warm the surroundings; endothermic ones cool them.</li></ul>")
    ex = [("12 g magnesium + 8 g oxygen → ?", ["12 + 8"], "20 g magnesium oxide"),
          ("Copper carbonate heated → copper oxide + carbon dioxide. Type?", ["Heat breaks one compound"], "thermal decomposition")]
    mist = ["Thinking mass is lost when something burns.", "Thinking melting is a chemical change.", "Thinking endothermic reactions get hotter."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is a reaction?", B1 + [(g_sign, 9), (us_kind, 3), (us_which, 3)]),
        ("Types of reaction", [(g_type, 11), (g_burn, 6), (us_which, 3)]),
        ("Conservation of mass", [(g_cons, 10), (us_mass, 5), (us_count, 5)]),
        ("Equations", [(us_bal, 8), (us_miss, 8), (us_count, 4)]),
        ("Energy changes", B5 + [(us_exo, 8), (us_edata, 6), (g_burn, 1)]),
    ])
    make_ks3(8, "chemical-reactions", 8, "Chemistry", "Chemical reactions",
             "Chemical reactions as the rearrangement of atoms; representing chemical reactions using formulae and using equations; combustion, thermal decomposition, oxidation and displacement reactions; defining acids and alkalis in terms of neutralisation reactions; what catalysts do; energy changes on changes of state (qualitative); exothermic and endothermic chemical reactions (qualitative); the conservation of mass in changes of state and chemical reactions.",
             "Chemical Reactions",
             "Year 8 Science: Chemical Reactions Worksheets (Word Equations, Conservation of Mass)",
             "Chemical Reactions",
             "Free Year 8 science worksheets on chemical reactions: signs of a reaction, word and symbol equations, conservation of mass, combustion, thermal decomposition, oxidation, exothermic and endothermic. 100 questions with answers.",
             "Atoms are rearranged, not lost.",
             "Mass is conserved; reactions can warm or cool the surroundings.",
             body(),
             [("How do you know a chemical reaction has happened?", "A new substance forms. Signs include fizzing, a colour change, a temperature change, a precipitate or light."),
              ("Why does a burning candle seem to lose mass?", "The carbon dioxide and water vapour it makes escape into the air. If they were collected, the total mass would be the same."),
              ("What is thermal decomposition?", "A reaction where heat breaks one compound into simpler substances, for example calcium carbonate → calcium oxide + carbon dioxide.")],
             sets)


if __name__ == "__main__":
    main()
