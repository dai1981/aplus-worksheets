# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 3: Dynamics
  python tools/gen_sg_science_s3_dynamics.py
Balanced and unbalanced forces, free-body diagrams, resultant force = mass × acceleration, friction and air resistance,
mass and weight (W = mg with g = 10 N/kg), gravitational field strength, inertia.
US and UK resultant-force and F = ma makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "a moving object needs a resultant force to keep moving", "mass and weight are the same",
"weight is measured in kg", "the resultant force is the sum of all the forces whatever their direction".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ans_num, ex

LV, SUBJ, SORT = 3, "Physics", 3
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

us_fma = keep(src("gen_us_science_phys_newtons_laws_and_net_force", "g_fma"), lambda it: "m/s²" not in it["c"][0] or (ans_num(it) or 99) <= 6)
us_net = keep(src("gen_us_science_phys_newtons_laws_and_net_force", "g_net"), lambda it: "m/s²" not in it["c"][0] or (ans_num(it) or 99) <= 6)
uk_res = src("gen_uk_science_y7_forces", "g_res")
uk_wt = src("gen_uk_science_y7_forces", "g_weight")
uk_planet = keep(src("gen_uk_science_y9_gravity_and_space", "g_weight"), lambda it: "mass on Earth?" not in it["q"])

VEH = [("car", 1000, 1500, 2000, 5000), ("lorry", 8000, 12000, 8000, 20000), ("motorcycle", 200, 300, 600, 1500), ("bus", 10000, 15000, 10000, 25000)]


