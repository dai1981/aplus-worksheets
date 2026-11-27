# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 16: Practical Electricity
  python tools/gen_sg_science_s4_practical_electricity.py
Electrical power P = VI = I²R = V²/R and energy E = VIt; the kilowatt-hour and the cost of electricity; heating effect uses;
hazards (damaged insulation, overheating cables, damp conditions); fuses and choosing a fuse rating, circuit breakers,
earthing and double insulation; the live, neutral and earth wires and why switches and fuses are in the live wire.
SG and UK power, cost and wiring makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "kWh is a unit of power", "a 13 A fuse is always the safest choice", "the fuse goes in
the neutral wire", "the earth wire carries current all the time".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 4
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

sg_cost = src("gen_sg_science_s2_electrical_systems", "g_cost")
uk_pw = src("gen_uk_science_y10_electricity", "g_pw")
uk_wire = src("gen_uk_science_y10_electricity", "g_wire")

DEV = [("an LED lamp", 10), ("a laptop charger", 65), ("a ceiling fan", 75), ("a television", 120), ("a rice cooker", 700), ("a microwave oven", 1000),
       ("an iron", 1200), ("a hair dryer", 1500), ("an air-conditioner", 1800), ("a kettle", 2200), ("a water heater", 3000)]


def g_p():
    d, Pw = R.choice(DEV)
    k = R.choice(["I", "P", "R", "E"])
    V = 230
    I = Pw / V
    if k == "I":
        return nq("%s is rated %d W, 230 V. What current does it draw?" % (d[0].upper() + d[1:], Pw), I, [Pw * V, V / Pw, Pw / 100], " A", "I = P ÷ V = %d ÷ 230 = %s A." % (Pw, nf(I)))
    if k == "R":
        Rr = V * V / Pw
        return nq("%s is rated %d W, 230 V. What is its resistance when working normally?" % (d[0].upper() + d[1:], Pw), Rr, [Pw / V, V / Pw, Pw / V ** 2], " Ω",
                  "R = V² ÷ P = 230² ÷ %d = %s Ω." % (Pw, nf(Rr)))
    if k == "E":
        t = R.choice([30, 60, 120, 300, 600])
        return nq("How much energy does %s (%d W) transfer in %d s?" % (d, Pw, t), Pw * t, [Pw / t, Pw * t / 1000, Pw * t * 60], " J", "E = Pt = %d × %d = %s J." % (Pw, t, nf(Pw * t)))
    Ii = R.choice([0.5, 1, 2, 4, 5])
    VV = R.choice([6, 12, 24, 230])
    return nq("A current of %s A flows through a device with a p.d. of %d V across it. What is its power?" % (N(Ii), VV), Ii * VV, [VV / Ii, Ii + VV, Ii * VV * Ii], " W", "P = VI = %d × %s = %s W." % (VV, N(Ii), nf(Ii * VV)))


def g_i2r():
    k = R.choice(["I2R", "V2R"])
    if k == "I2R":
        I = R.choice([0.5, 1, 2, 3, 4, 5])
        Rr = R.choice([2, 4, 5, 10, 20, 50])
        return nq("A current of %s A flows through a %d Ω resistor. What power is dissipated?" % (N(I), Rr), I * I * Rr, [I * Rr, I * Rr * Rr, I * I / Rr], " W",
                  "P = I²R = %s² × %d = %s W." % (N(I), Rr, nf(I * I * Rr)))
    V = R.choice([6, 12, 24, 230])
    Rr = R.choice([2, 4, 6, 12, 24, 50, 100])
    if V == 230 and Rr < 24:
        return None
    return nq("A %d Ω resistor is connected across %d V. What power does it dissipate?" % (Rr, V), V * V / Rr, [V / Rr, V * Rr, V * V * Rr], " W",
              "P = V² ÷ R = %d² ÷ %d = %s W." % (V, Rr, nf(V * V / Rr)))


def g_cost():
    d, Pw = R.choice(DEV[3:])
    h = R.choice([0.5, 1, 2, 3, 4, 5, 8])
    days = R.choice([1, 7, 30])
    price = R.choice([28, 30, 32])
    kwh = Pw / 1000 * h * days
    k = R.choice(["kwh", "cost"])
    per = " a day for %d days" % days if days > 1 else ""
    if k == "kwh":
        return nq("%s (%d W) is used for %s h%s. How many kWh of energy does it use?" % (d[0].upper() + d[1:], Pw, N(h), per), kwh, [Pw * h * days, kwh * 60, Pw / 1000 * h], " kWh",
                  "Energy = %s kW × %s h = %s kWh." % (N(Pw / 1000), N(h * days), nf(kwh)))
    c = kwh * price
    return tq("%s (%d W) is used for %s h%s. Electricity costs %d cents per kWh. What is the cost?" % (d[0].upper() + d[1:], Pw, N(h), per, price), "$%.2f" % (c / 100),
           ["$%.2f" % (Pw * h * days * price / 100 / 100), "$%.2f" % (c / 1000), "$%.2f" % (c / 10)],
           "Energy = %s kW × %s h = %s kWh; cost = %s × %d cents = %s cents = $%.2f." % (N(Pw / 1000), N(h * days), nf(kwh), nf(kwh), price, nf(c), c / 100))


