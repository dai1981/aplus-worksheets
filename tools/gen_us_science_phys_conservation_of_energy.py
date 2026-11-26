# -*- coding: utf-8 -*-
"""
US High School Physics: Conservation of Energy (HS-PS3-1)
  python tools/gen_us_science_phys_conservation_of_energy.py
Create a computational model to calculate the change in the energy of one component in a system when the change in
energy of the other component(s) and energy flows in and out of the system are known.
Energy accounting tables (PE + KE + thermal = total), falling objects, roller coasters and pendulums, energy lost to
friction, and speed from height.
Wrong answers come from real mistakes: "energy is used up", "friction destroys energy", "the speed at the bottom
depends on mass", "total energy changes as an object falls".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90309)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_drop():
    m = R.choice([0.5, 1, 2, 5, 10])
    h = R.choice([1.25, 5, 10, 20, 45, 80, 2.5, 3.2])
    k = R.choice(["ke", "v", "h"])
    if not once(("dr", m, h, k)):
        return None
    E = m * 9.8 * h
    v = (2 * 9.8 * h) ** 0.5
    if k == "ke":
        g = "%s J" % num(E, 1)
        return item("A %s kg ball is dropped from %s m. Ignoring air resistance, how much kinetic energy does it have just before it lands?" % (num(m), num(h)), g,
                    uniq(g, ["0 J", "%s J" % num(m * h), "%s J" % num(E / 2, 1), "%s J" % num(E * 2, 1)]), "All the PE (mgh = %s J) becomes KE." % num(E, 1))
    if k == "v":
        g = "%s m/s" % num(v, 1)
        return item("A ball is dropped from %s m. Ignoring air resistance, how fast is it moving just before it lands? (v = √(2gh))" % num(h), g,
                    uniq(g, ["%s m/s" % num(9.8 * h, 1), "%s m/s" % num(2 * 9.8 * h, 1), "%s m/s" % num((9.8 * h) ** 0.5, 1), "%s m/s" % num(v * 2, 1)]),
                    "mgh = ½mv² → v = √(2 × 9.8 × %s) = %s m/s. Mass cancels." % (num(h), num(v, 1)))
    g = "%s m" % num(h)
    return item("A stone hits the ground at %s m/s after being dropped. Ignoring air resistance, from what height was it dropped? (h = v² ÷ 2g)" % num(v, 1), g,
                uniq(g, ["%s m" % num(v / 9.8, 2), "%s m" % num(v * v / 9.8, 1), "%s m" % num(h * 2), "%s m" % num(v, 1)]), "h = %s² ÷ 19.6 = %s m." % (num(v, 1), num(h)))


@safe
def g_coast():
    who = P.next()[0]
    m = R.choice([200, 300, 400, 500, 600, 800])
    h1 = R.choice([20, 30, 40, 45, 50, 60])
    h2 = R.choice([0, 5, 10, 15, 20, 25])
    if h2 >= h1:
        return None
    k = R.choice(["ke", "pe", "v"])
    if not once(("cs", m, h1, h2, k)):
        return None
    top = m * 9.8 * h1
    pe2 = m * 9.8 * h2
    ke2 = top - pe2
    if k == "ke":
        g = "%s J" % num(ke2)
        return item("%s's %d kg coaster car starts at rest at the top of a %d m hill. Ignoring friction, what is its kinetic energy at a point %d m high?" % (who, m, h1, h2), g,
                    uniq(g, ["%s J" % num(top), "%s J" % num(pe2), "%s J" % num(top + pe2), "0 J"]), "KE = total − PE = %s − %s = %s J." % (num(top), num(pe2), num(ke2)))
    if k == "pe":
        g = "%s J" % num(pe2)
        return item("A %d kg coaster car is at a point %d m high on %s's track. What is its gravitational potential energy there? (g = 9.8 m/s²)" % (m, h2, who), g,
                    uniq(g, ["%s J" % num(top), "%s J" % num(ke2), "%s J" % num(m * h2), "0 J"] if h2 else ["%s J" % num(top), "%s J" % num(m * 9.8), "%s J" % num(ke2 / 2), "%s J" % num(m)]),
                    "PE = mgh = %d × 9.8 × %d = %s J." % (m, h2, num(pe2)))
    v = (2 * 9.8 * (h1 - h2)) ** 0.5
    g = "%s m/s" % num(v, 1)
    return item("A coaster car starts at rest %d m high and rolls down to %d m high. Ignoring friction, how fast is it going? (v = √(2gΔh))" % (h1, h2), g,
                uniq(g, ["%s m/s" % num((2 * 9.8 * h1) ** 0.5, 1), "%s m/s" % num(9.8 * (h1 - h2), 1), "%s m/s" % num(v / 2, 1), "%s m/s" % num(v + 5, 1)]),
                "Δh = %d m; v = √(19.6 × %d) = %s m/s." % (h1 - h2, h1 - h2, num(v, 1)))


@safe
def g_table():
    who = P.next()[0]
    T = R.choice([600, 800, 1000, 1200, 1500, 2000, 2400])
    rows = []
    thermal = 0
    pts = ["A (top)", "B", "C", "D (bottom)"]
    mid = sorted(R.sample(range(50, T, 50), 2), reverse=True)
    pes = [T, mid[0], mid[1], 0]
    if len(set(pes)) < 4:
        return None
    fr = R.random() < 0.5
    th = [0, 0, 0, 0]
    if fr:
        th = [0, R.choice([20, 40, 50]), R.choice([60, 80, 100]), R.choice([120, 150, 200])]
    kes = [T - p - t for p, t in zip(pes, th)]
    if min(kes) < 0:
        return None
    i = R.randint(1, 3)
    col = R.choice(["ke", "pe"] if not fr else ["ke", "pe", "th"])
    if not once(("tb", T, tuple(pes), tuple(th), i, col)):
        return None
    cells = []
    for j in range(4):
        r = [pts[j], num(pes[j]), num(kes[j]), num(th[j])]
        if j == i:
            r[{"pe": 1, "ke": 2, "th": 3}[col]] = "?"
        cells.append(r)
    tab = table(["Point", "Potential energy (J)", "Kinetic energy (J)", "Thermal energy (J)"], cells)
    ans = {"pe": pes[i], "ke": kes[i], "th": th[i]}[col]
    g = "%s J" % num(ans)
    return item(tab + "%s's energy model of a skateboarder on a ramp. The total energy is %s J. What is the missing value at point %s?" % (who, num(T), pts[i][0]), g,
                uniq(g, ["%s J" % num(T), "%s J" % num(T - ans), "0 J", "%s J" % num(ans + 100)]), "Total = PE + KE + thermal = %s J at every point." % num(T))


@safe
def g_loss():
    who = P.next()[0]
    m = R.choice([20, 30, 40, 50, 60])
    h = R.choice([2, 3, 4, 5, 6, 8, 10])
    pe = m * 9.8 * h
    keb = round(pe * R.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.9]))
    k = R.choice(["th", "pct"])
    if not once(("ls", m, h, keb, k)):
        return None
    th = pe - keb
    if k == "th":
        g = "%s J" % num(th, 1)
        return item("%s (%d kg) slides down a slide %d m high. At the bottom, %s has %s J of kinetic energy. How much energy became thermal energy from friction? (g = 9.8 m/s²)" % (who, m, h, who, num(keb)), g,
                    uniq(g, ["0 J", "%s J" % num(pe, 1), "%s J" % num(keb), "%s J" % num(pe + keb, 1)]), "PE at top = %s J; %s − %s = %s J." % (num(pe, 1), num(pe, 1), num(keb), num(th, 1)))
    pc = 100 * keb / pe
    g = "%s%%" % num(pc, 0)
    return item("A %d kg sled starts %d m up a hill (PE = %s J) and has %s J of kinetic energy at the bottom. What percent of its energy became kinetic energy?" % (m, h, num(pe, 1), num(keb)), g,
                uniq(g, ["%s%%" % num(100 - pc, 0), "100%", "%s%%" % num(keb / 10, 0), "0%"]), "%s ÷ %s × 100 ≈ %s%%; the rest became thermal energy." % (num(keb), num(pe, 1), num(pc, 0)))


PEND = [("at the highest point of the swing", "maximum potential energy, zero kinetic energy"), ("at the lowest point of the swing", "maximum kinetic energy, minimum potential energy"),
        ("halfway down the swing", "some potential energy and some kinetic energy"), ("after many swings with air resistance", "less total mechanical energy; some became thermal energy")]


@safe
def g_pend():
    who = P.next()[0]
    s, a = R.choice(PEND)
    if not once(("pdn", s), 2):
        return None
    return item("Describe the energy of %s's pendulum %s." % (who, s), a, R.sample([x[1] for x in PEND if x[1] != a], 3), "PE and KE trade back and forth; friction turns some into thermal energy.")


B1 = bank([
    ("What does the law of conservation of energy say?", "Energy cannot be created or destroyed, only transferred or transformed.", ["Energy is used up over time.", "Energy can be created by machines.", "Energy is destroyed by friction."], "Total stays constant."),
    ("A ball falls freely. What happens to its potential and kinetic energy?", "PE decreases and KE increases by the same amount.", ["Both increase.", "Both decrease.", "PE increases."], "Transformation."),
    ("Where does energy 'lost' to friction go?", "It becomes thermal energy (and some sound) in the surfaces and air.", ["It is destroyed.", "It turns into mass.", "It returns to the battery."], "Still conserved."),
    ("What is a closed (isolated) system?", "a system where no energy flows in or out", ["a system with no motion", "a system with only one object", "a system with friction only"], "Total is constant."),
    ("Do a heavy ball and a light ball dropped from the same height land at the same speed (no air resistance)?", "Yes, because mass cancels in mgh = ½mv².", ["No, the heavy one is faster.", "No, the light one is faster.", "Only on the Moon."], "v = √(2gh)."),
    ("What is mechanical energy?", "the sum of kinetic and potential energy", ["thermal energy only", "the energy in a battery", "the mass of an object"], "KE + PE."),
    ("Why can a roller coaster's later hills not be taller than the first hill?", "The car cannot gain more energy than it started with, and friction removes some.", ["The track is too weak.", "Gravity gets stronger.", "Taller hills are illegal."], "Energy budget."),
    ("A computational model of a system tracks energy in a table. What should stay the same?", "the total energy (if no energy enters or leaves)", ["the kinetic energy", "the potential energy", "the speed"], "Accounting."),
])
B5 = bank([
    ("Why does a bouncing ball rise a little lower each bounce?", "Some energy becomes thermal energy and sound in each bounce.", ["Energy is destroyed.", "Gravity gets stronger.", "The ball loses mass."], "Energy transfer."),
    ("A cyclist coasts down a hill and her speed is lower than predicted. Which energy flow was left out of the model?", "work done by air resistance and friction", ["gravity", "her mass", "the height"], "Energy leaves the system."),
    ("Energy enters a car as chemical energy in fuel. Where does most of it go?", "thermal energy in the engine and surroundings", ["kinetic energy only", "potential energy only", "it is destroyed"], "Efficiency."),
    ("A pole vaulter runs fast before jumping. Why?", "More kinetic energy can become gravitational potential energy (more height).", ["Speed adds mass.", "Running reduces gravity.", "Kinetic energy is destroyed."], "KE → elastic PE → PE."),
    ("A student's energy table shows total energy increasing as a ball falls. What does this tell her?", "There is a mistake, because energy cannot be created.", ["Gravity adds energy.", "The ball gained mass.", "It is correct for falling objects."], "Check the model."),
])


def body():
    think = ("<p><b>Total energy stays the same; it only changes form or moves.</b></p>"
             "<ul><li>No friction: PE<sub>top</sub> + KE<sub>top</sub> = PE<sub>bottom</sub> + KE<sub>bottom</sub>. Falling from rest: v = √(2gh).</li>"
             "<li>With friction: some energy becomes thermal energy, but the total is still the same.</li>"
             "<li>Energy table: PE + KE + thermal = total at every point.</li></ul>")
    ex = [("Dropped from 20 m. Speed at the bottom?", ["√(2 × 9.8 × 20)"], "19.8 m/s"),
          ("PE 1,000 J at top, KE 850 J at bottom. Thermal?", ["1,000 − 850"], "150 J")]
    mist = ["Thinking energy gets used up.", "Thinking friction destroys energy.", "Thinking heavier objects land faster (no air resistance)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy is conserved", B1 + [(g_pend, 3), (g_drop, 9)]),
        ("Falling objects", [(g_drop, 14), (g_pend, 3), (g_coast, 3)]),
        ("Roller coasters", [(g_coast, 16), (g_drop, 4)]),
        ("Energy tables", [(g_table, 14), (g_loss, 6)]),
        ("Energy flowing out", B5 + [(g_loss, 8), (g_table, 4), (g_coast, 3)]),
    ])
    make("physics", "conservation-of-energy", 9, "HS-PS3-1",
         "Create a computational model to calculate the change in the energy of one component in a system when the change in energy of the other component(s) and energy flows in and out of the system are known.",
         "Conservation of Energy",
         "Conservation of Energy Worksheets: Roller Coasters, Falling Objects and Energy Tables (Physics)",
         "Conservation of Energy",
         "Free high school physics worksheets on conservation of energy (NGSS HS-PS3-1): energy tables, falling objects, roller coasters, pendulums and energy lost to friction. 100 questions with answers.",
         "Energy is never created or destroyed.",
         "PE + KE + thermal energy stays the same in a closed system.",
         body(),
         [("What is conservation of energy?", "In a closed system, the total energy stays the same. It can change from one form to another, such as potential to kinetic."),
          ("How fast does a dropped object land?", "Without air resistance, v = √(2gh). The mass does not matter."),
          ("What happens to energy lost to friction?", "It is not destroyed. It becomes thermal energy (and a little sound) in the surfaces and the air.")],
         sets)


if __name__ == "__main__":
    main()
