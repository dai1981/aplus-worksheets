# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Electric Circuits (4-PS3-2)
  python tools/gen_us_science_g4_electric_circuits.py
An electric current carries energy from a battery through a complete (closed) circuit to a bulb,
buzzer or motor. An open switch, a gap or an insulator breaks the circuit. Conductors complete it.
Pictures: simple circuits with a battery, a bulb, wires and a switch or a gap.
Wrong answers come from real mistakes: "one wire is enough", "the bulb uses up the electricity
and nothing comes back", "a switch makes electricity".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, line, rect, circle, text, People, INK, SUN

U = Unit(40103)
R = U.R
P = People(R)
COND = ["a steel paper clip", "a copper wire", "an aluminum foil strip", "an iron nail", "a brass key", "a steel spoon", "a coin", "the graphite in a pencil"]
INS = ["a rubber band", "a plastic straw", "a wooden craft stick", "a cotton string", "a glass marble", "a paper strip", "a plastic button", "a crayon"]


def circuit(state="closed", gap=None, lit=None, label=None, dev="bulb"):
    """state: closed / open (switch) / gap (with an object name in the gap) / broken (a wire not attached)."""
    W, H = 300, 190
    s = []
    x0, x1, y0, y1 = 40, 260, 40, 160
    s.append(line(x0, y0, 130, y0, INK, 3) + line(170, y0, x1, y0, INK, 3))   # top wire with bulb gap
    s.append(line(x1, y0, x1, y1, INK, 3))
    if state == "broken":
        s.append(line(x0, y1, 100, y1, INK, 3) + line(100, y1, 138, y1 - 20, INK, 3) + line(160, y1, x1, y1, INK, 3))
    elif state == "open":
        s.append(line(x0, y1, 120, y1, INK, 3) + circle(120, y1, 4, INK, INK, 1) + line(120, y1, 160, y1 - 22, INK, 3)
                 + circle(165, y1, 4, INK, INK, 1) + line(165, y1, x1, y1, INK, 3) + text(142, y1 + 22, "switch", 11, weight=400))
    elif state == "gap":
        s.append(line(x0, y1, 115, y1, INK, 3) + line(185, y1, x1, y1, INK, 3) + rect(115, y1 - 9, 70, 18, "#f3f3f3", INK, 1.5, 4)
                 + text(150, y1 + 26, gap, 11, weight=400))
    else:
        s.append(line(x0, y1, 120, y1, INK, 3) + circle(120, y1, 4, INK, INK, 1) + line(120, y1, 165, y1, INK, 3)
                 + circle(165, y1, 4, INK, INK, 1) + line(165, y1, x1, y1, INK, 3) + text(142, y1 + 22, "switch", 11, weight=400))
    s.append(line(x0, y0, x0, 85, INK, 3) + line(x0, 115, x0, y1, INK, 3))
    s.append(rect(x0 - 14, 85, 28, 30, "#cfcfcf", INK, 2, 3) + rect(x0 - 5, 80, 10, 5, "#999999", INK, 1) + text(x0 + 30, 104, "battery", 11, "start", weight=400))
    on = lit if lit is not None else (state == "closed")
    if dev != "bulb":
        s.append(rect(130, y0 - 16, 40, 30, "#e8f1fb" if dev == "motor" else "#f6dcb4", INK, 2, 4) + text(150, y0 + 3, "M" if dev == "motor" else "B", 14))
        s.append(text(150, y0 + 30, dev, 11, weight=400))
        return svg_wrap(W, H, "".join(s), label or ("circuit with a %s, %s" % (dev, state)))
    if on:
        s.append(circle(150, y0 - 2, 26, "#fff3b0", "none", 0))
    s.append(circle(150, y0 - 2, 15, "#fffbe6" if not on else SUN, INK, 2) + line(130, y0, 136, y0, INK, 3) + line(164, y0, 170, y0, INK, 3))
    s.append(text(150, y0 + 30, "bulb", 11, weight=400))
    return svg_wrap(W, H, "".join(s), label or ("circuit, " + state))


DEV = {"bulb": ("light", "the bulb"), "buzzer": ("buzz", "the buzzer"), "motor": ("spin", "the motor")}


