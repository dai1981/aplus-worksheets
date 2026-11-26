# -*- coding: utf-8 -*-
"""
US High School Physics: Newton's Laws and Net Force (HS-PS2-1)
  python tools/gen_us_science_phys_newtons_laws_and_net_force.py
Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the
net force on a macroscopic object, its mass, and its acceleration.
Newton's three laws, net force from several forces, F = ma, weight W = mg, friction, and force-acceleration data.
Wrong answers come from real mistakes: "a moving object needs a force to keep moving", "action-reaction forces cancel",
"weight and mass are the same", "use the applied force instead of the net force".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90302)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


OBJ = [("shopping cart", (10, 40)), ("sled", (5, 30)), ("box", (2, 50)), ("hockey puck", (0.2, 0.2)), ("car", (800, 1500)), ("bowling ball", (6, 7)), ("wagon", (10, 25)), ("skateboarder", (40, 70))]


@safe
def g_fma():
    o, (lo, hi) = R.choice(OBJ)
    m = R.choice([x for x in range(int(lo), int(hi) + 1)] or [lo]) if lo != hi else lo
    if o == "car":
        m = R.choice([800, 900, 1000, 1200, 1500])
    a = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
    F = m * a
    k = R.choice(["F", "a", "m"])
    if F != round(F, 1) or not once(("fm", o, m, a, k)):
        return None
    if k == "F":
        g = "%s N" % num(F)
        return item("What net force gives a %s kg %s an acceleration of %s m/s²?" % (num(m), o, num(a)), g, uniq(g, ["%s N" % num(m / a), "%s N" % num(m + a), "%s N" % num(F * 9.8, 1), "%s N" % num(a / m, 3)]),
                    "F = ma = %s × %s = %s N." % (num(m), num(a), num(F)))
    if k == "a":
        g = "%s m/s²" % num(a)
        return item("A net force of %s N acts on a %s kg %s. What is its acceleration?" % (num(F), num(m), o), g, uniq(g, ["%s m/s²" % num(F * m), "%s m/s²" % num(m / F, 3), "%s m/s²" % num(F - m), "%s m/s²" % num(a * 2)]),
                    "a = F ÷ m = %s ÷ %s = %s m/s²." % (num(F), num(m), num(a)))
    g = "%s kg" % num(m)
    return item("A net force of %s N gives a %s an acceleration of %s m/s². What is the mass?" % (num(F), o, num(a)), g, uniq(g, ["%s kg" % num(F * a), "%s kg" % num(a / F, 3), "%s kg" % num(F - a), "%s kg" % num(m * 2)]),
                "m = F ÷ a = %s ÷ %s = %s kg." % (num(F), num(a), num(m)))


@safe
def g_net():
    who = P.next()[0]
    f1 = R.randint(4, 30) * 5
    f2 = R.randint(1, 25) * 5
    k = R.choice(["opp", "same", "acc"])
    if f1 == f2 or not once(("nt", f1, f2, k)):
        return None
    if k == "same":
        g = "%d N" % (f1 + f2)
        return item("%s and a friend push a stalled car in the same direction with %d N and %d N. What is the net force (ignore friction)?" % (who, f1, f2), g,
                    uniq(g, ["%d N" % abs(f1 - f2), "%d N" % max(f1, f2), "0 N", "%d N" % (f1 * f2)]), "Same direction: add. %d + %d = %d N." % (f1, f2, f1 + f2))
    big, small = max(f1, f2), min(f1, f2)
    if k == "opp":
        g = "%d N toward the %s team" % (big - small, "left")
        return item("In a tug-of-war, the left team pulls with %d N and the right team pulls with %d N. What is the net force?" % (big, small), g,
                    uniq(g, ["%d N toward the left team" % (big + small), "%d N toward the right team" % (big - small), "0 N", "%d N toward the left team" % big]), "Opposite directions: subtract; the larger force wins.")
    m = R.choice([2, 4, 5, 10, 20, 25, 50])
    a = (big - small) / m
    if a != round(a, 2):
        return None
    g = "%s m/s²" % num(a)
    return item("A %d kg crate is pushed with %d N while friction is %d N. What is its acceleration?" % (m, big, small), g, uniq(g, ["%s m/s²" % num(big / m), "%s m/s²" % num((big + small) / m), "%s m/s²" % num(big - small), "0 m/s²"]),
                "Net force = %d − %d = %d N; a = %d ÷ %d = %s m/s²." % (big, small, big - small, big - small, m, num(a)))


@safe
def g_weight():
    m = R.choice([1, 2, 5, 10, 20, 45, 50, 60, 70, 80, 100, 0.5, 2.5])
    k = R.choice(["w", "m", "moon"])
    if not once(("wt", m, k)) or (k == "moon" and not once("moon", 3)):
        return None
    w = m * 9.8
    if k == "w":
        g = "%s N" % num(w, 1)
        return item("What is the weight of a %s kg object on Earth? (g = 9.8 m/s²)" % num(m), g, uniq(g, ["%s N" % num(m), "%s N" % num(m / 9.8, 2), "%s N" % num(w * 2, 1), "%s kg" % num(w, 1)]),
                    "W = mg = %s × 9.8 = %s N." % (num(m), num(w, 1)))
    if k == "m":
        g = "%s kg" % num(m)
        return item("An object weighs %s N on Earth. What is its mass? (g = 9.8 m/s²)" % num(w, 1), g, uniq(g, ["%s kg" % num(w, 1), "%s kg" % num(w * 9.8, 1), "%s N" % num(m), "%s kg" % num(m * 2)]),
                    "m = W ÷ g = %s ÷ 9.8 = %s kg." % (num(w, 1), num(m)))
    g = "%s kg" % num(m)
    return item("An astronaut's tool has a mass of %s kg on Earth. What is its mass on the Moon (g = 1.6 m/s²)?" % num(m), g, uniq(g, ["%s kg" % num(m * 1.6, 2), "%s kg" % num(m / 6, 2), "0 kg", "%s kg" % num(m * 9.8, 1)]),
                "Mass does not change; only weight changes.")


LAWS = [("A book on a table stays at rest until someone pushes it.", 0), ("Passengers lurch forward when a bus stops suddenly.", 0), ("A hockey puck slides a long way on smooth ice.", 0),
        ("A seat belt stops you from flying forward in a crash.", 0), ("Pushing an empty cart makes it speed up more than pushing a full one.", 1),
        ("A harder kick makes a soccer ball accelerate more.", 1), ("A truck needs a bigger engine force than a car to reach the same acceleration.", 1),
        ("A small rocket accelerates faster after burning off most of its fuel.", 1), ("A swimmer pushes the water back and moves forward.", 2),
        ("A rocket pushes gas down and the gas pushes the rocket up.", 2), ("When you jump off a boat, the boat moves backward.", 2), ("A gun recoils when it is fired.", 2),
        ("A skater pushes against a wall and rolls away from it.", 2), ("A ball keeps rolling on a level floor until friction slows it.", 0)]
LN = ["Newton's first law (inertia)", "Newton's second law (F = ma)", "Newton's third law (action and reaction)"]


@safe
def g_law():
    s, k = R.choice(LAWS)
    if not once(("lw", s)):
        return None
    return item("%s Which law does this best show?" % s, LN[k], [x for x in LN if x != LN[k]] + ["the law of conservation of mass"],
                ["Objects keep doing what they are doing unless a net force acts.", "Acceleration depends on net force and mass.", "Forces come in equal and opposite pairs."][k])


@safe
def g_data():
    who = P.next()[0]
    m = R.choice([0.5, 1, 2, 2.5, 4, 5])
    k = R.choice(["mass", "pred", "trend"])
    fs = [1, 2, 3, 4, 5] if m <= 1 else [2, 4, 6, 8, 10]
    acc = [f / m for f in fs]
    if any(a != round(a, 2) for a in acc) or not once(("dt", m, k)) or (k == "trend" and not once("dtt", 3)):
        return None
    tab = table(["Net force (N)", "Acceleration (m/s²)"], [[num(f), num(a)] for f, a in zip(fs, acc)])
    if k == "mass":
        g = "%s kg" % num(m)
        return item(tab + "%s pulls a cart with different forces. What is the cart's mass?" % who, g, uniq(g, ["%s kg" % num(1 / m, 2), "%s kg" % num(fs[-1]), "%s kg" % num(acc[-1]), "%s kg" % num(m * 2)]),
                    "m = F ÷ a = %s ÷ %s = %s kg." % (num(fs[0]), num(acc[0]), num(m)))
    if k == "pred":
        f = fs[-1] + fs[0]
        g = "%s m/s²" % num(f / m)
        return item(tab + "Predict the acceleration of %s's cart with a net force of %s N." % (who, num(f)), g, uniq(g, ["%s m/s²" % num(acc[-1]), "%s m/s²" % num(f * m), "%s m/s²" % num(f / m + 2), "%s m/s²" % num(f)]),
                    "a = F ÷ m = %s ÷ %s." % (num(f), num(m)))
    return item(tab + "What relationship do %s's data show?" % who, "Acceleration is directly proportional to net force.", ["Acceleration decreases as force increases.", "Acceleration does not depend on force.", "Force and acceleration are unrelated."],
                "Double the force, double the acceleration.")


B1 = bank([
    ("What does Newton's first law say?", "An object stays at rest or moves at constant velocity unless a net force acts on it.", ["All moving objects slow down by themselves.", "Force equals mass times acceleration.", "Every force has an equal opposite force."], "Inertia."),
    ("What is inertia?", "an object's resistance to a change in its motion", ["the force of gravity", "the speed of an object", "a type of friction"], "Depends on mass."),
    ("What is net force?", "the total of all forces acting on an object, including direction", ["the largest single force", "the force of gravity only", "the mass of the object"], "Add forces as vectors."),
    ("What is the SI unit of force?", "the newton (N)", ["the kilogram", "the joule", "the watt"], "1 N = 1 kg·m/s²."),
    ("If the net force on a moving object is zero, what happens?", "It keeps moving at a constant velocity.", ["It stops right away.", "It speeds up.", "It moves in a circle."], "Balanced forces."),
    ("What is the difference between mass and weight?", "Mass is the amount of matter; weight is the force of gravity on it.", ["They are the same.", "Weight never changes.", "Mass is measured in newtons."], "W = mg."),
    ("Action and reaction forces act on…", "two different objects", ["the same object", "only heavy objects", "only moving objects"], "So they do not cancel."),
    ("Which has more inertia?", "a loaded truck", ["a bicycle", "a tennis ball", "a feather"], "More mass, more inertia."),
])
B5 = bank([
    ("A horse pulls a cart. If the cart pulls back on the horse with an equal force, how can they move?", "The horse also pushes on the ground; the net force on each object decides its motion.",
     ["They cannot move.", "The cart's force is smaller.", "Newton's third law is wrong."], "Forces on different objects."),
    ("Why do air bags and crumple zones reduce injuries?", "They make the stop take longer, so the force on the passenger is smaller.", ["They add mass.", "They remove inertia.", "They speed up the car."], "Smaller acceleration."),
    ("A student pulls a cart with a spring scale at different forces and measures acceleration. Which variable must stay the same?", "the cart's mass", ["the force", "the acceleration", "the time"], "Control variable."),
    ("An elevator moves up at a constant speed. What is the net force on it?", "zero", ["upward and large", "downward", "equal to its weight"], "Constant velocity."),
    ("A space probe drifts with its engines off. Why doesn't it stop?", "No net force acts to slow it down.", ["Space pushes it.", "Its engines are on.", "Gravity is zero everywhere."], "First law."),
])


def body():
    think = ("<p><b>Net force causes acceleration: F<sub>net</sub> = ma.</b></p>"
             "<ul><li>1st law: no net force → no change in motion. 3rd law: forces come in pairs on different objects.</li>"
             "<li>Find the net force first (add same direction, subtract opposite), then a = F<sub>net</sub> ÷ m.</li>"
             "<li>Weight W = mg (g = 9.8 m/s² on Earth). Mass stays the same everywhere.</li></ul>")
    ex = [("100 N push, 40 N friction, 20 kg box. a?", ["Net 60 N", "60 ÷ 20"], "3 m/s²"),
          ("Weight of 50 kg?", ["50 × 9.8"], "490 N")]
    mist = ["Thinking a moving object needs a force to keep moving.", "Thinking action and reaction forces cancel.", "Using the applied force instead of the net force."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Newton's laws", B1 + [(g_law, 8), (g_weight, 4)]),
        ("Net force", [(g_net, 16), (g_law, 4)]),
        ("F = ma", [(g_fma, 16), (g_weight, 4)]),
        ("Weight and friction", [(g_weight, 10), (g_net, 6), (g_fma, 4)]),
        ("Analyzing force data", B5 + [(g_data, 10), (g_fma, 5)]),
    ])
    make("physics", "newtons-laws-and-net-force", 2, "HS-PS2-1",
         "Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the net force on a macroscopic object, its mass, and its acceleration.",
         "Newton's Laws and Net Force",
         "Newton's Laws Worksheets: Net Force, F = ma and Weight (High School Physics)",
         "Newton's Laws",
         "Free high school physics worksheets on Newton's laws (NGSS HS-PS2-1): inertia, net force, F = ma, weight, friction and force-acceleration data. 100 questions with answers.",
         "Net force causes acceleration.",
         "F = ma: more force, more acceleration; more mass, less acceleration.",
         body(),
         [("What are Newton's three laws?", "1: an object keeps its motion unless a net force acts. 2: F = ma. 3: every force has an equal and opposite force on another object."),
          ("How do you find net force?", "Add forces in the same direction and subtract forces in opposite directions."),
          ("Why don't action and reaction forces cancel?", "They act on different objects, so each one affects only the object it acts on.")],
         sets)


if __name__ == "__main__":
    main()
