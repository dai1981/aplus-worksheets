# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U07: patterns in synthesis, decomposition and displacement reactions (and
combustion), the reactivity series, and the factors that affect reaction rates (temperature, concentration, surface area,
catalysts) explained by collision theory.
  python tools/gen_au_science_y10_reaction_types_and_rates.py
Reuses the US Chemistry types of reactions and reaction rates makers, the SG Secondary 4 rate of reactions makers and the UK
Year 11 rates makers with Australian names, plus own questions on Australian contexts.
Wrong answers come from real mistakes: thinking a catalyst is used up, thinking larger lumps react faster than powder, and
confusing synthesis with decomposition.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

TY = "gen_us_science_chem_types_of_chemical_reactions"
RR = "gen_us_science_chem_reaction_rates"
SR = "gen_sg_science_s4_rate_of_reactions"
K11 = "gen_uk_science_y11_rates_and_equilibrium"
REP = [(r"\bsingle[- ]replacement\b", "displacement"), (r"\bSingle[- ]replacement\b", "Displacement"), (r"\bsingle[- ]displacement\b", "displacement"),
       (r"\bSingle[- ]displacement\b", "Displacement")]
NO = ["double[- ]replacement", "double[- ]displacement", "Double[- ]replacement", "activation energy", "equilibrium", "reversible", "enthalpy", "kJ"]
t_act = limit(src(TY, "g_act", rep=REP, drop=NO), 6)
t_evid = src(TY, "g_evid", rep=REP, drop=NO)
t_prod = src(TY, "g_prod", rep=REP, drop=NO)
t_type = limit(src(TY, "g_type", rep=REP, drop=NO), 8)
t_b1 = src.B(TY, "B1", rep=REP, drop=NO)
t_b5 = src.B(TY, "B5", rep=REP, drop=NO)
r_data = limit(src(RR, "g_data", rep=REP, drop=NO), 5)
r_factor = limit(src(RR, "g_factor", rep=REP, drop=NO), 6)
r_rate = src(RR, "g_rate", rep=REP, drop=NO)
r_b1 = src.B(RR, "B1", rep=REP, drop=NO)
r_b5 = src.B(RR, "B5", rep=REP, drop=NO)
s_curve = limit(src(SR, "g_curve", rep=REP, drop=NO), 5)
s_chg = limit(src(SR, "g_chg", rep=REP, drop=NO), 4)
k_coll = src(K11, "g_coll", rep=REP, drop=NO)

POOL1 = pool(R, [
    ("What is a synthesis reaction?", "two or more substances combine to make one product (A + B → AB)", ["one substance breaks into two or more (AB → A + B)", "a more reactive element swaps places with a less reactive one", "a fuel reacts with oxygen"], "Example: iron + sulfur → iron sulfide."),
    ("What is a decomposition reaction?", "one substance breaks down into two or more simpler substances", ["two substances join to make one", "an element swaps places in a compound", "an acid reacts with a base"], "Example: calcium carbonate → calcium oxide + carbon dioxide."),
    ("What is a displacement reaction?", "a more reactive element replaces a less reactive one in a compound", ["two elements join together", "a compound breaks down by heating", "a fuel burns in oxygen"], "Example: zinc + copper sulfate → zinc sulfate + copper."),
    ("Which type of reaction is 2H₂O → 2H₂ + O₂?", "decomposition", ["synthesis", "displacement", "combustion"], "One reactant breaks into two products."),
    ("Which type of reaction is 2Mg + O₂ → 2MgO?", "synthesis (and combustion)", ["decomposition", "displacement", "neutralisation"], "Two reactants make one product."),
    ("Will copper displace zinc from zinc sulfate solution?", "No, copper is less reactive than zinc.", ["Yes, copper is more reactive.", "Yes, all metals displace each other.", "Only if heated to melting."], "Only a more reactive metal displaces a less reactive one."),
    ("According to collision theory, what must happen for particles to react?", "They must collide with enough energy and in the right orientation.", ["They must stay apart.", "They must be the same colour.", "They must be solids."], "More successful collisions mean a faster rate."),
    ("Why does increasing the temperature speed up a reaction?", "Particles move faster, so they collide more often and with more energy.", ["Particles get bigger.", "It adds more reactant.", "It removes the catalyst."], "Food goes off faster on a hot day."),
    ("Why does powdered marble react faster with acid than a single marble chip of the same mass?", "The powder has a larger surface area for collisions.", ["The powder has more mass.", "The chip is more reactive.", "Powder is a catalyst."], "Grain dust explosions in silos happen for this reason."),
    ("What does a catalyst do?", "speeds up a reaction without being used up", ["slows a reaction and is used up", "becomes a product", "increases the temperature"], "Catalytic converters in cars use platinum."),
    ("Why does increasing the concentration of an acid speed up its reaction with magnesium?", "There are more acid particles in the same volume, so more collisions.", ["The acid gets hotter.", "Magnesium becomes a catalyst.", "Concentration has no effect."], "Rate depends on the frequency of successful collisions."),
    ("Why are enzymes important in living things?", "They are biological catalysts that speed up reactions in cells.", ["They are fuels.", "They slow all reactions.", "They are used up in reactions."], "Digestive enzymes break down food."),
])
POOL5 = pool(R, [
    ("Mia times how long a 1 cm magnesium ribbon takes to dissolve in acid at 20 °C, 30 °C and 40 °C. What is the dependent variable?", "the time for the magnesium to dissolve", ["the temperature", "the length of ribbon", "the type of acid"], "She measures the time."),
    ("Jack collects the gas from marble chips and acid every 30 s. The volume rises quickly then levels off. Why does it level off?", "One of the reactants has been used up.", ["The gas stops being a gas.", "The catalyst stops working.", "The temperature falls to 0 °C."], "The reaction has finished."),
    ("Ruby adds manganese dioxide to hydrogen peroxide. Bubbles of oxygen form quickly. After filtering, the manganese dioxide has the same mass. What is it?", "a catalyst", ["a reactant", "a product", "an inhibitor"], "Catalysts are not used up."),
    ("Kai puts zinc, copper and magnesium strips into copper sulfate solution. Which metals will become coated with copper?", "zinc and magnesium", ["copper only", "all three", "none"], "Only metals more reactive than copper displace it."),
    ("Ella's graph shows two reactions. Line A is steeper at the start than line B. What does this mean?", "Reaction A has a faster initial rate.", ["Reaction B is faster.", "Reaction A makes less product.", "They have the same rate."], "A steeper slope means a faster rate."),
    ("Noah heats green copper carbonate and it turns black, giving off a gas that turns limewater milky. Which type of reaction is this?", "decomposition", ["synthesis", "displacement", "neutralisation"], "Copper carbonate → copper oxide + carbon dioxide."),
    ("Zara wants a fair test of how surface area affects rate. What should she keep the same?", "the mass of marble, the volume and concentration of acid, and the temperature", ["the size of the marble pieces", "nothing", "the time she stops"], "Only the surface area should change."),
    ("Why do bakers in hot Australian summers keep dough in the fridge to slow its rising?", "Lower temperature slows the reactions of yeast.", ["Cold speeds up yeast.", "The fridge adds a catalyst.", "Dough stops being dough."], "Temperature affects reaction rate."),
])


