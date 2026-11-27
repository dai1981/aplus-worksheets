# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 5: Pressure
  python tools/gen_sg_science_s3_pressure.py
Density = mass ÷ volume, pressure = force ÷ area, hydraulic systems (the same pressure is transmitted through the liquid),
pressure in a liquid p = hρg (g = 10 N/kg), atmospheric pressure (mercury barometer) and the manometer.
UK and SG density and pressure makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "pressure = force × area", "using cm² with N/m²", "pressure in a liquid depends on the
shape of the container", "a hydraulic press multiplies the pressure".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Physics", 5
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_p = src("gen_uk_science_y9_pressure", "g_calc")
uk_rho = src("gen_uk_science_y10_particle_model_and_density", "g_rho")
uk_dens = src("gen_uk_science_y7_particles_and_states_of_matter", "g_dens")
sg_float = src("gen_sg_science_s1_physical_properties_of_matter", "g_float")

MAT = [("aluminium", 2700), ("iron", 7900), ("copper", 8900), ("lead", 11300), ("gold", 19300), ("glass", 2500), ("ice", 920), ("cork", 240),
       ("concrete", 2400), ("seawater", 1030), ("cooking oil", 920), ("mercury", 13600)]


def g_dens():
    m_, rho = R.choice(MAT)
    k = R.choice(["rho", "m", "V"])
    V = R.choice([0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 2])
    m = rho * V
    if k == "rho":
        return nq("A block of %s has a mass of %s kg and a volume of %s m³. What is its density?" % (m_, N(m), N(V)), rho, [m * V, V / m, m / V / 1000], " kg/m³",
                  "ρ = m ÷ V = %s ÷ %s = %s kg/m³." % (N(m), N(V), N(rho)))
    if k == "m":
        return nq("%s has a density of %s kg/m³. What is the mass of %s m³ of it?" % (m_[0].upper() + m_[1:], N(rho), N(V)), m, [rho / V, V / rho, m * 10], " kg",
                  "m = ρV = %s × %s = %s kg." % (N(rho), N(V), N(m)))
    return nq("A piece of %s has a mass of %s kg. Its density is %s kg/m³. What is its volume?" % (m_, N(m), N(rho)), V, [m * rho, rho / m, V * 10], " m³",
              "V = m ÷ ρ = %s ÷ %s = %s m³." % (N(m), N(rho), N(V)))


def g_pfa():
    k = R.choice(["p", "p", "F", "A", "cm"])
    F = R.choice([20, 50, 60, 120, 200, 400, 500, 600, 800, 1200, 3000])
    A = R.choice([0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.5, 2])
    p = F / A
    if k == "p":
        return nq("A force of %d N acts on an area of %s m². What is the pressure?" % (F, N(A)), p, [F * A, A / F, F / A / 100], " Pa", "p = F ÷ A = %d ÷ %s = %s Pa." % (F, N(A), N(p)))
    if k == "F":
        return nq("A pressure of %s Pa acts on an area of %s m². What force does it exert?" % (N(p), N(A)), F, [p / A, A / p, p], " N", "F = pA = %s × %s = %d N." % (N(p), N(A), F))
    if k == "A":
        return nq("A force of %d N gives a pressure of %s Pa. What is the area?" % (F, N(p)), A, [F * p, p / F, F / p * 100], " m²", "A = F ÷ p = %d ÷ %s = %s m²." % (F, N(p), N(A)))
    m = R.choice([40, 50, 55, 60, 70])
    a = R.choice([150, 200, 250, 300, 400])
    return nq("A student of mass %d kg stands on both feet. Each shoe has %d cm² in contact with the floor. What is the pressure on the floor? (g = 10 N/kg)" % (m, a),
              m * 10 / (2 * a / 1e4), [m * 10 / (a / 1e4), m * 10 / (2 * a), m / (2 * a / 1e4)], " Pa",
              "Weight = %d N. Area = 2 × %d cm² = %d cm² = %s m². p = %d ÷ %s = %s Pa." % (m * 10, a, 2 * a, N(2 * a / 1e4), m * 10, N(2 * a / 1e4), N(m * 10 / (2 * a / 1e4))))


