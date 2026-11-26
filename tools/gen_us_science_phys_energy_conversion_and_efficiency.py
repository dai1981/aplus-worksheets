# -*- coding: utf-8 -*-
"""
US High School Physics: Energy Conversion and Efficiency (HS-PS3-3)
  python tools/gen_us_science_phys_energy_conversion_and_efficiency.py
Design, build, and refine a device that works within given constraints to convert one form of energy into another
form of energy.
Energy conversions in devices, efficiency = useful output ÷ input, wasted energy, power P = E/t and P = VI, Ohm's law,
kilowatt-hours and cost, and choosing a design that meets criteria and constraints.
Wrong answers come from real mistakes: "a device can be more than 100% efficient", "wasted energy disappears",
"a higher-power device always uses more energy", "kilowatt-hours measure power".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90310)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


CONV = [("solar panel", "light → electrical"), ("battery-powered flashlight", "chemical → electrical → light"), ("generator", "kinetic → electrical"),
        ("electric motor", "electrical → kinetic"), ("loudspeaker", "electrical → sound"), ("toaster", "electrical → thermal"), ("wind turbine", "kinetic → electrical"),
        ("hydroelectric dam", "gravitational potential → kinetic → electrical"), ("microphone", "sound → electrical"), ("plant leaf", "light → chemical"),
        ("car engine", "chemical → thermal → kinetic"), ("hand-crank radio", "kinetic → electrical → sound"), ("LED bulb", "electrical → light"), ("wind-up toy", "elastic potential → kinetic")]


@safe
def g_conv():
    d, c = R.choice(CONV)
    k = R.random() < 0.6
    if not once(("cv", d, k)):
        return None
    if k:
        return item("Which energy conversion happens in a %s?" % d, c, R.sample(sorted({x[1] for x in CONV if x[1] != c}), 3), "Follow the energy from input to useful output.")
    return item("Which device converts energy like this: %s?" % c, d, R.sample([x[0] for x in CONV if x[1] != c], 3), "Match the input and output.")


@safe
def g_eff():
    who = P.next()[0]
    dev = R.choice(["motor", "LED lamp", "car engine", "phone charger", "solar panel", "electric kettle", "generator", "toy car"])
    Ein = R.choice([100, 200, 250, 400, 500, 800, 1000, 1200, 1500, 2000])
    e = R.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90, 95])
    out = Ein * e / 100
    k = R.choice(["e", "out", "waste"])
    if out != int(out) or not once(("ef", dev, Ein, e, k)):
        return None
    out = int(out)
    if k == "e":
        g = "%d%%" % e
        return item("%s's %s uses %s J of energy and gives %s J of useful energy. What is its efficiency?" % (who, dev, num(Ein), num(out)), g,
                    uniq(g, ["%d%%" % (100 - e), "%s%%" % num(Ein / out * 100, 0), "%d%%" % (e + 10), "100%"]), "%s ÷ %s × 100 = %d%%." % (num(out), num(Ein), e))
    if k == "out":
        g = "%s J" % num(out)
        return item("A %s is %d%% efficient. It takes in %s J. How much useful energy comes out?" % (dev, e, num(Ein)), g, uniq(g, ["%s J" % num(Ein - out), "%s J" % num(Ein), "%s J" % num(Ein / e, 1), "%s J" % num(out * 2)]),
                    "%d%% of %s = %s J." % (e, num(Ein), num(out)))
    g = "%s J" % num(Ein - out)
    return item("A %s takes in %s J and gives %s J of useful energy. How much energy is wasted (mostly as heat)?" % (dev, num(Ein), num(out)), g,
                uniq(g, ["0 J", "%s J" % num(out), "%s J" % num(Ein + out), "%s J" % num(Ein)]), "%s − %s = %s J; it is not destroyed, just not useful." % (num(Ein), num(out), num(Ein - out)))


@safe
def g_power():
    k = R.choice(["p", "e", "kwh"])
    if k == "kwh":
        dev, w = R.choice([("space heater", 1500), ("TV", 100), ("laptop", 50), ("microwave", 1000), ("LED bulb", 10), ("hair dryer", 2000), ("refrigerator", 200), ("game console", 150)])
        h = R.choice([2, 3, 4, 5, 6, 8, 10, 20, 30])
        c = R.choice([10, 12, 15, 20])
        if not once(("kw", dev, h, c)):
            return None
        kwh = w * h / 1000
        cost = kwh * c
        g = "%s kWh, costing %s¢" % (num(kwh, 2), num(cost, 1))
        return item("A %s W %s runs for %d hours. How much energy does it use, and what does it cost at %d¢ per kWh?" % (num(w), dev, h, c), g,
                    uniq(g, ["%s kWh, costing %s¢" % (num(w * h, 0), num(w * h * c, 0)), "%s kWh, costing %s¢" % (num(w / 1000, 3), num(w / 1000 * c, 2)), "%s kWh, costing %s¢" % (num(kwh * 2, 2), num(cost * 2, 1))]),
                    "%s W × %d h = %s Wh = %s kWh; × %d¢ = %s¢." % (num(w), h, num(w * h), num(kwh, 2), c, num(cost, 1)))
    E = R.choice([600, 1200, 1800, 3000, 6000, 12000, 36000])
    t = R.choice([10, 20, 30, 60, 120, 300, 600])
    p = E / t
    if p != round(p, 1) or not once(("pw", E, t, k)):
        return None
    if k == "p":
        g = "%s W" % num(p, 1)
        return item("A motor transfers %s J of energy in %d s. What is its power?" % (num(E), t), g, uniq(g, ["%s W" % num(E * t), "%s W" % num(t / E, 4), "%s W" % num(E), "%s W" % num(p * 2, 1)]),
                    "P = E ÷ t = %s ÷ %d = %s W." % (num(E), t, num(p, 1)))
    g = "%s J" % num(E)
    return item("A %s W device runs for %d s. How much energy does it use?" % (num(p, 1), t), g, uniq(g, ["%s J" % num(p / t, 3), "%s J" % num(p), "%s J" % num(E / 1000, 2), "%s J" % num(E * 2)]),
                "E = Pt = %s × %d = %s J." % (num(p, 1), t, num(E)))


@safe
def g_elec():
    V = R.choice([1.5, 3, 6, 9, 12, 120, 240])
    Rr = R.choice([2, 3, 4, 5, 6, 10, 12, 20, 24, 30, 60])
    I = V / Rr
    k = R.choice(["I", "P", "R"])
    if I != round(I, 2) or not once(("el", V, Rr, k)):
        return None
    if k == "I":
        g = "%s A" % num(I)
        return item("A %s V battery is connected to a %d Ω resistor. What current flows? (I = V ÷ R)" % (num(V), Rr), g, uniq(g, ["%s A" % num(V * Rr), "%s A" % num(Rr / V, 2), "%s A" % num(V), "%s A" % num(I * 2)]),
                    "I = %s ÷ %d = %s A." % (num(V), Rr, num(I)))
    if k == "P":
        Pw = V * I
        g = "%s W" % num(Pw, 2)
        return item("A device runs on %s V and draws %s A. What is its power? (P = VI)" % (num(V), num(I)), g, uniq(g, ["%s W" % num(V / I, 2), "%s W" % num(V + I, 2), "%s W" % num(I * I, 3), "%s W" % num(Pw * 2, 2)]),
                    "P = %s × %s = %s W." % (num(V), num(I), num(Pw, 2)))
    g = "%d Ω" % Rr
    return item("A %s V source pushes %s A through a heater coil. What is its resistance? (R = V ÷ I)" % (num(V), num(I)), g, uniq(g, ["%s Ω" % num(V * I, 2), "%s Ω" % num(I / V, 3), "%d Ω" % (Rr * 2), "%s Ω" % num(V)]),
                "R = %s ÷ %s = %d Ω." % (num(V), num(I), Rr))


@safe
def g_design():
    who = P.next()[0]
    names = ["Design A", "Design B", "Design C", "Design D"]
    eff = R.sample([20, 25, 30, 35, 40, 45, 50], 4)
    cost = R.sample([15, 20, 25, 30, 40, 50, 60], 4)
    lim = R.choice([30, 40, 50])
    ok = [i for i in range(4) if cost[i] <= lim]
    if len(ok) < 2:
        return None
    best = max(ok, key=lambda i: eff[i])
    top = max(range(4), key=lambda i: eff[i])
    if top == best or not once(("dg", tuple(eff), tuple(cost), lim)):
        return None
    tab = table(["Water-wheel generator", "Efficiency (%)", "Cost to build ($)"], [[n, str(e), str(c)] for n, e, c in zip(names, eff, cost)])
    return item(tab + "%s's team must spend no more than $%d. Which design best meets the goal of the highest efficiency within the budget?" % (who, lim), names[best],
                [names[top]] + [names[i] for i in range(4) if i not in (best, top)][:2], "%s is the most efficient design that meets the cost constraint." % names[best])


B1 = bank([
    ("What is efficiency?", "the percent of input energy that becomes useful output energy", ["the total energy used", "the speed of a machine", "the power of a battery"], "useful ÷ input × 100."),
    ("Can any real device be 100% efficient?", "No. Some energy is always transferred as heat to the surroundings.", ["Yes, all motors are.", "Yes, if it is new.", "Only batteries."], "Energy spreads out."),
    ("Where does the 'wasted' energy in a light bulb go?", "It becomes thermal energy in the surroundings.", ["It is destroyed.", "It turns into mass.", "It goes back into the wall."], "Still conserved."),
    ("What does a kilowatt-hour measure?", "energy", ["power", "current", "voltage"], "1 kWh = 3.6 million J."),
    ("What is the unit of power?", "the watt (W)", ["the joule (J)", "the volt (V)", "the ohm (Ω)"], "1 W = 1 J/s."),
    ("Why is an LED bulb better than an old incandescent bulb?", "It converts more of its electrical energy into light.", ["It uses more energy.", "It makes more heat.", "It has higher resistance only."], "Higher efficiency."),
    ("What is a constraint in an engineering design?", "a limit the design must stay within, such as cost or size", ["the goal of the design", "a test result", "a type of energy"], "Criteria vs constraints."),
    ("What does Ohm's law say?", "current = voltage ÷ resistance", ["power = voltage ÷ current", "voltage = current ÷ resistance", "resistance = voltage × current"], "I = V/R."),
])
B5 = bank([
    ("A team's solar oven heats water too slowly. Which change would most improve it?", "add insulation and a reflector to trap and collect more light", ["paint it white inside", "remove the lid", "make it smaller with no window"], "Refine the design."),
    ("Why do power plants waste more than half of the energy in their fuel?", "Turning thermal energy into electricity always loses much of it as heat.", ["Fuel has no energy.", "Generators create energy.", "Wires store energy."], "Thermal limits."),
    ("A student's wind turbine lights an LED in strong wind but not in light wind. Which refinement should she test?", "blades with a different shape or angle to catch more wind", ["a heavier base", "a brighter LED", "shorter wires only"], "Iterate."),
    ("Which device would most reduce a home's energy use for heating?", "better insulation in walls and windows", ["a bigger heater", "more lights", "an older furnace"], "Reduce losses."),
    ("Two kettles boil the same water. Kettle A uses 200 kJ, kettle B uses 250 kJ. Which is more efficient?", "Kettle A", ["Kettle B", "They are equal.", "It cannot be known."], "Same output, less input."),
])


def body():
    think = ("<p><b>Devices change energy from one form to another, but never perfectly.</b></p>"
             "<ul><li>Efficiency = useful output ÷ input × 100%. The rest is wasted, mostly as heat, but not destroyed.</li>"
             "<li>Power P = E ÷ t (watts). Electric power P = VI; Ohm's law I = V ÷ R. Energy in kWh = kW × hours.</li>"
             "<li>Good designs meet the criteria (goals) within the constraints (limits like cost).</li></ul>")
    ex = [("Input 500 J, useful 150 J. Efficiency?", ["150 ÷ 500 × 100"], "30%"),
          ("1,500 W heater for 4 h. Energy?", ["1.5 kW × 4 h"], "6 kWh")]
    mist = ["Thinking a device can be more than 100% efficient.", "Thinking wasted energy disappears.", "Thinking kilowatt-hours measure power."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy conversions", B1 + [(g_conv, 12)]),
        ("Efficiency", [(g_eff, 16), (g_conv, 4)]),
        ("Power and energy", [(g_power, 14), (g_eff, 6)]),
        ("Electric power", [(g_elec, 14), (g_power, 6)]),
        ("Designing devices", B5 + [(g_design, 8), (g_conv, 4), (g_elec, 3)]),
    ])
    make("physics", "energy-conversion-and-efficiency", 10, "HS-PS3-3",
         "Design, build, and refine a device that works within given constraints to convert one form of energy into another form of energy.",
         "Energy Conversion and Efficiency",
         "Energy Efficiency Worksheets: Conversions, Power, Ohm's Law and kWh (High School Physics)",
         "Energy Efficiency",
         "Free high school physics worksheets on energy conversion and efficiency (NGSS HS-PS3-3): energy conversions, efficiency, power, Ohm's law, kilowatt-hours and design constraints. 100 questions with answers.",
         "No device is 100% efficient.",
         "Efficiency = useful output ÷ input; the rest becomes heat.",
         body(),
         [("How do you calculate efficiency?", "Divide the useful output energy by the input energy and multiply by 100."),
          ("Where does wasted energy go?", "It is transferred to the surroundings, mostly as thermal energy. It is not destroyed."),
          ("What is a kilowatt-hour?", "A unit of energy: the energy used by a 1,000 W device running for 1 hour (3.6 million joules).")],
         sets)


if __name__ == "__main__":
    main()
