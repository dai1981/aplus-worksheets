# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Energy and Speed (4-PS3-1)
  python tools/gen_us_science_g4_energy_and_speed.py
The faster an object moves, the more energy it has. Evidence comes from ramps (higher start ->
faster ball -> the cup or block it hits moves farther) and from everyday motion.
Assessment boundary: no quantitative measures of energy, so questions compare, not calculate energy.
Wrong answers come from real mistakes: "bigger always means more energy", "a moving object's energy
stays the same when it slows down", "energy is the same as force".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, figure, svg_wrap, line, rect, circle, text, People, INK, BLUE, RED

U = Unit(40101)
R = U.R
P = People(R)
THINGS = ["bike", "skateboard", "soccer ball", "toy car", "shopping cart", "sled", "scooter", "bowling ball", "wagon", "roller coaster car"]


def ramp(h, d, label="ball rolling down a ramp into a cup"):
    W, H = 360, 140
    x0, y0, x1 = 20, 120 - h * 3, 150
    s = [line(10, 122, W - 10, 122, INK, 2), "<path d='M%d %d L%d 122 L%d 122 Z' fill='#e4e4e4' stroke='%s' stroke-width='2'/>" % (x0, y0, x1, x0, INK),
         circle(x0 + 10, y0 - 9, 8, BLUE, INK, 1.5), text(x0 - 4, y0 + 4, "%d cm" % h, 11, "start", weight=400) if False else "",
         rect(x1 + 6 + d * 4, 104, 22, 18, "#f6dcb4", INK, 1.5),
         line(x1 + 6, 132, x1 + 6 + d * 4, 132, RED, 2), text(x1 + 6 + d * 2, 138, "%d cm" % d, 11, col=RED, weight=400)]
    return svg_wrap(W, H, "".join(s), label)


def cap(s):
    return s[0].upper() + s[1:]


SPEED = {"bike": 8, "skateboard": 6, "soccer ball": 15, "toy car": 3, "shopping cart": 3, "sled": 10, "scooter": 6, "bowling ball": 8, "wagon": 3, "roller coaster car": 25}


def g_compare():
    t = R.choice(THINGS)
    a, b = sorted(R.sample(range(1, SPEED[t] + 1), 2))
    unit = "meters per second"
    ask = R.choice(["more", "less"])
    ans = "the %s moving at %d %s" % (t, b if ask == "more" else a, unit)
    w = ["the %s moving at %d %s" % (t, a if ask == "more" else b, unit), "They have the same energy.", "Speed does not change energy."]
    one = lambda v: ("%d meter per second" % v) if v == 1 else ("%d meters per second" % v)
    ans = "the %s moving at %s" % (t, one(b if ask == "more" else a))
    w = ["the %s moving at %s" % (t, one(a if ask == "more" else b)), "They have the same energy.", "Speed does not change energy."]
    return item("The same %s moves at %s and later at %s. When does it have %s energy of motion?" % (t, one(a), one(b), ask),
                ans, w, "The same object has more energy when it moves faster and less when it moves slower.")


