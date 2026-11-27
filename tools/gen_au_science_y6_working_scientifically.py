# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, Science inquiry (AC9S6I01-I06): independent, dependent and controlled variables,
reading line graphs, finding patterns and anomalies, evaluating methods and communicating findings.
  python tools/gen_au_science_y6_working_scientifically.py
Own investigations (with Australian contexts) for naming the three kinds of variable and own line graphs to read, plus the
UK Year 6 working scientifically makers with Australian names.
Wrong answers come from real mistakes: swapping the independent and dependent variables, reading a graph between the gridlines
wrongly, and writing a conclusion the data does not support.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once

YEAR, SORT = 6, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

W6 = "gen_uk_science_y6_working_scientifically"
uk_pred = limit(src(W6, "g_pred"), 4)
uk_anom = limit(src(W6, "g_anom"), 4)
uk_conc = src(W6, "g_conc")
uk_graph = limit(src(W6, "g_graph"), 5)
uk_b1 = src.B(W6, "B1")
uk_b5 = src.B(W6, "B5")

INV = [("how the height of a ramp affects how far a toy car rolls", "the height of the ramp", "how far the car rolls", "the same car and the same floor surface"),
       ("how the amount of salt in water affects how fast bean seeds sprout", "the amount of salt", "how many days the seeds take to sprout", "the same kind of seed and the same temperature"),
       ("how the size of a parachute affects how long it takes to fall", "the size of the parachute", "the time it takes to fall", "the same drop height and the same load"),
       ("how the colour of a bottle affects how hot the water inside gets in the sun", "the colour of the bottle", "the temperature of the water", "the same amount of water and the same time in the sun"),
       ("how the length of a pendulum affects the time for 10 swings", "the length of the pendulum", "the time for 10 swings", "the same mass and the same starting angle"),
       ("how the temperature of water affects how fast a stock cube dissolves", "the temperature of the water", "the time to dissolve", "the same amount of water and the same kind of stock cube"),
       ("how the number of batteries affects how bright a lamp is", "the number of batteries", "the brightness of the lamp", "the same lamp and the same wires"),
       ("how the type of surface affects how far a marble rolls", "the type of surface", "the distance the marble rolls", "the same marble and the same push"),
       ("how the amount of light affects the growth of wheat seedlings", "the amount of light", "the height of the seedlings", "the same soil and the same amount of water"),
       ("how the thickness of an elastic band affects how far it can stretch", "the thickness of the band", "how far it stretches", "the same length of band and the same mass hung on it")]


def g_ivdv():
    t, iv, dv, cv = R.choice(INV)
    k = R.choice(["iv", "dv", "cv"])
    if not once(("ivdv", t, k)):
        return None
    q = {"iv": "Which is the independent variable (the one you change)?", "dv": "Which is the dependent variable (the one you measure)?",
         "cv": "Which variables should be controlled (kept the same)?"}[k]
    a = {"iv": iv, "dv": dv, "cv": cv}[k]
    w = [x for x in (iv, dv, cv) if x != a]
    other = R.choice([x for x in INV if x[0] != t])
    w.append({"iv": other[1], "dv": other[2], "cv": other[3]}[k])
    return tq("A class investigates %s. %s" % (t, q), a, w, "Change: %s. Measure: %s. Keep the same: %s." % (iv, dv, cv))


