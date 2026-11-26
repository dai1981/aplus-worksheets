# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Physics): Electricity
  python tools/gen_uk_science_y10_electricity.py
Charge and current (Q = It), potential difference and resistance (V = IR), series and parallel circuits, total
resistance in series, I–V characteristics (resistors, filament lamps, diodes, LDRs, thermistors), power (P = IV,
P = I²R), energy transferred (E = Pt, E = QV), mains electricity (230 V, 50 Hz, live, neutral and earth wires) and the
National Grid. Reuses the V = IR, series and parallel questions of the Year 8 unit (new seed).
Wrong answers come from real mistakes: "current is used up", "the earth wire carries the current", "resistance
falls as a filament lamp heats up", "P = I × R".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build
from sci_phys import uniq, num

U, R, P, us = U4(62011)
E8 = "gen_uk_science_y8_electricity"
y8_vir, y8_ser, y8_par, y8_pd = [us.uk(E8, n) for n in ("g_vir", "g_series", "g_par", "g_pd")]


def g_q():
    k = R.choice(["Q", "I", "t"])
    i = R.choice([0.2, 0.5, 1, 1.5, 2, 3, 4, 5])
    t = R.choice([10, 20, 30, 60, 120, 300])
    if not once(("q", k, i, t)):
        return None
    q = i * t
    if k == "Q":
        g = "%s C" % num(q)
        return item("A current of %s A flows for %d s. How much charge flows? (Q = It)" % (num(i), t), g, uniq(g, ["%s C" % num(i / t), "%s C" % num(t / i), "%s C" % num(i + t), "%s C" % num(q * 10)]), "%s × %d = %s C." % (num(i), t, num(q)))
    if k == "I":
        g = "%s A" % num(i)
        return item("%s C of charge flows in %d s. What is the current?" % (num(q), t), g, uniq(g, ["%s A" % num(q * t), "%s A" % num(t / q), "%s A" % num(q), "%s A" % num(i * 10)]), "I = Q ÷ t.")
    g = "%d s" % t
    return item("How long does it take for %s C to flow with a current of %s A?" % (num(q), num(i)), g, uniq(g, ["%s s" % num(q * i), "%s s" % num(t / 2), "%s s" % num(t * 10), "%s s" % num(q)]), "t = Q ÷ I.")


def g_pw():
    k = R.choice(["IV", "I2R", "E"])
    i = R.choice([0.5, 1, 2, 3, 4, 5, 10])
    if k == "IV":
        v = R.choice([3, 6, 9, 12, 230])
        if not once(("iv", i, v)):
            return None
        p = i * v
        g = "%s W" % num(p)
        return item("A current of %s A flows through a device with a potential difference of %d V. What is its power? (P = IV)" % (num(i), v), g,
                    uniq(g, ["%s W" % num(v / i), "%s W" % num(i + v), "%s W" % num(p * 2), "%d W" % v]), "%s × %d = %s W." % (num(i), v, num(p)))
    if k == "I2R":
        r = R.choice([2, 4, 5, 10, 20, 50])
        if not once(("i2r", i, r)):
            return None
        p = i * i * r
        g = "%s W" % num(p)
        return item("A current of %s A flows through a %d Ω resistor. What power is transferred? (P = I²R)" % (num(i), r), g,
                    uniq(g, ["%s W" % num(i * r), "%s W" % num(i * i), "%s W" % num(i * r * r), "%s W" % num(p * 2)]), "%s² × %d = %s W." % (num(i), r, num(p)))
    q = R.choice([10, 20, 50, 100, 200, 500])
    v = R.choice([1.5, 3, 6, 9, 12, 230])
    if not once(("eqv", q, v)):
        return None
    e = q * v
    g = "%s J" % num(e)
    return item("%d C of charge passes through a potential difference of %s V. How much energy is transferred? (E = QV)" % (q, num(v)), g,
                uniq(g, ["%s J" % num(q / v), "%s J" % num(q + v), "%s J" % num(v), "%s J" % num(e * 10)]), "%d × %s = %s J." % (q, num(v), num(e)))


