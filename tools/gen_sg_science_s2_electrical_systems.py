# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Systems): Electrical Systems
  python tools/gen_sg_science_s2_electrical_systems.py
Current (A), potential difference (V) and resistance (ohm); circuit symbols and diagrams with cells, switches, lamps, fixed and
variable resistors, ammeters and voltmeters; current in series and parallel circuits; chemical, heating and magnetic effects
of current and their uses; electrical hazards and safety (fuses, earthing, overloading, wet hands); power in watts; the cost of
electricity in kWh; saving electricity at home.
UK KS3 circuit makers are reused (no V = IR: not required in the Singapore syllabus).
Wrong answers come from real mistakes: "current is used up by a lamp", "an ammeter is connected in parallel",
"a fuse is in the neutral wire", "kWh is a unit of power".
"""
from sg_sci import item, bank, lesson, fig
from sg_lss import Unit, luse, make_lss, seo, once, upto, People
from uk_sci_pics import symbol
from sci_common import svg_wrap, rect, line, text, circle, arrow


def sym2(k):
    w = line(8, 30, 112, 30, w=2.5)
    if k == "resistor":
        b = rect(40, 20, 40, 20, fill="#fff", sw=2.5)
    elif k == "variable_resistor":
        b = rect(40, 20, 40, 20, fill="#fff", sw=2.5) + arrow(34, 48, 86, 10, w=2)
    else:
        b = circle(60, 30, 16, fill="#fff", sw=2.5) + text(60, 37, "A" if k == "ammeter" else "V", fs=18)
    return svg_wrap(120, 60, w + b, "circuit symbol")

U = Unit(64207)
R = U.R
P = People(R)
EL = luse(U, "gen_uk_science_y8_electricity", drop=[r"resistance\?", r"static", r"field", r"\bΩ\b.*\bA\b"])
EP = luse(U, "gen_uk_science_y8_energy_and_power", drop=[r"\bstore", r"efficien", r"loft", r"winter"])

QTY = [("electric current", "ampere (A)", "an ammeter"), ("potential difference (voltage)", "volt (V)", "a voltmeter"), ("resistance", "ohm (Ω)", "an ohmmeter"), ("power", "watt (W)", "a power meter")]


def g_unit():
    q, u, m = R.choice(QTY)
    if not once(("un", q)):
        return None
    return item("What is the SI unit of %s?" % q, u, R.sample([x[1] for x in QTY if x[1] != u], 3), "%s is measured in the %s." % (q[0].upper() + q[1:], u))


SYM = [("cell", "a cell"), ("battery", "a battery"), ("lamp", "a lamp"), ("switch_open", "an open switch"), ("switch_closed", "a closed switch"), ("buzzer", "a buzzer"), ("motor", "a motor"),
       ("resistor", "a fixed resistor"), ("variable_resistor", "a variable resistor"), ("ammeter", "an ammeter"), ("voltmeter", "a voltmeter")]


def g_sym():
    k, a = R.choice(SYM)
    if not once(("sy", k)):
        return None
    try:
        pic = fig(sym2(k) if k in ("resistor", "variable_resistor", "ammeter", "voltmeter") else symbol(k))
    except Exception:
        return None
    return item(pic + "What does this circuit symbol show?", a, R.sample([x[1] for x in SYM if x[1] != a], 3), "This is the symbol for %s." % a)


EFF = [("an electric kettle", "heating effect"), ("an electric iron", "heating effect"), ("a hair dryer's heating coil", "heating effect"), ("a fuse", "heating effect"),
       ("an electric bell", "magnetic effect"), ("an electromagnet in a scrapyard crane", "magnetic effect"), ("an electric motor", "magnetic effect"), ("a loudspeaker", "magnetic effect"),
       ("electroplating a spoon with silver", "chemical effect"), ("charging a handphone battery", "chemical effect"), ("purifying copper by electrolysis", "chemical effect")]


def g_eff():
    d, a = R.choice(EFF)
    if not once(("ef", d)):
        return None
    return item("Which effect of electric current is used in %s?" % d, "the " + a, ["the " + x for x in ["heating effect", "magnetic effect", "chemical effect", "lighting effect only"] if x != a],
                {"heating effect": "Current through a resistor produces heat.", "magnetic effect": "A current in a coil produces a magnetic field.",
                 "chemical effect": "Current causes chemical changes in a solution."}[a])


HAZ = [("using an appliance with wet hands", "Water conducts electricity, so you could get an electric shock."),
       ("plugging too many appliances into one socket", "The cable overheats and could start a fire."),
       ("using a cable with damaged insulation", "Bare wires could give an electric shock or cause a short circuit."),
       ("putting a 13 A fuse in a lamp that needs only 1 A", "The fuse will not melt if there is a fault, so the cable could overheat."),
       ("removing the earth wire from a metal kettle", "If a live wire touches the metal case, the case could give a shock."),
       ("pushing a metal object into a socket", "It conducts electricity to your body, giving a shock.")]


def g_haz():
    s, a = R.choice(HAZ)
    if not once(("hz", s)):
        return None
    return item("Why is %s dangerous?" % s, a, R.sample([x[1] for x in HAZ if x[0] != s], 3), a)


def g_cost():
    p = R.choice([0.1, 0.5, 1, 1.5, 2, 2.5])
    h = R.choice([2, 3, 4, 5, 8, 10])
    c = R.choice([30, 32, 35])
    ap = {0.1: "a television", 0.5: "a rice cooker", 1: "a microwave oven", 1.5: "an air-conditioner", 2: "an electric kettle", 2.5: "a water heater"}[p]
    if not once(("cs", p, h)):
        return None
    kwh = p * h
    cost = kwh * c
    return item("%s of power %g kW is used for %d hours. Electricity costs %d cents per kWh. What is the cost?" % (ap[0].upper() + ap[1:], p, h, c),
                "%g cents" % round(cost, 2), ["%g cents" % round(p * c, 2), "%g cents" % round(kwh, 2), "%g cents" % round(p * h * c * 10, 2)],
                "Energy = %g kW × %d h = %g kWh; cost = %g × %d = %g cents." % (p, h, kwh, kwh, c, round(cost, 2)))


VAR = [("The resistance of the variable resistor is increased.", "The current decreases and the lamp becomes dimmer."),
       ("The resistance of the variable resistor is decreased.", "The current increases and the lamp becomes brighter."),
       ("A second lamp is added in series.", "The total resistance increases, so the current decreases and both lamps are dimmer."),
       ("A second lamp is added in parallel.", "Each branch has the full voltage, so each lamp stays as bright and the total current increases.")]


def g_var():
    s, a = R.choice(VAR)
    if not once(("va", s)):
        return None
    return item("A lamp is in a circuit with a cell. " + s + " What happens?", a, R.sample([x[1] for x in VAR if x[1] != a], 2) + ["The current is used up by the lamp."],
                "More resistance means less current.")


B1 = bank([
    ("How is an ammeter connected to measure the current through a lamp?", "in series with the lamp", ["in parallel with the lamp", "across the cell only", "it is not connected"], "All the current must pass through it."),
    ("How is a voltmeter connected to measure the potential difference across a lamp?", "in parallel with the lamp", ["in series with the lamp", "only at the switch", "in a separate circuit"], "It compares the two ends of the lamp."),
    ("What does a fuse do?", "It melts and breaks the circuit when the current is too large.", ["It makes the current larger.", "It stores charge.", "It turns the appliance on."], "The fuse is in the live wire."),
    ("Why is the metal case of a kettle connected to the earth wire?", "If the case becomes live, current flows to earth and the fuse melts.", ["To make the kettle heat faster.", "To save electricity.", "To make it lighter."], "This protects the user."),
    ("What is the kilowatt-hour (kWh)?", "a unit of electrical energy used by power companies", ["a unit of power", "a unit of current", "a unit of time"], "1 kWh = the energy used by a 1 kW appliance in 1 hour."),
    ("Which statement about current in a series circuit is correct?", "The current is the same at every point.", ["The current is used up by each lamp.", "The current is largest after the last lamp.", "There is no current in a series circuit."], "Current is not used up."),
    ("Which household habit saves the most electricity?", "setting the air-conditioner to 25 °C and switching it off when not needed", ["leaving the TV on standby all night", "keeping the fridge door open", "charging phones all day"], "Air-conditioners use a lot of power."),
    ("Why does an appliance with a higher power rating cost more to run for the same time?", "It uses more electrical energy each second.", ["It has a lower current.", "It uses less energy.", "Power does not affect cost."], "Power = energy used per second."),
])
B5 = bank([
    ("A 2 kW kettle is used for 0.25 h every day for 30 days. How much energy is used?", "15 kWh", ["60 kWh", "0.5 kWh", "2 kWh"], "2 × 0.25 × 30 = 15 kWh."),
    ("Why are household appliances connected in parallel?", "Each one gets the full voltage and can be switched on and off on its own.", ["To use less wire only.", "So that one switch controls all.", "To make the current smaller everywhere."], "If one breaks, the others still work."),
    ("Mei Ling's hair dryer stopped working and the fuse was found melted. What is the most likely cause?", "A fault caused too large a current to flow.", ["The current was too small.", "The hair dryer was switched off.", "The voltage was zero."], "A fuse protects the cable."),
    ("Which energy label tick rating helps a family in Singapore save electricity when buying a fridge?", "the one with more ticks, meaning it is more energy efficient", ["the one with fewer ticks", "the one with the largest box", "the most expensive one"], "More ticks means lower running cost."),
    ("A circuit has a cell, a lamp and a variable resistor in series. What is the variable resistor used for?", "to change the current and so the brightness of the lamp", ["to measure the current", "to store energy", "to protect against shocks"], "It is like a dimmer switch."),
    ("Why should you never touch a person who is getting an electric shock?", "The current could pass through you too; switch off the power first.", ["It is always safe to touch them.", "Rubber gloves conduct electricity.", "Current stops when you touch them."], "Switch off at the mains or use a dry insulator."),
])


def body():
    think = ("<p><b>Current flows when a potential difference pushes charge round a complete circuit.</b></p>"
             "<ul><li>Current: amperes (A), measured by an <b>ammeter in series</b>. Potential difference: volts (V), measured by a <b>voltmeter in parallel</b>. Resistance: ohms (Ω).</li>"
             "<li>More resistance means less current. A variable resistor changes the current.</li>"
             "<li>Effects of current: <b>heating</b> (kettle, fuse), <b>magnetic</b> (motor, bell), <b>chemical</b> (electroplating, charging).</li>"
             "<li>Energy (kWh) = power (kW) × time (h). Cost = kWh × price per kWh. Use fuses and earthing to stay safe.</li></ul>")
    ex = [("A 1.5 kW air-conditioner runs for 4 h at 30 cents per kWh. Cost?", ["1.5 × 4 = 6 kWh", "6 × 30"], "180 cents ($1.80)"),
          ("How is an ammeter connected?", ["Current must pass through it"], "in series")]
    mist = ["Saying current is used up by a lamp. The current is the same all round a series circuit.", "Connecting an ammeter in parallel or a voltmeter in series.",
            "Calling kWh a unit of power. It is a unit of energy.", "Thinking a bigger fuse is always safer. It must suit the appliance."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Current, voltage and resistance", B1[:2] + EL.B1 + [(g_unit, 4), (g_sym, 6), (B1[5], 1)]),
        ("Series and parallel circuits", [(EL.g_series, 6), (EL.g_par, 6), (EL.g_pd, 4), (g_var, 4)]),
        ("Effects of electric current", [(g_eff, 11), (g_unit, 2), (g_sym, 2), (g_var, 1)] + B1[2:4] + [(EL.g_par, 2)]),
        ("Power, energy and cost", B1[4:5] + B1[6:8] + [(g_cost, 8), (EP.g_kwh, 4), (EP.g_watt, 3)]),
        ("Safety and exam-style questions", B5 + EL.B5 + [(g_haz, 6), (g_cost, 2), (EP.g_kwh, 2)]),
    ])
    make_lss(2, "electrical-systems", 7, "Systems", "Electrical Systems",
             "Describe current, potential difference and resistance and their SI units; draw and interpret circuit diagrams with cells, switches, lamps, fixed and variable resistors, "
             "ammeters and voltmeters; investigate current in series and parallel circuits; describe applications of the chemical, heating and magnetic effects of current; state "
             "electrical hazards and safety precautions; explain power and calculate the cost of electricity using kWh (summary of the MOE Lower Secondary Science Syllabus).",
             "Electrical Systems", seo(2, "Electrical Systems"), "Electrical systems",
             "Free Secondary 2 science worksheets for Singapore students on electricity: current, voltage, resistance, series and parallel circuits, effects of current, safety and the cost of electricity. With answers.",
             "Ammeter in series; voltmeter in parallel.", "Energy (kWh) = power (kW) × time (h).",
             body(),
             [("How do you calculate the cost of electricity?", "Multiply power in kW by time in hours to get kWh, then multiply by the price per kWh."),
              ("What does a fuse do?", "It melts and breaks the circuit if the current becomes too large, protecting the cable from overheating."),
              ("Is current used up in a circuit?", "No. The current is the same at every point in a series circuit; energy is transferred, not the current.")],
             sets)


if __name__ == "__main__":
    main()
