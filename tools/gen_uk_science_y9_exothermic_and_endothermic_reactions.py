# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Chemistry): Exothermic and Endothermic Reactions
  python tools/gen_uk_science_y9_exothermic_and_endothermic_reactions.py
Exothermic and endothermic reactions and changes (qualitative), measuring temperature changes, energy level diagrams,
bond breaking and bond making, uses (hand warmers, cold packs, self-heating cans), and the factors that change the rate
of a reaction (temperature, concentration, surface area, catalysts). Reuses the classification, energy-diagram,
data and rate-factor questions of the US units in British English.
Wrong answers come from real mistakes: "endothermic reactions get hotter", "breaking bonds releases energy",
"a catalyst is used up", "powder reacts slower than lumps".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61904)
R = U.R
P = People(R)
uk_sci.USED.clear()
EC = adopt_us("gen_us_science_chem_energy_in_chemical_reactions", U)
E7 = adopt_us("gen_us_science_g7_energy_in_chemical_reactions", U)
RR = adopt_us("gen_us_science_chem_reaction_rates", U)
us_exo, _diag = ukm(EC.g_exo), ukm(EC.g_diag)


def us_diag():
    it = _diag()
    return None if it is None or "ΔH" in it["q"] or "reverse" in it["q"] else it
us_kind, us_data, us_design = ukm(E7.g_kind), ukm(E7.g_data), ukm(E7.g_design)
us_factor, us_cat = ukm(RR.g_factor), ukm(RR.g_cat)

PAIRS = [("hydrochloric acid and sodium hydroxide", True), ("magnesium ribbon and dilute acid", True), ("citric acid and sodium hydrogencarbonate", False),
         ("ammonium nitrate dissolving in water", False), ("calcium chloride dissolving in water", True), ("zinc powder and copper sulfate solution", True),
         ("potassium chloride dissolving in water", False), ("iron filings, salt water and air (a hand warmer)", True)]


def g_temp():
    who = P.next()[0]
    what, exo = R.choice(PAIRS)
    t0 = R.choice([18, 19, 20, 21, 22])
    d = R.choice([4, 6, 8, 9, 12, 15])
    t1 = t0 + d if exo else t0 - d
    k = R.choice(["kind", "change"])
    if not once(("te", what, k)) or not once(("te2", what, t0, d)):
        return None
    tab = table(["", "Temperature (°C)"], [["start", str(t0)], ["end", str(t1)]])
    intro = tab + "%s mixed %s. " % (who, what)
    if k == "kind":
        a = "exothermic, because the temperature rose" if exo else "endothermic, because the temperature fell"
        b = "endothermic, because the temperature rose" if exo else "exothermic, because the temperature fell"
        return item(intro + "Is this change exothermic or endothermic?", a, [b, "neither, because no gas was made", "both at once"], "Exothermic warms the surroundings; endothermic cools them.")
    g = "%d °C" % d
    return item(intro + "By how much did the temperature change?", g, uniq(g, ["%d °C" % t1, "%d °C" % t0, "%d °C" % (t0 + t1), "%d °C" % (d + 2)]), "%d − %d = %d." % (max(t0, t1), min(t0, t1), d))


