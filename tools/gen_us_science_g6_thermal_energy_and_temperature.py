# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Thermal Energy and Temperature (MS-PS3-4)
  python tools/gen_us_science_g6_thermal_energy_and_temperature.py
Plan an investigation to determine the relationships among the energy transferred, the type of matter,
the mass, and the change in the average kinetic energy of the particles (temperature).
Same energy into more mass -> smaller temperature change; different materials (water vs. sand vs. metal)
change temperature by different amounts; more energy -> bigger temperature change. Temperature vs. thermal energy.
Assessment boundary: no calculations of specific heat; qualitative and simple proportional reasoning only.
Wrong answers come from real mistakes: "temperature and thermal energy are the same", "a bathtub of warm water
has less thermal energy than a cup of hot tea", "all materials heat up the same".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(60106)
R = U.R
P = People(R)


def g_mass():
    m1, m2 = sorted(R.sample([100, 200, 300, 400, 500], 2))
    rise = R.choice([10, 12, 15, 20, 24, 30])
    if (rise * m1) % m2:
        return None
    r2 = rise * m1 // m2
    p = P.next()
    rows = [["%d g" % m1, "%d °C" % rise], ["%d g" % m2, "%d °C" % r2]]
    tab = table(["Mass of water", "Temperature rise"], rows)
    k = R.choice(["which", "why", "predict"])
    if k == "which":
        return item(tab + "%s heated two beakers of water on the same hot plate for 5 minutes. Which beaker's temperature rose more?" % p[0], "the %d g beaker" % m1,
                    ["the %d g beaker" % m2, "They rose the same amount.", "Neither changed."], "The same energy was shared by fewer particles in the smaller mass.")
    if k == "why":
        return item(tab + "In %s's test, why did the %d g of water warm up less?" % (p[0], m2), "The same energy was spread over more particles.",
                    ["It got less energy from the hot plate.", "Bigger amounts of water cannot get warm.", "Its particles are bigger."], "More mass means a smaller temperature change for the same energy.")
    m3 = m1 * 2
    r3 = rise // 2 if rise % 2 == 0 else None
    if r3 is None or m3 in (m1, m2):
        return None
    return item(tab + "If %s heats %d g of water the same way for 5 minutes, about how much will its temperature rise?" % (p[0], m3), "%d °C" % r3,
                ["%d °C" % (rise * 2), "%d °C" % rise, "0 °C"], "Twice the mass of %d g gives about half the rise: %d ÷ 2 = %d °C." % (m1, rise, r3))


MATS = [("sand", 3), ("water", 1), ("iron", 4), ("soil", 2), ("aluminum", 3)]


def g_material():
    a, b = R.sample([("sand", 30), ("water", 8), ("iron", 40), ("soil", 22), ("concrete", 25)], 2)
    if a[1] == b[1]:
        return None
    p = P.next()
    rows = [[a[0], "%d °C" % a[1]], [b[0], "%d °C" % b[1]]]
    hi = a if a[1] > b[1] else b
    lo = b if hi == a else a
    tab = table(["Material (same mass)", "Temperature rise in 10 min of sunlight"], rows)
    if R.random() < 0.5:
        return item(tab + "%s put the same mass of %s and %s in sunlight. Which material changed temperature more?" % (p[0], a[0], b[0]), hi[0],
                    [lo[0], "They changed the same.", "Neither changed."], "%s rose %d °C; %s rose only %d °C." % (hi[0].capitalize(), hi[1], lo[0], lo[1]))
    return item(tab + "What does %s's data show?" % p[0], "Different materials change temperature by different amounts with the same energy.",
                ["All materials heat up the same.", "Mass is the only thing that matters.", "Sunlight does not carry energy."], "The type of matter affects the temperature change.")


