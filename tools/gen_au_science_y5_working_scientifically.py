# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, Science inquiry (AC9S5I01-I06): questioning and predicting, planning fair tests,
measuring and recording, finding patterns, evaluating and communicating.
  python tools/gen_au_science_y5_working_scientifically.py
Reuses the UK Year 5-6 working scientifically makers (variables, predictions, anomalies, graphs) with Australian names,
plus own questions on testable questions, reading equipment and averaging repeated results.
Wrong answers come from real mistakes: changing more than one variable, choosing a bar graph for data over time,
leaving out an anomalous result without checking it, and confusing an observation with a conclusion.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 5, 8
U, R, P, src = AU(seed_of(YEAR, SORT))

W5 = "gen_uk_science_y5_working_scientifically"
W6 = "gen_uk_science_y6_working_scientifically"
uk5_b1 = src.B(W5, "B1")
uk5_b5 = src.B(W5, "B5")
uk6_b1 = src.B(W6, "B1")
uk6_b5 = src.B(W6, "B5")
uk_var = src(W6, "g_var")
uk_pred = limit(src(W6, "g_pred"), 8)
uk_anom = limit(src(W6, "g_anom"), 5)
uk_conc = src(W6, "g_conc")
uk_graph = src(W6, "g_graph")

MEAN = [("the time for a paper helicopter to fall from 3 m", "s", 3, 6, 1), ("the distance a toy car rolled off a ramp", "cm", 60, 150, 6),
        ("the height a tennis ball bounced", "cm", 40, 90, 3), ("the time for an ice cube to melt in the sun", "min", 15, 40, 2),
        ("the temperature of water in a shaded bottle at 3 pm", "°C", 22, 32, 1), ("the number of seeds that sprouted in each tray", "seeds", 12, 20, 2),
        ("the time for sugar to dissolve in warm water", "s", 30, 90, 4), ("the length of a bean plant after two weeks", "cm", 8, 20, 1)]


def g_mean():
    what, u, lo, hi, dd = R.choice(MEAN)
    from au_sci import once
    if not once(("mean", what)):
        return None
    m = R.randint(lo, hi)
    d = R.randint(1, dd)
    xs = [m - d, m, m + d]
    R.shuffle(xs)
    sp = " "
    f = lambda v: "%d%s%s" % (v, sp, u)
    return tq("A group measured %s three times: %s. What is the average?" % (what, ", ".join(f(x) for x in xs)), f(m),
              [f(sum(xs)), f(max(xs)), f(m + 2 * d + 1)], "Add the results and divide by 3: %d ÷ 3 = %d." % (sum(xs), m))


EQ = [("the temperature of water", "a thermometer", "°C"), ("the mass of a rock", "electronic scales", "g"),
      ("the volume of water in a cup", "a measuring cylinder", "mL"), ("the time for a marble to roll down a ramp", "a stopwatch", "s"),
      ("the length of a leaf", "a ruler", "mm"), ("the width of the school oval", "a trundle wheel or long tape measure", "m"),
      ("the force needed to pull a shoe across the floor", "a spring balance (force meter)", "N"), ("how bright a torch is", "a light meter", "lux")]


def g_eq():
    what, tool, u = R.choice(EQ)
    if R.random() < 0.5:
        w = sorted({x[1] for x in EQ if x[1] != tool})
        return tq("Which equipment would you use to measure %s?" % what, tool, R.sample(w, 3), "Use %s; it measures in %s." % (tool, u))
    w = sorted({x[2] for x in EQ if x[2] != u})
    return tq("Which unit would you use to record %s?" % what, u, R.sample(w, 3), "%s measures it in %s." % (tool[0].upper() + tool[1:], u))


QS = [("Does the height of a ramp change how far a toy car rolls?", True), ("Which colour is the nicest for a bedroom wall?", False),
      ("Does the amount of sunlight change how tall bean plants grow?", True), ("Why are koalas cute?", False),
      ("Does salt water freeze faster than tap water?", True), ("What is the best footy team?", False),
      ("Does the length of a pendulum change how long each swing takes?", True), ("Do people like the smell of eucalyptus?", False),
      ("Does the temperature of water change how fast sugar dissolves?", True), ("Is science more fun than art?", False),
      ("Does the type of surface change how far a ball rolls?", True), ("Which day of the week is the best?", False)]


def g_test():
    t = [q for q, ok in QS if ok]
    f = [q for q, ok in QS if not ok]
    if R.random() < 0.5:
        a = R.choice(t)
        return tq("Which of these questions can be answered by a fair test?", a, R.sample(f, 3),
                  "A testable question changes one thing and measures another.")
    a = R.choice(f)
    return tq("Which of these questions CANNOT be answered by a scientific test?", a, R.sample(t, 3), "Opinions cannot be measured with a fair test.")