FUSES = [1, 3, 5, 10, 13]


def g_fuse():
    d, Pw = R.choice(DEV[1:])
    I = Pw / 230
    best = next((f for f in FUSES if f > I), None)
    if best is None:
        return None
    wrong = [f for f in FUSES if f != best]
    small = [f for f in wrong if f < I]
    big = [f for f in wrong if f > best]
    ws = (small[-1:] + big)[:3]
    if len(ws) < 3:
        ws = (small + big)[-3:]
    return tq("%s is rated %d W, 230 V. Which fuse should be used: 1 A, 3 A, 5 A, 10 A or 13 A?" % (d[0].upper() + d[1:], Pw), "%d A" % best, ["%d A" % f for f in ws],
              "Normal current = %d ÷ 230 = %s A. Choose the smallest fuse rating just above this: %d A." % (Pw, nf(I), best))


SAFE = [("the fuse", "melts and breaks the circuit when the current is too large, protecting the cable from overheating"),
        ("the circuit breaker", "switches off automatically when the current is too large and can be reset"),
        ("the earth wire", "provides a low-resistance path to earth so that a large current flows and blows the fuse if the metal casing becomes live"),
        ("double insulation", "means the appliance has a plastic outer casing, so the user cannot touch live metal and no earth wire is needed"),
        ("the switch in the live wire", "means the appliance is disconnected from the high p.d. when it is switched off")]
g_safe = rows(R, SAFE, "What does %s do (or mean)?", "Which safety feature %s?")

HAZ = [("damaged insulation on a cable", "a person could touch the live wire and get an electric shock"),
       ("overloading a socket with many appliances", "the large current overheats the cables and may start a fire"),
       ("using a hair dryer with wet hands in the bathroom", "water conducts, so current may flow through the person"),
       ("a cable that is too thin for the current", "the cable overheats because of its resistance and may melt the insulation")]
g_haz = rows(R, HAZ, "What is the danger of %s?")

POOL1 = pool(R, [
    ("What is electrical power?", "the rate at which electrical energy is transferred", ["the total energy used", "the current per volt", "the charge per second"], "P = VI, in watts."),
    ("What is 1 kilowatt-hour (kWh)?", "the energy transferred by a 1 kW appliance in 1 hour", ["the power of a 1 kW appliance", "1000 J", "the current in a 1 kW appliance"], "1 kWh = 3.6 × 10⁶ J."),
    ("Is the kilowatt-hour a unit of power or of energy?", "energy", ["power", "current", "charge"], "kW × h = energy."),
    ("How many joules are in 1 kWh?", "3 600 000 J", ["1000 J", "3600 J", "60 000 J"], "1000 W × 3600 s."),
    ("Which wire is the fuse connected to?", "the live wire", ["the neutral wire", "the earth wire", "any of the three"], "So the appliance is disconnected from the high p.d. when the fuse blows."),
    ("What is the mains supply in Singapore?", "230 V a.c. at 50 Hz", ["110 V d.c.", "12 V a.c.", "230 V d.c."], "Plugs have three pins: live, neutral and earth."),
    ("What colour is the live wire in a Singapore plug?", "brown", ["blue", "green and yellow", "red"], "Neutral is blue; earth is green and yellow."),
    ("What colour is the neutral wire?", "blue", ["brown", "green and yellow", "black"], "It completes the circuit."),
    ("Which wire is at a high alternating potential?", "the live wire", ["the neutral wire", "the earth wire", "all three wires"], "The neutral wire is at about 0 V."),
    ("Why do heating elements get hot?", "Current in a resistance transfers electrical energy to thermal energy (the heating effect).", ["They store charge.", "They contain magnets.", "Friction with the air."], "P = I²R."),
])
POOL5 = pool(R, [
    ("Why does a metal-cased kettle need an earth wire?", "If the live wire touches the casing, a large current flows to earth and blows the fuse, so the user does not get a shock.",
     ["To make it heat faster.", "To save electricity.", "To stop the kettle rusting."], "The casing stays at 0 V."),
    ("Why does a hair dryer with a plastic casing need no earth wire?", "It is double insulated: the user cannot touch any metal that could become live.", ["Plastic conducts electricity.", "Hair dryers use d.c.", "It has no fuse."], "Look for the double-square symbol."),
    ("Why should the fuse rating be only a little higher than the normal current?", "So it melts quickly if a fault makes the current rise, before the cable overheats.", ["So it never melts.", "So it uses less energy.", "So the appliance runs faster."], "A 13 A fuse in a lamp circuit gives little protection."),
    ("Why must a switch be placed in the live wire?", "So that when it is off, the appliance is not connected to the high p.d.", ["So it lasts longer.", "So it works faster.", "It makes no difference."], "Otherwise parts stay live even when switched off."),
    ("What is the advantage of a circuit breaker over a fuse?", "It acts faster and can be reset instead of replaced.", ["It never trips.", "It is cheaper to make.", "It increases the current."], "Many Singapore homes have them in the distribution board."),
    ("A 2 kW air-conditioner runs 8 h a day for 30 days at 30 cents per kWh. What does it cost?", "$144.00", ["$14.40", "$1440.00", "$4.80"], "2 × 8 × 30 = 480 kWh; 480 × 30 cents = 14 400 cents."),
    ("Why are thick cables used for appliances such as water heaters?", "They carry a large current, and thick cables have low resistance so they do not overheat.", ["Thick cables use less current.", "They look safer.", "They have higher resistance."], "R ∝ 1/A."),
    ("A family wants to lower its electricity bill. Which change saves the most energy?", "setting the air-conditioner a few degrees warmer", ["switching off a phone charger", "using a smaller LED lamp", "unplugging a clock"], "The air-conditioner has the largest power and runs for many hours."),
    ("A 60 W lamp and a 10 W LED give the same light. How much energy does the LED save in 1000 hours?", "50 kWh", ["50 J", "500 kWh", "5 kWh"], "(60 − 10) W × 1000 h = 50 000 Wh."),
    ("Which of these is NOT a safe practice?", "plugging many high-power appliances into one adaptor", ["using the correct fuse", "keeping appliances away from water", "replacing damaged cables"], "Overloading can cause a fire."),
])