def g_ramp_table():
    hs = sorted(R.sample([5, 10, 15, 20, 25, 30, 40], 4))
    ds = [h // 5 * R.choice([3, 4]) + R.randint(0, 2) for h in hs]
    ds = sorted(ds)
    if len(set(ds)) < 4:
        return None
    rows = [["%d cm" % h, "%d cm" % d] for h, d in zip(hs, ds)]
    k = R.choice(["most", "pattern", "predict"])
    p = P.next()
    tab = table(["Start height on ramp", "Distance the cup moved"], rows)
    if k == "most":
        return item(tab + "%s rolled the same ball down a ramp into a cup. In which trial was the ball moving fastest when it hit the cup?" % p[0],
                    "the %d cm start" % hs[-1], ["the %d cm start" % h for h in hs[:-1]][:3],
                    "The higher start made the ball move fastest, so it had the most energy and pushed the cup the farthest (%d cm)." % ds[-1])
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % p[0], "The higher the start, the faster the ball and the farther the cup moved.",
                    ["The higher the start, the shorter the cup moved.", "The height did not matter.", "The cup moved the same distance every time."],
                    "From %d cm to %d cm the cup moved from %d cm to %d cm. A faster ball has more energy to transfer." % (hs[0], hs[-1], ds[0], ds[-1]))
    mid = (hs[1] + hs[2]) // 2
    if mid in hs:
        return None
    return item(tab + "%s tries a start height of %d cm. About how far will the cup move?" % (p[0], mid),
                "between %d cm and %d cm" % (ds[1], ds[2]), ["less than %d cm" % ds[0], "more than %d cm" % ds[-1], "0 cm"],
                "%d cm is between %d cm and %d cm, so the distance should be between %d cm and %d cm." % (mid, hs[1], hs[2], ds[1], ds[2]))


def g_pic():
    h = R.choice([10, 20, 30])
    d = {10: 8, 20: 16, 30: 24}[h]
    k = R.choice(["higher", "lower"])
    return item(fig(ramp(h, d)) + "A ball rolls down a ramp and pushes a block %d cm. If the ball starts %s on the ramp, what will most likely happen?" % (d, k),
                "The block will move %s than %d cm." % ("farther" if k == "higher" else "less far", d),
                ["The block will move %s than %d cm." % ("less far" if k == "higher" else "farther", d), "The block will move exactly %d cm again." % d, "The block will not move at all."],
                "A %s start means the ball is moving %s at the bottom, so it has %s energy to give the block." % (k, "faster" if k == "higher" else "slower", "more" if k == "higher" else "less"))


B1 = bank([
    ("What is energy?", "the ability to make things move or change", ["a kind of matter", "the weight of an object", "a force that only pulls"],
     "Energy can make objects move, warm up, light up or make sound."),
    ("Energy of motion is the energy an object has because it is", "moving", ["big", "cold", "heavy but still"],
     "Every moving object has energy of motion."),
    ("Which has more energy of motion?", "a ball rolling quickly", ["the same ball rolling slowly", "the same ball sitting still", "They all have the same."],
     "For the same object, faster means more energy of motion."),
    ("A ball sitting still on the floor has", "no energy of motion", ["a lot of energy of motion", "the most energy of motion", "energy of motion only if it is red"],
     "It is not moving, so it has no energy of motion."),
    ("A bike slows down as it rolls up a hill. What happens to its energy of motion?", "It decreases.", ["It increases.", "It stays the same.", "It turns into a force."],
     "Slower motion means less energy of motion."),
    ("Why does a fast pitch sting your hand more than a slow pitch?", "The faster ball has more energy to transfer to your hand.", ["Fast balls are heavier.", "Slow balls have no energy.", "Your hand is colder."],
     "The faster ball carries more energy, and some of it goes into your hand."),
    ("Which statement about speed and energy is true?", "The faster an object moves, the more energy it has.", ["The slower an object moves, the more energy it has.", "Speed has nothing to do with energy.", "Only big objects have energy."],
     "This is the main idea of 4-PS3-1."),
    ("A runner speeds up at the end of a race. What happens to the runner's energy of motion?", "It increases.", ["It decreases.", "It stays the same.", "It disappears."],
     "Faster motion means more energy of motion."),
    ("Which tool helps measure speed?", "a stopwatch and a measuring tape", ["a thermometer", "a balance", "a magnet"],
     "Speed = distance ÷ time, so you measure both."),
    ("A car travels 100 meters in 10 seconds. Another car travels 100 meters in 20 seconds. Which is faster?", "the car that took 10 seconds", ["the car that took 20 seconds", "They are the same speed.", "You cannot tell."],
     "The same distance in less time means a faster speed."),
])
B5 = bank([
    ("Ava rolls a marble from different heights on a ramp. What should she keep the same?", "the marble, the ramp and the cup", ["the start height", "nothing", "the number of trials only"],
     "Only the start height should change, so speed is the only difference."),
    ("Why should Ava do each height three times?", "to check that her results are reliable", ["to make the marble faster", "to change the variable", "so the ramp gets warm"],
     "Repeating trials shows whether a result happens again."),
    ("Leo says a big slow truck must always have more energy of motion than a small fast truck. Why is his claim not supported by speed alone?", "Speed also matters, so you must compare the same object at different speeds.", ["Big things never move.", "Small things have no energy.", "Trucks have no energy."],
     "In grade 4 we compare the same object at different speeds to see that speed changes energy."),
    ("In a bowling game, which roll knocks down more pins?", "a fast roll of the same ball", ["a slow roll of the same ball", "a ball that is not moving", "They always knock down the same number."],
     "The faster ball has more energy to transfer to the pins."),
    ("A swing is pushed harder and moves faster. What evidence shows it has more energy?", "It swings higher and farther.", ["It becomes heavier.", "It changes color.", "It stops at once."],
     "More energy of motion lets it move farther."),
    ("Mia lets a toy car go from the top of a long ramp and from halfway down. Which car hits the wall harder?", "the car from the top of the ramp", ["the car from halfway down", "They hit the wall equally hard.", "Neither car moves."],
     "The car from the top is moving faster at the bottom, so it has more energy."),
])


