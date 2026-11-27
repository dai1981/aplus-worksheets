# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 15: D.C. Circuits
  python tools/gen_sg_science_s4_dc_circuits.py
Circuit symbols; current and potential difference in series and parallel circuits; effective resistance of resistors in series
(R = R₁ + R₂) and in parallel (1/R = 1/R₁ + 1/R₂); solving circuits with V = IR; the potential divider; thermistors and
light-dependent resistors (LDRs) as input transducers.
UK series and parallel makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "parallel resistances add", "the current is shared in a series circuit", "the p.d. is the
same across every component in series", "an LDR's resistance rises in bright light".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 3
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_ser = src("gen_uk_science_y8_electricity", "g_series")
uk_par = src("gen_uk_science_y8_electricity", "g_par")
uk_pd = src("gen_uk_science_y8_electricity", "g_pd")
uk_rs = src("gen_uk_science_y10_electricity", "g_rs")


def par(*rs):
    return 1 / sum(1 / r for r in rs)


def g_par():
    k = R.choice(["two", "two", "three", "same"])
    if k == "two":
        a, b = R.choice([(2, 2), (3, 6), (4, 4), (6, 12), (10, 10), (4, 12), (12, 24), (20, 30), (10, 40), (6, 3), (5, 20), (8, 8), (30, 60), (15, 30)])
        t = par(a, b)
        return nq("Resistors of %d Ω and %d Ω are connected in parallel. What is the effective resistance?" % (a, b), t, [a + b, (a + b) / 2, 1 / a + 1 / b], " Ω",
                  "1/R = 1/%d + 1/%d, so R = %s Ω (less than the smallest resistor)." % (a, b, nf(t)))
    if k == "three":
        a, b, c = R.choice([(6, 6, 6), (2, 3, 6), (4, 6, 12), (10, 10, 5), (12, 12, 6), (3, 6, 6), (20, 20, 10)])
        t = par(a, b, c)
        return nq("Resistors of %d Ω, %d Ω and %d Ω are connected in parallel. What is the effective resistance?" % (a, b, c), t, [a + b + c, (a + b + c) / 3, 1 / a + 1 / b + 1 / c], " Ω",
                  "1/R = 1/%d + 1/%d + 1/%d, so R = %s Ω." % (a, b, c, nf(t)))
    n = R.choice([2, 3, 4, 5])
    r = R.choice([10, 20, 30, 60, 100])
    return nq("%d identical %d Ω resistors are connected in parallel. What is the effective resistance?" % (n, r), r / n, [n * r, r, r / n / 2], " Ω", "n equal resistors in parallel: R = %d ÷ %d = %s Ω." % (r, n, nf(r / n)))


def g_mix():
    """R1 in series with (R2 || R3), supply V"""
    r1 = R.choice([2, 3, 4, 5, 6, 8, 10])
    r2, r3 = R.choice([(6, 3), (4, 4), (12, 6), (6, 6), (10, 10), (12, 4), (20, 20), (6, 12)])
    p = par(r2, r3)
    tot = r1 + p
    V = R.choice([6, 9, 12, 18, 24])
    I = V / tot
    if abs(I * 100 - round(I * 100)) > 1e-6:
        return None
    k = R.choice(["R", "I", "V1", "Vp"])
    q = "A %d Ω resistor is in series with a parallel pair of %d Ω and %d Ω resistors, connected to a %d V supply. " % (r1, r2, r3, V)
    if k == "R":
        return nq(q + "What is the total resistance of the circuit?", tot, [r1 + r2 + r3, p, r1 + (r2 + r3) / 2], " Ω", "Parallel pair = %s Ω; total = %d + %s = %s Ω." % (nf(p), r1, nf(p), nf(tot)))
    if k == "I":
        return nq(q + "What current flows from the supply?", I, [V / (r1 + r2 + r3), V / r1, V / p], " A", "Total R = %s Ω; I = %d ÷ %s = %s A." % (nf(tot), V, nf(tot), nf(I)))
    if k == "V1":
        return nq(q + "What is the potential difference across the %d Ω resistor?" % r1, I * r1, [V - I * r1, V, V / 2], " V", "I = %s A; V = IR = %s × %d = %s V." % (nf(I), nf(I), r1, nf(I * r1)))
    return nq(q + "What is the potential difference across the parallel pair?", I * p, [I * r1, V, V / 2], " V", "V = %d − %s = %s V." % (V, nf(I * r1), nf(I * p)))


