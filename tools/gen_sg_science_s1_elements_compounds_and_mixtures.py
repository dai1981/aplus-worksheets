# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Diversity): Exploring Diversity of Matter by its Chemical Composition
  python tools/gen_sg_science_s1_elements_compounds_and_mixtures.py
Elements as the basic building blocks (metals and non-metals in the Periodic Table), compounds (elements chemically combined,
fixed proportions, new properties) and mixtures (not chemically combined, can be separated physically); solute, solvent and
solution; solutions and suspensions; factors that affect the rate of dissolving and solubility; classifying waste for recycling.
UK KS3 element and mixture makers are reused.
Wrong answers come from real mistakes: "a compound keeps the properties of its elements", "air is a compound",
"stirring increases solubility", "a suspension is a solution".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64103)
R = U.R
P = People(R)
EL = luse(U, "gen_uk_science_y7_elements_atoms_and_compounds", drop=[r"formula unit", r"atoms are there"])
MX = luse(U, "gen_uk_science_y7_mixtures_and_separation")

METALS = ["sodium", "magnesium", "aluminium", "iron", "copper", "zinc", "silver", "gold", "calcium", "potassium", "mercury", "lead"]
NONMETALS = ["oxygen", "nitrogen", "carbon", "sulfur", "chlorine", "hydrogen", "helium", "neon", "iodine", "phosphorus", "bromine", "argon"]


def g_metal():
    k = R.choice(["m", "n"])
    a = R.choice(METALS if k == "m" else NONMETALS)
    if not once(("mt", a)):
        return None
    w = R.sample(NONMETALS if k == "m" else METALS, 3)
    return item("Which of these elements is a %s?" % ("metal" if k == "m" else "non-metal"), a, w,
                "In the Periodic Table, metals are on the left and in the middle; non-metals are on the right.")


SOL = [("salt", "water", "salt solution"), ("sugar", "tea", "sweet tea"), ("copper(II) sulfate", "water", "a blue solution"),
       ("iodine", "alcohol", "tincture of iodine"), ("carbon dioxide", "water", "soda water"), ("Milo powder", "hot water", "a Milo drink"),
       ("instant coffee", "hot water", "coffee"), ("oil paint", "turpentine", "thinned paint")]


def g_sol():
    a, b, c = R.choice(SOL)
    k = R.choice(["solute", "solvent"])
    if not once(("sl", a, k)):
        return None
    ans = a if k == "solute" else b
    other = b if k == "solute" else a
    return item("When %s dissolves in %s to make %s, what is the %s?" % (a, b, c, k), ans, [other, c, "the container"],
                "The solute dissolves; the solvent does the dissolving; together they make the solution.")


FACT = [("stirring", "increases the rate of dissolving", "It brings fresh solvent to the solid."),
        ("using hot water instead of cold water", "increases the rate of dissolving", "Particles move faster at higher temperatures."),
        ("crushing the solid into a powder", "increases the rate of dissolving", "A larger surface area is in contact with the water."),
        ("using one large crystal instead of a fine powder", "decreases the rate of dissolving", "Less surface area is in contact with the solvent."),
        ("using cold water instead of hot water", "decreases the rate of dissolving", "Particles move more slowly."),
        ("not stirring the mixture", "decreases the rate of dissolving", "Solvent near the solid becomes saturated.")]


def g_rate():
    f, a, e = R.choice(FACT)
    if not once(("rt", f)):
        return None
    return item("A student is dissolving a solid in water. What is the effect of %s?" % f, "It %s." % a.replace("increases", "increases").replace("decreases", "decreases"),
                ["It %s." % x for x in ["increases the rate of dissolving", "decreases the rate of dissolving", "has no effect on the rate of dissolving", "stops the solid from dissolving"] if x != a][:3], e)