def g_light():
    st = R.choice(["closed", "open", "broken", "gap"])
    dev = R.choice(["bulb", "bulb", "buzzer", "motor"])
    verb, the = DEV[dev]
    will = "Will %s %s?" % (the, verb)
    if st == "gap":
        if R.random() < 0.5:
            ob = R.choice(COND)
            q = fig(circuit("gap", ob, lit=False, dev=dev)) + "%s is placed across the gap. %s" % (ob[0].upper() + ob[1:], will)
            return item(q, "Yes, because it is a conductor and completes the circuit.", ["No, because it is an insulator.", "No, because the battery is off.", "Only if the gap is made wider."],
                        "Metals and graphite let current flow, so the circuit is closed.")
        ob = R.choice(INS)
        q = fig(circuit("gap", ob, lit=False, dev=dev)) + "%s is placed across the gap. %s" % (ob[0].upper() + ob[1:], will)
        return item(q, "No, because it is an insulator and the circuit stays open.", ["Yes, because it completes the circuit.", "Yes, because any object closes a gap.", "Only if it is wet."],
                    "Current cannot flow through an insulator, so the circuit is still open.")
    stem = R.choice(["Look at the circuit. " + will, "In this circuit, " + will[0].lower() + will[1:], will])
    if st == "closed":
        return item(fig(circuit("closed", dev=dev)) + stem, "Yes. The circuit is closed, so current flows all the way around.", ["No. The switch is open.", "No. A wire is loose.", "No. It needs two batteries."],
                    "The path goes from the battery, through %s and back with no gaps." % the)
    if st == "open":
        return item(fig(circuit("open", dev=dev)) + stem, "No. The switch is open, so there is a gap in the path.", ["Yes. The battery is attached.", "Yes. One wire is enough.", "Yes, but weakly."],
                    "An open switch breaks the path. Current cannot flow.")
    return item(fig(circuit("broken", dev=dev)) + stem, "No. A wire is not connected, so the circuit is open.", ["Yes. Most of the wires are connected.", "Yes. The switch is closed.", "Yes, but only for a second."],
                "Every part of the loop must be connected for current to flow.")


def g_fix():
    st = R.choice(["open", "broken", "gap"])
    dev = R.choice(["bulb", "buzzer", "motor"])
    verb, the = DEV[dev]
    if st == "gap":
        ob = R.choice(INS)
        return item(fig(circuit("gap", ob, lit=False, dev=dev)) + "%s is in the gap, and %s does not %s. What change would make it work?" % (ob[0].upper() + ob[1:], the, verb),
                    "Replace it with a metal object, like a paper clip.", ["Replace it with another plastic object.", "Take out the battery.", "Open the switch."],
                    "A conductor in the gap closes the circuit.")
    if st == "open":
        return item(fig(circuit("open", dev=dev)) + "How can you make %s %s?" % (the, verb), "Close the switch.", ["Take out a wire.", "Turn the battery upside down and leave the switch open.", "Add a plastic straw."],
                    "Closing the switch completes the loop.")
    return item(fig(circuit("broken", dev=dev)) + "How can you make %s %s?" % (the, verb), "Connect the loose wire.", ["Open the switch.", "Remove the battery.", "Wrap the wire in tape so it does not touch."],
                "The loose wire leaves a gap. Connect it to close the circuit.")


def g_cond():
    if R.random() < 0.5:
        a = R.choice(COND)
        return item("Which object would complete a circuit if you put it in a gap between two wires?", a, R.sample(INS, 3), "%s conducts electricity." % (a[0].upper() + a[1:]))
    a = R.choice(INS)
    return item("Which object would <b>not</b> let a bulb light if you put it in a gap in a circuit?", a, R.sample(COND, 3), "%s is an insulator." % (a[0].upper() + a[1:]))


