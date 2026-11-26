# -*- coding: utf-8 -*-
"""
US Grade 6 Science: The Engineering Design Process (MS-ETS1-1, MS-ETS1-2, MS-ETS1-3, MS-ETS1-4)
  python tools/gen_us_science_g6_engineering_design_process.py
Define a design problem with precise criteria and constraints (including impacts on people and the
environment); evaluate competing solutions with a decision matrix; analyze test data to find the best
characteristics of each and combine them; iterative testing and modification of a model or prototype.
Wrong answers come from real mistakes: "a constraint is a goal", "the first design is always final",
"choose the solution that scores highest on one criterion only", "change several variables in one test".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(60112)
R = U.R
P = People(R)

PROBLEMS = [("a water filter for a camping trip", ["It must remove visible dirt from 1 liter of water.", "It must filter 1 liter in under 5 minutes."], ["It must cost less than $10.", "It must weigh less than 500 g."]),
            ("a backpack for carrying books", ["It must hold 8 kg without tearing.", "It must have padded straps."], ["It must be made from recycled fabric.", "It must cost less than $25."]),
            ("an egg-drop protector", ["The egg must not crack when dropped from 3 meters.", "It must land within 1 meter of the target."], ["It can use only 10 straws and 1 meter of tape.", "It must be built in 30 minutes."]),
            ("a playground shade structure", ["It must shade at least 20 square meters.", "It must stand up to strong winds."], ["It must cost less than $5,000.", "It must be built in one weekend."]),
            ("a bridge model", ["It must hold at least 2 kg.", "It must span a 40 cm gap."], ["It can use only 100 craft sticks and glue.", "It must weigh less than 300 g."]),
            ("a phone stand", ["It must hold a phone at a 60° angle.", "It must not tip over when tapped."], ["It must be made from one sheet of cardboard.", "It must fit in a pocket."])]


def g_cc():
    name, crit, cons = R.choice(PROBLEMS)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s's team is designing %s. Which is a criterion (what the design must do)?" % (who, name), R.choice(crit), cons + ["It must be finished by Friday."],
                    "Criteria describe what a successful solution must do.")
    return item("%s's team is designing %s. Which is a constraint (a limit on the design)?" % (who, name), R.choice(cons), crit + ["It must work well."],
                "Constraints are limits such as cost, materials, time, size or effects on the environment.")


def g_matrix():
    crit = R.sample(["cost", "strength", "weight", "ease of building", "safety", "durability"], 3)
    designs = ["Design A", "Design B", "Design C"]
    while True:
        sc = [[R.randint(1, 5) for _ in crit] for _ in designs]
        tot = [sum(r) for r in sc]
        if len(set(tot)) == 3:
            break
    rows = [[d] + ["%d" % v for v in r] + ["%d" % t] for d, r, t in zip(designs, sc, tot)]
    tab = table(["Design"] + [c.capitalize() for c in crit] + ["Total"], rows)
    who = P.next()[0]
    k = R.choice(["best", "crit", "total"])
    if k == "best":
        a = designs[tot.index(max(tot))]
        return item(tab + "%s's team scored three designs from 1 (poor) to 5 (great). Which design best meets the criteria overall?" % who, a,
                    [d for d in designs if d != a] + ["They all score the same."], "%s has the highest total (%d)." % (a, max(tot)))
    if k == "crit":
        j = R.randrange(3)
        col = [r[j] for r in sc]
        if col.count(max(col)) > 1:
            return None
        a = designs[col.index(max(col))]
        return item(tab + "In %s's decision matrix, which design scored best for %s?" % (who, crit[j]), a, [d for d in designs if d != a] + ["the design with the highest total"],
                    "%s scored %d for %s." % (a, max(col), crit[j]))
    i = R.randrange(3)
    return item(tab + "Check %s's decision matrix. What is %s's total score?" % (who, designs[i]), "%d" % tot[i],
                ["%d" % (tot[i] + 1), "%d" % max(sc[i]), "%d" % (tot[i] - 1)], "%s." % " + ".join(str(v) for v in sc[i]) + " = %d" % tot[i])


def g_combine():
    feats = [("Bridge A held the most weight", "triangle supports"), ("Bridge B was the lightest", "thin, hollow straws"),
             ("Filter A was the fastest", "a wide funnel"), ("Filter B made the clearest water", "a layer of sand and charcoal"),
             ("Egg protector A landed closest to the target", "a small parachute"), ("Egg protector B kept the egg safe", "a cushion of cotton balls")]
    i = R.choice([0, 2, 4])
    (a, fa), (b, fb) = feats[i], feats[i + 1]
    who = P.next()[0]
    return item("%s's class tested two designs. %s because it had %s. %s because it had %s. What should the next design do?" % (who, a, fa, b, fb),
                "Combine %s with %s." % (fa, fb), ["Use only the first design and ignore the second.", "Start over with a new idea and no testing.", "Pick the one that looks nicest."],
                "Engineers combine the best features of different solutions.")


def g_iter():
    steps = ["Define the problem", "Brainstorm solutions", "Build a prototype", "Test it", "Improve it and test again"]
    i = R.randrange(4)
    who = P.next()[0]
    return item("%s's team just finished: “%s.” What is the next step in the design process?" % (who, steps[i]), steps[i + 1],
                [x for x in steps if x not in (steps[i], steps[i + 1])][:3], "Design is a cycle: define, brainstorm, build, test, improve, and test again.")


B1 = bank([
    ("What is a criterion in engineering?", "a requirement a solution must meet to be successful", ["a limit on time or money", "the final product", "a guess about what will happen"],
     "Criteria are goals; constraints are limits."),
    ("What is a constraint?", "a limit on a design, such as cost, time, materials or size", ["a goal the design must reach", "a test result", "a type of material"], "Constraints narrow the possible solutions."),
    ("Why should criteria be precise, like “hold 2 kg” instead of “be strong”?", "Precise criteria can be measured to see if a design succeeds.", ["Precise criteria are shorter.", "It does not matter.", "Vague criteria are always better."],
     "You can test a measurable criterion."),
    ("What is a prototype?", "an early model of a design used for testing", ["the final product sold in stores", "a drawing of the problem", "a list of constraints"], "Prototypes are tested and improved."),
    ("Why do engineers test a design many times?", "to find problems and improve it", ["to waste materials", "because the first test is always right", "to change the criteria"], "Iterative testing improves designs."),
    ("What is a decision matrix used for?", "to compare solutions using the criteria in a fair, organized way", ["to draw the final design", "to measure temperature", "to list materials only"],
     "Scores make the comparison clear."),
    ("Why might a design need to consider effects on the environment?", "Solutions can cause new problems for people and nature.", ["The environment never matters.", "It makes the design cheaper always.", "Only to make it look good."],
     "Good designs limit harmful effects."),
    ("In a fair test of two designs, what should stay the same?", "the testing conditions, like the drop height or the amount of water", ["nothing", "only the color", "the design being tested"],
     "Only the design should differ."),
])
B5 = bank([
    ("Ava's bridge holds 3 kg but uses 150 sticks. The constraint is 100 sticks. What should she do?", "redesign it to use 100 or fewer sticks and test again", ["keep it, since it is strong", "ignore the constraint", "change the constraint to 150 sticks"],
     "A design must meet the constraints."),
    ("Leo's water filter works but is too slow. Which change should he test?", "a wider funnel, while keeping the filter layers the same", ["change the funnel and all layers at once", "use dirtier water", "stop testing"],
     "Change one thing at a time."),
    ("Mia's egg protector failed. Why is this useful?", "The failure shows what needs to be improved.", ["Failures are never useful.", "It means the egg was bad.", "It ends the design process."],
     "Engineers learn from failures."),
    ("Two teams build phone stands. Team A's is cheaper; Team B's is sturdier. The criterion is “must not tip over.” What should the class do first?", "test both stands for tipping", ["choose Team A because it is cheaper", "choose by vote without testing", "build a third stand without looking"],
     "Use data from tests to judge criteria."),
    ("Why do engineers make a model before building the real product?", "Models are cheaper and faster to test and change.", ["Models are always better than the real thing.", "Models never need testing.", "Models are required by law."],
     "Testing models saves time and money."),
])


def body():
    think = ("<p>Engineers solve problems with a <b>design process</b>:</p><ol><li>Define the problem with precise <b>criteria</b> (what it must do) and <b>constraints</b> (limits like cost, time, materials and environmental impact).</li>"
             "<li>Brainstorm several solutions.</li><li>Compare solutions with a <b>decision matrix</b> that scores each one against the criteria.</li>"
             "<li>Build a <b>prototype</b> or model and <b>test</b> it.</li><li>Analyze the data, combine the best features and <b>improve</b> the design. Test again.</li></ol>"
             "<p>In every test, change only one thing so the results are fair.</p>")
    ex = [("“It must cost less than $10.” Criterion or constraint?", ["It is a limit."], "constraint"),
          ("Design A scores 4, 3, 5; Design B scores 5, 4, 2. Which total is higher?", ["A: 4 + 3 + 5 = 12", "B: 5 + 4 + 2 = 11"], "Design A")]
    mist = ["Mixing up criteria (goals) and constraints (limits).",
            "Stopping after the first test.",
            "Changing several things at once in one test."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Criteria and constraints", B1 + [(g_cc, 12)]),
        ("Defining design problems", [(g_cc, 12), (g_iter, 8)]),
        ("Decision matrices", [(g_matrix, 16), (g_cc, 4)]),
        ("Testing and improving", [(g_combine, 10), (g_iter, 6), (g_matrix, 4)]),
        ("Engineering challenges", B5 + [g_matrix, g_combine, g_cc, g_iter]),
    ])
    make("grade-6", "engineering-design-process", 12, "MS-ETS1-1",
         "Define the criteria and constraints of a design problem with sufficient precision to ensure a successful solution, taking into account relevant scientific principles and potential impacts on people and the natural environment that may limit possible solutions.",
         "The Engineering Design Process",
         "Grade 6 Engineering Design Worksheets: Criteria, Constraints, Decision Matrices and Testing",
         "Engineering Design Process",
         "Free middle school science worksheets on the engineering design process (NGSS MS-ETS1-1 to MS-ETS1-4): criteria and constraints, decision matrices, combining the best features and iterative testing. 100 practice questions with answers.",
         "Define, compare, test and improve.",
         "Precise criteria and constraints, a decision matrix and repeated testing help engineers find the best solution.",
         body(),
         [("What is the difference between criteria and constraints?", "Criteria are what a design must do to succeed. Constraints are limits such as cost, time, materials and size."),
          ("What is a decision matrix?", "A table that scores each possible solution against the criteria so they can be compared fairly."),
          ("Why do engineers test and improve designs many times?", "Each test gives data that shows what to fix. Combining the best features and testing again makes the design better.")],
         sets)


if __name__ == "__main__":
    main()
