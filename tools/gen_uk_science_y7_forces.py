# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Physics): Forces
  python tools/gen_uk_science_y7_forces.py
Forces as pushes or pulls arising from the interaction between two objects; using force arrows; adding forces along a
line to find the resultant force; balanced and unbalanced forces; contact and non-contact forces (friction, air
resistance, upthrust, tension, weight, magnetism); weight = mass × gravitational field strength; and stretching a
spring (extension proportional to force).
Wrong answers come from real mistakes: "a moving object needs a resultant force to keep moving", "mass and weight are
the same", "forces in opposite directions add up", "air resistance is a non-contact force".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61710)
R = U.R
P = People(R)


def g_res():
    a = R.choice(range(2, 41, 2))
    b = R.choice(range(2, 41, 2))
    k = R.choice(["opp", "same"])
    if not once(("re", a, b, k)):
        return None
    obj = R.choice(["a box", "a trolley", "a sledge", "a crate", "a toy car"])
    if k == "same":
        g = "%d N to the right" % (a + b)
        return item("Two people push %s to the right with forces of %d N and %d N. What is the resultant force?" % (obj, a, b), g,
                    uniq(g, ["%d N to the right" % abs(a - b), "%d N to the left" % (a + b), "0 N", "%d N to the right" % (a + b + 10)]), "Forces in the same direction add: %d + %d = %d N." % (a, b, a + b))
    if a == b:
        g = "0 N (the forces are balanced)"
        return item("%s is pushed with %d N to the right and %d N to the left. What is the resultant force?" % (obj[0].upper() + obj[1:], a, b), g,
                    ["%d N to the right" % (a + b), "%d N to the left" % a, "%d N to the right" % a], "Equal and opposite forces cancel out.")
    d = abs(a - b)
    dr = "right" if a > b else "left"
    g = "%d N to the %s" % (d, dr)
    return item("%s is pushed with %d N to the right and %d N to the left. What is the resultant force?" % (obj[0].upper() + obj[1:], a, b), g,
                uniq(g, ["%d N to the %s" % (d, "left" if dr == "right" else "right"), "%d N to the %s" % (a + b, dr), "0 N", "%d N to the %s" % (max(a, b), dr)]),
                "Opposite forces subtract: %d − %d = %d N, towards the bigger force." % (max(a, b), min(a, b), d))


MOT = [("is still and the forces on it are balanced", "It stays still."), ("is moving at a steady speed and the forces on it are balanced", "It keeps moving at the same speed in the same direction."),
       ("is moving and there is a resultant force forwards", "It speeds up."), ("is moving and there is a resultant force backwards", "It slows down."),
       ("is still and there is a resultant force to the left", "It starts to move to the left.")]


def g_bal():
    s, a = R.choice(MOT)
    obj = R.choice(["A car", "A cyclist", "A boat", "A skateboarder", "A football"])
    if not once(("ba", s, obj)) or not once(("bs", s), 3):
        return None
    return item("%s %s. What happens?" % (obj, s), a, R.sample([x[1] for x in MOT if x[1] != a], 3), "Balanced forces: no change in motion. Unbalanced forces: speeding up, slowing down or changing direction.")


NAME = [("the force that slows things down when surfaces rub together", "friction"), ("the force from the air that pushes against a moving object", "air resistance"),
        ("the upward push of a liquid or gas on an object in it", "upthrust"), ("the force of gravity pulling an object towards the Earth", "weight"),
        ("the pulling force in a stretched rope or string", "tension"), ("the force between a magnet and a piece of iron", "magnetic force"),
        ("the push of a surface back up on an object resting on it", "the normal (reaction) force"), ("the force of water slowing a swimmer", "water resistance (drag)")]


def g_name():
    d, n = R.choice(NAME)
    k = R.random() < 0.6
    if not once(("na", d, k)):
        return None
    if k:
        return item("What is the name of %s?" % d, n, R.sample([x[1] for x in NAME if x[1] != n], 3), "Learn the names of common forces.")
    nc = n in ("weight", "magnetic force")
    return item("Is %s a contact force or a non-contact force?" % n, "a non-contact force" if nc else "a contact force", ["a contact force" if nc else "a non-contact force", "it is not a force", "both at once"],
                "Gravity (weight), magnetism and electrostatic forces act at a distance; the others need contact.")


