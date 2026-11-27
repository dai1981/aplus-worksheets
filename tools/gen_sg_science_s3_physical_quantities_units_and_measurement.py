# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 1: Physical Quantities, Units and Measurement
  python tools/gen_sg_science_s3_physical_quantities_units_and_measurement.py
Base quantities and SI units, prefixes (nano to giga), scalars and vectors, adding two vectors (parallel and at right angles),
choosing instruments with a suitable precision, significant figures, random and systematic errors, averaging repeated readings
and timing many oscillations of a pendulum.
Wrong answers come from real mistakes: "mass is a vector", "1 mA = 1000 A", "a zero error is a random error",
"the resultant of 3 N and 4 N at right angles is 7 N".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, fx, trim, rows, pool, upto, ex

LV, SUBJ, SORT = 3, "Physics", 1
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

BASE = [("mass", "kilogram (kg)"), ("length", "metre (m)"), ("time", "second (s)"), ("electric current", "ampere (A)"),
        ("thermodynamic temperature", "kelvin (K)"), ("amount of substance", "mole (mol)")]
g_si = rows(R, BASE, "What is the SI base unit of %s?", "Which base quantity has the SI unit %s?")

PRE = [("giga", "G", 9), ("mega", "M", 6), ("kilo", "k", 3), ("centi", "c", -2), ("milli", "m", -3), ("micro", "µ", -6), ("nano", "n", -9)]
g_pre_word = rows(R, [(p, "10<sup>%s</sup>" % str(e).replace("-", "−")) for p, s, e in PRE], "What power of ten does the prefix %s stand for?",
                  "Which prefix stands for %s?")

QTY = [("m", "length"), ("g", "mass"), ("A", "current"), ("s", "time"), ("W", "power"), ("J", "energy"), ("V", "potential difference"), ("Hz", "frequency")]


N = lambda x: trim(nf(x))


def g_conv():
    p, s, e = R.choice([x for x in PRE if x[1] != "c"] + [("centi", "c", -2)])
    u, what = R.choice(QTY if s != "c" else [("m", "length")])
    if s == "k" and u == "g":
        u = "g"
    v = R.choice([1.5, 2, 2.5, 4, 12, 25, 45, 120, 250, 360, 800])
    val = v * 10 ** e
    a = N(val) + " " + u
    wr = [N(v * 10 ** (-e)) + " " + u, N(v * 10 ** (e + 3)) + " " + u, N(v * 10 ** (e - 3)) + " " + u, N(v * 10 ** (e + 1)) + " " + u]
    return tq("Convert %s %s%s into %s." % (N(v), s, u, u), a, wr, "%s means × 10<sup>%s</sup>, so %s %s%s = %s." % (p, str(e).replace("-", "−"), N(v), s, u, a))


def g_conv2():
    k = R.choice(["mm-m", "cm-m", "g-kg", "ms-s", "km-m", "cm3-m3", "cm2-m2"])
    v = R.choice([2, 5, 8, 12, 25, 40, 60, 150, 250, 400, 750])
    if k == "mm-m":
        return nq("A wire is %d mm long. What is its length in metres?" % v, v / 1000, [v / 100, v / 10, v * 1000], " m", "1 mm = 0.001 m.")
    if k == "cm-m":
        return nq("A table is %d cm long. What is its length in metres?" % v, v / 100, [v / 1000, v / 10, v * 100], " m", "1 cm = 0.01 m.")
    if k == "g-kg":
        return nq("An apple has a mass of %d g. What is its mass in kilograms?" % v, v / 1000, [v / 100, v * 1000, v / 10], " kg", "1 g = 0.001 kg.")
    if k == "ms-s":
        return nq("A camera flash lasts %d ms. How long is this in seconds?" % v, v / 1000, [v / 100, v * 1000, v / 10], " s", "1 ms = 0.001 s.")
    if k == "km-m":
        return nq("A runner covers %s km. How far is this in metres?" % nf(v / 10), v * 100, [v / 10000, v * 10, v * 1000], " m", "1 km = 1000 m.")
    if k == "cm3-m3":
        return nq("A block has a volume of %d cm³. What is its volume in m³?" % (v * 100), v * 100 / 1e6, [v * 100 / 100, v * 100 / 1000, v * 100 / 1e4], " m³",
                  "1 m³ = 100 × 100 × 100 cm³ = 1 000 000 cm³.")
    return nq("A tile has an area of %d cm². What is its area in m²?" % (v * 10), v * 10 / 1e4, [v * 10 / 100, v * 10 / 1000, v * 10 / 1e6], " m²",
              "1 m² = 100 × 100 cm² = 10 000 cm².")