def g_energy():
    times = [2, 4, 6]
    k1 = R.choice([3, 4, 5, 6])
    t0 = R.choice([18, 20, 22])
    temps = [t0 + k1 * t for t in times]
    rows = [["%d min" % t, "%d °C" % v] for t, v in zip(times, temps)]
    p = P.next()
    tab = table(["Heating time", "Water temperature"], rows)
    if R.random() < 0.5:
        return item(tab + "%s heated the same 200 g of water on the same burner. What happens when more energy is added?" % p[0], "The temperature rises more.",
                    ["The temperature rises less.", "The temperature does not change.", "The water loses mass."], "Longer heating adds more energy, so the temperature goes up more.")
    nxt = t0 + k1 * 8
    return item(tab + "If the pattern continues, what will %s's water temperature be at 8 minutes?" % p[0], "%d °C" % nxt,
                ["%d °C" % temps[-1], "%d °C" % (nxt + k1), "%d °C" % (temps[-1] + 2)], "It rises %d °C every minute: %d + %d × 2 = %d °C." % (k1, temps[-1], k1, nxt))


def g_te():
    pairs = [("a bathtub of warm water (40 °C)", "a cup of hot tea (80 °C)"), ("a swimming pool (25 °C)", "a pot of boiling water (100 °C)"),
             ("a large lake (15 °C)", "a hot spark (900 °C)"), ("a big pot of soup (60 °C)", "a spoonful of the same soup (60 °C)")]
    big, small = R.choice(pairs)
    k = R.choice(["te", "temp"])
    who = P.next()[0] + " compares two things. "
    if "same soup" in small:
        if k == "temp":
            return item(who + "Which has a higher temperature: %s or %s?" % (big, small), "They have the same temperature.", [big, small, "You cannot compare temperatures."],
                        "Both are 60 °C, so the particles have the same average energy.")
        return item(who + "Which has more thermal energy: %s or %s?" % (big, small), big, [small, "They have the same thermal energy.", "Neither has thermal energy."],
                    "Same temperature, but the big pot has many more particles, so it has more total thermal energy.")
    if k == "temp":
        return item(who + "Which has a higher temperature: %s or %s?" % (big, small), small, [big, "They are the same.", "Neither has a temperature."],
                    "Temperature measures the average motion of the particles.")
    return item(who + "Which has more total thermal energy: %s or %s?" % (big, small), big, [small, "They have the same thermal energy.", "Neither has thermal energy."],
                "Thermal energy is the total energy of all the particles; the larger amount has far more particles.")


B1 = bank([
    ("What does temperature measure?", "the average kinetic energy (motion) of the particles", ["the total energy of all the particles", "the mass of an object", "the size of the particles"],
     "Faster particles mean higher temperature."),
    ("What is thermal energy?", "the total kinetic energy of all the particles in an object", ["only the temperature", "the energy of light", "the weight of an object"],
     "More particles at the same temperature means more thermal energy."),
    ("Two pots of water get the same amount of heat. Pot A has 1 kg and pot B has 2 kg. Which warms up more?", "pot A", ["pot B", "They warm up the same.", "Neither warms up."],
     "Less mass means a bigger temperature change."),
    ("Why does sand on a beach get hot faster than the ocean water?", "Sand changes temperature more easily than water with the same energy.", ["Sand gets more sunlight.", "Water has no particles.", "The ocean is always cold."],
     "Different materials change temperature differently."),
    ("When you heat water, what happens to its particles?", "They move faster on average.", ["They move slower.", "They get heavier.", "They stop moving."], "Adding energy increases kinetic energy."),
    ("In an investigation about mass and temperature change, which variable should you change?", "the mass of the material", ["the amount of energy and the mass", "the material and the mass", "nothing"],
     "Change only one variable."),
    ("What tool do you need to measure a change in temperature?", "a thermometer", ["a balance", "a ruler", "a stopwatch only"], "Measure before and after."),
    ("Energy is transferred from a hot stove to a pot of water. What happens to the stove's particles near the pot?", "They lose some kinetic energy.", ["They gain energy.", "They stop moving.", "Nothing changes."],
     "Energy moves from hotter to cooler."),
])
B5 = bank([
    ("Ava wants to test whether the type of material affects temperature change. Which setup is best?", "the same mass of sand, water and soil under the same lamp for the same time", ["different masses of each under different lamps", "only water under one lamp", "sand in sun and water in shade"],
     "Keep everything the same except the material."),
    ("Leo adds 100 g of 80 °C water to 100 g of 20 °C water. About what temperature is the mixture?", "50 °C", ["100 °C", "80 °C", "20 °C"],
     "Equal masses meet in the middle: (80 + 20) ÷ 2 = 50 °C."),
    ("Mia adds 100 g of 80 °C water to 300 g of 20 °C water. Will the mixture be closer to 80 °C or 20 °C?", "closer to 20 °C", ["closer to 80 °C", "exactly 50 °C", "100 °C"],
     "There is more cold water, so the final temperature is closer to 20 °C."),
    ("Why do coastal cities have milder temperatures than cities far inland?", "Large amounts of water change temperature slowly.", ["The ocean makes its own heat.", "Coastal cities get no sunlight.", "Sand is always cool."],
     "Water keeps nearby land from getting very hot or very cold."),
    ("Noah heats a small and a large pan of water on the same stove. The small one boils first. What does this show?", "Less mass needs less energy to reach the same temperature.", ["The small pan got more heat.", "Large pans cannot boil.", "Mass does not matter."],
     "Mass affects temperature change."),
])


