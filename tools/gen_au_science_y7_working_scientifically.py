# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, Science inquiry (AC9S7I01-I06): hypotheses, independent, dependent and controlled
variables, laboratory safety and hazard symbols, choosing equipment and SI units, reading graphs, reliability, accuracy and precision.
  python tools/gen_au_science_y7_working_scientifically.py
Reuses the SG Secondary 1 scientific endeavour makers and the AU Year 6 inquiry makers, plus own questions on accuracy, precision,
reliability and validity. Wrong answers come from real mistakes: confusing accuracy with precision, thinking more decimal places
always means more accurate, and keeping an anomalous result in the mean without checking it.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

SE = "gen_sg_science_s1_the_scientific_endeavour"
se_app = limit(src(SE, "g_app"), 8)
se_haz = src(SE, "g_haz")
se_unit = src(SE, "g_unit")
se_var = limit(src(SE, "g_var"), 10)
se_b1 = src.B(SE, "B1")
se_b5 = src.B(SE, "B5")
Y6 = src.mod("gen_au_science_y6_working_scientifically")
y6_read = Y6.g_read
y6_type = Y6.g_type
y6_obs = Y6.g_obs


def g_mean():
    from au_sci import once
    ctx = R.choice([("time for a trolley to roll down a ramp", "s", 1), ("temperature rise of water heated for 2 minutes", "°C", 1),
                    ("height of bean seedlings after 10 days", "cm", 1), ("distance a paper plane flew", "m", 1)])
    if not once(("mean7", ctx[0])):
        return None
    base = R.randint(20, 60) / 10
    xs = [round(base + d, 1) for d in R.sample([-0.2, -0.1, 0.0, 0.1, 0.2], 3)]
    out = round(base + R.choice([1.5, -1.5, 2.0]), 1)
    data = xs + [out]
    R.shuffle(data)
    m = round(sum(xs) / 3, 2)
    f = lambda v: ("%g %s" % (v, ctx[1])) if ctx[1] != "°C" else "%g °C" % v
    if len({f(round(m, 1)), f(round(sum(data) / 4, 1)), f(out), f(round(max(xs), 1))}) < 4:
        return None
    return tq("A student measured the %s four times: %s. Ignoring the anomalous result, what is the mean?" % (ctx[0], ", ".join(f(x) for x in data)),
              f(round(m, 1)), [f(round(sum(data) / 4, 1)), f(out), f(round(max(xs), 1))],
              "The anomaly is %s. Mean of the other three: %s ÷ 3 = %s." % (f(out), "%g" % round(sum(xs), 1), f(round(m, 1))))


POOL1 = pool(R, [
    ("What is a hypothesis?", "a testable explanation or prediction based on scientific ideas", ["a list of results", "a final conclusion", "a guess with no reason"], "Example: 'If the temperature increases, sugar will dissolve faster because particles move faster.'"),
    ("What does 'accurate' mean for a measurement?", "close to the true value", ["has many decimal places", "the same every time", "measured quickly"], "Accuracy is about closeness to the true value."),
    ("What does 'precise' mean for a set of measurements?", "the results are close to each other", ["the results are close to the true value", "measured with a ruler", "only one result"], "Precise results have little spread."),
    ("Why do scientists repeat measurements and calculate a mean?", "to reduce the effect of random errors and improve reliability", ["to make the results bigger", "because one result is always wrong", "to change the variable"], "Repeats show whether results are consistent."),
    ("What is a valid investigation?", "one that tests what it is meant to test, with other variables controlled", ["one that gives the expected result", "one that is short", "one that uses expensive equipment"], "Valid means it answers the question fairly."),
    ("What is a random error?", "unpredictable variation, such as reaction time when using a stopwatch", ["the same mistake every time", "a broken thermometer reading 2 °C too high", "a planned change"], "Repeats reduce the effect of random errors."),
    ("What is a systematic error?", "an error that shifts every result in the same way, such as a balance not zeroed", ["a random mistake", "an anomalous result", "a variable you change"], "Repeats do not remove systematic errors."),
    ("A thermometer reads 2 °C in ice water. What kind of error is this?", "a systematic (zero) error", ["a random error", "no error", "an anomaly only"], "Pure ice water should read 0 °C."),
    ("Which measurement is most precise?", "12.35 cm (measured to 0.01 cm)", ["12 cm", "about 12 cm", "12.4 cm"], "Precision depends on the smallest division used."),
    ("Why should a risk assessment be done before an experiment?", "to identify hazards and plan how to stay safe", ["to make the results more accurate", "to choose the graph", "it is not needed"], "Safety first."),
    ("Which variable goes on the x-axis of a line graph?", "the independent variable", ["the dependent variable", "the controlled variable", "the units only"], "The dependent variable goes on the y-axis."),
    ("What is peer review in science?", "other scientists checking work before it is published", ["students marking homework", "repeating one test", "drawing a graph"], "It helps catch errors."),
])
POOL5 = pool(R, [
    ("Mia's four results are 5.1 s, 5.0 s, 5.2 s and 5.1 s. The true value is 6.0 s. How would you describe them?", "precise but not accurate", ["accurate and precise", "accurate but not precise", "neither"], "They agree closely but are far from the true value."),
    ("Jack's balance reads 0.3 g with nothing on it. What should he do?", "zero (tare) the balance before measuring", ["subtract 3 g", "ignore it", "add 0.3 g to each result"], "This removes a systematic error."),
    ("Ruby tests if fertiliser affects plant growth using 2 plants. How could she improve reliability?", "use more plants in each group and repeat", ["use 1 plant", "change the light too", "measure only once"], "Larger samples are more reliable."),
    ("Kai's graph of temperature against time is a straight line going up. What does this show?", "Temperature increased steadily with time.", ["Temperature fell.", "There is no relationship.", "Time depends on temperature."], "A straight upward line shows a steady increase."),
    ("Ella says her conclusion is proven because one test worked. What is wrong?", "One test is not enough; results must be repeated and checked.", ["Nothing is wrong.", "She should not write conclusions.", "Tests always prove ideas."], "Science gathers evidence over many tests."),
    ("A class measures the boiling point of water as 98 °C, 99 °C and 98 °C. Why might this differ from 100 °C?", "Air pressure, impurities or thermometer error can change the reading.", ["Water never boils at 100 °C.", "The class made it up.", "Boiling point changes every day for no reason."], "Look for sources of error."),
    ("Which change makes an investigation more valid?", "controlling all variables except the one being tested", ["using brighter colours on the graph", "writing the conclusion first", "testing only once"], "Validity is about a fair test."),
    ("Why do scientists publish their methods in detail?", "so others can repeat the investigation and check the results", ["to make reports longer", "so nobody can copy them", "to hide errors"], "Reproducibility builds trust in results."),
    ("Noah uses a stopwatch to time a ball falling 1 m. Why are his times so variable?", "Human reaction time adds random error to short times.", ["Gravity changes.", "The ball changes mass.", "The stopwatch is too accurate."], "Use a longer fall or a light gate."),
])


