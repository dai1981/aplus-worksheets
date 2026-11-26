# -*- coding: utf-8 -*-
"""
US High School Physics: Gravitational Force (HS-PS2-4)
  python tools/gen_us_science_phys_gravitational_force.py
Use mathematical representations of Newton's Law of Gravitation and Coulomb's Law to describe and predict the
gravitational and electrostatic forces between objects.
F = Gm₁m₂/r², the inverse-square law (changing mass and distance), weight on other worlds, and why orbits happen.
Wrong answers come from real mistakes: "double the distance halves the force", "there is no gravity in space",
"heavier objects pull on lighter ones but not the other way", "mass changes on the Moon".
"""
from fractions import Fraction
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, sci, uniq, safe

U = Unit(90305)
R = U.R
P = People(R)
USED = {}
G = 6.67e-11


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def frac(f):
    f = Fraction(f)
    if f.denominator == 1:
        return "%d times as large" % f.numerator if f.numerator != 1 else "the same size"
    if f.numerator == 1:
        return "1/%d as large" % f.denominator
    return "%d/%d as large" % (f.numerator, f.denominator)


@safe
def g_ratio():
    a = R.choice([1, 2, 3, 4, Fraction(1, 2)])
    b = R.choice([1, 2, 3, 4, Fraction(1, 2)])
    k = R.choice(["mass", "both"])
    if k == "mass":
        b = 1
        if a == 1:
            return None
    if (a, b) == (1, 1) or not once(("rt", a, b)):
        return None
    f = Fraction(a) / Fraction(b) ** 2
    ma = {1: "", 2: "One mass is doubled", 3: "One mass is tripled", 4: "One mass is made 4 times larger", Fraction(1, 2): "One mass is halved"}[a]
    db = {1: "", 2: "the distance is doubled", 3: "the distance is tripled", 4: "the distance is made 4 times larger", Fraction(1, 2): "the distance is halved"}[b]
    ch = (ma + (" and " + db if db else "")) if ma else db.capitalize()
    g = frac(f)
    w = [frac(Fraction(a) / Fraction(b)), frac(Fraction(a) * Fraction(b) ** 2), frac(Fraction(a) * Fraction(b)), frac(f * 2), frac(f / 2)]
    return item("%s. How does the gravitational force between the two objects change?" % ch, "The force becomes %s." % g, ["The force becomes %s." % x for x in uniq(g, w)],
                "F ∝ m₁m₂ ÷ r²: × %s ÷ %s² = %s." % (a, b, frac(f)))


@safe
def g_calc():
    who = P.next()[0]
    m1 = R.choice([50, 60, 70, 80, 100, 500, 1000, 2000, 5000])
    m2 = R.choice([50, 60, 70, 80, 100, 500, 1000, 2000, 5000])
    r = R.choice([0.5, 1, 2, 4, 5, 10])
    if not once(("cc", tuple(sorted((m1, m2))), r)):
        return None
    F = G * m1 * m2 / r ** 2
    g = "%s N" % sci(F)
    return item("%s calculates the gravitational force between %s kg object and a %s kg object %s m apart. What is it? (G = 6.67 × 10<sup>−11</sup> N·m²/kg²)" % (who, ("an " if str(m1)[0] == "8" else "a ") + num(m1), num(m2), num(r)), g,
                uniq(g, ["%s N" % sci(G * m1 * m2 / r), "%s N" % sci(G * m1 * m2 * r ** 2), "%s N" % sci(F * 10), "%s N" % sci(G * (m1 + m2) / r ** 2)]),
                "F = Gm₁m₂ ÷ r² = 6.67 × 10<sup>−11</sup> × %s × %s ÷ %s² = %s N." % (num(m1), num(m2), num(r), sci(F)))


WORLD = [("the Moon", 1.6), ("Mars", 3.7), ("Jupiter", 24.8), ("Venus", 8.9), ("Mercury", 3.7), ("Saturn", 10.4), ("Neptune", 11.2)]