LIQ = [("water", 1000), ("seawater", 1030), ("mercury", 13600), ("oil", 800), ("paraffin", 800)]


def g_hrg():
    name, rho = R.choice(LIQ)
    k = R.choice(["p", "p", "h", "tot"])
    h = R.choice([0.05, 0.1, 0.2, 0.5, 0.76, 1.5, 2, 5, 10, 20, 50]) if name != "mercury" else R.choice([0.01, 0.05, 0.1, 0.2, 0.76])
    p = h * rho * 10
    if k == "p":
        return nq("What is the pressure due to %s at a depth of %s m? (density %d kg/m³, g = 10 N/kg)" % (name, N(h), rho), p, [h * rho, h * 10, rho * 10 / h], " Pa",
                  "p = hρg = %s × %d × 10 = %s Pa." % (N(h), rho, N(p)))
    if k == "h":
        return nq("At what depth in %s is the pressure due to the liquid %s Pa? (density %d kg/m³, g = 10 N/kg)" % (name, N(p), rho), h, [p / rho, p * rho * 10, p / 10], " m",
                  "h = p ÷ ρg = %s ÷ (%d × 10) = %s m." % (N(p), rho, N(h)))
    if name not in ("water", "seawater"):
        return None
    pt = p + 100000
    return nq("A diver is %s m below the surface of %s (density %d kg/m³). Atmospheric pressure is 100 000 Pa. What is the total pressure on the diver? (g = 10 N/kg)" % (N(h), name, rho),
              pt, [p, 100000 - p, 100000 + h * rho], " Pa", "Total = atmospheric + hρg = 100 000 + %s = %s Pa." % (N(p), N(pt)))


def g_hyd():
    a1 = R.choice([0.001, 0.002, 0.005, 0.01])
    ratio = R.choice([5, 10, 20, 25, 40, 50])
    a2 = a1 * ratio
    F1 = R.choice([10, 20, 25, 40, 50, 100, 150])
    F2 = F1 * ratio
    k = R.choice(["F2", "F1", "p"])
    if k == "F2":
        return nq("In a hydraulic jack, a force of %d N acts on a small piston of area %s m². The large piston has an area of %s m². What force acts on the large piston?" % (F1, N(a1), N(a2)),
                  F2, [F1, F1 / ratio, F1 * a2], " N", "Pressure is the same: F₂ = F₁ × A₂ ÷ A₁ = %d × %d = %s N." % (F1, ratio, N(F2)))
    if k == "F1":
        return nq("A hydraulic lift raises a load of %s N on a piston of area %s m². The small piston has an area of %s m². What force is needed on the small piston?" % (N(F2), N(a2), N(a1)),
                  F1, [F2 * ratio, F2, F2 * a1], " N", "F₁ = F₂ × A₁ ÷ A₂ = %s ÷ %d = %d N." % (N(F2), ratio, F1))
    return nq("A force of %d N on a piston of area %s m² presses on oil in a hydraulic system. What is the pressure in the oil?" % (F1, N(a1)), F1 / a1, [F1 * a1, a1 / F1, F1 / a1 / 1000], " Pa",
              "p = F ÷ A = %d ÷ %s = %s Pa. The same pressure acts everywhere in the oil." % (F1, N(a1), N(F1 / a1)))


def g_mano():
    liq, rho = R.choice([("water", 1000), ("mercury", 13600), ("oil", 800)])
    hc = R.choice([2, 4, 5, 8, 10, 12, 15, 20, 25, 30])
    h = hc / 100
    dp = h * rho * 10
    k = R.choice(["dp", "gas"])
    if k == "dp":
        return nq("A %s manometer is connected to a gas supply. The %s level is %d cm higher in the open arm. What is the gas pressure above atmospheric pressure? (density %d kg/m³, g = 10 N/kg)" % (liq, liq, hc, rho),
                  dp, [hc * rho * 10, h * rho, dp * 2], " Pa", "Δp = hρg = %s × %d × 10 = %s Pa (use h in metres)." % (N(h), rho, N(dp)))
    return nq("A %s manometer shows a difference in levels of %d cm, higher in the open arm. Atmospheric pressure is 100 000 Pa. What is the gas pressure? (density %d kg/m³, g = 10 N/kg)" % (liq, hc, rho),
              100000 + dp, [100000 - dp, dp, 100000 + hc * rho * 10], " Pa", "Gas pressure = 100 000 + %s = %s Pa." % (N(dp), N(100000 + dp)))


