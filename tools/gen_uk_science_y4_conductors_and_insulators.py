# -*- coding: utf-8 -*-
"""
UK Year 4 science: Conductors and Insulators (Electricity)
  python tools/gen_uk_science_y4_conductors_and_insulators.py
Electrical conductors and insulators, testing materials in a circuit gap, metals as good conductors, and why
conductors and insulators are used where they are (copper wires in plastic covers, rubber handles).
Reuses the gap question of the Year 6 circuits unit (new seed) and adds Year 4 questions.
Wrong answers come from real mistakes: "all shiny things conduct", "plastic conducts if it is thin",
"water is always safe near electricity", "wood conducts because it comes from trees".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
import gen_uk_science_y6_circuits_and_switches as C6

C6.U = Unit(61413)
C6.R = C6.U.R
C6.P = People(C6.R)
uk_sci.USED.clear()
U, R, P = C6.U, C6.R, C6.P

COND = ["aluminium foil", "copper", "steel", "iron", "graphite (pencil lead)", "brass", "silver", "gold", "tin"]
INS = ["plastic", "wood", "rubber", "glass", "paper", "cotton", "wool", "cork", "pottery"]


def g_mat():
    k = R.random() < 0.5
    m = R.choice(COND if k else INS)
    if not once(("ma", m)):
        return None
    ans = "an electrical conductor" if k else "an electrical insulator"
    return item("Is %s an electrical conductor or an electrical insulator?" % m, ans, ["an electrical insulator" if k else "an electrical conductor", "a light source", "a battery"],
                "Metals (and graphite) conduct electricity; plastic, wood, rubber, glass and fabrics do not.")


OBJ = [("a steel paperclip", True), ("a plastic spoon", False), ("an aluminium can", True), ("a rubber band", False), ("a 1p coin", True), ("a wooden ruler", False),
       ("a key", True), ("a glass marble", False), ("a pencil lead", True), ("a cork", False), ("a foil sweet wrapper", True), ("a paper straw", False)]


def g_test():
    who = P.next()[0]
    rows = R.sample(OBJ, 5)
    nc = sum(1 for _, c in rows if c)
    if nc in (0, 5):
        return None
    k = R.choice(["which", "not", "count", "pattern"])
    if not once(("te", tuple(r[0] for r in rows), k)) or (k == "pattern" and not once(("tp",), 3)):
        return None
    tab = table(["Object put in the gap", "Did the bulb light?"], [[o, "yes" if c else "no"] for o, c in rows])
    intro = tab + "%s tested objects in a gap in a circuit. " % who
    if k == "which":
        a = R.choice([o for o, c in rows if c])
        w = [o for o, c in rows if not c]
        if len(w) < 3:
            return None
        return item(intro + "Which object is an electrical conductor?", a, w[:3], "The bulb lit, so electricity flowed through it.")
    if k == "not":
        a = R.choice([o for o, c in rows if not c])
        w = [o for o, c in rows if c]
        if len(w) < 3:
            return None
        return item(intro + "Which object is an electrical insulator?", a, w[:3], "The bulb did not light, so electricity could not flow through it.")
    if k == "count":
        g = str(nc)
        return item(intro + "How many of the objects were conductors?", g, [str(x) for x in range(6) if x != nc][:3], "Count the yes rows.")
    return item(intro + "What pattern do the results show?", "The objects made of metal let the bulb light.", ["The heaviest objects let the bulb light.", "Only round objects conduct.", "None of the objects conducted."],
                "Metals are good electrical conductors.")


WHY = [("The inside of an electrical wire is made of copper.", "Copper is a good conductor, so electricity flows easily."),
       ("Wires are covered in plastic.", "Plastic is an insulator, so it keeps the electricity in and protects us."),
       ("A plug's pins are made of brass.", "Brass is a metal that conducts electricity into the appliance."),
       ("A plug's case is made of hard plastic.", "Plastic is an insulator, so it is safe to hold."),
       ("Electricians use screwdrivers with rubber or plastic handles.", "The handles are insulators that protect their hands."),
       ("Switches on walls have plastic covers.", "Plastic insulates, so you can press them safely."),
       ("Overhead power cables hang from glass or pottery holders.", "Glass and pottery are insulators, so the electricity does not reach the pylon."),
       ("Circuit boards have thin lines of copper on them.", "Copper conducts electricity between the parts.")]


def g_why():
    s, a = R.choice(WHY)
    if not once(("wh", s)):
        return None
    ins = "insulator" in a
    pool = [x[1] for x in WHY if ("insulator" in x[1]) != ins]
    return item("%s Why?" % s, a, R.sample(pool, 3),
                "Conductors carry electricity where it is needed; insulators keep it from where it is not.")


B1 = bank([
    ("What is an electrical conductor?", "a material that lets electricity flow through it", ["a material that stops electricity", "a person who leads an orchestra only", "a type of battery"], "Metals are conductors."),
    ("What is an electrical insulator?", "a material that does not let electricity flow through it", ["a material that lets electricity flow", "a kind of wire", "a light bulb"], "Plastic is an insulator."),
    ("Which group of materials are usually good electrical conductors?", "metals", ["plastics", "fabrics", "woods"], "Copper, steel, aluminium."),
    ("How can you test if a material is a conductor?", "Put it in a gap in a circuit and see if the bulb lights.", ["Hold it near a magnet.", "Drop it in water.", "Look at its colour."], "A simple tester."),
    ("Is pencil lead (graphite) a conductor?", "Yes, although it is not a metal.", ["No, it is wood.", "No, it is plastic.", "Only when wet."], "A surprising conductor."),
    ("Is a shiny plastic toy a conductor?", "No. Being shiny does not make a material a conductor.", ["Yes, shiny things conduct.", "Yes, if it is silver-coloured.", "Only in sunlight."], "Test, do not guess."),
    ("Why is it dangerous to use electrical things near water?", "Water with things dissolved in it conducts electricity.", ["Water is an insulator.", "Water makes electricity stronger.", "It is never dangerous."], "Keep electricals dry."),
    ("Which part of a wire carries the electricity?", "the metal inside", ["the plastic outside", "the air around it", "the label"], "Usually copper."),
])
B5 = bank([
    ("Why should the same bulb and cell be used for every material tested?", "so only the material changes", ["to make it quicker", "to use more bulbs", "it does not matter"], "Fair test."),
    ("A bulb lit very dimly with one material. What might this show?", "The material conducts, but not very well.", ["It is a perfect insulator.", "The bulb is broken.", "It is a magnet."], "Some materials conduct poorly."),
    ("Why do birds sit safely on a single power line?", "Electricity has no path through the bird to the ground.", ["Birds are insulators.", "Power lines have no electricity.", "Feathers are metal."], "No complete circuit."),
    ("Why is gold used in some electrical connectors?", "It conducts well and does not rust.", ["It is an insulator.", "It is cheap.", "It is magnetic."], "Choose for the job."),
    ("How could you check that your conductor tester works before testing materials?", "Touch the two loose wire ends together: the bulb should light.", ["Test plastic first.", "Remove the cell.", "Open the switch."], "Check equipment."),
])


def body():
    think = ("<p><b>Conductors let electricity flow; insulators do not.</b></p>"
             "<ul><li>Metals (copper, steel, aluminium) and graphite are conductors. Plastic, wood, rubber, glass and fabrics are insulators.</li>"
             "<li>Test a material by putting it in a gap in a circuit: if the bulb lights, it conducts.</li>"
             "<li>Wires have copper inside (conductor) and plastic outside (insulator) to keep us safe.</li></ul>")
    ex = [("A steel key in the gap. Bulb?", ["Steel is a metal conductor"], "lights"),
          ("A rubber band in the gap. Bulb?", ["Rubber is an insulator"], "stays off")]
    mist = ["Thinking all shiny things conduct.", "Thinking plastic conducts if it is thin.", "Using electrical things near water."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Conductors and insulators", B1 + [(g_mat, 12)]),
        ("Which materials conduct?", [(g_mat, 5), (C6.g_cond, 15)]),
        ("Testing materials", [(g_test, 20)]),
        ("Using materials safely", [(C6.g_cond, 14), (g_why, 6)]),
        ("Thinking it through", B5 + [(g_test, 10), (C6.g_cond, 3), (g_why, 2)]),
    ])
    make_uk(4, "conductors-and-insulators", 13, "Electricity",
            "Recognise some common conductors and insulators, and associate metals with being good conductors.",
            "Conductors and Insulators",
            "Year 4 Science: Conductors and Insulators Worksheets (Electricity)",
            "Conductors and Insulators",
            "Free Year 4 science worksheets on electrical conductors and insulators: metals, plastic, rubber and wood, testing materials in a circuit, and using materials safely. 100 questions with answers.",
            "Metals conduct; plastic insulates.",
            "Test a material in a circuit gap: if the bulb lights, it conducts.",
            body(),
            [("What is the difference between a conductor and an insulator?", "A conductor lets electricity flow through it, like copper or steel. An insulator stops electricity flowing, like plastic or rubber."),
             ("How do you test whether a material conducts?", "Put it across a gap in a simple circuit with a cell and a bulb. If the bulb lights, the material is a conductor."),
             ("Why are wires covered in plastic?", "Plastic is an insulator, so it keeps the electricity inside the copper wire and stops it reaching us.")],
            sets)


if __name__ == "__main__":
    main()
