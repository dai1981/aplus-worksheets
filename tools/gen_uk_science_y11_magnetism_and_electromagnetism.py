# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Physics): Magnetism and Electromagnetism
  python tools/gen_uk_science_y11_magnetism_and_electromagnetism.py
Poles of magnets, permanent and induced magnets, magnetic materials, magnetic fields and field lines, the Earth's
field and compasses, the magnetic effect of a current, solenoids and electromagnets, and (higher tier) the motor
effect, F = BIl, Fleming's left-hand rule and electric motors. Reuses the US Physics electromagnetism questions in
British English.
Wrong answers come from real mistakes: "all metals are magnetic", "field lines go from south to north", "a copper core
makes an electromagnet stronger", "the thumb shows the current".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62112)
EI, EF = "phys_electromagnetism_and_induction", "phys_electric_and_magnetic_fields"
us_data, us_em = us(EI, "g_data"), us(EI, "g_em")
_dev = us(EI, "g_dev")
us_lines = us(EF, "g_lines", drop=("charge",))


def us_dev():
    it = _dev()
    if it is None or it["c"][it["a"]] not in ("electric motor", "loudspeaker") and "loudspeaker" not in it["q"] and "motor" not in it["q"]:
        return None
    return it


MAT = [("iron", True), ("steel", True), ("nickel", True), ("cobalt", True), ("copper", False), ("aluminium", False), ("brass", False), ("gold", False), ("plastic", False)]


def g_pole():
    if R.random() < 0.45:
        m, y = R.choice(MAT)
        if not once(("mt", m)):
            return None
        return item("Is %s a magnetic material?" % m, "Yes" if y else "No", ["No" if y else "Yes", "Only when it is hot", "Only when it is wet"],
                    "Iron, steel, nickel and cobalt are magnetic. Most other metals are not.")
    a, b = R.choice(["north", "south"]), R.choice(["north", "south"])
    k = R.choice(["what", "why"])
    if not once(("pl", a, b, k)):
        return None
    r = "They attract." if a != b else "They repel."
    if k == "why":
        return item("A %s pole is brought near a %s pole. Why do they %s?" % (a, b, "attract" if a != b else "repel"),
                    "Unlike poles attract." if a != b else "Like poles repel.", ["Like poles attract." if a != b else "Unlike poles repel.", "Magnets always attract.", "Only iron poles do this."],
                    "Like poles repel; unlike poles attract.")
    return item("The %s pole of one magnet is brought near the %s pole of another. What happens?" % (a, b), r,
                ["They repel." if a != b else "They attract.", "Nothing happens.", "They both lose their magnetism."], "Like poles repel; unlike poles attract.")


YES = ["a steel paper clip", "an iron nail", "a steel spoon", "a steel washer"]
NO = ["a copper wire", "an aluminium can", "a plastic ruler", "a wooden pencil", "a glass marble", "a gold ring", "a brass key"]


def g_pick():
    y = R.choice(YES)
    ns = R.sample(NO, 3)
    if not once(("pk", y, tuple(sorted(ns)))):
        return None
    opts = [y] + ns
    R.shuffle(opts)
    return item("A magnet is held near %s and %s. Which one is attracted?" % (", ".join(opts[:-1]), opts[-1]), y, ns, "Only iron, steel, nickel and cobalt are attracted to magnets.")


EMS = [("using more turns of wire on the coil", "stronger"), ("using a larger current", "stronger"), ("putting an iron core inside the coil", "stronger"),
       ("using fewer turns of wire", "weaker"), ("using a smaller current", "weaker"), ("removing the iron core", "weaker"),
       ("reversing the direction of the current", "the same strength, but the poles swap"), ("switching off the current", "not magnetic")]


def g_ems():
    c, a = R.choice(EMS)
    if not once(("em", c)):
        return None
    return item("How does %s change an electromagnet?" % c, a, [x for x in ["stronger", "weaker", "the same strength, but the poles swap", "not magnetic"] if x != a],
                "Strength increases with more turns, more current and an iron core.")


