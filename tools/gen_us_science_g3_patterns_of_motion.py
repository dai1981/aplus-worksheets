# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Patterns of Motion (3-PS2-2)
  python tools/gen_us_science_g3_patterns_of_motion.py
Observations and measurements of an object's motion show patterns that can predict future motion:
a pendulum or swing goes back and forth in a regular rhythm, a ball rolling in a bowl rocks back and forth,
a merry-go-round turns in circles, a toy car moving steadily covers the same distance every second.
Assessment boundary: no technical terms such as period or frequency.
Wrong answers come from real mistakes: "you cannot predict motion", "the pattern changes for no reason",
"a swing goes faster each time without a push".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, figure, svg_wrap, line, circle, text, People, INK, BLUE, RED, GRAY

U = Unit(30102)
R = U.R
P = People(R)


def pendulum(side, label="a pendulum swinging between two sides"):
    W, H = 260, 170
    s = [line(60, 15, 200, 15, INK, 4)]
    for sd, col in [("left", "#bbb"), ("middle", "#bbb"), ("right", "#bbb")]:
        x = {"left": 70, "middle": 130, "right": 190}[sd]
        y = {"left": 128, "middle": 145, "right": 128}[sd]
        c = BLUE if sd == side else col
        dash = "" if sd == side else " stroke-dasharray='4 4'"
        s.append(line(130, 15, x, y, c, 2, dash) + circle(x, y, 13, c if sd == side else "#fff", c, 2))
        s.append(text(x, y + 30 if sd == "middle" else y + 28, sd, 12, weight=400))
    return svg_wrap(W, H, "".join(s), label)


def g_swing():
    seq = ["left", "middle", "right", "middle"]
    start = R.randrange(4)
    n = R.choice([4, 5, 6])
    obs = [seq[(start + i) % 4] for i in range(n)]
    nxt = seq[(start + n) % 4]
    what = R.choice(["a pendulum", "a playground swing", "a clock pendulum", "a weight on a string"])
    p = P.next()
    rows = [["%d" % (i + 1), o] for i, o in enumerate(obs)]
    return item(table(["Look", "Position"], rows) + "%s watched %s and wrote down where it was every half swing. Where will it be at look %d?" % (p[0], what, n + 1), nxt,
                [x for x in ["left", "middle", "right"] if x != nxt] + ["It will stop in the air."],
                "The pattern repeats: left, middle, right, middle, left ... The next position is %s." % nxt)


def g_steady():
    step = R.choice([10, 15, 20, 25, 30, 40, 50])
    t0 = 0
    n = 4
    obj = R.choice(["toy car", "robot toy", "wind-up mouse", "turtle toy", "rolling ball"])
    rows = [["%d s" % i, "%d cm" % (t0 + step * i)] for i in range(n)]
    ask = R.choice([4, 5, 6])
    ans = t0 + step * ask
    p = P.next()
    return item(table(["Time", "Distance from start"], rows) + "%s measured a %s moving at a steady speed. How far from the start will it be at %d seconds?" % (p[0], obj, ask),
                "%d cm" % ans, ["%d cm" % (ans - step), "%d cm" % (ans + step), "%d cm" % (t0 + step * (n - 1))],
                "It moves %d cm every second. After %d seconds it is %d cm from the start." % (step, ask, ans))


def g_count():
    per = R.choice([5, 6, 8, 10, 12, 15])
    secs = R.choice([10, 20, 30])
    p = P.next()
    what = R.choice(["a pendulum", "a swing", "a metronome arm", "a rocking chair"])
    k = R.choice([2, 3])
    return item("%s counts that %s goes back and forth %d times in %d seconds. If the pattern stays the same, how many times will it go back and forth in %d seconds?" % (p[0], what, per, secs, secs * k),
                "%d times" % (per * k), ["%d times" % per, "%d times" % (per + secs), "%d times" % (per * k + per)],
                "%d seconds is %d × %d seconds, so %d × %d = %d." % (secs * k, k, secs, k, per, per * k))