SV = [("mass", "scalar"), ("distance", "scalar"), ("speed", "scalar"), ("time", "scalar"), ("energy", "scalar"), ("temperature", "scalar"), ("density", "scalar"),
      ("power", "scalar"), ("pressure", "scalar"), ("work done", "scalar"),
      ("displacement", "vector"), ("velocity", "vector"), ("acceleration", "vector"), ("force", "vector"), ("weight", "vector"), ("friction", "vector")]


def g_sv():
    q, a = R.choice(SV)
    if R.random() < 0.5:
        return tq("Is %s a scalar or a vector quantity?" % q, "a %s" % a, ["a %s" % ("vector" if a == "scalar" else "scalar"), "both", "neither: it has no unit"],
                  "A vector has magnitude and direction; a scalar has magnitude only. %s is a %s." % (q[0].upper() + q[1:], a))
    if a == "vector":
        others = [x for x, y in SV if y == "scalar"]
        return tq("Which of these is a vector quantity?", q, R.sample(others, 3), "%s has a direction as well as a size." % (q[0].upper() + q[1:]))
    others = [x for x, y in SV if y == "vector"]
    return tq("Which of these is a scalar quantity?", q, R.sample(others, 3), "%s has size only, no direction." % (q[0].upper() + q[1:]))


TRI = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25), (15, 20, 25), (20, 21, 29)]


def g_vec():
    k = R.choice(["perp", "perp", "same", "opp"])
    what, u = R.choice([("forces", "N"), ("forces", "N"), ("displacements", "m"), ("velocities", "m/s")])
    if k == "perp":
        a, b, c = R.choice(TRI)
        return nq("Two %s of %d %s and %d %s act at right angles to each other. What is the size of the resultant?" % (what, a, u, b, u), c,
                  [a + b, b - a, (a + b) / 2], " " + u, "Use Pythagoras: √(%d² + %d²) = %d %s." % (a, b, c, u))
    a, b = R.sample([2, 3, 4, 5, 6, 8, 10, 12, 15, 20], 2)
    if k == "same":
        return nq("Two %s of %d %s and %d %s act in the same direction. What is the size of the resultant?" % (what, a, u, b, u), a + b,
                  [abs(a - b), math.hypot(a, b), a * b], " " + u, "Same direction: add them, %d + %d = %d %s." % (a, b, a + b, u))
    return nq("Two %s of %d %s and %d %s act in opposite directions. What is the size of the resultant?" % (what, a, u, b, u), abs(a - b),
              [a + b, math.hypot(a, b), (a + b) / 2], " " + u, "Opposite directions: subtract, %d − %d = %d %s." % (max(a, b), min(a, b), abs(a - b), u))


def g_avg():
    what, u, bases = R.choice([("time for 20 swings of a pendulum", "s", [28.4, 31.6, 35.2, 40.0, 24.8]), ("length of a spring", "cm", [12.4, 15.6, 20.2, 8.8]),
                               ("time for a ball to roll down a ramp", "s", [2.4, 3.1, 4.6, 5.2]), ("distance a toy car travels", "cm", [45.8, 64.0, 82.5, 120.3])])
    base = R.choice(bases)
    d = R.sample([-0.2, -0.1, 0.0, 0.1, 0.2, 0.3, -0.3], 3)
    xs = [round(base + x, 1) for x in d]
    m = sum(xs) / 3
    return nq("A student measures the %s three times: %s %s, %s %s and %s %s. What is the average value?" % (what, xs[0], u, xs[1], u, xs[2], u),
              m, [sum(xs), max(xs) - min(xs), (max(xs) + min(xs)) / 2 + 0.1], " " + u, "Average = (%s + %s + %s) ÷ 3 = %s %s." % (xs[0], xs[1], xs[2], nf(m), u), keep=True)


