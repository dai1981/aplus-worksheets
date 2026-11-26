# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Solving Problems Like an Engineer (K-2-ETS1-1, K-2-ETS1-2, K-2-ETS1-3)
  python tools/gen_us_science_g2_solving_problems_like_an_engineer.py
Define a simple problem, sketch how the shape of an object helps it work, and compare test data from two designs.
Steps: ask, imagine, plan, create, test, improve.
Wrong answers come from real mistakes: "start building before knowing the problem", "the prettiest design is best",
"one test is enough", "shape does not matter".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, svg_wrap, arrow, People
from ws_common import text, INK
import sci_kids as K

U = Unit(20112)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


STEPS = ["ask", "imagine", "plan", "create", "test", "improve"]


def steps_svg(hide=None):
    s = ""
    for i, st in enumerate(STEPS):
        x = 40 + i * 86
        s += "<rect x='%d' y='20' width='64' height='36' rx='8' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x - 32, "#fff3c4" if st != hide else "#ffffff", INK)
        s += text(x, 44, "?" if st == hide else st, 13)
        if i:
            s += arrow(x - 52, 38, x - 34, 38, INK, 2, 6)
    return svg_wrap(512, 74, s, "engineering steps: " + ", ".join("?" if st == hide else st for st in STEPS))


def g_step():
    who = P.next()[0]
    k = R.choice(["next", "hide", "first"])
    if k == "first":
        if not once("first", 2):
            return None
        return item("%s wants to solve a problem. What should %s do first?" % (who, who), "ask questions to understand the problem", ["build right away", "test the design", "paint the design"],
                    "Engineers start by asking.")
    if k == "hide":
        h = R.choice(STEPS)
        if not once(("h", h)):
            return None
        return item(fig(steps_svg(h)) + "%s's poster shows the engineering steps. Which word is missing?" % who, h, R.sample([x for x in STEPS if x != h], 3), "Ask, imagine, plan, create, test, improve.")
    i = R.randrange(5)
    if not once(("n", i)):
        return None
    return item("%s just finished the “%s” step. What comes next?" % (who, STEPS[i]), STEPS[i + 1], R.sample([x for x in STEPS if x not in (STEPS[i], STEPS[i + 1])], 3),
                "Ask, imagine, plan, create, test, improve.")


SITU = [("Jen's crayons roll off her desk.", "Crayons need something to keep them from rolling.", "a holder or tray for the crayons"),
        ("Ducks at the park get wet in the rain.", "The ducks need a dry place in the rain.", "a small roof or shelter"),
        ("The class plant falls over in the wind.", "The plant needs support so it stands up.", "a stick and a soft tie"),
        ("Water spills when Sam pours it into a small bottle.", "Water needs to go into a small opening without spilling.", "a funnel"),
        ("Leo can't reach the top shelf.", "Leo needs a safe way to reach high things.", "a sturdy step stool"),
        ("Birds eat all the seeds in the garden.", "Seeds need protection from birds.", "a net over the garden"),
        ("Mia's lunch gets squished in her bag.", "The lunch needs to be protected from squishing.", "a hard lunch box"),
        ("Snow piles up on the school steps.", "The steps need a way to stay clear of snow.", "a small roof over the steps"),
        ("The class hamster gets out of its cage.", "The cage needs a way to keep the hamster in.", "a cage door that latches"),
        ("Toy cars roll too fast down the ramp and crash.", "The cars need to slow down on the ramp.", "a rougher ramp or a lower slope")]


def g_define():
    s, p, t = R.choice(SITU)
    who = P.next()[0]
    k = R.random() < 0.5
    if not once((s, k)):
        return None
    if k:
        w = R.sample([x[1] for x in SITU if x[1] != p], 2) + ["There is no problem."]
        return item("%s notices: “%s” What is the problem to solve?" % (who, s), p, w, "Say the problem clearly before building.")
    w = R.sample([x[2] for x in SITU if x[2] != t], 2) + ["a bigger crayon box for the whole school" if "crayon" not in s else "a new paint color"]
    return item("%s notices: “%s” Which tool could solve it?" % (who, s), t, w, "The tool must fit the problem.")


