# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U03: the carbon cycle - carbon stores (atmosphere, oceans, living things,
fossil fuels, rocks), the processes that move carbon (photosynthesis, respiration, combustion, decomposition, ocean exchange),
and human impacts on the cycle.
  python tools/gen_au_science_y9_the_carbon_cycle.py
Reuses the US Biology carbon cycle makers, the US Earth and Space Science carbon cycle makers and the US Grade 7 cycling of
matter makers with Australian names, plus own questions on bushfires, coal and blue carbon in mangroves and seagrass.
Wrong answers come from real mistakes: thinking plants get their carbon from the soil, thinking only animals respire, and
thinking burning fossil fuels moves "new" carbon that was never in the cycle.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

BC = "gen_us_science_bio_carbon_cycle"
EC = "gen_us_science_ess_carbon_cycle_and_earth_systems"
G7 = "gen_us_science_g7_cycling_of_matter_and_energy_flow"
BAD = [r"(Where|Which way) does [^?]*(animals|fires|plants|forests|bacteria|organisms|people)\b", r"Does (bacteria|people)"]
b_air = limit(src(BC, "g_air", drop=BAD), 6)
b_ml = limit(src(BC, "g_ml"), 6)
b_path = src(BC, "g_path", drop=BAD)
b_proc = src(BC, "g_proc", drop=BAD)
b_res = src(BC, "g_res", drop=BAD)
b_b1 = src.B(BC, "B1")
b_b5 = src.B(BC, "B5")
e_budget = limit(src(EC, "g_budget"), 11)
e_flux = limit(src(EC, "g_flux", drop=BAD), 6)
e_keel = limit(src(EC, "g_keel"), 10)
e_res = src(EC, "g_res", drop=BAD)
e_b1 = src.B(EC, "B1")
e_b5 = src.B(EC, "B5")
c_cycle = src(G7, "g_cycle")

POOL1 = pool(R, [
    ("Which process removes carbon dioxide from the air?", "photosynthesis", ["respiration", "combustion", "decomposition"], "Plants use CO₂ to make glucose."),
    ("Which processes add carbon dioxide to the air?", "respiration, combustion and decomposition", ["photosynthesis only", "only volcanoes", "evaporation and condensation"], "All three release CO₂."),
    ("Where does a gum tree get most of the carbon in its wood?", "carbon dioxide from the air", ["the soil", "water", "fertiliser"], "Photosynthesis builds glucose from CO₂ and water."),
    ("Do plants respire?", "Yes, all living cells respire, day and night.", ["No, only animals respire.", "Only at night.", "Only when they are dying."], "Plants photosynthesise and respire."),
    ("What are fossil fuels made from?", "the remains of living things buried for millions of years", ["volcanic rock", "sea water", "sunlight"], "Coal formed from ancient plants."),
    ("Why does burning coal increase the carbon dioxide in the air?", "It releases carbon that was stored underground for millions of years.", ["Coal has no carbon.", "Coal makes oxygen.", "It creates new carbon atoms."], "Carbon atoms are conserved but move stores."),
    ("During a bushfire, where does the carbon in the burnt trees go?", "mostly into the air as carbon dioxide", ["it is destroyed", "into the rocks immediately", "into the Sun"], "Regrowth later takes CO₂ back in."),
    ("Mangroves and seagrass along Australian coasts store a lot of carbon. What is this called?", "blue carbon", ["fossil carbon", "green energy", "acid rain"], "They trap carbon in mud for a long time."),
    ("Which is the largest store of carbon near Earth's surface?", "rocks such as limestone, then the deep ocean", ["the air", "living animals", "clouds"], "The atmosphere holds only a small part."),
    ("What role do decomposers play in the carbon cycle?", "They break down dead things and release carbon dioxide by respiration.", ["They photosynthesise.", "They store carbon forever.", "They make fossil fuels directly."], "Fungi and bacteria are decomposers."),
    ("How does the ocean take in carbon dioxide?", "CO₂ dissolves in sea water and is used by marine algae.", ["The ocean cannot take in CO₂.", "Fish breathe it in.", "Waves blow it away."], "Too much makes the ocean more acidic."),
    ("Which word equation shows photosynthesis?", "carbon dioxide + water → glucose + oxygen", ["glucose + oxygen → carbon dioxide + water", "carbon + oxygen → water", "oxygen → carbon dioxide"], "Respiration is the reverse."),
])
POOL5 = pool(R, [
    ("Mia seals a water plant in a test tube with indicator that turns yellow when CO₂ rises and purple when it falls. In bright light it turns purple. Why?", "Photosynthesis removes more CO₂ than respiration adds.", ["The plant stopped respiring.", "Light adds CO₂.", "The indicator is broken."], "In the dark it would turn yellow."),
    ("Jack keeps the same set-up in the dark. What colour change would he expect?", "towards yellow, because only respiration happens", ["towards purple", "no change", "it turns clear"], "Without light, there is no photosynthesis."),
    ("Ruby reads that air CO₂ at Cape Grim, Tasmania rose from about 330 ppm in 1976 to over 410 ppm. What is the main cause?", "burning fossil fuels and clearing land", ["more photosynthesis", "fewer volcanoes", "cooler oceans"], "Cape Grim measures clean air from the Southern Ocean."),
    ("Kai compares the mass of a seedling and its soil after a month. The seedling gained 20 g but the soil lost only 0.1 g. What does this show?", "Most of the plant's new mass came from air and water.", ["The plant ate the soil.", "Mass was created.", "The scale is wrong."], "This is like van Helmont's famous experiment."),
    ("Ella plans to plant trees to take carbon from the air. Why are fast-growing native trees a good choice?", "They photosynthesise quickly and store carbon in their wood.", ["They release more CO₂ than they take in.", "They stop all respiration.", "They grow without light."], "Growing forests are carbon sinks."),
    ("A graph shows CO₂ at a station going up and down every year, as well as rising overall. Why does it go up and down?", "Plants photosynthesise more in the growing season.", ["The station moves.", "The Sun turns off in winter.", "People stop breathing in summer."], "Seasonal plant growth causes the yearly wave."),
])


