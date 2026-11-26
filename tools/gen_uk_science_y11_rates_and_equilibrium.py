# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Chemistry): Rates and Equilibrium
  python tools/gen_uk_science_y11_rates_and_equilibrium.py
Calculating mean rates of reaction from gas volume or mass change, factors affecting the rate (concentration,
pressure, surface area, temperature, catalysts) and collision theory, reading rate graphs and 'disappearing cross'
data, reversible reactions and energy changes, dynamic equilibrium and (higher tier) Le Chatelier's principle.
Gas volumes are in cm³. Reuses the US Chemistry rate and equilibrium questions in British English.
Wrong answers come from real mistakes: "a catalyst is used up", "higher temperature only makes more collisions",
"a longer time means a faster reaction", "at equilibrium the reactions stop".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62105)
RR, EQ = "chem_reaction_rates", "chem_chemical_equilibrium"
ML = (("mL/s", "cm³/s"), ("mL", "cm³"))
us_factor, us_cat = us(RR, "g_factor"), us(RR, "g_cat")
us_rate, us_data = us(RR, "g_rate", rep=ML), us(RR, "g_data", rep=ML)
us_shift, us_more, us_reach = us(EQ, "g_shift"), us(EQ, "g_more"), us(EQ, "g_reach")

COLL = [("increasing the concentration", "There are more particles in the same volume, so collisions are more frequent."),
        ("increasing the pressure of a gas", "The particles are closer together, so collisions are more frequent."),
        ("increasing the surface area", "More particles are exposed, so collisions are more frequent."),
        ("increasing the temperature", "Particles move faster, so they collide more often and with more energy."),
        ("adding a catalyst", "It provides a different pathway with a lower activation energy.")]


def g_coll():
    f, why = R.choice(COLL)
    k = R.choice(["why", "which"])
    if not once(("co", f, k)):
        return None
    if k == "why":
        return item("Use collision theory. Why does %s speed up a reaction?" % f, why, [x[1] for x in COLL if x[0] != f][:3], "Rate depends on how often particles collide with enough energy.")
    return item("Which change speeds up a reaction for this reason? “%s”" % why, f, [x[0] for x in COLL if x[0] != f][:3], "Match the change to its explanation.")


def g_mean():
    k = R.choice(["gas", "gas", "mass"])
    t = R.choice([10, 20, 25, 30, 40, 50, 60, 80, 100, 120])
    if k == "gas":
        r = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
        v = r * t
        if v != int(v) or not once(("mg", r, t)):
            return None
        name = P.next()[0]
        f = lambda x: ("%g" % x)
        return item("%s collected %d cm³ of gas in %d s. What is the mean rate of reaction?" % (name, v, t), "%s cm³/s" % f(r),
                    ["{:,} cm³/s".format(int(v * t)), "%s cm³/s" % f(round(t / v, 2)), "%s cm³/s" % f(v)],
                    "Mean rate = volume ÷ time = %d ÷ %d." % (v, t))
    m0 = R.choice([80.0, 95.0, 102.0, 120.0, 150.0])
    loss = R.choice([0.5, 1.0, 1.2, 1.5, 2.0, 2.4, 3.0])
    r = loss / t
    if r * 1000 != int(r * 1000) or not once(("mm", m0, loss, t)):
        return None
    g = "%g g/s" % r
    return item("A flask of marble chips and acid had a mass of %.1f g. After %d s it was %.1f g. What is the mean rate of mass loss?" % (m0, t, m0 - loss), g,
                ["%g g/s" % round(m0 / t, 3), "%g g/s" % loss, "%g g/s" % (loss * t)], "Loss = %.1f g. Rate = %.1f ÷ %d." % (loss, loss, t))


