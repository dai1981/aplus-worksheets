# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Chemistry): Particles and States of Matter
  python tools/gen_uk_science_y7_particles_and_states_of_matter.py
The particulate nature of matter: properties of solids, liquids and gases explained by the arrangement and movement of
particles; changes of state (melting, freezing, boiling, evaporating, condensing, sublimating) and melting and boiling
points; diffusion and Brownian motion; density; conservation of mass in changes of state.
Wrong answers come from real mistakes: "particles in a solid do not move", "particles expand when heated",
"mass is lost when ice melts", "boiling and evaporating are exactly the same".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61706)
R = U.R
P = People(R)

PROP = [("has a fixed shape and a fixed volume", "solid"), ("flows and takes the shape of its container but keeps a fixed volume", "liquid"),
        ("spreads out to fill any container", "gas"), ("can easily be squashed (compressed)", "gas"), ("has particles in a regular pattern that vibrate on the spot", "solid"),
        ("has particles close together that slide past each other", "liquid"), ("has particles far apart that move quickly in all directions", "gas"),
        ("cannot be poured and keeps its shape", "solid"), ("has the weakest forces between its particles", "gas"), ("has the strongest forces between its particles", "solid")]


def g_state():
    d, s = R.choice(PROP)
    if not once(("st", d)):
        return None
    return item("Which state of matter %s?" % d, "a " + s, ["a " + x for x in ["solid", "liquid", "gas"] if x != s] + ["a mixture"], "Use the particle model: arrangement, movement and forces.")


CHG = [("melting", "solid", "liquid"), ("freezing", "liquid", "solid"), ("boiling", "liquid", "gas"), ("evaporating", "liquid", "gas"), ("condensing", "gas", "liquid"),
       ("sublimating", "solid", "gas")]


def g_change():
    n, a, b = R.choice(CHG)
    k = R.random() < 0.5
    if not once(("ch", n, k)):
        return None
    if k:
        return item("What happens to a substance when it is %s?" % n, "It changes from a %s to a %s." % (a, b),
                    ["It changes from a %s to a %s." % (x[1], x[2]) for x in R.sample([x for x in CHG if (x[1], x[2]) != (a, b)], 3)], "Changes of state are physical changes.")
    if n == "evaporating":
        return None
    return item("What is the name for a change from a %s to a %s%s?" % (a, b, " at its boiling point" if n == "boiling" else ""), n,
                R.sample([x[0] for x in CHG if x[0] != n and not (n == "boiling" and x[0] == "evaporating")], 3), "Melting, freezing, boiling, condensing and sublimating.")


SUB = [("water", 0, 100), ("ethanol", -114, 78), ("oxygen", -218, -183), ("iron", 1538, 2862), ("mercury", -39, 357), ("sodium chloride (salt)", 801, 1413), ("nitrogen", -210, -196)]


def fmt(t):
    return ("−%s" % "{:,}".format(-t)) if t < 0 else "{:,}".format(t)


