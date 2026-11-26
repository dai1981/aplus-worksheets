# -*- coding: utf-8 -*-
"""
UK Year 6 science: Circuits and Switches (Electricity)
  python tools/gen_uk_science_y6_circuits_and_switches.py
Explaining whether components work: complete loops, open and closed switches, two switches in series, gaps,
conductors and insulators in a gap, and finding faults (dead cell, broken bulb, loose wire).
Wrong answers come from real mistakes: "one closed switch is enough when there are two in series",
"a plastic ruler can complete a circuit", "a lamp works with only one wire", "a dead cell still lights a lamp".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig
from uk_sci_pics import circuit

U = Unit(61615)
R = U.R
P = People(R)

LOAD = ["lamp", "buzzer", "motor"]
WORK = {"lamp": "light up", "buzzer": "buzz", "motor": "spin"}


def g_work():
    who = P.next()[0]
    load = R.choice(LOAD)
    kind = R.choice(["ok", "open", "gap", "nocell", "ok2"])
    nc = R.choice([1, 2])
    top = ["cell"] * nc if kind != "nocell" else ["wire"]
    bot = [load]
    if kind == "open":
        bot.append("switch_open")
    elif kind == "gap":
        bot.append("gap")
    elif kind in ("ok", "ok2"):
        bot.append("switch_closed")
    if kind == "nocell":
        bot.append("switch_closed")
    R.shuffle(bot)
    if not once(("wk", who, load, kind)):
        return None
    ans = {"ok": "Yes, the loop is complete and the switch is closed.", "ok2": "Yes, the loop is complete and the switch is closed.",
           "open": "No, the switch is open so there is a gap.", "gap": "No, there is a gap in the wire.", "nocell": "No, there is no cell to push the current."}[kind]
    allw = ["Yes, the loop is complete and the switch is closed.", "No, the switch is open so there is a gap.", "No, there is a gap in the wire.", "No, there is no cell to push the current."]
    return item(fig(circuit(top, bot, "circuit diagram")) + "%s draws this circuit. Will the %s %s?" % (who, load, WORK[load]), ans, [x for x in allw if x != ans],
                "A component works only in a complete loop with a cell and no gaps.")


def g_two():
    who = P.next()[0]
    a, b = R.choice([0, 1]), R.choice([0, 1])
    load = R.choice(LOAD)
    if not once(("tw", a, b, load, who)) or not once(("twc", a, b, load), 2):
        return None
    top = ["cell", "cell"]
    bot = ["switch_closed" if a else "switch_open", load, "switch_closed" if b else "switch_open"]
    st = lambda x: "closed" if x else "open"
    on = a and b
    ans = "Yes, both switches are closed." if on else "No, at least one switch is open."
    w = ["No, at least one switch is open." if on else "Yes, both switches are closed.", "Yes, one closed switch is enough.", "No, two switches can never work together."]
    return item(fig(circuit(top, bot, "circuit with two switches")) + "In %s's circuit, the left switch is %s and the right switch is %s. Will the %s %s?" % (who, st(a), st(b), load, WORK[load]),
                ans, w, "With two switches in one loop, both must be closed for current to flow.")


COND = ["a steel paperclip", "an aluminium can", "a copper wire", "a brass key", "an iron nail", "a metal spoon", "a 2p coin"]
INS = ["a plastic ruler", "a rubber band", "a wooden lolly stick", "a glass marble", "a cotton thread", "a paper straw", "a pencil eraser"]


def g_cond():
    k = R.random() < 0.6
    if k:
        a = R.choice(COND)
        w = R.sample(INS, 3)
        if not once(("cd", a), 3):
            return None
        o = sorted([a] + w)
        return item("A lamp will not light because there is a gap in its circuit. Which object placed across the gap would make it light: %s or %s?" % (", ".join(o[:3]), o[3]), a, w,
                    "Metals are electrical conductors; they let current flow.")
    a = R.choice(INS)
    w = R.sample(COND, 3)
    if not once(("in", a), 3):
        return None
    o = sorted([a] + w)
    return item("Which object placed across a gap in a circuit would NOT let the lamp light: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "%s is an electrical insulator." % (a[0].upper() + a[1:]))


FAULT = [("The lamp worked yesterday, but today it will not light. A new cell makes it work.", "The old cell had run out."),
         ("The cell is new, the wires are fine, but the lamp will not light. The thin wire inside the bulb is broken.", "The bulb has blown."),
         ("A wire has come off one side of the lamp holder.", "There is a gap, so the circuit is not complete."),
         ("Everything is joined up, but the switch is in the off position.", "The switch is open, so current cannot flow."),
         ("A plastic paperclip has been used to join two wires.", "Plastic is an insulator, so it blocks the current."),
         ("Two cells are both facing the same way, but the lamp still will not light. One cell is very old.", "One cell is flat, so there is not enough voltage."),
         ("The lamp lights very dimly with one cell and six lamps in a row.", "Six lamps share the voltage of one cell, so each gets very little.")]


def g_fault():
    s, a = R.choice(FAULT)
    if not once(("fa", s)):
        return None
    lead = "" if s.startswith("The lamp") else "A lamp in a circuit will not light. "
    return item("%s%s What is the most likely reason?" % (lead, s), a, R.sample([x[1] for x in FAULT if x[1] != a], 3), "Check: cells, bulb, every connection, switches and materials.")


B1 = bank([
    ("What does a circuit need for a lamp to light?", "a cell and a complete loop of wires with no gaps", ["only a lamp", "one wire from the cell to the lamp", "a switch and no cell"], "A complete circuit."),
    ("What does a switch do?", "opens or closes a gap in the circuit to turn it off or on", ["makes the lamp brighter", "stores electricity", "changes the cell's voltage"], "On and off."),
    ("When a switch is closed, what happens?", "The circuit is complete and current flows.", ["The circuit has a gap.", "The cell stops working.", "The lamp gets dimmer."], "Closed = on."),
    ("Which materials are good electrical conductors?", "metals", ["plastics", "rubber", "wood"], "Copper is used in wires."),
    ("Why are wires covered in plastic?", "Plastic is an insulator, so it stops the current reaching our hands.", ["Plastic makes the current faster.", "Plastic is a conductor.", "To make wires heavier."], "Safety."),
    ("What is the job of the cell in a circuit?", "to push the current around the circuit", ["to switch the circuit off", "to make the wires longer", "to stop current"], "It provides the voltage."),
    ("Why does a lamp go out when a wire is disconnected?", "There is now a gap, so the circuit is not complete.", ["The lamp gets too hot.", "The cell gets bigger.", "The switch closes."], "Current needs a loop."),
    ("A torch has a switch on its side. What does pressing it do?", "closes the gap so the lamp lights", ["adds a new cell", "changes the lamp's colour", "makes the torch heavier"], "Switches control circuits."),
])
B5 = bank([
    ("How could you use a circuit to test whether a material conducts electricity?", "Put the material across a gap in a lamp circuit and see if the lamp lights.", ["Weigh the material.", "Hold it near a magnet.", "Put it in water."], "Conductor tester."),
    ("Why does a car have a switch for each light rather than one for everything?", "so each light can be controlled on its own", ["to save metal", "because switches make cars faster", "it does not need switches"], "Separate control."),
    ("A pupil's lamp flickers when the wires are wiggled. What should they check?", "that every connection is tight", ["the colour of the wires", "the weather", "the lamp's price"], "Loose connections."),
    ("A buzzer is quiet compared with yesterday, with the same circuit. Why?", "The cells are running low.", ["The buzzer is new.", "The switch is closed.", "Buzzers always get quieter on Tuesdays."], "Voltage drops as cells run down."),
    ("Why should you never put metal objects into a plug socket?", "Metal conducts electricity, so mains current could flow through you.", ["Metal is an insulator.", "Sockets are made of metal.", "It would charge the object."], "Safety."),
])


def body():
    think = ("<p><b>A component works only in a complete loop that has a cell and no gaps.</b></p>"
             "<ul><li>A closed switch completes the loop; an open switch makes a gap. With two switches in one loop, both must be closed.</li>"
             "<li>Metals conduct electricity; plastic, rubber, wood and glass are insulators.</li>"
             "<li>If something does not work, check the cells, the bulb, each connection, the switches and the materials.</li></ul>")
    ex = [("Two switches in a loop: one open, one closed. Lamp?", ["The open switch makes a gap"], "off"),
          ("A plastic ruler across a gap. Lamp?", ["Plastic is an insulator"], "off")]
    mist = ["Thinking one closed switch is enough when there are two in the loop.", "Thinking plastic can complete a circuit.", "Forgetting that cells run out."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Complete circuits", B1 + [(g_work, 8), (g_cond, 4)]),
        ("Will it work?", [(g_work, 16), (g_cond, 4)]),
        ("Switches", [(g_two, 14), (g_work, 6)]),
        ("Conductors and faults", [(g_cond, 10), (g_fault, 7), (g_two, 3)]),
        ("Fixing circuits", B5 + [(g_work, 6), (g_two, 6), (g_cond, 3)]),
    ])
    make_uk(6, "circuits-and-switches", 15, "Electricity",
            "Compare and give reasons for variations in how components function, including the brightness of bulbs, the loudness of buzzers and the on/off position of switches.",
            "Circuits and Switches",
            "Year 6 Science: Circuits and Switches Worksheets (Will It Work? Conductors and Faults)",
            "Circuits and Switches",
            "Free Year 6 science worksheets on circuits and switches: complete circuits, open and closed switches, two switches in series, conductors and insulators, and finding faults. 100 questions with answers.",
            "No gaps, no current.",
            "A complete loop with a cell and closed switches makes components work.",
            body(),
            [("Why does a switch turn a lamp off?", "Opening the switch makes a gap in the circuit, so current cannot flow around the loop and the lamp goes out."),
             ("What happens with two switches in one circuit?", "If both are in the same loop (in series), both must be closed for the lamp to light. Opening either one breaks the circuit."),
             ("Why won't my lamp light?", "Check that the cell is not flat, the bulb is not blown, every wire is firmly connected, the switch is closed and nothing in the loop is an insulator.")],
            sets)


if __name__ == "__main__":
    main()
