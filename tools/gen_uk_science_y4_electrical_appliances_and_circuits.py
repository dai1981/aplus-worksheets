# -*- coding: utf-8 -*-
"""
UK Year 4 science: Electrical Appliances and Circuits (Electricity)
  python tools/gen_uk_science_y4_electrical_appliances_and_circuits.py
Appliances that run on mains electricity or batteries, staying safe with electricity, the parts of a simple series
circuit (cells, wires, bulbs, switches, buzzers), whether a bulb will light, and what a switch does.
Reuses the circuit-diagram question of the Year 6 unit (new seed) and adds Year 4 questions.
Wrong answers come from real mistakes: "a bulb lights with one wire", "a switch makes a bulb brighter",
"all appliances use batteries", "it is safe to touch plugs with wet hands".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
import gen_uk_science_y6_circuits_and_switches as C6

C6.U = Unit(61412)
C6.R = C6.U.R
C6.P = People(C6.R)
uk_sci.USED.clear()
U, R, P = C6.U, C6.R, C6.P

APP = [("a kettle", "mains"), ("a toaster", "mains"), ("a fridge", "mains"), ("a washing machine", "mains"), ("a television", "mains"), ("an oven", "mains"),
       ("a torch", "battery"), ("a TV remote control", "battery"), ("a wristwatch", "battery"), ("a smoke alarm", "battery"), ("a calculator", "battery"),
       ("a mobile phone (when not plugged in)", "battery"), ("a hairdryer", "mains"), ("a hand-held games console", "battery")]
NOEL = ["a pencil", "a bicycle", "a skipping rope", "a book", "a wooden spoon", "scissors", "a football", "a teddy bear"]


def g_app():
    a, t = R.choice(APP)
    if not once(("ap", a)):
        return None
    ans = "mains electricity (a plug in the wall)" if t == "mains" else "batteries (cells)"
    return item("Does %s usually run on mains electricity or on batteries?" % a, ans, ["batteries (cells)" if t == "mains" else "mains electricity (a plug in the wall)", "it does not use electricity", "only solar power"],
                "Big, powerful appliances use mains; small, portable ones use batteries.")


def g_uses():
    a = R.choice(APP)[0]
    w = R.sample(NOEL, 3)
    if not once(("us", a), 2):
        return None
    o = sorted([a] + w)
    return item("Which of these needs electricity to work: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Electrical appliances need electricity from the mains or a battery.")


PART = [("a cell (battery)", "pushes electricity around the circuit"), ("a wire", "carries electricity from one part to the next"), ("a bulb", "lights up when electricity flows through it"),
        ("a switch", "opens or closes a gap to turn the circuit off or on"), ("a buzzer", "makes a sound when electricity flows through it"), ("a motor", "spins when electricity flows through it")]


def g_part():
    p, j = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    if k:
        return item("What does %s do in a circuit?" % p, "It " + j + ".", ["It " + x[1] + "." for x in R.sample([x for x in PART if x[0] != p], 3)], "Each part has a job.")
    return item("Which part of a circuit %s?" % j, p, R.sample([x[0] for x in PART if x[0] != p], 3), "Each part has a job.")


TXT = [("A bulb is joined to a cell by one wire from one end of the cell.", "No, there is only one wire, so the circuit is not complete."),
       ("A bulb is joined to both ends of a cell by two wires.", "Yes, the circuit is a complete loop."),
       ("A bulb, a cell and a switch are joined in a loop, and the switch is open.", "No, the open switch makes a gap."),
       ("A bulb, a cell and a switch are joined in a loop, and the switch is closed.", "Yes, the circuit is a complete loop."),
       ("Two wires go from a bulb, but both are joined to the same end of the cell.", "No, the loop does not go through the cell."),
       ("A bulb is joined to both ends of a cell, but one wire has come loose.", "No, the loose wire leaves a gap."),
       ("A bulb and a buzzer are joined in a loop with a cell and no gaps.", "Yes, the circuit is a complete loop."),
       ("A bulb is joined in a loop with wires, but there is no cell.", "No, there is nothing to push the electricity.")]


def g_txt():
    s, a = R.choice(TXT)
    if not once(("tx", s)):
        return None
    w = sorted({x[1] for x in TXT if x[1] != a})
    return item("%s Will the bulb light?" % s, a, R.sample(w, 3), "A bulb lights only in a complete loop with a cell.")


B1 = bank([
    ("What is mains electricity?", "electricity from power stations that comes through the wires to plug sockets", ["electricity from a battery", "electricity from lightning", "a kind of fuel"], "About 230 volts: dangerous."),
    ("Why is mains electricity dangerous?", "It is very powerful and can kill.", ["It is weak.", "It is the same as a battery.", "It is only dangerous at night."], "Never play with sockets."),
    ("Why should you never touch a switch or plug with wet hands?", "Water conducts electricity and could give you a shock.", ["Water makes switches slippery only.", "Plugs do not like water.", "It is perfectly safe."], "Keep water away."),
    ("What is a circuit?", "a complete loop that electricity can flow around", ["a single wire", "a type of battery", "a light switch only"], "No gaps."),
    ("What does a switch do?", "turns a circuit on or off by closing or opening a gap", ["makes a bulb brighter", "stores electricity", "changes a bulb's colour"], "On or off."),
    ("Why does a torch need a switch?", "so you can turn it off and save the battery", ["to make it heavier", "to make the light red", "it does not need one"], "Control the circuit."),
    ("What should you do if you see a damaged electrical cable?", "tell an adult and not touch it", ["fix it with tape yourself", "pull it out of the wall", "touch it to check"], "Safety first."),
    ("Which of these is safe to use in a school circuit?", "a small battery (cell)", ["a mains plug socket", "a car battery", "a kettle's cable"], "Only use cells in experiments."),
])
B5 = bank([
    ("Why do batteries eventually stop working?", "The chemicals inside get used up.", ["The wires melt.", "Batteries get lonely.", "Electricity leaks into the air."], "Some can be recharged."),
    ("Why should used batteries be recycled and not put in the bin?", "They contain chemicals that can harm the environment.", ["They are too heavy.", "They might explode with joy.", "Bins are for paper only."], "Recycle safely."),
    ("A bulb does not light even though the circuit looks complete. What should you check first?", "that all the connections are tight and the cell works", ["the colour of the wires", "the weather", "the size of the table"], "Find the fault."),
    ("Why do many devices use rechargeable batteries?", "They can be used many times, which saves money and waste.", ["They never run out.", "They are mains powered.", "They need no charging."], "Reuse."),
    ("Why is a smoke alarm usually battery-powered?", "It keeps working even if the mains power goes off.", ["Batteries are louder.", "Mains is not allowed in ceilings.", "Smoke stops mains electricity."], "Reliability."),
])


def body():
    think = ("<p><b>Appliances need electricity, from the mains or from batteries.</b></p>"
             "<ul><li>Mains electricity is powerful and dangerous; batteries (cells) are safe for experiments.</li>"
             "<li>A simple circuit needs a cell and a complete loop of wires through a bulb, buzzer or motor.</li>"
             "<li>A switch opens a gap (off) or closes it (on). Any gap stops the electricity.</li></ul>")
    ex = [("A bulb joined to a cell by one wire. Light?", ["The loop is not complete"], "No"),
          ("Kettle: mains or battery?", ["Big, powerful appliance"], "mains")]
    mist = ["Thinking a bulb lights with one wire.", "Thinking a switch makes a bulb brighter.", "Touching plugs or switches with wet hands."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Using electricity", B1 + [(g_app, 8), (g_uses, 4)]),
        ("Appliances", [(g_app, 6), (g_uses, 8), (g_part, 6)]),
        ("Parts of a circuit", [(g_part, 6), (g_txt, 8), (C6.g_work, 6)]),
        ("Will it light?", [(C6.g_work, 14), (C6.g_two, 6)]),
        ("Thinking about circuits", B5 + [(C6.g_work, 6), (C6.g_two, 6), (g_uses, 3)]),
    ])
    make_uk(4, "electrical-appliances-and-circuits", 12, "Electricity",
            "Identify common appliances that run on electricity. Construct a simple series electrical circuit, identifying and naming its basic parts, including cells, wires, bulbs, switches and buzzers. "
            "Identify whether or not a lamp will light in a simple series circuit, based on whether or not the lamp is part of a complete loop with a battery. Recognise that a switch opens and closes a circuit and associate this with whether or not a lamp lights in a simple series circuit.",
            "Electrical Appliances and Circuits",
            "Year 4 Science: Electrical Appliances and Circuits Worksheets (Will the Bulb Light?)",
            "Appliances and Circuits",
            "Free Year 4 science worksheets on electricity: mains and battery appliances, electrical safety, the parts of a circuit, switches, and whether a bulb will light. 100 questions with answers.",
            "A complete loop makes a bulb light.",
            "Cells push electricity round wires; a switch opens or closes the loop.",
            body(),
            [("What makes a bulb light up?", "A cell joined in a complete loop of wires through the bulb, with no gaps. Electricity can then flow all the way round."),
             ("What does a switch do?", "It opens or closes a gap in the circuit. When it is closed (on), electricity flows; when it is open (off), it stops."),
             ("What is the difference between mains and battery power?", "Mains electricity comes from power stations through plug sockets and is dangerous. Batteries (cells) store a small amount of electricity and are safe for school experiments.")],
            sets)


if __name__ == "__main__":
    main()