ERR = [("A metre rule's zero end is worn away, so every length reads 2 mm too long.", "a systematic error"),
       ("A balance shows 0.3 g before anything is put on it.", "a systematic error"),
       ("The student starts and stops the stopwatch a little early or late each time.", "a random error"),
       ("Readings of the same length differ slightly because the student's eye is not always in line with the mark.", "a random error"),
       ("A thermometer always reads 1 °C higher than the true temperature.", "a systematic error"),
       ("A spring's length is read while it is still bouncing slightly, so readings scatter.", "a random error"),
       ("An ammeter needle points to 0.1 A when no current flows.", "a systematic error"),
       ("Wind makes a pendulum's swing time vary a little from trial to trial.", "a random error")]


def g_err():
    q, a = R.choice(ERR)
    return tq(q + " What kind of error is this?", a, ["a %s error" % ("random" if "systematic" in a else "systematic"), "no error: the reading is exact", "a unit error"],
              "A systematic error shifts every reading the same way (fix it, e.g. correct the zero). A random error scatters readings (repeat and average).")


SFQ = [("0.0250", 3), ("3.40", 3), ("1200.", 4), ("0.5", 1), ("2.008", 4), ("45.0", 3), ("0.00760", 3), ("6.02", 3), ("19", 2), ("0.103", 3), ("7.10", 3), ("80.04", 4)]


def g_sf():
    x, n = R.choice(SFQ)
    return nq("How many significant figures are there in %s?" % x, n, [n + 1, n - 1 if n > 1 else n + 2, len(x.replace(".", ""))], "",
              "Leading zeros do not count; zeros after the first non-zero digit and trailing zeros after a decimal point do count. %s has %d significant figure%s." % (x, n, "" if n == 1 else "s"))


def g_pend():
    n = R.choice([10, 20, 25, 50])
    T = R.choice([0.8, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.2])
    t = round(n * T, 1)
    if R.random() < 0.5:
        return nq("A student times %d complete oscillations of a pendulum as %s s. What is the period?" % (n, trim(nf(t))), T, [t, t / (n / 2), t * n], " s",
                  "Period = total time ÷ number of oscillations = %s ÷ %d = %s s." % (nf(t), n, nf(T)))
    return nq("A pendulum has a period of %s s. How long do %d complete oscillations take?" % (trim(nf(T)), n), t, [T, n / T, t / 2], " s", "Time = %d × %s = %s s." % (n, nf(T), nf(t)))


INSTR = [("the length of a laboratory bench (about 2 m)", "a measuring tape"), ("the length of a pencil (about 15 cm)", "a metre rule"),
         ("the internal diameter of a beaker", "vernier calipers"), ("the diameter of a thin copper wire", "a micrometer screw gauge"),
         ("the thickness of a coin (about 2 mm)", "a micrometer screw gauge"), ("the depth of a test tube", "vernier calipers"),
         ("the time for a 100 m race", "a stopwatch"), ("the outside diameter of a test tube (about 1.6 cm)", "vernier calipers"),
         ("the length of a football field", "a measuring tape"), ("the thickness of one sheet of paper", "a micrometer screw gauge")]


def g_instr():
    q, a = R.choice(INSTR)
    others = sorted({y for x, y in INSTR if y != a} | {"a metre rule", "a measuring cylinder"} - {a})
    return tq("Which instrument is most suitable for measuring %s?" % q, a, R.sample(others, 3),
              "Precision: metre rule 0.1 cm, vernier calipers 0.01 cm, micrometer screw gauge 0.01 mm. %s suits %s." % (a[0].upper() + a[1:], q))


PREC = [("a metre rule", "0.1 cm (1 mm)"), ("vernier calipers", "0.01 cm (0.1 mm)"), ("a micrometer screw gauge", "0.01 mm"), ("a digital stopwatch", "0.01 s")]
g_prec = rows(R, PREC, "What is the precision (smallest reading) of %s?", "Which instrument has a precision of %s?", extra=["1 cm", "0.001 mm"])

