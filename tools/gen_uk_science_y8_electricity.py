# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Physics): Electricity
  python tools/gen_uk_science_y8_electricity.py
Electric current (amps) and potential difference (volts), measuring them with ammeters and voltmeters, current in
series and parallel circuits, sharing potential difference, resistance (R = V ÷ I), conductors and insulators,
static electricity (charges attract and repel) and electric fields. Reuses the circuit-symbol questions of the
Year 6 unit (new seed).
Wrong answers come from real mistakes: "current is used up by a bulb", "a voltmeter goes in series",
"in parallel the current is the same everywhere", "like charges attract".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y6_circuit_symbols as CS
from sci_phys import uniq

CS.U = Unit(61811)
CS.R = CS.U.R
CS.P = People(CS.R)
uk_sci.USED.clear()
U, R, P = CS.U, CS.R, CS.P


def num(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def g_vir():
    k = R.choice(["R", "V", "I"])
    i = R.choice([0.1, 0.2, 0.25, 0.5, 1, 1.5, 2, 3])
    r = R.choice([2, 4, 5, 6, 10, 12, 20, 24])
    v = i * r
    if v > 240 or v != round(v, 2) or not once(("vi", k, i, r)):
        return None
    if k == "R":
        g = "%s Ω" % num(r)
        return item("A lamp has a potential difference of %s V across it and a current of %s A through it. What is its resistance?" % (num(v), num(i)), g,
                    uniq(g, ["%s Ω" % num(v * i), "%s Ω" % num(i / v if v else 0), "%s Ω" % num(v + i), "%s Ω" % num(r * 2)]), "R = V ÷ I = %s ÷ %s = %s Ω." % (num(v), num(i), num(r)))
    if k == "V":
        g = "%s V" % num(v)
        return item("A current of %s A flows through a %s Ω resistor. What is the potential difference across it?" % (num(i), num(r)), g,
                    uniq(g, ["%s V" % num(r / i), "%s V" % num(r + i), "%s V" % num(r), "%s V" % num(v * 2)]), "V = I × R = %s × %s = %s V." % (num(i), num(r), num(v)))
    g = "%s A" % num(i)
    return item("A potential difference of %s V is across a %s Ω resistor. What current flows?" % (num(v), num(r)), g,
                uniq(g, ["%s A" % num(v * r), "%s A" % num(r / v), "%s A" % num(v), "%s A" % num(i * 2)]), "I = V ÷ R = %s ÷ %s = %s A." % (num(v), num(r), num(i)))


def g_series():
    a = R.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.2])
    n = R.choice([2, 3])
    k = R.choice(["same", "after"])
    if not once(("se", a, n, k)):
        return None
    g = "%s A" % num(a)
    if k == "same":
        q = "An ammeter before the first of %d lamps in a series circuit reads %s A. What does an ammeter between the lamps read?" % (n, num(a))
    else:
        q = "In a series circuit with %d lamps, the current leaving the cell is %s A. What is the current returning to the cell?" % (n, num(a))
    return item(q, g, uniq(g, ["%s A" % num(a / n), "%s A" % num(a * n), "0 A", "%s A" % num(a / 2)]), "In series the current is the same everywhere. It is not used up.")


def g_par():
    b1 = R.choice([0.2, 0.3, 0.4, 0.5, 0.6])
    b2 = R.choice([0.1, 0.2, 0.3, 0.4, 0.7])
    k = R.choice(["total", "branch"])
    if not once(("pa", b1, b2, k)):
        return None
    t = round(b1 + b2, 2)
    if k == "total":
        g = "%s A" % num(t)
        return item("A parallel circuit has two branches. The currents in the branches are %s A and %s A. What is the current from the cell?" % (num(b1), num(b2)), g,
                    uniq(g, ["%s A" % num(b1), "%s A" % num(abs(b1 - b2)), "%s A" % num(b1 * b2), "%s A" % num(t * 2)]), "In parallel the branch currents add up: %s + %s." % (num(b1), num(b2)))
    g = "%s A" % num(b2)
    return item("The current from the cell is %s A. One of two parallel branches carries %s A. What does the other branch carry?" % (num(t), num(b1)), g,
                uniq(g, ["%s A" % num(t), "%s A" % num(b1), "%s A" % num(t + b1), "%s A" % num(t / 2)]), "%s − %s = %s A." % (num(t), num(b1), num(b2)))


def g_pd():
    v = R.choice([3, 4.5, 6, 9, 12])
    a = R.choice([1, 1.5, 2, 2.5, 3, 4, 5])
    if a >= v or not once(("pd", v, a)):
        return None
    b = v - a
    g = "%s V" % num(b)
    return item("Two lamps are in series with a %s V battery. The voltmeter across one lamp reads %s V. What does it read across the other lamp?" % (num(v), num(a)), g,
                uniq(g, ["%s V" % num(v), "%s V" % num(a), "%s V" % num(v + a), "%s V" % num(v / 2) if v / 2 != b else "0 V"]), "In series the potential difference is shared: %s − %s." % (num(v), num(a)))


CH = [("positive", "positive", "repel"), ("negative", "negative", "repel"), ("positive", "negative", "attract"), ("negative", "positive", "attract")]
RUB = [("a polythene rod rubbed with a cloth", "negative", "Electrons move from the cloth to the rod."), ("an acetate rod rubbed with a cloth", "positive", "Electrons move from the rod to the cloth."),
       ("a balloon rubbed on hair", "negative", "Electrons move from the hair to the balloon.")]


