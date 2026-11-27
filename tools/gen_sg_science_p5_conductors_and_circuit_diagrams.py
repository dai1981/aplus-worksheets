# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Conductors of electricity and circuit diagrams (Energy)
  python tools/gen_sg_science_p5_conductors_and_circuit_diagrams.py
Electrical conductors (metals such as copper, iron and aluminium, and graphite) let electricity flow; electrical insulators
(plastic, rubber, wood, glass, cloth) do not. Testing materials in a circuit tester; uses of conductors and insulators for
safety. Circuit diagrams use symbols for batteries, bulbs, switches and wires. UK Year 4 and Year 6 conductor and
circuit-symbol questions are reused with Singapore names; a circuit-tester table and a material classifier are written here.
Wrong answers come from real mistakes: "all shiny things conduct", "pencil lead is an insulator because pencils are wood",
"a battery symbol is the same as a bulb symbol", "water never conducts electricity".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto
import uk_sci_pics as K

U = Unit(63509)
R = U.R
P = People(R)
REP = [(r"\b\d+p coins?\b", "10-cent coin"), (r"lolly stick", "ice-cream stick")]
DROP = ["volt", " V ", " V.", "dB", "decibel", "winter", "snow", "pottery"]
CI = use(U, "gen_uk_science_y4_conductors_and_insulators", rep=REP, drop=DROP)
CS = use(U, "gen_uk_science_y6_circuits_and_switches", rep=REP, drop=DROP)
SY = use(U, "gen_uk_science_y6_circuit_symbols", rep=REP, drop=DROP)

COND = ["a copper wire", "an iron nail", "an aluminium foil strip", "a steel paper clip", "a pencil lead (graphite)", "a brass key", "a stainless steel spoon", "a 10-cent coin"]
INS = ["a plastic ruler", "a rubber band", "a wooden ice-cream stick", "a glass marble", "a cotton thread", "a paper strip", "a ceramic tile", "a plastic straw"]


def g_pick():
    k = R.choice(["c", "i"])
    a = R.choice(COND if k == "c" else INS)
    if not once(("pk", a)):
        return None
    if k == "c":
        return item("Which of these is an electrical conductor?", a, R.sample(INS, 3), "%s lets electricity flow through it." % (a[0].upper() + a[1:]))
    return item("Which of these is an electrical insulator?", a, R.sample(COND, 3), "%s does not let electricity flow through it." % (a[0].upper() + a[1:]))


def g_tester():
    objs = R.sample(COND, 2) + R.sample(INS, 2)
    R.shuffle(objs)
    k = R.choice(["count", "cond", "ins", "concl", "var"])
    key = tuple(sorted(objs))
    if not once(("ts", k, key)) or not once(("tsn", k), 1 if k in ("concl", "var") else 3):
        return None
    tb = table(["Object placed in the gap", "Did the bulb light?"], [[o, "yes" if o in COND else "no"] for o in objs])
    q0 = "%s placed objects one at a time across the gap in a circuit tester.<br>%s" % (P.next()[0], tb)
    if k == "count":
        return item(q0 + "How many objects are electrical conductors?", "2", ["0", "1", "4"], "The bulb lit for 2 objects.")
    if k == "cond":
        c = [o for o in objs if o in COND]
        return item(q0 + "Which object is an electrical conductor?", c[0], [o for o in objs if o not in COND] + ["none of them"], "The bulb lit when it was in the gap.")
    if k == "ins":
        i = [o for o in objs if o in INS]
        return item(q0 + "Which object is an electrical insulator?", i[0], [o for o in objs if o in COND] + ["all of them"], "The bulb did not light when it was in the gap.")
    if k == "concl":
        return item(q0 + "What can be concluded?", "Objects made of metal or graphite let electricity pass through.", ["All objects let electricity pass through.", "Only plastic objects conduct electricity.", "Shiny objects never conduct electricity."],
                    "The bulb lit only for the conductors.")
    return item(q0 + "Why should the same battery and bulb be used for every object?", "so that only the object being tested is changed", ["to make the bulb brighter", "to save time", "to make the objects conduct"],
                "This makes the test fair.")


USES = [("the metal pins of a plug", "conductor", "They must let electricity flow into the appliance."), ("the plastic case of a plug", "insulator", "It stops electricity reaching your hand."),
        ("the copper inside a wire", "conductor", "Electricity must flow through the wire."), ("the plastic covering of a wire", "insulator", "It stops electric shocks and short circuits."),
        ("the rubber gloves of an electrician", "insulator", "They protect the electrician from shocks."), ("the metal contacts in a battery holder", "conductor", "They connect the battery to the circuit."),
        ("the plastic handle of a screwdriver for electrical work", "insulator", "It protects the hand."), ("the metal filament inside a bulb", "conductor", "Current flows through it and makes it glow.")]