def g_rs():
    rs = R.sample([2, 3, 4, 5, 6, 8, 10, 12, 15, 20], R.choice([2, 3]))
    v = R.choice([6, 12, 24])
    k = R.choice(["tot", "cur"])
    if not once(("rs", tuple(sorted(rs)), k)):
        return None
    t = sum(rs)
    names = ", ".join("%d Ω" % x for x in rs[:-1]) + " and %d Ω" % rs[-1]
    if k == "tot":
        g = "%d Ω" % t
        return item("Resistors of %s are connected in series. What is the total resistance?" % names, g, uniq(g, ["%d Ω" % max(rs), "%d Ω" % min(rs), "%s Ω" % num(t / len(rs)), "%d Ω" % (t * 2)]), "In series, R total = R₁ + R₂ + …")
    i = v / t
    if i * 100 != int(i * 100):
        return None
    g = "%s A" % num(i)
    return item("Resistors of %s are in series with a %d V battery. What is the current?" % (names, v), g, uniq(g, ["%s A" % num(v * t), "%s A" % num(v / max(rs)), "%s A" % num(t / v), "%s A" % num(i * 2)]), "R = %d Ω, I = V ÷ R = %d ÷ %d." % (t, v, t))


IV = [("a fixed resistor (at constant temperature)", "a straight line through the origin: current is directly proportional to potential difference"),
      ("a filament lamp", "a curve: resistance increases as the filament gets hotter"),
      ("a diode", "current flows in one direction only: resistance is very high in reverse")]
SENS = [("a thermistor", "temperature rises", "decreases"), ("a light-dependent resistor (LDR)", "light gets brighter", "decreases"), ("a thermistor", "temperature falls", "increases"), ("an LDR", "it gets darker", "increases")]


def g_iv():
    if R.random() < 0.5:
        c, d = R.choice(IV)
        if not once(("iv", c)):
            return None
        return item("What does the I–V graph for %s look like?" % c, d[0].upper() + d[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in IV if x[0] != c] + ["A horizontal line: no current ever flows."], "I–V characteristics.")
    c, cond, a = R.choice(SENS)
    if not once(("se", c, cond)):
        return None
    return item("What happens to the resistance of %s when the %s?" % (c, cond), "It %s." % a, ["It %s." % ("increases" if a == "decreases" else "decreases"), "It stays the same.", "It becomes zero."], "Thermistors and LDRs are used in sensing circuits.")


WIRE = [("the live wire", "brown", "carries the alternating potential difference from the supply (230 V)"), ("the neutral wire", "blue", "completes the circuit and is at about 0 V"),
        ("the earth wire", "green and yellow stripes", "is a safety wire that stops the case becoming live")]


def g_wire():
    w, col, j = R.choice(WIRE)
    k = R.choice(["col", "job", "which"])
    if not once(("wi", w, k)):
        return None
    if k == "col":
        return item("What colour is %s in a UK plug?" % w, col, [x[1] for x in WIRE if x[0] != w] + ["red"], "Brown live, blue neutral, green and yellow earth.")
    if k == "job":
        return item("What does %s do?" % w, "It " + j + ".", ["It " + x[2] + "." for x in WIRE if x[0] != w] + ["It stores charge for later."], "Three-core cable.")
    return item("Which wire %s?" % j, w, [x[0] for x in WIRE if x[0] != w] + ["the fuse"], "Three-core cable.")


