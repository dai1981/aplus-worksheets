# -*- coding: utf-8 -*-
"""
US High School Physics: Electric Force and Coulomb's Law (HS-PS2-4)
  python tools/gen_us_science_phys_electric_force_and_coulombs_law.py
Use mathematical representations of Newton's Law of Gravitation and Coulomb's Law to describe and predict the
gravitational and electrostatic forces between objects.
Like and unlike charges, F = kq₁q₂/r², changing charge and distance, charge in coulombs and counting electrons,
charging by friction and contact, and comparing electric and gravitational forces.
Wrong answers come from real mistakes: "protons move when objects are charged", "double distance halves the force",
"like charges attract", "electric force is weaker than gravity".
"""
from fractions import Fraction
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, sci, uniq, safe

U = Unit(90306)
R = U.R
P = People(R)
USED = {}
K = 8.99e9


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
    a = R.choice([1, 2, 3, 4])
    c = R.choice([1, 2, 3])
    b = R.choice([1, 2, 3, Fraction(1, 2)])
    if (a, b, c) == (1, 1, 1) or not once(("rt", a, b, c)):
        return None
    f = Fraction(a * c) / Fraction(b) ** 2
    parts = []
    if a != 1:
        parts.append("one charge is made %d times larger" % a)
    if c != 1:
        parts.append(("the other charge" if a != 1 else "one charge") + " is made %d times larger" % c)
    if b != 1:
        parts.append("the distance is halved" if b == Fraction(1, 2) else "the distance is made %d times larger" % b)
    ch = " and ".join(parts)
    ch = ch[0].upper() + ch[1:]
    g = frac(f)
    w = [frac(Fraction(a * c) / Fraction(b)), frac(Fraction(a * c) * Fraction(b) ** 2), frac(Fraction(a + c) / Fraction(b) ** 2), frac(f * 2), frac(f / 2)]
    return item("%s. How does the electric force between the two charges change?" % ch, "It becomes %s." % g, ["It becomes %s." % x for x in uniq(g, w)],
                "F ∝ q₁q₂ ÷ r²: %d × %d ÷ (%s)² = %s." % (a, c, b, frac(f)))


def f3(x):
    t = "%.3g" % x
    return sci(x) if "e" in t else t


@safe
def g_calc():
    who = P.next()[0]
    q1, q2 = R.choice([1, 2, 3, 4, 5]), R.choice([1, 2, 3, 4, 5, 6])
    r = R.choice([0.1, 0.2, 0.3, 0.5, 1])
    if not once(("cc", tuple(sorted((q1, q2))), r)):
        return None
    F = K * q1 * 1e-6 * q2 * 1e-6 / r ** 2
    g = "%s N" % f3(F)
    w = [K * q1 * q2 * 1e-12 / r, K * q1 * q2 * 1e-12 * r ** 2, F * 10, K * (q1 + q2) * 1e-6 / r ** 2]
    w = ["%s N" % f3(x) for x in w]
    return item("%s finds the force between a %d μC charge and a %d μC charge %s m apart. What is it? (k = 8.99 × 10<sup>9</sup> N·m²/C², 1 μC = 10<sup>−6</sup> C)" % (who, q1, q2, num(r)), g, uniq(g, w),
                "F = kq₁q₂ ÷ r² = 8.99 × 10<sup>9</sup> × %d × 10<sup>−6</sup> × %d × 10<sup>−6</sup> ÷ %s² = %s." % (q1, q2, num(r), g))


@safe
def g_sign():
    a = R.choice(["positive", "negative"])
    b = R.choice(["positive", "negative"])
    who = R.choice(["two balloons", "two pith balls", "a rod and a sphere", "two strips of tape", "two charged spheres", "a comb and a scrap of paper"])
    if not once(("sg", a, b, who)):
        return None
    t = "They repel." if a == b else "They attract."
    return item("In a demo, %s carry charges that are %s and %s. What happens?" % (who, a, b), t, ["They attract." if a == b else "They repel.", "Nothing happens.", "They become neutral right away."],
                "Like charges repel; unlike charges attract.")