B1 = bank([
    ("What is an electric circuit?", "a complete path that electric current can flow around", ["a battery by itself", "a light bulb", "a single wire"],
     "Current flows from the battery, through the parts and back to the battery."),
    ("What does a battery do in a circuit?", "It is the energy source that pushes current around the circuit.", ["It uses up all the current.", "It is a switch.", "It makes light by itself."],
     "The battery stores energy and pushes the current."),
    ("What is a closed circuit?", "a circuit with no gaps, so current can flow", ["a circuit that is turned off", "a circuit in a box", "a circuit with a gap"],
     "Closed means complete: the bulb lights."),
    ("What is an open circuit?", "a circuit with a gap, so current cannot flow", ["a circuit that works", "a circuit with two bulbs", "a circuit with a battery"],
     "A gap, an open switch or a loose wire makes an open circuit."),
    ("What does a switch do?", "It opens or closes the circuit.", ["It makes electricity.", "It stores energy.", "It changes the battery."],
     "Closing the switch completes the path; opening it makes a gap."),
    ("A bulb is connected to a battery with only one wire. Why won't it light?", "There is no complete loop back to the battery.", ["The wire is too short.", "The bulb is too big.", "One wire carries too much current."],
     "Current must flow out of the battery and back into it."),
    ("Which carries energy from a battery to a bulb?", "an electric current in the wires", ["sound in the wires", "air in the wires", "water in the wires"],
     "Electric current carries the energy."),
    ("A flashlight doesn't work with the switch on. What is the most likely problem?", "The batteries are dead or there is a gap in the circuit.", ["The flashlight is too heavy.", "The switch makes too much light.", "Flashlights need sunlight."],
     "Either no energy source or no complete path."),
    ("What turns electrical energy into light in a circuit?", "the bulb", ["the wire", "the switch", "the tape"],
     "In the bulb, electrical energy changes into light (and some heat)."),
    ("Why are wires coated with plastic?", "Plastic is an insulator that keeps the current inside the wire.", ["Plastic makes the current stronger.", "Plastic conducts electricity.", "To make wires heavier."],
     "The metal inside conducts; the plastic outside protects us."),
])
B5 = bank([
    ("Ava's circuit has a battery, a bulb and a buzzer in one loop. She unscrews the bulb. What happens to the buzzer?", "It stops, because the loop is broken.", ["It gets louder.", "It keeps working.", "It lights up."],
     "In a single loop, a break anywhere stops the current everywhere."),
    ("Leo tests 6 objects in a circuit tester. Which result shows an object is a conductor?", "The bulb lights when the object is in the gap.", ["The bulb stays dark.", "The object gets cold.", "The battery gets lighter."],
     "If current flows through it, it is a conductor."),
    ("Why should you never use water near electrical outlets?", "Water with impurities can conduct electricity to your body.", ["Water stops all electricity.", "Water makes outlets louder.", "Water is an insulator."],
     "Tap water conducts electricity and can carry dangerous current."),
    ("Mia adds a second battery to her circuit, and the bulb gets brighter. What does this show?", "More energy is being delivered to the bulb.", ["Batteries make bulbs smaller.", "The circuit is open.", "The bulb is broken."],
     "Two batteries push more current, so more energy reaches the bulb."),
    ("A circuit has a motor that spins a fan. What energy change happens in the motor?", "electrical energy to energy of motion", ["motion to sound only", "light to electrical energy", "heat to electrical energy"],
     "Motors turn electrical energy into motion."),
    ("Noah builds a circuit and the bulb does not light. What is the best first step?", "Check that every connection is tight and the switch is closed.", ["Buy a new house.", "Add more tape everywhere.", "Shake the battery."],
     "Look for gaps in the path first."),
])


def body():
    pics = "<div class='sn-row'>%s%s</div>" % (figure(circuit("closed"), "Closed circuit: the bulb lights."), figure(circuit("open"), "Open switch: no current, no light."))
    think = ("<p>An <b>electric circuit</b> is a complete loop. Current flows from the <b>battery</b>, through wires and a <b>bulb</b> (or buzzer or motor), "
             "and back to the battery. The current carries energy.</p>"
             "<p>A <b>closed circuit</b> has no gaps, so the bulb lights. An <b>open circuit</b> has a gap (an open switch, a loose wire or an insulator), so nothing works.</p>"
             + pics + "<p><b>Conductors</b> (metals, graphite) let current flow. <b>Insulators</b> (plastic, rubber, wood, glass) do not.</p>")
    ex = [("A plastic straw is placed across a gap in a circuit. Does the bulb light?", ["Plastic is an insulator.", "The circuit stays open."], "No."),
          ("A bulb is attached to a battery with one wire. Does it light?", ["Current needs a path out and back."], "No, the loop is not complete.")]
    mist = ["Using one wire. A circuit needs a complete loop.",
            "Thinking any object closes a gap. Only conductors do.",
            "Thinking the switch makes electricity. It only opens or closes the path."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a circuit", B1 + [(g_light, 6), (g_cond, 4)]),
        ("Open or closed?", [(g_light, 14), (g_fix, 6)]),
        ("Conductors and insulators", [(g_cond, 10), (g_light, 10)]),
        ("Fixing circuits", [(g_fix, 12), (g_light, 8)]),
        ("Investigations", B5 + [g_light, g_cond, g_fix]),
    ])
    make("grade-4", "electric-circuits", 3, "4-PS3-2",
         "Make observations to provide evidence that energy can be transferred from place to place by sound, light, heat, and electric currents.",
         "Electric Circuits",
         "Grade 4 Electric Circuits Worksheets: Open and Closed Circuits, Conductors and Insulators",
         "Electric Circuits",
         "Free Grade 4 science worksheets on electric circuits (NGSS 4-PS3-2): batteries, bulbs, switches, open and closed circuits, conductors and insulators, with circuit pictures. 100 practice questions with answers.",
         "Current only flows around a complete, closed circuit.",
         "A battery pushes current through wires to a bulb and back. A gap, an open switch or an insulator stops it.",
         body(),
         [("What is the difference between an open and a closed circuit?", "A closed circuit is a complete loop, so current flows and the bulb lights. An open circuit has a gap, so no current flows."),
          ("What are conductors and insulators?", "Conductors, like metals and graphite, let electric current flow. Insulators, like plastic, rubber, wood and glass, do not."),
          ("Why does a bulb need two connections?", "Current must flow out of the battery, through the bulb and back to the battery. One wire does not make a loop.")],
         sets)


if __name__ == "__main__":
    main()