POOL1 = pool(R, [
    ("What does every physical quantity consist of?", "a numerical magnitude and a unit", ["a number only", "a unit only", "a direction and a unit"], "For example 5.0 kg: 5.0 is the magnitude and kg is the unit."),
    ("Which of these is a base quantity, not a derived quantity?", "length", ["speed", "area", "density"], "Speed, area and density are derived from base quantities."),
    ("The unit of speed is m/s. Which base units is it made from?", "metre and second", ["metre and kilogram", "second and kelvin", "kilogram and second"], "Speed = distance ÷ time."),
    ("The unit of density is kg/m³. Which base quantities is it made from?", "mass and length", ["mass and time", "length and time", "mass and current"], "Density = mass ÷ volume, and volume comes from length."),
    ("What is the SI unit of force, written in base units?", "kg m/s²", ["kg m/s", "kg/m²", "kg m²/s"], "F = ma, so 1 N = 1 kg × 1 m/s²."),
    ("A length is written as 3.5 × 10⁻⁶ m. Which is the same?", "3.5 µm", ["3.5 mm", "3.5 nm", "3.5 cm"], "Micro (µ) means 10⁻⁶."),
    ("Which is the largest length?", "2 km", ["2000 cm", "2 × 10⁵ mm", "2 × 10⁸ µm"], "2 km = 2000 m; 2000 cm = 20 m; 2 × 10⁵ mm = 200 m; 2 × 10⁸ µm = 200 m."),
    ("Which is the smallest time?", "5 ns", ["5 µs", "5 ms", "0.005 s"], "Nano is 10⁻⁹, the smallest of these prefixes."),
    ("A student says 1 mA = 1000 A. What is the correct value?", "1 mA = 0.001 A", ["1 mA = 100 A", "1 mA = 0.01 A", "1 mA = 1 000 000 A"], "Milli means one thousandth."),
    ("What is meant by a vector quantity?", "a quantity with both magnitude and direction", ["a quantity with magnitude only", "a quantity with no unit", "a quantity that never changes"], "Force and velocity are vectors."),
    ("A boat heads north at 4 m/s across a river flowing east at 3 m/s. What is the boat's resultant speed?", "5 m/s", ["7 m/s", "1 m/s", "12 m/s"], "√(4² + 3²) = 5 m/s."),
    ("Why do you look straight down at a scale when you read it?", "to avoid parallax error", ["to avoid zero error", "to make the reading more precise", "to see the scale more clearly"], "Your eye must be level with the mark."),
])
POOL5 = pool(R, [
    ("Why is it better to time 20 oscillations of a pendulum than one?", "It reduces the effect of human reaction time on the result.", ["It makes the pendulum swing faster.", "It removes zero error.", "It changes the period."], "The reaction-time error is spread over 20 swings."),
    ("Why is the diameter of a wire measured at several places and averaged?", "The wire may not be perfectly uniform, so the average is more accurate.", ["It makes the micrometer precise.", "It removes parallax.", "One reading is always wrong."], "Repeat and average to reduce random errors."),
    ("100 sheets of paper make a stack 1.0 cm thick. What is the thickness of one sheet?", "0.010 cm", ["0.10 cm", "1.0 cm", "0.0010 cm"], "1.0 ÷ 100 = 0.010 cm (0.10 mm)."),
    ("A stopwatch is used to time a 100 m sprint. Why is a hand timing less accurate than an electronic timer?", "Human reaction time adds an error of about 0.2 s.", ["The stopwatch is not precise.", "The runner moves too fast to see.", "Time is a vector."], "Electronic timing starts and stops automatically."),
    ("Two forces of 6 N act on a box: one east and one west. What is the resultant force?", "0 N", ["12 N", "6 N", "8.5 N"], "Equal and opposite forces cancel."),
    ("A plane flies 400 km north and then 300 km east. What is the size of its displacement?", "500 km", ["700 km", "100 km", "350 km"], "√(400² + 300²) = 500 km."),
    ("A ruler is worn at the zero end, so a student measures from the 1.0 cm mark. The other end is at 13.4 cm. What is the length?", "12.4 cm", ["13.4 cm", "14.4 cm", "12.0 cm"], "13.4 − 1.0 = 12.4 cm."),
    ("A balance reads 0.4 g with nothing on it. A beaker then reads 52.6 g. What is the mass of the beaker?", "52.2 g", ["53.0 g", "52.6 g", "52.4 g"], "This is a zero error (systematic): 52.6 − 0.4 = 52.2 g."),
    ("How can random errors be reduced?", "by repeating the measurement and taking the average", ["by correcting the zero of the instrument", "by using a bigger unit", "by measuring only once, carefully"], "Random errors scatter readings above and below the true value."),
    ("How can a systematic error such as a zero error be removed?", "by checking the zero and correcting every reading", ["by taking more readings", "by averaging the results", "by measuring faster"], "Averaging does not remove an error that shifts every reading the same way."),
    ("Why is a measuring tape better than a metre rule for measuring the length of a corridor?", "It is long enough, so fewer readings add fewer errors.", ["It is more precise.", "It has no zero error.", "It measures in mm."], "Moving a metre rule many times adds up the errors."),
])


