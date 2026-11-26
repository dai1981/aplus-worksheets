# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Physics): Magnetism and Electromagnets
  python tools/gen_uk_science_y8_magnetism_and_electromagnets.py
Magnetic poles, attraction and repulsion, magnetic materials, magnetic fields and field lines (drawn with iron filings
or a plotting compass), the Earth's magnetism and compasses, the magnetic effect of a current, electromagnets and how to
make them stronger, and uses (cranes, door locks, relays, the D.C. motor). Reuses the pole, material and electromagnet
questions of the US Grade 8 unit in British English and the magnet pictures of the Year 3 unit.
Wrong answers come from real mistakes: "all metals are magnetic", "field lines go from south to north",
"an electromagnet works with the current off", "a bigger magnet is always stronger".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
import gen_uk_science_y3_magnets_attract_and_repel as M3

U = Unit(61812)
R = U.R
P = People(R)
M3.U, M3.R, M3.P = U, R, P
uk_sci.USED.clear()
EM = adopt_us("gen_us_science_g8_electric_and_magnetic_forces", U)
us_poles, us_coil, us_dist, us_mat = ukm(EM.g_poles), ukm(EM.g_coil), ukm(EM.g_dist), ukm(EM.g_mat)


def g_em():
    who = P.next()[0]
    turns = [10, 20, 30, 40]
    per = R.choice([2, 3])
    clips = [t // 10 * per + R.choice([0, 1]) for t in turns]
    clips = sorted(set(clips))
    if len(clips) < 4:
        return None
    k = R.choice(["pattern", "most", "iv", "ctrl", "pred", "core"])
    if not once(("em", per, tuple(clips), k)) or not once(("em", k), 3 if k in ("pattern", "iv", "ctrl", "core") else 12):
        return None
    tab = table(["Turns of wire on the nail", "Paperclips picked up"], [[str(t), str(c)] for t, c in zip(turns, clips)])
    intro = tab + "%s made an electromagnet from a nail, wire and a cell. " % who
    if k == "pattern":
        return item(intro + "What do the results show?", "More turns of wire make a stronger electromagnet.", ["More turns make it weaker.", "The number of turns has no effect.", "The nail is not needed."], "Coils add up their fields.")
    if k == "most":
        return item(intro + "How many paperclips did 40 turns pick up?", str(clips[3]), [str(c) for c in clips[:3]], "Read the last row.")
    if k == "iv":
        return item(intro + "What is the independent variable?", "the number of turns of wire", ["the number of paperclips", "the size of the paperclips", "the type of cell"], "What was changed.")
    if k == "ctrl":
        return item(intro + "Which variable must stay the same for a fair test?", "the current (use the same cell)", ["the number of turns", "the number of paperclips", "the time of day only"], "Current also affects strength.")
    if k == "core":
        return item(intro + "What would happen if the iron nail were replaced by a wooden rod?", "The electromagnet would be much weaker.", ["It would be stronger.", "No change.", "It would repel the paperclips."], "Iron concentrates the field.")
    d = clips[3] - clips[0]
    return item(intro + "How many more paperclips did 40 turns pick up than 10 turns?", str(d), [str(x) for x in sorted({clips[3], clips[0], d + 2, d + 1} - {d})][:3], "%d − %d = %d." % (clips[3], clips[0], d))


FIELD = [("Which way do magnetic field lines point?", "from the north pole to the south pole", ["from the south pole to the north pole", "round in circles only", "away from both poles"]),
         ("Where is the magnetic field of a bar magnet strongest?", "at the poles", ["in the middle", "far away from the magnet", "it is the same everywhere"]),
         ("What do field lines that are close together show?", "a strong field", ["a weak field", "no field", "a south pole"]),
         ("How can you show the shape of a magnetic field?", "with iron filings or a plotting compass", ["with a thermometer", "with a ruler only", "with copper filings"]),
         ("Which way does a compass needle point?", "towards the Earth's magnetic north pole", ["towards the Sun", "always to the east", "towards the nearest wall"]),
         ("Why does a compass work?", "The Earth has a magnetic field, and the compass needle is a small magnet.", ["The Earth's core is cold.", "The needle is electric.", "Air pushes the needle north."]),
         ("What happens to a compass near a wire carrying a current?", "The needle moves because the current makes a magnetic field.", ["Nothing happens.", "The needle melts.", "It points at the Sun."]),
         ("What happens if a bar magnet is cut in half?", "Each piece becomes a smaller magnet with its own north and south poles.", ["One piece is north and the other is south only.", "Both pieces lose all magnetism.", "Each piece has two north poles."]),
         ("Why does the Earth's magnetic field matter for living things?", "It protects the Earth from charged particles from the Sun and helps some animals navigate.", ["It makes the Earth spin.", "It causes the seasons.", "It has no effect."]),
         ("How can you find out whether a metal bar is a magnet?", "See if it repels one end of a known magnet: only a magnet can repel.", ["See if it attracts a magnet.", "Weigh it.", "Heat it."]),
         ("What is the shape of the field around a long straight wire with a current?", "circles around the wire", ["straight lines along the wire", "no field", "a bar shape"])]


def g_field():
    q, a, w = R.choice(FIELD)
    if not once(("fi", q)):
        return None
    return item(q, a, w, "Field lines go from N to S and are closest where the field is strongest.")


STR = [("using more turns of wire on the coil", "stronger"), ("using a bigger current", "stronger"), ("putting an iron core inside the coil", "stronger"),
       ("using fewer turns of wire", "weaker"), ("using a smaller current", "weaker"), ("removing the iron core", "weaker"), ("switching the current off", "no longer magnetic"), ("adding a second cell to increase the current", "stronger"), ("replacing the iron core with a plastic rod", "weaker")]


def g_str():
    s, a = R.choice(STR)
    if not once(("sr", s)):
        return None
    T = {"stronger": "It gets stronger.", "weaker": "It gets weaker.", "no longer magnetic": "It stops being magnetic.", "perm": "It becomes a permanent magnet."}
    return item("What happens to an electromagnet if you change it by %s?" % s, T[a], [v for k2, v in T.items() if k2 != a][:3],
                "More turns, more current and an iron core make it stronger.")


USE = [("a scrapyard crane", "It can be switched off to drop the steel."), ("an electric door lock", "It holds the door until the current is switched off."),
       ("a relay", "A small current switches on a circuit with a big current."), ("an electric bell", "The magnet switches on and off, so the hammer hits the bell again and again."),
       ("a maglev train", "Electromagnets lift and push the train without touching the track.")]


def g_use():
    d, a = R.choice(USE)
    if not once(("us", d)):
        return None
    return item("Why is an electromagnet used in %s?" % d, a, R.sample([x[1] for x in USE if x[1] != a], 3), "Electromagnets can be switched on and off.")


B1 = bank([
    ("What happens when two north poles are brought together?", "They repel.", ["They attract.", "Nothing happens.", "They stick then fall apart."], "Like poles repel."),
    ("Which metals are magnetic?", "iron, nickel and cobalt (and steel)", ["all metals", "copper and aluminium", "gold and silver"], "Most metals are not."),
    ("What is a magnetic field?", "the region around a magnet where magnetic materials feel a force", ["the inside of a magnet only", "a field of grass with iron", "the light from a magnet"], "Non-contact force."),
    ("What is an electromagnet?", "a coil of wire that becomes a magnet when a current flows", ["a magnet made of electrons", "a permanent magnet", "a battery"], "Often with an iron core."),
])
B5 = bank([
    ("What makes a D.C. motor spin?", "a coil with a current in a magnetic field feels a force", ["static electricity", "heat from the wires", "gravity on the coil"], "Electric motors."),
    ("Why is a steel bar used for permanent magnets but soft iron for electromagnet cores?", "Steel keeps its magnetism; soft iron loses it quickly when the current stops.", ["Steel is not magnetic.", "Soft iron is a permanent magnet.", "Both lose magnetism instantly."], "Permanent vs temporary."),
    ("How can you tell which end of an electromagnet is the north pole?", "Use a plotting compass: its north end points away from the north pole.", ["Look at the colour of the wire.", "Feel which end is warmer.", "It has no poles."], "Test with a compass."),
    ("Why might an electromagnet get hot?", "The current heats the wire.", ["Magnets are always hot.", "The field burns.", "The iron core reacts."], "Energy transfer."),
])


def body():
    think = ("<p><b>Magnets have north and south poles: like poles repel, unlike poles attract.</b></p>"
             "<ul><li>Field lines go from north to south and are closest where the field is strongest.</li>"
             "<li>A current in a wire makes a magnetic field. A coil with a current is an electromagnet.</li>"
             "<li>More turns, a bigger current and an iron core make an electromagnet stronger.</li></ul>")
    ex = [("North pole near a south pole?", ["Unlike poles"], "attract"),
          ("Remove the iron core: electromagnet?", ["Iron concentrates the field"], "weaker")]
    mist = ["Thinking all metals are magnetic.", "Drawing field lines from south to north.", "Thinking an electromagnet works with the current off."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Magnets and poles", B1 + [(us_poles, 7), (M3.g_pic, 5), (us_mat, 4)]),
        ("Magnetic fields", [(g_field, 9), (us_poles, 5), (us_dist, 2), (M3.g_three, 4)]),
        ("Electromagnets", [(g_str, 8), (g_em, 9), (us_coil, 3)]),
        ("Testing electromagnets", [(g_em, 10), (g_use, 4), (M3.g_pic, 4), (M3.g_three, 2)]),
        ("Using magnetism", B5 + [(g_em, 6), (M3.g_three, 5), (us_poles, 2), (us_coil, 1), (g_field, 1), (M3.g_pic, 1)]),
    ])
    make_ks3(8, "magnetism-and-electromagnets", 12, "Physics", "Magnetism",
             "Magnetic poles, attraction and repulsion; magnetic fields by plotting with compass, representation by field lines; Earth's magnetism, compass and navigation; the magnetic effect of a current, electromagnets, D.C. motors (principles only).",
             "Magnetism and Electromagnets",
             "Year 8 Science: Magnetism and Electromagnets Worksheets (Poles, Fields, Electromagnets)",
             "Magnetism and Electromagnets",
             "Free Year 8 science worksheets on magnetism: poles, magnetic materials, field lines, compasses, electromagnets, how to make them stronger and their uses. 100 questions with answers.",
             "Like poles repel; unlike poles attract.",
             "A current makes a magnetic field; more turns, more current and an iron core make it stronger.",
             body(),
             [("Which materials are magnetic?", "Iron, nickel, cobalt and steel. Most other metals, such as copper and aluminium, are not."),
              ("How do you make an electromagnet stronger?", "Use more turns of wire on the coil, a bigger current, or an iron core inside the coil."),
              ("Why are electromagnets useful?", "They can be switched on and off, so they are used in scrapyard cranes, door locks, relays and electric bells.")],
             sets)


if __name__ == "__main__":
    main()
