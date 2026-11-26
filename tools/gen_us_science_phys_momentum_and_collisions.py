# -*- coding: utf-8 -*-
"""
US High School Physics: Momentum and Collisions (HS-PS2-2)
  python tools/gen_us_science_phys_momentum_and_collisions.py
Use mathematical representations to support the claim that the total momentum of a system of objects is conserved when
there is no net force on the system.
Momentum p = mv, conservation of momentum in sticking collisions, collisions where one object's final velocity is
unknown, and recoil (explosions) from rest. Directions use + for right and − for left.
Wrong answers come from real mistakes: "momentum is lost in a collision", "a heavier object always has more momentum",
"ignore the sign for objects moving left", "add the speeds and divide by 2".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, uniq, safe

U = Unit(90303)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_p():
    o, m = R.choice([("baseball", 0.15), ("bowling ball", 6), ("cart", 2), ("football player", 100), ("car", 1200), ("truck", 3000), ("cyclist and bike", 80), ("soccer ball", 0.4)])
    v = R.choice([2, 3, 4, 5, 8, 10, 12, 15, 20, 25, 30, 40])
    if o in ("baseball", "soccer ball"):
        v = R.choice([10, 20, 30, 40])
    if o in ("football player", "cyclist and bike", "cart", "bowling ball"):
        v = R.choice([2, 3, 4, 5, 6, 8, 10])
    p = m * v
    k = R.choice(["p", "v", "m"])
    if not once(("p", o, v, k)):
        return None
    if k == "p":
        g = "%s kg·m/s" % num(p)
        return item("What is the momentum of a %s kg %s moving at %d m/s?" % (num(m), o, v), g, uniq(g, ["%s kg·m/s" % num(m / v, 3), "%s kg·m/s" % num(m + v), "%s kg·m/s" % num(0.5 * m * v * v), "%s kg·m/s" % num(p * 2)]),
                    "p = mv = %s × %d = %s kg·m/s." % (num(m), v, num(p)))
    if k == "v":
        g = "%d m/s" % v
        return item("A %s kg %s has a momentum of %s kg·m/s. How fast is it moving?" % (num(m), o, num(p)), g, uniq(g, ["%s m/s" % num(p * m), "%s m/s" % num(m / p, 3), "%s m/s" % num(p - m), "%d m/s" % (v * 2)]),
                    "v = p ÷ m = %s ÷ %s = %d m/s." % (num(p), num(m), v))
    g = "%s kg" % num(m)
    return item("A %s moving at %d m/s has a momentum of %s kg·m/s. What is its mass?" % (o, v, num(p)), g, uniq(g, ["%s kg" % num(p * v), "%s kg" % num(v / p, 3), "%s kg" % num(p - v), "%s kg" % num(m * 2)]),
                "m = p ÷ v = %s ÷ %d = %s kg." % (num(p), v, num(m)))


@safe
def g_stick():
    who = P.next()[0]
    m1, m2 = R.choice([1, 2, 3, 4, 5]), R.choice([1, 2, 3, 4, 5, 6])
    v1 = R.choice([2, 3, 4, 5, 6, 8, 10])
    v2 = R.choice([0, 0, 0, 1, 2, -1, -2])
    vf = (m1 * v1 + m2 * v2) / (m1 + m2)
    if vf != round(vf, 2) or not once(("st", m1, m2, v1, v2)):
        return None
    g = "%s m/s" % num(vf)
    d2 = "at rest" if v2 == 0 else ("moving at %d m/s to the right" % v2 if v2 > 0 else "moving at %d m/s to the left" % -v2)
    return item("In %s's lab, a %d kg cart moving at %d m/s to the right hits a %d kg cart %s. They stick together. What is their velocity afterward? (+ = right)" % (who, m1, v1, m2, d2), g,
                uniq(g, ["%s m/s" % num((v1 + v2) / 2), "%d m/s" % v1, "%s m/s" % num((m1 * v1 - m2 * v2) / (m1 + m2)), "%s m/s" % num(m1 * v1 / m2), "0 m/s"]),
                "(%d × %d + %d × %s) ÷ (%d + %d) = %s m/s." % (m1, v1, m2, num(v2), m1, m2, num(vf)))


@safe
def g_recoil():
    who = P.next()[0]
    case = R.choice([("a skater pushes off from a friend", "skater", "friend", (40, 70), (40, 80)), ("a cannon fires a ball", "ball", "cannon", (5, 20), (200, 800)),
                     ("an astronaut throws a tool", "tool", "astronaut", (1, 5), (80, 120)), ("a person jumps off a still boat", "person", "boat", (50, 80), (100, 300))])
    ctx, a, b, ra, rb = case
    ma = R.randint(*ra)
    mb = R.randint(*rb)
    va = R.choice([1, 2, 3, 4, 5, 6, 8, 10]) if a != "ball" else R.choice([50, 80, 100, 120, 150])
    vb = ma * va / mb
    if vb != round(vb, 2) or not once(("rc", ma, mb, va)):
        return None
    g = "%s m/s in the opposite direction" % num(vb)
    return item("Everything starts at rest; then %s. The %s (%d kg) moves at %s m/s. How does the %s (%d kg) move?" % (ctx, a, ma, num(va), b, mb), g,
                uniq(g, ["%s m/s in the same direction" % num(vb), "%s m/s in the opposite direction" % num(va), "It does not move.", "%s m/s in the opposite direction" % num(mb * va / ma, 2)]),
                "Total momentum stays 0: %d × %s = %d × v, so v = %s m/s the other way." % (ma, num(va), mb, num(vb)))


@safe
def g_after():
    m1, m2 = R.choice([2, 3, 4, 5]), R.choice([2, 3, 4, 5, 6])
    v1 = R.choice([4, 5, 6, 8, 10])
    v1f = R.choice([0, 1, 2, -1, -2])
    v2f = (m1 * v1 - m1 * v1f) / m2
    if v2f != round(v2f, 2) or v2f <= v1f or m1 * v1f ** 2 + m2 * v2f ** 2 > m1 * v1 ** 2 or not once(("af", m1, m2, v1, v1f)):
        return None
    g = "%s m/s" % num(v2f)
    after = "stops" if v1f == 0 else ("keeps moving right at %d m/s" % v1f if v1f > 0 else "bounces back at %d m/s" % -v1f)
    return item("A %d kg ball moving right at %d m/s hits a %d kg ball at rest. The first ball %s. What is the velocity of the second ball? (+ = right)" % (m1, v1, m2, after), g,
                uniq(g, ["%s m/s" % num(m1 * v1 / m2), "%d m/s" % v1, "%s m/s" % num((m1 * v1 + m1 * v1f) / m2), "%s m/s" % num(v1 - v1f)]),
                "%d × %d = %d × %s + %d × v → v = %s m/s." % (m1, v1, m1, num(v1f), m2, num(v2f)))


@safe
def g_cmp():
    a = R.choice([("a 0.15 kg baseball at 40 m/s", 6), ("a 1,000 kg car at 2 m/s", 2000), ("a 60 kg runner at 5 m/s", 300), ("a 5 kg bowling ball at 8 m/s", 40),
                  ("a 0.06 kg tennis ball at 50 m/s", 3), ("a 2,000 kg truck at 1 m/s", 2000), ("a 100 kg linebacker at 6 m/s", 600), ("an 8 kg dog at 10 m/s", 80)])
    b = R.choice([x for x in [("a 0.15 kg baseball at 40 m/s", 6), ("a 1,000 kg car at 2 m/s", 2000), ("a 60 kg runner at 5 m/s", 300), ("a 5 kg bowling ball at 8 m/s", 40),
                              ("a 0.06 kg tennis ball at 50 m/s", 3), ("a 2,000 kg truck at 1 m/s", 2000), ("a 100 kg linebacker at 6 m/s", 600), ("an 8 kg dog at 10 m/s", 80)] if x[1] != a[1]])
    if not once(("cp", tuple(sorted((a[0], b[0]))))):
        return None
    big, small = (a, b) if a[1] > b[1] else (b, a)
    first, second = sorted([a, b])
    return item("Which has more momentum: %s or %s?" % (first[0], second[0]), big[0], [small[0], "They have the same momentum.", "Neither has momentum."],
                "%s kg·m/s vs %s kg·m/s." % (num(big[1]), num(small[1])))


B1 = bank([
    ("What is momentum?", "mass times velocity", ["mass times acceleration", "force times distance", "half of mass times speed squared"], "p = mv."),
    ("What are the units of momentum?", "kg·m/s", ["N", "J", "m/s²"], "Mass × velocity."),
    ("What does the law of conservation of momentum say?", "In a closed system with no net outside force, total momentum stays the same.", ["Momentum is always lost in collisions.", "Momentum only exists for heavy objects.", "Energy and momentum are the same."], "Before = after."),
    ("Is momentum a vector?", "Yes. It has the same direction as the velocity.", ["No, it has no direction.", "Only for cars.", "Only when moving up."], "Signs matter."),
    ("What is an inelastic collision?", "a collision where objects stick together or lose kinetic energy", ["a collision with no momentum", "a collision where objects bounce perfectly", "an explosion"], "Momentum is still conserved."),
    ("A bullet and a truck move at the same speed. Which has more momentum?", "the truck", ["the bullet", "They are equal.", "Neither has momentum."], "Much more mass."),
    ("If an object is at rest, what is its momentum?", "zero", ["equal to its mass", "equal to its weight", "always positive"], "v = 0."),
    ("When a gun fires, why does it kick back?", "The bullet gets forward momentum, so the gun gets equal backward momentum.", ["The bullet pulls the gun.", "Air pushes the gun.", "Momentum is created."], "Total stays zero."),
])
B5 = bank([
    ("Two carts collide on a track. Before: total momentum 12 kg·m/s right. After the collision, what is the total momentum (no friction)?", "12 kg·m/s right", ["0 kg·m/s", "6 kg·m/s right", "24 kg·m/s right"], "Conserved."),
    ("How do rockets move in space where there is nothing to push against?", "They push gas backward, and the gas pushes the rocket forward with equal momentum.", ["They push against the air.", "Gravity pulls them.", "They cannot move in space."], "Conservation of momentum."),
    ("A student measures momentum before a collision as 8.0 and after as 7.6 kg·m/s. What is the most likely reason?", "Friction on the track took away a little momentum.", ["Momentum is never conserved.", "The carts gained mass.", "The scale is too accurate."], "Outside forces."),
    ("Why are crash tests done with carts of known mass on low-friction tracks?", "So the system is nearly closed and momentum can be compared before and after.", ["To make carts heavier.", "To increase friction.", "To slow time."], "Model a closed system."),
    ("Pool ball A hits ball B head-on and stops. Ball B moves off. What can you say?", "Ball B gets about the same momentum that ball A had.", ["Ball B has zero momentum.", "Momentum was destroyed.", "Ball B moves backward."], "Equal masses swap velocities."),
])


def body():
    think = ("<p><b>Total momentum before = total momentum after (no outside net force).</b></p>"
             "<ul><li>p = mv. Momentum has direction: use + for right and − for left.</li>"
             "<li>Sticking collision: m<sub>1</sub>v<sub>1</sub> + m<sub>2</sub>v<sub>2</sub> = (m<sub>1</sub> + m<sub>2</sub>)v<sub>f</sub>.</li>"
             "<li>Starting from rest, the pieces fly apart with equal and opposite momentum.</li></ul>")
    ex = [("3 kg at 4 m/s hits 1 kg at rest; they stick. v?", ["12 ÷ 4"], "3 m/s"),
          ("50 kg skater pushes 70 kg skater; first moves at 7 m/s. Second?", ["50 × 7 = 70 × v"], "5 m/s the other way")]
    mist = ["Thinking momentum is lost in a collision.", "Ignoring the minus sign for objects moving left.", "Averaging the speeds instead of using momentum."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Momentum", B1 + [(g_p, 12)]),
        ("Comparing momentum", [(g_p, 10), (g_cmp, 10)]),
        ("Sticking collisions", [(g_stick, 16), (g_cmp, 4)]),
        ("Recoil and bouncing", [(g_recoil, 10), (g_after, 10)]),
        ("Momentum in real systems", B5 + [(g_stick, 5), (g_after, 5), (g_recoil, 5)]),
    ])
    make("physics", "momentum-and-collisions", 3, "HS-PS2-2",
         "Use mathematical representations to support the claim that the total momentum of a system of objects is conserved when there is no net force on the system.",
         "Momentum and Collisions",
         "Momentum Worksheets: p = mv, Collisions and Conservation of Momentum (High School Physics)",
         "Momentum",
         "Free high school physics worksheets on momentum (NGSS HS-PS2-2): p = mv, conservation of momentum, sticking collisions, recoil and explosions. 100 questions with answers.",
         "Total momentum is conserved.",
         "In a closed system, momentum before a collision equals momentum after.",
         body(),
         [("What is momentum?", "Momentum is mass times velocity (p = mv). It has direction, like velocity."),
          ("When is momentum conserved?", "When no net outside force acts on the system, the total momentum stays the same in collisions and explosions."),
          ("How do you solve a sticking collision?", "Add the momenta before the collision and divide by the total mass to get the shared final velocity.")],
         sets)


if __name__ == "__main__":
    main()
