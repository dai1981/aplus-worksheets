# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, Science inquiry (AC9S8I01-I06): planning investigations, identifying variables,
analysing data in tables and graphs, describing relationships, interpolating and extrapolating, evaluating claims and methods,
and using models.
  python tools/gen_au_science_y8_working_scientifically.py
Own data tables and claim questions, plus the AU Year 6 inquiry makers and the US Grade 6 engineering design makers.
Wrong answers come from real mistakes: reading a correlation as a cause, trusting a claim from a tiny sample or with no control
group, and extrapolating far beyond the data.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once

YEAR, SORT = 8, 8
U, R, P, src = AU(seed_of(YEAR, SORT))

Y6 = src.mod("gen_au_science_y6_working_scientifically")
y6_ivdv = limit(Y6.g_ivdv, 8)
EN = "gen_us_science_g6_engineering_design_process"
en_cc = limit(src(EN, "g_cc"), 10)
en_mat = limit(src(EN, "g_matrix"), 8)
en_b1 = src.B(EN, "B1")

import math

CTX = [  # independent, unit, dependent, unit, kind, x values
    ("mass hung on a spring", "g", "stretch", "cm", "prop", [[50, 100, 150, 200, 250], [100, 200, 300, 400, 500]]),
    ("time a kettle is switched on", "s", "energy used", "kJ", "prop", [[10, 20, 30, 40, 50], [20, 40, 60, 80, 100]]),
    ("number of coils on an electromagnet", "", "number of paperclips picked up", "", "prop", [[10, 20, 30, 40, 50], [20, 40, 60, 80, 100]]),
    ("volume of water in a kettle", "mL", "time to boil", "s", "prop", [[250, 500, 750, 1000, 1250], [200, 400, 600, 800, 1000]]),
    ("height of a ramp", "cm", "speed of a trolley at the bottom", "cm/s", "up", [[10, 20, 30, 40, 50], [20, 40, 60, 80, 100]]),
    ("length of a pendulum", "cm", "time for 10 swings", "s", "up", [[20, 40, 60, 80, 100], [25, 50, 75, 100, 125]]),
    ("thickness of insulation around a can", "mm", "temperature drop in 10 minutes", "°C", "down", [[0, 5, 10, 15, 20], [0, 10, 20, 30, 40]]),
    ("temperature of water", "°C", "time for a tablet to dissolve", "s", "down", [[20, 30, 40, 50, 60], [15, 25, 35, 45, 55]]),
    ("distance from a lamp", "cm", "light reading", "lux", "down", [[20, 40, 60, 80, 100], [30, 60, 90, 120, 150]]),
    ("shoe size of students", "", "score on a science quiz (out of 20)", "", "none", [[5, 6, 7, 8, 9], [6, 7, 8, 9, 10]]),
]
SLOPE = {"mass hung on a spring": [0.02, 0.04, 0.06], "time a kettle is switched on": [1.5, 2, 2.4],
         "number of coils on an electromagnet": [0.2, 0.3, 0.4], "volume of water in a kettle": [0.12, 0.16, 0.2]}
DESC = {"prop": "As the {iv} increases, the {dv} increases in proportion (doubling one doubles the other).",
        "up": "As the {iv} increases, the {dv} increases, but not in proportion.",
        "down": "As the {iv} increases, the {dv} decreases.",
        "none": "There is no clear relationship between the {iv} and the {dv}."}


def fmt(v):
    v = round(v, 1)
    return "{:,}".format(int(v)) if v >= 10000 and v == int(v) else "%g" % v


def series(c):
    iv, iu, dv, du, kind, opts = c
    xs = R.choice(opts)
    if kind == "prop":
        m = R.choice(SLOPE[iv])
        ys = [m * x for x in xs]
    elif kind == "up":
        if "ramp" in iv:
            k = R.choice([0.7, 0.8, 0.9])
            ys = [round(k * math.sqrt(2 * 9.8 * x / 100) * 100) for x in xs]
        else:
            ys = [round(10 * 2 * math.pi * math.sqrt(x / 100 / 9.8) + R.choice([-0.2, 0, 0.2]), 1) for x in xs]
    elif kind == "down":
        if "lamp" in iv:
            k = R.choice([400000, 600000, 900000])
            ys = [round(k / x ** 2, -1 if k / x ** 2 > 100 else 0) for x in xs]
        elif "insulation" in iv:
            top = R.randint(26, 34)
            ys = [round(top * 8 / (8 + x)) for x in xs]
        else:
            k = R.choice([3600, 4200, 4800])
            ys = [round(k / x) for x in xs]
    else:
        ys = R.sample(range(8, 20), 5)
        if ys == sorted(ys) or ys == sorted(ys, reverse=True):
            return None
    return xs, ys


