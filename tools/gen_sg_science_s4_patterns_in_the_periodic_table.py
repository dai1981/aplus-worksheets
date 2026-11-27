# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 8: Patterns in the Periodic Table
  python tools/gen_sg_science_s4_patterns_in_the_periodic_table.py
Groups and periods, the change from metallic to non-metallic character across a period; Group 1 alkali metals (trends in
reactivity and melting point, reaction with water), Group 17 halogens (colour, state, reactivity and displacement), Group 18
noble gases; transition elements (high melting points, variable oxidation states, coloured compounds, catalysts); the
reactivity series from reactions with water, steam, acids and displacement; thermal stability of carbonates; extraction of
metals by reduction with carbon or by electrolysis; rusting and its prevention, including sacrificial protection.
UK and US periodic-table and reactivity makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "reactivity of Group 1 decreases down the group", "iodine displaces chlorine",
"copper reacts with dilute acid", "aluminium is extracted by heating with carbon", "painting iron is sacrificial protection".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Chemistry", 10
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

NOUS = lambda it: not any(w in it["q"] + it["c"][0] + it["e"] for w in ("ionisation", "electronegativ", "metalloid", "alkaline earth", "group 0", "Group 0"))
uk_rs = keep(src("gen_uk_science_y8_metals_and_non_metals", "g_rs"), NOUS)
us_fam = keep(src("gen_us_science_chem_periodic_table_and_trends", "g_fam"), NOUS)
us_loc = keep(src("gen_us_science_chem_periodic_table_and_trends", "g_loc"), NOUS)
uk_ext = src("gen_uk_science_y9_reactivity_and_extraction", "g_ext")
us_act = keep(src("gen_us_science_chem_types_of_chemical_reactions", "g_act"), NOUS)

G1 = ["lithium", "sodium", "potassium", "rubidium", "caesium"]
G17 = [("fluorine", "pale yellow gas"), ("chlorine", "greenish-yellow gas"), ("bromine", "reddish-brown liquid"), ("iodine", "black solid (purple vapour)")]


def g_g1():
    a, b = sorted(R.sample(G1, 2), key=G1.index)
    k = R.choice(["react", "mp", "react"])
    if k == "react":
        return tq("Which is more reactive with water: %s or %s?" % (a, b) if R.random() < 0.5 else "Which is more reactive with water: %s or %s?" % (b, a), b,
                  [a, "They react equally.", "Neither reacts with water."], "Reactivity of Group 1 metals increases down the group: the outer electron is further from the nucleus and lost more easily.")
    return tq("Which has the higher melting point: %s or %s?" % (b, a), a, [b, "They are the same.", "Group 1 metals do not melt."], "Melting points of Group 1 metals decrease down the group.")


def g_g17():
    (a, sa), (b, sb) = sorted(R.sample(G17, 2), key=G17.index)
    k = R.choice(["react", "disp", "state", "state"])
    if k == "react":
        return tq("Which is more reactive: %s or %s?" % (b, a), a, [b, "They are equally reactive.", "Halogens do not react."], "Reactivity of the halogens decreases down Group 17.")
    if k == "disp":
        if a == "fluorine":
            return None
        ion = {"chlorine": "chloride", "bromine": "bromide", "iodine": "iodide"}
        if R.random() < 0.5:
            return tq("Aqueous %s is added to aqueous potassium %s. What happens?" % (a, ion[b]), "%s is displaced: the solution turns %s." % (b.capitalize(), "orange-brown" if b == "bromine" else "brown"),
                      ["No reaction, because %s is less reactive." % a, "%s is displaced." % a.capitalize(), "A white precipitate forms."], "A more reactive halogen displaces a less reactive one from its halide.")
        return tq("Aqueous %s is added to aqueous potassium %s. What happens?" % (b, ion[a]), "No reaction, because %s is less reactive than %s." % (b, a),
                  ["%s is displaced." % a.capitalize(), "%s is displaced." % b.capitalize(), "Hydrogen is given off."], "A less reactive halogen cannot displace a more reactive one.")
    h, st = R.choice(G17)
    return tq("What is %s like at room temperature?" % h, st, [s for x, s in G17 if x != h], "Down Group 17 the colour darkens and the state changes from gas to liquid to solid.")


SERIES = ["potassium", "sodium", "calcium", "magnesium", "aluminium", "zinc", "iron", "lead", "copper", "silver"]
WATER = {"potassium": "reacts violently with cold water", "sodium": "reacts vigorously with cold water", "calcium": "reacts readily with cold water",
         "magnesium": "reacts very slowly with cold water but readily with steam", "zinc": "reacts with steam but not cold water", "iron": "reacts slowly with steam when red hot",
         "copper": "does not react with water or steam", "silver": "does not react with water or steam"}