def g_bil():
    B = R.choice([0.05, 0.1, 0.2, 0.25, 0.4, 0.5, 0.8, 1.2])
    I = R.choice([0.5, 1, 2, 2.5, 3, 4, 5, 8, 10])
    L = R.choice([0.05, 0.1, 0.2, 0.25, 0.4, 0.5])
    F = round(B * I * L, 4)
    q = R.choice(["F", "F", "B", "I"])
    if F * 1000 != int(F * 1000) or not once(("bil", B, I, L, q)):
        return None
    f = lambda x: "%g" % x
    if q == "F":
        return item("A wire %s m long carries a current of %s A at right angles to a magnetic field of %s T. What is the force on the wire? (F = BIl)" % (f(L), f(I), f(B)), f(F) + " N",
                    [x for x in [f(round(B * I / L, 3)) + " N", f(round(B + I + L, 3)) + " N", f(round(F * 10, 3)) + " N", f(round(I * L, 3)) + " N"] if x != f(F) + " N"][:3],
                    "F = %s × %s × %s = %s N." % (f(B), f(I), f(L), f(F)))
    if q == "B":
        return item("A force of %s N acts on a wire %s m long carrying %s A at right angles to a magnetic field. What is the magnetic flux density? (F = BIl)" % (f(F), f(L), f(I)), f(B) + " T",
                    [x for x in [f(round(F * I * L, 4)) + " T", f(round(I * L / F, 2)) + " T", f(round(B * 10, 2)) + " T", f(round(F / I, 3)) + " T"] if x != f(B) + " T"][:3],
                    "B = F ÷ (I × l) = %s ÷ (%s × %s)." % (f(F), f(I), f(L)))
    return item("A force of %s N acts on a wire %s m long in a magnetic field of %s T (at right angles). What is the current? (F = BIl)" % (f(F), f(L), f(B)), f(I) + " A",
                [x for x in [f(round(F * B * L, 4)) + " A", f(round(B * L / F, 2)) + " A", f(round(I * 10, 2)) + " A", f(round(F / B, 3)) + " A"] if x != f(I) + " A"][:3],
                "I = F ÷ (B × l) = %s ÷ (%s × %s)." % (f(F), f(B), f(L)))


DIRS = {"to the right": (1, 0, 0), "to the left": (-1, 0, 0), "up the page": (0, 1, 0), "down the page": (0, -1, 0), "into the page": (0, 0, -1), "out of the page": (0, 0, 1)}
NAME = {v: k for k, v in DIRS.items()}
FING = [("first finger", "the magnetic field"), ("second finger", "the current"), ("thumb", "the force (motion)")]


def g_flem():
    if R.random() < 0.3:
        f, m = R.choice(FING)
        k = R.choice(["f", "m"])
        if not once(("fg", f, k)):
            return None
        if k == "f":
            return item("In Fleming's left-hand rule, what does the %s show?" % f, m, [x[1] for x in FING if x[0] != f] + ["the voltage"], "First finger: field. Second finger: current. Thumb: motion.")
        return item("In Fleming's left-hand rule, which finger shows %s?" % m, "the " + f, ["the " + x[0] for x in FING if x[0] != f] + ["the little finger"], "First finger: field. Second finger: current. Thumb: motion.")
    b, i = R.sample(list(DIRS), 2)
    B, I = DIRS[b], DIRS[i]
    Fv = (I[1] * B[2] - I[2] * B[1], I[2] * B[0] - I[0] * B[2], I[0] * B[1] - I[1] * B[0])
    if Fv == (0, 0, 0) or not once(("fl", b, i)):
        return None
    a = NAME[Fv]
    w = [NAME[tuple(-x for x in Fv)]] + R.sample([d for d in DIRS if d not in (a, NAME[tuple(-x for x in Fv)])], 2)
    return item("A wire carries a current %s. The magnetic field points %s. Use Fleming's left-hand rule. Which way is the force on the wire?" % (i, b), a, w,
                "First finger = field (%s), second finger = current (%s), thumb = force." % (b, i))