def body():
    think = ("<p><b>Energy</b> is the ability to make things move or change. A moving object has <b>energy of motion</b>.</p>"
             "<p>The <b>faster</b> an object moves, the <b>more energy</b> it has. A fast ball can push a cup farther, ring a bell louder "
             "or sting your hand more than the same ball moving slowly.</p>"
             + figure(ramp(20, 16), "A ball from higher on the ramp moves faster and pushes the block farther."))
    ex = [("The same ball starts at 10 cm and at 30 cm on a ramp. Which start pushes the cup farther?", ["Higher start = faster ball.", "Faster ball = more energy."], "the 30 cm start"),
          ("A bike slows from fast to slow. What happens to its energy of motion?", ["Slower means less energy of motion."], "It decreases.")]
    mist = ["Thinking a bigger object always has more energy. Compare the same object at different speeds.",
            "Thinking speed and energy are not connected. Faster means more energy.",
            "Changing more than one thing in a ramp test."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy of motion", B1 + [(g_compare, 8)]),
        ("Faster means more energy", [(g_compare, 10), (g_pic, 10)]),
        ("Ramp data", [(g_ramp_table, 14), (g_pic, 6)]),
        ("Evidence about speed and energy", [(g_ramp_table, 8), (g_compare, 6), (g_pic, 6)]),
        ("Investigations", B5 + [g_ramp_table, g_pic, g_compare]),
    ])
    make("grade-4", "energy-and-speed", 1, "4-PS3-1",
         "Use evidence to construct an explanation relating the speed of an object to the energy of that object.",
         "Energy and Speed",
         "Grade 4 Energy and Speed Worksheets: Energy of Motion and Ramp Investigations",
         "Energy and Speed",
         "Free Grade 4 science worksheets on energy and speed (NGSS 4-PS3-1): energy of motion, faster objects have more energy, and ramp investigations with data tables. 100 practice questions with answers.",
         "The faster an object moves, the more energy it has.",
         "A moving object has energy of motion. A faster ball can push a cup farther than the same ball moving slowly.",
         body(),
         [("How is speed related to energy?", "The faster an object moves, the more energy of motion it has. The same ball rolling fast has more energy than when it rolls slowly."),
          ("Does an object that is not moving have energy of motion?", "No. Energy of motion depends on motion. A ball sitting still has no energy of motion."),
          ("How can you show that faster objects have more energy?", "Roll the same ball down a ramp from different heights. The higher start makes the ball faster, and it pushes a cup farther.")],
         sets)


if __name__ == "__main__":
    main()