@safe
def g_count():
    n = R.choice([2, 3, 5, 10, 20, 50, 100, 1000])
    k = R.choice(["n", "q"])
    sign = R.choice([-1, 1])
    if not once(("ct", n, k, sign)):
        return None
    q = sign * n * 1.6e-19
    word = "gained" if sign < 0 else "lost"
    if k == "q":
        g = "%s C" % sci(q)
        return item("A neutral object %s %s electrons. What is its charge? (e = 1.6 × 10<sup>−19</sup> C)" % (word, num(n)), g,
                    uniq(g, ["%s C" % sci(-q), "%s C" % sci(q / 1.6e-19 * 1e-19 * 10), "%s C" % sci(1.6e-19 / n * sign), "%s C" % sci(q * 2)]),
                    "q = %s × 1.6 × 10<sup>−19</sup> C, %s because electrons were %s." % (num(n), "negative" if sign < 0 else "positive", word))
    g = "%s electrons %s" % (num(n), word)
    return item("An object has a charge of %s C. How did it get this charge? (e = 1.6 × 10<sup>−19</sup> C)" % sci(q), g,
                uniq(g, ["%s electrons %s" % (num(n), "lost" if sign < 0 else "gained"), "%s protons %s" % (num(n), "lost" if sign < 0 else "gained"), "%s electrons %s" % (num(n * 2), word), "%s protons %s" % (num(n), word)]),
                "n = |q| ÷ e = %s. Only electrons move." % num(n))


RUB = [("A balloon is rubbed on hair and becomes negative.", "Electrons moved from the hair to the balloon."), ("A glass rod is rubbed with silk and becomes positive.", "Electrons moved from the glass to the silk."),
       ("You shuffle on carpet and get a shock from a doorknob.", "Extra electrons on you jump to the doorknob."), ("A charged rod touches a neutral metal sphere.", "Charge spreads onto the sphere, so both have the same sign."),
       ("A negative rod is brought near a neutral can, which rolls toward it.", "The can's electrons are pushed to the far side, so the near side is positive."),
       ("Clothes stick together after a dryer cycle.", "Tumbling transfers electrons, so clothes get opposite charges.")]


@safe
def g_rub():
    s, a = R.choice(RUB)
    if not once(("rb", s)):
        return None
    return item("%s Which explanation is best?" % s, a, R.sample([x[1] for x in RUB if x[1] != a], 2) + ["Protons moved from one object to the other."], "Only electrons move between objects.")


B1 = bank([
    ("What does Coulomb's law describe?", "the force between two electric charges", ["the force between two masses", "the speed of light", "the current in a wire"], "F = kq₁q₂/r²."),
    ("What happens when two negative charges are near each other?", "They repel.", ["They attract.", "Nothing happens.", "They become positive."], "Like charges repel."),
    ("When objects are charged by rubbing, which particles move?", "electrons", ["protons", "neutrons", "whole atoms always"], "Protons stay in the nucleus."),
    ("What is the unit of electric charge?", "the coulomb (C)", ["the newton", "the volt", "the ampere"], "e = 1.6 × 10⁻¹⁹ C."),
    ("How is Coulomb's law like Newton's law of gravitation?", "Both forces get weaker with the square of the distance.", ["Both are always attractive.", "Both are equally strong.", "Both depend only on mass."], "Inverse-square laws."),
    ("How is the electric force different from gravity?", "It can attract or repel.", ["It never changes with distance.", "It only attracts.", "It needs mass."], "Two kinds of charge."),
    ("An object gains electrons. What is its charge?", "negative", ["positive", "neutral", "it has no charge"], "Electrons are negative."),
    ("What holds the electrons in an atom near the nucleus?", "the electric attraction between electrons and protons", ["gravity", "magnetism only", "friction"], "Opposite charges."),
])
B5 = bank([
    ("Compare the electric and gravitational forces between two electrons.", "The electric force is about 10⁴² times stronger.", ["Gravity is stronger.", "They are equal.", "There is no electric force."], "Electric forces dominate at atomic scales."),
    ("Why do photocopiers and laser printers work?", "Charged toner is attracted to oppositely charged areas on a drum.", ["Toner is magnetic only.", "Gravity pulls the toner.", "Heat pushes the toner."], "Electrostatics."),
    ("Why do we not notice electric forces between everyday objects most of the time?", "Most objects are neutral, with equal positive and negative charge.", ["Electric forces are weak.", "Objects have no electrons.", "Air blocks charge."], "Balanced charge."),
    ("A student hangs two charged balloons and measures the force at 10 cm and 20 cm. What should she find?", "The force at 20 cm is about 1/4 of the force at 10 cm.", ["The forces are equal.", "The force at 20 cm is double.", "The force at 20 cm is 1/2."], "Inverse square."),
    ("Why do gas stations warn people not to slide across car seats before fueling?", "Sliding can build up charge that may spark near fuel vapor.", ["It wastes fuel.", "Seats get hot.", "It changes gravity."], "Static discharge."),
])