B1 = bank([
    ("What is electric current?", "the rate of flow of electric charge", ["the push of the battery", "the energy in a wire", "the resistance of a wire"], "Measured in amps."),
    ("What is the UK mains supply?", "alternating current at 230 V and 50 Hz", ["direct current at 12 V", "alternating current at 110 V and 60 Hz", "direct current at 230 V"], "a.c."),
    ("How does the total resistance of two resistors in parallel compare with each one?", "It is less than the smallest resistance.", ["It is the sum.", "It is more than the largest.", "It is the same as each."], "More paths."),
    ("In a series circuit, how is the potential difference of the supply shared?", "between the components, adding up to the supply p.d.", ["each gets the full p.d.", "only the first component gets any", "it is not shared"], "Series rule."),
])
B5 = bank([
    ("Why is electricity transmitted in the National Grid at very high potential difference?", "A lower current means less energy is wasted heating the cables.", ["It travels faster.", "It is safer for homes.", "It makes more energy."], "Step-up transformers."),
    ("What does a step-down transformer do?", "reduces the potential difference to a safe level for homes", ["increases the p.d. for the cables", "changes a.c. to d.c.", "stores energy"], "Near consumers."),
    ("Why is touching a live wire dangerous?", "Your body is at 0 V, so a large current could flow through you to earth.", ["The wire is cold.", "The neutral wire protects you.", "It only gives a small spark."], "Electric shock."),
    ("Why does a filament lamp's resistance increase as it gets hotter?", "The ions vibrate more and collide with electrons more often.", ["The wire gets shorter.", "Electrons speed up.", "Charge is used up."], "Higher tier explanation."),
])

if __name__ == "__main__":
  build(U, 10, "electricity", 11, "Physics", "Electricity",
      "Standard circuit symbols; electrical charge and current (Q = It); current, resistance and potential difference (V = IR); resistors and I–V characteristics of a resistor, filament lamp and diode; thermistors and LDRs; series and parallel circuits; direct and alternating potential difference; mains electricity; power (P = IV, P = I²R); energy transfers in everyday appliances (E = Pt, E = QV); the National Grid.",
      "Electricity", "Electricity",
      "Free Year 10 GCSE Combined Science worksheets on electricity: charge and current, V = IR, series and parallel circuits, I–V graphs, thermistors and LDRs, power, mains electricity and the National Grid. 100 questions with answers.",
      "V = IR, Q = It, P = IV",
      "Series: resistances add. Parallel: total resistance is less than the smallest.",
      "<p><b>Current is the rate of flow of charge.</b></p><ul><li>Q = It, V = IR, P = IV = I²R, E = Pt = QV.</li>"
      "<li>Series: same current everywhere, p.d. shared, resistances add. Parallel: same p.d. across each branch, currents add.</li>"
      "<li>UK mains: 230 V a.c. at 50 Hz. Live (brown), neutral (blue), earth (green and yellow).</li></ul>",
      [("2 A for 30 s. Charge?", ["Q = 2 × 30"], "60 C"), ("3 A through 4 Ω. Power?", ["P = I²R = 9 × 4"], "36 W")],
      ["Thinking current is used up in a circuit.", "Thinking the earth wire normally carries current.", "Using P = I × R instead of P = I²R."],
      [("What are the main electricity equations at GCSE?", "Q = It, V = IR, P = IV, P = I²R, E = Pt and E = QV."),
       ("What do the three wires in a plug do?", "The live wire (brown) carries the supply p.d., the neutral wire (blue) completes the circuit, and the earth wire (green and yellow) is a safety wire."),
       ("How do thermistors and LDRs behave?", "A thermistor's resistance falls as temperature rises. An LDR's resistance falls as light gets brighter.")],
      [("Charge and current", B1 + [(g_q, 10), (y8_ser, 6)]),
       ("Resistance", [(y8_vir, 12), (g_rs, 8)]),
       ("Series and parallel", [(y8_par, 8), (y8_pd, 6), (g_rs, 6)]),
       ("Power and energy", [(g_pw, 16), (g_iv, 4)]),
       ("Mains electricity", B5 + [(g_wire, 8), (g_iv, 2), (g_q, 6)])])