def line_svg(xs, ys, xl, yl, ymax, step):
    W, H, L, B = 340, 220, 50, 180
    sx = (W - L - 20) / (xs[-1] - xs[0])
    sy = (B - 20) / ymax
    g = "".join("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#ddd'/><text x='%d' y='%.1f' font-size='11' text-anchor='end'>%d</text>" %
                (L, B - v * sy, W - 20, B - v * sy, L - 4, B - v * sy + 4, v) for v in range(0, ymax + 1, step))
    g += "".join("<text x='%.1f' y='%d' font-size='11' text-anchor='middle'>%d</text>" % (L + (x - xs[0]) * sx, B + 15, x) for x in xs)
    pts = " ".join("%.1f,%.1f" % (L + (x - xs[0]) * sx, B - y * sy) for x, y in zip(xs, ys))
    g += "<polyline points='%s' fill='none' stroke='#2a6fdb' stroke-width='2.5'/>" % pts
    g += "".join("<circle cx='%.1f' cy='%.1f' r='3.5' fill='#2a6fdb'/>" % (L + (x - xs[0]) * sx, B - y * sy) for x, y in zip(xs, ys))
    g += "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333'/><line x1='%d' y1='20' x2='%d' y2='%d' stroke='#333'/>" % (L, B, W - 20, B, L, L, B)
    g += "<text x='%d' y='%d' font-size='12' text-anchor='middle'>%s</text>" % ((L + W - 20) // 2, B + 32, xl)
    g += "<text x='14' y='%d' font-size='12' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>" % ((B + 20) // 2, (B + 20) // 2, yl)
    return "<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='line graph of %s against %s'>%s</svg>" % (W, H + 20, W, yl, xl, g)


GR = [("Temperature of water in a black bottle in the sun", "Time (minutes)", "Temperature (°C)", [0, 10, 20, 30, 40, 50], [20, 26, 31, 35, 38, 40], 50, 10, "°C"),
      ("Height of a sunflower", "Week", "Height (cm)", [0, 1, 2, 3, 4, 5], [0, 4, 10, 18, 28, 40], 50, 10, "cm"),
      ("Temperature of a cup of tea cooling", "Time (minutes)", "Temperature (°C)", [0, 5, 10, 15, 20, 25], [80, 64, 52, 44, 38, 34], 90, 10, "°C"),
      ("Distance a toy car rolls from different ramp heights", "Ramp height (cm)", "Distance (cm)", [10, 20, 30, 40, 50, 60], [30, 62, 90, 122, 150, 180], 200, 40, "cm")]


def g_read():
    title, xl, yl, xs, ys, ymax, step, u = R.choice(GR)
    k = R.choice(["read", "when", "pattern"])
    if not once(("read", title, k)):
        return None
    svg = line_svg(xs, ys, xl, yl, ymax, step)
    i = R.randrange(1, len(xs) - 1)
    unit = lambda v: "%d %s" % (v, u) if u != "°C" else "%d °C" % v
    xname = xl.split(" (")[0].lower()
    if k == "read":
        return tq("%s<br>%s. What is the value when the %s is %d?" % (svg, title, xname, xs[i]), unit(ys[i]),
                  [unit(ys[i - 1]), unit(ys[i + 1]), unit(xs[i])], "Go up from %d on the bottom axis to the line, then across." % xs[i])
    if k == "when":
        j = len(xs) - 1
        return tq("%s<br>%s. At which %s was the value %s?" % (svg, title, xname, unit(ys[j])), str(xs[j]), [str(xs[j - 1]), str(xs[0]), str(ys[j])],
                  "Find %s on the side axis, go across to the line, then down." % unit(ys[j]))
    up = ys[-1] > ys[0]
    a = "As the %s increases, the %s %s." % (xname, yl.split(" (")[0].lower(), "increases" if up else "decreases")
    return tq("%s<br>%s. What pattern does the graph show?" % (svg, title), a,
              ["As the %s increases, the %s %s." % (xname, yl.split(" (")[0].lower(), "decreases" if up else "increases"), "There is no pattern.", "The values stay the same."],
              "Follow the line from left to right.")


GT = [("the number of each kind of bird seen at a waterhole", "a column graph"), ("the temperature in Alice Springs every hour for a day", "a line graph"),
      ("the favourite fruit of students in a class", "a column graph"), ("the height of a bean plant measured every day", "a line graph"),
      ("the amount of rain in each month of the year", "a column graph"), ("how far a car rolls from ramps of different heights", "a line graph"),
      ("the number of students who walk, ride or drive to school", "a column graph"), ("the temperature of cooling water every 2 minutes", "a line graph"),
      ("which of four materials kept ice frozen longest", "a column graph"), ("a baby's mass each month for a year", "a line graph")]


def g_type():
    d, g = R.choice(GT)
    return tq("Which graph is best for showing %s?" % d, g, [x for x in ["a column graph", "a line graph", "a pie chart", "no graph: just a sentence"] if x != g],
              "Use a column graph for separate groups and a line graph when both variables are numbers that change.")


OB = [("The water in the black bottle reached 40 °C.", "observation"), ("The black bottle got hotter because dark colours absorb more light.", "inference"),
      ("18 of the 20 slaters moved to the dark side.", "observation"), ("Slaters prefer the dark because it is safer from birds.", "inference"),
      ("The lamp glowed brighter with two batteries.", "observation"), ("Two batteries give the lamp more energy.", "inference"),
      ("The nail in salt water had the most rust after a week.", "observation"), ("Salt makes iron rust faster.", "inference"),
      ("The seedling in the cupboard was pale and 9 cm tall.", "observation"), ("The seedling grew tall and pale because it was looking for light.", "inference"),
      ("The ice cube wrapped in wool took 52 minutes to melt.", "observation"), ("Wool traps air, so it slows down heat moving into the ice.", "inference")]


def g_obs():
    st, k = R.choice(OB)
    return tq("Is this an observation or an inference (an explanation)? “%s”" % st, "an " + k,
              ["an " + x for x in ["observation", "inference"] if x != k] + ["a prediction made before the test", "a variable"],
              "An observation is what you saw or measured; an inference explains it.")


POOL1 = pool(R, [
    ("What is a hypothesis?", "a testable idea that explains what you think will happen and why", ["a list of results", "the equipment you use", "the title of a graph"], "For example: 'If the ramp is higher, the car will roll further because it gains more energy.'"),
    ("Which is the best hypothesis?", "If more light reaches the seedlings, they will grow taller because plants use light to make food.", ["Plants are green.", "I like seedlings.", "Seedlings grow."], "A good hypothesis names the variables and gives a reason."),
    ("Why do scientists record the unit in a table heading?", "so everyone knows what was measured and how", ["to make the table longer", "because units change the results", "units are not needed"], "Write units once in the heading, such as Time (s)."),
    ("When is a line graph better than a column graph?", "when both variables are numbers, such as time and temperature", ["when comparing kinds of animals", "when the data are colours", "never"], "Line graphs show change."),
    ("Which axis usually shows the independent variable?", "the horizontal (bottom) axis", ["the vertical (side) axis", "neither axis", "the title"], "The variable you change goes along the bottom."),
    ("Why should a sample be large, such as 30 seeds instead of 2?", "Results from more seeds are more reliable.", ["Fewer seeds are always better.", "It makes the test unfair.", "It changes the variable."], "A bigger sample reduces the effect of chance."),
    ("What is a controlled variable?", "a variable kept the same so the test is fair", ["the variable you change", "the variable you measure", "a variable that is ignored"], "Controlled variables stop other things affecting the result."),
    ("A scientist publishes results so others can repeat the test. Why is this important?", "Others can check whether they get the same results.", ["It keeps the results secret.", "It changes the results.", "It makes the test unfair."], "Science is checked by others."),
])
POOL5 = pool(R, [
    ("Mia tested 3 parachutes once each. How could she improve her method?", "repeat each test several times and find the average", ["test only one parachute", "change two variables at once", "drop each from a different height"], "Repeats make results more reliable."),
    ("Jack's graph shows that seedlings in more light grew taller, but he only grew 2 seedlings. How confident should he be?", "not very confident: he should grow more seedlings", ["completely confident", "the graph proves it for all plants", "it does not matter"], "Small samples can mislead."),
    ("Ruby says her results prove all metals rust in salt water. She only tested iron nails. What is wrong?", "Her conclusion goes further than her data.", ["Nothing is wrong.", "She should have used fewer nails.", "Iron is not a metal."], "Conclusions must match what was tested."),
    ("Kai reads in an advertisement that a drink 'makes you run faster'. What should a scientist ask?", "What evidence is there, and was it a fair test?", ["What colour is the can?", "Who is the most famous runner?", "How much does it cost?"], "Ask for evidence."),
    ("Ella's measurements of a plant's height are 12 cm, 12 cm and 21 cm on the same day. What is the most likely reason for the 21 cm?", "a mistake in measuring or recording", ["the plant grew 9 cm in a few minutes", "plants change height when measured", "the ruler stretched"], "Check results that do not fit."),
    ("Which is the clearest way to report an investigation to the class?", "question, method, results table and graph, conclusion", ["only the conclusion", "a list of equipment only", "a photo of the class"], "Others should be able to repeat it."),
    ("Noah tests sunscreen with UV beads that change colour in sunlight. Why should all beads be put in the sun at the same time?", "so the amount of sunlight is controlled", ["so the beads change colour faster", "so the results are different", "it does not matter"], "Sunlight changes during the day."),
    ("A data logger records the temperature every minute. What is an advantage over reading a thermometer by hand?", "It takes many accurate readings without anyone watching.", ["It changes the temperature.", "It makes the test unfair.", "It only works at night."], "Digital tools help collect data."),
])


def main():
    sets = U.sets([
        ("Questions and hypotheses", [(POOL1, 5), (uk_pred, 4), (uk_b1, 4), (g_obs, 7)]),
        ("Variables", [(g_ivdv, 18), (POOL1, 2)]),
        ("Graphs", [(g_read, 10), (g_type, 7), (uk_graph, 3)]),
        ("Patterns and conclusions", [(uk_anom, 4), (uk_conc, 4), (g_ivdv, 6), (g_obs, 3), (g_read, 2), (uk_b1, 1)]),
        ("Evaluating and communicating", [(POOL5, 8), (uk_b5, 5), (g_type, 3), (g_ivdv, 4)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S6I01, AC9S6I02, AC9S6I03, AC9S6I04, AC9S6I05, AC9S6I06", "Science inquiry",
            "Pose investigable questions and hypotheses; plan fair tests, identifying the independent, dependent and controlled variables; "
            "use equipment and digital tools to collect data; construct and read tables and graphs; identify patterns and anomalies; "
            "evaluate methods; and communicate findings (summary of the Australian Curriculum v9.0 Year 6 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 6 science worksheets on working scientifically: hypotheses, independent, dependent and controlled variables, line "
            "and column graphs, anomalies, conclusions and evaluating evidence. 100 questions with answers.",
            "Change one, measure one, control the rest.", "The independent variable is changed, the dependent is measured, controlled variables stay the same.",
            "<p><b>Every fair test has three kinds of variable.</b></p><ul>"
            "<li>Independent variable: the one you change on purpose (it goes on the bottom axis of a graph).</li>"
            "<li>Dependent variable: the one you measure (it goes on the side axis).</li>"
            "<li>Controlled variables: everything you keep the same. Repeat the test, look for the pattern, and check any result that does not fit.</li></ul>",
            [("Ramp height and distance rolled. Which variable do you change?", ["you choose the ramp height"], "ramp height (independent)"),
             ("Temperature every 10 minutes. Which graph?", ["both variables are numbers", "the data change over time"], "a line graph")],
            ["Swapping the independent variable (changed) and the dependent variable (measured).", "Choosing a column graph for data that change over time.",
             "Writing a conclusion that goes further than the results."],
            [("What are independent, dependent and controlled variables?", "The independent variable is the one you change. The dependent variable is the one you measure. Controlled variables are kept the same so the test is fair."),
             ("What is the difference between an observation and an inference?", "An observation is what you see or measure, such as 'the water reached 40 °C'. An inference is an explanation of it, such as 'dark colours absorb more light'."),
             ("How do I read a line graph?", "Find the value on the bottom axis, go straight up to the line, then go across to the side axis and read the value. Check the units.")],
            sets)


if __name__ == "__main__":
    main()