def g_div():
    Vin = R.choice([6, 9, 12, 15, 24])
    r1, r2 = R.choice([(1, 2), (2, 1), (1, 1), (1, 3), (3, 1), (2, 3), (1, 5), (4, 2), (10, 20), (20, 10), (3, 6)])
    unit = R.choice(["Ω", "kΩ"])
    out = Vin * r2 / (r1 + r2)
    return nq("A potential divider is made of R₁ = %d %s (top) and R₂ = %d %s (bottom) across a %d V supply. What is the output p.d. across R₂?" % (r1, unit, r2, unit, Vin), out,
              [Vin * r1 / (r1 + r2), Vin * r2 / r1, Vin / 2], " V", "V<sub>out</sub> = V<sub>in</sub> × R₂ ÷ (R₁ + R₂) = %d × %d ÷ %d = %s V." % (Vin, r2, r1 + r2, nf(out)))


SENS = [("The thermistor is R₂ (bottom) and the temperature rises.", "falls", "The thermistor's resistance falls, so it takes a smaller share of the p.d."),
        ("The thermistor is R₂ (bottom) and the temperature falls.", "rises", "The thermistor's resistance rises, so it takes a larger share of the p.d."),
        ("The LDR is R₂ (bottom) and it gets darker.", "rises", "In the dark the LDR's resistance rises, so it takes a larger share of the p.d."),
        ("The LDR is R₂ (bottom) and the light gets brighter.", "falls", "In bright light the LDR's resistance falls, so its share of the p.d. falls."),
        ("The thermistor is R₁ (top) and the temperature rises; the output is across the fixed resistor R₂.", "rises", "The thermistor's resistance falls, so the fixed resistor takes a larger share."),
        ("The LDR is R₁ (top) and it gets darker; the output is across the fixed resistor R₂.", "falls", "The LDR's resistance rises, so the fixed resistor's share falls.")]


def g_sens():
    q, a, e = R.choice(SENS)
    return tq("A potential divider has a fixed resistor and a sensor. " + q + " What happens to the output p.d. across R₂?", "It %s." % a,
              ["It %s." % ("rises" if a == "falls" else "falls"), "It stays the same.", "It becomes zero."], e)


TR = [("a thermistor", "temperature rises", "decreases"), ("a thermistor", "temperature falls", "increases"), ("a light-dependent resistor (LDR)", "light intensity increases", "decreases"),
      ("a light-dependent resistor (LDR)", "it gets darker", "increases")]


def g_tr():
    c, cond, a = R.choice(TR)
    return tq("What happens to the resistance of %s when the %s?" % (c, cond), "It %s." % a, ["It %s." % ("increases" if a == "decreases" else "decreases"), "It stays the same.", "It becomes infinite."],
              "Thermistors (NTC) and LDRs have resistances that fall as temperature or light intensity rises.")


def g_rules():
    k = R.choice(["serI", "serV", "parV", "parI"])
    if k == "serI":
        I = R.choice([0.2, 0.3, 0.5, 1.2, 2])
        return nq("Three lamps are in series. The current through the first lamp is %s A. What is the current through the third lamp?" % N(I), I, [I / 3, 3 * I, I / 2], " A", "In series the current is the same everywhere.")
    if k == "serV":
        V = R.choice([6, 9, 12, 24])
        v1 = R.choice([x for x in range(1, V) if x != V / 2])
        return nq("Two resistors are in series with a %d V supply. The p.d. across one is %d V. What is the p.d. across the other?" % (V, v1), V - v1, [V, v1, V + v1], " V",
                  "In series the p.d.s add up to the supply p.d.: %d − %d = %d V." % (V, v1, V - v1))
    if k == "parV":
        V = R.choice([3, 6, 9, 12])
        return nq("Three lamps are connected in parallel across a %d V battery. What is the p.d. across each lamp?" % V, V, [V / 3, 3 * V, V / 2], " V", "In parallel each branch has the full supply p.d.")
    I1, I2 = R.sample([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5], 2)
    return nq("Two branches are in parallel. They carry %s A and %s A. What current flows from the supply?" % (N(I1), N(I2)), I1 + I2, [abs(I1 - I2), I1 * I2, (I1 + I2) / 2], " A",
              "Currents in parallel branches add up: %s + %s = %s A." % (N(I1), N(I2), N(I1 + I2)))