B1 = bank([
    ("What is the difference between a permanent magnet and an induced magnet?", "A permanent magnet makes its own field; an induced magnet only becomes magnetic in a magnetic field.", ["They are the same.", "Induced magnets are always stronger.", "Permanent magnets need electricity."], "Induced magnets lose most of their magnetism when removed from the field."),
    ("Which way do magnetic field lines point?", "from the north pole to the south pole", ["from the south pole to the north pole", "in circles around the north pole only", "they have no direction"], "Shown with arrows."),
    ("Where is the magnetic field of a bar magnet strongest?", "at the poles", ["in the middle", "far away from it", "it is the same everywhere"], "Field lines are closest together there."),
])
B2 = bank([
    ("Why does a compass point north?", "Its needle lines up with the Earth's magnetic field.", ["It is attracted to the Sun.", "The Earth spins.", "It is pulled by gravity."], "This is evidence that the Earth's core is magnetic."),
    ("What happens around a wire carrying a current?", "A magnetic field forms in circles around the wire.", ["Nothing happens.", "The wire becomes a permanent magnet.", "An electric field only."], "The field is stronger closer to the wire and with a bigger current."),
    ("What is a solenoid?", "a coil of wire", ["a bar magnet", "a battery", "a compass"], "Inside a solenoid the field is strong and uniform."),
    ("Which is the shape of the field around a solenoid?", "similar to a bar magnet", ["circles only around one end", "no field at all", "straight lines only inside"], "Adding an iron core makes it stronger."),
])
B5 = bank([
    ("What is the motor effect?", "A wire carrying a current in a magnetic field feels a force.", ["A magnet heats up.", "Current flows without a cell.", "A wire becomes a magnet only."], "Higher tier."),
    ("How can the speed of an electric motor be increased?", "Increase the current or use a stronger magnet.", ["Reverse the current.", "Use a weaker magnet.", "Remove the coil."], "A bigger force on the coil."),
    ("How can the direction of an electric motor be reversed?", "Reverse the current or the magnetic field.", ["Increase the current.", "Add more turns.", "Use a bigger battery."], "Fleming's left-hand rule."),
    ("When is the force on a current-carrying wire zero?", "when the wire is parallel to the magnetic field", ["when the wire is at right angles to the field", "when the current is large", "always"], "F = BIl only applies at right angles."),
])

if __name__ == "__main__":
  build(U, 11, "magnetism-and-electromagnetism", 12, "Physics", "Magnetism and electromagnetism",
      "Poles of a magnet; permanent and induced magnetism and magnetic forces; magnetic fields and the Earth's field; the magnetic effect of a current; solenoids and electromagnets; (higher tier) Fleming's left-hand rule, the motor effect (F = BIl) and electric motors.",
      "Magnetism and Electromagnetism", "Magnetism and Electromagnetism",
      "Free Year 11 GCSE Combined Science worksheets on magnetism: poles, magnetic materials, field lines, electromagnets, the motor effect, F = BIl and Fleming's left-hand rule. 100 questions with answers.",
      "Like poles repel; unlike poles attract.",
      "Force on a wire = flux density × current × length (F = BIl).",
      "<p><b>Currents make magnetic fields, and magnetic fields push on currents.</b></p><ul><li>Field lines go from north to south. Iron, steel, nickel and cobalt are magnetic.</li>"
      "<li>An electromagnet is stronger with more turns, a larger current and an iron core.</li>"
      "<li>F = BIl. Fleming's left-hand rule: first finger field, second finger current, thumb motion.</li></ul>",
      [("B = 0.5 T, I = 2 A, l = 0.1 m. Force?", ["0.5 × 2 × 0.1"], "0.1 N"), ("North near south?", ["Unlike poles"], "attract")],
      ["Thinking all metals are magnetic.", "Drawing field lines from south to north.", "Mixing up the fingers in Fleming's left-hand rule."],
      [("How can you make an electromagnet stronger?", "Use more turns of wire, a larger current, or put an iron core inside the coil."),
       ("What is the motor effect?", "A wire carrying a current in a magnetic field feels a force. The force F = BIl when the wire is at right angles to the field."),
       ("How do you use Fleming's left-hand rule?", "Point your first finger along the field (north to south), your second finger along the current, and your thumb shows the direction of the force.")],
      [("Magnets", B1 + [(g_pole, 8), (g_pick, 6), (us_lines, 3)]),
       ("Magnetic fields", B2 + [(us_em, 6), (g_pole, 6), (g_pick, 4)]),
       ("Electromagnets", [(g_ems, 6), (us_data, 9), (us_em, 5)]),
       ("The motor effect", [(g_bil, 14), (g_flem, 6)]),
       ("Fleming's left-hand rule", B5 + [(g_flem, 13), (us_dev, 3)])])
