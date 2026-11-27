# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 2: Kinematics
  python tools/gen_sg_science_s3_kinematics.py
Distance and displacement, speed and velocity, average speed, acceleration = change in velocity ÷ time, distance-time and
speed-time graphs (gradient = speed or acceleration, area = distance), free fall with g = 10 m/s² and terminal velocity.
UK and US speed and acceleration makers are reused (Singapore names); graph questions draw their own SVG graphs.
Wrong answers come from real mistakes: "average speed = average of the two speeds", "a flat distance-time line means constant
speed", "a negative acceleration means moving backwards", "a heavy ball falls faster without air resistance".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, graph, fig, ex

LV, SUBJ, SORT = 3, "Physics", 2
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

us_speed = src("gen_us_science_phys_motion_and_kinematics", "g_speed")
uk_speed = src("gen_uk_science_y9_speed_and_motion", "g_speed")
uk_conv = src("gen_uk_science_y9_speed_and_motion", "g_conv")


def g_avg():
    who = P.next()[0]
    verb, lo, hi = R.choice([("cycles", 10, 20), ("runs", 8, 12), ("drives", 40, 80), ("walks", 4, 6)])
    t1 = R.choice([0.5, 1, 1.5, 2])
    t2 = R.choice([0.5, 1, 2, 3])
    v1 = R.randint(lo, hi)
    v2 = R.choice([x for x in range(lo, hi + 1) if x != v1])
    if t1 == t2:
        return None
    d1, d2 = v1 * t1, v2 * t2
    v = (d1 + d2) / (t1 + t2)
    return nq("%s %s %s km in %s h and then %s km in %s h. What is the average speed for the whole journey?" % (who, verb, N(d1), N(t1), N(d2), N(t2)),
              v, [(v1 + v2) / 2, (d1 + d2) / max(t1, t2), v1 + v2], " km/h",
              "Average speed = total distance ÷ total time = %s ÷ %s = %s km/h." % (N(d1 + d2), N(t1 + t2), N(v)))


def g_acc():
    k = R.choice(["a", "a", "v", "t", "dec"])
    what = R.choice(["A car", "A bus", "A cyclist", "A lift", "An MRT train", "A sprinter"])
    u = R.choice([0, 0, 2, 4, 5, 8, 10])
    a = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    t = R.choice([2, 3, 4, 5, 6, 8, 10])
    v = u + a * t
    if v > {"A sprinter": 11, "A cyclist": 12, "A lift": 6, "An MRT train": 25, "A bus": 20, "A car": 30}[what] or (what == "A lift" and a > 1.5) or (what == "A sprinter" and a > 4):
        return None
    if k == "a":
        return nq("%s speeds up from %s m/s to %s m/s in %d s. What is its acceleration?" % (what, N(u), N(v), t), a, [v / t, (v - u) * t, (v + u) / t], " m/s²",
                  "a = (v − u) ÷ t = (%s − %s) ÷ %d = %s m/s²." % (N(v), N(u), t, N(a)))
    if k == "v":
        return nq("%s starts at %s m/s and accelerates at %s m/s² for %d s. What is its final speed?" % (what, N(u), N(a), t), v, [a * t, u + a, (u + a) * t], " m/s",
                  "v = u + at = %s + %s × %d = %s m/s." % (N(u), N(a), t, N(v)))
    if k == "t":
        return nq("%s accelerates at %s m/s² from %s m/s to %s m/s. How long does this take?" % (what, N(a), N(u), N(v)), t, [v / a, (v - u) * a, (v + u) / a], " s",
                  "t = (v − u) ÷ a = (%s − %s) ÷ %s = %d s." % (N(v), N(u), N(a), t))
    if v == 0:
        return None
    return nq("%s slows down from %s m/s to rest in %d s. What is its acceleration?" % (what, N(v), t), -v / t, [v / t, -v * t, -t / v], " m/s²",
              "a = (0 − %s) ÷ %d = −%s m/s². The minus sign means it is slowing down (deceleration)." % (N(v), t, N(v / t)))