POOL1 = pool(R, [
    ("What is pressure?", "force per unit area", ["force × area", "mass per unit volume", "force per unit mass"], "p = F ÷ A, in pascals (Pa)."),
    ("What is 1 pascal?", "1 N/m²", ["1 N m", "1 kg/m³", "1 N/cm²"], "The SI unit of pressure."),
    ("Why does a knife cut better when it is sharp?", "The force acts on a smaller area, so the pressure is larger.", ["The force is larger.", "The area is larger.", "The knife is heavier."], "p = F ÷ A."),
    ("Why do tractors have wide tyres?", "to spread the weight over a large area and reduce the pressure on soft ground", ["to increase the pressure", "to go faster", "to make the tractor lighter"], "Larger area, smaller pressure."),
    ("What is density?", "mass per unit volume", ["weight per unit area", "volume per unit mass", "mass × volume"], "ρ = m ÷ V."),
    ("What is the SI unit of density?", "kg/m³", ["g/m³", "kg/m²", "N/m³"], "g/cm³ is also used: 1 g/cm³ = 1000 kg/m³."),
    ("Convert a density of 2.7 g/cm³ into kg/m³.", "2700 kg/m³", ["2.7 kg/m³", "270 kg/m³", "27 000 kg/m³"], "Multiply by 1000."),
    ("Ice (density 920 kg/m³) is put in water (1000 kg/m³). What happens?", "It floats.", ["It sinks.", "It dissolves straight away.", "It stays at the bottom."], "Less dense than water, so it floats."),
    ("On which factors does the pressure in a liquid depend?", "the depth, the density of the liquid and g", ["the shape and width of the container", "the area of the base only", "the volume of liquid only"], "p = hρg."),
    ("Why is the wall of a dam thicker at the bottom?", "Water pressure increases with depth.", ["The water is colder at the bottom.", "The bottom has less water.", "It looks stronger."], "The force on the lower wall is larger."),
])
POOL5 = pool(R, [
    ("Why does a hydraulic jack let a small force lift a heavy car?", "The pressure is the same throughout the liquid, so a larger piston area gives a larger force.", ["The liquid makes the pressure larger.", "The liquid is compressed.", "The car becomes lighter."], "F₂ = p × A₂."),
    ("Why must a hydraulic system contain no air bubbles?", "Air can be compressed, so the pressure would not be passed on fully.", ["Air makes the liquid heavier.", "Air increases the pressure.", "Bubbles cool the liquid."], "Liquids are almost incompressible."),
    ("A mercury barometer reads 760 mm. What does this show?", "Atmospheric pressure supports a 760 mm column of mercury.", ["The tube is 760 mm long.", "The air is 760 mm deep.", "The mercury has a mass of 760 g."], "Standard atmospheric pressure."),
    ("Why is mercury used in barometers instead of water?", "It is very dense, so the column is short (about 0.76 m instead of about 10 m).", ["It is cheaper.", "It is transparent.", "It evaporates quickly."], "Water would need a column about 10 m tall."),
    ("What happens to atmospheric pressure as you go up a mountain?", "It decreases.", ["It increases.", "It stays the same.", "It doubles."], "There is less air above you."),
    ("How does a drinking straw work?", "Sucking lowers the pressure inside the straw, and atmospheric pressure pushes the drink up.", ["The mouth pulls the drink.", "Gravity pushes the drink up.", "The drink expands."], "Pressure difference."),
    ("Three containers of different shapes are filled with water to the same depth. How does the pressure at the bottom compare?", "It is the same in all three.", ["It is largest in the widest one.", "It is largest in the narrowest one.", "It depends on the volume."], "p = hρg does not depend on shape."),
    ("A gas supply is connected to a manometer. Why is the liquid lower in the arm connected to the gas?", "The gas pressure is greater than atmospheric pressure.", ["The gas pressure is less than atmospheric pressure.", "The liquid is heavier in that arm.", "The gas has no pressure."], "The larger pressure pushes the liquid down."),
    ("At 10 m below the sea surface, the water pressure is about 100 000 Pa. What is the total pressure on a diver there?", "about 200 000 Pa", ["about 100 000 Pa", "about 10 000 Pa", "about 1 000 000 Pa"], "Add atmospheric pressure (about 100 000 Pa)."),
    ("A block has a mass of 600 g and measures 10 cm × 5 cm × 4 cm. Will it float in water (1.0 g/cm³)?", "No: its density is 3.0 g/cm³, so it sinks.",
     ["Yes: its density is 0.3 g/cm³.", "Yes: it has a large volume.", "No: its density is 30 g/cm³."], "Volume = 200 cm³; ρ = 600 ÷ 200 = 3.0 g/cm³."),
])


