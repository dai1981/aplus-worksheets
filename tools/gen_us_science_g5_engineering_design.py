# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Engineering Design (3-5-ETS1-1, 3-5-ETS1-2, 3-5-ETS1-3)
  python tools/gen_us_science_g5_engineering_design.py
Define a problem with criteria (what success looks like) and constraints (limits on materials,
time or cost); compare possible solutions against them; plan fair tests that change one variable,
repeat trials and find failure points to improve a prototype.
Questions use design tables and test data (paper bridges, foil boats, egg drops, insulated cups).
Wrong answers come from real mistakes: mixing up criteria and constraints, choosing the design that is
best at one thing but breaks a constraint, changing two variables at once, trusting one trial.
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(50117)
R = U.R
P = People(R)

TASKS = [
    ("a bridge made of paper that crosses a 30 cm gap", ["It must hold at least 20 pennies.", "It must span the whole 30 cm gap."], ["Each team may use only 5 sheets of paper.", "Teams have 20 minutes to build it.", "Tape is limited to 50 cm."]),
    ("a foil boat that floats", ["The boat must hold at least 50 marbles.", "The boat must stay afloat for 1 minute."], ["Each team gets one 30 cm square of foil.", "No tape or glue may be used.", "Teams have 15 minutes."]),
    ("a container that keeps an egg from breaking when dropped", ["The egg must not crack when dropped from 3 meters.", "The egg must be easy to take out."], ["The materials may cost no more than $5.", "The container must weigh less than 200 g.", "Teams have one class period."]),
    ("a cup that keeps hot water warm", ["The water must stay above 50 °C for 20 minutes.", "The cup must not leak."], ["Only materials from the recycling bin may be used.", "The cup must fit in one hand.", "Teams have 30 minutes to build it."]),
    ("a solar oven that melts chocolate", ["The chocolate must melt within 30 minutes.", "The oven must stand up on its own."], ["It must be made from one pizza box.", "Teams may use only 1 meter of foil.", "Building time is 45 minutes."]),
    ("a water filter that cleans muddy water", ["The water that comes out must look clear.", "It must filter 200 mL of water."], ["Materials may cost no more than $3.", "Only sand, gravel, cotton and coffee filters may be used.", "Teams have 2 days."]),
]


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ makers
def g_crit():
    task, cr, co = R.choice(TASKS)
    if R.random() < 0.5:
        a = R.choice(cr)
        return item("A class is designing %s. Which statement is a <b>criterion</b> (a goal the design must meet)?" % task, a, R.sample(co, 3),
                    "Criteria describe what a successful design must do. The others are constraints: limits on materials, time or cost.")
    a = R.choice(co)
    w = list(cr) + [R.choice([c for t, cc, oo in TASKS if t != task for c in cc])]
    return item("A class is designing %s. Which statement is a <b>constraint</b> (a limit)?" % task, a, w[:3],
                "Constraints limit the materials, time or cost. The others are criteria for success.")


def g_compare():
    budget = R.choice([5, 6, 8, 10])
    need = R.choice([20, 25, 30, 40])
    names = ["Design A", "Design B", "Design C", "Design D"]
    rows = []
    good = R.randrange(4)
    data = []
    for i in range(4):
        if i == good:
            cost, held = R.randint(budget - 3, budget), need + R.randint(2, 15)
        else:
            kind = R.choice(["cost", "held"])
            if kind == "cost":
                cost, held = budget + R.randint(1, 4), need + R.randint(10, 40)
            else:
                cost, held = R.randint(2, budget), need - R.randint(3, 12)
        data.append((cost, held))
        rows.append([names[i], "$%d" % cost, str(held)])
    if sum(1 for c, h in data if c <= budget and h >= need) != 1:
        return None
    top = max(range(4), key=lambda i: data[i][1])
    p = P.next()
    return item(table(["Design", "Cost", "Pennies held"], rows)
                + "%s's bridge must hold at least %d pennies and cost no more than $%d. Which design meets both?" % (p[0], need, budget),
                names[good], [n for i, n in enumerate(names) if i != good],
                "%s costs $%d and holds %d pennies. %s" % (names[good], data[good][0], data[good][1],
                                                          ("%s holds the most, but it costs too much." % names[top]) if top != good and data[top][0] > budget else "The others fail a criterion or a constraint."))