B1 = bank([
    ("What is an exothermic reaction?", "a reaction that transfers energy to the surroundings, so the temperature rises", ["a reaction that takes in energy", "a reaction with no energy change", "a reaction that needs light"], "Burning, neutralisation, respiration."),
    ("What is an endothermic reaction?", "a reaction that takes in energy from the surroundings, so the temperature falls", ["a reaction that gives out heat", "a reaction that explodes", "a reaction that makes light"], "Thermal decomposition, photosynthesis."),
    ("Does breaking chemical bonds take in or give out energy?", "It takes in energy.", ["It gives out energy.", "It has no energy change.", "It makes light only."], "Energy is needed to pull atoms apart."),
    ("Does making chemical bonds take in or give out energy?", "It gives out energy.", ["It takes in energy.", "It has no energy change.", "It needs a catalyst."], "Energy is released when bonds form."),
    ("Why is a reaction exothermic overall?", "More energy is released making new bonds than is needed to break the old ones.", ["Less energy is released than taken in.", "No bonds are broken.", "The products are heavier."], "Energy balance."),
])
B5 = bank([
    ("Why does a reaction go faster when the temperature is higher?", "Particles move faster and collide more often and with more energy.", ["Particles get bigger.", "The reaction needs less product.", "Heat is a reactant."], "Collision theory."),
    ("Why does powdered marble react faster with acid than marble chips?", "The powder has a larger surface area, so there are more collisions.", ["Powder is heavier.", "Chips are more reactive.", "Powder is a catalyst."], "Surface area."),
    ("What happens to a catalyst at the end of a reaction?", "It is unchanged and can be used again.", ["It is used up.", "It becomes a product.", "It turns into a gas."], "Speeds up without being used up."),
    ("Why does a more concentrated acid react faster?", "There are more acid particles in the same volume, so collisions are more frequent.", ["The acid is hotter.", "The particles are larger.", "There is less water to block it."], "Concentration."),
    ("Which change is a physical endothermic change?", "ice melting", ["wood burning", "water freezing", "a hand warmer heating up"], "Melting takes in energy."),
])


def body():
    think = ("<p><b>Every reaction transfers energy to or from the surroundings.</b></p>"
             "<ul><li>Exothermic: gives out energy, the temperature rises (burning, neutralisation, hand warmers).</li>"
             "<li>Endothermic: takes in energy, the temperature falls (thermal decomposition, cold packs).</li>"
             "<li>Breaking bonds takes in energy; making bonds gives it out. Higher temperature, concentration and surface area, and catalysts, speed reactions up.</li></ul>")
    ex = [("Start 20 °C, end 12 °C. Type?", ["Temperature fell"], "endothermic"),
          ("Start 19 °C, end 31 °C. Change?", ["31 − 19"], "12 °C")]
    mist = ["Thinking endothermic reactions get hotter.", "Thinking breaking bonds releases energy.", "Thinking a catalyst is used up."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Exothermic or endothermic?", B1[:2] + [(us_exo, 10), (us_kind, 8)]),
        ("Measuring temperature changes", [(g_temp, 13), (us_data, 7)]),
        ("Energy level diagrams", B1[2:] + [(us_diag, 8), (us_exo, 7), (us_data, 2)]),
        ("Using energy changes", [(us_design, 6), (us_data, 6), (g_temp, 2), (us_kind, 4), (us_exo, 2)]),
        ("Rates of reaction", B5 + [(us_factor, 12), (us_cat, 3)]),
    ])
    make_ks3(9, "exothermic-and-endothermic-reactions", 4, "Chemistry", "Energetics",
             "Energy changes on changes of state (qualitative); exothermic and endothermic chemical reactions (qualitative); what catalysts do.",
             "Exothermic and Endothermic Reactions",
             "Year 9 Science: Exothermic and Endothermic Reactions Worksheets (Energy Changes)",
             "Exothermic and Endothermic",
             "Free Year 9 science worksheets on exothermic and endothermic reactions: temperature changes, energy level diagrams, bond breaking and making, hand warmers and cold packs, and rates of reaction. 100 questions with answers.",
             "Exothermic warms; endothermic cools.",
             "Breaking bonds takes in energy; making bonds gives it out.",
             body(),
             [("How can you tell if a reaction is exothermic?", "Measure the temperature before and after. If it rises, energy was transferred to the surroundings: the reaction is exothermic."),
              ("What are some uses of endothermic reactions?", "Instant cold packs for sports injuries use an endothermic change, such as ammonium nitrate dissolving in water."),
              ("What does an energy level diagram show?", "The energy of the reactants and products. If the products are lower, the reaction is exothermic; if higher, it is endothermic.")],
             sets)


if __name__ == "__main__":
    main()