def g_series():
    k = R.choice(["more", "disp", "water", "acid"])
    if k == "more":
        a, b = R.sample(SERIES, 2)
        ans = a if SERIES.index(a) < SERIES.index(b) else b
        return tq("Which metal is more reactive: %s or %s?" % (a, b), ans, [b if ans == a else a, "They are equally reactive.", "It cannot be predicted."],
                  "Reactivity series: K > Na > Ca > Mg > Al > Zn > Fe > Pb > (H) > Cu > Ag.")
    if k == "disp":
        a, b = R.sample(["magnesium", "zinc", "iron", "lead", "copper", "silver"], 2)
        salt = {"magnesium": "magnesium sulfate", "zinc": "zinc sulfate", "iron": "iron(II) sulfate", "lead": "lead(II) nitrate", "copper": "copper(II) sulfate", "silver": "silver nitrate"}[b]
        yes = SERIES.index(a) < SERIES.index(b)
        return tq("%s is added to aqueous %s. Does a displacement reaction happen?" % (a.capitalize(), salt), "Yes: %s is displaced." % b if yes else "No: %s is less reactive than %s." % (a, b),
                  ["No: %s is less reactive than %s." % (a, b) if yes else "Yes: %s is displaced." % b, "Yes: hydrogen is given off.", "Only if the solution is boiled."],
                  "A more reactive metal displaces a less reactive metal from a solution of its salt.")
    if k == "water":
        m = R.choice(list(WATER))
        return tq("How does %s react with water?" % m, "It " + WATER[m] + ".", R.sample(["It " + w + "." for x, w in WATER.items() if w != WATER[m]], 3), "Reactivity with water and steam follows the reactivity series.")
    m = R.choice(["magnesium", "zinc", "iron", "copper", "silver", "lead"])
    yes = SERIES.index(m) < SERIES.index("copper")
    return tq("Does %s react with dilute hydrochloric acid to give hydrogen?" % m, "Yes" if yes else "No", ["No" if yes else "Yes", "Only when the acid is concentrated and hot", "Only if it is a powder"],
              "Metals above hydrogen in the reactivity series displace hydrogen from dilute acids; copper and silver do not. (Lead reacts very slowly.)")


EXT = [("potassium", "electrolysis of the molten compound"), ("sodium", "electrolysis of the molten compound"), ("calcium", "electrolysis of the molten compound"),
       ("magnesium", "electrolysis of the molten compound"), ("aluminium", "electrolysis of the molten oxide"), ("zinc", "reduction of the oxide by carbon"),
       ("iron", "reduction of the oxide by carbon (carbon monoxide) in a blast furnace"), ("lead", "reduction of the oxide by carbon"), ("copper", "reduction of the oxide by carbon")]


def g_ext():
    m, how = R.choice(EXT)
    return tq("How is %s extracted from its ore?" % m, "by " + how, ["by " + x for x in sorted({h for _, h in EXT if h != how})][:3],
              "Metals above carbon in the reactivity series are extracted by electrolysis; metals below carbon by reduction with carbon.")


CARB = [("potassium carbonate", "does not decompose on heating with a Bunsen burner"), ("sodium carbonate", "does not decompose on heating with a Bunsen burner"),
        ("calcium carbonate", "decomposes on strong heating to calcium oxide and carbon dioxide"), ("zinc carbonate", "decomposes easily to zinc oxide and carbon dioxide"),
        ("copper(II) carbonate", "decomposes very easily to black copper(II) oxide and carbon dioxide")]
g_carb = rows(R, CARB, "What happens when %s is heated?")

TR = [("high melting points and densities", True), ("coloured compounds", True), ("variable oxidation states", True), ("use as catalysts", True),
      ("very low densities, so they float on water", False), ("reaction with cold water to form alkalis", False), ("only white compounds", False), ("a single fixed oxidation state", False)]


def g_tr():
    yes = [t for t, v in TR if v]
    no = [t for t, v in TR if not v]
    a = R.choice(yes)
    return tq("Which is a typical property of transition elements?", a, R.sample(no, 3), "Transition elements (such as iron, copper, nickel) are dense, high-melting metals with coloured compounds, variable oxidation states and catalytic activity.")


