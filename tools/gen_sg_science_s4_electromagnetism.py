# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 18: Electromagnetism
  python tools/gen_sg_science_s4_electromagnetism.py
The magnetic field around a straight wire (right-hand grip rule) and a solenoid; making stronger electromagnets and their uses
(relay, electric bell, circuit breaker); the force on a current-carrying conductor in a magnetic field (Fleming's left-hand
rule) and the factors that affect it; the force between parallel currents; the turning effect on a coil and the d.c. motor with
a split-ring commutator.
UK and US electromagnetism makers are reused (Singapore names); direction questions are worked out here.
Wrong answers come from real mistakes: "a wire with a current has no magnetic field", "using the right hand for the motor
effect", "the commutator changes a.c. into d.c.", "a stronger motor needs a weaker magnet".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 6
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_flem = src("gen_uk_science_y11_magnetism_and_electromagnetism", "g_flem")
uk_ems = src("gen_uk_science_y11_magnetism_and_electromagnetism", "g_ems")
us_em = src("gen_us_science_phys_electromagnetism_and_induction", "g_em")

V = {"to the right": (1, 0, 0), "to the left": (-1, 0, 0), "up the page": (0, 1, 0), "down the page": (0, -1, 0), "out of the page": (0, 0, 1), "into the page": (0, 0, -1)}
NAME = {v: k for k, v in V.items()}


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def g_flem():
    while True:
        i, b = R.sample(list(V), 2)
        f = cross(V[i], V[b])
        if f != (0, 0, 0):
            break
    ans = NAME[f]
    opp = NAME[tuple(-x for x in f)]
    wr = [opp, i, b]
    if len(set(wr + [ans])) < 4:
        wr = [opp] + [x for x in V if x not in (ans, opp, i, b)][:2]
    k = R.choice(["force", "force", "current"])
    if k == "force":
        return tq("A wire carries a current %s in a magnetic field that points %s. Use Fleming's left-hand rule. In which direction is the force on the wire?" % (i, b), ans, wr,
                  "Left hand: First finger = Field (%s), seCond finger = Current (%s), thuMb = Motion/force (%s)." % (b, i, ans))
    others = [x for x in V if x not in (i, NAME[tuple(-x for x in V[i])])]
    return tq("A wire in a magnetic field pointing %s feels a force %s. Use Fleming's left-hand rule. In which direction is the current?" % (b, ans), i,
              [NAME[tuple(-x for x in V[i])]] + [x for x in others if x not in (b, ans)][:2],
              "Left hand: First finger = Field, seCond finger = Current, thuMb = force. The current flows %s." % i)


def g_grip():
    k = R.choice(["wire", "wire", "sol"])
    if k == "wire":
        cur = R.choice(["out of the page", "into the page"])
        ans = "anticlockwise" if cur == "out of the page" else "clockwise"
        return tq("A long straight wire carries a current %s. Seen from the front, what is the direction of the magnetic field lines around the wire?" % cur, ans,
                  ["clockwise" if ans == "anticlockwise" else "anticlockwise", "straight lines away from the wire", "there is no magnetic field"],
                  "Right-hand grip rule: thumb along the current, curled fingers give the field direction (out of the page: anticlockwise).")
    way = R.choice(["clockwise", "anticlockwise"])
    ans = "south" if way == "clockwise" else "north"
    return tq("You look at one end of a solenoid. The current flows %s around this end. What pole is this end?" % way, "a %s pole" % ans,
              ["a %s pole" % ("north" if ans == "south" else "south"), "no pole: the field is only inside", "both poles"],
              "Clockwise current seen from an end makes it a south pole; anticlockwise makes it a north pole.")


STR = [("more turns of wire on the coil", "stronger"), ("a larger current", "stronger"), ("a soft iron core inside the coil", "stronger"), ("fewer turns of wire", "weaker"),
       ("a smaller current", "weaker"), ("removing the iron core", "weaker"), ("reversing the current", "the same strength, but the poles swap")]
g_str = rows(R, STR, "How does using %s change the magnetic field of a solenoid?", None, extra=["it has no magnetic field at all"])