def g_static():
    k = R.choice(["ch", "ch", "rub", "why"])
    if k == "ch":
        a, b, r = R.choice(CH)
        if not once(("st", a, b)):
            return None
        return item("A %s charge is brought near a %s charge. What happens?" % (a, b), "They " + r + ".", ["They " + ("attract" if r == "repel" else "repel") + ".", "Nothing happens.", "They both become neutral."],
                    "Like charges repel; unlike charges attract.")
    if k == "rub":
        o, c, e = R.choice(RUB)
        if not once(("rb", o)):
            return None
        return item("What charge does %s gain?" % o, c, [x for x in ["positive", "negative", "no charge", "a magnetic charge"] if x != c], e)
    if not once(("why",)):
        return None
    return item("Why does a charged balloon stick to a wall?", "It attracts opposite charges in the wall.", ["It is magnetic.", "Air pushes it.", "The wall is glue."], "Induced charge.")


B1 = bank([
    ("What is electric current?", "the flow of charge (electrons) around a circuit", ["the push of the battery", "the amount of energy in a wire", "the resistance of a lamp"], "Measured in amps (A)."),
    ("What is potential difference (voltage)?", "the push that makes charge flow, measured in volts", ["the flow of charge", "the resistance of a wire", "the power of a lamp"], "Measured with a voltmeter."),
    ("How is an ammeter connected?", "in series with the component", ["in parallel across the component", "not in the circuit", "only to the battery"], "Current passes through it."),
    ("How is a voltmeter connected?", "in parallel across the component", ["in series with the component", "between the switch and the cell only", "in a separate circuit"], "It compares two points."),
    ("What is the unit of resistance?", "the ohm (Ω)", ["the amp (A)", "the volt (V)", "the watt (W)"], "R = V ÷ I."),
    ("Is current used up by a lamp?", "No. The same current flows back to the cell; energy is transferred, not current.", ["Yes, it is all used up.", "Half of it is used up.", "Current turns into light."], "Common mistake."),
])
B5 = bank([
    ("Why are the lights in a house wired in parallel?", "Each can be switched on and off on its own, and one failing does not turn off the others.", ["To make them dimmer.", "To use less wire.", "Parallel uses no current."], "Independent branches."),
    ("Adding more lamps in series makes them dimmer. Why?", "The total resistance increases, so the current falls.", ["The current is used up faster.", "The voltage rises.", "Lamps share light."], "More resistance."),
    ("Why do long thin wires have more resistance than short thick ones?", "Charges collide more as they move through them.", ["They are colder.", "They have no electrons.", "They are insulators."], "Size of conductor."),
    ("What is an electric field?", "the region around a charged object where another charge feels a force", ["a field of wires", "the space inside a battery only", "a magnet's pull"], "Non-contact force."),
    ("Why can you get a small shock after walking on a nylon carpet?", "Your body builds up static charge that jumps to a metal object.", ["The carpet is plugged in.", "You become magnetic.", "Shoes make electricity."], "Static discharge."),
    ("Which material is a good electrical insulator?", "plastic", ["copper", "steel", "graphite"], "Used to cover wires."),
])


def body():
    think = ("<p><b>Current is the flow of charge; potential difference is the push.</b></p>"
             "<ul><li>Series: the current is the same everywhere; the potential difference is shared.</li>"
             "<li>Parallel: the branch currents add up to the total; each branch gets the full potential difference.</li>"
             "<li>Resistance R = V ÷ I, in ohms. Like charges repel; unlike charges attract.</li></ul>")
    ex = [("6 V across a lamp, 0.5 A through it. R?", ["R = 6 ÷ 0.5"], "12 Ω"),
          ("Branches carry 0.3 A and 0.2 A. Total?", ["Add in parallel"], "0.5 A")]
    mist = ["Thinking current is used up by a lamp.", "Connecting a voltmeter in series.", "Thinking like charges attract."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Current and potential difference", B1 + [(CS.g_sym, 6), (CS.g_read, 4), (g_series, 4)]),
        ("Series and parallel", [(g_series, 6), (g_par, 8), (g_pd, 6)]),
        ("Resistance", [(g_vir, 16), (g_pd, 4)]),
        ("Static electricity", [(g_static, 7), (g_vir, 7), (g_par, 6)]),
        ("Using circuits", B5 + [(g_vir, 6), (g_par, 4), (g_series, 4)]),
    ])
    make_ks3(8, "electricity", 11, "Physics", "Current electricity",
             "Electric current, measured in amperes, in circuits, series and parallel circuits, currents add where branches meet and current as flow of charge; potential difference, measured in volts, battery and bulb ratings; resistance, measured in ohms, as the ratio of potential difference (p.d.) to current; differences in resistance between conducting and insulating components (quantitative); static electricity: separation of positive or negative charges when objects are rubbed together, transfer of electrons, forces between charged objects; the idea of electric field, forces acting across the space between objects not in contact.",
             "Electricity",
             "Year 8 Science: Electricity Worksheets (Current, Voltage, Resistance, Static)",
             "Electricity",
             "Free Year 8 science worksheets on electricity: current and potential difference, ammeters and voltmeters, series and parallel circuits, resistance R = V ÷ I and static electricity. 100 questions with answers.",
             "Resistance = potential difference ÷ current.",
             "In series current is the same everywhere; in parallel branch currents add up.",
             body(),
             [("What is the difference between current and potential difference?", "Current is the flow of charge, measured in amps with an ammeter in series. Potential difference is the push, measured in volts with a voltmeter in parallel."),
              ("How do you calculate resistance?", "Divide the potential difference by the current: R = V ÷ I. The unit is the ohm (Ω)."),
              ("How does static electricity work?", "Rubbing two materials moves electrons from one to the other. The one gaining electrons becomes negative; like charges repel and unlike charges attract.")],
             sets)


if __name__ == "__main__":
    main()