def main():
    sets = U.sets([
        ("Hypotheses and variables", [(POOL1, 4), (se_var, 10), (se_b1, 4), (y6_obs, 2)]),
        ("Safety and equipment", [(se_haz, 8), (se_app, 7), (se_unit, 4), (se_b5, 1)]),
        ("Accuracy, precision and errors", [(POOL1, 8), (g_mean, 4), (POOL5, 3), (se_b5, 3), (se_unit, 2)]),
        ("Graphs and patterns", [(y6_read, 8), (y6_type, 6), (y6_obs, 4), (se_b1, 2)]),
        ("Evaluating investigations", [(POOL5, 6), (se_b1, 1), (y6_read, 4), (y6_type, 3), (y6_obs, 4), (se_haz, 2)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S7I01, AC9S7I02, AC9S7I03, AC9S7I04, AC9S7I05, AC9S7I06", "Science inquiry",
            "Develop investigable questions and hypotheses; plan safe, valid investigations, identifying variables and hazards; select "
            "equipment and record data accurately; represent data in tables and graphs; analyse patterns and errors; and evaluate "
            "methods and conclusions (summary of the Australian Curriculum v9.0 Year 7 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 7 science worksheets on working scientifically: hypotheses, variables, lab safety and hazard symbols, SI units, "
            "accuracy, precision, errors, graphs and evaluating investigations. 100 questions with answers.",
            "Accurate is close to true; precise is close together.", "Control variables, repeat measurements and look for errors to make results reliable and valid.",
            "<p><b>Good investigations are safe, valid and reliable.</b></p><ul>"
            "<li>State a hypothesis; change the independent variable, measure the dependent variable and control the rest.</li>"
            "<li>Accurate results are close to the true value; precise results are close to each other. Repeats reduce random error; zeroing removes some systematic errors.</li>"
            "<li>Graph the data (independent variable on the x-axis), find the pattern, check anomalies and evaluate the method.</li></ul>",
            [("5.1, 5.0, 5.2 s; true value 6.0 s?", ["close together", "far from the true value"], "precise but not accurate"),
             ("Balance reads 0.3 g when empty. Fix?", ["every reading is 0.3 g too high"], "zero (tare) it")],
            ["Confusing accuracy (close to the true value) with precision (close together).", "Thinking more decimal places always means more accurate.",
             "Including an anomalous result in the mean without checking it."],
            [("What is the difference between accuracy and precision?", "Accuracy is how close a measurement is to the true value. Precision is how close repeated measurements are to each other."),
             ("What is the difference between random and systematic errors?", "Random errors change unpredictably from one measurement to the next; repeating helps. Systematic errors shift all results the same way, such as an unzeroed balance."),
             ("What makes an investigation valid?", "It tests what it claims to test: only the independent variable changes, and all other variables are controlled.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
