# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Physics): Particle Model and Density
  python tools/gen_uk_science_y10_particle_model_and_density.py
Density (ρ = m ÷ V) and measuring it (including the displacement method), the particle model of solids, liquids and
gases, changes of state and conservation of mass, internal energy, specific latent heat (E = mL) and heating and
cooling curves, and gas pressure and temperature. Reuses the state and change questions of the Year 7 unit and the
gas pressure question of the Year 9 unit (new seed).
Wrong answers come from real mistakes: "the temperature rises while ice melts", "particles get bigger when heated",
"density = volume ÷ mass", "a change of state changes the mass".
"""
from uk_sci import item, bank, table, once
from uk_ks4 import U4, build
from sci_phys import uniq, num

U, R, P, us = U4(62012)
y7_state, y7_change = us.uk("gen_uk_science_y7_particles_and_states_of_matter", "g_state"), us.uk("gen_uk_science_y7_particles_and_states_of_matter", "g_change")
y9_gas = us.uk("gen_uk_science_y9_pressure", "g_gas")


def g_rho():
    k = R.choice(["rho", "m", "V", "disp"])
    if k == "disp":
        who = P.next()[0]
        a = R.choice([20, 30, 40, 50])
        dv = R.choice([4, 5, 8, 10, 12, 15])
        rho = R.choice([2.5, 2.7, 7.9, 8.9, 11.3, 1.2])
        m = round(rho * dv, 1)
        if not once(("dp", a, dv, rho)):
            return None
        g = "%s g/cm³" % num(rho)
        return item("%s puts a stone of mass %s g into a measuring cylinder. The water rises from %d cm³ to %d cm³. What is the density of the stone?" % (who, num(m), a, a + dv), g,
                    uniq(g, ["%s g/cm³" % num(m / (a + dv)), "%s g/cm³" % num(dv / m), "%s g/cm³" % num(m * dv), "%s g/cm³" % num(rho * 10)]), "Volume = %d cm³. ρ = %s ÷ %d." % (dv, num(m), dv))
    m = R.choice([2, 5, 10, 20, 27, 54, 79, 120])
    v = R.choice([2, 4, 5, 10, 20])
    rho = m / v
    if rho * 100 != int(rho * 100) or not once(("rh", k, m, v)):
        return None
    if k == "rho":
        g = "%s kg/m³" % num(rho * 1000)
        return item("A block has a mass of %s kg and a volume of %s m³. What is its density?" % (num(m * v), num(v)), "%s kg/m³" % num(m), uniq("%s kg/m³" % num(m), ["%s kg/m³" % num(m * v * v), "%s kg/m³" % num(v / m / v), "%s kg/m³" % num(m * v), "%s kg/m³" % num(m + v)]),
                    "ρ = m ÷ V = %s ÷ %s = %s kg/m³." % (num(m * v), num(v), num(m)))
    if k == "m":
        g = "%s g" % num(rho * v * 10)
        return item("A liquid has a density of %s g/cm³. What is the mass of %d cm³ of it?" % (num(rho), v * 10), g, uniq(g, ["%s g" % num(rho / (v * 10)), "%s g" % num(v * 10 / rho), "%s g" % num(rho + v * 10), "%d g" % (v * 10)]), "m = ρ × V.")
    g = "%s cm³" % num(v * 10)
    return item("An object has a mass of %s g and a density of %s g/cm³. What is its volume?" % (num(rho * v * 10), num(rho)), g, uniq(g, ["%s cm³" % num(rho * v * 10 * rho), "%s cm³" % num(rho), "%s cm³" % num(v * 100), "%s cm³" % num(v)]), "V = m ÷ ρ.")


L = [("ice melting", "specific latent heat of fusion of water", 334000), ("water boiling", "specific latent heat of vaporisation of water", 2260000),
     ("lead melting", "specific latent heat of fusion of lead", 23000), ("ethanol boiling", "specific latent heat of vaporisation of ethanol", 850000),
     ("copper melting", "specific latent heat of fusion of copper", 205000)]


def g_lat():
    what, name, lv = R.choice(L)
    m = R.choice([0.1, 0.2, 0.25, 0.5, 1, 2])
    k = R.random() < 0.6
    if not once(("la", what, m, k)):
        return None
    e = lv * m
    if e != int(e):
        return None
    if k:
        g = "{:,} J".format(int(e))
        return item("How much energy is needed for %s kg of %s (no temperature change)? (%s = {:,} J/kg)".format(lv) % (num(m), what, name), g,
                    uniq(g, ["{:,} J".format(int(lv / m)), "{:,} J".format(lv), "{:,} J".format(int(e * 10)), "{:,} J".format(int(e / 10))]), "E = m × L = %s × {:,}.".format(lv) % num(m))
    g = "%s kg" % num(m)
    return item("{:,} J is used for %s with no temperature change. What mass changed state? (%s = {:,} J/kg)".format(int(e), lv) % (what, name), g,
                uniq(g, ["%s kg" % num(lv / e), "%s kg" % num(m * 10), "{:,} kg".format(int(e * lv)) if e * lv < 1e7 else "%s kg" % num(m / 10), "%s kg" % num(m * 2)]), "m = E ÷ L.")


def tc(x):
    return ("−%d" % -x) if x < 0 else str(x)


def g_curve():
    who = P.next()[0]
    k = R.choice(["flat", "why", "mp", "state", "bp"])
    mp = R.choice([0, 5, 16, 44, 63, 80])
    bp = mp + R.choice([60, 70, 80, 100])
    if not once(("cu", mp, bp, k)) or not once(("cu", k), 2 if k in ("flat", "why") else 6):
        return None
    tab = table(["Time (min)", "Temperature (°C)"], [["0", tc(mp - 20)], ["2", str(mp)], ["4", str(mp)], ["6", str((mp + bp) // 2)], ["8", str(bp)], ["10", str(bp)]])
    intro = tab + "%s heated a solid steadily and recorded its temperature. " % who
    if k == "flat":
        return item(intro + "What is happening between 2 and 4 minutes?", "The solid is melting.", ["The liquid is boiling.", "The solid is getting hotter.", "Nothing is happening."], "The temperature stays the same during a change of state.")
    if k == "why":
        return item(intro + "Why does the temperature stay the same while it melts?", "The energy is used to break bonds between particles, not to raise the temperature.", ["The heater was switched off.", "Particles stop moving.", "Energy is destroyed."], "Latent heat.")
    if k == "mp":
        return item(intro + "What is the melting point of the substance?", "%s °C" % tc(mp), ["%s °C" % tc(x) for x in (mp - 20, bp, (mp + bp) // 2)], "The first flat part.")
    if k == "bp":
        return item(intro + "What is the boiling point of the substance?", "%d °C" % bp, ["%s °C" % tc(x) for x in (mp, mp - 20, (mp + bp) // 2)], "The second flat part.")
    return item(intro + "What state is the substance in at 6 minutes?", "liquid", ["solid", "gas", "melting"], "Between the melting and boiling points.")


B1 = bank([
    ("What is the equation for density?", "density = mass ÷ volume", ["density = volume ÷ mass", "density = mass × volume", "density = mass + volume"], "kg/m³ or g/cm³."),
    ("Why are gases much less dense than solids?", "Their particles are much further apart.", ["Their particles are smaller.", "They have no mass.", "Their particles are heavier."], "Particle model."),
    ("What is internal energy?", "the total kinetic and potential energy of all the particles in a system", ["only the temperature of a system", "the energy in the nucleus", "the energy of the container"], "Heating increases it."),
    ("What happens to the mass when ice melts?", "It stays the same.", ["It increases.", "It decreases.", "It becomes zero."], "Changes of state are physical and conserve mass."),
])
B5 = bank([
    ("What is specific latent heat?", "the energy needed to change the state of 1 kg of a substance without changing its temperature", ["the energy to raise 1 kg by 1 °C", "the temperature of melting", "the mass of a substance"], "Fusion and vaporisation."),
    ("Why does steam at 100 °C cause worse burns than water at 100 °C?", "Steam releases its latent heat of vaporisation as it condenses on the skin.", ["Steam is hotter.", "Water does not burn.", "Steam is denser."], "Extra energy."),
    ("Why does a gas exert pressure on its container?", "Its particles collide with the walls.", ["Its particles are still.", "The walls pull the gas.", "Gas has no mass."], "Particle collisions."),
    ("How does heating a gas in a sealed container affect its pressure?", "It increases, because particles move faster and collide more often and harder.", ["It decreases.", "It stays the same.", "The particles grow."], "Constant volume."),
])

if __name__ == "__main__":
  build(U, 10, "particle-model-and-density", 12, "Physics", "Particle model of matter",
      "Density of materials (ρ = m ÷ V) and the particle model; changes of state and conservation of mass; internal energy; temperature changes in a system and specific heat capacity; changes of heat and specific latent heat; particle motion in gases and gas pressure.",
      "Particle Model and Density", "Particle Model and Density",
      "Free Year 10 GCSE Combined Science worksheets on the particle model: density and its measurement, solids, liquids and gases, changes of state, internal energy, specific latent heat and gas pressure. 100 questions with answers.",
      "density = mass ÷ volume",
      "During a change of state the temperature stays the same; E = mL.",
      "<p><b>The particle model explains density, changes of state and gas pressure.</b></p><ul><li>ρ = m ÷ V. Measure an irregular object's volume by displacement of water.</li>"
      "<li>During melting or boiling the temperature stays the same: energy breaks bonds (latent heat). E = mL.</li>"
      "<li>Gas particles collide with container walls; hotter gas means faster particles and higher pressure.</li></ul>",
      [("54 g, 20 cm³. Density?", ["54 ÷ 20"], "2.7 g/cm³"), ("0.5 kg ice melting (L = 334,000 J/kg)?", ["0.5 × 334,000"], "167,000 J")],
      ["Thinking the temperature rises while a solid melts.", "Thinking particles get bigger when heated.", "Writing density = volume ÷ mass."],
      [("How do you find the density of an irregular object?", "Measure its mass on a balance and its volume by the rise in water level in a measuring cylinder, then divide mass by volume."),
       ("What is specific latent heat?", "The energy needed to change the state of 1 kg of a substance without changing its temperature. E = m × L."),
       ("Why does gas pressure rise when a gas is heated?", "The particles move faster, so they collide with the walls more often and with more force.")],
      [("Density", B1 + [(g_rho, 16)]),
       ("States of matter", [(y7_state, 8), (y7_change, 8), (g_rho, 4)]),
       ("Heating curves", [(g_curve, 12), (g_lat, 8)]),
       ("Latent heat", [(g_lat, 10), (g_rho, 6), (g_curve, 4)]),
       ("Gas pressure", B5 + [(y9_gas, 5), (g_rho, 7), (g_lat, 4)])])