def main():
    sets = U.sets([
        ("Electrical power", [(g_p, 9), (uk_pw, 5), POOL1]),
        ("Power and resistance", [(g_i2r, 8), (g_p, 6), POOL1]),
        ("Energy and cost", [(g_cost, 10), (sg_cost, 5), POOL1]),
        ("Safety: fuses, earthing and wiring", [(g_fuse, 6), (g_safe, 6), (g_haz, 4), (uk_wire, 4)]),
        ("Exam-style questions", [(POOL5, 9), (g_cost, 4), (g_fuse, 3), (g_i2r, 2), (g_haz, 2)]),
    ])
    make_ol(LV, SUBJ, "practical-electricity", SORT, "Practical Electricity",
            "Describe the use of the heating effect of electricity in appliances; recall and apply P = VI and E = VIt, together with P = I²R and P = V²/R; calculate the "
            "cost of using electrical appliances where the energy unit is the kWh; state the hazards of damaged insulation, overheating cables and damp conditions; "
            "explain the use of fuses and circuit breakers and the choice of fuse rating; explain the need for earthing metal cases and for double insulation; state "
            "the meaning of the terms live, neutral and earth and why switches and fuses are connected in the live wire (summary of the Singapore-Cambridge O-Level "
            "Physics 6091 syllabus).",
            "Practical Electricity", "Practical electricity",
            "Free Secondary 4 O-Level Physics worksheets on practical electricity: electrical power, energy and cost in kWh, fuses and circuit breakers, earthing, double "
            "insulation and safe wiring. 100 questions with answers.",
            "P = VI; energy (kWh) = power (kW) × time (h)", "Fuses and switches go in the live wire.",
            "<p><b>Power is the rate of transfer of electrical energy.</b></p><ul>"
            "<li>P = VI = I²R = V² ÷ R. E = VIt (J). Energy in kWh = power in kW × time in h; 1 kWh = 3.6 × 10⁶ J.</li>"
            "<li>Cost = number of kWh × price per kWh (in Singapore, about 30 cents).</li>"
            "<li>Choose a fuse rating just above the normal current. Fuses and switches go in the live wire.</li>"
            "<li>Earth metal cases so a fault current blows the fuse; double-insulated appliances need no earth wire.</li></ul>",
            [("A 1500 W hair dryer on 230 V. Current? Fuse (3 A, 5 A, 13 A)?", ["I = 1500 ÷ 230 = 6.5 A"], "6.5 A, so a 13 A fuse"),
             ("A 2.4 kW heater is used for 30 min at 30 cents per kWh. Cost?", ["2.4 × 0.5 = 1.2 kWh", "1.2 × 30"], "36 cents")],
            ["Calling the kWh a unit of power. It is a unit of energy.", "Choosing a fuse much larger than the normal current.",
             "Putting the fuse or switch in the neutral wire.", "Using minutes instead of hours when finding kWh."],
            [("How do you calculate the cost of electricity?", "Change the power into kW and the time into hours, multiply to get kWh, then multiply by the price per kWh."),
             ("How do you choose the right fuse?", "Work out the normal current with I = P ÷ V and choose the fuse with the next rating above it."),
             ("Why is the earth wire important?", "If a fault makes a metal case live, the earth wire lets a large current flow to earth, which blows the fuse and makes the appliance safe.")],
            sets)


if __name__ == "__main__":
    main()