MOT = [("increasing the current", "faster"), ("using a stronger magnet", "faster"), ("using more turns on the coil", "faster"), ("reversing the current", "the same speed in the opposite direction"),
       ("reversing the magnet's poles", "the same speed in the opposite direction"), ("reducing the current", "slower")]
g_mot = rows(R, MOT, "How does %s change the rotation of a d.c. motor?", None, extra=["it stops completely"])

DEV = [("a relay", "A small current in the coil magnetises a soft iron core, which pulls an armature to close a switch in a second circuit with a large current."),
       ("an electric bell", "The electromagnet pulls the armature so the hammer hits the gong; this breaks the circuit, the armature springs back, and the cycle repeats."),
       ("a circuit breaker", "A large current makes the electromagnet strong enough to pull an iron catch and open the switch."),
       ("a d.c. motor", "A current-carrying coil in a magnetic field feels a turning effect; the split-ring commutator reverses the current every half turn so it keeps turning."),
       ("a loudspeaker", "A changing current in a coil in a magnet's field makes the coil and cone vibrate.")]
g_dev = rows(R, DEV, "How does %s work?", "Which device works like this? “%s”")

POOL1 = pool(R, [
    ("What is produced around a wire carrying a current?", "a magnetic field in circles around the wire", ["an electric field only", "nothing unless it is coiled", "a magnetic field along the wire"], "Shown with iron filings or compasses."),
    ("What does the magnetic field of a solenoid look like?", "like the field of a bar magnet, with a uniform field inside", ["circles around each turn only", "no field outside", "random lines"], "The ends act as poles."),
    ("How does the magnetic field around a straight wire change further from the wire?", "It gets weaker: the circles are further apart.", ["It gets stronger.", "It stays the same.", "It reverses."], "Field strength falls with distance."),
    ("What is the motor effect?", "the force on a current-carrying conductor in a magnetic field", ["the heating effect of a current", "a current made by a moving magnet", "the attraction of iron by a magnet"], "Used in motors and loudspeakers."),
    ("What does each finger stand for in Fleming's left-hand rule?", "First finger: field; second finger: current; thumb: force (motion)", ["First finger: force; second finger: current; thumb: field", "First finger: current; second finger: field; thumb: force", "First finger: motion; second finger: field; thumb: current"], "FBI: F (thumb), B (first finger), I (second finger)."),
    ("When is there no force on a current-carrying wire in a magnetic field?", "when the wire is parallel to the field", ["when the wire is at right angles to the field", "when the current is large", "when the magnet is strong"], "The force is largest at right angles."),
    ("Two parallel wires carry currents in the same direction. What happens?", "They attract each other.", ["They repel each other.", "Nothing happens.", "They twist round each other."], "Currents in opposite directions repel."),
    ("Two parallel wires carry currents in opposite directions. What happens?", "They repel each other.", ["They attract each other.", "Nothing happens.", "They both get hotter only."], "Their fields push apart between the wires."),
    ("What does the split-ring commutator in a d.c. motor do?", "It reverses the current in the coil every half turn so the coil keeps turning in the same direction.",
     ["It changes a.c. into d.c.", "It makes the magnet stronger.", "It stops the coil spinning."], "The brushes press against it."),
    ("What are the carbon brushes in a d.c. motor for?", "to make electrical contact with the rotating commutator", ["to clean the coil", "to make the magnetic field", "to reduce the current"], "They allow the coil to turn freely."),
])
POOL5 = pool(R, [
    ("Why does an electromagnet have a soft iron core rather than a steel one?", "Soft iron is magnetised strongly and loses its magnetism as soon as the current is switched off.", ["Steel is non-magnetic.", "Soft iron is a better electrical conductor.", "Steel makes the field weaker forever."], "The electromagnet can be switched off."),
    ("Why is a relay used to switch on a car's starter motor?", "A small current in a safe circuit controls a very large current in another circuit.", ["It increases the battery voltage.", "It changes d.c. into a.c.", "It makes the motor quieter."], "Thin wires can be used for the switch circuit."),
    ("A coil in a motor is horizontal and parallel to the field. Why is the turning effect largest here?", "The sides of the coil cutting across the field have forces at the largest perpendicular distance from the axis.",
     ["There is no force in this position.", "The current is largest here.", "The magnet is closest here."], "The moment is largest."),
    ("Which change does NOT make a d.c. motor turn faster?", "using a commutator made of plastic", ["increasing the current", "using a stronger magnet", "adding more turns to the coil"], "A plastic commutator would not conduct."),
    ("A wire carrying a current is placed between the poles of a magnet. The current is doubled. What happens to the force?", "It doubles.", ["It halves.", "It stays the same.", "It reverses."], "F is proportional to the current."),
    ("Both the current and the magnetic field direction are reversed. What happens to the force on the wire?", "It stays in the same direction.", ["It reverses.", "It becomes zero.", "It doubles."], "Reversing both cancels out."),
    ("Why does a loudspeaker cone vibrate?", "The alternating current in the coil keeps reversing the force on the coil in the magnet's field.", ["The magnet vibrates by itself.", "Air pushes the cone.", "The cone is charged."], "The motor effect."),
    ("Why can an electric bell not work with the circuit permanently closed?", "The armature must break the circuit so the electromagnet switches off and the armature springs back.", ["It would ring too loudly.", "It needs alternating current only.", "The gong would melt."], "This makes it ring repeatedly."),
])