def g_solub():
    t = [20, 40, 60, 80]
    base = R.choice([30, 34, 36, 20])
    step = R.choice([4, 6, 8, 10, 12])
    vals = [base + i * step for i in range(4)]
    nm = P.next()[0]
    tb = table(["Temperature (°C)", "Mass of solid X that dissolves in 100 g of water (g)"], [[str(a), str(b)] for a, b in zip(t, vals)])
    k = R.choice(["trend", "read", "more"])
    if not once(("su", base, step, k)) or not once(("suk", k), 1 if k == "trend" else 4):
        return None
    if k == "trend":
        return item(tb + "%s measured the solubility of solid X. What does the table show?" % nm, "The solubility of X increases as the temperature increases.",
                    ["The solubility of X decreases as the temperature increases.", "Temperature does not affect the solubility of X.", "X is insoluble in water."], "More X dissolves at higher temperatures.")
    if k == "read":
        i = R.randrange(4)
        return item(tb + "%s measured the solubility of solid X. What mass of X can dissolve in 100 g of water at %d °C?" % (nm, t[i]), "%d g" % vals[i],
                    ["%d g" % vals[(i + 1) % 4], "%d g" % (vals[i] + t[i]), "%d g" % t[i]], "Read across from %d °C." % t[i])
    return item(tb + "%s dissolved %d g of X in 100 g of water at 80 °C, then cooled it to 20 °C. What mass of X would come out as crystals?" % (nm, vals[3]), "%d g" % (vals[3] - vals[0]),
                ["%d g" % vals[0], "%d g" % vals[3], "0 g"], "%d g − %d g = %d g cannot stay dissolved at 20 °C." % (vals[3], vals[0], vals[3] - vals[0]))


SUSP = [("muddy water", "a suspension"), ("chalk powder shaken in water", "a suspension"), ("salt water", "a solution"), ("sugar dissolved in water", "a solution"),
        ("soda water", "a solution"), ("flour stirred into water", "a suspension"), ("copper(II) sulfate dissolved in water", "a solution"), ("sand shaken in water", "a suspension")]


def g_susp():
    x, a = R.choice(SUSP)
    if not once(("sp", x)):
        return None
    return item("Is %s a solution or a suspension?" % x, a, [y for y in ["a solution", "a suspension", "a pure substance", "an element"] if y != a],
                "A solution is clear and does not settle; a suspension is cloudy, its solid particles settle and can be filtered." if a == "a suspension" else
                "The solute is dissolved, so the liquid is clear and nothing settles.")


B1 = bank([
    ("What is an element?", "a substance that cannot be broken down into simpler substances by chemical methods", ["a substance made of two kinds of atoms", "any mixture", "anything that dissolves"], "Elements are the basic building blocks of matter."),
    ("What is a compound?", "a substance made of two or more elements chemically combined", ["two elements mixed but not combined", "a single element", "any solution"], "Water is a compound of hydrogen and oxygen."),
    ("Which statement about mixtures is correct?", "The substances are not chemically combined and can be separated by physical methods.", ["They always have a fixed composition.", "They form new substances.", "They cannot be separated."], "Air, sea water and soil are mixtures."),
    ("Iron and sulfur are heated to form iron(II) sulfide. Which is true of the product?", "It has different properties from iron and sulfur.", ["It is still attracted to a magnet like iron.", "It is a mixture.", "It is an element."], "A compound has new properties."),
    ("Is air a compound or a mixture?", "a mixture, because its gases are not chemically combined", ["a compound, because it has oxygen", "an element", "a solution of water"], "The amounts of gases in air can vary."),
    ("What is a solution?", "a mixture formed when a solute dissolves in a solvent", ["a pure element", "a solid that does not dissolve", "a compound"], "Sea water is a solution."),
    ("Why should we sort waste into paper, plastic and metal before recycling?", "Different materials have different compositions and are recycled in different ways.", ["They all melt at the same temperature.", "It makes the waste heavier.", "Sorting is not needed."], "Singapore's blue bins take paper, plastic, metal and glass."),
    ("Melamine was illegally added to milk to make it seem higher in protein. What does this show?", "Knowing the chemical composition of food helps to keep it safe.", ["All chemicals in food are harmful.", "Milk has no protein.", "Melamine is a vitamin."], "Food testing checks what is really in food."),
])
B5 = bank([
    ("A substance melts sharply at 801 °C and cannot be split by heating. Which is it most likely to be?", "a pure substance", ["a mixture", "a suspension", "a solution"], "Pure substances have fixed melting points."),
    ("Iron filings and sulfur powder are mixed. Which method can separate them?", "using a magnet", ["heating them strongly", "filtering", "they cannot be separated"], "In a mixture, iron keeps its magnetic property."),
    ("A sugar cube dissolves faster in hot tea than in iced tea. Why?", "Particles move faster at higher temperatures.", ["Hot tea has more sugar.", "Ice stops all dissolving.", "Sugar is a gas."], "Temperature affects the rate of dissolving."),
    ("A student adds salt to water until no more dissolves. What kind of solution is this?", "a saturated solution", ["a suspension", "a pure substance", "a dilute solution"], "Extra salt stays at the bottom."),
    ("Sea water has a mass of 500 g and contains 17.5 g of salt. What is the mass of water?", "482.5 g", ["517.5 g", "500 g", "17.5 g"], "500 − 17.5 = 482.5 g."),
    ("Which is a compound?", "carbon dioxide", ["oxygen", "air", "salt water"], "Carbon and oxygen are chemically combined."),
])