def g_fric():
    v, m0, m1, f0, f1 = R.choice(VEH)
    m = R.choice(range(m0, m1 + 1, 100 if m1 < 5000 else 1000))
    F = R.choice(range(f0, f1 + 1, 100 if f1 < 5000 else 500))
    fr = R.choice([x for x in range(f0 // 5, F, 100 if f1 < 5000 else 500)])
    a = (F - fr) / m
    if a <= 0 or a > 5 or (a * 100) != int(a * 100):
        return None
    k = R.choice(["a", "a", "res"])
    if k == "res":
        return nq("A %s has a driving force of %s N and resistive forces of %s N. What is the resultant force?" % (v, F, fr), F - fr, [F + fr, F, (F + fr) / 2], " N",
                  "Resultant = %s − %s = %s N in the direction of motion." % (F, fr, F - fr))
    return nq("A %s of mass %s kg has a driving force of %s N. Friction and air resistance total %s N. What is its acceleration?" % (v, m, F, fr), a,
              [F / m, (F + fr) / m, (F - fr) * m], " m/s²", "Resultant = %s − %s = %s N; a = F ÷ m = %s ÷ %s = %s m/s²." % (F, fr, F - fr, F - fr, m, N(a)))


def g_wt():
    k = R.choice(["W", "m", "Moon"])
    m = R.choice([0.2, 0.5, 1.5, 2, 4, 5, 12, 45, 60, 75, 1200])
    if k == "W":
        return nq("What is the weight of a %s kg object on Earth? (g = 10 N/kg)" % N(m), m * 10, [m, m / 10, m * 100], " N", "W = mg = %s × 10 = %s N." % (N(m), N(m * 10)))
    if k == "m":
        W = m * 10
        return nq("An object weighs %s N on Earth. What is its mass? (g = 10 N/kg)" % N(W), m, [W, W * 10, W / 100], " kg", "m = W ÷ g = %s ÷ 10 = %s kg." % (N(W), N(m)))
    m = R.choice([48, 52, 55, 60, 65, 70])
    return tq("An astronaut's mass is %d kg on Earth. What is her mass on the Moon, where g = 1.6 N/kg?" % m, "%d kg" % m,
              ["%s kg" % N(m * 1.6), "%s kg" % N(m / 6.25), "0 kg"], "Mass is the amount of matter and does not change from place to place; only weight changes.")


def g_fm():
    k = R.choice(["F", "m"])
    m = R.choice([0.5, 2, 4, 5, 8, 10, 20, 50, 800, 1200])
    a = R.choice([0.5, 1.5, 2, 3, 4, 6])
    F = m * a
    if k == "F":
        return nq("What resultant force gives a %s kg object an acceleration of %s m/s²?" % (N(m), N(a)), F, [m / a, a / m, m + a], " N", "F = ma = %s × %s = %s N." % (N(m), N(a), N(F)))
    return nq("A resultant force of %s N gives an object an acceleration of %s m/s². What is its mass?" % (N(F), N(a)), m, [F * a, a / F, F - a], " kg", "m = F ÷ a = %s ÷ %s = %s kg." % (N(F), N(a), N(m)))


def g_lift():
    m = R.choice([2, 4, 5, 10, 20, 50])
    T = m * 10 + R.choice([-1, 1]) * m * R.choice([1, 2, 3, 4])
    a = (T - m * 10) / m
    up = a > 0
    return nq("A %d kg box hangs from a rope. The rope pulls up with %d N. Taking g = 10 N/kg, what is the size of the box's acceleration?" % (m, T), abs(a),
              [T / m, (T + m * 10) / m, abs(T - m * 10)], " m/s²",
              "Weight = %d N. Resultant = %d N %s. a = %d ÷ %d = %s m/s² %s." % (m * 10, abs(T - m * 10), "upwards" if up else "downwards", abs(T - m * 10), m, N(abs(a)), "upwards" if up else "downwards"))


STATE = [("A book rests on a table.", "The forces are balanced: the resultant force is zero and it stays at rest."),
         ("A car moves along a straight road at a constant speed.", "The forces are balanced: the resultant force is zero."),
         ("A skydiver falls at terminal velocity.", "The forces are balanced: the resultant force is zero."),
         ("A cyclist speeds up along a flat road.", "The forces are unbalanced: the resultant force acts forwards."),
         ("A car brakes and slows down.", "The forces are unbalanced: the resultant force acts backwards."),
         ("A ball is dropped and speeds up as it falls (no air resistance).", "The forces are unbalanced: the resultant force acts downwards.")]


def g_state():
    q, a = R.choice(STATE)
    others = sorted({y for x, y in STATE if y != a} | {"There are no forces acting on it."})
    return tq(q + " Which statement is correct?", a, R.sample(others, 3), "Balanced forces: constant velocity (or at rest). Unbalanced forces: acceleration in the direction of the resultant force.")


MW = [("is the amount of matter in a body", "mass"), ("is the gravitational force acting on a body", "weight"), ("is measured in kilograms", "mass"), ("is measured in newtons", "weight"),
      ("changes when you go to the Moon", "weight"), ("is the same everywhere", "mass"), ("is a vector quantity", "weight"), ("is a scalar quantity", "mass"),
      ("is measured with a spring balance", "weight"), ("is a measure of inertia", "mass")]


def g_mw():
    q, a = R.choice(MW)
    return tq("Which quantity %s?" % q, a, ["weight" if a == "mass" else "mass", "density", "volume"], "Mass (kg) is the amount of matter and measures inertia; weight (N) = mg is a force.")


POOL1 = pool(R, [
    ("What is the SI unit of force?", "the newton (N)", ["the kilogram (kg)", "the joule (J)", "the watt (W)"], "1 N = 1 kg m/s²."),
    ("What does a free-body diagram show?", "all the forces acting on one object, drawn as arrows", ["the path the object takes", "the forces the object exerts on others", "the speed of the object"], "Arrow length shows the size of each force."),
    ("Two forces act on a crate: 30 N to the right and 30 N to the left. What happens if it is at rest?", "It stays at rest.", ["It moves right.", "It moves left.", "It speeds up."], "Balanced forces give zero resultant force."),
    ("A hockey puck slides on smooth ice at a steady speed. What is the resultant force on it?", "zero", ["a forward force that keeps it moving", "its weight", "a large backward force"], "No resultant force is needed to keep moving at constant velocity."),
    ("What is inertia?", "the reluctance of a body to change its state of rest or motion", ["the force that stops moving objects", "the weight of a body", "the speed of a body"], "Mass is a measure of inertia."),
    ("Why do passengers lurch forwards when a bus brakes suddenly?", "Their inertia keeps them moving forwards while the bus slows.", ["The bus pushes them forwards.", "Gravity increases.", "Friction pulls them forwards."], "Wear a seat belt."),
    ("Why is it harder to push a loaded trolley than an empty one?", "It has more mass, so more inertia.", ["It has less friction.", "It has a smaller weight.", "Its wheels are smaller."], "More mass means more force is needed for the same acceleration."),
    ("What is the gravitational field strength near the Earth's surface?", "10 N/kg", ["1 N/kg", "100 N/kg", "1.6 N/kg"], "g = 10 N/kg (10 m/s²)."),
    ("What is meant by gravitational field strength?", "the gravitational force per unit mass", ["the mass per unit weight", "the speed of falling objects", "the force per unit area"], "g = W ÷ m."),
    ("In which direction does friction act on a box sliding to the right?", "to the left", ["to the right", "upwards", "downwards"], "Friction opposes motion."),
])
POOL5 = pool(R, [
    ("A 1000 kg car accelerates at 2 m/s². Friction is 500 N. What is the driving force?", "2500 N", ["2000 N", "1500 N", "500 N"], "Resultant = ma = 2000 N; driving force = 2000 + 500 = 2500 N."),
    ("A 60 kg person stands in a lift that is at rest. What is the force from the floor on the person?", "600 N upwards", ["60 N upwards", "600 N downwards", "0 N"], "Balanced: the floor pushes up with a force equal to the weight."),
    ("The same resultant force acts on a 2 kg trolley and a 4 kg trolley. How do their accelerations compare?", "The 2 kg trolley's acceleration is twice as large.", ["They are the same.", "The 4 kg trolley's is twice as large.", "The 2 kg trolley's is four times as large."], "a = F ÷ m."),
    ("A resultant force on a trolley is doubled. What happens to its acceleration?", "It doubles.", ["It halves.", "It stays the same.", "It becomes four times larger."], "a is proportional to F for a fixed mass."),
    ("Why do tyres have treads?", "to increase friction and grip on wet roads", ["to reduce friction", "to make the car lighter", "to reduce air resistance"], "Treads push water away."),
    ("How is friction useful when walking?", "It stops your feet slipping backwards.", ["It makes you lighter.", "It pushes you upwards.", "It has no use."], "Friction acts on your shoe."),
    ("How can friction in a machine be reduced?", "by lubricating the moving parts with oil", ["by making surfaces rougher", "by adding mass", "by pushing harder"], "Less friction means less energy wasted as heat."),
    ("A box weighs 200 N on Earth. What is its weight on the Moon, where g = 1.6 N/kg?", "32 N", ["200 N", "20 N", "320 N"], "Mass = 200 ÷ 10 = 20 kg; W = 20 × 1.6 = 32 N."),
    ("A parachutist falls at a constant 6 m/s. Her weight is 700 N. What is the air resistance on her?", "700 N", ["0 N", "6 N", "4200 N"], "Constant velocity: balanced forces."),
    ("A space probe moves through deep space with its engines off, far from any planet. What happens to its motion?", "It continues at a constant velocity.", ["It slows down and stops.", "It speeds up.", "It moves in a circle."], "With no resultant force there is no acceleration."),
])


def main():
    sets = U.sets([
        ("Forces and free-body diagrams", [POOL1, (uk_res, 5), (us_net, 4), (g_state, 5)]),
        ("Resultant force and acceleration", [(g_fm, 7), (us_fma, 6), (g_fric, 5), POOL1]),
        ("Mass and weight", [(g_wt, 8), (g_mw, 6), (uk_wt, 3), (uk_planet, 3)]),
        ("Friction and motion", [(g_fric, 8), (g_lift, 6), (g_state, 3), (us_net, 3)]),
        ("Inertia and exam-style questions", [(POOL5, 10), POOL1, (g_lift, 3), (g_fm, 3), (g_mw, 2)]),
    ])
    make_ol(LV, SUBJ, "dynamics", SORT, "Dynamics",
            "Apply the relationship between resultant force, mass and acceleration (F = ma) to new situations; identify the forces acting on an object and draw free-body "
            "diagrams; explain the effects of balanced and unbalanced forces and of friction; state that mass is a measure of the amount of matter and of inertia, that "
            "weight is a gravitational force and that gravitational field strength is the force per unit mass (W = mg, g = 10 N/kg) (summary of the Singapore-Cambridge "
            "O-Level Physics 6091 syllabus).",
            "Dynamics", "Dynamics",
            "Free Secondary 3 O-Level Physics worksheets on dynamics: balanced and unbalanced forces, free-body diagrams, F = ma, friction, mass, weight (W = mg) and inertia. "
            "100 questions with answers.",
            "Resultant force = mass × acceleration", "Weight = mg, with g = 10 N/kg.",
            "<p><b>An unbalanced (resultant) force makes an object accelerate.</b></p><ul>"
            "<li>Balanced forces: the object stays at rest or keeps moving at constant velocity.</li>"
            "<li>F = ma, where F is the resultant force in N, m in kg and a in m/s². Find the resultant first (forward forces − backward forces).</li>"
            "<li>Friction opposes motion. Weight W = mg (g = 10 N/kg) is a force in N; mass in kg is the same everywhere and measures inertia.</li></ul>",
            [("A 1200 kg car: driving force 3000 N, friction 600 N. Acceleration?", ["resultant = 3000 − 600 = 2400 N", "a = 2400 ÷ 1200"], "2 m/s²"),
             ("Weight of a 55 kg student?", ["W = 55 × 10"], "550 N")],
            ["Using the driving force in F = ma instead of the resultant force.", "Giving weight in kg. Weight is a force, in newtons.",
             "Thinking a moving object needs a resultant force to keep moving. At constant velocity the resultant force is zero.",
             "Thinking mass changes on the Moon. Only weight changes."],
            [("What is the difference between mass and weight?", "Mass is the amount of matter in a body (kg) and does not change; weight is the gravitational force on it (N), W = mg."),
             ("What happens when the forces on an object are balanced?", "The resultant force is zero, so the object stays at rest or moves at a constant velocity."),
             ("How do you use F = ma with friction?", "Subtract the friction (and other resistive forces) from the driving force to get the resultant force, then divide by the mass.")],
            sets)


if __name__ == "__main__":
    main()
