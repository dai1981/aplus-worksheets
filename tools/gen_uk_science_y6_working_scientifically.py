# -*- coding: utf-8 -*-
"""
UK Year 6 science: Working Scientifically
  python tools/gen_uk_science_y6_working_scientifically.py
Upper key stage 2 enquiry skills: variables (change, measure, keep the same), fair tests, repeat readings,
anomalous results and means, choosing a bar chart, line graph or scatter graph, predicting from results,
and drawing conclusions supported by evidence.
Wrong answers come from real mistakes: "changing two things at once", "including an anomalous result in the mean",
"using a line graph for categories", "a conclusion that goes beyond the results".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61616)
R = U.R
P = People(R)

EXP = [("Does the height of a ramp affect how far a toy car rolls?", "the height of the ramp", "how far the car rolls", "the same car, the same surface and letting go without pushing"),
       ("Does the temperature of water affect how fast sugar dissolves?", "the temperature of the water", "the time for the sugar to dissolve", "the same amount of sugar and water, and stirring the same way"),
       ("Does the length of a paper helicopter's wings affect how long it takes to fall?", "the length of the wings", "the time taken to fall", "the same paper, the same drop height and the same paperclip"),
       ("Does the number of cells affect how bright a lamp is?", "the number of cells", "the brightness of the lamp", "the same lamp and the same wires"),
       ("Does the type of surface affect how much force is needed to pull a shoe?", "the type of surface", "the force needed to pull the shoe", "the same shoe and the same newton meter"),
       ("Does the amount of light affect how tall a bean plant grows?", "the amount of light", "the height of the plant after two weeks", "the same type of seed, soil and amount of water"),
       ("Does the thickness of a wrapping affect how fast a cup of water cools?", "the thickness of the wrapping", "the temperature after 20 minutes", "the same cup, the same starting temperature and the same volume of water"),
       ("Does the size of a parachute affect how slowly it falls?", "the size of the parachute", "the time taken to fall", "the same load, the same string and the same drop height"),
       ("Does the height a ball is dropped from affect how high it bounces?", "the drop height", "the bounce height", "the same ball and the same floor"),
       ("Does the type of soil affect how much water drains through it?", "the type of soil", "the volume of water that drains through in 5 minutes", "the same amount of soil, the same amount of water and the same funnel")]


def g_var():
    q, ch, me, same = R.choice(EXP)
    k = R.choice(["change", "measure", "same"])
    if not once(("va", q, k)):
        return None
    if k == "change":
        return item("Investigation: \"%s\" Which variable should be changed?" % q, ch, [me, same, "everything at once"], "Change one variable: the one in the question.")
    if k == "measure":
        return item("Investigation: \"%s\" What should be measured?" % q, me, [ch, same, "nothing, just watch"], "Measure the result (the dependent variable).")
    return item("Investigation: \"%s\" What should be kept the same to make it a fair test?" % q, same, [ch, me, "the person's opinion"], "Control variables keep the test fair.")


def g_anom():
    who = P.next()[0]
    base = R.choice([12, 15, 18, 20, 24, 30, 36])
    good = [base + d for d in R.sample([-1, 0, 1, 2], 3)]
    bad = base + R.choice([-9, -8, 9, 10, 12])
    if bad <= 0:
        return None
    rows = good + [bad]
    R.shuffle(rows)
    k = R.choice(["which", "mean"])
    what = R.choice([("time for sugar to dissolve", "s"), ("distance a car rolled", "cm"), ("time for ice to melt", "min"), ("height of a bounce", "cm")])
    if not once(("an", tuple(rows), k)):
        return None
    tab = table(["Test", "Result (%s)" % what[1]], [[str(i + 1), str(v)] for i, v in enumerate(rows)])
    intro = tab + "%s measured the %s four times. " % (who, what[0])
    if k == "which":
        a = "%d %s" % (bad, what[1])
        return item(intro + "Which result is anomalous (does not fit the pattern)?", a, ["%d %s" % (v, what[1]) for v in good], "It is far from the other results.")
    s = sum(good)
    if s % 3:
        return None
    m = s // 3
    g = "%d %s" % (m, what[1])
    return item(intro + "Leave out the anomalous result. What is the mean of the other three?", g,
                uniq(g, ["%s %s" % (num(sum(rows) / 4, 2), what[1]), "%d %s" % (s, what[1]), "%d %s" % (max(good), what[1]), "%d %s" % (m + 2, what[1])]), "%d ÷ 3 = %d." % (s, m))


GR = [("the favourite fruit of pupils in a class", "a bar chart"), ("the number of birds of each kind seen in a garden", "a bar chart"),
      ("which material kept a drink warmest", "a bar chart"), ("the temperature of a cup of tea every 2 minutes as it cools", "a line graph"),
      ("the height of a sunflower measured every week", "a line graph"), ("how the length of a shadow changes during the day", "a line graph"),
      ("the arm span and height of every pupil in a class", "a scatter graph"), ("the foot length and hand span of 30 people", "a scatter graph"),
      ("the mass and length of 20 different fish", "a scatter graph")]


def g_graph():
    d, a = R.choice(GR)
    if not once(("gr", d)):
        return None
    return item("Which type of graph is best for showing %s?" % d, a, [x for x in ["a bar chart", "a line graph", "a scatter graph"] if x != a] + ["a classification key"],
                "Bar chart: separate groups. Line graph: change over time or a continuous measurement. Scatter graph: a link between two measurements.")


def g_pred():
    who = P.next()[0]
    xs = [10, 20, 30, 40, 50]
    a0 = R.choice([20, 30, 40, 50])
    st = R.choice([10, 15, 20, 25])
    ys = [a0 + st * i for i in range(5)]
    k = R.choice(["mid", "next"])
    if not once(("pr", a0, st, k)):
        return None
    tab = table(["Ramp height (cm)", "Distance rolled (cm)"], [[str(x), str(y)] for x, y in zip(xs, ys)])
    intro = tab + "%s rolled a car down a ramp at different heights. " % who
    if k == "mid":
        g = "%d cm" % ((ys[1] + ys[2]) // 2)
        if (ys[1] + ys[2]) % 2:
            return None
        return item(intro + "Predict how far it would roll from a 25 cm high ramp.", g, uniq(g, ["%d cm" % ys[1], "%d cm" % ys[2], "%d cm" % (ys[2] + st), "25 cm"]),
                    "25 cm is halfway between 20 and 30 cm, so the distance is halfway between %d and %d." % (ys[1], ys[2]))
    g = "%d cm" % (ys[4] + st)
    return item(intro + "If the pattern continues, how far would it roll from a 60 cm high ramp?", g, uniq(g, ["%d cm" % ys[4], "%d cm" % (ys[4] + 10), "%d cm" % (ys[4] * 2), "60 cm"]),
                "Each 10 cm higher adds %d cm." % st)


CONC = [(["Plastic cup", "Paper cup", "Metal cup"], [55, 48, 38], "temperature after 10 minutes (°C)", "The plastic cup kept the water warmest.",
         ["The metal cup kept the water warmest.", "All cups are the same.", "Plastic cups are best for every drink."]),
        (["Carpet", "Wood", "Tiles"], [40, 85, 120], "distance a ball rolled (cm)", "The ball rolled furthest on tiles.",
         ["The ball rolled furthest on carpet.", "Carpet has the least friction.", "All surfaces are the same."]),
        (["Cotton", "Wool", "Foil"], [12, 25, 6], "time for ice to melt (min)", "Ice took longest to melt when wrapped in wool.",
         ["Foil kept the ice frozen longest.", "Wool makes ice melt fastest.", "Cotton is the best insulator."]),
        (["Small", "Medium", "Large"], [2, 4, 6], "time to fall (s)", "Larger parachutes took longer to fall.",
         ["Smaller parachutes took longer to fall.", "Size makes no difference.", "All parachutes fall in 4 seconds."])]


def g_conc():
    who = P.next()[0]
    i = R.randrange(len(CONC))
    labs, vals, head, a, w = CONC[i]
    if not once(("cc", i), 3) or not once(("ccw", i, who)):
        return None
    tab = table(["", head], [[x, str(v)] for x, v in zip(labs, vals)])
    return item(tab + "Which conclusion is supported by %s's results?" % who, a, w, "A conclusion must match the results and not go beyond them.")


B1 = bank([
    ("What is a fair test?", "a test where only one variable is changed and the others are kept the same", ["a test that everyone likes", "a test done only once", "a test where everything changes"], "Change one thing."),
    ("Why do scientists repeat measurements?", "to check results and make them more reliable", ["to use up time", "to change the answer", "because the first result is always wrong"], "Repeats show if results agree."),
    ("What is an anomalous result?", "a result that does not fit the pattern of the others", ["the biggest result", "the first result", "the average result"], "Check it or repeat it."),
    ("What should you do with an anomalous result?", "repeat the test or leave it out of the mean", ["always include it", "change the other results", "make up a new number"], "It may be a mistake."),
    ("Which equipment measures force?", "a newton meter", ["a thermometer", "a stopwatch", "a ruler"], "Force is measured in newtons."),
    ("Which equipment measures time accurately?", "a stopwatch", ["a ruler", "a newton meter", "a measuring jug"], "Time in seconds."),
    ("What is a prediction?", "what you think will happen, with a reason", ["what did happen", "a measurement", "a type of graph"], "Made before the test."),
    ("What is a conclusion?", "what the results show, answering the question", ["a guess before the test", "the list of equipment", "a drawing of the test"], "Based on evidence."),
])
B5 = bank([
    ("Two pupils get different results for the same test. What should they do?", "repeat the test carefully and compare", ["choose the result they like", "give up", "change the question"], "More evidence."),
    ("A pupil measures to the nearest millimetre instead of the nearest centimetre. What is improved?", "the precision of the measurement", ["the safety", "the number of variables", "the conclusion"], "Smaller units, more precise."),
    ("Why is 'Does exercise make you healthier?' hard to test in class?", "Healthy is hard to measure; a measurable question is better.", ["It is too easy.", "Exercise cannot be done in school.", "It has only one variable."], "Make questions testable."),
    ("Which result would refute the idea that heavier objects always fall faster?", "a heavy ball and a light ball dropped together landing at the same time", ["a feather falling slowly", "a heavy ball falling", "a light ball bouncing"], "Evidence can disprove ideas."),
    ("Why should results be recorded in a table straight away?", "so nothing is forgotten or mixed up", ["to make the test fair", "because tables are pretty", "to change results later"], "Accurate records."),
])


def body():
    think = ("<p><b>Plan a fair test, measure carefully, then let the results answer the question.</b></p>"
             "<ul><li>Change one variable, measure one variable, keep everything else the same.</li>"
             "<li>Repeat readings; spot anomalous results; find the mean of the good ones.</li>"
             "<li>Bar chart for groups, line graph for change over time, scatter graph for a link between two measurements. Conclusions must match the evidence.</li></ul>")
    ex = [("Results 14, 15, 26, 16. Anomaly and mean?", ["26 does not fit", "(14 + 15 + 16) ÷ 3"], "26 is anomalous; mean = 15"),
          ("Plant height every week: which graph?", ["Change over time"], "a line graph")]
    mist = ["Changing two variables at once.", "Including an anomalous result in the mean.", "Using a line graph for separate groups."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fair tests", B1 + [(g_var, 12)]),
        ("Variables", [(g_var, 12), (g_graph, 8)]),
        ("Repeat readings", [(g_anom, 20)]),
        ("Graphs and predictions", [(g_pred, 14), (g_conc, 6)]),
        ("Conclusions", B5 + [(g_conc, 5), (g_anom, 7), (g_pred, 3)]),
    ])
    make_uk(6, "working-scientifically", 16, "Working scientifically",
            "Plan different types of scientific enquiries to answer questions, including recognising and controlling variables where necessary; take measurements with increasing accuracy and precision, taking repeat readings when appropriate; "
            "record data and results using tables, bar and line graphs and scatter graphs; use test results to make predictions; report and present findings, including conclusions; identify scientific evidence that has been used to support or refute ideas.",
            "Working Scientifically",
            "Year 6 Science: Working Scientifically Worksheets (Fair Tests, Variables, Graphs)",
            "Working Scientifically",
            "Free Year 6 science worksheets on working scientifically: fair tests, variables, repeat readings, anomalous results, choosing graphs, predictions and conclusions. 100 questions with answers.",
            "Change one thing, measure one thing.",
            "Keep the rest the same, repeat readings, and let the evidence decide.",
            body(),
            [("What are the three kinds of variable?", "The variable you change, the variable you measure, and the variables you keep the same (control variables) to make the test fair."),
             ("Why repeat readings?", "Repeats show whether results agree. They help you spot anomalous results and give a more reliable mean."),
             ("Which graph should I use?", "A bar chart for separate groups, a line graph for something that changes over time or along a scale, and a scatter graph to see if two measurements are linked.")],
            sets)


if __name__ == "__main__":
    main()