def main():
    sets = U.sets([
        ("Carbon stores and processes", [(POOL1, 6), (b_proc, 6), (b_res, 4), (e_res, 4)]),
        ("Photosynthesis and respiration", [(b_air, 5), (b_path, 4), (c_cycle, 4), (POOL1, 3), (b_b1, 4)]),
        ("Combustion and fossil fuels", [(b_ml, 5), (e_flux, 5), (e_b1, 5), (POOL1, 3), (c_cycle, 2)]),
        ("Carbon data", [(e_keel, 5), (e_budget, 5), (b_ml, 1), (e_flux, 1), (b_air, 1), (POOL5, 3), (b_b1, 2)]),
        ("Investigations", [(POOL5, 3), (b_b5, 4), (e_b5, 4), (e_budget, 4), (e_keel, 3), (POOL1, 2)]),
    ])
    make_au(YEAR, "the-carbon-cycle", SORT, "AC9S9U03", "Earth and space sciences",
            "Represent the carbon cycle and examine how key processes including combustion, photosynthesis and respiration rely on "
            "interactions between Earth's spheres (summary of the Australian Curriculum v9.0 Science content description).",
            "The Carbon Cycle", "The carbon cycle",
            "Free Year 9 science worksheets on the carbon cycle: carbon stores, photosynthesis, respiration, combustion, decomposition, "
            "ocean uptake, fossil fuels and CO₂ data. 100 questions with answers.",
            "Carbon atoms move between stores.", "Photosynthesis takes CO₂ out of the air; respiration, combustion and decay put it back.",
            "<p><b>Carbon cycles between the air, living things, oceans and rocks.</b></p><ul>"
            "<li>Photosynthesis: carbon dioxide + water → glucose + oxygen (removes CO₂ from the air).</li>"
            "<li>Respiration, decomposition and combustion return CO₂ to the air.</li>"
            "<li>Burning fossil fuels moves carbon stored for millions of years back into the air faster than it is removed.</li></ul>",
            [("A tree grows 50 kg heavier. Where did the carbon come from?", ["photosynthesis uses CO₂ from air"], "the air"),
             ("Coal is burnt. Which store gains carbon?", ["combustion releases CO₂"], "the atmosphere")],
            ["Thinking plants get their carbon from the soil.", "Thinking only animals respire.", "Thinking carbon is destroyed when fuel burns."],
            [("Why is the carbon cycle important?", "It moves carbon between living things and the environment. The balance of carbon dioxide in the air affects Earth's temperature."),
             ("How do humans change the carbon cycle?", "Burning fossil fuels and clearing forests add carbon dioxide to the air faster than plants and oceans can remove it."),
             ("What is a carbon sink?", "A store that takes in more carbon than it gives out, such as a growing forest, seagrass meadow or the ocean.")],
            sets)


if __name__ == "__main__":
    main()