def g_use():
    thing, a, e = R.choice(USES)
    if not once(("us", thing)):
        return None
    if a == "conductor":
        return item("Why is %s made of a conductor?" % thing, "to let electricity flow through", ["to stop electricity from flowing", "to make it lighter", "to make it waterproof"], e)
    return item("Why is %s made of an insulator?" % thing, "to stop electricity from flowing through", ["to let electricity flow through", "to make it heavier", "to make it shiny"], e)


def g_draw():
    comps = R.choice([(["cell"], ["lamp"]), (["cell", "cell"], ["lamp"]), (["battery", "switch_closed"], ["lamp"]), (["cell", "switch_open"], ["lamp"]),
                      (["cell"], ["lamp", "lamp"]), (["cell", "cell", "switch_closed"], ["lamp", "buzzer"]), (["battery"], ["motor"]), (["cell", "switch_open"], ["buzzer"])])
    top, bot = comps
    k = R.choice(["works", "cells", "bulbs"])
    if not once(("dr", tuple(top), tuple(bot), k)) or not once(("drn", k), 4):
        return None
    svg = "<div class='qfig'>%s</div>" % K.circuit(top, bot)
    works = "switch_open" not in top
    if k == "works":
        return item(svg + "Will a current flow in this circuit?", "Yes, it is a closed circuit." if works else "No, the switch is open.",
                    ["No, the switch is open." if works else "Yes, it is a closed circuit.", "No, there is no battery.", "Yes, but only through the switch."],
                    "Look for gaps and open switches.")
    if k == "cells":
        n = top.count("cell") + 2 * top.count("battery")
        return item(svg + "How many cells (single batteries) does this circuit have?", str(n), [str(x) for x in range(0, 5) if x != n][:3],
                    "A battery symbol is drawn as two or more cells joined.")
    n = bot.count("lamp")
    return item(svg + "How many bulbs are in this circuit?", str(n), [str(x) for x in range(0, 4) if x != n][:3], "The bulb symbol is a circle with a cross.")


B1 = bank([
    ("What is an electrical conductor?", "a material that allows electricity to flow through it", ["a material that stops electricity", "a battery", "a switch that is open"], "Metals are good electrical conductors."),
    ("What is an electrical insulator?", "a material that does not allow electricity to flow through it", ["a material that lets electricity flow", "a kind of bulb", "a source of electricity"], "Plastic and rubber are insulators."),
    ("Which group of materials are good electrical conductors?", "metals", ["plastics", "woods", "fabrics"], "Copper, iron and aluminium conduct electricity."),
    ("Which non-metal is a good electrical conductor?", "graphite (pencil lead)", ["plastic", "rubber", "glass"], "Graphite is a non-metal that conducts electricity."),
    ("Why are electric wires covered with plastic?", "Plastic is an insulator and prevents electric shocks.", ["Plastic is a conductor.", "Plastic makes the wire heavier.", "Plastic makes electricity flow faster."], "The copper inside conducts; the plastic outside insulates."),
    ("Why is tap water dangerous near electricity?", "Tap water can conduct electricity.", ["Tap water is an insulator.", "Water makes electricity stop.", "Water turns into electricity."], "Never use electrical appliances with wet hands."),
])
B2 = bank([
    ("Why do we use symbols in circuit diagrams?", "They are simple and understood by everyone.", ["They look nicer than pictures.", "They make circuits work.", "They show the colour of the wires."], "Symbols are a standard way to draw circuits."),
    ("How are wires shown in a circuit diagram?", "as straight lines", ["as wavy lines", "as dotted circles", "as arrows"], "Wires are drawn as straight lines with corners."),
    ("How is a bulb shown in a circuit diagram?", "as a circle with a cross inside", ["as a long line and a short line", "as a circle with M inside", "as a broken line"], "This is the bulb symbol."),
    ("How is a cell (one battery) shown?", "as a long thin line next to a short thick line", ["as a circle with a cross", "as two dots", "as a zigzag"], "Two or more cells joined make a battery."),
    ("How is an open switch shown?", "as a line that is lifted, leaving a gap", ["as a circle with a cross", "as a long and short line", "as a closed straight line"], "The gap means no current flows."),
    ("In a circuit diagram, two cells are joined end to end. What do they show?", "a battery of two cells in series", ["two bulbs", "an open switch", "a motor"], "More cells in series give a bigger push."),
])
B5 = bank([
    ("Siti tested a pencil lead in a circuit tester and the bulb lit dimly. What does this show?", "Graphite conducts electricity, but not as well as copper.", ["Graphite is an insulator.", "The bulb is broken.", "The pencil lead is a magnet."], "A dim bulb shows a weaker conductor."),
    ("Ravi wants to find out which material is the best conductor. What should he observe?", "how bright the bulb is with each material", ["the colour of each material", "the mass of each material", "the length of the wires"], "A brighter bulb shows a better conductor."),
    ("Mei Ling put a plastic ruler in the gap of a circuit tester. The bulb did not light. Which is the best conclusion?", "Plastic is an electrical insulator.", ["The battery is flat.", "Plastic is a conductor.", "The bulb is too bright."], "Check that the tester works with a metal first."),
    ("Why should a pupil first test the circuit tester with a metal paper clip?", "to check that the battery and bulb are working", ["to make the clip magnetic", "to warm up the bulb", "to use up the battery"], "This is a control to check the circuit."),
    ("A switch is made of a strip of metal that can be pressed down to touch another metal strip. Why are the strips metal?", "Metal conducts electricity, so the circuit closes when they touch.", ["Metal is an insulator.", "Metal is cheap.", "Metal is shiny."], "A switch must conduct when closed."),
])


