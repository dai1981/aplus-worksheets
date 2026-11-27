# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 14: Current of Electricity
  python tools/gen_sg_science_s4_current_of_electricity.py
Electric current as the rate of flow of charge (Q = It), conventional current and electron flow, electromotive force and
potential difference as work done per unit charge (V = W ÷ Q), resistance R = V ÷ I, resistivity (R = ρL ÷ A), I-V graphs of a
metallic conductor at constant temperature, a filament lamp and a semiconductor diode, and the use of ammeters and voltmeters.
UK and US charge and current makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "current is used up by a lamp", "conventional current flows from − to +", "R = I ÷ V",
"a thicker wire has more resistance", "e.m.f. is a force".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex, graph, fig

LV, SUBJ, SORT = 4, "Physics", 2
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_q = src("gen_uk_science_y10_electricity", "g_q")
uk_vir = src("gen_uk_science_y8_electricity", "g_vir")
uk_iv = src("gen_uk_science_y10_electricity", "g_iv")


def g_q():
    k = R.choice(["Q", "I", "t", "mA"])
    I = R.choice([0.2, 0.25, 0.5, 1.5, 2, 3, 4, 5])
    t = R.choice([5, 10, 20, 30, 60, 120, 180, 300])
    Q = I * t
    if k == "Q":
        return nq("A current of %s A flows for %d s. How much charge passes?" % (N(I), t), Q, [I / t, t / I, I + t], " C", "Q = It = %s × %d = %s C." % (N(I), t, N(Q)))
    if k == "I":
        return nq("%s C of charge passes a point in %d s. What is the current?" % (N(Q), t), I, [Q * t, t / Q, Q], " A", "I = Q ÷ t = %s ÷ %d = %s A." % (N(Q), t, N(I)))
    if k == "t":
        return nq("How long does it take for %s C to pass a point when the current is %s A?" % (N(Q), N(I)), t, [Q * I, I / Q, Q], " s", "t = Q ÷ I = %s ÷ %s = %d s." % (N(Q), N(I), t))
    ma = R.choice([20, 50, 100, 200, 250, 400, 500])
    t2 = R.choice([60, 120, 300, 600])
    return nq("A current of %d mA flows for %d s. How much charge passes?" % (ma, t2), ma / 1000 * t2, [ma * t2, ma * t2 / 100, ma / t2], " C",
              "%d mA = %s A; Q = %s × %d = %s C." % (ma, N(ma / 1000), N(ma / 1000), t2, N(ma / 1000 * t2)))


def g_w():
    k = R.choice(["W", "V", "Q"])
    V = R.choice([1.5, 3, 4.5, 6, 9, 12, 24])
    Q = R.choice([2, 5, 10, 20, 40, 50, 100])
    W = V * Q
    if k == "W":
        return nq("A cell of e.m.f. %s V drives %d C of charge round a circuit. How much electrical energy does it supply?" % (N(V), Q), W, [V / Q, Q / V, V + Q], " J",
                  "W = QV = %d × %s = %s J." % (Q, N(V), N(W)))
    if k == "V":
        return nq("%s J of energy is transferred when %d C of charge passes through a lamp. What is the potential difference across the lamp?" % (N(W), Q), V, [W * Q, Q / W, W - Q], " V",
                  "V = W ÷ Q = %s ÷ %d = %s V." % (N(W), Q, N(V)))
    return nq("A %s V battery supplies %s J of energy. How much charge has it driven round the circuit?" % (N(V), N(W)), Q, [W * V, V / W, W - V], " C",
              "Q = W ÷ V = %s ÷ %s = %d C." % (N(W), N(V), Q))


