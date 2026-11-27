# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 9: Thermal Properties of Matter
  python tools/gen_sg_science_s3_thermal_properties_of_matter.py
Internal energy; heat capacity (C = Q ÷ Δθ) and specific heat capacity (Q = mcΔθ); melting, boiling and evaporation;
specific latent heat of fusion and vaporisation (Q = mL); why the temperature stays constant during a change of state;
heating and cooling curves; factors that affect evaporation and its cooling effect.
UK specific heat capacity and latent heat makers are reused (Singapore names); heating curves draw their own SVG.
Wrong answers come from real mistakes: "temperature rises while ice melts", "boiling and evaporation are the same",
"specific heat capacity is the energy to heat any mass by 1 °C", "a larger mass heats up faster with the same energy".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, graph, fig, ex

LV, SUBJ, SORT = 3, "Physics", 9
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_shc = src("gen_uk_science_y10_energy", "g_shc")
uk_lat = src("gen_uk_science_y10_particle_model_and_density", "g_lat")
uk_curve = src("gen_uk_science_y10_particle_model_and_density", "g_curve")

SHC = [("water", 4200), ("aluminium", 900), ("copper", 390), ("iron", 450), ("cooking oil", 2000), ("glass", 840), ("concrete", 880)]


def g_q():
    m_, c = R.choice(SHC)
    k = R.choice(["Q", "Q", "c", "dT", "m"])
    m = R.choice([0.1, 0.2, 0.25, 0.5, 1, 2, 4, 5])
    dT = R.choice([2, 5, 10, 15, 20, 25, 40, 50, 60])
    Q = m * c * dT
    if k == "Q":
        return nq("How much energy is needed to raise the temperature of %s kg of %s by %d °C? (specific heat capacity of %s = %d J/(kg °C))" % (N(m), m_, dT, m_, c), Q,
                  [c * dT, m * c, m * c * (dT + 273)], " J", "Q = mcΔθ = %s × %d × %d = %s J." % (N(m), c, dT, N(Q)))
    if k == "c":
        return nq("%s J raises the temperature of %s kg of a substance by %d °C. What is its specific heat capacity?" % (N(Q), N(m), dT), c, [Q / dT, Q / m, Q * m / dT], " J/(kg °C)",
                  "c = Q ÷ (mΔθ) = %s ÷ (%s × %d) = %d J/(kg °C)." % (N(Q), N(m), dT, c))
    if k == "dT":
        return nq("%s J of energy is supplied to %s kg of %s (c = %d J/(kg °C)). What is the rise in temperature?" % (N(Q), N(m), m_, c), dT, [Q / c, Q / m, Q / (m * c * 10)], " °C",
                  "Δθ = Q ÷ (mc) = %s ÷ (%s × %d) = %d °C." % (N(Q), N(m), c, dT))
    return nq("%s J raises the temperature of a sample of %s (c = %d J/(kg °C)) by %d °C. What is the mass of the sample?" % (N(Q), m_, c, dT), m, [Q / c, Q / dT, Q * c * dT], " kg",
              "m = Q ÷ (cΔθ) = %s ÷ (%d × %d) = %s kg." % (N(Q), c, dT, N(m)))


def g_cap():
    C = R.choice([50, 80, 200, 420, 450, 900, 1200, 2100, 4200])
    dT = R.choice([2, 5, 10, 20, 25])
    Q = C * dT
    if R.random() < 0.5:
        return nq("A metal block absorbs %s J and its temperature rises by %d °C. What is its heat capacity?" % (N(Q), dT), C, [Q * dT, dT / Q, Q / dT / 1000], " J/°C",
                  "C = Q ÷ Δθ = %s ÷ %d = %d J/°C." % (N(Q), dT, C))
    return nq("An object has a heat capacity of %d J/°C. How much energy raises its temperature by %d °C?" % (C, dT), Q, [C / dT, C + dT, C * dT * 10], " J", "Q = CΔθ = %d × %d = %s J." % (C, dT, N(Q)))


LAT = [("ice", "fusion", 334000, "melt"), ("water", "vaporisation", 2260000, "boil away (vaporise)"), ("paraffin wax", "fusion", 200000, "melt"), ("ethanol", "vaporisation", 840000, "vaporise")]


