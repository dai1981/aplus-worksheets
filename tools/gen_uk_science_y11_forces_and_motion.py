# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Physics): Forces and Motion
  python tools/gen_uk_science_y11_forces_and_motion.py
Scalar and vector quantities, contact and non-contact forces, weight (W = mg), resultant forces, Newton's laws and
F = ma, forces and elasticity (F = ke), speed, velocity, acceleration, v² − u² = 2as, distance–time and velocity–time
graphs, stopping distances, and (higher tier) momentum and its conservation. g = 9.8 N/kg. Reuses the US Physics
motion, Newton's laws and momentum questions in British English.
Wrong answers come from real mistakes: "mass and weight are the same", "a moving object needs a resultant force to
keep moving", "tiredness increases braking distance", "speed is a vector".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62110)
MK, NL, MC = "phys_motion_and_kinematics", "phys_newtons_laws_and_net_force", "phys_momentum_and_collisions"
us_speed, us_acc, us_data = us(MK, "g_speed"), us(MK, "g_acc"), us(MK, "g_data")
us_fma, us_net, us_law, us_weight = us(NL, "g_fma"), us(NL, "g_net"), us(NL, "g_law"), us(NL, "g_weight", rep=(("m/s²)", "N/kg)"),))
us_p, us_stick = us(MC, "g_p", rep=(("How fast is it moving?", "What is its speed?"), ("football ball", "football")))), us(MC, "g_stick")

VEC = [("speed", "scalar"), ("velocity", "vector"), ("distance", "scalar"), ("displacement", "vector"), ("mass", "scalar"), ("weight", "vector"),
       ("force", "vector"), ("acceleration", "vector"), ("momentum", "vector"), ("energy", "scalar"), ("time", "scalar"), ("temperature", "scalar")]


def g_vec():
    x, a = R.choice(VEC)
    if not once(("vc", x)):
        return None
    return item("Is %s a scalar or a vector quantity?" % x, "a " + a, ["a " + ("vector" if a == "scalar" else "scalar"), "both", "neither"],
                "Vectors have magnitude and direction; scalars have magnitude only.")


CON = [("friction", "contact"), ("air resistance", "contact"), ("tension", "contact"), ("normal contact force", "contact"), ("upthrust", "contact"),
       ("gravity (weight)", "non-contact"), ("magnetic force", "non-contact"), ("electrostatic force", "non-contact")]


def g_contact():
    x, a = R.choice(CON)
    if not once(("ct", x)):
        return None
    return item("Is %s a contact or a non-contact force?" % x, "a " + a + " force", ["a " + ("non-contact" if a == "contact" else "contact") + " force", "not a force", "both"],
                "Non-contact forces act at a distance: gravity, magnetic and electrostatic.")


def g_suvat():
    u = R.choice([0, 0, 2, 4, 5, 6, 10])
    a = R.choice([1, 2, 2.5, 3, 4, 5])
    s = R.choice([4, 5, 8, 10, 12, 16, 20, 25, 40])
    v2 = u * u + 2 * a * s
    v = v2 ** 0.5
    if abs(v - round(v)) > 1e-9 or not once(("sv", u, a, s)):
        return None
    v = int(round(v))
    who = R.choice(["A cyclist", "A car", "A trolley", "A skier", "A train"])
    return item("%s starts at %d m/s and accelerates at %g m/s² over %d m. What is the final velocity? (v² − u² = 2as)" % (who, u, a, s), "%d m/s" % v,
                [x for x in ["%d m/s" % v2, "%g m/s" % (u + a * s), "%d m/s" % (v + 2), "%g m/s" % (2 * a * s)] if x != "%d m/s" % v][:3],
                "v² = %d² + 2 × %g × %d = %d, so v = %d m/s." % (u, a, s, v2, v))


THINK = ["tiredness", "drinking alcohol", "taking drugs", "using a mobile phone while driving"]
BRAKE = ["a wet road", "an icy road", "worn tyres", "worn brakes"]