# object, part/shape, plural part?, what it helps the object do, picture
SHAPE = [("a spoon", "the round, curved end", 0, "hold soup without spilling", "spoon"), ("a ball", "the round shape", 0, "roll easily", "ball"),
         ("an umbrella", "the dome shape", 0, "let rain slide off", "umbrella"), ("a cup", "the handle", 0, "let you hold a hot drink safely", "cup"),
         ("a straw", "the hollow tube", 0, "let liquid flow through", None), ("a funnel", "the wide top and narrow bottom", 1, "guide liquid into a small opening", None),
         ("a wagon", "the round wheels", 1, "move smoothly", None), ("a shovel", "the flat, wide scoop", 0, "pick up a lot of dirt", None),
         ("a fork", "the pointy prongs", 1, "pick up food", None), ("a rake", "the long teeth", 1, "gather leaves", None),
         ("a sun hat", "the wide brim", 0, "shade your face", "hat"), ("a bird", "the strong, pointed beak", 0, "crack seeds", "bird"),
         ("a coat", "the hood", 0, "keep rain off your head", "coat"), ("a bike", "the brakes", 1, "stop safely", None)]


def g_shape():
    o, part, pl, does, pic = R.choice(SHAPE)
    who = P.next()[0]
    k = R.random() < 0.6
    if not once((o, k)):
        return None
    fg = fig(K.card(pic)) if pic else ""
    if k:
        w = R.sample([x[3] for x in SHAPE if x[3] != does], 3)
        return item(fg + "%s looks at %s. What %s %s help %s do?" % (who, o, "do" if pl else "does", part, o.replace("a ", "the ", 1).replace("an ", "the ", 1)), does, w,
                    "Shape helps an object do its job.")
    w = R.sample([x[1] for x in SHAPE if x[1] != part], 3)
    return item(fg + "%s draws %s. Which part helps %s %s?" % (who, o, o.replace("a ", "the ", 1).replace("an ", "the ", 1), does), part, w,
                "%s helps %s %s." % (part[0].upper() + part[1:], o.replace("a ", "the ", 1).replace("an ", "the ", 1), does))


DES = [("paper boats", "pennies held before sinking", True, [("boat A", "folded paper", 8, 15), ("boat B", "foil", 18, 30)]),
       ("towers", "centimeters tall before falling", True, [("tower A", "paper cups", 40, 60), ("tower B", "wooden blocks", 70, 90)]),
       ("paper airplanes", "steps it flew", True, [("plane A", "a pointed nose", 12, 18), ("plane B", "a flat nose", 4, 9)]),
       ("cups for ice", "minutes until the ice melted", True, [("cup A", "foam", 40, 60), ("cup B", "paper", 15, 25)]),
       ("roofs for a model house", "drops that leaked through", False, [("roof A", "plastic", 0, 2), ("roof B", "paper", 8, 14)]),
       ("ramps to slow a toy car", "seconds to reach the bottom", True, [("ramp A", "a carpet top", 4, 6), ("ramp B", "a smooth wood top", 1, 2)])]


def g_data():
    things, meas, bigger, rows = R.choice(DES)
    who = P.next()[0]
    v = [R.randint(lo, hi) for *_, lo, hi in rows]
    k = R.choice(["best", "diff", "why", "worse"])
    if v[0] == v[1] or not once((things, k, v[0], v[1])):
        return None
    if not once(("dk", things, k), 2):
        return None
    tab = table(["Design", "Idea", meas[0].upper() + meas[1:]], [[n, m, str(x)] for (n, m, *_), x in zip(rows, v)])
    bi = max(range(2), key=lambda i: v[i] if bigger else -v[i])
    best, worst = rows[bi], rows[1 - bi]
    if k == "best":
        return item(tab + "%s tested two %s. Which design worked better?" % (who, things), best[0], [worst[0], "They worked the same.", "Neither one worked."],
                    "%s: %d %s." % (best[0], v[bi], meas.split(" (")[0]))
    if k == "worse":
        return item(tab + "%s tested two %s. What is a weakness of %s?" % (who, things, worst[0]), "Its result was worse than %s's." % best[0],
                    ["It was the best design.", "It cannot be tested.", "It is the wrong color."], "Compare the numbers: %d and %d." % (v[0], v[1]))
    if k == "why":
        return item(tab + "%s tested two %s. Why might %s have worked better?" % (who, things, best[0]), "It used %s." % best[1],
                    ["It used %s." % worst[1], "It was a prettier color.", "It was tested fewer times."], "The material or shape made the difference: %s." % best[1])
    d = abs(v[0] - v[1])
    return item(tab + "In %s's test of two %s, what is the difference between the two results?" % (who, things), str(d), [str(max(v)), str(v[0] + v[1]), str(d + 1)],
                "%d − %d = %d." % (max(v), min(v), d))