def g_lat():
    m_, kind, L, verb = R.choice(LAT)
    m = R.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 2])
    Q = m * L
    k = R.choice(["Q", "Q", "m", "L"])
    if k == "Q":
        return nq("How much energy is needed to %s %s kg of %s at its %s point? (specific latent heat of %s = %s J/kg)" % (verb, N(m), m_, "melting" if kind == "fusion" else "boiling", kind, N(L)),
                  Q, [L / m, L, Q / 1000], " J", "Q = mL = %s × %s = %s J." % (N(m), N(L), N(Q)))
    if k == "m":
        return nq("%s J of energy is supplied to %s at its %s point. What mass changes state? (specific latent heat of %s = %s J/kg)" % (N(Q), m_, "melting" if kind == "fusion" else "boiling", kind, N(L)),
                  m, [Q * L, L / Q, m * 10], " kg", "m = Q ÷ L = %s ÷ %s = %s kg." % (N(Q), N(L), N(m)))
    return nq("%s J is needed to %s %s kg of %s without any change in temperature. What is the specific latent heat of %s?" % (N(Q), verb, N(m), m_, kind),
              L, [Q * m, m / Q, Q], " J/kg", "L = Q ÷ m = %s ÷ %s = %s J/kg." % (N(Q), N(m), N(L)))