def table(iv, iu, dv, du, xs, ys):
    h = lambda n, u: n[0].upper() + n[1:] + (" (%s)" % u if u else "")
    return "<table class='sn-table'><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></table>" % (
        h(iv, iu), "".join("<td>%s</td>" % fmt(x) for x in xs), h(dv, du), "".join("<td>%s</td>" % fmt(y) for y in ys))


def g_rel():
    c = R.choice(CTX)
    iv, iu, dv, du, kind = c[:5]
    s = series(c)
    if not s:
        return None
    xs, ys = s
    if not once(("rel", iv, xs[0], ys[0], ys[-1])):
        return None
    a = DESC[kind].format(iv=iv, dv=dv)
    w = [DESC[k].format(iv=iv, dv=dv) for k in DESC if k != kind]
    return tq("%sWhich statement best describes the relationship in the table?" % table(iv, iu, dv, du, xs, ys), a, w,
              "Look at how the %s changes as the %s goes up." % (dv, iv))


def g_interp():
    c = R.choice([c for c in CTX if c[4] == "prop"])
    iv, iu, dv, du = c[:4]
    xs, ys = series(c)
    m = ys[0] / xs[0]
    i = R.randrange(4)
    xq = (xs[i] + xs[i + 1]) / 2
    if not once(("int", iv, xs[0], round(m, 3), xq)):
        return None
    yq = m * xq
    if not du and yq != int(yq):
        return None
    step = ys[1] - ys[0]
    f = lambda v: (fmt(v) + " " + du).strip()
    return tq("%sUse the pattern to estimate the %s when the %s is %s%s." % (table(iv, iu, dv, du, xs, ys), dv, iv, fmt(xq), (" " + iu) if iu else ""),
              f(yq), [f(yq + step), f(yq - step / 2), f(xq)], "%s is halfway between %s and %s, so the %s is halfway between %s and %s: %s (interpolation)." %
              (fmt(xq), fmt(xs[i]), fmt(xs[i + 1]), dv, fmt(ys[i]), fmt(ys[i + 1]), f(yq)))


def g_extra():
    c = R.choice([c for c in CTX if c[4] == "prop"])
    iv, iu, dv, du = c[:4]
    xs = R.choice(c[5])
    big = xs[-1] * R.choice([10, 20])
    if not once(("ex", iv, xs[0], big)):
        return None
    u = (" " + iu) if iu else ""
    return tq("A class measured the %s for a %s from %s to %s%s. Why is it risky to predict the result for %s%s?" % (dv, iv, fmt(xs[0]), fmt(xs[-1]), u, fmt(big), u),
              "It is far outside the range tested, so the pattern may not continue.", ["It is inside the range tested.", "Predictions are never allowed in science.", "Larger values are always more accurate."],
              "Extrapolating far beyond the data is unreliable; for example, a spring can overstretch.")


CLAIMS = [
    ("A company says its energy drink improves test scores because 3 students who drank it scored well.", "The sample is far too small and there is no comparison group."),
    ("An advert says a cream 'removes wrinkles in 7 days', based on a study paid for by the cream company.", "The study may be biased, so it should be checked by independent scientists."),
    ("A website says ice-cream sales and shark sightings both rise in summer, so ice-cream attracts sharks.", "Both are caused by hot weather; a correlation does not show cause."),
    ("A student says a new fertiliser works because her one tomato plant grew tall.", "There was no control plant without fertiliser and only one plant."),
    ("A post says a magnetic bracelet cures back pain, based on people's stories.", "Stories are not a controlled test; a blind trial with a control group is needed."),
    ("A sports shoe company says its shoe makes you run 20% faster, tested on its own sponsored athletes.", "The test is not fair or independent; the athletes may already be fast."),
    ("A survey of 10 people at a Bondi surf club says 90% of Australians love surfing.", "The sample is small and not representative of all Australians."),
    ("A friend says rain always comes after his footy team wins, because it happened twice.", "Two events are not enough data, and there is no reason one causes the other."),
]
CW = ["The claim is proven because it was published online.", "The claim must be true because many people believe it.",
      "Nothing is wrong; one result is enough.", "The claim is wrong because the scientists were young."]


