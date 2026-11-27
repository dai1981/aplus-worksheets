# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 19: Electromagnetic Induction
  python tools/gen_sg_science_s4_electromagnetic_induction.py
A changing magnetic field (or a conductor cutting field lines) induces an e.m.f.; the factors that affect its size (Faraday's
law) and its direction (Lenz's law); the a.c. generator with slip rings and its output; the transformer, Vs/Vp = Ns/Np and
VpIp = VsIs for an ideal transformer; why electricity is transmitted at high voltage (less power lost, P = I²R).
US induction makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "a stationary magnet in a coil induces a current", "a transformer works with d.c.",
"a step-up transformer increases the power", "high-voltage transmission means a larger current in the cables".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 7
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

GV = [(r"\bthe metre\b", "the galvanometer"), (r"\ba metre\b", "a galvanometer"), (r"\bjunkyard\b", "scrapyard")]
us_ind = src("gen_us_science_phys_electromagnetism_and_induction", "g_ind", rep=GV)
us_dev = src("gen_us_science_phys_electromagnetism_and_induction", "g_dev", rep=GV)


def g_tf():
    k = R.choice(["Vs", "Vs", "Np", "Ns", "Ip", "Is"])
    Vp = R.choice([230, 240, 12, 24, 110, 11000])
    ratio = R.choice([0.05, 0.1, 0.25, 0.5, 2, 4, 5, 10, 20])
    Np = R.choice([100, 200, 400, 500, 1000, 2000])
    Ns = Np * ratio
    Vs = Vp * ratio
    if Ns != int(Ns) or Vs != int(Vs) or Vs > 500000:
        return None
    Ns, Vs = int(Ns), int(Vs)
    kind = "step-up" if ratio > 1 else "step-down"
    if k == "Vs":
        return nq("A transformer has %d turns on the primary coil and %d turns on the secondary coil. The primary voltage is %d V. What is the secondary voltage?" % (Np, Ns, Vp), Vs,
                  [Vp * Np / Ns, Vp, Vp * Ns * Np / 1000], " V", "Vs ÷ Vp = Ns ÷ Np, so Vs = %d × %d ÷ %d = %s V (a %s transformer)." % (Vp, Ns, Np, nf(Vs), kind))
    if k == "Np":
        return nq("A transformer changes %d V to %d V. The secondary coil has %d turns. How many turns are on the primary coil?" % (Vp, Vs, Ns), Np, [Ns * Vs / Vp, Ns, Ns * Vp * Vs / 1000], "",
                  "Np = Ns × Vp ÷ Vs = %d × %d ÷ %d = %d turns." % (Ns, Vp, Vs, Np))
    if k == "Ns":
        return nq("A transformer changes %d V to %d V. The primary coil has %d turns. How many turns are on the secondary coil?" % (Vp, Vs, Np), Ns, [Np * Vp / Vs, Np, Np + Vs], "",
                  "Ns = Np × Vs ÷ Vp = %d × %d ÷ %d = %d turns." % (Np, Vs, Vp, Ns))
    Ip = R.choice([0.1, 0.2, 0.5, 1, 2, 4])
    Is = Vp * Ip / Vs
    if k == "Is":
        return nq("An ideal transformer has a primary voltage of %d V and a primary current of %s A. The secondary voltage is %d V. What is the secondary current?" % (Vp, N(Ip), Vs), Is,
                  [Ip * Vs / Vp, Ip, Vp * Ip * Vs], " A", "VpIp = VsIs, so Is = %d × %s ÷ %d = %s A." % (Vp, N(Ip), Vs, nf(Is)))
    return nq("An ideal transformer gives %d V and %s A at its secondary coil. The primary voltage is %d V. What is the primary current?" % (Vs, nf(Is), Vp), Ip,
              [Is * Vp / Vs, Is, Vp * Vs * Is], " A", "VpIp = VsIs, so Ip = %d × %s ÷ %d = %s A." % (Vs, nf(Is), Vp, N(Ip)))


def g_loss():
    Pw = R.choice([100000, 200000, 500000, 1000000])
    Rc = R.choice([2, 4, 5, 10])
    V1, V2 = R.choice([(1000, 10000), (2000, 20000), (10000, 100000), (5000, 50000)])
    I1, I2 = Pw / V1, Pw / V2
    k = R.choice(["I", "loss", "ratio"])
    if k == "I":
        return nq("A power station sends %s W through cables at %s V. What is the current in the cables?" % (nf(Pw), nf(V2)), I2, [Pw * V2, V2 / Pw, I2 * 10], " A",
                  "I = P ÷ V = %s ÷ %s = %s A." % (nf(Pw), nf(V2), nf(I2)))
    if k == "loss":
        return nq("A current of %s A flows in transmission cables of total resistance %d Ω. What power is lost as heat in the cables?" % (trim(nf(I2)), Rc), I2 * I2 * Rc, [I2 * Rc, I2 * Rc * Rc, I2 * I2 / Rc], " W",
                  "P = I²R = %s² × %d = %s W." % (nf(I2), Rc, nf(I2 * I2 * Rc)))
    return tq("The voltage used to send the same power along a cable is increased 10 times. By what factor does the power lost in the cable change?", "It becomes 100 times smaller.",
              ["It becomes 10 times smaller.", "It becomes 10 times larger.", "It stays the same."], "The current falls by 10 times and P = I²R, so the loss falls by 10² = 100 times.")


FACT = [("moving the magnet into the coil faster", "a larger induced e.m.f."), ("using a stronger magnet", "a larger induced e.m.f."), ("using a coil with more turns", "a larger induced e.m.f."),
        ("holding the magnet still inside the coil", "no induced e.m.f."), ("moving the magnet out of the coil instead of in", "an induced e.m.f. in the opposite direction"),
        ("moving the coil towards a stationary magnet", "an induced e.m.f., just as when the magnet moves"), ("moving the magnet more slowly", "a smaller induced e.m.f.")]
g_fact = rows(R, FACT, "A magnet and a coil connected to a galvanometer are used. What is the effect of %s?", None, extra=["a constant current that never stops"])

LENZ = [("The N pole of a magnet is pushed into one end of a coil.", "a north pole, so it repels the approaching magnet"),
        ("The N pole of a magnet is pulled out of one end of a coil.", "a south pole, so it attracts the leaving magnet"),
        ("The S pole of a magnet is pushed into one end of a coil.", "a south pole, so it repels the approaching magnet"),
        ("The S pole of a magnet is pulled out of one end of a coil.", "a north pole, so it attracts the leaving magnet")]


def g_lenz():
    q, a = R.choice(LENZ)
    return tq(q + " What pole is induced at that end of the coil?", a, [x[1] for x in LENZ if x[1] != a],
              "Lenz's law: the induced current always opposes the change that produces it, so work must be done to move the magnet.")


POOL1 = pool(R, [
    ("What is electromagnetic induction?", "producing an e.m.f. in a conductor when the magnetic field through it changes (or it cuts field lines)", ["making a magnet with a current", "the force on a wire carrying a current", "heating a wire with a current"], "Discovered by Faraday."),
    ("State Faraday's law of electromagnetic induction.", "The induced e.m.f. is proportional to the rate of change of magnetic flux linkage (how fast field lines are cut).", ["The induced e.m.f. opposes the change.", "Current is proportional to p.d.", "Like poles repel."], "Faster change, larger e.m.f."),
    ("State Lenz's law.", "The induced current flows in a direction that opposes the change producing it.", ["The induced e.m.f. is proportional to the rate of change.", "The force is at right angles to current and field.", "Energy is created by induction."], "It follows from conservation of energy."),
    ("A magnet rests inside a coil connected to a galvanometer. What does the galvanometer show?", "zero: there is no change in the field", ["a steady current", "a large current", "an alternating current"], "Induction needs a change."),
    ("What are the slip rings in an a.c. generator for?", "to keep the coil connected to the outside circuit as it turns, so the output is alternating", ["to reverse the current every half turn and give d.c.", "to make the magnetic field", "to slow the coil down"], "A d.c. motor uses a split ring instead."),
    ("How does the output of an a.c. generator change if the coil turns faster?", "The peak e.m.f. increases and the frequency increases.", ["Only the frequency increases.", "The output becomes d.c.", "The peak e.m.f. decreases."], "Faster cutting of field lines."),
    ("Why does a transformer not work with a steady d.c. supply?", "A steady current makes a constant magnetic field, so no e.m.f. is induced in the secondary coil.", ["d.c. is too strong.", "The core would melt.", "d.c. cannot flow in coils."], "Transformers need a changing field."),
    ("What is the core of a transformer made of, and why?", "soft iron, so the changing magnetic field is linked strongly from the primary to the secondary coil", ["copper, to carry the current", "steel, to keep its magnetism", "plastic, to insulate the coils"], "The core is laminated to reduce energy losses."),
    ("What does a step-up transformer do?", "increases the alternating voltage; the secondary coil has more turns than the primary", ["increases the power", "changes a.c. into d.c.", "decreases the voltage"], "The current is stepped down."),
    ("In an ideal transformer, how do input power and output power compare?", "They are equal.", ["Output power is larger.", "Output power is zero.", "Input power is larger by the turns ratio."], "VpIp = VsIs."),
])
POOL5 = pool(R, [
    ("Why is electricity transmitted over long distances at very high voltage?", "For the same power, the current is smaller, so less energy is lost as heat in the cables (P = I²R).", ["High voltage travels faster.", "It is safer for homes.", "It increases the power."], "Step-down transformers lower the voltage near homes."),
    ("A magnet is dropped through a copper tube. Why does it fall slowly?", "Its moving field induces currents in the tube that oppose its motion (Lenz's law).", ["Copper is magnetic.", "Air pressure in the tube.", "The tube is charged."], "Energy is transferred to heat in the tube."),
    ("Why is it harder to turn a generator when it supplies a large current?", "The induced current produces a force that opposes the motion, so more work must be done.", ["The coil gets heavier.", "Friction increases with current.", "The magnet gets weaker."], "Conservation of energy."),
    ("A phone charger uses a transformer to change 230 V a.c. into a lower voltage. What type is it?", "a step-down transformer", ["a step-up transformer", "a generator", "a d.c. motor"], "Fewer turns on the secondary coil."),
    ("Which change does NOT increase the e.m.f. induced in a generator?", "using a thicker plastic casing", ["turning the coil faster", "using a stronger magnet", "adding more turns to the coil"], "The casing does not affect the field."),
    ("Why is a transformer core laminated (made of thin insulated sheets)?", "to reduce energy lost as heat by currents induced in the core", ["to make it stronger", "to increase the voltage", "to make it magnetic"], "These are called eddy currents."),
    ("A coil turns in a magnetic field. When is the induced e.m.f. zero?", "when the plane of the coil is at right angles to the field (its sides move parallel to the field lines)", ["when the coil is parallel to the field", "always", "never"], "No field lines are being cut at that instant."),
    ("A 230 V mains supply feeds a transformer with 1150 primary turns. How many secondary turns give 12 V?", "60", ["22 000", "240", "12"], "Ns = 1150 × 12 ÷ 230 = 60."),
])


def main():
    sets = U.sets([
        ("Inducing an e.m.f.", [POOL1, (g_fact, 5), (us_ind, 6)]),
        ("Faraday's and Lenz's laws", [(g_lenz, 4), (g_fact, 3), (us_ind, 4), (us_dev, 4), POOL1]),
        ("Generators and transformers", [(g_tf, 10), POOL1, (us_dev, 4)]),
        ("Transformer calculations and transmission", [(g_tf, 10), (g_loss, 8), (POOL5, 2)]),
        ("Exam-style questions", [(POOL5, 8), (g_tf, 5), (g_loss, 4), (g_lenz, 3)]),
    ])
    make_ol(LV, SUBJ, "electromagnetic-induction", SORT, "Electromagnetic Induction",
            "Deduce from experiments that a changing magnetic field can induce an e.m.f. in a circuit; state the factors affecting the magnitude of the induced e.m.f. "
            "(Faraday's law) and that its direction opposes the change producing it (Lenz's law); describe a simple a.c. generator with slip rings and sketch its output; "
            "describe the structure and principle of a transformer and recall and apply Vs/Vp = Ns/Np and VpIp = VsIs for an ideal transformer; explain the use of "
            "high voltage for the transmission of electrical energy (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Electromagnetic Induction", "EM induction",
            "Free Secondary 4 O-Level Physics worksheets on electromagnetic induction: Faraday's and Lenz's laws, the a.c. generator, transformers and high-voltage "
            "transmission. 100 questions with answers.",
            "A changing magnetic field induces an e.m.f.", "Transformer: Vs ÷ Vp = Ns ÷ Np; ideal: VpIp = VsIs.",
            "<p><b>A changing magnetic field induces an e.m.f. in a conductor.</b></p><ul>"
            "<li>Larger e.m.f.: faster movement, stronger magnet, more turns (Faraday's law). The induced current opposes the change (Lenz's law).</li>"
            "<li>An a.c. generator uses slip rings; turning faster gives a larger peak e.m.f. and a higher frequency.</li>"
            "<li>Transformers need a.c.: Vs ÷ Vp = Ns ÷ Np, and for an ideal transformer VpIp = VsIs.</li>"
            "<li>Transmitting at high voltage means a small current, so less power (I²R) is lost in the cables.</li></ul>",
            [("Np = 500, Ns = 25, Vp = 240 V. Vs?", ["Vs = 240 × 25 ÷ 500"], "12 V"),
             ("Ideal: 240 V, 0.5 A in; 12 V out. Is?", ["240 × 0.5 = 12 × Is"], "10 A")],
            ["Thinking a stationary magnet in a coil induces a current.", "Thinking a transformer works with d.c.",
             "Saying a step-up transformer increases the power. It increases the voltage and decreases the current.", "Mixing up slip rings (generator, a.c.) and the split-ring commutator (d.c. motor)."],
            [("What affects the size of an induced e.m.f.?", "How fast the magnetic field changes: the speed of movement, the strength of the magnet and the number of turns on the coil."),
             ("How does a transformer work?", "An alternating current in the primary coil makes a changing magnetic field in the soft iron core, which induces an alternating e.m.f. in the secondary coil."),
             ("Why is high voltage used for transmission?", "The same power at a higher voltage needs a smaller current, and the power lost in the cables (I²R) falls with the square of the current.")],
            sets)


if __name__ == "__main__":
    main()
