# -*- coding: utf-8 -*-
"""
US High School Chemistry: Thermal Energy and Specific Heat (HS-PS3-4)
  python tools/gen_us_science_chem_thermal_energy_and_specific_heat.py
Plan and conduct an investigation to provide evidence that the transfer of thermal energy when two components of
different temperature are combined within a closed system results in a more uniform energy distribution among the
components in the system (second law of thermodynamics).
Heat flow from hot to cold, thermal equilibrium, specific heat, q = mcΔT, mixing water at two temperatures and simple
calorimetry.
Wrong answers come from real mistakes: "cold flows into hot objects", "the final temperature is the simple average
of any two masses", "a high specific heat means it heats up quickly".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import num

U = Unit(90213)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


C = {"water": 4.18, "aluminum": 0.90, "iron": 0.45, "copper": 0.39, "glass": 0.84, "granite": 0.79, "olive oil": 1.97, "ethanol": 2.44, "silver": 0.24, "lead": 0.13}


def g_q():
    who = P.next()[0]
    s = R.choice(list(C))
    c = C[s]
    m = R.choice([10, 20, 25, 40, 50, 100, 200, 250, 500])
    dt = R.choice([2, 4, 5, 10, 12, 15, 20, 25, 30, 40])
    q = m * c * dt
    k = R.choice(["q", "q", "dt", "m"])
    if q != round(q, 1) or not once(("q", s, m, dt, k)):
        return None
    if k == "q":
        w = [num(m * c), num(q / 1000) if q >= 1000 else num(m * dt), num(m * c * dt * 2), num(m * dt / c)]
        w = [x + " J" for x in dict.fromkeys(w) if x != num(q)][:3]
        return item("How much heat does %s need to warm %d g of %s by %d °C? (c = %s J/g·°C)" % (who, m, s, dt, num(c)), num(q) + " J", w,
                    "q = mcΔT = %d × %s × %d = %s J." % (m, num(c), dt, num(q)))
    if k == "dt":
        w = [num(q / m), num(q / c), num(dt * 2), num(dt + 10)]
        w = [x + " °C" for x in dict.fromkeys(w) if x != num(dt)][:3]
        return item("%s adds %s J of heat to %d g of %s (c = %s J/g·°C). By how much does its temperature rise?" % (who, num(q), m, s, num(c)), "%d °C" % dt, w,
                    "ΔT = q ÷ (mc) = %s ÷ (%d × %s) = %d °C." % (num(q), m, num(c), dt))
    w = [num(q / dt), num(q / c), num(m * 2), num(m / 2)]
    w = [x + " g" for x in dict.fromkeys(w) if x != num(m)][:3]
    return item("It takes %s J to raise the temperature of a sample of %s by %d °C (c = %s J/g·°C). What is its mass?" % (num(q), s, dt, num(c)), "%d g" % m, w,
                "m = q ÷ (cΔT) = %s ÷ (%s × %d) = %d g." % (num(q), num(c), dt, m))


def g_mix():
    who = P.next()[0]
    m1, m2 = R.choice([50, 100, 150, 200, 300]), R.choice([50, 100, 150, 200, 300])
    t1, t2 = R.randint(5, 30), R.randint(50, 90)
    tf = (m1 * t1 + m2 * t2) / (m1 + m2)
    if tf != int(tf) or not once(("mx", m1, m2, t1, t2)):
        return None
    tf = int(tf)
    avg = (t1 + t2) / 2
    w = [num(avg), num(t2 - t1), num((t1 + t2) / 2 + 10)]
    w = [x + " °C" for x in dict.fromkeys(w) if x != str(tf)][:3]
    if len(w) < 3:
        w.append("%d °C" % (tf + 5))
    return item("%s mixes %d g of water at %d °C with %d g of water at %d °C in an insulated cup. What is the final temperature?" % (who, m1, t1, m2, t2), "%d °C" % tf, w[:3],
                "Heat lost = heat gained: (%d × %d + %d × %d) ÷ %d = %d °C." % (m1, t1, m2, t2, m1 + m2, tf))


def g_cal():
    who = P.next()[0]
    s = R.choice(["aluminum", "iron", "copper", "lead", "silver"])
    k = R.choice(["dir", "final", "who", "same"])
    tm, tw = R.choice([80, 90, 100, 95]), R.choice([18, 20, 22, 25])
    if not once(("cl", s, tm, tw, k)) or (k != "final" and not once(("ck", k), 4)):
        return None
    if k == "dir":
        return item("%s drops a %s block at %d °C into water at %d °C. Which way does thermal energy flow?" % (who, s, tm, tw), "from the %s to the water" % s,
                    ["from the water to the %s" % s, "both ways equally, so nothing changes", "cold flows from the water into the %s" % s], "Energy flows from hot to cold.")
    if k == "final":
        return item("%s %s block at %d °C is placed in water at %d °C in a closed, insulated cup. Which final temperature is possible?" % ("An" if s[0] in "aeiou" else "A", s, tm, tw), "%d °C" % (tw + R.randint(2, 8)),
                    ["%d °C" % (tm + 5), "%d °C" % (tw - 5), "%d °C" % (tm + tw)], "The final temperature is between the two starting temperatures.")
    if k == "who":
        return item("In %s's insulated cup, a hot %s block and cool water reach the same temperature. Which statement is true?" % (who, s), "The heat lost by the metal equals the heat gained by the water.",
                    ["The metal gains heat.", "The water loses heat.", "Energy is destroyed."], "Energy is conserved in a closed system.")
    return item("After a while, the %s block and the water in %s's cup stop changing temperature. What state have they reached?" % (s, who), "thermal equilibrium (the same temperature)",
                ["the metal is still hotter", "the water is now hotter", "both are at 0 °C"], "Energy spreads out until temperatures are equal.")


def g_cmp():
    a, b = R.sample(list(C), 2)
    if abs(C[a] - C[b]) < 0.2 or not once(("cp", tuple(sorted((a, b))))):
        return None
    m = R.choice([100, 200, 500])
    fast = a if C[a] < C[b] else b
    slow = b if fast == a else a
    k = R.random() < 0.5
    tab = table(["Substance", "Specific heat (J/g·°C)"], [[a, num(C[a])], [b, num(C[b])]])
    if k:
        return item(tab + "Equal %d g samples of %s and %s get the same heat. Which warms up more?" % (m, a, b), fast, [slow, "They warm the same.", "Neither warms."],
                    "Lower specific heat → bigger temperature change.")
    return item(tab + "Which needs more energy to warm %d g by 10 °C: %s or %s?" % (m, a, b), slow, [fast, "They need the same.", "Neither needs energy."], "Higher specific heat → more energy needed.")


B1 = bank([
    ("Which way does thermal energy flow by itself?", "from a hotter object to a colder object", ["from a colder object to a hotter one", "in no direction", "only upward"], "Second law of thermodynamics."),
    ("What is thermal equilibrium?", "when objects in contact reach the same temperature", ["when one object becomes very hot", "when heat stops existing", "when an object freezes"], "No more net flow."),
    ("What is specific heat?", "the energy needed to raise 1 g of a substance by 1 °C", ["the temperature of a substance", "the mass of a substance", "how fast it melts"], "Units J/g·°C."),
    ("Why does a beach's sand get hotter than the water on a sunny day?", "Sand has a lower specific heat than water.", ["Sand has a higher specific heat.", "Water absorbs no energy.", "Sand is closer to the Sun."], "Water 4.18 J/g·°C."),
    ("What is temperature a measure of?", "the average kinetic energy of the particles", ["the total energy of all particles", "the amount of heat", "the mass of the particles"], "Average, not total."),
    ("What does a calorimeter measure?", "heat released or absorbed in a process", ["mass", "volume", "pressure"], "Insulated cup."),
    ("In a closed system, what happens to the total energy as temperatures even out?", "It stays the same.", ["It increases.", "It decreases.", "It becomes zero."], "Conservation of energy."),
    ("A spoon in hot soup gets warm. What process moves the energy?", "conduction", ["radiation only", "convection in the spoon", "evaporation"], "Particles collide."),
])
B5 = bank([
    ("Why is the final temperature of mixed water closer to the larger sample's starting temperature?", "The larger sample has more particles, so its temperature changes less.", ["Larger samples are always hotter.", "Mass does not matter.", "Small samples cannot change."],
     "Weighted average."),
    ("Why should a calorimeter be insulated?", "So no energy escapes to or enters from the surroundings.", ["To make it heavier.", "To cool the water.", "To stop the reaction."], "Closed system."),
    ("Ice in a drink melts and the drink gets colder. Which explanation is best?", "Thermal energy flows from the drink into the ice.", ["Cold flows from the ice into the drink.", "The ice creates cold.", "The drink loses mass."], "Hot to cold."),
    ("Why do cities near large lakes have milder temperatures?", "Water's high specific heat lets it absorb and release a lot of energy with little temperature change.", ["Lakes are always warm.", "Water has a low specific heat.", "Lakes block sunlight."],
     "Moderating effect."),
    ("A student mixes hot and cold water, but the final temperature is lower than she calculated. What is the likely reason?", "Some energy was lost to the cup and the air.", ["Energy was created.", "Her calculation used too much mass.", "Water cannot mix."], "Heat losses."),
])


def body():
    think = ("<p><b>Thermal energy flows from hot to cold until temperatures are equal.</b></p>"
             "<ul><li>q = mcΔT (heat = mass × specific heat × temperature change).</li>"
             "<li>In a closed system, heat lost by the hot part = heat gained by the cold part. The final temperature is between the starting ones.</li>"
             "<li>Low specific heat (metals): big temperature change. High specific heat (water): small change.</li></ul>")
    ex = [("Heat to warm 50 g of water by 10 °C (c = 4.18)?", ["50 × 4.18 × 10"], "2,090 J"),
          ("100 g at 20 °C + 100 g at 60 °C?", ["Equal masses: average"], "40 °C")]
    mist = ["Thinking “cold” flows into warm objects.", "Taking a simple average when the masses are different.", "Thinking a high specific heat means fast warming."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Heat flow", B1 + [(g_cal, 8), (g_cmp, 4)]),
        ("Specific heat", [(g_cmp, 10), (g_q, 10)]),
        ("q = mcΔT", [(g_q, 20)]),
        ("Mixing and calorimetry", [(g_mix, 12), (g_cal, 8)]),
        ("Evidence from experiments", B5 + [(g_mix, 6), (g_q, 5), (g_cal, 4)]),
    ])
    make("chemistry", "thermal-energy-and-specific-heat", 13, "HS-PS3-4",
         "Plan and conduct an investigation to provide evidence that the transfer of thermal energy when two components of different temperature are combined within a closed system results in a more uniform energy distribution among the components in the system (second law of thermodynamics).",
         "Thermal Energy and Specific Heat",
         "Specific Heat Worksheets: q = mcΔT, Heat Flow and Calorimetry (High School Chemistry)",
         "Specific Heat",
         "Free high school chemistry worksheets on thermal energy and specific heat (NGSS HS-PS3-4): heat flow, thermal equilibrium, q = mcΔT, mixing water and calorimetry. 100 questions with answers.",
         "Heat flows from hot to cold.",
         "In a closed system, energy spreads out until the temperatures are equal.",
         body(),
         [("What is the formula for heat?", "q = mcΔT: heat equals mass times specific heat times the change in temperature."),
          ("How do you find the final temperature when mixing water?", "Heat lost by the hot water equals heat gained by the cold water, so the final temperature is the mass-weighted average."),
          ("Why does water heat up slowly?", "Water has a high specific heat (4.18 J/g·°C), so it needs a lot of energy for each degree.")],
         sets)


if __name__ == "__main__":
    main()