def main():
    sets = U.sets([
        ("Density", [(g_dens, 9), (uk_rho, 5), (sg_float, 4), POOL1]),
        ("Pressure = force ÷ area", [(g_pfa, 10), (uk_p, 6), POOL1]),
        ("Pressure in liquids", [(g_hrg, 12), POOL1, (POOL5, 3)]),
        ("Hydraulics, the atmosphere and manometers", [(g_hyd, 8), (g_mano, 7), (POOL5, 5)]),
        ("Exam-style questions", [(POOL5, 8), (g_hrg, 4), (g_hyd, 3), (g_pfa, 3), (g_mano, 2)]),
    ])
    make_ol(LV, SUBJ, "pressure", SORT, "Pressure",
            "Recall and apply density = mass ÷ volume; define pressure as force per unit area and apply p = F ÷ A; describe how pressure is transmitted in hydraulic "
            "systems such as a hydraulic press; recall and apply the relationship pressure due to a liquid column = height × density × g; describe how the height of a "
            "liquid column may be used to measure atmospheric pressure and how a manometer measures pressure differences (summary of the Singapore-Cambridge O-Level "
            "Physics 6091 syllabus).",
            "Pressure", "Pressure",
            "Free Secondary 3 O-Level Physics worksheets on density and pressure: p = F/A, hydraulic jacks, pressure in liquids (p = hρg), atmospheric pressure, barometers and "
            "manometers. 100 questions with answers.",
            "Pressure = force ÷ area", "In a liquid, p = hρg (g = 10 N/kg).",
            "<p><b>Pressure is force per unit area.</b></p><ul>"
            "<li>p = F ÷ A in pascals (1 Pa = 1 N/m²). Change cm² into m² (1 m² = 10 000 cm²).</li>"
            "<li>Density ρ = m ÷ V (kg/m³). An object floats in a liquid that is denser than it.</li>"
            "<li>Pressure in a liquid p = hρg depends on depth and density, not on the shape of the container. Total pressure = atmospheric + hρg.</li>"
            "<li>A hydraulic system passes the same pressure through the liquid: F₁ ÷ A₁ = F₂ ÷ A₂.</li></ul>",
            [("Pressure of water at 4 m depth? (ρ = 1000 kg/m³)", ["p = 4 × 1000 × 10"], "40 000 Pa"),
             ("A 600 N weight stands on 0.03 m². Pressure?", ["p = 600 ÷ 0.03"], "20 000 Pa")],
            ["Multiplying force by area. Pressure = force ÷ area.", "Using an area in cm² with an answer in Pa. Change it into m² first.",
             "Thinking a wider container gives more pressure at the same depth.", "Thinking a hydraulic system increases the pressure. It keeps the pressure the same and increases the force."],
            [("What is the formula for pressure in a liquid?", "p = hρg: depth (m) × density (kg/m³) × gravitational field strength (10 N/kg). The answer is in pascals."),
             ("How does a hydraulic jack work?", "A small force on a small piston makes a pressure that is passed through the liquid. The same pressure on a larger piston gives a larger force."),
             ("How is atmospheric pressure measured?", "With a mercury barometer: atmospheric pressure holds up a column of mercury about 760 mm tall.")],
            sets)


if __name__ == "__main__":
    main()