def body():
    think = ("<p><b>Like charges repel, unlike charges attract: F = kq<sub>1</sub>q<sub>2</sub> ÷ r<sup>2</sup>.</b></p>"
             "<ul><li>Double one charge → double the force. Double the distance → 1/4 the force.</li>"
             "<li>Objects get charged when electrons move. Gaining electrons → negative; losing → positive.</li>"
             "<li>k = 8.99 × 10<sup>9</sup> N·m²/C²; electric forces are much stronger than gravity between small particles.</li></ul>")
    ex = [("Both charges doubled, distance doubled?", ["2 × 2 ÷ 2²"], "the same size"),
          ("Gained 5 electrons. Charge?", ["5 × 1.6 × 10<sup>−19</sup>"], "−8.00 × 10<sup>−19</sup> C")]
    mist = ["Thinking protons move when objects are charged.", "Thinking doubling the distance halves the force.", "Thinking electric force is weaker than gravity."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Electric charge", B1 + [(g_sign, 8), (g_rub, 4)]),
        ("Charging objects", [(g_count, 12), (g_sign, 7), (g_rub, 1)]),
        ("Changing charge and distance", [(g_ratio, 16), (g_count, 4)]),
        ("Calculating electric force", [(g_calc, 16), (g_ratio, 4)]),
        ("Electric and gravitational forces", B5 + [(g_calc, 5), (g_ratio, 5), (g_count, 5)]),
    ])
    make("physics", "electric-force-and-coulombs-law", 6, "HS-PS2-4",
         "Use mathematical representations of Newton's Law of Gravitation and Coulomb's Law to describe and predict the gravitational and electrostatic forces between objects.",
         "Electric Force and Coulomb's Law",
         "Coulomb's Law Worksheets: Electric Charge and Electric Force (High School Physics)",
         "Coulomb's Law",
         "Free high school physics worksheets on electric force (NGSS HS-PS2-4): like and unlike charges, Coulomb's law, the inverse-square law and counting electrons. 100 questions with answers.",
         "Like charges repel; unlike attract.",
         "F = kq₁q₂/r²: bigger charges, bigger force; twice the distance, 1/4 the force.",
         body(),
         [("What is Coulomb's law?", "The electric force between two charges is F = kq₁q₂/r². It is larger for bigger charges and smaller at larger distances."),
          ("How do objects become charged?", "Electrons move from one object to another. The object that gains electrons becomes negative, and the one that loses them becomes positive."),
          ("How are electric and gravitational forces alike?", "Both follow an inverse-square law. Unlike gravity, the electric force can attract or repel.")],
         sets)


if __name__ == "__main__":
    main()