POOL1 = pool(R, [
    ("What is the effective resistance of resistors in series?", "the sum of the resistances", ["the reciprocal of the sum", "the largest resistance", "the average resistance"], "R = R₁ + R₂ + …"),
    ("How does the effective resistance of two resistors in parallel compare with each one?", "It is less than the smaller of the two.", ["It is more than the larger one.", "It is the sum of the two.", "It is the same as the larger one."], "Adding a parallel path lets more current flow."),
    ("In a series circuit, how does the current compare at different points?", "It is the same at every point.", ["It decreases after each component.", "It is largest after the last lamp.", "It is shared equally."], "There is only one path."),
    ("In a parallel circuit, how does the p.d. across each branch compare with the supply p.d.?", "It is equal to the supply p.d.", ["It is shared between branches.", "It is double the supply p.d.", "It is zero."], "Each branch is connected directly across the supply."),
    ("Why are the lamps in a home connected in parallel?", "Each gets the full mains p.d. and can be switched on or off on its own.", ["To use less current overall.", "So one switch controls them all.", "So that if one fails, all go off."], "Parallel branches are independent."),
    ("In a series circuit of two lamps, one lamp breaks. What happens?", "The other lamp goes out because the circuit is broken.", ["The other lamp gets brighter.", "Nothing changes.", "The other lamp gets dimmer only."], "One path only."),
    ("Another resistor is added in parallel to a circuit. What happens to the total current from the supply?", "It increases.", ["It decreases.", "It stays the same.", "It becomes zero."], "The total resistance falls."),
    ("What is a potential divider used for?", "to provide a fraction of the supply p.d. as an output", ["to store charge", "to increase the supply p.d.", "to change a.c. into d.c."], "Two resistors in series share the p.d. in the ratio of their resistances."),
])
POOL5 = pool(R, [
    ("A light sensor switches on street lights when it gets dark. Which input transducer is used?", "a light-dependent resistor (LDR)", ["a thermistor", "a diode", "a fuse"], "The LDR's resistance rises in the dark."),
    ("A fire alarm circuit uses a thermistor. Why?", "Its resistance falls sharply as the temperature rises, changing the output p.d.", ["It produces sound.", "Its resistance rises when hot.", "It stores charge."], "An input transducer."),
    ("Two 6 Ω resistors are in parallel, and this pair is in series with a 3 Ω resistor. What is the total resistance?", "6 Ω", ["15 Ω", "3 Ω", "1.5 Ω"], "Pair = 3 Ω; 3 + 3 = 6 Ω."),
    ("A 12 V supply is connected across 4 Ω and 8 Ω resistors in series. What is the p.d. across the 8 Ω resistor?", "8 V", ["4 V", "12 V", "6 V"], "The larger resistor takes the larger share: 12 × 8 ÷ 12."),
    ("Why does a voltmeter need a very high resistance?", "So it takes almost no current and does not change the circuit it measures.", ["So it measures current accurately.", "So it heats up less.", "So it can be connected in series."], "It is connected in parallel."),
    ("Why does an ammeter need a very low resistance?", "So it does not reduce the current it is measuring.", ["So it can be connected in parallel.", "So it measures p.d.", "So it uses more power."], "It is connected in series."),
    ("Two identical lamps are connected in parallel to a cell. A third identical lamp is added in parallel. How does the brightness of each lamp change?", "It stays the same.", ["Each gets dimmer.", "Each gets brighter.", "They all go out."], "Each branch still has the full p.d. of an ideal cell."),
    ("Two identical lamps are connected in series to a cell. A third identical lamp is added in series. How does the brightness of each lamp change?", "Each gets dimmer.", ["Each gets brighter.", "It stays the same.", "Only the new lamp lights."], "The total resistance rises, so the current falls."),
    ("Which arrangement of two 10 Ω resistors gives the smallest effective resistance?", "in parallel (5 Ω)", ["in series (20 Ω)", "one alone (10 Ω)", "all arrangements are equal"], "Parallel gives less than either resistor."),
    ("A potential divider has two equal resistors across a 9 V supply. What is the output across one of them?", "4.5 V", ["9 V", "3 V", "18 V"], "Equal resistors share the p.d. equally."),
])