def g_mp():
    nm, mp, bp = R.choice(SUB)
    t = R.choice([mp - R.choice([10, 20, 50]), (mp + bp) // 2, bp + R.choice([10, 20, 50])])
    if t in (mp, bp):
        return None
    st = "solid" if t < mp else "liquid" if t < bp else "gas"
    if not once(("mp", nm, st)):
        return None
    tab = table(["Substance", "Melting point (°C)", "Boiling point (°C)"], [[nm, fmt(mp), fmt(bp)]])
    return item(tab + "What state is %s at %s °C?" % (nm, fmt(t)), st, [x for x in ["solid", "liquid", "gas"] if x != st] + ["a mixture of all three"],
                "Below the melting point: solid. Between melting and boiling point: liquid. Above the boiling point: gas.")


def D(x):
    t = ("{:,.2f}".format(x)).rstrip("0").rstrip(".")
    return t + " g/cm³"


def g_dens():
    m = R.choice([20, 40, 60, 80, 100, 120, 150, 200, 270, 390])
    v = R.choice([10, 20, 25, 40, 50, 100])
    if m % v and (m * 10) % v:
        return None
    d = m / v
    if not once(("de", m, v)):
        return None
    g = D(d)
    return item("A block has a mass of %d g and a volume of %d cm³. What is its density?" % (m, v), g, uniq(g, [D(v / m), D(m * v), D(m + v), D(d * 10)]),
                "Density = mass ÷ volume = %d ÷ %d = %s." % (m, v, g))


def g_mass():
    m = R.choice([25, 40, 50, 75, 100, 120, 150, 200, 250])
    what = R.choice([("an ice cube", "melts", "water"), ("some water", "freezes", "ice"), ("some chocolate", "melts", "liquid chocolate"), ("some candle wax", "melts", "liquid wax")])
    if not once(("ma", m, what[0])):
        return None
    g = "%d g" % m
    return item("%s with a mass of %d g %s completely in a sealed container. What is the mass of the %s?" % (what[0][0].upper() + what[0][1:], m, what[1], what[2]), g,
                uniq(g, ["%d g" % (m - 10), "%d g" % (m + 10), "0 g", "%d g" % (m * 2)]), "Mass is conserved in a change of state: no particles are added or lost.")


B1 = bank([
    ("What is matter made of?", "tiny particles", ["only air", "only water", "light"], "The particle model."),
    ("What happens to particles when a solid is heated?", "They vibrate faster.", ["They get bigger.", "They stop moving.", "They melt individually."], "Particles do not expand."),
    ("Why do gases spread out?", "Their particles move quickly in all directions.", ["Their particles are bigger.", "Gases are heavy.", "Gas particles do not move."], "Random movement."),
    ("What is diffusion?", "the spreading of particles from high to low concentration", ["particles joining together", "a solid turning into a liquid", "a gas turning into a liquid"], "Smells spreading."),
    ("Why does diffusion happen faster in a gas than in a liquid?", "Gas particles move faster and are further apart.", ["Gas particles are bigger.", "Liquids have no particles.", "Gas particles do not move."], "Speed and space."),
    ("What is Brownian motion?", "the random jiggling of tiny specks caused by being hit by moving particles", ["the melting of ice", "light travelling in straight lines", "a planet's orbit"], "Evidence for particles."),
    ("What is the melting point of pure water?", "0 °C", ["100 °C", "−10 °C", "37 °C"], "Ice melts at 0 °C."),
    ("What is the boiling point of pure water at sea level?", "100 °C", ["0 °C", "50 °C", "200 °C"], "Water boils at 100 °C."),
])
B5 = bank([
    ("Why can you smell perfume across a room?", "Perfume particles diffuse through the air.", ["The air pushes them in a line.", "Perfume particles are huge.", "Light carries them."], "Diffusion."),
    ("Why is ice less dense than liquid water?", "Its particles are held in an open pattern with more space between them.", ["Ice has no particles.", "Ice is a gas.", "Ice particles are bigger."], "Water is unusual."),
    ("How is evaporation different from boiling?", "Evaporation happens only at the surface and at any temperature; boiling happens throughout the liquid at the boiling point.", ["They are exactly the same.", "Boiling happens only at the surface.", "Evaporation needs 100 °C."], "Surface vs throughout."),
    ("Why does a gas exert pressure on the walls of its container?", "Its particles hit the walls.", ["It is heavy.", "It is a solid.", "Its particles stick to the walls."], "Particle collisions."),
    ("A substance melts at 63 °C. What does this suggest about it at room temperature (20 °C)?", "It is a solid.", ["It is a gas.", "It is a liquid.", "It is boiling."], "Below its melting point."),
])


def body():
    think = ("<p><b>Everything is made of particles, and how they are arranged decides the state.</b></p>"
             "<ul><li>Solid: regular pattern, vibrate on the spot. Liquid: close together, slide past each other. Gas: far apart, move fast in all directions.</li>"
             "<li>Melting, freezing, boiling, evaporating, condensing and sublimating are changes of state. Mass is conserved.</li>"
             "<li>Density = mass ÷ volume. Particles diffuse from high to low concentration.</li></ul>")
    ex = [("Mass 60 g, volume 20 cm³. Density?", ["60 ÷ 20"], "3 g/cm³"),
          ("Gas to liquid is called?", ["It happens on a cold window"], "condensing")]
    mist = ["Thinking particles in a solid do not move.", "Thinking particles get bigger when heated.", "Thinking mass is lost when ice melts."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Solids, liquids and gases", B1 + [(g_state, 9), (g_change, 3)]),
        ("Changes of state", [(g_change, 5), (g_mp, 10), (g_mass, 5)]),
        ("Melting and boiling points", [(g_mp, 8), (g_mass, 12)]),
        ("Density", [(g_dens, 20)]),
        ("Thinking about particles", B5 + [(g_dens, 8), (g_mass, 7)]),
    ])
    make_ks3(7, "particles-and-states-of-matter", 6, "Chemistry", "The particulate nature of matter",
             "The properties of the different states of matter (solid, liquid and gas) in terms of the particle model, including gas pressure; changes of state in terms of the particle model; the differences in arrangements, in motion and in closeness of particles explaining changes of state, shape and density; conservation of material and of mass, and reversibility, in melting, freezing, evaporation, sublimation, condensation, dissolving; Brownian motion in gases; diffusion in liquids and gases driven by differences in concentration.",
             "Particles and States of Matter",
             "Year 7 Science: Particles and States of Matter Worksheets (Particle Model, Density)",
             "States of Matter",
             "Free Year 7 science worksheets on particles and states of matter: the particle model of solids, liquids and gases, changes of state, melting and boiling points, diffusion and density. 100 questions with answers.",
             "Particles explain solids, liquids and gases.",
             "Density = mass ÷ volume. Mass is conserved in a change of state.",
             body(),
             [("How are particles arranged in solids, liquids and gases?", "In a solid they are close together in a regular pattern and vibrate. In a liquid they are close together but move past each other. In a gas they are far apart and move quickly."),
              ("Is mass lost when ice melts?", "No. The same particles are still there, so the mass of the water equals the mass of the ice."),
              ("How do you calculate density?", "Density = mass ÷ volume. A block of 60 g with a volume of 20 cm³ has a density of 3 g/cm³.")],
             sets)


if __name__ == "__main__":
    main()