def g_vir():
    k = R.choice(["R", "I", "V"])
    I = R.choice([0.1, 0.2, 0.25, 0.4, 0.5, 1.5, 2, 3])
    Rr = R.choice([2, 4, 5, 6, 10, 12, 15, 20, 24, 30, 50, 100])
    V = I * Rr
    if V > 240:
        return None
    if k == "R":
        return nq("The potential difference across a resistor is %s V and the current through it is %s A. What is its resistance?" % (N(V), N(I)), Rr, [V * I, I / V, V - I], " Ω",
                  "R = V ÷ I = %s ÷ %s = %d Ω." % (N(V), N(I), Rr))
    if k == "I":
        return nq("A %d Ω resistor has a potential difference of %s V across it. What current flows?" % (Rr, N(V)), I, [V * Rr, Rr / V, V], " A", "I = V ÷ R = %s ÷ %d = %s A." % (N(V), Rr, N(I)))
    return nq("A current of %s A flows through a %d Ω resistor. What is the potential difference across it?" % (N(I), Rr), V, [I / Rr, Rr / I, I + Rr], " V", "V = IR = %s × %d = %s V." % (N(I), Rr, N(V)))


RHO = [("copper", 1.7e-8), ("aluminium", 2.8e-8), ("nichrome", 1.1e-6), ("constantan", 4.9e-7), ("iron", 1.0e-7)]


def g_rho():
    m_, rho = R.choice(RHO)
    L = R.choice([0.5, 1.0, 2.0, 5.0, 10, 20, 50, 100])
    A = R.choice([1.0e-6, 2.0e-6, 5.0e-7, 2.5e-7, 1.0e-7])
    Rr = rho * L / A
    k = R.choice(["R", "R", "rho"])
    if k == "R":
        return nq("A %s wire is %s m long with a cross-sectional area of %s m². The resistivity of %s is %s Ω m. What is its resistance?" % (m_, N(L), nf(A, 2), m_, nf(rho, 2)), Rr,
                  [rho * A / L, rho * L * A, L / (rho * A)], " Ω", "R = ρL ÷ A = %s × %s ÷ %s = %s Ω." % (nf(rho, 2), N(L), nf(A, 2), nf(Rr)))
    return nq("A wire %s m long with cross-sectional area %s m² has a resistance of %s Ω. What is the resistivity of the material?" % (N(L), nf(A, 2), nf(Rr)), rho,
              [Rr * L / A, Rr / (L * A), L / (Rr * A)], " Ω m", "ρ = RA ÷ L = %s × %s ÷ %s = %s Ω m." % (nf(Rr), nf(A, 2), N(L), nf(rho, 2)))


def g_scale():
    R0 = R.choice([2, 4, 5, 6, 8, 10, 12, 20])
    k = R.choice(["L2", "A2", "d2", "L3", "both"])
    if k == "L2":
        return nq("A wire has a resistance of %d Ω. What is the resistance of a wire of the same material and thickness that is twice as long?" % R0, 2 * R0, [R0 / 2, 4 * R0, R0], " Ω", "R ∝ L, so it doubles.")
    if k == "L3":
        return nq("A wire has a resistance of %d Ω. It is cut into three equal lengths. What is the resistance of one piece?" % (3 * R0), R0, [9 * R0, 3 * R0, R0 / 3], " Ω", "R ∝ L, so a third of the length has a third of the resistance.")
    if k == "A2":
        return nq("A wire has a resistance of %d Ω. What is the resistance of a wire of the same material and length with twice the cross-sectional area?" % R0, R0 / 2, [2 * R0, R0 / 4, R0], " Ω", "R ∝ 1/A, so it halves.")
    if k == "d2":
        return nq("A wire has a resistance of %d Ω. What is the resistance of a wire of the same material and length with twice the diameter?" % (4 * R0), R0, [2 * R0, 8 * R0, 16 * R0], " Ω",
                  "Doubling the diameter makes the area 4 times larger (A = πd²/4), so R becomes a quarter.")
    return nq("A wire has a resistance of %d Ω. Another wire of the same material is twice as long and has twice the cross-sectional area. What is its resistance?" % R0, R0, [4 * R0, R0 / 4, 2 * R0], " Ω",
              "R ∝ L ÷ A: × 2 ÷ 2, so no change.")


def g_ivg():
    """read resistance from an I-V graph of an ohmic conductor"""
    Rr = R.choice([2, 4, 5, 10, 20, 25, 50])
    Vmax = R.choice([6, 10, 12])
    Imax = Vmax / Rr
    ys = Imax / 4
    svg = graph([(0, 0), (Vmax, Imax)], Vmax, Imax * 1.25, 2, ys, "potential difference / V", "current / A", label="I-V graph")
    V = R.choice([x for x in range(2, Vmax + 1, 2)])
    return nq(fig(svg) + "The graph shows how the current in a resistor depends on the potential difference across it. What is its resistance?", Rr,
              [Imax / Vmax, Vmax * Imax, Rr / 2], " Ω", "R = V ÷ I = %d ÷ %s = %d Ω (the graph is a straight line through the origin, so R is constant)." % (V, nf(V / Rr), Rr))


