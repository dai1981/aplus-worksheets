# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Speed and Motion
  python tools/gen_uk_science_y9_speed_and_motion.py
Speed and the quantitative relationship between average speed, distance and time (speed = distance ÷ time), units
(m/s and km/h), the representation of a journey on a distance-time graph, relative motion, and forces as the cause of
changes in motion (balanced and unbalanced forces, resultant force). Reuses the resultant-force and motion questions
of the US Grade 8 unit in British English.
Wrong answers come from real mistakes: "speed = time ÷ distance", "a flat line on a distance-time graph means
constant speed", "a moving object must have an unbalanced force", "units do not matter".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61907)
R = U.R
P = People(R)
uk_sci.USED.clear()
FM = adopt_us("gen_us_science_g8_forces_and_motion", U)
us_net, us_motion = ukm(FM.g_net), ukm(FM.g_motion)


def f(x):
    x = round(x, 1)
    return "{:,}".format(int(x)) if x == int(x) else "{:,}".format(x)


def tt(n, tn):
    return "%s %s" % (f(n), tn[:-1] if n == 1 else tn)


TRIP = [("cycles", "m", "s", [3, 4, 5, 6, 8]), ("runs", "m", "s", [2, 3, 4, 5, 6]), ("drives", "km", "h", [30, 40, 50, 60, 70, 80, 90]),
        ("walks", "m", "s", [1, 2]), ("travels by train", "km", "h", [80, 100, 120, 150, 200])]


def g_speed():
    who = P.next()[0]
    verb, du, tu, speeds = R.choice(TRIP)
    v = R.choice(speeds)
    t = R.choice(([20, 30, 60, 100] if verb == "walks" else [2, 3, 4, 5, 10, 20, 30, 60, 100]) if tu == "s" else [2, 3, 4, 5])
    d = v * t
    su = "%s/%s" % (du, tu)
    k = R.choice(["v", "d", "t"])
    if not once(("sp", verb, v, t, k)):
        return None
    tn = "seconds" if tu == "s" else "hours"
    if k == "v":
        g = "%s %s" % (f(v), su)
        return item("%s %s %s %s in %d %s. What is the average speed?" % (who, verb, f(d), du, t, tn), g,
                    uniq(g, ["%s %s" % (f(d * t), su), "%s %s" % (f(d - t), su), "%s %s" % (f(d + t), su), "%s %s" % (f(d), su)]), "speed = distance ÷ time = %s ÷ %d = %s %s." % (f(d), t, f(v), su))
    if k == "d":
        g = "%s %s" % (f(d), du)
        return item("%s %s at an average speed of %s %s for %d %s. How far does %s travel?" % (who, verb, f(v), su, t, tn, who), g,
                    uniq(g, ["%s %s" % (f(v + t), du), "%s %s" % (f(round(v / t, 1)), du), "%s %s" % (f(v), du), "%s %s" % (f(d * 10), du)]), "distance = speed × time = %s × %d." % (f(v), t))
    g = tt(t, tn)
    return item("%s %s %s %s at an average speed of %s %s. How long does the journey take?" % (who, verb, f(d), du, f(v), su), g,
                uniq(g, [tt(d * v, tn), tt(d - v, tn), tt(v, tn), tt(t * 2, tn)]), "time = distance ÷ speed = %s ÷ %s." % (f(d), f(v)))