def g_curve():
    """heating curve: solid warms, melts, liquid warms, boils"""
    mp = R.choice([20, 30, 40, 50, 60, 80])
    bp = mp + R.choice([40, 50, 60, 80])
    t0 = R.choice([0, 10]) if mp > 20 else 0
    a, b, c = R.choice([2, 3, 4]), R.choice([4, 5, 6]), R.choice([3, 4, 5])
    d = R.choice([4, 6])
    pts = [(0, t0), (a, mp), (a + b, mp), (a + b + c, bp), (a + b + c + d, bp)]
    T = a + b + c + d
    ys = 20
    svg = graph(pts, ((T + 1) // 2) * 2, ((bp + 20) // ys) * ys + ys, 2, ys, "time / min", "temperature / °C", label="heating curve",
                marks=[(a / 2, "P"), (a + b / 2, "Q"), (a + b + c / 2, "R"), (a + b + c + d / 2, "S")])
    k = R.choice(["mp", "bp", "Q", "S", "state", "energy"])
    q = fig(svg) + "A solid is heated at a steady rate. The graph shows its temperature. "
    if k == "mp":
        return nq(q + "What is the melting point of the substance?", mp, [bp, t0, (mp + bp) // 2], " °C", "The first flat part (Q) is melting, at %d °C." % mp)
    if k == "bp":
        return nq(q + "What is the boiling point of the substance?", bp, [mp, bp - 20, (mp + bp) // 2], " °C", "The second flat part (S) is boiling, at %d °C." % bp)
    if k == "Q":
        return tq(q + "What is happening in part Q?", "The solid is melting.", ["The liquid is boiling.", "The solid is warming up.", "The liquid is cooling."], "Temperature stays constant during a change of state.")
    if k == "S":
        return tq(q + "What is happening in part S?", "The liquid is boiling.", ["The solid is melting.", "The gas is cooling.", "The liquid is freezing."], "The second flat part is boiling.")
    if k == "state":
        return tq(q + "In which state is the substance during part R?", "liquid", ["solid", "gas", "a mixture of solid and liquid"], "After melting and before boiling, it is a liquid.")
    return tq(q + "Why does the temperature stay constant in part Q although heating continues?", "The energy is used to break the bonds (forces) between particles, not to increase their kinetic energy.",
              ["The thermometer stops working.", "No energy is supplied during melting.", "The particles stop moving."], "Latent heat changes the potential energy of the particles.")


EVAP = [("raising the temperature of the liquid", "increases"), ("increasing the exposed surface area", "increases"), ("blowing air (wind) over the surface", "increases"),
        ("increasing the humidity of the air", "decreases"), ("lowering the temperature of the liquid", "decreases"), ("covering the container", "decreases")]


def g_evap():
    q, a = R.choice(EVAP)
    return tq("What is the effect of %s on the rate of evaporation?" % q, "It %s the rate." % a, ["It %s the rate." % ("decreases" if a == "increases" else "increases"), "It has no effect.", "It stops evaporation completely."],
              "Evaporation is faster at higher temperature, larger surface area, with moving air and in drier (less humid) air.")


POOL1 = pool(R, [
    ("What is internal energy?", "the total kinetic and potential energy of all the particles in a body", ["the temperature of a body", "the kinetic energy of the body moving", "the energy stored in its chemical bonds only"], "Heating raises internal energy."),
    ("What is specific heat capacity?", "the energy needed to raise the temperature of 1 kg of a substance by 1 °C (or 1 K)", ["the energy needed to melt 1 kg of a substance", "the energy needed to raise the temperature of any object by 1 °C", "the temperature of 1 kg of a substance"], "Unit: J/(kg °C)."),
    ("What is heat capacity?", "the energy needed to raise the temperature of a body by 1 °C (or 1 K)", ["the energy needed to raise 1 kg by 1 °C", "the energy needed to melt a body", "the most heat a body can hold"], "Unit: J/°C."),
    ("What is the specific latent heat of fusion?", "the energy needed to change 1 kg of a solid into liquid without a change in temperature", ["the energy needed to raise 1 kg by 1 °C", "the energy given out when 1 kg boils", "the temperature at which a solid melts"], "Unit: J/kg."),
    ("What is the specific latent heat of vaporisation?", "the energy needed to change 1 kg of a liquid into gas without a change in temperature", ["the energy needed to melt 1 kg of a solid", "the energy needed to raise 1 kg of gas by 1 °C", "the boiling point of a liquid"], "Unit: J/kg."),
    ("Why does the temperature stay constant while a substance boils?", "The energy supplied is used to overcome the forces between particles, not to raise their kinetic energy.", ["No energy is absorbed.", "The thermometer cannot measure higher temperatures.", "Bubbles cool the liquid."], "This is latent heat."),
    ("How is boiling different from evaporation?", "Boiling happens throughout the liquid at a fixed temperature; evaporation happens only at the surface at any temperature.",
     ["They are the same process.", "Evaporation needs a fixed temperature.", "Boiling happens only at the surface."], "Bubbles of vapour form inside a boiling liquid."),
    ("Why does evaporation cause cooling?", "The most energetic particles escape, so the average kinetic energy of the particles left behind falls.", ["The liquid gains particles.", "Evaporation releases heat.", "The surface becomes darker."], "This is why sweating cools you."),
    ("Why is water good for cooling car engines?", "It has a high specific heat capacity, so it absorbs a lot of energy for a small temperature rise.", ["It has a low specific heat capacity.", "It boils easily.", "It is a good conductor of electricity."], "c of water = 4200 J/(kg °C)."),
    ("Why does a sandy beach get hotter than the sea on a sunny day?", "Sand has a much lower specific heat capacity than water.", ["Sand absorbs less sunlight.", "Water is darker.", "The sea receives less sunlight."], "Same energy, bigger temperature rise for sand."),
])
POOL5 = pool(R, [
    ("Why does a steam burn at 100 °C hurt more than a burn from boiling water at 100 °C?", "Steam gives out its latent heat of vaporisation as it condenses on the skin, as well as heat from cooling.",
     ["Steam is hotter than 100 °C.", "Water has no energy to give.", "Steam moves faster."], "Condensation releases a lot of energy."),
    ("Why do you feel cold when you come out of a swimming pool on a windy day?", "Water evaporates quickly from your skin and takes thermal energy from your body.", ["The water is colder than the air.", "Wind adds cold to your skin.", "Your body stops making heat."], "Wind speeds up evaporation."),
    ("Why do clothes dry faster on a hot, windy day than on a humid day?", "Higher temperature and moving air increase evaporation, while humid air slows it.", ["Humid air is hotter.", "Wind adds water to the clothes.", "Clothes absorb sunlight only on humid days."], "Singapore's high humidity slows drying."),
    ("1.0 kg of water and 1.0 kg of cooking oil get the same energy. Which has the larger temperature rise?", "the cooking oil", ["the water", "both the same", "neither changes"], "Oil has a lower specific heat capacity (about 2000 J/(kg °C))."),
    ("A 2 kg block and a 1 kg block of the same metal get the same energy. How do their temperature rises compare?", "The 1 kg block's rise is twice as large.", ["They are the same.", "The 2 kg block's rise is twice as large.", "The 2 kg block's rise is four times as large."], "Δθ = Q ÷ mc."),
    ("Ice at 0 °C is put in a drink. Why does it cool the drink more than the same mass of water at 0 °C?", "The ice absorbs latent heat of fusion from the drink as it melts.", ["Ice is colder than 0 °C.", "Water at 0 °C has no energy.", "Ice reflects heat."], "Melting needs energy."),
    ("A pure substance cools from liquid to solid. What does its cooling curve show at the freezing point?", "a flat part, where the temperature stays constant", ["a steady fall in temperature", "a sudden rise to boiling point", "a gap in the graph"], "Latent heat is given out during freezing."),
    ("An electric heater of 50 W heats a 1 kg aluminium block for 180 s. Its temperature rises by 10 °C. What is the specific heat capacity of aluminium found by this experiment?", "900 J/(kg °C)", ["9000 J/(kg °C)", "90 J/(kg °C)", "50 J/(kg °C)"], "Q = Pt = 9000 J; c = 9000 ÷ (1 × 10) = 900 J/(kg °C)."),
    ("Why is the measured specific heat capacity in a school experiment often larger than the true value?", "Some energy is lost to the surroundings, so more energy seems to be needed.", ["The thermometer is too accurate.", "The heater gives out extra energy.", "The block gains mass."], "Insulate the block to reduce losses."),
    ("Why does sweating help to keep you cool in Singapore's hot weather?", "Sweat evaporates and the energetic particles carry thermal energy away from the skin.", ["Sweat is cold.", "Sweat reflects sunlight.", "Sweat stops convection."], "In very humid air sweat evaporates more slowly, so you feel hotter."),
])


def main():
    sets = U.sets([
        ("Internal energy and heat capacity", [POOL1, (g_cap, 6), (g_q, 6)]),
        ("Specific heat capacity", [(g_q, 10), (uk_shc, 6), POOL1]),
        ("Latent heat", [(g_lat, 10), (uk_lat, 5), POOL1]),
        ("Melting, boiling and evaporation", [(g_curve, 8), (g_evap, 5), (uk_curve, 3), POOL1]),
        ("Exam-style questions", [(POOL5, 10), (g_curve, 4), (g_lat, 3), (g_q, 3)]),
    ])
    make_ol(LV, SUBJ, "thermal-properties-of-matter", SORT, "Thermal Properties of Matter",
            "Describe a rise in temperature of an object in terms of an increase in its internal energy; define heat capacity and specific heat capacity and apply "
            "Q = mcΔθ; describe melting, boiling and evaporation in terms of the kinetic particle model and explain why the temperature stays constant during a change of "
            "state; define specific latent heat of fusion and vaporisation and apply Q = mL; distinguish between boiling and evaporation and describe the factors that "
            "affect evaporation and its cooling effect (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Thermal Properties of Matter", "Thermal properties",
            "Free Secondary 3 O-Level Physics worksheets on thermal properties of matter: internal energy, heat capacity, specific heat capacity, latent heat, heating curves, "
            "boiling and evaporation. 100 questions with answers.",
            "Q = mcΔθ and Q = mL", "Temperature stays constant during a change of state.",
            "<p><b>Heating raises the internal energy of a body.</b></p><ul>"
            "<li>Q = mcΔθ: c is the specific heat capacity, in J/(kg °C). Heat capacity C = Q ÷ Δθ, in J/°C.</li>"
            "<li>Q = mL during a change of state: L is the specific latent heat of fusion (melting) or vaporisation (boiling), in J/kg.</li>"
            "<li>While a substance melts or boils, the energy breaks forces between particles, so the temperature stays constant (flat parts of a heating curve).</li>"
            "<li>Evaporation happens at the surface at any temperature and cools the liquid; it is faster when hotter, with more surface, with wind and in dry air.</li></ul>",
            [("Energy to heat 2 kg of water by 15 °C? (c = 4200)", ["Q = 2 × 4200 × 15"], "126 000 J"),
             ("Energy to melt 0.5 kg of ice? (L = 334 000 J/kg)", ["Q = 0.5 × 334 000"], "167 000 J")],
            ["Thinking the temperature rises while ice melts. It stays at 0 °C until all the ice has melted.", "Mixing up heat capacity (whole object, J/°C) and specific heat capacity (per kg, J/(kg °C)).",
             "Using Q = mcΔθ during a change of state. Use Q = mL there.", "Calling boiling and evaporation the same."],
            [("What is the difference between heat capacity and specific heat capacity?", "Heat capacity is the energy to raise a whole object by 1 °C (J/°C). Specific heat capacity is the energy to raise 1 kg of the substance by 1 °C (J/(kg °C))."),
             ("Why are there flat parts on a heating curve?", "During melting and boiling, the energy supplied overcomes the forces between particles (latent heat), so the temperature does not rise."),
             ("What affects the rate of evaporation?", "Temperature, surface area, air movement (wind) and humidity. Hotter, larger, windier and drier all make evaporation faster.")],
            sets)


if __name__ == "__main__":
    main()