def g_avg():
    vals = [R.randint(10, 40) for _ in range(3)]
    while sum(vals) % 3:
        vals[2] += 1
    p = P.next()
    k = R.choice(["marbles held by a foil boat", "pennies held by a paper bridge", "seconds an ice cube lasted in a cooler", "centimeters a paper airplane flew"])
    return item(table(["Trial 1", "Trial 2", "Trial 3"], [[str(v) for v in vals]]) + "%s tested the same design 3 times and recorded the %s. What is the mean (average)?" % (p[0], k),
                str(sum(vals) // 3), [str(sum(vals)), str(max(vals)), str(min(vals))], "(%d + %d + %d) ÷ 3 = %d." % (vals[0], vals[1], vals[2], sum(vals) // 3))


def g_variable():
    tests = [("whether the length of a paper airplane's wings changes how far it flies", "wing length", ["the kind of paper", "how hard it is thrown", "where it is thrown"]),
             ("whether the shape of a foil boat changes how many marbles it holds", "boat shape", ["the size of the foil sheet", "the kind of marbles", "the water in the tub"]),
             ("whether the material wrapped around a cup keeps water warm longer", "wrapping material", ["the starting water temperature", "the amount of water", "the size of the cup"]),
             ("whether the height of a ramp changes how far a toy car rolls", "ramp height", ["the car", "the ramp surface", "how the car is released"]),
             ("whether the number of layers of sand in a filter makes water clearer", "number of sand layers", ["the kind of muddy water", "the amount of water poured", "the size of the bottle"]),
             ("whether parachute size changes how slowly a toy falls", "parachute size", ["the toy's weight", "the drop height", "the parachute material"])]
    t, var, keep = R.choice(tests)
    p = P.next()
    if R.random() < 0.5:
        return item("%s tests %s. Which variable should %s change?" % (p[0], t, p[1]), var, keep, "Change only the %s. Keep everything else the same." % var)
    k = R.choice(keep)
    return item("%s tests %s. Which should %s keep the same in every trial?" % (p[0], t, p[1]), k, [var, "the results", "nothing needs to stay the same"],
                "To be fair, only the %s changes. %s stays the same." % (var, cap(k)))


def g_failure():
    f = [("A paper bridge sags and tears in the middle.", "Add supports or fold the paper to make the middle stronger."),
         ("A foil boat tips over when marbles are piled on one side.", "Spread the marbles out or make the boat wider."),
         ("The egg cracks when the container lands on one corner.", "Add more padding on all sides, especially the corners."),
         ("Hot water cools fastest at the open top of the cup.", "Add a lid made of an insulating material."),
         ("Muddy water runs straight through a gap at the side of the filter.", "Seal the edges so all the water passes through the layers."),
         ("A model car's wheels wobble and rub on the body.", "Make the axle holes straight and add spacers.")]
    prob, fix = R.choice(f)
    w = [x for p_, x in f if x != fix]
    return item("During testing: %s Which improvement best fixes this failure point?" % prob, fix, R.sample(w, 3), "The improvement targets the exact part that failed.")


B1 = bank([
    ("What is a criterion in engineering?", "something the design must do to be successful", ["a limit on time or money", "the materials list", "the name of the design"],
     "For example: the bridge must hold 20 pennies."),
    ("What is a constraint in engineering?", "a limit, such as on materials, time or cost", ["the goal of the design", "a test result", "a drawing"],
     "For example: you may use only 5 sheets of paper."),
    ("What is a prototype?", "an early model built to test a design", ["the final product sold in stores", "a drawing only", "a list of criteria"],
     "Engineers test prototypes to find problems before making the final version."),
    ("Why do engineers think of several possible solutions?", "to compare them and choose the one that best meets the criteria and constraints", ["because the first idea is always wrong", "to use more materials", "to make the project take longer"],
     "Comparing options leads to better designs."),
    ("What is a failure point?", "a place where a design breaks or does not work", ["the end of the project", "the most expensive part", "a constraint"],
     "Finding failure points shows what to improve."),
    ("What should engineers do after testing a prototype?", "improve the design and test it again", ["stop working", "change every part at once", "ignore the results"],
     "Design is a cycle: test, improve, test again."),
    ("Which step comes first in the engineering design process?", "define the problem with its criteria and constraints", ["build the final product", "test the design", "sell the product"],
     "You need to know what the design must do and its limits before starting."),
    ("Why are tests repeated several times?", "to make sure the results are reliable", ["to use up materials", "to get a different answer", "because the first test is never counted"],
     "Repeating trials shows whether a result was a fluke."),
])
B5 = bank([
    ("Two water filters both make the water clear. Filter A costs $2 and Filter B costs $6. The budget is $3. Which should the team choose?", "Filter A, because it meets the criterion and the constraint", ["Filter B, because it costs more", "Either one", "Neither, because both make water clear"],
     "Only Filter A fits within the $3 limit."),
    ("Ava changes both the shape and the size of her foil boat between tests. What is the problem?", "She cannot tell which change made the difference.", ["Nothing is wrong.", "The boat will sink.", "She should change three things."],
     "Change one variable at a time."),
    ("A team's egg survives a 1-meter drop but cracks at 2 meters. The criterion is 3 meters. What should they do next?", "Find what failed at 2 meters and improve that part, then test again.", ["Say the design is finished.", "Test only from 1 meter.", "Start a completely different project."],
     "Use the failure point to guide the next improvement."),
    ("Why do engineers draw a design before building it?", "to plan the materials and share ideas with the team", ["because drawings are always the final product", "to skip testing", "to make it cost more"],
     "Sketches help compare ideas and spot problems early."),
    ("A city wants a playground that is safe, fun and finished in 2 months for $50,000. Which is a constraint?", "finished in 2 months for $50,000", ["safe", "fun", "has swings children like"],
     "Time and money limits are constraints."),
    ("Leo's bridge holds 35 pennies, 12 pennies and 34 pennies in three trials. What should he do about the 12?", "Check what went wrong in that trial and test again.", ["Use 12 as the only result.", "Throw away the other results.", "Add the numbers and stop."],
     "An unusual result may come from a mistake, like pennies placed unevenly."),
])


def body():
    rows = [["Design A", "$4", "28"], ["Design B", "$9", "45"], ["Design C", "$5", "15"]]
    think = ("<p>Engineers solve problems step by step:</p>"
             "<ol><li><b>Define the problem.</b> List the <b>criteria</b> (what success looks like) and the <b>constraints</b> (limits on materials, time or cost).</li>"
             "<li><b>Think of several solutions</b> and compare how well each one meets the criteria and constraints.</li>"
             "<li><b>Build a prototype and test it fairly.</b> Change one variable at a time, repeat the trials, and look for <b>failure points</b>.</li>"
             "<li><b>Improve</b> the design and test again.</li></ol>"
             + table(["Design", "Cost", "Pennies held"], rows)
             + "<p>If a bridge must hold at least 20 pennies and cost no more than $5, only Design A works. Design B holds the most but costs too much.</p>")
    ex = [("“The boat must hold 50 marbles” and “use only one sheet of foil.” Which is the criterion?", ["The goal is holding 50 marbles.", "One sheet of foil is a limit."], "holding 50 marbles"),
          ("Trials: 18, 22 and 20 pennies. What is the mean?", ["18 + 22 + 20 = 60", "60 ÷ 3 = 20"], "20 pennies")]
    mist = ["Mixing up criteria (goals) and constraints (limits).",
            "Picking the design that is best at one thing even though it breaks a constraint.",
            "Changing more than one variable in a test.",
            "Trusting a single trial instead of repeating the test."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Criteria and constraints", B1 + [(g_crit, 12)]),
        ("Comparing solutions", [(g_compare, 12), (g_crit, 8)]),
        ("Fair tests", [(g_variable, 12), (g_avg, 8)]),
        ("Failure points and data", [(g_failure, 6), (g_avg, 7), (g_compare, 7)]),
        ("Design challenges", B5 + [g_compare, g_variable, g_failure, g_avg]),
    ])
    make("grade-5", "engineering-design", 17, "3-5-ETS1-1, 3-5-ETS1-2, 3-5-ETS1-3",
         "Define a simple design problem reflecting a need or a want that includes specified criteria for success and constraints on materials, time, or cost. Generate and compare multiple possible solutions to a problem based on how well each is likely to meet the criteria and constraints of the problem. Plan and carry out fair tests in which variables are controlled and failure points are considered to identify aspects of a model or prototype that can be improved.",
         "Engineering Design",
         "Grade 5 Engineering Design Worksheets: Criteria, Constraints, Fair Tests and Prototypes",
         "Engineering Design",
         "Free Grade 5 science worksheets on engineering design (NGSS 3-5-ETS1): criteria and constraints, comparing solutions in tables, fair tests, failure points and improving prototypes. 100 practice questions with answers.",
         "A good design meets every criterion within its constraints.",
         "Criteria are goals; constraints are limits on materials, time or cost. Test fairly, find failure points and improve.",
         body(),
         [("What is the difference between criteria and constraints?", "Criteria are what the design must do to succeed, like holding 20 pennies. Constraints are limits, like using only 5 sheets of paper or spending no more than $5."),
          ("What is a fair test?", "A test where only one variable changes and everything else stays the same, repeated several times."),
          ("What is a failure point?", "A part of a design that breaks or does not work during testing. It shows what to improve."),
          ("What are the steps of the engineering design process?", "Define the problem, think of and compare solutions, build and test a prototype, then improve it and test again.")],
         sets)


if __name__ == "__main__":
    main()