B1 = bank([
    ("What does an engineer do?", "designs things to solve problems", ["only paints pictures", "only reads books", "only plays games"], "Engineers solve problems."),
    ("What is a problem in engineering?", "a situation people want to change", ["a math worksheet", "a kind of tool", "a happy day"], "Find what needs to change."),
    ("Why do engineers draw a sketch?", "to show their idea and plan it", ["to waste paper", "to skip testing", "to make it pretty only"], "Sketches help plan."),
    ("Why do engineers test a design?", "to see if it solves the problem", ["to break it for fun", "to make it heavier", "to finish faster"], "Testing gives data."),
    ("What should an engineer do if a design fails a test?", "improve it and test again", ["give up", "throw it away and stop", "say it worked"], "Improve and try again."),
    ("Why is a ball round?", "so it can roll", ["so it is heavy", "so it is see-through", "so it cannot move"], "Shape helps it work."),
    ("Which is the first engineering step?", "ask", ["test", "improve", "create"], "Ask questions first."),
    ("Why compare two designs?", "to find the strengths and weaknesses of each", ["to pick the prettier one", "to make more trash", "to skip testing"], "Use data."),
])
B5 = bank([
    ("Ava's foil boat held 25 pennies. Her paper boat held 10. What should she do next?", "use foil and try to make it hold even more", ["give up", "use paper because it held less", "stop testing"], "Improve the better design."),
    ("Leo tested his bridge only once. Why should he test more times?", "to make sure the result is true", ["to make it heavier", "to make it fall", "there is no reason"], "More tests, more trust."),
    ("Mia's ramp is too steep, so the car crashes. How can she improve it?", "make the ramp less steep", ["make it steeper", "paint it red", "use a bigger car"], "Change one thing and test again."),
    ("Kai sketches a bird feeder with a roof. What does the roof help do?", "keep the seeds dry", ["make the birds bigger", "make it heavier", "hide the seeds"], "Shape helps function."),
    ("Two cups kept ice: foam 50 minutes, paper 20 minutes. Which is a strength of the foam cup?", "It kept the ice cold longer.", ["It melted the ice faster.", "It is paper.", "It is smaller."], "50 is more than 20."),
])


def body():
    pic = steps_svg()
    ex = [("Crayons roll off a desk. What is the problem?", ["What needs to change?"], "Crayons need something to stop them rolling."),
          ("A foil boat held 20 pennies, a paper boat held 9. Which is better?", ["More pennies is better."], "the foil boat")]
    mist = ["Building before you know the problem.",
            "Choosing the prettiest design, not the one that works.",
            "Testing only once."]
    return kid_lesson(pic, "Engineers solve problems step by step.",
                      ["Ask: what is the problem?", "Draw it: the shape helps it work.", "Test two designs and compare."], ex, mist)


def main():
    sets = U.sets([
        ("What engineers do", B1 + [(g_step, 6), (g_define, 6)]),
        ("Defining the problem", [(g_define, 14), (g_step, 6)]),
        ("Shape and function", [(g_shape, 16), (g_step, 4)]),
        ("Testing two designs", [(g_data, 12), (g_shape, 8)]),
        ("Improving designs", B5 + [(g_data, 10), (g_shape, 2), (g_step, 3)]),
    ])
    make("grade-2", "solving-problems-like-an-engineer", 12, "K-2-ETS1-1",
         "Ask questions, make observations, and gather information about a situation people want to change to define a simple problem that can be solved through the development of a new or improved object or tool. "
         "Develop a simple sketch, drawing, or physical model to illustrate how the shape of an object helps it function as needed to solve a given problem. "
         "Analyze data from tests of two objects designed to solve the same problem to compare the strengths and weaknesses of how each performs.",
         "Solving Problems Like an Engineer",
         "Grade 2 Engineering Worksheets: Define a Problem, Shape and Function, Compare Designs",
         "Engineering",
         "Free grade 2 engineering worksheets (NGSS K-2-ETS1): define a problem, see how shape helps objects work, and compare test data from two designs. 100 questions with answers.",
         "Ask, plan, build, test, improve.",
         "Engineers solve problems and use tests to pick the best design.",
         body(),
         [("What are the engineering steps?", "Ask, imagine, plan, create, test and improve."),
          ("How does shape help an object?", "A spoon's curve holds soup, a ball's round shape rolls, and an umbrella's dome lets rain slide off."),
          ("How do kids compare two designs?", "Test both the same way, write the results in a table and see which one works better.")],
         sets)


if __name__ == "__main__":
    main()