PLANET = [("Earth", 10), ("the Moon", 1.6), ("Mars", 3.7), ("Jupiter", 25)]


def g_weight():
    pl, gg = R.choice(PLANET)
    m = R.choice([2, 5, 8, 10, 20, 25, 40, 50, 60, 70, 80])
    k = R.random() < 0.7
    if not once(("we", pl, m, k)):
        return None
    w = round(m * gg, 1)
    ws = ("%g" % w)
    if k:
        g = "%s N" % ws
        return item("What is the weight of a %d kg object on %s, where g = %g N/kg?" % (m, pl, gg), g, uniq(g, ["%d N" % m, "%g N" % round(m / gg, 2), "%g N" % round(w * 10, 1), "%d kg" % m]),
                    "Weight = mass × g = %d × %g = %s N." % (m, gg, ws))
    g = "%d kg" % m
    return item("An astronaut's kit has a mass of %d kg on Earth. What is its mass on %s?" % (m, pl), g, uniq(g, ["%s kg" % ws, "%s N" % ws, "0 kg", "%d kg" % (m * 2)]),
                "Mass is the amount of matter; it does not change from place to place. Only weight changes.")


def g_spring():
    who = P.next()[0]
    k_ = R.choice([1, 2, 3, 4, 5])
    loads = [0, 1, 2, 3, 4, 5]
    ext = [k_ * x for x in loads]
    q = R.choice(["read", "predict", "pattern", "force"])
    ri = R.randrange(1, 6)
    if not once(("sp", k_, q, ri if q in ("read", "force") else 0)):
        return None
    tab = table(["Force (N)", "Extension (cm)"], [[str(a), str(b)] for a, b in zip(loads, ext)])
    intro = tab + "%s hung weights on a spring and measured how much it stretched. " % who
    if q == "read":
        g = "%d cm" % ext[ri]
        return item(intro + "What was the extension with a force of %d N?" % loads[ri], g, uniq(g, ["%d cm" % x for x in ext] + ["%d cm" % loads[ri]]), "Read the row.")
    if q == "predict":
        g = "%d cm" % (k_ * 7)
        return item(intro + "If the pattern continues, what would the extension be with 7 N?", g, uniq(g, ["%d cm" % (k_ * 6), "7 cm", "%d cm" % (k_ * 7 + k_), "%d cm" % (ext[5] + 2)]),
                    "Each 1 N stretches it %d cm, so 7 × %d = %d cm." % (k_, k_, k_ * 7))
    if q == "pattern":
        return item(intro + "What pattern do the results show?", "The extension is proportional to the force: double the force, double the stretch.", ["The extension stays the same.", "The spring gets shorter as force increases.", "The extension halves as the force doubles."],
                    "A straight-line pattern through zero.")
    g = "%d N" % loads[ri]
    return item(intro + "Which force made the spring stretch by %d cm?" % ext[ri], g, uniq(g, ["%d N" % x for x in loads] + ["%d N" % ext[ri]]), "Read the table backwards.")