def body():
    think = ("<p><b>All matter is made of elements. Elements combine to form compounds, or mix without combining to form mixtures.</b></p>"
             "<ul><li><b>Element</b>: cannot be broken down chemically. Metals are on the left of the Periodic Table, non-metals on the right.</li>"
             "<li><b>Compound</b>: elements chemically combined in a fixed ratio; it has new properties (water, carbon dioxide).</li>"
             "<li><b>Mixture</b>: not chemically combined; can be separated physically (air, sea water).</li>"
             "<li>A <b>solute</b> dissolves in a <b>solvent</b> to form a <b>solution</b>. Stirring, heat and smaller pieces dissolve a solid faster.</li></ul>")
    ex = [("Salt dissolves in water. Which is the solute?", ["The substance that dissolves"], "salt"),
          ("Iron and sulfur heated together form a black solid that is not magnetic. Element, compound or mixture?", ["New properties, cannot be separated by a magnet"], "a compound")]
    mist = ["Thinking a compound keeps the properties of its elements.", "Calling air a compound. It is a mixture of gases.",
            "Mixing up the rate of dissolving and solubility. Stirring is faster, but the same mass dissolves.", "Calling muddy water a solution. It is a suspension."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Elements, compounds and mixtures", B1[:5] + EL.B1 + [(EL.g_class, 7)]),
        ("Metals, non-metals and symbols", [(g_metal, 8), (EL.g_sym, 8), (EL.g_name, 4)]),
        ("Solutions and suspensions", B1[5:6] + [(g_sol, 8), (g_susp, 6), (MX.g_voc, 3), (MX.g_mass, 2)]),
        ("Dissolving and solubility", [(g_rate, 6), (g_solub, 8), (EL.g_class, 3), (g_metal, 3)]),
        ("Exam-style questions", B5 + B1[6:] + EL.B5 + [(g_solub, 1), (g_sol, 3), (g_susp, 2)]),
    ])
    make_lss(1, "elements-compounds-and-mixtures", 3, "Diversity", "Exploring Diversity of Matter by its Chemical Composition",
             "Describe elements as the basic building blocks of matter and recognise metals and non-metals in the Periodic Table; describe compounds as two or more elements chemically "
             "combined and mixtures as substances not chemically combined; distinguish solute, solvent and solution, and solutions and suspensions; investigate factors that affect "
             "the rate of dissolving and solubility (summary of the MOE Lower Secondary Science Syllabus).",
             "Elements, Compounds and Mixtures", seo(1, "Elements, Compounds and Mixtures"), "Elements, compounds, mixtures",
             "Free Secondary 1 science worksheets for Singapore students on elements, compounds and mixtures: metals and non-metals, chemical symbols, solutions, suspensions and solubility. With answers.",
             "Compound: chemically combined. Mixture: not combined.", "Solute + solvent = solution.",
             body(),
             [("What is the difference between a compound and a mixture?", "In a compound the elements are chemically combined in a fixed ratio and have new properties. In a mixture they are not combined and can be separated physically."),
              ("What affects how fast a solid dissolves?", "Stirring, a higher temperature and smaller pieces (a larger surface area) make it dissolve faster."),
              ("What is the difference between a solution and a suspension?", "A solution is clear and nothing settles. A suspension is cloudy; its particles settle and can be filtered out.")],
             sets)


if __name__ == "__main__":
    main()
