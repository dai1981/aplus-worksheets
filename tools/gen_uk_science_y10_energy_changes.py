# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Chemistry): Energy Changes
  python tools/gen_uk_science_y10_energy_changes.py
Exothermic and endothermic reactions, measuring temperature changes, uses (hand warmers, cold packs, self-heating
cans), reaction profiles and activation energy, and (higher tier) calculating the overall energy change from bond
energies. Reuses the US Chemistry and Grade 7 energy questions in British English and the temperature question of the
Year 9 unit (new seed).
Wrong answers come from real mistakes: "breaking bonds releases energy", "endothermic reactions get hot",
"activation energy is the overall energy change", "the products are higher in an exothermic profile".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62009)
EC = "chem_energy_in_chemical_reactions"
E7 = "g7_energy_in_chemical_reactions"
us_bond, us_diag, us_exo = us(EC, "g_bond"), us(EC, "g_diag"), us(EC, "g_exo")
us_kind, us_data, us_design = us(E7, "g_kind"), us(E7, "g_data"), us(E7, "g_design")
y9_temp = us.uk("gen_uk_science_y9_exothermic_and_endothermic_reactions", "g_temp")

PROF = [("The products are lower in energy than the reactants.", "exothermic"), ("The products are higher in energy than the reactants.", "endothermic"),
        ("Energy is released to the surroundings.", "exothermic"), ("Energy is taken in from the surroundings.", "endothermic"),
        ("More energy is released making new bonds than is used breaking old bonds.", "exothermic"), ("More energy is used breaking bonds than is released making new bonds.", "endothermic"),
        ("The temperature of the surroundings falls.", "endothermic"), ("The temperature of the surroundings rises.", "exothermic")]


def g_prof():
    s, a = R.choice(PROF)
    if not once(("pf", s)):
        return None
    return item("%s Is the reaction exothermic or endothermic?" % s, a, [x for x in ["exothermic", "endothermic", "neither", "both"] if x != a], "Exothermic: energy out. Endothermic: energy in.")


B1 = bank([
    ("What is activation energy?", "the minimum energy particles need to react when they collide", ["the overall energy change", "the energy of the products", "the energy released by bonds forming"], "Shown as the hump on a reaction profile."),
    ("Does breaking bonds take in or release energy?", "It takes in energy (endothermic).", ["It releases energy.", "No energy change.", "It makes light."], "Making bonds releases energy."),
    ("Give an everyday example of an exothermic reaction.", "combustion of fuels", ["photosynthesis", "thermal decomposition of calcium carbonate", "dissolving ammonium nitrate"], "Also neutralisation and respiration."),
    ("Give an example of an endothermic reaction.", "thermal decomposition", ["combustion", "neutralisation", "respiration"], "Takes in heat."),
])
B5 = bank([
    ("Why is a polystyrene cup with a lid used to measure temperature changes?", "It is a good insulator, so less energy is lost to the surroundings.", ["It reacts with the chemicals.", "It speeds up the reaction.", "It is cheaper than glass only."], "Accuracy."),
    ("How does a catalyst affect a reaction profile?", "It lowers the activation energy.", ["It raises the products' energy.", "It changes the overall energy change.", "It removes the hump completely."], "Another pathway."),
    ("Why do sports injury cold packs feel cold?", "An endothermic process takes in energy from the surroundings.", ["They release heat.", "They contain ice only.", "They are exothermic."], "Dissolving ammonium nitrate."),
    ("Why are hand warmers based on oxidation of iron useful?", "The reaction is exothermic and releases heat slowly.", ["It is endothermic.", "It makes ice.", "It needs electricity."], "Iron + oxygen."),
])

if __name__ == "__main__":
  build(U, 10, "energy-changes", 9, "Chemistry", "Energy changes",
      "Exothermic and endothermic reactions; the energy transferred and temperature changes; everyday uses; reaction profiles and activation energy; the energy change of reactions, including (higher tier) calculating energy changes from bond energies.",
      "Energy Changes", "Energy Changes",
      "Free Year 10 GCSE Combined Science worksheets on energy changes: exothermic and endothermic reactions, temperature changes, reaction profiles, activation energy and bond energy calculations. 100 questions with answers.",
      "Breaking bonds takes in energy; making bonds releases it.",
      "Exothermic profiles go down; endothermic profiles go up.",
      "<p><b>Every reaction transfers energy.</b></p><ul><li>Exothermic: energy is released and the surroundings warm up. Endothermic: energy is taken in and the surroundings cool.</li>"
      "<li>A reaction profile shows the energy of reactants and products; the hump is the activation energy.</li>"
      "<li>Higher tier: energy change = energy to break bonds − energy released making bonds. Negative means exothermic.</li></ul>",
      [("Break 1,000 kJ, make 1,200 kJ. Type?", ["1,000 − 1,200 = −200"], "exothermic"), ("Temperature 20 °C → 12 °C?", ["It fell"], "endothermic")],
      ["Thinking breaking bonds releases energy.", "Thinking endothermic reactions get hot.", "Mixing up activation energy and the overall energy change."],
      [("How can you tell if a reaction is exothermic or endothermic?", "Measure the temperature. If it rises, energy was released (exothermic). If it falls, energy was taken in (endothermic)."),
       ("What does a reaction profile show?", "The energy of the reactants and products and the activation energy. In an exothermic profile the products are lower than the reactants."),
       ("How do you use bond energies?", "Add up the energy needed to break the bonds in the reactants, subtract the energy released making the bonds in the products. A negative answer means exothermic.")],
      [("Exothermic and endothermic", B1 + [(us_exo, 10), (g_prof, 6)]),
       ("Temperature changes", [(y9_temp, 10), (us_data, 10)]),
       ("Uses of energy changes", [(us_kind, 10), (us_design, 6), (g_prof, 1), (us_exo, 3)]),
       ("Reaction profiles", [(us_diag, 16), (us_exo, 4)]),
       ("Bond energies", B5 + [(us_bond, 16)])])
