# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U03: electric circuits - complete loops, switches, components, circuit
diagrams, series and parallel bulbs, and finding faults.
  python tools/gen_au_science_y6_electric_circuits.py
Reuses the UK Year 6 circuit and circuit-symbol makers, the US Grade 4 circuit makers and the SG Primary 5 circuit makers
with Australian names. Wrong answers come from real mistakes: thinking one wire is enough, thinking a closed switch breaks
the circuit, and thinking a bulb in parallel goes out when another one blows.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

C6 = "gen_uk_science_y6_circuits_and_switches"
SY = "gen_uk_science_y6_circuit_symbols"
US = "gen_us_science_g4_electric_circuits"
SG = "gen_sg_science_p5_electrical_circuits"
uk_two = src(C6, "g_two")
uk_work = src(C6, "g_work")
uk_fault = src(C6, "g_fault")
uk_b1 = src.B(C6, "B1")
uk_b5 = src.B(C6, "B5")
sy_sym = src(SY, "g_sym")
sy_desc = src(SY, "g_desc")
sy_count = limit(src(SY, "g_count"), 4)
sy_read = limit(src(SY, "g_read"), 5)
sy_b1 = src.B(SY, "B1")
sy_b5 = src.B(SY, "B5")
us_light = limit(src(US, "g_light"), 6)
us_fix = limit(src(US, "g_fix"), 5)
us_b1 = src.B(US, "B1")
us_b5 = src.B(US, "B5")
sg_closed = src(SG, "g_closed")
sg_fuse = src(SG, "g_fuse", rep=[(r"\bfuses\b", "blows"), (r"\bfused\b", "blown")])
sg_switch = src(SG, "g_switch")
sg_cmp = limit(src(SG, "g_cmp"), 4)
sg_b1 = src.B(SG, "B1")
sg_b2 = src.B(SG, "B2")

POOL = pool(R, [
    ("What does a circuit need for a lamp to light?", "a complete loop from the battery through the lamp and back", ["one wire from the battery to the lamp", "a switch that is open", "a magnet"], "Electricity flows only around a complete loop."),
    ("Which component pushes electricity around a circuit?", "a battery (cell)", ["a lamp", "a switch", "a buzzer"], "The cell is the energy source."),
    ("What is the job of a switch?", "to open or close a gap in the circuit", ["to make the lamp brighter", "to store electricity", "to make sound"], "A closed switch completes the loop."),
    ("Two lamps are in a single loop (series). One blows. What happens to the other?", "It goes out too.", ["It gets brighter.", "It stays lit.", "It flashes."], "The loop is broken."),
    ("Two lamps are on separate branches (parallel). One blows. What happens to the other?", "It stays lit.", ["It goes out too.", "It gets dimmer and goes out.", "It starts to buzz."], "Its own branch is still a complete loop."),
    ("Why are the lights in a house wired in parallel?", "so each light can be switched on and off by itself", ["so all lights go out together", "to use more batteries", "so the lights are dimmer"], "Each branch has its own switch."),
    ("What happens to a lamp's brightness when more lamps are added in series with one cell?", "The lamps get dimmer.", ["They get brighter.", "Nothing changes.", "They all go out."], "The cell's energy is shared between more lamps."),
    ("What happens to a lamp when a second cell is added in series?", "It gets brighter.", ["It gets dimmer.", "It goes out.", "It changes colour."], "More cells push more energy through the lamp."),
    ("Why do scientists draw circuit diagrams with symbols?", "so anyone can understand the circuit quickly and clearly", ["because pictures are not allowed", "to make circuits work better", "to save batteries"], "The symbols are the same around the world."),
    ("Which is safe for a classroom circuit investigation?", "1.5 V cells, wires and small lamps", ["mains power from a wall socket", "a car battery and bare hands", "wet wires and a 230 V plug"], "Mains electricity in Australia is 230 V and can kill."),
])
POOL5 = pool(R, [
    ("Mia's lamp does not light. The cell is new and the lamp works in another circuit. What should she check next?", "that all the wires are connected and the switch is closed", ["the colour of the wires", "the weather", "the table she is using"], "Check one part at a time."),
    ("Jack adds a second lamp in series and both lamps are dimmer. What could he change to make them brighter?", "add another cell in series", ["remove the switch", "use longer wires", "add a third lamp"], "More cells, brighter lamps."),
    ("Ruby wants one switch to turn on two lamps at the same time. Where should the switch go?", "in the main part of the circuit, next to the cell", ["on one branch only", "outside the circuit", "inside a lamp"], "A switch in the main loop controls everything."),
    ("Kai tests how many lamps one cell can light brightly. What should he count?", "the number of lamps that still glow brightly", ["the length of the wires", "the colour of the cell", "the number of switches"], "Count the result he is testing."),
    ("Ella's buzzer makes a quiet sound. Which change would make it louder?", "add another cell in series", ["add another buzzer in series", "use thinner wires only", "open the switch"], "More energy from the cells makes the buzzer louder."),
    ("Why should you never test circuits with a wall socket?", "Mains electricity is 230 V and can cause serious injury.", ["Wall sockets have no electricity.", "Wall sockets only work at night.", "It makes lamps too dim."], "Use only cells in class."),
])