def g_cross():
    temps = [20, 30, 40, 50]
    base = R.choice([80, 96, 100, 112, 120, 128, 140, 160])
    times = [base, base // 2 + R.choice([-4, 0, 4]), base // 4 + R.choice([-2, 0, 2]), base // 8 + R.choice([-1, 0, 1])]
    k = R.choice(["fast", "trend", "pred"])
    if not once(("cr", base, tuple(times), k)):
        return None
    name = P.next()[0]
    tab = table(["Temperature (°C)"] + [str(x) for x in temps], [["Time for the cross to disappear (s)"] + [str(x) for x in times]])
    if k == "fast":
        return item(tab + "%s timed sodium thiosulfate reacting with acid. At which temperature was the reaction fastest?" % name, "50 °C", ["20 °C", "30 °C", "40 °C"],
                    "The shortest time means the fastest rate.")
    if k == "trend":
        return item(tab + "What do %s's results show?" % name, "As the temperature rises, the time falls, so the rate increases.",
                    ["As the temperature rises, the reaction gets slower.", "Temperature has no effect.", "A longer time means a faster reaction."], "Rate ∝ 1/time.")
    return item(tab + "%s repeats the test at 35 °C. Predict the time." % name, "between %d s and %d s" % (times[2], times[1]),
                ["less than %d s" % times[3], "more than %d s" % times[0], "exactly %d s" % times[0]], "35 °C is between 30 °C and 40 °C.")


REV = [("hydrated copper sulfate ⇌ anhydrous copper sulfate + water", "endothermic"), ("ammonium chloride ⇌ ammonia + hydrogen chloride", "endothermic"),
       ("calcium carbonate ⇌ calcium oxide + carbon dioxide", "endothermic"), ("nitrogen + hydrogen ⇌ ammonia", "exothermic"),
       ("sulfur dioxide + oxygen ⇌ sulfur trioxide", "exothermic")]


def g_dir():
    eq, fw = R.choice(REV)
    if not once(("dir", eq)):
        return None
    rv = "exothermic" if fw == "endothermic" else "endothermic"
    return item("The forward reaction is %s: %s. What is the reverse reaction?" % (fw, eq), rv, [fw, "neither", "it depends on the colour"],
                "The same amount of energy is transferred in each direction, but the opposite way.")


B1 = bank([
    ("What must happen for particles to react?", "They must collide with at least the activation energy.", ["They must stay still.", "They must be a liquid.", "They must be the same colour."], "Collision theory."),
    ("What is the unit of rate when gas volume is measured?", "cm³/s", ["g", "s", "cm³"], "Volume per unit time."),
    ("Why does powder react faster than a lump?", "It has a larger surface area.", ["It has a smaller surface area.", "It is hotter.", "It has more mass."], "More particles exposed."),
    ("Which method measures the rate by the loss of mass?", "putting the flask on a balance and recording the mass as gas escapes", ["timing a colour change only", "counting bubbles by hand only", "measuring the pH"], "Mass falls as gas leaves."),
])
B4 = bank([
    ("What is a catalyst?", "a substance that speeds up a reaction without being used up", ["a reactant that is used up", "a product of the reaction", "something that slows a reaction"], "Enzymes are biological catalysts."),
    ("What happens when water is added to white anhydrous copper sulfate?", "It turns blue and gets warm.", ["It turns white.", "It gets cold.", "Nothing happens."], "The reverse reaction is exothermic."),
    ("What is dynamic equilibrium?", "The forward and reverse reactions happen at the same rate.", ["Both reactions stop.", "Only the forward reaction happens.", "There are no products."], "Concentrations stay constant."),
    ("What is needed for a reversible reaction to reach equilibrium?", "a closed system", ["an open beaker", "a catalyst", "a high temperature"], "Nothing can get in or out."),
])
B5 = bank([
    ("What does Le Chatelier's principle say?", "If a condition changes, the equilibrium shifts to counteract the change.", ["The equilibrium never changes.", "A catalyst moves the equilibrium.", "The reaction stops."], "Higher tier."),
    ("Does a catalyst change the position of equilibrium?", "No. It makes equilibrium reached faster.", ["Yes, to the right.", "Yes, to the left.", "It stops the reaction."], "Both directions speed up equally."),
])

if __name__ == "__main__":
  build(U, 11, "rates-and-equilibrium", 5, "Chemistry", "The rate and extent of chemical change",
      "Calculating rates of reactions; factors which affect the rates of chemical reactions (concentration, pressure, surface area, temperature, catalysts); collision theory and activation energy; reversible reactions and energy changes; equilibrium; (higher tier) the effect of changing conditions on equilibrium (Le Chatelier's principle).",
      "Rates and Equilibrium", "Rates and Equilibrium",
      "Free Year 11 GCSE Combined Science worksheets on rates of reaction and equilibrium: mean rate, collision theory, temperature and concentration, catalysts, reversible reactions and Le Chatelier's principle. 100 questions with answers.",
      "Mean rate = amount of product ÷ time.",
      "More frequent, more energetic collisions mean a faster rate.",
      "<p><b>Reactions speed up when particles collide more often or with more energy.</b></p><ul><li>Mean rate = volume of gas (cm³) ÷ time (s), or mass lost (g) ÷ time (s).</li>"
      "<li>Concentration, pressure, surface area and temperature increase the rate. A catalyst lowers the activation energy.</li>"
      "<li>In a closed system a reversible reaction reaches equilibrium: forward and reverse rates are equal.</li></ul>",
      [("60 cm³ of gas in 30 s. Mean rate?", ["60 ÷ 30"], "2 cm³/s"), ("Forward reaction endothermic. Reverse?", ["Opposite direction"], "exothermic")],
      ["Thinking a catalyst is used up.", "Thinking a longer time means a faster reaction.", "Thinking the reactions stop at equilibrium."],
      [("How do you calculate a mean rate of reaction?", "Divide the amount of product made (or reactant used) by the time taken, for example cm³ of gas ÷ seconds."),
       ("How does temperature affect the rate?", "At a higher temperature particles move faster, so they collide more often and more collisions have at least the activation energy."),
       ("What happens at dynamic equilibrium?", "The forward and reverse reactions continue at the same rate, so the amounts of reactants and products stay constant.")],
      [("Collision theory", B1 + [(g_coll, 7), (us_factor, 9)]),
       ("Mean rate", [(g_mean, 14), (us_rate, 6)]),
       ("Rate data", [(g_cross, 10), (us_data, 10)]),
       ("Catalysts and reversible reactions", B4 + [(us_cat, 3), (g_coll, 2), (us_reach, 3), (g_dir, 4), (us_shift, 4)]),
       ("Equilibrium", B5 + [(us_shift, 12), (us_more, 6)])])