def g_claim():
    c, a = R.choice(CLAIMS)
    if not once(("cl", c)):
        return None
    return tq("%s What is the main problem with this claim?" % c, a, R.sample(CW, 3), "Good evidence needs a fair test, a large sample, a control and no bias.")


POOL1 = pool(R, [
    ("What is the independent variable?", "the variable you change on purpose", ["the variable you measure", "the variables you keep the same", "the result"], "It goes on the x-axis."),
    ("What is the dependent variable?", "the variable you measure", ["the variable you change", "a variable you keep the same", "the title of the graph"], "It depends on the independent variable."),
    ("Why does an experiment need a control?", "to compare results with and without the change being tested", ["to make it longer", "so the results are always the same", "to change two variables"], "A control shows what happens normally."),
    ("What is a correlation?", "a relationship where two variables change together", ["proof that one variable causes another", "a single result", "a type of graph only"], "Correlation does not always mean cause."),
    ("What is interpolation?", "estimating a value between measured data points", ["guessing far beyond the data", "removing anomalies", "repeating a test"], "It is safer than extrapolation."),
    ("What is extrapolation?", "extending a pattern beyond the measured data", ["measuring more carefully", "drawing a column graph", "finding the mean"], "It is less reliable."),
    ("Why do scientists use models, such as a model of particles?", "to explain and predict things that are too small, big or complex to see directly", ["because models are always perfectly accurate", "to replace experiments", "to make science harder"], "Every model has limitations."),
    ("What is a limitation of a ball-and-stick model of a molecule?", "Real atoms are not solid balls and bonds are not sticks.", ["It shows too many atoms.", "It is too accurate.", "It has no limitations."], "Models simplify reality."),
    ("What is a controlled variable?", "a variable kept the same so the test is fair", ["the variable you change", "the variable you measure", "a variable nobody can measure"], "Example: the same amount of water for every plant."),
    ("What is a hypothesis?", "a testable explanation that predicts what will happen and why", ["a final result", "a list of equipment", "a guess with no reason"], "It is tested by an experiment."),
    ("What is an anomaly (outlier) in a set of results?", "a result that does not fit the pattern of the others", ["the average result", "the first result", "the independent variable"], "Check and repeat anomalies."),
    ("Why should a sample be random?", "so it represents the whole group without bias", ["so it is smaller", "so the results are the same", "so the test is quicker"], "Choosing only some people can bias results."),
    ("What is bias in a study?", "something that unfairly pushes results one way", ["a type of graph", "a controlled variable", "a random error that cancels out"], "Who pays for a study can cause bias."),
    ("Why is a blind trial used to test a new medicine?", "so people's expectations do not affect the results", ["to save money", "so nobody takes the medicine", "to make it faster"], "Some people get a placebo without knowing."),
    ("Which graph is best to show how plant height changes over 6 weeks?", "a line graph", ["a pie chart", "a column graph of plant names", "no graph"], "Use a line graph for continuous data over time."),
    ("Which graph is best to compare the number of each type of bird seen in a park?", "a column graph", ["a line graph", "a scatter plot", "a pie chart of temperatures"], "Categories suit a column graph."),
])
POOL5 = pool(R, [
    ("Mia tests whether the colour of a car affects how hot it gets inside. Which question is testable?", "Does the colour of a car affect the temperature inside after 1 hour in the sun?", ["Which car colour is best?", "Are black cars nicer?", "Why do people buy white cars?"], "A testable question names the variables."),
    ("Jack's results: one trial is much higher than the rest. What should he do first?", "check for a mistake and repeat that trial", ["delete all his data", "include it without checking", "change his hypothesis"], "Anomalies should be checked."),
    ("Ruby's hypothesis was not supported by her data. What should she do?", "report the result honestly and suggest why", ["change the data", "say the hypothesis was right", "stop doing science"], "Unsupported hypotheses still teach us something."),
    ("Kai uses a data logger instead of a stopwatch. How does this improve his investigation?", "It reduces human reaction-time error and records more readings.", ["It changes the independent variable.", "It makes the test unfair.", "It removes the need for a hypothesis."], "Better equipment improves accuracy."),
    ("Ella's scatter plot shows points close to a straight line going up. What does this suggest?", "a strong positive correlation", ["no correlation", "a negative correlation", "the data is wrong"], "Points close to a rising line show a strong positive link."),
    ("CSIRO scientists test a new drought-tolerant wheat in 50 paddocks across three states. Why so many?", "to make the results reliable across different soils and weather", ["to use up seed", "because one paddock is enough", "to change the variable"], "Large, varied samples make conclusions stronger."),
    ("Noah's experiment gives results that agree closely, but his ruler was missing the first 1 cm. What kind of error is this?", "a systematic error", ["a random error", "no error", "an anomaly"], "Every reading is shifted by the same amount."),
    ("Harper says her results prove that more sunlight makes tomatoes taste sweeter. What would make her conclusion stronger?", "testing many plants in each group and measuring sugar content, not just taste", ["testing one plant", "asking only her friends", "using different soil for each group"], "Measured data from many plants is more reliable."),
    ("Liam's model of the solar system shows the planets the right order but all close together. What is its limitation?", "The distances are not to scale.", ["It has too many planets.", "It is perfectly accurate.", "The Sun should be at the edge."], "Models often trade accuracy for convenience."),
    ("A Bureau of Meteorology graph shows Australia's average temperature rising since 1910. Why do scientists trust it?", "It uses many years of measurements from many weather stations.", ["It comes from one day of data.", "It was drawn by hand.", "It is a prediction only."], "Large, long-term data sets make trends reliable."),
    ("Aarav repeats his test five times and gets almost the same answer each time. What does this show?", "His results are repeatable (precise).", ["His results must be accurate.", "He changed the variable.", "His hypothesis is wrong."], "Repeatable results may still have a systematic error."),
    ("Zara wants to know how the angle of a solar panel affects its power. Which variable must be kept the same?", "the time of day and the panel used", ["the angle", "the power output", "nothing"], "Control everything except the angle."),
])


