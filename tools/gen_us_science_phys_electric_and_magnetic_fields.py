# -*- coding: utf-8 -*-
"""
US High School Physics: Electric and Magnetic Fields (HS-PS3-5)
  python tools/gen_us_science_phys_electric_and_magnetic_fields.py
Develop and use a model of two objects interacting through electric or magnetic fields to illustrate the forces between
objects and the changes in energy of the objects due to the interaction.
Field lines (direction and strength), field strength E = F/q, the force on positive and negative charges, and how the
energy stored in a field changes when charges or magnets move closer or farther apart (compared with lifting a mass).
Wrong answers come from real mistakes: "field lines point toward positive charges", "energy always decreases when objects
move apart", "a field needs contact", "a negative charge moves along the field lines".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, sci, uniq, safe

U = Unit(90311)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


PAIRS = [("two opposite charges", "attract"), ("two like charges", "repel"), ("the north pole of one magnet and the south pole of another", "attract"),
         ("the north poles of two magnets", "repel"), ("a positive and a negative ion", "attract"), ("two negatively charged balloons", "repel"),
         ("a proton and an electron", "attract"), ("two protons", "repel"), ("the south poles of two magnets", "repel"), ("a magnet and a steel paper clip", "attract")]


@safe
def g_energy():
    who = P.next()[0]
    p, kind = R.choice(PAIRS)
    move = R.choice(["pulls apart", "pushes closer together", "lets go and they move"])
    if not once(("en", p, move)):
        return None
    if move == "lets go and they move":
        g = "The field's stored energy decreases and their kinetic energy increases."
        d = "closer together" if kind == "attract" else "farther apart"
        return item("%s holds %s near each other, then lets go and they move %s. What happens to the energy?" % (who, p, d), g,
                    ["The stored energy increases and they slow down.", "No energy changes.", "Energy is destroyed by the field."], "Like a dropped ball: stored energy becomes motion.")
    up = (move == "pulls apart") == (kind == "attract")
    g = "%s does work, and the energy stored in the field increases." % who if up else "The energy stored in the field decreases."
    w = ["The energy stored in the field decreases." if up else "%s does work, and the energy stored in the field increases." % who, "The energy stored in the field stays the same.", "The objects lose mass."]
    verb = "pulls %s apart" % p if move == "pulls apart" else "pushes %s closer together" % p
    return item("%s slowly %s (they %s). What happens to the energy stored in the field?" % (who, verb, kind), g, w,
                "Moving against the force stores energy (like lifting a mass); moving with it releases energy.")


@safe
def g_lines():
    q = R.choice(["positive charge", "negative charge", "bar magnet", "pair of opposite charges", "pair of like positive charges", "wire carrying current", "pair of north poles facing each other", "pair of parallel plates, positive on top"])
    k = R.choice(["dir", "strong"])
    if not once(("ln", q, k)):
        return None
    if k == "strong":
        g = "where the field lines are closest together"
        return item("In a field-line drawing of a %s, where is the field strongest?" % q, g, ["where the field lines are farthest apart", "where there are no lines", "always at the edge of the page"],
                    "Closer lines = stronger field.")
    ans = {"positive charge": "straight out, away from the charge", "negative charge": "straight in, toward the charge", "bar magnet": "from the north pole around to the south pole",
           "pair of opposite charges": "from the positive charge to the negative charge", "pair of like positive charges": "away from both charges, with a gap between them",
           "wire carrying current": "in circles around the wire", "pair of north poles facing each other": "out of both north poles, bending away from each other with a gap between them",
           "pair of parallel plates, positive on top": "straight down from the positive plate to the negative plate, evenly spaced"}[q]
    others = sorted({"straight out, away from the charge", "straight in, toward the charge", "from the north pole around to the south pole", "from the positive charge to the negative charge",
                     "away from both charges, with a gap between them", "in circles around the wire", "from the south pole to the north pole outside the magnet", "from the negative charge to the positive charge",
                     "out of both north poles, bending away from each other with a gap between them", "straight down from the positive plate to the negative plate, evenly spaced"} - {ans})
    return item("How do the field lines run for a %s?" % q, ans, R.sample(others, 3), "Electric field lines go from + to −; magnetic field lines go from N to S outside a magnet.")


@safe
def g_E():
    k = R.choice(["E", "F", "q"])
    q = R.choice([1, 2, 3, 4, 5, 8, 10])
    E = R.choice([100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    F = q * 1e-6 * E
    if not once(("ee", q, E, k)):
        return None
    if k == "E":
        g = "%s N/C" % num(E)
        return item("%s %d μC test charge feels a force of %s N. What is the electric field strength? (E = F ÷ q, 1 μC = 10<sup>−6</sup> C)" % ("An" if q == 8 else "A", q, num(F, 4)), g,
                    uniq(g, ["%s N/C" % num(F * q, 6), "%s N/C" % num(F, 4), "%s N/C" % num(E / 1000, 2), "%s N/C" % num(E * 2)]), "E = %s ÷ (%d × 10<sup>−6</sup>) = %s N/C." % (num(F, 4), q, num(E)))
    if k == "F":
        g = "%s N" % num(F, 4)
        return item("%s %d μC charge is placed in a %s N/C electric field. What force acts on it? (F = qE)" % ("An" if q == 8 else "A", q, num(E)), g,
                    uniq(g, ["%s N" % num(E / q, 1), "%s N" % num(q * E), "%s N" % num(F * 10, 4), "%s N" % num(F / 10, 5)]), "F = %d × 10<sup>−6</sup> × %s = %s N." % (q, num(E), num(F, 4)))
    g = "%d μC" % q
    return item("A charge feels %s N in a %s N/C field. What is its charge? (q = F ÷ E)" % (num(F, 4), num(E)), g, uniq(g, ["%s μC" % num(q * 10), "%s μC" % num(E * F, 2), "%s μC" % num(q * 2), "%s μC" % num(q / 10, 2)]),
                "q = %s ÷ %s = %d × 10<sup>−6</sup> C." % (num(F, 4), num(E), q))


@safe
def g_force():
    s = R.choice([("A proton is placed in a field pointing east.", "east"), ("An electron is placed in a field pointing east.", "west"), ("A positive ion is placed in a field pointing up.", "up"),
                  ("An electron is placed in a field pointing up.", "down"), ("A negative ion is placed in a field pointing north.", "south"), ("A positive charge is placed in a field pointing west.", "west"),
                  ("A compass is placed east of a bar magnet's north pole. Which way does the compass's north end point?", "east (away from the magnet's north pole)"),
                  ("A compass is placed near a magnet's south pole. Which way does its north end point?", "toward the magnet's south pole")])
    if not once(("fc", s[0])):
        return None
    if "compass" in s[0]:
        return item(s[0], s[1], ["toward the magnet's north pole" if "south" not in s[1] else "away from the magnet's south pole", "straight down", "it does not move"], "Opposite poles attract.")
    dirs = ["east", "west", "north", "south", "up", "down"]
    return item("%s Which way is the electric force on it?" % s[0], s[1], R.sample([d for d in dirs if d != s[1]], 3), "Positive charges are pushed along the field; negative charges are pushed the opposite way.")


B1 = bank([
    ("What is a field in physics?", "a region where an object feels a force without touching the source", ["a place with no forces", "a type of energy only in batteries", "a solid object"], "Gravity, electric and magnetic fields."),
    ("Which way do electric field lines point?", "away from positive charges and toward negative charges", ["toward positive charges", "in circles always", "from negative to positive"], "Direction of force on a + test charge."),
    ("What do closer field lines show?", "a stronger field", ["a weaker field", "no field", "a field of zero energy"], "Line density."),
    ("Lifting a ball stores energy in which field?", "the gravitational field between the ball and Earth", ["the ball's magnetic field", "the air", "the ball's electric field only"], "Field energy."),
    ("Pulling apart two magnets that attract each other does what to the stored energy?", "increases it", ["decreases it", "leaves it the same", "destroys it"], "Work against the force."),
    ("What are the units of electric field strength?", "N/C (newtons per coulomb)", ["N", "C", "J"], "Force per charge."),
    ("Where do magnetic field lines go outside a bar magnet?", "from the north pole to the south pole", ["from south to north", "straight out of both poles to infinity", "in a straight line through the middle only"], "Closed loops."),
    ("Why do two like charges released near each other speed up as they separate?", "Energy stored in the field turns into kinetic energy.", ["Energy is created.", "They gain mass.", "Gravity pushes them."], "Field energy → motion."),
])
B5 = bank([
    ("How is a charged particle accelerated in a particle accelerator?", "An electric field pushes on it, turning field energy into kinetic energy.", ["Gravity pulls it.", "A magnet makes it heavier.", "It accelerates by itself."], "Work done by a field."),
    ("Why does a fridge magnet stay on the door?", "The magnetic field pulls the magnet toward the steel door.", ["Glue in the magnet.", "Air pressure only.", "Gravity pulls it sideways."], "Magnetic force."),
    ("A model shows two opposite charges moving apart. Which outside action is needed?", "a push or pull that does work against the attraction", ["nothing; they move apart by themselves", "cooling them", "adding mass"], "Energy must be added."),
    ("How is moving two opposite charges together like dropping a ball?", "In both, stored field energy becomes kinetic energy.", ["Both create energy.", "Both need no field.", "Neither involves energy."], "Field model."),
    ("Iron filings sprinkled near a magnet form a pattern. What does the pattern show?", "the shape and strength of the magnetic field", ["the magnet's mass", "the electric charge", "the temperature"], "Model of a field."),
])


def body():
    think = ("<p><b>Objects interact through fields, and fields store energy.</b></p>"
             "<ul><li>Electric field lines go from + to −; magnetic field lines go from N to S outside a magnet. Closer lines = stronger field.</li>"
             "<li>E = F ÷ q. A positive charge is pushed along the field; a negative charge the opposite way.</li>"
             "<li>Moving objects against the field force stores energy (like lifting a mass); moving with it releases energy as motion.</li></ul>")
    ex = [("2 μC feels 0.004 N. E?", ["0.004 ÷ 0.000002"], "2,000 N/C"),
          ("Pull apart two attracting magnets?", ["Work against the force"], "stored energy increases")]
    mist = ["Thinking field lines point toward positive charges.", "Thinking stored energy always drops when objects move apart.", "Thinking a negative charge moves along the field lines."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fields", B1 + [(g_lines, 12)]),
        ("Forces in fields", [(g_force, 6), (g_E, 14)]),
        ("Field strength", [(g_E, 14), (g_energy, 6)]),
        ("Energy in fields", [(g_energy, 12), (g_E, 8)]),
        ("Modeling interactions", B5 + [(g_energy, 5), (g_E, 8), (g_lines, 2)]),
    ])
    make("physics", "electric-and-magnetic-fields", 11, "HS-PS3-5",
         "Develop and use a model of two objects interacting through electric or magnetic fields to illustrate the forces between objects and the changes in energy of the objects due to the interaction.",
         "Electric and Magnetic Fields",
         "Electric Field Worksheets: Field Lines, E = F/q and Energy in Fields (High School Physics)",
         "Electric and Magnetic Fields",
         "Free high school physics worksheets on electric and magnetic fields (NGSS HS-PS3-5): field lines, field strength E = F/q, forces on charges and energy stored in fields. 100 questions with answers.",
         "Fields carry forces and store energy.",
         "Moving objects against a field force stores energy; moving with it releases energy.",
         body(),
         [("What is an electric field?", "A region around a charge where other charges feel a force. Its strength is E = F ÷ q."),
          ("How do field lines show direction and strength?", "Arrows show the direction of the force on a positive test charge (or a north pole), and closer lines mean a stronger field."),
          ("How do fields store energy?", "Pulling attracting objects apart or pushing repelling objects together takes work, which is stored in the field, just like lifting a mass in Earth's gravitational field.")],
         sets)


if __name__ == "__main__":
    main()