def main():
    sets = U.sets([
        ("Complete circuits", [(POOL, 4), (us_light, 6), (uk_work, 5), (us_b1, 3), (sg_b1, 2)]),
        ("Switches and faults", [(uk_two, 6), (sg_closed, 3), (us_fix, 5), (uk_fault, 4), (uk_b1, 2)]),
        ("Circuit diagrams", [(sy_sym, 6), (sy_desc, 5), (sy_count, 4), (sy_read, 3), (sy_b1, 2)]),
        ("Series and parallel", [(POOL, 6), (sg_fuse, 3), (sg_switch, 3), (sg_cmp, 4), (sg_b2, 4)]),
        ("Investigations", [(POOL5, 6), (uk_b5, 4), (us_b5, 4), (sy_b5, 3), (sy_read, 2), (sg_b2, 1)]),
    ])
    make_au(YEAR, "electric-circuits", SORT, "AC9S6U03", "Physical sciences",
            "Investigate the transfer and transformation of energy in electrical circuits, including the role of circuit components, "
            "insulators and conductors (summary of the Australian Curriculum v9.0 Science content description).",
            "Electric Circuits", "Electric circuits",
            "Free Year 6 science worksheets on electric circuits: complete loops, switches, circuit symbols and diagrams, series and "
            "parallel lamps, and finding faults. 100 questions with answers.",
            "Electricity needs a complete loop.", "Cells push energy around a closed circuit; a gap stops the flow.",
            "<p><b>Electricity flows only around a complete loop from the cell and back.</b></p><ul>"
            "<li>A switch opens or closes a gap. Closed switch: the circuit is complete.</li>"
            "<li>Circuit diagrams use symbols for cells, lamps, switches, buzzers and motors.</li>"
            "<li>Series: one loop, so if one lamp blows, all go out. Parallel: separate branches, so the others stay lit.</li></ul>",
            [("A lamp and a cell are joined with one wire. Will it light?", ["there is no path back to the cell"], "no"),
             ("Two lamps in parallel; one blows. The other?", ["its branch is still complete"], "stays lit")],
            ["Thinking one wire is enough (the loop must return to the cell).", "Thinking a closed switch turns the circuit off.",
             "Thinking all lamps go out when one blows in a parallel circuit."],
            [("What is a complete circuit?", "A complete circuit is an unbroken loop that goes from one end of the cell, through the components, and back to the other end of the cell."),
             ("What is the difference between series and parallel circuits?", "In a series circuit everything is in one loop. In a parallel circuit there are separate branches, so each lamp can work on its own."),
             ("Why must children not experiment with mains electricity?", "Mains electricity in Australia is 230 volts. It can cause serious burns or death. Classroom circuits use 1.5 V cells.")],
            sets)


if __name__ == "__main__":
    main()