RUST = [("painting", "a barrier: stops oxygen and water reaching the iron"), ("oiling or greasing", "a barrier: stops oxygen and water reaching the iron"),
        ("galvanising (coating with zinc)", "a barrier, and sacrificial protection if scratched, because zinc is more reactive"),
        ("attaching blocks of magnesium to a ship's hull", "sacrificial protection: magnesium corrodes instead of iron"),
        ("tin-plating food cans", "a barrier only: if scratched, the iron rusts faster"), ("making stainless steel", "alloying with chromium and nickel forms a protective layer")]
g_rust = rows(R, RUST, "How does %s protect iron from rusting?")

POOL1 = pool(R, [
    ("What do elements in the same group have in common?", "the same number of outer (valence) electrons, so similar chemical properties", ["the same number of shells", "the same mass", "the same state at room temperature"], "Group number = outer electrons (for Groups 1, 2, 13–17)."),
    ("What changes across a period from left to right?", "The elements change from metals to non-metals.", ["The number of shells increases.", "The elements become more metallic.", "The outer electrons decrease."], "Period 3: Na, Mg, Al are metals; Si; P, S, Cl, Ar are non-metals."),
    ("What is formed when sodium reacts with water?", "sodium hydroxide and hydrogen", ["sodium oxide and hydrogen", "sodium hydroxide and oxygen", "sodium chloride and water"], "2Na + 2H₂O → 2NaOH + H₂."),
    ("Why are Group 1 metals stored under oil?", "to stop them reacting with oxygen and water vapour in the air", ["to keep them cold", "because they are liquids", "to stop them dissolving"], "They are very reactive."),
    ("Why are the noble gases unreactive?", "Their atoms have full outer shells (stable electronic configurations).", ["They are too heavy.", "They have no electrons.", "They are liquids."], "Group 18."),
    ("Why is argon used in light bulbs?", "It is unreactive, so the hot filament does not burn.", ["It glows brightly.", "It is a good conductor.", "It is cheap and coloured."], "An inert atmosphere."),
    ("Why is helium used in weather balloons?", "It is much less dense than air and unreactive (not flammable).", ["It is heavier than air.", "It burns easily.", "It is coloured."], "Hydrogen is less dense but flammable."),
    ("What two substances must be present for iron to rust?", "oxygen and water", ["oxygen and carbon dioxide", "water and salt only", "nitrogen and water"], "Salt speeds up rusting."),
    ("Which metal is most likely to be found uncombined in the Earth?", "gold", ["sodium", "aluminium", "magnesium"], "Very unreactive metals occur native."),
    ("What is the role of coke in the blast furnace?", "It burns to give heat and forms carbon monoxide, which reduces iron(III) oxide.", ["It removes sand.", "It is the iron ore.", "It makes slag."], "Limestone removes impurities as slag."),
])
POOL5 = pool(R, [
    ("Why is limestone added to the blast furnace?", "It decomposes to calcium oxide, which reacts with sandy impurities (silicon dioxide) to form slag.", ["It reduces the iron oxide.", "It is a fuel.", "It makes the iron harder."], "CaO + SiO₂ → CaSiO₃."),
    ("Why is aluminium not extracted by heating its oxide with carbon?", "Aluminium is more reactive than carbon, so carbon cannot reduce it.", ["Aluminium oxide has no oxygen.", "Carbon is too expensive.", "Aluminium melts too easily."], "Electrolysis is used instead."),
    ("Why does a scratched tin-plated can rust quickly?", "Iron is more reactive than tin, so the iron corrodes in preference.", ["Tin reacts with water.", "Tin speeds up all reactions.", "The can was made of copper."], "Tin is only a barrier."),
    ("Why does galvanised iron not rust even when scratched?", "Zinc is more reactive than iron, so zinc corrodes first (sacrificial protection).", ["Zinc is less reactive.", "Zinc stops all water.", "Zinc is a non-metal."], "The zinc gives up electrons."),
    ("Astatine is below iodine in Group 17. Predict its state and reactivity.", "a black solid, less reactive than iodine", ["a gas, more reactive than chlorine", "a liquid, more reactive than bromine", "a colourless gas, unreactive"], "Trends continue down the group."),
    ("Francium is below caesium in Group 1. Predict how it reacts with water.", "even more violently than caesium", ["more slowly than lithium", "it does not react", "it forms an acid"], "Reactivity increases down Group 1."),
    ("Why are transition metals and their compounds used as catalysts?", "They can change oxidation state and provide surfaces for reactions.", ["They are coloured.", "They are unreactive.", "They are very light."], "Iron in the Haber process."),
    ("Why does a more reactive metal form a more stable carbonate?", "Its carbonate needs more energy to decompose.", ["Its carbonate has less carbon.", "It is a liquid.", "It does not form a carbonate."], "Sodium carbonate does not decompose in a Bunsen flame."),
    ("What is an alloy and why is steel used instead of pure iron?", "a mixture of a metal with other elements; steel is harder and stronger", ["a compound of iron and carbon; it is softer", "a pure metal; it conducts better", "an ionic compound; it melts lower"], "Different-sized atoms stop layers sliding."),
    ("Chlorine water is added to potassium iodide solution. The solution turns brown. Write the ionic equation.", "Cl₂ + 2I⁻ → 2Cl⁻ + I₂", ["I₂ + 2Cl⁻ → 2I⁻ + Cl₂", "Cl⁻ + I⁻ → ClI", "2K⁺ + Cl₂ → 2KCl"], "Chlorine is reduced; iodide is oxidised."),
])