IV = [("a metallic conductor (resistor) at constant temperature", "a straight line through the origin: current is proportional to p.d. and the resistance is constant"),
      ("a filament lamp", "a curve that gets less steep: the resistance increases as the filament gets hotter"),
      ("a semiconductor diode", "almost no current in reverse, then a steep rise in the forward direction: it lets current flow one way only")]
g_ivr = rows(R, IV, "What does the I-V graph of %s look like?", "Which component has an I-V graph that is %s?",
             extra=["a horizontal line: the current is the same for every p.d."])

POOL1 = pool(R, [
    ("What is electric current?", "the rate of flow of electric charge", ["the energy carried by charge", "the push that makes charge move", "the opposition to the flow of charge"], "I = Q ÷ t, in amperes."),
    ("What is 1 coulomb?", "the charge that passes a point when a current of 1 A flows for 1 s", ["the current that flows in 1 s", "the energy of 1 A for 1 s", "the charge of one electron"], "1 C = 1 A s."),
    ("In which direction does conventional current flow?", "from the positive terminal to the negative terminal of the supply", ["from negative to positive", "both ways at once", "only through insulators"], "Electrons actually flow the other way."),
    ("In which direction do electrons flow in a circuit?", "from the negative terminal to the positive terminal", ["from positive to negative", "the same way as conventional current", "they do not move"], "Opposite to conventional current."),
    ("What is the electromotive force (e.m.f.) of a source?", "the work done by the source in driving unit charge round a complete circuit", ["the force on an electron", "the current from the source", "the resistance of the source"], "Measured in volts: 1 V = 1 J/C."),
    ("What is the potential difference across a component?", "the work done (energy transferred) per unit charge passing through it", ["the current through it", "the charge stored in it", "the force on each charge"], "V = W ÷ Q."),
    ("What is resistance?", "the ratio of the potential difference across a component to the current through it", ["the current per volt", "the energy per coulomb", "the charge per second"], "R = V ÷ I, in ohms."),
    ("How is an ammeter connected?", "in series with the component", ["in parallel with the component", "across the cell only", "it is not connected"], "It must have a very small resistance."),
    ("How is a voltmeter connected?", "in parallel with the component", ["in series with the component", "between two cells", "in place of the switch"], "It must have a very large resistance."),
    ("Is current used up as it flows through a lamp?", "No: the current is the same on both sides; energy is transferred, not charge.", ["Yes: less current comes out.", "Yes: all the current is used up.", "Only in parallel circuits."], "Charge is conserved."),
])
POOL5 = pool(R, [
    ("Why does the resistance of a filament lamp increase as the current increases?", "The filament gets hotter, so its metal ions vibrate more and get in the way of the electrons.", ["The filament gets longer.", "The electrons speed up.", "The lamp gets brighter, which blocks current."], "The I-V graph curves."),
    ("Which of these wires has the lowest resistance (same material)?", "short and thick", ["long and thin", "long and thick", "short and thin"], "R = ρL ÷ A."),
    ("Why are connecting wires in circuits made of copper?", "Copper has a very low resistivity.", ["Copper is magnetic.", "Copper has a high resistivity.", "Copper is the cheapest metal."], "Less energy is wasted in the wires."),
    ("Why is nichrome used for heating elements?", "It has a high resistivity and does not oxidise easily when hot.", ["It has a very low resistivity.", "It is a good insulator.", "It is magnetic."], "A large resistance gives more heating."),
    ("A component lets current flow in only one direction. What is it?", "a diode", ["a filament lamp", "a fixed resistor", "a fuse"], "Used to protect circuits and change a.c. to d.c."),
    ("For which component is the ratio V ÷ I constant?", "a metal resistor at constant temperature", ["a filament lamp", "a diode", "a thermistor in a warming room"], "Its I-V graph is a straight line through the origin."),
    ("A 12 V battery drives a current of 0.5 A for 60 s. How much energy does it supply?", "360 J", ["30 J", "6 J", "1440 J"], "Q = It = 30 C; W = QV = 30 × 12 = 360 J."),
    ("A current of 2 A flows for 1 minute. How much charge passes?", "120 C", ["2 C", "30 C", "0.033 C"], "Change the time into seconds: 60 s."),
    ("What is the unit of resistivity?", "Ω m", ["Ω/m", "Ω m²", "Ω"], "ρ = RA ÷ L: Ω × m² ÷ m = Ω m."),
    ("A resistor is connected to a variable supply. The p.d. is doubled. What happens to the current?", "It doubles.", ["It halves.", "It stays the same.", "It becomes four times larger."], "R is constant, so I ∝ V."),
])