def main():
    sets = U.sets([
        ("Questions and variables", [(POOL1, 5), (y6_ivdv, 8), (POOL5, 3), (en_b1, 2), (en_cc, 2)]),
        ("Relationships in data", [(g_rel, 10), (POOL1, 3), (g_interp, 5), (g_extra, 2)]),
        ("Interpolating and extrapolating", [(g_interp, 8), (g_extra, 5), (g_rel, 4), (POOL1, 2), (en_mat, 1)]),
        ("Evaluating claims", [(g_claim, 8), (POOL5, 4), (POOL1, 3), (en_mat, 3), (en_cc, 2)]),
        ("Models and design", [(en_cc, 4), (en_mat, 3), (en_b1, 4), (POOL1, 3), (POOL5, 5), (g_extra, 1)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S8I01, AC9S8I02, AC9S8I03, AC9S8I04, AC9S8I05, AC9S8I06", "Science inquiry",
            "Develop investigable questions and hypotheses; plan and conduct safe, valid investigations controlling variables; analyse "
            "data to identify relationships and anomalies; evaluate claims and methods; and use models and representations "
            "(summary of the Australian Curriculum v9.0 Year 8 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 8 science worksheets on working scientifically: variables and controls, relationships in data, interpolation and "
            "extrapolation, evaluating claims, correlation and cause, and models. 100 questions with answers.",
            "Correlation is not cause.", "Look for a fair test, a large sample, a control group and no bias before trusting a claim.",
            "<p><b>Good science needs fair tests and careful thinking about data.</b></p><ul>"
            "<li>Change one independent variable, measure the dependent variable, and control the rest. Use a control group to compare.</li>"
            "<li>Describe relationships from tables and graphs; interpolate between points, and be careful extrapolating beyond them.</li>"
            "<li>Evaluate claims: Is the sample large? Is there a control? Who paid for it? Could something else cause the pattern?</li></ul>",
            [("Mass 10, 20, 30 g; stretch 4, 8, 12 cm. Stretch for 25 g?", ["each 10 g adds 4 cm", "25 g → 10 cm"], "10 cm"),
             ("Ice-cream sales and drownings both rise in summer. Cause?", ["both rise with hot weather"], "no; correlation is not cause")],
            ["Thinking a correlation proves cause.", "Trusting a claim from a tiny sample or with no control group.",
             "Extrapolating far beyond the range of the data."],
            [("What is the difference between interpolation and extrapolation?", "Interpolation estimates a value between data points you measured. Extrapolation extends the pattern beyond your data, which is less reliable."),
             ("How do I evaluate a claim?", "Ask whether it was a fair test with a control, whether the sample was large and representative, who paid for the study, and whether something else could explain the result."),
             ("Why are models useful if they are not perfect?", "Models help explain and predict things that are hard to see, such as particles or the solar system. Scientists improve models when new evidence appears.")],
            sets)


if __name__ == "__main__":
    main()
