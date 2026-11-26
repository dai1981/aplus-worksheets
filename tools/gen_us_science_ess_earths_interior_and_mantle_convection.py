# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Earth's Interior and Mantle Convection (HS-ESS2-3)
  python tools/gen_us_science_ess_earths_interior_and_mantle_convection.py
Develop a model based on evidence of Earth's interior to describe the cycling of matter by thermal convection.
Layers by composition and by state (crust, mantle, outer core, inner core; lithosphere, asthenosphere), depths, density,
seismic P and S waves and the shadow zone, S–P lag time and distance, and mantle convection driven by internal heat.
Wrong answers come from real mistakes: "the mantle is liquid lava", "S waves travel through the outer core",
"Earth is the same density all the way through", "convection is driven by the Sun".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90408)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


LAY = [("crust", 0, 35), ("mantle", 35, 2900), ("outer core", 2900, 5150), ("inner core", 5150, 6371)]


@safe
def g_depth():
    who = P.next()[0]
    i = R.randrange(4)
    lo, hi = LAY[i][1], LAY[i][2]
    d = R.randint(lo + 1, hi - 1) // 10 * 10 if hi - lo > 40 else R.randint(lo + 1, hi - 1)
    if d <= lo or d >= hi or not once(("dp", d)):
        return None
    tab = table(["Layer", "Depth (km)"], [[n, "%s–%s" % (num(a), num(b))] for n, a, b in LAY])
    return item(tab + "%s's model probe is %s km below the surface. Which layer is it in?" % (who, num(d)), LAY[i][0], [x[0] for x in LAY if x[0] != LAY[i][0]], "Find the depth range that includes %s km." % num(d))


PROP = [("crust", "thin, rocky outer layer; thickest under continents"), ("lithosphere", "rigid outer layer of crust and uppermost mantle, broken into plates"),
        ("asthenosphere", "hot, soft part of the upper mantle that flows slowly"), ("mantle", "thick layer of hot solid rock that moves by slow convection"),
        ("outer core", "liquid iron and nickel whose motion makes Earth's magnetic field"), ("inner core", "solid iron and nickel under enormous pressure")]


@safe
def g_prop():
    n, d = R.choice(PROP)
    k = R.random() < 0.5
    if not once(("pr", n, k)):
        return None
    if k:
        return item("Which layer is described: %s?" % d, "the %s" % n, ["the %s" % x[0] for x in R.sample([x for x in PROP if x[0] != n], 3)], "Layers differ in composition and state.")
    return item("Which best describes Earth's %s?" % n, d, R.sample([x[1] for x in PROP if x[1] != d], 3), "Match the layer.")