B1 = bank([
    ("What is a force?", "a push or a pull", ["a type of energy", "a kind of mass", "a speed"], "Forces come from interactions between objects."),
    ("What is the unit of force?", "the newton (N)", ["the kilogram (kg)", "the metre (m)", "the joule (J)"], "Named after Isaac Newton."),
    ("What measures force?", "a newton meter", ["a thermometer", "a ruler", "a measuring cylinder"], "It has a spring inside."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter (kg); weight is the force of gravity on it (N).", ["They are the same.", "Weight is in kg.", "Mass changes on the Moon."], "Weight depends on gravity."),
    ("What is gravitational field strength on Earth?", "about 10 N/kg", ["about 1 N/kg", "about 100 N/kg", "0 N/kg"], "Each kilogram weighs about 10 N."),
    ("What are balanced forces?", "forces that are equal in size and opposite in direction", ["forces that are all in the same direction", "any two forces", "forces that are always zero"], "No change in motion."),
    ("What is a resultant force?", "the single force that has the same effect as all the forces together", ["the biggest force", "the weight only", "the force of friction only"], "Add forces along a line."),
    ("What do force arrows show?", "the size and direction of a force", ["the speed of an object", "the colour of an object", "the mass of an object"], "Longer arrow, bigger force."),
])
B5 = bank([
    ("A skydiver falls at a steady speed. What can you say about the forces on her?", "Her weight and the air resistance are balanced.", ["There is no gravity.", "Air resistance is bigger than weight.", "Weight is much bigger than air resistance."], "Terminal velocity."),
    ("Why does a ship float?", "The upthrust from the water balances its weight.", ["It has no weight.", "Water pulls it up with magnets.", "Air resistance holds it up."], "Balanced forces."),
    ("Why do astronauts bounce around on the Moon?", "Their weight is less because the Moon's gravity is weaker.", ["Their mass is less.", "There is no gravity at all.", "The Moon is made of springs."], "Weaker gravitational field."),
    ("Does a car moving at a steady speed on a flat road need a resultant force?", "No. The driving force balances friction and air resistance.", ["Yes, a big forward force.", "Yes, a backward force.", "Cars cannot move steadily."], "Newton's first law."),
    ("How could you check that a spring stretches in proportion to the force?", "Add equal weights one at a time and measure the extension each time.", ["Add all the weights at once.", "Use a different spring each time.", "Measure only once."], "Fair test."),
])


def body():
    think = ("<p><b>A force is a push or a pull, measured in newtons (N).</b></p>"
             "<ul><li>Add forces in the same direction; subtract opposite ones. The answer is the resultant force.</li>"
             "<li>Balanced forces: no change in motion. Unbalanced forces: speeding up, slowing down or turning.</li>"
             "<li>Weight = mass × g. On Earth g ≈ 10 N/kg. Mass does not change; weight does.</li></ul>")
    ex = [("30 N right, 12 N left. Resultant?", ["30 − 12"], "18 N to the right"),
          ("Weight of 5 kg on Earth?", ["5 × 10"], "50 N")]
    mist = ["Thinking a moving object needs a resultant force to keep moving.", "Thinking mass and weight are the same.", "Adding forces that point in opposite directions."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What forces are", B1 + [(g_name, 12)]),
        ("Resultant forces", [(g_res, 16), (g_name, 4)]),
        ("Balanced and unbalanced", [(g_bal, 12), (g_res, 8)]),
        ("Weight and mass", [(g_weight, 20)]),
        ("Stretching springs", B5 + [(g_spring, 15)]),
    ])
    make_ks3(7, "forces", 10, "Physics", "Motion and forces",
             "Forces as pushes or pulls, arising from the interaction between two objects; using force arrows in diagrams, adding forces in one dimension, balanced and unbalanced forces; moment as the turning effect of a force; forces: associated with deforming objects; stretching and squashing – springs; with rubbing and friction between surfaces, with pushing things out of the way; resistance to motion of air and water; forces measured in newtons, measurements of stretch or compression as force is changed; force-extension linear relation; non-contact forces: gravity forces acting at a distance on Earth and in space; weight = mass × gravitational field strength.",
             "Forces",
             "Year 7 Science: Forces Worksheets (Resultant Force, Weight and Mass, Springs)",
             "Forces",
             "Free Year 7 science worksheets on forces: types of force, force arrows, resultant force, balanced and unbalanced forces, weight and mass, and stretching springs. 100 questions with answers.",
             "Forces are pushes or pulls, measured in newtons.",
             "Resultant force decides how motion changes. Weight = mass × g.",
             body(),
             [("How do you find the resultant force?", "Add forces acting in the same direction and subtract forces acting in opposite directions. The resultant points the way of the bigger total."),
              ("What happens when forces are balanced?", "The motion does not change: a still object stays still and a moving object keeps moving at the same speed in the same direction."),
              ("What is the difference between mass and weight?", "Mass (kg) is the amount of matter and is the same everywhere. Weight (N) is the pull of gravity: weight = mass × g, which is about 10 N/kg on Earth.")],
             sets)


if __name__ == "__main__":
    main()