def _vt():
    v1 = R.choice([4, 6, 8, 10, 12, 15, 20])
    t1 = R.choice([2, 4, 5])
    t2 = R.choice([4, 5, 6, 8])
    t3 = R.choice([2, 4, 5])
    T = t1 + t2 + t3
    if v1 / t1 > 5 or v1 / t3 > 8:
        raise ValueError
    pts = [(0, 0), (t1, v1), (t1 + t2, v1), (T, 0)]
    xs = 2 if T <= 20 else 4
    ys = 2 if v1 <= 12 else 5
    ymax = ((v1 + ys) // ys) * ys
    svg = graph(pts, ((T + xs - 1) // xs) * xs, ymax, xs, ys, "time / s", "speed / (m/s)", label="speed-time graph",
                marks=[(t1 / 2, "A"), (t1 + t2 / 2, "B"), (t1 + t2 + t3 / 2, "C")])
    return v1, t1, t2, t3, svg


def g_vt():
    v1, t1, t2, t3, svg = _vt()
    k = R.choice(["accA", "decC", "distA", "distB", "total", "avg", "descB"])
    q = fig(svg) + "The speed-time graph shows the motion of a car. "
    if k == "accA":
        return nq(q + "What is the acceleration in section A?", v1 / t1, [v1 * t1, t1 / v1, v1 / (t1 + t2)], " m/s²", "Gradient = %d ÷ %d = %s m/s²." % (v1, t1, N(v1 / t1)))
    if k == "decC":
        return nq(q + "What is the deceleration in section C?", v1 / t3, [v1 * t3, t3 / v1, v1 / (t1 + t2 + t3)], " m/s²", "Gradient = %d ÷ %d = %s m/s² (slowing down)." % (v1, t3, N(v1 / t3)))
    if k == "distA":
        return nq(q + "How far does the car travel in section A?", v1 * t1 / 2, [v1 * t1, v1 / t1, v1 + t1], " m", "Area of triangle = ½ × %d × %d = %s m." % (t1, v1, N(v1 * t1 / 2)))
    if k == "distB":
        return nq(q + "How far does the car travel in section B?", v1 * t2, [v1 * t2 / 2, v1 * (t1 + t2), v1 + t2], " m", "Area of rectangle = %d × %d = %d m." % (t2, v1, v1 * t2))
    tot = v1 * (t1 / 2 + t2 + t3 / 2)
    if k == "total":
        return nq(q + "What is the total distance travelled?", tot, [v1 * (t1 + t2 + t3), v1 * t2, v1 * (t1 + t2 + t3) / 2], " m",
                  "Total area = ½ × %d × %d + %d × %d + ½ × %d × %d = %s m." % (t1, v1, t2, v1, t3, v1, N(tot)))
    if k == "avg":
        T = t1 + t2 + t3
        return nq(q + "What is the average speed for the whole journey?", tot / T, [v1 / 2, v1, tot / t2], " m/s", "Average speed = %s m ÷ %d s = %s m/s." % (N(tot), T, N(tot / T)))
    return tq(q + "Describe the motion in section B.", "It moves at a constant speed of %d m/s." % v1,
              ["It is at rest.", "It accelerates uniformly at %d m/s²." % v1, "It slows down uniformly."], "A horizontal line on a speed-time graph means constant speed (zero acceleration).")


def g_st():
    v = R.choice([2, 3, 4, 5, 6, 8, 10])
    t1 = R.choice([4, 5, 6])
    t2 = R.choice([2, 3, 4])
    d1 = v * t1
    v3 = R.choice([x for x in (2, 4, 5, 6, 10) if x != v])
    t3 = R.choice([2, 4])
    d3 = d1 + v3 * t3
    T = t1 + t2 + t3
    pts = [(0, 0), (t1, d1), (t1 + t2, d1), (T, d3)]
    ys = 10 if d3 <= 60 else 20
    svg = graph(pts, ((T + 1) // 2) * 2, ((d3 + ys) // ys) * ys, 2, ys, "time / s", "distance / m", label="distance-time graph",
                marks=[(t1 / 2, "P"), (t1 + t2 / 2, "Q"), (t1 + t2 + t3 / 2, "R")])
    q = fig(svg) + "The distance-time graph shows a cyclist's journey. "
    k = R.choice(["P", "R", "Q", "avg"])
    if k == "P":
        return nq(q + "What is the speed in part P?", v, [d1, t1, d1 * t1], " m/s", "Speed = gradient = %d ÷ %d = %d m/s." % (d1, t1, v))
    if k == "R":
        return nq(q + "What is the speed in part R?", v3, [d3 / T, d3, v3 * t3 * 2], " m/s", "Speed = gradient = %d ÷ %d = %d m/s." % (v3 * t3, t3, v3))
    if k == "Q":
        return tq(q + "What is the cyclist doing in part Q?", "The cyclist is at rest (stationary).", ["The cyclist is moving at a constant speed.", "The cyclist is accelerating.", "The cyclist is moving backwards."],
                  "A horizontal line on a distance-time graph means the distance is not changing: the cyclist is at rest.")
    return nq(q + "What is the average speed for the whole journey?", d3 / T, [(v + v3) / 2, d3 / (T - t2), (v + 0 + v3) / 3], " m/s", "Average speed = %d m ÷ %d s = %s m/s." % (d3, T, N(d3 / T)))


def g_fall():
    k = R.choice(["v", "t", "d"])
    t = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    if k == "v":
        return nq("A stone is dropped from rest from a high bridge. Ignoring air resistance (g = 10 m/s²), what is its speed after %s s?" % N(t), 10 * t, [10 / t, 5 * t * t, 10 * t * t], " m/s",
                  "v = gt = 10 × %s = %s m/s." % (N(t), N(10 * t)))
    if k == "t":
        v = 10 * t
        return nq("A ball is dropped from rest. Ignoring air resistance (g = 10 m/s²), how long does it take to reach a speed of %s m/s?" % N(v), t, [v * 10, v / 5, v], " s",
                  "t = v ÷ g = %s ÷ 10 = %s s." % (N(v), N(t)))
    if k == "d":
        return nq("A coin falls from rest for %s s. Use the area under its speed-time graph (g = 10 m/s², no air resistance) to find how far it falls." % N(t), 5 * t * t,
                  [10 * t * t, 10 * t, 5 * t], " m", "Speed after %s s = %s m/s. Area = ½ × %s × %s = %s m." % (N(t), N(10 * t), N(t), N(10 * t), N(5 * t * t)))
    m = R.choice([1, 2, 5, 10])
    return tq("A %d kg ball and a 0.1 kg ball are dropped together in a vacuum. Which reaches the ground first?" % m, "They land at the same time.",
              ["the %d kg ball" % m, "the 0.1 kg ball", "It depends on their colour."], "Without air resistance, every object falls with the same acceleration g = 10 m/s².")


SHAPES = [("a horizontal line on a distance-time graph", "The object is at rest."), ("a straight sloping line on a distance-time graph", "The object moves at a constant speed."),
          ("a curve getting steeper on a distance-time graph", "The object is speeding up."), ("a horizontal line on a speed-time graph", "The object moves at a constant speed."),
          ("a straight line sloping upwards on a speed-time graph", "The object has a constant (uniform) acceleration."),
          ("a straight line sloping downwards on a speed-time graph", "The object has a constant deceleration."),
          ("a speed-time curve that gets less steep and becomes flat", "The acceleration decreases until the object reaches a constant speed.")]
g_shape = rows(R, SHAPES, "What does %s show?")

POOL1 = pool(R, [
    ("What is the difference between distance and displacement?", "Displacement is distance in a stated direction.", ["They are the same.", "Distance is always larger than zero; displacement is never zero.", "Displacement has no unit."], "Displacement is a vector."),
    ("What is the difference between speed and velocity?", "Velocity is speed in a stated direction.", ["Velocity is always larger.", "Speed is a vector.", "They have different units."], "Both are measured in m/s."),
    ("What is acceleration?", "the rate of change of velocity", ["the rate of change of distance", "the speed in a direction", "the distance per second squared"], "a = (v − u) ÷ t, in m/s²."),
    ("A car goes round a roundabout at a constant speed of 10 m/s. Is it accelerating?", "Yes, because its direction (and so its velocity) changes.", ["No, because its speed is constant.", "No, because it is not speeding up.", "Only if it slows down."], "A change in direction is a change in velocity."),
    ("A runner completes one lap of a 400 m track and stops at the start. What is her displacement?", "0 m", ["400 m", "200 m", "800 m"], "She ends where she started."),
    ("What does the gradient of a distance-time graph give?", "the speed", ["the acceleration", "the distance travelled", "the time taken"], "Gradient = distance ÷ time."),
    ("What does the gradient of a speed-time graph give?", "the acceleration", ["the speed", "the distance travelled", "the force"], "Gradient = change in speed ÷ time."),
    ("What does the area under a speed-time graph give?", "the distance travelled", ["the acceleration", "the speed", "the time taken"], "Area = speed × time = distance."),
    ("What is the unit of acceleration?", "m/s²", ["m/s", "m²/s", "s/m"], "Change in velocity (m/s) per second."),
    ("A train has an acceleration of 2 m/s². What does this mean?", "Its speed increases by 2 m/s every second.", ["It travels 2 m every second.", "It moves at 2 m/s.", "It takes 2 s to start."], "Acceleration is speed gained per second."),
])
POOL5 = pool(R, [
    ("A skydiver jumps from a plane. Why does she reach a terminal velocity?", "Air resistance increases with speed until it equals her weight, so the resultant force is zero.",
     ["Her weight decreases as she falls.", "Gravity stops acting at high speed.", "Air resistance is always equal to her weight."], "With no resultant force, the acceleration is zero."),
    ("A skydiver opens her parachute while falling at terminal velocity. What happens next?", "Air resistance becomes larger than her weight, so she slows down to a lower terminal velocity.",
     ["She speeds up.", "She stops in the air.", "Her weight increases."], "A larger area gives more air resistance."),
    ("At the moment a skydiver leaves the plane, what is her acceleration (ignore air resistance at the start)?", "10 m/s² downwards", ["0 m/s²", "her terminal velocity", "1 m/s² downwards"], "At first only weight acts."),
    ("How does the acceleration of a falling object change as air resistance grows?", "It decreases until it becomes zero.", ["It increases.", "It stays at 10 m/s².", "It becomes negative straight away."], "The resultant force falls as air resistance grows."),
    ("A ball is thrown straight up. What is its velocity at the highest point?", "0 m/s", ["10 m/s", "its starting speed", "−10 m/s"], "It stops for an instant before falling back."),
    ("A ball is thrown straight up. What is its acceleration at the highest point (ignore air resistance)?", "10 m/s² downwards", ["0 m/s²", "10 m/s² upwards", "it has no acceleration"], "Gravity still acts at the top."),
    ("A 5 kg ball and a 0.1 kg ball are dropped together in a vacuum. Which reaches the ground first?", "They land at the same time.", ["the 5 kg ball", "the 0.1 kg ball", "Neither: they float."], "Without air resistance, every object falls with the same acceleration g = 10 m/s²."),
    ("A feather and a hammer are dropped together on the Moon. What happens?", "They hit the ground at the same time.", ["The hammer lands first.", "The feather lands first.", "They float."], "There is no air on the Moon."),
    ("A car's speed-time graph is a straight line from 0 to 20 m/s in 10 s. How far does it travel?", "100 m", ["200 m", "2 m", "20 m"], "Area = ½ × 10 × 20 = 100 m."),
    ("Two cars have the same speed-time graph shape, but car X's line is steeper. What does this show?", "Car X has a larger acceleration.", ["Car X travels less far.", "Car X is slower.", "Car X has a smaller acceleration."], "Gradient = acceleration."),
    ("A distance-time graph for a toy car is a curve that gets less steep. What is the car doing?", "slowing down", ["speeding up", "at rest", "moving at constant speed"], "The gradient (speed) is getting smaller."),
])


def main():
    sets = U.sets([
        ("Speed, velocity and acceleration", [POOL1, (us_speed, 4), (uk_speed, 3), (g_acc, 6), (uk_conv, 2)]),
        ("Calculating speed and acceleration", [(g_acc, 10), (g_avg, 6), (us_speed, 3), (uk_conv, 2)]),
        ("Distance-time graphs", [(g_st, 10), (g_shape, 4), (g_avg, 3), (uk_speed, 3), POOL1]),
        ("Speed-time graphs", [(g_vt, 14), (g_shape, 3), POOL1]),
        ("Free fall and exam-style questions", [POOL5, (g_fall, 8), (g_vt, 4), (g_acc, 2)]),
    ])
    make_ol(LV, SUBJ, "kinematics", SORT, "Kinematics",
            "State what is meant by speed, velocity and acceleration; calculate average speed and acceleration = change in velocity ÷ time taken; plot and interpret "
            "distance-time and speed-time graphs, using the gradient to find speed or acceleration and the area under a speed-time graph to find distance; state that the "
            "acceleration of free fall near the Earth is constant at about 10 m/s²; describe the motion of objects falling with and without air resistance, including "
            "terminal velocity (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Kinematics", "Kinematics",
            "Free Secondary 3 O-Level Physics worksheets on kinematics: speed, velocity, acceleration, distance-time and speed-time graphs, free fall and terminal velocity. "
            "100 questions with answers.",
            "a = (v − u) ÷ t", "Speed-time graph: gradient = acceleration, area = distance.",
            "<p><b>Acceleration is the rate of change of velocity.</b></p><ul>"
            "<li>Average speed = total distance ÷ total time. Velocity is speed in a stated direction.</li>"
            "<li>a = (v − u) ÷ t, in m/s². A negative value means slowing down (deceleration).</li>"
            "<li>Distance-time graph: gradient = speed; flat line = at rest. Speed-time graph: gradient = acceleration; area = distance.</li>"
            "<li>Without air resistance every object falls with g = 10 m/s². With air resistance a falling object reaches a terminal velocity.</li></ul>",
            [("A bus goes from 4 m/s to 16 m/s in 6 s. Acceleration?", ["a = (16 − 4) ÷ 6"], "2 m/s²"),
             ("A speed-time graph rises from 0 to 12 m/s in 4 s. Distance?", ["area of triangle = ½ × 4 × 12"], "24 m"),
             ("A stone is dropped. Speed after 3 s? (g = 10 m/s²)", ["v = 0 + 10 × 3"], "30 m/s")],
            ["Averaging the two speeds instead of dividing total distance by total time.",
             "Reading a horizontal line on a distance-time graph as constant speed. It means the object is at rest.",
             "Using the gradient of a speed-time graph for distance. Distance is the area under the graph.",
             "Thinking heavier objects fall faster. Without air resistance all objects fall with the same acceleration."],
            [("How do you find distance from a speed-time graph?", "Work out the area under the graph: triangles (½ × base × height) and rectangles (base × height), then add them."),
             ("What is terminal velocity?", "The constant speed a falling object reaches when air resistance has grown to equal its weight, so the resultant force is zero."),
             ("What value of g is used in O-Level Physics?", "The acceleration of free fall near the Earth is taken as 10 m/s² (the gravitational field strength is 10 N/kg).")],
            sets)


if __name__ == "__main__":
    main()