@safe
def g_world():
    w, gw = R.choice(WORLD)
    m = R.choice([10, 20, 50, 60, 70, 80, 100, 120])
    k = R.choice(["w", "m", "cmp"])
    if not once(("wd", w, m, k)):
        return None
    if k == "w":
        g = "%s N" % num(m * gw, 1)
        return item("A %d kg rover is on %s (g = %s m/s²). What is its weight there?" % (m, w, num(gw)), g, uniq(g, ["%s N" % num(m * 9.8, 1), "%d N" % m, "%s N" % num(m / gw, 1), "%s kg" % num(m * gw, 1)]),
                    "W = mg = %d × %s = %s N." % (m, num(gw), num(m * gw, 1)))
    if k == "m":
        g = "%d kg" % m
        return item("An astronaut has a mass of %d kg on Earth. What is her mass on %s?" % (m, w), g, uniq(g, ["%s kg" % num(m * gw / 9.8, 1), "%s kg" % num(m * gw, 1), "0 kg", "%s kg" % num(m * 9.8 / gw, 1)]),
                    "Mass is the amount of matter; it does not change.")
    more = gw > 9.8
    g = "on %s" % (w if more else "Earth")
    return item("Would a %d kg backpack weigh more on Earth (g = 9.8 m/s²) or on %s (g = %s m/s²)?" % (m, w, num(gw)), g, ["on %s" % ("Earth" if more else w), "the same on both", "It has no weight on either."],
                "Weight depends on the local g.")


@safe
def g_data():
    who = P.next()[0]
    F1 = R.choice([2560, 5120, 7680, 10240, 12800])
    rs = [1, 2, 4, 8]
    Fs = [F1 / r ** 2 for r in rs]
    k = R.choice(["pat", "pred"])
    if any(f != int(f) for f in Fs) or not once(("dt", F1, k)):
        return None
    tab = table(["Distance (in Earth radii)", "Gravitational force on a probe (N)"], [[str(r), num(f)] for r, f in zip(rs, Fs)])
    if k == "pat":
        return item(tab + "What pattern do %s's data show?" % who, "Doubling the distance makes the force 1/4 as large.", ["Doubling the distance halves the force.", "The force does not change with distance.", "The force grows with distance."],
                    "Inverse-square: %s ÷ 4 = %s." % (num(F1), num(Fs[1])))
    g = "%s N" % num(F1 / 256)
    return item(tab + "Predict the force on %s's probe at 16 Earth radii." % who, g, uniq(g, ["%s N" % num(F1 / 16), "%s N" % num(Fs[-1] / 2), "0 N", "%s N" % num(F1 / 32)]), "%s ÷ 16² = %s N." % (num(F1), num(F1 / 256)))