def body():
    think = ("<p><b>Temperature</b> measures the average motion (kinetic energy) of particles. <b>Thermal energy</b> is the total energy of all the particles.</p>"
             "<p>When the same amount of energy is added:</p><ul><li><b>Less mass</b> changes temperature <b>more</b>; more mass changes temperature less.</li>"
             "<li>Different <b>materials</b> change temperature by different amounts (sand heats faster than water).</li>"
             "<li><b>More energy</b> added means a bigger temperature change.</li></ul>"
             "<p>A bathtub of warm water has more thermal energy than a cup of hot tea, even though the tea has a higher temperature.</p>")
    ex = [("Same heat to 100 g and 400 g of water. Which warms more?", ["Less mass, bigger change."], "the 100 g"),
          ("A cup and a pot of soup are both 60 °C. Which has more thermal energy?", ["Same temperature.", "The pot has more particles."], "the pot")]
    mist = ["Thinking temperature and thermal energy are the same thing.",
            "Thinking all materials heat up the same way.",
            "Changing more than one variable in an investigation."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Temperature and thermal energy", B1 + [(g_te, 6), (g_mass, 6)]),
        ("Mass and temperature change", [(g_mass, 14), (g_te, 6)]),
        ("Type of material", [(g_material, 14), (g_energy, 6)]),
        ("More energy, more change", [(g_energy, 12), (g_mass, 4), (g_material, 4)]),
        ("Planning investigations", B5 + [g_energy, g_material, g_mass, g_te]),
    ])
    make("grade-6", "thermal-energy-and-temperature", 6, "MS-PS3-4",
         "Plan an investigation to determine the relationships among the energy transferred, the type of matter, the mass, and the change in the average kinetic energy of the particles as measured by the temperature of the sample.",
         "Thermal Energy and Temperature",
         "Grade 6 Thermal Energy Worksheets: Temperature, Mass and Type of Material",
         "Thermal Energy and Temperature",
         "Free middle school science worksheets on thermal energy and temperature (NGSS MS-PS3-4): average kinetic energy, how mass and material affect temperature change, and heating data. 100 practice questions with answers.",
         "The same energy changes temperature differently.",
         "Less mass or a different material can mean a bigger temperature change. Temperature is the average energy of particles.",
         body(),
         [("What is the difference between temperature and thermal energy?", "Temperature is the average kinetic energy of the particles. Thermal energy is the total energy of all the particles."),
          ("How does mass affect temperature change?", "With the same energy added, a smaller mass changes temperature more than a larger mass."),
          ("Why does sand get hotter than water in the sun?", "Different materials change temperature by different amounts. Sand warms up much faster than water.")],
         sets)


if __name__ == "__main__":
    main()