def main():
    sets = U.sets([
        ("The Periodic Table: groups, periods and Group 1", [POOL1, (g_g1, 6), (us_loc, 4), (us_fam, 3)]),
        ("Group 17, Group 18 and transition elements", [(g_g17, 10), (g_tr, 4), POOL1, (POOL5, 2)]),
        ("The reactivity series", [(g_series, 12), (uk_rs, 4), (us_act, 4)]),
        ("Extraction and rusting", [(g_ext, 6), (g_rust, 6), (g_carb, 4), (uk_ext, 2), (POOL5, 2)]),
        ("Exam-style questions", [(POOL5, 8), (g_series, 5), (g_g17, 4), (g_g1, 3)]),
    ])
    make_ol(LV, SUBJ, "patterns-in-the-periodic-table", SORT, "Patterns in the Periodic Table",
            "Describe the Periodic Table as an arrangement of elements in order of proton number and relate group number to outer electrons; describe the change from "
            "metallic to non-metallic character across a period; describe the trends in Group 1 (reactivity, melting point, reaction with water), Group 17 (colour, state, "
            "reactivity, displacement) and Group 18; describe the general properties of transition elements; place metals in a reactivity series using their reactions "
            "with water, steam and dilute acids and displacement reactions; describe the thermal decomposition of carbonates; relate the extraction of metals to their "
            "reactivity; describe rusting and its prevention, including sacrificial protection (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Patterns in the Periodic Table", "Periodic Table and metals",
            "Free Secondary 4 O-Level Chemistry worksheets on patterns in the Periodic Table: Group 1, Group 17, noble gases, transition elements, the reactivity series, "
            "extraction of metals and rusting. 100 questions with answers.",
            "Group 1: more reactive down. Group 17: less reactive down.", "K Na Ca Mg Al Zn Fe Pb (H) Cu Ag",
            "<p><b>Elements in the same group have similar properties and show trends.</b></p><ul>"
            "<li>Group 1: soft, reactive metals; reactivity increases and melting point decreases down the group; react with water to give an alkali and hydrogen.</li>"
            "<li>Group 17: colour darkens and state goes gas → liquid → solid down the group; reactivity decreases; a more reactive halogen displaces a less reactive one.</li>"
            "<li>Reactivity series: K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Ag. Metals above carbon are extracted by electrolysis; below carbon, by reduction with carbon.</li>"
            "<li>Rusting needs oxygen and water. Barriers (paint, oil) and sacrificial protection (zinc, magnesium) prevent it.</li></ul>",
            [("Does iron displace copper from copper(II) sulfate?", ["Fe is above Cu"], "yes: pink copper forms and the blue colour fades"),
             ("Does bromine displace chlorine from KCl?", ["Br₂ is less reactive than Cl₂"], "no reaction")],
            ["Saying Group 1 reactivity decreases down the group.", "Thinking iodine can displace chlorine.",
             "Saying aluminium can be extracted by heating with carbon.", "Calling painting 'sacrificial protection'."],
            [("Why does reactivity increase down Group 1?", "The atoms get larger, so the single outer electron is further from the nucleus and is lost more easily."),
             ("How are metals extracted?", "Metals more reactive than carbon (K to Al) are extracted by electrolysis of their molten compounds; less reactive metals (Zn, Fe, Pb, Cu) by heating their oxides with carbon."),
             ("What is sacrificial protection?", "Attaching a more reactive metal such as zinc or magnesium to iron, so the more reactive metal corrodes instead of the iron.")],
            sets)


if __name__ == "__main__":
    main()
