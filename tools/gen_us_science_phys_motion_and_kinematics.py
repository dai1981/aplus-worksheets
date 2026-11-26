# -*- coding: utf-8 -*-
"""
US High School Physics: Motion and Kinematics (HS-PS2-1)
  python tools/gen_us_science_phys_motion_and_kinematics.py
Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the
net force on a macroscopic object, its mass, and its acceleration (kinematics is the language used to describe motion).
Speed and velocity, acceleration, the equations v = u + at and d = ut + ½at², free fall (g = 9.8 m/s²), and
reading position-time and velocity-time data.
Wrong answers come from real mistakes: "speed and velocity are the same", "acceleration means speeding up only",
"a constant speed on a curve means no acceleration", "d = vt for an accelerating object".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90301)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_speed():
    who = P.next()[0]
    what = R.choice([("electric scooter", (4, 9)), ("toy car", (1, 4)), ("car", (10, 30)), ("train", (20, 60)), ("skateboard", (2, 6)), ("drone", (5, 20))])
    v = R.randint(*what[1])
    t = R.choice([5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60])
    d = v * t
    k = R.choice(["v", "d", "t"])
    if not once(("sp", what[0], v, t, k)):
        return None
    if k == "v":
        return item("%s's %s travels %s m in %d s at a steady speed. What is its speed?" % (who, what[0], num(d), t), "%d m/s" % v,
                    uniq("%d m/s" % v, ["%s m/s" % num(d * t), "%s m/s" % num(t / d, 2), "%d m/s" % (v + 2), "%d m/s" % (d - t)]), "v = d ÷ t = %s ÷ %d = %d m/s." % (num(d), t, v))
    if k == "d":
        return item("A %s moves at %d m/s for %d s. How far does the %s go?" % (what[0], v, t, what[0]), "%s m" % num(d), uniq("%s m" % num(d), ["%s m" % num(v + t), "%s m" % num(t / v, 2), "%s m" % num(d * 2), "%s m" % num(d / 2)]),
                    "d = vt = %d × %d = %s m." % (v, t, num(d)))
    return item("How long does a %s moving at %d m/s take to travel %s m?" % (what[0], v, num(d)), "%d s" % t, uniq("%d s" % t, ["%s s" % num(d * v), "%s s" % num(v / d, 2), "%d s" % (t + 5), "%d s" % (t * 2)]),
                "t = d ÷ v = %s ÷ %d = %d s." % (num(d), v, t))


@safe
def g_acc():
    who = P.next()[0]
    u = R.choice([0, 0, 2, 4, 5, 10])
    a = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
    t = R.choice([2, 3, 4, 5, 6, 8, 10])
    v = u + a * t
    k = R.choice(["a", "v", "neg"])
    if not once(("ac", u, a, t, k)):
        return None
    if k == "a":
        return item("%s's car goes from %d m/s to %s m/s in %d s. What is its acceleration?" % (who, u, num(v), t), "%s m/s²" % num(a),
                    uniq("%s m/s²" % num(a), ["%s m/s²" % num(v / t), "%s m/s²" % num(v - u), "%s m/s²" % num((v - u) * t), "%s m/s²" % num(a + 1)]),
                    "a = (v − u) ÷ t = (%s − %d) ÷ %d = %s m/s²." % (num(v), u, t, num(a)))
    if k == "v":
        return item("A cart starts at %d m/s and accelerates at %s m/s² for %d s. What is its final velocity?" % (u, num(a), t), "%s m/s" % num(v),
                    uniq("%s m/s" % num(v), ["%s m/s" % num(a * t), "%s m/s" % num(u + a), "%s m/s" % num(v + u), "%s m/s" % num(u + a * t * t)]), "v = u + at = %d + %s × %d = %s m/s." % (u, num(a), t, num(v)))
    if v == u:
        return None
    return item("A bike slows from %s m/s to %d m/s in %d s. What is its acceleration?" % (num(v), u, t), "−%s m/s²" % num(a),
                uniq("−%s m/s²" % num(a), ["%s m/s²" % num(a), "−%s m/s²" % num(v / t), "−%s m/s²" % num(v - u), "0 m/s²"]), "a = (%d − %s) ÷ %d = −%s m/s² (slowing down)." % (u, num(v), t, num(a)))


@safe
def g_dist():
    a = R.choice([1, 2, 3, 4, 5, 6, 0.5, 1.5])
    t = R.choice([2, 4, 5, 6, 8, 10])
    u = R.choice([0, 0, 0, 2, 4])
    d = u * t + a * t * t / 2
    if not once(("ds", a, t, u)):
        return None
    good = "%s m" % num(d)
    return item("A sled starts at %d m/s and accelerates at %s m/s² for %d s. How far does it travel? (d = ut + ½at²)" % (u, num(a), t), good,
                uniq(good, ["%s m" % num(u * t + a * t * t), "%s m" % num(u * t + a * t / 2), "%s m" % num((u + a * t) * t), "%s m" % num(d + 10)]),
                "d = %d × %d + ½ × %s × %d² = %s m." % (u, t, num(a), t, num(d)))


@safe
def g_fall():
    t = R.choice([1, 1.5, 2, 2.5, 3, 4, 5])
    k = R.choice(["v", "d"])
    if not once(("fl", t, k)):
        return None
    v = 9.8 * t
    d = 4.9 * t * t
    if k == "v":
        g = "%s m/s" % num(v, 1)
        return item("A stone is dropped from rest off a cliff. How fast is it falling after %s s? (g = 9.8 m/s², ignore air resistance)" % num(t), g,
                    uniq(g, ["%s m/s" % num(4.9 * t, 2), "%s m/s" % num(d, 2), "%s m/s" % num(9.8 * t * t, 2), "9.8 m/s"]), "v = gt = 9.8 × %s = %s m/s." % (num(t), num(v, 1)))
    g = "%s m" % num(d, 2)
    return item("A ball is dropped from rest. How far does it fall in %s s? (g = 9.8 m/s², ignore air resistance)" % num(t), g,
                uniq(g, ["%s m" % num(v, 1), "%s m" % num(9.8 * t * t, 2), "%s m" % num(4.9 * t, 2), "%s m" % num(d * 2, 2)]), "d = ½gt² = 4.9 × %s² = %s m." % (num(t), num(d, 2)))


@safe
def g_data():
    who = P.next()[0]
    kind = R.choice(["pos", "vel"])
    k = R.choice(["rate", "type", "read"])
    ts = [0, 1, 2, 3, 4]
    if kind == "pos":
        v = R.randint(2, 9)
        x0 = R.choice([0, 0, 5, 10])
        xs = [x0 + v * t for t in ts]
        if not once(("dp", v, x0, k)):
            return None
        tab = table(["Time (s)", "Position (m)"], [[str(t), str(x)] for t, x in zip(ts, xs)])
        if k == "rate":
            return item(tab + "What is the velocity of %s's toy car?" % who, "%d m/s" % v, uniq("%d m/s" % v, ["%d m/s" % xs[-1], "%d m/s" % (v + 1), "0 m/s", "%d m/s" % (xs[-1] // 2)]),
                        "Slope = Δx ÷ Δt = %d m/s." % v)
        if k == "type":
            return item(tab + "Describe the motion of %s's toy car." % who, "constant velocity", ["speeding up", "slowing down", "not moving"], "Equal distance in each second.")
        return item(tab + "Where is %s's toy car at 3 s?" % who, "%d m" % xs[3], uniq("%d m" % xs[3], ["%d m" % xs[2], "%d m" % xs[4], "%d m" % (3 * v + 1), "3 m"]), "Read the row for 3 s.")
    a = R.randint(1, 5)
    u = R.choice([0, 2, 4, 6])
    vs = [u + a * t for t in ts]
    if not once(("dv", a, u, k)):
        return None
    tab = table(["Time (s)", "Velocity (m/s)"], [[str(t), str(x)] for t, x in zip(ts, vs)])
    if k == "rate":
        return item(tab + "What is the acceleration of %s's cart?" % who, "%d m/s²" % a, uniq("%d m/s²" % a, ["%d m/s²" % vs[-1], "%d m/s²" % (a + 1), "0 m/s²", "%d m/s²" % (vs[-1] // 4 + 1)]),
                    "Slope of v–t = %d m/s each second." % a)
    if k == "type":
        return item(tab + "Describe the motion of %s's cart." % who, "speeding up at a constant rate", ["constant velocity", "slowing down", "not moving"], "Velocity rises by the same amount each second.")
    return item(tab + "What is the velocity of %s's cart at 2 s?" % who, "%d m/s" % vs[2], uniq("%d m/s" % vs[2], ["%d m/s" % vs[1], "%d m/s" % vs[3], "%d m/s" % (2 * a), "2 m/s"]), "Read the row for 2 s.")


B1 = bank([
    ("What is the difference between speed and velocity?", "Velocity includes direction; speed does not.", ["They are exactly the same.", "Speed includes direction.", "Velocity is always larger."], "Velocity is a vector."),
    ("What is acceleration?", "the rate at which velocity changes", ["the distance traveled", "a high speed", "the time taken"], "Speeding up, slowing down or turning."),
    ("A car goes around a curve at a steady 20 m/s. Is it accelerating?", "Yes, because its direction is changing.", ["No, its speed is constant.", "Only if it speeds up.", "Only if it stops."], "Changing direction is acceleration."),
    ("What does the slope of a position-time graph show?", "velocity", ["acceleration", "distance only", "force"], "Δx ÷ Δt."),
    ("What does the slope of a velocity-time graph show?", "acceleration", ["position", "mass", "speed only"], "Δv ÷ Δt."),
    ("What are the units of acceleration?", "m/s²", ["m/s", "m", "N"], "Meters per second each second."),
    ("Ignoring air, how does a heavy ball fall compared with a light ball?", "They fall with the same acceleration.", ["The heavy one falls much faster.", "The light one falls faster.", "Neither accelerates."], "g = 9.8 m/s² for all."),
    ("Which is a vector quantity?", "displacement", ["distance", "speed", "time"], "Has size and direction."),
])
B5 = bank([
    ("A runner goes 400 m around a track and ends where she started. What is her displacement?", "0 m", ["400 m", "200 m", "800 m"], "Same start and end point."),
    ("Why do crash investigators measure skid marks?", "To find how fast a car was going from its stopping distance and deceleration.", ["To find the car's mass.", "To measure the road color.", "To find the driver's age."], "Kinematics."),
    ("A ball thrown straight up reaches its highest point. What is its velocity there?", "0 m/s", ["9.8 m/s", "its starting speed", "it cannot be known"], "It stops for an instant; acceleration is still 9.8 m/s² down."),
    ("A student times a falling ball 5 times and gets 0.62, 0.60, 0.61, 0.63 and 0.60 s. Why repeat?", "to reduce the effect of random timing errors", ["to make the ball fall faster", "because one trial is too accurate", "to change gravity"], "Average the trials."),
    ("Two cars have the same speed but move in opposite directions. Do they have the same velocity?", "No, their directions are different.", ["Yes, speed is velocity.", "Yes, if they have the same mass.", "Only on a highway."], "Velocity is a vector."),
])


def body():
    think = ("<p><b>Kinematics describes how position and velocity change with time.</b></p>"
             "<ul><li>v = d ÷ t (steady speed). a = (v − u) ÷ t.</li>"
             "<li>With constant acceleration: v = u + at and d = ut + ½at². Free fall: a = g = 9.8 m/s².</li>"
             "<li>Slope of position-time = velocity; slope of velocity-time = acceleration.</li></ul>")
    ex = [("0 to 20 m/s in 4 s. Acceleration?", ["(20 − 0) ÷ 4"], "5 m/s²"),
          ("Dropped for 2 s. Distance?", ["4.9 × 2²"], "19.6 m")]
    mist = ["Treating speed and velocity as the same.", "Thinking a steady speed on a curve means no acceleration.", "Using d = vt when the object is accelerating."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Speed and velocity", B1 + [(g_speed, 12)]),
        ("Acceleration", [(g_acc, 14), (g_speed, 6)]),
        ("Motion equations", [(g_dist, 8), (g_fall, 8), (g_acc, 4)]),
        ("Motion data", [(g_data, 16), (g_dist, 4)]),
        ("Analyzing motion", B5 + [(g_data, 6), (g_fall, 4), (g_dist, 5)]),
    ])
    make("physics", "motion-and-kinematics", 1, "HS-PS2-1",
         "Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the net force on a macroscopic object, its mass, and its acceleration.",
         "Motion and Kinematics",
         "Kinematics Worksheets: Velocity, Acceleration and Free Fall (High School Physics)",
         "Kinematics",
         "Free high school physics worksheets on motion and kinematics (NGSS HS-PS2-1): speed and velocity, acceleration, motion equations, free fall and motion graphs. 100 questions with answers.",
         "Acceleration is change in velocity.",
         "Use v = u + at and d = ut + ½at² for constant acceleration.",
         body(),
         [("What is the difference between speed and velocity?", "Speed tells how fast; velocity tells how fast and in which direction."),
          ("How do you calculate acceleration?", "Subtract the starting velocity from the final velocity and divide by the time: a = (v − u) ÷ t."),
          ("What is the acceleration due to gravity?", "Near Earth's surface, falling objects accelerate at about 9.8 m/s² when air resistance is small.")],
         sets)


if __name__ == "__main__":
    main()
