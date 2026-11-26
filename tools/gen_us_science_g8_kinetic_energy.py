# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Kinetic Energy (MS-PS3-1)
  python tools/gen_us_science_g8_kinetic_energy.py
Construct and interpret graphical displays of data to describe the relationships of kinetic energy to the mass of an
object and to the speed of an object. KE = 1/2 m v^2: doubling mass doubles KE, doubling speed makes KE four times.
Wrong answers come from real mistakes: "doubling speed doubles KE", "forgetting the 1/2", "forgetting to square v",
"objects at rest have kinetic energy".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People, comma

U = Unit(80105)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


THINGS = ["a cart", "a bowling ball", "a bicycle and rider", "a skateboarder", "a soccer ball", "a toy car", "a sled", "a runner"]
OBJ = [("a toy car", [2, 3], [2, 3, 4, 5]), ("a bowling ball", [6], [2, 3, 4, 5]), ("a lab cart", [2, 4, 5], [2, 3, 4]), ("a sled with a child", [40], [2, 3, 4, 5]),
       ("a runner", [50, 60], [3, 4, 5, 6]), ("a bicycle and rider", [80], [3, 4, 5, 6]), ("a skateboarder", [40, 50], [2, 3, 4, 5]), ("a shopping cart", [20, 30], [2, 3])]


def ke(m, v):
    return m * v * v / 2


def J(x):
    return comma(int(x)) + " J" if x == int(x) else ("%g J" % x)


def g_calc():
    th, ms, vs = R.choice(OBJ)
    m, v = R.choice(ms), R.choice(vs)
    if v == 1 or not once(("c", m, v)):
        return None
    who = P.next()[0]
    a = ke(m, v)
    w = [J(m * v * v), J(m * v / 2), J(m * v)]
    w = [x for x in dict.fromkeys(w) if x != J(a)]
    if len(w) < 3:
        w.append(J(a + m))
    return item("%s measures %s with a mass of %d kg moving at %d m/s. What is its kinetic energy? (KE = ½ × m × v²)" % (who, th, m, v), J(a), w[:3],
                "KE = ½ × %d × %d² = ½ × %d × %d = %s." % (m, v, m, v * v, J(a)))


def g_scale():
    who = P.next()[0]
    k = R.choice(["m2", "m3", "v2", "v3", "vh"])
    base = R.choice([40, 80, 100, 120, 200, 300, 400, 600])
    th = R.choice(["a cart", "a sled", "a wagon", "a go-kart", "a skateboarder", "a bike rider"])
    if not once(("s", k, base)):
        return None
    if k[0] == "m":
        f = int(k[1])
        return item("%s observes %s with %s of kinetic energy. If its mass is %s but its speed stays the same, what is its new kinetic energy?" % (who, th, J(base), "doubled" if f == 2 else "tripled"),
                    J(base * f), [J(base * f * f), J(base), J(base / f) if base % f == 0 else J(base + f)], "KE is proportional to mass: %d × %s = %s." % (f, J(base), J(base * f)))
    if k == "vh":
        return item("%s observes %s with %s of kinetic energy. If its speed is cut in half, what is its new kinetic energy?" % (who, th, J(base)), J(base / 4), [J(base / 2), J(base), J(base * 2)],
                    "Half the speed → (½)² = ¼ of the KE: %s." % J(base / 4))
    f = int(k[1])
    return item("%s observes %s with %s of kinetic energy. If its speed is %s and its mass stays the same, what is its new kinetic energy?" % (who, th, J(base), "doubled" if f == 2 else "tripled"),
                J(base * f * f), [J(base * f), J(base), J(base / f) if base % f == 0 else J(base * f + base)], "KE depends on speed squared: %d² = %d, so %d × %s = %s." % (f, f * f, f * f, J(base), J(base * f * f)))


