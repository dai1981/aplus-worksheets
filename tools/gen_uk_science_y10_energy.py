# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Physics): Energy
  python tools/gen_uk_science_y10_energy.py
Energy stores and systems, kinetic energy (½mv²), gravitational potential energy (mgh), elastic potential energy
(½ke²), specific heat capacity (ΔE = mcΔθ), power (P = E ÷ t), conservation and dissipation of energy, efficiency
and energy resources. Reuses the US Physics energy questions in British English, the store, efficiency and resource
questions of the Year 8 unit (new seed); specific heat capacity uses J/kg °C as at GCSE.
Wrong answers come from real mistakes: "KE = mv²", "energy is used up", "a device can be more than 100% efficient",
"temperature and thermal energy are the same".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build
from sci_phys import uniq, num

U, R, P, us = U4(62010)
KP = "phys_kinetic_and_potential_energy"
CO = "phys_conservation_of_energy"
us_ke, us_pe, us_spring, us_work = [us(KP, "g_" + n) for n in ("ke", "pe", "spring", "work")]
us_drop, us_coast, us_loss = us(CO, "g_drop"), us(CO, "g_coast"), us(CO, "g_loss")
y8_store, y8_eff, y8_res = [us.uk("gen_uk_science_y8_energy_and_power", n) for n in ("g_store", "g_eff", "g_res")]

MAT = [("water", 4200), ("aluminium", 900), ("iron", 450), ("copper", 390), ("concrete", 880), ("oil", 2000)]


def g_shc():
    m_name, c = R.choice(MAT)
    mass = R.choice([0.5, 1, 2, 2.5, 4, 5])
    dt = R.choice([2, 4, 5, 10, 20, 25])
    k = R.choice(["E", "dt"])
    if not once(("sh", m_name, mass, dt, k)):
        return None
    e = mass * c * dt
    if e != int(e):
        return None
    if k == "E":
        g = "{:,} J".format(int(e))
        return item("How much energy is needed to raise the temperature of %s kg of %s by %d °C? (specific heat capacity = {:,} J/kg °C)".format(c) % (num(mass), m_name, dt), g,
                    uniq(g, ["{:,} J".format(int(c * dt)), "{:,} J".format(int(mass * c)), "{:,} J".format(int(e * 10)), "{:,} J".format(int(mass * dt))]),
                    "ΔE = m × c × Δθ = %s × {:,} × %d.".format(c) % (num(mass), dt))
    g = "%d °C" % dt
    return item("{:,} J of energy heats %s kg of %s. By how much does its temperature rise? (specific heat capacity = {:,} J/kg °C)".format(int(e), c) % (num(mass), m_name), g,
                uniq(g, ["%s °C" % num(e / c), "%s °C" % num(dt * mass * 2), "%d °C" % (dt * 10), "%s °C" % num(e / mass / 1000)]), "Δθ = ΔE ÷ (m × c).")


def g_pow():
    k = R.choice(["P", "E", "t"])
    p = R.choice([20, 40, 60, 100, 500, 1000, 1500, 2000])
    t = R.choice([5, 10, 20, 30, 60, 120])
    if not once(("pw", p, t, k)):
        return None
    e = p * t
    if k == "P":
        g = "{:,} W".format(p)
        return item("A motor transfers {:,} J of energy in %d s. What is its power?".format(e) % t, g, uniq(g, ["{:,} W".format(e * t), "{:,} W".format(e), "{:,} W".format(t), "{:,} W".format(p * 10)]), "P = E ÷ t.")
    if k == "E":
        g = "{:,} J".format(e)
        return item("A {:,} W heater is on for %d s. How much energy does it transfer?".format(p) % t, g, uniq(g, ["{:,} J".format(p), "%s J" % num(p / t), "{:,} J".format(p + t), "{:,} J".format(e * 10)]), "E = P × t.")
    g = "%d s" % t
    return item("A {:,} W kettle transfers {:,} J. How long is it on for?".format(p, e), g, uniq(g, ["{:,} s".format(e * p), "%d s" % (t * 10), "{:,} s".format(p), "%d s" % (t * 2)]), "t = E ÷ P.")