def body():
    think = ("<p><b>Electrical conductors let electricity flow; electrical insulators do not.</b></p>"
             "<ul><li>Conductors: metals (copper, iron, aluminium, steel) and graphite.</li>"
             "<li>Insulators: plastic, rubber, wood, glass, cloth and paper.</li>"
             "<li>Use a <b>circuit tester</b>: if the bulb lights when the object is in the gap, the object is a conductor.</li>"
             "<li><b>Circuit diagrams</b> use symbols: a cell (long thin line and short thick line), a bulb (circle with a cross), a switch (gap or closed line), wires (straight lines).</li></ul>")
    ex = [("A steel paper clip makes the bulb in a tester light. What is it?", ["The bulb lit", "Current flowed through the clip"], "A conductor."),
          ("Why is a plug's case plastic but its pins metal?", ["Pins must conduct", "The case must protect your hand"], "Metal conducts; plastic insulates.")]
    mist = ["Thinking all shiny things conduct. A shiny plastic button does not.",
            "Thinking pencil lead is an insulator because the pencil is wood. Graphite conducts.",
            "Mixing up the cell symbol and the bulb symbol.",
            "Thinking water never conducts. Tap water can conduct and is dangerous near electricity."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Conductors and insulators", B1 + [(g_pick, 8), (CI.g_mat, 4), (CS.g_cond, 2)]),
        ("Using conductors and insulators", CI.B1 + [(g_use, 7), (CI.g_why, 4), (g_pick, 4), (CS.g_cond, 3)]),
        ("Circuit symbols", B2 + SY.B1 + [(SY.g_sym, 5), (SY.g_desc, 4), (SY.g_count, 2)]),
        ("Reading circuit diagrams", SY.B5 + [(g_draw, 6), (SY.g_read, 5), (SY.g_flow, 2), (CS.g_work, 3), (SY.g_count, 2)]),
        ("PSLE-style experiments", B5 + CI.B5 + [(g_tester, 6), (CI.g_test, 4), (CS.g_fault, 3)]),
    ])
    make_sg(5, "conductors-and-circuit-diagrams", 9, "Energy", "Energy forms and uses (Electrical systems: conductors, insulators and circuit diagrams)",
            "Identify electrical conductors and insulators and relate their uses to electrical safety. Test whether materials conduct electricity, and draw and "
            "read circuit diagrams using symbols for batteries, bulbs, switches and wires (summary of the MOE Primary Science Syllabus).",
            "Conductors, Insulators and Circuit Diagrams",
            "Primary 5 Science: Electrical Conductors and Circuit Diagrams Worksheets (with Answers)",
            "Conductors and circuit diagrams",
            "Free Primary 5 science worksheets for Singapore pupils on electrical conductors and insulators, circuit testers, uses for safety, and circuit diagram symbols. 100 questions with answers.",
            "Conductors let electricity flow; insulators do not.",
            "Circuit diagrams use symbols for each component.",
            body(),
            [("Which materials are electrical conductors?", "Metals such as copper, iron, aluminium and steel, and graphite (pencil lead)."),
             ("How do I test if a material conducts electricity?", "Put it across the gap in a circuit with a battery and a bulb. If the bulb lights, the material is a conductor."),
             ("Why do we use symbols in circuit diagrams?", "Symbols are quick to draw and everyone understands them, so circuits can be shared and built correctly.")],
            sets)


if __name__ == "__main__":
    main()