@safe
def g_lag():
    who = P.next()[0]
    lag = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 90, 120])
    k = R.choice(["d", "lag"])
    if not once(("lg", lag, k)):
        return None
    d = lag * 8
    if k == "d":
        g = "about %s km" % num(d)
        return item("At %s's station, S waves arrive %d s after P waves. Using the rule of thumb of 8 km per second of lag, how far away was the earthquake?" % (who, lag), g,
                    uniq(g, ["about %s km" % num(lag / 8, 2), "about %s km" % num(lag), "about %s km" % num(d * 2), "about %s km" % num(lag * 6)]), "%d × 8 = %s km." % (lag, num(d)))
    g = "%d s" % lag
    return item("An earthquake is %s km from a seismograph. Using about 8 km per second of S–P lag, how long after the P waves do the S waves arrive?" % num(d), g,
                uniq(g, ["%s s" % num(d * 8), "%d s" % (lag * 2), "%d s" % (lag // 2), "0 s"]), "%s ÷ 8 = %d s." % (num(d), lag))


@safe
def g_travel():
    w, v = R.choice([("P wave", 6), ("S wave", 3.5), ("P wave", 8), ("S wave", 4.5)])
    d = R.choice([120, 240, 360, 480, 600, 720, 900, 1200, 1800])
    t = d / v
    if t != round(t, 1) or not once(("tv", w, v, d)):
        return None
    g = "%s s" % num(t, 1)
    return item("A %s travels %s km at %s km/s through the crust and upper mantle. How long does it take?" % (w, num(d), num(v, 1)), g,
                uniq(g, ["%s s" % num(d * v, 1), "%s s" % num(v / d, 4), "%s s" % num(t * 2, 1), "%s s" % num(t / 2, 1)]), "t = d ÷ v = %s ÷ %s = %s s." % (num(d), num(v, 1), num(t, 1)))


SEIS = [("S waves do not pass through the outer core.", "The outer core is liquid."), ("P waves bend and slow down when they enter the outer core.", "The outer core is a different material and state from the mantle."),
        ("There is a shadow zone where no direct S waves arrive.", "A liquid layer blocks S waves deep inside Earth."), ("P waves speed up again in the inner core.", "The inner core is solid."),
        ("Earth's average density (5.5 g/cm³) is much greater than crust rock (2.7 g/cm³).", "Much denser material, like iron, must be deep inside."),
        ("Seismic waves slow down in a zone about 100–200 km deep.", "The asthenosphere is hot and partly soft.")]


@safe
def g_seis():
    s, a = R.choice(SEIS)
    k = R.random() < 0.6
    if not once(("ss", s, k)):
        return None
    if k:
        return item("Evidence: %s What does it show?" % s, a, R.sample([x[1] for x in SEIS if x[1] != a], 3), "We learn about the interior mainly from seismic waves and density.")
    return item("Which evidence supports this claim: “%s”" % a, s, R.sample([x[0] for x in SEIS if x[0] != s], 3), "Match the evidence.")


B1 = bank([
    ("What is the main heat source inside Earth?", "radioactive decay plus heat left over from Earth's formation", ["sunlight soaking into the ground", "friction from wind", "the Moon's light"], "Internal heat."),
    ("How does mantle convection move matter?", "Hot, less dense rock slowly rises; cooler, denser rock sinks.", ["Liquid lava flows quickly in rivers.", "The Sun heats the mantle.", "Rock never moves."], "Convection cells."),
    ("Is the mantle liquid?", "No. It is mostly solid rock that can flow very slowly over millions of years.", ["Yes, it is all molten lava.", "Yes, it is water.", "It is a gas."], "Plastic solid."),
    ("Why is the inner core solid even though it is very hot?", "The enormous pressure keeps the iron solid.", ["It is cold.", "It is made of ice.", "Gravity is zero there."], "Pressure effect."),
    ("Which seismic waves can travel through liquids?", "P waves", ["S waves", "both equally", "neither"], "Compressional waves."),
    ("What creates Earth's magnetic field?", "moving liquid iron in the outer core", ["the crust's rocks", "the oceans", "the atmosphere"], "Geodynamo."),
    ("How is the lithosphere different from the asthenosphere?", "The lithosphere is rigid; the asthenosphere is hot and soft enough to flow.", ["They are the same.", "The lithosphere is liquid.", "The asthenosphere is part of the core."], "Mechanical layers."),
    ("How does mantle convection connect to plate tectonics?", "Rising and sinking mantle helps move the plates above.", ["It stops plates.", "It only makes weather.", "It has no connection."], "Driving force."),
])
B5 = bank([
    ("Why do scientists rely on seismic waves to study the deep interior?", "No one can drill that deep, but waves travel through it and change speed and direction.", ["They have drilled to the core.", "The interior is visible from space.", "Volcanoes bring up core samples."], "Indirect evidence."),
    ("Iron meteorites are thought to be pieces of planet cores. How do they help?", "They give samples similar to what Earth's core may be made of.", ["They are from the Sun.", "They show the core is ice.", "They prove Earth has no core."], "Model evidence."),
    ("A lava lamp is used to model the mantle. What is one limitation?", "The mantle flows millions of times more slowly and is mostly solid.", ["The mantle is lighter than a lamp.", "There is no limitation.", "The mantle is cold."], "Evaluate the model."),
    ("Hot spots like Hawaii are thought to come from what?", "plumes of hot mantle rising from deep inside", ["meteorite impacts", "ocean currents", "the Moon's pull"], "Mantle plumes."),
    ("Why are cold, sinking slabs of old ocean plate important for convection?", "Their sinking pulls plates and returns crust to the mantle.", ["They heat the core.", "They float up.", "They stop convection."], "Cycling of matter."),
])


def body():
    think = ("<p><b>Earth's hot interior cycles rock by slow convection.</b></p>"
             "<ul><li>Layers: crust, mantle, liquid outer core, solid inner core. Lithosphere (rigid plates) sits on the softer asthenosphere.</li>"
             "<li>Evidence: S waves cannot cross the liquid outer core (shadow zone); P waves bend; Earth is denser inside.</li>"
             "<li>Heat from radioactive decay drives convection: hot rock rises, cool rock sinks, moving plates.</li></ul>")
    ex = [("S–P lag 30 s. Distance?", ["30 × 8"], "about 240 km"),
          ("Probe at 4,000 km depth?", ["Between 2,900 and 5,150 km"], "outer core")]
    mist = ["Thinking the mantle is liquid lava.", "Thinking S waves travel through the outer core.", "Thinking the Sun drives mantle convection."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Earth's layers", B1 + [(g_prop, 7), (g_depth, 5)]),
        ("Layer properties", [(g_prop, 4), (g_depth, 12), (g_seis, 4)]),
        ("Seismic evidence", [(g_seis, 7), (g_travel, 13)]),
        ("Locating earthquakes", [(g_lag, 16), (g_travel, 4)]),
        ("Modeling convection", B5 + [(g_lag, 6), (g_depth, 6), (g_travel, 3)]),
    ])
    make("earth-and-space-science", "earths-interior-and-mantle-convection", 8, "HS-ESS2-3",
         "Develop a model based on evidence of Earth's interior to describe the cycling of matter by thermal convection.",
         "Earth's Interior and Mantle Convection",
         "Earth's Interior Worksheets: Layers, Seismic Waves and Mantle Convection (Earth Science)",
         "Earth's Interior",
         "Free high school Earth and space science worksheets on Earth's interior (NGSS HS-ESS2-3): layers, density, P and S waves, the shadow zone, S–P lag and mantle convection. 100 questions with answers.",
         "Hot rock rises; cool rock sinks.",
         "Seismic waves reveal the layers; internal heat drives mantle convection.",
         body(),
         [("How do we know what Earth's interior is like?", "Seismic waves change speed and direction at boundaries. S waves cannot pass through the liquid outer core, and Earth's high average density shows iron deep inside."),
          ("What is mantle convection?", "Hot, less dense rock rises slowly while cooler, denser rock sinks, cycling matter and helping to move tectonic plates."),
          ("What heats Earth's interior?", "Mostly radioactive decay of elements like uranium, thorium and potassium, plus heat left from Earth's formation.")],
         sets)


if __name__ == "__main__":
    main()