def g_stop():
    k = R.choice(["fac", "fac", "think", "stop"])
    if k == "fac":
        f = R.choice(THINK + BRAKE)
        if not once(("sf", f)):
            return None
        a = "thinking distance" if f in THINK else "braking distance"
        return item("Which distance is mainly increased by %s?" % f, a, ["thinking distance" if a == "braking distance" else "braking distance", "neither", "the car's mass"],
                    "Thinking distance depends on the driver's reaction time; braking distance on the car and the road.")
    v = R.choice([10, 12, 13, 15, 20, 25, 30])
    t = R.choice([0.5, 0.6, 0.7, 0.8, 1.0, 1.2])
    d = round(v * t, 1)
    if k == "think":
        if not once(("st", v, t)):
            return None
        return item("A car travels at %d m/s. The driver's reaction time is %g s. What is the thinking distance?" % (v, t), "%g m" % d,
                    [x for x in ["%g m" % round(v / t, 1), "%g m" % (v + t), "%g m" % (d * 2), "%d m" % v] if x != "%g m" % d][:3], "distance = speed × time = %d × %g." % (v, t))
    b = R.choice([6, 8, 10, 14, 18, 24, 32, 38, 48, 55])
    if not once(("ss", v, t, b)):
        return None
    return item("A car at %d m/s has a thinking distance of %g m and a braking distance of %d m. What is the stopping distance?" % (v, d, b), "%g m" % round(d + b, 1),
                [x for x in ["%d m" % b, "%g m" % d, "%g m" % round(abs(b - d), 1), "%g m" % round((d + b) * 2, 1)] if x != "%g m" % round(d + b, 1)][:3],
                "Stopping distance = thinking distance + braking distance.")