def main():
    sets = U.sets([
        ("Base quantities and SI units", [POOL1, (g_si, 6), (g_pre_word, 6), (g_conv, 4)]),
        ("Prefixes and unit conversions", [(g_conv, 9), (g_conv2, 8), (g_pre_word, 3), POOL1]),
        ("Scalars and vectors", [(g_sv, 9), (g_vec, 9), POOL1]),
        ("Measuring instruments", [(g_instr, 6), (g_prec, 4), (g_pend, 5), (g_avg, 5), (g_sf, 4)]),
        ("Errors and exam-style questions", [(POOL5, 8), (g_err, 5), (g_avg, 3), (g_pend, 2), (g_sf, 2), (g_vec, 2)]),
    ])
    make_ol(LV, SUBJ, "physical-quantities-units-and-measurement", SORT, "Physical Quantities, Units and Measurement",
            "Show understanding that all physical quantities consist of a numerical magnitude and a unit; recall the base quantities and their SI units (mass, length, time, "
            "current, temperature, amount of substance); use the prefixes nano, micro, milli, centi, kilo, mega and giga; distinguish between scalar and vector quantities and "
            "determine the resultant of two vectors; choose instruments to measure length and time with appropriate precision, and reduce random and systematic errors "
            "(summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Physical Quantities, Units and Measurement", "Units and measurement",
            "Free Secondary 3 O-Level Physics worksheets on physical quantities and units: SI base units, prefixes, scalars and vectors, resultant of two vectors, "
            "precision, significant figures and errors. 100 questions with answers.",
            "Every quantity = number + unit.", "Vectors have size and direction; scalars have size only.",
            "<p><b>Every physical quantity is a number with a unit.</b></p><ul>"
            "<li>SI base units: kg, m, s, A, K, mol. Prefixes: G 10⁹, M 10⁶, k 10³, c 10⁻², m 10⁻³, µ 10⁻⁶, n 10⁻⁹.</li>"
            "<li>A vector (force, velocity, displacement) has direction. Two vectors at right angles: resultant = √(a² + b²).</li>"
            "<li>Precision: metre rule 0.1 cm, vernier calipers 0.01 cm, micrometer screw gauge 0.01 mm.</li>"
            "<li>Random errors: repeat and average. Systematic errors (such as a zero error): correct every reading. Time many oscillations and divide.</li></ul>",
            [("Convert 450 mA into A.", ["milli = 10⁻³", "450 × 10⁻³"], "0.45 A"),
             ("Forces of 6 N and 8 N act at right angles. Resultant?", ["√(6² + 8²) = √100"], "10 N"),
             ("20 oscillations take 32.0 s. Period?", ["32.0 ÷ 20"], "1.60 s")],
            ["Thinking averaging removes a zero error. It only reduces random errors.",
             "Adding two perpendicular vectors as numbers (3 N + 4 N = 7 N). Use Pythagoras.",
             "Getting prefixes the wrong way round: 1 mA is 0.001 A, not 1000 A.",
             "Calling mass or speed a vector. They have no direction."],
            [("What are the SI base units?", "kilogram (mass), metre (length), second (time), ampere (current), kelvin (temperature) and mole (amount of substance)."),
             ("What is the difference between random and systematic errors?", "Random errors scatter readings above and below the true value and are reduced by averaging. Systematic errors shift every reading the same way and must be corrected."),
             ("Why time many oscillations of a pendulum?", "Reaction time adds the same error to one long timing as to a short one, so timing 20 swings and dividing by 20 gives a more accurate period.")],
            sets)


if __name__ == "__main__":
    main()