def g_bounce():
    h0 = R.choice([80, 120, 160, 200, 240])
    f = R.choice([2])
    hs = [h0 // (f ** i) for i in range(3)]
    if hs[-1] * 2 != hs[-2]:
        return None
    nxt = hs[-1] // 2
    ball = R.choice(["rubber ball", "tennis ball", "bouncy ball", "basketball"])
    p = P.next()
    rows = [["drop", "%d cm" % hs[0]]] + [["bounce %d" % i, "%d cm" % hs[i]] for i in (1, 2)]
    return item(table(["", "Height"], rows) + "%s drops a %s and measures how high it goes. Each bounce is half as high as the one before. About how high will bounce 3 be?" % (p[0], ball),
                "%d cm" % nxt, ["%d cm" % hs[-1], "%d cm" % (hs[-1] + hs[-1] // 2), "%d cm" % hs[0]],
                "Half of %d cm is %d cm." % (hs[-1], nxt))


MOTION = [("A playground swing", "back and forth"), ("A merry-go-round", "around in a circle"), ("A ball rolling in a bowl", "back and forth"),
          ("A seesaw", "up and down"), ("A spinning top", "around in a circle"), ("A ceiling fan", "around in a circle"), ("A yo-yo", "up and down"),
          ("A Ferris wheel", "around in a circle"), ("A rocking horse", "back and forth"), ("A jumping kid on a trampoline", "up and down"),
          ("A clock's second hand", "around in a circle"), ("A bouncing ball", "up and down")]


def g_kind():
    obj, kind = R.choice(MOTION)
    return item("%s moves in a pattern. Which pattern?" % obj, kind, [k for k in ["back and forth", "around in a circle", "up and down", "in a straight line only"] if k != kind],
                "%s moves %s, and the pattern repeats." % (obj, kind))


B1 = bank([
    ("What is a pattern of motion?", "a way of moving that repeats, so you can predict what comes next", ["a motion that never happens again", "a picture of a moving thing", "a force that stops things"],
     "Swings, pendulums and merry-go-rounds move in patterns."),
    ("Why do scientists measure motion?", "to find patterns and predict future motion", ["to make objects heavier", "to stop all motion", "to change the color of objects"],
     "Measurements show patterns."),
    ("A pendulum swings left, right, left, right. What will it do next?", "swing left", ["stop in the middle of the air", "swing up in a circle", "swing right twice"],
     "It keeps repeating the pattern."),
    ("Why does a swing slowly stop if no one pushes it?", "Friction and air slow it down a little each swing.", ["Gravity turns off.", "Swings get tired.", "The chains get longer."],
     "Without a push, the swings get smaller and smaller."),
    ("A toy car moves 20 cm every second. How far does it go in 3 seconds?", "60 cm", ["20 cm", "23 cm", "40 cm"], "20 + 20 + 20 = 60 cm."),
    ("Which tools help measure motion?", "a stopwatch and a meter stick", ["a thermometer and a cup", "a magnet and a mirror", "a scale and a spoon"], "Measure time and distance."),
    ("A merry-go-round turns once every 10 seconds. How many turns in 30 seconds?", "3", ["10", "30", "1"], "30 ÷ 10 = 3 turns."),
    ("Why can you predict when a clock's pendulum will swing back?", "It swings in a regular rhythm.", ["It moves randomly.", "It never comes back.", "It only swings at night."],
     "Regular patterns let us predict."),
])
B5 = bank([
    ("Ava times 10 swings of a pendulum three times: 12 s, 12 s, 13 s. Why did she repeat the test?", "to check that the pattern is reliable", ["to make the pendulum faster", "to change the string", "to stop the pendulum"],
     "Repeated results that are about the same show a reliable pattern."),
    ("Leo rolls a marble in a bowl. It rocks back and forth and slowly stops at the bottom. What will happen if he gives it the same push again?", "It will rock back and forth in the same pattern.", ["It will roll out of the bowl upward forever.", "It will not move.", "It will move in a square."],
     "The same push gives the same pattern."),
    ("Mia sees a stoplight change green, yellow, red, green, yellow, red. What color comes next?", "green", ["yellow", "red", "blue"],
     "Patterns that repeat help us predict."),
    ("A ball rolls down the same ramp 5 times and always stops near the 80 cm mark. Where will it stop on the 6th try?", "near the 80 cm mark", ["at 0 cm", "at 200 cm", "You cannot predict it at all."],
     "The pattern lets you predict."),
    ("Noah's swing goes back and forth 8 times in 20 seconds. He makes the chains shorter. What should he do to find out how this changes the pattern?", "count the swings in 20 seconds again and compare", ["guess without measuring", "paint the swing", "use a different playground"],
     "Measure again and compare."),
])


def body():
    think = ("<p>Many objects move in <b>patterns</b> that repeat: a swing goes <b>back and forth</b>, a merry-go-round goes <b>around in a circle</b>, a yo-yo goes <b>up and down</b>.</p>"
             "<p>When we <b>observe and measure</b> motion (with a stopwatch and a meter stick), we can find the pattern and <b>predict</b> what will happen next.</p>"
             + figure(pendulum("left"), "A pendulum swings left, middle, right, middle, left ... again and again."))
    ex = [("A car moves 15 cm each second: 0, 15, 30, 45 cm. Where will it be at 4 seconds?", ["It adds 15 cm each second.", "45 + 15 = 60"], "60 cm"),
          ("A swing goes back and forth 6 times in 10 seconds. How many times in 20 seconds?", ["20 seconds is 2 × 10 seconds.", "2 × 6 = 12"], "12 times")]
    mist = ["Thinking motion cannot be predicted. Repeating patterns can be predicted.",
            "Adding the wrong amount when the object moves the same distance each second.",
            "Thinking a swing keeps going forever. Friction slowly stops it."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Motion that repeats", B1 + [(g_kind, 8), (g_swing, 4)]),
        ("Back and forth", [(g_swing, 10), (g_kind, 4), (g_count, 6)]),
        ("Measuring steady motion", [(g_steady, 14), (g_count, 6)]),
        ("Predicting motion from data", [(g_count, 8), (g_bounce, 6), (g_steady, 6)]),
        ("Motion investigations", B5 + [g_swing, g_steady, g_count, g_bounce]),
    ])
    make("grade-3", "patterns-of-motion", 2, "3-PS2-2",
         "Make observations and/or measurements of an object’s motion to provide evidence that a pattern can be used to predict future motion.",
         "Patterns of Motion",
         "Grade 3 Motion Worksheets: Patterns of Motion and Predicting with Data",
         "Patterns of Motion",
         "Free Grade 3 science worksheets on patterns of motion (NGSS 3-PS2-2): swings and pendulums, back and forth and circular motion, steady motion tables and predicting future motion. 100 practice questions with answers.",
         "Patterns of motion help us predict what comes next.",
         "A swing goes back and forth in a regular pattern. If we measure it, we can predict where it will be.",
         body(),
         [("What is a pattern of motion?", "It is a way of moving that repeats, like a swing going back and forth or a merry-go-round turning in circles."),
          ("How can you predict future motion?", "Measure the motion, find the pattern, and use it to say what will happen next."),
          ("Why does a swing stop if no one pushes it?", "Friction and the air slow it down a little on each swing.")],
         sets)


if __name__ == "__main__":
    main()