def main():
    sets = U.sets([
        ("Current and charge", [POOL1, (g_q, 8), (uk_q, 5)]),
        ("E.m.f. and potential difference", [(g_w, 9), POOL1, (POOL5, 3), (g_q, 3)]),
        ("Resistance and V = IR", [(g_vir, 9), (uk_vir, 4), (g_ivg, 4), (POOL5, 3)]),
        ("Resistivity and I-V graphs", [(g_rho, 6), (g_scale, 6), (g_ivr, 4), (uk_iv, 4)]),
        ("Exam-style questions", [(POOL5, 7), (g_scale, 4), (g_ivg, 3), (g_w, 3), (g_rho, 3)]),
    ])
    make_ol(LV, SUBJ, "current-of-electricity", SORT, "Current of Electricity",
            "State that current is a rate of flow of charge and recall and apply Q = It; distinguish between conventional current and electron flow; define electromotive "
            "force and potential difference as work done per unit charge and apply V = W ÷ Q; describe how to measure current and potential difference with ammeters and "
            "voltmeters; define resistance and apply R = V ÷ I; recall and apply R = ρL ÷ A; sketch and interpret the I-V characteristics of a metallic conductor at "
            "constant temperature, a filament lamp and a semiconductor diode (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Current of Electricity", "Current of electricity",
            "Free Secondary 4 O-Level Physics worksheets on current of electricity: charge and current (Q = It), e.m.f. and potential difference, resistance, resistivity and "
            "I-V graphs. 100 questions with answers.",
            "Q = It, V = W ÷ Q, R = V ÷ I", "R = ρL ÷ A: longer wire, more resistance; thicker wire, less.",
            "<p><b>Current is the rate of flow of charge.</b></p><ul>"
            "<li>Q = It (coulombs = amperes × seconds). Conventional current flows from + to −; electrons flow from − to +.</li>"
            "<li>E.m.f. and p.d. are work done per unit charge: V = W ÷ Q (1 V = 1 J/C).</li>"
            "<li>Resistance R = V ÷ I (ohms). For a wire R = ρL ÷ A, where ρ is the resistivity (Ω m).</li>"
            "<li>I-V graphs: resistor at constant temperature is a straight line through the origin; a filament lamp curves (R rises when hot); a diode conducts one way only.</li></ul>",
            [("3 A flows for 2 min. Charge?", ["t = 120 s", "Q = 3 × 120"], "360 C"),
             ("6 V across a resistor, 0.3 A through it. Resistance?", ["R = 6 ÷ 0.3"], "20 Ω")],
            ["Thinking current is used up in a lamp.", "Writing R = I ÷ V.", "Forgetting to change minutes into seconds or mA into A.",
             "Thinking a thicker wire has more resistance. It has less (larger area)."],
            [("What is the difference between e.m.f. and potential difference?", "E.m.f. is the energy per unit charge supplied by a source to drive charge round the whole circuit; p.d. is the energy per unit charge transferred in one component."),
             ("How does the length and thickness of a wire affect its resistance?", "Resistance is proportional to length and inversely proportional to cross-sectional area: R = ρL ÷ A."),
             ("Why is the I-V graph of a filament lamp curved?", "As the current rises the filament gets hotter, its resistance increases, so the current rises less for each extra volt.")],
            sets)


if __name__ == "__main__":
    main()