def g_hooke():
    k = R.choice([10, 20, 25, 40, 50, 80, 100, 200])
    e = R.choice([0.02, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
    F = round(k * e, 2)
    q = R.choice(["F", "k", "e"])
    if not once(("hk", k, e, q)):
        return None
    if q == "F":
        return item("A spring has a spring constant of %d N/m. It is stretched by %g m. What force is applied? (F = ke)" % (k, e), "%g N" % F,
                    [x for x in ["%g N" % round(k / e, 1), "%g N" % (k + e), "{:,} N".format(round(F * 100, 1)).replace(".0 N", " N"), "%g N" % round(F / 2, 2)] if x != "%g N" % F][:3], "F = %d × %g." % (k, e))
    if q == "k":
        return item("A force of %g N stretches a spring by %g m. What is the spring constant? (F = ke)" % (F, e), "%d N/m" % k,
                    [x for x in ["%g N/m" % round(F * e, 3), "%g N/m" % round(e / F, 3), "%d N/m" % (k * 2), "%g N/m" % F] if x != "%d N/m" % k][:3], "k = F ÷ e = %g ÷ %g." % (F, e))
    return item("A spring has a spring constant of %d N/m. A force of %g N stretches it. What is the extension? (F = ke)" % (k, F), "%g m" % e,
                [x for x in ["%g m" % round(F * k, 1), "%g m" % round(k / F, 2), "%g m" % round(e * 10, 2), "%g m" % round(e / 2, 3)] if x != "%g m" % e][:3], "e = F ÷ k = %g ÷ %d." % (F, k))


B1 = bank([
    ("What is the difference between mass and weight?", "Mass is the amount of matter (kg); weight is the force of gravity on it (N).", ["They are the same.", "Weight is measured in kg.", "Mass changes on the Moon."], "W = mg."),
    ("What is a resultant force?", "the single force that has the same effect as all the forces acting together", ["the largest force", "the force of gravity only", "the force at the end of a journey"], "Add forces in the same direction, subtract opposite ones."),
    ("What is the gravitational field strength on Earth?", "about 9.8 N/kg", ["about 1.6 N/kg", "about 98 N/kg", "about 0.98 N/kg"], "On the Moon it is about 1.6 N/kg."),
])
B4 = bank([
    ("What is stopping distance?", "thinking distance + braking distance", ["thinking distance − braking distance", "braking distance only", "the distance before seeing a hazard"], "Both increase with speed."),
    ("Why is braking dangerous at high speed?", "A large deceleration means large forces, and the brakes may overheat.", ["The car gets lighter.", "Friction disappears.", "Thinking distance becomes zero."], "Work done by brakes heats them."),
    ("How do brakes slow a car down?", "Friction between the brakes and wheels does work, transferring kinetic energy to thermal energy.", ["They make the car heavier.", "They increase the car's speed.", "They remove the car's mass."], "The brakes get hot."),
    ("How can a typical reaction time be measured in class?", "by catching a dropped ruler", ["by weighing a person", "by measuring height", "by timing a run of 100 m only"], "Typical reaction times are 0.2–0.9 s."),
])
B5 = bank([
    ("What is the law of conservation of momentum?", "In a closed system, total momentum before an event equals total momentum after.", ["Momentum always increases.", "Momentum is lost in every collision.", "Only mass is conserved."], "Higher tier."),
    ("What is the unit of momentum?", "kg·m/s", ["N", "m/s²", "J"], "p = mv."),
])

if __name__ == "__main__":
  build(U, 11, "forces-and-motion", 10, "Physics", "Forces",
      "Scalar and vector quantities; contact and non-contact forces; gravity and weight; resultant forces; work done; forces and elasticity; speed, velocity and acceleration; distance–time and velocity–time graphs; Newton's laws; stopping distances; (higher tier) momentum and conservation of momentum.",
      "Forces and Motion", "Forces and Motion",
      "Free Year 11 GCSE Combined Science worksheets on forces and motion: vectors and scalars, weight, resultant forces, Newton's laws, F = ma, F = ke, acceleration, stopping distances and momentum. 100 questions with answers.",
      "Resultant force = mass × acceleration (F = ma).",
      "Stopping distance = thinking distance + braking distance.",
      "<p><b>Forces change how objects move.</b></p><ul><li>W = mg (g = 9.8 N/kg). F = ma. F = ke. p = mv.</li>"
      "<li>Acceleration = change in velocity ÷ time. v² − u² = 2as.</li>"
      "<li>Stopping distance = thinking distance (reaction time) + braking distance (road, tyres, brakes).</li></ul>",
      [("Resultant 20 N on 4 kg. Acceleration?", ["a = F ÷ m = 20 ÷ 4"], "5 m/s²"), ("20 m/s, reaction time 0.7 s. Thinking distance?", ["20 × 0.7"], "14 m")],
      ["Mixing up mass (kg) and weight (N).", "Thinking a moving object needs a resultant force to keep moving.", "Thinking tiredness increases braking distance."],
      [("What is Newton's second law?", "The acceleration of an object is proportional to the resultant force and inversely proportional to its mass: F = ma."),
       ("What affects stopping distance?", "Thinking distance depends on speed and reaction time (tiredness, alcohol, drugs, distractions). Braking distance depends on speed, the road, the tyres and the brakes."),
       ("What is momentum?", "Momentum = mass × velocity (p = mv). In a closed system, momentum before a collision equals momentum after.")],
      [("Forces", B1 + [(g_vec, 6), (g_contact, 5), (us_weight, 6)]),
       ("Newton's laws", [(us_net, 8), (us_law, 5), (us_fma, 7)]),
       ("Speed and acceleration", [(us_speed, 6), (us_acc, 6), (g_suvat, 4), (us_data, 4)]),
       ("Stopping distances", B4 + [(g_stop, 12), (g_hooke, 4)]),
       ("Elasticity and momentum", B5 + [(g_hooke, 6), (us_p, 6), (us_stick, 6)])])