B1 = bank([
    ("What does Newton's law of gravitation say?", "Every two masses attract with a force that grows with their masses and shrinks with the square of the distance.", ["Only planets attract each other.", "Heavier objects repel lighter ones.", "Gravity does not depend on distance."], "F = Gm₁m₂/r²."),
    ("Is there gravity in space where astronauts float?", "Yes. They float because they are in free fall around Earth.", ["No, gravity is zero in space.", "Only on the Moon.", "Only near the Sun."], "Orbit = falling around."),
    ("Earth pulls on you with 600 N. How hard do you pull on Earth?", "600 N", ["0 N", "6 N", "much less than 600 N"], "Newton's third law."),
    ("Why don't you feel the gravitational pull of a classmate?", "The force between small masses is extremely tiny.", ["People have no gravity.", "Gravity only acts on planets.", "The classroom blocks it."], "G is very small."),
    ("What keeps the Moon in orbit around Earth?", "Earth's gravity pulls it toward Earth as it moves sideways.", ["Nothing; it floats.", "The Sun pushes it.", "Magnetism."], "Centripetal force from gravity."),
    ("What is G?", "the universal gravitational constant, 6.67 × 10⁻¹¹ N·m²/kg²", ["the acceleration due to gravity", "the mass of Earth", "the weight of an object"], "Same everywhere."),
    ("Why is g smaller on the Moon than on Earth?", "The Moon has much less mass.", ["The Moon has no atmosphere.", "The Moon is closer to the Sun.", "The Moon is made of rock."], "Smaller mass → weaker pull."),
    ("What is an inverse-square law?", "the force changes with 1 ÷ distance²", ["the force changes with distance²", "the force does not change", "the force changes with 1 ÷ distance"], "Gravity and electric force."),
])
B5 = bank([
    ("Why are tides caused mostly by the Moon even though the Sun is far more massive?", "The Moon is much closer, and the difference in its pull across Earth is larger.", ["The Sun has no gravity on Earth.", "The Moon is heavier.", "Tides are caused by wind."], "Distance matters a lot."),
    ("Scientists found Neptune by noticing that Uranus was pulled off its predicted path. What did this use?", "Newton's law of gravitation to predict an unseen mass", ["Coulomb's law", "the law of reflection", "chemical analysis"], "Prediction from gravity."),
    ("A satellite moves to an orbit twice as far from Earth's center. How does Earth's pull on it change?", "It becomes 1/4 as large.", ["It becomes half as large.", "It doubles.", "It stays the same."], "Inverse square."),
    ("Why do astronauts on the International Space Station feel weightless?", "They and the station fall around Earth together.", ["There is no gravity at 400 km.", "They are too far from Earth.", "The station blocks gravity."], "Free fall."),
    ("Henry Cavendish measured G with lead balls in a lab. Why was this hard?", "The gravitational force between lab-sized masses is extremely small.", ["Lead has no gravity.", "Gravity is too strong.", "Balls move too fast."], "Tiny forces."),
])


def body():
    think = ("<p><b>Every two masses attract: F = Gm<sub>1</sub>m<sub>2</sub> ÷ r<sup>2</sup>.</b></p>"
             "<ul><li>Double one mass → double the force. Double the distance → 1/4 the force (inverse square).</li>"
             "<li>G = 6.67 × 10<sup>−11</sup> N·m²/kg², so the force between small objects is tiny.</li>"
             "<li>Weight W = mg depends on the planet; mass does not change.</li></ul>")
    ex = [("Distance tripled. Force?", ["1 ÷ 3²"], "1/9 as large"),
          ("70 kg on Mars (g = 3.7)?", ["70 × 3.7"], "259 N")]
    mist = ["Thinking doubling the distance halves the force.", "Thinking there is no gravity in space.", "Thinking mass changes on another planet."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The law of gravitation", B1 + [(g_ratio, 10), (g_world, 2)]),
        ("Changing mass and distance", [(g_ratio, 10), (g_data, 4), (g_world, 6)]),
        ("Calculating gravitational force", [(g_calc, 18), (g_ratio, 2)]),
        ("Weight on other worlds", [(g_world, 18), (g_data, 2)]),
        ("Gravity in the solar system", B5 + [(g_calc, 6), (g_world, 7), (g_data, 2)]),
    ])
    make("physics", "gravitational-force", 5, "HS-PS2-4",
         "Use mathematical representations of Newton's Law of Gravitation and Coulomb's Law to describe and predict the gravitational and electrostatic forces between objects.",
         "Gravitational Force",
         "Gravitational Force Worksheets: Newton's Law of Gravitation and Inverse Squares (Physics)",
         "Gravitational Force",
         "Free high school physics worksheets on gravitational force (NGSS HS-PS2-4): Newton's law of gravitation, the inverse-square law, weight on other planets and orbits. 100 questions with answers.",
         "Gravity weakens with distance squared.",
         "F = Gm₁m₂/r²: more mass, more force; twice the distance, 1/4 the force.",
         body(),
         [("What is Newton's law of universal gravitation?", "Every two masses attract each other with a force F = Gm₁m₂/r², where r is the distance between their centers."),
          ("What happens if the distance doubles?", "The gravitational force becomes 1/4 as large because it depends on 1 ÷ r²."),
          ("Why do astronauts float in orbit?", "Gravity still pulls on them, but they and their spacecraft are falling around Earth together.")],
         sets)


if __name__ == "__main__":
    main()