def main():
    sets = U.sets([
        ("Series and parallel rules", [(g_rules, 8), (uk_ser, 3), (uk_par, 3), (uk_pd, 3), POOL1]),
        ("Effective resistance", [(g_par, 9), (uk_rs, 6), POOL1]),
        ("Solving circuits", [(g_mix, 12), (g_par, 4), (POOL5, 4)]),
        ("Potential dividers and sensors", [(g_div, 7), (g_sens, 6), (g_tr, 4), POOL1]),
        ("Exam-style questions", [(POOL5, 8), (g_mix, 4), (g_div, 3), (g_sens, 3), (uk_rs, 2)]),
    ])
    make_ol(LV, SUBJ, "dc-circuits", SORT, "D.C. Circuits",
            "Draw and interpret circuit diagrams with standard symbols; state that the current at every point in a series circuit is the same and that the sum of the "
            "p.d.s across the components equals the supply p.d.; state that in parallel circuits the current from the source is the sum of the branch currents and the p.d. "
            "across each branch is the same; recall and calculate effective resistance in series and in parallel; solve circuit problems using V = IR; describe the action "
            "of a potential divider and of thermistors and light-dependent resistors as input transducers (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "D.C. Circuits", "D.C. circuits",
            "Free Secondary 4 O-Level Physics worksheets on D.C. circuits: series and parallel circuits, effective resistance, solving circuits with V = IR, potential "
            "dividers, thermistors and LDRs. 100 questions with answers.",
            "Series: R = R₁ + R₂. Parallel: 1/R = 1/R₁ + 1/R₂.", "Series: same current. Parallel: same p.d.",
            "<p><b>Series and parallel circuits follow different rules.</b></p><ul>"
            "<li>Series: the same current everywhere; p.d.s add up to the supply p.d.; R = R₁ + R₂.</li>"
            "<li>Parallel: the same p.d. across each branch; branch currents add up; 1/R = 1/R₁ + 1/R₂, so R is less than the smallest resistor.</li>"
            "<li>Potential divider: V<sub>out</sub> = V<sub>in</sub> × R₂ ÷ (R₁ + R₂). A thermistor's resistance falls when hot; an LDR's falls in bright light.</li></ul>",
            [("4 Ω and 12 Ω in parallel?", ["1/R = 1/4 + 1/12 = 4/12"], "3 Ω"),
             ("2 Ω in series with (6 Ω ∥ 3 Ω), 12 V supply. Current?", ["pair = 2 Ω", "total = 4 Ω", "I = 12 ÷ 4"], "3 A")],
            ["Adding parallel resistances like series ones.", "Thinking the current is shared out along a series circuit.",
             "Forgetting to take the reciprocal at the end of 1/R = 1/R₁ + 1/R₂.", "Saying an LDR's resistance rises in bright light."],
            [("How do you find the effective resistance of resistors in parallel?", "Add the reciprocals: 1/R = 1/R₁ + 1/R₂, then take the reciprocal of the answer. For two resistors, R = R₁R₂ ÷ (R₁ + R₂)."),
             ("How does a potential divider work?", "Two resistors in series share the supply p.d. in the ratio of their resistances, so the output across one of them is a fraction of the supply."),
             ("How are thermistors and LDRs used in circuits?", "As one resistor in a potential divider: when temperature or light changes, their resistance changes, so the output p.d. changes and can switch on a device.")],
            sets)


if __name__ == "__main__":
    main()