B1 = bank([
    ("What is the equation for kinetic energy?", "kinetic energy = ½ × mass × speed²", ["kinetic energy = mass × speed", "kinetic energy = ½ × mass × speed", "kinetic energy = mass × g × height"], "Ek = ½mv²."),
    ("What is the equation for gravitational potential energy?", "GPE = mass × gravitational field strength × height", ["GPE = ½ × mass × speed²", "GPE = force × time", "GPE = mass ÷ height"], "Ep = mgh."),
    ("What is specific heat capacity?", "the energy needed to raise the temperature of 1 kg of a substance by 1 °C", ["the temperature of a substance", "the energy to melt 1 kg", "the mass of a substance"], "Water: 4,200 J/kg °C."),
    ("What is power?", "the rate at which energy is transferred", ["the total energy transferred", "the force on an object", "the efficiency of a device"], "Measured in watts (J/s)."),
])
B5 = bank([
    ("How can unwanted energy transfers be reduced?", "lubrication to reduce friction and thermal insulation to reduce heating", ["adding more friction", "removing insulation", "using thinner walls"], "Less dissipation."),
    ("Why do thick walls with a low thermal conductivity keep a house warm?", "Energy is transferred through them more slowly.", ["They create energy.", "They conduct heat quickly.", "They reflect sound."], "Insulation."),
    ("Which energy resource is renewable and reliable day and night?", "geothermal or hydroelectric power", ["solar power", "coal", "natural gas"], "Solar does not work at night."),
    ("What is one disadvantage of nuclear power?", "It produces radioactive waste that must be stored safely.", ["It releases lots of carbon dioxide.", "It only works when windy.", "It runs out next year."], "No carbon dioxide while running."),
])

if __name__ == "__main__":
  build(U, 10, "energy", 10, "Physics", "Energy",
      "Energy changes in a system and the ways energy is stored before and after such changes; kinetic energy, elastic potential energy and gravitational potential energy calculations; specific heat capacity; power; conservation and dissipation of energy; efficiency; national and global energy resources.",
      "Energy", "Energy",
      "Free Year 10 GCSE Combined Science worksheets on energy: stores, kinetic and gravitational potential energy, elastic energy, specific heat capacity, power, efficiency and energy resources. 100 questions with answers.",
      "Energy is never created or destroyed.",
      "Ek = ½mv², Ep = mgh, ΔE = mcΔθ, P = E ÷ t.",
      "<p><b>Energy is transferred between stores; the total stays the same.</b></p><ul><li>Kinetic energy = ½mv². Gravitational potential energy = mgh. Elastic potential energy = ½ke².</li>"
      "<li>ΔE = mcΔθ: specific heat capacity is the energy to warm 1 kg by 1 °C.</li>"
      "<li>Power = energy ÷ time. Efficiency = useful output ÷ total input. Wasted energy is usually dissipated as heat.</li></ul>",
      [("2 kg at 3 m/s. Kinetic energy?", ["½ × 2 × 3²"], "9 J"), ("1 kg of water warmed by 10 °C?", ["1 × 4,200 × 10"], "42,000 J")],
      ["Forgetting to square the speed in ½mv².", "Saying energy is used up.", "Thinking efficiency can be over 100%."],
      [("How do you calculate kinetic energy?", "Kinetic energy (J) = ½ × mass (kg) × speed² (m/s). Square the speed first."),
       ("What is specific heat capacity?", "The energy needed to raise 1 kg of a substance by 1 °C. Use ΔE = m × c × Δθ."),
       ("How do you calculate efficiency?", "Efficiency = useful energy output ÷ total energy input. Multiply by 100 for a percentage.")],
      [("Energy stores", B1 + [(y8_store, 6), (us_ke, 10)]),
       ("Kinetic and potential energy", [(us_pe, 8), (us_spring, 6), (us_drop, 6)]),
       ("Specific heat capacity", [(g_shc, 16), (us_work, 4)]),
       ("Power and efficiency", [(g_pow, 10), (y8_eff, 6), (us_loss, 4)]),
       ("Conservation and resources", B5 + [(y8_res, 6), (us_coast, 6), (us_work, 4)])])