def g_conv():
    v = R.choice([18, 36, 54, 72, 90, 108])
    k = R.random() < 0.5
    if not once(("cv", v, k)):
        return None
    m = v * 1000 // 3600
    if k:
        g = "%d m/s" % m
        return item("A car travels at %d km/h. What is this in m/s? (1 km/h = 1,000 m ÷ 3,600 s)" % v, g, uniq(g, ["{:,} m/s".format(v * 1000), "%d m/s" % (v * 36 // 10), "%d m/s" % v, "%d m/s" % (m * 2)]),
                    "%d × 1,000 ÷ 3,600 = %d m/s." % (v, m))
    g = "%d km/h" % v
    return item("A bird flies at %d m/s. What is this in km/h? (multiply by 3.6)" % m, g, uniq(g, ["%d km/h" % m, "%d km/h" % (m * 36), "%d km/h" % (m * 1000), "%d km/h" % (v // 2)]), "%d × 3.6 = %d km/h." % (m, v))


def g_dt():
    who = P.next()[0]
    a = R.choice([100, 150, 200, 300])
    b = R.choice([0, 0, 50, 100])
    c = R.choice([200, 250, 300])
    pts = [(0, 0), (10, a), (20, a + b), (30, a + b + c)]
    k = R.choice(["still", "fast", "speed1", "total", "flat"])
    if b == 0 and k not in ("still", "flat", "total"):
        k = "still"
    if b != 0 and k in ("still", "flat"):
        k = "fast"
    if not once(("dt", a, b, c, k)) or not once(("dt", k), 6):
        return None
    tab = table(["Time (s)", "Distance from start (m)"], [[str(t), "{:,}".format(d)] for t, d in pts])
    intro = tab + "The table gives points from %s's distance-time graph. " % who
    if k == "still":
        return item(intro + "What was %s doing between 10 s and 20 s?" % who, "standing still", ["moving at a steady speed", "speeding up", "going backwards"], "The distance did not change: a flat line on the graph.")
    if k == "flat":
        return item(intro + "What would the graph look like between 10 s and 20 s?", "a flat (horizontal) line", ["a steep straight line", "a curve upwards", "a vertical line"], "No change in distance.")
    if k == "total":
        g = "{:,} m".format(a + b + c)
        return item(intro + "How far did %s travel altogether?" % who, g, uniq(g, ["{:,} m".format(c), "{:,} m".format(a), "{:,} m".format(a + c + 100), "30 m"]), "Read the last distance.")
    segs = [("0–10 s", a), ("10–20 s", b), ("20–30 s", c)]
    if k == "fast":
        best = max(segs, key=lambda x: x[1])[0]
        return item(intro + "In which 10-second section was %s moving fastest?" % who, best, [s[0] for s in segs if s[0] != best] + ["all the same"], "The biggest distance in the same time: the steepest line.")
    g = "%d m/s" % (a // 10)
    return item(intro + "What was the average speed in the first 10 seconds?", g, uniq(g, ["%d m/s" % a, "%d m/s" % (a * 10), "%d m/s" % (a // 20), "10 m/s" if a != 100 else "20 m/s"]), "%d ÷ 10." % a)


B1 = bank([
    ("What is the equation for average speed?", "speed = distance ÷ time", ["speed = time ÷ distance", "speed = distance × time", "speed = distance + time"], "Units: m/s or km/h."),
    ("What does a steeper line on a distance-time graph show?", "a faster speed", ["a slower speed", "standing still", "going backwards only"], "The gradient is the speed."),
    ("What does a flat line on a distance-time graph show?", "the object is stationary (not moving)", ["a constant high speed", "speeding up", "slowing down"], "Distance is not changing."),
    ("Why do we usually talk about average speed?", "Speed changes during a journey, so we use total distance ÷ total time.", ["Speed never changes.", "It is the top speed.", "It is the starting speed."], "Journeys vary."),
])
B5 = bank([
    ("Two cars travel side by side at 50 km/h. How fast is one moving compared with the other?", "0 km/h", ["50 km/h", "100 km/h", "25 km/h"], "Relative motion."),
    ("Two trains pass in opposite directions at 60 km/h and 80 km/h. What is their speed relative to each other?", "140 km/h", ["20 km/h", "60 km/h", "80 km/h"], "Add for opposite directions."),
    ("A car moves at a steady speed in a straight line. What can you say about the forces on it?", "They are balanced.", ["The driving force is bigger.", "There are no forces.", "Friction is bigger."], "Balanced forces: no change in motion."),
    ("What happens when the forces on a moving object become unbalanced?", "It speeds up, slows down or changes direction.", ["Nothing changes.", "It always stops.", "It must explode."], "Resultant force."),
    ("Why do speed cameras measure the time to travel between two lines?", "Speed = distance ÷ time, and the distance between the lines is known.", ["To measure the car's mass.", "To find the colour.", "To count the passengers."], "Average speed checks."),
])


def body():
    think = ("<p><b>Speed tells you how far something goes in each second (or hour).</b></p>"
             "<ul><li>speed = distance ÷ time; distance = speed × time; time = distance ÷ speed.</li>"
             "<li>On a distance-time graph, a steeper line means faster; a flat line means stopped.</li>"
             "<li>Balanced forces keep the motion the same; an unbalanced (resultant) force changes speed or direction.</li></ul>")
    ex = [("300 m in 60 s?", ["300 ÷ 60"], "5 m/s"),
          ("72 km/h in m/s?", ["72 × 1,000 ÷ 3,600"], "20 m/s")]
    mist = ["Writing speed = time ÷ distance.", "Thinking a flat line means a steady speed.", "Thinking a moving object needs an unbalanced force."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Calculating speed", B1[:1] + [(g_speed, 19)]),
        ("Units of speed", [(g_conv, 8), (g_speed, 12)]),
        ("Distance-time graphs", B1[1:] + [(g_dt, 17)]),
        ("Forces and motion", [(us_net, 12), (us_motion, 5), (g_dt, 3)]),
        ("Relative motion", B5 + [(g_speed, 6), (us_net, 6), (g_conv, 3)]),
    ])
    make_ks3(9, "speed-and-motion", 7, "Physics", "Motion and forces",
             "Speed and the quantitative relationship between average speed, distance and time (speed = distance ÷ time); the representation of a journey on a distance-time graph; relative motion: trains and cars passing one another; forces being needed to cause objects to stop or start moving, or to change their speed or direction of motion (qualitative only); change depending on direction of force and its size.",
             "Speed and Motion",
             "Year 9 Science: Speed and Motion Worksheets (Speed = Distance ÷ Time, Graphs)",
             "Speed and Motion",
             "Free Year 9 science worksheets on speed and motion: speed, distance and time calculations, m/s and km/h, distance-time graphs, relative motion and balanced and unbalanced forces. 100 questions with answers.",
             "speed = distance ÷ time",
             "On a distance-time graph, steeper means faster and flat means stopped.",
             body(),
             [("How do you calculate speed?", "Divide the distance travelled by the time taken: speed = distance ÷ time. Use m/s for metres and seconds, km/h for kilometres and hours."),
              ("How do you read a distance-time graph?", "A straight sloping line means a steady speed; steeper is faster. A flat line means the object has stopped."),
              ("What is relative motion?", "Speed compared with another moving object. Two cars at the same speed side by side are not moving relative to each other.")],
             sets)


if __name__ == "__main__":
    main()