POOL1 = pool(R, [
    ("What is a prediction?", "what you think will happen, based on what you already know", ["the result you measured", "a list of equipment", "the title of the test"], "Make a prediction before the test."),
    ("Mia predicts a ball will bounce higher on concrete than on grass. Which reason fits a good prediction?", "Grass is soft and takes in some of the ball's energy.", ["I like concrete.", "Grass is green.", "Balls are round."], "A prediction should give a reason."),
    ("Which is an observation, not a conclusion?", "The ice in the foil cup melted after 20 minutes.", ["Foil is the best insulator.", "Ice always melts fastest in foil.", "Foil keeps everything cold."], "An observation is what you saw or measured."),
    ("Why do scientists repeat a test several times?", "to check the results are reliable", ["to make the test longer", "to change the variable", "because the first result is always wrong"], "Repeated results that agree are more trustworthy."),
    ("Which is the safest way to heat water in a classroom test?", "with an adult, using a kettle and heat-proof gloves", ["on your own with a candle", "holding a glass over a flame", "in a microwave in a closed metal tin"], "Plan safety before you start."),
    ("Why should you record results in a table?", "to keep the results organised and easy to compare", ["to make the test fair", "so you do not need to measure", "to change the results"], "Tables have headings and units."),
    ("A table has the heading 'Time'. What is missing?", "the unit, such as (s) or (min)", ["the title of the school", "the date", "nothing"], "Always write units in table headings."),
    ("Which graph is best for comparing the number of birds of each kind seen in a park?", "a column graph", ["a line graph", "no graph", "a map"], "Use a column graph for separate categories."),
])
POOL5 = pool(R, [
    ("Jack tests paper planes with different wing sizes. He also changes the paper type each time. What is wrong?", "He changed two variables, so he cannot tell which one caused the result.", ["Nothing is wrong.", "He should change more variables.", "Paper planes cannot be tested."], "Change only one variable."),
    ("Ruby's results: ramp 10 cm, car rolls 40 cm; 20 cm, 80 cm; 30 cm, 120 cm. Predict the distance for a 40 cm ramp.", "160 cm", ["40 cm", "120 cm", "200 cm"], "Each 10 cm of height adds 40 cm of distance."),
    ("Kai finds one result much bigger than the others. What should he do?", "Repeat that test to check it.", ["Delete all the results.", "Ignore the other results.", "Change his prediction to match."], "An anomalous result should be checked."),
    ("Ella's results do not match her prediction. What should she do?", "Report the results honestly and explain what she found.", ["Change the results to match.", "Throw the results away.", "Pretend she did not make a prediction."], "Results that surprise us help us learn."),
    ("Which change would make Mia's plant test fairer?", "giving every plant the same amount of water", ["using a different pot for each plant", "putting some plants inside and some outside", "testing only one plant"], "Keep everything the same except the variable you test."),
    ("Which is the best way to share the results of a test with the class?", "a clear table and graph with a short conclusion", ["only saying 'it worked'", "showing only the best result", "drawing a picture of the equipment only"], "Communicate results so others can check them."),
    ("Noah measures how long a candle burns under jars of different sizes. Why should an adult light the candles?", "to keep everyone safe from burns", ["to make the candles burn longer", "to change the variable", "because children cannot count"], "Safety is part of planning."),
    ("Which conclusion matches the data: 'the bigger the jar, the longer the candle burned'?", "Bigger jars hold more air, so the candle could burn longer.", ["Candles do not need air.", "Small jars make candles burn longer.", "The jars were the same size."], "A conclusion explains the pattern."),
])


def main():
    sets = U.sets([
        ("Questions and predictions", [(g_test, 6), (POOL1, 5), (uk_pred, 4), (uk6_b1, 3), (uk5_b1, 2)]),
        ("Variables and fair tests", [(uk_var, 12), (uk5_b1, 4), (g_test, 2), (POOL1, 2)]),
        ("Measuring and recording", [(g_eq, 10), (uk_graph, 6), (uk6_b5, 2), (POOL1, 1), (uk6_b1, 1)]),
        ("Patterns and anomalies", [(g_mean, 6), (uk_anom, 5), (uk_conc, 3), (uk_pred, 4), (uk_graph, 2)]),
        ("Evaluating and communicating", [(POOL5, 8), (uk5_b5, 4), (uk6_b5, 2), (uk_var, 4), (g_mean, 2)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S5I01, AC9S5I02, AC9S5I03, AC9S5I04, AC9S5I05, AC9S5I06", "Science inquiry",
            "Pose questions and make predictions; plan and conduct fair tests, identifying variables and safety; use equipment to measure "
            "and record data in tables and graphs; identify patterns; evaluate methods; and communicate findings "
            "(summary of the Australian Curriculum v9.0 Year 5 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 5 science worksheets on working scientifically: testable questions, predictions, fair tests and variables, "
            "measuring, averages, graphs, anomalies and conclusions. 100 questions with answers.",
            "Change one thing, measure one thing.", "A fair test changes one variable, measures one and keeps the rest the same.",
            "<p><b>Scientists ask questions they can test, then plan a fair test.</b></p><ul>"
            "<li>Change one variable, measure one variable, and keep everything else the same.</li>"
            "<li>Measure with the right equipment and units, repeat the test, and record the results in a table.</li>"
            "<li>Look for a pattern, check results that do not fit, and write a conclusion that matches the data.</li></ul>",
            [("Does ramp height change how far a car rolls? What do you change?", ["the question names the ramp height"], "the height of the ramp"),
             ("Results: 24 s, 26 s, 25 s. Average?", ["24 + 26 + 25 = 75", "75 ÷ 3 = 25"], "25 s")],
            ["Changing more than one variable at a time.", "Using a column graph for data that changes over time (use a line graph).",
             "Leaving out a result that does not fit without testing it again."],
            [("What is a fair test?", "A fair test changes only one variable, measures one variable and keeps all the other variables the same, so you know what caused the result."),
             ("Why repeat a test?", "Repeating a test shows whether the results are reliable. If one result is very different, test again to check it."),
             ("Which graph should I use?", "Use a column graph to compare separate groups, such as kinds of birds. Use a line graph when something changes over time or when both variables are numbers.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