def main():
    sets = U.sets([
        ("Synthesis, decomposition and displacement", [(POOL1, 6), (t_type, 7), (t_b1, 4), (t_prod, 3)]),
        ("Patterns and the reactivity series", [(t_act, 6), (t_prod, 4), (t_evid, 4), (POOL1, 3), (t_type, 1), (POOL5, 2)]),
        ("Collision theory", [(k_coll, 5), (r_factor, 6), (POOL1, 3), (r_b1, 4), (s_chg, 2)]),
        ("Factors affecting rate", [(s_chg, 2), (r_rate, 5), (s_curve, 5), (r_data, 4), (POOL1, 2), (r_factor, 2)]),
        ("Investigations", [(POOL5, 6), (t_b5, 4), (r_b5, 4), (r_data, 1), (s_curve, 2), (t_act, 2), (t_evid, 1)]),
    ])
    make_au(YEAR, "reaction-types-and-rates", SORT, "AC9S10U07", "Chemical sciences",
            "Identify patterns in synthesis, decomposition and displacement reactions and investigate the factors that affect reaction "
            "rates (summary of the Australian Curriculum v9.0 Science content description).",
            "Reaction Types and Rates", "Reaction types and rates",
            "Free Year 10 science worksheets on chemical reactions: synthesis, decomposition and displacement reactions, the reactivity "
            "series, collision theory, and how temperature, concentration, surface area and catalysts affect reaction rate. 100 questions with answers.",
            "More collisions, faster reaction.", "Temperature, concentration, surface area and catalysts change how often particles collide successfully.",
            "<p><b>Many reactions follow simple patterns.</b></p><ul>"
            "<li>Synthesis: A + B → AB. Decomposition: AB → A + B. Displacement: A + BC → AC + B, when A is more reactive than B.</li>"
            "<li>Collision theory: particles react when they collide with enough energy in the right direction.</li>"
            "<li>Rate increases with higher temperature, higher concentration, larger surface area (smaller pieces) and a catalyst.</li></ul>",
            [("Zn + CuSO₄ → ZnSO₄ + Cu. Type?", ["zinc replaces copper"], "displacement"),
             ("Why does powder react faster than a lump?", ["more surface area", "more collisions"], "larger surface area")],
            ["Thinking a catalyst is used up in the reaction.", "Thinking a large lump reacts faster than powder.",
             "Mixing up synthesis (joining) and decomposition (breaking down)."],
            [("How do I tell the reaction types apart?", "Synthesis has one product; decomposition has one reactant; displacement has an element swapping places with another element in a compound."),
             ("What is collision theory?", "It says reactions happen when particles collide with enough energy and in the right orientation. Anything that increases successful collisions speeds up the reaction."),
             ("How does a catalyst work?", "A catalyst gives the reaction an easier pathway that needs less energy, so more collisions succeed. It is not used up.")],
            sets)


if __name__ == "__main__":
    main()
