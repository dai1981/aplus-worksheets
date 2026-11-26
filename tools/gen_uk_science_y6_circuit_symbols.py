# -*- coding: utf-8 -*-
"""
UK Year 6 science: Circuit Symbols and Diagrams (Electricity)
  python tools/gen_uk_science_y6_circuit_symbols.py
The recognised symbols for a cell, battery, lamp, open and closed switch, buzzer, motor and wire; reading circuit
diagrams (drawn new each time) and describing them; and why scientists use symbols.
Wrong answers come from real mistakes: "a lamp symbol is a plain circle", "a battery is the same as one cell",
"an open switch lets current flow", "counting the two lines of a cell as two cells".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, People, once, fig
from uk_sci_pics import symbol, circuit

U = Unit(61613)
R = U.R
P = People(R)

NAME = {"cell": "a cell", "battery": "a battery (two or more cells)", "lamp": "a lamp (bulb)", "switch_open": "an open switch",
        "switch_closed": "a closed switch", "buzzer": "a buzzer", "motor": "a motor"}
DESC = {"cell": "a long thin line next to a short thick line", "battery": "two cell symbols joined together",
        "lamp": "a circle with a cross inside", "switch_open": "a line lifted up away from a contact (a gap in the wire)",
        "switch_closed": "a line joining two dots, with no gap", "buzzer": "a half circle on the wire", "motor": "a circle with the letter M inside"}


def g_sym():
    n = R.choice(sorted(NAME))
    q = R.choice(["What does this circuit symbol show?", "Which component does this symbol stand for?"])
    if not once(("sy", n, q)):
        return None
    w = R.sample([NAME[x] for x in NAME if x != n], 3)
    return item(fig(symbol(n, "circuit symbol")) + q, NAME[n], w, "%s is drawn as %s." % (NAME[n][0].upper() + NAME[n][1:], DESC[n]))


def g_desc():
    n = R.choice(sorted(NAME))
    k = R.random() < 0.5
    if not once(("de", n, k)):
        return None
    if k:
        return item("Which component has a symbol that is %s?" % DESC[n], NAME[n], R.sample([NAME[x] for x in NAME if x != n], 3), "Learn each symbol's shape.")
    return item("How is %s drawn in a circuit diagram?" % NAME[n].split(" (")[0], "as " + DESC[n], R.sample(["as " + DESC[x] for x in DESC if x != n], 3), "Learn each symbol's shape.")


PARTS = ["lamp", "buzzer", "motor", "switch_open", "switch_closed"]
WORD = {"cell": ("cell", "cells"), "battery": ("battery", "batteries"), "lamp": ("lamp", "lamps"), "switch_open": ("open switch", "open switches"),
        "switch_closed": ("closed switch", "closed switches"), "buzzer": ("buzzer", "buzzers"), "motor": ("motor", "motors")}
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def rand_circuit():
    nc = R.choice([1, 1, 2, 2, 3])
    other = R.sample(PARTS, R.choice([1, 2])) if R.random() < 0.5 else [R.choice(PARTS)] * R.choice([1, 2])
    if "switch_open" in other and "switch_closed" in other:
        other.remove("switch_closed")
    if not any(x in other for x in ("lamp", "buzzer", "motor")):
        other.append(R.choice(["lamp", "buzzer", "motor"]))
    comps = ["cell"] * nc + other
    R.shuffle(comps)
    top = comps[:(len(comps) + 1) // 2]
    bot = comps[(len(comps) + 1) // 2:]
    return comps, top, bot


def describe(comps):
    from collections import Counter
    c = Counter(comps)
    order = [k for k in ["cell", "battery", "lamp", "buzzer", "motor", "switch_open", "switch_closed"] if c[k]]
    parts = ["%s %s" % (NUM[c[k]], WORD[k][0] if c[k] == 1 else WORD[k][1]) for k in order]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def g_read():
    comps, top, bot = rand_circuit()
    from collections import Counter
    c = Counter(comps)
    key = tuple(sorted(c.items()))
    if not once(("rd", key)):
        return None
    a = describe(comps)
    wrong = set()
    for k in list(c):
        for d in (-1, 1):
            cc = list(comps)
            if d < 0:
                cc.remove(k)
                if not cc or "cell" not in cc:
                    continue
            else:
                cc.append(k)
            wrong.add(describe(cc))
    if "switch_open" in c:
        wrong.add(describe([x if x != "switch_open" else "switch_closed" for x in comps]))
    if c["cell"] >= 2:
        wrong.add(describe([x for x in comps if x != "cell"] + ["cell"] * (c["cell"] * 2)))
    wrong.discard(a)
    if len(wrong) < 3:
        return None
    return item(fig(circuit(top, bot, "circuit diagram")) + "Which list describes the components in this circuit?", a, R.sample(sorted(wrong), 3),
                "Count each symbol. A single cell is one long line and one short line.")


def g_count():
    comps, top, bot = rand_circuit()
    k = R.choice(sorted(set(comps)))
    n = comps.count(k)
    if not once(("co", tuple(top), tuple(bot), k)):
        return None
    w = [str(x) for x in (0, 1, 2, 3, 4) if x != n][:3] if n > 0 else ["1", "2", "3"]
    if k == "cell":
        w = [str(n * 2)] + [x for x in w if x != str(n * 2)][:2]
    return item(fig(circuit(top, bot, "circuit diagram")) + "How many %s are in this circuit?" % WORD[k][1], str(n), w,
                "Count the symbols for %s." % WORD[k][1] if k != "cell" else "Each cell has one long and one short line: count pairs, not lines.")


def g_flow():
    comps, top, bot = rand_circuit()
    if not once(("fl", tuple(top), tuple(bot))):
        return None
    opn = "switch_open" in comps
    a = "No, the open switch makes a gap in the circuit." if opn else "Yes, the circuit is a complete loop."
    w = ["Yes, the circuit is a complete loop." if opn else "No, the open switch makes a gap in the circuit.",
         "No, a circuit needs at least two cells.", "Yes, but only through the wires on the bottom."]
    return item(fig(circuit(top, bot, "circuit diagram")) + "Will a current flow in this circuit?", a, w, "Current flows only when there is a complete loop with no gaps.")


B1 = bank([
    ("Why do scientists use symbols for circuit diagrams?", "Symbols are quick to draw and understood by everyone, in any language.", ["Symbols look prettier than pictures.", "Pictures are not allowed.", "Symbols make circuits work better."], "Clear and universal."),
    ("In a circuit diagram, how are wires drawn?", "as straight lines", ["as wavy lines", "as dotted circles", "as arrows"], "Use a ruler."),
    ("What is the difference between a cell and a battery?", "A battery is two or more cells joined together.", ["They are the same thing.", "A cell is bigger than a battery.", "A battery has no energy."], "We often call one cell a battery in everyday life."),
    ("In a cell symbol, which line shows the positive side?", "the long thin line", ["the short thick line", "both lines", "neither line"], "Long line = positive (+)."),
    ("Which symbol shows a component that makes light?", "a circle with a cross inside", ["a circle with M inside", "a half circle", "a long and a short line"], "That is a lamp."),
    ("What does an open switch do in a circuit?", "makes a gap so current cannot flow", ["makes the lamp brighter", "adds more cells", "joins two circuits"], "Open = off."),
    ("What does a closed switch do in a circuit?", "completes the loop so current can flow", ["breaks the circuit", "stores electricity", "makes a sound"], "Closed = on."),
    ("Which tool helps you draw neat circuit diagrams?", "a ruler", ["a protractor only", "a thermometer", "a magnifying glass"], "Straight lines with corners."),
])
B5 = bank([
    ("A pupil draws a lamp as a plain circle. Why is this a problem?", "Others may not know it is a lamp; the lamp symbol has a cross inside.", ["There is no problem.", "A plain circle means battery.", "Lamps have no symbol."], "Use recognised symbols."),
    ("Why must a circuit diagram show a complete loop?", "Current only flows around a complete circuit.", ["To make it look neat.", "Diagrams are always loops.", "Current flows in straight lines only."], "No gaps."),
    ("A torch has two cells, a switch and a lamp. Which diagram list matches it?", "two cells, one switch and one lamp", ["one cell, two switches and one lamp", "two lamps and one cell", "one motor and one buzzer"], "Match each part."),
    ("Why do electricians in different countries understand the same diagram?", "They all use the same recognised symbols.", ["They all speak English.", "Diagrams are written as sentences.", "They guess."], "International symbols."),
    ("How would you show a motor in a circuit diagram?", "as a circle with the letter M inside", ["as a circle with a cross", "as a half circle", "as a long and short line"], "M for motor."),
])


def body():
    think = ("<p><b>Circuit diagrams use recognised symbols so everyone can read them.</b></p>"
             "<ul><li>Cell: long thin line (+) and short thick line. Battery: two or more cells joined.</li>"
             "<li>Lamp: circle with a cross. Buzzer: half circle. Motor: circle with M. Switch: open (gap) or closed.</li>"
             "<li>Wires are straight lines. Current flows only around a complete loop.</li></ul>")
    ex = [("A circle with a cross inside?", ["Symbol for a light"], "a lamp"),
          ("Open switch in the loop: does current flow?", ["There is a gap"], "No")]
    mist = ["Drawing a lamp as a plain circle.", "Counting the two lines of one cell as two cells.", "Thinking an open switch lets current flow."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The symbols", B1 + [(g_sym, 8), (g_desc, 4)]),
        ("Naming symbols", [(g_sym, 4), (g_desc, 10), (g_count, 6)]),
        ("Reading diagrams", [(g_count, 12), (g_read, 8)]),
        ("Describing circuits", [(g_read, 12), (g_flow, 8)]),
        ("Using diagrams", B5 + [(g_flow, 6), (g_read, 4), (g_count, 5)]),
    ])
    make_uk(6, "circuit-symbols", 13, "Electricity",
            "Use recognised symbols when representing a simple circuit in a diagram.",
            "Circuit Symbols and Diagrams",
            "Year 6 Science: Circuit Symbols Worksheets (Cells, Lamps, Switches, Buzzers, Motors)",
            "Circuit Symbols",
            "Free Year 6 science worksheets on circuit symbols and diagrams: cells, batteries, lamps, switches, buzzers and motors, reading and describing circuit diagrams. 100 questions with answers.",
            "Symbols make circuits easy to read.",
            "Cell, lamp, switch, buzzer, motor: one shape each, joined by straight wires.",
            body(),
            [("Why do we use circuit symbols?", "They are quicker to draw than pictures and every scientist and electrician recognises them, whatever language they speak."),
             ("What is the symbol for a cell?", "A long thin line (the positive side) and a short thick line next to it. Two or more cells joined make a battery."),
             ("How do you show a switch?", "An open switch is drawn with the line lifted away from the contact, leaving a gap. A closed switch is drawn as a line joining the two dots.")],
            sets)


if __name__ == "__main__":
    main()