def g_graph():
    who = P.next()[0]
    k = R.choice(["mass", "speed"])
    if k == "mass":
        v = R.choice([2, 4, 6])
        ms = [1, 2, 3, 4]
        vals = [ke(m, v) for m in ms]
        ch = bar_chart(["%d kg" % m for m in ms], vals, "kinetic energy (J)", "bar graph of kinetic energy for carts of different mass at %d m/s" % v, ymax=max(vals), step=max(vals) // 4, w=300)
        q = R.choice(["shape", "pred"])
        if not once(("g", k, v, q)):
            return None
        if q == "shape":
            return item(fig(ch) + "%s's carts all moved at %d m/s. What does the graph show?" % (who, v), "Kinetic energy increases in equal steps as mass increases (a straight-line relationship).",
                        ["Kinetic energy increases faster and faster as mass increases.", "Mass has no effect on kinetic energy.", "Kinetic energy decreases as mass increases."],
                        "KE is directly proportional to mass.")
        return item(fig(ch) + "Using %s's graph, what would the kinetic energy of an 8 kg cart at %d m/s be?" % (who, v), J(ke(8, v)), [J(ke(4, v)), J(ke(8, v) * 2), J(ke(5, v))],
                    "Twice the mass of the 4 kg cart → twice the KE.")
    m = R.choice([2, 4, 6])
    vs = [1, 2, 3, 4]
    vals = [ke(m, v) for v in vs]
    ch = bar_chart(["%d m/s" % v for v in vs], vals, "kinetic energy (J)", "bar graph of kinetic energy for a %d kg cart at different speeds" % m, ymax=max(vals), step=max(vals) // 4, w=300)
    q = R.choice(["shape", "pred"])
    if not once(("g", k, m, q)):
        return None
    if q == "shape":
        return item(fig(ch) + "%s's %d kg cart was rolled at different speeds. What does the graph show?" % (who, m), "Kinetic energy increases faster and faster as speed increases.",
                    ["Kinetic energy increases in equal steps as speed increases.", "Speed has no effect on kinetic energy.", "Kinetic energy decreases as speed increases."],
                    "KE depends on speed squared, so the graph curves upward.")
    return item(fig(ch) + "Using %s's graph, what would the kinetic energy of the %d kg cart at 8 m/s be?" % (who, m), J(ke(m, 8)), [J(ke(m, 4) * 2), J(ke(m, 4)), J(ke(m, 4) * 3)],
                "Double the speed of 4 m/s → 4 times the KE.")


def g_compare():
    who = P.next()[0]
    a = (R.choice([2, 4, 6]), R.choice([2, 3, 4]))
    b = (a[0] * 2, a[1])
    c = (a[0], a[1] * 2)
    opts = [("Cart A", a), ("Cart B", b), ("Cart C", c)]
    if not once(("cmp", a, R.random() < 0.5)):
        return None
    rows = [[n, "%d kg" % x[0], "%d m/s" % x[1]] for n, x in opts]
    tab = table(["Cart", "Mass", "Speed"], rows)
    if R.random() < 0.5:
        best = max(opts, key=lambda o: ke(*o[1]))[0]
        return item(tab + "Which of %s's carts has the most kinetic energy?" % who, best, [n for n, _ in opts if n != best] + ["They all have the same."],
                    "Cart C: doubling speed gives 4 times the KE; doubling mass gives only 2 times.")
    return item(tab + "How many times more kinetic energy does Cart C have than Cart A in %s's table?" % who, "4 times", ["2 times", "the same", "8 times"],
                "Cart C moves twice as fast: 2² = 4 times the KE.")


B1 = bank([
    ("What is kinetic energy?", "the energy an object has because it is moving", ["energy stored in an object's position", "energy from food only", "the mass of an object"], "Moving objects have KE."),
    ("Which two things determine an object's kinetic energy?", "its mass and its speed", ["its color and shape", "its height only", "its temperature only"], "KE = ½mv²."),
    ("Does a parked car have kinetic energy?", "No, because it is not moving.", ["Yes, because it is heavy.", "Yes, because it has fuel.", "Only at night."], "Speed is 0, so KE is 0."),
    ("If two balls roll at the same speed, which has more kinetic energy?", "the one with more mass", ["the one with less mass", "the smaller one", "they always have the same"], "More mass → more KE."),
    ("What happens to kinetic energy if speed doubles?", "It becomes 4 times as large.", ["It doubles.", "It stays the same.", "It halves."], "Speed is squared."),
    ("What unit is used for energy?", "joule (J)", ["newton (N)", "kilogram (kg)", "meter per second (m/s)"], "1 J = 1 kg·m²/s²."),
    ("Why is a speeding truck more dangerous than a slow one?", "Its kinetic energy is much larger, so a crash transfers much more energy.", ["It weighs less.", "It has no energy.", "Speed does not matter."], "KE grows with v²."),
    ("Which has more kinetic energy: a 1 kg ball at 10 m/s or a 10 kg ball at 1 m/s?", "the 1 kg ball at 10 m/s (50 J vs. 5 J)", ["the 10 kg ball", "they are the same", "neither has kinetic energy"], "½ × 1 × 100 = 50 J; ½ × 10 × 1 = 5 J."),
])
B5 = bank([
    ("Ava wants to graph how mass affects kinetic energy. What should she keep the same?", "the speed", ["the mass", "nothing", "the kinetic energy"], "Change mass, keep speed the same."),
    ("Leo graphs kinetic energy against speed and gets a curve that bends upward. Why?", "Kinetic energy depends on speed squared.", ["He made a mistake.", "Speed does not affect KE.", "Mass changed."], "The relationship is not a straight line."),
    ("Mia's 60 kg brother rides a bike at 5 m/s. What is his kinetic energy (ignore the bike)?", "750 J", ["150 J", "300 J", "1,500 J"], "½ × 60 × 25 = 750 J."),
    ("A ball has 80 J of kinetic energy. It slows to half its speed. How much KE is left?", "20 J", ["40 J", "80 J", "160 J"], "(½)² × 80 = 20 J."),
    ("Which graph type best shows kinetic energy for carts of four different masses?", "a bar graph or line graph with mass on the x-axis and KE on the y-axis", ["a pie chart of colors", "a map", "a table with no numbers"],
     "Put the variable you change on the x-axis."),
])


def body():
    think = ("<p><b>Kinetic energy</b> (KE) is the energy of motion. It depends on <b>mass</b> and <b>speed</b>:</p>"
             "<p><b>KE = ½ × m × v²</b> (m in kg, v in m/s, KE in joules)</p>"
             "<ul><li>Double the <b>mass</b> → KE doubles (straight-line graph).</li>"
             "<li>Double the <b>speed</b> → KE becomes <b>4 times</b> as large (graph curves upward).</li></ul>")
    ex = [("A 4 kg cart moves at 3 m/s. What is its KE?", ["½ × 4 × 3²", "½ × 4 × 9"], "18 J"),
          ("A bike has 200 J of KE. Its speed doubles. New KE?", ["2² = 4", "4 × 200"], "800 J")]
    mist = ["Thinking doubling speed doubles KE. It makes it 4 times.",
            "Forgetting the ½ or forgetting to square the speed.",
            "Thinking an object at rest has kinetic energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy of motion", B1 + [(g_calc, 10), (g_compare, 2)]),
        ("Calculating kinetic energy", [(g_calc, 12), (g_compare, 8)]),
        ("Mass and speed", [(g_scale, 14), (g_compare, 6)]),
        ("Graphs of kinetic energy", [(g_graph, 9), (g_scale, 8), (g_calc, 3)]),
        ("Interpreting data", B5 + [g_graph, g_scale, g_calc, g_compare]),
    ])
    make("grade-8", "kinetic-energy", 5, "MS-PS3-1",
         "Construct and interpret graphical displays of data to describe the relationships of kinetic energy to the mass of an object and to the speed of an object.",
         "Kinetic Energy",
         "Grade 8 Kinetic Energy Worksheets: KE = ½mv², Mass, Speed and Graphs",
         "Kinetic Energy",
         "Free middle school science worksheets on kinetic energy (NGSS MS-PS3-1): KE = ½mv², how mass and speed affect kinetic energy, and reading graphs of kinetic energy data. 100 practice questions with answers.",
         "KE = ½ × mass × speed².",
         "Doubling the mass doubles kinetic energy. Doubling the speed makes it four times as large.",
         body(),
         [("How do you calculate kinetic energy?", "KE = ½ × m × v², with mass in kilograms and speed in meters per second. The answer is in joules."),
          ("Why does speed matter more than mass for kinetic energy?", "Speed is squared. Doubling speed gives 4 times the kinetic energy, but doubling mass only doubles it."),
          ("What does a graph of kinetic energy vs. speed look like?", "It curves upward, because kinetic energy depends on the square of speed. A graph of KE vs. mass is a straight line.")],
         sets)


if __name__ == "__main__":
    main()