def main():
    sets = U.sets([
        ("Magnetic effect of a current", [POOL1, (g_grip, 6), (g_str, 5)]),
        ("Electromagnets and their uses", [(g_str, 4), (g_dev, 6), (uk_ems, 4), (us_em, 6)]),
        ("The force on a current-carrying conductor", [(g_flem, 10), (uk_flem, 5), POOL1]),
        ("The d.c. motor", [(g_mot, 6), (g_dev, 4), POOL1, (POOL5, 4), (us_em, 2)]),
        ("Exam-style questions", [(POOL5, 7), (g_flem, 5), (g_grip, 4), (uk_flem, 2), (us_em, 2)]),
    ])
    make_ol(LV, SUBJ, "electromagnetism", SORT, "Electromagnetism",
            "Draw the pattern of the magnetic field due to currents in straight wires and in solenoids and state the effect of reversing the current; describe how the "
            "magnetic effect of a current is used in a relay and a circuit breaker; describe the force on a current-carrying conductor in a magnetic field and use "
            "Fleming's left-hand rule to find its direction; describe the forces between parallel currents; explain the turning effect on a coil and how a d.c. motor "
            "works, including the split-ring commutator, and how its speed can be increased (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Electromagnetism", "Electromagnetism",
            "Free Secondary 4 O-Level Physics worksheets on electromagnetism: magnetic fields of wires and solenoids, electromagnets, relays, Fleming's left-hand rule and the "
            "d.c. motor. 100 questions with answers.",
            "A current makes a magnetic field.", "Fleming's left-hand rule: field, current, force.",
            "<p><b>An electric current produces a magnetic field.</b></p><ul>"
            "<li>Straight wire: circular field lines; right-hand grip rule (thumb = current, fingers = field). Solenoid: like a bar magnet.</li>"
            "<li>Stronger electromagnet: more turns, larger current, soft iron core.</li>"
            "<li>Motor effect: a current at right angles to a magnetic field feels a force. Fleming's left-hand rule: First finger Field, seCond finger Current, thuMb Motion.</li>"
            "<li>D.C. motor: the split-ring commutator reverses the current every half turn. Faster: more current, stronger magnet, more turns.</li></ul>",
            [("Current to the right, field into the page. Force?", ["left hand: field into page, current right"], "up the page"),
             ("Seen from one end, current flows anticlockwise. Pole?", ["anticlockwise = N"], "north")],
            ["Using the right hand for the motor effect. Use the left hand.", "Thinking the commutator changes a.c. into d.c.",
             "Forgetting that a wire parallel to the field feels no force.", "Using steel for the core of an electromagnet."],
            [("How do you use Fleming's left-hand rule?", "Hold the thumb, first finger and second finger of your left hand at right angles: first finger = field (N to S), second finger = current (+ to −), thumb = force."),
             ("How can you make an electromagnet stronger?", "Increase the current, add more turns of wire, or put a soft iron core inside the coil."),
             ("What does the commutator in a d.c. motor do?", "It reverses the direction of the current in the coil every half turn, so the forces keep turning the coil in the same direction.")],
            sets)


if __name__ == "__main__":
    main()
